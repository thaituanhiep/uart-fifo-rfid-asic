import sys, os, io

# Read the git version of create_presentation.py (commit 654ca1a)
git_lines = open('rdm6300-picorv32-rom-data/document/temp/git_base_presentation.py', encoding='utf-8').readlines()

# Segment definitions from git_base_presentation.py
header_setup = git_lines[0:227]
slide1_code = git_lines[227:294]   # Slide 1: Trang bìa
slide2_code = git_lines[294:412]   # Slide 2: Phần 1 (Giới thiệu)
slide3_code = git_lines[412:433]   # Slide 3: Phần 3 (Sơ đồ khối SoC)
slide9_code = git_lines[702:805]   # Slide 9: Phần 5 (Demo Thiết Bị Phần Cứng - from git)
slide10_code = git_lines[885:975]  # Slide 10: Phần 6 (OpenLane 2 config.json - from git)
slide11_code = git_lines[975:1054] # Slide 11: Phần 6 (Bản Vẽ Layout OpenROAD - from git)
slide12_code = git_lines[1054:1192]# Slide 12: Phần 6 (Báo Cáo STA Multi-Corner - from git)
slide13_code = git_lines[1192:1267]# Slide 13: Tổng Kết Đồ Án (from git)

# Slide 4 code: 3-column table
slide4_code = '''
    # =========================================================================
    # SLIDE 04: PHẦN 3 - BẢNG TRA CỨU ĐỊA CHỈ MEMORY MAP (C & RTL)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Phần 3: Kiến Trúc Vi Hệ Thống SoC",
               "Bảng Tra Cứu Địa Chỉ (Memory Map) & Khai Báo Biến Trong C / RTL", 4, total_slides=TOTAL_SLIDES)

    t_card = add_card(s4, Inches(0.8), Inches(1.30), Inches(11.733), Inches(5.60), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)

    rows, cols = 7, 3
    t_left = Inches(0.95)
    t_top = Inches(1.42)
    t_width = Inches(11.433)
    t_height = Inches(5.35)

    table_shape = s4.shapes.add_table(rows, cols, t_left, t_top, t_width, t_height)
    table = table_shape.table

    table.columns[0].width = Inches(2.25)
    table.columns[1].width = Inches(3.20)
    table.columns[2].width = Inches(5.983)

    headers = [
        "ĐỊA CHỈ VÙNG NHỚ (MMIO / ADDRESS)",
        "NƠI KHAI BÁO C & GIAO DIỆN RTL",
        "Ý NGHĨA SỬ DỤNG VỚI FIRMWARE C (CÁCH DÙNG ➔ TÁC DÙNG)"
    ]

    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY_DARK
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.margin_left = cell.margin_right = Inches(0.08)
        cell.margin_top = cell.margin_bottom = Inches(0.05)
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.name = "Segoe UI"
        p.font.size = Pt(12.0)
        p.font.bold = True
        p.font.color.rgb = C_CYAN_ACCENT
        p.alignment = PP_ALIGN.CENTER

    table_rows_data = [
        (
            "0x1000_0000\\n0x1000_0004",
            "• C: REG_RFID_UART_DAT / DIV\\n• RTL: uart_mmio.v (u_rfid_uart)",
            [
                ("👉 Cách dùng:", "Polling non-blocking thanh ghi DAT."),
                ("🎯 Tác dụng:", "Nhận 14 byte chuỗi RFID 125kHz không treo CPU.")
            ]
        ),
        (
            "0x3000_0000\\n0x3000_0004",
            "• C: REG_PC_UART_DAT / DIV\\n• RTL: uart_mmio.v (u_pc_uart)",
            [
                ("👉 Cách dùng:", "Gọi hàm putchar_pc() / getchar_pc()."),
                ("🎯 Tác dụng:", "Giao tiếp Host CLI 9600 bps quản trị SoC.")
            ]
        ),
        (
            "0x4000_0000",
            "• C: REG_GPIO_LEDS (0x40000000)\\n• RTL: soc_gpio_mmio.v",
            [
                ("👉 Cách dùng:", "Ghi bitmask 16-bit điều khiển I/O."),
                ("🎯 Tác dụng:", "Báo LED xác thực và đóng/ngắt Relay mở cửa.")
            ]
        ),
        (
            "0x0030_0000\\n(Sector 48)",
            "• C: USER_FLASH_ADDR (0x00300000)\\n• NVM: SPI Flash Sector 48",
            [
                ("👉 Cách dùng:", "Nạp buffer thẻ ghi vào SPI Flash."),
                ("🎯 Tác dụng:", "Lưu cố định danh sách Whitelist khi mất nguồn.")
            ]
        ),
        (
            "0x0031_0000\\n(Sector 49)",
            "• C: LOG_FLASH_ADDR (0x00310000)\\n• NVM: SPI Flash Sector 49",
            [
                ("👉 Cách dùng:", "Ghi nối tiếp bản ghi AccessLog_t."),
                ("🎯 Tác dụng:", "Lưu vết lịch sử quét thẻ an ninh chống ghi đè.")
            ]
        ),
        (
            "0x0200_0000\\n(1KB SRAM)",
            "• LDS: sections.lds (ORIGIN 0x02000000)\\n• RTL: data_sram.v (1KB SPRAM)",
            [
                ("👉 Cách dùng:", "Chứa Stack, .data và nạp flashio_worker."),
                ("🎯 Tác dụng:", "CPU chạy trong RAM khi Flash bận xóa/ghi.")
            ]
        )
    ]

    for row_idx, (addr_txt, decl_txt, use_bullets) in enumerate(table_rows_data, start=1):
        bg_col = RGBColor(255, 255, 255) if row_idx % 2 == 1 else RGBColor(248, 250, 252)

        # Col 0: Address
        cell0 = table.cell(row_idx, 0)
        cell0.fill.solid()
        cell0.fill.fore_color.rgb = bg_col
        cell0.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell0.margin_left = cell0.margin_right = Inches(0.08)
        cell0.margin_top = cell0.margin_bottom = Inches(0.03)
        p0 = cell0.text_frame.paragraphs[0]
        p0.text = addr_txt
        p0.font.name = "Consolas"
        p0.font.size = Pt(12.0)
        p0.font.bold = True
        p0.font.color.rgb = C_BLUE_ACCENT
        p0.alignment = PP_ALIGN.CENTER

        # Col 1: Declaration in C & RTL
        cell1 = table.cell(row_idx, 1)
        cell1.fill.solid()
        cell1.fill.fore_color.rgb = bg_col
        cell1.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell1.margin_left = cell1.margin_right = Inches(0.08)
        cell1.margin_top = cell1.margin_bottom = Inches(0.03)
        p1 = cell1.text_frame.paragraphs[0]
        p1.text = decl_txt
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(10.8)
        p1.font.color.rgb = C_NAVY_DARK
        p1.line_spacing = 1.18

        # Col 2: Usage and Impact (👉 Cách dùng ➔ 🎯 Tác dụng)
        cell2 = table.cell(row_idx, 2)
        cell2.fill.solid()
        cell2.fill.fore_color.rgb = bg_col
        cell2.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell2.margin_left = cell2.margin_right = Inches(0.08)
        cell2.margin_top = cell2.margin_bottom = Inches(0.03)
        tf2 = cell2.text_frame
        tf2.word_wrap = True

        for b_idx, (b_label, b_desc) in enumerate(use_bullets):
            p2 = tf2.paragraphs[0] if b_idx == 0 else tf2.add_paragraph()
            p2.text = f"{b_label} {b_desc}"
            p2.font.name = "Segoe UI"
            p2.font.size = Pt(12.0)
            p2.font.color.rgb = C_TEXT_DARK
            p2.line_spacing = 1.16
            if b_idx == 0:
                p2.space_after = Pt(3.0)
'''

