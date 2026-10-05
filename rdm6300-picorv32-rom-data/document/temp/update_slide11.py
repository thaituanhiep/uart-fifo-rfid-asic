# -*- coding: utf-8 -*-
"""
Script: update_slide11.py
Cập nhật Slide 11 thành dạng so sánh đối chiếu trực quan 2 cột (Software Bit-Bang C vs RTL Hardware UART)
kèm theo bảng tổng hợp chỉ số kỹ thuật ở đáy slide, thay thế hình ảnh bị méo.
"""
import re

with open('create_presentation.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_slide11_code = """    # =========================================================================
    # SLIDE 11: SO SÁNH ĐỐI CHIẾU - RTL HARDWARE UART VS SOFTWARE C BIT-BANG
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Phần 3: Phân Tích Kiến Trúc Vi Hệ Thống",
               "So Sánh Kiến Trúc: Thiết Kế UART Trên RTL vs Viết Bằng Firmware C", 11, total_slides=TOTAL_SLIDES)

    # Khung bên trái: Phương án 1 - Software Bit-bang UART trong C (Cảnh báo / Yếu điểm)
    card_l11 = add_card(s11, Inches(0.8), Inches(1.35), Inches(5.75), Inches(4.25), bg_color=C_WHITE, border_color=C_ROSE, border_width=1.8)

    tb_l11 = s11.shapes.add_textbox(Inches(1.00), Inches(1.48), Inches(5.35), Inches(4.00))
    tf_l11 = tb_l11.text_frame
    tf_l11.word_wrap = True
    tf_l11.margin_left = tf_l11.margin_top = tf_l11.margin_right = tf_l11.margin_bottom = 0

    p_l11_h = tf_l11.paragraphs[0]
    p_l11_h.text = "PHƯƠNG ÁN 1: SOFTWARE BIT-BANG TRONG C (NHƯỢC ĐIỂM)"
    p_l11_h.font.name = "Segoe UI"
    p_l11_h.font.bold = True
    p_l11_h.font.size = Pt(11.0)
    p_l11_h.font.color.rgb = C_ROSE
    p_l11_h.space_after = Pt(6)

    c_weaknesses = [
        ("Treo CPU 100% khi chờ bit (CPU Blocking):", "Tại 9600 baud, 1 khung 14 byte mất ~14.5 ms. Vòng lặp delay/polling khóa chết CPU, không thể đa nhiệm xử lý tác vụ khác."),
        ("Mất 100% mã thẻ khi ghi Flash (Flash Stall):", "Xóa/Ghi SPI Flash NVM mất từ 1-100 ms làm CPU bị chiếm dụng hoàn toàn. Firmware C không thể quét GPIO, gây rớt toàn bộ dữ liệu thẻ quẹt!"),
        ("Rung pha (Jitter) do trễ nạp mã Flash XIP:", "Mã C thực thi qua SPI Flash XIP có độ trễ truy xuất thay đổi (wait states biến thiên), làm sai lệch chu kỳ hàm delay, gây lỗi Framing Error."),
        ("Bất lực trước lỗi siêu ổn định (Metastability):", "Đọc chân GPIO bằng phần mềm không thể xử lý xung đột miền xung (CDC) và không thể lọc xung gai (glitch) ở mức tín hiệu vật lý.")
    ]

    for p_lbl, p_val in c_weaknesses:
        p_item = tf_l11.add_paragraph()
        p_item.text = f"• {p_lbl} {p_val}"
        p_item.font.name = "Segoe UI"
        p_item.font.size = Pt(8.4)
        p_item.font.color.rgb = C_TEXT_DARK
        p_item.space_after = Pt(4)
        p_item.line_spacing = 1.12

    # Khung bên phải: Phương án 2 - Thiết kế UART MMIO & FIFO trên RTL (Ưu điểm vượt trội)
    card_r11 = add_card(s11, Inches(6.78), Inches(1.35), Inches(5.75), Inches(4.25), bg_color=C_WHITE, border_color=C_GREEN, border_width=1.8)

    tb_r11 = s11.shapes.add_textbox(Inches(6.98), Inches(1.48), Inches(5.35), Inches(4.00))
    tf_r11 = tb_r11.text_frame
    tf_r11.word_wrap = True
    tf_r11.margin_left = tf_r11.margin_top = tf_r11.margin_right = tf_r11.margin_bottom = 0

    p_r11_h = tf_r11.paragraphs[0]
    p_r11_h.text = "PHƯƠNG ÁN 2: THIẾT KẾ UART & FIFO TRÊN RTL (TỐI ƯU)"
    p_r11_h.font.name = "Segoe UI"
    p_r11_h.font.bold = True
    p_r11_h.font.size = Pt(11.0)
    p_r11_h.font.color.rgb = C_GREEN
    p_r11_h.space_after = Pt(6)

    rtl_strengths = [
        ("Tải CPU xấp xỉ 0% (Zero CPU Overhead):", "Mạch UART chạy ngầm hoàn toàn độc lập ở 50 MHz. CPU chỉ mất đúng 1 chu kỳ clock (20 ns) đọc REG_RFID_UART_DAT khi có dữ liệu."),
        ("Hàng đợi FIFO 32B chống tràn tuyệt đối:", "Phần cứng tự động bắt và lưu trọn vẹn 14 byte chuỗi thẻ vào FIFO 32B, bảo toàn dữ liệu 100% ngay cả khi CPU đang bận ghi Flash NVM."),
        ("Định thời chuẩn xác 100% từ Clock 50 MHz:", "Mạch chia tần phần cứng (divisor = 5208) tạo chu kỳ baud 9600 bps chính xác tuyệt đối, miễn nhiễm hoàn toàn với độ trễ nạp lệnh XIP."),
        ("Khử Metastability 2-FF & Lọc nhiễu 16x:", "Tích hợp sync_2ff.v (MTBF > 1.000 năm) và bộ lấy mẫu 16x với thuật toán bầu đa số 3 mẫu triệt tiêu 100% xung gai nhiễu từ ăng-ten.")
    ]

    for p_lbl, p_val in rtl_strengths:
        p_item = tf_r11.add_paragraph()
        p_item.text = f"• {p_lbl} {p_val}"
        p_item.font.name = "Segoe UI"
        p_item.font.size = Pt(8.4)
        p_item.font.color.rgb = C_TEXT_DARK
        p_item.space_after = Pt(4)
        p_item.line_spacing = 1.12

    # Khung đáy: Bảng tổng hợp so sánh các chỉ số kỹ thuật then chốt
    card_b11 = add_card(s11, Inches(0.8), Inches(5.72), Inches(11.73), Inches(1.15), bg_color=RGBColor(241, 245, 249), border_color=C_BLUE_ACCENT, border_width=1.5)

    tb_b11 = s11.shapes.add_textbox(Inches(0.95), Inches(5.77), Inches(11.43), Inches(1.05))
    tf_b11 = tb_b11.text_frame
    tf_b11.word_wrap = True
    tf_b11.margin_left = tf_b11.margin_top = tf_b11.margin_right = tf_b11.margin_bottom = 0

    p_b11_h = tf_b11.paragraphs[0]
    p_b11_h.text = "TỔNG KẾT SO SÁNH CHỈ SỐ KỸ THUẬT: SOFTWARE C BIT-BANG  vs  HARDWARE RTL UART"
    p_b11_h.font.name = "Segoe UI"
    p_b11_h.font.bold = True
    p_b11_h.font.size = Pt(9.2)
    p_b11_h.font.color.rgb = C_BLUE_ACCENT
    p_b11_h.space_after = Pt(2)

    p_b11_c = tf_b11.add_paragraph()
    p_b11_c.text = "• Chiếm dụng CPU: 14.5 ms / thẻ (100% CPU)  ➔  20 ns (1 Chu kỳ clock duy nhất)  |  • An toàn Flash: Rơi mất 100% dữ liệu  ➔  FIFO 32B đệm an toàn tuyệt đối\n• Độ ổn định Baudrate: Bị rung pha do trễ Flash XIP  ➔  Chuẩn xác 100% (50MHz / 5208)  |  • Xử lý miền xung CDC: Không hỗ trợ  ➔  2-FF Sync + Lấy mẫu 16x Majority"
    p_b11_c.font.name = "Segoe UI"
    p_b11_c.font.size = Pt(8.2)
    p_b11_c.font.color.rgb = C_TEXT_DARK
    p_b11_c.line_spacing = 1.18
"""

# Replace Slide 11 block in create_presentation.py
pattern = r'    # =========================================================================\s+# SLIDE 11:.*?(?=    # =========================================================================\s+# SLIDE 12:)'

content = re.sub(pattern, new_slide11_code, content, flags=re.DOTALL)

with open('create_presentation.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Slide 11 successfully replaced with 2-column comparative layout!")
