`timescale 1ns/1ps

module uart_rx #(
    parameter CLKS_PER_BIT = 868
) (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       rx,
    output reg        rx_dv,
    output reg [7:0]  rx_byte
);

    localparam S_IDLE         = 3'd0;
    localparam S_START_BIT    = 3'd1;
    localparam S_DATA_BITS    = 3'd2;
    localparam S_STOP_BIT     = 3'd3;
    localparam S_CLEANUP      = 3'd4;

    reg [2:0] state;
    reg [15:0] clk_count;
    reg [2:0] bit_index;
    reg [7:0] rx_shift;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state      <= S_IDLE;
            rx_dv      <= 1'b0;
            rx_byte    <= 8'd0;
            clk_count  <= 16'd0;
            bit_index  <= 3'd0;
            rx_shift   <= 8'd0;
        end else begin
            case (state)
                S_IDLE: begin
                    rx_dv <= 1'b0;
                    clk_count <= 16'd0;
                    bit_index <= 3'd0;

                    if (rx == 1'b0)
                        state <= S_START_BIT;
                    else
                        state <= S_IDLE;
                end

                S_START_BIT: begin
                    if (clk_count == (CLKS_PER_BIT - 1) / 2) begin
                        if (rx == 1'b0) begin
                            clk_count <= 16'd0;
                            state <= S_DATA_BITS;
                        end else begin
                            state <= S_IDLE;
                        end
                    end else begin
                        clk_count <= clk_count + 1'b1;
                        state <= S_START_BIT;
                    end
                end

                S_DATA_BITS: begin
                    if (clk_count < CLKS_PER_BIT - 1) begin
                        clk_count <= clk_count + 1'b1;
                        state <= S_DATA_BITS;
                    end else begin
                        clk_count <= 16'd0;
                        rx_shift[bit_index] <= rx;
                        if (bit_index < 3'd7) begin
                            bit_index <= bit_index + 1'b1;
                            state <= S_DATA_BITS;
                        end else begin
                            bit_index <= 3'd0;
                            state <= S_STOP_BIT;
                        end
                    end
                end

                S_STOP_BIT: begin
                    if (clk_count < CLKS_PER_BIT - 1) begin
                        clk_count <= clk_count + 1'b1;
                        state <= S_STOP_BIT;
                    end else begin
                        rx_dv <= 1'b1;
                        rx_byte <= rx_shift;
                        clk_count <= 16'd0;
                        state <= S_CLEANUP;
                    end
                end

                S_CLEANUP: begin
                    rx_dv <= 1'b0;
                    state <= S_IDLE;
                end

                default: state <= S_IDLE;
            endcase
        end
    end

endmodule
