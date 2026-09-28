# -*- coding: utf-8 -*-
"""
Script: create_presentation.py
Generates an executive, publication-grade 16:9 widescreen PowerPoint presentation (pptx)
from the comprehensive project report:
"Báo Cáo Đồ Án: Thiết Kế Hệ Thống Quét và Xử Lý Dữ Liệu Thẻ RFID Tích Hợp CPU RISC-V PicoRV32 Quản Lý Dữ Liệu Trên Flash"

Fully integrates the 4 requested design step slides:
- 3.1. Bước 1: Lựa chọn tài nguyên phần cứng (RDM6300, Basys 3) và phần mềm
- 3.2. Bước 2: Thiết kế firmware và định nghĩa giao thức giao tiếp trước (Software-First)
- 3.3. Bước 3: Thiết kế hệ thống xử lý phần cứng: nhân CPU PicoRV32 và 1KB Data SRAM
- 3.4. Bước 4: Thiết kế bộ điều khiển bộ nhớ ngoài SPI Flash Controller (spimemio.v)
Total: 16 comprehensive, publication-grade slides with high-res figures and zero awkward whitespace.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette Constants
    C_NAVY_DARK   = RGBColor(11, 19, 43)     # #0B132B
    C_NAVY_MID    = RGBColor(28, 37, 65)     # #1C2541
    C_BLUE_ACCENT = RGBColor(37, 99, 235)    # #2563EB
    C_CYAN_ACCENT = RGBColor(14, 165, 233)   # #0EA5E9
    C_BG_LIGHT    = RGBColor(248, 250, 252)  # #F8FAFC
    C_WHITE       = RGBColor(255, 255, 255)  # #FFFFFF
    C_CARD_BG     = RGBColor(255, 255, 255)  # #FFFFFF
    C_CARD_BORDER = RGBColor(203, 213, 225)  # #CBD5E1
    C_TEXT_DARK   = RGBColor(15, 23, 42)     # #0F172A
    C_TEXT_MUTED  = RGBColor(71, 85, 105)    # #475569
    C_GREEN       = RGBColor(16, 185, 129)   # #10B981
    C_AMBER       = RGBColor(217, 119, 6)    # #D97706
    C_PURPLE      = RGBColor(124, 58, 237)   # #7C3AED
    C_ROSE        = RGBColor(225, 29, 72)    # #E11D48

    cur_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(cur_dir)

    img_fig1 = os.path.join(cur_dir, "fig1_block_diagram.png")
    img_fig2 = os.path.join(cur_dir, "fig2_rdm6300_subsystem.png")
    img_fig2_h = os.path.join(cur_dir, "fig2_rdm6300_horizontal.png")
    img_openroad = os.path.join(root_dir, "Openroad_1.png")
    img_signoff = os.path.join(root_dir, "AntennaLvsDrc.png")

    # Helper: Add Slide Header (for content slides)
    def add_header(slide, category, title, slide_num, total_slides=16):
        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG_LIGHT
        bg.line.fill.background()

        # Top Accent Ribbon
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.1))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = C_BLUE_ACCENT
        top_bar.line.fill.background()

        # Header Text Box
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.22), Inches(11.733), Inches(0.95))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_cat = tf.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.name = "Segoe UI"
        p_cat.font.size = Pt(10.5)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_BLUE_ACCENT
        p_cat.space_after = Pt(2)

        p_title = tf.add_paragraph()
        p_title.text = title
        p_title.font.name = "Segoe UI"
        p_title.font.size = Pt(19)
        p_title.font.bold = True
        p_title.font.color.rgb = C_TEXT_DARK

        # Footer Line & Slide Number
        footer_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.02))
        footer_line.fill.solid()
        footer_line.fill.fore_color.rgb = RGBColor(226, 232, 240)
        footer_line.line.fill.background()

        tb_foot = slide.shapes.add_textbox(Inches(0.8), Inches(7.1), Inches(8.0), Inches(0.3))
        tf_foot = tb_foot.text_frame
        p_foot = tf_foot.paragraphs[0]
        p_foot.text = "PicoRV32 RFID Access Controller SoC | SkyWater 130nm ASIC & Basys 3 Demo"
        p_foot.font.name = "Segoe UI"
        p_foot.font.size = Pt(9.5)
        p_foot.font.color.rgb = C_TEXT_MUTED

        tb_num = slide.shapes.add_textbox(Inches(11.0), Inches(7.1), Inches(1.533), Inches(0.3))
        tf_num = tb_num.text_frame
        p_num = tf_num.paragraphs[0]
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.text = f"{slide_num:02d} / {total_slides:02d}"
        p_num.font.name = "Segoe UI"
        p_num.font.size = Pt(9.5)
        p_num.font.bold = True
        p_num.font.color.rgb = C_BLUE_ACCENT

    # Helper: Add Styled Card Container
    def add_card(slide, left, top, width, height, border_color=C_CARD_BORDER, bg_color=C_CARD_BG):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        return card

    # =========================================================================
    # SLIDE 1: COVER / TITLE SLIDE (Dark Tech Widescreen)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_NAVY_DARK
    bg1.line.fill.background()

    card1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
    card1.fill.solid()
    card1.fill.fore_color.rgb = C_NAVY_MID
    card1.line.color.rgb = C_BLUE_ACCENT
    card1.line.width = Pt(2.0)

    tb_title = s1.shapes.add_textbox(Inches(1.3), Inches(1.2), Inches(10.7), Inches(4.8))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True

    p_sub = tf_title.paragraphs[0]
    p_sub.text = "BÁO CÁO ĐỒ ÁN THIẾT KẾ VI MẠCH SỐ (ASIC / SOC DESIGN PROJECT)"
    p_sub.font.name = "Segoe UI"
    p_sub.font.size = Pt(13)
    p_sub.font.bold = True
    p_sub.font.color.rgb = C_CYAN_ACCENT
    p_sub.space_after = Pt(12)

    p_main = tf_title.add_paragraph()
    p_main.text = "HỆ THỐNG VI MẠCH SOC XỬ LÝ DỮ LIỆU THẺ RFID RDM6300"
    p_main.font.name = "Segoe UI"
    p_main.font.size = Pt(28)
    p_main.font.bold = True
    p_main.font.color.rgb = C_WHITE
    p_main.space_after = Pt(10)

    p_desc = tf_title.add_paragraph()
    p_desc.text = "Tích Hợp Nhân CPU RISC-V PicoRV32 Quản Lý Firmware, Danh Mục Thẻ & Nhật Ký Trên SPI Flash"
    p_desc.font.name = "Segoe UI"
    p_desc.font.size = Pt(15)
    p_desc.font.color.rgb = RGBColor(203, 213, 225)
    p_desc.space_after = Pt(28)

    # Tech badges
    badges = [
        ("SkyWater 130nm ASIC", C_BLUE_ACCENT),
        ("RISC-V PicoRV32 RV32I", C_CYAN_ACCENT),
        ("32 Mb SPI Flash NVM", C_GREEN),
        ("RDM6300 125 kHz", C_AMBER),
        ("Basys 3 FPGA Demo", C_PURPLE),
        ("OpenLane 2 Sign-off", C_ROSE)
    ]
    bx = Inches(1.2)
    by = Inches(4.3)
    bw = Inches(1.7)
    bh = Inches(0.42)
    bgap = Inches(0.18)

    for i, (b_txt, b_col) in enumerate(badges):
        b_shp = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx + i*(bw + bgap), by, bw, bh)
        b_shp.fill.solid()
        b_shp.fill.fore_color.rgb = C_NAVY_DARK
        b_shp.line.color.rgb = b_col
        b_shp.line.width = Pt(1.5)
        tf_b = b_shp.text_frame
        tf_b.word_wrap = False
        p_b = tf_b.paragraphs[0]
        p_b.text = b_txt
        p_b.font.name = "Segoe UI"
        p_b.font.size = Pt(9.5)
        p_b.font.bold = True
        p_b.font.color.rgb = b_col
        p_b.alignment = PP_ALIGN.CENTER

    tb_auth = s1.shapes.add_textbox(Inches(1.3), Inches(5.1), Inches(10.7), Inches(1.2))
    tf_auth = tb_auth.text_frame
    p_au = tf_auth.paragraphs[0]
    p_au.text = "• Nền tảng thiết kế: OpenLane 2 (SkyWater Sky130A) | Ký duyệt STA 50 MHz (MET TIMING ở 9 Corners)\n• Thực nghiệm phần cứng: Bo mạch FPGA Xilinx Artix-7 Basys 3 kết nối đầu đọc RFID thật & phần mềm Host C"
    p_au.font.name = "Segoe UI"
    p_au.font.size = Pt(11)
    p_au.font.color.rgb = RGBColor(148, 163, 184)

    # =========================================================================
    # SLIDE 2: ĐẶT VẤN ĐỀ & ĐỊNH HƯỚNG SẢN PHẨM (3 Pillar Cards)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Chương 1 | Tổng quan & Đặt vấn đề", "Định Hướng Sản Phẩm: Thiết Bị Kiểm Soát Ra Vào Độc Lập (Offline)", 2)

    col_w = Inches(3.68)
    col_h = Inches(4.05)
    col_gap = Inches(0.34)
    start_x = Inches(0.8)
    top_y = Inches(1.35)

    # Card 1: Hạn chế Cloud
    add_card(s2, start_x, top_y, col_w, col_h, C_ROSE)
    tb1 = s2.shapes.add_textbox(start_x + Inches(0.2), top_y + Inches(0.2), col_w - Inches(0.4), col_h - Inches(0.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "🔴 Hạn Chế Access Control Đám Mây"
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = C_ROSE
    p1.space_after = Pt(8)

    bullets1 = [
        ("Nguy cơ mất kết nối:", "Hệ thống tê liệt khi đứt cáp quang hoặc mất mạng viễn thông."),
        ("Độ trễ cao:", "Phải gửi dữ liệu lên máy chủ từ xa rồi chờ phản hồi, gây ùn tắc."),
        ("Nguy cơ an ninh mạng:", "Dữ liệu định danh truyền qua mạng công cộng dễ bị nghe lén, DDoS."),
        ("Khó triển khai biệt lập:", "Bất khả thi tại các địa bàn vùng sâu, kho quân sự, hầm mỏ, phòng lab.")
    ]
    for b_title, b_desc in bullets1:
        p_b = tf1.add_paragraph()
        p_b.text = f"• {b_title}\n"
        p_b.font.name = "Segoe UI"
        p_b.font.size = Pt(10.5)
        p_b.font.bold = True
        p_b.font.color.rgb = C_TEXT_DARK
        p_b.space_after = Pt(4)
        run_d = p_b.add_run()
        run_d.text = f"  {b_desc}"
        run_d.font.bold = False
        run_d.font.color.rgb = C_TEXT_MUTED
        run_d.font.size = Pt(10)

    # Card 2: Định hướng Standalone
    add_card(s2, start_x + col_w + col_gap, top_y, col_w, col_h, C_BLUE_ACCENT)
    tb2 = s2.shapes.add_textbox(start_x + col_w + col_gap + Inches(0.2), top_y + Inches(0.2), col_w - Inches(0.4), col_h - Inches(0.4))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = "🔵 Thiết Bị Standalone Offline"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = C_BLUE_ACCENT
    p2.space_after = Pt(8)

    bullets2 = [
        ("Vận hành 100% độc lập:", "Tự giải mã thẻ và đối chiếu cơ sở dữ liệu tại chỗ, không cần Internet."),
        ("Độ trễ siêu nhỏ (< 10 µs):", "Xác thực thẻ tức thì bằng phần cứng chuyên dụng, loại trừ trễ mạng."),
        ("Bảo mật vật lý (Air-Gap):", "Cách ly vật lý triệt tiêu hoàn toàn mọi khả năng xâm nhập từ xa."),
        ("Tính sẵn sàng cao:", "Hoạt động liên tục 24/7 ngay cả trong điều kiện mạng viễn thông sập.")
    ]
    for b_title, b_desc in bullets2:
        p_b = tf2.add_paragraph()
        p_b.text = f"• {b_title}\n"
        p_b.font.name = "Segoe UI"
        p_b.font.size = Pt(10.5)
        p_b.font.bold = True
        p_b.font.color.rgb = C_TEXT_DARK
        p_b.space_after = Pt(4)
        run_d = p_b.add_run()
        run_d.text = f"  {b_desc}"
        run_d.font.bold = False
        run_d.font.color.rgb = C_TEXT_MUTED
        run_d.font.size = Pt(10)

    # Card 3: Vai trò Flash
    add_card(s2, start_x + (col_w + col_gap)*2, top_y, col_w, col_h, C_GREEN)
    tb3 = s2.shapes.add_textbox(start_x + (col_w + col_gap)*2 + Inches(0.2), top_y + Inches(0.2), col_w - Inches(0.4), col_h - Inches(0.4))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    p3 = tf3.paragraphs[0]
    p3.text = "🟢 Vai Trò Của SPI Flash (NVM)"
    p3.font.name = "Segoe UI"
    p3.font.size = Pt(14)
    p3.font.bold = True
    p3.font.color.rgb = C_GREEN
    p3.space_after = Pt(8)

    bullets3 = [
        ("Lưu trữ bất biến > 20 năm:", "Danh sách thẻ Whitelist và nhật ký ra vào an toàn khi mất điện."),
        ("Dung lượng lớn chi phí thấp:", "Chip 32 Mbit (4MB) chứa được 4096 thẻ và 512 bản ghi nhật ký."),
        ("Tiết kiệm chân I/O tối đa:", "Chuẩn SPI chỉ cần 4 đường (CS, SCK, MOSI, MISO), rất lý tưởng cho ASIC."),
        ("Bảo trì & trích xuất tiện lợi:", "Cắm máy tính qua UART để nạp danh mục thẻ hoặc xuất file CSV an toàn.")
    ]
    for b_title, b_desc in bullets3:
        p_b = tf3.add_paragraph()
        p_b.text = f"• {b_title}\n"
        p_b.font.name = "Segoe UI"
        p_b.font.size = Pt(10.5)
        p_b.font.bold = True
        p_b.font.color.rgb = C_TEXT_DARK
        p_b.space_after = Pt(4)
        run_d = p_b.add_run()
        run_d.text = f"  {b_desc}"
        run_d.font.bold = False
        run_d.font.color.rgb = C_TEXT_MUTED
        run_d.font.size = Pt(10)

    # Bottom Takeaway Card
    add_card(s2, start_x, Inches(5.6), Inches(11.733), Inches(1.15), C_BLUE_ACCENT, RGBColor(241, 245, 249))
    tb_bot = s2.shapes.add_textbox(start_x + Inches(0.25), Inches(5.68), Inches(11.233), Inches(1.0))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    p_b0 = tf_bot.paragraphs[0]
    p_b0.text = "💡 KẾT LUẬN CHIẾN LƯỢC: ĐỊNH HƯỚNG THIẾT KẾ ACCESS CONTROL STANDALONE"
    p_b0.font.name = "Segoe UI"
    p_b0.font.size = Pt(11.5)
    p_b0.font.bold = True
    p_b0.font.color.rgb = C_BLUE_ACCENT
    p_b0.space_after = Pt(3)

    p_b1 = tf_bot.add_paragraph()
    p_b1.text = "Hệ thống Standalone giải quyết triệt để rủi ro bảo mật & độ trễ thông qua kiến trúc xử lý cục bộ — Phù hợp tuyệt đối cho kho quân sự, phòng máy chủ, phòng sạch bán dẫn và các khu vực bảo mật nghiêm ngặt."
    p_b1.font.name = "Segoe UI"
    p_b1.font.size = Pt(10.5)
    p_b1.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 3: TỔNG QUAN KIẾN TRÚC VI HỆ THỐNG SOC (Hình 1)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Chương 2 | Kiến trúc hệ thống phần cứng", "Sơ Đồ Khối Kiến Trúc Vi Hệ Thống SoC PicoRV32 Tích Hợp (Hình 1)", 3)

    if os.path.exists(img_fig1):
        s3.shapes.add_picture(img_fig1, Inches(0.8), Inches(1.35), width=Inches(7.6))

    right_x = Inches(8.65)
    right_w = Inches(3.88)
    add_card(s3, right_x, Inches(1.35), right_w, Inches(5.35), C_BLUE_ACCENT)
    tb_arch = s3.shapes.add_textbox(right_x + Inches(0.2), Inches(1.5), right_w - Inches(0.4), Inches(5.0))
    tf_arch = tb_arch.text_frame
    tf_arch.word_wrap = True

    p_a0 = tf_arch.paragraphs[0]
    p_a0.text = "Đặc Điểm Cốt Lõi SoC"
    p_a0.font.name = "Segoe UI"
    p_a0.font.size = Pt(15)
    p_a0.font.bold = True
    p_a0.font.color.rgb = C_BLUE_ACCENT
    p_a0.space_after = Pt(10)

    arch_points = [
        ("CPU RISC-V PicoRV32:", "Hỗ trợ chuẩn tập lệnh RV32I, thiết kế gọn gàng, hiệu suất diện tích silicon cao."),
        ("1KB On-Chip Data SRAM:", "Chứa ngăn xếp Stack (sp = 0x400), biến .data, .bss và hàm flashio_worker."),
        ("Flash XIP Execution:", "Thực thi trực tiếp mã máy từ Flash tại địa chỉ reset 0x0025_0000 thông qua SPIMEMIO."),
        ("Động Cơ Giải Mã RDM6300:", "Phần cứng hóa tự động nhận dạng STX/ETX và so khớp XOR Checksum trong 1 chu kỳ."),
        ("Đệm FIFO Kép Cho UART:", "Ngăn chặn nghẽn bus hoặc rơi rụng lệnh khi CPU đang bận ghi/xóa Flash."),
        ("16 Đèn LED Chẩn Đoán:", "Giám sát nhịp tim hệ thống (1Hz), cờ bận Flash, và trạng thái xác thực thẻ.")
    ]
    for apt, adesc in arch_points:
        p_pt = tf_arch.add_paragraph()
        p_pt.text = f"▸ {apt} "
        p_pt.font.name = "Segoe UI"
        p_pt.font.size = Pt(11)
        p_pt.font.bold = True
        p_pt.font.color.rgb = C_TEXT_DARK
        p_pt.space_after = Pt(4)
        run_ad = p_pt.add_run()
        run_ad.text = adesc
        run_ad.font.bold = False
        run_ad.font.color.rgb = C_TEXT_MUTED
        run_ad.font.size = Pt(10.5)

    # =========================================================================
    # SLIDE 4: BƯỚC 1: LỰA CHỌN TÀI NGUYÊN PHẦN CỨNG & PHẦN MỀM
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Chương 3 | Quy trình thiết kế tuần tự", "3.1. Bước 1: Lựa Chọn Tài Nguyên Phần Cứng & Phần Mềm", 4)

    col2_w = Inches(5.7)
    col2_h = Inches(4.05)
    gap2 = Inches(0.333)

    # Left: Hardware Selection
    add_card(s4, start_x, top_y, col2_w, col2_h, C_BLUE_ACCENT)
    tb_hw = s4.shapes.add_textbox(start_x + Inches(0.2), top_y + Inches(0.2), col2_w - Inches(0.4), col2_h - Inches(0.4))
    tf_hw = tb_hw.text_frame
    tf_hw.word_wrap = True
    p_hw0 = tf_hw.paragraphs[0]
    p_hw0.text = "🎯 Lựa Chọn Tài Nguyên Phần Cứng"
    p_hw0.font.name = "Segoe UI"
    p_hw0.font.size = Pt(14)
    p_hw0.font.bold = True
    p_hw0.font.color.rgb = C_BLUE_ACCENT
    p_hw0.space_after = Pt(8)

    hw_items = [
        ("Module RFID RDM6300 (125 kHz):", "Độ bền công nghiệp cao, hoạt động 5V/3.3V, ngõ ra UART 9600 bps tương thích hoàn hảo mức logic 3.3V của các cổng PMOD."),
        ("Bo mạch FPGA Digilent Basys 3 (XC7A35T):", "NỀN TẢNG DEMO VÀ TẠO MẪU PHẦN CỨNG (Hardware Prototype Platform). Tích hợp chip SPI Flash 32 Mbit (Spansion S25FL032P), chip USB-UART FTDI, 16 LED và cổng PMOD tiêu chuẩn."),
        ("Ý nghĩa kiểm chứng thực nghiệm:", "Cho phép xác thực hệ vi mạch SoC, firmware và thẻ RFID thật hoạt động ổn định 100% trong điều kiện nhiễu trước khi chuyển sang ASIC.")
    ]
    for h_t, h_d in hw_items:
        p = tf_hw.add_paragraph()
        p.text = f"• {h_t}\n"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(4)
        r = p.add_run()
        r.text = f"  {h_d}"
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED
        r.font.size = Pt(10)

    # Right: Software Toolchain
    add_card(s4, start_x + col2_w + gap2, top_y, col2_w, col2_h, C_PURPLE)
    tb_sw = s4.shapes.add_textbox(start_x + col2_w + gap2 + Inches(0.2), top_y + Inches(0.2), col2_w - Inches(0.4), col2_h - Inches(0.4))
    tf_sw = tb_sw.text_frame
    tf_sw.word_wrap = True
    p_sw0 = tf_sw.paragraphs[0]
    p_sw0.text = "⚙️ Chuỗi Công Cụ Phát Triển Phần Mềm"
    p_sw0.font.name = "Segoe UI"
    p_sw0.font.size = Pt(14)
    p_sw0.font.bold = True
    p_sw0.font.color.rgb = C_PURPLE
    p_sw0.space_after = Pt(8)

    sw_items = [
        ("Xilinx Vivado ML Edition:", "Tổng hợp RTL, gán chân ràng buộc vật lý XDC (basys3_picorv32_rdm6300.xdc), nạp bitstream demo trên Basys 3."),
        ("OpenLane 2 & SkyWater 130nm PDK:", "Thực thi toàn bộ luồng tổng hợp vật lý RTL-to-GDSII ra layout bán dẫn hoàn chỉnh cho xưởng đúc."),
        ("GNU RISC-V Toolchain (riscv32-unknown-elf-gcc):", "Biên dịch mã nguồn C bare-metal và file khởi động Assembly start.s thành tệp mã máy nhị phân firmware.hex."),
        ("Host PC Console (host/main.c):", "Phát triển bằng ngôn ngữ C thuần trên Win32 Serial API, đóng vai trò giao diện điều khiển trung tâm.")
    ]
    for s_t, s_d in sw_items:
        p = tf_sw.add_paragraph()
        p.text = f"• {s_t}\n"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(3)
        r = p.add_run()
        r.text = f"  {s_d}"
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED
        r.font.size = Pt(9.5)

    # Bottom Takeaway Card
    add_card(s4, start_x, Inches(5.6), Inches(11.733), Inches(1.15), C_BLUE_ACCENT, RGBColor(241, 245, 249))
    tb_b4 = s4.shapes.add_textbox(start_x + Inches(0.25), Inches(5.68), Inches(11.233), Inches(1.0))
    tf_b4 = tb_b4.text_frame
    tf_b4.word_wrap = True
    p_b0 = tf_b4.paragraphs[0]
    p_b0.text = "💡 Ý NGHĨA CHIẾN LƯỢC CỦA BƯỚC CHỌN TÀI NGUYÊN:"
    p_b0.font.name = "Segoe UI"
    p_b0.font.size = Pt(11.5)
    p_b0.font.bold = True
    p_b0.font.color.rgb = C_BLUE_ACCENT
    p_b0.space_after = Pt(3)
    p_b1 = tf_b4.add_paragraph()
    p_b1.text = "Sự phối hợp giữa bo mạch FPGA Basys 3 (môi trường kiểm chứng thực nghiệm) và OpenLane 2 (luồng thiết kế vi mạch ASIC Sky130) giúp đảm bảo thiết kế chạy đúng 100% trên phần cứng thật trước khi gửi tape-out."
    p_b1.font.name = "Segoe UI"
    p_b1.font.size = Pt(10.5)
    p_b1.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 5: BƯỚC 2: THIẾT KẾ FIRMWARE & ĐỊNH NGHĨA GIAO THỨC TRƯỚC
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Chương 3 | Quy trình thiết kế tuần tự", "3.2. Bước 2: Thiết Kế Firmware & Định Nghĩa Giao Thức Trước", 5)

    # Left: Software-First & Flash Layout
    add_card(s5, start_x, top_y, col2_w, col2_h, C_BLUE_ACCENT)
    tb_fw = s5.shapes.add_textbox(start_x + Inches(0.2), top_y + Inches(0.2), col2_w - Inches(0.4), col2_h - Inches(0.4))
    tf_fw = tb_fw.text_frame
    tf_fw.word_wrap = True
    p_fw0 = tf_fw.paragraphs[0]
    p_fw0.text = "🎯 Triết Lý Software-First & Quy Hoạch Flash"
    p_fw0.font.name = "Segoe UI"
    p_fw0.font.size = Pt(14)
    p_fw0.font.bold = True
    p_fw0.font.color.rgb = C_BLUE_ACCENT
    p_fw0.space_after = Pt(8)

    fw_items = [
        ("Triết lý thiết kế Software-First:", "Xác định các chức năng và giao thức phần mềm trước giúp định hình chính xác các thanh ghi ngoại vi và cấu trúc bus phần cứng cần thiết, tránh lãng phí diện tích silicon."),
        ("Sector 48 (0x0030_0000) - Danh mục thẻ hợp lệ:", "Dung lượng 64KB chứa tối đa 4096 bản ghi thẻ. Mỗi bản ghi 16 bytes: 4B Magic ('RFID' - 0x52464944), 4B UID High, 4B UID Low, 4B Flags trạng thái."),
        ("Sector 49 (0x0031_0000) - Nhật ký quẹt thẻ:", "Chứa tối đa 512 bản ghi nhật ký. Mỗi bản ghi 16 bytes: 4B Magic ('SUCC' hoặc 'FAIL'), 4B UID thẻ đã quẹt, 4B thứ tự lượt quẹt và 4B địa chỉ slot.")
    ]
    for f_t, f_d in fw_items:
        p = tf_fw.add_paragraph()
        p.text = f"• {f_t}\n"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(4)
        r = p.add_run()
        r.text = f"  {f_d}"
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED
        r.font.size = Pt(10)

    # Right: UART Commands & Core C Functions
    add_card(s5, start_x + col2_w + gap2, top_y, col2_w, col2_h, C_GREEN)
    tb_cmd = s5.shapes.add_textbox(start_x + col2_w + gap2 + Inches(0.2), top_y + Inches(0.2), col2_w - Inches(0.4), col2_h - Inches(0.4))
    tf_cmd = tb_cmd.text_frame
    tf_cmd.word_wrap = True
    p_cm0 = tf_cmd.paragraphs[0]
    p_cm0.text = "📡 Tập Lệnh UART & Hàm Cốt Lõi C"
    p_cm0.font.name = "Segoe UI"
    p_cm0.font.size = Pt(14)
    p_cm0.font.bold = True
    p_cm0.font.color.rgb = C_GREEN
    p_cm0.space_after = Pt(8)

    cmd_items = [
        ("Giao thức tập lệnh ASCII kết thúc bằng '\\n':", "Chuẩn hóa giao tiếp: 'P' (Ping CPU), 'N<UID>' (Thêm thẻ mới), 'C<UID>' (Kiểm tra thẻ), 'D<UID>' (Xóa thẻ), 'V<UID>' (Quẹt thẻ ảo), 'L' (Đọc nhật ký), 'X' (Xóa nhật ký sau sao lưu), 'E' (Xóa hết thẻ), 'S' (Trạng thái SoC)."),
        ("Hàm xử lý quét thẻ execute_card_scan():", "Bóc tách mã thẻ từ thanh ghi phần cứng -> Tra cứu Sector 48 qua find_tag_slot()."),
        ("Xử lý kết quả xác thực tức thì:", "Hợp lệ: Bật LED xanh, ghi log SUCC vào Sector 49, xuất 'ACCESS:GRANTED'; Không hợp lệ: Bật LED cảnh báo, ghi log FAIL, xuất 'ACCESS:DENIED'.")
    ]
    for c_t, c_d in cmd_items:
        p = tf_cmd.add_paragraph()
        p.text = f"• {c_t}\n"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(4)
        r = p.add_run()
        r.text = f"  {c_d}"
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED
        r.font.size = Pt(10)

    # Bottom Takeaway Card
    add_card(s5, start_x, Inches(5.6), Inches(11.733), Inches(1.15), C_GREEN, RGBColor(240, 253, 244))
    tb_b5 = s5.shapes.add_textbox(start_x + Inches(0.25), Inches(5.68), Inches(11.233), Inches(1.0))
    tf_b5 = tb_b5.text_frame
    tf_b5.word_wrap = True
    p_b0 = tf_b5.paragraphs[0]
    p_b0.text = "💡 HIỆU QUẢ CỦA BƯỚC ĐỊNH NGHĨA PHẦN MỀM TRƯỚC:"
    p_b0.font.name = "Segoe UI"
    p_b0.font.size = Pt(11.5)
    p_b0.font.bold = True
    p_b0.font.color.rgb = C_GREEN
    p_b0.space_after = Pt(3)
    p_b1 = tf_b5.add_paragraph()
    p_b1.text = "Việc đặc tả rõ ràng 13 chức năng và cấu trúc 16-byte cho từng slot giúp kỹ sư thiết kế phần cứng xác định chính xác số lượng thanh ghi MMIO, kích thước bộ đệm FIFO và các đường ngắt IRQ cần thiết mà không bị dư thừa."
    p_b1.font.name = "Segoe UI"
    p_b1.font.size = Pt(10.5)
    p_b1.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 6: BƯỚC 3: THIẾT KẾ PHẦN CỨNG CPU PICORV32 VÀ 1KB DATA SRAM
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Chương 3 | Quy trình thiết kế tuần tự", "3.3. Bước 3: Thiết Kế Khối Xử Lý Trung Tâm: CPU PicoRV32 & 1KB SRAM", 6)

    # Left: PicoRV32 Core
    add_card(s6, start_x, top_y, col2_w, col2_h, C_BLUE_ACCENT)
    tb_cpu = s6.shapes.add_textbox(start_x + Inches(0.2), top_y + Inches(0.2), col2_w - Inches(0.4), col2_h - Inches(0.4))
    tf_cpu = tb_cpu.text_frame
    tf_cpu.word_wrap = True
    p_cp0 = tf_cpu.paragraphs[0]
    p_cp0.text = "🧠 Nhân CPU RISC-V PicoRV32 (rtl/picorv32.v)"
    p_cp0.font.name = "Segoe UI"
    p_cp0.font.size = Pt(14)
    p_cp0.font.bold = True
    p_cp0.font.color.rgb = C_BLUE_ACCENT
    p_cp0.space_after = Pt(8)

    cpu_items = [
        ("Chuẩn tập lệnh RV32I:", "Cấu hình nhân 32-bit cơ bản RV32I, thiết kế cực kỳ tinh gọn, tối ưu hóa diện tích cho vi mạch SoC nhúng."),
        ("Giao thức Memory Bus 32-bit:", "Giao tiếp qua các tín hiệu: mem_valid, mem_ready, mem_addr[31:0], mem_wdata[31:0], mem_wstrb[3:0], mem_rdata[31:0]."),
        ("Mặt nạ ghi byte mem_wstrb[3:0]:", "Cho phép ghi chính xác từng byte đơn lẻ vào SRAM mà không làm ghi đè dữ liệu lân cận."),
        ("Khởi động trực tiếp Reset Vector (PROGADDR_RESET):", "Đặt tại địa chỉ 0x0025_0000 trong SPI Flash. CPU bắt đầu fetch lệnh trực tiếp từ Flash thông qua cơ chế XIP ngay khi nhả reset.")
    ]
    for cp_t, cp_d in cpu_items:
        p = tf_cpu.add_paragraph()
        p.text = f"• {cp_t}\n"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(3)
        r = p.add_run()
        r.text = f"  {cp_d}"
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED
        r.font.size = Pt(9.5)

    # Right: 1KB Data SRAM & Startup Code
    add_card(s6, start_x + col2_w + gap2, top_y, col2_w, col2_h, C_AMBER)
    tb_ram = s6.shapes.add_textbox(start_x + col2_w + gap2 + Inches(0.2), top_y + Inches(0.2), col2_w - Inches(0.4), col2_h - Inches(0.4))
    tf_ram = tb_ram.text_frame
    tf_ram.word_wrap = True
    p_rm0 = tf_ram.paragraphs[0]
    p_rm0.text = "📦 Bộ Nhớ On-Chip 1KB Data SRAM & Startup"
    p_rm0.font.name = "Segoe UI"
    p_rm0.font.size = Pt(14)
    p_rm0.font.bold = True
    p_rm0.font.color.rgb = C_AMBER
    p_rm0.space_after = Pt(8)

    ram_items = [
        ("Mảng nhớ nội bộ 1KB (rtl/data_sram.v):", "Dung lượng chính xác 1 KByte (256 words x 32-bit = 1024 bytes), ánh xạ địa chỉ 0x0000_0000 đến 0x0000_03FF."),
        ("Không gian dữ liệu đọc/ghi:", "Chứa ngăn xếp Stack Pointer (sp = 0x0000_0400), biến toàn cục (.data, .bss) và chứa đoạn mã hàm flashio_worker."),
        ("Tối ưu hóa diện tích bán dẫn:", "1KB tối giản giúp khuôn chip chỉ tốn 1.69 mm² trên Sky130 và suy luận hoàn hảo thành khối Block RAM đồng bộ trên FPGA Basys 3."),
        ("Mã Assembly start.s & Linker sections.lds:", "Thiết lập sp = 0x400, sao chép .data từ Flash vào SRAM, xóa sạch .bss về 0 trước khi gọi hàm main().")
    ]
    for rm_t, rm_d in ram_items:
        p = tf_ram.add_paragraph()
        p.text = f"• {rm_t}\n"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(3)
        r = p.add_run()
        r.text = f"  {rm_d}"
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED
        r.font.size = Pt(9.5)

    # Bottom Takeaway Card
    add_card(s6, start_x, Inches(5.6), Inches(11.733), Inches(1.15), C_AMBER, RGBColor(254, 243, 199))
    tb_b6 = s6.shapes.add_textbox(start_x + Inches(0.25), Inches(5.68), Inches(11.233), Inches(1.0))
    tf_b6 = tb_b6.text_frame
    tf_b6.word_wrap = True
    p_b0 = tf_b6.paragraphs[0]
    p_b0.text = "💡 ĐẶC TÍNH VƯỢT TRỘI CỦA KHỐI XỬ LÝ TRUNG TÂM:"
    p_b0.font.name = "Segoe UI"
    p_b0.font.size = Pt(11.5)
    p_b0.font.bold = True
    p_b0.font.color.rgb = C_AMBER
    p_b0.space_after = Pt(3)
    p_b1 = tf_b6.add_paragraph()
    p_b1.text = "Bằng cách giới hạn SRAM ở mức 1KB vừa đủ cho Stack/Data và chạy mã lệnh trực tiếp từ Flash ngoài, SoC đạt được hiệu năng tính toán 32-bit mạnh mẽ mà vẫn giữ diện tích silicon ở mức tối thiểu tuyệt đối."
    p_b1.font.name = "Segoe UI"
    p_b1.font.size = Pt(10.5)
    p_b1.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 7: BƯỚC 4: THIẾT KẾ BỘ ĐIỀU KHIỂN SPI FLASH CONTROLLER
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Chương 3 | Quy trình thiết kế tuần tự", "3.4. Bước 4: Thiết Kế Bộ Điều Khiển Bộ Nhớ Ngoài SPI Flash", 7)

    # Left: FSM SPI & Commands
    add_card(s7, start_x, top_y, col2_w, col2_h, C_AMBER)
    tb_spi = s7.shapes.add_textbox(start_x + Inches(0.2), top_y + Inches(0.2), col2_w - Inches(0.4), col2_h - Inches(0.4))
    tf_spi = tb_spi.text_frame
    tf_spi.word_wrap = True
    p_sp0 = tf_spi.paragraphs[0]
    p_sp0.text = "⚙️ FSM Điều Khiển SPI & Tập Lệnh Phần Cứng"
    p_sp0.font.name = "Segoe UI"
    p_sp0.font.size = Pt(14)
    p_sp0.font.bold = True
    p_sp0.font.color.rgb = C_AMBER
    p_sp0.space_after = Pt(8)

    spi_items = [
        ("Cầu nối MMIO - SPI Flash (rtl/spimemio.v):", "Chuyển đổi các giao dịch đọc/ghi bus 32-bit của CPU thành chuỗi xung nối tiếp SPI 1-bit điều khiển chip Flash ngoài."),
        ("Máy trạng thái FSM điều khiển tự động:", "Tự động hóa hoàn toàn phát xung nhịp SCK, hạ chân chọn chip CS_N, đẩy địa chỉ qua MOSI và lấy mẫu dữ liệu từ MISO."),
        ("Tập lệnh Flash phần cứng hỗ trợ:", "• 0x03 / 0x0B: Đọc dữ liệu (Read / Fast Read kèm 8 Dummy Clocks).\n• 0x02: Ghi dữ liệu theo trang 256 bytes (Page Program).\n• 0xD8 / 0x20: Xóa khối Sector 64KB / 4KB (Sector Erase).\n• 0x05: Đọc thanh ghi trạng thái Flash (Read Status Register).")
    ]
    for sp_t, sp_d in spi_items:
        p = tf_spi.add_paragraph()
        p.text = f"• {sp_t}\n"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(3)
        r = p.add_run()
        r.text = f"  {sp_d}"
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED
        r.font.size = Pt(9.5)

    # Right: WIP Polling & flashio_worker
    add_card(s7, start_x + col2_w + gap2, top_y, col2_w, col2_h, C_GREEN)
    tb_wip = s7.shapes.add_textbox(start_x + col2_w + gap2 + Inches(0.2), top_y + Inches(0.2), col2_w - Inches(0.4), col2_h - Inches(0.4))
    tf_wip = tb_wip.text_frame
    tf_wip.word_wrap = True
    p_wp0 = tf_wip.paragraphs[0]
    p_wp0.text = "🔄 Polling Cờ WIP & Hàm flashio_worker"
    p_wp0.font.name = "Segoe UI"
    p_wp0.font.size = Pt(14)
    p_wp0.font.bold = True
    p_wp0.font.color.rgb = C_GREEN
    p_wp0.space_after = Pt(8)

    wip_items = [
        ("Tự động Polling cờ WIP bằng phần cứng:", "Sau mỗi chu kỳ ghi trang hoặc xóa sector, khối SPIMEMIO tự động gửi lệnh 0x05 kiểm tra bit 0 (Write-In-Progress) của Flash."),
        ("Giải phóng 100% thời gian chờ cho CPU:", "Khi Flash bận ghi vật lý, bit REG_SPI_STATUS_BUSY giữ mức 1; khi hoàn tất, cờ tự hạ về 0, CPU không phải chạy vòng lặp delay lãng phí."),
        ("Hàm flashio_worker chạy trên 1KB SRAM:", "Khi cần ghi hoặc xóa Flash, hàm điều khiển tạm thời chuyển vào 1KB SRAM để thực thi an toàn, loại trừ hoàn toàn xung đột với lệnh fetch XIP."),
        ("Tiết kiệm chân I/O tối đa:", "Toàn bộ giao tiếp bộ nhớ chỉ cần 4 chân tín hiệu (CS_N, SCK, MOSI, MISO), rất lý tưởng cho đóng gói vi mạch ASIC.")
    ]
    for wp_t, wp_d in wip_items:
        p = tf_wip.add_paragraph()
        p.text = f"• {wp_t}\n"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(3)
        r = p.add_run()
        r.text = f"  {wp_d}"
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED
        r.font.size = Pt(9.5)

    # Bottom Takeaway Card
    add_card(s7, start_x, Inches(5.6), Inches(11.733), Inches(1.15), C_GREEN, RGBColor(240, 253, 244))
    tb_b7 = s7.shapes.add_textbox(start_x + Inches(0.25), Inches(5.68), Inches(11.233), Inches(1.0))
    tf_b7 = tb_b7.text_frame
    tf_b7.word_wrap = True
    p_b0 = tf_b7.paragraphs[0]
    p_b0.text = "💡 VAI TRÒ SỐNG CÒN CỦA SPI FLASH CONTROLLER:"
    p_b0.font.name = "Segoe UI"
    p_b0.font.size = Pt(11.5)
    p_b0.font.bold = True
    p_b0.font.color.rgb = C_GREEN
    p_b0.space_after = Pt(3)
    p_b1 = tf_b7.add_paragraph()
    p_b1.text = "Khối spimemio.v giải quyết triệt để bài toán dung lượng bộ nhớ lớn trong thiết kế ASIC: vừa cho phép chạy mã lệnh XIP trực tiếp, vừa cung cấp cơ chế lưu trữ bền vững > 20 năm cho danh mục thẻ và nhật ký ra vào."
    p_b1.font.name = "Segoe UI"
    p_b1.font.size = Pt(10.5)
    p_b1.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 8: ĐƯỜNG ỐNG GIẢI MÃ PHẦN CỨNG RDM6300 (Hình 2 Chiều Ngang Full-Width)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Chương 3 | Ngoại vi thu nhận RFID", "3.5. Bước 5: Đường Ống 5 Giai Đoạn Thu Nhận & Giải Mã Phần Cứng (Hình 2)", 8)

    # Embed High-Res Horizontal Figure 2 across full slide width
    if os.path.exists(img_fig2_h):
        # 4320 x 2100 px -> Aspect Ratio 2.05714
        fig_w = Inches(11.417)
        fig_h = Inches(5.55)
        fig_x = Inches(0.958)
        fig_y = Inches(1.35)
        s8.shapes.add_picture(img_fig2_h, fig_x, fig_y, width=fig_w, height=fig_h)
    elif os.path.exists(img_fig2):
        s8.shapes.add_picture(img_fig2, Inches(0.8), Inches(1.35), width=Inches(11.733))

    # =========================================================================
    # SLIDE 9: CẤU TRÚC KHUNG 14 BYTE & TOÁN TỬ XOR KIỂM TRA TOÀN VẸN
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Chương 3 | Giao thức dữ liệu RFID", "Cấu Trúc Khung 14 Byte & Chứng Minh Toán Học Cây Toán Tử XOR", 9)

    add_card(s9, Inches(0.8), Inches(1.35), Inches(11.733), Inches(2.2), C_BLUE_ACCENT)
    tb_fr = s9.shapes.add_textbox(Inches(1.0), Inches(1.45), Inches(11.333), Inches(2.0))
    tf_fr = tb_fr.text_frame
    tf_fr.word_wrap = True

    p_f0 = tf_fr.paragraphs[0]
    p_f0.text = "Cấu Trúc Khung Truyền UART 14 Byte Của RDM6300 (Ví Dụ Thẻ Thật: 0007508976)"
    p_f0.font.name = "Segoe UI"
    p_f0.font.size = Pt(14)
    p_f0.font.bold = True
    p_f0.font.color.rgb = C_BLUE_ACCENT
    p_f0.space_after = Pt(6)

    byte_defs = [
        ("Byte 0", "STX", "0x02", C_TEXT_MUTED),
        ("B 1-2", "Version", "0x00 ('0''0')", C_BLUE_ACCENT),
        ("B 3-4", "Data[31:24]", "0x00 ('0''0')", C_GREEN),
        ("B 5-6", "Data[23:16]", "0x72 ('7''2')", C_GREEN),
        ("B 7-8", "Data[15:8]", "0x93 ('9''3')", C_GREEN),
        ("B 9-10", "Data[7:0]", "0xF0 ('F''0')", C_GREEN),
        ("B 11-12", "Checksum", "0xF0 ('F''0')", C_ROSE),
        ("Byte 13", "ETX", "0x03", C_TEXT_MUTED),
    ]
    b_start_x = Inches(1.0)
    b_y = Inches(1.9)
    b_w = Inches(1.35)
    b_h = Inches(1.05)
    b_gap = Inches(0.08)

    for i, (b_idx, b_name, b_val, b_col) in enumerate(byte_defs):
        card_b = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, b_start_x + i*(b_w + b_gap), b_y, b_w, b_h)
        card_b.fill.solid()
        card_b.fill.fore_color.rgb = RGBColor(241, 245, 249) if b_col == C_TEXT_MUTED else RGBColor(238, 242, 255) if b_col == C_BLUE_ACCENT else RGBColor(236, 253, 245) if b_col == C_GREEN else RGBColor(255, 241, 242)
        card_b.line.color.rgb = b_col
        card_b.line.width = Pt(1.5)

        tf_cb = card_b.text_frame
        tf_cb.word_wrap = True
        p_c0 = tf_cb.paragraphs[0]
        p_c0.alignment = PP_ALIGN.CENTER
        p_c0.text = b_idx
        p_c0.font.name = "Segoe UI"
        p_c0.font.size = Pt(9.5)
        p_c0.font.color.rgb = C_TEXT_MUTED

        p_c1 = tf_cb.add_paragraph()
        p_c1.alignment = PP_ALIGN.CENTER
        p_c1.text = b_name
        p_c1.font.name = "Segoe UI"
        p_c1.font.size = Pt(10)
        p_c1.font.bold = True
        p_c1.font.color.rgb = b_col

        p_c2 = tf_cb.add_paragraph()
        p_c2.alignment = PP_ALIGN.CENTER
        p_c2.text = b_val
        p_c2.font.name = "Consolas"
        p_c2.font.size = Pt(8.5)
        p_c2.font.color.rgb = C_TEXT_DARK

    # Bottom Two Columns
    add_card(s9, Inches(0.8), Inches(3.75), Inches(5.6), Inches(2.95), C_GREEN)
    tb_conv = s9.shapes.add_textbox(Inches(1.0), Inches(3.85), Inches(5.2), Inches(2.75))
    tf_conv = tb_conv.text_frame
    tf_conv.word_wrap = True

    p_cv0 = tf_conv.paragraphs[0]
    p_cv0.text = "Quy Đổi Định Dạng Thẻ RFID Thật"
    p_cv0.font.name = "Segoe UI"
    p_cv0.font.size = Pt(14)
    p_cv0.font.bold = True
    p_cv0.font.color.rgb = C_GREEN
    p_cv0.space_after = Pt(6)

    conv_bullets = [
        ("Số in dập nổi trên thẻ:", "0007508976 (10 chữ số thập phân)"),
        ("Định dạng Wiegand chuẩn:", "Facility Code: 114 | Card ID: 37872"),
        ("Mã Hex 10 ký tự chuẩn hóa:", "0x00 007293F0 (Version: 0x00, Serial: 0x007293F0)"),
        ("Thuật toán chuyển đổi:", "Do phần mềm Host C và FSM phần cứng tự động quy đổi đồng bộ 100%.")
    ]
    for ct, cd in conv_bullets:
        p_c = tf_conv.add_paragraph()
        p_c.text = f"• {ct}\n  {cd}"
        p_c.font.name = "Segoe UI"
        p_c.font.size = Pt(10.5)
        p_c.font.bold = True if ct in ["Số in dập nổi trên thẻ:", "Mã Hex 10 ký tự chuẩn hóa:"] else False
        p_c.font.color.rgb = C_TEXT_DARK
        p_c.space_after = Pt(3)

    add_card(s9, Inches(6.6), Inches(3.75), Inches(5.933), Inches(2.95), C_PURPLE)
    tb_xor = s9.shapes.add_textbox(Inches(6.8), Inches(3.85), Inches(5.533), Inches(2.75))
    tf_xor = tb_xor.text_frame
    tf_xor.word_wrap = True

    p_x0 = tf_xor.paragraphs[0]
    p_x0.text = "Cây Toán Tử XOR Song Song 1 Chu Kỳ (20.0 ns)"
    p_x0.font.name = "Segoe UI"
    p_x0.font.size = Pt(14)
    p_x0.font.bold = True
    p_x0.font.color.rgb = C_PURPLE
    p_x0.space_after = Pt(6)

    xor_lines = [
        ("Công thức:", "Calc_CS = D[0] ^ D[1] ^ D[2] ^ D[3] ^ D[4]"),
        ("Dạng nhị phân:", "= 00000000 ^ 00000000 ^ 01110010 ^ 10010011 ^ 11110000"),
        ("Dạng Hex:", "= 0x00 ^ 0x00 ^ 0x72 ^ 0x93 ^ 0xF0 = 0xF0"),
        ("So khớp:", "Calc_CS (0xF0) == Received_CS (0xF0) -> MATCH OK!"),
        ("Hiệu năng:", "Hoàn tất trong 1 chu kỳ clock, không tốn tài nguyên CPU.")
    ]
    for xt, xd in xor_lines:
        p_x = tf_xor.add_paragraph()
        p_x.text = f"• {xt} "
        p_x.font.name = "Segoe UI"
        p_x.font.size = Pt(10.5)
        p_x.font.bold = True
        p_x.font.color.rgb = C_TEXT_DARK
        p_x.space_after = Pt(2)
        run_x = p_x.add_run()
        run_x.text = xd
        run_x.font.bold = False
        run_x.font.color.rgb = C_GREEN if "MATCH OK" in xd else C_TEXT_MUTED
        run_x.font.size = Pt(10)

    # =========================================================================
    # SLIDE 10: QUY HOẠCH BỘ NHỚ FLASH & CƠ CHẾ XIP
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Chương 3 | Quản lý bộ nhớ Flash", "3.6. Bước 6: Phân Vùng Bộ Nhớ SPI Flash & Cơ Chế Thực Thi XIP", 10)

    add_card(s10, Inches(0.8), Inches(1.35), Inches(6.6), Inches(5.35), C_BLUE_ACCENT)
    tb_m = s10.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(6.2), Inches(3.2))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True

    p_mm0 = tf_m.paragraphs[0]
    p_mm0.text = "Quy Hoạch Bộ Nhớ SPI NOR Flash (32 Mbit / 4 MBytes)"
    p_mm0.font.name = "Segoe UI"
    p_mm0.font.size = Pt(14)
    p_mm0.font.bold = True
    p_mm0.font.color.rgb = C_BLUE_ACCENT
    p_mm0.space_after = Pt(8)

    flash_sectors = [
        ("Sector 0 - 36 (0x000000 - 0x0024FFFF):", "Dung lượng ~2.3 MB. Chứa FPGA Bitstream (khi nạp demo trên Basys 3) hoặc Bootloader."),
        ("Sector 37 (0x00250000 - 0x0025FFFF):", "Dung lượng 64 KB. Chứa toàn bộ Firmware RISC-V PicoRV32 thực thi tại chỗ (XIP)."),
        ("Sector 48 (0x00300000 - 0x0030FFFF):", "Dung lượng 64 KB. Cơ sở dữ liệu danh mục thẻ hợp lệ (Whitelist), lưu trữ tối đa 4096 bản ghi thẻ."),
        ("Sector 49 (0x00310000 - 0x0031FFFF):", "Dung lượng 64 KB. Cơ sở dữ liệu nhật ký quẹt thẻ (Access Logs), lưu trữ tối đa 512 bản ghi lượt quẹt.")
    ]
    for s_hdr, s_txt in flash_sectors:
        p_fs = tf_m.add_paragraph()
        p_fs.text = f"💾 {s_hdr}\n"
        p_fs.font.name = "Segoe UI"
        p_fs.font.size = Pt(10.5)
        p_fs.font.bold = True
        p_fs.font.color.rgb = C_TEXT_DARK
        p_fs.space_after = Pt(4)
        run_fs = p_fs.add_run()
        run_fs.text = f"    {s_txt}"
        run_fs.font.bold = False
        run_fs.font.color.rgb = C_TEXT_MUTED
        run_fs.font.size = Pt(10)

    # Mini visual flash bar
    bar_y = Inches(4.75)
    bar_h = Inches(0.42)
    seg_widths = [Inches(2.8), Inches(1.15), Inches(1.15), Inches(1.15)]
    seg_colors = [RGBColor(226, 232, 240), RGBColor(186, 230, 253), RGBColor(187, 247, 208), RGBColor(254, 215, 170)]
    seg_labels = ["Sec 0-36 (2.3M Bitstream)", "Sec 37 (XIP)", "Sec 48 (List)", "Sec 49 (Logs)"]
    cur_bx = Inches(1.0)
    for w, col, lbl in zip(seg_widths, seg_colors, seg_labels):
        s_rect = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, cur_bx, bar_y, w, bar_h)
        s_rect.fill.solid()
        s_rect.fill.fore_color.rgb = col
        s_rect.line.color.rgb = C_CARD_BORDER
        s_rect.line.width = Pt(1.0)
        tf_s = s_rect.text_frame
        tf_s.word_wrap = False
        p_s = tf_s.paragraphs[0]
        p_s.text = lbl
        p_s.font.name = "Segoe UI"
        p_s.font.size = Pt(8.5)
        p_s.font.bold = True
        p_s.font.color.rgb = C_NAVY_DARK
        p_s.alignment = PP_ALIGN.CENTER
        cur_bx += w

    # Capacity summary text below bar
    tb_csum = s10.shapes.add_textbox(Inches(1.0), Inches(5.28), Inches(6.25), Inches(1.2))
    tf_csum = tb_csum.text_frame
    tf_csum.word_wrap = True
    p_cs0 = tf_csum.paragraphs[0]
    p_cs0.text = "💡 Hiệu Quả Quy Hoạch Bộ Nhớ:"
    p_cs0.font.name = "Segoe UI"
    p_cs0.font.size = Pt(11)
    p_cs0.font.bold = True
    p_cs0.font.color.rgb = C_BLUE_ACCENT
    p_cs0.space_after = Pt(2)
    p_cs1 = tf_csum.add_paragraph()
    p_cs1.text = "Bản đồ phân vùng bộ nhớ được chia tách vật lý độc lập theo từng Sector 64 KB, đảm bảo lệnh xóa Sector của một vùng không bao giờ ảnh hưởng hay gây hỏng hóc tới mã máy firmware và cơ sở dữ liệu các vùng khác."
    p_cs1.font.name = "Segoe UI"
    p_cs1.font.size = Pt(10)
    p_cs1.font.color.rgb = C_TEXT_MUTED

    add_card(s10, Inches(7.8), Inches(1.35), Inches(4.733), Inches(5.35), C_GREEN)
    tb_xip = s10.shapes.add_textbox(Inches(8.0), Inches(1.5), Inches(4.333), Inches(3.2))
    tf_xip = tb_xip.text_frame
    tf_xip.word_wrap = True

    p_x0 = tf_xip.paragraphs[0]
    p_x0.text = "Cơ Chế Thực Thi Tại Chỗ (XIP)"
    p_x0.font.name = "Segoe UI"
    p_x0.font.size = Pt(14)
    p_x0.font.bold = True
    p_x0.font.color.rgb = C_GREEN
    p_x0.space_after = Pt(8)

    xip_points = [
        ("Không cần nạp vào RAM:", "PicoRV32 đọc mã máy trực tiếp từ Flash thông qua bộ điều khiển spimemio.v, tiết kiệm diện tích SRAM trên chip."),
        ("Vector Reset 0x0025_0000:", "Ngay khi nhả tín hiệu rst_n, CPU bắt đầu fetch lệnh đầu tiên tại Sector 37 trong Flash."),
        ("Hàm flashio_worker độc đáo:", "Khi ghi hoặc xóa Flash, hàm điều khiển tạm thời chuyển vào 1KB SRAM để thực thi an toàn, không bị xung đột lệnh fetch."),
        ("Tự động Polling cờ WIP:", "Khối SPIMEMIO tự động kiểm tra bit bận của Flash bằng phần cứng, giải phóng hoàn toàn thời gian chờ đợi cho CPU.")
    ]
    for xp, xd in xip_points:
        p_xp = tf_xip.add_paragraph()
        p_xp.text = f"▸ {xp}\n"
        p_xp.font.name = "Segoe UI"
        p_xp.font.size = Pt(10.5)
        p_xp.font.bold = True
        p_xp.font.color.rgb = C_TEXT_DARK
        p_xp.space_after = Pt(4)
        run_xd = p_xp.add_run()
        run_xd.text = f"  {xd}"
        run_xd.font.bold = False
        run_xd.font.color.rgb = C_TEXT_MUTED
        run_xd.font.size = Pt(10)

    # XIP Flow Box
    add_card(s10, Inches(8.0), Inches(4.8), Inches(4.333), Inches(1.7), C_GREEN, RGBColor(240, 253, 244))
    tb_xf = s10.shapes.add_textbox(Inches(8.1), Inches(4.86), Inches(4.133), Inches(1.55))
    tf_xf = tb_xf.text_frame
    tf_xf.word_wrap = True
    p_xf0 = tf_xf.paragraphs[0]
    p_xf0.text = "⚡ Chu Trình Thực Thi Lệnh XIP (Fast Read):"
    p_xf0.font.name = "Segoe UI"
    p_xf0.font.size = Pt(10.5)
    p_xf0.font.bold = True
    p_xf0.font.color.rgb = C_GREEN
    p_xf0.space_after = Pt(3)

    p_xf1 = tf_xf.add_paragraph()
    p_xf1.text = "1. CPU phát địa chỉ Fetch PC: 0x0025_0000\n2. SPIMEMIO kích hoạt Fast Read (Lệnh 0x0B)\n3. Đọc 4 byte mã máy qua chân MISO\n4. Trả về bus dữ liệu ➔ PicoRV32 thực thi ngay!"
    p_xf1.font.name = "Segoe UI"
    p_xf1.font.size = Pt(9.5)
    p_xf1.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 11: PHẦN MỀM HOST CONSOLE TRÊN MÁY TÍNH (host/main.c)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Chương 3 | Phần mềm quản trị trên máy tính", "3.7. Bước 7: Giao Diện Điều Khiển Host Console 13 Chức Năng (host/main.c)", 11)

    add_card(s11, Inches(0.8), Inches(1.35), Inches(5.6), Inches(5.35), C_NAVY_MID, RGBColor(15, 23, 42))
    tb_term = s11.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(5.2), Inches(5.0))
    tf_term = tb_term.text_frame
    tf_term.word_wrap = True

    p_tm0 = tf_term.paragraphs[0]
    p_tm0.text = "RDM6300 RFID - PICORV32 MANAGER CONSOLE"
    p_tm0.font.name = "Consolas"
    p_tm0.font.size = Pt(11.5)
    p_tm0.font.bold = True
    p_tm0.font.color.rgb = C_CYAN_ACCENT
    p_tm0.space_after = Pt(6)

    menu_lines = [
        "[1]  Ping Hardware (Kiem tra ket noi PicoRV32)",
        "[2]  Input & Save New RFID Tag (Nhap 10 so in tren the)",
        "[3]  Check RFID Tag in Flash (Tra cuu danh sach)",
        "[4]  Delete RFID Tag from Flash (Xoa the khoi Flash)",
        "[5]  Virtual Scan: By Decimal (Quet the ao: 10 so)",
        "[6]  Virtual Scan: By Hex (Quet the ao: 10 ky tu Hex)",
        "[7]  View Access Logs from Flash (Xem nhat ky)",
        "[8]  Export Access Logs to CSV (Xuat file vao host/logs)",
        "[9]  Erase Access Logs (Sao luu CSV roi xoa Flash)",
        "[10] Erase Authorized Tags Sector (Xoa toan bo the)",
        "[11] Get SoC Status (Xem trang thai LED, Flash, CPU)",
        "[12] Export RFID Tags to CSV (Xuat danh sach the)",
        "[13] Import RFID Tags from Latest CSV (Nap lai the)",
        "[0]  Exit (Thoat chuong trinh)"
    ]
    for ml in menu_lines:
        p_ml = tf_term.add_paragraph()
        p_ml.text = ml
        p_ml.font.name = "Consolas"
        p_ml.font.size = Pt(9.2)
        p_ml.font.color.rgb = RGBColor(226, 232, 240) if "[5]" not in ml and "[8]" not in ml else C_GREEN
        p_ml.space_after = Pt(1)

    add_card(s11, Inches(6.6), Inches(1.35), Inches(5.933), Inches(5.35), C_PURPLE)
    tb_feat = s11.shapes.add_textbox(Inches(6.8), Inches(1.5), Inches(5.533), Inches(5.0))
    tf_feat = tb_feat.text_frame
    tf_feat.word_wrap = True

    p_ft0 = tf_feat.paragraphs[0]
    p_ft0.text = "Tính Năng Nổi Bật Của Host Console"
    p_ft0.font.name = "Segoe UI"
    p_ft0.font.size = Pt(15)
    p_ft0.font.bold = True
    p_ft0.font.color.rgb = C_PURPLE
    p_ft0.space_after = Pt(10)

    host_features = [
        ("Giao tiếp Win32 Serial API thuần túy:", "Phát triển hoàn toàn bằng ngôn ngữ C, không phụ thuộc thư viện nặng nề, kết nối cổng COM trực tiếp qua chip FTDI FT2232."),
        ("Bộ phân tích định dạng thẻ linh hoạt:", "Người dùng có thể nhập trực tiếp 10 số dập nổi trên thẻ, mã Wiegand (114,37872) hoặc mã Hex 10 ký tự; phần mềm tự động quy đổi."),
        ("Chế độ Quẹt Thẻ Ảo (Virtual Scan):", "Cho phép kiểm thử toàn bộ logic tra cứu Flash và ghi log từ xa mà không cần quẹt thẻ vật lý trên đầu đọc RDM6300."),
        ("Tự động sao lưu và bảo vệ dữ liệu CSV:", "Mỗi khi thêm/xóa thẻ hoặc xóa nhật ký, hệ thống tự động xuất bản ghi ra file CSV kèm dấu thời gian (Timestamp).")
    ]
    for hf, hd in host_features:
        p_hf = tf_feat.add_paragraph()
        p_hf.text = f"▸ {hf}\n"
        p_hf.font.name = "Segoe UI"
        p_hf.font.size = Pt(11.5)
        p_hf.font.bold = True
        p_hf.font.color.rgb = C_TEXT_DARK
        p_hf.space_after = Pt(4)
        run_hd = p_hf.add_run()
        run_hd.text = f"  {hd}"
        run_hd.font.bold = False
        run_hd.font.color.rgb = C_TEXT_MUTED
        run_hd.font.size = Pt(10.5)

    # =========================================================================
    # SLIDE 12: THỰC NGHIỆM TRÊN FPGA BASYS 3 (Hardware Demo)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Chương 4 | Demo kiểm chứng thực nghiệm", "Tạo Mẫu Phần Cứng & Kiểm Chứng Thực Tế Trên Bo Mạch Basys 3", 12)

    col3_w = Inches(3.68)
    col3_h = Inches(3.45)
    col_gap = Inches(0.34)

    # Card 1: Vai trò FPGA
    add_card(s12, start_x, top_y, col3_w, col3_h, C_BLUE_ACCENT)
    tb_fp1 = s12.shapes.add_textbox(start_x + Inches(0.2), top_y + Inches(0.2), col3_w - Inches(0.4), col3_h - Inches(0.4))
    tf_fp1 = tb_fp1.text_frame
    tf_fp1.word_wrap = True
    p_fp1 = tf_fp1.paragraphs[0]
    p_fp1.text = "🎯 Vai Trò Tạo Mẫu (Prototyping)"
    p_fp1.font.name = "Segoe UI"
    p_fp1.font.size = Pt(13.5)
    p_fp1.font.bold = True
    p_fp1.font.color.rgb = C_BLUE_ACCENT
    p_fp1.space_after = Pt(8)

    fp_b1 = [
        ("Nền tảng kiểm chứng thật:", "Basys 3 (XC7A35T) đóng vai trò demo và tạo mẫu phần cứng trước khi tiến hành ASIC."),
        ("Phát hiện lỗi sớm:", "Xác thực CPU PicoRV32 với thẻ RFID thật và SPI Flash thật trong điều kiện nhiễu thực tế."),
        ("Giảm thiểu rủi ro băng đai:", "Đảm bảo tính đúng đắn 100% trước khi gửi bản vẽ đi tape-out ở xưởng đúc.")
    ]
    for b_t, b_d in fp_b1:
        p = tf_fp1.add_paragraph()
        p.text = f"• {b_t}\n"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(3)
        r = p.add_run()
        r.text = f"  {b_d}"
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED
        r.font.size = Pt(9.5)

    # Card 2: STARTUPE2 Primitive
    add_card(s12, start_x + col3_w + col_gap, top_y, col3_w, col3_h, C_AMBER)
    tb_fp2 = s12.shapes.add_textbox(start_x + col3_w + col_gap + Inches(0.2), top_y + Inches(0.2), col3_w - Inches(0.4), col3_h - Inches(0.4))
    tf_fp2 = tb_fp2.text_frame
    tf_fp2.word_wrap = True
    p_fp2 = tf_fp2.paragraphs[0]
    p_fp2.text = "⚙️ Giải Pháp Xilinx STARTUPE2"
    p_fp2.font.name = "Segoe UI"
    p_fp2.font.size = Pt(13.5)
    p_fp2.font.bold = True
    p_fp2.font.color.rgb = C_AMBER
    p_fp2.space_after = Pt(8)

    fp_b2 = [
        ("Vấn đề chân CCLK dùng chung:", "Chân SCK SPI Flash nối cố định với mạch nạp bitstream của FPGA 7-Series."),
        ("Nguyên thủy STARTUPE2:", "Top-level đưa xung SCK từ spimemio vào cổng USRCCLKO của STARTUPE2."),
        ("Làm chủ xung nhịp Flash:", "Cho phép CPU tự do phát xung SCK giao tiếp Flash sau khi FPGA khởi động xong.")
    ]
    for b_t, b_d in fp_b2:
        p = tf_fp2.add_paragraph()
        p.text = f"• {b_t}\n"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(3)
        r = p.add_run()
        r.text = f"  {b_d}"
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED
        r.font.size = Pt(9.5)

    # Card 3: Kết quả thực nghiệm
    add_card(s12, start_x + (col3_w + col_gap)*2, top_y, col3_w, col3_h, C_GREEN)
    tb_fp3 = s12.shapes.add_textbox(start_x + (col3_w + col_gap)*2 + Inches(0.2), top_y + Inches(0.2), col3_w - Inches(0.4), col3_h - Inches(0.4))
    tf_fp3 = tb_fp3.text_frame
    tf_fp3.word_wrap = True
    p_fp3 = tf_fp3.paragraphs[0]
    p_fp3.text = "✅ Kết Quả Thực Nghiệm"
    p_fp3.font.name = "Segoe UI"
    p_fp3.font.size = Pt(13.5)
    p_fp3.font.bold = True
    p_fp3.font.color.rgb = C_GREEN
    p_fp3.space_after = Pt(8)

    fp_b3 = [
        ("Ping Hardware thành công:", "PicoRV32 phản hồi tức thì lệnh 'P' từ máy tính với chuỗi 'PONG:CPU_OK'."),
        ("Xác thực thẻ thật chính xác:", "Quẹt thẻ EM4100 thật trên module RDM6300, LED[2] sáng, đối chiếu Whitelist < 10 µs."),
        ("Lưu trữ nhật ký ổn định:", "Ghi bản ghi SUCC/FAIL vào Flash Sector 49 và xuất trọn vẹn ra file CSV.")
    ]
    for b_t, b_d in fp_b3:
        p = tf_fp3.add_paragraph()
        p.text = f"• {b_t}\n"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(3)
        r = p.add_run()
        r.text = f"  {b_d}"
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED
        r.font.size = Pt(9.5)

    # Bottom Terminal Log Card
    add_card(s12, start_x, Inches(4.98), Inches(11.733), Inches(1.78), C_NAVY_MID, RGBColor(15, 23, 42))
    tb_log = s12.shapes.add_textbox(start_x + Inches(0.2), Inches(5.04), Inches(11.333), Inches(1.65))
    tf_log = tb_log.text_frame
    tf_log.word_wrap = True
    p_lh = tf_log.paragraphs[0]
    p_lh.text = ">_ TRÍCH XUẤT NHẬT KÝ UART GIAO TIẾP THỰC TẾ TRÊN BO MẠCH BASYS 3 (9600-8-N-1):"
    p_lh.font.name = "Consolas"
    p_lh.font.size = Pt(10)
    p_lh.font.bold = True
    p_lh.font.color.rgb = C_CYAN_ACCENT
    p_lh.space_after = Pt(2)

    log_lines = [
        "[HOST -> SoC]    Gửi lệnh 'P' (Ping Hardware) -> Phản hồi: 'PONG:CPU_OK' (Mạch số & firmware sống 100%)",
        "[RDM6300 -> SoC] Quẹt thẻ thật 0007508976 -> STX/ETX khớp -> Checksum XOR: 0xF0 == 0xF0 -> Bật strobe",
        "[PicoRV32 CPU]   Tra cứu Sector 48 (Flash) -> TÌM THẤY THẺ TRONG WHITELIST -> LED[2]=1 (CẤP QUYỀN RA VÀO)",
        "[SPI Flash NVM]  Ghi nhật ký vào Sector 49 -> Xong sau 2.1ms -> Host trích xuất báo cáo CSV hoàn hảo!"
    ]
    for ll in log_lines:
        p_l = tf_log.add_paragraph()
        p_l.text = ll
        p_l.font.name = "Consolas"
        p_l.font.size = Pt(9.2)
        p_l.font.color.rgb = C_GREEN if "CẤP QUYỀN" in ll or "CPU_OK" in ll or "hoàn hảo" in ll else RGBColor(226, 232, 240)
        p_l.space_after = Pt(1)

    # =========================================================================
    # SLIDE 13: THIẾT KẾ VẬT LÝ ASIC TRÊN OPENLANE 2 (Openroad_1.png Căn Khung)
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Chương 5 | Hiện thực hóa vi mạch ASIC", "Thiết Kế Vật Lý Vi Mạch Trên OpenLane 2 & OpenROAD (Sky130A)", 13)

    # Left: Framed Openroad_1.png
    if os.path.exists(img_openroad):
        card_pic = add_card(s13, Inches(0.8), Inches(1.35), Inches(7.3), Inches(5.35), C_NAVY_MID, RGBColor(15, 23, 42))
        s13.shapes.add_picture(img_openroad, Inches(0.9), Inches(1.45), width=Inches(7.1))

    # Right: Physical Specs Card
    add_card(s13, Inches(8.35), Inches(1.35), Inches(4.183), Inches(5.35), C_BLUE_ACCENT)
    tb_or = s13.shapes.add_textbox(Inches(8.55), Inches(1.5), Inches(3.783), Inches(5.0))
    tf_or = tb_or.text_frame
    tf_or.word_wrap = True

    p_or0 = tf_or.paragraphs[0]
    p_or0.text = "Thông Số Thiết Kế Vật Lý"
    p_or0.font.name = "Segoe UI"
    p_or0.font.size = Pt(14)
    p_or0.font.bold = True
    p_or0.font.color.rgb = C_BLUE_ACCENT
    p_or0.space_after = Pt(8)

    phys_specs = [
        ("Công nghệ chế tạo:", "SkyWater 130nm Standard Cells (sky130_fd_sc_hd)."),
        ("Kích thước Die:", "1300 µm x 1300 µm (Diện tích: 1.69 mm²)."),
        ("Kích thước Core:", "1270 µm x 1270 µm (Mật độ Core Utilization tối ưu)."),
        ("Số lượng linh kiện:", "57,544 transistors / devices."),
        ("Số lượng dây kim loại:", "50,028 nets định tuyến đa lớp (met1 đến met5)."),
        ("Mạng lưới nguồn PDN:", "Thanh kim loại Met4 và Met5 đan lưới, độ sụt áp tồi nhất chỉ 0.04% (0.739 mV)."),
        ("Tần số mục tiêu:", "50.0 MHz (Chu kỳ xung nhịp CLK = 20.0 ns).")
    ]
    for sp, sd in phys_specs:
        p = tf_or.add_paragraph()
        p.text = f"▸ {sp}\n"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(3)
        r = p.add_run()
        r.text = f"  {sd}"
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED
        r.font.size = Pt(10)

    # =========================================================================
    # SLIDE 14: KẾT QUẢ KÝ DUYỆT CHẾ TẠO SIGN-OFF TOÀN DIỆN
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Chương 5 | Báo cáo kiểm định Sign-off", "Kết Quả Ký Duyệt Bán Dẫn Tuyệt Đối (Run RUN_2026-09-27_21-51-11)", 14)

    # Left: Sign-off Metrics Cards
    left_so_w = Inches(6.6)
    add_card(s14, Inches(0.8), Inches(1.35), left_so_w, Inches(5.35), C_GREEN)
    tb_so = s14.shapes.add_textbox(Inches(1.0), Inches(1.5), left_so_w - Inches(0.4), Inches(5.0))
    tf_so = tb_so.text_frame
    tf_so.word_wrap = True

    p_so0 = tf_so.paragraphs[0]
    p_so0.text = "Bảng Điểm Ký Duyệt Tape-out (100% CLEAN)"
    p_so0.font.name = "Segoe UI"
    p_so0.font.size = Pt(15)
    p_so0.font.bold = True
    p_so0.font.color.rgb = C_GREEN
    p_so0.space_after = Pt(10)

    so_metrics = [
        ("Netgen LVS (Layout vs Schematic):", "CLEAN 100% | 57,544 devices và 50,028 nets trùng khớp tuyệt đối, 0 mismatch, 0 lỗi nối dây."),
        ("Magic DRC & KLayout DRC:", "0 vi phạm hình học bán dẫn (0 violations)."),
        ("Hiệu ứng Ăng-ten (Antenna Rules):", "0 net vi phạm, 0 pin vi phạm trên tất cả các lớp kim loại sau khi chèn diode bảo vệ tự động."),
        ("Định thời tĩnh STA (Timing Sign-off):", "ĐẠT MET TIMING trên toàn bộ 9 góc đo công nghệ (PVT Corners: nom, min, max, tt, ss, ff) ở tần số 50 MHz. Không có lỗi Setup, không có lỗi Hold."),
        ("Kiểm tra sụt áp (IR Drop Analysis):", "Sụt áp nguồn danh định 1.8V xấu nhất chỉ 0.739 mV (tương đương 0.04%).")
    ]
    for m_title, m_desc in so_metrics:
        p = tf_so.add_paragraph()
        p.text = f"✅ {m_title}\n"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(2)
        r = p.add_run()
        r.text = f"    {m_desc}"
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED
        r.font.size = Pt(9.5)

    # 4 metric summary chips at bottom of Left Card
    so_badges = [
        (Inches(1.0), Inches(5.12), "Khuôn Chip Die Size", "1300 x 1300 µm (1.69 mm²)", C_BLUE_ACCENT),
        (Inches(4.15), Inches(5.12), "Thiết Bị Netgen LVS", "57,544 Devs (0 Mismatch)", C_GREEN),
        (Inches(1.0), Inches(5.82), "Kiểm Tra DRC & Antenna", "0 DRC | 0 Antenna", C_PURPLE),
        (Inches(4.15), Inches(5.82), "STA Timing 50.0 MHz", "MET TIMING (9/9 Corners)", C_GREEN),
    ]
    for bx, by, b_title, b_val, b_col in so_badges:
        bd_shape = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, by, Inches(3.0), Inches(0.65))
        bd_shape.fill.solid()
        bd_shape.fill.fore_color.rgb = RGBColor(241, 245, 249)
        bd_shape.line.color.rgb = b_col
        bd_shape.line.width = Pt(1.2)
        tf_b = bd_shape.text_frame
        tf_b.word_wrap = True
        p_bt = tf_b.paragraphs[0]
        p_bt.text = b_title
        p_bt.font.name = "Segoe UI"
        p_bt.font.size = Pt(8.5)
        p_bt.font.bold = True
        p_bt.font.color.rgb = C_TEXT_MUTED
        p_bt.space_after = Pt(1)
        p_bv = tf_b.add_paragraph()
        p_bv.text = b_val
        p_bv.font.name = "Segoe UI"
        p_bv.font.size = Pt(10)
        p_bv.font.bold = True
        p_bv.font.color.rgb = b_col

    # Right: Screenshot + STA 9-Corner Summary Box
    right_so_x = Inches(7.65)
    right_so_w = Inches(4.883)
    add_card(s14, right_so_x, Inches(1.35), right_so_w, Inches(5.35), C_BLUE_ACCENT)

    # Screenshot at top
    if os.path.exists(img_signoff):
        s14.shapes.add_picture(img_signoff, right_so_x + Inches(0.2), Inches(1.5), width=right_so_w - Inches(0.4))

    # STA Table Box below
    tb_sta = s14.shapes.add_textbox(right_so_x + Inches(0.2), Inches(3.2), right_so_w - Inches(0.4), Inches(3.3))
    tf_sta = tb_sta.text_frame
    tf_sta.word_wrap = True

    p_stah = tf_sta.paragraphs[0]
    p_stah.text = "STA 9 PVT CORNERS KÝ DUYỆT (50 MHz)"
    p_stah.font.name = "Segoe UI"
    p_stah.font.size = Pt(12)
    p_stah.font.bold = True
    p_stah.font.color.rgb = C_BLUE_ACCENT
    p_stah.space_after = Pt(6)

    corners = [
        ("nom_tt_025C_1v80", "Điển hình: 25°C, 1.8V", "MET TIMING ✅"),
        ("nom_ss_100C_1v60", "Chậm: 100°C, 1.6V", "MET TIMING ✅"),
        ("nom_ff_n40C_1v95", "Nhanh: -40°C, 1.95V", "MET TIMING ✅"),
        ("min_ss_100C_1v60", "Góc trễ lớn nhất", "MET TIMING ✅"),
        ("max_ff_n40C_1v95", "Góc nhanh nhất", "MET TIMING ✅"),
    ]
    for c_name, c_cond, c_eval in corners:
        p_c = tf_sta.add_paragraph()
        p_c.text = f"• {c_name}: "
        p_c.font.name = "Consolas"
        p_c.font.size = Pt(10)
        p_c.font.bold = True
        p_c.font.color.rgb = C_TEXT_DARK
        p_c.space_after = Pt(2)
        r_c = p_c.add_run()
        r_c.text = f"{c_eval}"
        r_c.font.name = "Segoe UI"
        r_c.font.bold = True
        r_c.font.color.rgb = C_GREEN

    p_ir = tf_sta.add_paragraph()
    p_ir.text = "\n• Worst IR Drop: 0.04% (0.739 mV) — Mạng PDN cực kỳ vững chắc!"
    p_ir.font.name = "Segoe UI"
    p_ir.font.size = Pt(10.5)
    p_ir.font.bold = True
    p_ir.font.color.rgb = C_PURPLE

    # =========================================================================
    # SLIDE 15: THẢO LUẬN & ĐÁNH GIÁ TỐI ƯU HÓA PPA
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Chương 6 | Đánh giá kỹ thuật", "Thảo Luận & Đánh Giá Tối Ưu Hóa PPA (Power - Performance - Area)", 15)

    col3_h = Inches(3.85)
    add_card(s15, start_x, top_y, col3_w, col3_h, C_BLUE_ACCENT)
    tb_ppa1 = s15.shapes.add_textbox(start_x + Inches(0.2), top_y + Inches(0.2), col3_w - Inches(0.4), col3_h - Inches(0.4))
    tf_ppa1 = tb_ppa1.text_frame
    tf_ppa1.word_wrap = True
    p = tf_ppa1.paragraphs[0]
    p.text = "⚡ Tối Ưu Hiệu Năng (Performance)"
    p.font.name = "Segoe UI"
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_ACCENT
    p.space_after = Pt(8)

    ppa_b1 = [
        ("Xử lý phần cứng 1 chu kỳ:", "Giải mã khung ASCII và tính XOR Checksum hoàn tất trong 20ns mà không tốn lệnh CPU."),
        ("Bộ đệm FIFO phần cứng:", "Cách ly tốc độ giữa máy tính và chu kỳ ghi Flash, chống nghẽn bus tuyệt đối."),
        ("Độ trễ xác thực siêu nhỏ:", "Từ lúc quẹt thẻ đến khi nhận kết quả kiểm tra chỉ mất dưới 10 micro-giây.")
    ]
    for bt, bd in ppa_b1:
        p = tf_ppa1.add_paragraph()
        p.text = f"• {bt}\n"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(3)
        r = p.add_run()
        r.text = f"  {bd}"
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED
        r.font.size = Pt(9.5)

    add_card(s15, start_x + col3_w + col_gap, top_y, col3_w, col3_h, C_GREEN)
    tb_ppa2 = s15.shapes.add_textbox(start_x + col3_w + col_gap + Inches(0.2), top_y + Inches(0.2), col3_w - Inches(0.4), col3_h - Inches(0.4))
    tf_ppa2 = tb_ppa2.text_frame
    tf_ppa2.word_wrap = True
    p = tf_ppa2.paragraphs[0]
    p.text = "📐 Tối Ưu Diện Tích & Công Suất"
    p.font.name = "Segoe UI"
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.font.color.rgb = C_GREEN
    p.space_after = Pt(8)

    ppa_b2 = [
        ("1KB Data SRAM tinh gọn:", "Được đo ni đóng giày đúng nhu cầu lưu Stack Pointer (0x400) và biến, tiết kiệm diện tích."),
        ("Tận dụng Flash ngoài:", "Lưu firmware XIP và cơ sở dữ liệu trên Flash SPI giúp khuôn chip chỉ tốn 1.69 mm²."),
        ("Lưới nguồn PDN vững chắc:", "Độ sụt áp chỉ 0.04% đảm bảo tiết kiệm điện năng và vận hành ổn định lâu dài.")
    ]
    for bt, bd in ppa_b2:
        p = tf_ppa2.add_paragraph()
        p.text = f"• {bt}\n"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(3)
        r = p.add_run()
        r.text = f"  {bd}"
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED
        r.font.size = Pt(9.5)

    add_card(s15, start_x + (col3_w + col_gap)*2, top_y, col3_w, col3_h, C_PURPLE)
    tb_ppa3 = s15.shapes.add_textbox(start_x + (col3_w + col_gap)*2 + Inches(0.2), top_y + Inches(0.2), col3_w - Inches(0.4), col3_h - Inches(0.4))
    tf_ppa3 = tb_ppa3.text_frame
    tf_ppa3.word_wrap = True
    p = tf_ppa3.paragraphs[0]
    p.text = "🚀 Định Hướng Nâng Cấp Tiếp Theo"
    p.font.name = "Segoe UI"
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.font.color.rgb = C_PURPLE
    p.space_after = Pt(8)

    ppa_b3 = [
        ("Tích hợp macro OpenRAM:", "Thay thế standard cell flip-flops bằng macro bộ nhớ nhúng OpenRAM giúp giảm 25-35% diện tích."),
        ("Nâng cấp Quad-SPI (QSPI):", "Nâng giao tiếp Flash từ 1-bit lên 4-bit giúp tăng tốc độ đọc dữ liệu thẻ gấp 4 lần."),
        ("Mã hóa phần cứng AES-128:", "Mã hóa cơ sở dữ liệu thẻ trước khi lưu vào Flash, chống đọc trộm dữ liệu trái phép.")
    ]
    for bt, bd in ppa_b3:
        p = tf_ppa3.add_paragraph()
        p.text = f"• {bt}\n"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(3)
        r = p.add_run()
        r.text = f"  {bd}"
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED
        r.font.size = Pt(9.5)

    # Bottom PPA Summary Card
    add_card(s15, start_x, Inches(5.42), Inches(11.733), Inches(1.3), C_GREEN, RGBColor(240, 253, 244))
    tb_ppabot = s15.shapes.add_textbox(start_x + Inches(0.25), Inches(5.48), Inches(11.233), Inches(1.15))
    tf_ppabot = tb_ppabot.text_frame
    tf_ppabot.word_wrap = True
    p_p0 = tf_ppabot.paragraphs[0]
    p_p0.text = "💡 TỔNG KẾT ĐÁNH GIÁ CHỈ SỐ PPA TOÀN DIỆN:"
    p_p0.font.name = "Segoe UI"
    p_p0.font.size = Pt(11)
    p_p0.font.bold = True
    p_p0.font.color.rgb = C_GREEN
    p_p0.space_after = Pt(2)

    p_p1 = tf_ppabot.add_paragraph()
    p_p1.text = "• Hiệu năng (Performance): Xác thực thẻ tức thì (< 10 µs), giải mã phần cứng 1 chu kỳ clock song song không tốn tài nguyên CPU.\n• Diện tích & Điện năng (Area & Power): Khuôn chip tối giản 1.69 mm² nhờ kiến trúc Flash XIP & SRAM 1KB, sụt áp chỉ 0.04% (0.739 mV).\n• Khả năng mở rộng: Sẵn sàng nâng cấp macro OpenRAM và bus Quad-SPI 4-bit."
    p_p1.font.name = "Segoe UI"
    p_p1.font.size = Pt(9.5)
    p_p1.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 16: KẾT LUẬN & TỔNG KẾT ĐỀ TÀI (Thank You Slide)
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    bg16 = s16.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg16.fill.solid()
    bg16.fill.fore_color.rgb = C_NAVY_DARK
    bg16.line.fill.background()

    card_fin = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
    card_fin.fill.solid()
    card_fin.fill.fore_color.rgb = C_NAVY_MID
    card_fin.line.color.rgb = C_GREEN
    card_fin.line.width = Pt(2.0)

    tb_end = s16.shapes.add_textbox(Inches(1.2), Inches(1.1), Inches(10.9), Inches(5.2))
    tf_end = tb_end.text_frame
    tf_end.word_wrap = True

    p_e0 = tf_end.paragraphs[0]
    p_e0.text = "TỔNG KẾT ĐỒ ÁN & THÀNH TỰU ĐẠT ĐƯỢC"
    p_e0.font.name = "Segoe UI"
    p_e0.font.size = Pt(22)
    p_e0.font.bold = True
    p_e0.font.color.rgb = C_GREEN
    p_e0.space_after = Pt(14)

    concl_points = [
        ("Hoàn thành xuất sắc mục tiêu thiết kế SoC chuyên dụng:", "Hiện thực hóa hệ thống kiểm soát ra vào độc lập (Offline Standalone), loại bỏ hoàn toàn rủi ro bảo mật và độ trễ mạng."),
        ("Kiểm chứng thực nghiệm 100% trên FPGA Basys 3:", "Xác thực module RDM6300 thật, thẻ RFID thật, chip SPI Flash thật và phần mềm Host C hoạt động đồng bộ hoàn hảo."),
        ("Đạt chuẩn ký duyệt chế tạo bán dẫn (Full Tapeout Ready):", "Lượt chạy OpenLane 2 đạt 0 lỗi DRC, 0 lỗi LVS (57,544 devices khớp 100%), 0 vi phạm Antenna, và MET TIMING ở cả 9 corners tần số 50 MHz."),
        ("Phương pháp thiết kế Software-First khoa học:", "Định hình tập lệnh và chức năng phần mềm trước giúp tối ưu hóa tối đa diện tích silicon và thời gian phát triển.")
    ]
    for cp, cd in concl_points:
        p_c = tf_end.add_paragraph()
        p_c.text = f"✔ {cp} "
        p_c.font.name = "Segoe UI"
        p_c.font.size = Pt(13)
        p_c.font.bold = True
        p_c.font.color.rgb = C_WHITE
        p_c.space_after = Pt(4)
        run_cd = p_c.add_run()
        run_cd.text = cd
        run_cd.font.bold = False
        run_cd.font.color.rgb = RGBColor(203, 213, 225)
        run_cd.font.size = Pt(12)

    p_thanks = tf_end.add_paragraph()
    p_thanks.alignment = PP_ALIGN.CENTER
    p_thanks.text = "\nCHÂN THÀNH CẢM ƠN QUÝ THẦY CÔ & HỘI ĐỒNG BẢO VỆ!\nQ & A"
    p_thanks.font.name = "Segoe UI"
    p_thanks.font.size = Pt(20)
    p_thanks.font.bold = True
    p_thanks.font.color.rgb = C_CYAN_ACCENT

    # Save Presentation
    out_pptx = os.path.join(cur_dir, "Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.pptx")
    prs.save(out_pptx)
    print(f"[SUCCESS] Refined 16-Slide PPTX generated successfully at: {out_pptx}")

if __name__ == '__main__':
    create_deck()
