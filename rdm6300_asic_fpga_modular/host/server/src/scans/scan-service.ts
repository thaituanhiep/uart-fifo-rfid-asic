import { randomUUID } from "node:crypto";
import type { Server } from "socket.io";
import type { ScanRepository } from "../database/scan-repository.js";
import { parseCardLine, parseTagRaw, type CardPacket } from "../protocol/card-protocol-parser.js";
import type { CardScan, ParsedCard } from "../types.js";

export class ScanService {
  private lastTagHex: string | null = null;
  private lastSeenAt = 0;

  constructor(
    private readonly repository: ScanRepository,
    private readonly io: Server,
    private readonly readerId: string,
    private readonly duplicateTimeoutMs = 1_000,
  ) {}

  processPacket(packet: CardPacket): CardScan | null {
    const parsed = parseTagRaw(packet.tagRaw);
    if (!parsed) return null;

    const tagHex = packet.tagRaw.toString("hex");
    const now = Date.now();
    const duplicate = tagHex === this.lastTagHex && now - this.lastSeenAt < this.duplicateTimeoutMs;
    this.lastTagHex = tagHex;
    this.lastSeenAt = now;
    if (duplicate) {
      this.io.emit("card:duplicate", { tagRaw: tagHex.toUpperCase(), at: new Date(now).toISOString() });
      return null;
    }
    return this.accept(parsed, packet.rawHex);
  }

  processLine(rawLine: string): CardScan | null {
    const parsed = parseCardLine(rawLine);
    if (!parsed) {
      this.io.emit("protocol:error", {
        rawData: rawLine,
        message: "Invalid RFID frame",
      });
      return null;
    }
    return this.accept(parsed, rawLine);
  }

  private accept(parsed: ParsedCard, rawData: string): CardScan {
    const scan: CardScan = {
      id: randomUUID(),
      ...parsed,
      rawData,
      readerId: this.readerId,
      scannedAt: new Date().toISOString(),
      status: "valid",
      imagePath: null,
    };
    this.repository.insert(scan);
    this.io.emit("card:scanned", scan);
    return scan;
  }
}
