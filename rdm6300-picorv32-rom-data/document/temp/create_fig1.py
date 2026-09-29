# -*- coding: utf-8 -*-
"""
Generate crisp, publication-grade architectural block diagram for:
"Hệ thống quét và xử lý dữ liệu thẻ RFID tích hợp CPU RISC-V PicoRV32 quản lý dữ liệu trên Flash"
Key Layout Principles:
- Complete elimination of text collisions: titles at top, subtitles top-aligned below.
- Spacious 3-column + dedicated bottom branch layout:
  * Top Left: PicoRV32 CPU Core
  * Middle Left: MMIO Bus Interconnect
  * Center: 8KB Mask ROM & 2KB Data SRAM (generously spaced)
  * Right: SPI Flash Controller, Host PC UART, GPIO & LEDs
  * Bottom ("Phía trống khác"): The entire RDM6300 processing branch:
    [rdm6300_rx_i] -> [RFID UART RX] -> [RDM6300 Frame Decoder] -> [RFID MMIO Registers]
- Orthogonal routing trunks with junction dots.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_main_block_diagram():
    fig, ax = plt.subplots(figsize=(17, 12), dpi=300)
    ax.set_xlim(0, 17)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # Styling constants
    BOX_EDGE = 'black'
    BOX_FACE = 'white'
    HEADER_FACE = '#EFEFEF'
    LINE_W = 1.6
    ARROW_W = 1.3

    def add_box(x, y, w, h, title, subtitle="", fontsize_t=10.5, fontsize_s=8.0, header_h=0.55):
        # Main Box
        rect = patches.Rectangle(
            (x, y), w, h,
            linewidth=LINE_W,
            edgecolor=BOX_EDGE,
            facecolor=BOX_FACE,
            zorder=2
        )
        ax.add_patch(rect)
        
        # Header banner
        hdr = patches.Rectangle(
            (x, y + h - header_h), w, header_h,
            linewidth=LINE_W,
            edgecolor=BOX_EDGE,
            facecolor=HEADER_FACE,
            zorder=3
        )
        ax.add_patch(hdr)
        
        # Title text (centered in header)
        ax.text(x + w/2, y + h - header_h/2, title, ha='center', va='center',
                fontsize=fontsize_t, fontweight='bold', fontfamily='sans-serif', color='black', zorder=4)
        
        # Subtitle / body text (top-aligned below header with breathing room)
        if subtitle:
            ax.text(x + w/2, y + h - header_h - 0.15, subtitle, ha='center', va='top',
                    fontsize=fontsize_s, fontfamily='sans-serif', color='black', zorder=4,
                    linespacing=1.25)

    def add_arrow(p1, p2, label="", label_pos=(0, 0), label_align='center', label_bg=True, fontsize=8):
        arrow = patches.FancyArrowPatch(
            p1, p2,
            arrowstyle='->,head_width=3.5,head_length=5.5',
            color='black',
            linewidth=ARROW_W,
            zorder=5
        )
        ax.add_patch(arrow)
        if label:
            lx = (p1[0] + p2[0]) / 2 + label_pos[0]
            ly = (p1[1] + p2[1]) / 2 + label_pos[1]
            bbox_dict = dict(boxstyle='square,pad=0.15', facecolor='white', edgecolor='none') if label_bg else None
            ax.text(lx, ly, label, ha=label_align, va='center',
                    fontsize=fontsize, fontfamily='sans-serif', color='black', zorder=6,
                    bbox=bbox_dict, linespacing=1.15)

    def add_bi_arrow(p1, p2, label="", label_pos=(0, 0), label_align='center', label_bg=True, fontsize=8):
        arrow = patches.FancyArrowPatch(
            p1, p2,
            arrowstyle='<->,head_width=3.5,head_length=5.5',
            color='black',
            linewidth=ARROW_W,
            zorder=5
        )
        ax.add_patch(arrow)
        if label:
            lx = (p1[0] + p2[0]) / 2 + label_pos[0]
            ly = (p1[1] + p2[1]) / 2 + label_pos[1]
            bbox_dict = dict(boxstyle='square,pad=0.15', facecolor='white', edgecolor='none') if label_bg else None
            ax.text(lx, ly, label, ha=label_align, va='center',
                    fontsize=fontsize, fontfamily='sans-serif', color='black', zorder=6,
                    bbox=bbox_dict, linespacing=1.15)

    def add_line(p1, p2):
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='black', linewidth=ARROW_W, zorder=5)

    def add_dot(x, y):
        ax.plot(x, y, 'ko', markersize=4.5, zorder=7)

    # =========================================================================
    # 1. LEFT COLUMN: CPU Core & MMIO Interconnect
    # =========================================================================
    # PicoRV32 CPU Core (Top Left)
    add_box(1.2, 7.2, 3.4, 3.8, "PicoRV32 CPU Core", 
            "32-bit RISC-V (RV32I ISA)\nClaire Wolf Multi-Cycle Core\nNative Memory Handshake\nDirect Execution from ROM",
            fontsize_t=11, fontsize_s=8.5, header_h=0.55)

    # External Inputs to CPU
    add_arrow((0.1, 10.4), (1.2, 10.4), label="clk (Clock 40/50MHz)", label_pos=(0, 0.18), fontsize=8)
    add_arrow((0.1, 9.6), (1.2, 9.6), label="rst_n (Active-low Reset)", label_pos=(0, 0.18), fontsize=8)
    add_arrow((0.1, 8.8), (1.2, 8.8), label="irq[31:0] (Interrupt lines)", label_pos=(0, 0.18), fontsize=8)
    add_arrow((1.2, 8.0), (0.1, 8.0), label="cpu_trap (Trap Status)", label_pos=(0, 0.18), fontsize=8)

    # MMIO Bus Interconnect (Middle Left)
    add_box(1.2, 3.6, 3.4, 2.8, "MMIO Bus Interconnect", 
            "Address Decoder & Bus Arbiter\nMultiplexer: rom, sram, rfid,\nflash, uart, gpio\n32-bit Data & Ready Handshake",
            fontsize_t=10.5, fontsize_s=8.0, header_h=0.55)

    # Handshake: CPU <-> MMIO Interconnect
    add_arrow((2.2, 7.2), (2.2, 6.4), label="mem_valid, mem_addr[31:0]\nmem_wdata, mem_wstrb", 
              label_pos=(-0.25, 0), label_align='right', fontsize=7.5)
    add_arrow((3.6, 6.4), (3.6, 7.2), label="mem_rdata[31:0]\nmem_ready", 
              label_pos=(0.25, 0), label_align='left', fontsize=7.5)

    # =========================================================================
    # 2. CENTER COLUMN: Memory Subsystem (Mask ROM & Data SRAM)
    # =========================================================================
    # 8KB Mask ROM (Top Center)
    add_box(6.0, 7.8, 3.8, 3.2, "8KB Mask ROM",
            "Instruction Memory (rtl/mask_rom.v)\nPure Combinational Decoder\n[0x0000_0000 - 0x0000_1FFF]\n0 Flip-Flops (0 DFFs)\nZero Antenna / Zero Hold Violations",
            fontsize_t=11, fontsize_s=8.0, header_h=0.55)

    # 2KB Data SRAM (Middle Center)
    add_box(6.0, 3.8, 3.8, 3.0, "2KB Data SRAM",
            "Data Memory (rtl/data_sram.v)\nSingle-Cycle Read / Byte-Write\n[0x0001_0000 - 0x0001_07FF]\nStack & Global Data (.data, .bss)\nByte Mask (mem_wstrb[3:0])",
            fontsize_t=11, fontsize_s=8.0, header_h=0.55)

    # =========================================================================
    # 3. RIGHT COLUMN: Flash, Host UART, GPIO
    # =========================================================================
    # SPI Flash Controller (Top Right)
    add_box(11.4, 7.8, 3.8, 3.2, "SPI Flash Controller",
            "spi_flash_controller.v (S25FL032P)\nFSM: Page Program (0x02), Read (0x03)\nSector Erase (0x20), WIP Polling\n[0x2000_0000 - 0x2000_0010]\nNon-Volatile Standalone Storage\nNo Internet / Offline Access",
            fontsize_t=10.5, fontsize_s=8.0, header_h=0.55)

    # Host PC UART (Middle Right)
    add_box(11.4, 4.4, 3.8, 2.6, "Host PC UART",
            "simpleuart.v (9600 Baud, 8-N-1)\nBaud Divisor & TX/RX Buffers\n[0x3000_0000 - 0x3000_0004]\nOffline Maintenance & Local Audit\nCSV Export & Tag Synchronization",
            fontsize_t=10.5, fontsize_s=8.0, header_h=0.55)

    # GPIO & Status Driver (Bottom Right)
    add_box(11.4, 1.0, 3.8, 2.2, "GPIO & LED Driver",
            "16-bit Status Register (Basys 3)\n[0x4000_0000]\nHeartbeat, Flash Busy, Tag Valid,\nCPU Trap, Diagnostic LEDs",
            fontsize_t=10.5, fontsize_s=8.0, header_h=0.55)

    # =========================================================================
    # 4. BOTTOM BRANCH: RDM6300 RFID PROCESSING PIPELINE
    # ("Cho sang phía trống khác cho dễ nhìn")
    # =========================================================================
    # External RFID reader module input
    add_arrow((0.05, 2.1), (1.0, 2.1))
    ax.text(0.5, 2.5, "rdm6300_rx_i\n(125kHz Serial)", ha='center', va='center',
            fontsize=7.5, fontweight='bold', fontfamily='sans-serif', color='black',
            bbox=dict(boxstyle='square,pad=0.1', facecolor='white', edgecolor='none'))

    # Sub-block 1: RFID UART RX
    add_box(1.0, 1.0, 2.7, 2.1, "RFID UART RX",
            "sync_2ff.v & uart_rx.v\n2-Stage CDC Synchronizer\n9600 Baud Deserializer\nOut: rx_dv, rx_byte[7:0]",
            fontsize_t=9.5, fontsize_s=7.5, header_h=0.45)

    # Arrow from RX to Decoder
    add_arrow((3.7, 2.05), (4.4, 2.05), label="rx_dv\nrx_byte[7:0]", label_pos=(0, 0.32), fontsize=7.5)

    # Sub-block 2: RDM6300 Frame Decoder
    add_box(4.4, 1.0, 3.1, 2.1, "RDM6300 Frame Decoder",
            "rdm6300_frame_decoder.v\n5-State FSM: STX -> ASCII -> ETX\nHardware XOR Checksum Engine\n(Chi tiết xem Hình 2)",
            fontsize_t=9.5, fontsize_s=7.5, header_h=0.45)

    # Arrow from Decoder to MMIO Regs
    add_arrow((7.5, 2.05), (8.2, 2.05), label="card_valid\ntag_raw[39:0]", label_pos=(0, 0.32), fontsize=7.5)

    # Sub-block 3: RFID MMIO Registers
    add_box(8.2, 1.0, 2.4, 2.1, "RFID MMIO Regs",
            "Thanh ghi MMIO\n[0x1000_0000]\nTag Lo / Tag Hi\nChốt dữ liệu thẻ",
            fontsize_t=9.5, fontsize_s=7.5, header_h=0.45)

    # Border grouping rectangle around the RDM6300 pipeline
    branch_rect = patches.Rectangle(
        (0.85, 0.7), 10.0, 2.6,
        linewidth=1.2, linestyle='--', edgecolor='#555555', facecolor='none', zorder=1
    )
    ax.add_patch(branch_rect)
    ax.text(0.95, 3.5, "Nhánh xử lý thẻ RFID RDM6300 độc lập (Hardware Pipeline)", 
            ha='left', va='center', fontsize=8.5, fontweight='bold', fontstyle='italic', color='#333333',
            bbox=dict(boxstyle='square,pad=0.15', facecolor='white', edgecolor='none'))

    # Connections from RFID MMIO Registers up to MMIO Bus & CPU IRQ
    # 1. To MMIO Bus Interconnect
    add_line((9.4, 3.1), (9.4, 3.6))
    add_line((9.4, 3.6), (5.2, 3.6))
    add_line((5.2, 3.6), (5.2, 4.6))
    add_arrow((5.2, 4.6), (4.6, 4.6), label="sel_rfid, rfid_rdata\nrfid_ready", label_pos=(0.3, 0.32), fontsize=7.5)

    # 2. Card event IRQ up to CPU
    add_line((8.6, 3.1), (8.6, 3.35))
    add_line((8.6, 3.35), (4.9, 3.35))
    add_line((4.9, 3.35), (4.9, 7.8))
    add_arrow((4.9, 7.8), (4.6, 7.8), label="card_event_o (IRQ)", label_pos=(-0.4, 0.2), label_align='right', fontsize=7.5)

    # =========================================================================
    # 5. MMIO BUS INTERCONNECT TRUNK ROUTING
    # =========================================================================
    # Main trunk leaves Interconnect from right side at y = 5.2
    add_line((4.6, 5.2), (5.4, 5.2))
    add_dot(5.4, 5.2)

    # Vertical trunk between Left and Center column (x = 5.4)
    add_line((5.4, 5.2), (5.4, 9.4))
    add_dot(5.4, 9.4)

    # Connection to Mask ROM
    add_bi_arrow((5.4, 9.4), (6.0, 9.4), label="sel_rom, addr[12:0]\nrom_rdata, rom_ready", 
                 label_pos=(0, 0.28), fontsize=7.5)

    # Connection to Data SRAM
    add_bi_arrow((5.4, 5.2), (6.0, 5.2), label="sel_sram, addr, wdata\nsram_rdata, sram_ready", 
                 label_pos=(0, 0.28), fontsize=7.5)

    # Bus trunk continuing to the Right Column (over the center boxes at y = 7.1)
    # Line goes between Mask ROM and Data SRAM (y = 7.2 is empty!)
    add_line((5.4, 7.2), (10.9, 7.2))
    add_dot(5.4, 7.2)
    add_dot(10.9, 7.2)

    # Vertical distribution line on the right side (x = 10.9)
    add_line((10.9, 2.1), (10.9, 9.4))
    add_dot(10.9, 9.4)
    add_dot(10.9, 5.7)
    add_dot(10.9, 2.1)

    # Connection to SPI Flash Controller
    add_bi_arrow((10.9, 9.4), (11.4, 9.4), label="sel_flash, bus_addr, bus_wdata\nflash_rdata, flash_ready", 
                 label_pos=(0, 0.28), fontsize=7.5)

    # Connection to Host PC UART
    add_bi_arrow((10.9, 5.7), (11.4, 5.7), label="sel_uart, uart_rdata\nuart_ready", 
                 label_pos=(0, 0.24), fontsize=7.5)

    # Connection to GPIO & LED Driver
    add_bi_arrow((10.9, 2.1), (11.4, 2.1), label="sel_gpio\nleds_data", 
                 label_pos=(0, 0.22), fontsize=7.5)

    # Bus Trunk Label
    ax.text(8.0, 7.42, "MMIO System Bus Trunk (32-bit Address & Data)", 
            ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='black',
            bbox=dict(boxstyle='square,pad=0.2', facecolor='white', edgecolor='none'))

    # =========================================================================
    # 6. EXTERNAL PERIPHERAL PINS (Far Right)
    # =========================================================================
    # External SPI Flash Lines
    add_arrow((15.2, 10.4), (16.7, 10.4), label="flash_csn (Chip Select)", label_pos=(0, 0.16), fontsize=7.5)
    add_arrow((15.2, 9.7), (16.7, 9.7), label="flash_sck (SPI Clock 25MHz)", label_pos=(0, 0.16), fontsize=7.5)
    add_arrow((15.2, 9.0), (16.7, 9.0), label="flash_mosi (Master Out)", label_pos=(0, 0.16), fontsize=7.5)
    add_arrow((16.7, 8.3), (15.2, 8.3), label="flash_miso (Master In)", label_pos=(0, 0.16), fontsize=7.5)
    ax.text(16.0, 11.15, "External SPI Flash\n(Spansion S25FL032P)", ha='center', va='center', 
            fontsize=8.5, fontweight='bold', color='black')

    # External Host PC UART Lines
    add_arrow((15.2, 6.0), (16.7, 6.0), label="uart_tx_o (To PC)", label_pos=(0, 0.16), fontsize=7.5)
    add_arrow((16.7, 5.1), (15.2, 5.1), label="uart_rx_i (From PC)", label_pos=(0, 0.16), fontsize=7.5)
    ax.text(16.0, 6.65, "Host PC (USB-UART / VCP)\n(Console 9600 bps)", ha='center', va='center', 
            fontsize=8.5, fontweight='bold', color='black')

    # External LED Lines
    add_arrow((15.2, 2.1), (16.7, 2.1), label="leds_o[15:0] (Diagnostic LEDs)", label_pos=(0, 0.16), fontsize=7.5)
    ax.text(16.0, 2.9, "Basys 3 LEDs Display\n(Heartbeat, Flash, Valid)", ha='center', va='center', 
            fontsize=8.5, fontweight='bold', color='black')

    plt.tight_layout()
    plt.savefig('fig1_block_diagram.png', dpi=300, facecolor='white', bbox_inches='tight')
    plt.close()
    print("Clean Fig 1 block diagram generated successfully: fig1_block_diagram.png")

if __name__ == "__main__":
    draw_main_block_diagram()
