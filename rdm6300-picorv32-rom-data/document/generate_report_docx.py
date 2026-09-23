# -*- coding: utf-8 -*-
"""
Script to generate the refined, publication-grade technical project report in DOCX format:
"BÁO CÁO ĐỒ ÁN THIẾT KẾ VI MẠCH SỐ: THIẾT KẾ HỆ THỐNG QUÉT VÀ XỬ LÝ DỮ LIỆU THẺ RFID
TÍCH HỢP CPU RISC-V PICORV32 QUẢN LÝ DỮ LIỆU TRÊN FLASH"
- Exact Title requested by user
- Product introduction: Standalone / Offline RFID scanner without Internet, using Non-Volatile Flash memory
- Completely un-cluttered Main Block Diagram (fig1_block_diagram.png)
- Dedicated RDM6300 Hardware Receiver & Frame Decoder Diagram (fig2_rdm6300_subsystem.png)
- OpenROAD Physical Layout visualization (openroad.png)
- Completely removed Section 5.2 (FPGA utilization and timing tables)
- Table of Contents with native Word tab stops and dot leaders (perfect right-alignment, sentence-case)
- No Header, No Footer (completely blank)
- 100% Black & White / Grayscale typography (zero colored text)
- Final successful ASIC Sign-off run (RUN_2026-09-22_21-34-37) with current config.json parameters
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_report():
    doc = docx.Document()
    
    # -------------------------------------------------------------
    # Page Setup (A4, 1-inch margins)
    # -------------------------------------------------------------
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    
    # NO HEADER, NO FOOTER (Completely removed as requested)
    header = section.header
    for p in header.paragraphs:
        p.text = ""
    footer = section.footer
    for p in footer.paragraphs:
        p.text = ""
        
    # Strictly Black & White palette
    BLACK = RGBColor(0, 0, 0)
    DARK_GRAY = RGBColor(60, 60, 60)
    
    # Style Helpers
    def set_font(run, name="Times New Roman", size=11, bold=False, italic=False, color=BLACK):
        run.font.name = name
        run.font.size = Pt(size)
        run.bold = bold
        run.italic = italic
        run.font.color.rgb = color

    def add_p(text="", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=4.5, line_spacing=1.15):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        if text:
            r = p.add_run(text)
            set_font(r, color=BLACK)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        set_font(r, size=13.5, bold=True, color=BLACK)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        set_font(r, size=12, bold=True, color=BLACK)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(5)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        set_font(r, size=11, bold=True, italic=True, color=BLACK)
        return p

    def add_bullet(bold_prefix="", text=""):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
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
        set_font(r, size=9.5, italic=True, color=BLACK)
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
        
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F4F4F4"/>')
        tcPr.append(shd)
        
        pad = parse_xml(
            f'<w:tcMar {nsdecls("w")}>'
            f'<w:top w:w="90" w:type="dxa"/>'
            f'<w:bottom w:w="90" w:type="dxa"/>'
            f'<w:left w:w="130" w:type="dxa"/>'
            f'<w:right w:w="130" w:type="dxa"/>'
            f'</w:tcMar>'
        )
        tcPr.append(pad)
        
        cell.paragraphs[0].text = ""
        for idx, line in enumerate(lines):
            p = cell.add_paragraph() if idx > 0 else cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.05
            r = p.add_run(line)
            set_font(r, name="Consolas", size=8.5, color=BLACK)
            
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(0)
        p_sp.paragraph_format.space_after = Pt(3)

    def style_table(table, col_widths, col_alignments, header_bg="E6E6E6"):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        tblPr = table._tbl.tblPr
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
            f'<w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
            f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
            f'<w:insideV w:val="none"/>'
            f'<w:left w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(borders)
        
        for row_idx, row in enumerate(table.rows):
            is_header = (row_idx == 0)
            trPr = row._tr.get_or_add_trPr()
            trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
            if is_header:
                trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
            
            for col_idx, cell in enumerate(row.cells):
                cell.width = col_widths[col_idx]
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                tcPr = cell._tc.get_or_add_tcPr()
                
                top_pad = "100" if is_header else "75"
                bot_pad = "100" if is_header else "75"
                pad_xml = parse_xml(
                    f'<w:tcMar {nsdecls("w")}>'
                    f'<w:top w:w="{top_pad}" w:type="dxa"/>'
                    f'<w:bottom w:w="{bot_pad}" w:type="dxa"/>'
                    f'<w:left w:w="110" w:type="dxa"/>'
                    f'<w:right w:w="110" w:type="dxa"/>'
                    f'</w:tcMar>'
                )
                tcPr.append(pad_xml)
                
                if is_header:
                    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{header_bg}"/>')
                    tcPr.append(shd)
                elif row_idx % 2 == 1:
                    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F9F9F9"/>')
                    tcPr.append(shd)
                
                for p in cell.paragraphs:
                    p.paragraph_format.space_before = Pt(0)
                    p.paragraph_format.space_after = Pt(0)
                    p.alignment = col_alignments[col_idx]
                    for r in p.runs:
                        if is_header:
                            set_font(r, size=9, bold=True, color=BLACK)
                        else:
                            set_font(r, size=9, bold=r.bold, italic=r.italic, color=BLACK)

    cur_dir = os.path.dirname(os.path.abspath(__file__))

    # =============================================================
    # TRANG 1: TRANG BÌA (COVER PAGE)
    # =============================================================
    add_p("", space_before=50)
    p_title1 = add_p("BÁO CÁO ĐỒ ÁN THIẾT KẾ VI MẠCH SỐ", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=16)
    set_font(p_title1.runs[0], size=16, bold=True, color=BLACK)

    p_title2 = add_p("THIẾT KẾ HỆ THỐNG QUÉT VÀ XỬ LÝ DỮ LIỆU THẺ RFID TÍCH HỢP CPU RISC-V PICORV32 QUẢN LÝ DỮ LIỆU TRÊN FLASH", 
                     align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18, line_spacing=1.25)
    set_font(p_title2.runs[0], size=14.5, bold=True, color=BLACK)

    p_sub = add_p("Hiện thực vật lý trên tiến trình ASIC SkyWater Sky130A (OpenLane 2) — Kiểm chứng thực nghiệm trên FPGA Basys 3", 
                  align=WD_ALIGN_PARAGRAPH.CENTER, space_after=90)
    set_font(p_sub.runs[0], size=11.5, italic=True, color=DARK_GRAY)

    p_group = add_p("Nhóm thực hiện: [Điền tên nhóm]\nThành viên: [Họ tên 1], [Họ tên 2], [Họ tên 3]\nCán bộ hướng dẫn: [Điền tên GVHD]",
                    align=WD_ALIGN_PARAGRAPH.CENTER, space_after=120, line_spacing=1.3)
    for r in p_group.runs:
        set_font(r, size=11, bold=False, color=BLACK)

    p_ref = add_p("Nguồn tài liệu tham chiếu: Repository rdm6300-picorv32-rom-data; cấu hình vật lý config.json; báo cáo ký duyệt Antenna / DRC / LVS / STA (OpenLane 2 - SkyWater Sky130A, run RUN_2026-09-22_21-34-37) và dữ liệu đo đạc thực nghiệm trên FPGA Basys 3 đính kèm",
                  align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0, line_spacing=1.15)
    set_font(p_ref.runs[0], size=9.5, italic=True, color=DARK_GRAY)

    doc.add_page_break()

    # =============================================================
    # TRANG 2: MỤC LỤC CHUẨN XÁC VỚI TAB STOP VÀ DOT LEADER
    # (Viết thường, không có "Mục lục ... 2" lặp lại, căn lề phải tuyệt đối)
    # =============================================================
    add_h1("Mục lục")
    
    # Exact Table of Contents items (sentence-case, no FPGA 5.2 resource table)
    toc_items = [
        ("1. Giới thiệu", "3", True, 0),
        ("1.1. Bối cảnh và đặt vấn đề", "3", False, 0.2),
        ("1.2. Định hướng sản phẩm: thiết bị quét thẻ RFID offline không cần internet", "3", False, 0.2),
        ("1.3. Lý do lựa chọn bộ nhớ bất biến non-volatile flash", "3", False, 0.2),
        ("1.4. Mục tiêu nghiên cứu và đóng góp của đề tài", "3", False, 0.2),
        ("2. Cơ sở lý thuyết và các công nghệ liên quan", "3", True, 0),
        ("3. Kiến trúc hệ thống rdm6300-picorv32-rom-data", "4", True, 0),
        ("3.1. Sơ đồ khối kiến trúc vi hệ thống", "4", False, 0.2),
        ("3.2. Lõi vi xử lý RISC-V PicoRV32 (RV32I)", "4", False, 0.2),
        ("3.3. Cấu trúc bộ nhớ kép: mask ROM 8KB và data SRAM 2KB", "4", False, 0.2),
        ("3.4. Khối giải mã phần cứng thẻ RFID RDM6300 (125 kHz)", "5", False, 0.2),
        ("3.5. Khối điều khiển bộ nhớ flash SPI ngoại vi (S25FL032P)", "5", False, 0.2),
        ("3.6. Khối giao tiếp máy tính (host PC UART) và GPIO", "5", False, 0.2),
        ("3.7. Bản đồ bộ nhớ MMIO (memory map)", "5", False, 0.2),
        ("4. Phương pháp thiết kế vật lý trên ASIC OpenLane 2 (SkyWater Sky130A)", "6", True, 0),
        ("4.1. Thiết lập công nghệ và cấu hình tham số config.json", "6", False, 0.2),
        ("4.2. Luồng tự động hóa từ RTL đến GDSII", "6", False, 0.2),
        ("5. Demo chức năng và kiểm chứng thực nghiệm trên FPGA Basys 3", "7", True, 0),
        ("5.1. Thiết lập phần cứng demo trên bo mạch Basys 3", "7", False, 0.2),
        ("5.2. Hướng dẫn sử dụng phần mềm điều khiển host console từng bước", "7", False, 0.2),
        ("5.3. Kịch bản thực nghiệm quẹt thẻ thực tế và kết quả xác thực", "8", False, 0.2),
        ("6. Kết quả và thảo luận", "9", True, 0),
        ("6.1. Các quyết định thiết kế tối ưu hóa diện tích và công suất (PPA)", "9", False, 0.2),
        ("6.2. Hạn chế của thiết kế hiện tại", "9", False, 0.2),
        ("7. Kết quả triển khai và ký duyệt ASIC (OpenLane 2 - SkyWater Sky130A)", "10", True, 0),
        ("7.1. Phân tích cấu hình config.json giúp đạt chuẩn tapeout", "10", False, 0.2),
        ("7.2. Bố trí layout vật lý và trực quan hóa trên OpenROAD", "10", False, 0.2),
        ("7.3. Kết quả sign-off toàn diện của run thành công (DRC, LVS, antenna clean)", "10", False, 0.2),
        ("7.4. Phân tích định thời tĩnh STA đa góc đo (9 corners) và công suất tiêu thụ", "11", False, 0.2),
        ("7.5. Các định hướng phát triển tiếp theo", "11", False, 0.2),
        ("8. Kết luận", "12", True, 0),
    ]
    
    for title, pg, is_main, indent in toc_items:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(1.5)
        p_t.paragraph_format.space_after = Pt(2.0)
        p_t.paragraph_format.line_spacing = 1.12
        if indent > 0:
            p_t.paragraph_format.left_indent = Inches(indent)
            
        # Add native Word right tab stop with dot leader (with safety margin inside 6.27" boundary)
        p_t.paragraph_format.tab_stops.add_tab_stop(Inches(6.20), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        
        r1 = p_t.add_run(title)
        set_font(r1, size=10 if not is_main else 10.5, bold=is_main, color=BLACK)
        
        r2 = p_t.add_run(f"\t{pg}")
        set_font(r2, size=10 if not is_main else 10.5, bold=is_main, color=BLACK)

    doc.add_page_break()

    # =============================================================
    # TRANG 3: GIỚI THIỆU & CƠ SỞ LÝ THUYẾT
    # =============================================================
    add_h1("1. Giới thiệu")
    add_h2("1.1. Bối cảnh và đặt vấn đề")
    add_p("Hệ thống nhận dạng qua tần số vô tuyến (Radio-Frequency Identification – RFID) dải tần số thấp 125 kHz (chuẩn EM4100) là giải pháp kinh điển và bền bỉ trong các hệ thống an ninh kiểm soát ra vào (Access Control), thẻ chấm công và theo dõi định danh nhân sự. Module đầu đọc RFID RDM6300 là thiết bị phần cứng phổ biến, giải điều chế sóng mang từ ăng-ten cảm ứng và truyền chuỗi dữ liệu 14 byte định dạng ASCII qua giao tiếp nối tiếp UART.")

    add_h2("1.2. Định hướng sản phẩm: thiết bị quét thẻ RFID offline không cần internet")
    add_p("Trong xu hướng IoT hiện nay, nhiều giải pháp kiểm soát ra vào phụ thuộc nặng nề vào kết nối mạng Internet hoặc hạ tầng máy chủ đám mây (Cloud-based Access Control). Tuy nhiên, kiến trúc phụ thuộc Internet bộc lộ nhiều điểm yếu nghiêm trọng: (1) hệ thống sẽ bị tê liệt hoàn toàn khi mất kết nối mạng hoặc đứt đường truyền cáp quang; (2) độ trễ xác thực lớn do phải truyền nhận gói tin qua mạng công cộng; (3) nguy cơ rò rỉ dữ liệu định danh nhân sự và tiềm ẩn hiểm họa bị tấn công an ninh mạng từ xa (Cybersecurity threats); (4) hoàn toàn không thể triển khai tại các địa bàn xa xôi, trạm gác biên giới, kho quân sự, hầm mỏ, công trường xây dựng hoặc các phân xưởng biệt lập.")
    add_p("Sản phẩm của đồ án này được định hướng phát triển là một thiết bị quẹt thẻ RFID vận hành hoàn toàn độc lập (Standalone / Offline Access Controller), không cần kết nối Internet. Thiết bị tự thu nhận tín hiệu từ thẻ RFID 125 kHz, tự giải mã và tự đối chiếu danh sách cấp phép ngay tại chỗ trong thời gian thực với độ trễ chỉ tính bằng microsecond.")

    add_h2("1.3. Lý do lựa chọn bộ nhớ bất biến non-volatile flash")
    add_p("Do hệ thống hoạt động độc lập không có mạng Internet để gửi dữ liệu về máy chủ đám mây, bài toán then chốt đặt ra là: Làm thế nào để lưu trữ danh sách thẻ người dùng (Whitelist) và nhật ký các lần quẹt thẻ (Access Logs) an toàn, bền vững mà không bị mất khi mất điện hoặc tắt nguồn thiết bị? Bộ nhớ bất biến (Non-Volatile Memory – NVM), cụ thể là bộ nhớ SPI NOR Flash (Spansion S25FL032P / Winbond W25Qxx), được lựa chọn vì các ưu điểm vượt trội:")
    add_bullet("1. Bảo toàn dữ liệu tuyệt đối khi mất nguồn: ", "Khác với RAM (mất sạch dữ liệu khi ngắt điện), bộ nhớ Flash lưu trữ thông tin bằng các cổng nổi (floating-gate), bảo toàn danh sách thẻ và lịch sử quẹt thẻ trong hơn 20 năm mà không cần pin dự phòng.")
    add_bullet("2. Dung lượng lớn và chi phí thấp: ", "Với chip Flash dung lượng 32 Mbit (4 MBytes), hệ thống có khả năng lưu trữ tới hàng chục nghìn mã thẻ người dùng và hàng triệu bản ghi nhật ký quẹt thẻ với chi phí phần cứng cực kỳ thấp.")
    add_bullet("3. Tối ưu hóa số lượng chân kết nối (Pin-count Efficiency): ", "Giao tiếp chuẩn SPI chỉ sử dụng 4 đường tín hiệu (CS_N, SCK, MOSI, MISO), tiết kiệm tối đa số chân I/O quý giá của chip vi mạch ASIC (chỉ có 31 chân).")
    add_bullet("4. Độ bền bỉ công nghiệp: ", "Hỗ trợ hơn 100,000 chu kỳ ghi/xóa (P/E cycles), đáp ứng hoàn hảo tiêu chuẩn vận hành liên tục 24/7.")
    add_bullet("5. Bảo trì cục bộ tiện lợi: ", "Khi cần trích xuất dữ liệu, người quản trị chỉ cần cắm máy tính bảo trì qua cổng USB-UART cục bộ để xuất file CSV nhật ký hoặc nạp thêm thẻ mới.")

    add_h2("1.4. Mục tiêu nghiên cứu và đóng góp của đề tài")
    add_bullet("Thiết kế vi kiến trúc SoC tối ưu PPA: ", "Tích hợp lõi PicoRV32 với bộ giải mã phần cứng RDM6300 tự trị, bộ điều khiển SPI Flash ngoại vi và Host PC UART.")
    add_bullet("Phần cứng hóa giải mã RFID: ", "Xây dựng máy trạng thái FSM 5 trạng thái chuyên trách, giải mã khung 14 byte và tính toán đối chiếu XOR Checksum song song trong phần cứng, giải phóng 100% thời gian xử lý cho CPU.")
    add_bullet("Hiện thực kiến trúc bộ nhớ đột phá: ", "Phân tầng thành Mask ROM 8KB tổ hợp (0 DFFs) chứa firmware nhúng và Data SRAM 2KB ghi đơn chu kỳ, giảm hơn 85% Flip-Flops so với thiết kế RAM thông thường.")
    add_bullet("Triển khai ASIC SkyWater Sky130A trên OpenLane 2: ", "Thực thi toàn bộ quy trình thiết kế vật lý từ RTL đến bản vẽ layout GDSII hoàn chỉnh, đạt chuẩn Ký duyệt (Sign-off Clean): 0 Antenna Violations, 0 DRC, 0 LVS và thỏa mãn định thời trên cả 9 góc đo (corners).")
    add_bullet("Kiểm chứng chức năng trên FPGA Basys 3: ", "Sử dụng bo mạch FPGA Digilent Basys 3 (Artix-7 XC7A35T) như một nền tảng demo thực nghiệm thời gian thực (Hardware In-The-Loop).")

    add_h1("2. Cơ sở lý thuyết và các công nghệ liên quan")
    add_p("Kiến trúc tập lệnh RISC-V RV32I và PicoRV32: RISC-V là kiến trúc tập lệnh mở chuẩn mực. Lõi PicoRV32 hiện thực đầy đủ tập lệnh cơ sở RV32I với 32 thanh ghi 32-bit, sử dụng giao diện bộ nhớ tối giản (valid/ready handshake) với độ trễ bus xác định, cực kỳ thích hợp cho các vi mạch nhúng yêu cầu diện tích silicon tối thiểu.")
    add_p("Giao thức đóng khung RDM6300: Khung truyền nối tiếp UART 9600 bps gồm chính xác 14 byte: Byte 0 là Header (0x02 - STX); 10 byte tiếp theo (Byte 1-10) là các ký tự ASCII Hex biểu diễn 5 byte dữ liệu thẻ; 2 byte tiếp theo (Byte 11-12) là ký tự ASCII biểu diễn mã Checksum; và Byte 13 là Footer (0x03 - ETX). Thuật toán kiểm tra toàn vẹn yêu cầu lấy phép toán XOR bitwise giữa 5 byte dữ liệu và so khớp với byte Checksum: Data[0] ^ Data[1] ^ Data[2] ^ Data[3] ^ Data[4] == Checksum.")
    add_p("Bộ nhớ SPI Flash S25FL032P và giải pháp STARTUPE2: Chip Flash 32 Mbit kết nối qua giao tiếp SPI 4 dây chuẩn (CS_N, SCK, MOSI, MISO), hỗ trợ các lệnh cơ bản: Read Data (0x03), Page Program (0x02), Sector Erase 4KB (0x20), Write Enable (0x06) và Read Status (0x05) kiểm tra cờ WIP (Write-In-Progress). Trên FPGA Xilinx 7-Series, chân CCLK nối tới Flash được chia sẻ với chân nạp bitstream; do đó, để phát xung SCK trong quá trình chạy, thiết kế phải sử dụng nguyên thủy STARTUPE2 qua cổng USRCCLKO.")
    add_p("Hiệu ứng Antenna trong công nghệ bán dẫn Sky130A: Trong các bước khắc khô plasma (RIE), các đường dây kim loại dài tích lũy các ion mang điện. Nếu điện tích không có đường thoát, nó sẽ phóng qua lớp màng oxit mỏng của cực cổng transistor MOS (Gate Oxide Breakdown), phá hủy linh kiện vĩnh viễn. Để ngăn chặn, công cụ tự động hóa thiết kế vật lý phải tính toán tỷ số diện tích kim loại trên diện tích cổng (Antenna Ratio) và chèn các diode khuếch tán bảo vệ (sky130_fd_sc_hd__diode_2) vào các vị trí vi phạm.")

    doc.add_page_break()

    # =============================================================
    # TRANG 4: KIẾN TRÚC HỆ THỐNG (BLOCK DIAGRAM CHÍNH RÕ NÉT)
    # =============================================================
    add_h1("3. Kiến trúc hệ thống rdm6300-picorv32-rom-data")
    add_h2("3.1. Sơ đồ khối kiến trúc vi hệ thống")
    add_p("Hệ thống rdm6300-picorv32-rom-data là một cấu trúc SoC nhúng tối giản, chặt chẽ, tối ưu hóa toàn diện cho việc thu nhận định danh RFID và lưu trữ cơ sở dữ liệu Flash. Kiến trúc tổng thể được thể hiện trong Hình 1.")

    # Chèn Hình 1: Block diagram chính un-cluttered
    fig1_path = os.path.join(cur_dir, "fig1_block_diagram.png")
    if os.path.exists(fig1_path):
        p_img1 = doc.add_paragraph()
        p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img1.paragraph_format.space_before = Pt(4)
        p_img1.paragraph_format.space_after = Pt(2)
        p_img1.paragraph_format.keep_with_next = True
        run_img1 = p_img1.add_run()
        run_img1.add_picture(fig1_path, width=Inches(6.15))
        add_caption("Hình 1. Sơ đồ khối kiến trúc tổng thể vi hệ thống SoC PicoRV32 tích hợp RDM6300 và SPI Flash")

    add_h2("3.2. Lõi vi xử lý RISC-V PicoRV32 (RV32I)")
    add_p("Lõi xử lý PicoRV32 (rtl/picorv32.v) giữ vai trò điều phối trung tâm. Lõi được cấu hình ở chế độ chuẩn RV32I không sử dụng bộ nhân/chia phần cứng nhằm giảm kích thước cổng logic tối đa. Giao tiếp bộ nhớ được thực hiện qua bus đồng bộ gồm các tín hiệu: mem_valid, mem_ready, mem_addr[31:0], mem_wdata[31:0], mem_wstrb[3:0], mem_rdata[31:0]. CPU khởi động trực tiếp tại địa chỉ 0x0000_0000 trong Mask ROM.")

    add_h2("3.3. Cấu trúc bộ nhớ kép: mask ROM 8KB và data SRAM 2KB")
    add_p("Một cải tiến mang tính bước ngoặt của đề tài là việc loại bỏ hoàn toàn ý tưởng dùng 8KB SRAM flip-flop (vốn tiêu tốn hơn 70,000 DFF, làm bùng nổ diện tích chip lên hơn 4 mm² và phát sinh vô số lỗi Antenna), thay thế bằng kiến trúc bộ nhớ kép chuyên biệt:")
    add_bullet("Mask ROM 8KB (rtl/mask_rom.v): ", "Lưu trữ toàn bộ mã nhị phân firmware nhúng (firmware.hex). Toàn bộ mảng nhớ 8192 bytes được hiện thực bằng mạch logic tổ hợp thuần túy (Combinational MUX Decoder). Khối này tiêu tốn chính xác 0 Flip-Flop (0 DFFs), giúp triệt tiêu tải trọng trên cây xung nhịp, giảm 85% diện tích so với SRAM flip-flop và hoàn toàn miễn nhiễm với lỗi vi phạm hold time.")
    add_bullet("Data SRAM 2KB (rtl/data_sram.v): ", "Mảng bộ nhớ đọc/ghi dung lượng 2048 bytes dùng làm không gian biến toàn cục (.data, .bss) và ngăn xếp (Stack). Bộ nhớ phản hồi đọc đơn chu kỳ (Single-Cycle Latency) và hỗ trợ ghi theo từng byte thông qua tín hiệu mặt nạ mem_wstrb[3:0], đảm bảo hiệu năng tính toán cao nhất cho CPU.")

    doc.add_page_break()

    # =============================================================
    # TRANG 5: KHỐI GIẢI MÃ RDM6300 (HÌNH RIÊNG) & BẢN ĐỒ BỘ NHỚ
    # =============================================================
    add_h2("3.4. Khối giải mã phần cứng thẻ RFID RDM6300 (125 kHz)")
    add_p("Để việc xử lý RFID hoàn toàn không gây tải cho CPU và không làm tắc nghẽn giao tiếp bus hệ thống, toàn bộ chuỗi thu nhận và giải mã thẻ RDM6300 được tách biệt thành một nhánh phần cứng độc lập kết nối đến thanh ghi RFID MMIO Registers, như được minh họa chi tiết trong sơ đồ riêng tại Hình 2.")

    # Chèn Hình 2: Sơ đồ khối riêng cho RDM6300
    fig2_path = os.path.join(cur_dir, "fig2_rdm6300_subsystem.png")
    if os.path.exists(fig2_path):
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img2.paragraph_format.space_before = Pt(4)
        p_img2.paragraph_format.space_after = Pt(2)
        p_img2.paragraph_format.keep_with_next = True
        run_img2 = p_img2.add_run()
        run_img2.add_picture(fig2_path, width=Inches(6.15))
        add_caption("Hình 2. Sơ đồ khối chi tiết đường ống thu nhận và giải mã phần cứng thẻ RFID RDM6300")

    add_p("Chuỗi giải mã phần cứng bao gồm các tầng xử lý tuần tự chặt chẽ:")
    add_bullet("1. Tầng đồng bộ CDC (sync_2ff.v): ", "Khử hiện tượng metastability khi tín hiệu không đồng bộ rdm6300_rx_i từ đầu đọc ngoài đi vào miền xung nhịp hệ thống (40/50 MHz).")
    add_bullet("2. Tầng giải tuần tự UART (uart_rx.v): ", "Hoạt động ở tốc độ 9600 baud (8-N-1), chia xung nhịp và lấy mẫu majority voting 3 điểm tại giữa bit, xuất tín hiệu byte hợp lệ rx_dv và dữ liệu 8-bit rx_byte.")
    add_bullet("3. Tầng FSM giải mã khung (rdm6300_frame_decoder.v): ", "Máy trạng thái 5 bước nhận diện STX (0x02), thu thập 10 ký tự ASCII dữ liệu (chuyển đổi tổ hợp tức thời sang 5 byte Hex), thu thập 2 ký tự Checksum, nhận diện ETX (0x03) và kích hoạt bộ tính XOR Checksum phần cứng song song: Data[0] ^ Data[1] ^ Data[2] ^ Data[3] ^ Data[4] == Checksum.")
    add_bullet("4. Tầng thanh ghi MMIO: ", "Khi kiểm tra Checksum thành công, cờ hw_card_valid bật lên 1 chu kỳ, chốt mã thẻ 40-bit vào thanh ghi rfid_tag_hi và rfid_tag_lo, đồng thời phát tín hiệu card_event_o kích hoạt ngắt CPU IRQ.")

    add_h2("3.5. Khối điều khiển bộ nhớ flash SPI ngoại vi (S25FL032P)")
    add_p("Khối spi_flash_controller.v đóng vai trò cầu nối phần cứng giữa bus MMIO và chip Flash ngoài, tự động hóa toàn bộ các giao thức nối tiếp SPI (Page Program 0x02, Read 0x03, Sector Erase 0x20, và tự động kiểm tra cờ WIP qua Read Status Register 0x05). Vùng lưu trữ thẻ và nhật ký an toàn được quy hoạch từ địa chỉ 0x30_0000 và 0x31_0000.")

    add_h2("3.6. Khối giao tiếp máy tính (host PC UART) và GPIO")
    add_p("Khối simpleuart.v cung cấp kênh truyền nối tiếp 9600 baud kết nối cổng USB-UART để bảo trì, xuất nhật ký và đồng bộ danh sách thẻ. Khối GPIO điều khiển 16 LED trạng thái (LED 0 nhịp tim 1 Hz, LED 1 Flash Busy, LED 2 thẻ hợp lệ, LED[15:6] trạng thái chẩn đoán).")

    add_h2("3.7. Bản đồ bộ nhớ MMIO (memory map)")
    add_p("Bảng 1 thể hiện không gian địa chỉ Memory-Mapped I/O (MMIO) hoàn chỉnh của hệ thống SoC PicoRV32.")

    # Bảng 1: Memory Map
    t1 = doc.add_table(rows=12, cols=3)
    t1_headers = ["Dải địa chỉ (Hex)", "Ngoại vi / Chức năng", "Mô tả chi tiết và Phương thức truy xuất"]
    t1_data = [
        ["0x0000_0000 - 0x0000_1FFF", "8KB Mask ROM", "Chứa mã lệnh thực thi (firmware.hex). Chỉ đọc (Read-Only), 0 DFFs."],
        ["0x0000_2000 - 0x0000_27FF", "2KB Data SRAM", "Bộ nhớ dữ liệu đọc/ghi: Chứa biến toàn cục, ngăn xếp (Stack). Ghi theo byte mask."],
        ["0x1000_0000", "RDM6300 Baud Divisor", "Thanh ghi cài đặt tốc độ baud UART RFID (Mặc định: 100MHz / 9600 = 10416)."],
        ["0x1000_0004", "RDM6300 UART RX", "Đọc dữ liệu byte thô nhận từ RFID UART (Trả về -1 nếu FIFO rỗng)."],
        ["0x1000_0008", "RFID Tag ID (Hardware)", "Đọc trực tiếp 32-bit mã thẻ đã giải mã và xác thực Checksum thành công."],
        ["0x1000_000C", "RFID Tag Valid Flag", "Cờ báo thẻ hợp lệ: Bit 0 = 1 khi có thẻ quẹt hợp lệ mới được giải mã."],
        ["0x2000_0000", "SPI Flash Control", "Bit 0: Trigger thực thi; Bit [3:1]: Opcode (0: Read, 1: Write, 2: Sector Erase)."],
        ["0x2000_0004", "SPI Flash Status", "Bit 0: Busy (1: Đang bận chu kỳ SPI/WIP); Bit 1: Write Done; Bit 2: Error."],
        ["0x2000_0008", "SPI Flash Address", "Địa chỉ Flash 24-bit (Vùng an toàn thẻ: 0x30_0000, Vùng nhật ký: 0x31_0000)."],
        ["0x2000_000C", "SPI Flash Write Data", "32-bit dữ liệu cần ghi vào Flash qua lệnh Page Program."],
        ["0x2000_0010", "SPI Flash Read Data", "32-bit dữ liệu đọc ra từ Flash sau khi hoàn tất lệnh Read."],
    ]
    for c_idx, h_text in enumerate(t1_headers):
        t1.cell(0, c_idx).paragraphs[0].text = h_text
    for r_idx, row_vals in enumerate(t1_data):
        for c_idx, val in enumerate(row_vals):
            t1.cell(r_idx + 1, c_idx).paragraphs[0].text = val
            
    col_w1 = [Inches(1.8), Inches(1.8), Inches(2.67)]
    col_a1 = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    style_table(t1, col_w1, col_a1)
    add_caption("Bảng 1. Bản đồ không gian địa chỉ Memory-Mapped I/O (MMIO) của hệ thống SoC")

    doc.add_page_break()

    # =============================================================
    # TRANG 6: PHƯƠNG PHÁP TRIỂN KHAI VẬT LÝ ASIC
    # =============================================================
    add_h1("4. Phương pháp thiết kế vật lý trên ASIC OpenLane 2 (SkyWater Sky130A)")
    add_p("Quy trình thiết kế vật lý ASIC được thực hiện hoàn toàn tự động hóa bằng công cụ OpenLane 2 trên tiến trình bán dẫn CMOS 130 nm SkyWater (PDK: sky130A, thư viện cell chuẩn: sky130_fd_sc_hd). Mục tiêu của luồng là tạo ra file layout GDSII không còn bất kỳ vi phạm nào về mặt hình học, liên kết điện và định thời.")

    add_h2("4.1. Thiết lập công nghệ và cấu hình tham số config.json")
    add_p("Toàn bộ quy trình điều khiển của OpenLane 2 được chỉ định tường minh trong file cấu hình chuẩn config.json của dự án. File config.json hiện tại được thiết lập với các thông số then chốt sau:")
    add_bullet("Tên thiết kế & Bộ thư viện: ", "\"DESIGN_NAME\": \"rdm6300_picorv32_soc\", \"PDK\": \"sky130A\", \"STD_CELL_LIBRARY\": \"sky130_fd_sc_hd\".")
    add_bullet("Ràng buộc xung nhịp hệ thống: ", "\"CLOCK_PORT\": \"clk\", \"CLOCK_PERIOD\": 20.0 (tương ứng tần số thiết kế mục tiêu 50 MHz).")
    add_bullet("Quy hoạch mặt bằng và Mật độ lõi: ", "\"FP_CORE_UTIL\": 30 (Mật độ khởi tạo 30% giúp tạo không gian rộng rãi cho các kênh định tuyến và chèn diode bảo vệ), \"FP_PIN_ORDER_CFG\": \"dir::pin_order.cfg\" phân bổ 31 chân I/O trên 4 cạnh die.")
    add_bullet("Chiến lược định vị và Di chuyển tế bào: ", "\"PL_MAX_DISPLACEMENT_X\": 100, \"PL_MAX_DISPLACEMENT_Y\": 2, \"PL_OPTIMIZE_MIRRORING\": false.")
    add_bullet("Cấu hình chèn Diode chống Antenna tự động: ", "\"RUN_HEURISTIC_DIODE_INSERTION\": true, \"HEURISTIC_ANTENNA_THRESHOLD\": 65 (khi tỷ số antenna vượt ngưỡng 65, thuật toán tự động đặt diode bảo vệ), \"DIODE_PADDING\": 0, \"RUN_ANTENNA_REPAIR\": true, \"DIODE_ON_PORTS\": \"in\".")
    add_bullet("Cấu hình bộ định tuyến toàn cục TritonRoute (GRT): ", "\"GRT_OVERFLOW_ITERS\": 60, \"GRT_ANTENNA_ITERS\": 25, \"GRT_ANTENNA_MARGIN\": 30, \"GRT_ALLOW_CONGESTION\": true, \"GRT_LAYER_ADJUSTMENTS\": [0.99, 0.65, 0.30, 0, 0, 0] (Giảm tải định tuyến trên các lớp kim loại thấp met1/met2/met3 để hướng các bus dài lên met4/met5).")
    add_bullet("Chiến lược tổng hợp logic: ", "\"SYNTH_STRATEGY\": \"AREA 0\" (Tập trung tối ưu hóa diện tích ở mức cổng logic, chia sẻ cổng và suy luận multiplexer gọn nhẹ).")

    add_h2("4.2. Luồng tự động hóa từ RTL đến GDSII")
    add_p("Luồng OpenLane 2 thực thi tuần tự và khép kín qua các giai đoạn:")
    add_bullet("1. Yosys Synthesis: ", "Tổng hợp mã nguồn Verilog RTL thành netlist cell chuẩn Sky130A, tối ưu hóa đồ thị boolean.")
    add_bullet("2. Floorplan & PDN: ", "Xác định kích thước khuôn die và vùng core, tạo các dải cấp nguồn VPWR/VGND (Power Distribution Network) trên lớp kim loại met4 và met5, chèn hàng loạt tap cell và endcap cell.")
    add_bullet("3. Placement & CTS: ", "Định vị linh kiện toàn cục và cục bộ. TritonCTS tổng hợp cây xung nhịp cân bằng, chèn các bộ đệm clock chuyên dụng nhằm giảm thiểu skew.")
    add_bullet("4. Routing & Antenna Repair: ", "TritonRoute thực hiện định tuyến chi tiết 5 lớp kim loại. Module sửa lỗi Antenna tích hợp diode chuyên dụng sky130_fd_sc_hd__diode_2 sát cực cổng vi phạm.")
    add_bullet("5. Physical Verification & Sign-off: ", "Kiểm tra DRC vật lý bằng Magic và KLayout, kiểm tra LVS đối chiếu netlist bằng Netgen, phân tích định thời tĩnh STA đa góc đo (9 corners) bằng OpenROAD và xuất bản vẽ layout GDSII hoàn thiện.")

    doc.add_page_break()

    # =============================================================
    # TRANG 7: DEMO CHỨC NĂNG TRÊN FPGA BASYS 3
    # (Đã bỏ mục 5.2 kết quả tài nguyên và timing theo yêu cầu người dùng)
    # =============================================================
    add_h1("5. Demo chức năng và kiểm chứng thực nghiệm trên FPGA Basys 3")
    add_p("Để kiểm chứng tính đúng đắn của toàn bộ thiết kế vi mạch trước khi đưa vào sản xuất ASIC, nhóm đã triển khai một phiên bản demo chức năng hoàn chỉnh trên bo mạch FPGA Digilent Basys 3 (Artix-7 XC7A35T). Mục tiêu của bước này là xác thực tương tác thời gian thực (Hardware In-The-Loop) giữa lõi PicoRV32, phần cứng giải mã thẻ RFID RDM6300 thật, bộ nhớ SPI Flash và phần mềm giao tiếp máy tính.")

    add_h2("5.1. Thiết lập phần cứng demo trên bo mạch Basys 3")
    add_p("Hệ thống phần cứng demo được kết nối trực quan như sau:")
    add_bullet("1. Bo mạch FPGA: ", "Digilent Basys 3 trang bị chip Xilinx Artix-7 (XC7A35T-CPG236-1) và bộ nhớ Flash SPI Spansion S25FL032P (32 Mbit = 4 MBytes).")
    add_bullet("2. Module đầu đọc RFID RDM6300: ", "Hoạt động ở tần số 125 kHz. Chân TX của module được nối vào chân Pmod JA1 (chân J1 của FPGA). Nguồn cấp VCC (5V/3.3V) và GND được lấy trực tiếp từ header Pmod của Basys 3.")
    add_bullet("3. Giao tiếp máy tính host: ", "Cáp Micro-USB vừa cấp nguồn cho bo mạch vừa đóng vai trò kênh truyền UART qua chip chuyển đổi FTDI (kết nối cổng ảo COM trên Windows/Linux ở tốc độ 9600 bps).")
    add_bullet("4. Nguyên thủy STARTUPE2: ", "Trong file fpga/rtl/top_basys3_picorv32_rdm6300.v, xung nhịp Flash SCK được dẫn vào cổng USRCCLKO của nguyên thủy STARTUPE2 của Xilinx để điều khiển xung clock tới chip Flash ngoài sau khi bitstream đã nạp xong.")
    add_bullet("5. Hiển thị LED 7 đoạn (4-digit 7-segment display): ", "Tích hợp bộ điều khiển quét 4 LED 7 đoạn (seg[6:0], an[3:0], dp) độc lập trên tầng wrapper FPGA (top_basys3_picorv32_rdm6300.v). Ở trạng thái chờ bình thường (không quẹt thẻ), toàn bộ 4 LED 7 đoạn tắt hoàn toàn (Blanking). Khi quẹt thẻ, hệ thống snoop kết quả xác thực từ CPU: nếu thẻ hợp lệ (được cấp phép trong Flash) màn hình sáng hiển thị chữ PASS (P-A-S-S) trong 2.0 giây rồi tự tắt; nếu thẻ không hợp lệ (từ chối truy cập) màn hình sáng hiển thị chữ FAIL (F-A-I-L) trong 2.0 giây rồi tự tắt.")

    add_h2("5.2. Hướng dẫn sử dụng phần mềm điều khiển host console từng bước")
    add_p("Nhóm đã phát triển phần mềm giao tiếp máy tính chuyên nghiệp viết bằng ngôn ngữ C (host/main.c) biên dịch thành file thực thi độc lập host/rdm6300_manager.exe trên Windows. Quy trình vận hành hệ thống từng bước như sau:")
    add_bullet("Bước 1: Nạp Bitstream vào FPGA: ", "Mở Vivado Hardware Manager hoặc chạy script fpga/program_basys3.bat để nạp file top_basys3_picorv32_rdm6300.bit vào Basys 3. Đèn LED[0] (Heartbeat) bắt đầu nhấp nháy 1 Hz, báo hiệu lõi PicoRV32 đang chạy bình thường, trap = 0.")
    add_bullet("Bước 2: Khởi động phần mềm Console trên PC: ", "Mở Command Prompt hoặc PowerShell tại thư mục host/ và khởi chạy ứng dụng:")
    
    add_console_block([
        "> cd rdm6300-picorv32-rom-data\\host",
        "> rdm6300_manager.exe",
        "Nhap cong COM noi voi Basys 3 FPGA (mac dinh: COM3): COM3",
        "Dang ket noi toi COM3 voi baudrate 9600 bps...",
        "[SUCCESS] Da ket noi thanh cong voi Basys 3 tren COM3!",
        "",
        "===============================================================",
        "     RDM6300 RFID - PICORV32 - BASYS 3 SPI FLASH MANAGER      ",
        "===============================================================",
        "  [1]  Ping Hardware (Kiem tra ket noi PicoRV32)",
        "  [2]  Input & Save New RFID Tag (Nhap 10 so in tren the de luu Flash & Export)",
        "  [3]  Check RFID Tag in Flash (Kiem tra the da co trong Flash chua)",
        "  [4]  Delete RFID Tag from Flash (Nhap 10 so in tren the de xoa khoi Flash)",
        "  [5]  Virtual Scan: By Decimal (Quet the ao: Nhap 10 so in tren the)",
        "  [6]  Virtual Scan: By Hex (Quet the ao: Nhap ma Hex 10 ky tu)",
        "  [7]  View Access Logs from Flash (Xem nhat ky quet the tu Flash 0x310000)",
        "  [8]  Export Access Logs to CSV (Xuat nhat ky quet the ra file CSV vao host/logs)",
        "  [9]  Erase Access Logs (Sao luu ra CSV truoc roi xoa nhat ky trong Flash)",
        "  [10] Erase Authorized Tags Sector (Xoa the da cap phep 0x300000)",
        "  [11] Get SoC Status (Xem trang thai LED, Flash, PicoRV32)",
        "  [12] Export RFID Tags to CSV (Xuat danh sach the ra file CSV vao host/rfids)",
        "  [13] Import RFID Tags from Latest CSV (Xoa Flash & Nap the tu file CSV gan nhat)",
        "  [0]  Exit (Thoat)",
        "---------------------------------------------------------------",
        "Lua chon cua ban [0-13]: "
    ])

    doc.add_page_break()

    # =============================================================
    # TRANG 8: KỊCH BẢN QUẸT THẺ THỰC TẾ
    # =============================================================
    add_h2("5.3. Kịch bản thực nghiệm quẹt thẻ thực tế và kết quả xác thực")
    add_p("Hệ thống đã trải qua quy trình kiểm thử toàn diện thông qua 4 kịch bản thực nghiệm điển hình:")

    add_h3("Kịch bản 1: Kiểm tra kết nối phần cứng (Ping Hardware)")
    add_p("Người dùng chọn phím [1]. Máy tính gửi ký tự 'P' xuống bo mạch. Lõi PicoRV32 nhận lệnh và phản hồi chuỗi 'PONG' cùng trạng thái thanh ghi:")
    add_console_block([
        "Lua chon cua ban [0-13]: 1",
        "-> Gui lenh 'P' (Ping)...",
        "[PHAN HOI] PONG:CPU_OK:TRAP=0:HEARTBEAT_ACTIVE"
    ])

    add_h3("Kịch bản 2: Đăng ký thẻ mới vào bộ nhớ Flash (Lưu trữ vĩnh viễn)")
    add_p("Người dùng chọn phím [2] và nhập 10 chữ số in dập nổi trên thẻ RFID thật (ví dụ thẻ: 0007508976). Phần mềm chuyển đổi thành mã Hex 0x007293F0 và gửi lệnh 'N' xuống SoC. PicoRV32 kích hoạt khối SPI Flash Controller phát lệnh Page Program ghi mã thẻ vào Flash sector 0x30_0000. Đèn LED[1] (Flash Busy) trên bo mạch chớp sáng trong 3 ms rồi tắt, thông báo ghi thành công:")
    add_console_block([
        "Lua chon cua ban [0-13]: 2",
        "Nhap 10 chu so in tren the RFID (vi du: 0007508976): 0007508976",
        "-> Da nhan dien the hop le:",
        "   + So in tren the        : 0007508976  (FC: 114, ID: 37872)",
        "   + Ma Hex (UID 10 ky tu) : 00007293F0",
        "-> Gui ma the 00007293F0 toi PicoRV32 de luu vao Flash...",
        "[THANH CONG] The moi 00007293F0 (0007508976) da duoc luu vao Flash Basys 3 tai Slot #0 (Dia chi: 0x300000)!",
        "-> Tu dong xuat danh sach the moi cap nhat ra file CSV: host/rfids/20260922_214510.csv"
    ])

    add_h3("Kịch bản 3: Quẹt thẻ thật trên module RFID RDM6300 (Access Control)")
    add_p("Đưa thẻ RFID 125 kHz (mã 0007508976) vào vùng cảm ứng của ăng-ten RDM6300. Quá trình xử lý diễn ra hoàn toàn tự động:")
    add_bullet("1. Tiếp nhận tín hiệu: ", "RDM6300 giải điều chế và truyền chuỗi 14 byte qua chân JA1 vào FPGA.")
    add_bullet("2. Giải mã & Đối chiếu Checksum: ", "Khối rdm6300_frame_decoder.v bắt đúng STX (0x02), giải mã 10 ký tự ASCII sang nhị phân, tính XOR 5 byte dữ liệu và so sánh với byte Checksum. Checksum hoàn toàn khớp!")
    add_bullet("3. Chốt dữ liệu & Báo hiệu trực quan: ", "Khối giải mã bật cờ tag_valid lên 1. Đèn LED[2] trên Basys 3 sáng rực báo hiệu thẻ hợp lệ, đồng thời màn hình 4 LED 7 đoạn trên bo mạch Basys 3 lập tức chuyển từ trạng thái FAIL sang hiển thị chữ PASS (P-A-S-S) trong 2.0 giây để người dùng nhận diện trực quan kết quả quẹt thẻ thành công.")
    add_bullet("4. CPU Tra cứu Flash & Xác thực: ", "PicoRV32 đọc mã thẻ từ thanh ghi RFID_DATA_REG, tự động kích hoạt SPI Flash Controller đọc bảng dữ liệu từ 0x30_0000 để đối chiếu. Tìm thấy thẻ tại Slot #0! CPU ghi nhận thẻ hợp lệ, điều khiển LED[15:8] hiển thị mã truy cập thành công và ghi một bản ghi nhật ký (Log) vào sector Flash 0x31_0000.")
    add_bullet("5. Hiển thị trên Host Console: ", "Màn hình máy tính hiển thị thông báo truy cập được cấp phép:")
    add_console_block([
        "===============================================================",
        "  [ACCESS GRANTED] >>> XAC THUC THANH CONG! <<<",
        "===============================================================",
        "  - The quet         : 0007508976 (FC: 114, ID: 37872) [UID: 00007293F0]",
        "  - Ket qua          : THE HOP LE (Khop Slot #0, Dia chi Flash 0x300000)",
        "  - Nhat ky Flash    : Da ghi vao Log Slot #0 (Dia chi Flash 0x310000)",
        "  - Trang thai LED   : LED[2]=1 (Tag Valid), LED[1]=0 (Flash Ready)",
        "==============================================================="
    ])

    add_h3("Kịch bản 4: Quẹt thẻ chưa đăng ký (Từ chối truy cập)")
    add_p("Khi quẹt một thẻ RFID lạ chưa được nạp vào Flash (ví dụ thẻ 0001234567 / UID 000012D687), FSM phần cứng vẫn kiểm tra XOR checksum hợp lệ, nhưng khi PicoRV32 tra cứu cơ sở dữ liệu trong Flash, không tìm thấy thẻ khớp. Hệ thống lập tức từ chối:")
    add_console_block([
        "===============================================================",
        "  [ACCESS DENIED] >>> TU CHOI TRUY CAP (THE KHONG HOP LE)! <<<",
        "===============================================================",
        "  - The quet         : 0001234567 (FC: 018, ID: 54919) [UID: 000012D687]",
        "  - Ket qua          : THE CHUA DANG KY trong co so du lieu Flash!",
        "  - Nhat ky Flash    : Da ghi vao Log Slot #1 (Canh bao the la)",
        "  - Trang thai LED   : LED[2]=1 (Nhan the), LED[7]=1 (Den canh bao)",
        "  - LED 7 doan       : Hien thi chu FAIL trong 2 giay roi tu dong tat",
        "==============================================================="
    ])

    add_p("Đánh giá kết quả kiểm chứng: Hệ thống vận hành cực kỳ tin cậy, không một lần bị treo (trap = 0). Tốc độ giải mã thẻ và tra cứu Flash diễn ra gần như tức thời (< 10 ms), đáp ứng hoàn hảo yêu cầu thực tế của một thiết bị Access Control công nghiệp.")

    doc.add_page_break()

    # =============================================================
    # TRANG 9: KẾT QUẢ VÀ THẢO LUẬN
    # =============================================================
    add_h1("6. Kết quả và thảo luận")
    add_p("Việc triển khai thành công cả bản demo thực nghiệm trên FPGA Basys 3 và luồng vật lý hoàn chỉnh trên ASIC SkyWater Sky130A khẳng định tính đúng đắn và hiệu quả vượt trội của phương pháp thiết kế vi mạch được đề xuất.")

    add_h2("6.1. Các quyết định thiết kế tối ưu hóa diện tích và công suất (PPA)")
    add_bullet("Đột phá từ kiến trúc Mask ROM 8KB tổ hợp: ", "Thay vì dùng SRAM thông thường cần tới 70,000 Flip-Flop, giải pháp chuyển toàn bộ firmware thành mạch giải mã MUX tổ hợp (rtl/mask_rom.v) tiêu tốn 0 DFFs. Quyết định này giúp giảm 87% số lượng Flip-Flop của toàn hệ thống (từ hơn 85,000 xuống 11,051 DFFs), thu nhỏ diện tích lõi xuống 1.63 mm², triệt tiêu tải trọng cây clock và là chìa khóa then chốt giúp loại bỏ hoàn toàn các lỗi vi phạm Antenna.")
    add_bullet("Phần cứng hóa bộ giải mã RDM6300 độc lập: ", "Mạch giải mã phần cứng tự động kiểm tra STX/ETX, chuyển đổi ASCII-to-Hex và đối chiếu XOR checksum chỉ trong 1 chu kỳ clock sau khi nhận đủ byte. CPU PicoRV32 hoàn toàn không phải tốn thời gian xử lý chuỗi ký tự hay chịu nguy cơ mất dữ liệu khi đang bận giao tiếp Flash SPI.")
    add_bullet("Tối ưu hóa Bus MMIO và Data SRAM 2KB: ", "Dung lượng SRAM 2KB được tính toán tối ưu vừa đủ cho ngăn xếp và mảng dữ liệu thẻ. Hỗ trợ ghi mặt nạ byte (mem_wstrb) giúp CPU thực thi các lệnh byte/half-word trực tiếp mà không cần mạch Read-Modify-Write cồng kềnh.")

    add_h2("6.2. Hạn chế của thiết kế hiện tại")
    add_bullet("Tính cố định của Mask ROM trên ASIC: ", "Mã chương trình được đúc cố định trên các lớp mặt nạ kim loại của chip ASIC. Sau khi sản xuất (Tapeout), firmware không thể nạp lại hay nâng cấp (khác với nền tảng FPGA).")
    add_bullet("Giao tiếp SPI Flash ở chế độ 1-bit Standard: ", "Tốc độ đọc/ghi Flash hiện tại bị giới hạn bởi chuẩn SPI 1-bit. Thiết kế có thể mở rộng lên chuẩn Quad-SPI (QSPI 4-bit) để tăng gấp 4 lần băng thông truyền dữ liệu.")

    doc.add_page_break()

    # =============================================================
    # TRANG 10: KẾT QUẢ KÝ DUYỆT ASIC (RUN THÀNH CÔNG VỚI OPENROAD.PNG)
    # =============================================================
    add_h1("7. Kết quả triển khai và ký duyệt ASIC (OpenLane 2 - SkyWater Sky130A)")
    add_p("Ở lượt chạy cuối cùng mang mã định danh RUN_2026-09-22_21-34-37 được thực thi với toàn bộ các tham số trong file config.json hiện tại, thiết kế vi mạch SoC rdm6300_picorv32_soc đã hoàn thành xuất sắc toàn bộ quy trình thiết kế vật lý và đạt ký duyệt toàn diện (Full Tapeout Sign-off Ready).")

    add_h2("7.1. Phân tích cấu hình config.json giúp đạt chuẩn tapeout")
    add_p("Sự thành công vượt bậc của lượt chạy này đến từ sự phối hợp tối ưu giữa các tham số vật lý trong config.json:")
    add_bullet("1. Giải tỏa mật độ diện tích (FP_CORE_UTIL = 30): ", "Việc thiết lập mật độ sử dụng lõi khởi tạo ở mức 30% tạo ra không gian đệm rộng rãi (routing whitespace), giúp bộ định tuyến TritonRoute thoải mái chọn đường đi mà không bị nghẽn (congestion), đồng thời dành đủ vị trí chèn các tế bào diode bảo vệ.")
    add_bullet("2. Chèn Diode dự phòng nâng cao (RUN_HEURISTIC_DIODE_INSERTION = true & THRESHOLD = 65): ", "Thuật toán phỏng đoán tự động phân tích các đường bus tín hiệu dài từ PicoRV32 ra ngoại vi và chèn ngay 66 cell diode khuếch tán (sky130_fd_sc_hd__diode_2) tại các ngõ vào có nguy cơ tích tụ điện tích cao trước khi bước vào định tuyến chi tiết.")
    add_bullet("3. Tái phân bổ lớp kim loại định tuyến (GRT_LAYER_ADJUSTMENTS = [0.99, 0.65, 0.30, 0, 0, 0]): ", "Tham số này giảm tải định tuyến trên các lớp kim loại mỏng met1 và met2, cưỡng bức các đường bus dài chạy trên các lớp kim loại cấp cao met3, met4 và met5 – nơi có diện tích mặt cắt lớn và tỷ số antenna thấp hơn.")
    add_bullet("4. Khắc phục Antenna sau định tuyến (RUN_ANTENNA_REPAIR = true & DIODE_ON_PORTS = \"in\"): ", "Toàn bộ 31 chân cổng I/O đầu vào được gắn kết diode bảo vệ, triệt tiêu nguy cơ phóng điện plasma từ các pad kết nối ngoài.")

    add_h2("7.2. Bố trí layout vật lý và trực quan hóa trên OpenROAD")
    add_p("Hình ảnh bản vẽ layout vật lý sau bước hoàn thiện định tuyến chi tiết (Detailed Routing) và chèn diode bảo vệ được hiển thị trực tiếp trên giao diện công cụ OpenROAD (OpenInOpenROAD resolved.json), thể hiện tại Hình 3.")

    # Chèn Hình 3: openroad.png theo yêu cầu người dùng
    openroad_path = os.path.join(cur_dir, "openroad.png")
    if os.path.exists(openroad_path):
        p_img3 = doc.add_paragraph()
        p_img3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img3.paragraph_format.space_before = Pt(4)
        p_img3.paragraph_format.space_after = Pt(2)
        p_img3.paragraph_format.keep_with_next = True
        run_img3 = p_img3.add_run()
        run_img3.add_picture(openroad_path, width=Inches(5.2))
        add_caption("Hình 3. Giao diện trực quan hóa layout vật lý chip ASIC trên công cụ OpenROAD (SkyWater Sky130A)")

    add_h2("7.3. Kết quả sign-off toàn diện của run thành công (DRC, LVS, antenna clean)")
    add_p("File báo cáo chế tạo manufacturability.rpt tại thư mục run chính thức xác nhận hệ thống đã vượt qua tuyệt đối 100% các bài kiểm tra ký duyệt vật lý:")
    add_bullet("* Antenna: Passed ✅ — ", "Không có bất kỳ vi phạm tỷ số Antenna nào (antenna__violating__nets = 0, antenna__violating__pins = 0).")
    add_bullet("* Magic DRC: Passed ✅ — ", "0 lỗi vi phạm quy tắc thiết kế hình học (magic__drc_error__count = 0).")
    add_bullet("* KLayout DRC: Passed ✅ — ", "0 lỗi vi phạm trên bộ kiểm tra hình học độc lập KLayout (klayout__drc_error__count = 0).")
    add_bullet("* Netgen LVS: Passed ✅ — ", "Netlist trích xuất từ layout GDSII hoàn toàn trùng khớp với Netlist sơ đồ nguyên lý (design__lvs_error__count = 0, không có thiết bị hay đường dây nào sai lệch).")

    # Bảng 2 (renumbered): Thông số Sign-off ASIC
    t2 = doc.add_table(rows=13, cols=3)
    t2_headers = ["Thông số vật lý / Ký duyệt (Metric)", "Giá trị đạt được", "Tiêu chuẩn / Đánh giá kiểm tra"]
    t2_data = [
        ["Tiến trình công nghệ (Process)", "SkyWater 130nm (sky130_fd_sc_hd)", "Tiến trình CMOS nguồn mở chuẩn công nghiệp"],
        ["Kích thước Khuôn Die (Die Dimensions)", "1287.265 µm x 1297.985 µm", "Diện tích Die = 1.670 mm² (1,670,850 µm²)"],
        ["Kích thước Vùng Lõi (Core Dimensions)", "1281.560 µm x 1286.560 µm", "Diện tích Core = 1.628 mm² (1,627,820 µm²)"],
        ["Tổng số tế bào chuẩn (Standard Cells)", "130,460 cells", "Gồm logic, buffers, tap/endcap và fill cells"],
        ["Mật độ sử dụng tế bào (Cell Utilization)", "49.64% (0.4964)", "Mật độ vàng tối ưu định tuyến và tản nhiệt"],
        ["Số cổng kết nối ngoại vi (I/O Pins)", "31 pins", "Sắp xếp cân đối trên 4 cạnh die (pin_order.cfg)"],
        ["Lỗi quy tắc Antenna (Antenna Violations)", "0 LỖI (Passed ✅)", "0 violating nets, 0 violating pins"],
        ["Kiểm tra DRC (Magic & KLayout)", "0 LỖI (Passed ✅)", "Hoàn toàn sạch lỗi hình học và khoảng cách vật lý"],
        ["Kiểm tra đối chiếu Layout - Sơ đồ (Netgen LVS)", "PASSED ✅", "Netlists match completely, 0 unmatched devices/nets"],
        ["Định thời Setup Slack xấu nhất (WNS)", "WNS = +3.632 ns (Passed ✅)", "Đo tại góc xấu nhất max_ss_100C_1v60 (TNS = 0.00 ns)"],
        ["Định thời Hold Slack xấu nhất (WHS)", "WHS = +0.075 ns (Passed ✅)", "Đo tại góc xấu nhất max_ss_100C_1v60 (THS = 0.00 ns)"],
        ["Tần số xung nhịp hoạt động (Clock Frequency)", "40 MHz (Fmax đạt ~46.8 MHz)", "Chu kỳ clock 25.0 ns, thỏa mãn cả 9 corners"],
    ]
    for c_idx, h_text in enumerate(t2_headers):
        t2.cell(0, c_idx).paragraphs[0].text = h_text
    for r_idx, row_vals in enumerate(t2_data):
        for c_idx, val in enumerate(row_vals):
            t2.cell(r_idx + 1, c_idx).paragraphs[0].text = val
    col_w2 = [Inches(2.5), Inches(1.8), Inches(1.97)]
    col_a2 = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    style_table(t2, col_w2, col_a2)
    add_caption("Bảng 2. Bảng tổng hợp các thông số ký duyệt (Signoff Metrics) của chip ASIC Sky130A")

    doc.add_page_break()

    # =============================================================
    # TRANG 11: STA 9 CORNERS & CÔNG SUẤT
    # =============================================================
    add_h2("7.4. Phân tích định thời tĩnh STA đa góc đo (9 corners) và công suất tiêu thụ")
    add_p("Phân tích định thời tĩnh Post-PnR bằng OpenROAD (summary.rpt) xác nhận rằng toàn bộ hệ thống đạt yêu cầu định thời (Timing Closure) trên cả 9 góc đo công nghệ khắc nghiệt nhất (gồm tổ hợp nhiệt độ từ -40°C đến 100°C và điện áp từ 1.60V đến 1.95V). Chi tiết được trình bày trong Bảng 3.")

    # Bảng 3 (renumbered): STA Summary 9 Corners
    t3 = doc.add_table(rows=10, cols=5)
    t3_headers = ["Góc đo công nghệ (Corner)", "Setup WNS (ns)", "Setup Vio", "Hold WHS (ns)", "Hold Vio"]
    t3_data = [
        ["nom_tt_025C_1v80 (Điển hình)", "+11.325 ns", "0", "+0.315 ns", "0"],
        ["nom_ss_100C_1v60 (Chậm - Nhiệt độ cao)", "+3.790 ns", "0", "+0.275 ns", "0"],
        ["nom_ff_n40C_1v95 (Nhanh - Nhiệt độ âm)", "+12.875 ns", "0", "+0.109 ns", "0"],
        ["min_tt_025C_1v80", "+11.522 ns", "0", "+0.312 ns", "0"],
        ["min_ss_100C_1v60", "+3.937 ns", "0", "+0.485 ns", "0"],
        ["min_ff_n40C_1v95", "+13.008 ns", "0", "+0.107 ns", "0"],
        ["max_tt_025C_1v80", "+11.151 ns", "0", "+0.320 ns", "0"],
        ["max_ss_100C_1v60 (Góc xấu nhất)", "+3.632 ns", "0", "+0.075 ns", "0"],
        ["max_ff_n40C_1v95", "+12.743 ns", "0", "+0.111 ns", "0"],
    ]
    for c_idx, h_text in enumerate(t3_headers):
        t3.cell(0, c_idx).paragraphs[0].text = h_text
    for r_idx, row_vals in enumerate(t3_data):
        for c_idx, val in enumerate(row_vals):
            t3.cell(r_idx + 1, c_idx).paragraphs[0].text = val
    col_w3 = [Inches(2.5), Inches(1.1), Inches(0.8), Inches(1.1), Inches(0.77)]
    col_a3 = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.CENTER]
    style_table(t3, col_w3, col_a3)
    add_caption("Bảng 3. Báo cáo phân tích định thời tĩnh STA qua 9 góc đo công nghệ trên OpenROAD")

    add_p("Về công suất tiêu thụ, công cụ phân tích công suất ghi nhận tổng công suất tiêu thụ của chip ASIC ở điện áp danh định 1.8V là 0.0717 W (71.7 mW), trong đó công suất chuyển mạch nội bộ là 42.0 mW, công suất chuyển mạch đường dây là 29.7 mW và công suất rò rỉ tĩnh cực nhỏ chỉ 0.88 µW. Độ sụt áp trên lưới nguồn (Worst IR Drop) chỉ đạt 0.000766 V (< 0.05% điện áp cấp), chứng tỏ lưới nguồn PDN cực kỳ vững chắc.")

    add_h2("7.5. Các định hướng phát triển tiếp theo")
    add_bullet("Tích hợp SRAM Compiler cứng (OpenRAM): ", "Ứng dụng OpenRAM để biên dịch Data SRAM thành macro cứng chuyên dụng, giúp thu gọn thêm 20-30% diện tích khuôn die.")
    add_bullet("Nâng cấp chuẩn SPI Flash lên Quad-SPI: ", "Thiết kế bộ điều khiển QSPI 4-bit nhằm nâng cao gấp 4 lần thông lượng đọc thẻ từ Flash.")
    add_bullet("Mã hóa bảo mật phần cứng: ", "Tích hợp thêm khối mã hóa nhẹ (Lightweight Crypto) như AES-128 để mã hóa dữ liệu thẻ trước khi lưu vào Flash.")

    doc.add_page_break()

    # =============================================================
    # TRANG 12: KẾT LUẬN
    # =============================================================
    add_h1("8. Kết luận")
    add_p("Đồ án đã nghiên cứu, thiết kế và hiện thực thành công trọn vẹn Hệ thống trên Vi mạch (SoC) mang tên \"Thiết kế hệ thống quét và xử lý dữ liệu thẻ RFID tích hợp CPU RISC-V PicoRV32 quản lý dữ liệu trên Flash\" trên tiến trình bán dẫn SkyWater Sky130A sử dụng bộ công cụ tự động hóa OpenLane 2, song song với việc kiểm chứng thực nghiệm chức năng trên bo mạch FPGA Digilent Basys 3.")
    add_p("Hệ thống giải quyết triệt để nhu cầu thực tế về một thiết bị kiểm soát ra vào vận hành độc lập (Offline), hoàn toàn không cần kết nối Internet, đảm bảo tính bảo mật và liên tục. Việc lựa chọn bộ nhớ bất biến Non-Volatile SPI Flash là quyết định kiến trúc đúng đắn, cho phép lưu trữ cơ sở dữ liệu thẻ và nhật ký truy cập bền vững qua nhiều thập kỷ mà không cần nguồn pin phụ.")
    add_p("Trên nền tảng demo FPGA Basys 3, hệ thống đã chứng minh độ ổn định và tính khả thi thực tiễn cao: Khối giải mã phần cứng RDM6300 tự động nhận diện và tính toán XOR Checksum chuẩn xác 100% từ thẻ RFID 125 kHz thực tế, giải phóng hoàn toàn thời gian tính toán cho CPU PicoRV32. Phần mềm quản lý Host Console trên máy tính giao tiếp mượt mà qua cổng USB-UART, thực hiện hoàn hảo các tác vụ đăng ký thẻ, lưu trữ Flash, đọc tra cứu và kiểm soát ra vào thời gian thực.")
    add_p("Trên nền tảng ASIC SkyWater Sky130A, với file cấu hình config.json tối ưu hiện tại, lượt chạy cuối cùng RUN_2026-09-22_21-34-37 đã đạt ký duyệt toàn diện (Tapeout Sign-off Ready): Đạt chuẩn tuyệt đối 0 Antenna violations, 0 Magic DRC errors, 0 KLayout DRC errors, Netgen LVS Clean và thỏa mãn định thời tĩnh Setup/Hold trên cả 9 góc đo công nghệ. Bản vẽ layout GDSII hoàn chỉnh có diện tích 1.67 mm² và công suất 71.7 mW, khẳng định sự thành công rực rỡ của đề tài từ ý tưởng lý thuyết đến bản vẽ sản xuất vi mạch thương mại.")

    # -------------------------------------------------------------
    # Save Document (Both original and v2)
    # -------------------------------------------------------------
    out_docx_path = os.path.join(cur_dir, "Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.docx")
    alt_docx_path = os.path.join(cur_dir, "Bao_Cao_Do_An_RDM6300_PicoRV32_SoC_v2.docx")
    
    doc.save(alt_docx_path)
    print(f"Updated report saved successfully at: {alt_docx_path}")
    
    try:
        doc.save(out_docx_path)
        print(f"Primary report also updated successfully at: {out_docx_path}")
    except PermissionError:
        print(f"Note: {out_docx_path} is currently locked by Word. Available at {alt_docx_path}.")

if __name__ == "__main__":
    create_report()
