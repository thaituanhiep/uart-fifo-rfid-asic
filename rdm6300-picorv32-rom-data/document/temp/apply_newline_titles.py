# -*- coding: utf-8 -*-
"""
apply_newline_titles.py
Updates Slide 11 (PPTX) and Table 2 (DOCX):
- Tiêu đề "• RTL [file]:" -> XUỐNG DÒNG -> in mã code RTL
- Tiêu đề "• Code C [file]:" -> XUỐNG DÒNG -> in mã code C
- Đảm bảo toàn bộ 8 hàng hiển thị đầy đủ, không bị cắt.
"""

import os
import re

cur_dir = os.path.dirname(os.path.abspath(__file__))

# =============================================================================
# 1. UPDATE CREATE_PRESENTATION.PY (SLIDE 11)
# =============================================================================
pres_path = os.path.join(cur_dir, "create_presentation.py")
with open(pres_path, "r", encoding="utf-8") as f:
    code = f.read()

new_table_func = '''    def add_bus_table_slide(slide_num, title, rows_data):
        slide = prs.slides.add_slide(blank_layout)
        add_header(slide, "Phần 6: Firmware C & Ánh Xạ MMIO", title, slide_num, total_slides=TOTAL_SLIDES)

        x = Inches(0.8)
        y = Inches(1.15)
        w = Inches(11.733)
        h = Inches(5.75)

        num_rows = len(rows_data) + 1
        tbl_shape = slide.shapes.add_table(num_rows, 3, x, y, w, h)
        tbl = tbl_shape.table

        col_w = [Inches(1.50), Inches(6.00), Inches(4.233)]
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
            cell.margin_left = Inches(0.08)
            cell.margin_right = Inches(0.08)
            cell.margin_top = Inches(0.02)
            cell.margin_bottom = Inches(0.02)

            p = cell.text_frame.paragraphs[0]
            p.text = h_text
            p.font.name = "Segoe UI"
            p.font.size = Pt(9.5)
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
            c0.margin_left = Inches(0.04)
            c0.margin_right = Inches(0.04)
            c0.margin_top = Inches(0.01)
            c0.margin_bottom = Inches(0.01)
            tf0 = c0.text_frame
            tf0.word_wrap = True

            p0_1 = tf0.paragraphs[0]
            p0_1.text = r["time"]
            p0_1.font.name = "Segoe UI"
            p0_1.font.size = Pt(9.5)
            p0_1.font.bold = True
            p0_1.font.color.rgb = C_BLUE_ACCENT
            p0_1.alignment = PP_ALIGN.CENTER

            p0_2 = tf0.add_paragraph()
            p0_2.text = r["task"]
            p0_2.font.name = "Segoe UI"
            p0_2.font.size = Pt(8.0)
            p0_2.font.bold = True
            p0_2.font.color.rgb = C_TEXT_DARK
            p0_2.alignment = PP_ALIGN.CENTER

            # Cột 1: Cấu hình RTL & Code C: Tiêu đề -> Xuống dòng -> Code
            c1 = tbl.cell(row_idx, 1)
            c1.fill.solid()
            c1.fill.fore_color.rgb = row_bg
            c1.vertical_anchor = MSO_ANCHOR.MIDDLE
            c1.margin_left = Inches(0.06)
            c1.margin_right = Inches(0.06)
            c1.margin_top = Inches(0.01)
            c1.margin_bottom = Inches(0.01)
            tf1 = c1.text_frame
            tf1.word_wrap = True

            # 1. Tiêu đề RTL
            p1 = tf1.paragraphs[0]
            p1.space_before = 0
            p1.space_after = 0
            p1.line_spacing = 1.0
            r1_lbl = p1.add_run()
            r1_lbl.text = "• RTL "
            r1_lbl.font.name = "Segoe UI"
            r1_lbl.font.size = Pt(7.5)
            r1_lbl.font.bold = True
            r1_lbl.font.color.rgb = C_BLUE_ACCENT

            r1_file = p1.add_run()
            r1_file.text = r["rtl_file"] + ":"
            r1_file.font.name = "Segoe UI"
            r1_file.font.size = Pt(7.0)
            r1_file.font.bold = True
            r1_file.font.color.rgb = RGBColor(30, 58, 138)

            # 2. Xuống dòng: Mã code RTL
            p1_code = tf1.add_paragraph()
            p1_code.space_before = 0
            p1_code.space_after = Pt(1.5)
            p1_code.line_spacing = 1.0
            r1_code = p1_code.add_run()
            r1_code.text = "  " + r["rtl_code"]
            r1_code.font.name = "Consolas"
            r1_code.font.size = Pt(6.8)
            r1_code.font.bold = True
            r1_code.font.color.rgb = RGBColor(15, 23, 42)

            # 3. Tiêu đề Code C (Xuống dòng riêng biệt)
            p2 = tf1.add_paragraph()
            p2.space_before = 0
            p2.space_after = 0
            p2.line_spacing = 1.0
            r2_lbl = p2.add_run()
            r2_lbl.text = "• Code C "
            r2_lbl.font.name = "Segoe UI"
            r2_lbl.font.size = Pt(7.5)
            r2_lbl.font.bold = True
            r2_lbl.font.color.rgb = C_GREEN

            r2_file = p2.add_run()
            r2_file.text = r["c_file"] + ":"
            r2_file.font.name = "Segoe UI"
            r2_file.font.size = Pt(7.0)
            r2_file.font.bold = True
            r2_file.font.color.rgb = RGBColor(21, 128, 61)

            # 4. Xuống dòng: Mã code C
            p2_code = tf1.add_paragraph()
            p2_code.space_before = 0
            p2_code.space_after = Pt(1.0)
            p2_code.line_spacing = 1.0
            r2_code = p2_code.add_run()
            r2_code.text = "  " + r["c_code"]
            r2_code.font.name = "Consolas"
            r2_code.font.size = Pt(6.8)
            r2_code.font.bold = True
            r2_code.font.color.rgb = RGBColor(15, 23, 42)

            # Cột 2: Ý nghĩa thao tác
            c2 = tbl.cell(row_idx, 2)
            c2.fill.solid()
            c2.fill.fore_color.rgb = row_bg
            c2.vertical_anchor = MSO_ANCHOR.MIDDLE
            c2.margin_left = Inches(0.06)
            c2.margin_right = Inches(0.06)
            c2.margin_top = Inches(0.01)
            c2.margin_bottom = Inches(0.01)
            tf2 = c2.text_frame
            tf2.word_wrap = True

            p3 = tf2.paragraphs[0]
            p3.space_before = 0
            p3.space_after = 0
            p3.line_spacing = 1.04
            r3_text = p3.add_run()
            r3_text.text = r["meaning"]
            r3_text.font.name = "Segoe UI"
            r3_text.font.size = Pt(7.2)
            r3_text.font.color.rgb = C_TEXT_DARK

        return slide'''

