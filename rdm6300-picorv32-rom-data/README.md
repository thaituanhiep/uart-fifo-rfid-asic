# RDM6300 RFID - PicoRV32 RISC-V SoC

Du an nay da duoc tinh gon de phuc vu viec review code. Repo hien chi giu lai source code, cac script build/chay, mot so file nhi phan can thiet (`.exe`, `.bin`) va tai lieu chinh (`.docx`, `.pptx`).

## Cau truc hien tai

```text
rdm6300-picorv32-rom-data/
|-- README.md
|-- build_all.bat
|-- config.json
|-- constraints.sdc
|-- pin_order.cfg
|-- run_fast.sh
|-- document/
|   |-- Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.docx
|   |-- Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.pptx
|   `-- Tom_Tat_Do_An_RDM6300_PicoRV32_SoC.docx
|-- firmware/
|   |-- Makefile
|   |-- bin2hex.c
|   |-- bin2hex.exe
|   |-- bin2hex.py
|   |-- build_firmware.bat
|   |-- main.c
|   |-- sections.lds
|   |-- start.s
|   |-- app/
|   |   |-- access_control.c
|   |   `-- access_control.h
|   |-- common/
|   |   |-- hex_utils.c
|   |   |-- hex_utils.h
|   |   `-- soc_regs.h
|   |-- drivers/
|   |   |-- flash.c
|   |   |-- flash.h
|   |   |-- uart.c
|   |   `-- uart.h
|   `-- protocol/
|       |-- rdm6300_parser.c
|       `-- rdm6300_parser.h
|-- fpga/
|   |-- build_vivado_basys3.tcl
|   |-- generate_bitstream.bat
|   |-- generate_flash_image.bat
|   |-- generate_flash_image.tcl
|   |-- program_basys3.bat
|   |-- program_basys3.tcl
|   |-- program_flash.bat
|   |-- program_flash.tcl
|   |-- top_basys3_picorv32_rdm6300_flash.bin
|   |-- constraints/
|   |   `-- basys3_picorv32_rdm6300.xdc
|   |-- rtl/
|   |   `-- top_basys3_picorv32_rdm6300.v
|   `-- vivado/
|       |-- clockInfo.txt
|       |-- dfx_runtime.txt
|       |-- vivado.jou
|       |-- vivado.log
|       `-- vivado_*.backup.{jou,log}
|-- host/
|   |-- build.bat
|   |-- main.c
|   `-- rdm6300_manager.exe
|-- rtl/
|   |-- rdm6300_picorv32_soc.v
|   |-- core/
|   |   |-- data_sram.v
|   |   |-- picorv32.v
|   |   |-- soc_gpio_mmio.v
|   |   |-- soc_interconnect.v
|   |   `-- spimemio.v
|   `-- uart/
|       |-- simpleuart.v
|       |-- simpleuart_fifo.v
|       |-- sync_2ff.v
|       |-- sync_fifo.v
|       |-- uart_mmio.v
|       `-- uart_rx.v
`-- tb/
    |-- README.md
    |-- dfx_runtime.txt
    |-- run_all_tb.bat
    |-- run_sim_ping.bat
    |-- run_sim_uart.bat
    |-- tb_uart_ping.v
    `-- tb_uart_rtl.v
```

## Mo ta cac khoi chinh

### RTL SoC
- `rtl/rdm6300_picorv32_soc.v`: top-level SoC, ket noi CPU PicoRV32, bo nho, UART va logic ngoai vi.
- `rtl/core/`: cac khoi trung tam nhu CPU, SRAM, SPI flash interface, interconnect, GPIO.
- `rtl/uart/`: cac khoi UART, FIFO dong bo va MMIO phuc vu giao tiep voi host va RFID path hien tai.

### Firmware
- `firmware/main.c`: firmware chinh chay tren PicoRV32.
- `firmware/app/`: logic access control.
- `firmware/drivers/`: driver UART va SPI flash.
- `firmware/protocol/`: parser khung du lieu RDM6300.
- `firmware/bin2hex.*`: cong cu chuyen doi firmware sang dang du lieu phu hop cho flow nap/nhung.

### FPGA
- `fpga/rtl/top_basys3_picorv32_rdm6300.v`: wrapper top cho board Basys 3.
- `fpga/*.tcl`, `fpga/*.bat`: script build bitstream, tao flash image va nap board.
- `fpga/top_basys3_picorv32_rdm6300_flash.bin`: flash image da sinh san duoc giu lai.
- `fpga/vivado/`: nhat ky va file thong tin moi truong Vivado duoc giu lai tren nhanh review nay.

