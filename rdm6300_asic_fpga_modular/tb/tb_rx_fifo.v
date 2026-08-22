`timescale 1ns/1ps

module tb_rx_fifo;
    reg clk = 1'b0;
    reg rst_n = 1'b0;
    reg in_valid = 1'b0;
    reg [7:0] in_data = 8'd0;
    wire in_ready;
    wire out_valid;
    wire [7:0] out_data;
    reg out_ready = 1'b0;
    wire full;
    wire empty;
    wire [2:0] level;
    wire overflow_pulse;
    wire underflow_pulse;

    always #5 clk = ~clk;

    rx_fifo #(.DATA_W(8), .DEPTH(4), .ADDR_W(2)) dut (
        .clk(clk), .rst_n(rst_n),
        .in_valid(in_valid), .in_data(in_data), .in_ready(in_ready),
        .out_valid(out_valid), .out_data(out_data), .out_ready(out_ready),
        .full(full), .empty(empty),
        .level(level), .overflow_pulse(overflow_pulse),
        .underflow_pulse(underflow_pulse)
    );

    task write_byte;
        input [7:0] value;
        begin
            @(negedge clk);
            if (!in_ready) $fatal(1, "RX FIFO was not ready for input");
            in_data = value; in_valid = 1'b1;
            @(negedge clk); in_valid = 1'b0;
        end
    endtask

    task read_check;
        input [7:0] expected;
        begin
            @(negedge clk);
            if (!out_valid || out_data !== expected)
                $fatal(1, "RX FIFO order mismatch: got %02x expected %02x", out_data, expected);
            out_ready = 1'b1;
            @(negedge clk); out_ready = 1'b0;
        end
    endtask

    initial begin
        repeat (3) @(negedge clk);
        rst_n = 1'b1;

        @(negedge clk); out_ready = 1'b1;
        @(negedge clk);
        if (!underflow_pulse || !empty) $fatal(1, "RX FIFO underflow was not reported");
        out_ready = 1'b0;

        write_byte(8'h11); write_byte(8'h22);
        write_byte(8'h33); write_byte(8'h44);
        if (!full || level != 4) $fatal(1, "RX FIFO did not become full");
        @(negedge clk); in_data = 8'h55; in_valid = 1'b1;
        if (in_ready) $fatal(1, "RX FIFO accepted input while full");
        @(negedge clk);
        if (!overflow_pulse || level != 4) $fatal(1, "RX FIFO overflow was not reported");
        in_valid = 1'b0;

        read_check(8'h11); read_check(8'h22);
        read_check(8'h33); read_check(8'h44);
        if (!empty || level != 0) $fatal(1, "RX FIFO did not drain to empty");

        write_byte(8'ha1); write_byte(8'ha2);
        @(negedge clk);
        if (!out_valid || out_data !== 8'ha1) $fatal(1, "RX FIFO head was not visible");
        in_data = 8'ha3; in_valid = 1'b1; out_ready = 1'b1;
        @(negedge clk);
        if (level != 2 || !out_valid || out_data !== 8'ha2)
            $fatal(1, "RX FIFO simultaneous read/write failed");
        in_valid = 1'b0; out_ready = 1'b0;
        read_check(8'ha2); read_check(8'ha3);

        $display("PASS: rx_fifo ready/valid/order/full/empty/wrap/error pulses");
        $finish;
    end
endmodule
