# -*- coding: utf-8 -*-
"""
tune_table_slide11.py
Tunes Slide 11 in create_presentation.py to ensure all 8 rows fit cleanly:
- y = Inches(1.15), h = Inches(5.75)
- Col widths: 1.65", 5.65", 4.433"
- In Col 1: P1 for RTL, P2 for C (label + file + exact code)
- Font size Pt(7.0) for code, Pt(7.5) for labels, Pt(7.5) for meaning
"""

import os
import re

cur_dir = os.path.dirname(os.path.abspath(__file__))
pres_path = os.path.join(cur_dir, "create_presentation.py")

with open(pres_path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update all_rows_bus
new_rows_data = '''    all_rows_bus = [
        {
            "time": "T = 0",
            "task": "(Boot Flash XIP)",
            "rtl_file": "[rdm6300_picorv32_soc.v & soc_interconnect.v]",
            "rtl_code": "parameter [31:0] PROGADDR_RESET = 32'h0025_0000; | assign sel_spimem = cpu_mem_valid && (cpu_mem_addr >= 32'h0010_0000 && cpu_mem_addr < 32'h0100_0000);",
            "c_file": "[sections.lds & start.s]",
            "c_code": "FLASH (rx) : ORIGIN = 0x00250000, LENGTH = 0x000B0000 | _start: lui sp, %hi(_stack_top)",
            "meaning": "Cấu hình vector reset trỏ thẳng vào Flash SPI để CPU tự động nạp và thực thi trực tiếp opcode firmware (XIP) ngay sau khi nhả reset mà không cần nạp vào RAM."
        },
        {
            "time": "T = 1..100",
            "task": "(Tạo Stack RAM)",
            "rtl_file": "[rdm6300_picorv32_soc.v & soc_interconnect.v]",
            "rtl_code": "parameter [31:0] STACKADDR = 32'h0000_0400; | assign sel_sram = cpu_mem_valid && (cpu_mem_addr < 32'h0000_0400); assign sram_ready = 1'b1;",
            "c_file": "[sections.lds & start.s]",
            "c_code": "RAM (rwx) : ORIGIN = 0x00000000, LENGTH = 0x00000400 | lui sp, %hi(_stack_top); addi sp, sp, %lo(_stack_top);",
            "meaning": "C sử dụng không gian SRAM 1KB (< 0x0400) qua con trỏ ngăn xếp sp để cấp phát biến cục bộ, lưu stack frame và địa chỉ trả về hàm, phản hồi tức thì trong 1 chu kỳ clock."
        },
        {
            "time": "T = 101",
            "task": "(Vào hàm main)",
            "rtl_file": "[soc_interconnect.v]",
            "rtl_code": "assign sel_spimem = cpu_mem_valid && (cpu_mem_addr >= 32'h0010_0000 && ...); | assign cpu_mem_rdata = sel_spimem ? spimem_rdata : ...;",
            "c_file": "[start.s & main.c]",
            "c_code": "call main; | int main(void) { access_control_init(); while (1) access_control_poll(); }",
            "meaning": "Chuyển giao quyền điều khiển từ assembly khởi động sang code C bậc cao. Hàm main() chạy trực tiếp từ Flash XIP, giải phóng toàn bộ 1KB SRAM chỉ dùng cho dữ liệu động."
        },
        {
            "time": "T = 105",
            "task": "(Set Baud Dual UART)",
            "rtl_file": "[soc_interconnect.v & uart_mmio.v]",
            "rtl_code": "assign sel_rfid = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h1); | if (reg_div_sel && |cpu_mem_wstrb) uart_div <= cpu_mem_wdata;",
            "c_file": "[soc_regs.h & access_control.c]",
            "c_code": "#define REG_RFID_UART_DIV (*(volatile uint32_t*)0x10000000) | REG_RFID_UART_DIV = 5208; // 50 MHz / 9600 Baud",
            "meaning": "C ghi giá trị chia tần 5208 vào địa chỉ 0x10000000 và 0x30000000 để cài đặt tốc độ baud 9600 bps cho cả đầu đọc RFID RDM6300 và cổng máy tính PC (50 MHz / 9600)."
        },
        {
            "time": "T = 200",
            "task": "(Đọc thẻ RFID)",
            "rtl_file": "[uart_mmio.v & simpleuart_fifo.v]",
            "rtl_code": "wire reg_dat_sel = valid && (addr[2] == 1'b1); | assign reg_dat_do = fifo_empty ? 32'hFFFFFFFF : {24'd0, fifo_dout};",
            "c_file": "[soc_regs.h & access_control.c]",
            "c_code": "#define REG_RFID_UART_DAT (*(volatile uint32_t*)0x10000004) | uint32_t d = REG_RFID_UART_DAT; if (d != 0xFFFFFFFF) rdm6300_push(d);",
            "meaning": "C đọc từ 0x10000004 rút (pop) 1 byte từ FIFO 32B (đọc không khóa: trả về byte mã thẻ nếu có, hoặc trả về 0xFFFFFFFF nếu FIFO rỗng để CPU không bị nghẽn bus)."
        },
        {
            "time": "T = 250",
            "task": "(Giao tiếp PC UART)",
            "rtl_file": "[soc_interconnect.v & uart_mmio.v]",
            "rtl_code": "assign sel_uart = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h3); | wire dat_we = reg_dat_sel && (|wstrb); // Write TX FIFO",
            "c_file": "[soc_regs.h & uart.c]",
            "c_code": "#define REG_PC_UART_DAT (*(volatile uint32_t*)0x30000004) | REG_PC_UART_DAT = c; /* Ghi TX */ | d = REG_PC_UART_DAT; /* Doc RX */",
            "meaning": "C ghi byte vào 0x30000004 để đẩy ký tự vào TX FIFO truyền lên Host PC, và đọc từ địa chỉ này để nhận chuỗi lệnh quản trị (Ping, thêm/xóa thẻ Whitelist, xuất log CSV)."
        },
        {
            "time": "T = 300",
            "task": "(Bật LED / Mở Cửa)",
            "rtl_file": "[soc_interconnect.v & soc_gpio_mmio.v]",
            "rtl_code": "assign sel_gpio = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h4); | if (sel_gpio && |wstrb) gpio_led_reg[7:0] <= wdata[7:0];",
            "c_file": "[soc_regs.h & access_control.c]",
            "c_code": "#define REG_GPIO_LEDS (*(volatile uint32_t*)0x40000000) | REG_GPIO_LEDS = (REG_GPIO_LEDS & ~0x0002) | 0x0004; // Bit 2: Granted",
            "meaning": "C ghi giá trị bitmask vào 0x40000000 điều khiển 16 LED chẩn đoán trên bo mạch và đóng/ngắt relay mở chốt cửa điện từ (Bit 0: Alive 1Hz, Bit 1: Denied, Bit 2: Granted)."
        },
        {
            "time": "T = 400",
            "task": "(Ghi Flash từ RAM)",
            "rtl_file": "[soc_interconnect.v & spimemio.v]",
            "rtl_code": "assign sel_spicfg = cpu_mem_valid && (cpu_mem_addr == 32'h0200_0000); | .cfgreg_we(sel_spicfg ? mem_wstrb : 4'b0000)",
            "c_file": "[start.s & flash.c]",
            "c_code": "flashio_worker: li t0, 0x02000000; sh t1, 0(t0); | static void flashio(uint8_t *data, int len, uint8_t wrencmd);",
            "meaning": "Khi chạy từ SRAM, hàm của C phát lệnh bit-bang SPI vào 0x02000000 để xóa sector và ghi dữ liệu thẻ mới vào Flash Whitelist / Log mà không gây xung đột bus với các lệnh XIP."
        }
    ]'''

start_m = "    all_rows_bus = ["
end_m = "    s11 = add_bus_table_slide(11,"
s_idx = code.find(start_m)
e_idx = code.find(end_m)
code = code[:s_idx] + new_rows_data + "\n" + code[e_idx:]

# 2. Update add_bus_table_slide
new_table_func = '''    def add_bus_table_slide(slide_num, title, rows_data):
        slide = prs.slides.add_slide(blank_layout)
        add_header(slide, "Phần 6: Firmware C & Ánh Xạ MMIO", title, slide_num, total_slides=TOTAL_SLIDES)

        x = Inches(0.8)
        y = Inches(1.18)
        w = Inches(11.733)
        h = Inches(5.72)

        num_rows = len(rows_data) + 1
        tbl_shape = slide.shapes.add_table(num_rows, 3, x, y, w, h)
        tbl = tbl_shape.table

        col_w = [Inches(1.60), Inches(5.80), Inches(4.333)]
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
            cell.margin_left = Inches(0.08)
            cell.margin_right = Inches(0.08)
            cell.margin_top = Inches(0.03)
            cell.margin_bottom = Inches(0.03)

            p = cell.text_frame.paragraphs[0]
            p.text = h_text
            p.font.name = "Segoe UI"
            p.font.size = Pt(10.0)
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
            c0.margin_left = Inches(0.04)
            c0.margin_right = Inches(0.04)
            tf0 = c0.text_frame
            tf0.word_wrap = True

            p0_1 = tf0.paragraphs[0]
            p0_1.text = r["time"]
            p0_1.font.name = "Segoe UI"
            p0_1.font.size = Pt(10.0)
            p0_1.font.bold = True
            p0_1.font.color.rgb = C_BLUE_ACCENT
            p0_1.alignment = PP_ALIGN.CENTER

            p0_2 = tf0.add_paragraph()
            p0_2.text = r["task"]
            p0_2.font.name = "Segoe UI"
            p0_2.font.size = Pt(8.2)
            p0_2.font.bold = True
            p0_2.font.color.rgb = C_TEXT_DARK
            p0_2.alignment = PP_ALIGN.CENTER

            # Cột 1: Cấu hình RTL & Code C in rõ ràng
            c1 = tbl.cell(row_idx, 1)
            c1.fill.solid()
            c1.fill.fore_color.rgb = row_bg
            c1.vertical_anchor = MSO_ANCHOR.MIDDLE
            c1.margin_left = Inches(0.06)
            c1.margin_right = Inches(0.06)
            c1.margin_top = Inches(0.01)
            c1.margin_bottom = Inches(0.01)
            tf1 = c1.text_frame
            tf1.word_wrap = True

            # RTL Line
            p1 = tf1.paragraphs[0]
            r1_lbl = p1.add_run()
            r1_lbl.text = "• RTL "
            r1_lbl.font.name = "Segoe UI"
            r1_lbl.font.size = Pt(7.8)
            r1_lbl.font.bold = True
            r1_lbl.font.color.rgb = C_BLUE_ACCENT

            r1_file = p1.add_run()
            r1_file.text = r["rtl_file"] + ": "
            r1_file.font.name = "Segoe UI"
            r1_file.font.size = Pt(7.2)
            r1_file.font.bold = True
            r1_file.font.color.rgb = RGBColor(30, 58, 138)

            r1_code = p1.add_run()
            r1_code.text = r["rtl_code"]
            r1_code.font.name = "Consolas"
            r1_code.font.size = Pt(7.0)
            r1_code.font.bold = True
            r1_code.font.color.rgb = RGBColor(15, 23, 42)
            p1.space_after = Pt(1.5)
            p1.line_spacing = 1.02

            # C Line
            p2 = tf1.add_paragraph()
            r2_lbl = p2.add_run()
            r2_lbl.text = "• Code C "
            r2_lbl.font.name = "Segoe UI"
            r2_lbl.font.size = Pt(7.8)
            r2_lbl.font.bold = True
            r2_lbl.font.color.rgb = C_GREEN

            r2_file = p2.add_run()
            r2_file.text = r["c_file"] + ": "
            r2_file.font.name = "Segoe UI"
            r2_file.font.size = Pt(7.2)
            r2_file.font.bold = True
            r2_file.font.color.rgb = RGBColor(21, 128, 61)

            r2_code = p2.add_run()
            r2_code.text = r["c_code"]
            r2_code.font.name = "Consolas"
            r2_code.font.size = Pt(7.0)
            r2_code.font.bold = True
            r2_code.font.color.rgb = RGBColor(15, 23, 42)
            p2.line_spacing = 1.02

            # Cột 2: Ý nghĩa thao tác
            c2 = tbl.cell(row_idx, 2)
            c2.fill.solid()
            c2.fill.fore_color.rgb = row_bg
            c2.vertical_anchor = MSO_ANCHOR.MIDDLE
            c2.margin_left = Inches(0.06)
            c2.margin_right = Inches(0.06)
            c2.margin_top = Inches(0.01)
            c2.margin_bottom = Inches(0.01)
            tf2 = c2.text_frame
            tf2.word_wrap = True

            p3 = tf2.paragraphs[0]
            r3_text = p3.add_run()
            r3_text.text = r["meaning"]
            r3_text.font.name = "Segoe UI"
            r3_text.font.size = Pt(7.5)
            r3_text.font.color.rgb = C_TEXT_DARK
            p3.line_spacing = 1.05

        return slide'''

start_f = "    def add_bus_table_slide(slide_num, title, rows_data):"
end_f = "    # Helper: Slide chi tiết cho từng trường hợp bus"
sf_idx = code.find(start_f)
ef_idx = code.find(end_f)
code = code[:sf_idx] + new_table_func + "\n\n" + code[ef_idx:]

with open(pres_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Successfully tuned Slide 11 in create_presentation.py")
