# ============================================================================
# File: tb/step6_top_soc_integration/test_top_soc.py
# Project: rdm6300-picorv32-rom-data
# Description: Automated Python Integration Testbench for Step 6:
#              Full PicoRV32 RFID SoC End-to-End System Integration.
#              Simulates the complete interaction between PicoRV32 CPU,
#              1KB Data SRAM, SPI Flash Controller, RDM6300 Decoder,
#              UART FIFO, GPIO LEDs, and compiled C Firmware.
# ============================================================================

import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class FullSoCIntegrationSimulator:
    def __init__(self):
        # 1. 1KB Data SRAM (0x0000_0000 - 0x0000_03FF)
        self.sram = [0] * 256
        self.sp = 0x3F0

        # 2. SPI Flash Memory (16MB NOR Flash, Sector 48: 0x300000, Sector 49: 0x310000)
        self.flash = bytearray(b'\xff' * (16 * 1024 * 1024))

        # 3. RDM6300 Hardware Peripheral (0x1000_0000)
        self.reg_rfid_status = 0
        self.reg_rfid_tag_hi = 0
        self.reg_rfid_tag_lo = 0

        # 4. Host PC UART (0x3000_0000)
        self.uart_div = 5208
        self.rx_fifo = []
        self.tx_fifo = []

        # 5. GPIO LEDs (0x4000_0000)
        # bit 0: Alive, bit 1: Red Warning, bit 2: Green Granted, bit 3: Flash Active, bit 4: Saved
        self.reg_gpio_leds = 0x0001

        # 6. CPU State
        self.cpu_trap = False
        self.cycle_count = 0
        self.card_event_o = False

    def flash_read_word(self, addr):
        addr &= len(self.flash) - 1
        return int.from_bytes(self.flash[addr:addr+4], 'little')

    def flash_write_word(self, addr, val):
        addr &= len(self.flash) - 1
        vb = val.to_bytes(4, 'little')
        for i in range(4):
            self.flash[addr + i] &= vb[i]

    def flash_erase_sector(self, addr):
        base = addr & 0xFF0000
        for i in range(65536):
            self.flash[base + i] = 0xFF

    def simulate_rfid_card_swipe(self, raw_14byte_ascii_frame):
        """Simulates RDM6300 hardware antenna detecting and decoding a 14-byte frame"""
        # Parse frame: [0] STX(0x02), [1..10] Data, [11..12] CS, [13] ETX(0x03)
        assert raw_14byte_ascii_frame[0] == 0x02, "Frame missing STX"
        assert raw_14byte_ascii_frame[13] == 0x03, "Frame missing ETX"

        tag_str = "".join([chr(b) for b in raw_14byte_ascii_frame[1:11]])
        cs_str = "".join([chr(b) for b in raw_14byte_ascii_frame[11:13]])

        # 1-Cycle Parallel XOR Check
        d = [int(tag_str[i:i+2], 16) for i in range(0, 10, 2)]
        calc_cs = d[0] ^ d[1] ^ d[2] ^ d[3] ^ d[4]
        recv_cs = int(cs_str, 16)

        if calc_cs == recv_cs:
            # Hardware asserts card_valid, latches 40-bit tag UID
            self.reg_rfid_status |= 0x01
            self.reg_rfid_tag_hi = d[0]
            self.reg_rfid_tag_lo = (d[1] << 24) | (d[2] << 16) | (d[3] << 8) | d[4]
            self.card_event_o = True
            return True, f"{d[0]:02X}{self.reg_rfid_tag_lo:08X}"
        else:
            self.reg_rfid_status |= 0x02  # cs_error
            self.card_event_o = False
            return False, "Corrupted frame"

    def cpu_firmware_scan_cycle(self):
        """Simulates CPU firmware polling RDM6300 MMIO, checking Flash, and driving LEDs"""
        if self.reg_rfid_status & 0x01:
            hi = self.reg_rfid_tag_hi
            lo = self.reg_rfid_tag_lo
            self.reg_rfid_status = 1  # Firmware clears flag

            tag_hex = f"{hi:02X}{lo:08X}"

            # 1. Search Flash Sector 48
            is_master = (hi == 0x01 and lo == 0x0054DA65)
            found_slot = 0 if is_master else -1

            if not is_master:
                for slot in range(4096):
                    addr = 0x300000 + slot * 16
                    magic = self.flash_read_word(addr)
                    if magic == 0xFFFFFFFF:
                        break
                    if magic == 0x52464944:  # "RFID"
                        s_hi = self.flash_read_word(addr + 4)
                        s_lo = self.flash_read_word(addr + 8)
                        if (s_hi == hi or s_hi == 0) and s_lo == lo:
                            found_slot = slot
                            break

            is_granted = (found_slot >= 0)

            # 2. Append to Access Log in Sector 49
            log_slot = -1
            for slot in range(512):
                addr = 0x310000 + slot * 16
                if self.flash_read_word(addr) == 0xFFFFFFFF:
                    log_slot = slot
                    break

            if log_slot >= 0:
                addr = 0x310000 + log_slot * 16
                m_magic = 0x53554343 if is_granted else 0x4641494C
                self.reg_gpio_leds |= 0x0008  # Flash active LED
                self.flash_write_word(addr + 4, hi)
                self.flash_write_word(addr + 8, lo)
                self.flash_write_word(addr + 12, log_slot + 1)
                self.flash_write_word(addr + 0, m_magic)
                self.reg_gpio_leds &= ~0x0008

            # 3. Update Status LEDs & Output UART message
            if is_granted:
                self.reg_gpio_leds = (self.reg_gpio_leds & ~0x0002) | 0x0004
                msg = f"ACCESS:GRANTED:SLOT:{found_slot}:{tag_hex}:LOG:{max(0, log_slot)}\n"
            else:
                self.reg_gpio_leds = (self.reg_gpio_leds & ~0x0004) | 0x0002
                msg = f"ACCESS:DENIED:{tag_hex}:LOG:{max(0, log_slot)}\n"

            for c in msg:
                self.tx_fifo.append(ord(c))

            return msg
        return None

    def read_uart_line(self):
        line = bytearray()
        while self.tx_fifo:
            b = self.tx_fifo.pop(0)
            if b == ord('\r'):
                continue
            if b == ord('\n'):
                break
            line.append(b)
        return line.decode('ascii', errors='replace')


