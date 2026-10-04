// ============================================================================
// File: firmware/drivers/flash.c
// Project: rdm6300-picorv32-rom-data
// Description: SPI Flash Driver & Data Storage Implementation (XIP + flashio)
// ============================================================================

#include "flash.h"
#include "soc_regs.h"
#include "uart.h"
#include "hex_utils.h"

// ----------------------------------------------------------------------------
// Low-Level SPI Flash Worker (from start.s)
// ----------------------------------------------------------------------------
extern uint32_t flashio_worker_begin;
extern uint32_t flashio_worker_end;

static void flashio(uint8_t *data, int len, uint8_t wrencmd) {
    uint32_t func[&flashio_worker_end - &flashio_worker_begin];
    uint32_t *src_ptr = &flashio_worker_begin;
    uint32_t *dst_ptr = func;

    while (src_ptr != &flashio_worker_end)
        *(dst_ptr++) = *(src_ptr++);

    ((void(*)(uint8_t*, uint32_t, uint32_t))func)(data, len, wrencmd);
}

// ----------------------------------------------------------------------------
// Primitive SPI Flash Operations
// ----------------------------------------------------------------------------
uint32_t flash_read_word(uint32_t addr) {
    return *(volatile uint32_t*)(addr & 0x00FFFFFF);
}

void flash_write_word(uint32_t addr, uint32_t data) {
    uint32_t paddr = addr & 0x00FFFFFF;
    uint8_t buf[8];
    buf[0] = 0x02; // Page Program
    buf[1] = (uint8_t)(paddr >> 16);
    buf[2] = (uint8_t)(paddr >> 8);
    buf[3] = (uint8_t)paddr;
    buf[4] = (uint8_t)data;
    buf[5] = (uint8_t)(data >> 8);
    buf[6] = (uint8_t)(data >> 16);
    buf[7] = (uint8_t)(data >> 24);
    flashio(buf, 8, 0x06); // WREN = 0x06
}

uint32_t flash_read_sr(void) {
    uint8_t buf[2] = {0x05, 0x00};
    flashio(buf, 2, 0);
    return (uint32_t)buf[1];
}

uint32_t flash_read_id(void) {
    uint8_t buf[4] = {0x9F, 0x00, 0x00, 0x00};
    flashio(buf, 4, 0);
    return ((uint32_t)buf[1] << 16) | ((uint32_t)buf[2] << 8) | (uint32_t)buf[3];
}

void flash_erase_sector(uint32_t addr) {
    uint32_t paddr = addr & 0x00FFFFFF;
    uint8_t buf[4];
    buf[0] = 0xD8; // Block Erase 64KB
    buf[1] = (uint8_t)(paddr >> 16);
    buf[2] = (uint8_t)(paddr >> 8);
    buf[3] = (uint8_t)paddr;
    flashio(buf, 4, 0x06); // WREN = 0x06
}

// ----------------------------------------------------------------------------
// Flash Data Storage Mechanisms: Authorized RFID Tags (Sector 48: 0x300000)
// ----------------------------------------------------------------------------
int flash_find_tag(uint32_t hi, uint32_t lo) {
    // Built-in authorized master test card (UID: 010054DA65 / 0005560933)
    if ((hi == 0x01 && lo == 0x0054DA65) || (lo == 0x0054DA65)) {
        return 0;
    }

    for (int slot = 0; slot < MAX_TAG_SLOTS; slot++) {
        uint32_t addr = USER_FLASH_ADDR + (uint32_t)(slot * FLASH_SLOT_SIZE);
        uint32_t magic = flash_read_word(addr);
        if (magic == 0xFFFFFFFF) {
            return -1; // Empty slot reached; stop searching
        }
        if (magic == FLASH_RECORD_MAGIC) {
            uint32_t s_hi = flash_read_word(addr + 4);
            uint32_t s_lo = flash_read_word(addr + 8);
            if ((s_hi == hi || s_hi == 0 || hi == 0) && (s_lo == lo)) {
                return slot; // Match found
            }
        }
    }
    return -1;
}

