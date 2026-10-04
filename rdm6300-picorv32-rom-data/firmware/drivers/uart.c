// ============================================================================
// File: firmware/drivers/uart.c
// Project: rdm6300-picorv32-rom-data
// Description: Host PC UART Communication Driver Implementation
// ============================================================================

#include "uart.h"
#include "soc_regs.h"
#include "hex_utils.h"

void uart_init(uint32_t baud_div) {
    if (REG_PC_UART_DIV == 0 && baud_div != 0) {
        REG_PC_UART_DIV = baud_div;
    }
}

void uart_putc(char c) {
    REG_PC_UART_DAT = (uint32_t)(uint8_t)c;
}

void uart_puts(const char *str) {
    while (*str) {
        if (*str == '\n') uart_putc('\r');
        uart_putc(*str++);
    }
}

int uart_getc_nonblock(void) {
    uint32_t d = REG_PC_UART_DAT;
    if (d == 0xFFFFFFFF) return -1;
    return (int)(d & 0xFF);
}

char uart_getc_blocking(void) {
    int c;
    do {
        c = uart_getc_nonblock();
    } while (c < 0);
    return (char)c;
}

void uart_puthex32(uint32_t val) {
    for (int i = 7; i >= 0; i--) {
        uart_putc(hex_chars[(val >> (i * 4)) & 0xF]);
    }
}

void uart_putdec(uint32_t val) {
    if (val == 0) {
        uart_putc('0');
        return;
    }
    uint32_t divisor = 1000000000;
    bool started = false;
    while (divisor > 0) {
        int d = 0;
        while (val >= divisor) {
            val -= divisor;
            d++;
        }
        if (d > 0 || started || divisor == 1) {
            uart_putc((char)('0' + d));
            started = true;
        }
        if (divisor == 1000000000) divisor = 100000000;
        else if (divisor == 100000000) divisor = 10000000;
        else if (divisor == 10000000) divisor = 1000000;
        else if (divisor == 1000000) divisor = 100000;
        else if (divisor == 100000) divisor = 10000;
        else if (divisor == 10000) divisor = 1000;
        else if (divisor == 1000) divisor = 100;
        else if (divisor == 100) divisor = 10;
        else if (divisor == 10) divisor = 1;
        else divisor = 0;
    }
}

void uart_print_slot_tag(const char *prefix, int slot, const char *tag) {
    uart_puts(prefix);
    uart_puts(":");
    uart_putdec((uint32_t)slot);
    uart_puts(":");
    uart_puts(tag);
    uart_puts("\n");
}

bool uart_read_tag_uid(char *out_tag, uint32_t *out_hi, uint32_t *out_lo, int timeout_cycles) {
    int k = 0;
    while (k < 10 && timeout_cycles > 0) {
        int ch = uart_getc_nonblock();
        if (ch >= 0 && ch != '\r' && ch != '\n') {
            out_tag[k++] = (char)ch;
        }
        timeout_cycles--;
    }
    out_tag[k] = '\0';
    if (k == 10) {
        return hex_str_to_uid(out_tag, out_hi, out_lo);
    }
    return false;
}
