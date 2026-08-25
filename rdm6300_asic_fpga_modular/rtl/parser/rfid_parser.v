`timescale 1ns/1ps

// Minimal hardware pipeline: validate one RDM6300 frame/checksum and emit its
// raw 40-bit tag as a CRC-protected binary packet. At equal UART baud rates the
// ten-byte output packet drains before the next fourteen-byte input frame can
// complete, so no intermediate card-event FIFO is required.
module rfid_parser #(
    parameter FRAME_TIMEOUT_CYCLES    = 500_000,
    parameter FRAME_TIMEOUT_COUNTER_W = 19
) (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        rx_byte_valid,
    input  wire [7:0]  rx_byte_data,
    output wire        rx_byte_ready,
    output wire        tx_byte_valid,
    output wire [7:0]  tx_byte_data,
    input  wire        tx_byte_ready,
    output wire        card_event,
    output wire [39:0] tag_raw,
    output wire        checksum_error,
    output wire        frame_error,
    output wire        invalid_hex_error,
    output wire        frame_timeout_error
);
    wire decoded_valid;
    wire [39:0] decoded_tag;
    wire encoder_busy;
    wire decoder_ready;

    rdm6300_frame_decoder #(
        .FRAME_TIMEOUT_CYCLES(FRAME_TIMEOUT_CYCLES),
        .TIMEOUT_COUNTER_W(FRAME_TIMEOUT_COUNTER_W)
    ) u_decoder (
        .clk(clk), .rst_n(rst_n),
        .byte_valid(rx_byte_valid), .byte_data(rx_byte_data),
        .byte_ready(decoder_ready),
        .card_valid(decoded_valid), .tag_raw(decoded_tag),
        .checksum_error(checksum_error), .frame_error(frame_error),
        .invalid_hex_error(invalid_hex_error),
        .frame_timeout_error(frame_timeout_error)
    );

    card_packet_encoder u_packet_encoder (
        .clk(clk), .rst_n(rst_n),
        .tag_valid(decoded_valid), .tag_raw(decoded_tag),
        .out_ready(tx_byte_ready),
        .out_valid(tx_byte_valid), .out_data(tx_byte_data),
        .busy(encoder_busy)
    );

    assign card_event = decoded_valid;
    assign tag_raw = decoded_tag;
    assign rx_byte_ready = decoder_ready;
endmodule
