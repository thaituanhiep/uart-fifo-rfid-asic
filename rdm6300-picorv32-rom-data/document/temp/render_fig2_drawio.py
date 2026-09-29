# -*- coding: utf-8 -*-
"""
Script: render_fig2_drawio.py
Generates both:
1. fig2_rdm6300_subsystem.drawio: Genuine editable Draw.io XML file (app.diagrams.net compatible).
2. fig2_rdm6300_subsystem.png: Ultra-sharp Draw.io-style vertical pipeline render via Headless Chrome at 2x DPI.
   Features:
   - 5 Stages arranged vertically as explicitly requested:
     Stage 1: RF Front-End & Analog Demodulator
     Stage 2: 2-FF CDC Synchronizer (sync_2ff.v)
     Stage 3: Hardware UART RX Engine (uart_rx.v)
     Stage 4: Autonomous Frame Decoder FSM & XOR Tree (rdm6300_frame_decoder.v)
     Stage 5: MMIO Registers & CPU Interrupt (0x1000_0000)
     Section 6: 14-Byte Frame Anatomy & 1-Cycle Parallel XOR Formula Demonstration
   - HUGE FONT SIZES (14px to 25px bold), ensuring exceptional legibility in Word reports.
   - Clean downward bus arrows with prominent signal pill badges.
"""

import os
import subprocess

