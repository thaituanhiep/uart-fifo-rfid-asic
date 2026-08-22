`timescale 1ns/1ps

module tb_rdm6300_frame_decoder;
    localparam TIMEOUT_CYCLES = 12;

    reg clk = 1'b0;
    reg rst_n = 1'b0;
    reg byte_valid = 1'b0;
    reg [7:0] byte_data = 8'd0;
    wire byte_ready;
    wire card_valid;
    wire [39:0] tag_raw;
    wire checksum_error;
    wire frame_error;
    wire invalid_hex_error;
    wire frame_timeout_error;

    integer valid_count = 0;
    integer checksum_count = 0;
    integer frame_count = 0;
    integer hex_count = 0;
    integer timeout_count = 0;

    always #5 clk = ~clk;

    rdm6300_frame_decoder #(
        .FRAME_TIMEOUT_CYCLES(TIMEOUT_CYCLES),
        .TIMEOUT_COUNTER_W(4)
    ) dut (
        .clk(clk), .rst_n(rst_n),
        .byte_valid(byte_valid), .byte_data(byte_data),
        .byte_ready(byte_ready),
        .card_valid(card_valid), .tag_raw(tag_raw),
        .checksum_error(checksum_error), .frame_error(frame_error),
        .invalid_hex_error(invalid_hex_error),
        .frame_timeout_error(frame_timeout_error)
    );

    always @(negedge clk) begin
        if (card_valid) valid_count = valid_count + 1;
        if (checksum_error) checksum_count = checksum_count + 1;
        if (frame_error) frame_count = frame_count + 1;
        if (invalid_hex_error) hex_count = hex_count + 1;
        if (frame_timeout_error) timeout_count = timeout_count + 1;
    end

    task send_byte;
        input [7:0] value;
        begin
            @(negedge clk);
            while (!byte_ready)
                @(negedge clk);
            byte_data = value;
            byte_valid = 1'b1;
            @(negedge clk);
            byte_valid = 1'b0;
        end
    endtask

    // Payload 01 02 03 04 05, checksum 01.
    task send_valid_frame;
        begin
            send_byte(8'h02);
            send_byte("0"); send_byte("1");
            send_byte("0"); send_byte("2");
            send_byte("0"); send_byte("3");
            send_byte("0"); send_byte("4");
            send_byte("0"); send_byte("5");
            send_byte("0"); send_byte("1");
            send_byte(8'h03);
        end
    endtask

    task check_last_card;
        begin
            if (tag_raw !== 40'h0102030405) $fatal(1, "tag_raw mismatch");
        end
    endtask

    initial begin
        repeat (3) @(negedge clk);
        rst_n = 1'b1;

        // 1. Garbage before STX is ignored; a valid frame is accepted.
        send_byte(8'h55);
        send_byte(8'haa);
        send_valid_frame();
        if (card_valid !== 1'b0)
            $fatal(1, "card_valid bypassed the ST_VALIDATE pipeline register");
        @(negedge clk);
        if (card_valid !== 1'b1)
            $fatal(1, "card_valid did not arrive one cycle after ETX decode");
        @(negedge clk);
        if (card_valid !== 1'b0)
            $fatal(1, "card_valid was not a one-cycle pulse");
        if (valid_count != 1) $fatal(1, "valid frame not accepted");
        check_last_card();

        // 2. Valid hex with the wrong checksum is classified separately.
        send_byte(8'h02);
        send_byte("0"); send_byte("1"); send_byte("0"); send_byte("2");
        send_byte("0"); send_byte("3"); send_byte("0"); send_byte("4");
        send_byte("0"); send_byte("5"); send_byte("0"); send_byte("0");
        send_byte(8'h03);
        repeat (2) @(negedge clk);
        if (checksum_count != 1 || valid_count != 1)
            $fatal(1, "checksum error classification failed");

        // 3. Invalid ASCII hex aborts immediately.
        send_byte(8'h02);
        send_byte("0");
        send_byte("G");
        repeat (2) @(negedge clk);
        if (hex_count != 1) $fatal(1, "invalid hex was not detected");

        // 4. ETX before all twelve digits is a structural frame error.
        send_byte(8'h02);
        send_byte("0"); send_byte("1");
        send_byte(8'h03);
        repeat (2) @(negedge clk);
        if (frame_count != 1) $fatal(1, "early ETX was not rejected");

        // 5. Missing bytes time out and return the decoder to WAIT_STX.
        send_byte(8'h02);
        send_byte("0");
        repeat (TIMEOUT_CYCLES + 2) @(negedge clk);
        if (timeout_count != 1) $fatal(1, "incomplete frame did not time out");

        // 6. A new STX abandons a damaged frame and immediately resynchronizes.
        send_byte(8'h02);
        send_byte("0"); send_byte("1"); send_byte("0");
        send_valid_frame(); // begins with the resynchronizing STX
        repeat (2) @(negedge clk);
        if (frame_count != 2 || valid_count != 2)
            $fatal(1, "STX resynchronization failed");
        check_last_card();

        // 7. Back-to-back valid frames are both accepted.
        send_valid_frame();
        send_valid_frame();
        repeat (2) @(negedge clk);
        if (valid_count != 4) $fatal(1, "back-to-back frames were lost");

        // 8. Reset in the middle of a frame, then recover on the next STX.
        send_byte(8'h02);
        send_byte("0"); send_byte("1");
        @(negedge clk); rst_n = 1'b0;
        repeat (2) @(negedge clk);
        rst_n = 1'b1;
        send_valid_frame();
        repeat (2) @(negedge clk);
        // Counters in the testbench are intentionally not reset with the DUT.
        if (valid_count != 5) $fatal(1, "decoder did not recover after reset");

        $display("PASS: decoder valid/error/timeout/resynchronization behavior");
        $finish;
    end
endmodule
