// ============================================================================
// File: firmware/main.c
// Project: rdm6300-picorv32-rom-data
// Target: PicoRV32 RISC-V SoC (Basys 3 FPGA / ASIC)
// Description: Main Firmware Application Coordinator & Host Command Dispatcher
// ============================================================================

#include "soc_regs.h"
#include "hex_utils.h"
#include "uart.h"
#include "flash.h"
#include "access_control.h"

// ----------------------------------------------------------------------------
// Minimal C Standard Library Hooks (Required for freestanding environment)
// ----------------------------------------------------------------------------
void *memcpy(void *dest, const void *src, unsigned int n) {
    return soc_memcpy(dest, src, n);
}

void *memset(void *s, int c, unsigned int n) {
    return soc_memset(s, c, n);
}

// ----------------------------------------------------------------------------
// Local Host Dispatch Helpers
// ----------------------------------------------------------------------------
static void report_tag_save_result(int res, int slot, const char *tag_hex, const char *succ_msg) {
    if (res == 1) {
        uart_print_slot_tag(succ_msg, slot, tag_hex);
        REG_GPIO_LEDS |= 0x0010;
    } else if (res == 2) {
        uart_print_slot_tag("INFO:EXISTS:SLOT", slot, tag_hex);
    } else if (res == -1) {
        uart_puts("ERR:FLASH_FULL\n");
    } else {
        uart_puts("ERR:FLASH_WRITE_FAIL\n");
    }
}

static void print_soc_status(bool has_tag) {
    uint32_t fid = flash_read_id();
    uint32_t fsr = flash_read_sr();
    uart_puts("STATUS: FlashID=");
    uart_puthex32(fid);
    uart_puts(", FlashSR=");
    uart_puthex32(fsr);
    uart_puts(", LEDs=");
    uart_puthex32(REG_GPIO_LEDS);
    uart_puts(", TagAvailable=");
    uart_putc(has_tag ? '1' : '0');
    uart_puts("\n");
}

