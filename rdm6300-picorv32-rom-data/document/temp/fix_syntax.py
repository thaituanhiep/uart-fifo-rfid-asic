# -*- coding: utf-8 -*-
import re

with open('create_presentation.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix addr1_points multiline string
text = text.replace(
    '("2. Cách thao tác trong C:", "• Cấu hình baudrate: Ghi giá trị 5208 (50,000,000 / 9600) vào REG_RFID_UART_DIV một lần duy nhất lúc khởi động.\n• Đọc không khóa (Non-blocking): Đọc REG_RFID_UART_DAT. Nếu d != 0xFFFFFFFF, ép kiểu lấy byte dữ liệu (d & 0xFF) đưa vào máy trạng thái parser.")',
    '("2. Cách thao tác trong C:", "• Cấu hình baudrate: Ghi giá trị 5208 (50,000,000 / 9600) vào REG_RFID_UART_DIV một lần duy nhất lúc khởi động.\\n• Đọc không khóa (Non-blocking): Đọc REG_RFID_UART_DAT. Nếu d != 0xFFFFFFFF, ép kiểu lấy byte dữ liệu (d & 0xFF) đưa vào máy trạng thái parser.")'
)

with open('create_presentation.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Checked and fixed create_presentation.py!")
