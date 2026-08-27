`timescale 1ns/1ps

// Basys3 system top: input synchronization plus the complete ready/valid
// UART RX -> RX FIFO -> Parser -> TX FIFO -> UART TX pipeline.
module top_basys3_rdm6300 #(
    parameter CLKS_PER_BIT = 10417,
    parameter FIFO_DEPTH   = 16,
    parameter FIFO_ADDR_W  = 4,
    parameter FRAME_TIMEOUT_CYCLES      = 500_000,
    parameter FRAME_TIMEOUT_COUNTER_W   = 19
) (
    input  wire clk,
    input  wire rdm6300_rx_i,
    output wire uart_tx_o
);
    // FPGA-only power-up reset; no Basys3 button enters the datapath.
    reg [3:0] startup_reset = 4'b0000;
    wire rst_n = startup_reset[3];
    wire rdm_rx_sync;

    wire       uart_rx_valid;
    wire [7:0] uart_rx_data;

    wire       rx_fifo_in_valid;
    wire [7:0] rx_fifo_in_data;
    wire       rx_fifo_in_ready;
    wire       rx_fifo_out_valid;
    wire [7:0] rx_fifo_out_data;
    wire       rx_fifo_out_ready;

    wire       parser_rx_valid;
    wire [7:0] parser_rx_data;
    wire       parser_rx_ready;
    wire       parser_tx_valid;
    wire [7:0] parser_tx_data;
    wire       parser_tx_ready;

    wire       tx_fifo_in_valid;
    wire [7:0] tx_fifo_in_data;
    wire       tx_fifo_in_ready;
    wire       tx_fifo_out_valid;
    wire [7:0] tx_fifo_out_data;
    wire       tx_fifo_out_ready;

    wire       uart_tx_valid;
    wire [7:0] uart_tx_data;
    wire       uart_tx_ready;
    reg        parser_in_valid_r;
    reg [7:0]  parser_in_data_r;

    // Internal status remains visible to simulation/debug hierarchy without
    // adding board pins to the minimal Basys3 interface.
    wire        card_event;
    wire [39:0] tag_raw;
    wire        checksum_error;
    wire        frame_error;
    wire        invalid_hex_error;
    wire        frame_timeout_error;
    wire        rx_fifo_full;
    wire        tx_fifo_full;
    wire        uart_framing_error;
    wire        uart_break_detect;
    wire        rx_fifo_overflow;
    wire        tx_fifo_overflow;

    always @(posedge clk)
        startup_reset <= {startup_reset[2:0], 1'b1};

    sync_2ff #(.RESET_VALUE(1'b1)) u_rx_sync (
        .clk(clk), .rst_n(rst_n),
        .async_i(rdm6300_rx_i), .sync_o(rdm_rx_sync)
    );

    uart_rx #(
        .CLKS_PER_BIT(CLKS_PER_BIT)
    ) u_uart_rx (
        .clk(clk),
        .rst_n(rst_n),
        .rx(rdm_rx_sync),
        .rx_dv(uart_rx_valid),
        .rx_byte(uart_rx_data),
        .framing_error(uart_framing_error),
        .break_detect(uart_break_detect)
    );

    // UART RX -> RX FIFO
    assign rx_fifo_in_valid = uart_rx_valid;
    assign rx_fifo_in_data  = uart_rx_data;

    rx_fifo #(
        .DATA_W(8),
        .DEPTH(FIFO_DEPTH),
        .ADDR_W(FIFO_ADDR_W)
    ) u_rx_fifo (
        .clk(clk),
        .rst_n(rst_n),
        .in_valid(rx_fifo_in_valid),
        .in_data(rx_fifo_in_data),
        .in_ready(rx_fifo_in_ready),
        .out_valid(rx_fifo_out_valid),
        .out_data(rx_fifo_out_data),
        .out_ready(rx_fifo_out_ready),
        .full(rx_fifo_full),
        .empty(),
        .level(),
        .overflow_pulse(rx_fifo_overflow),
        .underflow_pulse()
    );

    // RX FIFO -> Parser
    // One-byte elastic stage to break long combinational path from FIFO read
    // logic into parser decode logic on FPGA.
    assign rx_fifo_out_ready = !parser_in_valid_r || parser_rx_ready;
    assign parser_rx_valid   = parser_in_valid_r;
    assign parser_rx_data    = parser_in_data_r;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            parser_in_valid_r <= 1'b0;
            parser_in_data_r  <= 8'h00;
        end else begin
            if (rx_fifo_out_valid && rx_fifo_out_ready) begin
                parser_in_valid_r <= 1'b1;
                parser_in_data_r  <= rx_fifo_out_data;
            end else if (parser_rx_ready && parser_in_valid_r) begin
                parser_in_valid_r <= 1'b0;
            end
        end
    end

    rfid_parser #(
        .FRAME_TIMEOUT_CYCLES(FRAME_TIMEOUT_CYCLES),
        .FRAME_TIMEOUT_COUNTER_W(FRAME_TIMEOUT_COUNTER_W)
    ) u_parser (
        .clk(clk),
        .rst_n(rst_n),
        .rx_byte_valid(parser_rx_valid),
        .rx_byte_data(parser_rx_data),
        .rx_byte_ready(parser_rx_ready),
        .tx_byte_valid(parser_tx_valid),
        .tx_byte_data(parser_tx_data),
        .tx_byte_ready(parser_tx_ready),
        .card_event(card_event),
        .tag_raw(tag_raw),
        .checksum_error(checksum_error),
        .frame_error(frame_error),
        .invalid_hex_error(invalid_hex_error),
        .frame_timeout_error(frame_timeout_error)
    );

    // Parser -> TX FIFO
    assign tx_fifo_in_valid = parser_tx_valid;
    assign tx_fifo_in_data  = parser_tx_data;
    assign parser_tx_ready  = tx_fifo_in_ready;

    tx_fifo #(
        .DATA_W(8),
        .DEPTH(FIFO_DEPTH),
        .ADDR_W(FIFO_ADDR_W)
    ) u_tx_fifo (
        .clk(clk),
        .rst_n(rst_n),
        .in_valid(tx_fifo_in_valid),
        .in_data(tx_fifo_in_data),
        .in_ready(tx_fifo_in_ready),
        .out_valid(tx_fifo_out_valid),
        .out_data(tx_fifo_out_data),
        .out_ready(tx_fifo_out_ready),
        .full(tx_fifo_full),
        .empty(),
        .level(),
        .overflow_pulse(tx_fifo_overflow),
        .underflow_pulse()
    );

    // TX FIFO -> UART TX
    assign uart_tx_valid     = tx_fifo_out_valid;
    assign uart_tx_data      = tx_fifo_out_data;
    assign tx_fifo_out_ready = uart_tx_ready;

    uart_tx #(
        .CLKS_PER_BIT(CLKS_PER_BIT)
    ) u_uart_tx (
        .clk(clk),
        .rst_n(rst_n),
        .in_valid(uart_tx_valid),
        .in_data(uart_tx_data),
        .in_ready(uart_tx_ready),
        .tx(uart_tx_o),
        .tx_active(),
        .tx_done()
    );
endmodule
