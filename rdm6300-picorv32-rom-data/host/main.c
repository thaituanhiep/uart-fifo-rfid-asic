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
#include <time.h>

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
// CSV Export & Import Management (Folder: rfids/)
// ----------------------------------------------------------------------------
static void get_rfids_dir(char *out_dir, size_t out_dir_size) {
    // If folder "host" exists in cwd, then the rfids dir is "host/rfids"
    DWORD attr_host = GetFileAttributesA("host");
    if (attr_host != INVALID_FILE_ATTRIBUTES && (attr_host & FILE_ATTRIBUTE_DIRECTORY)) {
        snprintf(out_dir, out_dir_size, "host/rfids");
    } else {
        snprintf(out_dir, out_dir_size, "rfids");
    }
    // Create directory if not already existing
    CreateDirectoryA(out_dir, NULL);
}

static void get_logs_dir(char *out_dir, size_t out_dir_size) {
    // If folder "host" exists in cwd, then the logs dir is "host/logs"
    DWORD attr_host = GetFileAttributesA("host");
    if (attr_host != INVALID_FILE_ATTRIBUTES && (attr_host & FILE_ATTRIBUTE_DIRECTORY)) {
        snprintf(out_dir, out_dir_size, "host/logs");
    } else {
        snprintf(out_dir, out_dir_size, "logs");
    }
    // Create directory if not already existing
    CreateDirectoryA(out_dir, NULL);
}

static bool find_latest_csv_file(char *out_path, size_t out_path_size, char *out_name, size_t out_name_size) {
    const char *search_dirs[] = {"host/rfids", "rfids", "host", "."};
    char best_ts[32] = "";
    char best_filename[MAX_PATH] = "";
    char best_filepath[MAX_PATH] = "";
    FILETIME best_ft = {0, 0};
    bool found = false;

    for (int d = 0; d < 4; d++) {
        DWORD attr = GetFileAttributesA(search_dirs[d]);
        if (attr == INVALID_FILE_ATTRIBUTES || !(attr & FILE_ATTRIBUTE_DIRECTORY)) continue;

        char pattern[MAX_PATH];
        snprintf(pattern, sizeof(pattern), "%s\\*.csv", search_dirs[d]);

        WIN32_FIND_DATAA find_data;
        HANDLE hFind = FindFirstFileA(pattern, &find_data);
        if (hFind != INVALID_HANDLE_VALUE) {
            do {
                if (!(find_data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)) {
                    const char *fname = find_data.cFileName;
                    size_t flen = strlen(fname);
                    char full_path[MAX_PATH];
                    snprintf(full_path, sizeof(full_path), "%s\\%s", search_dirs[d], fname);

                    // Check 14-digit timestamp pattern: YYYYMMDDHHMMSS.csv
                    if (flen == 18 && strcasecmp(fname + 14, ".csv") == 0) {
                        bool is_digits = true;
                        for (int i = 0; i < 14; i++) {
                            if (!isdigit((unsigned char)fname[i])) { is_digits = false; break; }
                        }
                        if (is_digits) {
                            char ts[15];
                            strncpy(ts, fname, 14);
                            ts[14] = '\0';
                            if (strcmp(ts, best_ts) > 0) {
                                strncpy(best_ts, ts, sizeof(best_ts));
                                strncpy(best_filename, fname, sizeof(best_filename));
                                strncpy(best_filepath, full_path, sizeof(best_filepath));
                                best_ft = find_data.ftLastWriteTime;
                                found = true;
                            }
                            continue;
                        }
                    }

                    // Fallback for general .csv files without 14-digit timestamp
                    if (best_ts[0] == '\0') {
                        if (!found || CompareFileTime(&find_data.ftLastWriteTime, &best_ft) > 0) {
                            strncpy(best_filename, fname, sizeof(best_filename));
                            strncpy(best_filepath, full_path, sizeof(best_filepath));
                            best_ft = find_data.ftLastWriteTime;
                            found = true;
                        }
                    }
                }
            } while (FindNextFileA(hFind, &find_data));
            FindClose(hFind);
        }
        if (found && best_ts[0] != '\0') break; // Prioritize rfids folder
    }

    if (found) {
        snprintf(out_path, out_path_size, "%s", best_filepath);
        snprintf(out_name, out_name_size, "%s", best_filename);
        return true;
    }
    return false;
}

