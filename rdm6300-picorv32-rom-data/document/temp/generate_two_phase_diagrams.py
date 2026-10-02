# -*- coding: utf-8 -*-
"""
generate_two_phase_diagrams.py
Generates the two large, crisp, prominent sequence diagrams:
1. Fig 3: Chặng 1 - Nạp mã lệnh từ Flash qua bus soc_interconnect (Instruction Fetch - XIP)
   - rdm6300_soc_phase1_instruction_fetch.drawio
   - rdm6300_soc_phase1_instruction_fetch.svg
   - document/temp/fig2_phase1_instruction_fetch.png
2. Fig 4: Chặng 2 - Truy xuất đọc dữ liệu biến và ngăn xếp từ 1KB Data SRAM (Data Memory Access)
   - rdm6300_soc_phase2_data_access.drawio
   - rdm6300_soc_phase2_data_access.svg
   - document/temp/fig2_phase2_data_access.png

Features:
- Extra-large fonts (20px body, 23px step titles, 24px column headers, 28px main titles, 21px bold arrow badges)
- Box width 560px with generous margins, ensuring ZERO text clipping or border overflow
- Exact signal names: rdm6300_picorv32_soc.v#tên_biến (module_nguồn ➔ module_đích)
- Professional draw.io XML + crisp SVG + 2x Retina PNG rendering via Chrome Headless
"""

import os
import subprocess
import shutil

PROJECT_DIR = r"d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data"
DOC_DIR     = os.path.join(PROJECT_DIR, "document")
TEMP_DIR    = os.path.join(DOC_DIR, "temp")
ARTIFACT_DIR = r"C:\Users\thait\.gemini\antigravity-ide\brain\40d01579-3c16-4b85-9b12-c0e7d33bcd21"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

os.makedirs(TEMP_DIR, exist_ok=True)

# Layout constants
WIDTH = 1800
COL1_X = 300
COL2_X = 900
COL3_X = 1500
BOX_W  = 560

