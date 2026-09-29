# ============================================================================
# File: tb/test_firmware.py
# Project: rdm6300-picorv32-rom-data
# Description: Python Automated Verification Testbench for PicoRV32 Firmware.
#              Tests all firmware functions, Flash storage layout, access logging,
#              anti-duplicate logic, authentication, and the complete UART host command protocol.
# ============================================================================

import sys
import io
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class FirmwareSimulator:
    def __init__(self):
        # 16 MB Mock Flash Memory initialized to 0xFF (Clean NOR Flash)
        self.flash_mem = bytearray(b'\xff' * (16 * 1024 * 1024))
        self.USER_FLASH_ADDR = 0x300000
        self.FLASH_SLOT_SIZE = 16
        self.MAX_TAG_SLOTS = 4096
        self.FLASH_RECORD_MAGIC = 0x52464944  # "RFID"

        self.LOG_FLASH_ADDR = 0x310000
        self.LOG_SLOT_SIZE = 16
        self.MAX_LOG_SLOTS = 512
        self.LOG_MAGIC_SUCC = 0x53554343  # "SUCC"
        self.LOG_MAGIC_FAIL = 0x4641494C  # "FAIL"

        # Hardware MMIO Registers
        self.reg_rfid_status = 0
        self.reg_rfid_tag_hi = 0
        self.reg_rfid_tag_lo = 0
        self.reg_gpio_leds = 0x0001  # Bit 0 alive
        self.reg_pc_uart_div = 5208

        # Firmware Global State
        self.last_tag_hex = "0000000000"
        self.tag_word_hi = 0
        self.tag_word_lo = 0
        self.tag_available = False
        self.last_scanned_hi = 0xFFFFFFFF
        self.last_scanned_lo = 0xFFFFFFFF
        self.rdm_cooldown_cnt = 0

        # UART Buffers
        self.rx_fifo = bytearray()
        self.tx_fifo = bytearray()

    # ------------------------------------------------------------------------
    # Flash Operations
    # ------------------------------------------------------------------------
    def flash_read_word(self, addr):
        addr &= len(self.flash_mem) - 1
        return int.from_bytes(self.flash_mem[addr:addr+4], byteorder='little')

    def flash_write_word(self, addr, data):
        addr &= len(self.flash_mem) - 1
        new_bytes = data.to_bytes(4, byteorder='little')
        # Emulate NOR Flash write (bits can only transition 1 -> 0)
        for i in range(4):
            self.flash_mem[addr + i] &= new_bytes[i]

    def flash_erase_sector(self, addr):
        addr &= len(self.flash_mem) - 1
        sector_base = addr & ~0xFFFF
        for i in range(65536):
            self.flash_mem[sector_base + i] = 0xFF

    def flash_read_id(self):
        return 0x00010215

    def flash_read_sr(self):
        return 0x00

    # ------------------------------------------------------------------------
    # UART Helper Functions
    # ------------------------------------------------------------------------
    def host_send_string(self, s):
        self.rx_fifo.extend(s.encode('ascii'))

    def uart_getc_nonblock(self):
        if not self.rx_fifo:
            return -1
        return self.rx_fifo.pop(0)

    def uart_putc(self, c):
        if isinstance(c, str):
            self.tx_fifo.append(ord(c))
        else:
            self.tx_fifo.append(c)

    def uart_puts(self, s):
        for c in s:
            if c == '\n':
                self.uart_putc('\r')
            self.uart_putc(c)

    def uart_puthex32(self, val):
        self.uart_puts(f"{val:08X}")

    def uart_putdec(self, val):
        self.uart_puts(str(val))

    def host_read_line(self):
        line = bytearray()
        while self.tx_fifo:
            b = self.tx_fifo.pop(0)
            if b == ord('\r'):
                continue
            if b == ord('\n'):
                break
            line.append(b)
        return line.decode('ascii', errors='replace')

    def host_clear_tx(self):
        self.tx_fifo.clear()

    def host_clear_rx(self):
        self.rx_fifo.clear()

    # ------------------------------------------------------------------------
    # Firmware Database Logic
    # ------------------------------------------------------------------------
    @staticmethod
    def hex2val(c):
        if '0' <= c <= '9': return ord(c) - ord('0')
        if 'A' <= c <= 'F': return ord(c) - ord('A') + 10
        if 'a' <= c <= 'f': return ord(c) - ord('a') + 10
        return -1

    def find_tag_slot(self, hi, lo):
        # Built-in Master Test Card: 010054DA65
        if (hi == 0x01 and lo == 0x0054DA65) or (lo == 0x0054DA65):
            return 0

        for slot in range(self.MAX_TAG_SLOTS):
            addr = self.USER_FLASH_ADDR + slot * self.FLASH_SLOT_SIZE
            magic = self.flash_read_word(addr)
            if magic == 0xFFFFFFFF:
                return -1
            if magic == self.FLASH_RECORD_MAGIC:
                s_hi = self.flash_read_word(addr + 4)
                s_lo = self.flash_read_word(addr + 8)
                if (s_hi == hi or s_hi == 0 or hi == 0) and (s_lo == lo):
                    return slot
        return -1

    def find_empty_slot(self):
        for slot in range(self.MAX_TAG_SLOTS):
            addr = self.USER_FLASH_ADDR + slot * self.FLASH_SLOT_SIZE
            magic = self.flash_read_word(addr)
            if magic == 0xFFFFFFFF:
                return slot
        return -1

    def save_tag_to_flash(self):
        if not self.tag_available:
            return 0, -1

        exist = self.find_tag_slot(self.tag_word_hi, self.tag_word_lo)
        if exist >= 0:
            return 2, exist

        slot = self.find_empty_slot()
        if slot < 0:
            return -1, -1

        addr = self.USER_FLASH_ADDR + slot * self.FLASH_SLOT_SIZE
        self.reg_gpio_leds |= 0x0008

        self.flash_write_word(addr + 0, self.FLASH_RECORD_MAGIC)
        self.flash_write_word(addr + 4, self.tag_word_hi)
        self.flash_write_word(addr + 8, self.tag_word_lo)
        self.flash_write_word(addr + 12, self.tag_word_hi ^ self.tag_word_lo)

        self.reg_gpio_leds &= ~0x0008

        v_magic = self.flash_read_word(addr + 0)
        v_hi = self.flash_read_word(addr + 4)
        v_lo = self.flash_read_word(addr + 8)

        if v_magic == self.FLASH_RECORD_MAGIC and v_hi == self.tag_word_hi and v_lo == self.tag_word_lo:
            return 1, slot
        return -2, -1

    def find_empty_log_slot(self):
        for slot in range(self.MAX_LOG_SLOTS):
            addr = self.LOG_FLASH_ADDR + slot * self.LOG_SLOT_SIZE
            magic = self.flash_read_word(addr)
            if magic == 0xFFFFFFFF:
                return slot
        return -1

    def append_access_log(self, success, hi, lo):
        slot = self.find_empty_log_slot()
        if slot < 0:
            return -1

        addr = self.LOG_FLASH_ADDR + slot * self.LOG_SLOT_SIZE
        status_magic = self.LOG_MAGIC_SUCC if success else self.LOG_MAGIC_FAIL
        seq = slot + 1

        self.reg_gpio_leds |= 0x0008
        self.flash_write_word(addr + 4, hi)
        self.flash_write_word(addr + 8, lo)
        self.flash_write_word(addr + 12, seq)
        self.flash_write_word(addr + 0, status_magic)
        self.reg_gpio_leds &= ~0x0008

        if self.flash_read_word(addr + 0) != status_magic:
            return -2
        return slot

    def execute_card_scan(self, tag_hex, hi, lo):
        tag_slot = self.find_tag_slot(hi, lo)
        is_granted = (tag_slot >= 0)
        log_slot = self.append_access_log(is_granted, hi, lo)

        if is_granted:
            self.reg_gpio_leds = (self.reg_gpio_leds & ~0x0002) | 0x0004
            self.uart_puts(f"ACCESS:GRANTED:SLOT:{tag_slot}:{tag_hex}:LOG:{max(0, log_slot)}\n")
        else:
            self.reg_gpio_leds = (self.reg_gpio_leds & ~0x0004) | 0x0002
            self.uart_puts(f"ACCESS:DENIED:{tag_hex}:LOG:{max(0, log_slot)}\n")

    def poll_rdm6300(self):
        if self.rdm_cooldown_cnt > 0:
            self.rdm_cooldown_cnt -= 1

        if self.reg_rfid_status & 0x01:
            hi = self.reg_rfid_tag_hi
            lo = self.reg_rfid_tag_lo
            self.reg_rfid_status = 1  # Clear hardware flag

            self.tag_available = True
            self.tag_word_hi = hi
            self.tag_word_lo = lo

            self.last_tag_hex = f"{hi:02X}{lo:08X}"

            if self.rdm_cooldown_cnt == 0 or self.tag_word_hi != self.last_scanned_hi or self.tag_word_lo != self.last_scanned_lo:
                self.last_scanned_hi = self.tag_word_hi
                self.last_scanned_lo = self.tag_word_lo
                self.rdm_cooldown_cnt = 250000
                self.execute_card_scan(self.last_tag_hex, self.tag_word_hi, self.tag_word_lo)

    # ------------------------------------------------------------------------
    # Command Interpreter Execution Loop
    # ------------------------------------------------------------------------
    def process_commands(self, max_cycles=10):
        for _ in range(max_cycles):
            self.poll_rdm6300()
            cmd = self.uart_getc_nonblock()
            if cmd < 0:
                break
            ch = chr(cmd)

            if ch in ('P', 'p'):
                self.uart_puts("PONG: PicoRV32 Active\n")
            elif ch in ('R', 'r'):
                if self.tag_available:
                    self.uart_puts(f"TAG:{self.last_tag_hex}\n")
                else:
                    self.uart_puts("ERR:NO_TAG\n")
            elif ch in ('W', 'w'):
                res, slot = self.save_tag_to_flash()
                if res == 1:
                    self.uart_puts(f"OK:SAVED:SLOT:{slot}:{self.last_tag_hex}\n")
                    self.reg_gpio_leds |= 0x0010
                elif res == 2:
                    self.uart_puts(f"INFO:EXISTS:SLOT:{slot}:{self.last_tag_hex}\n")
                elif res == -1:
                    self.uart_puts("ERR:FLASH_FULL\n")
                elif res == -2:
                    self.uart_puts("ERR:FLASH_WRITE_FAIL\n")
                else:
                    self.uart_puts("ERR:NO_TAG_TO_SAVE\n")
            elif ch in ('N', 'n'):
                input_tag = []
                while len(input_tag) < 10 and self.rx_fifo:
                    b = self.uart_getc_nonblock()
                    if b >= 0 and chr(b) not in ('\r', '\n'):
                        input_tag.append(chr(b))
                tag_str = "".join(input_tag)
                if len(tag_str) == 10:
                    self.tag_word_hi = int(tag_str[0:2], 16)
                    self.tag_word_lo = int(tag_str[2:10], 16)
                    self.tag_available = True
                    self.last_tag_hex = tag_str
                    res, slot = self.save_tag_to_flash()
                    if res == 1:
                        self.uart_puts(f"OK:MANUAL_TAG_SAVED:SLOT:{slot}:{self.last_tag_hex}\n")
                        self.reg_gpio_leds |= 0x0010
                    elif res == 2:
                        self.uart_puts(f"INFO:EXISTS:SLOT:{slot}:{self.last_tag_hex}\n")
                    elif res == -1:
                        self.uart_puts("ERR:FLASH_FULL\n")
                    else:
                        self.uart_puts("ERR:FLASH_WRITE_FAIL\n")
                else:
                    self.uart_puts("ERR:INVALID_LENGTH\n")
            elif ch in ('D', 'd'):
                self.uart_puts("DUMP:\n")
                for i in range(8):
                    a = self.USER_FLASH_ADDR + i * 4
                    w = self.flash_read_word(a)
                    self.uart_puts(f"{a:08X}: {w:08X}\n")
            elif ch in ('F', 'f'):
                count = 0
                self.uart_puts("TAGS_START\n")
                for slot in range(self.MAX_TAG_SLOTS):
                    addr = self.USER_FLASH_ADDR + slot * self.FLASH_SLOT_SIZE
                    magic = self.flash_read_word(addr)
                    if magic == 0xFFFFFFFF:
                        break
                    if magic == self.FLASH_RECORD_MAGIC:
                        hi = self.flash_read_word(addr + 4)
                        lo = self.flash_read_word(addr + 8)
                        count += 1
                        self.uart_puts(f"TAG_ITEM:{slot}:{hi:02X}{lo:08X}\n")
                if count == 0:
                    self.uart_puts("ERR:EMPTY_FLASH\n")
                else:
                    self.uart_puts(f"TAGS_TOTAL:{count}\n")
                self.uart_puts("TAGS_END\n")
            elif ch in ('E', 'e'):
                self.reg_gpio_leds |= 0x0008
                self.flash_erase_sector(self.USER_FLASH_ADDR)
                self.reg_gpio_leds &= ~0x0008
                self.uart_puts("OK:SECTOR_ERASED\n")
            elif ch in ('C', 'c'):
                input_tag = []
                while len(input_tag) < 10 and self.rx_fifo:
                    b = self.uart_getc_nonblock()
                    if b >= 0 and chr(b) not in ('\r', '\n'):
                        input_tag.append(chr(b))
                ctag = "".join(input_tag)
                if len(ctag) == 10:
                    c_hi = int(ctag[0:2], 16)
                    c_lo = int(ctag[2:10], 16)
                    slot = self.find_tag_slot(c_hi, c_lo)
                    if slot >= 0:
                        self.uart_puts(f"OK:TAG_FOUND:SLOT:{slot}:{ctag}\n")
                    else:
                        self.uart_puts("ERR:TAG_NOT_FOUND\n")
                else:
                    self.uart_puts("ERR:INVALID_LENGTH\n")
            elif ch in ('K', 'k'):
                input_tag = []
                while len(input_tag) < 10 and self.rx_fifo:
                    b = self.uart_getc_nonblock()
                    if b >= 0 and chr(b) not in ('\r', '\n'):
                        input_tag.append(chr(b))
                dtag = "".join(input_tag)
                if len(dtag) == 10:
                    d_hi = int(dtag[0:2], 16)
                    d_lo = int(dtag[2:10], 16)
                    slot = self.find_tag_slot(d_hi, d_lo)
                    if slot >= 0:
                        addr = self.USER_FLASH_ADDR + slot * self.FLASH_SLOT_SIZE
                        self.reg_gpio_leds |= 0x0008
                        self.flash_write_word(addr + 0, 0)
                        self.flash_write_word(addr + 4, 0)
                        self.flash_write_word(addr + 8, 0)
                        self.flash_write_word(addr + 12, 0)
                        self.reg_gpio_leds &= ~0x0008
                        self.uart_puts(f"OK:TAG_DELETED:SLOT:{slot}:{dtag}\n")
                    else:
                        self.uart_puts("ERR:TAG_NOT_FOUND\n")
                else:
                    self.uart_puts("ERR:INVALID_LENGTH\n")
            elif ch in ('V', 'v'):
                input_tag = []
                while len(input_tag) < 10 and self.rx_fifo:
                    b = self.uart_getc_nonblock()
                    if b >= 0 and chr(b) not in ('\r', '\n'):
                        input_tag.append(chr(b))
                vtag = "".join(input_tag)
                if len(vtag) == 10:
                    v_hi = int(vtag[0:2], 16)
                    v_lo = int(vtag[2:10], 16)
                    self.execute_card_scan(vtag, v_hi, v_lo)
                else:
                    self.uart_puts("ERR:INVALID_LENGTH\n")
            elif ch in ('L', 'l'):
                count = 0
                succ = 0
                fail = 0
                self.uart_puts("LOGS_START\n")
                for slot in range(self.MAX_LOG_SLOTS):
                    addr = self.LOG_FLASH_ADDR + slot * self.LOG_SLOT_SIZE
                    magic = self.flash_read_word(addr)
                    if magic == 0xFFFFFFFF:
                        break
                    if magic in (self.LOG_MAGIC_SUCC, self.LOG_MAGIC_FAIL):
                        hi = self.flash_read_word(addr + 4)
                        lo = self.flash_read_word(addr + 8)
                        seq = self.flash_read_word(addr + 12)
                        count += 1
                        m_str = "SUCC" if magic == self.LOG_MAGIC_SUCC else "FAIL"
                        if magic == self.LOG_MAGIC_SUCC: succ += 1
                        else: fail += 1
                        self.uart_puts(f"LOG_ITEM:{slot}:{m_str}:{hi:02X}{lo:08X}:{seq}\n")
                if count == 0:
                    self.uart_puts("ERR:EMPTY_LOGS\n")
                else:
                    self.uart_puts(f"LOGS_TOTAL:{count}:{succ}:{fail}\n")
                self.uart_puts("LOGS_END\n")
            elif ch in ('X', 'x'):
                self.reg_gpio_leds |= 0x0008
                self.flash_erase_sector(self.LOG_FLASH_ADDR)
                self.reg_gpio_leds &= ~0x0008
                self.uart_puts("OK:LOGS_ERASED\n")
            elif ch in ('S', 's'):
                fid = self.flash_read_id()
                fsr = self.flash_read_sr()
                self.uart_puts(f"STATUS: FlashID={fid:08X}, FlashSR={fsr:08X}, LEDs={self.reg_gpio_leds:08X}, TagAvailable={'1' if self.tag_available else '0'}\n")
            elif ch == '?':
                self.uart_puts("CMDS: P(Ping) R(ReadTag) W(WriteFlash) F(ReadFlash) E(EraseFlash) S(Status)\n")


