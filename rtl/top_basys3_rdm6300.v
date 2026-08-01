`timescale 1ns/1ps

module top_basys3_rdm6300 #(
    parameter CLKS_PER_BIT = 10417,
    parameter FIFO_DEPTH   = 16,
    parameter FIFO_ADDR_W  = 4
) (
    input  wire       clk,
    input  wire       rst_btn,

    input  wire       rdm6300_rx_i,
    output wire       uart_tx_o,

    output wire [3:0] led
);

    wire rst_n;

    wire [7:0] rx_rd_data;
    wire       rx_empty;
    wire       rx_full;

    reg rx_rd_en;
    reg tx_wr_en;
    reg [7:0] tx_wr_data;
    wire      tx_full;
    wire      tx_empty;

    reg [2:0] bridge_fsm;
    reg [7:0] bridge_data;

    localparam BR_IDLE  = 3'd0;
    localparam BR_READ  = 3'd1;
    localparam BR_LATCH = 3'd2;
    localparam BR_WRITE = 3'd3;

    assign rst_n = ~rst_btn;

    uart_fifo_core #(
        .CLKS_PER_BIT(CLKS_PER_BIT),
        .FIFO_DEPTH(FIFO_DEPTH),
        .FIFO_ADDR_W(FIFO_ADDR_W)
    ) u_core (
        .clk(clk),
        .rst_n(rst_n),
        .uart_rx_i(rdm6300_rx_i),
        .uart_tx_o(uart_tx_o),
        .tx_wr_en(tx_wr_en),
        .tx_wr_data(tx_wr_data),
        .tx_full(tx_full),
        .tx_empty(tx_empty),
        .rx_rd_en(rx_rd_en),
        .rx_rd_data(rx_rd_data),
        .rx_empty(rx_empty),
        .rx_full(rx_full)
    );

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            bridge_fsm <= BR_IDLE;
            rx_rd_en <= 1'b0;
            tx_wr_en <= 1'b0;
            tx_wr_data <= 8'd0;
            bridge_data <= 8'd0;
        end else begin
            rx_rd_en <= 1'b0;
            tx_wr_en <= 1'b0;

            case (bridge_fsm)
                BR_IDLE: begin
                    if (!rx_empty && !tx_full) begin
                        rx_rd_en <= 1'b1;
                        bridge_fsm <= BR_READ;
                    end
                end

                BR_READ: begin
                    bridge_fsm <= BR_LATCH;
                end

                BR_LATCH: begin
                    bridge_data <= rx_rd_data;
                    bridge_fsm <= BR_WRITE;
                end

                BR_WRITE: begin
                    if (!tx_full) begin
                        tx_wr_en <= 1'b1;
                        tx_wr_data <= bridge_data;
                        bridge_fsm <= BR_IDLE;
                    end
                end

                default: bridge_fsm <= BR_IDLE;
            endcase
        end
    end

    assign led[0] = ~rx_empty;
    assign led[1] = ~tx_empty;
    assign led[2] = rx_full;
    assign led[3] = tx_full;

endmodule
