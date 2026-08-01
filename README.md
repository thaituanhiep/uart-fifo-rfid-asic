# UART FIFO Verilog Project (ASIC + FPGA)

Project khung cho UART + FIFO viết bằng Verilog, dùng chung RTL cho:
- OpenLane ASIC flow (block-level)
- FPGA Basys3 với Vivado

Hiện tại đã có top riêng cho Basys3 dùng RDM6300:

- `rtl/top_basys3_rdm6300.v`

Luồng dữ liệu:

- RDM6300 TX UART -> Basys3 `rdm6300_rx_i`
- Basys3 đọc byte vào RX FIFO
- Logic bridge trong top đẩy dữ liệu sang TX FIFO
- UART TX của Basys3 -> USB-UART onboard -> Putty trên PC

LED debug trên Basys3 (top_basys3_rdm6300):

- `led[0]`: heartbeat (nháy liên tục nếu bitstream chạy)
- `led[1]`: có byte đi từ RX FIFO
- `led[2]`: có byte ghi sang TX FIFO
- `led[3]`: báo reset đang active hoặc FIFO full

## Cấu trúc

- `rtl/`
  - `fifo_sync.v`: FIFO đồng bộ tham số hóa
  - `uart_rx.v`: UART receiver 8N1
  - `uart_tx.v`: UART transmitter 8N1
  - `uart_fifo_core.v`: core tích hợp UART RX/TX + RX/TX FIFO
  - `top_basys3_rdm6300.v`: top cho Basys3 (RDM6300 passthrough sang PC)
- `sim/`
  - `tb_uart_fifo_core.v`: testbench loopback mức core
  - `run_iverilog.ps1`: script chạy mô phỏng nhanh với Icarus Verilog
- `openlane/uart_fifo_core/config.tcl`: cấu hình OpenLane cho block `uart_fifo_core`
- `fpga/vivado/create_project.tcl`: script tạo project Vivado Basys3
- `constraints/basys3_template.xdc`: chân cho `top_basys3_rdm6300`

## Mô phỏng nhanh

Yêu cầu cài Icarus Verilog (`iverilog`, `vvp`).

Trên PowerShell:

```powershell
cd sim
./run_iverilog.ps1
```

## OpenLane (block-level)

Khi chạy OpenLane, dùng design config tại:

- `openlane/uart_fifo_core/config.tcl`

Lưu ý:
- Đây là flow mức block cho `uart_fifo_core`, chưa phải full chip có padframe/top IO ring.
- Khi cần tapeout flow đầy đủ, bạn sẽ thêm top-level wrapper và cấu hình IO/pad tương ứng.

## Vivado Basys3

Trong Vivado Tcl console (từ root project):

```tcl
source fpga/vivado/create_project.tcl
```

Sau đó:
1. Run Synthesis/Implementation/Bitstream.
2. Mở Putty đúng COM của Basys3 USB-UART, baud `9600`, 8 data bits, no parity, 1 stop bit.

### Wiring RDM6300 -> Basys3

- `RDM6300 TX` -> `JA1` (pin `J1`) của Basys3, tương ứng cổng `rdm6300_rx_i`.
- `GND RDM6300` -> `GND Basys3` (bắt buộc chung mass).
- `uart_tx_o` của FPGA đi qua USB-UART onboard ra PC (Putty đọc tại COM của board, pin `A18` theo Basys3 Master XDC).

Lưu ý mức điện áp:

- IO của Basys3 là 3.3V. Nếu TX của module RDM6300 là 5V TTL, cần mạch chia áp hoặc level shifter trước khi vào JA1.

## Gợi ý bước tiếp theo

- Thêm parser frame RFID (start/end byte, checksum) nếu muốn lọc đúng payload thẻ.
- Thêm debounce/reset sync cho `rst_btn` để tăng độ ổn định hệ thống.
- Viết testbench riêng cho top Basys3 với luồng UART passthrough dài hơn.
