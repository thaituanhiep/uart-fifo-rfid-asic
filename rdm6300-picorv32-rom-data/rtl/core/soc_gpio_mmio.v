// ============================================================================
// File: rtl/soc_gpio_mmio.v
// Project: rdm6300-picorv32-rom-data
// Description: General Purpose I/O (GPIO) Controller, Hardware Heartbeat Counter,
//              System Status Diagnostics, and PicoRV32 MMIO Slave Interface (Base: 0x4000_0000).
//
// Memory Map (Base: 0x4000_0000):
//   0x4000_0000: GPIO LED Output Register (16-bit Read/Write)
//
// LED Physical Pin Assignment (leds_o[15:0]):
//   LED 0       : Heartbeat blink (~1.5Hz at 50MHz) - proves ASIC clock is alive
//   LED 1       : CPU TRAP indicator (active HIGH only if PicoRV32 crashes)
//   LED 2       : RFID Card Event detected pulse
//   LED 3       : SPI Flash busy indicator (active low CS_N asserted)
//   LED 4       : SPI Flash done / idle indicator
//   LED 5       : Reserved (GND / 0)
//   LED [15:6]  : Software-programmable general purpose LED outputs
// ============================================================================

`timescale 1ns / 1ps

module soc_gpio_mmio (
    input  wire        clk,
    input  wire        rst_n,

    // PicoRV32 Native Memory Bus Slave Interface (0x4000_0000)
    input  wire        valid,
    input  wire [3:0]  addr,      // cpu_mem_addr[3:0]
    input  wire [31:0] wdata,
    input  wire [3:0]  wstrb,
    output reg  [31:0] rdata,
    output reg         ready,

    // Hardware Diagnostic Inputs from SoC Subsystems
    input  wire        cpu_trap,
    input  wire        card_event_i,
    input  wire        flash_busy_i,
    input  wire        flash_done_i,

    // Physical LED Output Pins (16-bit status & GPIO)
    output reg  [15:0] leds_o
);

    reg [25:0] heartbeat_cnt;
    reg [15:0] gpio_led_reg;

    // ------------------------------------------------------------------------
    // 1. MMIO Register Logic & Heartbeat Counter
    // ------------------------------------------------------------------------
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            ready         <= 1'b0;
            rdata         <= 32'd0;
            gpio_led_reg  <= 16'd0;
            heartbeat_cnt <= 26'd0;
        end else begin
            heartbeat_cnt <= heartbeat_cnt + 1'b1;
            ready         <= valid && !ready;

            if (valid && !ready) begin
                rdata <= {16'd0, gpio_led_reg};
                if (|wstrb) begin
                    if (wstrb[0]) gpio_led_reg[7:0]  <= wdata[7:0];
                    if (wstrb[1]) gpio_led_reg[15:8] <= wdata[15:8];
                end
            end
        end
    end

    // ------------------------------------------------------------------------
    // 2. Hardware Status Diagnostic Output Multiplexer
    // ------------------------------------------------------------------------
    always @(*) begin
        leds_o = {
            gpio_led_reg[15:6], // Software-controlled LEDs [15:6]
            1'b0,               // LED 5: Reserved
            flash_done_i,       // LED 4: SPI Flash idle
            flash_busy_i,       // LED 3: SPI Flash active
            card_event_i,       // LED 2: Card event detected
            cpu_trap,           // LED 1: CPU TRAP fault
            heartbeat_cnt[25]   // LED 0: Clock heartbeat blink
        };
    end

endmodule
