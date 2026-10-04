# -*- coding: utf-8 -*-
"""
Script: generate_5stages_diagrams.py
Vẽ 5 sơ đồ khối đen trắng (Black & White Textbook Schematic Block Diagrams)
cho 5 giai đoạn phát triển vi hệ thống SoC:
- stage1_bw_diagram.png: Giai đoạn 1 - Khởi nguồn từ 2 khối có sẵn (picorv32.v, spimemio.v) & Bổ sung 1KB SRAM (data_sram)
- stage2_bw_diagram.png: Giai đoạn 2 - Thiết kế Cầu nối Bus Interconnect (soc_interconnect.v)
- stage3_bw_diagram.png: Giai đoạn 3 - Đồng thiết kế Phần cứng - Phần mềm (Co-Design Bootstrap)
- stage4_bw_diagram.png: Giai đoạn 4 - Mở rộng Ngoại vi MMIO có FIFO chống tràn (uart_mmio.v, sync_fifo.v, gpio)
- stage5_bw_diagram.png: Giai đoạn 5 - Tầng Firmware C tương tác phần cứng qua con trỏ volatile (soc_regs.h)
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, FancyBboxPatch
import math

def draw_open_arrow(ax, x_start, y_start, x_end, y_end, size=0.20, lw=1.6, color='#000000'):
    """Vẽ đường nối với mũi tên tam giác rỗng phong cách sơ đồ điện tử kinh điển"""
    ax.plot([x_start, x_end], [y_start, y_end], color=color, lw=lw, zorder=5)
    dx = x_end - x_start
    dy = y_end - y_start
    angle = math.atan2(dy, dx)
    a1_x = x_end - size * math.cos(angle - math.pi / 6)
    a1_y = y_end - size * math.sin(angle - math.pi / 6)
    a2_x = x_end - size * math.cos(angle + math.pi / 6)
    a2_y = y_end - size * math.sin(angle + math.pi / 6)
    ax.plot([a1_x, x_end, a2_x], [a1_y, y_end, a2_y], color=color, lw=lw, zorder=6)

def draw_bi_arrow(ax, x_start, y_start, x_end, y_end, size=0.18, lw=1.6, color='#000000'):
    """Vẽ đường bus 2 chiều có mũi tên ở cả 2 đầu"""
    draw_open_arrow(ax, x_start, y_start, x_end, y_end, size=size, lw=lw, color=color)
    draw_open_arrow(ax, x_end, y_end, x_start, y_start, size=size, lw=lw, color=color)

def create_stage1():
    fig, ax = plt.subplots(figsize=(6.5, 6.0), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.add_patch(Rectangle((0, 0), 10, 10, facecolor='#FFFFFF', zorder=0))

    # Tiêu đề
    ax.text(5.0, 9.5, "GIAI ĐOẠN 1: KHỐI CỐT LÕI & BỔ SUNG SRAM", 
            fontsize=11.5, fontweight='bold', ha='center', va='center')
    ax.plot([0.8, 9.2], [9.15, 9.15], color='#000000', lw=1.2)

    # Khối 1: CPU Master (picorv32.v)
    ax.add_patch(Rectangle((0.8, 4.2), 3.4, 4.2, facecolor='#FFFFFF', edgecolor='#000000', lw=2.0))
    ax.text(2.5, 8.0, "CPU MASTER", fontsize=10, fontweight='bold', ha='center')
    ax.text(2.5, 7.5, "picorv32.v", fontsize=10, fontweight='bold', family='monospace', ha='center')
    ax.plot([1.0, 4.0], [7.15, 7.15], color='#000000', lw=0.8)
    ax.text(2.5, 6.7, "• RV32I Core (ALU, 32 Regs)\n• Native Memory Bus\n• Chưa có RAM / ROM nội\n• mem_valid, mem_ready\n• mem_addr, wdata/rdata", 
            fontsize=8.2, ha='center', va='top', family='sans-serif', linespacing=1.35)

    # Khối 2: SPIMEMIO (spimemio.v)
    ax.add_patch(Rectangle((5.8, 5.5), 3.4, 2.9, facecolor='#FFFFFF', edgecolor='#000000', lw=2.0))
    ax.text(7.5, 8.0, "SLAVE 1: FLASH CONTROLLER", fontsize=8.5, fontweight='bold', ha='center')
    ax.text(7.5, 7.55, "spimemio.v", fontsize=10, fontweight='bold', family='monospace', ha='center')
    ax.plot([6.0, 9.0], [7.25, 7.25], color='#000000', lw=0.8)
    ax.text(7.5, 6.9, "• Cơ chế XIP (eXecute-In-Place)\n• Đọc mã lệnh trực tiếp\n• KHÔNG THỂ LƯU STACK C!\n• Giao tiếp SPI Flash ngoài", 
            fontsize=8.0, ha='center', va='top', linespacing=1.35)

    # Khối 3: data_sram (Bổ sung mới)
    ax.add_patch(Rectangle((5.8, 1.2), 3.4, 3.2, facecolor='#F8F8F8', edgecolor='#000000', lw=2.2, linestyle='--'))
    ax.text(7.5, 4.0, "[BỔ SUNG MỚI]", fontsize=9, fontweight='bold', color='#000000', ha='center')
    ax.text(7.5, 3.55, "SLAVE 0: data_sram", fontsize=9.5, fontweight='bold', family='monospace', ha='center')
    ax.plot([6.0, 9.0], [3.25, 3.25], color='#000000', lw=0.8)
    ax.text(7.5, 2.9, "• 1KB On-Chip SRAM (256x32)\n• Phản hồi 1 chu kỳ clock\n• Chứa Stack Pointer (sp)\n• Lưu trữ biến cục bộ & mảng C\n• Cho phép ghi/đọc tức thời", 
            fontsize=8.0, ha='center', va='top', linespacing=1.35)

    # Đường nối Bus
    draw_bi_arrow(ax, 4.2, 7.0, 5.8, 7.0, lw=1.6)
    ax.text(5.0, 7.2, "Native Bus\n(XIP Read)", fontsize=7.5, ha='center', va='bottom', family='monospace')

    draw_open_arrow(ax, 2.5, 4.2, 2.5, 2.8, lw=1.6)
    draw_bi_arrow(ax, 2.5, 2.8, 5.8, 2.8, lw=1.6)
    ax.text(4.2, 3.0, "Native Bus (RW 1-Cycle)", fontsize=7.5, ha='center', va='bottom', family='monospace')

    # Chip Flash ngoài
    ax.add_patch(Rectangle((6.2, 8.8), 2.6, 0.55, facecolor='#FFFFFF', edgecolor='#000000', lw=1.2))
    ax.text(7.5, 9.07, "External SPI Flash (W25Q128)", fontsize=7.5, fontweight='bold', ha='center', va='center')
    draw_bi_arrow(ax, 7.5, 8.4, 7.5, 8.8, lw=1.2)

    # Hộp Callout kết luận dưới cùng
    ax.add_patch(Rectangle((0.8, 0.4), 8.4, 0.65, facecolor='#EEEEEE', edgecolor='#000000', lw=1.0))
    ax.text(5.0, 0.72, "KẾT LUẬN: Bắt buộc cần 1KB SRAM nội bộ để chương trình C có thể cấp phát Stack & biến!", 
            fontsize=7.8, fontweight='bold', ha='center', va='center')

    plt.tight_layout()
    out_path = os.path.join(os.path.dirname(__file__), "stage1_bw_diagram.png")
    plt.savefig(out_path, dpi=300, facecolor='#FFFFFF', bbox_inches='tight', pad_inches=0.12)
    plt.close()
    print("Created stage1_bw_diagram.png")

def create_stage2():
    fig, ax = plt.subplots(figsize=(6.5, 6.0), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.add_patch(Rectangle((0, 0), 10, 10, facecolor='#FFFFFF', zorder=0))

    # Tiêu đề
    ax.text(5.0, 9.5, "GIAI ĐOẠN 2: THIẾT KẾ CẦU NỐI BUS INTERCONNECT", 
            fontsize=11.5, fontweight='bold', ha='center', va='center')
    ax.plot([0.8, 9.2], [9.15, 9.15], color='#000000', lw=1.2)

    # Master: picorv32.v
    ax.add_patch(Rectangle((0.6, 3.8), 2.5, 3.8, facecolor='#FFFFFF', edgecolor='#000000', lw=2.0))
    ax.text(1.85, 7.2, "CPU MASTER", fontsize=9.5, fontweight='bold', ha='center')
    ax.text(1.85, 6.75, "picorv32.v", fontsize=10, fontweight='bold', family='monospace', ha='center')
    ax.plot([0.8, 2.9], [6.4, 6.4], color='#000000', lw=0.8)
    ax.text(1.85, 5.9, "1 CỔNG BUS DUY NHẤT:\n• cpu_mem_valid\n• cpu_mem_addr[31:0]\n• cpu_mem_wdata[31:0]\n• cpu_mem_ready (chờ)\n• cpu_mem_rdata", 
            fontsize=7.5, ha='center', va='top', linespacing=1.3)

    # Center: soc_interconnect.v
    ax.add_patch(Rectangle((3.7, 2.0), 3.2, 6.2, facecolor='#F9F9F9', edgecolor='#000000', lw=2.2))
    ax.text(5.3, 7.8, "CẦU NỐI BUS [MỚI]", fontsize=9.5, fontweight='bold', ha='center')
    ax.text(5.3, 7.4, "soc_interconnect.v", fontsize=10, fontweight='bold', family='monospace', ha='center')
    ax.plot([3.9, 6.7], [7.1, 7.1], color='#000000', lw=0.8)
    
    dec_text = (
        "1. Giải mã địa chỉ (0 cycle):\n"
        "• addr < 0x0400 -> sel_sram\n"
        "• 0x0010_0000 -> sel_spimem\n"
        "• 0x0200_0000 -> sel_spicfg\n"
        "\n"
        "2. Dồn kênh phản hồi (MUX):\n"
        "cpu_mem_ready = \n"
        "  sram_ready  ||\n"
        "  spimem_ready||\n"
        "  sel_spicfg;\n"
        "cpu_mem_rdata = \n"
        "  sel_sram ? sram_rdata : \n"
        "  spimem_rdata;"
    )
    ax.text(5.3, 6.9, dec_text, fontsize=7.2, family='monospace', ha='center', va='top', linespacing=1.2)

    # Slaves bên phải
    # Slave 0: data_sram
    ax.add_patch(Rectangle((7.4, 5.5), 2.2, 2.6, facecolor='#FFFFFF', edgecolor='#000000', lw=1.8))
    ax.text(8.5, 7.7, "SLAVE 0: SRAM", fontsize=8.5, fontweight='bold', ha='center')
    ax.text(8.5, 7.25, "data_sram (1KB)", fontsize=8.2, family='monospace', ha='center')
    ax.plot([7.6, 9.4], [7.0, 7.0], color='#000000', lw=0.6)
    ax.text(8.5, 6.7, "0x0000_0000\nđến\n0x0000_03FF\n(sram_ready = 1)", fontsize=7.5, ha='center', va='top', linespacing=1.2)

    # Slave 1: spimemio.v
    ax.add_patch(Rectangle((7.4, 2.0), 2.2, 2.8, facecolor='#FFFFFF', edgecolor='#000000', lw=1.8))
    ax.text(8.5, 4.4, "SLAVE 1: FLASH", fontsize=8.5, fontweight='bold', ha='center')
    ax.text(8.5, 3.95, "spimemio.v", fontsize=8.2, family='monospace', ha='center')
    ax.plot([7.6, 9.4], [3.7, 3.7], color='#000000', lw=0.6)
    ax.text(8.5, 3.4, "0x0010_0000\nđến\n0x00FF_FFFF\n(spimem_ready)", fontsize=7.5, ha='center', va='top', linespacing=1.2)

    # Mũi tên kết nối
    draw_bi_arrow(ax, 3.1, 5.7, 3.7, 5.7, lw=1.8)
    draw_bi_arrow(ax, 6.9, 6.8, 7.4, 6.8, lw=1.6)
    ax.text(7.15, 7.0, "sel_sram", fontsize=7.0, ha='center', va='bottom', family='monospace')

    draw_bi_arrow(ax, 6.9, 3.4, 7.4, 3.4, lw=1.6)
    ax.text(7.15, 3.6, "sel_spimem", fontsize=7.0, ha='center', va='bottom', family='monospace')

    # Callout
    ax.add_patch(Rectangle((0.6, 0.4), 8.8, 0.7, facecolor='#EEEEEE', edgecolor='#000000', lw=1.0))
    ax.text(5.0, 0.75, "KẾT LUẬN: soc_interconnect.v là bộ 'cảnh sát giao thông' phân luồng 1 CPU tới nhiều bộ nhớ!", 
            fontsize=7.8, fontweight='bold', ha='center', va='center')

    plt.tight_layout()
    out_path = os.path.join(os.path.dirname(__file__), "stage2_bw_diagram.png")
    plt.savefig(out_path, dpi=300, facecolor='#FFFFFF', bbox_inches='tight', pad_inches=0.12)
    plt.close()
    print("Created stage2_bw_diagram.png")

def create_stage3():
    fig, ax = plt.subplots(figsize=(6.5, 6.0), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.add_patch(Rectangle((0, 0), 10, 10, facecolor='#FFFFFF', zorder=0))

    # Tiêu đề
    ax.text(5.0, 9.5, "GIAI ĐOẠN 3: ĐỒNG THIẾT KẾ PHẦN CỨNG - PHẦN MỀM", 
            fontsize=11.0, fontweight='bold', ha='center', va='center')
    ax.plot([0.8, 9.2], [9.15, 9.15], color='#000000', lw=1.2)

    # Cột Trái: PHẦN CỨNG (RTL)
    ax.add_patch(Rectangle((0.6, 2.2), 3.8, 6.5, facecolor='#FFFFFF', edgecolor='#000000', lw=2.0))
    ax.text(2.5, 8.3, "[PHẦN CỨNG RTL]", fontsize=9.5, fontweight='bold', ha='center')
    ax.text(2.5, 7.85, "picorv32_soc.v", fontsize=9.5, fontweight='bold', family='monospace', ha='center')
    ax.plot([0.8, 4.2], [7.55, 7.55], color='#000000', lw=0.8)

    hw_text = (
        "1. Tham số Vector Reset:\n"
        "parameter [31:0]\n"
        "PROGADDR_RESET = \n"
        "  32'h0025_0000;\n"
        "\n"
        "2. Tham số Đỉnh Stack:\n"
        "parameter [31:0]\n"
        "STACKADDR = \n"
        "  32'h0000_0400;\n"
        "\n"
        "3. Ngay khi nhả resetn=1:\n"
        "CPU nạp PC = 0x0025_0000\n"
        "và phát chu kỳ đọc bus đầu tiên."
    )
    ax.text(2.5, 7.3, hw_text, fontsize=7.4, family='monospace', ha='center', va='top', linespacing=1.2)

    # Cột Phải: PHẦN MỀM (FIRMWARE C & ASM)
    ax.add_patch(Rectangle((5.6, 2.2), 3.8, 6.5, facecolor='#FFFFFF', edgecolor='#000000', lw=2.0))
    ax.text(7.5, 8.3, "[PHẦN MỀM FIRMWARE]", fontsize=9.5, fontweight='bold', ha='center')
    ax.text(7.5, 7.85, "sections.lds & start.s", fontsize=9.0, fontweight='bold', family='monospace', ha='center')
    ax.plot([5.8, 9.2], [7.55, 7.55], color='#000000', lw=0.8)

    sw_text = (
        "1. sections.lds (Linker):\n"
        "FLASH: ORIGIN = 0x00250000\n"
        "RAM  : ORIGIN = 0x00000000\n"
        "_stack_top = 0x0400;\n"
        "\n"
        "2. start.s (Bootstrap ASM):\n"
        "_start:\n"
        "  lui  sp, %hi(_stack_top)\n"
        "  addi sp, sp, %lo(_stack_top)\n"
        "  call main  # Nhảy vào C!\n"
        "\n"
        "3. main.c:\n"
        "Mã nguồn C thực thi!"
    )
    ax.text(7.5, 7.3, sw_text, fontsize=7.4, family='monospace', ha='center', va='top', linespacing=1.2)

    # Mũi tên ánh xạ 1-1 giữa RTL và Firmware
    draw_bi_arrow(ax, 4.4, 6.3, 5.6, 6.3, lw=1.8)
    ax.text(5.0, 6.5, "100% Khớp\n0x0025_0000", fontsize=7.2, fontweight='bold', ha='center', va='bottom')

    draw_bi_arrow(ax, 4.4, 4.5, 5.6, 4.5, lw=1.8)
    ax.text(5.0, 4.7, "100% Khớp\n_stack_top", fontsize=7.2, fontweight='bold', ha='center', va='bottom')

    # Callout
    ax.add_patch(Rectangle((0.6, 0.4), 8.8, 1.2, facecolor='#EEEEEE', edgecolor='#000000', lw=1.0))
    ax.text(5.0, 1.25, "KẾT QUẢ ĐỒNG THIẾT KẾ (CO-DESIGN BOOTSTRAP):", fontsize=8.2, fontweight='bold', ha='center')
    ax.text(5.0, 0.8, "Ngay khi bật nguồn vi mạch ASIC, CPU tự động lấy lệnh từ Flash ngoài và thiết lập\nngăn xếp trong 1KB RAM, sẵn sàng chạy hàm main() của C mà không cần can thiệp!", 
            fontsize=7.4, ha='center', va='center', linespacing=1.25)

    plt.tight_layout()
    out_path = os.path.join(os.path.dirname(__file__), "stage3_bw_diagram.png")
    plt.savefig(out_path, dpi=300, facecolor='#FFFFFF', bbox_inches='tight', pad_inches=0.12)
    plt.close()
    print("Created stage3_bw_diagram.png")

def create_stage4():
    fig, ax = plt.subplots(figsize=(6.5, 6.0), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.add_patch(Rectangle((0, 0), 10, 10, facecolor='#FFFFFF', zorder=0))

    # Tiêu đề
    ax.text(5.0, 9.5, "GIAI ĐOẠN 4: MỞ RỘNG NGOẠI VI MMIO CÓ FIFO CHỐNG TRÀN", 
            fontsize=10.5, fontweight='bold', ha='center', va='center')
    ax.plot([0.8, 9.2], [9.15, 9.15], color='#000000', lw=1.2)

    # Trái: soc_interconnect.v
    ax.add_patch(Rectangle((0.6, 2.2), 3.2, 6.5, facecolor='#F9F9F9', edgecolor='#000000', lw=2.0))
    ax.text(2.2, 8.3, "soc_interconnect.v", fontsize=9.5, fontweight='bold', family='monospace', ha='center')
    ax.text(2.2, 7.9, "[Bộ Giải Mã 4-bit Cao]", fontsize=8.0, ha='center')
    ax.plot([0.8, 3.6], [7.6, 7.6], color='#000000', lw=0.8)

    inter_text = (
        "Giải mã addr[31:28]:\n"
        "\n"
        "• 4'h1 (0x1000_0000)\n"
        "  -> sel_rfid = 1\n"
        "\n"
        "• 4'h3 (0x3000_0000)\n"
        "  -> sel_uart = 1\n"
        "\n"
        "• 4'h4 (0x4000_0000)\n"
        "  -> sel_gpio = 1\n"
        "\n"
        "Phản hồi 1 chu kỳ clock:\n"
        "rfid_ready, uart_ready,\n"
        "gpio_ready = 1"
    )
    ax.text(2.2, 7.3, inter_text, fontsize=7.5, family='monospace', ha='center', va='top', linespacing=1.25)

    # Phải: 3 Ngoại vi MMIO
    # Ngoại vi 1: Slave 2 (RFID)
    ax.add_patch(Rectangle((4.8, 6.7), 4.6, 2.0, facecolor='#FFFFFF', edgecolor='#000000', lw=1.8))
    ax.text(7.1, 8.35, "SLAVE 2: RFID RDM6300 (uart_mmio.v)", fontsize=8.2, fontweight='bold', ha='center')
    ax.text(7.1, 7.95, "Địa chỉ: 0x1000_0000 & 0x1000_0004", fontsize=7.5, family='monospace', ha='center')
    ax.plot([5.0, 9.2], [7.7, 7.7], color='#000000', lw=0.6)
    ax.text(7.1, 7.4, "• sync_2ff.v: Chống siêu ổn định (Metastability)\n• sync_fifo.v: 32B RX FIFO chống mất gói thẻ\n• Baudrate 9600 bps", 
            fontsize=7.2, ha='center', va='top', linespacing=1.2)

    # Ngoại vi 2: Slave 3 (Host UART)
    ax.add_patch(Rectangle((4.8, 4.4), 4.6, 2.0, facecolor='#FFFFFF', edgecolor='#000000', lw=1.8))
    ax.text(7.1, 6.05, "SLAVE 3: HOST PC UART (uart_mmio.v)", fontsize=8.2, fontweight='bold', ha='center')
    ax.text(7.1, 5.65, "Địa chỉ: 0x3000_0000 & 0x3000_0004", fontsize=7.5, family='monospace', ha='center')
    ax.plot([5.0, 9.2], [5.4, 5.4], color='#000000', lw=0.6)
    ax.text(7.1, 5.1, "• 32B RX FIFO: Nhận lệnh quản trị PC\n• 32B TX FIFO: Xuất log thẻ & audit trail\n• Giao tiếp máy tính Full-Duplex", 
            fontsize=7.2, ha='center', va='top', linespacing=1.2)

    # Ngoại vi 3: Slave 4 (GPIO)
    ax.add_patch(Rectangle((4.8, 2.2), 4.6, 1.9, facecolor='#FFFFFF', edgecolor='#000000', lw=1.8))
    ax.text(7.1, 3.8, "SLAVE 4: GPIO (soc_gpio_mmio.v)", fontsize=8.2, fontweight='bold', ha='center')
    ax.text(7.1, 3.4, "Địa chỉ: 0x4000_0000", fontsize=7.5, family='monospace', ha='center')
    ax.plot([5.0, 9.2], [3.15, 3.15], color='#000000', lw=0.6)
    ax.text(7.1, 2.85, "• 16 LED trạng thái (Bit 0: Alive, Bit 1/2: RFID)\n• Điều khiển Relay chốt điện mở cửa", 
            fontsize=7.2, ha='center', va='top', linespacing=1.2)

    # Đường bus kết nối
    draw_bi_arrow(ax, 3.8, 7.7, 4.8, 7.7, lw=1.5)
    draw_bi_arrow(ax, 3.8, 5.4, 4.8, 5.4, lw=1.5)
    draw_bi_arrow(ax, 3.8, 3.1, 4.8, 3.1, lw=1.5)

    # Callout
    ax.add_patch(Rectangle((0.6, 0.4), 8.8, 1.1, facecolor='#EEEEEE', edgecolor='#000000', lw=1.0))
    ax.text(5.0, 1.15, "Ý NGHĨA KỸ THUẬT CỦA HÀNG ĐỢI PHẦN CỨNG (FIFO 32 BYTES):", fontsize=8.0, fontweight='bold', ha='center')
    ax.text(5.0, 0.75, "Khi CPU bận ghi dữ liệu vào Flash (mất vài ms), nếu đầu đọc RFID liên tục gửi dữ liệu,\nhàng đợi FIFO 32B sẽ tự động đệm toàn bộ chuỗi 14-byte của thẻ mà không bị rơi rụng!", 
            fontsize=7.3, ha='center', va='center', linespacing=1.25)

    plt.tight_layout()
    out_path = os.path.join(os.path.dirname(__file__), "stage4_bw_diagram.png")
    plt.savefig(out_path, dpi=300, facecolor='#FFFFFF', bbox_inches='tight', pad_inches=0.12)
    plt.close()
    print("Created stage4_bw_diagram.png")

def create_stage5():
    fig, ax = plt.subplots(figsize=(6.5, 6.0), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.add_patch(Rectangle((0, 0), 10, 10, facecolor='#FFFFFF', zorder=0))

    # Tiêu đề
    ax.text(5.0, 9.5, "GIAI ĐOẠN 5: TẦNG C TƯƠNG TÁC QUA VOLATILE MMIO", 
            fontsize=11.0, fontweight='bold', ha='center', va='center')
    ax.plot([0.8, 9.2], [9.15, 9.15], color='#000000', lw=1.2)

    # Tầng 1: Tầng Ứng Dụng C
    ax.add_patch(Rectangle((0.8, 6.8), 8.4, 2.0, facecolor='#FFFFFF', edgecolor='#000000', lw=2.0))
    ax.text(5.0, 8.45, "TẦNG ỨNG DỤNG C (access_control.c & uart.c)", fontsize=9.0, fontweight='bold', ha='center')
    ax.plot([1.0, 9.0], [8.15, 8.15], color='#000000', lw=0.6)
    c_app_text = (
        "uint32_t d = REG_RFID_UART_DAT; // Đọc byte thẻ từ FIFO\n"
        "if (d != 0xFFFFFFFF) rdm6300_push((uint8_t)d);\n"
        "if (granted) REG_GPIO_LEDS = 0x0004; // Bật LED xanh & mở cửa"
    )
    ax.text(5.0, 7.8, c_app_text, fontsize=7.5, family='monospace', ha='center', va='top', linespacing=1.25)

    # Mũi tên đi xuống Tầng 2
    draw_open_arrow(ax, 5.0, 6.8, 5.0, 6.1, lw=1.8)
    ax.text(5.2, 6.45, "Gọi Macro MMIO", fontsize=7.2, va='center', family='sans-serif')

    # Tầng 2: soc_regs.h
    ax.add_patch(Rectangle((0.8, 4.0), 8.4, 2.1, facecolor='#F9F9F9', edgecolor='#000000', lw=2.0))
    ax.text(5.0, 5.8, "TẦNG ĐỊNH NGHĨA CON TRỎ PHẦN CỨNG (firmware/common/soc_regs.h)", fontsize=8.5, fontweight='bold', ha='center')
    ax.plot([1.0, 9.0], [5.5, 5.5], color='#000000', lw=0.6)
    regs_text = (
        "#define REG_RFID_UART_DAT (*(volatile uint32_t*)0x10000004)\n"
        "#define REG_PC_UART_DAT   (*(volatile uint32_t*)0x30000004)\n"
        "#define REG_GPIO_LEDS     (*(volatile uint32_t*)0x40000000)\n"
        "--> volatile: Ép GCC luôn phát lệnh load/store bus, không lưu tạm thanh ghi!"
    )
    ax.text(5.0, 5.2, regs_text, fontsize=7.3, family='monospace', ha='center', va='top', linespacing=1.25)

    # Mũi tên đi xuống Tầng 3
    draw_open_arrow(ax, 5.0, 4.0, 5.0, 3.3, lw=1.8)
    ax.text(5.2, 3.65, "Biên dịch sang lệnh lw / sw", fontsize=7.2, va='center', family='sans-serif')

    # Tầng 3: Tầng Phần Cứng RTL Thực Thi
    ax.add_patch(Rectangle((0.8, 1.4), 8.4, 1.9, facecolor='#FFFFFF', edgecolor='#000000', lw=2.0))
    ax.text(5.0, 2.95, "TẦNG PHẦN CỨNG RTL THỰC THI (1 Chu Kỳ Clock = 20ns @ 50MHz)", fontsize=8.5, fontweight='bold', ha='center')
    ax.plot([1.0, 9.0], [2.65, 2.65], color='#000000', lw=0.6)
    hw_exec = (
        "1. CPU phát: cpu_mem_valid=1, addr=0x1000_0004\n"
        "2. soc_interconnect.v kích hoạt sel_rfid=1\n"
        "3. uart_mmio.v pop 1 byte từ RX FIFO, trả về cpu_mem_rdata & rfid_ready=1\n"
        "4. Nếu FIFO rỗng: Trả về 0xFFFFFFFF ngay tức thì -> CPU KHÔNG BỊ TREO BUS!"
    )
    ax.text(5.0, 2.45, hw_exec, fontsize=7.3, family='monospace', ha='center', va='top', linespacing=1.2)

    # Callout
    ax.add_patch(Rectangle((0.8, 0.4), 8.4, 0.7, facecolor='#EEEEEE', edgecolor='#000000', lw=1.0))
    ax.text(5.0, 0.75, "KẾT LUẬN: Giao tiếp C và RTL đạt tính TRONG SUỐT (Transparent) và KHÔNG KHÓA (Non-blocking)!", 
            fontsize=7.6, fontweight='bold', ha='center', va='center')

    plt.tight_layout()
    out_path = os.path.join(os.path.dirname(__file__), "stage5_bw_diagram.png")
    plt.savefig(out_path, dpi=300, facecolor='#FFFFFF', bbox_inches='tight', pad_inches=0.12)
    plt.close()
    print("Created stage5_bw_diagram.png")

if __name__ == '__main__':
    create_stage1()
    create_stage2()
    create_stage3()
    create_stage4()
    create_stage5()
    print("All 5 stage diagrams generated successfully!")
