# Bước 2: Testbench Kiểm Thử Firmware & Giao Thức (Software-First)

Thư mục này chứa toàn bộ các file phục vụ kiểm thử **Bước 2: Thiết kế firmware và định nghĩa giao thức giao tiếp trước** cho SoC PicoRV32 RFID.

## 1. Danh Sách File Trong Thư Mục
- `test_firmware.py`: Bộ kiểm thử tự động viết bằng Python, chạy trực tiếp trên Windows/Linux mà không bị chặn bởi chính sách hệ thống (Device Guard), thực hiện 21 kịch bản kiểm thử độc lập.
- `tb_firmware.c`: Bộ testbench C chi tiết mô phỏng chính xác các thanh ghi MMIO (`REG_RFID_STATUS`, `REG_RFID_TAG_HI`, `REG_RFID_TAG_LO`, `REG_PC_UART_DIV`, `REG_PC_UART_DAT`, `REG_GPIO_LEDS`), mảng bộ nhớ NOR Flash 16MB và hàng đợi UART FIFO.
- `run_tb_firmware.bat`: Script tự động hóa chạy testbench bằng 1 click.
- `README.md`: Tài liệu hướng dẫn và đặc tả 21 test case.

## 2. Hướng Dẫn Chạy Testbench
Chạy bằng Python (khuyến nghị trên mọi môi trường):
```powershell
cd tb\step2_firmware
py test_firmware.py
```
Hoặc chạy file batch:
```cmd
run_tb_firmware.bat
```

## 3. Danh Mục 21 Test Case Đã Được Kiểm Thử Đạt 100%
| Test Case | Tên Kiểm Thử | Mục Đích & Kỳ Vọng | Kết Quả |
| :--- | :--- | :--- | :---: |
| **TC01** | Utility `hex2val()` | Chuyển đổi ASCII Hex sang giá trị 0..15, bắt lỗi ký tự sai | **PASS** |
| **TC02** | UART Numerical Formatting | Định dạng xuất 32-bit Hex và Decimal không dùng bộ chia phần cứng | **PASS** |
| **TC03** | Command `P` (Ping) | Gửi `P\n`, nhận phản hồi `PONG: PicoRV32 Active` | **PASS** |
| **TC04** | Command `R` (Query Empty) | Truy vấn khi chưa có thẻ, nhận `ERR:NO_TAG` | **PASS** |
| **TC05** | Command `E` (Erase Tags) | Xóa trắng Sector 48 Flash (`0x300000`), trả về `OK:SECTOR_ERASED` | **PASS** |
| **TC06** | Master Card Protection | Thẻ Master `010054DA65` được định danh là Slot 0 (`INFO:EXISTS:SLOT:0`) | **PASS** |
| **TC07** | Command `N` (Register Tag) | Đăng ký thẻ `00007293F0`, lưu 16-byte record vào Slot 0 | **PASS** |
| **TC08** | Anti-Duplicate Protection | Đăng ký lại thẻ `00007293F0`, trả về `INFO:EXISTS:SLOT:0`, chống hao mòn Flash | **PASS** |
| **TC09** | Multi-Tag Allocation | Cấp phát tuần tự Slot 1 (`000073161D`) và Slot 2 (`0000A1B2C3`) | **PASS** |
| **TC10** | Command `C` (Check Tag) | Tra cứu thẻ trong Flash, thẻ Master và thẻ chưa đăng ký | **PASS** |
| **TC11** | Command `F` (List All Tags) | Đọc danh mục toàn bộ 3 thẻ đã lưu trong Flash Sector 48 | **PASS** |
| **TC12** | Virtual Scan `V` (Authorized) | Quẹt thẻ hợp lệ: `ACCESS:GRANTED`, bật LED Xanh, ghi log `SUCC` | **PASS** |
| **TC13** | Virtual Scan `V` (Denied) | Quẹt thẻ lạ: `ACCESS:DENIED`, bật LED Đỏ cảnh báo, ghi log `FAIL` | **PASS** |
| **TC14** | Command `L` (Read Logs) | Đọc lịch sử ra vào Sector 49, phân loại 1 `SUCC` và 1 `FAIL` | **PASS** |
| **TC15** | Command `K` (Kill Tag) | Xóa mềm thẻ khỏi Slot 0 bằng cách ghi 0x0, không ảnh hưởng các slot khác | **PASS** |
| **TC16** | Command `X` (Erase Logs) | Xóa trắng Sector 49 (`0x310000`), đọc lại trả về `ERR:EMPTY_LOGS` | **PASS** |
| **TC17** | Command `S` (Hardware Status) | Đọc Flash ID (`0x00010215`), Status Register, GPIO LEDs | **PASS** |
| **TC18** | Command `?` (Help) | Xuất bảng menu trợ giúp tập lệnh Host PC | **PASS** |
| **TC19** | Error Handling | Xử lý lỗi chuỗi thẻ ngắn hơn 10 ký tự: `ERR:INVALID_LENGTH` | **PASS** |
| **TC20** | Hardware MMIO Handshake | Bắt ngắt `poll_rdm6300()`, xóa cờ `card_valid`, kích hoạt debounce 250k chu kỳ | **PASS** |
| **TC21** | Command `D` (Raw Dump) | Đọc dump thô 8 từ nhớ 32-bit từ địa chỉ `0x300000` | **PASS** |
