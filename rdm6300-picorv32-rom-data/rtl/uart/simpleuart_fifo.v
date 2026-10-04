// ============================================================================
// File: rtl/uart/simpleuart_fifo.v
// Project: rdm6300-picorv32-rom-data
// Description: Wrapper around simpleuart.v that integrates a synchronous RX FIFO
//              to buffer incoming bytes and prevent overrun/dropped data.
// ============================================================================

`timescale 1ns / 1ps

module simpleuart_fifo #(
    parameter integer DEFAULT_DIV = 1,
    parameter integer FIFO_DEPTH  = 32
)(
    input  wire        clk,
    input  wire        resetn,

    output wire        ser_tx,
    input  wire        ser_rx,

    input  wire [3:0]  reg_div_we,
    input  wire [31:0] reg_div_di,
    output wire [31:0] reg_div_do,

    input  wire        reg_dat_we,
    input  wire        reg_dat_re,
    input  wire [31:0] reg_dat_di,
    output wire [31:0] reg_dat_do,
    output wire        reg_dat_wait,

    // Status / Activity output
    output wire        rx_fifo_not_empty
);

    // Internal connections to simpleuart
    wire [31:0] raw_uart_dat_do;
    wire        raw_uart_has_byte = (raw_uart_dat_do != 32'hFFFFFFFF);
    wire        raw_uart_re;

    // FIFO signals
    wire        fifo_full;
    wire        fifo_empty;
    wire [7:0]  fifo_dout;
    wire        fifo_push;
    wire        fifo_pop;

    // Push into FIFO whenever simpleuart finishes receiving a byte
    assign fifo_push   = raw_uart_has_byte && !fifo_full;
    assign raw_uart_re = fifo_push;

    // Read from FIFO
    assign fifo_pop    = reg_dat_re && !fifo_empty;
    assign reg_dat_do  = fifo_empty ? 32'hFFFFFFFF : {24'd0, fifo_dout};

    assign rx_fifo_not_empty = !fifo_empty;

    // Instantiate simpleuart core
    simpleuart #(
        .DEFAULT_DIV(DEFAULT_DIV)
    ) u_simpleuart_core (
        .clk         (clk),
        .resetn      (resetn),
        .ser_tx      (ser_tx),
        .ser_rx      (ser_rx),
        .reg_div_we  (reg_div_we),
        .reg_div_di  (reg_div_di),
        .reg_div_do  (reg_div_do),
        .reg_dat_we  (reg_dat_we),
        .reg_dat_re  (raw_uart_re),
        .reg_dat_di  (reg_dat_di),
        .reg_dat_do  (raw_uart_dat_do),
        .reg_dat_wait(reg_dat_wait)
    );

    // Instantiate synchronous FIFO
    sync_fifo #(
        .DATA_WIDTH(8),
        .DEPTH     (FIFO_DEPTH)
    ) u_rx_fifo (
        .clk       (clk),
        .rst_n     (resetn),
        .push      (fifo_push),
        .din       (raw_uart_dat_do[7:0]),
        .pop       (fifo_pop),
        .dout      (fifo_dout),
        .empty     (fifo_empty),
        .full      (fifo_full),
        .count     ()
    );

endmodule
