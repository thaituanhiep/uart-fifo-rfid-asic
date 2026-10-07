# -*- coding: utf-8 -*-
"""
Script: generate_report_docx.py
Tạo báo cáo đồ án Word (.docx) chuyên nghiệp, chuẩn mực học thuật cao cấp theo đúng 6 Phần Cốt Lõi của Slide:
- Trang bìa: FPT Jetking Chip Design - SEM3
- Phần 1: Giới thiệu dự án & Lý do lựa chọn SPI Flash NVM
- Phần 2: Nền tảng phần cứng & Chuỗi công cụ phát triển
- Phần 3: Kiến trúc vi hệ thống SoC & Vi mạch UART RTL (5 giai đoạn Co-Design, so sánh RTL vs C, sơ đồ khối UART, 6 biến địa chỉ phần cứng)
- Phần 4: Hệ thống Testbench & Kiểm thử mô phỏng (tb_uart_rtl waveform & tb_uart_ping code/log)
- Phần 5: Demo thực nghiệm trên FPGA Basys 3 (Thiết lập mạch nguồn 5V/trở 1k, CLI 10 chức năng, kịch bản quẹt thẻ)
- Phần 6: Thiết kế vật lý ASIC & Ký duyệt Sign-off (OpenLane 2 Sky130, Layout OpenROAD, PPA & 3 chỉ số Sign-off)
- Kết luận & Hướng phát triển
"""

