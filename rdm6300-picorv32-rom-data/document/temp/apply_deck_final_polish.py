import os
import re

cur_dir = r"d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp"

# 1. Polish Slide 14 in create_presentation.py
pres_file = os.path.join(cur_dir, "create_presentation.py")
with open(pres_file, "r", encoding="utf-8") as f:
    pres_content = f.read()

# Replace spacing in Slide 14
pres_content = pres_content.replace("p_end1.space_after = Pt(26)", "p_end1.space_after = Pt(16)")
pres_content = pres_content.replace("p.space_after = Pt(20)\n        p.line_spacing = 1.25", "p.space_after = Pt(13)\n        p.line_spacing = 1.18")
pres_content = pres_content.replace("run_title.font.size = Pt(17.5)", "run_title.font.size = Pt(16.0)")
pres_content = pres_content.replace("run_desc.font.size = Pt(16.5)", "run_desc.font.size = Pt(15.0)")
pres_content = pres_content.replace("p_git.space_before = Pt(14)", "p_git.space_before = Pt(10)")
pres_content = pres_content.replace("p_ty.space_before = Pt(18)", "p_ty.space_before = Pt(12)")
pres_content = pres_content.replace("p_ty.font.size = Pt(22)", "p_ty.font.size = Pt(20)")

with open(pres_file, "w", encoding="utf-8") as f:
    f.write(pres_content)

print("create_presentation.py polished!")

# 2. Update generate_abstract_docx.py
abs_file = os.path.join(cur_dir, "generate_abstract_docx.py")
with open(abs_file, "r", encoding="utf-8") as f:
    abs_content = f.read()

abs_content = abs_content.replace(
    'add_h1("PHẦN III: BẢNG ĐỐI CHIẾU NHANH THEO 12 SLIDE BÁO CÁO")',
    'add_h1("PHẦN III: BẢNG ĐỐI CHIẾU NHANH THEO 14 SLIDE BÁO CÁO")'
)
abs_content = abs_content.replace(
    'Nhằm hỗ trợ theo dõi xuyên suốt quá trình thuyết trình, bảng dưới đây tóm tắt trục nội dung và kết quả chính của từng slide trong bộ slide 12 trang:',
    'Nhằm hỗ trợ theo dõi xuyên suốt quá trình thuyết trình, bảng dưới đây tóm tắt trục nội dung và kết quả chính của từng slide trong bộ slide 14 trang:'
)
abs_content = abs_content.replace(
    'tbl_slides = doc.add_table(rows=13, cols=3)',
    'tbl_slides = doc.add_table(rows=15, cols=3)'
)

old_slides_map = '''    slides_map = [
        ("Slide", "Tiêu Đề Trọng Tâm", "Nội Dung & Minh Chứng Kỹ Thuật Đạt Được"),
        ("Slide 1", "Bìa Báo Cáo Đồ Án", "Thông tin học viên, giảng viên hướng dẫn, chuyên ngành Chip Design SEM3."),
        ("Slide 2", "Phần 1: Giới Thiệu Dự Án", "3 luận điểm cốt lõi: Tính cấp thiết Offline, vai trò Flash NVM và tự chủ ASIC."),
        ("Slide 3", "Phần 3: Sơ Đồ Khối SoC", "Sơ đồ kiến trúc vi hệ thống SoC PicoRV32 (1 Master - 5 Slaves, 4MB Flash, 1KB SRAM)."),
        ("Slide 4", "Phần 3: Kiến Trúc UART RTL", "Bản vẽ 5 tầng UART RTL: CDC 2-FF, 16x Sampler, FIFO 32B, MMIO Non-blocking."),
        ("Slide 5", "Phần 4: Testbench 1 (tb_uart_rtl)", "Dạng sóng mô phỏng Vivado 15.275 µs xác nhận 100% Pass 5 kịch bản phần cứng thuần."),
        ("Slide 6", "Phần 4: Testbench 2 (tb_uart_ping)", "Kiểm thử tích hợp Boot Flash XIP & Ping; CPU healthy, cpu_trap == 0 suốt 2.086 ms."),
        ("Slide 7", "Phần 5: Demo FPGA Thiết Lập", "Sơ đồ kết nối phần cứng Basys 3: Nguồn 5V MB102 riêng cho RDM6300, trở đệm bảo vệ 1kΩ."),
        ("Slide 8", "Phần 5: Demo FPGA Host CLI", "Giao diện Host Console CLI 10 chức năng; Tra cứu Whitelist, xuất nhập CSV, 512 Logs."),
        ("Slide 9", "Phần 6: ASIC Sign-off & Config", "Bằng chứng 0 Antenna, 0 LVS, 0 DRC violations, bản vẽ OpenROAD và cấu hình config.json."),
        ("Slide 10", "Phần 6: Bảng PPA Metrics", "Bảng tổng hợp diện tích Die 1.87 mm², 164K cells, công suất 76 mW, IR Drop 1.39 mV."),
        ("Slide 11", "Phần 6: Phân Tích Định Thời STA", "Bảng Multi-Corner Timing từ summary.rpt; Fmax = 92.81 MHz (vượt 85.6%), 21.9K hold buffers."),
        ("Slide 12", "Tổng Kết Đồ Án & Lời Cảm Ơn", "4 thành tựu nổi bật của đồ án và lời cảm ơn trân trọng gửi tới Quý Thầy Cô cùng độc giả.")
    ]'''

