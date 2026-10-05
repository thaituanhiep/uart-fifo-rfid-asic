# -*- coding: utf-8 -*-
"""
Script: update_slide_structure_26.py
Sắp xếp lại luồng slide chuẩn mực gồm 26 slide:
- Slide 10: Giai đoạn 4 (Mở rộng MMIO & FIFO 32B)
- Slide 11: Giai đoạn 5 (Tầng Firmware C Volatile MMIO)
- Slide 12: Phân tích kiến trúc: So sánh RTL Hardware UART vs Software C Bit-bang
- Slide 13: Sơ đồ khối kiến trúc vi mạch UART RTL (Draw.io Đen Trắng & Đặc tả 5 tầng phần cứng)
- Slide 14..26: Testbench, Biến địa chỉ MMIO, Demo thực nghiệm, ASIC Sign-off, Tổng kết
"""
import os
import re

cur_dir = os.path.dirname(os.path.abspath(__file__))
target_file = os.path.join(cur_dir, "create_presentation.py")

with open(target_file, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update TOTAL_SLIDES
text = text.replace("TOTAL_SLIDES = 25", "TOTAL_SLIDES = 26")
text = text.replace("TOTAL_SLIDES = 24", "TOTAL_SLIDES = 26")
text = text.replace("Tổng cộng: 25 slide mạch lạc", "Tổng cộng: 26 slide mạch lạc")
text = text.replace("Tổng cộng: 24 slide mạch lạc", "Tổng cộng: 26 slide mạch lạc")

# 2. Add img_uart_bw definition
img_def = """    img_uart_bw = os.path.join(cur_dir, "uart_architecture_bw_diagram.png")
    if not os.path.exists(img_uart_bw):
        img_uart_bw = os.path.join(doc_dir, "uart_architecture_bw_diagram.png")
    if not os.path.exists(img_uart_bw):
        img_uart_bw = os.path.join(project_root, "temp", "uart_architecture_bw_diagram.png")"""

if "img_uart_bw =" not in text:
    old_img_block = """    img_device = os.path.join(project_root, "Device.jpg")
    if not os.path.exists(img_device):
        img_device = os.path.join(cur_dir, "Device.jpg")
    if not os.path.exists(img_device):
        img_device = os.path.join(doc_dir, "Device.jpg")"""
    text = text.replace(old_img_block, old_img_block + "\n\n" + img_def)

# Define clean Slide 11, 12, 13 code
slides_11_12_13_code = """    # =========================================================================
    # SLIDE 11: GIAI ĐOẠN 5 - TẦNG FIRMWARE C TƯƠNG TÁC QUA VOLATILE MMIO
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Phần 3: Quy Trình Thiết Kế SoC (Giai Đoạn 5/5)",
               "Giai Đoạn 5: Tầng Firmware C Tương Tác Qua Con Trỏ Volatile MMIO (soc_regs.h, access_control.c, uart.c)", 11, total_slides=TOTAL_SLIDES)

    if os.path.exists(img_stages[4]):
        add_card(s11, Inches(0.8), Inches(1.30), Inches(5.75), Inches(5.50), bg_color=C_WHITE, border_color=C_GREEN, border_width=1.5)
        s11.shapes.add_picture(img_stages[4], Inches(0.95), Inches(1.45), Inches(5.45), Inches(5.20))

    rx11 = Inches(6.75)
    rw11 = Inches(5.78)
    add_card(s11, rx11, Inches(1.30), rw11, Inches(5.50), bg_color=C_WHITE, border_color=C_GREEN, border_width=1.5)
    tb_r11 = s11.shapes.add_textbox(rx11 + Inches(0.20), Inches(1.45), rw11 - Inches(0.40), Inches(5.20))
    tf_r11 = tb_r11.text_frame
    tf_r11.word_wrap = True

    p_r11_h = tf_r11.paragraphs[0]
    p_r11_h.text = "TRỪU TƯỢNG HÓA PHẦN CỨNG BẰNG NGÔN NGỮ C"
    p_r11_h.font.name = "Segoe UI"
    p_r11_h.font.bold = True
    p_r11_h.font.size = Pt(12)
    p_r11_h.font.color.rgb = C_GREEN
    p_r11_h.space_after = Pt(8)

    st5_points = [
        ("Tầng Macro MMIO (soc_regs.h):", "Định nghĩa các con trỏ phần cứng:\\n  #define REG_RFID_UART_DAT (*(volatile uint32_t*)0x10000004)\\n  #define REG_PC_UART_DAT   (*(volatile uint32_t*)0x30000004)\\n  #define REG_GPIO_LEDS     (*(volatile uint32_t*)0x40000000)"),
        ("Bản chất từ khóa volatile:", "Ép trình biên dịch GCC luôn sinh ra lệnh đọc/ghi bus thật (lw, sw), loại bỏ triệt để lỗi tối ưu hóa lưu biến vào thanh ghi."),
        ("Tầng Ứng Dụng C (access_control.c):", "Xử lý nghiệp vụ hoàn toàn trong suốt:\\n  uint32_t d = REG_RFID_UART_DAT;\\n  if (d != 0xFFFFFFFF) rdm6300_push_byte((uint8_t)d);\\n  if (card_valid) REG_GPIO_LEDS |= 0x04; // Mở cửa"),
        ("Ý nghĩa kỹ thuật:", "Lập trình viên C có thể điều khiển toàn bộ vi mạch số phức tạp chỉ bằng các biến con trỏ quen thuộc, mã nguồn trong sáng, độc lập với phần cứng.")
    ]

    for p_lbl, p_val in st5_points:
        p = tf_r11.add_paragraph()
        p.text = f"• {p_lbl} {p_val}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(5)
        p.line_spacing = 1.15

    p_sum5 = tf_r11.add_paragraph()
    p_sum5.text = "=> KẾT LUẬN: 5 giai đoạn thiết kế đã tạo nên một SoC hoàn chỉnh, tối ưu và sẵn sàng sản xuất."
    p_sum5.font.name = "Segoe UI"
    p_sum5.font.size = Pt(9.2)
    p_sum5.font.bold = True
    p_sum5.font.color.rgb = C_GREEN
    p_sum5.space_before = Pt(4)

    # =========================================================================
    # SLIDE 12: SO SÁNH ĐỐI CHIẾU - RTL HARDWARE UART VS SOFTWARE C BIT-BANG
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Phần 3: Phân Tích Kiến Trúc Vi Hệ Thống",
               "So Sánh Kiến Trúc: Thiết Kế UART Trên RTL vs Viết Bằng Firmware C", 12, total_slides=TOTAL_SLIDES)

    # Khung bên trái: Phương án 1 - Software Bit-bang UART trong C (Cảnh báo / Yếu điểm)
    card_l12 = add_card(s12, Inches(0.8), Inches(1.35), Inches(5.75), Inches(4.25), bg_color=C_WHITE, border_color=C_ROSE, border_width=1.8)

    tb_l12 = s12.shapes.add_textbox(Inches(1.00), Inches(1.48), Inches(5.35), Inches(4.00))
    tf_l12 = tb_l12.text_frame
    tf_l12.word_wrap = True
    tf_l12.margin_left = tf_l12.margin_top = tf_l12.margin_right = tf_l12.margin_bottom = 0

    p_l12_h = tf_l12.paragraphs[0]
    p_l12_h.text = "PHƯƠNG ÁN 1: SOFTWARE BIT-BANG TRONG C (NHƯỢC ĐIỂM)"
    p_l12_h.font.name = "Segoe UI"
    p_l12_h.font.bold = True
    p_l12_h.font.size = Pt(11.5)
    p_l12_h.font.color.rgb = C_ROSE
    p_l12_h.space_after = Pt(6)

    c_weaknesses = [
        ("1. TREO CPU 100% KHI CHỜ BIT (CPU BLOCKING)", "Tại 9600 baud, 1 bit = 104.16 µs; khung thẻ 14 byte (140 bit) mất ~14.5 ms. Vòng lặp delay/polling chiếm dụng 100% CPU, không thể đa nhiệm xử lý tác vụ khác."),
        ("2. MẤT 100% MÃ THẺ KHI GHI FLASH (FLASH STALL)", "Xóa Sector (4KB) mất 20-100 ms, ghi Page mất 1-3 ms. CPU nạp mã vào SRAM bị chiếm dụng; không thể quét GPIO, gây rớt toàn bộ dữ liệu thẻ quẹt!"),
        ("3. RUNG PHA (JITTER) DO TRỄ NẠP MÃ FLASH XIP", "Thực thi lệnh C qua SPI Flash XIP có độ trễ thay đổi (wait-states biến thiên), làm sai lệch chu kỳ hàm delay trong C, gây lỗi định dạng Framing Error."),
        ("4. BẤT LỰC TRƯỚC LỖI SIÊU ỔN ĐỊNH (METASTABILITY)", "Đọc chân GPIO bằng phần mềm không thể giải quyết xung đột miền xung (CDC) và không thể lọc xung gai (glitch) ở mức tín hiệu bán dẫn.")
    ]

    for p_lbl, p_val in c_weaknesses:
        p_t = tf_l12.add_paragraph()
        p_t.text = f"• {p_lbl}:"
        p_t.font.name = "Segoe UI"
        p_t.font.size = Pt(8.8)
        p_t.font.bold = True
        p_t.font.color.rgb = C_ROSE
        p_t.space_before = Pt(3)
        p_t.space_after = Pt(1)

        p_d = tf_l12.add_paragraph()
        p_d.text = f"  {p_val}"
        p_d.font.name = "Segoe UI"
        p_d.font.size = Pt(8.2)
        p_d.font.color.rgb = C_TEXT_DARK
        p_d.space_after = Pt(3)
        p_d.line_spacing = 1.12

    # Khung bên phải: Phương án 2 - Thiết kế UART MMIO & FIFO trên RTL (Ưu điểm vượt trội)
    card_r12 = add_card(s12, Inches(6.78), Inches(1.35), Inches(5.75), Inches(4.25), bg_color=C_WHITE, border_color=C_GREEN, border_width=1.8)

    tb_r12 = s12.shapes.add_textbox(Inches(6.98), Inches(1.48), Inches(5.35), Inches(4.00))
    tf_r12 = tb_r12.text_frame
    tf_r12.word_wrap = True
    tf_r12.margin_left = tf_r12.margin_top = tf_r12.margin_right = tf_r12.margin_bottom = 0

    p_r12_h = tf_r12.paragraphs[0]
    p_r12_h.text = "PHƯƠNG ÁN 2: THIẾT KẾ UART & FIFO TRÊN RTL (TỐI ƯU)"
    p_r12_h.font.name = "Segoe UI"
    p_r12_h.font.bold = True
    p_r12_h.font.size = Pt(11.5)
    p_r12_h.font.color.rgb = C_GREEN
    p_r12_h.space_after = Pt(6)

    rtl_strengths = [
        ("1. GIẢI PHÓNG 100% CPU (ZERO CPU OVERHEAD)", "Mạch UART chạy ngầm hoàn toàn độc lập ở 50 MHz. CPU chỉ mất đúng 1 chu kỳ clock (20 ns) đọc REG_RFID_UART_DAT khi có dữ liệu mới."),
        ("2. HÀNG ĐỢI FIFO 32B CHỐNG TRÀN TUYỆT ĐỐI", "Phần cứng tự động thu nhận và đệm toàn bộ 14 byte chuỗi thẻ vào sync_fifo.v, bảo toàn dữ liệu 100% ngay cả khi CPU đang bận ghi/xóa Flash NVM."),
        ("3. ĐỊNH THỜI CHUẨN XÁC 100% TỪ CLOCK 50 MHZ", "Bộ chia tần cứng (divisor = 5208) tạo chu kỳ baud 9600 bps chính xác tuyệt đối, miễn nhiễm hoàn toàn với độ trễ nạp lệnh Flash XIP."),
        ("4. KHỬ METASTABILITY 2-FF & LỌC NHIỄU 16X", "Tích hợp sync_2ff.v (MTBF > 1.000 năm) và bộ lấy mẫu 16x với thuật toán bầu đa số 3 mẫu triệt tiêu 100% xung gai nhiễu từ ăng-ten.")
    ]

    for p_lbl, p_val in rtl_strengths:
        p_t = tf_r12.add_paragraph()
        p_t.text = f"• {p_lbl}:"
        p_t.font.name = "Segoe UI"
        p_t.font.size = Pt(8.8)
        p_t.font.bold = True
        p_t.font.color.rgb = C_GREEN
        p_t.space_before = Pt(3)
        p_t.space_after = Pt(1)

        p_d = tf_r12.add_paragraph()
        p_d.text = f"  {p_val}"
        p_d.font.name = "Segoe UI"
        p_d.font.size = Pt(8.2)
        p_d.font.color.rgb = C_TEXT_DARK
        p_d.space_after = Pt(3)
        p_d.line_spacing = 1.12

    # Khung đáy: Bảng tổng hợp so sánh các chỉ số kỹ thuật then chốt
    card_b12 = add_card(s12, Inches(0.8), Inches(5.72), Inches(11.73), Inches(1.18), bg_color=RGBColor(241, 245, 249), border_color=C_BLUE_ACCENT, border_width=1.5)

    tb_b12 = s12.shapes.add_textbox(Inches(0.95), Inches(5.77), Inches(11.43), Inches(1.08))
    tf_b12 = tb_b12.text_frame
    tf_b12.word_wrap = True
    tf_b12.margin_left = tf_b12.margin_top = tf_b12.margin_right = tf_b12.margin_bottom = 0

    p_b12_h = tf_b12.paragraphs[0]
    p_b12_h.text = "TỔNG KẾT SO SÁNH CHỈ SỐ KỸ THUẬT: SOFTWARE C BIT-BANG  vs  HARDWARE RTL UART"
    p_b12_h.font.name = "Segoe UI"
    p_b12_h.font.bold = True
    p_b12_h.font.size = Pt(9.5)
    p_b12_h.font.color.rgb = C_BLUE_ACCENT
    p_b12_h.space_after = Pt(2)

    p_b12_c1 = tf_b12.add_paragraph()
    p_b12_c1.text = "• Chiếm dụng CPU: 14.5 ms / thẻ (100% CPU)  ➔  20 ns (1 Chu kỳ clock duy nhất)  |  • An toàn Flash: Rơi mất 100% dữ liệu  ➔  FIFO 32B đệm an toàn tuyệt đối"
    p_b12_c1.font.name = "Segoe UI"
    p_b12_c1.font.size = Pt(8.5)
    p_b12_c1.font.color.rgb = C_TEXT_DARK
    p_b12_c1.line_spacing = 1.15

    p_b12_c2 = tf_b12.add_paragraph()
    p_b12_c2.text = "• Độ ổn định Baudrate: Bị rung pha do trễ Flash XIP  ➔  Chuẩn xác 100% (50MHz / 5208)  |  • Xử lý miền xung CDC: Không hỗ trợ  ➔  2-FF Sync + Lấy mẫu 16x Majority"
    p_b12_c2.font.name = "Segoe UI"
    p_b12_c2.font.size = Pt(8.5)
    p_b12_c2.font.color.rgb = C_TEXT_DARK
    p_b12_c2.line_spacing = 1.15

    # =========================================================================
    # SLIDE 13: SƠ ĐỒ KHỐI KIẾN TRÚC VI MẠCH UART RTL & ĐẶC TẢ THIẾT KẾ
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Phần 3: Kiến Trúc Khối Ngoại Vi UART",
               "Sơ Đồ Khối Kiến Trúc Vi Mạch UART RTL (Draw.io Đen Trắng & Đặc Tả Thiết Kế)", 13, total_slides=TOTAL_SLIDES)

    if os.path.exists(img_uart_bw):
        add_card(s13, Inches(0.8), Inches(1.30), Inches(5.75), Inches(5.50), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
        s13.shapes.add_picture(img_uart_bw, Inches(0.95), Inches(1.45), Inches(5.45), Inches(5.20))

    rx13 = Inches(6.75)
    rw13 = Inches(5.78)
    add_card(s13, rx13, Inches(1.30), rw13, Inches(5.50), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
    tb_r13 = s13.shapes.add_textbox(rx13 + Inches(0.20), Inches(1.45), rw13 - Inches(0.40), Inches(5.20))
    tf_r13 = tb_r13.text_frame
    tf_r13.word_wrap = True

    p_r13_h = tf_r13.paragraphs[0]
    p_r13_h.text = "ĐẶC TẢ THIẾT KẾ 5 TẦNG VI MẠCH NGOẠI VI UART RTL"
    p_r13_h.font.name = "Segoe UI"
    p_r13_h.font.bold = True
    p_r13_h.font.size = Pt(11.5)
    p_r13_h.font.color.rgb = C_BLUE_ACCENT
    p_r13_h.space_after = Pt(4)

    uart_stages_desc = [
        ("TẦNG 1: ĐỒNG BỘ HÓA MIỀN XUNG 2-FF CDC (sync_2ff.v)", C_ROSE, [
            ("Ngõ vào không đồng bộ rx_i:", "Tín hiệu nối tiếp từ đầu đọc RDM6300 125kHz hoặc chip USB FT2232 đi qua 2 tầng Flip-Flop."),
            ("Chống hiện tượng siêu ổn định:", "Bảo đảm thời gian trung bình giữa 2 lỗi MTBF > 1.000 năm trên tiến trình SkyWater 130nm.")
        ]),
        ("TẦNG 2 & 3: BỘ TẠO BAUD, LẤY MẪU 16X & RX FSM (simpleuart.v)", C_AMBER, [
            ("Chia tần số chuẩn xác:", "Thanh ghi cfg_divider = 5208 (50 MHz / 9600 bps) tạo chu kỳ định thời phần cứng chính xác 100%."),
            ("Bộ lấy mẫu 16x & Bầu đa số 3 mẫu:", "Lấy mẫu tại tick 7, 8, 9 ở giữa bit, triệt tiêu xung gai nhiễu glitch."),
            ("Máy trạng thái RX FSM:", "Tự động phát hiện Start bit (0), dịch 8-bit dữ liệu LSB-first và kiểm tra Stop bit (1).")
        ]),
        ("TẦNG 4: HÀNG ĐỢI FIFO 32 BYTES ĐỘC LẬP (sync_fifo.v)", C_BLUE_ACCENT, [
            ("Cơ chế đệm độc lập:", "Quản lý con trỏ ghi wr_ptr và đọc rd_ptr độc lập trên mảng nhớ 32x8-bit."),
            ("Bảo vệ chống tràn khi Flash bận:", "Đệm trọn vẹn 14 byte chuỗi thẻ RFID ngay cả khi CPU bận chạy flashio_worker ghi Flash.")
        ]),
        ("TẦNG 5: GIẢI MÃ BUS MMIO & NON-BLOCKING (uart_mmio.v)", C_GREEN, [
            ("Ánh xạ không gian địa chỉ:", "0x1000_0000 (Divider Prescaler) và 0x1000_0004 (RX FIFO Data)."),
            ("Giao tiếp Non-blocking 1 chu kỳ:", "Nếu FIFO rỗng, trả về ngay 0xFFFFFFFF trong 20 ns, không bao giờ làm treo bus CPU.")
        ])
    ]

    for sec_idx, (sec_title, sec_col, sec_bullets) in enumerate(uart_stages_desc):
        p_sec = tf_r13.add_paragraph()
        p_sec.text = sec_title
        p_sec.font.name = "Segoe UI"
        p_sec.font.size = Pt(8.6)
        p_sec.font.bold = True
        p_sec.font.color.rgb = sec_col
        p_sec.space_before = Pt(3)
        p_sec.space_after = Pt(1)

        for b_lbl, b_val in sec_bullets:
            p_b = tf_r13.add_paragraph()
            p_b.text = f"• {b_lbl} {b_val}"
            p_b.font.name = "Segoe UI"
            p_b.font.size = Pt(7.6)
            p_b.font.color.rgb = C_TEXT_DARK
            p_b.space_after = Pt(1.2)
            p_b.line_spacing = 1.10
"""

# Re-index all slides from old Slide 12 (now Slide 14) up to Slide 25 (now Slide 26)
# Let's inspect the file content around SLIDE 11/12
# Pattern to replace from `# SLIDE 11:` up to `# SLIDE 13:` (or former Slide 12)
slide_block_pattern = r'    # =========================================================================\s+# SLIDE 11:.*?(?=    # =========================================================================\s+# SLIDE 13:)'

# If we have old slides 13..25, let's increment them to 14..26 from the bottom up!
for old_num in range(25, 12, -1):
    new_num = old_num + 1
    text = re.sub(rf'\bSLIDE {old_num}:', f'SLIDE {new_num}:', text)
    text = re.sub(rf'\bs{old_num}\b', f's{new_num}', text)
    text = re.sub(rf'\bcard{old_num}\b', f'card{new_num}', text)
    text = re.sub(rf'\btb{old_num}\b', f'tb{new_num}', text)
    text = re.sub(rf'\btf{old_num}\b', f'tf{new_num}', text)
    text = re.sub(rf'\badd_header\((s{new_num}),\s*([^,]+),\s*([^,]+),\s*{old_num}\b', rf'add_header(\1, \2, \3, {new_num}', text)

# Now replace the slide 11 & 12 area with our new slides 11, 12, 13
replace_area_pattern = r'    # =========================================================================\s+# SLIDE 11:.*?(?=    # =========================================================================\s+# SLIDE 14:)'

text = re.sub(replace_area_pattern, slides_11_12_13_code, text, flags=re.DOTALL)

# Update docstring
doc_header_old = """- Slide 10: Giai Đoạn 4: Mở Rộng Ngoại Vi MMIO Với Hàng Đợi FIFO Chống Tràn (uart_mmio.v, sync_fifo.v, gpio)
- Slide 11: Phân Tích Kiến Trúc: Lý Do Cốt Tử Thiết Kế UART Trên RTL Thay Vì Viết Bằng Firmware C
- Slide 12: Giai Đoạn 5: Tầng Firmware C Tương Tác Qua Con Trỏ Volatile MMIO (soc_regs.h, access_control.c, uart.c)
- Slide 13: Phần 4 - Testbench 1: Kiểm Thử Phần Cứng RTL Thuần Cho UART MMIO & FIFO (tb_uart_rtl.v)
- Slide 14: Phần 4 - Testbench 2: Kiểm Thử Tích Hợp Toàn Diện Top SoC Boot Flash & Ping (tb_uart_ping.v)
- Slide 15: Biến Địa Chỉ 1: REG_RFID_UART_DAT & DIV (0x1000_0004 & 0x1000_0000) - Đọc RFID RX FIFO
- Slide 16: Biến Địa Chỉ 2: REG_PC_UART_DAT & DIV (0x3000_0004 & 0x3000_0000) - Giao Tiếp Host PC UART
- Slide 17: Biến Địa Chỉ 3: REG_GPIO_LEDS (0x4000_0000) - Điều Khiển LED Trạng Thái & Relay Mở Cửa
- Slide 18: Biến Địa Chỉ 4: USER_FLASH_ADDR (0x0030_0000 - Sector 48) - Cơ Sở Dữ Liệu Thẻ Whitelist
- Slide 19: Biến Địa Chỉ 5: LOG_FLASH_ADDR (0x0031_0000 - Sector 49) - Nhật Ký Quẹt Thẻ Access Logs
- Slide 20: Biến Địa Chỉ 6: 0x0200_0000 & flashio_worker - Nạp Routine Vào SRAM Lập Trình Flash NVM
- Slide 21: Phần 5 - Demo Thực Nghiệm Trên FPGA: Thiết Lập Kết Nối Phần Cứng & Nguồn 5V/Trở 1k
- Slide 22: Phần 5 - Demo Thực Nghiệm Trên FPGA: Giao Diện Host Console CLI & Đánh Giá Chức Năng
- Slide 23: Phần 6 - Thiết Kế Vật Lý ASIC: Quy Trình RTL-to-GDSII Trên OpenLane 2 (SkyWater 130nm)
- Slide 24: Phần 6 - Thiết Kế Vật Lý ASIC: Bản Vẽ Layout OpenROAD & Báo Cáo Ký Duyệt Sign-off
- Slide 25: Tổng Kết Đồ Án Và Các Đóng Góp Nổi Bật"""

doc_header_new = """- Slide 10: Giai Đoạn 4: Mở Rộng Ngoại Vi MMIO Với Hàng Đợi FIFO Chống Tràn (uart_mmio.v, sync_fifo.v, gpio)
- Slide 11: Giai Đoạn 5: Tầng Firmware C Tương Tác Qua Con Trỏ Volatile MMIO (soc_regs.h, access_control.c, uart.c)
- Slide 12: Phân Tích Kiến Trúc: So Sánh Thiết Kế UART Trên RTL vs Viết Bằng Firmware C
- Slide 13: Sơ Đồ Khối Kiến Trúc Vi Mạch UART RTL (Draw.io Đen Trắng & Đặc Tả Thiết Kế)
- Slide 14: Phần 4 - Testbench 1: Kiểm Thử Phần Cứng RTL Thuần Cho UART MMIO & FIFO (tb_uart_rtl.v)
- Slide 15: Phần 4 - Testbench 2: Kiểm Thử Tích Hợp Toàn Diện Top SoC Boot Flash & Ping (tb_uart_ping.v)
- Slide 16: Biến Địa Chỉ 1: REG_RFID_UART_DAT & DIV (0x1000_0004 & 0x1000_0000) - Đọc RFID RX FIFO
- Slide 17: Biến Địa Chỉ 2: REG_PC_UART_DAT & DIV (0x3000_0004 & 0x3000_0000) - Giao Tiếp Host PC UART
- Slide 18: Biến Địa Chỉ 3: REG_GPIO_LEDS (0x4000_0000) - Điều Khiển LED Trạng Thái & Relay Mở Cửa
- Slide 19: Biến Địa Chỉ 4: USER_FLASH_ADDR (0x0030_0000 - Sector 48) - Cơ Sở Dữ Liệu Thẻ Whitelist
- Slide 20: Biến Địa Chỉ 5: LOG_FLASH_ADDR (0x0031_0000 - Sector 49) - Nhật Ký Quẹt Thẻ Access Logs
- Slide 21: Biến Địa Chỉ 6: 0x0200_0000 & flashio_worker - Nạp Routine Vào SRAM Lập Trình Flash NVM
- Slide 22: Phần 5 - Demo Thực Nghiệm Trên FPGA: Thiết Lập Kết Nối Phần Cứng & Nguồn 5V/Trở 1k
- Slide 23: Phần 5 - Demo Thực Nghiệm Trên FPGA: Giao Diện Host Console CLI & Đánh Giá Chức Năng
- Slide 24: Phần 6 - Thiết Kế Vật Lý ASIC: Quy Trình RTL-to-GDSII Trên OpenLane 2 (SkyWater 130nm)
- Slide 25: Phần 6 - Thiết Kế Vật Lý ASIC: Bản Vẽ Layout OpenROAD & Báo Cáo Ký Duyệt Sign-off
- Slide 26: Tổng Kết Đồ Án Và Các Đóng Góp Nổi Bật"""

text = text.replace(doc_header_old, doc_header_new)

with open(target_file, "w", encoding="utf-8") as f:
    f.write(text)

print("Slide structure updated successfully to 26 slides!")
