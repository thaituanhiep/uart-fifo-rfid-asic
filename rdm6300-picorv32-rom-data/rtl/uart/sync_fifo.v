// ============================================================================
// File: rtl/uart/sync_fifo.v
// Project: rdm6300-picorv32-rom-data
// Description: Generic Synchronous FIFO with parameterized width and depth.
//              Used for buffering UART TX and RX data streams.
// ============================================================================

`timescale 1ns / 1ps

module sync_fifo #(
    parameter DATA_WIDTH = 8,
    parameter DEPTH      = 32
)(
    input  wire                  clk,
    input  wire                  rst_n,

    input  wire                  push,
    input  wire [DATA_WIDTH-1:0] din,

    input  wire                  pop,
    output wire [DATA_WIDTH-1:0] dout,

    output wire                  empty,
    output wire                  full,
    output wire [$clog2(DEPTH):0] count
);

    localparam ADDR_WIDTH = $clog2(DEPTH);

    reg [DATA_WIDTH-1:0] mem [0:DEPTH-1];
    reg [ADDR_WIDTH:0]   wr_ptr;
    reg [ADDR_WIDTH:0]   rd_ptr;

    // Status Flags
    assign empty = (wr_ptr == rd_ptr);
    assign full  = (wr_ptr[ADDR_WIDTH] != rd_ptr[ADDR_WIDTH]) &&
                   (wr_ptr[ADDR_WIDTH-1:0] == rd_ptr[ADDR_WIDTH-1:0]);
    assign count = wr_ptr - rd_ptr;

    // First-word fall-through / synchronous read
    assign dout  = mem[rd_ptr[ADDR_WIDTH-1:0]];

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            wr_ptr <= 0;
            rd_ptr <= 0;
        end else begin
            if (push && !full) begin
                mem[wr_ptr[ADDR_WIDTH-1:0]] <= din;
                wr_ptr <= wr_ptr + 1'b1;
            end
            if (pop && !empty) begin
                rd_ptr <= rd_ptr + 1'b1;
            end
        end
    end

endmodule
