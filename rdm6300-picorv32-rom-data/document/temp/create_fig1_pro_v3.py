# -*- coding: utf-8 -*-
"""
Script: create_fig1_pro_v3.py
Generates a stunning, publication-grade, semiconductor-datasheet quality architectural block diagram for:
"Kiến trúc tổng thể Hệ thống trên Vi mạch (SoC) PicoRV32 RFID RDM6300 với SPI Flash XIP và 1KB Data SRAM"

Design Highlights:
- Professional semiconductor TRM (Technical Reference Manual) style.
- Perfectly scaled fonts, clear hierarchy, balanced spacing, zero text clipping.
- Clear Central Crossbar Bus Fabric with orthogonal buses, arrows, and width slashes.
- True hardware datapath representation with internal logic blocks, FSMs, and register banks.
- Z-order explicitly managed on all elements so text is never hidden.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, ArrowStyle

def create_figure1():
    fig, ax = plt.subplots(figsize=(21, 14.5), dpi=300)
    ax.set_xlim(0, 21)
    ax.set_ylim(0, 14.5)
    ax.axis('off')

    # Color Palette: High-End Semiconductor Datasheet (Deep blues, slates, crisp accents)
    CLR_BG         = '#F8FAFC'
    CLR_DIE_BG     = '#FFFFFF'
    CLR_DIE_BORDER = '#0F172A'
    
    PAL = {
        'cpu':   {'hdr': '#0F2942', 'hdr_accent': '#2563EB', 'body': '#F0F6FA', 'bdr': '#1E3A8A', 'cell_bg': '#FFFFFF', 'cell_bdr': '#93C5FD'},
        'bus':   {'hdr': '#7C2D12', 'hdr_accent': '#D97706', 'body': '#FFFBEB', 'bdr': '#B45309', 'cell_bg': '#FFFFFF', 'cell_bdr': '#FDE68A'},
        'sram':  {'hdr': '#064E3B', 'hdr_accent': '#059669', 'body': '#ECFDF5', 'bdr': '#047857', 'cell_bg': '#FFFFFF', 'cell_bdr': '#A7F3D0'},
        'flash': {'hdr': '#3B0764', 'hdr_accent': '#7C3AED', 'body': '#F5F3FF', 'bdr': '#6D28D9', 'cell_bg': '#FFFFFF', 'cell_bdr': '#DDD6FE'},
        'rfid':  {'hdr': '#115E59', 'hdr_accent': '#0D9488', 'body': '#F0FDFA', 'bdr': '#0F766E', 'cell_bg': '#FFFFFF', 'cell_bdr': '#99F6E4'},
        'uart':  {'hdr': '#1F2937', 'hdr_accent': '#4B5563', 'body': '#F9FAFB', 'bdr': '#374151', 'cell_bg': '#FFFFFF', 'cell_bdr': '#D1D5DB'},
        'gpio':  {'hdr': '#881337', 'hdr_accent': '#E11D48', 'body': '#FFF1F2', 'bdr': '#BE123C', 'cell_bg': '#FFFFFF', 'cell_bdr': '#FECDD3'},
        'ext':   {'hdr': '#334155', 'hdr_accent': '#64748B', 'body': '#F1F5F9', 'bdr': '#475569', 'cell_bg': '#FFFFFF', 'cell_bdr': '#CBD5E1'}
    }

    # Background canvas tint
    ax.add_patch(Rectangle((0, 0), 21, 14.5, facecolor=CLR_BG, zorder=0))

    # Main SoC Die Boundary
    die_rect = FancyBboxPatch((1.3, 0.7), 17.2, 13.1,
                              boxstyle="round,pad=0.06,rounding_size=0.25",
                              facecolor=CLR_DIE_BG, edgecolor=CLR_DIE_BORDER, linewidth=2.4, zorder=1)
    ax.add_patch(die_rect)

    # Top Die Title Header
    top_bar = FancyBboxPatch((1.3, 13.05), 17.2, 0.75,
                             boxstyle="round,pad=0.04,rounding_size=0.15",
                             facecolor='#0F172A', edgecolor='#0F172A', zorder=2)
    ax.add_patch(top_bar)
    
    ax.text(1.6, 13.42, "SoC DIE ARCHITECTURE: rdm6300_picorv32_soc",
            fontsize=12.0, fontweight='bold', color='#FFFFFF', va='center', fontfamily='sans-serif', zorder=10)
    ax.text(1.6, 13.18, "Target: SkyWater 130nm ASIC (sky130_fd_sc_hd) | Prototype Demo: Digilent Basys 3 (Xilinx Artix-7)",
            fontsize=8.5, color='#94A3B8', va='center', fontfamily='sans-serif', zorder=10)
    ax.text(18.2, 13.42, "Clock: 50 MHz (Period: 20.0 ns) | Sign-off: MET TIMING across 9 Corners",
            fontsize=9.2, fontweight='bold', color='#38BDF8', ha='right', va='center', fontfamily='sans-serif', zorder=10)
    ax.text(18.2, 13.18, "Area: 57,544 Devices | 50,028 Nets | 0 DRC | 0 LVS | 0 Antenna",
            fontsize=8.5, color='#A7F3D0', ha='right', va='center', fontfamily='sans-serif', zorder=10)

    # Helper: draw stylized module box
    def draw_box(x, y, w, h, title, sub_title, pal_key, tag=""):
        p = PAL[pal_key]
        # Main body
        body = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                              facecolor=p['body'], edgecolor=p['bdr'], linewidth=1.3, zorder=3)
        ax.add_patch(body)
        
        # Header banner
        hdr_h = 0.58
        hdr = FancyBboxPatch((x, y + h - hdr_h), w, hdr_h, boxstyle="round,pad=0.02,rounding_size=0.12",
                             facecolor=p['hdr'], edgecolor=p['bdr'], linewidth=1.3, zorder=4)
        ax.add_patch(hdr)
        ax.add_patch(Rectangle((x, y + h - hdr_h), w, 0.1, facecolor=p['hdr'], edgecolor=p['hdr'], zorder=5))
        
        # Title text
        ax.text(x + 0.2, y + h - 0.22, title,
                fontsize=8.8, fontweight='bold', color='#FFFFFF', va='center', fontfamily='sans-serif', zorder=10)
        ax.text(x + 0.2, y + h - 0.44, sub_title,
                fontsize=6.8, color='#94A3B8', va='center', fontfamily='sans-serif', zorder=10)
        
        if tag:
            tag_w = len(tag) * 0.11 + 0.35
            tag_box = FancyBboxPatch((x + w - tag_w - 0.15, y + h - 0.46), tag_w, 0.34,
                                     boxstyle="round,pad=0.02,rounding_size=0.06",
                                     facecolor=p['hdr_accent'], edgecolor='none', zorder=6)
            ax.add_patch(tag_box)
            ax.text(x + w - tag_w/2 - 0.15, y + h - 0.29, tag,
                    fontsize=6.8, fontweight='bold', color='#FFFFFF',
                    ha='center', va='center', fontfamily='sans-serif', zorder=10)

    # Helper: draw internal subunit cell
    def draw_sub(x, y, w, h, title, desc="", pal_key='cpu', fs_t=7.2, fs_d=6.2):
        p = PAL[pal_key]
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                              facecolor=p['cell_bg'], edgecolor=p['cell_bdr'], linewidth=0.8, zorder=6)
        ax.add_patch(rect)
        if desc:
            lines = desc.split('\n')
            total_lines = len(lines) + 1
            ax.text(x + w/2, y + h - 0.22, title, fontsize=fs_t, fontweight='bold', color='#0F172A',
                    ha='center', va='center', fontfamily='sans-serif', zorder=10)
            
            line_y = y + h - 0.46
            for l in lines:
                ax.text(x + w/2, line_y, l, fontsize=fs_d, color='#475569',
                        ha='center', va='center', fontfamily='sans-serif', zorder=10)
                line_y -= 0.20
        else:
            ax.text(x + w/2, y + h/2, title, fontsize=fs_t, fontweight='bold', color='#0F172A',
                    ha='center', va='center', fontfamily='sans-serif', zorder=10)

    # =========================================================================
    # 1. PICORV32 CPU CORE (Top Left)
    # =========================================================================
    draw_box(1.7, 7.8, 5.2, 5.0, "PicoRV32 RISC-V CPU CORE", "rtl/picorv32.v — Claire Wolf", 'cpu', tag="RV32I 32-bit")
    
    draw_sub(1.9, 11.0, 2.3, 1.05, "PC & Fetch Engine", "Reset: 0x0025_0000\nStarts directly via Flash XIP", 'cpu')
    draw_sub(4.4, 11.0, 2.3, 1.05, "Microcode FSM Sequencer", "Multi-cycle State Machine\nArea-optimized RV32I Decoder", 'cpu')
    
    draw_sub(1.9, 9.6, 2.3, 1.25, "Dual-Port Register File", "32 x 32-bit Registers (x0 - x31)\nx0 Hardwired to 0x0000_0000\nx1 (ra), x2 (sp = 0x0400)", 'cpu')
    draw_sub(4.4, 9.6, 2.3, 1.25, "32-bit Integer ALU & Shifter", "ADD, SUB, SLT, SLTU, XOR, OR, AND\nLogical / Arithmetic Barrel Shifter\nSingle-cycle execution", 'cpu')
    
    draw_sub(1.9, 8.05, 2.3, 1.40, "Trap & Interrupt Engine", "q_irq[31:0] Hardware Vector\nExternal RFID Event Strobe (IRQ)\ntimer_irq / cycle / instr counters", 'cpu')
    draw_sub(4.4, 8.05, 2.3, 1.40, "Native Memory Bus Master", "Handshake: mem_valid / mem_ready\nmem_addr[31:0] Byte Address\nmem_wstrb[3:0] Byte Enable Mask", 'cpu')

    # =========================================================================
    # 2. SYSTEM BUS INTERCONNECT & CROSSBAR (Center-Left Column)
    # =========================================================================
    draw_box(7.5, 4.4, 4.4, 8.4, "MMIO BUS CROSSBAR FABRIC", "Crossbar Switch & Address Decoder", 'bus', tag="32-bit MMIO")
    
    # Crossbar decoding slots
    slots = [
        ("0x0000_0000 - 0x0000_03FF", "1KB On-Chip Data SRAM (sel_sram)\n256 Words x 32-bit (Single-Cycle Read/Write)", 'sram'),
        ("0x0010_0000 - 0x00FF_FFFF", "SPI Flash XIP Area (sel_spimem)\n15MB Code Space (Reset Vector: 0x0025_0000)", 'flash'),
        ("0x0200_0000", "SPIMEMIO Bit-Bang Reg (sel_spicfg)\nDirect SPI Pin Control (Ghi/Xóa Flash)", 'flash'),
        ("0x1000_0000 - 0x1000_0008", "RDM6300 RFID Regs (sel_rfid)\nSTATUS(0x00), TAG_HI(0x04), TAG_LO(0x08)", 'rfid'),
        ("0x3000_0000 - 0x3000_0004", "Host PC UART with FIFOs (sel_uart)\nBAUD_DIV(0x00), DATA_REG(0x04)", 'uart'),
        ("0x4000_0000", "GPIO & Diagnostic LEDs (sel_gpio)\n16-bit Status Output Register", 'gpio'),
    ]
    slot_y = 11.45
    for addr_range, desc, p_key in slots:
        draw_sub(7.7, slot_y, 4.0, 0.95, addr_range, desc, p_key, fs_t=7.2, fs_d=6.0)
        slot_y -= 1.15

    # Crossbar Internal Logic summary cell
    draw_sub(7.7, 4.6, 4.0, 0.70, "Address Decoder & Read Data Mux Logic", "mem_addr[31:24] Combinational Decode | mem_ready Aggregator", 'bus', fs_t=6.8, fs_d=5.8)

    # =========================================================================
    # 3. 1KB ON-CHIP DATA SRAM (Top Right)
    # =========================================================================
    draw_box(12.5, 10.3, 5.7, 2.5, "1KB ON-CHIP DATA SRAM SUBSYSTEM", "rtl/data_sram.v — 256 Words x 32-bit", 'sram', tag="1024 Bytes")
    draw_sub(12.7, 10.55, 2.6, 1.55, "Synchronous Single-Cycle RAM Core", "Single-cycle synchronous read/write\nmem_wstrb[3:0] Byte Enable Masking\nArea: Macro-efficient logic gates\nZero wait-state (ready asserted next cycle)", 'sram', fs_t=7.0, fs_d=5.8)
    draw_sub(15.45, 10.55, 2.6, 1.55, "Firmware Memory Allocations", "0x0000 - 0x00FF: .data (Init globals)\n0x0100 - 0x01FF: .bss (Zero globals)\n0x0200 - 0x02FF: flashio_worker in RAM\n0x0400: Stack Top (sp initial value)", 'sram', fs_t=7.0, fs_d=5.8)

    # =========================================================================
    # 4. SPI FLASH CONTROLLER & XIP CACHE ENGINE (Middle Right)
    # =========================================================================
    draw_box(12.5, 7.3, 5.7, 2.7, "SPI FLASH CONTROLLER & XIP CACHE", "rtl/spimemio.v — Flash Memory Subsystem", 'flash', tag="XIP Cache")
    draw_sub(12.7, 7.55, 2.6, 1.75, "Flash XIP Engine & Cache Line", "eXecute-In-Place from SPI Flash\n64-bit Read Prefetch Cache Line Buffer\nLow instruction latency on sequential fetch\nDirect execution without external RAM copy", 'flash', fs_t=7.0, fs_d=5.8)
    draw_sub(15.45, 7.55, 2.6, 1.75, "SPI Command & WIP Polling FSM", "Read Data (0x03) | Page Program (0x02)\nSector Erase 64KB (0x20 / 0xD8)\nRead Status Reg (0x05) | Write Enable (0x06)\nHardware Auto-Polling WIP (Bit 0) busy flag", 'flash', fs_t=7.0, fs_d=5.8)

    # =========================================================================
    # 5. HOST PC UART SUBSYSTEM (Lower Right)
    # =========================================================================
    draw_box(12.5, 4.4, 5.7, 2.6, "HOST PC UART SUBSYSTEM WITH FIFOs", "rtl/simpleuart_fifo.v — 9600 Baud 8-N-1", 'uart', tag="Dual FIFO")
    draw_sub(12.7, 4.65, 2.6, 1.65, "16-Entry TX FIFO Buffer", "sync_fifo.v (16 x 8-bit depth)\nNon-blocking CPU character transmission\nAutomatic TX shift-out serialization\nPrevents CPU stalls during string output", 'uart', fs_t=7.0, fs_d=5.8)
    draw_sub(15.45, 4.65, 2.6, 1.65, "16-Entry RX FIFO Buffer", "sync_fifo.v (16 x 8-bit depth)\nBuffers host PC commands continuously\nOverflow & Underflow flag protection\nBaud Rate Divider: 50MHz / 9600 = 5208", 'uart', fs_t=7.0, fs_d=5.8)

    # =========================================================================
    # 6. RDM6300 RFID AUTONOMOUS HARDWARE ENGINE (Bottom Wide Block)
    # =========================================================================
    draw_box(1.7, 1.0, 10.2, 3.1, "RDM6300 RFID AUTONOMOUS HARDWARE ENGINE", "rtl/rdm6300_frame_decoder.v — Hardware Protocol Pipeline", 'rfid', tag="Zero CPU Overhead")
    
    draw_sub(1.9, 1.3, 1.7, 2.1, "2-FF CDC Sync", "sync_2ff.v\nClock: 50 MHz\nMetastability Filter\nDouble-stage flipflop\nMTBF > 1000 years", 'rfid', fs_t=6.8, fs_d=5.8)
    draw_sub(3.8, 1.3, 2.0, 2.1, "UART RX Core", "uart_rx.v\nBaud: 9600 bps 8-N-1\nDiv: 5208 clock cycles\n16x Oversampling\n3-Point Majority Voter", 'rfid', fs_t=6.8, fs_d=5.8)
    draw_sub(6.0, 1.3, 3.4, 2.1, "14-Byte Frame Decoder FSM", "rdm6300_frame_decoder.v\nST_WAIT_STX (0x02) -> ST_DATA (10 Hex ASCII)\n1-Cycle Parallel Combinational XOR Checksum\nST_WAIT_ETX (0x03) -> ST_VALIDATE\n10 ms Watchdog Timeout Counter (anti-hang)", 'rfid', fs_t=6.8, fs_d=5.8)
    draw_sub(9.6, 1.3, 2.1, 2.1, "MMIO Output Regs", "0x1000_0000: STATUS\n0x1000_0004: TAG_HI (Ver)\n0x1000_0008: TAG_LO (UID)\ncard_valid Strobe (W1C)", 'rfid', fs_t=6.8, fs_d=5.8)

    # Pipeline arrow flow inside RFID module
    ax.annotate("", xy=(3.8, 2.35), xytext=(3.6, 2.35), arrowprops=dict(arrowstyle="->", color=PAL['rfid']['hdr_accent'], lw=1.8), zorder=10)
    ax.annotate("", xy=(6.0, 2.35), xytext=(5.8, 2.35), arrowprops=dict(arrowstyle="->", color=PAL['rfid']['hdr_accent'], lw=1.8), zorder=10)
    ax.annotate("", xy=(9.6, 2.35), xytext=(9.4, 2.35), arrowprops=dict(arrowstyle="->", color=PAL['rfid']['hdr_accent'], lw=1.8), zorder=10)

    # =========================================================================
    # 7. GPIO & DIAGNOSTIC STATUS DRIVER (Bottom Right)
    # =========================================================================
    draw_box(12.5, 1.0, 5.7, 3.1, "GPIO & DIAGNOSTIC STATUS DRIVER", "0x4000_0000 — 16-Bit Output Register", 'gpio', tag="16 LEDs")
    draw_sub(12.7, 1.3, 5.3, 2.1, "16 Diagnostic LED Outputs (Basys 3 Prototyping Platform)",
             "LED[0]: 1 Hz Heartbeat Pulse (Continuous CPU Activity Confirmation)\n"
             "LED[1]: SPI Flash Busy Strobe (High during Flash Page Program / Sector Erase)\n"
             "LED[2]: RFID Tag Valid Strobe (Pulses High upon Verified Card Checksum Match)\n"
             "LED[15:3]: Hardware Verification & Self-Test Diagnostic Status Indicators\n"
             "Drive: 3.3V LVCMOS I/O buffers driving on-board active-high LEDs",
             'gpio', fs_t=7.2, fs_d=6.0)

    # =========================================================================
    # 8. EXTERNAL CHIP PADS & HARDWARE MODULES (Outside Die)
    # =========================================================================
    # External RFID Reader
    draw_box(0.2, 1.2, 0.95, 2.7, "RFID", "125 kHz", 'ext')
    ax.text(0.675, 2.2, "RDM6300\n125 kHz\nEM4100\nReader\n(PMOD)", fontsize=6.8, fontweight='bold', color='#1E293B', ha='center', va='center', zorder=10)

    # External Flash Chip
    draw_box(18.9, 7.3, 1.05, 2.7, "FLASH", "4 MBytes", 'flash')
    ax.text(19.42, 8.35, "SPI NOR\nFLASH\nS25FL032P\n4 MBytes\n(32 Mbit)", fontsize=6.8, fontweight='bold', color=PAL['flash']['hdr'], ha='center', va='center', zorder=10)

    # External Host PC
    draw_box(18.9, 4.4, 1.05, 2.6, "HOST", "USB-COM", 'uart')
    ax.text(19.42, 5.4, "Host PC\nConsole C\nWin32 API\n(USB-UART\nFT2232)", fontsize=6.8, fontweight='bold', color='#1F2937', ha='center', va='center', zorder=10)

    # External LED array
    draw_box(18.9, 1.2, 1.05, 2.7, "LEDS", "Basys 3", 'gpio')
    ax.text(19.42, 2.2, "16 LEDs\n(Basys 3\nBoard)", fontsize=6.8, fontweight='bold', color=PAL['gpio']['hdr'], ha='center', va='center', zorder=10)

    # =========================================================================
    # 9. SYSTEM BUS & INTERCONNECT ROUTING (Crisp Orthogonal Lines)
    # =========================================================================
    # CPU -> MMIO Crossbar
    ax.annotate("", xy=(7.5, 10.3), xytext=(6.9, 10.3),
                arrowprops=dict(arrowstyle="<->", color=PAL['bus']['bdr'], lw=2.6), zorder=15)
    ax.text(7.2, 10.6, "mem_bus", fontsize=7.8, fontweight='bold', color=PAL['bus']['hdr'], ha='center', zorder=15)
    ax.text(7.2, 10.05, "32-bit", fontsize=6.8, color=PAL['bus']['hdr'], ha='center', zorder=15)

    # Crossbar -> 1KB SRAM
    ax.annotate("", xy=(12.5, 11.5), xytext=(11.9, 11.5),
                arrowprops=dict(arrowstyle="<->", color=PAL['sram']['bdr'], lw=2.2), zorder=15)
    ax.text(12.2, 11.75, "sel_sram", fontsize=7.2, fontweight='bold', color=PAL['sram']['hdr'], ha='center', zorder=15)
    ax.text(12.2, 11.25, "/32", fontsize=6.5, color=PAL['sram']['hdr'], ha='center', zorder=15)

    # Crossbar -> SPIMEMIO
    ax.annotate("", xy=(12.5, 8.6), xytext=(11.9, 8.6),
                arrowprops=dict(arrowstyle="<->", color=PAL['flash']['bdr'], lw=2.2), zorder=15)
    ax.text(12.2, 8.85, "sel_spimem", fontsize=7.2, fontweight='bold', color=PAL['flash']['hdr'], ha='center', zorder=15)
    ax.text(12.2, 8.35, "/32", fontsize=6.5, color=PAL['flash']['hdr'], ha='center', zorder=15)

    # Crossbar -> Host UART
    ax.annotate("", xy=(12.5, 5.7), xytext=(11.9, 5.7),
                arrowprops=dict(arrowstyle="<->", color=PAL['uart']['bdr'], lw=2.2), zorder=15)
    ax.text(12.2, 5.95, "sel_uart", fontsize=7.2, fontweight='bold', color=PAL['uart']['hdr'], ha='center', zorder=15)
    ax.text(12.2, 5.45, "/32", fontsize=6.5, color=PAL['uart']['hdr'], ha='center', zorder=15)

    # Crossbar -> GPIO LEDs
    ax.annotate("", xy=(12.5, 2.5), xytext=(11.9, 2.5),
                arrowprops=dict(arrowstyle="->", color=PAL['gpio']['bdr'], lw=2.2), zorder=15)
    ax.text(12.2, 2.75, "sel_gpio", fontsize=7.2, fontweight='bold', color=PAL['gpio']['hdr'], ha='center', zorder=15)
    ax.text(12.2, 2.25, "/32", fontsize=6.5, color=PAL['gpio']['hdr'], ha='center', zorder=15)

    # Crossbar -> RFID Subsystem MMIO bus tap
    ax.plot([8.5, 8.5, 10.3, 10.3], [4.4, 4.2, 4.2, 4.1], color=PAL['rfid']['bdr'], lw=1.8, zorder=15)
    ax.annotate("", xy=(10.3, 4.1), xytext=(10.3, 4.2), arrowprops=dict(arrowstyle="->", color=PAL['rfid']['bdr'], lw=1.8), zorder=15)
    ax.text(9.4, 4.3, "sel_rfid (/32)", fontsize=6.8, fontweight='bold', color=PAL['rfid']['hdr'], ha='center', zorder=15)

    # RFID Card Event IRQ -> CPU (Routed cleanly along the bottom and up left margin)
    ax.plot([2.5, 2.5, 1.5, 1.5, 2.5, 2.5], [4.1, 4.3, 4.3, 7.6, 7.6, 7.8], color='#DC2626', lw=1.6, ls='--', zorder=15)
    ax.annotate("", xy=(2.5, 7.8), xytext=(2.4, 7.8), arrowprops=dict(arrowstyle="->", color='#DC2626', lw=1.6), zorder=15)
    ax.text(1.35, 6.0, "card_event_o (CPU IRQ Pulse)", fontsize=6.8, fontweight='bold', color='#DC2626', rotation=90, va='center', zorder=15)

    # External PMOD RX -> 2FF Sync (Input Pad)
    ax.annotate("", xy=(1.7, 2.35), xytext=(1.15, 2.35),
                arrowprops=dict(arrowstyle="->", color='#2563EB', lw=2.0), zorder=15)
    ax.text(1.42, 2.55, "rdm_rx", fontsize=6.8, fontweight='bold', color='#2563EB', ha='center', zorder=15)

    # SPIMEMIO -> External SPI Flash (4 physical lines)
    ax.annotate("", xy=(18.9, 8.6), xytext=(18.2, 8.6),
                arrowprops=dict(arrowstyle="<->", color=PAL['flash']['bdr'], lw=2.2), zorder=15)
    ax.text(18.55, 8.85, "SPI BUS", fontsize=7.2, fontweight='bold', color=PAL['flash']['hdr'], ha='center', zorder=15)
    ax.text(18.55, 8.2, "CS_N, SCK\nMOSI, MISO", fontsize=6.0, color=PAL['flash']['hdr'], ha='center', zorder=15)

    # Host UART -> External PC
    ax.annotate("", xy=(18.9, 5.7), xytext=(18.2, 5.7),
                arrowprops=dict(arrowstyle="<->", color=PAL['uart']['bdr'], lw=2.0), zorder=15)
    ax.text(18.55, 5.95, "UART", fontsize=7.2, fontweight='bold', color=PAL['uart']['hdr'], ha='center', zorder=15)
    ax.text(18.55, 5.45, "TX, RX", fontsize=6.2, color=PAL['uart']['hdr'], ha='center', zorder=15)

    # GPIO -> External Basys 3 LEDs
    ax.annotate("", xy=(18.9, 2.5), xytext=(18.2, 2.5),
                arrowprops=dict(arrowstyle="->", color=PAL['gpio']['bdr'], lw=2.0), zorder=15)
    ax.text(18.55, 2.75, "LED[15:0]", fontsize=7.2, fontweight='bold', color=PAL['gpio']['hdr'], ha='center', zorder=15)
    ax.text(18.55, 2.25, "/16", fontsize=6.2, color=PAL['gpio']['hdr'], ha='center', zorder=15)

    plt.tight_layout()
    out_path = 'fig1_block_diagram.png'
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor=CLR_BG)
    plt.close()
    print(f"[SUCCESS] Figure 1 v3 generated successfully at: {out_path}")

if __name__ == '__main__':
    create_figure1()