# Slide 5 code: Host console matching exact host/main.c print_menu implementation
slide5_code_custom = '''
    # =========================================================================
    # SLIDE 05: PHẦN 5 - DEMO THỰC NGHIỆM: CÁC KỊCH BẢN & GIAO DIỆN HOST CONSOLE
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Phần 5: Demo Chức Năng Sản Phẩm",
               "Các Kịch Bản Thực Nghiệm & Giao Diện Quản Trị Host Console", 5, total_slides=TOTAL_SLIDES)

    lx21 = Inches(0.8)
    lw21 = Inches(5.85)
    cli_lines = [
        "===============================================================",
        "     RDM6300 RFID - PICORV32 - BASYS 3 SPI FLASH MANAGER      ",
        "===============================================================",
        "  [1]  Ping Hardware (Kiem tra ket noi PicoRV32)",
        "  [2]  Input & Save New RFID Tag (Nhap 10 so in tren the luu Flash)",
        "  [3]  Check RFID Tag in Flash (Kiem tra the da co trong Flash)",
        "  [4]  Delete RFID Tag from Flash (Nhap 10 so de xoa khoi Flash)",
        "  [5]  Virtual Scan (Quet the ao: Nhap 10 so in tren the)",
        "  [6]  View Access Logs from Flash (Xem nhat ky Flash 0x310000)",
        "  [7]  Erase Access Logs (Sao luu CSV roi xoa nhat ky Flash)",
        "  [8]  Export RFID Tags to CSV (Xuat danh sach the ra file CSV)",
        "  [9]  Import RFID Tags from Latest CSV (Xoa Flash & Nap CSV)",
        "  [0]  Exit (Thoat)",
        "---------------------------------------------------------------",
        "Lua chon cua ban [0-9]: _"
    ]
    add_code_box(s5, lx21, Inches(1.30), lw21, Inches(5.60), "Menu Host Console CLI (host/main.c)", cli_lines, status_text="=== GIAO DIỆN QUẢN TRỊ TRÊN HOST PC GIAO TIẾP VỚI PICORV32 ===", font_size=10.5, line_spacing=1.55, title_color=RGBColor(52, 211, 153))

    rx21 = Inches(6.80)
    rw21 = Inches(5.73)
    add_card(s5, rx21, Inches(1.30), rw21, Inches(5.60), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
    tb_r21 = s5.shapes.add_textbox(rx21 + Inches(0.20), Inches(1.42), rw21 - Inches(0.40), Inches(5.35))
    tf_r21 = tb_r21.text_frame
    tf_r21.word_wrap = True

    pr21 = tf_r21.paragraphs[0]
    pr21.text = "ÁNH XẠ LỆNH HOST VÀO FIRMWARE C (MAIN.C)"
    pr21.font.name = "Segoe UI"
    pr21.font.size = Pt(14.0)
    pr21.font.bold = True
    pr21.font.color.rgb = C_BLUE_ACCENT
    pr21.space_after = Pt(8)

    fw_cases = [
        ("• [1] Ping Hardware ➔ case 'P':", "Phản hồi 'PONG: PicoRV32 Active', kiểm tra kết nối CPU & UART."),
        ("• [2] Save New Tag ➔ case 'N':", "Nạp 10 số in trên thẻ vào Flash Sector 48 (địa chỉ 0x0030_0000)."),
        ("• [3] Check Tag ➔ case 'C':", "Tra cứu xem mã thẻ đã tồn tại trong Whitelist SPI Flash hay chưa."),
        ("• [4] Delete Tag ➔ case 'K':", "Xóa duy nhất 1 thẻ chỉ định trong Flash bằng cách ghi đè Magic word."),
        ("• [5] Virtual Scan ➔ case 'V':", "Mô phỏng quẹt thẻ ảo từ terminal máy tính để kiểm tra xác thực."),
        ("• [6] View Logs ➔ case 'L':", "Đọc toàn bộ lịch sử quét thẻ từ Flash Sector 49 (địa chỉ 0x0031_0000)."),
        ("• [7] Erase Logs ➔ case 'X':", "Firmware xóa trắng Sector 49 (Host tự gửi 'L' sao lưu CSV trên PC trước)."),
        ("• [8] & [9] Quản lý CSV (Host PC):", "Host tự xử lý file CSV; gửi lệnh 'F' (đọc thẻ) hoặc 'E'+'N' (nạp thẻ) sang SoC.")
    ]

    for c_lbl, c_val in fw_cases:
        p = tf_r21.add_paragraph()
        p.text = f"{c_lbl} {c_val}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(12.0)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(6.5)
        p.line_spacing = 1.15
'''

