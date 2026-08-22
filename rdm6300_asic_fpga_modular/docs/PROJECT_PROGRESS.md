# RDM6300 Basys3 FPGA Project Progress

## Current lean-RTL baseline

- Basys3 buttons and LEDs removed from top-level ports and XDC.
- Status/register interface and bidirectional host-command path removed.
- Convenience counters/sticky flags removed; scan totals remain in host SQLite.
- Reset synchronizer and pulse stretcher removed from synthesis sources.
- Decoder, binary packet encoder, independent `rx_fifo`/`tx_fifo` modules and error pulses remain.
- Logic top directly instantiates UART RX, RX FIFO, Parser, TX FIFO and UART TX.
- Pipeline transfers use `valid/ready`; top has no RX/TX transfer FSM or busy/done tracking.
- `rdm6300_access_core`, `uart_fifo_core` and the shared `fifo_sync` module were removed.
- Burst/end-to-end testbenches remain verification-only and are not synthesized.

The older sections below are project history, not the current synthesis source list.

## Historical: bidirectional host diagnostics (removed)

- Basys3 onboard USB-UART RX (B18) now accepts register-read and diagnostic-clear commands.
- The compact line protocol supports `Rxx`, `C`, `@Rxx=dddddddd`, `@OK`, and `@ERR`.
- Command responses share TX FIFO/UART with card output using message-safe arbitration;
  responses cannot split a formatted card line.
- Node.js exposes `GET /api/diagnostics` and `POST /api/diagnostics/clear`.
- WebUI includes a Diagnostics panel for identity, version, flags, sequence, tag, and counters.
- Physical UART waveform simulation passes read, clear, and invalid-command responses.

## Status/register interface v1

- A technology-neutral one-clock read/write bus exposes device ID, RTL version,
  capabilities, live/sticky flags, last accepted card, raw tag, and card sequence.
- All decoder, UART, duplicate, and FIFO-overflow counters are readable as 32-bit registers.
- `CONTROL[0]` clears diagnostic sticky flags/counters without resetting the datapath
  or discarding queued card events.
- Unknown addresses and simultaneous read/write operations report a bus error.
- Standalone register-map verification, integrated diagnostic clear, top compile,
  and normal UART end-to-end regression all pass.

## Human-visible card indication

- LED0 now remains active for 500 ms after each accepted card event.
- A new card event while LED0 is active restarts the complete 500 ms interval.
- LED1 no longer uses duplicate sticky state; it returns to the instantaneous
  duplicate pulse while the duplicate counter remains available internally.
- LED2 decoder/UART sticky diagnostics and LED3 overflow diagnostics are unchanged.

## Complete error telemetry

- Saturating 16-bit counters and sticky flags now cover checksum, frame structure,
  invalid hex, frame timeout, UART framing, UART BREAK, and duplicate-card events.
- BREAK is edge-counted, so one continuous LOW incident increments its counter once.
- Basys3 LED1 now holds duplicate status and LED2 holds UART/decoder error status until reset.
- `tb_rdm6300_error_counters.v` injects every error class, verifies the counters/sticky
  flags, and verifies that reset clears all diagnostic state.

## Current direct-path burst/end-to-end verification

- `tb_top_basys3_rdm6300_burst.v` sends 64 valid, distinct RDM6300 frames through
  the physical UART RX waveform path without bypassing the decoder.
- Every decoded tag goes directly into the binary Packet Encoder and then the TX FIFO.
- The test requires 64 decoded frames and 64 ordered, CRC-correct output packets.
- The test fails immediately if a decoded event arrives while Packet Encoder is busy.
- No checksum, frame, invalid-hex, timeout, RX FIFO, TX FIFO, framing, or BREAK
  error occurs during the valid burst.

## Removed historical event buffering

- The former card-event FIFO, its parameters, ports, testbench and filelist were removed.
- A 14-byte input frame takes longer than the 10-byte output packet at equal baud,
  allowing a direct Decoder-to-Packet-Encoder connection for this fixed protocol.

## Reset conditioning

- The Basys3 reset button now asserts the internal active-low reset immediately.
- Reset release crosses a two-stage synchronizer and only reaches the core on a
  100 MHz clock edge.
- The synchronizer registers carry the `ASYNC_REG` implementation attribute.
- `tb_reset_sync.v` verifies asynchronous assertion, two-stage release, and rejection
  of a release pulse that is shorter than the required clock crossings.

