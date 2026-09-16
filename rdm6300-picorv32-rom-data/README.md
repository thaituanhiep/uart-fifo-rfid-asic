# RDM6300 RFID - PicoRV32 RISC-V SoC with SPI Flash Data Storage

## 1. Tổng quan Kiến trúc (System Architecture)
Dự án được thiết kế theo cấu trúc tối giản, từng bước (step-by-step), sử dụng lõi xử lý RISC-V **PicoRV32** làm trung tâm điều khiển:
- **Lõi CPU**: [picorv32.v](file:///d:/VirtualSharedFolders/uart-fifo-rfid-asic/rdm6300-picorv32-rom-data/rtl/picorv32.v) (RV32I, 32-bit).
- **Bộ nhớ On-Chip**: [boot_rom.v](file:///d:/VirtualSharedFolders/uart-fifo-rfid-asic/rdm6300-picorv32-rom-data/rtl/boot_rom.v) (8 KBytes SRAM / Boot ROM).
- **Bộ điều khiển Flash SPI**: [spi_flash_controller.v](file:///d:/VirtualSharedFolders/uart-fifo-rfid-asic/rdm6300-picorv32-rom-data/rtl/spi_flash_controller.v) (Giao tiếp Spansion S25FL032P / W25Qxx trên Basys 3 để lưu và đọc dữ liệu thẻ RFID).
- **Giao tiếp PC**: [simpleuart.v](file:///d:/VirtualSharedFolders/uart-fifo-rfid-asic/rdm6300-picorv32-rom-data/rtl/simpleuart.v) (Host PC UART TX/RX qua USB-UART Basys 3).
- **Giao tiếp RFID RDM6300**: [simpleuart.v](file:///d:/VirtualSharedFolders/uart-fifo-rfid-asic/rdm6300-picorv32-rom-data/rtl/simpleuart.v) (Kênh RX nhận chuỗi ký tự thẻ 9600 baud từ chân PMOD JA1).
- **Phần mềm máy tính (Host PC)**: Viết bằng ngôn ngữ C ([host/main.c](file:///d:/VirtualSharedFolders/uart-fifo-rfid-asic/rdm6300-picorv32-rom-data/host/main.c)) tương tác qua cổng COM.

---

## 2. Bản đồ Bộ nhớ MMIO (Memory Map)
| Dải địa chỉ | Ngoại vi / Chức năng | Mô tả chi tiết |
| :--- | :--- | :--- |
| `0x0000_0000 - 0x0000_1FFF` | **8KB SRAM / Boot ROM** | Nơi chứa mã lệnh thực thi và ngăn xếp (Stack) của PicoRV32. |
| `0x1000_0000` | **RDM6300 UART Baud Divisor** | Thanh ghi chia tần baud rate (mặc định 100MHz / 9600 = 10416). |
| `0x1000_0004` | **RDM6300 UART Data RX** | Đọc 1 byte nhận từ RDM6300 (trả về `-1` nếu chưa có dữ liệu). |
| `0x2000_0000` | **SPI Flash Control** | Bit 0: Trigger lệnh, Bit [3:1]: Opcode (0: Read, 1: Write, 2: Sector Erase). |
| `0x2000_0004` | **SPI Flash Status** | Bit 0: Busy, Bit 1: Write Done, Bit 2: Error. |
| `0x2000_0008` | **SPI Flash Address** | Địa chỉ Flash 24-bit (offset an toàn: `0x30_0000` = 3MB). |
| `0x2000_000C` | **SPI Flash Write Data** | 32-bit dữ liệu cần ghi vào Flash (Page Program). |
| `0x2000_0010` | **SPI Flash Read Data** | 32-bit dữ liệu đọc ra từ Flash. |
| `0x3000_0000` | **Host PC UART Baud Divisor** | Thanh ghi chia tần UART giao tiếp máy tính (9600 baud). |
| `0x3000_0004` | **Host PC UART Data TX/RX** | Ghi byte để gửi lên máy tính; đọc byte máy tính gửi xuống. |
| `0x4000_0000` | **GPIO / Status LEDs** | Điều khiển 16 LED trạng thái trên bo mạch Basys 3. |

---

## 3. Cấu trúc Thư mục Clean
```text
rdm6300-picorv32-rom-data/
├── config.json                             # OpenLane ASIC Flow config
├── pin_order.cfg                           # Floorplan pin assignment
├── rtl/
│   ├── picorv32.v                          # Nhân vi xử lý RISC-V 32-bit
│   ├── boot_rom.v                          # 8KB SRAM / ROM nhúng
│   ├── spi_flash_controller.v              # Điều khiển Flash Basys 3
│   ├── simpleuart.v                        # UART thu/phát gọn nhẹ
│   ├── sync_2ff.v                          # Chống metastability 2-FF
│   └── rdm6300_picorv32_soc.v              # Top-level SoC tích hợp
├── fpga/
│   ├── rtl/top_basys3_picorv32_rdm6300.v   # Top FPGA Basys 3 (STARTUPE2 CCLK)
│   └── constraints/basys3_picorv32_rdm6300.xdc # Map chân Basys 3
├── firmware/
│   ├── main.c                              # Firmware C chạy trên PicoRV32
│   ├── start.s                             # Khởi tạo Stack & BSS
│   ├── sections.lds                        # Linker script 8KB SRAM
│   └── Makefile                            # Build firmware ra .hex
├── host/
│   ├── main.c                              # Mã nguồn C trên PC (Win32 Serial)
│   ├── main.py                             # Giao diện Python CLI chạy ngay
│   └── build.bat                           # Script biên dịch C trên Windows
└── tb/
    └── tb_picorv32_rdm6300_flash.v         # Testbench Icarus Verilog
```

---

## 4. Hướng dẫn Chạy Thử nghiệm

### A. Chạy Phần mềm C trên Máy tính
1. Biên dịch file [host/main.c](file:///d:/VirtualSharedFolders/uart-fifo-rfid-asic/rdm6300-picorv32-rom-data/host/main.c):
   ```cmd
   cd rdm6300-picorv32-rom-data\host
   build.bat
   ```
   Hoặc chạy file thực thi Python CLI có sẵn:
   ```cmd
   python main.py
   ```
2. Giao diện menu điều khiển trên máy tính:
   - **Phím 1**: Kiểm tra kết nối với PicoRV32 (Ping -> Pong).
   - **Phím 2**: Đọc mã thẻ RFID vừa quet từ đầu đọc RDM6300.
   - **Phím 3**: Ghi và lưu mã thẻ RFID vào chip Flash Basys 3.
   - **Phím 4**: Đọc lại mã thẻ RFID đã lưu từ Flash ra màn hình máy tính.
   - **Phím 5**: Xóa sector Flash (`0x30_0000`).

### B. Chạy trên FPGA Basys 3 (Vivado)
- Thêm các file trong `rtl/` và `fpga/rtl/top_basys3_picorv32_rdm6300.v` vào project Vivado.
- Thêm file constraints `fpga/constraints/basys3_picorv32_rdm6300.xdc`.
- Generate Bitstream và nạp vào Basys 3 qua Vivado Hardware Manager.
