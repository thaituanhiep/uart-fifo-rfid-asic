// ============================================================================
// File: data_sram.v
// Project: rdm6300-picorv32-rom-data
// Description: On-Chip Data SRAM with Byte-Write Enables for PicoRV32
//              Size: 1 KByte (256 words x 32 bits = 8,192 bits)
//              Mapped at 0x0000_0000 - 0x0000_03FF for Stack and Data/BSS.
//              Synchronous memory access for clean BRAM inference in Vivado.
// ============================================================================

`timescale 1ns / 1ps

module data_sram #(
    parameter WORDS = 256
)(
    input  wire        clk,
    input  wire        rst_n,
    input  wire        valid,
    input  wire [9:0]  addr,     // Word address: 256 words = [9:2] (8 bits)
    input  wire [31:0] wdata,
    input  wire [3:0]  wstrb,
    output reg  [31:0] rdata,
    output reg         ready
);

    reg [31:0] mem [0:WORDS-1];

    integer i;
    initial begin
        for (i = 0; i < WORDS; i = i + 1) begin
            mem[i] = 32'd0;
        end
    end

    wire [7:0] word_addr = addr[9:2];
    wire req_fire = valid && !ready;

    // Asynchronous reset for ready handshake
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            ready <= 1'b0;
        end else begin
            ready <= req_fire;
        end
    end

    // Synchronous memory array access (No async reset on array allows clean BRAM inference)
    always @(posedge clk) begin
        if (req_fire) begin
            rdata <= mem[word_addr];
            if (wstrb[0]) mem[word_addr][ 7: 0] <= wdata[ 7: 0];
            if (wstrb[1]) mem[word_addr][15: 8] <= wdata[15: 8];
            if (wstrb[2]) mem[word_addr][23:16] <= wdata[23:16];
            if (wstrb[3]) mem[word_addr][31:24] <= wdata[31:24];
        end
    end

endmodule
