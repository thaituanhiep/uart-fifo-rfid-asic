# -*- coding: utf-8 -*-
"""
Script: create_fig1_pro_v2.py
Generates a publication-grade, semiconductor-datasheet quality architectural block diagram for:
"Kiến trúc tổng thể Hệ thống trên Vi mạch (SoC) PicoRV32 RFID RDM6300 với SPI Flash XIP và 1KB Data SRAM"

Design Highlights:
- High technical elegance: Crisp architectural hierarchy, subtle drop shadows / borders, clean typography.
- Professional semiconductor styling: Distinct system bus crossbar with address decoding logic, bus widths (/32, /4, /1).
- PicoRV32 Internal Datapath: PC & Fetch, Microcode Decoder FSM, 32x32 RegFile, 32-bit ALU/Shifter, Interrupt Controller.
- 1KB Data SRAM: 256 x 32-bit single-cycle synchronous RAM, Byte-write masks, memory sections (.data, .bss, stack, flashio_worker).
- SPIMEMIO Flash Controller: 64-bit XIP Cache line, SPI Command FSM, Hardware Auto-WIP Polling.
- Hardware RDM6300 Decoder: 2-FF Sync, UART RX 9600, Autonomous 14-byte FSM, Combinational XOR, MMIO registers.
- Host PC UART with 16-entry Sync FIFOs (TX/RX).
- GPIO & Diagnostic LED controller.
- SkyWater 130nm I/O Pad Boundary with 31 pins and external peripherals (RDM6300 PMOD, SPI NOR Flash, Host PC).
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, Polygon
import numpy as np

def create_figure1():
    # Large canvas for high resolution and clean proportions
    fig, ax = plt.subplots(figsize=(20, 13.5), dpi=300)
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 13.5)
    ax.axis('off')

    # Color Palette: Modern Semiconductor / High-End EDA Tool Palette
    CLR_CANVAS_BG  = '#F8FAFC'
    CLR_DIE_BG     = '#FFFFFF'
    CLR_DIE_BORDER = '#1E293B'
    
    # Subsystem Palettes (Header BG, Body BG, Border, Accent/Text)
    PAL = {
        'cpu':   {'hdr': '#1E3A8A', 'hdr_text': '#FFFFFF', 'body': '#F0F7FF', 'bdr': '#1D4ED8', 'sub_bg': '#FFFFFF', 'sub_bdr': '#93C5FD'},
        'bus':   {'hdr': '#B45309', 'hdr_text': '#FFFFFF', 'body': '#FFFBEB', 'bdr': '#D97706', 'sub_bg': '#FFFFFF', 'sub_bdr': '#FDE68A'},
        'sram':  {'hdr': '#065F46', 'hdr_text': '#FFFFFF', 'body': '#ECFDF5', 'bdr': '#059669', 'sub_bg': '#FFFFFF', 'sub_bdr': '#A7F3D0'},
        'flash': {'hdr': '#5B21B6', 'hdr_text': '#FFFFFF', 'body': '#F5F3FF', 'bdr': '#7C3AED', 'sub_bg': '#FFFFFF', 'sub_bdr': '#DDD6FE'},
        'rfid':  {'hdr': '#0F766E', 'hdr_text': '#FFFFFF', 'body': '#F0FDFA', 'bdr': '#0D9488', 'sub_bg': '#FFFFFF', 'sub_bdr': '#99F6E4'},
        'uart':  {'hdr': '#374151', 'hdr_text': '#FFFFFF', 'body': '#F9FAFB', 'bdr': '#4B5563', 'sub_bg': '#FFFFFF', 'sub_bdr': '#D1D5DB'},
        'gpio':  {'hdr': '#9F1239', 'hdr_text': '#FFFFFF', 'body': '#FFF1F2', 'bdr': '#E11D48', 'sub_bg': '#FFFFFF', 'sub_bdr': '#FECDD3'},
        'ext':   {'hdr': '#475569', 'hdr_text': '#FFFFFF', 'body': '#F1F5F9', 'bdr': '#64748B', 'sub_bg': '#FFFFFF', 'sub_bdr': '#CBD5E1'}
    }

    # Background canvas tint
    bg_rect = Rectangle((0, 0), 20, 13.5, facecolor=CLR_CANVAS_BG, zorder=0)
    ax.add_patch(bg_rect)

    # 1. Main SoC Chip Die Boundary (ASIC SkyWater 130nm)
    die = FancyBboxPatch((1.4, 0.7), 16.2, 12.1,
                         boxstyle="round,pad=0.08,rounding_size=0.25",
                         facecolor=CLR_DIE_BG, edgecolor=CLR_DIE_BORDER, linewidth=2.2, zorder=1)
    ax.add_patch(die)

    # Die Header / Title Block
    title_bar = FancyBboxPatch((1.4, 12.15), 16.2, 0.65,
                               boxstyle="round,pad=0.04,rounding_size=0.15",
                               facecolor='#1E293B', edgecolor='#1E293B', zorder=2)
    ax.add_patch(title_bar)
    ax.text(1.7, 12.47, "SoC DIE ARCHITECTURE: rdm6300_picorv32_soc (SkyWater 130nm ASIC / OpenLane 2)", 
            fontsize=11.5, fontweight='bold', color='#FFFFFF', va='center', fontfamily='sans-serif')
    ax.text(17.3, 12.47, "Clock: 50 MHz | Core VDD: 1.8V | I/O: 3.3V | Cells: 57,544", 
            fontsize=9.2, fontweight='bold', color='#94A3B8', ha='right', va='center', fontfamily='sans-serif')

    # Helper: draw stylized subsystem block with professional header & badge
    def draw_module(x, y, w, h, title, pal_key, badge=""):
        p = PAL[pal_key]
        # Main body
        body = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.03,rounding_size=0.14",
                              facecolor=p['body'], edgecolor=p['bdr'], linewidth=1.4, zorder=3)
        ax.add_patch(body)
        
        # Header banner
        hdr_h = 0.50
        hdr = FancyBboxPatch((x, y + h - hdr_h), w, hdr_h, boxstyle="round,pad=0.03,rounding_size=0.14",
                             facecolor=p['hdr'], edgecolor=p['bdr'], linewidth=1.4, zorder=4)
        ax.add_patch(hdr)
        # Flatten bottom corners of header
        ax.add_patch(Rectangle((x, y + h - hdr_h), w, 0.12, facecolor=p['hdr'], edgecolor=p['hdr'], zorder=5))
        
        # Header text
        title_x = x + 0.25 if badge else x + w/2
        ha_align = 'left' if badge else 'center'
        ax.text(title_x, y + h - hdr_h/2, title,
                fontsize=9.2, fontweight='bold', color=p['hdr_text'],
                ha=ha_align, va='center', fontfamily='sans-serif', zorder=6)
        
        if badge:
            # Badge pill on right side of header
            badge_box = FancyBboxPatch((x + w - 1.7, y + h - hdr_h + 0.08), 1.55, hdr_h - 0.16,
                                       boxstyle="round,pad=0.02,rounding_size=0.08",
                                       facecolor='#FFFFFF', edgecolor='none', zorder=6)
            ax.add_patch(badge_box)
            ax.text(x + w - 0.925, y + h - hdr_h/2, badge,
                    fontsize=7.2, fontweight='bold', color=p['hdr'],
                    ha='center', va='center', fontfamily='sans-serif', zorder=7)

    # Helper: draw internal sub-block
    def draw_cell(x, y, w, h, title, subtitle="", pal_key='cpu', fs_title=7.5, fs_sub=6.5):
        p = PAL[pal_key]
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                              facecolor=p['sub_bg'], edgecolor=p['sub_bdr'], linewidth=0.9, zorder=6)
        ax.add_patch(rect)
        if subtitle:
            ax.text(x + w/2, y + h*0.62, title, fontsize=fs_title, fontweight='bold', color='#0F172A',
                    ha='center', va='center', fontfamily='sans-serif', zorder=7)
            ax.text(x + w/2, y + h*0.28, subtitle, fontsize=fs_sub, color='#475569',
                    ha='center', va='center', fontfamily='sans-serif', zorder=7)
        else:
            ax.text(x + w/2, y + h/2, title, fontsize=fs_title, fontweight='bold', color='#0F172A',
                    ha='center', va='center', fontfamily='sans-serif', zorder=7)

    # =========================================================================
    # 2. PICORV32 CPU CORE (Top Left)
    # =========================================================================
    draw_module(1.8, 7.3, 5.0, 4.6, "PicoRV32 RISC-V CPU CORE (rtl/picorv32.v)", 'cpu', badge="RV32I Core")
    
    # Internal sub-units inside PicoRV32
    draw_cell(2.0, 10.3, 2.2, 0.9, "PC & Instruction Fetch", "Reset Vector: 0x0025_0000", 'cpu')
    draw_cell(4.4, 10.3, 2.2, 0.9, "Microcode FSM Sequencer", "Instruction Decoder (RV32I)", 'cpu')
    
    draw_cell(2.0, 9.1, 2.2, 1.0, "Register File (x0 - x31)", "32 x 32-bit Dual-Port Registers", 'cpu')
    draw_cell(4.4, 9.1, 2.2, 1.0, "32-bit ALU & Barrel Shifter", "ADD, SUB, XOR, SLT, SLL, SRA", 'cpu')
    
    draw_cell(2.0, 7.7, 2.2, 1.15, "Trap & Interrupt Engine", "External RFID Event IRQ\nCycle & Instr Counters", 'cpu', fs_sub=6.0)
    draw_cell(4.4, 7.7, 2.2, 1.15, "Native Memory Bus Master", "mem_valid / mem_ready\nmem_addr[31:0], wstrb[3:0]", 'cpu', fs_sub=6.0)

    # =========================================================================
    # 3. MMIO CROSSBAR & BUS INTERCONNECT (Center-Left Trunk)
    # =========================================================================
    draw_module(7.4, 4.3, 3.9, 7.6, "SYSTEM BUS INTERCONNECT (MMIO Crossbar)", 'bus', badge="32-bit Bus")
    
    # Crossbar decoding slots
    slots = [
        ("0x0000_0000 - 0x0000_03FF", "1KB On-Chip SRAM (sel_sram)", 'sram'),
        ("0x0010_0000 - 0x00FF_FFFF", "Flash XIP Cached Area (sel_spimem)", 'flash'),
        ("0x0200_0000", "SPIMEMIO Bit-Bang Reg (sel_spicfg)", 'flash'),
        ("0x1000_0000 - 0x1000_0008", "RDM6300 RFID Dec Regs (sel_rfid)", 'rfid'),
        ("0x3000_0000 - 0x3000_0004", "Host PC UART with FIFO (sel_uart)", 'uart'),
        ("0x4000_0000", "GPIO & Diagnostic LEDs (sel_gpio)", 'gpio')
    ]
    curr_y = 10.45
    for addr_range, desc, p_key in slots:
        draw_cell(7.6, curr_y, 3.5, 0.85, addr_range, desc, p_key, fs_title=7.2, fs_sub=6.3)
        curr_y -= 1.08

    # Bottom interconnect logic note
    draw_cell(7.6, 4.5, 3.5, 0.55, "Address Decoder & Read Mux", "Combinational Select & Wait-state Gen", 'bus', fs_title=6.8, fs_sub=5.8)

    # =========================================================================
    # 4. 1KB ON-CHIP DATA SRAM (Top Right)
    # =========================================================================
    draw_module(12.0, 9.6, 5.2, 2.3, "1KB ON-CHIP DATA SRAM (rtl/data_sram.v)", 'sram', badge="256 x 32-bit")
    draw_cell(12.2, 9.85, 2.4, 1.45, "Synchronous Single-Cycle RAM", "256 Words x 32-bit (1024 Bytes)\nSingle-cycle Read/Write Access\nmem_wstrb[3:0] Byte Enable Mask", 'sram', fs_title=7.2, fs_sub=6.2)
    draw_cell(14.7, 9.85, 2.3, 1.45, "Memory Space Layout", "0x000: .data / 0x100: .bss\n0x200: flashio_worker (RAM)\n0x400: Stack Top (sp = 0x400)", 'sram', fs_title=7.2, fs_sub=6.2)

    # =========================================================================
    # 5. SPI FLASH CONTROLLER & XIP CACHE (Right Upper-Mid)
    # =========================================================================
    draw_module(12.0, 6.9, 5.2, 2.4, "SPI FLASH CONTROLLER (rtl/spimemio.v)", 'flash', badge="XIP Cache Engine")
    draw_cell(12.2, 7.15, 2.4, 1.55, "Flash XIP Engine", "eXecute In Place (0x0025_0000)\n64-bit Read Cache Line Buffer\nPrefetch Hit / Low Latency", 'flash', fs_title=7.2, fs_sub=6.2)
    draw_cell(14.7, 7.15, 2.3, 1.55, "SPI Command & WIP FSM", "Read Data (0x03) | Page Prog (0x02)\nSector Erase (0x20) | Read Reg (0x05)\nHardware Auto WIP Polling", 'flash', fs_title=7.2, fs_sub=6.0)

    # =========================================================================
    # 6. HOST PC UART SUBSYSTEM (Right Lower-Mid)
    # =========================================================================
    draw_module(12.0, 4.3, 5.2, 2.3, "HOST PC UART SUBSYSTEM (rtl/simpleuart_fifo.v)", 'uart', badge="9600 Baud 8-N-1")
    draw_cell(12.2, 4.55, 2.4, 1.45, "16-Entry TX FIFO Buffer", "sync_fifo.v (16 x 8-bit)\nNon-blocking CPU Transmission\nDirect Shift Register Transmit", 'uart', fs_title=7.2, fs_sub=6.2)
    draw_cell(14.7, 4.55, 2.3, 1.45, "16-Entry RX FIFO Buffer", "sync_fifo.v (16 x 8-bit)\nContinuous Command Buffering\nOverflow / Underflow Protection", 'uart', fs_title=7.2, fs_sub=6.2)

    # =========================================================================
    # 7. RDM6300 RFID HARDWARE SUBSYSTEM (Bottom Left to Mid)
    # =========================================================================
    draw_module(1.8, 1.1, 9.5, 2.8, "RDM6300 RFID HARDWARE SUBSYSTEM (rtl/rdm6300_frame_decoder.v)", 'rfid', badge="Autonomous Engine")
    
    draw_cell(2.0, 1.4, 1.6, 1.9, "2-FF CDC Sync", "sync_2ff.v\nClock: 50 MHz\nMetastability Filter\nMTBF > 1000 yrs", 'rfid', fs_title=7.0, fs_sub=5.8)
    draw_cell(3.8, 1.4, 1.9, 1.9, "UART RX Core", "uart_rx.v\nBaud: 9600 bps\nDiv: 5208 cycles\n3-Point Majority Vote", 'rfid', fs_title=7.0, fs_sub=5.8)
    draw_cell(5.9, 1.4, 2.9, 1.9, "14-Byte Frame Decoder FSM", "rdm6300_frame_decoder.v\nDetect STX (0x02) -> 10 Hex ASCII\n1-Cycle Parallel XOR Checksum Engine\nDetect ETX (0x03) | 10ms Timeout WDT", 'rfid', fs_title=7.0, fs_sub=5.8)
    draw_cell(9.0, 1.4, 2.1, 1.9, "MMIO Output Regs", "0x1000_0000: STATUS\n0x1000_0004: TAG_HI\n0x1000_0008: TAG_LO\ncard_valid (W1C Strobe)", 'rfid', fs_title=7.0, fs_sub=5.8)

    # Internal pipeline arrows within RFID module
    ax.annotate("", xy=(3.8, 2.35), xytext=(3.6, 2.35), arrowprops=dict(arrowstyle="->", color=PAL['rfid']['hdr'], lw=1.6))
    ax.annotate("", xy=(5.9, 2.35), xytext=(5.7, 2.35), arrowprops=dict(arrowstyle="->", color=PAL['rfid']['hdr'], lw=1.6))
    ax.annotate("", xy=(9.0, 2.35), xytext=(8.8, 2.35), arrowprops=dict(arrowstyle="->", color=PAL['rfid']['hdr'], lw=1.6))

    # =========================================================================
    # 8. GPIO & STATUS LED DRIVER (Bottom Right)
    # =========================================================================
    draw_module(12.0, 1.1, 5.2, 2.8, "GPIO & DIAGNOSTIC STATUS DRIVER (0x4000_0000)", 'gpio', badge="16-Bit Output")
    draw_cell(12.2, 1.4, 4.8, 1.9, "16 Diagnostic LED Outputs (Basys 3 Prototyping)",
              "LED[0]: 1 Hz Heartbeat Pulse (CPU Operational Strobe)\n"
              "LED[1]: SPI Flash Busy Flag (WIP Active - Programming / Erasing)\n"
              "LED[2]: RFID Tag Valid Strobe (Card Successfully Decoded)\n"
              "LED[15:3]: Hardware Verification & Self-Test Diagnostic Status",
              'gpio', fs_title=7.5, fs_sub=6.5)

    # =========================================================================
    # 9. EXTERNAL CHIP PADS & HARDWARE MODULES (Outside Die)
    # =========================================================================
    # External RFID Reader
    draw_module(0.2, 1.3, 0.95, 2.4, "RFID", 'ext')
    ax.text(0.675, 2.3, "RDM6300\n125 kHz\nEM4100\nReader\n(PMOD)", fontsize=6.8, fontweight='bold', color='#1E293B', ha='center', va='center')

    # External Flash Chip
    draw_module(18.0, 6.9, 1.0, 2.4, "FLASH", 'flash')
    ax.text(18.5, 7.9, "SPI NOR\nFLASH\nS25FL032P\n4 MBytes\n(32 Mbit)", fontsize=6.8, fontweight='bold', color=PAL['flash']['hdr'], ha='center', va='center')

    # External Host PC
    draw_module(18.0, 4.3, 1.0, 2.3, "HOST", 'uart')
    ax.text(18.5, 5.2, "Host PC\nConsole C\nWin32 API\n(USB-UART\nFT2232)", fontsize=6.8, fontweight='bold', color='#1F2937', ha='center', va='center')

    # =========================================================================
    # 10. SYSTEM BUS & INTERCONNECT ROUTING (Crisp Orthogonal Lines)
    # =========================================================================
    # CPU -> MMIO Crossbar
    ax.annotate("", xy=(7.4, 9.6), xytext=(6.8, 9.6),
                arrowprops=dict(arrowstyle="<->", color=PAL['bus']['bdr'], lw=2.4))
    ax.text(7.1, 9.85, "mem_bus", fontsize=7.6, fontweight='bold', color=PAL['bus']['hdr'], ha='center')
    ax.text(7.1, 9.35, "32-bit", fontsize=6.8, color=PAL['bus']['hdr'], ha='center')

    # Crossbar -> 1KB SRAM
    ax.annotate("", xy=(12.0, 10.7), xytext=(11.3, 10.7),
                arrowprops=dict(arrowstyle="<->", color=PAL['sram']['bdr'], lw=2.2))
    ax.text(11.65, 10.95, "sel_sram", fontsize=7.2, fontweight='bold', color=PAL['sram']['hdr'], ha='center')
    ax.text(11.65, 10.45, "/32", fontsize=6.5, color=PAL['sram']['hdr'], ha='center')

    # Crossbar -> SPIMEMIO
    ax.annotate("", xy=(12.0, 8.1), xytext=(11.3, 8.1),
                arrowprops=dict(arrowstyle="<->", color=PAL['flash']['bdr'], lw=2.2))
    ax.text(11.65, 8.35, "sel_spimem", fontsize=7.2, fontweight='bold', color=PAL['flash']['hdr'], ha='center')
    ax.text(11.65, 7.85, "/32", fontsize=6.5, color=PAL['flash']['hdr'], ha='center')

    # Crossbar -> Host UART
    ax.annotate("", xy=(12.0, 5.4), xytext=(11.3, 5.4),
                arrowprops=dict(arrowstyle="<->", color=PAL['uart']['bdr'], lw=2.2))
    ax.text(11.65, 5.65, "sel_uart", fontsize=7.2, fontweight='bold', color=PAL['uart']['hdr'], ha='center')
    ax.text(11.65, 5.15, "/32", fontsize=6.5, color=PAL['uart']['hdr'], ha='center')

    # Crossbar -> GPIO LEDs
    ax.annotate("", xy=(12.0, 2.5), xytext=(11.3, 2.5),
                arrowprops=dict(arrowstyle="->", color=PAL['gpio']['bdr'], lw=2.2))
    ax.text(11.65, 2.75, "sel_gpio", fontsize=7.2, fontweight='bold', color=PAL['gpio']['hdr'], ha='center')
    ax.text(11.65, 2.25, "/32", fontsize=6.5, color=PAL['gpio']['hdr'], ha='center')

    # Crossbar -> RFID Subsystem MMIO bus tap
    ax.plot([8.2, 8.2, 9.5, 9.5], [4.3, 4.0, 4.0, 3.9], color=PAL['rfid']['bdr'], lw=1.8, zorder=5)
    ax.annotate("", xy=(9.5, 3.9), xytext=(9.5, 4.0), arrowprops=dict(arrowstyle="->", color=PAL['rfid']['bdr'], lw=1.8))
    ax.text(8.85, 4.12, "sel_rfid (/32)", fontsize=6.8, fontweight='bold', color=PAL['rfid']['hdr'], ha='center')

    # RFID Card Event IRQ -> CPU (Routed cleanly along the bottom and up left)
    ax.plot([2.5, 2.5, 1.6, 1.6, 2.5, 2.5], [3.9, 4.1, 4.1, 7.1, 7.1, 7.3], color='#DC2626', lw=1.6, ls='--', zorder=5)
    ax.annotate("", xy=(2.5, 7.3), xytext=(2.4, 7.3), arrowprops=dict(arrowstyle="->", color='#DC2626', lw=1.6))
    ax.text(1.9, 5.6, "card_event_o (CPU IRQ Pulse)", fontsize=6.8, fontweight='bold', color='#DC2626', rotation=90, va='center')

    # External PMOD RX -> 2FF Sync (Input Pad)
    ax.annotate("", xy=(1.8, 2.35), xytext=(1.15, 2.35),
                arrowprops=dict(arrowstyle="->", color='#2563EB', lw=2.0))
    ax.text(1.48, 2.55, "rdm_rx", fontsize=6.8, fontweight='bold', color='#2563EB', ha='center')

    # SPIMEMIO -> External SPI Flash (4 physical lines)
    ax.annotate("", xy=(18.0, 8.1), xytext=(17.2, 8.1),
                arrowprops=dict(arrowstyle="<->", color=PAL['flash']['bdr'], lw=2.2))
    ax.text(17.6, 8.35, "SPI BUS", fontsize=7.2, fontweight='bold', color=PAL['flash']['hdr'], ha='center')
    ax.text(17.6, 7.7, "CS_N, SCK\nMOSI, MISO", fontsize=6.0, color=PAL['flash']['hdr'], ha='center')

    # Host UART -> External PC
    ax.annotate("", xy=(18.0, 5.4), xytext=(17.2, 5.4),
                arrowprops=dict(arrowstyle="<->", color=PAL['uart']['bdr'], lw=2.0))
    ax.text(17.6, 5.65, "UART", fontsize=7.2, fontweight='bold', color=PAL['uart']['hdr'], ha='center')
    ax.text(17.6, 5.15, "TX, RX", fontsize=6.2, color=PAL['uart']['hdr'], ha='center')

    # GPIO -> External Basys 3 LEDs
    ax.annotate("", xy=(18.0, 2.5), xytext=(17.2, 2.5),
                arrowprops=dict(arrowstyle="->", color=PAL['gpio']['bdr'], lw=2.0))
    ax.text(17.6, 2.75, "LED[15:0]", fontsize=7.2, fontweight='bold', color=PAL['gpio']['hdr'], ha='center')
    ax.text(17.6, 2.25, "/16", fontsize=6.2, color=PAL['gpio']['hdr'], ha='center')

    # External LED box on right
    draw_module(18.0, 1.4, 1.0, 2.2, "LEDS", 'gpio')
    ax.text(18.5, 2.3, "16 LEDs\n(Basys 3\nBoard)", fontsize=6.8, fontweight='bold', color=PAL['gpio']['hdr'], ha='center', va='center')

    plt.tight_layout()
    out_path = 'fig1_block_diagram.png'
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor=CLR_CANVAS_BG)
    plt.close()
    print(f"[SUCCESS] Figure 1 v2 generated successfully at: {out_path}")

if __name__ == '__main__':
    create_figure1()
