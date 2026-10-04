// ============================================================================
// File: firmware/drivers/flash.h
// Project: rdm6300-picorv32-rom-data
// Description: SPI Flash Driver & Flash Data Storage Engine Header
// ============================================================================

#ifndef DRIVER_FLASH_H
#define DRIVER_FLASH_H

#include <stdint.h>
#include <stdbool.h>

// ----------------------------------------------------------------------------
// Primitive SPI Flash Operations (Hardware Interface via spimemio)
// ----------------------------------------------------------------------------
uint32_t flash_read_word(uint32_t addr);
void     flash_write_word(uint32_t addr, uint32_t data);
uint32_t flash_read_sr(void);
uint32_t flash_read_id(void);
void     flash_erase_sector(uint32_t addr);

// ----------------------------------------------------------------------------
// Flash Data Storage Mechanisms: Authorized RFID Tags (Sector 48: 0x300000)
// ----------------------------------------------------------------------------
int  flash_find_tag(uint32_t hi, uint32_t lo);
int  flash_find_empty_tag_slot(void);
int  flash_save_tag(uint32_t hi, uint32_t lo, int *out_slot);
bool flash_delete_tag(int slot);
void flash_erase_tags_sector(void);

// ----------------------------------------------------------------------------
// Flash Data Storage Mechanisms: Access Logs (Sector 49: 0x310000)
// ----------------------------------------------------------------------------
int  flash_find_empty_log_slot(void);
int  flash_append_log(bool success, uint32_t hi, uint32_t lo);
void flash_erase_logs_sector(void);

// ----------------------------------------------------------------------------
// Flash Diagnostic & Reporting Procedures
// ----------------------------------------------------------------------------
void flash_dump_raw(uint32_t addr, int word_count);
void flash_dump_all_tags(void);
void flash_dump_all_logs(void);

#endif // DRIVER_FLASH_H
