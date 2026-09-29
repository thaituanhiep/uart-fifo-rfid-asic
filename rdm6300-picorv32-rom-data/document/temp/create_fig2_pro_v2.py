# -*- coding: utf-8 -*-
"""
Script: create_fig2_pro_v2.py
Generates a publication-grade, semiconductor-datasheet quality architectural pipeline diagram for:
"Đường ống thu nhận và giải mã phần cứng thẻ RFID RDM6300 (rdm6300_frame_decoder.v)" (Hình 2)

Design Highlights:
- Explicit z-order on every single patch, line, and text label (zorder=10+ for text) to prevent any hidden text.
- Clean 5-Stage Hardware Pipeline (RF Front-End, 2-FF CDC, UART RX, Frame Decoder FSM & XOR, MMIO Registers).
- High-density 14-Byte Serial Frame Anatomy with real card breakdown (EM4100 0007508976 / 0x007293F0).
- Explicit bitwise parallel XOR checksum mathematical demonstration.
- Zero CPU Overhead & Anti-Hang Watchdog Timeout mechanism.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle

def generate_pro_rdm6300_diagram():
    fig, ax = plt.subplots(figsize=(21, 14.5), dpi=300)
    ax.set_xlim(0, 21)
    ax.set_ylim(0, 14.5)
    ax.axis('off')

    # Color Palette (High-Tech Semiconductor Engineering)
    CLR_BG         = '#F8FAFC'
    CLR_DIE_BG     = '#FFFFFF'
    CLR_BORDER     = '#0F172A'
    
    PAL = {
        'rf':   {'hdr': '#1E3A8A', 'hdr_accent': '#2563EB', 'body': '#EFF6FF', 'bdr': '#1D4ED8', 'cell_bg': '#FFFFFF', 'cell_bdr': '#93C5FD'},
        'sync': {'hdr': '#064E3B', 'hdr_accent': '#059669', 'body': '#ECFDF5', 'bdr': '#047857', 'cell_bg': '#FFFFFF', 'cell_bdr': '#A7F3D0'},
        'uart': {'hdr': '#78350F', 'hdr_accent': '#D97706', 'body': '#FFFBEB', 'bdr': '#B45309', 'cell_bg': '#FFFFFF', 'cell_bdr': '#FDE68A'},
        'fsm':  {'hdr': '#4C1D95', 'hdr_accent': '#7C3AED', 'body': '#F5F3FF', 'bdr': '#6D28D9', 'cell_bg': '#FFFFFF', 'cell_bdr': '#DDD6FE'},
        'reg':  {'hdr': '#831843', 'hdr_accent': '#DB2777', 'body': '#FDF2F8', 'bdr': '#BE185D', 'cell_bg': '#FFFFFF', 'cell_bdr': '#FBCFE8'},
        'card': {'hdr': '#0F766E', 'hdr_accent': '#0D9488', 'body': '#F0FDFA', 'bdr': '#0F766E', 'cell_bg': '#FFFFFF', 'cell_bdr': '#99F6E4'}
    }

    # Background canvas tint
    ax.add_patch(Rectangle((0, 0), 21, 14.5, facecolor=CLR_BG, zorder=0))

    # Main outer boundary
    main_box = FancyBboxPatch((1.0, 0.7), 19.0, 13.1,
                              boxstyle="round,pad=0.06,rounding_size=0.22",
                              facecolor=CLR_DIE_BG, edgecolor=CLR_BORDER, linewidth=2.4, zorder=1)
    ax.add_patch(main_box)
    
    # Top Title Banner
    top_bar = FancyBboxPatch((1.0, 13.05), 19.0, 0.75,
                             boxstyle="round,pad=0.04,rounding_size=0.15",
                             facecolor='#0F172A', edgecolor='#0F172A', zorder=2)
    ax.add_patch(top_bar)
    
    ax.text(1.3, 13.44, "RDM6300 RFID HARDWARE RECEPTION & AUTONOMOUS DECODING PIPELINE",
            fontsize=12.0, fontweight='bold', color='#FFFFFF', va='center', fontfamily='sans-serif', zorder=10)
    ax.text(1.3, 13.18, "Module: rtl/rdm6300_frame_decoder.v, rtl/uart_rx.v, rtl/sync_2ff.v | SkyWater 130nm ASIC & Basys 3 Demo",
            fontsize=8.5, color='#94A3B8', va='center', fontfamily='sans-serif', zorder=10)
    ax.text(19.7, 13.44, "Autonomous Hardware Engine | Zero CPU Polling Overhead",
            fontsize=9.2, fontweight='bold', color='#38BDF8', ha='right', va='center', fontfamily='sans-serif', zorder=10)
    ax.text(19.7, 13.18, "Deterministic Latency: 1-Cycle Parallel XOR Checksum Verification",
            fontsize=8.5, color='#A7F3D0', ha='right', va='center', fontfamily='sans-serif', zorder=10)

    # Helper: draw stylized stage block
    def draw_stage(x, y, w, h, title, sub_title, pal_key, tag=""):
        p = PAL[pal_key]
        body = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                              facecolor=p['body'], edgecolor=p['bdr'], linewidth=1.3, zorder=3)
        ax.add_patch(body)
        
        hdr_h = 0.56
        hdr = FancyBboxPatch((x, y + h - hdr_h), w, hdr_h, boxstyle="round,pad=0.02,rounding_size=0.12",
                             facecolor=p['hdr'], edgecolor=p['bdr'], linewidth=1.3, zorder=4)
        ax.add_patch(hdr)
        ax.add_patch(Rectangle((x, y + h - hdr_h), w, 0.1, facecolor=p['hdr'], edgecolor=p['hdr'], zorder=5))
        
        ax.text(x + 0.18, y + h - 0.22, title,
                fontsize=8.5, fontweight='bold', color='#FFFFFF', va='center', fontfamily='sans-serif', zorder=10)
        ax.text(x + 0.18, y + h - 0.43, sub_title,
                fontsize=6.8, color='#94A3B8', va='center', fontfamily='sans-serif', zorder=10)
        
        if tag:
            tag_w = len(tag) * 0.10 + 0.30
            tag_box = FancyBboxPatch((x + w - tag_w - 0.12, y + h - 0.44), tag_w, 0.32,
                                     boxstyle="round,pad=0.02,rounding_size=0.06",
                                     facecolor=p['hdr_accent'], edgecolor='none', zorder=6)
            ax.add_patch(tag_box)
            ax.text(x + w - tag_w/2 - 0.12, y + h - 0.28, tag,
                    fontsize=6.5, fontweight='bold', color='#FFFFFF',
                    ha='center', va='center', fontfamily='sans-serif', zorder=10)

    # Helper: draw internal subunit cell
    def draw_sub(x, y, w, h, title, desc="", pal_key='rf', fs_t=7.0, fs_d=6.0):
        p = PAL[pal_key]
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                              facecolor=p['cell_bg'], edgecolor=p['cell_bdr'], linewidth=0.8, zorder=6)
        ax.add_patch(rect)
        if desc:
            lines = desc.split('\n')
            ax.text(x + w/2, y + h - 0.20, title, fontsize=fs_t, fontweight='bold', color='#0F172A',
                    ha='center', va='center', fontfamily='sans-serif', zorder=10)
            line_y = y + h - 0.42
            for l in lines:
                ax.text(x + w/2, line_y, l, fontsize=fs_d, color='#475569',
                        ha='center', va='center', fontfamily='sans-serif', zorder=10)
                line_y -= 0.18
        else:
            ax.text(x + w/2, y + h/2, title, fontsize=fs_t, fontweight='bold', color='#0F172A',
                    ha='center', va='center', fontfamily='sans-serif', zorder=10)

    # =========================================================================
    # PART A: TOP HARDWARE PIPELINE (Stages 1 through 5)
    # =========================================================================
    # Stage 1: RF Front-End (Left)
    draw_stage(1.3, 7.3, 3.2, 5.5, "STAGE 1: RF FRONT-END", "Physical Transponder & Analog", 'rf', tag="125 kHz")
    draw_sub(1.5, 11.0, 2.8, 1.15, "EM4100 Transponder", "125 kHz Passive RFID Tag\nManchester RF Modulation\n64-bit Internal Memory Map", 'rf')
    draw_sub(1.5, 9.4, 2.8, 1.35, "Coil Antenna & Demod", "Inductive Coupling (LC Tank)\nEnvelope Demodulator\nNoise Shaping & Slicer Filter", 'rf')
    draw_sub(1.5, 7.6, 2.8, 1.55, "RDM6300 TTL Output", "UART 9600 bps 8-N-1 Serial\nTTL Output Pin -> PMOD JA1\n3.3V/5V Level Tolerant", 'rf')

    # Stage 2: CDC Synchronizer
    draw_stage(4.8, 7.3, 3.1, 5.5, "STAGE 2: 2-FF CDC SYNC", "sync_2ff.v — Metastability", 'sync', tag="50 MHz")
    draw_sub(5.0, 11.0, 2.7, 1.15, "Asynchronous Input Pin", "Signal: rdm_rx_i (Async)\nPMOD JA1 (FPGA Pin J1)\nPotential Metastability Risk", 'sync')
    draw_sub(5.0, 9.4, 2.7, 1.35, "Stage 1 Flip-Flop", "Captures async input at 50MHz\nQ1 output may oscillate briefly\nTsu / Th violation absorbed", 'sync')
    draw_sub(5.0, 7.6, 2.7, 1.55, "Stage 2 Flip-Flop (Filter)", "Resolves state to valid 0 or 1\nOutput: rdm_rx_sync (Clean)\nMTBF > 1000 years in 130nm", 'sync')

    # Stage 3: UART RX Core
    draw_stage(8.2, 7.3, 3.4, 5.5, "STAGE 3: UART RX ENGINE", "uart_rx.v — 9600 Baud Receiver", 'uart', tag="Oversampling")
    draw_sub(8.4, 11.0, 3.0, 1.15, "Baud Clock Divider", "Divisor = 50,000,000 / 9600\n= 5208 Clock Cycles per bit\n16x Sampling Clock Generator", 'uart')
    draw_sub(8.4, 9.4, 3.0, 1.35, "16x Majority Voter", "Center 3-Point Majority Vote\nSamples at ticks 7, 8, 9 of bit\nRejects noise spikes & glitches", 'uart')
    draw_sub(8.4, 7.6, 3.0, 1.55, "Byte Deserializer Register", "8-bit SIPO Shift Register\nOutputs: byte_data[7:0]\nStrobe: byte_valid (1 cycle pulse)", 'uart')

    # Stage 4: 14-Byte Frame Decoder FSM
    draw_stage(12.2, 7.3, 4.3, 5.5, "STAGE 4: FRAME DECODER FSM", "rdm6300_frame_decoder.v", 'fsm', tag="Hardware FSM")
    draw_sub(12.4, 11.0, 3.9, 1.15, "FSM State Controller", "ST_WAIT_STX -> ST_COLLECT_DATA\nST_CHECKSUM -> ST_WAIT_ETX\nST_VALIDATE (Auto State Machine)", 'fsm')
    draw_sub(12.4, 9.4, 3.9, 1.35, "ASCII-to-Hex Combinational Unit", "ascii_to_nibble() Function\nConverts '0'-'9' (0x30-0x39) to 0-9\nConverts 'A'-'F' (0x41-0x46) to 10-15\n10 ASCII Chars -> 5 Hex Bytes", 'fsm')
    draw_sub(12.4, 7.6, 3.9, 1.55, "Parallel XOR Parity Engine & WDT", "1-Cycle Combinational XOR Tree\nD[0] ^ D[1] ^ D[2] ^ D[3] ^ D[4] == CS\n10 ms Watchdog (500k cycles) Timeout", 'fsm')

    # Stage 5: MMIO Registers & Interrupt
    draw_stage(17.1, 7.3, 2.7, 5.5, "STAGE 5: MMIO REGS", "Address: 0x1000_0000", 'reg', tag="MMIO")
    draw_sub(17.3, 11.0, 2.3, 1.15, "REG_STATUS (0x00)", "Bit 0: card_valid (W1C)\nBit 1: cs_error (Fail)\nRead/Write by MMIO", 'reg')
    draw_sub(17.3, 9.4, 2.3, 1.35, "REG_TAG_HI (0x04)", "Bits [39:32]: Version Byte\nExample: 0x00\nRead-only register", 'reg')
    draw_sub(17.3, 7.6, 2.3, 1.55, "REG_TAG_LO (0x08)", "Bits [31:0]: Serial Number\nExample: 0x007293F0\nHardware IRQ Output", 'reg')

    # Inter-stage arrows
    ax.annotate("", xy=(4.8, 9.8), xytext=(4.5, 9.8), arrowprops=dict(arrowstyle="->", color=PAL['rf']['bdr'], lw=2.0), zorder=15)
    ax.text(4.65, 10.05, "rdm_rx", fontsize=6.8, fontweight='bold', color=PAL['rf']['hdr'], ha='center', zorder=15)

    ax.annotate("", xy=(8.2, 9.8), xytext=(7.9, 9.8), arrowprops=dict(arrowstyle="->", color=PAL['sync']['bdr'], lw=2.0), zorder=15)
    ax.text(8.05, 10.05, "rx_sync", fontsize=6.8, fontweight='bold', color=PAL['sync']['hdr'], ha='center', zorder=15)

    ax.annotate("", xy=(12.2, 9.8), xytext=(11.6, 9.8), arrowprops=dict(arrowstyle="->", color=PAL['uart']['bdr'], lw=2.0), zorder=15)
    ax.text(11.9, 10.15, "byte_data[7:0]", fontsize=6.5, fontweight='bold', color=PAL['uart']['hdr'], ha='center', zorder=15)
    ax.text(11.9, 9.45, "byte_valid", fontsize=6.2, color=PAL['uart']['hdr'], ha='center', zorder=15)

    ax.annotate("", xy=(17.1, 9.8), xytext=(16.5, 9.8), arrowprops=dict(arrowstyle="->", color=PAL['fsm']['bdr'], lw=2.0), zorder=15)
    ax.text(16.8, 10.15, "tag[39:0]", fontsize=6.5, fontweight='bold', color=PAL['fsm']['hdr'], ha='center', zorder=15)
    ax.text(16.8, 9.45, "valid_strobe", fontsize=6.2, color=PAL['fsm']['hdr'], ha='center', zorder=15)

    # Interrupt Output to CPU
    ax.annotate("", xy=(20.3, 8.4), xytext=(19.8, 8.4), arrowprops=dict(arrowstyle="->", color='#DC2626', lw=2.2), zorder=15)
    ax.text(20.05, 8.65, "card_event_o", fontsize=6.8, fontweight='bold', color='#DC2626', ha='center', zorder=15)
    ax.text(20.05, 8.15, "(CPU IRQ)", fontsize=6.2, color='#DC2626', ha='center', zorder=15)

    # =========================================================================
    # PART B: BOTTOM SECTION: 14-BYTE FRAME ANATOMY & PARALLEL XOR FORMULA
    # =========================================================================
    frame_box = FancyBboxPatch((1.3, 0.95), 18.4, 6.0,
                               boxstyle="round,pad=0.04,rounding_size=0.15",
                               facecolor='#FFFFFF', edgecolor='#334155', linewidth=1.5, zorder=3)
    ax.add_patch(frame_box)

    # Section B Header
    ax.text(1.6, 6.65, "RDM6300 14-BYTE SERIAL FRAME BREAKDOWN & PARALLEL XOR CHECKSUM FORMULA",
            fontsize=10.0, fontweight='bold', color='#0F172A', fontfamily='sans-serif', zorder=10)
    ax.text(19.4, 6.65, "Real Card Verification Example: 0007508976 (Wiegand: FC 114, ID 37872 | Hex: 0x007293F0)",
            fontsize=8.2, color='#047857', fontweight='bold', ha='right', fontfamily='sans-serif', zorder=10)

    # 14-Byte Frame Grid Definition (Total width = 17.8 inches)
    # Byte slots: 14 total
    slots = [
        ("Byte 0", "Header", "STX\n(0x02)", "#F1F5F9", 1.05),
        ("Byte 1", "Ver[7:4]", "ASCII '0'\n(0x30)", "#EFF6FF", 1.25),
        ("Byte 2", "Ver[3:0]", "ASCII '0'\n(0x30)", "#EFF6FF", 1.25),
        ("Byte 3", "Data[31:28]", "ASCII '0'\n(0x30)", "#ECFDF5", 1.25),
        ("Byte 4", "Data[27:24]", "ASCII '0'\n(0x30)", "#ECFDF5", 1.25),
        ("Byte 5", "Data[23:20]", "ASCII '7'\n(0x37)", "#ECFDF5", 1.25),
        ("Byte 6", "Data[19:16]", "ASCII '2'\n(0x32)", "#ECFDF5", 1.25),
        ("Byte 7", "Data[15:12]", "ASCII '9'\n(0x39)", "#ECFDF5", 1.25),
        ("Byte 8", "Data[11:8]", "ASCII '3'\n(0x33)", "#ECFDF5", 1.25),
        ("Byte 9", "Data[7:4]", "ASCII 'F'\n(0x46)", "#ECFDF5", 1.25),
        ("Byte 10", "Data[3:0]", "ASCII '0'\n(0x30)", "#ECFDF5", 1.25),
        ("Byte 11", "CS[7:4]", "ASCII 'F'\n(0x46)", "#FDF2F8", 1.25),
        ("Byte 12", "CS[3:0]", "ASCII '0'\n(0x30)", "#FDF2F8", 1.25),
        ("Byte 13", "Footer", "ETX\n(0x03)", "#F1F5F9", 1.05),
    ]

    curr_x = 1.6
    for b_idx, name, char_val, c_fill, w in slots:
        rect = FancyBboxPatch((curr_x, 4.9), w, 1.45, boxstyle="round,pad=0.02,rounding_size=0.06",
                              facecolor=c_fill, edgecolor='#475569', linewidth=1.0, zorder=5)
        ax.add_patch(rect)
        
        ax.text(curr_x + w/2, 6.10, b_idx, fontsize=6.8, color='#64748B', ha='center', va='center', fontweight='bold', zorder=10)
        ax.text(curr_x + w/2, 5.75, name, fontsize=6.5, color='#0F172A', ha='center', va='center', fontweight='bold', zorder=10)
        
        lines = char_val.split('\n')
        ax.text(curr_x + w/2, 5.32, lines[0], fontsize=7.2, color='#1E40AF', ha='center', va='center', fontfamily='monospace', fontweight='bold', zorder=10)
        ax.text(curr_x + w/2, 5.05, lines[1], fontsize=6.2, color='#475569', ha='center', va='center', fontfamily='monospace', zorder=10)
        
        curr_x += w + 0.08

    # Category Bracket Annotations under the frame
    # STX
    ax.annotate("", xy=(1.6, 4.75), xytext=(2.65, 4.75), arrowprops=dict(arrowstyle="-", color='#64748B', lw=1.2), zorder=10)
    ax.text(2.12, 4.58, "Start of Text", fontsize=6.5, ha='center', color='#64748B', zorder=10)

    # Version (Bytes 1-2)
    ax.annotate("", xy=(2.73, 4.75), xytext=(5.23, 4.75), arrowprops=dict(arrowstyle="-", color='#1D4ED8', lw=1.2), zorder=10)
    ax.text(3.98, 4.58, "Version: 0x00 (Byte 0)", fontsize=6.8, ha='center', color='#1D4ED8', fontweight='bold', zorder=10)

    # 32-bit Serial (Bytes 3-10)
    ax.annotate("", xy=(5.31, 4.75), xytext=(15.95, 4.75), arrowprops=dict(arrowstyle="-", color='#047857', lw=1.2), zorder=10)
    ax.text(10.63, 4.58, "32-bit Tag Serial Number: 0x007293F0 (Card ID: 0007508976 | Wiegand: FC 114, ID 37872)",
            fontsize=7.2, ha='center', color='#047857', fontweight='bold', zorder=10)

    # Checksum (Bytes 11-12)
    ax.annotate("", xy=(16.03, 4.75), xytext=(18.53, 4.75), arrowprops=dict(arrowstyle="-", color='#BE185D', lw=1.2), zorder=10)
    ax.text(17.28, 4.58, "XOR Checksum: 0xF0", fontsize=6.8, ha='center', color='#BE185D', fontweight='bold', zorder=10)

    # ETX
    ax.annotate("", xy=(18.61, 4.75), xytext=(19.66, 4.75), arrowprops=dict(arrowstyle="-", color='#64748B', lw=1.2), zorder=10)
    ax.text(19.13, 4.58, "End of Text", fontsize=6.5, ha='center', color='#64748B', zorder=10)

    # Mathematical Verification Box
    math_box = FancyBboxPatch((1.6, 1.2), 17.8, 3.1,
                              boxstyle="round,pad=0.04,rounding_size=0.08",
                              facecolor='#F8FAFC', edgecolor='#CBD5E1', linewidth=1.1, zorder=5)
    ax.add_patch(math_box)

    ax.text(1.9, 4.0, "PARALLEL HARDWARE XOR CHECKSUM VERIFICATION LOGIC (1-Cycle Combinational Tree):",
            fontsize=8.2, fontweight='bold', color='#0F172A', zorder=10)

    f_line1 = "Formula:   Calculated_Checksum = Data_Byte[0] ^ Data_Byte[1] ^ Data_Byte[2] ^ Data_Byte[3] ^ Data_Byte[4]"
    f_line2 = "Binary:    = (0000_0000)    ^    (0000_0000)    ^    (0111_0010)    ^    (1001_0011)    ^    (1111_0000)"
    f_line3 = "Hex Eval:  = (0x00)          ^    (0x00)          ^    (0x72)          ^    (0x93)          ^    (0xF0)          = 0xF0"
    f_line4 = "Result:    Calculated_Checksum (0xF0) == Received_Checksum (0xF0)  -->  VALIDATION SUCCESS! (Assert card_valid)"

    ax.text(1.9, 3.65, f_line1, fontsize=7.2, fontfamily='monospace', color='#0369A1', fontweight='bold', zorder=10)
    ax.text(1.9, 3.35, f_line2, fontsize=7.0, fontfamily='monospace', color='#475569', zorder=10)
    ax.text(1.9, 3.05, f_line3, fontsize=7.2, fontfamily='monospace', color='#15803D', fontweight='bold', zorder=10)
    ax.text(1.9, 2.75, f_line4, fontsize=7.2, fontfamily='monospace', color='#B91C1C', fontweight='bold', zorder=10)

    note_text = (
        "* Anti-Hang Hardware Watchdog Timer: A 19-bit counter (FRAME_TIMEOUT_CYCLES = 500,000 cycles = 10 ms at 50 MHz) resets\n"
        "  the FSM back to ST_WAIT_STX if byte intervals exceed 10 ms, ensuring complete recovery from severed transmissions or RF collisions.\n"
        "* Autonomous Zero-Overhead Operation: PicoRV32 never polls individual UART characters; it is only notified via interrupt or flag\n"
        "  when an entire 14-byte frame has been authenticated and latched into REG_RFID_TAG_HI / REG_RFID_TAG_LO."
    )
    ax.text(1.9, 2.15, note_text, fontsize=6.8, color='#334155', linespacing=1.35, zorder=10)

    plt.tight_layout()
    out_path = 'fig2_rdm6300_subsystem.png'
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor=CLR_BG)
    plt.close()
    print(f"[SUCCESS] Figure 2 v2 generated successfully at: {out_path}")

if __name__ == '__main__':
    generate_pro_rdm6300_diagram()
