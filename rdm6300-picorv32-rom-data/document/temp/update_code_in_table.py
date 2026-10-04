# -*- coding: utf-8 -*-
"""
update_code_in_table.py
Updates the 3-column table in both:
1. create_presentation.py (Slide 11: add_bus_table_slide & all_rows_bus)
2. generate_report_docx.py (Section 6.2 Table 2: t2_rows & styling)
Ensuring exact, verbatim RTL and C/Linker code lines are clearly displayed.
"""

import os
import re

cur_dir = os.path.dirname(os.path.abspath(__file__))

# =============================================================================
# 1. UPDATE CREATE_PRESENTATION.PY (SLIDE 11)
# =============================================================================
pres_path = os.path.join(cur_dir, "create_presentation.py")
with open(pres_path, "r", encoding="utf-8") as f:
    pres_code = f.read()

# New definition of all_rows_bus
new_all_rows_bus = '''    all_rows_bus = [
        {
            "time": "T = 0",
            "task": "(Boot Flash XIP)",
            "rtl_file": "[rdm6300_picorv32_soc.v & soc_interconnect.v]",
            "rtl_code": "parameter [31:0] PROGADDR_RESET = 32'h0025_0000;\\nassign sel_spimem = cpu_mem_valid && (cpu_mem_addr >= 32'h0010_0000 && cpu_mem_addr < 32'h0100_0000);",
            "c_file": "[sections.lds & start.s]",
            "c_code": "FLASH (rx) : ORIGIN = 0x00250000, LENGTH = 0x000B0000\\n_start: lui sp, %hi(_stack_top)",
            "meaning": "Cấu hình vector reset trỏ thẳng vào Flash SPI để CPU tự động nạp và thực thi trực tiếp opcode firmware (XIP) ngay sau khi nhả reset mà không cần nạp vào RAM."
        },
        {
            "time": "T = 1..100",
            "task": "(Tạo Stack RAM)",
            "rtl_file": "[rdm6300_picorv32_soc.v & soc_interconnect.v]",
            "rtl_code": "parameter [31:0] STACKADDR = 32'h0000_0400;\\nassign sel_sram = cpu_mem_valid && (cpu_mem_addr < 32'h0000_0400);\\nassign sram_ready = 1'b1;",
            "c_file": "[sections.lds & start.s]",
            "c_code": "RAM (rwx) : ORIGIN = 0x00000000, LENGTH = 0x00000400\\nlui sp, %hi(_stack_top); addi sp, sp, %lo(_stack_top);",
            "meaning": "C sử dụng không gian SRAM 1KB (< 0x0400) qua con trỏ ngăn xếp sp để cấp phát biến cục bộ, lưu stack frame và địa chỉ trả về hàm, phản hồi tức thì trong 1 chu kỳ clock."
        },
        {
            "time": "T = 101",
            "task": "(Vào hàm main)",
            "rtl_file": "[soc_interconnect.v]",
            "rtl_code": "assign sel_spimem = cpu_mem_valid && (cpu_mem_addr >= 32'h0010_0000 && ...);\\nassign cpu_mem_rdata = sel_spimem ? spimem_rdata : sel_sram ? sram_rdata : ...;",
            "c_file": "[start.s & main.c]",
            "c_code": "call main;\\nint main(void) { access_control_init(); while (1) access_control_poll(); }",
            "meaning": "Chuyển giao quyền điều khiển từ assembly khởi động sang code C bậc cao. Hàm main() chạy trực tiếp từ Flash XIP, giải phóng toàn bộ 1KB SRAM chỉ dùng cho dữ liệu động."
        },
        {
            "time": "T = 105",
            "task": "(Set Baud Dual UART)",
            "rtl_file": "[soc_interconnect.v & uart_mmio.v]",
            "rtl_code": "assign sel_rfid = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h1);\\nif (reg_div_sel && |cpu_mem_wstrb) uart_div <= cpu_mem_wdata;",
            "c_file": "[soc_regs.h & access_control.c]",
            "c_code": "#define REG_RFID_UART_DIV (*(volatile uint32_t*)0x10000000)\\nREG_RFID_UART_DIV = 5208; // 50 MHz / 9600 Baud",
            "meaning": "C ghi giá trị chia tần 5208 vào địa chỉ 0x10000000 và 0x30000000 để cài đặt tốc độ baud 9600 bps cho cả đầu đọc RFID RDM6300 và cổng máy tính PC (50 MHz / 9600)."
        },
        {
            "time": "T = 200",
            "task": "(Đọc thẻ RFID)",
            "rtl_file": "[uart_mmio.v & simpleuart_fifo.v]",
            "rtl_code": "wire reg_dat_sel = valid && (addr[2] == 1'b1);\\nassign reg_dat_do = fifo_empty ? 32'hFFFFFFFF : {24'd0, fifo_dout};",
            "c_file": "[soc_regs.h & access_control.c]",
            "c_code": "#define REG_RFID_UART_DAT (*(volatile uint32_t*)0x10000004)\\nuint32_t d = REG_RFID_UART_DAT; if (d != 0xFFFFFFFF) rdm6300_push(d);",
            "meaning": "C đọc từ 0x10000004 rút (pop) 1 byte từ FIFO 32B (đọc không khóa: trả về byte mã thẻ nếu có, hoặc trả về 0xFFFFFFFF nếu FIFO rỗng để CPU không bị nghẽn bus)."
        },
        {
            "time": "T = 250",
            "task": "(Giao tiếp PC UART)",
            "rtl_file": "[soc_interconnect.v & uart_mmio.v]",
            "rtl_code": "assign sel_uart = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h3);\\nwire dat_we = reg_dat_sel && (|wstrb); // Write TX FIFO",
            "c_file": "[soc_regs.h & uart.c]",
            "c_code": "#define REG_PC_UART_DAT (*(volatile uint32_t*)0x30000004)\\nREG_PC_UART_DAT = c; /* Ghi TX */ | d = REG_PC_UART_DAT; /* Doc RX */",
            "meaning": "C ghi byte vào 0x30000004 để đẩy ký tự vào TX FIFO truyền lên Host PC, và đọc từ địa chỉ này để nhận chuỗi lệnh quản trị (Ping, thêm/xóa thẻ Whitelist, xuất log CSV)."
        },
        {
            "time": "T = 300",
            "task": "(Bật LED / Mở Cửa)",
            "rtl_file": "[soc_interconnect.v & soc_gpio_mmio.v]",
            "rtl_code": "assign sel_gpio = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h4);\\nif (sel_gpio && |wstrb) gpio_led_reg[7:0] <= wdata[7:0];",
            "c_file": "[soc_regs.h & access_control.c]",
            "c_code": "#define REG_GPIO_LEDS (*(volatile uint32_t*)0x40000000)\\nREG_GPIO_LEDS = (REG_GPIO_LEDS & ~0x0002) | 0x0004; // Bit 2: Granted",
            "meaning": "C ghi giá trị bitmask vào 0x40000000 điều khiển 16 LED chẩn đoán trên bo mạch và đóng/ngắt relay mở chốt cửa điện từ (Bit 0: Alive 1Hz, Bit 1: Denied, Bit 2: Granted)."
        },
        {
            "time": "T = 400",
            "task": "(Ghi Flash từ RAM)",
            "rtl_file": "[soc_interconnect.v & spimemio.v]",
            "rtl_code": "assign sel_spicfg = cpu_mem_valid && (cpu_mem_addr == 32'h0200_0000);\\n.cfgreg_we(sel_spicfg ? mem_wstrb : 4'b0000), .cfgreg_di(mem_wdata)",
            "c_file": "[start.s & flash.c]",
            "c_code": "flashio_worker: li t0, 0x02000000; sh t1, 0(t0);\\nstatic void flashio(uint8_t *data, int len, uint8_t wrencmd);",
            "meaning": "Khi chạy từ SRAM, hàm của C phát lệnh bit-bang SPI vào 0x02000000 để xóa sector và ghi dữ liệu thẻ mới vào Flash Whitelist / Log mà không gây xung đột bus với các lệnh XIP."
        }
    ]'''

