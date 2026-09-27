// ============================================================================
// File: rdm6300_picorv32_soc.v
// Project: rdm6300-picorv32-rom-data
// Description: PicoRV32 RISC-V SoC with spimemio (XIP SPI Flash Controller),
//              Hardware RDM6300 RFID Decoder, 1KB SRAM, and Host PC UART.
// ============================================================================

`timescale 1ns / 1ps

module rdm6300_picorv32_soc #(
    parameter CLK_FREQ_HZ         = 50_000_000,
    parameter UART_BAUD           = 9600,
    parameter [31:0] PROGADDR_RESET = 32'h0025_0000, // Reset vector into SPI Flash (offset 0x250000, unified for ASIC & FPGA)
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
    output reg  [15:0] leds_o,

    // Processor Core Status
    output wire        cpu_trap,
    output wire        card_event_o,
    output wire        flash_busy_o,
    output wire        flash_done_o
);

    localparam DEFAULT_DIV = CLK_FREQ_HZ / UART_BAUD;

    // ------------------------------------------------------------------------
    // CDC Synchronizers for External Asynchronous Inputs
    // ------------------------------------------------------------------------
    wire rdm_rx_sync;
    wire pc_rx_sync;

    sync_2ff #(.RESET_VALUE(1'b1)) u_sync_rdm (
        .clk(clk),
        .rst_n(rst_n),
        .async_i(rdm6300_rx_i),
        .sync_o(rdm_rx_sync)
    );

    sync_2ff #(.RESET_VALUE(1'b1)) u_sync_pcrx (
        .clk(clk),
        .rst_n(rst_n),
        .async_i(uart_rx_i),
        .sync_o(pc_rx_sync)
    );

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

    // Memory Address Decoding:
    // 0x0000_0000 - 0x0000_03FF: 1KB Data SRAM (Read/Write, Stack & Variables)
    // 0x0010_0000 - 0x00FF_FFFF: 15MB Flash XIP via spimemio (Read-Only)
    // 0x0200_0000: SPIMEMIO Configuration & Manual SPI Bit-Bang Register
    // 0x1000_0000 - 0x1000_0007: RDM6300 RFID Status & Data Registers
    // 0x3000_0000 - 0x3000_0007: Host PC UART (simpleuart TX/RX)
    // 0x4000_0000 - 0x4000_0003: GPIO / LEDs
    wire sel_sram   = mem_valid && (mem_addr < 32'h0000_0400);
    wire sel_spimem = mem_valid && (mem_addr >= 32'h0010_0000 && mem_addr < 32'h0100_0000);
    wire sel_spicfg = mem_valid && (mem_addr == 32'h0200_0000);
    wire sel_rfid   = mem_valid && (mem_addr[31:28] == 4'h1);
    wire sel_uart   = mem_valid && (mem_addr[31:28] == 4'h3);
    wire sel_gpio   = mem_valid && (mem_addr[31:28] == 4'h4);

    wire        sram_ready;
    wire [31:0] sram_rdata;

    wire        spimem_ready;
    wire [31:0] spimem_rdata;
    wire [31:0] spimemio_cfgreg_do;

    wire        rfid_ready;
    wire [31:0] rfid_rdata;

    wire        uart_ready;
    wire [31:0] uart_rdata;

    reg         gpio_ready;
    reg  [31:0] gpio_rdata;

    assign mem_ready = sram_ready || spimem_ready || sel_spicfg || rfid_ready || uart_ready || gpio_ready;
    assign mem_rdata = sel_sram   ? sram_rdata   :
                       sel_spimem ? spimem_rdata :
                       sel_spicfg ? spimemio_cfgreg_do :
                       sel_rfid   ? rfid_rdata   :
                       sel_uart   ? uart_rdata   :
                       sel_gpio   ? gpio_rdata   : 32'd0;

    // ------------------------------------------------------------------------
    // PicoRV32 Core Instantiation
    // ------------------------------------------------------------------------
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

    // ------------------------------------------------------------------------
    // 1. Data SRAM 1KB (0x0000_0000 - 0x0000_03FF) - Read / Write
    // ------------------------------------------------------------------------
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

    // ------------------------------------------------------------------------
    // 2. SPI Flash XIP Controller (spimemio)
    // ------------------------------------------------------------------------
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

    assign flash_busy_o = !flash_csb;
    assign flash_done_o = flash_csb;

    // ------------------------------------------------------------------------
    // 3. Hardware RDM6300 RFID Receiver & Frame Decoder (0x1000_0000)
    // ------------------------------------------------------------------------
    wire        hw_rx_dv;
    wire [7:0]  hw_rx_byte;
    wire        hw_card_valid;
    wire [39:0] hw_tag_raw;

    uart_rx #(
        .CLKS_PER_BIT(CLK_FREQ_HZ / UART_BAUD)
    ) u_rdm_rx (
        .clk(clk),
        .rst_n(rst_n),
        .rx(rdm_rx_sync),
        .rx_dv(hw_rx_dv),
        .rx_byte(hw_rx_byte),
        .framing_error(),
        .break_detect()
    );

    rdm6300_frame_decoder #(
        .FRAME_TIMEOUT_CYCLES(CLK_FREQ_HZ / 200)
    ) u_rdm_decoder (
        .clk(clk),
        .rst_n(rst_n),
        .byte_valid(hw_rx_dv),
        .byte_data(hw_rx_byte),
        .byte_ready(),
        .card_valid(hw_card_valid),
        .tag_raw(hw_tag_raw),
        .checksum_error(),
        .frame_error(),
        .invalid_hex_error(),
        .frame_timeout_error()
    );

    reg        rfid_tag_ready;
    reg [7:0]  rfid_tag_hi;
    reg [31:0] rfid_tag_lo;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            rfid_tag_ready <= 1'b0;
            rfid_tag_hi    <= 8'd0;
            rfid_tag_lo    <= 32'd0;
        end else begin
            if (hw_card_valid) begin
                rfid_tag_ready <= 1'b1;
                rfid_tag_hi    <= hw_tag_raw[39:32];
                rfid_tag_lo    <= hw_tag_raw[31:0];
            end else if (sel_rfid && (|mem_wstrb) && (mem_addr[3:2] == 2'b00)) begin
                rfid_tag_ready <= 1'b0;
            end
        end
    end

    // Memory-mapped interface at 0x1000_0000:
    // 0x1000_0000: Status register (bit 0: rfid_tag_ready, write to clear)
    // 0x1000_0004: Tag Word Hi (8-bit version byte: tag_raw[39:32])
    // 0x1000_0008: Tag Word Lo (32-bit serial number: tag_raw[31:0])
    assign rfid_ready = sel_rfid;
    assign rfid_rdata = (mem_addr[3:2] == 2'b00) ? {31'd0, rfid_tag_ready} :
                        (mem_addr[3:2] == 2'b01) ? {24'd0, rfid_tag_hi}     :
                        (mem_addr[3:2] == 2'b10) ? rfid_tag_lo              : 32'd0;

    assign card_event_o = hw_card_valid;

    // ------------------------------------------------------------------------
    // 4. Host PC UART Interface (0x3000_0000)
    // ------------------------------------------------------------------------
    wire [31:0] pc_uart_div_do;
    wire [31:0] pc_uart_dat_do;
    wire        pc_uart_wait;

    wire pc_reg_div_sel = sel_uart && (mem_addr[2] == 1'b0);
    wire pc_reg_dat_sel = sel_uart && (mem_addr[2] == 1'b1);

    wire pc_dat_we = pc_reg_dat_sel && (|mem_wstrb);
    wire pc_dat_re = pc_reg_dat_sel && (!(|mem_wstrb));

    assign uart_ready = sel_uart && (pc_reg_div_sel || (pc_reg_dat_sel && !pc_uart_wait));
    assign uart_rdata = pc_reg_div_sel ? pc_uart_div_do : pc_uart_dat_do;

    simpleuart_fifo #(
        .DEFAULT_DIV(DEFAULT_DIV),
        .FIFO_DEPTH(32)
    ) u_host_uart (
        .clk(clk),
        .resetn(rst_n),
        .ser_tx(uart_tx_o),
        .ser_rx(pc_rx_sync),
        .reg_div_we(pc_reg_div_sel ? mem_wstrb : 4'b0000),
        .reg_div_di(mem_wdata),
        .reg_div_do(pc_uart_div_do),
        .reg_dat_we(pc_dat_we),
        .reg_dat_re(pc_dat_re),
        .reg_dat_di(mem_wdata),
        .reg_dat_do(pc_uart_dat_do),
        .reg_dat_wait(pc_uart_wait)
    );

    // ------------------------------------------------------------------------
    // 5. GPIO LEDs Peripheral (0x4000_0000)
    // ------------------------------------------------------------------------
    reg [25:0] heartbeat_cnt;
    reg [15:0] gpio_led_reg;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            gpio_ready    <= 1'b0;
            gpio_rdata    <= 32'd0;
            gpio_led_reg  <= 16'd0;
            heartbeat_cnt <= 26'd0;
        end else begin
            heartbeat_cnt <= heartbeat_cnt + 1'b1;
            gpio_ready    <= sel_gpio && !gpio_ready;

            if (sel_gpio && !gpio_ready) begin
                gpio_rdata <= {16'd0, gpio_led_reg};
                if (|mem_wstrb) begin
                    if (mem_wstrb[0]) gpio_led_reg[7:0]  <= mem_wdata[7:0];
                    if (mem_wstrb[1]) gpio_led_reg[15:8] <= mem_wdata[15:8];
                end
            end
        end
    end

    // Hardware status indicators / debug output pins:
    // LED 0: Heartbeat blink (~1.5Hz) - proves clock is ticking!
    // LED 1: CPU TRAP indicator (lights up ONLY if CPU crashes)
    // LED 2: Card event detected
    // LED 3: SPI Flash busy (active low CS)
    // LED 4: SPI Flash done
    // LED 5: Reserved (0)
    // LED [15:6]: Software-controlled LEDs
    always @(*) begin
        leds_o = {gpio_led_reg[15:6], 1'b0, flash_done_o, flash_busy_o, card_event_o, cpu_trap, heartbeat_cnt[25]};
    end

endmodule