# Slide 6 code: UART Architecture with shorter content and larger font size
slide6_code_custom = '''
    # =========================================================================
    # SLIDE 06: PHẦN 3 - SƠ ĐỒ KHỐI KIẾN TRÚC VI MẠCH UART RTL & ĐẶC TẢ THIẾT KẾ
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Phần 3: Kiến Trúc Khối Ngoại Vi UART",
               "Sơ Đồ Khối Kiến Trúc Vi Mạch UART RTL (Draw.io Đen Trắng & Đặc Tả Thiết Kế)", 6, total_slides=TOTAL_SLIDES)

    if os.path.exists(img_uart_bw):
        add_card(s6, Inches(0.8), Inches(1.30), Inches(5.75), Inches(5.60), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
        s6.shapes.add_picture(img_uart_bw, Inches(0.95), Inches(1.45), Inches(5.45), Inches(5.30))

    rx8 = Inches(6.75)
    rw8 = Inches(5.78)
    add_card(s6, rx8, Inches(1.30), rw8, Inches(5.60), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
    tb_r8 = s6.shapes.add_textbox(rx8 + Inches(0.20), Inches(1.42), rw8 - Inches(0.40), Inches(5.35))
    tf_r8 = tb_r8.text_frame
    tf_r8.word_wrap = True

    p_r8_h = tf_r8.paragraphs[0]
    p_r8_h.text = "ĐẶC TẢ THIẾT KẾ 5 TẦNG PHẦN CỨNG UART RTL"
    p_r8_h.font.name = "Segoe UI"
    p_r8_h.font.bold = True
    p_r8_h.font.size = Pt(14.5)
    p_r8_h.font.color.rgb = C_BLUE_ACCENT
    p_r8_h.space_after = Pt(10)

    uart_stages_short = [
        ("TẦNG 1: ĐỒNG BỘ 2-FF CDC (sync_2ff.v)", C_ROSE,
         "• Khử siêu ổn định (Metastability) tín hiệu rx_i 125kHz; MTBF > 1.000 năm trên SkyWater 130nm."),
        ("TẦNG 2 & 3: TẠO BAUD & MÁY TRẠNG THÁI RX (simpleuart.v)", C_AMBER,
         "• Chia tần số cfg_divider = 5208 (9600 bps); Lấy mẫu 16x bầu đa số 3 mẫu & bắt khung 8-N-1."),
        ("TẦNG 4: HÀNG ĐỢI FIFO 32 BYTES ĐỘC LẬP (sync_fifo.v)", C_BLUE_ACCENT,
         "• Đệm trọn vẹn 14 byte chuỗi thẻ RFID, chống tràn dữ liệu tuyệt đối khi CPU bận ghi Flash."),
        ("TẦNG 5: GIẢI MÃ BUS MMIO NON-BLOCKING (uart_mmio.v)", C_GREEN,
         "• Ánh xạ 0x1000_0000 / 0x1000_0004; Phản hồi trong 1 chu kỳ 20ns, không bao giờ treo CPU.")
    ]

    for sec_title, sec_col, sec_desc in uart_stages_short:
        p_sec = tf_r8.add_paragraph()
        p_sec.text = sec_title
        p_sec.font.name = "Segoe UI"
        p_sec.font.size = Pt(12.5)
        p_sec.font.bold = True
        p_sec.font.color.rgb = sec_col
        p_sec.space_before = Pt(8)
        p_sec.space_after = Pt(2)

        p_b = tf_r8.add_paragraph()
        p_b.text = sec_desc
        p_b.font.name = "Segoe UI"
        p_b.font.size = Pt(12.0)
        p_b.font.color.rgb = C_TEXT_DARK
        p_b.space_after = Pt(6)
        p_b.line_spacing = 1.15
'''

