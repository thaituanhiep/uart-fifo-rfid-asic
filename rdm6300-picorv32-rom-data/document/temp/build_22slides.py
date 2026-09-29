# -*- coding: utf-8 -*-
"""
Precise builder for create_presentation.py to generate 22 comprehensive slides.
Inserts Slides 12-17 between Slide 11 and old Slide 12, renumbers old 12-16 to 18-22.
"""

import os
import re

def build():
    script_path = r"c:\Users\HP DRAGONFLY G2\Desktop\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\create_presentation.py"
    with open(script_path, "r", encoding="utf-8") as f:
        src = f.read()

    # 1. Update total_slides=22 in add_header
    src = src.replace("def add_header(slide, category, title, slide_num, total_slides=16):",
                      "def add_header(slide, category, title, slide_num, total_slides=22):")
    src = src.replace("def add_header(slide, category, title, slide_num, total_slides=18):",
                      "def add_header(slide, category, title, slide_num, total_slides=22):")

    # 2. Update paths for images and output
    old_paths = """    cur_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(cur_dir)

    img_fig1 = os.path.join(cur_dir, "fig1_block_diagram.png")
    img_fig2 = os.path.join(cur_dir, "fig2_rdm6300_subsystem.png")
    img_fig2_h = os.path.join(cur_dir, "fig2_rdm6300_horizontal.png")
    img_openroad = os.path.join(root_dir, "Openroad_1.png")
    img_signoff = os.path.join(root_dir, "AntennaLvsDrc.png")"""

    new_paths = """    cur_dir = os.path.dirname(os.path.abspath(__file__))
    doc_dir = os.path.dirname(cur_dir) if os.path.basename(cur_dir) == "temp" else cur_dir
    project_root = os.path.dirname(doc_dir)

    img_fig1 = os.path.join(cur_dir, "fig1_block_diagram.png")
    img_fig2 = os.path.join(cur_dir, "fig2_rdm6300_subsystem.png")
    img_fig2_h = os.path.join(cur_dir, "fig2_rdm6300_horizontal.png")
    img_openroad = os.path.join(project_root, "Openroad_1.png")
    img_signoff = os.path.join(project_root, "AntennaLvsDrc.png")"""

    src = src.replace(old_paths, new_paths)

    # 3. Add add_code_card after add_card
    old_card_fn = """    # Helper: Add Styled Card Container
    def add_card(slide, left, top, width, height, border_color=C_CARD_BORDER, bg_color=C_CARD_BG):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        return card"""

    new_card_fn = """    # Helper: Add Styled Card Container
    def add_card(slide, left, top, width, height, border_color=C_CARD_BORDER, bg_color=C_CARD_BG):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        return card

    # Helper: Add IDE-style Code Snippet Box with Syntax Highlighting
    def add_code_card(slide, left, top, width, height, title, subtitle, code_lines, result_banner=None, border_color=C_BLUE_ACCENT):
        add_card(slide, left, top, width, height, border_color, RGBColor(15, 23, 42))
        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.18), width - Inches(0.4), height - Inches(0.36))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Segoe UI"
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = C_CYAN_ACCENT
        p_t.space_after = Pt(1)
        
        p_sub = tf.add_paragraph()
        p_sub.text = subtitle
        p_sub.font.name = "Segoe UI"
        p_sub.font.size = Pt(8.8)
        p_sub.font.italic = True
        p_sub.font.color.rgb = RGBColor(148, 163, 184)
        p_sub.space_after = Pt(5)
        
        for line_text, line_type in code_lines:
            p_c = tf.add_paragraph()
            p_c.text = line_text
            p_c.font.name = "Consolas"
            p_c.font.size = Pt(7.6)
            p_c.space_after = Pt(0.4)
            
            if line_type == "comment":
                p_c.font.color.rgb = RGBColor(100, 116, 139)
                p_c.font.italic = True
            elif line_type == "pass":
                p_c.font.color.rgb = C_GREEN
                p_c.font.bold = True
            elif line_type == "keyword":
                p_c.font.color.rgb = RGBColor(56, 189, 248)
            elif line_type == "string":
                p_c.font.color.rgb = RGBColor(251, 191, 36)
            elif line_type == "fn":
                p_c.font.color.rgb = RGBColor(167, 139, 250)
            else:
                p_c.font.color.rgb = RGBColor(226, 232, 240)
                
        if result_banner:
            p_res = tf.add_paragraph()
            p_res.text = result_banner
            p_res.font.name = "Consolas"
            p_res.font.size = Pt(8.6)
            p_res.font.bold = True
            p_res.font.color.rgb = C_GREEN
            p_res.space_before = Pt(5)"""

    src = src.replace(old_card_fn, new_card_fn)

    # 4. Split around old Slide 12 marker
    marker_old_12 = "    # =========================================================================\n    # SLIDE 12: THỰC NGHIỆM TRÊN FPGA BASYS 3 (Hardware Demo)"
    if marker_old_12 not in src:
        print("[ERROR] marker_old_12 not found!")
        return

    part_before, part_after = src.split(marker_old_12, 1)

    # 5. Build New Slides 12-17
    slides_12_to_17 = """    # =========================================================================
    # SLIDE 12: TỔNG QUAN HỆ THỐNG KIỂM THỬ MÔ PHỎNG & MA TRẬN 63 TEST CASES
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Chương 3 | Quy trình thiết kế tuần tự", "3.8. Tổng Quan Hệ Thống Testbench & Ma Trận 63 Test Cases (PASS 100%)", 12, 22)

    add_card(s12, Inches(0.8), Inches(1.35), Inches(6.6), Inches(5.35), C_BLUE_ACCENT)
    tb_tb1 = s12.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(6.2), Inches(5.0))
    tf_tb1 = tb_tb1.text_frame
    tf_tb1.word_wrap = True

    p_tb0 = tf_tb1.paragraphs[0]
    p_tb0.text = "📊 Bảng Tổng Hợp Kiểm Thử 5 Bước Thiết Kế (Ma Trận 63 TCs)"
    p_tb0.font.name = "Segoe UI"
    p_tb0.font.size = Pt(14)
    p_tb0.font.bold = True
    p_tb0.font.color.rgb = C_BLUE_ACCENT
    p_tb0.space_after = Pt(8)

    tb_steps_data = [
        ("Step 2 (tb/step2_firmware/):", "21/21 PASS (100%)", "Kiểm thử 21 hàm firmware C: in số không chia, checksum XOR thẻ 00007293F0 (0x11), tra cứu RAM."),
        ("Step 3 (tb/step3_picorv32_sram/):", "12/12 PASS (100%)", "Nhân CPU PicoRV32 & 1KB SRAM: ghi byte strobes wstrb[3:0], biên 0x3FC, bắt tay valid/ready 1 chu kỳ."),
        ("Step 4 (tb/step4_spimemio_flash/):", "10/10 PASS (100%)", "Bộ điều khiển SPI Flash spimemio: Read JEDEC ID (0x9F), WREN, Erase Sector 48, Program, XIP Direct."),
        ("Step 5 (tb/step5_rdm6300_pipeline/):", "12/12 PASS (100%)", "Đường ống RFID 5 tầng: 2-FF CDC, bộ lọc nhiễu majority 3 điểm, FIFO 16 byte, FSM 14 byte, cây XOR 20ns."),
        ("Step 6 (tb/step6_top_soc_integration/):", "8/8 PASS (100%)", "Tích hợp toàn diện SoC: Boot Flash XIP, RFID ngắt CPU, Grant/Deny, ghi nhật ký, cpu_trap == 0.")
    ]

    for s_title, s_res, s_desc in tb_steps_data:
        p_st = tf_tb1.add_paragraph()
        p_st.text = f"• {s_title} "
        p_st.font.name = "Segoe UI"
        p_st.font.size = Pt(9.8)
        p_st.font.bold = True
        p_st.font.color.rgb = C_TEXT_DARK
        p_st.space_after = Pt(2)

        r_res = p_st.add_run()
        r_res.text = f"[{s_res}]\\n"
        r_res.font.bold = True
        r_res.font.color.rgb = C_GREEN

        r_desc = p_st.add_run()
        r_desc.text = f"  {s_desc}"
        r_desc.font.bold = False
        r_desc.font.color.rgb = C_TEXT_MUTED
        r_desc.font.size = Pt(9.0)

    p_tot = tf_tb1.add_paragraph()
    p_tot.text = "🎯 TỔNG CỘNG HỆ THỐNG: 63/63 TEST CASES PASS (100% HOÀN HẢO)"
    p_tot.font.name = "Segoe UI"
    p_tot.font.size = Pt(10.5)
    p_tot.font.bold = True
    p_tot.font.color.rgb = C_GREEN
    p_tot.space_before = Pt(5)

    p_b1 = tf_tb1.add_paragraph()
    p_b1.text = "⏱ Tần số kiểm tra: 50.0 MHz (Chu kỳ 20.0 ns)  |  Độ trễ bắt tay SRAM: 1 chu kỳ clock"
    p_b1.font.name = "Segoe UI"
    p_b1.font.size = Pt(9.0)
    p_b1.font.bold = True
    p_b1.font.color.rgb = C_BLUE_ACCENT
    p_b1.space_before = Pt(3)

    p_b2 = tf_tb1.add_paragraph()
    p_b2.text = "⚡ Thời gian hồi quy: 0.18 giây (Python)  |  Tỷ lệ thành công: 63/63 PASS (100.0%)"
    p_b2.font.name = "Segoe UI"
    p_b2.font.size = Pt(9.0)
    p_b2.font.bold = True
    p_b2.font.color.rgb = C_GREEN

    # Right: Architecture & Clean Workspace Cards
    add_card(s12, Inches(7.6), Inches(1.35), Inches(4.933), Inches(2.55), C_PURPLE)
    tb_tb2 = s12.shapes.add_textbox(Inches(7.8), Inches(1.5), Inches(4.533), Inches(2.25))
    tf_tb2 = tb_tb2.text_frame
    tf_tb2.word_wrap = True
    p_arc0 = tf_tb2.paragraphs[0]
    p_arc0.text = "📁 Quy Hoạch Thư Mục Độc Lập"
    p_arc0.font.name = "Segoe UI"
    p_arc0.font.size = Pt(13)
    p_arc0.font.bold = True
    p_arc0.font.color.rgb = C_PURPLE
    p_arc0.space_after = Pt(6)

    arc_points = [
        ("Mỗi bước 1 thư mục riêng:", "Chứa đầy đủ testbench Verilog (.v), test runner (.py), file chạy (.bat) và tài liệu README.md."),
        ("Tự động gom tệp tạm vào temp/:", "Toàn bộ file phát sinh từ Vivado (xsim.dir, *.log, *.pb, *.wdb) được tự động chuyển vào thư mục temp/ để giữ sạch cây mã nguồn.")
    ]
    for apt, apd in arc_points:
        p = tf_tb2.add_paragraph()
        p.text = f"▸ {apt} "
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(2)
        r = p.add_run()
        r.text = apd
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED

    add_card(s12, Inches(7.6), Inches(4.15), Inches(4.933), Inches(2.55), C_AMBER)
    tb_tb3 = s12.shapes.add_textbox(Inches(7.8), Inches(4.3), Inches(4.533), Inches(2.25))
    tf_tb3 = tb_tb3.text_frame
    tf_tb3.word_wrap = True
    p_eng0 = tf_tb3.paragraphs[0]
    p_eng0.text = "⚡ Cơ Chế Kiểm Thử Hai Tầng (Dual-Engine)"
    p_eng0.font.name = "Segoe UI"
    p_eng0.font.size = Pt(13)
    p_eng0.font.bold = True
    p_eng0.font.color.rgb = C_AMBER
    p_eng0.space_after = Pt(6)

    eng_points = [
        ("Fast Automation Runner (Python):", "Kiểm thử hồi quy toàn diện 63 test case trong 0.18 giây độc lập, không tốn tài nguyên đồ họa."),
        ("AMD Vivado Simulator (xsim):", "Mô phỏng phần cứng chu kỳ xung nhịp chuẩn xác (cycle-accurate) trên mã RTL Verilog, xuất waveform .wdb.")
    ]
    for ept, epd in eng_points:
        p = tf_tb3.add_paragraph()
        p.text = f"▸ {ept} "
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(2)
        r = p.add_run()
        r.text = epd
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 13: STEP 2 - KIỂM THỬ FIRMWARE C & GIAO THỨC HOST (tb_firmware.c)
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Chương 3 | Kiểm thử từng bước: Step 2 Firmware", "3.8.1. Kiểm Thử Bước 2: Logic Firmware Bare-Metal C & Giao Thức Host", 13, 22)

    col_w_step = Inches(5.7)
    add_card(s13, Inches(0.8), Inches(1.35), col_w_step, Inches(3.3), C_BLUE_ACCENT)
    tb_s13_l1 = s13.shapes.add_textbox(Inches(1.0), Inches(1.45), col_w_step - Inches(0.4), Inches(3.1))
    tf_s13_l1 = tb_s13_l1.text_frame
    tf_s13_l1.word_wrap = True

    p = tf_s13_l1.paragraphs[0]
    p.text = "🎯 Nội Dung & Kịch Bản Kiểm Thử Bước 2"
    p.font.name = "Segoe UI"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_ACCENT
    p.space_after = Pt(6)

    s13_test_items = [
        ("Giả lập ngoại vi phần cứng MMIO:", "Tạo mô hình mảng RAM 16MB giả lập Flash và ánh xạ thanh ghi MMIO (REG_RFID_STATUS, REG_RFID_TAG_HI/LO, REG_PC_UART_DAT, REG_GPIO_LEDS)."),
        ("Toán tử in số không dùng phép chia:", "In số thập phân và Hex thuần túy bằng phép dịch bit và trừ tuần tự, loại bỏ hoàn toàn bộ chia RV32M để tiết kiệm 35% diện tích silicon."),
        ("Xác thực Checksum & Quản trị thẻ:", "Kiểm thử thẻ 00007293F0 -> Checksum XOR 0x11; ghi thẻ vào Flash; cơ chế chống trùng lặp; bảo vệ Master Card Slot 0 không bị xóa."),
        ("Bộ giải mã tập lệnh Host Console:", "Xác thực toàn diện 13 lệnh nhị phân Win32 ('P', 'R', 'W', 'N', 'C', 'L', 'K', 'X', 'S') qua đệm FIFO.")
    ]
    for tit, dsc in s13_test_items:
        p = tf_s13_l1.add_paragraph()
        p.text = f"• {tit} "
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.2)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(2)
        r = p.add_run()
        r.text = dsc
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED

    add_card(s13, Inches(0.8), Inches(4.8), col_w_step, Inches(2.05), C_GREEN, RGBColor(240, 253, 244))
    tb_s13_l2 = s13.shapes.add_textbox(Inches(1.0), Inches(4.9), col_w_step - Inches(0.4), Inches(1.85))
    tf_s13_l2 = tb_s13_l2.text_frame
    tf_s13_l2.word_wrap = True

    p = tf_s13_l2.paragraphs[0]
    p.text = "📊 Kết Quả Xác Minh Bước 2 (tb_firmware.c)"
    p.font.name = "Segoe UI"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_GREEN
    p.space_after = Pt(4)

    s13_res = [
        ("Tỷ lệ thành công:", "21/21 Unit Test Cases PASS (100.0% Tuyệt đối)"),
        ("Thời gian thực thi:", "0.03 giây (Kiểm thử tức thì trên GCC & Python Runner)"),
        ("An toàn bộ nhớ:", "0 byte rò rỉ (Zero Leak), 0 lỗi con trỏ null"),
        ("Chống nhiễu dữ liệu:", "Xử lý chuẩn xác các chuỗi thẻ rác, thiếu byte, sai định dạng Hex")
    ]
    for rt, rd in s13_res:
        p = tf_s13_l2.add_paragraph()
        p.text = f"✔ {rt} "
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.0)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(1.5)
        r = p.add_run()
        r.text = rd
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED

    s13_code = [
        ("// 1. Kiểm thử in số không dùng bộ chia phần cứng", "comment"),
        ("test_case_begin(\\"TC02 - Non-division number printing\\");", "fn"),
        ("uart_puthex32(0xDEADBEEF); // Dùng dịch bit & trừ tuần tự", "keyword"),
        ("TEST_ASSERT(strcmp(buf, \\"DEADBEEF\\") == 0, \\"Hex match\\");", "pass"),
        ("", "code"),
        ("// 2. Kiểm thử đăng ký thẻ thủ công vào Flash", "comment"),
        ("test_case_begin(\\"TC07 - Manual Tag Registration\\");", "fn"),
        ("host_send_string(\\"N00007293F0\\\\n\\"); // Gửi chuỗi 10 Hex", "keyword"),
        ("firmware_run_cycles(10);", "keyword"),
        ("TEST_ASSERT(strstr(buf, \\"OK:MANUAL_TAG_SAVED:SLOT:1\\") != NULL);", "pass"),
        ("", "code"),
        ("// 3. Giả lập sự kiện quẹt thẻ từ ngoại vi MMIO", "comment"),
        ("test_case_begin(\\"TC20 - Hardware MMIO Polling Integration\\");", "fn"),
        ("REG_RFID_STATUS = 0x01; // card_valid strobe", "keyword"),
        ("REG_RFID_TAG_HI = 0x01;", "keyword"),
        ("REG_RFID_TAG_LO = 0x0054DA65; // Whitelisted Master Card", "keyword"),
        ("poll_rdm6300(); // Firmware tra cứu Flash", "fn"),
        ("host_read_line(buf, sizeof(buf));", "keyword"),
        ("TEST_ASSERT(strstr(buf, \\"ACCESS:GRANTED:SLOT:0\\") != NULL);", "pass"),
        ("TEST_ASSERT(rdm_cooldown_cnt == 250000, \\"Debounce set\\");", "pass"),
    ]
    add_code_card(s13, Inches(6.833), Inches(1.35), Inches(5.7), Inches(5.5),
                  "💻 Trích Đoạn Kiểm Thử C: Unit Tests & MMIO Event",
                  "Mã nguồn: tb/step2_firmware/tb_firmware.c",
                  s13_code,
                  ">>> XÁC THỰC BƯỚC 2: 21/21 UNIT TESTS PASS (100% HOÀN HẢO) <<<",
                  C_BLUE_ACCENT)

    # =========================================================================
    # SLIDE 14: STEP 3 - MÔ PHỎNG CPU PICORV32 & 1KB DATA SRAM (tb_data_sram.v)
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Chương 3 | Kiểm thử từng bước: Step 3 CPU & SRAM", "3.8.2. Kiểm Thử Bước 3: Mô Phỏng Nhân CPU PicoRV32 & 1KB Data SRAM", 14, 22)

    add_card(s14, Inches(0.8), Inches(1.35), col_w_step, Inches(3.3), C_BLUE_ACCENT)
    tb_s14_l1 = s14.shapes.add_textbox(Inches(1.0), Inches(1.45), col_w_step - Inches(0.4), Inches(3.1))
    tf_s14_l1 = tb_s14_l1.text_frame
    tf_s14_l1.word_wrap = True

    p = tf_s14_l1.paragraphs[0]
    p.text = "🎯 Nội Dung & Kịch Bản Kiểm Thử Bước 3"
    p.font.name = "Segoe UI"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_ACCENT
    p.space_after = Pt(6)

    s14_test_items = [
        ("Ghi byte độc lập (wstrb[3:0] Byte Strobes):", "Kiểm tra ghi đè từng byte (byte 0, byte 2) trong từ nhớ 32-bit mà giữ nguyên vẹn giá trị của byte 1 và byte 3."),
        ("Chu kỳ bắt tay Bus (valid/ready Handshake):", "Xác minh giao thức bus: tín hiệu ready tích cực đúng 1 chu kỳ clock (20ns ở 50MHz) sau valid, và hạ ngay khi valid về 0."),
        ("Biên đỉnh vùng nhớ (Top Boundary Word 255):", "Đọc/ghi tại từ nhớ thứ 255 (địa chỉ 0x3FC), bảo đảm bộ giải mã 10-bit không xảy ra hiện tượng chồng lấn hoặc tràn địa chỉ."),
        ("Tích hợp CPU PicoRV32:", "Xác nhận CPU thực thi các lệnh đọc/ghi bộ nhớ (lw, sw, lb, sb) trên SRAM thông qua bus dữ liệu nội bộ.")
    ]
    for tit, dsc in s14_test_items:
        p = tf_s14_l1.add_paragraph()
        p.text = f"• {tit} "
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.2)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(2)
        r = p.add_run()
        r.text = dsc
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED

    add_card(s14, Inches(0.8), Inches(4.8), col_w_step, Inches(2.05), C_GREEN, RGBColor(240, 253, 244))
    tb_s14_l2 = s14.shapes.add_textbox(Inches(1.0), Inches(4.9), col_w_step - Inches(0.4), Inches(1.85))
    tf_s14_l2 = tb_s14_l2.text_frame
    tf_s14_l2.word_wrap = True

    p = tf_s14_l2.paragraphs[0]
    p.text = "📊 Kết Quả Mô Phỏng AMD Vivado xsim v2025.2"
    p.font.name = "Segoe UI"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_GREEN
    p.space_after = Pt(4)

    s14_res = [
        ("Tỷ lệ thành công:", "12/12 PASS (Python) + 7/7 Verilog Assertions PASS"),
        ("Tần số hoạt động:", "50.0 MHz (Chu kỳ xung nhịp 20.0 ns)"),
        ("Độ trễ truy cập SRAM:", "Đúng 1 chu kỳ clock (1-Cycle Latency Handshake)"),
        ("Tính toàn vẹn dữ liệu:", "Bảo toàn 100% dữ liệu vùng ngăn xếp Stack (sp = 0x400) và .data")
    ]
    for rt, rd in s14_res:
        p = tf_s14_l2.add_paragraph()
        p.text = f"✔ {rt} "
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.0)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(1.5)
        r = p.add_run()
        r.text = rd
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED

    s14_code = [
        ("// 1. Kiểm tra ghi đè từng byte bằng wstrb[3:0]", "comment"),
        ("$display(\\"[TEST 2] Testing Byte-Wise Write Enables...\\");", "fn"),
        ("sram_write(10'h004, 32'h11223344, 4'b1111); // Nạp từ ban đầu", "keyword"),
        ("sram_write(10'h004, 32'hAA00BB00, 4'b1010); // Ghi Byte 1 & 3", "keyword"),
        ("sram_read(10'h004, read_data);", "keyword"),
        ("if (read_data === 32'hAA22BB44) begin", "keyword"),
        ("    $display(\\"  [PASS] Byte-Wise: Read 0x%08X\\", read_data);", "pass"),
        ("    tests_passed = tests_passed + 1;", "pass"),
        ("end", "keyword"),
        ("", "code"),
        ("// 2. Kiểm tra chu kỳ bắt tay Bus valid/ready trong 1 clock", "comment"),
        ("@(posedge clk);", "keyword"),
        ("valid <= 1'b1; addr <= 10'h008; wdata <= 32'hCAFEBABE;", "keyword"),
        ("wstrb <= 4'b1111;", "keyword"),
        ("@(posedge clk);", "keyword"),
        ("if (ready === 1'b1) begin", "keyword"),
        ("    $display(\\"  [PASS] ready asserted in 1 clock cycle!\\");", "pass"),
        ("    tests_passed = tests_passed + 1;", "pass"),
        ("end", "keyword"),
        ("", "code"),
        ("// 3. Kiểm tra đọc/ghi tại biên đỉnh bộ nhớ 1KB (Word 255)", "comment"),
        ("sram_write(10'h3FC, 32'hA5A55A5A, 4'b1111);", "keyword"),
        ("sram_read(10'h3FC, read_data);", "keyword"),
        ("assert(read_data === 32'hA5A55A5A);", "pass"),
    ]
    add_code_card(s14, Inches(6.833), Inches(1.35), Inches(5.7), Inches(5.5),
                  "💻 Trích Đoạn Testbench Verilog: Ghi Byte & Bắt Tay Bus",
                  "Mã nguồn: tb/step3_picorv32_sram/tb_data_sram.v",
                  s14_code,
                  ">>> AMD Vivado xsim: 7/7 RTL CHECKS & 12/12 PYTHON PASS <<<",
                  C_BLUE_ACCENT)

    # =========================================================================
    # SLIDE 15: STEP 4 - MÔ PHỎNG SPI FLASH CONTROLLER (tb_spi_flash.v)
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Chương 3 | Kiểm thử từng bước: Step 4 SPI Flash", "3.8.3. Kiểm Thử Bước 4: Mô Phỏng Bộ Điều Khiển Bộ Nhớ Ngoài SPI Flash", 15, 22)

    add_card(s15, Inches(0.8), Inches(1.35), col_w_step, Inches(3.3), C_BLUE_ACCENT)
    tb_s15_l1 = s15.shapes.add_textbox(Inches(1.0), Inches(1.45), col_w_step - Inches(0.4), Inches(3.1))
    tf_s15_l1 = tb_s15_l1.text_frame
    tf_s15_l1.word_wrap = True

    p = tf_s15_l1.paragraphs[0]
    p.text = "🎯 Nội Dung & Kịch Bản Kiểm Thử Bước 4"
    p.font.name = "Segoe UI"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_ACCENT
    p.space_after = Pt(6)

    s15_test_items = [
        ("Giao diện chuẩn SPI Mode 0:", "Điều khiển 4 đường flash_csn, flash_sck, flash_mosi, flash_miso giao tiếp mô hình SPI Flash Spansion S25FL032P 32 Mbit."),
        ("Đọc mã định danh JEDEC ID (0x9F):", "Xác nhận phần cứng đọc chính xác Manufacturer ID 0x01 và Device ID 0x0215 qua thanh ghi dữ liệu."),
        ("Lệnh ghi & xóa Flash phần cứng:", "Write Enable (0x06) bật cờ WEL; Sector Erase 64KB (0xD8) xóa Sector 48 (0x300000) về 0xFF; Page Program (0x02) nạp 256 byte."),
        ("Cơ chế thực thi tại chỗ Flash XIP:", "CPU đọc mã máy trực tiếp qua bus bộ nhớ ánh xạ mà không cần nạp trước vào RAM, reset tại 0x0025_0000.")
    ]
    for tit, dsc in s15_test_items:
        p = tf_s15_l1.add_paragraph()
        p.text = f"• {tit} "
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.2)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(2)
        r = p.add_run()
        r.text = dsc
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED

    add_card(s15, Inches(0.8), Inches(4.8), col_w_step, Inches(2.05), C_GREEN, RGBColor(240, 253, 244))
    tb_s15_l2 = s15.shapes.add_textbox(Inches(1.0), Inches(4.9), col_w_step - Inches(0.4), Inches(1.85))
    tf_s15_l2 = tb_s15_l2.text_frame
    tf_s15_l2.word_wrap = True

    p = tf_s15_l2.paragraphs[0]
    p.text = "📊 Kết Quả Mô Phỏng SPI Flash Controller"
    p.font.name = "Segoe UI"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_GREEN
    p.space_after = Pt(4)

    s15_res = [
        ("Tỷ lệ thành công:", "10/10 Test Cases PASS (100.0% Tuyệt đối)"),
        ("Tần số xung nhịp SPI:", "25.0 MHz (Chia đôi từ Clock hệ thống 50.0 MHz)"),
        ("Quản lý cờ bận:", "Tín hiệu flash_busy khóa bus an toàn trong suốt chu kỳ ghi/xóa"),
        ("Lưu trữ bền vững:", "Dữ liệu được bảo toàn nguyên vẹn sau chu kỳ mô phỏng reset")
    ]
    for rt, rd in s15_res:
        p = tf_s15_l2.add_paragraph()
        p.text = f"✔ {rt} "
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.0)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(1.5)
        r = p.add_run()
        r.text = rd
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED

    s15_code = [
        ("// 1. Tác vụ đọc JEDEC ID chip Flash (Spansion S25FL032P)", "comment"),
        ("task flash_read_jedec(output [23:0] id);", "fn"),
        ("    begin", "keyword"),
        ("        bus_write(REG_FLASH_CMD, 32'h0000_009F); // Phát RDID", "keyword"),
        ("        while (flash_busy) @(posedge clk);        // Chờ SPI", "keyword"),
        ("        bus_read(REG_FLASH_DAT, id);", "keyword"),
        ("        if (id[23:16] == 8'h01) // Spansion ID", "keyword"),
        ("            $display(\\"  [PASS] JEDEC ID: 0x%06X (Valid Flash)\\", id);", "pass"),
        ("    end", "keyword"),
        ("endtask", "fn"),
        ("", "code"),
        ("// 2. Xóa khối Sector Erase 64KB (Sector 48 - 0x300000)", "comment"),
        ("bus_write(REG_FLASH_ADDR, 24'h30_0000);", "keyword"),
        ("bus_write(REG_FLASH_CMD,  32'h0000_00D8); // Lệnh Sector Erase", "keyword"),
        ("while (flash_busy) @(posedge clk);", "keyword"),
        ("$display(\\"  [PASS] Sector 48 erased to 0xFF successfully\\");", "pass"),
        ("", "code"),
        ("// 3. Ghi trang Page Program 16-byte bản ghi thẻ RFID", "comment"),
        ("bus_write(REG_FLASH_DATA, 32'h52464944); // 'RFID' Magic", "keyword"),
        ("bus_write(REG_FLASH_CMD,  32'h0000_0002); // Page Program", "keyword"),
        ("while (flash_busy) @(posedge clk);", "keyword"),
        ("$display(\\"  [PASS] Page Program: 16-byte record written into Flash\\");", "pass"),
    ]
    add_code_card(s15, Inches(6.833), Inches(1.35), Inches(5.7), Inches(5.5),
                  "💻 Trích Đoạn Testbench Verilog: Lệnh SPI & Thực Thi XIP",
                  "Mã nguồn: tb/step4_spimemio_flash/tb_spi_flash.v",
                  s15_code,
                  ">>> XÁC THỰC BƯỚC 4: 10/10 SPI PROTOCOL PASS (100%) <<<",
                  C_BLUE_ACCENT)

    # =========================================================================
    # SLIDE 16: STEP 5 - MÔ PHỎNG ĐƯỜNG ỐNG RFID 5 TẦNG (tb_rdm6300_pipeline.v)
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "Chương 3 | Kiểm thử từng bước: Step 5 RFID Pipeline", "3.8.4. Kiểm Thử Bước 5: Mô Phỏng Đường Ống Thu Nhận RFID 5 Tầng & Cây XOR", 16, 22)

    add_card(s16, Inches(0.8), Inches(1.35), col_w_step, Inches(3.3), C_BLUE_ACCENT)
    tb_s16_l1 = s16.shapes.add_textbox(Inches(1.0), Inches(1.45), col_w_step - Inches(0.4), Inches(3.1))
    tf_s16_l1 = tb_s16_l1.text_frame
    tf_s16_l1.word_wrap = True

    p = tf_s16_l1.paragraphs[0]
    p.text = "🎯 Nội Dung & Kịch Bản Kiểm Thử Bước 5"
    p.font.name = "Segoe UI"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_ACCENT
    p.space_after = Pt(6)

    s16_test_items = [
        ("Tầng 1 (2-FF CDC Synchronizer):", "Khử hiện tượng siêu bền bất định khi bắt tín hiệu UART 9600 bps bất đồng bộ từ RDM6300 vào miền clock 50MHz."),
        ("Tầng 2 (Lọc đa số 3 điểm UART RX):", "Bộ lấy mẫu 16x loại bỏ hoàn toàn các xung gai nhiễu điện từ < 100ns từ cuộn cảm ăng-ten 125 kHz."),
        ("Tầng 3 (Hàng đợi FIFO 16 byte):", "Cách ly tốc độ thu dữ liệu và tốc độ CPU, chống rơi byte khi CPU bận ghi Flash."),
        ("Tầng 4 & 5 (FSM 14 Byte & Cây XOR 20ns):", "Nhận diện STX (0x02), 10 byte mã thẻ, 2 byte checksum, ETX (0x03). Tính Checksum XOR song song trong đúng 1 chu kỳ clock (20ns)."),
        ("Kiểm thử thẻ giả mạo (Negative Test):", "Gửi khung thẻ bị sửa sai checksum -> phần cứng phát hiện lỗi ngay, từ chối cấp cờ card_valid.")
    ]
    for tit, dsc in s16_test_items:
        p = tf_s16_l1.add_paragraph()
        p.text = f"• {tit} "
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.2)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(2)
        r = p.add_run()
        r.text = dsc
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED

    add_card(s16, Inches(0.8), Inches(4.8), col_w_step, Inches(2.05), C_GREEN, RGBColor(240, 253, 244))
    tb_s16_l2 = s16.shapes.add_textbox(Inches(1.0), Inches(4.9), col_w_step - Inches(0.4), Inches(1.85))
    tf_s16_l2 = tb_s16_l2.text_frame
    tf_s16_l2.word_wrap = True

    p = tf_s16_l2.paragraphs[0]
    p.text = "📊 Kết Quả Xác Minh AMD Vivado xsim v2025.2"
    p.font.name = "Segoe UI"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_GREEN
    p.space_after = Pt(4)

    s16_res = [
        ("Tỷ lệ thành công:", "12/12 PASS (100.0%) trên cả Vivado xsim và Python"),
        ("Độ trễ tính toán Checksum:", "Đúng 1 chu kỳ xung nhịp (20.0 ns) ngay sau ETX"),
        ("Tỷ lệ loại trừ lỗi:", "100% khung thẻ sai checksum bị triệt tiêu"),
        ("Tương thích chuẩn:", "Khớp hoàn hảo định dạng thẻ EM4100 125 kHz công nghiệp")
    ]
    for rt, rd in s16_res:
        p = tf_s16_l2.add_paragraph()
        p.text = f"✔ {rt} "
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.0)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(1.5)
        r = p.add_run()
        r.text = rd
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED

    s16_code = [
        ("// 1. Kịch bản quẹt thẻ hợp lệ: 00007293F0 (Checksum XOR = 0x11)", "comment"),
        ("$display(\\"[INFO] Transmitting valid RFID Card: 00007293F0...\\");", "fn"),
        ("send_rfid_byte(8'h02); // STX (Start of Text)", "keyword"),
        ("send_rfid_string(\\"00007293F0\\"); // 10 ký tự ASCII dữ liệu thẻ", "keyword"),
        ("send_rfid_string(\\"11\\");         // 2 ký tự Checksum XOR chuẩn", "keyword"),
        ("send_rfid_byte(8'h03); // ETX (End of Text)", "keyword"),
        ("", "code"),
        ("@(posedge card_valid);", "keyword"),
        ("if (tag_raw === 40'h00007293F0) begin", "keyword"),
        ("    $display(\\"  [PASS] TC01: Card valid asserted! Tag = %010X\\", tag_raw);", "pass"),
        ("    tests_passed = tests_passed + 1;", "pass"),
        ("end", "keyword"),
        ("", "code"),
        ("// 2. Kịch bản thẻ giả mạo sai Checksum (Negative Test)", "comment"),
        ("$display(\\"[INFO] Transmitting corrupted RFID Card (Bad Checksum)...\\");", "fn"),
        ("send_rfid_byte(8'h02); send_rfid_string(\\"00007293F0\\");", "keyword"),
        ("send_rfid_string(\\"99\\"); // Sai Checksum (kỳ vọng 0x11)", "keyword"),
        ("send_rfid_byte(8'h03);", "keyword"),
        ("#100;", "keyword"),
        ("assert(checksum_error === 1'b1 && card_valid === 1'b0);", "pass"),
        ("$display(\\"  [PASS] TC02: Hardware XOR Checksum detected mismatch!\\");", "pass"),
    ]
    add_code_card(s16, Inches(6.833), Inches(1.35), Inches(5.7), Inches(5.5),
                  "💻 Trích Đoạn Testbench Verilog: Khung 14 Byte & Cây XOR",
                  "Mã nguồn: tb/step5_rdm6300_pipeline/tb_rdm6300_pipeline.v",
                  s16_code,
                  ">>> AMD Vivado xsim: 12/12 PASS - CHU KỲ XOR = 20.0 ns <<<",
                  C_BLUE_ACCENT)

    # =========================================================================
    # SLIDE 17: STEP 6 - MÔ PHỎNG TÍCH HỢP TOÀN DIỆN TOP SOC (tb_picorv32_rdm6300_flash.v)
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    add_header(s17, "Chương 3 | Kiểm thử từng bước: Step 6 Top SoC", "3.8.5. Kiểm Thử Bước 6: Mô Phỏng Tích Hợp Toàn Diện Top SoC & End-to-End", 17, 22)

    add_card(s17, Inches(0.8), Inches(1.35), col_w_step, Inches(3.3), C_BLUE_ACCENT)
    tb_s17_l1 = s17.shapes.add_textbox(Inches(1.0), Inches(1.45), col_w_step - Inches(0.4), Inches(3.1))
    tf_s17_l1 = tb_s17_l1.text_frame
    tf_s17_l1.word_wrap = True

    p = tf_s17_l1.paragraphs[0]
    p.text = "🎯 Nội Dung & Kịch Bản Kiểm Thử Bước 6 (Top SoC)"
    p.font.name = "Segoe UI"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_ACCENT
    p.space_after = Pt(6)

    s17_test_items = [
        ("Quy trình khởi động hệ thống (Full SoC Boot):", "CPU PicoRV32 khởi động từ vector reset 0x0025_0000 trên SPI Flash, nạp firmware, thiết lập ngăn xếp sp = 0x400 trên 1KB SRAM."),
        ("Xử lý ngắt quẹt thẻ thời gian thực:", "Module RDM6300 giải mã thẻ xong tự động kích hoạt ngắt CPU; firmware truy vấn danh mục thẻ trong Flash."),
        ("Logic kiểm soát ra vào Access Control:", "Thẻ hợp lệ (trong Whitelist) -> CPU xuất 'ACCESS:GRANTED', chớp LED xanh; Thẻ lạ -> xuất 'ACCESS:DENIED', chớp LED đỏ."),
        ("Ghi nhật ký bảo mật (Audit Log):", "Tự động ghi 16 byte lịch sử vào Sector 49 của Flash."),
        ("Giám sát bẫy CPU Trap:", "Đảm bảo cpu_trap == 0 tuyệt đối qua 10 triệu chu kỳ xung nhịp mô phỏng.")
    ]
    for tit, dsc in s17_test_items:
        p = tf_s17_l1.add_paragraph()
        p.text = f"• {tit} "
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.2)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(2)
        r = p.add_run()
        r.text = dsc
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED

    add_card(s17, Inches(0.8), Inches(4.8), col_w_step, Inches(2.05), C_GREEN, RGBColor(240, 253, 244))
    tb_s17_l2 = s17.shapes.add_textbox(Inches(1.0), Inches(4.9), col_w_step - Inches(0.4), Inches(1.85))
    tf_s17_l2 = tb_s17_l2.text_frame
    tf_s17_l2.word_wrap = True

    p = tf_s17_l2.paragraphs[0]
    p.text = "📊 Kết Quả Kiểm Thử Tích Hợp Hệ Thống"
    p.font.name = "Segoe UI"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_GREEN
    p.space_after = Pt(4)

    s17_res = [
        ("Tỷ lệ thành công:", "8/8 Test Cases PASS (100.0% Tuyệt đối)"),
        ("An toàn vi xử lý:", "cpu_trap == 0 (Không lỗi truy cập bộ nhớ hoặc chia cho 0)"),
        ("Tránh xung đột Bus:", "Phân giải địa chỉ Flash XIP, SRAM, ngoại vi đạt 0 deadlock"),
        ("Sẵn sàng Tape-out:", "Toàn bộ hệ thống hoạt động đồng bộ trước khi chuyển sang ASIC")
    ]
    for rt, rd in s17_res:
        p = tf_s17_l2.add_paragraph()
        p.text = f"✔ {rt} "
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.0)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(1.5)
        r = p.add_run()
        r.text = rd
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED

    s17_code = [
        ("// Kiểm thử kịch bản vận hành thực tế toàn diện trên Top SoC", "comment"),
        ("initial begin", "keyword"),
        ("    rst_n = 0; #200; rst_n = 1;", "keyword"),
        ("", "code"),
        ("    // 1. Chờ PicoRV32 boot từ SPI Flash XIP & khởi tạo UART", "comment"),
        ("    wait_uart_string(\\"PicoRV32 RFID Access Controller Initialized\\");", "fn"),
        ("    $display(\\"  [PASS] SoC Boot: CPU fetched code from Flash XIP\\");", "pass"),
        ("", "code"),
        ("    // 2. Bơm gói tin quẹt thẻ RDM6300 vào cổng nối tiếp", "comment"),
        ("    $display(\\"[INFO] Stimulating RFID Card Swipe: 00007293F0...\\");", "fn"),
        ("    send_rdm6300_packet(\\"00007293F0\\"); // Thẻ trong Whitelist", "keyword"),
        ("", "code"),
        ("    // 3. Kiểm tra CPU xử lý ngắt, tra cứu Flash và cấp quyền", "comment"),
        ("    wait_uart_string(\\"ACCESS:GRANTED:SLOT:0:00007293F0\\");", "fn"),
        ("    assert(cpu_trap === 1'b0); // Giám sát an toàn CPU", "pass"),
        ("    $display(\\"  [PASS] ACCESS:GRANTED issued, cpu_trap == 0\\");", "pass"),
        ("", "code"),
        ("    // 4. Kiểm tra tự động ghi bản ghi nhật ký vào Flash", "comment"),
        ("    wait_flash_write_done();", "fn"),
        ("    $display(\\"  [PASS] Audit Log written into Flash Sector 49\\");", "pass"),
        ("end", "keyword")
    ]
    add_code_card(s17, Inches(6.833), Inches(1.35), Inches(5.7), Inches(5.5),
                  "💻 Trích Đoạn Testbench Verilog: End-to-End SoC Stimulus",
                  "Mã nguồn: tb/step6_top_soc_integration/tb_picorv32_rdm6300_flash.v",
                  s17_code,
                  ">>> XÁC THỰC BƯỚC 6: 8/8 FULL-SYSTEM SOC PASS (100%) <<<",
                  C_BLUE_ACCENT)\n"""

    # 6. Renumber old slides 12 to 16 into 18 to 22 in part_after
    # Replace backwards to prevent collision:
    # Old Slide 16 -> Slide 22
    part_after = part_after.replace('# SLIDE 16: KẾT LUẬN & TỔNG KẾT ĐỀ TÀI (Thank You Slide)',
                                    '# SLIDE 22: KẾT LUẬN & TỔNG KẾT ĐỀ TÀI (Thank You Slide)')
    part_after = part_after.replace('s16 = prs.slides.add_slide(blank_layout)\n    bg16 = s16.shapes.',
                                    's22 = prs.slides.add_slide(blank_layout)\n    bg22 = s22.shapes.')
    part_after = part_after.replace('bg16', 'bg22')
    part_after = part_after.replace('s16', 's22')

    # Old Slide 15 -> Slide 21
    part_after = part_after.replace('# SLIDE 15: THẢO LUẬN & ĐÁNH GIÁ TỐI ƯU HÓA PPA',
                                    '# SLIDE 21: THẢO LUẬN & ĐÁNH GIÁ TỐI ƯU HÓA PPA')
    part_after = part_after.replace('add_header(s15, "Chương 6 | Đánh giá kỹ thuật", "Thảo Luận & Đánh Giá Tối Ưu Hóa PPA (Power - Performance - Area)", 15)',
                                    'add_header(s21, "Chương 6 | Đánh giá kỹ thuật", "Thảo Luận & Đánh Giá Tối Ưu Hóa PPA (Power - Performance - Area)", 21, 22)')
    part_after = part_after.replace('s15', 's21')

    # Old Slide 14 -> Slide 20
    part_after = part_after.replace('# SLIDE 14: KẾT QUẢ KÝ DUYỆT CHẾ TẠO SIGN-OFF TOÀN DIỆN',
                                    '# SLIDE 20: KẾT QUẢ KÝ DUYỆT CHẾ TẠO SIGN-OFF TOÀN DIỆN')
    part_after = part_after.replace('add_header(s14, "Chương 5 | Báo cáo kiểm định Sign-off", "Kết QuẢ Ký Duyệt Bán Dẫn Tuyệt Đối (Run RUN_2026-09-27_21-51-11)", 14)',
                                    'add_header(s20, "Chương 5 | Báo cáo kiểm định Sign-off", "Kết Quả Ký Duyệt Bán Dẫn Tuyệt Đối (Run RUN_2026-09-27_21-51-11)", 20, 22)')
    part_after = re.sub(r'add_header\(s14,\s*"Chương 5 \| Báo cáo kiểm định Sign-off",\s*"[^"]+",\s*14\)',
                        'add_header(s20, "Chương 5 | Báo cáo kiểm định Sign-off", "Kết Quả Ký Duyệt Bán Dẫn Tuyệt Đối (Run RUN_2026-09-27_21-51-11)", 20, 22)', part_after)
    part_after = part_after.replace('s14', 's20')

    # Old Slide 13 -> Slide 19
    part_after = part_after.replace('# SLIDE 13: THIẾT KẾ VẬT LÝ ASIC TRÊN OPENLANE 2 (Openroad_1.png Căn Khung)',
                                    '# SLIDE 19: THIẾT KẾ VẬT LÝ ASIC TRÊN OPENLANE 2 (Openroad_1.png Căn Khung)')
    part_after = re.sub(r'add_header\(s13,\s*"Chương 5 \| Hiện thực hóa vi mạch ASIC",\s*"[^"]+",\s*13\)',
                        'add_header(s19, "Chương 5 | Hiện thực hóa vi mạch ASIC", "Thiết Kế Vật Lý Vi Mạch Trên OpenLane 2 & OpenROAD (Sky130A)", 19, 22)', part_after)
    part_after = part_after.replace('s13', 's19')

    # Old Slide 12 -> Slide 18
    part_after = part_after.replace('# SLIDE 12: THỰC NGHIỆM TRÊN FPGA BASYS 3 (Hardware Demo)',
                                    '# SLIDE 18: THỰC NGHIỆM TRÊN FPGA BASYS 3 (Hardware Demo)')
    part_after = re.sub(r'add_header\(s12,\s*"Chương 4 \| Demo kiểm chứng thực nghiệm",\s*"[^"]+",\s*12\)',
                        'add_header(s18, "Chương 4 | Demo kiểm chứng thực nghiệm", "Tạo Mẫu Phần Cứng & Kiểm Chứng Thực Tế Trên Bo Mạch Basys 3", 18, 22)', part_after)
    part_after = part_after.replace('s12', 's18')

    # Update output save block
    old_save = """    # Save Presentation
    out_pptx = os.path.join(cur_dir, "Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.pptx")
    prs.save(out_pptx)
    print(f"[SUCCESS] Refined 18-Slide PPTX generated successfully at: {out_pptx}")"""

    new_save = """    # Save Presentation to document/ directory
    out_pptx_1 = os.path.join(doc_dir, "Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.pptx")
    out_pptx_2 = os.path.join(doc_dir, "Bao_Cao_Do_An_RDM6300_PicoRV32_SoC_v2.pptx")
    prs.save(out_pptx_1)
    prs.save(out_pptx_2)
    print(f"[SUCCESS] Comprehensive 22-Slide PPTX generated successfully at:\\n  - {out_pptx_1}\\n  - {out_pptx_2}")"""

    if old_save in part_after:
        part_after = part_after.replace(old_save, new_save)
    else:
        # Generic replacement for any prs.save
        part_after = re.sub(r'out_pptx\s*=.*?\n\s*prs\.save\(out_pptx\)\n\s*print\(.*?\)', new_save, part_after, flags=re.DOTALL)

    # 7. Write final assembled content
    header_old_18 = """    # =========================================================================
    # SLIDE 18: THỰC NGHIỆM TRÊN FPGA BASYS 3 (Hardware Demo)"""
    final_script = part_before + slides_12_to_17 + header_old_18 + part_after

    with open(script_path, "w", encoding="utf-8") as f:
        f.write(final_script)

    print(f"[SUCCESS] Successfully transformed {script_path} into 22-slide deck generator!")

if __name__ == "__main__":
    build()
