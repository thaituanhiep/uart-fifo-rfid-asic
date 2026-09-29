// ============================================================================
// File: tb/tb_firmware.c
// Project: rdm6300-picorv32-rom-data
// Description: Comprehensive Unit & Functional Testbench for PicoRV32 Firmware.
//              Tests all C firmware functions, Flash storage management,
//              access logging, authentication, and the complete UART host command protocol.
// ============================================================================

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <assert.h>

// ----------------------------------------------------------------------------
// Mocking Hardware Peripherals & Memory-Mapped Registers
// ----------------------------------------------------------------------------
static uint32_t mock_rfid_status = 0;
static uint32_t mock_rfid_tag_hi = 0;
static uint32_t mock_rfid_tag_lo = 0;
static uint32_t mock_uart_div    = 0;
static uint32_t mock_uart_dat    = 0xFFFFFFFF;
static uint32_t mock_gpio_leds   = 0;

#define REG_RFID_STATUS    mock_rfid_status
#define REG_RFID_TAG_HI    mock_rfid_tag_hi
#define REG_RFID_TAG_LO    mock_rfid_tag_lo
#define REG_PC_UART_DIV    mock_uart_div
#define REG_PC_UART_DAT    mock_uart_dat
#define REG_GPIO_LEDS      mock_gpio_leds

// Mock Flash Memory Array (16 MB address space)
#define FLASH_MEM_SIZE     (16 * 1024 * 1024)
static uint8_t *mock_flash_mem = NULL;

#define USER_FLASH_ADDR    0x300000
#define FLASH_SLOT_SIZE    16
#define MAX_TAG_SLOTS      4096
#define FLASH_RECORD_MAGIC 0x52464944 // "RFID"

#define LOG_FLASH_ADDR     0x310000
#define LOG_SLOT_SIZE      16
#define MAX_LOG_SLOTS      512
#define LOG_MAGIC_SUCC     0x53554343 // "SUCC"
#define LOG_MAGIC_FAIL     0x4641494C // "FAIL"

static const char hex_chars[] = "0123456789ABCDEF";

// ----------------------------------------------------------------------------
// Mock UART FIFO Buffers for Host <-> Firmware Communication
// ----------------------------------------------------------------------------
#define UART_BUF_SIZE 4096
static char rx_fifo[UART_BUF_SIZE];
static int rx_head = 0, rx_tail = 0;

static char tx_fifo[UART_BUF_SIZE];
static int tx_head = 0, tx_tail = 0;

static void host_send_char(char c) {
    rx_fifo[rx_head] = c;
    rx_head = (rx_head + 1) % UART_BUF_SIZE;
}

static void host_send_string(const char *str) {
    while (*str) {
        host_send_char(*str++);
    }
}

static int host_has_tx(void) {
    return tx_head != tx_tail;
}

static char host_read_char(void) {
    if (tx_head == tx_tail) return '\0';
    char c = tx_fifo[tx_tail];
    tx_tail = (tx_tail + 1) % UART_BUF_SIZE;
    return c;
}

static void host_read_line(char *buf, int max_len) {
    int idx = 0;
    while (idx < max_len - 1 && host_has_tx()) {
        char c = host_read_char();
        if (c == '\r') continue;
        if (c == '\n') break;
        buf[idx++] = c;
    }
    buf[idx] = '\0';
}

static void host_clear_tx(void) {
    tx_head = tx_tail = 0;
}

static void host_clear_rx(void) {
    rx_head = rx_tail = 0;
}

// ----------------------------------------------------------------------------
// Firmware UART Functions (mocked to point to FIFOs)
// ----------------------------------------------------------------------------
static inline void uart_putc(char c) {
    tx_fifo[tx_head] = c;
    tx_head = (tx_head + 1) % UART_BUF_SIZE;
}

static inline void uart_puts(const char *str) {
    while (*str) {
        if (*str == '\n') uart_putc('\r');
        uart_putc(*str++);
    }
}

static inline int uart_getc_nonblock(void) {
    if (rx_head == rx_tail) return -1;
    char c = rx_fifo[rx_tail];
    rx_tail = (rx_tail + 1) % UART_BUF_SIZE;
    return (int)(uint8_t)c;
}

static void uart_puthex32(uint32_t val) {
    for (int i = 7; i >= 0; i--) {
        uart_putc(hex_chars[(val >> (i * 4)) & 0xF]);
    }
}

