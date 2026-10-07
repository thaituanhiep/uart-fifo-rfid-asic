import os

def update_slide5_cases():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    target_file = os.path.join(cur_dir, "create_presentation.py")

    with open(target_file, "r", encoding="utf-8") as f:
        code = f.read()

    # Find the right column block in Slide 5
    old_right_start = '    # Khung bên phải: Liệt kê chức năng theo các case trong Firmware main.c'
    if old_right_start not in code:
        old_right_start = 'card_r21 = add_card(s23,'
        idx_start = code.find(old_right_start)
        idx_start = code.rfind("    #", 0, idx_start)
    else:
        idx_start = code.find(old_right_start)

    old_right_end = 's8 = prs.slides.add_slide(blank_layout)'
    idx_end = code.find(old_right_end, idx_start)
    idx_end_comment = code.rfind("    # ===", idx_start, idx_end)

    new_right_code = '''    # Khung bên phải: Liệt kê chức năng theo các case trong Firmware main.c
    card_r21 = add_card(s23, Inches(6.75), Inches(1.35), Inches(5.78), Inches(5.50), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)

    tb_r21 = s23.shapes.add_textbox(Inches(7.05), Inches(1.50), Inches(5.25), Inches(5.20))
    tf_r21 = tb_r21.text_frame
    tf_r21.word_wrap = True
    tf_r21.margin_left = tf_r21.margin_top = tf_r21.margin_right = tf_r21.margin_bottom = 0

    p_r21_h = tf_r21.paragraphs[0]
    p_r21_h.text = "XỬ LÝ LỆNH TRONG FIRMWARE (SWITCH-CASE MAIN.C)"
    p_r21_h.font.name = "Segoe UI"
    p_r21_h.font.bold = True
    p_r21_h.font.size = Pt(11.5)
    p_r21_h.font.color.rgb = C_BLUE_ACCENT
    p_r21_h.space_after = Pt(4)

    firmware_cases_sections = [
        ("1. KIỂM THỬ KẾT NỐI & CHẨN ĐOÁN HỆ THỐNG", C_BLUE_ACCENT, [
            ("case 'P': Ping Hardware ->", "Phản hồi 'PONG: PicoRV32 Active' — Xác nhận CPU RISC-V, bus interconnect và UART FIFO hoạt động tốt."),
            ("case 'S': Query SoC Status ->", "Đọc Flash ID (0x9F), Flash Status Reg (0x05) và trạng thái các bit đèn LED GPIO (REG_GPIO_LEDS).")
        ]),
        ("2. QUẢN TRỊ DANH SÁCH THẺ WHITELIST (FLASH SECTOR 48)", C_GREEN, [
            ("case 'W' / 'N': Save Tag ->", "Gọi flash_save_tag(hi, lo) — Ghi thẻ vào Sector 48 (0x300000), phản hồi vị trí Slot và bật LED Save."),
            ("case 'C': Check Tag ->", "Gọi flash_find_tag(hi, lo) — Tra cứu thẻ trong Whitelist qua bus XIP, trả về OK:TAG_FOUND:SLOT."),
            ("case 'K': Delete Tag ->", "Gọi flash_delete_tag(slot) — Nạp flashio_worker() vào RAM xóa thẻ an toàn, không treo bus XIP."),
            ("case 'F' & 'E': Dump / Erase ->", "flash_dump_all_tags() xuất danh sách thẻ ra CSV; flash_erase_tags_sector() xóa sạch Sector 48.")
        ]),
        ("3. QUẢN TRỊ NHẬT KÝ KIỂM TOÁN ACCESS LOGS (FLASH SECTOR 49)", C_ROSE, [
            ("case 'L': Read Access Logs ->", "flash_dump_all_logs() đọc 512 bản ghi 16-byte (Magic SUCC/FAIL, UID, Timestamp, Lượt quẹt)."),
            ("case 'X': Erase Access Logs ->", "flash_erase_logs_sector() xóa toàn bộ Sector 49 (0x310000) sau khi Host đã backup ra file CSV.")
        ]),
        ("4. GIẢ LẬP QUẸT THẺ & TRUY VẤN DỮ LIỆU TỪ XA", C_AMBER, [
            ("case 'V': Virtual Scan ->", "Gọi access_control_process_card() — Giả lập quẹt thẻ từ bàn phím, đối chiếu Whitelist & bật LED mở cửa."),
            ("case 'R': Query Last Tag ->", "Đọc chuỗi 10 số ASCII thẻ vừa quẹt gần nhất từ bộ đệm access_control_get_last_tag().")
        ])
    ]

    for sec_idx, (sec_title, sec_col, sec_bullets) in enumerate(firmware_cases_sections):
        p_sec = tf_r21.add_paragraph()
        p_sec.text = sec_title
        p_sec.font.name = "Segoe UI"
        p_sec.font.size = Pt(8.6)
        p_sec.font.bold = True
        p_sec.font.color.rgb = sec_col
        p_sec.space_before = Pt(2.5)
        p_sec.space_after = Pt(1)

        for b_lbl, b_val in sec_bullets:
            p_b = tf_r21.add_paragraph()
            p_b.text = f"• {b_lbl} {b_val}"
            p_b.font.name = "Segoe UI"
            p_b.font.size = Pt(7.6)
            p_b.font.color.rgb = C_TEXT_DARK
            p_b.space_after = Pt(1.2)
            p_b.line_spacing = 1.08'''

    code_new = code[:idx_start] + new_right_code + "\n\n" + code[idx_end_comment:]

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(code_new)

    print("Updated Slide 5 right column cleanly!")

if __name__ == "__main__":
    update_slide5_cases()
