`timescale 1ns/1ps

// Ready/valid byte FIFO dedicated to the UART RX -> parser path.
// The head is exposed continuously so the top needs no read-latency FSM.
module rx_fifo #(
    parameter DATA_W = 8,
    parameter DEPTH  = 16,
    parameter ADDR_W = 4
) (
    input  wire              clk,
    input  wire              rst_n,
    input  wire              in_valid,
    input  wire [DATA_W-1:0] in_data,
    output wire              in_ready,
    output wire              out_valid,
    output wire [DATA_W-1:0] out_data,
    input  wire              out_ready,
    output wire              full,
    output wire              empty,
    output reg  [ADDR_W:0]   level,
    output reg               overflow_pulse,
    output reg               underflow_pulse
);
    reg [DATA_W-1:0] mem [0:DEPTH-1];
    reg [ADDR_W-1:0] wr_ptr;
    reg [ADDR_W-1:0] rd_ptr;

    wire do_write = in_valid && in_ready;
    wire do_read  = out_valid && out_ready;

    assign full  = (level == DEPTH);
    assign empty = (level == 0);
    assign in_ready = !full;
    assign out_valid = !empty;
    assign out_data = mem[rd_ptr];

    always @(posedge clk) begin
        if (do_write)
            mem[wr_ptr] <= in_data;
    end

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            wr_ptr          <= {ADDR_W{1'b0}};
            rd_ptr          <= {ADDR_W{1'b0}};
            level           <= {(ADDR_W+1){1'b0}};
            overflow_pulse  <= 1'b0;
            underflow_pulse <= 1'b0;
        end else begin
            overflow_pulse  <= in_valid && !in_ready;
            underflow_pulse <= out_ready && !out_valid;

            if (do_write)
                wr_ptr <= wr_ptr + 1'b1;

            if (do_read)
                rd_ptr  <= rd_ptr + 1'b1;

            case ({do_write, do_read})
                2'b10: level <= level + 1'b1;
                2'b01: level <= level - 1'b1;
                default: level <= level;
            endcase
        end
    end
endmodule
