# -*- coding: utf-8 -*-
"""
Script: update_documents_diagram.py
Updates the embedded Hình 1 (SoC Architecture Block Diagram) in:
- document/Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.docx
- document/Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.pptx
- document/Bao_Cao_Do_An_RDM6300_PicoRV32_SoC_v2.docx
- document/Bao_Cao_Do_An_RDM6300_PicoRV32_SoC_v2.pptx

Replaces image1.png with the new high-resolution render of fig1_block_diagram.png.
"""

import os
import zipfile
import shutil

def replace_image_in_zip(zip_path, target_entry, new_image_path):
    if not os.path.exists(zip_path):
        print(f"[SKIP] File not found: {zip_path}")
        return False
    
    with open(new_image_path, "rb") as f:
        new_data = f.read()

    temp_zip_path = zip_path + ".tmp"
    with zipfile.ZipFile(zip_path, "r") as zin:
        with zipfile.ZipFile(temp_zip_path, "w", compression=zin.compression) as zout:
            for item in zin.infolist():
                if item.filename == target_entry:
                    zout.writestr(item, new_data)
                else:
                    zout.writestr(item, zin.read(item.filename))

    shutil.move(temp_zip_path, zip_path)
    print(f"[SUCCESS] Replaced {target_entry} in {os.path.basename(zip_path)} ({len(new_data)} bytes)")
    return True

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    new_image = os.path.join(base_dir, "document", "temp", "fig1_block_diagram.png")
    
    if not os.path.exists(new_image):
        print(f"[ERROR] Source image not found: {new_image}")
        return

    targets = [
        ("document/Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.docx", "word/media/image1.png"),
        ("document/Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.pptx", "ppt/media/image1.png"),
        ("document/Bao_Cao_Do_An_RDM6300_PicoRV32_SoC_v2.docx", "word/media/image1.png"),
        ("document/Bao_Cao_Do_An_RDM6300_PicoRV32_SoC_v2.pptx", "ppt/media/image1.png"),
    ]

    for rel_path, entry in targets:
        full_path = os.path.join(base_dir, rel_path)
        replace_image_in_zip(full_path, entry, new_image)

if __name__ == "__main__":
    main()
