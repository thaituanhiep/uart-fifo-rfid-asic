# -*- coding: utf-8 -*-
"""
Script: create_presentation.py
Tạo bộ slide báo cáo PowerPoint 16:9 widescreen tiêu chuẩn xuất bản cao cấp (Publication-Grade).
Bao gồm:
- Slide 1: Bìa Đồ Án Tốt Nghiệp
- Slide 2: Phần 1 - Tính Cấp Thiết Của Hệ Thống Offline & Vai Trò Cốt Tử Của SPI Flash NVM (3 Cột Toàn Slide)
- Slide 3: Phần 3 - Sơ Đồ Khối Kiến Trúc Vi Hệ Thống SoC PicoRV32 (4MB Flash, 1KB SRAM, 32 Fifo)
- Slide 4: Phần 3 - Sơ Đồ Khối Kiến Trúc Vi Mạch UART RTL (Draw.io Đen Trắng & Đặc Tả Thiết Kế)
- Slide 5: Phần 4 - Testbench 1: Kiểm Thử Phần Cứng RTL Thuần Cho UART MMIO & FIFO (tb_uart_rtl.v)
- Slide 6: Phần 4 - Testbench 2: Kiểm Thử Tích Hợp Toàn Diện Top SoC Boot Flash & Ping (tb_uart_ping.v)
- Slide 7: Phần 5 - Demo Thực Nghiệm Trên FPGA: Thiết Lập Kết Nối Phần Cứng & Nguồn 5V/Trở 1k
- Slide 8: Phần 5 - Demo Thực Nghiệm Trên FPGA: Giao Diện Host Console CLI & Đánh Giá Chức Năng
- Slide 9: Phần 6 - Thiết Kế Vật Lý ASIC: Minh Chứng Ký Duyệt Sign-off, Bản Vẽ OpenROAD & Cấu Hình OpenLane
- Slide 10: Phần 6 - Thiết Kế Vật Lý ASIC: Bảng Tổng Hợp Kết Quả Thiết Kế Vật Lý & Chỉ Số PPA
- Slide 11: Phần 6 - Thiết Kế Vật Lý ASIC: Phân Tích Định Thời Tĩnh STA & Báo Cáo Multi-Corner Timing
- Slide 12: Tổng Kết Đồ Án Và Các Đóng Góp Nổi Bật

Tổng cộng: 12 slide súc tích, mạch lạc, trực quan, phục vụ thuyết trình đồ án tốt nghiệp xuất sắc.
"""

