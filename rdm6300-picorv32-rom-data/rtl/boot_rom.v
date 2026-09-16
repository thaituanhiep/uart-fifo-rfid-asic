// ============================================================================
// File: boot_rom.v
// Project: rdm6300-picorv32-rom-data
// Description: On-Chip SRAM / Boot ROM with Byte Write Enables for PicoRV32
// Size: 8 KBytes (2048 words x 32 bits)
// ============================================================================

`timescale 1ns / 1ps

module boot_rom #(
    parameter WORDS = 2048,
    parameter INIT_FILE = ""
)(
    input  wire        clk,
    input  wire        rst_n,
    input  wire        valid,
    input  wire [12:0] addr,     // Word address: 2048 words = 11 bits [12:2]
    input  wire [31:0] wdata,
    input  wire [3:0]  wstrb,
    output reg  [31:0] rdata,
    output reg         ready
);

    reg [31:0] mem [0:WORDS-1];

    // Initialize memory
    integer i;
    initial begin
        for (i = 0; i < WORDS; i = i + 1) begin
            mem[i] = 32'h00000013; // NOP (addi x0, x0, 0)
        end

        if (INIT_FILE != "") begin
            $readmemh(INIT_FILE, mem);
        end
    end

    // Synchronous Read / Write with single-cycle ready response
    always @(posedge clk) begin
        if (!rst_n) begin
            ready <= 1'b0;
            rdata <= 32'd0;
        end else begin
            ready <= valid && !ready;
            if (valid && !ready) begin
                if (wstrb[0]) mem[addr[12:2]][7:0]   <= wdata[7:0];
                if (wstrb[1]) mem[addr[12:2]][15:8]  <= wdata[15:8];
                if (wstrb[2]) mem[addr[12:2]][23:16] <= wdata[23:16];
                if (wstrb[3]) mem[addr[12:2]][31:24] <= wdata[31:24];
                rdata <= mem[addr[12:2]];
            end
        end
    end

endmodule
