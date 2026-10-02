// ============================================================================
// File: rtl/rdm6300_mmio.v
// Project: rdm6300-picorv32-rom-data
// Description: RDM6300 125kHz RFID Hardware Receiver, Pipeline Frame Decoder,
//              and PicoRV32 MMIO Slave Interface (Base: 0x1000_0000).
//
// Memory Map (Base: 0x1000_0000):
//   0x1000_0000: RFID Status Register (Bit 0: tag_ready, write to clear)
//   0x1000_0004: RFID Tag Word Hi    (8-bit version byte: tag_raw[39:32])
//   0x1000_0008: RFID Tag Word Lo    (32-bit serial number: tag_raw[31:0])
// ============================================================================

`timescale 1ns / 1ps

module rdm6300_mmio #(
    parameter CLK_FREQ_HZ         = 50_000_000,
    parameter UART_BAUD           = 9600,
    parameter FRAME_TIMEOUT_CYCLES = CLK_FREQ_HZ / 200
)(
    input  wire        clk,
    input  wire        rst_n,

    // Physical RDM6300 RX pin from external RFID antenna module (9600-8-N-1)
    input  wire        rdm_rx_i,

    // PicoRV32 Native Memory Bus Slave Interface (0x1000_0000)
    input  wire        valid,
    input  wire [3:0]  addr,      // cpu_mem_addr[3:0]
    input  wire [31:0] wdata,
    input  wire [3:0]  wstrb,
    output wire [31:0] rdata,
    output wire        ready,

    // Hardware Event / Status Indicators
    output wire        card_event_o,
    output wire [39:0] tag_raw_o,
    output wire        tag_ready_o
);

    // ------------------------------------------------------------------------
    // 1. Two-Stage Synchronizer for Asynchronous External RX Pin
    // ------------------------------------------------------------------------
    wire rdm_rx_sync;

    sync_2ff #(.RESET_VALUE(1'b1)) u_sync_rdm (
        .clk(clk),
        .rst_n(rst_n),
        .async_i(rdm_rx_i),
        .sync_o(rdm_rx_sync)
    );

    // ------------------------------------------------------------------------
    // 2. Hardware UART Byte Receiver (9600 Baud)
    // ------------------------------------------------------------------------
    wire       hw_rx_dv;
    wire [7:0] hw_rx_byte;

    uart_rx #(
        .CLKS_PER_BIT(CLK_FREQ_HZ / UART_BAUD)
    ) u_rdm_rx (
        .clk(clk),
        .rst_n(rst_n),
        .rx(rdm_rx_sync),
        .rx_dv(hw_rx_dv),
        .rx_byte(hw_rx_byte),
        .framing_error(),
        .break_detect()
    );

    // ------------------------------------------------------------------------
    // 3. Hardware Frame Decoder (14-Byte ASCII Frame Pipeline)
    // ------------------------------------------------------------------------
    wire        hw_card_valid;
    wire [39:0] hw_tag_raw;

    rdm6300_frame_decoder #(
        .FRAME_TIMEOUT_CYCLES(FRAME_TIMEOUT_CYCLES)
    ) u_rdm_decoder (
        .clk(clk),
        .rst_n(rst_n),
        .byte_valid(hw_rx_dv),
        .byte_data(hw_rx_byte),
        .byte_ready(),
        .card_valid(hw_card_valid),
        .tag_raw(hw_tag_raw),
        .checksum_error(),
        .frame_error(),
        .invalid_hex_error(),
        .frame_timeout_error()
    );

    // ------------------------------------------------------------------------
    // 4. Memory-Mapped Registers (0x1000_0000 - 0x1000_0008)
    // ------------------------------------------------------------------------
    reg        rfid_tag_ready;
    reg [7:0]  rfid_tag_hi;
    reg [31:0] rfid_tag_lo;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            rfid_tag_ready <= 1'b0;
            rfid_tag_hi    <= 8'd0;
            rfid_tag_lo    <= 32'd0;
        end else begin
            if (hw_card_valid) begin
                rfid_tag_ready <= 1'b1;
                rfid_tag_hi    <= hw_tag_raw[39:32];
                rfid_tag_lo    <= hw_tag_raw[31:0];
            end else if (valid && (|wstrb) && (addr[3:2] == 2'b00)) begin
                rfid_tag_ready <= 1'b0; // CPU write clears the ready flag
            end
        end
    end

    // Read Data Multiplexing & Ready Response
    assign ready = valid;
    assign rdata = (addr[3:2] == 2'b00) ? {31'd0, rfid_tag_ready} :
                   (addr[3:2] == 2'b01) ? {24'd0, rfid_tag_hi}     :
                   (addr[3:2] == 2'b10) ? rfid_tag_lo              : 32'd0;

    // Outputs
    assign card_event_o = hw_card_valid;
    assign tag_raw_o    = hw_tag_raw;
    assign tag_ready_o  = rfid_tag_ready;

endmodule
