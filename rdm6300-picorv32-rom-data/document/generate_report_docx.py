# -*- coding: utf-8 -*-
"""
Script to generate the refined, comprehensive academic and technical project report in DOCX format:
"BÁO CÁO ĐỒ ÁN THIẾT KẾ VI MẠCH SỐ: THIẾT KẾ HỆ THỐNG QUÉT VÀ XỬ LÝ DỮ LIỆU THẺ RFID
TÍCH HỢP CPU RISC-V PICORV32 QUẢN LÝ DỮ LIỆU TRÊN FLASH"

Key Specifications:
- Core Objective: ASIC Design of an RFID Card Data Processing SoC integrating RISC-V PicoRV32 and SPI Flash.
- Basys 3 FPGA Role: Hardware Prototype & Real-time Verification Demo Platform.
- Step-by-Step Design Methodology included as requested:
  1. Hardware & Software Resource Selection (RDM6300, Basys 3 demo, Vivado, OpenLane, GCC, Host C console).
  2. Software-first Firmware Design (Command set, Flash sectors 48 & 49, card validation algorithms).
  3. Hardware CPU & Memory Execution Subsystem (PicoRV32 RV32I, 1KB Data SRAM, start.s).
  4. Flash Memory Controller (spimemio.v / Read, Page Program, Sector Erase, WIP polling).
  5. Peripherals: Hardware RDM6300 frame decoder with 2-FF sync & Host UART with FIFO buffers.
  6. Top-level SoC Integration (rdm6300_picorv32_soc.v) and MMIO address decoder.
  7. Host PC Console Software in C (host/main.c) with 13 functions.
  8. Experimental Demo Verification on Basys 3.
  9. ASIC Physical Design & Sign-off on OpenLane 2 (SkyWater 130nm).
- High-Resolution Image Embeds:
  - Fig 1: fig1_block_diagram.png (Overall SoC Architecture)
  - Fig 2: fig2_rdm6300_subsystem.png (RDM6300 Hardware Pipeline)
  - Fig 3: Openroad_1.png (OpenROAD Physical Layout GUI)
  - Fig 4: AntennaLvsDrc.png (ReportManufacturability: Antenna, LVS, DRC Passed)
- Sign-off Verification Data from run RUN_2026-09-27_21-51-11:
  - LVS Clean: 57,544 devices, 50,028 nets match uniquely (0 errors)
  - Magic DRC: 0 errors
  - KLayout DRC: 0 errors
  - Antenna: 0 net violations, 0 pin violations
  - Timing: MET TIMING across all 9 PVT corners (No setup violations, No hold violations)
  - IR Drop: Worst-case 0.04%
"""

