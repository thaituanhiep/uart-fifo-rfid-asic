// ============================================================================
// File: host/main.c
// Project: rdm6300-picorv32-rom-data
// Target: Host PC (Windows / Linux)
// Description: Host PC C software communicating with Basys 3 FPGA over UART.
//              Sends user commands to PicoRV32 RISC-V SoC to:
//              - Query scanned RFID tags from RDM6300
//              - Input new RFID tags manually from keyboard and save to Flash
//              - Save RFID tags into Basys 3 SPI Flash memory
//              - Read back stored RFID tags from SPI Flash memory
//              - Erase Flash sector
//              - Check hardware status and connection
// ============================================================================

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <stdint.h>
#include <ctype.h>

#ifdef _WIN32
    #include <windows.h>
    typedef HANDLE serial_port_t;
    #define INVALID_PORT_HANDLE INVALID_HANDLE_VALUE
#else
    #include <fcntl.h>
    #include <termios.h>
    #include <unistd.h>
    typedef int serial_port_t;
    #define INVALID_PORT_HANDLE -1
#endif

// ----------------------------------------------------------------------------
// Serial Port Abstraction
// ----------------------------------------------------------------------------
serial_port_t open_serial(const char *port_name, int baudrate) {
#ifdef _WIN32
    char full_name[64];
    snprintf(full_name, sizeof(full_name), "\\\\.\\%s", port_name);

    HANDLE hSerial = CreateFileA(full_name, GENERIC_READ | GENERIC_WRITE,
                                 0, NULL, OPEN_EXISTING, 0, NULL);
    if (hSerial == INVALID_HANDLE_VALUE) {
        return INVALID_HANDLE_VALUE;
    }

    DCB dcbSerialParams = {0};
    dcbSerialParams.DCBlength = sizeof(dcbSerialParams);

    if (!GetCommState(hSerial, &dcbSerialParams)) {
        CloseHandle(hSerial);
        return INVALID_HANDLE_VALUE;
    }

    dcbSerialParams.BaudRate = baudrate;
    dcbSerialParams.ByteSize = 8;
    dcbSerialParams.StopBits = ONESTOPBIT;
    dcbSerialParams.Parity   = NOPARITY;
    dcbSerialParams.fDtrControl = DTR_CONTROL_ENABLE;

    if (!SetCommState(hSerial, &dcbSerialParams)) {
        CloseHandle(hSerial);
        return INVALID_HANDLE_VALUE;
    }

    COMMTIMEOUTS timeouts = {0};
    timeouts.ReadIntervalTimeout         = 50;
    timeouts.ReadTotalTimeoutConstant    = 1000;
    timeouts.ReadTotalTimeoutMultiplier  = 10;
    timeouts.WriteTotalTimeoutConstant   = 50;
    timeouts.WriteTotalTimeoutMultiplier = 10;

    SetCommTimeouts(hSerial, &timeouts);
    return hSerial;
#else
    int fd = open(port_name, O_RDWR | O_NOCTTY | O_NDELAY);
    if (fd == -1) return -1;

    struct termios options;
    tcgetattr(fd, &options);
    cfsetispeed(&options, B9600);
    cfsetospeed(&options, B9600);
    options.c_cflag |= (CLOCAL | CREAD);
    options.c_cflag &= ~PARENB;
    options.c_cflag &= ~CSTOPB;
    options.c_cflag &= ~CSIZE;
    options.c_cflag |= CS8;
    options.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG);
    options.c_iflag &= ~(IXON | IXOFF | IXANY);
    options.c_oflag &= ~OPOST;
    tcsetattr(fd, TCSANOW, &options);
    return fd;
#endif
}

void close_serial(serial_port_t port) {
#ifdef _WIN32
    if (port != INVALID_HANDLE_VALUE) CloseHandle(port);
#else
    if (port >= 0) close(port);
#endif
}

void flush_serial(serial_port_t port) {
#ifdef _WIN32
    if (port != INVALID_HANDLE_VALUE) {
        PurgeComm(port, PURGE_RXCLEAR | PURGE_TXCLEAR);
    }
#else
    if (port >= 0) {
        tcflush(port, TCIOFLUSH);
    }
#endif
}

