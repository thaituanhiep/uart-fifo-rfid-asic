# -*- coding: utf-8 -*-
"""
Script to generate:
  1. rdm6300_picorv32_instruction_flow.drawio (Pure B&W Draw.io XML with Super-Clean Layout)
  2. rdm6300_picorv32_instruction_flow.svg (Vector SVG with Big Legible Fonts)
  3. document/temp/fig2_instruction_flow.png (High-Res 2x Retina PNG via Headless Chrome)

Shows the exact step-by-step sequence of processing 1 firmware instruction
(lw a0, 0(sp)) across 4 separate columns:
  - Column 1: PicoRV32 CPU (Master - Native Memory Bus)
  - Column 2: soc_interconnect.v (Central Bus Arbiter & Address Decoder)
  - Column 3: SPI Flash / spimemio (0x0010_0000 - 0x00FF_FFFF - Code XIP)
  - Column 4: 1KB Data SRAM (0x0000_0000 - 0x0000_03FF - Data & Stack)
"""

import os
import subprocess
import shutil

PROJECT_DIR = r"d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data"
DRAWIO_PATH = os.path.join(PROJECT_DIR, "rdm6300_picorv32_instruction_flow.drawio")
SVG_PATH    = os.path.join(PROJECT_DIR, "rdm6300_picorv32_instruction_flow.svg")
PNG_OUT     = os.path.join(PROJECT_DIR, "document", "temp", "fig2_instruction_flow.png")
HTML_RENDER = os.path.join(PROJECT_DIR, "document", "temp", "render_instruction_flow.html")

WIDTH  = 1660
HEIGHT = 1740

# Lifeline X positions
X_COL1 = 220   # CPU
X_COL2 = 635   # soc_interconnect
X_COL3 = 1045  # SPI Flash
X_COL4 = 1450  # 1KB SRAM