import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Bảng màu thiết kế chuyên nghiệp
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
    doc_dir = os.path.dirname(cur_dir) if os.path.basename(cur_dir) == "temp" else cur_dir
    project_root = os.path.dirname(doc_dir)

    img_fig1 = os.path.join(cur_dir, "fig1_block_diagram.png")
    if not os.path.exists(img_fig1):
        img_fig1 = os.path.join(doc_dir, "fig1_block_diagram.png")

    img_openroad = os.path.join(project_root, "OpenROAD.png")
    if not os.path.exists(img_openroad):
        img_openroad = os.path.join(cur_dir, "OpenROAD.png")
    if not os.path.exists(img_openroad):
        img_openroad = os.path.join(doc_dir, "OpenROAD.png")
    if not os.path.exists(img_openroad):
        img_openroad = os.path.join(cur_dir, "Openroad_1.png")

    img_signoff = os.path.join(project_root, "AntennaLvsDrc.png")
    if not os.path.exists(img_signoff):
        img_signoff = os.path.join(cur_dir, "AntennaLvsDrc.png")
    if not os.path.exists(img_signoff):
        img_signoff = os.path.join(doc_dir, "AntennaLvsDrc.png")

    img_device = os.path.join(project_root, "Device.jpg")
    if not os.path.exists(img_device):
        img_device = os.path.join(cur_dir, "Device.jpg")
    if not os.path.exists(img_device):
        img_device = os.path.join(doc_dir, "Device.jpg")

    img_uart_bw = os.path.join(cur_dir, "uart_architecture_bw_diagram.png")
    if not os.path.exists(img_uart_bw):
        img_uart_bw = os.path.join(doc_dir, "uart_architecture_bw_diagram.png")
    if not os.path.exists(img_uart_bw):
        img_uart_bw = os.path.join(project_root, "temp", "uart_architecture_bw_diagram.png")

    img_fig2a = os.path.join(cur_dir, "fig2a_rdm6300_subsystem.png")
    if not os.path.exists(img_fig2a):
        img_fig2a = os.path.join(doc_dir, "fig2a_rdm6300_subsystem.png")
    if not os.path.exists(img_fig2a):
        img_fig2a = os.path.join(project_root, "temp", "fig2a_rdm6300_subsystem.png")

    img_stages = [
        os.path.join(cur_dir, f"stage{i}_bw_diagram.png") for i in range(1, 6)
    ]

    img_tb_uart_rtl = os.path.join(cur_dir, "waveform_tb_uart_rtl.png")
    if not os.path.exists(img_tb_uart_rtl):
        img_tb_uart_rtl = os.path.join(doc_dir, "waveform_tb_uart_rtl.png")

    img_tb_uart_ping = os.path.join(cur_dir, "waveform_tb_uart_ping.png")
    if not os.path.exists(img_tb_uart_ping):
        img_tb_uart_ping = os.path.join(doc_dir, "waveform_tb_uart_ping.png")

    TOTAL_SLIDES = 13

    # Helper: Tiêu đề slide chuẩn hóa
    def add_header(slide, category, title, slide_num, total_slides=TOTAL_SLIDES):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG_LIGHT
        bg.line.fill.background()

        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.1))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = C_BLUE_ACCENT
        top_bar.line.fill.background()

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
        p_title.font.size = Pt(17.0)
        p_title.font.bold = True
        p_title.font.color.rgb = C_TEXT_DARK

        footer_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.02))
        footer_line.fill.solid()
        footer_line.fill.fore_color.rgb = RGBColor(226, 232, 240)
        footer_line.line.fill.background()

        tb_foot = slide.shapes.add_textbox(Inches(0.8), Inches(7.1), Inches(8.0), Inches(0.3))
        tf_foot = tb_foot.text_frame
        tf_foot.margin_left = tf_foot.margin_top = tf_foot.margin_right = tf_foot.margin_bottom = 0
        p_foot = tf_foot.paragraphs[0]
        p_foot.text = "Đồ Án: SoC PicoRV32 RFID RDM6300 & SPI Flash | FPT Jetking Chip Design - SEM3 | HV: Thái Tuấn Hiệp"
        p_foot.font.name = "Segoe UI"
        p_foot.font.size = Pt(9.5)
        p_foot.font.color.rgb = C_TEXT_MUTED

        tb_num = slide.shapes.add_textbox(Inches(11.0), Inches(7.1), Inches(1.533), Inches(0.3))
        tf_num = tb_num.text_frame
        tf_num.margin_left = tf_num.margin_top = tf_num.margin_right = tf_num.margin_bottom = 0
        p_num = tf_num.paragraphs[0]
        p_num.text = f"{slide_num:02d} / {total_slides:02d}"
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.font.name = "Segoe UI"
        p_num.font.size = Pt(9.5)
        p_num.font.bold = True
        p_num.font.color.rgb = C_BLUE_ACCENT

    # Helper: Hộp nội dung có viền (Card)
    def add_card(slide, x, y, w, h, bg_color=C_CARD_BG, border_color=C_CARD_BORDER, border_width=1.0):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
        try:
            card.adjustments[0] = 0.02
        except Exception:
            pass
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(border_width)
        return card

    # Helper: Hộp mã nguồn dạng Terminal / IDE Code Box
    def add_code_box(slide, x, y, w, h, title, lines, status_text=None, title_color=C_CYAN_ACCENT, font_size=8.0, line_spacing=1.08):
        card = add_card(slide, x, y, w, h, bg_color=C_NAVY_DARK, border_color=C_NAVY_MID, border_width=1.5)
        tb_t = slide.shapes.add_textbox(x + Inches(0.15), y + Inches(0.08), w - Inches(0.3), Inches(0.32))
        tf_t = tb_t.text_frame
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = f">_  {title}"
        p_t.font.name = "Consolas"
        p_t.font.size = Pt(10.5)
        p_t.font.bold = True
        p_t.font.color.rgb = title_color

        h_code = h - Inches(0.45) if not status_text else h - Inches(0.78)
        tb_c = slide.shapes.add_textbox(x + Inches(0.15), y + Inches(0.40), w - Inches(0.3), h_code)
        tf_c = tb_c.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0

        for idx, line in enumerate(lines):
            p = tf_c.paragraphs[0] if idx == 0 else tf_c.add_paragraph()
            p.text = line
            p.font.name = "Consolas"
            p.font.size = Pt(font_size)
            p.line_spacing = line_spacing
            p.space_after = 0
            if "[PASS]" in line or "100%" in line or "CONFIRMED" in line or "MET TIMING" in line or "[SUCCESS]" in line or "PASSED" in line:
                p.font.color.rgb = C_GREEN
                p.font.bold = True
            elif "[TEST" in line or "[BOOT]" in line or "[EXEC]" in line or "[UART" in line or "[HOST" in line or "[TB]" in line or "[FLASH" in line:
                p.font.color.rgb = C_CYAN_ACCENT
                p.font.bold = True
            elif line.strip().startswith("//") or line.strip().startswith("/*") or line.strip().startswith("*") or line.strip().startswith("#"):
                p.font.color.rgb = RGBColor(148, 163, 184)
            elif "parameter" in line or "assign" in line or "module" in line or "output" in line or "input" in line or "#define" in line:
                p.font.color.rgb = RGBColor(254, 215, 170)
            elif "return" in line or "if" in line or "while" in line or "for" in line or "static" in line or "void" in line:
                p.font.color.rgb = RGBColor(147, 197, 253)
            else:
                p.font.color.rgb = C_WHITE

        if status_text:
            tb_s = slide.shapes.add_textbox(x + Inches(0.15), y + h - Inches(0.42), w - Inches(0.3), Inches(0.3))
            tf_s = tb_s.text_frame
            tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0
            p_s = tf_s.paragraphs[0]
            p_s.text = status_text
            p_s.font.name = "Segoe UI"
            p_s.font.size = Pt(9.5)
            p_s.font.bold = True
            p_s.font.color.rgb = C_GREEN


    # =========================================================================
    # SLIDE 01: TRANG BÌA (Title Slide) - LOGO ECOSYSTEM
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

    # 1. Header & Main Title Textbox (spanning full width)
    tb_title = s1.shapes.add_textbox(Inches(1.05), Inches(0.98), Inches(11.233), Inches(1.55))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0

    p_org = tf_title.paragraphs[0]
    p_org.text = "FPT JETKING — CHIP DESIGN"
    p_org.font.name = "Segoe UI"
    p_org.font.size = Pt(13.5)
    p_org.font.bold = True
    p_org.font.color.rgb = C_CYAN_ACCENT
    p_org.space_after = Pt(8)

    p_main = tf_title.add_paragraph()
    p_main.text = "THIẾT KẾ HỆ THỐNG SOC XỬ LÝ DỮ LIỆU THẺ RA VÀO RFID\nTỐI ƯU RTL TO GDSII TRÊN CHIP ASIC"
    p_main.font.name = "Segoe UI"
    p_main.font.size = Pt(25.0)
    p_main.font.bold = True
    p_main.font.color.rgb = C_WHITE
    p_main.line_spacing = 1.22

    # 2. Left Column: Subtitle & Student / Advisor Info
    tb_info = s1.shapes.add_textbox(Inches(1.05), Inches(2.72), Inches(7.4), Inches(2.45))
    tf_info = tb_info.text_frame
    tf_info.word_wrap = True
    tf_info.margin_left = tf_info.margin_right = tf_info.margin_top = tf_info.margin_bottom = 0

    p_sub = tf_info.paragraphs[0]
    p_sub.text = "Giao tiếp RFID RDM6300 | Lưu trữ Whitelist SPI Flash NVM\nTạo mẫu Basys 3 FPGA | Ký duyệt ASIC OpenLane 2 (SkyWater 130nm)"
    p_sub.font.name = "Segoe UI"
    p_sub.font.size = Pt(12.0)
    p_sub.font.color.rgb = RGBColor(203, 213, 225)
    p_sub.space_after = Pt(14)
    p_sub.line_spacing = 1.25

    p_info1 = tf_info.add_paragraph()
    p_info1.text = "Học viên thực hiện :  Thái Tuấn Hiệp"
    p_info1.font.name = "Segoe UI"
    p_info1.font.size = Pt(13.5)
    p_info1.font.bold = True
    p_info1.font.color.rgb = C_WHITE
    p_info1.space_after = Pt(6)

    p_info2 = tf_info.add_paragraph()
    p_info2.text = "Giảng viên hướng dẫn :  ThS. Nguyễn Văn Đông"
    p_info2.font.name = "Segoe UI"
    p_info2.font.size = Pt(12.5)
    p_info2.font.color.rgb = RGBColor(226, 232, 240)
    p_info2.space_after = Pt(6)

    p_info3 = tf_info.add_paragraph()
    p_info3.text = "Học kỳ :  SEM3  |  Chuyên ngành: Thiết kế Vi mạch Bán dẫn (Chip Design)"
    p_info3.font.name = "Segoe UI"
    p_info3.font.size = Pt(11.5)
    p_info3.font.italic = True
    p_info3.font.color.rgb = RGBColor(148, 163, 184)

    # 3. Right Column: Card with RFID Reader & 125kHz Card image
    card_r = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.70), Inches(2.65), Inches(3.58), Inches(2.55))
    try:
        card_r.adjustments[0] = 0.04
    except Exception:
        pass
    card_r.fill.solid()
    card_r.fill.fore_color.rgb = RGBColor(15, 23, 42)
    card_r.line.color.rgb = C_CYAN_ACCENT
    card_r.line.width = Pt(1.5)

    img_rfid_card = os.path.join(cur_dir, "rfid_card_rounded.png")
    if not os.path.exists(img_rfid_card):
        img_rfid_card = os.path.join(doc_dir, "rfid_card_rounded.png")
    if os.path.exists(img_rfid_card):
        s1.shapes.add_picture(img_rfid_card, Inches(8.78), Inches(2.72), Inches(3.42), Inches(2.20))

    tb_cap = s1.shapes.add_textbox(Inches(8.70), Inches(4.90), Inches(3.58), Inches(0.28))
    tf_cap = tb_cap.text_frame
    tf_cap.margin_left = tf_cap.margin_right = tf_cap.margin_top = tf_cap.margin_bottom = 0
    p_cap = tf_cap.paragraphs[0]
    p_cap.text = "Đầu đọc RDM6300 & Thẻ RFID 125kHz (EM4100)"
    p_cap.alignment = PP_ALIGN.CENTER
    p_cap.font.name = "Segoe UI"
    p_cap.font.size = Pt(9.5)
    p_cap.font.bold = True
    p_cap.font.color.rgb = RGBColor(147, 197, 253)

    # Logo header label
    tb_lbl = s1.shapes.add_textbox(Inches(1.05), Inches(5.32), Inches(11.233), Inches(0.28))
    tf_lbl = tb_lbl.text_frame
    tf_lbl.margin_left = tf_lbl.margin_right = tf_lbl.margin_top = tf_lbl.margin_bottom = 0
    p_l = tf_lbl.paragraphs[0]
    p_l.text = "CÔNG CỤ EDA & HỆ SINH THÁI CÔNG NGHỆ SỬ DỤNG TRONG ĐỒ ÁN:"
    p_l.font.name = "Segoe UI"
    p_l.font.size = Pt(10.5)
    p_l.font.bold = True
    p_l.font.color.rgb = C_CYAN_ACCENT

    # Logo search directories
    logo_candidates = [
        os.path.join(cur_dir, "logos"),
        os.path.join(doc_dir, "logos"),
        os.path.join(cur_dir, "temp", "logos"),
        os.path.join(project_root, "rdm6300-picorv32-rom-data", "document", "logos"),
    ]
    resolved_logo_dir = cur_dir
    for ld in logo_candidates:
        if os.path.exists(ld):
            resolved_logo_dir = ld
            break

    badges_list = [
        ("badge_openlane.png", 247, 87),
        ("badge_vivado.png", 240, 87),
        ("badge_fpga.png", 254, 87),
        ("badge_riscv.png", 381, 87),
        ("badge_skywater.png", 290, 87),
    ]

    b_h = Inches(0.72)
    b_widths = [b_h * (w / h) for _, w, h in badges_list]
    tot_bw = sum(b_widths)
    av_w = Inches(11.233)
    b_gap = (av_w - tot_bw) / (len(badges_list) - 1)
    bx = Inches(1.05)
    by = Inches(5.66)

    for (b_fname, _, _), bw in zip(badges_list, b_widths):
        bp = os.path.join(resolved_logo_dir, b_fname)
        if os.path.exists(bp):
            s1.shapes.add_picture(bp, bx, by, bw, b_h)
        bx += bw + b_gap
    # SLIDE 2: PHẦN 1 - GIỚI THIỆU DỰ ÁN & LÝ DO CHỌN SPI FLASH NVM
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Phần 1: Giới Thiệu Dự Án",
               "Tính Cấp Thiết & Vai Trò Cốt Tử Của Bộ Nhớ SPI Flash NVM", 2, total_slides=TOTAL_SLIDES)

    col_w = Inches(3.72)
    col_h = Inches(5.62)
    col_y = Inches(1.28)
    col_gap = Inches(0.28)
    start_x = Inches(0.80)

    cols_data = [
        {
            "icon": "🌐",
            "title": "1. HỆ THỐNG OFFLINE",
            "subtitle": "Loại bỏ phụ thuộc Internet & Cloud",
            "border_color": C_BLUE_ACCENT,
            "badge_bg": RGBColor(239, 246, 255),
            "points": [
                ("Triệt tiêu độ trễ mạng:", "Khắc phục triệt để độ trễ lớn (hàng trăm ms đến vài giây), nguy cơ đứt cáp và nghẽn băng thông."),
                ("Phản hồi tức thì (< 10 µs):", "SoC tự giải mã chuỗi RFID và đối chiếu Whitelist tại chỗ trong thời gian thực."),
                ("Bảo mật dữ liệu tuyệt đối:", "Dữ liệu định danh lưu trữ nội bộ khép kín, triệt tiêu 100% rủi ro rò rỉ qua Internet."),
                ("Vận hành liên tục 24/7:", "Hoạt động bền bỉ, tin cậy tại địa bàn biệt lập, phòng sạch hoặc khi mất kết nối mạng.")
            ]
        },
        {
            "icon": "💾",
            "title": "2. BỘ NHỚ SPI FLASH NVM",
            "subtitle": "Lưu trữ bất biến & Thực thi tại chỗ",
            "border_color": C_GREEN,
            "badge_bg": RGBColor(240, 253, 244),
            "points": [
                ("Lưu trữ bất biến không cần pin:", "Bảo toàn 4,096 thẻ Whitelist (Sector 48) và 512 bản ghi Access Logs (Sector 49) trên 20 năm."),
                ("Thực thi tại chỗ XIP (eXecute-In-Place):", "CPU kéo trực tiếp opcode từ Flash ngoài 4MB để chạy, chỉ cần 1KB SRAM, tiết kiệm > 70% diện tích ASIC."),
                ("Tiết kiệm chân pad ngoại vi:", "Chuẩn SPI chỉ dùng 4 chân (CS, SCK, MOSI, MISO), tối ưu hóa số chân pad (chỉ 31 chân) và chi phí đóng gói."),
                ("Cập nhật In-RAM linh hoạt:", "Nạp worker vào SRAM để xóa/ghi Flash an toàn mà không làm nghẽn bus XIP của CPU.")
            ]
        },
        {
            "icon": "🛡️",
            "title": "3. TỰ CHỦ VI MẠCH ASIC",
            "subtitle": "Làm chủ 100% RTL & Ký duyệt Sign-off",
            "border_color": C_PURPLE,
            "badge_bg": RGBColor(250, 245, 255),
            "points": [
                ("Triệt tiêu Backdoor phần cứng:", "Làm chủ hoàn toàn từ mã nguồn RTL Verilog (CPU RV32I, bus interconnect, FIFO) đến layout GDSII."),
                ("Khối UART chuyên biệt cho RFID:", "Tích hợp bộ đệm FIFO 32B và khối oversampling 16x lấy mẫu đa số, chống rớt mã thẻ."),
                ("Ký duyệt Tape-out SkyWater 130nm:", "Luồng OpenLane 2 đạt 100% tiêu chuẩn xuất xưởng: 0 Antenna, 0 LVS, 0 DRC violations."),
                ("Hiệu năng cao & Tiết kiệm năng lượng:", "Đạt tần số Fmax = 92.81 MHz (vượt 85% mục tiêu), công suất chỉ 76 mW, độ sụt áp < 0.08% VDD.")
            ]
        }
    ]

    for idx, col in enumerate(cols_data):
        cx = start_x + idx * (col_w + col_gap)
        add_card(s3, cx, col_y, col_w, col_h, bg_color=C_WHITE, border_color=col["border_color"], border_width=1.5)

        banner = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx + Inches(0.12), col_y + Inches(0.12), col_w - Inches(0.24), Inches(1.02))
        try:
            banner.adjustments[0] = 0.05
        except Exception:
            pass
        banner.fill.solid()
        banner.fill.fore_color.rgb = col["badge_bg"]
        banner.line.color.rgb = col["border_color"]
        banner.line.width = Pt(1.2)

        tb_h = s3.shapes.add_textbox(cx + Inches(0.16), col_y + Inches(0.16), col_w - Inches(0.32), Inches(0.92))
        tf_h = tb_h.text_frame
        tf_h.word_wrap = True
        tf_h.margin_left = tf_h.margin_top = tf_h.margin_right = tf_h.margin_bottom = 0

        p_ht = tf_h.paragraphs[0]
        p_ht.text = f"{col['icon']}  {col['title']}"
        p_ht.font.name = "Segoe UI"
        p_ht.font.size = Pt(13.5)
        p_ht.font.bold = True
        p_ht.font.color.rgb = col["border_color"]
        p_ht.alignment = PP_ALIGN.CENTER
        p_ht.space_after = Pt(3)

        p_hs = tf_h.add_paragraph()
        p_hs.text = col["subtitle"]
        p_hs.font.name = "Segoe UI"
        p_hs.font.size = Pt(11.0)
        p_hs.font.italic = True
        p_hs.font.color.rgb = C_TEXT_MUTED
        p_hs.alignment = PP_ALIGN.CENTER

        tb_body = s3.shapes.add_textbox(cx + Inches(0.18), col_y + Inches(1.26), col_w - Inches(0.36), col_h - Inches(1.38))
        tf_body = tb_body.text_frame
        tf_body.word_wrap = True
        tf_body.margin_left = tf_body.margin_top = tf_body.margin_right = tf_body.margin_bottom = 0

        for p_idx, (b_lbl, b_val) in enumerate(col["points"]):
            p = tf_body.paragraphs[0] if p_idx == 0 else tf_body.add_paragraph()
            p.space_after = Pt(10)
            p.line_spacing = 1.25

            r_lbl = p.add_run()
            r_lbl.text = f"• {b_lbl} "
            r_lbl.font.name = "Segoe UI"
            r_lbl.font.size = Pt(12.0)
            r_lbl.font.bold = True
            r_lbl.font.color.rgb = C_TEXT_DARK

            r_val = p.add_run()
            r_val.text = b_val
            r_val.font.name = "Segoe UI"
            r_val.font.size = Pt(11.5)
            r_val.font.color.rgb = C_TEXT_MUTED





    # =========================================================================
    # SLIDE 3: PHẦN 3 - SƠ ĐỒ KHỐI TỔNG THỂ SOC (BLOCK DIAGRAM B&W DRAW.IO)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Phần 3: Kiến Trúc Vi Hệ Thống SoC",
               "Sơ Đồ Khối Kiến Trúc Vi Hệ Thống SoC PicoRV32 (4MB Flash, 1KB SRAM, 32 Fifo)", 3, total_slides=TOTAL_SLIDES)

    if os.path.exists(img_fig1):
        card_x = Inches(0.8)
        card_y = Inches(1.25)
        card_w = Inches(11.733)
        card_h = Inches(5.68)
        add_card(s6, card_x, card_y, card_w, card_h, bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)

        # Giữ nguyên tỷ lệ chuẩn của hình fig1_block_diagram.png (3053x1753 -> ~1.7416)
        img_h = Inches(5.52)
        img_w = Inches(5.52 * (3053 / 1753))  # ~9.613 inches
        img_x = card_x + (card_w - img_w) / 2
        img_y = card_y + (card_h - img_h) / 2
        s6.shapes.add_picture(img_fig1, img_x, img_y, img_w, img_h)

    # =========================================================================

    # =========================================================================
    # SLIDE 04: PHẦN 3 - BẢNG TRA CỨU ĐỊA CHỈ MEMORY MAP (C & RTL)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Phần 3: Kiến Trúc Vi Hệ Thống SoC",
               "Bảng Tra Cứu Địa Chỉ (Memory Map) & Khai Báo Biến Trong C / RTL", 4, total_slides=TOTAL_SLIDES)

    t_card = add_card(s4, Inches(0.8), Inches(1.30), Inches(11.733), Inches(5.60), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)

    rows, cols = 7, 3
    t_left = Inches(0.95)
    t_top = Inches(1.42)
    t_width = Inches(11.433)
    t_height = Inches(5.35)

    table_shape = s4.shapes.add_table(rows, cols, t_left, t_top, t_width, t_height)
    table = table_shape.table

    table.columns[0].width = Inches(2.25)
    table.columns[1].width = Inches(3.20)
    table.columns[2].width = Inches(5.983)

    headers = [
        "ĐỊA CHỈ VÙNG NHỚ (MMIO / ADDRESS)",
        "NƠI KHAI BÁO C & GIAO DIỆN RTL",
        "Ý NGHĨA SỬ DỤNG VỚI FIRMWARE C (CÁCH DÙNG ➔ TÁC DÙNG)"
    ]

    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY_DARK
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.margin_left = cell.margin_right = Inches(0.08)
        cell.margin_top = cell.margin_bottom = Inches(0.05)
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.name = "Segoe UI"
        p.font.size = Pt(12.0)
        p.font.bold = True
        p.font.color.rgb = C_CYAN_ACCENT
        p.alignment = PP_ALIGN.CENTER

    table_rows_data = [
        (
            "0x1000_0000\n0x1000_0004",
            "• C: REG_RFID_UART_DAT / DIV\n• RTL: uart_mmio.v (u_rfid_uart)",
            [
                ("👉 Cách dùng:", "Polling non-blocking thanh ghi DAT."),
                ("🎯 Tác dụng:", "Nhận 14 byte chuỗi RFID 125kHz không treo CPU.")
            ]
        ),
        (
            "0x3000_0000\n0x3000_0004",
            "• C: REG_PC_UART_DAT / DIV\n• RTL: uart_mmio.v (u_pc_uart)",
            [
                ("👉 Cách dùng:", "Gọi hàm putchar_pc() / getchar_pc()."),
                ("🎯 Tác dụng:", "Giao tiếp Host CLI 9600 bps quản trị SoC.")
            ]
        ),
        (
            "0x4000_0000",
            "• C: REG_GPIO_LEDS (0x40000000)\n• RTL: soc_gpio_mmio.v",
            [
                ("👉 Cách dùng:", "Ghi bitmask 16-bit điều khiển I/O."),
                ("🎯 Tác dụng:", "Báo LED xác thực và đóng/ngắt Relay mở cửa.")
            ]
        ),
        (
            "0x0030_0000\n(Sector 48)",
            "• C: USER_FLASH_ADDR (0x00300000)\n• NVM: SPI Flash Sector 48",
            [
                ("👉 Cách dùng:", "Nạp buffer thẻ ghi vào SPI Flash."),
                ("🎯 Tác dụng:", "Lưu cố định danh sách Whitelist khi mất nguồn.")
            ]
        ),
        (
            "0x0031_0000\n(Sector 49)",
            "• C: LOG_FLASH_ADDR (0x00310000)\n• NVM: SPI Flash Sector 49",
            [
                ("👉 Cách dùng:", "Ghi nối tiếp bản ghi AccessLog_t."),
                ("🎯 Tác dụng:", "Lưu vết lịch sử quét thẻ an ninh chống ghi đè.")
            ]
        ),
        (
            "0x0200_0000\n(1KB SRAM)",
            "• LDS: sections.lds (ORIGIN 0x02000000)\n• RTL: data_sram.v (1KB SPRAM)",
            [
                ("👉 Cách dùng:", "Chứa Stack, .data và nạp flashio_worker."),
                ("🎯 Tác dụng:", "CPU chạy trong RAM khi Flash bận xóa/ghi.")
            ]
        )
    ]

    for row_idx, (addr_txt, decl_txt, use_bullets) in enumerate(table_rows_data, start=1):
        bg_col = RGBColor(255, 255, 255) if row_idx % 2 == 1 else RGBColor(248, 250, 252)

        # Col 0: Address
        cell0 = table.cell(row_idx, 0)
        cell0.fill.solid()
        cell0.fill.fore_color.rgb = bg_col
        cell0.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell0.margin_left = cell0.margin_right = Inches(0.08)
        cell0.margin_top = cell0.margin_bottom = Inches(0.03)
        p0 = cell0.text_frame.paragraphs[0]
        p0.text = addr_txt
        p0.font.name = "Consolas"
        p0.font.size = Pt(12.0)
        p0.font.bold = True
        p0.font.color.rgb = C_BLUE_ACCENT
        p0.alignment = PP_ALIGN.CENTER

        # Col 1: Declaration in C & RTL
        cell1 = table.cell(row_idx, 1)
        cell1.fill.solid()
        cell1.fill.fore_color.rgb = bg_col
        cell1.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell1.margin_left = cell1.margin_right = Inches(0.08)
        cell1.margin_top = cell1.margin_bottom = Inches(0.03)
        p1 = cell1.text_frame.paragraphs[0]
        p1.text = decl_txt
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(10.8)
        p1.font.color.rgb = C_NAVY_DARK
        p1.line_spacing = 1.18

        # Col 2: Usage and Impact (👉 Cách dùng ➔ 🎯 Tác dụng)
        cell2 = table.cell(row_idx, 2)
        cell2.fill.solid()
        cell2.fill.fore_color.rgb = bg_col
        cell2.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell2.margin_left = cell2.margin_right = Inches(0.08)
        cell2.margin_top = cell2.margin_bottom = Inches(0.03)
        tf2 = cell2.text_frame
        tf2.word_wrap = True

        for b_idx, (b_label, b_desc) in enumerate(use_bullets):
            p2 = tf2.paragraphs[0] if b_idx == 0 else tf2.add_paragraph()
            p2.text = f"{b_label} {b_desc}"
            p2.font.name = "Segoe UI"
            p2.font.size = Pt(12.0)
            p2.font.color.rgb = C_TEXT_DARK
            p2.line_spacing = 1.16
            if b_idx == 0:
                p2.space_after = Pt(3.0)

    # =========================================================================
    # SLIDE 05: PHẦN 5 - DEMO THỰC NGHIỆM: CÁC KỊCH BẢN & GIAO DIỆN HOST CONSOLE
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Phần 5: Demo Chức Năng Sản Phẩm",
               "Các Kịch Bản Thực Nghiệm & Giao Diện Quản Trị Host Console", 5, total_slides=TOTAL_SLIDES)

    lx21 = Inches(0.8)
    lw21 = Inches(5.85)
    cli_lines = [
        "===============================================================",
        "     RDM6300 RFID - PICORV32 - BASYS 3 SPI FLASH MANAGER      ",
        "===============================================================",
        "  [1]  Ping Hardware (Kiem tra ket noi PicoRV32)",
        "  [2]  Input & Save New RFID Tag (Nhap 10 so in tren the luu Flash)",
        "  [3]  Check RFID Tag in Flash (Kiem tra the da co trong Flash)",
        "  [4]  Delete RFID Tag from Flash (Nhap 10 so de xoa khoi Flash)",
        "  [5]  Virtual Scan (Quet the ao: Nhap 10 so in tren the)",
        "  [6]  View Access Logs from Flash (Xem nhat ky Flash 0x310000)",
        "  [7]  Erase Access Logs (Sao luu CSV roi xoa nhat ky Flash)",
        "  [8]  Export RFID Tags to CSV (Xuat danh sach the ra file CSV)",
        "  [9]  Import RFID Tags from Latest CSV (Xoa Flash & Nap CSV)",
        "  [0]  Exit (Thoat)",
        "---------------------------------------------------------------",
        "Lua chon cua ban [0-9]: _"
    ]
    add_code_box(s5, lx21, Inches(1.30), lw21, Inches(5.60), "Menu Host Console CLI (host/main.c)", cli_lines, status_text="=== GIAO DIỆN QUẢN TRỊ TRÊN HOST PC GIAO TIẾP VỚI PICORV32 ===", font_size=10.5, line_spacing=1.55, title_color=RGBColor(52, 211, 153))

    rx21 = Inches(6.80)
    rw21 = Inches(5.73)
    add_card(s5, rx21, Inches(1.30), rw21, Inches(5.60), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
    tb_r21 = s5.shapes.add_textbox(rx21 + Inches(0.20), Inches(1.42), rw21 - Inches(0.40), Inches(5.35))
    tf_r21 = tb_r21.text_frame
    tf_r21.word_wrap = True

    pr21 = tf_r21.paragraphs[0]
    pr21.text = "ÁNH XẠ LỆNH HOST VÀO FIRMWARE C (MAIN.C)"
    pr21.font.name = "Segoe UI"
    pr21.font.size = Pt(14.0)
    pr21.font.bold = True
    pr21.font.color.rgb = C_BLUE_ACCENT
    pr21.space_after = Pt(8)

    fw_cases = [
        ("• [1] Ping Hardware ➔ case 'P':", "Phản hồi 'PONG: PicoRV32 Active', kiểm tra kết nối CPU & UART."),
        ("• [2] Save New Tag ➔ case 'N':", "Nạp 10 số in trên thẻ vào Flash Sector 48 (địa chỉ 0x0030_0000)."),
        ("• [3] Check Tag ➔ case 'C':", "Tra cứu xem mã thẻ đã tồn tại trong Whitelist SPI Flash hay chưa."),
        ("• [4] Delete Tag ➔ case 'K':", "Xóa duy nhất 1 thẻ chỉ định trong Flash bằng cách ghi đè Magic word."),
        ("• [5] Virtual Scan ➔ case 'V':", "Mô phỏng quẹt thẻ ảo từ terminal máy tính để kiểm tra xác thực."),
        ("• [6] View Logs ➔ case 'L':", "Đọc toàn bộ lịch sử quét thẻ từ Flash Sector 49 (địa chỉ 0x0031_0000)."),
        ("• [7] Erase Logs ➔ case 'X':", "Firmware xóa trắng Sector 49 (Host tự gửi 'L' sao lưu CSV trên PC trước)."),
        ("• [8] & [9] Quản lý CSV (Host PC):", "Host tự xử lý file CSV; gửi lệnh 'F' (đọc thẻ) hoặc 'E'+'N' (nạp thẻ) sang SoC.")
    ]

    for c_lbl, c_val in fw_cases:
        p = tf_r21.add_paragraph()
        p.text = f"{c_lbl} {c_val}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(12.0)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(6.5)
        p.line_spacing = 1.15

    # =========================================================================
    # SLIDE 06: PHẦN 3 - SƠ ĐỒ KHỐI KIẾN TRÚC VI MẠCH UART RTL & ĐẶC TẢ THIẾT KẾ
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Phần 3: Kiến Trúc Khối Ngoại Vi UART",
               "Sơ Đồ Khối Kiến Trúc Vi Mạch UART RTL (Draw.io Đen Trắng & Đặc Tả Thiết Kế)", 6, total_slides=TOTAL_SLIDES)

    if os.path.exists(img_uart_bw):
        add_card(s6, Inches(0.8), Inches(1.30), Inches(5.75), Inches(5.60), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
        s6.shapes.add_picture(img_uart_bw, Inches(0.95), Inches(1.45), Inches(5.45), Inches(5.30))

    rx8 = Inches(6.75)
    rw8 = Inches(5.78)
    add_card(s6, rx8, Inches(1.30), rw8, Inches(5.60), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
    tb_r8 = s6.shapes.add_textbox(rx8 + Inches(0.20), Inches(1.42), rw8 - Inches(0.40), Inches(5.35))
    tf_r8 = tb_r8.text_frame
    tf_r8.word_wrap = True

    p_r8_h = tf_r8.paragraphs[0]
    p_r8_h.text = "ĐẶC TẢ THIẾT KẾ 5 TẦNG PHẦN CỨNG UART RTL"
    p_r8_h.font.name = "Segoe UI"
    p_r8_h.font.bold = True
    p_r8_h.font.size = Pt(14.5)
    p_r8_h.font.color.rgb = C_BLUE_ACCENT
    p_r8_h.space_after = Pt(10)

    uart_stages_short = [
        ("TẦNG 1: ĐỒNG BỘ 2-FF CDC (sync_2ff.v)", C_ROSE,
         "• Khử siêu ổn định (Metastability) tín hiệu rx_i 125kHz; MTBF > 1.000 năm trên SkyWater 130nm."),
        ("TẦNG 2 & 3: TẠO BAUD & MÁY TRẠNG THÁI RX (simpleuart.v)", C_AMBER,
         "• Chia tần số cfg_divider = 5208 (9600 bps); Lấy mẫu 16x bầu đa số 3 mẫu & bắt khung 8-N-1."),
        ("TẦNG 4: HÀNG ĐỢI FIFO 32 BYTES ĐỘC LẬP (sync_fifo.v)", C_BLUE_ACCENT,
         "• Đệm trọn vẹn 14 byte chuỗi thẻ RFID, chống tràn dữ liệu tuyệt đối khi CPU bận ghi Flash."),
        ("TẦNG 5: GIẢI MÃ BUS MMIO NON-BLOCKING (uart_mmio.v)", C_GREEN,
         "• Ánh xạ 0x1000_0000 / 0x1000_0004; Phản hồi trong 1 chu kỳ 20ns, không bao giờ treo CPU.")
    ]

    for sec_title, sec_col, sec_desc in uart_stages_short:
        p_sec = tf_r8.add_paragraph()
        p_sec.text = sec_title
        p_sec.font.name = "Segoe UI"
        p_sec.font.size = Pt(12.5)
        p_sec.font.bold = True
        p_sec.font.color.rgb = sec_col
        p_sec.space_before = Pt(8)
        p_sec.space_after = Pt(2)

        p_b = tf_r8.add_paragraph()
        p_b.text = sec_desc
        p_b.font.name = "Segoe UI"
        p_b.font.size = Pt(12.0)
        p_b.font.color.rgb = C_TEXT_DARK
        p_b.space_after = Pt(6)
        p_b.line_spacing = 1.15

    # =========================================================================
    # SLIDE 07: PHẦN 4 - HỆ THỐNG TESTBENCH: UART RTL (TB_UART_RTL.V)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Phần 4: Hệ Thống Testbench & Mô Phỏng",
               "Testbench 1: Kiểm Thử Phần Cứng RTL Thuần Cho UART MMIO & FIFO (tb_uart_rtl.v)", 7, total_slides=TOTAL_SLIDES)

    # Khung Timeline Waveform chiếm phần lớn slide (Top / Center)
    add_card(s7, Inches(0.8), Inches(1.30), Inches(11.733), Inches(4.18), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)

    tb_lt = s7.shapes.add_textbox(Inches(0.95), Inches(1.36), Inches(11.433), Inches(0.26))
    tf_lt = tb_lt.text_frame
    tf_lt.margin_left = tf_lt.margin_top = tf_lt.margin_right = tf_lt.margin_bottom = 0
    p_lt = tf_lt.paragraphs[0]
    p_lt.text = "DẠNG SÓNG MÔ PHỎNG TIMELINE VIVADO XSIM (15.275 µs)"
    p_lt.alignment = PP_ALIGN.CENTER
    p_lt.font.name = "Segoe UI"
    p_lt.font.size = Pt(12.0)
    p_lt.font.bold = True
    p_lt.font.color.rgb = C_BLUE_ACCENT

    if os.path.exists(img_tb_uart_rtl):
        # Tăng kích thước ảnh timeline cực lớn để lấp đầy khung
        s7.shapes.add_picture(img_tb_uart_rtl, Inches(1.86), Inches(1.65), Inches(9.60), Inches(3.72))

    # Khung bên dưới: 5 Kịch bản kiểm thử viết rất ngắn gọn & Font chữ to rõ
    add_card(s7, Inches(0.8), Inches(5.58), Inches(8.30), Inches(1.32), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
    tb_sc = s7.shapes.add_textbox(Inches(0.95), Inches(5.64), Inches(8.00), Inches(1.20))
    tf_sc = tb_sc.text_frame
    tf_sc.word_wrap = True
    tf_sc.margin_left = tf_sc.margin_top = tf_sc.margin_right = tf_sc.margin_bottom = 0

    p_sc_h = tf_sc.paragraphs[0]
    p_sc_h.text = "5 KỊCH BẢN KIỂM THỬ RTL THUẦN (XÁC MINH PHẦN CỨNG 100% PASS):"
    p_sc_h.font.name = "Segoe UI"
    p_sc_h.font.size = Pt(11.0)
    p_sc_h.font.bold = True
    p_sc_h.font.color.rgb = C_BLUE_ACCENT
    p_sc_h.space_after = Pt(2)

    short_scenarios = [
        "1. Divider Mặc Định: Prescaler nạp đúng TEST_DIV = 16 ➔ PASS",
        "2. Tái Cấu Hình: Ghi giá trị chia tần mới qua MMIO tức thì ➔ PASS",
        "3. Phát Khung TX: Ký tự 0x4B ('K') xuất chuẩn UART 8-N-1 ➔ PASS",
        "4. Nhận Khung RX: Bắt chuỗi xung rx_i, nạp sạch FIFO (read_val = 75) ➔ PASS",
        "5. Xả Tràn FIFO: Đệm liên tục nhiều byte, đọc cạn trả về 0xFFFFFFFF ➔ PASS"
    ]

    for sc in short_scenarios:
        p = tf_sc.add_paragraph()
        p.text = f"• {sc}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(1.2)
        p.line_spacing = 1.05

    # Huy hiệu kết quả thành công bên dưới góc phải
    add_card(s7, Inches(9.20), Inches(5.58), Inches(3.333), Inches(1.32), bg_color=RGBColor(236, 253, 245), border_color=C_GREEN, border_width=1.5)
    tb_b7 = s7.shapes.add_textbox(Inches(9.32), Inches(5.68), Inches(3.10), Inches(1.12))
    tf_b7 = tb_b7.text_frame
    tf_b7.word_wrap = True
    tf_b7.margin_left = tf_b7.margin_top = tf_b7.margin_right = tf_b7.margin_bottom = 0

    pb7_1 = tf_b7.paragraphs[0]
    pb7_1.text = "XÁC NHẬN VIVADO XSIM:"
    pb7_1.font.name = "Segoe UI"
    pb7_1.font.size = Pt(11.0)
    pb7_1.font.bold = True
    pb7_1.font.color.rgb = C_GREEN
    pb7_1.space_after = Pt(2)

    pb7_2 = tf_b7.add_paragraph()
    pb7_2.text = "100% PASS (5/5 TEST SCENARIOS)\nRUNTIME: 15.275 µs | SỐ LỖI: 0"
    pb7_2.font.name = "Segoe UI"
    pb7_2.font.size = Pt(10.5)
    pb7_2.font.bold = True
    pb7_2.font.color.rgb = RGBColor(6, 95, 70)
    pb7_2.line_spacing = 1.15

    # =========================================================================
    # SLIDE 08: PHẦN 4 - HỆ THỐNG TESTBENCH: TOP SOC BOOT & PING (TB_UART_PING.V)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Phần 4: Hệ Thống Testbench & Mô Phỏng",
               "Testbench 2: Kiểm Thử Tích Hợp Toàn Diện Top SoC Boot Flash & Ping (tb_uart_ping.v)", 8, total_slides=TOTAL_SLIDES)

    lx21 = Inches(0.8)
    lw21 = Inches(11.733)
    code_lines_ping = [
        "// === tb/tb_uart_ping.v: KỊCH BẢN KIỂM THỬ TÍCH HỢP TOÀN DIỆN TOP SOC ===",
        "initial begin",
        "    clk = 0; rst_n = 0; rdm6300_rx_i = 1; uart_rx_i = 1;",
        "    #200; rst_n = 1;                 // Giải phóng Reset ➔ CPU thức dậy & Boot Flash 0x250000",
        "    wait(ready_matched == 1'b1);     // Đợi CPU PicoRV32 thực thi xong Banner C",
        "    #100000; send_pc_byte(\"P\");      // Host PC gửi byte lệnh Ping ('P' = 0x50)",
        "    send_pc_byte(8'h0A);             // Gửi ký tự kết thúc dòng '\\n' (0x0A)",
        "    wait(pong_matched == 1'b1);      // Đợi CPU nhận diện và phản hồi chuỗi PONG",
        "    if (pong_matched && !cpu_trap)   $display(\"  [SUCCESS] PING-PONG TEST PASSED!\");",
        "end",
        "",
        "// === VIVADO SIMULATOR (XSIM) EXECUTION OUTPUT LOG ===",
        "[FLASH MODEL] Loaded 2048 words (8192 bytes) from firmware.hex",
        "[TB] System Reset released. PicoRV32 booting from 0x250000...",
        "[UART TX] ========================================================================",
        "[UART TX]            RDM6300 PICORV32 SOC ACCESS CONTROLLER READY                 ",
        "[UART TX] ========================================================================",
        "[TB] Boot banner detected! Sending 'P' (Ping) command to SoC...",
        "[HOST -> SOC] Sent Byte: 'P' (0x50), '\\n' (0x0A)",
        "[UART TX] PONG: PicoRV32 Active",
        "[SUCCESS] PING-PONG TEST PASSED! PicoRV32 responded with PONG.",
        "cpu_trap = 0 (CPU healthy, no illegal instructions, no stack overflow)"
    ]
    add_code_box(s8, lx21, Inches(1.30), lw21, Inches(5.60), "tb/tb_uart_ping.v [Mã Nguồn Testbench & Nhật Ký Mô Phỏng Vivado XSim]", code_lines_ping, status_text="=== XÁC NHẬN: BOOT FLASH XIP + UART PING-PONG 100% PASS | RUNTIME: 2,086.555 µs | TRAP = 0 ===", font_size=11.5, line_spacing=1.0, title_color=RGBColor(52, 211, 153))

    # =========================================================================
    # SLIDE 09: PHẦN 5 - DEMO THỰC NGHIỆM TRÊN FPGA BASYS 3: DANH SÁCH THIẾT BỊ
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Phần 5: Demo Chức Năng Sản Phẩm",
               "Danh Sách Thiết Bị & Thiết Lập Kết Nối Phần Cứng FPGA Basys 3", 9, total_slides=TOTAL_SLIDES)

    # Khung bên trái: Hình ảnh hệ thống thực nghiệm
    add_card(s9, Inches(0.8), Inches(1.30), Inches(5.75), Inches(5.60), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)

    tb_lt9 = s9.shapes.add_textbox(Inches(0.95), Inches(1.42), Inches(5.45), Inches(0.32))
    tf_lt9 = tb_lt9.text_frame
    tf_lt9.margin_left = tf_lt9.margin_top = tf_lt9.margin_right = tf_lt9.margin_bottom = 0
    p_lt9 = tf_lt9.paragraphs[0]
    p_lt9.text = "HỆ THỐNG THỰC NGHIỆM THỰC TẾ"
    p_lt9.alignment = PP_ALIGN.CENTER
    p_lt9.font.name = "Segoe UI"
    p_lt9.font.size = Pt(13.0)
    p_lt9.font.bold = True
    p_lt9.font.color.rgb = C_BLUE_ACCENT

    if os.path.exists(img_device):
        # Tỷ lệ ảnh Device.jpg 1276 x 956 = 1.3347 -> rộng 5.45 inch, cao 4.08 inch
        s9.shapes.add_picture(img_device, Inches(0.95), Inches(1.85), Inches(5.45), Inches(4.08))

    tb_note9 = s9.shapes.add_textbox(Inches(0.95), Inches(6.05), Inches(5.45), Inches(0.75))
    tf_note9 = tb_note9.text_frame
    tf_note9.word_wrap = True
    tf_note9.margin_left = tf_note9.margin_top = tf_note9.margin_right = tf_note9.margin_bottom = 0
    p_note9 = tf_note9.paragraphs[0]
    p_note9.text = "Nguồn 5V riêng cho RDM6300 (chung GND) • Trở 1kΩ nối tiếp TX ➔ JA1 bảo vệ I/O 3.3V"
    p_note9.alignment = PP_ALIGN.CENTER
    p_note9.font.name = "Segoe UI"
    p_note9.font.size = Pt(11.0)
    p_note9.font.italic = True
    p_note9.font.color.rgb = C_TEXT_MUTED
    p_note9.line_spacing = 1.15

    # Khung bên phải: Chỉ liệt kê danh sách thiết bị
    rx9 = Inches(6.75)
    rw9 = Inches(5.78)
    add_card(s9, rx9, Inches(1.30), rw9, Inches(5.60), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
    tb_r9 = s9.shapes.add_textbox(rx9 + Inches(0.25), Inches(1.45), rw9 - Inches(0.50), Inches(5.35))
    tf_r9 = tb_r9.text_frame
    tf_r9.word_wrap = True
    tf_r9.margin_left = tf_r9.margin_top = tf_r9.margin_right = tf_r9.margin_bottom = 0

    p_r9_h = tf_r9.paragraphs[0]
    p_r9_h.text = "DANH SÁCH THIẾT BỊ THỰC NGHIỆM"
    p_r9_h.font.name = "Segoe UI"
    p_r9_h.font.bold = True
    p_r9_h.font.size = Pt(15.0)
    p_r9_h.font.color.rgb = C_BLUE_ACCENT
    p_r9_h.space_after = Pt(10)

    devices = [
        ("Bo mạch FPGA Digilent Basys 3", "Artix-7 XC7A35T, SPI Flash 32Mbit"),
        ("Module RFID RDM6300", "125 kHz, kèm ăng-ten cuộn dây"),
        ("Thẻ RFID EM4100", "Thẻ từ 125 kHz mẫu"),
        ("Module nguồn MB102 + Adapter DC", "Cấp 5V cho RDM6300"),
        ("Điện trở 1kΩ", "Nối tiếp chân TX RDM6300 ➔ JA1"),
        ("Breadboard & dây cắm", "Đấu nối mạch thử nghiệm"),
        ("Cáp Micro-USB", "Nạp FPGA & UART 9600 bps"),
        ("Máy tính Host PC", "Chạy chương trình Host Console")
    ]

    for d_idx, (d_name, d_spec) in enumerate(devices, start=1):
        p = tf_r9.add_paragraph()
        p.space_before = Pt(7)
        p.text = f"{d_idx}. {d_name}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(15.0)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK

        p_s = tf_r9.add_paragraph()
        p_s.text = f"     {d_spec}"
        p_s.font.name = "Segoe UI"
        p_s.font.size = Pt(12.5)
        p_s.font.color.rgb = C_TEXT_MUTED
    # SLIDE 9: PHẦN 6 - MINH CHỨNG KÝ DUYỆT SIGN-OFF, OPENROAD & CONFIG.JSON
    # =========================================================================
    s24 = prs.slides.add_slide(blank_layout)
    add_header(s24, "Phần 6: Thiết Kế Vật Lý ASIC",
               "Minh Chứng Ký Duyệt Sign-off, Bản Vẽ OpenROAD & Cấu Hình OpenLane", 10, total_slides=TOTAL_SLIDES)

    # Bố cục 2 tầng phân tách rõ ràng, giữ nguyên 100% tỷ lệ khung hình chuẩn (Aspect Ratio) không bị méo

    # TẦNG 1: Cấu hình config.json (Trái) & Bản vẽ Layout OpenROAD (Phải)
    top_y = Inches(1.30)
    top_h = Inches(3.60)

    # 1. Cột 1 (Trái): Cấu hình config.json (Box code Terminal)
    lx24_1 = Inches(0.8)
    lw24_1 = Inches(5.6)
    code_lines_24 = [
        '{',
        '  "DESIGN_NAME": "rdm6300_picorv32_soc",',
        '  "PDK": "sky130A",  "STD_CELL_LIBRARY": "sky130_fd_sc_hd",',
        '  "CLOCK_PERIOD": 20.0, // 50 MHz Clock',
        '  "FP_CORE_UTIL": 26,   // 26% Core Density',
        '  "MAX_FANOUT_CONSTRAINT": 12,',
        '  "PL_RESIZER_HOLD_SLACK_MARGIN": 0.6,',
        '  "RUN_HEURISTIC_DIODE_INSERTION": true,',
        '  "HEURISTIC_ANTENNA_THRESHOLD": 24,',
        '  "GRT_ANTENNA_ITERS": 35,',
        '  "RUN_ANTENNA_REPAIR": true,',
        '  "SYNTH_STRATEGY": "AREA 0"',
        '}'
    ]
    add_code_box(s24, lx24_1, top_y, lw24_1, top_h, "Cấu hình OpenLane (config.json)", code_lines_24, font_size=10.5, line_spacing=1.12)

    # 2. Cột 2 (Phải): Bản vẽ Layout OpenROAD (Giữ đúng tỷ lệ ảnh 1.38:1)
    rx24_2 = Inches(6.65)
    rw24_2 = Inches(5.883)
    add_card(s24, rx24_2, top_y, rw24_2, top_h, bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
    
    tb_c2_lbl = s24.shapes.add_textbox(rx24_2 + Inches(0.20), top_y + Inches(0.08), rw24_2 - Inches(0.40), Inches(0.30))
    tb_c2_lbl.text_frame.margin_left = tb_c2_lbl.text_frame.margin_top = 0
    p_c2 = tb_c2_lbl.text_frame.paragraphs[0]
    p_c2.text = "🖼️ Bản Vẽ Layout OpenROAD (Die 1.87 mm² - 1362 x 1373 µm)"
    p_c2.font.name = "Segoe UI"
    p_c2.font.size = Pt(11.0)
    p_c2.font.bold = True
    p_c2.font.color.rgb = C_BLUE_ACCENT

    if os.path.exists(img_openroad):
        # Kích thước chuẩn: width = 4.25 in, height = 3.08 in (Aspect ratio ~1.38:1)
        s24.shapes.add_picture(img_openroad, rx24_2 + Inches(0.82), top_y + Inches(0.42), Inches(4.25), Inches(3.08))

    # TẦNG 2: Báo cáo Ký duyệt Sign-off (Terminal Pass) & Badge Tổng kết
    bot_y = Inches(5.05)
    bot_h = Inches(1.85)
    add_card(s24, Inches(0.8), bot_y, Inches(11.733), bot_h, bg_color=C_WHITE, border_color=C_GREEN, border_width=2.0)

    # Ảnh Terminal Sign-off Pass (Giữ đúng tỷ lệ gốc 4.31:1 không bị nén méo)
    if os.path.exists(img_signoff):
        # Kích thước chuẩn: width = 6.90 in, height = 1.60 in (Aspect ratio ~4.31:1)
        s24.shapes.add_picture(img_signoff, Inches(0.95), bot_y + Inches(0.12), Inches(6.90), Inches(1.60))

    # Khung tóm tắt ký duyệt bên phải ảnh
    tb_sign_sum = s24.shapes.add_textbox(Inches(8.05), bot_y + Inches(0.10), Inches(4.35), Inches(1.65))
    tf_sign_sum = tb_sign_sum.text_frame
    tf_sign_sum.word_wrap = True
    tf_sign_sum.margin_left = tf_sign_sum.margin_top = tf_sign_sum.margin_right = tf_sign_sum.margin_bottom = 0

    p_ss_h = tf_sign_sum.paragraphs[0]
    p_ss_h.text = "✅ KÝ DUYỆT TAPE-OUT READY (100% PASS)"
    p_ss_h.font.name = "Segoe UI"
    p_ss_h.font.size = Pt(12.0)
    p_ss_h.font.bold = True
    p_ss_h.font.color.rgb = C_GREEN
    p_ss_h.space_after = Pt(4)

    ss_items = [
        ("Antenna Sign-off:", "0 vi phạm (3,471 diodes xả tĩnh điện bảo vệ oxit cổng)"),
        ("LVS Sign-off (Netgen):", "0 lỗi (Netlists match uniquely 100%, 0 unmatched)"),
        ("DRC Sign-off (Magic/KLayout):", "0 lỗi (Zero DRC violations trên toàn bộ 5 lớp kim loại)"),
        ("PDN & Timing:", "Worst IR Drop: 1.39 mV (< 0.08% VDD) | WNS = 0.00 ns")
    ]
    for lbl, val in ss_items:
        p_item = tf_sign_sum.add_paragraph()
        p_item.text = f"• {lbl} {val}"
        p_item.font.name = "Segoe UI"
        p_item.font.size = Pt(9.8)
        p_item.font.color.rgb = C_TEXT_DARK
        p_item.space_after = Pt(1.5)
        p_item.line_spacing = 1.10

    # =========================================================================
    # SLIDE 10: PHẦN 6 - BẢNG TỔNG HỢP KẾT QUẢ VẬT LÝ & THỐNG KÊ PPA METRICS
    # =========================================================================
    s25 = prs.slides.add_slide(blank_layout)
    add_header(s25, "Phần 6: Thiết Kế Vật Lý ASIC",
               "Tổng Hợp Kết Quả Thiết Kế Vật Lý & Chỉ Số PPA (OpenLane 2 / SkyWater 130nm)", 11, total_slides=TOTAL_SLIDES)

    # Tạo bảng kích thước lớn, font chữ to rõ ràng
    tbl_x = Inches(0.8)
    tbl_y = Inches(1.30)
    tbl_w = Inches(11.733)
    tbl_h = Inches(5.50)

    ppa_table_data = [
        ("Tiến trình & Điện áp hoạt động", "SkyWater 130nm (sky130_fd_sc_hd) | VDD = 1.80 V | Xung nhịp: 50.0 MHz", "Thư viện High Density, VDD chuẩn 1.8V"),
        ("Kích thước & Diện tích khuôn (Die / Core)", "Die Area: 1.87 mm² (1362.08 x 1372.80 µm) | Core: 1.82 mm² (52.84% Util)", "Chuẩn đóng gói khung chân đế QFN/QFP"),
        ("Quy mô linh kiện (Cell Breakdown)", "Tổng 164,478 cells (10,779 D-FF | 23,442 Comb | 77,243 Diode bảo vệ)", "24,247 timing buffer + 2,564 CTS buffer/inv"),
        ("Tổng công suất tiêu thụ (Power Analysis)", "Tổng: 76.02 mW (Internal: 41.12 mW, Switching: 34.90 mW) | Rò rỉ: 1.18 µW", "Dòng rò tĩnh siêu thấp (Static Leakage ~0%)"),
        ("Độ sụt áp nguồn (Worst-case IR Drop)", "Worst IR Drop: 1.39 mV (0.00139 V, sụt áp < 0.08% VDD | Avg: 0.085 mV)", "Lưới nguồn PDN met4/met5 an toàn tuyệt đối"),
        ("Định tuyến & Dây nối (Interconnect)", "60,225 Nets | 575,767 Vias | Tổng chiều dài dây dẫn kim loại: 3.215 mét", "Định tuyến 5 lớp kim loại (met1 - met5)"),
        ("Phân tích định thời tĩnh (STA Timing)", "Chu kỳ 20.0 ns (50.0 MHz) | WNS = 0.00 ns | TNS = 0.00 ns (Setup & Hold)", "MET TIMING trên toàn bộ 9 góc đo (9 corners)"),
        ("Ký duyệt xuất xưởng (Sign-off Status)", "0 Antenna Violations | 0 LVS Errors (Netgen 100%) | 0 DRC Errors (Magic)", "ĐẠT CHUẨN XUẤT XƯỞNG (TAPE-OUT READY!)")
    ]

    rows_count = len(ppa_table_data) + 1
    cols_count = 3
    shape_tbl = s25.shapes.add_table(rows_count, cols_count, tbl_x, tbl_y, tbl_w, tbl_h)
    tbl25 = shape_tbl.table

    tbl25.columns[0].width = Inches(3.20)
    tbl25.columns[1].width = Inches(5.333)
    tbl25.columns[2].width = Inches(3.20)

    # Tiêu đề bảng
    headers_25 = ["Hạng Mục Đo Đạc Vật Lý", "Thông Số Trích Xuất Thực Tế (OpenLane Runs)", "Đánh Giá & Tiêu Chuẩn Sign-off"]
    for c_idx, h_text in enumerate(headers_25):
        c_cell = tbl25.cell(0, c_idx)
        c_cell.fill.solid()
        c_cell.fill.fore_color.rgb = C_BLUE_ACCENT
        c_cell.text = h_text
        for p in c_cell.text_frame.paragraphs:
            p.alignment = PP_ALIGN.CENTER
            p.font.name = "Segoe UI"
            p.font.size = Pt(12.5)
            p.font.bold = True
            p.font.color.rgb = C_WHITE

    # Dữ liệu bảng
    for r_idx, (col0, col1, col2) in enumerate(ppa_table_data):
        row_cells = [tbl25.cell(r_idx + 1, 0), tbl25.cell(r_idx + 1, 1), tbl25.cell(r_idx + 1, 2)]
        bg_col = RGBColor(241, 245, 249) if r_idx % 2 == 1 else C_WHITE
        if r_idx == len(ppa_table_data) - 1:
            bg_col = RGBColor(236, 253, 245) # Hàng Sign-off nổi bật xanh lá nhạt

        for c_idx, cell in enumerate(row_cells):
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_col

        row_cells[0].text = col0
        row_cells[1].text = col1
        row_cells[2].text = col2

        for c_idx, cell in enumerate(row_cells):
            for p in cell.text_frame.paragraphs:
                p.font.name = "Segoe UI"
                p.font.size = Pt(11.0)
                if c_idx == 0:
                    p.font.bold = True
                    p.font.color.rgb = C_TEXT_DARK
                    p.alignment = PP_ALIGN.LEFT
                elif c_idx == 1:
                    p.font.bold = (r_idx in [0, 1, 3, 4, 7])
                    p.font.color.rgb = C_BLUE_ACCENT if r_idx in [0, 1, 3, 4] else (C_GREEN if r_idx == 7 else C_TEXT_DARK)
                    p.alignment = PP_ALIGN.LEFT
                else:
                    p.font.color.rgb = C_GREEN if r_idx == 7 else C_TEXT_MUTED
                    p.font.bold = (r_idx == 7)
                    p.alignment = PP_ALIGN.LEFT

    # =========================================================================
    # SLIDE 11: PHẦN 6 - PHÂN TÍCH ĐỊNH THỜI TĨNH STA TỪ SUMMARY.RPT
    # =========================================================================
    s26 = prs.slides.add_slide(blank_layout)
    add_header(s26, "Phần 6: Thiết Kế Vật Lý ASIC",
               "Phân Tích Định Thời Tĩnh STA & Báo Cáo Multi-Corner Timing (summary.rpt)", 12, total_slides=TOTAL_SLIDES)

    # TẦNG 1: Bảng kết quả Multi-Corner Timing trích xuất từ 55-openroad-stapostpnr/summary.rpt
    tbl_sta_x = Inches(0.8)
    tbl_sta_y = Inches(1.30)
    tbl_sta_w = Inches(11.733)
    tbl_sta_h = Inches(3.20)

    sta_table_data = [
        ("nom_tt_025C_1v80 (Typical)", "+4.4194 ns (+6.5934 ns)", "+0.5418 ns (+0.5418 ns)", "0 Vio (TNS = 0.00)", "MET TIMING (Đạt chuẩn 50.0 MHz)"),
        ("nom_ff_n40C_1v95 (Fast-Fast)", "+5.5199 ns (+7.7276 ns)", "+0.1680 ns (+0.1680 ns)", "0 Vio (TNS = 0.00)", "MET TIMING (Biên độ Setup cực lớn)"),
        ("min_tt_025C_1v80 (Min Typical)", "+4.5720 ns (+6.6560 ns)", "+0.6874 ns (+0.6874 ns)", "0 Vio (TNS = 0.00)", "MET TIMING (Hold Margin tối ưu)"),
        ("min_ff_n40C_1v95 (Min Fast)", "+5.6454 ns (+7.7576 ns)", "+0.2879 ns (+0.2879 ns)", "0 Vio (TNS = 0.00)", "MET TIMING (Hoạt động ổn định)"),
        ("max_tt_025C_1v80 (Max Typical)", "+4.2744 ns (+6.5546 ns)", "+0.3169 ns (+0.3169 ns)", "0 Vio (TNS = 0.00)", "MET TIMING (Dư địa 4.27 ns)")
    ]

    sta_rows = len(sta_table_data) + 1
    sta_cols = 5
    shape_sta = s26.shapes.add_table(sta_rows, sta_cols, tbl_sta_x, tbl_sta_y, tbl_sta_w, tbl_sta_h)
    tbl_sta = shape_sta.table

    tbl_sta.columns[0].width = Inches(2.65)
    tbl_sta.columns[1].width = Inches(2.35)
    tbl_sta.columns[2].width = Inches(2.35)
    tbl_sta.columns[3].width = Inches(1.75)
    tbl_sta.columns[4].width = Inches(2.633)

    sta_headers = ["Góc Đo Công Nghệ (Corner)", "Setup Slack (Worst / Reg)", "Hold Slack (Worst / Reg)", "Vi Phạm (Vio)", "Đánh Giá Định Thời"]
    for c_idx, h_text in enumerate(sta_headers):
        c_cell = tbl_sta.cell(0, c_idx)
        c_cell.fill.solid()
        c_cell.fill.fore_color.rgb = C_BLUE_ACCENT
        c_cell.text = h_text
        for p in c_cell.text_frame.paragraphs:
            p.alignment = PP_ALIGN.CENTER
            p.font.name = "Segoe UI"
            p.font.size = Pt(11.5)
            p.font.bold = True
            p.font.color.rgb = C_WHITE

    for r_idx, row_vals in enumerate(sta_table_data):
        row_cells = [tbl_sta.cell(r_idx + 1, ci) for ci in range(5)]
        bg_col = RGBColor(241, 245, 249) if r_idx % 2 == 1 else C_WHITE

        for c_idx, cell in enumerate(row_cells):
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_col
            cell.text = row_vals[c_idx]
            for p in cell.text_frame.paragraphs:
                p.font.name = "Segoe UI"
                p.font.size = Pt(10.5)
                if c_idx == 0:
                    p.font.bold = True
                    p.font.color.rgb = C_TEXT_DARK
                    p.alignment = PP_ALIGN.LEFT
                elif c_idx in [1, 2]:
                    p.font.bold = True
                    p.font.color.rgb = C_BLUE_ACCENT
                    p.alignment = PP_ALIGN.CENTER
                elif c_idx == 3:
                    p.font.bold = True
                    p.font.color.rgb = C_GREEN
                    p.alignment = PP_ALIGN.CENTER
                else:
                    p.font.bold = True
                    p.font.color.rgb = C_GREEN
                    p.alignment = PP_ALIGN.LEFT

    # TẦNG 2: 2 Khung phân tích chuyên sâu (Clock.rpt & Chiến lược Timing Closure)
    bot_sta_y = Inches(4.70)
    bot_sta_h = Inches(2.20)
    card_sta_w = Inches(5.75)

    # Khung trái: Thông số clock.rpt
    add_card(s26, Inches(0.8), bot_sta_y, card_sta_w, bot_sta_h, bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
    tb_c_l = s26.shapes.add_textbox(Inches(0.95), bot_sta_y + Inches(0.08), card_sta_w - Inches(0.30), bot_sta_h - Inches(0.16))
    tf_c_l = tb_c_l.text_frame
    tf_c_l.word_wrap = True
    tf_c_l.margin_left = tf_c_l.margin_top = tf_c_l.margin_right = tf_c_l.margin_bottom = 0

    p_cl_h = tf_c_l.paragraphs[0]
    p_cl_h.text = "⏱️ ĐẶC TÍNH MẠNG XUNG NHỊP (CLOCK.RPT)"
    p_cl_h.font.name = "Segoe UI"
    p_cl_h.font.size = Pt(12.0)
    p_cl_h.font.bold = True
    p_cl_h.font.color.rgb = C_BLUE_ACCENT
    p_cl_h.space_after = Pt(3)

    clk_bullets = [
        ("Tần số thiết kế mục tiêu:", "50.0 MHz (Chu kỳ Tclk = 20.0 ns)."),
        ("Tần số cực đại khả thi (Fmax):", "92.81 MHz (Chu kỳ Tmin = 10.77 ns)."),
        ("Dư địa định thời (Timing Headroom):", "+85.6% (Hệ thống có thể boost lên 90MHz an toàn)."),
        ("Cây xung nhịp TritonCTS:", "2,564 Buffers/Inverters | Latency: 2.35 - 3.72 ns | Skew: 1.36 ns.")
    ]
    for lbl, val in clk_bullets:
        p = tf_c_l.add_paragraph()
        p.text = f"• {lbl} {val}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(1.5)
        p.line_spacing = 1.10

    # Khung phải: Chiến lược Timing Closure
    add_card(s26, Inches(6.783), bot_sta_y, card_sta_w, bot_sta_h, bg_color=C_WHITE, border_color=C_GREEN, border_width=1.5)
    tb_c_r = s26.shapes.add_textbox(Inches(6.933), bot_sta_y + Inches(0.08), card_sta_w - Inches(0.30), bot_sta_h - Inches(0.16))
    tf_c_r = tb_c_r.text_frame
    tf_c_r.word_wrap = True
    tf_c_r.margin_left = tf_c_r.margin_top = tf_c_r.margin_right = tf_c_r.margin_bottom = 0

    p_cr_h = tf_c_r.paragraphs[0]
    p_cr_h.text = "🛡️ CHIẾN LƯỢC TỐI ƯU HÓA ĐỊNH THỜI (TIMING CLOSURE)"
    p_cr_h.font.name = "Segoe UI"
    p_cr_h.font.size = Pt(12.0)
    p_cr_h.font.bold = True
    p_cr_h.font.color.rgb = C_GREEN
    p_cr_h.space_after = Pt(3)

    opt_bullets = [
        ("Sửa lỗi Hold Time triệt để:", "Chèn 21,947 Hold Buffers (dlygate4sd3), triệt tiêu 100% lỗi Hold."),
        ("Kiểm soát Max Slew / Max Cap:", "Bố trí 2,300+ buffer resizer cân bằng tải dung và độ dốc sườn xung."),
        ("Đường truyền tới hạn (Critical Path):", "FF _52233_ -> flash_io2_do: Arrival 13.33 ns < Required 17.75 ns."),
        ("Kết luận Ký duyệt STA:", "Hội tụ định thời hoàn hảo (Timing Closed), đạt chuẩn sản xuất 130nm.")
    ]
    for lbl, val in opt_bullets:
        p = tf_c_r.add_paragraph()
        p.text = f"• {lbl} {val}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(1.5)
        p.line_spacing = 1.10

    # =========================================================================
    # SLIDE 12: TỔNG KẾT ĐỀ TÀI & HƯỚNG PHÁT TRIỂN (THANK YOU SLIDE)
    # =========================================================================
    s27 = prs.slides.add_slide(blank_layout)
    bg24 = s27.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg24.fill.solid()
    bg24.fill.fore_color.rgb = C_NAVY_DARK
    bg24.line.fill.background()

    card27 = s27.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
    card27.fill.solid()
    card27.fill.fore_color.rgb = C_NAVY_MID
    card27.line.color.rgb = C_BLUE_ACCENT
    card27.line.width = Pt(2.0)

    tb_t24 = s27.shapes.add_textbox(Inches(1.2), Inches(1.1), Inches(10.9), Inches(5.3))
    tf_t24 = tb_t24.text_frame
    tf_t24.word_wrap = True

    p_end1 = tf_t24.paragraphs[0]
    p_end1.text = "TỔNG KẾT ĐỒ ÁN & KẾT QUẢ ĐẠT ĐƯỢC"
    p_end1.font.name = "Segoe UI"
    p_end1.font.size = Pt(28)
    p_end1.font.bold = True
    p_end1.font.color.rgb = C_CYAN_ACCENT
    p_end1.space_after = Pt(26)

    contributions = [
        ("1. Tự chủ kiến trúc SoC:", " Tích hợp CPU RISC-V PicoRV32, cầu bus 0-delay, 1KB SRAM & 2 khối UART FIFO 32B."),
        ("2. Tối ưu thực thi nhúng:", " Chạy lệnh XIP từ SPI Flash; Nạp worker vào SRAM ghi/xóa Flash không nghẽn bus."),
        ("3. Kiểm chứng thực tế 100%:", " Testbench Vivado 100% Pass; Chạy ổn định trên bo mạch FPGA Basys 3 thật."),
        ("4. Đạt chuẩn ASIC Tape-out:", " OpenLane 2 (SkyWater 130nm) đạt 0 Antenna, 0 LVS, 0 DRC | Fmax = 92.81 MHz.")
    ]

    for c_title, c_desc in contributions:
        p = tf_t24.add_paragraph()
        p.space_after = Pt(20)
        p.line_spacing = 1.25

        run_title = p.add_run()
        run_title.text = c_title
        run_title.font.name = "Segoe UI"
        run_title.font.size = Pt(17.5)
        run_title.font.bold = True
        run_title.font.color.rgb = RGBColor(56, 189, 248) # Sky blue accent

        run_desc = p.add_run()
        run_desc.text = c_desc
        run_desc.font.name = "Segoe UI"
        run_desc.font.size = Pt(16.5)
        run_desc.font.color.rgb = RGBColor(241, 245, 249) # Bright white/slate

    p_git = tf_t24.add_paragraph()
    p_git.text = "🔗 GitHub Repository: https://github.com/thaituanhiep/uart-fifo-rfid-asic/tree/rfid_flash_firmware_optimize"
    p_git.font.name = "Segoe UI"
    p_git.font.size = Pt(14)
    p_git.font.color.rgb = RGBColor(147, 197, 253)
    p_git.space_before = Pt(14)

    p_ty = tf_t24.add_paragraph()
    p_ty.text = "XIN TRÂN TRỌNG CẢM ƠN QUÝ THẦY CÔ ĐÃ LẮNG NGHE!"
    p_ty.font.name = "Segoe UI"
    p_ty.font.size = Pt(22)
    p_ty.font.bold = True
    p_ty.font.color.rgb = C_WHITE
    p_ty.space_before = Pt(18)

    # -------------------------------------------------------------
    # LƯU FILE VÀ COPY (CHỈ 1 BẢN CHÍNH THỨC DUY NHẤT)
    # -------------------------------------------------------------
    out_path = os.path.join(cur_dir, "Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.pptx")
    prs.save(out_path)
    print(f"Presentation generated successfully: {out_path} ({os.path.getsize(out_path)} bytes)")

    doc_out = os.path.join(doc_dir, "Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.pptx")
    try:
        shutil.copy2(out_path, doc_out)
        print(f"Copied presentation to document root: {doc_out}")
    except Exception as e:
        print(f"Notice: {doc_out} is locked: {e}")

if __name__ == "__main__":
    create_deck()
