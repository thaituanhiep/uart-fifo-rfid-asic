`timescale 1ns/1ps

module top_basys3_rdm6300 #(
    parameter CLKS_PER_BIT = 10417,
    parameter FIFO_DEPTH   = 16,
    parameter FIFO_ADDR_W  = 4
) (
    input  wire       clk,
    input  wire       rst_btn,

    input  wire       rdm6300_rx_i,
    output wire       uart_tx_o,

    output wire [3:0] led
);

    wire rst_n;

    // ------------------------------------------------------------------
    // 2-FF input synchronizer for RDM6300 RX line (prevents metastability)
    // Reset to 1 = UART idle-high state
    // ------------------------------------------------------------------
    reg rdm6300_rx_sync1, rdm6300_rx_sync;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            rdm6300_rx_sync1 <= 1'b1;
            rdm6300_rx_sync  <= 1'b1;
        end else begin
            rdm6300_rx_sync1 <= rdm6300_rx_i;
            rdm6300_rx_sync  <= rdm6300_rx_sync1;
        end
    end

    wire [7:0] rx_rd_data;
    wire       rx_empty;
    wire       rx_full;

    reg rx_rd_en;
    reg tx_wr_en;
    reg [7:0] tx_wr_data;
    wire      tx_full;
    wire      tx_empty;

    reg [2:0] bridge_fsm;
    reg       frame_active;
    reg       last_frame_valid;
    reg [3:0] frame_count;
    reg [4:0] send_idx;
    reg [4:0] send_len;
    reg [7:0] frame_buf [0:13];
    reg [7:0] last_frame [0:13];
    reg [7:0] tx_line_buf [0:21];

    integer i;
    reg frame_same;
    reg checksum_ok;
    reg [4:0] n0, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11;
    reg [7:0] b0, b1, b2, b3, b4;
    reg [7:0] chk_calc, chk_rx;
    reg [31:0] id32;
    reg [7:0]  fc_dec;
    reg [15:0] cn_dec;
    reg [3:0] d0, d1, d2, d3, d4, d5, d6, d7, d8, d9;
    reg [3:0] h, t, o;
    reg [3:0] tt, th, hu, te, on;

    localparam BR_IDLE  = 3'd0;
    localparam BR_READ  = 3'd1;
    localparam BR_LATCH = 3'd2;
    localparam BR_WRITE = 3'd3;

    // Decode one ASCII hex character. Invalid characters map to 5'h10.
    function [4:0] ascii_hex_to_nibble;
        input [7:0] ch;
        begin
            if ((ch >= 8'h30) && (ch <= 8'h39))
                ascii_hex_to_nibble = {1'b0, ch[3:0]};
            else if ((ch >= 8'h41) && (ch <= 8'h46))
                ascii_hex_to_nibble = {1'b0, (ch[3:0] + 4'd9)};
            else if ((ch >= 8'h61) && (ch <= 8'h66))
                ascii_hex_to_nibble = {1'b0, (ch[3:0] + 4'd9)};
            else
                ascii_hex_to_nibble = 5'h10;
        end
    endfunction

    assign rst_n = ~rst_btn;

    uart_fifo_core #(
        .CLKS_PER_BIT(CLKS_PER_BIT),
        .FIFO_DEPTH(FIFO_DEPTH),
        .FIFO_ADDR_W(FIFO_ADDR_W)
    ) u_core (
        .clk(clk),
        .rst_n(rst_n),
        .uart_rx_i(rdm6300_rx_sync),
        .uart_tx_o(uart_tx_o),
        .tx_wr_en(tx_wr_en),
        .tx_wr_data(tx_wr_data),
        .tx_full(tx_full),
        .tx_empty(tx_empty),
        .rx_rd_en(rx_rd_en),
        .rx_rd_data(rx_rd_data),
        .rx_empty(rx_empty),
        .rx_full(rx_full)
    );

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            bridge_fsm   <= BR_IDLE;
            rx_rd_en     <= 1'b0;
            tx_wr_en     <= 1'b0;
            tx_wr_data   <= 8'd0;
            frame_active <= 1'b0;
            last_frame_valid <= 1'b0;
            frame_count <= 4'd0;
            send_idx <= 5'd0;
            send_len <= 5'd0;
            checksum_ok = 1'b0;
            chk_calc = 8'd0;
            chk_rx = 8'd0;
            id32 = 32'd0;
            fc_dec = 8'd0;
            cn_dec = 16'd0;

            for (i = 0; i < 14; i = i + 1) begin
                frame_buf[i] <= 8'd0;
                last_frame[i] <= 8'd0;
            end
            for (i = 0; i < 22; i = i + 1)
                tx_line_buf[i] <= 8'd0;
        end else begin
            rx_rd_en <= 1'b0;
            tx_wr_en <= 1'b0;

            case (bridge_fsm)
                BR_IDLE: begin
                    if (!rx_empty && !tx_full) begin
                        rx_rd_en <= 1'b1;
                        bridge_fsm <= BR_READ;
                    end
                end

                BR_READ: begin
                    bridge_fsm <= BR_LATCH;
                end

                BR_LATCH: begin
                    // Capture one whole frame STX..ETX first, then decide whether to forward.
                    if (!frame_active) begin
                        if (rx_rd_data == 8'h02) begin
                            frame_active <= 1'b1;
                            frame_count <= 4'd1;
                            frame_buf[0] <= 8'h02;
                        end
                        bridge_fsm <= BR_IDLE;
                    end else begin
                        if (frame_count < 4'd14)
                            frame_buf[frame_count] <= rx_rd_data;

                        if ((rx_rd_data == 8'h03) && (frame_count == 4'd13)) begin
                            // Validate RDM6300 checksum over 10 ASCII hex payload digits.
                            n0  = ascii_hex_to_nibble(frame_buf[1]);
                            n1  = ascii_hex_to_nibble(frame_buf[2]);
                            n2  = ascii_hex_to_nibble(frame_buf[3]);
                            n3  = ascii_hex_to_nibble(frame_buf[4]);
                            n4  = ascii_hex_to_nibble(frame_buf[5]);
                            n5  = ascii_hex_to_nibble(frame_buf[6]);
                            n6  = ascii_hex_to_nibble(frame_buf[7]);
                            n7  = ascii_hex_to_nibble(frame_buf[8]);
                            n8  = ascii_hex_to_nibble(frame_buf[9]);
                            n9  = ascii_hex_to_nibble(frame_buf[10]);
                            n10 = ascii_hex_to_nibble(frame_buf[11]);
                            n11 = ascii_hex_to_nibble(frame_buf[12]);

                            checksum_ok = 1'b0;
                            if ((n0 < 5'd16) && (n1 < 5'd16) && (n2 < 5'd16) && (n3 < 5'd16) &&
                                (n4 < 5'd16) && (n5 < 5'd16) && (n6 < 5'd16) && (n7 < 5'd16) &&
                                (n8 < 5'd16) && (n9 < 5'd16) && (n10 < 5'd16) && (n11 < 5'd16)) begin
                                b0 = {n0[3:0],  n1[3:0]};
                                b1 = {n2[3:0],  n3[3:0]};
                                b2 = {n4[3:0],  n5[3:0]};
                                b3 = {n6[3:0],  n7[3:0]};
                                b4 = {n8[3:0],  n9[3:0]};
                                chk_calc = b0 ^ b1 ^ b2 ^ b3 ^ b4;
                                chk_rx   = {n10[3:0], n11[3:0]};
                                checksum_ok = (chk_calc == chk_rx);
                            end

                            frame_active <= 1'b0;
                            frame_count <= 4'd0;

                            if (checksum_ok) begin
                                // TODO(thait): Move duplicate-frame compare/filter into FIFO-side logic
                                // so top-level BR_LATCH only does frame capture and handoff.
                                frame_same = last_frame_valid;
                                for (i = 0; i < 13; i = i + 1) begin
                                    if (frame_buf[i] != last_frame[i])
                                        frame_same = 1'b0;
                                end
                                if (rx_rd_data != last_frame[13])
                                    frame_same = 1'b0;

                                if (!frame_same) begin
                                    for (i = 0; i < 13; i = i + 1)
                                        last_frame[i] <= frame_buf[i];
                                    last_frame[13] <= rx_rd_data;
                                    last_frame_valid <= 1'b1;

                                    // Build fixed-width card text: ID10 + " " + FC3 + "," + CN5 + LF.
                                    id32   = {b1, b2, b3, b4};
                                    fc_dec = b2;
                                    cn_dec = {b3, b4};

                                    d0 = (id32 / 32'd1000000000) % 10;
                                    d1 = (id32 / 32'd100000000)  % 10;
                                    d2 = (id32 / 32'd10000000)   % 10;
                                    d3 = (id32 / 32'd1000000)    % 10;
                                    d4 = (id32 / 32'd100000)     % 10;
                                    d5 = (id32 / 32'd10000)      % 10;
                                    d6 = (id32 / 32'd1000)       % 10;
                                    d7 = (id32 / 32'd100)        % 10;
                                    d8 = (id32 / 32'd10)         % 10;
                                    d9 =  id32 % 10;

                                    tx_line_buf[0]  <= 8'h30 + d0;
                                    tx_line_buf[1]  <= 8'h30 + d1;
                                    tx_line_buf[2]  <= 8'h30 + d2;
                                    tx_line_buf[3]  <= 8'h30 + d3;
                                    tx_line_buf[4]  <= 8'h30 + d4;
                                    tx_line_buf[5]  <= 8'h30 + d5;
                                    tx_line_buf[6]  <= 8'h30 + d6;
                                    tx_line_buf[7]  <= 8'h30 + d7;
                                    tx_line_buf[8]  <= 8'h30 + d8;
                                    tx_line_buf[9]  <= 8'h30 + d9;
                                    tx_line_buf[10] <= 8'h20;

                                    h = (fc_dec / 8'd100) % 10;
                                    t = (fc_dec / 8'd10)  % 10;
                                    o =  fc_dec % 10;

                                    tx_line_buf[11] <= 8'h30 + h;
                                    tx_line_buf[12] <= 8'h30 + t;
                                    tx_line_buf[13] <= 8'h30 + o;
                                    tx_line_buf[14] <= 8'h2C;

                                    tt = (cn_dec / 16'd10000) % 10;
                                    th = (cn_dec / 16'd1000)  % 10;
                                    hu = (cn_dec / 16'd100)   % 10;
                                    te = (cn_dec / 16'd10)    % 10;
                                    on =  cn_dec % 10;

                                    tx_line_buf[15] <= 8'h30 + tt;
                                    tx_line_buf[16] <= 8'h30 + th;
                                    tx_line_buf[17] <= 8'h30 + hu;
                                    tx_line_buf[18] <= 8'h30 + te;
                                    tx_line_buf[19] <= 8'h30 + on;

                                    tx_line_buf[20] <= 8'h0A;
                                    tx_line_buf[21] <= 8'h00;

                                    send_len <= 5'd21;
                                    send_idx <= 5'd0;
                                     bridge_fsm <= BR_WRITE;
                                end else begin
                                    bridge_fsm <= BR_IDLE;
                                end
                            end else begin
                                // Drop corrupted frames instead of forwarding mismatched payload.
                                bridge_fsm <= BR_IDLE;
                            end
                        end else if (frame_count == 4'd13) begin
                            // Overflow/no ETX at expected position -> drop corrupted frame.
                            frame_active <= 1'b0;
                            frame_count <= 4'd0;
                            bridge_fsm <= BR_IDLE;
                        end else begin
                            frame_count <= frame_count + 1'b1;
                            bridge_fsm <= BR_IDLE;
                        end
                    end
                end

                BR_WRITE: begin
                    if (send_len == 5'd0) begin
                        bridge_fsm <= BR_IDLE;
                    end else if (send_idx >= send_len) begin
                        bridge_fsm <= BR_IDLE;
                    end else if (!tx_full) begin
                         tx_wr_en <= 1'b1;
                         tx_wr_data <= tx_line_buf[send_idx];

                         if (send_idx == (send_len - 1'b1)) begin
                             bridge_fsm <= BR_IDLE;
                         end else begin
                             send_idx <= send_idx + 1'b1;
                             bridge_fsm <= BR_WRITE;
                         end
                     end
                 end

                default: bridge_fsm <= BR_IDLE;
            endcase
        end
    end

    assign led[0] = ~rx_empty;
    assign led[1] = ~tx_empty;
    assign led[2] = rx_full;
    assign led[3] = tx_full;

endmodule
