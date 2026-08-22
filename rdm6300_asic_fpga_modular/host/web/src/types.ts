export type ReaderState = {
  connected: boolean;
  connecting: boolean;
  port: string | null;
  baudRate: number;
  readerId: string;
  mode: "serial" | "mock" | "idle";
  error: string | null;
};
export type PortInfo = {
  path: string;
  manufacturer?: string;
  serialNumber?: string;
  vendorId?: string;
  productId?: string;
};
export type CardScan = {
  id: string;
  cardId: string;
  facilityCode: number;
  cardNumber: number;
  rawData: string;
  readerId: string;
  scannedAt: string;
  status: "valid" | "invalid";
  imagePath: string | null;
};
