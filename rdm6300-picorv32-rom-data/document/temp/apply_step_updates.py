# -*- coding: utf-8 -*-
"""
apply_step_updates.py
Implements the 3 requested updates:
1. Block diagram cũ, không có code: Restores fig1_block_diagram.png from fig1_block_diagram_backup.png.
2. Show code RTL những đoạn cấu hình firmware trong 1 trang slide (Slide 10) và 1 trang docx (Mục 6.1.1).
3. Show bảng 2 cột chúng ta vừa làm (Slide 11 & Bảng 2 Mục 6.2).
"""

import os
import shutil
import re

cur_dir = os.path.dirname(os.path.abspath(__file__))
doc_dir = os.path.dirname(cur_dir) if os.path.basename(cur_dir) == "temp" else cur_dir
project_root = os.path.dirname(doc_dir)

# =============================================================================
# 1. RESTORE BLOCK DIAGRAM CŨ, KHÔNG CÓ CODE
# =============================================================================
backup_png = os.path.join(cur_dir, "fig1_block_diagram_backup.png")
if os.path.exists(backup_png):
    target_pngs = [
        os.path.join(cur_dir, "fig1_block_diagram.png"),
        os.path.join(doc_dir, "fig1_block_diagram.png"),
        os.path.join(project_root, "fig1_block_diagram.png"),
        r"C:\Users\thait\.gemini\antigravity-ide\brain\40d01579-3c16-4b85-9b12-c0e7d33bcd21\fig1_soc_block_diagram.png"
    ]
    for p in target_pngs:
        try:
            shutil.copyfile(backup_png, p)
            print(f"[SUCCESS] Restored clean block diagram: {p}")
        except Exception as e:
            print(f"[WARN] Could not copy to {p}: {e}")

# =============================================================================
# 2. UPDATE CREATE_PRESENTATION.PY (SLIDE 10)
# =============================================================================
pres_path = os.path.join(cur_dir, "create_presentation.py")
with open(pres_path, "r", encoding="utf-8") as f:
    pres_code = f.read()

# Replace Slide 10 content with dedicated RTL Firmware Configuration slide
slide10_old_marker = """    # =========================================================================
    # SLIDE 10: PHẦN 6 - CẦU NỐI MMIO: KHAI BÁO ĐỊA CHỈ SOC_REGS.H VS RTL
    # ========================================================================="""