# Slide 7 code: Waveform timeline occupies most of the slide, 5 scenarios very concise with large font
slide7_code_custom = '''
    # =========================================================================
    # SLIDE 07: PHẦN 4 - HỆ THỐNG TESTBENCH: UART RTL (TB_UART_RTL.V)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Phần 4: Hệ Thống Testbench & Mô Phỏng",
               "Testbench 1: Kiểm Thử Phần Cứng RTL Thuần Cho UART MMIO & FIFO (tb_uart_rtl.v)", 7, total_slides=TOTAL_SLIDES)

    # Khung Timeline Waveform chiếm phần lớn slide (Top / Center)
    add_card(s7, Inches(0.8), Inches(1.30), Inches(11.733), Inches(4.18), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)

    tb_lt = s7.shapes.add_textbox(Inches(0.95), Inches(1.36), Inches(11.433), Inches(0.26))
    tf_lt = tb_lt.text_frame
    tf_lt.margin_left = tf_lt.margin_top = tf_lt.margin_right = tf_lt.margin_bottom = 0
    p_lt = tf_lt.paragraphs[0]
    p_lt.text = "DẠNG SÓNG MÔ PHỎNG TIMELINE VIVADO XSIM (15.275 µs)"
    p_lt.alignment = PP_ALIGN.CENTER
    p_lt.font.name = "Segoe UI"
    p_lt.font.size = Pt(12.0)
    p_lt.font.bold = True
    p_lt.font.color.rgb = C_BLUE_ACCENT

    if os.path.exists(img_tb_uart_rtl):
        # Tăng kích thước ảnh timeline cực lớn để lấp đầy khung
        s7.shapes.add_picture(img_tb_uart_rtl, Inches(1.86), Inches(1.65), Inches(9.60), Inches(3.72))

    # Khung bên dưới: 5 Kịch bản kiểm thử viết rất ngắn gọn & Font chữ to rõ
    add_card(s7, Inches(0.8), Inches(5.58), Inches(8.30), Inches(1.32), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
    tb_sc = s7.shapes.add_textbox(Inches(0.95), Inches(5.64), Inches(8.00), Inches(1.20))
    tf_sc = tb_sc.text_frame
    tf_sc.word_wrap = True
    tf_sc.margin_left = tf_sc.margin_top = tf_sc.margin_right = tf_sc.margin_bottom = 0

    p_sc_h = tf_sc.paragraphs[0]
    p_sc_h.text = "5 KỊCH BẢN KIỂM THỬ RTL THUẦN (XÁC MINH PHẦN CỨNG 100% PASS):"
    p_sc_h.font.name = "Segoe UI"
    p_sc_h.font.size = Pt(11.0)
    p_sc_h.font.bold = True
    p_sc_h.font.color.rgb = C_BLUE_ACCENT
    p_sc_h.space_after = Pt(2)

    short_scenarios = [
        "1. Divider Mặc Định: Prescaler nạp đúng TEST_DIV = 16 ➔ PASS",
        "2. Tái Cấu Hình: Ghi giá trị chia tần mới qua MMIO tức thì ➔ PASS",
        "3. Phát Khung TX: Ký tự 0x4B ('K') xuất chuẩn UART 8-N-1 ➔ PASS",
        "4. Nhận Khung RX: Bắt chuỗi xung rx_i, nạp sạch FIFO (read_val = 75) ➔ PASS",
        "5. Xả Tràn FIFO: Đệm liên tục nhiều byte, đọc cạn trả về 0xFFFFFFFF ➔ PASS"
    ]

    for sc in short_scenarios:
        p = tf_sc.add_paragraph()
        p.text = f"• {sc}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(1.2)
        p.line_spacing = 1.05

    # Huy hiệu kết quả thành công bên dưới góc phải
    add_card(s7, Inches(9.20), Inches(5.58), Inches(3.333), Inches(1.32), bg_color=RGBColor(236, 253, 245), border_color=C_GREEN, border_width=1.5)
    tb_b7 = s7.shapes.add_textbox(Inches(9.32), Inches(5.68), Inches(3.10), Inches(1.12))
    tf_b7 = tb_b7.text_frame
    tf_b7.word_wrap = True
    tf_b7.margin_left = tf_b7.margin_top = tf_b7.margin_right = tf_b7.margin_bottom = 0

    pb7_1 = tf_b7.paragraphs[0]
    pb7_1.text = "XÁC NHẬN VIVADO XSIM:"
    pb7_1.font.name = "Segoe UI"
    pb7_1.font.size = Pt(11.0)
    pb7_1.font.bold = True
    pb7_1.font.color.rgb = C_GREEN
    pb7_1.space_after = Pt(2)

    pb7_2 = tf_b7.add_paragraph()
    pb7_2.text = "100% PASS (5/5 TEST SCENARIOS)\\nRUNTIME: 15.275 µs | SỐ LỖI: 0"
    pb7_2.font.name = "Segoe UI"
    pb7_2.font.size = Pt(10.5)
    pb7_2.font.bold = True
    pb7_2.font.color.rgb = RGBColor(6, 95, 70)
    pb7_2.line_spacing = 1.15
'''

