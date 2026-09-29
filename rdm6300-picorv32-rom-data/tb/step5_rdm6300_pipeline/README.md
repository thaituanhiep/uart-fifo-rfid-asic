# Bước 5: Testbench Đường Ống 5 Giai Đoạn Thu Nhận & Giải Mã Thẻ RFID RDM6300 Tự Trị

Thư mục này chứa toàn bộ các file phục vụ kiểm thử **Bước 5: Thiết kế ngoại vi thu nhận & giải mã thẻ RFID RDM6300 tự trị** (`rtl/sync_2ff.v` + `rtl/uart_rx.v` + `rtl/rdm6300_frame_decoder.v`).

## 1. Danh Sách File Trong Thư Mục
- `tb_rdm6300_pipeline.v`: Testbench Verilog mô phỏng toàn bộ 5 giai đoạn đường ống (2-FF -> UART RX -> FIFO -> Frame Decoder -> Checksum XOR) với tín hiệu xung nhịp 50MHz và luồng bit RFID 9600 baud.
- `test_rdm6300_pipeline.py`: Testbench tự động hóa bằng Python kiểm thử toàn diện 12 kịch bản qua 5 giai đoạn đường ống: 2 tầng D-FF đồng bộ xung CDC khử bất định, bộ bỏ phiếu đa số 3 điểm (Tick 7, 8, 9) lọc nhiễu gai xung, bộ chia tần 5208, FSM giải mã 5 bước, bộ chuyển đổi tổ hợp ASCII sang Hex trong 0 chu kỳ trễ, cây toán tử XOR song song 1 chu kỳ clock (20ns), bộ định thời Watchdog 10ms tự động giải cứu FSM, và cơ chế ngắt phần cứng Zero-CPU Overhead.
- `run_tb_step5.bat`: Script chạy testbench 1 click.
- `README.md`: Tài liệu đặc tả và hướng dẫn chi tiết.

## 2. Hướng Dẫn Thực Thi
Chạy testbench tự động:
```powershell
cd tb\step5_rdm6300_pipeline
py test_rdm6300_pipeline.py
```
Hoặc:
```cmd
run_tb_step5.bat
```

## 3. Danh Mục 12 Test Case Đã Được Kiểm Thử Đạt 100%
| Test Case | Tên Kiểm Thử | Mục Đích & Kỳ Vọng | Kết Quả |
| :--- | :--- | :--- | :---: |
| **TC01** | 2-FF CDC Synchronizer | Khử bất định (Metastability Tsu/Th violation), MTBF > 1000 năm | **PASS** |
| **TC02** | 3-Point Majority Voter | Lấy mẫu tại Tick 7, 8, 9 lọc sạch gai nhiễu cao tần trên đường truyền | **PASS** |
| **TC03** | Baud Rate Divisor | Tần số 50 MHz chia cho 9600 bps = đúng 5208 chu kỳ/bit (104.16 µs) | **PASS** |
| **TC04** | Combinational ASCII-to-Hex | Chuyển đổi tổ hợp ký tự ASCII sang 4-bit Hex trong 0 chu kỳ trễ | **PASS** |
| **TC05** | FSM STX Transition | Bỏ qua nhiễu đường truyền, chuyển sang `COLLECT_DATA` khi gặp STX (`0x02`) | **PASS** |
| **TC06** | Full Valid Frame Decode | Giải mã thẻ thật `00007293F0`, Checksum `0x11`, kích hoạt `card_valid_strobe` | **PASS** |
| **TC07** | Master Card Decode | Giải mã thẻ Master `010054DA65`, Checksum `0xEA`, khớp chuẩn 100% | **PASS** |
| **TC08** | Checksum Error Rejection | Phát hiện sai lệch Checksum, từ chối thẻ hỏng, bật cờ `cs_error=1` | **PASS** |
| **TC09** | Invalid ETX Rejection | Bắt buộc ký tự kết thúc là ETX (`0x03`), nếu sai tự động reset FSM | **PASS** |
| **TC10** | 1-Cycle Parallel XOR Proof | Chứng minh tính toàn vẹn Checksum song song trong 1 chu kỳ (20.0 ns) | **PASS** |
| **TC11** | Watchdog 10ms Auto-Reset | Tự động khôi phục FSM về `WAIT_STX` khi khung truyền bị gián đoạn giữa chừng | **PASS** |
| **TC12** | Zero-CPU Overhead Verification | Toàn bộ 14 byte xử lý bằng phần cứng, CPU hoàn toàn không tốn chu kỳ thăm dò | **PASS** |