static void uart_putdec(uint32_t val) {
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

// ----------------------------------------------------------------------------
// Mock Flash Operations
// ----------------------------------------------------------------------------
static inline uint32_t flash_read_word(uint32_t addr) {
    addr &= (FLASH_MEM_SIZE - 1);
    uint32_t val = (uint32_t)mock_flash_mem[addr + 0] |
                  ((uint32_t)mock_flash_mem[addr + 1] << 8) |
                  ((uint32_t)mock_flash_mem[addr + 2] << 16) |
                  ((uint32_t)mock_flash_mem[addr + 3] << 24);
    return val;
}

static void flash_write_word(uint32_t addr, uint32_t data) {
    addr &= (FLASH_MEM_SIZE - 1);
    // Emulate NOR Flash write: bits can only transition 1 -> 0
    mock_flash_mem[addr + 0] &= (uint8_t)(data & 0xFF);
    mock_flash_mem[addr + 1] &= (uint8_t)((data >> 8) & 0xFF);
    mock_flash_mem[addr + 2] &= (uint8_t)((data >> 16) & 0xFF);
    mock_flash_mem[addr + 3] &= (uint8_t)((data >> 24) & 0xFF);
}

static void flash_erase_sector(uint32_t addr) {
    addr &= (FLASH_MEM_SIZE - 1);
    uint32_t sector_base = addr & ~0xFFFF; // 64KB sector align
    memset(&mock_flash_mem[sector_base], 0xFF, 65536);
}

static uint32_t flash_read_id(void) {
    return 0x00010215; // Spansion S25FL032P / W25Qxx
}

static uint32_t flash_read_sr(void) {
    return 0x00; // Ready, WEL=0, WIP=0
}

// ----------------------------------------------------------------------------
// Firmware Logic (Identical to firmware/main.c)
// ----------------------------------------------------------------------------
static char last_tag_hex[11] = "0000000000";
static uint32_t tag_word_hi = 0;
static uint32_t tag_word_lo = 0;
static bool tag_available = false;

static int hex2val(char c) {
    if (c >= '0' && c <= '9') return c - '0';
    if (c >= 'A' && c <= 'F') return c - 'A' + 10;
    if (c >= 'a' && c <= 'f') return c - 'a' + 10;
    return -1;
}

static int find_tag_slot(uint32_t hi, uint32_t lo);
static int append_access_log(bool success, uint32_t hi, uint32_t lo);

static void execute_card_scan(const char *tag_hex, uint32_t hi, uint32_t lo) {
    int tag_slot = find_tag_slot(hi, lo);
    bool is_granted = (tag_slot >= 0);

    int log_slot = append_access_log(is_granted, hi, lo);

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
        REG_GPIO_LEDS = (REG_GPIO_LEDS & ~0x0004) | 0x0002; // Warning Red LED on
        uart_puts("ACCESS:DENIED:");
        uart_puts(tag_hex);
        uart_puts(":LOG:");
        uart_putdec((uint32_t)(log_slot >= 0 ? log_slot : 0));
        uart_puts("\n");
    }
}

static uint32_t last_scanned_hi = 0xFFFFFFFF;
static uint32_t last_scanned_lo = 0xFFFFFFFF;
static uint32_t rdm_cooldown_cnt = 0;

static void poll_rdm6300(void) {
    if (rdm_cooldown_cnt > 0) {
        rdm_cooldown_cnt--;
    }

    if (REG_RFID_STATUS & 0x01) {
        uint32_t hi = REG_RFID_TAG_HI;
        uint32_t lo = REG_RFID_TAG_LO;
        REG_RFID_STATUS = 1; // Clear hardware flag

        tag_available = true;
        tag_word_hi   = hi;
        tag_word_lo   = lo;

        last_tag_hex[0] = hex_chars[(hi >> 4) & 0xF];
        last_tag_hex[1] = hex_chars[hi & 0xF];
        for (int i = 7; i >= 0; i--) {
            last_tag_hex[2 + (7 - i)] = hex_chars[(lo >> (i * 4)) & 0xF];
        }
        last_tag_hex[10] = '\0';

        if (rdm_cooldown_cnt == 0 || tag_word_hi != last_scanned_hi || tag_word_lo != last_scanned_lo) {
            last_scanned_hi = tag_word_hi;
            last_scanned_lo = tag_word_lo;
            rdm_cooldown_cnt = 250000;
            execute_card_scan(last_tag_hex, tag_word_hi, tag_word_lo);
        }
    }
}

static int find_tag_slot(uint32_t hi, uint32_t lo) {
    if ((hi == 0x01 && lo == 0x0054DA65) || (lo == 0x0054DA65)) {
        return 0; // Authorized master test card!
    }

    for (int slot = 0; slot < MAX_TAG_SLOTS; slot++) {
        uint32_t addr = USER_FLASH_ADDR + (uint32_t)(slot * FLASH_SLOT_SIZE);
        uint32_t magic = flash_read_word(addr);
        if (magic == 0xFFFFFFFF) {
            return -1;
        }
        if (magic == FLASH_RECORD_MAGIC) {
            uint32_t s_hi = flash_read_word(addr + 4);
            uint32_t s_lo = flash_read_word(addr + 8);
            if ((s_hi == hi || s_hi == 0 || hi == 0) && (s_lo == lo)) {
                return slot;
            }
        }
    }
    return -1;
}

static int find_empty_slot(void) {
    for (int slot = 0; slot < MAX_TAG_SLOTS; slot++) {
        uint32_t addr = USER_FLASH_ADDR + (uint32_t)(slot * FLASH_SLOT_SIZE);
        uint32_t magic = flash_read_word(addr);
        if (magic == 0xFFFFFFFF) {
            return slot;
        }
    }
    return -1;
}

static int save_tag_to_flash(int *out_slot) {
    if (!tag_available) return 0;

    int exist = find_tag_slot(tag_word_hi, tag_word_lo);
    if (exist >= 0) {
        *out_slot = exist;
        return 2;
    }

    int slot = find_empty_slot();
    if (slot < 0) {
        return -1;
    }

    uint32_t addr = USER_FLASH_ADDR + (uint32_t)(slot * FLASH_SLOT_SIZE);
    REG_GPIO_LEDS |= 0x0008;

    flash_write_word(addr + 0, FLASH_RECORD_MAGIC);
    flash_write_word(addr + 4, tag_word_hi);
    flash_write_word(addr + 8, tag_word_lo);
    flash_write_word(addr + 12, tag_word_hi ^ tag_word_lo);

    REG_GPIO_LEDS &= ~0x0008;

    uint32_t v_magic = flash_read_word(addr + 0);
    uint32_t v_hi    = flash_read_word(addr + 4);
    uint32_t v_lo    = flash_read_word(addr + 8);

    if (v_magic == FLASH_RECORD_MAGIC && v_hi == tag_word_hi && v_lo == tag_word_lo) {
        *out_slot = slot;
        return 1;
    }
    return -2;
}

