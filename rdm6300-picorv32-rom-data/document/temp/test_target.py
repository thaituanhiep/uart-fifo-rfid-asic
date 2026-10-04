# Script to update generate_report_docx.py with 8 dedicated pages for the 8 bus cases
import sys

with open("generate_report_docx.py", "r", encoding="utf-8") as f:
    content = f.read()

# Verify that key targets exist
target_table_end = """    col_w2 = [Inches(1.85), Inches(4.80)]
    col_a2 = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    style_table(t2, col_w2, col_a2, font_size=10.0)
    add_caption("Bảng 2. Bảng phân tích chu kỳ bus thực tế: Đối chiếu thiết lập giải mã RTL, định nghĩa code C và ý nghĩa biến địa chỉ")"""

if target_table_end not in content:
    print("[ERROR] target_table_end not found!")
    sys.exit(1)

print("[INFO] target_table_end found successfully.")
