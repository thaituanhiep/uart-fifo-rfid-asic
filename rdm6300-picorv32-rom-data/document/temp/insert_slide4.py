import os
import sys

def main():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    target_file = os.path.join(cur_dir, "create_presentation.py")

    with open(target_file, "r", encoding="utf-8") as f:
        code = f.read()

    # 1. Update TOTAL_SLIDES = 13
    code = code.replace("TOTAL_SLIDES = 12", "TOTAL_SLIDES = 13")

    # 2. Target anchor
    target_after_s6 = "        s6.shapes.add_picture(img_fig1, img_x, img_y, img_w, img_h)"

    new_slide_4_code = '''        s6.shapes.add_picture(img_fig1, img_x, img_y, img_w, img_h)

    # =========================================================================
    # SLIDE 4: PHẦN 3 - BẢNG TRA CỨU ĐỊA CHỈ BỘ NHỚ (MEMORY MAP) & C / RTL
    # =========================================================================
    s_map = prs.slides.add_slide(blank_layout)
    add_header(s_map, "Phần 3: Kiến Trúc Vi Hệ Thống SoC",
               "Bảng Tra Cứu Địa Chỉ (Memory Map) & Khai Báo Biến Trong C / RTL", 4, total_slides=TOTAL_SLIDES)

    # Khung bao bọc bảng (Card)
    add_card(s_map, Inches(0.8), Inches(1.26), Inches(11.733), Inches(5.68), bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)

    # Tạo bảng 3 cột (7 hàng = 1 Header + 6 Dải địa chỉ)
    table_map_shape = s_map.shapes.add_table(7, 3, Inches(0.85), Inches(1.32), Inches(11.633), Inches(5.54))
    tbl_map = table_map_shape.table
    tbl_map.columns[0].width = Inches(2.35)
    tbl_map.columns[1].width = Inches(3.60)
    tbl_map.columns[2].width = Inches(5.683)

    map_headers = ["DẢI ĐỊA CHỈ (ADDRESS / OFFSET)", "NƠI KHAI BÁO TRONG C VÀ RTL", "Ý NGHĨA SỬ DỤNG VỚI FIRMWARE C & NGHIỆP VỤ"]
    for col_i, h_text in enumerate(map_headers):
        c_cell = tbl_map.cell(0, col_i)
        c_cell.fill.solid()
        c_cell.fill.fore_color.rgb = C_NAVY_MID
        c_cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        c_cell.margin_left = c_cell.margin_right = Inches(0.08)
        c_cell.margin_top = c_cell.margin_bottom = Inches(0.04)
        hp = c_cell.text_frame.paragraphs[0]
        hp.text = h_text
        hp.font.name = "Segoe UI"
        hp.font.size = Pt(9.5)
        hp.font.bold = True
        hp.font.color.rgb = RGBColor(255, 255, 255)
        hp.alignment = PP_ALIGN.CENTER

    map_rows_data = [
        (
            [("0x0000_0000", True, C_BLUE_ACCENT), ("\\n- 0x0000_03FF", False, C_TEXT_DARK), ("\\n(1KB Data SRAM)", True, C_TEXT_MUTED)],
            [("• C/Linker: ", True, C_BLUE_ACCENT), ("sections.lds\\n  (RAM: 0x0, _stack_top: 0x400)\\n", False, C_TEXT_DARK),
             ("• RTL: ", True, C_PURPLE), ("soc_interconnect.v\\n  (sel_sram < 0x400), data_sram.v", False, C_TEXT_DARK)],
            [("• Vùng nhớ RAM tĩnh 1 chu kỳ clock ", True, C_TEXT_DARK), ("(phản hồi sram_ready = 1 tức thì).\\n", False, C_TEXT_MUTED),
             ("• Bắt buộc lưu con trỏ Stack (sp), ", True, C_BLUE_ACCENT), ("biến cục bộ, mảng dữ liệu làm việc cho C, đảm bảo tính thời gian thực.", False, C_TEXT_MUTED)]
        ),
        (
            [("0x0010_0000", True, C_BLUE_ACCENT), ("\\n- 0x00FF_FFFF", False, C_TEXT_DARK), ("\\n(SPI Flash XIP 4MB)", True, C_GREEN)],
            [("• C/Linker: ", True, C_BLUE_ACCENT), ("sections.lds (FLASH: 0x250000)\\n  soc_regs.h (USER: 0x300000, LOG: 0x310000)\\n", False, C_TEXT_DARK),
             ("• RTL: ", True, C_PURPLE), ("soc_interconnect.v\\n  (sel_spimem), spimemio.v", False, C_TEXT_DARK)],
            [("• 0x0025_0000: ", True, C_BLUE_ACCENT), ("Nạp mã máy Firmware XIP (thực thi trực tiếp từ Flash).\\n", False, C_TEXT_MUTED),
             ("• 0x0030_0000 (Sec 48): ", True, C_GREEN), ("Database 4.096 thẻ hợp lệ (Magic: 'RFID').\\n", False, C_TEXT_MUTED),
             ("• 0x0031_0000 (Sec 49): ", True, C_PURPLE), ("Lưu 512 bản ghi nhật ký quẹt thẻ (Magic: 'SUCC'/'FAIL').", False, C_TEXT_MUTED)]
        ),
        (
            [("0x0200_0000", True, C_BLUE_ACCENT), ("\\n(SPIMEMIO Cfg)", True, C_TEXT_MUTED)],
            [("• C/ASM: ", True, C_BLUE_ACCENT), ("start.s (li t0, 0x02000000)\\n  Hàm nạp RAM flashio_worker()\\n", False, C_TEXT_DARK),
             ("• RTL: ", True, C_PURPLE), ("soc_interconnect.v\\n  (sel_spicfg == 0x02000000), spimemio.v", False, C_TEXT_DARK)],
            [("• Thanh ghi Bit-Bang SPI Flash: ", True, C_TEXT_DARK), ("Cho phép CPU ngắt tạm thời chế độ đọc XIP để phát xung SPI trực tiếp.\\n", False, C_TEXT_MUTED),
             ("• Thực hiện lệnh Xóa Sector (0x20) và Ghi Trang (0x02) ", True, C_ROSE), ("vào Flash an toàn mà không nghẽn bus CPU.", False, C_TEXT_MUTED)]
        ),
        (
            [("0x1000_0000 (DIV)\\n0x1000_0004 (DAT)", True, C_BLUE_ACCENT), ("\\n(RFID RDM6300 UART)", True, C_ROSE)],
            [("• C Driver: ", True, C_BLUE_ACCENT), ("soc_regs.h\\n  REG_RFID_UART_DIV, REG_RFID_UART_DAT\\n", False, C_TEXT_DARK),
             ("• RTL: ", True, C_PURPLE), ("soc_interconnect.v (sel_rfid)\\n  u_rfid_uart (uart_mmio.v)", False, C_TEXT_DARK)],
            [("• Giao tiếp đầu đọc thẻ RFID RDM6300 (9600 bps, 8-N-1).\\n", True, C_TEXT_DARK),
             ("• Đọc ký tự từ hàng đợi RX FIFO 32-Byte ", True, C_BLUE_ACCENT), ("(trả về 0xFFFFFFFF khi FIFO rỗng), tự động ghép frame mã thẻ 14-byte STX/ETX.", False, C_TEXT_MUTED)]
        ),
        (
            [("0x3000_0000 (DIV)\\n0x3000_0004 (DAT)", True, C_BLUE_ACCENT), ("\\n(Host PC Console UART)", True, C_AMBER)],
            [("• C Driver: ", True, C_BLUE_ACCENT), ("soc_regs.h\\n  REG_PC_UART_DIV, REG_PC_UART_DAT\\n", False, C_TEXT_DARK),
             ("• RTL: ", True, C_PURPLE), ("soc_interconnect.v (sel_uart)\\n  u_host_uart (uart_mmio.v)", False, C_TEXT_DARK)],
            [("• Giao tiếp máy tính Host PC qua UART (115200 bps, 8-N-1).\\n", True, C_TEXT_DARK),
             ("• Truyền/nhận 2 chiều có FIFO đệm: ", True, C_GREEN), ("Nhận 10 menu lệnh điều khiển CLI từ người dùng và xuất log điểm danh ra console máy tính.", False, C_TEXT_MUTED)]
        ),
        (
            [("0x4000_0000", True, C_BLUE_ACCENT), ("\\n(GPIO Status LEDs)", True, C_GREEN)],
            [("• C Driver: ", True, C_BLUE_ACCENT), ("soc_regs.h\\n  REG_GPIO_LEDS\\n", False, C_TEXT_DARK),
             ("• RTL: ", True, C_PURPLE), ("soc_interconnect.v (sel_gpio)\\n  soc_gpio_mmio.v", False, C_TEXT_DARK)],
            [("• Điều khiển 5 đèn LED chỉ thị trạng thái hoạt động trên FPGA Basys 3:\\n", True, C_TEXT_DARK),
             ("  - Bit 0: Alive (Hệ thống sống)  |  Bit 1: Warn (Thẻ không hợp lệ)\\n  - Bit 2: Granted (Quẹt thẻ đúng) |  Bit 3: Flash access  |  Bit 4: Save OK", False, C_TEXT_MUTED)]
        )
    ]

    for r_idx, r_tuples in enumerate(map_rows_data, 1):
        r_bg = RGBColor(255, 255, 255) if r_idx % 2 == 1 else RGBColor(241, 245, 249)
        for c_idx, c_runs in enumerate(r_tuples):
            d_cell = tbl_map.cell(r_idx, c_idx)
            d_cell.fill.solid()
            d_cell.fill.fore_color.rgb = r_bg
            d_cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            d_cell.margin_left = d_cell.margin_right = Inches(0.08)
            d_cell.margin_top = d_cell.margin_bottom = Inches(0.04)
            tf_d = d_cell.text_frame
            tf_d.word_wrap = True
            p_d = tf_d.paragraphs[0]
            p_d.line_spacing = 1.12
            p_d.space_after = 0
            if c_idx == 0:
                p_d.alignment = PP_ALIGN.CENTER
            for t_txt, t_bold, t_col in c_runs:
                r_elem = p_d.add_run()
                r_elem.text = t_txt
                r_elem.font.name = "Consolas" if c_idx == 0 else "Segoe UI"
                r_elem.font.size = Pt(8.6) if c_idx != 0 else Pt(8.8)
                r_elem.font.bold = t_bold
                r_elem.font.color.rgb = t_col'''

    code = code.replace(target_after_s6, new_slide_4_code)

    # 3. Update slide numbers from former slide 4 to 12 (+1)
    code = code.replace('"Sơ Đồ Khối Kiến Trúc Vi Mạch UART RTL (Draw.io Đen Trắng & Đặc Tả Thiết Kế)", 4,',
                        '"Sơ Đồ Khối Kiến Trúc Vi Mạch UART RTL (Draw.io Đen Trắng & Đặc Tả Thiết Kế)", 5,')

    code = code.replace('"Testbench 1: Kiểm Thử Phần Cứng RTL Thuần Cho UART MMIO & FIFO (tb_uart_rtl.v)", 5,',
                        '"Testbench 1: Kiểm Thử Phần Cứng RTL Thuần Cho UART MMIO & FIFO (tb_uart_rtl.v)", 6,')

    code = code.replace('"Testbench 2: Kiểm Thử Tích Hợp Toàn Diện Top SoC Boot Flash & Ping (tb_uart_ping.v)", 6,',
                        '"Testbench 2: Kiểm Thử Tích Hợp Toàn Diện Top SoC Boot Flash & Ping (tb_uart_ping.v)", 7,')

    code = code.replace('"Danh Sách Thiết Bị & Thiết Lập Kết Nối Phần Cứng FPGA Basys 3", 7,',
                        '"Danh Sách Thiết Bị & Thiết Lập Kết Nối Phần Cứng FPGA Basys 3", 8,')

    code = code.replace('"Các Kịch Bản Thực Nghiệm & Giao Diện Quản Trị Host Console", 8,',
                        '"Các Kịch Bản Thực Nghiệm & Giao Diện Quản Trị Host Console", 9,')

    code = code.replace('"Minh Chứng Ký Duyệt Sign-off, Bản Vẽ OpenROAD & Cấu Hình OpenLane", 9,',
                        '"Minh Chứng Ký Duyệt Sign-off, Bản Vẽ OpenROAD & Cấu Hình OpenLane", 10,')

    code = code.replace('"Tổng Hợp Kết Quả Thiết Kế Vật Lý & Chỉ Số PPA (OpenLane 2 / SkyWater 130nm)", 10,',
                        '"Tổng Hợp Kết Quả Thiết Kế Vật Lý & Chỉ Số PPA (OpenLane 2 / SkyWater 130nm)", 11,')

    code = code.replace('"Phân Tích Định Thời Tĩnh STA & Báo Cáo Multi-Corner Timing (summary.rpt)", 11,',
                        '"Phân Tích Định Thời Tĩnh STA & Báo Cáo Multi-Corner Timing (summary.rpt)", 12,')

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(code)

    print("create_presentation.py successfully updated with Slide 4 (Total 13 slides)!")

if __name__ == "__main__":
    main()
