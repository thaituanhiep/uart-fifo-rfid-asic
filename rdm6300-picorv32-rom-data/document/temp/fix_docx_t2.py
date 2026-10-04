# -*- coding: utf-8 -*-
import os

docx_path = r"d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\generate_report_docx.py"
with open(docx_path, "r", encoding="utf-8") as f:
    content = f.read()

# Find start of t2_headers and end of add_caption
start_idx = content.find('    t2_headers = [')
end_marker = 'add_caption("Bảng 2. Bảng phân tích chu kỳ bus thực tế: Đối chiếu thiết lập giải mã RTL, định nghĩa code C và ý nghĩa thao tác của Firmware")'
end_idx = content.find(end_marker) + len(end_marker)

new_t2_block = '''    t2_headers = [
        "Trường hợp / Thời điểm",
        "Thiết lập RTL & Định nghĩa Firmware C (In rõ mã nguồn)",
        "Ý nghĩa thao tác của Firmware C & Cơ chế Co-Design"
    ]
    t2_rows = [
        {
            "case_time": "T = 0",
            "case_task": "(Boot Flash XIP)",
            "rtl_code": "// rtl/rdm6300_picorv32_soc.v\\nparameter [31:0] PROGADDR_RESET = 32\\'h0025_0000;\\n// rtl/core/soc_interconnect.v\\nassign sel_spimem = cpu_mem_valid &&\\n       (cpu_mem_addr >= 32\\'h0010_0000 && cpu_mem_addr < 32\\'h0100_0000);",
            "c_code": "/* firmware/boot/sections.lds */\\nFLASH (rx) : ORIGIN = 0x00250000, LENGTH = 0x000B0000\\n/* firmware/boot/start.s */\\n_start: lui sp, %hi(_stack_top)",
            "meaning": "Cấu hình vector reset của CPU trỏ trực tiếp vào Flash SPI để CPU tự động nạp và thực thi trực tiếp các opcode của firmware (XIP - Execute-in-Place) ngay sau khi nhả reset mà không cần nạp mã trung gian vào RAM."
        },
        {
            "case_time": "T = 1..100",
            "case_task": "(Tạo Stack RAM)",
            "rtl_code": "// rtl/rdm6300_picorv32_soc.v & soc_interconnect.v\\nparameter [31:0] STACKADDR = 32\\'h0000_0400;\\nassign sel_sram = cpu_mem_valid && (cpu_mem_addr < 32\\'h0000_0400);\\nassign sram_ready = 1\\'b1;",
            "c_code": "/* firmware/boot/sections.lds & start.s */\\nRAM (rwx) : ORIGIN = 0x00000000, LENGTH = 0x00000400\\nlui sp, %hi(_stack_top); addi sp, sp, %lo(_stack_top);",
            "meaning": "C sử dụng vùng không gian địa chỉ SRAM 1KB (< 0x0400) thông qua con trỏ ngăn xếp sp để cấp phát biến cục bộ, lưu trữ stack frame và địa chỉ trả về hàm (ra), phản hồi tức thì trong 1 chu kỳ clock."
        },
        {
            "case_time": "T = 101",
            "case_task": "(Vào hàm main)",
            "rtl_code": "// rtl/core/soc_interconnect.v\\nassign sel_spimem = cpu_mem_valid && (cpu_mem_addr >= 32\\'h0010_0000 && ...);\\nassign cpu_mem_rdata = sel_spimem ? spimem_rdata : sel_sram ? sram_rdata : ...;",
            "c_code": "/* firmware/boot/start.s & firmware/main.c */\\ncall main;\\nint main(void) { access_control_init(); while (1) access_control_poll(); }",
            "meaning": "C đặt toàn bộ mã máy thực thi của hàm main() và logic ứng dụng vào Flash để CPU đọc và giải mã từng opcode trực tiếp qua bus XIP, giải phóng toàn bộ 1KB SRAM chỉ dành cho lưu trữ dữ liệu động."
        },
        {
            "case_time": "T = 105",
            "case_task": "(Set Baud Dual UART)",
            "rtl_code": "// rtl/core/soc_interconnect.v & rtl/uart/uart_mmio.v\\nassign sel_rfid = cpu_mem_valid && (cpu_mem_addr[31:28] == 4\\'h1);\\nif (reg_div_sel && |cpu_mem_wstrb) uart_div <= cpu_mem_wdata;",
            "c_code": "/* firmware/common/soc_regs.h & firmware/app/access_control.c */\\n#define REG_RFID_UART_DIV (*(volatile uint32_t*)0x10000000)\\nREG_RFID_UART_DIV = 5208; // 50 MHz / 9600 Baud",
            "meaning": "C ghi giá trị chia tần 5208 vào địa chỉ 0x10000000 và 0x30000000 để cấu hình bộ chia baud rate 9600 bps cho cả khối UART RFID (50 MHz / 9600) và UART Host PC."
        },
        {
            "case_time": "T = 200",
            "case_task": "(Đọc thẻ RFID)",
            "rtl_code": "// rtl/uart/uart_mmio.v & rtl/uart/simpleuart_fifo.v\\nwire reg_dat_sel = valid && (addr[2] == 1\\'b1);\\nassign reg_dat_do = fifo_empty ? 32\\'hFFFFFFFF : {24\\'d0, fifo_dout};",
            "c_code": "/* firmware/common/soc_regs.h & firmware/app/access_control.c */\\n#define REG_RFID_UART_DAT (*(volatile uint32_t*)0x10000004)\\nuint32_t d = REG_RFID_UART_DAT; if (d != 0xFFFFFFFF) rdm6300_push(d);",
            "meaning": "C đọc từ địa chỉ 0x10000004 để rút (pop) 1 byte dữ liệu từ hàng đợi phần cứng FIFO 32-byte (đọc không khóa: trả về byte mã thẻ nếu có dữ liệu, hoặc trả về 0xFFFFFFFF nếu FIFO rỗng để CPU không bị treo chờ bus)."
        },
        {
            "case_time": "T = 250",
            "case_task": "(Giao tiếp PC UART)",
            "rtl_code": "// rtl/core/soc_interconnect.v & rtl/uart/uart_mmio.v\\nassign sel_uart = cpu_mem_valid && (cpu_mem_addr[31:28] == 4\\'h3);\\nwire dat_we = reg_dat_sel && (|wstrb); // Write TX FIFO",
            "c_code": "/* firmware/common/soc_regs.h & firmware/drivers/uart.c */\\n#define REG_PC_UART_DAT (*(volatile uint32_t*)0x30000004)\\nREG_PC_UART_DAT = c; /* Ghi TX */ | d = REG_PC_UART_DAT; /* Doc RX */",
            "meaning": "C ghi byte vào địa chỉ 0x30000004 để đẩy ký tự vào TX FIFO truyền lên máy tính Host PC, và đọc từ địa chỉ này để nhận các chuỗi lệnh cấu hình quản trị (Ping, thêm/xóa thẻ Whitelist, xuất nhật ký ra file CSV)."
        },
        {
            "case_time": "T = 300",
            "case_task": "(Bật LED / Mở Cửa)",
            "rtl_code": "// rtl/core/soc_interconnect.v & rtl/core/soc_gpio_mmio.v\\nassign sel_gpio = cpu_mem_valid && (cpu_mem_addr[31:28] == 4\\'h4);\\nif (sel_gpio && |wstrb) gpio_led_reg[7:0] <= wdata[7:0];",
            "c_code": "/* firmware/common/soc_regs.h & firmware/app/access_control.c */\\n#define REG_GPIO_LEDS (*(volatile uint32_t*)0x40000000)\\nREG_GPIO_LEDS = (REG_GPIO_LEDS & ~0x0002) | 0x0004; // Bit 2: Granted",
            "meaning": "C ghi giá trị bitmask vào địa chỉ 0x40000000 để điều khiển trực tiếp 16 LED chẩn đoán trên bo mạch và đóng/ngắt relay chốt cửa điện từ (Bit 0: Nhịp tim Alive, Bit 1: Cảnh báo từ chối Denied, Bit 2: Mở chốt cửa Granted)."
        },
        {
            "case_time": "T = 400",
            "case_task": "(Ghi Flash từ RAM)",
            "rtl_code": "// rtl/core/soc_interconnect.v & rtl/core/spimemio.v\\nassign sel_spicfg = cpu_mem_valid && (cpu_mem_addr == 32\\'h0200_0000);\\n.cfgreg_we(sel_spicfg ? mem_wstrb : 4\\'b0000), .cfgreg_di(mem_wdata)",
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

updated_content = content[:start_idx] + new_t2_block + content[end_idx:]
with open(docx_path, "w", encoding="utf-8") as f:
    f.write(updated_content)
print("Successfully fixed Table 2 in generate_report_docx.py")