start_f = "    def add_bus_table_slide(slide_num, title, rows_data):"
end_f = "    # Helper: Slide chi tiết cho từng trường hợp bus"
sf_idx = code.find(start_f)
ef_idx = code.find(end_f)
code = code[:sf_idx] + new_table_func + "\n\n" + code[ef_idx:]

with open(pres_path, "w", encoding="utf-8") as f:
    f.write(code)

print("[SUCCESS] Updated add_bus_table_slide with newline titles in create_presentation.py")

# =============================================================================
# 2. UPDATE GENERATE_REPORT_DOCX.PY (TABLE 2)
# =============================================================================
docx_path = os.path.join(cur_dir, "generate_report_docx.py")
with open(docx_path, "r", encoding="utf-8") as f:
    dcode = f.read()

# In docx, update the row rendering in Table 2
old_cell_code = '''        # Cột 1: Cấu hình RTL & Code C in rõ ràng
        c1 = t2.cell(row_num, 1)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(1.5)
        p1.paragraph_format.space_after = Pt(1.5)
        p1.paragraph_format.line_spacing = 1.05
        r1_lbl = p1.add_run("• Mã RTL:\\n")
        r1_lbl.bold = True
        set_font(r1_lbl, size=8.5, bold=True, color=RGBColor(30, 58, 138))
        r1_code = p1.add_run(r["rtl_code"])
        set_font(r1_code, size=7.8, bold=True, name="Consolas", color=BLACK)

        p2 = c1.add_paragraph()
        p2.paragraph_format.space_before = Pt(1.5)
        p2.paragraph_format.space_after = Pt(1.5)
        p2.paragraph_format.line_spacing = 1.05
        r2_lbl = p2.add_run("• Mã C / Linker:\\n")
        r2_lbl.bold = True
        set_font(r2_lbl, size=8.5, bold=True, color=RGBColor(21, 128, 61))
        r2_code = p2.add_run(r["c_code"])
        set_font(r2_code, size=7.8, bold=True, name="Consolas", color=BLACK)'''

