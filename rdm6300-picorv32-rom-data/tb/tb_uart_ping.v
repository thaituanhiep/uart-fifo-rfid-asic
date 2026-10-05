// ============================================================================
// File: tb/tb_uart_ping.v
// Project: rdm6300-picorv32-rom-data
// Description: End-to-End System-Level Testbench for PicoRV32 RFID SoC.
//              Verifies:
//              1. SPI Flash XIP Boot: PicoRV32 boots C firmware from offset 0x250000.
//              2. Boot Banner: Verifies SoC starts up and prints ready message.
//              3. Host PC Ping Command: PC sends 'P' + '\n' over UART.
//              4. SoC Response: PicoRV32 processes command and returns "PONG".
//              5. CPU Health: Verifies zero trap (cpu_trap == 0).
// ============================================================================

`timescale 1ns / 1ps

module tb_uart_ping;

    // ------------------------------------------------------------------------
    // Clock & Reset Generation
    // ------------------------------------------------------------------------
    reg clk;
    reg rst_n;

    // 100 MHz System Clock (10 ns period)
    always #5 clk = ~clk;

    // Fast baud simulation: DIV = 16 (18 cycles per bit = 180 ns)
    localparam CLK_PERIOD = 10;
    localparam DIV        = 16;
    localparam BIT_CYCLES = DIV + 2;
    localparam BIT_PERIOD = BIT_CYCLES * CLK_PERIOD; // 180 ns

    // ------------------------------------------------------------------------
    // SoC Interface Signals
    // ------------------------------------------------------------------------
    reg         rdm6300_rx_i;
    reg         uart_rx_i;
    wire        uart_tx_o;

    wire        flash_csb;
    wire        flash_clk;
    wire        flash_io0_oe;
    wire        flash_io1_oe;
    wire        flash_io2_oe;
    wire        flash_io3_oe;
    wire        flash_io0_do;
    wire        flash_io1_do;
    wire        flash_io2_do;
    wire        flash_io3_do;
    wire        flash_io0_di;
    wire        flash_io1_di;
    wire        flash_io2_di;
    wire        flash_io3_di;

    wire [15:0] leds_o;
    wire        cpu_trap;
    wire        card_event_o;
    wire        flash_busy_o;
    wire        flash_done_o;

    // ------------------------------------------------------------------------
    // DUT Instantiation
    // ------------------------------------------------------------------------
    rdm6300_picorv32_soc #(
        .CLK_FREQ_HZ(100_000_000),
        .UART_BAUD(6_250_000) // DIV = 16 (fast simulation)
    ) dut (
        .clk(clk),
        .rst_n(rst_n),
        .rdm6300_rx_i(rdm6300_rx_i),
        .uart_tx_o(uart_tx_o),
        .uart_rx_i(uart_rx_i),
        .flash_csb(flash_csb),
        .flash_clk(flash_clk),
        .flash_io0_oe(flash_io0_oe),
        .flash_io1_oe(flash_io1_oe),
        .flash_io2_oe(flash_io2_oe),
        .flash_io3_oe(flash_io3_oe),
        .flash_io0_do(flash_io0_do),
        .flash_io1_do(flash_io1_do),
        .flash_io2_do(flash_io2_do),
        .flash_io3_do(flash_io3_do),
        .flash_io0_di(flash_io0_di),
        .flash_io1_di(flash_io1_di),
        .flash_io2_di(flash_io2_di),
        .flash_io3_di(flash_io3_di),
        .leds_o(leds_o),
        .cpu_trap(cpu_trap),
        .card_event_o(card_event_o),
        .flash_busy_o(flash_busy_o),
        .flash_done_o(flash_done_o)
    );

    // ------------------------------------------------------------------------
    // Behavioral SPI Flash Memory Model (Preloaded with firmware.hex)
    // ------------------------------------------------------------------------
    reg [31:0] fw_words [0:2047];
    reg [7:0]  flash_mem [0:16383]; // 16KB Flash buffer for code at 0x250000
    integer i;

    initial begin
        for (i = 0; i < 16384; i = i + 1) flash_mem[i] = 8'hFF;
        $readmemh("firmware.hex", fw_words);
        if (fw_words[0] === 32'bx || fw_words[0] === 32'bz) begin
            $display("\n================================================================");
            $display("  [TB ERROR] File 'firmware.hex' could NOT be opened in xsim!");
            $display("  CPU has no instructions to execute and will TRAP immediately.");
            $display("----------------------------------------------------------------");
            $display("  [FIX] Run this command in Vivado Tcl Console and re-simulate:");
            $display("  add_files -fileset sim_1 -norecurse D:/VirtualSharedFolders/uart-fifo-rfid-asic/rdm6300-picorv32-rom-data/firmware/firmware.hex");
            $display("================================================================\n");
        end else begin
            for (i = 0; i < 2048; i = i + 1) begin
                flash_mem[i*4 + 0] = fw_words[i][ 7: 0];
                flash_mem[i*4 + 1] = fw_words[i][15: 8];
                flash_mem[i*4 + 2] = fw_words[i][23:16];
                flash_mem[i*4 + 3] = fw_words[i][31:24];
            end
            $display("[FLASH MODEL] Loaded 2048 words (8192 bytes) from firmware.hex");
        end
    end

    reg [7:0]  spi_cmd;
    reg [23:0] spi_addr;
    reg [7:0]  spi_rx_byte;
    reg [2:0]  spi_rx_bit;
    integer    spi_byte_cnt;
    reg [7:0]  spi_tx_byte;
    reg [2:0]  spi_tx_bit;
    reg        flash_miso;

    assign flash_io0_di = 1'b0;
    assign flash_io1_di = flash_csb ? 1'b0 : flash_miso;
    assign flash_io2_di = 1'b1;
    assign flash_io3_di = 1'b1;

    function [7:0] get_flash_byte(input [23:0] addr);
        begin
            if (addr >= 24'h250000 && addr < (24'h250000 + 16384)) begin
                get_flash_byte = flash_mem[addr - 24'h250000];
            end else begin
                get_flash_byte = 8'hFF;
            end
        end
    endfunction

    always @(posedge flash_csb) begin
        flash_miso   <= 1'b0;
        spi_byte_cnt <= 0;
        spi_rx_bit   <= 7;
        spi_rx_byte  <= 8'd0;
    end

    always @(negedge flash_csb) begin
        flash_miso   <= 1'b0;
        spi_byte_cnt <= 0;
        spi_rx_bit   <= 7;
        spi_rx_byte  <= 8'd0;
    end

    always @(posedge flash_clk) begin
        if (!flash_csb) begin
            spi_rx_byte[spi_rx_bit] <= flash_io0_do;
            if (spi_rx_bit == 0) begin
                spi_rx_bit   <= 7;
                spi_byte_cnt <= spi_byte_cnt + 1;
                if (spi_byte_cnt == 0) begin
                    spi_cmd <= {spi_rx_byte[7:1], flash_io0_do};
                end else if (spi_byte_cnt == 1) begin
                    spi_addr[23:16] <= {spi_rx_byte[7:1], flash_io0_do};
                end else if (spi_byte_cnt == 2) begin
                    spi_addr[15:8] <= {spi_rx_byte[7:1], flash_io0_do};
                end else if (spi_byte_cnt == 3) begin
                    spi_addr[7:0] <= {spi_rx_byte[7:1], flash_io0_do};
                    spi_tx_byte   <= get_flash_byte({spi_addr[23:8], spi_rx_byte[7:1], flash_io0_do});
                    spi_tx_bit    <= 7;
                    spi_addr      <= {spi_addr[23:8], spi_rx_byte[7:1], flash_io0_do} + 1'b1;
                end else begin
                    spi_tx_byte   <= get_flash_byte(spi_addr);
                    spi_tx_bit    <= 7;
                    spi_addr      <= spi_addr + 1'b1;
                end
            end else begin
                spi_rx_bit <= spi_rx_bit - 1;
            end
        end
    end

    always @(negedge flash_clk) begin
        if (!flash_csb) begin
            if (spi_byte_cnt >= 4 && (spi_cmd == 8'h03 || spi_cmd == 8'h0B)) begin
                flash_miso <= spi_tx_byte[spi_tx_bit];
                if (spi_tx_bit > 0)
                    spi_tx_bit <= spi_tx_bit - 1;
                else
                    spi_tx_bit <= 7;
            end else begin
                flash_miso <= 1'b0;
            end
        end else begin
            flash_miso <= 1'b0;
        end
    end

    // ------------------------------------------------------------------------
    // Host PC UART Transmitter Task
    // ------------------------------------------------------------------------
    task send_pc_byte(input [7:0] b);
        integer k;
        begin
            uart_rx_i = 1'b0; // start bit
            #BIT_PERIOD;
            for (k = 0; k < 8; k = k + 1) begin
                uart_rx_i = b[k];
                #BIT_PERIOD;
            end
            uart_rx_i = 1'b1; // stop bit
            #BIT_PERIOD;
            #(BIT_PERIOD);
        end
    endtask

    // ------------------------------------------------------------------------
    // UART Output Monitor & Response Matcher
    // ------------------------------------------------------------------------
    reg [7:0]  tx_byte;
    integer    bit_idx;
    reg [39:0] ready_shifter = 40'd0;
    reg        ready_matched = 1'b0;
    reg [31:0] pong_shifter  = 32'd0;
    reg        pong_matched  = 1'b0;

    always @(negedge uart_tx_o) begin
        // Start bit detected: wait 1.5 bit periods to center of bit 0
        #(BIT_PERIOD + BIT_PERIOD / 2);
        for (bit_idx = 0; bit_idx < 8; bit_idx = bit_idx + 1) begin
            tx_byte[bit_idx] = uart_tx_o;
            #BIT_PERIOD;
        end
        $write("%c", tx_byte);
        ready_shifter = {ready_shifter[31:0], tx_byte};
        if (ready_shifter == 40'h5265616479) begin // "Ready"
            ready_matched = 1'b1;
        end

        pong_shifter = {pong_shifter[23:0], tx_byte};
        if (pong_shifter == 32'h504F4E47) begin // "PONG"
            pong_matched = 1'b1;
        end
    end

    // ------------------------------------------------------------------------
    // Main Verification Flow
    // ------------------------------------------------------------------------
    initial begin
        $display("================================================================");
        $display("  STARTING TESTBENCH: tb_uart_ping (Full SoC RISC-V Verification)");
        $display("================================================================");

        clk           = 0;
        rst_n         = 0;
        rdm6300_rx_i  = 1'b1;
        uart_rx_i     = 1'b1;
        ready_matched = 1'b0;
        pong_matched  = 1'b0;

        // Reset Pulse
        #200;
        rst_n = 1;
        $display("[TB] System Reset released. PicoRV32 booting from SPI Flash at 0x250000...");

        // Wait for CPU to boot and print boot banner
        wait(ready_matched == 1'b1);

        if (cpu_trap) begin
            $display("\n[TB ERROR] CPU entered TRAP state!");
            $finish;
        end

        #100000;
        $display("\n\n[TB] Boot banner detected! Sending 'P' (Ping) command from PC Host...");
        send_pc_byte("P");
        send_pc_byte(8'h0A); // '\n'

        // Wait for SoC to process command and output "PONG: PicoRV32 Active"
        wait(pong_matched == 1'b1);

        #250000;
        $display("\n\n================================================================");
        if (pong_matched && !cpu_trap) begin
            $display("  [SUCCESS] PING-PONG TEST PASSED! PicoRV32 responded with PONG.");
            $display("  cpu_trap = 0 (CPU healthy and executing normally)");
        end else begin
            $display("  [FAIL] Ping response not received or CPU trapped!");
            $display("  pong_matched = %b, cpu_trap = %b", pong_matched, cpu_trap);
        end
        $display("================================================================");
        $finish;
    end

    // Safety timeout
    initial begin
        #5000000; // 5ms timeout
        $display("\n[TB TIMEOUT] Simulation exceeded maximum time!");
        $finish;
    end

endmodule
