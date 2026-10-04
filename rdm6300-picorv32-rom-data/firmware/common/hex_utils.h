// ============================================================================
// File: firmware/common/hex_utils.h
// Project: rdm6300-picorv32-rom-data
// Description: Hexadecimal Conversion & String Utility Helpers
// ============================================================================

#ifndef HEX_UTILS_H
#define HEX_UTILS_H

#include <stdint.h>
#include <stdbool.h>

extern const char hex_chars[];

// Convert a single ASCII hex character ('0'-'9', 'A'-'F', 'a'-'f') to nibble (0-15).
// Returns -1 if invalid.
int hex2val(char c);

// Convert a nibble (0-15) to uppercase ASCII hex character.
char val2hex(uint8_t nibble);

// Convert 10-char ASCII hex string to 40-bit UID (hi 8-bit, lo 32-bit).
// Returns true on success, false if invalid characters or length.
bool hex_str_to_uid(const char *str10, uint32_t *out_hi, uint32_t *out_lo);

// Convert 40-bit UID (hi, lo) to 10-char ASCII hex string + null terminator.
void uid_to_hex_str(uint32_t hi, uint32_t lo, char *out_str11);

// Standard memory primitives for freestanding environment
void *soc_memcpy(void *dest, const void *src, unsigned int n);
void *soc_memset(void *s, int c, unsigned int n);

#endif // HEX_UTILS_H