void export_tags_to_csv(serial_port_t port) {
    time_t now = time(NULL);
    struct tm *t = localtime(&now);
    char time_str[32];
    strftime(time_str, sizeof(time_str), "%Y%m%d%H%M%S", t);
    char time_readable[64];
    strftime(time_readable, sizeof(time_readable), "%d/%m/%Y %H:%M:%S", t);

    char filename[64];
    snprintf(filename, sizeof(filename), "%s.csv", time_str);

    char rfids_dir[128];
    get_rfids_dir(rfids_dir, sizeof(rfids_dir));

    char filepath[256];
    snprintf(filepath, sizeof(filepath), "%s/%s", rfids_dir, filename);

    FILE *f = fopen(filepath, "w");
    if (!f) {
        printf("[LOI] Khong the tao file CSV tai: %s\n", filepath);
        return;
    }

    fprintf(f, "10 so in tren the\n");

    printf("\n-> Gui lenh 'F' (Doc danh sach the tu SPI Flash de xuat CSV vao folder rfids)...\n");
    flush_serial(port);
    write_serial(port, "F\n", 2);

    char resp[256];
    int tag_count = 0;
    bool empty = false;

    while (read_line_serial(port, resp, sizeof(resp), 2000) > 0) {
        if (strstr(resp, "EMPTY")) {
            empty = true;
            break;
        }
        if (strstr(resp, "TAG_ITEM:")) {
            int slot = 0;
            char tag[32] = "";
            if (sscanf(resp, "TAG_ITEM:%d:%31s", &slot, tag) == 2) {
                uint32_t val = (uint32_t)strtoul(tag + 2, NULL, 16);
                fprintf(f, "%010u\n", (unsigned int)val);
                tag_count++;
            }
        }
        if (strstr(resp, "TAGS_END")) {
            break;
        }
    }

    fclose(f);

    if (empty || tag_count == 0) {
        printf("[THONG BAO] Flash hien dang TRONG (Chua co the nao duoc luu)!\n");
    }

    printf("\n===================================================================================\n");
    printf("                     XUAT DANH SACH THE RA FILE CSV THANH CONG                     \n");
    printf("===================================================================================\n");
    printf("  - Thoi gian hien tai (Export Time) : %s  (%s)\n", time_readable, time_str);
    printf("  - Ten file CSV da tao              : %s\n", filename);
    printf("  - Thu muc luu tru                  : %s\n", rfids_dir);
    printf("  - Duong dan day du                 : %s\n", filepath);
    printf("  - Dinh dang CSV                    : 1 cot (10 so in tren the)\n");
    printf("  - Tong so the RFID da export       : %d the\n", tag_count);
    printf("===================================================================================\n");
}