# =============================================================================
# 1. PHASE 1: INSTRUCTION FETCH (XIP)
# =============================================================================
def generate_phase1():
    print("\n=== Generating Phase 1 Diagram (Extra-Large Fonts, High Visibility) ===")
    
    H = 1865
    drawio_path = os.path.join(TEMP_DIR, "rdm6300_soc_phase1_instruction_fetch.drawio")
    svg_path    = os.path.join(TEMP_DIR, "rdm6300_soc_phase1_instruction_fetch.svg")
    png_path    = os.path.join(TEMP_DIR, "fig2_phase1_instruction_fetch.png")

    steps = [
        {
            "num": 1,
            "col": 1,
            "x": COL1_X - BOX_W // 2,
            "y": 320,
            "w": BOX_W,
            "h": 170,
            "title": "Bước 1: CPU phát chu kỳ nạp mã lệnh",
            "lines": [
                "• mem_valid = 1 & mem_instr = 1 (Nạp mã máy)",
                "• mem_addr = 0x0025_0000 (Địa chỉ PC nạp lệnh)",
                "• mem_wstrb = 4'b0000 (Chu kỳ đọc, không ghi)"
            ]
        },
        {
            "num": 2,
            "col": 2,
            "x": COL2_X - BOX_W // 2,
            "y": 620,
            "w": BOX_W,
            "h": 170,
            "title": "Bước 2: Interconnect giải mã & chọn Flash",
            "lines": [
                "• So khớp: 32'h0025_0000 ∈ [Flash 0x0010_0000..]",
                "• Bật sel_spimem = 1 (Kích hoạt bộ điều khiển Flash)",
                "• Khóa sel_sram = 0 (Khối 1KB SRAM nghỉ ngơi)"
            ]
        },
        {
            "num": 3,
            "col": 3,
            "x": COL3_X - BOX_W // 2,
            "y": 920,
            "w": BOX_W,
            "h": 170,
            "title": "Bước 3: spimemio phát xung SPI đọc Flash",
            "lines": [
                "• FSM kéo flash_csb = 0, phát chuỗi xung flash_clk",
                "• Fast Read phát qua io0, nhận dữ liệu qua io1",
                "• CPU rơi vào Stall (cpu_state = Stall trong picorv32.v)"
            ]
        },
        {
            "num": 4,
            "col": 3,
            "x": COL3_X - BOX_W // 2,
            "y": 1115,
            "w": BOX_W,
            "h": 135,
            "title": "Bước 4: Flash trả về từ mã máy 32-bit",
            "lines": [
                "• spimem_rdata = Mã opcode 32-bit của lệnh 'lw'",
                "• Bật spimem_ready = 1 (Hoàn tất đọc 4 byte Flash)"
            ]
        },
        {
            "num": 5,
            "col": 2,
            "x": COL2_X - BOX_W // 2,
            "y": 1380,
            "w": BOX_W,
            "h": 135,
            "title": "Bước 5: Interconnect ghép mã lệnh về CPU",
            "lines": [
                "• mem_rdata = spimem_rdata (Chuyển mã lệnh về CPU)",
                "• mem_ready = spimem_ready = 1 (Báo CPU chốt lệnh)"
            ]
        },
        {
            "num": 6,
            "col": 1,
            "x": COL1_X - BOX_W // 2,
            "y": 1645,
            "w": BOX_W,
            "h": 170,
            "title": "Bước 6: CPU nhận mã lệnh vào IR & Giải phóng",
            "lines": [
                "• Chốt reg_op = mem_rdata (Thanh ghi lệnh IR)",
                "• Hạ mem_valid = 0 (Kết thúc chu kỳ bus nạp lệnh)",
                "• CHẶNG 1 HOÀN TẤT (MÃ LỆNH ĐÃ VÀO CPU)!"
            ]
        }
    ]

    arrows = [
        {
            "from_x": COL1_X, "to_x": COL2_X, "y": 560,
            "line1": "rdm6300_picorv32_soc.v#mem_valid, #mem_addr",
            "line2": "(từ picorv32 ➔ soc_interconnect)"
        },
        {
            "from_x": COL2_X, "to_x": COL3_X, "y": 860,
            "line1": "rdm6300_picorv32_soc.v#sel_spimem",
            "line2": "(từ soc_interconnect ➔ spimemio)"
        },
        {
            "from_x": COL3_X, "to_x": COL2_X, "y": 1320,
            "line1": "rdm6300_picorv32_soc.v#spimem_rdata, #spimem_ready",
            "line2": "(từ spimemio ➔ soc_interconnect)"
        },
        {
            "from_x": COL2_X, "to_x": COL1_X, "y": 1585,
            "line1": "rdm6300_picorv32_soc.v#mem_rdata, #mem_ready",
            "line2": "(từ soc_interconnect ➔ picorv32)"
        }
    ]

    # --- Draw.io XML ---
    cells = []
    cell_id = 2

    # Title Box
    cells.append(f'''<mxCell id="{cell_id}" value="&lt;b style=&quot;font-size:26px;&quot;&gt;CHẶNG 1: NẠP MÃ LỆNH TỪ SPI FLASH QUA SOC_INTERCONNECT (INSTRUCTION FETCH - XIP)&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:18px;color:#444;&quot;&gt;Ví dụ: Nạp mã lệnh lw a0, 0(sp) tại PC = 0x0025_0000 — Tín hiệu trên các mũi tên: rdm6300_picorv32_soc.v#tên_biến (module nguồn, module đích)&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;" vertex="1" parent="1">
  <mxGeometry x="20" y="20" width="{WIDTH - 40}" height="80" as="geometry"/>
</mxCell>''')
    cell_id += 1

    # Column Headers
    headers = [
        (COL1_X - BOX_W//2, "CỘT 1: PicoRV32 CPU (MASTER)", "File nguồn: rtl/core/picorv32.v", "Phát chu kỳ bus: mem_valid, mem_addr, mem_wstrb"),
        (COL2_X - BOX_W//2, "CỘT 2: soc_interconnect (TRỌNG TÀI BUS)", "File nguồn: rtl/core/soc_interconnect.v", "Giải mã địa chỉ, bật sel_spimem = 1, ghép cpu_mem_rdata"),
        (COL3_X - BOX_W//2, "CỘT 3: BỘ ĐIỀU KHIỂN SPI FLASH (SLAVE 1)", "File nguồn: rtl/core/spimemio.v (Chip Flash W25Q128)", "Dải địa chỉ Flash: 0x0010_0000 - 0x00FF_FFFF")
    ]
    for hx, htitle, hsub1, hsub2 in headers:
        val = f"&lt;b style=&quot;font-size:22px;&quot;&gt;{htitle}&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:17px;color:#333;&quot;&gt;{hsub1}&lt;br/&gt;{hsub2}&lt;/span&gt;"
        cells.append(f'''<mxCell id="{cell_id}" value="{val}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;" vertex="1" parent="1">
  <mxGeometry x="{hx}" y="115" width="{BOX_W}" height="115" as="geometry"/>
</mxCell>''')
        cell_id += 1

    # Lifelines
    for col_x in [COL1_X, COL2_X, COL3_X]:
        cells.append(f'''<mxCell id="{cell_id}" value="" style="endArrow=none;dashed=1;html=1;strokeWidth=2;strokeColor=#888888;" edge="1" parent="1">
  <mxGeometry width="50" height="50" relative="1" as="geometry">
    <mxPoint x="{col_x}" y="1845" as="sourcePoint"/>
    <mxPoint x="{col_x}" y="230" as="targetPoint"/>
  </mxGeometry>
</mxCell>''')
        cell_id += 1

    # Note Banner
    note_val = "&lt;b style=&quot;font-size:19px;&quot;&gt;[GHI CHÚ] Khối 1KB SRAM nghỉ ngơi do sel_sram = 0 (Bộ nhớ SRAM không hoạt động trong chu kỳ nạp lệnh)&lt;/b&gt;"
    cells.append(f'''<mxCell id="{cell_id}" value="{note_val}" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;" vertex="1" parent="1">
  <mxGeometry x="20" y="245" width="{WIDTH - 40}" height="55" as="geometry"/>
</mxCell>''')
    cell_id += 1

    # Steps
    for b in steps:
        lines_str = "<br/>".join([f"&lt;span style=&quot;font-size:18px;&quot;&gt;{l}&lt;/span&gt;" for l in b["lines"]])
        b_val = f"&lt;b style=&quot;font-size:21px;&quot;&gt;{b['title']}&lt;/b&gt;&lt;br/&gt;{lines_str}"
        cells.append(f'''<mxCell id="{cell_id}" value="{b_val}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2.5;align=left;spacingLeft=16;spacingRight=16;" vertex="1" parent="1">
  <mxGeometry x="{b['x']}" y="{b['y']}" width="{b['w']}" height="{b['h']}" as="geometry"/>
</mxCell>''')
        cell_id += 1

    # Arrows
    for a in arrows:
        lbl = f"&lt;b style=&quot;font-size:19px;&quot;&gt;{a['line1']}&lt;br/&gt;{a['line2']}&lt;/b&gt;"
        cells.append(f'''<mxCell id="{cell_id}" value="{lbl}" style="endArrow=classic;html=1;strokeWidth=3.5;strokeColor=#000000;labelBackgroundColor=#ffffff;align=center;" edge="1" parent="1">
  <mxGeometry width="50" height="50" relative="1" as="geometry">
    <mxPoint x="{a['from_x']}" y="{a['y']}" as="sourcePoint"/>
    <mxPoint x="{a['to_x']}" y="{a['y']}" as="targetPoint"/>
  </mxGeometry>
</mxCell>''')
        cell_id += 1

    xml_content = f'''<mxfile host="Electron" modified="2026-10-02T00:00:00.000Z" agent="Antigravity" version="21.0.0" type="device">
  <diagram id="phase1_instruction_fetch" name="Chặng 1: Nạp mã lệnh (XIP)">
    <mxGraphModel dx="{WIDTH}" dy="{H}" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{WIDTH}" pageHeight="{H}" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        {"".join(cells)}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''

    with open(drawio_path, "w", encoding="utf-8") as f:
        f.write(xml_content)
    print(f"[OK] Generated Phase 1 Draw.io: {drawio_path}")

    # --- SVG Generation ---
    svg_elements = []
    
    # Title Box
    svg_elements.append(f'''  <rect x="20" y="20" width="{WIDTH - 40}" height="80" fill="#ffffff" stroke="#000000" stroke-width="2.5" rx="6"/>
  <text x="{WIDTH // 2}" y="54" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" fill="#000000" text-anchor="middle">CHẶNG 1: NẠP MÃ LỆNH TỪ SPI FLASH QUA SOC_INTERCONNECT (INSTRUCTION FETCH - XIP)</text>
  <text x="{WIDTH // 2}" y="84" font-family="Arial, Helvetica, sans-serif" font-size="19" fill="#444444" text-anchor="middle">Ví dụ: Nạp mã lệnh lw a0, 0(sp) tại PC = 0x0025_0000 — Tín hiệu trên các mũi tên: rdm6300_picorv32_soc.v#tên_biến (module nguồn, module đích)</text>''')

    # Column Headers
    for hx, htitle, hsub1, hsub2 in headers:
        svg_elements.append(f'''  <rect x="{hx}" y="115" width="{BOX_W}" height="115" fill="#ffffff" stroke="#000000" stroke-width="2.5" rx="6"/>
  <text x="{hx + BOX_W // 2}" y="150" font-family="Arial, Helvetica, sans-serif" font-size="23" font-weight="bold" fill="#000000" text-anchor="middle">{htitle}</text>
  <text x="{hx + BOX_W // 2}" y="180" font-family="Arial, Helvetica, sans-serif" font-size="18" fill="#444444" text-anchor="middle">{hsub1}</text>
  <text x="{hx + BOX_W // 2}" y="208" font-family="Arial, Helvetica, sans-serif" font-size="18" fill="#444444" text-anchor="middle">{hsub2}</text>''')

    # Lifelines
    for col_x in [COL1_X, COL2_X, COL3_X]:
        svg_elements.append(f'  <line x1="{col_x}" y1="230" x2="{col_x}" y2="1845" stroke="#888888" stroke-width="2" stroke-dasharray="8,8"/>')

    # Note Banner
    svg_elements.append(f'''  <rect x="20" y="245" width="{WIDTH - 40}" height="55" fill="#ffffff" stroke="#000000" stroke-width="2" rx="4"/>
  <text x="{WIDTH // 2}" y="280" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" fill="#000000" text-anchor="middle">[GHI CHÚ] Khối 1KB SRAM nghỉ ngơi do sel_sram = 0 (Bộ nhớ SRAM không hoạt động trong chu kỳ nạp lệnh)</text>''')

    # Steps
    for b in steps:
        svg_elements.append(f'''  <rect x="{b['x']}" y="{b['y']}" width="{b['w']}" height="{b['h']}" fill="#ffffff" stroke="#000000" stroke-width="2.5" rx="6"/>
  <text x="{b['x'] + 22}" y="{b['y'] + 36}" font-family="Arial, Helvetica, sans-serif" font-size="23" font-weight="bold" fill="#000000">{b['title']}</text>
  <line x1="{b['x'] + 15}" y1="{b['y'] + 48}" x2="{b['x'] + b['w'] - 15}" y2="{b['y'] + 48}" stroke="#e2e8f0" stroke-width="1.5"/>''')
        curr_y = b['y'] + 80
        for line in b['lines']:
            svg_elements.append(f'  <text x="{b["x"] + 22}" y="{curr_y}" font-family="Arial, Helvetica, sans-serif" font-size="20" fill="#111111">{line}</text>')
            curr_y += 34

    # Arrows
    for a in arrows:
        mid_x = (a['from_x'] + a['to_x']) // 2
        # Arrow line
        svg_elements.append(f'  <line x1="{a["from_x"]}" y1="{a["y"]}" x2="{a["to_x"]}" y2="{a["y"]}" stroke="#000000" stroke-width="3.5" marker-end="url(#arrowhead)"/>')
        # Background badge for label
        svg_elements.append(f'''  <rect x="{mid_x - 260}" y="{a['y'] - 54}" width="520" height="44" fill="#ffffff" fill-opacity="0.96" stroke="#b0b0b0" stroke-width="1.2" rx="5"/>
  <text x="{mid_x}" y="{a['y'] - 31}" font-family="Arial, Helvetica, sans-serif" font-size="19" font-weight="bold" fill="#000000" text-anchor="middle">{a['line1']}</text>
  <text x="{mid_x}" y="{a['y'] - 13}" font-family="Arial, Helvetica, sans-serif" font-size="17" font-weight="bold" fill="#2b6cb0" text-anchor="middle">{a['line2']}</text>''')

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {H}" width="{WIDTH}" height="{H}">
  <defs>
    <marker id="arrowhead" markerWidth="14" markerHeight="10" refX="12" refY="5" orient="auto">
      <polygon points="0 0, 14 5, 0 10" fill="#000000" />
    </marker>
  </defs>
  <rect width="{WIDTH}" height="{H}" fill="#ffffff"/>
{"\n".join(svg_elements)}
</svg>'''

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"[OK] Generated Phase 1 SVG: {svg_path}")

    # Render PNG with Chrome Headless
    html_temp = os.path.join(TEMP_DIR, "_temp_phase1.html")
    with open(html_temp, "w", encoding="utf-8") as f:
        f.write(f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: #ffffff; width: {WIDTH}px; height: {H}px; overflow: hidden; }}
</style>
</head>
<body>
{svg_content}
</body>
</html>''')

    cmd = [
        CHROME_PATH,
        "--headless",
        "--disable-gpu",
        "--force-device-scale-factor=2",
        f"--window-size={WIDTH},{H}",
        f"--screenshot={png_path}",
        html_temp
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if os.path.exists(html_temp):
        os.remove(html_temp)
    print(f"[OK] Rendered High-Res PNG: {png_path}")

    # Sync to brain artifacts
    if os.path.exists(ARTIFACT_DIR):
        shutil.copy2(png_path, os.path.join(ARTIFACT_DIR, "fig2_phase1_instruction_fetch.png"))
        print("[OK] Synced artifact: fig2_phase1_instruction_fetch.png")


# =============================================================================
# 2. PHASE 2: DATA ACCESS (SRAM)
# =============================================================================
def generate_phase2():
    print("\n=== Generating Phase 2 Diagram (Extra-Large Fonts, High Visibility) ===")
    
    H = 1740
    drawio_path = os.path.join(TEMP_DIR, "rdm6300_soc_phase2_data_access.drawio")
    svg_path    = os.path.join(TEMP_DIR, "rdm6300_soc_phase2_data_access.svg")
    png_path    = os.path.join(TEMP_DIR, "fig2_phase2_data_access.png")

    steps = [
        {
            "num": 7,
            "col": 1,
            "x": COL1_X - BOX_W // 2,
            "y": 320,
            "w": BOX_W,
            "h": 170,
            "title": "Bước 7: CPU phát chu kỳ đọc Stack SRAM",
            "lines": [
                "• mem_valid = 1 & mem_instr = 0 (Đọc dữ liệu)",
                "• mem_addr = 0x0000_03F0 (Địa chỉ đỉnh Stack)",
                "• mem_wstrb = 4'b0000 (Chu kỳ đọc, không ghi)"
            ]
        },
        {
            "num": 8,
            "col": 2,
            "x": COL2_X - BOX_W // 2,
            "y": 620,
            "w": BOX_W,
            "h": 170,
            "title": "Bước 8: Interconnect giải mã chọn SRAM",
            "lines": [
                "• So khớp: 32'h0000_03F0 < 32'h0000_0400",
                "• Bật sel_sram = 1 (Kích hoạt khối 1KB Data SRAM)",
                "• Khóa sel_spimem = 0 (Bộ điều khiển Flash nghỉ)"
            ]
        },
        {
            "num": 9,
            "col": 3,
            "x": COL3_X - BOX_W // 2,
            "y": 920,
            "w": BOX_W,
            "h": 170,
            "title": "Bước 9: SRAM đọc ô nhớ & Phản hồi (1 cycle)",
            "lines": [
                "• Đọc mem[addr] trong rtl/data_sram.v (Stack 0x3F0)",
                "• sram_rdata = Giá trị biến local_var từ Stack",
                "• sram_ready = 1 (Phản hồi tức thì trong 1 cycle 20ns)"
            ]
        },
        {
            "num": 10,
            "col": 2,
            "x": COL2_X - BOX_W // 2,
            "y": 1220,
            "w": BOX_W,
            "h": 135,
            "title": "Bước 10: Interconnect ghép dữ liệu về CPU",
            "lines": [
                "• mem_rdata = sram_rdata (Chuyển dữ liệu biến)",
                "• mem_ready = sram_ready = 1 (Báo CPU chốt)"
            ]
        },
        {
            "num": 11,
            "col": 1,
            "x": COL1_X - BOX_W // 2,
            "y": 1485,
            "w": BOX_W,
            "h": 205,
            "title": "Bước 11: CPU chốt dữ liệu vào a0 & Hoàn tất",
            "lines": [
                "• Ghi cpuregs[10] = mem_rdata (Thanh ghi a0/x10)",
                "• Hạ mem_valid = 0 (Kết thúc chu kỳ đọc dữ liệu)",
                "• Tăng reg_pc = reg_pc + 4 (Chuyển sang lệnh kế)",
                "• LỆNH FIRMWARE HOÀN TẤT THỰC THI 100%!"
            ]
        }
    ]

    arrows = [
        {
            "from_x": COL1_X, "to_x": COL2_X, "y": 560,
            "line1": "rdm6300_picorv32_soc.v#mem_valid, #mem_addr",
            "line2": "(từ picorv32 ➔ soc_interconnect)"
        },
        {
            "from_x": COL2_X, "to_x": COL3_X, "y": 860,
            "line1": "rdm6300_picorv32_soc.v#sel_sram",
            "line2": "(từ soc_interconnect ➔ data_sram)"
        },
        {
            "from_x": COL3_X, "to_x": COL2_X, "y": 1160,
            "line1": "rdm6300_picorv32_soc.v#sram_rdata, #sram_ready",
            "line2": "(từ data_sram ➔ soc_interconnect)"
        },
        {
            "from_x": COL2_X, "to_x": COL1_X, "y": 1425,
            "line1": "rdm6300_picorv32_soc.v#mem_rdata, #mem_ready",
            "line2": "(từ soc_interconnect ➔ picorv32)"
        }
    ]

    # --- Draw.io XML ---
    cells = []
    cell_id = 2

    # Title Box
    cells.append(f'''<mxCell id="{cell_id}" value="&lt;b style=&quot;font-size:26px;&quot;&gt;CHẶNG 2: TRUY XUẤT DỮ LIỆU TỪ SRAM QUA SOC_INTERCONNECT (DATA MEMORY ACCESS)&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:18px;color:#444;&quot;&gt;Ví dụ: Lệnh lw a0, 0(sp) đọc biến local_var từ đỉnh Stack sp = 0x0000_03F0 — Tín hiệu trên các mũi tên: rdm6300_picorv32_soc.v#tên_biến (module nguồn, module đích)&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;" vertex="1" parent="1">
  <mxGeometry x="20" y="20" width="{WIDTH - 40}" height="80" as="geometry"/>
</mxCell>''')
    cell_id += 1

    # Column Headers
    headers = [
        (COL1_X - BOX_W//2, "CỘT 1: PicoRV32 CPU (MASTER)", "File nguồn: rtl/core/picorv32.v", "Giải mã opcode, phát chu kỳ đọc Stack: mem_valid, mem_addr"),
        (COL2_X - BOX_W//2, "CỘT 2: soc_interconnect (TRỌNG TÀI BUS)", "File nguồn: rtl/core/soc_interconnect.v", "Giải mã địa chỉ, bật sel_sram = 1, ghép sram_rdata về CPU"),
        (COL3_X - BOX_W//2, "CỘT 3: 1KB ON-CHIP DATA SRAM (SLAVE 0)", "File nguồn: rtl/core/data_sram.v (256 từ x 32-bit = 1024 Bytes)", "Dải địa chỉ SRAM: 0x0000_0000 - 0x0000_03FF")
    ]
    for hx, htitle, hsub1, hsub2 in headers:
        val = f"&lt;b style=&quot;font-size:22px;&quot;&gt;{htitle}&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:17px;color:#333;&quot;&gt;{hsub1}&lt;br/&gt;{hsub2}&lt;/span&gt;"
        cells.append(f'''<mxCell id="{cell_id}" value="{val}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;" vertex="1" parent="1">
  <mxGeometry x="{hx}" y="115" width="{BOX_W}" height="115" as="geometry"/>
</mxCell>''')
        cell_id += 1

    # Lifelines
    for col_x in [COL1_X, COL2_X, COL3_X]:
        cells.append(f'''<mxCell id="{cell_id}" value="" style="endArrow=none;dashed=1;html=1;strokeWidth=2;strokeColor=#888888;" edge="1" parent="1">
  <mxGeometry width="50" height="50" relative="1" as="geometry">
    <mxPoint x="{col_x}" y="1720" as="sourcePoint"/>
    <mxPoint x="{col_x}" y="230" as="targetPoint"/>
  </mxGeometry>
</mxCell>''')
        cell_id += 1

    # Note Banner
    note_val = "&lt;b style=&quot;font-size:19px;&quot;&gt;[TIỀN ĐỀ] ALU tính addr = 32'h0000_03F0 (SRAM). Khối Flash nghỉ ngơi do sel_spimem = 0 (CS_N giữ mức cao 1'b1)&lt;/b&gt;"
    cells.append(f'''<mxCell id="{cell_id}" value="{note_val}" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;" vertex="1" parent="1">
  <mxGeometry x="20" y="245" width="{WIDTH - 40}" height="55" as="geometry"/>
</mxCell>''')
    cell_id += 1

    # Steps
    for b in steps:
        lines_str = "<br/>".join([f"&lt;span style=&quot;font-size:18px;&quot;&gt;{l}&lt;/span&gt;" for l in b["lines"]])
        b_val = f"&lt;b style=&quot;font-size:21px;&quot;&gt;{b['title']}&lt;/b&gt;&lt;br/&gt;{lines_str}"
        cells.append(f'''<mxCell id="{cell_id}" value="{b_val}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2.5;align=left;spacingLeft=16;spacingRight=16;" vertex="1" parent="1">
  <mxGeometry x="{b['x']}" y="{b['y']}" width="{b['w']}" height="{b['h']}" as="geometry"/>
</mxCell>''')
        cell_id += 1

    # Arrows
    for a in arrows:
        lbl = f"&lt;b style=&quot;font-size:19px;&quot;&gt;{a['line1']}&lt;br/&gt;{a['line2']}&lt;/b&gt;"
        cells.append(f'''<mxCell id="{cell_id}" value="{lbl}" style="endArrow=classic;html=1;strokeWidth=3.5;strokeColor=#000000;labelBackgroundColor=#ffffff;align=center;" edge="1" parent="1">
  <mxGeometry width="50" height="50" relative="1" as="geometry">
    <mxPoint x="{a['from_x']}" y="{a['y']}" as="sourcePoint"/>
    <mxPoint x="{a['to_x']}" y="{a['y']}" as="targetPoint"/>
  </mxGeometry>
</mxCell>''')
        cell_id += 1

    xml_content = f'''<mxfile host="Electron" modified="2026-10-02T00:00:00.000Z" agent="Antigravity" version="21.0.0" type="device">
  <diagram id="phase2_data_access" name="Chặng 2: Truy xuất dữ liệu (Data Access)">
    <mxGraphModel dx="{WIDTH}" dy="{H}" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{WIDTH}" pageHeight="{H}" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        {"".join(cells)}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''

    with open(drawio_path, "w", encoding="utf-8") as f:
        f.write(xml_content)
    print(f"[OK] Generated Phase 2 Draw.io: {drawio_path}")

    # --- SVG Generation ---
    svg_elements = []
    
    # Title Box
    svg_elements.append(f'''  <rect x="20" y="20" width="{WIDTH - 40}" height="80" fill="#ffffff" stroke="#000000" stroke-width="2.5" rx="6"/>
  <text x="{WIDTH // 2}" y="54" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" fill="#000000" text-anchor="middle">CHẶNG 2: TRUY XUẤT DỮ LIỆU TỪ 1KB SRAM (DATA MEMORY ACCESS)</text>
  <text x="{WIDTH // 2}" y="84" font-family="Arial, Helvetica, sans-serif" font-size="19" fill="#444444" text-anchor="middle">Ví dụ: Lệnh lw a0, 0(sp) đọc biến local_var từ đỉnh Stack sp = 0x0000_03F0 — rdm6300_picorv32_soc.v#tên_biến (module nguồn, module đích)</text>''')

    # Column Headers
    for hx, htitle, hsub1, hsub2 in headers:
        svg_elements.append(f'''  <rect x="{hx}" y="115" width="{BOX_W}" height="115" fill="#ffffff" stroke="#000000" stroke-width="2.5" rx="6"/>
  <text x="{hx + BOX_W // 2}" y="150" font-family="Arial, Helvetica, sans-serif" font-size="23" font-weight="bold" fill="#000000" text-anchor="middle">{htitle}</text>
  <text x="{hx + BOX_W // 2}" y="180" font-family="Arial, Helvetica, sans-serif" font-size="18" fill="#444444" text-anchor="middle">{hsub1}</text>
  <text x="{hx + BOX_W // 2}" y="208" font-family="Arial, Helvetica, sans-serif" font-size="18" fill="#444444" text-anchor="middle">{hsub2}</text>''')

    # Lifelines
    for col_x in [COL1_X, COL2_X, COL3_X]:
        svg_elements.append(f'  <line x1="{col_x}" y1="230" x2="{col_x}" y2="1720" stroke="#888888" stroke-width="2" stroke-dasharray="8,8"/>')

    # Note Banner
    svg_elements.append(f'''  <rect x="20" y="245" width="{WIDTH - 40}" height="55" fill="#ffffff" stroke="#000000" stroke-width="2" rx="4"/>
  <text x="{WIDTH // 2}" y="280" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" fill="#000000" text-anchor="middle">[TIỀN ĐỀ] ALU tính addr = 32'h0000_03F0 (SRAM). SPI Flash nghỉ ngơi: sel_spimem = 0 (CS_N giữ mức cao 1'b1)</text>''')

    # Steps
    for b in steps:
        svg_elements.append(f'''  <rect x="{b['x']}" y="{b['y']}" width="{b['w']}" height="{b['h']}" fill="#ffffff" stroke="#000000" stroke-width="2.5" rx="6"/>
  <text x="{b['x'] + 22}" y="{b['y'] + 36}" font-family="Arial, Helvetica, sans-serif" font-size="23" font-weight="bold" fill="#000000">{b['title']}</text>
  <line x1="{b['x'] + 15}" y1="{b['y'] + 48}" x2="{b['x'] + b['w'] - 15}" y2="{b['y'] + 48}" stroke="#e2e8f0" stroke-width="1.5"/>''')
        curr_y = b['y'] + 80
        for line in b['lines']:
            svg_elements.append(f'  <text x="{b["x"] + 22}" y="{curr_y}" font-family="Arial, Helvetica, sans-serif" font-size="20" fill="#111111">{line}</text>')
            curr_y += 34

    # Arrows
    for a in arrows:
        mid_x = (a['from_x'] + a['to_x']) // 2
        # Arrow line
        svg_elements.append(f'  <line x1="{a["from_x"]}" y1="{a["y"]}" x2="{a["to_x"]}" y2="{a["y"]}" stroke="#000000" stroke-width="3.5" marker-end="url(#arrowhead)"/>')
        # Background badge for label
        svg_elements.append(f'''  <rect x="{mid_x - 260}" y="{a['y'] - 54}" width="520" height="44" fill="#ffffff" fill-opacity="0.96" stroke="#b0b0b0" stroke-width="1.2" rx="5"/>
  <text x="{mid_x}" y="{a['y'] - 31}" font-family="Arial, Helvetica, sans-serif" font-size="19" font-weight="bold" fill="#000000" text-anchor="middle">{a['line1']}</text>
  <text x="{mid_x}" y="{a['y'] - 13}" font-family="Arial, Helvetica, sans-serif" font-size="17" font-weight="bold" fill="#2b6cb0" text-anchor="middle">{a['line2']}</text>''')

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {H}" width="{WIDTH}" height="{H}">
  <defs>
    <marker id="arrowhead" markerWidth="14" markerHeight="10" refX="12" refY="5" orient="auto">
      <polygon points="0 0, 14 5, 0 10" fill="#000000" />
    </marker>
  </defs>
  <rect width="{WIDTH}" height="{H}" fill="#ffffff"/>
{"\n".join(svg_elements)}
</svg>'''

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"[OK] Generated Phase 2 SVG: {svg_path}")

    # Render PNG with Chrome Headless
    html_temp = os.path.join(TEMP_DIR, "_temp_phase2.html")
    with open(html_temp, "w", encoding="utf-8") as f:
        f.write(f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: #ffffff; width: {WIDTH}px; height: {H}px; overflow: hidden; }}
</style>
</head>
<body>
{svg_content}
</body>
</html>''')

    cmd = [
        CHROME_PATH,
        "--headless",
        "--disable-gpu",
        "--force-device-scale-factor=2",
        f"--window-size={WIDTH},{H}",
        f"--screenshot={png_path}",
        html_temp
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if os.path.exists(html_temp):
        os.remove(html_temp)
    print(f"[OK] Rendered High-Res PNG: {png_path}")

    # Sync to brain artifacts
    if os.path.exists(ARTIFACT_DIR):
        shutil.copy2(png_path, os.path.join(ARTIFACT_DIR, "fig2_phase2_data_access.png"))
        print("[OK] Synced artifact: fig2_phase2_data_access.png")


if __name__ == "__main__":
    generate_phase1()
    generate_phase2()
    print("\n[ALL COMPLETE] Both phase diagrams generated successfully with big, prominent fonts and exact arrow syntax.")