bool write_serial(serial_port_t port, const char *buf, int len) {
#ifdef _WIN32
    DWORD written = 0;
    return WriteFile(port, buf, len, &written, NULL) && ((int)written == len);
#else
    int written = write(port, buf, len);
    return (written == len);
#endif
}

int read_line_serial(serial_port_t port, char *buf, int max_len, int timeout_ms) {
    int count = 0;
    memset(buf, 0, max_len);

#ifdef _WIN32
    DWORD bytes_read = 0;
    char c;
    DWORD start = GetTickCount();

    while (count < max_len - 1) {
        if (ReadFile(port, &c, 1, &bytes_read, NULL) && bytes_read > 0) {
            if (c == '\r') continue;
            if (c == '\n') break;
            buf[count++] = c;
        } else {
            if (GetTickCount() - start > (DWORD)timeout_ms) break;
            Sleep(5);
        }
    }
#else
    char c;
    while (count < max_len - 1) {
        int r = read(port, &c, 1);
        if (r > 0) {
            if (c == '\r') continue;
            if (c == '\n') break;
            buf[count++] = c;
        } else {
            usleep(5000);
        }
    }
#endif

    buf[count] = '\0';
    return count;
}

// ----------------------------------------------------------------------------
// Helper: Parse RFID card input (Prioritizing 10 decimal digits printed on card)
// ----------------------------------------------------------------------------
static bool parse_card_input(const char *input, char *out_hex10) {
    if (!input || !out_hex10) return false;

    // Skip leading whitespace
    while (isspace((unsigned char)*input)) input++;
    if (*input == '\0') return false;

    // Make a clean copy without trailing whitespace
    char clean[128];
    strncpy(clean, input, sizeof(clean) - 1);
    clean[sizeof(clean) - 1] = '\0';
    int clen = (int)strlen(clean);
    while (clen > 0 && (clean[clen - 1] == '\r' || clean[clen - 1] == '\n' || isspace((unsigned char)clean[clen - 1]))) {
        clean[--clen] = '\0';
    }
    if (clen == 0) return false;

    // 1. Primary: 10-digit decimal number printed on card (e.g. 0007508976 or 7508976)
    bool is_all_digits = true;
    for (int i = 0; i < clen; i++) {
        if (!isdigit((unsigned char)clean[i])) {
            is_all_digits = false;
            break;
        }
    }
    if (is_all_digits && clen >= 1 && clen <= 10) {
        unsigned long num = strtoul(clean, NULL, 10);
        snprintf(out_hex10, 11, "00%08X", (unsigned int)num);
        return true;
    }

    // 2. Fallback: Both numbers printed on card / Wiegand (e.g. "0007508976  114,37872" or "114,37872")
    const char *comma = strchr(clean, ',');
    if (!comma) comma = strchr(clean, '.');
    if (comma) {
        const char *fc_end = comma;
        while (fc_end > clean && isspace((unsigned char)*(fc_end - 1))) fc_end--;
        const char *fc_start = fc_end;
        while (fc_start > clean && isdigit((unsigned char)*(fc_start - 1))) fc_start--;

        if (fc_start < fc_end) {
            unsigned int fc = 0, id = 0;
            if (sscanf(fc_start, "%u", &fc) == 1 && sscanf(comma + 1, "%u", &id) == 1) {
                uint32_t val = ((fc & 0xFF) << 16) | (id & 0xFFFF);
                snprintf(out_hex10, 11, "00%08X", (unsigned int)val);
                return true;
            }
        }
    }

    // 3. Fallback: 10-character Hex UID (e.g. 010054DA65, 00007293F0)
    if (clen == 10) {
        bool is_all_hex = true;
        for (int i = 0; i < 10; i++) {
            char c = clean[i];
            if (!((c >= '0' && c <= '9') || (c >= 'A' && c <= 'F') || (c >= 'a' && c <= 'f'))) {
                is_all_hex = false;
                break;
            }
        }
        if (is_all_hex) {
            for (int i = 0; i < 10; i++) {
                char c = clean[i];
                if (c >= 'a' && c <= 'f') c = c - 'a' + 'A';
                out_hex10[i] = c;
            }
            out_hex10[10] = '\0';
            return true;
        }
    }

    return false;
}