# Slide 8 code: Code box & Vivado log occupies the entire slide with large font
slide8_code_custom = '''
    # =========================================================================
    # SLIDE 08: PHẦN 4 - HỆ THỐNG TESTBENCH: TOP SOC BOOT & PING (TB_UART_PING.V)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Phần 4: Hệ Thống Testbench & Mô Phỏng",
               "Testbench 2: Kiểm Thử Tích Hợp Toàn Diện Top SoC Boot Flash & Ping (tb_uart_ping.v)", 8, total_slides=TOTAL_SLIDES)

    lx21 = Inches(0.8)
    lw21 = Inches(11.733)
    code_lines_ping = [
        "// === tb/tb_uart_ping.v: KỊCH BẢN KIỂM THỬ TÍCH HỢP TOÀN DIỆN TOP SOC ===",
        "initial begin",
        "    clk = 0; rst_n = 0; rdm6300_rx_i = 1; uart_rx_i = 1;",
        "    #200; rst_n = 1;                 // Giải phóng Reset ➔ CPU thức dậy & Boot Flash 0x250000",
        "    wait(ready_matched == 1'b1);     // Đợi CPU PicoRV32 thực thi xong Banner C",
        "    #100000; send_pc_byte(\\"P\\");      // Host PC gửi byte lệnh Ping ('P' = 0x50)",
        "    send_pc_byte(8'h0A);             // Gửi ký tự kết thúc dòng '\\\\n' (0x0A)",
        "    wait(pong_matched == 1'b1);      // Đợi CPU nhận diện và phản hồi chuỗi PONG",
        "    if (pong_matched && !cpu_trap)   $display(\\"  [SUCCESS] PING-PONG TEST PASSED!\\");",
        "end",
        "",
        "// === VIVADO SIMULATOR (XSIM) EXECUTION OUTPUT LOG ===",
        "[FLASH MODEL] Loaded 2048 words (8192 bytes) from firmware.hex",
        "[TB] System Reset released. PicoRV32 booting from 0x250000...",
        "[UART TX] ========================================================================",
        "[UART TX]            RDM6300 PICORV32 SOC ACCESS CONTROLLER READY                 ",
        "[UART TX] ========================================================================",
        "[TB] Boot banner detected! Sending 'P' (Ping) command to SoC...",
        "[HOST -> SOC] Sent Byte: 'P' (0x50), '\\\\n' (0x0A)",
        "[UART TX] PONG: PicoRV32 Active",
        "[SUCCESS] PING-PONG TEST PASSED! PicoRV32 responded with PONG.",
        "cpu_trap = 0 (CPU healthy, no illegal instructions, no stack overflow)"
    ]
    add_code_box(s8, lx21, Inches(1.30), lw21, Inches(5.60), "tb/tb_uart_ping.v [Mã Nguồn Testbench & Nhật Ký Mô Phỏng Vivado XSim]", code_lines_ping, status_text="=== XÁC NHẬN: BOOT FLASH XIP + UART PING-PONG 100% PASS | RUNTIME: 2,086.555 µs | TRAP = 0 ===", font_size=11.5, line_spacing=1.0, title_color=RGBColor(52, 211, 153))
'''

