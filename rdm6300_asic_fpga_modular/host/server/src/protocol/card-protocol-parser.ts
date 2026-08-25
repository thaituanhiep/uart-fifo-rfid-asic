import type { ParsedCard } from "../types.js";

const SOF_0 = 0xa5;
const SOF_1 = 0x5a;
const VERSION = 0x01;
const TAG_LENGTH = 0x05;
const PACKET_LENGTH = 10;

export type CardPacket = {
  tagRaw: Buffer;
  rawHex: string;
};

function crc8(data: Uint8Array): number {
  let crc = 0;
  for (const byte of data) {
    crc ^= byte;
    for (let bit = 0; bit < 8; bit += 1)
      crc = crc & 0x80 ? ((crc << 1) ^ 0x07) & 0xff : (crc << 1) & 0xff;
  }
  return crc;
}

// Resynchronizes on A5 5A and validates version, fixed payload length and CRC.
export class BinaryPacketFramer {
  private buffer = Buffer.alloc(0);

  push(chunk: Buffer): CardPacket[] {
    this.buffer = Buffer.concat([this.buffer, chunk]);
    const packets: CardPacket[] = [];

    while (this.buffer.length >= 2) {
      const sof = this.buffer.indexOf(Buffer.from([SOF_0, SOF_1]));
      if (sof < 0) {
        this.buffer = this.buffer.at(-1) === SOF_0
          ? this.buffer.subarray(this.buffer.length - 1)
          : Buffer.alloc(0);
        break;
      }
      if (sof > 0) this.buffer = this.buffer.subarray(sof);
      if (this.buffer.length < PACKET_LENGTH) break;

      const candidate = this.buffer.subarray(0, PACKET_LENGTH);
      const headerValid = candidate[2] === VERSION && candidate[3] === TAG_LENGTH;
      const crcValid = crc8(candidate.subarray(2, 9)) === candidate[9];
      if (!headerValid || !crcValid) {
        this.buffer = this.buffer.subarray(1);
        continue;
      }

      const tagRaw = Buffer.from(candidate.subarray(4, 9));
      packets.push({ tagRaw, rawHex: candidate.toString("hex").toUpperCase() });
      this.buffer = this.buffer.subarray(PACKET_LENGTH);
    }
    return packets;
  }

  reset(): void {
    this.buffer = Buffer.alloc(0);
  }
}

export function parseTagRaw(tagRaw: Buffer): ParsedCard | null {
  if (tagRaw.length !== TAG_LENGTH) return null;
  return {
    cardId: String(tagRaw.readUInt32BE(1)).padStart(10, "0"),
    facilityCode: tagRaw[2]!,
    cardNumber: tagRaw.readUInt16BE(3),
  };
}

// Retained only for the mock HTTP endpoint; physical serial uses binary packets.
const CARD_LINE = /^(\d{10}) (\d{3}),(\d{5})$/;
export function parseCardLine(rawLine: string): ParsedCard | null {
  const match = CARD_LINE.exec(rawLine.replace(/\r$/, ""));
  if (!match) return null;
  return { cardId: match[1]!, facilityCode: Number(match[2]), cardNumber: Number(match[3]) };
}