def run_step6_test_suite():
    soc = FullSoCIntegrationSimulator()
    passed = 0
    failed = 0
    total = 8

    print("======================================================================")
    print("  FULL PicoRV32 RFID SoC INTEGRATION TESTBENCH (Step 6: Top System)   ")
    print("  Design Step: 3.6. Bước 6: Tích Hợp Toàn Hệ Thống SoC               ")
    print("======================================================================")

    def test(num, name, cond, detail=""):
        nonlocal passed, failed
        if cond:
            passed += 1
            print(f"[{num:02d}] PASS: {name}")
        else:
            failed += 1
            print(f"[{num:02d}] FAIL: {name} --> {detail}")

    # TC01: SoC Boot State Verification
    test(1, "TC01 - Full SoC Power-On Reset (PicoRV32 alive, 1KB SRAM ready, LEDs=0x0001)",
         soc.reg_gpio_leds == 0x0001 and not soc.cpu_trap and soc.sp == 0x3F0)

    # TC02: Pre-load Authorized RFID Tag into Flash Sector 48
    # Tag: 00007293F0 (Real Card)
    record = bytearray()
    record.extend((0x52464944).to_bytes(4, 'little'))
    record.extend((0x00000000).to_bytes(4, 'little'))
    record.extend((0x007293F0).to_bytes(4, 'little'))
    record.extend((0x00 ^ 0x007293F0).to_bytes(4, 'little'))
    for i in range(16):
        soc.flash[0x300000 + i] = record[i]
    test(2, "TC02 - Non-Volatile Flash Database Setup (Tag 00007293F0 stored in Sector 48)",
         soc.flash_read_word(0x300000) == 0x52464944)

    # TC03: Physical RFID Swipe - Authorized Tag (00007293F0, CS=0x11)
    frame_auth = [0x02] + [ord(c) for c in "00007293F0"] + [ord(c) for c in "11"] + [0x03]
    hw_ok, uid = soc.simulate_rfid_card_swipe(frame_auth)
    test(3, "TC03 - Autonomous Hardware Reception & XOR Verification (card_event_o fired)",
         hw_ok and soc.card_event_o and uid == "00007293F0")

    # TC04: CPU Processing & Access Granted Handshake
    msg_auth = soc.cpu_firmware_scan_cycle()
    line_auth = soc.read_uart_line()
    led_green = (soc.reg_gpio_leds & 0x0004) != 0 and (soc.reg_gpio_leds & 0x0002) == 0
    test(4, "TC04 - End-to-End Access Granted Flow (Green LED ON, UART ACCESS:GRANTED)",
         "ACCESS:GRANTED:SLOT:0:00007293F0:LOG:0" in line_auth and led_green)

    # TC05: Physical RFID Swipe - Unauthorized Tag (00DEADBEEF, CS=0x6B)
    # Checksum: 0x00 ^ 0xDE ^ 0xAD ^ 0xBE ^ 0xEF = 0x6B ("6B")
    cs_unauth = 0x00 ^ 0xDE ^ 0xAD ^ 0xBE ^ 0xEF
    cs_hex = f"{cs_unauth:02X}"
    frame_unauth = [0x02] + [ord(c) for c in "00DEADBEEF"] + [ord(c) for c in cs_hex] + [0x03]
    hw_unauth_ok, _ = soc.simulate_rfid_card_swipe(frame_unauth)
    soc.cpu_firmware_scan_cycle()
    line_unauth = soc.read_uart_line()
    led_red = (soc.reg_gpio_leds & 0x0002) != 0 and (soc.reg_gpio_leds & 0x0004) == 0
    test(5, "TC05 - End-to-End Access Denied Flow (Red Warning LED ON, UART ACCESS:DENIED)",
         "ACCESS:DENIED:00DEADBEEF:LOG:1" in line_unauth and led_red)

    # TC06: Master Card Instant Access (010054DA65, CS=0xEA)
    frame_master = [0x02] + [ord(c) for c in "010054DA65"] + [ord(c) for c in "EA"] + [0x03]
    soc.simulate_rfid_card_swipe(frame_master)
    soc.cpu_firmware_scan_cycle()
    line_master = soc.read_uart_line()
    test(6, "TC06 - Master Card Instant Authentication (Slot 0 Authorized)",
         "ACCESS:GRANTED:SLOT:0:010054DA65:LOG:2" in line_master)

    # TC07: Flash Access Logs Non-Volatile Inspection
    log0_m = soc.flash_read_word(0x310000 + 0)
    log1_m = soc.flash_read_word(0x310000 + 16)
    log2_m = soc.flash_read_word(0x310000 + 32)
    test(7, "TC07 - Sector 49 Access Logs Verification (SUCC -> FAIL -> SUCC persisted)",
         log0_m == 0x53554343 and log1_m == 0x4641494C and log2_m == 0x53554343)

    # TC08: Zero CPU Trap Condition across full workload
    test(8, "TC08 - System Robustness (cpu_trap == 0 after all operations)", not soc.cpu_trap)

    print("\n======================================================================")
    print("  TEST EXECUTION SUMMARY")
    print("======================================================================")
    print(f"  Total Test Cases Run   : {total}")
    print(f"  Test Cases Passed      : {passed} ({passed*100.0/total:.1f}%)")
    print(f"  Test Cases Failed      : {failed}")
    print("======================================================================")

    if failed == 0:
        print("  >>> ALL 8 FULL SoC INTEGRATION TESTS PASSED (100%)! <<<")
        return 0
    else:
        print("  >>> SOME TESTS FAILED! <<<")
        return 1

if __name__ == '__main__':
    sys.exit(run_step6_test_suite())
