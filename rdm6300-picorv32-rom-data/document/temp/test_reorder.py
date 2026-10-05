# -*- coding: utf-8 -*-
"""
Script: move_testbenches_before_demo.py
Di chuyển 2 slide testbench (tb_uart_rtl.v, tb_uart_ping.v) xuống ngay trước Phần 5 Demo.
Thứ tự mới:
- Slide 14..19: 6 Biến địa chỉ phần cứng MMIO trong C
- Slide 20: Testbench 1 (tb_uart_rtl.v)
- Slide 21: Testbench 2 (tb_uart_ping.v)
- Slide 22: Demo FPGA Hardware Setup (Device.jpg & Nguồn 5V / 1k)
- Slide 23: Demo Host Console CLI & Kịch bản quẹt thẻ
- Slide 24: ASIC OpenLane 2 config.json
- Slide 25: ASIC Layout & Sign-off
- Slide 26: Tổng kết đề tài
"""
import os
import re

cur_dir = os.path.dirname(os.path.abspath(__file__))
target_file = os.path.join(cur_dir, "create_presentation.py")

with open(target_file, "r", encoding="utf-8") as f:
    text = f.read()

# Let's extract the Testbench block and Address Variables block
# Find Testbench block: from `# SLIDE 14: PHẦN 4 - HỆ THỐNG TESTBENCH: UART RTL` to before `# SLIDE 16: BIẾN ĐỊA CHỈ 1`
tb_pattern = r'(    # =========================================================================\s+# SLIDE 14: PHẦN 4 - HỆ THỐNG TESTBENCH: UART RTL.*?(?=    # =========================================================================\s+# SLIDE 16: BIẾN ĐỊA CHỈ 1))'
tb_match = re.search(tb_pattern, text, re.DOTALL)
if not tb_match:
    print("Error: Could not find tb_pattern!")
    # Let's inspect what slide numbers testbench and addr vars currently have
else:
    print("Found tb_pattern successfully!")

