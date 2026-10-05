# -*- coding: utf-8 -*-
"""
Script: generate_uart_diagram.py
Vẽ sơ đồ khối kiến trúc vi mạch UART RTL (Black & White Textbook Draw.io Schematic Block Diagram)
Tối ưu hóa hiển thị 5 tầng phần cứng: 
sync_2ff.v -> simpleuart.v (16x Baud Gen & Sampler) -> RX FSM -> sync_fifo.v (32B) -> uart_mmio.v (Non-blocking MMIO Bus)
"""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
import math

def draw_open_arrow(ax, x_start, y_start, x_end, y_end, size=0.18, lw=1.5, color='#000000'):
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

def draw_bi_arrow(ax, x_start, y_start, x_end, y_end, size=0.16, lw=1.5, color='#000000'):
    """Vẽ đường bus 2 chiều có mũi tên ở cả 2 đầu"""
    draw_open_arrow(ax, x_start, y_start, x_end, y_end, size=size, lw=lw, color=color)
    draw_open_arrow(ax, x_end, y_end, x_start, y_start, size=size, lw=lw, color=color)

def create_uart_diagram():
    fig, ax = plt.subplots(figsize=(6.5, 6.0), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.add_patch(Rectangle((0, 0), 10, 10, facecolor='#FFFFFF', zorder=0))

    # Tiêu đề sơ đồ
    ax.text(5.0, 9.6, "KIẾN TRÚC VI MẠCH UART MMIO & FIFO (RTL)", 
            fontsize=11.5, fontweight='bold', ha='center', va='center')
    ax.plot([0.8, 9.2], [9.25, 9.25], color='#000000', lw=1.2)

    # 1. Tầng 1: sync_2ff.v (Đồng bộ miền xung CDC)
    ax.add_patch(Rectangle((0.6, 6.8), 2.6, 2.1, facecolor='#FFFFFF', edgecolor='#000000', lw=1.8))
    ax.text(1.9, 8.6, "TẦNG 1: CDC 2-FF", fontsize=9.0, fontweight='bold', ha='center')
    ax.text(1.9, 8.2, "sync_2ff.v", fontsize=9.5, fontweight='bold', family='monospace', ha='center')
    ax.plot([0.8, 3.0], [7.95, 7.95], color='#000000', lw=0.8)
    ax.text(1.9, 7.7, "• In: rx_i (Asynch TTL)\n• 2 tầng Flip-Flop (50MHz)\n• Khử Metastability vật lý\n• MTBF > 1.000 năm", 
            fontsize=7.5, ha='center', va='top', linespacing=1.2)

    # Tín hiệu vào rx_i
    draw_open_arrow(ax, 0.0, 7.85, 0.6, 7.85, lw=1.5)
    ax.text(0.3, 8.05, "rx_i", fontsize=8.0, fontweight='bold', family='monospace', ha='center')

    # 2. Tầng 2: simpleuart.v (Bộ chia tần & Lấy mẫu 16x)
    ax.add_patch(Rectangle((3.7, 6.8), 2.8, 2.1, facecolor='#FFFFFF', edgecolor='#000000', lw=1.8))
    ax.text(5.1, 8.6, "TẦNG 2: 16x BAUD GEN", fontsize=9.0, fontweight='bold', ha='center')
    ax.text(5.1, 8.2, "simpleuart.v", fontsize=9.5, fontweight='bold', family='monospace', ha='center')
    ax.plot([3.9, 6.3], [7.95, 7.95], color='#000000', lw=0.8)
    ax.text(5.1, 7.7, "• Divisor = 5208 (9600 baud)\n• Bộ lấy mẫu 16x Oversampling\n• Bầu đa số 3 mẫu (Tick 7,8,9)\n• Triệt tiêu 100% nhiễu Glitch", 
            fontsize=7.5, ha='center', va='top', linespacing=1.2)

    # Mũi tên từ Tầng 1 -> Tầng 2
    draw_open_arrow(ax, 3.2, 7.85, 3.7, 7.85, lw=1.5)
    ax.text(3.45, 8.05, "rx_sync", fontsize=7.2, family='monospace', ha='center')

    # 3. Tầng 3: RX FSM Máy trạng thái thu nhận
    ax.add_patch(Rectangle((7.0, 6.8), 2.5, 2.1, facecolor='#FFFFFF', edgecolor='#000000', lw=1.8))
    ax.text(8.25, 8.6, "TẦNG 3: RX FSM", fontsize=9.0, fontweight='bold', ha='center')
    ax.text(8.25, 8.2, "simpleuart.v", fontsize=9.5, fontweight='bold', family='monospace', ha='center')
    ax.plot([7.2, 9.3], [7.95, 7.95], color='#000000', lw=0.8)
    ax.text(8.25, 7.7, "• Bắt Start Bit = 0\n• Dịch 8-bit LSB-first\n• Kiểm tra Stop Bit = 1\n• Phát xung rx_valid", 
            fontsize=7.5, ha='center', va='top', linespacing=1.2)

    # Mũi tên từ Tầng 2 -> Tầng 3
    draw_open_arrow(ax, 6.5, 7.85, 7.0, 7.85, lw=1.5)
    ax.text(6.75, 8.05, "sample", fontsize=7.2, family='monospace', ha='center')

    # 4. Tầng 4: sync_fifo.v (Hàng đợi FIFO 32B độc lập)
    ax.add_patch(Rectangle((5.2, 3.4), 4.3, 2.6, facecolor='#F8F8F8', edgecolor='#000000', lw=2.0))
    ax.text(7.35, 5.7, "TẦNG 4: HÀNG ĐỢI ĐỆM 32 BYTES FIFO", fontsize=8.8, fontweight='bold', ha='center')
    ax.text(7.35, 5.3, "sync_fifo.v (32x8-bit RAM)", fontsize=9.5, fontweight='bold', family='monospace', ha='center')
    ax.plot([5.4, 9.3], [5.05, 5.05], color='#000000', lw=0.8)
    ax.text(7.35, 4.8, "• Quản lý wr_ptr[4:0] & rd_ptr[4:0] độc lập\n• Bộ đếm count[5:0], cờ empty / full\n• Đệm trọn vẹn 14 byte chuỗi thẻ RFID\n• BẢO TOÀN DỮ LIỆU KHI CPU GHI FLASH!", 
            fontsize=7.5, ha='center', va='top', linespacing=1.25)

    # Mũi tên từ Tầng 3 xuống Tầng 4
    draw_open_arrow(ax, 8.25, 6.8, 8.25, 6.0, lw=1.5)
    ax.text(8.4, 6.4, "rx_data[7:0]\n+ wr_en", fontsize=7.2, family='monospace', ha='left', va='center')

    # 5. Tầng 5: uart_mmio.v (Giao tiếp Bus Native MMIO)
    ax.add_patch(Rectangle((0.6, 3.4), 3.8, 2.6, facecolor='#FFFFFF', edgecolor='#000000', lw=2.0))
    ax.text(2.5, 5.7, "TẦNG 5: GIẢI MÃ BUS MMIO", fontsize=9.0, fontweight='bold', ha='center')
    ax.text(2.5, 5.3, "uart_mmio.v", fontsize=9.5, fontweight='bold', family='monospace', ha='center')
    ax.plot([0.8, 4.2], [5.05, 5.05], color='#000000', lw=0.8)
    ax.text(2.5, 4.8, "• 0x1000_0000: REG_DIV (Prescaler)\n• 0x1000_0004: REG_DAT (RX FIFO)\n• FIFO Empty -> Trả về 0xFFFFFFFF\n• Phản hồi mem_ready = 1 (1 cycle)", 
            fontsize=7.5, ha='center', va='top', linespacing=1.25)

    # Đường nối giữa Tầng 4 (FIFO) và Tầng 5 (MMIO)
    draw_bi_arrow(ax, 5.2, 4.4, 4.4, 4.4, lw=1.5)
    ax.text(4.8, 4.65, "rd_en\nrdata", fontsize=7.2, family='monospace', ha='center')

    # Cổng Bus nối với CPU PicoRV32 Interconnect
    ax.add_patch(Rectangle((0.6, 1.4), 8.9, 1.4, facecolor='#F0F4F8', edgecolor='#000000', lw=1.8, linestyle='--'))
    ax.text(5.0, 2.5, "CẦU BUS TRUNG TÂM SOC INTERCONNECT & CPU PICORV32", fontsize=9.0, fontweight='bold', ha='center')
    ax.text(5.0, 2.05, "• CPU đọc 0x1000_0004 qua lệnh C: uint32_t d = REG_RFID_UART_DAT;\n• Non-blocking Bus: 1 chu kỳ clock duy nhất (20 ns @ 50 MHz), KHÔNG TREO CPU!", 
            fontsize=7.8, ha='center', va='top', linespacing=1.2)

    # Đường nối từ MMIO xuống Bus
    draw_bi_arrow(ax, 2.5, 3.4, 2.5, 2.8, lw=1.6)
    ax.text(2.65, 3.1, "Native Bus (mem_valid, ready, rdata)", fontsize=7.2, family='monospace', ha='left', va='center')

    # Hộp Callout kết luận dưới cùng
    ax.add_patch(Rectangle((0.6, 0.35), 8.9, 0.70, facecolor='#E2E8F0', edgecolor='#000000', lw=1.2))
    ax.text(5.0, 0.70, "KẾT LUẬN: 5 tầng phần cứng tự động đệm toàn bộ chuỗi thẻ độc lập hoàn toàn với CPU!", 
            fontsize=8.0, fontweight='bold', ha='center', va='center')

    plt.tight_layout()
    out_path = os.path.join(os.path.dirname(__file__), "uart_architecture_bw_diagram.png")
    plt.savefig(out_path, dpi=300, facecolor='#FFFFFF', bbox_inches='tight', pad_inches=0.12)
    plt.close()
    print("Created uart_architecture_bw_diagram.png successfully!")

if __name__ == "__main__":
    create_uart_diagram()