# Slide 9 code: Device setup photo (left) + equipment list only (right), large fonts
slide9_code_custom = '''
    # =========================================================================
    # SLIDE 09: PHẦN 5 - DEMO THỰC NGHIỆM TRÊN FPGA BASYS 3: DANH SÁCH THIẾT BỊ
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Phần 5: Demo Chức Năng Sản Phẩm",
               "Danh Sách Thiết Bị & Thiết Lập Kết Nối Phần Cứng FPGA Basys 3", 9, total_slides=TOTAL_SLIDES)

    # Khung bên trái: Hình ảnh hệ thống thực nghiệm
    add_card(s9, Inches(0.8), Inches(1.30), Inches(5.75), Inches(5.60), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)

    tb_lt9 = s9.shapes.add_textbox(Inches(0.95), Inches(1.42), Inches(5.45), Inches(0.32))
    tf_lt9 = tb_lt9.text_frame
    tf_lt9.margin_left = tf_lt9.margin_top = tf_lt9.margin_right = tf_lt9.margin_bottom = 0
    p_lt9 = tf_lt9.paragraphs[0]
    p_lt9.text = "HỆ THỐNG THỰC NGHIỆM THỰC TẾ"
    p_lt9.alignment = PP_ALIGN.CENTER
    p_lt9.font.name = "Segoe UI"
    p_lt9.font.size = Pt(13.0)
    p_lt9.font.bold = True
    p_lt9.font.color.rgb = C_BLUE_ACCENT

    if os.path.exists(img_device):
        # Tỷ lệ ảnh Device.jpg 1276 x 956 = 1.3347 -> rộng 5.45 inch, cao 4.08 inch
        s9.shapes.add_picture(img_device, Inches(0.95), Inches(1.85), Inches(5.45), Inches(4.08))

    tb_note9 = s9.shapes.add_textbox(Inches(0.95), Inches(6.05), Inches(5.45), Inches(0.75))
    tf_note9 = tb_note9.text_frame
    tf_note9.word_wrap = True
    tf_note9.margin_left = tf_note9.margin_top = tf_note9.margin_right = tf_note9.margin_bottom = 0
    p_note9 = tf_note9.paragraphs[0]
    p_note9.text = "Nguồn 5V riêng cho RDM6300 (chung GND) • Trở 1kΩ nối tiếp TX ➔ JA1 bảo vệ I/O 3.3V"
    p_note9.alignment = PP_ALIGN.CENTER
    p_note9.font.name = "Segoe UI"
    p_note9.font.size = Pt(11.0)
    p_note9.font.italic = True
    p_note9.font.color.rgb = C_TEXT_MUTED
    p_note9.line_spacing = 1.15

    # Khung bên phải: Chỉ liệt kê danh sách thiết bị
    rx9 = Inches(6.75)
    rw9 = Inches(5.78)
    add_card(s9, rx9, Inches(1.30), rw9, Inches(5.60), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
    tb_r9 = s9.shapes.add_textbox(rx9 + Inches(0.25), Inches(1.45), rw9 - Inches(0.50), Inches(5.35))
    tf_r9 = tb_r9.text_frame
    tf_r9.word_wrap = True
    tf_r9.margin_left = tf_r9.margin_top = tf_r9.margin_right = tf_r9.margin_bottom = 0

    p_r9_h = tf_r9.paragraphs[0]
    p_r9_h.text = "DANH SÁCH THIẾT BỊ THỰC NGHIỆM"
    p_r9_h.font.name = "Segoe UI"
    p_r9_h.font.bold = True
    p_r9_h.font.size = Pt(15.0)
    p_r9_h.font.color.rgb = C_BLUE_ACCENT
    p_r9_h.space_after = Pt(10)

    devices = [
        ("Bo mạch FPGA Digilent Basys 3", "Artix-7 XC7A35T, SPI Flash 32Mbit"),
        ("Module RFID RDM6300", "125 kHz, kèm ăng-ten cuộn dây"),
        ("Thẻ RFID EM4100", "Thẻ từ 125 kHz mẫu"),
        ("Module nguồn MB102 + Adapter DC", "Cấp 5V cho RDM6300"),
        ("Điện trở 1kΩ", "Nối tiếp chân TX RDM6300 ➔ JA1"),
        ("Breadboard & dây cắm", "Đấu nối mạch thử nghiệm"),
        ("Cáp Micro-USB", "Nạp FPGA & UART 9600 bps"),
        ("Máy tính Host PC", "Chạy chương trình Host Console")
    ]

    for d_idx, (d_name, d_spec) in enumerate(devices, start=1):
        p = tf_r9.add_paragraph()
        p.space_before = Pt(7)
        p.text = f"{d_idx}. {d_name}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(15.0)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK

        p_s = tf_r9.add_paragraph()
        p_s.text = f"     {d_spec}"
        p_s.font.name = "Segoe UI"
        p_s.font.size = Pt(12.5)
        p_s.font.color.rgb = C_TEXT_MUTED
'''

def fix_slide_numbers(code_block, old_num_str, new_num):
    code_block = code_block.replace(f'total_slides=TOTAL_SLIDES', f'total_slides=TOTAL_SLIDES')
    code_block = code_block.replace(f', {old_num_str}, total_slides=TOTAL_SLIDES)', f', {new_num}, total_slides=TOTAL_SLIDES)')
    code_block = code_block.replace(f'# SLIDE {old_num_str}:', f'# SLIDE {new_num:02d}:')
    code_block = code_block.replace(f'# SLIDE {int(old_num_str)}:', f'# SLIDE {new_num:02d}:')
    return code_block

