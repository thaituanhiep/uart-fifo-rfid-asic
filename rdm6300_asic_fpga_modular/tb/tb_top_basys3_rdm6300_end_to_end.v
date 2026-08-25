`timescale 1ns/1ps

module tb_top_basys3_rdm6300_end_to_end;
    localparam CLKS_PER_BIT = 32;

    reg clk = 1'b0;
    reg rdm6300_rx_i = 1'b1;
    wire uart_tx_o;
    wire rst_n;
    wire card_event;
    wire [39:0] tag_raw;
    wire checksum_error;
    wire frame_error;
    wire invalid_hex_error;
    wire frame_timeout_error;
    wire rx_fifo_full;
    wire tx_fifo_full;
    wire uart_framing_error;
    wire uart_break_detect;

    wire host_byte_valid;
    wire [7:0] host_byte;
    reg [7:0] expected [0:9];
    integer received = 0;
    integer timeout_cycles = 0;

    always #5 clk = ~clk;

    top_basys3_rdm6300 #(
        .CLKS_PER_BIT(CLKS_PER_BIT),
        .FIFO_DEPTH(16),
        .FIFO_ADDR_W(4),
        .FRAME_TIMEOUT_CYCLES(1000),
        .FRAME_TIMEOUT_COUNTER_W(10)
    ) dut (
        .clk(clk),
        .rdm6300_rx_i(rdm6300_rx_i),
        .uart_tx_o(uart_tx_o)
    );

    assign rst_n               = dut.rst_n;
    assign card_event          = dut.card_event;
    assign tag_raw             = dut.tag_raw;
    assign checksum_error      = dut.checksum_error;
    assign frame_error         = dut.frame_error;
    assign invalid_hex_error   = dut.invalid_hex_error;
    assign frame_timeout_error = dut.frame_timeout_error;
    assign rx_fifo_full        = dut.rx_fifo_full;
    assign tx_fifo_full        = dut.tx_fifo_full;
    assign uart_framing_error  = dut.uart_framing_error;
    assign uart_break_detect   = dut.uart_break_detect;

    // Decode the core's physical UART output back into bytes for checking.
    uart_rx #(.CLKS_PER_BIT(CLKS_PER_BIT)) host_monitor (
        .clk(clk), .rst_n(rst_n), .rx(uart_tx_o),
        .rx_dv(host_byte_valid), .rx_byte(host_byte),
        .framing_error(), .break_detect()
    );

    task send_uart_byte;
        input [7:0] value;
        integer bit_no;
        begin
            @(negedge clk);
            rdm6300_rx_i = 1'b0;
            repeat (CLKS_PER_BIT) @(negedge clk);
            for (bit_no = 0; bit_no < 8; bit_no = bit_no + 1) begin
                rdm6300_rx_i = value[bit_no];
                repeat (CLKS_PER_BIT) @(negedge clk);
            end
            rdm6300_rx_i = 1'b1;
            repeat (CLKS_PER_BIT) @(negedge clk);
        end
    endtask

    always @(negedge clk) begin
        if (host_byte_valid) begin
            if (received >= 10)
                $fatal(1, "received unexpected extra UART byte %02x", host_byte);
            if (host_byte !== expected[received])
                $fatal(1, "UART byte %0d mismatch: got %02x expected %02x",
                       received, host_byte, expected[received]);
            received = received + 1;
        end
    end

    initial begin
        // Fixed packet for validated tag 01:02:03:04:05.
        expected[0]=8'hA5; expected[1]=8'h5A; expected[2]=8'h01;
        expected[3]=8'h05; expected[4]=8'h01; expected[5]=8'h02;
        expected[6]=8'h03; expected[7]=8'h04; expected[8]=8'h05;
        expected[9]=8'hEE;

        wait (rst_n);
        repeat (3) @(posedge clk);

        send_uart_byte(8'h02);
        send_uart_byte("0"); send_uart_byte("1");
        send_uart_byte("0"); send_uart_byte("2");
        send_uart_byte("0"); send_uart_byte("3");
        send_uart_byte("0"); send_uart_byte("4");
        send_uart_byte("0"); send_uart_byte("5");
        send_uart_byte("0"); send_uart_byte("1");
        send_uart_byte(8'h03);

        while ((received < 10) && (timeout_cycles < 30000)) begin
            @(posedge clk);
            timeout_cycles = timeout_cycles + 1;
        end

        if (received != 10) $fatal(1, "end-to-end timeout after %0d output bytes", received);
        if (checksum_error || frame_error || invalid_hex_error ||
            frame_timeout_error || rx_fifo_full || tx_fifo_full)
            $fatal(1, "unexpected error flag in end-to-end path");

        $display("PASS: flattened Basys3 top UART-in to UART-out path");
        $finish;
    end
endmodule
