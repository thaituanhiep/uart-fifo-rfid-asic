// ============================================================================
// File: firmware/app/access_control.h
// Project: rdm6300-picorv32-rom-data
// Description: RFID Access Control Business Logic & Authorization Engine
// ============================================================================

#ifndef APP_ACCESS_CONTROL_H
#define APP_ACCESS_CONTROL_H

#include <stdint.h>
#include <stdbool.h>

// Initialize Access Control Subsystem
void access_control_init(void);

// Non-blocking background task: Polls RFID UART, feeds parser & processes card
void access_control_poll(void);

// Process and verify an RFID card (Flash lookup, Logging, LED drive, UART report)
void access_control_process_card(const char *tag_hex, uint32_t hi, uint32_t lo);

// Query state of last authenticated/scanned tag
bool access_control_is_tag_available(void);
void access_control_get_last_tag(char *out_hex10, uint32_t *out_hi, uint32_t *out_lo);
void access_control_set_current_tag(const char *tag_hex, uint32_t hi, uint32_t lo);

#endif // APP_ACCESS_CONTROL_H
