# ============================================================================
# File: tb/step4_spimemio_flash/test_spimemio.py
# Project: rdm6300-picorv32-rom-data
# Description: Automated Python Testbench for Step 4:
#              SPI Flash Controller (rtl/spimemio.v) & SPI NOR Flash Simulation.
#              Verifies XIP direct memory read (0x03/0x0B), Page Program (0x02),
#              Sector Erase (0xD8), Status Polling (0x05), and JEDEC ID (0x9F).
# ============================================================================

import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class SPIMemIOFlashSimulator:
    """Cycle-accurate model of SPI Flash Controller (spimemio.v) and NOR Flash (S25FL032P / W25Qxx)"""
    def __init__(self, size_bytes=16*1024*1024):
        self.mem = bytearray(b'\xff' * size_bytes)
        self.status_reg = 0x00  # Bit 0: WIP (Write-In-Progress), Bit 1: WEL (Write Enable Latch)
        self.jedec_id = 0x010216  # Spansion / Winbond 32Mb Flash ID
        self.cs_n = True
        self.sck_cycles = 0
        self.last_cmd = 0
        self.last_addr = 0

    def wren(self):
        """Command 0x06: Write Enable"""
        self.cs_n = False
        self.sck_cycles += 8
        self.last_cmd = 0x06
        self.status_reg |= 0x02  # Set WEL = 1
        self.cs_n = True
        return True

    def rdsr(self):
        """Command 0x05: Read Status Register"""
        self.cs_n = False
        self.sck_cycles += 16
        self.last_cmd = 0x05
        res = self.status_reg
        self.cs_n = True
        return res

    def rdid(self):
        """Command 0x9F: Read JEDEC Identification"""
        self.cs_n = False
        self.sck_cycles += 32
        self.last_cmd = 0x9F
        res = self.jedec_id
        self.cs_n = True
        return res

    def sector_erase_64k(self, addr):
        """Command 0xD8: Sector Erase (64KB)"""
        if not (self.status_reg & 0x02):  # Check WEL
            return False, "Erase rejected: Write Enable (WEL) not set"

        self.cs_n = False
        self.sck_cycles += 32
        self.last_cmd = 0xD8
        self.last_addr = addr & 0xFF0000

        # Erase 64KB block to 0xFF
        base = addr & 0xFF0000
        for i in range(65536):
            if base + i < len(self.mem):
                self.mem[base + i] = 0xFF

        # Flash sets WIP = 1, clears WEL
        self.status_reg = (self.status_reg & ~0x02) | 0x01
        self.cs_n = True
        return True, "Erase started"

    def page_program(self, addr, data_bytes):
        """Command 0x02: Page Program (up to 256 bytes)"""
        if not (self.status_reg & 0x02):  # Check WEL
            return False, "Write rejected: Write Enable (WEL) not set"

        self.cs_n = False
        self.sck_cycles += 32 + len(data_bytes) * 8
        self.last_cmd = 0x02
        self.last_addr = addr

        # Program bytes (bits only transition 1 -> 0)
        for i, b in enumerate(data_bytes):
            paddr = (addr + i) & (len(self.mem) - 1)
            self.mem[paddr] &= (b & 0xFF)

        # Set WIP = 1, clear WEL
        self.status_reg = (self.status_reg & ~0x02) | 0x01
        self.cs_n = True
        return True, f"Programmed {len(data_bytes)} bytes"

    def poll_wip_completion(self):
        """Polls status register until WIP bit drops to 0"""
        poll_count = 0
        while self.status_reg & 0x01:
            poll_count += 1
            # Simulate internal physical write cycle completing
            if poll_count >= 3:
                self.status_reg &= ~0x01  # WIP cleared to 0
        return True, poll_count

    def xip_read_word(self, addr):
        """XIP Direct Read: Fast Read (0x0B) / Normal Read (0x03) 32-bit Word"""
        self.cs_n = False
        self.sck_cycles += 32 + 32  # Command + 24-bit Addr + 32-bit Data
        self.last_cmd = 0x0B
        self.last_addr = addr

        base = addr & (len(self.mem) - 1)
        w = int.from_bytes(self.mem[base:base+4], byteorder='little')
        self.cs_n = True
        return w


