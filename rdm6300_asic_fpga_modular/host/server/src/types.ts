export type ReaderState = {
  connected: boolean;
  connecting: boolean;
  port: string | null;
  baudRate: number;
  readerId: string;
  mode: "serial" | "mock" | "idle";
  error: string | null;
};

export type ParsedCard = {
  cardId: string;
  facilityCode: number;
  cardNumber: number;
};

export type CardScan = ParsedCard & {
  id: string;
  rawData: string;
  readerId: string;
  scannedAt: string;
  status: "valid" | "invalid";
  imagePath: string | null;
};

export type SerialPortInfo = {
  path: string;
  manufacturer?: string;
  serialNumber?: string;
  vendorId?: string;
  productId?: string;
};
