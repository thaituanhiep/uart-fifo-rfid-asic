// ============================================================================
// File: firmware/main.c
// Project: rdm6300-picorv32-rom-data
// Description: PicoRV32 C Firmware for RDM6300 RFID Reader & SPI Flash Manager.
//              Handles RFID frame parsing, SPI Flash programming/reading,
//              and bidirectional command communication with PC Host over UART.
// ============================================================================

#include <stdint.h>
#include <stdbool.h>

// ----------------------------------------------------------------------------
// Memory Mapped Peripheral Base Addresses
// ----------------------------------------------------------------------------
#define REG_RDM_UART_DIV   (*(volatile uint32_t*)0x10000000)
#define REG_RDM_UART_DAT   (*(volatile uint32_t*)0x10000004)

#define REG_FLASH_CTRL     (*(volatile uint32_t*)0x20000000)
#define REG_FLASH_STATUS   (*(volatile uint32_t*)0x20000004)
#define REG_FLASH_ADDR     (*(volatile uint32_t*)0x20000008)
#define REG_FLASH_WDATA    (*(volatile uint32_t*)0x2000000C)
#define REG_FLASH_RDATA    (*(volatile uint32_t*)0x20000010)

#define REG_PC_UART_DIV    (*(volatile uint32_t*)0x30000000)
#define REG_PC_UART_DAT    (*(volatile uint32_t*)0x30000004)

#define REG_GPIO_LEDS      (*(volatile uint32_t*)0x40000000)

// SPI Flash Command Opcodes for REG_FLASH_CTRL
#define FLASH_OP_READ          0
#define FLASH_OP_WRITE         1
#define FLASH_OP_SECTOR_ERASE  2
#define FLASH_OP_RDID          3
#define FLASH_OP_RDSR          4

// Default Flash storage address (3MB offset, safe from FPGA bitstream)
#define USER_FLASH_ADDR        0x300000

// ----------------------------------------------------------------------------
void *memcpy(void *dest, const void *src, unsigned int n) {
    char *d = (char *)dest;
    const char *s = (const char *)src;
    while (n--) *d++ = *s++;
    return dest;
}

void *memset(void *s, int c, unsigned int n) {
    char *p = (char *)s;
    while (n--) *p++ = (char)c;
    return s;
}

static const char hex_chars[] = "0123456789ABCDEF";

// ----------------------------------------------------------------------------
// Host PC UART Functions
// ----------------------------------------------------------------------------
static inline void uart_putc(char c) {
    REG_PC_UART_DAT = (uint32_t)(uint8_t)c;
}

static inline void uart_puts(const char *str) {
    while (*str) {
        if (*str == '\n') uart_putc('\r');
        uart_putc(*str++);
    }
}

static inline int uart_getc_nonblock(void) {
    uint32_t d = REG_PC_UART_DAT;
    if (d == 0xFFFFFFFF) return -1;
    return (int)(d & 0xFF);
}

static inline char uart_getc_blocking(void) {
    int c;
    do {
        c = uart_getc_nonblock();
    } while (c < 0);
    return (char)c;
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
    uint32_t divisor = 10000;
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
        if (divisor == 10000) divisor = 1000;
        else if (divisor == 1000) divisor = 100;
        else if (divisor == 100) divisor = 10;
        else if (divisor == 10) divisor = 1;
        else divisor = 0;
    }
}

// Multi-Tag Flash Storage Layout (Sector 48: 0x300000)
#define FLASH_SLOT_SIZE        16        // 16 bytes per tag record
#define MAX_TAG_SLOTS          256       // 256 records max (4096 bytes / 4KB)
#define FLASH_RECORD_MAGIC     0x52464944 // "RFID"

// Access Log Flash Storage Layout (Sector 49: 0x310000)
#define LOG_FLASH_ADDR         0x310000  // Base address for access logs
#define LOG_SLOT_SIZE          16        // 16 bytes per log record
#define MAX_LOG_SLOTS          512       // 512 log records max (8KB)
#define LOG_MAGIC_SUCC         0x53554343 // "SUCC"
#define LOG_MAGIC_FAIL         0x4641494C // "FAIL"