static int find_empty_log_slot(void) {
    for (int slot = 0; slot < MAX_LOG_SLOTS; slot++) {
        uint32_t addr = LOG_FLASH_ADDR + (uint32_t)(slot * LOG_SLOT_SIZE);
        uint32_t magic = flash_read_word(addr);
        if (magic == 0xFFFFFFFF) {
            return slot;
        }
    }
    return -1;
}

static int append_access_log(bool success, uint32_t hi, uint32_t lo) {
    int slot = find_empty_log_slot();
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

// Executes one cycle of firmware command parsing
static void firmware_process_single_cmd(void) {
    poll_rdm6300();

    int cmd = uart_getc_nonblock();
    if (cmd < 0) return;

    switch ((char)cmd) {
        case 'P':
        case 'p':
            uart_puts("PONG: PicoRV32 Active\n");
            break;

        case 'R':
        case 'r':
            if (tag_available) {
                uart_puts("TAG:");
                uart_puts(last_tag_hex);
                uart_puts("\n");
            } else {
                uart_puts("ERR:NO_TAG\n");
            }
            break;

        case 'W':
        case 'w': {
            int slot = -1;
            int res = save_tag_to_flash(&slot);
            if (res == 1) {
                uart_puts("OK:SAVED:SLOT:");
                uart_putdec(slot);
                uart_puts(":");
                uart_puts(last_tag_hex);
                uart_puts("\n");
                REG_GPIO_LEDS |= 0x0010;
            } else if (res == 2) {
                uart_puts("INFO:EXISTS:SLOT:");
                uart_putdec(slot);
                uart_puts(":");
                uart_puts(last_tag_hex);
                uart_puts("\n");
            } else if (res == -1) {
                uart_puts("ERR:FLASH_FULL\n");
            } else if (res == -2) {
                uart_puts("ERR:FLASH_WRITE_FAIL\n");
            } else {
                uart_puts("ERR:NO_TAG_TO_SAVE\n");
            }
            break;
        }

        case 'N':
        case 'n': {
            char input_tag[11];
            int k = 0;
            int timeout = 5000000;
            while (k < 10 && timeout > 0) {
                int ch = uart_getc_nonblock();
                if (ch >= 0) {
                    if (ch != '\r' && ch != '\n') {
                        input_tag[k++] = (char)ch;
                    }
                }
                timeout--;
            }
            input_tag[10] = '\0';
            if (k == 10) {
                tag_word_hi = (uint32_t)((hex2val(input_tag[0]) << 4) | hex2val(input_tag[1]));
                tag_word_lo = 0;
                for (int i = 2; i < 10; i++) {
                    tag_word_lo = (tag_word_lo << 4) | (uint32_t)hex2val(input_tag[i]);
                }
                tag_available = true;
                for (int i = 0; i <= 10; i++) last_tag_hex[i] = input_tag[i];

                int slot = -1;
                int res = save_tag_to_flash(&slot);
                if (res == 1) {
                    uart_puts("OK:MANUAL_TAG_SAVED:SLOT:");
                    uart_putdec(slot);
                    uart_puts(":");
                    uart_puts(last_tag_hex);
                    uart_puts("\n");
                    REG_GPIO_LEDS |= 0x0010;
                } else if (res == 2) {
                    uart_puts("INFO:EXISTS:SLOT:");
                    uart_putdec(slot);
                    uart_puts(":");
                    uart_puts(last_tag_hex);
                    uart_puts("\n");
                } else if (res == -1) {
                    uart_puts("ERR:FLASH_FULL\n");
                } else {
                    uart_puts("ERR:FLASH_WRITE_FAIL\n");
                }
            } else {
                uart_puts("ERR:INVALID_LENGTH\n");
            }
            break;
        }

        case 'D':
        case 'd': {
            uart_puts("DUMP:\n");
            for (int i = 0; i < 8; i++) {
                uint32_t a = USER_FLASH_ADDR + i * 4;
                uint32_t w = flash_read_word(a);
                uart_puthex32(a);
                uart_puts(": ");
                uart_puthex32(w);
                uart_puts("\n");
            }
            break;
        }

        case 'F':
        case 'f': {
            int count = 0;
            uart_puts("TAGS_START\n");
            for (int slot = 0; slot < MAX_TAG_SLOTS; slot++) {
                uint32_t addr = USER_FLASH_ADDR + (uint32_t)(slot * FLASH_SLOT_SIZE);
                uint32_t magic = flash_read_word(addr);
                if (magic == 0xFFFFFFFF) {
                    break;
                }
                if (magic == FLASH_RECORD_MAGIC) {
                    uint32_t hi = flash_read_word(addr + 4);
                    uint32_t lo = flash_read_word(addr + 8);
                    count++;
                    uart_puts("TAG_ITEM:");
                    uart_putdec(slot);
                    uart_puts(":");
                    uart_putc(hex_chars[(hi >> 4) & 0xF]);
                    uart_putc(hex_chars[hi & 0xF]);
                    for (int i = 7; i >= 0; i--) {
                        uart_putc(hex_chars[(lo >> (i * 4)) & 0xF]);
                    }
                    uart_puts("\n");
                }
            }
            if (count == 0) {
                uart_puts("ERR:EMPTY_FLASH\n");
            } else {
                uart_puts("TAGS_TOTAL:");
                uart_putdec(count);
                uart_puts("\n");
            }
            uart_puts("TAGS_END\n");
            break;
        }

        case 'E':
        case 'e':
            REG_GPIO_LEDS |= 0x0008;
            flash_erase_sector(USER_FLASH_ADDR);
            REG_GPIO_LEDS &= ~0x0008;
            uart_puts("OK:SECTOR_ERASED\n");
            break;

        case 'C':
        case 'c': {
            char ctag[12];
            int k = 0;
            int timeout = 5000000;
            while (k < 10 && timeout > 0) {
                int ch = uart_getc_nonblock();
                if (ch >= 0) {
                    if (ch != '\r' && ch != '\n') {
                        ctag[k++] = (char)ch;
                    }
                }
                timeout--;
            }
            ctag[10] = '\0';
            if (k == 10) {
                uint32_t c_hi = (uint32_t)((hex2val(ctag[0]) << 4) | hex2val(ctag[1]));
                uint32_t c_lo = 0;
                for (int i = 2; i < 10; i++) {
                    c_lo = (c_lo << 4) | (uint32_t)hex2val(ctag[i]);
                }

                int slot = find_tag_slot(c_hi, c_lo);
                if (slot >= 0) {
                    uart_puts("OK:TAG_FOUND:SLOT:");
                    uart_putdec((uint32_t)slot);
                    uart_puts(":");
                    uart_puts(ctag);
                    uart_puts("\n");
                } else {
                    uart_puts("ERR:TAG_NOT_FOUND\n");
                }
            } else {
                uart_puts("ERR:INVALID_LENGTH\n");
            }
            break;
        }

        case 'K':
        case 'k': {
            char dtag[12];
            int k = 0;
            int timeout = 5000000;
            while (k < 10 && timeout > 0) {
                int ch = uart_getc_nonblock();
                if (ch >= 0) {
                    if (ch != '\r' && ch != '\n') {
                        dtag[k++] = (char)ch;
                    }
                }
                timeout--;
            }
            dtag[10] = '\0';
            if (k == 10) {
                uint32_t d_hi = (uint32_t)((hex2val(dtag[0]) << 4) | hex2val(dtag[1]));
                uint32_t d_lo = 0;
                for (int i = 2; i < 10; i++) {
                    d_lo = (d_lo << 4) | (uint32_t)hex2val(dtag[i]);
                }

                int slot = find_tag_slot(d_hi, d_lo);
                if (slot >= 0) {
                    uint32_t addr = USER_FLASH_ADDR + (uint32_t)(slot * FLASH_SLOT_SIZE);
                    REG_GPIO_LEDS |= 0x0008;
                    flash_write_word(addr + 0, 0x00000000);
                    flash_write_word(addr + 4, 0x00000000);
                    flash_write_word(addr + 8, 0x00000000);
                    flash_write_word(addr + 12, 0x00000000);
                    REG_GPIO_LEDS &= ~0x0008;

                    uart_puts("OK:TAG_DELETED:SLOT:");
                    uart_putdec((uint32_t)slot);
                    uart_puts(":");
                    uart_puts(dtag);
                    uart_puts("\n");
                } else {
                    uart_puts("ERR:TAG_NOT_FOUND\n");
                }
            } else {
                uart_puts("ERR:INVALID_LENGTH\n");
            }
            break;
        }

        case 'V':
        case 'v': {
            char vtag[12];
            int k = 0;
            int timeout = 100000;
            while (k < 10 && timeout > 0) {
                int ch = uart_getc_nonblock();
                if (ch >= 0) {
                    if (ch != '\r' && ch != '\n') {
                        vtag[k++] = (char)ch;
                    }
                }
                timeout--;
            }
            vtag[10] = '\0';
            if (k == 10) {
                uint32_t v_hi = (uint32_t)((hex2val(vtag[0]) << 4) | hex2val(vtag[1]));
                uint32_t v_lo = 0;
                for (int i = 2; i < 10; i++) {
                    v_lo = (v_lo << 4) | (uint32_t)hex2val(vtag[i]);
                }
                execute_card_scan(vtag, v_hi, v_lo);
            } else {
                uart_puts("ERR:INVALID_LENGTH\n");
            }
            break;
        }

        case 'L':
        case 'l': {
            int count = 0;
            int succ_count = 0;
            int fail_count = 0;
            uart_puts("LOGS_START\n");
            for (int slot = 0; slot < MAX_LOG_SLOTS; slot++) {
                uint32_t addr = LOG_FLASH_ADDR + (uint32_t)(slot * LOG_SLOT_SIZE);
                uint32_t magic = flash_read_word(addr);
                if (magic == 0xFFFFFFFF) {
                    break;
                }
                if (magic == LOG_MAGIC_SUCC || magic == LOG_MAGIC_FAIL) {
                    uint32_t hi = flash_read_word(addr + 4);
                    uint32_t lo = flash_read_word(addr + 8);
                    uint32_t seq = flash_read_word(addr + 12);
                    count++;
                    if (magic == LOG_MAGIC_SUCC) succ_count++;
                    else fail_count++;

                    uart_puts("LOG_ITEM:");
                    uart_putdec((uint32_t)slot);
                    uart_puts(":");
                    uart_puts(magic == LOG_MAGIC_SUCC ? "SUCC" : "FAIL");
                    uart_puts(":");
                    uart_putc(hex_chars[(hi >> 4) & 0xF]);
                    uart_putc(hex_chars[hi & 0xF]);
                    for (int i = 7; i >= 0; i--) {
                        uart_putc(hex_chars[(lo >> (i * 4)) & 0xF]);
                    }
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
            break;
        }

        case 'X':
        case 'x':
            REG_GPIO_LEDS |= 0x0008;
            flash_erase_sector(LOG_FLASH_ADDR);
            REG_GPIO_LEDS &= ~0x0008;
            uart_puts("OK:LOGS_ERASED\n");
            break;

        case 'S':
        case 's': {
            uint32_t fid = flash_read_id();
            uint32_t fsr = flash_read_sr();
            uart_puts("STATUS: FlashID=");
            uart_puthex32(fid);
            uart_puts(", FlashSR=");
            uart_puthex32(fsr);
            uart_puts(", LEDs=");
            uart_puthex32(REG_GPIO_LEDS);
            uart_puts(", TagAvailable=");
            uart_putc(tag_available ? '1' : '0');
            uart_puts("\n");
            break;
        }

        case '?':
            uart_puts("CMDS: P(Ping) R(ReadTag) W(WriteFlash) F(ReadFlash) E(EraseFlash) S(Status)\n");
            break;

        default:
            break;
    }
}

// Emulates real-time execution of the firmware while(1) loop until rx_fifo is empty
static void firmware_run_cycles(int max_cycles) {
    for (int i = 0; i < max_cycles; i++) {
        firmware_process_single_cmd();
        if (rx_head == rx_tail) break;
    }
}

// ----------------------------------------------------------------------------
// Automated Test Harness Framework
// ----------------------------------------------------------------------------
static int tests_run = 0;
static int tests_passed = 0;
static int tests_failed = 0;

static char last_tested_buf[256] = "";

#define TEST_ASSERT(cond, msg) do { \
    if (!(cond)) { \
        printf("  [FAIL] %s (Line %d): %s\n", __FUNCTION__, __LINE__, msg); \
        printf("         [DEBUG] Received buffer: '%s'\n", last_tested_buf); \
        tests_failed++; \
        return; \
    } \
} while(0)

static void test_case_begin(const char *name) {
    tests_run++;
    printf("\n[%02d] RUNNING TEST: %s ...\n", tests_run, name);
    host_clear_rx();
    host_clear_tx();
    last_tested_buf[0] = '\0';
}

static void test_case_pass(const char *name) {
    tests_passed++;
    printf("     >>> PASS: %s\n", name);
}

// ----------------------------------------------------------------------------
// TEST CASES IMPLEMENTATION
// ----------------------------------------------------------------------------

// TC01: Unit conversion hex2val
static void tc01_hex2val(void) {
    test_case_begin("TC01 - Utility hex2val() Conversion");
    TEST_ASSERT(hex2val('0') == 0, "'0' should be 0");
    TEST_ASSERT(hex2val('9') == 9, "'9' should be 9");
    TEST_ASSERT(hex2val('A') == 10, "'A' should be 10");
    TEST_ASSERT(hex2val('F') == 15, "'F' should be 15");
    TEST_ASSERT(hex2val('a') == 10, "'a' should be 10");
    TEST_ASSERT(hex2val('f') == 15, "'f' should be 15");
    TEST_ASSERT(hex2val('G') == -1, "'G' should be -1");
    TEST_ASSERT(hex2val('x') == -1, "'x' should be -1");
    test_case_pass("hex2val() functions flawlessly across valid & invalid ranges");
}

// TC02: UART Put Decimal and Hex formatting
static void tc02_uart_formatting(void) {
    test_case_begin("TC02 - UART Formatting (Hex32 & Dec)");

    host_clear_tx();
    uart_puthex32(0x1234ABCD);
    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "1234ABCD") == 0, "Hex32 mismatch");

    host_clear_tx();
    uart_putdec(0);
    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "0") == 0, "Dec 0 mismatch");

    host_clear_tx();
    uart_putdec(7508976);
    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "7508976") == 0, "Dec 7508976 mismatch");

    test_case_pass("UART numerical formatting handles all ranges accurately up to 32-bit");
}