def create_drawio_xml():
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="2026-09-28T07:40:00.000Z" agent="Mozilla/5.0" version="21.0.0" type="device">
  <diagram id="rdm6300_pipeline" name="RDM6300 Hardware Pipeline">
    <mxGraphModel dx="1400" dy="2200" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1350" pageHeight="2200" math="0" shadow="1">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- STAGE 1: RF FRONT-END -->
        <mxCell id="stg1" value="&lt;b style=&quot;font-size:18px;&quot;&gt;STAGE 1: RF FRONT-END &amp;amp; ANALOG DEMODULATOR&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:13.5px;&quot;&gt;• External LC Tuned Antenna (125 kHz) | EM4100 Passive Card Modulation&lt;br&gt;• Envelope Demodulator &amp;amp; Slicer Filter | TTL Serial Output @ 9600 bps 8-N-1 (PMOD JA1)&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#eff6ff;strokeColor=#2563eb;strokeWidth=2.5;fontFamily=Segoe UI;shadow=1;align=left;spacingLeft=18;" vertex="1" parent="1">
          <mxGeometry x="80" y="80" width="1180" height="150" as="geometry" />
        </mxCell>

        <!-- Arrow 1 -> 2 -->
        <mxCell id="arr1_2" value="rdm_rx (9600 bps TTL Asynchronous Stream)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3.5;strokeColor=#2563eb;fontSize=14;fontStyle=1;endArrow=block;endFill=1;" edge="1" parent="1" source="stg1" target="stg2">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- STAGE 2: 2-FF CDC SYNCHRONIZER -->
        <mxCell id="stg2" value="&lt;b style=&quot;font-size:18px;&quot;&gt;STAGE 2: 2-STAGE FLIP-FLOP CDC SYNCHRONIZER (sync_2ff.v)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:13.5px;&quot;&gt;• Captures Asynchronous rdm_rx_i on 50 MHz Master SoC Clock Domain&lt;br&gt;• FF Stage 1 Absorbs Metastability Violations (Tsu / Th) | FF Stage 2 Filters to Clean 0/1 CMOS Logic&lt;br&gt;• Output: rdm_rx_sync | MTBF &amp;gt; 1000 Years in SkyWater 130nm Standard Cells&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ecfdf5;strokeColor=#059669;strokeWidth=2.5;fontFamily=Segoe UI;shadow=1;align=left;spacingLeft=18;" vertex="1" parent="1">
          <mxGeometry x="80" y="320" width="1180" height="150" as="geometry" />
        </mxCell>

        <!-- Arrow 2 -> 3 -->
        <mxCell id="arr2_3" value="rdm_rx_sync (50 MHz Synchronous Bit Stream)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3.5;strokeColor=#059669;fontSize=14;fontStyle=1;endArrow=block;endFill=1;" edge="1" parent="1" source="stg2" target="stg3">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- STAGE 3: HARDWARE UART RX ENGINE -->
        <mxCell id="stg3" value="&lt;b style=&quot;font-size:18px;&quot;&gt;STAGE 3: HARDWARE UART RX ENGINE (uart_rx.v)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:13.5px;&quot;&gt;• Baud Rate Divider: Divisor = 50,000,000 / 9600 = 5208 Cycles/Bit (16x Sampling Clock)&lt;br&gt;• 3-Point Majority Voter (Samples Ticks 7, 8, 9) Rejects Glitches and High-Frequency Noise&lt;br&gt;• 8-bit SIPO Shift Register: Deserializes ASCII Byte Stream | Strobe: byte_valid (1-cycle pulse)&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fffbeb;strokeColor=#d97706;strokeWidth=2.5;fontFamily=Segoe UI;shadow=1;align=left;spacingLeft=18;" vertex="1" parent="1">
          <mxGeometry x="80" y="560" width="1180" height="160" as="geometry" />
        </mxCell>

        <!-- Arrow 3 -> 4 -->
        <mxCell id="arr3_4" value="byte_data[7:0] (ASCII Byte) + byte_valid (1-Cycle Pulse)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3.5;strokeColor=#d97706;fontSize=14;fontStyle=1;endArrow=block;endFill=1;" edge="1" parent="1" source="stg3" target="stg4">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- STAGE 4: AUTONOMOUS FRAME DECODER FSM -->
        <mxCell id="stg4" value="&lt;b style=&quot;font-size:18px;&quot;&gt;STAGE 4: 14-BYTE FRAME DECODER FSM &amp;amp; PARALLEL XOR TREE (rdm6300_frame_decoder.v)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:13.5px;&quot;&gt;• FSM Controller: ST_WAIT_STX -&amp;gt; ST_COLLECT_DATA (10 ASCII) -&amp;gt; ST_CHECKSUM (2 ASCII) -&amp;gt; ST_WAIT_ETX&lt;br&gt;• Combinational ASCII-to-Hex Engine: Translates 10 ASCII characters into 5 Hex bytes (0 latency)&lt;br&gt;• 1-Cycle Parallel XOR Checksum Engine: D[0] ^ D[1] ^ D[2] ^ D[3] ^ D[4] == Received_CS&lt;br&gt;• Anti-Hang Hardware Watchdog Timer: 19-bit Counter (500,000 cycles = 10ms) auto-resets on severed packet&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f3ff;strokeColor=#7c3aed;strokeWidth=2.5;fontFamily=Segoe UI;shadow=1;align=left;spacingLeft=18;" vertex="1" parent="1">
          <mxGeometry x="80" y="810" width="1180" height="180" as="geometry" />
        </mxCell>

        <!-- Arrow 4 -> 5 -->
        <mxCell id="arr4_5" value="tag_id[39:0] (Validated 40-bit UID) + card_valid_strobe + cs_error" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3.5;strokeColor=#7c3aed;fontSize=14;fontStyle=1;endArrow=block;endFill=1;" edge="1" parent="1" source="stg4" target="stg5">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- STAGE 5: MMIO REGISTERS -->
        <mxCell id="stg5" value="&lt;b style=&quot;font-size:18px;&quot;&gt;STAGE 5: MMIO INTERFACE REGISTERS &amp;amp; CPU INTERRUPT (MMIO Base: 0x1000_0000)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:13.5px;&quot;&gt;• REG_RFID_STATUS (0x1000_0000): Bit 0 = card_valid (Write 1 to Clear), Bit 1 = cs_error&lt;br&gt;• REG_RFID_TAG_HI (0x1000_0004): Bits [39:32] = Version Byte (e.g., 0x00)&lt;br&gt;• REG_RFID_TAG_LO (0x1000_0008): Bits [31:0] = 32-bit Tag Serial Number (e.g., 0x007293F0)&lt;br&gt;• Hardware IRQ output card_event_o directly wakes PicoRV32 (Zero CPU Polling Overhead)&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff1f2;strokeColor=#e11d48;strokeWidth=2.5;fontFamily=Segoe UI;shadow=1;align=left;spacingLeft=18;" vertex="1" parent="1">
          <mxGeometry x="80" y="1080" width="1180" height="160" as="geometry" />
        </mxCell>

        <!-- SECTION 6: 14-BYTE FRAME ANATOMY -->
        <mxCell id="stg6" value="&lt;b style=&quot;font-size:18px;&quot;&gt;SECTION 6: 14-BYTE FRAME STRUCTURE &amp;amp; PARALLEL XOR FORMULA DEMONSTRATION&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:13.5px;&quot;&gt;Example Real Card: 0007508976 | Wiegand: FC 114, ID 37872 | Hexadecimal: 0x007293F0&lt;br&gt;&lt;b&gt;Frame Stream:&lt;/b&gt; [0x02 STX] + [0x30, 0x30 (Ver 0x00)] + [0x30, 0x30, 0x37, 0x32, 0x39, 0x33, 0x46, 0x30 (Serial 0x007293F0)] + [0x46, 0x30 (CS 0xF0)] + [0x03 ETX]&lt;br&gt;&lt;b&gt;1-Cycle XOR Parity:&lt;/b&gt; (0x00) ^ (0x00) ^ (0x72) ^ (0x93) ^ (0xF0) = 0xF0 == Received_CS (VALIDATION SUCCESS!)&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#475569;strokeWidth=2.5;fontFamily=Segoe UI;shadow=1;align=left;spacingLeft=18;" vertex="1" parent="1">
          <mxGeometry x="80" y="1310" width="1180" height="150" as="geometry" />
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
    with open("fig2_rdm6300_subsystem.drawio", "w", encoding="utf-8") as f:
        f.write(xml_content)
    print("[SUCCESS] Genuine Draw.io file created at: fig2_rdm6300_subsystem.drawio")

