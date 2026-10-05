# -*- coding: utf-8 -*-
"""
Script: apply_new_slide.py
Cập nhật create_presentation.py để thêm slide so sánh RTL UART vs Software C Bit-bang UART.
Tổng số slide nâng từ 24 lên 25 slide.
"""
import os
import re

cur_dir = os.path.dirname(os.path.abspath(__file__))
target_file = os.path.join(cur_dir, "create_presentation.py")

with open(target_file, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update docstring & total slides = 25
content = content.replace("TOTAL_SLIDES = 24", "TOTAL_SLIDES = 25")
content = content.replace("Tổng cộng: 24 slide mạch lạc", "Tổng cộng: 25 slide mạch lạc")

# 2. Add img_fig2a definition if not already present
if "img_fig2a =" not in content:
    img_def = """    img_device = os.path.join(project_root, "Device.jpg")
    if not os.path.exists(img_device):
        img_device = os.path.join(cur_dir, "Device.jpg")
    if not os.path.exists(img_device):
        img_device = os.path.join(doc_dir, "Device.jpg")

    img_fig2a = os.path.join(cur_dir, "fig2a_rdm6300_subsystem.png")
    if not os.path.exists(img_fig2a):
        img_fig2a = os.path.join(doc_dir, "fig2a_rdm6300_subsystem.png")
    if not os.path.exists(img_fig2a):
        img_fig2a = os.path.join(project_root, "temp", "fig2a_rdm6300_subsystem.png")"""
    
    old_img_block = """    img_device = os.path.join(project_root, "Device.jpg")
    if not os.path.exists(img_device):
        img_device = os.path.join(cur_dir, "Device.jpg")
    if not os.path.exists(img_device):
        img_device = os.path.join(doc_dir, "Device.jpg")"""
    content = content.replace(old_img_block, img_def)

# 3. Renumber slides from 11 up to 24 -> 12 up to 25
# Let's inspect how slides are named: s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22, s23, s24
# We should do this from 24 down to 11 to avoid collisions.

for old_num in range(24, 10, -1):
    new_num = old_num + 1
    # Replace slide variable names and references
    # Note: s11 -> s12, s12 -> s13, etc.
    # Be careful not to replace parts of other strings
    content = re.sub(rf'\bSLIDE {old_num}:', f'SLIDE {new_num}:', content)
    content = re.sub(rf'\bs{old_num}\b', f's{new_num}', content)
    content = re.sub(rf'\bcard{old_num}\b', f'card{new_num}', content)
    content = re.sub(rf'\btb{old_num}\b', f'tb{new_num}', content)
    content = re.sub(rf'\btf{old_num}\b', f'tf{new_num}', content)
    content = re.sub(rf'\badd_header\((s{new_num}),\s*([^,]+),\s*([^,]+),\s*{old_num}\b', rf'add_header(\1, \2, \3, {new_num}', content)

# 4. Now insert NEW SLIDE 11 right before SLIDE 12 (which was formerly Slide 11)
new_slide_11_code = """    # =========================================================================
    # SLIDE 11: PHÂN TÍCH KIẾN TRÚC - TẠI SAO PHẢI THIẾT KẾ UART TRÊN RTL THAY VÌ FIRMWARE C
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Phần 3: Phân Tích Kiến Trúc Vi Hệ Thống",
               "Lý Do Cốt Tử Thiết Kế UART Trên RTL Thay Vì Viết Bằng Firmware C", 11, total_slides=TOTAL_SLIDES)

    # Khung bên trái: Sơ đồ phần cứng 5 tầng độc lập với CPU
    card_l11 = add_card(s11, Inches(0.8), Inches(1.35), Inches(5.75), Inches(5.50), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)

    tb_lt11 = s11.shapes.add_textbox(Inches(0.95), Inches(1.50), Inches(5.45), Inches(0.30))
    tf_lt11 = tb_lt11.text_frame
    tf_lt11.margin_left = tf_lt11.margin_top = tf_lt11.margin_right = tf_lt11.margin_bottom = 0
    p_lt11 = tf_lt11.paragraphs[0]
    p_lt11.text = "ĐƯỜNG ỐNG PHẦN CỨNG 5 TẦNG THU NHẬN RFID ĐỘC LẬP"
    p_lt11.alignment = PP_ALIGN.CENTER
    p_lt11.font.name = "Segoe UI"
    p_lt11.font.size = Pt(10.5)
    p_lt11.font.bold = True
    p_lt11.font.color.rgb = C_BLUE_ACCENT

    if os.path.exists(img_fig2a):
        s11.shapes.add_picture(img_fig2a, Inches(0.95), Inches(1.85), Inches(5.45), Inches(3.60))

    card_lc11 = add_card(s11, Inches(0.95), Inches(5.55), Inches(5.45), Inches(1.15), bg_color=RGBColor(241, 245, 249), border_color=C_BLUE_ACCENT, border_width=1.0)
    tb_lc11 = s11.shapes.add_textbox(Inches(1.05), Inches(5.60), Inches(5.25), Inches(1.05))
    tf_lc11 = tb_lc11.text_frame
    tf_lc11.word_wrap = True
    tf_lc11.margin_left = tf_lc11.margin_top = tf_lc11.margin_right = tf_lc11.margin_bottom = 0

    p_lc11_1 = tf_lc11.paragraphs[0]
    p_lc11_1.text = "CƠ CHẾ PHẦN CỨNG HOÀN TOÀN ĐỘC LẬP VỚI CPU:"
    p_lc11_1.font.name = "Segoe UI"
    p_lc11_1.font.size = Pt(8.2)
    p_lc11_1.font.bold = True
    p_lc11_1.font.color.rgb = C_BLUE_ACCENT
    p_lc11_1.space_after = Pt(2)

    p_lc11_2 = tf_lc11.add_paragraph()
    p_lc11_2.text = "• 5 tầng phần cứng (2-FF Sync -> 16x Baud Gen -> RX FSM -> FIFO 32B -> MMIO) tự động bắt và đệm trọn vẹn 14 byte chuỗi thẻ RFID mà không tiêu tốn chu kỳ lệnh nào của CPU RISC-V."
    p_lc11_2.font.name = "Segoe UI"
    p_lc11_2.font.size = Pt(7.8)
    p_lc11_2.font.color.rgb = C_TEXT_DARK
    p_lc11_2.line_spacing = 1.15

    # Khung bên phải: 4 luận điểm kỹ thuật cốt tử
    card_r11 = add_card(s11, Inches(6.75), Inches(1.35), Inches(5.78), Inches(5.50), bg_color=C_WHITE, border_color=C_ROSE, border_width=1.5)

    tb_r11 = s11.shapes.add_textbox(Inches(7.05), Inches(1.50), Inches(5.25), Inches(5.20))
    tf_r11 = tb_r11.text_frame
    tf_r11.word_wrap = True
    tf_r11.margin_left = tf_r11.margin_top = tf_r11.margin_right = tf_r11.margin_bottom = 0

    p_r11_h = tf_r11.paragraphs[0]
    p_r11_h.text = "4 LÝ DO KỸ THUẬT BẮT BUỘC THIẾT KẾ UART TRÊN RTL"
    p_r11_h.font.name = "Segoe UI"
    p_r11_h.font.bold = True
    p_r11_h.font.size = Pt(11.5)
    p_r11_h.font.color.rgb = C_ROSE
    p_r11_h.space_after = Pt(4)

    uart_rtl_reasons = [
        ("1. CHỐNG MẤT MÁT DỮ LIỆU KHI CPU GHI/XÓA FLASH NVM", C_ROSE, [
            ("Hiện tượng Flash Stall:", "Xóa Sector mất 20-100 ms, ghi Page mất 1-3 ms. CPU phải nạp mã vào SRAM và bị chiếm dụng hoàn toàn."),
            ("Hậu quả nếu bit-bang C:", "CPU không thể quét GPIO, gây mất 100% dữ liệu quẹt thẻ trong lúc hệ thống cập nhật Whitelist/Log."),
            ("Giải pháp RTL UART + FIFO:", "Hàng đợi FIFO 32B phần cứng tự động đệm toàn bộ chuỗi thẻ độc lập với hoạt động của CPU.")
        ]),
        ("2. GIẢI PHÓNG 100% TẢI CPU & ĐÁP ỨNG THỜI GIAN THỰC", C_AMBER, [
            ("Lãng phí CPU do Bit-bang C:", "Tại 9600 baud, 1 khung thẻ 14 byte mất ~14.5 ms. Software C polling/delay sẽ khóa chết CPU 100%."),
            ("Hiệu năng vượt trội của RTL:", "UART phần cứng chạy song song ở 50 MHz; CPU chỉ mất đúng 1 chu kỳ clock đọc REG_RFID_UART_DAT.")
        ]),
        ("3. CHỐNG SIÊU ỔN ĐỊNH (CDC) & LỌC NHIỄU BẰNG PHẦN CỨNG", C_BLUE_ACCENT, [
            ("Miền xung không đồng bộ (CDC):", "Tín hiệu RX từ RDM6300 đi qua sync_2ff.v (2 Flip-Flop) loại trừ triệt để Metastability (MTBF > 1000 năm)."),
            ("Lấy mẫu 16x & Bầu đa số 3 mẫu:", "Bộ lọc phần cứng loại bỏ sạch xung gai (glitch) mà firmware C không thể thực hiện được.")
        ]),
        ("4. TRIỆT TIÊU RUNG PHA (JITTER) DO TRỄ KÉO LỆNH FLASH XIP", C_GREEN, [
            ("Hiện tượng Flash XIP Jitter:", "Mã C thực thi qua SPI Flash XIP có độ trễ thay đổi (wait states), khiến vòng lặp delay trong C bị sai lệch baudrate."),
            ("Độ chính xác RTL:", "Mạch chia tần phần cứng dùng xung 50 MHz (divisor = 5208) tạo baudrate 9600 bps chính xác 100%.")
        ])
    ]

    for sec_idx, (sec_title, sec_col, sec_bullets) in enumerate(uart_rtl_reasons):
        p_sec = tf_r11.add_paragraph()
        p_sec.text = sec_title
        p_sec.font.name = "Segoe UI"
        p_sec.font.size = Pt(8.6)
        p_sec.font.bold = True
        p_sec.font.color.rgb = sec_col
        p_sec.space_before = Pt(3)
        p_sec.space_after = Pt(1)

        for b_lbl, b_val in sec_bullets:
            p_b = tf_r11.add_paragraph()
            p_b.text = f"• {b_lbl} {b_val}"
            p_b.font.name = "Segoe UI"
            p_b.font.size = Pt(7.6)
            p_b.font.color.rgb = C_TEXT_DARK
            p_b.space_after = Pt(1.2)
            p_b.line_spacing = 1.10

"""

# Insert right before `# SLIDE 12: GIAI ĐOẠN 5`
target_marker = "    # =========================================================================\n    # SLIDE 12: GIAI ĐOẠN 5"
if target_marker in content:
    content = content.replace(target_marker, new_slide_11_code + target_marker)
else:
    print("Warning: target_marker not found, searching alternative")
    # Let's search with regex
    content = re.sub(r'(    # =+?\n    # SLIDE 12: GIAI ĐOẠN 5)', new_slide_11_code + r'\1', content)

# 5. Update header docstring in create_presentation.py
doc_old = """- Slide 10: Giai Đoạn 4: Mở Rộng Ngoại Vi MMIO Với Hàng Đợi FIFO Chống Tràn (uart_mmio.v, sync_fifo.v, gpio)
- Slide 11: Giai Đoạn 5: Tầng Firmware C Tương Tác Qua Con Trỏ Volatile MMIO (soc_regs.h, access_control.c, uart.c)
- Slide 12: Phần 4 - Testbench 1: Kiểm Thử Phần Cứng RTL Thuần Cho UART MMIO & FIFO (tb_uart_rtl.v)
- Slide 13: Phần 4 - Testbench 2: Kiểm Thử Tích Hợp Toàn Diện Top SoC Boot Flash & Ping (tb_uart_ping.v)
- Slide 14: Biến Địa Chỉ 1: REG_RFID_UART_DAT & DIV (0x1000_0004 & 0x1000_0000) - Đọc RFID RX FIFO
- Slide 15: Biến Địa Chỉ 2: REG_PC_UART_DAT & DIV (0x3000_0004 & 0x3000_0000) - Giao Tiếp Host PC UART
- Slide 16: Biến Địa Chỉ 3: REG_GPIO_LEDS (0x4000_0000) - Điều Khiển LED Trạng Thái & Relay Mở Cửa
- Slide 17: Biến Địa Chỉ 4: USER_FLASH_ADDR (0x0030_0000 - Sector 48) - Cơ Sở Dữ Liệu Thẻ Whitelist
- Slide 18: Biến Địa Chỉ 5: LOG_FLASH_ADDR (0x0031_0000 - Sector 49) - Nhật Ký Quẹt Thẻ Access Logs
- Slide 19: Biến Địa Chỉ 6: 0x0200_0000 & flashio_worker - Nạp Routine Vào SRAM Lập Trình Flash NVM
- Slide 20: Phần 5 - Demo Thực Nghiệm Trên FPGA: Thiết Lập Kết Nối Phần Cứng & Nguồn 5V/Trở 1k
- Slide 21: Phần 5 - Demo Thực Nghiệm Trên FPGA: Giao Diện Host Console CLI & Đánh Giá Chức Năng
- Slide 22: Phần 6 - Thiết Kế Vật Lý ASIC: Quy Trình RTL-to-GDSII Trên OpenLane 2 (SkyWater 130nm)
- Slide 23: Phần 6 - Thiết Kế Vật Lý ASIC: Bản Vẽ Layout OpenROAD & Báo Cáo Ký Duyệt Sign-off
- Slide 24: Tổng Kết Đồ Án Và Các Đóng Góp Nổi Bật"""

doc_new = """- Slide 10: Giai Đoạn 4: Mở Rộng Ngoại Vi MMIO Với Hàng Đợi FIFO Chống Tràn (uart_mmio.v, sync_fifo.v, gpio)
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

content = content.replace(doc_old, doc_new)

with open(target_file, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully modified create_presentation.py with 25 slides!")