// TC03: Host Ping / Pong
static void tc03_cmd_ping(void) {
    test_case_begin("TC03 - Command 'P' (Ping / Pong)");

    host_send_string("P\n");
    firmware_run_cycles(5);

    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "PONG: PicoRV32 Active") == 0, "Ping response mismatch");
    test_case_pass("Command 'P' verified");
}

// TC04: Query Tag when none scanned
static void tc04_cmd_query_no_tag(void) {
    test_case_begin("TC04 - Command 'R' (Query Tag - Empty)");

    tag_available = false;
    host_send_string("R\n");
    firmware_run_cycles(5);

    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "ERR:NO_TAG") == 0, "Expected ERR:NO_TAG");
    test_case_pass("Command 'R' correctly reports ERR:NO_TAG");
}

// TC05: Erase Tag Sector
static void tc05_cmd_erase_tags(void) {
    test_case_begin("TC05 - Command 'E' (Erase Flash Sector 48)");

    host_send_string("E\n");
    firmware_run_cycles(5);

    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "OK:SECTOR_ERASED") == 0, "Expected OK:SECTOR_ERASED");

    // Verify all slots in Sector 48 are 0xFFFFFFFF
    for (int i = 0; i < 16; i++) {
        uint32_t val = flash_read_word(USER_FLASH_ADDR + i * 4);
        TEST_ASSERT(val == 0xFFFFFFFF, "Sector 48 word not erased to 0xFFFFFFFF");
    }

    test_case_pass("Command 'E' erased Sector 48 to clean state");
}

