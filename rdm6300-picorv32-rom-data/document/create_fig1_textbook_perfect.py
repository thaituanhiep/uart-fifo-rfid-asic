# -*- coding: utf-8 -*-
"""
Script: create_fig1_textbook_perfect.py
Generates an authentic academic textbook-style hardware schematic block diagram
matching the user's reference image with exact architectural precision:
- Pure white background with crisp black schematic lines.
- Large, bold, highly legible fonts throughout (10pt - 18pt).
- Exact schematic symbols:
  * Top Power & Clock:
    - Power Input (USB 5V DC)
    - Regulator (LDO 3.3V & 1.8V with schematic IC symbol)
    - Clock Oscillator (50 MHz Crystal with quartz crystal schematic symbol)
  * Central IC: PicoRV32 RISC-V SoC with exact pin stubs, pin numbers, and bold pin names
  * Left: RFID Reader RDM6300 with schematic coil antenna and EM4100 tag
  * Left: ASM/C Program (RISC-V GCC C/ASM)
  * Right: SPI NOR Flash Memory (S25FL032P) with pin stubs and internal memory map
  * Right: Host PC Management Console (FTDI USB-UART Bridge + Win32 C App)
  * Bottom Right: Status Button with schematic push-button switch symbol
  * Bottom Center: 16 Diagnostic LEDs with schematic LED diode symbols
- Academic open-triangle arrows (classic schematic style).
- Zero line overlaps, generous spacing, perfect plumb alignment.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, Circle, Polygon, Arc
import math

def create_textbook_diagram():
    # 21 x 15 inches at 300 DPI for crystal clear vector-like quality
    fig, ax = plt.subplots(figsize=(21, 15), dpi=300)
    ax.set_xlim(0, 21)
    ax.set_ylim(0, 15)
    ax.axis('off')

    # Pure white background
    ax.add_patch(Rectangle((0, 0), 21, 15, facecolor='#FFFFFF', zorder=0))

    # Helper: Draw open triangle arrowhead (classic schematic style like user's reference)
    def draw_open_arrow(x_start, y_start, x_end, y_end, size=0.25, lw=1.8):
        ax.plot([x_start, x_end], [y_start, y_end], color='#000000', lw=lw, zorder=5)
        dx = x_end - x_start
        dy = y_end - y_start
        angle = math.atan2(dy, dx)
        a1_x = x_end - size * math.cos(angle - math.pi / 6)
        a1_y = y_end - size * math.sin(angle - math.pi / 6)
        a2_x = x_end - size * math.cos(angle + math.pi / 6)
        a2_y = y_end - size * math.sin(angle + math.pi / 6)
        ax.plot([a1_x, x_end, a2_x], [a1_y, y_end, a2_y], color='#000000', lw=lw, zorder=6)

    # Helper: Draw schematic LED symbol
    def draw_schematic_led(x, y, label=""):
        tri = Polygon([[x - 0.18, y + 0.18], [x + 0.18, y + 0.18], [x, y - 0.14]],
                      closed=True, edgecolor='#000000', facecolor='#FFFFFF', lw=1.6, zorder=5)
        ax.add_patch(tri)
        ax.plot([x - 0.20, x + 0.20], [y - 0.14, y - 0.14], color='#000000', lw=1.8, zorder=5)
        ax.annotate("", xy=(x + 0.36, y + 0.20), xytext=(x + 0.20, y + 0.08),
                    arrowprops=dict(arrowstyle="->", color='#000000', lw=1.3))
        ax.annotate("", xy=(x + 0.40, y + 0.08), xytext=(x + 0.24, y - 0.04),
                    arrowprops=dict(arrowstyle="->", color='#000000', lw=1.3))
        if label:
            ax.text(x, y - 0.38, label, fontsize=9.2, fontweight='bold', ha='center', va='top', fontfamily='monospace', zorder=10)

    # Helper: Draw schematic push-button switch
    def draw_switch(x, y):
        ax.plot([x - 0.50, x - 0.22], [y, y], color='#000000', lw=1.8, zorder=5)
        ax.plot([x + 0.22, x + 0.50], [y, y], color='#000000', lw=1.8, zorder=5)
        ax.plot([x - 0.32, x + 0.32], [y + 0.24, y + 0.24], color='#000000', lw=2.4, zorder=5)
        ax.plot([x, x], [y + 0.24, y + 0.46], color='#000000', lw=1.8, zorder=5)
        ax.add_patch(Circle((x - 0.22, y), 0.045, facecolor='#FFFFFF', edgecolor='#000000', lw=1.6, zorder=6))
        ax.add_patch(Circle((x + 0.22, y), 0.045, facecolor='#FFFFFF', edgecolor='#000000', lw=1.6, zorder=6))
        ax.text(x - 0.38, y + 0.10, "(1)", fontsize=9.0, fontweight='bold')
        ax.text(x + 0.38, y + 0.10, "(2)", fontsize=9.0, fontweight='bold')

    # Helper: Draw schematic crystal oscillator
    def draw_crystal(x, y):
        ax.plot([x - 0.26, x - 0.26], [y - 0.32, y + 0.32], color='#000000', lw=2.2, zorder=5)
        ax.plot([x + 0.26, x + 0.26], [y - 0.32, y + 0.32], color='#000000', lw=2.2, zorder=5)
        ax.add_patch(Rectangle((x - 0.16, y - 0.26), 0.32, 0.52, facecolor='#F0F0F0', edgecolor='#000000', lw=1.5, zorder=6))
        ax.plot([x - 0.60, x - 0.26], [y, y], color='#000000', lw=1.8, zorder=5)
        ax.plot([x + 0.26, x + 0.60], [y, y], color='#000000', lw=1.8, zorder=5)

    # Helper: Draw schematic IC Regulator
    def draw_regulator_symbol(x, y, w=2.6, h=1.4, in_txt="VI", out_txt="VO", gnd_txt="GND", name="LDO"):
        ax.add_patch(Rectangle((x, y), w, h, facecolor='#FFFFFF', edgecolor='#000000', lw=1.8, zorder=4))
        ax.text(x + w/2, y + h/2 + 0.15, name, fontsize=12.0, fontweight='bold', ha='center', va='center', zorder=10)
        # Pin IN (1)
        ax.plot([x - 0.45, x], [y + h/2, y + h/2], color='#000000', lw=1.8, zorder=5)
        ax.text(x + 0.18, y + h/2, in_txt, fontsize=9.5, fontweight='bold', va='center', ha='left', zorder=10)
        ax.text(x - 0.25, y + h/2 + 0.18, "1", fontsize=9.0, ha='center', zorder=10)
        # Pin OUT (3)
        ax.plot([x + w, x + w + 0.45], [y + h/2, y + h/2], color='#000000', lw=1.8, zorder=5)
        ax.text(x + w - 0.18, y + h/2, out_txt, fontsize=9.5, fontweight='bold', va='center', ha='right', zorder=10)
        ax.text(x + w + 0.25, y + h/2 + 0.18, "3", fontsize=9.0, ha='center', zorder=10)
        # Pin GND (2)
        ax.plot([x + w/2, x + w/2], [y, y - 0.38], color='#000000', lw=1.8, zorder=5)
        ax.text(x + w/2, y + 0.22, gnd_txt, fontsize=9.0, fontweight='bold', ha='center', va='bottom', rotation=90, zorder=10)
        ax.text(x + w/2 + 0.18, y - 0.20, "2", fontsize=9.0, va='center', zorder=10)

    # =========================================================================
    # 1. TOP POWER SUPPLY & CLOCK SUBSYSTEM (Transformer -> Rectifier -> Regulator Style)
    # =========================================================================
    # Box 1: Power Input (USB 5V DC)
    p_in_x, p_in_y, p_in_w, p_in_h = 1.0, 11.8, 3.8, 2.3
    ax.add_patch(Rectangle((p_in_x, p_in_y), p_in_w, p_in_h, facecolor='#FFFFFF', edgecolor='#000000', lw=2.0, zorder=3))
    ax.text(p_in_x + p_in_w/2, p_in_y + p_in_h + 0.24, "Power Input", fontsize=14.0, fontweight='bold', ha='center', zorder=10)
    
    # USB Connector Symbol inside
    ax.add_patch(Rectangle((p_in_x + 0.45, p_in_y + 0.70), 1.25, 0.95, facecolor='#F6F6F6', edgecolor='#000000', lw=1.6, zorder=4))
    ax.text(p_in_x + 1.08, p_in_y + 1.17, "USB", fontsize=11.5, fontweight='bold', ha='center', va='center', zorder=10)
    ax.plot([p_in_x + 1.70, p_in_x + 2.80], [p_in_y + 1.40, p_in_y + 1.40], color='#000000', lw=1.8)
    ax.plot([p_in_x + 1.70, p_in_x + 2.80], [p_in_y + 0.95, p_in_y + 0.95], color='#000000', lw=1.8)
    ax.text(p_in_x + 2.90, p_in_y + 1.40, "+5V DC", fontsize=10.5, fontweight='bold', va='center', zorder=10)
    ax.text(p_in_x + 2.90, p_in_y + 0.95, "GND", fontsize=10.5, fontweight='bold', va='center', zorder=10)
    ax.text(p_in_x + p_in_w/2, p_in_y + 0.28, "5.0V @ 500mA", fontsize=10.5, fontweight='bold', ha='center', fontfamily='monospace', zorder=10)

    # Arrow from Power Input to Regulator
    draw_open_arrow(p_in_x + p_in_w, p_in_y + p_in_h/2, 5.8, p_in_y + p_in_h/2, size=0.25, lw=1.8)

    # Box 2: Regulator (LDO Dual)
    reg_x, reg_y, reg_w, reg_h = 5.8, 11.8, 5.8, 2.3
    ax.add_patch(Rectangle((reg_x, reg_y), reg_w, reg_h, facecolor='#FFFFFF', edgecolor='#000000', lw=2.0, zorder=3))
    ax.text(reg_x + reg_w/2, reg_y + p_in_h + 0.24, "Regulator", fontsize=14.0, fontweight='bold', ha='center', zorder=10)
    draw_regulator_symbol(reg_x + 1.6, reg_y + 0.50, w=2.6, h=1.3, in_txt="VI", out_txt="VO", gnd_txt="GND", name="LDO Dual")
    ax.text(reg_x + 0.80, reg_y + 0.25, "Vin: 5V", fontsize=10.0, fontweight='bold', ha='center', zorder=10)
    ax.text(reg_x + reg_w - 0.80, reg_y + 0.25, "3.3V / 1.8V", fontsize=10.0, fontweight='bold', ha='center', zorder=10)

    # Box 3: Clock Oscillator (50 MHz Crystal)
    clk_x, clk_y, clk_w, clk_h = 12.8, 11.8, 7.2, 2.3
    ax.add_patch(Rectangle((clk_x, clk_y), clk_w, clk_h, facecolor='#FFFFFF', edgecolor='#000000', lw=2.0, zorder=3))
    ax.text(clk_x + clk_w/2, clk_y + clk_h + 0.24, "Clock Oscillator", fontsize=14.0, fontweight='bold', ha='center', zorder=10)
    draw_crystal(clk_x + 2.0, clk_y + 1.15)
    ax.text(clk_x + 3.6, clk_y + 1.40, "50 MHz Crystal", fontsize=12.0, fontweight='bold', zorder=10)
    ax.text(clk_x + 3.6, clk_y + 0.90, "Period = 20.0 ns", fontsize=10.5, fontfamily='monospace', zorder=10)
    ax.text(clk_x + clk_w/2, clk_y + 0.28, "Main System Clock (clk)", fontsize=10.0, fontweight='bold', ha='center', color='#333333', zorder=10)

    # Clean Power & Clock Wires down to SoC top pins (Zero crossing, perfect breathing room):
    # 1. Regulator VO drops straight down at x = 7.8 from Regulator directly to SoC VDD!
    draw_open_arrow(7.8, 11.8, 7.8, 11.0, size=0.22, lw=1.8)
    ax.text(7.7, 11.35, "VDD (1.8V / 3.3V)", fontsize=9.5, fontweight='bold', va='center', ha='right', zorder=10)

    # 2. Clock out exits from bottom of Clock Box at (13.6, 11.8), goes down to y = 11.4, left to x = 10.2, then down to SoC clk!
    ax.plot([13.6, 13.6, 10.2, 10.2], [11.8, 11.4, 11.4, 11.0], color='#000000', lw=1.8, zorder=4)
    draw_open_arrow(10.2, 11.4, 10.2, 11.0, size=0.22, lw=1.8)
    ax.text(11.9, 11.58, "clk (50 MHz)", fontsize=10.0, fontweight='bold', ha='center', zorder=10)

    # =========================================================================
    # 2. CENTRAL INTEGRATED CIRCUIT (PicoRV32 RISC-V SoC Chip)
    # =========================================================================
    chip_x, chip_y, chip_w, chip_h = 6.0, 3.4, 5.4, 7.1
    ax.add_patch(Rectangle((chip_x, chip_y), chip_w, chip_h,
                           facecolor='#FFFFFF', edgecolor='#000000', lw=2.6, zorder=3))

    # Prominent Central Chip Title rotated 90 degrees (just like "8051 series MC")
    ax.text(chip_x + chip_w/2 - 0.35, chip_y + chip_h/2,
            "PicoRV32 RISC-V SoC",
            fontsize=18.0, fontweight='bold', color='#000000', ha='center', va='center',
            fontfamily='sans-serif', rotation=90, zorder=10)

    ax.text(chip_x + chip_w/2 + 0.45, chip_y + chip_h/2,
            "rdm6300_picorv32_soc",
            fontsize=12.0, fontweight='bold', color='#333333', ha='center', va='center',
            fontfamily='monospace', rotation=90, zorder=10)

    ax.text(chip_x + chip_w/2 + 1.05, chip_y + chip_h/2,
            "(RV32I Core + 1KB SRAM + SPIMEMIO + UART)",
            fontsize=9.5, fontstyle='italic', color='#555555', ha='center', va='center',
            fontfamily='sans-serif', rotation=90, zorder=10)

    # Helper: draw chip pin stub
    def draw_chip_pin(x_chip, y, length, pin_num, pin_name, side='left'):
        lw = 1.8
        if side == 'left':
            ax.plot([x_chip - length, x_chip], [y, y], color='#000000', lw=lw, zorder=4)
            if pin_num:
                ax.text(x_chip - 0.12, y + 0.12, str(pin_num), fontsize=9.5, fontweight='bold', color='#000000', ha='right', va='bottom', zorder=10)
            ax.text(x_chip + 0.22, y, pin_name, fontsize=11.5, fontweight='bold', color='#000000', va='center', ha='left', fontfamily='monospace', zorder=10)
        elif side == 'right':
            ax.plot([x_chip, x_chip + length], [y, y], color='#000000', lw=lw, zorder=4)
            if pin_num:
                ax.text(x_chip + 0.12, y + 0.12, str(pin_num), fontsize=9.5, fontweight='bold', color='#000000', ha='left', va='bottom', zorder=10)
            ax.text(x_chip - 0.22, y, pin_name, fontsize=11.5, fontweight='bold', color='#000000', va='center', ha='right', fontfamily='monospace', zorder=10)
        elif side == 'bottom':
            ax.plot([x_chip, x_chip], [y, y - length], color='#000000', lw=lw, zorder=4)
            ax.text(x_chip, y + 0.22, pin_name, fontsize=10.5, fontweight='bold', color='#000000', va='bottom', ha='center', fontfamily='monospace', rotation=90, zorder=10)
        elif side == 'top':
            ax.plot([x_chip, x_chip], [y, y + length], color='#000000', lw=lw, zorder=4)
            ax.text(x_chip, y - 0.22, pin_name, fontsize=11.0, fontweight='bold', color='#000000', va='top', ha='center', fontfamily='monospace', rotation=90, zorder=10)

    # --- TOP PINS ---
    draw_chip_pin(7.8, chip_y + chip_h, length=0.5, pin_num="", pin_name="VDD", side='top')
    draw_chip_pin(10.2, chip_y + chip_h, length=0.5, pin_num="W5", pin_name="clk", side='top')

    # --- LEFT PINS ---
    left_pins = [
        (8.8, "rdm_rx", "J1"),
        (7.0, "boot_vec", "0x25"),
        (5.5, "flashio_reloc", "SRAM"),
        (4.2, "VSS/GND", "Die"),
    ]
    for py, pname, pnum in left_pins:
        draw_chip_pin(chip_x, py, length=0.6, pin_num=pnum, pin_name=pname, side='left')

    # --- RIGHT PINS ---
    right_pins = [
        (9.7, "flash_csb", "L13"),
        (8.9, "flash_clk", "CCLK"),
        (8.1, "flash_io0", "K17"),
        (7.3, "flash_io1", "K18"),
        (5.8, "uart_rx", "B18"),
        (5.0, "uart_tx", "A18"),
        (4.1, "rst_n", "U18"),
    ]
    for py, pname, pnum in right_pins:
        draw_chip_pin(chip_x + chip_w, py, length=0.6, pin_num=pnum, pin_name=pname, side='right')

    # --- BOTTOM PINS (16 Diagnostic LEDs - Plumb alignment) ---
    bottom_pins = [
        (chip_x + 0.8, "led[0]"),
        (chip_x + 1.8, "led[1]"),
        (chip_x + 2.8, "led[2]"),
        (chip_x + 3.8, "led[3]"),
        (chip_x + 4.6, "led[15:4]"),
    ]
    for px, pname in bottom_pins:
        draw_chip_pin(px, chip_y, length=0.5, pin_num="", pin_name=pname, side='bottom')

    # =========================================================================
    # 3. EXTERNAL HARDWARE BLOCK 1: RFID READER RDM6300 (Left Upper-Mid)
    # =========================================================================
    rf_x, rf_y, rf_w, rf_h = 0.8, 7.6, 4.0, 2.7
    ax.add_patch(Rectangle((rf_x, rf_y), rf_w, rf_h, facecolor='#FFFFFF', edgecolor='#000000', lw=2.0, zorder=3))
    ax.text(rf_x + rf_w/2, rf_y + rf_h + 0.24, "RFID READER", fontsize=14.0, fontweight='bold', ha='center', zorder=10)
    
    # Antenna Coil & Tag Symbol inside
    c_y = rf_y + 1.45
    for i in range(3):
        arc = Arc((rf_x + 0.75 + i*0.35, c_y), 0.50, 0.85, angle=0, theta1=0, theta2=180, color='#000000', lw=2.0, zorder=5)
        ax.add_patch(arc)
    ax.plot([rf_x + 0.75, rf_x + 1.45], [c_y, c_y], color='#000000', lw=2.0)
    ax.plot([rf_x + 1.10, rf_x + 1.10], [c_y, c_y - 0.35], color='#000000', lw=2.0)
    ax.text(rf_x + 1.10, c_y - 0.60, "125 kHz Coil", fontsize=9.0, fontweight='bold', ha='center', zorder=10)

    # Transponder Tag Symbol
    ax.add_patch(Rectangle((rf_x + 2.2, c_y - 0.35), 1.45, 0.85, facecolor='#F6F6F6', edgecolor='#000000', lw=1.5, zorder=4))
    ax.text(rf_x + 2.92, c_y + 0.10, "EM4100", fontsize=10.0, fontweight='bold', ha='center', zorder=10)
    ax.text(rf_x + 2.92, c_y - 0.18, "Passive Tag", fontsize=8.5, ha='center', zorder=10)

    ax.text(rf_x + rf_w/2, rf_y + 0.25, "RDM6300 PMOD (9600 bps UART)", fontsize=9.2, fontweight='bold', fontfamily='monospace', ha='center', zorder=10)

    # Direct arrow to rdm_rx at y = 8.8
    draw_open_arrow(rf_x + rf_w, 8.8, chip_x - 0.6, 8.8, size=0.25, lw=1.8)
    ax.text((rf_x + rf_w + chip_x - 0.6)/2, 9.05, "rdm_rx", fontsize=11.5, fontweight='bold', fontfamily='monospace', ha='center', zorder=10)

    # =========================================================================
    # 4. EXTERNAL HARDWARE BLOCK 2: ASM / C PROGRAM (Left Bottom)
    # =========================================================================
    fw_x, fw_y, fw_w, fw_h = 0.8, 3.8, 4.0, 3.0
    ax.add_patch(Rectangle((fw_x, fw_y), fw_w, fw_h, facecolor='#FFFFFF', edgecolor='#000000', lw=2.0, zorder=3))
    ax.text(fw_x + fw_w/2, fw_y + fw_h + 0.24, "ASM/C PROGRAM", fontsize=14.0, fontweight='bold', ha='center', zorder=10)

    ax.text(fw_x + fw_w/2, fw_y + 2.40, "RISC-V Firmware (GCC)", fontsize=11.0, fontweight='bold', color='#222222', ha='center', zorder=10)
    ax.text(fw_x + fw_w/2, fw_y + 1.85, "Toolchain: riscv32-unknown-elf", fontsize=9.2, ha='center', zorder=10)
    ax.text(fw_x + fw_w/2, fw_y + 1.40, "Source: start.s & firmware.c", fontsize=9.2, ha='center', zorder=10)
    ax.text(fw_x + fw_w/2, fw_y + 0.90, "Compiled to firmware.hex (XIP)", fontsize=8.8, fontstyle='italic', ha='center', zorder=10)
    ax.text(fw_x + fw_w/2, fw_y + 0.35, "Reset Vector: 0x0025_0000", fontsize=9.2, fontweight='bold', fontfamily='monospace', ha='center', zorder=10)

    # Direct arrow to boot_vec at y = 7.0
    draw_open_arrow(fw_x + fw_w, 7.0, chip_x - 0.6, 7.0, size=0.25, lw=1.8)
    ax.text((fw_x + fw_w + chip_x - 0.6)/2, 7.25, "boot_vec", fontsize=11.5, fontweight='bold', fontfamily='monospace', ha='center', zorder=10)

    # =========================================================================
    # 5. EXTERNAL HARDWARE BLOCK 3: DISPLAY / SPI NOR FLASH MEMORY (Right Upper-Mid)
    # =========================================================================
    fl_x, fl_y, fl_w, fl_h = 12.8, 6.7, 7.2, 3.8
    ax.add_patch(Rectangle((fl_x, fl_y), fl_w, fl_h, facecolor='#FFFFFF', edgecolor='#000000', lw=2.0, zorder=3))
    ax.text(fl_x + fl_w/2, fl_y + fl_h + 0.24, "SPI NOR FLASH MEMORY", fontsize=14.0, fontweight='bold', ha='center', zorder=10)
    ax.text(fl_x + fl_w/2, fl_y + fl_h - 0.38, "Spansion S25FL032P (4 MBytes / 32 Mbit)", fontsize=11.0, fontweight='bold', color='#333333', ha='center', zorder=10)
    ax.plot([fl_x, fl_x + fl_w], [fl_y + fl_h - 0.65, fl_y + fl_h - 0.65], color='#000000', lw=1.2)

    # Internal Sector Map (like LCD display screen)
    mem_slots = [
        ("Sector 0-36 (0x000000)", "FPGA Bitstream Configuration"),
        ("Sector 37   (0x00250000)", "PicoRV32 Firmware (XIP Execution)"),
        ("Sector 48   (0x00300000)", "Authorized RFID Whitelist Database"),
        ("Sector 49   (0x00310000)", "Non-Volatile Access Logs Database"),
    ]
    sy = fl_y + fl_h - 1.10
    for s_addr, s_desc in mem_slots:
        ax.add_patch(Rectangle((fl_x + 0.45, sy - 0.12), fl_w - 0.90, 0.48, facecolor='#F9F9F9', edgecolor='#CCCCCC', lw=1.0, zorder=4))
        ax.text(fl_x + 0.65, sy + 0.12, s_addr, fontsize=9.2, fontweight='bold', fontfamily='monospace', zorder=10)
        ax.text(fl_x + 3.75, sy + 0.12, s_desc, fontsize=9.2, color='#111111', zorder=10)
        sy -= 0.58

    # Pins on left of Flash connecting directly across to SoC right pins
    spi_signals = [
        (9.7, "/CS", "out"),
        (8.9, "SCK", "out"),
        (8.1, "SI/MOSI", "out"),
        (7.3, "SO/MISO", "in"),
    ]
    for y_pos, fl_sig, direction in spi_signals:
        ax.plot([fl_x - 0.55, fl_x], [y_pos, y_pos], color='#000000', lw=1.8, zorder=4)
        ax.text(fl_x + 0.18, y_pos, fl_sig, fontsize=10.0, fontweight='bold', va='center', ha='left', fontfamily='monospace', zorder=10)
        if direction == "out":
            draw_open_arrow(chip_x + chip_w + 0.6, y_pos, fl_x - 0.55, y_pos, size=0.22, lw=1.8)
        else:
            draw_open_arrow(fl_x - 0.55, y_pos, chip_x + chip_w + 0.6, y_pos, size=0.22, lw=1.8)

    ax.text((chip_x + chip_w + 0.6 + fl_x - 0.55)/2, 10.15, "SPI BUS", fontsize=11.5, fontweight='bold', ha='center', backgroundcolor='#FFFFFF', zorder=10)

    # =========================================================================
    # 6. EXTERNAL HARDWARE BLOCK 4: HOST PC MANAGEMENT CONSOLE (Right Lower-Mid)
    # =========================================================================
    pc_x, pc_y, pc_w, pc_h = 12.8, 4.5, 7.2, 1.8
    ax.add_patch(Rectangle((pc_x, pc_y), pc_w, pc_h, facecolor='#FFFFFF', edgecolor='#000000', lw=2.0, zorder=3))
    ax.text(pc_x + pc_w/2, pc_y + pc_h + 0.24, "HOST PC CONSOLE", fontsize=14.0, fontweight='bold', ha='center', zorder=10)

    ax.text(pc_x + pc_w/2, pc_y + 1.35, "Win32 C Serial App (host/main.c)", fontsize=10.5, fontweight='bold', color='#222222', ha='center', zorder=10)
    ax.text(pc_x + pc_w/2, pc_y + 0.85, "FTDI FT2232 USB-to-UART Bridge (9600 8-N-1)", fontsize=9.2, ha='center', zorder=10)
    ax.text(pc_x + pc_w/2, pc_y + 0.35, "13 Functions: Whitelist, Logs, CSV, Virtual Scan", fontsize=9.0, fontweight='bold', ha='center', zorder=10)

    # UART TX/RX wires:
    # TXD at 5.8 -> input to SoC uart_rx at 5.8
    ax.plot([pc_x - 0.55, pc_x], [5.8, 5.8], color='#000000', lw=1.8, zorder=4)
    ax.text(pc_x + 0.18, 5.8, "TXD", fontsize=10.0, fontweight='bold', va='center', ha='left', fontfamily='monospace', zorder=10)
    draw_open_arrow(pc_x - 0.55, 5.8, chip_x + chip_w + 0.6, 5.8, size=0.22, lw=1.8)

    # RXD at 5.0 <- output from SoC uart_tx at 5.0
    ax.plot([pc_x - 0.55, pc_x], [5.0, 5.0], color='#000000', lw=1.8, zorder=4)
    ax.text(pc_x + 0.18, 5.0, "RXD", fontsize=10.0, fontweight='bold', va='center', ha='left', fontfamily='monospace', zorder=10)
    draw_open_arrow(chip_x + chip_w + 0.6, 5.0, pc_x - 0.55, 5.0, size=0.22, lw=1.8)

    ax.text((chip_x + chip_w + 0.6 + pc_x - 0.55)/2, 5.40, "UART Bus", fontsize=11.5, fontweight='bold', ha='center', backgroundcolor='#FFFFFF', zorder=10)

    # =========================================================================
    # 7. EXTERNAL HARDWARE BLOCK 5: STATUS BUTTON (Bottom Right - Exactly like Reference Image!)
    # =========================================================================
    btn_x, btn_y, btn_w, btn_h = 14.2, 0.8, 4.6, 2.4
    ax.add_patch(Rectangle((btn_x, btn_y), btn_w, btn_h, facecolor='#FFFFFF', edgecolor='#000000', lw=2.0, zorder=3))
    ax.text(btn_x + btn_w/2, btn_y + btn_h + 0.24, "Status Button", fontsize=14.0, fontweight='bold', ha='center', zorder=10)
    draw_switch(btn_x + 2.3, btn_y + 1.35)
    ax.text(btn_x + 2.3, btn_y + 0.65, "Push Button (Manual)", fontsize=10.0, fontweight='bold', ha='center', zorder=10)
    ax.text(btn_x + 2.3, btn_y + 0.28, "Active-Low Reset (rst_n)", fontsize=9.2, fontfamily='monospace', ha='center', zorder=10)

    # Clean orthogonal wire from Status Button to rst_n pin (y=4.1 on SoC right):
    # Exits button terminal (1) at btn_x: routes left along y=2.15 to x=12.4, turns UP to y=4.1, then left into rst_n!
    ax.plot([btn_x, 12.4, 12.4], [btn_y + 1.35, btn_y + 1.35, 4.1], color='#000000', lw=1.8, zorder=4)
    draw_open_arrow(12.4, 4.1, chip_x + chip_w + 0.6, 4.1, size=0.22, lw=1.8)

    # =========================================================================
    # 8. EXTERNAL HARDWARE BLOCK 6: 16 DIAGNOSTIC LEDS (Bottom Center)
    # =========================================================================
    led_x, led_y, led_w, led_h = 4.8, 0.5, 7.8, 2.1
    ax.add_patch(Rectangle((led_x, led_y), led_w, led_h, facecolor='#FFFFFF', edgecolor='#000000', lw=2.0, zorder=3))
    
    # Header inside LED box so wires entering top don't cross any title text:
    ax.text(led_x + led_w/2, led_y + led_h - 0.35, "16 DIAGNOSTIC LEDS (Basys 3 Prototyping Board)", fontsize=11.5, fontweight='bold', ha='center', zorder=10)
    ax.plot([led_x, led_x + led_w], [led_y + led_h - 0.60, led_y + led_h - 0.60], color='#000000', lw=1.2, zorder=4)

    # Plumb aligned LEDs matching SoC bottom pin x-coordinates exactly:
    led_defs = [
        (chip_x + 0.8, "LED[0]\nHeartbeat"),
        (chip_x + 1.8, "LED[1]\nFlash WIP"),
        (chip_x + 2.8, "LED[2]\nTag Strobe"),
        (chip_x + 3.8, "LED[3]\nMatch OK"),
        (chip_x + 4.6, "LED[15:4]\nDiagnostics"),
    ]
    for lx, ltxt in led_defs:
        draw_schematic_led(lx, led_y + 0.95)
        ax.text(lx, led_y + 0.28, ltxt, fontsize=8.8, fontweight='bold', fontfamily='monospace', ha='center', va='center', zorder=10)

    # Connect wires straight down into top of LED box:
    for i, (px, pname) in enumerate(bottom_pins):
        draw_open_arrow(px, chip_y - 0.5, px, led_y + led_h, size=0.18, lw=1.6)

    # Outer border for entire diagram (textbook look)
    ax.add_patch(Rectangle((0.3, 0.2), 20.4, 14.6, facecolor='none', edgecolor='#000000', lw=2.4, zorder=1))

    plt.tight_layout()
    out_path = 'fig1_block_diagram.png'
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print(f"[SUCCESS] Textbook-perfect Figure 1 generated successfully at: {out_path}")

if __name__ == '__main__':
    create_textbook_diagram()
