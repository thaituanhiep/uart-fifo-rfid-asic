import os

cur_dir = r"d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp"

# 1. Update create_presentation.py
pres_file = os.path.join(cur_dir, "create_presentation.py")
with open(pres_file, "r", encoding="utf-8") as f:
    content = f.read()

# Locate the blocks
overview_header = "# SLIDE 03: PHẦN 1 - TỔNG QUAN NHỮNG GÌ SẢN PHẨM ĐÃ LÀM ĐƯỢC (4 TRỤ CỘT)"
block_diag_header = "# SLIDE 04: PHẦN 3 - SƠ ĐỒ KHỐI TỔNG THỂ SOC (BLOCK DIAGRAM B&W DRAW.IO)"
memory_map_header = "# SLIDE 05: PHẦN 3 - BẢNG TRA CỨU ĐỊA CHỈ MEMORY MAP (C & RTL)"

pos_overview = content.find(overview_header)
pos_block_diag = content.find(block_diag_header)
pos_memory_map = content.find(memory_map_header)

if pos_overview == -1 or pos_block_diag == -1 or pos_memory_map == -1:
    raise ValueError(f"Could not find headers! {pos_overview}, {pos_block_diag}, {pos_memory_map}")

# Extract block 1 (Overview) and block 2 (Block Diagram)
# Overview block: from pos_overview to pos_block_diag (trimmed of leading/trailing dividers)
overview_block = content[pos_overview:pos_block_diag]
# Block Diagram block: from pos_block_diag to pos_memory_map
block_diag_block = content[pos_block_diag:pos_memory_map]

# Adjust Overview block to be Slide 04
overview_block = overview_block.replace(
    '# SLIDE 03: PHẦN 1 - TỔNG QUAN NHỮNG GÌ SẢN PHẨM ĐÃ LÀM ĐƯỢC (4 TRỤ CỘT)',
    '# SLIDE 04: PHẦN 1 - TỔNG QUAN NHỮNG GÌ SẢN PHẨM ĐÃ LÀM ĐƯỢC (4 TRỤ CỘT)'
)
overview_block = overview_block.replace(
    '"Tổng Quan Những Gì Sản Phẩm Đã Thực Hiện Thành Công", 3, total_slides=TOTAL_SLIDES)',
    '"Tổng Quan Những Gì Sản Phẩm Đã Thực Hiện Thành Công", 4, total_slides=TOTAL_SLIDES)'
)

# Adjust Block Diagram block to be Slide 03
block_diag_block = block_diag_block.replace(
    '# SLIDE 04: PHẦN 3 - SƠ ĐỒ KHỐI TỔNG THỂ SOC (BLOCK DIAGRAM B&W DRAW.IO)',
    '# SLIDE 03: PHẦN 3 - SƠ ĐỒ KHỐI TỔNG THỂ SOC (BLOCK DIAGRAM B&W DRAW.IO)'
)
block_diag_block = block_diag_block.replace(
    '"Sơ Đồ Khối Kiến Trúc Vi Hệ Thống SoC PicoRV32 (4MB Flash, 1KB SRAM, 32 Fifo)", 4, total_slides=TOTAL_SLIDES)',
    '"Sơ Đồ Khối Kiến Trúc Vi Hệ Thống SoC PicoRV32 (4MB Flash, 1KB SRAM, 32 Fifo)", 3, total_slides=TOTAL_SLIDES)'
)

# Clean up divider comment separators
clean_overview = overview_block.strip()
clean_block_diag = block_diag_block.strip()

new_middle_section = f"    # =========================================================================\n    {clean_block_diag}\n\n    # =========================================================================\n    {clean_overview}\n\n    # =========================================================================\n    "

# Reconstruct
prefix = content[:pos_overview]
suffix = content[pos_memory_map:]

# Check if there is extra divider before pos_overview
if prefix.endswith("    # =========================================================================\n"):
    prefix = prefix[:-len("    # =========================================================================\n")]

new_content = prefix + new_middle_section + suffix

with open(pres_file, "w", encoding="utf-8") as f:
    f.write(new_content)

print("create_presentation.py: Swapped Slide 3 and Slide 4 successfully!")

# 2. Update generate_abstract_docx.py
abs_file = os.path.join(cur_dir, "generate_abstract_docx.py")
with open(abs_file, "r", encoding="utf-8") as f:
    abs_content = f.read()

old_slides_map = '''    slides_map = [
        ("Slide", "Tiêu Đề Trọng Tâm", "Nội Dung & Minh Chứng Kỹ Thuật Đạt Được"),
        ("Slide 1", "Bìa Báo Cáo Đồ Án", "Thông tin tác giả, đồ án SoC PicoRV32 RFID RDM6300 & SPI Flash, hệ sinh thái EDA."),
        ("Slide 2", "Phần 1: Giới Thiệu Dự Án", "3 luận điểm cốt lõi: Tính cấp thiết Offline, vai trò Flash NVM và tự chủ ASIC."),
        ("Slide 3", "Phần 1: Tổng Quan Sản Phẩm", "4 trụ cột: RTL chạy firmware C & mở rộng; Firmware C trên chip; FPGA Basys 3; OpenLane ASIC."),
        ("Slide 4", "Phần 3: Sơ Đồ Khối SoC", "Sơ đồ kiến trúc vi hệ thống SoC PicoRV32 (1 Master - 5 Slaves, 4MB Flash, 1KB SRAM, 32 FIFO)."),
        ("Slide 5", "Phần 3: Bảng Memory Map", "Bảng tra cứu MMIO 0x1000/0x3000/0x4000, Flash Sector 48/49, SRAM 0x0200_0000 trong C/RTL."),'''

new_slides_map = '''    slides_map = [
        ("Slide", "Tiêu Đề Trọng Tâm", "Nội Dung & Minh Chứng Kỹ Thuật Đạt Được"),
        ("Slide 1", "Bìa Báo Cáo Đồ Án", "Thông tin tác giả, đồ án SoC PicoRV32 RFID RDM6300 & SPI Flash, hệ sinh thái EDA."),
        ("Slide 2", "Phần 1: Giới Thiệu Dự Án", "3 luận điểm cốt lõi: Tính cấp thiết Offline, vai trò Flash NVM và tự chủ ASIC."),
        ("Slide 3", "Phần 3: Sơ Đồ Khối SoC", "Sơ đồ kiến trúc vi hệ thống SoC PicoRV32 (1 Master - 5 Slaves, 4MB Flash, 1KB SRAM, 32 FIFO)."),
        ("Slide 4", "Phần 1: Tổng Quan Sản Phẩm", "4 trụ cột: RTL chạy firmware C & mở rộng; Firmware C trên chip; FPGA Basys 3; OpenLane ASIC."),
        ("Slide 5", "Phần 3: Bảng Memory Map", "Bảng tra cứu MMIO 0x1000/0x3000/0x4000, Flash Sector 48/49, SRAM 0x0200_0000 trong C/RTL."),'''

if old_slides_map in abs_content:
    abs_content = abs_content.replace(old_slides_map, new_slides_map)
    with open(abs_file, "w", encoding="utf-8") as f:
        f.write(abs_content)
    print("generate_abstract_docx.py: Swapped Slide 3 and Slide 4 in table!")
else:
    print("Warning: could not find old_slides_map in generate_abstract_docx.py")