// ----------------------------------------------------------------------------
// RDM6300 RFID UART Functions
// ----------------------------------------------------------------------------
static inline int rdm_getc_nonblock(void) {
    uint32_t d = REG_RDM_UART_DAT;
    if (d == 0xFFFFFFFF) return -1;
    return (int)(d & 0xFF);
}

// Global storage for the last valid scanned RFID tag (10 hex characters)
static char last_tag_hex[11] = "0000000000";
static uint32_t tag_word_hi = 0; // Top 8 bits of tag UID
static uint32_t tag_word_lo = 0; // Low 32 bits of tag UID
static bool tag_available = false;

// Hex char to nibble
static int hex2val(char c) {
    if (c >= '0' && c <= '9') return c - '0';
    if (c >= 'A' && c <= 'F') return c - 'A' + 10;
    if (c >= 'a' && c <= 'f') return c - 'a' + 10;
    return -1;
}

// Poll RDM6300 receiver for a 14-byte frame:
// Format: [0x02] [10 ASCII Hex UID] [2 ASCII Hex Checksum] [0x03]
static void poll_rdm6300(void) {
    static char frame[14];
    static int idx = 0;

    int c = rdm_getc_nonblock();
    while (c >= 0) {
        if (c == 0x02) {
            // Start of frame
            idx = 0;
            frame[idx++] = (char)c;
        } else if (idx > 0 && idx < 14) {
            frame[idx++] = (char)c;
            if (idx == 14) {
                // Verify End-of-Frame
                if (frame[13] == 0x03) {
                    // Calculate XOR checksum of 5 bytes (10 hex chars)
                    uint8_t calc_csum = 0;
                    bool valid_hex = true;
                    for (int b = 0; b < 5; b++) {
                        int h1 = hex2val(frame[1 + b * 2]);
                        int h2 = hex2val(frame[1 + b * 2 + 1]);
                        if (h1 < 0 || h2 < 0) {
                            valid_hex = false;
                            break;
                        }
                        calc_csum ^= (uint8_t)((h1 << 4) | h2);
                    }

                    int c1 = hex2val(frame[11]);
                    int c2 = hex2val(frame[12]);
                    uint8_t frame_csum = (uint8_t)((c1 << 4) | c2);

                    if (valid_hex && (calc_csum == frame_csum)) {
                        // Valid card! Copy to last_tag_hex
                        for (int k = 0; k < 10; k++) {
                            last_tag_hex[k] = frame[1 + k];
                        }
                        last_tag_hex[10] = '\0';
                        tag_available = true;

                        // Parse into 32-bit words for Flash storage
                        tag_word_hi = (uint32_t)((hex2val(last_tag_hex[0]) << 4) | hex2val(last_tag_hex[1]));
                        tag_word_lo = 0;
                        for (int k = 2; k < 10; k++) {
                            tag_word_lo = (tag_word_lo << 4) | (uint32_t)hex2val(last_tag_hex[k]);
                        }

                        // Blink LED on card detect
                        REG_GPIO_LEDS |= 0x0004;
                    }
                }
                idx = 0;
            }
        } else {
            idx = 0;
        }
        c = rdm_getc_nonblock();
    }
}

// ----------------------------------------------------------------------------
// SPI Flash Operations via MMIO Controller
// ----------------------------------------------------------------------------
static void flash_wait_ready(void) {
    while (REG_FLASH_STATUS & 0x01) {
        // Busy wait until flash controller completes SPI transaction
    }
}

static uint32_t flash_read_word(uint32_t addr) {
    flash_wait_ready();
    REG_FLASH_ADDR = addr;
    REG_FLASH_CTRL = (FLASH_OP_READ << 1) | 0x01; // Trigger Read
    flash_wait_ready();
    return REG_FLASH_RDATA;
}

static void flash_write_word(uint32_t addr, uint32_t data) {
    flash_wait_ready();
    REG_FLASH_ADDR = addr;
    REG_FLASH_WDATA = data;
    REG_FLASH_CTRL = (FLASH_OP_WRITE << 1) | 0x01; // Trigger Page Program / Write
    flash_wait_ready();
}

