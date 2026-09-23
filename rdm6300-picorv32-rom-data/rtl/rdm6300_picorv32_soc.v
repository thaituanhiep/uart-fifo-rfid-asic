// ============================================================================
// File: rdm6300_picorv32_soc.v
// Project: rdm6300-picorv32-rom-data
// Description: PicoRV32 RISC-V SoC integrating SPI Flash Manager, PC UART,
//              RDM6300 RFID UART, 8KB Boot SRAM, and Memory Mapped Bus.
// ============================================================================

`timescale 1ns / 1ps

module rdm6300_picorv32_soc #(
    parameter CLK_FREQ_HZ   = 100_000_000,
    parameter UART_BAUD     = 9600,
    parameter FLASH_BASE    = 24'h30_0000,
    parameter BOOT_HEX      = ""
)(
    input  wire        clk,
    input  wire        rst_n,

    // External RDM6300 RFID Interface (9600 Baud 8-N-1)
    input  wire        rdm6300_rx_i,

    // External Host PC UART Interface
    output wire        uart_tx_o,
    input  wire        uart_rx_i,

    // Physical SPI Flash Interface (Basys 3 / ASIC)
    output wire        flash_csn,
    output wire        flash_sck,
    output wire        flash_mosi,
    input  wire        flash_miso,

    // General Purpose I/O (Status LEDs on Basys 3)
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
    // 0x0000_0000 - 0x0000_1FFF: 8KB Mask ROM (Read-Only)
    // 0x0001_0000 - 0x0001_07FF: 2KB Data SRAM (Read/Write)
    // 0x1000_0000 - 0x1000_0007: RDM6300 UART RX (simpleuart)
    // 0x2000_0000 - 0x2000_001F: SPI Flash Controller MMIO
    // 0x3000_0000 - 0x3000_0007: Host PC UART (simpleuart TX/RX)
    // 0x4000_0000 - 0x4000_0003: GPIO / LEDs
    wire sel_rom   = mem_valid && (mem_addr[31:16] == 16'h0000);
    wire sel_sram  = mem_valid && (mem_addr[31:16] == 16'h0001);
    wire sel_rfid  = mem_valid && (mem_addr[31:28] == 4'h1);
    wire sel_flash = mem_valid && (mem_addr[31:28] == 4'h2);
    wire sel_uart  = mem_valid && (mem_addr[31:28] == 4'h3);
    wire sel_gpio  = mem_valid && (mem_addr[31:28] == 4'h4);

    wire        rom_ready;
    wire [31:0] rom_rdata;

    wire        sram_ready;
    wire [31:0] sram_rdata;

    wire        flash_ready;
    wire [31:0] flash_rdata;

    wire        rfid_ready;
    wire [31:0] rfid_rdata;

    wire        uart_ready;
    wire [31:0] uart_rdata;

    reg         gpio_ready;
    reg  [31:0] gpio_rdata;

    assign mem_ready = rom_ready || sram_ready || flash_ready || rfid_ready || uart_ready || gpio_ready;
    assign mem_rdata = sel_rom   ? rom_rdata   :
                       sel_sram  ? sram_rdata  :
                       sel_flash ? flash_rdata :
                       sel_rfid  ? rfid_rdata  :
                       sel_uart  ? uart_rdata  :
                       sel_gpio  ? gpio_rdata  : 32'd0;

    // ------------------------------------------------------------------------
    // PicoRV32 Core Instantiation
    // ------------------------------------------------------------------------
    wire [31:0] irq_lines;

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
        .ENABLE_IRQ(1),
        .ENABLE_IRQ_QREGS(0),
        .ENABLE_IRQ_TIMER(1),
        .MASKED_IRQ(32'h0000_0000),
        .LATCHED_IRQ(32'hffff_ffff),
        .PROGADDR_RESET(32'h0000_0000),
        .PROGADDR_IRQ(32'h0000_0010),
        .STACKADDR(32'h0001_0400)
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
        .irq(irq_lines),
        .eoi()
    );

    // ------------------------------------------------------------------------
    // 1. Mask ROM 8KB (0x0000_0000) - Read Only
    // ------------------------------------------------------------------------
    mask_rom #(
        .WORDS(2048),
        .INIT_FILE(BOOT_HEX)
    ) u_mask_rom (
        .clk(clk),
        .rst_n(rst_n),
        .valid(sel_rom),
        .addr(mem_addr[12:0]),
        .rdata(rom_rdata),
        .ready(rom_ready)
    );

    // ------------------------------------------------------------------------
    // 2. Data SRAM 1KB (0x0001_0000) - Read / Write
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
    // 2. Hardware RDM6300 RFID Receiver & Frame Decoder (0x1000_0000)
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
    // 0x1000_0004: Tag Word Hi (8-bit version/manufacturer byte: tag_raw[39:32])
    // 0x1000_0008: Tag Word Lo (32-bit serial number: tag_raw[31:0])
    assign rfid_ready = sel_rfid;
    assign rfid_rdata = (mem_addr[3:2] == 2'b00) ? {31'd0, rfid_tag_ready} :
                        (mem_addr[3:2] == 2'b01) ? {24'd0, rfid_tag_hi}     :
                        (mem_addr[3:2] == 2'b10) ? rfid_tag_lo              : 32'd0;

    assign card_event_o = hw_card_valid;

    // ------------------------------------------------------------------------
    // 3. SPI Flash Memory Controller (0x2000_0000)
    // ------------------------------------------------------------------------
    wire flash_write_done;
    wire flash_error;
    wire [15:0] saved_records;

    spi_flash_controller #(
        .CLK_FREQ_HZ(CLK_FREQ_HZ),
        .SPI_FREQ_HZ(25_000_000),
        .FLASH_BASE_ADDR(FLASH_BASE)
    ) u_flash_ctrl (
        .clk(clk),
        .rst_n(rst_n),
        .bus_valid(sel_flash),
        .bus_addr(mem_addr[4:0]),
        .bus_wdata(mem_wdata),
        .bus_wstrb(mem_wstrb),
        .bus_rdata(flash_rdata),
        .bus_ready(flash_ready),
        .auto_save_enable(1'b0), // Software-controlled through PicoRV32 MMIO
        .card_valid(hw_card_valid),
        .tag_raw(hw_tag_raw),
        .tag_checksum(8'd0),
        .flash_csn(flash_csn),
        .flash_sck(flash_sck),
        .flash_mosi(flash_mosi),
        .flash_miso(flash_miso),
        .flash_busy(flash_busy_o),
        .flash_write_done(flash_write_done),
        .flash_error(flash_error),
        .saved_records_count(saved_records)
    );

    assign flash_done_o = flash_write_done;

    // ------------------------------------------------------------------------
    // 4. Host PC UART Interface (0x3000_0000)
    // ------------------------------------------------------------------------
    // Mapped as SimpleUART for bidirectional host communication:
    // 0x3000_0000: Divisor register
    // 0x3000_0004: Data register (write byte to transmit, read to receive)
    wire [31:0] pc_uart_div_do;
    wire [31:0] pc_uart_dat_do;
    wire        pc_uart_wait;

    wire pc_reg_div_sel = sel_uart && (mem_addr[2] == 1'b0);
    wire pc_reg_dat_sel = sel_uart && (mem_addr[2] == 1'b1);

    wire pc_dat_we = pc_reg_dat_sel && (|mem_wstrb);
    wire pc_dat_re = pc_reg_dat_sel && (!(|mem_wstrb));

    assign uart_ready = sel_uart && (pc_reg_div_sel || (pc_reg_dat_sel && !pc_uart_wait));
    assign uart_rdata = pc_reg_div_sel ? pc_uart_div_do : pc_uart_dat_do;

    simpleuart #(
        .DEFAULT_DIV(DEFAULT_DIV)
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

    // Direct, unmistakable hardware LED indicators on Basys 3:
    // LED 0: Heartbeat blink (~1.5Hz) - proves 100MHz clock is ticking!
    // LED 1: CPU TRAP indicator (lights up ONLY if CPU crashes)
    // LED 2: Card event detected
    // LED 3: SPI Flash busy
    // LED 4: SPI Flash done
    // LED 5: SPI Flash error
    // LED [15:6]: Software-controlled LEDs
    always @(*) begin
        leds_o = {gpio_led_reg[15:6], flash_error, flash_done_o, flash_busy_o, card_event_o, cpu_trap, heartbeat_cnt[25]};
    end

    // Interrupts to PicoRV32
    assign irq_lines = {29'd0, flash_write_done, flash_error, card_event_o};

endmodule
