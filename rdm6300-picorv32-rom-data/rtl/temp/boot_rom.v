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

    localparam BANK_WORDS = 512;

    // 4 physical banks of 512 words x 32 bits = 2048 words = 8 KBytes
    reg [31:0] bank0 [0:BANK_WORDS-1];
    reg [31:0] bank1 [0:BANK_WORDS-1];
    reg [31:0] bank2 [0:BANK_WORDS-1];
    reg [31:0] bank3 [0:BANK_WORDS-1];

    // Initialize memory banks
    integer i;
    reg [31:0] temp_mem [0:WORDS-1];
    initial begin
        for (i = 0; i < WORDS; i = i + 1) begin
            temp_mem[i] = 32'h00000013; // NOP (addi x0, x0, 0)
        end

        if (INIT_FILE != "") begin
            $readmemh(INIT_FILE, temp_mem);
        end

        for (i = 0; i < BANK_WORDS; i = i + 1) begin
            bank0[i] = temp_mem[i];
            bank1[i] = temp_mem[i + BANK_WORDS];
            bank2[i] = temp_mem[i + 2 * BANK_WORDS];
            bank3[i] = temp_mem[i + 3 * BANK_WORDS];
        end
    end

    // Address Decoding:
    // addr[12:11] selects 1 of 4 banks (each bank is 512 words = 2KB)
    // addr[10:2]  selects the 32-bit word within the bank (9 bits = 512 words)
    wire [1:0] bank_sel  = addr[12:11];
    wire [8:0] bank_addr = addr[10:2];

    wire req_fire = valid && !ready;

    // Synchronous Read / Write with single-cycle ready response
    always @(posedge clk) begin
        if (!rst_n) begin
            ready <= 1'b0;
            rdata <= 32'd0;
        end else begin
            ready <= valid && !ready;
            if (req_fire) begin
                // Read path: 4-to-1 MUX selecting from the 4 localized 512-word banks
                case (bank_sel)
                    2'b00: rdata <= bank0[bank_addr];
                    2'b01: rdata <= bank1[bank_addr];
                    2'b10: rdata <= bank2[bank_addr];
                    2'b11: rdata <= bank3[bank_addr];
                endcase

                // Write path: localized per-bank byte enables
                case (bank_sel)
                    2'b00: begin
                        if (wstrb[0]) bank0[bank_addr][7:0]   <= wdata[7:0];
                        if (wstrb[1]) bank0[bank_addr][15:8]  <= wdata[15:8];
                        if (wstrb[2]) bank0[bank_addr][23:16] <= wdata[23:16];
                        if (wstrb[3]) bank0[bank_addr][31:24] <= wdata[31:24];
                    end
                    2'b01: begin
                        if (wstrb[0]) bank1[bank_addr][7:0]   <= wdata[7:0];
                        if (wstrb[1]) bank1[bank_addr][15:8]  <= wdata[15:8];
                        if (wstrb[2]) bank1[bank_addr][23:16] <= wdata[23:16];
                        if (wstrb[3]) bank1[bank_addr][31:24] <= wdata[31:24];
                    end
                    2'b10: begin
                        if (wstrb[0]) bank2[bank_addr][7:0]   <= wdata[7:0];
                        if (wstrb[1]) bank2[bank_addr][15:8]  <= wdata[15:8];
                        if (wstrb[2]) bank2[bank_addr][23:16] <= wdata[23:16];
                        if (wstrb[3]) bank2[bank_addr][31:24] <= wdata[31:24];
                    end
                    2'b11: begin
                        if (wstrb[0]) bank3[bank_addr][7:0]   <= wdata[7:0];
                        if (wstrb[1]) bank3[bank_addr][15:8]  <= wdata[15:8];
                        if (wstrb[2]) bank3[bank_addr][23:16] <= wdata[23:16];
                        if (wstrb[3]) bank3[bank_addr][31:24] <= wdata[31:24];
                    end
                endcase
            end
        end
    end

endmodule
