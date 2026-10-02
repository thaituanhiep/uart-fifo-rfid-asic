# -*- coding: utf-8 -*-
"""
Script: generate_drawio_flow_diagram.py
Generates the authentic Draw.io Black & White Execution & Data Flow Diagram
strictly matching the user's requested architecture:
  [NGUỒN 1: HOST PC]              [NGUỒN 2: THẺ RFID RDM6300]
     (Gõ lệnh UART)                     (Quẹt thẻ 125kHz)
           |                                   |
           v (uart_rx_i)                       v (rdm6300_rx_i)
  +------------------+                +------------------+
  | sync_2ff + UART  |                | sync_2ff + UART  |
  | + sync_fifo 32B  |                | + Frame Decoder  |
  +------------------+                +------------------+
           | (0x3000_0004)                     | (0x1000_0000)
           +-----------------+-----------------+
                             |
                             v
               +---------------------------+
               |     soc_interconnect      |
               +---------------------------+
                             |
                             v (PicoRV32 Native Bus)
               +---------------------------+
               |  PicoRV32 CPU (Firmware)  | <--- Fetch code XIP từ Flash (Detailed sub-boxes)
               |     (firmware/main.c)     |
               +---------------------------+
                 |             |             |
        (0x0030_0000)     (0x4000_0000) (0x3000_0004)
                 |             |             |
                 v             v             v
            [SPI FLASH]    [GPIO LEDs]   [HOST PC UART]
           Tra cứu thẻ /   Bật LED Xanh/   Phản hồi ASCII
           Ghi nhật ký     Đỏ/Flash bận    về màn hình PC

- Pure Black & White (white boxes, solid black borders 2px)
- Large, bold typography (13px - 22px)
- NO code variables inside block boxes
- Fully detailed CPU box with 3 internal sub-boxes
- Outputs:
  1. rdm6300_picorv32_soc_execution_flow.drawio (Authentic Draw.io XML)
  2. rdm6300_picorv32_soc_execution_flow.svg (Vector SVG)
  3. document/temp/fig2_execution_flow.png (High-Res 2x Retina PNG via Headless Chrome)
"""

import os
import subprocess
import shutil

