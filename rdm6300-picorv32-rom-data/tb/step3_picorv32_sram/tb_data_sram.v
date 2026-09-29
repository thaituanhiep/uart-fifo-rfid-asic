// ============================================================================
// File: tb/step3_picorv32_sram/tb_data_sram.v
// Project: rdm6300-picorv32-rom-data
// Description: Comprehensive Verilog Testbench for 1KB On-Chip Data SRAM (data_sram.v)
//              Verifies 32-bit word, 16-bit halfword, and 8-bit byte write strobes,
//              synchronous read latency, address decoding, and ready handshake.
// ============================================================================

`timescale 1ns / 1ps

module tb_data_sram;

    reg         clk;
    reg         rst_n;
    reg         valid;
    reg  [9:0]  addr;
    reg  [31:0] wdata;
    reg  [3:0]  wstrb;
    wire [31:0] rdata;
    wire        ready;

    integer tests_passed = 0;
    integer tests_failed = 0;

    // 50 MHz clock (20ns period)
    always #10 clk = ~clk;

    // Instantiate DUT
    data_sram #(
        .WORDS(256)
    ) dut (
        .clk(clk),
        .rst_n(rst_n),
        .valid(valid),
        .addr(addr),
        .wdata(wdata),
        .wstrb(wstrb),
        .rdata(rdata),
        .ready(ready)
    );

    // Task: Synchronous Write Transaction
    task sram_write(input [9:0] target_addr, input [31:0] data, input [3:0] strb);
        begin
            @(posedge clk);
            valid <= 1'b1;
            addr  <= target_addr;
            wdata <= data;
            wstrb <= strb;
            @(posedge clk);
            while (!ready) @(posedge clk);
            valid <= 1'b0;
            wstrb <= 4'b0000;
        end
    endtask

    // Task: Synchronous Read Transaction
    task sram_read(input [9:0] target_addr, output [31:0] read_val);
        begin
            @(posedge clk);
            valid <= 1'b1;
            addr  <= target_addr;
            wstrb <= 4'b0000;
            @(posedge clk);
            while (!ready) @(posedge clk);
            read_val = rdata;
            valid <= 1'b0;
        end
    endtask

    reg [31:0] read_data;

    initial begin
        $display("======================================================================");
        $display("  STARTING TESTBENCH: 1KB DATA SRAM (Step 3: Hardware Memory System)  ");
        $display("======================================================================");

        clk   = 0;
        rst_n = 0;
        valid = 0;
        addr  = 0;
        wdata = 0;
        wstrb = 0;

        // Reset pulse
        #40;
        rst_n = 1;
        #20;

        // --------------------------------------------------------------------
        // Test 1: Full 32-bit Word Write and Read Back
        // --------------------------------------------------------------------
        $display("\n[TEST 1] Testing 32-bit Full Word Write and Read Back...");
        sram_write(10'h000, 32'hDEADBEEF, 4'b1111);
        sram_read(10'h000, read_data);

        if (read_data === 32'hDEADBEEF) begin
            $display("  [PASS] Addr 0x000: Wrote 0xDEADBEEF, Read 0x%08X", read_data);
            tests_passed = tests_passed + 1;
        end else begin
            $display("  [FAIL] Addr 0x000: Expected 0xDEADBEEF, got 0x%08X", read_data);
            tests_failed = tests_failed + 1;
        end

        // --------------------------------------------------------------------
        // Test 2: Byte-Enable Write Strobes (wstrb[0..3])
        // --------------------------------------------------------------------
        $display("\n[TEST 2] Testing Byte-Wise Write Enables without corrupting neighbor bytes...");
        // Initialize Word at Addr 0x004 to 0x11223344
        sram_write(10'h004, 32'h11223344, 4'b1111);

        // Modify Byte 0 only (wstrb = 4'b0001, new byte = 0xAA)
        sram_write(10'h004, 32'h000000AA, 4'b0001);
        sram_read(10'h004, read_data);
        if (read_data === 32'h112233AA) begin
            $display("  [PASS] Byte 0 modification: 0x112233AA (Expected 0x112233AA)");
            tests_passed = tests_passed + 1;
        end else begin
            $display("  [FAIL] Byte 0 modification: Expected 0x112233AA, got 0x%08X", read_data);
            tests_failed = tests_failed + 1;
        end

        // Modify Byte 2 only (wstrb = 4'b0100, new byte = 0xBB)
        sram_write(10'h004, 32'h00BB0000, 4'b0100);
        sram_read(10'h004, read_data);
        if (read_data === 32'h11BB33AA) begin
            $display("  [PASS] Byte 2 modification: 0x11BB33AA (Expected 0x11BB33AA)");
            tests_passed = tests_passed + 1;
        end else begin
            $display("  [FAIL] Byte 2 modification: Expected 0x11BB33AA, got 0x%08X", read_data);
            tests_failed = tests_failed + 1;
        end

        // --------------------------------------------------------------------
        // Test 3: Half-Word (16-bit) Write Strobes (wstrb[1:0] and wstrb[3:2])
        // --------------------------------------------------------------------
        $display("\n[TEST 3] Testing 16-bit Half-Word Write Strobes...");
        sram_write(10'h008, 32'h55667788, 4'b1111);
        // Overwrite Lower 16-bit with 0xCAFE
        sram_write(10'h008, 32'h0000CAFE, 4'b0011);
        sram_read(10'h008, read_data);
        if (read_data === 32'h5566CAFE) begin
            $display("  [PASS] Lower Halfword write: 0x5566CAFE (Expected 0x5566CAFE)");
            tests_passed = tests_passed + 1;
        end else begin
            $display("  [FAIL] Lower Halfword write: Expected 0x5566CAFE, got 0x%08X", read_data);
            tests_failed = tests_failed + 1;
        end

        // --------------------------------------------------------------------
        // Test 4: Highest Address Boundary (Slot 255 = 10'h3FC = 1020 bytes)
        // --------------------------------------------------------------------
        $display("\n[TEST 4] Testing Top Address Boundary (Word 255 = Addr 0x3FC)...");
        sram_write(10'h3FC, 32'hA5A55A5A, 4'b1111);
        sram_read(10'h3FC, read_data);
        if (read_data === 32'hA5A55A5A) begin
            $display("  [PASS] Boundary Word 255: 0xA5A55A5A (Expected 0xA5A55A5A)");
            tests_passed = tests_passed + 1;
        end else begin
            $display("  [FAIL] Boundary Word 255: Expected 0xA5A55A5A, got 0x%08X", read_data);
            tests_failed = tests_failed + 1;
        end

        // --------------------------------------------------------------------
        // Test 5: Handshake Timing Verification
        // --------------------------------------------------------------------
        $display("\n[TEST 5] Testing Ready Handshake Timing...");
        @(posedge clk);
        valid <= 1'b1;
        addr  <= 10'h000;
        wstrb <= 4'b0000;
        @(posedge clk);
        #1;
        if (ready === 1'b1) begin
            $display("  [PASS] ready asserted in exactly 1 clock cycle after valid.");
            tests_passed = tests_passed + 1;
        end else begin
            $display("  [FAIL] ready was NOT asserted 1 cycle after valid!");
            tests_failed = tests_failed + 1;
        end
        valid <= 1'b0;
        @(posedge clk);
        #1;
        if (ready === 1'b0) begin
            $display("  [PASS] ready de-asserted cleanly when valid was lowered.");
            tests_passed = tests_passed + 1;
        end else begin
            $display("  [FAIL] ready did not de-assert cleanly!");
            tests_failed = tests_failed + 1;
        end

        // --------------------------------------------------------------------
        // Summary
        // --------------------------------------------------------------------
        $display("\n======================================================================");
        $display("  1KB DATA SRAM TEST RESULTS: %0d PASSED, %0d FAILED", tests_passed, tests_failed);
        $display("======================================================================");
        if (tests_failed == 0) begin
            $display("  >>> ALL 1KB DATA SRAM TESTS PASSED SUCCESSFULLY! <<<\n");
        end else begin
            $display("  >>> SOME TESTS FAILED! <<<\n");
        end
        $finish;
    end

endmodule
