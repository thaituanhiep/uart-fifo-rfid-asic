# RFID Reader Monitor

Ứng dụng local thay thế PuTTY cho luồng `RDM6300 → Basys3 → USB-UART → PC`.

## Kiến trúc

```text
UART/COM → SerialReader → CardProtocolParser → ScanService
                                              ├─ SQLite
                                              ├─ REST API
                                              └─ Socket.IO → React WebUI
```

Phần host hoàn toàn độc lập và không thay đổi RTL. Parser tại `server/src/protocol/card-protocol-parser.ts` nhận đúng dòng FPGA hiện tại:

```text
ID10 FC3,CN5\n
0033752069 003,01029\n
```

## Chạy

Yêu cầu Node.js 24 và pnpm.

```bash
pnpm install
pnpm dev
```

Mở `http://localhost:5173`. WebUI tự kết nối server tại cổng 3001. Chọn COM của Basys3 rồi nhấn **Kết nối Basys3**. Không mở PuTTY cùng lúc vì cổng COM chỉ nên do một ứng dụng sử dụng.

Nếu chưa cắm board, dùng **Tạo lượt quét mô phỏng** để kiểm tra toàn bộ SQLite, API, realtime và giao diện.

## Scripts

```bash
pnpm dev
pnpm build
pnpm typecheck
pnpm start
```

Sau `pnpm build`, lệnh `pnpm start` phục vụ cả API và WebUI tại `http://localhost:3001`.

## API

- `GET /api/health`
- `GET /api/readers`
- `GET /api/readers/ports`
- `POST /api/readers/connect` với `{ "port": "COM5", "baudRate": 9600 }`
- `POST /api/readers/disconnect`
- `GET /api/scans?limit=100`
- `GET /api/scans/:id`
- `DELETE /api/scans` (xóa toàn bộ lịch sử)
- `POST /api/mock/scan`

## Dữ liệu

SQLite được tạo tại `server/data/rfid.db` khi chạy server. Lịch sử vẫn còn sau khi khởi động lại. Trường `imagePath` đã được dự trù cho camera nhưng camera chưa được triển khai trong Phase 1.

## Giới hạn hiện tại

- FPGA chỉ gửi các lượt quét hợp lệ đã qua duplicate filter; WebUI chưa thể biết checksum/frame/duplicate error từ RTL.
- Một server đang quản lý một kết nối serial vật lý.
- Camera, ESP32/Wi-Fi reader, tài khoản và cloud nằm ngoài Phase 1.