def create_drawio_xml():
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="2026-10-02T05:00:00.000Z" agent="Mozilla/5.0" version="21.0.0" type="device">
  <diagram id="soc_firmware_flow" name="Firmware Execution Flow">
    <mxGraphModel dx="1600" dy="1100" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1560" pageHeight="1080" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- Title Banner -->
        <mxCell id="title" value="&lt;b style=&quot;font-size:22px;&quot;&gt;SƠ ĐỒ LUỒNG ĐIỀU KHIỂN &amp;amp; XỬ LÝ FIRMWARE (FIRMWARE CONTROL &amp;amp; DATA FLOW)&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2.5;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="30" y="20" width="1500" height="50" as="geometry" />
        </mxCell>

        <!-- ============================================================= -->
        <!-- LEVEL 1: TWO INCOMING EVENT SOURCES                           -->
        <!-- ============================================================= -->
        <!-- Source 1: Host PC -->
        <mxCell id="src_pc" value="&lt;b style=&quot;font-size:16px;&quot;&gt;NGUỒN 1: HOST PC&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:13px;&quot;&gt;(Gõ lệnh điều khiển UART qua cổng COM)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="120" y="95" width="560" height="50" as="geometry" />
        </mxCell>

        <!-- Source 2: RFID Reader -->
        <mxCell id="src_rfid" value="&lt;b style=&quot;font-size:16px;&quot;&gt;NGUỒN 2: THẺ RFID RDM6300&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:13px;&quot;&gt;(Quẹt thẻ sóng vô tuyến 125kHz)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="880" y="95" width="560" height="50" as="geometry" />
        </mxCell>

        <!-- Level 1 Hardware Receivers -->
        <mxCell id="hw_pc" value="&lt;b style=&quot;font-size:15.5px;&quot;&gt;Khối thu Host PC UART (0x3000_0004)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:13px;&quot;&gt;sync_2ff + simpleuart (9600 Baud) + sync_fifo (32-byte đệm an toàn)&lt;br&gt;Đệm dữ liệu lệnh, chống mất/tràn gói khi CPU bận&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.8;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="120" y="180" width="560" height="75" as="geometry" />
        </mxCell>

        <mxCell id="hw_rfid" value="&lt;b style=&quot;font-size:15.5px;&quot;&gt;Khối thu Thẻ RFID RDM6300 (0x1000_0000)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:13px;&quot;&gt;sync_2ff + uart_rx (9600 Baud) + rdm6300_frame_decoder&lt;br&gt;Kiểm tra XOR Checksum 14-byte 1-cycle -&amp;gt; Chốt UID vào TAG_HI / TAG_LO &amp;amp; Bật cờ card_valid&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.8;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="880" y="180" width="560" height="75" as="geometry" />
        </mxCell>

        <mxCell id="e_src_pc" value="uart_rx_i" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=13;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="src_pc" target="hw_pc" />
        <mxCell id="e_src_rfid" value="rdm6300_rx_i" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=13;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="src_rfid" target="hw_rfid" />

        <!-- ============================================================= -->
        <!-- LEVEL 2: CENTRAL SOC INTERCONNECT                             -->
        <!-- ============================================================= -->
        <mxCell id="soc_bus" value="&lt;b style=&quot;font-size:17px;&quot;&gt;soc_interconnect.v (Address Decoder &amp;amp; Bus Multiplexer)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:13.5px;&quot;&gt;Giải mã địa chỉ, kích hoạt tín hiệu chọn khối sel_* và ghép kênh dữ liệu đọc rdata / tín hiệu ready&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2.2;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="460" y="295" width="640" height="70" as="geometry" />
        </mxCell>

        <!-- Edges into soc_interconnect -->
        <mxCell id="e_pc_bus" value="0x3000_0004" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=13;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="hw_pc" target="soc_bus">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="400" y="275" />
              <mxPoint x="620" y="275" />
            </Array>
          </mxGeometry>
        </mxCell>

        <mxCell id="e_rfid_bus" value="0x1000_0000" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=13;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="hw_rfid" target="soc_bus">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="1160" y="275" />
              <mxPoint x="940" y="275" />
            </Array>
          </mxGeometry>
        </mxCell>

        <!-- ============================================================= -->
        <!-- LEVEL 3: DETAILED PICORV32 CPU FIRMWARE (C MAIN.C)            -->
        <!-- ============================================================= -->
        <mxCell id="cpu_box" value="&lt;b style=&quot;font-size:18px;&quot;&gt;PicoRV32 RISC-V CPU CORE (FIRMWARE C main.c) - BỘ NÃO ĐIỀU PHỐI HỆ THỐNG&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2.5;verticalAlign=top;align=center;spacingTop=12;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="50" y="405" width="1460" height="325" as="geometry" />
        </mxCell>

        <!-- CPU Edge from Interconnect -->
        <mxCell id="e_bus_cpu" value="PicoRV32 Native Memory Bus" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2.5;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=13;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="soc_bus" target="cpu_box" />

        <!-- Sub-box 1: XIP Fetch -->
        <mxCell id="cpu_xip" value="&lt;b style=&quot;font-size:15.5px;&quot;&gt;1. Nạp Mã Lệnh XIP (Fetch Code từ Flash)&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;span style=&quot;font-size:13px;line-height:1.6;&quot;&gt;• &lt;b&gt;PC Reset = 0x0025_0000&lt;/b&gt; (vị trí đầu firmware.bin)&lt;br&gt;• CPU phát chu kỳ đọc &lt;b&gt;mem_valid=1, mem_instr=1&lt;/b&gt;&lt;br&gt;• &lt;b&gt;spimemio&lt;/b&gt; phát xung nhịp SPI đọc 4 byte từ Flash ngoài&lt;br&gt;• CPU tự động tạm dừng (&lt;b&gt;Stall&lt;/b&gt;) chờ Flash trả dữ liệu&lt;br&gt;• Chốt từ 32-bit vào thanh ghi lệnh (IR), tăng &lt;b&gt;PC = PC + 4&lt;/b&gt;&lt;br&gt;• &lt;b&gt;Thực thi trực tiếp tại chỗ, không cần nạp vào RAM!&lt;/b&gt;&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.8;fontFamily=Arial,Helvetica,sans-serif;align=left;spacingLeft=15;" vertex="1" parent="cpu_box">
          <mxGeometry x="25" y="45" width="445" height="260" as="geometry" />
        </mxCell>

        <!-- Sub-box 2: while(1) loop -->
        <mxCell id="cpu_loop" value="&lt;b style=&quot;font-size:15.5px;&quot;&gt;2. Vòng Lặp Chính Firmware (while(1) Event Loop)&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;span style=&quot;font-size:13px;line-height:1.6;&quot;&gt;• &lt;b&gt;Bước 1: poll_rdm6300()&lt;/b&gt;&lt;br&gt;  Đọc 0x1000_0000: nếu card_valid=1 -&amp;gt; đọc UID &amp;amp; xóa cờ&lt;br&gt;• &lt;b&gt;Bước 2: uart_getc_nonblock()&lt;/b&gt;&lt;br&gt;  Đọc 0x3000_0004: lấy byte lệnh từ đỉnh hàng đợi FIFO&lt;br&gt;• &lt;b&gt;Bước 3: Điều phối lệnh switch(cmd)&lt;/b&gt;&lt;br&gt;  &#39;P&#39;: Ping | &#39;V&#39;: Quét thẻ ảo | &#39;F&#39;: Đọc thẻ | &#39;W&#39;: Ghi thẻ | &#39;E&#39;: Xóa&lt;br&gt;• &lt;b&gt;Bước 4: Tra cứu database &amp;amp; Ra quyết định&lt;/b&gt;&lt;br&gt;  So sánh UID với Flash -&amp;gt; Hợp lệ (Granted) / Bị từ chối (Denied)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.8;fontFamily=Arial,Helvetica,sans-serif;align=left;spacingLeft=15;" vertex="1" parent="cpu_box">
          <mxGeometry x="495" y="45" width="470" height="260" as="geometry" />
        </mxCell>

        <!-- Sub-box 3: 1KB Data SRAM -->
        <mxCell id="cpu_sram" value="&lt;b style=&quot;font-size:15.5px;&quot;&gt;3. Bộ Nhớ 1KB Data SRAM (0x0000_0000)&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;span style=&quot;font-size:13px;line-height:1.6;&quot;&gt;• Ngăn xếp &lt;b&gt;Stack: sp = 0x0000_0400&lt;/b&gt; (đỉnh 1KB SRAM)&lt;br&gt;• Lưu trữ các biến toàn cục &amp;amp; cục bộ C (.data, .bss)&lt;br&gt;• Mảng đệm: last_tag_hex[11], vtag[12], input_tag[11]&lt;br&gt;• Độ trễ đọc/ghi: &lt;b&gt;Cố định đúng 1 chu kỳ clock&lt;/b&gt;&lt;br&gt;• Đảm bảo CPU tính toán và xử lý logic C tốc độ tối đa&lt;br&gt;• Không chứa mã lệnh, chỉ chứa dữ liệu động!&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.8;fontFamily=Arial,Helvetica,sans-serif;align=left;spacingLeft=15;" vertex="1" parent="cpu_box">
          <mxGeometry x="990" y="45" width="445" height="260" as="geometry" />
        </mxCell>

        <!-- ============================================================= -->
        <!-- LEVEL 4: THREE OUTBOUND ACTION CHANNELS                       -->
        <!-- ============================================================= -->
        <!-- Action 1: SPI Flash -->
        <mxCell id="act_flash" value="&lt;b style=&quot;font-size:16px;&quot;&gt;1. SPI FLASH NGOÀI (spimemio.v)&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;span style=&quot;font-size:13px;&quot;&gt;• Tra cứu database danh sách thẻ hợp lệ (&lt;b&gt;0x0030_0000&lt;/b&gt;)&lt;br&gt;• Ghi nhật ký truy cập (Access Log) vào Sector 49 (&lt;b&gt;0x0031_0000&lt;/b&gt;)&lt;br&gt;• Bản ghi 16-byte: Magic + UID + Timestamp + Số lượt quẹt&lt;br&gt;• &lt;b&gt;Lưu trữ vĩnh viễn, không mất dữ liệu khi ngắt nguồn&lt;/b&gt;&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.8;fontFamily=Arial,Helvetica,sans-serif;align=left;spacingLeft=15;" vertex="1" parent="1">
          <mxGeometry x="50" y="780" width="455" height="145" as="geometry" />
        </mxCell>

        <!-- Action 2: GPIO LEDs -->
        <mxCell id="act_leds" value="&lt;b style=&quot;font-size:16px;&quot;&gt;2. GPIO STATUS LEDS (0x4000_0000)&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;span style=&quot;font-size:13px;&quot;&gt;Firmware ghi thanh ghi điều khiển leds_o[15:0]:&lt;br&gt;• &lt;b&gt;Bit 1 (0x0002):&lt;/b&gt; Bật LED Xanh -&amp;gt; &lt;b&gt;CHO PHÉP TRUY CẬP (GRANTED)&lt;/b&gt;&lt;br&gt;• &lt;b&gt;Bit 2 (0x0004):&lt;/b&gt; Bật LED Đỏ -&amp;gt; &lt;b&gt;TỪ CHỐI TRUY CẬP (DENIED)&lt;/b&gt;&lt;br&gt;• &lt;b&gt;Bit 3 (0x0008):&lt;/b&gt; Bật LED Vàng -&amp;gt; &lt;b&gt;ĐANG GHI/XÓA FLASH BẬN&lt;/b&gt;&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.8;fontFamily=Arial,Helvetica,sans-serif;align=left;spacingLeft=15;" vertex="1" parent="1">
          <mxGeometry x="550" y="780" width="460" height="145" as="geometry" />
        </mxCell>

        <!-- Action 3: Host PC UART TX -->
        <mxCell id="act_uart" value="&lt;b style=&quot;font-size:16px;&quot;&gt;3. HOST PC UART (simpleuart.v)&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;span style=&quot;font-size:13px;&quot;&gt;Firmware ghi từng ký tự vào 0x3000_0004 -&amp;gt; chân &lt;b&gt;uart_tx_o&lt;/b&gt;:&lt;br&gt;• &lt;b&gt;PONG: PicoRV32 Active&lt;/b&gt;&lt;br&gt;• &lt;b&gt;SCAN:TAG=000073161D:ACCESS_GRANTED:SLOT=0&lt;/b&gt;&lt;br&gt;• &lt;b&gt;LOG_ITEM:0:SUCC:000073161D:1&lt;/b&gt;&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.8;fontFamily=Arial,Helvetica,sans-serif;align=left;spacingLeft=15;" vertex="1" parent="1">
          <mxGeometry x="1055" y="780" width="455" height="145" as="geometry" />
        </mxCell>

        <!-- Edges from CPU to Outbound Actions -->
        <mxCell id="e_cpu_flash" value="0x0030_0000" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=13;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="277" y="730" as="sourcePoint" />
            <mxPoint x="277" y="780" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <mxCell id="e_cpu_leds" value="0x4000_0000" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=13;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="780" y="730" as="sourcePoint" />
            <mxPoint x="780" y="780" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <mxCell id="e_cpu_uart" value="0x3000_0004" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=13;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="1282" y="730" as="sourcePoint" />
            <mxPoint x="1282" y="780" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <!-- Final Target Entities -->
        <mxCell id="tgt_flash" value="&lt;b style=&quot;font-size:15px;&quot;&gt;Chip Nhớ SPI Flash W25Q128 (16 MByte Off-Chip)&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.8;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="50" y="970" width="455" height="55" as="geometry" />
        </mxCell>

        <mxCell id="tgt_pc" value="&lt;b style=&quot;font-size:15px;&quot;&gt;Màn Hình Máy Tính Host PC (Giao Diện Người Dùng)&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.8;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="1055" y="970" width="455" height="55" as="geometry" />
        </mxCell>

        <mxCell id="e_act_tgt_flash" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#000000;endArrow=classic;endFill=1;" edge="1" parent="1" source="act_flash" target="tgt_flash" />
        <mxCell id="e_act_tgt_pc" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#000000;endArrow=classic;endFill=1;" edge="1" parent="1" source="act_uart" target="tgt_pc" />

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
    return xml