// ----------------------------------------------------------------------------
// User Menu & Application Logic
// ----------------------------------------------------------------------------
void print_menu(void) {
    printf("\n===============================================================\n");
    printf("     RDM6300 RFID - PICORV32 - BASYS 3 SPI FLASH MANAGER      \n");
    printf("===============================================================\n");
    printf("  [1]  Ping Hardware (Kiem tra ket noi PicoRV32)\n");
    printf("  [2]  Input & Save New RFID Tag (Nhap 10 so in tren the de luu Flash)\n");
    printf("  [3]  Check RFID Tag in Flash (Kiem tra the da co trong Flash chua)\n");
    printf("  [4]  Read All RFID Tags from Flash (Doc toan bo the tu SPI Flash)\n");
    printf("  [5]  Virtual Scan: By Decimal (Quet the ao: Nhap 10 so in tren the)\n");
    printf("  [6]  Virtual Scan: By Hex (Quet the ao: Nhap ma Hex 10 ky tu)\n");
    printf("  [7]  View Access Logs from Flash (Xem nhat ky quet the tu Flash)\n");
    printf("  [8]  Erase Access Logs (Xoa nhat ky quet the trong Flash 0x310000)\n");
    printf("  [9]  Erase Authorized Tags Sector (Xoa the da cap phep 0x300000)\n");
    printf("  [10] Get SoC Status (Xem trang thai LED, Flash, PicoRV32)\n");
    printf("  [0]  Exit (Thoat)\n");
    printf("---------------------------------------------------------------\n");
    printf("Lua chon cua ban [0-10]: ");
}