slide10_new_content = """    # =========================================================================
    # SLIDE 10: PHẦN 6 - CÁC ĐOẠN CODE RTL CẤU HÌNH HỆ THỐNG ĐỂ CHẠY FIRMWARE C
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Phần 6: Cấu Hình Phần Cứng Thực Thi Firmware", "Các Đoạn Code RTL Cấu Hình Hệ Thống Để Chạy Firmware C (Khớp Nối sections.lds)", 10)

    lines_rtl_cfg = [
        "// rtl/rdm6300_picorv32_soc.v - Tham số cấu hình nhân CPU PicoRV32",
        "parameter [31:0] PROGADDR_RESET = 32'h 0025_0000; // Reset vector Flash XIP",
        "parameter [31:0] STACKADDR      = 32'h 0000_0400; // Đỉnh ngăn xếp 1KB SRAM",
        "parameter [0:0]  COMPRESSED_ISA = 1;              // Hỗ trợ tập lệnh nén RVC",
        "parameter [0:0]  ENABLE_COUNTERS = 1;             // Bộ đếm chu kỳ hiệu năng",
        "",
        "// rtl/core/spimemio.v - Bộ điều khiển Flash SPI",
        "parameter [0:0]  FAST_READ      = 1'b1;           // Fast Read Opcode 0x0B",
        "// Flash XIP dải nhớ 4MB: 0x0010_0000 -> 0x00FF_FFFF (chứa firmware)",
        "",
        "// rtl/core/data_sram.v - Bộ nhớ dữ liệu 1KB SRAM nội vi mạch",
        "parameter integer WORDS = 256;                   // 256 từ x 32-bit = 1024 Bytes",
        "assign sram_ready = 1'b1;                        // Zero-wait-state trong 1 clock"
    ]
    add_code_box(s10, Inches(0.8), Inches(1.35), Inches(5.7), Inches(4.3), "rtl/rdm6300_picorv32_soc.v & core modules", lines_rtl_cfg)

    lines_rtl_interconnect_lds = [
        "// rtl/core/soc_interconnect.v - Logic giải mã Bus Interconnect",
        "assign sel_sram   = cpu_mem_valid && (cpu_mem_addr < 32'h0000_0400);",
        "assign sel_spimem = cpu_mem_valid && (cpu_mem_addr >= 32'h0010_0000 &&",
        "                                      cpu_mem_addr <  32'h0100_0000);",
        "assign sel_spicfg = cpu_mem_valid && (cpu_mem_addr == 32'h0200_0000);",
        "assign sel_rfid   = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h1); // 0x1000_0000",
        "assign sel_uart   = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h3); // 0x3000_0000",
        "assign sel_gpio   = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h4); // 0x4000_0000",
        "",
        "/* firmware/sections.lds - Linker Script khớp nối 100% phần cứng */",
        "MEMORY {",
        "    FLASH (rx) : ORIGIN = 0x00250000, LENGTH = 0x000B0000 /* 704 KB Flash */",
        "    RAM (rwx)  : ORIGIN = 0x00000000, LENGTH = 0x00000400 /* 1 KB Data SRAM */",
        "}",
        "_stack_top = 0x00000400; /* Trùng khớp hoàn toàn STACKADDR của phần cứng */"
    ]
    add_code_box(s10, Inches(6.8), Inches(1.35), Inches(5.73), Inches(4.3), "rtl/core/soc_interconnect.v & sections.lds", lines_rtl_interconnect_lds)

    add_card(s10, Inches(0.8), Inches(5.8), Inches(11.733), Inches(1.05), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
    tb_c10 = s10.shapes.add_textbox(Inches(0.95), Inches(5.85), Inches(11.4), Inches(0.95))
    tf_c10 = tb_c10.text_frame
    tf_c10.word_wrap = True
    p_c10_1 = tf_c10.paragraphs[0]
    p_c10_1.text = "TÍNH ĐỒNG BỘ TUYỆT ĐỐI GIỮA THIẾT KẾ PHẦN CỨNG RTL VÀ CHUỖI BIÊN DỊCH C"
    p_c10_1.font.name = "Segoe UI"
    p_c10_1.font.size = Pt(11)
    p_c10_1.font.bold = True
    p_c10_1.font.color.rgb = C_BLUE_ACCENT
    p_c10_1.space_after = Pt(2)

    p_c10_2 = tf_c10.add_paragraph()
    p_c10_2.text = "Tham số RTL PROGADDR_RESET (0x0025_0000) và vùng FLASH trong Linker Script trùng khớp 100%, cho phép CPU thực thi trực tiếp mã máy (XIP) từ Flash SPI ngay sau khi nhả reset. Con trỏ ngăn xếp sp và biến động định vị trong 1KB SRAM (< 0x0400) với phản hồi 1 chu kỳ clock, hoàn toàn không cần bộ nạp ROM trung gian."
    p_c10_2.font.name = "Segoe UI"
    p_c10_2.font.size = Pt(10)
    p_c10_2.font.color.rgb = C_TEXT_DARK"""

# Find Slide 10 in create_presentation.py and replace it
s10_pattern = re.compile(r'    # =========================================================================\s+# SLIDE 10:.*?(?=    # =========================================================================\s+# SLIDE 11:)', re.DOTALL)
if s10_pattern.search(pres_code):
    pres_code = s10_pattern.sub(slide10_new_content + "\n\n", pres_code, count=1)
    with open(pres_path, "w", encoding="utf-8") as f:
        f.write(pres_code)
    print("[SUCCESS] Updated Slide 10 in create_presentation.py")
else:
    print("[WARN] Slide 10 pattern not found in create_presentation.py")

# =============================================================================
# 3. UPDATE GENERATE_REPORT_DOCX.PY (MỤC 6.1.1 DEDICATED PAGE & TOC)
# =============================================================================
docx_script_path = os.path.join(cur_dir, "generate_report_docx.py")
with open(docx_script_path, "r", encoding="utf-8") as f:
    docx_code = f.read()

# Update TOC: add 6.1.1
old_toc_entry = """        ("6.1. Cầu nối phần cứng - phần mềm: Khai báo địa chỉ MMIO trong soc_regs.h vs soc_interconnect.v", "10", False, 0.2),"""
new_toc_entry = """        ("6.1. Cầu nối phần cứng - phần mềm: Khai báo địa chỉ MMIO trong soc_regs.h vs soc_interconnect.v", "10", False, 0.2),
        ("6.1.1. Các đoạn mã RTL cấu hình phần cứng cho phép hệ thống thực thi Firmware C", "11", False, 0.3),"""

if old_toc_entry in docx_code and "6.1.1." not in docx_code.split("toc_items = [")[1].split("]")[0]:
    docx_code = docx_code.replace(old_toc_entry, new_toc_entry)
    print("[SUCCESS] Updated TOC in generate_report_docx.py")