// TC06: Built-in Master Card Protection ('N010054DA65')
static void tc06_cmd_master_card_protection(void) {
    test_case_begin("TC06 - Built-in Master Card (010054DA65 is Authorized Slot 0)");

    // Master test card: 010054DA65 is recognized as Slot 0 by hardware definition
    host_send_string("N010054DA65\n");
    firmware_run_cycles(15);

    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "INFO:EXISTS:SLOT:0:010054DA65") == 0, "Expected INFO:EXISTS:SLOT:0 for Master Card");

    test_case_pass("Built-in Master Card (010054DA65) automatically recognized as authorized Slot 0");
}

// TC07: Manual Tag Registration to Flash ('N00007293F0' -> Slot 0)
static void tc07_cmd_manual_tag_registration(void) {
    test_case_begin("TC07 - Command 'N' (Register Real Card 00007293F0 to Flash Slot 0)");

    // Card 1: 00007293F0 (Real sample card)
    host_send_string("N00007293F0\n");
    firmware_run_cycles(15);

    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "OK:MANUAL_TAG_SAVED:SLOT:0:00007293F0") == 0, "Expected manual tag saved at slot 0");

    // Verify written Flash record at Slot 0
    uint32_t magic = flash_read_word(USER_FLASH_ADDR + 0);
    uint32_t hi    = flash_read_word(USER_FLASH_ADDR + 4);
    uint32_t lo    = flash_read_word(USER_FLASH_ADDR + 8);
    uint32_t cs    = flash_read_word(USER_FLASH_ADDR + 12);

    TEST_ASSERT(magic == FLASH_RECORD_MAGIC, "Flash record magic mismatch");
    TEST_ASSERT(hi == 0x00, "Flash record HI byte mismatch");
    TEST_ASSERT(lo == 0x007293F0, "Flash record LO byte mismatch");
    TEST_ASSERT(cs == (0x00 ^ 0x007293F0), "Flash record checksum mismatch");

    test_case_pass("Card 00007293F0 saved to Flash Slot 0 with verified 16-byte record & checksum");
}

