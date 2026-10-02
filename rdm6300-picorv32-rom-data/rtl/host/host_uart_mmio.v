// ============================================================================
// File: rtl/host_uart_mmio.v
// Project: rdm6300-picorv32-rom-data
// Description: Host PC UART Controller with 32-Byte TX/RX Hardware FIFOs,
//              CDC Synchronizer, and PicoRV32 MMIO Slave Interface (Base: 0x3000_0000).
//
// Memory Map (Base: 0x3000_0000):
//   0x3000_0000: Clock Prescaler / Baud Divider Register (Default: CLK / BAUD)
//   0x3000_0004: UART Data FIFO Register (Write to TX FIFO, Read from RX FIFO)
//                Reading returns 32'hFFFF_FFFF (-1) if RX FIFO is empty.
// ============================================================================

`timescale 1ns / 1ps

module host_uart_mmio #(
    parameter DEFAULT_DIV = 5208, // 50 MHz / 9600 Baud
    parameter FIFO_DEPTH  = 32
)(
    input  wire        clk,
    input  wire        rst_n,

    // External Physical UART Pins (Connected to FTDI USB-UART Bridge)
    input  wire        uart_rx_i,
    output wire        uart_tx_o,

    // PicoRV32 Native Memory Bus Slave Interface (0x3000_0000)
    input  wire        valid,
    input  wire [3:0]  addr,      // cpu_mem_addr[3:0]
    input  wire [31:0] wdata,
    input  wire [3:0]  wstrb,
    output wire [31:0] rdata,
    output wire        ready
);

    // ------------------------------------------------------------------------
    // 1. Two-Stage Synchronizer for Asynchronous External RX Pin
    // ------------------------------------------------------------------------
    wire pc_rx_sync;

    sync_2ff #(.RESET_VALUE(1'b1)) u_sync_pcrx (
        .clk(clk),
        .rst_n(rst_n),
        .async_i(uart_rx_i),
        .sync_o(pc_rx_sync)
    );

    // ------------------------------------------------------------------------
    // 2. Register Selection & Read/Write Decoding
    // ------------------------------------------------------------------------
    wire [31:0] pc_uart_div_do;
    wire [31:0] pc_uart_dat_do;
    wire        pc_uart_wait;

    wire pc_reg_div_sel = valid && (addr[2] == 1'b0); // 0x3000_0000
    wire pc_reg_dat_sel = valid && (addr[2] == 1'b1); // 0x3000_0004

    wire pc_dat_we = pc_reg_dat_sel && (|wstrb);
    wire pc_dat_re = pc_reg_dat_sel && (!(|wstrb));

    // Bus Response
    assign ready = valid && (pc_reg_div_sel || (pc_reg_dat_sel && !pc_uart_wait));
    assign rdata = pc_reg_div_sel ? pc_uart_div_do : pc_uart_dat_do;

    // ------------------------------------------------------------------------
    // 3. FIFO-Buffered Hardware UART Core (simpleuart_fifo)
    // ------------------------------------------------------------------------
    simpleuart_fifo #(
        .DEFAULT_DIV(DEFAULT_DIV),
        .FIFO_DEPTH(FIFO_DEPTH)
    ) u_host_uart (
        .clk(clk),
        .resetn(rst_n),
        .ser_tx(uart_tx_o),
        .ser_rx(pc_rx_sync),
        .reg_div_we(pc_reg_div_sel ? wstrb : 4'b0000),
        .reg_div_di(wdata),
        .reg_div_do(pc_uart_div_do),
        .reg_dat_we(pc_dat_we),
        .reg_dat_re(pc_dat_re),
        .reg_dat_di(wdata),
        .reg_dat_do(pc_uart_dat_do),
        .reg_dat_wait(pc_uart_wait)
    );

endmodule