new_slides_map = '''    slides_map = [
        ("Slide", "Tiêu Đề Trọng Tâm", "Nội Dung & Minh Chứng Kỹ Thuật Đạt Được"),
        ("Slide 1", "Bìa Báo Cáo Đồ Án", "Thông tin tác giả, đồ án SoC PicoRV32 RFID RDM6300 & SPI Flash, hệ sinh thái EDA."),
        ("Slide 2", "Phần 1: Giới Thiệu Dự Án", "3 luận điểm cốt lõi: Tính cấp thiết Offline, vai trò Flash NVM và tự chủ ASIC."),
        ("Slide 3", "Phần 1: Tổng Quan Sản Phẩm", "4 trụ cột: RTL chạy firmware C & mở rộng; Firmware C trên chip; FPGA Basys 3; OpenLane ASIC."),
        ("Slide 4", "Phần 3: Sơ Đồ Khối SoC", "Sơ đồ kiến trúc vi hệ thống SoC PicoRV32 (1 Master - 5 Slaves, 4MB Flash, 1KB SRAM, 32 FIFO)."),
        ("Slide 5", "Phần 3: Bảng Memory Map", "Bảng tra cứu MMIO 0x1000/0x3000/0x4000, Flash Sector 48/49, SRAM 0x0200_0000 trong C/RTL."),
        ("Slide 6", "Phần 5: Demo Host Console CLI", "Giao diện Host CLI 10 chức năng: Ping, thêm/xóa thẻ, quét ảo, 512 Logs, đồng bộ CSV."),
        ("Slide 7", "Phần 3: Kiến Trúc UART RTL", "Bản vẽ 5 tầng UART RTL: CDC 2-FF, 16x Sampler, FIFO 32B, MMIO Non-blocking."),
        ("Slide 8", "Phần 4: Testbench 1 (tb_uart_rtl)", "Dạng sóng mô phỏng Vivado 15.275 µs xác nhận 100% Pass 5 kịch bản phần cứng thuần."),
        ("Slide 9", "Phần 4: Testbench 2 (tb_uart_ping)", "Kiểm thử tích hợp Boot Flash XIP & Ping; CPU healthy, cpu_trap == 0 suốt 2.086 ms."),
        ("Slide 10", "Phần 5: Demo FPGA Thiết Lập", "Sơ đồ kết nối phần cứng Basys 3: Nguồn 5V MB102 riêng cho RDM6300, trở đệm bảo vệ 1kΩ."),
        ("Slide 11", "Phần 6: ASIC Sign-off & Config", "Bằng chứng 0 Antenna, 0 LVS, 0 DRC violations, bản vẽ OpenROAD và cấu hình config.json."),
        ("Slide 12", "Phần 6: Bảng PPA Metrics", "Bảng tổng hợp diện tích Die 1.87 mm², 164K cells, công suất 76 mW, IR Drop 1.39 mV."),
        ("Slide 13", "Phần 6: Phân Tích Định Thời STA", "Bảng Multi-Corner Timing từ summary.rpt; Fmax = 92.81 MHz (vượt 85.6%), 21.9K hold buffers."),
        ("Slide 14", "Tổng Kết Đồ Án & Lời Cảm Ơn", "4 thành tựu nổi bật của đồ án, link GitHub repository và lời cảm ơn trân trọng.")
    ]'''

abs_content = abs_content.replace(old_slides_map, new_slides_map)

with open(abs_file, "w", encoding="utf-8") as f:
    f.write(abs_content)

print("generate_abstract_docx.py updated to 14 slides mapping!")