int export_logs_to_csv(serial_port_t port, char *out_filepath, size_t out_filepath_size, bool is_backup) {
    time_t now = time(NULL);
    struct tm *t = localtime(&now);
    char time_str[32];
    strftime(time_str, sizeof(time_str), "%Y%m%d%H%M%S", t);
    char time_readable[64];
    strftime(time_readable, sizeof(time_readable), "%d/%m/%Y %H:%M:%S", t);

    char filename[64];
    snprintf(filename, sizeof(filename), "%s_LOGS.csv", time_str);

    char logs_dir[128];
    get_logs_dir(logs_dir, sizeof(logs_dir));

    char filepath[256];
    snprintf(filepath, sizeof(filepath), "%s/%s", logs_dir, filename);
    if (out_filepath && out_filepath_size > 0) {
        snprintf(out_filepath, out_filepath_size, "%s", filepath);
    }

    if (is_backup) {
        printf("\n-> [SAO LUU] Dang doc toan bo nhat ky tu SPI Flash (0x310000) de luu tru vao CSV...\n");
    } else {
        printf("\n-> Gui lenh 'L' (Doc nhat ky quet the tu SPI Flash 0x310000 de xuat CSV vao folder logs)...\n");
    }

    flush_serial(port);
    write_serial(port, "L\n", 2);

    FILE *f = NULL;
    char resp[256];
    int log_count = 0;
    int succ_count = 0;
    int fail_count = 0;
    bool empty = false;

    while (read_line_serial(port, resp, sizeof(resp), 2000) > 0) {
        if (strstr(resp, "EMPTY_LOGS")) {
            empty = true;
            break;
        }
        if (strstr(resp, "LOG_ITEM:")) {
            if (!f) {
                f = fopen(filepath, "w");
                if (!f) {
                    printf("[LOI] Khong the tao file CSV tai: %s\n", filepath);
                    return -1;
                }
                fprintf(f, "STT,Ket qua,10 so in tren the,Ma the (FC-ID),Ma Hex UID,Slot Flash,So thu tu (Seq)\n");
            }
            int slot = 0, seq = 0;
            char status[16] = "", tag[32] = "";
            if (sscanf(resp, "LOG_ITEM:%d:%15[^:]:%31[^:]:%d", &slot, status, tag, &seq) == 4) {
                log_count++;
                bool is_succ = (strcmp(status, "SUCC") == 0);
                if (is_succ) succ_count++;
                else fail_count++;

                uint32_t val = (uint32_t)strtoul(tag + 2, NULL, 16);
                unsigned int fc = (val >> 16) & 0xFF;
                unsigned int id = val & 0xFFFF;
                const char *status_str = is_succ ? "THANH CONG" : "THAT BAI";

                fprintf(f, "%d,%s,%010u,%03u-%05u,%s,%d,%d\n",
                        log_count, status_str, (unsigned int)val, fc, id, tag, slot, seq);
            }
        }
        if (strstr(resp, "LOGS_TOTAL:")) {
            int total = 0, s = 0, fa = 0;
            sscanf(resp, "LOGS_TOTAL:%d:%d:%d", &total, &s, &fa);
        }
        if (strstr(resp, "LOGS_END")) {
            break;
        }
    }

    if (f) {
        fclose(f);
    }

    if (empty || log_count == 0) {
        if (is_backup) {
            printf("[THONG BAO] Nhat ky Flash hien dang TRONG (Chua co ban ghi nao can sao luu)!\n");
        } else {
            printf("[THONG BAO] Nhat ky Flash hien dang TRONG (Chua co luot quet nao duoc ghi nhan)!\n");
        }
        if (f) {
            remove(filepath);
        }
        return 0;
    }

    printf("\n===================================================================================\n");
    if (is_backup) {
        printf("       SAO LUU NHAT KY QUET THE RA FILE CSV THANH CONG (PRE-ERASE)        \n");
    } else {
        printf("                  XUAT NHAT KY QUET THE RA FILE CSV THANH CONG                     \n");
    }
    printf("===================================================================================\n");
    printf("  - Thoi gian xuat (Export Time)     : %s  (%s)\n", time_readable, time_str);
    printf("  - Ten file CSV da tao              : %s\n", filename);
    printf("  - Thu muc luu tru                  : %s\n", logs_dir);
    printf("  - Duong dan tap tin                : %s\n", filepath);
    printf("  - Tong so nhat ky da xuat          : %d luot\n", log_count);
    printf("  - So luot quet hop le (THANH CONG) : %d\n", succ_count);
    printf("  - So luot khong hop le (THAT BAI)  : %d\n", fail_count);
    printf("===================================================================================\n");

    return log_count;
}

