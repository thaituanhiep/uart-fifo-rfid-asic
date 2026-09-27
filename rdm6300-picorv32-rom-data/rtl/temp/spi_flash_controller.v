// ============================================================================
// File: spi_flash_controller.v
// Project: rdm6300-picorv32-rom-data
// Description: SPI Flash Memory Controller with RFID Tag Auto-Storage & MMIO
// Target: Spansion S25FL032P / Winbond W25Qxx on Digilent Basys 3 & ASIC
// ============================================================================

`timescale 1ns / 1ps

module spi_flash_controller #(
    parameter CLK_FREQ_HZ   = 100_000_000,
    parameter SPI_FREQ_HZ   = 25_000_000,
    parameter FLASH_BASE_ADDR = 24'h30_0000 // Offset 3MB (safe from FPGA bitstream)
)(
    input  wire        clk,
    input  wire        rst_n,

    // ------------------------------------------------------------------------
    // Memory Mapped Interface (PicoRV32 or System Bus)
    // ------------------------------------------------------------------------
    input  wire        bus_valid,
    input  wire [4:0]  bus_addr,     // Register offset (0x00 to 0x1C)
    input  wire [31:0] bus_wdata,
    input  wire [3:0]  bus_wstrb,
    output reg  [31:0] bus_rdata,
    output reg         bus_ready,

    // ------------------------------------------------------------------------
    // Autonomous RFID Tag Auto-Store Interface
    // ------------------------------------------------------------------------
    input  wire        auto_save_enable,  // Enable auto-writing tags to flash
    input  wire        card_valid,        // 1-cycle pulse from rdm6300_frame_decoder
    input  wire [39:0] tag_raw,           // 40-bit RFID tag UID
    input  wire [7:0]  tag_checksum,      // 8-bit frame checksum

    // ------------------------------------------------------------------------
    // Physical SPI Flash Interface (Mode 0: CPOL=0, CPHA=0)
    // ------------------------------------------------------------------------
    output reg         flash_csn,         // Active-low Chip Select
    output reg         flash_sck,         // SPI Clock (max 25 MHz)
    output reg         flash_mosi,        // Master Out Slave In
    input  wire        flash_miso,        // Master In Slave Out

    // ------------------------------------------------------------------------
    // Status & Diagnostic Indicators
    // ------------------------------------------------------------------------
    output wire        flash_busy,
    output reg         flash_write_done,
    output reg         flash_error,
    output wire [15:0] saved_records_count
);

    // ------------------------------------------------------------------------
    // SPI Flash Commands
    // ------------------------------------------------------------------------
    localparam CMD_WREN         = 8'h06; // Write Enable
    localparam CMD_WRDI         = 8'h04; // Write Disable
    localparam CMD_RDSR         = 8'h05; // Read Status Register
    localparam CMD_READ         = 8'h03; // Read Data (up to 33MHz/50MHz)
    localparam CMD_PAGE_PROG    = 8'h02; // Page Program (1 - 256 bytes)
    localparam CMD_SECTOR_ERASE = 8'hD8; // 64KB Sector Erase (Universal for Spansion S25FL032P, Winbond, Micron)
    localparam CMD_RDID         = 8'h9F; // Read JEDEC ID

    // Clock Divider: 100MHz / (2 * 2) = 25MHz
    localparam CLK_DIV = (CLK_FREQ_HZ / (2 * SPI_FREQ_HZ)) > 0 ? (CLK_FREQ_HZ / (2 * SPI_FREQ_HZ)) : 1;

    // ------------------------------------------------------------------------
    // Internal Registers
    // ------------------------------------------------------------------------
    reg [2:0]  reg_cmd_op;        // 0:READ, 1:WRITE, 2:SECTOR_ERASE, 3:RDID, 4:RDSR
    reg        reg_cmd_trigger;
    reg        reg_auto_enable;
    reg [23:0] reg_flash_addr;
    reg [31:0] reg_wdata;
    reg [31:0] reg_rdata;
    reg [15:0] record_counter;
    reg [31:0] timestamp_counter;

    assign saved_records_count = record_counter;

    // Timestamp generator (ticks every microsecond based on CLK_FREQ_HZ)
    localparam US_CYCLES = (CLK_FREQ_HZ / 1_000_000) > 0 ? (CLK_FREQ_HZ / 1_000_000) - 1 : 0;
    reg [6:0] us_timer;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            us_timer          <= 7'd0;
            timestamp_counter <= 32'd0;
        end else begin
            if (us_timer >= US_CYCLES[6:0]) begin
                us_timer          <= 7'd0;
                timestamp_counter <= timestamp_counter + 1'b1;
            end else begin
                us_timer <= us_timer + 1'b1;
            end
        end
    end

    // ------------------------------------------------------------------------
    // FSM States
    // ------------------------------------------------------------------------
    localparam S_IDLE          = 5'd0;
    localparam S_WREN_CS_LOW   = 5'd1;
    localparam S_WREN_SEND     = 5'd2;
    localparam S_WREN_CS_HIGH  = 5'd3;
    localparam S_CMD_CS_LOW    = 5'd4;
    localparam S_CMD_SEND      = 5'd5;
    localparam S_ADDR_SEND     = 5'd6;
    localparam S_DATA_TX       = 5'd7;
    localparam S_DATA_RX       = 5'd8;
    localparam S_CS_HIGH_DELAY = 5'd9;
    localparam S_POLL_RDSR_CS  = 5'd10;
    localparam S_POLL_RDSR_CMD = 5'd11;
    localparam S_POLL_RDSR_RX  = 5'd12;
    localparam S_POLL_CHECK    = 5'd13;
    localparam S_DONE          = 5'd14;

    reg [4:0]  state;
    reg [4:0]  next_state_after_wren;
    reg [7:0]  spi_tx_byte;
    reg [7:0]  spi_rx_byte;
    reg [2:0]  spi_bit_cnt;
    reg [7:0]  clk_div_cnt;
    reg [4:0]  byte_idx;
    reg [4:0]  total_bytes;
    reg [7:0]  flash_status_reg;
    reg [127:0] tag_record_buffer; // 16-byte record

    assign flash_busy = (state != S_IDLE);

    // ------------------------------------------------------------------------
    // MMIO Register Interface
    // ------------------------------------------------------------------------
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            bus_ready       <= 1'b0;
            bus_rdata       <= 32'd0;
            reg_cmd_op      <= 3'd0;
            reg_cmd_trigger <= 1'b0;
            reg_auto_enable <= 1'b1; // Default: auto-save enabled
            reg_flash_addr  <= FLASH_BASE_ADDR;
            reg_wdata       <= 32'd0;
        end else begin
            bus_ready <= 1'b0;
            if (reg_cmd_trigger && state != S_IDLE) begin
                reg_cmd_trigger <= 1'b0;
            end

            if (bus_valid && !bus_ready) begin
                bus_ready <= 1'b1;
                // Read Registers
                case (bus_addr[4:2])
                    3'b000: bus_rdata <= {24'd0, reg_auto_enable, 4'd0, reg_cmd_op};               // 0x00 CTRL
                    3'b001: bus_rdata <= {12'd0, state, flash_status_reg[0], flash_error, flash_write_done, flash_busy}; // 0x04 STATUS
                    3'b010: bus_rdata <= {8'd0, reg_flash_addr};                                    // 0x08 ADDR
                    3'b011: bus_rdata <= reg_wdata;                                                // 0x0C WDATA
                    3'b100: bus_rdata <= reg_rdata;                                                // 0x10 RDATA
                    3'b101: bus_rdata <= {16'd0, record_counter};                                  // 0x14 RECORD_COUNT
                    3'b110: bus_rdata <= timestamp_counter;                                         // 0x18 TIMESTAMP
                    default: bus_rdata <= 32'd0;
                endcase

                // Write Registers
                if (|bus_wstrb) begin
                    case (bus_addr[4:2])
                        3'b000: begin // 0x00 CTRL
                            if (bus_wstrb[0]) begin
                                reg_cmd_trigger <= bus_wdata[0];
                                reg_cmd_op      <= bus_wdata[3:1];
                            end
                            if (bus_wstrb[1]) begin
                                reg_auto_enable <= bus_wdata[7];
                            end
                        end
                        3'b010: begin // 0x08 ADDR
                            if (bus_wstrb[0]) reg_flash_addr[7:0]   <= bus_wdata[7:0];
                            if (bus_wstrb[1]) reg_flash_addr[15:8]  <= bus_wdata[15:8];
                            if (bus_wstrb[2]) reg_flash_addr[23:16] <= bus_wdata[23:16];
                        end
                        3'b011: begin // 0x0C WDATA
                            if (bus_wstrb[0]) reg_wdata[7:0]   <= bus_wdata[7:0];
                            if (bus_wstrb[1]) reg_wdata[15:8]  <= bus_wdata[15:8];
                            if (bus_wstrb[2]) reg_wdata[23:16] <= bus_wdata[23:16];
                            if (bus_wstrb[3]) reg_wdata[31:24] <= bus_wdata[31:24];
                        end
                    endcase
                end
            end
        end
    end

    // ------------------------------------------------------------------------
    // SPI Master & Auto-Save Controller FSM
    // ------------------------------------------------------------------------
    reg [23:0] cur_addr;
    reg [7:0]  cur_cmd;
    reg        auto_mode_active;
    reg [7:0]  delay_timer;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state                 <= S_IDLE;
            next_state_after_wren <= S_IDLE;
            flash_csn             <= 1'b1;
            flash_sck             <= 1'b0;
            flash_mosi            <= 1'b0;
            flash_write_done      <= 1'b0;
            flash_error           <= 1'b0;
            record_counter        <= 16'd0;
            reg_rdata             <= 32'd0;
            flash_status_reg      <= 8'd0;
            spi_bit_cnt           <= 3'd0;
            clk_div_cnt           <= 8'd0;
            byte_idx              <= 5'd0;
            total_bytes           <= 5'd0;
            auto_mode_active      <= 1'b0;
            cur_addr              <= FLASH_BASE_ADDR;
            cur_cmd               <= 8'd0;
            delay_timer           <= 8'd0;
            tag_record_buffer     <= 128'd0;
        end else begin
            flash_write_done <= 1'b0;

            case (state)
                // ------------------------------------------------------------
                // S_IDLE: Check for Software Trigger or RFID Hardware Auto-Trigger
                // ------------------------------------------------------------
                S_IDLE: begin
                    flash_csn   <= 1'b1;
                    flash_sck   <= 1'b0;
                    flash_mosi  <= 1'b0;
                    clk_div_cnt <= 8'd0;
                    spi_bit_cnt <= 3'd0;
                    byte_idx    <= 5'd0;

                    // 1. Hardware Auto-Trigger upon valid RFID card
                    if ((auto_save_enable || reg_auto_enable) && card_valid) begin
                        auto_mode_active <= 1'b1;
                        // Format 16-byte record:
                        // [15:14] Preamble (0xA5, 0x5A)
                        // [13:12] Record Counter [15:0]
                        // [11:8]  Timestamp [31:0]
                        // [7:3]   Tag Raw [39:0] (5 bytes)
                        // [2]     Checksum [7:0]
                        // [1:0]   Postamble (0x55, 0xAA)
                        tag_record_buffer <= {
                            8'hA5, 8'h5A,
                            record_counter[15:8], record_counter[7:0],
                            timestamp_counter[31:24], timestamp_counter[23:16], timestamp_counter[15:8], timestamp_counter[7:0],
                            tag_raw[39:32], tag_raw[31:24], tag_raw[23:16], tag_raw[15:8], tag_raw[7:0],
                            tag_checksum,
                            8'h55, 8'hAA
                        };
                        cur_addr              <= FLASH_BASE_ADDR + {8'd0, record_counter[7:0], 4'b0000}; // 16 bytes/record
                        cur_cmd               <= CMD_PAGE_PROG;
                        total_bytes           <= 5'd16;
                        next_state_after_wren <= S_CMD_CS_LOW;
                        state                 <= S_WREN_CS_LOW;
                    end
                    // 2. Software MMIO Trigger
                    else if (reg_cmd_trigger) begin
                        auto_mode_active <= 1'b0;
                        cur_addr         <= reg_flash_addr;
                        case (reg_cmd_op)
                            3'b000: begin // READ 32-bit word
                                cur_cmd     <= CMD_READ;
                                total_bytes <= 5'd4;
                                state       <= S_CMD_CS_LOW;
                            end
                            3'b001: begin // WRITE 32-bit word
                                cur_cmd               <= CMD_PAGE_PROG;
                                total_bytes           <= 5'd4;
                                tag_record_buffer[31:0] <= reg_wdata;
                                next_state_after_wren <= S_CMD_CS_LOW;
                                state                 <= S_WREN_CS_LOW;
                            end
                            3'b010: begin // SECTOR ERASE 4KB
                                cur_cmd               <= CMD_SECTOR_ERASE;
                                total_bytes           <= 5'd0;
                                next_state_after_wren <= S_CMD_CS_LOW;
                                state                 <= S_WREN_CS_LOW;
                            end
                            3'b011: begin // RDID (3 bytes)
                                cur_cmd     <= CMD_RDID;
                                total_bytes <= 5'd3;
                                state       <= S_CMD_CS_LOW;
                            end
                            3'b100: begin // RDSR (1 byte)
                                cur_cmd     <= CMD_RDSR;
                                total_bytes <= 5'd1;
                                state       <= S_CMD_CS_LOW;
                            end
                            default: state <= S_IDLE;
                        endcase
                    end
                end

                // ------------------------------------------------------------
                // WREN: Send Write Enable (0x06) to Flash
                // ------------------------------------------------------------
                S_WREN_CS_LOW: begin
                    flash_csn   <= 1'b0;
                    flash_sck   <= 1'b0;
                    spi_tx_byte <= CMD_WREN;
                    spi_bit_cnt <= 3'd7;
                    clk_div_cnt <= 8'd0;
                    state       <= S_WREN_SEND;
                end

                S_WREN_SEND: begin
                    if (clk_div_cnt == 0) begin
                        flash_mosi <= spi_tx_byte[spi_bit_cnt];
                    end
                    if (clk_div_cnt == CLK_DIV) begin
                        flash_sck   <= 1'b1;
                        clk_div_cnt <= clk_div_cnt + 1'b1;
                    end else if (clk_div_cnt == (CLK_DIV * 2)) begin
                        flash_sck   <= 1'b0;
                        clk_div_cnt <= 8'd0;
                        if (spi_bit_cnt == 0) begin
                            state <= S_WREN_CS_HIGH;
                        end else begin
                            spi_bit_cnt <= spi_bit_cnt - 1'b1;
                        end
                    end else begin
                        clk_div_cnt <= clk_div_cnt + 1'b1;
                    end
                end

                S_WREN_CS_HIGH: begin
                    flash_csn   <= 1'b1;
                    delay_timer <= 8'd10; // Chip Select deselect time (tSHSL >= 50ns)
                    state       <= S_CS_HIGH_DELAY;
                end

                S_CS_HIGH_DELAY: begin
                    if (delay_timer == 0) begin
                        state <= next_state_after_wren;
                    end else begin
                        delay_timer <= delay_timer - 1'b1;
                    end
                end

                // ------------------------------------------------------------
                // Command Execution: Send Command Opcode
                // ------------------------------------------------------------
                S_CMD_CS_LOW: begin
                    flash_csn   <= 1'b0;
                    flash_sck   <= 1'b0;
                    spi_tx_byte <= cur_cmd;
                    spi_bit_cnt <= 3'd7;
                    clk_div_cnt <= 8'd0;
                    byte_idx    <= 5'd0;
                    state       <= S_CMD_SEND;
                end

                S_CMD_SEND: begin
                    if (clk_div_cnt == 0) begin
                        flash_mosi <= spi_tx_byte[spi_bit_cnt];
                    end
                    if (clk_div_cnt == CLK_DIV) begin
                        flash_sck   <= 1'b1;
                        clk_div_cnt <= clk_div_cnt + 1'b1;
                    end else if (clk_div_cnt == (CLK_DIV * 2)) begin
                        flash_sck   <= 1'b0;
                        clk_div_cnt <= 8'd0;
                        if (spi_bit_cnt == 0) begin
                            // Depending on command, send address or start data
                            if (cur_cmd == CMD_READ || cur_cmd == CMD_PAGE_PROG || cur_cmd == CMD_SECTOR_ERASE) begin
                                state       <= S_ADDR_SEND;
                                spi_tx_byte <= cur_addr[23:16]; // A23-A16
                                spi_bit_cnt <= 3'd7;
                                byte_idx    <= 5'd1;
                            end else if (cur_cmd == CMD_RDID || cur_cmd == CMD_RDSR) begin
                                state       <= S_DATA_RX;
                                spi_bit_cnt <= 3'd7;
                                byte_idx    <= 5'd0;
                            end else begin
                                state <= S_DONE;
                            end
                        end else begin
                            spi_bit_cnt <= spi_bit_cnt - 1'b1;
                        end
                    end else begin
                        clk_div_cnt <= clk_div_cnt + 1'b1;
                    end
                end

                // ------------------------------------------------------------
                // Send 3-byte Address (24-bit)
                // ------------------------------------------------------------
                S_ADDR_SEND: begin
                    if (clk_div_cnt == 0) begin
                        flash_mosi <= spi_tx_byte[spi_bit_cnt];
                    end
                    if (clk_div_cnt == CLK_DIV) begin
                        flash_sck   <= 1'b1;
                        clk_div_cnt <= clk_div_cnt + 1'b1;
                    end else if (clk_div_cnt == (CLK_DIV * 2)) begin
                        flash_sck   <= 1'b0;
                        clk_div_cnt <= 8'd0;
                        if (spi_bit_cnt == 0) begin
                            if (byte_idx == 1) begin
                                spi_tx_byte <= cur_addr[15:8]; // A15-A8
                                spi_bit_cnt <= 3'd7;
                                byte_idx    <= 5'd2;
                            end else if (byte_idx == 2) begin
                                spi_tx_byte <= cur_addr[7:0];  // A7-A0
                                spi_bit_cnt <= 3'd7;
                                byte_idx    <= 5'd3;
                            end else begin
                                byte_idx <= 5'd0;
                                if (cur_cmd == CMD_SECTOR_ERASE) begin
                                    flash_csn             <= 1'b1;
                                    delay_timer           <= 8'd20;
                                    next_state_after_wren <= S_POLL_RDSR_CS;
                                    state                 <= S_CS_HIGH_DELAY;
                                end else if (cur_cmd == CMD_PAGE_PROG) begin
                                    state       <= S_DATA_TX;
                                    spi_bit_cnt <= 3'd7;
                                    if (auto_mode_active) begin
                                        spi_tx_byte <= tag_record_buffer[127:120];
                                    end else begin
                                        spi_tx_byte <= tag_record_buffer[31:24];
                                    end
                                end else begin // CMD_READ
                                    state       <= S_DATA_RX;
                                    spi_bit_cnt <= 3'd7;
                                end
                            end
                        end else begin
                            spi_bit_cnt <= spi_bit_cnt - 1'b1;
                        end
                    end else begin
                        clk_div_cnt <= clk_div_cnt + 1'b1;
                    end
                end

                // ------------------------------------------------------------
                // Transmit Data Bytes (Page Program)
                // ------------------------------------------------------------
                S_DATA_TX: begin
                    if (clk_div_cnt == 0) begin
                        flash_mosi <= spi_tx_byte[spi_bit_cnt];
                    end
                    if (clk_div_cnt == CLK_DIV) begin
                        flash_sck   <= 1'b1;
                        clk_div_cnt <= clk_div_cnt + 1'b1;
                    end else if (clk_div_cnt == (CLK_DIV * 2)) begin
                        flash_sck   <= 1'b0;
                        clk_div_cnt <= 8'd0;
                        if (spi_bit_cnt == 0) begin
                            byte_idx <= byte_idx + 1'b1;
                            if (byte_idx + 1'b1 >= total_bytes) begin
                                flash_csn             <= 1'b1;
                                delay_timer           <= 8'd20;
                                next_state_after_wren <= S_POLL_RDSR_CS;
                                state                 <= S_CS_HIGH_DELAY;
                            end else begin
                                spi_bit_cnt <= 3'd7;
                                if (auto_mode_active) begin
                                    // Shift next byte from 16-byte record
                                    tag_record_buffer <= {tag_record_buffer[119:0], 8'd0};
                                    spi_tx_byte       <= tag_record_buffer[119:112];
                                end else begin
                                    tag_record_buffer[31:0] <= {tag_record_buffer[23:0], 8'd0};
                                    spi_tx_byte             <= tag_record_buffer[23:16];
                                end
                            end
                        end else begin
                            spi_bit_cnt <= spi_bit_cnt - 1'b1;
                        end
                    end else begin
                        clk_div_cnt <= clk_div_cnt + 1'b1;
                    end
                end

                // ------------------------------------------------------------
                // Receive Data Bytes (Read Data / RDID / RDSR)
                // ------------------------------------------------------------
                S_DATA_RX: begin
                    if (clk_div_cnt == CLK_DIV) begin
                        flash_sck   <= 1'b1;
                        spi_rx_byte <= {spi_rx_byte[6:0], flash_miso};
                        clk_div_cnt <= clk_div_cnt + 1'b1;
                    end else if (clk_div_cnt == (CLK_DIV * 2)) begin
                        flash_sck   <= 1'b0;
                        clk_div_cnt <= 8'd0;
                        if (spi_bit_cnt == 0) begin
                            reg_rdata <= {reg_rdata[23:0], spi_rx_byte};
                            byte_idx  <= byte_idx + 1'b1;
                            if (byte_idx + 1'b1 >= total_bytes) begin
                                flash_csn <= 1'b1;
                                state     <= S_DONE;
                            end else begin
                                spi_bit_cnt <= 3'd7;
                            end
                        end else begin
                            spi_bit_cnt <= spi_bit_cnt - 1'b1;
                        end
                    end else begin
                        clk_div_cnt <= clk_div_cnt + 1'b1;
                    end
                end

                // ------------------------------------------------------------
                // Polling Status Register (Wait for Program / Erase completion)
                // ------------------------------------------------------------
                S_POLL_RDSR_CS: begin
                    flash_csn   <= 1'b0;
                    flash_sck   <= 1'b0;
                    spi_tx_byte <= CMD_RDSR;
                    spi_bit_cnt <= 3'd7;
                    clk_div_cnt <= 8'd0;
                    state       <= S_POLL_RDSR_CMD;
                end

                S_POLL_RDSR_CMD: begin
                    if (clk_div_cnt == 0) flash_mosi <= spi_tx_byte[spi_bit_cnt];
                    if (clk_div_cnt == CLK_DIV) begin
                        flash_sck   <= 1'b1;
                        clk_div_cnt <= clk_div_cnt + 1'b1;
                    end else if (clk_div_cnt == (CLK_DIV * 2)) begin
                        flash_sck   <= 1'b0;
                        clk_div_cnt <= 8'd0;
                        if (spi_bit_cnt == 0) begin
                            state       <= S_POLL_RDSR_RX;
                            spi_bit_cnt <= 3'd7;
                        end else begin
                            spi_bit_cnt <= spi_bit_cnt - 1'b1;
                        end
                    end else begin
                        clk_div_cnt <= clk_div_cnt + 1'b1;
                    end
                end

                S_POLL_RDSR_RX: begin
                    if (clk_div_cnt == CLK_DIV) begin
                        flash_sck   <= 1'b1;
                        spi_rx_byte <= {spi_rx_byte[6:0], flash_miso};
                        clk_div_cnt <= clk_div_cnt + 1'b1;
                    end else if (clk_div_cnt == (CLK_DIV * 2)) begin
                        flash_sck   <= 1'b0;
                        clk_div_cnt <= 8'd0;
                        if (spi_bit_cnt == 0) begin
                            flash_status_reg <= spi_rx_byte;
                            flash_csn        <= 1'b1;
                            state            <= S_POLL_CHECK;
                        end else begin
                            spi_bit_cnt <= spi_bit_cnt - 1'b1;
                        end
                    end else begin
                        clk_div_cnt <= clk_div_cnt + 1'b1;
                    end
                end

                S_POLL_CHECK: begin
                    // Bit 0 of SR1 is WIP (Write In Progress)
                    if (flash_status_reg[0] == 1'b0) begin
                        // Done writing / erasing!
                        if (auto_mode_active) begin
                            record_counter <= record_counter + 1'b1;
                        end
                        state <= S_DONE;
                    end else begin
                        // Still busy, wait 50 cycles and poll again
                        delay_timer           <= 8'd50;
                        next_state_after_wren <= S_POLL_RDSR_CS;
                        state                 <= S_CS_HIGH_DELAY;
                    end
                end

                // ------------------------------------------------------------
                // S_DONE: Signal completion
                // ------------------------------------------------------------
                S_DONE: begin
                    flash_csn        <= 1'b1;
                    flash_sck        <= 1'b0;
                    flash_write_done <= 1'b1;
                    state            <= S_IDLE;
                end

                default: state <= S_IDLE;
            endcase
        end
    end

endmodule
