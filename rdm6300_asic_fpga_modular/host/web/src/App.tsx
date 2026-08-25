import { useEffect, useMemo, useState } from "react";
import { io } from "socket.io-client";
import type { CardScan, PortInfo, ReaderState } from "./types";

const initialReader: ReaderState = {
  connected: false,
  connecting: false,
  port: null,
  baudRate: 9600,
  readerId: "reader-01",
  mode: "idle",
  error: null,
};
const api = async <T,>(path: string, options?: RequestInit): Promise<T> => {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error?.message ?? "Request failed");
  return data;
};
const time = (iso: string) =>
  new Intl.DateTimeFormat("vi-VN", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    day: "2-digit",
    month: "2-digit",
  }).format(new Date(iso));

export function App() {
  const [reader, setReader] = useState(initialReader);
  const [ports, setPorts] = useState<PortInfo[]>([]);
  const [selectedPort, setSelectedPort] = useState("");
  const [scans, setScans] = useState<CardScan[]>([]);
  const [raw, setRaw] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const refreshPorts = () =>
    api<PortInfo[]>("/api/readers/ports")
      .then((p) => {
        setPorts(p);
        if (!selectedPort && p[0]) setSelectedPort(p[0].path);
      })
      .catch((e: Error) => setError(e.message));
  useEffect(() => {
    Promise.all([
      api<ReaderState>("/api/readers"),
      api<CardScan[]>("/api/scans"),
      api<PortInfo[]>("/api/readers/ports"),
    ])
      .then(([r, s, p]) => {
        setReader(r);
        setScans(s);
        setPorts(p);
        setSelectedPort(r.port ?? p[0]?.path ?? "");
      })
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
    const socket = io();
    socket.on("reader:state", setReader);
    socket.on("card:scanned", (scan: CardScan) =>
      setScans((items) => [scan, ...items].slice(0, 100)),
    );
    socket.on("scans:cleared", () => setScans([]));
    socket.on("serial:raw", ({ data, at }: { data: string; at: string }) =>
      setRaw((lines) =>
        [`${time(at)}  ${JSON.stringify(data)}`, ...lines].slice(0, 80),
      ),
    );
    socket.on("protocol:error", ({ message }: { message: string }) =>
      setError(message),
    );
    return () => {
      socket.disconnect();
    };
  }, []);

  const latest = scans[0];
  const isRepeatedScan = Boolean(latest && scans[1]?.cardId === latest.cardId);
  const latestCardCount = latest
    ? scans.filter((scan) => scan.cardId === latest.cardId).length
    : 0;
  const uniqueCards = useMemo(
    () => new Set(scans.map((scan) => scan.cardId)).size,
    [scans],
  );
  const connect = async () => {
    setError(null);
    try {
      if (reader.connected)
        await api("/api/readers/disconnect", { method: "POST" });
      else if (selectedPort)
        await api("/api/readers/connect", {
          method: "POST",
          body: JSON.stringify({ port: selectedPort, baudRate: 9600 }),
        });
    } catch (e) {
      setError(e instanceof Error ? e.message : "Không thể kết nối");
    }
  };
  const mockScan = () =>
    api<CardScan>("/api/mock/scan", { method: "POST", body: "{}" }).catch(
      (e: Error) => setError(e.message),
    );
  const clearHistory = async () => {
    if (
      !window.confirm(
        "Xóa toàn bộ lịch sử quẹt thẻ? Thao tác này không thể hoàn tác.",
      )
    )
      return;
    setError(null);
    try {
      await api<{ deleted: number }>("/api/scans", { method: "DELETE" });
      setScans([]);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Không thể xóa lịch sử");
    }
  };
  return (
    <main className="shell">
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark">
            <span />
          </div>
          <div>
            <p>HARDWARE LAB / BASYS3</p>
            <h1>RFID Reader Monitor</h1>
          </div>
        </div>
        <div className={`status-pill ${reader.connected ? "online" : ""}`}>
          <i />
          {reader.connected
            ? `${reader.port} đang kết nối`
            : "Chưa kết nối thiết bị"}
        </div>
      </header>

      {error && (
        <div className="alert">
          <span>!</span>
          <p>{error}</p>
          <button onClick={() => setError(null)}>Đóng</button>
        </div>
      )}

      <section className="hero-grid">
        <article className="panel reader-panel">
          <div className="panel-head">
            <div>
              <small>READER CONTROL</small>
              <h2>Kết nối phần cứng</h2>
            </div>
            <span className="port-count">{ports.length} PORT</span>
          </div>
          <label>Cổng nối tiếp</label>
          <div className="select-row">
            <select
              value={selectedPort}
              disabled={reader.connected}
              onChange={(e) => setSelectedPort(e.target.value)}
            >
              <option value="">Không tìm thấy cổng COM</option>
              {ports.map((p) => (
                <option key={p.path} value={p.path}>
                  {p.path}
                  {p.manufacturer ? ` — ${p.manufacturer}` : ""}
                </option>
              ))}
            </select>
            <button
              className="icon-button"
              title="Quét lại cổng"
              onClick={refreshPorts}
            >
              ↻
            </button>
          </div>
          <div className="spec-row">
            <span>
              <b>9600</b> BAUD
            </span>
            <span>
              <b>8N1</b> FORMAT
            </span>
            <span>
              <b>{reader.readerId}</b> READER
            </span>
          </div>
          <button
            className={`primary ${reader.connected ? "disconnect" : ""}`}
            disabled={reader.connecting || (!reader.connected && !selectedPort)}
            onClick={connect}
          >
            {reader.connecting
              ? "Đang kết nối…"
              : reader.connected
                ? "Ngắt kết nối"
                : "Kết nối Basys3"}
          </button>
          <button className="ghost" onClick={mockScan}>
            Tạo lượt quét mô phỏng
          </button>
        </article>

        <article
          key={latest?.id ?? "waiting"}
          className={`panel latest-panel ${latest ? "has-scan scan-arrived" : ""} ${isRepeatedScan ? "repeated" : ""}`}
        >
          <div className="panel-head">
            <div>
              <small>LATEST SCAN</small>
              <h2>Thẻ vừa nhận</h2>
            </div>
            {latest && (
              <span
                className={`valid-badge ${isRepeatedScan ? "repeat-badge" : ""}`}
              >
                {isRepeatedScan ? "↻ QUÉT LẠI · VALID" : "✓ THẺ MỚI · VALID"}
              </span>
            )}
          </div>
          {latest ? (
            <>
              <div className="scan-confirm">
                <i />
                {isRepeatedScan
                  ? "Đã ghi nhận lượt quét tiếp theo của cùng thẻ"
                  : "Đã ghi nhận một thẻ khác"}
                <b>Lượt #{latestCardCount}</b>
              </div>
              <div className="uid-label">CARD ID</div>
              <div className="uid">{latest.cardId}</div>
              <div className="scan-details">
                <div>
                  <span>Facility code</span>
                  <b>{String(latest.facilityCode).padStart(3, "0")}</b>
                </div>
                <div>
                  <span>Card number</span>
                  <b>{String(latest.cardNumber).padStart(5, "0")}</b>
                </div>
                <div>
                  <span>Nhận lúc</span>
                  <b>{time(latest.scannedAt)}</b>
                </div>
              </div>
            </>
          ) : (
            <div className="empty-latest">
              <div className="radio-waves">
                <i />
                <i />
                <i />
              </div>
              <p>Đang chờ tín hiệu thẻ</p>
              <span>Quẹt thẻ trên đầu đọc RDM6300</span>
            </div>
          )}
        </article>
      </section>

      <section className="stats">
        <div>
          <span>TỔNG LƯỢT QUÉT</span>
          <b>{scans.length}</b>
        </div>
        <div>
          <span>THẺ KHÁC NHAU</span>
          <b>{uniqueCards}</b>
        </div>
        <div>
          <span>TRẠNG THÁI SERVER</span>
          <b className="server-ok">● ONLINE</b>
        </div>
      </section>

      <section className="lower-grid">
        <article className="panel history">
          <div className="panel-head">
            <div>
              <small>SCAN LOG</small>
              <h2>Lịch sử quẹt thẻ</h2>
            </div>
            <div className="history-actions">
              <span className="muted">Lưu cục bộ bằng SQLite</span>
              <button
                className="clear-history"
                disabled={scans.length === 0}
                onClick={clearHistory}
              >
                Xóa lịch sử
              </button>
            </div>
          </div>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Thời gian</th>
                  <th>Card ID</th>
                  <th>Facility</th>
                  <th>Card No.</th>
                  <th>Trạng thái</th>
                </tr>
              </thead>
              <tbody>
                {scans.map((scan) => (
                  <tr key={scan.id}>
                    <td>{time(scan.scannedAt)}</td>
                    <td className="mono strong">{scan.cardId}</td>
                    <td className="mono">
                      {String(scan.facilityCode).padStart(3, "0")}
                    </td>
                    <td className="mono">
                      {String(scan.cardNumber).padStart(5, "0")}
                    </td>
                    <td>
                      <span className="table-status">VALID</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {!loading && scans.length === 0 && (
              <div className="empty-table">
                Chưa có lượt quét nào được ghi nhận.
              </div>
            )}
          </div>
        </article>
        <article className="panel terminal">
          <div className="panel-head">
            <div>
              <small>UART DEBUG</small>
              <h2>Dữ liệu thô</h2>
            </div>
            <button onClick={() => setRaw([])}>Xóa</button>
          </div>
          <div className="terminal-body">
            {raw.length ? (
              raw.map((line, i) => (
                <p key={i}>
                  <span>›</span>
                  {line}
                </p>
              ))
            ) : (
              <div className="terminal-empty">
                <span>_</span> Chờ dữ liệu UART...
              </div>
            )}
          </div>
          <footer>
            <i /> LIVE · LF DELIMITED
          </footer>
        </article>
      </section>
      <footer className="page-footer">
        <span>RDM6300 ACCESS CORE</span>
        <span>FPGA → UART → LOCAL SERVER</span>
        <span>PHASE 1</span>
      </footer>
    </main>
  );
}
