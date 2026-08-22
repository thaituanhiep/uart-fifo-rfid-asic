import { mkdirSync } from "node:fs";
import { dirname } from "node:path";
import { DatabaseSync } from "node:sqlite";
import type { CardScan } from "../types.js";

type ScanRow = {
  id: string;
  card_id: string;
  facility_code: number;
  card_number: number;
  raw_data: string;
  reader_id: string;
  scanned_at: string;
  status: "valid" | "invalid";
  image_path: string | null;
};

export class ScanRepository {
  private readonly db: DatabaseSync;

  constructor(path: string) {
    mkdirSync(dirname(path), { recursive: true });
    this.db = new DatabaseSync(path);
    this.db.exec(`
      PRAGMA journal_mode = WAL;
      CREATE TABLE IF NOT EXISTS scans (
        id TEXT PRIMARY KEY,
        card_id TEXT NOT NULL,
        facility_code INTEGER NOT NULL,
        card_number INTEGER NOT NULL,
        raw_data TEXT NOT NULL,
        reader_id TEXT NOT NULL,
        scanned_at TEXT NOT NULL,
        status TEXT NOT NULL CHECK(status IN ('valid', 'invalid')),
        image_path TEXT
      );
      CREATE INDEX IF NOT EXISTS idx_scans_scanned_at ON scans(scanned_at DESC);
      PRAGMA optimize;
    `);
  }

  insert(scan: CardScan): void {
    this.db
      .prepare(
        `INSERT INTO scans
      (id, card_id, facility_code, card_number, raw_data, reader_id, scanned_at, status, image_path)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`,
      )
      .run(
        scan.id,
        scan.cardId,
        scan.facilityCode,
        scan.cardNumber,
        scan.rawData,
        scan.readerId,
        scan.scannedAt,
        scan.status,
        scan.imagePath,
      );
  }

  list(limit = 100): CardScan[] {
    const rows = this.db
      .prepare("SELECT * FROM scans ORDER BY scanned_at DESC LIMIT ?")
      .all(Math.min(Math.max(limit, 1), 500)) as unknown as ScanRow[];
    return rows.map(mapRow);
  }

  get(id: string): CardScan | null {
    const row = this.db.prepare("SELECT * FROM scans WHERE id = ?").get(id) as
      | ScanRow
      | undefined;
    return row ? mapRow(row) : null;
  }

  clear(): number {
    const result = this.db.prepare("DELETE FROM scans").run();
    return Number(result.changes);
  }

  close(): void {
    this.db.close();
  }
}

function mapRow(row: ScanRow): CardScan {
  return {
    id: row.id,
    cardId: row.card_id,
    facilityCode: row.facility_code,
    cardNumber: row.card_number,
    rawData: row.raw_data,
    readerId: row.reader_id,
    scannedAt: row.scanned_at,
    status: row.status,
    imagePath: row.image_path,
  };
}
