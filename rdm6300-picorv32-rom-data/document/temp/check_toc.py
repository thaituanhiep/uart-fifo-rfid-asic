# -*- coding: utf-8 -*-
import docx

doc = docx.Document('Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.docx')
with open('toc_check.txt', 'w', encoding='utf-8') as f:
    for i, p in enumerate(doc.paragraphs[:40]):
        f.write(f"P{i} [indent={p.paragraph_format.left_indent}]: {p.text}\n")
print("Done writing toc_check.txt")
