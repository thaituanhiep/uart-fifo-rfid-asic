import "dotenv/config";
import { existsSync } from "node:fs";
import { resolve } from "node:path";
import cors from "cors";
import express from "express";
import { createServer } from "node:http";
import { Server } from "socket.io";
import { z } from "zod";
import { ScanRepository } from "./database/scan-repository.js";
import { ScanService } from "./scans/scan-service.js";
import { SerialReader } from "./serial/serial-reader.js";

const port = Number(process.env.SERVER_PORT ?? 3001);
const baudRate = Number(process.env.SERIAL_BAUD_RATE ?? 9600);
const readerId = process.env.DEFAULT_READER_ID ?? "reader-01";
const duplicateTimeoutMs = Number(process.env.DUPLICATE_TIMEOUT_MS ?? 1_000);
const dbPath = resolve(
  process.cwd(),
  process.env.DATABASE_PATH ?? "./data/rfid.db",
);
const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, { cors: { origin: true } });
const repository = new ScanRepository(dbPath);
const reader = new SerialReader(readerId, baudRate);
const scans = new ScanService(repository, io, readerId, duplicateTimeoutMs);

app.use(cors());
app.use(express.json());
reader.on("packet", (packet) => scans.processPacket(packet));
reader.on("raw", (data: string) =>
  io.emit("serial:raw", { data, at: new Date().toISOString() }),
);
reader.on("state", (state) => io.emit("reader:state", state));

app.get("/api/health", (_req, res) =>
  res.json({ ok: true, time: new Date().toISOString() }),
);
app.get("/api/readers", (_req, res) => res.json(reader.getState()));
app.get("/api/readers/ports", async (_req, res, next) => {
  try {
    res.json(await SerialReader.listPorts());
  } catch (error) {
    next(error);
  }
});
app.post("/api/readers/connect", async (req, res, next) => {
  try {
    const body = z
      .object({
        port: z.string().min(1),
        baudRate: z.number().int().positive().optional(),
      })
      .parse(req.body);
    await reader.connect(body.port, body.baudRate);
    res.json(reader.getState());
  } catch (error) {
    next(error);
  }
});
app.post("/api/readers/disconnect", async (_req, res, next) => {
  try {
    await reader.disconnect();
    res.json(reader.getState());
  } catch (error) {
    next(error);
  }
});
app.get("/api/scans", (req, res) =>
  res.json(repository.list(Number(req.query.limit ?? 100))),
);
app.get("/api/scans/:id", (req, res) => {
  const scan = repository.get(req.params.id);
  if (!scan)
    return res.status(404).json({ error: { message: "Scan not found" } });
  res.json(scan);
});
app.delete("/api/scans", (_req, res) => {
  const deleted = repository.clear();
  io.emit("scans:cleared", { deleted, clearedAt: new Date().toISOString() });
  res.json({ deleted });
});
app.post("/api/mock/scan", (req, res, next) => {
  try {
    const body = z.object({ line: z.string().optional() }).parse(req.body);
    const generated = `${String(Math.floor(Math.random() * 1e10)).padStart(10, "0")} 003,${String(Math.floor(Math.random() * 65536)).padStart(5, "0")}`;
    const raw = body.line ?? generated;
    io.emit("serial:raw", { data: `${raw}\n`, at: new Date().toISOString() });
    const scan = scans.processLine(raw);
    if (!scan)
      return res.status(422).json({ error: { message: "Invalid mock frame" } });
    res.status(201).json(scan);
  } catch (error) {
    next(error);
  }
});

// A production build is served by the same local process; Vite handles this in development.
const webDist = resolve(process.cwd(), "../web/dist");
if (existsSync(webDist)) {
  app.use(express.static(webDist));
  app.use((req, res, next) => {
    if (req.method === "GET" && !req.path.startsWith("/api/"))
      return res.sendFile(resolve(webDist, "index.html"));
    next();
  });
}

app.use(
  (
    error: unknown,
    _req: express.Request,
    res: express.Response,
    _next: express.NextFunction,
  ) => {
    const message =
      error instanceof Error ? error.message : "Unexpected server error";
    res
      .status(error instanceof z.ZodError ? 400 : 500)
      .json({ error: { message } });
  },
);

io.on("connection", (socket) => socket.emit("reader:state", reader.getState()));
httpServer.listen(port, () =>
  console.log(`RFID server listening on http://localhost:${port}`),
);

async function shutdown(): Promise<void> {
  await reader.disconnect().catch(() => undefined);
  repository.close();
  io.close();
  httpServer.close(() => process.exit(0));
}
process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);