int flash_find_empty_tag_slot(void) {
    for (int slot = 0; slot < MAX_TAG_SLOTS; slot++) {
        uint32_t addr = USER_FLASH_ADDR + (uint32_t)(slot * FLASH_SLOT_SIZE);
        uint32_t magic = flash_read_word(addr);
        if (magic == 0xFFFFFFFF) {
            return slot;
        }
    }
    return -1;
}

int flash_save_tag(uint32_t hi, uint32_t lo, int *out_slot) {
    // Check if tag already exists in Flash
    int exist = flash_find_tag(hi, lo);
    if (exist >= 0) {
        if (out_slot) *out_slot = exist;
        return 2;
    }

    // Find next empty slot
    int slot = flash_find_empty_tag_slot();
    if (slot < 0) {
        return -1; // Flash full
    }

    uint32_t addr = USER_FLASH_ADDR + (uint32_t)(slot * FLASH_SLOT_SIZE);

    REG_GPIO_LEDS |= 0x0008; // Flash active LED

    flash_write_word(addr + 0, FLASH_RECORD_MAGIC);
    flash_write_word(addr + 4, hi);
    flash_write_word(addr + 8, lo);
    flash_write_word(addr + 12, hi ^ lo);

    REG_GPIO_LEDS &= ~0x0008;

    // Verify written data
    uint32_t v_magic = flash_read_word(addr + 0);
    uint32_t v_hi    = flash_read_word(addr + 4);
    uint32_t v_lo    = flash_read_word(addr + 8);

    if (v_magic == FLASH_RECORD_MAGIC && v_hi == hi && v_lo == lo) {
        if (out_slot) *out_slot = slot;
        return 1; // Success
    }

    return -2; // Verification failed
}

bool flash_delete_tag(int slot) {
    if (slot < 0 || slot >= MAX_TAG_SLOTS) return false;

    uint32_t addr = USER_FLASH_ADDR + (uint32_t)(slot * FLASH_SLOT_SIZE);
    REG_GPIO_LEDS |= 0x0008;

    flash_write_word(addr + 0, 0x00000000);
    flash_write_word(addr + 4, 0x00000000);
    flash_write_word(addr + 8, 0x00000000);
    flash_write_word(addr + 12, 0x00000000);

    REG_GPIO_LEDS &= ~0x0008;
    return true;
}

void flash_erase_tags_sector(void) {
    REG_GPIO_LEDS |= 0x0008;
    flash_erase_sector(USER_FLASH_ADDR);
    REG_GPIO_LEDS &= ~0x0008;
}

// ----------------------------------------------------------------------------
// Flash Data Storage Mechanisms: Access Logs (Sector 49: 0x310000)
// ----------------------------------------------------------------------------
int flash_find_empty_log_slot(void) {
    for (int slot = 0; slot < MAX_LOG_SLOTS; slot++) {
        uint32_t addr = LOG_FLASH_ADDR + (uint32_t)(slot * LOG_SLOT_SIZE);
        uint32_t magic = flash_read_word(addr);
        if (magic == 0xFFFFFFFF) {
            return slot;
        }
    }
    return -1;
}

int flash_append_log(bool success, uint32_t hi, uint32_t lo) {
    int slot = flash_find_empty_log_slot();
    if (slot < 0) return -1;

    uint32_t addr = LOG_FLASH_ADDR + (uint32_t)(slot * LOG_SLOT_SIZE);
    uint32_t status_magic = success ? LOG_MAGIC_SUCC : LOG_MAGIC_FAIL;
    uint32_t seq = (uint32_t)(slot + 1);

    REG_GPIO_LEDS |= 0x0008;

    flash_write_word(addr + 4, hi);
    flash_write_word(addr + 8, lo);
    flash_write_word(addr + 12, seq);
    flash_write_word(addr + 0, status_magic);

    REG_GPIO_LEDS &= ~0x0008;

    if (flash_read_word(addr + 0) != status_magic) {
        return -2;
    }
    return slot;
}

