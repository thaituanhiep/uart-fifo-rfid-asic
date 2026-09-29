# Step 6: Full PicoRV32 RFID SoC Integration Testbench

Thư mục này chứa toàn bộ các file phục vụ cho quá trình kiểm tra tích hợp toàn hệ thống SoC (**Bước 6: Tích Hợp Toàn Diện Toàn Hệ Thống SoC**):

## 1. Danh sách các file trong thư mục

- `tb_picorv32_rdm6300_flash.v`: Testbench Verilog mô phỏng toàn bộ chip SoC hoàn chỉnh kết nối với mô hình bộ nhớ SPI Flash Winbond W25Q128, module truyền thẻ RFID RDM6300, và bộ thu phát UART PC.
- `tb_uart_ping.v`: Testbench Verilog kiểm tra nhanh giao tiếp UART ping-pong giữa PicoRV32 SoC và máy tính chủ.
- `firmware.hex`: File định dạng Verilog HEX chứa mã máy thực thi (firmware C) của CPU PicoRV32, được nạp vào SPI Flash / ROM khi khởi động.
- `test_top_soc.py`: Bộ kiểm thử tự động hóa toàn diện 8 Test Cases cho luồng tích hợp phần cứng và phần mềm.
- `run_tb_step6.bat`: Kịch bản thực thi nhanh 1-click cho Bước 6.
- `README.md`: Tài liệu hướng dẫn chi tiết của thư mục này.

---

## 2. Danh mục 8 Test Cases trong Step 6

| Mã TC | Tên Test Case | Mục Tiêu Kiểm Tra | Kết Quả |
| :--- | :--- | :--- | :---: |
| **TC01** | Full SoC Power-On Reset | CPU PicoRV32 khởi động, nạp firmware từ Flash, khởi tạo 1KB SRAM, LED trạng thái = 0x0001 | **PASS** |
| **TC02** | Non-Volatile Flash Database Setup | Nạp cơ sở dữ liệu thẻ hợp lệ vào Flash Sector 48 (Tag `00007293F0`) | **PASS** |
| **TC03** | Autonomous Hardware Reception & XOR Verification | RDM6300 5-stage pipeline tự nhận thẻ, tính XOR và kích hoạt `card_event_o` | **PASS** |
| **TC04** | End-to-End Access Granted Flow | CPU đọc thẻ từ FIFO, tra cứu Flash thành công -> bật LED Xanh, phát UART `"ACCESS:GRANTED"` | **PASS** |
| **TC05** | End-to-End Access Denied Flow | Thẻ lạ quét vào -> CPU tra cứu không có -> nháy LED Đỏ cảnh báo, phát UART `"ACCESS:DENIED"` | **PASS** |
| **TC06** | Master Card Instant Authentication | Thẻ Master `010054DA65` được chứng thực ngay tại Slot 0 trong RAM | **PASS** |
| **TC07** | Sector 49 Access Logs Verification | Kiểm tra nhật ký quẹt thẻ lưu vào Flash Sector 49 (`SUCC` -> `FAIL` -> `SUCC`) | **PASS** |
| **TC08** | System Robustness & Zero-Trap | Xác nhận thanh ghi `cpu_trap == 0` sau toàn bộ các kịch bản kiểm tra | **PASS** |

---

## 3. Cách chạy kiểm tra

### Cách 1: Chạy bằng file Batch (Windows)
```cmd
run_tb_step6.bat
```

### Cách 2: Chạy trực tiếp bằng Python
```cmd
py test_top_soc.py
```
