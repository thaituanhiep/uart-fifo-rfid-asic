`timescale 1ns/1ps

module tb_top_basys3_rdm6300_burst;
    localparam CLKS_PER_BIT = 32;
    localparam FRAME_COUNT  = 64;

    reg clk = 1'b0;
    reg rdm6300_rx_i = 1'b1;

    wire uart_tx_o;
    wire rst_n;
    wire card_event;
    wire [39:0] tag_raw;
    wire checksum_error, frame_error, invalid_hex_error, frame_timeout_error;
    wire rx_fifo_full, tx_fifo_full, uart_framing_error, uart_break_detect;

    wire host_byte_valid;
    wire [7:0] host_byte;

    integer accepted_ids [0:FRAME_COUNT-1];
    integer accepted_count = 0;
    integer output_count = 0;
    integer output_id = 0;
    integer output_position = 0;
    reg [7:0] packet_crc = 8'h00;
    integer sent_count = 0;
    integer timeout_cycles = 0;
    integer decoded_count = 0;
    integer checksum_error_count = 0;
    integer frame_error_count = 0;
    integer i;

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

    uart_rx #(.CLKS_PER_BIT(CLKS_PER_BIT)) host_monitor (
        .clk(clk), .rst_n(rst_n), .rx(uart_tx_o),
        .rx_dv(host_byte_valid), .rx_byte(host_byte),
        .framing_error(), .break_detect()
    );

    function [7:0] hex_char;
        input [3:0] nibble;
        begin
            hex_char = (nibble < 10) ? (8'h30 + nibble) : (8'h41 + nibble - 10);
        end
    endfunction

    function [7:0] crc8_byte;
        input [7:0] crc_in;
        input [7:0] data;
        integer bit_index;
        reg [7:0] value;
        begin
            value = crc_in ^ data;
            for (bit_index = 0; bit_index < 8; bit_index = bit_index + 1)
                value = value[7] ? ((value << 1) ^ 8'h07) : (value << 1);
            crc8_byte = value;
        end
    endfunction

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

    task send_hex_byte;
        input [7:0] value;
        begin
            send_uart_byte(hex_char(value[7:4]));
            send_uart_byte(hex_char(value[3:0]));
        end
    endtask

    // Tag bytes are 01:02:03:04:index. The sixth byte is XOR checksum.
    task send_frame;
        input [7:0] index;
        begin
            send_uart_byte(8'h02);
            send_hex_byte(8'h01);
            send_hex_byte(8'h02);
            send_hex_byte(8'h03);
            send_hex_byte(8'h04);
            send_hex_byte(index);
            send_hex_byte(8'h04 ^ index);
            send_uart_byte(8'h03);
            // Model the reader's short idle gap between complete frames while
            // keeping the aggregate input rate above the formatted output rate.
            repeat (2 * CLKS_PER_BIT) @(negedge clk);
        end
    endtask

    // Every decoded card must reach the encoder immediately. At equal baud the
    // ten-byte output packet must finish before the next fourteen-byte input
    // frame completes, so encoder_busy here would indicate an invalid design
    // assumption or a regression in the direct decoder-to-encoder path.
    always @(posedge clk) begin
        if (dut.u_parser.decoded_valid)
            decoded_count = decoded_count + 1;
        if (checksum_error) checksum_error_count = checksum_error_count + 1;
        if (frame_error) frame_error_count = frame_error_count + 1;
        if (rst_n && dut.u_parser.decoded_valid && dut.u_parser.encoder_busy)
            $fatal(1, "decoder produced a card while packet encoder was busy");
        if (rst_n && card_event) begin
            accepted_ids[accepted_count] = tag_raw[31:0];
            accepted_count = accepted_count + 1;
        end
    end

    // Parse fixed ten-byte packets and compare their tag IDs with FIFO order.
    always @(negedge clk) begin
        if (host_byte_valid) begin
            if (output_position == 0 && host_byte != 8'hA5) $fatal(1, "bad SOF[0]");
            if (output_position == 1 && host_byte != 8'h5A) $fatal(1, "bad SOF[1]");
            if (output_position == 2 && host_byte != 8'h01) $fatal(1, "bad version");
            if (output_position == 3 && host_byte != 8'h05) $fatal(1, "bad length");
            if (output_position >= 2 && output_position <= 8)
                packet_crc = crc8_byte(packet_crc, host_byte);
            if (output_position >= 5 && output_position <= 8)
                output_id = (output_id << 8) | host_byte;

            if (output_position == 9) begin
                if (host_byte != packet_crc)
                    $fatal(1, "packet CRC mismatch: got %02x expected %02x",
                           host_byte, packet_crc);
                if (output_count >= accepted_count)
                    $fatal(1, "output packet has no decoded input event");
                if (output_id != accepted_ids[output_count])
                    $fatal(1, "event order mismatch: got %0d expected %0d",
                           output_id, accepted_ids[output_count]);
                output_count = output_count + 1;
                output_position = 0;
                output_id = 0;
                packet_crc = 8'h00;
            end else begin
                output_position = output_position + 1;
            end
        end
    end

    initial begin
        wait (rst_n);
        repeat (3) @(posedge clk);

        for (i = 1; i <= FRAME_COUNT; i = i + 1) begin
            send_frame(i[7:0]);
            sent_count = sent_count + 1;
        end

        while ((output_count < accepted_count || output_position != 0) &&
               timeout_cycles < 300000) begin
            @(posedge clk);
            timeout_cycles = timeout_cycles + 1;
        end

        if (output_count != accepted_count)
            $fatal(1, "drain timeout: accepted=%0d output=%0d",
                   accepted_count, output_count);
        $display("BURST STATS: sent=%0d decoded=%0d output=%0d checksum_err=%0d frame_err=%0d",
                 sent_count, decoded_count, output_count,
                 checksum_error_count, frame_error_count);
        if (decoded_count != sent_count || accepted_count != sent_count ||
            output_count != sent_count)
            $fatal(1, "direct decoder-to-encoder path dropped an event");
        if (checksum_error || frame_error || invalid_hex_error ||
            frame_timeout_error || rx_fifo_full || tx_fifo_full ||
            uart_framing_error || uart_break_detect)
            $fatal(1, "unexpected non-overflow error during valid burst");

        $display("PASS: direct burst decoded=%0d output=%0d",
                 decoded_count, output_count);
        $finish;
    end
endmodule
