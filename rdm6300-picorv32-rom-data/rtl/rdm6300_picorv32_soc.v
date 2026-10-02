// ============================================================================
// File: rtl/rdm6300_picorv32_soc.v
// Project: rdm6300-picorv32-rom-data
// Description: Top-Level Pure Structural RISC-V SoC containing:
//              - Master: PicoRV32 RISC-V RV32IMC CPU Core (rtl/picorv32.v)
//              - Bus: Central Memory Interconnect & Decoder (rtl/soc_interconnect.v)
//              - Slave 0: 1KB On-Chip Data SRAM (rtl/data_sram.v)
//              - Slave 1: SPI Flash XIP Controller (rtl/spimemio.v)
//              - Slave 2: RDM6300 RFID Controller & Pipeline (rtl/rdm6300_mmio.v)
//              - Slave 3: Host PC UART Controller with FIFOs (rtl/host_uart_mmio.v)
//              - Slave 4: GPIO LEDs & System Diagnostics (rtl/soc_gpio_mmio.v)
// ============================================================================

`timescale 1ns / 1ps

module rdm6300_picorv32_soc #(
    parameter CLK_FREQ_HZ         = 50_000_000,
    parameter UART_BAUD           = 9600,
    parameter [31:0] PROGADDR_RESET = 32'h0025_0000, // Reset vector into SPI Flash (offset 0x250000)
    parameter [31:0] PROGADDR_IRQ   = 32'h0025_0010,
    parameter [31:0] STACKADDR      = 32'h0000_0400  // End of 1KB SRAM (0x000 - 0x3FF)
)(
    input  wire        clk,
    input  wire        rst_n,

    // External RDM6300 RFID Interface (9600 Baud 8-N-1)
    input  wire        rdm6300_rx_i,

    // External Host PC UART Interface
    output wire        uart_tx_o,
    input  wire        uart_rx_i,

    // Physical QSPI Flash Interface (spimemio)
    output wire        flash_csb,
    output wire        flash_clk,

    output wire        flash_io0_oe,
    output wire        flash_io1_oe,
    output wire        flash_io2_oe,
    output wire        flash_io3_oe,

    output wire        flash_io0_do,
    output wire        flash_io1_do,
    output wire        flash_io2_do,
    output wire        flash_io3_do,

    input  wire        flash_io0_di,
    input  wire        flash_io1_di,
    input  wire        flash_io2_di,
    input  wire        flash_io3_di,

    // General Purpose I/O (Status LEDs & Test Pins)
    output wire [15:0] leds_o,

    // Processor & System Status Signals
    output wire        cpu_trap,
    output wire        card_event_o,
    output wire        flash_busy_o,
    output wire        flash_done_o
);

    localparam DEFAULT_DIV = CLK_FREQ_HZ / UART_BAUD;

    // ------------------------------------------------------------------------
    // PicoRV32 Native Memory Bus Signals
    // ------------------------------------------------------------------------
    wire        mem_valid;
    wire        mem_instr;
    wire        mem_ready;
    wire [31:0] mem_addr;
    wire [31:0] mem_wdata;
    wire [3:0]  mem_wstrb;
    wire [31:0] mem_rdata;

    // ------------------------------------------------------------------------
    // Slave Select Signals (Decoded by soc_interconnect)
    // ------------------------------------------------------------------------
    wire        sel_sram;
    wire        sel_spimem;
    wire        sel_spicfg;
    wire        sel_rfid;
    wire        sel_uart;
    wire        sel_gpio;

    // Slave Response Signals
    wire        sram_ready;
    wire [31:0] sram_rdata;

    wire        spimem_ready;
    wire [31:0] spimem_rdata;
    wire [31:0] spimemio_cfgreg_do;

    wire        rfid_ready;
    wire [31:0] rfid_rdata;

    wire        uart_ready;
    wire [31:0] uart_rdata;

    wire        gpio_ready;
    wire [31:0] gpio_rdata;

    // Flash Status Outputs
    assign flash_busy_o = !flash_csb;
    assign flash_done_o = flash_csb;

    // ========================================================================
    // 1. Central Bus Interconnect & Address Decoder
    // ========================================================================
    soc_interconnect u_interconnect (
        .cpu_mem_valid (mem_valid),
        .cpu_mem_addr  (mem_addr),
        .cpu_mem_rdata (mem_rdata),
        .cpu_mem_ready (mem_ready),

        .sel_sram      (sel_sram),
        .sel_spimem    (sel_spimem),
        .sel_spicfg    (sel_spicfg),
        .sel_rfid      (sel_rfid),
        .sel_uart      (sel_uart),
        .sel_gpio      (sel_gpio),

        .sram_rdata    (sram_rdata),
        .sram_ready    (sram_ready),

        .spimem_rdata  (spimem_rdata),
        .spimem_ready  (spimem_ready),
        .spimem_cfg_do (spimemio_cfgreg_do),

        .rfid_rdata    (rfid_rdata),
        .rfid_ready    (rfid_ready),

        .uart_rdata    (uart_rdata),
        .uart_ready    (uart_ready),

        .gpio_rdata    (gpio_rdata),
        .gpio_ready    (gpio_ready)
    );

    // ========================================================================
    // 2. PicoRV32 RISC-V CPU Core (Bus Master)
    // ========================================================================
    picorv32 #(
        .ENABLE_COUNTERS(1),
        .ENABLE_COUNTERS64(0),
        .ENABLE_REGS_16_31(1),
        .ENABLE_REGS_DUALPORT(1),
        .LATCHED_MEM_RDATA(0),
        .TWO_STAGE_SHIFT(1),
        .BARREL_SHIFTER(0),
        .TWO_CYCLE_COMPARE(0),
        .TWO_CYCLE_ALU(0),
        .COMPRESSED_ISA(0),
        .CATCH_MISALIGN(1),
        .CATCH_ILLINSN(1),
        .ENABLE_PCPI(0),
        .ENABLE_MUL(0),
        .ENABLE_FAST_MUL(0),
        .ENABLE_DIV(0),
        .ENABLE_IRQ(0),
        .ENABLE_IRQ_QREGS(0),
        .ENABLE_IRQ_TIMER(0),
        .MASKED_IRQ(32'hffff_ffff),
        .LATCHED_IRQ(32'hffff_ffff),
        .PROGADDR_RESET(PROGADDR_RESET),
        .PROGADDR_IRQ(PROGADDR_IRQ),
        .STACKADDR(STACKADDR)
    ) u_cpu (
        .clk(clk),
        .resetn(rst_n),
        .trap(cpu_trap),
        .mem_valid(mem_valid),
        .mem_instr(mem_instr),
        .mem_ready(mem_ready),
        .mem_addr(mem_addr),
        .mem_wdata(mem_wdata),
        .mem_wstrb(mem_wstrb),
        .mem_rdata(mem_rdata),
        .irq(32'd0),
        .eoi()
    );

    // ========================================================================
    // 3. Slave 0: 1KB On-Chip Data SRAM (0x0000_0000 - 0x0000_03FF)
    // ========================================================================
    data_sram #(
        .WORDS(256)
    ) u_data_sram (
        .clk(clk),
        .rst_n(rst_n),
        .valid(sel_sram),
        .addr(mem_addr[9:0]),
        .wdata(mem_wdata),
        .wstrb(mem_wstrb),
        .rdata(sram_rdata),
        .ready(sram_ready)
    );

    // ========================================================================
    // 4. Slave 1: SPI Flash XIP Controller (spimemio: 0x0010_0000 - 0x00FF_FFFF)
    // ========================================================================
    spimemio u_spimemio (
        .clk(clk),
        .resetn(rst_n),
        .valid(sel_spimem),
        .ready(spimem_ready),
        .addr(mem_addr[23:0]),
        .rdata(spimem_rdata),

        .flash_csb(flash_csb),
        .flash_clk(flash_clk),

        .flash_io0_oe(flash_io0_oe),
        .flash_io1_oe(flash_io1_oe),
        .flash_io2_oe(flash_io2_oe),
        .flash_io3_oe(flash_io3_oe),

        .flash_io0_do(flash_io0_do),
        .flash_io1_do(flash_io1_do),
        .flash_io2_do(flash_io2_do),
        .flash_io3_do(flash_io3_do),

        .flash_io0_di(flash_io0_di),
        .flash_io1_di(flash_io1_di),
        .flash_io2_di(flash_io2_di),
        .flash_io3_di(flash_io3_di),

        .cfgreg_we(sel_spicfg ? mem_wstrb : 4'b0000),
        .cfgreg_di(mem_wdata),
        .cfgreg_do(spimemio_cfgreg_do)
    );

    // ========================================================================
    // 5. Slave 2: RDM6300 RFID Controller & Decoder (0x1000_0000 - 0x1000_0008)
    // ========================================================================
    rdm6300_mmio #(
        .CLK_FREQ_HZ(CLK_FREQ_HZ),
        .UART_BAUD(UART_BAUD),
        .FRAME_TIMEOUT_CYCLES(CLK_FREQ_HZ / 200)
    ) u_rdm6300_mmio (
        .clk(clk),
        .rst_n(rst_n),
        .rdm_rx_i(rdm6300_rx_i),

        .valid(sel_rfid),
        .addr(mem_addr[3:0]),
        .wdata(mem_wdata),
        .wstrb(mem_wstrb),
        .rdata(rfid_rdata),
        .ready(rfid_ready),

        .card_event_o(card_event_o),
        .tag_raw_o(),
        .tag_ready_o()
    );

    // ========================================================================
    // 6. Slave 3: Host PC UART Controller with FIFOs (0x3000_0000 - 0x3000_0004)
    // ========================================================================
    host_uart_mmio #(
        .DEFAULT_DIV(DEFAULT_DIV),
        .FIFO_DEPTH(32)
    ) u_host_uart_mmio (
        .clk(clk),
        .rst_n(rst_n),
        .uart_rx_i(uart_rx_i),
        .uart_tx_o(uart_tx_o),

        .valid(sel_uart),
        .addr(mem_addr[3:0]),
        .wdata(mem_wdata),
        .wstrb(mem_wstrb),
        .rdata(uart_rdata),
        .ready(uart_ready)
    );

    // ========================================================================
    // 7. Slave 4: GPIO Status LEDs & Heartbeat Diagnostics (0x4000_0000)
    // ========================================================================
    soc_gpio_mmio u_soc_gpio_mmio (
        .clk(clk),
        .rst_n(rst_n),

        .valid(sel_gpio),
        .addr(mem_addr[3:0]),
        .wdata(mem_wdata),
        .wstrb(mem_wstrb),
        .rdata(gpio_rdata),
        .ready(gpio_ready),

        .cpu_trap(cpu_trap),
        .card_event_i(card_event_o),
        .flash_busy_i(flash_busy_o),
        .flash_done_i(flash_done_o),

        .leds_o(leds_o)
    );

endmodule
