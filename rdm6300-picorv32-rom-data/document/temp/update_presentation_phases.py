# -*- coding: utf-8 -*-
"""
Script to update create_presentation.py by adding Slide 8 (Chặng 1) and Slide 9 (Chặng 2),
renumbering slides 8-22 to 10-24, setting total_slides=24, and generating all 4 PPTX copies.
"""

import os
import re

def update_presentation():
    target_script = r"d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\create_presentation.py"
    with open(target_script, "r", encoding="utf-8") as f:
        src = f.read()

    # 1. Update total_slides=22 -> total_slides=24 in add_header definition
    src = src.replace("def add_header(slide, category, title, slide_num, total_slides=22):",
                      "def add_header(slide, category, title, slide_num, total_slides=24):")

    # 2. Add img_phase1 and img_phase2 image paths
    old_imgs = """    img_fig1 = os.path.join(cur_dir, "fig1_block_diagram.png")
    img_fig2 = os.path.join(cur_dir, "fig2_rdm6300_subsystem.png")
    img_fig2_h = os.path.join(cur_dir, "fig2_rdm6300_horizontal.png")
    img_openroad = os.path.join(project_root, "Openroad_1.png")
    img_signoff = os.path.join(project_root, "AntennaLvsDrc.png")"""

    new_imgs = """    img_fig1 = os.path.join(cur_dir, "fig1_block_diagram.png")
    img_fig2 = os.path.join(cur_dir, "fig2_rdm6300_subsystem.png")
    img_fig2_h = os.path.join(cur_dir, "fig2_rdm6300_horizontal.png")
    img_phase1 = os.path.join(cur_dir, "fig2_phase1_instruction_fetch.png")
    img_phase2 = os.path.join(cur_dir, "fig2_phase2_data_access.png")
    img_openroad = os.path.join(project_root, "Openroad_1.png")
    img_signoff = os.path.join(project_root, "AntennaLvsDrc.png")"""

    src = src.replace(old_imgs, new_imgs)

    # 3. Two new slides code
    new_slides_code = '''    # =========================================================================
    # SLIDE 8: CHẶNG 1: NẠP MÃ LỆNH TỪ SPI FLASH QUA SOC_INTERCONNECT (XIP)
    # =========================================================================
    s8_phase1 = prs.slides.add_slide(blank_layout)
    add_header(s8_phase1, "Chương 3 | Cơ chế thực thi bus liên kết", "Chu Trình Thực Thi: Chặng 1 - Nạp Mã Lệnh Từ SPI Flash (Instruction Fetch - XIP)", 8)

    # Left: High-Res Diagram Card
    if os.path.exists(img_phase1):
        p1_h = Inches(5.55)
        p1_w = Inches(7.15)
        p1_x = Inches(0.8)
        p1_y = Inches(1.35)
        add_card(s8_phase1, p1_x, p1_y, p1_w, p1_h, C_BLUE_ACCENT, C_WHITE)
        s8_phase1.shapes.add_picture(img_phase1, p1_x + Inches(0.08), p1_y + Inches(0.08), width=p1_w - Inches(0.16), height=p1_h - Inches(0.16))

    # Right: Technical Signal Interconnect Card
    p1_rw = Inches(4.38)
    p1_rx = Inches(8.15)
    add_card(s8_phase1, p1_rx, Inches(1.35), p1_rw, Inches(5.55), C_BLUE_ACCENT, C_CARD_BG)
    tb_p1 = s8_phase1.shapes.add_textbox(p1_rx + Inches(0.2), Inches(1.48), p1_rw - Inches(0.4), Inches(5.25))
    tf_p1 = tb_p1.text_frame
    tf_p1.word_wrap = True

    p_p1_0 = tf_p1.paragraphs[0]
    p_p1_0.text = "⚡ Luồng Tín Hiệu Nạp Lệnh (PC = 0x0025_0000)"
    p_p1_0.font.name = "Segoe UI"
    p_p1_0.font.size = Pt(13)
    p_p1_0.font.bold = True
    p_p1_0.font.color.rgb = C_BLUE_ACCENT
    p_p1_0.space_after = Pt(6)

    p1_steps = [
        ("Khai báo Top-Level rdm6300_picorv32_soc.v:", "CPU, Interconnect, Flash và SRAM được kết nối vật lý bằng các đường dây wire trung gian."),
        ("Bước 1: CPU phát chu kỳ nạp lệnh:", "rdm6300_picorv32_soc.v#mem_valid, #mem_addr (picorv32, soc_interconnect)\\n• mem_valid=1, mem_instr=1, mem_addr=0x0025_0000."),
        ("Bước 2: Giải mã địa chỉ trúng Flash:", "rdm6300_picorv32_soc.v#sel_spimem (soc_interconnect, spimemio)\\n• 0x0025_0000 thuộc 0x0010_0000..0x00FF_FFFF -> sel_spimem=1."),
        ("Bước 3: Flash trả về 4 byte mã máy:", "rdm6300_picorv32_soc.v#spimem_rdata, #spimem_ready (spimemio, soc_interconnect)\\n• Flash đọc 4 byte lệnh 'lw', báo spimem_ready=1."),
        ("Bước 4: Interconnect trả lệnh về CPU:", "rdm6300_picorv32_soc.v#mem_rdata, #mem_ready (soc_interconnect, picorv32)\\n• Ghép bus mem_rdata và mem_ready=1 để CPU chốt lệnh.")
    ]
    for st_h, st_t in p1_steps:
        p = tf_p1.add_paragraph()
        p.text = f"• {st_h}\\n"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.8)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(2)
        r = p.add_run()
        r.text = f"  {st_t}"
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED
        r.font.size = Pt(9.0)

    p_sram_idle = tf_p1.add_paragraph()
    p_sram_idle.text = "💡 Trạng thái SRAM: sel_sram = 0 (Khối SRAM nghỉ ngơi hoàn toàn, giảm công suất tiêu thụ động)."
    p_sram_idle.font.name = "Segoe UI"
    p_sram_idle.font.size = Pt(9.2)
    p_sram_idle.font.bold = True
    p_sram_idle.font.color.rgb = C_GREEN
    p_sram_idle.space_before = Pt(4)

    # =========================================================================
    # SLIDE 9: CHẶNG 2: TRUY XUẤT ĐỌC DỮ LIỆU BIẾN & NGĂN XẾP TỪ 1KB SRAM
    # =========================================================================
    s9_phase2 = prs.slides.add_slide(blank_layout)
    add_header(s9_phase2, "Chương 3 | Cơ chế thực thi bus liên kết", "Chu Trình Thực Thi: Chặng 2 - Truy Xuất Dữ Liệu Từ 1KB SRAM (Data Memory Access)", 9)

    # Left: High-Res Diagram Card
    if os.path.exists(img_phase2):
        p2_h = Inches(5.55)
        p2_w = Inches(7.3)
        p2_x = Inches(0.8)
        p2_y = Inches(1.35)
        add_card(s9_phase2, p2_x, p2_y, p2_w, p2_h, C_AMBER, C_WHITE)
        s9_phase2.shapes.add_picture(img_phase2, p2_x + Inches(0.08), p2_y + Inches(0.08), width=p2_w - Inches(0.16), height=p2_h - Inches(0.16))

    # Right: Technical Signal Interconnect Card
    p2_rw = Inches(4.23)
    p2_rx = Inches(8.3)
    add_card(s9_phase2, p2_rx, Inches(1.35), p2_rw, Inches(5.55), C_AMBER, C_CARD_BG)
    tb_p2 = s9_phase2.shapes.add_textbox(p2_rx + Inches(0.2), Inches(1.48), p2_rw - Inches(0.4), Inches(5.25))
    tf_p2 = tb_p2.text_frame
    tf_p2.word_wrap = True

    p_p2_0 = tf_p2.paragraphs[0]
    p_p2_0.text = "📦 Luồng Đọc Dữ Liệu SRAM (Stack = 0x0000_03F0)"
    p_p2_0.font.name = "Segoe UI"
    p_p2_0.font.size = Pt(13)
    p_p2_0.font.bold = True
    p_p2_0.font.color.rgb = C_AMBER
    p_p2_0.space_after = Pt(6)

    p2_steps = [
        ("Mục tiêu thực thi lệnh lw a0, 0(sp):", "Đọc dữ liệu 32-bit từ đỉnh Stack trong SRAM đưa vào thanh ghi a0 của CPU."),
        ("Bước 1: CPU phát chu kỳ đọc dữ liệu:", "rdm6300_picorv32_soc.v#mem_valid, #mem_addr (picorv32, soc_interconnect)\\n• mem_valid=1, mem_instr=0, mem_addr=0x0000_03F0."),
        ("Bước 2: Giải mã địa chỉ trúng SRAM:", "rdm6300_picorv32_soc.v#sel_sram (soc_interconnect, data_sram)\\n• Địa chỉ < 0x0000_0400 -> sel_sram=1, sel_spimem=0."),
        ("Bước 3: SRAM phản hồi trong 1 chu kỳ:", "rdm6300_picorv32_soc.v#sram_rdata, #sram_ready (data_sram, soc_interconnect)\\n• Đọc word 32-bit tại offset [9:0], báo sram_ready=1."),
        ("Bước 4: CPU chốt dữ liệu vào thanh ghi:", "rdm6300_picorv32_soc.v#mem_rdata, #mem_ready (soc_interconnect, picorv32)\\n• Chuyển sram_rdata vào thanh ghi a0 trong đúng 1 chu kỳ.")
    ]
    for st_h, st_t in p2_steps:
        p = tf_p2.add_paragraph()
        p.text = f"• {st_h}\\n"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.8)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(2)
        r = p.add_run()
        r.text = f"  {st_t}"
        r.font.bold = False
        r.font.color.rgb = C_TEXT_MUTED
        r.font.size = Pt(9.0)

    p_flash_idle = tf_p2.add_paragraph()
    p_flash_idle.text = "💡 Trạng thái Flash: sel_spimem = 0 (Chip Flash nghỉ ngơi, chân SPI CS_N giữ mức cao 1'b1)."
    p_flash_idle.font.name = "Segoe UI"
    p_flash_idle.font.size = Pt(9.2)
    p_flash_idle.font.bold = True
    p_flash_idle.font.color.rgb = C_BLUE_ACCENT
    p_flash_idle.space_before = Pt(4)

'''

    # Insert new slides before old Slide 8
    target_marker = "    # =========================================================================\n    # SLIDE 8:"
    if target_marker in src:
        src = src.replace(target_marker, new_slides_code + target_marker)
    else:
        print("[ERROR] Could not find target_marker for Slide 8")
        return False

    # 4. Renumber old slides 8..22 to 10..24
    # Pattern: # SLIDE X: -> # SLIDE (X+2):
    # and add_header(..., X) -> add_header(..., X+2)
    # We must do this from 22 down to 8 to avoid collision
    for old_num in range(22, 7, -1):
        new_num = old_num + 2
        # Replace header comment
        src = src.replace(f"# SLIDE {old_num}:", f"# SLIDE {new_num}:")
        # Replace add_header call
        # e.g., add_header(s8, "Chương 3 | Ngoại vi thu nhận RFID", "3.5. Bước 5: Đường Ống 5 Giai Đoạn Thu Nhận & Giải Mã Phần Cứng (Hình 2)", 8)
        src = re.sub(rf"(add_header\([^)]+,\s*){old_num}(\))", rf"\g<1>{new_num}\2", src)

    # Also update save presentation to save to all locations
    old_save = """    # Save Presentation to document/ directory
    out_pptx_1 = os.path.join(doc_dir, "Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.pptx")
    out_pptx_2 = os.path.join(doc_dir, "Bao_Cao_Do_An_RDM6300_PicoRV32_SoC_v2.pptx")
    prs.save(out_pptx_1)
    prs.save(out_pptx_2)
    print(f"[SUCCESS] Comprehensive 22-Slide PPTX generated successfully at:")
    print(f"  - {out_pptx_1}")
    print(f"  - {out_pptx_2}")"""

    new_save = """    # Save Presentation to all directories
    targets = [
        os.path.join(doc_dir, "Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.pptx"),
        os.path.join(doc_dir, "Bao_Cao_Do_An_RDM6300_PicoRV32_SoC_v2.pptx"),
        os.path.join(cur_dir, "Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.pptx"),
        os.path.join(cur_dir, "Bao_Cao_Do_An_RDM6300_PicoRV32_SoC_v2.pptx"),
    ]
    for p in targets:
        try:
            prs.save(p)
            print(f"[SUCCESS] Saved PPTX at: {p}")
        except Exception as e:
            print(f"[NOTE] Could not save to {p}: {e}")"""

    src = src.replace(old_save, new_save)

    # Write updated script
    with open(target_script, "w", encoding="utf-8") as f:
        f.write(src)

    print("[SUCCESS] Successfully updated create_presentation.py with 24 slides!")
    return True

if __name__ == "__main__":
    update_presentation()