def generate_svg():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1560 1080" width="100%" height="100%" style="background-color: #ffffff; font-family: Arial, Helvetica, sans-serif;">
  <defs>
    <marker id="arr" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="10" markerHeight="10" markerUnits="userSpaceOnUse" orient="auto">
      <path d="M 1 2 L 10 6 L 1 10 z" fill="#000000" />
    </marker>
  </defs>

  <!-- ===================================================================== -->
  <!-- TITLE BANNER                                                          -->
  <!-- ===================================================================== -->
  <rect x="30" y="20" width="1500" height="50" fill="#ffffff" stroke="#000000" stroke-width="2.5" />
  <text x="780" y="52" font-size="20" font-weight="bold" fill="#000000" text-anchor="middle">SƠ ĐỒ LUỒNG ĐIỀU KHIỂN &amp; XỬ LÝ FIRMWARE (FIRMWARE CONTROL &amp; DATA FLOW)</text>

  <!-- ===================================================================== -->
  <!-- LEVEL 1: TWO INCOMING EVENT SOURCES                                   -->
  <!-- ===================================================================== -->
  <!-- Source 1: Host PC -->
  <rect x="120" y="95" width="560" height="50" fill="#ffffff" stroke="#000000" stroke-width="2" />
  <text x="400" y="120" font-size="16" font-weight="bold" fill="#000000" text-anchor="middle">NGUỒN 1: HOST PC</text>
  <text x="400" y="137" font-size="13" fill="#333333" text-anchor="middle">(Gõ lệnh điều khiển UART qua cổng COM)</text>

  <!-- Source 2: RFID Reader -->
  <rect x="880" y="95" width="560" height="50" fill="#ffffff" stroke="#000000" stroke-width="2" />
  <text x="1160" y="120" font-size="16" font-weight="bold" fill="#000000" text-anchor="middle">NGUỒN 2: THẺ RFID RDM6300</text>
  <text x="1160" y="137" font-size="13" fill="#333333" text-anchor="middle">(Quẹt thẻ sóng vô tuyến 125kHz)</text>

  <!-- Level 1 Hardware Receivers -->
  <rect x="120" y="180" width="560" height="75" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
  <text x="400" y="206" font-size="15.5" font-weight="bold" fill="#000000" text-anchor="middle">Khối thu Host PC UART (0x3000_0004)</text>
  <text x="400" y="228" font-size="13" fill="#222222" text-anchor="middle">sync_2ff + simpleuart (9600 Baud) + sync_fifo (32-byte đệm an toàn)</text>
  <text x="400" y="246" font-size="12.5" fill="#444444" text-anchor="middle">Đệm dữ liệu lệnh, chống mất/tràn gói khi CPU bận</text>

  <rect x="880" y="180" width="560" height="75" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
  <text x="1160" y="206" font-size="15.5" font-weight="bold" fill="#000000" text-anchor="middle">Khối thu Thẻ RFID RDM6300 (0x1000_0000)</text>
  <text x="1160" y="228" font-size="13" fill="#222222" text-anchor="middle">sync_2ff + uart_rx (9600 Baud) + rdm6300_frame_decoder</text>
  <text x="1160" y="246" font-size="12.5" font-weight="bold" fill="#000000" text-anchor="middle">XOR Check 1-cycle -&gt; Chốt UID vào TAG_HI/LO &amp; Bật cờ card_valid</text>

  <!-- Arrows from Source to Hardware -->
  <g stroke="#000000" stroke-width="2" fill="none">
    <path d="M 400 145 L 400 180" marker-end="url(#arr)" />
    <path d="M 1160 145 L 1160 180" marker-end="url(#arr)" />
  </g>
  <rect x="365" y="152" width="70" height="18" fill="#ffffff" />
  <text x="400" y="165" font-size="12.5" font-weight="bold" fill="#000000" text-anchor="middle">uart_rx_i</text>
  <rect x="1115" y="152" width="90" height="18" fill="#ffffff" />
  <text x="1160" y="165" font-size="12.5" font-weight="bold" fill="#000000" text-anchor="middle">rdm6300_rx_i</text>

  <!-- ============================================================= -->
  <!-- LEVEL 2: CENTRAL SOC INTERCONNECT                             -->
  <!-- ============================================================= -->
  <rect x="460" y="295" width="640" height="70" fill="#ffffff" stroke="#000000" stroke-width="2.2" />
  <text x="780" y="324" font-size="17" font-weight="bold" fill="#000000" text-anchor="middle">soc_interconnect.v (Address Decoder &amp; Bus Multiplexer)</text>
  <text x="780" y="348" font-size="13.5" fill="#333333" text-anchor="middle">Giải mã địa chỉ, kích hoạt tín hiệu chọn khối sel_* và ghép kênh dữ liệu rdata / ready</text>

  <!-- Edges into soc_interconnect -->
  <g stroke="#000000" stroke-width="2" fill="none">
    <path d="M 400 255 L 400 275 L 620 275 L 620 295" marker-end="url(#arr)" />
    <path d="M 1160 255 L 1160 275 L 940 275 L 940 295" marker-end="url(#arr)" />
  </g>
  <rect x="475" y="266" width="90" height="18" fill="#ffffff" />
  <text x="520" y="279" font-size="12.5" font-weight="bold" fill="#000000" text-anchor="middle">0x3000_0004</text>
  <rect x="995" y="266" width="90" height="18" fill="#ffffff" />
  <text x="1040" y="279" font-size="12.5" font-weight="bold" fill="#000000" text-anchor="middle">0x1000_0000</text>

  <!-- ============================================================= -->
  <!-- LEVEL 3: DETAILED PICORV32 CPU FIRMWARE (C MAIN.C)            -->
  <!-- ============================================================= -->
  <rect x="50" y="405" width="1460" height="325" fill="#ffffff" stroke="#000000" stroke-width="2.5" />
  <text x="780" y="432" font-size="18" font-weight="bold" fill="#000000" text-anchor="middle">PicoRV32 RISC-V CPU CORE (FIRMWARE C main.c) - BỘ NÃO ĐIỀU PHỐI HỆ THỐNG</text>

  <!-- Line from Interconnect to CPU -->
  <path d="M 780 365 L 780 405" stroke="#000000" stroke-width="2.5" fill="none" marker-end="url(#arr)" />
  <rect x="670" y="375" width="220" height="20" fill="#ffffff" stroke="#000000" stroke-width="1" />
  <text x="780" y="389" font-size="12.5" font-weight="bold" fill="#000000" text-anchor="middle">PicoRV32 Native Memory Bus</text>

  <!-- Sub-box 1: XIP Fetch -->
  <rect x="75" y="450" width="445" height="260" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
  <text x="297" y="478" font-size="15.5" font-weight="bold" fill="#000000" text-anchor="middle">1. Nạp Mã Lệnh XIP (Fetch Code từ Flash)</text>
  <line x1="95" y1="490" x2="500" y2="490" stroke="#000000" stroke-width="1" />
  <text x="95" y="514" font-size="13" fill="#222222">• <tspan font-weight="bold">PC Reset = 0x0025_0000</tspan> (vị trí đầu firmware.bin)</text>
  <text x="95" y="540" font-size="13" fill="#222222">• CPU phát chu kỳ đọc <tspan font-weight="bold">mem_valid=1, mem_instr=1</tspan></text>
  <text x="95" y="566" font-size="13" fill="#222222">• <tspan font-weight="bold">spimemio</tspan> phát xung nhịp SPI đọc 4 byte từ Flash ngoài</text>
  <text x="95" y="592" font-size="13" fill="#222222">• CPU tự động tạm dừng (<tspan font-weight="bold">Stall</tspan>) chờ Flash trả dữ liệu</text>
  <text x="95" y="618" font-size="13" fill="#222222">• Chốt từ 32-bit vào thanh ghi lệnh (IR), tăng <tspan font-weight="bold">PC = PC + 4</tspan></text>
  <text x="95" y="648" font-size="13" font-weight="bold" fill="#000000">• Thực thi trực tiếp tại chỗ, không cần nạp vào RAM!</text>
  <text x="95" y="674" font-size="12" fill="#555555">  (15MB Flash Address Space: 0x0010_0000..0x00FF_FFFF)</text>

  <!-- Sub-box 2: while(1) loop -->
  <rect x="545" y="450" width="470" height="260" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
  <text x="780" y="478" font-size="15.5" font-weight="bold" fill="#000000" text-anchor="middle">2. Vòng Lặp Chính Firmware (while(1) Event Loop)</text>
  <line x1="565" y1="490" x2="995" y2="490" stroke="#000000" stroke-width="1" />
  <text x="565" y="514" font-size="13" font-weight="bold" fill="#000000">• Bước 1: poll_rdm6300()</text>
  <text x="580" y="534" font-size="12.5" fill="#222222">Đọc 0x1000_0000: nếu card_valid=1 -&gt; đọc UID &amp; xóa cờ</text>
  <text x="565" y="558" font-size="13" font-weight="bold" fill="#000000">• Bước 2: uart_getc_nonblock()</text>
  <text x="580" y="578" font-size="12.5" fill="#222222">Đọc 0x3000_0004: lấy byte lệnh từ đỉnh hàng đợi FIFO</text>
  <text x="565" y="602" font-size="13" font-weight="bold" fill="#000000">• Bước 3: Điều phối lệnh switch(cmd)</text>
  <text x="580" y="622" font-size="12.5" fill="#222222">&#39;P&#39;: Ping | &#39;V&#39;: Quét thẻ ảo | &#39;F&#39;: Đọc thẻ | &#39;W&#39;: Ghi thẻ | &#39;E&#39;: Xóa</text>
  <text x="565" y="646" font-size="13" font-weight="bold" fill="#000000">• Bước 4: Tra cứu database &amp; Ra quyết định</text>
  <text x="580" y="666" font-size="12.5" fill="#222222">So sánh UID với Flash -&gt; Hợp lệ (Granted) / Bị từ chối (Denied)</text>

  <!-- Sub-box 3: 1KB Data SRAM -->
  <rect x="1040" y="450" width="445" height="260" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
  <text x="1262" y="478" font-size="15.5" font-weight="bold" fill="#000000" text-anchor="middle">3. Bộ Nhớ 1KB Data SRAM (0x0000_0000)</text>
  <line x1="1060" y1="490" x2="1465" y2="490" stroke="#000000" stroke-width="1" />
  <text x="1060" y="514" font-size="13" fill="#222222">• Ngăn xếp <tspan font-weight="bold">Stack: sp = 0x0000_0400</tspan> (đỉnh 1KB SRAM)</text>
  <text x="1060" y="540" font-size="13" fill="#222222">• Lưu trữ các biến toàn cục &amp; cục bộ C (.data, .bss)</text>
  <text x="1060" y="566" font-size="13" fill="#222222">• Mảng đệm: last_tag_hex[11], vtag[12], input_tag[11]</text>
  <text x="1060" y="592" font-size="13" fill="#222222">• Độ trễ đọc/ghi: <tspan font-weight="bold">Cố định đúng 1 chu kỳ clock</tspan></text>
  <text x="1060" y="618" font-size="13" fill="#222222">• Đảm bảo CPU tính toán và xử lý logic C tốc độ tối đa</text>
  <text x="1060" y="648" font-size="13" font-weight="bold" fill="#000000">• Không chứa mã lệnh, chỉ chứa dữ liệu động!</text>

  <!-- ============================================================= -->
  <!-- LEVEL 4: THREE OUTBOUND ACTION CHANNELS                       -->
  <!-- ============================================================= -->
  <!-- Action 1: SPI Flash -->
  <rect x="50" y="780" width="455" height="145" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
  <text x="277" y="808" font-size="16" font-weight="bold" fill="#000000" text-anchor="middle">1. SPI FLASH NGOÀI (spimemio.v)</text>
  <line x1="70" y1="820" x2="485" y2="820" stroke="#000000" stroke-width="1" />
  <text x="70" y="844" font-size="13" fill="#222222">• Tra cứu database danh sách thẻ hợp lệ (<tspan font-weight="bold">0x0030_0000</tspan>)</text>
  <text x="70" y="866" font-size="13" fill="#222222">• Ghi nhật ký truy cập (Access Log) vào Sector 49 (<tspan font-weight="bold">0x0031_0000</tspan>)</text>
  <text x="70" y="888" font-size="13" fill="#222222">• Bản ghi 16-byte: Magic + UID + Timestamp + Số lượt quẹt</text>
  <text x="70" y="910" font-size="13" font-weight="bold" fill="#000000">• Lưu trữ vĩnh viễn, không mất dữ liệu khi ngắt nguồn</text>

  <!-- Action 2: GPIO LEDs -->
  <rect x="550" y="780" width="460" height="145" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
  <text x="780" y="808" font-size="16" font-weight="bold" fill="#000000" text-anchor="middle">2. GPIO STATUS LEDS (0x4000_0000)</text>
  <line x1="570" y1="820" x2="990" y2="820" stroke="#000000" stroke-width="1" />
  <text x="570" y="844" font-size="13" fill="#222222">Firmware ghi thanh ghi điều khiển leds_o[15:0]:</text>
  <text x="570" y="868" font-size="13.5" font-weight="bold" fill="#000000">• Bit 1 (0x0002): Bật LED Xanh -&gt; CHO PHÉP TRUY CẬP</text>
  <text x="570" y="890" font-size="13.5" font-weight="bold" fill="#000000">• Bit 2 (0x0004): Bật LED Đỏ -&gt; TỪ CHỐI TRUY CẬP</text>
  <text x="570" y="912" font-size="13.5" font-weight="bold" fill="#000000">• Bit 3 (0x0008): Bật LED Vàng -&gt; ĐANG GHI/XÓA FLASH BẬN</text>

  <!-- Action 3: Host PC UART TX -->
  <rect x="1055" y="780" width="455" height="145" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
  <text x="1282" y="808" font-size="16" font-weight="bold" fill="#000000" text-anchor="middle">3. HOST PC UART (simpleuart.v)</text>
  <line x1="1075" y1="820" x2="1490" y2="820" stroke="#000000" stroke-width="1" />
  <text x="1075" y="844" font-size="13" fill="#222222">Firmware ghi từng ký tự vào 0x3000_0004 -&gt; chân <tspan font-weight="bold">uart_tx_o</tspan>:</text>
  <text x="1075" y="868" font-size="13.5" font-weight="bold" fill="#000000">• PONG: PicoRV32 Active</text>
  <text x="1075" y="890" font-size="13.5" font-weight="bold" fill="#000000">• SCAN:TAG=000073161D:ACCESS_GRANTED:SLOT=0</text>
  <text x="1075" y="912" font-size="13.5" font-weight="bold" fill="#000000">• LOG_ITEM:0:SUCC:000073161D:1</text>

  <!-- Edges from CPU to Outbound Actions -->
  <g stroke="#000000" stroke-width="2" fill="none">
    <path d="M 277 730 L 277 780" marker-end="url(#arr)" />
    <path d="M 780 730 L 780 780" marker-end="url(#arr)" />
    <path d="M 1282 730 L 1282 780" marker-end="url(#arr)" />
  </g>
  <rect x="232" y="747" width="90" height="18" fill="#ffffff" />
  <text x="277" y="760" font-size="12.5" font-weight="bold" fill="#000000" text-anchor="middle">0x0030_0000</text>
  <rect x="735" y="747" width="90" height="18" fill="#ffffff" />
  <text x="780" y="760" font-size="12.5" font-weight="bold" fill="#000000" text-anchor="middle">0x4000_0000</text>
  <rect x="1237" y="747" width="90" height="18" fill="#ffffff" />
  <text x="1282" y="760" font-size="12.5" font-weight="bold" fill="#000000" text-anchor="middle">0x3000_0004</text>

  <!-- Final Target Entities -->
  <rect x="50" y="970" width="455" height="55" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
  <text x="277" y="1003" font-size="15" font-weight="bold" fill="#000000" text-anchor="middle">Chip Nhớ SPI Flash W25Q128 (16 MByte Off-Chip)</text>

  <rect x="1055" y="970" width="455" height="55" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
  <text x="1282" y="1003" font-size="15" font-weight="bold" fill="#000000" text-anchor="middle">Màn Hình Máy Tính Host PC (Giao Diện Người Dùng)</text>

  <g stroke="#000000" stroke-width="2" fill="none">
    <path d="M 277 925 L 277 970" marker-end="url(#arr)" />
    <path d="M 1282 925 L 1282 970" marker-end="url(#arr)" />
  </g>

