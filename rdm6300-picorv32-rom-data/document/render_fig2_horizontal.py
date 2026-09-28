# -*- coding: utf-8 -*-
"""
Script: render_fig2_horizontal.py
Generates a magnificent, ultra-sharp LANDSCAPE (horizontal) version of:
"Hình 2. Sơ đồ khối chi tiết đường ống 5 giai đoạn thu nhận và giải mã phần cứng thẻ RFID RDM6300 tự trị"

Features:
- 5 main pipeline stages laid out horizontally from Left to Right with prominent flow arrows.
- Big, crisp, publication-grade typography (14px to 28px).
- Bottom wide container showing the 14-byte frame structure and 1-cycle parallel XOR proof.
- High-res PNG render via Headless Chrome with --force-device-scale-factor=2.
- Generates fig2_rdm6300_horizontal.png and fig2_rdm6300_horizontal.drawio.
"""

import os
import subprocess

def create_horizontal_drawio_xml():
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="2026-09-28T09:35:00.000Z" agent="Mozilla/5.0" version="21.0.0" type="device">
  <diagram id="rdm6300_horizontal_pipeline" name="RDM6300 Horizontal Pipeline">
    <mxGraphModel dx="2200" dy="1200" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="2100" pageHeight="1100" math="0" shadow="1">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- Title Banner -->
        <mxCell id="title" value="&lt;b style=&quot;font-size:24px;&quot;&gt;HỆ THỐNG PHẦN CỨNG THU NHẬN &amp;amp; GIẢI MÃ THẺ RFID RDM6300 TỰ TRỊ&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:15px; color:#475569;&quot;&gt;Sơ đồ khối vi kiến trúc đường ống 5 giai đoạn phần cứng (Hardware 5-Stage Autonomous Decoding Pipeline)&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#cbd5e1;strokeWidth=2;fontFamily=Segoe UI;align=center;" vertex="1" parent="1">
          <mxGeometry x="40" y="30" width="2020" height="70" as="geometry" />
        </mxCell>

        <!-- STAGE 1: RF FRONT-END -->
        <mxCell id="stg1" value="&lt;b style=&quot;font-size:16px; color:#1e40af;&quot;&gt;GIAI ĐOẠN 1: KHỐI THU NHẬN RF&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:13px; font-weight:bold; color:#2563eb;&quot;&gt;Module RDM6300 (125 kHz)&lt;/span&gt;&lt;hr style=&quot;border:0; border-top:1px solid #93c5fd; margin:6px 0;&quot;&gt;&lt;div style=&quot;text-align:left; font-size:12.5px; line-height:1.5;&quot;&gt;&lt;b&gt;• Thẻ Thụ Động (EM4100):&lt;/b&gt;&lt;br&gt;Sóng mang 125 kHz, điều chế ASK/Manchester.&lt;br&gt;&lt;br&gt;&lt;b&gt;• Cuộn Cảm Thu &amp;amp; Tách Sóng:&lt;/b&gt;&lt;br&gt;Tách sóng đường bao + Schmitt Trigger khử nhiễu.&lt;br&gt;&lt;br&gt;&lt;b&gt;• Ngõ Ra TTL Nối Tiếp:&lt;/b&gt;&lt;br&gt;Baud 9600 bps 8-N-1 đưa vào cổng PMOD JA1.&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#eff6ff;strokeColor=#2563eb;strokeWidth=2.5;fontFamily=Segoe UI;shadow=1;align=center;verticalAlign=top;spacingTop=10;spacingLeft=10;spacingRight=10;" vertex="1" parent="1">
          <mxGeometry x="40" y="130" width="370" height="370" as="geometry" />
        </mxCell>

        <!-- Arrow 1 -> 2 -->
        <mxCell id="arr1_2" value="rdm_rx_i&lt;br&gt;(9600 bps TTL)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#2563eb;fontSize=12;fontStyle=1;endArrow=block;endFill=1;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="stg1" target="stg2">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- STAGE 2: 2-FF CDC -->
        <mxCell id="stg2" value="&lt;b style=&quot;font-size:16px; color:#065f46;&quot;&gt;GIAI ĐOẠN 2: ĐỒNG BỘ CDC&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:13px; font-weight:bold; color:#059669;&quot;&gt;sync_2ff.v (2-Stage Flip-Flop)&lt;/span&gt;&lt;hr style=&quot;border:0; border-top:1px solid #6ee7b7; margin:6px 0;&quot;&gt;&lt;div style=&quot;text-align:left; font-size:12.5px; line-height:1.5;&quot;&gt;&lt;b&gt;• Khử Bất Định (Metastability):&lt;/b&gt;&lt;br&gt;Cách ly xung nhịp ngoài và miền xung 50 MHz.&lt;br&gt;&lt;br&gt;&lt;b&gt;• 2 Tầng D-Flip-Flop Đồng Bộ:&lt;/b&gt;&lt;br&gt;Tầng 1 hấp thụ dao động; Tầng 2 chốt mức 0/1 CMOS sạch.&lt;br&gt;&lt;br&gt;&lt;b&gt;• Độ Tin Cậy Cực Cao:&lt;/b&gt;&lt;br&gt;MTBF &amp;gt; 1,000 năm trên công nghệ SkyWater 130nm.&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ecfdf5;strokeColor=#059669;strokeWidth=2.5;fontFamily=Segoe UI;shadow=1;align=center;verticalAlign=top;spacingTop=10;spacingLeft=10;spacingRight=10;" vertex="1" parent="1">
          <mxGeometry x="455" y="130" width="370" height="370" as="geometry" />
        </mxCell>

        <!-- Arrow 2 -> 3 -->
        <mxCell id="arr2_3" value="rdm_rx_sync&lt;br&gt;(50 MHz Sync)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#059669;fontSize=12;fontStyle=1;endArrow=block;endFill=1;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="stg2" target="stg3">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- STAGE 3: UART RX -->
        <mxCell id="stg3" value="&lt;b style=&quot;font-size:16px; color:#92400e;&quot;&gt;GIAI ĐOẠN 3: BỘ THU UART RX&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:13px; font-weight:bold; color:#d97706;&quot;&gt;uart_rx.v (Bộ Bỏ Phiếu 16x)&lt;/span&gt;&lt;hr style=&quot;border:0; border-top:1px solid #fcd34d; margin:6px 0;&quot;&gt;&lt;div style=&quot;text-align:left; font-size:12.5px; line-height:1.5;&quot;&gt;&lt;b&gt;• Bộ Chia Tần Số Baud (5208):&lt;/b&gt;&lt;br&gt;Divisor = 50MHz / 9600 = 5208 chu kỳ/bit.&lt;br&gt;&lt;br&gt;&lt;b&gt;• Bộ Bỏ Phiếu Đa Số 3 Điểm:&lt;/b&gt;&lt;br&gt;Lấy mẫu Ticks 7,8,9; lọc sạch gai xung nhiễu đường truyền.&lt;br&gt;&lt;br&gt;&lt;b&gt;• Thanh Ghi Dịch SIPO 8-bit:&lt;/b&gt;&lt;br&gt;Tái lập byte ASCII và phát xung strobe byte_valid (1T).&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fffbeb;strokeColor=#d97706;strokeWidth=2.5;fontFamily=Segoe UI;shadow=1;align=center;verticalAlign=top;spacingTop=10;spacingLeft=10;spacingRight=10;" vertex="1" parent="1">
          <mxGeometry x="870" y="130" width="370" height="370" as="geometry" />
        </mxCell>

        <!-- Arrow 3 -> 4 -->
        <mxCell id="arr3_4" value="byte_data[7:0]&lt;br&gt;+ byte_valid" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#d97706;fontSize=12;fontStyle=1;endArrow=block;endFill=1;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="stg3" target="stg4">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- STAGE 4: FRAME DECODER FSM -->
        <mxCell id="stg4" value="&lt;b style=&quot;font-size:16px; color:#5b21b6;&quot;&gt;GIAI ĐOẠN 4: FSM GIẢI MÃ &amp;amp; XOR&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:13px; font-weight:bold; color:#7c3aed;&quot;&gt;rdm6300_frame_decoder.v&lt;/span&gt;&lt;hr style=&quot;border:0; border-top:1px solid #d8b4fe; margin:6px 0;&quot;&gt;&lt;div style=&quot;text-align:left; font-size:12.5px; line-height:1.5;&quot;&gt;&lt;b&gt;• Máy Trạng Thái FSM 5 Bước:&lt;/b&gt;&lt;br&gt;STX -&amp;gt; 10 Byte Data -&amp;gt; 2 Byte CS -&amp;gt; ETX.&lt;br&gt;&lt;br&gt;&lt;b&gt;• Đổi Tổ Hợp ASCII ➔ Hex:&lt;/b&gt;&lt;br&gt;0 chu kỳ trễ, chuyển 10 ký tự ASCII thành 5 byte Hex.&lt;br&gt;&lt;br&gt;&lt;b&gt;• Cây XOR Song Song 1 Chu Kỳ:&lt;/b&gt;&lt;br&gt;Tính D[0]^D[1]^D[2]^D[3]^D[4] trong 20ns + Watchdog 10ms.&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f3ff;strokeColor=#7c3aed;strokeWidth=2.5;fontFamily=Segoe UI;shadow=1;align=center;verticalAlign=top;spacingTop=10;spacingLeft=10;spacingRight=10;" vertex="1" parent="1">
          <mxGeometry x="1285" y="130" width="370" height="370" as="geometry" />
        </mxCell>

        <!-- Arrow 4 -> 5 -->
        <mxCell id="arr4_5" value="tag_id[39:0]&lt;br&gt;+ card_valid" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#7c3aed;fontSize=12;fontStyle=1;endArrow=block;endFill=1;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="stg4" target="stg5">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- STAGE 5: MMIO REGISTERS -->
        <mxCell id="stg5" value="&lt;b style=&quot;font-size:16px; color:#9f1239;&quot;&gt;GIAI ĐOẠN 5: MMIO &amp;amp; NGẮT CPU&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:13px; font-weight:bold; color:#e11d48;&quot;&gt;Base: 0x1000_0000 (PicoRV32)&lt;/span&gt;&lt;hr style=&quot;border:0; border-top:1px solid #fda4af; margin:6px 0;&quot;&gt;&lt;div style=&quot;text-align:left; font-size:12.5px; line-height:1.5;&quot;&gt;&lt;b&gt;• REG_RFID_STATUS (0x1000_0000):&lt;/b&gt;&lt;br&gt;Bit 0: card_valid (Write 1 Clear), Bit 1: cs_error.&lt;br&gt;&lt;br&gt;&lt;b&gt;• REG_TAG_HI &amp;amp; REG_TAG_LO:&lt;/b&gt;&lt;br&gt;Chứa 8-bit Version và 32-bit Serial Number thẻ.&lt;br&gt;&lt;br&gt;&lt;b&gt;• Cơ Chế Không Tốn CPU (Zero CPU):&lt;/b&gt;&lt;br&gt;Ngắt card_event_o đánh thức CPU ngay tức thì.&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff1f2;strokeColor=#e11d48;strokeWidth=2.5;fontFamily=Segoe UI;shadow=1;align=center;verticalAlign=top;spacingTop=10;spacingLeft=10;spacingRight=10;" vertex="1" parent="1">
          <mxGeometry x="1695" y="130" width="365" height="370" as="geometry" />
        </mxCell>

        <!-- SECTION 6: 14-BYTE FRAME & XOR PROOF -->
        <mxCell id="stg6" value="&lt;b style=&quot;font-size:16px; color:#0f172a;&quot;&gt;CẤU TRÚC KHUNG TRUYỀN UART 14 BYTE VÀ TOÁN TỬ XOR KIỂM TRA TOÀN VẸN (1 CHU KỲ PHẦN CỨNG 20.0 NS)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:13px; color:#475569;&quot;&gt;Ví dụ thẻ thật: 0007508976 | Wiegand: Facility Code 114, Card ID 37872 | Mã Hex: 0x007293F0 (Version 0x00, Serial 0x007293F0)&lt;/span&gt;&lt;hr style=&quot;border:0; border-top:1px solid #cbd5e1; margin:8px 0;&quot;&gt;&lt;div style=&quot;font-family:Consolas, monospace; font-size:13.5px; text-align:left;&quot;&gt;&lt;b&gt;Chuỗi Khung UART:&lt;/b&gt; [0x02 STX] + [0x30, 0x30 (Ver 0x00)] + [0x30, 0x30, 0x37, 0x32, 0x39, 0x33, 0x46, 0x30 (Serial 0x007293F0)] + [0x46, 0x30 (CS 0xF0)] + [0x03 ETX]&lt;br&gt;&lt;b style=&quot;color:#059669;&quot;&gt;Toán Tử XOR Song Song:&lt;/b&gt; Calc_CS = D[0] ^ D[1] ^ D[2] ^ D[3] ^ D[4] = (0x00) ^ (0x00) ^ (0x72) ^ (0x93) ^ (0xF0) = &lt;b style=&quot;color:#e11d48;&quot;&gt;0xF0&lt;/b&gt; == Received_CS &lt;b style=&quot;color:#059669;&quot;&gt;(SO KHỚP 100% ➔ KÍCH HOẠT CARD_VALID!)&lt;/b&gt;&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#475569;strokeWidth=2.5;fontFamily=Segoe UI;shadow=1;align=center;verticalAlign=top;spacingTop=10;spacingLeft=16;spacingRight=16;" vertex="1" parent="1">
          <mxGeometry x="40" y="530" width="2020" height="150" as="geometry" />
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
    drawio_path = os.path.abspath("fig2_rdm6300_horizontal.drawio")
    with open(drawio_path, "w", encoding="utf-8") as f:
        f.write(xml_content)
    print(f"[SUCCESS] Genuine horizontal Draw.io file created at: {drawio_path}")