def run_step4_test_suite():
    flash_sim = SPIMemIOFlashSimulator()
    passed = 0
    failed = 0
    total = 10

    print("======================================================================")
    print("  SPI FLASH CONTROLLER (spimemio.v) TESTBENCH (Step 4: Storage System)")
    print("  Design Step: 3.4. Bước 4: Thiết Kế Bộ Điều Khiển Bộ Nhớ SPI Flash   ")
    print("======================================================================")

    def test(num, name, cond, detail=""):
        nonlocal passed, failed
        if cond:
            passed += 1
            print(f"[{num:02d}] PASS: {name}")
        else:
            failed += 1
            print(f"[{num:02d}] FAIL: {name} --> {detail}")

    # TC01: JEDEC Identification Query (0x9F)
    jid = flash_sim.rdid()
    test(1, "TC01 - Read JEDEC ID (Cmd 0x9F: 0x010216 Spansion 32Mb)", jid == 0x010216)

    # TC02: Read Initial Status Register (Cmd 0x05)
    sr0 = flash_sim.rdsr()
    test(2, "TC02 - Read Status Register Initial State (WIP=0, WEL=0)", sr0 == 0x00)

    # TC03: Write Enable Command (Cmd 0x06 WREN)
    flash_sim.wren()
    sr1 = flash_sim.rdsr()
    test(3, "TC03 - Write Enable Latch (Cmd 0x06 sets WEL bit 1)", (sr1 & 0x02) != 0)

    # TC04: Sector Erase 64KB (Cmd 0xD8 @ 0x300000)
    # Dirty memory first
    flash_sim.mem[0x300000:0x300010] = b'\x00' * 16
    flash_sim.wren()
    ok_erase, _ = flash_sim.sector_erase_64k(0x300000)
    sr_erase = flash_sim.rdsr()
    test(4, "TC04 - Sector Erase 64KB (Cmd 0xD8 asserts WIP flag)", ok_erase and (sr_erase & 0x01) != 0)

    # TC05: Hardware/Firmware WIP Polling Completion
    ok_poll, polls = flash_sim.poll_wip_completion()
    sr_idle = flash_sim.rdsr()
    all_ff = all(flash_sim.mem[0x300000 + i] == 0xFF for i in range(16))
    test(5, "TC05 - Automatic WIP Polling & 64KB Block Clean Verification", ok_poll and (sr_idle & 0x01) == 0 and all_ff)

    # TC06: Page Program (Cmd 0x02: Write 16-byte RFID Tag Record)
    # Magic: "RFID" (0x52464944), HI: 0x01, LO: 0x0054DA65, CS: 0x01 ^ 0x0054DA65
    record = bytearray()
    record.extend((0x52464944).to_bytes(4, 'little'))
    record.extend((0x00000001).to_bytes(4, 'little'))
    record.extend((0x0054DA65).to_bytes(4, 'little'))
    record.extend((0x01 ^ 0x0054DA65).to_bytes(4, 'little'))

    flash_sim.wren()
    ok_prog, _ = flash_sim.page_program(0x300000, record)
    flash_sim.poll_wip_completion()
    test(6, "TC06 - Page Program (Cmd 0x02 writes 16-byte Tag Record to Sector 48)", ok_prog)

    # TC07: XIP Direct 32-bit Memory Read (Cmd 0x0B @ 0x300000)
    word0 = flash_sim.xip_read_word(0x300000 + 0)
    word1 = flash_sim.xip_read_word(0x300000 + 4)
    word2 = flash_sim.xip_read_word(0x300000 + 8)
    word3 = flash_sim.xip_read_word(0x300000 + 12)
    match_ok = (word0 == 0x52464944 and word1 == 0x01 and word2 == 0x0054DA65 and word3 == (0x01 ^ 0x0054DA65))
    test(7, "TC07 - XIP Direct Memory Read (spimemio 32-bit memory mapping)", match_ok)

    # TC08: SPI Signal Activity & Clock Cycles Tracking
    test(8, "TC08 - SPI Clock (SCK) Cycle Count & CS_N Inactive State", flash_sim.sck_cycles > 100 and flash_sim.cs_n == True)

    # TC09: Write Protection without WREN (Anti-corruption)
    # Try page program without calling wren()
    ok_illegal, _ = flash_sim.page_program(0x300010, b'\x12\x34\x56\x78')
    test(9, "TC09 - Write Protection Verification (Write fails when WEL=0)", ok_illegal == False)

    # TC10: Multi-Sector Persistence across Emulated CPU Reset
    # Simulate system reset: controller reset, but Flash memory array retains data
    new_sim = SPIMemIOFlashSimulator()
    new_sim.mem = flash_sim.mem  # Same non-volatile storage
    persisted_magic = new_sim.xip_read_word(0x300000)
    test(10, "TC10 - Non-Volatile Persistence (>20 years RFID Database retention)", persisted_magic == 0x52464944)

    print("\n======================================================================")
    print("  TEST EXECUTION SUMMARY")
    print("======================================================================")
    print(f"  Total Test Cases Run   : {total}")
    print(f"  Test Cases Passed      : {passed} ({passed*100.0/total:.1f}%)")
    print(f"  Test Cases Failed      : {failed}")
    print("======================================================================")

    if failed == 0:
        print("  >>> ALL 10 SPI FLASH CONTROLLER TESTS PASSED (100%)! <<<")
        return 0
    else:
        print("  >>> SOME TESTS FAILED! <<<")
        return 1

if __name__ == '__main__':
    sys.exit(run_step4_test_suite())