</svg>
'''
    return svg

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    # 1. Generate Draw.io XML file (.drawio)
    drawio_content = create_drawio_xml()
    drawio_path = os.path.join(root_dir, "rdm6300_picorv32_soc_execution_flow.drawio")
    with open(drawio_path, "w", encoding="utf-8") as f:
        f.write(drawio_content)
    print(f"[SUCCESS] Wrote Draw.io Flow file: {drawio_path}")

    # 2. Generate clean Black & White SVG (.svg)
    svg_content = generate_svg()
    svg_path = os.path.join(root_dir, "rdm6300_picorv32_soc_execution_flow.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"[SUCCESS] Wrote Flow SVG to: {svg_path}")

    # 3. Create HTML wrapper for Headless Chrome rendering
    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: #ffffff;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0;
    width: 1560px;
    height: 1080px;
  }}
  .diagram-container {{
    width: 1560px;
    height: 1080px;
  }}
</style>
</head>
<body>
  <div class="diagram-container">
    {svg_content}
  </div>
</body>
</html>
"""
    html_path = os.path.join(root_dir, "document", "temp", "render_flow_diagram.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # 4. Render High-Resolution PNG via Headless Chrome (2x retina)
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    png_path = os.path.join(root_dir, "document", "temp", "fig2_execution_flow.png")
    
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--force-device-scale-factor=2",
        f"--screenshot={png_path}",
        "--window-size=1560,1080",
        f"file:///{html_path.replace(os.sep, '/')}"
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(png_path):
        size = os.path.getsize(png_path)
        print(f"[SUCCESS] Rendered Flow PNG via Headless Chrome: {png_path} ({size} bytes)")
    else:
        print(f"[ERROR] Chrome screenshot failed: {res.stderr}")

    # 5. Copy to Brain Artifacts directory
    art_path = r"C:\Users\thait\.gemini\antigravity-ide\brain\40d01579-3c16-4b85-9b12-c0e7d33bcd21\fig2_execution_flow.png"
    if os.path.exists(png_path):
        shutil.copyfile(png_path, art_path)
        print(f"[SUCCESS] Copied Flow PNG to Artifacts: {art_path}")

if __name__ == "__main__":
    main()