import os
import shutil
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def generate_report():
    doc = Document()

    # Thiết lập lề chuẩn đồ án: Trái 3cm (1.18 in), Phải 2cm (0.79 in), Trên 2cm (0.79 in), Dưới 2cm (0.79 in)
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(0.85)
        s.bottom_margin = Inches(0.85)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(0.85)

    # Bảng màu đơn sắc chuẩn in ấn học thuật (Black & Grayscale)
    BLACK = RGBColor(0, 0, 0)
    DARK_GRAY = RGBColor(60, 60, 60)
    MID_GRAY = RGBColor(100, 100, 100)
    NAVY = RGBColor(11, 19, 43)
    BLUE_ACCENT = RGBColor(37, 99, 235)

    # -------------------------------------------------------------
    # CÁC HÀM TIỆN ÍCH ĐỊNH DẠNG VĂN BẢN
    # -------------------------------------------------------------
    def set_font(run, name="Times New Roman", size=11, bold=False, italic=False, color=BLACK):
        run.font.name = name
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = color

    def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(
            f'<w:tcMar {nsdecls("w")}>'
            f'<w:top w:w="{top}" w:type="dxa"/>'
            f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
            f'<w:left w:w="{left}" w:type="dxa"/>'
            f'<w:right w:w="{right}" w:type="dxa"/>'
            f'</w:tcMar>'
        )
        tcPr.append(tcMar)

    def style_table(table, col_widths, alignments, font_size=9.5):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        for r_idx, row in enumerate(table.rows):
            is_header = (r_idx == 0)
            trPr = row._tr.get_or_add_trPr()
            trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
            if is_header:
                trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

            for c_idx, cell in enumerate(row.cells):
                cell.width = col_widths[c_idx]
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
                
                shading_color = "E6E6E6" if is_header else ("F7F7F7" if r_idx % 2 == 1 else "FFFFFF")
                tcPr = cell._tc.get_or_add_tcPr()
                shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{shading_color}"/>')
                tcPr.append(shd)

                borders = parse_xml(
                    f'<w:tcBorders {nsdecls("w")}>'
                    f'<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
                    f'<w:bottom w:val="{"single" if is_header else "single"}" w:sz="{"12" if is_header else "4"}" w:space="0" w:color="000000"/>'
                    f'<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
                    f'<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
                    f'</w:tcBorders>'
                )
                tcPr.append(borders)

                for p in cell.paragraphs:
                    p.alignment = alignments[c_idx]
                    p.paragraph_format.space_before = Pt(1.5)
                    p.paragraph_format.space_after = Pt(1.5)
                    p.paragraph_format.line_spacing = 1.05
                    for run in p.runs:
                        fn = run.font.name if run.font.name else "Times New Roman"
                        set_font(run, name=fn, size=font_size, bold=(is_header or bool(run.bold)), color=BLACK)

    def add_p(text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=3.5, line_spacing=1.15):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        r = p.add_run(text)
        set_font(r, size=11, color=BLACK)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        set_font(r, size=13.5, bold=True, color=BLACK)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        set_font(r, size=12, bold=True, color=BLACK)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        set_font(r, size=11, bold=True, italic=True, color=BLACK)
        return p

    def add_bullet(bold_prefix="", text=""):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(1.5)
        p.paragraph_format.space_after = Pt(2.5)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r1 = p.add_run(bold_prefix)
            set_font(r1, bold=True, color=BLACK)
        if text:
            r2 = p.add_run(text)
            set_font(r2, color=BLACK)
        return p

    def add_caption(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(8)
        r = p.add_run(text)
        set_font(r, size=9.5, italic=True, color=DARK_GRAY)
        return p

    def add_console_block(lines):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.27)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            f'<w:left w:val="single" w:sz="18" w:space="0" w:color="000000"/>'
            f'<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F5F5F5"/>')
        tcPr.append(shd)
        set_cell_margins(cell, top=70, bottom=70, left=100, right=100)

        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.05
        for i, line in enumerate(lines):
            r = p.add_run(line + ("\n" if i < len(lines)-1 else ""))
            set_font(r, name="Consolas", size=8.5, color=BLACK)

        doc.add_paragraph().paragraph_format.space_after = Pt(2)

    cur_dir = os.path.dirname(os.path.abspath(__file__))
    doc_dir = os.path.dirname(cur_dir) if os.path.basename(cur_dir) == "temp" else cur_dir
    project_root = os.path.dirname(doc_dir)

    # Khai báo đường dẫn các ảnh
    img_fig1 = os.path.join(cur_dir, "fig1_block_diagram.png")
    if not os.path.exists(img_fig1): img_fig1 = os.path.join(doc_dir, "fig1_block_diagram.png")

    img_stages = [os.path.join(cur_dir, f"stage{i}_bw_diagram.png") for i in range(1, 6)]
    for i in range(5):
        if not os.path.exists(img_stages[i]):
            img_stages[i] = os.path.join(doc_dir, f"stage{i}_bw_diagram.png")

    img_uart_bw = os.path.join(cur_dir, "uart_architecture_bw_diagram.png")
    if not os.path.exists(img_uart_bw): img_uart_bw = os.path.join(doc_dir, "uart_architecture_bw_diagram.png")

    img_tb_uart_rtl = os.path.join(cur_dir, "waveform_tb_uart_rtl.png")
    if not os.path.exists(img_tb_uart_rtl): img_tb_uart_rtl = os.path.join(doc_dir, "waveform_tb_uart_rtl.png")

    img_device = os.path.join(project_root, "Device.jpg")
    if not os.path.exists(img_device): img_device = os.path.join(cur_dir, "Device.jpg")
    if not os.path.exists(img_device): img_device = os.path.join(doc_dir, "Device.jpg")

    img_openroad = os.path.join(project_root, "OpenROAD.png")
    if not os.path.exists(img_openroad): img_openroad = os.path.join(cur_dir, "OpenROAD.png")
    if not os.path.exists(img_openroad): img_openroad = os.path.join(cur_dir, "Openroad_1.png")

    img_signoff = os.path.join(project_root, "AntennaLvsDrc.png")
    if not os.path.exists(img_signoff): img_signoff = os.path.join(cur_dir, "AntennaLvsDrc.png")

    # =============================================================
    # TRANG BÌA (COVER PAGE)
    # =============================================================
    p_univ = add_p("FPT JETKING — CHIP DESIGN", 
                   align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=4)
    set_font(p_univ.runs[0], size=14, bold=True, color=NAVY)

    p_dep = add_p("BÁO CÁO ĐỒ ÁN TỐT NGHIỆP THIẾT KẾ VI MẠCH BÁN DẪN (CHIP DESIGN)", 
                  align=WD_ALIGN_PARAGRAPH.CENTER, space_after=20)
    set_font(p_dep.runs[0], size=11, bold=True, color=DARK_GRAY)

    p_border_top = add_p("----------------------------------------------------------------------------------------------------", 
                         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    set_font(p_border_top.runs[0], size=8, color=MID_GRAY)

    p_topic_lbl = add_p("TÊN ĐỀ TÀI:", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    set_font(p_topic_lbl.runs[0], size=12, bold=True, color=DARK_GRAY)

    p_title = add_p("THIẾT KẾ HỆ THỐNG XỬ LÝ DỮ LIỆU CỦA THẺ RA VÀO RFID 125KHZ OFFLINE\nTÍCH HỢP CPU RISC-V PICORV32 & XỬ LÝ NGHIỆP VỤ DỮ LIỆU THẺ BẰNG FIRMWARE C", 
                    align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14, line_spacing=1.25)
    set_font(p_title.runs[0], size=15, bold=True, color=BLACK)

    p_sub = add_p("Giao tiếp RFID RDM6300 | Lưu trữ Whitelist SPI Flash NVM | Tạo mẫu Basys 3 FPGA | Ký duyệt ASIC OpenLane 2 (Sky130)", 
                  align=WD_ALIGN_PARAGRAPH.CENTER, space_after=16)
    set_font(p_sub.runs[0], size=10.5, italic=True, color=DARK_GRAY)

    p_border_bot = add_p("----------------------------------------------------------------------------------------------------", 
                         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=35)
    set_font(p_border_bot.runs[0], size=8, color=MID_GRAY)

    p_std_hdr = add_p("THÔNG TIN THỰC HIỆN ĐỒ ÁN:", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=10, space_after=3)
    set_font(p_std_hdr.runs[0], size=11, bold=True, color=BLACK)
    
    p_std_val = add_p("Học viên thực hiện : Thái Tuấn Hiệp\nGiảng viên hướng dẫn : ThS. Nguyễn Văn Đông\nHọc kỳ đào tạo      : SEM3 (Chuyên ngành Thiết kế Vi mạch Bán dẫn - Chip Design)", 
                      align=WD_ALIGN_PARAGRAPH.LEFT, space_after=45, line_spacing=1.2)
    set_font(p_std_val.runs[0], size=11, color=BLACK)

    p_date = add_p("HÀ NỘI – 2026", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    set_font(p_date.runs[0], size=11, bold=True, color=BLACK)

    p_ref = add_p("Kho lưu trữ mã nguồn mở: github.com/thaituanhiep/uart-fifo-rfid-asic", 
                  align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0, line_spacing=1.15)
    set_font(p_ref.runs[0], size=9.5, italic=True, color=DARK_GRAY)

    doc.add_page_break()

    # =============================================================
    # TRANG 2: MỤC LỤC CHUẨN XÁC 6 PHẦN THEO SLIDE
    # =============================================================
    add_h1("Mục Lục Báo Cáo")
    
    toc_items = [
        ("Phần 1: Giới thiệu dự án & Lý do lựa chọn SPI Flash NVM", "3", True, 0),
        ("1.1. Bối cảnh công nghệ và định hướng thiết bị kiểm soát ra vào Offline", "3", False, 0.2),
        ("1.2. Vai trò cốt tử của bộ nhớ bất biến SPI Flash NVM (Whitelist & Logs)", "3", False, 0.2),
        ("Phần 2: Nền tảng phần cứng & Chuỗi công cụ phát triển", "4", True, 0),
        ("2.1. Lựa chọn phần cứng: Bo mạch FPGA Basys 3 & Đầu đọc RFID RDM6300", "4", False, 0.2),
        ("2.2. Chuỗi công cụ phát triển: FPGA Vivado, ASIC OpenLane 2 & RISC-V GCC", "4", False, 0.2),
        ("Phần 3: Kiến trúc vi hệ thống SoC & Vi mạch UART RTL", "5", True, 0),
        ("3.1. Sơ đồ khối kiến trúc vi hệ thống SoC PicoRV32 (1 Master - 5 Slaves)", "5", False, 0.2),
        ("3.2. Quy trình 5 giai đoạn thiết kế vi hệ thống SoC (Co-Design)", "6", False, 0.2),
        ("3.3. So sánh kiến trúc: Thiết kế UART trên phần cứng RTL vs Viết bằng Firmware C", "9", False, 0.2),
        ("3.4. Sơ đồ khối kiến trúc vi mạch UART RTL (5 tầng chức năng)", "10", False, 0.2),
        ("3.5. Chi tiết 6 biến địa chỉ phần cứng cốt lõi trong Firmware C", "11", False, 0.2),
        ("Phần 4: Hệ thống Testbench & Kiểm thử mô phỏng", "14", True, 0),
        ("4.1. Testbench 1: Kiểm thử RTL thuần cho UART MMIO & FIFO (tb_uart_rtl.v)", "14", False, 0.2),
        ("4.2. Testbench 2: Kiểm thử tích hợp toàn diện Top SoC Boot Flash & Ping (tb_uart_ping.v)", "15", False, 0.2),
        ("Phần 5: Demo thực nghiệm trên bo mạch FPGA Basys 3", "16", True, 0),
        ("5.1. Thiết lập mạch phần cứng thực tế (Nguồn ngoài 5V MB102 & Trở đệm 1kΩ)", "16", False, 0.2),
        ("5.2. Giao diện quản trị Host Console CLI 10 chức năng & Kịch bản quẹt thẻ thực tế", "17", False, 0.2),
        ("Phần 6: Thiết kế vật lý ASIC & Ký duyệt Sign-off", "18", True, 0),
        ("6.1. Quy trình thiết kế vật lý RTL-to-GDSII trên OpenLane 2 (SkyWater 130nm)", "18", False, 0.2),
        ("6.2. Bản vẽ Layout OpenROAD, chỉ số PPA và báo cáo ký duyệt Sign-off toàn diện", "19", False, 0.2),
        ("Kết luận & Hướng phát triển đồ án", "20", True, 0),
    ]

    tbl_toc = doc.add_table(rows=len(toc_items), cols=2)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (title, page, is_major, indent) in enumerate(toc_items):
        r = tbl_toc.rows[idx]
        c0 = r.cells[0]
        c1 = r.cells[1]
        c0.width = Inches(5.6)
        c1.width = Inches(0.67)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.left_indent = Inches(indent)
        p0.paragraph_format.space_before = Pt(2.5 if is_major else 1.0)
        p0.paragraph_format.space_after = Pt(2.5 if is_major else 1.0)
        p0.paragraph_format.line_spacing = 1.05
        run0 = p0.add_run(title)
        set_font(run0, size=10 if is_major else 9.5, bold=is_major, color=BLACK)

        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.space_before = Pt(2.5 if is_major else 1.0)
        p1.paragraph_format.space_after = Pt(2.5 if is_major else 1.0)
        p1.paragraph_format.line_spacing = 1.05
        run1 = p1.add_run(page)
        set_font(run1, size=10 if is_major else 9.5, bold=is_major, color=BLACK)

        for cell in [c0, c1]:
            set_cell_margins(cell, top=20, bottom=20, left=40, right=40)
            borders = parse_xml(
                f'<w:tcBorders {nsdecls("w")}>'
                f'<w:top w:val="none"/>'
                f'<w:bottom w:val="none"/>'
                f'<w:left w:val="none"/>'
                f'<w:right w:val="none"/>'
                f'</w:tcBorders>'
            )
            cell._tc.get_or_add_tcPr().append(borders)

    doc.add_page_break()

    # =============================================================
    # PHẦN 1: GIỚI THIỆU DỰ ÁN & LÝ DO LỰA CHỌN SPI FLASH NVM
    # =============================================================
    add_h1("Phần 1: Giới Thiệu Dự Án & Lý Do Lựa Chọn SPI Flash NVM")
    
    add_h2("1.1. Bối cảnh công nghệ và định hướng thiết bị kiểm soát ra vào Offline")
    add_p("Trong các hệ thống an ninh hiện đại tại các nhà máy, văn phòng, phòng thí nghiệm trọng yếu và trạm thu phí tự động, nhu cầu kiểm soát quyền ra vào thông qua thẻ RFID không tiếp xúc là vô cùng cấp thiết. Tuy nhiên, phần lớn các thiết bị kiểm soát hiện nay trên thị trường phụ thuộc hoàn toàn vào kết nối mạng Ethernet hoặc Wi-Fi liên tục với máy chủ cơ sở dữ liệu trung tâm.")
    add_p("Kiến trúc phụ thuộc mạng này bộc lộ 3 điểm yếu chí tử trong vận hành thực tế:")
    add_bullet("1. Nguy cơ tắc nghẽn và ngắt quãng: ", "Khi mạng nội bộ bị quá tải, đứt cáp mạng hoặc thiết bị phát Wi-Fi gặp sự cố, cửa ra vào sẽ bị vô hiệu hóa hoàn toàn hoặc gây tắc nghẽn nghiêm trọng.")
    add_bullet("2. Độ trễ xác thực lớn: ", "Quá trình gửi yêu cầu truy vấn qua giao thức HTTP/TCP lên máy chủ và chờ phản hồi làm tăng thời gian mở cửa lên từ 500ms đến 2 giây, không đáp ứng được yêu cầu lưu thông nhanh.")
    add_bullet("3. Rủi ro an ninh mạng: ", "Hệ thống kết nối trực tuyến dễ trở thành mục tiêu của các cuộc tấn công từ chối dịch vụ (DoS), giả mạo địa chỉ IP (IP Spoofing) hoặc nghe lén gói tin.")
    add_p("Chính vì vậy, đồ án tập trung thiết kế một hệ thống vi mạch trên chip (System-on-Chip - SoC) hoạt động theo cơ chế **Offline Độc Lập Hoàn Toàn (Stand-alone)**. Thiết bị tự lưu trữ danh sách thẻ hợp lệ (Whitelist) và tự đối soát, xác thực, ghi vết nhật ký ra vào (Access Log) với thời gian phản hồi tức thì dưới 1 mili-giây mà không cần bất kỳ kết nối mạng nào.")

    add_h2("1.2. Vai trò cốt tử của bộ nhớ bất biến SPI Flash NVM (Whitelist & Logs)")
    add_p("Do hệ thống vận hành hoàn toàn Offline, yêu cầu đặt ra cho bộ nhớ lưu trữ là phải lưu giữ được dữ liệu vĩnh viễn khi mất điện đột ngột (Non-Volatile Memory - NVM), đồng thời cho phép CPU đọc mã lệnh thực thi với tốc độ cao và cho phép ghi/xóa linh hoạt khi quản trị viên thêm hoặc thu hồi quyền của thẻ.")
    
    # Bảng so sánh các giải pháp bộ nhớ
    t_mem = doc.add_table(rows=4, cols=5)
    mem_headers = ["Loại Bộ Nhớ", "Khả Năng Lưu Dữ Liệu", "Khả Năng Ghi Lại", "Tốc Độ & Tài Nguyên", "Đánh Giá Trong Đồ Án"]
    for i, h in enumerate(mem_headers):
        t_mem.cell(0, i).paragraphs[0].text = h
    
    mem_rows = [
        ["Mặt nạ ROM (Mask ROM)", "Không mất khi mất điện", "Cố định từ lúc đúc chip, KHÔNG thể sửa", "Chi phí diện tích nhỏ", "Không thể cập nhật thêm/xóa thẻ mới!"],
        ["Bộ nhớ SRAM nội bộ", "MẤT TOÀN BỘ khi mất điện", "Ghi/đọc cực nhanh từng chu kỳ", "Tốn diện tích Si lớn (6T/bit)", "Không thể dùng lưu cơ sở dữ liệu thẻ!"],
        ["Bộ nhớ SPI Flash NVM (Được chọn)", "Bất biến vĩnh viễn (> 20 năm)", "Ghi / Xóa theo từng Sector linh hoạt", "Tiết kiệm chân (4-wire SPI), dung lượng lớn", "LỰA CHỌN TỐI ƯU: Lưu Whitelist & Logs an toàn!"]
    ]
    for r_idx, row_data in enumerate(mem_rows):
        for c_idx, val in enumerate(row_data):
            t_mem.cell(r_idx + 1, c_idx).paragraphs[0].text = val
            
    style_table(t_mem, [Inches(1.2), Inches(1.2), Inches(1.3), Inches(1.3), Inches(1.27)], 
                [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT])
    add_caption("Bảng 1.1: So sánh đặc tính các loại bộ nhớ và lý do lựa chọn SPI Flash NVM trong thiết kế SoC")

    # =============================================================
    # PHẦN 2: NỀN TẢNG PHẦN CỨNG & CHUỖI CÔNG CỤ PHÁT TRIỂN
    # =============================================================
    add_h1("Phần 2: Nền Tảng Phần Cứng & Chuỗi Công Cụ Phát Triển")
    
    add_h2("2.1. Lựa chọn phần cứng: Bo mạch FPGA Basys 3 & Đầu đọc RFID RDM6300")
    add_p("Hệ thống được hiện thực hóa và kiểm chứng trên nền tảng phần cứng tiêu chuẩn công nghiệp:")
    add_bullet("Bo mạch FPGA Digilent Basys 3 (Xilinx Artix-7 XC7A35T): ", "Bo mạch tạo mẫu lý tưởng với 33,280 tế bào logic (Logic Cells), 50 khối Block RAM 36Kb, tích hợp sẵn chip SPI Flash ngoài 32MB Spansion S25FL032P và chip FTDI chuyển đổi UART-USB nối thẳng vào máy tính.")
    add_bullet("Module Đầu Đọc Thẻ RFID 125 kHz RDM6300: ", "Hoạt động ở tần số sóng mang 125 kHz, khoảng cách đọc 20 - 50 mm. Sau khi giải điều chế sóng vô tuyến từ thẻ EM4100, module tự động truyền chuỗi 14 byte nối tiếp chuẩn UART (9600-8-N-1): Byte mở đầu 0x02, 10 ký tự ASCII biểu diễn mã UID thẻ, 2 ký tự mã kiểm tra Checksum XOR và byte kết thúc 0x03.")

    add_h2("2.2. Chuỗi công cụ phát triển: FPGA Vivado, ASIC OpenLane 2 & RISC-V GCC")
    add_p("Quy trình thiết kế vi mạch được xây dựng khép kín bằng chuỗi công cụ phát triển EDA chuẩn mực:")
    add_bullet("Chuỗi Công Cụ FPGA (AMD/Xilinx Vivado ML Standard 2025.1): ", "Đảm nhận toàn bộ chu trình tổng hợp RTL, tối ưu hóa công nghệ, phân tích định thời tĩnh, bố trí vị trí tế bào logic (Placement & Routing) và nạp file cấu hình Bitstream lên kit Basys 3.")
    add_bullet("Chuỗi Công Cụ ASIC OpenLane 2 (Tiến trình SkyWater 130nm): ", "Chuỗi công cụ mã nguồn mở tự động hóa quy trình RTL-to-GDSII từ tổng hợp logic Yosys, chèn cây xung nhịp CTS TritonCTS, định tuyến OpenROAD đến ký duyệt vật lý Magic/KLayout/Netgen.")
    add_bullet("Trình Biên Dịch Chéo RISC-V GNU GCC (RV32I): ", "Trình biên dịch gcc mã nguồn mở biên dịch mã nguồn C và mã khởi động Assembly thành mã máy nhị phân 32-bit (firmware.hex) để nạp vào mô hình SPI Flash và chip nhớ thật.")

    # =============================================================
    # PHẦN 3: KIẾN TRÚC VI HỆ THỐNG SOC & VI MẠCH UART RTL
    # =============================================================
    add_h1("Phần 3: Kiến Trúc Vi Hệ Thống SoC & Vi Mạch UART RTL")
    
    add_h2("3.1. Sơ đồ khối kiến trúc vi hệ thống SoC PicoRV32 (1 Master - 5 Slaves)")
    add_p("Kiến trúc vi hệ thống trên chip (SoC) được tổ chức theo mô hình **1 Master - 5 Slaves** trên nền bus 32-bit tối ưu hóa độ trễ:")
    add_bullet("Khối Master Cốt Lõi: ", "CPU RISC-V PicoRV32 (32-bit RISC-V RV32I) chịu trách nhiệm kéo mã lệnh và thực thi logic.")
    add_bullet("Slave 0 - Bộ Điều Khiển SPI Flash (spimemio.v): ", "Địa chỉ 0x0025_0000 - 0x003F_FFFF (Chế độ đọc XIP) & 0x0200_0000 (Thanh ghi cấu hình SPICFG điều khiển bit-bang CS, SCK, MOSI, MISO).")
    add_bullet("Slave 1 - Bộ Nhớ 1KB Data SRAM (data_sram.v): ", "Địa chỉ 0x0000_0000 - 0x0000_03FF. Chứa Stack, biến toàn cục và đoạn mã worker lập trình Flash.")
    add_bullet("Slave 2 - Ngoại Vi RFID UART MMIO (uart_mmio.v): ", "Địa chỉ 0x1000_0000 - 0x1000_0007. Kết nối chân RX module RDM6300 với hàng đợi FIFO 32 byte.")
    add_bullet("Slave 3 - Ngoại Vi Host PC UART MMIO (uart_mmio.v): ", "Địa chỉ 0x3000_0000 - 0x3000_0007. Kết nối cổng micro-USB máy tính truyền nhận lệnh CLI quản trị.")
    add_bullet("Slave 4 - Ngoại Vi Điều Khiển GPIO MMIO (soc_gpio_mmio.v): ", "Địa chỉ 0x4000_0000 - 0x4000_0003. Điều khiển 4 LED trạng thái và tín hiệu Relay mở chốt cửa điện từ.")

    if os.path.exists(img_fig1):
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.paragraphs[-1].paragraph_format.space_before = Pt(4)
        doc.paragraphs[-1].paragraph_format.space_after = Pt(2)
        doc.paragraphs[-1].add_run().add_picture(img_fig1, width=Inches(6.0))
        add_caption("Hình 3.1: Sơ đồ khối kiến trúc vi hệ thống trên chip SoC PicoRV32 (1 Master - 5 Slaves)")

    add_h2("3.2. Quy trình 5 giai đoạn thiết kế vi hệ thống SoC (Co-Design)")
    add_p("Vi hệ thống SoC được thiết kế tuần tự và chặt chẽ qua 5 giai đoạn đồng thiết kế Phần cứng - Phần mềm:")

    # Giai đoạn 1
    add_h3("Giai đoạn 1: Khối Cốt Lõi Có Sẵn & Bổ Sung 1KB Data SRAM")
    add_p("Tận dụng lõi CPU PicoRV32 mã nguồn mở và bộ điều khiển SPI Flash spimemio.v của Claire Wolf. Để hệ thống có thể chạy được mã nguồn C tự do mà không phụ thuộc vào bộ nhớ ngoài, tiến hành thiết kế thêm khối **1KB Data SRAM (data_sram.v)** tại địa chỉ cơ sở `0x0000_0000`. Khối SRAM nội này đóng vai trò sống còn làm không gian Stack con trỏ ngăn xếp và vùng nhớ dữ liệu tĩnh cho chương trình C.")
    if os.path.exists(img_stages[0]):
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.paragraphs[-1].add_run().add_picture(img_stages[0], width=Inches(5.8))
        add_caption("Hình 3.2: Sơ đồ khối Giai đoạn 1 - Khối cốt lõi có sẵn & Bổ sung 1KB Data SRAM")

    # Giai đoạn 2
    add_h3("Giai đoạn 2: Thiết Kế Cầu Nối Bus Interconnect Tối Ưu")
    add_p("Thiết kế module cầu nối trung tâm **soc_interconnect.v**. Module này giải mã dải địa chỉ 32-bit từ CPU, phân phối tín hiệu `mem_valid` và `mem_wstrb` tới đúng 1 trong 5 Slave, đồng thời gom tín hiệu phản hồi `mem_ready` và dữ liệu `mem_rdata` trả về CPU PicoRV32. Cơ chế giải mã địa chỉ tĩnh không qua arbiter phức tạp giúp giảm thiểu diện tích cell logic và đạt độ trễ truy xuất chỉ 1 chu kỳ xung nhịp đối với SRAM.")
    if os.path.exists(img_stages[1]):
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.paragraphs[-1].add_run().add_picture(img_stages[1], width=Inches(5.8))
        add_caption("Hình 3.3: Sơ đồ khối Giai đoạn 2 - Thiết kế cầu nối Bus Interconnect tối ưu")

    # Giai đoạn 3
    add_h3("Giai đoạn 3: Đồng Thiết Kế Phần Cứng - Phần Mềm & Bootstrap")
    add_p("Xây dựng tệp liên kết bộ nhớ **sections.lds** và mã khởi động Assembly **start.s**. CPU PicoRV32 thức dậy tại địa chỉ `0x0025_0000` ngay sau khi giải phóng Reset, thiết lập con trỏ ngăn xếp `sp = 0x000003F0` trên SRAM, sao chép dữ liệu `.data` và xóa sạch vùng nhớ `.bss`, sau đó gọi hàm `main()` của Firmware C. Kiến trúc này cho phép CPU kéo trực tiếp mã lệnh từ SPI Flash qua cơ chế thực thi tại chỗ (Execute-In-Place - XIP).")
    if os.path.exists(img_stages[2]):
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.paragraphs[-1].add_run().add_picture(img_stages[2], width=Inches(5.8))
        add_caption("Hình 3.4: Sơ đồ khối Giai đoạn 3 - Đồng thiết kế Phần cứng - Phần mềm & Bootstrap")

    # Giai đoạn 4
    add_h3("Giai đoạn 4: Mở Rộng Ngoại Vi MMIO Với Hàng Đợi FIFO Chống Tràn")
    add_p("Thiết kế các khối ngoại vi phần cứng giao tiếp qua thanh ghi ánh xạ bộ nhớ (Memory-Mapped I/O - MMIO): khối UART tùy biến **uart_mmio.v** tích hợp hàng đợi **sync_fifo.v 32 byte** chống tràn dữ liệu khi CPU bận ghi Flash, và khối điều khiển LED/Relay **soc_gpio_mmio.v**.")
    if os.path.exists(img_stages[3]):
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.paragraphs[-1].add_run().add_picture(img_stages[3], width=Inches(5.8))
        add_caption("Hình 3.5: Sơ đồ khối Giai đoạn 4 - Mở rộng ngoại vi MMIO với hàng đợi FIFO chống tràn")

    # Giai đoạn 5
    add_h3("Giai đoạn 5: Tầng Firmware C Tương Tác Qua Con Trỏ Volatile MMIO")
    add_p("Phát triển toàn bộ tầng ứng dụng quản trị bằng ngôn ngữ C (`soc_regs.h`, `access_control.c`, `uart.c`, `flash.c`). Mã C sử dụng các con trỏ `volatile uint32_t*` để đọc ghi trực tiếp các thanh ghi phần cứng, hiện thực hóa 10 chức năng quản lý thẻ, xác thực đối soát Whitelist và ghi vết kiểm toán Access Log an toàn.")
    if os.path.exists(img_stages[4]):
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.paragraphs[-1].add_run().add_picture(img_stages[4], width=Inches(5.8))
        add_caption("Hình 3.6: Sơ đồ khối Giai đoạn 5 - Tầng Firmware C tương tác qua con trỏ volatile MMIO")

    add_h2("3.3. So sánh kiến trúc: Thiết kế UART trên phần cứng RTL vs Viết bằng Firmware C")
    add_p("Trong thiết kế hệ thống nhúng SoC, việc phân định ranh giới giữa phần cứng (RTL) và phần mềm (Firmware C) là bài toán then chốt để đạt tối ưu hóa diện tích và độ tin cậy:")
    
    t_comp = doc.add_table(rows=7, cols=4)
    comp_headers = ["Tiêu Chí So Sánh", "Thiết Kế Trên Phần Cứng RTL (uart_mmio.v)", "Xử Lý Bằng Phần Mềm C (Firmware)", "Đánh Giá Kiến Trúc SoC"]
    for i, h in enumerate(comp_headers):
        t_comp.cell(0, i).paragraphs[0].text = h
        
    comp_rows = [
        ["Định thời xung Baud Rate", "Mạch chia tần số phần cứng chính xác từng xung nhịp", "Phụ thuộc vòng lặp delay mềm, dễ sai lệch khi CPU bận", "RTL bảo đảm không lệch baud!"],
        ["Đệm dữ liệu thu (RX Buffer)", "Hàng đợi phần cứng FIFO 32 byte chạy nền tự động", "Polling ngắt quãng, dễ mất mát byte khi ghi Flash", "RTL chống tràn dữ liệu tuyệt đối!"],
        ["Giải mã khung truyền", "FSM 4 trạng thái (IDLE, START, DATA, STOP)", "Xử lý chuỗi ASCII, tách Checksum, phân tích lệnh", "Phối hợp: RTL bắt bit, C xử lý chuỗi!"],
        ["Đồng bộ chống Metastability", "Mạch 2 tầng D-FF (sync_2ff.v) khử nhiễu tín hiệu RX", "Không thể thực hiện bằng phần mềm", "Bắt buộc phải có ở tầng RTL!"],
        ["Tải tính toán của CPU", "0% tải CPU trong suốt quá trình nhận/truyền chuỗi bit", "CPU bị khóa cứng (blocking) nếu bit-bang mềm", "RTL giải phóng 100% tài nguyên CPU!"],
        ["Tính linh hoạt nâng cấp", "Cần tổng hợp và nạp lại bitstream/đúc lại chip", "Chỉ cần biên dịch lại file C nạp vào Flash", "Firmware C thay đổi nghiệp vụ cực nhanh!"]
    ]
    for r_idx, row_data in enumerate(comp_rows):
        for c_idx, val in enumerate(row_data):
            t_comp.cell(r_idx + 1, c_idx).paragraphs[0].text = val
            
    style_table(t_comp, [Inches(1.2), Inches(1.8), Inches(1.8), Inches(1.47)], 
                [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT])
    add_caption("Bảng 3.1: So sánh đặc tính thiết kế khối UART trên phần cứng RTL và xử lý bằng Firmware C")

    add_h2("3.4. Sơ đồ khối kiến trúc vi mạch UART RTL (5 tầng chức năng)")
    add_p("Khối vi mạch **uart_mmio.v** được tổ chức thành 5 tầng mạch logic chuyên biệt:")
    add_bullet("1. Tầng Tạo Tốc Độ Baud (Baud Rate Prescaler): ", "Thanh ghi chia tần 32-bit nạp giá trị DIV = 5208 (9600 baud @ 50MHz) hoặc 16 (trong mô phỏng).")
    add_bullet("2. Tầng Thu Nối Tiếp (UART Receiver): ", "Bộ lọc đồng bộ 2 tầng D-FF khử hiện tượng bất định (Metastability), mạch phát hiện Start bit và bộ lấy mẫu trung tâm bit dữ liệu.")
    add_bullet("3. Tầng Hàng Đợi Đệm (Synchronous FIFO 32 Byte): ", "Hàng đợi đệm tròn Circular Buffer với 2 con trỏ đọc/ghi và các cờ trạng thái `empty`, `full`.")
    add_bullet("4. Tầng Phát Nối Tiếp (UART Transmitter): ", "Máy trạng thái FSM phát khung truyền chuẩn 8-N-1 (Start bit 0, 8 bit dữ liệu LSB-first, Stop bit 1).")
    add_bullet("5. Tầng Giao Tiếp Bus MMIO (Bus Interface): ", "Giải mã offset `0x00` (Divider) và `0x04` (Data), trả về cờ `ready` sau đúng 1 chu kỳ xung nhịp.")

    if os.path.exists(img_uart_bw):
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.paragraphs[-1].add_run().add_picture(img_uart_bw, width=Inches(6.0))
        add_caption("Hình 3.7: Sơ đồ khối 5 tầng kiến trúc vi mạch UART RTL (uart_mmio.v)")

    add_h2("3.5. Chi tiết 6 biến địa chỉ phần cứng cốt lõi trong Firmware C")
    add_p("Tầng Firmware C tương tác với toàn bộ vi mạch phần cứng thông qua 6 biến địa chỉ MMIO và con trỏ bộ nhớ cốt lõi:")

    add_bullet("1. REG_RFID_UART_DAT & DIV (0x1000_0004 & 0x1000_0000): ", "Ánh xạ trực tiếp vào hàng đợi FIFO của cổng UART nối với đầu đọc RDM6300. Khi đọc địa chỉ `0x1000_0004`, nếu FIFO rỗng trả về `0xFFFFFFFF`, nếu có byte hợp lệ trả về byte dữ liệu [7:0] và tự động giảm con trỏ FIFO.")
    add_bullet("2. REG_PC_UART_DAT & DIV (0x3000_0004 & 0x3000_0000): ", "Giao tiếp với cổng nối tiếp Host PC. Dùng để xuất chuỗi chào mừng, menu CLI 10 chức năng và nhận các ký tự điều khiển quản trị từ máy tính.")
    add_bullet("3. REG_GPIO_LEDS (0x4000_0000): ", "Điều khiển các chân đầu ra: Bit [0] = LED Hoạt động (D1), Bit [1] = LED Thành công/Mở cửa (D2), Bit [2] = LED Từ chối (D3), Bit [3] = LED Ghi Flash (D4), Bit [4] = Tín hiệu kích hoạt Relay mở chốt cửa điện từ.")
    add_bullet("4. USER_FLASH_ADDR (0x0030_0000 - Sector 48): ", "Địa chỉ cơ sở vùng nhớ lưu trữ cơ sở dữ liệu thẻ hợp lệ (Whitelist). Lưu trữ 256 thẻ theo cấu trúc bản ghi 16 byte (UID High, UID Low, Slot ID, Magic Key).")
    add_bullet("5. LOG_FLASH_ADDR (0x0031_0000 - Sector 49): ", "Địa chỉ cơ sở vùng nhớ lưu trữ nhật ký quẹt thẻ (Access Logs). Dành riêng 8KB lưu tuần tự 512 sự kiện quẹt thẻ mới nhất phục vụ kiểm toán.")
    add_bullet("6. 0x0200_0000 & flashio_worker (In-SRAM Execution): ", "Giải quyết triệt để vấn đề xung đột bus khi CPU vừa kéo lệnh từ Flash XIP vừa ghi Flash. Toàn bộ đoạn mã máy phát lệnh bit-bang SPI được sao chép vào 1KB SRAM nội và thực thi tại đó, giúp hệ thống không bao giờ bị treo (Zero-Stall).")

    # =============================================================
    # PHẦN 4: HỆ THỐNG TESTBENCH & KIỂM THỬ MÔ PHỎNG
    # =============================================================
    add_h1("Phần 4: Hệ Thống Testbench & Kiểm Thử Mô Phỏng")
    
    add_h2("4.1. Testbench 1: Kiểm thử RTL thuần cho UART MMIO & FIFO (tb_uart_rtl.v)")
    add_p("Testbench `tb_uart_rtl.v` kiểm thử độc lập toàn bộ các module phần cứng `uart_mmio.v`, `sync_fifo.v` và `simpleuart.v` mà không cần lõi CPU PicoRV32. Hệ thống vượt qua 100% cả 5 kịch bản kiểm thử sau 15,275 ns:")
    add_bullet("Kịch bản 1: ", "Kiểm tra thanh ghi Prescaler tại offset 0x00 nạp đúng giá trị mặc định TEST_DIV = 16 -> PASS.")
    add_bullet("Kịch bản 2: ", "Ghi giá trị chia tần mới và đọc lại qua bus MMIO, xác nhận mạch thanh ghi hoạt động chuẩn xác -> PASS.")
    add_bullet("Kịch bản 3: ", "Ghi ký tự 0x4B ('K' / 75) vào wdata, kiểm tra dạng sóng nối tiếp tx_o đúng chuẩn 8-N-1 -> PASS.")
    add_bullet("Kịch bản 4: ", "Bơm chuỗi bit vào rx_i, cờ rx_activity_o tích cực, dữ liệu nạp sạch vào FIFO và đọc ra read_val = 75 -> PASS.")
    add_bullet("Kịch bản 5: ", "Bắn chuỗi 16 byte liên tiếp kiểm tra cơ chế chống tràn của hàng đợi FIFO, đọc cạn trả về 0xFFFFFFFF -> PASS.")

    if os.path.exists(img_tb_uart_rtl):
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.paragraphs[-1].add_run().add_picture(img_tb_uart_rtl, width=Inches(6.0))
        add_caption("Hình 4.1: Dạng sóng mô phỏng Vivado XSim cho Testbench UART RTL (15.275 µs - 100% PASS)")

    add_h2("4.2. Testbench 2: Kiểm thử tích hợp toàn diện Top SoC Boot Flash & Ping (tb_uart_ping.v)")
    add_p("Testbench `tb_uart_ping.v` kiểm thử tích hợp toàn diện Top SoC hoàn chỉnh gồm CPU PicoRV32, bộ điều khiển SPI Flash spimemio, 1KB SRAM, Interconnect và 2 khối UART.")
    
    add_p("Đoạn mã Verilog Testbench cốt lõi:")
    ping_code = [
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
        "end"
    ]
    add_console_block(ping_code)

    add_p("Log thực thi thực tế trên Vivado Simulator (XSim):")
    ping_log = [
        "Vivado Simulator v2025.1 - xsim tb_uart_ping",
        "Time resolution is 1 ps",
        "[FLASH MODEL] Loaded 2048 words (8192 bytes) from firmware.hex",
        "================================================================",
        "  STARTING TESTBENCH: tb_uart_ping (Full SoC RISC-V Verification)",
        "================================================================",
        "[TB] System Reset released. PicoRV32 booting from SPI Flash at 0x250000...",
        "[UART TX] ================================================",
        "[UART TX]   RDM6300 PICORV32 SOC ACCESS CONTROLLER READY  ",
        "[UART TX] ================================================",
        "[TB] Boot banner detected! Sending 'P' (Ping) command from PC Host...",
        "[HOST -> SOC] Sent Byte: 'P' (0x50), '\\n' (0x0A)",
        "[UART TX] PONG: PicoRV32 Active",
        "================================================================",
        "  [SUCCESS] PING-PONG TEST PASSED! PicoRV32 responded with PONG.",
        "  cpu_trap = 0 (CPU healthy and executing normally)",
        "================================================================"
    ]
    add_console_block(ping_log)
    add_caption("Hình 4.2: Log thực thi mô phỏng Vivado XSim cho Testbench Top SoC (2,086.555 µs - 100% PASS)")

    # =============================================================
    # PHẦN 5: DEMO THỰC NGHIỆM TRÊN BO MẠCH FPGA BASYS 3
    # =============================================================
    add_h1("Phần 5: Demo Thực Nghiệm Trên Bo Mạch FPGA Basys 3")
    
    add_h2("5.1. Thiết lập mạch phần cứng thực tế (Nguồn ngoài 5V MB102 & Trở đệm 1kΩ)")
    add_p("Hệ thống thực nghiệm trên phần cứng thật bao gồm bo mạch FPGA Basys 3, đầu đọc RFID RDM6300, module nguồn MB102, điện trở đệm 1kΩ và máy tính PC:")
    
    if os.path.exists(img_device):
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.paragraphs[-1].add_run().add_picture(img_device, width=Inches(5.5))
        add_caption("Hình 5.1: Hệ thống thực nghiệm hoàn chỉnh trên bo mạch FPGA Basys 3 và đầu đọc RFID RDM6300")

    add_p("2 giải pháp kỹ thuật cốt tử trong thiết kế phần cứng:")
    add_bullet("1. Mạch nguồn MB102 cấp riêng 5V DC cho RDM6300: ", "Cổng PMOD Basys 3 chỉ cung cấp điện áp 3.3V, không đủ để module RDM6300 phát xung kích hoạt cuộn cảm 125 kHz. Module nguồn MB102 cấp nguồn 5V ổn định với mass GND chung.")
    add_bullet("2. Điện trở đệm 1kΩ bảo vệ chân FPGA: ", "Mắc nối tiếp giữa chân TX (mức logic 5V) của RDM6300 và chân JA1 (chịu tối đa 3.3V) của FPGA Artix-7, hạn dòng bảo vệ an toàn tuyệt đối cho các diode kẹp nội bộ của FPGA.")

    add_h2("5.2. Giao diện quản trị Host Console CLI 10 chức năng & Kịch bản quẹt thẻ thực tế")
    add_p("Hệ thống cung cấp giao diện dòng lệnh CLI 10 chức năng chuyên nghiệp qua cổng UART (115200 baud):")
    
    cli_menu = [
        "================== ACCESS CONTROLLER CLI ==================",
        " [1] Show Whitelist          [6] Ping Controller (Health)",
        " [2] Add Master / Admin Tag  [7] Clear Whitelist Sector",
        " [3] Add User Tag            [8] Read Access Event Logs",
        " [4] Delete Specific Tag     [9] Clear Event Logs Sector",
        " [5] System Status (Flash/IO)[0] Run Automated Self-Test",
        "==========================================================="
    ]
    add_console_block(cli_menu)
    add_caption("Hình 5.2: Menu dòng lệnh quản trị Host Console CLI 10 chức năng")

    add_p("Kết quả thực nghiệm 4 kịch bản quẹt thẻ thực tế:")
    add_bullet("Kịch bản 1 (Quẹt thẻ hợp lệ): ", "Khi quẹt thẻ đã lưu trong Whitelist, còi Buzzer kêu 1 tiếng bíp ngắn, LED xanh D2 sáng, Relay mở chốt cửa trong 3 giây và tự động ghi sự kiện SUCC vào Sector 49.")
    add_bullet("Kịch bản 2 (Quẹt thẻ lạ): ", "Khi quẹt thẻ chưa đăng ký, còi Buzzer kêu 3 tiếng bíp cảnh báo, LED đỏ D3 sáng và ghi sự kiện FAIL vào Sector 49.")
    add_bullet("Kịch bản 3 (Thêm thẻ mới qua CLI): ", "Quản trị viên gửi lệnh số [3] và UID thẻ, CPU nạp routine flashio_worker vào SRAM ghi trực tiếp vào Flash Sector 48.")
    add_bullet("Kịch bản 4 (Xuất nhật ký Access Log): ", "Gửi lệnh số [8], CPU xuất toàn bộ danh sách 512 sự kiện quẹt thẻ gần nhất lên máy tính phục vụ kiểm toán an ninh.")

    # =============================================================
    # PHẦN 6: THIẾT KẾ VẬT LÝ ASIC & KÝ DUYỆT SIGN-OFF
    # =============================================================
    add_h1("Phần 6: Thiết Kế Vật Lý ASIC & Ký Duyệt Sign-off")
    
    add_h2("6.1. Quy trình thiết kế vật lý RTL-to-GDSII trên OpenLane 2 (SkyWater 130nm)")
    add_p("Toàn bộ vi mạch SoC được thực thi thiết kế vật lý từ mã Verilog RTL sang bản vẽ mặt nạ GDSII hoàn chỉnh trên OpenLane 2 (PDK SkyWater 130nm - thư viện sky130_fd_sc_hd):")
    add_bullet("1. Tổng hợp logic (Synthesis - Yosys & ABC): ", "Chuyển đổi Verilog RTL thành sơ đồ cổng logic chuẩn (Gate-Level Netlist) gồm 10,779 D-FF và 23,442 cell logic tổ hợp.")
    add_bullet("2. Hoạch định mặt bằng & Lưới nguồn (Floorplan & PDN): ", "Kích thước Die: 1362.08 x 1372.80 µm (1.87 mm²), kích thước Core: 1351.02 x 1349.12 µm (1.82 mm²), mật độ tế bào Core Utilization = 52.84%. Lưới nguồn met4/met5 bảo đảm sụt áp nguồn cực nhỏ (IR Drop tối đa chỉ 1.39 mV tại điện áp 1.80V).")
    add_bullet("3. Xếp đặt tế bào chuẩn (Placement - OpenROAD): ", "Bố trí 164,478 cell các loại (bao gồm cell logic, tap cell, diode bảo vệ và fill cell) tối ưu hóa độ trễ đường truyền.")
    add_bullet("4. Tổng hợp cây xung nhịp (Clock Tree Synthesis - TritonCTS): ", "Chèn 1,666 clock buffers và 898 clock inverters, cân bằng độ trễ xung nhịp mạng clock 50 MHz, Skew cực nhỏ, bảo đảm không vi phạm Hold time.")
    add_bullet("5. Định tuyến chi tiết (Global & Detailed Routing - FastRoute & TritonRoute): ", "Định tuyến 60,225 nets và 575,767 vias với tổng chiều dài dây dẫn 3.215 mét trên 5 lớp kim loại (met1 - met5), không nghẽn DRC.")

    add_h2("6.2. Bản vẽ Layout OpenROAD, chỉ số PPA và báo cáo ký duyệt Sign-off toàn diện")
    if os.path.exists(img_openroad):
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.paragraphs[-1].add_run().add_picture(img_openroad, width=Inches(5.5))
        add_caption("Hình 6.1: Bản vẽ Layout vi mạch SoC PicoRV32 hoàn chỉnh trên OpenROAD (SkyWater 130nm)")

    if os.path.exists(img_signoff):
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.paragraphs[-1].add_run().add_picture(img_signoff, width=Inches(5.5))
        add_caption("Hình 6.2: Báo cáo ký duyệt Sign-off 3 chỉ số then chốt (Antenna, LVS, DRC)")

    # Bảng PPA và Sign-off chi tiết đầy đủ
    t_ppa = doc.add_table(rows=12, cols=3)
    ppa_headers = ["Chỉ Số Thiết Kế Vật Lý (PPA & Physical Metrics)", "Giá Trị Trích Xuất Thực Tế (OpenLane Runs)", "Tiêu Chuẩn Đánh Giá / Ký Duyệt"]
    for i, h in enumerate(ppa_headers):
        t_ppa.cell(0, i).paragraphs[0].text = h
        
    ppa_rows = [
        ["Tiến trình công nghệ (Process Node)", "SkyWater 130nm (sky130_fd_sc_hd)", "Thư viện High Density Standard Cells"],
        ["Điện áp hoạt động định mức (Nominal Voltage)", "1.80 V (VDD / VPWR)", "Điện áp chuẩn lõi số tiến trình Sky130"],
        ["Kích thước khuôn & Diện tích Die (Die Area)", "1362.08 x 1372.80 µm | 1.87 mm² (1,869,850 µm²)", "Chuẩn đóng gói khung chân đế QFN / QFP"],
        ["Kích thước lõi & Diện tích Core (Core Area)", "1351.02 x 1349.12 µm | 1.82 mm² (1,822,690 µm²)", "Mật độ sử dụng lõi Core Utilization = 52.84%"],
        ["Tổng số lượng tế bào chuẩn (Standard Cells)", "164,478 cells (10,779 D-FF + 23,442 Comb + 77,243 Diode)", "Bao gồm 24,247 timing buffer + 2,564 CTS buffer/inv"],
        ["Tổng chiều dài dây dẫn & Vias (Interconnect)", "3,215,448 µm (3.215 m) | 60,225 Nets | 575,767 Vias", "Định tuyến trên 5 lớp kim loại (met1 - met5)"],
        ["Tổng công suất tiêu thụ (Total Power @ 50MHz)", "76.02 mW (Internal: 41.12 mW, Switching: 34.90 mW)", "Dòng rò tĩnh cực nhỏ (Static Leakage: 1.18 µW)"],
        ["Độ sụt áp nguồn tối đa (Worst IR Drop)", "1.39 mV (0.00139 V, sụt áp < 0.08% VDD)", "Mạng PDN met4/met5 an toàn tuyệt đối (Avg: 0.085 mV)"],
        ["Tần số xung nhịp & Định thời (STA Timing)", "50.0 MHz (Tclk = 20.0 ns) | WNS = 0.00 ns", "MET TIMING trên toàn bộ 9 góc đo công nghệ (9 corners)!"],
        ["Ký duyệt hiệu ứng Ăng-ten (Antenna Sign-off)", "0 vi phạm (Zero Violations) | 77,243 Diode bảo vệ", "100% pin/net vượt qua kiểm tra Magic Antenna"],
        ["Ký duyệt LVS & DRC Sign-off (Tape-out Ready)", "0 lỗi LVS (Netgen 100% Match) | 0 lỗi DRC (Magic/KLayout)", "Đạt chuẩn xuất xưởng chế tạo vi mạch (Tape-out Ready)!"]
    ]
    for r_idx, row_data in enumerate(ppa_rows):
        for c_idx, val in enumerate(row_data):
            t_ppa.cell(r_idx + 1, c_idx).paragraphs[0].text = val
            
    style_table(t_ppa, [Inches(2.5), Inches(2.3), Inches(1.47)], 
                [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT])
    add_caption("Bảng 6.1: Bảng tổng hợp các chỉ số PPA và báo cáo ký duyệt Sign-off vi mạch ASIC")

    add_h2("6.3. Phân tích định thời tĩnh STA & Báo cáo Multi-Corner Timing (summary.rpt & clock.rpt)")
    add_p("Phân tích định thời tĩnh (Static Timing Analysis - STA) sau giai đoạn bố trí và định tuyến (Post-PNR) được thực hiện trên toàn bộ 9 góc đo công nghệ (Multi-Corner Analysis):")

    # Bảng STA Timing từ summary.rpt
    t_sta = doc.add_table(rows=6, cols=5)
    sta_headers = ["Góc Đo Công Nghệ (Corner)", "Setup Slack (Worst / Reg)", "Hold Slack (Worst / Reg)", "Số Lỗi (Vio / TNS)", "Đánh Giá Định Thời"]
    for i, h in enumerate(sta_headers):
        t_sta.cell(0, i).paragraphs[0].text = h
        
    sta_rows = [
        ["nom_tt_025C_1v80 (Typical)", "+4.4194 ns (+6.5934 ns)", "+0.5418 ns (+0.5418 ns)", "0 Vio (TNS = 0.00)", "MET TIMING (Đạt chuẩn 50.0 MHz)"],
        ["nom_ff_n40C_1v95 (Fast-Fast)", "+5.5199 ns (+7.7276 ns)", "+0.1680 ns (+0.1680 ns)", "0 Vio (TNS = 0.00)", "MET TIMING (Biên độ Setup cực lớn)"],
        ["min_tt_025C_1v80 (Min Typical)", "+4.5720 ns (+6.6560 ns)", "+0.6874 ns (+0.6874 ns)", "0 Vio (TNS = 0.00)", "MET TIMING (Hold Margin tối ưu)"],
        ["min_ff_n40C_1v95 (Min Fast)", "+5.6454 ns (+7.7576 ns)", "+0.2879 ns (+0.2879 ns)", "0 Vio (TNS = 0.00)", "MET TIMING (Hoạt động ổn định)"],
        ["max_tt_025C_1v80 (Max Typical)", "+4.2744 ns (+6.5546 ns)", "+0.3169 ns (+0.3169 ns)", "0 Vio (TNS = 0.00)", "MET TIMING (Dư địa 4.27 ns)"]
    ]
    for r_idx, row_data in enumerate(sta_rows):
        for c_idx, val in enumerate(row_data):
            t_sta.cell(r_idx + 1, c_idx).paragraphs[0].text = val
            
    style_table(t_sta, [Inches(2.0), Inches(1.5), Inches(1.5), Inches(1.1), Inches(1.67)], 
                [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT])
    add_caption("Bảng 6.2: Bảng phân tích định thời đa góc đo (Multi-Corner STA) trích xuất từ 55-openroad-stapostpnr/summary.rpt")

    add_p("Các điểm nhấn kỹ thuật quan trọng trong báo cáo định thời:")
    add_bullet("1. Tần số hoạt động cực đại (clock.rpt): ", "Với chu kỳ tối thiểu Tmin = 10.77 ns, tần số cực đại đạt được là Fmax = 92.81 MHz, vượt trội 85.6% so với tần số thiết kế mục tiêu 50.0 MHz.")
    add_bullet("2. Triệt tiêu hoàn toàn lỗi Hold Time: ", "Luồng OpenLane đã tự động chèn 21,947 Hold Buffers (dlygate4sd3) để cân bằng thời gian truyền giữa các tầng thanh ghi, bảo đảm Hold Slack dương trên toàn bộ các corner.")
    add_bullet("3. Đường truyền tới hạn (Critical Path): ", "Đường truyền từ FF _52233_ tới cổng xuất flash_io2_do có thời gian đến Data Arrival Time là 13.33 ns, nhỏ hơn nhiều so với Data Required Time 17.75 ns (Slack dương +4.42 ns).")

    # =============================================================
    # KẾT LUẬN & HƯỚNG PHÁT TRIỂN
    # =============================================================
    add_h1("Kết Luận & Hướng Phát Triển Đồ Án")
    
    add_h2("Các kết quả nổi bật đã đạt được")
    add_p("Đồ án đã hoàn thành xuất sắc và trọn vẹn toàn bộ các mục tiêu nghiên cứu đề ra:")
    add_bullet("1. Tự chủ thiết kế kiến trúc SoC: ", "Thiết kế hoàn chỉnh vi mạch SoC tích hợp nhân RISC-V PicoRV32, khối liên kết bus trung tâm soc_interconnect.v, 1KB Data SRAM, bộ điều khiển SPI Flash spimemio, và ngoại vi UART có đệm phần cứng FIFO 32 byte.")
    add_bullet("2. Tối ưu hóa kiến trúc nhúng: ", "Hiện thực hóa cơ chế thực thi tại chỗ XIP từ SPI Flash kết hợp nạp động routine flashio_worker vào 1KB SRAM để ghi/xóa cơ sở dữ liệu Whitelist và nhật ký Access Log mà không xung đột bus.")
    add_bullet("3. Kiểm chứng thực nghiệm 100%: ", "Xây dựng hệ sinh thái kiểm thử mô phỏng tinh gọn (tb_uart_rtl.v và tb_uart_ping.v), nạp bitstream kiểm thử thành công trên bo mạch FPGA Basys 3 với thẻ RFID thật và đầu đọc RDM6300 thật.")
    add_bullet("4. Đạt chuẩn ký duyệt sản xuất ASIC (Tape-out Ready): ", "Thực thi thành công luồng thiết kế vật lý OpenLane 2 trên tiến trình SkyWater 130nm, đạt 0 vi phạm Antenna, 0 lỗi LVS, 0 lỗi DRC, MET TIMING ở tần số 50 MHz trên cả 9 góc đo và sụt áp IR drop an toàn.")

    add_h2("Hướng phát triển tiếp theo")
    add_bullet("1. ", "Đưa thiết kế đi chế tạo thực tế (Tape-out) thông qua chương trình Google / Efabless ChipIgnite.")
    add_bullet("2. ", "Tích hợp thêm module mã hóa phần cứng AES-128 để mã hóa toàn bộ dữ liệu thẻ trên SPI Flash.")
    add_bullet("3. ", "Bổ sung chuẩn thẻ RFID tần số cao 13.56 MHz (Mifare / NFC) để mở rộng ứng dụng trong thanh toán không tiếp xúc.")

    # -------------------------------------------------------------
    # LƯU FILE VÀ COPY (CHỈ 1 BẢN CHÍNH THỨC DUY NHẤT)
    # -------------------------------------------------------------
    out_path = os.path.join(cur_dir, "Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.docx")
    doc.save(out_path)
    print(f"Report generated successfully: {out_path} ({os.path.getsize(out_path)} bytes)")

    doc_out = os.path.join(doc_dir, "Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.docx")
    try:
        shutil.copy2(out_path, doc_out)
        print(f"Copied to document root: {doc_out}")
    except Exception as e:
        print(f"Notice during copy: {e}")

if __name__ == "__main__":
    generate_report()
