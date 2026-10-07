import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_test():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    C_NAVY_DARK = RGBColor(10, 15, 30)
    C_NAVY_MID = RGBColor(26, 38, 57)
    C_BLUE_ACCENT = RGBColor(37, 99, 235)
    C_TEXT_DARK = RGBColor(30, 41, 59)
    C_TEXT_MUTED = RGBColor(71, 85, 105)
    C_GREEN = RGBColor(16, 185, 129)
    C_AMBER = RGBColor(245, 158, 11)
    C_PURPLE = RGBColor(139, 92, 246)
    C_ROSE = RGBColor(244, 63, 94)
    C_BG_LIGHT = RGBColor(248, 250, 252)

    slide = prs.slides.add_slide(blank_layout)

    # Header
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = C_BG_LIGHT
    bg.line.fill.background()

    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.1))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = C_BLUE_ACCENT
    top_bar.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.22), Inches(11.733), Inches(0.95))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_cat = tf.paragraphs[0]
    p_cat.text = "PHẦN 3: KIẾN TRÚC VI HỆ THỐNG SOC".upper()
    p_cat.font.name = "Segoe UI"
    p_cat.font.size = Pt(10.5)
    p_cat.font.bold = True
    p_cat.font.color.rgb = C_BLUE_ACCENT
    p_cat.space_after = Pt(2)

    p_title = tf.add_paragraph()
    p_title.text = "Bảng Tra Cứu Địa Chỉ (Memory Map) & Khai Báo Biến Trong C / RTL"
    p_title.font.name = "Segoe UI"
    p_title.font.size = Pt(17.0)
    p_title.font.bold = True
    p_title.font.color.rgb = C_TEXT_DARK

    footer_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.02))
    footer_line.fill.solid()
    footer_line.fill.fore_color.rgb = RGBColor(226, 232, 240)
    footer_line.line.fill.background()

    tb_foot = slide.shapes.add_textbox(Inches(0.8), Inches(7.1), Inches(8.0), Inches(0.3))
    tf_foot = tb_foot.text_frame
    tf_foot.margin_left = tf_foot.margin_top = tf_foot.margin_right = tf_foot.margin_bottom = 0
    p_foot = tf_foot.paragraphs[0]
    p_foot.text = "Đồ Án: SoC PicoRV32 RFID RDM6300 & SPI Flash | FPT Jetking Chip Design - SEM3 | HV: Thái Tuấn Hiệp"
    p_foot.font.name = "Segoe UI"
    p_foot.font.size = Pt(9.5)
    p_foot.font.color.rgb = C_TEXT_MUTED

    tb_num = slide.shapes.add_textbox(Inches(11.0), Inches(7.1), Inches(1.533), Inches(0.3))
    tf_num = tb_num.text_frame
    tf_num.margin_left = tf_num.margin_top = tf_num.margin_right = tf_num.margin_bottom = 0
    p_num = tf_num.paragraphs[0]
    p_num.text = "04 / 13"
    p_num.alignment = PP_ALIGN.RIGHT
    p_num.font.name = "Segoe UI"
    p_num.font.size = Pt(9.5)
    p_num.font.bold = True
    p_num.font.color.rgb = C_BLUE_ACCENT

    # Data definition
    rows_data = [
        (
            [("0x0000_0000", True, C_BLUE_ACCENT), ("\n- 0x0000_03FF", False, C_TEXT_DARK), ("\n(1KB Data SRAM)", True, C_TEXT_MUTED)],
            [("• C/Linker: ", True, C_BLUE_ACCENT), ("sections.lds\n  (RAM: 0x0, _stack_top: 0x400)\n", False, C_TEXT_DARK),
             ("• RTL: ", True, C_PURPLE), ("soc_interconnect.v\n  (sel_sram < 0x400), data_sram.v", False, C_TEXT_DARK)],
            [("• Vùng nhớ RAM tĩnh 1 chu kỳ clock ", True, C_TEXT_DARK), ("(phản hồi sram_ready = 1 tức thì).\n", False, C_TEXT_MUTED),
             ("• Lưu trữ con trỏ ngăn xếp Stack (sp), ", True, C_BLUE_ACCENT), ("biến cục bộ và mảng dữ liệu tạm thời cho Firmware C, đảm bảo tính thời gian thực.", False, C_TEXT_MUTED)]
        ),
        (
            [("0x0010_0000", True, C_BLUE_ACCENT), ("\n- 0x00FF_FFFF", False, C_TEXT_DARK), ("\n(SPI Flash XIP 4MB)", True, C_GREEN)],
            [("• C/Linker: ", True, C_BLUE_ACCENT), ("sections.lds (FLASH: 0x250000)\n  soc_regs.h (USER: 0x300000, LOG: 0x310000)\n", False, C_TEXT_DARK),
             ("• RTL: ", True, C_PURPLE), ("soc_interconnect.v\n  (sel_spimem), spimemio.v", False, C_TEXT_DARK)],
            [("• 0x0025_0000: ", True, C_BLUE_ACCENT), ("Mã lệnh Firmware XIP (thực thi trực tiếp từ Flash).\n", False, C_TEXT_MUTED),
             ("• 0x0030_0000 (Sec 48): ", True, C_GREEN), ("Database 4.096 thẻ hợp lệ (Magic: 'RFID').\n", False, C_TEXT_MUTED),
             ("• 0x0031_0000 (Sec 49): ", True, C_PURPLE), ("Lưu 512 bản ghi nhật ký quẹt thẻ (Magic: 'SUCC'/'FAIL').", False, C_TEXT_MUTED)]
        ),
        (
            [("0x0200_0000", True, C_BLUE_ACCENT), ("\n(SPIMEMIO Cfg)", True, C_TEXT_MUTED)],
            [("• C/ASM: ", True, C_BLUE_ACCENT), ("start.s (li t0, 0x02000000)\n  Hàm nạp RAM flashio_worker()\n", False, C_TEXT_DARK),
             ("• RTL: ", True, C_PURPLE), ("soc_interconnect.v\n  (sel_spicfg == 0x02000000), spimemio.v", False, C_TEXT_DARK)],
            [("• Thanh ghi Bit-Bang SPI Flash: ", True, C_TEXT_DARK), ("Cho phép CPU ngắt tạm thời chế độ đọc XIP để phát xung SPI trực tiếp.\n", False, C_TEXT_MUTED),
             ("• Thực hiện lệnh Xóa Sector (0x20) và Ghi Trang (0x02) ", True, C_ROSE), ("vào Flash an toàn.", False, C_TEXT_MUTED)]
        ),
        (
            [("0x1000_0000 (DIV)\n0x1000_0004 (DAT)", True, C_BLUE_ACCENT), ("\n(RFID RDM6300 UART)", True, C_ROSE)],
            [("• C Driver: ", True, C_BLUE_ACCENT), ("soc_regs.h\n  REG_RFID_UART_DIV, REG_RFID_UART_DAT\n", False, C_TEXT_DARK),
             ("• RTL: ", True, C_PURPLE), ("soc_interconnect.v (sel_rfid)\n  u_rfid_uart (uart_mmio.v)", False, C_TEXT_DARK)],
            [("• Giao tiếp đầu đọc thẻ RFID RDM6300 (9600 bps, 8-N-1).\n", True, C_TEXT_DARK),
             ("• Đọc ký tự từ hàng đợi RX FIFO 32-Byte ", True, C_BLUE_ACCENT), ("(trả về 0xFFFFFFFF khi FIFO rỗng), tự động ghép frame mã thẻ 14-byte STX/ETX.", False, C_TEXT_MUTED)]
        ),
        (
            [("0x3000_0000 (DIV)\n0x3000_0004 (DAT)", True, C_BLUE_ACCENT), ("\n(Host PC Console UART)", True, C_AMBER)],
            [("• C Driver: ", True, C_BLUE_ACCENT), ("soc_regs.h\n  REG_PC_UART_DIV, REG_PC_UART_DAT\n", False, C_TEXT_DARK),
             ("• RTL: ", True, C_PURPLE), ("soc_interconnect.v (sel_uart)\n  u_host_uart (uart_mmio.v)", False, C_TEXT_DARK)],
            [("• Giao tiếp máy tính Host PC qua UART (115200 bps, 8-N-1).\n", True, C_TEXT_DARK),
             ("• Truyền/nhận 2 chiều có FIFO đệm: ", True, C_GREEN), ("Nhận 10 menu lệnh điều khiển CLI từ người dùng và xuất log điểm danh ra console máy tính.", False, C_TEXT_MUTED)]
        ),
        (
            [("0x4000_0000", True, C_BLUE_ACCENT), ("\n(GPIO Status LEDs)", True, C_GREEN)],
            [("• C Driver: ", True, C_BLUE_ACCENT), ("soc_regs.h\n  REG_GPIO_LEDS\n", False, C_TEXT_DARK),
             ("• RTL: ", True, C_PURPLE), ("soc_interconnect.v (sel_gpio)\n  soc_gpio_mmio.v", False, C_TEXT_DARK)],
            [("• Điều khiển 5 đèn LED chỉ thị trạng thái hoạt động trên FPGA Basys 3:\n", True, C_TEXT_DARK),
             ("  - Bit 0: Alive (Hệ thống sống)  |  Bit 1: Warn (Thẻ không hợp lệ)\n  - Bit 2: Granted (Quẹt thẻ đúng) |  Bit 3: Flash access  |  Bit 4: Save OK", False, C_TEXT_MUTED)]
        )
    ]

    table_shape = slide.shapes.add_table(7, 3, Inches(0.8), Inches(1.30), Inches(11.733), Inches(5.62))
    table = table_shape.table
    table.columns[0].width = Inches(2.35)
    table.columns[1].width = Inches(3.60)
    table.columns[2].width = Inches(5.783)

    headers = ["DẢI ĐỊA CHỈ (ADDRESS / OFFSET)", "NƠI KHAI BÁO TRONG C VÀ RTL", "Ý NGHĨA SỬ DỤNG VỚI FIRMWARE C & NGHIỆP VỤ"]
    for col_idx, h in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY_MID
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.margin_left = cell.margin_right = Inches(0.08)
        cell.margin_top = cell.margin_bottom = Inches(0.04)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER

    for row_idx, r_data in enumerate(rows_data, 1):
        bg_row = RGBColor(255, 255, 255) if row_idx % 2 == 1 else RGBColor(241, 245, 249)
        for col_idx, col_runs in enumerate(r_data):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_row
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.margin_left = cell.margin_right = Inches(0.08)
            cell.margin_top = cell.margin_bottom = Inches(0.04)
            tf_c = cell.text_frame
            tf_c.word_wrap = True
            p = tf_c.paragraphs[0]
            p.line_spacing = 1.12
            p.space_after = 0
            if col_idx == 0:
                p.alignment = PP_ALIGN.CENTER
            
            for text_str, is_bold, text_color in col_runs:
                run = p.add_run()
                run.text = text_str
                run.font.name = "Consolas" if col_idx == 0 else "Segoe UI"
                run.font.size = Pt(8.6) if col_idx != 0 else Pt(8.8)
                run.font.bold = is_bold
                run.font.color.rgb = text_color

    test_path = os.path.join(os.path.dirname(__file__), "test_table_slide.pptx")
    prs.save(test_path)
    print(f"Saved test presentation: {test_path}")

if __name__ == "__main__":
    build_test()