static uint32_t flash_read_sr(void) {
    flash_wait_ready();
    REG_FLASH_CTRL = (FLASH_OP_RDSR << 1) | 0x01; // Trigger RDSR
    flash_wait_ready();
    return REG_FLASH_RDATA & 0xFF;
}

static uint32_t flash_read_id(void) {
    flash_wait_ready();
    REG_FLASH_CTRL = (FLASH_OP_RDID << 1) | 0x01; // Trigger RDID
    flash_wait_ready();
    return REG_FLASH_RDATA & 0xFFFFFF;
}

static void flash_erase_sector(uint32_t addr) {
    flash_wait_ready();
    REG_FLASH_ADDR = addr;
    REG_FLASH_CTRL = (FLASH_OP_SECTOR_ERASE << 1) | 0x01; // Trigger Sector Erase (64KB)
    flash_wait_ready();
}

// ----------------------------------------------------------------------------
// Multi-Tag Storage Functions
// ----------------------------------------------------------------------------
// Check if a tag is already present in Flash. Returns slot index (0..255) if found, or -1.
static int find_tag_slot(uint32_t hi, uint32_t lo) {
    for (int slot = 0; slot < MAX_TAG_SLOTS; slot++) {
        uint32_t addr = USER_FLASH_ADDR + (uint32_t)(slot * FLASH_SLOT_SIZE);
        uint32_t magic = flash_read_word(addr);
        if (magic == 0xFFFFFFFF) {
            return -1; // Empty slot reached; stop searching
        }
        if (magic == FLASH_RECORD_MAGIC) {
            uint32_t s_hi = flash_read_word(addr + 4);
            uint32_t s_lo = flash_read_word(addr + 8);
            if (s_hi == hi && s_lo == lo) {
                return slot; // Match found!
            }
        }
    }
    return -1;
}

// Find next available empty slot (Word 0 == 0xFFFFFFFF). Returns slot index, or -1 if full.
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

// Save tag to next empty slot in Flash without erasing earlier slots.
// Return codes:
//   1: Successfully saved new tag to *out_slot
//   2: Tag already exists in Flash at *out_slot
//  -1: Flash storage is full (all slots used)
//  -2: Flash write verification failed
//   0: No valid tag available to save
static int save_tag_to_flash(int *out_slot) {
    if (!tag_available) return 0;

    // Check duplicate
    int exist = find_tag_slot(tag_word_hi, tag_word_lo);
    if (exist >= 0) {
        *out_slot = exist;
        return 2;
    }

    // Find free slot
    int slot = find_empty_slot();
    if (slot < 0) {
        return -1;
    }

    uint32_t addr = USER_FLASH_ADDR + (uint32_t)(slot * FLASH_SLOT_SIZE);

    REG_GPIO_LEDS |= 0x0008; // Flash active LED

    // Write 16-byte record into slot without sector erase
    flash_write_word(addr + 0, FLASH_RECORD_MAGIC);
    flash_write_word(addr + 4, tag_word_hi);
    flash_write_word(addr + 8, tag_word_lo);
    flash_write_word(addr + 12, tag_word_hi ^ tag_word_lo);

    REG_GPIO_LEDS &= ~0x0008;

    // Verify written data
    uint32_t v_magic = flash_read_word(addr + 0);
    uint32_t v_hi    = flash_read_word(addr + 4);
    uint32_t v_lo    = flash_read_word(addr + 8);

    if (v_magic == FLASH_RECORD_MAGIC && v_hi == tag_word_hi && v_lo == tag_word_lo) {
        *out_slot = slot;
        return 1;
    }

    return -2;
}

// ----------------------------------------------------------------------------
// Access Log Storage Functions (Sector 49: 0x310000)
// ----------------------------------------------------------------------------
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

