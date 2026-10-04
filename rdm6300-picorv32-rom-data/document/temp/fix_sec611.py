# -*- coding: utf-8 -*-
with open("generate_report_docx.py", "r", encoding="utf-8") as f:
    docx_code = f.read()

# Check if the function call or section heading is in the body
if "add_h2(\"6.1.1. Các đoạn mã RTL cấu hình phần cứng" not in docx_code:
    sec_611_code = '''    # -------------------------------------------------------------
    # 6.1.1. CÁC ĐOẠN MÃ RTL CẤU HÌNH PHẦN CỨNG THỰC THI FIRMWARE C
    # (DEDICATED 1 PAGE TRƯỚC BẢNG 2 CỘT 6.2)
    # -------------------------------------------------------------
    doc.add_page_break()
    add_h2("6.1.1. Các đoạn mã RTL cấu hình phần cứng cho phép hệ thống thực thi Firmware C")
    add_p("Mục này trình bày toàn bộ các đoạn mã nguồn phần cứng Verilog RTL cấu hình thông số kiến trúc để nhân vi xử lý PicoRV32 có thể khởi động và thực thi trơn tru firmware C, đồng thời đối chiếu sự tương thích tuyệt đối với tệp cấu hình bản đồ bộ nhớ Linker Script (firmware/sections.lds):")

    # Bảng tóm tắt thông số cấu hình phần cứng RTL vs Firmware C
    t_cfg = doc.add_table(rows=7, cols=4)
    cfg_headers = ["Tham số phần cứng RTL", "File RTL", "Giá trị thiết lập", "Khớp nối Firmware C / Linker (sections.lds)"]
    for c_idx, h_t in enumerate(cfg_headers):
        t_cfg.cell(0, c_idx).paragraphs[0].text = h_t

    cfg_rows = [
        ("PROGADDR_RESET", "rdm6300_picorv32_soc.v", "32'h0025_0000", "FLASH (rx) : ORIGIN = 0x00250000 (Vector Reset XIP)"),
        ("STACKADDR", "rdm6300_picorv32_soc.v", "32'h0000_0400", "_stack_top = 0x00000400 (Đỉnh ngăn xếp 1KB SRAM)"),
        ("WORDS = 256", "rtl/core/data_sram.v", "1024 Bytes", "RAM (rwx) : LENGTH = 0x00000400 (Vùng biến động & Stack)"),
        ("FAST_READ = 1'b1", "rtl/core/spimemio.v", "Opcode 0x0B", "Fast Read SPI Flash nạp opcode trực tiếp"),
        ("COMPRESSED_ISA = 1", "rtl/core/picorv32.v", "RV32IMC (16-bit)", "Tối ưu hóa mã máy, giảm 30% dung lượng Flash"),
        ("sel_sram / sel_spimem", "rtl/core/soc_interconnect.v", "< 0x0400 / >= 0x0010_0000", "Tách biệt vật lý bộ nhớ mã lệnh (Flash) và dữ liệu (SRAM)")
    ]
    for r_idx, (p_name, p_file, p_val, p_map) in enumerate(cfg_rows):
        row_i = r_idx + 1
        t_cfg.cell(row_i, 0).paragraphs[0].text = p_name
        t_cfg.cell(row_i, 1).paragraphs[0].text = p_file
        t_cfg.cell(row_i, 2).paragraphs[0].text = p_val
        t_cfg.cell(row_i, 3).paragraphs[0].text = p_map

    style_table(t_cfg, [Inches(1.8), Inches(1.5), Inches(1.2), Inches(2.2)], 
                [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT], font_size=8.5)
    add_caption("Bảng 1b. Đối chiếu tham số cấu hình phần cứng Verilog RTL và bản đồ bộ nhớ Linker Script Firmware C")

    p_lbl_rtl1 = add_p("1. Tham số cấu hình CPU PicoRV32, Flash Controller và SRAM (RTL):")
    p_lbl_rtl1.runs[0].bold = True
    add_console_block([
        "// rtl/rdm6300_picorv32_soc.v - Tham số khởi động nhân CPU PicoRV32",
        "parameter [31:0] PROGADDR_RESET = 32'h 0025_0000; // Reset vector Flash XIP",
        "parameter [31:0] STACKADDR      = 32'h 0000_0400; // Đỉnh ngăn xếp 1KB SRAM",
        "parameter [0:0]  COMPRESSED_ISA = 1;              // Hỗ trợ tập lệnh nén RVC",
        "parameter [0:0]  ENABLE_COUNTERS = 1;             // Kích hoạt bộ đếm chu kỳ hiệu năng",
        "",
        "// rtl/core/spimemio.v - Cấu hình bộ điều khiển Flash SPI",
        "parameter [0:0]  FAST_READ      = 1'b1;           // Chế độ đọc nhanh Fast Read (0x0B)",
        "// Dải địa chỉ Flash XIP: 0x0010_0000 - 0x00FF_FFFF (4MB)",
        "",
        "// rtl/core/data_sram.v - Cấu hình bộ nhớ dữ liệu nội vi mạch",
        "parameter integer WORDS = 256;                   // 256 từ x 32-bit = 1024 Bytes",
        "assign sram_ready = 1'b1;                        // Phản hồi tức thì trong 1 chu kỳ clock"
    ])

    p_lbl_rtl2 = add_p("2. Logic giải mã địa chỉ điều phối bus trung tâm (soc_interconnect.v):")
    p_lbl_rtl2.runs[0].bold = True
    add_console_block([
        "// rtl/core/soc_interconnect.v - Bus Decoding Equations",
        "assign sel_sram   = cpu_mem_valid && (cpu_mem_addr < 32'h0000_0400);",
        "assign sel_spimem = cpu_mem_valid && (cpu_mem_addr >= 32'h0010_0000 && cpu_mem_addr < 32'h0100_0000);",
        "assign sel_spicfg = cpu_mem_valid && (cpu_mem_addr == 32'h0200_0000);",
        "assign sel_rfid   = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h1); // 0x1000_0000",
        "assign sel_uart   = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h3); // 0x3000_0000",
        "assign sel_gpio   = cpu_mem_valid && (cpu_mem_addr[31:28] == 4'h4); // 0x4000_0000"
    ])

    p_lbl_c = add_p("3. Cấu hình bản đồ bộ nhớ trong Linker Script của Firmware C (firmware/sections.lds):")
    p_lbl_c.runs[0].bold = True
    add_console_block([
        "/* firmware/sections.lds - Linker script khớp nối trực tiếp với phần cứng */",
        "MEMORY {",
        "    FLASH (rx) : ORIGIN = 0x00250000, LENGTH = 0x000B0000 /* 704 KB Flash */",
        "    RAM (rwx)  : ORIGIN = 0x00000000, LENGTH = 0x00000400 /* 1 KB Data SRAM */",
        "}",
        "_stack_top = 0x00000400; /* Trùng khớp STACKADDR của phần cứng */"
    ])

    add_p("Ý nghĩa kỹ thuật và tính tương thích đồng thiết kế:")
    add_p("1. Thực thi tại chỗ (XIP): Bằng cách gán PROGADDR_RESET = 32'h0025_0000 trùng với vùng FLASH ORIGIN trong sections.lds, CPU PicoRV32 lập tức phát lệnh đọc opcode trực tiếp từ chip nhớ ngoài SPI Flash ngay sau khi nhả reset. Cơ chế này loại bỏ hoàn toàn nhu cầu về bộ nhớ ROM nạp trung gian (bootloader ROM) tốn kém diện tích trên vi mạch ASIC.")
    add_p("2. Tối ưu hóa bộ nhớ RAM: Toàn bộ 1024 bytes SRAM (< 0x0400) được dành trọn vẹn cho việc tạo khung ngăn xếp Stack Frame và lưu biến dữ liệu động, phản hồi tức thời trong đúng 1 chu kỳ xung nhịp (zero-wait-state), đảm bảo hiệu năng tính toán thời gian thực.")
'''
    target_62_heading = '    # 6.2. BẢNG PHÂN TÍCH CHU KỲ BUS THỰC TẾ: ĐỐI CHIẾU SETTING RTL, CODE C VÀ Ý NGHĨA BIẾN ĐỊA CHỈ\n    add_h2("6.2. Bảng phân tích chu kỳ bus thực tế: Đối chiếu setting RTL, code C và ý nghĩa biến địa chỉ")'
    if target_62_heading in docx_code:
        docx_code = docx_code.replace(target_62_heading, sec_611_code + "\n" + target_62_heading)
        with open("generate_report_docx.py", "w", encoding="utf-8") as f:
            f.write(docx_code)
        print("[SUCCESS] Properly inserted Section 6.1.1 into generate_report_docx.py")
    else:
        print("[ERROR] target_62_heading not found")
else:
    print("[INFO] Already present")
