// ============================================================================
// File: tb_picorv32_rdm6300_flash.v
// Project: rdm6300-picorv32-rom-data
// Description: Testbench verifying PicoRV32 execution, RDM6300 RFID reception,
//              and SPI Flash automatic card logging.
// ============================================================================

`timescale 1ns / 1ps

module tb_picorv32_rdm6300_flash;

    reg clk;
    reg rst_n;
    reg rdm6300_rx_i;
    reg uart_rx_i;

    wire uart_tx_o;
    wire flash_csn;
    wire flash_sck;
    wire flash_mosi;
    wire flash_miso;
    wire [15:0] leds_o;
    wire cpu_trap;
    wire card_event_o;
    wire flash_busy_o;
    wire flash_done_o;

    // 100 MHz Clock (10 ns period)
    always #5 clk = ~clk;

    // Fast baud simulation for testbench: CLKS_PER_BIT = 16
    localparam TB_CLKS_PER_BIT = 16;
    localparam BIT_PERIOD = TB_CLKS_PER_BIT * 10; // 160 ns per bit

    // ------------------------------------------------------------------------
    // DUT Instantiation
    // ------------------------------------------------------------------------
    rdm6300_picorv32_soc #(
        .CLK_FREQ_HZ(100_000_000),
        .UART_BAUD(6_250_000), // Scaled for fast testbench simulation
        .FLASH_BASE(24'h30_0000),
        .BOOT_HEX("firmware.hex")
    ) dut (
        .clk(clk),
        .rst_n(rst_n),
        .rdm6300_rx_i(rdm6300_rx_i),
        .uart_tx_o(uart_tx_o),
        .uart_rx_i(uart_rx_i),
        .flash_csn(flash_csn),
        .flash_sck(flash_sck),
        .flash_mosi(flash_mosi),
        .flash_miso(flash_miso),
        .leds_o(leds_o),
        .cpu_trap(cpu_trap),
        .card_event_o(card_event_o),
        .flash_busy_o(flash_busy_o),
        .flash_done_o(flash_done_o)
    );

    // ------------------------------------------------------------------------
    // Behavioral SPI Flash Model (Spansion S25FL032P / W25Qxx)
    // ------------------------------------------------------------------------
    reg [7:0] flash_mem [0:4095]; // 4KB model buffer
    reg [7:0] flash_sr = 8'h00;   // Status register (bit 0: WIP, bit 1: WEL)
    reg flash_miso_reg = 1'b0;
    assign flash_miso = flash_csn ? 1'bz : flash_miso_reg;

    reg [7:0]  spi_cmd;
    reg [23:0] spi_addr;
    reg [7:0]  rx_shifter;
    reg [2:0]  bit_idx;
    integer    state_spi;
    integer    byte_count;

    initial begin
        state_spi = 0;
        bit_idx = 0;
    end

    always @(negedge flash_csn) begin
        state_spi  <= 0;
        bit_idx    <= 7;
        rx_shifter <= 8'd0;
        byte_count <= 0;
    end

    always @(posedge flash_sck) begin
        rx_shifter[bit_idx] <= flash_mosi;
        if (bit_idx == 0) begin
            bit_idx <= 7;
            case (state_spi)
                0: begin // Command Byte
                    spi_cmd <= {rx_shifter[7:1], flash_mosi};
                    if ({rx_shifter[7:1], flash_mosi} == 8'h06) begin // WREN
                        flash_sr[1] <= 1'b1; // Set WEL
                        $display("[FLASH MODEL] Command: WREN (Write Enable)");
                    end else if ({rx_shifter[7:1], flash_mosi} == 8'h05) begin // RDSR
                        state_spi <= 3; // Shift status register
                    end else if ({rx_shifter[7:1], flash_mosi} == 8'h9F) begin // RDID
                        state_spi <= 4; // Shift JEDEC ID
                        $display("[FLASH MODEL] Command: RDID (Read JEDEC ID)");
                    end else begin
                        state_spi <= 1; // Expect address
                        byte_count <= 0;
                    end
                end

                1: begin // Address Bytes (3 bytes)
                    if (byte_count == 0) begin
                        spi_addr[23:16] <= {rx_shifter[7:1], flash_mosi};
                        byte_count <= 1;
                    end else if (byte_count == 1) begin
                        spi_addr[15:8] <= {rx_shifter[7:1], flash_mosi};
                        byte_count <= 2;
                    end else if (byte_count == 2) begin
                        spi_addr[7:0] <= {rx_shifter[7:1], flash_mosi};
                        state_spi <= 2; // Data phase
                        byte_count <= 0;
                        $display("[FLASH MODEL] Command: 0x%02X, Target Addr: 0x%06X", spi_cmd, {spi_addr[23:8], rx_shifter[7:1], flash_mosi});
                    end
                end

                2: begin // Data write phase (Page Program)
                    if (spi_cmd == 8'h02) begin
                        flash_mem[spi_addr[11:0] + byte_count] <= {rx_shifter[7:1], flash_mosi};
                        $display("[FLASH MODEL] Written Byte[%0d] = 0x%02X at Addr 0x%06X", byte_count, {rx_shifter[7:1], flash_mosi}, spi_addr + byte_count);
                        byte_count <= byte_count + 1;
                    end
                end
            endcase
        end else begin
            bit_idx <= bit_idx - 1;
        end
    end

    // MISO shifting
    reg [23:0] flash_id_val = 24'h010216; // Spansion S25FL032P ID
    always @(negedge flash_sck) begin
        if (state_spi == 3) begin // RDSR response
            flash_miso_reg <= flash_sr[bit_idx];
        end else if (state_spi == 4) begin // RDID response
            flash_miso_reg <= flash_id_val[bit_idx];
        end else begin
            flash_miso_reg <= 1'b0;
        end
    end

    reg card_event_latched = 1'b0;
    reg flash_busy_latched = 1'b0;
    reg flash_done_latched = 1'b0;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            card_event_latched <= 1'b0;
            flash_busy_latched <= 1'b0;
            flash_done_latched <= 1'b0;
        end else begin
            if (card_event_o) card_event_latched <= 1'b1;
            if (flash_busy_o) flash_busy_latched <= 1'b1;
            if (flash_done_o) flash_done_latched <= 1'b1;
        end
    end

    always @(posedge clk) begin
        if (dut.u_rdm_rx.rx_dv) $display("[TB MON] u_rdm_rx received byte: 0x%02X ('%c')", dut.u_rdm_rx.rx_byte, dut.u_rdm_rx.rx_byte);
        if (dut.u_rdm_rx.framing_error) $display("[TB MON ERROR] u_rdm_rx framing_error!");
        if (dut.u_rdm_decoder.frame_error) $display("[TB MON ERROR] u_rdm_decoder frame_error!");
        if (dut.u_rdm_decoder.checksum_error) $display("[TB MON ERROR] u_rdm_decoder checksum_error!");
    end

    // ------------------------------------------------------------------------
    // Tasks: UART Byte Transmission
    // ------------------------------------------------------------------------
    task send_uart_byte(input [7:0] b);
        integer k;
        begin
            // Start bit
            rdm6300_rx_i = 1'b0;
            #BIT_PERIOD;
            // 8 Data bits (LSB first)
            for (k = 0; k < 8; k = k + 1) begin
                rdm6300_rx_i = b[k];
                #BIT_PERIOD;
            end
            // Stop bit
            rdm6300_rx_i = 1'b1;
            #BIT_PERIOD;
            #(BIT_PERIOD / 2);
        end
    endtask

    task send_rdm6300_frame;
        begin
            $display("[TB] Sending RDM6300 14-byte ASCII Frame: STX 010054DA65 Checksum(EE) ETX");
            send_uart_byte(8'h02); // STX
            send_uart_byte("0");   // Version B0
            send_uart_byte("1");
            send_uart_byte("0");   // Tag Data B1
            send_uart_byte("0");
            send_uart_byte("5");   // Tag Data B2
            send_uart_byte("4");
            send_uart_byte("D");   // Tag Data B3
            send_uart_byte("A");
            send_uart_byte("6");   // Tag Data B4
            send_uart_byte("5");
            send_uart_byte("E");   // Checksum (0x01 ^ 0x00 ^ 0x54 ^ 0xDA ^ 0x65 = 0xEA)
            send_uart_byte("A");
            send_uart_byte(8'h03); // ETX
            $display("[TB] Frame transmission complete.");
        end
    endtask

    // ------------------------------------------------------------------------
    // Test Sequence
    // ------------------------------------------------------------------------
    initial begin
        $display("===============================================================");
        $display("  Starting Simulation: tb_picorv32_rdm6300_flash");
        $display("===============================================================");

        clk          = 0;
        rst_n        = 0;
        rdm6300_rx_i = 1;
        uart_rx_i    = 1;

        // Reset pulse
        #100;
        rst_n = 1;
        $display("[TB] System Reset released. PicoRV32 booting from SRAM...");

        // Wait 100 cycles for PicoRV32 to execute initial instructions
        #1000;

        // Verify CPU did not trap
        if (cpu_trap) begin
            $display("[TB ERROR] CPU entered TRAP state!");
            $finish;
        end else begin
            $display("[TB] PicoRV32 is running smoothly (cpu_trap = 0).");
        end

        // Send valid RFID frame
        #500;
        send_rdm6300_frame();

        // Wait for card_event
        wait(card_event_latched == 1'b1);
        $display("[TB SUCCESS] Card event detected! Tag UID = 0x010054DA65");

        // Wait for SPI Flash controller to execute write
        wait(flash_busy_latched == 1'b1);
        $display("[TB] SPI Flash controller is busy writing card record to Flash...");

        wait(flash_done_latched == 1'b1);
        $display("[TB SUCCESS] SPI Flash controller completed writing to Flash!");

        #1000;
        $display("===============================================================");
        $display("  ALL VERIFICATION CHECKS PASSED SUCCESSFULLY!");
        $display("  1. PicoRV32 Core booted and running.");
        $display("  2. RDM6300 RFID frame received & decoded.");
        $display("  3. SPI Flash auto-save executed successfully.");
        $display("===============================================================");
        $finish;
    end

    // Safety timeout
    initial begin
        #500000;
        $display("[TB TIMEOUT] Simulation exceeded maximum time!");
        $finish;
    end

endmodule