void flash_erase_logs_sector(void) {
    REG_GPIO_LEDS |= 0x0008;
    flash_erase_sector(LOG_FLASH_ADDR);
    REG_GPIO_LEDS &= ~0x0008;
}

// ----------------------------------------------------------------------------
// Flash Diagnostic & Reporting Procedures
// ----------------------------------------------------------------------------
void flash_dump_raw(uint32_t addr, int word_count) {
    uart_puts("DUMP:\n");
    for (int i = 0; i < word_count; i++) {
        uint32_t a = addr + (uint32_t)(i * 4);
        uint32_t w = flash_read_word(a);
        uart_puthex32(a);
        uart_puts(": ");
        uart_puthex32(w);
        uart_puts("\n");
    }
}

void flash_dump_all_tags(void) {
    int count = 0;
    uart_puts("TAGS_START\n");
    for (int slot = 0; slot < MAX_TAG_SLOTS; slot++) {
        uint32_t addr = USER_FLASH_ADDR + (uint32_t)(slot * FLASH_SLOT_SIZE);
        uint32_t magic = flash_read_word(addr);
        if (magic == 0xFFFFFFFF) {
            break; // End of list
        }
        if (magic == FLASH_RECORD_MAGIC) {
            uint32_t hi = flash_read_word(addr + 4);
            uint32_t lo = flash_read_word(addr + 8);
            char tag_str[11];
            uid_to_hex_str(hi, lo, tag_str);

            count++;
            uart_print_slot_tag("TAG_ITEM", slot, tag_str);
        }
    }
    if (count == 0) {
        uart_puts("ERR:EMPTY_FLASH\n");
    } else {
        uart_puts("TAGS_TOTAL:");
        uart_putdec((uint32_t)count);
        uart_puts("\n");
    }
    uart_puts("TAGS_END\n");
}

void flash_dump_all_logs(void) {
    int count = 0;
    int succ_count = 0;
    int fail_count = 0;
    uart_puts("LOGS_START\n");
    for (int slot = 0; slot < MAX_LOG_SLOTS; slot++) {
        uint32_t addr = LOG_FLASH_ADDR + (uint32_t)(slot * LOG_SLOT_SIZE);
        uint32_t magic = flash_read_word(addr);
        if (magic == 0xFFFFFFFF) {
            break; // End of log records
        }
        if (magic == LOG_MAGIC_SUCC || magic == LOG_MAGIC_FAIL) {
            uint32_t hi = flash_read_word(addr + 4);
            uint32_t lo = flash_read_word(addr + 8);
            uint32_t seq = flash_read_word(addr + 12);
            char tag_str[11];
            uid_to_hex_str(hi, lo, tag_str);

            count++;
            if (magic == LOG_MAGIC_SUCC) succ_count++;
            else fail_count++;

            uart_puts("LOG_ITEM:");
            uart_putdec((uint32_t)slot);
            uart_puts(":");
            uart_puts(magic == LOG_MAGIC_SUCC ? "SUCC" : "FAIL");
            uart_puts(":");
            uart_puts(tag_str);
            uart_puts(":");
            uart_putdec(seq);
            uart_puts("\n");
        }
    }
    if (count == 0) {
        uart_puts("ERR:EMPTY_LOGS\n");
    } else {
        uart_puts("LOGS_TOTAL:");
        uart_putdec((uint32_t)count);
        uart_puts(":");
        uart_putdec((uint32_t)succ_count);
        uart_puts(":");
        uart_putdec((uint32_t)fail_count);
        uart_puts("\n");
    }
    uart_puts("LOGS_END\n");
}
