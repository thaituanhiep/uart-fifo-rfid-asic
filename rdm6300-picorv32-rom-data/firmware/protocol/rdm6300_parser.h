// ============================================================================
// File: firmware/protocol/rdm6300_parser.h
// Project: rdm6300-picorv32-rom-data
// Description: Pure Algorithmic 14-Byte RDM6300 RFID Frame Decoder & Checksum Verifier
// ============================================================================

#ifndef RDM6300_PARSER_H
#define RDM6300_PARSER_H

#include <stdint.h>
#include <stdbool.h>

// Parsed RFID Tag Data Structure
typedef struct {
    uint32_t hi;          // Top 8-bit version byte (tag UID [39:32])
    uint32_t lo;          // Lower 32-bit serial number (tag UID [31:0])
    char     tag_hex[11]; // 10-character ASCII hex string + null terminator
} rdm6300_tag_t;

// Reset parser state machine
void rdm6300_parser_init(void);

// Feed a single received byte into the RDM6300 frame parser.
// Frame format: [0x02 STX] [10 hex UID] [2 hex Checksum] [0x03 ETX]
// Returns true when a complete 14-byte frame is verified and valid.
// Upon returning true, *out_tag contains the decoded 40-bit UID and string.
bool rdm6300_parse_byte(uint8_t byte, rdm6300_tag_t *out_tag);

#endif // RDM6300_PARSER_H
