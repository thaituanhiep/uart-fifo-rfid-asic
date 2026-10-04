# -*- coding: utf-8 -*-
"""
apply_3col_table.py
Updates the 2-column table to 3 columns in both:
1. create_presentation.py (Slide 11: add_bus_table_slide)
2. generate_report_docx.py (Section 6.2 Table 2)
Column 0: Trường Hợp / Thời Điểm
Column 1: Cấu Hình RTL & Mã Lệnh Firmware C
Column 2: Ý Nghĩa Thao Tác & Cơ Chế Co-Design
"""

import os
import re

cur_dir = os.path.dirname(os.path.abspath(__file__))

# =============================================================================
# 1. UPDATE CREATE_PRESENTATION.PY (SLIDE 11: add_bus_table_slide)
# =============================================================================
pres_path = os.path.join(cur_dir, "create_presentation.py")
with open(pres_path, "r", encoding="utf-8") as f:
    pres_code = f.read()

# Replace add_bus_table_slide implementation
old_table_func_pattern = re.compile(
    r'    def add_bus_table_slide\(slide_num, title, rows_data\):.*?'
    r'        return slide\n',
    re.DOTALL
)

new_table_func = '''    def add_bus_table_slide(slide_num, title, rows_data):
        slide = prs.slides.add_slide(blank_layout)
        add_header(slide, "Phần 6: Firmware C & Ánh Xạ MMIO", title, slide_num, total_slides=TOTAL_SLIDES)

        x = Inches(0.8)
        y = Inches(1.30)
        w = Inches(11.733)
        h = Inches(5.60)

        num_rows = len(rows_data) + 1
        tbl_shape = slide.shapes.add_table(num_rows, 3, x, y, w, h)
        tbl = tbl_shape.table

        col_w = [Inches(1.85), Inches(4.95), Inches(4.933)]
        for ci, cw in enumerate(col_w):
            tbl.columns[ci].width = cw

        headers = [
            "Trường Hợp / Thời Điểm",
            "Cấu Hình RTL & Mã Lệnh Firmware C",
            "Ý Nghĩa Thao Tác & Cơ Chế Co-Design"
        ]

        for ci, h_text in enumerate(headers):
            cell = tbl.cell(0, ci)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_NAVY_DARK
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.margin_left = Inches(0.10)
            cell.margin_right = Inches(0.10)
            cell.margin_top = Inches(0.05)
            cell.margin_bottom = Inches(0.05)

            p = cell.text_frame.paragraphs[0]
            p.text = h_text
            p.font.name = "Segoe UI"
            p.font.size = Pt(10.5)
            p.font.bold = True
            p.font.color.rgb = C_WHITE
            p.alignment = PP_ALIGN.CENTER if ci == 0 else PP_ALIGN.LEFT

        for ri, r in enumerate(rows_data):
            row_idx = ri + 1
            row_bg = RGBColor(241, 245, 249) if ri % 2 == 0 else RGBColor(255, 255, 255)

            # Cột 0: Trường hợp / Thời điểm
            c0 = tbl.cell(row_idx, 0)
            c0.fill.solid()
            c0.fill.fore_color.rgb = row_bg
            c0.vertical_anchor = MSO_ANCHOR.MIDDLE
            c0.margin_left = Inches(0.06)
            c0.margin_right = Inches(0.06)
            tf0 = c0.text_frame
            tf0.word_wrap = True

            p0_1 = tf0.paragraphs[0]
            p0_1.text = r["time"]
            p0_1.font.name = "Segoe UI"
            p0_1.font.size = Pt(10.5)
            p0_1.font.bold = True
            p0_1.font.color.rgb = C_BLUE_ACCENT
            p0_1.alignment = PP_ALIGN.CENTER

            p0_2 = tf0.add_paragraph()
            p0_2.text = r["task"]
            p0_2.font.name = "Segoe UI"
            p0_2.font.size = Pt(9.0)
            p0_2.font.bold = True
            p0_2.font.color.rgb = C_TEXT_DARK
            p0_2.alignment = PP_ALIGN.CENTER

            # Cột 1: Cấu hình RTL & Code C
            c1 = tbl.cell(row_idx, 1)
            c1.fill.solid()
            c1.fill.fore_color.rgb = row_bg
            c1.vertical_anchor = MSO_ANCHOR.MIDDLE
            c1.margin_left = Inches(0.10)
            c1.margin_right = Inches(0.10)
            c1.margin_top = Inches(0.03)
            c1.margin_bottom = Inches(0.03)
            tf1 = c1.text_frame
            tf1.word_wrap = True

            # RTL line
            p1 = tf1.paragraphs[0]
            r1_lbl = p1.add_run()
            r1_lbl.text = "• RTL: "
            r1_lbl.font.name = "Segoe UI"
            r1_lbl.font.size = Pt(8.5)
            r1_lbl.font.bold = True
            r1_lbl.font.color.rgb = C_BLUE_ACCENT

            r1_file = p1.add_run()
            r1_file.text = r["rtl_file"] + "  "
            r1_file.font.name = "Segoe UI"
            r1_file.font.size = Pt(8.0)
            r1_file.font.bold = True
            r1_file.font.color.rgb = RGBColor(30, 58, 138)

            r1_code = p1.add_run()
            r1_code.text = r["rtl_code"]
            r1_code.font.name = "Consolas"
            r1_code.font.size = Pt(8.0)
            r1_code.font.bold = True
            r1_code.font.color.rgb = RGBColor(15, 23, 42)
            p1.space_after = Pt(1.0)

            # C line
            p2 = tf1.add_paragraph()
            r2_lbl = p2.add_run()
            r2_lbl.text = "• Code C: "
            r2_lbl.font.name = "Segoe UI"
            r2_lbl.font.size = Pt(8.5)
            r2_lbl.font.bold = True
            r2_lbl.font.color.rgb = C_GREEN

            r2_file = p2.add_run()
            r2_file.text = r["c_file"] + "  "
            r2_file.font.name = "Segoe UI"
            r2_file.font.size = Pt(8.0)
            r2_file.font.bold = True
            r2_file.font.color.rgb = RGBColor(21, 128, 61)

            r2_code = p2.add_run()
            r2_code.text = r["c_code"]
            r2_code.font.name = "Consolas"
            r2_code.font.size = Pt(8.0)
            r2_code.font.bold = True
            r2_code.font.color.rgb = RGBColor(15, 23, 42)

            # Cột 2: Ý nghĩa thao tác chuyển qua đây
            c2 = tbl.cell(row_idx, 2)
            c2.fill.solid()
            c2.fill.fore_color.rgb = row_bg
            c2.vertical_anchor = MSO_ANCHOR.MIDDLE
            c2.margin_left = Inches(0.10)
            c2.margin_right = Inches(0.10)
            c2.margin_top = Inches(0.03)
            c2.margin_bottom = Inches(0.03)
            tf2 = c2.text_frame
            tf2.word_wrap = True

            p3 = tf2.paragraphs[0]
            r3_text = p3.add_run()
            r3_text.text = r["meaning"]
            r3_text.font.name = "Segoe UI"
            r3_text.font.size = Pt(8.0)
            r3_text.font.color.rgb = C_TEXT_DARK
            p3.line_spacing = 1.10

        return slide
'''