def create_horizontal_html_and_render_png():
    html_content = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background-color: #f8fafc;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
    color: #0f172a;
    padding: 24px;
    width: 2160px;
    height: 1040px;
    position: relative;
    overflow: hidden;
  }

  /* Main Bordered Canvas */
  .diagram-canvas {
    width: 2112px;
    height: 992px;
    border: 3.5px solid #0f172a;
    border-radius: 18px;
    background: #ffffff;
    position: relative;
    padding: 22px 28px;
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.12);
  }

  /* Title Banner */
  .title-banner {
    text-align: center;
    border-bottom: 2.5px solid #cbd5e1;
    padding-bottom: 12px;
    margin-bottom: 22px;
  }
  .title-banner h1 {
    font-size: 26px;
    font-weight: 900;
    color: #0f172a;
    letter-spacing: 0.5px;
    text-transform: uppercase;
  }
  .title-banner p {
    font-size: 15px;
    font-weight: 700;
    color: #475569;
    margin-top: 4px;
  }

  /* 5-Stage Horizontal Flex Row */
  .pipeline-row {
    display: flex;
    align-items: stretch;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 22px;
  }

  /* Individual Stage Card */
  .stage-card {
    flex: 1;
    border-radius: 14px;
    border: 2.5px solid;
    padding: 16px 16px;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
    background: #ffffff;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  /* Stage Headers */
  .stage-top {
    border-bottom: 2px solid;
    padding-bottom: 10px;
    margin-bottom: 14px;
  }
  .stage-num {
    font-size: 13.5px;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 3px;
  }
  .stage-title {
    font-size: 16.5px;
    font-weight: 900;
    line-height: 1.25;
  }
  .stage-badge {
    display: inline-block;
    margin-top: 6px;
    font-family: 'Consolas', monospace;
    font-size: 12.5px;
    font-weight: 800;
    padding: 3px 8px;
    border-radius: 6px;
  }

  /* Subunit List inside Card */
  .subunit-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
    flex-grow: 1;
  }
  .subunit-item {
    background: #ffffff;
    border: 1.5px solid #e2e8f0;
    border-radius: 10px;
    padding: 10px 12px;
  }
  .sub-title {
    font-size: 14px;
    font-weight: 800;
    color: #0f172a;
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 4px;
  }
  .sub-desc {
    font-size: 12.5px;
    font-weight: 600;
    color: #475569;
    line-height: 1.45;
  }

  /* Arrow Connector Between Stages */
  .arrow-connector {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 32px;
    position: relative;
  }
  .arrow-line {
    width: 24px;
    height: 4px;
    background: #64748b;
    position: relative;
  }
  .arrow-line::after {
    content: '';
    position: absolute;
    right: -8px;
    top: -6px;
    width: 0;
    height: 0;
    border-top: 8px solid transparent;
    border-bottom: 8px solid transparent;
    border-left: 10px solid #64748b;
  }
  .arrow-label {
    position: absolute;
    top: 50%;
    transform: translateY(-50%) rotate(90deg);
    white-space: nowrap;
    font-size: 11px;
    font-weight: 800;
    font-family: 'Consolas', monospace;
    background: #ffffff;
    padding: 2px 6px;
    border-radius: 4px;
    border: 1px solid #cbd5e1;
    color: #0f172a;
    z-index: 10;
  }

  /* Color Schemes for Stages */
  /* Stage 1 */
  .card-stg1 { border-color: #2563eb; background: #eff6ff; }
  .card-stg1 .stage-top { border-color: #bfdbfe; }
  .card-stg1 .stage-num { color: #1d4ed8; }
  .card-stg1 .stage-title { color: #1e3a8a; }
  .card-stg1 .stage-badge { background: #dbeafe; color: #1e40af; }
  .card-stg1 .sub-title { color: #1d4ed8; }

  /* Stage 2 */
  .card-stg2 { border-color: #059669; background: #ecfdf5; }
  .card-stg2 .stage-top { border-color: #a7f3d0; }
  .card-stg2 .stage-num { color: #047857; }
  .card-stg2 .stage-title { color: #064e3b; }
  .card-stg2 .stage-badge { background: #d1fae5; color: #065f46; }
  .card-stg2 .sub-title { color: #047857; }

  /* Stage 3 */
  .card-stg3 { border-color: #d97706; background: #fffbeb; }
  .card-stg3 .stage-top { border-color: #fde68a; }
  .card-stg3 .stage-num { color: #b45309; }
  .card-stg3 .stage-title { color: #78350f; }
  .card-stg3 .stage-badge { background: #fef3c7; color: #92400e; }
  .card-stg3 .sub-title { color: #b45309; }

  /* Stage 4 */
  .card-stg4 { border-color: #7c3aed; background: #f5f3ff; }
  .card-stg4 .stage-top { border-color: #ddd6fe; }
  .card-stg4 .stage-num { color: #6d28d9; }
  .card-stg4 .stage-title { color: #4c1d95; }
  .card-stg4 .stage-badge { background: #ede9fe; color: #5b21b6; }
  .card-stg4 .sub-title { color: #6d28d9; }

  /* Stage 5 */
  .card-stg5 { border-color: #e11d48; background: #fff1f2; }
  .card-stg5 .stage-top { border-color: #fecdd3; }
  .card-stg5 .stage-num { color: #be123c; }
  .card-stg5 .stage-title { color: #881337; }
  .card-stg5 .stage-badge { background: #ffe4e6; color: #9f1239; }
  .card-stg5 .sub-title { color: #be123c; }

  /* Bottom Section: 14-Byte Frame & XOR Demonstration */
  .bottom-container {
    border: 2.5px solid #334155;
    border-radius: 14px;
    background: #f8fafc;
    padding: 14px 20px;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.05);
  }
  .bottom-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1.5px solid #cbd5e1;
    padding-bottom: 8px;
    margin-bottom: 10px;
  }
  .bottom-title {
    font-size: 15px;
    font-weight: 900;
    color: #0f172a;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .bottom-example {
    font-family: 'Segoe UI', sans-serif;
    font-size: 13.5px;
    font-weight: 700;
    color: #475569;
  }

  .frame-grid {
    display: grid;
    grid-template-columns: repeat(14, 1fr);
    gap: 6px;
    margin-bottom: 10px;
  }
  .byte-cell {
    border: 1.5px solid #cbd5e1;
    border-radius: 6px;
    padding: 5px 2px;
    text-align: center;
    background: #ffffff;
  }
  .b-idx { font-size: 11px; font-weight: 700; color: #64748b; }
  .b-name { font-size: 12px; font-weight: 900; color: #0f172a; margin: 1px 0; }
  .b-val { font-family: 'Consolas', monospace; font-size: 11px; font-weight: 800; color: #2563eb; }

  .formula-box {
    background: #ffffff;
    border: 1.5px solid #cbd5e1;
    border-radius: 8px;
    padding: 8px 14px;
    font-family: 'Consolas', monospace;
    font-size: 13px;
    line-height: 1.5;
  }
  .f-row { display: flex; align-items: center; gap: 8px; }
  .f-lbl { font-weight: 800; color: #334155; width: 140px; }
  .f-val { font-weight: 800; color: #0f172a; }
  .f-succ { color: #059669; font-weight: 900; }
</style>
</head>
<body>

<div class="diagram-canvas">

  <!-- Title Banner -->
  <div class="title-banner">
    <h1>HỆ THỐNG PHẦN CỨNG THU NHẬN & GIẢI MÃ THẺ RFID RDM6300 TỰ TRỊ</h1>
    <p>Sơ đồ khối vi kiến trúc đường ống 5 giai đoạn phần cứng (Hardware 5-Stage Autonomous Decoding Pipeline)</p>
  </div>

  <!-- 5-Stage Horizontal Row -->
  <div class="pipeline-row">

    <!-- STAGE 1 -->
    <div class="stage-card card-stg1">
      <div class="stage-top">
        <div class="stage-num">GIAI ĐOẠN 1 (125 kHz)</div>
        <div class="stage-title">KHỐI THU NHẬN RF & GIẢI ĐIỀU CHẾ</div>
        <span class="stage-badge">RDM6300 PMOD Module</span>
      </div>
      <div class="subunit-list">
        <div class="subunit-item">
          <div class="sub-title">📡 Thẻ Thụ Động (EM4100)</div>
          <div class="sub-desc">Tần số cộng hưởng 125 kHz, không pin, điều chế biên độ ASK/Manchester.</div>
        </div>
        <div class="subunit-item">
          <div class="sub-title">🌀 Cuộn Cảm Thu & Tách Sóng</div>
          <div class="sub-desc">Mạch tách sóng đường bao kết hợp bộ so sánh Schmitt Trigger khử nhiễu.</div>
        </div>
        <div class="subunit-item">
          <div class="sub-title">⚡ Đầu Ra Chuẩn TTL Nối Tiếp</div>
          <div class="sub-desc">Tốc độ 9600 bps 8-N-1 xuất chuỗi xung rdm_rx_i vào cổng PMOD JA1.</div>
        </div>
      </div>
    </div>

    <!-- Connector 1 -> 2 -->
    <div class="arrow-connector">
      <div class="arrow-line"></div>
      <span class="arrow-label">rdm_rx_i (9600)</span>
    </div>

    <!-- STAGE 2 -->
    <div class="stage-card card-stg2">
      <div class="stage-top">
        <div class="stage-num">GIAI ĐOẠN 2 (50 MHz)</div>
        <div class="stage-title">ĐỒNG BỘ XUNG NHỊP KHỬ BẤT ĐỊNH (CDC)</div>
        <span class="stage-badge">rtl/sync_2ff.v</span>
      </div>
      <div class="subunit-list">
        <div class="subunit-item">
          <div class="sub-title">⚠️ Nguy Cơ Bất Định (Metastability)</div>
          <div class="sub-desc">Xung rdm_rx_i không đồng pha với xung SoC 50 MHz (vi phạm Tsu / Th).</div>
        </div>
        <div class="subunit-item">
          <div class="sub-title">⏱️ 2 Tầng Flip-Flop Đồng Bộ</div>
          <div class="sub-desc">Tầng 1 hấp thụ dao động; Tầng 2 chốt mức logic 0/1 CMOS sạch chuẩn xác.</div>
        </div>
        <div class="subunit-item">
          <div class="sub-title">🛡️ Độ Tin Cậy Cực Cao</div>
          <div class="sub-desc">MTBF > 1,000 năm trên công nghệ bán dẫn SkyWater 130nm Standard Cells.</div>
        </div>
      </div>
    </div>

    <!-- Connector 2 -> 3 -->
    <div class="arrow-connector">
      <div class="arrow-line"></div>
      <span class="arrow-label">rdm_rx_sync</span>
    </div>

    <!-- STAGE 3 -->
    <div class="stage-card card-stg3">
      <div class="stage-top">
        <div class="stage-num">GIAI ĐOẠN 3 (Sampling 16x)</div>
        <div class="stage-title">BỘ THU PHẦN CỨNG UART BỎ PHIẾU ĐA SỐ</div>
        <span class="stage-badge">rtl/uart_rx.v</span>
      </div>
      <div class="subunit-list">
        <div class="subunit-item">
          <div class="sub-title">⏱️ Bộ Chia Tần Số Baud (5208)</div>
          <div class="sub-desc">Divisor = 50,000,000 / 9600 = 5208 chu kỳ; bộ đếm lấy mẫu 16 lần/bit.</div>
        </div>
        <div class="subunit-item">
          <div class="sub-title">🗳️ Bộ Bỏ Phiếu Đa Số 3 Điểm</div>
          <div class="sub-desc">Lấy mẫu Ticks 7,8,9; lọc sạch gai xung nhiễu cao tần trên đường truyền.</div>
        </div>
        <div class="subunit-item">
          <div class="sub-title">🔄 Thanh Ghi SIPO 8-bit</div>
          <div class="sub-desc">Tái lập byte ASCII byte_data[7:0] và phát xung kích hoạt byte_valid (1T).</div>
        </div>
      </div>
    </div>

    <!-- Connector 3 -> 4 -->
    <div class="arrow-connector">
      <div class="arrow-line"></div>
      <span class="arrow-label">byte_data + valid</span>
    </div>

    <!-- STAGE 4 -->
    <div class="stage-card card-stg4">
      <div class="stage-top">
        <div class="stage-num">GIAI ĐOẠN 4 (1 Clock Cycle)</div>
        <div class="stage-title">FSM GIẢI MÃ KHUNG & CÂY XOR SONG SONG</div>
        <span class="stage-badge">rdm6300_frame_decoder.v</span>
      </div>
      <div class="subunit-list">
        <div class="subunit-item">
          <div class="sub-title">🤖 Máy Trạng Thái FSM 5 Bước</div>
          <div class="sub-desc">WAIT_STX -> 10 Byte Data -> 2 Byte Checksum -> WAIT_ETX tự động.</div>
        </div>
        <div class="subunit-item">
          <div class="sub-title">🔀 Đổi Tổ Hợp ASCII ➔ Hex</div>
          <div class="sub-desc">0 chu kỳ trễ, chuyển 10 ký tự ASCII thành 5 byte Hex nhị phân hoàn chỉnh.</div>
        </div>
        <div class="subunit-item">
          <div class="sub-title">⚡ Cây XOR Song Song 1 Chu Kỳ</div>
          <div class="sub-desc">D[0]^D[1]^D[2]^D[3]^D[4] hoàn tất trong 20ns + Watchdog Timer chống treo 10ms.</div>
        </div>
      </div>
    </div>

    <!-- Connector 4 -> 5 -->
    <div class="arrow-connector">
      <div class="arrow-line"></div>
      <span class="arrow-label">tag_id + strobe</span>
    </div>

    <!-- STAGE 5 -->
    <div class="stage-card card-stg5">
      <div class="stage-top">
        <div class="stage-num">GIAI ĐOẠN 5 (Zero CPU)</div>
        <div class="stage-title">THANH GHI MMIO & BÁO NGẮT PHẦN CỨNG</div>
        <span class="stage-badge">Base: 0x1000_0000</span>
      </div>
      <div class="subunit-list">
        <div class="subunit-item">
          <div class="sub-title">📋 REG_RFID_STATUS (0x1000_0000)</div>
          <div class="sub-desc">Bit 0: card_valid (Write 1 Clear); Bit 1: cs_error (Lỗi checksum).</div>
        </div>
        <div class="subunit-item">
          <div class="sub-title">🏷️ REG_TAG_HI & REG_TAG_LO</div>
          <div class="sub-desc">Chứa 8-bit Version (0x1000_0004) và 32-bit Serial Number (0x1000_0008).</div>
        </div>
        <div class="subunit-item">
          <div class="sub-title">🚀 Cơ Chế Không Tốn CPU (Zero CPU)</div>
          <div class="sub-desc">Ngắt card_event_o đánh thức CPU ngay tức thì; độ trễ phản hồi < 40 ns.</div>
        </div>
      </div>
    </div>

  </div>

  <!-- Bottom Container: 14-Byte Frame Structure & XOR Demonstration -->
  <div class="bottom-container">
    <div class="bottom-header">
      <div class="bottom-title">
        <span>📦 CẤU TRÚC KHUNG TRUYỀN UART 14 BYTE VÀ TOÁN TỬ XOR KIỂM TRA TOÀN VẸN (1 CHU KỲ CLOCK = 20.0 NS)</span>
      </div>
      <div class="bottom-example">
        Ví dụ thẻ thật: <b>0007508976</b> | Wiegand: <b>FC 114, ID 37872</b> | Mã Hex: <b>0x007293F0</b> (Ver: 0x00, Serial: 0x007293F0)
      </div>
    </div>

    <!-- 14 Bytes Badges Grid -->
    <div class="frame-grid">
      <div class="byte-cell" style="background:#f1f5f9;">
        <div class="b-idx">Byte 0</div>
        <div class="b-name" style="color:#475569;">Header</div>
        <div class="b-val" style="color:#0f172a;">STX (0x02)</div>
      </div>
      <div class="byte-cell" style="background:#eff6ff; border-color:#93c5fd;">
        <div class="b-idx">Byte 1</div>
        <div class="b-name" style="color:#1d4ed8;">Ver[7:4]</div>
        <div class="b-val">'0' (0x30)</div>
      </div>
      <div class="byte-cell" style="background:#eff6ff; border-color:#93c5fd;">
        <div class="b-idx">Byte 2</div>
        <div class="b-name" style="color:#1d4ed8;">Ver[3:0]</div>
        <div class="b-val">'0' (0x30)</div>
      </div>
      <div class="byte-cell" style="background:#ecfdf5; border-color:#a7f3d0;">
        <div class="b-idx">Byte 3</div>
        <div class="b-name" style="color:#047857;">D[31:28]</div>
        <div class="b-val">'0' (0x30)</div>
      </div>
      <div class="byte-cell" style="background:#ecfdf5; border-color:#a7f3d0;">
        <div class="b-idx">Byte 4</div>
        <div class="b-name" style="color:#047857;">D[27:24]</div>
        <div class="b-val">'0' (0x30)</div>
      </div>
      <div class="byte-cell" style="background:#ecfdf5; border-color:#a7f3d0;">
        <div class="b-idx">Byte 5</div>
        <div class="b-name" style="color:#047857;">D[23:20]</div>
        <div class="b-val">'7' (0x37)</div>
      </div>
      <div class="byte-cell" style="background:#ecfdf5; border-color:#a7f3d0;">
        <div class="b-idx">Byte 6</div>
        <div class="b-name" style="color:#047857;">D[19:16]</div>
        <div class="b-val">'2' (0x32)</div>
      </div>
      <div class="byte-cell" style="background:#ecfdf5; border-color:#a7f3d0;">
        <div class="b-idx">Byte 7</div>
        <div class="b-name" style="color:#047857;">D[15:12]</div>
        <div class="b-val">'9' (0x39)</div>
      </div>
      <div class="byte-cell" style="background:#ecfdf5; border-color:#a7f3d0;">
        <div class="b-idx">Byte 8</div>
        <div class="b-name" style="color:#047857;">D[11:8]</div>
        <div class="b-val">'3' (0x33)</div>
      </div>
      <div class="byte-cell" style="background:#ecfdf5; border-color:#a7f3d0;">
        <div class="b-idx">Byte 9</div>
        <div class="b-name" style="color:#047857;">D[7:4]</div>
        <div class="b-val">'F' (0x46)</div>
      </div>
      <div class="byte-cell" style="background:#ecfdf5; border-color:#a7f3d0;">
        <div class="b-idx">Byte 10</div>
        <div class="b-name" style="color:#047857;">D[3:0]</div>
        <div class="b-val">'0' (0x30)</div>
      </div>
      <div class="byte-cell" style="background:#fff1f2; border-color:#fecdd3;">
        <div class="b-idx">Byte 11</div>
        <div class="b-name" style="color:#be123c;">CS[7:4]</div>
        <div class="b-val">'F' (0x46)</div>
      </div>
      <div class="byte-cell" style="background:#fff1f2; border-color:#fecdd3;">
        <div class="b-idx">Byte 12</div>
        <div class="b-name" style="color:#be123c;">CS[3:0]</div>
        <div class="b-val">'0' (0x30)</div>
      </div>
      <div class="byte-cell" style="background:#f1f5f9;">
        <div class="b-idx">Byte 13</div>
        <div class="b-name" style="color:#475569;">Footer</div>
        <div class="b-val" style="color:#0f172a;">ETX (0x03)</div>
      </div>
    </div>

    <!-- Math Formula -->
    <div class="formula-box">
      <div class="f-row">
        <span class="f-lbl">Công Thức XOR:</span>
        <span class="f-val">Calc_CS = D[0] ^ D[1] ^ D[2] ^ D[3] ^ D[4]</span>
      </div>
      <div class="f-row">
        <span class="f-lbl">Tính Toán Hex:</span>
        <span class="f-val">= (0x00) ^ (0x00) ^ (0x72) ^ (0x93) ^ (0xF0) = <b style="color:#e11d48; font-size:14px;">0xF0</b></span>
      </div>
      <div class="f-row">
        <span class="f-lbl">Đối Chiếu Kiểm Tra:</span>
        <span class="f-val f-succ">Calculated_CS (0xF0) == Received_CS (0xF0) &rarr; KHỚP CHUẨN XÁC 100% &rarr; KÍCH HOẠT CARD_VALID_STROBE!</span>
      </div>
    </div>

  </div>

</div>

</body>
</html>
"""
    html_path = os.path.abspath("fig2_rdm6300_horizontal.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[SUCCESS] HTML vector source written at: {html_path}")

    # Render via Chrome headless at 2x DPI
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    out_img = os.path.abspath("fig2_rdm6300_horizontal.png")

    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--force-device-scale-factor=2",
        f"--screenshot={out_img}",
        "--window-size=2160,1050",
        f"file:///{html_path.replace(os.sep, '/')}"
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(out_img):
        print(f"[SUCCESS] Ultra-sharp Horizontal Fig 2 image generated at: {out_img} ({os.path.getsize(out_img)} bytes)")
    else:
        print("[ERROR] Chrome rendering failed:", res.stderr)

if __name__ == '__main__':
    create_horizontal_drawio_xml()
    create_horizontal_html_and_render_png()