# Add Section 6.1.1 dedicated page before Section 6.2
sec_611_code = '''    # -------------------------------------------------------------
    # 6.1.1. CÁC ĐOẠN MÃ RTL CẤU HÌNH PHẦN CỨNG THỰC THI FIRMWARE C
    # (DEDICATED 1 PAGE TRƯỚC BẢNG 2 CỘT 6.2)
    # -------------------------------------------------------------
    doc.add_page_break()
    add_h2("6.1.1. Các đoạn mã RTL cấu hình phần cứng cho phép hệ thống thực thi Firmware C")
    add_p("Mục này trình bày toàn bộ các đoạn mã nguồn phần cứng Verilog RTL cấu hình thông số kiến trúc để nhân vi xử lý PicoRV32 có thể khởi động và thực thi trơn tru firmware C, đồng thời đối chiếu sự tương thích tuyệt đối với tệp cấu hình bản đồ bộ nhớ Linker Script (firmware/sections.lds):")

    # Bảng tóm tắt thông số cấu hình phần cứng RTL vs Firmware C
    t_cfg = doc.add_table(rows=7, cols=4)
    cfg_headers = ["Tham số phần cứng RTL", "File RTL", "Giá trị thiết lập", "Khớp nối Firmware C / Linker (sections.lds)"]
    for c_idx, h_t in enumerate(cfg_headers):
        t_cfg.cell(0, c_idx).paragraphs[0].text = h_t

    cfg_rows = [
        ("PROGADDR_RESET", "rdm6300_picorv32_soc.v", "32'h0025_0000", "FLASH (rx) : ORIGIN = 0x00250000 (Vector Reset XIP)"),
        ("STACKADDR", "rdm6300_picorv32_soc.v", "32'h0000_0400", "_stack_top = 0x00000400 (Đỉnh ngăn xếp 1KB SRAM)"),
        ("WORDS = 256", "rtl/core/data_sram.v", "1024 Bytes", "RAM (rwx) : LENGTH = 0x00000400 (Vùng biến động & Stack)"),
        ("FAST_READ = 1'b1", "rtl/core/spimemio.v", "Opcode 0x0B", "Fast Read SPI Flash nạp opcode trực tiếp"),
        ("COMPRESSED_ISA = 1", "rtl/core/picorv32.v", "RV32IMC (16-bit)", "Tối ưu hóa mã máy, giảm 30% dung lượng Flash"),
        ("sel_sram / sel_spimem", "rtl/core/soc_interconnect.v", "< 0x0400 / >= 0x0010_0000", "Tách biệt vật lý bộ nhớ mã lệnh (Flash) và dữ liệu (SRAM)")
    ]
    for r_idx, (p_name, p_file, p_val, p_map) in enumerate(cfg_rows):
        row_i = r_idx + 1
        t_cfg.cell(row_i, 0).paragraphs[0].text = p_name
        t_cfg.cell(row_i, 1).paragraphs[0].text = p_file
        t_cfg.cell(row_i, 2).paragraphs[0].text = p_val
        t_cfg.cell(row_i, 3).paragraphs[0].text = p_map

    style_table(t_cfg, [Inches(1.8), Inches(1.5), Inches(1.2), Inches(2.2)], 
                [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT], font_size=8.5)
    add_caption("Bảng 1b. Đối chiếu tham số cấu hình phần cứng Verilog RTL và bản đồ bộ nhớ Linker Script Firmware C")

    p_lbl_rtl1 = add_p("1. Tham số cấu hình CPU PicoRV32, Flash Controller và SRAM (RTL):")
    p_lbl_rtl1.runs[0].bold = True
    add_console_block([
        "// rtl/rdm6300_picorv32_soc.v - Tham số khởi động nhân CPU PicoRV32",
        "parameter [31:0] PROGADDR_RESET = 32'h 0025_0000; // Reset vector Flash XIP",
        "parameter [31:0] STACKADDR      = 32'h 0000_0400; // Đỉnh ngăn xếp 1KB SRAM",
        "parameter [0:0]  COMPRESSED_ISA = 1;              // Hỗ trợ tập lệnh nén RVC",
        "parameter [0:0]  ENABLE_COUNTERS = 1;             // Kích hoạt bộ đếm chu kỳ hiệu năng",
        "",
        "// rtl/core/spimemio.v - Cấu hình bộ điều khiển Flash SPI",
        "parameter [0:0]  FAST_READ      = 1'b1;           // Chế độ đọc nhanh Fast Read (0x0B)",
        "// Dải địa chỉ Flash XIP: 0x0010_0000 - 0x00FF_FFFF (4MB)",
        "",
        "// rtl/core/data_sram.v - Cấu hình bộ nhớ dữ liệu nội vi mạch",
        "parameter integer WORDS = 256;                   // 256 từ x 32-bit = 1024 Bytes",
        "assign sram_ready = 1'b1;                        // Phản hồi tức thì trong 1 chu kỳ clock"
    ])

    p_lbl_rtl2 = add_p("2. Logic giải mã địa chỉ điều phối bus trung tâm (soc_interconnect.v):")
    p_lbl_rtl2.runs[0].bold = True
    add_console_block([
        "// rtl/core/soc_interconnect.v - Bus Decoding Equations",
        "assign sel_sram   = cpu_mem_valid && (cpu_mem_addr < 32'h0000_0400);",
        "assign sel_spimem = cpu_mem_valid && (cpu_mem_addr >= 32'h0010_0000 && cpu_mem_addr < 32'h0100_0000);",
        "assign sel_spicfg = cpu_mem_valid && (cpu_mem_addr == 32'h0200_0000);",
        "assign sel_rfid   = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h1); // 0x1000_0000",
        "assign sel_uart   = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h3); // 0x3000_0000",
        "assign sel_gpio   = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h4); // 0x4000_0000"
    ])

    p_lbl_c = add_p("3. Cấu hình bản đồ bộ nhớ trong Linker Script của Firmware C (firmware/sections.lds):")
    p_lbl_c.runs[0].bold = True
    add_console_block([
        "/* firmware/sections.lds - Linker script khớp nối trực tiếp với phần cứng */",
        "MEMORY {",
        "    FLASH (rx) : ORIGIN = 0x00250000, LENGTH = 0x000B0000 /* 704 KB Flash */",
        "    RAM (rwx)  : ORIGIN = 0x00000000, LENGTH = 0x00000400 /* 1 KB Data SRAM */",
        "}",
        "_stack_top = 0x00000400; /* Trùng khớp STACKADDR của phần cứng */"
    ])

    add_p("Ý nghĩa kỹ thuật và tính tương thích đồng thiết kế:")
    add_p("1. Thực thi tại chỗ (XIP): Bằng cách gán PROGADDR_RESET = 32'h0025_0000 trùng với vùng FLASH ORIGIN trong sections.lds, CPU PicoRV32 lập tức phát lệnh đọc opcode trực tiếp từ chip nhớ ngoài SPI Flash ngay sau khi nhả reset. Cơ chế này loại bỏ hoàn toàn nhu cầu về bộ nhớ ROM nạp trung gian (bootloader ROM) tốn kém diện tích trên vi mạch ASIC.")
    add_p("2. Tối ưu hóa bộ nhớ RAM: Toàn bộ 1024 bytes SRAM (< 0x0400) được dành trọn vẹn cho việc tạo khung ngăn xếp Stack Frame và lưu biến dữ liệu động, phản hồi tức thời trong đúng 1 chu kỳ xung nhịp (zero-wait-state), đảm bảo hiệu năng tính toán thời gian thực.")
'''

