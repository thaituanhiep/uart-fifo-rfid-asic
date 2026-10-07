import os

def update_slide5_firmware():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    target_file = os.path.join(cur_dir, "create_presentation.py")

    with open(target_file, "r", encoding="utf-8") as f:
        code = f.read()

    # Old right side code for Slide 5
    old_right_start = '    # Khung bên phải: Nhận xét và đánh giá chuyên sâu các chức năng'
    old_right_end = '    # =========================================================================\n    # SLIDE 4: PHẦN 3 - SƠ ĐỒ KHỐI KIẾN TRÚC VI MẠCH UART RTL & ĐẶC TẢ THIẾT KẾ'
    if old_right_end not in code:
        old_right_end = 's8 = prs.slides.add_slide(blank_layout)'

    idx_start = code.find(old_right_start)
    idx_end = code.find(old_right_end, idx_start)
    # Find comment before s8
    idx_end_comment = code.rfind("    # ===", idx_start, idx_end)

    new_right_code = '''    # Khung bên phải: Các chức năng nghiệp vụ Firmware C làm được
    card_r21 = add_card(s23, Inches(6.75), Inches(1.35), Inches(5.78), Inches(5.50), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)

    tb_r21 = s23.shapes.add_textbox(Inches(7.05), Inches(1.50), Inches(5.25), Inches(5.20))
    tf_r21 = tb_r21.text_frame
    tf_r21.word_wrap = True
    tf_r21.margin_left = tf_r21.margin_top = tf_r21.margin_right = tf_r21.margin_bottom = 0

    p_r21_h = tf_r21.paragraphs[0]
    p_r21_h.text = "CÁC CHỨC NĂNG NGHIỆP VỤ FIRMWARE C HIỆN THỰC"
    p_r21_h.font.name = "Segoe UI"
    p_r21_h.font.bold = True
    p_r21_h.font.size = Pt(11.5)
    p_r21_h.font.color.rgb = C_BLUE_ACCENT
    p_r21_h.space_after = Pt(4)

    firmware_functions_sections = [
        ("1. KHỞI TẠO & ĐIỀU KHIỂN PHẦN CỨNG MMIO", C_BLUE_ACCENT, [
            ("Cấu hình UART & 1KB SRAM:", "Thiết lập REG_RFID_UART_DIV = 5208 (9600 bps), REG_PC_UART_DIV = 434 (115200 bps); khởi tạo con trỏ Stack sp trên SRAM nội."),
            ("Phản hồi tức thì & LED GPIO:", "Xử lý gói Ping kiểm tra kết nối PicoRV32 trong < 1 µs; điều khiển 5 LED trạng thái (Alive, Granted, Warn, Flash Busy).")
        ]),
        ("2. GIẢI MÃ & KIỂM ĐỊNH FRAME THẺ RFID 125KHZ", C_AMBER, [
            ("Đọc FIFO & Bóc tách Frame:", "Rút dữ liệu từ RX FIFO 32B qua MMIO non-blocking; nhận diện Start STX (0x02), trích xuất 10 ký tự ASCII UID và chốt End ETX (0x03)."),
            ("Kiểm toán Checksum & Watchdog:", "Tính toán mã kiểm tra XOR LRC 2-byte xác thực tính toàn vẹn; cơ chế Watchdog 10ms tự reset buffer khi frame bị nhiễu.")
        ]),
        ("3. QUẢN LÝ DATABASE WHITELIST TRÊN FLASH (0x300000)", C_GREEN, [
            ("Tra cứu XIP tốc độ cao:", "Tra cứu trực tiếp danh sách 4.096 thẻ hợp lệ từ Sector 48 qua bus XIP, thuật toán dừng sớm cho độ trễ < 10 µs."),
            ("In-RAM Flash Programming:", "Nạp flashio_worker() vào SRAM để xóa Sector (0x20) và ghi thẻ mới (0x02) an toàn, không làm treo bus CPU.")
        ]),
        ("4. KIỂM TOÁN AN NINH & GHI ACCESS LOGS (0x310000)", C_ROSE, [
            ("Lưu 512 bản ghi nhật ký:", "Tự động đóng gói bản ghi 16-byte (Magic SUCC/FAIL + UID + Timestamp + Counter) ghi bền vững vào Sector 49."),
            ("Đồng bộ & Backup CSV:", "Hỗ trợ xuất toàn bộ 512 log ra Host Console CLI máy tính và tự động sao lưu CSV trước khi thực hiện lệnh xóa sạch log.")
        ])
    ]

    for sec_idx, (sec_title, sec_col, sec_bullets) in enumerate(firmware_functions_sections):
        p_sec = tf_r21.add_paragraph()
        p_sec.text = sec_title
        p_sec.font.name = "Segoe UI"
        p_sec.font.size = Pt(8.8)
        p_sec.font.bold = True
        p_sec.font.color.rgb = sec_col
        p_sec.space_before = Pt(3)
        p_sec.space_after = Pt(1)

        for b_lbl, b_val in sec_bullets:
            p_b = tf_r21.add_paragraph()
            p_b.text = f"• {b_lbl} {b_val}"
            p_b.font.name = "Segoe UI"
            p_b.font.size = Pt(7.8)
            p_b.font.color.rgb = C_TEXT_DARK
            p_b.space_after = Pt(1.5)
            p_b.line_spacing = 1.10'''

    code_new = code[:idx_start] + new_right_code + "\n\n" + code[idx_end_comment:]

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(code_new)

    print("Updated Slide 5 right column with Firmware Capabilities successfully!")

if __name__ == "__main__":
    update_slide5_firmware()
