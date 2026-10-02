# Hệ Thống Testbench & Môi Trường Kiểm Thử SoC PicoRV32 RFID RDM6300

Tất cả các file phục vụ cho từng file testbench đã được quy hoạch gọn gàng và độc lập trong từng thư mục riêng biệt tương ứng với từng bước thiết kế trong đồ án.

---

## 1. Cấu Trúc Thư Mục Tổng Thể (`tb/`)

```
tb/
├── step2_firmware/               # Bước 2: Thiết kế firmware & giao thức truyền thông
│   ├── tb_firmware.c             # Harness C mô phỏng môi trường CPU & toàn bộ hàm firmware
│   ├── test_firmware.py          # Bộ kiểm thử tự động 21 test case cho firmware
│   ├── run_tb_firmware.bat       # Script chạy 1-click cho Bước 2
│   └── README.md                 # Tài liệu đặc tả Bước 2
│
├── step3_picorv32_sram/          # Bước 3: Nhân xử lý PicoRV32 & 1KB Data SRAM
│   ├── tb_data_sram.v            # Testbench Verilog kiểm tra chu kỳ bus SRAM & byte strobes
│   ├── test_picorv32_sram.py     # Bộ kiểm thử tự động 12 test case cho CPU & SRAM
│   ├── run_tb_step3.bat          # Script chạy 1-click cho Bước 3
│   ├── run_vivado_sim.bat        # Mô phỏng RTL trên Vivado Simulator (xsim)
│   └── README.md                 # Tài liệu đặc tả Bước 3
│
├── step4_spimemio_flash/         # Bước 4: Bộ điều khiển bộ nhớ ngoài SPI Flash (spimemio)
│   ├── tb_spi_flash.v            # Testbench Verilog mô phỏng SPI Flash Controller & mô hình Flash
│   ├── test_spimemio.py          # Bộ kiểm thử tự động 10 test case cho SPI Flash & XIP
│   ├── run_tb_step4.bat          # Script chạy 1-click cho Bước 4
│   └── README.md                 # Tài liệu đặc tả Bước 4
│
├── step5_rdm6300_pipeline/       # Bước 5: Đường ống 5 giai đoạn thu nhận & giải mã thẻ RFID
│   ├── tb_rdm6300_pipeline.v     # Testbench Verilog mô phỏng đường ống 5 giai đoạn (2FF->UART->FIFO->Decoder->XOR)
│   ├── test_rdm6300_pipeline.py  # Bộ kiểm thử tự động 12 test case cho đường ống RFID
│   ├── run_tb_step5.bat          # Script chạy 1-click cho Bước 5
│   ├── run_vivado_sim.bat        # Mô phỏng RTL trên Vivado Simulator (xsim)
│   └── README.md                 # Tài liệu đặc tả Bước 5
│
├── step6_top_soc_integration/    # Bước 6: Tích hợp toàn diện toàn hệ thống SoC
│   ├── tb_picorv32_rdm6300_flash.v # Testbench Verilog tích hợp toàn hệ thống SoC + Flash + RFID + UART
│   ├── tb_uart_ping.v            # Testbench Verilog kiểm tra UART ping
│   ├── firmware.hex              # Mã máy Verilog HEX nạp vào hệ thống mô phỏng
│   ├── test_top_soc.py           # Bộ kiểm thử tự động 8 test case cho luồng phần cứng + phần mềm
│   ├── run_tb_step6.bat          # Script chạy 1-click cho Bước 6 bằng Python
│   ├── run_vivado_sim.bat        # Mô phỏng RTL toàn bộ 14 module trên Vivado Simulator (xsim)
│   └── README.md                 # Tài liệu đặc tả Bước 6
│
├── firmware.hex                  # File HEX gốc được sinh tự động khi build firmware
├── run_all_testbenches.py        # Master Python runner chạy toàn bộ 5 bước (63 test cases)
├── run_all_testbenches.bat       # Master batch script 1-click chạy toàn bộ test suite
└── README.md                     # Tài liệu hướng dẫn này
```

---

## 2. Bảng Thống Kê Số Lượng Test Cases

| Thư Mục | Bước Thiết Kế | Số Test Cases | Tỷ Lệ Đạt (Pass Rate) | Trạng Thái |
| :--- | :--- | :---: | :---: | :---: |
| `step2_firmware/` | Bước 2: Thiết kế firmware & giao thức | 21 | 100.0% | **PASS** |
| `step3_picorv32_sram/` | Bước 3: Nhân PicoRV32 & 1KB SRAM | 12 | 100.0% | **PASS** |
| `step4_spimemio_flash/` | Bước 4: Bộ điều khiển SPI Flash (`spimemio`) | 10 | 100.0% | **PASS** |
| `step5_rdm6300_pipeline/`| Bước 5: Đường ống thu nhận RFID 5 giai đoạn | 12 | 100.0% | **PASS** |
| `step6_top_soc_integration/` | Bước 6: Tích hợp toàn hệ thống SoC | 8 | 100.0% | **PASS** |
| **TỔNG CỘNG** | **Toàn bộ hệ sinh thái vi mạch SoC** | **63** | **100.0%** | **CERTIFIED** |

---

## 3. Hướng Dẫn Thực Thi

### Chạy toàn bộ 63 Test Cases cùng lúc:
Chạy file script trong thư mục `tb/`:
```cmd
run_all_testbenches.bat
```
Hoặc:
```cmd
py run_all_testbenches.py
```

### Chạy riêng từng bước:
Người dùng chỉ cần di chuyển vào thư mục tương ứng và chạy file `.bat` hoặc `.py`:
- **Bước 2**: `cd step2_firmware && run_tb_firmware.bat`
- **Bước 3**: `cd step3_picorv32_sram && run_tb_step3.bat`
- **Bước 4**: `cd step4_spimemio_flash && run_tb_step4.bat`
- **Bước 5**: `cd step5_rdm6300_pipeline && run_tb_step5.bat`
- **Bước 6**: `cd step6_top_soc_integration && run_tb_step6.bat`