# Check if Section 6.1.1 is already inserted
if "6.1.1. Các đoạn mã RTL cấu hình phần cứng" not in docx_code:
    # Insert right before Section 6.2 heading
    target_62_heading = '    # 6.2. BẢNG PHÂN TÍCH CHU KỲ BUS THỰC TẾ: ĐỐI CHIẾU SETTING RTL, CODE C VÀ Ý NGHĨA BIẾN ĐỊA CHỈ\n    add_h2("6.2. Bảng phân tích chu kỳ bus thực tế: Đối chiếu setting RTL, code C và ý nghĩa biến địa chỉ")'
    if target_62_heading in docx_code:
        docx_code = docx_code.replace(target_62_heading, sec_611_code + "\n    # 6.2. BẢNG PHÂN TÍCH CHU KỲ BUS THỰC TẾ: ĐỐI CHIẾU SETTING RTL, CODE C VÀ Ý NGHĨA BIẾN ĐỊA CHỈ\n    add_h2(\"6.2. Bảng phân tích chu kỳ bus thực tế: Đối chiếu setting RTL, code C và ý nghĩa biến địa chỉ\")")
        with open(docx_script_path, "w", encoding="utf-8") as f:
            f.write(docx_code)
        print("[SUCCESS] Added Section 6.1.1 dedicated page to generate_report_docx.py")
    else:
        print("[WARN] target_62_heading not found in generate_report_docx.py")
else:
    print("[INFO] Section 6.1.1 already present in generate_report_docx.py")
