`timescale 1ns/1ps

module uart_tx #(
    parameter CLKS_PER_BIT = 868
) (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       in_valid,
    input  wire [7:0] in_data,
    output wire       in_ready,
    output reg        tx,
    output reg        tx_active,
    output reg        tx_done
);

    localparam S_IDLE      = 3'd0;
    localparam S_START_BIT = 3'd1;
    localparam S_DATA_BITS = 3'd2;
    localparam S_STOP_BIT  = 3'd3;
    localparam S_CLEANUP   = 3'd4;

    reg [2:0] state;
    reg [15:0] clk_count;
    reg [2:0] bit_index;
    reg [7:0] tx_data;

    assign in_ready = (state == S_IDLE);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state      <= S_IDLE;
            tx         <= 1'b1;
            tx_active  <= 1'b0;
            tx_done    <= 1'b0;
            clk_count  <= 16'd0;
            bit_index  <= 3'd0;
            tx_data    <= 8'd0;
        end else begin
            case (state)
                S_IDLE: begin
                    tx        <= 1'b1;
                    tx_done   <= 1'b0;
                    clk_count <= 16'd0;
                    bit_index <= 3'd0;

                    if (in_valid) begin
                        tx_active <= 1'b1;
                        tx_data   <= in_data;
                        state     <= S_START_BIT;
                    end else begin
                        tx_active <= 1'b0;
                        state     <= S_IDLE;
                    end
                end

                S_START_BIT: begin
                    tx <= 1'b0;
                    if (clk_count < CLKS_PER_BIT - 1) begin
                        clk_count <= clk_count + 1'b1;
                        state <= S_START_BIT;
                    end else begin
                        clk_count <= 16'd0;
                        state <= S_DATA_BITS;
                    end
                end

                S_DATA_BITS: begin
                    tx <= tx_data[bit_index];
                    if (clk_count < CLKS_PER_BIT - 1) begin
                        clk_count <= clk_count + 1'b1;
                        state <= S_DATA_BITS;
                    end else begin
                        clk_count <= 16'd0;
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
                    tx <= 1'b1;
                    if (clk_count < CLKS_PER_BIT - 1) begin
                        clk_count <= clk_count + 1'b1;
                        state <= S_STOP_BIT;
                    end else begin
                        tx_done <= 1'b1;
                        clk_count <= 16'd0;
                        state <= S_CLEANUP;
                    end
                end

                S_CLEANUP: begin
                    tx_active <= 1'b0;
                    state <= S_IDLE;
                end

                default: state <= S_IDLE;
            endcase
        end
    end

endmodule
