# -*- coding: utf-8 -*-
import re

with open('create_presentation.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix addr2_points
text = text.replace(
    '("2. Cách thao tác trong C:", "• Ghi dữ liệu phát (TX): Gán REG_PC_UART_DAT = c. Phần cứng tự động nạp ký tự vào TX FIFO 32 bytes và phát ra chân tx_o.\n• Đọc dữ liệu nhận (RX): Đọc REG_PC_UART_DAT. Nhận lệnh điều khiển từ Host Console PC mà không bị khóa chương trình.")',
    '("2. Cách thao tác trong C:", "• Ghi dữ liệu phát (TX): Gán REG_PC_UART_DAT = c. Phần cứng tự động nạp ký tự vào TX FIFO 32 bytes và phát ra chân tx_o.\\n• Đọc dữ liệu nhận (RX): Đọc REG_PC_UART_DAT. Nhận lệnh điều khiển từ Host Console PC mà không bị khóa chương trình.")'
)

# Fix addr3_points
text = text.replace(
    '("2. Phép toán Bitmask chuẩn mực:", "• Bit 0 (0x0001): LED nhịp tim (Heartbeat 1 Hz), đảo trạng thái bằng phép ^= 0x0001.\n• Bit 1 (0x0002): LED đỏ cảnh báo từ chối quẹt thẻ (Access Denied).\n• Bit 2 (0x0004): LED xanh mở cửa & kích hoạt Relay chốt điện từ (Access Granted).\n• Bit 3 (0x0008): LED vàng cảnh báo chip Flash đang bận xóa/ghi sector.")',
    '("2. Phép toán Bitmask chuẩn mực:", "• Bit 0 (0x0001): LED nhịp tim (Heartbeat 1 Hz), đảo trạng thái bằng phép ^= 0x0001.\\n• Bit 1 (0x0002): LED đỏ cảnh báo từ chối quẹt thẻ (Access Denied).\\n• Bit 2 (0x0004): LED xanh mở cửa & kích hoạt Relay chốt điện từ (Access Granted).\\n• Bit 3 (0x0008): LED vàng cảnh báo chip Flash đang bận xóa/ghi sector.")'
)

# Fix addr4_points
text = text.replace(
    '("2. Cấu trúc bản ghi 16 Bytes (Slot Record):", "• Offset +0 (4B): Magic Number 0x52464944 (\'RFID\') xác nhận slot hợp lệ.\n• Offset +4 (4B): UID Word High (tag_hi).\n• Offset +8 (4B): UID Word Low (tag_lo).\n• Offset +12 (4B): Checksum toàn vẹn (tag_hi ^ tag_lo).")',
    '("2. Cấu trúc bản ghi 16 Bytes (Slot Record):", "• Offset +0 (4B): Magic Number 0x52464944 (\'RFID\') xác nhận slot hợp lệ.\\n• Offset +4 (4B): UID Word High (tag_hi).\\n• Offset +8 (4B): UID Word Low (tag_lo).\\n• Offset +12 (4B): Checksum toàn vẹn (tag_hi ^ tag_lo).")'
)

text = text.replace(
    '("3. Cách thao tác trong C:", "• Tra cứu tức thì qua cơ chế XIP: CPU đọc thẳng vùng nhớ 0x300000 qua con trỏ con trỏ bộ nhớ mà không cần tải vào RAM.\n• Thuật toán Early Termination: Khi gặp slot có Magic == 0xFFFFFFFF (vùng Flash trắng chưa ghi), vòng lặp dừng ngay lập tức.")',
    '("3. Cách thao tác trong C:", "• Tra cứu tức thì qua cơ chế XIP: CPU đọc thẳng vùng nhớ 0x300000 qua con trỏ con trỏ bộ nhớ mà không cần tải vào RAM.\\n• Thuật toán Early Termination: Khi gặp slot có Magic == 0xFFFFFFFF (vùng Flash trắng chưa ghi), vòng lặp dừng ngay lập tức.")'
)

# Fix addr5_points
text = text.replace(
    '("2. Cấu trúc bản ghi sự kiện 16 Bytes:", "• Offset +0 (4B): Trạng thái mở cửa: 0x53554343 (\'SUCC\') hoặc 0x4641494C (\'FAIL\').\n• Offset +4 (4B): UID High của thẻ quẹt.\n• Offset +8 (4B): UID Low của thẻ quẹt.\n• Offset +12 (4B): Số thứ tự sự kiện (Sequence Number 1, 2, 3...).")',
    '("2. Cấu trúc bản ghi sự kiện 16 Bytes:", "• Offset +0 (4B): Trạng thái mở cửa: 0x53554343 (\'SUCC\') hoặc 0x4641494C (\'FAIL\').\\n• Offset +4 (4B): UID High của thẻ quẹt.\\n• Offset +8 (4B): UID Low của thẻ quẹt.\\n• Offset +12 (4B): Số thứ tự sự kiện (Sequence Number 1, 2, 3...).")'
)

with open('create_presentation.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Strings fixed successfully!")
