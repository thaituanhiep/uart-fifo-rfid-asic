import os
import re

script_path = r"d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\create_presentation.py"

with open(script_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update TOTAL_SLIDES = 13 to TOTAL_SLIDES = 14
content = content.replace("TOTAL_SLIDES = 13", "TOTAL_SLIDES = 14")

# 2. Slide 3 code to insert
slide3_code = '''    # =========================================================================
    # SLIDE 03: PHẦN 1 - TỔNG QUAN NHỮNG GÌ SẢN PHẨM ĐÃ LÀM ĐƯỢC (4 TRỤ CỘT)
    # =========================================================================
    s_overview = prs.slides.add_slide(blank_layout)
    add_header(s_overview, "Phần 1: Giới Thiệu Dự Án",
               "Tổng Quan Những Gì Sản Phẩm Đã Thực Hiện Thành Công", 3, total_slides=TOTAL_SLIDES)

    overview_cards = [
        {
            "num": "01",
            "icon": "💻",
            "title": "THIẾT KẾ RTL CHẠY FIRMWARE C & NỀN TẢNG MỞ",
            "border_color": C_BLUE_ACCENT,
            "badge_bg": RGBColor(239, 246, 255),
            "points": [
                ("Thực thi Firmware C mượt mà:", "RTL tích hợp CPU RISC-V PicoRV32 (RV32I), hỗ trợ thực thi trực tiếp firmware C bare-metal."),
                ("Thao tác SPI Flash & LED GPIO:", "RTL cung cấp bus MMIO cho phép C đọc/ghi/xóa dữ liệu Flash và điều khiển chớp nháy LED."),
                ("Kiến trúc mở rộng linh hoạt:", "Dễ dàng nạp lại firmware C để làm các nghiệp vụ nhúng khác, không chỉ quản lý thẻ RFID.")
            ]
        },
        {
            "num": "02",
            "icon": "⚙️",
            "title": "FIRMWARE C XỬ LÝ THẺ & THỰC THI TRÊN CHIP",
            "border_color": C_GREEN,
            "badge_bg": RGBColor(240, 253, 244),
            "points": [
                ("Nghiệp vụ thẻ an ninh tại chỗ:", "Thuật toán C giải mã chuỗi RFID RDM6300, đối chiếu Whitelist tức thì (< 10 µs), ghi nhật ký Flash."),
                ("Thực thi code C ngay trên chip:", "Cơ chế XIP kéo lệnh từ Flash kết hợp nạp worker vào 1KB SRAM để xóa/ghi Flash an toàn."),
                ("Tối ưu hóa Bare-metal độc lập:", "Hoạt động tin cậy không cần hệ điều hành (RTOS/Linux), khởi động tức thì và tiết kiệm bộ nhớ.")
            ]
        },
        {
            "num": "03",
            "icon": "🎯",
            "title": "TRIỂN KHAI THỰC TẾ TRÊN FPGA BASYS 3",
            "border_color": RGBColor(217, 119, 6),
            "badge_bg": RGBColor(254, 243, 199),
            "points": [
                ("Hiện thực hóa trên phần cứng thật:", "Tổng hợp bitstream Vivado và nạp chạy ổn định 100% trên bo mạch FPGA Digilent Basys 3."),
                ("Ghép nối ngoại vi hoàn chỉnh:", "Kết nối vật lý với đầu đọc RFID RDM6300 125kHz, nguồn MB102 5V và trở đệm 1kΩ chống sốc I/O."),
                ("Kiểm chứng thực nghiệm thành công:", "Quẹt thẻ RFID thật phản hồi tức thì, còi/LED báo hiệu chính xác và lưu trữ bền vững vào Flash.")
            ]
        },
        {
            "num": "04",
            "icon": "🏭",
            "title": "ÁP DỤNG OPENLANE TẠO GDSII ĐẠT CHUẨN SX",
            "border_color": RGBColor(147, 51, 234),
            "badge_bg": RGBColor(250, 245, 255),
            "points": [
                ("Tự động hóa RTL-to-GDSII:", "Ứng dụng thành công OpenLane 2 trên tiến trình SkyWater 130nm, thiết kế vật lý nhanh chóng và chính xác."),
                ("Ký duyệt Sign-off sạch hoàn toàn:", "Đạt 100% tiêu chuẩn nhà máy: 0 DRC, 0 LVS, 0 Antenna violations trên toàn bộ 5 lớp kim loại."),
                ("Sẵn sàng sản xuất (Tape-out Ready):", "Die 1.87 mm², 164K cells, Fmax đạt 92.81 MHz (vượt 85% mục tiêu), đủ tiêu chuẩn gia công vi mạch.")
            ]
        }
    ]

    grid_w = Inches(5.72)
    grid_h = Inches(2.70)
    col_xs = [Inches(0.80), Inches(6.81)]
    row_ys = [Inches(1.28), Inches(4.20)]

    for idx, c_data in enumerate(overview_cards):
        cx = col_xs[idx % 2]
        cy = row_ys[idx // 2]

        add_card(s_overview, cx, cy, grid_w, grid_h, bg_color=C_WHITE, border_color=c_data["border_color"], border_width=1.5)

        banner = s_overview.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx + Inches(0.12), cy + Inches(0.12), grid_w - Inches(0.24), Inches(0.48))
        try:
            banner.adjustments[0] = 0.08
        except Exception:
            pass
        banner.fill.solid()
        banner.fill.fore_color.rgb = c_data["badge_bg"]
        banner.line.color.rgb = c_data["border_color"]
        banner.line.width = Pt(1.2)

        tb_bh = s_overview.shapes.add_textbox(cx + Inches(0.16), cy + Inches(0.14), grid_w - Inches(0.32), Inches(0.44))
        tf_bh = tb_bh.text_frame
        tf_bh.word_wrap = True
        tf_bh.margin_left = tf_bh.margin_top = tf_bh.margin_right = tf_bh.margin_bottom = 0

        p_bh = tf_bh.paragraphs[0]
        p_bh.text = f"{c_data['icon']}  [{c_data['num']}]  {c_data['title']}"
        p_bh.font.name = "Segoe UI"
        p_bh.font.size = Pt(14.0)
        p_bh.font.bold = True
        p_bh.font.color.rgb = c_data["border_color"]
        p_bh.alignment = PP_ALIGN.LEFT

        tb_body = s_overview.shapes.add_textbox(cx + Inches(0.18), cy + Inches(0.68), grid_w - Inches(0.36), grid_h - Inches(0.76))
        tf_body = tb_body.text_frame
        tf_body.word_wrap = True
        tf_body.margin_left = tf_body.margin_top = tf_body.margin_right = tf_body.margin_bottom = 0

        for p_idx, (b_lbl, b_val) in enumerate(c_data["points"]):
            p = tf_body.paragraphs[0] if p_idx == 0 else tf_body.add_paragraph()
            p.space_after = Pt(6)
            p.line_spacing = 1.16

            r_lbl = p.add_run()
            r_lbl.text = f"• {b_lbl} "
            r_lbl.font.name = "Segoe UI"
            r_lbl.font.size = Pt(13.2)
            r_lbl.font.bold = True
            r_lbl.font.color.rgb = C_TEXT_DARK

            r_val = p.add_run()
            r_val.text = b_val
            r_val.font.name = "Segoe UI"
            r_val.font.size = Pt(12.6)
            r_val.font.color.rgb = RGBColor(51, 65, 85)

'''

# Insert slide3_code right before "# SLIDE 3: PHẦN 3 - SƠ ĐỒ KHỐI TỔNG THỂ SOC"
target_marker = "# SLIDE 3: PHẦN 3 - SƠ ĐỒ KHỐI TỔNG THỂ SOC"
if target_marker not in content:
    raise ValueError(f"Could not find marker '{target_marker}' in create_presentation.py")

content = content.replace(target_marker, slide3_code + "    # =========================================================================\n    " + target_marker)

# 3. Update subsequent slide numbers in comments and add_header calls
# Slide 3 -> Slide 4
content = content.replace(
    'Sơ Đồ Khối Kiến Trúc Vi Hệ Thống SoC PicoRV32 (4MB Flash, 1KB SRAM, 32 Fifo)", 3, total_slides=TOTAL_SLIDES)',
    'Sơ Đồ Khối Kiến Trúc Vi Hệ Thống SoC PicoRV32 (4MB Flash, 1KB SRAM, 32 Fifo)", 4, total_slides=TOTAL_SLIDES)'
)
content = content.replace("# SLIDE 3: PHẦN 3 - SƠ ĐỒ KHỐI TỔNG THỂ SOC", "# SLIDE 04: PHẦN 3 - SƠ ĐỒ KHỐI TỔNG THỂ SOC")

# Slide 4 -> Slide 5
content = content.replace(
    'Bảng Tra Cứu Địa Chỉ (Memory Map) & Khai Báo Biến Trong C / RTL", 4, total_slides=TOTAL_SLIDES)',
    'Bảng Tra Cứu Địa Chỉ (Memory Map) & Khai Báo Biến Trong C / RTL", 5, total_slides=TOTAL_SLIDES)'
)
content = content.replace("# SLIDE 04: PHẦN 3 - BẢNG TRA CỨU ĐỊA CHỈ MEMORY MAP", "# SLIDE 05: PHẦN 3 - BẢNG TRA CỨU ĐỊA CHỈ MEMORY MAP")

# Slide 5 -> Slide 6
content = content.replace(
    'Các Kịch Bản Thực Nghiệm & Giao Diện Quản Trị Host Console", 5, total_slides=TOTAL_SLIDES)',
    'Các Kịch Bản Thực Nghiệm & Giao Diện Quản Trị Host Console", 6, total_slides=TOTAL_SLIDES)'
)
content = content.replace("# SLIDE 05: PHẦN 5 - DEMO THỰC NGHIỆM: CÁC KỊCH BẢN", "# SLIDE 06: PHẦN 5 - DEMO THỰC NGHIỆM: CÁC KỊCH BẢN")

# Slide 6 -> Slide 7
content = content.replace(
    'Sơ Đồ Khối Kiến Trúc Vi Mạch UART RTL (Draw.io Đen Trắng & Đặc Tả Thiết Kế)", 6, total_slides=TOTAL_SLIDES)',
    'Sơ Đồ Khối Kiến Trúc Vi Mạch UART RTL (Draw.io Đen Trắng & Đặc Tả Thiết Kế)", 7, total_slides=TOTAL_SLIDES)'
)
content = content.replace("# SLIDE 06: PHẦN 3 - SƠ ĐỒ KHỐI KIẾN TRÚC VI MẠCH UART RTL", "# SLIDE 07: PHẦN 3 - SƠ ĐỒ KHỐI KIẾN TRÚC VI MẠCH UART RTL")

# Slide 7 -> Slide 8
content = content.replace(
    'Testbench 1: Kiểm Thử Phần Cứng RTL Thuần Cho UART MMIO & FIFO (tb_uart_rtl.v)", 7, total_slides=TOTAL_SLIDES)',
    'Testbench 1: Kiểm Thử Phần Cứng RTL Thuần Cho UART MMIO & FIFO (tb_uart_rtl.v)", 8, total_slides=TOTAL_SLIDES)'
)
content = content.replace("# SLIDE 07: PHẦN 4 - HỆ THỐNG TESTBENCH: UART RTL", "# SLIDE 08: PHẦN 4 - HỆ THỐNG TESTBENCH: UART RTL")

# Slide 8 -> Slide 9
content = content.replace(
    'Testbench 2: Kiểm Thử Tích Hợp Toàn Diện Top SoC Boot Flash & Ping (tb_uart_ping.v)", 8, total_slides=TOTAL_SLIDES)',
    'Testbench 2: Kiểm Thử Tích Hợp Toàn Diện Top SoC Boot Flash & Ping (tb_uart_ping.v)", 9, total_slides=TOTAL_SLIDES)'
)
content = content.replace("# SLIDE 08: PHẦN 4 - HỆ THỐNG TESTBENCH: TOP SOC BOOT & PING", "# SLIDE 09: PHẦN 4 - HỆ THỐNG TESTBENCH: TOP SOC BOOT & PING")

# Slide 9 -> Slide 10
content = content.replace(
    'Danh Sách Thiết Bị & Thiết Lập Kết Nối Phần Cứng FPGA Basys 3", 9, total_slides=TOTAL_SLIDES)',
    'Danh Sách Thiết Bị & Thiết Lập Kết Nối Phần Cứng FPGA Basys 3", 10, total_slides=TOTAL_SLIDES)'
)
content = content.replace("# SLIDE 09: PHẦN 5 - DEMO THỰC NGHIỆM TRÊN FPGA BASYS 3", "# SLIDE 10: PHẦN 5 - DEMO THỰC NGHIỆM TRÊN FPGA BASYS 3")

# Slide 10 -> Slide 11
content = content.replace(
    'Minh Chứng Ký Duyệt Sign-off, Bản Vẽ OpenROAD & Cấu Hình OpenLane", 10, total_slides=TOTAL_SLIDES)',
    'Minh Chứng Ký Duyệt Sign-off, Bản Vẽ OpenROAD & Cấu Hình OpenLane", 11, total_slides=TOTAL_SLIDES)'
)
content = content.replace("# SLIDE 9: PHẦN 6 - MINH CHỨNG KÝ DUYỆT SIGN-OFF", "# SLIDE 11: PHẦN 6 - MINH CHỨNG KÝ DUYỆT SIGN-OFF")

# Slide 11 -> Slide 12
content = content.replace(
    'Tổng Hợp Kết Quả Thiết Kế Vật Lý & Chỉ Số PPA (OpenLane 2 / SkyWater 130nm)", 11, total_slides=TOTAL_SLIDES)',
    'Tổng Hợp Kết Quả Thiết Kế Vật Lý & Chỉ Số PPA (OpenLane 2 / SkyWater 130nm)", 12, total_slides=TOTAL_SLIDES)'
)
content = content.replace("# SLIDE 10: PHẦN 6 - BẢNG TỔNG HỢP KẾT QUẢ VẬT LÝ", "# SLIDE 12: PHẦN 6 - BẢNG TỔNG HỢP KẾT QUẢ VẬT LÝ")

# Slide 12 -> Slide 13
content = content.replace(
    'Phân Tích Định Thời Tĩnh STA & Báo Cáo Multi-Corner Timing (summary.rpt)", 12, total_slides=TOTAL_SLIDES)',
    'Phân Tích Định Thời Tĩnh STA & Báo Cáo Multi-Corner Timing (summary.rpt)", 13, total_slides=TOTAL_SLIDES)'
)
content = content.replace("# SLIDE 11: PHẦN 6 - PHÂN TÍCH ĐỊNH THỜI TĨNH STA", "# SLIDE 13: PHẦN 6 - PHÂN TÍCH ĐỊNH THỜI TĨNH STA")

# Slide 13 -> Slide 14
content = content.replace(
    '# SLIDE 12: TỔNG KẾT ĐỀ TÀI & HƯỚNG PHÁT TRIỂN (THANK YOU SLIDE)',
    '# SLIDE 14: TỔNG KẾT ĐỀ TÀI & HƯỚNG PHÁT TRIỂN (THANK YOU SLIDE)'
)

with open(script_path, "w", encoding="utf-8") as f:
    f.write(content)

print("create_presentation.py successfully updated with new Slide 3 and 14 slides total!")
