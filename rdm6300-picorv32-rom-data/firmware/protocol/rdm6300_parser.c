// ============================================================================
// File: firmware/protocol/rdm6300_parser.c
// Project: rdm6300-picorv32-rom-data
// Description: Pure Algorithmic 14-Byte RDM6300 RFID Frame Decoder & Checksum Verifier
// ============================================================================

#include "rdm6300_parser.h"
#include "hex_utils.h"

// Parser State Variables
static char frame_buf[14];
static int  frame_idx     = 0;
static bool frame_in_sync = false;

void rdm6300_parser_init(void) {
    frame_idx     = 0;
    frame_in_sync = false;
}

bool rdm6300_parse_byte(uint8_t byte, rdm6300_tag_t *out_tag) {
    char c = (char)byte;

    // Detect Start of Text (STX: 0x02)
    if (c == 0x02) {
        frame_idx     = 0;
        frame_in_sync = true;
        return false;
    }

    if (!frame_in_sync) {
        return false;
    }

    // Detect End of Text (ETX: 0x03)
    if (c == 0x03) {
        bool result = false;

        // Check exact length: 10 UID hex digits + 2 Checksum hex digits = 12
        if (frame_idx == 12) {
            uint8_t xor_sum = 0;
            bool hex_valid = true;

            // Compute XOR checksum across 5 data bytes (10 ASCII hex chars)
            for (int i = 0; i < 5; i++) {
                int h1 = hex2val(frame_buf[i * 2]);
                int h2 = hex2val(frame_buf[i * 2 + 1]);
                if (h1 < 0 || h2 < 0) {
                    hex_valid = false;
                    break;
                }
                xor_sum ^= (uint8_t)((h1 << 4) | h2);
            }

            int c1 = hex2val(frame_buf[10]);
            int c2 = hex2val(frame_buf[11]);
            if (c1 < 0 || c2 < 0) hex_valid = false;
            uint8_t expected_cs = (uint8_t)((c1 << 4) | c2);

            // Validate Checksum Match
            if (hex_valid && xor_sum == expected_cs && out_tag) {
                out_tag->hi = (uint32_t)((hex2val(frame_buf[0]) << 4) | hex2val(frame_buf[1]));
                out_tag->lo = 0;
                for (int i = 2; i < 10; i++) {
                    out_tag->lo = (out_tag->lo << 4) | (uint32_t)hex2val(frame_buf[i]);
                }

                for (int i = 0; i < 10; i++) {
                    out_tag->tag_hex[i] = frame_buf[i];
                }
                out_tag->tag_hex[10] = '\0';

                result = true;
            }
        }

        // Reset for next frame
        frame_in_sync = false;
        frame_idx     = 0;
        return result;
    }

    // Accumulate payload characters
    if (frame_idx < 12) {
        frame_buf[frame_idx++] = c;
    } else {
        // Frame overflow without ETX -> discard and re-sync
        frame_in_sync = false;
        frame_idx     = 0;
    }

    return false;
}