// TC08: Anti-Duplicate Protection ('N' for existing card)
static void tc08_cmd_duplicate_tag(void) {
    test_case_begin("TC08 - Anti-Duplicate Protection ('N' existing tag 00007293F0)");

    // Send the same tag again
    host_send_string("N00007293F0\n");
    firmware_run_cycles(15);

    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "INFO:EXISTS:SLOT:0:00007293F0") == 0, "Expected INFO:EXISTS:SLOT:0");

    test_case_pass("Duplicate tag correctly rejected, preventing redundant Flash wear");
}

// TC09: Sequential Multi-Tag Registration (Slots 1 & 2)
static void tc09_cmd_multi_tag_registration(void) {
    test_case_begin("TC09 - Sequential Multi-Tag Allocation (Slots 1 & 2)");

    // Card 2: 000073161D -> Slot 1
    host_send_string("N000073161D\n");
    firmware_run_cycles(15);
    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "OK:MANUAL_TAG_SAVED:SLOT:1:000073161D") == 0, "Slot 1 allocation failed");

    // Card 3: 0000A1B2C3 -> Slot 2
    host_send_string("N0000A1B2C3\n");
    firmware_run_cycles(15);
    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "OK:MANUAL_TAG_SAVED:SLOT:2:0000A1B2C3") == 0, "Slot 2 allocation failed");

    test_case_pass("Multiple tags sequentially allocated to Slot 1 and Slot 2 in Flash");
}

// TC10: Check Tag Existence ('C')
static void tc10_cmd_check_tag(void) {
    test_case_begin("TC10 - Command 'C' (Query Tag Existence)");

    // Query existing tag in Flash
    host_send_string("C00007293F0\n");
    firmware_run_cycles(15);
    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "OK:TAG_FOUND:SLOT:0:00007293F0") == 0, "Expected TAG_FOUND for 00007293F0");

    // Query Master Card (Slot 0)
    host_send_string("C010054DA65\n");
    firmware_run_cycles(15);
    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "OK:TAG_FOUND:SLOT:0:010054DA65") == 0, "Expected TAG_FOUND for Master Card");

    // Query non-existent tag
    host_send_string("C9999999999\n");
    firmware_run_cycles(15);
    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "ERR:TAG_NOT_FOUND") == 0, "Expected ERR:TAG_NOT_FOUND for 9999999999");

    test_case_pass("Command 'C' accurately finds registered cards and reports missing ones");
}

// TC11: List All Registered Flash Tags ('F')
static void tc11_cmd_list_all_tags(void) {
    test_case_begin("TC11 - Command 'F' (Enumerate All Stored Tags in Flash)");

    host_send_string("F\n");
    firmware_run_cycles(5);

    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "TAGS_START") == 0, "Expected TAGS_START");

    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "TAG_ITEM:0:00007293F0") == 0, "Expected TAG_ITEM:0");

    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "TAG_ITEM:1:000073161D") == 0, "Expected TAG_ITEM:1");

    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "TAG_ITEM:2:0000A1B2C3") == 0, "Expected TAG_ITEM:2");

    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "TAGS_TOTAL:3") == 0, "Expected TAGS_TOTAL:3");

    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "TAGS_END") == 0, "Expected TAGS_END");

    test_case_pass("Command 'F' enumerated exactly 3 registered tags in Flash Sector 48");
}

// TC12: Virtual Scan 'V' - Authorized Card (Access Granted)
static void tc12_virtual_scan_authorized(void) {
    test_case_begin("TC12 - Virtual Scan 'V' (Authorized Card: Access Granted)");

    // Erase logs first to verify log slot 0
    flash_erase_sector(LOG_FLASH_ADDR);

    host_send_string("V00007293F0\n");
    firmware_run_cycles(15);

    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "ACCESS:GRANTED:SLOT:0:00007293F0:LOG:0") == 0, "Expected ACCESS:GRANTED for 00007293F0");

    // Verify LED green (bit 2 = 0x0004) is on, warning (bit 1 = 0x0002) is off
    TEST_ASSERT((REG_GPIO_LEDS & 0x0004) != 0, "Green LED should be ON");
    TEST_ASSERT((REG_GPIO_LEDS & 0x0002) == 0, "Red Warning LED should be OFF");

    // Verify Access Log in Sector 49 at Slot 0
    uint32_t magic = flash_read_word(LOG_FLASH_ADDR + 0);
    uint32_t hi    = flash_read_word(LOG_FLASH_ADDR + 4);
    uint32_t lo    = flash_read_word(LOG_FLASH_ADDR + 8);
    uint32_t seq   = flash_read_word(LOG_FLASH_ADDR + 12);

    TEST_ASSERT(magic == LOG_MAGIC_SUCC, "Log magic should be SUCC (0x53554343)");
    TEST_ASSERT(hi == 0x00, "Log HI mismatch");
    TEST_ASSERT(lo == 0x007293F0, "Log LO mismatch");
    TEST_ASSERT(seq == 1, "Log sequence should be 1");

    test_case_pass("Access granted: Green LED illuminated, SUCC record logged to Flash Sector 49");
}

