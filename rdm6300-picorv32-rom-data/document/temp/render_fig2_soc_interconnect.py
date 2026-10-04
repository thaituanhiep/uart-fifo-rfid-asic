# -*- coding: utf-8 -*-
"""
Script: render_fig2_soc_interconnect.py
Generates:
1. fig2_soc_interconnect.drawio: Genuine editable Draw.io XML file (app.diagrams.net compatible)
2. fig2_soc_interconnect.png: Ultra-sharp Draw.io-style vector render via Headless Chrome at 2x DPI.

Illustrates:
- CPU Master (PicoRV32) native memory interface
- soc_interconnect.v central 32-bit bus arbiter & address decoder
- Connection to 1KB Data SRAM (Slave 0), SPI Flash XIP via spimemio (Slave 1 & 1b),
  RFID UART with FIFO (Slave 2), Host PC UART with FIFO (Slave 3), GPIO LEDs (Slave 4)
- 4-phase baremetal C firmware execution flow (Reset vector -> XIP fetch -> SRAM stack -> MMIO control -> In-RAM Flash worker)
"""

import os
import subprocess
import shutil

def create_drawio_xml():
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="2026-10-03T12:00:00.000Z" agent="Mozilla/5.0" version="21.0.0" type="device">
  <diagram id="soc_interconnect" name="SoC Interconnect &amp; C Firmware Execution Flow">
    <mxGraphModel dx="1600" dy="1100" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1560" pageHeight="1060" math="0" shadow="1">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- Title Banner -->
        <mxCell id="title" value="&lt;b style=&quot;font-size:22px;color:#0f172a;&quot;&gt;KIẾN TRÚC BUS SOC_INTERCONNECT.V &amp;amp; CƠ CHẾ THỰC THI FIRMWARE C&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:14px;color:#475569;&quot;&gt;Bộ giải mã địa chỉ trung tâm, phân luồng bộ nhớ XIP Flash / 1KB SRAM và giao tiếp ngoại vi MMIO&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#cbd5e1;strokeWidth=2;fontFamily=Segoe UI;shadow=1;" vertex="1" parent="1">
          <mxGeometry x="40" y="20" width="1480" height="70" as="geometry" />
        </mxCell>

        <!-- CPU MASTER CARD -->
        <mxCell id="cpu_master" value="&lt;b style=&quot;font-size:18px;color:#1e3a8a;&quot;&gt;CPU MASTER: PicoRV32&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:13px;color:#2563eb;&quot;&gt;&lt;b&gt;RV32IMC RISC-V Native Core&lt;/b&gt;&lt;/span&gt;&lt;br&gt;&lt;hr style=&quot;border:1px solid #93c5fd;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:12.5px;color:#334155;line-height:1.6;&quot;&gt;&lt;b&gt;• PROGADDR_RESET:&lt;/b&gt; 0x0025_0000 (Flash XIP)&lt;br&gt;&lt;b&gt;• Stack Pointer (sp):&lt;/b&gt; 0x0000_0400 (Top SRAM)&lt;br&gt;&lt;b&gt;• Native Memory Bus:&lt;/b&gt;&lt;br&gt;&amp;nbsp;&amp;nbsp;- cpu_mem_valid (Master Strobe)&lt;br&gt;&amp;nbsp;&amp;nbsp;- cpu_mem_addr[31:0] (Address)&lt;br&gt;&amp;nbsp;&amp;nbsp;- cpu_mem_wdata[31:0] / wstrb[3:0]&lt;br&gt;&amp;nbsp;&amp;nbsp;- cpu_mem_rdata[31:0] (Read Data)&lt;br&gt;&amp;nbsp;&amp;nbsp;- cpu_mem_ready (Ack / Handshake)&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dbeafe;strokeColor=#2563eb;strokeWidth=2.5;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=12;" vertex="1" parent="1">
          <mxGeometry x="40" y="110" width="310" height="420" as="geometry" />
        </mxCell>

        <!-- CENTRAL INTERCONNECT CARD -->
        <mxCell id="interconnect" value="&lt;b style=&quot;font-size:19px;color:#7c2d12;&quot;&gt;soc_interconnect.v&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:13.5px;color:#ea580c;&quot;&gt;&lt;b&gt;Bộ giải mã địa chỉ &amp;amp; Ghép kênh tín hiệu Bus (Interconnect)&lt;/b&gt;&lt;/span&gt;&lt;br&gt;&lt;hr style=&quot;border:1px solid #fdba74;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:12px;color:#431407;line-height:1.5;&quot;&gt;&lt;b&gt;1. Address Range Decoding Logic:&lt;/b&gt;&lt;br&gt;&amp;nbsp;&amp;nbsp;• &lt;b&gt;sel_sram:&lt;/b&gt; valid &amp;amp;&amp;amp; (addr &amp;lt; 0x0000_0400)&lt;br&gt;&amp;nbsp;&amp;nbsp;• &lt;b&gt;sel_spimem:&lt;/b&gt; valid &amp;amp;&amp;amp; (0x0010_0000 &amp;lt;= addr &amp;lt; 0x0100_0000)&lt;br&gt;&amp;nbsp;&amp;nbsp;• &lt;b&gt;sel_spicfg:&lt;/b&gt; valid &amp;amp;&amp;amp; (addr == 0x0200_0000)&lt;br&gt;&amp;nbsp;&amp;nbsp;• &lt;b&gt;sel_rfid:&lt;/b&gt; valid &amp;amp;&amp;amp; (addr[31:28] == 4&#39;h1)&lt;br&gt;&amp;nbsp;&amp;nbsp;• &lt;b&gt;sel_uart:&lt;/b&gt; valid &amp;amp;&amp;amp; (addr[31:28] == 4&#39;h3)&lt;br&gt;&amp;nbsp;&amp;nbsp;• &lt;b&gt;sel_gpio:&lt;/b&gt; valid &amp;amp;&amp;amp; (addr[31:28] == 4&#39;h4)&lt;br&gt;&lt;br&gt;&lt;b&gt;2. Response Muxing (Return to CPU Master):&lt;/b&gt;&lt;br&gt;&amp;nbsp;&amp;nbsp;• cpu_mem_rdata = sel_sram ? sram_rdata :&lt;br&gt;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;sel_spimem ? spimem_rdata :&lt;br&gt;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;sel_spicfg ? spimem_cfg_do :&lt;br&gt;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;sel_rfid ? rfid_rdata : ...&lt;br&gt;&amp;nbsp;&amp;nbsp;• cpu_mem_ready = sram_ready | spimem_ready |&lt;br&gt;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;sel_spicfg | rfid_ready | ...&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffedd5;strokeColor=#ea580c;strokeWidth=2.5;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=12;" vertex="1" parent="1">
          <mxGeometry x="420" y="110" width="370" height="420" as="geometry" />
        </mxCell>

        <!-- Bus CPU -> Interconnect -->
        <mxCell id="bus_cpu_ic" value="PicoRV32 Native Bus&lt;br&gt;[valid, addr, wdata, wstrb]&lt;br&gt;&amp;lt;==== [rdata, ready] ====" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#2563eb;fontSize=12;fontStyle=1;endArrow=block;endFill=1;startArrow=block;startFill=1;" edge="1" parent="1" source="cpu_master" target="interconnect">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- SLAVE 0: 1KB SRAM -->
        <mxCell id="slv_sram" value="&lt;b style=&quot;font-size:15px;color:#065f46;&quot;&gt;SLAVE 0: 1KB Data SRAM&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:12px;color:#059669;&quot;&gt;&lt;b&gt;data_sram.v (0x0000_0000 - 0x0000_03FF)&lt;/b&gt;&lt;/span&gt;&lt;br&gt;&lt;span style=&quot;font-size:11.5px;color:#064e3b;&quot;&gt;• Stack frame C (sp = 0x0400), biến cục bộ, .bss, .data&lt;br&gt;• 1 chu kỳ phản hồi (sram_ready = 1) - Tốc độ cao&lt;br&gt;• Nạp và thực thi mã động flashio_worker&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d1fae5;strokeColor=#10b981;strokeWidth=2;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=8;" vertex="1" parent="1">
          <mxGeometry x="870" y="110" width="350" height="85" as="geometry" />
        </mxCell>

        <!-- SLAVE 1: SPI FLASH XIP -->
        <mxCell id="slv_spimem" value="&lt;b style=&quot;font-size:15px;color:#1e40af;&quot;&gt;SLAVE 1 &amp;amp; 1b: SPI Flash XIP &amp;amp; Config&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:12px;color:#2563eb;&quot;&gt;&lt;b&gt;spimemio.v (0x0010_0000 - 0x00FF_FFFF &amp;amp; 0x0200_0000)&lt;/b&gt;&lt;/span&gt;&lt;br&gt;&lt;span style=&quot;font-size:11.5px;color:#1e3a8a;&quot;&gt;• XIP Code (.text): 0x0025_0000 (Vector khởi động Boot)&lt;br&gt;• Flash DB Thẻ: Sector 48 (0x0030_0000, 64KB)&lt;br&gt;• Flash Audit Log: Sector 49 (0x0031_0000, 64KB)&lt;br&gt;• SPICFG (0x0200_0000): Bit-bang điều khiển nạp/xóa Flash&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e0e7ff;strokeColor=#4f46e5;strokeWidth=2;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=8;" vertex="1" parent="1">
          <mxGeometry x="870" y="210" width="350" height="105" as="geometry" />
        </mxCell>

        <!-- EXTERNAL SPI FLASH CHIP -->
        <mxCell id="ext_flash" value="&lt;b style=&quot;font-size:14px;color:#701a75;&quot;&gt;External SPI Flash&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:11.5px;color:#86198f;&quot;&gt;32Mbit / 4MB SPI Flash&lt;br&gt;W25Q32JV / S25FL032P&lt;br&gt;&lt;b&gt;[CSB, CLK, IO0, IO1]&lt;/b&gt;&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fae8ff;strokeColor=#c026d3;strokeWidth=2;fontFamily=Segoe UI;shadow=1;" vertex="1" parent="1">
          <mxGeometry x="1270" y="215" width="240" height="95" as="geometry" />
        </mxCell>

        <!-- SLAVE 2: RFID UART -->
        <mxCell id="slv_rfid" value="&lt;b style=&quot;font-size:14px;color:#92400e;&quot;&gt;SLAVE 2: RFID UART Controller&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:11.5px;color:#78350f;&quot;&gt;&lt;b&gt;0x1000_0000 (DIV) | 0x1000_0004 (DAT)&lt;/b&gt;&lt;br&gt;Tích hợp 32-Byte RX FIFO, tự đệm frame thẻ RDM6300 (9600 baud)&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fef3c7;strokeColor=#f59e0b;strokeWidth=2;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=6;" vertex="1" parent="1">
          <mxGeometry x="870" y="330" width="350" height="60" as="geometry" />
        </mxCell>

        <!-- SLAVE 3: HOST PC UART -->
        <mxCell id="slv_host" value="&lt;b style=&quot;font-size:14px;color:#0e7490;&quot;&gt;SLAVE 3: Host PC UART Controller&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:11.5px;color:#155e75;&quot;&gt;&lt;b&gt;0x3000_0000 (DIV) | 0x3000_0004 (DAT)&lt;/b&gt;&lt;br&gt;Tích hợp 32-Byte RX FIFO &amp;amp; 32-Byte TX FIFO kết nối PC Terminal&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#cffafe;strokeColor=#06b6d4;strokeWidth=2;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=6;" vertex="1" parent="1">
          <mxGeometry x="870" y="405" width="350" height="60" as="geometry" />
        </mxCell>

        <!-- SLAVE 4: GPIO LEDS -->
        <mxCell id="slv_gpio" value="&lt;b style=&quot;font-size:14px;color:#374151;&quot;&gt;SLAVE 4: GPIO Status LEDs&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:11.5px;color:#1f2937;&quot;&gt;&lt;b&gt;0x4000_0000 (LEDs)&lt;/b&gt; - Bit 0: Alive, Bit 1: Warn, Bit 2: Granted, Bit 3: Flash&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f3f4f6;strokeColor=#4b5563;strokeWidth=2;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=6;" vertex="1" parent="1">
          <mxGeometry x="870" y="480" width="350" height="50" as="geometry" />
        </mxCell>

        <!-- External Modules -->
        <mxCell id="ext_rdm" value="&lt;b&gt;RDM6300 RFID&lt;/b&gt;&lt;br&gt;125 kHz UART" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fffbeb;strokeColor=#d97706;strokeWidth=2;fontFamily=Segoe UI;" vertex="1" parent="1">
          <mxGeometry x="1270" y="335" width="240" height="50" as="geometry" />
        </mxCell>

        <mxCell id="ext_pc" value="&lt;b&gt;Host PC Terminal&lt;/b&gt;&lt;br&gt;USB-UART Bridge" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ecfeff;strokeColor=#0891b2;strokeWidth=2;fontFamily=Segoe UI;" vertex="1" parent="1">
          <mxGeometry x="1270" y="410" width="240" height="50" as="geometry" />
        </mxCell>

        <mxCell id="ext_leds" value="&lt;b&gt;16x LEDs / Relay&lt;/b&gt;&lt;br&gt;Basys 3 Diagnostic" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f1f5f9;strokeColor=#64748b;strokeWidth=2;fontFamily=Segoe UI;" vertex="1" parent="1">
          <mxGeometry x="1270" y="480" width="240" height="50" as="geometry" />
        </mxCell>

        <!-- Wires from Interconnect to Slaves -->
        <mxCell id="w_sram" value="sel_sram" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#10b981;fontSize=11;fontStyle=1;endArrow=block;" edge="1" parent="1" source="interconnect" target="slv_sram">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="w_spimem" value="sel_spimem / sel_spicfg" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#4f46e5;fontSize=11;fontStyle=1;endArrow=block;" edge="1" parent="1" source="interconnect" target="slv_spimem">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="w_rfid" value="sel_rfid" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#f59e0b;fontSize=11;fontStyle=1;endArrow=block;" edge="1" parent="1" source="interconnect" target="slv_rfid">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="w_uart" value="sel_uart" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#06b6d4;fontSize=11;fontStyle=1;endArrow=block;" edge="1" parent="1" source="interconnect" target="slv_host">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="w_gpio" value="sel_gpio" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#4b5563;fontSize=11;fontStyle=1;endArrow=block;" edge="1" parent="1" source="interconnect" target="slv_gpio">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <mxCell id="w_spi_ext" value="SPI Bus" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#c026d3;fontSize=11;fontStyle=1;endArrow=block;startArrow=block;" edge="1" parent="1" source="slv_spimem" target="ext_flash">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="w_rfid_ext" value="RX Data" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#d97706;fontSize=11;fontStyle=1;endArrow=block;" edge="1" parent="1" source="ext_rdm" target="slv_rfid">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="w_pc_ext" value="TX / RX" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#0891b2;fontSize=11;fontStyle=1;endArrow=block;startArrow=block;" edge="1" parent="1" source="slv_host" target="ext_pc">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="w_led_ext" value="Output" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#64748b;fontSize=11;fontStyle=1;endArrow=block;" edge="1" parent="1" source="slv_gpio" target="ext_leds">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- 4 PHASES FIRMWARE EXECUTION WORKFLOW CARDS AT BOTTOM -->
        <mxCell id="wf_box" value="&lt;b style=&quot;font-size:16px;color:#0f172a;&quot;&gt;CƠ CHẾ KÍCH HOẠT VÀ ĐIỀU PHỐI THỰC THI FIRMWARE C TRÊN PHẦN CỨNG&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f1f5f9;strokeColor=#94a3b8;strokeWidth=2;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=8;" vertex="1" parent="1">
          <mxGeometry x="40" y="555" width="1480" height="240" as="geometry" />
        </mxCell>

        <mxCell id="p1" value="&lt;b style=&quot;font-size:14px;color:#1d4ed8;&quot;&gt;① Boot XIP từ SPI Flash&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:11.5px;color:#1e3a8a;line-height:1.4;&quot;&gt;Khi reset hạ thấp, PicoRV32 nhảy tới vector &lt;b&gt;0x0025_0000&lt;/b&gt;. &lt;i&gt;soc_interconnect&lt;/i&gt; kích hoạt &lt;b&gt;sel_spimem&lt;/b&gt;. &lt;i&gt;spimemio&lt;/i&gt; tự động phát lệnh đọc SPI 0x03, kéo từng từ lệnh 32-bit từ Flash vào CPU không cần bootloader trung gian.&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3b82f6;strokeWidth=2;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=8;" vertex="1" parent="1">
          <mxGeometry x="60" y="595" width="340" height="180" as="geometry" />
        </mxCell>

        <mxCell id="p2" value="&lt;b style=&quot;font-size:14px;color:#047857;&quot;&gt;② Khởi tạo Stack &amp;amp; C Data trên SRAM&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:11.5px;color:#064e3b;line-height:1.4;&quot;&gt;Mã khởi động &lt;i&gt;start.s&lt;/i&gt; gán con trỏ ngăn xếp &lt;b&gt;sp = 0x0000_0400&lt;/b&gt; (đỉnh 1KB SRAM). Khi code C gọi hàm, tạo biến cục bộ, con trỏ Stack hit dải địa chỉ &amp;lt; 0x0400. &lt;i&gt;soc_interconnect&lt;/i&gt; bật &lt;b&gt;sel_sram&lt;/b&gt; cho phép đọc/ghi tức thì trong &lt;b&gt;1 chu kỳ xung nhịp&lt;/b&gt;.&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#10b981;strokeWidth=2;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=8;" vertex="1" parent="1">
          <mxGeometry x="430" y="595" width="340" height="180" as="geometry" />
        </mxCell>

        <mxCell id="p3" value="&lt;b style=&quot;font-size:14px;color:#b45309;&quot;&gt;③ Điều khiển ngoại vi MMIO qua C&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:11.5px;color:#78350f;line-height:1.4;&quot;&gt;Code C truy xuất phần cứng bằng macro biến volatile: &lt;b&gt;REG_RFID_UART_DAT (0x1000_0004)&lt;/b&gt;, &lt;b&gt;REG_PC_UART_DAT (0x3000_0004)&lt;/b&gt;, &lt;b&gt;REG_GPIO_LEDS (0x4000_0000)&lt;/b&gt;. Bus Interconnect tự động giải mã prefix 0x1, 0x3, 0x4 kích hoạt FIFO UART &amp;amp; LED tương ứng.&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#f59e0b;strokeWidth=2;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=8;" vertex="1" parent="1">
          <mxGeometry x="800" y="595" width="340" height="180" as="geometry" />
        </mxCell>

        <mxCell id="p4" value="&lt;b style=&quot;font-size:14px;color:#7c3aed;&quot;&gt;④ Nạp mã RAM ghi Flash không gián đoạn&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:11.5px;color:#4c1d95;line-height:1.4;&quot;&gt;Flash không thể vừa đọc lệnh XIP vừa ghi Sector mới. Trình điều khiển &lt;i&gt;flash.c&lt;/i&gt; copy routine nhị phân &lt;b&gt;flashio_worker&lt;/b&gt; lên ngăn xếp SRAM, CPU nhảy lên SRAM thực thi và điều khiển địa chỉ &lt;b&gt;0x0200_0000 (sel_spicfg)&lt;/b&gt; để xóa/ghi thẻ an toàn tuyệt đối.&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#8b5cf6;strokeWidth=2;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=8;" vertex="1" parent="1">
          <mxGeometry x="1170" y="595" width="330" height="180" as="geometry" />
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
    return xml_content