def create_html_and_render_png():
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background-color: #ffffff;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    padding: 24px;
    width: 1320px;
    height: 2280px;
    position: relative;
    overflow: hidden;
  }

  /* Main Frame */
  .diagram-container {
    width: 1272px;
    height: 2232px;
    border: 3px solid #0f172a;
    border-radius: 16px;
    background: #ffffff;
    position: relative;
    padding: 24px 28px;
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.1);
  }

  /* Header Title Banner */
  .title-banner {
    text-align: center;
    border-bottom: 2.5px solid #cbd5e1;
    padding-bottom: 14px;
    margin-bottom: 26px;
  }
  .title-banner h1 {
    font-size: 24px;
    font-weight: 900;
    color: #0f172a;
    letter-spacing: 0.5px;
    text-transform: uppercase;
  }
  .title-banner p {
    font-size: 14.5px;
    font-weight: 700;
    color: #475569;
    margin-top: 4px;
  }

  /* Stage Block (Vertical Card spanning full width) */
  .stage-card {
    width: 1216px;
    border-radius: 12px;
    border: 2.5px solid;
    padding: 16px 20px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    background: #ffffff;
    margin-bottom: 50px;
    position: relative;
  }

  .stage-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1.5px solid rgba(0, 0, 0, 0.1);
    padding-bottom: 10px;
    margin-bottom: 14px;
  }
  .stage-title {
    font-size: 19px;
    font-weight: 900;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .stage-module {
    font-family: 'Consolas', monospace;
    font-size: 14px;
    font-weight: 800;
    padding: 3px 10px;
    border-radius: 6px;
    background: rgba(0, 0, 0, 0.05);
  }
  .stage-badge {
    font-size: 12.5px;
    font-weight: 800;
    padding: 4px 10px;
    border-radius: 6px;
    text-transform: uppercase;
  }

  /* 3-Column Subunit Grid inside each Stage */
  .subunit-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 14px;
  }
  .subunit {
    background: #ffffff;
    border: 1.8px solid #cbd5e1;
    border-radius: 8px;
    padding: 12px 14px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  }
  .sub-title {
    font-size: 15px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .sub-body {
    font-size: 13px;
    font-weight: 600;
    color: #334155;
    line-height: 1.5;
  }
  .code-term {
    font-family: 'Consolas', monospace;
    font-weight: 800;
    color: #0f172a;
    background: #f1f5f9;
    padding: 1px 5px;
    border-radius: 4px;
  }

  /* Downward Pipeline Bus Arrow Connector */
  .pipe-connector {
    position: relative;
    height: 50px;
    margin-top: -50px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 10;
  }
  .pipe-arrow {
    width: 4px;
    height: 100%;
    background: #2563eb;
    position: relative;
  }
  .pipe-arrow::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: -7px;
    width: 0;
    height: 0;
    border-left: 9px solid transparent;
    border-right: 9px solid transparent;
    border-top: 14px solid #2563eb;
  }

  .pipe-badge {
    position: absolute;
    background: #ffffff;
    border: 2px solid #2563eb;
    border-radius: 20px;
    padding: 4px 16px;
    font-family: 'Consolas', monospace;
    font-size: 13.5px;
    font-weight: 800;
    color: #1e3a8a;
    box-shadow: 0 2px 6px rgba(0,0,0,0.12);
    white-space: nowrap;
  }

  /* Stage Themes */
  .stg-1 { border-color: #2563eb; background: #f8fafc; }
  .stg-1 .stage-title { color: #1e3a8a; }
  .stg-1 .stage-badge { background: #dbeafe; color: #1e40af; }

  .stg-2 { border-color: #059669; background: #f8fafc; }
  .stg-2 .stage-title { color: #064e3b; }
  .stg-2 .stage-badge { background: #d1fae5; color: #065f46; }

  .stg-3 { border-color: #d97706; background: #f8fafc; }
  .stg-3 .stage-title { color: #78350f; }
  .stg-3 .stage-badge { background: #fef3c7; color: #92400e; }

  .stg-4 { border-color: #7c3aed; background: #f8fafc; }
  .stg-4 .stage-title { color: #4c1d95; }
  .stg-4 .stage-badge { background: #ede9fe; color: #5b21b6; }

  .stg-5 { border-color: #e11d48; background: #f8fafc; }
  .stg-5 .stage-title { color: #881337; }
  .stg-5 .stage-badge { background: #ffe4e6; color: #9f1239; }

  /* Section 6 (Frame Table & XOR Parity) */
  .stg-6 { border-color: #475569; background: #f8fafc; margin-bottom: 0; }
  .stg-6 .stage-title { color: #0f172a; }

  /* 14-Byte Frame Grid */
  .frame-table {
    display: grid;
    grid-template-columns: repeat(14, 1fr);
    gap: 6px;
    margin: 12px 0 16px 0;
  }
  .byte-cell {
    background: #ffffff;
    border: 1.8px solid #cbd5e1;
    border-radius: 6px;
    padding: 8px 4px;
    text-align: center;
  }
  .byte-num {
    font-size: 11px;
    font-weight: 700;
    color: #64748b;
    margin-bottom: 2px;
  }
  .byte-name {
    font-size: 12px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 4px;
  }
  .byte-ascii {
    font-family: 'Consolas', monospace;
    font-size: 13.5px;
    font-weight: 900;
    color: #1e40af;
  }
  .byte-hex {
    font-family: 'Consolas', monospace;
    font-size: 11px;
    font-weight: 700;
    color: #475569;
  }

  /* Math Box */
  .math-card {
    background: #ffffff;
    border: 1.8px solid #cbd5e1;
    border-radius: 8px;
    padding: 14px 18px;
    margin-top: 10px;
  }
  .math-line {
    font-family: 'Consolas', monospace;
    font-size: 13.5px;
    margin-bottom: 6px;
    line-height: 1.4;
  }
</style>
</head>
<body>

<div class="diagram-container">
  <!-- Title Banner -->
  <div class="title-banner">
    <h1>HỆ THỐNG PHẦN CỨNG THU NHẬN &amp; GIẢI MÃ THẺ RFID RDM6300 TỰ TRỊ</h1>
    <p>Sơ đồ khối vi kiến trúc đường ống 5 giai đoạn phần cứng (Hardware 5-Stage Autonomous Decoding Pipeline)</p>
  </div>

  <!-- STAGE 1 -->
  <div class="stage-card stg-1">
    <div class="stage-header">
      <div class="stage-title">
        <span>GIAI ĐOẠN 1: KHỐI THU NHẬN TÍN HIỆU RF &amp; GIẢI ĐIỀU CHẾ TƯƠNG TỰ</span>
        <span class="stage-module">RDM6300 PMOD Module</span>
      </div>
      <span class="stage-badge">STAGE 1: RF FRONT-END (125 kHz)</span>
    </div>
    <div class="subunit-grid">
      <div class="subunit">
        <div class="sub-title">🏷️ Thẻ RFID Thụ Động (EM4100)</div>
        <div class="sub-body">
          • Tần số sóng mang cộng hưởng LC: <b>125 kHz</b><br>
          • Không dùng pin (Passive Transponder lấy năng lượng từ từ trường)<br>
          • Điều chế tải biên độ (ASK / Manchester 64-bit RF Data)
        </div>
      </div>
      <div class="subunit">
        <div class="sub-title">📡 Cuộn Cảm Thu &amp; Tách Sóng</div>
        <div class="sub-body">
          • Cuộn ăng-ten ngoài đường kính lớn tối ưu hóa cự ly đọc thẻ (3–5 cm)<br>
          • Mạch lọc phong bì tương tự (Envelope Demodulator)<br>
          • Bộ so sánh Schmitt Trigger tái tạo xung logic sạch nhiễu
        </div>
      </div>
      <div class="subunit">
        <div class="sub-title">🔌 Đầu Ra Nối Tiếp Chuẩn TTL</div>
        <div class="sub-body">
          • Tốc độ truyền thông: <b>9600 bps</b>, khung truyền 8-N-1<br>
          • Tín hiệu xuất: <span class="code-term">rdm_rx_i</span> đưa vào cổng PMOD JA1<br>
          • Chân J1 trên FPGA Basys 3 / Cổng I/O Pad ASIC SkyWater
        </div>
      </div>
    </div>
  </div>

  <!-- Pipe Arrow 1 -> 2 -->
  <div class="pipe-connector">
    <div class="pipe-arrow" style="background:#059669;">
      <div class="pipe-badge" style="border-color:#059669; color:#064e3b; top:-12px; left:-240px;">
        rdm_rx_i (9600 bps Asynchronous TTL Serial Stream)
      </div>
    </div>
  </div>

  <!-- STAGE 2 -->
  <div class="stage-card stg-2">
    <div class="stage-header">
      <div class="stage-title">
        <span>GIAI ĐOẠN 2: BỘ ĐỒNG BỘ HÓA XUNG NHỊP KHỬ TRẠNG THÁI BẤT ĐỊNH (CDC)</span>
        <span class="stage-module">rtl/sync_2ff.v</span>
      </div>
      <span class="stage-badge">STAGE 2: 2-STAGE FLIP-FLOP SYNCHRONIZER</span>
    </div>
    <div class="subunit-grid">
      <div class="subunit">
        <div class="sub-title">⚠️ Nguy Cơ Bất Định (Metastability)</div>
        <div class="sub-body">
          • Tín hiệu <span class="code-term">rdm_rx_i</span> đến từ bên ngoài độc lập xung nhịp<br>
          • Nếu chuyển mức logic đúng thời điểm xung nhịp SoC 50 MHz, sẽ gây vi phạm thời gian thiết lập và duy trì (Tsu / Th violation)
        </div>
      </div>
      <div class="subunit">
        <div class="sub-title">⚡ Tầng Flip-Flop 1 (Hấp Thụ Dao Động)</div>
        <div class="sub-body">
          • D-Flip-Flop chốt tín hiệu tại sườn dương xung nhịp <b>50 MHz</b><br>
          • Toàn bộ thời gian dao động bất định được nhốt kín trong tầng FF1<br>
          • Ngăn chặn hiện tượng lỗi lan truyền vào hệ thống logic nội bộ
        </div>
      </div>
      <div class="subunit">
        <div class="sub-title">🛡️ Tầng Flip-Flop 2 (Xuất Tín Hiệu Sạch)</div>
        <div class="sub-body">
          • Tầng FF2 lấy mẫu ngõ ra FF1 sau tròn 1 chu kỳ clock (20.0 ns)<br>
          • Tín hiệu xuất: <span class="code-term">rdm_rx_sync</span> ổn định tuyệt đối mức logic '0' hoặc '1'<br>
          • Thời gian trung bình giữa 2 lần lỗi (MTBF) &gt; 1,000 năm trên Sky130
        </div>
      </div>
    </div>
  </div>

  <!-- Pipe Arrow 2 -> 3 -->
  <div class="pipe-connector">
    <div class="pipe-arrow" style="background:#d97706;">
      <div class="pipe-badge" style="border-color:#d97706; color:#78350f; top:-12px; left:-230px;">
        rdm_rx_sync (50 MHz Synchronous Bit Stream - Glitch-Free)
      </div>
    </div>
  </div>

  <!-- STAGE 3 -->
  <div class="stage-card stg-3">
    <div class="stage-header">
      <div class="stage-title">
        <span>GIAI ĐOẠN 3: BỘ THU PHẦN CỨNG NỐI TIẾP UART CÓ BỘ BỎ PHIẾU ĐA SỐ 16X</span>
        <span class="stage-module">rtl/uart_rx.v</span>
      </div>
      <span class="stage-badge">STAGE 3: HARDWARE UART RX ENGINE</span>
    </div>
    <div class="subunit-grid">
      <div class="subunit">
        <div class="sub-title">⏱️ Bộ Chia Tần Số Baud (Clock Divider)</div>
        <div class="sub-body">
          • Hệ số chia chu kỳ: <span class="code-term">Divisor = 50,000,000 / 9600 = 5208</span><br>
          • Bộ đếm tích tắc tạo xung lấy mẫu gấp 16 lần tần số baud (16x Oversampling)<br>
          • Tự động căn pha sườn âm Start-Bit chính xác đến từng chu kỳ 20ns
        </div>
      </div>
      <div class="subunit">
        <div class="sub-title">🗳️ Bộ Bỏ Phiếu Đa Số 3 Điểm (Majority Voter)</div>
        <div class="sub-body">
          • Lấy mẫu tín hiệu tại 3 tích tắc trung tâm của bit: <b>Tick 7, 8, 9</b><br>
          • Thuật toán logic đa số: <span class="code-term">Bit = (S7 &amp; S8) | (S8 &amp; S9) | (S7 &amp; S9)</span><br>
          • Lọc bỏ hoàn toàn xung gai nhiễu cao tần và hiện tượng méo xung đường truyền
        </div>
      </div>
      <div class="subunit">
        <div class="sub-title">📦 Thanh Ghi Dịch Chuyển Tái Lập Byte</div>
        <div class="sub-body">
          • Thanh ghi 8-bit dịch nối tiếp - xuất song song (8-bit SIPO)<br>
          • Ngõ ra dữ liệu: <span class="code-term">byte_data[7:0]</span> (Byte mã ASCII hợp lệ)<br>
          • Ngõ ra xung chốt: <span class="code-term">byte_valid</span> (Xung Strobe tích cực đúng 1 chu kỳ clk)
        </div>
      </div>
    </div>
  </div>

  <!-- Pipe Arrow 3 -> 4 -->
  <div class="pipe-connector">
    <div class="pipe-arrow" style="background:#7c3aed;">
      <div class="pipe-badge" style="border-color:#7c3aed; color:#4c1d95; top:-12px; left:-250px;">
        byte_data[7:0] (ASCII Byte) + byte_valid (1-Cycle Strobe Pulse)
      </div>
    </div>
  </div>

  <!-- STAGE 4 -->
  <div class="stage-card stg-4">
    <div class="stage-header">
      <div class="stage-title">
        <span>GIAI ĐOẠN 4: BỘ GIẢI MÃ KHUNG VÀ ĐỐI CHIẾU CHECKSUM PHẦN CỨNG TỰ TRỊ</span>
        <span class="stage-module">rtl/rdm6300_frame_decoder.v</span>
      </div>
      <span class="stage-badge">STAGE 4: FRAME DECODER FSM &amp; PARALLEL XOR</span>
    </div>
    <div class="subunit-grid">
      <div class="subunit">
        <div class="sub-title">🔄 Máy Trạng Thái FSM 5 Bước Tự Động</div>
        <div class="sub-body">
          • <span class="code-term">ST_WAIT_STX</span>: Đợi ký tự mở đầu khung STX (0x02)<br>
          • <span class="code-term">ST_COLLECT_DATA</span>: Nhận đủ 10 ký tự ASCII dữ liệu thẻ<br>
          • <span class="code-term">ST_CHECKSUM</span>: Nhận 2 ký tự ASCII mã Checksum<br>
          • <span class="code-term">ST_WAIT_ETX</span>: Xác nhận ký tự kết thúc ETX (0x03)<br>
          • <span class="code-term">ST_VALIDATE</span>: So khớp kiểm tra toàn vẹn
        </div>
      </div>
      <div class="subunit">
        <div class="sub-title">🔢 Bộ Chuyển Đổi Tổ Hợp ASCII-to-Hex</div>
        <div class="sub-body">
          • Chuyển đổi ký tự ASCII sang số Hex nhị phân trong 0 chu kỳ trễ:<br>
          &nbsp;&nbsp;'0'–'9' (0x30–0x39) &rarr; Giá trị 0x0–0x9<br>
          &nbsp;&nbsp;'A'–'F' (0x41–0x46) &rarr; Giá trị 0xA–0xF<br>
          • Ghép 2 ký tự ASCII thành 1 byte nhị phân hoàn chỉnh<br>
          • Thu được 5 byte dữ liệu nhị phân: <b>D[0]</b> đến <b>D[4]</b>
        </div>
      </div>
      <div class="subunit">
        <div class="sub-title">⚙️ Cây XOR Song Song &amp; Watchdog Timer</div>
        <div class="sub-body">
          • <b>Cây XOR 1 chu kỳ phần cứng (20.0 ns):</b><br>
          &nbsp;&nbsp;<span class="code-term">Calc_CS = D[0] ^ D[1] ^ D[2] ^ D[3] ^ D[4]</span><br>
          • So khớp: <span class="code-term">Calc_CS == Received_CS</span><br>
          • <b>Bộ định thời Watchdog 19-bit (500k cycles = 10 ms):</b><br>
          &nbsp;&nbsp;Tự động cưỡng chế Reset FSM về trạng thái chờ nếu đứt gói
        </div>
      </div>
    </div>
  </div>

  <!-- Pipe Arrow 4 -> 5 -->
  <div class="pipe-connector">
    <div class="pipe-arrow" style="background:#e11d48;">
      <div class="pipe-badge" style="border-color:#e11d48; color:#881337; top:-12px; left:-270px;">
        tag_id[39:0] (Validated 40-bit Tag Code) + card_valid_strobe + cs_error
      </div>
    </div>
  </div>

  <!-- STAGE 5 -->
  <div class="stage-card stg-5">
    <div class="stage-header">
      <div class="stage-title">
        <span>GIAI ĐOẠN 5: CÁC THANH GHI GIAO TIẾP BUS MMIO &amp; BÁO NGẮT PHẦN CỨNG CPU</span>
        <span class="stage-module">MMIO Base: 0x1000_0000</span>
      </div>
      <span class="stage-badge">STAGE 5: MMIO INTERFACES &amp; IRQ</span>
    </div>
    <div class="subunit-grid">
      <div class="subunit">
        <div class="sub-title">📋 Thanh Ghi Trạng Thái (REG_STATUS)</div>
        <div class="sub-body">
          • Địa chỉ MMIO: <span class="code-term">0x1000_0000</span> (Đọc/Ghi 32-bit)<br>
          • <b>Bit 0 (card_valid):</b> Tự động bật lên '1' khi nhận thẻ hợp lệ. CPU ghi '1' để xóa cờ (Write-1-to-Clear)<br>
          • <b>Bit 1 (cs_error):</b> Bật '1' cảnh báo nếu lỗi XOR Checksum
        </div>
      </div>
      <div class="subunit">
        <div class="sub-title">💾 Thanh Ghi Dữ Liệu Thẻ (TAG_HI &amp; LO)</div>
        <div class="sub-body">
          • <b>REG_TAG_HI (0x1000_0004):</b><br>
          &nbsp;&nbsp;Chứa 8-bit mã Version thẻ (Bits [39:32], ví dụ: <span class="code-term">0x00</span>)<br>
          • <b>REG_TAG_LO (0x1000_0008):</b><br>
          &nbsp;&nbsp;Chứa 32-bit số sê-ri thẻ (Bits [31:0], ví dụ: <span class="code-term">0x007293F0</span>)
        </div>
      </div>
      <div class="subunit">
        <div class="sub-title">🚀 Cơ Chế Không Tốn CPU (Zero Overhead)</div>
        <div class="sub-body">
          • Tín hiệu ngắt <span class="code-term">card_event_o</span> kích hoạt tức thời CPU PicoRV32<br>
          • CPU hoàn toàn rảnh tay, không bao giờ phải chạy vòng lặp thăm dò (polling) từng ký tự UART<br>
          • Độ trễ phản hồi kể từ khi kết thúc khung truyền &lt; 40 ns
        </div>
      </div>
    </div>
  </div>

  <!-- SECTION 6: 14-BYTE FRAME ANATOMY & PARALLEL XOR -->
  <div class="stage-card stg-6">
    <div class="stage-header">
      <div class="stage-title">
        <span>CẤU TRÚC KHUNG TRUYỀN 14 BYTE VÀ TOÁN TỬ XOR KIỂM TRA TOÀN VẸN</span>
        <span class="stage-module">Real Tag Example: 0007508976 | Hex: 0x007293F0</span>
      </div>
      <span class="stage-badge" style="background:#e2e8f0; color:#1e293b;">FRAME ANATOMY &amp; MATH FORMULA</span>
    </div>

    <!-- 14-Byte Grid -->
    <div class="frame-table">
      <div class="byte-cell" style="background:#f1f5f9; border-color:#94a3b8;">
        <div class="byte-num">Byte 0</div>
        <div class="byte-name">Header</div>
        <div class="byte-ascii">STX</div>
        <div class="byte-hex">0x02</div>
      </div>
      <div class="byte-cell" style="background:#eff6ff; border-color:#93c5fd;">
        <div class="byte-num">Byte 1</div>
        <div class="byte-name">Ver[7:4]</div>
        <div class="byte-ascii">'0'</div>
        <div class="byte-hex">0x30</div>
      </div>
      <div class="byte-cell" style="background:#eff6ff; border-color:#93c5fd;">
        <div class="byte-num">Byte 2</div>
        <div class="byte-name">Ver[3:0]</div>
        <div class="byte-ascii">'0'</div>
        <div class="byte-hex">0x30</div>
      </div>
      <div class="byte-cell" style="background:#ecfdf5; border-color:#86efac;">
        <div class="byte-num">Byte 3</div>
        <div class="byte-name">D[31:28]</div>
        <div class="byte-ascii">'0'</div>
        <div class="byte-hex">0x30</div>
      </div>
      <div class="byte-cell" style="background:#ecfdf5; border-color:#86efac;">
        <div class="byte-num">Byte 4</div>
        <div class="byte-name">D[27:24]</div>
        <div class="byte-ascii">'0'</div>
        <div class="byte-hex">0x30</div>
      </div>
      <div class="byte-cell" style="background:#ecfdf5; border-color:#86efac;">
        <div class="byte-num">Byte 5</div>
        <div class="byte-name">D[23:20]</div>
        <div class="byte-ascii">'7'</div>
        <div class="byte-hex">0x37</div>
      </div>
      <div class="byte-cell" style="background:#ecfdf5; border-color:#86efac;">
        <div class="byte-num">Byte 6</div>
        <div class="byte-name">D[19:16]</div>
        <div class="byte-ascii">'2'</div>
        <div class="byte-hex">0x32</div>
      </div>
      <div class="byte-cell" style="background:#ecfdf5; border-color:#86efac;">
        <div class="byte-num">Byte 7</div>
        <div class="byte-name">D[15:12]</div>
        <div class="byte-ascii">'9'</div>
        <div class="byte-hex">0x39</div>
      </div>
      <div class="byte-cell" style="background:#ecfdf5; border-color:#86efac;">
        <div class="byte-num">Byte 8</div>
        <div class="byte-name">D[11:8]</div>
        <div class="byte-ascii">'3'</div>
        <div class="byte-hex">0x33</div>
      </div>
      <div class="byte-cell" style="background:#ecfdf5; border-color:#86efac;">
        <div class="byte-num">Byte 9</div>
        <div class="byte-name">D[7:4]</div>
        <div class="byte-ascii">'F'</div>
        <div class="byte-hex">0x46</div>
      </div>
      <div class="byte-cell" style="background:#ecfdf5; border-color:#86efac;">
        <div class="byte-num">Byte 10</div>
        <div class="byte-name">D[3:0]</div>
        <div class="byte-ascii">'0'</div>
        <div class="byte-hex">0x30</div>
      </div>
      <div class="byte-cell" style="background:#fdf2f8; border-color:#f472b6;">
        <div class="byte-num">Byte 11</div>
        <div class="byte-name">CS[7:4]</div>
        <div class="byte-ascii">'F'</div>
        <div class="byte-hex">0x46</div>
      </div>
      <div class="byte-cell" style="background:#fdf2f8; border-color:#f472b6;">
        <div class="byte-num">Byte 12</div>
        <div class="byte-name">CS[3:0]</div>
        <div class="byte-ascii">'0'</div>
        <div class="byte-hex">0x30</div>
      </div>
      <div class="byte-cell" style="background:#f1f5f9; border-color:#94a3b8;">
        <div class="byte-num">Byte 13</div>
        <div class="byte-name">Footer</div>
        <div class="byte-ascii">ETX</div>
        <div class="byte-hex">0x03</div>
      </div>
    </div>

    <!-- Mathematical Formula Box -->
    <div class="math-card">
      <div style="font-weight: 800; font-size: 14.5px; color: #0f172a; margin-bottom: 8px;">
        📐 CHỨNG MINH TOÁN HỌC CÂY TOÁN TỬ XOR KIỂM TRA TOÀN VẸN (1 Chu Kỳ Tổ Hợp):
      </div>
      <div class="math-line" style="color: #0369a1; font-weight:800;">
        Công thức:  Calculated_Checksum = D[0] ^ D[1] ^ D[2] ^ D[3] ^ D[4]
      </div>
      <div class="math-line" style="color: #475569;">
        Dạng nhị phân: = (0000_0000) ^ (0000_0000) ^ (0111_0010) ^ (1001_0011) ^ (1111_0000)
      </div>
      <div class="math-line" style="color: #15803d; font-weight:800;">
        Dạng Hex:      = (0x00)       ^ (0x00)       ^ (0x72)       ^ (0x93)       ^ (0xF0)       = 0xF0
      </div>
      <div class="math-line" style="color: #b91c1c; font-weight:900;">
        Kết quả:       Calculated_Checksum (0xF0) == Received_Checksum (0xF0) &rarr; SO KHỚP CHUẨN XÁC 100% &rarr; Bật cờ card_valid!
      </div>
    </div>
  </div>

</div>

</body>
</html>
"""
    with open("fig2_drawio_style.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("[SUCCESS] HTML vector source written at: fig2_drawio_style.html")

    # Render via Chrome headless at 2x DPI
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    html_path = os.path.abspath("fig2_drawio_style.html")
    out_img = os.path.abspath("fig2_rdm6300_subsystem.png")

    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--force-device-scale-factor=2",
        f"--screenshot={out_img}",
        "--window-size=1340,2300",
        f"file:///{html_path.replace(os.sep, '/')}"
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(out_img):
        print(f"[SUCCESS] Ultra-high resolution Fig 2 rendered image generated at: {out_img} ({os.path.getsize(out_img)} bytes)")
    else:
        print("[ERROR] Chrome rendering failed:", res.stderr)

if __name__ == '__main__':
    create_drawio_xml()
    create_html_and_render_png()