# ----------------------------------------------------------------------------
# Test Suite Implementation
# ----------------------------------------------------------------------------
def run_test_suite():
    sim = FirmwareSimulator()
    passed = 0
    failed = 0
    total = 21

    print("======================================================================")
    print("  PicoRV32 RFID SoC - FIRMWARE UNIT & PROTOCOL TESTBENCH (Python Runner)")
    print("  Design Step: 3.2. Bước 2: Thiết Kế Firmware & Giao Thức (Software-First)")
    print("======================================================================")

    def test(num, name, cond, detail=""):
        nonlocal passed, failed
        if cond:
            passed += 1
            print(f"[{num:02d}] PASS: {name}")
        else:
            failed += 1
            print(f"[{num:02d}] FAIL: {name} --> {detail}")

    # TC01: Utility hex2val
    t1 = all([
        sim.hex2val('0') == 0,
        sim.hex2val('9') == 9,
        sim.hex2val('A') == 10,
        sim.hex2val('F') == 15,
        sim.hex2val('a') == 10,
        sim.hex2val('f') == 15,
        sim.hex2val('Z') == -1
    ])
    test(1, "TC01 - Utility hex2val() Conversion", t1)

    # TC02: Numerical Formatting
    sim.host_clear_tx()
    sim.uart_puthex32(0x1234ABCD)
    h_res = sim.host_read_line()
    sim.uart_putdec(7508976)
    d_res = sim.host_read_line()
    test(2, "TC02 - UART Formatting (Hex32 & Dec)", h_res == "1234ABCD" and d_res == "7508976")

    # TC03: Command 'P' (Ping)
    sim.host_clear_rx(); sim.host_clear_tx()
    sim.host_send_string("P\n")
    sim.process_commands()
    test(3, "TC03 - Command 'P' (Ping / Pong)", sim.host_read_line() == "PONG: PicoRV32 Active")

    # TC04: Command 'R' (Query Empty)
    sim.host_clear_rx(); sim.host_clear_tx()
    sim.tag_available = False
    sim.host_send_string("R\n")
    sim.process_commands()
    test(4, "TC04 - Command 'R' (Query Tag - Empty)", sim.host_read_line() == "ERR:NO_TAG")

    # TC05: Command 'E' (Erase Flash Sector 48)
    sim.host_clear_rx(); sim.host_clear_tx()
    sim.host_send_string("E\n")
    sim.process_commands()
    w_check = all(sim.flash_read_word(sim.USER_FLASH_ADDR + i * 4) == 0xFFFFFFFF for i in range(16))
    test(5, "TC05 - Command 'E' (Erase Flash Sector 48)", sim.host_read_line() == "OK:SECTOR_ERASED" and w_check)

    # TC06: Built-in Master Card Protection
    sim.host_clear_rx(); sim.host_clear_tx()
    sim.host_send_string("N010054DA65\n")
    sim.process_commands()
    test(6, "TC06 - Master Card Protection (010054DA65 is Authorized Slot 0)", sim.host_read_line() == "INFO:EXISTS:SLOT:0:010054DA65")

    # TC07: Manual Tag Registration to Flash Slot 0
    sim.host_clear_rx(); sim.host_clear_tx()
    sim.host_send_string("N00007293F0\n")
    sim.process_commands()
    rec_ok = (
        sim.flash_read_word(sim.USER_FLASH_ADDR + 0) == sim.FLASH_RECORD_MAGIC and
        sim.flash_read_word(sim.USER_FLASH_ADDR + 4) == 0x00 and
        sim.flash_read_word(sim.USER_FLASH_ADDR + 8) == 0x007293F0 and
        sim.flash_read_word(sim.USER_FLASH_ADDR + 12) == (0x00 ^ 0x007293F0)
    )
    test(7, "TC07 - Command 'N' (Save Real Tag 00007293F0 to Slot 0)", sim.host_read_line() == "OK:MANUAL_TAG_SAVED:SLOT:0:00007293F0" and rec_ok)

    # TC08: Anti-Duplicate Protection
    sim.host_clear_rx(); sim.host_clear_tx()
    sim.host_send_string("N00007293F0\n")
    sim.process_commands()
    test(8, "TC08 - Anti-Duplicate Protection ('N' for existing card)", sim.host_read_line() == "INFO:EXISTS:SLOT:0:00007293F0")

    # TC09: Sequential Multi-Tag Registration (Slots 1 & 2)
    sim.host_clear_rx(); sim.host_clear_tx()
    sim.host_send_string("N000073161D\n")
    sim.process_commands()
    l1 = sim.host_read_line()
    sim.host_send_string("N0000A1B2C3\n")
    sim.process_commands()
    l2 = sim.host_read_line()
    test(9, "TC09 - Sequential Multi-Tag Allocation (Slots 1 & 2)", l1 == "OK:MANUAL_TAG_SAVED:SLOT:1:000073161D" and l2 == "OK:MANUAL_TAG_SAVED:SLOT:2:0000A1B2C3")

    # TC10: Check Tag Existence ('C')
    sim.host_clear_rx(); sim.host_clear_tx()
    sim.host_send_string("C00007293F0\n")
    sim.process_commands()
    c1 = sim.host_read_line()
    sim.host_send_string("C010054DA65\n")
    sim.process_commands()
    c2 = sim.host_read_line()
    sim.host_send_string("C9999999999\n")
    sim.process_commands()
    c3 = sim.host_read_line()
    test(10, "TC10 - Command 'C' (Query Tag Existence in Flash & Master)", c1 == "OK:TAG_FOUND:SLOT:0:00007293F0" and c2 == "OK:TAG_FOUND:SLOT:0:010054DA65" and c3 == "ERR:TAG_NOT_FOUND")

    # TC11: List All Tags ('F')
    sim.host_clear_rx(); sim.host_clear_tx()
    sim.host_send_string("F\n")
    sim.process_commands()
    f_lines = [sim.host_read_line() for _ in range(6)]
    expected_f = ["TAGS_START", "TAG_ITEM:0:00007293F0", "TAG_ITEM:1:000073161D", "TAG_ITEM:2:0000A1B2C3", "TAGS_TOTAL:3", "TAGS_END"]
    test(11, "TC11 - Command 'F' (Enumerate All Stored Tags)", f_lines == expected_f)

    # TC12: Virtual Scan 'V' (Authorized Card)
    sim.flash_erase_sector(sim.LOG_FLASH_ADDR)
    sim.host_clear_rx(); sim.host_clear_tx()
    sim.host_send_string("V00007293F0\n")
    sim.process_commands()
    v1 = sim.host_read_line()
    log0_magic = sim.flash_read_word(sim.LOG_FLASH_ADDR + 0)
    led_green = (sim.reg_gpio_leds & 0x0004) != 0 and (sim.reg_gpio_leds & 0x0002) == 0
    test(12, "TC12 - Virtual Scan 'V' (Authorized Card: Access Granted)", v1 == "ACCESS:GRANTED:SLOT:0:00007293F0:LOG:0" and log0_magic == sim.LOG_MAGIC_SUCC and led_green)

    # TC13: Virtual Scan 'V' (Unauthorized Card)
    sim.host_clear_rx(); sim.host_clear_tx()
    sim.host_send_string("V00DEADBEEF\n")
    sim.process_commands()
    v2 = sim.host_read_line()
    log1_magic = sim.flash_read_word(sim.LOG_FLASH_ADDR + sim.LOG_SLOT_SIZE + 0)
    led_red = (sim.reg_gpio_leds & 0x0002) != 0 and (sim.reg_gpio_leds & 0x0004) == 0
    test(13, "TC13 - Virtual Scan 'V' (Unauthorized Card: Access Denied)", v2 == "ACCESS:DENIED:00DEADBEEF:LOG:1" and log1_magic == sim.LOG_MAGIC_FAIL and led_red)

    # TC14: Read Access Logs ('L')
    sim.host_clear_rx(); sim.host_clear_tx()
    sim.host_send_string("L\n")
    sim.process_commands()
    l_lines = [sim.host_read_line() for _ in range(5)]
    expected_l = ["LOGS_START", "LOG_ITEM:0:SUCC:00007293F0:1", "LOG_ITEM:1:FAIL:00DEADBEEF:2", "LOGS_TOTAL:2:1:1", "LOGS_END"]
    test(14, "TC14 - Command 'L' (Read Access Logs History)", l_lines == expected_l)

    # TC15: Soft Delete Tag ('K')
    sim.host_clear_rx(); sim.host_clear_tx()
    sim.host_send_string("K00007293F0\n")
    sim.process_commands()
    k1 = sim.host_read_line()
    slot0_zeroed = sim.flash_read_word(sim.USER_FLASH_ADDR + 0) == 0
    sim.host_send_string("C00007293F0\n")
    sim.process_commands()
    k2 = sim.host_read_line()
    test(15, "TC15 - Command 'K' (Soft Invalidate Tag in Flash)", k1 == "OK:TAG_DELETED:SLOT:0:00007293F0" and slot0_zeroed and k2 == "ERR:TAG_NOT_FOUND")

    # TC16: Erase Access Logs Sector ('X')
    sim.host_clear_rx(); sim.host_clear_tx()
    sim.host_send_string("X\n")
    sim.process_commands()
    x1 = sim.host_read_line()
    sim.host_send_string("L\n")
    sim.process_commands()
    x_lines = [sim.host_read_line() for _ in range(3)]
    test(16, "TC16 - Command 'X' (Erase Access Logs Sector 49)", x1 == "OK:LOGS_ERASED" and x_lines == ["LOGS_START", "ERR:EMPTY_LOGS", "LOGS_END"])

    # TC17: Hardware Status Command ('S')
    sim.host_clear_rx(); sim.host_clear_tx()
    sim.host_send_string("S\n")
    sim.process_commands()
    s_line = sim.host_read_line()
    test(17, "TC17 - Command 'S' (Hardware Status Query)", "STATUS: FlashID=00010215" in s_line and "FlashSR=00000000" in s_line)

    # TC18: Help Command ('?')
    sim.host_clear_rx(); sim.host_clear_tx()
    sim.host_send_string("?\n")
    sim.process_commands()
    test(18, "TC18 - Command '?' (Host Help Interface)", "CMDS: P(Ping)" in sim.host_read_line())

    # TC19: Error Handling (Short / Malformed Tag UID)
    sim.host_clear_rx(); sim.host_clear_tx()
    sim.host_send_string("N123456789\n")
    sim.process_commands()
    test(19, "TC19 - Error Handling (Truncated 9-char Tag Input)", sim.host_read_line() == "ERR:INVALID_LENGTH")

    # TC20: Hardware MMIO Interrupt & Polling Trigger (`poll_rdm6300`)
    sim.reg_rfid_status = 0x01
    sim.reg_rfid_tag_hi = 0x01
    sim.reg_rfid_tag_lo = 0x0054DA65
    sim.rdm_cooldown_cnt = 0
    sim.host_clear_rx(); sim.host_clear_tx()
    sim.poll_rdm6300()
    mmio_ok = (
        sim.reg_rfid_status == 1 and
        sim.tag_available == True and
        sim.tag_word_hi == 0x01 and
        sim.tag_word_lo == 0x0054DA65 and
        sim.last_tag_hex == "010054DA65" and
        sim.rdm_cooldown_cnt == 250000
    )
    mmio_out = sim.host_read_line()
    test(20, "TC20 - Hardware MMIO Integration (poll_rdm6300 Handshake)", mmio_ok and "ACCESS:GRANTED:SLOT:0:010054DA65" in mmio_out)

    # TC21: Command 'D' (Raw 32-bit Memory Dump)
    sim.host_clear_rx(); sim.host_clear_tx()
    sim.host_send_string("D\n")
    sim.process_commands()
    d_header = sim.host_read_line()
    d_lines = [sim.host_read_line() for _ in range(8)]
    test(21, "TC21 - Command 'D' (Raw 32-bit Flash Memory Dump)", d_header == "DUMP:" and len(d_lines) == 8 and all(":" in l for l in d_lines))

    print("\n======================================================================")
    print("  TEST EXECUTION SUMMARY")
    print("======================================================================")
    print(f"  Total Test Cases Run   : {total}")
    print(f"  Test Cases Passed      : {passed} ({passed*100.0/total:.1f}%)")
    print(f"  Test Cases Failed      : {failed}")
    print("======================================================================")

    if failed == 0:
        print("  >>> ALL 21 FIRMWARE PROTOCOL & UNIT TESTS PASSED (100%)! <<<")
        return 0
    else:
        print("  >>> SOME TESTS FAILED! <<<")
        return 1

if __name__ == '__main__':
    sys.exit(run_test_suite())