new_cell_code = '''        # Cột 1: Cấu hình RTL & Code C in rõ ràng: Tiêu đề -> Xuống dòng -> Code
        c1 = t2.cell(row_num, 1)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(1.0)
        p1.paragraph_format.space_after = Pt(0.5)
        p1.paragraph_format.line_spacing = 1.0
        r1_lbl = p1.add_run("• Tiêu đề RTL:\\n")
        r1_lbl.bold = True
        set_font(r1_lbl, size=8.5, bold=True, color=RGBColor(30, 58, 138))
        
        p1_code = c1.add_paragraph()
        p1_code.paragraph_format.space_before = Pt(0)
        p1_code.paragraph_format.space_after = Pt(2.0)
        p1_code.paragraph_format.line_spacing = 1.02
        r1_code = p1_code.add_run(r["rtl_code"])
        set_font(r1_code, size=7.8, bold=True, name="Consolas", color=BLACK)

        p2 = c1.add_paragraph()
        p2.paragraph_format.space_before = Pt(1.0)
        p2.paragraph_format.space_after = Pt(0.5)
        p2.paragraph_format.line_spacing = 1.0
        r2_lbl = p2.add_run("• Tiêu đề Firmware C / Linker:\\n")
        r2_lbl.bold = True
        set_font(r2_lbl, size=8.5, bold=True, color=RGBColor(21, 128, 61))
        
        p2_code = c1.add_paragraph()
        p2_code.paragraph_format.space_before = Pt(0)
        p2_code.paragraph_format.space_after = Pt(1.5)
        p2_code.paragraph_format.line_spacing = 1.02
        r2_code = p2_code.add_run(r["c_code"])
        set_font(r2_code, size=7.8, bold=True, name="Consolas", color=BLACK)'''

if old_cell_code in dcode:
    dcode = dcode.replace(old_cell_code, new_cell_code)
    with open(docx_path, "w", encoding="utf-8") as f:
        f.write(dcode)
    print("[SUCCESS] Updated Table 2 cell formatting in generate_report_docx.py")
else:
    print("[NOTE] Searching regex for Table 2 cell formatting in generate_report_docx.py")
    dcode = re.sub(
        r'        # Cột 1: Cấu hình RTL & Code C in rõ ràng.*?'
        r'set_font\(r2_code, size=7\.8, bold=True, name="Consolas", color=BLACK\)',
        new_cell_code,
        dcode,
        flags=re.DOTALL
    )
    with open(docx_path, "w", encoding="utf-8") as f:
        f.write(dcode)
    print("[SUCCESS] Regex replaced Table 2 cell formatting in generate_report_docx.py")
