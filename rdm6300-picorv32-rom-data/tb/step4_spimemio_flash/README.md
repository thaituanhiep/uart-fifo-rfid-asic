# Bước 4: Testbench Bộ Điều Khiển Bộ Nhớ Ngoài SPI Flash Controller (`spimemio.v`)

Thư mục này chứa toàn bộ các file phục vụ kiểm thử **Bước 4: Thiết kế bộ điều khiển bộ nhớ ngoài SPI Flash Controller** (`rtl/spimemio.v`).

## 1. Danh Sách File Trong Thư Mục
- `tb_spi_flash.v`: Testbench Verilog mô phỏng bộ điều khiển SPI Flash Controller giao tiếp với mô hình bộ nhớ Flash SPI qua các đường tín hiệu CS_N, SCK, MOSI, MISO.
- `test_spimemio.py`: Testbench tự động hóa bằng Python kiểm thử toàn diện 10 kịch bản truyền thông chuẩn SPI, các lệnh Flash 0x03/0x0B (Đọc XIP), 0x06 (WREN), 0x02 (Page Program), 0xD8 (Sector Erase), 0x05 (Đọc trạng thái & Polling cờ WIP), 0x9F (Đọc JEDEC ID), và tính bền vững lưu trữ không bay hơi (>20 năm).
- `run_tb_step4.bat`: Script chạy testbench 1 click.
- `README.md`: Tài liệu đặc tả và hướng dẫn chi tiết.

## 2. Hướng Dẫn Thực Thi
Chạy testbench tự động:
```powershell
cd tb\step4_spimemio_flash
py test_spimemio.py
```
Hoặc:
```cmd
run_tb_step4.bat
```

## 3. Danh Mục 10 Test Case Đã Được Kiểm Thử Đạt 100%
| Test Case | Tên Kiểm Thử | Mục Đích & Kỳ Vọng | Kết Quả |
| :--- | :--- | :--- | :---: |
| **TC01** | Read JEDEC ID (`0x9F`) | Đọc mã nhận dạng chip Spansion/Winbond 32Mb (`0x010216`) | **PASS** |
| **TC02** | Read Status Register (`0x05`) | Kiểm tra trạng thái rảnh rỗi ban đầu: `WIP=0`, `WEL=0` | **PASS** |
| **TC03** | Write Enable Latch (`0x06`) | Gửi lệnh WREN bật bit cờ `WEL=1` cho phép ghi/xóa | **PASS** |
| **TC04** | Sector Erase 64KB (`0xD8`) | Xóa khối 64KB Sector 48 (`0x300000`), xác nhận cờ `WIP=1` | **PASS** |
| **TC05** | Automatic WIP Polling | Vòng lặp polling phần cứng/firmware chờ Flash hoàn tất và trả về rảnh | **PASS** |
| **TC06** | Page Program (`0x02`) | Ghi bản ghi thẻ RFID 16-byte vào Flash Sector 48 | **PASS** |
| **TC07** | XIP Direct Memory Read | Đọc trực tiếp từ bus CPU 32-bit qua cầu nối ánh xạ bộ nhớ `spimemio` | **PASS** |
| **TC08** | SPI Clock & CS_N Pin State | Giám sát xung nhịp SCK và chân chọn chip CS_N hạ mức 0 khi truyền | **PASS** |
| **TC09** | Write Protection Check | Khóa an toàn: từ chối ghi/xóa khi chưa kích hoạt WREN (`WEL=0`) | **PASS** |
| **TC10** | Non-Volatile Persistence | Mô phỏng ngắt nguồn/reset SoC: dữ liệu danh bạ thẻ vẫn nguyên vẹn | **PASS** |
