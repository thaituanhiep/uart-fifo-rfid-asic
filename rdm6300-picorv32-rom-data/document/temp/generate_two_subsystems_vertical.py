# -*- coding: utf-8 -*-
"""
Script: generate_two_subsystems_vertical.py
Generates TWO GENUINE BLACK & WHITE VERTICAL DRAW.IO DIAGRAMS with HUGE, PROMINENT TEXT:
1. fig2a_rdm6300_subsystem (Vertical layout, 1400 x 2000 px):
   - Sơ đồ khối 5 giai đoạn phần cứng thu nhận & giải mã thẻ RFID RDM6300 (0x1000_0000)
2. fig2b_host_uart_subsystem (Vertical layout, 1400 x 2000 px):
   - Sơ đồ khối phần cứng giao tiếp máy tính Host PC UART tích hợp 32-Byte FIFO (0x3000_0000)

Output formats:
- Genuine Draw.io XML (.drawio)
- Clean Vector SVG (.svg)
- Ultra-Sharp 2x Retina PNG (.png) via Headless Chrome (2800 x 4000 px)
- Synchronized to project root, document/, document/temp/ and IDE Artifacts
"""

import os
import subprocess
import shutil

PROJECT_DIR = r"d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data"
DOC_DIR     = os.path.join(PROJECT_DIR, "document")
TEMP_DIR    = os.path.join(DOC_DIR, "temp")
ARTIFACT_DIR = r"C:\Users\thait\.gemini\antigravity-ide\brain\40d01579-3c16-4b85-9b12-c0e7d33bcd21"

WIDTH  = 1400
HEIGHT = 2000

def run_chrome_headless(html_path, png_out, w=WIDTH, h=HEIGHT):
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if not os.path.exists(chrome_path):
        chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

    cmd = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        "--force-device-scale-factor=2",
        f"--window-size={w},{h}",
        f"--screenshot={png_out}",
        html_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"[OK] Rendered PNG: {png_out}")
    else:
        print(f"[ERROR] Chrome render failed: {res.stderr}")

