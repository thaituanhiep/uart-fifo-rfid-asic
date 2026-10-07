import os

def reorder_host_console():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    target_file = os.path.join(cur_dir, "create_presentation.py")

    with open(target_file, "r", encoding="utf-8") as f:
        code = f.read()

    # Find the Host Console slide code block
    host_start_str = "    # =========================================================================\n    # SLIDE 8: PHẦN 5 - DEMO THỰC NGHIỆM TRÊN FPGA BASYS 3: CÁC KỊCH BẢN THỰC TẾ\n    # ========================================================================="
    if host_start_str not in code:
        # try more generic search
        idx_host = code.find("s23 = prs.slides.add_slide(blank_layout)")
        # find comment before it
        idx_host_start = code.rfind("    # ===", 0, idx_host)
    else:
        idx_host_start = code.find(host_start_str)

    # Find where Host Console ends (before next slide comment)
    idx_next_slide = code.find("    # =========================================================================\n    # SLIDE 9: PHẦN 6", idx_host_start)
    if idx_next_slide == -1:
        idx_next_slide = code.find("s24 = prs.slides.add_slide(blank_layout)", idx_host_start)
        idx_next_slide = code.rfind("    # ===", 0, idx_next_slide)

    host_code_block = code[idx_host_start:idx_next_slide].strip()

    # Remove host_code_block from its old location
    code_without_host = code[:idx_host_start] + code[idx_next_slide:]

    # Find Slide 4 (s_map) end
    # It ends before "# SLIDE 4: PHẦN 3 - SƠ ĐỒ KHỐI KIẾN TRÚC VI MẠCH UART RTL" or "s8 = prs.slides.add_slide(blank_layout)"
    idx_s8 = code_without_host.find("s8 = prs.slides.add_slide(blank_layout)")
    idx_s8_start = code_without_host.rfind("    # ===", 0, idx_s8)

    # Update host_code_block to have slide_num = 5
    # Category: "Phần 5: Demo Chức Năng Sản Phẩm"
    host_code_block_updated = host_code_block.replace(
        'add_header(s23, "Phần 5: Demo Chức Năng Sản Phẩm",\n               "Các Kịch Bản Thực Nghiệm & Giao Diện Quản Trị Host Console", 9, total_slides=TOTAL_SLIDES)',
        'add_header(s23, "Phần 5: Demo Chức Năng Sản Phẩm",\n               "Các Kịch Bản Thực Nghiệm & Giao Diện Quản Trị Host Console", 5, total_slides=TOTAL_SLIDES)'
    ).replace(
        'add_header(s23, "Phần 5: Demo Chức Năng Sản Phẩm",\n               "Các Kịch Bản Thực Nghiệm & Giao Diện Quản Trị Host Console", 8, total_slides=TOTAL_SLIDES)',
        'add_header(s23, "Phần 5: Demo Chức Năng Sản Phẩm",\n               "Các Kịch Bản Thực Nghiệm & Giao Diện Quản Trị Host Console", 5, total_slides=TOTAL_SLIDES)'
    )

    # Insert host_code_block right before s8
    code_new = (
        code_without_host[:idx_s8_start] +
        "    # =========================================================================\n" +
        "    # SLIDE 5: PHẦN 5 - CÁC KỊCH BẢN THỰC NGHIỆM & GIAO DIỆN QUẢN TRỊ HOST CONSOLE\n" +
        "    # =========================================================================\n" +
        "    " + host_code_block_updated.strip() + "\n\n" +
        code_without_host[idx_s8_start:]
    )

    # Now update subsequent slide numbers:
    # s8 (UART RTL): was 5 -> now 6
    code_new = code_new.replace(
        '"Sơ Đồ Khối Kiến Trúc Vi Mạch UART RTL (Draw.io Đen Trắng & Đặc Tả Thiết Kế)", 5,',
        '"Sơ Đồ Khối Kiến Trúc Vi Mạch UART RTL (Draw.io Đen Trắng & Đặc Tả Thiết Kế)", 6,'
    ).replace(
        '"Sơ Đồ Khối Kiến Trúc Vi Mạch UART RTL (Draw.io Đen Trắng & Đặc Tả Thiết Kế)", 4,',
        '"Sơ Đồ Khối Kiến Trúc Vi Mạch UART RTL (Draw.io Đen Trắng & Đặc Tả Thiết Kế)", 6,'
    )

    # s20 (TB UART RTL): was 6 -> now 7
    code_new = code_new.replace(
        '"Testbench 1: Kiểm Thử Phần Cứng RTL Thuần Cho UART MMIO & FIFO (tb_uart_rtl.v)", 6,',
        '"Testbench 1: Kiểm Thử Phần Cứng RTL Thuần Cho UART MMIO & FIFO (tb_uart_rtl.v)", 7,'
    ).replace(
        '"Testbench 1: Kiểm Thử Phần Cứng RTL Thuần Cho UART MMIO & FIFO (tb_uart_rtl.v)", 5,',
        '"Testbench 1: Kiểm Thử Phần Cứng RTL Thuần Cho UART MMIO & FIFO (tb_uart_rtl.v)", 7,'
    )

    # s21 (TB UART PING): was 7 -> now 8
    code_new = code_new.replace(
        '"Testbench 2: Kiểm Thử Tích Hợp Toàn Diện Top SoC Boot Flash & Ping (tb_uart_ping.v)", 7,',
        '"Testbench 2: Kiểm Thử Tích Hợp Toàn Diện Top SoC Boot Flash & Ping (tb_uart_ping.v)", 8,'
    ).replace(
        '"Testbench 2: Kiểm Thử Tích Hợp Toàn Diện Top SoC Boot Flash & Ping (tb_uart_ping.v)", 6,',
        '"Testbench 2: Kiểm Thử Tích Hợp Toàn Diện Top SoC Boot Flash & Ping (tb_uart_ping.v)", 8,'
    )

    # s22 (Device Setup): was 8 -> now 9
    code_new = code_new.replace(
        '"Danh Sách Thiết Bị & Thiết Lập Kết Nối Phần Cứng FPGA Basys 3", 8,',
        '"Danh Sách Thiết Bị & Thiết Lập Kết Nối Phần Cứng FPGA Basys 3", 9,'
    ).replace(
        '"Danh Sách Thiết Bị & Thiết Lập Kết Nối Phần Cứng FPGA Basys 3", 7,',
        '"Danh Sách Thiết Bị & Thiết Lập Kết Nối Phần Cứng FPGA Basys 3", 9,'
    )

    # s24 (ASIC Sign-off OpenLane 2): 10
    code_new = code_new.replace(
        '"Minh Chứng Ký Duyệt Sign-off, Bản Vẽ OpenROAD & Cấu Hình OpenLane", 9,',
        '"Minh Chứng Ký Duyệt Sign-off, Bản Vẽ OpenROAD & Cấu Hình OpenLane", 10,'
    )

    # s25 (ASIC PPA): 11
    code_new = code_new.replace(
        '"Tổng Hợp Kết Quả Thiết Kế Vật Lý & Chỉ Số PPA (OpenLane 2 / SkyWater 130nm)", 10,',
        '"Tổng Hợp Kết Quả Thiết Kế Vật Lý & Chỉ Số PPA (OpenLane 2 / SkyWater 130nm)", 11,'
    )

    # s26 (ASIC STA): 12
    code_new = code_new.replace(
        '"Phân Tích Định Thời Tĩnh STA & Báo Cáo Multi-Corner Timing (summary.rpt)", 11,',
        '"Phân Tích Định Thời Tĩnh STA & Báo Cáo Multi-Corner Timing (summary.rpt)", 12,'
    )

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(code_new)

    print("Reordered Host Console slide to Slide 5 successfully!")

if __name__ == "__main__":
    reorder_host_console()