old_all_rows_bus_pattern = re.compile(r'    all_rows_bus = \[.*?\n    \]', re.DOTALL)
if old_all_rows_bus_pattern.search(pres_code):
    pres_code = old_all_rows_bus_pattern.sub(new_all_rows_bus, pres_code, count=1)
    print("[SUCCESS] Replaced all_rows_bus in create_presentation.py")
else:
    print("[ERROR] all_rows_bus not found in create_presentation.py")

# Update add_bus_table_slide formatting for clear code display
new_add_bus_table_func = '''    def add_bus_table_slide(slide_num, title, rows_data):
        slide = prs.slides.add_slide(blank_layout)
        add_header(slide, "Phần 6: Firmware C & Ánh Xạ MMIO", title, slide_num, total_slides=TOTAL_SLIDES)

        x = Inches(0.8)
        y = Inches(1.30)
        w = Inches(11.733)
        h = Inches(5.60)

        num_rows = len(rows_data) + 1
        tbl_shape = slide.shapes.add_table(num_rows, 3, x, y, w, h)
        tbl = tbl_shape.table

        col_w = [Inches(1.65), Inches(5.75), Inches(4.333)]
        for ci, cw in enumerate(col_w):
            tbl.columns[ci].width = cw

        headers = [
            "Trường Hợp / Thời Điểm",
            "Cấu Hình RTL & Mã Lệnh Firmware C",
            "Ý Nghĩa Thao Tác & Cơ Chế Co-Design"
        ]

        for ci, h_text in enumerate(headers):
            cell = tbl.cell(0, ci)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_NAVY_DARK
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.margin_left = Inches(0.10)
            cell.margin_right = Inches(0.10)
            cell.margin_top = Inches(0.05)
            cell.margin_bottom = Inches(0.05)

            p = cell.text_frame.paragraphs[0]
            p.text = h_text
            p.font.name = "Segoe UI"
            p.font.size = Pt(10.5)
            p.font.bold = True
            p.font.color.rgb = C_WHITE
            p.alignment = PP_ALIGN.CENTER if ci == 0 else PP_ALIGN.LEFT

        for ri, r in enumerate(rows_data):
            row_idx = ri + 1
            row_bg = RGBColor(241, 245, 249) if ri % 2 == 0 else RGBColor(255, 255, 255)

            # Cột 0: Trường hợp / Thời điểm
            c0 = tbl.cell(row_idx, 0)
            c0.fill.solid()
            c0.fill.fore_color.rgb = row_bg
            c0.vertical_anchor = MSO_ANCHOR.MIDDLE
            c0.margin_left = Inches(0.05)
            c0.margin_right = Inches(0.05)
            tf0 = c0.text_frame
            tf0.word_wrap = True

            p0_1 = tf0.paragraphs[0]
            p0_1.text = r["time"]
            p0_1.font.name = "Segoe UI"
            p0_1.font.size = Pt(10.5)
            p0_1.font.bold = True
            p0_1.font.color.rgb = C_BLUE_ACCENT
            p0_1.alignment = PP_ALIGN.CENTER

            p0_2 = tf0.add_paragraph()
            p0_2.text = r["task"]
            p0_2.font.name = "Segoe UI"
            p0_2.font.size = Pt(8.5)
            p0_2.font.bold = True
            p0_2.font.color.rgb = C_TEXT_DARK
            p0_2.alignment = PP_ALIGN.CENTER

            # Cột 1: Cấu hình RTL & Code C in rõ ràng
            c1 = tbl.cell(row_idx, 1)
            c1.fill.solid()
            c1.fill.fore_color.rgb = row_bg
            c1.vertical_anchor = MSO_ANCHOR.MIDDLE
            c1.margin_left = Inches(0.08)
            c1.margin_right = Inches(0.08)
            c1.margin_top = Inches(0.02)
            c1.margin_bottom = Inches(0.02)
            tf1 = c1.text_frame
            tf1.word_wrap = True

            # RTL Header & File
            p1 = tf1.paragraphs[0]
            r1_lbl = p1.add_run()
            r1_lbl.text = "• RTL "
            r1_lbl.font.name = "Segoe UI"
            r1_lbl.font.size = Pt(8.0)
            r1_lbl.font.bold = True
            r1_lbl.font.color.rgb = C_BLUE_ACCENT

            r1_file = p1.add_run()
            r1_file.text = r["rtl_file"] + ":\\n"
            r1_file.font.name = "Segoe UI"
            r1_file.font.size = Pt(7.5)
            r1_file.font.bold = True
            r1_file.font.color.rgb = RGBColor(30, 58, 138)

            r1_code = p1.add_run()
            r1_code.text = "  " + r["rtl_code"].replace("\\n", "\\n  ")
            r1_code.font.name = "Consolas"
            r1_code.font.size = Pt(7.3)
            r1_code.font.bold = True
            r1_code.font.color.rgb = RGBColor(15, 23, 42)
            p1.space_after = Pt(2.0)
            p1.line_spacing = 1.05

            # C Header & File
            p2 = tf1.add_paragraph()
            r2_lbl = p2.add_run()
            r2_lbl.text = "• Code C "
            r2_lbl.font.name = "Segoe UI"
            r2_lbl.font.size = Pt(8.0)
            r2_lbl.font.bold = True
            r2_lbl.font.color.rgb = C_GREEN

            r2_file = p2.add_run()
            r2_file.text = r["c_file"] + ":\\n"
            r2_file.font.name = "Segoe UI"
            r2_file.font.size = Pt(7.5)
            r2_file.font.bold = True
            r2_file.font.color.rgb = RGBColor(21, 128, 61)

            r2_code = p2.add_run()
            r2_code.text = "  " + r["c_code"].replace("\\n", "\\n  ")
            r2_code.font.name = "Consolas"
            r2_code.font.size = Pt(7.3)
            r2_code.font.bold = True
            r2_code.font.color.rgb = RGBColor(15, 23, 42)
            p2.line_spacing = 1.05

            # Cột 2: Ý nghĩa thao tác chuyển qua đây
            c2 = tbl.cell(row_idx, 2)
            c2.fill.solid()
            c2.fill.fore_color.rgb = row_bg
            c2.vertical_anchor = MSO_ANCHOR.MIDDLE
            c2.margin_left = Inches(0.08)
            c2.margin_right = Inches(0.08)
            c2.margin_top = Inches(0.02)
            c2.margin_bottom = Inches(0.02)
            tf2 = c2.text_frame
            tf2.word_wrap = True

            p3 = tf2.paragraphs[0]
            r3_text = p3.add_run()
            r3_text.text = r["meaning"]
            r3_text.font.name = "Segoe UI"
            r3_text.font.size = Pt(7.8)
            r3_text.font.color.rgb = C_TEXT_DARK
            p3.line_spacing = 1.08

        return slide'''