def create_drawio_xml():
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="2026-10-02T05:35:00.000Z" agent="Mozilla/5.0" version="21.0.0" type="device">
  <diagram id="soc_instruction_flow" name="Instruction Execution Sequence">
    <mxGraphModel dx="1600" dy="1700" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{WIDTH}" pageHeight="{HEIGHT}" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- Title Banner -->
        <mxCell id="title" value="&lt;b style=&quot;font-size:24px;&quot;&gt;SƠ ĐỒ TRÌNH TỰ THỰC THI 1 LỆNH FIRMWARE QUA SOC_INTERCONNECT&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:16px;&quot;&gt;Ví dụ: Lệnh đọc biến từ ngăn xếp Stack: &lt;b&gt;int x = local_var;&lt;/b&gt; (Mã máy RISC-V: &lt;b&gt;lw a0, 0(sp)&lt;/b&gt;)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2.5;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="30" y="20" width="1600" height="70" as="geometry" />
        </mxCell>

        <!-- Column Headers -->
        <mxCell id="col1_head" value="&lt;b style=&quot;font-size:19px;&quot;&gt;CỘT 1: PicoRV32 CPU (MASTER)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:14.5px;&quot;&gt;Native Memory Bus (cpu_mem_*)&lt;br&gt;Nạp lệnh, Giải mã, Thực thi, Đọc/Ghi dữ liệu&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2.2;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="40" y="110" width="360" height="85" as="geometry" />
        </mxCell>

        <mxCell id="col2_head" value="&lt;b style=&quot;font-size:19px;&quot;&gt;CỘT 2: soc_interconnect.v&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:14.5px;&quot;&gt;Address Decoder &amp;amp; Bus Multiplexer&lt;br&gt;Giải mã địa chỉ, bật sel_*, ghép rdata / ready&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2.2;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="455" y="110" width="360" height="85" as="geometry" />
        </mxCell>

        <mxCell id="col3_head" value="&lt;b style=&quot;font-size:19px;&quot;&gt;CỘT 3: SPI FLASH (spimemio.v)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:14.5px;&quot;&gt;Dải địa chỉ: &lt;b&gt;0x0010_0000 - 0x00FF_FFFF&lt;/b&gt;&lt;br&gt;Chứa mã lệnh XIP (firmware) &amp;amp; Database UID&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2.2;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="865" y="110" width="360" height="85" as="geometry" />
        </mxCell>

        <mxCell id="col4_head" value="&lt;b style=&quot;font-size:19px;&quot;&gt;CỘT 4: 1KB DATA SRAM (data_sram)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:14.5px;&quot;&gt;Dải địa chỉ: &lt;b&gt;0x0000_0000 - 0x0000_03FF&lt;/b&gt;&lt;br&gt;Chứa ngăn xếp Stack (sp), biến cục bộ (.data, .bss)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2.2;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="1270" y="110" width="360" height="85" as="geometry" />
        </mxCell>

        <!-- Lifelines -->
        <mxCell id="line_col1" value="" style="endArrow=none;dashed=1;strokeWidth=1.8;strokeColor=#888888;html=1;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="{X_COL1}" y="195" as="sourcePoint" />
            <mxPoint x="{X_COL1}" y="1710" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <mxCell id="line_col2" value="" style="endArrow=none;dashed=1;strokeWidth=1.8;strokeColor=#888888;html=1;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="{X_COL2}" y="195" as="sourcePoint" />
            <mxPoint x="{X_COL2}" y="1710" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <mxCell id="line_col3" value="" style="endArrow=none;dashed=1;strokeWidth=1.8;strokeColor=#888888;html=1;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="{X_COL3}" y="195" as="sourcePoint" />
            <mxPoint x="{X_COL3}" y="1710" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <mxCell id="line_col4" value="" style="endArrow=none;dashed=1;strokeWidth=1.8;strokeColor=#888888;html=1;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="{X_COL4}" y="195" as="sourcePoint" />
            <mxPoint x="{X_COL4}" y="1710" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <!-- ============================================================= -->
        <!-- CHẶNG 1: NẠP MÃ LỆNH TỪ FLASH                                 -->
        <!-- ============================================================= -->
        <mxCell id="banner_stage1" value="&lt;b style=&quot;font-size:18px;&quot;&gt;CHẶNG 1: NẠP MÃ LỆNH TỪ FLASH (INSTRUCTION FETCH - XIP VIA FLASH)&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;align=left;spacingLeft=15;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="40" y="215" width="1590" height="40" as="geometry" />
        </mxCell>

        <!-- Step 1 Box -->
        <mxCell id="box_s1" value="&lt;b style=&quot;font-size:16px;&quot;&gt;Bước 1: CPU phát chu kỳ nạp lệnh&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:14px;&quot;&gt;• &lt;b&gt;cpu_mem_valid = 1&lt;/b&gt;&lt;br&gt;• &lt;b&gt;cpu_mem_addr = 0x0025_0000&lt;/b&gt; (Vị trí mã lệnh)&lt;br&gt;• &lt;b&gt;cpu_mem_wstrb = 0&lt;/b&gt; (Chu kỳ đọc mã lệnh)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.8;align=left;spacingLeft=12;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="50" y="270" width="340" height="85" as="geometry" />
        </mxCell>

        <!-- Step 1 Arrow -->
        <mxCell id="arrow_s1" value="cpu_mem_valid = 1, addr = 0x0025_0000" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2.2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=15;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="{X_COL1}" y="380" as="sourcePoint" />
            <mxPoint x="{X_COL2}" y="380" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <!-- Step 2 Box -->
        <mxCell id="box_s2" value="&lt;b style=&quot;font-size:16px;&quot;&gt;Bước 2: Giải mã địa chỉ Flash&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:14px;&quot;&gt;• So khớp: 0x0025_0000 ∈ [0x0010_0000..0x0100_0000)&lt;br&gt;• Kích hoạt: &lt;b&gt;sel_spimem = 1&lt;/b&gt;&lt;br&gt;• Khóa các cổng khác (&lt;b&gt;sel_sram = 0&lt;/b&gt;, sel_uart = 0)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.8;align=left;spacingLeft=12;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="465" y="405" width="340" height="85" as="geometry" />
        </mxCell>

        <!-- Step 2 Arrow -->
        <mxCell id="arrow_s2" value="sel_spimem = 1 (Kích hoạt bộ điều khiển Flash)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2.2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=15;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="{X_COL2}" y="515" as="sourcePoint" />
            <mxPoint x="{X_COL3}" y="515" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <!-- Step 3 Box -->
        <mxCell id="box_s3" value="&lt;b style=&quot;font-size:16px;&quot;&gt;Bước 3: Giao tiếp SPI Flash ngoài&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:14px;&quot;&gt;• &lt;b&gt;spimemio&lt;/b&gt; phát chuỗi xung SPI (SCK/MOSI/MISO)&lt;br&gt;• Đọc 4 byte mã máy từ chip Flash ngoài&lt;br&gt;• CPU tự động tạm dừng (&lt;b&gt;Stall&lt;/b&gt;) chờ nạp mã lệnh&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.8;align=left;spacingLeft=12;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="875" y="540" width="340" height="85" as="geometry" />
        </mxCell>

        <!-- Step 4 Box -->
        <mxCell id="box_s4" value="&lt;b style=&quot;font-size:16px;&quot;&gt;Bước 4: Flash trả mã lệnh &amp;amp; Báo xong&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:14px;&quot;&gt;• &lt;b&gt;spimem_rdata&lt;/b&gt; = Mã opcode 32-bit (lw)&lt;br&gt;• Kích hoạt: &lt;b&gt;spimem_ready = 1&lt;/b&gt;&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.8;align=left;spacingLeft=12;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="875" y="640" width="340" height="75" as="geometry" />
        </mxCell>

        <!-- Step 4 Arrow -->
        <mxCell id="arrow_s4" value="spimem_rdata (mã opcode lw), spimem_ready = 1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2.2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=15;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="{X_COL3}" y="740" as="sourcePoint" />
            <mxPoint x="{X_COL2}" y="740" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <!-- Step 5 Box -->
        <mxCell id="box_s5" value="&lt;b style=&quot;font-size:16px;&quot;&gt;Bước 5: Ghép kênh dữ liệu về CPU&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:14px;&quot;&gt;• &lt;b&gt;cpu_mem_rdata = spimem_rdata&lt;/b&gt;&lt;br&gt;• &lt;b&gt;cpu_mem_ready = spimem_ready = 1&lt;/b&gt;&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.8;align=left;spacingLeft=12;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="465" y="765" width="340" height="75" as="geometry" />
        </mxCell>

        <!-- Step 5 Arrow -->
        <mxCell id="arrow_s5" value="cpu_mem_rdata, cpu_mem_ready = 1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2.2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=15;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="{X_COL2}" y="865" as="sourcePoint" />
            <mxPoint x="{X_COL1}" y="865" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <!-- Step 6 Box -->
        <mxCell id="box_s6" value="&lt;b style=&quot;font-size:16px;&quot;&gt;Bước 6: CPU nhận mã lệnh vào IR&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:14px;&quot;&gt;• Chốt opcode &#39;lw&#39; vào thanh ghi lệnh (IR)&lt;br&gt;• Hạ &lt;b&gt;cpu_mem_valid = 0&lt;/b&gt; (Kết thúc chu kỳ đọc lệnh)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.8;align=left;spacingLeft=12;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="50" y="890" width="340" height="75" as="geometry" />
        </mxCell>

        <!-- ============================================================= -->
        <!-- INTERMEDIATE STAGE                                            -->
        <!-- ============================================================= -->
        <mxCell id="banner_stage_mid" value="&lt;b style=&quot;font-size:17.5px;&quot;&gt;GIAI ĐOẠN TRUNG GIAN: GIẢI MÃ LỆNH NỘI BỘ CPU (INSTRUCTION DECODE &amp;amp; ALU)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:14.5px;&quot;&gt;• CPU giải mã mã lệnh &#39;lw&#39;: Xác định cần đọc 1 từ (4-byte) từ con trỏ ngăn xếp: &lt;b&gt;addr = sp + 0 = 0x0000_03F0&lt;/b&gt;&lt;br&gt;• Địa chỉ này thuộc vùng &lt;b&gt;1KB SRAM&lt;/b&gt; -&amp;gt; CPU kích hoạt chu kỳ truy xuất bus dữ liệu mới (Data Memory Access)!&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;align=left;spacingLeft=15;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="40" y="985" width="1590" height="65" as="geometry" />
        </mxCell>

        <!-- ============================================================= -->
        <!-- CHẶNG 2: ĐỌC DỮ LIỆU TỪ SRAM                                  -->
        <!-- ============================================================= -->
        <mxCell id="banner_stage2" value="&lt;b style=&quot;font-size:18px;&quot;&gt;CHẶNG 2: ĐỌC DỮ LIỆU TỪ SRAM (DATA MEMORY ACCESS - 1KB DATA SRAM)&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;align=left;spacingLeft=15;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="40" y="1065" width="1590" height="40" as="geometry" />
        </mxCell>

        <!-- Step 7 Box -->
        <mxCell id="box_s7" value="&lt;b style=&quot;font-size:16px;&quot;&gt;Bước 7: CPU phát chu kỳ đọc dữ liệu&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:14px;&quot;&gt;• &lt;b&gt;cpu_mem_valid = 1&lt;/b&gt;&lt;br&gt;• &lt;b&gt;cpu_mem_addr = 0x0000_03F0&lt;/b&gt; (Địa chỉ biến trên Stack)&lt;br&gt;• &lt;b&gt;cpu_mem_wstrb = 0&lt;/b&gt; (Chu kỳ đọc dữ liệu)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.8;align=left;spacingLeft=12;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="50" y="1120" width="340" height="85" as="geometry" />
        </mxCell>

        <!-- Step 7 Arrow -->
        <mxCell id="arrow_s7" value="cpu_mem_valid = 1, addr = 0x0000_03F0" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2.2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=15;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="{X_COL1}" y="1230" as="sourcePoint" />
            <mxPoint x="{X_COL2}" y="1230" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <!-- Step 8 Box -->
        <mxCell id="box_s8" value="&lt;b style=&quot;font-size:16px;&quot;&gt;Bước 8: Giải mã địa chỉ SRAM&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:14px;&quot;&gt;• So khớp: 0x0000_03F0 &amp;lt; 0x0000_0400 (Dưới 1KB)&lt;br&gt;• Kích hoạt: &lt;b&gt;sel_sram = 1&lt;/b&gt;&lt;br&gt;• Cột 3 SPI Flash nghỉ (&lt;b&gt;sel_spimem = 0&lt;/b&gt;)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.8;align=left;spacingLeft=12;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="465" y="1255" width="340" height="85" as="geometry" />
        </mxCell>

        <!-- Step 8 Arrow -->
        <mxCell id="arrow_s8" value="sel_sram = 1 (Kích hoạt 1KB Data SRAM)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2.2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=15;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="{X_COL2}" y="1365" as="sourcePoint" />
            <mxPoint x="{X_COL4}" y="1365" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <!-- Step 9 Box -->
        <mxCell id="box_s9" value="&lt;b style=&quot;font-size:16px;&quot;&gt;Bước 9: SRAM truy xuất ô nhớ 0x3F0&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:14px;&quot;&gt;• SRAM on-chip đọc ô nhớ Stack 0x3F0&lt;br&gt;• Xuất dữ liệu: &lt;b&gt;sram_rdata = Giá trị biến x&lt;/b&gt;&lt;br&gt;• Bật &lt;b&gt;sram_ready = 1&lt;/b&gt; sau &lt;b&gt;đúng 1 chu kỳ clock&lt;/b&gt;&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.8;align=left;spacingLeft=12;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="1280" y="1390" width="340" height="85" as="geometry" />
        </mxCell>

        <!-- Step 10 Arrow -->
        <mxCell id="arrow_s10" value="sram_rdata (giá trị biến x), sram_ready = 1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2.2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=15;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="{X_COL4}" y="1500" as="sourcePoint" />
            <mxPoint x="{X_COL2}" y="1500" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <!-- Step 10b Box -->
        <mxCell id="box_s10" value="&lt;b style=&quot;font-size:16px;&quot;&gt;Bước 10: Ghép kênh dữ liệu SRAM về CPU&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:14px;&quot;&gt;• &lt;b&gt;cpu_mem_rdata = sram_rdata&lt;/b&gt;&lt;br&gt;• &lt;b&gt;cpu_mem_ready = sram_ready = 1&lt;/b&gt;&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.8;align=left;spacingLeft=12;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="465" y="1525" width="340" height="75" as="geometry" />
        </mxCell>

        <!-- Step 11 Arrow -->
        <mxCell id="arrow_s11" value="cpu_mem_rdata, cpu_mem_ready = 1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2.2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=15;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="{X_COL2}" y="1625" as="sourcePoint" />
            <mxPoint x="{X_COL1}" y="1625" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <!-- Step 11 Box -->
        <mxCell id="box_s11" value="&lt;b style=&quot;font-size:16px;&quot;&gt;Bước 11: CPU chốt dữ liệu vào a0 &amp;amp; Hoàn tất&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:14px;&quot;&gt;• Ghi giá trị biến vào thanh ghi mục tiêu &lt;b&gt;a0&lt;/b&gt;&lt;br&gt;• Hạ &lt;b&gt;cpu_mem_valid = 0&lt;/b&gt; | Tăng &lt;b&gt;PC = PC + 4&lt;/b&gt;&lt;br&gt;• &lt;b&gt;LỆNH HOÀN TẤT THỰC THI 100%!&lt;/b&gt;&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.8;align=left;spacingLeft=12;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="50" y="1645" width="340" height="85" as="geometry" />
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
    with open(DRAWIO_PATH, "w", encoding="utf-8") as f:
        f.write(xml.strip())
    print(f"[OK] Generated Draw.io XML: {DRAWIO_PATH}")

