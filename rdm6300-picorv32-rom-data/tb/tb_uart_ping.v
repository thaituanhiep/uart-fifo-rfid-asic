`timescale 1ns / 1ps

module tb_uart_ping;
    reg clk;
    reg rst_n;
    reg rdm6300_rx_i;
    reg uart_rx_i;
    wire uart_tx_o;
    wire [15:0] leds_o;
    wire cpu_trap;

    always #5 clk = ~clk; // 100MHz

    // Use fast baud for simulation: DIV = 16 (160ns per bit)
    localparam DIV = 16;
    localparam BIT_PERIOD = DIV * 10;

    rdm6300_picorv32_soc #(
        .CLK_FREQ_HZ(100_000_000),
        .UART_BAUD(6_250_000), // DIV = 16
        .FLASH_BASE(24'h30_0000),
        .BOOT_HEX("firmware.hex")
    ) dut (
        .clk(clk),
        .rst_n(rst_n),
        .rdm6300_rx_i(rdm6300_rx_i),
        .uart_tx_o(uart_tx_o),
        .uart_rx_i(uart_rx_i),
        .flash_csn(),
        .flash_sck(),
        .flash_mosi(),
        .flash_miso(1'b1),
        .leds_o(leds_o),
        .cpu_trap(cpu_trap),
        .card_event_o(),
        .flash_busy_o(),
        .flash_done_o()
    );

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

    // Monitor characters sent by FPGA on uart_tx_o
    reg [7:0] tx_byte;
    integer bit_idx;
    always @(negedge uart_tx_o) begin
        // Start bit detected
        #(BIT_PERIOD + BIT_PERIOD/2);
        for (bit_idx = 0; bit_idx < 8; bit_idx = bit_idx + 1) begin
            tx_byte[bit_idx] = uart_tx_o;
            #BIT_PERIOD;
        end
        $write("%c", tx_byte);
    end

    initial begin
        clk = 0;
        rst_n = 0;
        rdm6300_rx_i = 1;
        uart_rx_i = 1;

        #200;
        rst_n = 1;
        $display("\n[TB] Reset released, waiting for CPU boot message...");

        // Wait for CPU boot message to finish
        #30000;

        $display("\n[TB] Sending 'P' (Ping) command from PC...");
        send_pc_byte("P");
        send_pc_byte(8'h0A); // '\n'

        #30000;
        $display("\n[TB] Simulation finished. cpu_trap = %b", cpu_trap);
        $finish;
    end
endmodule
