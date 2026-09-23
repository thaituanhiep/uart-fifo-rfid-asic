# -*- coding: utf-8 -*-
"""
Generate crisp, publication-grade architectural block diagram for:
"Bộ giải mã phần cứng thẻ RFID RDM6300 (rdm6300_frame_decoder)" (Hình 2)
Key Layout Principles:
- Zero text collisions: boxes with header banners and top-aligned body text.
- Full pipeline view:
  [Module RDM6300] -> [sync_2ff.v] -> [uart_rx.v] -> [rdm6300_frame_decoder.v] -> [RFID MMIO Registers] -> [Bus / IRQ]
- Comprehensive protocol explanation table at bottom.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_rdm6300_subsystem():
    fig, ax = plt.subplots(figsize=(17, 11), dpi=300)
    ax.set_xlim(0, 17)
    ax.set_ylim(0, 11)
    ax.axis('off')

    # Styling constants
    BOX_EDGE = 'black'
    BOX_FACE = 'white'
    HEADER_FACE = '#EFEFEF'
    LINE_W = 1.6
    ARROW_W = 1.3

    def add_box(x, y, w, h, title, subtitle="", fontsize_t=10, fontsize_s=8.0, header_h=0.55):
        rect = patches.Rectangle(
            (x, y), w, h,
            linewidth=LINE_W,
            edgecolor=BOX_EDGE,
            facecolor=BOX_FACE,
            zorder=2
        )
        ax.add_patch(rect)
        
        hdr = patches.Rectangle(
            (x, y + h - header_h), w, header_h,
            linewidth=LINE_W,
            edgecolor=BOX_EDGE,
            facecolor=HEADER_FACE,
            zorder=3
        )
        ax.add_patch(hdr)
        
        ax.text(x + w/2, y + h - header_h/2, title, ha='center', va='center',
                fontsize=fontsize_t, fontweight='bold', fontfamily='sans-serif', color='black', zorder=4)
        
        if subtitle:
            ax.text(x + w/2, y + h - header_h - 0.15, subtitle, ha='center', va='top',
                    fontsize=fontsize_s, fontfamily='sans-serif', color='black', zorder=4,
                    linespacing=1.25)

    def add_arrow(p1, p2, label="", label_pos=(0, 0), label_align='center', label_bg=True, fontsize=7.5):
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

    def add_bi_arrow(p1, p2, label="", label_pos=(0, 0), label_align='center', label_bg=True, fontsize=7.5):
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

    # =========================================================================
    # PIPELINE BLOCKS (Left to Right, y = 5.2 to 10.4)
    # =========================================================================

    # 1. External RDM6300 Module (Far Left)
    add_box(0.5, 5.4, 2.7, 4.4, "Module RDM6300",
            "Đầu đọc RFID 125 kHz\nCuộn cảm thu sóng EM4100\nBộ giải điều chế Analog\nXuất chuỗi 14 byte ASCII\nTốc độ: 9600 Baud (8-N-1)\nĐiện áp cấp: 5V / 3.3V DC\nKhoảng cách quét: 2 - 5 cm",
            fontsize_t=10, fontsize_s=8.0, header_h=0.55)

    # 2. CDC Synchronizer (sync_2ff.v)
    add_box(3.8, 6.0, 2.5, 3.4, "sync_2ff.v",
            "Mạch chống Metastability\n2 tầng D-FF nối tiếp\nĐồng bộ tín hiệu không đồng bộ\nvào miền xung nhịp clk (50 MHz)\nNgõ ra: rdm_rx_sync",
            fontsize_t=10, fontsize_s=8.0, header_h=0.55)

    # 3. UART RX Deserializer (uart_rx.v)
    add_box(6.9, 5.4, 2.9, 4.4, "uart_rx.v (9600 Baud)",
            "Bộ giải tuần tự UART\nBộ chia tần Clks/Bit (5208)\nBộ lọc Majority 3 mẫu điểm giữa\nThanh ghi dịch 8-bit\nKhử nhiễu đường truyền\nNgõ ra:\n  • rx_dv (Data Valid strobe)\n  • rx_byte[7:0] (Byte data)",
            fontsize_t=10, fontsize_s=7.8, header_h=0.55)

    # 4. Hardware Frame Decoder FSM (rdm6300_frame_decoder.v)
    add_box(9.9, 4.8, 3.4, 5.2, "rdm6300_frame_decoder.v",
            "FSM Giải mã Phần cứng 5 Trạng thái:\n  • S_IDLE: Chờ Header STX (0x02)\n  • S_DATA: Thu thập 10 ký tự ASCII\n    (Giải mã tổ hợp sang 5 byte Hex)\n  • S_CKSUM: Thu thập 2 ký tự Checksum\n  • S_VERIFY: Kiểm tra Footer ETX (0x03)\n  • S_VALID: Kích hoạt cờ valid 1 chu kỳ\n------------------------------------\nBộ tính XOR Checksum phần cứng song song:\n  D0 ^ D1 ^ D2 ^ D3 ^ D4 == CKSUM\nNgõ ra:\n  • hw_card_valid (1 cycle strobe)\n  • hw_tag_raw[39:0] (40-bit Card UID)",
            fontsize_t=9.5, fontsize_s=7.4, header_h=0.55)

    # 5. RFID MMIO Registers (0x1000_0000)
    add_box(13.9, 5.0, 2.1, 4.8, "RFID MMIO Regs",
            "Thanh ghi MMIO\n[0x1000_0000 - 0x1000_0008]\n---------------------------\n0x1000_0000: Status Reg\n  Bit 0: rfid_tag_ready\n0x1000_0004: Tag Hi Word\n  Bit [7:0]: Version / Cust\n0x1000_0008: Tag Lo Word\n  Bit [31:0]: Card Serial\n---------------------------\nChốt dữ liệu thẻ & Phát ngắt",
            fontsize_t=9.5, fontsize_s=7.2, header_h=0.55)

    # =========================================================================
    # CONNECTIONS & LABELS
    # =========================================================================
    # RDM6300 -> sync_2ff
    add_arrow((3.2, 7.7), (3.8, 7.7), label="rdm6300_rx_i\n(UART TTL 9600)", label_pos=(0, 0.35), fontsize=7.5)

    # sync_2ff -> uart_rx
    add_arrow((6.3, 7.7), (6.9, 7.7), label="rdm_rx_sync", label_pos=(0, 0.28), fontsize=7.5)

    # uart_rx -> rdm6300_frame_decoder
    add_arrow((9.8, 8.2), (9.9, 8.2), label="rx_dv (Strobe)", label_pos=(0, 0.25), fontsize=7.5)
    add_arrow((9.8, 7.0), (9.9, 7.0), label="rx_byte[7:0]", label_pos=(0, -0.25), fontsize=7.5)

    # Frame Decoder -> RFID MMIO Regs
    add_arrow((13.3, 7.8), (13.9, 7.8), label="hw_card_valid", label_pos=(0, 0.25), fontsize=7.5)
    add_arrow((13.3, 6.6), (13.9, 6.6), label="hw_tag_raw[39:0]", label_pos=(0, -0.25), fontsize=7.5)

    # External bus outputs from RFID MMIO Regs (To PicoRV32 Core & MMIO Interconnect)
    add_arrow((16.0, 9.5), (16.9, 9.5), label="rfid_rdata[31:0]", label_pos=(0, 0.20), fontsize=7.0)
    add_arrow((16.0, 8.8), (16.9, 8.8), label="rfid_ready", label_pos=(0, 0.20), fontsize=7.0)
    add_arrow((16.9, 8.1), (16.0, 8.1), label="sel_rfid, mem_addr", label_pos=(0, 0.20), fontsize=7.0)
    add_arrow((16.0, 5.6), (16.9, 5.6), label="card_event_o (IRQ to CPU)", label_pos=(0, 0.20), fontsize=7.0)

    ax.text(16.45, 10.1, "Giao tiếp MMIO Bus & CPU", ha='center', va='center',
            fontsize=8.0, fontweight='bold', fontfamily='sans-serif', color='black')

    # =========================================================================
    # BOTTOM PANEL: PROTOCOL EXPLANATION & CHECKSUM ENGINE
    # =========================================================================
    proto_box = patches.Rectangle(
        (0.5, 0.6), 16.0, 3.7,
        linewidth=LINE_W, edgecolor=BOX_EDGE, facecolor='#FAFAFA', zorder=2
    )
    ax.add_patch(proto_box)

    proto_hdr = patches.Rectangle(
        (0.5, 3.75), 16.0, 0.55,
        linewidth=LINE_W, edgecolor=BOX_EDGE, facecolor='#E8E8E8', zorder=3
    )
    ax.add_patch(proto_hdr)

    ax.text(8.5, 4.02, "Cấu trúc Khung truyền Thẻ RFID RDM6300 (14 Byte ASCII Standard Frame Format & Hardware Checksum)",
            ha='center', va='center', fontsize=9.5, fontweight='bold', fontfamily='sans-serif', color='black', zorder=4)

    proto_texts = [
        ("Byte 0 (1 Byte): Header STX", "= 0x02. Tín hiệu bắt đầu khung truyền. FSM dùng STX để loại bỏ nhiễu đường truyền."),
        ("Byte 1 - 2 (2 Bytes ASCII)", "= Mã phiên bản / Khách hàng (Version / Customer ID). Chuyển đổi tổ hợp 2 ký tự ASCII Hex thành 1 byte nhị phân (D0)."),
        ("Byte 3 - 10 (8 Bytes ASCII)", "= Số sê-ri thẻ 32-bit (Card Serial Number). Chuyển đổi tổ hợp 8 ký tự ASCII Hex thành 4 byte nhị phân (D1, D2, D3, D4)."),
        ("Byte 11 - 12 (2 Bytes ASCII)", "= Mã kiểm tra Checksum. Chuyển đổi tổ hợp 2 ký tự ASCII Hex thành 1 byte nhị phân kiểm tra (CKSUM)."),
        ("Byte 13 (1 Byte): Footer ETX", "= 0x03. Tín hiệu kết thúc khung truyền. Xác nhận chuỗi 14 byte đã thu nhận trọn vẹn."),
        ("Thuật toán XOR Phần cứng", ": CKSUM_CALC = D0 ^ D1 ^ D2 ^ D3 ^ D4. Mạch logic tổ hợp đối chiếu: (CKSUM_CALC == CKSUM) && (Footer == 0x03)."),
        ("Thời gian thực thi", ": Hoàn thành xác thực và chốt mã thẻ 40-bit vào thanh ghi MMIO chính xác trong 1 chu kỳ xung nhịp (20 ns @ 50 MHz).")
    ]

    for idx, (label, desc) in enumerate(proto_texts):
        y_pos = 3.45 - idx * 0.42
        ax.text(0.8, y_pos, label, ha='left', va='center',
                fontsize=8.0, fontweight='bold', fontfamily='sans-serif', color='black', zorder=4)
        ax.text(5.5, y_pos, desc, ha='left', va='center',
                fontsize=8.0, fontfamily='sans-serif', color='black', zorder=4)

    plt.tight_layout()
    plt.savefig('fig2_rdm6300_subsystem.png', dpi=300, facecolor='white', bbox_inches='tight')
    plt.close()
    print("Clean Fig 2 RDM6300 subsystem diagram generated successfully: fig2_rdm6300_subsystem.png")

if __name__ == "__main__":
    draw_rdm6300_subsystem()