// ----------------------------------------------------------------------------
// Host UART Command Processing Dispatcher
// ----------------------------------------------------------------------------
static void process_host_command(char cmd) {
    char cur_tag_hex[11];
    uint32_t cur_hi = 0, cur_lo = 0;
    bool has_tag = access_control_is_tag_available();
    if (has_tag) {
        access_control_get_last_tag(cur_tag_hex, &cur_hi, &cur_lo);
    }

    switch (cmd) {
        // 'P': Ping
        case 'P':
        case 'p':
            uart_puts("PONG: PicoRV32 Active\n");
            break;

        // 'R': Query Last Scanned RFID Tag
        case 'R':
        case 'r':
            if (has_tag) {
                uart_puts("TAG:");
                uart_puts(cur_tag_hex);
                uart_puts("\n");
            } else {
                uart_puts("ERR:NO_TAG\n");
            }
            break;

        // 'W': Write Current Tag into Flash Database
        case 'W':
        case 'w':
            if (!has_tag) {
                uart_puts("ERR:NO_TAG_TO_SAVE\n");
            } else {
                int slot = -1;
                int res = flash_save_tag(cur_hi, cur_lo, &slot);
                report_tag_save_result(res, slot, cur_tag_hex, "OK:SAVED:SLOT");
            }
            break;

        // 'N': Save New / Manual Tag from Host PC (Format: N<10-hex-digits>\n)
        case 'N':
        case 'n': {
            char tag[11];
            uint32_t hi, lo;
            if (uart_read_tag_uid(tag, &hi, &lo, 5000000)) {
                access_control_set_current_tag(tag, hi, lo);
                int slot = -1;
                int res = flash_save_tag(hi, lo, &slot);
                report_tag_save_result(res, slot, tag, "OK:MANUAL_TAG_SAVED:SLOT");
            } else {
                uart_puts("ERR:INVALID_LENGTH\n");
            }
            break;
        }

        // 'D': Dump Raw Flash Memory Words
        case 'D':
        case 'd':
            flash_dump_raw(USER_FLASH_ADDR, 8);
            break;

        // 'F': Read All Authorized Tags from Flash Sector 48
        case 'F':
        case 'f':
            flash_dump_all_tags();
            break;

        // 'E': Erase Authorized Tags Sector (0x300000)
        case 'E':
        case 'e':
            flash_erase_tags_sector();
            uart_puts("OK:SECTOR_ERASED\n");
            break;

        // 'C': Check / Query If Single Tag Exists (Format: C<10-hex-digits>\n)
        case 'C':
        case 'c': {
            char tag[11];
            uint32_t hi, lo;
            if (!uart_read_tag_uid(tag, &hi, &lo, 5000000)) {
                uart_puts("ERR:INVALID_LENGTH\n");
            } else {
                int slot = flash_find_tag(hi, lo);
                if (slot >= 0) {
                    uart_print_slot_tag("OK:TAG_FOUND:SLOT", slot, tag);
                } else {
                    uart_puts("ERR:TAG_NOT_FOUND\n");
                }
            }
            break;
        }

        // 'K': Kill / Delete Single Tag from Flash (Format: K<10-hex-digits>\n)
        case 'K':
        case 'k': {
            char tag[11];
            uint32_t hi, lo;
            if (!uart_read_tag_uid(tag, &hi, &lo, 5000000)) {
                uart_puts("ERR:INVALID_LENGTH\n");
            } else {
                int slot = flash_find_tag(hi, lo);
                if (slot >= 0) {
                    flash_delete_tag(slot);
                    uart_print_slot_tag("OK:TAG_DELETED:SLOT", slot, tag);
                } else {
                    uart_puts("ERR:TAG_NOT_FOUND\n");
                }
            }
            break;
        }

        // 'V': Virtual Scan Simulation (Format: V<10-hex-digits>\n)
        case 'V':
        case 'v': {
            char tag[11];
            uint32_t hi, lo;
            if (uart_read_tag_uid(tag, &hi, &lo, 100000)) {
                access_control_process_card(tag, hi, lo);
            } else {
                uart_puts("ERR:INVALID_LENGTH\n");
            }
            break;
        }

        // 'L': Read Access Logs from Flash Sector 49 (0x310000)
        case 'L':
        case 'l':
            flash_dump_all_logs();
            break;

        // 'X': Erase Access Logs Sector (0x310000)
        case 'X':
        case 'x':
            flash_erase_logs_sector();
            uart_puts("OK:LOGS_ERASED\n");
            break;

        // 'S': Query Diagnostic Hardware Status
        case 'S':
        case 's':
            print_soc_status(has_tag);
            break;

        // '?': Help Info
        case '?':
            uart_puts("CMDS: P(Ping) R(ReadTag) W(WriteFlash) F(ReadFlash) E(EraseFlash) S(Status)\n");
            break;

        default:
            break;
    }
}
// ----------------------------------------------------------------------------
// Main Application Bootstrap & Polling Loop
// ----------------------------------------------------------------------------
int main(void) {
    // 1. Initialize Host UART (Clock 50MHz / 9600 Baud = 5208)
    uart_init(5208);

    // 2. Set LED alive indicator (Bit 0 on)
    REG_GPIO_LEDS = 0x0001;

    // 3. Initialize RFID Access Control Subsystem
    access_control_init();

    // 4. Print startup banner over UART
    uart_puts("\n==================================================\n");
    uart_puts("  PicoRV32 RISC-V SoC: RDM6300 & SPI Flash Ready\n");
    uart_puts("==================================================\n");

    // 5. Main Execution Loop
    while (1) {
        // Continuous non-blocking hardware polling & RFID card processing
        access_control_poll();

        // Non-blocking check for incoming command characters from PC Host
        int cmd = uart_getc_nonblock();
        if (cmd >= 0) {
            process_host_command((char)cmd);
        }
    }

    return 0;
}