def create_svg():
    # Build high-legibility vector SVG
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}">
  <defs>
    <style>
      .title-box {{ fill: #ffffff; stroke: #000000; stroke-width: 2.5; }}
      .col-box {{ fill: #ffffff; stroke: #000000; stroke-width: 2.2; }}
      .banner-box {{ fill: #ffffff; stroke: #000000; stroke-width: 2; }}
      .step-box {{ fill: #ffffff; stroke: #000000; stroke-width: 1.8; }}
      .lifeline {{ stroke: #888888; stroke-width: 1.8; stroke-dasharray: 6,6; }}
      .flow-arrow {{ stroke: #000000; stroke-width: 2.2; fill: none; }}
      .arrowhead {{ fill: #000000; }}
      .txt-title {{ font-family: Arial, Helvetica, sans-serif; font-size: 24px; font-weight: bold; text-anchor: middle; fill: #000000; }}
      .txt-subtitle {{ font-family: Arial, Helvetica, sans-serif; font-size: 16px; text-anchor: middle; fill: #222222; }}
      .txt-col-title {{ font-family: Arial, Helvetica, sans-serif; font-size: 18.5px; font-weight: bold; text-anchor: middle; fill: #000000; }}
      .txt-col-desc {{ font-family: Arial, Helvetica, sans-serif; font-size: 14px; text-anchor: middle; fill: #222222; }}
      .txt-banner {{ font-family: Arial, Helvetica, sans-serif; font-size: 17.5px; font-weight: bold; fill: #000000; }}
      .txt-banner-sub {{ font-family: Arial, Helvetica, sans-serif; font-size: 14.5px; fill: #222222; }}
      .txt-step-title {{ font-family: Arial, Helvetica, sans-serif; font-size: 16px; font-weight: bold; fill: #000000; }}
      .txt-step-body {{ font-family: Arial, Helvetica, sans-serif; font-size: 14px; fill: #111111; }}
      .txt-label {{ font-family: Arial, Helvetica, sans-serif; font-size: 15px; font-weight: bold; fill: #000000; }}
      .label-bg {{ fill: #ffffff; }}
    </style>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" class="arrowhead" />
    </marker>
  </defs>

  <!-- Background Canvas -->
  <rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" fill="#ffffff" />

  <!-- 1. Title Banner -->
  <rect x="30" y="20" width="1600" height="70" class="title-box" />
  <text x="830" y="47" class="txt-title">SƠ ĐỒ TRÌNH TỰ THỰC THI 1 LỆNH FIRMWARE QUA SOC_INTERCONNECT</text>
  <text x="830" y="73" class="txt-subtitle">Ví dụ: Lệnh đọc biến từ ngăn xếp Stack: int x = local_var; (Mã máy RISC-V: lw a0, 0(sp))</text>

  <!-- 2. Column Headers -->
  <!-- Col 1: CPU -->
  <rect x="40" y="110" width="360" height="85" class="col-box" />
  <text x="{X_COL1}" y="139" class="txt-col-title">CỘT 1: PicoRV32 CPU (MASTER)</text>
  <text x="{X_COL1}" y="162" class="txt-col-desc">Native Memory Bus (cpu_mem_*)</text>
  <text x="{X_COL1}" y="180" class="txt-col-desc">Nạp lệnh, Giải mã, Thực thi, Đọc/Ghi dữ liệu</text>

  <!-- Col 2: soc_interconnect -->
  <rect x="455" y="110" width="360" height="85" class="col-box" />
  <text x="{X_COL2}" y="139" class="txt-col-title">CỘT 2: soc_interconnect.v</text>
  <text x="{X_COL2}" y="162" class="txt-col-desc">Address Decoder &amp; Bus Multiplexer</text>
  <text x="{X_COL2}" y="180" class="txt-col-desc">Giải mã địa chỉ, bật sel_*, ghép rdata / ready</text>

  <!-- Col 3: SPI Flash -->
  <rect x="865" y="110" width="360" height="85" class="col-box" />
  <text x="{X_COL3}" y="139" class="txt-col-title">CỘT 3: SPI FLASH (spimemio.v)</text>
  <text x="{X_COL3}" y="162" class="txt-col-desc">0x0010_0000 - 0x00FF_FFFF</text>
  <text x="{X_COL3}" y="180" class="txt-col-desc">Chứa mã lệnh XIP (firmware) &amp; Database UID</text>

  <!-- Col 4: 1KB SRAM -->
  <rect x="1270" y="110" width="360" height="85" class="col-box" />
  <text x="{X_COL4}" y="139" class="txt-col-title">CỘT 4: 1KB DATA SRAM (data_sram)</text>
  <text x="{X_COL4}" y="162" class="txt-col-desc">0x0000_0000 - 0x0000_03FF</text>
  <text x="{X_COL4}" y="180" class="txt-col-desc">Chứa ngăn xếp Stack (sp), biến cục bộ (.data, .bss)</text>

  <!-- Vertical Lifelines -->
  <line x1="{X_COL1}" y1="195" x2="{X_COL1}" y2="1710" class="lifeline" />
  <line x1="{X_COL2}" y1="195" x2="{X_COL2}" y2="1710" class="lifeline" />
  <line x1="{X_COL3}" y1="195" x2="{X_COL3}" y2="1710" class="lifeline" />
  <line x1="{X_COL4}" y1="195" x2="{X_COL4}" y2="1710" class="lifeline" />

  <!-- ============================================================= -->
  <!-- CHẶNG 1: INSTRUCTION FETCH FROM FLASH                         -->
  <!-- ============================================================= -->
  <rect x="40" y="215" width="1590" height="40" class="banner-box" />
  <text x="55" y="241" class="txt-banner">CHẶNG 1: NẠP MÃ LỆNH TỪ FLASH (INSTRUCTION FETCH - XIP VIA FLASH)</text>

  <!-- Step 1: CPU initiates fetch -->
  <rect x="50" y="270" width="340" height="85" class="step-box" />
  <text x="65" y="295" class="txt-step-title">Bước 1: CPU phát chu kỳ nạp lệnh</text>
  <text x="65" y="316" class="txt-step-body">• cpu_mem_valid = 1</text>
  <text x="65" y="335" class="txt-step-body">• cpu_mem_addr = 0x0025_0000 (Vị trí mã lệnh)</text>

  <!-- Step 1 Arrow: Lifeline 1 -> Lifeline 2 -->
  <line x1="{X_COL1}" y1="380" x2="{X_COL2}" y2="380" class="flow-arrow" marker-end="url(#arrow)" />
  <rect x="270" y="367" width="315" height="26" class="label-bg" />
  <text x="427" y="385" class="txt-label" text-anchor="middle">cpu_mem_valid = 1, addr = 0x0025_0000</text>

  <!-- Step 2: Interconnect Decodes Flash -->
  <rect x="465" y="405" width="340" height="85" class="step-box" />
  <text x="480" y="430" class="txt-step-title">Bước 2: Giải mã địa chỉ Flash</text>
  <text x="480" y="451" class="txt-step-body">• 0x0025_0000 ∈ [0x0010_0000..0x0100_0000)</text>
  <text x="480" y="470" class="txt-step-body">• Kích hoạt: sel_spimem = 1 (khóa sel_sram = 0)</text>

  <!-- Step 2 Arrow: Lifeline 2 -> Lifeline 3 -->
  <line x1="{X_COL2}" y1="515" x2="{X_COL3}" y2="515" class="flow-arrow" marker-end="url(#arrow)" />
  <rect x="670" y="502" width="340" height="26" class="label-bg" />
  <text x="840" y="520" class="txt-label" text-anchor="middle">sel_spimem = 1 (Kích hoạt bộ điều khiển Flash)</text>

  <!-- Step 3: Flash reads 4 bytes -->
  <rect x="875" y="540" width="340" height="85" class="step-box" />
  <text x="890" y="565" class="txt-step-title">Bước 3: Giao tiếp SPI Flash ngoài</text>
  <text x="890" y="586" class="txt-step-body">• spimemio phát chuỗi xung SPI (SCK/MOSI/MISO)</text>
  <text x="890" y="605" class="txt-step-body">• CPU tự động tạm dừng (Stall) chờ nạp mã lệnh</text>

  <!-- Step 4: Flash returns opcode & ready -->
  <rect x="875" y="640" width="340" height="75" class="step-box" />
  <text x="890" y="665" class="txt-step-title">Bước 4: Flash trả mã lệnh &amp; Báo xong</text>
  <text x="890" y="686" class="txt-step-body">• spimem_rdata = Mã opcode 32-bit (lw)</text>
  <text x="890" y="703" class="txt-step-body">• Kích hoạt: spimem_ready = 1</text>

  <!-- Step 4 Arrow: Lifeline 3 -> Lifeline 2 -->
  <line x1="{X_COL3}" y1="740" x2="{X_COL2}" y2="740" class="flow-arrow" marker-end="url(#arrow)" />
  <rect x="670" y="727" width="340" height="26" class="label-bg" />
  <text x="840" y="745" class="txt-label" text-anchor="middle">spimem_rdata (mã opcode lw), ready = 1</text>

  <!-- Step 5: Interconnect Mux to CPU -->
  <rect x="465" y="765" width="340" height="75" class="step-box" />
  <text x="480" y="790" class="txt-step-title">Bước 5: Ghép kênh dữ liệu về CPU</text>
  <text x="480" y="811" class="txt-step-body">• cpu_mem_rdata = spimem_rdata</text>
  <text x="480" y="828" class="txt-step-body">• cpu_mem_ready = spimem_ready = 1</text>

  <!-- Step 5 Arrow: Lifeline 2 -> Lifeline 1 -->
  <line x1="{X_COL2}" y1="865" x2="{X_COL1}" y2="865" class="flow-arrow" marker-end="url(#arrow)" />
  <rect x="280" y="852" width="295" height="26" class="label-bg" />
  <text x="427" y="870" class="txt-label" text-anchor="middle">cpu_mem_rdata, cpu_mem_ready = 1</text>

  <!-- Step 6: CPU Latches Opcode -->
  <rect x="50" y="890" width="340" height="75" class="step-box" />
  <text x="65" y="915" class="txt-step-title">Bước 6: CPU nhận mã lệnh vào IR</text>
  <text x="65" y="936" class="txt-step-body">• Chốt opcode lw vào thanh ghi lệnh (IR)</text>
  <text x="65" y="953" class="txt-step-body">• Hạ cpu_mem_valid = 0 (Xong chu kỳ đọc)</text>

  <!-- ============================================================= -->
  <!-- GIAI ĐOẠN TRUNG GIAN                                          -->
  <!-- ============================================================= -->
  <rect x="40" y="985" width="1590" height="65" class="banner-box" />
  <text x="55" y="1010" class="txt-banner">GIAI ĐOẠN TRUNG GIAN: GIẢI MÃ LỆNH NỘI BỘ CPU (INSTRUCTION DECODE &amp; ALU)</text>
  <text x="55" y="1035" class="txt-banner-sub">• CPU giải mã opcode 'lw': Xác định cần đọc 1 từ (4-byte) từ con trỏ ngăn xếp: addr = sp + 0 = 0x0000_03F0 (vùng 1KB SRAM). Phát chu kỳ bus mới!</text>

  <!-- ============================================================= -->
  <!-- CHẶNG 2: DATA MEMORY ACCESS TO SRAM                           -->
  <!-- ============================================================= -->
  <rect x="40" y="1065" width="1590" height="40" class="banner-box" />
  <text x="55" y="1091" class="txt-banner">CHẶNG 2: ĐỌC DỮ LIỆU TỪ SRAM (DATA MEMORY ACCESS - 1KB DATA SRAM)</text>

  <!-- Step 7: CPU initiates data read -->
  <rect x="50" y="1120" width="340" height="85" class="step-box" />
  <text x="65" y="1145" class="txt-step-title">Bước 7: CPU phát chu kỳ đọc dữ liệu</text>
  <text x="65" y="1166" class="txt-step-body">• cpu_mem_valid = 1</text>
  <text x="65" y="1185" class="txt-step-body">• cpu_mem_addr = 0x0000_03F0 (Địa chỉ Stack)</text>

  <!-- Step 7 Arrow: Lifeline 1 -> Lifeline 2 -->
  <line x1="{X_COL1}" y1="1230" x2="{X_COL2}" y2="1230" class="flow-arrow" marker-end="url(#arrow)" />
  <rect x="270" y="1217" width="315" height="26" class="label-bg" />
  <text x="427" y="1235" class="txt-label" text-anchor="middle">cpu_mem_valid = 1, addr = 0x0000_03F0</text>

  <!-- Step 8: Interconnect Decodes SRAM -->
  <rect x="465" y="1255" width="340" height="85" class="step-box" />
  <text x="480" y="1280" class="txt-step-title">Bước 8: Giải mã địa chỉ SRAM</text>
  <text x="480" y="1301" class="txt-step-body">• 0x0000_03F0 &lt; 0x0000_0400 (Dưới 1KB)</text>
  <text x="480" y="1320" class="txt-step-body">• Kích hoạt: sel_sram = 1 (Cột 3 Flash nghỉ)</text>

  <!-- Step 8 Arrow: Lifeline 2 -> Lifeline 4 -->
  <line x1="{X_COL2}" y1="1365" x2="{X_COL4}" y2="1365" class="flow-arrow" marker-end="url(#arrow)" />
  <rect x="880" y="1352" width="320" height="26" class="label-bg" />
  <text x="1042" y="1370" class="txt-label" text-anchor="middle">sel_sram = 1 (Kích hoạt 1KB Data SRAM)</text>

  <!-- Step 9: SRAM reads data -->
  <rect x="1280" y="1390" width="340" height="85" class="step-box" />
  <text x="1295" y="1415" class="txt-step-title">Bước 9: SRAM truy xuất ô nhớ 0x3F0</text>
  <text x="1295" y="1436" class="txt-step-body">• SRAM on-chip đọc ô nhớ Stack 0x3F0</text>
  <text x="1295" y="1455" class="txt-step-body">• Xuất dữ liệu: sram_rdata = Giá trị biến x</text>

  <!-- Step 10 Arrow: Lifeline 4 -> Lifeline 2 -->
  <line x1="{X_COL4}" y1="1500" x2="{X_COL2}" y2="1500" class="flow-arrow" marker-end="url(#arrow)" />
  <rect x="880" y="1487" width="320" height="26" class="label-bg" />
  <text x="1042" y="1505" class="txt-label" text-anchor="middle">sram_rdata (biến x), sram_ready = 1</text>

  <!-- Step 10b: Interconnect Mux to CPU -->
  <rect x="465" y="1525" width="340" height="75" class="step-box" />
  <text x="480" y="1550" class="txt-step-title">Bước 10: Ghép kênh dữ liệu SRAM về CPU</text>
  <text x="480" y="1571" class="txt-step-body">• cpu_mem_rdata = sram_rdata</text>
  <text x="480" y="1588" class="txt-step-body">• cpu_mem_ready = sram_ready = 1</text>

  <!-- Step 11 Arrow: Lifeline 2 -> Lifeline 1 -->
  <line x1="{X_COL2}" y1="1625" x2="{X_COL1}" y2="1625" class="flow-arrow" marker-end="url(#arrow)" />
  <rect x="280" y="1612" width="295" height="26" class="label-bg" />
  <text x="427" y="1630" class="txt-label" text-anchor="middle">cpu_mem_rdata, cpu_mem_ready = 1</text>

  <!-- Step 11: CPU Latches Data & Completes -->
  <rect x="50" y="1645" width="340" height="85" class="step-box" />
  <text x="65" y="1670" class="txt-step-title">Bước 11: CPU chốt dữ liệu vào a0</text>
  <text x="65" y="1691" class="txt-step-body">• Ghi giá trị biến vào thanh ghi mục tiêu a0</text>
  <text x="65" y="1710" class="txt-step-body">• Tăng PC = PC + 4 -&gt; LỆNH HOÀN TẤT 100%!</text>

</svg>
"""
    with open(SVG_PATH, "w", encoding="utf-8") as f:
        f.write(svg.strip())
    print(f"[OK] Generated SVG Vector: {SVG_PATH}")

def render_png():
    html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{
      margin: 0;
      padding: 0;
      background-color: #ffffff;
      display: flex;
      justify-content: center;
      align-items: center;
    }}
    svg {{
      width: {WIDTH}px;
      height: {HEIGHT}px;
    }}
  </style>
</head>
<body>
  <img src="file:///{SVG_PATH.replace(os.sep, '/')}" width="{WIDTH}" height="{HEIGHT}" />
</body>
</html>
"""
    with open(HTML_RENDER, "w", encoding="utf-8") as f:
        f.write(html_content)

    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if not os.path.exists(chrome_path):
        chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

    cmd = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        "--force-device-scale-factor=2",
        f"--window-size={WIDTH},{HEIGHT}",
        f"--screenshot={PNG_OUT}",
        HTML_RENDER
    ]
    print(f"Running Chrome Headless screenshot to {PNG_OUT}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"[OK] Successfully rendered High-Res PNG: {PNG_OUT}")
    else:
        print(f"[ERROR] Chrome headless failed: {res.stderr}")

    artifact_png = r"C:\Users\thait\.gemini\antigravity-ide\brain\40d01579-3c16-4b85-9b12-c0e7d33bcd21\fig2_instruction_flow.png"
    shutil.copy2(PNG_OUT, artifact_png)
    print(f"[OK] Copied to Artifact: {artifact_png}")

if __name__ == "__main__":
    create_drawio_xml()
    create_svg()
    render_png()