void import_tags_from_latest_csv(serial_port_t port) {
    char filepath[MAX_PATH];
    char filename[MAX_PATH];

    if (!find_latest_csv_file(filepath, sizeof(filepath), filename, sizeof(filename))) {
        printf("\n[LOI] Khong tim thay file .csv nao trong thu muc 'rfids', 'host' hoac thu muc lam viec!\n");
        return;
    }

    // Parse readable timestamp if filename is YYYYMMDDHHMMSS.csv
    char time_display[64] = "Khong xac dinh";
    if (strlen(filename) >= 18 && isdigit((unsigned char)filename[0])) {
        int y, m, d, h, min, s;
        if (sscanf(filename, "%4d%2d%2d%2d%2d%2d", &y, &m, &d, &h, &min, &s) == 6) {
            snprintf(time_display, sizeof(time_display), "%02d/%02d/%04d %02d:%02d:%02d", d, m, y, h, min, s);
        }
    }

    FILE *f = fopen(filepath, "r");
    if (!f) {
        printf("\n[LOI] Khong the mo file CSV: %s\n", filepath);
        return;
    }

    printf("\n===================================================================================\n");
    printf("             IMPORT DANH SACH THE TU FILE CSV CO THOI GIAN GAN NHAT                \n");
    printf("===================================================================================\n");
    printf("  - File CSV duoc chon   : %s\n", filename);
    printf("  - Thoi gian ghi nhan   : %s\n", time_display);
    printf("  - Duong dan tap tin    : %s\n", filepath);
    printf("  - Dinh dang            : 1 cot (10 so in tren the)\n");
    printf("-----------------------------------------------------------------------------------\n");
    printf("-> [BUOC 1] Dang xoa toan bo danh muc the cu tren SPI Flash Basys 3 (0x300000)...\n");
    flush_serial(port);
    write_serial(port, "E\n", 2);
    char resp_erase[256];
    if (read_line_serial(port, resp_erase, sizeof(resp_erase), 4000) > 0) {
        printf("[THANH CONG] %s\n", resp_erase);
    } else {
        printf("[CANH BAO] Timeout khi xoa Flash Sector 48! Van tiep tuc nap the...\n");
    }
    printf("-----------------------------------------------------------------------------------\n");
    printf("-> [BUOC 2] Dang doc tung dong va nap the tu file CSV vao SPI Flash PicoRV32...\n\n");

    char line[256];
    int total_lines = 0;
    int succ_count = 0;
    int exists_count = 0;
    int err_count = 0;
    bool flash_full = false;

    while (fgets(line, sizeof(line), f)) {
        // Trim newline and carriage return
        char *nl = strchr(line, '\r');
        if (nl) *nl = '\0';
        nl = strchr(line, '\n');
        if (nl) *nl = '\0';

        // Trim leading and trailing whitespace
        char *p = line;
        while (*p && isspace((unsigned char)*p)) p++;
        char *end = p + strlen(p) - 1;
        while (end >= p && isspace((unsigned char)*end)) {
            *end = '\0';
            end--;
        }

        // Skip empty line
        if (strlen(p) == 0) continue;

        // Skip CSV header line
        if (strstr(p, "hex") || strstr(p, "HEX") || strstr(p, "so") || strstr(p, "the") || strstr(p, "tag") || strstr(p, "card")) {
            continue;
        }

        // Strip surrounding quotes if present
        if (*p == '"' || *p == '\'') {
            p++;
            char *q = strchr(p, '"');
            if (!q) q = strchr(p, '\'');
            if (q) *q = '\0';
        }

        // If line contains comma (e.g. legacy multi-column), take first column
        char token[64] = "";
        char *comma = strchr(p, ',');
        if (comma) {
            size_t tlen = comma - p;
            if (tlen >= sizeof(token)) tlen = sizeof(token) - 1;
            strncpy(token, p, tlen);
            token[tlen] = '\0';
        } else {
            strncpy(token, p, sizeof(token) - 1);
        }

        // Parse 10 digits printed on card into hex tag
        char hex_tag[11] = "";
        bool ok = parse_card_input(token, hex_tag);
        if (!ok && comma) {
            ok = parse_card_input(comma + 1, hex_tag);
        }

        if (!ok) {
            printf("  [BO QUA] Dong khong hop le: %s\n", line);
            continue;
        }

        total_lines++;
        uint32_t val = (uint32_t)strtoul(hex_tag + 2, NULL, 16);
        unsigned int fc = (val >> 16) & 0xFF;
        unsigned int id = val & 0xFFFF;

        char send_buf[32];
        snprintf(send_buf, sizeof(send_buf), "N%s\n", hex_tag);
        flush_serial(port);
        write_serial(port, send_buf, strlen(send_buf));

        char resp[256];
        bool done = false;
        while (read_line_serial(port, resp, sizeof(resp), 2500) > 0) {
            if (strstr(resp, "OK:MANUAL_TAG_SAVED:SLOT:")) {
                int slot = 0;
                char rtag[32] = "";
                sscanf(resp, "OK:MANUAL_TAG_SAVED:SLOT:%d:%31s", &slot, rtag);
                succ_count++;
                if (total_lines <= 5 || total_lines % 50 == 0 || total_lines == 1000) {
                    printf("  [%4d] The %010u (%03u,%05u) [UID: %s] -> [LUU MOI THANH CONG] Slot #%d (0x%06X)\n",
                           total_lines, (unsigned int)val, fc, id, hex_tag, slot, 0x300000 + slot * 16);
                }
                done = true;
                break;
            } else if (strstr(resp, "INFO:EXISTS:SLOT:")) {
                int slot = 0;
                char rtag[32] = "";
                sscanf(resp, "INFO:EXISTS:SLOT:%d:%31s", &slot, rtag);
                exists_count++;
                if (total_lines <= 5 || total_lines % 50 == 0 || total_lines == 1000) {
                    printf("  [%4d] The %010u (%03u,%05u) [UID: %s] -> [DA TON TAI] trong Flash tai Slot #%d\n",
                           total_lines, (unsigned int)val, fc, id, hex_tag, slot);
                }
                done = true;
                break;
            } else if (strstr(resp, "FLASH_FULL")) {
                printf("  [%4d] The %010u [UID: %s] -> [LOI: FLASH DAY] Toi da 4096 the!\n",
                       total_lines, (unsigned int)val, hex_tag);
                err_count++;
                flash_full = true;
                done = true;
                break;
            } else if (strstr(resp, "FAIL") || strstr(resp, "ERR:")) {
                printf("  [%4d] The %010u [UID: %s] -> [THAT BAI]: %s\n",
                       total_lines, (unsigned int)val, hex_tag, resp);
                err_count++;
                done = true;
                break;
            }
        }

        if (!done) {
            printf("  [%4d] The %010u [UID: %s] -> [TIMEOUT] PicoRV32 khong phan hoi!\n",
                   total_lines, (unsigned int)val, hex_tag);
            err_count++;
        }

        if (flash_full) break;
    }

    fclose(f);

    printf("-----------------------------------------------------------------------------------\n");
    printf("[TONG KET IMPORT]\n");
    printf("  + File CSV da doc        : %s\n", filename);
    printf("  + Tong so the trong file : %d the\n", total_lines);
    printf("  + Luu moi thanh cong     : %d the\n", succ_count);
    printf("  + The da co san trong DB : %d the\n", exists_count);
    if (err_count > 0) {
        printf("  + Loi hoac that bai      : %d the\n", err_count);
    }
    printf("===================================================================================\n");
}

