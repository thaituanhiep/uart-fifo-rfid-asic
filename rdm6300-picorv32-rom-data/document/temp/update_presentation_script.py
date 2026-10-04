# -*- coding: utf-8 -*-
"""
Helper script to update create_presentation.py with the 26-slide publication deck.
"""
import os

def generate_new_presentation_py():
    script_content = '''# -*- coding: utf-8 -*-
"""
Script: create_presentation.py
Tạo bộ slide báo cáo PowerPoint 16:9 widescreen tiêu chuẩn xuất bản cao cấp (Publication-Grade)
theo đúng cấu trúc yêu cầu của đề tài:
1. Block Diagram SoC PicoRV32 (B&W Draw.io chuẩn xuất bản: PicoRV32, spimemio, data_sram cấu hình firmware, soc_interconnect logic giải mã, UART MMIO)
2. Bảng 2 cột đối chiếu chu kỳ bus thực tế (Master Roadmap)
3. 8 slide chuyên sâu độc lập (1 slide cho mỗi row trong bảng 2 cột), trình bày đoạn code C thực tế sử dụng biến địa chỉ, giải mã RTL và cơ chế đồng thiết kế phần cứng - phần mềm.
4. Hệ thống Testbench mô phỏng xsim (tb_uart_rtl.v, tb_uart_ping.v).
5. Thực nghiệm và Demo sản phẩm trên bo mạch FPGA Basys 3.
6. Thiết kế vật lý ASIC OpenLane 2 & Ký duyệt Sign-off (SkyWater 130nm PDK).
7. Tổng kết và đóng góp của đề tài.

Tổng cộng: 26 slides thiết kế trực quan, tỷ lệ 16:9 chuẩn công nghiệp.
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

    # Bảng màu thiết kế chuyên nghiệp (Executive Dark & Clean Light)
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

    img_fig2 = os.path.join(cur_dir, "fig2_soc_interconnect.png")
    if not os.path.exists(img_fig2):
        img_fig2 = os.path.join(doc_dir, "fig2_soc_interconnect.png")

    img_openroad = os.path.join(project_root, "OpenROAD.png")
    if not os.path.exists(img_openroad):
        img_openroad = os.path.join(cur_dir, "OpenROAD.png")
    if not os.path.exists(img_openroad):
        img_openroad = os.path.join(doc_dir, "OpenROAD.png")

    img_signoff = os.path.join(project_root, "AntennaLvsDrc.png")
    if not os.path.exists(img_signoff):
        img_signoff = os.path.join(cur_dir, "AntennaLvsDrc.png")
    if not os.path.exists(img_signoff):
        img_signoff = os.path.join(doc_dir, "AntennaLvsDrc.png")

    TOTAL_SLIDES = 26

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
        p_title.font.size = Pt(19)
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
        p_foot.text = "Đồ Án Tốt Nghiệp: SoC PicoRV32 RFID RDM6300 & SPI Flash | SV: Thái Tuấn Hiệp | GVHD: ThS. Nguyễn Văn Đông"
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
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(border_width)
        return card

    # Helper: Hộp mã nguồn dạng Terminal
    def add_code_box(slide, x, y, w, h, title, lines, result_banner=None):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
        card.fill.solid()
        card.fill.fore_color.rgb = C_NAVY_DARK
        card.line.color.rgb = C_BLUE_ACCENT
        card.line.width = Pt(1.5)

        tb = slide.shapes.add_textbox(x + Inches(0.12), y + Inches(0.08), w - Inches(0.24), h - Inches(0.16))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = f"// {title}"
        p0.font.name = "Consolas"
        p0.font.size = Pt(9.5)
        p0.font.bold = True
        p0.font.color.rgb = RGBColor(56, 189, 248)
        p0.space_after = Pt(3)

        for l in lines:
            p = tf.add_paragraph()
            p.text = l
            p.font.name = "Consolas"
            p.font.size = Pt(8.0)
            p.font.color.rgb = RGBColor(226, 232, 240)
            p.space_after = Pt(0.5)

        if result_banner:
            pr = tf.add_paragraph()
            pr.text = result_banner
            pr.font.name = "Consolas"
            pr.font.size = Pt(9.0)
            pr.font.bold = True
            pr.font.color.rgb = C_GREEN
            pr.space_before = Pt(3)

    # Helper: Bảng đối chiếu chu kỳ bus thực tế (Master Roadmap Table 8 Rows)
    def add_bus_table_slide(slide_num, title, rows_data):
        slide = prs.slides.add_slide(blank_layout)
        add_header(slide, "Phần 6: Firmware C & Ánh Xạ MMIO", title, slide_num, total_slides=TOTAL_SLIDES)

        x = Inches(0.8)
        y = Inches(1.30)
        w = Inches(11.733)
        h = Inches(5.60)

        num_rows = len(rows_data) + 1
        tbl_shape = slide.shapes.add_table(num_rows, 2, x, y, w, h)
        tbl = tbl_shape.table

        col_w = [Inches(2.40), Inches(9.333)]
        for ci, cw in enumerate(col_w):
            tbl.columns[ci].width = cw

        headers = [
            "Trường Hợp / Thời Điểm",
            "Thiết Lập RTL, Định Nghĩa C & Ý Nghĩa Thao Tác Của Firmware C"
        ]

        for ci, h_text in enumerate(headers):
            cell = tbl.cell(0, ci)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_NAVY_DARK
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.margin_left = Inches(0.12)
            cell.margin_right = Inches(0.12)
            cell.margin_top = Inches(0.06)
            cell.margin_bottom = Inches(0.06)

            p = cell.text_frame.paragraphs[0]
            p.text = h_text
            p.font.name = "Segoe UI"
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = C_WHITE
            p.alignment = PP_ALIGN.CENTER if ci == 0 else PP_ALIGN.LEFT

        for ri, r in enumerate(rows_data):
            row_idx = ri + 1
            row_bg = RGBColor(241, 245, 249) if ri % 2 == 0 else RGBColor(255, 255, 255)

            # Cột 0: Trường hợp
            c0 = tbl.cell(row_idx, 0)
            c0.fill.solid()
            c0.fill.fore_color.rgb = row_bg
            c0.vertical_anchor = MSO_ANCHOR.MIDDLE
            c0.margin_left = Inches(0.08)
            c0.margin_right = Inches(0.08)
            tf0 = c0.text_frame
            tf0.word_wrap = True

            p0_1 = tf0.paragraphs[0]
            p0_1.text = r["time"]
            p0_1.font.name = "Segoe UI"
            p0_1.font.size = Pt(11)
            p0_1.font.bold = True
            p0_1.font.color.rgb = C_BLUE_ACCENT
            p0_1.alignment = PP_ALIGN.CENTER

            p0_2 = tf0.add_paragraph()
            p0_2.text = r["task"]
            p0_2.font.name = "Segoe UI"
            p0_2.font.size = Pt(9.5)
            p0_2.font.bold = True
            p0_2.font.color.rgb = C_TEXT_DARK
            p0_2.alignment = PP_ALIGN.CENTER

            # Cột 1: RTL, C & Ý nghĩa
            c1 = tbl.cell(row_idx, 1)
            c1.fill.solid()
            c1.fill.fore_color.rgb = row_bg
            c1.vertical_anchor = MSO_ANCHOR.MIDDLE
            c1.margin_left = Inches(0.12)
            c1.margin_right = Inches(0.12)
            c1.margin_top = Inches(0.04)
            c1.margin_bottom = Inches(0.04)
            tf1 = c1.text_frame
            tf1.word_wrap = True

            # RTL line
            p1 = tf1.paragraphs[0]
            r1_lbl = p1.add_run()
            r1_lbl.text = "• RTL: "
            r1_lbl.font.name = "Segoe UI"
            r1_lbl.font.size = Pt(9.5)
            r1_lbl.font.bold = True
            r1_lbl.font.color.rgb = C_BLUE_ACCENT

            r1_file = p1.add_run()

            r1_file.text = r["rtl_file"] + "  "
            r1_file.font.name = "Segoe UI"
            r1_file.font.size = Pt(9.0)
            r1_file.font.bold = True
            r1_file.font.color.rgb = RGBColor(30, 58, 138)

            r1_code = p1.add_run()

            r1_code.text = r["rtl_code"]
            r1_code.font.name = "Consolas"
            r1_code.font.size = Pt(9.0)
            r1_code.font.bold = True
            r1_code.font.color.rgb = RGBColor(15, 23, 42)
            p1.space_after = Pt(1.5)

            # C line
            p2 = tf1.add_paragraph()
            r2_lbl = p2.add_run()
            r2_lbl.text = "• Code C: "
            r2_lbl.font.name = "Segoe UI"
            r2_lbl.font.size = Pt(9.5)
            r2_lbl.font.bold = True
            r2_lbl.font.color.rgb = C_GREEN

            r2_file = p2.add_run()

            r2_file.text = r["c_file"] + "  "
            r2_file.font.name = "Segoe UI"
            r2_file.font.size = Pt(9.0)
            r2_file.font.bold = True
            r2_file.font.color.rgb = RGBColor(21, 128, 61)

            r2_code = p2.add_run()

            r2_code.text = r["c_code"]
            r2_code.font.name = "Consolas"
            r2_code.font.size = Pt(9.0)
            r2_code.font.bold = True
            r2_code.font.color.rgb = RGBColor(15, 23, 42)
            p2.space_after = Pt(1.5)

            # Meaning line
            p3 = tf1.add_paragraph()
            r3_lbl = p3.add_run()
            r3_lbl.text = "• Ý nghĩa: "
            r3_lbl.font.name = "Segoe UI"
            r3_lbl.font.size = Pt(9.5)
            r3_lbl.font.bold = True
            r3_lbl.font.color.rgb = RGBColor(194, 65, 12)

            r3_text = p3.add_run()

            r3_text.text = r["meaning"]
            r3_text.font.name = "Segoe UI"
            r3_text.font.size = Pt(9.0)
            r3_text.font.color.rgb = C_TEXT_DARK

        return slide

    # Helper: Slide chi tiết cho từng trường hợp bus (Dedicated 1 Slide per Row)
    def add_case_detail_slide(slide_num, case_idx, time_tag, task_name, addr_info, bus_sig,
                               rtl_file, rtl_lines, rtl_desc,
                               c_file, c_lines, c_desc,
                               why_title, why_text, theme_color=C_BLUE_ACCENT):
        slide = prs.slides.add_slide(blank_layout)
        add_header(slide, f"Phần 6: Chi Tiết Chu Kỳ Bus & Biến Địa Chỉ C (Case {case_idx}/8)", 
                   f"Trường Hợp {case_idx}: {time_tag} - {task_name}", slide_num, total_slides=TOTAL_SLIDES)

        # Top Badge Bar
        badge_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.22), Inches(11.733), Inches(0.40))
        badge_box.fill.solid()
        badge_box.fill.fore_color.rgb = RGBColor(241, 245, 249)
        badge_box.line.color.rgb = theme_color
        badge_box.line.width = Pt(1.2)
        tf_b = badge_box.text_frame
        tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
        p_b = tf_b.paragraphs[0]
        p_b.alignment = PP_ALIGN.CENTER
        
        r_b1 = p_b.add_run()
        
        r_b1.text = "ĐỊA CHỈ TRUY XUẤT: "
        r_b1.font.name = "Segoe UI"
        r_b1.font.bold = True
        r_b1.font.size = Pt(10)
        r_b1.font.color.rgb = theme_color
        
        r_b2 = p_b.add_run()
        
        r_b2.text = f"{addr_info}   |   "
        r_b2.font.name = "Consolas"
        r_b2.font.bold = True
        r_b2.font.size = Pt(10)
        r_b2.font.color.rgb = C_TEXT_DARK
        
        r_b3 = p_b.add_run()
        
        r_b3.text = "TÍN HIỆU BUS INTERCONNECT: "
        r_b3.font.name = "Segoe UI"
        r_b3.font.bold = True
        r_b3.font.size = Pt(10)
        r_b3.font.color.rgb = theme_color
        
        r_b4 = p_b.add_run()
        
        r_b4.text = f"{bus_sig}   |   "
        r_b4.font.name = "Consolas"
        r_b4.font.bold = True
        r_b4.font.size = Pt(10)
        r_b4.font.color.rgb = C_TEXT_DARK

        r_b5 = p_b.add_run()

        r_b5.text = "THỜI ĐIỂM: "
        r_b5.font.name = "Segoe UI"
        r_b5.font.bold = True
        r_b5.font.size = Pt(10)
        r_b5.font.color.rgb = theme_color
        
        r_b6 = p_b.add_run()
        
        r_b6.text = time_tag
        r_b6.font.name = "Segoe UI"
        r_b6.font.bold = True
        r_b6.font.size = Pt(10)
        r_b6.font.color.rgb = C_TEXT_DARK

        # Left Column: RTL Verilog
        add_code_box(slide, Inches(0.8), Inches(1.70), Inches(5.7), Inches(2.6), rtl_file, rtl_lines)
        
        card_l = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.38), Inches(5.7), Inches(1.35))
        card_l.fill.solid()
        card_l.fill.fore_color.rgb = C_WHITE
        card_l.line.color.rgb = C_CARD_BORDER
        card_l.line.width = Pt(1.0)
        tf_l = card_l.text_frame
        tf_l.word_wrap = True
        tf_l.margin_left = tf_l.margin_right = Inches(0.12)
        tf_l.margin_top = tf_l.margin_bottom = Inches(0.08)
        p_l_t = tf_l.paragraphs[0]
        p_l_t.text = "CƠ CHẾ PHẦN CỨNG & GIẢI MÃ BUS:"
        p_l_t.font.name = "Segoe UI"
        p_l_t.font.bold = True
        p_l_t.font.size = Pt(10)
        p_l_t.font.color.rgb = theme_color
        p_l_t.space_after = Pt(2)
        for bullet in rtl_desc:
            p = tf_l.add_paragraph()
            p.text = f"• {bullet}"
            p.font.name = "Segoe UI"
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_TEXT_DARK
            p.space_after = Pt(1.5)
            p.line_spacing = 1.1

        # Right Column: C Code Snippet
        add_code_box(slide, Inches(6.8), Inches(1.70), Inches(5.73), Inches(2.6), c_file, c_lines)

        card_r = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(4.38), Inches(5.73), Inches(1.35))
        card_r.fill.solid()
        card_r.fill.fore_color.rgb = C_WHITE
        card_r.line.color.rgb = C_CARD_BORDER
        card_r.line.width = Pt(1.0)
        tf_r = card_r.text_frame
        tf_r.word_wrap = True
        tf_r.margin_left = tf_r.margin_right = Inches(0.12)
        tf_r.margin_top = tf_r.margin_bottom = Inches(0.08)
        p_r_t = tf_r.paragraphs[0]
        p_r_t.text = "THAO TÁC CỦA FIRMWARE C:"
        p_r_t.font.name = "Segoe UI"
        p_r_t.font.bold = True
        p_r_t.font.size = Pt(10)
        p_r_t.font.color.rgb = theme_color
        p_r_t.space_after = Pt(2)
        for bullet in c_desc:
            p = tf_r.add_paragraph()
            p.text = f"• {bullet}"
            p.font.name = "Segoe UI"
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_TEXT_DARK
            p.space_after = Pt(1.5)
            p.line_spacing = 1.1

        # Bottom Card: Hardware-Software Co-Design Insight
        card_bot = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(5.82), Inches(11.733), Inches(1.10))
        card_bot.fill.solid()
        card_bot.fill.fore_color.rgb = C_WHITE
        card_bot.line.color.rgb = theme_color
        card_bot.line.width = Pt(1.5)
        tf_bot = card_bot.text_frame
        tf_bot.word_wrap = True
        tf_bot.margin_left = tf_bot.margin_right = Inches(0.15)
        tf_bot.margin_top = tf_bot.margin_bottom = Inches(0.08)
        
        p_b_h = tf_bot.paragraphs[0]
        p_b_h.text = f"Ý NGHĨA ĐỒNG THIẾT KẾ PHẦN CỨNG - PHẦN MỀM: {why_title.upper()}"
        p_b_h.font.name = "Segoe UI"
        p_b_h.font.bold = True
        p_b_h.font.size = Pt(10.5)
        p_b_h.font.color.rgb = theme_color
        p_b_h.space_after = Pt(2)
        
        p_b_t = tf_bot.add_paragraph()
        p_b_t.text = why_text
        p_b_t.font.name = "Segoe UI"
        p_b_t.font.size = Pt(10)
        p_b_t.font.color.rgb = C_TEXT_DARK
        p_b_t.line_spacing = 1.15
        
        return slide

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

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.1), Inches(10.9), Inches(5.3))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "BÁO CÁO ĐỒ ÁN THIẾT KẾ VI MẠCH SỐ & HỆ THỐNG NHÚNG"
    p0.font.name = "Segoe UI"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = C_CYAN_ACCENT
    p0.space_after = Pt(10)

    p_main = tf1.add_paragraph()
    p_main.text = "THIẾT KẾ HỆ THỐNG TRÊN VI MẠCH (SoC) CHO THIẾT BỊ KIỂM SOÁT RA VÀO DỰA TRÊN RFID RDM6300 VÀ BỘ NHỚ SPI FLASH"
    p_main.font.name = "Segoe UI"
    p_main.font.size = Pt(22)
    p_main.font.bold = True
    p_main.font.color.rgb = C_WHITE
    p_main.space_after = Pt(14)
    p_main.line_spacing = 1.15

    p_sub = tf1.add_paragraph()
    p_sub.text = "Tích hợp CPU RISC-V PicoRV32 | Kiến trúc Boot Flash XIP | Tạo mẫu Basys 3 FPGA | Ký duyệt ASIC OpenLane 2 (SkyWater 130nm)"
    p_sub.font.name = "Segoe UI"
    p_sub.font.size = Pt(12)
    p_sub.font.color.rgb = RGBColor(203, 213, 225)
    p_sub.space_after = Pt(24)

    p_info1 = tf1.add_paragraph()
    p_info1.text = "Sinh viên thực hiện :  Thái Tuấn Hiệp  -  MSSV: 20210328  (Chuyên ngành Kỹ thuật Vi điện tử)"
    p_info1.font.name = "Segoe UI"
    p_info1.font.size = Pt(12.5)
    p_info1.font.bold = True
    p_info1.font.color.rgb = C_WHITE
    p_info1.space_after = Pt(6)

    p_info2 = tf1.add_paragraph()
    p_info2.text = "Giảng viên hướng dẫn :  ThS. Nguyễn Văn Đông  -  Bộ môn Kỹ thuật Máy tính & Vi điện tử"
    p_info2.font.name = "Segoe UI"
    p_info2.font.size = Pt(12)
    p_info2.font.color.rgb = RGBColor(226, 232, 240)
    p_info2.space_after = Pt(6)

    p_info3 = tf1.add_paragraph()
    p_info3.text = "Thời gian thực hiện :  Học kỳ 2025.2 - 2026.1  |  Địa điểm: Phòng thí nghiệm Thiết kế Vi mạch VLSI"
    p_info3.font.name = "Segoe UI"
    p_info3.font.size = Pt(11)
    p_info3.font.italic = True
    p_info3.font.color.rgb = RGBColor(148, 163, 184)

    # =========================================================================
    # SLIDE 2: MỤC LỤC / NỘI DUNG BÁO CÁO (Agenda)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Tổng Quan Báo Cáo", "Nội Dung Báo Cáo Đồ Án (9 Phần Chuẩn Mực)", 2)

    agenda_items = [
        ("Phần 1: Giới Thiệu Dự Án", "Thiết bị kiểm soát ra vào offline, lý do chọn SPI Flash NVM."),
        ("Phần 2: Lựa Chọn Phần Cứng", "Bo mạch FPGA Basys 3 (Artix-7 XC7A35T) & Đầu đọc RFID RDM6300."),
        ("Phần 3: Lựa Chọn Phần Mềm", "Vivado 2025.1, OpenLane 2 (Sky130A), RISC-V GCC & Host Console C."),
        ("Phần 4: Block Diagram SoC", "Sơ đồ khối kiến trúc vi hệ thống SoC PicoRV32 (B&W Draw.io chuẩn xuất bản)."),
        ("Phần 5: Khối Liên Kết Bus", "soc_interconnect.v, giải mã địa chỉ và cơ chế chạy Firmware C."),
        ("Phần 6: Chi Tiết Chu Kỳ Bus & C", "Master Roadmap 2 cột & 8 slide chuyên sâu từng trường hợp bus & biến C."),
        ("Phần 7: Hệ Thống Testbench", "Mô phỏng tb_uart_rtl.v (RTL thuần) và tb_uart_ping.v (Top SoC Boot Flash)."),
        ("Phần 8: Demo Thực Nghiệm", "Tạo mẫu Basys 3 FPGA, giao tiếp UART PC và quẹt thẻ RFID thật."),
        ("Phần 9: Thiết Kế Vật Lý ASIC", "OpenLane 2 RTL-to-GDSII: Sign-off 0 DRC, 0 LVS, 0 Antenna, MET TIMING.")
    ]

    for i, (ag_t, ag_d) in enumerate(agenda_items):
        col = i % 3
        row = i // 3
        ax = Inches(0.8) + col * Inches(3.95)
        ay = Inches(1.35) + row * Inches(1.80)
        aw = Inches(3.75)
        ah = Inches(1.65)

        card_ag = add_card(s2, ax, ay, aw, ah)
        tb_ag = s2.shapes.add_textbox(ax + Inches(0.15), ay + Inches(0.12), aw - Inches(0.3), ah - Inches(0.24))
        tf_ag = tb_ag.text_frame
        tf_ag.word_wrap = True

        p1 = tf_ag.paragraphs[0]
        p1.text = ag_t
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(11.5)
        p1.font.bold = True
        p1.font.color.rgb = C_BLUE_ACCENT
        p1.space_after = Pt(4)

        p2 = tf_ag.add_paragraph()
        p2.text = ag_d
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_TEXT_MUTED
        p2.line_spacing = 1.15

    # =========================================================================
    # SLIDE 3: PHẦN 1 - GIỚI THIỆU DỰ ÁN & LÝ DO CHỌN SPI FLASH NVM
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Phần 1: Giới Thiệu Dự Án", "Thiết Bị Kiểm Soát Ra Vào Offline & Lý Do Lựa Chọn SPI Flash", 3)

    p1_cards = [
        ("TÍNH CẤP THIẾT CỦA HỆ THỐNG OFFLINE", C_BLUE_ACCENT, [
            ("Hạn chế của Access Control dựa trên Cloud:", "Phụ thuộc kết nối Internet, độ trễ mạng lớn (vài trăm ms đến vài giây), nguy cơ gián đoạn khi đứt cáp và lộ lọt dữ liệu định danh nhân sự."),
            ("Định hướng hệ thống Offline Standalone:", "SoC tự giải mã thẻ và tự đối chiếu phân quyền tại chỗ với độ trễ siêu nhỏ (< 10 µs), vận hành ổn định 24/7 tại các địa bàn biệt lập, bảo mật cao."),
            ("Nhu cầu tự chủ thiết kế vi mạch ASIC:", "Loại bỏ hoàn toàn nguy cơ backdoor phần cứng, làm chủ từ kiến trúc RTL đến quy trình chế tạo vi mạch bán dẫn.")
        ]),
        ("VAI TRÒ CỐT TỬ CỦA BỘ NHỚ SPI FLASH NVM", C_GREEN, [
            ("Lưu trữ bất biến không cần pin nuôi:", "Khác với RAM mất sạch dữ liệu khi ngắt điện, SPI Flash lưu trữ danh sách thẻ (Whitelist) và nhật ký quẹt thẻ (Access Logs) an toàn trên 20 năm."),
            ("Dung lượng lớn với chi phí tối thiểu:", "Dung lượng 32 Mbit (4MB) cho phép lưu tới 4,096 thẻ người dùng và 512 bản ghi nhật ký kiểm toán với chi phí linh kiện cực rẻ."),
            ("Tiết kiệm chân kết nối ngoại vi ASIC:", "Chuẩn SPI chỉ dùng 4 chân tín hiệu (CS, SCK, MOSI, MISO), tối ưu hóa số chân pad (chỉ 31 chân toàn vi mạch) và diện tích die silicon."),
            ("Hỗ trợ chế độ thực thi lệnh tại chỗ (XIP):", "Cho phép CPU PicoRV32 kéo trực tiếp mã lệnh từ Flash chạy mà không cần nạp vào SRAM lớn.")
        ])
    ]

    for i, (c_title, c_col, points) in enumerate(p1_cards):
        cx = Inches(0.8) + i * Inches(5.9)
        cw = Inches(5.7)
        add_card(s3, cx, Inches(1.35), cw, Inches(5.4), bg_color=C_WHITE, border_color=c_col, border_width=2.0)
        tb_c = s3.shapes.add_textbox(cx + Inches(0.2), Inches(1.5), cw - Inches(0.4), Inches(5.1))
        tf_c = tb_c.text_frame
        tf_c.word_wrap = True

        pt = tf_c.paragraphs[0]
        pt.text = c_title
        pt.font.name = "Segoe UI"
        pt.font.size = Pt(13)
        pt.font.bold = True
        pt.font.color.rgb = c_col
        pt.space_after = Pt(12)

        for p_lbl, p_val in points:
            p = tf_c.add_paragraph()
            p.text = f"• {p_lbl} {p_val}"
            p.font.name = "Segoe UI"
            p.font.size = Pt(10.5)
            p.font.color.rgb = C_TEXT_DARK
            p.space_after = Pt(10)
            p.line_spacing = 1.2

    # =========================================================================
    # SLIDE 4: PHẦN 2 - LỰA CHỌN PHẦN CỨNG: BASYS 3 & RDM6300
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Phần 2: Lựa Chọn Phần Cứng", "Nền Tảng Tạo Mẫu FPGA Basys 3 & Module Đọc Thẻ RFID RDM6300", 4)

    p2_cards = [
        ("MODULE RFID 125 KHZ RDM6300", C_AMBER, [
            ("Chuẩn định danh thông dụng:", "Tương thích chuẩn thẻ không tiếp xúc EM4100 / TK4100 tần số 125 kHz."),
            ("Giao tiếp UART 9600-8-N-1:", "Tự động phát chuỗi 14 byte ASCII khi quẹt thẻ (1 STX + 10 Hex UID + 2 Checksum + 1 ETX)."),
            ("Ăng-ten cuộn cảm rời độ nhạy cao:", "Khoảng cách nhận diện thẻ ổn định từ 20 mm - 50 mm."),
            ("Kết nối PMOD JA linh hoạt:", "Dễ dàng cắm trực tiếp vào bo mạch FPGA để thu nhận tín hiệu nối tiếp.")
        ]),
        ("BO MẠCH FPGA DIGILENT BASYS 3", C_BLUE_ACCENT, [
            ("Chip FPGA Xilinx Artix-7 XC7A35T:", "Cung cấp 33,280 Logic Cells, 1,800 Kbits Block RAM, 90 DSP Slices."),
            ("Nền tảng tạo mẫu phần cứng (Prototyping):", "Kiểm chứng thực nghiệm thiết kế SoC trong điều kiện thời gian thực với thẻ thật trước khi gửi chế tạo ASIC."),
            ("Tích hợp ngoại vi phong phú:", "Cổng PMOD JA cho RFID, chip FTDI nạp bitstream và UART PC qua Micro-USB, 16 LED và 16 Switch."),
            ("Chip SPI Flash On-board 32 Mbit:", "Spansion S25FL032P kết nối sẵn, hỗ trợ hoàn hảo cho kiểm chứng boot XIP.")
        ])
    ]

    for i, (c_title, c_col, points) in enumerate(p2_cards):
        cx = Inches(0.8) + i * Inches(5.9)
        cw = Inches(5.7)
        add_card(s4, cx, Inches(1.35), cw, Inches(5.4), bg_color=C_WHITE, border_color=c_col, border_width=2.0)
        tb_c = s4.shapes.add_textbox(cx + Inches(0.2), Inches(1.5), cw - Inches(0.4), Inches(5.1))
        tf_c = tb_c.text_frame
        tf_c.word_wrap = True

        pt = tf_c.paragraphs[0]
        pt.text = c_title
        pt.font.name = "Segoe UI"
        pt.font.size = Pt(13)
        pt.font.bold = True
        pt.font.color.rgb = c_col
        pt.space_after = Pt(12)

        for p_lbl, p_val in points:
            p = tf_c.add_paragraph()
            p.text = f"• {p_lbl} {p_val}"
            p.font.name = "Segoe UI"
            p.font.size = Pt(10.5)
            p.font.color.rgb = C_TEXT_DARK
            p.space_after = Pt(10)
            p.line_spacing = 1.2

    # =========================================================================
    # SLIDE 5: PHẦN 3 - LỰA CHỌN PHẦN MỀM & CHUỖI CÔNG CỤ PHÁT TRIỂN
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Phần 3: Lựa Chọn Phần Mềm", "Chuỗi Công Cụ Phát Triển: FPGA, ASIC OpenLane 2 & Toolchain Nhúng", 5)

    sw_tools = [
        ("MÔ PHỎNG & FPGA: XILINX VIVADO", C_BLUE_ACCENT, [
            ("Môi trường Vivado 2025.1:", "Công cụ số 1 thế giới cho tổng hợp logic và nạp FPGA Artix-7."),
            ("Vivado Simulator (xsim):", "Mô phỏng chính xác mức chu kỳ clock cho cả testbench RTL thuần và Top SoC."),
            ("Tự động hóa bằng Batch Script:", "Tích hợp sẵn run_sim_uart.bat và run_sim_ping.bat chạy 1-click.")
        ]),
        ("THIẾT KẾ VẬT LÝ ASIC: OPENLANE 2", C_PURPLE, [
            ("Chuỗi công cụ nguồn mở OpenLane 2:", "Hiện thực hóa luồng RTL-to-GDSII tự động trên tiến trình SkyWater 130nm."),
            ("Công cụ chuẩn công nghiệp tích hợp:", "Yosys (Synthesis), OpenROAD (P&R), Magic & KLayout (DRC), Netgen (LVS)."),
            ("Sign-off Tape-out Ready:", "Tự động chèn diode triệt tiêu Antenna, tối ưu hóa timing MET TIMING 50 MHz.")
        ]),
        ("TOOLCHAIN FIRMWARE: RISC-V GCC & C", C_GREEN, [
            ("Bộ biên dịch riscv32-unknown-elf-gcc:", "Biên dịch mã C thành tập lệnh RV32I freestanding tối ưu kích thước."),
            ("Linker Script sections.lds:", "Định vị mã nguồn vào Flash XIP (0x0025_0000) và biến vào 1KB SRAM."),
            ("Host Console C tương tác:", "Phần mềm quản trị trên máy tính hỗ trợ 11 lệnh điều khiển qua UART.")
        ])
    ]

    for i, (tool_title, tool_col, points) in enumerate(sw_tools):
        tx = Inches(0.8) + i * Inches(3.95)
        add_card(s5, tx, Inches(1.4), Inches(3.75), Inches(5.3), bg_color=C_WHITE, border_color=tool_col, border_width=2.0)
        tb_t = s5.shapes.add_textbox(tx + Inches(0.18), Inches(1.6), Inches(3.39), Inches(4.9))
        tf_t = tb_t.text_frame
        tf_t.word_wrap = True

        pt = tf_t.paragraphs[0]
        pt.text = tool_title
        pt.font.name = "Segoe UI"
        pt.font.size = Pt(12)
        pt.font.bold = True
        pt.font.color.rgb = tool_col
        pt.space_after = Pt(12)

        for p_lbl, p_val in points:
            p = tf_t.add_paragraph()
            p.text = f"• {p_lbl} {p_val}"
            p.font.name = "Segoe UI"
            p.font.size = Pt(10.5)
            p.font.color.rgb = C_TEXT_DARK
            p.space_after = Pt(8)
            p.line_spacing = 1.15

    # =========================================================================
    # SLIDE 6: PHẦN 4 - TỔNG QUAN KIẾN TRÚC SOC PICORV32
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Phần 4: Kiến Trúc Vi Hệ Thống SoC", "Kiến Trúc Tổng Thể Vi Hệ Thống SoC PicoRV32 (1 Master - 5 Slaves)", 6)

    soc_layers = [
        ("BUS MASTER: PICORV32 RISC-V CPU CORE", C_BLUE_ACCENT, [
            ("Lõi xử lý RISC-V 32-bit (RV32I):", "32 thanh ghi đa năng (x0..x31), thiết kế nhỏ gọn, tối ưu diện tích silicon ASIC."),
            ("Vector Reset phần cứng:", "PROGADDR_RESET = 32'h0025_0000 trỏ thẳng vào phân vùng firmware trong SPI Flash."),
            ("Đỉnh con trỏ Stack phần cứng:", "STACKADDR = 32'h0000_0400 trỏ đỉnh khối 1KB SRAM nội bộ."),
            ("Giao diện Native Memory Bus:", "cpu_mem_valid, cpu_mem_addr, cpu_mem_wdata, cpu_mem_wstrb, cpu_mem_ready, cpu_mem_rdata.")
        ]),
        ("TRỌNG TÀI BUS: SOC_INTERCONNECT.V", C_AMBER, [
            ("Cầu nối ghép kênh trung tâm:", "Kết nối 1 Master CPU PicoRV32 tới 5 khối Slaves độc lập bằng mạch tổ hợp thuần túy."),
            ("Giải mã địa chỉ trong suốt (Decoding):", "Tự động nhận diện dải địa chỉ và tiền tố 4 bit cao [31:28] để kích hoạt cờ sel_*."),
            ("Ghép kênh dữ liệu đọc (Response MUX):", "cpu_mem_rdata tự động chọn dữ liệu từ SRAM, Flash, RFID, UART hoặc GPIO."),
            ("Tổng hợp cờ sẵn sàng (Ready Handshake):", "cpu_mem_ready = sram_ready || spimem_ready || rfid_ready || uart_ready || gpio_ready.")
        ]),
        ("5 SLAVES NGOẠI VI & BỘ NHỚ CHUYÊN BIỆT", C_GREEN, [
            ("Slave 0 - 1KB Data SRAM (data_sram.v):", "256 từ x 32-bit, lưu Stack C và biến động, phản hồi 1 clock zero-wait."),
            ("Slave 1 & 1b - SPI Flash Controller (spimemio.v):", "Chạy mã XIP (0x0010_0000) và thanh ghi bit-bang SPI (0x0200_0000)."),
            ("Slave 2 - RFID Reader UART MMIO (uart_mmio.v):", "Tích hợp FIFO 32B đệm chuỗi thẻ RDM6300 tại địa chỉ 0x1000_0000."),
            ("Slave 3 - Host PC UART MMIO (uart_mmio.v):", "Tích hợp 2 bộ đệm FIFO 32B giao tiếp máy tính tại 0x3000_0000."),
            ("Slave 4 - GPIO MMIO Module (soc_gpio_mmio.v):", "Thanh ghi chốt 16 LED trạng thái và điều khiển mở relay cửa tại 0x4000_0000.")
        ])
    ]

    for i, (layer_title, layer_col, points) in enumerate(soc_layers):
        col = i % 3
        lx = Inches(0.8) + col * Inches(3.95)
        add_card(s6, lx, Inches(1.4), Inches(3.75), Inches(5.3), bg_color=C_WHITE, border_color=layer_col, border_width=2.0)
        tb_l = s6.shapes.add_textbox(lx + Inches(0.18), Inches(1.6), Inches(3.39), Inches(4.9))
        tf_l = tb_l.text_frame
        tf_l.word_wrap = True

        pt = tf_l.paragraphs[0]
        pt.text = layer_title
        pt.font.name = "Segoe UI"
        pt.font.size = Pt(12)
        pt.font.bold = True
        pt.font.color.rgb = layer_col
        pt.space_after = Pt(12)

        for p_lbl, p_val in points:
            p = tf_l.add_paragraph()
            p.text = f"• {p_lbl} {p_val}"
            p.font.name = "Segoe UI"
            p.font.size = Pt(10.5)
            p.font.color.rgb = C_TEXT_DARK
            p.space_after = Pt(8)
            p.line_spacing = 1.15

    # =========================================================================
    # SLIDE 7: PHẦN 4 - BLOCK DIAGRAM KIẾN TRÚC SOC PICORV32 (B&W DRAW.IO)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Phần 4: Sơ Đồ Khối Kiến Trúc", "Sơ Đồ Khối Kiến Trúc Vi Hệ Thống SoC PicoRV32 (Block Diagram Đen Trắng)", 7)

    if os.path.exists(img_fig1):
        add_card(s7, Inches(0.8), Inches(1.35), Inches(7.4), Inches(5.4), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
        s7.shapes.add_picture(img_fig1, Inches(0.9), Inches(1.45), Inches(7.2), Inches(5.2))

    rx7 = Inches(8.4)
    rw7 = Inches(4.13)
    add_card(s7, rx7, Inches(1.35), rw7, Inches(5.4), bg_color=C_WHITE, border_color=C_CARD_BORDER, border_width=1.5)
    tb_b7 = s7.shapes.add_textbox(rx7 + Inches(0.2), Inches(1.5), rw7 - Inches(0.4), Inches(5.1))
    tf_b7 = tb_b7.text_frame
    tf_b7.word_wrap = True

    pb1 = tf_b7.paragraphs[0]
    pb1.text = "CÁC KHỐI CHỨC NĂNG CỐT LÕI"
    pb1.font.name = "Segoe UI"
    pb1.font.size = Pt(13)
    pb1.font.bold = True
    pb1.font.color.rgb = C_BLUE_ACCENT
    pb1.space_after = Pt(10)

    b_points = [
        ("Nhân CPU PicoRV32 (Master):", "Cấu hình PROGADDR_RESET = 0x0025_0000, STACKADDR = 0x0000_0400, RV32I, bus chuẩn."),
        ("Khối bus soc_interconnect.v:", "Chứa logic giải mã sel_* hoàn chỉnh và ghép kênh dữ liệu rdata."),
        ("1KB Data SRAM (Slave 0):", "WORDS=256, < 0x0400, phản hồi sram_ready = 1 trong 1 chu kỳ clock cho Stack và biến."),
        ("Bộ điều khiển SPI Flash (Slave 1):", "spimemio.v chạy XIP (0x0010_0000..0x00FF_FFFF) và bit-bang SPI (0x0200_0000)."),
        ("Dual UART MMIO FIFO (Slaves 2 & 3):", "Khối u_rfid_uart đệm chuỗi thẻ RDM6300; khối u_host_uart giao tiếp PC."),
        ("Khối GPIO Status (Slave 4):", "Điều khiển 16 LED chẩn đoán nhịp tim và hiển thị kết quả phân quyền tại 0x4000_0000.")
    ]

    for p_lbl, p_val in b_points:
        p = tf_b7.add_paragraph()
        p.text = f"• {p_lbl} {p_val}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(6)
        p.line_spacing = 1.15

    # =========================================================================
    # SLIDE 8: PHẦN 5 - KHỐI LIÊN KẾT BUS SOC_INTERCONNECT.V (DRAW.IO DIAGRAM)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Phần 5: Khối Liên Kết Bus", "Khối soc_interconnect.v - Cầu Nối CPU, Flash XIP, SRAM & Ngoại Vi MMIO", 8)

    if os.path.exists(img_fig2):
        add_card(s8, Inches(0.8), Inches(1.35), Inches(7.4), Inches(5.4), bg_color=C_WHITE, border_color=C_AMBER, border_width=1.5)
        s8.shapes.add_picture(img_fig2, Inches(0.9), Inches(1.45), Inches(7.2), Inches(5.2))

    rx8 = Inches(8.4)
    rw8 = Inches(4.13)
    add_card(s8, rx8, Inches(1.35), rw8, Inches(5.4), bg_color=C_WHITE, border_color=C_CARD_BORDER, border_width=1.5)
    tb_b8 = s8.shapes.add_textbox(rx8 + Inches(0.2), Inches(1.5), rw8 - Inches(0.4), Inches(5.1))
    tf_b8 = tb_b8.text_frame
    tf_b8.word_wrap = True

    pb8 = tf_b8.paragraphs[0]
    pb8.text = "LOGIC ĐIỀU PHỐI BUS TRUNG TÂM"
    pb8.font.name = "Segoe UI"
    pb8.font.size = Pt(13)
    pb8.font.bold = True
    pb8.font.color.rgb = C_AMBER
    pb8.space_after = Pt(10)

    ic_points = [
        ("Mạch tổ hợp thuần túy:", "Giải mã địa chỉ hoàn toàn không tốn clock, đảm bảo trễ truyền dẫn cực thấp."),
        ("Bảo vệ truy xuất (Strobe Mask):", "Hỗ trợ cpu_mem_wstrb[3:0] ghi chính xác từng byte dữ liệu."),
        ("Cơ chế ghép kênh tập trung:", "cpu_mem_rdata được MUX chọn từ 5 nguồn tương ứng với tín hiệu sel_* đang tích cực."),
        ("Xử lý ngoại vi đồng bộ:", "Mọi ngoại vi MMIO (UART, GPIO) trả ready = 1 trong 1 clock, không bao giờ stall CPU."),
        ("Không gian XIP trong suốt:", "CPU đọc opcode từ Flash chip ngoài hệt như đang đọc từ bộ nhớ ROM nội bộ.")
    ]

    for p_lbl, p_val in ic_points:
        p = tf_b8.add_paragraph()
        p.text = f"• {p_lbl} {p_val}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(8)
        p.line_spacing = 1.15

    # =========================================================================
    # SLIDE 9: PHẦN 5 - CƠ CHẾ KÍCH HOẠT VÀ THỰC THI FIRMWARE C TRÊN PHẦN CỨNG
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Phần 5: Khối Liên Kết Bus", "Cơ Chế Kích Hoạt Và Điều Phối Thực Thi Firmware C Trên Phần Cứng", 9)

    exec_steps = [
        ("BƯỚC 1: BOOT XIP TỪ FLASH", C_BLUE_ACCENT, [
            ("Vector Reset:", "PROGADDR_RESET = 0x0025_0000 nằm trong dải Flash XIP."),
            ("Tự động giải mã:", "soc_interconnect bật sel_spimem, spimemio phát lệnh đọc 0x03 kéo mã máy từ Flash ngoài."),
            ("Không cần RAM lớn:", "Lệnh thực thi trực tiếp trên Flash, tiết kiệm tối đa diện tích silicon ASIC.")
        ]),
        ("BƯỚC 2: KHỞI TẠO STACK TRÊN SRAM", C_GREEN, [
            ("Đỉnh ngăn xếp (sp):", "Mã khởi động start.s gán con trỏ sp = 0x0000_0400 (đỉnh 1KB SRAM nội bộ)."),
            ("Truy xuất 1 chu kỳ clock:", "Mọi biến cục bộ, stack frame C truy xuất vùng < 0x0400 (sel_sram), sram_ready = 1 tức thì."),
            ("Tối ưu hóa hiệu năng:", "Loại bỏ hoàn toàn độ trễ đọc dữ liệu biến qua bus SPI, cho phép code C chạy tốc độ cao.")
        ]),
        ("BƯỚC 3: ĐIỀU KHIỂN NGOẠI VI MMIO", C_AMBER, [
            ("Con trỏ volatile trong C:", "Code C đọc/ghi thanh ghi qua macro volatile uint32_t* (soc_regs.h)."),
            ("Bắt tay trong suốt:", "Khi đọc REG_RFID_UART_DAT (0x1000_0004), interconnect bật sel_rfid lấy byte từ FIFO."),
            ("Chống nghẽn CPU:", "FIFO 32B đệm chuỗi thẻ tự động, CPU chỉ đọc khi rfid_ready tích cực.")
        ]),
        ("BƯỚC 4: CHẠY MÃ RAM GHI FLASH", C_PURPLE, [
            ("Xung đột Flash XIP:", "Flash không thể vừa phát lệnh đọc mã XIP vừa thực thi chu kỳ ghi/xóa Sector."),
            ("Chuyển vùng thực thi:", "flash.c sao chép routine flashio_worker lên Stack SRAM, CPU nhảy sang SRAM chạy."),
            ("Ghi xóa an toàn:", "Code chạy từ SRAM điều khiển 0x0200_0000 (sel_spicfg) bit-bang SPI an toàn 100%.")
        ])
    ]

    for i, (st_title, st_col, points) in enumerate(exec_steps):
        col = i % 2
        row = i // 2
        sx = Inches(0.8) + col * Inches(5.9)
        sy = Inches(1.4) + row * Inches(2.65)
        sw = Inches(5.6)
        sh = Inches(2.35)

        add_card(s9, sx, sy, sw, sh, bg_color=C_WHITE, border_color=st_col, border_width=2.0)
        tb_s = s9.shapes.add_textbox(sx + Inches(0.2), sy + Inches(0.15), sw - Inches(0.4), sh - Inches(0.3))
        tf_s = tb_s.text_frame
        tf_s.word_wrap = True

        pt = tf_s.paragraphs[0]
        pt.text = st_title
        pt.font.name = "Segoe UI"
        pt.font.size = Pt(12.5)
        pt.font.bold = True
        pt.font.color.rgb = st_col
        pt.space_after = Pt(8)

        for p_lbl, p_val in points:
            p = tf_s.add_paragraph()
            p.text = f"• {p_lbl} {p_val}"
            p.font.name = "Segoe UI"
            p.font.size = Pt(10.5)
            p.font.color.rgb = C_TEXT_DARK
            p.space_after = Pt(4)
            p.line_spacing = 1.15

    # =========================================================================
    # SLIDE 10: PHẦN 6 - CẦU NỐI MMIO: KHAI BÁO ĐỊA CHỈ SOC_REGS.H VS RTL
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Phần 6: Firmware C & Ánh Xạ MMIO", "Cầu Nối Phần Cứng - Phần Mềm: soc_regs.h vs soc_interconnect.v", 10)

    lines_c_regs = [
        "// firmware/common/soc_regs.h - MMIO Base Addresses",
        "#define REG_RFID_UART_DIV (*(volatile uint32_t*)0x10000000)",
        "#define REG_RFID_UART_DAT (*(volatile uint32_t*)0x10000004)",
        "#define REG_PC_UART_DIV   (*(volatile uint32_t*)0x30000000)",
        "#define REG_PC_UART_DAT   (*(volatile uint32_t*)0x30000004)",
        "#define REG_GPIO_LEDS     (*(volatile uint32_t*)0x40000000)",
        "",
        "// Flash Memory Partition",
        "#define USER_FLASH_ADDR    0x300000   // Sector 48 (64KB Whitelist)",
        "#define FLASH_RECORD_MAGIC 0x52464944 // Header 'RFID'",
        "#define LOG_FLASH_ADDR     0x310000   // Sector 49 (64KB Logs)",
        "#define LOG_MAGIC_SUCC     0x53554343 // Header 'SUCC'",
        "#define LOG_MAGIC_FAIL     0x4641494C // Header 'FAIL'"
    ]
    add_code_box(s10, Inches(0.8), Inches(1.35), Inches(5.7), Inches(4.3), "firmware/common/soc_regs.h", lines_c_regs)

    lines_rtl_ic = [
        "// rtl/core/soc_interconnect.v - Bus Decoding",
        "assign sel_sram   = cpu_mem_valid &&",
        "                    (cpu_mem_addr < 32'h0000_0400);",
        "assign sel_spimem = cpu_mem_valid &&",
        "                    (cpu_mem_addr >= 32'h0010_0000 &&",
        "                     cpu_mem_addr <  32'h0100_0000);",
        "assign sel_spicfg = cpu_mem_valid &&",
        "                    (cpu_mem_addr == 32'h0200_0000);",
        "assign sel_rfid   = cpu_mem_valid &&",
        "                    (cpu_mem_addr[31:28] == 4'h1);",
        "assign sel_uart   = cpu_mem_valid &&",
        "                    (cpu_mem_addr[31:28] == 4'h3);",
        "assign sel_gpio   = cpu_mem_valid &&",
        "                    (cpu_mem_addr[31:28] == 4'h4);"
    ]
    add_code_box(s10, Inches(6.8), Inches(1.35), Inches(5.73), Inches(4.3), "rtl/core/soc_interconnect.v", lines_rtl_ic)

    add_card(s10, Inches(0.8), Inches(5.8), Inches(11.733), Inches(1.05), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
    tb_c10 = s10.shapes.add_textbox(Inches(0.95), Inches(5.85), Inches(11.4), Inches(0.95))
    tf_c10 = tb_c10.text_frame
    tf_c10.word_wrap = True
    p_c10_1 = tf_c10.paragraphs[0]
    p_c10_1.text = "CƠ CHẾ LIÊN KẾT: TỪ CON TRỎ VOLATILE C ĐẾN CHU KỲ BUS PHẦN CỨNG"
    p_c10_1.font.name = "Segoe UI"
    p_c10_1.font.size = Pt(11)
    p_c10_1.font.bold = True
    p_c10_1.font.color.rgb = C_BLUE_ACCENT
    p_c10_1.space_after = Pt(2)

    p_c10_2 = tf_c10.add_paragraph()
    p_c10_2.text = "Khi C đọc/ghi *REG_RFID_UART_DAT (0x1000_0004), CPU phát cpu_mem_valid=1 & cpu_mem_addr. soc_interconnect so khớp tiền tố 0x1 kích hoạt sel_rfid, lấy 1 byte từ FIFO 32B trả về thanh ghi CPU trong suốt."
    p_c10_2.font.name = "Segoe UI"
    p_c10_2.font.size = Pt(10)
    p_c10_2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 11: PHẦN 6 - BẢNG ĐỐI CHIẾU CHU KỲ BUS THỰC TẾ (MASTER ROADMAP 8 ROWS)
    # =========================================================================
    all_rows_bus = [
        {
            "time": "T = 0",
            "task": "(Boot Flash XIP)",
            "rtl_file": "[rdm6300_picorv32_soc.v & soc_interconnect.v]",
            "rtl_code": "PROGADDR_RESET = 32'h0025_0000; | sel_spimem (0x0010_0000..0x00FF_FFFF)",
            "c_file": "[sections.lds & start.s]",
            "c_code": "FLASH (rx) : ORIGIN = 0x00250000 | _start",
            "meaning": "Cấu hình vector reset trỏ thẳng vào Flash SPI để CPU tự động nạp và thực thi trực tiếp opcode firmware (XIP) ngay sau khi nhả reset mà không cần nạp vào RAM."
        },
        {
            "time": "T = 1..100",
            "task": "(Tạo Stack RAM)",
            "rtl_file": "[picorv32.v & data_sram.v]",
            "rtl_code": "STACKADDR = 32'h0000_0400; | sel_sram (< 0x0400) | sram_ready = 1 (1 clock)",
            "c_file": "[start.s & sections.lds]",
            "c_code": "lui sp, %hi(_stack_top) (0x0400) | Copy .data & Zero .bss",
            "meaning": "C sử dụng không gian SRAM 1KB (< 0x0400) qua con trỏ ngăn xếp sp để cấp phát biến cục bộ, lưu stack frame và địa chỉ trả về hàm, phản hồi tức thì trong 1 chu kỳ clock."
        },
        {
            "time": "T = 101",
            "task": "(Vào hàm main)",
            "rtl_file": "[soc_interconnect.v & picorv32.v]",
            "rtl_code": "sel_spimem = 1 (Fetch Opcode Flash) + sel_sram = 1 (Stack Frame)",
            "c_file": "[start.s & main.c]",
            "c_code": "call main | int main(void) { access_control_init(); ... }",
            "meaning": "Chuyển giao quyền điều khiển từ assembly khởi động sang code C bậc cao. Hàm main() chạy trực tiếp từ Flash XIP, giải phóng toàn bộ 1KB SRAM chỉ dùng cho dữ liệu động."
        },
        {
            "time": "T = 105",
            "task": "(Set Baud Dual UART)",
            "rtl_file": "[soc_interconnect.v & uart_mmio.v]",
            "rtl_code": "sel_rfid (4'h1) & sel_uart (4'h3) | reg_div_sel (addr[2]==0) <= 5208",
            "c_file": "[soc_regs.h & access_control.c]",
            "c_code": "REG_RFID_UART_DIV = 5208; REG_PC_UART_DIV = 5208;",
            "meaning": "C ghi giá trị chia tần 5208 vào địa chỉ 0x10000000 và 0x30000000 để cài đặt tốc độ baud 9600 bps cho cả đầu đọc RFID RDM6300 và cổng máy tính PC (50 MHz / 9600)."
        },
        {
            "time": "T = 200",
            "task": "(Đọc thẻ RFID)",
            "rtl_file": "[uart_mmio.v & sync_fifo.v]",
            "rtl_code": "sel_rfid (4'h1) & reg_dat_sel (addr[2]==1) | rdata = fifo_empty ? 0xFFFFFFFF : byte",
            "c_file": "[soc_regs.h & access_control.c]",
            "c_code": "d = REG_RFID_UART_DAT (0x10000004); if (d == 0xFFFFFFFF) return -1;",
            "meaning": "C đọc từ 0x10000004 rút (pop) 1 byte từ FIFO 32B (đọc không khóa: trả về byte mã thẻ nếu có, hoặc trả về 0xFFFFFFFF nếu FIFO rỗng để CPU không bị nghẽn bus)."
        },
        {
            "time": "T = 250",
            "task": "(Giao tiếp PC UART)",
            "rtl_file": "[uart_mmio.v & sync_fifo.v]",
            "rtl_code": "sel_uart (4'h3) & reg_dat_sel (addr[2]==1) | Ghi TX FIFO / Đọc RX FIFO 32B",
            "c_file": "[soc_regs.h & uart.c]",
            "c_code": "REG_PC_UART_DAT (0x30000004) = c; | d = REG_PC_UART_DAT;",
            "meaning": "C ghi byte vào 0x30000004 để đẩy ký tự vào TX FIFO truyền lên Host PC, và đọc từ địa chỉ này để nhận chuỗi lệnh quản trị (Ping, thêm/xóa thẻ Whitelist, xuất log CSV)."
        },
        {
            "time": "T = 300",
            "task": "(Bật LED / Mở Cửa)",
            "rtl_file": "[soc_interconnect.v & soc_gpio_mmio.v]",
            "rtl_code": "sel_gpio (4'h4) | gpio_led_reg <= wdata | leds_o = gpio_led_reg",
            "c_file": "[soc_regs.h & access_control.c]",
            "c_code": "REG_GPIO_LEDS (0x40000000) = (REG_GPIO_LEDS & ~0x02) | 0x04;",
            "meaning": "C ghi giá trị bitmask vào 0x40000000 điều khiển 16 LED chẩn đoán trên bo mạch và đóng/ngắt relay mở chốt cửa điện từ (Bit 0: Alive 1Hz, Bit 1: Denied, Bit 2: Granted)."
        },
        {
            "time": "T = 400",
            "task": "(Ghi Flash từ RAM)",
            "rtl_file": "[soc_interconnect.v & spimemio.v]",
            "rtl_code": "sel_spicfg (0x0200_0000) | Điều khiển thủ công CSB, SCK, MOSI, MISO",
            "c_file": "[flash.c & start.s]",
            "c_code": "flashio(buf, len, 0x06); | flashio_worker: li t0, 0x02000000",
            "meaning": "Khi chạy từ SRAM, hàm của C phát lệnh bit-bang SPI vào 0x02000000 để xóa sector và ghi dữ liệu thẻ mới vào Flash Whitelist / Log mà không gây xung đột bus với các lệnh XIP."
        }
    ]
    s11 = add_bus_table_slide(11, "Bảng Đối Chiếu 8 Chu Kỳ Bus Thực Tế: Setting RTL, Code C & Ý Nghĩa Biến Địa Chỉ", all_rows_bus)

    # =========================================================================
    # SLIDE 12: ROW 1 - T = 0 (BOOT FLASH SPI XIP - VECTOR 0x0025_0000)
    # =========================================================================
    s12 = add_case_detail_slide(
        slide_num=12, case_idx=1, time_tag="T = 0", task_name="Khởi Động Reset & Nạp Opcode Flash SPI XIP",
        addr_info="0x0025_0000 (Flash XIP Entry Point)", bus_sig="sel_spimem = 1 | spimem_ready = 1",
        rtl_file="rtl/rdm6300_picorv32_soc.v & soc_interconnect.v (RTL)",
        rtl_lines=[
            "// 1. Cấu hình Vector Reset CPU PicoRV32:",
            "parameter [31:0] PROGADDR_RESET = 32'h0025_0000;",
            "",
            "// 2. soc_interconnect.v giải mã dải Flash XIP:",
            "assign sel_spimem = cpu_mem_valid &&",
            "       (cpu_mem_addr >= 32'h0010_0000 &&",
            "        cpu_mem_addr <  32'h0100_0000); // Khớp 0x0025_0000!",
            "",
            "// 3. spimemio.v tự động phát lệnh SPI FAST READ (0x03):",
            "assign cpu_mem_ready = spimem_ready;",
            "assign cpu_mem_rdata = spimem_rdata; // Opcode đầu tiên"
        ],
        rtl_desc=[
            "CPU PicoRV32 cấu hình PROGADDR_RESET = 0x0025_0000, nằm ngay sau phân vùng bitstream FPGA.",
            "soc_interconnect.v nhận địa chỉ 0x0025_0000, kích hoạt sel_spimem=1 chuyển giao cho spimemio.v.",
            "spimemio kéo 4 byte opcode đầu tiên từ chip Flash ngoài trả về CPU kèm spimem_ready=1."
        ],
        c_file="firmware/sections.lds & firmware/start.s (C / Asm)",
        c_lines=[
            "/* firmware/sections.lds - Linker Script */",
            "MEMORY {",
            "    FLASH (rx) : ORIGIN = 0x00250000, LENGTH = 0x000B0000",
            "    RAM  (rwx) : ORIGIN = 0x00000000, LENGTH = 0x00000400",
            "}",
            "SECTIONS {",
            "    .text : { *(.text.start) *(.text*) } > FLASH",
            "}",
            "",
            "/* firmware/start.s - Bootstrap Entry */",
            ".section .text.start",
            ".global _start",
            "_start: # Lệnh đầu tiên thực thi trực tiếp tại 0x00250000"
        ],
        c_desc=[
            "Linker script sections.lds quy định gốc phân vùng FLASH tại ORIGIN = 0x00250000.",
            "Đoạn mã khởi động _start trong start.s được đặt ngay tại địa chỉ này, khớp 100% với RTL.",
            "CPU thực thi lệnh C/Assembly trực tiếp trên Flash (XIP) ngay khi nhả reset mà không cần nạp vào RAM."
        ],
        why_title="Cơ Chế Boot XIP Trực Tiếp Từ Flash Ngoài (Execute-in-Place)",
        why_text="Bằng cách đặt vector reset 0x0025_0000 vào dải giải mã sel_spimem của spimemio.v, CPU PicoRV32 tự động kéo từng từ lệnh mã C từ chip Flash ngoài và thực thi tại chỗ (XIP). Giải pháp này loại bỏ hoàn toàn nhu cầu trang bị ROM Bootloader nội bộ hoặc chip RAM đắt đỏ trên vi mạch, tiết kiệm tối đa diện tích silicon ASIC SkyWater 130nm.",
        theme_color=C_BLUE_ACCENT
    )

    # =========================================================================
    # SLIDE 13: ROW 2 - T = 1..100 (KHỞI TẠO STACK 0x0000_0400 & 1KB SRAM)
    # =========================================================================
    s13 = add_case_detail_slide(
        slide_num=13, case_idx=2, time_tag="T = 1..100", task_name="Khởi Tạo Ngăn Xếp Stack sp & Vùng Nhớ SRAM 1KB",
        addr_info="0x0000_0400 (STACKADDR & Đỉnh 1KB SRAM)", bus_sig="sel_sram = 1 | sram_ready = 1 (1 chu kỳ clock)",
        rtl_file="rtl/core/picorv32.v & rtl/core/data_sram.v (RTL)",
        rtl_lines=[
            "// 1. Cấu hình Đỉnh Stack phần cứng trong picorv32.v:",
            "parameter [31:0] STACKADDR = 32'h0000_0400; // 1KB SRAM",
            "",
            "// 2. soc_interconnect.v giải mã truy xuất SRAM nội bộ:",
            "assign sel_sram = cpu_mem_valid &&",
            "                  (cpu_mem_addr < 32'h0000_0400);",
            "",
            "// 3. data_sram.v (256 từ x 32-bit = 1024 bytes):",
            "assign sram_ready = 1'b1; // Phản hồi tức thì 1 clock!",
            "always @(posedge clk) begin",
            "    if (sel_sram && (|wstrb)) mem[addr[9:2]] <= wdata;",
            "end"
        ],
        rtl_desc=[
            "Mọi chu kỳ bus truy xuất địa chỉ < 0x0400 được Interconnect định tuyến thẳng vào khối data_sram.v.",
            "Khối SRAM nội bộ phản hồi sram_ready = 1 trong đúng 1 chu kỳ clock, không tạo chu kỳ chờ (zero wait-state).",
            "Hỗ trợ phân chia wstrb[3:0] cho phép ghi chính xác từng byte biến cục bộ của chương trình C."
        ],
        c_file="firmware/start.s & firmware/sections.lds (C / Asm)",
        c_lines=[
            "/* firmware/start.s - Khởi tạo môi trường C */",
            "_start:",
            "    /* 1. Thiết lập con trỏ ngăn xếp sp = 0x00000400 */",
            "    lui  sp, %hi(_stack_top) # _stack_top = 0x0400",
            "    addi sp, sp, %lo(_stack_top)",
            "",
            "    /* 2. Sao chép phân vùng .data từ Flash lên SRAM */",
            "    la a0, __data_start; la a1, __data_end; la a2, __data_load",
            "copy_data_loop:",
            "    bge a0, a1, copy_done; lw t0, 0(a2); sw t0, 0(a0); ...",
            "",
            "    /* 3. Xóa trắng phân vùng .bss trong SRAM */",
            "zero_bss_loop: sw zero, 0(a0); addi a0, a0, 4; ..."
        ],
        c_desc=[
            "Con trỏ ngăn xếp sp được khởi tạo tại 0x0000_0400, phát triển giảm dần xuống để lưu stack frame C.",
            "Dữ liệu biến khởi tạo (.data) và biến toàn cục (.bss) được đưa trọn vẹn vào 1KB SRAM nội bộ.",
            "Các hàm C gọi đệ quy, cấp phát biến cục bộ đều thao tác siêu tốc trên đỉnh Stack SRAM này."
        ],
        why_title="Tối Ưu Hóa Hiệu Năng Truy Xuất Biến Và Stack C Với SRAM Zero-Wait-State",
        why_text="SRAM nội bộ phản hồi cực nhanh (1 chu kỳ clock) giúp CPU PicoRV32 thực thi các lệnh đọc/ghi biến cục bộ (lw/sw qua con trỏ sp) với tốc độ tối đa, khắc phục hoàn toàn độ trễ đọc của bus SPI ngoài. Việc phân vùng rõ ràng 1KB SRAM chỉ dành riêng cho dữ liệu động cho phép chạy trơn tru toàn bộ chương trình nhúng C.",
        theme_color=C_GREEN
    )

    # =========================================================================
    # SLIDE 14: ROW 3 - T = 101 (NHẢY VÀO HÀM MAIN() C TỪ FLASH XIP)
    # =========================================================================
    s14 = add_case_detail_slide(
        slide_num=14, case_idx=3, time_tag="T = 101", task_name="Chuyển Quyền Điều Khiển Sang Hàm main() C Từ Flash XIP",
        addr_info="0x0025_XXXX (Hàm main.c trong Flash XIP)", bus_sig="sel_spimem = 1 (Opcode) + sel_sram = 1 (Stack)",
        rtl_file="rtl/core/soc_interconnect.v & picorv32.v (RTL)",
        rtl_lines=[
            "// soc_interconnect.v phối hợp 2 kênh bus độc lập:",
            "assign sel_spimem = cpu_mem_valid &&",
            "       (cpu_mem_addr >= 32'h0010_0000 &&",
            "        cpu_mem_addr <  32'h0100_0000); // Lấy lệnh C",
            "",
            "assign sel_sram   = cpu_mem_valid &&",
            "       (cpu_mem_addr < 32'h0000_0400);  // Lưu Frame C",
            "",
            "// Bộ MUX ghép kênh trả lệnh Flash hoặc dữ liệu SRAM:",
            "assign cpu_mem_rdata = sel_sram   ? sram_rdata :",
            "                       sel_spimem ? spimem_rdata : ...;"
        ],
        rtl_desc=[
            "CPU PicoRV32 đọc opcode hàm C từ Flash XIP (sel_spimem), đồng thời đọc/ghi con trỏ $fp, $ra lên Stack SRAM (sel_sram).",
            "Interconnect phân luồng địa chỉ trong suốt giữa 2 vùng nhớ mà không gây xung đột tín hiệu bus.",
            "Nhân CPU duy trì chu kỳ lấy lệnh và chu kỳ dữ liệu xen kẽ mượt mà."
        ],
        c_file="firmware/start.s & firmware/main.c (C)",
        c_lines=[
            "/* firmware/start.s */",
            "    call main       # Lệnh nhảy từ Assembly sang hàm main() C",
            "hang: j hang        # Vòng lặp bẫy an toàn nếu main() kết thúc",
            "",
            "/* firmware/main.c - Vòng lặp nghiệp vụ chính */",
            "int main(void) {",
            "    system_init();",
            "    access_control_init();",
            "    uart_puts(\"\\n[SYSTEM] PicoRV32 RFID Access Control Ready.\\n\");",
            "    while (1) {",
            "        access_control_poll();   // Polling quét thẻ RDM6300",
            "        process_host_commands(); // Xử lý lệnh từ máy tính",
            "    }",
            "}"
        ],
        c_desc=[
            "Chuyển giao quyền điều khiển từ chuỗi khởi động sang logic ứng dụng C bậc cao.",
            "Toàn bộ thân hàm main(), access_control_poll() chạy trực tiếp từ Flash, giải phóng 100% SRAM cho biến động.",
            "Vòng lặp while(1) thực hiện luồng điều khiển kiểm soát vào ra vĩnh cửu không ngừng nghỉ."
        ],
        why_title="Bật Chế Độ Thực Thi Ứng Dụng C Hoàn Chỉnh Trên Nền Tảng RISC-V Freestanding",
        why_text="SoC PicoRV32 chạy môi trường C Freestanding (không cần hệ điều hành). Toàn bộ mã nguồn C được biên dịch thành tập lệnh RV32I thuần túy, định vị trong phân vùng Flash XIP. Sự phối hợp nhịp nhàng giữa spimemio kéo lệnh và SRAM lưu biến tạo thành nền tảng thực thi ứng dụng C ổn định, tiêu thụ cực ít năng lượng.",
        theme_color=C_BLUE_ACCENT
    )

    # =========================================================================
    # SLIDE 15: ROW 4 - T = 105 (CẤU HÌNH BAUD RATE DUAL UART MMIO)
    # =========================================================================
    s15 = add_case_detail_slide(
        slide_num=15, case_idx=4, time_tag="T = 105", task_name="Cấu Hình Tốc Độ Baud Dual UART MMIO (RFID & PC)",
        addr_info="0x1000_0000 (RFID_DIV) & 0x3000_0000 (PC_DIV)", bus_sig="sel_rfid = 1 (4'h1) & sel_uart = 1 (4'h3)",
        rtl_file="rtl/core/soc_interconnect.v & rtl/uart/uart_mmio.v (RTL)",
        rtl_lines=[
            "// 1. soc_interconnect.v giải mã tiền tố Base Address:",
            "assign sel_rfid = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h1);",
            "assign sel_uart = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h3);",
            "",
            "// 2. uart_mmio.v nạp thanh ghi chia tần tại Offset 0x00:",
            "wire reg_div_sel = valid && (addr[2] == 1'b0); // +0x00",
            "always @(posedge clk) begin",
            "    if (reg_div_sel && (|wstrb))",
            "        baud_div_reg <= wdata[15:0]; // Nạp 5208 (9600 baud)",
            "end",
            "assign ready = 1'b1; // Phản hồi trong 1 chu kỳ clock!"
        ],
        rtl_desc=[
            "Interconnect so khớp 4 bit cao addr[31:28] kích hoạt module u_rfid_uart hoặc u_host_uart.",
            "Offset 0x00 (addr[2] == 0) ghi giá trị xung nhịp chia tần vào thanh ghi prescaler phần cứng.",
            "Tín hiệu ready = 1 lập tức được trả về, chu kỳ ghi hoàn tất chỉ trong 1 chu kỳ xung nhịp 20 ns."
        ],
        c_file="firmware/common/soc_regs.h & firmware/app/access_control.c (C)",
        c_lines=[
            "/* firmware/common/soc_regs.h */",
            "#define REG_RFID_UART_DIV (*(volatile uint32_t*)0x10000000)",
            "#define REG_PC_UART_DIV   (*(volatile uint32_t*)0x30000000)",
            "",
            "/* firmware/app/access_control.c & drivers/uart.c */",
            "void access_control_init(void) {",
            "    if (REG_RFID_UART_DIV == 0) {",
            "        REG_RFID_UART_DIV = 5208; // 50 MHz / 9600 baud = 5208",
            "    }",
            "}",
            "void uart_init(uint32_t baud_div) {",
            "    REG_PC_UART_DIV = baud_div;   // Cài đặt 9600 baud cho Host PC",
            "}"
        ],
        c_desc=[
            "C sử dụng macro con trỏ volatile uint32_t* trỏ tới địa chỉ vật lý 0x10000000 và 0x30000000.",
            "Ghi giá trị 5208 để định chuẩn tốc độ truyền 9600 bps cho cả đầu đọc thẻ RFID và cổng nối tiếp máy tính.",
            "Từ khóa volatile ngăn chặn trình biên dịch GCC tối ưu loại bỏ lệnh ghi phần cứng quan trọng này."
        ],
        why_title="Cơ Chế Điều Khiển Ngoại Vi Trong Suốt Bằng Memory-Mapped I/O (MMIO)",
        why_text="Trình biên dịch C không cần tập lệnh I/O chuyên biệt; thao tác ghi biến REG_RFID_UART_DIV = 5208 được chuyển thành lệnh sw thông thường. soc_interconnect tự động định tuyến lệnh sw tới khối UART MMIO tương ứng. Mạch giải mã offset addr[2] tự động cập nhật thanh ghi chia tần baud rate trong đúng 1 chu kỳ clock.",
        theme_color=C_AMBER
    )

    # =========================================================================
    # SLIDE 16: ROW 5 - T = 200 (POLLING KHÔNG KHÓA NHẬN THẺ RFID 0x1000_0004)
    # =========================================================================
    s16 = add_case_detail_slide(
        slide_num=16, case_idx=5, time_tag="T = 200", task_name="Polling Không Khóa Nhận Dữ Liệu Thẻ RFID RDM6300",
        addr_info="0x1000_0004 (REG_RFID_UART_DAT - Đọc FIFO 32B)", bus_sig="sel_rfid = 1 | rfid_ready = 1 (Trả về Byte hoặc 0xFFFFFFFF)",
        rtl_file="rtl/uart/uart_mmio.v & rtl/uart/sync_fifo.v (RTL)",
        rtl_lines=[
            "// rtl/uart/uart_mmio.v - Offset 0x04 (addr[2] == 1):",
            "wire fifo_empty;",
            "assign rdata = fifo_empty ? 32'hFFFF_FFFF : {24'h0, fifo_rdata};",
            "",
            "// Tự động pop 1 byte khỏi FIFO khi CPU phát chu kỳ đọc hợp lệ:",
            "assign fifo_rd_en = reg_dat_sel && (!cpu_mem_wstrb) && (!fifo_empty);",
            "assign ready = 1'b1; // Luôn sẵn sàng trong 1 clock, không stall CPU!",
            "",
            "// rtl/uart/sync_fifo.v (Hàng đợi 32-Byte phần cứng):",
            "always @(posedge clk) begin",
            "    if (fifo_rd_en) rptr <= rptr + 1;",
            "end"
        ],
        rtl_desc=[
            "Khi C đọc 0x1000_0004, phần cứng kiểm tra cờ rỗng FIFO: nếu rỗng trả về 0xFFFFFFFF, nếu có dữ liệu trả về byte và tự động tăng con trỏ FIFO (Auto-POP).",
            "Tín hiệu rfid_ready = 1 lập tức được trả về, CPU không bao giờ bị nghẽn bus dù có thẻ hay không.",
            "Hàng đợi FIFO 32 byte tự động đệm toàn bộ chuỗi 14 byte từ RDM6300 mà không làm rơi byte nào."
        ],
        c_file="firmware/common/soc_regs.h & firmware/app/access_control.c (C)",
        c_lines=[
            "/* firmware/common/soc_regs.h */",
            "#define REG_RFID_UART_DAT (*(volatile uint32_t*)0x10000004)",
            "",
            "/* firmware/app/access_control.c - Đọc FIFO không khóa */",
            "static inline int rfid_uart_getc_nonblock(void) {",
            "    uint32_t d = REG_RFID_UART_DAT; // Đọc từ thanh ghi 0x10000004",
            "    if (d == 0xFFFFFFFF) return -1; // FIFO rỗng -> trả về ngay!",
            "    return (int)(d & 0xFF);         // Trả về byte ký tự ASCII hợp lệ",
            "}",
            "void access_control_poll(void) {",
            "    int ch;",
            "    while ((ch = rfid_uart_getc_nonblock()) >= 0) {",
            "        rdm6300_parse_byte((uint8_t)ch, &tag); // Đưa vào máy trạng thái",
            "    }",
            "}"
        ],
        c_desc=[
            "C đọc thăm dò (polling) không khóa: nếu không có thẻ, hàm thoát ngay lập tức trong vài chu kỳ clock.",
            "Khi người dùng quẹt thẻ, vòng lặp while rút từng byte trong FIFO nạp vào FSM giải mã gói tin 14 byte.",
            "Mã C chạy liên tục mượt mà, không bị hiện tượng treo cứng phần mềm (hang/deadlock)."
        ],
        why_title="Thiết Kế Đọc Phi Khóa (Non-Blocking Polling) Ngăn Ngừa Treo Nghẽn Bus CPU",
        why_text="Nếu phần cứng giữ chân cpu_mem_ready = 0 khi chưa có thẻ, nhân CPU PicoRV32 sẽ bị đóng băng (bus stall) không thể thực thi việc khác. Bằng cách thiết kế phần cứng trả về giá trị lính canh 0xFFFFFFFF kèm ready = 1 tức thì, tầng C kiểm tra điều kiện cực nhanh, cho phép CPU vừa quét thẻ vừa xử lý lệnh máy tính trơn tru.",
        theme_color=C_GREEN
    )

    # =========================================================================
    # SLIDE 17: ROW 6 - T = 250 (GIAO TIẾP MÁY TÍNH HOST PC UART 0x3000_0004)
    # =========================================================================
    s17 = add_case_detail_slide(
        slide_num=17, case_idx=6, time_tag="T = 250", task_name="Truyền Nhận Dữ Liệu Máy Tính Host PC UART (Console C)",
        addr_info="0x3000_0004 (REG_PC_UART_DAT - RX/TX FIFO 32B)", bus_sig="sel_uart = 1 | uart_ready = 1 (Giao tiếp Full-Duplex)",
        rtl_file="rtl/core/soc_interconnect.v & rtl/uart/uart_mmio.v (RTL)",
        rtl_lines=[
            "// rtl/uart/uart_mmio.v - u_host_uart:",
            "// Ghi (cpu_mem_wstrb != 0): Đẩy byte vào hàng đợi TX FIFO 32B:",
            "assign tx_fifo_wr_en = reg_dat_sel && (|cpu_mem_wstrb) && (!tx_fifo_full);",
            "assign tx_fifo_wdata = cpu_mem_wdata[7:0];",
            "",
            "// Đọc (cpu_mem_wstrb == 0): Rút byte từ hàng đợi RX FIFO 32B:",
            "assign rdata = rx_fifo_empty ? 32'hFFFF_FFFF : {24'h0, rx_fifo_rdata};",
            "assign rx_fifo_rd_en = reg_dat_sel && (!cpu_mem_wstrb) && (!rx_fifo_empty);",
            "assign ready = 1'b1; // Phản hồi trong 1 chu kỳ clock"
        ],
        rtl_desc=[
            "Module u_host_uart tích hợp 2 bộ đệm FIFO 32-byte độc lập cho hai chiều thu và phát dữ liệu.",
            "Thao tác ghi nạp byte vào TX FIFO để bộ phát baud phát tự động; thao tác đọc lấy byte từ RX FIFO.",
            "Hỗ trợ giao tiếp Full-Duplex 9600 bps hoàn chỉnh giữa vi mạch SoC và máy tính PC qua cổng USB-UART."
        ],
        c_file="firmware/common/soc_regs.h & firmware/drivers/uart.c (C)",
        c_lines=[
            "/* firmware/common/soc_regs.h */",
            "#define REG_PC_UART_DAT (*(volatile uint32_t*)0x30000004)",
            "",
            "/* firmware/drivers/uart.c - Trình điều khiển Host PC */",
            "void uart_putc(char c) {",
            "    REG_PC_UART_DAT = (uint32_t)(uint8_t)c; // Đẩy 1 ký tự vào TX FIFO",
            "}",
            "void uart_puts(const char *str) {",
            "    while (*str) { if (*str == '\\n') uart_putc('\\r'); uart_putc(*str++); }",
            "}",
            "int uart_getc_nonblock(void) {",
            "    uint32_t d = REG_PC_UART_DAT; // Đọc từ 0x30000004",
            "    return (d == 0xFFFFFFFF) ? -1 : (int)(d & 0xFF);",
            "}"
        ],
        c_desc=[
            "C gọi uart_puts() để truyền kết quả xác thực (ACCESS:GRANTED, ACCESS:DENIED) lên màn hình máy tính.",
            "C gọi uart_getc_nonblock() để nhận chuỗi lệnh quản trị ('P' Ping, 'W' lưu thẻ, 'L' xuất log CSV).",
            "Bộ đệm TX/RX FIFO 32-byte giúp C gửi nhận cả chuỗi văn bản dài mà không bị mất mát ký tự."
        ],
        why_title="Bộ Đệm FIFO 32 Byte Phần Cứng Giải Phóng Tốc Độ Xử Lý Cho CPU PicoRV32",
        why_text="Với tốc độ baud 9600 bps, mỗi byte truyền mất hơn 1 ms (rất chậm so với xung nhịp 50 MHz của CPU). Việc trang bị hàng đợi TX/RX FIFO 32 byte phần cứng cho phép CPU ghi liên tiếp một chuỗi ký tự dài vào FIFO trong vài chu kỳ nano-giây rồi quay lại làm việc khác, mạch UART phần cứng sẽ tự động rút và phát từng bit ra chân ngoài.",
        theme_color=C_BLUE_ACCENT
    )

    # =========================================================================
    # SLIDE 18: ROW 7 - T = 300 (ĐIỀU KHIỂN LED BÁO & RELAY CỬA GPIO MMIO 0x4000_0000)
    # =========================================================================
    s18 = add_case_detail_slide(
        slide_num=18, case_idx=7, time_tag="T = 300", task_name="Điều Khiển Đèn Báo LED & Rơ-Le Chốt Cửa GPIO MMIO",
        addr_info="0x4000_0000 (REG_GPIO_LEDS - 16 Ngõ Ra Chốt)", bus_sig="sel_gpio = 1 | gpio_ready = 1 (Chốt trong 1 clock)",
        rtl_file="rtl/core/soc_gpio_mmio.v & soc_interconnect.v (RTL)",
        rtl_lines=[
            "// rtl/core/soc_gpio_mmio.v",
            "reg [15:0] gpio_led_reg;",
            "always @(posedge clk or negedge resetn) begin",
            "    if (!resetn) gpio_led_reg <= 16'h0000;",
            "    else if (valid && (!ready) && (|wstrb)) begin",
            "        if (wstrb[0]) gpio_led_reg[7:0]  <= wdata[7:0];",
            "        if (wstrb[1]) gpio_led_reg[15:8] <= wdata[15:8];",
            "    end",
            "end",
            "assign leds_o = gpio_led_reg; // Đưa trực tiếp ra 16 chân pad ngoài",
            "assign ready  = valid;        // Phản hồi 1 chu kỳ clock"
        ],
        rtl_desc=[
            "soc_interconnect.v giải mã tiền tố 4'h4 (0x4000_0000) kích hoạt khối soc_gpio_mmio.v.",
            "Thanh ghi chốt 16-bit lưu trạng thái dữ liệu và đưa trực tiếp ra các chân pad vật lý leds_o[15:0].",
            "Chu kỳ ghi hoàn thành tức thì trong 1 xung nhịp clock, không tạo độ trễ cho CPU."
        ],
        c_file="firmware/common/soc_regs.h & firmware/app/access_control.c (C)",
        c_lines=[
            "/* firmware/common/soc_regs.h */",
            "#define REG_GPIO_LEDS (*(volatile uint32_t*)0x40000000)",
            "",
            "/* firmware/app/access_control.c */",
            "void access_control_process_card(const char *tag_hex, uint32_t hi, uint32_t lo) {",
            "    if (is_granted) {",
            "        // Bật Bit 2 (Mở chốt cửa / Relay ON), Tắt Bit 1 (Cảnh báo)",
            "        REG_GPIO_LEDS = (REG_GPIO_LEDS & ~0x0002) | 0x0004;",
            "    } else {",
            "        // Bật Bit 1 (LED đỏ cảnh báo), Tắt Bit 2 (Khóa cửa)",
            "        REG_GPIO_LEDS = (REG_GPIO_LEDS & ~0x0004) | 0x0002;",
            "    }",
            "}"
        ],
        c_desc=[
            "C thao tác toán tử bitwise (|, & ~) trên con trỏ 0x40000000 để cập nhật trạng thái thiết bị ngoại vi.",
            "Bit 0: Nhịp tim Alive (chớp tắt 1Hz trong hàm main); Bit 1: Cảnh báo từ chối; Bit 2: Mở chốt cửa điện từ.",
            "Tác động phần cứng trực tiếp, giúp người quản trị và người dùng quan sát kết quả xác thực tại chỗ."
        ],
        why_title="Điều Khiển Trực Tiếp Cơ Cấu Chấp Hành Vật Lý Với Độ Trễ Zero Nanosecond",
        why_text="Nhờ cơ chế ghi thanh ghi chốt GPIO MMIO tại địa chỉ 0x4000_0000 trong 1 chu kỳ clock (20 ns), tín hiệu mở chốt cửa điện từ và đèn báo LED được kích hoạt tức thì ngay khi thuật toán xác thực C ra quyết định. Không tồn tại bất kỳ độ trễ phần mềm hay trễ truyền thông nào giữa logic quyết định và cơ cấu chấp hành.",
        theme_color=C_ROSE
    )

    # =========================================================================
    # SLIDE 19: ROW 8 - T = 400 (GHI / XÓA FLASH SECTOR WHITELIST TỪ SRAM)
    # =========================================================================
    s19 = add_case_detail_slide(
        slide_num=19, case_idx=8, time_tag="T = 400", task_name="Ghi / Xóa Flash Sector Whitelist 0x0200_0000 Từ SRAM",
        addr_info="0x0200_0000 (SPICFG) & 0x0030_0000 (Sector 48)", bus_sig="sel_spicfg = 1 | Điều khiển thủ công CSB, SCK, IO[3:0]",
        rtl_file="rtl/core/soc_interconnect.v & rtl/core/spimemio.v (RTL)",
        rtl_lines=[
            "// 1. soc_interconnect.v kích hoạt thanh ghi SPICFG:",
            "assign sel_spicfg = cpu_mem_valid &&",
            "                    (cpu_mem_addr == 32'h0200_0000);",
            "",
            "// 2. spimemio.v chuyển giao quyền điều khiển chân SPI cho CPU:",
            "// bit 8: CSB, bit 0: SCK, bit 1: IO0 (MOSI), bit 2: IO1 (MISO)",
            "// Cho phép CPU nạp lệnh WREN (0x06), Block Erase (0xD8), Page Prog (0x02):",
            "assign flash_csb = sel_spicfg ? spicfg_reg[8] : spimem_csb;",
            "assign flash_clk = sel_spicfg ? spicfg_reg[0] : spimem_clk;"
        ],
        rtl_desc=[
            "Địa chỉ đặc biệt 0x0200_0000 kích hoạt chế độ cấu hình SPI trực tiếp (Bit-Bang SPI Configuration).",
            "CPU trực tiếp làm chủ các đường tín hiệu vật lý của chip Flash ngoài để thực hiện chu kỳ ghi/xóa.",
            "Cơ chế này tách biệt hoàn toàn với chế độ đọc XIP, ngăn chặn xung đột bus phần cứng."
        ],
        c_file="firmware/drivers/flash.c & firmware/boot/start.s (C / Asm)",
        c_lines=[
            "/* firmware/drivers/flash.c - Nạp worker lên Stack SRAM */",
            "static void flashio(uint8_t *data, int len, uint8_t wrencmd) {",
            "    uint32_t func[&flashio_worker_end - &flashio_worker_begin];",
            "    uint32_t *src = &flashio_worker_begin, *dst = func;",
            "    while (src != &flashio_worker_end) *(dst++) = *(src++);",
            "    ((void(*)(uint8_t*, uint32_t, uint32_t))func)(data, len, wrencmd);",
            "}",
            "",
            "/* firmware/boot/start.s - flashio_worker (Chạy trong SRAM) */",
            "flashio_worker_begin:",
            "    li   t0, 0x02000000  # Trỏ thanh ghi SPICFG trong RTL",
            "    li   t1, 0x120       # CS=1, IO0=output",
            "    sh   t1, 0(t0)       # Gửi lệnh SPI Bit-bang xóa/ghi Flash"
        ],
        c_desc=[
            "Hàm flashio() sao chép đoạn code máy flashio_worker từ Flash lên vùng Stack SRAM nội bộ và nhảy sang chạy.",
            "Khi đang chạy trên SRAM (không đọc XIP), CPU điều khiển 0x0200_0000 ghi thẻ mới vào Sector 48 (0x300000).",
            "Sau khi hoàn tất chu kỳ ghi/xóa Flash, CPU an toàn nhảy ngược về không gian XIP để tiếp tục chạy."
        ],
        why_title="Giải Quyết Xung Đột Bus XIP Bằng Cơ Chế Nạp Động Routine Lên SRAM (In-SRAM Execution)",
        why_text="Chip SPI NOR Flash không thể vừa đọc mã lệnh XIP vừa thực thi chu kỳ ghi/xóa Sector. Để giải quyết triệt để xung đột này, hệ thống nạp động routine flashio_worker lên 1KB SRAM nội bộ. CPU thực thi từ SRAM để ghi/xóa Flash an toàn 100%, sau đó quay lại không gian XIP mà không gây lỗi bus hay treo hệ thống.",
        theme_color=C_PURPLE
    )

    # =========================================================================
    # SLIDE 20: PHẦN 7 - HỆ THỐNG TESTBENCH: UART RTL (TB_UART_RTL.V)
    # =========================================================================
    s20 = prs.slides.add_slide(blank_layout)
    add_header(s20, "Phần 7: Hệ Thống Testbench", "Testbench 1: Kiểm Thử Phần Cứng RTL Thuần Cho UART MMIO & FIFO (tb_uart_rtl.v)", 20)

    lx20 = Inches(0.8)
    lw20 = Inches(5.7)
    add_card(s20, lx20, Inches(1.35), lw20, Inches(5.4), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
    tb_l20 = s20.shapes.add_textbox(lx20 + Inches(0.2), Inches(1.5), lw20 - Inches(0.4), Inches(5.1))
    tf_l20 = tb_l20.text_frame
    tf_l20.word_wrap = True

    pt20 = tf_l20.paragraphs[0]
    pt20.text = "5 KỊCH BẢN KIỂM THỬ UART RTL THUẦN"
    pt20.font.name = "Segoe UI"
    pt20.font.size = Pt(13)
    pt20.font.bold = True
    pt20.font.color.rgb = C_BLUE_ACCENT
    pt20.space_after = Pt(10)

    tb_uart_scenarios = [
        ("Mục tiêu:", "Xác minh tính đúng đắn phần cứng của uart_mmio.v, sync_fifo.v và simpleuart.v mà không cần CPU."),
        ("1. Default Divider:", "Kiểm tra thanh ghi Prescaler tại offset 0x00 nạp đúng giá trị mặc định 5208 (9600 baud @ 50MHz)."),
        ("2. Divider Reconfig:", "Ghi giá trị chia tần mới và đọc lại qua bus MMIO, xác nhận mạch thanh ghi hoạt động chuẩn xác."),
        ("3. Serial TX Waveform:", "Ghi ký tự vào offset 0x04, kiểm tra dạng sóng nối tiếp tx_o (Start bit = 0, 8 data bits LSB-first, Stop bit = 1)."),
        ("4. Serial RX & FIFO:", "Bắn chuỗi bit vào rx_i, cờ rx_activity_o tích cực, kiểm tra dữ liệu nạp vào FIFO và trả về 0xFFFFFFFF khi rỗng."),
        ("5. Multi-Byte Burst:", "Bắn liên tiếp chuỗi byte kiểm tra cơ chế chống tràn của hàng đợi FIFO 32 byte.")
    ]

    for p_lbl, p_val in tb_uart_scenarios:
        p = tf_l20.add_paragraph()
        p.text = f"• {p_lbl} {p_val}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(8)
        p.line_spacing = 1.15

    rx20 = Inches(6.8)
    rw20 = Inches(5.73)
    code_lines_20 = [
        "Vivado Simulator v2025.1 - xelab & xsim",
        "Analyzing Verilog file rtl/uart/sync_2ff.v",
        "Analyzing Verilog file rtl/uart/sync_fifo.v",
        "Analyzing Verilog file rtl/uart/simpleuart.v",
        "Analyzing Verilog file rtl/uart/uart_mmio.v",
        "Analyzing Verilog file tb/tb_uart_rtl.v",
        "",
        "[TEST 1] Checking Default Prescaler Divider...",
        "  [PASS] Prescaler default matches DEFAULT_DIV = 5208",
        "[TEST 2] Reconfiguring Divider to 10416 (4800 baud)...",
        "  [PASS] Read-back matches written value 10416",
        "[TEST 3] Transmitting Byte 0x55 ('U') over TX...",
        "  [PASS] TX Waveform matches 9600-8-N-1 timing!",
        "[TEST 4] Receiving Serial Byte 0xA5 into FIFO...",
        "  [PASS] rx_activity_o asserted! Read 0xA5 cleanly!",
        "  [PASS] FIFO Empty flag returns 0xFFFFFFFF",
        "[TEST 5] Multi-Byte Burst Test (16 bytes)...",
        "  [PASS] All 16 bytes drained without data corruption!"
    ]
    add_code_box(s20, rx20, Inches(1.35), rw20, Inches(5.4), "tb/run_sim_uart.bat output", code_lines_20, "=== UART RTL TESTBENCH: 100% PASS ===")

    # =========================================================================
    # SLIDE 21: PHẦN 7 - HỆ THỐNG TESTBENCH: TOP SOC BOOT & PING (TB_UART_PING.V)
    # =========================================================================
    s21 = prs.slides.add_slide(blank_layout)
    add_header(s21, "Phần 7: Hệ Thống Testbench", "Testbench 2: Kiểm Thử Tích Hợp Toàn Diện Top SoC Boot Flash & Ping (tb_uart_ping.v)", 21)

    lx21 = Inches(0.8)
    lw21 = Inches(5.7)
    add_card(s21, lx21, Inches(1.35), lw21, Inches(5.4), bg_color=C_WHITE, border_color=C_GREEN, border_width=1.5)
    tb_l21 = s21.shapes.add_textbox(lx21 + Inches(0.2), Inches(1.5), lw21 - Inches(0.4), Inches(5.1))
    tf_l21 = tb_l21.text_frame
    tf_l21.word_wrap = True

    pt21 = tf_l21.paragraphs[0]
    pt21.text = "5 KỊCH BẢN KIỂM THỬ TÍCH HỢP TOP SOC"
    pt21.font.name = "Segoe UI"
    pt21.font.size = Pt(13)
    pt21.font.bold = True
    pt21.font.color.rgb = C_GREEN
    pt21.space_after = Pt(10)

    tb_soc_scenarios = [
        ("Mục tiêu:", "Xác minh hệ thống Top-level hoàn chỉnh gồm CPU PicoRV32, spimemio, 1KB SRAM, Interconnect và UART."),
        ("1. Power-On Reset & Boot Flash:", "PicoRV32 thức dậy tại 0x0025_0000, spimemio kéo từng từ lệnh mã C từ firmware.hex qua XIP."),
        ("2. C Startup Banner:", "CPU thực thi mã C trong main.c, khởi tạo ngoại vi và in toàn bộ chuỗi chào mừng ra UART."),
        ("3. Host Ping Processing:", "Testbench đóng vai trò PC Host gửi byte lệnh 'P' (0x50) và '\\n' (0x0A) qua cổng nối tiếp."),
        ("4. Response Verification:", "CPU phản hồi chuỗi 'PONG: PicoRV32 Active', testbench so khớp từng ký tự."),
        ("5. CPU Health & Zero-Trap:", "Khẳng định tín hiệu cpu_trap == 0 xuyên suốt quá trình chạy, không bị illegal instruction hay tràn RAM.")
    ]

    for p_lbl, p_val in tb_soc_scenarios:
        p = tf_l21.add_paragraph()
        p.text = f"• {p_lbl} {p_val}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(8)
        p.line_spacing = 1.15

    rx21 = Inches(6.8)
    rw21 = Inches(5.73)
    code_lines_21 = [
        "Vivado Simulator v2025.1 - xelab & xsim",
        "Analyzing Verilog file rtl/rdm6300_picorv32_soc.v",
        "Analyzing Verilog file tb/tb_uart_ping.v",
        "",
        "[BOOT] Releasing CPU Reset...",
        "[BOOT] PicoRV32 woke up at 0x00250000 (Flash XIP)",
        "[EXEC] Loading instructions from firmware.hex...",
        "[UART] Detected Startup Banner:",
        "  ================================================",
        "    RDM6300 PICORV32 SOC ACCESS CONTROLLER READY  ",
        "  ================================================",
        "[HOST] Sending Host Command: 'P' (Ping)...",
        "[RECV] CPU Response received via UART:",
        "  PONG: PicoRV32 Active",
        "[VERIFY] String matches expected response!",
        "[ASSERT] Checking cpu_trap signal...",
        "  cpu_trap == 0 (CONFIRMED: ZERO CPU TRAPS!)"
    ]
    add_code_box(s21, rx21, Inches(1.35), rw21, Inches(5.4), "tb/run_sim_ping.bat output", code_lines_21, "=== TOP SOC PING TESTBENCH: 100% PASS ===")

    # =========================================================================
    # SLIDE 22: PHẦN 8 - DEMO THỰC NGHIỆM TRÊN FPGA BASYS 3: THIẾT LẬP KẾT NỐI
    # =========================================================================
    s22 = prs.slides.add_slide(blank_layout)
    add_header(s22, "Phần 8: Demo Chức Năng Sản Phẩm", "Kiểm Chứng Thực Nghiệm Trên FPGA Basys 3: Thiết Lập Kết Nối Phần Cứng", 22)

    demo_setup_cards = [
        ("KẾT NỐI ĐẦU ĐỌC RFID RDM6300", C_AMBER, [
            ("Cổng PMOD JA trên Basys 3:", "Cắm module RDM6300 trực tiếp vào cổng PMOD JA."),
            ("Chân JA1 (Pin J1 FPGA):", "Nhận luồng dữ liệu UART TX 9600-8-N-1 từ RDM6300."),
            ("Nguồn cấp 5V & GND:", "Lấy trực tiếp từ chân VCC/GND của cổng PMOD bo mạch."),
            ("Ăng-ten cuộn cảm rời:", "Đặt cách ly chống nhiễu từ trường với các linh kiện số trên bo mạch.")
        ]),
        ("KẾT NỐI MÁY TÍNH HOST PC", C_BLUE_ACCENT, [
            ("Cáp Micro-USB tiêu chuẩn:", "Vừa cấp nguồn +5V DC vừa mở cổng COM ảo qua chip FTDI."),
            ("Tốc độ baud 9600 bps:", "Giao tiếp Full-Duplex tin cậy giữa máy tính và SoC PicoRV32."),
            ("Phần mềm Host Console C:", "Giao diện dòng lệnh tương tác 11 chức năng quản trị cơ sở dữ liệu thẻ."),
            ("Trích xuất dữ liệu tự động:", "Tự động sao lưu lịch sử quẹt thẻ ra file CSV trên máy tính.")
        ]),
        ("ĐIỀU KHIỂN FLASH & HIỂN THỊ LED", C_PURPLE, [
            ("Nguyên thủy STARTUPE2:", "Đưa xung nhịp Flash SCK vào USRCCLKO để làm chủ chân CCLK nối tới chip Flash."),
            ("Chip Flash Spansion S25FL032P:", "Lưu trữ bền vững danh mục Whitelist (Sector 48) và Access Logs (Sector 49)."),
            ("LED[0] (Heartbeat):", "Nhấp nháy 1 Hz báo hiệu CPU PicoRV32 đang hoạt động bình thường."),
            ("LED[1] & LED[2]:", "LED[1] sáng khi chip Flash đang bận ghi; LED[2] sáng khi quẹt thẻ hợp lệ.")
        ])
    ]

    for i, (ds_title, ds_col, points) in enumerate(demo_setup_cards):
        dx = Inches(0.8) + i * Inches(3.95)
        add_card(s22, dx, Inches(1.4), Inches(3.75), Inches(5.3), bg_color=C_WHITE, border_color=ds_col, border_width=2.0)
        tb_d = s22.shapes.add_textbox(dx + Inches(0.18), Inches(1.6), Inches(3.39), Inches(4.9))
        tf_d = tb_d.text_frame
        tf_d.word_wrap = True

        pt = tf_d.paragraphs[0]
        pt.text = ds_title
        pt.font.name = "Segoe UI"
        pt.font.size = Pt(12)
        pt.font.bold = True
        pt.font.color.rgb = ds_col
        pt.space_after = Pt(12)

        for p_lbl, p_val in points:
            p = tf_d.add_paragraph()
            p.text = f"• {p_lbl} {p_val}"
            p.font.name = "Segoe UI"
            p.font.size = Pt(10.5)
            p.font.color.rgb = C_TEXT_DARK
            p.space_after = Pt(8)
            p.line_spacing = 1.15

    # =========================================================================
    # SLIDE 23: PHẦN 8 - DEMO THỰC NGHIỆM TRÊN FPGA BASYS 3: CÁC KỊCH BẢN THỰC TẾ
    # =========================================================================
    s23 = prs.slides.add_slide(blank_layout)
    add_header(s23, "Phần 8: Demo Chức Năng Sản Phẩm", "Các Kịch Bản Thực Nghiệm Quẹt Thẻ Thực Tế Trên FPGA Basys 3", 23)

    demo_cases = [
        ("KỊCH BẢN 1: PING PHẦN CỨNG", C_BLUE_ACCENT, [
            ("Thao tác:", "Chọn menu [1] trên Host Console gửi lệnh 'P'."),
            ("Kết quả:", "PicoRV32 phản hồi ngay 'PONG: PicoRV32 Active'."),
            ("Ý nghĩa:", "Khẳng định CPU, Interconnect và UART hoạt động thông suốt.")
        ]),
        ("KỊCH BẢN 2: THẺ CHƯA ĐĂNG KÝ", C_ROSE, [
            ("Thao tác:", "Quẹt thẻ thật 0007508976 chưa có trong Flash."),
            ("Phản hồi:", "Hệ thống bóc tách UID 00007293F0 -> 'ACCESS:DENIED'."),
            ("Tác động:", "Nháy LED đỏ cảnh báo, ghi vết FAIL vào Flash Sector 49.")
        ]),
        ("KỊCH BẢN 3: ĐĂNG KÝ THẺ VÀO FLASH", C_AMBER, [
            ("Thao tác:", "Chọn menu [2] nhập 10 số in trên thẻ (0007508976)."),
            ("Xử lý:", "CPU nạp flashio_worker vào SRAM ghi vào Sector 48."),
            ("Kết quả:", "Lưu thành công tại Slot #0 (0x300000), nháy LED Flash.")
        ]),
        ("KỊCH BẢN 4: QUẸT THẺ HỢP LỆ", C_GREEN, [
            ("Thao tác:", "Quẹt lại thẻ 0007508976 lên đầu đọc RDM6300."),
            ("Phản hồi:", "SoC tra cứu trúng Slot #0 -> 'ACCESS:GRANTED'."),
            ("Tác động:", "Bật sáng LED xanh mở cửa, ghi vết SUCC vào Flash Sector 49.")
        ])
    ]

    for i, (dc_title, dc_col, points) in enumerate(demo_cases):
        col = i % 2
        row = i // 2
        cx = Inches(0.8) + col * Inches(5.9)
        cy = Inches(1.4) + row * Inches(2.65)
        cw = Inches(5.6)
        ch = Inches(2.35)

        add_card(s23, cx, cy, cw, ch, bg_color=C_WHITE, border_color=dc_col, border_width=2.0)
        tb_c = s23.shapes.add_textbox(cx + Inches(0.2), cy + Inches(0.15), cw - Inches(0.4), ch - Inches(0.3))
        tf_c = tb_c.text_frame
        tf_c.word_wrap = True

        pt = tf_c.paragraphs[0]
        pt.text = dc_title
        pt.font.name = "Segoe UI"
        pt.font.size = Pt(12.5)
        pt.font.bold = True
        pt.font.color.rgb = dc_col
        pt.space_after = Pt(8)

        for p_lbl, p_val in points:
            p = tf_c.add_paragraph()
            p.text = f"• {p_lbl} {p_val}"
            p.font.name = "Segoe UI"
            p.font.size = Pt(10.5)
            p.font.color.rgb = C_TEXT_DARK
            p.space_after = Pt(4)
            p.line_spacing = 1.15

    # =========================================================================
    # SLIDE 24: PHẦN 9 - THIẾT KẾ VẬT LÝ ASIC: LUỒNG OPENLANE 2 (SKYWATER 130NM)
    # =========================================================================
    s24 = prs.slides.add_slide(blank_layout)
    add_header(s24, "Phần 9: Thiết Kế Vật Lý ASIC", "Quy Trình Thiết Kế Vật Lý Vi Mạch RTL-to-GDSII Trên OpenLane 2", 24)

    lx24 = Inches(0.8)
    lw24 = Inches(5.7)
    code_lines_24 = [
        '{',
        '  "DESIGN_NAME": "rdm6300_picorv32_soc",',
        '  "PDK": "sky130A",',
        '  "STD_CELL_LIBRARY": "sky130_fd_sc_hd",',
        '  "CLOCK_PORT": "clk",',
        '  "CLOCK_PERIOD": 20.0, // 50 MHz',
        '  "FP_CORE_UTIL": 26,   // 26% density',
        '  "MAX_FANOUT_CONSTRAINT": 12,',
        '  "PL_RESIZER_HOLD_SLACK_MARGIN": 0.6,',
        '  "RUN_HEURISTIC_DIODE_INSERTION": true,',
        '  "HEURISTIC_ANTENNA_THRESHOLD": 24,',
        '  "GRT_ANTENNA_ITERS": 35,',
        '  "RUN_ANTENNA_REPAIR": true,',
        '  "SYNTH_STRATEGY": "AREA 0"',
        '}'
    ]
    add_code_box(s24, lx24, Inches(1.35), lw24, Inches(5.4), "Cấu hình config.json chính thức", code_lines_24)

    rx24 = Inches(6.8)
    rw24 = Inches(5.73)
    add_card(s24, rx24, Inches(1.35), rw24, Inches(5.4), bg_color=C_WHITE, border_color=C_ROSE, border_width=2.0)
    tb_r24 = s24.shapes.add_textbox(rx24 + Inches(0.2), Inches(1.5), rw24 - Inches(0.4), Inches(5.1))
    tf_r24 = tb_r24.text_frame
    tf_r24.word_wrap = True

    pr24 = tf_r24.paragraphs[0]
    pr24.text = "CÁC CHIẾN LƯỢC VẬT LÝ THEN CHỐT"
    pr24.font.name = "Segoe UI"
    pr24.font.size = Pt(13)
    pr24.font.bold = True
    pr24.font.color.rgb = C_ROSE
    pr24.space_after = Pt(10)

    asic_strategies = [
        ("Mật độ diện tích lõi 26% (FP_CORE_UTIL):", "Khởi tạo mật độ cell 26%, để lại 74% diện tích cho các kênh định tuyến kim loại và chèn diode bảo vệ plasma."),
        ("Ràng buộc xung nhịp 50 MHz (CLOCK_PERIOD = 20.0 ns):", "Ràng buộc định thời thống nhất từ khâu tổng hợp logic Yosys, xây dựng cây clock CTS tới khâu phân tích định thời tĩnh STA."),
        ("Chèn Diode phỏng đoán (HEURISTIC_ANTENNA_THRESHOLD = 24):", "Thuật toán tối ưu tự động chèn diode tiêu tán điện tích plasma khi tỷ lệ dây/cực cổng vượt ngưỡng 24, triệt tiêu 100% lỗi Antenna."),
        ("Biên an toàn Hold Guard-band 0.60 ns:", "Đảm bảo bộ tối ưu hóa tế bào Resizer xử lý sạch sẽ các vi phạm chạy đua dữ liệu (Hold Violations) sau bước đi dây chi tiết.")
    ]

    for p_lbl, p_val in asic_strategies:
        p = tf_r24.add_paragraph()
        p.text = f"• {p_lbl} {p_val}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(8)
        p.line_spacing = 1.15

    # =========================================================================
    # SLIDE 25: PHẦN 9 - THIẾT KẾ VẬT LÝ ASIC: BẢN VẼ LAYOUT & KÝ DUYỆT SIGN-OFF
    # =========================================================================
    s25 = prs.slides.add_slide(blank_layout)
    add_header(s25, "Phần 9: Thiết Kế Vật Lý ASIC", "Bản Vẽ Layout OpenROAD & Báo Cáo Ký Duyệt Sign-off Toàn Diện", 25)

    if os.path.exists(img_openroad):
        add_card(s25, Inches(0.8), Inches(1.35), Inches(5.7), Inches(4.3), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
        s25.shapes.add_picture(img_openroad, Inches(0.9), Inches(1.45), Inches(5.5), Inches(4.1))

    if os.path.exists(img_signoff):
        add_card(s25, Inches(6.8), Inches(1.35), Inches(5.73), Inches(4.3), bg_color=C_WHITE, border_color=C_GREEN, border_width=1.5)
        s25.shapes.add_picture(img_signoff, Inches(6.9), Inches(1.45), Inches(5.53), Inches(4.1))

    add_card(s25, Inches(0.8), Inches(5.8), Inches(11.733), Inches(1.05), bg_color=C_WHITE, border_color=C_CARD_BORDER, border_width=1.5)
    tb_c25 = s25.shapes.add_textbox(Inches(0.95), Inches(5.85), Inches(11.4), Inches(0.95))
    tf_c25 = tb_c25.text_frame
    tf_c25.word_wrap = True

    p_c25_1 = tf_c25.paragraphs[0]
    p_c25_1.text = "KẾT QUẢ KÝ DUYỆT TAPE-OUT READY: 0 ANTENNA | 0 LVS | 0 DRC | MET TIMING 50 MHZ"
    p_c25_1.font.name = "Segoe UI"
    p_c25_1.font.size = Pt(11)
    p_c25_1.font.bold = True
    p_c25_1.font.color.rgb = C_GREEN
    p_c25_1.space_after = Pt(2)

    p_c25_2 = tf_c25.add_paragraph()
    p_c25_2.text = "• Bố cục vật lý: Lưới nguồn PDN met4/met5 dày đặc, phân bổ 31 chân pad đối xứng trên 4 cạnh die, độ sụt áp IR drop < 1.5% an toàn.\\n• Định thời & Ký duyệt: WNS >= 0.00 ns tại 50 MHz trên cả 9 góc đo công nghệ từ -40°C đến 100°C; Netgen xác nhận 100% khớp netlist RTL."
    p_c25_2.font.name = "Segoe UI"
    p_c25_2.font.size = Pt(9.5)
    p_c25_2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 26: TỔNG KẾT ĐỀ TÀI & HƯỚNG PHÁT TRIỂN (THANK YOU SLIDE)
    # =========================================================================
    s26 = prs.slides.add_slide(blank_layout)
    bg26 = s26.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg26.fill.solid()
    bg26.fill.fore_color.rgb = C_NAVY_DARK
    bg26.line.fill.background()

    card26 = s26.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
    card26.fill.solid()
    card26.fill.fore_color.rgb = C_NAVY_MID
    card26.line.color.rgb = C_BLUE_ACCENT
    card26.line.width = Pt(2.0)

    tb_t26 = s26.shapes.add_textbox(Inches(1.2), Inches(1.1), Inches(10.9), Inches(5.3))
    tf_t26 = tb_t26.text_frame
    tf_t26.word_wrap = True

    p_end1 = tf_t26.paragraphs[0]
    p_end1.text = "TỔNG KẾT ĐỒ ÁN VÀ CÁC ĐÓNG GÓP NỔI BẬT"
    p_end1.font.name = "Segoe UI"
    p_end1.font.size = Pt(22)
    p_end1.font.bold = True
    p_end1.font.color.rgb = C_CYAN_ACCENT
    p_end1.space_after = Pt(16)

    contributions = [
        ("1. Tự chủ thiết kế kiến trúc SoC:", "Xây dựng hoàn chỉnh vi mạch tích hợp CPU RISC-V PicoRV32, cầu nối bus trung tâm soc_interconnect.v, 1KB SRAM, bộ điều khiển SPI Flash spimemio.v và ngoại vi UART FIFO."),
        ("2. Tối ưu hóa kiến trúc thực thi nhúng:", "Hiện thực hóa cơ chế thực thi XIP từ SPI Flash kết hợp nạp động routine flashio_worker vào 1KB SRAM để ghi/xóa cơ sở dữ liệu Whitelist và nhật ký Access Log không xung đột bus."),
        ("3. Kiểm chứng thực nghiệm 100%:", "Xây dựng 2 testbench mô phỏng tinh gọn (tb_uart_rtl.v, tb_uart_ping.v) và kiểm chứng thành công trên bo mạch FPGA Basys 3 với thẻ RFID thật và đầu đọc RDM6300 thật."),
        ("4. Đạt chuẩn xuất xưởng ASIC (Tape-out Ready):", "Hoàn thành quy trình thiết kế vật lý trên OpenLane 2 với tiến trình SkyWater 130nm: 0 vi phạm Antenna, 0 lỗi LVS, 0 lỗi DRC, MET TIMING ở tần số 50 MHz trên cả 9 góc đo công nghệ.")
    ]

    for c_title, c_desc in contributions:
        p = tf_t26.add_paragraph()
        p.text = f"{c_title} {c_desc}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.space_after = Pt(8)
        p.line_spacing = 1.15

    p_ty = tf_t26.add_paragraph()
    p_ty.text = "XIN TRÂN TRỌNG CẢM ƠN THẦY CÔ VÀ HỘI ĐỒNG ĐÃ LẮNG NGHE!"
    p_ty.font.name = "Segoe UI"
    p_ty.font.size = Pt(15)
    p_ty.font.bold = True
    p_ty.font.color.rgb = C_WHITE
    p_ty.space_before = Pt(16)

    # -------------------------------------------------------------
    # LƯU FILE VÀ COPY
    # -------------------------------------------------------------
    out_path = os.path.join(cur_dir, "Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.pptx")
    out_v2   = os.path.join(cur_dir, "Bao_Cao_Do_An_RDM6300_PicoRV32_SoC_v2.pptx")
    prs.save(out_path)
    shutil.copy2(out_path, out_v2)
    print(f"Presentation generated successfully: {out_path} ({os.path.getsize(out_path)} bytes)")

    doc_out    = os.path.join(doc_dir, "Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.pptx")
    doc_out_v2 = os.path.join(doc_dir, "Bao_Cao_Do_An_RDM6300_PicoRV32_SoC_v2.pptx")
    shutil.copy2(out_path, doc_out)
    shutil.copy2(out_path, doc_out_v2)
    print(f"Copied presentation to document root: {doc_out} & {doc_out_v2}")

if __name__ == "__main__":
    create_deck()
'''
    target_path = os.path.join(os.path.dirname(__file__), "create_presentation.py")
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(script_content)
    print(f"[SUCCESS] Updated {target_path}")

if __name__ == "__main__":
    generate_new_presentation_py()