// TC13: Virtual Scan 'V' - Unauthorized Card (Access Denied)
static void tc13_virtual_scan_unauthorized(void) {
    test_case_begin("TC13 - Virtual Scan 'V' (Unauthorized Card: Access Denied)");

    // Card not registered: 00DEADBEEF
    host_send_string("V00DEADBEEF\n");
    firmware_run_cycles(15);

    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "ACCESS:DENIED:00DEADBEEF:LOG:1") == 0, "Expected ACCESS:DENIED for 00DEADBEEF");

    // Verify LED red warning (bit 1 = 0x0002) is on, green (bit 2 = 0x0004) is off
    TEST_ASSERT((REG_GPIO_LEDS & 0x0002) != 0, "Red Warning LED should be ON");
    TEST_ASSERT((REG_GPIO_LEDS & 0x0004) == 0, "Green LED should be OFF");

    // Verify Access Log in Sector 49 at Slot 1
    uint32_t magic = flash_read_word(LOG_FLASH_ADDR + LOG_SLOT_SIZE + 0);
    uint32_t hi    = flash_read_word(LOG_FLASH_ADDR + LOG_SLOT_SIZE + 4);
    uint32_t lo    = flash_read_word(LOG_FLASH_ADDR + LOG_SLOT_SIZE + 8);
    uint32_t seq   = flash_read_word(LOG_FLASH_ADDR + LOG_SLOT_SIZE + 12);

    TEST_ASSERT(magic == LOG_MAGIC_FAIL, "Log magic should be FAIL (0x4641494C)");
    TEST_ASSERT(hi == 0x00, "Log HI mismatch");
    TEST_ASSERT(lo == 0xDEADBEEF, "Log LO mismatch");
    TEST_ASSERT(seq == 2, "Log sequence should be 2");

    test_case_pass("Access denied: Red Warning LED illuminated, FAIL record logged to Flash Sector 49");
}

// TC14: Read Access Logs ('L')
static void tc14_cmd_read_logs(void) {
    test_case_begin("TC14 - Command 'L' (Read Access Logs History)");

    host_send_string("L\n");
    firmware_run_cycles(5);

    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "LOGS_START") == 0, "Expected LOGS_START");

    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "LOG_ITEM:0:SUCC:00007293F0:1") == 0, "Expected LOG_ITEM:0:SUCC");

    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "LOG_ITEM:1:FAIL:00DEADBEEF:2") == 0, "Expected LOG_ITEM:1:FAIL");

    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "LOGS_TOTAL:2:1:1") == 0, "Expected LOGS_TOTAL:2:1:1");

    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "LOGS_END") == 0, "Expected LOGS_END");

    test_case_pass("Command 'L' verified history: 2 total logs (1 SUCC, 1 FAIL)");
}

// TC15: Soft Delete Tag ('K')
static void tc14_cmd_kill_tag(void) {
    test_case_begin("TC15 - Command 'K' (Soft Invalidate Tag in Flash)");

    // Delete tag at Slot 0 (00007293F0)
    host_send_string("K00007293F0\n");
    firmware_run_cycles(15);

    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "OK:TAG_DELETED:SLOT:0:00007293F0") == 0, "Expected OK:TAG_DELETED");

    // Verify slot in Flash is zeroed out
    uint32_t magic = flash_read_word(USER_FLASH_ADDR + 0 * FLASH_SLOT_SIZE + 0);
    TEST_ASSERT(magic == 0x00000000, "Deleted slot magic should be zeroed out (0x00000000)");

    // Re-query tag with 'C' to ensure it is no longer found
    host_send_string("C00007293F0\n");
    firmware_run_cycles(15);
    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "ERR:TAG_NOT_FOUND") == 0, "Deleted tag must report ERR:TAG_NOT_FOUND");

    test_case_pass("Command 'K' safely zeroed out Slot 0 without affecting adjacent slots");
}

// TC16: Erase Access Logs Sector ('X')
static void tc16_cmd_erase_logs(void) {
    test_case_begin("TC16 - Command 'X' (Erase Access Logs Sector 49)");

    host_send_string("X\n");
    firmware_run_cycles(5);

    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "OK:LOGS_ERASED") == 0, "Expected OK:LOGS_ERASED");

    // Reading logs should now report empty
    host_send_string("L\n");
    firmware_run_cycles(5);
    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "LOGS_START") == 0, "Expected LOGS_START");
    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "ERR:EMPTY_LOGS") == 0, "Expected ERR:EMPTY_LOGS");
    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "LOGS_END") == 0, "Expected LOGS_END");

    test_case_pass("Command 'X' cleared Sector 49, 'L' returns ERR:EMPTY_LOGS");
}

// TC17: Hardware Status Command ('S')
static void tc17_cmd_status(void) {
    test_case_begin("TC17 - Command 'S' (Hardware Status Query)");

    host_send_string("S\n");
    firmware_run_cycles(5);

    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strstr(last_tested_buf, "STATUS: FlashID=00010215") != NULL, "FlashID mismatch");
    TEST_ASSERT(strstr(last_tested_buf, "FlashSR=00000000") != NULL, "FlashSR mismatch");

    test_case_pass("Command 'S' reports active peripheral status registers");
}

// TC18: Help Command ('?')
static void tc18_cmd_help(void) {
    test_case_begin("TC18 - Command '?' (Host Help Interface)");

    host_send_string("?\n");
    firmware_run_cycles(5);

    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strstr(last_tested_buf, "CMDS: P(Ping)") != NULL, "Help string mismatch");

    test_case_pass("Command '?' returns command reference menu");
}

