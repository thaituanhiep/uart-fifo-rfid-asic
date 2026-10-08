# -*- coding: utf-8 -*-
"""
Script: generate_abstract_docx.py
Tạo tài liệu Tóm Tắt Đồ Án (Executive Abstract & Summary):
- Trả lời trực diện, rõ ràng 2 câu hỏi lớn: "Tôi đã làm gì?" và "Kết quả thế nào?"
- Bám sát chặt chẽ cấu trúc 12 slide báo cáo thực tế
- Tích hợp bảng chỉ số kỹ thuật KPI, bảng số liệu PPA, bảng phân tích định thời STA và bảng ánh xạ 12 slide
- Chèn các hình ảnh minh chứng thực tế: Sơ đồ khối SoC, dạng sóng testbench, bo mạch thật FPGA và layout OpenROAD / Sign-off
"""

import os
import shutil
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def create_abstract_docx():
    doc = Document()

    # Thiết lập lề chuẩn trang A4
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)
        section.page_width = Inches(8.27)   # A4 width
        section.page_height = Inches(11.69) # A4 height

        # Header & Footer
        header = section.header
        p_hdr = header.paragraphs[0]
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_hdr = p_hdr.add_run("FPT JETKING — BẢN TÓM TẮT ĐỒ ÁN (EXECUTIVE SUMMARY)")
        r_hdr.font.name = "Times New Roman"
        r_hdr.font.size = Pt(8.5)
        r_hdr.font.italic = True
        r_hdr.font.color.rgb = RGBColor(100, 100, 100)

        footer = section.footer
        p_ftr = footer.paragraphs[0]
        p_ftr.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_ftr = p_ftr.add_run("Đồ án: SoC PicoRV32 RFID RDM6300 & SPI Flash | Học viên: Thái Tuấn Hiệp | GVHD: ThS. Nguyễn Văn Đông")
        r_ftr.font.name = "Times New Roman"
        r_ftr.font.size = Pt(8.5)
        r_ftr.font.color.rgb = RGBColor(100, 100, 100)

    # Bảng màu
    BLACK = RGBColor(0, 0, 0)
    DARK_BLUE = RGBColor(15, 23, 42)
    NAVY = RGBColor(11, 19, 43)
    BLUE_ACCENT = RGBColor(37, 99, 235)
    GREEN = RGBColor(16, 185, 129)
    GRAY = RGBColor(71, 85, 105)

    # Thư mục chứa tài nguyên
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    doc_dir = os.path.dirname(cur_dir) if os.path.basename(cur_dir) == "temp" else cur_dir
    project_root = os.path.dirname(doc_dir)

    img_fig1 = os.path.join(cur_dir, "fig1_block_diagram.png")
    if not os.path.exists(img_fig1):
        img_fig1 = os.path.join(doc_dir, "fig1_block_diagram.png")

    img_tb_rtl = os.path.join(cur_dir, "waveform_tb_uart_rtl.png")
    if not os.path.exists(img_tb_rtl):
        img_tb_rtl = os.path.join(doc_dir, "waveform_tb_uart_rtl.png")

    img_device = os.path.join(project_root, "Device.jpg")
    if not os.path.exists(img_device):
        img_device = os.path.join(cur_dir, "Device.jpg")
    if not os.path.exists(img_device):
        img_device = os.path.join(doc_dir, "Device.jpg")

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

    # Helper format font
    def set_font(run, name="Times New Roman", size=11, bold=False, italic=False, color=BLACK):
        run.font.name = name
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = color

    def set_cell_margins(cell, top=70, bottom=70, left=100, right=100):
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

    def style_table(table, col_widths, alignments, font_size=9.5, header_bg="1E293B", alt_bg="F8FAFC"):
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
                set_cell_margins(cell, top=65, bottom=65, left=90, right=90)

                shading_color = header_bg if is_header else (alt_bg if r_idx % 2 == 1 else "FFFFFF")
                tcPr = cell._tc.get_or_add_tcPr()
                shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{shading_color}"/>')
                tcPr.append(shd)

                border_color = "0F172A" if is_header else "CBD5E1"
                borders = parse_xml(
                    f'<w:tcBorders {nsdecls("w")}>'
                    f'<w:top w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
                    f'<w:bottom w:val="single" w:sz="{"10" if is_header else "4"}" w:space="0" w:color="{border_color}"/>'
                    f'<w:left w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
                    f'<w:right w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
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
                        text_col = RGBColor(255, 255, 255) if is_header else BLACK
                        set_font(run, name=fn, size=font_size, bold=(is_header or bool(run.bold)), color=text_col)

    def add_p(text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=3.0, line_spacing=1.15):
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
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        set_font(r, size=13.0, bold=True, color=DARK_BLUE)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        set_font(r, size=11.5, bold=True, color=BLUE_ACCENT)
        return p

    def add_bullet(bold_prefix="", text=""):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(1.5)
        p.paragraph_format.space_after = Pt(2.0)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r1 = p.add_run(bold_prefix)
            set_font(r1, bold=True, color=BLACK)
        if text:
            r2 = p.add_run(text)
            set_font(r2, color=BLACK)
        return p

    def add_callout(title, bullets, border_hex="2563EB", bg_hex="EFF6FF"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.57)

        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="4" w:space="0" w:color="{border_hex}"/>'
            f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="{border_hex}"/>'
            f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_hex}"/>'
            f'<w:right w:val="single" w:sz="4" w:space="0" w:color="{border_hex}"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_hex}"/>')
        tcPr.append(shd)
        set_cell_margins(cell, top=70, bottom=70, left=120, right=100)

        p0 = cell.paragraphs[0]
        p0.paragraph_format.space_before = Pt(1)
        p0.paragraph_format.space_after = Pt(3)
        r0 = p0.add_run(title)
        set_font(r0, size=11.0, bold=True, color=NAVY)

        for b_lbl, b_val in bullets:
            p = cell.add_paragraph()
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.12
            r1 = p.add_run(f"• {b_lbl} ")
            set_font(r1, size=10.0, bold=True, color=BLACK)
            r2 = p.add_run(b_val)
            set_font(r2, size=9.8, color=BLACK)

        doc.add_paragraph().paragraph_format.space_after = Pt(2)

    def add_caption(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(text)
        set_font(r, size=9.5, italic=True, color=GRAY)
        return p

    def add_hyperlink(paragraph, url, text, font_size=9.5, bold=False, color="2563EB", underline=True):
        part = paragraph.part
        r_id = part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
        hyperlink = parse_xml(
            f'<w:hyperlink {nsdecls("w")} r:id="{r_id}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            f'<w:r>'
            f'<w:rPr>'
            f'<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
            f'<w:sz w:val="{int(font_size * 2)}"/>'
            f'{"<w:b/>" if bold else ""}'
            f'{"<w:u w:val=\"single\"/>" if underline else ""}'
            f'<w:color w:val="{color}"/>'
            f'</w:rPr>'
            f'<w:t>{text}</w:t>'
            f'</w:r>'
            f'</w:hyperlink>'
        )
        paragraph._p.append(hyperlink)

    # =========================================================================
    # PHẦN 1: BÌA TIÊU ĐỀ & METADATA BÁO CÁO
    # =========================================================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_after = Pt(2)
    r_inst = p_inst.add_run("FPT JETKING — CHUYÊN NGÀNH THIẾT KẾ VI MẠCH BÁN DẪN (CHIP DESIGN)")
    set_font(r_inst, size=11, bold=True, color=NAVY)

    p_doc_type = doc.add_paragraph()
    p_doc_type.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_doc_type.paragraph_format.space_after = Pt(6)
    r_doc_type = p_doc_type.add_run("BẢN TÓM TẮT ĐỒ ÁN\n(EXECUTIVE ABSTRACT & SUMMARY)")
    set_font(r_doc_type, size=14, bold=True, color=BLUE_ACCENT)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(8)
    r_title = p_title.add_run("THIẾT KẾ HỆ THỐNG XỬ LÝ DỮ LIỆU CỦA THẺ RA VÀO RFID 125KHZ OFFLINE\nTÍCH HỢP CPU RISC-V PICORV32 & XỬ LÝ NGHIỆP VỤ DỮ LIỆU THẺ BẰNG FIRMWARE C")
    set_font(r_title, size=12.5, bold=True, color=BLACK)

    # Bảng thông tin học viên & GVHD
    tbl_meta = doc.add_table(rows=2, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_w_m = [Inches(3.28), Inches(3.29)]
    align_m = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]

    cell_00 = tbl_meta.cell(0, 0)
    p = cell_00.paragraphs[0]
    p.add_run("Học viên thực hiện: ").bold = True
    p.add_run("Thái Tuấn Hiệp")

    cell_01 = tbl_meta.cell(0, 1)
    p = cell_01.paragraphs[0]
    p.add_run("Giảng viên hướng dẫn: ").bold = True
    p.add_run("ThS. Nguyễn Văn Đông")

    cell_10 = tbl_meta.cell(1, 0)
    p = cell_10.paragraphs[0]
    p.add_run("Học kỳ: ").bold = True
    p.add_run("SEM3 (Khóa Đồ Án Chuyên Sâu)")

    cell_11 = tbl_meta.cell(1, 1)
    p = cell_11.paragraphs[0]
    p.add_run("Thời gian thực hiện: ").bold = True
    p.add_run("Tháng 10 / 2026")

    style_table(tbl_meta, col_w_m, align_m, font_size=9.5, header_bg="F1F5F9", alt_bg="F1F5F9")
    for r in tbl_meta.rows[0].cells:
        for p in r.paragraphs:
            for run in p.runs:
                run.font.color.rgb = BLACK
                if "Học viên" in run.text or "Giảng viên" in run.text:
                    run.font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(1)

    p_git = doc.add_paragraph()
    p_git.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_git.paragraph_format.space_before = Pt(1)
    p_git.paragraph_format.space_after = Pt(4)
    r_git = p_git.add_run("Kho mã nguồn mở (GitHub): ")
    set_font(r_git, size=9.5, bold=True, color=NAVY)
    add_hyperlink(p_git, 
                  "https://github.com/thaituanhiep/uart-fifo-rfid-asic/tree/rfid_flash_firmware_optimize",
                  "https://github.com/thaituanhiep/uart-fifo-rfid-asic/tree/rfid_flash_firmware_optimize",
                  font_size=9.5, color="2563EB", underline=True)

    # =========================================================================
    # BẢNG TỔNG QUAN CHỈ SỐ KỸ THUẬT CỐT LÕI (EXECUTIVE KPI METRICS)
    # =========================================================================
    add_h1("TỔNG QUAN CHỈ SỐ KỸ THUẬT CỐT LÕI (EXECUTIVE SUMMARY)")

    add_p("Bản tóm tắt này cô đọng toàn bộ quá trình nghiên cứu, thiết kế phần cứng, lập trình firmware và kết quả thực nghiệm của đồ án. Nhằm giúp người đọc nắm bắt nhanh chóng và chính xác bản chất công việc cùng các bằng chứng định lượng, tài liệu được phân tách rõ ràng thành hai nội dung trọng tâm: (1) Tôi đã làm gì? và (2) Kết quả đạt được thế nào?")

    tbl_kpi = doc.add_table(rows=7, cols=3)
    kpi_widths = [Inches(1.80), Inches(2.30), Inches(2.47)]
    kpi_aligns = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]

    kpi_data = [
        ("Hạng Mục Kỹ Thuật", "Giải Pháp / Cấu Hình Cốt Lõi", "Kết Quả Đo Đạc Thực Tế"),
        ("Kiến trúc Vi hệ thống SoC", "PicoRV32 RISC-V 32-bit (RV32I), Cầu bus Interconnect 0-delay định tuyến 5 Slaves", "Tích hợp hoàn chỉnh Top-level SoC, 1KB SRAM nội, chạy ổn định cả trên FPGA và ASIC"),
        ("Bộ nhớ Ngoài & Cơ chế XIP", "SPI Flash 4MB (W25Q32), nạp mã thực thi tại chỗ (eXecute-In-Place) qua SPIMEMIO", "Tiết kiệm > 70% diện tích silicon ASIC; Nạp worker vào SRAM ghi/xóa Flash không nghẽn bus"),
        ("Ngoại vi UART RFID & PC", "Thiết kế RTL 5 tầng: CDC 2-FF, Lấy mẫu 16x đa số, Hàng đợi FIFO 32B, MMIO 1 chu kỳ", "Triệt tiêu 100% rớt mã thẻ; Giao tiếp Non-blocking phản hồi trong 20 ns (ở 50MHz)"),
        ("Kiểm thử Mô phỏng Vivado", "Mô phỏng RTL thuần (tb_uart_rtl) & Tích hợp Top SoC Boot Flash (tb_uart_ping)", "100% PASS (10/10 kịch bản); cpu_trap = 0; Bắt trọn vẹn chuỗi PONG trong 2.086 ms"),
        ("Thực nghiệm Bo mạch FPGA", "FPGA Digilent Basys 3 (Artix-7), RDM6300 125kHz, Nguồn MB102 5V, Trở đệm 1kΩ", "Hoạt động chính xác 10/10 chức năng CLI Host Console; Nhận diện thẻ với độ trễ < 10 µs"),
        ("Ký duyệt ASIC Tape-out", "Quy trình OpenLane 2 trên tiến trình SkyWater 130nm (sky130_fd_sc_hd)", "0 Antenna, 0 LVS, 0 DRC violations (100% Tape-out Ready); Fmax = 92.81 MHz (vượt 85.6%)")
    ]

    for r_idx, row_vals in enumerate(kpi_data):
        for c_idx, val in enumerate(row_vals):
            cell = tbl_kpi.cell(r_idx, c_idx)
            cell.text = val

    style_table(tbl_kpi, kpi_widths, kpi_aligns, font_size=9.2, header_bg="1E293B", alt_bg="F8FAFC")
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

    # =========================================================================
    # PHẦN I: TÔI ĐÃ LÀM GÌ? (NỘI DUNG & ĐÓNG GÓP KỸ THUẬT)
    # =========================================================================
    add_h1("PHẦN I: TÔI ĐÃ LÀM GÌ? (NHIỆM VỤ & ĐÓNG GÓP KỸ THUẬT)")

    add_p("Để giải quyết bài toán kiểm soát an ninh ra vào độc lập, bảo mật và chi phí thấp, tôi đã tự chủ thiết kế toàn diện một Vi hệ thống trên chip (System-on-Chip - SoC) từ mức mô tả phần cứng RTL Verilog, kiểm thử mô phỏng, lập trình nhúng Firmware C, thực nghiệm trên bo mạch FPGA Basys 3 và hoàn thiện thiết kế vật lý ASIC đạt chuẩn băng từ xuất xưởng (Tape-out) trên công nghệ SkyWater 130nm. Các phần việc cụ thể bao gồm:")

    add_h2("1. Giải Quyết Bài Toán Cấp Thiết: Hệ Thống Offline & Bộ Nhớ SPI Flash NVM")
    add_bullet("Tính cấp thiết của hệ thống Offline: ", "Khắc phục triệt để độ trễ lớn của mạng Internet/Cloud (vài trăm ms đến vài giây), loại bỏ hoàn toàn rủi ro đứt cáp quang, nghẽn server và triệt tiêu nguy cơ lộ lọt dữ liệu định danh nhân sự ra mạng ngoài. Hệ thống tự đối chiếu thẻ tại chỗ với độ trễ siêu nhỏ (< 10 µs), vận hành độc lập 24/7.")
    add_bullet("Vai trò cốt tử của bộ nhớ SPI Flash NVM: ", "Lưu trữ bất biến 4,096 mã thẻ Whitelist (Sector 48) và 512 bản ghi Access Logs (Sector 49) trên 20 năm mà không cần pin nuôi. Đặc biệt, bằng cách áp dụng cơ chế eXecute-In-Place (XIP), CPU kéo opcode trực tiếp từ Flash ngoài 4MB để thực thi, hệ thống chỉ cần 1KB SRAM nội, giúp cắt giảm hơn 70% diện tích khuôn silicon ASIC và tiết kiệm chi phí.")
    add_bullet("Tối ưu hóa chân pad ASIC: ", "Chuẩn giao tiếp SPI chỉ chiếm dụng 4 chân pad (CS, SCK, MOSI, MISO), cho phép chip ASIC đạt kích thước pad-limited tối ưu (chỉ 31 chân toàn chip), hạ giá thành đóng gói vi mạch.")

    add_h2("2. Thiết Kế Kiến Trúc Vi Hệ Thống SoC PicoRV32 (1 Master - 5 Dedicated Slaves)")
    add_p("Hệ thống SoC được thiết kế theo kiến trúc Master - Multi-Slave với bus nội bộ không có độ trễ (0-delay combinational interconnect), kết nối trực tiếp lõi xử lý RISC-V với 5 khối chức năng ngoại vi độc lập:")
    add_bullet("Master CPU PicoRV32: ", "Lõi CPU kiến trúc RV32I 32-bit mở, cấu hình 32 thanh ghi nguyên bản, tần số xung nhịp danh định 50 MHz.")
    add_bullet("Slave 0 - Khối 1KB SRAM Nội (data_sram.v): ", "Ánh xạ địa chỉ 0x0000_0000 - 0x0000_03FF. Đảm nhiệm lưu trữ ngăn xếp hàm C (Stack Pointer = 0x0000_0400), biến toàn cục (.data, .bss) và chứa hàm nạp worker ghi Flash.")
    add_bullet("Slave 1 - Bộ điều khiển SPI Flash XIP (spimemio.v): ", "Ánh xạ 0x0010_0000 - 0x00FF_FFFF (Không gian XIP đọc mã lệnh) và 0x0200_0000 (Bộ điều khiển SPI bit-bang nạp dữ liệu).")
    add_bullet("Slave 2 - Ngoại vi UART MMIO Đầu đọc RFID (rdm6300_mmio.v): ", "Ánh xạ 0x1000_0000 (Divisor) và 0x1000_0004 (Data FIFO). Tích hợp hàng đợi FIFO 32-byte độc lập.")
    add_bullet("Slave 3 - Ngoại vi UART MMIO Máy tính Host PC (host_uart_mmio.v): ", "Ánh xạ 0x3000_0000 (Divisor) và 0x3000_0004 (Data FIFO). Hỗ trợ song công truyền nhận dữ liệu điều khiển.")
    add_bullet("Slave 4 - Khối GPIO Điều Khiển (soc_gpio_mmio.v): ", "Ánh xạ 0x4000_0000. Điều khiển 16-bit LED trạng thái bo mạch, tín hiệu báo Heartbeat 1Hz, cờ Flash Busy và tín hiệu mở relay chốt cửa.")

    if os.path.exists(img_fig1):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(img_fig1, width=Inches(6.20))
        add_caption("Hình 1: Sơ đồ khối kiến trúc vi hệ thống SoC PicoRV32 (1 Master - 5 Dedicated Slaves)")

    add_h2("3. Tự Chủ Thiết Kế Khối Ngoại Vi Vi Mạch UART RTL 5 Tầng Chuyên Dụng")
    add_p("Để đảm bảo việc thu nhận chuỗi 14 byte ASCII từ đầu đọc RFID RDM6300 không bao giờ bị rớt gói hoặc treo bus CPU, tôi đã thiết kế vi mạch UART phần cứng thuần gồm 5 tầng phân tách chặt chẽ:")
    add_bullet("Tầng 1 (Đồng bộ miền xung CDC 2-FF - sync_2ff.v): ", "Khử hiện tượng metastability vật lý khi tín hiệu bất đồng bộ từ bên ngoài đi vào miền xung nhịp 50 MHz của chip, đảm bảo thời gian trung bình giữa 2 lỗi MTBF > 1000 năm.")
    add_bullet("Tầng 2 & 3 (Bộ chia tần 16x & Máy trạng thái FSM 8-N-1 - simpleuart.v): ", "Thanh ghi Prescaler chia tần 5208 (50 MHz / 9600 bps). Bộ lấy mẫu 16x áp dụng cơ chế bầu đa số tại tick 7, 8, 9 ở giữa chu kỳ bit để triệt tiêu nhiễu xung gai.")
    add_bullet("Tầng 4 (Hàng đợi bộ đệm FIFO 32-byte độc lập - sync_fifo.v): ", "Quản lý con trỏ ghi wr_ptr và đọc rd_ptr độc lập trên mảng SRAM 32x8-bit. Dung lượng 32 byte lớn hơn gấp đôi độ dài 14 byte của một khung thẻ RFID, giúp lưu đệm an toàn toàn bộ mã thẻ ngay cả khi CPU đang bận ghi Flash.")
    add_bullet("Tầng 5 (Giải mã bus MMIO Non-blocking - uart_mmio.v): ", "Giao thức bus Non-blocking trả lời trong đúng 1 chu kỳ clock (20 ns). Khi FIFO rỗng, mạch trả về ngay lập tức giá trị 0xFFFFFFFF, không bao giờ làm treo bus chờ CPU.")

    add_h2("4. Kỹ Thuật Đồng Thiết Kế HW/SW: Chạy Mã Xóa/Ghi Flash Trong SRAM (In-RAM Worker)")
    add_p("Một thách thức kỹ thuật lớn trong kiến trúc SoC XIP là CPU không thể vừa đọc opcode từ SPI Flash vừa phát lệnh ghi/xóa chính con chip Flash đó. Để khắc phục, tôi đã triển khai giải pháp kỹ thuật:")
    add_bullet("Khớp tuyệt đối Linker & RTL Bootstrap: ", "Thiết lập PROGADDR_RESET = 0x0025_0000 trên RTL trùng khớp với điểm vào _start trong start.s và tệp định vị bộ nhớ sections.lds.")
    add_bullet("Cơ chế In-RAM Flash Worker: ", "Viết hàm thực thi `flashio_worker` bằng C, sau đó nạp mã máy của hàm này vào vùng nhớ SRAM 1KB. Khi cần ghi Whitelist hoặc xóa nhật ký, CPU chuyển quyền thực thi tạm thời vào SRAM để phát lệnh SPI bit-bang điều khiển W25Q32. Sau khi Flash hoàn tất ghi, CPU nhảy ngược trở lại Flash XIP tiếp tục chạy bình thường.")

    add_h2("5. Tầng Firmware C Nghiệp Vụ & Giao Diện Quản Trị Host Console CLI 10 Chức Năng")
    add_bullet("Giải mã thẻ RFID EM4100: ", "Phân tích khung 14-byte (1 byte Start 0x02, 10 byte mã thẻ ASCII hex, 2 byte Checksum XOR, 1 byte Stop 0x03) với cơ chế Watchdog 10ms tự phục hồi khi tín hiệu đứt đoạn.")
    add_bullet("Tra cứu danh sách trắng Whitelist: ", "Quản lý 4,096 vị trí thẻ tại Sector 48 (0x030000). Thuật toán so khớp với điểm dừng sớm (Early Termination) đạt độ trễ tìm kiếm cực đại < 10 µs.")
    add_bullet("Phần mềm Host Console CLI trên PC (rdm6300_manager.exe): ", "Cung cấp giao diện dòng lệnh 10 chức năng hoàn chỉnh: Ping phần cứng, thêm/xóa thẻ, quét thẻ ảo (Virtual Scan), xem 512 nhật ký Access Log, sao lưu an toàn trước khi xóa Sector và xuất/nhập danh sách thẻ định dạng CSV.")

    # =========================================================================
    # PHẦN II: KẾT QUẢ ĐẠT ĐƯỢC THẾ NÀO? (MINH CHỨNG & SỐ LIỆU)
    # =========================================================================
    add_h1("PHẦN II: KẾT QUẢ ĐẠT ĐƯỢC THẾ NÀO? (MINH CHỨNG & SỐ LIỆU ĐO ĐẠC)")

    add_p("Mọi thiết kế phần cứng và phần mềm trong đồ án đều được kiểm chứng thực tế và đo đạc định lượng thông qua ba cấp độ nghiêm ngặt: Mô phỏng Testbench Vivado, Thực nghiệm bo mạch FPGA thật và Ký duyệt thiết kế vật lý ASIC OpenLane 2.")

    add_h2("1. Kết Quả Mô Phỏng Testbench Vivado XSIM (100% PASS)")
    add_bullet("Testbench 1 - tb_uart_rtl.v (Kiểm thử RTL UART thuần): ", "Vượt qua 5/5 kịch bản kiểm thử (Default Div, Reconfig Divider, TX Frame, RX FIFO, Multi-byte Burst Overflow). Toàn bộ Assert phần cứng đều thỏa mãn, thời gian mô phỏng 15.275 µs, số lỗi = 0.")
    add_bullet("Testbench 2 - tb_uart_ping.v (Kiểm thử tích hợp toàn diện Top SoC): ", "Vượt qua 5/5 kịch bản hệ thống (Power-on Reset, Boot Flash 8KB hex qua XIP, C Startup Banner, Host Ping-Pong phản hồi chuỗi PONG, CPU Health Zero-Trap `cpu_trap == 0`). Thời gian mô phỏng 2.086 ms, số lỗi = 0.")

    if os.path.exists(img_tb_rtl):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(img_tb_rtl, width=Inches(5.80))
        add_caption("Hình 2: Dạng sóng mô phỏng Vivado XSIM xác nhận hoạt động 100% Pass của khối UART RTL thuần (15.275 µs)")

    add_h2("2. Kết Quả Thực Nghiệm Trên Bo Mạch Phần Cứng FPGA Digilent Basys 3 Thật")
    add_bullet("Phối hợp điện áp & Mạch nguồn an toàn: ", "Sử dụng module nguồn Breadboard MB102 cấp riêng 5V DC cho đầu đọc RFID RDM6300 để cuộn cảm LC phát đủ từ trường 125kHz kích hoạt chip thẻ; Mắc điện trở đệm 1kΩ nối tiếp chân TX của RDM6300 sang chân PMOD JA1 (Pin J1) của FPGA Basys 3 để giới hạn dòng bảo vệ diode kẹp < 2mA, ngăn chặn triệt để nguy cơ quá áp 3.3V của FPGA.")
    add_bullet("Xác nhận hoạt động 10 kịch bản CLI thực tế: ", "Hệ thống nhận diện chính xác thẻ RFID mẫu trong thực tế, mở cửa tức thì, ghi bản ghi sự kiện vào Flash và phản hồi đầy đủ qua phần mềm Host Console trên máy tính với baud rate 9600 bps.")

    if os.path.exists(img_device):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(img_device, width=Inches(4.60))
        add_caption("Hình 3: Thiết lập thực nghiệm phần cứng thực tế giữa FPGA Basys 3, Module nguồn MB102 5V và Đầu đọc RFID RDM6300")

    add_h2("3. Kết Quả Thiết Kế Vật Lý ASIC OpenLane 2 (SkyWater 130nm) & Chỉ Số PPA")
    add_p("Toàn bộ thiết kế SoC đã hoàn thành luồng thiết kế vật lý ASIC backend tự động bằng OpenLane 2 (Docker container) trên thư viện ô chuẩn SkyWater 130nm (sky130_fd_sc_hd). Kết quả trích xuất trực tiếp từ các báo cáo runs:")

    tbl_ppa = doc.add_table(rows=8, cols=3)
    ppa_widths = [Inches(1.85), Inches(2.35), Inches(2.37)]
    ppa_aligns = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]

    ppa_data = [
        ("Chỉ Số Vật Lý (PPA Metrics)", "Giá Trị Trích Xuất (OpenLane Runs)", "Đánh Giá & Tiêu Chuẩn Kỹ Thuật"),
        ("Tiến trình & Thư viện ô chuẩn", "SkyWater 130nm (sky130_fd_sc_hd) | VDD = 1.80V", "Thư viện High Density, độ cao tiêu chuẩn, VDD danh định 1.8V"),
        ("Kích thước & Diện tích khuôn (Die)", "Die: 1.87 mm² (1362.08 x 1372.80 µm) | Core: 1.82 mm²", "Mật độ sử dụng lõi Core Density = 52.84%, chuẩn khung chân đế QFN/QFP"),
        ("Tổng số lượng linh kiện (Cells)", "Tổng: 164,478 cells (10,779 D-FF, 23,442 Comb, 77,243 Diode)", "24,247 timing buffers + 2,564 CTS clock buffers/inverters"),
        ("Mạng định tuyến dây nối (Routing)", "60,225 Nets | 575,767 Vias | Chiều dài dây: 3.215 mét", "Định tuyến thành công trên 5 lớp kim loại (met1 - met5), 0 short"),
        ("Tổng công suất tiêu thụ (Power)", "76.02 mW (Internal: 41.12 mW, Switching: 34.90 mW)", "Dòng rò tĩnh siêu thấp (Static Leakage = 1.18 µW ~ 0% tổng công suất)"),
        ("Độ sụt áp nguồn (IR Drop)", "Worst IR Drop: 1.39 mV (0.00139 V, sụt áp < 0.08% VDD)", "Lưới nguồn PDN kim loại dày met4/met5 an toàn tuyệt đối"),
        ("Ký duyệt xuất xưởng (Sign-off)", "0 Antenna Violations | 0 LVS Errors | 0 DRC Errors", "ĐẠT 100% TIÊU CHUẨN XUẤT XƯỞNG BĂNG TỪ (TAPE-OUT READY)")
    ]

    for r_idx, row_vals in enumerate(ppa_data):
        for c_idx, val in enumerate(row_vals):
            cell = tbl_ppa.cell(r_idx, c_idx)
            cell.text = val

    style_table(tbl_ppa, ppa_widths, ppa_aligns, font_size=9.2, header_bg="1E293B", alt_bg="F8FAFC")
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

    add_h2("4. Kết Quả Phân Tích Định Thời Tĩnh STA Multi-Corner (summary.rpt & clock.rpt)")
    add_p("Báo cáo phân tích định thời tĩnh sau bước định tuyến chi tiết (55-openroad-stapostpnr/summary.rpt) xác nhận hệ thống đạt hội tụ định thời hoàn hảo (Timing Closed) trên toàn bộ 9 góc công nghệ (Process Corners):")

    tbl_sta = doc.add_table(rows=6, cols=5)
    sta_widths = [Inches(1.80), Inches(1.20), Inches(1.20), Inches(1.00), Inches(1.37)]
    sta_aligns = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]

    sta_data = [
        ("Góc Công Nghệ (Corner)", "Setup Slack (Worst)", "Hold Slack (Worst)", "Vi Phạm (Vio)", "Đánh Giá STA"),
        ("nom_tt_025C_1v80 (Typical)", "+4.4194 ns", "+0.5418 ns", "0 Vio (TNS = 0.00)", "MET TIMING (Đạt chuẩn 50.0 MHz)"),
        ("nom_ff_n40C_1v95 (Fast-Fast)", "+5.5199 ns", "+0.1680 ns", "0 Vio (TNS = 0.00)", "MET TIMING (Biên độ Setup lớn)"),
        ("min_tt_025C_1v80 (Min Typical)", "+4.5720 ns", "+0.6874 ns", "0 Vio (TNS = 0.00)", "MET TIMING (Hold Margin tối ưu)"),
        ("min_ff_n40C_1v95 (Min Fast)", "+5.6454 ns", "+0.2879 ns", "0 Vio (TNS = 0.00)", "MET TIMING (Vận hành ổn định)"),
        ("max_tt_025C_1v80 (Max Typical)", "+4.2744 ns", "+0.3169 ns", "0 Vio (TNS = 0.00)", "MET TIMING (Dư địa 4.27 ns)")
    ]

    for r_idx, row_vals in enumerate(sta_data):
        for c_idx, val in enumerate(row_vals):
            cell = tbl_sta.cell(r_idx, c_idx)
            cell.text = val

    style_table(tbl_sta, sta_widths, sta_aligns, font_size=9.0, header_bg="2563EB", alt_bg="F1F5F9")
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

    add_callout(
        "KẾT LUẬN ĐẶC TÍNH XUNG NHỊP VÀ TỐI ƯU HÓA ĐỊNH THỜI (TIMING CLOSURE):",
        [
            ("Tần số cực đại khả thi (Fmax):", "92.81 MHz (Chu kỳ xung nhịp tối thiểu Tmin = 10.77 ns, vượt 85.6% mục tiêu 50 MHz)."),
            ("Triệt tiêu 100% lỗi Hold Time:", "Công cụ chèn 21,947 Hold Buffers (dlygate4sd3), đảm bảo không còn bất kỳ vi phạm Hold nào trên toàn chip."),
            ("Cây xung nhịp TritonCTS:", "2,564 đệm xung nhịp, độ trễ phân tán 2.35 - 3.72 ns, độ lệch pha Skew = 1.36 ns, kiểm soát tốt sườn xung."),
            ("Ký duyệt xuất xưởng hoàn tất:", "Đạt đồng thời 0 Antenna, 0 LVS và 0 DRC violations. Vi mạch sẵn sàng gửi xưởng chế tạo.")
        ],
        border_hex="10B981", bg_hex="F0FDF4"
    )

    if os.path.exists(img_openroad) and os.path.exists(img_signoff):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(img_signoff, width=Inches(6.00))
        add_caption("Hình 4: Minh chứng ký duyệt Sign-off 100% Pass (0 Antenna, 0 LVS, 0 DRC) trên công cụ OpenLane 2")

    # =========================================================================
    # PHẦN III: BẢNG ÁNH XẠ 12 SLIDE BÁO CÁO
    # =========================================================================
    add_h1("PHẦN III: BẢNG ĐỐI CHIẾU NHANH THEO 14 SLIDE BÁO CÁO")

    add_p("Nhằm hỗ trợ theo dõi xuyên suốt quá trình thuyết trình, bảng dưới đây tóm tắt trục nội dung và kết quả chính của từng slide trong bộ slide 14 trang:")

    tbl_slides = doc.add_table(rows=15, cols=3)
    sl_widths = [Inches(0.95), Inches(2.60), Inches(3.02)]
    sl_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]

    slides_map = [
        ("Slide", "Tiêu Đề Trọng Tâm", "Nội Dung & Minh Chứng Kỹ Thuật Đạt Được"),
        ("Slide 1", "Bìa Báo Cáo Đồ Án", "Thông tin tác giả, đồ án SoC PicoRV32 RFID RDM6300 & SPI Flash, hệ sinh thái EDA."),
        ("Slide 2", "Phần 1: Giới Thiệu Dự Án", "3 luận điểm cốt lõi: Tính cấp thiết Offline, vai trò Flash NVM và tự chủ ASIC."),
        ("Slide 3", "Phần 3: Sơ Đồ Khối SoC", "Sơ đồ kiến trúc vi hệ thống SoC PicoRV32 (1 Master - 5 Slaves, 4MB Flash, 1KB SRAM, 32 FIFO)."),
        ("Slide 4", "Phần 1: Tổng Quan Sản Phẩm", "4 trụ cột: RTL chạy firmware C & mở rộng; Firmware C trên chip; FPGA Basys 3; OpenLane ASIC."),
        ("Slide 5", "Phần 3: Bảng Memory Map", "Bảng tra cứu MMIO 0x1000/0x3000/0x4000, Flash Sector 48/49, SRAM 0x0200_0000 trong C/RTL."),
        ("Slide 6", "Phần 5: Demo Host Console CLI", "Giao diện Host CLI 10 chức năng: Ping, thêm/xóa thẻ, quét ảo, 512 Logs, đồng bộ CSV."),
        ("Slide 7", "Phần 3: Kiến Trúc UART RTL", "Bản vẽ 5 tầng UART RTL: CDC 2-FF, 16x Sampler, FIFO 32B, MMIO Non-blocking."),
        ("Slide 8", "Phần 4: Testbench 1 (tb_uart_rtl)", "Dạng sóng mô phỏng Vivado 15.275 µs xác nhận 100% Pass 5 kịch bản phần cứng thuần."),
        ("Slide 9", "Phần 4: Testbench 2 (tb_uart_ping)", "Kiểm thử tích hợp Boot Flash XIP & Ping; CPU healthy, cpu_trap == 0 suốt 2.086 ms."),
        ("Slide 10", "Phần 5: Demo FPGA Thiết Lập", "Sơ đồ kết nối phần cứng Basys 3: Nguồn 5V MB102 riêng cho RDM6300, trở đệm bảo vệ 1kΩ."),
        ("Slide 11", "Phần 6: ASIC Sign-off & Config", "Bằng chứng 0 Antenna, 0 LVS, 0 DRC violations, bản vẽ OpenROAD và cấu hình config.json."),
        ("Slide 12", "Phần 6: Bảng PPA Metrics", "Bảng tổng hợp diện tích Die 1.87 mm², 164K cells, công suất 76 mW, IR Drop 1.39 mV."),
        ("Slide 13", "Phần 6: Phân Tích Định Thời STA", "Bảng Multi-Corner Timing từ summary.rpt; Fmax = 92.81 MHz (vượt 85.6%), 21.9K hold buffers."),
        ("Slide 14", "Tổng Kết Đồ Án & Lời Cảm Ơn", "4 thành tựu nổi bật của đồ án, link GitHub repository và lời cảm ơn trân trọng.")
    ]

    for r_idx, row_vals in enumerate(slides_map):
        for c_idx, val in enumerate(row_vals):
            cell = tbl_slides.cell(r_idx, c_idx)
            cell.text = val

    style_table(tbl_slides, sl_widths, sl_aligns, font_size=8.8, header_bg="1E293B", alt_bg="F8FAFC")
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

    # =========================================================================
    # PHẦN IV: TỔNG KẾT & KẾT LUẬN CỦA ĐỒ ÁN
    # =========================================================================
    add_h1("PHẦN IV: TỔNG KẾT & ĐÓNG GÓP NỔI BẬT CỦA ĐỒ ÁN")

    add_bullet("1. Làm chủ hoàn toàn kiến trúc SoC vi mạch: ", "Tự chủ thiết kế từ mã nguồn RTL Verilog tích hợp lõi vi xử lý RISC-V PicoRV32, cầu bus Interconnect 0-delay, 1KB SRAM nội và 2 kênh UART FIFO 32-byte độc lập.")
    add_bullet("2. Tối ưu hóa tài nguyên với cơ chế XIP & In-RAM Worker: ", "Giải quyết triệt để bài toán thiếu bộ nhớ trong ASIC bằng kỹ thuật chạy lệnh tại chỗ từ SPI Flash ngoài và chuyển worker vào SRAM khi cần ghi/xóa dữ liệu.")
    add_bullet("3. Kiểm chứng thực tế toàn diện: ", "Testbench mô phỏng đạt 100% Pass; hệ thống vận hành ổn định trên bo mạch phần cứng FPGA Basys 3 thật cùng đầu đọc RFID RDM6300 qua 10 chức năng CLI.")
    add_bullet("4. Đạt chuẩn sản xuất vi mạch ASIC quốc tế: ", "Luồng OpenLane 2 trên tiến trình SkyWater 130nm đạt hoàn hảo 0 vi phạm Antenna, 0 lỗi LVS và 0 lỗi DRC; tần số hoạt động cực đại Fmax = 92.81 MHz, hoàn toàn sẵn sàng cho công đoạn chế tạo (Tape-out Ready).")

    p_b5 = doc.add_paragraph(style='List Bullet')
    p_b5.paragraph_format.space_before = Pt(1.5)
    p_b5.paragraph_format.space_after = Pt(2.0)
    p_b5.paragraph_format.line_spacing = 1.15
    r5_1 = p_b5.add_run("5. Minh bạch mã nguồn & Tài nguyên thiết kế: ")
    set_font(r5_1, bold=True, color=BLACK)
    r5_2 = p_b5.add_run("Toàn bộ mã nguồn RTL Verilog, Firmware C, Testbench Vivado, kịch bản ASIC OpenLane 2 và tài liệu đồ án được lưu trữ công khai tại GitHub: ")
    set_font(r5_2, color=BLACK)
    add_hyperlink(p_b5,
                  "https://github.com/thaituanhiep/uart-fifo-rfid-asic/tree/rfid_flash_firmware_optimize",
                  "https://github.com/thaituanhiep/uart-fifo-rfid-asic/tree/rfid_flash_firmware_optimize",
                  font_size=10.5, color="2563EB", underline=True)

    p_end = doc.add_paragraph()
    p_end.paragraph_format.space_before = Pt(8)
    p_end.paragraph_format.space_after = Pt(4)
    r_end = p_end.add_run("Học viên xin trân trọng cảm ơn Quý Thầy Cô và bạn đọc đã dành thời gian theo dõi và đánh giá!")
    set_font(r_end, size=11, bold=True, italic=True, color=NAVY)

    # Lưu file
    out_filename = "Tom_Tat_Do_An_RDM6300_PicoRV32_SoC.docx"
    out_path = os.path.join(cur_dir, out_filename)
    doc.save(out_path)
    print(f"Abstract document created successfully: {out_path} ({os.path.getsize(out_path)} bytes)")

    doc_out = os.path.join(doc_dir, out_filename)
    try:
        shutil.copy2(out_path, doc_out)
        print(f"Copied abstract document to document root: {doc_out}")
    except Exception as e:
        print(f"Notice: {doc_out} locked: {e}")

    # Xuất bản PDF tự động
    try:
        import subprocess
        pdf_filename = "Tom_Tat_Do_An_RDM6300_PicoRV32_SoC.pdf"
        pdf_out = os.path.join(doc_dir, pdf_filename)
        pdf_temp = os.path.join(cur_dir, pdf_filename)
        ps_code = f"""
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {{
    $doc = $word.Documents.Open('{os.path.abspath(doc_out)}')
    $doc.ExportAsFixedFormat('{os.path.abspath(pdf_out)}', 17)
    $doc.Close([ref]$false)
}} finally {{
    try {{ $word.Quit() }} catch {{}}
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}}
"""
        subprocess.run(["powershell", "-NoProfile", "-Command", ps_code], capture_output=True)
        if os.path.exists(pdf_out):
            shutil.copy2(pdf_out, pdf_temp)
            print(f"Exported PDF successfully: {pdf_out}")
    except Exception as e:
        print(f"Notice: PDF export skipped: {e}")

if __name__ == "__main__":
    create_abstract_docx()
