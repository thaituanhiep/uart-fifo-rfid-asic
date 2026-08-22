`timescale 1ns/1ps

module tb_card_packet_encoder;
    reg clk = 1'b0;
    reg rst_n = 1'b0;
    reg tag_valid = 1'b0;
    reg [39:0] tag_raw = 40'd0;
    reg out_ready = 1'b0;
    wire out_valid;
    wire [7:0] out_data;
    wire busy;

    reg [7:0] expected [0:9];
    integer byte_index;

    always #5 clk = ~clk;

    card_packet_encoder dut (
        .clk(clk), .rst_n(rst_n),
        .tag_valid(tag_valid), .tag_raw(tag_raw),
        .out_ready(out_ready), .out_valid(out_valid),
        .out_data(out_data), .busy(busy)
    );

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

    task load_expected;
        input [39:0] tag;
        reg [7:0] crc;
        begin
            expected[0] = 8'hA5;
            expected[1] = 8'h5A;
            expected[2] = 8'h01;
            expected[3] = 8'h05;
            expected[4] = tag[39:32];
            expected[5] = tag[31:24];
            expected[6] = tag[23:16];
            expected[7] = tag[15:8];
            expected[8] = tag[7:0];
            crc = crc8_byte(8'h00, 8'h01);
            crc = crc8_byte(crc, 8'h05);
            crc = crc8_byte(crc, tag[39:32]);
            crc = crc8_byte(crc, tag[31:24]);
            crc = crc8_byte(crc, tag[23:16]);
            crc = crc8_byte(crc, tag[15:8]);
            expected[9] = crc8_byte(crc, tag[7:0]);
        end
    endtask

    task start_tag;
        input [39:0] tag;
        begin
            @(negedge clk);
            tag_raw = tag;
            tag_valid = 1'b1;
            @(negedge clk);
            tag_valid = 1'b0;
        end
    endtask

    task consume_and_check_packet;
        input [39:0] tag;
        begin
            load_expected(tag);
            if (!out_valid || !busy) $fatal(1, "encoder did not start");

            // Backpressure must not change the current byte or drop valid.
            out_ready = 1'b0;
            repeat (3) begin
                if (!out_valid || out_data !== expected[0])
                    $fatal(1, "output changed while stalled");
                @(negedge clk);
            end

            for (byte_index = 0; byte_index < 10; byte_index = byte_index + 1) begin
                if (!out_valid || !busy)
                    $fatal(1, "packet ended before byte %0d", byte_index);
                if (out_data !== expected[byte_index])
                    $fatal(1, "byte %0d mismatch: got %02x expected %02x",
                           byte_index, out_data, expected[byte_index]);
                out_ready = 1'b1;
                @(negedge clk);
            end
            out_ready = 1'b0;
            if (out_valid || busy) $fatal(1, "encoder remained busy after packet");
        end
    endtask

    initial begin
        repeat (3) @(negedge clk);
        rst_n = 1'b1;

        // Known end-to-end vector; its CRC byte must be EE.
        load_expected(40'h0102030405);
        if (expected[9] !== 8'hEE) $fatal(1, "CRC reference calculation failed");
        start_tag(40'h0102030405);

        // Changing the input after acceptance must not alter the active packet.
        tag_raw = 40'hFFEEDDCCBB;
        consume_and_check_packet(40'h0102030405);

        // A second nontrivial vector proves the encoder returns cleanly to idle.
        start_tag(40'hA1B2C3D4E5);
        consume_and_check_packet(40'hA1B2C3D4E5);

        $display("PASS: packet encoder framing/CRC/backpressure/tag-latching behavior");
        $finish;
    end
endmodule
