// ============================================================================
// File: rtl/soc_interconnect.v
// Project: rdm6300-picorv32-rom-data
// Description: Central 32-bit Memory Bus Interconnect & Address Decoder for
//              rdm6300_picorv32_soc.
//
//              Decodes CPU memory cycles and multiplexes read data & ready
//              signals between PicoRV32 Master and 5 Slaves:
//              - Slave 0: 1KB Data SRAM (0x0000_0000 - 0x0000_03FF)
//              - Slave 1: SPI Flash XIP via spimemio (0x0010_0000 - 0x00FF_FFFF)
//              - Slave 1b: SPIMEMIO Configuration Register (0x0200_0000)
//              - Slave 2: RDM6300 RFID Controller (0x1000_0000 - 0x1000_0007)
//              - Slave 3: Host PC UART with FIFO (0x3000_0000 - 0x3000_0007)
//              - Slave 4: GPIO Status LEDs (0x4000_0000 - 0x4000_0003)
// ============================================================================

`timescale 1ns / 1ps

module soc_interconnect (
    // ------------------------------------------------------------------------
    // CPU Master Interface (PicoRV32 Native Memory Interface)
    // ------------------------------------------------------------------------
    input  wire        cpu_mem_valid,
    input  wire [31:0] cpu_mem_addr,
    output wire [31:0] cpu_mem_rdata,
    output wire        cpu_mem_ready,

    // ------------------------------------------------------------------------
    // Slave Select Signals (Decoded from cpu_mem_addr & cpu_mem_valid)
    // ------------------------------------------------------------------------
    output wire        sel_sram,
    output wire        sel_spimem,
    output wire        sel_spicfg,
    output wire        sel_rfid,
    output wire        sel_uart,
    output wire        sel_gpio,

    // ------------------------------------------------------------------------
    // Slave 0: 1KB Data SRAM (0x0000_0000 - 0x0000_03FF)
    // ------------------------------------------------------------------------
    input  wire [31:0] sram_rdata,
    input  wire        sram_ready,

    // ------------------------------------------------------------------------
    // Slave 1: SPI Flash XIP via spimemio (0x0010_0000 - 0x00FF_FFFF)
    // ------------------------------------------------------------------------
    input  wire [31:0] spimem_rdata,
    input  wire        spimem_ready,
    input  wire [31:0] spimem_cfg_do,

    // ------------------------------------------------------------------------
    // Slave 2: RDM6300 RFID Controller (0x1000_0000 - 0x1000_0007)
    // ------------------------------------------------------------------------
    input  wire [31:0] rfid_rdata,
    input  wire        rfid_ready,

    // ------------------------------------------------------------------------
    // Slave 3: Host PC UART with FIFO (0x3000_0000 - 0x3000_0007)
    // ------------------------------------------------------------------------
    input  wire [31:0] uart_rdata,
    input  wire        uart_ready,

    // ------------------------------------------------------------------------
    // Slave 4: GPIO Status LEDs (0x4000_0000 - 0x4000_0003)
    // ------------------------------------------------------------------------
    input  wire [31:0] gpio_rdata,
    input  wire        gpio_ready
);

    // ========================================================================
    // 1. Address Decoding Logic (Base & Range Matching)
    // ========================================================================
    assign sel_sram   = cpu_mem_valid && (cpu_mem_addr < 32'h0000_0400);
    assign sel_spimem = cpu_mem_valid && (cpu_mem_addr >= 32'h0010_0000 && cpu_mem_addr < 32'h0100_0000);
    assign sel_spicfg = cpu_mem_valid && (cpu_mem_addr == 32'h0200_0000);
    assign sel_rfid   = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h1);
    assign sel_uart   = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h3);
    assign sel_gpio   = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h4);

    // ========================================================================
    // 2. Response Multiplexing (Return to CPU Master)
    // ========================================================================
    assign cpu_mem_rdata = sel_sram   ? sram_rdata    :
                           sel_spimem ? spimem_rdata  :
                           sel_spicfg ? spimem_cfg_do :
                           sel_rfid   ? rfid_rdata    :
                           sel_uart   ? uart_rdata    :
                           sel_gpio   ? gpio_rdata    : 32'd0;

    assign cpu_mem_ready = sram_ready   ||
                           spimem_ready ||
                           sel_spicfg   ||
                           rfid_ready   ||
                           uart_ready   ||
                           gpio_ready;

endmodule
