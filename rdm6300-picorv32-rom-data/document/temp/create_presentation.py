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

    TOTAL_SLIDES = 12

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
        p_t.font.size = Pt(9.5)
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
            p_s.font.size = Pt(8.2)
            p_s.font.bold = True
            p_s.font.color.rgb = C_GREEN

    # =========================================================================
    # SLIDE 1: TRANG BÌA (Title Slide)
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

    tb1 = s1.shapes.add_textbox(Inches(0.95), Inches(1.05), Inches(11.45), Inches(5.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = Inches(0.05)

    p_org = tf1.paragraphs[0]
    p_org.text = "FPT JETKING — CHIP DESIGN"
    p_org.font.name = "Segoe UI"
    p_org.font.size = Pt(13.5)
    p_org.font.bold = True
    p_org.font.color.rgb = C_CYAN_ACCENT
    p_org.space_after = Pt(16)

    p_main = tf1.add_paragraph()
    p_main.text = "THIẾT KẾ HỆ THỐNG XỬ LÝ DỮ LIỆU CỦA THẺ RA VÀO RFID 125KHZ OFFLINE\nTÍCH HỢP CPU RISC-V PICORV32 & XỬ LÝ NGHIỆP VỤ DỮ LIỆU THẺ BẰNG FIRMWARE C"
    p_main.font.name = "Segoe UI"
    p_main.font.size = Pt(17.5)
    p_main.font.bold = True
    p_main.font.color.rgb = C_WHITE
    p_main.space_after = Pt(16)
    p_main.line_spacing = 1.25

    p_sub = tf1.add_paragraph()
    p_sub.text = "Giao tiếp RFID RDM6300 | Lưu trữ Whitelist SPI Flash NVM | Tạo mẫu Basys 3 FPGA | Ký duyệt ASIC OpenLane 2 (Sky130)"
    p_sub.font.name = "Segoe UI"
    p_sub.font.size = Pt(12)
    p_sub.font.color.rgb = RGBColor(203, 213, 225)
    p_sub.space_after = Pt(24)

    p_info1 = tf1.add_paragraph()
    p_info1.text = "Học viên thực hiện :  Thái Tuấn Hiệp"
    p_info1.font.name = "Segoe UI"
    p_info1.font.size = Pt(13)
    p_info1.font.bold = True
    p_info1.font.color.rgb = C_WHITE
    p_info1.space_after = Pt(6)

    p_info2 = tf1.add_paragraph()
    p_info2.text = "Giảng viên hướng dẫn :  ThS. Nguyễn Văn Đông"
    p_info2.font.name = "Segoe UI"
    p_info2.font.size = Pt(12.5)
    p_info2.font.color.rgb = RGBColor(226, 232, 240)
    p_info2.space_after = Pt(6)

    p_info3 = tf1.add_paragraph()
    p_info3.text = "Học kỳ :  SEM3  |  Chuyên ngành: Thiết kế Vi mạch Bán dẫn (Chip Design)"
    p_info3.font.name = "Segoe UI"
    p_info3.font.size = Pt(11.5)
    p_info3.font.italic = True
    p_info3.font.color.rgb = RGBColor(148, 163, 184)

    # =========================================================================
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
        p_hs.font.size = Pt(10.0)
        p_hs.font.italic = True
        p_hs.font.color.rgb = C_TEXT_MUTED
        p_hs.alignment = PP_ALIGN.CENTER

        tb_body = s3.shapes.add_textbox(cx + Inches(0.18), col_y + Inches(1.26), col_w - Inches(0.36), col_h - Inches(1.38))
        tf_body = tb_body.text_frame
        tf_body.word_wrap = True
        tf_body.margin_left = tf_body.margin_top = tf_body.margin_right = tf_body.margin_bottom = 0

        for p_idx, (b_lbl, b_val) in enumerate(col["points"]):
            p = tf_body.paragraphs[0] if p_idx == 0 else tf_body.add_paragraph()
            p.space_after = Pt(16)
            p.line_spacing = 1.25

            r_lbl = p.add_run()
            r_lbl.text = f"• {b_lbl} "
            r_lbl.font.name = "Segoe UI"
            r_lbl.font.size = Pt(11.5)
            r_lbl.font.bold = True
            r_lbl.font.color.rgb = C_TEXT_DARK

            r_val = p.add_run()
            r_val.text = b_val
            r_val.font.name = "Segoe UI"
            r_val.font.size = Pt(10.5)
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
    # SLIDE 4: PHẦN 3 - SƠ ĐỒ KHỐI KIẾN TRÚC VI MẠCH UART RTL & ĐẶC TẢ THIẾT KẾ
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Phần 3: Kiến Trúc Khối Ngoại Vi UART",
               "Sơ Đồ Khối Kiến Trúc Vi Mạch UART RTL (Draw.io Đen Trắng & Đặc Tả Thiết Kế)", 4, total_slides=TOTAL_SLIDES)

    if os.path.exists(img_uart_bw):
        add_card(s8, Inches(0.8), Inches(1.30), Inches(5.75), Inches(5.50), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
        s8.shapes.add_picture(img_uart_bw, Inches(0.95), Inches(1.45), Inches(5.45), Inches(5.20))

    rx8 = Inches(6.75)
    rw8 = Inches(5.78)
    add_card(s8, rx8, Inches(1.30), rw8, Inches(5.50), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
    tb_r8 = s8.shapes.add_textbox(rx8 + Inches(0.20), Inches(1.45), rw8 - Inches(0.40), Inches(5.20))
    tf_r8 = tb_r8.text_frame
    tf_r8.word_wrap = True

    p_r8_h = tf_r8.paragraphs[0]
    p_r8_h.text = "ĐẶC TẢ THIẾT KẾ 5 TẦNG VI MẠCH NGOẠI VI UART RTL"
    p_r8_h.font.name = "Segoe UI"
    p_r8_h.font.bold = True
    p_r8_h.font.size = Pt(11.5)
    p_r8_h.font.color.rgb = C_BLUE_ACCENT
    p_r8_h.space_after = Pt(4)

    uart_stages_desc = [
        ("TẦNG 1: ĐỒNG BỘ HÓA MIỀN XUNG 2-FF CDC (sync_2ff.v)", C_ROSE, [
            ("Ngõ vào không đồng bộ rx_i:", "Tín hiệu nối tiếp từ đầu đọc RDM6300 125kHz hoặc chip USB FT2232 đi qua 2 tầng Flip-Flop."),
            ("Chống hiện tượng siêu ổn định:", "Bảo đảm thời gian trung bình giữa 2 lỗi MTBF > 1.000 năm trên tiến trình SkyWater 130nm.")
        ]),
        ("TẦNG 2 & 3: BỘ TẠO BAUD, LẤY MẪU 16X & RX FSM (simpleuart.v)", C_AMBER, [
            ("Chia tần số chuẩn xác:", "Thanh ghi cfg_divider = 5208 (50 MHz / 9600 bps) tạo chu kỳ định thời phần cứng chính xác 100%."),
            ("Bộ lấy mẫu 16x & Bầu đa số 3 mẫu:", "Lấy mẫu tại tick 7, 8, 9 ở giữa bit, triệt tiêu xung gai nhiễu glitch."),
            ("Máy trạng thái RX FSM:", "Tự động phát hiện Start bit (0), dịch 8-bit dữ liệu LSB-first và kiểm tra Stop bit (1).")
        ]),
        ("TẦNG 4: HÀNG ĐỢI FIFO 32 BYTES ĐỘC LẬP (sync_fifo.v)", C_BLUE_ACCENT, [
            ("Cơ chế đệm độc lập:", "Quản lý con trỏ ghi wr_ptr và đọc rd_ptr độc lập trên mảng nhớ 32x8-bit."),
            ("Bảo vệ chống tràn khi Flash bận:", "Đệm trọn vẹn 14 byte chuỗi thẻ RFID ngay cả khi CPU bận chạy flashio_worker ghi Flash.")
        ]),
        ("TẦNG 5: GIẢI MÃ BUS MMIO & NON-BLOCKING (uart_mmio.v)", C_GREEN, [
            ("Ánh xạ không gian địa chỉ:", "0x1000_0000 (Divider Prescaler) và 0x1000_0004 (RX FIFO Data)."),
            ("Giao tiếp Non-blocking 1 chu kỳ:", "Nếu FIFO rỗng, trả về ngay 0xFFFFFFFF trong 20 ns, không bao giờ làm treo bus CPU.")
        ])
    ]

    for sec_idx, (sec_title, sec_col, sec_bullets) in enumerate(uart_stages_desc):
        p_sec = tf_r8.add_paragraph()
        p_sec.text = sec_title
        p_sec.font.name = "Segoe UI"
        p_sec.font.size = Pt(8.6)
        p_sec.font.bold = True
        p_sec.font.color.rgb = sec_col
        p_sec.space_before = Pt(3)
        p_sec.space_after = Pt(1)

        for b_lbl, b_val in sec_bullets:
            p_b = tf_r8.add_paragraph()
            p_b.text = f"• {b_lbl} {b_val}"
            p_b.font.name = "Segoe UI"
            p_b.font.size = Pt(7.6)
            p_b.font.color.rgb = C_TEXT_DARK
            p_b.space_after = Pt(1.2)
            p_b.line_spacing = 1.10






    # =========================================================================
    # SLIDE 5: PHẦN 4 - HỆ THỐNG TESTBENCH: UART RTL (TB_UART_RTL.V)
    # =========================================================================
    s20 = prs.slides.add_slide(blank_layout)
    add_header(s20, "Phần 4: Hệ Thống Testbench & Mô Phỏng",
               "Testbench 1: Kiểm Thử Phần Cứng RTL Thuần Cho UART MMIO & FIFO (tb_uart_rtl.v)", 5, total_slides=TOTAL_SLIDES)

    # Khung bên trái: Hình ảnh waveform Vivado xsim
    card_l20 = add_card(s20, Inches(0.8), Inches(1.35), Inches(5.85), Inches(5.50), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)

    tb_lt20 = s20.shapes.add_textbox(Inches(0.95), Inches(1.48), Inches(5.55), Inches(0.28))
    tf_lt20 = tb_lt20.text_frame
    tf_lt20.margin_left = tf_lt20.margin_top = tf_lt20.margin_right = tf_lt20.margin_bottom = 0
    p_lt20 = tf_lt20.paragraphs[0]
    p_lt20.text = "DẠNG SÓNG MÔ PHỎNG VIVADO XSIM (15.275 µs)"
    p_lt20.alignment = PP_ALIGN.CENTER
    p_lt20.font.name = "Segoe UI"
    p_lt20.font.size = Pt(10.5)
    p_lt20.font.bold = True
    p_lt20.font.color.rgb = C_BLUE_ACCENT

    if os.path.exists(img_tb_uart_rtl):
        # Image aspect ratio 1024x608 = 1.684. Width 5.45" -> Height 3.24"
        s20.shapes.add_picture(img_tb_uart_rtl, Inches(1.00), Inches(1.78), Inches(5.45), Inches(3.24))

    # Ghi chú phân tích tín hiệu bên dưới waveform
    add_card(s20, Inches(1.00), Inches(5.12), Inches(5.45), Inches(1.58), bg_color=RGBColor(241, 245, 249), border_color=RGBColor(203, 213, 225), border_width=1.0)
    tb_lc20 = s20.shapes.add_textbox(Inches(1.12), Inches(5.18), Inches(5.20), Inches(1.46))
    tf_lc20 = tb_lc20.text_frame
    tf_lc20.word_wrap = True
    tf_lc20.margin_left = tf_lc20.margin_top = tf_lc20.margin_right = tf_lc20.margin_bottom = 0

    p_lc1 = tf_lc20.paragraphs[0]
    p_lc1.text = "ĐẶC TRƯNG TÍN HIỆU TRÊN DẠNG SÓNG (WAVEFORM ANALYSIS):"
    p_lc1.font.name = "Segoe UI"
    p_lc1.font.size = Pt(8.2)
    p_lc1.font.bold = True
    p_lc1.font.color.rgb = C_BLUE_ACCENT
    p_lc1.space_after = Pt(2)

    rtl_sig_notes = [
        "• clk / rst_n: Chu kỳ xung nhịp 10ns (100MHz), reset giải phóng tại t = 100ns.",
        "• tx_o (Serial TX): Khung truyền 8-N-1 (Start bit 0 -> 8 bit dữ liệu LSB -> Stop bit 1).",
        "• rx_activity_o & FIFO: Bắt chuỗi xung rx_i, nạp sạch vào FIFO và trả về read_val = 75.",
        "• err_count = 0: 5/5 kịch bản tự động Assert thành công, kết thúc an toàn tại 15.275 µs."
    ]
    for note in rtl_sig_notes:
        p = tf_lc20.add_paragraph()
        p.text = note
        p.font.name = "Segoe UI"
        p.font.size = Pt(7.6)
        p.font.color.rgb = C_TEXT_DARK
        p.line_spacing = 1.12

    # Khung bên phải: 5 kịch bản kiểm thử xác minh chi tiết
    card_r20 = add_card(s20, Inches(6.80), Inches(1.35), Inches(5.73), Inches(5.50), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
    tb_r20 = s20.shapes.add_textbox(Inches(7.00), Inches(1.48), Inches(5.33), Inches(4.35))
    tf_r20 = tb_r20.text_frame
    tf_r20.word_wrap = True
    tf_r20.margin_left = tf_r20.margin_top = tf_r20.margin_right = tf_r20.margin_bottom = 0

    pt20 = tf_r20.paragraphs[0]
    pt20.text = "5 KỊCH BẢN KIỂM THỬ UART RTL THUẦN (100% PASS)"
    pt20.font.name = "Segoe UI"
    pt20.font.size = Pt(12.0)
    pt20.font.bold = True
    pt20.font.color.rgb = C_BLUE_ACCENT
    pt20.space_after = Pt(8)

    tb_uart_scenarios = [
        ("Mục tiêu:", "Xác minh tính đúng đắn phần cứng của uart_mmio.v, sync_fifo.v và simpleuart.v mà không cần CPU."),
        ("1. Default Divider:", "Kiểm tra thanh ghi Prescaler tại offset 0x00 nạp đúng giá trị mặc định TEST_DIV = 16 -> PASS."),
        ("2. Divider Reconfig:", "Ghi giá trị chia tần mới và đọc lại qua bus MMIO, xác nhận mạch thanh ghi hoạt động chuẩn xác -> PASS."),
        ("3. Serial TX Frame:", "Ghi ký tự 0x4B ('K' / 75) vào wdata, kiểm tra dạng sóng nối tiếp tx_o đúng chuẩn 8-N-1 -> PASS."),
        ("4. Serial RX & FIFO:", "Bơm chuỗi bit vào rx_i, cờ rx_activity_o tích cực, dữ liệu nạp sạch vào FIFO và đọc ra read_val = 75 -> PASS."),
        ("5. Multi-Byte Burst:", "Bắn chuỗi byte kiểm tra cơ chế chống tràn của hàng đợi FIFO, đọc cạn trả về 0xFFFFFFFF (4294967295) -> PASS.")
    ]

    for p_lbl, p_val in tb_uart_scenarios:
        p = tf_r20.add_paragraph()
        p.text = f"• {p_lbl} {p_val}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.3)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(5)
        p.line_spacing = 1.15

    # Huy hiệu kết quả thành công bên dưới góc phải
    add_card(s20, Inches(7.00), Inches(5.98), Inches(5.33), Inches(0.72), bg_color=RGBColor(236, 253, 245), border_color=C_GREEN, border_width=1.5)
    tb_badge20 = s20.shapes.add_textbox(Inches(7.10), Inches(6.04), Inches(5.13), Inches(0.60))
    tf_b20 = tb_badge20.text_frame
    tf_b20.word_wrap = True
    tf_b20.margin_left = tf_b20.margin_top = tf_b20.margin_right = tf_b20.margin_bottom = 0
    pb20_1 = tf_b20.paragraphs[0]
    pb20_1.text = "XÁC NHẬN KẾT QUẢ MÔ PHỎNG VIVADO XSIM:"
    pb20_1.font.name = "Segoe UI"
    pb20_1.font.size = Pt(8.2)
    pb20_1.font.bold = True
    pb20_1.font.color.rgb = C_GREEN
    pb20_1.space_after = Pt(1)

    pb20_2 = tf_b20.add_paragraph()
    pb20_2.text = "100% PASS (5/5 TEST SCENARIOS) | RUNTIME: 15,275 ns | SỐ LỖI: 0"
    pb20_2.font.name = "Segoe UI"
    pb20_2.font.size = Pt(8.8)
    pb20_2.font.bold = True
    pb20_2.font.color.rgb = RGBColor(6, 95, 70)

    # =========================================================================
    # SLIDE 6: PHẦN 4 - HỆ THỐNG TESTBENCH: TOP SOC BOOT & PING (TB_UART_PING.V)
    # =========================================================================
    s21 = prs.slides.add_slide(blank_layout)
    add_header(s21, "Phần 4: Hệ Thống Testbench & Mô Phỏng",
               "Testbench 2: Kiểm Thử Tích Hợp Toàn Diện Top SoC Boot Flash & Ping (tb_uart_ping.v)", 6, total_slides=TOTAL_SLIDES)

    # Khung bên trái: Code Testbench chính & Log mô phỏng Vivado XSim
    lx21 = Inches(0.8)
    lw21 = Inches(5.85)
    code_lines_ping = [
        "// tb/tb_uart_ping.v - Kịch bản kiểm thử tích hợp Top SoC",
        "initial begin",
        "    clk = 0; rst_n = 0; rdm6300_rx_i = 1; uart_rx_i = 1;",
        "    #200; rst_n = 1; // Release Reset -> Boot Flash 0x250000",
        "    wait(ready_matched == 1'b1); // Đợi CPU phát xong Banner C",
        "    #100000; send_pc_byte(\"P\");  // PC Host gửi lệnh Ping",
        "    send_pc_byte(8'h0A);         // Gửi ký tự '\\n'",
        "    wait(pong_matched == 1'b1);  // Đợi CPU phản hồi chuỗi PONG",
        "    if (pong_matched && !cpu_trap)",
        "        $display(\"  [SUCCESS] PING-PONG TEST PASSED!\");",
        "end",
        "",
        "// === VIVADO SIMULATOR (XSIM) EXECUTION OUTPUT LOG ===",
        "[FLASH MODEL] Loaded 2048 words (8192 bytes) from firmware.hex",
        "[TB] System Reset released. PicoRV32 booting from 0x250000...",
        "[UART TX] ================================================",
        "[UART TX]   RDM6300 PICORV32 SOC ACCESS CONTROLLER READY  ",
        "[UART TX] ================================================",
        "[TB] Boot banner detected! Sending 'P' (Ping) command...",
        "[HOST -> SOC] Sent Byte: 'P' (0x50), '\\n' (0x0A)",
        "[UART TX] PONG: PicoRV32 Active",
        "[SUCCESS] PING-PONG TEST PASSED! PicoRV32 responded with PONG.",
        "cpu_trap = 0 (CPU healthy and executing normally)"
    ]
    add_code_box(s21, lx21, Inches(1.35), lw21, Inches(5.50), "tb/tb_uart_ping.v [Testbench Code & Sim Log]", code_lines_ping, status_text="=== BOOT FLASH XIP + UART PING-PONG: 100% PASS | RUNTIME: 2,086.555 µs ===", font_size=7.2, line_spacing=1.10, title_color=RGBColor(52, 211, 153))

    # Khung bên phải: 5 kịch bản tích hợp Top SoC chi tiết
    card_r21 = add_card(s21, Inches(6.80), Inches(1.35), Inches(5.73), Inches(5.50), bg_color=C_WHITE, border_color=C_GREEN, border_width=1.5)
    tb_r21 = s21.shapes.add_textbox(Inches(7.00), Inches(1.48), Inches(5.33), Inches(4.35))
    tf_r21 = tb_r21.text_frame
    tf_r21.word_wrap = True
    tf_r21.margin_left = tf_r21.margin_top = tf_r21.margin_right = tf_r21.margin_bottom = 0

    pt21 = tf_r21.paragraphs[0]
    pt21.text = "5 KỊCH BẢN KIỂM THỬ TÍCH HỢP TOP SOC (100% PASS)"
    pt21.font.name = "Segoe UI"
    pt21.font.size = Pt(12.0)
    pt21.font.bold = True
    pt21.font.color.rgb = C_GREEN
    pt21.space_after = Pt(8)

    tb_soc_scenarios = [
        ("Mục tiêu:", "Xác minh hệ thống Top-level hoàn chỉnh gồm CPU PicoRV32, spimemio, 1KB SRAM, Interconnect và UART."),
        ("1. Power-On Reset & Boot Flash:", "PicoRV32 thức dậy tại 0x0025_0000, spimemio kéo từng từ lệnh mã C từ firmware.hex qua XIP."),
        ("2. C Startup Banner Output:", "CPU thực thi mã C main.c, khởi tạo ngoại vi và in chuỗi chào mừng ra UART (ready_matched = 1)."),
        ("3. Host Ping Processing:", "Testbench đóng vai trò PC Host gửi byte lệnh 'P' (0x50) và '\\n' (0x0A) qua chân uart_rx."),
        ("4. Response Verification:", "CPU nhận dạng lệnh, phản hồi tức thì chuỗi 'PONG: PicoRV32 Active' (pong_matched = 1)."),
        ("5. CPU Health & Zero-Trap:", "Khẳng định tín hiệu trap == 0 xuyên suốt 2,086,555 ns, CPU không bị illegal instruction hay tràn RAM.")
    ]

    for p_lbl, p_val in tb_soc_scenarios:
        p = tf_r21.add_paragraph()
        p.text = f"• {p_lbl} {p_val}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.3)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(5)
        p.line_spacing = 1.15

    # Huy hiệu kết quả thành công bên dưới góc phải
    add_card(s21, Inches(7.00), Inches(5.98), Inches(5.33), Inches(0.72), bg_color=RGBColor(236, 253, 245), border_color=C_GREEN, border_width=1.5)
    tb_badge21 = s21.shapes.add_textbox(Inches(7.10), Inches(6.04), Inches(5.13), Inches(0.60))
    tf_b21 = tb_badge21.text_frame
    tf_b21.word_wrap = True
    tf_b21.margin_left = tf_b21.margin_top = tf_b21.margin_right = tf_b21.margin_bottom = 0
    pb21_1 = tf_b21.paragraphs[0]
    pb21_1.text = "XÁC NHẬN KẾT QUẢ MÔ PHỎNG VIVADO XSIM:"
    pb21_1.font.name = "Segoe UI"
    pb21_1.font.size = Pt(8.2)
    pb21_1.font.bold = True
    pb21_1.font.color.rgb = C_GREEN
    pb21_1.space_after = Pt(1)

    pb21_2 = tf_b21.add_paragraph()
    pb21_2.text = "100% PASS (BOOT XIP + PING-PONG) | RUNTIME: 2,086.555 µs | TRAP: 0"
    pb21_2.font.name = "Segoe UI"
    pb21_2.font.size = Pt(8.8)
    pb21_2.font.bold = True
    pb21_2.font.color.rgb = RGBColor(6, 95, 70)

    # =========================================================================
    # SLIDE 7: PHẦN 5 - DEMO THỰC NGHIỆM TRÊN FPGA BASYS 3: THIẾT LẬP KẾT NỐI
    # =========================================================================
    s22 = prs.slides.add_slide(blank_layout)
    add_header(s22, "Phần 5: Demo Chức Năng Sản Phẩm",
               "Danh Sách Thiết Bị & Thiết Lập Kết Nối Phần Cứng FPGA Basys 3", 7, total_slides=TOTAL_SLIDES)

    # Khung bên trái: Hình ảnh thiết bị thực nghiệm và ghi chú kỹ thuật
    card_l20 = add_card(s22, Inches(0.8), Inches(1.35), Inches(5.75), Inches(5.50), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)

    tb_lt20 = s22.shapes.add_textbox(Inches(0.95), Inches(1.50), Inches(5.45), Inches(0.30))
    tf_lt20 = tb_lt20.text_frame
    tf_lt20.margin_left = tf_lt20.margin_top = tf_lt20.margin_right = tf_lt20.margin_bottom = 0
    p_lt20 = tf_lt20.paragraphs[0]
    p_lt20.text = "HỆ THỐNG THỰC NGHIỆM THỰC TẾ (DEVICE SETUP)"
    p_lt20.alignment = PP_ALIGN.CENTER
    p_lt20.font.name = "Segoe UI"
    p_lt20.font.size = Pt(11.0)
    p_lt20.font.bold = True
    p_lt20.font.color.rgb = C_BLUE_ACCENT

    if os.path.exists(img_device):
        # Tỷ lệ ảnh Device.jpg là 1276 x 956 = 1.3347
        # Rộng 5.25 inch -> Cao 3.93 inch
        s22.shapes.add_picture(img_device, Inches(1.05), Inches(1.84), Inches(5.25), Inches(3.93))

    # Hộp ghi chú nổi bật bên dưới hình ảnh
    add_card(s22, Inches(1.05), Inches(5.88), Inches(5.25), Inches(0.82), bg_color=RGBColor(241, 245, 249), border_color=RGBColor(203, 213, 225), border_width=1.0)
    tb_lc20 = s22.shapes.add_textbox(Inches(1.18), Inches(5.92), Inches(5.00), Inches(0.72))
    tf_lc20 = tb_lc20.text_frame
    tf_lc20.word_wrap = True
    tf_lc20.margin_left = tf_lc20.margin_top = tf_lc20.margin_right = tf_lc20.margin_bottom = 0

    p_lc1 = tf_lc20.paragraphs[0]
    p_lc1.text = "ĐIỂM NỔI BẬT TRONG THIẾT KẾ PHẦN CỨNG THỰC TẾ:"
    p_lc1.font.name = "Segoe UI"
    p_lc1.font.size = Pt(8.2)
    p_lc1.font.bold = True
    p_lc1.font.color.rgb = C_BLUE_ACCENT
    p_lc1.space_after = Pt(2)

    p_lc2 = tf_lc20.add_paragraph()
    p_lc2.text = "• Mạch nguồn MB102 cấp riêng 5V DC cho RDM6300 (PMOD chỉ có 3.3V, chung mass GND).\n• Điện trở đệm 1kΩ mắc nối tiếp chân TX RDM6300 sang JA1 Basys 3 bảo vệ I/O 3.3V FPGA."
    p_lc2.font.name = "Segoe UI"
    p_lc2.font.size = Pt(7.8)
    p_lc2.font.color.rgb = C_TEXT_DARK
    p_lc2.line_spacing = 1.15

    # Khung bên phải: Chi tiết BOM thiết bị và giải thích nguyên lý mạch
    card_r20 = add_card(s22, Inches(6.75), Inches(1.35), Inches(5.78), Inches(5.50), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)

    tb_r20 = s22.shapes.add_textbox(Inches(7.05), Inches(1.50), Inches(5.25), Inches(5.20))
    tf_r20 = tb_r20.text_frame
    tf_r20.word_wrap = True
    tf_r20.margin_left = tf_r20.margin_top = tf_r20.margin_right = tf_r20.margin_bottom = 0

    p_r20_h = tf_r20.paragraphs[0]
    p_r20_h.text = "DANH SÁCH THIẾT BỊ & NGUYÊN LÝ PHỐI HỢP MỨC ĐIỆN ÁP"
    p_r20_h.font.name = "Segoe UI"
    p_r20_h.font.bold = True
    p_r20_h.font.size = Pt(11.5)
    p_r20_h.font.color.rgb = C_BLUE_ACCENT
    p_r20_h.space_after = Pt(4)

    hw_sections = [
        ("1. DANH SÁCH THIẾT BỊ THỰC NGHIỆM (BOM)", C_NAVY_MID, [
            ("Bo mạch FPGA Digilent Basys 3:", "Xilinx Artix-7 XC7A35T, 32Mbit SPI Flash S25FL032P, mạch nạp & UART FTDI qua cổng Micro-USB."),
            ("Module RFID RDM6300 (125 kHz):", "Giải mã thẻ EM4100, kèm cuộn cảm ăng-ten rời phát sóng điện từ 125 kHz."),
            ("Mạch nguồn 5V DC độc lập:", "Module nguồn Breadboard MB102 + Adapter DC ngoài cung cấp nguồn 5V ổn định cho RDM6300."),
            ("Điện trở bảo vệ 1kΩ & Phụ kiện:", "Điện trở 1kΩ hạn dòng, Breadboard mini, tập dây nối cắm mạch và thẻ từ RFID 125 kHz mẫu.")
        ]),
        ("2. TẠI SAO CẦN MẠCH NGUỒN 5V RIÊNG CHO RDM6300?", C_AMBER, [
            ("PMOD Basys 3 chỉ cấp 3.3V:", "Không đủ điện áp để mạch dao động LC trên RDM6300 phát từ trường kích hoạt chip thẻ RFID (ở 3.3V module hoàn toàn không nhận diện được thẻ)."),
            ("Giải pháp cấp nguồn 5V ngoài:", "Dùng module MB102 cấp đủ 5V/GND cho RDM6300; Nối chung mass (Common GND) giữa nguồn 5V và Basys 3 để đồng bộ mức tham chiếu logic.")
        ]),
        ("3. TẠI SAO CẦN ĐIỆN TRỞ 1KΩ TRÊN CHÂN TX NỐI BASYS 3?", C_ROSE, [
            ("Chênh lệch mức logic (5V TTL vs 3.3V LVCMOS):", "Chân TX của RDM6300 xuất tín hiệu UART ở mức 5V, trong khi chân I/O FPGA Artix-7 (PMOD JA1 - Pin J1) chỉ chấp nhận mức áp tối đa 3.3V."),
            ("Bảo vệ chân I/O FPGA Artix-7:", "Điện trở 1kΩ mắc nối tiếp hạn chế dòng rò đưa vào diode kẹp (clamping diode) của FPGA < 2mA, ngăn chặn quá áp/hỏng chip, giữ dạng sóng UART sắc nét.")
        ]),
        ("4. GIAO TIẾP HOST PC & HIỂN THỊ TRỰC QUAN", C_GREEN, [
            ("Cáp Micro-USB tiêu chuẩn:", "Vừa cấp nguồn Basys 3 vừa truyền thông với Host Console C qua UART FTDI (9600 bps); LED 7 đoạn hiển thị kết quả PASS/FAIL thời gian thực.")
        ])
    ]

    for sec_idx, (sec_title, sec_col, sec_bullets) in enumerate(hw_sections):
        p_sec = tf_r20.add_paragraph()
        p_sec.text = sec_title
        p_sec.font.name = "Segoe UI"
        p_sec.font.size = Pt(8.8)
        p_sec.font.bold = True
        p_sec.font.color.rgb = sec_col
        p_sec.space_before = Pt(3)
        p_sec.space_after = Pt(1)

        for b_lbl, b_val in sec_bullets:
            p_b = tf_r20.add_paragraph()
            p_b.text = f"• {b_lbl} {b_val}"
            p_b.font.name = "Segoe UI"
            p_b.font.size = Pt(7.8)
            p_b.font.color.rgb = C_TEXT_DARK
            p_b.space_after = Pt(1.5)
            p_b.line_spacing = 1.10

    # =========================================================================
    # SLIDE 8: PHẦN 5 - DEMO THỰC NGHIỆM TRÊN FPGA BASYS 3: CÁC KỊCH BẢN THỰC TẾ
    # =========================================================================
    s23 = prs.slides.add_slide(blank_layout)
    add_header(s23, "Phần 5: Demo Chức Năng Sản Phẩm",
               "Các Kịch Bản Thực Nghiệm & Giao Diện Quản Trị Host Console", 8, total_slides=TOTAL_SLIDES)

    # Khung bên trái: Terminal danh sách các lựa chọn Host Console CLI
    host_menu_lines = [
        "===========================================================",
        "    RDM6300 RFID - PICORV32 - BASYS 3 SPI FLASH MANAGER    ",
        "===========================================================",
        "  [1]  Ping Hardware (Kiem tra ket noi PicoRV32)",
        "  [2]  Input & Save New RFID Tag (Nhap 10 so in tren the)",
        "  [3]  Check RFID Tag in Flash (Kiem tra the da co chua)",
        "  [4]  Delete RFID Tag from Flash (Xoa the khoi Flash)",
        "  [5]  Virtual Scan (Quet the ao: Nhap 10 so tu ban phim)",
        "  [6]  View Access Logs (Xem 512 nhat ky tu Flash 0x310000)",
        "  [7]  Erase Access Logs (Backup CSV & xoa nhat ky Flash)",
        "  [8]  Export RFID Tags to CSV (Xuat danh sach ra file CSV)",
        "  [9]  Import RFID Tags from CSV (Xoa & nap the tu CSV)",
        "  [0]  Exit (Ngat ket noi UART va thoat chuong trinh)",
        "-----------------------------------------------------------",
        "Lua chon cua ban [0-9]: _"
    ]
    add_code_box(s23, Inches(0.8), Inches(1.35), Inches(5.75), Inches(5.50), "Host Console C CLI (rdm6300_manager.exe)", host_menu_lines, status_text="=== UART COM3 @ 9600 bps | 10 CHỨC NĂNG QUẢN TRỊ TOÀN DIỆN ===", title_color=C_CYAN_ACCENT, font_size=8.8, line_spacing=1.18)

    # Khung bên phải: Nhận xét và đánh giá chuyên sâu các chức năng
    card_r21 = add_card(s23, Inches(6.75), Inches(1.35), Inches(5.78), Inches(5.50), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)

    tb_r21 = s23.shapes.add_textbox(Inches(7.05), Inches(1.50), Inches(5.25), Inches(5.20))
    tf_r21 = tb_r21.text_frame
    tf_r21.word_wrap = True
    tf_r21.margin_left = tf_r21.margin_top = tf_r21.margin_right = tf_r21.margin_bottom = 0

    p_r21_h = tf_r21.paragraphs[0]
    p_r21_h.text = "ĐÁNH GIÁ & NHẬN XÉT CÁC CHỨC NĂNG THỰC NGHIỆM"
    p_r21_h.font.name = "Segoe UI"
    p_r21_h.font.bold = True
    p_r21_h.font.size = Pt(11.5)
    p_r21_h.font.color.rgb = C_BLUE_ACCENT
    p_r21_h.space_after = Pt(4)

    host_commentary_sections = [
        ("1. NHÓM KIỂM THỬ KẾT NỐI & GIÁM SÁT [MENU 1, 5]", C_BLUE_ACCENT, [
            ("Menu [1] Ping Hardware:", "Kiểm tra độ trễ phản hồi tức thì qua UART, xác nhận CPU PicoRV32, cầu bus interconnect và UART FIFO 32B hoạt động thông suốt không nghẽn bus."),
            ("Menu [5] Virtual Scan:", "Giả lập quẹt thẻ từ xa qua bàn phím mà không cần đưa thẻ vật lý vào đầu đọc, phục vụ kiểm thử đơn vị (Unit Test) logic phân quyền.")
        ]),
        ("2. NHÓM QUẢN TRỊ WHITELIST THẺ [MENU 2, 3, 4]", C_AMBER, [
            ("Menu [2] & [4] Thêm/Xóa Thẻ:", "Thao tác an toàn trên Flash Sector 48 (0x300000) bằng cơ chế In-SRAM Execution (flashio_worker), bảo đảm không gây treo bus XIP."),
            ("Menu [3] Tra Cứu Thẻ:", "Đọc trực tiếp từ Flash qua XIP với thuật toán dừng sớm (Early Termination), độ trễ xác thực siêu nhỏ (< 10 µs).")
        ]),
        ("3. NHÓM KIỂM TOÁN AN NINH & NHẬT KÝ [MENU 6, 7]", C_ROSE, [
            ("Menu [6] Đọc Access Logs:", "Đọc và giải mã 512 bản ghi từ Sector 49 (0x310000), hiển thị rõ ràng kết quả PASS/FAIL, UID thẻ và số thứ tự sự kiện."),
            ("Menu [7] Xóa Log An Toàn:", "Tự động sao lưu toàn bộ nhật ký ra file CSV trước khi xóa Sector, đảm bảo không mất mát dữ liệu kiểm toán.")
        ]),
        ("4. NHÓM ĐỒNG BỘ DỮ LIỆU NGOẠI TUYẾN [MENU 8, 9]", C_GREEN, [
            ("Menu [8] & [9] Export/Import CSV:", "Sao lưu và phục hồi danh sách 4,096 thẻ nhanh chóng qua cổng UART, rất tiện lợi khi cấu hình hàng loạt cho nhiều trạm kiểm soát.")
        ])
    ]

    for sec_idx, (sec_title, sec_col, sec_bullets) in enumerate(host_commentary_sections):
        p_sec = tf_r21.add_paragraph()
        p_sec.text = sec_title
        p_sec.font.name = "Segoe UI"
        p_sec.font.size = Pt(8.8)
        p_sec.font.bold = True
        p_sec.font.color.rgb = sec_col
        p_sec.space_before = Pt(3)
        p_sec.space_after = Pt(1)

        for b_lbl, b_val in sec_bullets:
            p_b = tf_r21.add_paragraph()
            p_b.text = f"• {b_lbl} {b_val}"
            p_b.font.name = "Segoe UI"
            p_b.font.size = Pt(7.8)
            p_b.font.color.rgb = C_TEXT_DARK
            p_b.space_after = Pt(1.5)
            p_b.line_spacing = 1.10

    # =========================================================================
    # SLIDE 9: PHẦN 6 - MINH CHỨNG KÝ DUYỆT SIGN-OFF, OPENROAD & CONFIG.JSON
    # =========================================================================
    s24 = prs.slides.add_slide(blank_layout)
    add_header(s24, "Phần 6: Thiết Kế Vật Lý ASIC",
               "Minh Chứng Ký Duyệt Sign-off, Bản Vẽ OpenROAD & Cấu Hình OpenLane", 9, total_slides=TOTAL_SLIDES)

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
    add_code_box(s24, lx24_1, top_y, lw24_1, top_h, "Cấu hình OpenLane (config.json)", code_lines_24, font_size=8.2, line_spacing=1.08)

    # 2. Cột 2 (Phải): Bản vẽ Layout OpenROAD (Giữ đúng tỷ lệ ảnh 1.38:1)
    rx24_2 = Inches(6.65)
    rw24_2 = Inches(5.883)
    add_card(s24, rx24_2, top_y, rw24_2, top_h, bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
    
    tb_c2_lbl = s24.shapes.add_textbox(rx24_2 + Inches(0.20), top_y + Inches(0.08), rw24_2 - Inches(0.40), Inches(0.30))
    tb_c2_lbl.text_frame.margin_left = tb_c2_lbl.text_frame.margin_top = 0
    p_c2 = tb_c2_lbl.text_frame.paragraphs[0]
    p_c2.text = "🖼️ Bản Vẽ Layout OpenROAD (Die 1.87 mm² - 1362 x 1373 µm)"
    p_c2.font.name = "Segoe UI"
    p_c2.font.size = Pt(10.5)
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
    p_ss_h.font.size = Pt(11.5)
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
        p_item.font.size = Pt(8.5)
        p_item.font.color.rgb = C_TEXT_DARK
        p_item.space_after = Pt(1.5)
        p_item.line_spacing = 1.10

    # =========================================================================
    # SLIDE 10: PHẦN 6 - BẢNG TỔNG HỢP KẾT QUẢ VẬT LÝ & THỐNG KÊ PPA METRICS
    # =========================================================================
    s25 = prs.slides.add_slide(blank_layout)
    add_header(s25, "Phần 6: Thiết Kế Vật Lý ASIC",
               "Tổng Hợp Kết Quả Thiết Kế Vật Lý & Chỉ Số PPA (OpenLane 2 / SkyWater 130nm)", 10, total_slides=TOTAL_SLIDES)

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
               "Phân Tích Định Thời Tĩnh STA & Báo Cáo Multi-Corner Timing (summary.rpt)", 11, total_slides=TOTAL_SLIDES)

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
            p.font.size = Pt(11.0)
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
                p.font.size = Pt(10.0)
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
    p_cl_h.font.size = Pt(11.0)
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
        p.font.size = Pt(8.5)
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
    p_cr_h.font.size = Pt(11.0)
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
        p.font.size = Pt(8.5)
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

    p_ty = tf_t24.add_paragraph()
    p_ty.text = "XIN TRÂN TRỌNG CẢM ƠN THẦY CÔ VÀ HỘI ĐỒNG ĐÃ LẮNG NGHE!"
    p_ty.font.name = "Segoe UI"
    p_ty.font.size = Pt(22)
    p_ty.font.bold = True
    p_ty.font.color.rgb = C_WHITE
    p_ty.space_before = Pt(28)

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
