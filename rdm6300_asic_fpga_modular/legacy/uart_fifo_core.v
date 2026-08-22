`timescale 1ns/1ps

module uart_fifo_core #(
    parameter CLKS_PER_BIT = 868,
    parameter FIFO_DEPTH = 16,
    parameter FIFO_ADDR_W = 4
) (
    input  wire       clk,
    input  wire       rst_n,

    input  wire       uart_rx_i,
    output wire       uart_tx_o,

    input  wire       tx_wr_en,
    input  wire [7:0] tx_wr_data,
    output wire       tx_full,
    output wire       tx_empty,

    input  wire       rx_rd_en,
    output wire [7:0] rx_rd_data,
    output wire       rx_empty,
    output wire       rx_full
);

    wire rx_dv;
    wire [7:0] rx_byte;

    wire [7:0] tx_fifo_rd_data;
    wire tx_fifo_rd_en;
    wire tx_fifo_empty;
    wire tx_fifo_full;
    wire tx_active;
    wire tx_done;

    reg tx_start;
    reg [7:0] tx_data_reg;
    reg [2:0] tx_fsm;

    localparam TX_IDLE      = 3'd0;
    localparam TX_READ      = 3'd1;
    localparam TX_LOAD      = 3'd2;
    localparam TX_WAIT_BUSY = 3'd3;
    localparam TX_WAIT_DONE = 3'd4;

    uart_rx #(
        .CLKS_PER_BIT(CLKS_PER_BIT)
    ) u_uart_rx (
        .clk(clk),
        .rst_n(rst_n),
        .rx(uart_rx_i),
        .rx_dv(rx_dv),
        .rx_byte(rx_byte)
    );

    fifo_sync #(
        .DATA_W(8),
        .DEPTH(FIFO_DEPTH),
        .ADDR_W(FIFO_ADDR_W)
    ) u_rx_fifo (
        .clk(clk),
        .rst_n(rst_n),
        .wr_en(rx_dv),
        .wr_data(rx_byte),
        .rd_en(rx_rd_en),
        .rd_data(rx_rd_data),
        .full(rx_full),
        .empty(rx_empty),
        .level()
    );

    fifo_sync #(
        .DATA_W(8),
        .DEPTH(FIFO_DEPTH),
        .ADDR_W(FIFO_ADDR_W)
    ) u_tx_fifo (
        .clk(clk),
        .rst_n(rst_n),
        .wr_en(tx_wr_en),
        .wr_data(tx_wr_data),
        .rd_en(tx_fifo_rd_en),
        .rd_data(tx_fifo_rd_data),
        .full(tx_fifo_full),
        .empty(tx_fifo_empty),
        .level()
    );

    uart_tx #(
        .CLKS_PER_BIT(CLKS_PER_BIT)
    ) u_uart_tx (
        .clk(clk),
        .rst_n(rst_n),
        .tx_dv(tx_start),
        .tx_byte(tx_data_reg),
        .tx(uart_tx_o),
        .tx_active(tx_active),
        .tx_done(tx_done)
    );

    assign tx_full = tx_fifo_full;
    assign tx_empty = tx_fifo_empty;
    assign tx_fifo_rd_en = (tx_fsm == TX_READ);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            tx_start <= 1'b0;
            tx_data_reg <= 8'd0;
            tx_fsm <= TX_IDLE;
        end else begin
            tx_start <= 1'b0;

            case (tx_fsm)
                TX_IDLE: begin
                    if (!tx_active && !tx_fifo_empty) begin
                        tx_fsm <= TX_READ;
                    end
                end

                TX_READ: begin
                    tx_fsm <= TX_LOAD;
                end

                TX_LOAD: begin
                    tx_data_reg <= tx_fifo_rd_data;
                    tx_start <= 1'b1;
                    tx_fsm <= TX_WAIT_BUSY;
                end

                TX_WAIT_BUSY: begin
                    if (tx_active)
                        tx_fsm <= TX_WAIT_DONE;
                end

                TX_WAIT_DONE: begin
                    if (!tx_active)
                        tx_fsm <= TX_IDLE;
                end

                default: tx_fsm <= TX_IDLE;
            endcase
        end
    end

endmodule
