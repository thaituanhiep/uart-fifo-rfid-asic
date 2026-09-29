`timescale 1ns / 1ps

// ============================================================================
// Module: tb_rdm6300_pipeline
// Description: Testbench Verilog for Step 5: RDM6300 5-Stage Autonomous Pipeline
//              Stages:
//                Stage 1: 2-FF CDC Synchronizer (sync_2ff.v)
//                Stage 2: 9600-Baud UART Receiver with 16x oversampling (uart_rx.v)
//                Stage 3: 16-deep Synchronous FIFO (sync_fifo.v)
//                Stage 4: 14-Byte Frame State Machine (rdm6300_frame_decoder.v)
//                Stage 5: Parallel XOR Hardware Checksum Validator & MMIO Registers
// ============================================================================

module tb_rdm6300_pipeline;

    reg clk;
    reg resetn;
    reg rfid_rx_async;

    // Stage 1 output
    wire rfid_rx_sync;

    // Stage 2 outputs
    wire uart_rx_dv;
    wire [7:0] uart_rx_byte;
    wire uart_framing_err;
    wire uart_break_detect;

    // Stage 3 outputs
    wire fifo_empty;
    wire fifo_full;
    wire [7:0] fifo_dout;
    wire [4:0] fifo_count;
    wire fifo_pop;

    // Stage 4 & 5 outputs
    wire decoder_ready;
    wire card_valid;
    wire [39:0] tag_raw;
    wire checksum_error;
    wire frame_error;
    wire invalid_hex_error;
    wire frame_timeout_error;

    // 50MHz System Clock (20ns period)
    initial clk = 0;
    always #10 clk = ~clk;

    // ========================================================================
    // DUT Instantiations (5 Stages)
    // ========================================================================

    // Stage 1: 2-FF Synchronizer
    sync_2ff u_sync (
        .clk(clk),
        .rst_n(resetn),
        .async_i(rfid_rx_async),
        .sync_o(rfid_rx_sync)
    );

    // Stage 2: 9600 Baud UART RX (50MHz / 9600 = 5208 clocks per bit)
    uart_rx #(
        .CLKS_PER_BIT(5208)
    ) u_uart_rx (
        .clk(clk),
        .rst_n(resetn),
        .rx(rfid_rx_sync),
        .rx_dv(uart_rx_dv),
        .rx_byte(uart_rx_byte),
        .framing_error(uart_framing_err),
        .break_detect(uart_break_detect)
    );

    // Stage 3: Synchronous FIFO (16 entries x 8 bits)
    sync_fifo #(
        .DATA_WIDTH(8),
        .DEPTH(16)
    ) u_fifo (
        .clk(clk),
        .rst_n(resetn),
        .push(uart_rx_dv && !fifo_full),
        .din(uart_rx_byte),
        .pop(fifo_pop),
        .dout(fifo_dout),
        .empty(fifo_empty),
        .full(fifo_full),
        .count(fifo_count)
    );

    // Connect FIFO to Frame Decoder
    assign fifo_pop = !fifo_empty && decoder_ready;

    // Stage 4 & 5: Frame Decoder & Parallel XOR Checksum
    rdm6300_frame_decoder #(
        .FRAME_TIMEOUT_CYCLES(500_000)
    ) u_decoder (
        .clk(clk),
        .rst_n(resetn),
        .byte_valid(!fifo_empty),
        .byte_data(fifo_dout),
        .byte_ready(decoder_ready),
        .card_valid(card_valid),
        .tag_raw(tag_raw),
        .checksum_error(checksum_error),
        .frame_error(frame_error),
        .invalid_hex_error(invalid_hex_error),
        .frame_timeout_error(frame_timeout_error)
    );

    // ========================================================================
    // UART Transmitter Task (9600 baud, 1 start, 8 data, 1 stop)
    // ========================================================================
    localparam BIT_PERIOD = 104166; // 104.166 us for 9600 baud (in ns)

    task send_uart_byte(input [7:0] b);
        integer i;
        begin
            // Start bit (0)
            rfid_rx_async = 1'b0;
            #(BIT_PERIOD);
            // 8 Data bits (LSB first)
            for (i = 0; i < 8; i = i + 1) begin
                rfid_rx_async = b[i];
                #(BIT_PERIOD);
            end
            // Stop bit (1)
            rfid_rx_async = 1'b1;
            #(BIT_PERIOD);
        end
    endtask

    // Send complete 14-byte RDM6300 frame
    task send_rdm6300_frame(
        input [7:0] v0, input [7:0] v1,
        input [7:0] s0, input [7:0] s1, input [7:0] s2,
        input [7:0] s3, input [7:0] s4, input [7:0] s5,
        input [7:0] s6, input [7:0] s7,
        input [7:0] c0, input [7:0] c1
    );
        begin
            send_uart_byte(8'h02); // Start byte (STX)
            send_uart_byte(v0);
            send_uart_byte(v1);
            send_uart_byte(s0);
            send_uart_byte(s1);
            send_uart_byte(s2);
            send_uart_byte(s3);
            send_uart_byte(s4);
            send_uart_byte(s5);
            send_uart_byte(s6);
            send_uart_byte(s7);
            send_uart_byte(c0);
            send_uart_byte(c1);
            send_uart_byte(8'h03); // Stop byte (ETX)
        end
    endtask

    // Latches to capture 1-cycle strobes
    reg card_valid_latched;
    reg checksum_error_latched;
    reg [39:0] tag_raw_latched;

    always @(posedge clk or negedge resetn) begin
        if (!resetn) begin
            card_valid_latched     <= 1'b0;
            checksum_error_latched <= 1'b0;
            tag_raw_latched        <= 40'd0;
        end else begin
            if (card_valid) begin
                card_valid_latched <= 1'b1;
                tag_raw_latched    <= tag_raw;
            end
            if (checksum_error) begin
                checksum_error_latched <= 1'b1;
            end
        end
    end

    // ========================================================================
    // Test Sequences
    // ========================================================================
    initial begin
        $display("================================================================");
        $display("  STARTING STEP 5: RDM6300 5-STAGE PIPELINE VERILOG TESTBENCH   ");
        $display("================================================================");

        rfid_rx_async = 1'b1;
        resetn = 1'b0;
        #200;
        resetn = 1'b1;
        #200;

        // Test 1: Send valid card 00007293F0 (Checksum 0x11: ASCII '1', '1')
        $display("[INFO] Transmitting valid RFID Card: 00007293F0 (Checksum 0x11)...");
        card_valid_latched = 1'b0;
        send_rdm6300_frame(
            "0", "0",
            "0", "0", "7", "2", "9", "3", "F", "0",
            "1", "1"
        );

        // Wait for frame decoder to process
        #100000;

        if (card_valid_latched) begin
            $display("  [PASS] TC01: Card valid asserted! Tag Raw = %h (Expected 00007293f0)", tag_raw_latched);
        end else begin
            $display("  [FAIL] TC01: Card valid was not asserted!");
        end

        // Test 2: Send corrupted card frame (bad checksum "99")
        $display("[INFO] Transmitting corrupted RFID Card frame (Bad Checksum)...");
        checksum_error_latched = 1'b0;
        send_rdm6300_frame(
            "0", "0",
            "0", "0", "7", "2", "9", "3", "F", "0",
            "9", "9"
        );

        #100000;

        if (checksum_error_latched) begin
            $display("  [PASS] TC02: Hardware XOR Parity Checksum detected mismatch successfully!");
        end else begin
            $display("  [FAIL] TC02: Checksum error flag not asserted!");
        end

        $display("\n================================================================");
        $display("  STEP 5 VERILOG TESTBENCH COMPLETED SUCCESSFULLY!             ");
        $display("================================================================\n");
        $finish;
    end

endmodule