if old_table_func_pattern.search(pres_code):
    pres_code = old_table_func_pattern.sub(new_table_func, pres_code, count=1)
    with open(pres_path, "w", encoding="utf-8") as f:
        f.write(pres_code)
    print("[SUCCESS] Updated add_bus_table_slide to 3 columns in create_presentation.py")
else:
    print("[ERROR] old_table_func_pattern not found in create_presentation.py")

# =============================================================================
# 2. UPDATE GENERATE_REPORT_DOCX.PY (SECTION 6.2 TABLE 2)
# =============================================================================
docx_path = os.path.join(cur_dir, "generate_report_docx.py")
with open(docx_path, "r", encoding="utf-8") as f:
    docx_code = f.read()

old_docx_t2_pattern = re.compile(
    r'    t2_headers = \["Trường hợp / Thời điểm", "Thiết lập RTL, Định nghĩa C & Ý nghĩa thao tác của Firmware C"\]\n'
    r'    t2_rows = \[.*?    col_w2 = \[Inches\(1\.85\), Inches\(4\.80\)\]\n'
    r'    col_a2 = \[WD_ALIGN_PARAGRAPH\.CENTER, WD_ALIGN_PARAGRAPH\.LEFT\]\n'
    r'    style_table\(t2, col_w2, col_a2, font_size=10\.0\)\n'
    r'    add_caption\("Bảng 2\. Bảng phân tích chu kỳ bus thực tế: Đối chiếu thiết lập giải mã RTL, định nghĩa code C và ý nghĩa biến địa chỉ"\)',
    re.DOTALL
)

