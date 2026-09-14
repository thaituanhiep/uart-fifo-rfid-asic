# RDM6300 Basys3 FPGA Modular Project

The synthesizable datapath is intentionally small. The validated 40-bit tag flows
directly from the frame decoder into the binary packet encoder.

`top_basys3_rdm6300` directly contains the FPGA power-up reset, RFID input
synchronizer and complete UART/FIFO/Parser pipeline. Buttons, LEDs and
PC-to-FPGA commands are omitted.

The end-to-end burst regression drives 64 distinct RFID frames through UART RX and
requires 64 ordered, CRC-correct UART TX packets with no decoder/encoder collision.

Duplicate timeout, field extraction, decimal formatting, counters, history and access
policy belong to the Node.js host and SQLite database, not the FPGA RTL.

Project được tối giản theo nguyên tắc: **một FPGA top duy nhất**, **module cục bộ
chỉ thực hiện một chức năng**, và **top nối pipeline bằng `valid/ready`**.

## Cấu trúc

```text
rtl/             Toàn bộ các file RTL verilog (sync_2ff, rx_fifo, tx_fifo, uart_rx, uart_tx, rdm6300_frame_decoder, card_packet_encoder, rfid_parser)
fpga/rtl/        Top-level hoàn chỉnh cho Basys3
fpga/constraints XDC riêng cho board
tb/              Testbench theo module
```

## Top-level

- FPGA Basys3: `top_basys3_rdm6300`
- Unit test đầu tiên: `rdm6300_frame_decoder`

## Luồng dữ liệu

```text
RDM6300 UART RX
  -> top_basys3_rdm6300
       -> sync_2ff
       -> UART RX
       -> RX FIFO
       -> RFID parser
       -> RDM6300 frame decoder
       -> binary packet encoder (A5 5A 01 05 TAG[4:0] CRC8)
       -> TX FIFO
       -> UART TX to PC
```

## Điểm đã chuẩn hóa

- Giữ 2-FF synchronizer tại biên input FPGA.
- Tách parser/checksum khỏi controller cấp cao.
- Chuyển duplicate timeout và định dạng ASCII/thập phân lên Backend.
- UART RX dùng 16x oversampling, majority vote ba mẫu giữa bit, kiểm tra
  stop bit và phát hiện UART BREAK.
- Decoder có timeout liên byte, resynchronization bằng STX mới và tách riêng
  checksum, cấu trúc frame, ký tự hex sai và frame timeout.
- Giữ giao tiếp reset active-low nhất quán bên trong các module.
- Có filelist riêng cho FPGA và từng testbench.
- `top_basys3_rdm6300` instantiate trực tiếp synchronizer, UART RX, RX FIFO,
  Parser, TX FIFO và UART TX; không còn `rdm6300_access_core` hay `uart_fifo_core`.
- Các chặng RX FIFO -> Parser -> TX FIFO -> UART TX dùng handshake
  `valid/ready`. Top chỉ nối luồng và backpressure, không giữ transfer FSM.
- RX FIFO và TX FIFO luôn expose phần tử đầu khi `out_valid=1`; con trỏ chỉ
  tiến khi `out_valid && out_ready`.

`rdm6300_frame_decoder.v` vẫn cần thiết: đây là phần Parser xử lý giao thức
RDM6300 (STX/ETX, ASCII-hex, checksum, timeout và resynchronization). Nó chỉ có
thể bị bỏ nếu toàn bộ logic này được chuyển nguyên vẹn vào `rfid_parser.v`.

## Phạm vi xử lý

RTL hoạt động xuất gói nhị phân 10 byte có CRC-8. Backend chịu trách nhiệm tách
Facility/Card Number, định dạng thập phân, lọc trùng, history và policy.

Các hướng mở rộng về sau vẫn có thể cân nhắc:

1. Xuất dữ liệu qua register interface khi tích hợp SoC.
2. Bổ sung firmware/ESP32 làm transport thay cho UART trực tiếp.

Ngoài ra nên bổ sung overflow counters, timeout khi khung thiếu ETX, assertions, coverage và testbench end-to-end.

## Vivado

Thêm toàn bộ file trong `filelists/fpga_basys3.f`, đặt top là `top_basys3_rdm6300`, rồi thêm `fpga/constraints/basys3_rdm6300.xdc`.

Hoặc build trực tiếp từ source chuẩn hóa (không dùng các bản source đã copy vào project cũ):

```text
vivado -mode batch -source scripts/build_basys3.tcl
```

Bitstream và các báo cáo được tạo trong `build/basys3/`.

Flow ASIC/OpenLane không còn nằm trong source/filelist của thư mục FPGA này;
nếu cần ASIC, dùng workspace OpenLane riêng đã backup.