// ----------------------------------------------------------------------------
// Delete RFID Tag from Flash & Re-Export CSV
// ----------------------------------------------------------------------------
void delete_tag_from_flash(serial_port_t port) {
    char custom_tag[128];
    printf("\nNhap 10 chu so in tren the RFID can xoa (vi du: 0007508976): ");
    if (!fgets(custom_tag, sizeof(custom_tag), stdin)) {
        return;
    }
    char *nl = strchr(custom_tag, '\n');
    if (nl) *nl = '\0';
    nl = strchr(custom_tag, '\r');
    if (nl) *nl = '\0';

    char target_hex[11];
    if (!parse_card_input(custom_tag, target_hex)) {
        printf("[LOI] Vui long nhap 10 chu so in tren the RFID (vi du: 0007508976)!\n");
        return;
    }

    uint32_t val = (uint32_t)strtoul(target_hex + 2, NULL, 16);
    unsigned int fc = (val >> 16) & 0xFF;
    unsigned int id = val & 0xFFFF;
    printf("\n-> Thong tin the can xoa:\n");
    printf("   + So in tren the        : %010u  (%03u,%05u)\n", (unsigned int)val, fc, id);
    printf("   + Ma Hex (UID 10 ky tu) : %s\n", target_hex);

    char send_buf[32];
    snprintf(send_buf, sizeof(send_buf), "K%s\n", target_hex);
    printf("-> Gui lenh xoa duy nhat the %s toi SPI Flash Basys 3...\n", target_hex);
    flush_serial(port);
    write_serial(port, send_buf, strlen(send_buf));

    char resp[256];
    bool done = false;
    while (read_line_serial(port, resp, sizeof(resp), 3000) > 0) {
        if (strstr(resp, "OK:TAG_DELETED:SLOT:")) {
            int slot = 0;
            char rtag[32] = "";
            sscanf(resp, "OK:TAG_DELETED:SLOT:%d:%31s", &slot, rtag);

            printf("\n===================================================================================\n");
            printf("                    XOA THE KHOI SPI FLASH THANH CONG                              \n");
            printf("===================================================================================\n");
            printf("  - The da xoa                  : %010u  (%03u,%05u) [UID: %s]\n", (unsigned int)val, fc, id, rtag);
            printf("  - Vi tri da xoa trong Flash   : Slot #%d (Dia chi: 0x%06X)\n", slot, 0x300000 + slot * 16);
            printf("  - Phuong thuc xoa             : Ghi de truc tiep Word Magic ve 0x00000000\n");
            printf("                                  (CHI XOA DUY NHAT THE NAY, KHONG XOA TOAN BO FLASH)\n");
            printf("===================================================================================\n");

            printf("\n-> Tu dong xuat danh sach the con lai ra file CSV moi trong host/rfids/...\n");
            export_tags_to_csv(port);
            done = true;
            break;
        } else if (strstr(resp, "ERR:TAG_NOT_FOUND")) {
            printf("\n===================================================================================\n");
            printf("[THONG BAO] The %010u (UID: %s) KHONG TON TAI trong Flash!\n", (unsigned int)val, target_hex);
            printf("            Khong co thay doi nao duoc thuc hien tren Flash va CSV.\n");
            printf("===================================================================================\n");
            done = true;
            break;
        } else if (strstr(resp, "FAIL") || strstr(resp, "ERR:")) {
            printf("[LOI] %s\n", resp);
            done = true;
            break;
        }
    }

    if (!done) {
        printf("[CANH BAO] Timeout khi gui lenh xoa the toi PicoRV32!\n");
    }
}


