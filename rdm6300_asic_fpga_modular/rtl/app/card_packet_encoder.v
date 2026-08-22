`timescale 1ns/1ps

// Encodes one validated 40-bit RDM6300 tag as a fixed-length host packet:
// A5 5A 01 05 TAG[39:32] TAG[31:24] TAG[23:16] TAG[15:8] TAG[7:0] CRC8
// CRC-8 uses polynomial 0x07, initial value 0x00, over version, length and tag.
module card_packet_encoder (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        tag_valid,
    input  wire [39:0] tag_raw,
    input  wire        out_ready,
    output wire        out_valid,
    output reg  [7:0]  out_data,
    output wire        busy
);
    reg [39:0] tag_latched;
    reg [7:0]  crc_latched;
    reg [3:0]  byte_index;
    reg        active;

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

    function [7:0] crc8_tag;
        input [39:0] tag;
        reg [7:0] crc;
        begin
            crc = crc8_byte(8'h00, 8'h01);
            crc = crc8_byte(crc, 8'h05);
            crc = crc8_byte(crc, tag[39:32]);
            crc = crc8_byte(crc, tag[31:24]);
            crc = crc8_byte(crc, tag[23:16]);
            crc = crc8_byte(crc, tag[15:8]);
            crc = crc8_byte(crc, tag[7:0]);
            crc8_tag = crc;
        end
    endfunction

    always @* begin
        case (byte_index)
            4'd0: out_data = 8'hA5;
            4'd1: out_data = 8'h5A;
            4'd2: out_data = 8'h01;
            4'd3: out_data = 8'h05;
            4'd4: out_data = tag_latched[39:32];
            4'd5: out_data = tag_latched[31:24];
            4'd6: out_data = tag_latched[23:16];
            4'd7: out_data = tag_latched[15:8];
            4'd8: out_data = tag_latched[7:0];
            default: out_data = crc_latched;
        endcase
    end

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            tag_latched <= 40'd0;
            crc_latched <= 8'd0;
            byte_index  <= 4'd0;
            active      <= 1'b0;
        end else begin
            if (!active && tag_valid) begin
                tag_latched <= tag_raw;
                crc_latched <= crc8_tag(tag_raw);
                byte_index <= 4'd0;
                active <= 1'b1;
            end else if (active && out_ready) begin
                if (byte_index == 4'd9) begin
                    active <= 1'b0;
                    byte_index <= 4'd0;
                end else begin
                    byte_index <= byte_index + 1'b1;
                end
            end
        end
    end

    assign out_valid = active;
    assign busy = active;
endmodule