# ============================================================================
# DIAGRAM 2A: RDM6300 RFID HARDWARE SUBSYSTEM (VERTICAL - BLACK & WHITE)
# ============================================================================
def create_fig2a_vertical():
    drawio_path = os.path.join(TEMP_DIR, "fig2a_rdm6300_subsystem.drawio")
    svg_path    = os.path.join(TEMP_DIR, "fig2a_rdm6300_subsystem.svg")
    png_path    = os.path.join(TEMP_DIR, "fig2a_rdm6300_subsystem.png")
    html_path   = os.path.join(TEMP_DIR, "render_fig2a.html")

    # 1. Draw.io XML
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="2026-10-02T06:15:00.000Z" agent="Mozilla/5.0" version="21.0.0" type="device">
  <diagram id="rdm6300_vertical_bnw" name="RDM6300 RFID Pipeline Vertical">
    <mxGraphModel dx="1600" dy="2200" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{WIDTH}" pageHeight="{HEIGHT}" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- Title Banner -->
        <mxCell id="title" value="&lt;b style=&quot;font-size:26px;&quot;&gt;HÌNH 2A: SƠ ĐỒ KHỐI ĐƯỜNG ỐNG 5 GIAI ĐOẠN THU NHẬN &amp;amp; GIẢI MÃ THẺ RFID RDM6300&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:18px;&quot;&gt;Kiến trúc module rdm6300_mmio.v (Slave 2: 0x1000_0000): Khử bất ổn 2-FF ➔ UART RX 9600 Majority ➔ FSM &amp;amp; Cây XOR 20ns ➔ MMIO Registers&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2.5;fontFamily=Arial,Helvetica,sans-serif;align=center;" vertex="1" parent="1">
          <mxGeometry x="60" y="30" width="1280" height="90" as="geometry" />
        </mxCell>

        <!-- STAGE 1: RF FRONT-END -->
        <mxCell id="stg1" value="&lt;b style=&quot;font-size:23px;&quot;&gt;GIAI ĐOẠN 1: KHỐI THU RF &amp;amp; TÁCH SÓNG TƯƠNG TỰ (ĐẦU ĐỌC RDM6300 125 kHz)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:18px;font-weight:bold;&quot;&gt;Module RDM6300 ngoại vi kết nối qua cổng PMOD JA1 bo mạch FPGA Basys 3&lt;/span&gt;&lt;hr style=&quot;border:0;border-top:2px solid #000000;margin:10px 0;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:18px;line-height:1.6;&quot;&gt;• &lt;b&gt;Thẻ RFID thụ động (EM4100):&lt;/b&gt; Tần số sóng mang 125 kHz, điều chế biên độ ASK / Manchester 64-bit.&lt;br&gt;• &lt;b&gt;Ăng-ten cuộn cảm &amp;amp; Mạch tách sóng tương tự:&lt;/b&gt; Mạch cộng hưởng LC, tách sóng đường bao (Envelope Detector) và Schmitt Trigger tạo xung vuông logic.&lt;br&gt;• &lt;b&gt;Ngõ ra UART TTL nối tiếp:&lt;/b&gt; Tốc độ chuẩn 9600 bps (8-N-1, không bit chẵn lẻ), phát chuỗi xung nhịp bất đồng bộ tới chân &lt;b&gt;rdm6300_rx_i&lt;/b&gt;.&lt;/div&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2.2;fontFamily=Arial,Helvetica,sans-serif;align=center;verticalAlign=top;spacingTop=12;spacingLeft=16;spacingRight=16;" vertex="1" parent="1">
          <mxGeometry x="60" y="150" width="1280" height="280" as="geometry" />
        </mxCell>

        <!-- Arrow 1 -> 2 -->
        <mxCell id="arr1_2" value="rdm6300_rx_i (Chuỗi bit 9600 bps TTL bất đồng bộ)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#000000;fontSize=18;fontStyle=1;endArrow=block;endFill=1;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="stg1" target="stg2">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- STAGE 2: 2-FF CDC -->
        <mxCell id="stg2" value="&lt;b style=&quot;font-size:23px;&quot;&gt;GIAI ĐOẠN 2: BỘ ĐỒNG BỘ CDC 2 TẦNG D-FLIP-FLOP (sync_2ff.v)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:18px;font-weight:bold;&quot;&gt;Chuyển đổi an toàn tín hiệu bất đồng bộ bên ngoài sang miền xung nhịp hệ thống 50 MHz&lt;/span&gt;&lt;hr style=&quot;border:0;border-top:2px solid #000000;margin:10px 0;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:18px;line-height:1.6;&quot;&gt;• &lt;b&gt;Khử hiện tượng siêu bền bất ổn định (Metastability):&lt;/b&gt; Cách ly miền xung của module RDM6300 với miền xung chủ 50 MHz (T_clk = 20.0 ns).&lt;br&gt;• &lt;b&gt;Hai tầng D-FF mắc nối tiếp:&lt;/b&gt; Tầng FF 1 hấp thụ các xung vi phạm thời gian thiết lập và giữ (T_su / T_h); Tầng FF 2 chốt mức logic CMOS 0/1 sạch.&lt;br&gt;• &lt;b&gt;Độ tin cậy bán dẫn cực cao:&lt;/b&gt; Thời gian trung bình giữa 2 lỗi (MTBF) &amp;gt; 1,000 năm trên công nghệ bán dẫn SkyWater 130nm.&lt;br&gt;• &lt;b&gt;Tín hiệu ngõ ra:&lt;/b&gt; &lt;b&gt;rdm_rx_sync&lt;/b&gt; đồng bộ hoàn toàn với nhịp clock 50 MHz của vi mạch SoC.&lt;/div&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2.2;fontFamily=Arial,Helvetica,sans-serif;align=center;verticalAlign=top;spacingTop=12;spacingLeft=16;spacingRight=16;" vertex="1" parent="1">
          <mxGeometry x="60" y="500" width="1280" height="280" as="geometry" />
        </mxCell>

        <!-- Arrow 2 -> 3 -->
        <mxCell id="arr2_3" value="rdm_rx_sync (Tín hiệu đã đồng bộ miền Clock SoC 50 MHz)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#000000;fontSize=18;fontStyle=1;endArrow=block;endFill=1;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="stg2" target="stg3">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- STAGE 3: UART RX -->
        <mxCell id="stg3" value="&lt;b style=&quot;font-size:23px;&quot;&gt;GIAI ĐOẠN 3: BỘ THU UART RX LẤY MẪU ĐA SỐ 16X (uart_rx.v)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:18px;font-weight:bold;&quot;&gt;Khôi phục dòng byte ASCII từ chuỗi xung bit nối tiếp với thuật toán lọc nhiễu 3 điểm&lt;/span&gt;&lt;hr style=&quot;border:0;border-top:2px solid #000000;margin:10px 0;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:18px;line-height:1.6;&quot;&gt;• &lt;b&gt;Bộ chia tần số Baudrate phần cứng:&lt;/b&gt; Divisor = 50,000,000 / 9600 = 5208 chu kỳ clock/bit (chu kỳ lấy mẫu 16x oversampling).&lt;br&gt;• &lt;b&gt;Bộ bỏ phiếu đa số 3 mẫu liên tiếp:&lt;/b&gt; Lấy mẫu tại các Ticks 7, 8, 9 ở chính giữa bit (Mid-bit), triệt tiêu hoàn toàn xung gai nhiễu điện từ.&lt;br&gt;• &lt;b&gt;Thanh ghi dịch SIPO 8-bit:&lt;/b&gt; Dịch chuyển bit nối tiếp sang song song, tái lập nguyên vẹn từng ký tự ASCII &lt;b&gt;hw_rx_byte[7:0]&lt;/b&gt;.&lt;br&gt;• &lt;b&gt;Xung strobe hoàn tất byte:&lt;/b&gt; Kích hoạt &lt;b&gt;hw_rx_dv&lt;/b&gt; đúng 1 chu kỳ clock (20ns) báo cho máy trạng thái FSM thu nhận.&lt;/div&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2.2;fontFamily=Arial,Helvetica,sans-serif;align=center;verticalAlign=top;spacingTop=12;spacingLeft=16;spacingRight=16;" vertex="1" parent="1">
          <mxGeometry x="60" y="850" width="1280" height="290" as="geometry" />
        </mxCell>

        <!-- Arrow 3 -> 4 -->
        <mxCell id="arr3_4" value="hw_rx_byte[7:0] (Byte ASCII) + hw_rx_dv (Xung Strobe 1 chu kỳ 20ns)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#000000;fontSize=18;fontStyle=1;endArrow=block;endFill=1;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="stg3" target="stg4">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- STAGE 4: FRAME DECODER & XOR TREE -->
        <mxCell id="stg4" value="&lt;b style=&quot;font-size:23px;&quot;&gt;GIAI ĐOẠN 4: FSM GIẢI MÃ KHUNG 14 BYTE &amp;amp; CÂY XOR SONG SONG 20ns (rdm6300_frame_decoder.v)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:18px;font-weight:bold;&quot;&gt;Máy trạng thái tự động bóc tách khung dữ liệu thẻ và kiểm tra Checksum trong đúng 1 chu kỳ clock&lt;/span&gt;&lt;hr style=&quot;border:0;border-top:2px solid #000000;margin:10px 0;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:18px;line-height:1.6;&quot;&gt;• &lt;b&gt;FSM bóc tách khung 14 byte:&lt;/b&gt; ST_WAIT_STX (0x02) ➔ ST_DATA (10 byte ASCII) ➔ ST_CHECKSUM (2 byte ASCII) ➔ ST_WAIT_ETX (0x03).&lt;br&gt;• &lt;b&gt;Bộ chuyển đổi tổ hợp ASCII ➔ Hex:&lt;/b&gt; Tự động quy đổi 10 ký tự ASCII thành 5 byte Hex nhị phân (D[0]..D[4]) ngay lập tức (0 chu kỳ trễ).&lt;br&gt;• &lt;b&gt;Cây toán tử XOR song song 1 chu kỳ (20ns):&lt;/b&gt; Calc_CS = D[0] ^ D[1] ^ D[2] ^ D[3] ^ D[4]; So khớp Calc_CS == Received_CS.&lt;br&gt;• &lt;b&gt;Watchdog Timer chống treo phần cứng:&lt;/b&gt; Bộ đếm 19-bit (500,000 clock = 10ms) tự động reset FSM về ST_WAIT_STX nếu đứt gói.&lt;/div&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2.2;fontFamily=Arial,Helvetica,sans-serif;align=center;verticalAlign=top;spacingTop=12;spacingLeft=16;spacingRight=16;" vertex="1" parent="1">
          <mxGeometry x="60" y="1210" width="1280" height="320" as="geometry" />
        </mxCell>

        <!-- Arrow 4 -> 5 -->
        <mxCell id="arr4_5" value="tag_id[39:0] (40-bit UID) + card_valid (Strobe) + cs_error (Cờ báo lỗi)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#000000;fontSize=18;fontStyle=1;endArrow=block;endFill=1;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="stg4" target="stg5">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- STAGE 5: MMIO REGISTERS -->
        <mxCell id="stg5" value="&lt;b style=&quot;font-size:23px;&quot;&gt;GIAI ĐOẠN 5: THANH GHI NGOẠI VI MMIO &amp;amp; GIAO DIỆN BUS (rdm6300_mmio.v - 0x1000_0000)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:18px;font-weight:bold;&quot;&gt;Lưu trữ kết quả giải mã vào thanh ghi bộ nhớ ánh xạ và phát tín hiệu ngắt đánh thức CPU&lt;/span&gt;&lt;hr style=&quot;border:0;border-top:2px solid #000000;margin:10px 0;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:18px;line-height:1.6;&quot;&gt;• &lt;b&gt;REG_RFID_STATUS (0x1000_0000):&lt;/b&gt; Bit 0 = cờ card_valid (Ghi 1 để xóa cờ sau khi đọc); Bit 1 = cờ checksum_error.&lt;br&gt;• &lt;b&gt;REG_RFID_TAG_HI (0x1000_0004):&lt;/b&gt; Bits [39:32] = Byte Version của thẻ (ví dụ thẻ thật: 0x00).&lt;br&gt;• &lt;b&gt;REG_RFID_TAG_LO (0x1000_0008):&lt;/b&gt; Bits [31:0] = 32-bit số Serial thẻ chuẩn hóa (ví dụ thẻ thật: 0x007293F0).&lt;br&gt;• &lt;b&gt;Tín hiệu ngắt card_event_o:&lt;/b&gt; Tự động kích hoạt ngắt đánh thức CPU PicoRV32 tra cứu danh mục thẻ trên SPI Flash tức thì (&amp;lt; 10 µs).&lt;/div&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2.2;fontFamily=Arial,Helvetica,sans-serif;align=center;verticalAlign=top;spacingTop=12;spacingLeft=16;spacingRight=16;" vertex="1" parent="1">
          <mxGeometry x="60" y="1600" width="1280" height="320" as="geometry" />
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
    with open(drawio_path, "w", encoding="utf-8") as f:
        f.write(xml)
    shutil.copy2(drawio_path, os.path.join(DOC_DIR, "fig2a_rdm6300_subsystem.drawio"))
    shutil.copy2(drawio_path, os.path.join(PROJECT_DIR, "fig2a_rdm6300_subsystem.drawio"))
    print(f"[OK] Generated Fig 2a Draw.io: {drawio_path}")

    # 2. Vector SVG
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}">
  <defs>
    <style>
      .border-box {{ fill: #ffffff; stroke: #000000; stroke-width: 2.5; }}
      .card-box {{ fill: #ffffff; stroke: #000000; stroke-width: 2.2; }}
      .arr-line {{ stroke: #000000; stroke-width: 3.0; fill: none; }}
      .arrowhead {{ fill: #000000; }}
      .txt-title {{ font-family: Arial, Helvetica, sans-serif; font-size: 26px; font-weight: bold; text-anchor: middle; fill: #000000; }}
      .txt-sub {{ font-family: Arial, Helvetica, sans-serif; font-size: 18px; text-anchor: middle; fill: #222222; }}
      .txt-card-h1 {{ font-family: Arial, Helvetica, sans-serif; font-size: 23px; font-weight: bold; text-anchor: middle; fill: #000000; }}
      .txt-card-h2 {{ font-family: Arial, Helvetica, sans-serif; font-size: 18px; font-weight: bold; text-anchor: middle; fill: #333333; }}
      .txt-body {{ font-family: Arial, Helvetica, sans-serif; font-size: 18px; fill: #111111; }}
      .txt-lbl {{ font-family: Arial, Helvetica, sans-serif; font-size: 18px; font-weight: bold; text-anchor: middle; fill: #000000; }}
    </style>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" class="arrowhead" />
    </marker>
  </defs>

  <rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" fill="#ffffff" />

  <!-- Title Banner -->
  <rect x="60" y="30" width="1280" height="90" class="border-box" />
  <text x="700" y="66" class="txt-title">HÌNH 2A: SƠ ĐỒ KHỐI ĐƯỜNG ỐNG 5 GIAI ĐOẠN THU NHẬN &amp; GIẢI MÃ THẺ RFID RDM6300</text>
  <text x="700" y="98" class="txt-sub">Kiến trúc module rdm6300_mmio.v (Slave 2: 0x1000_0000): Khử bất ổn 2-FF ➔ UART RX 9600 Majority ➔ FSM &amp; Cây XOR 20ns ➔ MMIO Registers</text>

  <!-- STAGE 1 -->
  <rect x="60" y="150" width="1280" height="280" class="card-box" />
  <text x="700" y="188" class="txt-card-h1">GIAI ĐOẠN 1: KHỐI THU RF &amp; TÁCH SÓNG TƯƠNG TỰ (ĐẦU ĐỌC RDM6300 125 kHz)</text>
  <text x="700" y="215" class="txt-card-h2">Module RDM6300 ngoại vi kết nối qua cổng PMOD JA1 bo mạch FPGA Basys 3</text>
  <line x1="90" y1="230" x2="1310" y2="230" stroke="#000000" stroke-width="2.0" />
  <text x="90" y="265" class="txt-body"><tspan font-weight="bold">• Thẻ RFID thụ động (EM4100):</tspan> Tần số sóng mang 125 kHz, điều chế biên độ ASK / Manchester 64-bit.</text>
  <text x="90" y="305" class="txt-body"><tspan font-weight="bold">• Ăng-ten cuộn cảm &amp; Mạch tách sóng tương tự:</tspan> Mạch cộng hưởng LC, tách sóng đường bao (Envelope Detector) và Schmitt Trigger tạo xung vuông logic.</text>
  <text x="90" y="345" class="txt-body"><tspan font-weight="bold">• Ngõ ra UART TTL nối tiếp:</tspan> Tốc độ chuẩn 9600 bps (8-N-1, không bit chẵn lẻ), phát chuỗi xung nhịp bất đồng bộ tới chân <tspan font-weight="bold">rdm6300_rx_i</tspan>.</text>

  <!-- Arrow 1 -> 2 -->
  <line x1="700" y1="430" x2="700" y2="500" class="arr-line" marker-end="url(#arrow)" />
  <rect x="440" y="446" width="520" height="38" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
  <text x="700" y="471" class="txt-lbl">rdm6300_rx_i (Chuỗi bit 9600 bps TTL bất đồng bộ)</text>

  <!-- STAGE 2 -->
  <rect x="60" y="500" width="1280" height="280" class="card-box" />
  <text x="700" y="538" class="txt-card-h1">GIAI ĐOẠN 2: BỘ ĐỒNG BỘ CDC 2 TẦNG D-FLIP-FLOP (sync_2ff.v)</text>
  <text x="700" y="565" class="txt-card-h2">Chuyển đổi an toàn tín hiệu bất đồng bộ bên ngoài sang miền xung nhịp hệ thống 50 MHz</text>
  <line x1="90" y1="580" x2="1310" y2="580" stroke="#000000" stroke-width="2.0" />
  <text x="90" y="615" class="txt-body"><tspan font-weight="bold">• Khử hiện tượng siêu bền bất ổn định (Metastability):</tspan> Cách ly miền xung RDM6300 với miền xung chủ 50 MHz (T_clk = 20.0 ns).</text>
  <text x="90" y="655" class="txt-body"><tspan font-weight="bold">• Hai tầng D-FF mắc nối tiếp:</tspan> Tầng FF 1 hấp thụ các xung vi phạm thời gian Setup/Hold; Tầng FF 2 chốt mức logic CMOS 0/1 sạch.</text>
  <text x="90" y="695" class="txt-body"><tspan font-weight="bold">• Độ tin cậy bán dẫn cực cao:</tspan> MTBF &gt; 1,000 năm trên công nghệ bán dẫn SkyWater 130nm | Ngõ ra: <tspan font-weight="bold">rdm_rx_sync</tspan> (đồng bộ 50 MHz).</text>

  <!-- Arrow 2 -> 3 -->
  <line x1="700" y1="780" x2="700" y2="850" class="arr-line" marker-end="url(#arrow)" />
  <rect x="410" y="796" width="580" height="38" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
  <text x="700" y="821" class="txt-lbl">rdm_rx_sync (Tín hiệu đã đồng bộ miền Clock SoC 50 MHz)</text>

  <!-- STAGE 3 -->
  <rect x="60" y="850" width="1280" height="290" class="card-box" />
  <text x="700" y="888" class="txt-card-h1">GIAI ĐOẠN 3: BỘ THU UART RX LẤY MẪU ĐA SỐ 16X (uart_rx.v)</text>
  <text x="700" y="915" class="txt-card-h2">Khôi phục dòng byte ASCII từ chuỗi xung bit nối tiếp với thuật toán lọc nhiễu 3 điểm</text>
  <line x1="90" y1="930" x2="1310" y2="930" stroke="#000000" stroke-width="2.0" />
  <text x="90" y="965" class="txt-body"><tspan font-weight="bold">• Bộ chia tần số Baudrate phần cứng:</tspan> Divisor = 50,000,000 / 9600 = 5208 chu kỳ clock/bit (lấy mẫu 16x oversampling).</text>
  <text x="90" y="1005" class="txt-body"><tspan font-weight="bold">• Bộ bỏ phiếu đa số 3 mẫu liên tiếp:</tspan> Lấy mẫu tại Ticks 7, 8, 9 ở chính giữa bit (Mid-bit), triệt tiêu hoàn toàn xung gai nhiễu điện từ.</text>
  <text x="90" y="1045" class="txt-body"><tspan font-weight="bold">• Thanh ghi dịch SIPO 8-bit &amp; Strobe:</tspan> Tái lập từng byte ASCII <tspan font-weight="bold">hw_rx_byte[7:0]</tspan> và phát xung <tspan font-weight="bold">hw_rx_dv</tspan> (1 chu kỳ clock 20ns).</text>

  <!-- Arrow 3 -> 4 -->
  <line x1="700" y1="1140" x2="700" y2="1210" class="arr-line" marker-end="url(#arrow)" />
  <rect x="360" y="1156" width="680" height="38" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
  <text x="700" y="1181" class="txt-lbl">hw_rx_byte[7:0] (Byte ASCII) + hw_rx_dv (Xung Strobe 1 chu kỳ 20ns)</text>

  <!-- STAGE 4 -->
  <rect x="60" y="1210" width="1280" height="320" class="card-box" />
  <text x="700" y="1248" class="txt-card-h1">GIAI ĐOẠN 4: FSM GIẢI MÃ KHUNG 14 BYTE &amp; CÂY XOR SONG SONG 20ns (rdm6300_frame_decoder.v)</text>
  <text x="700" y="1275" class="txt-card-h2">Máy trạng thái tự động bóc tách khung dữ liệu thẻ và kiểm tra Checksum trong đúng 1 chu kỳ clock</text>
  <line x1="90" y1="1290" x2="1310" y2="1290" stroke="#000000" stroke-width="2.0" />
  <text x="90" y="1325" class="txt-body"><tspan font-weight="bold">• FSM bóc tách khung 14 byte:</tspan> ST_WAIT_STX (0x02) ➔ ST_DATA (10 byte ASCII) ➔ ST_CHECKSUM (2 byte ASCII) ➔ ST_WAIT_ETX (0x03).</text>
  <text x="90" y="1365" class="txt-body"><tspan font-weight="bold">• Chuyển đổi tổ hợp ASCII ➔ Hex nhị phân:</tspan> Tự động quy đổi 10 ký tự ASCII thành 5 byte Hex nhị phân (D[0]..D[4]) trong 0 chu kỳ trễ.</text>
  <text x="90" y="1405" class="txt-body"><tspan font-weight="bold">• Cây toán tử XOR song song 1 chu kỳ (20ns):</tspan> Calc_CS = D[0] ^ D[1] ^ D[2] ^ D[3] ^ D[4]; So khớp Calc_CS == Received_CS.</text>
  <text x="90" y="1445" class="txt-body"><tspan font-weight="bold">• Watchdog Timer chống treo phần cứng:</tspan> Bộ đếm 19-bit (500,000 clock = 10ms) tự động reset FSM về ST_WAIT_STX nếu đứt gói.</text>

  <!-- Arrow 4 -> 5 -->
  <line x1="700" y1="1530" x2="700" y2="1600" class="arr-line" marker-end="url(#arrow)" />
  <rect x="370" y="1546" width="660" height="38" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
  <text x="700" y="1571" class="txt-lbl">tag_id[39:0] (40-bit UID) + card_valid (Strobe) + cs_error (Cờ báo lỗi)</text>

  <!-- STAGE 5 -->
  <rect x="60" y="1600" width="1280" height="320" class="card-box" />
  <text x="700" y="1638" class="txt-card-h1">GIAI ĐOẠN 5: THANH GHI NGOẠI VI MMIO &amp; GIAO DIỆN BUS (rdm6300_mmio.v - 0x1000_0000)</text>
  <text x="700" y="1665" class="txt-card-h2">Lưu trữ kết quả giải mã vào thanh ghi bộ nhớ ánh xạ và phát tín hiệu ngắt đánh thức CPU</text>
  <line x1="90" y1="1680" x2="1310" y2="1680" stroke="#000000" stroke-width="2.0" />
  <text x="90" y="1715" class="txt-body"><tspan font-weight="bold">• REG_RFID_STATUS (0x1000_0000):</tspan> Bit 0 = cờ card_valid (Ghi 1 để xóa cờ sau khi đọc); Bit 1 = cờ checksum_error.</text>
  <text x="90" y="1755" class="txt-body"><tspan font-weight="bold">• REG_RFID_TAG_HI (0x1000_0004):</tspan> Bits [39:32] = Byte Version của thẻ (ví dụ thẻ thật: 0x00).</text>
  <text x="90" y="1795" class="txt-body"><tspan font-weight="bold">• REG_RFID_TAG_LO (0x1000_0008):</tspan> Bits [31:0] = 32-bit số Serial thẻ chuẩn hóa (ví dụ thẻ thật: 0x007293F0).</text>
  <text x="90" y="1835" class="txt-body"><tspan font-weight="bold">• Tín hiệu ngắt card_event_o:</tspan> Tự động kích hoạt ngắt đánh thức CPU PicoRV32 tra cứu danh mục thẻ trên SPI Flash tức thì (&lt; 10 µs).</text>

</svg>
"""
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg)
    shutil.copy2(svg_path, os.path.join(DOC_DIR, "fig2a_rdm6300_subsystem.svg"))
    shutil.copy2(svg_path, os.path.join(PROJECT_DIR, "fig2a_rdm6300_subsystem.svg"))
    print(f"[OK] Generated Fig 2a SVG: {svg_path}")

    # 3. HTML for Chrome Rendering
    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ background: #ffffff; width: {WIDTH}px; height: {HEIGHT}px; overflow: hidden; }}
    svg {{ width: {WIDTH}px; height: {HEIGHT}px; display: block; }}
  </style>
</head>
<body>
  {svg}
</body>
</html>
"""
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    # 4. Render PNG
    run_chrome_headless(html_path, png_path, WIDTH, HEIGHT)
    shutil.copy2(png_path, os.path.join(DOC_DIR, "fig2a_rdm6300_subsystem.png"))
    shutil.copy2(png_path, os.path.join(PROJECT_DIR, "fig2a_rdm6300_subsystem.png"))
    if os.path.exists(ARTIFACT_DIR):
        shutil.copy2(png_path, os.path.join(ARTIFACT_DIR, "fig2a_rdm6300_subsystem.png"))
        print(f"[OK] Copied Fig 2a to Artifacts: {ARTIFACT_DIR}")

# ============================================================================
# DIAGRAM 2B: HOST PC UART FIFO SUBSYSTEM (VERTICAL - BLACK & WHITE)
# ============================================================================
def create_fig2b_vertical():
    drawio_path = os.path.join(TEMP_DIR, "fig2b_host_uart_subsystem.drawio")
    svg_path    = os.path.join(TEMP_DIR, "fig2b_host_uart_subsystem.svg")
    png_path    = os.path.join(TEMP_DIR, "fig2b_host_uart_subsystem.png")
    html_path   = os.path.join(TEMP_DIR, "render_fig2b.html")

    # 1. Draw.io XML
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="2026-10-02T06:15:00.000Z" agent="Mozilla/5.0" version="21.0.0" type="device">
  <diagram id="host_uart_vertical_bnw" name="Host PC UART FIFO Subsystem Vertical">
    <mxGraphModel dx="1600" dy="2200" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{WIDTH}" pageHeight="{HEIGHT}" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- Title Banner -->
        <mxCell id="title" value="&lt;b style=&quot;font-size:26px;&quot;&gt;HÌNH 2B: SƠ ĐỒ KHỐI PHẦN CỨNG GIAO TIẾP HOST PC UART TÍCH HỢP FIFO 32 BYTE&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:18px;&quot;&gt;Kiến trúc module host_uart_mmio.v (Slave 3: 0x3000_0000): Host Console C ➔ FTDI FT2232 ➔ CDC 2-FF ➔ FIFO 32B ➔ MMIO Registers&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2.5;fontFamily=Arial,Helvetica,sans-serif;align=center;" vertex="1" parent="1">
          <mxGeometry x="60" y="30" width="1280" height="90" as="geometry" />
        </mxCell>

        <!-- STAGE 1: HOST CONSOLE C -->
        <mxCell id="stg1" value="&lt;b style=&quot;font-size:23px;&quot;&gt;GIAI ĐOẠN 1: PHẦN MỀM QUẢN TRỊ MÁY TÍNH HOST CONSOLE (host/main.c)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:18px;font-weight:bold;&quot;&gt;Giao diện điều khiển Win32 C Console phát tập lệnh quản trị 13 chức năng kiểm soát ra vào&lt;/span&gt;&lt;hr style=&quot;border:0;border-top:2px solid #000000;margin:10px 0;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:18px;line-height:1.6;&quot;&gt;• &lt;b&gt;Giao thức điều khiển 13 chức năng:&lt;/b&gt; Ping kết nối (P), Thêm thẻ mới (N), Tra cứu danh sách (C), Quẹt ảo (R), Nhật ký (L, K), v.v.&lt;br&gt;• &lt;b&gt;Bộ tiền xử lý &amp;amp; chuẩn hóa dữ liệu thẻ:&lt;/b&gt; Tự động quy đổi linh hoạt giữa 10 số in trên thẻ, định dạng Wiegand (114, 37872) và mã Hex 10 ký tự.&lt;br&gt;• &lt;b&gt;Truyền nhận chuỗi khối qua USB:&lt;/b&gt; Phát chuỗi lệnh liên tục tốc độ cao qua cáp USB Type-B nối trực tiếp với máy tính quản trị.&lt;/div&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2.2;fontFamily=Arial,Helvetica,sans-serif;align=center;verticalAlign=top;spacingTop=12;spacingLeft=16;spacingRight=16;" vertex="1" parent="1">
          <mxGeometry x="60" y="150" width="1280" height="280" as="geometry" />
        </mxCell>

        <!-- Arrow 1 -> 2 -->
        <mxCell id="arr1_2" value="D+/D- USB Bus ➔ Tín hiệu UART nối tiếp TTL 3.3V (uart_rx / uart_tx)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#000000;fontSize=18;fontStyle=1;endArrow=block;endFill=1;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="stg1" target="stg2">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- STAGE 2: FTDI & CDC 2-FF -->
        <mxCell id="stg2" value="&lt;b style=&quot;font-size:23px;&quot;&gt;GIAI ĐOẠN 2: IC CẦU NỐI FTDI FT2232 &amp;amp; BỘ ĐỒNG BỘ CDC 2-FF (sync_2ff.v)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:18px;font-weight:bold;&quot;&gt;Chuyển đổi giao thức USB sang UART và khử bất ổn định trước khi đưa vào nhân vi mạch&lt;/span&gt;&lt;hr style=&quot;border:0;border-top:2px solid #000000;margin:10px 0;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:18px;line-height:1.6;&quot;&gt;• &lt;b&gt;Cầu nối phần cứng FTDI FT2232:&lt;/b&gt; Chuyển đổi tín hiệu USB CDC sang luồng UART nối tiếp chuẩn logic TTL 3.3V.&lt;br&gt;• &lt;b&gt;Tầng khử bất ổn định 2-Stage D-FF:&lt;/b&gt; Đồng bộ hóa tín hiệu uart_rx từ cáp USB vào miền xung nhịp nội bộ 50 MHz của vi mạch.&lt;br&gt;• &lt;b&gt;Chống méo dạng và phản xạ xung:&lt;/b&gt; Khử triệt để các xung gai ký sinh sinh ra trên đường dây cáp USB dài, bảo vệ mạch số ASIC.&lt;br&gt;• &lt;b&gt;Tín hiệu đồng bộ:&lt;/b&gt; &lt;b&gt;uart_rx_sync&lt;/b&gt; sẵn sàng cấp cho bộ giải mã UART nội bộ; Chiều phát: &lt;b&gt;uart_tx_o&lt;/b&gt; đưa trực tiếp ra ngoài.&lt;/div&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2.2;fontFamily=Arial,Helvetica,sans-serif;align=center;verticalAlign=top;spacingTop=12;spacingLeft=16;spacingRight=16;" vertex="1" parent="1">
          <mxGeometry x="60" y="500" width="1280" height="280" as="geometry" />
        </mxCell>

        <!-- Arrow 2 -> 3 -->
        <mxCell id="arr2_3" value="uart_rx_sync (Miền Clock 50 MHz) | Kênh phát: uart_tx_o" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#000000;fontSize=18;fontStyle=1;endArrow=block;endFill=1;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="stg2" target="stg3">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- STAGE 3: UART RX/TX CONTROLLER & BAUD -->
        <mxCell id="stg3" value="&lt;b style=&quot;font-size:23px;&quot;&gt;GIAI ĐOẠN 3: BỘ ĐIỀU KHIỂN UART RX/TX &amp;amp; BỘ CHIA BAUDRATE (simpleuart.v)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:18px;font-weight:bold;&quot;&gt;Đóng gói và giải gói khung truyền nối tiếp với bộ chia tần số baudrate lập trình được&lt;/span&gt;&lt;hr style=&quot;border:0;border-top:2px solid #000000;margin:10px 0;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:18px;line-height:1.6;&quot;&gt;• &lt;b&gt;Bộ chia tần số Baudrate linh hoạt:&lt;/b&gt; Thanh ghi cfg_divider (mặc định 5208 ➔ 9600 bps, hỗ trợ lên tới 115200 bps).&lt;br&gt;• &lt;b&gt;Bộ thu UART RX:&lt;/b&gt; Tự động phát hiện Start bit, lấy mẫu 8-bit dữ liệu, kiểm tra Stop bit hợp lệ và tạo xung rx_push.&lt;br&gt;• &lt;b&gt;Bộ phát UART TX:&lt;/b&gt; Tự động tạo khung truyền (Start bit, 8-bit data, Stop bit) đẩy dữ liệu ra chân uart_tx tới máy tính khi có xung tx_start.&lt;br&gt;• &lt;b&gt;Bắt tay luồng byte nội bộ:&lt;/b&gt; Đẩy byte nhận vào RX FIFO và rút byte cần gửi từ TX FIFO.&lt;/div&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2.2;fontFamily=Arial,Helvetica,sans-serif;align=center;verticalAlign=top;spacingTop=12;spacingLeft=16;spacingRight=16;" vertex="1" parent="1">
          <mxGeometry x="60" y="850" width="1280" height="290" as="geometry" />
        </mxCell>

        <!-- Arrow 3 -> 4 -->
        <mxCell id="arr3_4" value="rx_byte[7:0] + rx_push ➔ Nạp RX FIFO | Rút TX FIFO ➔ tx_byte[7:0] + tx_start" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#000000;fontSize=18;fontStyle=1;endArrow=block;endFill=1;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="stg3" target="stg4">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- STAGE 4: HARDWARE FIFO BUFFERS -->
        <mxCell id="stg4" value="&lt;b style=&quot;font-size:23px;&quot;&gt;GIAI ĐOẠN 4: CẶP BỘ ĐỆM PHẦN CỨNG FIFO 32 BYTE ĐỘC LẬP (sync_fifo.v)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:18px;font-weight:bold;&quot;&gt;Hai hàng đợi FIFO 32x8-bit độc lập giúp chống tràn bộ đệm khi CPU PicoRV32 bận ghi Flash&lt;/span&gt;&lt;hr style=&quot;border:0;border-top:2px solid #000000;margin:10px 0;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:18px;line-height:1.6;&quot;&gt;• &lt;b&gt;Hai hàng đợi FIFO 32-Byte riêng biệt:&lt;/b&gt; Kênh nhận (RX FIFO 32x8-bit) và kênh phát (TX FIFO 32x8-bit) hoạt động song công hoàn toàn.&lt;br&gt;• &lt;b&gt;Quản lý con trỏ phần cứng:&lt;/b&gt; Tự động cập nhật con trỏ ghi wr_ptr[4:0], con trỏ đọc rd_ptr[4:0] và bộ đếm dung lượng fifo_count[5:0].&lt;br&gt;• &lt;b&gt;BẢO VỆ CHỐNG TRÀN BỘ ĐỆM PHẦN CỨNG:&lt;/b&gt; Cách ly hoàn toàn tốc độ truyền dữ liệu của Host PC với CPU PicoRV32 khi CPU bận chu kỳ xóa/ghi Flash (WIP kéo dài tới vài milli-giây).&lt;br&gt;• &lt;b&gt;Cờ trạng thái thời gian thực:&lt;/b&gt; Xuất các cờ rx_empty, rx_full, tx_empty, tx_full phản ánh trạng thái hàng đợi tức thì.&lt;/div&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2.2;fontFamily=Arial,Helvetica,sans-serif;align=center;verticalAlign=top;spacingTop=12;spacingLeft=16;spacingRight=16;" vertex="1" parent="1">
          <mxGeometry x="60" y="1210" width="1280" height="320" as="geometry" />
        </mxCell>

        <!-- Arrow 4 -> 5 -->
        <mxCell id="arr4_5" value="fifo_rdata[7:0] + fifo_valid (Bắt tay 1 chu kỳ 20ns) ➔ Bus ghép nối MMIO 32-bit" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#000000;fontSize=18;fontStyle=1;endArrow=block;endFill=1;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="stg4" target="stg5">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- STAGE 5: MMIO ADDRESS DECODER -->
        <mxCell id="stg5" value="&lt;b style=&quot;font-size:23px;&quot;&gt;GIAI ĐOẠN 5: THANH GHI NGOẠI VI MMIO &amp;amp; GIAO DIỆN BUS (host_uart_mmio.v - 0x3000_0000)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:18px;font-weight:bold;&quot;&gt;Ánh xạ không gian địa chỉ bộ nhớ MMIO và bắt tay chu kỳ bus 1 clock với CPU&lt;/span&gt;&lt;hr style=&quot;border:0;border-top:2px solid #000000;margin:10px 0;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:18px;line-height:1.6;&quot;&gt;• &lt;b&gt;REG_PC_UART_DAT (0x3000_0000):&lt;/b&gt; Đọc byte từ đỉnh RX FIFO (trả về 0x0000_00XX nếu có byte, hoặc 0xFFFF_FFFF nếu FIFO rỗng); Ghi byte vào TX FIFO.&lt;br&gt;• &lt;b&gt;REG_PC_UART_CFG (0x3000_0004):&lt;/b&gt; Cấu hình bộ chia baudrate 32-bit (cfg_divider).&lt;br&gt;• &lt;b&gt;REG_PC_UART_STATUS (0x3000_0008):&lt;/b&gt; Cờ trạng thái rx_ready, tx_busy, số lượng byte chờ rx_count[5:0] và tx_count[5:0].&lt;br&gt;• &lt;b&gt;Bắt tay bus Native MMIO:&lt;/b&gt; Phản hồi mem_ready = 1 trong đúng 1 chu kỳ clock (20ns), không làm nghẽn bus hệ thống của PicoRV32.&lt;/div&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2.2;fontFamily=Arial,Helvetica,sans-serif;align=center;verticalAlign=top;spacingTop=12;spacingLeft=16;spacingRight=16;" vertex="1" parent="1">
          <mxGeometry x="60" y="1600" width="1280" height="320" as="geometry" />
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
    with open(drawio_path, "w", encoding="utf-8") as f:
        f.write(xml)
    shutil.copy2(drawio_path, os.path.join(DOC_DIR, "fig2b_host_uart_subsystem.drawio"))
    shutil.copy2(drawio_path, os.path.join(PROJECT_DIR, "fig2b_host_uart_subsystem.drawio"))
    print(f"[OK] Generated Fig 2b Draw.io: {drawio_path}")

    # 2. Vector SVG
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}">
  <defs>
    <style>
      .border-box {{ fill: #ffffff; stroke: #000000; stroke-width: 2.5; }}
      .card-box {{ fill: #ffffff; stroke: #000000; stroke-width: 2.2; }}
      .arr-line {{ stroke: #000000; stroke-width: 3.0; fill: none; }}
      .arrowhead {{ fill: #000000; }}
      .txt-title {{ font-family: Arial, Helvetica, sans-serif; font-size: 26px; font-weight: bold; text-anchor: middle; fill: #000000; }}
      .txt-sub {{ font-family: Arial, Helvetica, sans-serif; font-size: 18px; text-anchor: middle; fill: #222222; }}
      .txt-card-h1 {{ font-family: Arial, Helvetica, sans-serif; font-size: 23px; font-weight: bold; text-anchor: middle; fill: #000000; }}
      .txt-card-h2 {{ font-family: Arial, Helvetica, sans-serif; font-size: 18px; font-weight: bold; text-anchor: middle; fill: #333333; }}
      .txt-body {{ font-family: Arial, Helvetica, sans-serif; font-size: 18px; fill: #111111; }}
      .txt-lbl {{ font-family: Arial, Helvetica, sans-serif; font-size: 18px; font-weight: bold; text-anchor: middle; fill: #000000; }}
    </style>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" class="arrowhead" />
    </marker>
  </defs>

  <rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" fill="#ffffff" />

  <!-- Title Banner -->
  <rect x="60" y="30" width="1280" height="90" class="border-box" />
  <text x="700" y="66" class="txt-title">HÌNH 2B: SƠ ĐỒ KHỐI PHẦN CỨNG GIAO TIẾP HOST PC UART TÍCH HỢP FIFO 32 BYTE</text>
  <text x="700" y="98" class="txt-sub">Kiến trúc module host_uart_mmio.v (Slave 3: 0x3000_0000): Host Console C ➔ FTDI FT2232 ➔ CDC 2-FF ➔ FIFO 32B ➔ MMIO Registers</text>

  <!-- STAGE 1 -->
  <rect x="60" y="150" width="1280" height="280" class="card-box" />
  <text x="700" y="188" class="txt-card-h1">GIAI ĐOẠN 1: PHẦN MỀM QUẢN TRỊ MÁY TÍNH HOST CONSOLE (host/main.c)</text>
  <text x="700" y="215" class="txt-card-h2">Giao diện điều khiển Win32 C Console phát tập lệnh quản trị 13 chức năng kiểm soát ra vào</text>
  <line x1="90" y1="230" x2="1310" y2="230" stroke="#000000" stroke-width="2.0" />
  <text x="90" y="265" class="txt-body"><tspan font-weight="bold">• Giao thức điều khiển 13 chức năng:</tspan> Ping kết nối (P), Thêm thẻ mới (N), Tra cứu danh sách (C), Quẹt ảo (R), Nhật ký (L, K), v.v.</text>
  <text x="90" y="305" class="txt-body"><tspan font-weight="bold">• Bộ tiền xử lý &amp; chuẩn hóa dữ liệu thẻ:</tspan> Tự động quy đổi linh hoạt giữa 10 số in trên thẻ, Wiegand (114, 37872) và mã Hex 10 ký tự.</text>
  <text x="90" y="345" class="txt-body"><tspan font-weight="bold">• Truyền nhận chuỗi khối qua USB:</tspan> Phát chuỗi lệnh liên tục tốc độ cao qua cáp USB Type-B nối trực tiếp với máy tính quản trị.</text>

  <!-- Arrow 1 -> 2 -->
  <line x1="700" y1="430" x2="700" y2="500" class="arr-line" marker-end="url(#arrow)" />
  <rect x="360" y="446" width="680" height="38" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
  <text x="700" y="471" class="txt-lbl">D+/D- USB Bus ➔ Tín hiệu UART nối tiếp TTL 3.3V (uart_rx / uart_tx)</text>

  <!-- STAGE 2 -->
  <rect x="60" y="500" width="1280" height="280" class="card-box" />
  <text x="700" y="538" class="txt-card-h1">GIAI ĐOẠN 2: IC CẦU NỐI FTDI FT2232 &amp; BỘ ĐỒNG BỘ CDC 2-FF (sync_2ff.v)</text>
  <text x="700" y="565" class="txt-card-h2">Chuyển đổi giao thức USB sang UART và khử bất ổn định trước khi đưa vào nhân vi mạch</text>
  <line x1="90" y1="580" x2="1310" y2="580" stroke="#000000" stroke-width="2.0" />
  <text x="90" y="615" class="txt-body"><tspan font-weight="bold">• Cầu nối phần cứng FTDI FT2232:</tspan> Chuyển đổi tín hiệu USB CDC sang luồng UART nối tiếp chuẩn logic TTL 3.3V.</text>
  <text x="90" y="655" class="txt-body"><tspan font-weight="bold">• Tầng khử bất ổn định 2-Stage D-FF:</tspan> Đồng bộ hóa tín hiệu uart_rx từ cáp USB vào miền xung nhịp nội bộ 50 MHz của vi mạch.</text>
  <text x="90" y="695" class="txt-body"><tspan font-weight="bold">• Chống méo dạng &amp; phản xạ xung:</tspan> Khử triệt để xung gai ký sinh trên cáp USB dài | Ngõ phát: <tspan font-weight="bold">uart_tx_o</tspan> đưa trực tiếp ra ngoài.</text>

  <!-- Arrow 2 -> 3 -->
  <line x1="700" y1="780" x2="700" y2="850" class="arr-line" marker-end="url(#arrow)" />
  <rect x="420" y="796" width="560" height="38" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
  <text x="700" y="821" class="txt-lbl">uart_rx_sync (Miền Clock 50 MHz) | Kênh phát: uart_tx_o</text>

  <!-- STAGE 3 -->
  <rect x="60" y="850" width="1280" height="290" class="card-box" />
  <text x="700" y="888" class="txt-card-h1">GIAI ĐOẠN 3: BỘ ĐIỀU KHIỂN UART RX/TX &amp; BỘ CHIA BAUDRATE (simpleuart.v)</text>
  <text x="700" y="915" class="txt-card-h2">Đóng gói và giải gói khung truyền nối tiếp với bộ chia tần số baudrate lập trình được</text>
  <line x1="90" y1="930" x2="1310" y2="930" stroke="#000000" stroke-width="2.0" />
  <text x="90" y="965" class="txt-body"><tspan font-weight="bold">• Bộ chia tần số Baudrate linh hoạt:</tspan> Thanh ghi cfg_divider (mặc định 5208 ➔ 9600 bps, hỗ trợ lên tới 115200 bps).</text>
  <text x="90" y="1005" class="txt-body"><tspan font-weight="bold">• Bộ thu UART RX:</tspan> Tự động phát hiện Start bit, lấy mẫu 8-bit dữ liệu, kiểm tra Stop bit hợp lệ và tạo xung rx_push.</text>
  <text x="90" y="1045" class="txt-body"><tspan font-weight="bold">• Bộ phát UART TX &amp; FIFO:</tspan> Tự động đẩy dữ liệu nối tiếp ra chân <tspan font-weight="bold">uart_tx_o</tspan> và rút byte từ hàng đợi FIFO 32-byte.</text>

  <!-- Arrow 3 -> 4 -->
  <line x1="700" y1="1140" x2="700" y2="1210" class="arr-line" marker-end="url(#arrow)" />
  <rect x="360" y="1156" width="680" height="38" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
  <text x="700" y="1181" class="txt-lbl">rx_byte[7:0] + rx_push ➔ Nạp RX FIFO | Rút TX FIFO ➔ tx_byte[7:0] + tx_start</text>

  <!-- STAGE 4 -->
  <rect x="60" y="1210" width="1280" height="320" class="card-box" />
  <text x="700" y="1248" class="txt-card-h1">GIAI ĐOẠN 4: CẶP BỘ ĐỆM PHẦN CỨNG FIFO 32 BYTE ĐỘC LẬP (sync_fifo.v)</text>
  <text x="700" y="1275" class="txt-card-h2">Hai hàng đợi FIFO 32x8-bit độc lập giúp chống tràn bộ đệm khi CPU PicoRV32 bận ghi Flash</text>
  <line x1="90" y1="1290" x2="1310" y2="1290" stroke="#000000" stroke-width="2.0" />
  <text x="90" y="1325" class="txt-body"><tspan font-weight="bold">• Hai hàng đợi FIFO 32-Byte riêng biệt:</tspan> Kênh nhận (RX FIFO 32x8-bit) và kênh phát (TX FIFO 32x8-bit) hoạt động song công hoàn toàn.</text>
  <text x="90" y="1365" class="txt-body"><tspan font-weight="bold">• Quản lý con trỏ phần cứng:</tspan> Tự động cập nhật con trỏ ghi wr_ptr[4:0], con trỏ đọc rd_ptr[4:0] và bộ đếm dung lượng fifo_count[5:0].</text>
  <text x="90" y="1405" class="txt-body"><tspan font-weight="bold">• BẢO VỆ CHỐNG TRÀN BỘ ĐỆM PHẦN CỨNG:</tspan> Cách ly hoàn toàn tốc độ truyền dữ liệu của Host PC với CPU PicoRV32 khi CPU bận chu kỳ xóa/ghi Flash (WIP kéo dài tới vài milli-giây).</text>
  <text x="90" y="1445" class="txt-body"><tspan font-weight="bold">• Cờ trạng thái thời gian thực:</tspan> Xuất các cờ rx_empty, rx_full, tx_empty, tx_full phản ánh trạng thái hàng đợi tức thì.</text>

  <!-- Arrow 4 -> 5 -->
  <line x1="700" y1="1530" x2="700" y2="1600" class="arr-line" marker-end="url(#arrow)" />
  <rect x="320" y="1546" width="760" height="38" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
  <text x="700" y="1571" class="txt-lbl">fifo_rdata[7:0] + fifo_valid (Bắt tay 1 chu kỳ 20ns) ➔ Bus ghép nối MMIO 32-bit</text>

  <!-- STAGE 5 -->
  <rect x="60" y="1600" width="1280" height="320" class="card-box" />
  <text x="700" y="1638" class="txt-card-h1">GIAI ĐOẠN 5: THANH GHI NGOẠI VI MMIO &amp; GIAO DIỆN BUS (host_uart_mmio.v - 0x3000_0000)</text>
  <text x="700" y="1665" class="txt-card-h2">Ánh xạ không gian địa chỉ bộ nhớ MMIO và bắt tay chu kỳ bus 1 clock với CPU</text>
  <line x1="90" y1="1680" x2="1310" y2="1680" stroke="#000000" stroke-width="2.0" />
  <text x="90" y="1715" class="txt-body"><tspan font-weight="bold">• REG_PC_UART_DAT (0x3000_0000):</tspan> Đọc byte từ đỉnh RX FIFO (0x00..0xXX, hoặc 0xFFFFFFFF nếu rỗng); Ghi byte vào TX FIFO.</text>
  <text x="90" y="1755" class="txt-body"><tspan font-weight="bold">• REG_PC_UART_CFG (0x3000_0004):</tspan> Cấu hình bộ chia baudrate 32-bit (cfg_divider).</text>
  <text x="90" y="1795" class="txt-body"><tspan font-weight="bold">• REG_PC_UART_STATUS (0x3000_0008):</tspan> Cờ trạng thái rx_ready, tx_busy, số lượng byte chờ rx_count[5:0] và tx_count[5:0].</text>
  <text x="90" y="1835" class="txt-body"><tspan font-weight="bold">• Bắt tay bus Native MMIO:</tspan> Phản hồi mem_ready = 1 trong đúng 1 chu kỳ clock (20ns), không làm nghẽn bus hệ thống của PicoRV32.</text>

</svg>
"""
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg)
    shutil.copy2(svg_path, os.path.join(DOC_DIR, "fig2b_host_uart_subsystem.svg"))
    shutil.copy2(svg_path, os.path.join(PROJECT_DIR, "fig2b_host_uart_subsystem.svg"))
    print(f"[OK] Generated Fig 2b SVG: {svg_path}")

    # 3. HTML for Chrome Rendering
    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ background: #ffffff; width: {WIDTH}px; height: {HEIGHT}px; overflow: hidden; }}
    svg {{ width: {WIDTH}px; height: {HEIGHT}px; display: block; }}
  </style>
</head>
<body>
  {svg}
</body>
</html>
"""
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    # 4. Render PNG
    run_chrome_headless(html_path, png_path, WIDTH, HEIGHT)
    shutil.copy2(png_path, os.path.join(DOC_DIR, "fig2b_host_uart_subsystem.png"))
    shutil.copy2(png_path, os.path.join(PROJECT_DIR, "fig2b_host_uart_subsystem.png"))
    if os.path.exists(ARTIFACT_DIR):
        shutil.copy2(png_path, os.path.join(ARTIFACT_DIR, "fig2b_host_uart_subsystem.png"))
        print(f"[OK] Copied Fig 2b to Artifacts: {ARTIFACT_DIR}")

if __name__ == "__main__":
    print("[INFO] Generating Fig 2a Vertical (RDM6300 Subsystem)...")
    create_fig2a_vertical()
    print("\n[INFO] Generating Fig 2b Vertical (Host UART FIFO Subsystem)...")
    create_fig2b_vertical()
    print("\n[SUCCESS] Completed generation of both vertical diagrams!")
