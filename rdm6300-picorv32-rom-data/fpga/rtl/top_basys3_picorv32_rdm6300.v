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
    output wire [15:0] led
);

    // ------------------------------------------------------------------------
    // Power-On Reset & User Button Reset Synchronization
    // ------------------------------------------------------------------------
    reg [5:0] por_cnt = 6'd0;
    wire      por_done = (por_cnt == 6'd60);

    always @(posedge clk) begin
        if (!por_done) por_cnt <= por_cnt + 1'b1;
    end

    // System reset is active-low (resets when button is pressed or during POR)
    wire rst_n = por_done && !btnC;

    // ------------------------------------------------------------------------
    // SPI Flash Pin Handling for Basys 3
    // ------------------------------------------------------------------------
    wire flash_sck_internal;
    wire flash_csn_internal;
    wire flash_mosi_internal;
    wire flash_miso_internal;

    assign qspi_cs       = flash_csn_internal;
    assign qspi_dq[0]    = flash_mosi_internal;   // MOSI / DQ0
    assign flash_miso_internal = qspi_dq[1];       // MISO / DQ1
    assign qspi_dq[2]    = 1'b1;                  // WP# (Write Protect disabled)
    assign qspi_dq[3]    = 1'b1;                  // HOLD# (Hold disabled)

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
        .USRCCLKO(flash_sck_internal), // Drive Flash CCLK
        .USRCCLKTS(1'b0),             // 0 = Output enabled
        .USRDONEO(1'b1),
        .USRDONETS(1'b1)
    );

    // ------------------------------------------------------------------------
    // SoC Core Instantiation
    // ------------------------------------------------------------------------
    wire cpu_trap_status;
    wire card_event_pulse;
    wire flash_busy_status;
    wire flash_done_pulse;

    rdm6300_picorv32_soc #(
        .CLK_FREQ_HZ(100_000_000),
        .UART_BAUD(9600),
        .FLASH_BASE(24'h30_0000),
        .BOOT_HEX("firmware.hex")
    ) u_soc_core (
        .clk(clk),
        .rst_n(rst_n),
        .rdm6300_rx_i(rdm6300_rx_i),
        .uart_tx_o(uart_tx_o),
        .uart_rx_i(uart_rx_i),
        .flash_csn(flash_csn_internal),
        .flash_sck(flash_sck_internal),
        .flash_mosi(flash_mosi_internal),
        .flash_miso(flash_miso_internal),
        .leds_o(led),
        .cpu_trap(cpu_trap_status),
        .card_event_o(card_event_pulse),
        .flash_busy_o(flash_busy_status),
        .flash_done_o(flash_done_pulse)
    );

endmodule
