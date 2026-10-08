import os
import re

script_path = r"d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\create_presentation.py"

with open(script_path, "r", encoding="utf-8") as f:
    content = f.read()

# Pattern to replace the entire Slide 3 block
old_slide3_start = "    # =========================================================================\n    # SLIDE 03: PHẦN 1 - TỔNG QUAN NHỮNG GÌ SẢN PHẨM ĐÃ LÀM ĐƯỢC (4 TRỤ CỘT)"
old_slide3_end = "    # =========================================================================\n    # SLIDE 04: PHẦN 3 - SƠ ĐỒ KHỐI TỔNG THỂ SOC"

new_slide3_block = '''    # =========================================================================
    # SLIDE 03: PHẦN 1 - TỔNG QUAN NHỮNG GÌ SẢN PHẨM ĐÃ LÀM ĐƯỢC (4 TRỤ CỘT)
    # =========================================================================
    s_overview = prs.slides.add_slide(blank_layout)
    add_header(s_overview, "Phần 1: Giới Thiệu Dự Án",
               "Tổng Quan Những Gì Sản Phẩm Đã Thực Hiện Thành Công", 3, total_slides=TOTAL_SLIDES)

    overview_cards = [
        {
            "num": "01",
            "icon": "💻",
            "title": "THIẾT KẾ VI MẠCH RTL & NỀN TẢNG SOC MỞ",
            "border_color": C_BLUE_ACCENT,
            "badge_bg": RGBColor(239, 246, 255),
            "points": [
                ("Thực thi Firmware C mượt mà:", "RTL tích hợp CPU RISC-V PicoRV32 (RV32I), kéo lệnh và chạy trực tiếp code C bare-metal."),
                ("Thao tác SPI Flash & LED GPIO:", "RTL cung cấp bus MMIO cho phép C đọc/ghi/xóa dữ liệu Flash và điều khiển chớp nháy LED."),
                ("Kiến trúc mở rộng linh hoạt:", "Dễ dàng nạp lại firmware C để làm các nghiệp vụ nhúng khác, không chỉ quản lý thẻ RFID.")
            ]
        },
        {
            "num": "02",
            "icon": "⚙️",
            "title": "FIRMWARE C THỰC THI TRỰC TIẾP TRÊN CHIP",
            "border_color": C_GREEN,
            "badge_bg": RGBColor(240, 253, 244),
            "points": [
                ("Xử lý thẻ an ninh tại chỗ:", "Thuật toán C giải mã chuỗi RFID RDM6300, đối chiếu Whitelist tức thì (< 10 µs), ghi log Flash."),
                ("Thực thi code C ngay trên chip:", "Cơ chế XIP kéo lệnh từ Flash kết hợp nạp worker vào 1KB SRAM để xóa/ghi Flash an toàn."),
                ("Tối ưu hóa Bare-metal độc lập:", "Vận hành tin cậy không cần hệ điều hành (RTOS/Linux), khởi động tức thì và tiết kiệm bộ nhớ.")
            ]
        },
        {
            "num": "03",
            "icon": "🎯",
            "title": "TRIỂN KHAI THỰC TẾ BO MẠCH FPGA BASYS 3",
            "border_color": RGBColor(217, 119, 6),
            "badge_bg": RGBColor(254, 243, 199),
            "points": [
                ("Hiện thực hóa trên phần cứng thật:", "Tổng hợp bitstream Vivado và nạp chạy ổn định 100% trên bo mạch FPGA Digilent Basys 3."),
                ("Ghép nối ngoại vi hoàn chỉnh:", "Kết nối vật lý với module RFID RDM6300 125kHz, nguồn MB102 5V và trở đệm 1kΩ bảo vệ I/O."),
                ("Kiểm chứng thực nghiệm thành công:", "Quẹt thẻ RFID thật phản hồi tức thì, còi/LED báo hiệu chính xác và lưu bền vững vào Flash.")
            ]
        },
        {
            "num": "04",
            "icon": "🏭",
            "title": "LUỒNG ASIC OPENLANE ĐẠT CHUẨN TAPE-OUT",
            "border_color": RGBColor(147, 51, 234),
            "badge_bg": RGBColor(250, 245, 255),
            "points": [
                ("Tự động hóa RTL-to-GDSII:", "Ứng dụng OpenLane 2 trên SkyWater 130nm, thiết kế vật lý tự động và chuyển sang GDSII nhanh chóng."),
                ("Ký duyệt Sign-off sạch hoàn toàn:", "Đạt 100% tiêu chuẩn nhà máy: 0 DRC, 0 LVS, 0 Antenna violations trên toàn bộ 5 lớp kim loại."),
                ("Sẵn sàng Tape-out xuất xưởng:", "Die 1.87 mm², 164K cells, Fmax = 92.81 MHz (vượt 85% mục tiêu), đủ chuẩn gia công nhà máy.")
            ]
        }
    ]

    grid_w = Inches(5.72)
    grid_h = Inches(2.72)
    col_xs = [Inches(0.80), Inches(6.81)]
    row_ys = [Inches(1.26), Inches(4.18)]

    for idx, c_data in enumerate(overview_cards):
        cx = col_xs[idx % 2]
        cy = row_ys[idx // 2]

        add_card(s_overview, cx, cy, grid_w, grid_h, bg_color=C_WHITE, border_color=c_data["border_color"], border_width=1.5)

        banner = s_overview.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx + Inches(0.12), cy + Inches(0.10), grid_w - Inches(0.24), Inches(0.42))
        try:
            banner.adjustments[0] = 0.08
        except Exception:
            pass
        banner.fill.solid()
        banner.fill.fore_color.rgb = c_data["badge_bg"]
        banner.line.color.rgb = c_data["border_color"]
        banner.line.width = Pt(1.2)

        tb_bh = s_overview.shapes.add_textbox(cx + Inches(0.16), cy + Inches(0.11), grid_w - Inches(0.32), Inches(0.38))
        tf_bh = tb_bh.text_frame
        tf_bh.word_wrap = False
        tf_bh.margin_left = tf_bh.margin_top = tf_bh.margin_right = tf_bh.margin_bottom = 0

        p_bh = tf_bh.paragraphs[0]
        p_bh.text = f"{c_data['icon']}  [{c_data['num']}]  {c_data['title']}"
        p_bh.font.name = "Segoe UI"
        p_bh.font.size = Pt(12.8)
        p_bh.font.bold = True
        p_bh.font.color.rgb = c_data["border_color"]
        p_bh.alignment = PP_ALIGN.LEFT

        tb_body = s_overview.shapes.add_textbox(cx + Inches(0.18), cy + Inches(0.60), grid_w - Inches(0.36), grid_h - Inches(0.68))
        tf_body = tb_body.text_frame
        tf_body.word_wrap = True
        tf_body.margin_left = tf_body.margin_top = tf_body.margin_right = tf_body.margin_bottom = 0

        for p_idx, (b_lbl, b_val) in enumerate(c_data["points"]):
            p = tf_body.paragraphs[0] if p_idx == 0 else tf_body.add_paragraph()
            p.space_after = Pt(5.5)
            p.line_spacing = 1.15

            r_lbl = p.add_run()
            r_lbl.text = f"• {b_lbl} "
            r_lbl.font.name = "Segoe UI"
            r_lbl.font.size = Pt(12.5)
            r_lbl.font.bold = True
            r_lbl.font.color.rgb = C_TEXT_DARK

            r_val = p.add_run()
            r_val.text = b_val
            r_val.font.name = "Segoe UI"
            r_val.font.size = Pt(12.0)
            r_val.font.color.rgb = RGBColor(51, 65, 85)

'''

start_idx = content.find(old_slide3_start)
end_idx = content.find(old_slide3_end)

if start_idx == -1 or end_idx == -1:
    raise ValueError(f"Could not locate Slide 3 section in file! start_idx={start_idx}, end_idx={end_idx}")

content = content[:start_idx] + new_slide3_block + content[end_idx:]

with open(script_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Slide 3 successfully tuned for 1-line banners and perfect text wrapping!")
