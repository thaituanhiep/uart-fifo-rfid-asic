`timescale 1ns/1ps

module sync_2ff #(
    parameter RESET_VALUE = 1'b0
) (
    input  wire clk,
    input  wire rst_n,
    input  wire async_i,
    output reg  sync_o
);
    reg sync_ff1;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            sync_ff1 <= RESET_VALUE;
            sync_o   <= RESET_VALUE;
        end else begin
            sync_ff1 <= async_i;
            sync_o   <= sync_ff1;
        end
    end
endmodule
