# -*- coding: utf-8 -*-
"""
Script: create_fig1_pro.py
Generates a stunning, publication-grade architectural block diagram for:
"Kiến trúc tổng thể Hệ thống trên Vi mạch (SoC) PicoRV32 RFID RDM6300 với SPI Flash XIP và 1KB Data SRAM"
Styling:
- High technical density, clean orthogonal bus routing, bus width slashes (/32, /4, /1)
- Subunits inside PicoRV32 (PC, RV32I ALU, RegFile 32x32, Microcode FSM, IRQ)
- Detailed MMIO Crossbar Interconnect
- 1KB Data SRAM, SPIMEMIO (Flash XIP), RDM6300 Decoder, Host UART FIFO, GPIO
- Modern semiconductor datasheet aesthetic (curated colors, clear contrast, perfect font proportions)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ArrowStyle

def generate_pro_block_diagram():
    fig, ax = plt.subplots(figsize=(19, 13), dpi=300)
    ax.set_xlim(0, 19)
    ax.set_ylim(0, 13)
    ax.axis('off')

    # Color Palette (High-end Semiconductor Datasheet)
    C_BG_CHIP    = '#FAFAFC'
    C_DIE_BORDER = '#2B3A42'
    
    # Subsystem theme colors: (fill, header, border, text_dark)
    PAL_CPU   = {'fill': '#F0F4F8', 'hdr': '#D9E2EC', 'border': '#102A43', 'accent': '#0B69A3'}
    PAL_MEM   = {'fill': '#E6FFFA', 'hdr': '#B2F5EA', 'border': '#234E52', 'accent': '#00A389'}
    PAL_FLASH = {'fill': '#FAF5FF', 'hdr': '#E9D8FD', 'border': '#44337A', 'accent': '#6B46C1'}
    PAL_RFID  = {'fill': '#F0FFF4', 'hdr': '#C6F6D5', 'border': '#22543D', 'accent': '#2F855A'}
    PAL_BUS   = {'fill': '#FFFAF0', 'hdr': '#FEEBC8', 'border': '#7B341E', 'accent': '#DD6B20'}
    PAL_UART  = {'fill': '#F7FAFC', 'hdr': '#EDF2F7', 'border': '#2D3748', 'accent': '#4A5568'}
    PAL_EXT   = {'fill': '#FFF5F5', 'hdr': '#FED7D7', 'border': '#742A2A', 'accent': '#C53030'}

    # 1. Main SoC Chip Die Boundary
    chip_rect = FancyBboxPatch((1.2, 0.6), 16.6, 11.8,
                               boxstyle="round,pad=0.1,rounding_size=0.3",
                               facecolor=C_BG_CHIP, edgecolor=C_DIE_BORDER, linewidth=2.5, zorder=1)
    ax.add_patch(chip_rect)
    
    # Die Header Title
    ax.text(1.5, 12.05, "SoC DIE BOUNDARY (SkyWater 130nm ASIC: rdm6300_picorv32_soc)", 
            fontsize=11.5, fontweight='bold', color=C_DIE_BORDER, fontfamily='sans-serif')
    ax.text(13.8, 12.05, "Clock: 50 MHz | Power: 1.8V", 
            fontsize=9.5, fontweight='bold', color='#486581', fontfamily='sans-serif')

    # Helper: draw stylized module box
    def draw_box(x, y, w, h, title, pal, badge="", radius=0.15):
        box = FancyBboxPatch((x, y), w, h,
                             boxstyle=f"round,pad=0.04,rounding_size={radius}",
                             facecolor=pal['fill'], edgecolor=pal['border'], linewidth=1.5, zorder=3)
        ax.add_patch(box)
        # Header banner
        hdr_h = 0.52
        hdr = FancyBboxPatch((x, y + h - hdr_h), w, hdr_h,
                             boxstyle=f"round,pad=0.04,rounding_size={radius}",
                             facecolor=pal['hdr'], edgecolor=pal['border'], linewidth=1.5, zorder=4)
        ax.add_patch(hdr)
        # Square bottom of header
        ax.add_patch(patches.Rectangle((x, y + h - hdr_h), w, 0.1, facecolor=pal['hdr'], edgecolor=pal['hdr'], zorder=5))
        
        # Title text
        ax.text(x + w/2, y + h - hdr_h/2, title,
                fontsize=9.5, fontweight='bold', color=pal['border'],
                ha='center', va='center', fontfamily='sans-serif', zorder=6)
        
        if badge:
            # Badge pill on right of header
            ax.text(x + w - 0.15, y + h - hdr_h/2, badge,
                    fontsize=7.0, fontweight='bold', color='white',
                    bbox=dict(boxstyle="round,pad=0.2", facecolor=pal['accent'], edgecolor='none'),
                    ha='right', va='center', fontfamily='sans-serif', zorder=7)

    # Helper: draw internal subunit inside a module
    def draw_sub(x, y, w, h, name, desc="", color='#FFFFFF', border='#718096', fontsize=7.5):
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                              facecolor=color, edgecolor=border, linewidth=0.9, zorder=6)
        ax.add_patch(rect)
        if desc:
            ax.text(x + w/2, y + h*0.62, name, fontsize=fontsize, fontweight='bold', color='#1A202C',
                    ha='center', va='center', fontfamily='sans-serif', zorder=7)
            ax.text(x + w/2, y + h*0.28, desc, fontsize=fontsize-1.2, color='#4A5568',
                    ha='center', va='center', fontfamily='sans-serif', zorder=7)
        else:
            ax.text(x + w/2, y + h/2, name, fontsize=fontsize, fontweight='bold', color='#1A202C',
                    ha='center', va='center', fontfamily='sans-serif', zorder=7)

    # =========================================================================
    # 2. MODULE: PICORV32 RISC-V CPU CORE (Top Left)
    # =========================================================================
    draw_box(1.7, 7.2, 5.0, 4.4, "PicoRV32 CPU CORE (RV32I)", PAL_CPU, badge="RISC-V 32-bit")
    
    # Internal sub-units of CPU
    draw_sub(2.0, 10.1, 2.0, 0.8, "PC & Fetch Logic", "Reset: 0x0025_0000", '#FFFFFF', PAL_CPU['accent'])
    draw_sub(4.3, 10.1, 2.1, 0.8, "Microcode FSM", "Instruction Decoder", '#FFFFFF', PAL_CPU['accent'])
    draw_sub(2.0, 8.9, 2.0, 0.9, "32 x 32-bit RegFile", "x0 - x31 Registers", '#FFFFFF', PAL_CPU['border'])
    draw_sub(4.3, 8.9, 2.1, 0.9, "32-bit ALU / Shifter", "ADD/SUB/XOR/SLT/SLL", '#FFFFFF', PAL_CPU['border'])
    draw_sub(2.0, 7.6, 2.0, 0.9, "IRQ & Trap Handler", "Timer / Card Events", '#FFFFFF', PAL_CPU['border'])
    draw_sub(4.3, 7.6, 2.1, 0.9, "Native Memory I/F", "Handshake Valid/Ready", '#EBF8FF', PAL_CPU['accent'])

    # =========================================================================
    # 3. MODULE: MMIO CROSSBAR & BUS INTERCONNECT (Center-Left Trunk)
    # =========================================================================
    draw_box(7.5, 4.3, 3.8, 7.3, "MMIO BUS INTERCONNECT & DECODER", PAL_BUS, badge="32-bit Crossbar")
    
    # Crossbar decoding slots
    slots = [
        ("0x0000_0000 - 0x0000_03FF", "1KB Data SRAM (sel_sram)", '#E6FFFA', '#234E52'),
        ("0x0010_0000 - 0x00FF_FFFF", "Flash XIP Area (sel_spimem)", '#FAF5FF', '#44337A'),
        ("0x0200_0000", "SPIMEMIO Bit-Bang (sel_spicfg)", '#FAF5FF', '#44337A'),
        ("0x1000_0000 - 0x1000_0008", "RDM6300 RFID Regs (sel_rfid)", '#F0FFF4', '#22543D'),
        ("0x3000_0000 - 0x3000_0004", "Host PC UART (sel_uart)", '#F7FAFC', '#2D3748'),
        ("0x4000_0000", "GPIO & Status LEDs (sel_gpio)", '#FFF5F5', '#742A2A'),
    ]
    slot_y = 10.2
    for addr, desc, c_fill, c_bdr in slots:
        draw_sub(7.8, slot_y, 3.2, 0.82, addr, desc, c_fill, c_bdr, fontsize=7.2)
        slot_y -= 1.05

    # =========================================================================
    # 4. MODULE: 1KB ON-CHIP DATA SRAM (Center Top)
    # =========================================================================
    draw_box(12.2, 9.4, 4.8, 2.2, "1KB ON-CHIP DATA SRAM (data_sram.v)", PAL_MEM, badge="256 x 32-bit")
    draw_sub(12.5, 9.7, 2.0, 1.2, "Single-Cycle RAM", "256 Words x 32-bit\nAddr: 0x0000-0x03FF", '#FFFFFF', PAL_MEM['border'], fontsize=7.2)
    draw_sub(14.8, 9.7, 1.9, 1.2, "Storage Contents", ".data, .bss, Stack\nflashio_worker in RAM", '#FFFFFF', PAL_MEM['border'], fontsize=7.0)

    # Byte-write strobe tag
    ax.text(14.6, 9.45, "wstrb[3:0] (Byte Masking)", fontsize=6.5, color='#234E52', fontweight='bold', ha='center', zorder=7)

    # =========================================================================
    # 5. MODULE: SPIMEMIO FLASH XIP CONTROLLER (Right Upper-Mid)
    # =========================================================================
    draw_box(12.2, 6.7, 4.8, 2.4, "SPI FLASH CONTROLLER (spimemio.v)", PAL_FLASH, badge="XIP Cache Engine")
    draw_sub(12.5, 7.0, 2.0, 1.4, "Flash XIP Engine", "eXecute In Place\nReset: 0x0025_0000\n64-bit Cache Line", '#FFFFFF', PAL_FLASH['border'], fontsize=7.0)
    draw_sub(14.8, 7.0, 1.9, 1.4, "Command FSM", "Read Data (0x03)\nPage Program (0x02)\nSector Erase (0x20)\nWIP Auto-Polling", '#FFFFFF', PAL_FLASH['border'], fontsize=6.8)

    # =========================================================================
    # 6. MODULE: HOST PC UART INTERFACE (Right Lower-Mid)
    # =========================================================================
    draw_box(12.2, 4.2, 4.8, 2.2, "HOST PC UART SUBSYSTEM (simpleuart_fifo.v)", PAL_UART, badge="9600 Baud 8-N-1")
    draw_sub(12.5, 4.5, 2.0, 1.2, "TX Buffer (FIFO)", "16-Depth Sync FIFO\nNon-blocking Transmit", '#FFFFFF', PAL_UART['border'], fontsize=7.0)
    draw_sub(14.8, 4.5, 1.9, 1.2, "RX Buffer (FIFO)", "16-Depth Sync FIFO\nOverflow Protection", '#FFFFFF', PAL_UART['border'], fontsize=7.0)

    # =========================================================================
    # 7. MODULE: RDM6300 RFID HARDWARE SUBSYSTEM (Bottom Wide Branch)
    # =========================================================================
    draw_box(1.7, 1.2, 9.6, 2.6, "RDM6300 RFID DECODER SUBSYSTEM (Hardware Autonomous Pipeline)", PAL_RFID, badge="Zero CPU Overhead")
    
    draw_sub(2.0, 1.5, 1.6, 1.6, "2-FF Sync", "sync_2ff.v\nMetastability\nFilter", '#FFFFFF', PAL_RFID['border'], fontsize=7.0)
    draw_sub(3.9, 1.5, 1.8, 1.6, "UART RX Core", "uart_rx.v\n9600 Baud 8-N-1\nMajority Voter", '#FFFFFF', PAL_RFID['border'], fontsize=7.0)
    draw_sub(6.0, 1.5, 2.8, 1.6, "14-Byte Frame Decoder FSM", "rdm6300_frame_decoder.v\nSTX(0x02) -> 10 Hex -> XOR -> ETX(0x03)\n1-Cycle Parallel Checksum Verify", '#FFFFFF', PAL_RFID['border'], fontsize=7.0)
    draw_sub(9.1, 1.5, 1.9, 1.6, "MMIO Registers", "REG_RFID_STATUS\nREG_RFID_TAG_HI\nREG_RFID_TAG_LO", '#E6FFFA', PAL_RFID['accent'], fontsize=7.0)

    # Pipeline arrow links inside RFID
    ax.annotate("", xy=(3.9, 2.3), xytext=(3.6, 2.3), arrowprops=dict(arrowstyle="->", color=PAL_RFID['accent'], lw=1.5))
    ax.annotate("", xy=(6.0, 2.3), xytext=(5.7, 2.3), arrowprops=dict(arrowstyle="->", color=PAL_RFID['accent'], lw=1.5))
    ax.annotate("", xy=(9.1, 2.3), xytext=(8.8, 2.3), arrowprops=dict(arrowstyle="->", color=PAL_RFID['accent'], lw=1.5))

    # =========================================================================
    # 8. MODULE: GPIO & STATUS LEDS (Bottom Right)
    # =========================================================================
    draw_box(12.2, 1.2, 4.8, 2.6, "GPIO & STATUS LED DRIVER (0x4000_0000)", PAL_EXT, badge="16-Bit Output")
    draw_sub(12.5, 1.5, 4.2, 1.6, "16 Diagnostic LEDs (Basys 3)", 
             "LED[0]: 1Hz Heartbeat Pulse | LED[1]: SPI Flash Busy (WIP)\nLED[2]: RFID Tag Valid Strobe | LED[15:3]: Verification Diagnostics",
             '#FFFFFF', PAL_EXT['border'], fontsize=7.5)

    # =========================================================================
    # 9. EXTERNAL HARDWARE COMPONENTS (Outside Die Boundary)
    # =========================================================================
    # External RFID Reader
    draw_box(0.2, 1.4, 0.8, 2.2, "RFID", PAL_EXT, radius=0.08)
    ax.text(0.6, 2.2, "RDM6300\n125kHz\nReader\n(PMOD)", fontsize=6.8, fontweight='bold', color=PAL_EXT['border'], ha='center', va='center')

    # External Flash Chip
    draw_box(17.9, 6.8, 0.9, 2.2, "FLASH", PAL_FLASH, radius=0.08)
    ax.text(18.35, 7.6, "SPI NOR\nFLASH\nS25FL032P\n(4MB)", fontsize=6.8, fontweight='bold', color=PAL_FLASH['border'], ha='center', va='center')

    # External PC Host
    draw_box(17.9, 4.2, 0.9, 2.2, "HOST", PAL_UART, radius=0.08)
    ax.text(18.35, 5.0, "PC Host\nConsole C\nWin32 COM\n(USB-UART)", fontsize=6.8, fontweight='bold', color=PAL_UART['border'], ha='center', va='center')

    # =========================================================================
    # 10. BUS CONNECTIONS & INTERCONNECT ROUTING (Crisp Orthogonal Lines)
    # =========================================================================
    # CPU -> Crossbar
    ax.annotate("", xy=(7.5, 9.4), xytext=(6.7, 9.4),
                arrowprops=dict(arrowstyle="<->", color='#C05621', lw=2.2))
    ax.text(7.1, 9.6, "mem_bus", fontsize=7.5, fontweight='bold', color='#C05621', ha='center')
    ax.text(7.1, 9.15, "/32 bit", fontsize=6.8, color='#7B341E', ha='center')

    # Crossbar -> 1KB SRAM
    ax.annotate("", xy=(12.2, 10.5), xytext=(11.3, 10.5),
                arrowprops=dict(arrowstyle="<->", color='#234E52', lw=2.0))
    ax.text(11.75, 10.7, "sel_sram", fontsize=7.2, fontweight='bold', color='#234E52', ha='center')
    ax.text(11.75, 10.25, "/32", fontsize=6.5, color='#234E52', ha='center')

    # Crossbar -> SPIMEMIO
    ax.annotate("", xy=(12.2, 7.9), xytext=(11.3, 7.9),
                arrowprops=dict(arrowstyle="<->", color='#553C9A', lw=2.0))
    ax.text(11.75, 8.1, "sel_spimem", fontsize=7.2, fontweight='bold', color='#553C9A', ha='center')
    ax.text(11.75, 7.65, "/32", fontsize=6.5, color='#553C9A', ha='center')

    # Crossbar -> Host UART
    ax.annotate("", xy=(12.2, 5.3), xytext=(11.3, 5.3),
                arrowprops=dict(arrowstyle="<->", color='#2D3748', lw=2.0))
    ax.text(11.75, 5.5, "sel_uart", fontsize=7.2, fontweight='bold', color='#2D3748', ha='center')
    ax.text(11.75, 5.05, "/32", fontsize=6.5, color='#2D3748', ha='center')

    # Crossbar -> GPIO LEDs
    ax.annotate("", xy=(12.2, 2.5), xytext=(11.3, 2.5),
                arrowprops=dict(arrowstyle="->", color='#742A2A', lw=2.0))
    ax.text(11.75, 2.7, "sel_gpio", fontsize=7.2, fontweight='bold', color='#742A2A', ha='center')

    # Crossbar -> RFID Subsystem (Register Read / Write)
    # Downward orthogonal connection
    ax.plot([8.5, 8.5, 9.8, 9.8], [4.3, 4.0, 4.0, 3.8], color='#22543D', lw=1.8, zorder=4)
    ax.annotate("", xy=(9.8, 3.8), xytext=(9.8, 3.9), arrowprops=dict(arrowstyle="->", color='#22543D', lw=1.8))
    ax.text(9.2, 3.9, "sel_rfid (/32)", fontsize=7.0, fontweight='bold', color='#22543D', ha='center')

    # RFID Card Valid Event / Interrupt -> CPU
    ax.plot([10.2, 10.2, 1.9, 1.9], [3.8, 6.4, 6.4, 7.2], color='#C53030', lw=1.6, ls='--', zorder=4)
    ax.annotate("", xy=(1.9, 7.2), xytext=(1.9, 7.0), arrowprops=dict(arrowstyle="->", color='#C53030', lw=1.6))
    ax.text(6.0, 6.55, "card_event_o (Hardware Interrupt Pulse to CPU)", fontsize=7.2, fontweight='bold', color='#C53030', ha='center')

    # External PMOD RX -> 2FF Sync
    ax.annotate("", xy=(1.7, 2.3), xytext=(1.0, 2.3),
                arrowprops=dict(arrowstyle="->", color='#2B6CB0', lw=2.0))
    ax.text(1.35, 2.5, "rdm_rx_i", fontsize=7.0, fontweight='bold', color='#2B6CB0', ha='center')

    # SPIMEMIO -> External SPI Flash (4 physical lines)
    ax.annotate("", xy=(17.9, 7.9), xytext=(17.0, 7.9),
                arrowprops=dict(arrowstyle="<->", color='#6B46C1', lw=2.2))
    ax.text(17.45, 8.1, "SPI BUS", fontsize=7.2, fontweight='bold', color='#6B46C1', ha='center')
    ax.text(17.45, 7.55, "CS, SCK\nMOSI, MISO", fontsize=6.2, color='#44337A', ha='center')

    # Host UART -> External PC
    ax.annotate("", xy=(17.9, 5.3), xytext=(17.0, 5.3),
                arrowprops=dict(arrowstyle="<->", color='#2D3748', lw=2.0))
    ax.text(17.45, 5.5, "UART", fontsize=7.2, fontweight='bold', color='#2D3748', ha='center')
    ax.text(17.45, 5.0, "TX, RX", fontsize=6.5, color='#4A5568', ha='center')

    plt.tight_layout()
    out_path = 'fig1_block_diagram.png'
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"[SUCCESS] Professional Fig 1 generated at: {out_path}")

if __name__ == '__main__':
    generate_pro_block_diagram()
