// ============================================================================
// File: firmware/common/hex_utils.c
// Project: rdm6300-picorv32-rom-data
// Description: Implementation of Hexadecimal Conversion & String Utilities
// ============================================================================

#include "hex_utils.h"

const char hex_chars[] = "0123456789ABCDEF";

int hex2val(char c) {
    if (c >= '0' && c <= '9') return c - '0';
    if (c >= 'A' && c <= 'F') return c - 'A' + 10;
    if (c >= 'a' && c <= 'f') return c - 'a' + 10;
    return -1;
}

char val2hex(uint8_t nibble) {
    return hex_chars[nibble & 0x0F];
}

bool hex_str_to_uid(const char *str10, uint32_t *out_hi, uint32_t *out_lo) {
    if (!str10) return false;

    int h0 = hex2val(str10[0]);
    int h1 = hex2val(str10[1]);
    if (h0 < 0 || h1 < 0) return false;

    uint32_t hi = (uint32_t)((h0 << 4) | h1);
    uint32_t lo = 0;

    for (int i = 2; i < 10; i++) {
        int v = hex2val(str10[i]);
        if (v < 0) return false;
        lo = (lo << 4) | (uint32_t)v;
    }

    if (out_hi) *out_hi = hi;
    if (out_lo) *out_lo = lo;
    return true;
}

void uid_to_hex_str(uint32_t hi, uint32_t lo, char *out_str11) {
    if (!out_str11) return;

    out_str11[0] = hex_chars[(hi >> 4) & 0x0F];
    out_str11[1] = hex_chars[hi & 0x0F];

    for (int i = 7; i >= 0; i--) {
        out_str11[2 + (7 - i)] = hex_chars[(lo >> (i * 4)) & 0x0F];
    }
    out_str11[10] = '\0';
}

void *soc_memcpy(void *dest, const void *src, unsigned int n) {
    char *d = (char *)dest;
    const char *s = (const char *)src;
    while (n--) *d++ = *s++;
    return dest;
}

void *soc_memset(void *s, int c, unsigned int n) {
    char *p = (char *)s;
    while (n--) *p++ = (char)c;
    return s;
}
