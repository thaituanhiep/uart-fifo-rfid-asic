// ============================================================================
// File: rtl/uart/uart_mmio.v
// Project: rdm6300-picorv32-rom-data
// Description: Unified Parameterized Memory-Mapped UART Peripheral.
//              Used for both Host PC Communication and RFID Reader Interface.
//
// Memory Map (Offset from Base Address):
//   +0x00: Baud Rate Clock Prescaler / Divider Register (R/W)
//   +0x04: UART Data FIFO Register (Write to TX FIFO, Read from RX FIFO)
//          Reading returns 32'hFFFF_FFFF (-1) if RX FIFO is empty.
// ============================================================================

`timescale 1ns / 1ps

module uart_mmio #(
    parameter DEFAULT_DIV = 5208, // 50 MHz / 9600 Baud
    parameter FIFO_DEPTH  = 32
)(
    input  wire        clk,
    input  wire        rst_n,

    // External Physical Serial Pins
    input  wire        rx_i,
    output wire        tx_o,

    // PicoRV32 Native Memory Bus Slave Interface
    input  wire        valid,
    input  wire [3:0]  addr,      // cpu_mem_addr[3:0]
    input  wire [31:0] wdata,
    input  wire [3:0]  wstrb,
    output wire [31:0] rdata,
    output wire        ready,

    // Activity / Event Indicator
    output wire        rx_activity_o
);

    // 1. Two-Stage Synchronizer for Asynchronous External RX Pin
    wire rx_sync;

    sync_2ff #(.RESET_VALUE(1'b1)) u_sync_rx (
        .clk(clk),
        .rst_n(rst_n),
        .async_i(rx_i),
        .sync_o(rx_sync)
    );

    // 2. Register Selection & Read/Write Decoding
    wire [31:0] uart_div_do;
    wire [31:0] uart_dat_do;
    wire        uart_wait;

    wire reg_div_sel = valid && (addr[2] == 1'b0); // offset +0x00
    wire reg_dat_sel = valid && (addr[2] == 1'b1); // offset +0x04

    wire dat_we = reg_dat_sel && (|wstrb);
    wire dat_re = reg_dat_sel && (!(|wstrb));

    // Bus Response
    assign ready = valid && (reg_div_sel || (reg_dat_sel && !uart_wait));
    assign rdata = reg_div_sel ? uart_div_do : uart_dat_do;

    // 3. FIFO-Buffered Hardware UART Core (simpleuart_fifo)
    simpleuart_fifo #(
        .DEFAULT_DIV(DEFAULT_DIV),
        .FIFO_DEPTH(FIFO_DEPTH)
    ) u_uart_fifo (
        .clk(clk),
        .resetn(rst_n),
        .ser_tx(tx_o),
        .ser_rx(rx_sync),
        .reg_div_we(reg_div_sel ? wstrb : 4'b0000),
        .reg_div_di(wdata),
        .reg_div_do(uart_div_do),
        .reg_dat_we(dat_we),
        .reg_dat_re(dat_re),
        .reg_dat_di(wdata),
        .reg_dat_do(uart_dat_do),
        .reg_dat_wait(uart_wait),
        .rx_fifo_not_empty(rx_activity_o)
    );

endmodule
