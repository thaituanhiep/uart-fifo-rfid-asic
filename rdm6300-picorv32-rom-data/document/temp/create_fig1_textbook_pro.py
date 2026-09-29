# -*- coding: utf-8 -*-
"""
Script: create_fig1_textbook_pro.py
Generates an authentic, textbook/academic hardware schematic block diagram matching
the user's reference image style:
- Clean, crisp black-and-white / technical monochrome drawing on pure white background.
- Large, bold, highly legible text (10pt - 14pt).
- Central IC chip symbol (PicoRV32 RISC-V SoC: rdm6300_picorv32_soc) with individual pin stubs,
  pin numbers, and pin labels (clk, resetn, rdm_rx, flash_csb, flash_clk, mosi, miso, uart_rx, uart_tx, led[15:0]).
- External peripheral blocks matching reference image:
  * Power Supply block (5V USB -> Regulators 3.3V & 1.8V -> VDD/GND)
  * Clock & Reset block (50 MHz Oscillator & Push-button Reset)
  * RFID Reader (RDM6300 125 kHz with Antenna Coil) -> rdm_rx
  * Firmware C Program block (RISC-V GCC Toolchain)
  * SPI Flash Memory (S25FL032P 4MB: Whitelist Sector 48, Logs Sector 49, XIP)
  * Host PC Console (C / Win32 Serial) via USB-UART
  * 16 Diagnostic LEDs (Basys 3 Prototyping Board)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon

def generate_hardware_block_diagram():
    # 18 x 13.5 inches at 300 DPI for ultra-sharp academic publication
    fig, ax = plt.subplots(figsize=(18, 13.5), dpi=300)
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 13.5)
    ax.axis('off')

    # Pure white background
    ax.add_patch(Rectangle((0, 0), 18, 13.5, facecolor='#FFFFFF', zorder=0))

    # Helper: draw clean rectangular block with black outline
    def draw_block(x, y, w, h, title="", subtitle="", lw=1.8, facecolor='#FFFFFF'):
        rect = Rectangle((x, y), w, h, facecolor=facecolor, edgecolor='#000000', linewidth=lw, zorder=2)
        ax.add_patch(rect)
        if title:
            # Header line if subtitle exists
            if subtitle:
                ax.text(x + w/2, y + h - 0.35, title, fontsize=11.5, fontweight='bold',
                        color='#000000', ha='center', va='center', fontfamily='sans-serif', zorder=10)
                ax.plot([x, x + w], [y + h - 0.7, y + h - 0.7], color='#000000', lw=1.2, zorder=3)
            else:
                ax.text(x + w/2, y + h/2, title, fontsize=11.5, fontweight='bold',
                        color='#000000', ha='center', va='center', fontfamily='sans-serif', zorder=10)
        return rect

    # Helper: draw pin stub on chip
    def draw_pin_stub(x1, y1, x2, y2, pin_num="", pin_name="", align='left', fs=9.5):
        ax.plot([x1, x2], [y1, y2], color='#000000', lw=1.5, zorder=4)
        if align == 'left': # pin on left of chip, stub goes left
            if pin_num:
                ax.text(x1 + 0.15, y1, str(pin_num), fontsize=8.0, color='#000000', va='center', ha='left', zorder=10)
            if pin_name:
                ax.text(x1 + 0.65, y1, pin_name, fontsize=fs, fontweight='bold', color='#000000', va='center', ha='left', fontfamily='monospace', zorder=10)
        elif align == 'right': # pin on right of chip, stub goes right
            if pin_num:
                ax.text(x1 - 0.15, y1, str(pin_num), fontsize=8.0, color='#000000', va='center', ha='right', zorder=10)
            if pin_name:
                ax.text(x1 - 0.65, y1, pin_name, fontsize=fs, fontweight='bold', color='#000000', va='center', ha='right', fontfamily='monospace', zorder=10)
        elif align == 'bottom':
            if pin_name:
                ax.text(x1, y1 + 0.3, pin_name, fontsize=fs, fontweight='bold', color='#000000', va='bottom', ha='center', fontfamily='monospace', rotation=90, zorder=10)

    # =========================================================================
    # 1. TOP POWER SUPPLY SUBSYSTEM (Like Transformer -> Rectifier -> Regulator)
    # =========================================================================
    # Box 1: 5V DC Input Source
    draw_block(1.0, 11.0, 3.2, 1.8, lw=1.6)
    ax.text(2.6, 12.35, "Power Input", fontsize=11.5, fontweight='bold', ha='center', zorder=10)
    ax.text(2.6, 11.85, "USB 5V DC / Adapter", fontsize=10.0, ha='center', zorder=10)
    ax.text(2.6, 11.35, "+5.0V @ 500mA", fontsize=9.5, fontweight='bold', color='#444444', ha='center', fontfamily='monospace', zorder=10)

    # Arrow to Regulator 1
    ax.annotate("", xy=(5.2, 11.9), xytext=(4.2, 11.9),
                arrowprops=dict(arrowstyle="->", color='#000000', lw=1.8), zorder=5)

    # Box 2: Dual Voltage Regulators (3.3V & 1.8V LDO)
    draw_block(5.2, 10.9, 4.4, 2.0, lw=1.6)
    ax.text(7.4, 12.45, "Voltage Regulators (LDO)", fontsize=11.5, fontweight='bold', ha='center', zorder=10)
    # Regulator schematic box inside
    ax.plot([5.2, 9.6], [12.15, 12.15], color='#000000', lw=1.0)
    ax.text(7.4, 11.75, "3.3V LDO: I/O, Flash & RFID (VDD33)", fontsize=9.5, fontweight='bold', ha='center', zorder=10)
    ax.text(7.4, 11.25, "1.8V LDO: ASIC Core Power (VDD18)", fontsize=9.5, fontweight='bold', ha='center', zorder=10)

    # Power Distribution Rails (Bus wire down to system)
    ax.plot([7.4, 7.4, 8.8], [10.9, 10.2, 10.2], color='#000000', lw=1.5, ls='--')
    ax.annotate("", xy=(8.8, 10.2), xytext=(8.6, 10.2),
                arrowprops=dict(arrowstyle="->", color='#000000', lw=1.5))
    ax.text(8.0, 10.45, "VDD (1.8V / 3.3V)", fontsize=9.0, fontweight='bold', color='#333333', ha='center', zorder=10)

    # Box 3: Clock & Reset Generator (Top-Right)
    draw_block(10.6, 10.9, 6.4, 2.0, lw=1.6)
    ax.text(13.8, 12.45, "Clock & System Reset", fontsize=11.5, fontweight='bold', ha='center', zorder=10)
    ax.plot([10.6, 17.0], [12.15, 12.15], color='#000000', lw=1.0)
    ax.text(13.8, 11.75, "50 MHz Crystal Oscillator (clk - Period: 20.0 ns)", fontsize=9.5, fontweight='bold', ha='center', zorder=10)
    ax.text(13.8, 11.25, "Manual Pushbutton / Power-On Reset (resetn)", fontsize=9.5, fontweight='bold', ha='center', zorder=10)

    # Clock & Reset connections down to SoC
    ax.plot([12.0, 12.0, 10.5], [10.9, 9.8, 9.8], color='#000000', lw=1.5)
    ax.annotate("", xy=(10.5, 9.8), xytext=(10.7, 9.8),
                arrowprops=dict(arrowstyle="->", color='#000000', lw=1.5))
    ax.text(12.0, 10.45, "Clock & Reset Bus", fontsize=9.0, fontweight='bold', ha='center', zorder=10)

    # =========================================================================
    # 2. CENTRAL INTEGRATED CIRCUIT (PicoRV32 RISC-V SoC Chip)
    # =========================================================================
    chip_x, chip_y, chip_w, chip_h = 5.2, 2.4, 5.3, 7.5
    # Outer chip package rectangle
    ax.add_patch(Rectangle((chip_x, chip_y), chip_w, chip_h,
                           facecolor='#FFFFFF', edgecolor='#000000', linewidth=2.4, zorder=2))
    
    # Inner border line (classic IC schematic look like in 8051 reference)
    ax.add_patch(Rectangle((chip_x + 0.45, chip_y + 0.45), chip_w - 0.9, chip_h - 0.9,
                           facecolor='#FFFFFF', edgecolor='#000000', linewidth=1.2, zorder=3))

    # Vertical / Prominent IC Title in Center (like "8051 series MC")
    ax.text(chip_x + chip_w/2, chip_y + chip_h/2 + 0.5,
            "PicoRV32 RISC-V SoC",
            fontsize=15.0, fontweight='bold', color='#000000', ha='center', va='center',
            fontfamily='sans-serif', rotation=90, zorder=10)
    
    ax.text(chip_x + chip_w/2 + 0.65, chip_y + chip_h/2 + 0.5,
            "rdm6300_picorv32_soc",
            fontsize=10.5, fontweight='bold', color='#444444', ha='center', va='center',
            fontfamily='monospace', rotation=90, zorder=10)

    ax.text(chip_x + chip_w/2 - 0.65, chip_y + chip_h/2 + 0.5,
            "SkyWater 130nm ASIC / Basys 3 Demo",
            fontsize=9.0, fontstyle='italic', color='#555555', ha='center', va='center',
            fontfamily='sans-serif', rotation=90, zorder=10)

    # --- LEFT SIDE PINS (Inputs & Power) ---
    left_pins = [
        (9.4, "clk", "W5", "Clock 50MHz"),
        (8.6, "resetn", "U18", "Active-Low Reset"),
        (7.8, "rdm_rx", "J1", "RFID UART Input"),
        (6.8, "VDD_1V8", "Core", "1.8V Core VDD"),
        (6.0, "VDD_3V3", "IO", "3.3V I/O VDD"),
        (5.2, "VSS / GND", "Die", "Common Ground"),
        (4.2, "flashio_reloc", "SRAM", "RAM Code Exec"),
        (3.4, "boot_vec", "0x25", "Reset: 0x0025_0000"),
    ]
    for py, pname, pnum, pdesc in left_pins:
        draw_pin_stub(chip_x, py, chip_x - 0.65, py, pin_num=pnum, pin_name=pname, align='left', fs=9.0)

    # --- RIGHT SIDE PINS (Flash SPI & Host UART & Trap) ---
    right_pins = [
        (9.4, "flash_csb", "L13", "SPI Chip Select (Active Low)"),
        (8.7, "flash_clk", "CCLK", "SPI SCK Clock (STARTUPE2)"),
        (8.0, "flash_io0", "K17", "MOSI (Master Out Slave In)"),
        (7.3, "flash_io1", "K18", "MISO (Master In Slave Out)"),
        (6.3, "uart_rx", "B18", "Host PC UART RX (with FIFO)"),
        (5.6, "uart_tx", "A18", "Host PC UART TX (with FIFO)"),
        (4.7, "trap", "P17", "CPU Error Trap Indicator"),
        (3.8, "irq_event", "Core", "RFID Event IRQ Vector"),
    ]
    for py, pname, pnum, pdesc in right_pins:
        draw_pin_stub(chip_x + chip_w, py, chip_x + chip_w + 0.65, py, pin_num=pnum, pin_name=pname, align='right', fs=9.0)

    # --- BOTTOM PINS (16 Diagnostic LEDs) ---
    bot_pins = [
        (chip_x + 1.0, "led[0]", "Heartbeat 1Hz"),
        (chip_x + 1.8, "led[1]", "Flash Busy (WIP)"),
        (chip_x + 2.6, "led[2]", "Tag Valid Strobe"),
        (chip_x + 3.4, "led[3]", "Scan Result"),
        (chip_x + 4.2, "led[15:4]", "Diagnostics"),
    ]
    for px, pname, pdesc in bot_pins:
        ax.plot([px, px], [chip_y, chip_y - 0.65], color='#000000', lw=1.5, zorder=4)
        ax.text(px, chip_y + 0.25, pname, fontsize=8.5, fontweight='bold', color='#000000',
                va='bottom', ha='center', fontfamily='monospace', rotation=90, zorder=10)

    # =========================================================================
    # 3. EXTERNAL HARDWARE BLOCK 1: RFID READER RDM6300 (Left Middle)
    # =========================================================================
    rf_x, rf_y, rf_w, rf_h = 0.6, 6.2, 3.8, 3.2
    draw_block(rf_x, rf_y, rf_w, rf_h, lw=1.8)
    
    # Header
    ax.text(rf_x + rf_w/2, rf_y + rf_h - 0.35, "RFID READER", fontsize=12.0, fontweight='bold', ha='center', zorder=10)
    ax.text(rf_x + rf_w/2, rf_y + rf_h - 0.65, "RDM6300 (125 kHz PMOD)", fontsize=10.0, fontweight='bold', color='#444444', ha='center', zorder=10)
    ax.plot([rf_x, rf_x + rf_w], [rf_y + rf_h - 0.85, rf_y + rf_h - 0.85], color='#000000', lw=1.2)

    # Antenna Schematic Symbol inside block
    # Coil loops
    for i in range(3):
        arc = patches.Arc((rf_x + 0.8 + i*0.35, rf_y + 1.55), 0.5, 0.9, angle=0, theta1=0, theta2=180, color='#000000', lw=1.6, zorder=4)
        ax.add_patch(arc)
    ax.plot([rf_x + 0.8, rf_x + 1.5], [rf_y + 1.55, rf_y + 1.55], color='#000000', lw=1.6)
    ax.plot([rf_x + 1.15, rf_x + 1.15], [rf_y + 1.55, rf_y + 1.05], color='#000000', lw=1.6)
    ax.text(rf_x + 1.15, rf_y + 0.8, "Coil Antenna\n(125 kHz)", fontsize=8.5, ha='center', zorder=10)

    # Transponder Tag Symbol
    ax.add_patch(Rectangle((rf_x + 2.1, rf_y + 1.1), 1.4, 0.85, facecolor='#F2F2F2', edgecolor='#000000', lw=1.2, zorder=4))
    ax.text(rf_x + 2.8, rf_y + 1.52, "EM4100", fontsize=8.5, fontweight='bold', ha='center', zorder=10)
    ax.text(rf_x + 2.8, rf_y + 1.25, "125 kHz Tag", fontsize=7.5, ha='center', zorder=10)

    # Signal annotation
    ax.text(rf_x + rf_w/2, rf_y + 0.35, "UART 9600 bps (14-Byte ASCII)", fontsize=8.5, fontweight='bold', ha='center', zorder=10)

    # Wire from RFID Reader to SoC rdm_rx
    ax.plot([rf_x + rf_w, chip_x - 0.65], [7.8, 7.8], color='#000000', lw=1.8, zorder=5)
    ax.annotate("", xy=(chip_x - 0.65, 7.8), xytext=(chip_x - 0.85, 7.8),
                arrowprops=dict(arrowstyle="->", color='#000000', lw=1.8), zorder=5)
    ax.text((rf_x + rf_w + chip_x - 0.65)/2, 8.05, "rdm_rx (UART)", fontsize=9.0, fontweight='bold', ha='center', zorder=10)

    # =========================================================================
    # 4. EXTERNAL HARDWARE BLOCK 2: ASM / C FIRMWARE PROGRAM (Left Bottom)
    # =========================================================================
    fw_x, fw_y, fw_w, fw_h = 0.6, 2.5, 3.8, 2.8
    draw_block(fw_x, fw_y, fw_w, fw_h, lw=1.8)
    
    ax.text(fw_x + fw_w/2, fw_y + fw_h - 0.35, "FIRMWARE PROGRAM", fontsize=12.0, fontweight='bold', ha='center', zorder=10)
    ax.text(fw_x + fw_w/2, fw_y + fw_h - 0.65, "RISC-V C & start.s", fontsize=10.0, fontweight='bold', color='#444444', ha='center', zorder=10)
    ax.plot([fw_x, fw_x + fw_w], [fw_y + fw_h - 0.85, fw_y + fw_h - 0.85], color='#000000', lw=1.2)

    ax.text(fw_x + fw_w/2, fw_y + 1.45, "GNU GCC Toolchain\n(riscv32-unknown-elf)", fontsize=9.0, ha='center', zorder=10)
    ax.text(fw_x + fw_w/2, fw_y + 0.85, "Compiled into firmware.hex\nExecuted via Flash XIP", fontsize=8.5, fontstyle='italic', ha='center', zorder=10)
    ax.text(fw_x + fw_w/2, fw_y + 0.35, "Reset Vector: 0x0025_0000", fontsize=8.5, fontweight='bold', fontfamily='monospace', ha='center', zorder=10)

    # Connection from Firmware to Chip boot
    ax.plot([fw_x + fw_w, chip_x - 0.65], [3.4, 3.4], color='#000000', lw=1.8, zorder=5)
    ax.annotate("", xy=(chip_x - 0.65, 3.4), xytext=(chip_x - 0.85, 3.4),
                arrowprops=dict(arrowstyle="->", color='#000000', lw=1.8), zorder=5)

    # =========================================================================
    # 5. EXTERNAL HARDWARE BLOCK 3: SPI NOR FLASH MEMORY (Right Upper-Mid)
    # =========================================================================
    fl_x, fl_y, fl_w, fl_h = 12.0, 6.7, 5.4, 3.5
    draw_block(fl_x, fl_y, fl_w, fl_h, lw=1.8)
    
    ax.text(fl_x + fl_w/2, fl_y + fl_h - 0.35, "SPI NOR FLASH MEMORY", fontsize=12.0, fontweight='bold', ha='center', zorder=10)
    ax.text(fl_x + fl_w/2, fl_y + fl_h - 0.65, "Spansion S25FL032P (4 MBytes / 32 Mbit)", fontsize=9.5, fontweight='bold', color='#444444', ha='center', zorder=10)
    ax.plot([fl_x, fl_x + fl_w], [fl_y + fl_h - 0.85, fl_y + fl_h - 0.85], color='#000000', lw=1.2)

    # Memory Map contents inside Flash block
    mem_slots = [
        ("Sector 0-36 (0x000000)", "FPGA Bitstream Configuration"),
        ("Sector 37 (0x00250000)", "PicoRV32 Firmware (XIP Execution)"),
        ("Sector 48 (0x00300000)", "Authorized RFID Whitelist Database"),
        ("Sector 49 (0x00310000)", "Non-Volatile Access Logs Database"),
    ]
    ms_y = fl_y + fl_h - 1.25
    for s_addr, s_desc in mem_slots:
        ax.add_patch(Rectangle((fl_x + 0.3, ms_y - 0.1), fl_w - 0.6, 0.45, facecolor='#F9F9F9', edgecolor='#CCCCCC', lw=0.8, zorder=3))
        ax.text(fl_x + 0.45, ms_y + 0.12, s_addr, fontsize=8.0, fontweight='bold', fontfamily='monospace', zorder=10)
        ax.text(fl_x + 2.55, ms_y + 0.12, s_desc, fontsize=8.0, color='#222222', zorder=10)
        ms_y -= 0.52

    # SPI 4-wire bus between SoC and Flash
    # We draw 4 clean parallel lines
    bus_y_start = [9.4, 8.7, 8.0, 7.3]
    bus_labels  = ["flash_csb", "flash_clk", "flash_io0 (MOSI)", "flash_io1 (MISO)"]
    for i, by in enumerate(bus_y_start):
        ax.plot([chip_x + chip_w + 0.65, fl_x], [by, by], color='#000000', lw=1.4, zorder=5)
        if i in [0, 1, 2]: # Out from SoC
            ax.annotate("", xy=(fl_x, by), xytext=(fl_x - 0.2, by), arrowprops=dict(arrowstyle="->", color='#000000', lw=1.4))
        else: # In to SoC (MISO)
            ax.annotate("", xy=(chip_x + chip_w + 0.65, by), xytext=(chip_x + chip_w + 0.85, by), arrowprops=dict(arrowstyle="->", color='#000000', lw=1.4))

    # Bus bracket label
    ax.text((chip_x + chip_w + 0.65 + fl_x)/2, 8.9, "SPI BUS (4-wire)", fontsize=8.5, fontweight='bold', ha='center', backgroundcolor='#FFFFFF', zorder=10)

    # =========================================================================
    # 6. EXTERNAL HARDWARE BLOCK 4: HOST PC CONSOLE C (Right Lower-Mid)
    # =========================================================================
    pc_x, pc_y, pc_w, pc_h = 12.0, 3.6, 5.4, 2.7
    draw_block(pc_x, pc_y, pc_w, pc_h, lw=1.8)
    
    ax.text(pc_x + pc_w/2, pc_y + pc_h - 0.35, "HOST PC MANAGEMENT CONSOLE", fontsize=12.0, fontweight='bold', ha='center', zorder=10)
    ax.text(pc_x + pc_w/2, pc_y + pc_h - 0.65, "Win32 C Serial Application (host/main.c)", fontsize=9.5, fontweight='bold', color='#444444', ha='center', zorder=10)
    ax.plot([pc_x, pc_x + pc_w], [pc_y + pc_h - 0.85, pc_y + pc_h - 0.85], color='#000000', lw=1.2)

    ax.text(pc_x + pc_w/2, pc_y + 1.35, "FTDI FT2232 USB-to-UART Bridge (9600 8-N-1)", fontsize=9.0, ha='center', zorder=10)
    ax.text(pc_x + pc_w/2, pc_y + 0.85, "13 Functions: Ping, Add/Delete Tags, Check Tag,", fontsize=8.5, color='#222222', ha='center', zorder=10)
    ax.text(pc_x + pc_w/2, pc_y + 0.40, "Virtual Scan, View Logs, Export/Import CSV", fontsize=8.5, fontweight='bold', color='#222222', ha='center', zorder=10)

    # UART TX/RX wires
    ax.plot([chip_x + chip_w + 0.65, pc_x], [6.3, 6.3], color='#000000', lw=1.4, zorder=5) # uart_rx
    ax.annotate("", xy=(chip_x + chip_w + 0.65, 6.3), xytext=(chip_x + chip_w + 0.85, 6.3), arrowprops=dict(arrowstyle="->", color='#000000', lw=1.4))
    
    ax.plot([chip_x + chip_w + 0.65, pc_x], [5.6, 5.6], color='#000000', lw=1.4, zorder=5) # uart_tx
    ax.annotate("", xy=(pc_x, 5.6), xytext=(pc_x - 0.2, 5.6), arrowprops=dict(arrowstyle="->", color='#000000', lw=1.4))

    ax.text((chip_x + chip_w + 0.65 + pc_x)/2, 6.0, "UART Bus", fontsize=8.5, fontweight='bold', ha='center', backgroundcolor='#FFFFFF', zorder=10)

    # =========================================================================
    # 7. EXTERNAL HARDWARE BLOCK 5: 16 DIAGNOSTIC LEDS & STATUS BUTTON (Bottom)
    # =========================================================================
    # Block for 16 LEDs (Bottom Right)
    led_x, led_y, led_w, led_h = 7.0, 0.4, 7.2, 1.4
    draw_block(led_x, led_y, led_w, led_h, lw=1.8)
    
    ax.text(led_x + led_w/2, led_y + led_h - 0.35, "16 DIAGNOSTIC LEDS (Basys 3 Prototyping Board)", fontsize=11.0, fontweight='bold', ha='center', zorder=10)
    ax.plot([led_x, led_x + led_w], [led_y + led_h - 0.55, led_y + led_h - 0.55], color='#000000', lw=1.0)
    
    # 4 distinct LED status labels inside
    ax.text(led_x + 0.2, led_y + 0.45, "LED[0]: Heartbeat (1Hz)", fontsize=8.5, fontweight='bold', fontfamily='monospace', zorder=10)
    ax.text(led_x + 2.7, led_y + 0.45, "LED[1]: Flash Busy (WIP)", fontsize=8.5, fontweight='bold', fontfamily='monospace', zorder=10)
    ax.text(led_x + 5.2, led_y + 0.45, "LED[2]: Tag Valid Strobe", fontsize=8.5, fontweight='bold', fontfamily='monospace', zorder=10)
    ax.text(led_x + led_w/2, led_y + 0.15, "LED[15:3]: Verification Diagnostics & Self-Test Pattern", fontsize=8.2, fontstyle='italic', ha='center', zorder=10)

    # Bus wire down from SoC to LEDs
    for px, pname, pdesc in bot_pins:
        ax.plot([px, px], [chip_y - 0.65, led_y + led_h], color='#000000', lw=1.4, zorder=5)
        ax.annotate("", xy=(px, led_y + led_h), xytext=(px, led_y + led_h + 0.15),
                    arrowprops=dict(arrowstyle="->", color='#000000', lw=1.4))

    # Block for Status Button (Bottom Left)
    btn_x, btn_y, btn_w, btn_h = 2.0, 0.4, 4.4, 1.4
    draw_block(btn_x, btn_y, btn_w, btn_h, lw=1.8)
    
    ax.text(btn_x + btn_w/2, btn_y + btn_h - 0.35, "Status / Reset Button", fontsize=11.0, fontweight='bold', ha='center', zorder=10)
    ax.plot([btn_x, btn_x + btn_w], [btn_y + btn_h - 0.55, btn_y + btn_h - 0.55], color='#000000', lw=1.0)
    
    # Push button schematic symbol
    pb_cx = btn_x + 1.2
    pb_cy = btn_y + 0.45
    ax.plot([pb_cx - 0.4, pb_cx - 0.15], [pb_cy, pb_cy], color='#000000', lw=1.5)
    ax.plot([pb_cx + 0.15, pb_cx + 0.4], [pb_cy, pb_cy], color='#000000', lw=1.5)
    ax.plot([pb_cx - 0.25, pb_cx + 0.25], [pb_cy + 0.18, pb_cy + 0.18], color='#000000', lw=2.0)
    ax.plot([pb_cx, pb_cx], [pb_cy + 0.18, pb_cy + 0.32], color='#000000', lw=1.5)
    ax.text(btn_x + 2.8, btn_y + 0.35, "Push Button (Manual)\nActive-Low System Reset", fontsize=8.5, ha='center', zorder=10)

    # Wire from button to reset line
    ax.plot([btn_x + btn_w, 4.5, 4.5], [btn_y + btn_h/2, btn_y + btn_h/2, 8.6], color='#000000', lw=1.4)
    ax.annotate("", xy=(chip_x - 0.65, 8.6), xytext=(4.5, 8.6),
                arrowprops=dict(arrowstyle="->", color='#000000', lw=1.4))

    # Outer border for entire diagram (textbook look)
    ax.add_patch(Rectangle((0.3, 0.2), 17.4, 13.0, facecolor='none', edgecolor='#000000', linewidth=2.0, zorder=1))

    plt.tight_layout()
    out_path = 'fig1_block_diagram.png'
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print(f"[SUCCESS] Textbook-style Figure 1 generated successfully at: {out_path}")

if __name__ == '__main__':
    generate_hardware_block_diagram()
