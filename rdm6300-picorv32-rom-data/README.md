# RDM6300 RFID - PicoRV32 RISC-V SoC with SPI Flash Data Storage

## 1. Tổng quan Kiến trúc (System Architecture)
Dự án được thiết kế theo cấu trúc mô-đun hóa cao cấp, phân chia thành 3 phân vùng độc lập và một lõi tích hợp trung tâm:
- **Phân vùng Lõi trung tâm (`rtl/core/`)**:
  - [picorv32.v](file:///d:/VirtualSharedFolders/uart-fifo-rfid-asic/rdm6300-picorv32-rom-data/rtl/core/picorv32.v): Nhân CPU RISC-V RV32I 32-bit.
  - [data_sram.v](file:///d:/VirtualSharedFolders/uart-fifo-rfid-asic/rdm6300-picorv32-rom-data/rtl/core/data_sram.v): 1KB On-Chip Data SRAM (Scratchpad/Stack, độ trễ 1 chu kỳ).
  - [spimemio.v](file:///d:/VirtualSharedFolders/uart-fifo-rfid-asic/rdm6300-picorv32-rom-data/rtl/core/spimemio.v): Bộ điều khiển SPI Flash Quad-SPI hỗ trợ XIP (Execute-In-Place) trực tiếp từ Flash.
  - [soc_interconnect.v](file:///d:/VirtualSharedFolders/uart-fifo-rfid-asic/rdm6300-picorv32-rom-data/rtl/core/soc_interconnect.v): Bộ giải mã địa chỉ và liên kết bus trung tâm (Crossbar / Interconnect).
  - [soc_gpio_mmio.v](file:///d:/VirtualSharedFolders/uart-fifo-rfid-asic/rdm6300-picorv32-rom-data/rtl/core/soc_gpio_mmio.v): Bộ điều khiển GPIO MMIO (16 LED trạng thái).
  - [sync_2ff.v](file:///d:/VirtualSharedFolders/uart-fifo-rfid-asic/rdm6300-picorv32-rom-data/rtl/core/sync_2ff.v): Bộ đồng bộ tín hiệu 2 tầng Flip-Flop chống hiện tượng siêu ổn định (CDC Metastability).
- **Phân vùng Ngoại vi RFID RDM6300 (`rtl/rdm6300/`)**:
  - [uart_rx.v](file:///d:/VirtualSharedFolders/uart-fifo-rfid-asic/rdm6300-picorv32-rom-data/rtl/rdm6300/uart_rx.v): Bộ thu UART 9600 baud tích hợp bộ lọc nhiễu đa số (Majority Voting).
  - [rdm6300_frame_decoder.v](file:///d:/VirtualSharedFolders/uart-fifo-rfid-asic/rdm6300-picorv32-rom-data/rtl/rdm6300/rdm6300_frame_decoder.v): Bộ giải mã khung 14-byte ASCII và cây tính chẵn lẻ XOR phần cứng (1 chu kỳ).
  - [rdm6300_mmio.v](file:///d:/VirtualSharedFolders/uart-fifo-rfid-asic/rdm6300-picorv32-rom-data/rtl/rdm6300/rdm6300_mmio.v): Bộ điều khiển giao tiếp MMIO cho ngoại vi RFID.
- **Phân vùng Giao tiếp Máy tính Chủ (`rtl/host/`)**:
  - [simpleuart.v](file:///d:/VirtualSharedFolders/uart-fifo-rfid-asic/rdm6300-picorv32-rom-data/rtl/host/simpleuart.v): Bộ thu phát UART siêu tinh gọn cho Host PC (115200 baud).
  - [sync_fifo.v](file:///d:/VirtualSharedFolders/uart-fifo-rfid-asic/rdm6300-picorv32-rom-data/rtl/host/sync_fifo.v): Bộ đệm phần cứng FIFO đồng bộ (16 phần tử).
  - [simpleuart_fifo.v](file:///d:/VirtualSharedFolders/uart-fifo-rfid-asic/rdm6300-picorv32-rom-data/rtl/host/simpleuart_fifo.v): UART tích hợp 2 hàng đợi TX/RX FIFO chống tràn dữ liệu.
  - [host_uart_mmio.v](file:///d:/VirtualSharedFolders/uart-fifo-rfid-asic/rdm6300-picorv32-rom-data/rtl/host/host_uart_mmio.v): Bộ điều khiển giao tiếp MMIO Host UART.
- **Top-Level SoC (`rtl/rdm6300_picorv32_soc.v`)**:
  - Tích hợp toàn diện 14 module phần cứng, liên kết bus, quản lý tín hiệu đồng bộ và phân phối địa chỉ.

---

## 2. Bản đồ Bộ nhớ MMIO (Memory Map)
| Dải địa chỉ | Ngoại vi / Chức năng | Mô tả chi tiết |
| :--- | :--- | :--- |
| `0x0000_0000 - 0x0000_03FF` | **1KB Data SRAM** | Scratchpad RAM on-chip, chứa biến cục bộ và ngăn xếp (Stack) của CPU PicoRV32. |
| `0x0025_0000 - 0x003F_FFFF` | **SPI Flash XIP Area** | Thực thi trực tiếp mã lệnh firmware (XIP) từ bộ nhớ Flash Spansion S25FL032P. |
| `0x0200_0000` | **SPI Flash Config Reg** | Thanh ghi cấu hình SPI Mode và tần số xung SCK của `spimemio`. |
| `0x1000_0000 - 0x1000_0008` | **RDM6300 RFID MMIO** | `0x00`: Status (bit 0: `tag_ready`); `0x04`: Tag Hi (8-bit); `0x08`: Tag Lo (32-bit). |
| `0x3000_0000 - 0x3000_0004` | **Host PC UART MMIO** | `0x00`: Clock Divider; `0x04`: TX/RX Data FIFO (giao tiếp PC 115200 baud). |
| `0x4000_0000` | **SoC GPIO / LEDs** | Điều khiển 16 LED trạng thái trên bo mạch Basys 3 hoặc ASIC IO pads. |

---

## 3. Cấu trúc Thư mục Dự Án
```text
rdm6300-picorv32-rom-data/
├── config.json                             # Cấu hình OpenLane 2 ASIC Flow (14 module RTL)
├── pin_order.cfg                           # Quy hoạch chân Floorplan ASIC
├── constraints.sdc                         # Ràng buộc thời gian tổng hợp ASIC SDC (50MHz)
├── run_fast.sh                             # Kịch bản OpenLane Dockerized siêu tốc trên Linux
├── build_all.bat                           # Kịch bản tự động hóa 4 bước biên dịch & nạp Flash
├── rtl/                                    # Toàn bộ mã nguồn Verilog RTL (14 files)
│   ├── core/                               # Phân vùng Lõi xử lý trung tâm
│   │   ├── picorv32.v
│   │   ├── data_sram.v
│   │   ├── spimemio.v
│   │   ├── soc_interconnect.v
│   │   ├── soc_gpio_mmio.v
│   │   └── sync_2ff.v
│   ├── rdm6300/                            # Phân vùng Ngoại vi RFID
│   │   ├── uart_rx.v
│   │   ├── rdm6300_frame_decoder.v
│   │   └── rdm6300_mmio.v
│   ├── host/                               # Phân vùng Giao tiếp Máy tính
│   │   ├── simpleuart.v
│   │   ├── sync_fifo.v
│   │   ├── simpleuart_fifo.v
│   │   └── host_uart_mmio.v
│   └── rdm6300_picorv32_soc.v              # Module đỉnh SoC tích hợp
├── fpga/                                   # Thiết kế FPGA Basys 3 (Vivado Flow)
│   ├── rtl/top_basys3_picorv32_rdm6300.v   # Wrapper FPGA Basys 3 (STARTUPE2 CCLK)
│   ├── constraints/basys3_picorv32_rdm6300.xdc # Constraints chân Basys 3
│   ├── build_vivado_basys3.tcl             # Kịch bản TCL tổng hợp & sinh Bitstream
│   ├── generate_bitstream.bat              # Script build Bitstream Vivado
│   ├── generate_flash_image.bat            # Script tạo file Flash (.bin & .mcs)
│   └── program_flash.bat                   # Script nạp SPI Flash qua cáp USB JTAG
├── firmware/                               # Phần mềm Firmware C cho PicoRV32
│   ├── main.c                              # Chương trình điều khiển Access Control
│   ├── start.s                             # File khởi động Assembly RV32I
│   ├── sections.lds                        # Linker script phân bổ bộ nhớ Flash XIP & SRAM
│   └── build_firmware.bat                  # Script biên dịch firmware ra .hex & .bin
├── host/                                   # Phần mềm giao tiếp trên máy tính Host PC
│   ├── main.c                              # Chương trình C Win32 Serial Console
│   └── build.bat                           # Script biên dịch console app bằng GCC/MSVC
└── tb/                                     # Hệ sinh thái Kiểm thử & Testbench (63 Test Cases)
    ├── run_all_testbenches.bat             # Chạy toàn bộ 5 bước kiểm thử tự động
    ├── run_all_testbenches.py              # Master Python Verification Suite (100% PASS)
    ├── step2_firmware/                     # Bước 2: Testbench Firmware (21 TCs)
    ├── step3_picorv32_sram/                # Bước 3: Testbench CPU & 1KB SRAM (12 TCs)
    ├── step4_spimemio_flash/               # Bước 4: Testbench SPI Flash XIP (10 TCs)
    ├── step5_rdm6300_pipeline/             # Bước 5: Testbench RDM6300 Pipeline (12 TCs)
    └── step6_top_soc_integration/          # Bước 6: Testbench Top SoC Tích Hợp (8 TCs)
```

---

## 4. Hướng dẫn Biên Dịch & Chạy Hệ Thống

### A. Kiểm thử toàn diện Testbench (63/63 Test Cases PASS 100%)
Chạy script kiểm thử tự động:
```cmd
cd tb
run_all_testbenches.bat
```
Hoặc mô phỏng chi tiết trên Vivado Simulator (xsim):
```cmd
cd tb\step6_top_soc_integration
run_vivado_sim.bat
```

### B. Biên dịch Firmware C cho CPU PicoRV32
```cmd
cd firmware
build_firmware.bat
```

### C. Biên dịch Bitstream & Nạp Flash Bo Mạch Basys 3 (Tự động 1-Click)
Tại thư mục gốc dự án:
```cmd
build_all.bat
```
Quy trình sẽ tự động:
1. Biên dịch Firmware C ra `firmware.bin` và `firmware.hex`.
2. Chạy Vivado ở chế độ batch tổng hợp toàn bộ 14 module Verilog và sinh Bitstream `top_basys3_picorv32_rdm6300.bit`.
3. Kết hợp Bitstream (offset `0x0000_0000`) và Firmware (offset `0x0025_0000`) thành file ảnh Flash `top_basys3_picorv32_rdm6300_flash.bin` và `.mcs`.
4. Nạp trực tiếp vào bộ nhớ Spansion SPI Flash trên bo Basys 3 để khởi động tự động không cần máy tính khi bật nguồn (Jumper JP1 đặt tại QSPI).

### D. Biên dịch & Chạy Ứng Dụng Quản Lý Máy Tính (Host PC)
```cmd
cd host
build.bat
rdm6300_manager.exe
```
