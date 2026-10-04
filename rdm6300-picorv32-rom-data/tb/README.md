# Hệ Thống Testbench & Môi Trường Kiểm Thử SoC PicoRV32 RFID RDM6300

Thư mục `tb/` được tinh gọn tập trung vào 2 bài test cốt lõi:
1. **`tb_uart_rtl.v`**: Kiểm thử Pure RTL cấp module cho khối ngoại vi UART MMIO (`uart_mmio.v`), bộ đệm FIFO 32 byte (`sync_fifo.v`), và bộ truyền nhận (`simpleuart.v`, `simpleuart_fifo.v`).
2. **`tb_uart_ping.v`**: Kiểm thử tích hợp toàn diện Top SoC (`rdm6300_picorv32_soc.v`), mô phỏng CPU PicoRV32 khởi động mã C thực tế từ mô hình SPI Flash XIP (`firmware.hex`), xuất chuỗi chào mừng qua UART và xử lý lệnh kiểm tra kết nối Ping ('P' -> "PONG").

---

## 1. Cấu Trúc Thư Mục Tinh Gọn (`tb/`)

```
tb/
├── tb_uart_rtl.v        # Testbench RTL thuần kiểm thử ngoại vi UART MMIO, bus cycle, FIFO
├── tb_uart_ping.v       # Testbench Top SoC: Boot C firmware từ SPI Flash, Ping-Pong UART
├── firmware.hex         # Mã máy Verilog HEX thực thi (RV32IMC) nạp vào mô hình SPI Flash
├── run_sim_uart.bat     # Script chạy mô phỏng tb_uart_rtl trên Vivado Simulator (xsim)
├── run_sim_ping.bat     # Script chạy mô phỏng tb_uart_ping trên Vivado Simulator (xsim)
├── run_all_tb.bat       # Master runner chạy tuần tự cả 2 testbench
└── README.md            # Tài liệu đặc tả testbench
```

---

## 2. Đặc Tả Chi Tiết Từng Testbench

### 2.1. Testbench UART RTL (`tb_uart_rtl.v`)
- **Mục tiêu**: Kiểm tra độ chính xác phần cứng của bộ điều khiển UART MMIO mà không cần nhân CPU.
- **Các kịch bản kiểm thử**:
  1. *Default Divider*: Kiểm tra thanh ghi Prescaler tại offset `0x00` nạp đúng `DEFAULT_DIV`.
  2. *Divider Configuration*: Ghi và đọc lại giá trị Prescaler mới qua bus MMIO.
  3. *Serial TX Waveform*: Ghi ký tự vào offset `0x04`, kiểm tra dạng sóng nối tiếp (Start bit, 8 data bits LSB-first, Stop bit).
  4. *Serial RX & FIFO*: Bắn tín hiệu nối tiếp vào chân `rx_i`, xác nhận cờ `rx_activity_o` tích cực và đọc dữ liệu qua offset `0x04`. Kiểm tra trả về `0xFFFFFFFF` khi FIFO rỗng.
  5. *Multi-Byte Burst*: Bắn liên tiếp nhiều byte dữ liệu kiểm tra cơ chế chống tràn của FIFO.

### 2.2. Testbench Top SoC Ping-Pong (`tb_uart_ping.v`)
- **Mục tiêu**: Kiểm tra hệ thống Top-level hoàn chỉnh gồm CPU PicoRV32, SPI Flash Controller (`spimemio`), 1KB SRAM, Interconnect và UART.
- **Các kịch bản kiểm thử**:
  1. *Power-On Reset & Boot Flash*: CPU PicoRV32 thức dậy tại vector `0x00250000`, đọc lệnh qua XIP từ mô hình SPI Flash (nạp từ `firmware.hex`).
  2. *C Startup Banner*: CPU in toàn bộ chuỗi chào mừng ra cổng UART Host PC.
  3. *Host Ping Processing*: Testbench đóng vai trò PC Host gửi byte lệnh `'P'` (`0x50`) và `'\n'` (`0x0A`).
  4. *Response Verification*: CPU phản hồi chuỗi `"PONG: PicoRV32 Active"`.
  5. *CPU Health*: Khẳng định `cpu_trap == 0` (CPU hoạt động mượt mà, không gặp lệnh lỗi hoặc tràn bộ nhớ).

---

## 3. Hướng Dẫn Chạy Mô Phỏng 1-Click

Yêu cầu môi trường: AMD Vivado 2025.1 hoặc mới hơn đã cài đặt trên máy.

- **Chạy toàn bộ test suite (Khuyến nghị)**:
  ```cmd
  run_all_tb.bat
  ```

- **Chạy riêng lẻ từng bài test**:
  ```cmd
  run_sim_uart.bat   :: Kiểm thử UART RTL
  run_sim_ping.bat   :: Kiểm thử Top SoC Boot & Ping
  ```
