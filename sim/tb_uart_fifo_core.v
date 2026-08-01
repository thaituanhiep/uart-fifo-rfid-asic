`timescale 1ns/1ps

module tb_uart_fifo_core;

    localparam CLKS_PER_BIT = 8;

    reg clk;
    reg rst_n;

    wire uart_line;

    reg tx_wr_en;
    reg [7:0] tx_wr_data;
    wire tx_full;
    wire tx_empty;

    reg rx_rd_en;
    wire [7:0] rx_rd_data;
    wire rx_empty;
    wire rx_full;

    reg [7:0] expected [0:2];
    integer idx;

    uart_fifo_core #(
        .CLKS_PER_BIT(CLKS_PER_BIT),
        .FIFO_DEPTH(16),
        .FIFO_ADDR_W(4)
    ) dut (
        .clk(clk),
        .rst_n(rst_n),
        .uart_rx_i(uart_line),
        .uart_tx_o(uart_line),
        .tx_wr_en(tx_wr_en),
        .tx_wr_data(tx_wr_data),
        .tx_full(tx_full),
        .tx_empty(tx_empty),
        .rx_rd_en(rx_rd_en),
        .rx_rd_data(rx_rd_data),
        .rx_empty(rx_empty),
        .rx_full(rx_full)
    );

    always #5 clk = ~clk;

    task push_tx;
        input [7:0] data;
        begin
            @(posedge clk);
            tx_wr_en <= 1'b1;
            tx_wr_data <= data;
            @(posedge clk);
            tx_wr_en <= 1'b0;
            tx_wr_data <= 8'd0;
        end
    endtask

    task pop_rx_and_check;
        input [7:0] exp;
        reg [7:0] sampled;
        begin
            while (rx_empty) @(posedge clk);
            @(posedge clk);
            rx_rd_en <= 1'b1;
            @(posedge clk);
            rx_rd_en <= 1'b0;
            @(posedge clk);
            sampled = rx_rd_data;

            if (sampled !== exp) begin
                $display("ERROR: expected %02x, got %02x at t=%0t", exp, sampled, $time);
                $fatal(1);
            end else begin
                $display("PASS: received %02x at t=%0t", sampled, $time);
            end
        end
    endtask

    initial begin
        clk = 1'b0;
        rst_n = 1'b0;
        tx_wr_en = 1'b0;
        tx_wr_data = 8'd0;
        rx_rd_en = 1'b0;

        expected[0] = 8'h55;
        expected[1] = 8'hA3;
        expected[2] = 8'h0F;

        repeat (10) @(posedge clk);
        rst_n = 1'b1;

        for (idx = 0; idx < 3; idx = idx + 1)
            push_tx(expected[idx]);

        for (idx = 0; idx < 3; idx = idx + 1)
            pop_rx_and_check(expected[idx]);

        repeat (20) @(posedge clk);
        $display("Simulation done");
        $finish;
    end

endmodule
