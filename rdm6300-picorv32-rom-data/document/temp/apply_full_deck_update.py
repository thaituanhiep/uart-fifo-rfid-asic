# -*- coding: utf-8 -*-
"""
apply_full_deck_update.py
Rebuilds create_presentation.py to focus strictly on slides:
1. TOTAL_SLIDES = 17
2. Updates Slide 2 (Agenda)
3. Removes Slide 6 (Phần 4: Tổng quan kiến trúc 1 Master - 5 Slaves)
4. Slide 6: Block Diagram SoC PicoRV32 (Draw.io đen trắng)
5. Slide 7: Các File Code Cấu Hình Hệ Thống Chạy Firmware C (4 box code tối ưu font size)
6. Slide 8: Khối Liên Kết Bus soc_interconnect.v (Draw.io diagram)
7. Slide 9: Cơ Chế Kích Hoạt & Điều Phối Thực Thi Firmware C (4 bước)
8. Slide 10: Bảng Đối Chiếu 3 Cột (Master Roadmap 8 chu kỳ bus thực tế)
9. Removes Slides 12-19 (8 slide chi tiết từng case của Phần 6)
10. Slides 11-17: Testbenches, Demo FPGA, ASIC OpenLane 2, Tổng kết.
"""

import os
import re

cur_dir = os.path.dirname(os.path.abspath(__file__))
pres_path = os.path.join(cur_dir, "create_presentation.py")

