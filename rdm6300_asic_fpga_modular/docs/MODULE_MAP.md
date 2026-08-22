# Module map

Luồng dữ liệu đang hoạt động:

```text
RDM6300 -> UART RX -> RX FIFO -> Decoder -> Binary Packet Encoder
        -> TX FIFO -> UART TX -> Backend -> WebUI
```

| Module | Chức năng | Phạm vi |
|---|---|---|
| `sync_2ff` | Đồng bộ ngõ vào RFID bất đồng bộ | FPGA input boundary |
| `rx_fifo` | FIFO `valid/ready`, expose head liên tục cho đường UART RX đến Parser | FPGA |
| `tx_fifo` | FIFO `valid/ready`, expose head liên tục cho đường Parser đến UART TX | FPGA |
| `uart_rx` | Nhận UART 8N1, oversampling, majority vote, phát hiện framing/BREAK | FPGA |
| `uart_tx` | Phát UART 8N1 | FPGA |
| `rdm6300_frame_decoder` | STX/ETX, ASCII-hex, checksum, timeout, resynchronization | Parser |
| `card_packet_encoder` | Tạo gói 10 byte `A5 5A 01 05 TAG[4:0] CRC8` | Parser |
| `rfid_parser` | Nối trực tiếp Decoder với Packet Encoder | FPGA pipeline |
| `top_basys3_rdm6300` | Top hoàn chỉnh: reset, sync, RX, RX FIFO, Parser, TX FIFO và TX | FPGA top |

Không cần FIFO sự kiện trung gian vì một frame RDM6300 đầu vào dài 14 byte,
trong khi packet đầu ra dài 10 byte và hai UART dùng cùng baud rate. Packet hiện
tại hoàn tất trước frame đầu vào kế tiếp có thể hoàn thành. Burst test kiểm tra
trực tiếp điều kiện này và yêu cầu không mất sự kiện.

Duplicate timeout, Facility/Card Number extraction, decimal formatting, counters,
history và access policy thuộc Backend. WebUI chỉ trình bày dữ liệu và cấu hình.

`uart_fifo_core` và `rdm6300_access_core` đã bị bỏ; mọi instance và handshake
nằm trực tiếp trong FPGA top. `rdm6300_frame_decoder` được giữ vì đó là logic
giao thức thực sự mà Parser đang cần, không phải một lớp wrapper dư thừa.

Top không theo dõi trạng thái busy/done của UART TX. Mỗi transfer xảy ra khi
`valid && ready`; state xử lý bit UART, con trỏ FIFO và trạng thái frame chỉ tồn
tại cục bộ trong module chịu trách nhiệm thực hiện chức năng đó.
