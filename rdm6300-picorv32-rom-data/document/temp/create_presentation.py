# -*- coding: utf-8 -*-
"""
Script: create_presentation.py
Tạo bộ slide báo cáo PowerPoint 16:9 widescreen tiêu chuẩn xuất bản cao cấp (Publication-Grade).
Bao gồm:
- Slide 1: Bìa Đồ Án Tốt Nghiệp
- Slide 2: Mục Lục / Nội Dung Báo Cáo (6 Phần Cốt Lõi)
- Slide 3: Phần 1 - Giới Thiệu Dự Án & Lý Do Lựa Chọn SPI Flash NVM
- Slide 4: Phần 2 - Lựa Chọn Phần Cứng: FPGA Basys 3 & Đầu Đọc RFID RDM6300
- Slide 5: Phần 2 - Chuỗi Công Cụ Phát Triển: FPGA Vivado, ASIC OpenLane 2 & RISC-V GCC
- Slide 6: Phần 3 - Sơ Đồ Khối Kiến Trúc Vi Hệ Thống SoC PicoRV32 (1 Master - 5 Slaves)
- Slide 7: Giai Đoạn 1: Khối Cốt Lõi Có Sẵn & Bổ Sung 1KB SRAM (picorv32.v, spimemio.v, data_sram)
- Slide 8: Giai Đoạn 2: Thiết Kế Cầu Nối Bus Interconnect Tối Ưu (soc_interconnect.v)
- Slide 9: Giai Đoạn 3: Đồng Thiết Kế Phần Cứng - Phần Mềm & Bootstrap (sections.lds, start.s, picorv32_soc.v)
- Slide 10: Giai Đoạn 4: Mở Rộng Ngoại Vi MMIO Với Hàng Đợi FIFO Chống Tràn (uart_mmio.v, sync_fifo.v, gpio)
- Slide 11: Giai Đoạn 5: Tầng Firmware C Tương Tác Qua Con Trỏ Volatile MMIO (soc_regs.h, access_control.c, uart.c)
- Slide 12: Phần 4 - Testbench 1: Kiểm Thử Phần Cứng RTL Thuần Cho UART MMIO & FIFO (tb_uart_rtl.v)
- Slide 13: Phần 4 - Testbench 2: Kiểm Thử Tích Hợp Toàn Diện Top SoC Boot Flash & Ping (tb_uart_ping.v)
- Slide 14: Biến Địa Chỉ 1: REG_RFID_UART_DAT & DIV (0x1000_0004 & 0x1000_0000) - Đọc RFID RX FIFO
- Slide 15: Biến Địa Chỉ 2: REG_PC_UART_DAT & DIV (0x3000_0004 & 0x3000_0000) - Giao Tiếp Host PC UART
- Slide 16: Biến Địa Chỉ 3: REG_GPIO_LEDS (0x4000_0000) - Điều Khiển LED Trạng Thái & Relay Mở Cửa
- Slide 17: Biến Địa Chỉ 4: USER_FLASH_ADDR (0x0030_0000 - Sector 48) - Cơ Sở Dữ Liệu Thẻ Whitelist
- Slide 18: Biến Địa Chỉ 5: LOG_FLASH_ADDR (0x0031_0000 - Sector 49) - Nhật Ký Quẹt Thẻ Access Logs
- Slide 19: Biến Địa Chỉ 6: 0x0200_0000 & flashio_worker - Nạp Routine Vào SRAM Lập Trình Flash NVM
- Slide 20: Phần 5 - Demo Thực Nghiệm Trên FPGA Basys 3: Thiết Lập Kết Nối Phần Cứng
- Slide 21: Phần 5 - Demo Thực Nghiệm Trên FPGA Basys 3: Các Kịch Bản Quẹt Thẻ Thực Tế
- Slide 22: Phần 6 - Thiết Kế Vật Lý ASIC: Quy Trình RTL-to-GDSII Trên OpenLane 2 (SkyWater 130nm)
- Slide 23: Phần 6 - Thiết Kế Vật Lý ASIC: Bản Vẽ Layout OpenROAD & Báo Cáo Ký Duyệt Sign-off
- Slide 24: Tổng Kết Đồ Án Và Các Đóng Góp Nổi Bật

Tổng cộng: 24 slide mạch lạc, chi tiết, chuyên sâu từ kiến trúc, quy trình 5 giai đoạn đến từng biến địa chỉ phần cứng trong C.
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

    img_stages = [
        os.path.join(cur_dir, f"stage{i}_bw_diagram.png") for i in range(1, 6)
    ]

    TOTAL_SLIDES = 24

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

    # Helper: Hộp mã nguồn dạng Terminal / IDE Code Box
    def add_code_box(slide, x, y, w, h, title, lines, status_text=None, title_color=C_CYAN_ACCENT):
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
            p.font.size = Pt(8.0)
            p.line_spacing = 1.08
            p.space_after = 0
            if "[PASS]" in line or "100%" in line or "CONFIRMED" in line or "MET TIMING" in line:
                p.font.color.rgb = C_GREEN
                p.font.bold = True
            elif "[TEST" in line or "[BOOT]" in line or "[EXEC]" in line or "[UART]" in line or "[HOST]" in line:
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

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.05), Inches(10.9), Inches(5.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p_org = tf1.paragraphs[0]
    p_org.text = "TRƯỜNG ĐẠI HỌC BÁCH KHOA HÀ NỘI — KHOA ĐIỆN TỬ VIỄN THÔNG"
    p_org.font.name = "Segoe UI"
    p_org.font.size = Pt(12)
    p_org.font.bold = True
    p_org.font.color.rgb = C_CYAN_ACCENT
    p_org.space_after = Pt(12)

    p_main = tf1.add_paragraph()
    p_main.text = "THIẾT KẾ VI HỆ THỐNG TRÊN CHIP (SoC) CHO THIẾT BỊ\nKIỂM SOÁT RA VÀO OFFLINE SỬ DỤNG RFID RDM6300 VÀ SPI FLASH"
    p_main.font.name = "Segoe UI"
    p_main.font.size = Pt(20)
    p_main.font.bold = True
    p_main.font.color.rgb = C_WHITE
    p_main.space_after = Pt(14)
    p_main.line_spacing = 1.15

    p_sub = tf1.add_paragraph()
    p_sub.text = "Tích hợp CPU RISC-V PicoRV32 | Kiến trúc Boot Flash XIP | Tạo mẫu Basys 3 FPGA | Ký duyệt ASIC OpenLane 2 (SkyWater 130nm)"
    p_sub.font.name = "Segoe UI"
    p_sub.font.size = Pt(11.5)
    p_sub.font.color.rgb = RGBColor(203, 213, 225)
    p_sub.space_after = Pt(22)

    p_info1 = tf1.add_paragraph()
    p_info1.text = "Sinh viên thực hiện :  Thái Tuấn Hiệp  -  MSSV: 20210328  (Chuyên ngành Kỹ thuật Vi điện tử)"
    p_info1.font.name = "Segoe UI"
    p_info1.font.size = Pt(12)
    p_info1.font.bold = True
    p_info1.font.color.rgb = C_WHITE
    p_info1.space_after = Pt(5)

    p_info2 = tf1.add_paragraph()
    p_info2.text = "Giảng viên hướng dẫn :  ThS. Nguyễn Văn Đông  -  Bộ môn Kỹ thuật Máy tính & Vi điện tử"
    p_info2.font.name = "Segoe UI"
    p_info2.font.size = Pt(11.5)
    p_info2.font.color.rgb = RGBColor(226, 232, 240)
    p_info2.space_after = Pt(5)

    p_info3 = tf1.add_paragraph()
    p_info3.text = "Thời gian thực hiện :  Học kỳ 2025.2 - 2026.1  |  Địa điểm: Phòng thí nghiệm Thiết kế Vi mạch VLSI"
    p_info3.font.name = "Segoe UI"
    p_info3.font.size = Pt(10.5)
    p_info3.font.italic = True
    p_info3.font.color.rgb = RGBColor(148, 163, 184)

    # =========================================================================
    # SLIDE 2: MỤC LỤC / NỘI DUNG BÁO CÁO (Agenda - 6 Phần Cốt Lõi)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Tổng Quan Báo Cáo", "Nội Dung Báo Cáo Đồ Án (6 Phần Chuẩn Mực)", 2, total_slides=TOTAL_SLIDES)

    agenda_items = [
        ("Phần 1: Giới Thiệu Dự Án", "Hệ thống kiểm soát ra vào Offline bảo mật cao, lý do chọn bộ nhớ SPI Flash NVM lưu trữ dữ liệu."),
        ("Phần 2: Nền Tảng Phần Cứng & Phần Mềm", "Kit FPGA Basys 3, đầu đọc RDM6300, chuỗi công cụ Vivado, OpenLane 2 & RISC-V GCC."),
        ("Phần 3: Quy Trình Thiết Kế SoC (5 Giai Đoạn)", "Khối cơ sở -> Cầu bus Interconnect -> Đồng thiết kế Bootstrap -> Mở rộng FIFO -> MMIO C."),
        ("Phần 4: Testbench & Chi Tiết Biến Địa Chỉ MMIO", "Kiểm thử RTL thuần, Top SoC Ping và phân tích 6 biến địa chỉ phần cứng trong mã nguồn C."),
        ("Phần 5: Demo Thực Nghiệm Trên FPGA", "Tạo mẫu thực tế trên kit Basys 3, giao tiếp UART PC và 4 kịch bản quẹt thẻ RFID thật."),
        ("Phần 6: Thiết Kế Vật Lý ASIC & Ký Duyệt", "Quy trình RTL-to-GDSII trên OpenLane 2 (Sky130): Layout GDSII, chỉ số PPA và ký duyệt Sign-off.")
    ]

    for i, (ag_t, ag_d) in enumerate(agenda_items):
        col = i % 3
        row = i // 3
        ax = Inches(0.8) + col * Inches(3.95)
        ay = Inches(1.50) + row * Inches(2.65)
        aw = Inches(3.75)
        ah = Inches(2.35)

        card_ag = add_card(s2, ax, ay, aw, ah, bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
        tb_ag = s2.shapes.add_textbox(ax + Inches(0.20), ay + Inches(0.20), aw - Inches(0.40), ah - Inches(0.40))
        tf_ag = tb_ag.text_frame
        tf_ag.word_wrap = True

        p1 = tf_ag.paragraphs[0]
        p1.text = ag_t
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(12.5)
        p1.font.bold = True
        p1.font.color.rgb = C_BLUE_ACCENT
        p1.space_after = Pt(8)

        p2 = tf_ag.add_paragraph()
        p2.text = ag_d
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_TEXT_MUTED
        p2.line_spacing = 1.25

    # =========================================================================
    # SLIDE 3: PHẦN 1 - GIỚI THIỆU DỰ ÁN & LÝ DO CHỌN SPI FLASH NVM
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Phần 1: Giới Thiệu Dự Án", "Thiết Bị Kiểm Soát Ra Vào Offline & Lý Do Lựa Chọn SPI Flash", 3, total_slides=TOTAL_SLIDES)

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
    add_header(s4, "Phần 2: Nền Tảng Phần Cứng", "Lựa Chọn Nền Tảng Phần Cứng: FPGA Basys 3 & Đầu Đọc RFID RDM6300", 4, total_slides=TOTAL_SLIDES)

    hw_cards = [
        ("NỀN TẢNG FPGA DIGILENT BASYS 3", C_BLUE_ACCENT, [
            ("Chip FPGA Xilinx Artix-7 (XC7A35T):", "33,280 Logic Cells, 50 Block RAM 36Kb, 90 DSP Slices - nền tảng lý tưởng tạo mẫu SoC."),
            ("Tích hợp sẵn chip Flash SPI 32Mbit:", "Chip Spansion S25FL032P giao tiếp qua nguyên thủy STARTUPE2 của Xilinx."),
            ("Tích hợp mạch nạp & UART FTDI:", "Cổng micro-USB cung cấp nguồn và kênh UART nối tiếp kết nối trực tiếp với máy tính."),
            ("Hệ thống hiển thị & chẩn đoán tại chỗ:", "16 LED đơn, 16 công tắc gạt (Switch) và 4 nút nhấn phục vụ chẩn đoán trạng thái.")
        ]),
        ("MODULE ĐẦU ĐỌC RFID RDM6300 125KHZ", C_AMBER, [
            ("Tần số sóng mang 125 kHz EM4100:", "Tần số tiêu chuẩn công nghiệp cho thẻ cảm ứng tầm gần (khoảng cách đọc 20 - 50 mm)."),
            ("Giao tiếp UART 9600-8-N-1 tự động:", "Module tự động điều chế và phát ra khung dữ liệu ASCII 14 byte ngay khi phát hiện thẻ."),
            ("Cấu trúc khung dữ liệu an toàn:", "Gồm 1 byte Start (0x02), 10 byte mã thẻ Hex, 2 byte Checksum XOR và 1 byte Stop (0x03)."),
            ("Ăng-ten cuộn cảm rời linh hoạt:", "Dễ dàng lắp đặt tại cửa kiểm soát mà không gây can nhiễu từ trường đến mạch số.")
        ])
    ]

    for i, (hw_title, hw_col, points) in enumerate(hw_cards):
        hx = Inches(0.8) + i * Inches(5.9)
        hw = Inches(5.7)
        add_card(s4, hx, Inches(1.35), hw, Inches(5.4), bg_color=C_WHITE, border_color=hw_col, border_width=2.0)
        tb_h = s4.shapes.add_textbox(hx + Inches(0.2), Inches(1.5), hw - Inches(0.4), Inches(5.1))
        tf_h = tb_h.text_frame
        tf_h.word_wrap = True

        pt = tf_h.paragraphs[0]
        pt.text = hw_title
        pt.font.name = "Segoe UI"
        pt.font.size = Pt(13)
        pt.font.bold = True
        pt.font.color.rgb = hw_col
        pt.space_after = Pt(12)

        for p_lbl, p_val in points:
            p = tf_h.add_paragraph()
            p.text = f"• {p_lbl} {p_val}"
            p.font.name = "Segoe UI"
            p.font.size = Pt(10.5)
            p.font.color.rgb = C_TEXT_DARK
            p.space_after = Pt(10)
            p.line_spacing = 1.2

    # =========================================================================
    # SLIDE 5: PHẦN 2 - LỰA CHỌN PHẦN MỀM: VIVADO, OPENLANE 2 & TOOLCHAIN
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Phần 2: Chuỗi Công Cụ Phát Triển", "Chuỗi Công Cụ Phát Triển: FPGA Vivado, ASIC OpenLane 2 & RISC-V GCC", 5, total_slides=TOTAL_SLIDES)

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
    # SLIDE 6: PHẦN 3 - SƠ ĐỒ KHỐI TỔNG THỂ SOC (BLOCK DIAGRAM B&W DRAW.IO)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Phần 3: Kiến Trúc Vi Hệ Thống SoC",
               "Sơ Đồ Khối Kiến Trúc Vi Hệ Thống SoC PicoRV32 (1 Master - 5 Slaves)", 6, total_slides=TOTAL_SLIDES)

    if os.path.exists(img_fig1):
        add_card(s6, Inches(0.8), Inches(1.35), Inches(7.4), Inches(5.4), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
        s6.shapes.add_picture(img_fig1, Inches(0.9), Inches(1.45), Inches(7.2), Inches(5.2))

    rx6 = Inches(8.4)
    rw6 = Inches(4.13)
    add_card(s6, rx6, Inches(1.35), rw6, Inches(5.4), bg_color=C_WHITE, border_color=C_CARD_BORDER, border_width=1.5)
    tb_b6 = s6.shapes.add_textbox(rx6 + Inches(0.2), Inches(1.5), rw6 - Inches(0.4), Inches(5.1))
    tf_b6 = tb_b6.text_frame
    tf_b6.word_wrap = True

    pb1 = tf_b6.paragraphs[0]
    pb1.text = "QUY TRÌNH THIẾT KẾ SOC QUA 5 GIAI ĐOẠN"
    pb1.font.name = "Segoe UI"
    pb1.font.size = Pt(12.0)
    pb1.font.bold = True
    pb1.font.color.rgb = C_BLUE_ACCENT
    pb1.space_after = Pt(8)

    b_points = [
        ("Giai đoạn 1 (Khối cốt lõi):", "Phân tích 2 IP có sẵn (picorv32.v, spimemio.v) và bổ sung 1KB SRAM (data_sram) chứa Stack C."),
        ("Giai đoạn 2 (Cầu bus Interconnect):", "Thiết kế soc_interconnect.v giải mã 0-delay định tuyến 1 CPU Master tới 5 Slaves."),
        ("Giai đoạn 3 (Đồng thiết kế Bootstrap):", "Khớp tuyệt đối tham số RTL (PROGADDR_RESET, STACKADDR) với Linker (sections.lds, start.s)."),
        ("Giai đoạn 4 (Mở rộng MMIO & FIFO):", "Tích hợp UART RFID & PC có bộ đệm FIFO 32B chống tràn, chống rớt mã thẻ."),
        ("Giai đoạn 5 (Tầng C Volatile MMIO):", "Trừu tượng hóa thanh ghi phần cứng qua con trỏ volatile (soc_regs.h) để C điều khiển trong suốt.")
    ]

    for p_lbl, p_val in b_points:
        p = tf_b6.add_paragraph()
        p.text = f"• {p_lbl} {p_val}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(6)
        p.line_spacing = 1.15

    # =========================================================================
    # SLIDE 7: GIAI ĐOẠN 1 - KHỐI CỐT LÕI CÓ SẴN & BỔ SUNG 1KB SRAM
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Phần 3: Quy Trình Thiết Kế SoC (Giai Đoạn 1/5)",
               "Giai Đoạn 1: Khối Cốt Lõi Có Sẵn & Bổ Sung 1KB SRAM (picorv32.v, spimemio.v, data_sram)", 7, total_slides=TOTAL_SLIDES)

    if os.path.exists(img_stages[0]):
        add_card(s7, Inches(0.8), Inches(1.30), Inches(5.75), Inches(5.50), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
        s7.shapes.add_picture(img_stages[0], Inches(0.95), Inches(1.45), Inches(5.45), Inches(5.20))

    rx7 = Inches(6.75)
    rw7 = Inches(5.78)
    add_card(s7, rx7, Inches(1.30), rw7, Inches(5.50), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
    tb_r7 = s7.shapes.add_textbox(rx7 + Inches(0.20), Inches(1.45), rw7 - Inches(0.40), Inches(5.20))
    tf_r7 = tb_r7.text_frame
    tf_r7.word_wrap = True

    p_r7_h = tf_r7.paragraphs[0]
    p_r7_h.text = "PHÂN TÍCH THIẾT KẾ & TẬN DỤNG IP CỐT LÕI"
    p_r7_h.font.name = "Segoe UI"
    p_r7_h.font.bold = True
    p_r7_h.font.size = Pt(12)
    p_r7_h.font.color.rgb = C_BLUE_ACCENT
    p_r7_h.space_after = Pt(8)

    st1_points = [
        ("Nhân CPU Master (picorv32.v):", "Thực thi tập lệnh RV32I, 32 thanh ghi 32-bit. Giao tiếp toàn bộ qua Native Memory Bus: phát mem_valid cùng địa chỉ mem_addr, chờ mem_ready phản hồi."),
        ("Bộ điều khiển Flash (spimemio.v):", "Tự sinh chuỗi xung SPI đọc chip Flash ngoài, chuyển đổi địa chỉ thành lệnh SPI và trả opcode về mem_rdata theo cơ chế XIP (eXecute-In-Place) tại dải 0x0010_0000 - 0x00FF_FFFF."),
        ("Bổ sung 1KB SRAM nội (data_sram):", "Do spimemio chỉ hỗ trợ đọc XIP nên KHÔNG THỂ LƯU STACK C! Ta bổ sung 256 words SRAM tĩnh (0x0000_0000 - 0x0000_03FF), phản hồi sram_ready = 1 tức thì trong 1 chu kỳ clock để lưu trữ con trỏ ngăn xếp (sp) và biến cục bộ."),
        ("Ý nghĩa kỹ thuật tối thượng:", "Kết hợp 'Flash ngoài 4MB lưu mã lệnh' + '1KB SRAM nội lưu Stack' giúp tiết kiệm tối đa diện tích silicon ASIC nhưng vẫn chạy được toàn bộ ứng dụng C.")
    ]

    for p_lbl, p_val in st1_points:
        p = tf_r7.add_paragraph()
        p.text = f"• {p_lbl} {p_val}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(6)
        p.line_spacing = 1.15

    p_sum1 = tf_r7.add_paragraph()
    p_sum1.text = "=> KẾT QUẢ: Hoàn thành nền tảng xử lý 1 Master - 2 Vùng nhớ cốt lõi (Flash XIP & Data SRAM)."
    p_sum1.font.name = "Segoe UI"
    p_sum1.font.size = Pt(9.2)
    p_sum1.font.bold = True
    p_sum1.font.color.rgb = C_BLUE_ACCENT
    p_sum1.space_before = Pt(4)

    # =========================================================================
    # SLIDE 8: GIAI ĐOẠN 2 - THIẾT KẾ CẦU NỐI BUS INTERCONNECT TỐI ƯU
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Phần 3: Quy Trình Thiết Kế SoC (Giai Đoạn 2/5)",
               "Giai Đoạn 2: Thiết Kế Cầu Nối Bus Interconnect Tối Ưu (soc_interconnect.v)", 8, total_slides=TOTAL_SLIDES)

    if os.path.exists(img_stages[1]):
        add_card(s8, Inches(0.8), Inches(1.30), Inches(5.75), Inches(5.50), bg_color=C_WHITE, border_color=C_AMBER, border_width=1.5)
        s8.shapes.add_picture(img_stages[1], Inches(0.95), Inches(1.45), Inches(5.45), Inches(5.20))

    rx8 = Inches(6.75)
    rw8 = Inches(5.78)
    add_card(s8, rx8, Inches(1.30), rw8, Inches(5.50), bg_color=C_WHITE, border_color=C_AMBER, border_width=1.5)
    tb_r8 = s8.shapes.add_textbox(rx8 + Inches(0.20), Inches(1.45), rw8 - Inches(0.40), Inches(5.20))
    tf_r8 = tb_r8.text_frame
    tf_r8.word_wrap = True

    p_r8_h = tf_r8.paragraphs[0]
    p_r8_h.text = "NGUYÊN LÝ PHÂN LUỒNG BUS TỔ HỢP 0-DELAY"
    p_r8_h.font.name = "Segoe UI"
    p_r8_h.font.bold = True
    p_r8_h.font.size = Pt(12)
    p_r8_h.font.color.rgb = C_AMBER
    p_r8_h.space_after = Pt(8)

    st2_points = [
        ("Vấn đề kỹ thuật:", "CPU chỉ có 1 cổng Native Bus duy nhất, trong khi hệ thống có tới 5 module bộ nhớ và ngoại vi khác nhau cần truy xuất đồng thời."),
        ("1. Giải mã địa chỉ tổ hợp (Address Decoder):", "soc_interconnect.v giải mã tức thì trong 0 chu kỳ clock:\n  - sel_sram: cpu_mem_addr < 0x0000_0400 (1KB SRAM)\n  - sel_spimem: 0x0010_0000 đến 0x00FF_FFFF (Flash XIP)\n  - sel_spicfg: 0x0200_0000 (Flash Bit-bang Controller)"),
        ("2. Dồn kênh phản hồi (Multiplexer MUX):", "cpu_mem_ready = sram_ready || spimem_ready || sel_spicfg;\n  cpu_mem_rdata = sel_sram ? sram_rdata : spimem_rdata;\nGiúp CPU nhận phản hồi chính xác từ Slave đang được chọn."),
        ("Ý nghĩa kỹ thuật:", "Bộ ghép bus thuần tổ hợp (0 FF trễ) đảm bảo tốc độ phản hồi tối đa, không phát sinh chu kỳ chờ (zero wait-state) khi truy xuất SRAM.")
    ]

    for p_lbl, p_val in st2_points:
        p = tf_r8.add_paragraph()
        p.text = f"• {p_lbl} {p_val}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(6)
        p.line_spacing = 1.15

    p_sum2 = tf_r8.add_paragraph()
    p_sum2.text = "=> KẾT QUẢ: Đóng vai trò 'cảnh sát giao thông' phân luồng hoàn hảo giữa CPU, Flash và RAM."
    p_sum2.font.name = "Segoe UI"
    p_sum2.font.size = Pt(9.2)
    p_sum2.font.bold = True
    p_sum2.font.color.rgb = C_AMBER
    p_sum2.space_before = Pt(4)

    # =========================================================================
    # SLIDE 9: GIAI ĐOẠN 3 - ĐỒNG THIẾT KẾ PHẦN CỨNG - PHẦN MỀM (BOOTSTRAP)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Phần 3: Quy Trình Thiết Kế SoC (Giai Đoạn 3/5)",
               "Giai Đoạn 3: Đồng Thiết Kế Phần Cứng - Phần Mềm & Bootstrap (sections.lds, start.s, picorv32_soc.v)", 9, total_slides=TOTAL_SLIDES)

    if os.path.exists(img_stages[2]):
        add_card(s9, Inches(0.8), Inches(1.30), Inches(5.75), Inches(5.50), bg_color=C_WHITE, border_color=C_PURPLE, border_width=1.5)
        s9.shapes.add_picture(img_stages[2], Inches(0.95), Inches(1.45), Inches(5.45), Inches(5.20))

    rx9 = Inches(6.75)
    rw9 = Inches(5.78)
    add_card(s9, rx9, Inches(1.30), rw9, Inches(5.50), bg_color=C_WHITE, border_color=C_PURPLE, border_width=1.5)
    tb_r9 = s9.shapes.add_textbox(rx9 + Inches(0.20), Inches(1.45), rw9 - Inches(0.40), Inches(5.20))
    tf_r9 = tb_r9.text_frame
    tf_r9.word_wrap = True

    p_r9_h = tf_r9.paragraphs[0]
    p_r9_h.text = "CƠ CHẾ CO-DESIGN BOOTSTRAP TỰ ĐỘNG KHỞI ĐỘNG"
    p_r9_h.font.name = "Segoe UI"
    p_r9_h.font.bold = True
    p_r9_h.font.size = Pt(12)
    p_r9_h.font.color.rgb = C_PURPLE
    p_r9_h.space_after = Pt(8)

    st3_points = [
        ("Vấn đề kỹ thuật:", "Sau khi có phần cứng, làm sao để CPU biết bắt đầu thực thi từ đâu và thiết lập môi trường chạy hàm main() của ngôn ngữ C mà không cần Bootloader?"),
        ("1. Khớp Vector Reset (0x0025_0000):", "RTL định nghĩa PROGADDR_RESET = 32'h0025_0000, khớp 100% với mốc ORIGIN FLASH trong Linker Script sections.lds. Ngay khi nhả resetn=1, CPU phát lệnh đọc opcode đầu tiên từ Flash Sector 37."),
        ("2. Khớp Đỉnh Ngăn Xếp (0x0000_0400):", "RTL định nghĩa STACKADDR = 32'h0000_0400, khớp với nhãn _stack_top trong sections.lds. Đoạn mã Assembly start.s nạp mốc này vào thanh ghi sp."),
        ("3. Chuyển tiếp sang C (call main):", "Sau 3 lệnh Assembly thiết lập ngăn xếp trên 1KB SRAM, start.s phát lệnh call main, chính thức chuyển giao quyền điều khiển cho Firmware C."),
        ("Ý nghĩa kỹ thuật:", "Hệ thống tự khởi động hoàn toàn tự động ngay khi cấp nguồn vi mạch ASIC mà không cần can thiệp từ bên ngoài.")
    ]

    for p_lbl, p_val in st3_points:
        p = tf_r9.add_paragraph()
        p.text = f"• {p_lbl} {p_val}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(5)
        p.line_spacing = 1.15

    p_sum3 = tf_r9.add_paragraph()
    p_sum3.text = "=> KẾT QUẢ: Đồng bộ 100% giữa Phần Cứng (Verilog) và Phần Mềm (C/ASM/Linker)."
    p_sum3.font.name = "Segoe UI"
    p_sum3.font.size = Pt(9.2)
    p_sum3.font.bold = True
    p_sum3.font.color.rgb = C_PURPLE
    p_sum3.space_before = Pt(4)

    # =========================================================================
    # SLIDE 10: GIAI ĐOẠN 4 - MỞ RỘNG NGOẠI VI MMIO CÓ FIFO CHỐNG TRÀN
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Phần 3: Quy Trình Thiết Kế SoC (Giai Đoạn 4/5)",
               "Giai Đoạn 4: Mở Rộng Ngoại Vi MMIO Với Hàng Đợi FIFO Chống Tràn (uart_mmio.v, sync_fifo.v, gpio)", 10, total_slides=TOTAL_SLIDES)

    if os.path.exists(img_stages[3]):
        add_card(s10, Inches(0.8), Inches(1.30), Inches(5.75), Inches(5.50), bg_color=C_WHITE, border_color=C_ROSE, border_width=1.5)
        s10.shapes.add_picture(img_stages[3], Inches(0.95), Inches(1.45), Inches(5.45), Inches(5.20))

    rx10 = Inches(6.75)
    rw10 = Inches(5.78)
    add_card(s10, rx10, Inches(1.30), rw10, Inches(5.50), bg_color=C_WHITE, border_color=C_ROSE, border_width=1.5)
    tb_r10 = s10.shapes.add_textbox(rx10 + Inches(0.20), Inches(1.45), rw10 - Inches(0.40), Inches(5.20))
    tf_r10 = tb_r10.text_frame
    tf_r10.word_wrap = True

    p_r10_h = tf_r10.paragraphs[0]
    p_r10_h.text = "TÍCH HỢP NGOẠI VI & HÀNG ĐỢI PHẦN CỨNG FIFO"
    p_r10_h.font.name = "Segoe UI"
    p_r10_h.font.bold = True
    p_r10_h.font.size = Pt(12)
    p_r10_h.font.color.rgb = C_ROSE
    p_r10_h.space_after = Pt(8)

    st4_points = [
        ("Ngoại vi RFID RDM6300 (Slave 2 @ 0x1000_0000):", "Tích hợp sync_2ff.v chống hiện tượng siêu ổn định (Metastability) từ ăng-ten ngoài và sync_fifo.v 32 byte để đệm trọn vẹn chuỗi 14 byte của thẻ."),
        ("Ngoại vi Host PC UART (Slave 3 @ 0x3000_0000):", "Tích hợp cả 32B RX FIFO và 32B TX FIFO hỗ trợ giao tiếp Full-Duplex tốc độ cao với máy tính quản trị."),
        ("Ngoại vi GPIO LED & Relay (Slave 4 @ 0x4000_0000):", "Điều khiển 16 LED trạng thái (LED 0 nhịp tim, LED 1 Flash, LED 2 mở cửa) và relay khóa điện."),
        ("Vai trò sống còn của FIFO 32 Bytes:", "Khi CPU bận ghi dữ liệu vào Flash NVM (mất 1-3 ms), nếu người dùng quẹt thẻ liên tục, hàng đợi FIFO 32B tự động lưu giữ toàn bộ dữ liệu, chống rớt gói tin tuyệt đối!"),
        ("Cơ chế Non-blocking Bus:", "Nếu FIFO rỗng, mạch trả về ngay 0xFFFFFFFF trong 1 chu kỳ clock, ngăn chặn hoàn toàn hiện tượng CPU bị treo bus.")
    ]

    for p_lbl, p_val in st4_points:
        p = tf_r10.add_paragraph()
        p.text = f"• {p_lbl} {p_val}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(5)
        p.line_spacing = 1.15

    p_sum4 = tf_r10.add_paragraph()
    p_sum4.text = "=> KẾT QUẢ: Hệ thống ngoại vi hoàn chỉnh, bảo đảm tính thời gian thực và an toàn dữ liệu."
    p_sum4.font.name = "Segoe UI"
    p_sum4.font.size = Pt(9.2)
    p_sum4.font.bold = True
    p_sum4.font.color.rgb = C_ROSE
    p_sum4.space_before = Pt(4)

    # =========================================================================
    # SLIDE 11: GIAI ĐOẠN 5 - TẦNG FIRMWARE C TƯƠNG TÁC QUA VOLATILE MMIO
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Phần 3: Quy Trình Thiết Kế SoC (Giai Đoạn 5/5)",
               "Giai Đoạn 5: Tầng Firmware C Tương Tác Qua Con Trỏ Volatile MMIO (soc_regs.h, access_control.c, uart.c)", 11, total_slides=TOTAL_SLIDES)

    if os.path.exists(img_stages[4]):
        add_card(s11, Inches(0.8), Inches(1.30), Inches(5.75), Inches(5.50), bg_color=C_WHITE, border_color=C_GREEN, border_width=1.5)
        s11.shapes.add_picture(img_stages[4], Inches(0.95), Inches(1.45), Inches(5.45), Inches(5.20))

    rx11 = Inches(6.75)
    rw11 = Inches(5.78)
    add_card(s11, rx11, Inches(1.30), rw11, Inches(5.50), bg_color=C_WHITE, border_color=C_GREEN, border_width=1.5)
    tb_r11 = s11.shapes.add_textbox(rx11 + Inches(0.20), Inches(1.45), rw11 - Inches(0.40), Inches(5.20))
    tf_r11 = tb_r11.text_frame
    tf_r11.word_wrap = True

    p_r11_h = tf_r11.paragraphs[0]
    p_r11_h.text = "TRỪU TƯỢNG HÓA PHẦN CỨNG BẰNG NGÔN NGỮ C"
    p_r11_h.font.name = "Segoe UI"
    p_r11_h.font.bold = True
    p_r11_h.font.size = Pt(12)
    p_r11_h.font.color.rgb = C_GREEN
    p_r11_h.space_after = Pt(8)

    st5_points = [
        ("Tầng Macro MMIO (soc_regs.h):", "Định nghĩa các con trỏ phần cứng:\n  #define REG_RFID_UART_DAT (*(volatile uint32_t*)0x10000004)\n  #define REG_PC_UART_DAT   (*(volatile uint32_t*)0x30000004)\n  #define REG_GPIO_LEDS     (*(volatile uint32_t*)0x40000000)"),
        ("Bản chất từ khóa volatile:", "Ép trình biên dịch GCC luôn sinh ra lệnh đọc/ghi bus thật (lw, sw), loại bỏ triệt để lỗi tối ưu hóa lưu biến vào thanh ghi."),
        ("Tầng Ứng Dụng C (access_control.c):", "Xử lý nghiệp vụ hoàn toàn trong suốt:\n  uint32_t d = REG_RFID_UART_DAT;\n  if (d != 0xFFFFFFFF) rdm6300_push_byte((uint8_t)d);\n  if (card_valid) REG_GPIO_LEDS |= 0x04; // Mở cửa"),
        ("Ý nghĩa kỹ thuật:", "Lập trình viên C có thể điều khiển toàn bộ vi mạch số phức tạp chỉ bằng các biến con trỏ quen thuộc, mã nguồn trong sáng, độc lập với phần cứng.")
    ]

    for p_lbl, p_val in st5_points:
        p = tf_r11.add_paragraph()
        p.text = f"• {p_lbl} {p_val}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(5)
        p.line_spacing = 1.15

    p_sum5 = tf_r11.add_paragraph()
    p_sum5.text = "=> KẾT LUẬN: 5 giai đoạn thiết kế đã tạo nên một SoC hoàn chỉnh, tối ưu và sẵn sàng sản xuất."
    p_sum5.font.name = "Segoe UI"
    p_sum5.font.size = Pt(9.2)
    p_sum5.font.bold = True
    p_sum5.font.color.rgb = C_GREEN
    p_sum5.space_before = Pt(4)

    # =========================================================================
    # SLIDE 12: PHẦN 4 - HỆ THỐNG TESTBENCH: UART RTL (TB_UART_RTL.V)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Phần 4: Hệ Thống Testbench & Mô Phỏng", "Testbench 1: Kiểm Thử Phần Cứng RTL Thuần Cho UART MMIO & FIFO (tb_uart_rtl.v)", 12, total_slides=TOTAL_SLIDES)

    lx12 = Inches(0.8)
    lw12 = Inches(5.7)
    add_card(s12, lx12, Inches(1.35), lw12, Inches(5.4), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
    tb_l12 = s12.shapes.add_textbox(lx12 + Inches(0.2), Inches(1.5), lw12 - Inches(0.4), Inches(5.1))
    tf_l12 = tb_l12.text_frame
    tf_l12.word_wrap = True

    pt12 = tf_l12.paragraphs[0]
    pt12.text = "5 KỊCH BẢN KIỂM THỬ UART RTL THUẦN"
    pt12.font.name = "Segoe UI"
    pt12.font.size = Pt(13)
    pt12.font.bold = True
    pt12.font.color.rgb = C_BLUE_ACCENT
    pt12.space_after = Pt(10)

    tb_uart_scenarios = [
        ("Mục tiêu:", "Xác minh tính đúng đắn phần cứng của uart_mmio.v, sync_fifo.v và simpleuart.v mà không cần CPU."),
        ("1. Default Divider:", "Kiểm tra thanh ghi Prescaler tại offset 0x00 nạp đúng giá trị mặc định 5208 (9600 baud @ 50MHz)."),
        ("2. Divider Reconfig:", "Ghi giá trị chia tần mới và đọc lại qua bus MMIO, xác nhận mạch thanh ghi hoạt động chuẩn xác."),
        ("3. Serial TX Waveform:", "Ghi ký tự vào offset 0x04, kiểm tra dạng sóng nối tiếp tx_o (Start bit = 0, 8 data bits LSB-first, Stop bit = 1)."),
        ("4. Serial RX & FIFO:", "Bắn chuỗi bit vào rx_i, cờ rx_activity_o tích cực, kiểm tra dữ liệu nạp vào FIFO và trả về 0xFFFFFFFF khi rỗng."),
        ("5. Multi-Byte Burst:", "Bắn liên tiếp chuỗi byte kiểm tra cơ chế chống tràn của hàng đợi FIFO 32 byte.")
    ]

    for p_lbl, p_val in tb_uart_scenarios:
        p = tf_l12.add_paragraph()
        p.text = f"• {p_lbl} {p_val}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(8)
        p.line_spacing = 1.15

    rx12 = Inches(6.8)
    rw12 = Inches(5.73)
    code_lines_12 = [
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
    add_code_box(s12, rx12, Inches(1.35), rw12, Inches(5.4), "tb/run_sim_uart.bat output", code_lines_12, "=== UART RTL TESTBENCH: 100% PASS ===")

    # =========================================================================
    # SLIDE 13: PHẦN 4 - HỆ THỐNG TESTBENCH: TOP SOC BOOT & PING (TB_UART_PING.V)
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Phần 4: Hệ Thống Testbench & Mô Phỏng", "Testbench 2: Kiểm Thử Tích Hợp Toàn Diện Top SoC Boot Flash & Ping (tb_uart_ping.v)", 13, total_slides=TOTAL_SLIDES)

    lx13 = Inches(0.8)
    lw13 = Inches(5.7)
    add_card(s13, lx13, Inches(1.35), lw13, Inches(5.4), bg_color=C_WHITE, border_color=C_GREEN, border_width=1.5)
    tb_l13 = s13.shapes.add_textbox(lx13 + Inches(0.2), Inches(1.5), lw13 - Inches(0.4), Inches(5.1))
    tf_l13 = tb_l13.text_frame
    tf_l13.word_wrap = True

    pt13 = tf_l13.paragraphs[0]
    pt13.text = "5 KỊCH BẢN KIỂM THỬ TÍCH HỢP TOP SOC"
    pt13.font.name = "Segoe UI"
    pt13.font.size = Pt(13)
    pt13.font.bold = True
    pt13.font.color.rgb = C_GREEN
    pt13.space_after = Pt(10)

    tb_soc_scenarios = [
        ("Mục tiêu:", "Xác minh hệ thống Top-level hoàn chỉnh gồm CPU PicoRV32, spimemio, 1KB SRAM, Interconnect và UART."),
        ("1. Power-On Reset & Boot Flash:", "PicoRV32 thức dậy tại 0x0025_0000, spimemio kéo từng từ lệnh mã C từ firmware.hex qua XIP."),
        ("2. C Startup Banner:", "CPU thực thi mã C trong main.c, khởi tạo ngoại vi và in toàn bộ chuỗi chào mừng ra UART."),
        ("3. Host Ping Processing:", "Testbench đóng vai trò PC Host gửi byte lệnh 'P' (0x50) và '\\n' (0x0A) qua cổng nối tiếp."),
        ("4. Response Verification:", "CPU phản hồi chuỗi 'PONG: PicoRV32 Active', testbench so khớp từng ký tự."),
        ("5. CPU Health & Zero-Trap:", "Khẳng định tín hiệu cpu_trap == 0 xuyên suốt quá trình chạy, không bị illegal instruction hay tràn RAM.")
    ]

    for p_lbl, p_val in tb_soc_scenarios:
        p = tf_l13.add_paragraph()
        p.text = f"• {p_lbl} {p_val}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(8)
        p.line_spacing = 1.15

    rx13 = Inches(6.8)
    rw13 = Inches(5.73)
    code_lines_13 = [
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
    add_code_box(s13, rx13, Inches(1.35), rw13, Inches(5.4), "tb/run_sim_ping.bat output", code_lines_13, "=== TOP SOC PING TESTBENCH: 100% PASS ===")

    # =========================================================================
    # SLIDE 14: BIẾN ĐỊA CHỈ 1 - REG_RFID_UART_DAT & DIV (0x1000_0004 & 0x1000_0000)
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Tầng Firmware C & Phần Cứng (Biến Địa Chỉ 1/6)",
               "Biến Địa Chỉ 1: REG_RFID_UART_DAT & DIV (0x1000_0004 & 0x1000_0000)", 14, total_slides=TOTAL_SLIDES)

    code_addr1 = [
        "// firmware/common/soc_regs.h - Định nghĩa con trỏ volatile",
        "#define REG_RFID_UART_DIV (*(volatile uint32_t*)0x10000000) // Baud divider",
        "#define REG_RFID_UART_DAT (*(volatile uint32_t*)0x10000004) // RX FIFO 32B",
        "",
        "// firmware/app/access_control.c - Khởi tạo bộ chia tần số",
        "void access_control_init(void) {",
        "    if (REG_RFID_UART_DIV == 0) {",
        "        REG_RFID_UART_DIV = 5208; // 50 MHz / 9600 Baud = 5208",
        "    }",
        "    rdm6300_parser_init();",
        "}",
        "",
        "// firmware/app/access_control.c - Đọc không khóa từ hàng đợi FIFO",
        "static inline int rfid_uart_getc_nonblock(void) {",
        "    uint32_t d = REG_RFID_UART_DAT; // Pop 1 byte từ RX FIFO phần cứng",
        "    if (d == 0xFFFFFFFF) return -1; // FIFO rỗng -> Thoát ngay (0-wait)",
        "    return (int)(d & 0xFF);         // Trả về byte dữ liệu 8-bit",
        "}",
        "",
        "void access_control_poll(void) {",
        "    int ch;",
        "    while ((ch = rfid_uart_getc_nonblock()) >= 0) {",
        "        rdm6300_tag_t tag;",
        "        if (rdm6300_parse_byte((uint8_t)ch, &tag))",
        "            access_control_process_card(tag.tag_hex, tag.tag_hi, tag.tag_lo);",
        "    }",
        "}"
    ]
    add_code_box(s14, Inches(0.8), Inches(1.30), Inches(5.75), Inches(5.50), "access_control.c & soc_regs.h [RFID MMIO]", code_addr1, status_text="=== READ: 0x1000_0004 -> POP RX FIFO (NON-BLOCKING 1-CYCLE) ===", title_color=C_CYAN_ACCENT)

    rx14 = Inches(6.75)
    rw14 = Inches(5.78)
    add_card(s14, rx14, Inches(1.30), rw14, Inches(5.50), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
    tb_r14 = s14.shapes.add_textbox(rx14 + Inches(0.20), Inches(1.45), rw14 - Inches(0.40), Inches(5.20))
    tf_r14 = tb_r14.text_frame
    tf_r14.word_wrap = True

    p14_h = tf_r14.paragraphs[0]
    p14_h.text = "THAO TÁC & MỤC ĐÍCH THIẾT KẾ ĐỊA CHỈ RFID MMIO"
    p14_h.font.name = "Segoe UI"
    p14_h.font.bold = True
    p14_h.font.size = Pt(12)
    p14_h.font.color.rgb = C_BLUE_ACCENT
    p14_h.space_after = Pt(8)

    addr1_points = [
        ("1. Địa chỉ vật lý phần cứng:", "0x1000_0000 (Prescaler Divider) và 0x1000_0004 (RX FIFO Data) do soc_interconnect.v giải mã khi cpu_mem_addr[31:28] == 4'h1 (Slave 2: uart_mmio.v)."),
        ("2. Cách thao tác trong C:", "• Cấu hình baudrate: Ghi giá trị 5208 (50,000,000 / 9600) vào REG_RFID_UART_DIV một lần duy nhất lúc khởi động.\n• Đọc không khóa (Non-blocking): Đọc REG_RFID_UART_DAT. Nếu d != 0xFFFFFFFF, ép kiểu lấy byte dữ liệu (d & 0xFF) đưa vào máy trạng thái parser."),
        ("3. Mục đích thiết kế:", "Thu nhận liên tục các byte mã thẻ từ đầu đọc RFID RDM6300 125kHz qua hàng đợi phần cứng FIFO 32 bytes mà không làm gián đoạn hay treo CPU."),
        ("4. Ràng buộc & Ưu điểm:", "Cơ chế Non-blocking giúp CPU chỉ mất đúng 1 chu kỳ clock để kiểm tra trạng thái thẻ, giải phóng thời gian cho CPU xử lý các tác vụ kiểm soát và ghi Flash.")
    ]

    for p_lbl, p_val in addr1_points:
        p = tf_r14.add_paragraph()
        p.text = f"• {p_lbl} {p_val}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.3)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(5)
        p.line_spacing = 1.15

    # =========================================================================
    # SLIDE 15: BIẾN ĐỊA CHỈ 2 - REG_PC_UART_DAT & DIV (0x3000_0004 & 0x3000_0000)
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Tầng Firmware C & Phần Cứng (Biến Địa Chỉ 2/6)",
               "Biến Địa Chỉ 2: REG_PC_UART_DAT & DIV (0x3000_0004 & 0x3000_0000)", 15, total_slides=TOTAL_SLIDES)

    code_addr2 = [
        "// firmware/common/soc_regs.h - Địa chỉ UART Host PC",
        "#define REG_PC_UART_DIV   (*(volatile uint32_t*)0x30000000)",
        "#define REG_PC_UART_DAT   (*(volatile uint32_t*)0x30000004)",
        "",
        "// firmware/drivers/uart.c - Khởi tạo & Gửi/Nhận ký tự",
        "void uart_init(uint32_t baud_div) {",
        "    if (REG_PC_UART_DIV == 0 && baud_div != 0)",
        "        REG_PC_UART_DIV = baud_div; // 5208 cho 9600 Baud @ 50MHz",
        "}",
        "",
        "void uart_putc(char c) {",
        "    REG_PC_UART_DAT = (uint32_t)(uint8_t)c; // Đẩy vào TX FIFO",
        "}",
        "void uart_puts(const char *str) {",
        "    while (*str) {",
        "        if (*str == '\\n') uart_putc('\\r'); // Chuẩn hóa CRLF",
        "        uart_putc(*str++);",
        "    }",
        "}",
        "",
        "int uart_getc_nonblock(void) {",
        "    uint32_t d = REG_PC_UART_DAT; // Đọc từ RX FIFO Host PC",
        "    if (d == 0xFFFFFFFF) return -1; // Chưa có phím bấm từ PC",
        "    return (int)(d & 0xFF);",
        "}",
        "char uart_getc_blocking(void) {",
        "    int c; do { c = uart_getc_nonblock(); } while (c < 0);",
        "    return (char)c;",
        "}"
    ]
    add_code_box(s15, Inches(0.8), Inches(1.30), Inches(5.75), Inches(5.50), "uart.c & soc_regs.h [Host PC UART MMIO]", code_addr2, status_text="=== WRITE: 0x3000_0004 -> PUSH TX FIFO | READ: POP RX FIFO ===", title_color=RGBColor(251, 191, 36))

    rx15 = Inches(6.75)
    rw15 = Inches(5.78)
    add_card(s15, rx15, Inches(1.30), rw15, Inches(5.50), bg_color=C_WHITE, border_color=C_AMBER, border_width=1.5)
    tb_r15 = s15.shapes.add_textbox(rx15 + Inches(0.20), Inches(1.45), rw15 - Inches(0.40), Inches(5.20))
    tf_r15 = tb_r15.text_frame
    tf_r15.word_wrap = True

    p15_h = tf_r15.paragraphs[0]
    p15_h.text = "THAO TÁC & MỤC ĐÍCH THIẾT KẾ ĐỊA CHỈ HOST PC UART"
    p15_h.font.name = "Segoe UI"
    p15_h.font.bold = True
    p15_h.font.size = Pt(12)
    p15_h.font.color.rgb = C_AMBER
    p15_h.space_after = Pt(8)

    addr2_points = [
        ("1. Địa chỉ vật lý phần cứng:", "0x3000_0000 (Bộ chia Baudrate) và 0x3000_0004 (TX/RX FIFO Data) do soc_interconnect.v giải mã khi cpu_mem_addr[31:28] == 4'h3 (Slave 3: uart_mmio.v)."),
        ("2. Cách thao tác trong C:", "• Ghi dữ liệu phát (TX): Gán REG_PC_UART_DAT = c. Phần cứng tự động nạp ký tự vào TX FIFO 32 bytes và phát ra chân tx_o.\n• Đọc dữ liệu nhận (RX): Đọc REG_PC_UART_DAT. Nhận lệnh điều khiển từ Host Console PC mà không bị khóa chương trình."),
        ("3. Mục đích thiết kế:", "Hiện thực hóa kênh truyền Full-Duplex tin cậy giữa SoC PicoRV32 và máy tính: phản hồi lệnh Ping ('PONG'), truyền log quẹt thẻ thời gian thực và nhận cấu hình nạp thẻ mới."),
        ("4. Tối ưu hóa chuỗi ký tự:", "Hàm uart_puts tự động chèn ký tự CR ('\\r') trước LF ('\\n') giúp định dạng văn bản chuẩn trên mọi Terminal (Putty, TeraTerm, Python Host Console).")
    ]

    for p_lbl, p_val in addr2_points:
        p = tf_r15.add_paragraph()
        p.text = f"• {p_lbl} {p_val}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.3)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(5)
        p.line_spacing = 1.15

    # =========================================================================
    # SLIDE 16: BIẾN ĐỊA CHỈ 3 - REG_GPIO_LEDS (0x4000_0000)
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "Tầng Firmware C & Phần Cứng (Biến Địa Chỉ 3/6)",
               "Biến Địa Chỉ 3: REG_GPIO_LEDS (0x4000_0000) - Điều Khiển LED & Relay", 16, total_slides=TOTAL_SLIDES)

    code_addr3 = [
        "// firmware/common/soc_regs.h",
        "#define REG_GPIO_LEDS (*(volatile uint32_t*)0x40000000) // 16-bit GPIO Out",
        "",
        "// firmware/app/access_control.c - Bật LED xanh/đỏ theo phân quyền",
        "void access_control_process_card(const char *hex, uint32_t hi, uint32_t lo) {",
        "    if (is_granted) {",
        "        // Bật LED xanh (Bit 2) & Kích hoạt Relay chốt điện mở cửa",
        "        REG_GPIO_LEDS = (REG_GPIO_LEDS & ~0x0002) | 0x0004;",
        "    } else {",
        "        // Bật LED đỏ cảnh báo (Bit 1) từ chối truy cập",
        "        REG_GPIO_LEDS = (REG_GPIO_LEDS & ~0x0004) | 0x0002;",
        "    }",
        "}",
        "",
        "// firmware/drivers/flash.c - Bật LED vàng cảnh báo Flash bận",
        "void flash_write_word(uint32_t addr, uint32_t data) {",
        "    REG_GPIO_LEDS |= 0x0008;  // Bật LED Bit 3",
        "    flashio(buf, 8, 0x06);    // Thực thi nạp Page Program",
        "    REG_GPIO_LEDS &= ~0x0008; // Tắt LED Bit 3 khi ghi xong",
        "}",
        "",
        "// firmware/main.c - Nhịp tim 1Hz chứng minh CPU đang sống",
        "void main_heartbeat_toggle(void) {",
        "    REG_GPIO_LEDS ^= 0x0001;  // Đảo trạng thái LED Bit 0 (Heartbeat)",
        "}"
    ]
    add_code_box(s16, Inches(0.8), Inches(1.30), Inches(5.75), Inches(5.50), "access_control.c & flash.c [GPIO MMIO]", code_addr3, status_text="=== WRITE: 0x4000_0000 -> 16-BIT PARALLEL GPIO OUT (1-CYCLE) ===", title_color=RGBColor(52, 211, 153))

    rx16 = Inches(6.75)
    rw16 = Inches(5.78)
    add_card(s16, rx16, Inches(1.30), rw16, Inches(5.50), bg_color=C_WHITE, border_color=C_GREEN, border_width=1.5)
    tb_r16 = s16.shapes.add_textbox(rx16 + Inches(0.20), Inches(1.45), rw16 - Inches(0.40), Inches(5.20))
    tf_r16 = tb_r16.text_frame
    tf_r16.word_wrap = True

    p16_h = tf_r16.paragraphs[0]
    p16_h.text = "THAO TÁC BITMASK & MỤC ĐÍCH ĐIỀU KHIỂN GPIO"
    p16_h.font.name = "Segoe UI"
    p16_h.font.bold = True
    p16_h.font.size = Pt(12)
    p16_h.font.color.rgb = C_GREEN
    p16_h.space_after = Pt(8)

    addr3_points = [
        ("1. Địa chỉ vật lý phần cứng:", "0x4000_0000 do soc_interconnect.v giải mã khi cpu_mem_addr[31:28] == 4'h4 (Slave 4: soc_gpio_mmio.v). Xuất tín hiệu ra 16 chân LED và Relay."),
        ("2. Phép toán Bitmask chuẩn mực:", "• Bit 0 (0x0001): LED nhịp tim (Heartbeat 1 Hz), đảo trạng thái bằng phép ^= 0x0001.\n• Bit 1 (0x0002): LED đỏ cảnh báo từ chối quẹt thẻ (Access Denied).\n• Bit 2 (0x0004): LED xanh mở cửa & kích hoạt Relay chốt điện từ (Access Granted).\n• Bit 3 (0x0008): LED vàng cảnh báo chip Flash đang bận xóa/ghi sector."),
        ("3. Mục đích thiết kế:", "Điều khiển cơ cấu chấp hành vật lý mở khóa cửa tại chỗ và cung cấp kênh chỉ thị thị giác trực quan về trạng thái hoạt động của toàn bộ hệ thống."),
        ("4. Tính an toàn thời gian thực:", "Thao tác ghi GPIO hoàn tất trong 1 chu kỳ clock (20ns), không tạo độ trễ đối với luồng quét thẻ.")
    ]

    for p_lbl, p_val in addr3_points:
        p = tf_r16.add_paragraph()
        p.text = f"• {p_lbl} {p_val}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.3)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(5)
        p.line_spacing = 1.15

    # =========================================================================
    # SLIDE 17: BIẾN ĐỊA CHỈ 4 - USER_FLASH_ADDR (0x0030_0000 - SECTOR 48)
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    add_header(s17, "Tầng Firmware C & Phần Cứng (Biến Địa Chỉ 4/6)",
               "Biến Địa Chỉ 4: USER_FLASH_ADDR (0x0030_0000 - Sector 48 Whitelist)", 17, total_slides=TOTAL_SLIDES)

    code_addr4 = [
        "// firmware/common/soc_regs.h - Vùng Whitelist Sector 48",
        "#define USER_FLASH_ADDR    0x300000   // Sector 48 (64KB)",
        "#define FLASH_SLOT_SIZE    16         // 16 bytes per tag record",
        "#define MAX_TAG_SLOTS      4096       // Tối đa 4096 thẻ",
        "#define FLASH_RECORD_MAGIC 0x52464944 // ASCII 'RFID'",
        "",
        "// firmware/drivers/flash.c - Tra cứu thẻ Whitelist qua XIP",
        "int flash_find_tag(uint32_t hi, uint32_t lo) {",
        "    for (int slot = 0; slot < MAX_TAG_SLOTS; slot++) {",
        "        uint32_t addr = USER_FLASH_ADDR + (uint32_t)(slot * 16);",
        "        uint32_t magic = flash_read_word(addr); // Đọc XIP trực tiếp",
        "        if (magic == 0xFFFFFFFF) return -1;    // Vùng trống -> Dừng ngay",
        "        if (magic == FLASH_RECORD_MAGIC) {",
        "            uint32_t s_hi = flash_read_word(addr + 4);",
        "            uint32_t s_lo = flash_read_word(addr + 8);",
        "            if (s_hi == hi && s_lo == lo) return slot; // Khớp thẻ!",
        "        }",
        "    }",
        "    return -1;",
        "}",
        "// firmware/drivers/flash.c - Lưu thẻ mới vào Flash",
        "int flash_save_tag(uint32_t hi, uint32_t lo, int *out_slot) {",
        "    int slot = flash_find_empty_tag_slot();",
        "    uint32_t addr = USER_FLASH_ADDR + (uint32_t)(slot * 16);",
        "    flash_write_word(addr + 4, hi);  flash_write_word(addr + 8, lo);",
        "    flash_write_word(addr + 12, hi ^ lo);",
        "    flash_write_word(addr + 0, FLASH_RECORD_MAGIC); // Commit",
        "    return 1;",
        "}"
    ]
    add_code_box(s17, Inches(0.8), Inches(1.30), Inches(5.75), Inches(5.50), "flash.c & soc_regs.h [Tag Whitelist Sector 48]", code_addr4, status_text="=== BASE: 0x0030_0000 | 4,096 SLOTS x 16B | XIP READ & WRITE ===", title_color=C_CYAN_ACCENT)

    rx17 = Inches(6.75)
    rw17 = Inches(5.78)
    add_card(s17, rx17, Inches(1.30), rw17, Inches(5.50), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
    tb_r17 = s17.shapes.add_textbox(rx17 + Inches(0.20), Inches(1.45), rw17 - Inches(0.40), Inches(5.20))
    tf_r17 = tb_r17.text_frame
    tf_r17.word_wrap = True

    p17_h = tf_r17.paragraphs[0]
    p17_h.text = "CƠ CHẾ LƯU TRỮ & TRA CỨU DANH SÁCH THẺ WHITELIST"
    p17_h.font.name = "Segoe UI"
    p17_h.font.bold = True
    p17_h.font.size = Pt(12)
    p17_h.font.color.rgb = C_BLUE_ACCENT
    p17_h.space_after = Pt(8)

    addr4_points = [
        ("1. Định vị vùng nhớ Flash:", "Sector 48 tại địa chỉ cơ sở 0x0030_0000 (kích thước 64KB) trên chip SPI Flash Spansion S25FL032P (4MB)."),
        ("2. Cấu trúc bản ghi 16 Bytes (Slot Record):", "• Offset +0 (4B): Magic Number 0x52464944 ('RFID') xác nhận slot hợp lệ.\n• Offset +4 (4B): UID Word High (tag_hi).\n• Offset +8 (4B): UID Word Low (tag_lo).\n• Offset +12 (4B): Checksum toàn vẹn (tag_hi ^ tag_lo)."),
        ("3. Cách thao tác trong C:", "• Tra cứu tức thì qua cơ chế XIP: CPU đọc thẳng vùng nhớ 0x300000 qua con trỏ con trỏ bộ nhớ mà không cần tải vào RAM.\n• Thuật toán Early Termination: Khi gặp slot có Magic == 0xFFFFFFFF (vùng Flash trắng chưa ghi), vòng lặp dừng ngay lập tức."),
        ("4. Mục đích thiết kế:", "Lưu trữ bền vững tới 4,096 thẻ nhân viên được phép mở cửa, bảo toàn dữ liệu vĩnh viễn không phụ thuộc nguồn điện.")
    ]

    for p_lbl, p_val in addr4_points:
        p = tf_r17.add_paragraph()
        p.text = f"• {p_lbl} {p_val}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.3)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(5)
        p.line_spacing = 1.15

    # =========================================================================
    # SLIDE 18: BIẾN ĐỊA CHỈ 5 - LOG_FLASH_ADDR (0x0031_0000 - SECTOR 49)
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    add_header(s18, "Tầng Firmware C & Phần Cứng (Biến Địa Chỉ 5/6)",
               "Biến Địa Chỉ 5: LOG_FLASH_ADDR (0x0031_0000 - Sector 49 Access Logs)", 18, total_slides=TOTAL_SLIDES)

    code_addr5 = [
        "// firmware/common/soc_regs.h - Vùng Nhật ký Sector 49",
        "#define LOG_FLASH_ADDR 0x310000   // Sector 49 (64KB)",
        "#define LOG_SLOT_SIZE  16         // 16 bytes per log record",
        "#define MAX_LOG_SLOTS  512        // 512 sự kiện kiểm toán",
        "#define LOG_MAGIC_SUCC 0x53554343 // 'SUCC' (Hợp lệ)",
        "#define LOG_MAGIC_FAIL 0x4641494C // 'FAIL' (Từ chối)",
        "",
        "// firmware/drivers/flash.c - Ghi nhật ký quẹt thẻ an toàn",
        "int flash_append_log(bool success, uint32_t hi, uint32_t lo) {",
        "    int slot = flash_find_empty_log_slot();",
        "    if (slot < 0) return -1; // Đầy bộ nhớ log",
        "    uint32_t addr = LOG_FLASH_ADDR + (uint32_t)(slot * 16);",
        "    uint32_t status = success ? LOG_MAGIC_SUCC : LOG_MAGIC_FAIL;",
        "    uint32_t seq = (uint32_t)(slot + 1);",
        "    REG_GPIO_LEDS |= 0x0008; // Flash LED active",
        "    flash_write_word(addr + 4, hi);",
        "    flash_write_word(addr + 8, lo);",
        "    flash_write_word(addr + 12, seq);",
        "    flash_write_word(addr + 0, status); // Ghi magic cuối cùng (Atomic Commit)!",
        "    REG_GPIO_LEDS &= ~0x0008;",
        "    return slot;",
        "}"
    ]
    add_code_box(s18, Inches(0.8), Inches(1.30), Inches(5.75), Inches(5.50), "flash.c & soc_regs.h [Access Logs Sector 49]", code_addr5, status_text="=== BASE: 0x0031_0000 | 512 AUDIT EVENTS x 16B | ATOMIC COMMIT ===", title_color=RGBColor(244, 63, 94))

    rx18 = Inches(6.75)
    rw18 = Inches(5.78)
    add_card(s18, rx18, Inches(1.30), rw18, Inches(5.50), bg_color=C_WHITE, border_color=C_ROSE, border_width=1.5)
    tb_r18 = s18.shapes.add_textbox(rx18 + Inches(0.20), Inches(1.45), rw18 - Inches(0.40), Inches(5.20))
    tf_r18 = tb_r18.text_frame
    tf_r18.word_wrap = True

    p18_h = tf_r18.paragraphs[0]
    p18_h.text = "GHI VẾT KIỂM TOÁN AN NINH (AUDIT TRAIL LOGGING)"
    p18_h.font.name = "Segoe UI"
    p18_h.font.bold = True
    p18_h.font.size = Pt(12)
    p18_h.font.color.rgb = C_ROSE
    p18_h.space_after = Pt(8)

    addr5_points = [
        ("1. Phân vùng nhật ký:", "Sector 49 tại địa chỉ cơ sở 0x0031_0000. Dành riêng 8KB đầu tiên lưu trữ tuần tự 512 sự kiện quẹt thẻ mới nhất."),
        ("2. Cấu trúc bản ghi sự kiện 16 Bytes:", "• Offset +0 (4B): Trạng thái mở cửa: 0x53554343 ('SUCC') hoặc 0x4641494C ('FAIL').\n• Offset +4 (4B): UID High của thẻ quẹt.\n• Offset +8 (4B): UID Low của thẻ quẹt.\n• Offset +12 (4B): Số thứ tự sự kiện (Sequence Number 1, 2, 3...)."),
        ("3. Kỹ thuật ghi chống hỏng dữ liệu (Atomic Commit):", "Dữ liệu UID và số thứ tự được ghi trước vào Flash, từ khóa Magic (SUCC/FAIL) được ghi sau cùng. Nếu mất điện giữa chừng, bản ghi chưa có Magic sẽ bị bỏ qua, chống rác dữ liệu!"),
        ("4. Mục đích thiết kế:", "Phục vụ công tác hậu kiểm, xuất file CSV lên máy tính để phát hiện các hành vi quẹt thẻ lạ hoặc dò tìm thẻ trái phép.")
    ]

    for p_lbl, p_val in addr5_points:
        p = tf_r18.add_paragraph()
        p.text = f"• {p_lbl} {p_val}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.3)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(5)
        p.line_spacing = 1.15

    # =========================================================================
    # SLIDE 19: BIẾN ĐỊA CHỈ 6 - 0x0200_0000 & FLASHIO_WORKER (SRAM ROUTINE)
    # =========================================================================
    s19 = prs.slides.add_slide(blank_layout)
    add_header(s19, "Tầng Firmware C & Phần Cứng (Biến Địa Chỉ 6/6)",
               "Biến Địa Chỉ 6: 0x0200_0000 & flashio_worker (Nạp Routine Vào SRAM)", 19, total_slides=TOTAL_SLIDES)

    code_addr6 = [
        "// firmware/start.s - Routine phát lệnh bit-bang SPI",
        ".global flashio_worker_begin, flashio_worker_end",
        "flashio_worker_begin:",
        "    li   t0, 0x02000000   # Địa chỉ SPICFG MMIO",
        "    sw   a2, 0(t0)        # Gửi lệnh WREN (0x06)",
        "    # ... Vòng lặp phát xung bit-bang SPI trên thanh ghi SPICFG ...",
        "    ret",
        "flashio_worker_end:",
        "",
        "// firmware/drivers/flash.c - Sao chép và thực thi trên 1KB SRAM",
        "static void flashio(uint8_t *data, int len, uint8_t wrencmd) {",
        "    // Cấp phát vùng nhớ hàm trên Stack (thuộc 1KB SRAM)",
        "    uint32_t func[&flashio_worker_end - &flashio_worker_begin];",
        "    uint32_t *src = &flashio_worker_begin;",
        "    uint32_t *dst = func;",
        "    while (src != &flashio_worker_end) *(dst++) = *(src++);",
        "",
        "    // Ép kiểu con trỏ hàm và thực thi thẳng trên SRAM!",
        "    ((void(*)(uint8_t*, uint32_t, uint32_t))func)(data, len, wrencmd);",
        "}"
    ]
    add_code_box(s19, Inches(0.8), Inches(1.30), Inches(5.75), Inches(5.50), "start.s & flash.c [In-SRAM Flash Worker]", code_addr6, status_text="=== SPICFG: 0x0200_0000 | COPIED TO SRAM @ 0x0000_0000 (ZERO-STALL) ===", title_color=RGBColor(167, 139, 250))

    rx19 = Inches(6.75)
    rw19 = Inches(5.78)
    add_card(s19, rx19, Inches(1.30), rw19, Inches(5.50), bg_color=C_WHITE, border_color=C_PURPLE, border_width=1.5)
    tb_r19 = s19.shapes.add_textbox(rx19 + Inches(0.20), Inches(1.45), rw19 - Inches(0.40), Inches(5.20))
    tf_r19 = tb_r19.text_frame
    tf_r19.word_wrap = True

    p19_h = tf_r19.paragraphs[0]
    p19_h.text = "CƠ CHẾ IN-SRAM EXECUTION GIẢI QUYẾT XUNG ĐỘT BUS"
    p19_h.font.name = "Segoe UI"
    p19_h.font.bold = True
    p19_h.font.size = Pt(12)
    p19_h.font.color.rgb = C_PURPLE
    p19_h.space_after = Pt(8)

    addr6_points = [
        ("1. Vấn đề xung đột bus cốt tử:", "CPU PicoRV32 đang kéo mã lệnh thực thi từ chip SPI Flash qua chế độ XIP. Khi muốn xóa sector hoặc ghi dữ liệu vào Flash, chip Flash sẽ bận và KHÔNG THỂ CUNG CẤP MÃ LỆNH CHO CPU -> Hệ thống sẽ bị treo vĩnh viễn!"),
        ("2. Giải pháp In-SRAM Execution:", "Sao chép đoạn mã máy flashio_worker từ Flash vào 1KB SRAM nội bộ và nhảy vào SRAM để thực thi. Trong suốt quá trình ghi Flash, CPU lấy mã lệnh từ 1KB SRAM nội mà không chạm vào Flash."),
        ("3. Tương tác địa chỉ 0x0200_0000:", "Đoạn mã worker ghi trực tiếp vào thanh ghi SPICFG tại 0x0200_0000 để bit-bang điều khiển chân CS, SCK, MOSI, MISO của chip Flash ngoài."),
        ("4. Ý nghĩa kỹ thuật đỉnh cao:", "Hiện thực hóa khả năng tự lập trình lại bộ nhớ không bay hơi (Self-Programming NVM) trên vi mạch SoC mà không cần thêm bộ nhớ ROM phụ trợ.")
    ]

    for p_lbl, p_val in addr6_points:
        p = tf_r19.add_paragraph()
        p.text = f"• {p_lbl} {p_val}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.3)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(5)
        p.line_spacing = 1.15

    # =========================================================================
    # SLIDE 20: PHẦN 5 - DEMO THỰC NGHIỆM TRÊN FPGA BASYS 3: THIẾT LẬP KẾT NỐI
    # =========================================================================
    s20 = prs.slides.add_slide(blank_layout)
    add_header(s20, "Phần 5: Demo Chức Năng Sản Phẩm", "Kiểm Chứng Thực Nghiệm Trên FPGA Basys 3: Thiết Lập Kết Nối Phần Cứng", 20, total_slides=TOTAL_SLIDES)

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
        add_card(s20, dx, Inches(1.4), Inches(3.75), Inches(5.3), bg_color=C_WHITE, border_color=ds_col, border_width=2.0)
        tb_d = s20.shapes.add_textbox(dx + Inches(0.18), Inches(1.6), Inches(3.39), Inches(4.9))
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
    # SLIDE 21: PHẦN 5 - DEMO THỰC NGHIỆM TRÊN FPGA BASYS 3: CÁC KỊCH BẢN THỰC TẾ
    # =========================================================================
    s21 = prs.slides.add_slide(blank_layout)
    add_header(s21, "Phần 5: Demo Chức Năng Sản Phẩm", "Các Kịch Bản Thực Nghiệm Quẹt Thẻ Thực Tế Trên FPGA Basys 3", 21, total_slides=TOTAL_SLIDES)

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

        add_card(s21, cx, cy, cw, ch, bg_color=C_WHITE, border_color=dc_col, border_width=2.0)
        tb_c = s21.shapes.add_textbox(cx + Inches(0.2), cy + Inches(0.15), cw - Inches(0.4), ch - Inches(0.3))
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
    # SLIDE 22: PHẦN 6 - THIẾT KẾ VẬT LÝ ASIC: LUỒNG OPENLANE 2 (SKYWATER 130NM)
    # =========================================================================
    s22 = prs.slides.add_slide(blank_layout)
    add_header(s22, "Phần 6: Thiết Kế Vật Lý ASIC", "Quy Trình Thiết Kế Vật Lý Vi Mạch RTL-to-GDSII Trên OpenLane 2", 22, total_slides=TOTAL_SLIDES)

    lx22 = Inches(0.8)
    lw22 = Inches(5.7)
    code_lines_22 = [
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
    add_code_box(s22, lx22, Inches(1.35), lw22, Inches(5.4), "Cấu hình config.json chính thức", code_lines_22)

    rx22 = Inches(6.8)
    rw22 = Inches(5.73)
    add_card(s22, rx22, Inches(1.35), rw22, Inches(5.4), bg_color=C_WHITE, border_color=C_ROSE, border_width=2.0)
    tb_r22 = s22.shapes.add_textbox(rx22 + Inches(0.2), Inches(1.5), rw22 - Inches(0.4), Inches(5.1))
    tf_r22 = tb_r22.text_frame
    tf_r22.word_wrap = True

    pr22 = tf_r22.paragraphs[0]
    pr22.text = "CÁC CHIẾN LƯỢC VẬT LÝ THEN CHỐT"
    pr22.font.name = "Segoe UI"
    pr22.font.size = Pt(13)
    pr22.font.bold = True
    pr22.font.color.rgb = C_ROSE
    pr22.space_after = Pt(10)

    asic_strategies = [
        ("Mật độ diện tích lõi 26% (FP_CORE_UTIL):", "Khởi tạo mật độ cell 26%, để lại 74% diện tích cho các kênh định tuyến kim loại và chèn diode bảo vệ plasma."),
        ("Ràng buộc xung nhịp 50 MHz (CLOCK_PERIOD = 20.0 ns):", "Ràng buộc định thời thống nhất từ khâu tổng hợp logic Yosys, xây dựng cây clock CTS tới khâu phân tích định thời tĩnh STA."),
        ("Chèn Diode phỏng đoán (HEURISTIC_ANTENNA_THRESHOLD = 24):", "Thuật toán tối ưu tự động chèn diode tiêu tán điện tích plasma khi tỷ lệ dây/cực cổng vượt ngưỡng 24, triệt tiêu 100% lỗi Antenna."),
        ("Biên an toàn Hold Guard-band 0.60 ns:", "Đảm bảo bộ tối ưu hóa tế bào Resizer xử lý sạch sẽ các vi phạm chạy đua dữ liệu (Hold Violations) sau bước đi dây chi tiết.")
    ]

    for p_lbl, p_val in asic_strategies:
        p = tf_r22.add_paragraph()
        p.text = f"• {p_lbl} {p_val}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(8)
        p.line_spacing = 1.15

    # =========================================================================
    # SLIDE 23: PHẦN 6 - THIẾT KẾ VẬT LÝ ASIC: BẢN VẼ LAYOUT & KÝ DUYỆT SIGN-OFF
    # =========================================================================
    s23 = prs.slides.add_slide(blank_layout)
    add_header(s23, "Phần 6: Thiết Kế Vật Lý ASIC", "Bản Vẽ Layout OpenROAD & Báo Cáo Ký Duyệt Sign-off Toàn Diện", 23, total_slides=TOTAL_SLIDES)

    if os.path.exists(img_openroad):
        add_card(s23, Inches(0.8), Inches(1.35), Inches(5.7), Inches(4.3), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
        s23.shapes.add_picture(img_openroad, Inches(0.9), Inches(1.45), Inches(5.5), Inches(4.1))

    if os.path.exists(img_signoff):
        add_card(s23, Inches(6.8), Inches(1.35), Inches(5.73), Inches(4.3), bg_color=C_WHITE, border_color=C_GREEN, border_width=1.5)
        s23.shapes.add_picture(img_signoff, Inches(6.9), Inches(1.45), Inches(5.53), Inches(4.1))

    add_card(s23, Inches(0.8), Inches(5.8), Inches(11.733), Inches(1.05), bg_color=C_WHITE, border_color=C_CARD_BORDER, border_width=1.5)
    tb_c23 = s23.shapes.add_textbox(Inches(0.95), Inches(5.85), Inches(11.4), Inches(0.95))
    tf_c23 = tb_c23.text_frame
    tf_c23.word_wrap = True

    p_c23_1 = tf_c23.paragraphs[0]
    p_c23_1.text = "KẾT QUẢ KÝ DUYỆT TAPE-OUT READY: 0 ANTENNA | 0 LVS | 0 DRC | MET TIMING 50 MHZ"
    p_c23_1.font.name = "Segoe UI"
    p_c23_1.font.size = Pt(11)
    p_c23_1.font.bold = True
    p_c23_1.font.color.rgb = C_GREEN
    p_c23_1.space_after = Pt(2)

    p_c23_2 = tf_c23.add_paragraph()
    p_c23_2.text = "• Bố cục vật lý: Lưới nguồn PDN met4/met5 dày đặc, phân bổ 31 chân pad đối xứng trên 4 cạnh die, độ sụt áp IR drop < 1.5% an toàn.\n• Định thời & Ký duyệt: WNS >= 0.00 ns tại 50 MHz trên cả 9 góc đo công nghệ từ -40°C đến 100°C; Netgen xác nhận 100% khớp netlist RTL."
    p_c23_2.font.name = "Segoe UI"
    p_c23_2.font.size = Pt(9.5)
    p_c23_2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 24: TỔNG KẾT ĐỀ TÀI & HƯỚNG PHÁT TRIỂN (THANK YOU SLIDE)
    # =========================================================================
    s24 = prs.slides.add_slide(blank_layout)
    bg24 = s24.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg24.fill.solid()
    bg24.fill.fore_color.rgb = C_NAVY_DARK
    bg24.line.fill.background()

    card24 = s24.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
    card24.fill.solid()
    card24.fill.fore_color.rgb = C_NAVY_MID
    card24.line.color.rgb = C_BLUE_ACCENT
    card24.line.width = Pt(2.0)

    tb_t24 = s24.shapes.add_textbox(Inches(1.2), Inches(1.1), Inches(10.9), Inches(5.3))
    tf_t24 = tb_t24.text_frame
    tf_t24.word_wrap = True

    p_end1 = tf_t24.paragraphs[0]
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
        p = tf_t24.add_paragraph()
        p.text = f"{c_title} {c_desc}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.space_after = Pt(8)
        p.line_spacing = 1.15

    p_ty = tf_t24.add_paragraph()
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