with open(pres_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update TOTAL_SLIDES = 17
content = re.sub(r'TOTAL_SLIDES\s*=\s*\d+', 'TOTAL_SLIDES = 17', content)

# 2. Update Slide 2 (Agenda)
old_agenda_pattern = re.compile(r'    agenda_items = \[.*?\n    \]', re.DOTALL)
new_agenda = '''    agenda_items = [
        ("Phần 1: Giới Thiệu Dự Án", "Thiết bị kiểm soát ra vào offline, lý do chọn SPI Flash NVM."),
        ("Phần 2: Lựa Chọn Phần Cứng", "Bo mạch FPGA Basys 3 (Artix-7 XC7A35T) & Đầu đọc RFID RDM6300."),
        ("Phần 3: Lựa Chọn Phần Mềm", "Vivado 2025.1, OpenLane 2 (Sky130A), RISC-V GCC & Host Console C."),
        ("Phần 4: Block Diagram SoC", "Sơ đồ khối kiến trúc vi hệ thống SoC PicoRV32 (B&W Draw.io)."),
        ("Phần 5: Code Cấu Hình & Bus", "Code cấu hình chạy Firmware C, giải mã soc_interconnect.v & cơ chế XIP."),
        ("Phần 6: Bảng Đối Chiếu Bus & C", "Master Roadmap 3 cột đối chiếu 8 chu kỳ bus thực tế, mã RTL & C."),
        ("Phần 7: Hệ Thống Testbench", "Mô phỏng tb_uart_rtl.v (RTL thuần) và tb_uart_ping.v (Top SoC Boot Flash)."),
        ("Phần 8: Demo Thực Nghiệm", "Tạo mẫu Basys 3 FPGA, giao tiếp UART PC và quẹt thẻ RFID thật."),
        ("Phần 9: Thiết Kế Vật Lý ASIC", "OpenLane 2 RTL-to-GDSII: Sign-off 0 DRC, 0 LVS, 0 Antenna, MET TIMING.")
    ]'''
content = old_agenda_pattern.sub(new_agenda, content, count=1)

# Helper function to add a nice code box with a header banner
code_box_helper = '''
    # Helper: Khung hiển thị code chuyên nghiệp với Header Bar
    def add_syntax_box(slide, left, top, width, height, title_text, code_lines, header_bg=C_NAVY_DARK, note_text=None):
        # Background Card
        card = add_card(slide, left, top, width, height, bg_color=RGBColor(248, 250, 252), border_color=header_bg, border_width=1.2)
        
        # Header Badge
        header_h = Inches(0.32)
        h_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, header_h)
        h_box.fill.solid()
        h_box.fill.fore_color.rgb = header_bg
        h_box.line.fill.background()
        tf_h = h_box.text_frame
        tf_h.margin_left = Inches(0.12)
        tf_h.margin_top = Inches(0.04)
        p_h = tf_h.paragraphs[0]
        p_h.text = title_text
        p_h.font.name = "Segoe UI"
        p_h.font.size = Pt(8.5)
        p_h.font.bold = True
        p_h.font.color.rgb = C_WHITE
        
        # Code Text Area
        code_top = top + header_h + Inches(0.05)
        code_h = height - header_h - (Inches(0.35) if note_text else Inches(0.08))
        tb_c = slide.shapes.add_textbox(left + Inches(0.10), code_top, width - Inches(0.20), code_h)
        tf_c = tb_c.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
        
        for li, line in enumerate(code_lines):
            p = tf_c.paragraphs[0] if li == 0 else tf_c.add_paragraph()
            p.text = line
            p.font.name = "Consolas"
            p.font.size = Pt(7.8)
            p.font.bold = True
            if line.strip().startswith("//") or line.strip().startswith("/*") or line.strip().startswith("*") or line.strip().startswith("#"):
                p.font.color.rgb = RGBColor(100, 116, 139) # Comment color
            elif "parameter" in line or "assign" in line or "MEMORY" in line or "SECTIONS" in line or "#define" in line:
                p.font.color.rgb = RGBColor(30, 58, 138) # Keyword color
            else:
                p.font.color.rgb = RGBColor(15, 23, 42) # Normal code color
            p.line_spacing = 1.05
            p.space_after = 0
            
        # Optional bottom note
        if note_text:
            note_top = top + height - Inches(0.30)
            tb_n = slide.shapes.add_textbox(left + Inches(0.12), note_top, width - Inches(0.24), Inches(0.26))
            tf_n = tb_n.text_frame
            tf_n.margin_left = tf_n.margin_right = tf_n.margin_top = tf_n.margin_bottom = 0
            p_n = tf_n.paragraphs[0]
            p_n.text = note_text
            p_n.font.name = "Segoe UI"
            p_n.font.size = Pt(7.5)
            p_n.font.italic = True
            p_n.font.color.rgb = RGBColor(71, 85, 105)
'''

# Insert code_box_helper before add_header or after helper functions
if "def add_syntax_box" not in content:
    content = content.replace("    def add_bus_table_slide", code_box_helper + "\n    def add_bus_table_slide")

# 3. Replace the entire middle design section (from SLIDE 6 to end of SLIDE 19)
# Current structure from:
# # SLIDE 6: PHẦN 4 - TỔNG QUAN KIẾN TRÚC SOC PICORV32
# down to:
# end of SLIDE 19 (before # SLIDE 20: PHẦN 7 - HỆ THỐNG TESTBENCH)

pattern_middle = re.compile(
    r'    # =========================================================================\n'
    r'    # SLIDE 6: PHẦN 4 - TỔNG QUAN KIẾN TRÚC SOC PICORV32.*?'
    r'(?=    # =========================================================================\n'
    r'    # SLIDE 20: PHẦN 7 - HỆ THỐNG TESTBENCH)',
    re.DOTALL
)

new_middle_section = '''    # =========================================================================
    # SLIDE 6: PHẦN 4 - BLOCK DIAGRAM KIẾN TRÚC SOC PICORV32 (B&W DRAW.IO)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Phần 4: Sơ Đồ Khối Kiến Trúc", "Sơ Đồ Khối Kiến Trúc Vi Hệ Thống SoC PicoRV32 (Block Diagram Đen Trắng)", 6, total_slides=TOTAL_SLIDES)

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
        p = tf_b6.add_paragraph()
        p.text = f"• {p_lbl} {p_val}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(6)
        p.line_spacing = 1.15

    # =========================================================================
    # SLIDE 7: PHẦN 5 - CÁC FILE CODE CẤU HÌNH HỆ THỐNG CHẠY FIRMWARE C (4 KHUNG CODE)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Phần 5: Cấu Hình Phần Cứng & Khởi Động Firmware", 
               "Các File Code Cấu Hình Hệ Thống Để Chạy Firmware C (Khớp Nối Co-Design)", 7, total_slides=TOTAL_SLIDES)

    # Box 1: RTL Top SoC (Top Left)
    code_soc = [
        "// rtl/rdm6300_picorv32_soc.v - Tham số cấu hình lõi CPU PicoRV32",
        "parameter [31:0] PROGADDR_RESET = 32'h0025_0000; // Reset Vector Flash XIP",
        "parameter [31:0] STACKADDR      = 32'h0000_0400; // Đỉnh ngăn xếp 1KB SRAM",
        "parameter [0:0]  COMPRESSED_ISA = 1;              // Hỗ trợ tập lệnh RV32IC",
        "wire mem_valid, mem_ready; wire [31:0] mem_addr, mem_wdata, mem_rdata;"
    ]
    add_syntax_box(s7, Inches(0.8), Inches(1.22), Inches(5.75), Inches(2.35),
                   "RTL TOP SOC: rtl/rdm6300_picorv32_soc.v", code_soc, header_bg=RGBColor(30, 58, 138),
                   note_text="-> Thiết lập điểm vào thực thi tại 0x0025_0000 và trỏ đỉnh Stack vào SRAM 1KB.")

    # Box 2: Linker Script (Top Right)
    code_lds = [
        "/* firmware/sections.lds - Phân bổ bộ nhớ Linker Script */",
        "MEMORY {",
        "    FLASH (rx) : ORIGIN = 0x00250000, LENGTH = 0x000B0000 /* 704KB */",
        "    RAM (rwx)  : ORIGIN = 0x00000000, LENGTH = 0x00000400 /* 1KB */",
        "}",
        ".text : { *(.text.start) *(.text*) } > FLASH",
        "_stack_top = 0x00000400; /* Trùng khớp STACKADDR của phần cứng */"
    ]
    add_syntax_box(s7, Inches(6.783), Inches(1.22), Inches(5.75), Inches(2.35),
                   "LINKER SCRIPT: firmware/sections.lds", code_lds, header_bg=RGBColor(21, 128, 61),
                   note_text="-> Định vị toàn bộ mã C vào Flash XIP, giải phóng 100% SRAM cho Stack.")

    # Box 3: RTL Interconnect (Bottom Left)
    code_ic = [
        "// rtl/core/soc_interconnect.v - Logic giải mã Bus Interconnect (0-delay)",
        "assign sel_sram   = cpu_mem_valid && (cpu_mem_addr < 32'h0000_0400);",
        "assign sel_spimem = cpu_mem_valid && (cpu_mem_addr >= 32'h0010_0000 &&",
        "                                      cpu_mem_addr <  32'h0100_0000);",
        "assign sel_spicfg = cpu_mem_valid && (cpu_mem_addr == 32'h0200_0000);",
        "assign sel_rfid   = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h1);",
        "assign sel_uart   = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h3);",
        "assign sel_gpio   = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h4);"
    ]
    add_syntax_box(s7, Inches(0.8), Inches(3.68), Inches(5.75), Inches(2.45),
                   "RTL BUS INTERCONNECT: rtl/core/soc_interconnect.v", code_ic, header_bg=C_BLUE_ACCENT,
                   note_text="-> Phân phối dải Flash XIP, SRAM 1KB và các thanh ghi MMIO ngoại vi.")

    # Box 4: Bootstrap & MMIO (Bottom Right)
    code_boot = [
        "/* firmware/start.s - Thiết lập Stack & Nhảy vào hàm main() C */",
        "_start: lui  sp, %hi(_stack_top)       # sp = 0x00000400 (Đỉnh SRAM)",
        "        addi sp, sp, %lo(_stack_top)  # Khởi tạo con trỏ ngăn xếp",
        "        call main                     # Chuyển quyền điều khiển sang C",
        "/* firmware/common/soc_regs.h - Định nghĩa con trỏ thanh ghi MMIO */",
        "#define REG_RFID_UART_DIV (*(volatile uint32_t*)0x10000000)",
        "#define REG_RFID_UART_DAT (*(volatile uint32_t*)0x10000004)",
        "#define REG_GPIO_LEDS     (*(volatile uint32_t*)0x40000000)"
    ]
    add_syntax_box(s7, Inches(6.783), Inches(3.68), Inches(5.75), Inches(2.45),
                   "BOOTSTRAP & MMIO: firmware/start.s & common/soc_regs.h", code_boot, header_bg=RGBColor(71, 85, 105),
                   note_text="-> Nhảy vào C và cho phép hàm C truy xuất thanh ghi ngoại vi qua con trỏ volatile.")

    # Bottom Summary Callout Banner
    banner_box = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.22), Inches(11.733), Inches(0.68))
    banner_box.fill.solid()
    banner_box.fill.fore_color.rgb = RGBColor(239, 246, 255) # Light blue
    banner_box.line.color.rgb = C_BLUE_ACCENT
    banner_box.line.width = Pt(1.5)
    tf_ban = banner_box.text_frame
    tf_ban.word_wrap = True
    tf_ban.margin_left = Inches(0.12)
    tf_ban.margin_top = Inches(0.04)
    tf_ban.margin_bottom = Inches(0.04)
    p_b1 = tf_ban.paragraphs[0]
    p_b1.text = "CƠ CHẾ ĐỒNG THIẾT KẾ PHẦN CỨNG - PHẦN MỀM (HARDWARE / SOFTWARE CO-DESIGN)"
    p_b1.font.name = "Segoe UI"
    p_b1.font.size = Pt(8.5)
    p_b1.font.bold = True
    p_b1.font.color.rgb = RGBColor(30, 58, 138)
    p_b1.space_after = Pt(1)

    p_b2 = tf_ban.add_paragraph()
    p_b2.text = "• Reset Vector: PROGADDR_RESET (RTL) = ORIGIN FLASH (Linker) = 0x0025_0000 -> CPU thực thi XIP từ Flash SPI ngoài mà không cần ROM nạp trung gian.\\n• Ngăn Xếp: STACKADDR (RTL) = _stack_top (ASM) = 0x0000_0400 -> Stack RAM 1KB phản hồi zero-wait-state trong đúng 1 chu kỳ clock."
    p_b2.font.name = "Segoe UI"
    p_b2.font.size = Pt(7.8)
    p_b2.font.color.rgb = RGBColor(15, 23, 42)
    p_b2.line_spacing = 1.05

    # =========================================================================
    # SLIDE 8: PHẦN 5 - KHỐI LIÊN KẾT BUS SOC_INTERCONNECT.V (DRAW.IO DIAGRAM)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Phần 5: Khối Liên Kết Bus", "Khối soc_interconnect.v - Cầu Nối CPU, Flash XIP, SRAM & Ngoại Vi MMIO", 8, total_slides=TOTAL_SLIDES)

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
    add_header(s9, "Phần 5: Khối Liên Kết Bus", "Cơ Chế Kích Hoạt Và Điều Phối Thực Thi Firmware C Trên Phần Cứng", 9, total_slides=TOTAL_SLIDES)

    exec_steps = [
        ("BƯỚC 1: BOOT XIP TỪ FLASH", C_BLUE_ACCENT, [
            ("Vector Reset:", "PROGADDR_RESET = 0x0025_0000 nằm trong dải Flash XIP."),
            ("Tự động giải mã:", "soc_interconnect bật sel_spimem, spimemio phát lệnh đọc kéo mã máy từ Flash ngoài."),
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
    # SLIDE 10: PHẦN 6 - BẢNG ĐỐI CHIẾU CHU KỲ BUS THỰC TẾ (MASTER ROADMAP 3 CỘT)
    # =========================================================================
    all_rows_bus = [
        {
            "time": "T = 0",
            "task": "(Boot Flash XIP)",
            "rtl_file": "[rdm6300_picorv32_soc.v & soc_interconnect.v]",
            "rtl_code": "parameter [31:0] PROGADDR_RESET = 32'h0025_0000; | assign sel_spimem = cpu_mem_valid && (cpu_mem_addr >= 32'h0010_0000 && cpu_mem_addr < 32'h0100_0000);",
            "c_file": "[sections.lds & start.s]",
            "c_code": "FLASH (rx) : ORIGIN = 0x00250000, LENGTH = 0x000B0000 | _start: lui sp, %hi(_stack_top)",
            "meaning": "Cấu hình vector reset trỏ thẳng vào Flash SPI để CPU tự động nạp và thực thi trực tiếp opcode firmware (XIP) ngay sau khi nhả reset mà không cần nạp vào RAM."
        },
        {
            "time": "T = 1..100",
            "task": "(Tạo Stack RAM)",
            "rtl_file": "[rdm6300_picorv32_soc.v & soc_interconnect.v]",
            "rtl_code": "parameter [31:0] STACKADDR = 32'h0000_0400; | assign sel_sram = cpu_mem_valid && (cpu_mem_addr < 32'h0000_0400); assign sram_ready = 1'b1;",
            "c_file": "[sections.lds & start.s]",
            "c_code": "RAM (rwx) : ORIGIN = 0x00000000, LENGTH = 0x00000400 | lui sp, %hi(_stack_top); addi sp, sp, %lo(_stack_top);",
            "meaning": "C sử dụng không gian SRAM 1KB (< 0x0400) qua con trỏ ngăn xếp sp để cấp phát biến cục bộ, lưu stack frame và địa chỉ trả về hàm, phản hồi tức thì trong 1 chu kỳ clock."
        },
        {
            "time": "T = 101",
            "task": "(Vào hàm main)",
            "rtl_file": "[soc_interconnect.v]",
            "rtl_code": "assign sel_spimem = cpu_mem_valid && (cpu_mem_addr >= 32'h0010_0000 && ...); | assign cpu_mem_rdata = sel_spimem ? spimem_rdata : ...;",
            "c_file": "[start.s & main.c]",
            "c_code": "call main; | int main(void) { access_control_init(); while (1) access_control_poll(); }",
            "meaning": "Chuyển giao quyền điều khiển từ assembly khởi động sang code C bậc cao. Hàm main() chạy trực tiếp từ Flash XIP, giải phóng toàn bộ 1KB SRAM chỉ dùng cho dữ liệu động."
        },
        {
            "time": "T = 105",
            "task": "(Set Baud Dual UART)",
            "rtl_file": "[soc_interconnect.v & uart_mmio.v]",
            "rtl_code": "assign sel_rfid = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h1); | if (reg_div_sel && |cpu_mem_wstrb) uart_div <= cpu_mem_wdata;",
            "c_file": "[soc_regs.h & access_control.c]",
            "c_code": "#define REG_RFID_UART_DIV (*(volatile uint32_t*)0x10000000) | REG_RFID_UART_DIV = 5208; // 50 MHz / 9600 Baud",
            "meaning": "C ghi giá trị chia tần 5208 vào địa chỉ 0x10000000 và 0x30000000 để cài đặt tốc độ baud 9600 bps cho cả đầu đọc RFID RDM6300 và cổng máy tính PC (50 MHz / 9600)."
        },
        {
            "time": "T = 200",
            "task": "(Đọc thẻ RFID)",
            "rtl_file": "[uart_mmio.v & simpleuart_fifo.v]",
            "rtl_code": "wire reg_dat_sel = valid && (addr[2] == 1'b1); | assign reg_dat_do = fifo_empty ? 32'hFFFFFFFF : {24'd0, fifo_dout};",
            "c_file": "[soc_regs.h & access_control.c]",
            "c_code": "#define REG_RFID_UART_DAT (*(volatile uint32_t*)0x10000004) | uint32_t d = REG_RFID_UART_DAT; if (d != 0xFFFFFFFF) rdm6300_push(d);",
            "meaning": "C đọc từ 0x10000004 rút (pop) 1 byte từ FIFO 32B (đọc không khóa: trả về byte mã thẻ nếu có, hoặc trả về 0xFFFFFFFF nếu FIFO rỗng để CPU không bị nghẽn bus)."
        },
        {
            "time": "T = 250",
            "task": "(Giao tiếp PC UART)",
            "rtl_file": "[soc_interconnect.v & uart_mmio.v]",
            "rtl_code": "assign sel_uart = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h3); | wire dat_we = reg_dat_sel && (|wstrb); // Write TX FIFO",
            "c_file": "[soc_regs.h & uart.c]",
            "c_code": "#define REG_PC_UART_DAT (*(volatile uint32_t*)0x30000004) | REG_PC_UART_DAT = c; /* Ghi TX */ | d = REG_PC_UART_DAT; /* Doc RX */",
            "meaning": "C ghi byte vào 0x30000004 để đẩy ký tự vào TX FIFO truyền lên Host PC, và đọc từ địa chỉ này để nhận chuỗi lệnh quản trị (Ping, thêm/xóa thẻ Whitelist, xuất log CSV)."
        },
        {
            "time": "T = 300",
            "task": "(Bật LED / Mở Cửa)",
            "rtl_file": "[soc_interconnect.v & soc_gpio_mmio.v]",
            "rtl_code": "assign sel_gpio = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h4); | if (sel_gpio && |wstrb) gpio_led_reg[7:0] <= wdata[7:0];",
            "c_file": "[soc_regs.h & access_control.c]",
            "c_code": "#define REG_GPIO_LEDS (*(volatile uint32_t*)0x40000000) | REG_GPIO_LEDS = (REG_GPIO_LEDS & ~0x0002) | 0x04; // Bit 2: Granted",
            "meaning": "C ghi giá trị bitmask vào 0x40000000 điều khiển 16 LED chẩn đoán trên bo mạch và đóng/ngắt relay mở chốt cửa điện từ (Bit 0: Alive 1Hz, Bit 1: Denied, Bit 2: Granted)."
        },
        {
            "time": "T = 400",
            "task": "(Ghi Flash từ RAM)",
            "rtl_file": "[soc_interconnect.v & spimemio.v]",
            "rtl_code": "assign sel_spicfg = cpu_mem_valid && (cpu_mem_addr == 32'h0200_0000); | .cfgreg_we(sel_spicfg ? mem_wstrb : 4'b0000)",
            "c_file": "[start.s & flash.c]",
            "c_code": "flashio_worker: li t0, 0x02000000; sh t1, 0(t0); | static void flashio(uint8_t *data, int len, uint8_t wrencmd);",
            "meaning": "Khi chạy từ SRAM, hàm của C phát lệnh bit-bang SPI vào 0x02000000 để xóa sector và ghi dữ liệu thẻ mới vào Flash Whitelist / Log mà không gây xung đột bus với các lệnh XIP."
        }
    ]
    s10 = add_bus_table_slide(10, "Bảng Đối Chiếu 8 Chu Kỳ Bus Thực Tế: Setting RTL, Code C & Ý Nghĩa Biến Địa Chỉ", all_rows_bus)
'''

if pattern_middle.search(content):
    content = pattern_middle.sub(new_middle_section, content, count=1)
    print("[SUCCESS] Replaced middle design section with focused slides")
else:
    print("[ERROR] pattern_middle not found")

# 4. Now update slide numbers from Slide 20 onwards (which will now be Slide 11 to 17)
# Let's map old slide numbers to new slide numbers:
# Slide 20 -> Slide 11
# Slide 21 -> Slide 12
# Slide 22 -> Slide 13
# Slide 23 -> Slide 14
# Slide 24 -> Slide 15
# Slide 25 -> Slide 16
# Slide 26 -> Slide 17

content = content.replace('add_header(s20, "Phần 7: Hệ Thống Testbench", "Testbench 1: Kiểm Thử Phần Cứng RTL Thuần Cho UART MMIO & FIFO (tb_uart_rtl.v)", 20)',
                          'add_header(s20, "Phần 7: Hệ Thống Testbench", "Testbench 1: Kiểm Thử Phần Cứng RTL Thuần Cho UART MMIO & FIFO (tb_uart_rtl.v)", 11, total_slides=TOTAL_SLIDES)')

content = content.replace('add_header(s21, "Phần 7: Hệ Thống Testbench", "Testbench 2: Mô Phỏng Toàn Diện Top SoC PicoRV32 Boot Flash & Ping (tb_uart_ping.v)", 21)',
                          'add_header(s21, "Phần 7: Hệ Thống Testbench", "Testbench 2: Mô Phỏng Toàn Diện Top SoC PicoRV32 Boot Flash & Ping (tb_uart_ping.v)", 12, total_slides=TOTAL_SLIDES)')

content = content.replace('add_header(s22, "Phần 8: Demo Thực Nghiệm FPGA", "Mô Hình Demo Thực Nghiệm Trên Bo Mạch Xilinx Artix-7 Basys 3", 22)',
                          'add_header(s22, "Phần 8: Demo Thực Nghiệm FPGA", "Mô Hình Demo Thực Nghiệm Trên Bo Mạch Xilinx Artix-7 Basys 3", 13, total_slides=TOTAL_SLIDES)')

content = content.replace('add_header(s23, "Phần 8: Demo Thực Nghiệm FPGA", "Kết Quả Thực Nghiệm Các Kịch Bản Kiểm Soát Ra Vào Offline & Host PC", 23)',
                          'add_header(s23, "Phần 8: Demo Thực Nghiệm FPGA", "Kết Quả Thực Nghiệm Các Kịch Bản Kiểm Soát Ra Vào Offline & Host PC", 14, total_slides=TOTAL_SLIDES)')

content = content.replace('add_header(s24, "Phần 9: Thiết Kế Vật Lý ASIC", "Quy Trình Thiết Kế Vật Lý Tự Động Với OpenLane 2 (Tiến Trình SkyWater 130nm)", 24)',
                          'add_header(s24, "Phần 9: Thiết Kế Vật Lý ASIC", "Quy Trình Thiết Kế Vật Lý Tự Động Với OpenLane 2 (Tiến Trình SkyWater 130nm)", 15, total_slides=TOTAL_SLIDES)')

content = content.replace('add_header(s25, "Phần 9: Thiết Kế Vật Lý ASIC", "Bản Vẽ Layout Vi Mạch ASIC & Kết Quả Sign-off Tape-out Chuẩn Công Nghiệp", 25)',
                          'add_header(s25, "Phần 9: Thiết Kế Vật Lý ASIC", "Bản Vẽ Layout Vi Mạch ASIC & Kết Quả Sign-off Tape-out Chuẩn Công Nghiệp", 16, total_slides=TOTAL_SLIDES)')

content = content.replace('add_header(s26, "Phần 10: Tổng Kết & Phát Triển", "Tổng Kết Đóng Góp Của Đề Tài & Định Hướng Nghiên Cứu Phát Triển", 26)',
                          'add_header(s26, "Phần 10: Tổng Kết & Phát Triển", "Tổng Kết Đóng Góp Của Đề Tài & Định Hướng Nghiên Cứu Phát Triển", 17, total_slides=TOTAL_SLIDES)')

# Update Slide 1, 2, 3, 4, 5 headers to use total_slides=TOTAL_SLIDES
content = content.replace('add_header(s2, "Tổng Quan Báo Cáo", "Nội Dung Báo Cáo Đồ Án (9 Phần Chuẩn Mực)", 2)',
                          'add_header(s2, "Tổng Quan Báo Cáo", "Nội Dung Báo Cáo Đồ Án (9 Phần Chuẩn Mực)", 2, total_slides=TOTAL_SLIDES)')
content = content.replace('add_header(s3, "Phần 1: Giới Thiệu Dự Án", "Thiết Bị Kiểm Soát Ra Vào Offline & Lý Do Lựa Chọn SPI Flash", 3)',
                          'add_header(s3, "Phần 1: Giới Thiệu Dự Án", "Thiết Bị Kiểm Soát Ra Vào Offline & Lý Do Lựa Chọn SPI Flash", 3, total_slides=TOTAL_SLIDES)')
content = content.replace('add_header(s4, "Phần 2: Lựa Chọn Phần Cứng", "Lựa Chọn Nền Tảng Phần Cứng: FPGA Basys 3 & Module RFID RDM6300", 4)',
                          'add_header(s4, "Phần 2: Lựa Chọn Phần Cứng", "Lựa Chọn Nền Tảng Phần Cứng: FPGA Basys 3 & Module RFID RDM6300", 4, total_slides=TOTAL_SLIDES)')
content = content.replace('add_header(s5, "Phần 3: Lựa Chọn Phần Mềm", "Chuỗi Công Cụ Phát Triển: FPGA, ASIC OpenLane 2 & Toolchain Nhúng", 5)',
                          'add_header(s5, "Phần 3: Lựa Chọn Phần Mềm", "Chuỗi Công Cụ Phát Triển: FPGA, ASIC OpenLane 2 & Toolchain Nhúng", 5, total_slides=TOTAL_SLIDES)')

with open(pres_path, "w", encoding="utf-8") as f:
    f.write(content)

print("[SUCCESS] Rebuilt create_presentation.py to 17 focused slides")
