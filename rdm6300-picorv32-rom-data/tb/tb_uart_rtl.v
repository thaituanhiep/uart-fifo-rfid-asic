// ============================================================================
// File: tb/tb_uart_rtl.v
// Project: rdm6300-picorv32-rom-data
// Description: Pure RTL Testbench for UART MMIO Module (uart_mmio.v)
//              Verifies:
//              1. Memory-Mapped bus interface (CSR read/write, ready/valid handshakes)
//              2. Baud rate divider register (offset 0x0)
//              3. Serial TX transmission waveform, bit timing, and data integrity
//              4. Serial RX reception, CDC 2-FF synchronizer, and FIFO buffering
//              5. RX FIFO read (offset 0x4) and empty flag handling (0xFFFFFFFF)
//              6. Back-to-back multi-byte burst transmission & reception
// ============================================================================

`timescale 1ns / 1ps

module tb_uart_rtl;

    // ------------------------------------------------------------------------
    // Clock & Reset Generation
    // ------------------------------------------------------------------------
    reg clk;
    reg rst_n;

    // 100 MHz clock (10 ns period)
    always #5 clk = ~clk;

    localparam CLK_PERIOD = 10;
    localparam TEST_DIV   = 16;
    localparam BIT_CYCLES = TEST_DIV + 2; // simpleuart counter counts 0..(cfg_divider+1) = cfg_divider+2 cycles
    localparam BIT_PERIOD = BIT_CYCLES * CLK_PERIOD; // 180 ns per bit

    // ------------------------------------------------------------------------
    // DUT Interface Signals
    // ------------------------------------------------------------------------
    reg         rx_i;
    wire        tx_o;

    reg         valid;
    reg  [3:0]  addr;
    reg  [31:0] wdata;
    reg  [3:0]  wstrb;
    wire [31:0] rdata;
    wire        ready;

    wire        rx_activity_o;

    // ------------------------------------------------------------------------
    // DUT Instantiation
    // ------------------------------------------------------------------------
    uart_mmio #(
        .DEFAULT_DIV(TEST_DIV),
        .FIFO_DEPTH(16)
    ) dut (
        .clk(clk),
        .rst_n(rst_n),
        .rx_i(rx_i),
        .tx_o(tx_o),
        .valid(valid),
        .addr(addr),
        .wdata(wdata),
        .wstrb(wstrb),
        .rdata(rdata),
        .ready(ready),
        .rx_activity_o(rx_activity_o)
    );

    // ------------------------------------------------------------------------
    // Bus Access Tasks
    // ------------------------------------------------------------------------
    task bus_write(input [3:0] a, input [31:0] d);
        begin
            @(posedge clk);
            valid <= 1'b1;
            addr  <= a;
            wdata <= d;
            wstrb <= 4'b1111;
            @(posedge clk);
            while (!ready) @(posedge clk);
            valid <= 1'b0;
            wstrb <= 4'b0000;
            @(posedge clk);
        end
    endtask

    task bus_read(input [3:0] a, output [31:0] d);
        begin
            @(posedge clk);
            valid <= 1'b1;
            addr  <= a;
            wdata <= 32'd0;
            wstrb <= 4'b0000;
            @(posedge clk);
            while (!ready) @(posedge clk);
            d = rdata;
            valid <= 1'b0;
            @(posedge clk);
        end
    endtask

    // ------------------------------------------------------------------------
    // Serial Transmission / Reception Tasks
    // ------------------------------------------------------------------------
    task send_serial_byte(input [7:0] b);
        integer k;
        begin
            // Start bit (0)
            rx_i = 1'b0;
            #BIT_PERIOD;
            // 8 Data bits (LSB first)
            for (k = 0; k < 8; k = k + 1) begin
                rx_i = b[k];
                #BIT_PERIOD;
            end
            // Stop bit (1)
            rx_i = 1'b1;
            #BIT_PERIOD;
            #(BIT_PERIOD / 2);
        end
    endtask

    task recv_serial_byte(output [7:0] b);
        integer k;
        begin
            @(negedge tx_o); // Detect falling edge of start bit
            #(BIT_PERIOD + BIT_PERIOD / 2); // Jump to center of bit 0
            for (k = 0; k < 8; k = k + 1) begin
                b[k] = tx_o;
                #BIT_PERIOD;
            end
        end
    endtask

    // ------------------------------------------------------------------------
    // Test Verification Execution
    // ------------------------------------------------------------------------
    reg [31:0] read_val;
    reg [7:0]  captured_tx;
    integer    err_count;

    initial begin
        $display("================================================================");
        $display("  STARTING TESTBENCH: tb_uart_rtl (uart_mmio Pure RTL)");
        $display("================================================================");

        clk       = 0;
        rst_n     = 0;
        rx_i      = 1'b1;
        valid     = 1'b0;
        addr      = 4'd0;
        wdata     = 32'd0;
        wstrb     = 4'd0;
        err_count = 0;

        // Reset Pulse
        #100;
        rst_n = 1;
        #50;
        $display("[TB] System Reset released.");

        // --------------------------------------------------------------------
        // TEST 1: Check Default Divider
        // --------------------------------------------------------------------
        $display("\n--- [TEST 1] Check Default Baud Divider ---");
        bus_read(4'h0, read_val);
        if (read_val === TEST_DIV) begin
            $display("[PASS] Default divider matches expected %0d", TEST_DIV);
        end else begin
            $display("[FAIL] Expected divider %0d, got %0d", TEST_DIV, read_val);
            err_count = err_count + 1;
        end

        // --------------------------------------------------------------------
        // TEST 2: Write & Read New Baud Divider
        // --------------------------------------------------------------------
        $display("\n--- [TEST 2] Write and Read Modified Baud Divider ---");
        bus_write(4'h0, 32'd42);
        bus_read(4'h0, read_val);
        if (read_val === 32'd42) begin
            $display("[PASS] Modified divider successfully read back: 42");
        end else begin
            $display("[FAIL] Expected divider 42, got %0d", read_val);
            err_count = err_count + 1;
        end
        // Restore TEST_DIV
        bus_write(4'h0, TEST_DIV);
        #(20 * BIT_PERIOD); // Wait for simpleuart dummy bits to settle

        // --------------------------------------------------------------------
        // TEST 3: Serial TX Waveform Verification
        // --------------------------------------------------------------------
        $display("\n--- [TEST 3] Serial TX Transmission ---");
        fork
            begin
                bus_write(4'h4, 32'h0000004B); // Transmit 'K' (0x4B)
            end
            begin
                recv_serial_byte(captured_tx);
            end
        join

        if (captured_tx === 8'h4B) begin
            $display("[PASS] Serial TX accurately transmitted byte: 0x%02X ('%c')", captured_tx, captured_tx);
        end else begin
            $display("[FAIL] Serial TX expected 0x4B, captured 0x%02X", captured_tx);
            err_count = err_count + 1;
        end

        // --------------------------------------------------------------------
        // TEST 4: Serial RX & FIFO Reception
        // --------------------------------------------------------------------
        $display("\n--- [TEST 4] Serial RX & FIFO Reception ---");
        // Verify initially FIFO is empty
        bus_read(4'h4, read_val);
        if (read_val === 32'hFFFFFFFF && rx_activity_o === 1'b0) begin
            $display("[PASS] Initial RX FIFO is empty (read 0xFFFFFFFF, activity=0)");
        end else begin
            $display("[FAIL] Initial FIFO not empty: read=0x%08X, activity=%b", read_val, rx_activity_o);
            err_count = err_count + 1;
        end

        // Send byte 'M' (0x4D) into rx_i
        send_serial_byte(8'h4D);
        #50;

        if (rx_activity_o === 1'b1) begin
            $display("[PASS] rx_activity_o asserted after byte reception");
        end else begin
            $display("[FAIL] rx_activity_o not asserted!");
            err_count = err_count + 1;
        end

        bus_read(4'h4, read_val);
        if (read_val === 32'h0000004D) begin
            $display("[PASS] Successfully read received byte from FIFO: 0x%02X ('%c')", read_val[7:0], read_val[7:0]);
        end else begin
            $display("[FAIL] Expected 0x4D from FIFO, got 0x%08X", read_val);
            err_count = err_count + 1;
        end

        // Verify FIFO is empty again
        bus_read(4'h4, read_val);
        if (read_val === 32'hFFFFFFFF) begin
            $display("[PASS] RX FIFO empty after read");
        end else begin
            $display("[FAIL] RX FIFO not empty after read: 0x%08X", read_val);
            err_count = err_count + 1;
        end

        // --------------------------------------------------------------------
        // TEST 5: Multi-Byte Burst FIFO Buffering
        // --------------------------------------------------------------------
        $display("\n--- [TEST 5] Multi-Byte Burst FIFO Buffering ---");
        send_serial_byte(8'h31); // '1'
        send_serial_byte(8'h32); // '2'
        send_serial_byte(8'h33); // '3'
        #50;

        bus_read(4'h4, read_val);
        if (read_val[7:0] !== 8'h31) err_count = err_count + 1;
        $display("[BURST 1] Read 0x%02X ('%c')", read_val[7:0], read_val[7:0]);

        bus_read(4'h4, read_val);
        if (read_val[7:0] !== 8'h32) err_count = err_count + 1;
        $display("[BURST 2] Read 0x%02X ('%c')", read_val[7:0], read_val[7:0]);

        bus_read(4'h4, read_val);
        if (read_val[7:0] !== 8'h33) err_count = err_count + 1;
        $display("[BURST 3] Read 0x%02X ('%c')", read_val[7:0], read_val[7:0]);

        bus_read(4'h4, read_val);
        if (read_val !== 32'hFFFFFFFF) err_count = err_count + 1;

        #200;
        $display("\n================================================================");
        if (err_count == 0) begin
            $display("  ALL UART RTL TESTS PASSED SUCCESSFULLY! (0 Errors)");
        end else begin
            $display("  UART RTL TESTS FAILED! Total Errors: %0d", err_count);
        end
        $display("================================================================");
        $finish;
    end

    // Safety timeout
    initial begin
        #500000;
        $display("[TB TIMEOUT] Simulation exceeded 500us!");
        $finish;
    end

endmodule