old_table_func_pattern = re.compile(
    r'    def add_bus_table_slide\(slide_num, title, rows_data\):.*?'
    r'        return slide\n',
    re.DOTALL
)

if old_table_func_pattern.search(pres_code):
    pres_code = old_table_func_pattern.sub(new_add_bus_table_func + "\n", pres_code, count=1)
    with open(pres_path, "w", encoding="utf-8") as f:
        f.write(pres_code)
    print("[SUCCESS] Updated add_bus_table_slide in create_presentation.py")
else:
    print("[ERROR] add_bus_table_slide pattern not found in create_presentation.py")


# =============================================================================
# 2. UPDATE GENERATE_REPORT_DOCX.PY (SECTION 6.2 TABLE 2)
# =============================================================================
docx_path = os.path.join(cur_dir, "generate_report_docx.py")
with open(docx_path, "r", encoding="utf-8") as f:
    docx_code = f.read()

new_docx_t2 = '''    t2_headers = [
        "Trường hợp / Thời điểm",
        "Thiết lập RTL & Định nghĩa Firmware C (In rõ mã nguồn)",
        "Ý nghĩa thao tác của Firmware C & Cơ chế Co-Design"
    ]
    t2_rows = [
        {
            "case_time": "T = 0",
            "case_task": "(Boot Flash XIP)",
            "rtl_code": "// rtl/rdm6300_picorv32_soc.v\\nparameter [31:0] PROGADDR_RESET = 32'h0025_0000;\\n// rtl/core/soc_interconnect.v\\nassign sel_spimem = cpu_mem_valid &&\\n       (cpu_mem_addr >= 32'h0010_0000 && cpu_mem_addr < 32'h0100_0000);",
            "c_code": "/* firmware/boot/sections.lds */\\nFLASH (rx) : ORIGIN = 0x00250000, LENGTH = 0x000B0000\\n/* firmware/boot/start.s */\\n_start: lui sp, %hi(_stack_top)",
            "meaning": "Cấu hình vector reset của CPU trỏ trực tiếp vào Flash SPI để CPU tự động nạp và thực thi trực tiếp các opcode của firmware (XIP - Execute-in-Place) ngay sau khi nhả reset mà không cần nạp mã trung gian vào RAM."
        },
        {
            "case_time": "T = 1..100",
            "case_task": "(Tạo Stack RAM)",
            "rtl_code": "// rtl/rdm6300_picorv32_soc.v & soc_interconnect.v\\nparameter [31:0] STACKADDR = 32'h0000_0400;\\nassign sel_sram = cpu_mem_valid && (cpu_mem_addr < 32'h0000_0400);\\nassign sram_ready = 1'b1;",
            "c_code": "/* firmware/boot/sections.lds & start.s */\\nRAM (rwx) : ORIGIN = 0x00000000, LENGTH = 0x00000400\\nlui sp, %hi(_stack_top); addi sp, sp, %lo(_stack_top);",
            "meaning": "C sử dụng vùng không gian địa chỉ SRAM 1KB (< 0x0400) thông qua con trỏ ngăn xếp sp để cấp phát biến cục bộ, lưu trữ stack frame và địa chỉ trả về hàm (ra), phản hồi tức thì trong 1 chu kỳ clock."
        },
        {
            "case_time": "T = 101",
            "case_task": "(Vào hàm main)",
            "rtl_code": "// rtl/core/soc_interconnect.v\\nassign sel_spimem = cpu_mem_valid && (cpu_mem_addr >= 32'h0010_0000 && ...);\\nassign cpu_mem_rdata = sel_spimem ? spimem_rdata : sel_sram ? sram_rdata : ...;",
            "c_code": "/* firmware/boot/start.s & firmware/main.c */\\ncall main;\\nint main(void) { access_control_init(); while (1) access_control_poll(); }",
            "meaning": "C đặt toàn bộ mã máy thực thi của hàm main() và logic ứng dụng vào Flash để CPU đọc và giải mã từng opcode trực tiếp qua bus XIP, giải phóng toàn bộ 1KB SRAM chỉ dành cho lưu trữ dữ liệu động."
        },
        {
            "case_time": "T = 105",
            "case_task": "(Set Baud Dual UART)",
            "rtl_code": "// rtl/core/soc_interconnect.v & rtl/uart/uart_mmio.v\\nassign sel_rfid = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h1);\\nif (reg_div_sel && |cpu_mem_wstrb) uart_div <= cpu_mem_wdata;",
            "c_code": "/* firmware/common/soc_regs.h & firmware/app/access_control.c */\\n#define REG_RFID_UART_DIV (*(volatile uint32_t*)0x10000000)\\nREG_RFID_UART_DIV = 5208; // 50 MHz / 9600 Baud",
            "meaning": "C ghi giá trị chia tần 5208 vào địa chỉ 0x10000000 và 0x30000000 để cấu hình bộ chia baud rate 9600 bps cho cả khối UART RFID (50 MHz / 9600) và UART Host PC."
        },
        {
            "case_time": "T = 200",
            "case_task": "(Đọc thẻ RFID)",
            "rtl_code": "// rtl/uart/uart_mmio.v & rtl/uart/simpleuart_fifo.v\\nwire reg_dat_sel = valid && (addr[2] == 1'b1);\\nassign reg_dat_do = fifo_empty ? 32'hFFFFFFFF : {24'd0, fifo_dout};",
            "c_code": "/* firmware/common/soc_regs.h & firmware/app/access_control.c */\\n#define REG_RFID_UART_DAT (*(volatile uint32_t*)0x10000004)\\nuint32_t d = REG_RFID_UART_DAT; if (d != 0xFFFFFFFF) rdm6300_push(d);",
            "meaning": "C đọc từ địa chỉ 0x10000004 để rút (pop) 1 byte dữ liệu từ hàng đợi phần cứng FIFO 32-byte (đọc không khóa: trả về byte mã thẻ nếu có dữ liệu, hoặc trả về 0xFFFFFFFF nếu FIFO rỗng để CPU không bị treo chờ bus)."
        },
        {
            "case_time": "T = 250",
            "case_task": "(Giao tiếp PC UART)",
            "rtl_code": "// rtl/core/soc_interconnect.v & rtl/uart/uart_mmio.v\\nassign sel_uart = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h3);\\nwire dat_we = reg_dat_sel && (|wstrb); // Write TX FIFO",
            "c_code": "/* firmware/common/soc_regs.h & firmware/drivers/uart.c */\\n#define REG_PC_UART_DAT (*(volatile uint32_t*)0x30000004)\\nREG_PC_UART_DAT = c; /* Ghi TX */ | d = REG_PC_UART_DAT; /* Doc RX */",
            "meaning": "C ghi byte vào địa chỉ 0x30000004 để đẩy ký tự vào TX FIFO truyền lên máy tính Host PC, và đọc từ địa chỉ này để nhận các chuỗi lệnh cấu hình quản trị (Ping, thêm/xóa thẻ Whitelist, xuất nhật ký ra file CSV)."
        },
        {
            "case_time": "T = 300",
            "case_task": "(Bật LED / Mở Cửa)",
            "rtl_code": "// rtl/core/soc_interconnect.v & rtl/core/soc_gpio_mmio.v\\nassign sel_gpio = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h4);\\nif (sel_gpio && |wstrb) gpio_led_reg[7:0] <= wdata[7:0];",
            "c_code": "/* firmware/common/soc_regs.h & firmware/app/access_control.c */\\n#define REG_GPIO_LEDS (*(volatile uint32_t*)0x40000000)\\nREG_GPIO_LEDS = (REG_GPIO_LEDS & ~0x0002) | 0x0004; // Bit 2: Granted",
            "meaning": "C ghi giá trị bitmask vào địa chỉ 0x40000000 để điều khiển trực tiếp 16 LED chẩn đoán trên bo mạch và đóng/ngắt relay chốt cửa điện từ (Bit 0: Nhịp tim Alive, Bit 1: Cảnh báo từ chối Denied, Bit 2: Mở chốt cửa Granted)."
        },
        {
            "case_time": "T = 400",
            "case_task": "(Ghi Flash từ RAM)",
            "rtl_code": "// rtl/core/soc_interconnect.v & rtl/core/spimemio.v\\nassign sel_spicfg = cpu_mem_valid && (cpu_mem_addr == 32'h0200_0000);\\n.cfgreg_we(sel_spicfg ? mem_wstrb : 4'b0000), .cfgreg_di(mem_wdata)",
            "c_code": "/* firmware/boot/start.s & firmware/drivers/flash.c */\\nflashio_worker: li t0, 0x02000000; sh t1, 0(t0);\\nstatic void flashio(uint8_t *data, int len, uint8_t wrencmd);",
            "meaning": "Khi thực thi mã từ SRAM, hàm của C phát lệnh bit-bang SPI vào địa chỉ 0x02000000 để xóa sector và ghi dữ liệu thẻ mới vào Flash Whitelist / Log mà không gây xung đột bus với các chu kỳ đọc lệnh XIP."
        }
    ]

    t2 = doc.add_table(rows=len(t2_rows) + 1, cols=3)
    for c_idx, h_text in enumerate(t2_headers):
        t2.cell(0, c_idx).paragraphs[0].text = h_text

    for r_idx, r in enumerate(t2_rows):
        row_num = r_idx + 1
        # Cột 0: Trường hợp / Thời điểm
        c0 = t2.cell(row_num, 0)
        p0 = c0.paragraphs[0]
        r0_1 = p0.add_run(r["case_time"] + "\\n")
        r0_1.bold = True
        r0_2 = p0.add_run(r["case_task"])

        # Cột 1: Cấu hình RTL & Code C in rõ ràng
        c1 = t2.cell(row_num, 1)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(1.5)
        p1.paragraph_format.space_after = Pt(1.5)
        p1.paragraph_format.line_spacing = 1.05
        r1_lbl = p1.add_run("• Mã RTL:\\n")
        r1_lbl.bold = True
        set_font(r1_lbl, size=8.5, bold=True, color=NAVY)
        r1_code = p1.add_run(r["rtl_code"])
        set_font(r1_code, size=7.8, bold=True, font_name="Consolas", color=BLACK)

        p2 = c1.add_paragraph()
        p2.paragraph_format.space_before = Pt(1.5)
        p2.paragraph_format.space_after = Pt(1.5)
        p2.paragraph_format.line_spacing = 1.05
        r2_lbl = p2.add_run("• Mã C / Linker:\\n")
        r2_lbl.bold = True
        set_font(r2_lbl, size=8.5, bold=True, color=RGBColor(21, 128, 61))
        r2_code = p2.add_run(r["c_code"])
        set_font(r2_code, size=7.8, bold=True, font_name="Consolas", color=BLACK)

        # Cột 2: Ý nghĩa thao tác chuyển qua cột mới
        c2 = t2.cell(row_num, 2)
        p3 = c2.paragraphs[0]
        p3.paragraph_format.space_before = Pt(1.5)
        p3.paragraph_format.space_after = Pt(1.5)
        p3.paragraph_format.line_spacing = 1.12
        r3_txt = p3.add_run(r["meaning"])
        set_font(r3_txt, size=8.2, color=BLACK)

    col_w2 = [Inches(1.15), Inches(3.20), Inches(2.45)]
    col_a2 = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.JUSTIFY]
    style_table(t2, col_w2, col_a2, font_size=8.0)
    add_caption("Bảng 2. Bảng phân tích chu kỳ bus thực tế: Đối chiếu thiết lập giải mã RTL, định nghĩa code C và ý nghĩa thao tác của Firmware")'''

old_docx_t2_pattern = re.compile(
    r'    t2_headers = \[.*?'
    r'    add_caption\("Bảng 2\. Bảng phân tích chu kỳ bus thực tế: Đối chiếu thiết lập giải mã RTL, định nghĩa code C và ý nghĩa thao tác của Firmware"\)',
    re.DOTALL
)

if old_docx_t2_pattern.search(docx_code):
    docx_code = old_docx_t2_pattern.sub(new_docx_t2, docx_code, count=1)
    with open(docx_path, "w", encoding="utf-8") as f:
        f.write(docx_code)
    print("[SUCCESS] Updated Table 2 in generate_report_docx.py")
else:
    print("[ERROR] Table 2 pattern not found in generate_report_docx.py")