def create_html_render():
    html_content = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background-color: #ffffff;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    padding: 24px;
    width: 1560px;
    height: 1040px;
    position: relative;
    overflow: hidden;
  }
  .diagram-container {
    width: 1512px;
    height: 992px;
    border: 2.5px solid #0f172a;
    border-radius: 12px;
    background: #ffffff;
    position: relative;
    padding: 16px 20px;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08);
  }
  .title-banner {
    text-align: center;
    border-bottom: 2px solid #cbd5e1;
    padding-bottom: 10px;
    margin-bottom: 18px;
  }
  .title-banner h1 {
    font-size: 23px;
    font-weight: 900;
    color: #0f172a;
    letter-spacing: 0.5px;
    text-transform: uppercase;
  }
  .title-banner p {
    font-size: 14.5px;
    font-weight: 700;
    color: #475569;
    margin-top: 3px;
  }
  .card {
    position: absolute;
    border-radius: 10px;
    border: 2px solid;
    padding: 12px 14px;
    box-shadow: 0 3px 8px rgba(0,0,0,0.06);
    background: #ffffff;
  }
  .card-title {
    font-size: 16.5px;
    font-weight: 800;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .card-subtitle {
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 6px;
  }
  .badge {
    font-size: 11px;
    font-weight: 800;
    padding: 2px 7px;
    border-radius: 4px;
    text-transform: uppercase;
  }

  /* CPU Master */
  .card-cpu {
    left: 20px;
    top: 75px;
    width: 330px;
    height: 480px;
    border-color: #2563eb;
    background: #f8faff;
  }
  .card-cpu .card-title { color: #1e3a8a; }
  .card-cpu .card-subtitle { color: #2563eb; }

  /* Interconnect */
  .card-ic {
    left: 380px;
    top: 75px;
    width: 440px;
    height: 480px;
    border-color: #ea580c;
    background: #fffaf5;
  }
  .card-ic .card-title { color: #9a3412; }
  .card-ic .card-subtitle { color: #ea580c; }

  /* Slaves */
  .card-sram {
    left: 850px;
    top: 75px;
    width: 370px;
    height: 90px;
    border-color: #10b981;
    background: #f0fdf4;
  }
  .card-spimem {
    left: 850px;
    top: 175px;
    width: 370px;
    height: 125px;
    border-color: #4f46e5;
    background: #f5f3ff;
  }
  .card-rfid {
    left: 850px;
    top: 310px;
    width: 370px;
    height: 75px;
    border-color: #f59e0b;
    background: #fffbeb;
  }
  .card-host {
    left: 850px;
    top: 395px;
    width: 370px;
    height: 75px;
    border-color: #06b6d4;
    background: #ecfeff;
  }
  .card-gpio {
    left: 850px;
    top: 480px;
    width: 370px;
    height: 75px;
    border-color: #64748b;
    background: #f8fafc;
  }

  /* External peripherals */
  .card-ext-flash {
    left: 1245px;
    top: 180px;
    width: 245px;
    height: 115px;
    border-color: #c026d3;
    background: #fdf4ff;
  }
  .card-ext-rdm {
    left: 1245px;
    top: 315px;
    width: 245px;
    height: 65px;
    border-color: #d97706;
    background: #fffbeb;
  }
  .card-ext-pc {
    left: 1245px;
    top: 400px;
    width: 245px;
    height: 65px;
    border-color: #0891b2;
    background: #f0fdfa;
  }
  .card-ext-led {
    left: 1245px;
    top: 485px;
    width: 245px;
    height: 65px;
    border-color: #475569;
    background: #f1f5f9;
  }

  /* Bottom Container */
  .bottom-box {
    position: absolute;
    left: 20px;
    top: 575px;
    width: 1470px;
    height: 395px;
    border: 2px solid #cbd5e1;
    border-radius: 10px;
    background: #f8fafc;
    padding: 12px 18px;
  }
  .bottom-header {
    font-size: 15.5px;
    font-weight: 800;
    color: #0f172a;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .workflow-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
  }
  .wf-step {
    background: #ffffff;
    border-radius: 8px;
    border: 1.5px solid;
    padding: 12px 14px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.04);
  }
  .wf-title {
    font-size: 14.5px;
    font-weight: 800;
    margin-bottom: 6px;
  }
  .wf-desc {
    font-size: 12px;
    color: #334155;
    line-height: 1.5;
  }
  .code-inline {
    font-family: Consolas, monospace;
    font-size: 11px;
    background: #f1f5f9;
    padding: 1px 4px;
    border-radius: 3px;
    color: #0f172a;
    font-weight: 600;
  }
</style>
</head>
<body>
<div class="diagram-container">
  <!-- Title -->
  <div class="title-banner">
    <h1>Kiến Trúc Bus soc_interconnect.v &amp; Cơ Chế Thực Thi Bare-Metal C</h1>
    <p>Giải mã không gian địa chỉ, điều phối bộ nhớ Flash XIP / 1KB SRAM và cầu nối ngoại vi MMIO cho CPU PicoRV32</p>
  </div>

  <!-- CPU Master -->
  <div class="card card-cpu">
    <div class="card-title">
      <span>CPU Master: PicoRV32</span>
      <span class="badge" style="background:#dbeafe;color:#1e40af;">RV32IMC</span>
    </div>
    <div class="card-subtitle">Nhân RISC-V 32-bit thực thi trực tiếp</div>
    <div style="font-size:12px;color:#334155;line-height:1.6;margin-top:8px;">
      <div><b>• PROGADDR_RESET:</b> <span class="code-inline">0x0025_0000</span> (Flash XIP)</div>
      <div><b>• Stack Pointer (sp):</b> <span class="code-inline">0x0000_0400</span> (Đỉnh SRAM)</div>
      <div style="margin-top:10px;padding:8px;background:#eff6ff;border-radius:6px;border:1px dashed #93c5fd;">
        <b>Tín hiệu Bus Native PicoRV32:</b><br>
        <span style="color:#2563eb;"><b>&gt; cpu_mem_valid:</b> Kích hoạt chu kỳ bus (1 bit)</span><br>
        <span style="color:#2563eb;"><b>&gt; cpu_mem_addr[31:0]:</b> Địa chỉ bộ nhớ truy cập</span><br>
        <span style="color:#2563eb;"><b>&gt; cpu_mem_wdata[31:0]:</b> Dữ liệu ghi ra từ CPU</span><br>
        <span style="color:#2563eb;"><b>&gt; cpu_mem_wstrb[3:0]:</b> Mặt nạ ghi từng byte</span><br>
        <span style="color:#059669;"><b>&lt; cpu_mem_rdata[31:0]:</b> Dữ liệu đọc trả về CPU</span><br>
        <span style="color:#059669;"><b>&lt; cpu_mem_ready:</b> Tín hiệu báo hoàn tất chu kỳ</span>
      </div>
      <div style="margin-top:10px;font-size:11.5px;color:#475569;">
        CPU tự động dừng (stall) cho đến khi ngoại vi hoặc bộ nhớ kéo <b>cpu_mem_ready = 1</b>.
      </div>
    </div>
  </div>

  <!-- Interconnect -->
  <div class="card card-ic">
    <div class="card-title">
      <span>soc_interconnect.v</span>
      <span class="badge" style="background:#ffedd5;color:#c2410c;">Central Bus</span>
    </div>
    <div class="card-subtitle">Bộ giải mã địa chỉ &amp; Ghép kênh tín hiệu trả về</div>
    <div style="font-size:12px;color:#334155;line-height:1.55;margin-top:6px;">
      <b>1. Logic giải mã địa chỉ (Range &amp; Prefix Decoding):</b>
      <div style="background:#fff7ed;padding:6px 8px;border-radius:6px;border:1px solid #fed7aa;margin:4px 0;font-family:Consolas,monospace;font-size:11px;">
        sel_sram   = cpu_mem_valid &amp;&amp; (addr &lt; 32'h0000_0400);<br>
        sel_spimem = cpu_mem_valid &amp;&amp; (addr &gt;= 0x0010_0000 &amp;&amp; addr &lt; 0x0100_0000);<br>
        sel_spicfg = cpu_mem_valid &amp;&amp; (addr == 32'h0200_0000);<br>
        sel_rfid   = cpu_mem_valid &amp;&amp; (addr[31:28] == 4'h1);<br>
        sel_uart   = cpu_mem_valid &amp;&amp; (addr[31:28] == 4'h3);<br>
        sel_gpio   = cpu_mem_valid &amp;&amp; (addr[31:28] == 4'h4);
      </div>
      <b>2. Bộ ghép kênh dữ liệu đọc (cpu_mem_rdata Mux):</b>
      <div style="background:#fff7ed;padding:6px 8px;border-radius:6px;border:1px solid #fed7aa;margin:4px 0;font-family:Consolas,monospace;font-size:11px;">
        cpu_mem_rdata = sel_sram   ? sram_rdata    :<br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sel_spimem ? spimem_rdata  :<br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sel_spicfg ? spimem_cfg_do :<br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sel_rfid   ? rfid_rdata    :<br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sel_uart   ? uart_rdata    :<br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sel_gpio   ? gpio_rdata    : 32'd0;
      </div>
      <b>3. Bộ tổng hợp tín hiệu sẵn sàng (cpu_mem_ready OR):</b>
      <div style="background:#fff7ed;padding:4px 8px;border-radius:6px;border:1px solid #fed7aa;margin:4px 0;font-family:Consolas,monospace;font-size:11px;">
        cpu_mem_ready = sram_ready | spimem_ready | sel_spicfg | rfid_ready | uart_ready | gpio_ready;
      </div>
    </div>
  </div>

  <!-- Slaves -->
  <!-- Slave 0: SRAM -->
  <div class="card card-sram">
    <div class="card-title">
      <span style="color:#065f46;font-size:14.5px;">Slave 0: 1KB Data SRAM (data_sram.v)</span>
      <span class="badge" style="background:#d1fae5;color:#047857;">1 Cycle Latency</span>
    </div>
    <div style="font-size:11.5px;color:#064e3b;line-height:1.4;">
      <b>Dải địa chỉ:</b> <span class="code-inline">0x0000_0000 - 0x0000_03FF</span><br>
      • Chứa Stack frames C, biến cục bộ, mảng dữ liệu tạm thời, .bss, .data.<br>
      • Tốc độ 1 chu kỳ xung nhịp (<span class="code-inline">sram_ready = 1</span>), chạy buffer <span class="code-inline">flashio_worker</span>.
    </div>
  </div>

  <!-- Slave 1: SPI Flash -->
  <div class="card card-spimem">
    <div class="card-title">
      <span style="color:#1e40af;font-size:14.5px;">Slave 1 &amp; 1b: SPI Flash XIP &amp; Config (spimemio.v)</span>
      <span class="badge" style="background:#e0e7ff;color:#3730a3;">XIP SPI Bus</span>
    </div>
    <div style="font-size:11px;color:#1e3a8a;line-height:1.4;">
      <b>Dải địa chỉ:</b> <span class="code-inline">0x0010_0000 - 0x00FF_FFFF</span> &amp; <span class="code-inline">0x0200_0000 (CFG)</span><br>
      • <b>XIP Firmware (.text):</b> Bắt đầu tại <span class="code-inline">0x0025_0000</span> (Vector Reset Boot).<br>
      • <b>Whitelist DB:</b> Sector 48 (<span class="code-inline">0x0030_0000</span>, 64KB, tối đa 4096 thẻ).<br>
      • <b>Access Logs:</b> Sector 49 (<span class="code-inline">0x0031_0000</span>, 64KB, 512 bản ghi vào ra).<br>
      • <b>SPICFG (0x0200_0000):</b> Thanh ghi cấu hình bitbang ghi/xóa Flash từ SRAM.
    </div>
  </div>

  <!-- Slave 2: RFID UART -->
  <div class="card card-rfid">
    <div class="card-title">
      <span style="color:#92400e;font-size:14px;">Slave 2: RDM6300 RFID UART Peripheral</span>
      <span class="badge" style="background:#fef3c7;color:#b45309;">FIFO 32B</span>
    </div>
    <div style="font-size:11px;color:#78350f;line-height:1.4;">
      <b>Địa chỉ:</b> <span class="code-inline">0x1000_0000 (DIV)</span> | <span class="code-inline">0x1000_0004 (DAT)</span><br>
      Baud divider = 5208 (9600 baud @ 50MHz). Đọc DAT lấy byte từ RX FIFO. Trả về <span class="code-inline">0xFFFFFFFF</span> nếu rỗng.
    </div>
  </div>

  <!-- Slave 3: Host UART -->
  <div class="card card-host">
    <div class="card-title">
      <span style="color:#0e7490;font-size:14px;">Slave 3: Host PC UART Peripheral</span>
      <span class="badge" style="background:#cffafe;color:#0891b2;">Dual FIFO 32B</span>
    </div>
    <div style="font-size:11px;color:#155e75;line-height:1.4;">
      <b>Địa chỉ:</b> <span class="code-inline">0x3000_0000 (DIV)</span> | <span class="code-inline">0x3000_0004 (DAT)</span><br>
      Giao tiếp 2 chiều với PC Terminal. Ghi DAT nạp vào TX FIFO, đọc DAT lấy byte từ RX FIFO.
    </div>
  </div>

  <!-- Slave 4: GPIO LEDs -->
  <div class="card card-gpio">
    <div class="card-title">
      <span style="color:#374151;font-size:14px;">Slave 4: GPIO Status LEDs</span>
      <span class="badge" style="background:#f1f5f9;color:#334155;">MMIO Output</span>
    </div>
    <div style="font-size:11px;color:#1f2937;line-height:1.4;">
      <b>Địa chỉ:</b> <span class="code-inline">0x4000_0000 (REG_GPIO_LEDS)</span><br>
      Bit 0: Alive Heartbeat | Bit 1: Access Denied / Warn | Bit 2: Access Granted | Bit 3: Flash Active.
    </div>
  </div>

  <!-- External Devices -->
  <div class="card card-ext-flash">
    <div class="card-title" style="color:#86198f;font-size:13.5px;">External SPI Flash</div>
    <div style="font-size:11px;color:#701a75;line-height:1.4;">
      <b>32Mbit SPI Flash Chip</b><br>
      W25Q32JV / S25FL032P<br>
      Tín hiệu 4 chân SPI:<br>
      <span class="code-inline">CSB, CLK, IO0/MOSI, IO1/MISO</span>
    </div>
  </div>

  <div class="card card-ext-rdm">
    <div class="card-title" style="color:#b45309;font-size:13px;">RDM6300 RFID Module</div>
    <div style="font-size:10.5px;color:#78350f;">
      Đầu đọc thẻ 125 kHz EM4100<br>
      Bắn luồng UART 9600-8-N-1 vào chân RX
    </div>
  </div>

  <div class="card card-ext-pc">
    <div class="card-title" style="color:#0891b2;font-size:13px;">Host PC Console</div>
    <div style="font-size:10.5px;color:#155e75;">
      Phần mềm điều khiển Python / C<br>
      Giao tiếp qua USB-UART Bridge FTDI
    </div>
  </div>

  <div class="card card-ext-led">
    <div class="card-title" style="color:#334155;font-size:13px;">Bo mạch Basys 3 / Relays</div>
    <div style="font-size:10.5px;color:#475569;">
      16 LED hiển thị trạng thái phần cứng<br>
      Chốt Relay kích hoạt cửa ra vào
    </div>
  </div>

  <!-- Bottom Workflow -->
  <div class="bottom-box">
    <div class="bottom-header">
      <span style="background:#0f172a;color:#ffffff;padding:2px 8px;border-radius:4px;font-size:12px;">4 BƯỚC</span>
      <span>CƠ CHẾ KÍCH HOẠT VÀ ĐIỀU PHỐI THỰC THI FIRMWARE C TRÊN PHẦN CỨNG</span>
    </div>
    <div class="workflow-grid">
      <!-- Step 1 -->
      <div class="wf-step" style="border-color:#3b82f6;">
        <div class="wf-title" style="color:#1d4ed8;">① Boot XIP Trực Tiếp từ Flash</div>
        <div class="wf-desc">
          Khi reset nhả về 0, CPU PicoRV32 nhảy tới vector <span class="code-inline">0x0025_0000</span>. Bộ giải mã <span class="code-inline">soc_interconnect</span> kích hoạt <span class="code-inline">sel_spimem</span>.<br>
          Bộ điều khiển <span class="code-inline">spimemio</span> tự động phát lệnh đọc 0x03, kéo từng từ lệnh 32-bit từ Flash vào CPU mà không cần nạp vào RAM trước.
        </div>
      </div>
      <!-- Step 2 -->
      <div class="wf-step" style="border-color:#10b981;">
        <div class="wf-title" style="color:#047857;">② Khởi Tạo Stack C trên 1KB SRAM</div>
        <div class="wf-desc">
          File khởi động <span class="code-inline">start.s</span> gán con trỏ <span class="code-inline">sp = 0x0000_0400</span> (đỉnh SRAM nội).<br>
          Khi code C gọi hàm hoặc cấp phát biến cục bộ, CPU truy xuất vùng &lt; 0x0400. <span class="code-inline">soc_interconnect</span> kích hoạt <span class="code-inline">sel_sram</span> phản hồi tức thì trong <b>1 chu kỳ</b> (<span class="code-inline">sram_ready = 1</span>), tránh nghẽn bus SPI.
        </div>
      </div>
      <!-- Step 3 -->
      <div class="wf-step" style="border-color:#f59e0b;">
        <div class="wf-title" style="color:#b45309;">③ Điều Khiển Ngoại Vi Bằng MMIO</div>
        <div class="wf-desc">
          Firmware C thao tác với ngoại vi qua con trỏ volatile trong file <span class="code-inline">soc_regs.h</span>.<br>
          Khi C đọc <span class="code-inline">REG_RFID_UART_DAT</span>, CPU truy cập địa chỉ <span class="code-inline">0x1000_0004</span>. Interconnect giải mã tiền tố <span class="code-inline">0x1</span> bật <span class="code-inline">sel_rfid</span>, lấy byte từ FIFO 32B nhanh chóng mà không làm mất frame thẻ.
        </div>
      </div>
      <!-- Step 4 -->
      <div class="wf-step" style="border-color:#8b5cf6;">
        <div class="wf-title" style="color:#7c3aed;">④ Chạy Mã RAM Ghi Flash An Toàn</div>
        <div class="wf-desc">
          Bộ nhớ SPI Flash không thể vừa đọc lệnh XIP vừa ghi xóa Sector. Khi cần ghi thẻ mới hoặc lưu log, hàm <span class="code-inline">flashio</span> copy đoạn mã nhỏ <span class="code-inline">flashio_worker</span> lên Stack SRAM.<br>
          CPU nhảy lên SRAM thực thi, truy cập <span class="code-inline">0x0200_0000 (sel_spicfg)</span> điều khiển SPI bit-bang an toàn 100%.
        </div>
      </div>
    </div>
  </div>

</div>
</body>
</html>
"""
    return html_content

def main():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    doc_dir = os.path.dirname(cur_dir) if os.path.basename(cur_dir) == "temp" else cur_dir

    drawio_file = os.path.join(cur_dir, "fig2_soc_interconnect.drawio")
    html_file = os.path.join(cur_dir, "fig2_soc_interconnect.html")
    png_file = os.path.join(cur_dir, "fig2_soc_interconnect.png")
    doc_png = os.path.join(doc_dir, "fig2_soc_interconnect.png")

    # 1. Write Draw.io XML
    with open(drawio_file, "w", encoding="utf-8") as f:
        f.write(create_drawio_xml())
    print("Saved Draw.io file:", drawio_file)

    # 2. Write HTML render template
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(create_html_render())
    print("Saved HTML file:", html_file)

    # 3. Render PNG using Headless Chrome at 2x DPI
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if os.path.exists(chrome_path):
        cmd = [
            chrome_path,
            "--headless=new",
            "--disable-gpu",
            "--force-device-scale-factor=2",
            f"--screenshot={png_file}",
            "--window-size=1560,1040",
            f"file:///{os.path.abspath(html_file).replace(os.sep, '/')}"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        print("Chrome render status code:", res.returncode)
        if os.path.exists(png_file):
            print(f"Generated PNG: {png_file} ({os.path.getsize(png_file)} bytes)")
            shutil.copy2(png_file, doc_png)
            print(f"Copied to doc root: {doc_png}")
        else:
            print("Error: PNG not created by Chrome!")
    else:
        print("Chrome not found at standard path:", chrome_path)

if __name__ == "__main__":
    main()
