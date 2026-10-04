// ============================================================================
// File: firmware/drivers/uart.h
// Project: rdm6300-picorv32-rom-data
// Description: Host PC UART Communication Driver Header
// ============================================================================

#ifndef DRIVER_UART_H
#define DRIVER_UART_H

#include <stdint.h>
#include <stdbool.h>

void uart_init(uint32_t baud_div);
void uart_putc(char c);
void uart_puts(const char *str);
int  uart_getc_nonblock(void);
char uart_getc_blocking(void);
void uart_puthex32(uint32_t val);
void uart_putdec(uint32_t val);
void uart_print_slot_tag(const char *prefix, int slot, const char *tag);
bool uart_read_tag_uid(char *out_tag, uint32_t *out_hi, uint32_t *out_lo, int timeout_cycles);

#endif // DRIVER_UART_H