// ----------------------------------------------------------------------------
// Main Firmware Entry Point & Command Loop
// ----------------------------------------------------------------------------
int main(void) {
    // Set status LED: bit 0 alive
    REG_GPIO_LEDS = 0x0001;

    uart_puts("\n==================================================\n");
    uart_puts("  PicoRV32 RISC-V SoC: RDM6300 & SPI Flash Ready\n");
    uart_puts("==================================================\n");

    while (1) {
        // Poll RDM6300 RFID reader for incoming tag frames
        poll_rdm6300();

        // Check for commands from Host PC
        int cmd = uart_getc_nonblock();
        if (cmd < 0) continue;

        switch ((char)cmd) {
            case 'P': // Ping command
            case 'p':
                uart_puts("PONG: PicoRV32 Active\n");
                break;

            case 'R': // Query RFID Tag
            case 'r':
                if (tag_available) {
                    uart_puts("TAG:");
                    uart_puts(last_tag_hex);
                    uart_puts("\n");
                } else {
                    uart_puts("ERR:NO_TAG\n");
                }
                break;

            case 'W': // Write current tag into SPI Flash
            case 'w': {
                int slot = -1;
                int res = save_tag_to_flash(&slot);
                if (res == 1) {
                    uart_puts("OK:SAVED:SLOT:");
                    uart_putdec(slot);
                    uart_puts(":");
                    uart_puts(last_tag_hex);
                    uart_puts("\n");
                    REG_GPIO_LEDS |= 0x0010; // Save success LED
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

            case 'N': // New / Manual Tag input from PC: "N010054DA65\n"
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

            case 'D': // Dump Flash words 0x300000..0x30001C
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

            case 'F': // Read all stored tags from SPI Flash
            case 'f': {
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

            case 'E': // Erase Flash sector
            case 'e':
                REG_GPIO_LEDS |= 0x0008;
                flash_erase_sector(USER_FLASH_ADDR);
                REG_GPIO_LEDS &= ~0x0008;
                uart_puts("OK:SECTOR_ERASED\n");
                break;

            case 'V': // Virtual Scan: V<10-char-hex>
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

                    int tag_slot = find_tag_slot(v_hi, v_lo);
                    bool is_granted = (tag_slot >= 0);

                    // Append to access log in Flash Sector 49 (0x310000)
                    int log_slot = append_access_log(is_granted, v_hi, v_lo);

                    if (is_granted) {
                        REG_GPIO_LEDS |= 0x0004; // Green LED indication
                        uart_puts("ACCESS:GRANTED:SLOT:");
                        uart_putdec((uint32_t)tag_slot);
                        uart_puts(":");
                        uart_puts(vtag);
                        uart_puts(":LOG:");
                        uart_putdec((uint32_t)(log_slot >= 0 ? log_slot : 0));
                        uart_puts("\n");
                    } else {
                        REG_GPIO_LEDS |= 0x0002; // Warning LED indication
                        uart_puts("ACCESS:DENIED:");
                        uart_puts(vtag);
                        uart_puts(":LOG:");
                        uart_putdec((uint32_t)(log_slot >= 0 ? log_slot : 0));
                        uart_puts("\n");
                    }
                } else {
                    uart_puts("ERR:INVALID_LENGTH\n");
                }
                break;
            }

            case 'L': // Read Access Logs from Flash Sector 49 (0x310000)
            case 'l': {
                int count = 0;
                int succ_count = 0;
                int fail_count = 0;
                uart_puts("LOGS_START\n");
                for (int slot = 0; slot < MAX_LOG_SLOTS; slot++) {
                    uint32_t addr = LOG_FLASH_ADDR + (uint32_t)(slot * LOG_SLOT_SIZE);
                    uint32_t magic = flash_read_word(addr);
                    if (magic == 0xFFFFFFFF) {
                        break; // End of log list
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

            case 'X': // Erase Access Logs Sector (0x310000)
            case 'x':
                REG_GPIO_LEDS |= 0x0008;
                flash_erase_sector(LOG_FLASH_ADDR);
                REG_GPIO_LEDS &= ~0x0008;
                uart_puts("OK:LOGS_ERASED\n");
                break;

            case 'S': // Hardware Status
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

            case '?': // Help
                uart_puts("CMDS: P(Ping) R(ReadTag) W(WriteFlash) F(ReadFlash) E(EraseFlash) S(Status)\n");
                break;

            default:
                break;
        }
    }

    return 0;
}
