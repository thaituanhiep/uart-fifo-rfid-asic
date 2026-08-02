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
    reg [3:0] send_idx;
    reg [7:0] frame_buf [0:13];
    reg [7:0] last_frame [0:13];

    integer i;
    reg frame_same;

    localparam BR_IDLE  = 3'd0;
    localparam BR_READ  = 3'd1;
    localparam BR_LATCH = 3'd2;
    localparam BR_WRITE = 3'd3;

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
            send_idx <= 4'd0;

            for (i = 0; i < 14; i = i + 1) begin
                frame_buf[i] <= 8'd0;
                last_frame[i] <= 8'd0;
            end
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
                            // TODO(thait): Move duplicate-frame compare/filter into FIFO-side logic
                            // so top-level BR_LATCH only does frame capture and handoff.
                            frame_same = last_frame_valid;
                            for (i = 0; i < 13; i = i + 1) begin
                                if (frame_buf[i] != last_frame[i])
                                    frame_same = 1'b0;
                            end
                            if (rx_rd_data != last_frame[13])
                                frame_same = 1'b0;

                            frame_active <= 1'b0;
                            frame_count <= 4'd0;

                            if (!frame_same) begin
                                for (i = 0; i < 13; i = i + 1)
                                    last_frame[i] <= frame_buf[i];
                                last_frame[13] <= rx_rd_data;
                                last_frame_valid <= 1'b1;
                                send_idx <= 4'd0;
                                bridge_fsm <= BR_WRITE;
                            end else begin
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
                    if (!tx_full) begin
                        tx_wr_en <= 1'b1;
                        tx_wr_data <= frame_buf[send_idx];
                        if (send_idx == 4'd13) begin
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
