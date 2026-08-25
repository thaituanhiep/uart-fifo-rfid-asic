`timescale 1ns/1ps

// UART 8N1 receiver with 16x oversampling and 3-sample majority voting.
// Samples 7, 8 and 9 of each bit, tolerating one corrupted center sample.
module uart_rx #(
    parameter CLKS_PER_BIT   = 868,
    parameter OVERSAMPLE     = 16,
    parameter BREAK_BITS     = 11,
    parameter BREAK_COUNT_W  = 24
) (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       rx,
    output reg        rx_dv,
    output reg [7:0]  rx_byte,
    output reg        framing_error,
    output reg        break_detect
);
    localparam S_IDLE       = 3'd0;
    localparam S_START_BIT  = 3'd1;
    localparam S_DATA_BITS  = 3'd2;
    localparam S_STOP_BIT   = 3'd3;
    localparam S_CLEANUP    = 3'd4;

    // Integer division gives 651 clocks at 100 MHz/9600 baud. The resulting
    // baud error is far below one percent and all 16 samples stay uniform.
    localparam SAMPLE_DIV = CLKS_PER_BIT / OVERSAMPLE;
    localparam SAMPLE_A   = (OVERSAMPLE / 2) - 1;
    localparam SAMPLE_B   = (OVERSAMPLE / 2);
    localparam SAMPLE_C   = (OVERSAMPLE / 2) + 1;

    reg [2:0]  state;
    reg [15:0] sample_div_count;
    reg [4:0]  sample_phase;
    reg [1:0]  vote_ones;
    reg [2:0]  bit_index;
    reg [7:0]  rx_shift;
    reg [BREAK_COUNT_W-1:0] low_count;

    wire sample_tick = (sample_div_count == SAMPLE_DIV - 1);
    wire vote_sample = (sample_phase == SAMPLE_A) ||
                       (sample_phase == SAMPLE_B) ||
                       (sample_phase == SAMPLE_C);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            low_count    <= {BREAK_COUNT_W{1'b0}};
            break_detect <= 1'b0;
        end else if (rx) begin
            low_count    <= {BREAK_COUNT_W{1'b0}};
            break_detect <= 1'b0;
        end else if (!break_detect) begin
            if (low_count >= (CLKS_PER_BIT * BREAK_BITS) - 1) begin
                break_detect <= 1'b1;
            end else begin
                low_count <= low_count + 1'b1;
            end
        end
    end

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state            <= S_IDLE;
            rx_dv            <= 1'b0;
            rx_byte          <= 8'd0;
            framing_error    <= 1'b0;
            sample_div_count <= 16'd0;
            sample_phase     <= 5'd0;
            vote_ones        <= 2'd0;
            bit_index        <= 3'd0;
            rx_shift         <= 8'd0;
        end else begin
            rx_dv         <= 1'b0;
            framing_error <= 1'b0;

            // A BREAK is not a valid stream of zero bytes. Abort any partial
            // frame and wait for the line to return HIGH before receiving.
            if (break_detect) begin
                state            <= S_IDLE;
                sample_div_count <= 16'd0;
                sample_phase     <= 5'd0;
                vote_ones        <= 2'd0;
                bit_index        <= 3'd0;
            end else begin
              case (state)
                S_IDLE: begin
                    sample_div_count <= 16'd0;
                    sample_phase     <= 5'd0;
                    vote_ones        <= 2'd0;
                    bit_index        <= 3'd0;
                    if (!rx)
                        state <= S_START_BIT;
                end

                S_START_BIT: begin
                    if (sample_tick) begin
                        sample_div_count <= 16'd0;
                        if (vote_sample && rx)
                            vote_ones <= vote_ones + 1'b1;

                        if (sample_phase == OVERSAMPLE - 1) begin
                            sample_phase <= 5'd0;
                            vote_ones    <= 2'd0;
                            if (vote_ones < 2)
                                state <= S_DATA_BITS;
                            else
                                state <= S_IDLE;
                        end else begin
                            sample_phase <= sample_phase + 1'b1;
                        end
                    end else begin
                        sample_div_count <= sample_div_count + 1'b1;
                    end
                end

                S_DATA_BITS: begin
                    if (sample_tick) begin
                        sample_div_count <= 16'd0;
                        if (vote_sample && rx)
                            vote_ones <= vote_ones + 1'b1;

                        if (sample_phase == OVERSAMPLE - 1) begin
                            rx_shift[bit_index] <= (vote_ones >= 2);
                            sample_phase <= 5'd0;
                            vote_ones    <= 2'd0;
                            if (bit_index == 3'd7) begin
                                bit_index <= 3'd0;
                                state <= S_STOP_BIT;
                            end else begin
                                bit_index <= bit_index + 1'b1;
                            end
                        end else begin
                            sample_phase <= sample_phase + 1'b1;
                        end
                    end else begin
                        sample_div_count <= sample_div_count + 1'b1;
                    end
                end

                S_STOP_BIT: begin
                    if (sample_tick) begin
                        sample_div_count <= 16'd0;
                        if (vote_sample && rx)
                            vote_ones <= vote_ones + 1'b1;

                        if (sample_phase == OVERSAMPLE - 1) begin
                            sample_phase <= 5'd0;
                            vote_ones    <= 2'd0;
                            if (vote_ones >= 2) begin
                                rx_byte <= rx_shift;
                                rx_dv   <= 1'b1;
                            end else begin
                                framing_error <= 1'b1;
                            end
                            state <= S_CLEANUP;
                        end else begin
                            sample_phase <= sample_phase + 1'b1;
                        end
                    end else begin
                        sample_div_count <= sample_div_count + 1'b1;
                    end
                end

                S_CLEANUP: begin
                    state <= S_IDLE;
                end

                  default: state <= S_IDLE;
              endcase
            end
        end
    end
endmodule
