import os

def update_slide5_concise():
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

    new_right_code = '''    # Khung bên phải: Liệt kê chức năng ngắn gọn theo switch-case main.c (Font to, rõ nét)
    card_r21 = add_card(s23, Inches(6.75), Inches(1.35), Inches(5.78), Inches(5.50), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)

    tb_r21 = s23.shapes.add_textbox(Inches(6.95), Inches(1.48), Inches(5.38), Inches(5.24))
    tf_r21 = tb_r21.text_frame
    tf_r21.word_wrap = True
    tf_r21.margin_left = tf_r21.margin_top = tf_r21.margin_right = tf_r21.margin_bottom = 0

    p_r21_h = tf_r21.paragraphs[0]
    p_r21_h.text = "XỬ LÝ LỆNH TRONG FIRMWARE (SWITCH-CASE MAIN.C)"
    p_r21_h.font.name = "Segoe UI"
    p_r21_h.font.bold = True
    p_r21_h.font.size = Pt(12.0)
    p_r21_h.font.color.rgb = C_BLUE_ACCENT
    p_r21_h.space_after = Pt(6)

    firmware_cases_sections = [
        ("1. KIỂM THỬ KẾT NỐI & CHẨN ĐOÁN HỆ THỐNG", C_BLUE_ACCENT, [
            ("case 'P': Ping ->", "Phản hồi 'PONG: PicoRV32 Active', kiểm tra bus & UART FIFO."),
            ("case 'S': Status ->", "Đọc Flash ID (0x9F), Flash Status Reg và các bit LED GPIO.")
        ]),
        ("2. QUẢN TRỊ WHITELIST TRÊN FLASH (SECTOR 48)", C_GREEN, [
            ("case 'W' / 'N': Save Tag ->", "Gọi flash_save_tag(hi, lo), lưu vào Sector 48, bật LED Save."),
            ("case 'C': Check Tag ->", "Gọi flash_find_tag(hi, lo) tra cứu thẻ trong Whitelist qua XIP."),
            ("case 'K': Delete Tag ->", "Gọi flash_delete_tag(slot) nạp flashio_worker() vào RAM xóa thẻ an toàn."),
            ("case 'F' & 'E': Dump / Erase ->", "flash_dump_all_tags() xuất CSV & flash_erase_tags_sector() xóa sạch.")
        ]),
        ("3. QUẢN TRỊ NHẬT KÝ KIỂM TOÁN ACCESS LOGS (SECTOR 49)", C_ROSE, [
            ("case 'L': View Logs ->", "flash_dump_all_logs() đọc 512 bản ghi nhật ký (Magic, UID, Timestamp)."),
            ("case 'X': Erase Logs ->", "flash_erase_logs_sector() xóa toàn bộ Sector 49 sau khi Host backup CSV.")
        ]),
        ("4. GIẢ LẬP QUẸT THẺ & TRUY VẤN DỮ LIỆU TỪ XA", C_AMBER, [
            ("case 'V': Virtual Scan ->", "Gọi access_control_process_card() đối chiếu Whitelist & bật LED mở cửa."),
            ("case 'R': Read Tag ->", "Đọc chuỗi 10 số ASCII thẻ vừa quẹt từ access_control_get_last_tag().")
        ])
    ]

    for sec_idx, (sec_title, sec_col, sec_bullets) in enumerate(firmware_cases_sections):
        p_sec = tf_r21.add_paragraph()
        p_sec.text = sec_title
        p_sec.font.name = "Segoe UI"
        p_sec.font.size = Pt(9.6)
        p_sec.font.bold = True
        p_sec.font.color.rgb = sec_col
        p_sec.space_before = Pt(5)
        p_sec.space_after = Pt(2)

        for b_lbl, b_val in sec_bullets:
            p_b = tf_r21.add_paragraph()
            p_b.space_after = Pt(2)
            p_b.line_spacing = 1.15

            r_tag = p_b.add_run()
            r_tag.text = f"• {b_lbl} "
            r_tag.font.name = "Consolas"
            r_tag.font.size = Pt(8.8)
            r_tag.font.bold = True
            r_tag.font.color.rgb = C_BLUE_ACCENT if "Ping" in b_lbl or "Status" in b_lbl else (C_GREEN if "Save" in b_lbl or "Check" in b_lbl or "Dump" in b_lbl else (C_ROSE if "Delete" in b_lbl or "Logs" in b_lbl else C_AMBER))

            r_desc = p_b.add_run()
            r_desc.text = b_val
            r_desc.font.name = "Segoe UI"
            r_desc.font.size = Pt(8.6)
            r_desc.font.color.rgb = C_TEXT_DARK'''

    code_new = code[:idx_start] + new_right_code + "\n\n" + code[idx_end_comment:]

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(code_new)

    print("Updated Slide 5 right column with concise cases and larger fonts successfully!")

if __name__ == "__main__":
    update_slide5_concise()
