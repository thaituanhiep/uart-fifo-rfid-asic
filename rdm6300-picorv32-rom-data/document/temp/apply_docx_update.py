# -*- coding: utf-8 -*-
import os
import re

with open("generate_report_docx.py", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update TOC items and TOC rendering
old_toc_start = """    toc_items = [
        ("1. Giới thiệu dự án: Thiết bị kiểm soát ra vào độc lập (offline)", "3", True, 0),"""

new_toc = """    toc_items = [
        ("1. Giới thiệu dự án: Thiết bị kiểm soát ra vào độc lập (offline)", "3", True, 0),
        ("1.1. Bối cảnh công nghệ và tính cấp thiết", "3", False, 0.2),
        ("1.2. Định hướng sản phẩm: Thiết bị kiểm soát ra vào độc lập (offline)", "3", False, 0.2),
        ("1.3. Lý do lựa chọn bộ nhớ bất biến non-volatile SPI Flash", "3", False, 0.2),
        ("1.4. Mục tiêu nghiên cứu và phương pháp tiếp cận", "4", False, 0.2),
        ("2. Lựa chọn phần cứng: Bo mạch FPGA Basys 3 và Module RFID RDM6300", "4", True, 0),
        ("2.1. Module đầu đọc thẻ RFID 125 kHz RDM6300", "4", False, 0.2),
        ("2.2. Bo mạch FPGA Digilent Basys 3 (Xilinx Artix-7 XC7A35T)", "4", False, 0.2),
        ("3. Lựa chọn phần mềm và Chuỗi công cụ phát triển", "5", True, 0),
        ("3.1. Chuỗi công cụ FPGA và mô phỏng: AMD Xilinx Vivado Design Suite", "5", False, 0.2),
        ("3.2. Chuỗi công cụ thiết kế vi mạch ASIC: OpenLane 2 & SkyWater 130nm PDK", "5", False, 0.2),
        ("3.3. Chuỗi công cụ phần mềm nhúng RISC-V GCC và Host Console C", "6", False, 0.2),
        ("4. Sơ đồ khối kiến trúc vi hệ thống SoC PicoRV32 (Block Diagram)", "6", True, 0),
        ("4.1. Tổng quan cấu trúc kiến trúc vi hệ thống SoC", "6", False, 0.2),
        ("4.2. Phân tích chi tiết các khối chức năng cốt lõi (Hình 1)", "6", False, 0.2),
        ("5. Khối liên kết bus soc_interconnect.v - Cầu nối CPU, Flash XIP, SRAM và Cơ chế chạy Firmware C", "7", True, 0),
        ("5.1. Kiến trúc kết nối bus và logic giải mã địa chỉ của soc_interconnect.v", "7", False, 0.2),
        ("5.2. Phân tích sơ đồ kiến trúc Draw.io bộ ghép bus trung tâm (Hình 2)", "8", False, 0.2),
        ("5.3. Bảng phân bổ không gian địa chỉ Memory-Mapped I/O (MMIO)", "9", False, 0.2),
        ("6. Mô tả từng module code chính của Firmware C và Ánh xạ địa chỉ MMIO", "10", True, 0),
        ("6.1. Cầu nối phần cứng - phần mềm: Khai báo địa chỉ MMIO trong soc_regs.h vs soc_interconnect.v", "10", False, 0.2),
        ("6.2. Bảng phân tích chu kỳ bus thực tế: Đối chiếu setting RTL, code C và ý nghĩa biến địa chỉ", "11", False, 0.2),
        ("6.2.1. Chu kỳ T=0: Khởi động Reset & Nạp thực thi trực tiếp từ Flash XIP (0x0025_0000)", "12", False, 0.3),
        ("6.2.2. Chu kỳ T=1..100: Thiết lập con trỏ Stack Pointer & Cấp phát SRAM (0x0000_0000 - 0x0000_03FF)", "13", False, 0.3),
        ("6.2.3. Chu kỳ T=101: Chuyển giao điều khiển và Thực thi vòng lặp chính hàm main() C", "14", False, 0.3),
        ("6.2.4. Chu kỳ T=105: Cấu hình tần số Baud Rate 9600 bps cho ngoại vi RFID UART (0x1000_0000)", "15", False, 0.3),
        ("6.2.5. Chu kỳ T=200: Đọc không khóa gói tin thẻ RFID từ Hardware FIFO (0x1000_0004)", "16", False, 0.3),
        ("6.2.6. Chu kỳ T=250: Giao tiếp hai chiều Host PC UART truyền nhận qua Hardware FIFO (0x3000_0004)", "17", False, 0.3),
        ("6.2.7. Chu kỳ T=300: Điều khiển chốt khóa cửa điện từ và hệ thống LED trạng thái qua GPIO (0x4000_0000)", "18", False, 0.3),
        ("6.2.8. Chu kỳ T=400: Thực thi hàm ghi xóa Flash trực tiếp từ SRAM qua chế độ bit-bang SPI (0x0200_0000)", "19", False, 0.3),
        ("6.3. Module driver flash.h và Cơ chế điều khiển SPI Flash (Đối chiếu C và RTL)", "20", False, 0.2),
        ("6.4. Module driver uart.h và Điều khiển ngoại vi FIFO UART / GPIO (Đối chiếu C và RTL)", "21", False, 0.2),
        ("6.5. Module giải mã giao thức thẻ RFID rdm6300_parser.h", "22", False, 0.2),
        ("6.6. Module nghiệp vụ kiểm soát ra vào access_control.h và Vòng lặp main.c", "23", False, 0.2),
        ("6.7. Luồng nghiệp vụ cốt lõi 1: Thu nhận, giải mã và xác thực thẻ RFID 6 bước", "23", False, 0.2),
        ("6.8. Luồng nghiệp vụ cốt lõi 2: Quy trình thực thi 11 chức năng điều khiển Host UART", "24", False, 0.2),
        ("7. Hệ thống kiểm thử mô phỏng Testbench", "25", True, 0),
        ("7.1. Tổng quan hệ thống kiểm thử tinh gọn trong thư mục tb/", "25", False, 0.2),
        ("7.2. Testbench 1: Kiểm thử RTL thuần cấp module cho UART MMIO & FIFO (tb_uart_rtl.v)", "25", False, 0.2),
        ("7.3. Testbench 2: Kiểm thử tích hợp toàn diện Top SoC Boot Flash & Ping (tb_uart_ping.v)", "26", False, 0.2),
        ("7.4. Hướng dẫn chạy mô phỏng 1-click trên Vivado Simulator (xsim)", "26", False, 0.2),
        ("8. Demo chức năng sản phẩm và Kiểm chứng thực nghiệm trên FPGA Basys 3", "27", True, 0),
        ("8.1. Vai trò của bo mạch FPGA Basys 3 và thiết lập kết nối phần cứng", "27", False, 0.2),
        ("8.2. Các kịch bản thực nghiệm quẹt thẻ thực tế và kết quả xác thực", "27", False, 0.2),
        ("9. Thiết kế vật lý vi mạch và Kết quả ký duyệt ASIC (OpenLane 2 - SkyWater Sky130A)", "29", True, 0),
        ("9.1. Phân tích thiết lập cấu hình vật lý trong config.json", "29", False, 0.2),
        ("9.2. Trực quan hóa layout vật lý trên công cụ OpenROAD (Hình 3)", "30", False, 0.2),
        ("9.3. Báo cáo ký duyệt chế tạo sign-off toàn diện (Hình 4)", "31", False, 0.2),
        ("9.4. Đánh giá phân tích định thời tĩnh STA đa góc đo (9 corners) và MET TIMING", "32", False, 0.2),
        ("9.5. Phân tích lưới nguồn PDN và kiểm tra sụt áp (IR drop analysis)", "32", False, 0.2),
        ("10. Kết luận và Hướng phát triển", "33", True, 0),
    ]"""

# Match the old toc_items block
toc_pattern = re.compile(r'    toc_items = \[\n.*?    \]', re.DOTALL)
text = toc_pattern.sub(new_toc, text, count=1)

# Also tighten TOC paragraph spacing so 43 items fit on 1 page:
old_toc_render = """    for title, pg, is_main, indent in toc_items:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(1.5)
        p_t.paragraph_format.space_after = Pt(2.0)
        p_t.paragraph_format.line_spacing = 1.12
        if indent > 0:
            p_t.paragraph_format.left_indent = Inches(indent)
            
        p_t.paragraph_format.tab_stops.add_tab_stop(Inches(6.20), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        
        r1 = p_t.add_run(title)
        set_font(r1, size=10 if not is_main else 10.5, bold=is_main, color=BLACK)
        
        r2 = p_t.add_run(f"\\t{pg}")
        set_font(r2, size=10 if not is_main else 10.5, bold=is_main, color=BLACK)"""

new_toc_render = """    for title, pg, is_main, indent in toc_items:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(1.0)
        p_t.paragraph_format.space_after = Pt(1.2)
        p_t.paragraph_format.line_spacing = 1.05
        if indent > 0:
            p_t.paragraph_format.left_indent = Inches(indent)
            
        p_t.paragraph_format.tab_stops.add_tab_stop(Inches(6.20), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        
        r1 = p_t.add_run(title)
        set_font(r1, size=8.5 if not is_main else 9.0, bold=is_main, color=BLACK)
        
        r2 = p_t.add_run(f"\\t{pg}")
        set_font(r2, size=8.5 if not is_main else 9.0, bold=is_main, color=BLACK)"""

text = text.replace(old_toc_render, new_toc_render)

# 2. Add 8 dedicated pages under Section 6.2
target_insertion_anchor = """    col_w2 = [Inches(1.85), Inches(4.80)]
    col_a2 = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    style_table(t2, col_w2, col_a2, font_size=10.0)
    add_caption("Bảng 2. Bảng phân tích chu kỳ bus thực tế: Đối chiếu thiết lập giải mã RTL, định nghĩa code C và ý nghĩa biến địa chỉ")"""

eight_dedicated_pages_code = '''    col_w2 = [Inches(1.85), Inches(4.80)]
    col_a2 = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    style_table(t2, col_w2, col_a2, font_size=10.0)
    add_caption("Bảng 2. Bảng phân tích chu kỳ bus thực tế: Đối chiếu thiết lập giải mã RTL, định nghĩa code C và ý nghĩa biến địa chỉ")

    # Helper: Xuất 1 trang DOCX chuyên biệt cho từng trường hợp chu kỳ Bus (Dedicated 1 Page per Row)
    def add_case_dedicated_page(case_num, time_tag, task_name, addr_info, bus_sig,
                                rtl_file, rtl_lines,
                                c_file, c_lines,
                                why_p1, why_p2):
        doc.add_page_break()
        add_h2(f"6.2.{case_num}. Chu kỳ {time_tag} ({task_name}) - Chi tiết ánh xạ biến địa chỉ {addr_info}")
        
        add_p(f"Phần này cung cấp phân tích chi tiết và đối chiếu mã nguồn thực tế cho Trường hợp {case_num}: thời điểm {time_tag}, thực hiện tác vụ {task_name}, truy xuất không gian địa chỉ {addr_info} với tín hiệu điều khiển bus kích hoạt {bus_sig}.")
        
        # Bảng tóm tắt thông số kỹ thuật 2 cột
        t_param = doc.add_table(rows=5, cols=2)
        params = [
            ("Thời điểm & Chức năng hệ thống", f"{time_tag} - {task_name}"),
            ("Không gian địa chỉ truy xuất", addr_info),
            ("Tín hiệu giải mã Bus Interconnect", bus_sig),
            ("Vị trí mã nguồn phần cứng RTL", rtl_file),
            ("Vị trí mã nguồn Firmware C / Linker", c_file)
        ]
        for row_i, (k_txt, v_txt) in enumerate(params):
            c0 = t_param.cell(row_i, 0)
            c1 = t_param.cell(row_i, 1)
            p0 = c0.paragraphs[0]
            r0 = p0.add_run(k_txt)
            set_font(r0, size=9.0, bold=True, color=BLACK)
            p1 = c1.paragraphs[0]
            r1 = p1.add_run(v_txt)
            set_font(r1, size=9.0, color=BLACK)
            
        style_table(t_param, [Inches(2.2), Inches(4.3)], [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT], font_size=9.0)
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(2)
        p_sp.paragraph_format.space_after = Pt(2)
        
        p_lbl1 = add_p("• Mã nguồn giải mã phần cứng RTL tương ứng:")
        p_lbl1.runs[0].bold = True
        add_console_block(rtl_lines)
        
        p_lbl2 = add_p("• Mã nguồn Firmware C / Linker thao tác trực tiếp trên biến địa chỉ:")
        p_lbl2.runs[0].bold = True
        add_console_block(c_lines)
        
        p_lbl3 = add_p("• Phân tích đồng thiết kế Phần cứng - Phần mềm (Co-Design Analysis):")
        p_lbl3.runs[0].bold = True
        add_p(why_p1)
        add_p(why_p2)

    # -------------------------------------------------------------
    # CASE 1/8: T = 0 (Boot Flash XIP)
    # -------------------------------------------------------------
    add_case_dedicated_page(
        case_num=1,
        time_tag="T = 0",
        task_name="Boot Flash XIP",
        addr_info="0x0025_0000 (Origin Flash XIP)",
        bus_sig="sel_spimem = 1",
        rtl_file="rtl/rdm6300_picorv32_soc.v & rtl/core/soc_interconnect.v",
        rtl_lines=[
            "// rtl/rdm6300_picorv32_soc.v - Cấu hình Vector Reset CPU",
            "parameter [31:0] PROGADDR_RESET = 32'h 0025_0000;",
            "",
            "// rtl/core/soc_interconnect.v - Giải mã địa chỉ Flash SPI XIP",
            "assign sel_spimem = cpu_mem_valid &&",
            "       (cpu_mem_addr >= 32'h0010_0000 && cpu_mem_addr < 32'h0100_0000);",
            "assign spimem_addr = cpu_mem_addr;"
        ],
        c_file="firmware/boot/sections.lds & firmware/boot/start.s",
        c_lines=[
            "/* firmware/boot/sections.lds - Định vị vùng nhớ Flash */",
            "MEMORY {",
            "    FLASH (rx)  : ORIGIN = 0x00250000, LENGTH = 0x400000 /* 4MB Flash */",
            "    RAM   (rwx) : ORIGIN = 0x00000000, LENGTH = 0x000400 /* 1KB SRAM */",
            "}",
            "SECTIONS {",
            "    .text : {",
            "        *(.text.start) /* Điểm khởi đầu mã máy */",
            "        *(.text*)",
            "    } > FLASH",
            "}",
            "",
            "/* firmware/boot/start.s - Opcode đầu tiên CPU nạp tại 0x00250000 */",
            ".section .text.start",
            ".global _start",
            "_start:",
            "    lui sp, %hi(_stack_top)       # Nạp con trỏ ngăn xếp đỉnh SRAM",
            "    addi sp, sp, %lo(_stack_top)  # sp = 0x00000400"
        ],
        why_p1="Khi tín hiệu reset nhả về 0, thanh ghi PC của nhân vi xử lý PicoRV32 lập tức nạp giá trị hằng số PROGADDR_RESET = 32'h0025_0000. CPU phát chu kỳ bus đầu tiên với cpu_mem_valid = 1 và địa chỉ 0x0025_0000. Bộ ghép bus trung tâm soc_interconnect so khớp địa chỉ nằm trong dải [0x0010_0000, 0x0100_0000), lập tức kéo tích cực tín hiệu sel_spimem = 1 để kích hoạt bộ điều khiển spimemio.",
        why_p2="Ý nghĩa đồng thiết kế: Cơ chế Execute-in-Place (XIP) cho phép CPU đọc và giải mã opcode trực tiếp từ chip nhớ ngoài SPI Flash thông qua lệnh đọc nhanh Fast Read (0x0B). Thiết kế này loại bỏ hoàn toàn nhu cầu về bộ nhớ ROM nạp khởi động trung gian (bootloader ROM) tốn kém diện tích trên vi mạch ASIC, đồng thời giải phóng trọn vẹn 100% dung lượng 1KB SRAM nội bộ để dành riêng cho biến động và ngăn xếp ứng dụng C."
    )

    # -------------------------------------------------------------
    # CASE 2/8: T = 1..100 (Tạo Stack Pointer & Zero BSS)
    # -------------------------------------------------------------
    add_case_dedicated_page(
        case_num=2,
        time_tag="T = 1..100",
        task_name="Tạo Stack RAM & Zero BSS",
        addr_info="0x0000_0000 - 0x0000_03FF (1024 Bytes SRAM)",
        bus_sig="sel_sram = 1",
        rtl_file="rtl/core/soc_interconnect.v & rtl/core/data_sram.v",
        rtl_lines=[
            "// rtl/core/soc_interconnect.v - Giải mã dải địa chỉ 1KB SRAM",
            "assign sel_sram = cpu_mem_valid && (cpu_mem_addr < 32'h0000_0400);",
            "assign sram_addr = cpu_mem_addr[9:2]; // 256 từ x 32-bit",
            "assign sram_wdata = cpu_mem_wdata;",
            "assign sram_wstrb = cpu_mem_wstrb;",
            "assign sram_ready = 1'b1;             // Phản hồi zero-wait-state"
        ],
        c_file="firmware/boot/start.s (Assembly)",
        c_lines=[
            "/* firmware/boot/start.s - Khởi tạo Stack Pointer & Sao chép dữ liệu */",
            "    lui sp, %hi(_stack_top)",
            "    addi sp, sp, %lo(_stack_top)   # sp = 0x00000400",
            "",
            "/* Sao chép dữ liệu khởi tạo .data từ Flash vào SRAM */",
            "copy_data:",
            "    la a0, _sdata                  # Đích: SRAM 0x00000000",
            "    la a1, _edata",
            "    la a2, _sidata                 # Nguồn: Flash XIP",
            "copy_loop:",
            "    beq a0, a1, zero_bss",
            "    lw t0, 0(a2)                   # Đọc từ Flash",
            "    sw t0, 0(a0)                   # Ghi vào SRAM",
            "    addi a0, a0, 4",
            "    addi a2, a2, 4",
            "    j copy_loop",
            "",
            "/* Xóa trắng vùng biến toàn cục không khởi tạo .bss về 0 */",
            "zero_bss:",
            "    la a0, _sbss",
            "    la a1, _ebss",
            "zero_loop:",
            "    beq a0, a1, call_main",
            "    sw zero, 0(a0)",
            "    addi a0, a0, 4",
            "    j zero_loop"
        ],
        why_p1="Khối data_sram nội bộ được thiết kế dưới dạng bộ nhớ đồng bộ 1 cổng với 256 từ 32-bit (1024 bytes), phản hồi tức thì với độ trễ đúng 1 chu kỳ clock (sram_ready = 1). Khi CPU thực thi lệnh lui sp, 0x00000400, con trỏ ngăn xếp sp được định vị tại ranh giới cao nhất của SRAM. Khi các hàm C được gọi, sp giảm dần để cấp phát stack frame cho biến cục bộ và thanh ghi ra.",
        why_p2="Ý nghĩa đồng thiết kế: Quá trình copy .data và zero .bss trong start.s chuẩn bị sẵn sàng môi trường runtime chuẩn ngôn ngữ C. Việc phân chia tách biệt vật lý giữa không gian mã lệnh (Flash XIP dải cao) và không gian dữ liệu động (SRAM dải thấp < 0x0400) đảm bảo tính toàn vẹn hệ thống tuyệt đối: mã lệnh không bao giờ bị ghi đè bởi tràn ngăn xếp, và tốc độ truy xuất stack đạt tối đa với độ trễ 0 chu kỳ chờ (zero wait-states)."
    )

    # -------------------------------------------------------------
    # CASE 3/8: T = 101 (Vào hàm main C)
    # -------------------------------------------------------------
    add_case_dedicated_page(
        case_num=3,
        time_tag="T = 101",
        task_name="Vào hàm main() C",
        addr_info="0x0025_0000+ (Vùng mã thực thi Flash C)",
        bus_sig="sel_spimem = 1",
        rtl_file="rtl/core/soc_interconnect.v",
        rtl_lines=[
            "// rtl/core/soc_interconnect.v - Kênh giải mã dòng lệnh thực thi",
            "assign sel_spimem = cpu_mem_valid &&",
            "       (cpu_mem_addr >= 32'h0010_0000 && cpu_mem_addr < 32'h0100_0000);",
            "assign cpu_mem_rdata = sel_spimem ? spimem_rdata : ...;",
            "assign cpu_mem_ready = sel_spimem ? spimem_ready : ...;"
        ],
        c_file="firmware/boot/start.s & firmware/main.c (C)",
        c_lines=[
            "/* firmware/boot/start.s - Lệnh gọi hàm C */",
            "call_main:",
            "    call main       # Nhảy từ Assembly khởi động sang hàm main() C",
            "hang:",
            "    j hang          # Vòng lặp bẫy an toàn nếu main() kết thúc",
            "",
            "/* firmware/main.c - Logic trung tâm của ứng dụng C */",
            "int main(void) {",
            "    system_init();",
            "    access_control_init();",
            "    uart_puts(\\"\\\\n[SYSTEM] PicoRV32 RFID Access Control Ready.\\\\n\\");",
            "    while (1) {",
            "        access_control_poll();   // Polling kiểm tra thẻ RFID",
            "        process_host_commands(); // Xử lý các lệnh quản trị Host PC",
            "    }",
            "    return 0;",
            "}"
        ],
        why_p1="Lệnh call main trong Assembly chuyển giao toàn bộ quyền điều khiển từ chuỗi khởi động sang hàm main() bằng ngôn ngữ C. Hàm main() được biên dịch và định vị hoàn toàn trong vùng Flash XIP (> 0x0025_0000). Dòng opcode được bộ điều khiển spimemio nạp liên tục qua bus SPI ngoại vi, trong khi các biến điều khiển vòng lặp và địa chỉ quay về hàm được quản lý tức thời trên ngăn xếp SRAM.",
        why_p2="Ý nghĩa đồng thiết kế: Hệ thống vận hành trong môi trường C Freestanding hoàn chỉnh không phụ thuộc vào hệ điều hành. Toàn bộ logic nghiệp vụ kiểm soát ra vào, máy trạng thái giải mã thẻ RFID và bộ xử lý 11 lệnh Host PC được diễn đạt trực quan, trong sáng bằng mã C chuẩn ANSI, dễ bảo trì và mở rộng tính năng, trong khi phần cứng RISC-V đảm bảo tốc độ phản hồi tính toán thời gian thực."
    )

    # -------------------------------------------------------------
    # CASE 4/8: T = 105 (Set Baud Rate 9600)
    # -------------------------------------------------------------
    add_case_dedicated_page(
        case_num=4,
        time_tag="T = 105",
        task_name="Set Baud Rate 9600 bps",
        addr_info="0x1000_0000 (RFID DIV) & 0x3000_0000 (Host DIV)",
        bus_sig="sel_rfid = 1 / sel_uart = 1",
        rtl_file="rtl/core/soc_interconnect.v & rtl/peripheral/uart_mmio.v",
        rtl_lines=[
            "// rtl/core/soc_interconnect.v - Giải mã thanh ghi chia baud UART",
            "assign sel_rfid = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h1);",
            "assign sel_uart = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h3);",
            "",
            "// rtl/peripheral/uart_mmio.v - Nạp ước số chia tần số baud rate",
            "always @(posedge clk or posedge reset) begin",
            "    if (reset) uart_div <= 32'd0;",
            "    else if (reg_div_sel && |cpu_mem_wstrb) uart_div <= cpu_mem_wdata;",
            "end"
        ],
        c_file="firmware/common/soc_regs.h & firmware/app/access_control.c",
        c_lines=[
            "/* firmware/common/soc_regs.h - Định nghĩa con trỏ thanh ghi MMIO */",
            "#define REG_RFID_UART_DIV  (*(volatile uint32_t*)0x10000000)",
            "#define REG_PC_UART_DIV    (*(volatile uint32_t*)0x30000000)",
            "",
            "/* firmware/app/access_control.c - Thiết lập cấu hình tốc độ truyền */",
            "void access_control_init(void) {",
            "    // 50,000,000 Hz / 9600 bps = 5208 (0x1458)",
            "    REG_RFID_UART_DIV = 5208; // Cấu hình UART đọc thẻ RDM6300",
            "    REG_PC_UART_DIV   = 5208; // Cấu hình UART giao tiếp Host PC",
            "    rdm6300_init(&parser);",
            "    whitelist_init();",
            "}"
        ],
        why_p1="Địa chỉ 0x1000_0000 được soc_interconnect nhận diện thông qua 4 bit cao addr[31:28] == 4'h1 và bit addr[2] == 0 trỏ vào thanh ghi ước số chia tần uart_div. Lệnh gán REG_RFID_UART_DIV = 5208 phát lệnh ghi sw với cpu_mem_wstrb = 4'b1111, nạp giá trị 5208 vào bộ đếm phần cứng. Từ khóa volatile bắt buộc trình biên dịch phát chu kỳ bus vật lý ra địa chỉ MMIO mà không bị tối ưu hóa bỏ qua.",
        why_p2="Ý nghĩa đồng thiết kế: Với xung nhịp hệ thống 50 MHz, ước số chia baud 5208 mang lại tốc độ truyền chính xác 9600 bps với sai số tần số lý thuyết cực thấp chỉ 0.006%, triệt tiêu hoàn toàn sai lệch định thời bit (bit timing jitter) khi nhận chuỗi ký tự nối tiếp chuẩn 8N1 từ module cảm biến RFID RDM6300 và cổng máy tính USB-UART."
    )

    # -------------------------------------------------------------
    # CASE 5/8: T = 200 (Đọc thẻ RFID qua FIFO Non-blocking)
    # -------------------------------------------------------------
    add_case_dedicated_page(
        case_num=5,
        time_tag="T = 200",
        task_name="Đọc thẻ RFID FIFO Non-blocking",
        addr_info="0x1000_0004 (RFID UART DAT)",
        bus_sig="sel_rfid = 1",
        rtl_file="rtl/peripheral/uart_mmio.v",
        rtl_lines=[
            "// rtl/peripheral/uart_mmio.v - Logic đọc rút tự động không khóa",
            "assign rfid_rdata = (rfid_fifo_empty) ? 32'hFFFF_FFFF",
            "                                      : {24'h0, rfid_rx_fifo_dout};",
            "assign rfid_rx_fifo_pop = sel_rfid && cpu_mem_valid &&",
            "                          (cpu_mem_addr[2] == 1'b1) && !cpu_mem_wstrb;"
        ],
        c_file="firmware/common/soc_regs.h & firmware/app/access_control.c",
        c_lines=[
            "/* firmware/common/soc_regs.h */",
            "#define REG_RFID_UART_DAT  (*(volatile uint32_t*)0x10000004)",
            "",
            "/* firmware/app/access_control.c - Đọc không khóa gói tin thẻ RFID */",
            "static inline int rfid_uart_getc_nonblock(void) {",
            "    uint32_t val = REG_RFID_UART_DAT;",
            "    if (val == 0xFFFFFFFF) {",
            "        return -1; // FIFO phần cứng đang rỗng, không có dữ liệu mới",
            "    }",
            "    return (int)(val & 0xFF); // Trả về byte mã thẻ 8-bit từ RDM6300",
            "}",
            "",
            "void access_control_poll(void) {",
            "    int c = rfid_uart_getc_nonblock();",
            "    if (c >= 0) {",
            "        rdm6300_parse_byte(&parser, (uint8_t)c); // Nạp vào parser 6 bước",
            "    }",
            "}"
        ],
        why_p1="Địa chỉ 0x1000_0004 có addr[2] == 1, trỏ vào thanh ghi dữ liệu của cổng RFID UART. Phần cứng RTL thực hiện cơ chế tự động: mỗi khi CPU đọc thanh ghi này, nếu FIFO có dữ liệu, mạch phát xung pop rút 1 byte chuyển sang CPU trong 1 chu kỳ clock. Nếu FIFO đang rỗng, mạch trả về giá trị đặc biệt 0xFFFFFFFF mà không làm dừng CPU.",
        why_p2="Ý nghĩa đồng thiết kế: Mô hình đọc không chặn (Non-blocking Pop) kết hợp hàng đợi FIFO 32 byte bằng phần cứng giải phóng hoàn toàn CPU khỏi việc chờ đợi ngoại vi UART chậm chạp. CPU chỉ mất đúng 1 chu kỳ bus để kiểm tra trạng thái dữ liệu. Khi module RDM6300 phát gói tin 14 byte với tốc độ 9600 bps, FIFO phần cứng hứng trọn vẹn toàn bộ chuỗi byte, loại bỏ hoàn toàn nguy cơ tràn đệm (overflow) hay mất mát dữ liệu thẻ."
    )

    # -------------------------------------------------------------
    # CASE 6/8: T = 250 (Giao tiếp Host PC UART qua FIFO)
    # -------------------------------------------------------------
    add_case_dedicated_page(
        case_num=6,
        time_tag="T = 250",
        task_name="Giao tiếp Host PC UART FIFO",
        addr_info="0x3000_0004 (PC UART DAT) & 0x3000_0000 (PC UART DIV)",
        bus_sig="sel_uart = 1",
        rtl_file="rtl/core/soc_interconnect.v & rtl/peripheral/uart_mmio.v",
        rtl_lines=[
            "// rtl/core/soc_interconnect.v",
            "assign sel_uart = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h3);",
            "",
            "// rtl/peripheral/uart_mmio.v - Điều khiển TX FIFO và RX FIFO Host",
            "assign host_tx_fifo_push = sel_uart && cpu_mem_valid &&",
            "                           (cpu_mem_addr[2] == 1'b1) && |cpu_mem_wstrb;",
            "assign host_rdata = (host_rx_fifo_empty) ? 32'hFFFF_FFFF",
            "                                         : {24'h0, host_rx_fifo_dout};",
            "assign host_rx_fifo_pop = sel_uart && cpu_mem_valid &&",
            "                          (cpu_mem_addr[2] == 1'b1) && !cpu_mem_wstrb;"
        ],
        c_file="firmware/common/soc_regs.h & firmware/drivers/uart.c",
        c_lines=[
            "/* firmware/common/soc_regs.h */",
            "#define REG_PC_UART_DAT    (*(volatile uint32_t*)0x30000004)",
            "",
            "/* firmware/drivers/uart.c - Truyền và nhận dữ liệu máy tính */",
            "void uart_putc(char c) {",
            "    REG_PC_UART_DAT = (uint32_t)(uint8_t)c; // Đẩy ký tự vào TX FIFO phần cứng",
            "}",
            "",
            "void uart_puts(const char *str) {",
            "    while (*str) {",
            "        uart_putc(*str++); // Ghi liên tiếp với độ trễ 1 chu kỳ clock",
            "    }",
            "}",
            "",
            "int uart_getc_nonblock(void) {",
            "    uint32_t val = REG_PC_UART_DAT;",
            "    if (val == 0xFFFFFFFF) return -1;",
            "    return (int)(val & 0xFF);",
            "}"
        ],
        why_p1="Ngoại vi Host PC UART sử dụng 2 bộ đệm FIFO 32 byte độc lập: 1 cho chiều truyền (TX) và 1 cho chiều nhận (RX). Khi firmware C gọi hàm uart_puts(\\"ACCESS:GRANTED\\\\n\\"), CPU ghi liên tiếp các ký tự vào địa chỉ 0x3000_0004. Mỗi lệnh sw chỉ tiêu tốn 1 chu kỳ bus (20 ns). Ký tự được nạp tức thời vào TX FIFO, và khối phát phần cứng tự động dịch nối tiếp từng bit ra chân TXD mà CPU không cần phải chờ đợi 1.04 ms mỗi ký tự.",
        why_p2="Ý nghĩa đồng thiết kế: Tách rời hoàn toàn tốc độ xử lý 50 MHz của nhân vi xử lý RISC-V khỏi tốc độ truyền thông nối tiếp 9600 bps. Nhờ đó, việc gửi thông báo kết quả quẹt thẻ và nhật ký kiểm toán lên máy tính diễn ra trơn tru mà không làm gián đoạn chu kỳ lấy mẫu RFID thời gian thực hay làm trễ thời gian đóng/mở chốt cửa an ninh."
    )

    # -------------------------------------------------------------
    # CASE 7/8: T = 300 (Điều khiển GPIO Relay & LED)
    # -------------------------------------------------------------
    add_case_dedicated_page(
        case_num=7,
        time_tag="T = 300",
        task_name="Bật LED / Mở Cửa GPIO",
        addr_info="0x4000_0000 (GPIO LEDS & Relays)",
        bus_sig="sel_gpio = 1",
        rtl_file="rtl/core/soc_interconnect.v",
        rtl_lines=[
            "// rtl/core/soc_interconnect.v - Giải mã và chốt ngõ ra GPIO 16-bit",
            "assign sel_gpio = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h4);",
            "always @(posedge clk or posedge reset) begin",
            "    if (reset)",
            "        gpio_reg <= 16'h0000;",
            "    else if (sel_gpio && |cpu_mem_wstrb)",
            "        gpio_reg <= cpu_mem_wdata[15:0]; // Chốt mức logic tức thì",
            "end",
            "assign gpio_leds = gpio_reg;"
        ],
        c_file="firmware/common/soc_regs.h & firmware/app/access_control.c",
        c_lines=[
            "/* firmware/common/soc_regs.h */",
            "#define REG_GPIO_LEDS      (*(volatile uint32_t*)0x40000000)",
            "",
            "/* firmware/app/access_control.c - Kích hoạt cơ cấu chấp hành */",
            "void handle_access_granted(uint32_t tag_id) {",
            "    // Bit 2 = 1 (0x0004): Kích hoạt Relay chốt mở cửa điện từ",
            "    REG_GPIO_LEDS |= 0x0004;",
            "    uart_puts(\\"[AUTH] ACCESS GRANTED. Door unlocked!\\\\n\\");",
            "}",
            "",
            "void handle_access_denied(uint32_t tag_id) {",
            "    // Bit 1 = 1 (0x0002): Bật LED đỏ báo động từ chối truy cập",
            "    REG_GPIO_LEDS |= 0x0002;",
            "    uart_puts(\\"[AUTH] ACCESS DENIED. Unauthorized card!\\\\n\\");",
            "}"
        ],
        why_p1="Địa chỉ 0x4000_0000 được định vị tại không gian MMIO thứ 4 (addr[31:28] == 4'h4). Thanh ghi gpio_reg 16-bit được nối trực tiếp ra các chân output pad vật lý của chip vi mạch ASIC: Bit 0 (0x0001) điều khiển LED nhịp tim Alive (nhấp nháy chu kỳ 1s), Bit 1 (0x0002) điều khiển LED đỏ cảnh báo Access Denied, và Bit 2 (0x0004) xuất tín hiệu kích hoạt mạch cuộn hút Relay khóa cửa điện từ (Access Granted).",
        why_p2="Ý nghĩa đồng thiết kế: Việc chốt trạng thái phần cứng diễn ra tức thời trong đúng 1 chu kỳ xung nhịp 20 ns khi CPU phát lệnh sw. Thiết kế phản hồi không độ trễ (zero-latency actuation) đem lại trải nghiệm mở cửa mượt mà, tức thời cho người sử dụng ngay sau khi quẹt thẻ, đồng thời đảm bảo an toàn vật lý cao nhất trong các tình huống khẩn cấp."
    )

    # -------------------------------------------------------------
    # CASE 8/8: T = 400 (Ghi Flash từ RAM qua Bit-bang SPI)
    # -------------------------------------------------------------
    add_case_dedicated_page(
        case_num=8,
        time_tag="T = 400",
        task_name="Ghi Flash từ RAM (Bit-bang SPI)",
        addr_info="0x0200_0000 (SPI Bit-Bang Register)",
        bus_sig="sel_spicfg = 1",
        rtl_file="rtl/core/soc_interconnect.v & rtl/core/spimemio.v",
        rtl_lines=[
            "// rtl/core/soc_interconnect.v - Giải mã thanh ghi cấu hình SPI Bit-Bang",
            "assign sel_spicfg = cpu_mem_valid && (cpu_mem_addr == 32'h0200_0000);",
            "",
            "// Khi sel_spicfg tích cực, spimemio ngắt chế độ XIP đọc tự động",
            "// và chuyển quyền điều khiển chân SPI sang thanh ghi bit-bang trực tiếp"
        ],
        c_file="firmware/boot/start.s & firmware/drivers/flash.c",
        c_lines=[
            "/* firmware/boot/start.s - Hàm thao tác SPI nạp trong SRAM */",
            ".section .data",
            ".global flashio_worker",
            "flashio_worker:",
            "    /* Hàm chạy trực tiếp từ SRAM (0x0000xxxx) để tránh xung đột bus XIP */",
            "    li t0, 0x02000000        # Địa chỉ thanh ghi điều khiển Bit-Bang SPI",
            "    sw a0, 0(t0)             # Gửi byte lệnh ghi / xóa sector (CS_N, CLK, MOSI)",
            "    lw a1, 0(t0)             # Đọc dữ liệu phản hồi từ Flash MISO",
            "    ret",
            "",
            "/* firmware/drivers/flash.c - Driver ghi dữ liệu bền vững */",
            "void flash_write_whitelist(uint32_t tag_id) {",
            "    // Gọi hàm thực thi từ SRAM để xóa sector 4KB và ghi thẻ mới vào Flash",
            "    // Đảm bảo CPU không nạp lệnh từ Flash khi Flash đang bận chu kỳ ghi",
            "    flashio(cmd_buffer, len, 0);",
            "}"
        ],
        why_p1="Bản chất vật lý của chip nhớ SPI Flash NOR là trong suốt chu kỳ xóa sector (Sector Erase, mất ~50-200 ms) hoặc nạp trang (Page Program, mất ~1-3 ms), chip Flash hoàn toàn bận (Busy) và từ chối mọi chu kỳ đọc dữ liệu chuẩn. Nếu CPU tiếp tục cố gắng đọc lệnh XIP từ Flash trong thời gian này, đường bus SPI sẽ trả về mã rác hoặc làm CPU bị treo vô hạn (bus lockup).",
        why_p2="Ý nghĩa đồng thiết kế: Đoạn mã con flashio_worker được định vị trong phân vùng .data và sao chép vào SRAM tại thời điểm boot. Khi thực hiện ghi thẻ vào Whitelist hoặc ghi nhật ký quẹt thẻ, CPU chuyển sang thực thi mã trong SRAM, sử dụng địa chỉ 0x0200_0000 để phát lệnh bit-bang SPI trực tiếp điều khiển chip Flash. Giải pháp sáng tạo này giải quyết triệt để bài toán xung đột bus trên các vi hệ thống SoC có kiến trúc Flash XIP đơn kênh, mang lại khả năng lưu trữ bất biến tin cậy tuyệt đối."
    )
'''

text = text.replace(target_insertion_anchor, eight_dedicated_pages_code)

with open("generate_report_docx.py", "w", encoding="utf-8") as f:
    f.write(text)

print("[SUCCESS] Successfully updated generate_report_docx.py with 8 dedicated pages and updated TOC!")
