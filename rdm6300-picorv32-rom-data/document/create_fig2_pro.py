# -*- coding: utf-8 -*-
"""
Script: create_fig2_pro.py
Generates a stunning, publication-grade architectural pipeline diagram for:
"Đường ống thu nhận và giải mã phần cứng thẻ RFID RDM6300 (rdm6300_frame_decoder.v)" (Hình 2)
Styling:
- Detailed multi-stage hardware pipeline with timing and register structures
- 14-Byte Frame Format Breakdown diagram with real card example
- FSM state transitions & parallel XOR checksum verification
- MMIO register bitfields
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

def generate_pro_rdm6300_diagram():
    fig, ax = plt.subplots(figsize=(19, 13), dpi=300)
    ax.set_xlim(0, 19)
    ax.set_ylim(0, 13)
    ax.axis('off')

    # Color Palette (Crisp High-Tech Engineering)
    PAL_BG    = '#F8FAFC'
    PAL_FRAME = {'fill': '#EFF6FF', 'hdr': '#DBEAFE', 'border': '#1E40AF', 'accent': '#3B82F6'}
    PAL_SYNC  = {'fill': '#F0FDF4', 'hdr': '#DCFCE7', 'border': '#166534', 'accent': '#22C55E'}
    PAL_UART  = {'fill': '#FEFCE8', 'hdr': '#FEF9C3', 'border': '#854D0E', 'accent': '#EAB308'}
    PAL_FSM   = {'fill': '#FAF5FF', 'hdr': '#F3E8FF', 'border': '#6B21A8', 'accent': '#A855F7'}
    PAL_REG   = {'fill': '#FDF2F8', 'hdr': '#FCE7F3', 'border': '#9D174D', 'accent': '#EC4899'}
    PAL_BUS   = {'fill': '#F1F5F9', 'hdr': '#E2E8F0', 'border': '#334155', 'accent': '#64748B'}

    # Main outer boundary
    main_box = FancyBboxPatch((0.8, 0.6), 17.4, 11.8,
                              boxstyle="round,pad=0.1,rounding_size=0.25",
                              facecolor=PAL_BG, edgecolor='#1E293B', linewidth=2.2, zorder=1)
    ax.add_patch(main_box)
    
    # Title Banner
    ax.text(1.2, 12.05, "RDM6300 RFID HARDWARE DECODING PIPELINE & TIMING ARCHITECTURE",
            fontsize=11.5, fontweight='bold', color='#0F172A', fontfamily='sans-serif')
    ax.text(14.0, 12.05, "Autonomous Hardware Engine | Zero CPU Overhead",
            fontsize=9.0, fontweight='bold', color='#475569', fontfamily='sans-serif')

    def draw_stage(x, y, w, h, title, pal, badge="", radius=0.12):
        box = FancyBboxPatch((x, y), w, h,
                             boxstyle=f"round,pad=0.04,rounding_size={radius}",
                             facecolor=pal['fill'], edgecolor=pal['border'], linewidth=1.4, zorder=3)
        ax.add_patch(box)
        hdr_h = 0.48
        hdr = FancyBboxPatch((x, y + h - hdr_h), w, hdr_h,
                             boxstyle=f"round,pad=0.04,rounding_size={radius}",
                             facecolor=pal['hdr'], edgecolor=pal['border'], linewidth=1.4, zorder=4)
        ax.add_patch(hdr)
        ax.add_patch(patches.Rectangle((x, y + h - hdr_h), w, 0.08, facecolor=pal['hdr'], edgecolor=pal['hdr'], zorder=5))
        
        ax.text(x + w/2, y + h - hdr_h/2, title,
                fontsize=8.8, fontweight='bold', color=pal['border'],
                ha='center', va='center', fontfamily='sans-serif', zorder=6)
        if badge:
            ax.text(x + w - 0.12, y + h - hdr_h/2, badge,
                    fontsize=6.5, fontweight='bold', color='white',
                    bbox=dict(boxstyle="round,pad=0.18", facecolor=pal['accent'], edgecolor='none'),
                    ha='right', va='center', fontfamily='sans-serif', zorder=7)

    def draw_sub(x, y, w, h, name, desc="", color='#FFFFFF', border='#94A3B8', fontsize=7.2):
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                              facecolor=color, edgecolor=border, linewidth=0.8, zorder=6)
        ax.add_patch(rect)
        if desc:
            ax.text(x + w/2, y + h*0.62, name, fontsize=fontsize, fontweight='bold', color='#0F172A',
                    ha='center', va='center', fontfamily='sans-serif', zorder=7)
            ax.text(x + w/2, y + h*0.28, desc, fontsize=fontsize-1.2, color='#475569',
                    ha='center', va='center', fontfamily='sans-serif', zorder=7)
        else:
            ax.text(x + w/2, y + h/2, name, fontsize=fontsize, fontweight='bold', color='#0F172A',
                    ha='center', va='center', fontfamily='sans-serif', zorder=7)

    # =========================================================================
    # PART A: TOP HORIZONTAL PIPELINE FLOW (5 Sequential Stages)
    # =========================================================================
    # Stage 1: RF Front-End & Physical Tag
    draw_stage(1.2, 7.2, 3.0, 4.4, "STAGE 1: RF FRONT-END", PAL_FRAME, badge="125 kHz")
    draw_sub(1.4, 10.1, 2.6, 0.9, "EM4100 Transponder", "125 kHz Passive Tag\nManchester Encoding", '#FFFFFF', PAL_FRAME['border'])
    draw_sub(1.4, 8.8, 2.6, 1.1, "Coil Antenna & Demod", "Inductive Coupling\nAnalog Frontend", '#FFFFFF', PAL_FRAME['border'])
    draw_sub(1.4, 7.5, 2.6, 1.1, "UART TTL Output", "9600 Baud, 8-N-1\nTX Pin -> PMOD JA1", '#DBEAFE', PAL_FRAME['accent'])

    # Stage 2: 2-FF Synchronizer (CDC)
    draw_stage(4.6, 7.2, 2.7, 4.4, "STAGE 2: CDC SYNC", PAL_SYNC, badge="sync_2ff.v")
    draw_sub(4.8, 9.8, 2.3, 1.2, "FF1 (First Stage)", "Captures async pin\nClock: 50 MHz sys_clk", '#FFFFFF', PAL_SYNC['border'])
    draw_sub(4.8, 8.3, 2.3, 1.2, "FF2 (Second Stage)", "Resolves metastability\nMTBF > 1000 years", '#FFFFFF', PAL_SYNC['border'])
    draw_sub(4.8, 7.5, 2.3, 0.65, "Output: rdm_rx_sync", "Clean 50MHz Domain Signal", '#DCFCE7', PAL_SYNC['accent'], fontsize=6.8)

    # Stage 3: UART Receiver Core
    draw_stage(7.7, 7.2, 3.2, 4.4, "STAGE 3: UART RX CORE", PAL_UART, badge="uart_rx.v")
    draw_sub(7.9, 10.1, 2.8, 0.9, "Baud Clock Divider", "Div = 50,000,000 / 9600\n= 5208 Clock Cycles", '#FFFFFF', PAL_UART['border'])
    draw_sub(7.9, 8.8, 2.8, 1.1, "16x Oversampling", "Center 3-Point Majority\nVoter (Filters Glitches)", '#FFFFFF', PAL_UART['border'])
    draw_sub(7.9, 7.5, 2.8, 1.1, "Byte Deserializer", "Shift Reg -> byte_data[7:0]\nStrobe: byte_valid (1 cycle)", '#FEF9C3', PAL_UART['accent'])

    # Stage 4: 14-Byte Frame Decoder FSM
    draw_stage(11.3, 7.2, 3.8, 4.4, "STAGE 4: FRAME DECODER FSM", PAL_FSM, badge="rdm6300_decoder")
    draw_sub(11.5, 10.1, 3.4, 0.9, "FSM State Controller", "WAIT_STX -> COLLECT -> VALIDATE", '#FFFFFF', PAL_FSM['border'])
    draw_sub(11.5, 8.8, 3.4, 1.1, "Hex Nibble Converter", "ascii_hex_to_nibble function\nConverts '0'-'9','A'-'F' to 4-bit", '#FFFFFF', PAL_FSM['border'])
    draw_sub(11.5, 7.5, 3.4, 1.1, "Hardware XOR Checksum", "D[0]^D[1]^D[2]^D[3]^D[4] == CS\n1-Cycle Parallel Verification", '#F3E8FF', PAL_FSM['accent'])

    # Stage 5: Output MMIO Registers
    draw_stage(15.5, 7.2, 2.4, 4.4, "STAGE 5: REGISTERS", PAL_REG, badge="MMIO")
    draw_sub(15.7, 10.0, 2.0, 1.0, "REG_RFID_STATUS", "Addr: 0x1000_0000\nBit 0: card_valid (W1C)\nBit 1: cs_error", '#FFFFFF', PAL_REG['border'], fontsize=6.8)
    draw_sub(15.7, 8.7, 2.0, 1.0, "REG_RFID_TAG_HI", "Addr: 0x1000_0004\n[39:32] Version Byte", '#FFFFFF', PAL_REG['border'], fontsize=6.8)
    draw_sub(15.7, 7.4, 2.0, 1.0, "REG_RFID_TAG_LO", "Addr: 0x1000_0008\n[31:0] Serial Number", '#FCE7F3', PAL_REG['accent'], fontsize=6.8)

    # Inter-stage arrows
    ax.annotate("", xy=(4.6, 9.4), xytext=(4.2, 9.4), arrowprops=dict(arrowstyle="->", color='#1E40AF', lw=2.0))
    ax.text(4.4, 9.65, "rdm_rx_i", fontsize=6.8, fontweight='bold', color='#1E40AF', ha='center')

    ax.annotate("", xy=(7.7, 9.4), xytext=(7.3, 9.4), arrowprops=dict(arrowstyle="->", color='#166534', lw=2.0))
    ax.text(7.5, 9.65, "rdm_rx_sync", fontsize=6.5, fontweight='bold', color='#166534', ha='center')

    ax.annotate("", xy=(11.3, 9.4), xytext=(10.9, 9.4), arrowprops=dict(arrowstyle="->", color='#854D0E', lw=2.0))
    ax.text(11.1, 9.75, "byte_data[7:0]", fontsize=6.5, fontweight='bold', color='#854D0E', ha='center')
    ax.text(11.1, 9.2, "byte_valid", fontsize=6.2, color='#854D0E', ha='center')

    ax.annotate("", xy=(15.5, 9.4), xytext=(15.1, 9.4), arrowprops=dict(arrowstyle="->", color='#6B21A8', lw=2.0))
    ax.text(15.3, 9.75, "tag_raw[39:0]", fontsize=6.5, fontweight='bold', color='#6B21A8', ha='center')
    ax.text(15.3, 9.2, "card_valid", fontsize=6.2, color='#6B21A8', ha='center')

    # Event output arrow from MMIO to CPU
    ax.annotate("", xy=(18.0, 8.2), xytext=(17.9, 8.2), arrowprops=dict(arrowstyle="->", color='#9D174D', lw=2.0))
    ax.text(18.0, 8.5, "card_event_o\n(CPU IRQ)", fontsize=6.5, fontweight='bold', color='#9D174D', ha='left')

    # =========================================================================
    # PART B: BOTTOM SECTION: 14-BYTE FRAME FORMAT & XOR CHECK-ENGINE
    # =========================================================================
    frame_box = FancyBboxPatch((1.2, 1.0), 16.7, 5.7,
                               boxstyle="round,pad=0.06,rounding_size=0.18",
                               facecolor='#FFFFFF', edgecolor='#334155', linewidth=1.5, zorder=3)
    ax.add_patch(frame_box)

    # Header of Section B
    ax.text(1.5, 6.35, "RDM6300 14-BYTE SERIAL FRAME BREAKDOWN & PARALLEL XOR CHECKSUM FORMULA",
            fontsize=9.8, fontweight='bold', color='#0F172A', fontfamily='sans-serif')

    # Visual 14-Byte Frame Grid
    # Total width: 16.0 inches across, split into 14 slots
    slots_def = [
        ("Byte 0\nHeader", "STX\n0x02", '#E2E8F0', 1.0),
        ("Byte 1\nVersion[7:4]", "ASCII\n'0' (0x30)", '#DBEAFE', 1.15),
        ("Byte 2\nVersion[3:0]", "ASCII\n'0' (0x30)", '#DBEAFE', 1.15),
        ("Byte 3\nData[31:28]", "ASCII\n'0' (0x30)", '#D1FAE5', 1.15),
        ("Byte 4\nData[27:24]", "ASCII\n'0' (0x30)", '#D1FAE5', 1.15),
        ("Byte 5\nData[23:20]", "ASCII\n'7' (0x37)", '#D1FAE5', 1.15),
        ("Byte 6\nData[19:16]", "ASCII\n'2' (0x32)", '#D1FAE5', 1.15),
        ("Byte 7\nData[15:12]", "ASCII\n'9' (0x39)", '#D1FAE5', 1.15),
        ("Byte 8\nData[11:8]", "ASCII\n'3' (0x33)", '#D1FAE5', 1.15),
        ("Byte 9\nData[7:4]", "ASCII\n'F' (0x46)", '#D1FAE5', 1.15),
        ("Byte 10\nData[3:0]", "ASCII\n'0' (0x30)", '#D1FAE5', 1.15),
        ("Byte 11\nCS[7:4]", "ASCII\n'F' (0x46)", '#FCE7F3', 1.15),
        ("Byte 12\nCS[3:0]", "ASCII\n'0' (0x30)", '#FCE7F3', 1.15),
        ("Byte 13\nFooter", "ETX\n0x03", '#E2E8F0', 1.0),
    ]

    curr_x = 1.45
    for title, val, c_fill, w in slots_def:
        rect = FancyBboxPatch((curr_x, 4.6), w, 1.4, boxstyle="round,pad=0.02,rounding_size=0.06",
                              facecolor=c_fill, edgecolor='#475569', linewidth=1.0, zorder=4)
        ax.add_patch(rect)
        ax.text(curr_x + w/2, 5.65, title, fontsize=6.5, color='#334155', ha='center', va='center', fontweight='bold')
        ax.text(curr_x + w/2, 4.95, val, fontsize=7.2, color='#0F172A', ha='center', va='center', fontfamily='monospace')
        curr_x += w + 0.08

    # Brackets & Category Annotations under frame
    # STX
    ax.annotate("", xy=(1.45, 4.45), xytext=(2.45, 4.45), arrowprops=dict(arrowstyle="-", color='#475569', lw=1.2))
    ax.text(1.95, 4.25, "Start of Text", fontsize=6.5, ha='center', color='#475569')

    # Version (Bytes 1-2)
    ax.annotate("", xy=(2.53, 4.45), xytext=(4.83, 4.45), arrowprops=dict(arrowstyle="-", color='#1D4ED8', lw=1.2))
    ax.text(3.68, 4.25, "Byte 0 (Version: 0x00)", fontsize=6.8, ha='center', color='#1D4ED8', fontweight='bold')

    # 32-bit Serial (Bytes 3-10)
    ax.annotate("", xy=(4.91, 4.45), xytext=(14.75, 4.45), arrowprops=dict(arrowstyle="-", color='#047857', lw=1.2))
    ax.text(9.83, 4.25, "32-bit Tag Serial: 0x007293F0 (Card ID: 0007508976 | Wiegand: 114, 37872)", fontsize=7.2, ha='center', color='#047857', fontweight='bold')

    # Checksum (Bytes 11-12)
    ax.annotate("", xy=(14.83, 4.45), xytext=(17.21, 4.45), arrowprops=dict(arrowstyle="-", color='#BE185D', lw=1.2))
    ax.text(16.02, 4.25, "XOR Checksum: 0xF0", fontsize=6.8, ha='center', color='#BE185D', fontweight='bold')

    # Mathematical Formula Box
    formula_box = FancyBboxPatch((1.45, 1.3), 16.2, 2.65, boxstyle="round,pad=0.04,rounding_size=0.08",
                                 facecolor='#F8FAFC', edgecolor='#CBD5E1', linewidth=1.1, zorder=4)
    ax.add_patch(formula_box)

    ax.text(1.7, 3.65, "HARDWARE XOR VERIFICATION LOGIC (1-Cycle Parallel Combinational Execution):",
            fontsize=7.8, fontweight='bold', color='#1E293B')

    eq_line1 = "Checksum_Calc = Data_Byte[0] ^ Data_Byte[1] ^ Data_Byte[2] ^ Data_Byte[3] ^ Data_Byte[4]"
    eq_line2 = "= (0x00)          ^ (0x00)          ^ (0x72)          ^ (0x93)          ^ (0xF0)          = 0xF0 (MATCH! VALID)"
    ax.text(1.7, 3.25, eq_line1, fontsize=7.2, fontfamily='monospace', color='#0369A1', fontweight='bold')
    ax.text(1.7, 2.85, eq_line2, fontsize=7.2, fontfamily='monospace', color='#15803D', fontweight='bold')

    note_text = ("* Watchdog Inter-Byte Timeout: A 19-bit hardware counter (FRAME_TIMEOUT_CYCLES = 500,000) resets the FSM\n"
                 "  to ST_WAIT_STX if bytes arrive spaced further than 10 ms apart, preventing permanent lockup on corrupted packets.\n"
                 "* Zero CPU Overhead: PicoRV32 only reads REG_RFID_TAG_HI/LO after card_valid pulses high; no character-by-character polling.")
    ax.text(1.7, 2.4, note_text, fontsize=6.8, color='#475569', linespacing=1.3)

    plt.tight_layout()
    out_path = 'fig2_rdm6300_subsystem.png'
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"[SUCCESS] Professional Fig 2 generated at: {out_path}")

if __name__ == '__main__':
    generate_pro_rdm6300_diagram()
