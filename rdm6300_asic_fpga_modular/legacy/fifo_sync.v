`timescale 1ns/1ps

module fifo_sync #(
    parameter DATA_W = 8,
    parameter DEPTH = 16,
    parameter ADDR_W = 4
) (
    input  wire              clk,
    input  wire              rst_n,
    input  wire              wr_en,
    input  wire [DATA_W-1:0] wr_data,
    input  wire              rd_en,
    output reg  [DATA_W-1:0] rd_data,
    output wire              full,
    output wire              empty,
    output reg  [ADDR_W:0]   level
);

    reg [DATA_W-1:0] mem [0:DEPTH-1];
    reg [ADDR_W-1:0] wr_ptr;
    reg [ADDR_W-1:0] rd_ptr;

    wire do_write;
    wire do_read;

    assign do_write = wr_en & ~full;
    assign do_read  = rd_en & ~empty;

    assign full  = (level == DEPTH);
    assign empty = (level == 0);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            wr_ptr  <= {ADDR_W{1'b0}};
            rd_ptr  <= {ADDR_W{1'b0}};
            rd_data <= {DATA_W{1'b0}};
            level   <= {(ADDR_W+1){1'b0}};
        end else begin
            if (do_write) begin
                mem[wr_ptr] <= wr_data;
                wr_ptr <= wr_ptr + 1'b1;
            end

            if (do_read) begin
                rd_data <= mem[rd_ptr];
                rd_ptr <= rd_ptr + 1'b1;
            end

            case ({do_write, do_read})
                2'b10: level <= level + 1'b1;
                2'b01: level <= level - 1'b1;
                default: level <= level;
            endcase
        end
    end

endmodule