### Host
- `host/main.c`: chuong trinh host giao tiep serial.
- `host/build.bat`: script build tren Windows.
- `host/rdm6300_manager.exe`: ban build san co de demo nhanh.

### Testbench
- `tb/tb_uart_rtl.v`: testbench cho khoi UART/MMIO/FIFO.
- `tb/tb_uart_ping.v`: testbench tich hop cho top-level SoC.
- `tb/run_*.bat`: script chay mo phong tren Windows.
- `tb/README.md`: tai lieu rieng cho he thong testbench.

## Cach dung nhanh

### Build firmware
```cmd
cd firmware
build_firmware.bat
```

### Build FPGA / tao flash image
```cmd
cd ..
build_all.bat
```

### Build host app
```cmd
cd host
build.bat
rdm6300_manager.exe
```

### Chay testbench
```cmd
cd tb
run_all_tb.bat
```

## Y nghia cac file build va run

| File | Vai tro |
| :--- | :--- |
| `build_all.bat` | Script tong hop o muc du an: build firmware, sinh bitstream FPGA, tao flash image, va co the nap SPI flash cho Basys 3. |
| `firmware\build_firmware.bat` | Bien dich firmware RISC-V bang GCC, tao `firmware.elf`, `firmware.bin`, `firmware.hex`, roi copy `firmware.hex` sang `rtl\`, `rtl\core\`, `fpga\rtl\`, `tb\` de dung cho FPGA va testbench. |
| `host\build.bat` | Bien dich chuong trinh host tren Windows thanh `rdm6300_manager.exe` bang GCC hoac MSVC. |
| `fpga\generate_bitstream.bat` | Goi Vivado batch mode de tong hop va route thiet ke Basys 3, sau do sinh file bitstream `.bit`. |
| `fpga\generate_flash_image.bat` | Goi script TCL de dong goi bitstream va firmware thanh flash image `.bin`/`.mcs` dung cho bo nho QSPI. |
| `fpga\program_basys3.bat` | Nap truc tiep file bitstream vao FPGA qua USB JTAG; dung cho chay tam thoi sau moi lan cap nguon. |
| `fpga\program_flash.bat` | Nap flash image vao SPI flash tren board de he thong tu boot lai sau khi tat/mo nguon. |
| `tb\run_sim_uart.bat` | Compile, elaborate va chay mo phong `tb_uart_rtl.v` trong Vivado Simulator de kiem tra khoi UART/MMIO/FIFO. |
| `tb\run_sim_ping.bat` | Compile, elaborate va chay mo phong `tb_uart_ping.v` cho toan bo SoC, bao gom boot firmware tu SPI flash model. |
| `tb\run_all_tb.bat` | Chay lan luot 2 bai mo phong `run_sim_uart.bat` va `run_sim_ping.bat`; dung nhu quick regression suite. |
| `run_fast.sh` | Script Linux de chay nhanh luong OpenLane/OpenROAD cho huong ASIC. |

## Dau ra build quan trong

| File dau ra | Nguon sinh ra | Y nghia |
| :--- | :--- | :--- |
| `firmware\firmware.elf` | `firmware\build_firmware.bat` | File ELF de debug/phan tich firmware. |
| `firmware\firmware.bin` | `firmware\build_firmware.bat` | Ban nhi phan thuan cua firmware. |
| `firmware\firmware.hex` | `firmware\build_firmware.bat` | Ban HEX de nhung vao mo phong/RTL. |
| `fpga\top_basys3_picorv32_rdm6300.bit` | `fpga\generate_bitstream.bat` | Bitstream nap tam thoi vao FPGA. |
| `fpga\top_basys3_picorv32_rdm6300_flash.bin` | `fpga\generate_flash_image.bat` | Anh flash tong hop giua bitstream va firmware, phuc vu boot QSPI. |
| `fpga\top_basys3_picorv32_rdm6300_flash.mcs` | `fpga\generate_flash_image.bat` | Dinh dang flash image thuong dung trong flow Vivado Hardware Manager. |
| `host\rdm6300_manager.exe` | `host\build.bat` | Chuong trinh host de giao tiep serial voi he thong. |

## Ghi chu

- Nhanh nay da loai bo phan lon file tam, hinh anh, artifact sinh tu dong va tai lieu phu tro khong can thiet.
- 2 file CSV moi nhat trong `host/` duoc giu lai rieng theo yeu cau.
