// ============================================================================
// File: firmware/app/access_control.c
// Project: rdm6300-picorv32-rom-data
// Description: RFID Access Control Business Logic & Authorization Engine
// ============================================================================

#include "access_control.h"
#include "rdm6300_parser.h"
#include "flash.h"
#include "uart.h"
#include "soc_regs.h"

// State Variables
static char     last_tag_hex[11] = "0000000000";
static uint32_t tag_word_hi      = 0;
static uint32_t tag_word_lo      = 0;
static bool     tag_available    = false;

static uint32_t last_scanned_hi  = 0xFFFFFFFF;
static uint32_t last_scanned_lo  = 0xFFFFFFFF;
static uint32_t rdm_cooldown_cnt = 0;

static inline int rfid_uart_getc_nonblock(void) {
    uint32_t d = REG_RFID_UART_DAT;
    if (d == 0xFFFFFFFF) return -1;
    return (int)(d & 0xFF);
}

void access_control_init(void) {
    if (REG_RFID_UART_DIV == 0) {
        REG_RFID_UART_DIV = 5208; // 50 MHz / 9600 Baud
    }
    tag_available     = false;
    rdm_cooldown_cnt  = 0;
    last_scanned_hi   = 0xFFFFFFFF;
    last_scanned_lo   = 0xFFFFFFFF;
    rdm6300_parser_init();
}

bool access_control_is_tag_available(void) {
    return tag_available;
}

void access_control_get_last_tag(char *out_hex10, uint32_t *out_hi, uint32_t *out_lo) {
    if (out_hex10) {
        for (int i = 0; i <= 10; i++) out_hex10[i] = last_tag_hex[i];
    }
    if (out_hi) *out_hi = tag_word_hi;
    if (out_lo) *out_lo = tag_word_lo;
}

void access_control_set_current_tag(const char *tag_hex, uint32_t hi, uint32_t lo) {
    for (int i = 0; i < 10 && tag_hex[i] != '\0'; i++) {
        last_tag_hex[i] = tag_hex[i];
    }
    last_tag_hex[10] = '\0';
    tag_word_hi   = hi;
    tag_word_lo   = lo;
    tag_available = true;
}

void access_control_process_card(const char *tag_hex, uint32_t hi, uint32_t lo) {
    // 1. Check authorization in Flash whitelist (Sector 48)
    int tag_slot = flash_find_tag(hi, lo);
    bool is_granted = (tag_slot >= 0);

    // 2. Append access audit event to Flash log (Sector 49)
    int log_slot = flash_append_log(is_granted, hi, lo);

    // 3. Actuate hardware indicators & send real-time report over UART
    if (is_granted) {
        REG_GPIO_LEDS = (REG_GPIO_LEDS & ~0x0002) | 0x0004; // Green LED on
        uart_puts("ACCESS:GRANTED:SLOT:");
        uart_putdec((uint32_t)tag_slot);
        uart_puts(":");
        uart_puts(tag_hex);
        uart_puts(":LOG:");
        uart_putdec((uint32_t)(log_slot >= 0 ? log_slot : 0));
        uart_puts("\n");
    } else {
        REG_GPIO_LEDS = (REG_GPIO_LEDS & ~0x0004) | 0x0002; // Red warning LED on
        uart_puts("ACCESS:DENIED:");
        uart_puts(tag_hex);
        uart_puts(":LOG:");
        uart_putdec((uint32_t)(log_slot >= 0 ? log_slot : 0));
        uart_puts("\n");
    }
}

void access_control_poll(void) {
    if (rdm_cooldown_cnt > 0) {
        rdm_cooldown_cnt--;
    }

    // Read all incoming bytes from RFID UART RX FIFO and feed to parser
    int ch;
    while ((ch = rfid_uart_getc_nonblock()) >= 0) {
        rdm6300_tag_t tag;
        if (rdm6300_parse_byte((uint8_t)ch, &tag)) {
            // Valid frame parsed & checksum verified! Update current tag
            tag_available = true;
            tag_word_hi   = tag.hi;
            tag_word_lo   = tag.lo;
            for (int i = 0; i <= 10; i++) last_tag_hex[i] = tag.tag_hex[i];

            // Debounce check
            if (rdm_cooldown_cnt == 0 || tag.hi != last_scanned_hi || tag.lo != last_scanned_lo) {
                last_scanned_hi  = tag.hi;
                last_scanned_lo  = tag.lo;
                rdm_cooldown_cnt = 250000;
                access_control_process_card(last_tag_hex, tag_word_hi, tag_word_lo);
            }
        }
    }
}
