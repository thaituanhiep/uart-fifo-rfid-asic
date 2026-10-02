`timescale 1ns/1ps

// RDM6300 frame format:
// STX + 10 ASCII hex payload digits + 2 ASCII hex checksum digits + ETX
// Payload bytes: version, ID[31:24], ID[23:16], ID[15:8], ID[7:0]
module rdm6300_frame_decoder #(
    // Inter-byte timeout while a frame is being collected.
    // 500_000 clocks is 5 ms at 100 MHz.
    parameter FRAME_TIMEOUT_CYCLES = 500_000,
    parameter TIMEOUT_COUNTER_W    = 19
) (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        byte_valid,
    input  wire [7:0]  byte_data,
    output wire        byte_ready,

    output reg         card_valid,
    output reg [39:0]  tag_raw,
    output reg         checksum_error,
    output reg         frame_error,
    output reg         invalid_hex_error,
    output reg         frame_timeout_error
);
    localparam ST_WAIT_STX = 2'd0;
    localparam ST_COLLECT  = 2'd1;
    localparam ST_VALIDATE = 2'd2;

    reg [1:0] state;
    reg [3:0] index;
    reg [TIMEOUT_COUNTER_W-1:0] timeout_count;
    reg [7:0] ascii_buf [0:11];
    integer i;

    reg [4:0] nibble [0:11];
    reg [7:0] payload_b0, payload_b1, payload_b2, payload_b3, payload_b4;
    reg [7:0] checksum_calc, checksum_rx;
    reg [39:0] decoded_payload;
    reg [7:0]  decoded_checksum_calc;
    reg [7:0]  decoded_checksum_rx;

    // Validation consumes one internal cycle; upstream holds its byte while
    // ready is low, so no input is silently discarded.
    assign byte_ready = (state != ST_VALIDATE);

    function [4:0] ascii_hex_to_nibble;
        input [7:0] ch;
        begin
            if ((ch >= 8'h30) && (ch <= 8'h39))
                ascii_hex_to_nibble = {1'b0, ch - 8'h30};
            else if ((ch >= 8'h41) && (ch <= 8'h46))
                ascii_hex_to_nibble = {1'b0, ch - 8'h41 + 8'd10};
            else if ((ch >= 8'h61) && (ch <= 8'h66))
                ascii_hex_to_nibble = {1'b0, ch - 8'h61 + 8'd10};
            else
                ascii_hex_to_nibble = 5'h10;
        end
    endfunction

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state          <= ST_WAIT_STX;
            index          <= 4'd0;
            card_valid     <= 1'b0;
            tag_raw        <= 40'd0;
            checksum_error <= 1'b0;
            frame_error    <= 1'b0;
            invalid_hex_error    <= 1'b0;
            frame_timeout_error  <= 1'b0;
            timeout_count        <= {TIMEOUT_COUNTER_W{1'b0}};
            decoded_payload       <= 40'd0;
            decoded_checksum_calc <= 8'd0;
            decoded_checksum_rx   <= 8'd0;
            for (i = 0; i < 12; i = i + 1)
                ascii_buf[i] <= 8'd0;
        end else begin
            card_valid     <= 1'b0;
            checksum_error <= 1'b0;
            frame_error    <= 1'b0;
            invalid_hex_error   <= 1'b0;
            frame_timeout_error <= 1'b0;

            // This state is a real sequential boundary. The ASCII-to-payload
            // cone terminates at decoded_payload/checksum registers; checksum
            // validation and the externally visible outputs happen one cycle
            // later from those registered values.
            if (state == ST_VALIDATE) begin
                if (decoded_checksum_calc != decoded_checksum_rx) begin
                    checksum_error <= 1'b1;
                end else begin
                    tag_raw   <= decoded_payload;
                    card_valid <= 1'b1;
                end
                state <= ST_WAIT_STX;
                timeout_count <= {TIMEOUT_COUNTER_W{1'b0}};
            end else if (byte_valid) begin
                case (state)
                    ST_WAIT_STX: begin
                        if (byte_data == 8'h02) begin
                            index <= 4'd0;
                            timeout_count <= {TIMEOUT_COUNTER_W{1'b0}};
                            state <= ST_COLLECT;
                        end
                    end

                    ST_COLLECT: begin
                        timeout_count <= {TIMEOUT_COUNTER_W{1'b0}};

                        // A new STX is always a reliable resynchronization point.
                        if (byte_data == 8'h02) begin
                            frame_error <= 1'b1;
                            index <= 4'd0;
                        end else if (byte_data == 8'h03) begin
                            if (index != 4'd12) begin
                                // ETX arrived before all payload/checksum digits.
                                frame_error <= 1'b1;
                                state <= ST_WAIT_STX;
                            end else begin
                                for (i = 0; i < 12; i = i + 1)
                                    nibble[i] = ascii_hex_to_nibble(ascii_buf[i]);

                                payload_b0 = {nibble[0][3:0], nibble[1][3:0]};
                                payload_b1 = {nibble[2][3:0], nibble[3][3:0]};
                                payload_b2 = {nibble[4][3:0], nibble[5][3:0]};
                                payload_b3 = {nibble[6][3:0], nibble[7][3:0]};
                                payload_b4 = {nibble[8][3:0], nibble[9][3:0]};
                                checksum_rx = {nibble[10][3:0], nibble[11][3:0]};
                                checksum_calc = payload_b0 ^ payload_b1 ^ payload_b2 ^ payload_b3 ^ payload_b4;

                                decoded_payload <= {
                                    payload_b0, payload_b1, payload_b2,
                                    payload_b3, payload_b4
                                };
                                decoded_checksum_calc <= checksum_calc;
                                decoded_checksum_rx <= checksum_rx;
                                state <= ST_VALIDATE;
                            end
                            index <= 4'd0;
                        end else if (index >= 4'd12) begin
                            // Exactly ETX is allowed after twelve hex digits.
                            frame_error <= 1'b1;
                            state <= ST_WAIT_STX;
                            index <= 4'd0;
                        end else if (ascii_hex_to_nibble(byte_data) >= 5'd16) begin
                            invalid_hex_error <= 1'b1;
                            state <= ST_WAIT_STX;
                            index <= 4'd0;
                        end else begin
                            ascii_buf[index] <= byte_data;
                            index <= index + 1'b1;
                        end
                    end

                    default: begin
                        state <= ST_WAIT_STX;
                        index <= 4'd0;
                        timeout_count <= {TIMEOUT_COUNTER_W{1'b0}};
                    end
                endcase
            end else if (state == ST_COLLECT) begin
                if (timeout_count >= FRAME_TIMEOUT_CYCLES - 1) begin
                    frame_timeout_error <= 1'b1;
                    state <= ST_WAIT_STX;
                    index <= 4'd0;
                    timeout_count <= {TIMEOUT_COUNTER_W{1'b0}};
                end else begin
                    timeout_count <= timeout_count + 1'b1;
                end
            end else begin
                timeout_count <= {TIMEOUT_COUNTER_W{1'b0}};
            end
        end
    end
endmodule
