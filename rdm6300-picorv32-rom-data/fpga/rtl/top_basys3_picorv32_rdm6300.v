// ============================================================================
// File: top_basys3_picorv32_rdm6300.v
// Project: rdm6300-picorv32-rom-data
// Target: Digilent Basys 3 (AMD Xilinx Artix-7 XC7A35T-CPG236-1)
// Description: Top-level wrapper for Basys 3 FPGA prototyping board, mapping
//              PicoRV32 SoC, RFID reader, onboard USB-UART, LEDs, and QSPI Flash.
// ============================================================================

`timescale 1ns / 1ps

module top_basys3_picorv32_rdm6300 (
    // 100 MHz System Clock
    input  wire        clk,

    // Center Pushbutton Reset (Active High on Basys 3, converted to active-low)
    input  wire        btnC,

    // RFID Reader RDM6300 UART RX (PMOD JA1, Pin J1)
    input  wire        rdm6300_rx_i,

    // Onboard USB-UART Bridge
    output wire        uart_tx_o,      // Pin A18 (Transmits to PC Terminal)
    input  wire        uart_rx_i,      // Pin B18 (Receives from PC)

    // Onboard Spansion S25FL032P QSPI Flash
    output wire        qspi_cs,        // Pin K19 (Active Low Chip Select)
    inout  wire [3:0]  qspi_dq,        // D0: D18 (MOSI), D1: D19 (MISO), D2: G18 (WP), D3: F18 (HOLD)

    // 16 Status LEDs on Basys 3
    output wire [15:0] led,

    // 4-Digit 7-Segment Display on Basys 3
    output wire [6:0]  seg,            // Segments a..g (Active Low)
    output wire        dp,             // Decimal point (Active Low)
    output wire [3:0]  an              // 4 Digits Anode Select (Active Low)
);

    // ------------------------------------------------------------------------
    // 50 MHz System Clock Generation (Divide 100 MHz oscillator by 2)
    // ------------------------------------------------------------------------
    reg clk_50_reg = 1'b0;
    always @(posedge clk) begin
        clk_50_reg <= ~clk_50_reg;
    end

    wire clk_50;
    BUFG u_bufg_clk50 (
        .I(clk_50_reg),
        .O(clk_50)
    );

    // ------------------------------------------------------------------------
    // Power-On Reset & User Button Reset Synchronization (on clk_50)
    // ------------------------------------------------------------------------
    reg [5:0] por_cnt = 6'd0;
    wire      por_done = (por_cnt == 6'd60);

    always @(posedge clk_50) begin
        if (!por_done) por_cnt <= por_cnt + 1'b1;
    end

    // System reset is active-low (resets when button is pressed or during POR)
    wire rst_n = por_done && !btnC;

    // ------------------------------------------------------------------------
    // SPI Flash Pin Handling for Basys 3 (spimemio QSPI)
    // ------------------------------------------------------------------------
    wire flash_csb;
    wire flash_clk;
    wire flash_io0_oe, flash_io1_oe, flash_io2_oe, flash_io3_oe;
    wire flash_io0_do, flash_io1_do, flash_io2_do, flash_io3_do;
    wire flash_io0_di, flash_io1_di, flash_io2_di, flash_io3_di;

    assign qspi_cs       = flash_csb;
    assign qspi_dq[0]    = flash_io0_oe ? flash_io0_do : 1'bz;
    assign flash_io0_di  = qspi_dq[0];
    assign qspi_dq[1]    = flash_io1_oe ? flash_io1_do : 1'bz;
    assign flash_io1_di  = qspi_dq[1];
    assign qspi_dq[2]    = flash_io2_oe ? flash_io2_do : 1'bz;
    assign flash_io2_di  = qspi_dq[2];
    assign qspi_dq[3]    = flash_io3_oe ? flash_io3_do : 1'bz;
    assign flash_io3_di  = qspi_dq[3];

    // In Xilinx 7-Series FPGA, the CCLK pin connected to Flash is accessed
    // post-configuration via the STARTUPE2 primitive's USRCCLKO port.
    STARTUPE2 #(
        .PROG_USR("FALSE"),
        .SIM_CCLK_FREQ(0.0)
    ) u_startup (
        .CFGCLK(),
        .CFGMCLK(),
        .EOS(),
        .PREQ(),
        .CLK(1'b0),
        .GSR(1'b0),
        .GTS(1'b0),
        .KEYCLEARB(1'b1),
        .PACK(1'b0),
        .USRCCLKO(flash_clk), // Drive Flash CCLK from spimemio
        .USRCCLKTS(1'b0),     // 0 = Output enabled
        .USRDONEO(1'b1),
        .USRDONETS(1'b1)
    );

    // ------------------------------------------------------------------------
    // SoC Core Instantiation (Running at 50 MHz)
    // ------------------------------------------------------------------------
    wire cpu_trap_status;
    wire card_event_pulse;
    wire flash_busy_status;
    wire flash_done_pulse;

    rdm6300_picorv32_soc #(
        .CLK_FREQ_HZ(50_000_000),
        .UART_BAUD(9600),
        .PROGADDR_RESET(32'h0025_0000), // 2.3MB into Flash on Basys 3
        .PROGADDR_IRQ(32'h0025_0010),
        .STACKADDR(32'h0000_0400)
    ) u_soc_core (
        .clk(clk_50),
        .rst_n(rst_n),
        .rdm6300_rx_i(rdm6300_rx_i),
        .uart_tx_o(uart_tx_o),
        .uart_rx_i(uart_rx_i),
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
        .leds_o(led),
        .cpu_trap(cpu_trap_status),
        .card_event_o(card_event_pulse),
        .flash_busy_o(flash_busy_status),
        .flash_done_o(flash_done_pulse)
    );

    // ------------------------------------------------------------------------
    // Snoop on CPU Host UART TX to detect card authentication results:
    // CPU outputs "ACCESS:GRANTED:..." when card is found in Flash whitelist
    // CPU outputs "ACCESS:DENIED:..." when card is unauthorized / unknown
    // ------------------------------------------------------------------------
    wire       snoop_uart_dv;
    wire [7:0] snoop_uart_byte;

    uart_rx #(
        .CLKS_PER_BIT(50_000_000 / 9600)
    ) u_snoop_tx (
        .clk(clk_50),
        .rst_n(rst_n),
        .rx(uart_tx_o),
        .rx_dv(snoop_uart_dv),
        .rx_byte(snoop_uart_byte),
        .framing_error(),
        .break_detect()
    );

    reg [2:0] access_match_idx = 3'd0;
    reg       trigger_pass     = 1'b0;
    reg       trigger_fail     = 1'b0;

    always @(posedge clk_50 or negedge rst_n) begin
        if (!rst_n) begin
            access_match_idx <= 3'd0;
            trigger_pass     <= 1'b0;
            trigger_fail     <= 1'b0;
        end else begin
            trigger_pass <= 1'b0;
            trigger_fail <= 1'b0;

            if (snoop_uart_dv) begin
                case (access_match_idx)
                    3'd0: if (snoop_uart_byte == "A") access_match_idx <= 3'd1;
                    3'd1: if (snoop_uart_byte == "C") access_match_idx <= 3'd2; else access_match_idx <= (snoop_uart_byte == "A") ? 3'd1 : 3'd0;
                    3'd2: if (snoop_uart_byte == "C") access_match_idx <= 3'd3; else access_match_idx <= (snoop_uart_byte == "A") ? 3'd1 : 3'd0;
                    3'd3: if (snoop_uart_byte == "E") access_match_idx <= 3'd4; else access_match_idx <= (snoop_uart_byte == "A") ? 3'd1 : 3'd0;
                    3'd4: if (snoop_uart_byte == "S") access_match_idx <= 3'd5; else access_match_idx <= (snoop_uart_byte == "A") ? 3'd1 : 3'd0;
                    3'd5: if (snoop_uart_byte == "S") access_match_idx <= 3'd6; else access_match_idx <= (snoop_uart_byte == "A") ? 3'd1 : 3'd0;
                    3'd6: if (snoop_uart_byte == ":") access_match_idx <= 3'd7; else access_match_idx <= (snoop_uart_byte == "A") ? 3'd1 : 3'd0;
                    3'd7: begin
                        access_match_idx <= 3'd0;
                        if (snoop_uart_byte == "G") begin
                            trigger_pass <= 1'b1;
                        end else if (snoop_uart_byte == "D") begin
                            trigger_fail <= 1'b1;
                        end
                    end
                    default: access_match_idx <= 3'd0;
                endcase
            end
        end
    end

    // ------------------------------------------------------------------------
    // 7-Segment Display Controller:
    // - Idle (no scan / after 2.0s): Display OFF (all 4 digits blank)
    // - Card Authorized: Shows "PASS" for 2.0s then turns OFF
    // - Card Unauthorized / Denied: Shows "FAIL" for 2.0s then turns OFF
    // ------------------------------------------------------------------------
    reg [26:0] display_timer   = 27'd0;
    reg        display_is_pass = 1'b0;
    wire       display_active  = (display_timer > 0);

    always @(posedge clk_50 or negedge rst_n) begin
        if (!rst_n) begin
            display_timer   <= 27'd0;
            display_is_pass <= 1'b0;
        end else begin
            if (trigger_pass) begin
                display_timer   <= 27'd100_000_000; // 2.0 seconds at 50 MHz
                display_is_pass <= 1'b1;
            end else if (trigger_fail) begin
                display_timer   <= 27'd100_000_000; // 2.0 seconds at 50 MHz
                display_is_pass <= 1'b0;
            end else if (display_timer > 0) begin
                display_timer <= display_timer - 1'b1;
            end
        end
    end

    // Display Refresh Counter (~191 Hz frame rate / ~763 Hz per digit)
    reg [17:0] refresh_cnt = 18'd0;
    always @(posedge clk_50 or negedge rst_n) begin
        if (!rst_n) begin
            refresh_cnt <= 18'd0;
        end else begin
            refresh_cnt <= refresh_cnt + 1'b1;
        end
    end

    wire [1:0] digit_sel = refresh_cnt[17:16];
    reg [3:0]  an_reg;
    reg [6:0]  seg_reg;

    assign dp  = 1'b1;     // Decimal point disabled (active-low)
    assign an  = an_reg;
    assign seg = seg_reg;

    // Active-Low 7-Segment Encoding (0 = ON, 1 = OFF):
    // Segments: {g, f, e, d, c, b, a}
    // 'P' = 7'b0001100 (0x0C)
    // 'A' = 7'b0001000 (0x08)
    // 'S' = 7'b0010010 (0x12)
    // 'F' = 7'b0001110 (0x0E)
    // 'I' = 7'b1111001 (0x79)
    // 'L' = 7'b1000111 (0x47)
    always @(*) begin
        if (!display_active) begin
            an_reg  = 4'b1111;      // All 4 digits OFF
            seg_reg = 7'b1111111;   // All segments OFF
        end else begin
            case (digit_sel)
                2'b11: begin // Digit 3 (Leftmost)
                    an_reg  = 4'b0111;
                    seg_reg = display_is_pass ? 7'b0001100 : 7'b0001110; // 'P' or 'F'
                end
                2'b10: begin // Digit 2
                    an_reg  = 4'b1011;
                    seg_reg = 7'b0001000;                                // 'A'
                end
                2'b01: begin // Digit 1
                    an_reg  = 4'b1101;
                    seg_reg = display_is_pass ? 7'b0010010 : 7'b1111001; // 'S' or 'I'
                end
                2'b00: begin // Digit 0 (Rightmost)
                    an_reg  = 4'b1110;
                    seg_reg = display_is_pass ? 7'b0010010 : 7'b1000111; // 'S' or 'L'
                end
            endcase
        end
    end

endmodule