Tài liệu này theo dõi các hạng mục đã hoàn thành và thứ tự nâng cấp tiếp theo.
Nguồn RTL chuẩn duy nhất nằm trong `rdm6300_asic_fpga_modular/`.

## Đã hoàn thành

### Kiến trúc module

- UART RX và UART TX tách riêng.
- RX FIFO và TX FIFO tách thành hai file/module `rx_fifo` và `tx_fifo`.
- Decoder RDM6300 tách riêng: STX/ETX, ASCII hex, checksum và card fields.
- Duplicate filter tách riêng, có timeout nhận lại cùng thẻ sau khi rời anten.
- ASCII formatter tách riêng.
- Toàn bộ pipeline được instantiate trực tiếp trong `top_basys3_rdm6300`.
- Đồng bộ UART bất đồng bộ đặt tại biên FPGA bằng `sync_2ff`.
- Filelist riêng cho FPGA và từng testbench.

### Formatter tuần tự

- Thay toàn bộ phép chia/modulo tổ hợp bằng double-dabble tuần tự 32 bước.
- Giữ nguyên giao tiếp `valid/ready` và output `ID10 FC3,CN5\n`.
- Có FSM tách ba pha: capture, convert và stream.
- Test giá trị thực tế `0007534416 114,63312\n`.
- Test giá trị cực đại `4294967295 255,65535\n`.
- Test backpressure khi đầu ra tạm thời chưa sẵn sàng.

### Verification hiện có

- `tb_rdm6300_frame_decoder.v`: frame RDM6300 hợp lệ.
- `tb_top_basys3_rdm6300_end_to_end.v`: waveform UART vào đi qua toàn bộ
  RX FIFO, Decoder, Packet Encoder, TX FIFO và UART ra.
- `tb_uart_rx_noise.v`: 16x oversampling, majority vote, một mẫu bị nhiễu,
  lệch baud, start giả, stop lỗi, BREAK và phục hồi frame kế tiếp.

### UART RX chống nhiễu

- 16x oversampling với ba mẫu giữa bit (7, 8, 9).
- Majority vote 2/3; một mẫu giữa bit bị sai không làm sai dữ liệu.
- Xác nhận start bit để loại xung LOW ngắn.
- Kiểm tra stop bit và phát `uart_framing_error`.
- Phát hiện đường RX bị giữ LOW bằng `uart_break_detect`.
- Hủy frame dở và tự phục hồi sau BREAK.
- Hai trạng thái lỗi được đưa lên LED lỗi trong wrapper Basys3.

### Decoder tự phục hồi

- Timeout liên byte mặc định 5 ms tại 100 MHz.
- Frame thiếu byte tự bị hủy và decoder trở về chờ STX.
- STX mới giữa frame dở trở thành điểm resynchronization ngay lập tức.
- ETX đến sớm hoặc byte thừa sau 12 digit tạo `frame_error`.
- Ký tự ngoài ASCII hex tạo `invalid_hex_error` riêng.
- Checksum không khớp tạo `checksum_error` riêng.
- `frame_timeout_error` tách biệt để chẩn đoán frame bị ngắt.
- Test frame đúng, checksum sai, invalid hex, ETX sớm, timeout, STX resync,
  hai frame liên tiếp và reset giữa frame.

### FPGA implementation

| Chỉ số | Formatter cũ | Formatter tuần tự |
|---|---:|---:|
| WNS | -14.430 ns | +2.972 ns |
| TNS | -458.154 ns | 0.000 ns |
| Timing 100 MHz | Fail | Pass |
| Slice LUTs | 3,725 | 485 |
| Slice Registers | 652 | 732 |
| DRC violations | 1 warning trước khi sửa XDC | 0 |

- Có script build tái lập `scripts/build_basys3.tcl`.
- Bitstream mới nằm tại `build/basys3/top_basys3_rdm6300.bit`.

### Host/WebUI

- Node.js/TypeScript đọc COM và parse protocol hiện tại.
- SQLite lưu lịch sử quét.
- REST API và Socket.IO realtime.
- React/Vite dashboard, raw UART log và mock scan.
- Phản hồi trực quan khi quét lại cùng thẻ.
- Xóa lịch sử qua WebUI.

## Hạng mục tiếp theo

1. Assertions, coverage, lint và CDC/RDC checks.
2. Đồng bộ thay đổi giao thức cần thiết sang workspace OpenLane riêng nếu tiếp tục nhánh ASIC.