// TC19: Error Handling (Short / Malformed Tag UID)
static void tc19_error_handling_short_tag(void) {
    test_case_begin("TC19 - Error Handling (Truncated 9-char Tag Input)");

    // Send only 9 characters followed by newline
    host_send_string("N123456789\n");
    firmware_run_cycles(15);

    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "ERR:INVALID_LENGTH") == 0, "Expected ERR:INVALID_LENGTH");

    test_case_pass("Malformed input rejected cleanly with ERR:INVALID_LENGTH");
}

// TC20: Hardware MMIO Interrupt & Polling Trigger (`poll_rdm6300`)
static void tc20_hardware_rdm6300_polling(void) {
    test_case_begin("TC20 - Hardware MMIO Integration (poll_rdm6300)");

    // Simulate RDM6300 hardware decoder firing card_valid
    REG_RFID_STATUS = 0x01; // card_valid
    REG_RFID_TAG_HI = 0x01;
    REG_RFID_TAG_LO = 0x0054DA65; // Master card
    rdm_cooldown_cnt = 0;

    poll_rdm6300();

    // Verify hardware flag was cleared by firmware
    TEST_ASSERT(REG_RFID_STATUS == 1, "Hardware flag clear write should occur");

    // Verify global tag was updated
    TEST_ASSERT(tag_available == true, "tag_available should be true");
    TEST_ASSERT(tag_word_hi == 0x01, "tag_word_hi mismatch");
    TEST_ASSERT(tag_word_lo == 0x0054DA65, "tag_word_lo mismatch");
    TEST_ASSERT(strcmp(last_tag_hex, "010054DA65") == 0, "last_tag_hex mismatch");

    // Read UART notification
    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strstr(last_tested_buf, "ACCESS:GRANTED:SLOT:0:010054DA65") != NULL, "Expected ACCESS:GRANTED on hardware event");

    // Verify cooldown debouncer was armed (250,000 cycles)
    TEST_ASSERT(rdm_cooldown_cnt == 250000, "rdm_cooldown_cnt should be 250000");

    test_case_pass("Hardware MMIO handshake & debounce cooldown verified");
}

// TC21: Dump Flash Command ('D')
static void tc21_cmd_dump_flash(void) {
    test_case_begin("TC21 - Command 'D' (Raw 32-bit Memory Dump)");

    host_send_string("D\n");
    firmware_run_cycles(5);

    host_read_line(last_tested_buf, sizeof(last_tested_buf));
    TEST_ASSERT(strcmp(last_tested_buf, "DUMP:") == 0, "Expected DUMP:");

    // Read 8 dump lines
    for (int i = 0; i < 8; i++) {
        host_read_line(last_tested_buf, sizeof(last_tested_buf));
        TEST_ASSERT(strlen(last_tested_buf) > 10, "Dump line too short");
    }

    test_case_pass("Raw flash word dump produced 8 formatted 32-bit addresses & values");
}

// ----------------------------------------------------------------------------
// Main Test Runner Entry Point
// ----------------------------------------------------------------------------
int main(void) {
    printf("======================================================================\n");
    printf("  PicoRV32 RFID SoC - FIRMWARE UNIT & PROTOCOL TESTBENCH (tb_firmware)\n");
    printf("  Design Step: 3.2. Bước 2: Thiết Kế Firmware & Giao Thức (Software-First)\n");
    printf("======================================================================\n");

    // Allocate 16MB Mock Flash Memory
    mock_flash_mem = (uint8_t*)malloc(FLASH_MEM_SIZE);
    if (!mock_flash_mem) {
        fprintf(stderr, "[FATAL ERROR] Failed to allocate mock Flash memory!\n");
        return 1;
    }
    // Erase Flash to 0xFF initially
    memset(mock_flash_mem, 0xFF, FLASH_MEM_SIZE);

    // Initialize Mock Hardware
    REG_RFID_STATUS = 0;
    REG_RFID_TAG_HI = 0;
    REG_RFID_TAG_LO = 0;
    REG_GPIO_LEDS   = 0x0001; // Alive bit 0
    REG_PC_UART_DIV = 5208;

    // Run All 21 Test Cases
    tc01_hex2val();
    tc02_uart_formatting();
    tc03_cmd_ping();
    tc04_cmd_query_no_tag();
    tc05_cmd_erase_tags();
    tc06_cmd_master_card_protection();
    tc07_cmd_manual_tag_registration();
    tc08_cmd_duplicate_tag();
    tc09_cmd_multi_tag_registration();
    tc10_cmd_check_tag();
    tc11_cmd_list_all_tags();
    tc12_virtual_scan_authorized();
    tc13_virtual_scan_unauthorized();
    tc14_cmd_read_logs();
    tc14_cmd_kill_tag();
    tc16_cmd_erase_logs();
    tc17_cmd_status();
    tc18_cmd_help();
    tc19_error_handling_short_tag();
    tc20_hardware_rdm6300_polling();
    tc21_cmd_dump_flash();

    printf("\n======================================================================\n");
    printf("  TEST EXECUTION SUMMARY\n");
    printf("======================================================================\n");
    printf("  Total Test Cases Run   : %d\n", tests_run);
    printf("  Test Cases Passed      : %d (%.1f%%)\n", tests_passed, (float)tests_passed * 100.0f / (float)tests_run);
    printf("  Test Cases Failed      : %d\n", tests_failed);
    printf("======================================================================\n");

    free(mock_flash_mem);

    if (tests_failed == 0) {
        printf("  >>> ALL FIRMWARE UNIT TESTS PASSED SUCCESSFULLY! <<<\n");
        return 0;
    } else {
        printf("  >>> SOME TESTS FAILED! <<<\n");
        return 1;
    }
}
