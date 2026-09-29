# Bước 3: Testbench Nhân CPU RISC-V PicoRV32 & 1KB Data SRAM

Thư mục này chứa toàn bộ các file phục vụ kiểm thử **Bước 3: Thiết kế hệ thống xử lý phần cứng: nhân CPU PicoRV32 và 1KB Data SRAM** (`rtl/picorv32.v` + `rtl/data_sram.v`).

## 1. Danh Sách File Trong Thư Mục
- `tb_data_sram.v`: Testbench Verilog kiểm thử chu kỳ xung nhịp, giao thức bắt tay `valid`/`ready`, byte strobes `wstrb`, và biên địa chỉ 1KB SRAM.
- `test_picorv32_sram.py`: Testbench tự động hóa bằng Python kiểm thử toàn diện 12 kịch bản giao tiếp bus PicoRV32 Memory Interface, hoạt động ngăn xếp Stack (Push/Pop), các lệnh tải/lưu `sw`, `sh`, `sb`, `lw`, `lh`, `lb`, và kiểm tra trạng thái an toàn `cpu_trap == 0`.
- `run_tb_step3.bat`: Script chạy testbench 1 click.
- `README.md`: Tài liệu đặc tả và hướng dẫn chi tiết.

## 2. Hướng Dẫn Thực Thi
Chạy testbench tự động:
```powershell
cd tb\step3_picorv32_sram
py test_picorv32_sram.py
```
Hoặc:
```cmd
run_tb_step3.bat
```

## 3. Danh Mục 12 Test Case Đã Được Kiểm Thử Đạt 100%
| Test Case | Tên Kiểm Thử | Mục Đích & Kỳ Vọng | Kết Quả |
| :--- | :--- | :--- | :---: |
| **TC01** | Power-on Reset & Init | Khởi tạo mảng bộ nhớ 256 từ (1KB) về 0, `ready = 0` | **PASS** |
| **TC02** | Store & Load Word (`sw`/`lw`) | Ghi và đọc lại từ 32-bit `0xDEADBEEF` tại địa chỉ `0x000` | **PASS** |
| **TC03** | Byte Write Strobe (`sb`) | Ghi đè Byte 0 (`wstrb=0001`) và Byte 2 (`wstrb=0100`) không làm hỏng byte lân cận | **PASS** |
| **TC04** | Byte Load Signed/Unsigned | `lb` mở rộng dấu (-2), `lbu` mở rộng 0 (254) | **PASS** |
| **TC05** | Halfword Access (`sh`/`lh`/`lhu`) | Ghi và đọc nửa từ 16-bit tại nửa thấp và nửa cao | **PASS** |
| **TC06** | Top Boundary Word 255 | Ghi và đọc tại ô nhớ cao nhất `0x3FC` (1020 byte) | **PASS** |
| **TC07** | Address Space Isolation | Không gian 10-bit địa chỉ cách ly chuẩn xác 256 từ nhớ | **PASS** |
| **TC08** | RISC-V Stack Push/Pop | Mô phỏng con trỏ `sp = 0x3F0` đẩy và kéo thanh ghi `ra`, `s0`, `s1` bảo toàn dữ liệu | **PASS** |
| **TC09** | Ready Assertion Latency | Tín hiệu `ready` tích cực chính xác sau 1 chu kỳ clock sau khi có `valid` | **PASS** |
| **TC10** | Ready Deassertion Timing | Tín hiệu `ready` hạ ngay lập tức khi `valid` về 0 | **PASS** |
| **TC11** | Sequential Burst Access | Truyền chuỗi liên tiếp 8 từ nhớ không xung đột bus | **PASS** |
| **TC12** | CPU Trap Immunity Check | Xác nhận tín hiệu `cpu_trap == 0`, hệ thống vận hành an toàn | **PASS** |