new_docx_t2 = '''    t2_headers = [
        "Trường hợp / Thời điểm",
        "Thiết lập RTL & Định nghĩa Firmware C",
        "Ý nghĩa thao tác của Firmware C"
    ]
    t2_rows = [
        {
            "case_time": "T = 0",
            "case_task": "(Boot Flash XIP)",
            "rtl_code": "[rtl/rdm6300_picorv32_soc.v] parameter PROGADDR_RESET = 32'h0025_0000;\\n[rtl/core/soc_interconnect.v] assign sel_spimem = cpu_mem_valid && (cpu_mem_addr >= 32'h0010_0000 && cpu_mem_addr < 32'h0100_0000);",
            "c_code": "[firmware/boot/sections.lds] FLASH (rx) : ORIGIN = 0x00250000",
            "meaning": "Cấu hình vector reset của CPU trỏ trực tiếp vào Flash SPI để CPU tự động nạp và thực thi trực tiếp các opcode của firmware (XIP - Execute-in-Place) ngay sau khi nhả reset mà không cần nạp mã trung gian vào RAM."
        },
        {
            "case_time": "T = 1..100",
            "case_task": "(Tạo Stack RAM)",
            "rtl_code": "[rtl/core/soc_interconnect.v] assign sel_sram = cpu_mem_valid && (cpu_mem_addr < 32'h0000_0400);",
            "c_code": "[firmware/boot/start.s] li sp, 0x00000400",
            "meaning": "C sử dụng vùng không gian địa chỉ SRAM 1KB (< 0x0400) thông qua con trỏ ngăn xếp sp để cấp phát biến cục bộ, lưu trữ stack frame và địa chỉ trả về hàm (ra), phản hồi tức thì trong 1 chu kỳ clock."
        },
        {
            "case_time": "T = 101",
            "case_task": "(Vào hàm main)",
            "rtl_code": "[rtl/core/soc_interconnect.v] assign sel_spimem = cpu_mem_valid && (cpu_mem_addr >= 32'h0010_0000 && cpu_mem_addr < 32'h0100_0000);",
            "c_code": "[firmware/boot/sections.lds] .text : { *(.text*) } > FLASH",
            "meaning": "C đặt toàn bộ mã máy thực thi của hàm main() và logic ứng dụng vào Flash để CPU đọc và giải mã từng opcode trực tiếp qua bus XIP, giải phóng toàn bộ 1KB SRAM chỉ dành cho lưu trữ dữ liệu động."
        },
        {
            "case_time": "T = 105",
            "case_task": "(Set Baud RFID)",
            "rtl_code": "[rtl/core/soc_interconnect.v] assign sel_rfid = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h1);",
            "c_code": "[firmware/common/soc_regs.h] #define REG_RFID_UART_DIV (*(volatile uint32_t*)0x10000000)",
            "meaning": "C ghi giá trị chia tần 5208 vào địa chỉ 0x10000000 để cấu hình bộ chia baud rate 9600 bps cho khối UART RFID (50 MHz / 9600), sẵn sàng thu nhận các xung tín hiệu nối tiếp từ module đầu đọc thẻ RDM6300."
        },
        {
            "case_time": "T = 200",
            "case_task": "(Đọc thẻ RFID)",
            "rtl_code": "[rtl/core/soc_interconnect.v] assign sel_rfid = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h1);",
            "c_code": "[firmware/common/soc_regs.h] #define REG_RFID_UART_DAT (*(volatile uint32_t*)0x10000004)",
            "meaning": "C đọc từ địa chỉ 0x10000004 để rút (pop) 1 byte dữ liệu từ hàng đợi phần cứng FIFO 32-byte (đọc không khóa: trả về byte mã thẻ nếu có dữ liệu, hoặc trả về 0xFFFFFFFF nếu FIFO rỗng để CPU không bị treo chờ bus)."
        },
        {
            "case_time": "T = 250",
            "case_task": "(Gửi PC UART)",
            "rtl_code": "[rtl/core/soc_interconnect.v] assign sel_uart = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h3);",
            "c_code": "[firmware/common/soc_regs.h] #define REG_PC_UART_DAT (*(volatile uint32_t*)0x30000004)",
            "meaning": "C ghi byte vào địa chỉ 0x30000004 để đẩy ký tự vào TX FIFO truyền lên máy tính Host PC, và đọc từ địa chỉ này để nhận các chuỗi lệnh cấu hình quản trị (Ping, thêm/xóa thẻ Whitelist, xuất nhật ký ra file CSV)."
        },
        {
            "case_time": "T = 300",
            "case_task": "(Bật LED / Cửa)",
            "rtl_code": "[rtl/core/soc_interconnect.v] assign sel_gpio = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h4);",
            "c_code": "[firmware/common/soc_regs.h] #define REG_GPIO_LEDS (*(volatile uint32_t*)0x40000000)",
            "meaning": "C ghi giá trị bitmask vào địa chỉ 0x40000000 để điều khiển trực tiếp 16 LED chẩn đoán trên bo mạch và đóng/ngắt relay chốt cửa điện từ (Bit 0: Nhịp tim Alive, Bit 1: Cảnh báo từ chối Denied, Bit 2: Mở chốt cửa Granted)."
        },
        {
            "case_time": "T = 400",
            "case_task": "(Ghi Flash từ RAM)",
            "rtl_code": "[rtl/core/soc_interconnect.v] assign sel_spicfg = cpu_mem_valid && (cpu_mem_addr == 32'h0200_0000);",
            "c_code": "[firmware/boot/start.s] flashio_worker: li t0, 0x02000000",
            "meaning": "Khi thực thi mã từ SRAM, hàm của C phát lệnh bit-bang SPI vào địa chỉ 0x02000000 để xóa sector và ghi dữ liệu thẻ mới vào Flash Whitelist / Log mà không gây xung đột bus với các chu kỳ đọc lệnh XIP."
        }
    ]

    t2 = doc.add_table(rows=len(t2_rows) + 1, cols=3)
    for c_idx, h_text in enumerate(t2_headers):
        t2.cell(0, c_idx).paragraphs[0].text = h_text

    for r_idx, r in enumerate(t2_rows):
        row_num = r_idx + 1
        # Cột 0: Trường hợp / Thời điểm
        c0 = t2.cell(row_num, 0)
        p0 = c0.paragraphs[0]
        r0_1 = p0.add_run(r["case_time"] + "\\n")
        r0_1.bold = True
        r0_2 = p0.add_run(r["case_task"])

        # Cột 1: Cấu hình RTL & Code C
        c1 = t2.cell(row_num, 1)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(1.5)
        p1.paragraph_format.space_after = Pt(1.5)
        p1.paragraph_format.line_spacing = 1.05
        r1_lbl = p1.add_run("• Code RTL: ")
        r1_lbl.bold = True
        r1_code = p1.add_run(r["rtl_code"])
        r1_code.font.name = "Consolas"
        r1_code.bold = True

        p2 = c1.add_paragraph()
        p2.paragraph_format.space_before = Pt(1.5)
        p2.paragraph_format.space_after = Pt(1.5)
        p2.paragraph_format.line_spacing = 1.05
        r2_lbl = p2.add_run("• Code C: ")
        r2_lbl.bold = True
        r2_code = p2.add_run(r["c_code"])
        r2_code.font.name = "Consolas"
        r2_code.bold = True

        # Cột 2: Ý nghĩa thao tác chuyển qua cột mới
        c2 = t2.cell(row_num, 2)
        p3 = c2.paragraphs[0]
        p3.paragraph_format.space_before = Pt(1.5)
        p3.paragraph_format.space_after = Pt(1.5)
        p3.paragraph_format.line_spacing = 1.12
        r3_txt = p3.add_run(r["meaning"])

    col_w2 = [Inches(1.25), Inches(2.75), Inches(2.70)]
    col_a2 = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.JUSTIFY]
    style_table(t2, col_w2, col_a2, font_size=8.5)
    add_caption("Bảng 2. Bảng phân tích chu kỳ bus thực tế: Đối chiếu thiết lập giải mã RTL, định nghĩa code C và ý nghĩa thao tác của Firmware")'''

if old_docx_t2_pattern.search(docx_code):
    docx_code = old_docx_t2_pattern.sub(new_docx_t2, docx_code, count=1)
    with open(docx_path, "w", encoding="utf-8") as f:
        f.write(docx_code)
    print("[SUCCESS] Updated Table 2 to 3 columns in generate_report_docx.py")
else:
    print("[ERROR] old_docx_t2_pattern not found in generate_report_docx.py")