// ----------------------------------------------------------------------------
// User Menu & Application Logic
// ----------------------------------------------------------------------------
void print_menu(void) {
    printf("\n===============================================================\n");
    printf("     RDM6300 RFID - PICORV32 - BASYS 3 SPI FLASH MANAGER      \n");
    printf("===============================================================\n");
    printf("  [1]  Ping Hardware (Kiem tra ket noi PicoRV32)\n");
    printf("  [2]  Input & Save New RFID Tag (Nhap 10 so in tren the de luu Flash & Export)\n");
    printf("  [3]  Check RFID Tag in Flash (Kiem tra the da co trong Flash chua)\n");
    printf("  [4]  Delete RFID Tag from Flash (Nhap 10 so in tren the de xoa khoi Flash & Export CSV)\n");
    printf("  [5]  Virtual Scan: By Decimal (Quet the ao: Nhap 10 so in tren the)\n");
    printf("  [6]  Virtual Scan: By Hex (Quet the ao: Nhap ma Hex 10 ky tu)\n");
    printf("  [7]  View Access Logs from Flash (Xem nhat ky quet the tu Flash 0x310000)\n");
    printf("  [8]  Export Access Logs to CSV (Xuat nhat ky quet the ra file CSV vao host/logs)\n");
    printf("  [9]  Erase Access Logs (Sao luu ra CSV truoc roi xoa nhat ky trong Flash 0x310000)\n");
    printf("  [10] Erase Authorized Tags Sector (Xoa the da cap phep 0x300000)\n");
    printf("  [11] Get SoC Status (Xem trang thai LED, Flash, PicoRV32)\n");
    printf("  [12] Export RFID Tags to CSV (Xuat danh sach the ra file CSV vao host/rfids)\n");
    printf("  [13] Import RFID Tags from Latest CSV (Xoa Flash & Nap the tu file CSV gan nhat)\n");
    printf("  [0]  Exit (Thoat)\n");
    printf("---------------------------------------------------------------\n");
    printf("Lua chon cua ban [0-13]: ");
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
                            printf("-> Tu dong xuat danh sach the moi cap nhat ra file CSV...\n");
                            export_tags_to_csv(port);
                            done = true;
                            break;
                        } else if (strstr(resp, "INFO:EXISTS:SLOT:")) {
                            int slot = 0;
                            char tag[32] = "";
                            sscanf(resp, "INFO:EXISTS:SLOT:%d:%31s", &slot, tag);
                            printf("[THONG BAO] The %s (%010u) DA TON TAI truoc do trong Flash tai Slot #%d -> Khong can them nua!\n",
                                   tag, (unsigned int)val, slot);
                            done = true;
                            break;
                        } else if (strstr(resp, "FLASH_FULL")) {
                            printf("[LOI] Bo nho Flash da day (toi da 4096 the)!\n");
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

                    char send_cmd[32];
                    snprintf(send_cmd, sizeof(send_cmd), "C%s\n", hex_tag);
                    flush_serial(port);
                    write_serial(port, send_cmd, strlen(send_cmd));

                    bool done = false;
                    while (read_line_serial(port, resp, sizeof(resp), 2000) > 0) {
                        if (strstr(resp, "OK:TAG_FOUND:SLOT:")) {
                            int slot = 0;
                            char r_tag[32] = "";
                            sscanf(resp, "OK:TAG_FOUND:SLOT:%d:%31s", &slot, r_tag);
                            printf("---------------------------------------------------------------\n");
                            printf("[KET QUA] [DA TON TAI] The %010u (UID: %s) DA CO trong Flash!\n",
                                   (unsigned int)val, hex_tag);
                            printf("         - Vi tri luu tru : Slot #%d\n", slot);
                            printf("         - Dia chi Flash  : 0x%06X\n", 0x300000 + slot * 16);
                            printf("---------------------------------------------------------------\n");
                            done = true;
                            break;
                        } else if (strstr(resp, "ERR:TAG_NOT_FOUND")) {
                            printf("---------------------------------------------------------------\n");
                            printf("[KET QUA] [CHUA CO] The %010u (UID: %s) CHUA CO trong Flash.\n",
                                   (unsigned int)val, hex_tag);
                            printf("         (Ban co the chon chuc nang [2] de luu the nay vao Flash).\n");
                            printf("---------------------------------------------------------------\n");
                            done = true;
                            break;
                        } else if (strstr(resp, "ERR:")) {
                            printf("[LOI] %s\n", resp);
                            done = true;
                            break;
                        }
                    }
                    if (!done) {
                        printf("[CANH BAO] Timeout khi tra cuu the tren Basys 3!\n");
                    }
                }
                break;
            }

            case 4: { // Delete RFID Tag from Flash & Re-Export CSV
                delete_tag_from_flash(port);
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
                            printf("  - The quet         : %010u (%03u,%05u)  [UID: %s]\n", (unsigned int)val, fc, id, hex_tag);
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
                            printf("  - The quet         : %010u (%03u,%05u)  [UID: %s]\n", (unsigned int)val, fc, id, hex_tag);
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
                            printf("  - The quet         : %010u (%03u,%05u)  [UID: %s]\n", (unsigned int)val, fc, id, clean);
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
                            printf("  - The quet         : %010u (%03u,%05u)  [UID: %s]\n", (unsigned int)val, fc, id, clean);
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
                        printf("\n==================================================================================================================\n");
                        printf("                                 NHAT KY QUET THE RFID TRONG SPI FLASH (0x310000)                                 \n");
                        printf("==================================================================================================================\n");
                        printf("  STT | KET QUA     | SO IN TREN THE (10 SO + MA)  | MA HEX UID | TRANG THAI CHI TIET        | DIA CHI FLASH      \n");
                        printf("------------------------------------------------------------------------------------------------------------------\n");
                        continue;
                    }
                    if (strstr(resp, "LOG_ITEM:")) {
                        int slot = 0, seq = 0;
                        char status[16] = "", tag[32] = "";
                        sscanf(resp, "LOG_ITEM:%d:%15[^:]:%31[^:]:%d", &slot, status, tag, &seq);
                        log_count++;

                        uint32_t val = (uint32_t)strtoul(tag + 2, NULL, 16);
                        unsigned int fc = (val >> 16) & 0xFF;
                        unsigned int id = val & 0xFFFF;
                        bool is_succ = (strcmp(status, "SUCC") == 0);

                        printf("  %3d | %-11s | %010u (%03u,%05u)     | %-10s | %-26s | Slot #%-2d (0x%06X)\n",
                               log_count,
                               is_succ ? "[THANH CONG]" : "[ THAT BAI ]",
                               (unsigned int)val, fc, id,
                               tag,
                               is_succ ? "Hop le (Access Granted)" : "Khong hop le (Denied)",
                               slot,
                               0x310000 + slot * 16);
                        continue;
                    }
                    if (strstr(resp, "LOGS_TOTAL:")) {
                        int total = 0, succ = 0, fail = 0;
                        sscanf(resp, "LOGS_TOTAL:%d:%d:%d", &total, &succ, &fail);
                        printf("------------------------------------------------------------------------------------------------------------------\n");
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

            case 8: { // Export Access Logs to CSV
                export_logs_to_csv(port, NULL, 0, false);
                break;
            }

            case 9: { // Erase Access Logs (Save to CSV first, then erase Flash 0x310000)
                char backup_file[MAX_PATH] = "";
                printf("\n===============================================================\n");
                printf("          XOA NHAT KY QUET THE (AUTO-BACKUP VAO CSV)          \n");
                printf("===============================================================\n");
                printf("-> [BUOC 1] Tu dong sao luu toan bo nhat ky ra file CSV trong host/logs/...\n");
                int backed_up = export_logs_to_csv(port, backup_file, sizeof(backup_file), true);
                if (backed_up > 0) {
                    printf("\n-> [DA SAO LUU] Toan bo %d nhat ky da duoc luu an toan vao:\n   %s\n", backed_up, backup_file);
                } else {
                    printf("-> Nhat ky Flash hien dang trong, tiep tuc xoa de dam bao sach du lieu.\n");
                }

                printf("\n-> [BUOC 2] Gui lenh 'X' (Xoa toan bo nhat ky quet the trong SPI Flash 0x310000)...\n");
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

            case 10: { // Erase Authorized Tags Sector (0x300000)
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

            case 11: { // Status
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

            case 12: { // Export RFID Tags to CSV
                export_tags_to_csv(port);
                break;
            }

            case 13: { // Import RFID Tags from Latest CSV
                import_tags_from_latest_csv(port);
                break;
            }

            default:
                printf("\nLua chon khong hop le! Vui long chon tu 0 den 13.\n");
                break;
        }

    }


    close_serial(port);
    return 0;
}