slide1_code_custom = '''
    # =========================================================================
    # SLIDE 01: TRANG BÌA (Title Slide) - LOGO ECOSYSTEM
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_NAVY_DARK
    bg1.line.fill.background()

    card1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
    card1.fill.solid()
    card1.fill.fore_color.rgb = C_NAVY_MID
    card1.line.color.rgb = C_BLUE_ACCENT
    card1.line.width = Pt(2.0)

    tb1 = s1.shapes.add_textbox(Inches(1.05), Inches(1.02), Inches(11.233), Inches(4.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = 0

    p_org = tf1.paragraphs[0]
    p_org.text = "FPT JETKING — CHIP DESIGN"
    p_org.font.name = "Segoe UI"
    p_org.font.size = Pt(13.5)
    p_org.font.bold = True
    p_org.font.color.rgb = C_CYAN_ACCENT
    p_org.space_after = Pt(12)

    p_main = tf1.add_paragraph()
    p_main.text = "THIẾT KẾ HỆ THỐNG SOC XỬ LÝ DỮ LIỆU THẺ RA VÀO RFID\\nTỐI ƯU RTL TO GDSII TRÊN CHIP ASIC"
    p_main.font.name = "Segoe UI"
    p_main.font.size = Pt(26.0)
    p_main.font.bold = True
    p_main.font.color.rgb = C_WHITE
    p_main.space_after = Pt(14)
    p_main.line_spacing = 1.25

    p_sub = tf1.add_paragraph()
    p_sub.text = "Giao tiếp RFID RDM6300 | Lưu trữ Whitelist SPI Flash NVM | Tạo mẫu Basys 3 FPGA | Ký duyệt ASIC OpenLane 2 (Sky130)"
    p_sub.font.name = "Segoe UI"
    p_sub.font.size = Pt(12.0)
    p_sub.font.color.rgb = RGBColor(203, 213, 225)
    p_sub.space_after = Pt(18)

    p_info1 = tf1.add_paragraph()
    p_info1.text = "Học viên thực hiện :  Thái Tuấn Hiệp"
    p_info1.font.name = "Segoe UI"
    p_info1.font.size = Pt(13.5)
    p_info1.font.bold = True
    p_info1.font.color.rgb = C_WHITE
    p_info1.space_after = Pt(5)

    p_info2 = tf1.add_paragraph()
    p_info2.text = "Giảng viên hướng dẫn :  ThS. Nguyễn Văn Đông"
    p_info2.font.name = "Segoe UI"
    p_info2.font.size = Pt(12.5)
    p_info2.font.color.rgb = RGBColor(226, 232, 240)
    p_info2.space_after = Pt(5)

    p_info3 = tf1.add_paragraph()
    p_info3.text = "Học kỳ :  SEM3  |  Chuyên ngành: Thiết kế Vi mạch Bán dẫn (Chip Design)"
    p_info3.font.name = "Segoe UI"
    p_info3.font.size = Pt(11.5)
    p_info3.font.italic = True
    p_info3.font.color.rgb = RGBColor(148, 163, 184)

    # Logo header label
    tb_lbl = s1.shapes.add_textbox(Inches(1.05), Inches(5.32), Inches(11.233), Inches(0.28))
    tf_lbl = tb_lbl.text_frame
    tf_lbl.margin_left = tf_lbl.margin_right = tf_lbl.margin_top = tf_lbl.margin_bottom = 0
    p_l = tf_lbl.paragraphs[0]
    p_l.text = "CÔNG CỤ EDA & HỆ SINH THÁI CÔNG NGHỆ SỬ DỤNG TRONG ĐỒ ÁN:"
    p_l.font.name = "Segoe UI"
    p_l.font.size = Pt(10.5)
    p_l.font.bold = True
    p_l.font.color.rgb = C_CYAN_ACCENT

    # Logo search directories
    logo_candidates = [
        os.path.join(cur_dir, "logos"),
        os.path.join(doc_dir, "logos"),
        os.path.join(cur_dir, "temp", "logos"),
        os.path.join(project_root, "rdm6300-picorv32-rom-data", "document", "logos"),
    ]
    resolved_logo_dir = cur_dir
    for ld in logo_candidates:
        if os.path.exists(ld):
            resolved_logo_dir = ld
            break

    badges_list = [
        ("badge_openlane.png", 247, 87),
        ("badge_vivado.png", 240, 87),
        ("badge_fpga.png", 254, 87),
        ("badge_riscv.png", 381, 87),
        ("badge_skywater.png", 290, 87),
    ]

    b_h = Inches(0.72)
    b_widths = [b_h * (w / h) for _, w, h in badges_list]
    tot_bw = sum(b_widths)
    av_w = Inches(11.233)
    b_gap = (av_w - tot_bw) / (len(badges_list) - 1)
    bx = Inches(1.05)
    by = Inches(5.66)

    for (b_fname, _, _), bw in zip(badges_list, b_widths):
        bp = os.path.join(resolved_logo_dir, b_fname)
        if os.path.exists(bp):
            s1.shapes.add_picture(bp, bx, by, bw, b_h)
        bx += bw + b_gap
'''

