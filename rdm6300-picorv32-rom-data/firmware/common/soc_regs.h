// ============================================================================
// File: firmware/common/soc_regs.h
// Project: rdm6300-picorv32-rom-data
// Target: PicoRV32 RISC-V SoC (Basys 3 FPGA / ASIC)
// Description: Peripheral Register Addresses, Flash Partition Map & System Constants
// ============================================================================

#ifndef SOC_REGS_H
#define SOC_REGS_H

#include <stdint.h>
#include <stdbool.h>

// ----------------------------------------------------------------------------
// Memory Mapped Peripheral Base Addresses (from soc_interconnect.v)
// ----------------------------------------------------------------------------
// Slave 2: RFID Reader UART Peripheral (0x1000_0000 - 0x1000_0004)
#define REG_RFID_UART_DIV  (*(volatile uint32_t*)0x10000000) // Baud rate divider (Clock / 9600 = 5208)
#define REG_RFID_UART_DAT  (*(volatile uint32_t*)0x10000004) // Read: RX FIFO (0xFFFFFFFF = empty)

// Slave 3: Host PC UART Controller with FIFOs (0x3000_0000 - 0x3000_0004)
#define REG_PC_UART_DIV    (*(volatile uint32_t*)0x30000000) // Baud rate divider (Clock / 9600 = 5208)
#define REG_PC_UART_DAT    (*(volatile uint32_t*)0x30000004) // Read: RX FIFO, Write: TX FIFO

// Slave 4: GPIO LEDs (0x4000_0000)
#define REG_GPIO_LEDS      (*(volatile uint32_t*)0x40000000) // Bit 0: Alive, Bit 1: Warn, Bit 2: Granted, Bit 3: Flash, Bit 4: Save Success

// ----------------------------------------------------------------------------
// SPI Flash Memory Partition Layout
// ----------------------------------------------------------------------------
// Tag Database Sector (Sector 48: 0x300000, 64KB)
#define USER_FLASH_ADDR        0x300000
#define FLASH_SLOT_SIZE        16        // 16 bytes per tag record
#define MAX_TAG_SLOTS          4096      // 4096 records max
#define FLASH_RECORD_MAGIC     0x52464944 // "RFID"

// Access Log Sector (Sector 49: 0x310000, 64KB)
#define LOG_FLASH_ADDR         0x310000  // Base address for access logs
#define LOG_SLOT_SIZE          16        // 16 bytes per log record
#define MAX_LOG_SLOTS          512       // 512 log records max (8KB)
#define LOG_MAGIC_SUCC         0x53554343 // "SUCC"
#define LOG_MAGIC_FAIL         0x4641494C // "FAIL"

#endif // SOC_REGS_H
