import { EventEmitter } from "node:events";
import { SerialPort } from "serialport";
import { BinaryPacketFramer } from "../protocol/card-protocol-parser.js";
import type { ReaderState, SerialPortInfo } from "../types.js";

export class SerialReader extends EventEmitter {
  private port: SerialPort | null = null;
  private readonly framer = new BinaryPacketFramer();
  private state: ReaderState;

  constructor(readerId: string, baudRate: number) {
    super();
    this.state = {
      connected: false,
      connecting: false,
      port: null,
      baudRate,
      readerId,
      mode: "idle",
      error: null,
    };
  }

  static async listPorts(): Promise<SerialPortInfo[]> {
    return (await SerialPort.list()).map(
      ({ path, manufacturer, serialNumber, vendorId, productId }) => ({
        path,
        ...(manufacturer && { manufacturer }),
        ...(serialNumber && { serialNumber }),
        ...(vendorId && { vendorId }),
        ...(productId && { productId }),
      }),
    );
  }

  getState(): ReaderState {
    return { ...this.state };
  }

  async connect(path: string, baudRate = this.state.baudRate): Promise<void> {
    if (this.port?.isOpen) await this.disconnect();
    this.setState({
      connecting: true,
      port: path,
      baudRate,
      mode: "serial",
      error: null,
    });
    const port = new SerialPort({ path, baudRate, autoOpen: false });
    this.port = port;
    port.on("data", (chunk: Buffer) => {
      this.emit("raw", `${chunk.toString("hex").toUpperCase()} `);
      for (const packet of this.framer.push(chunk)) {
        this.emit("packet", packet);
      }
    });
    port.on("error", (error) => this.setState({ error: error.message }));
    port.on("close", () =>
      this.setState({ connected: false, connecting: false, mode: "idle" }),
    );
    try {
      await new Promise<void>((resolve, reject) => {
        const timer = setTimeout(
          () => reject(new Error(`Timed out opening ${path}`)),
          5_000,
        );
        port.open((error) => {
          clearTimeout(timer);
          if (error) reject(error);
          else resolve();
        });
      });
      this.setState({ connected: true, connecting: false });
    } catch (error) {
      const message =
        error instanceof Error ? error.message : `Unable to open ${path}`;
      if (this.port === port) this.port = null;
      this.setState({
        connected: false,
        connecting: false,
        mode: "idle",
        error: message,
      });
      throw error;
    }
  }

  async disconnect(): Promise<void> {
    const port = this.port;
    this.port = null;
    this.framer.reset();
    if (port?.isOpen)
      await new Promise<void>((resolve) => port.close(() => resolve()));
    this.setState({
      connected: false,
      connecting: false,
      port: null,
      mode: "idle",
      error: null,
    });
  }

  private setState(patch: Partial<ReaderState>): void {
    this.state = { ...this.state, ...patch };
    this.emit("state", this.getState());
  }
}