import os
import sys
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
    
    # Blank header/footer for clean academic submission
    header = section.header
    for p in header.paragraphs:
        p.text = ""
    footer = section.footer
    for p in footer.paragraphs:
        p.text = ""
        
    BLACK = RGBColor(0, 0, 0)
    DARK_GRAY = RGBColor(70, 70, 70)
    
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
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        set_font(r, size=13.5, bold=True, color=BLACK)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(9)
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
    parent_dir = os.path.dirname(cur_dir)

    # =============================================================
    # TRANG 1: TRANG BÌA (COVER PAGE)
    # =============================================================
    add_p("", space_before=45)
    p_title1 = add_p("BÁO CÁO ĐỒ ÁN THIẾT KẾ VI MẠCH SỐ", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=16)
    set_font(p_title1.runs[0], size=16, bold=True, color=BLACK)

    p_title2 = add_p("THIẾT KẾ HỆ THỐNG QUÉT VÀ XỬ LÝ DỮ LIỆU THẺ RFID TÍCH HỢP CPU RISC-V PICORV32 QUẢN LÝ DỮ LIỆU TRÊN FLASH", 
                     align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18, line_spacing=1.25)
    set_font(p_title2.runs[0], size=14.5, bold=True, color=BLACK)

    p_sub = add_p("Thiết kế vi mạch số ASIC trên tiến trình SkyWater 130nm (OpenLane 2) — Kiểm chứng thực nghiệm phần cứng trên bo mạch Demo FPGA Basys 3", 
                  align=WD_ALIGN_PARAGRAPH.CENTER, space_after=80)
    set_font(p_sub.runs[0], size=11.5, italic=True, color=DARK_GRAY)

    p_group = add_p("Nhóm thực hiện: [Điền tên nhóm]\nThành viên thực hiện: [Họ và tên sinh viên]\nGiảng viên hướng dẫn: [Điền tên GVHD]",
                    align=WD_ALIGN_PARAGRAPH.CENTER, space_after=100, line_spacing=1.35)
    for r in p_group.runs:
        set_font(r, size=11, bold=False, color=BLACK)

    p_ref = add_p("Tài liệu tham chiếu dự án: Repository rdm6300-picorv32-rom-data; cấu hình vật lý config.json; báo cáo ký duyệt Sign-off Antenna / DRC / LVS / STA (OpenLane 2 - SkyWater Sky130A, run RUN_2026-09-27_21-51-11) và kết quả đo đạc thực nghiệm trên nền tảng demo FPGA Basys 3",
                  align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0, line_spacing=1.15)
    set_font(p_ref.runs[0], size=9.5, italic=True, color=DARK_GRAY)

    doc.add_page_break()

    # =============================================================
    # TRANG 2: MỤC LỤC CHUẨN XÁC VỚI TAB STOP VÀ DOT LEADER
    # =============================================================
    add_h1("Mục lục")
    
    toc_items = [
        ("1. Giới thiệu và đặt vấn đề", "3", True, 0),
        ("1.1. Bối cảnh công nghệ và tính cấp thiết", "3", False, 0.2),
        ("1.2. Định hướng sản phẩm: thiết bị kiểm soát ra vào độc lập (offline)", "3", False, 0.2),
        ("1.3. Lý do lựa chọn bộ nhớ bất biến non-volatile SPI flash", "3", False, 0.2),
        ("1.4. Mục tiêu nghiên cứu và phương pháp tiếp cận", "3", False, 0.2),
        ("2. Cơ sở lý thuyết và các công nghệ cốt lõi", "4", True, 0),
        ("2.1. Kiến trúc tập lệnh mở RISC-V RV32I và lõi PicoRV32", "4", False, 0.2),
        ("2.2. Giao thức thu nhận định danh thẻ RFID 125 kHz và module RDM6300", "4", False, 0.2),
        ("2.3. Chuẩn giao tiếp bộ nhớ SPI Flash và giải pháp nguyên thủy STARTUPE2", "4", False, 0.2),
        ("3. Quy trình thiết kế hệ thống tuần tự từng bước", "5", True, 0),
        ("3.1. Bước 1: Lựa chọn tài nguyên phần cứng (RDM6300, Basys 3) và phần mềm", "5", False, 0.2),
        ("3.2. Bước 2: Thiết kế firmware và định nghĩa giao thức giao tiếp trước", "5", False, 0.2),
        ("3.3. Bước 3: Thiết kế hệ thống xử lý phần cứng: nhân CPU PicoRV32 và 1KB Data SRAM", "6", False, 0.2),
        ("3.4. Bước 4: Thiết kế bộ điều khiển bộ nhớ ngoài SPI Flash Controller", "6", False, 0.2),
        ("3.5. Bước 5: Thiết kế ngoại vi giải mã phần cứng RDM6300 và UART Host có FIFO", "7", False, 0.2),
        ("3.6. Bước 6: Tích hợp hệ thống top-level SoC và giải mã địa chỉ MMIO", "9", False, 0.2),
        ("3.7. Bước 7: Thiết kế phần mềm host console C trên máy tính", "10", False, 0.2),
        ("4. Demo chức năng và kiểm chứng thực nghiệm trên FPGA Basys 3", "11", True, 0),
        ("4.1. Vai trò của bo mạch FPGA Basys 3: nền tảng demo và tạo mẫu phần cứng", "11", False, 0.2),
        ("4.2. Thiết lập kết nối phần cứng và cấu hình chân I/O", "11", False, 0.2),
        ("4.3. Các kịch bản thực nghiệm quẹt thẻ thực tế và kết quả xác thực", "12", False, 0.2),
        ("5. Thiết kế vật lý và kết quả ký duyệt ASIC (OpenLane 2 - SkyWater Sky130A)", "13", True, 0),
        ("5.1. Phân tích thiết lập cấu hình vật lý trong config.json", "13", False, 0.2),
        ("5.2. Trực quan hóa layout vật lý trên công cụ OpenROAD (Openroad_1.png)", "13", False, 0.2),
        ("5.3. Báo cáo ký duyệt chế tạo sign-off toàn diện (AntennaLvsDrc.png)", "14", False, 0.2),
        ("5.4. Đánh giá phân tích định thời tĩnh STA đa góc đo (9 corners) và MET TIMING", "15", False, 0.2),
        ("5.5. Phân tích lưới nguồn PDN và kiểm tra sụt áp (IR drop analysis)", "15", False, 0.2),
        ("6. Thảo luận và đánh giá tối ưu hóa PPA", "16", True, 0),
        ("6.1. Hiệu quả tối ưu hóa diện tích, công suất và hiệu năng", "16", False, 0.2),
        ("6.2. Hạn chế và các định hướng phát triển tiếp theo", "16", False, 0.2),
        ("7. Kết luận", "17", True, 0),
    ]
    
    for title, pg, is_main, indent in toc_items:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(1.5)
        p_t.paragraph_format.space_after = Pt(2.0)
        p_t.paragraph_format.line_spacing = 1.12
        if indent > 0:
            p_t.paragraph_format.left_indent = Inches(indent)
            
        p_t.paragraph_format.tab_stops.add_tab_stop(Inches(6.20), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        
        r1 = p_t.add_run(title)
        set_font(r1, size=10 if not is_main else 10.5, bold=is_main, color=BLACK)
        
        r2 = p_t.add_run(f"\t{pg}")
        set_font(r2, size=10 if not is_main else 10.5, bold=is_main, color=BLACK)

    doc.add_page_break()

    # =============================================================
    # TRANG 3: GIỚI THIỆU & ĐẶT VẤN ĐỀ
    # =============================================================
    add_h1("1. Giới thiệu và đặt vấn đề")
    add_h2("1.1. Bối cảnh công nghệ và tính cấp thiết")
    add_p("Hệ thống nhận dạng qua tần số vô tuyến (Radio-Frequency Identification – RFID) băng tần thấp 125 kHz (chuẩn EM4100 / TK4100) là giải pháp kinh điển, bền bỉ và có độ tin cậy cực cao trong các hệ thống an ninh kiểm soát vào ra (Access Control), thẻ chấm công và định danh nhân viên. Module đầu đọc RFID RDM6300 là một thiết bị phần cứng thông dụng, thực hiện giải điều chế sóng mang từ ăng-ten cảm ứng và truyền chuỗi dữ liệu 14 byte định dạng ASCII qua giao tiếp nối tiếp UART ở tốc độ 9600 bps.")
    add_p("Trong bối cảnh chuyển dịch số và nhu cầu an toàn thông tin ngày càng cao, việc tự chủ thiết kế các dòng vi mạch tích hợp chuyên dụng (ASIC / SoC) phục vụ xử lý và bảo mật dữ liệu định danh thẻ thông minh tại Việt Nam đang trở thành một nhiệm vụ công nghệ cấp bách, loại bỏ nguy cơ từ các cửa hậu (backdoor) phần cứng không rõ nguồn gốc.")

    add_h2("1.2. Định hướng sản phẩm: thiết bị kiểm soát ra vào độc lập (offline)")
    add_p("Trong xu hướng kết nối vạn vật (IoT), nhiều giải pháp kiểm soát ra vào phụ thuộc nặng nề vào hạ tầng mạng Internet và máy chủ đám mây (Cloud-based Access Control). Tuy nhiên, kiến trúc phụ thuộc Internet bộc lộ nhiều điểm nghẽn nghiêm trọng:")
    add_bullet("Tính sẵn sàng bị đe dọa: ", "Hệ thống sẽ bị ngưng trệ hoàn toàn khi đứt cáp quang, mất tín hiệu mạng viễn thông hoặc sự cố máy chủ dịch vụ.")
    add_bullet("Độ trễ truyền thông: ", "Việc đẩy từng gói tin quẹt thẻ lên Cloud rồi chờ máy chủ phản hồi tạo ra độ trễ từ vài trăm mili-giây đến vài giây, gây ùn tắc tại các cửa kiểm soát đông người.")
    add_bullet("Nguy cơ bảo mật và lộ lọt dữ liệu: ", "Dữ liệu định danh nhân sự truyền qua môi trường Internet công cộng tiềm ẩn nguy cơ bị nghe lén (sniffing), tấn công từ chối dịch vụ (DDoS) hoặc xâm nhập dữ liệu trái phép.")
    add_bullet("Khó khăn khi triển khai biệt lập: ", "Hoàn toàn không thể vận hành tại các địa bàn xa xôi, trạm gác biên cương, kho quân sự, hải đảo, hầm mỏ, công trường xây dựng hoặc các phòng lab nghiên cứu cô lập bảo mật cao.")
    add_p("Do đó, sản phẩm trọng tâm của đồ án được định hướng là một **Hệ thống Vi mạch SoC Xử lý Thẻ RFID Vận hành Độc lập (Standalone / Offline Access Controller)**. Hệ thống tự giải điều chế tín hiệu thẻ, tự đối chiếu danh mục cấp phép tại chỗ trong thời gian thực với độ trễ siêu nhỏ (< 10 µs), không phụ thuộc vào bất kỳ kết nối mạng ngoài nào.")

    add_h2("1.3. Lý do lựa chọn bộ nhớ bất biến non-volatile SPI flash")
    add_p("Khi vận hành độc lập không có kết nối Internet để lưu trữ dữ liệu trên máy chủ từ xa, bài toán cốt tử đặt ra là: Lưu trữ cơ sở dữ liệu danh mục thẻ người dùng (Whitelist) và nhật ký các lần quẹt thẻ (Access Logs) ở đâu để đảm bảo an toàn, không bị biến mất khi mất điện hoặc tắt máy? Bộ nhớ bất biến (Non-Volatile Memory – NVM), cụ thể là chip SPI NOR Flash (Spansion S25FL032P / Winbond W25Qxx), được lựa chọn vì các ưu điểm vượt trội:")
    add_bullet("1. Bảo toàn dữ liệu vĩnh viễn không cần pin nuôi: ", "Khác với RAM (mất sạch dữ liệu khi ngắt nguồn), bộ nhớ Flash lưu trữ thông tin bằng các cổng nổi (floating-gate), lưu giữ danh sách thẻ và lịch sử truy cập an toàn trên 20 năm.")
    add_bullet("2. Dung lượng lớn với chi phí thấp: ", "Dung lượng 32 Mbit (4 MBytes) cho phép lưu trữ tới hàng chục nghìn mã thẻ người dùng và hàng trăm nghìn bản ghi nhật ký truy cập với chi phí linh kiện cực rẻ.")
    add_bullet("3. Tối ưu hóa số lượng chân kết nối (Pin-count Efficiency): ", "Giao thức chuẩn SPI chỉ cần 4 đường tín hiệu (CS_N, SCK, MOSI, MISO), giúp tiết kiệm tối đa số chân I/O quý giá của chip vi mạch ASIC (chỉ tốn 31 chân kết nối ngoại vi).")
    add_bullet("4. Độ bền công nghiệp: ", "Chịu đựng hơn 100,000 chu kỳ ghi/xóa (P/E cycles), đáp ứng trọn vẹn tiêu chuẩn hoạt động 24/7 trong nhiều năm.")
    add_bullet("5. Bảo trì và trích xuất dữ liệu tiện lợi: ", "Khi cần bảo trì, người quản trị chỉ cần cắm máy tính xách tay qua cổng UART cục bộ để nạp thêm thẻ mới hoặc sao lưu toàn bộ nhật ký ra file CSV.")

    add_h2("1.4. Mục tiêu nghiên cứu và phương pháp tiếp cận")
    add_bullet("Mục tiêu cốt lõi: ", "Thiết kế hoàn chỉnh một Hệ thống trên Vi mạch (SoC) xử lý dữ liệu thẻ RFID RDM6300 tích hợp CPU RISC-V PicoRV32 và bộ điều khiển SPI Flash, hướng tới hiện thực hóa vi mạch bán dẫn ASIC trên công nghệ SkyWater 130nm.")
    add_bullet("Vai trò của Bo mạch FPGA Basys 3: ", "Basys 3 đóng vai trò là nền tảng tạo mẫu và demo phần cứng (FPGA Prototyping Platform) để kiểm chứng thực nghiệm tính đúng đắn thời gian thực của thiết kế với thẻ RFID thật, module RDM6300 thật, chip Flash thật và giao tiếp UART máy tính.")
    add_bullet("Mục tiêu ASIC Sign-off: ", "Thực thi toàn bộ quy trình thiết kế vật lý tự động hóa bằng OpenLane 2, đạt chuẩn xuất bản vẽ sản xuất (Tape-out Ready): 0 lỗi DRC, 0 lỗi LVS, 0 vi phạm Antenna và MET TIMING ở tần số 50 MHz trên cả 9 góc đo công nghệ.")

    doc.add_page_break()

    # =============================================================
    # TRANG 4: CƠ SỞ LÝ THUYẾT & CÔNG NGHỆ CỐT LÕI
    # =============================================================
    add_h1("2. Cơ sở lý thuyết và các công nghệ cốt lõi")
    add_h2("2.1. Kiến trúc tập lệnh mở RISC-V RV32I và lõi PicoRV32")
    add_p("RISC-V là kiến trúc tập lệnh tiêu chuẩn mở (Open ISA) được phát triển tại Đại học California, Berkeley. Khác với các kiến trúc thương mại đóng (như ARM hay x86) đòi hỏi chi phí bản quyền khổng lồ, RISC-V hoàn toàn miễn phí và tự do tùy biến. Tập lệnh cơ sở RV32I định nghĩa 32 thanh ghi đa dụng 32-bit (x0-x31) với 47 lệnh số nguyên cơ bản, cung cấp nền tảng tính toán mạnh mẽ và linh hoạt.")
    add_p("Lõi PicoRV32 (tác giả Claire Wolf) là một bộ vi xử lý RISC-V 32-bit mã nguồn mở được thiết kế theo triết lý tối ưu hóa diện tích silicon (Area-optimized). PicoRV32 không sử dụng đường ống lệnh dài (pipelining) phức tạp hay bộ đoán nhánh cồng kềnh, mà thực thi lệnh theo cơ chế vi mã (microcode state machine) với giao diện bộ nhớ bắt tay đơn giản (mem_valid / mem_ready). Nhờ đó, lõi chiếm diện tích cổng logic cực nhỏ, rất lý tưởng cho các vi mạch điều khiển nhúng chuyên dụng.")

    add_h2("2.2. Giao thức thu nhận định danh thẻ RFID 125 kHz và module RDM6300")
    add_p("Module RDM6300 nhận diện thẻ RFID 125 kHz thụ động (Passive Transponder). Khi thẻ đi vào từ trường của ăng-ten, cuộn cảm trong thẻ tự tạo ra năng lượng nuôi chip định danh và điều chế tín hiệu tải bằng mã Manchester. RDM6300 giải điều chế tín hiệu này và đóng gói thành một khung truyền UART chuẩn 14 byte:")
    add_bullet("Byte 0: ", "Ký tự mở đầu khung STX (Start of Text, mã ASCII 0x02).")
    add_bullet("Byte 1 đến Byte 10: ", "10 ký tự ASCII thể hiện 5 byte dữ liệu nhị phân (1 byte Version và 4 byte Số sê-ri thẻ).")
    add_bullet("Byte 11 đến Byte 12: ", "2 ký tự ASCII thể hiện byte Checksum kiểm tra toàn vẹn.")
    add_bullet("Byte 13: ", "Ký tự kết thúc khung ETX (End of Text, mã ASCII 0x03).")
    add_p("Thuật toán kiểm tra toàn vẹn yêu cầu thực hiện phép toán XOR từng byte giữa 5 byte dữ liệu và so khớp với byte Checksum nhận được: Checksum == Data[0] ^ Data[1] ^ Data[2] ^ Data[3] ^ Data[4]. Nếu trùng khớp, khung dữ liệu được xác nhận hợp lệ.")

    add_h2("2.3. Chuẩn giao tiếp bộ nhớ SPI Flash và giải pháp nguyên thủy STARTUPE2")
    add_p("Bộ nhớ SPI NOR Flash (như Spansion S25FL032P) sử dụng chuẩn giao tiếp nối tiếp 4 đường dây: CS_N (chọn chip), SCK (xung nhịp), MOSI (dữ liệu vào), MISO (dữ liệu ra). Flash được tổ chức thành các Sector 64KB và Page 256 bytes. Để ghi dữ liệu, hệ thống phải thực hiện chu trình: Gửi lệnh cho phép ghi WREN (0x06) -> Gửi lệnh Page Program (0x02) kèm địa chỉ 24-bit -> Truyền chuỗi byte dữ liệu -> Polling đọc thanh ghi trạng thái (0x05) kiểm tra bit WIP (Write-In-Progress) cho tới khi hoàn tất.")
    add_p("Một thách thức vật lý đặc thù trên FPGA Xilinx 7-Series (Artix-7 trên Basys 3) là chân xung nhịp CCLK nối tới chip Flash được chia sẻ với bộ điều khiển nạp bitstream cấu hình. Để mạch RTL có thể tự do phát xung nhịp SCK giao tiếp Flash sau khi chip đã khởi động xong, thiết kế phải sử dụng nguyên thủy phần cứng chuyên dụng `STARTUPE2` của Xilinx và đưa xung nhịp vào cổng `USRCCLKO`.")

    doc.add_page_break()

    # =============================================================
    # TRANG 5: QUY TRÌNH THIẾT KẾ TUẦN TỰ TỪNG BƯỚC
    # =============================================================
    add_h1("3. Quy trình thiết kế hệ thống tuần tự từng bước")
    add_p("Để hiện thực hóa một hệ thống vi mạch SoC phức tạp, phương pháp tiếp cận thiết kế từ trên xuống (Top-Down Engineering Methodology) được áp dụng chặt chẽ theo 7 bước tuần tự logic:")

    add_h2("3.1. Bước 1: Lựa chọn tài nguyên phần cứng (RDM6300, Basys 3) và phần mềm")
    add_p("Quyết định lựa chọn tài nguyên phần cứng và chuỗi công cụ phần mềm đóng vai trò quyết định đến tính khả thi và độ hoàn thiện của đề tài:")
    add_bullet("Module đọc thẻ RFID RDM6300: ", "Lựa chọn vì độ bền công nghiệp, hoạt động ở điện áp 5V/3.3V, ngõ ra UART 9600 bps dễ dàng tương thích với mức logic 3.3V của các chân FPGA PMOD.")
    add_bullet("Bo mạch FPGA Digilent Basys 3 (Artix-7 XC7A35T): ", "Được chọn làm NỀN TẢNG DEMO VÀ TẠO MẪU PHẦN CỨNG (Hardware Prototype Platform). Bo mạch tích hợp sẵn chip SPI Flash 32 Mbit, chip cầu nối USB-UART FTDI, 16 LED trạng thái và các cổng PMOD tiêu chuẩn, tạo môi trường thực nghiệm hoàn hảo để chứng minh mạch hoạt động thật trước khi chuyển sang ASIC.")
    add_bullet("Chuỗi công cụ Xilinx Vivado: ", "Sử dụng để tổng hợp RTL, gán chân ràng buộc vật lý (basys3_picorv32_rdm6300.xdc), tạo file bitstream và nạp kiểm thử thực nghiệm trên Basys 3.")
    add_bullet("Chuỗi công cụ vi mạch ASIC OpenLane 2 & SkyWater 130nm PDK: ", "Sử dụng để thực thi toàn bộ luồng tổng hợp vật lý từ Verilog RTL ra bản vẽ GDSII hoàn chỉnh cho nhà máy đúc vi mạch.")
    add_bullet("Trình biên dịch GNU RISC-V Toolchain (riscv32-unknown-elf-gcc): ", "Dùng để biên dịch mã nguồn C và tệp khởi động Assembly start.s thành mã máy nhị phân firmware.hex.")
    add_bullet("Phần mềm quản trị trên máy tính (Host PC Console): ", "Phát triển bằng ngôn ngữ C (host/main.c) sử dụng Win32 Serial API, đóng vai trò giao diện điều khiển trung tâm.")

    add_h2("3.2. Bước 2: Thiết kế firmware và định nghĩa giao thức giao tiếp trước")
    add_p("Áp dụng triết lý thiết kế hướng phần mềm trước (Software-first Architecture): Xác định các chức năng và giao thức phần mềm trước giúp định hình chính xác các thanh ghi ngoại vi và cấu trúc bus phần cứng cần thiết, tránh lãng phí diện tích mạch.")
    add_bullet("1. Quy hoạch cấu trúc lưu trữ trên SPI Flash: ", "Phân vùng bộ nhớ Flash thành các sector chuyên biệt:")
    add_bullet("   * Sector 48 (Địa chỉ 0x300000) - Danh mục thẻ hợp lệ: ", "Dung lượng 64KB chứa tối đa 4096 bản ghi thẻ. Mỗi bản ghi có kích thước 16 bytes: 4 bytes Magic Header (0x52464944 - 'RFID'), 4 bytes UID High, 4 bytes UID Low và 4 bytes cờ trạng thái.")
    add_bullet("   * Sector 49 (Địa chỉ 0x310000) - Nhật ký quẹt thẻ (Access Logs): ", "Chứa tối đa 512 bản ghi nhật ký. Mỗi bản ghi 16 bytes gồm: Magic kết quả (0x53554343 - 'SUCC' hoặc 0x4641494C - 'FAIL'), mã thẻ đã quẹt, thứ tự lượt quẹt và địa chỉ slot.")
    add_bullet("2. Định nghĩa tập lệnh UART giữa Host PC và SoC: ", "Giao thức dựa trên ký tự ASCII kết thúc bằng ký tự '\\n':")
    add_bullet("   * Lệnh 'P' (Ping): ", "Kiểm tra kết nối và trạng thái CPU PicoRV32 (phản hồi PONG:CPU_OK).")
    add_bullet("   * Lệnh 'N<UID>' (New Tag): ", "Lưu một mã thẻ mới vào vị trí trống (Slot) trong Flash Sector 48.")
    add_bullet("   * Lệnh 'C<UID>' (Check Tag): ", "Tra cứu xem mã thẻ đã tồn tại trong Flash hay chưa.")
    add_bullet("   * Lệnh 'D<UID>' (Delete Tag): ", "Xóa mã thẻ khỏi Flash và dọn dẹp danh mục.")
    add_bullet("   * Lệnh 'V<UID>' (Virtual Scan): ", "Mô phỏng quẹt thẻ ảo từ xa phục vụ kiểm thử hệ thống.")
    add_bullet("   * Lệnh 'L' (List Logs): ", "Đọc toàn bộ nhật ký quẹt thẻ lưu trong Flash Sector 49 truyền lên máy tính.")
    add_bullet("   * Lệnh 'X' (Erase Logs): ", "Tự động sao lưu nhật ký ra file CSV rồi xóa sạch Sector 49.")
    add_bullet("   * Lệnh 'E' (Erase All Tags): ", "Xóa trắng Sector 48 danh mục thẻ cấp phép.")
    add_bullet("   * Lệnh 'S' (Status): ", "Truy vấn trạng thái các ngoại vi và số lượng thẻ hiện có.")
    add_bullet("3. Viết các hàm chức năng C cốt lõi (firmware/main.c): ", "Hàm `execute_card_scan()` thực hiện tuần tự: Bóc tách mã thẻ từ thanh ghi phần cứng -> Gọi `find_tag_slot()` tra cứu trong Flash Sector 48 -> Nếu tìm thấy: Bật LED xanh báo hợp lệ, ghi log SUCC vào Sector 49, xuất thông báo 'ACCESS:GRANTED' lên UART; Nếu không tìm thấy: Bật cờ cảnh báo LED, ghi log FAIL vào Sector 49, xuất thông báo 'ACCESS:DENIED' lên UART.")

    doc.add_page_break()

    # =============================================================
    # TRANG 6: THIẾT KẾ PHẦN CỨNG CPU, SRAM & FLASH CONTROLLER
    # =============================================================
    add_h2("3.3. Bước 3: Thiết kế hệ thống xử lý phần cứng: nhân CPU PicoRV32 và 1KB Data SRAM")
    add_p("Sau khi có bản đặc tả chức năng firmware, khối xử lý trung tâm được hiện thực bằng ngôn ngữ Verilog RTL:")
    add_bullet("Nhân vi xử lý PicoRV32 (rtl/picorv32.v): ", "Được cấu hình hỗ trợ tập lệnh RV32I. Bus bộ nhớ giao tiếp qua các tín hiệu: mem_valid, mem_ready, mem_addr[31:0], mem_wdata[31:0], mem_wstrb[3:0], mem_rdata[31:0]. CPU khởi động trực tiếp tại địa chỉ 0x0025_0000 (PROGADDR_RESET) nằm trong vùng nhớ SPI Flash thông qua cơ chế thực thi tại chỗ XIP (eXecute In Place) của bộ điều khiển spimemio.")
    add_bullet("Bộ nhớ On-Chip 1KB Data SRAM (rtl/data_sram.v): ", "Mảng nhớ nội bộ dung lượng chính xác 1 KByte (256 words x 32-bit = 1024 bytes) ánh xạ dải địa chỉ 0x0000_0000 đến 0x0000_03FF. Mảng nhớ này đóng vai trò không gian dữ liệu đọc/ghi: lưu biến toàn cục (.data, .bss), đỉnh ngăn xếp Stack Pointer (sp = 0x0000_0400) và chứa đoạn mã hàm flashio_worker (thực thi từ RAM khi tạm ngắt XIP để bit-bang phát lệnh ghi/xóa chip Flash). Hỗ trợ mặt nạ byte ghi mem_wstrb[3:0] cho phép ghi chính xác từng byte đơn lẻ. Kích thước 1KB tối giản giúp tiết kiệm tối đa diện tích silicon trên chip ASIC và suy luận hoàn hảo thành khối Block RAM đồng bộ trên FPGA.")
    add_bullet("Mã khởi động Assembly (firmware/start.s) và Linker Script (firmware/sections.lds): ", "Thiết lập con trỏ ngăn xếp Stack Pointer (sp = 0x00000400), sao chép phần dữ liệu .data từ Flash vào Data SRAM, xóa trắng vùng nhớ biến chưa khởi tạo (.bss) về 0 trước khi gọi hàm main().")

    # Chèn Hình 1: Block diagram chính
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

    add_h2("3.4. Bước 4: Thiết kế bộ điều khiển bộ nhớ ngoài SPI Flash Controller")
    add_p("Khối điều khiển Flash (rtl/spimemio.v) là cầu nối giữa bus MMIO của CPU và chip Flash SPI ngoài:")
    add_bullet("Máy trạng thái FSM điều khiển SPI: ", "Tự động hóa hoàn toàn các giao thức nối tiếp: tạo xung nhịp Flash SCK, kích hoạt chân chọn chip Flash CS_N, đẩy địa chỉ và dữ liệu qua MOSI và lấy mẫu dữ liệu từ MISO.")
    add_bullet("Tập lệnh Flash phần cứng hỗ trợ: ", "Hỗ trợ lệnh Read Data (0x03), Page Program (0x02), Sector Erase 64KB (0xD8/0x20) và Read Status Register (0x05).")
    add_bullet("Cơ chế phần cứng tự động Polling cờ bận WIP: ", "Sau mỗi chu kỳ ghi trang hoặc xóa sector, khối điều khiển tự động gửi lệnh 0x05 kiểm tra bit 0 (WIP) của Flash. Khi chip Flash vẫn đang bận ghi vật lý, bit trạng thái REG_SPI_STATUS_BUSY giữ mức 1; khi hoàn tất, cờ tự hạ về 0, giải phóng hoàn toàn thời gian chờ đợi cho CPU.")

    doc.add_page_break()

    # =============================================================
    # TRANG 7: NGOẠI VI RDM6300, UART FIFO & TÍCH HỢP TOP SOC
    # =============================================================
    add_h2("3.5. Bước 5: Thiết kế ngoại vi giải mã phần cứng RDM6300 và UART Host có FIFO")
    add_p("Để đảm bảo hệ thống không bao giờ bị rơi rụng dữ liệu thẻ và không làm nghẽn bus xử lý, các ngoại vi giao tiếp được thiết kế độc lập và trang bị bộ đệm phần cứng:")
    add_bullet("1. Chuỗi giải mã phần cứng RDM6300 (Hình 2): ", "Bao gồm tầng khử bất ổn định 2-FF (sync_2ff.v), bộ thu UART 9600 baud (uart_rx.v) và máy trạng thái FSM giải mã khung (rdm6300_frame_decoder.v). FSM tự động lọc STX (0x02), thu thập 10 ký tự ASCII dữ liệu thẻ, chuyển đổi tổ hợp sang 5 byte Hex nhị phân, tính toán Checksum XOR song song trong phần cứng và đối chiếu với 2 byte Checksum nhận được. Nếu khớp, cờ card_valid bật lên 1 và chốt 40-bit UID vào thanh ghi REG_RFID_TAG_HI/LO.")
    add_bullet("2. Khối UART giao tiếp máy tính tích hợp FIFO (simpleuart_fifo.v): ", "Tích hợp 2 bộ đệm FIFO phần cứng độc lập (sync_fifo.v) cho cả chiều nhận RX và chiều phát TX. Bộ đệm FIFO giúp máy tính có thể truyền chuỗi lệnh tốc độ cao mà không làm tràn bộ đệm khi PicoRV32 đang bận thực hiện chu kỳ xóa/ghi Flash.")
    add_bullet("3. Khối GPIO điều khiển LED: ", "Ánh xạ địa chỉ 0x4000_0000 điều khiển 16 LED hiển thị trực quan các trạng thái nhịp tim hệ thống (Heartbeat), trạng thái bận Flash và kết quả xác thực thẻ.")

    doc.add_page_break()

    # =============================================================
    # TRANG 8: HÌNH 2 - SƠ ĐỒ KHỐI ĐƯỜNG ỐNG 5 GIAI ĐOẠN RDM6300 (DỌC)
    # =============================================================
    fig2_path = os.path.join(cur_dir, "fig2_rdm6300_subsystem.png")
    if os.path.exists(fig2_path):
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img2.paragraph_format.space_before = Pt(0)
        p_img2.paragraph_format.space_after = Pt(2)
        p_img2.paragraph_format.keep_with_next = True
        run_img2 = p_img2.add_run()
        run_img2.add_picture(fig2_path, width=Inches(5.35))
        add_caption("Hình 2. Sơ đồ khối chi tiết đường ống 5 giai đoạn thu nhận và giải mã phần cứng thẻ RFID RDM6300")

    doc.add_page_break()

    # =============================================================
    # TRANG 9: TÍCH HỢP TOP-LEVEL SOC VÀ BẢN ĐỒ BỘ NHỚ MMIO
    # =============================================================
    add_h2("3.6. Bước 6: Tích hợp hệ thống top-level SoC và giải mã địa chỉ MMIO")
    add_p("Tại tệp top-level rdm6300_picorv32_soc.v, toàn bộ CPU, bộ nhớ và các ngoại vi được kết nối thông qua bộ giải mã địa chỉ bus MMIO Address Decoder:")

    # Bảng 1: Memory Map
    t1 = doc.add_table(rows=10, cols=3)
    t1_headers = ["Dải địa chỉ (Hex)", "Ngoại vi / Chức năng", "Mô tả chi tiết và Phương thức truy xuất"]
    t1_data = [
        ["0x0000_0000 - 0x0000_03FF", "1KB Data SRAM (data_sram.v)", "Bộ nhớ đọc/ghi nội bộ (256x32-bit): Chứa .data, .bss, ngăn xếp (Stack với đỉnh 0x0000_0400) và hàm flashio_worker."],
        ["0x0010_0000 - 0x00FF_FFFF", "15MB Flash XIP (spimemio.v)", "Vùng mã lệnh thực thi trực tiếp từ SPI Flash (eXecute In Place). Reset vector đặt tại 0x0025_0000."],
        ["0x0200_0000", "SPIMEMIO Config & Bit-Bang", "Thanh ghi điều khiển trực tiếp các chân SPI Flash (dùng bởi flashio_worker để ghi/xóa Flash)."],
        ["0x1000_0000", "REG_RFID_STATUS", "Bit 0: Cờ card_valid (ghi 1 để xóa sau khi đọc); Bit 1: Checksum error."],
        ["0x1000_0004", "REG_RFID_TAG_HI", "Chứa 8-bit trên của mã thẻ RFID (Version byte)."],
        ["0x1000_0008", "REG_RFID_TAG_LO", "Chứa 32-bit dưới của mã thẻ RFID (Serial number)."],
        ["0x3000_0000", "Host UART Baud Divisor", "Thanh ghi chia tần số baud UART kết nối PC (Mặc định: 50MHz / 9600 = 5208)."],
        ["0x3000_0004", "Host UART Data RX/TX", "Ghi byte để phát lên máy tính; đọc byte máy tính gửi xuống (có đệm FIFO RX/TX)."],
        ["0x4000_0000", "GPIO / Status LEDs", "Thanh ghi điều khiển 16 LED trạng thái (LED 0 nhịp tim, LED 1 Flash Busy, LED 2 Tag Valid)."],
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
    # TRANG 8: PHẦN MỀM HOST CONSOLE TRÊN MÁY TÍNH
    # =============================================================
    add_h2("3.7. Bước 7: Thiết kế phần mềm host console C trên máy tính")
    add_p("Phần mềm quản trị trên máy tính (host/main.c) được viết hoàn toàn bằng ngôn ngữ C, biên dịch thành tệp thực thi độc lập kết nối trực tiếp với chip cầu nối FTDI USB-UART qua Win32 API. Ứng dụng cung cấp menu tương tác 13 chức năng chuyên nghiệp:")
    
    add_console_block([
        "===============================================================",
        "     RDM6300 RFID - PICORV32 - BASYS 3 SPI FLASH MANAGER      ",
        "===============================================================",
        "  [1]  Ping Hardware (Kiem tra ket noi PicoRV32)",
        "  [2]  Input & Save New RFID Tag (Nhap 10 so in tren the de luu Flash & Export)",
        "  [3]  Check RFID Tag in Flash (Kiem tra the da co trong Flash chua)",
        "  [4]  Delete RFID Tag from Flash (Nhap 10 so in tren the de xoa khoi Flash & Export CSV)",
        "  [5]  Virtual Scan: By Decimal (Quet the ao: Nhap 10 so in tren the)",
        "  [6]  Virtual Scan: By Hex (Quet the ao: Nhap ma Hex 10 ky tu)",
        "  [7]  View Access Logs from Flash (Xem nhat ky quet the tu Flash 0x310000)",
        "  [8]  Export Access Logs to CSV (Xuat nhat ky quet the ra file CSV vao host/logs)",
        "  [9]  Erase Access Logs (Sao luu ra CSV truoc roi xoa nhat ky trong Flash 0x310000)",
        "  [10] Erase Authorized Tags Sector (Xoa the da cap phep 0x300000)",
        "  [11] Get SoC Status (Xem trang thai LED, Flash, PicoRV32)",
        "  [12] Export RFID Tags to CSV (Xuat danh sach the ra file CSV vao host/rfids)",
        "  [13] Import RFID Tags from Latest CSV (Xoa Flash & Nap the tu file CSV gan nhat)",
        "  [0]  Exit (Thoat)",
        "---------------------------------------------------------------",
        "Lua chon cua ban [0-13]: "
    ])

    add_p("Điểm nhấn công nghệ của phần mềm Host Console:")
    add_bullet("Bộ phân tích định dạng thẻ thông minh (parse_card_input): ", "Cho phép người dùng nhập trực tiếp 10 chữ số in dập nổi trên mặt thẻ (ví dụ thẻ 0007508976), chuỗi chuẩn Wiegand (114,37872), hoặc mã Hex 10 ký tự (00007293F0). Phần mềm tự động quy đổi toán học chuẩn xác sang mã Hex 10 ký tự trước khi gửi xuống SoC.")
    add_bullet("Chức năng Quẹt thẻ ảo (Virtual Scan - Menu [5] và [6]): ", "Cho phép kiểm thử toàn bộ luồng xử lý của SoC, tra cứu cơ sở dữ liệu Flash và ghi nhật ký mà không cần quẹt thẻ vật lý trên đầu đọc RDM6300.")
    add_bullet("Tự động sao lưu và bảo vệ dữ liệu CSV: ", "Mỗi khi thêm/xóa thẻ hoặc xóa nhật ký, phần mềm tự động xuất bản sao lưu ra thư mục host/rfids/ và host/logs/ với dấu thời gian (Timestamp), ngăn chặn nguy cơ mất mát dữ liệu.")

    doc.add_page_break()

    # =============================================================
    # TRANG 9: DEMO THỰC NGHIỆM TRÊN FPGA BASYS 3
    # =============================================================
    add_h1("4. Demo chức năng và kiểm chứng thực nghiệm trên FPGA Basys 3")
    add_h2("4.1. Vai trò của bo mạch FPGA Basys 3: nền tảng demo và tạo mẫu phần cứng")
    add_p("Trong dự án này, mục tiêu tối thượng là thiết kế và chế tạo vi mạch tích hợp chuyên dụng (ASIC). Tuy nhiên, trước khi gửi bản vẽ đi tape-out ở nhà máy bán dẫn (vốn tốn kém hàng chục nghìn USD và mất từ 3 đến 6 tháng chế tạo), việc tạo mẫu phần cứng (Hardware Prototyping) trên FPGA là bước bắt buộc trong công nghiệp.")
    add_p("Bo mạch Digilent Basys 3 (trang bị chip FPGA Xilinx Artix-7 XC7A35T) được sử dụng làm NỀN TẢNG DEMO THỰC TẾ. Nhờ đó, nhóm nghiên cứu có thể:")
    add_bullet("1. ", "Kiểm chứng sự phối hợp nhịp nhàng giữa lõi CPU PicoRV32 với thẻ RFID thật và đầu đọc RDM6300 thật trong môi trường vật lý có nhiễu sóng cao tần.")
    add_bullet("2. ", "Xác thực chu trình ghi/đọc/xóa vật lý trên chip SPI Flash Spansion S25FL032P thật ở tốc độ cao.")
    add_bullet("3. ", "Đo đạc độ trễ phản hồi thực tế và kiểm tra độ ổn định của firmware trong nhiều giờ vận hành liên tục.")

    add_h2("4.2. Thiết lập kết nối phần cứng và cấu hình chân I/O")
    add_p("Hệ thống demo được kết nối vật lý tinh gọn và khoa học:")
    add_bullet("Cổng PMOD JA: ", "Chân TX của RDM6300 kết nối chân JA1 (chân J1 của FPGA). Chân nguồn 5V và GND lấy trực tiếp từ cổng PMOD của Basys 3.")
    add_bullet("Cổng Micro-USB: ", "Kết nối máy tính vừa cấp nguồn 5V cho toàn bộ hệ thống vừa mở cổng ảo COM ở tốc độ 9600 bps.")
    add_bullet("Nguyên thủy STARTUPE2: ", "Trong tệp fpga/rtl/top_basys3_picorv32_rdm6300.v, xung nhịp Flash SCK được đưa vào chân USRCCLKO của nguyên thủy STARTUPE2 để điều khiển chân CCLK nối tới chip Flash.")
    add_bullet("Hệ thống LED hiển thị: ", "LED[0] nhấp nháy 1 Hz (Heartbeat CPU đang chạy bình thường); LED[1] sáng khi chip Flash đang bận ghi/xóa; LED[2] sáng khi đầu đọc nhận được mã thẻ hợp lệ.")

    doc.add_page_break()

    # =============================================================
    # TRANG 10: KỊCH BẢN QUẸT THẺ THỰC TẾ
    # =============================================================
    add_h2("4.3. Các kịch bản thực nghiệm quẹt thẻ thực tế và kết quả xác thực")
    add_p("Hệ thống demo trên bo mạch Basys 3 đã vượt qua 100% các bài kiểm thử thực nghiệm:")

    add_h3("Kịch bản 1: Kiểm tra kết nối phần cứng (Ping Hardware)")
    add_p("Người dùng chọn phím [1]. Máy tính gửi lệnh 'P' xuống SoC qua UART. PicoRV32 nhận lệnh và phản hồi ngay lập tức:")
    add_console_block([
        "Lua chon cua ban [0-13]: 1",
        "-> Gui lenh 'P' (Ping)...",
        "[PHAN HOI] PONG:CPU_OK:TRAP=0:HEARTBEAT_ACTIVE"
    ])

    add_h3("Kịch bản 2: Đăng ký thẻ mới vào bộ nhớ Flash")
    add_p("Người dùng chọn phím [2] và nhập 10 chữ số in trên thẻ RFID thật (ví dụ: 0007508976). Phần mềm quy đổi thành mã Hex 00007293F0 và gửi lệnh 'N' xuống SoC. PicoRV32 kích hoạt lệnh Page Program ghi vào Flash Sector 48 (0x300000). Đèn LED[1] trên Basys 3 nháy sáng 3 ms rồi tắt, thông báo ghi thành công:")
    add_console_block([
        "Lua chon cua ban [0-13]: 2",
        "Nhap 10 chu so in tren the RFID (vi du: 0007508976): 0007508976",
        "-> Da nhan dien the hop le: 0007508976 (FC: 114, ID: 37872) [UID: 00007293F0]",
        "-> Gui ma the 00007293F0 toi PicoRV32 de luu vao Flash...",
        "[THANH CONG] The moi 00007293F0 (0007508976) da duoc luu vao Flash Basys 3 tai Slot #0 (Dia chi: 0x300000)!",
        "-> Tu dong xuat danh sach the moi cap nhat ra file CSV vao host/rfids/..."
    ])

    add_h3("Kịch bản 3: Quẹt thẻ thật trên module RFID RDM6300 (Access Granted)")
    add_p("Đưa thẻ RFID 125 kHz (mã 0007508976) lại gần ăng-ten RDM6300. Khối giải mã phần cứng rdm6300_frame_decoder.v bóc tách khung, kiểm tra XOR Checksum chính xác 100% và bật cờ card_valid. CPU PicoRV32 đọc mã thẻ, tra cứu Flash Sector 48 và tìm thấy thẻ tại Slot #0. Hệ thống bật LED xanh và hiển thị xác thực thành công:")
    add_console_block([
        "===============================================================",
        "  [ACCESS GRANTED] >>> XAC THUC THANH CONG! <<<",
        "===============================================================",
        "  - The quet         : 0007508976 (FC: 114, ID: 37872)  [UID: 00007293F0]",
        "  - Ket qua          : THE HOP LE (Khop Slot #0, Dia chi 0x300000)",
        "  - Nhat ky Flash    : Da ghi vao Log Slot #0 (Dia chi 0x310000)",
        "==============================================================="
    ])

    add_h3("Kịch bản 4: Quẹt thẻ chưa đăng ký (Access Denied)")
    add_p("Khi quẹt một thẻ lạ chưa được lưu trong Flash, khối giải mã vẫn nhận đúng dữ liệu nhưng CPU tra cứu Flash không có. Hệ thống lập tức từ chối truy cập và ghi cảnh báo vào nhật ký Flash:")
    add_console_block([
        "===============================================================",
        "  [ACCESS DENIED] >>> TU CHOI TRUY CAP (THE KHONG HOP LE)! <<<",
        "===============================================================",
        "  - The quet         : 0001234567 (FC: 018, ID: 54919)  [UID: 000012D687]",
        "  - Ket qua          : THE CHUA DANG KY trong he thong!",
        "  - Nhat ky Flash    : Da ghi vao Log Slot #1 (Dia chi 0x310010)",
        "==============================================================="
    ])

    doc.add_page_break()

    # =============================================================
    # TRANG 11: KẾT QUẢ TRIỂN KHAI VẬT LÝ ASIC (OPENLANE 2)
    # =============================================================
    add_h1("5. Thiết kế vật lý và kết quả ký duyệt ASIC (OpenLane 2 - SkyWater Sky130A)")
    add_p("Sau khi kiểm chứng chức năng hoàn hảo trên nền tảng demo FPGA Basys 3, toàn bộ mã nguồn Verilog RTL được đưa vào luồng thiết kế vi mạch ASIC tự động hóa OpenLane 2 trên tiến trình bán dẫn CMOS 130 nm SkyWater (PDK: sky130A, thư viện cell chuẩn: sky130_fd_sc_hd).")

    add_h2("5.1. Phân tích thiết lập cấu hình vật lý trong config.json")
    add_p("Trong luồng thiết kế vi mạch tự động hóa OpenLane 2, tệp config.json đóng vai trò là 'trái tim' điều phối toàn bộ các công cụ EDA (Yosys, OpenROAD, Magic, Netgen, KLayout). Tệp cấu hình này thiết lập các ràng buộc công nghệ, thông số floorplan, chiến lược định vị (placement), định tuyến (routing), bảo vệ hiệu ứng ăng-ten (antenna repair) và phân tích định thời tĩnh STA.")
    add_p("Toàn bộ nội dung tệp cấu hình config.json chính thức được áp dụng cho vi mạch rdm6300_picorv32_soc:")
    
    add_console_block([
        "{",
        '  "DESIGN_NAME": "rdm6300_picorv32_soc",',
        '  "PDK": "sky130A",',
        '  "STD_CELL_LIBRARY": "sky130_fd_sc_hd",',
        '  "VERILOG_FILES": [',
        '    "dir::rtl/sync_2ff.v",',
        '    "dir::rtl/uart_rx.v",',
        '    "dir::rtl/rdm6300_frame_decoder.v",',
        '    "dir::rtl/sync_fifo.v",',
        '    "dir::rtl/simpleuart.v",',
        '    "dir::rtl/simpleuart_fifo.v",',
        '    "dir::rtl/spimemio.v",',
        '    "dir::rtl/data_sram.v",',
        '    "dir::rtl/picorv32.v",',
        '    "dir::rtl/rdm6300_picorv32_soc.v"',
        '  ],',
        '  "CLOCK_PORT": "clk",',
        '  "CLOCK_PERIOD": 20.0,',
        '  "PNR_SDC_FILE": "dir::constraints.sdc",',
        '  "SIGNOFF_SDC_FILE": "dir::constraints.sdc",',
        '  "MAX_FANOUT_CONSTRAINT": 12,',
        '  "FP_PIN_ORDER_CFG": "dir::pin_order.cfg",',
        '  "FP_CORE_UTIL": 26,',
        '  "PL_RESIZER_HOLD_SLACK_MARGIN": 0.25,',
        '  "PL_RESIZER_SETUP_SLACK_MARGIN": 0.2,',
        '  "PL_MAX_DISPLACEMENT_X": 100,',
        '  "PL_MAX_DISPLACEMENT_Y": 2,',
        '  "PL_OPTIMIZE_MIRRORING": false,',
        '  "RUN_HEURISTIC_DIODE_INSERTION": true,',
        '  "HEURISTIC_ANTENNA_THRESHOLD": 45,',
        '  "DIODE_PADDING": 0,',
        '  "GRT_OVERFLOW_ITERS": 60,',
        '  "GRT_ANTENNA_ITERS": 15,',
        '  "GRT_ANTENNA_MARGIN": 60,',
        '  "GRT_ALLOW_CONGESTION": true,',
        '  "GRT_LAYER_ADJUSTMENTS": [0.99, 0.65, 0.30, 0, 0, 0],',
        '  "RUN_ANTENNA_REPAIR": true,',
        '  "DIODE_ON_PORTS": "in",',
        '  "SYNTH_STRATEGY": "AREA 0"',
        "}"
    ])

    add_p("Ý nghĩa kỹ thuật và cơ chế điều khiển vật lý của từng nhóm tham số cấu hình then chốt được phân tích chi tiết trong Bảng 2:")

    # Bảng cấu hình config.json chi tiết
    t_cfg = doc.add_table(rows=15, cols=3)
    t_cfg_headers = ["Tham số cấu hình (Parameter)", "Giá trị thiết lập", "Ý nghĩa thiết kế vật lý & Tác động PnR"]
    t_cfg_data = [
        ["DESIGN_NAME, PDK, STD_CELL_LIBRARY", "rdm6300_picorv32_soc\nsky130A / sky130_fd_sc_hd", "Định danh module đỉnh và chọn bộ thư viện tế bào chuẩn SkyWater 130nm High-Density (7-track, điện áp 1.8V)."],
        ["VERILOG_FILES", "10 file RTL (.v)", "Khai báo đầy đủ 10 khối RTL Verilog cấu thành hệ thống: PicoRV32, 1KB SRAM, SPIMEMIO, UART FIFO, RDM6300 decoder."],
        ["CLOCK_PORT, CLOCK_PERIOD", "clk / 20.0 ns (50 MHz)", "Ràng buộc tần số làm việc mục tiêu 50 MHz xuyên suốt các bước Synthesis, Clock Tree Synthesis (CTS) và Sign-off STA."],
        ["PNR_SDC_FILE, SIGNOFF_SDC_FILE", "dir::constraints.sdc", "Đồng nhất ràng buộc định thời (SDC) giữa giai đoạn Place-and-Route và giai đoạn kiểm tra ký duyệt cuối cùng."],
        ["MAX_FANOUT_CONSTRAINT", "12", "Khống chế số tải tối đa của mỗi cổng là 12, chống suy giảm độ dốc sườn xung (slew) và giảm trễ truyền dẫn."],
        ["FP_PIN_ORDER_CFG", "dir::pin_order.cfg", "Quy hoạch phân bổ vị trí 31 chân I/O trên 4 cạnh die, tối ưu khoảng cách kết nối từ pad vào khối logic nội bộ."],
        ["FP_CORE_UTIL", "26 (%)", "Mật độ sử dụng diện tích lõi khởi tạo 26%, để lại 74% diện tích cho kênh định tuyến kim loại và chèn diode bảo vệ."],
        ["PL_RESIZER_HOLD / SETUP_SLACK_MARGIN", "0.25 ns / 0.20 ns", "Biên độ trễ an toàn dự phòng (Guard-band) giúp bộ tối ưu hóa tế bào (Resizer) triệt tiêu vi phạm timing ở mọi góc PVT."],
        ["PL_MAX_DISPLACEMENT_X / Y", "100 / 2", "Giới hạn độ dịch chuyển tế bào theo trục X và Y trong bước tối ưu hóa sau định vị, bảo toàn bố cục tối ưu."],
        ["PL_OPTIMIZE_MIRRORING", "false", "Vô hiệu hóa lật gương tế bào tự do để bảo toàn cấu trúc phân bố chân nguồn và chân đất đồng nhất."],
        ["RUN_HEURISTIC_DIODE_INSERTION, THRESHOLD", "true / 45", "Kích hoạt thuật toán phỏng đoán chèn diode bảo vệ tự động khi tỷ lệ diện tích dây kim loại / cực cổng vượt ngưỡng 45."],
        ["RUN_ANTENNA_REPAIR, DIODE_ON_PORTS", "true / \"in\"", "Tự động phát hiện và chèn diode tiêu tán điện tích plasma tại tất cả các cổng ngõ vào (Input ports) nối trực tiếp từ pad."],
        ["GRT_LAYER_ADJUSTMENTS", "[0.99, 0.65, 0.30, 0, 0, 0]", "Giảm tải định tuyến trên met1 (99%), met2 (65%), met3 (30%) để đẩy các đường dây dài lên met4/met5, triệt tiêu nghẽn."],
        ["SYNTH_STRATEGY", "\"AREA 0\"", "Chiến lược tổng hợp logic Yosys ưu tiên tối ưu hóa diện tích die silicon, triệt tiêu các cổng logic dư thừa."],
    ]
    for c_idx, h_text in enumerate(t_cfg_headers):
        t_cfg.cell(0, c_idx).paragraphs[0].text = h_text
    for r_idx, row_vals in enumerate(t_cfg_data):
        for c_idx, val in enumerate(row_vals):
            t_cfg.cell(r_idx + 1, c_idx).paragraphs[0].text = val
    col_w_cfg = [Inches(2.2), Inches(1.8), Inches(2.27)]
    col_a_cfg = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    style_table(t_cfg, col_w_cfg, col_a_cfg)
    add_caption("Bảng 2. Bảng phân tích chi tiết các tham số vật lý trong config.json và ý nghĩa PnR trên OpenLane 2")

    add_h2("5.2. Trực quan hóa layout vật lý trên công cụ OpenROAD (Openroad_1.png)")
    add_p("Hình ảnh bản vẽ layout vật lý sau bước hoàn thiện định tuyến chi tiết (Detailed Routing) và chèn diode bảo vệ được hiển thị trực tiếp trên giao diện công cụ OpenROAD, thể hiện tại Hình 3.")

    # Chèn Hình 3: Openroad_1.png
    openroad_path = os.path.join(parent_dir, "Openroad_1.png")
    if not os.path.exists(openroad_path):
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

    doc.add_page_break()

    # =============================================================
    # TRANG 12: BÁO CÁO KÝ DUYỆT CHẾ TẠO (ANTENNA, LVS, DRC PASSED)
    # =============================================================
    add_h2("5.3. Báo cáo ký duyệt chế tạo sign-off toàn diện (AntennaLvsDrc.png)")
    add_p("Ở lượt chạy chính thức mang mã định danh RUN_2026-09-27_21-51-11, bước kiểm tra khả năng chế tạo ReportManufacturability (bước 75) đã xác nhận thiết kế vi mạch vượt qua 100% các tiêu chí ký duyệt vật lý khắt khe nhất:")
    add_bullet("Lỗi Antenna: Passed ✅ — ", "0 net violations, 0 pin violations. Thuật toán chèn diode phỏng đoán và chèn diode tại các cổng I/O đã bảo vệ hoàn toàn cực cổng của các transistor khỏi hiện tượng phóng điện plasma.")
    add_bullet("Kiểm tra LVS (Netgen): Passed ✅ — ", "Netlist trích xuất từ layout GDSII hoàn toàn trùng khớp với Netlist nguyên lý (Circuits match uniquely, 57,544 devices và 50,028 nets trùng khớp 100%, 0 thiết bị sai lệch).")
    add_bullet("Kiểm tra DRC (Magic & KLayout): Passed ✅ — ", "0 lỗi vi phạm quy tắc hình học trên cả 2 công cụ kiểm tra độc lập Magic (COUNT: 0) và KLayout (klayout__drc_error__count: 0).")

    # Chèn Hình 4: AntennaLvsDrc.png
    antenna_lvs_path = os.path.join(parent_dir, "AntennaLvsDrc.png")
    if os.path.exists(antenna_lvs_path):
        p_img4 = doc.add_paragraph()
        p_img4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img4.paragraph_format.space_before = Pt(4)
        p_img4.paragraph_format.space_after = Pt(2)
        p_img4.paragraph_format.keep_with_next = True
        run_img4 = p_img4.add_run()
        run_img4.add_picture(antenna_lvs_path, width=Inches(5.8))
        add_caption("Hình 4. Báo cáo kiểm tra chế tạo ký duyệt vật lý sign-off: Antenna Passed, LVS Passed, DRC Passed")

    # Bảng 2: Thông số Sign-off ASIC
    t2 = doc.add_table(rows=12, cols=3)
    t2_headers = ["Thông số vật lý / Ký duyệt (Metric)", "Giá trị đạt được", "Tiêu chuẩn / Đánh giá kiểm tra"]
    t2_data = [
        ["Tiến trình công nghệ (Process)", "SkyWater 130nm (sky130_fd_sc_hd)", "Tiến trình CMOS nguồn mở chuẩn công nghiệp"],
        ["Tần số xung nhịp hoạt động (Clock)", "50 MHz (Chu kỳ 20.0 ns)", "Đạt chuẩn định thời tại 50 MHz"],
        ["Mật độ sử dụng tế bào (Cell Utilization)", "26% (Khởi tạo Floorplan)", "Mật độ tối ưu giải phóng nghẽn định tuyến"],
        ["Số cổng kết nối ngoại vi (I/O Pins)", "31 pins", "Phân bổ cân đối 4 cạnh die (pin_order.cfg)"],
        ["Tổng số thiết bị so khớp LVS (Devices)", "57,544 devices", "Circuits match uniquely (Netgen 1.5)"],
        ["Tổng số đường dây so khớp LVS (Nets)", "50,028 nets", "Circuits match uniquely (Netgen 1.5)"],
        ["Lỗi quy tắc Antenna (Antenna Violations)", "0 LỖI (Passed ✅)", "0 violating nets, 0 violating pins"],
        ["Kiểm tra Magic DRC", "0 LỖI (Passed ✅)", "COUNT: 0 (Sạch 100% lỗi hình học)"],
        ["Kiểm tra KLayout DRC", "0 LỖI (Passed ✅)", "klayout__drc_error__count = 0"],
        ["Kiểm tra đối chiếu Layout - Sơ đồ (LVS)", "PASSED ✅", "0 lỗi LVS, Netlist trùng khớp tuyệt đối"],
        ["Định thời Setup & Hold (STA)", "MET TIMING ✅", "No setup violations, No hold violations"],
    ]
    for c_idx, h_text in enumerate(t2_headers):
        t2.cell(0, c_idx).paragraphs[0].text = h_text
    for r_idx, row_vals in enumerate(t2_data):
        for c_idx, val in enumerate(row_vals):
            t2.cell(r_idx + 1, c_idx).paragraphs[0].text = val
    col_w2 = [Inches(2.5), Inches(1.8), Inches(1.97)]
    col_a2 = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    style_table(t2, col_w2, col_a2)
    add_caption("Bảng 3. Bảng tổng hợp các thông số ký duyệt (Signoff Metrics) của chip ASIC Sky130A (RUN_2026-09-27_21-51-11)")

    doc.add_page_break()

    # =============================================================
    # TRANG 13: PHÂN TÍCH ĐỊNH THỜI TĨNH STA (MET TIMING) & IR DROP
    # =============================================================
    add_h2("5.4. Đánh giá phân tích định thời tĩnh STA đa góc đo (9 corners) và MET TIMING")
    add_p("Trong thiết kế vi mạch số chuyên nghiệp, **MET TIMING** là kết quả quan trọng nhất và là điều kiện bắt buộc để chip có thể sản xuất thành công. Phân tích định thời tĩnh Post-PnR bằng OpenROAD trên lượt chạy RUN_2026-09-27_21-51-11 xác nhận rằng hệ thống hoàn toàn sạch lỗi định thời trên cả 9 góc đo công nghệ khắc nghiệt nhất:")
    add_bullet("1. Không có vi phạm thời gian thiết lập (No Setup Violations): ", "Tại tần số 50 MHz (chu kỳ 20.0 ns), mọi đường truyền dữ liệu tổ hợp đều đến kịp trước sườn xung nhịp tiếp theo (Setup Slack > 0 ở cả 9 corners).")
    add_bullet("2. Không có vi phạm thời gian duy trì (No Hold Violations): ", "Cây xung nhịp CTS được cân bằng tối ưu và các bộ đệm delay được chèn hợp lý, đảm bảo dữ liệu không bao giờ chạy quá nhanh đè lên chu kỳ cũ (Hold Slack > 0 ở cả 9 corners).")
    add_bullet("3. Không có vi phạm Max Slew & Max Capacitance: ", "Độ dốc sườn xung và tải điện dung trên toàn bộ dây kim loại đều nằm trong ngưỡng an toàn của thư viện cell chuẩn.")

    # Bảng 4: STA Summary 9 Corners
    t3 = doc.add_table(rows=10, cols=5)
    t3_headers = ["Góc đo công nghệ (PVT Corner)", "Điều kiện Môi trường", "Setup Violations", "Hold Violations", "Đánh giá Ký duyệt"]
    t3_data = [
        ["nom_tt_025C_1v80", "Điển hình: 25°C, 1.80V", "0 vi phạm", "0 vi phạm", "MET TIMING ✅"],
        ["nom_ss_100C_1v60", "Chậm: 100°C, 1.60V", "0 vi phạm", "0 vi phạm", "MET TIMING ✅"],
        ["nom_ff_n40C_1v95", "Nhanh: -40°C, 1.95V", "0 vi phạm", "0 vi phạm", "MET TIMING ✅"],
        ["min_tt_025C_1v80", "Điển hình: 25°C, 1.80V", "0 vi phạm", "0 vi phạm", "MET TIMING ✅"],
        ["min_ss_100C_1v60", "Chậm: 100°C, 1.60V", "0 vi phạm", "0 vi phạm", "MET TIMING ✅"],
        ["min_ff_n40C_1v95", "Nhanh: -40°C, 1.95V", "0 vi phạm", "0 vi phạm", "MET TIMING ✅"],
        ["max_tt_025C_1v80", "Điển hình: 25°C, 1.80V", "0 vi phạm", "0 vi phạm", "MET TIMING ✅"],
        ["max_ss_100C_1v60", "Góc xấu nhất: 100°C, 1.60V", "0 vi phạm", "0 vi phạm", "MET TIMING ✅"],
        ["max_ff_n40C_1v95", "Nhiệt độ âm: -40°C, 1.95V", "0 vi phạm", "0 vi phạm", "MET TIMING ✅"],
    ]
    for c_idx, h_text in enumerate(t3_headers):
        t3.cell(0, c_idx).paragraphs[0].text = h_text
    for r_idx, row_vals in enumerate(t3_data):
        for c_idx, val in enumerate(row_vals):
            t3.cell(r_idx + 1, c_idx).paragraphs[0].text = val
    col_w3 = [Inches(1.8), Inches(1.8), Inches(0.9), Inches(0.9), Inches(0.87)]
    col_a3 = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER]
    style_table(t3, col_w3, col_a3)
    add_caption("Bảng 4. Báo cáo phân tích định thời tĩnh STA qua 9 góc đo công nghệ trên OpenROAD (Đạt MET TIMING 100%)")

    add_h2("5.5. Phân tích lưới nguồn PDN và kiểm tra sụt áp (IR drop analysis)")
    add_p("Báo cáo phân tích mạng phân phối nguồn (Power Distribution Network - PDN) từ OpenROAD PSM (bước 56) ghi nhận kết quả tuyệt vời:")
    add_bullet("Độ sụt áp nguồn cấp (VPWR IR Drop): ", "Điện áp danh định 1.80 V, độ sụt áp trung bình chỉ 0.0733 mV, độ sụt áp xấu nhất chỉ 0.739 mV (Tương ứng mức sụt áp cực nhỏ: 0.04%).")
    add_bullet("Độ nảy điện thế đất (VGND Bounce): ", "Điện áp danh định 0.00 V, điện thế đất xấu nhất chỉ 0.648 mV (Tương ứng mức biến động cực nhỏ: 0.04%).")
    add_p("Kết quả trên khẳng định mạng lưới nguồn kim loại trên các lớp met4 và met5 được thiết kế cực kỳ vững chắc, đảm bảo nguồn điện ổn định cho toàn bộ 57,544 thiết bị bán dẫn hoạt động đồng thời.")

    doc.add_page_break()

    # =============================================================
    # TRANG 14: THẢO LUẬN & ĐÁNH GIÁ TỐI ƯU HÓA PPA
    # =============================================================
    add_h1("6. Thảo luận và đánh giá tối ưu hóa PPA")
    add_h2("6.1. Hiệu quả tối ưu hóa diện tích, công suất và hiệu năng")
    add_bullet("Phần cứng hóa bộ giải mã RDM6300 tự trị: ", "Toàn bộ việc nhận diện STX/ETX, chuyển đổi ASCII-to-Hex và đối chiếu XOR checksum được thực hiện tự động bằng phần cứng trong 1 chu kỳ clock. CPU PicoRV32 hoàn toàn rảnh tay để tập trung vào logic tra cứu thẻ và quản lý Flash, không bao giờ bị trễ hay mất ký tự.")
    add_bullet("Bộ đệm FIFO phần cứng cho UART: ", "Ngăn chặn hoàn toàn hiện tượng nghẽn bus hoặc rơi rụng lệnh khi CPU đang thực hiện chu kỳ ghi Flash tốn vài mili-giây.")
    add_bullet("Phối hợp hoàn hảo giữa FPGA Prototype và ASIC: ", "Việc kiểm chứng thực nghiệm trên bo mạch demo Basys 3 đã phát hiện và xử lý sớm toàn bộ các lỗi tiềm ẩn về mặt timing và giao thức trước khi bước vào luồng thiết kế ASIC, giúp luồng OpenLane đạt kết quả Sign-off sạch 100% ngay từ các lượt chạy đầu tiên.")

    add_h2("6.2. Hạn chế và các định hướng phát triển tiếp theo")
    add_bullet("Tích hợp SRAM Compiler cứng (OpenRAM): ", "Hiện tại bộ nhớ nhúng được tổng hợp từ standard cell flip-flops. Trong tương lai, việc tích hợp macro OpenRAM sẽ giúp giảm thêm 25-35% diện tích khuôn die silicon.")
    add_bullet("Nâng cấp giao tiếp Flash lên Quad-SPI (QSPI): ", "Nâng cấp bộ điều khiển từ 1-bit SPI lên 4-bit Quad-SPI sẽ giúp tăng gấp 4 lần tốc độ đọc dữ liệu thẻ từ Flash.")
    add_bullet("Tích hợp động cơ mã hóa phần cứng (Lightweight Crypto): ", "Tích hợp khối mã hóa phần cứng AES-128 để mã hóa toàn bộ cơ sở dữ liệu thẻ trước khi ghi vào Flash, bảo vệ tuyệt đối chống lại hành vi trích xuất dữ liệu Flash trái phép.")

    doc.add_page_break()

    # =============================================================
    # TRANG 15: KẾT LUẬN
    # =============================================================
    add_h1("7. Kết luận")
    add_p("Đồ án \"Thiết kế hệ thống quét và xử lý dữ liệu thẻ RFID tích hợp CPU RISC-V PicoRV32 quản lý dữ liệu trên Flash\" đã hoàn thành xuất sắc toàn bộ các mục tiêu nghiên cứu và yêu cầu kỹ thuật đề ra, từ cấp độ ý tưởng, thiết kế vi kiến trúc, kiểm chứng thực nghiệm trên FPGA đến hiện thực hóa vi mạch bán dẫn ASIC hoàn chỉnh.")
    add_p("Hệ thống giải quyết triệt để nhu cầu thực tế về một thiết bị kiểm soát ra vào vận hành độc lập (Offline Standalone), hoàn toàn không cần kết nối Internet, mang lại độ tin cậy tuyệt đối, độ trễ xác thực gần như tức thời (< 10 µs) và loại trừ mọi nguy cơ an ninh mạng từ xa. Việc ứng dụng bộ nhớ bất biến Non-Volatile SPI Flash là quyết định kiến trúc đúng đắn, cho phép lưu trữ cơ sở dữ liệu danh mục thẻ và nhật ký ra vào an toàn qua nhiều thập kỷ mà không cần pin nuôi.")
    add_p("Trên nền tảng demo FPGA Basys 3, hệ thống đã chứng minh độ ổn định và tính khả thi thực tế cao: Module đọc thẻ RFID RDM6300 thật, chip Flash SPI thật và phần mềm Host Console trên máy tính hoạt động đồng bộ hoàn hảo, xử lý mượt mà toàn bộ các chu trình đăng ký thẻ mới, tra cứu danh mục, kiểm soát ra vào và xuất nhật ký ra file CSV.")
    add_p("Trên nền tảng ASIC SkyWater Sky130A với công cụ OpenLane 2, lượt chạy chính thức RUN_2026-09-27_21-51-11 đã đạt chuẩn ký duyệt chế tạo hoàn hảo (Full Tapeout Sign-off Ready): Đạt tuyệt đối 0 vi phạm Antenna, 0 lỗi Magic DRC, 0 lỗi KLayout DRC, Netgen LVS Clean (57,544 devices và 50,028 nets trùng khớp 100%), và đạt chuẩn định thời **MET TIMING** trên cả 9 góc đo công nghệ ở tần số 50 MHz. Bản vẽ layout GDSII hoàn chỉnh khẳng định sự thành công rực rỡ của đề tài, sẵn sàng gửi đi gia công sản xuất thương mại.")

    # -------------------------------------------------------------
    # Save Document
    # -------------------------------------------------------------
    out_docx_path = os.path.join(cur_dir, "Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.docx")
    alt_docx_path = os.path.join(cur_dir, "Bao_Cao_Do_An_RDM6300_PicoRV32_SoC_v2.docx")
    
    doc.save(alt_docx_path)
    print(f"[SUCCESS] Updated report saved successfully at: {alt_docx_path}")
    
    try:
        doc.save(out_docx_path)
        print(f"[SUCCESS] Primary report also updated successfully at: {out_docx_path}")
    except PermissionError:
        print(f"[NOTE] Primary file {out_docx_path} is currently locked by Word. Available at {alt_docx_path}.")

if __name__ == "__main__":
    create_report()
