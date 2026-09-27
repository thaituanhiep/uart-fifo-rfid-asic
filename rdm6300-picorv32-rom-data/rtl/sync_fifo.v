// ============================================================================
// File: sync_fifo.v
// Project: rdm6300-picorv32-rom-data
// Description: Generic Synchronous FIFO buffer with configurable width and depth.
// ============================================================================

`timescale 1ns / 1ps

module sync_fifo #(
    parameter integer DATA_WIDTH = 8,
    parameter integer DEPTH      = 32
)(
    input  wire                  clk,
    input  wire                  rst_n,

    input  wire                  push,
    input  wire [DATA_WIDTH-1:0] din,

    input  wire                  pop,
    output wire [DATA_WIDTH-1:0] dout,

    output wire                  empty,
    output wire                  full,
    output reg  [$clog2(DEPTH):0] count
);
    localparam integer PTR_WIDTH = $clog2(DEPTH);

    reg [DATA_WIDTH-1:0] mem [0:DEPTH-1];
    reg [PTR_WIDTH-1:0]  wr_ptr;
    reg [PTR_WIDTH-1:0]  rd_ptr;

    assign full  = (count == DEPTH);
    assign empty = (count == 0);
    assign dout  = mem[rd_ptr];

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            wr_ptr <= {PTR_WIDTH{1'b0}};
            rd_ptr <= {PTR_WIDTH{1'b0}};
            count  <= {($clog2(DEPTH)+1){1'b0}};
        end else begin
            if (push && !full) begin
                mem[wr_ptr] <= din;
                wr_ptr      <= wr_ptr + 1'b1;
            end

            if (pop && !empty) begin
                rd_ptr      <= rd_ptr + 1'b1;
            end

            case ({push && !full, pop && !empty})
                2'b10: count <= count + 1'b1;
                2'b01: count <= count - 1'b1;
                default: count <= count;
            endcase
        end
    end

endmodule
