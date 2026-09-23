// ============================================================================
// File: mask_rom.v
// Project: rdm6300-picorv32-rom-data
// Description: Pure Read-Only Mask ROM (8 KBytes = 2048 words x 32 bits)
//              Direct $readmemh initialization for 100% clean Block RAM inference
//              in Xilinx Vivado (Basys 3) and combinational logic in ASIC Sky130.
// ============================================================================

`timescale 1ns / 1ps

module mask_rom #(
    parameter WORDS = 2048,
    parameter INIT_FILE = ""
)(
    input  wire        clk,
    input  wire        rst_n,
    input  wire        valid,
    input  wire [12:0] addr,     // Word address: 2048 words = [12:2] (11 bits)
    output reg  [31:0] rdata,
    output reg         ready
);

    reg [31:0] rom [0:WORDS-1];

    integer i;
    initial begin
        for (i = 0; i < WORDS; i = i + 1) begin
            rom[i] = 32'h00000013; // NOP (addi x0, x0, 0)
        end
        if (INIT_FILE != "") begin
            $readmemh(INIT_FILE, rom);
        end
    end

    wire [10:0] word_addr = addr[12:2];
    wire req_fire = valid && !ready;

    // Synchronous Read with single-cycle ready response
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            ready <= 1'b0;
            rdata <= 32'd0;
        end else begin
            ready <= req_fire;
            if (req_fire) begin
                rdata <= rom[word_addr];
            end
        end
    end

endmodule