int main(int argc, char *argv[]) {
    char port_name[32] = "COM3";

    if (argc > 1) {
        strncpy(port_name, argv[1], sizeof(port_name) - 1);
    } else {
        printf("Nhap cong COM noi voi Basys 3 FPGA (mac dinh: COM3): ");
        char input[32];
        if (fgets(input, sizeof(input), stdin)) {
            char *newline = strchr(input, '\n');
            if (newline) *newline = '\0';
            if (strlen(input) > 0) {
                strncpy(port_name, input, sizeof(port_name) - 1);
            }
        }
    }

    printf("\nDang ket noi toi %s voi baudrate 9600 bps...\n", port_name);
    serial_port_t port = open_serial(port_name, 9600);

    if (port == INVALID_PORT_HANDLE) {
        printf("[ERROR] Khong the mo cong serial %s!\n", port_name);
        printf("Vui long kiem tra lai cap ket noi Basys 3 va Device Manager.\n");
        return 1;
    }

    printf("[SUCCESS] Da ket noi thanh cong voi Basys 3 tren %s!\n", port_name);

    char resp[256];
    int choice = -1;

    while (1) {
        print_menu();
        char menu_line[64];
        if (!fgets(menu_line, sizeof(menu_line), stdin)) {
            break;
        }
        if (sscanf(menu_line, "%d", &choice) != 1) {
            choice = -1;
        }

        if (choice == 0) {
            printf("\nThoat chuong trinh. Tam biet!\n");
            break;
        }

        switch (choice) {
            case 1: // Ping
                printf("\n-> Gui lenh 'P' (Ping)...\n");
                flush_serial(port);
                write_serial(port, "P\n", 2);
                if (read_line_serial(port, resp, sizeof(resp), 1500) > 0) {
                    printf("[PHAN HOI] %s\n", resp);
                } else {
                    printf("[CANH BAO] Khong nhan duoc phan hoi tu PicoRV32 (Timeout)!\n");
                }
                break;

            case 2: { // Input & Save New RFID Tag (10 digits printed on card)
                char custom_tag[128];
                printf("\nNhap 10 chu so in tren the RFID (vi du: 0007508976): ");
                if (fgets(custom_tag, sizeof(custom_tag), stdin)) {
                    char *nl = strchr(custom_tag, '\n');
                    if (nl) *nl = '\0';
                    nl = strchr(custom_tag, '\r');
                    if (nl) *nl = '\0';

                    char hex_tag[11];
                    if (!parse_card_input(custom_tag, hex_tag)) {
                        printf("[LOI] Vui long nhap 10 chu so in tren the RFID (vi du: 0007508976)!\n");
                        break;
                    }
                    uint32_t val = (uint32_t)strtoul(hex_tag + 2, NULL, 16);
                    unsigned int fc = (val >> 16) & 0xFF;
                    unsigned int id = val & 0xFFFF;
                    printf("-> Da nhan dien the hop le:\n");
                    printf("   + So in tren the        : %010u  (%03u,%05u)\n", (unsigned int)val, fc, id);
                    printf("   + Ma Hex (UID 10 ky tu) : %s\n", hex_tag);

                    char send_buf[32];
                    snprintf(send_buf, sizeof(send_buf), "N%s\n", hex_tag);
                    printf("-> Gui ma the %s toi PicoRV32 de luu vao Flash...\n", hex_tag);
                    flush_serial(port);
                    write_serial(port, send_buf, strlen(send_buf));
                    bool done = false;
                    while (read_line_serial(port, resp, sizeof(resp), 2500) > 0) {
                        if (strstr(resp, "OK:MANUAL_TAG_SAVED:SLOT:")) {
                            int slot = 0;
                            char tag[32] = "";
                            sscanf(resp, "OK:MANUAL_TAG_SAVED:SLOT:%d:%31s", &slot, tag);
                            printf("[THANH CONG] The moi %s (%010u) da duoc luu vao Flash Basys 3 tai Slot #%d (Dia chi: 0x%06X)!\n",
                                   tag, (unsigned int)val, slot, 0x300000 + slot * 16);
                            done = true;
                            break;
                        } else if (strstr(resp, "INFO:EXISTS:SLOT:")) {
                            int slot = 0;
                            char tag[32] = "";
                            sscanf(resp, "INFO:EXISTS:SLOT:%d:%31s", &slot, tag);
                            printf("[THONG BAO] The %s DA TON TAI truoc do trong Flash tai Slot #%d!\n", tag, slot);
                            done = true;
                            break;
                        } else if (strstr(resp, "FLASH_FULL")) {
                            printf("[LOI] Bo nho Flash da day (toi da 256 the)! Vui long chon [5] de xoa neu can.\n");
                            done = true;
                            break;
                        } else if (strstr(resp, "FAIL") || strstr(resp, "ERR:")) {
                            printf("[LOI] %s\n", resp);
                            done = true;
                            break;
                        } else {
                            printf("[PHAN HOI] %s\n", resp);
                        }
                    }
                    if (!done) {
                        printf("[CANH BAO] Timeout khi luu the moi vao Flash!\n");
                    }
                }
                break;
            }

            case 3: { // Check RFID Tag in Flash
                char custom_tag[128];
                printf("\nNhap 10 chu so in tren the can kiem tra (vi du: 0007508976): ");
                if (fgets(custom_tag, sizeof(custom_tag), stdin)) {
                    char *nl = strchr(custom_tag, '\n');
                    if (nl) *nl = '\0';
                    nl = strchr(custom_tag, '\r');
                    if (nl) *nl = '\0';

                    char hex_tag[11];
                    if (!parse_card_input(custom_tag, hex_tag)) {
                        printf("[LOI] Vui long nhap 10 chu so in tren the RFID (vi du: 0007508976)!\n");
                        break;
                    }
                    uint32_t val = (uint32_t)strtoul(hex_tag + 2, NULL, 16);
                    unsigned int fc = (val >> 16) & 0xFF;
                    unsigned int id = val & 0xFFFF;
                    printf("-> Kiem tra the:\n");
                    printf("   + So in tren the        : %010u  (%03u,%05u)\n", (unsigned int)val, fc, id);
                    printf("   + Ma Hex (UID 10 ky tu) : %s\n", hex_tag);
                    printf("-> Dang tra cuu trong SPI Flash Basys 3...\n");

                    flush_serial(port);
                    write_serial(port, "F\n", 2);

                    bool found = false;
                    int found_slot = -1;
                    int total_tags = 0;
                    bool empty = false;

                    while (read_line_serial(port, resp, sizeof(resp), 2000) > 0) {
                        if (strstr(resp, "EMPTY")) {
                            empty = true;
                            break;
                        }
                        if (strstr(resp, "TAG_ITEM:")) {
                            int slot = 0;
                            char tag[32] = "";
                            sscanf(resp, "TAG_ITEM:%d:%31s", &slot, tag);
                            total_tags++;
                            if (strcasecmp(tag, hex_tag) == 0) {
                                found = true;
                                found_slot = slot;
                            }
                        }
                        if (strstr(resp, "TAGS_END")) {
                            break;
                        }
                    }

                    printf("---------------------------------------------------------------\n");
                    if (empty || total_tags == 0) {
                        printf("[KET QUA] Flash hien dang TRONG (Chua co the nao duoc luu)!\n");
                        printf("         -> The %010u (UID: %s) CHUA CO trong Flash.\n", (unsigned int)val, hex_tag);
                    } else if (found) {
                        printf("[KET QUA] [DA TON TAI] The %010u (UID: %s) DA CO trong Flash!\n",
                               (unsigned int)val, hex_tag);
                        printf("         - Vi tri luu tru : Slot #%d\n", found_slot);
                        printf("         - Dia chi Flash  : 0x%06X\n", 0x300000 + found_slot * 16);
                    } else {
                        printf("[KET QUA] [CHUA CO] The %010u (UID: %s) CHUA CO trong Flash.\n",
                               (unsigned int)val, hex_tag);
                        printf("         (Hien tai Flash dang luu %d the khac. Ban co the chon [2] de luu the nay).\n", total_tags);
                    }
                    printf("---------------------------------------------------------------\n");
                }
                break;
            }

            case 4: { // Read all stored tags from Flash
                printf("\n-> Gui lenh 'F' (Doc toan bo the da luu tu SPI Flash Basys 3)...\n");
                flush_serial(port);
                write_serial(port, "F\n", 2);
                int tag_count = 0;
                while (read_line_serial(port, resp, sizeof(resp), 2000) > 0) {
                    if (strstr(resp, "TAGS_START")) {
                        printf("\n===================================================================================\n");
                        printf("                      DANH SACH THE RFID TRONG SPI FLASH BASYS 3                   \n");
                        printf("===================================================================================\n");
                        continue;
                    }
                    if (strstr(resp, "TAG_ITEM:")) {
                        int slot = 0;
                        char tag[32] = "";
                        sscanf(resp, "TAG_ITEM:%d:%31s", &slot, tag);
                        tag_count++;
                        uint32_t val = (uint32_t)strtoul(tag + 2, NULL, 16);
                        unsigned int fc = (val >> 16) & 0xFF;
                        unsigned int id = val & 0xFFFF;
                        printf("  [%2d] UID: %s | In tren the: %010u (%03u,%05u) | Slot #%d (0x%06X)\n",
                               tag_count, tag, (unsigned int)val, fc, id, slot, 0x300000 + slot * 16);
                        continue;
                    }
                    if (strstr(resp, "TAGS_TOTAL:")) {
                        int total = 0;
                        sscanf(resp, "TAGS_TOTAL:%d", &total);
                        printf("-----------------------------------------------------------------------------------\n");
                        printf("[THANH CONG] Tong so the RFID da luu trong Flash: %d the\n", total);
                        continue;
                    }
                    if (strstr(resp, "TAGS_END")) {
                        break;
                    }
                    if (strstr(resp, "EMPTY")) {
                        printf("[FLASH TRONG] Chua co the RFID nao duoc luu trong Flash (hoac da bi xoa)!\n");
                        break;
                    }
                    if (strncmp(resp, "FLASH_TAG:", 10) == 0) {
                        printf("[THANH CONG] The RFID doc tu SPI Flash: %s\n", resp + 10);
                        break;
                    }
                }
                break;
            }

            case 5: { // Virtual Scan: By Decimal
                char custom_tag[128];
                printf("\n--- QUET THE RFID AO (NHAP 10 SO IN TREN THE) ---\n");
                printf("Nhap 10 chu so in tren the (vi du: 0007508976): ");
                if (fgets(custom_tag, sizeof(custom_tag), stdin)) {
                    char *nl = strchr(custom_tag, '\n');
                    if (nl) *nl = '\0';
                    nl = strchr(custom_tag, '\r');
                    if (nl) *nl = '\0';

                    char hex_tag[11];
                    if (!parse_card_input(custom_tag, hex_tag)) {
                        printf("[LOI] Vui long nhap dung 10 chu so in tren the RFID (vi du: 0007508976)!\n");
                        break;
                    }
                    uint32_t val = (uint32_t)strtoul(hex_tag + 2, NULL, 16);
                    unsigned int fc = (val >> 16) & 0xFF;
                    unsigned int id = val & 0xFFFF;
                    printf("-> Dang mo phong quet the qua PicoRV32 SoC:\n");
                    printf("   + So in tren the        : %010u  (%03u,%05u)\n", (unsigned int)val, fc, id);
                    printf("   + Ma Hex (UID 10 ky tu) : %s\n", hex_tag);

                    char send_buf[32];
                    snprintf(send_buf, sizeof(send_buf), "V%s\n", hex_tag);
                    flush_serial(port);
                    write_serial(port, send_buf, strlen(send_buf));

                    bool done = false;
                    while (read_line_serial(port, resp, sizeof(resp), 2500) > 0) {
                        if (strstr(resp, "ACCESS:GRANTED:SLOT:")) {
                            int tag_slot = 0, log_slot = 0;
                            char r_tag[32] = "";
                            sscanf(resp, "ACCESS:GRANTED:SLOT:%d:%10[^:]:LOG:%d", &tag_slot, r_tag, &log_slot);
                            printf("\n===============================================================\n");
                            printf("  [ACCESS GRANTED] >>> XAC THUC THANH CONG! <<<\n");
                            printf("===============================================================\n");
                            printf("  - The quet         : %010u  (UID: %s)\n", (unsigned int)val, hex_tag);
                            printf("  - Ket qua          : THE HOP LE (Khop Slot #%d, Dia chi 0x%06X)\n",
                                   tag_slot, 0x300000 + tag_slot * 16);
                            printf("  - Nhat ky Flash    : Da ghi vao Log Slot #%d (Dia chi 0x%06X)\n",
                                   log_slot, 0x310000 + log_slot * 16);
                            printf("===============================================================\n");
                            done = true;
                            break;
                        } else if (strstr(resp, "ACCESS:DENIED:")) {
                            int log_slot = 0;
                            char r_tag[32] = "";
                            sscanf(resp, "ACCESS:DENIED:%10[^:]:LOG:%d", r_tag, &log_slot);
                            printf("\n===============================================================\n");
                            printf("  [ACCESS DENIED] >>> TU CHOI TRUY CAP (THE KHONG HOP LE)! <<<\n");
                            printf("===============================================================\n");
                            printf("  - The quet         : %010u  (UID: %s)\n", (unsigned int)val, hex_tag);
                            printf("  - Ket qua          : THE CHUA DANG KY trong he thong!\n");
                            printf("  - Nhat ky Flash    : Da ghi vao Log Slot #%d (Dia chi 0x%06X)\n",
                                   log_slot, 0x310000 + log_slot * 16);
                            printf("===============================================================\n");
                            done = true;
                            break;
                        } else if (strstr(resp, "ERR:")) {
                            printf("[LOI] %s\n", resp);
                            done = true;
                            break;
                        }
                    }
                    if (!done) {
                        printf("[CANH BAO] Timeout khi quet the ao!\n");
                    }
                }
                break;
            }

            case 6: { // Virtual Scan: By Hex
                char custom_tag[128];
                printf("\n--- QUET THE RFID AO (NHAP MA HEX 10 KY TU) ---\n");
                printf("Nhap ma Hex 10 ky tu cua the (vi du: 00007293F0 hoac 010054DA65): ");
                if (fgets(custom_tag, sizeof(custom_tag), stdin)) {
                    char *nl = strchr(custom_tag, '\n');
                    if (nl) *nl = '\0';
                    nl = strchr(custom_tag, '\r');
                    if (nl) *nl = '\0';

                    char clean[32];
                    int clen = 0;
                    for (int i = 0; custom_tag[i] && clen < 10; i++) {
                        char c = custom_tag[i];
                        if (isspace((unsigned char)c)) continue;
                        if ((c >= '0' && c <= '9') || (c >= 'A' && c <= 'F') || (c >= 'a' && c <= 'f')) {
                            if (c >= 'a' && c <= 'f') c = c - 'a' + 'A';
                            clean[clen++] = c;
                        } else {
                            clen = -1;
                            break;
                        }
                    }
                    if (clen != 10) {
                        printf("[LOI] Vui long nhap dung 10 ky tu Hex hop le (0-9, A-F)!\n");
                        break;
                    }
                    clean[10] = '\0';

                    uint32_t val = (uint32_t)strtoul(clean + 2, NULL, 16);
                    unsigned int fc = (val >> 16) & 0xFF;
                    unsigned int id = val & 0xFFFF;
                    printf("-> Dang mo phong quet the qua PicoRV32 SoC:\n");
                    printf("   + Ma Hex (UID 10 ky tu) : %s\n", clean);
                    printf("   + Tuong duong in tren the: %010u  (%03u,%05u)\n", (unsigned int)val, fc, id);

                    char send_buf[32];
                    snprintf(send_buf, sizeof(send_buf), "V%s\n", clean);
                    flush_serial(port);
                    write_serial(port, send_buf, strlen(send_buf));

                    bool done = false;
                    while (read_line_serial(port, resp, sizeof(resp), 2500) > 0) {
                        if (strstr(resp, "ACCESS:GRANTED:SLOT:")) {
                            int tag_slot = 0, log_slot = 0;
                            char r_tag[32] = "";
                            sscanf(resp, "ACCESS:GRANTED:SLOT:%d:%10[^:]:LOG:%d", &tag_slot, r_tag, &log_slot);
                            printf("\n===============================================================\n");
                            printf("  [ACCESS GRANTED] >>> XAC THUC THANH CONG! <<<\n");
                            printf("===============================================================\n");
                            printf("  - The quet         : UID %s  (%010u)\n", clean, (unsigned int)val);
                            printf("  - Ket qua          : THE HOP LE (Khop Slot #%d, Dia chi 0x%06X)\n",
                                   tag_slot, 0x300000 + tag_slot * 16);
                            printf("  - Nhat ky Flash    : Da ghi vao Log Slot #%d (Dia chi 0x%06X)\n",
                                   log_slot, 0x310000 + log_slot * 16);
                            printf("===============================================================\n");
                            done = true;
                            break;
                        } else if (strstr(resp, "ACCESS:DENIED:")) {
                            int log_slot = 0;
                            char r_tag[32] = "";
                            sscanf(resp, "ACCESS:DENIED:%10[^:]:LOG:%d", r_tag, &log_slot);
                            printf("\n===============================================================\n");
                            printf("  [ACCESS DENIED] >>> TU CHOI TRUY CAP (THE KHONG HOP LE)! <<<\n");
                            printf("===============================================================\n");
                            printf("  - The quet         : UID %s  (%010u)\n", clean, (unsigned int)val);
                            printf("  - Ket qua          : THE CHUA DANG KY trong he thong!\n");
                            printf("  - Nhat ky Flash    : Da ghi vao Log Slot #%d (Dia chi 0x%06X)\n",
                                   log_slot, 0x310000 + log_slot * 16);
                            printf("===============================================================\n");
                            done = true;
                            break;
                        } else if (strstr(resp, "ERR:")) {
                            printf("[LOI] %s\n", resp);
                            done = true;
                            break;
                        }
                    }
                    if (!done) {
                        printf("[CANH BAO] Timeout khi quet the ao!\n");
                    }
                }
                break;
            }

            case 7: { // View Access Logs from Flash (0x310000)
                printf("\n-> Gui lenh 'L' (Doc nhat ky quet the tu SPI Flash Basys 3)...\n");
                flush_serial(port);
                write_serial(port, "L\n", 2);

                int log_count = 0;
                while (read_line_serial(port, resp, sizeof(resp), 2000) > 0) {
                    if (strstr(resp, "LOGS_START")) {
                        printf("\n====================================================================================================\n");
                        printf("                          NHAT KY QUET THE RFID TRONG SPI FLASH (0x310000)                  \n");
                        printf("====================================================================================================\n");
                        printf("  STT | KET QUA     | SO IN TREN THE | MA HEX UID | TRANG THAI CHI TIET        | DIA CHI FLASH      \n");
                        printf("----------------------------------------------------------------------------------------------------\n");
                        continue;
                    }
                    if (strstr(resp, "LOG_ITEM:")) {
                        int slot = 0, seq = 0;
                        char status[16] = "", tag[32] = "";
                        sscanf(resp, "LOG_ITEM:%d:%15[^:]:%31[^:]:%d", &slot, status, tag, &seq);
                        log_count++;

                        uint32_t val = (uint32_t)strtoul(tag + 2, NULL, 16);
                        bool is_succ = (strcmp(status, "SUCC") == 0);

                        printf("  %3d | %-11s | %-14u | %-10s | %-26s | Slot #%-2d (0x%06X)\n",
                               log_count,
                               is_succ ? "[THANH CONG]" : "[ THAT BAI ]",
                               (unsigned int)val,
                               tag,
                               is_succ ? "Hop le (Access Granted)" : "Khong hop le (Denied)",
                               slot,
                               0x310000 + slot * 16);
                        continue;
                    }
                    if (strstr(resp, "LOGS_TOTAL:")) {
                        int total = 0, succ = 0, fail = 0;
                        sscanf(resp, "LOGS_TOTAL:%d:%d:%d", &total, &succ, &fail);
                        printf("----------------------------------------------------------------------------------------------------\n");
                        printf("[TONG KET] Tong so luot quet: %d | Thanh cong: %d | That bai: %d\n", total, succ, fail);
                        continue;
                    }
                    if (strstr(resp, "LOGS_END")) {
                        break;
                    }
                    if (strstr(resp, "EMPTY_LOGS")) {
                        printf("[NHAT KY TRONG] Chua co luot quet the nao duoc ghi nhan trong Flash (hoac da bi xoa)!\n");
                        break;
                    }
                }
                break;
            }

            case 8: { // Erase Access Logs (0x310000)
                printf("\n-> Gui lenh 'X' (Xoa toan bo nhat ky quet the trong SPI Flash 0x310000)...\n");
                flush_serial(port);
                write_serial(port, "X\n", 2);
                if (read_line_serial(port, resp, sizeof(resp), 3000) > 0) {
                    if (strstr(resp, "OK:LOGS_ERASED")) {
                        printf("[THANH CONG] Toan bo nhat ky quet the trong Flash (0x310000) da duoc xoa sach!\n");
                        printf("(Danh muc the da cap phep tai 0x300000 van duoc giu nguyen ven).\n");
                    } else {
                        printf("[PHAN HOI] %s\n", resp);
                    }
                } else {
                    printf("[CANH BAO] Timeout khi xoa nhat ky Flash!\n");
                }
                break;
            }

            case 9: { // Erase Authorized Tags Sector (0x300000)
                printf("\n-> Gui lenh 'E' (Xoa sector SPI Flash danh muc the 0x300000)...\n");
                flush_serial(port);
                write_serial(port, "E\n", 2);
                if (read_line_serial(port, resp, sizeof(resp), 3000) > 0) {
                    printf("[THANH CONG] %s\n", resp);
                } else {
                    printf("[CANH BAO] Timeout khi xoa Flash!\n");
                }
                break;
            }

            case 10: { // Status
                printf("\n-> Gui lenh 'S' (Xem trang thai)...\n");
                flush_serial(port);
                write_serial(port, "S\n", 2);
                if (read_line_serial(port, resp, sizeof(resp), 1500) > 0) {
                    printf("[TRANG THAI] %s\n", resp);
                } else {
                    printf("[CANH BAO] Timeout!\n");
                }
                break;
            }

            default:
                printf("\nLua chon khong hop le! Vui long chon tu 0 den 10.\n");
                break;
        }

    }


    close_serial(port);
    return 0;
}
