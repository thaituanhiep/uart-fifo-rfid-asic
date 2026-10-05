# -*- coding: utf-8 -*-
"""
Script: reorder_slides_perfect.py
Chuyển 2 slide Testbench xuống ngay trước Phần 5 Demo (Vị trí Slide 20 & 21).
Các slide biến địa chỉ MMIO C chuyển lên vị trí Slide 14..19.
"""
import os
import re

cur_dir = os.path.dirname(os.path.abspath(__file__))
target_file = os.path.join(cur_dir, "create_presentation.py")

with open(target_file, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Extract Slide 14 & 15 (Testbench 1 & Testbench 2)
tb_pattern = r'(    # =========================================================================\s+# SLIDE 14: PHẦN 4 - HỆ THỐNG TESTBENCH: UART RTL.*?(?=    # =========================================================================\s+# SLIDE 16: BIẾN ĐỊA CHỈ 1))'
tb_match = re.search(tb_pattern, text, re.DOTALL)
assert tb_match, "Could not find tb_block!"
tb_block = tb_match.group(1)

# 2. Extract Slide 16..21 (6 Address Variables)
addr_pattern = r'(    # =========================================================================\s+# SLIDE 16: BIẾN ĐỊA CHỈ 1.*?(?=    # =========================================================================\s+# SLIDE 22: PHẦN 5 - DEMO THỰC NGHIỆM))'
addr_match = re.search(addr_pattern, text, re.DOTALL)
assert addr_match, "Could not find addr_block!"
addr_block = addr_match.group(1)

# 3. Renumber addr_block: Slide 16..21 -> Slide 14..19
# Variables: s16->s14, s17->s15, s18->s16, s19->s17, s20->s18, s21->s19
new_addr_block = addr_block
for old_s, new_s, old_num, new_num in [
    ("s16", "s14", "16", "14"),
    ("s17", "s15", "17", "15"),
    ("s18", "s16", "18", "16"),
    ("s19", "s17", "19", "17"),
    ("s20", "s18", "20", "18"),
    ("s21", "s19", "21", "19")
]:
    new_addr_block = re.sub(rf'\bSLIDE {old_num}:', f'SLIDE {new_num}:', new_addr_block)
    new_addr_block = re.sub(rf'\b{old_s}\b', f'{new_s}', new_addr_block)
    new_addr_block = re.sub(rf'\bcard_{old_s}\b', f'card_{new_s}', new_addr_block)
    new_addr_block = re.sub(rf'\btb_{old_s}\b', f'tb_{new_s}', new_addr_block)
    new_addr_block = re.sub(rf'\btf_{old_s}\b', f'tf_{new_s}', new_addr_block)
    new_addr_block = re.sub(rf'\badd_header\({new_s},\s*([^,]+),\s*([^,]+),\s*{old_num}\b', rf'add_header({new_s}, \1, \2, {new_num}', new_addr_block)

# 4. Renumber tb_block: Slide 14..15 -> Slide 20..21
new_tb_block = tb_block
for old_s, new_s, old_num, new_num in [
    ("s14", "s20", "14", "20"),
    ("s15", "s21", "15", "21")
]:
    new_tb_block = re.sub(rf'\bSLIDE {old_num}:', f'SLIDE {new_num}:', new_tb_block)
    new_tb_block = re.sub(rf'\b{old_s}\b', f'{new_s}', new_tb_block)
    new_tb_block = re.sub(rf'\badd_header\({new_s},\s*([^,]+),\s*([^,]+),\s*{old_num}\b', rf'add_header({new_s}, \1, \2, {new_num}', new_tb_block)

# 5. Swap the order: new_addr_block followed by new_tb_block
combined_block = new_addr_block + new_tb_block

# Replace the entire region (from Slide 14 to before Slide 22)
full_region_pattern = r'    # =========================================================================\s+# SLIDE 14: PHẦN 4 - HỆ THỐNG TESTBENCH: UART RTL.*?(?=    # =========================================================================\s+# SLIDE 22: PHẦN 5 - DEMO THỰC NGHIỆM)'

text = re.sub(full_region_pattern, combined_block, text, flags=re.DOTALL)

# 6. Update docstring
doc_old = """- Slide 14: Phần 4 - Testbench 1: Kiểm Thử Phần Cứng RTL Thuần Cho UART MMIO & FIFO (tb_uart_rtl.v)
- Slide 15: Phần 4 - Testbench 2: Kiểm Thử Tích Hợp Toàn Diện Top SoC Boot Flash & Ping (tb_uart_ping.v)
- Slide 16: Biến Địa Chỉ 1: REG_RFID_UART_DAT & DIV (0x1000_0004 & 0x1000_0000) - Đọc RFID RX FIFO
- Slide 17: Biến Địa Chỉ 2: REG_PC_UART_DAT & DIV (0x3000_0004 & 0x3000_0000) - Giao Tiếp Host PC UART
- Slide 18: Biến Địa Chỉ 3: REG_GPIO_LEDS (0x4000_0000) - Điều Khiển LED Trạng Thái & Relay Mở Cửa
- Slide 19: Biến Địa Chỉ 4: USER_FLASH_ADDR (0x0030_0000 - Sector 48) - Cơ Sở Dữ Liệu Thẻ Whitelist
- Slide 20: Biến Địa Chỉ 5: LOG_FLASH_ADDR (0x0031_0000 - Sector 49) - Nhật Ký Quẹt Thẻ Access Logs
- Slide 21: Biến Địa Chỉ 6: 0x0200_0000 & flashio_worker - Nạp Routine Vào SRAM Lập Trình Flash NVM"""

doc_new = """- Slide 14: Biến Địa Chỉ 1: REG_RFID_UART_DAT & DIV (0x1000_0004 & 0x1000_0000) - Đọc RFID RX FIFO
- Slide 15: Biến Địa Chỉ 2: REG_PC_UART_DAT & DIV (0x3000_0004 & 0x3000_0000) - Giao Tiếp Host PC UART
- Slide 16: Biến Địa Chỉ 3: REG_GPIO_LEDS (0x4000_0000) - Điều Khiển LED Trạng Thái & Relay Mở Cửa
- Slide 17: Biến Địa Chỉ 4: USER_FLASH_ADDR (0x0030_0000 - Sector 48) - Cơ Sở Dữ Liệu Thẻ Whitelist
- Slide 18: Biến Địa Chỉ 5: LOG_FLASH_ADDR (0x0031_0000 - Sector 49) - Nhật Ký Quẹt Thẻ Access Logs
- Slide 19: Biến Địa Chỉ 6: 0x0200_0000 & flashio_worker - Nạp Routine Vào SRAM Lập Trình Flash NVM
- Slide 20: Phần 4 - Testbench 1: Kiểm Thử Phần Cứng RTL Thuần Cho UART MMIO & FIFO (tb_uart_rtl.v)
- Slide 21: Phần 4 - Testbench 2: Kiểm Thử Tích Hợp Toàn Diện Top SoC Boot Flash & Ping (tb_uart_ping.v)"""

text = text.replace(doc_old, doc_new)

# 7. Update Slide 2 Agenda items to match the new flow
agenda_old = """    agenda_items = [
        ("Phần 1: Giới Thiệu Dự Án", "Hệ thống kiểm soát ra vào Offline bảo mật cao, lý do chọn bộ nhớ SPI Flash NVM lưu trữ dữ liệu."),
        ("Phần 2: Nền Tảng Phần Cứng & Phần Mềm", "Kit FPGA Basys 3, đầu đọc RDM6300, chuỗi công cụ Vivado, OpenLane 2 & RISC-V GCC."),
        ("Phần 3: Quy Trình Thiết Kế SoC (5 Giai Đoạn)", "Khối cơ sở -> Cầu bus Interconnect -> Đồng thiết kế Bootstrap -> Mở rộng FIFO -> MMIO C."),
        ("Phần 4: Testbench & Chi Tiết Biến Địa Chỉ MMIO", "Kiểm thử RTL thuần, Top SoC Ping và phân tích 6 biến địa chỉ phần cứng trong mã nguồn C."),
        ("Phần 5: Demo Thực Nghiệm Trên FPGA", "Danh sách thiết bị kết nối, giải pháp nguồn 5V & điện trở 1kΩ, cùng 4 kịch bản quẹt thẻ RFID thật."),
        ("Phần 6: Thiết Kế Vật Lý ASIC & Ký Duyệt", "Quy trình RTL-to-GDSII trên OpenLane 2 (Sky130): Layout GDSII, chỉ số PPA và ký duyệt Sign-off.")
    ]"""

agenda_new = """    agenda_items = [
        ("Phần 1: Giới Thiệu Dự Án", "Hệ thống kiểm soát ra vào Offline bảo mật cao, lý do chọn bộ nhớ SPI Flash NVM lưu trữ dữ liệu."),
        ("Phần 2: Nền Tảng Phần Cứng & Phần Mềm", "Kit FPGA Basys 3, đầu đọc RDM6300, chuỗi công cụ Vivado, OpenLane 2 & RISC-V GCC."),
        ("Phần 3: Kiến Trúc SoC & Vi Mạch UART", "Quy trình 5 giai đoạn thiết kế SoC, so sánh RTL vs C và sơ đồ khối 5 tầng vi mạch UART."),
        ("Phần 4: Firmware MMIO & Testbench Mô Phỏng", "Chi tiết 6 biến địa chỉ phần cứng trong C và 2 testbench kiểm thử toàn diện RTL & Top SoC."),
        ("Phần 5: Demo Thực Nghiệm Trên FPGA", "Mạch nguồn 5V & trở 1kΩ, phần mềm Host Console CLI 10 chức năng & kịch bản quẹt thẻ."),
        ("Phần 6: Thiết Kế Vật Lý ASIC & Ký Duyệt", "Quy trình RTL-to-GDSII trên OpenLane 2 (Sky130): Layout GDSII, chỉ số PPA và ký duyệt Sign-off.")
    ]"""

text = text.replace(agenda_old, agenda_new)

with open(target_file, "w", encoding="utf-8") as f:
    f.write(text)

print("Reordered slides successfully!")