# Adjust headers and slide numbers
s1_text = slide1_code_custom
s2_text = ''.join(slide2_code).replace(', 2, total_slides=TOTAL_SLIDES)', ', 2, total_slides=TOTAL_SLIDES)')
# Slide 2: larger body fonts
s2_text = (s2_text.replace('r_lbl.font.size = Pt(11.5)', 'r_lbl.font.size = Pt(12.0)')
                  .replace('r_val.font.size = Pt(10.5)', 'r_val.font.size = Pt(11.5)')
                  .replace('p_hs.font.size = Pt(10.0)', 'p_hs.font.size = Pt(11.0)')
                  .replace('p.space_after = Pt(16)', 'p.space_after = Pt(10)'))
s3_text = ''.join(slide3_code).replace(', 3, total_slides=TOTAL_SLIDES)', ', 3, total_slides=TOTAL_SLIDES)')
s4_text = slide4_code
s5_text = slide5_code_custom
s6_text = slide6_code_custom
s7_text = slide7_code_custom
s8_text = slide8_code_custom
s9_text = slide9_code_custom
s10_text = fix_slide_numbers(''.join(slide10_code), '8', 10).replace(', 9, total_slides=TOTAL_SLIDES)', ', 10, total_slides=TOTAL_SLIDES)').replace(', 8, total_slides=TOTAL_SLIDES)', ', 10, total_slides=TOTAL_SLIDES)').replace(', 24, total_slides=TOTAL_SLIDES)', ', 10, total_slides=TOTAL_SLIDES)')
s11_text = fix_slide_numbers(''.join(slide11_code), '9', 11).replace(', 10, total_slides=TOTAL_SLIDES)', ', 11, total_slides=TOTAL_SLIDES)').replace(', 9, total_slides=TOTAL_SLIDES)', ', 11, total_slides=TOTAL_SLIDES)').replace(', 25, total_slides=TOTAL_SLIDES)', ', 11, total_slides=TOTAL_SLIDES)')
s12_text = fix_slide_numbers(''.join(slide12_code), '10', 12).replace(', 11, total_slides=TOTAL_SLIDES)', ', 12, total_slides=TOTAL_SLIDES)').replace(', 10, total_slides=TOTAL_SLIDES)', ', 12, total_slides=TOTAL_SLIDES)').replace(', 26, total_slides=TOTAL_SLIDES)', ', 12, total_slides=TOTAL_SLIDES)')
s13_text = ''.join(slide13_code)

# Slide 10 (config.json + sign-off): larger code & summary fonts
s10_text = (s10_text.replace('font_size=8.2, line_spacing=1.08)', 'font_size=10.5, line_spacing=1.12)')
                    .replace('p_c2.font.size = Pt(10.5)', 'p_c2.font.size = Pt(11.0)')
                    .replace('p_ss_h.font.size = Pt(11.5)', 'p_ss_h.font.size = Pt(12.0)')
                    .replace('p_item.font.size = Pt(8.5)', 'p_item.font.size = Pt(9.8)'))

# Slide 12 (STA): larger table + bullet fonts
s12_text = (s12_text.replace('p.font.size = Pt(11.0)', 'p.font.size = Pt(11.5)')
                    .replace('p.font.size = Pt(10.0)', 'p.font.size = Pt(10.5)')
                    .replace('p.font.size = Pt(8.5)', 'p.font.size = Pt(10.5)')
                    .replace('p_cl_h.font.size = Pt(11.0)', 'p_cl_h.font.size = Pt(12.0)')
                    .replace('p_cr_h.font.size = Pt(11.0)', 'p_cr_h.font.size = Pt(12.0)'))

# Update TOTAL_SLIDES in header
header_text = ''.join(header_setup)
header_text = header_text.replace('TOTAL_SLIDES = 10', 'TOTAL_SLIDES = 13')
header_text = header_text.replace('TOTAL_SLIDES = 11', 'TOTAL_SLIDES = 13')
header_text = header_text.replace('TOTAL_SLIDES = 12', 'TOTAL_SLIDES = 13')
header_text = header_text.replace('TOTAL_SLIDES = 26', 'TOTAL_SLIDES = 13')
# Code box helper: larger title & status line
header_text = header_text.replace('p_t.font.size = Pt(9.5)', 'p_t.font.size = Pt(10.5)')
header_text = header_text.replace('p_s.font.size = Pt(8.2)', 'p_s.font.size = Pt(9.5)')

full_script = header_text + s1_text + s2_text + s3_text + s4_text + s5_text + s6_text + s7_text + s8_text + s9_text + s10_text + s11_text + s12_text + s13_text

# Write out the finalized create_presentation.py
with open('rdm6300-picorv32-rom-data/document/temp/create_presentation.py', 'w', encoding='utf-8') as f:
    f.write(full_script)

print("Successfully generated create_presentation.py from original git commits!")
