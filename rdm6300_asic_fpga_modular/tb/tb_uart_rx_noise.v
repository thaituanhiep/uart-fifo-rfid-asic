`timescale 1ns/1ps

module tb_uart_rx_noise;
    localparam CLKS_PER_BIT = 160;
    localparam SAMPLE_DIV = CLKS_PER_BIT / 16;

    reg clk = 1'b0;
    reg rst_n = 1'b0;
    reg rx = 1'b1;
    wire rx_dv;
    wire [7:0] rx_byte;
    wire framing_error;
    wire break_detect;
    integer byte_count = 0;
    integer frame_error_count = 0;
    reg [7:0] last_byte = 8'd0;

    always #5 clk = ~clk;

    uart_rx #(
        .CLKS_PER_BIT(CLKS_PER_BIT),
        .OVERSAMPLE(16),
        .BREAK_BITS(11),
        .BREAK_COUNT_W(16)
    ) dut (
        .clk(clk), .rst_n(rst_n), .rx(rx), .rx_dv(rx_dv),
        .rx_byte(rx_byte), .framing_error(framing_error),
        .break_detect(break_detect)
    );

    always @(negedge clk) begin
        if (rx_dv) begin
            byte_count = byte_count + 1;
            last_byte = rx_byte;
        end
        if (framing_error)
            frame_error_count = frame_error_count + 1;
    end

    task drive_bit;
        input value;
        input integer clocks;
        input inject_center_glitch;
        integer cycle_no;
        begin
            for (cycle_no = 0; cycle_no < clocks; cycle_no = cycle_no + 1) begin
                // Corrupt only the middle 16x sample. Samples on either side
                // remain correct, so majority voting must recover the bit.
                if (inject_center_glitch &&
                    (cycle_no >= (8*SAMPLE_DIV + 2)) &&
                    (cycle_no <  (9*SAMPLE_DIV + 2)))
                    rx = ~value;
                else
                    rx = value;
                @(posedge clk);
            end
        end
    endtask

    task send_byte;
        input [7:0] value;
        input integer clocks_per_tx_bit;
        input integer noisy_bit;
        input bad_stop;
        integer bit_no;
        begin
            drive_bit(1'b0, clocks_per_tx_bit, 1'b0);
            for (bit_no = 0; bit_no < 8; bit_no = bit_no + 1)
                drive_bit(value[bit_no], clocks_per_tx_bit, bit_no == noisy_bit);
            drive_bit(!bad_stop, clocks_per_tx_bit, 1'b0);
            rx = 1'b1;
            repeat (CLKS_PER_BIT/2) @(posedge clk);
        end
    endtask

    task require_byte;
        input integer expected_count;
        input [7:0] expected_byte;
        begin
            repeat (20) @(posedge clk);
            if (byte_count != expected_count || last_byte !== expected_byte)
                $fatal(1, "byte check failed: count=%0d data=%02x", byte_count, last_byte);
        end
    endtask

    initial begin
        repeat (5) @(posedge clk);
        rst_n = 1'b1;
        repeat (5) @(posedge clk);

        // 1. Clean nominal byte.
        send_byte(8'ha5, CLKS_PER_BIT, -1, 1'b0);
        require_byte(1, 8'ha5);

        // 2. One center sample of data bit 3 is inverted; 2-of-3 wins.
        send_byte(8'h3c, CLKS_PER_BIT, 3, 1'b0);
        require_byte(2, 8'h3c);

        // 3. Receiver tolerates a transmitter about 3.1 percent slower.
        send_byte(8'h96, 165, -1, 1'b0);
        require_byte(3, 8'h96);

        // 4. A short LOW pulse must not be accepted as a start bit.
        rx = 1'b0;
        repeat (CLKS_PER_BIT/4) @(posedge clk);
        rx = 1'b1;
        repeat (CLKS_PER_BIT*2) @(posedge clk);
        if (byte_count != 3) $fatal(1, "false start produced a byte");

        // 5. Invalid stop bit raises framing_error and suppresses rx_dv.
        send_byte(8'h55, CLKS_PER_BIT, -1, 1'b1);
        repeat (20) @(posedge clk);
        if (frame_error_count != 1 || byte_count != 3)
            $fatal(1, "bad stop was not rejected");

        // 6. Holding RX LOW for 11 bit periods raises break_detect.
        rx = 1'b0;
        repeat (CLKS_PER_BIT*12) @(posedge clk);
        if (!break_detect) $fatal(1, "UART break was not detected");
        rx = 1'b1;
        repeat (5) @(posedge clk);
        if (break_detect) $fatal(1, "break_detect did not clear on idle HIGH");

        // 7. Receiver recovers and accepts the next valid frame.
        repeat (CLKS_PER_BIT) @(posedge clk);
        send_byte(8'hc3, CLKS_PER_BIT, -1, 1'b0);
        require_byte(4, 8'hc3);

        $display("PASS: UART RX oversampling, noise, baud drift and error recovery");
        $finish;
    end
endmodule
