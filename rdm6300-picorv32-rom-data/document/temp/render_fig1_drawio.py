# -*- coding: utf-8 -*-
"""
Script: render_fig1_drawio.py
Generates both:
1. fig1_block_diagram.drawio: Genuine editable Draw.io XML file (app.diagrams.net compatible).
2. fig1_block_diagram.png: Ultra-sharp Draw.io-style vector render via Headless Chrome at 2x DPI.
   Features:
   - Authentic Draw.io aesthetic (clean rounded cards, color-coded functional domains,
     crisp drop shadows, Segoe UI typography).
   - ENLARGED, BOLD FONTS (15px to 26px), ensuring maximum legibility inside Word reports.
   - Generous clearances ensuring ZERO badge, wire, or card intersections!
"""

import os
import subprocess

def create_drawio_xml():
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="2026-09-28T04:45:00.000Z" agent="Mozilla/5.0" version="21.0.0" type="device">
  <diagram id="soc_diagram" name="PicoRV32 Hardware Architecture">
    <mxGraphModel dx="1600" dy="1100" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1560" pageHeight="1060" math="0" shadow="1">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- 1. POWER INPUT -->
        <mxCell id="pwr_in" value="&lt;b style=&quot;font-size:18px;&quot;&gt;POWER INPUT&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:14px;&quot;&gt;USB +5V DC @ 500mA&lt;br&gt;External Adapter / VBUS&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;strokeWidth=2.5;fontFamily=Segoe UI;shadow=1;" vertex="1" parent="1">
          <mxGeometry x="50" y="45" width="260" height="100" as="geometry" />
        </mxCell>

        <!-- 2. REGULATORS -->
        <mxCell id="reg" value="&lt;b style=&quot;font-size:18px;&quot;&gt;VOLTAGE REGULATORS (LDO)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:14px;&quot;&gt;3.3V LDO: I/O, Flash &amp;amp; RFID (VDD33)&lt;br&gt;1.8V LDO: ASIC Core Power (VDD18)&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;strokeWidth=2.5;fontFamily=Segoe UI;shadow=1;" vertex="1" parent="1">
          <mxGeometry x="420" y="45" width="330" height="100" as="geometry" />
        </mxCell>

        <!-- 3. CLOCK GENERATOR -->
        <mxCell id="clk_gen" value="&lt;b style=&quot;font-size:18px;&quot;&gt;CLOCK GENERATOR&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:14px;&quot;&gt;50 MHz Quartz Crystal Oscillator&lt;br&gt;Period = 20.0 ns (Master System Clock)&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;strokeWidth=2.5;fontFamily=Segoe UI;shadow=1;" vertex="1" parent="1">
          <mxGeometry x="830" y="45" width="310" height="100" as="geometry" />
        </mxCell>

        <!-- Wire Pwr -> Reg -->
        <mxCell id="w_pwr_reg" value="+5V DC" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2.5;strokeColor=#b85450;fontSize=14;fontStyle=1;endArrow=block;endFill=1;" edge="1" parent="1" source="pwr_in" target="reg">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- 4. CENTRAL SOC -->
        <mxCell id="soc" value="&lt;b style=&quot;font-size:24px;color:#1e3a8a;&quot;&gt;PicoRV32 RISC-V SoC&lt;/b&gt;&lt;br&gt;&lt;b style=&quot;font-size:16px;color:#3b82f6;font-family:Consolas;&quot;&gt;rdm6300_picorv32_soc&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:13.5px;color:#475569;&quot;&gt;SkyWater 130nm ASIC / Basys 3 FPGA Demo&lt;/span&gt;&lt;br&gt;&lt;br&gt;&lt;table style=&quot;width:100%;font-size:12.5px;border-collapse:collapse;color:#334155;&quot;&gt;&lt;tr&gt;&lt;td style=&quot;border:1px solid #cbd5e1;padding:5px;&quot;&gt;&lt;b&gt;CPU Core:&lt;/b&gt; PicoRV32 RV32I&lt;/td&gt;&lt;td style=&quot;border:1px solid #cbd5e1;padding:5px;&quot;&gt;&lt;b&gt;SRAM:&lt;/b&gt; 1KB Data Memory&lt;/td&gt;&lt;/tr&gt;&lt;tr&gt;&lt;td style=&quot;border:1px solid #cbd5e1;padding:5px;&quot;&gt;&lt;b&gt;Flash Ctrl:&lt;/b&gt; SPIMEMIO QSPI&lt;/td&gt;&lt;td style=&quot;border:1px solid #cbd5e1;padding:5px;&quot;&gt;&lt;b&gt;UARTs:&lt;/b&gt; Dual (Host &amp;amp; RFID)&lt;/td&gt;&lt;/tr&gt;&lt;tr&gt;&lt;td style=&quot;border:1px solid #cbd5e1;padding:5px;&quot;&gt;&lt;b&gt;HW Decoder:&lt;/b&gt; XOR Verifier&lt;/td&gt;&lt;td style=&quot;border:1px solid #cbd5e1;padding:5px;&quot;&gt;&lt;b&gt;GPIO:&lt;/b&gt; 16 Diagnostic LEDs&lt;/td&gt;&lt;/tr&gt;&lt;/table&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#2563eb;strokeWidth=3.5;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=16;" vertex="1" parent="1">
          <mxGeometry x="420" y="270" width="460" height="470" as="geometry" />
        </mxCell>

        <!-- Wire Reg -> SoC (VDD) -->
        <mxCell id="w_reg_soc" value="VDD (1.8V / 3.3V)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2.5;strokeColor=#b85450;fontSize=14;fontStyle=1;endArrow=block;endFill=1;entryX=0.25;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="reg" target="soc">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Wire Clk -> SoC (clk) -->
        <mxCell id="w_clk_soc" value="clk (50 MHz)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2.5;strokeColor=#475569;fontSize=14;fontStyle=1;endArrow=block;endFill=1;entryX=0.75;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="clk_gen" target="soc">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- 5. RFID READER -->
        <mxCell id="rfid" value="&lt;b style=&quot;font-size:19px;&quot;&gt;RFID READER&lt;/b&gt;&lt;br&gt;&lt;b style=&quot;font-size:15px;color:#d97706;&quot;&gt;RDM6300 (125 kHz PMOD)&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;span style=&quot;font-size:13.5px;&quot;&gt;• External Coil Antenna (125 kHz)&lt;br&gt;• EM4100 Compatible Passive Tag&lt;br&gt;• 14-Byte ASCII Frame Protocol&lt;br&gt;• Autonomous HW Verifier Engine&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fef3c7;strokeColor=#d97706;strokeWidth=2.5;fontFamily=Segoe UI;shadow=1;align=left;spacingLeft=16;" vertex="1" parent="1">
          <mxGeometry x="50" y="270" width="260" height="205" as="geometry" />
        </mxCell>

        <!-- Wire RFID -> SoC (rdm_rx) -->
        <mxCell id="w_rfid_soc" value="rdm_rx (9600 bps)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#d97706;fontSize=14;fontStyle=1;endArrow=block;endFill=1;entryX=0;entryY=0.25;entryDx=0;entryDy=0;" edge="1" parent="1" source="rfid" target="soc">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- 6. FIRMWARE PROGRAM -->
        <mxCell id="fw" value="&lt;b style=&quot;font-size:19px;&quot;&gt;ASM / C PROGRAM&lt;/b&gt;&lt;br&gt;&lt;b style=&quot;font-size:15px;color:#059669;&quot;&gt;RISC-V Firmware (GCC)&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;span style=&quot;font-size:13.5px;&quot;&gt;• Toolchain: riscv32-unknown-elf-gcc&lt;br&gt;• Source: start.s &amp;amp; firmware.c&lt;br&gt;• Compiled to firmware.hex (XIP)&lt;br&gt;• Reset Vector: 0x0025_0000&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d1fae5;strokeColor=#059669;strokeWidth=2.5;fontFamily=Segoe UI;shadow=1;align=left;spacingLeft=16;" vertex="1" parent="1">
          <mxGeometry x="50" y="525" width="260" height="215" as="geometry" />
        </mxCell>

        <!-- Wire FW -> SoC (boot_vec) -->
        <mxCell id="w_fw_soc" value="boot_vec (0x0025_0000)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#059669;fontSize=14;fontStyle=1;endArrow=block;endFill=1;entryX=0;entryY=0.75;entryDx=0;entryDy=0;" edge="1" parent="1" source="fw" target="soc">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- 7. SPI FLASH MEMORY -->
        <mxCell id="flash" value="&lt;b style=&quot;font-size:19px;&quot;&gt;SPI NOR FLASH MEMORY&lt;/b&gt;&lt;br&gt;&lt;b style=&quot;font-size:15px;color:#16a34a;&quot;&gt;Spansion S25FL032P (4 MB / 32 Mbit)&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;table style=&quot;width:100%;font-size:13px;border-collapse:collapse;&quot;&gt;&lt;tr&gt;&lt;td style=&quot;border:1.5px solid #bbf7d0;padding:5px;&quot;&gt;&lt;b&gt;Sec 0-36 (0x000000):&lt;/b&gt; FPGA Bitstream&lt;/td&gt;&lt;/tr&gt;&lt;tr&gt;&lt;td style=&quot;border:1.5px solid #bbf7d0;padding:5px;&quot;&gt;&lt;b&gt;Sec 37 (0x002500):&lt;/b&gt; Firmware (XIP)&lt;/td&gt;&lt;/tr&gt;&lt;tr&gt;&lt;td style=&quot;border:1.5px solid #bbf7d0;padding:5px;&quot;&gt;&lt;b&gt;Sec 48 (0x003000):&lt;/b&gt; Authorized Whitelist&lt;/td&gt;&lt;/tr&gt;&lt;tr&gt;&lt;td style=&quot;border:1.5px solid #bbf7d0;padding:5px;&quot;&gt;&lt;b&gt;Sec 49 (0x003100):&lt;/b&gt; Access Logs Database&lt;/td&gt;&lt;/tr&gt;&lt;/table&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#16a34a;strokeWidth=2.5;fontFamily=Segoe UI;shadow=1;align=left;spacingLeft=16;" vertex="1" parent="1">
          <mxGeometry x="1000" y="240" width="460" height="235" as="geometry" />
        </mxCell>

        <!-- Wire SoC -> Flash (SPI 4-wire) -->
        <mxCell id="w_soc_flash" value="SPI BUS (4-wire)&lt;br&gt;/CS, SCK, MOSI, MISO" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#16a34a;fontSize=14;fontStyle=1;endArrow=block;endFill=1;startArrow=block;startFill=1;exitX=1;exitY=0.25;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="soc" target="flash">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- 8. HOST PC CONSOLE -->
        <mxCell id="host_pc" value="&lt;b style=&quot;font-size:19px;&quot;&gt;HOST PC CONSOLE&lt;/b&gt;&lt;br&gt;&lt;b style=&quot;font-size:15px;color:#7c3aed;&quot;&gt;Win32 C Serial App (host/main.c)&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;span style=&quot;font-size:13.5px;&quot;&gt;• FTDI FT2232 USB-UART (9600 8-N-1)&lt;br&gt;• 13 Management Functions&lt;br&gt;• Whitelist Add/Delete &amp;amp; CSV Export/Import&lt;br&gt;• Live Event Log Monitoring&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ede9fe;strokeColor=#7c3aed;strokeWidth=2.5;fontFamily=Segoe UI;shadow=1;align=left;spacingLeft=16;" vertex="1" parent="1">
          <mxGeometry x="1000" y="500" width="460" height="205" as="geometry" />
        </mxCell>

        <!-- Wire SoC <-> Host PC -->
        <mxCell id="w_soc_pc" value="UART Bus (TXD / RXD)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#7c3aed;fontSize=14;fontStyle=1;endArrow=block;endFill=1;startArrow=block;startFill=1;exitX=1;exitY=0.75;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="soc" target="host_pc">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- 9. STATUS BUTTON -->
        <mxCell id="btn" value="&lt;b style=&quot;font-size:17px;&quot;&gt;STATUS BUTTON (RESET)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:13.5px;&quot;&gt;Manual Push Button (Active-Low)&lt;br&gt;Pin U18 (Basys 3) / ASIC rst_n&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe4e6;strokeColor=#f43f5e;strokeWidth=2.5;fontFamily=Segoe UI;shadow=1;" vertex="1" parent="1">
          <mxGeometry x="1040" y="740" width="340" height="110" as="geometry" />
        </mxCell>

        <!-- Wire Button -> SoC (rst_n) -->
        <mxCell id="w_btn_soc" value="rst_n" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2.5;strokeColor=#f43f5e;fontSize=14;fontStyle=1;endArrow=block;endFill=1;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.92;entryDx=0;entryDy=0;" edge="1" parent="1" source="btn" target="soc">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- 10. 16 DIAGNOSTIC LEDS -->
        <mxCell id="leds" value="&lt;b style=&quot;font-size:17px;&quot;&gt;16 DIAGNOSTIC LEDS (Basys 3 Prototyping Board)&lt;/b&gt;&lt;br&gt;&lt;table style=&quot;width:100%;font-size:13px;margin-top:6px;&quot;&gt;&lt;tr&gt;&lt;td&gt;&lt;b&gt;LED[0]:&lt;/b&gt; Heartbeat (1Hz)&lt;/td&gt;&lt;td&gt;&lt;b&gt;LED[1]:&lt;/b&gt; Flash Busy (WIP)&lt;/td&gt;&lt;td&gt;&lt;b&gt;LED[2]:&lt;/b&gt; Tag Valid Strobe&lt;/td&gt;&lt;td&gt;&lt;b&gt;LED[3]:&lt;/b&gt; Match OK&lt;/td&gt;&lt;td&gt;&lt;b&gt;LED[15:4]:&lt;/b&gt; Diagnostics&lt;/td&gt;&lt;/tr&gt;&lt;/table&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f1f5f9;strokeColor=#475569;strokeWidth=2.5;fontFamily=Segoe UI;shadow=1;" vertex="1" parent="1">
          <mxGeometry x="140" y="780" width="760" height="110" as="geometry" />
        </mxCell>

        <!-- Wire SoC -> LEDs -->
        <mxCell id="w_soc_leds" value="leds_o[15:0]" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2.5;strokeColor=#475569;fontSize=14;fontStyle=1;endArrow=block;endFill=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="soc" target="leds">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
    with open("fig1_block_diagram.drawio", "w", encoding="utf-8") as f:
        f.write(xml_content)
    print("[SUCCESS] Genuine Draw.io file created at: fig1_block_diagram.drawio")

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
    padding: 20px;
    width: 1540px;
    height: 1040px;
    position: relative;
    overflow: hidden;
  }

  /* Main Diagram Frame */
  .diagram-container {
    width: 1500px;
    height: 1000px;
    border: 3px solid #0f172a;
    border-radius: 14px;
    background: #ffffff;
    position: relative;
    padding: 20px 24px;
    box-shadow: 0 12px 30px -5px rgba(0, 0, 0, 0.1);
  }

  /* Header Title Banner */
  .title-banner {
    text-align: center;
    border-bottom: 2.5px solid #cbd5e1;
    padding-bottom: 12px;
    margin-bottom: 20px;
  }
  .title-banner h1 {
    font-size: 25px;
    font-weight: 900;
    color: #0f172a;
    letter-spacing: 0.6px;
    text-transform: uppercase;
  }
  .title-banner p {
    font-size: 15px;
    font-weight: 700;
    color: #475569;
    margin-top: 4px;
  }

  /* Card Common Styles */
  .drawio-card {
    position: absolute;
    border-radius: 12px;
    border: 2.5px solid;
    padding: 15px 18px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.07);
    background: #ffffff;
  }
  .card-title {
    font-size: 19px;
    font-weight: 800;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .card-subtitle {
    font-size: 14.5px;
    font-weight: 700;
    margin-bottom: 8px;
  }
  .badge {
    font-size: 12.5px;
    font-weight: 800;
    padding: 3px 9px;
    border-radius: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  /* 1. POWER SUPPLY (TOP LEFT) */
  .card-power {
    left: 30px;
    top: 85px;
    width: 280px;
    height: 110px;
    border-color: #d97706;
    background: #fffbeb;
  }
  .card-power .card-title { color: #b45309; }

  /* 2. REGULATOR (TOP CENTER) */
  .card-reg {
    left: 420px;
    top: 85px;
    width: 320px;
    height: 110px;
    border-color: #dc2626;
    background: #fef2f2;
  }
  .card-reg .card-title { color: #b91c1c; }

  /* 3. CLOCK OSCILLATOR (TOP RIGHT) */
  .card-clk {
    left: 780px;
    top: 85px;
    width: 300px;
    height: 110px;
    border-color: #4f46e5;
    background: #eef2ff;
  }
  .card-clk .card-title { color: #4338ca; }

  /* 4. CENTRAL SOC (CENTERPIECE) */
  .card-soc {
    left: 420px;
    top: 265px;
    width: 470px;
    height: 485px;
    border-color: #2563eb;
    background: #f8fafc;
    border-width: 3.5px;
    padding: 16px 18px;
    z-index: 5;
  }
  .soc-header {
    text-align: center;
    background: #eff6ff;
    border: 2px solid #bfdbfe;
    border-radius: 10px;
    padding: 10px 12px;
    margin-bottom: 12px;
  }
  .soc-title {
    font-size: 26px;
    font-weight: 900;
    color: #1e3a8a;
    letter-spacing: 0.5px;
  }
  .soc-modname {
    font-family: 'Consolas', monospace;
    font-size: 16px;
    font-weight: 800;
    color: #2563eb;
  }
  .soc-desc {
    font-size: 13px;
    font-weight: 700;
    color: #475569;
    margin-top: 2px;
  }
  .soc-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 12px;
  }
  .soc-pill {
    background: #ffffff;
    border: 1.8px solid #cbd5e1;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 14px;
    font-weight: 800;
    color: #0f172a;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }
  .soc-pill span {
    display: block;
    font-size: 11.5px;
    font-weight: 600;
    color: #64748b;
    margin-top: 1px;
  }

  /* 5. RFID READER (LEFT TOP) */
  .card-rfid {
    left: 30px;
    top: 265px;
    width: 280px;
    height: 225px;
    border-color: #f59e0b;
    background: #fffdf5;
  }
  .card-rfid .card-title { color: #b45309; }

  /* 6. FIRMWARE PROGRAM (LEFT BOTTOM) */
  .card-fw {
    left: 30px;
    top: 525px;
    width: 280px;
    height: 225px;
    border-color: #10b981;
    background: #f0fdf4;
  }
  .card-fw .card-title { color: #047857; }

  /* 7. SPI FLASH MEMORY (RIGHT TOP) */
  .card-flash {
    left: 1030px;
    top: 245px;
    width: 440px;
    height: 245px;
    border-color: #16a34a;
    background: #f0fdf4;
  }
  .card-flash .card-title { color: #15803d; }
  .mem-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    margin-top: 6px;
  }
  .mem-table td {
    padding: 5px 8px;
    border: 1.5px solid #bbf7d0;
    background: #ffffff;
  }
  .mem-addr {
    font-family: 'Consolas', monospace;
    font-weight: 800;
    color: #166534;
    white-space: nowrap;
  }

  /* 8. HOST PC CONSOLE (RIGHT MID) */
  .card-host {
    left: 1030px;
    top: 515px;
    width: 440px;
    height: 205px;
    border-color: #8b5cf6;
    background: #faf5ff;
  }
  .card-host .card-title { color: #6d28d9; }

  /* 9. STATUS BUTTON (RIGHT BOTTOM) */
  .card-btn {
    left: 1080px;
    top: 755px;
    width: 390px;
    height: 155px;
    border-color: #f43f5e;
    background: #fff1f2;
    padding: 16px 20px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .card-btn .card-title { color: #be123c; margin-bottom: 6px; }

  /* 10. 16 DIAGNOSTIC LEDS (BOTTOM CENTER-LEFT) */
  .card-leds {
    left: 130px;
    top: 785px;
    width: 750px;
    height: 155px;
    border-color: #475569;
    background: #f8fafc;
  }
  .card-leds .card-title { color: #1e293b; }
  .led-row {
    display: flex;
    gap: 12px;
    margin-top: 10px;
  }
  .led-item {
    flex: 1;
    background: #ffffff;
    border: 1.8px solid #cbd5e1;
    border-radius: 8px;
    padding: 10px 8px;
    text-align: center;
  }
  .led-dot {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    margin: 0 auto 6px auto;
    background: #22c55e;
    box-shadow: 0 0 10px #22c55e;
  }
  .led-item:nth-child(2) .led-dot { background: #eab308; box-shadow: 0 0 10px #eab308; }
  .led-item:nth-child(3) .led-dot { background: #3b82f6; box-shadow: 0 0 10px #3b82f6; }
  .led-item:nth-child(4) .led-dot { background: #10b981; box-shadow: 0 0 10px #10b981; }
  .led-item:nth-child(5) .led-dot { background: #8b5cf6; box-shadow: 0 0 10px #8b5cf6; }

  .led-name {
    font-family: 'Consolas', monospace;
    font-size: 14px;
    font-weight: 800;
    color: #0f172a;
  }
  .led-func {
    font-size: 12.5px;
    font-weight: 600;
    color: #64748b;
    margin-top: 2px;
  }

  /* SVG CONNECTORS OVERLAY */
  svg.connectors {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 2;
  }

  .signal-label {
    position: absolute;
    background: #ffffff;
    border: 2px solid;
    border-radius: 6px;
    padding: 4px 10px;
    font-family: 'Consolas', monospace;
    font-size: 13px;
    font-weight: 800;
    box-shadow: 0 2px 6px rgba(0,0,0,0.12);
    z-index: 10;
    white-space: nowrap;
    text-align: center;
  }
</style>
</head>
<body>

<div class="diagram-container">
  <!-- Banner -->
  <div class="title-banner">
    <h1>HỆ THỐNG PHẦN CỨNG PICORV32 RISC-V SOC XỬ LÝ DỮ LIỆU THẺ RFID RDM6300</h1>
    <p>Sơ đồ khối phần cứng nguyên lý hoàn chỉnh (Hardware Architecture Schematic Block Diagram)</p>
  </div>

  <!-- SVG Arrows and Bus lines -->
  <svg class="connectors">
    <defs>
      <marker id="arrow-black" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
        <polygon points="0 1, 9 4.5, 0 8" fill="#0f172a"/>
      </marker>
      <marker id="arrow-red" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
        <polygon points="0 1, 9 4.5, 0 8" fill="#dc2626"/>
      </marker>
      <marker id="arrow-orange" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
        <polygon points="0 1, 9 4.5, 0 8" fill="#d97706"/>
      </marker>
      <marker id="arrow-green" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
        <polygon points="0 1, 9 4.5, 0 8" fill="#16a34a"/>
      </marker>
      <marker id="arrow-blue" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
        <polygon points="0 1, 9 4.5, 0 8" fill="#2563eb"/>
      </marker>
      <marker id="arrow-purple" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
        <polygon points="0 1, 9 4.5, 0 8" fill="#7c3aed"/>
      </marker>
      <marker id="arrow-rose" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
        <polygon points="0 1, 9 4.5, 0 8" fill="#f43f5e"/>
      </marker>
    </defs>

    <!-- 1. Pwr -> Reg (Horizontal: x=310 to 420 at y=140) -->
    <path d="M 310 140 L 420 140" stroke="#dc2626" stroke-width="3" fill="none" marker-end="url(#arrow-red)"/>

    <!-- 2. Reg -> SoC (VDD: from x=540, y=195 down to y=265) -->
    <path d="M 540 195 L 540 265" stroke="#dc2626" stroke-width="3" fill="none" marker-end="url(#arrow-red)"/>

    <!-- 3. Clk -> SoC (clk: from x=880, y=195 down to y=230, left to x=760, down to y=265) -->
    <path d="M 880 195 L 880 230 L 760 230 L 760 265" stroke="#4f46e5" stroke-width="3" fill="none" marker-end="url(#arrow-blue)"/>

    <!-- 4. RFID -> SoC (rdm_rx: Horizontal: x=310 to 420 at y=375) -->
    <path d="M 310 375 L 420 375" stroke="#d97706" stroke-width="3.5" fill="none" marker-end="url(#arrow-orange)"/>

    <!-- 5. FW -> SoC (boot_vec: Horizontal: x=310 to 420 at y=640) -->
    <path d="M 310 640 L 420 640" stroke="#10b981" stroke-width="3.5" fill="none" marker-end="url(#arrow-green)"/>

    <!-- 6. SoC <-> SPI Flash (Gap: x=890 to 1030) -->
    <!-- MOSI/CS/SCK: SoC -> Flash at y=335 -->
    <path d="M 890 335 L 1030 335" stroke="#16a34a" stroke-width="3.5" fill="none" marker-end="url(#arrow-green)"/>
    <!-- MISO: Flash -> SoC at y=400 -->
    <path d="M 1030 400 L 890 400" stroke="#16a34a" stroke-width="3.5" fill="none" marker-end="url(#arrow-green)"/>

    <!-- 7. SoC <-> Host PC (Gap: x=890 to 1030) -->
    <!-- UART TX: SoC -> PC at y=575 -->
    <path d="M 890 575 L 1030 575" stroke="#7c3aed" stroke-width="3.5" fill="none" marker-end="url(#arrow-purple)"/>
    <!-- UART RX: PC -> SoC at y=640 -->
    <path d="M 1030 640 L 890 640" stroke="#7c3aed" stroke-width="3.5" fill="none" marker-end="url(#arrow-purple)"/>

    <!-- 8. Status Button -> SoC (rst_n: Completely in open gap x=970, y=832 to 705) -->
    <path d="M 1080 832 L 970 832 L 970 705 L 890 705" stroke="#f43f5e" stroke-width="3" fill="none" marker-end="url(#arrow-rose)"/>

    <!-- 9. SoC -> LEDs (Vertical: x=510, y=750 down to y=785) -->
    <path d="M 510 750 L 510 785" stroke="#0f172a" stroke-width="3.5" fill="none" marker-end="url(#arrow-black)"/>
  </svg>

  <!-- Signal Pill Badges (Carefully Centered in Gaps to Prevent ANY Box Clipping) -->
  <!-- Gap 1: Power to Reg (x=310..420, width=110px) -->
  <div class="signal-label" style="left: 325px; top: 125px; color: #b91c1c; border-color: #dc2626;">+5V DC</div>

  <!-- Gap 2: Reg to SoC (y=195..265, height=70px) -->
  <div class="signal-label" style="left: 470px; top: 224px; color: #b91c1c; border-color: #dc2626;">VDD (1.8V / 3.3V)</div>

  <!-- Gap 3: Clk to SoC (y=195..265, height=70px) -->
  <div class="signal-label" style="left: 775px; top: 224px; color: #4338ca; border-color: #4f46e5;">clk (50MHz)</div>

  <!-- Gap 4: RFID to SoC (x=310..420, center=365) -->
  <div class="signal-label" style="left: 316px; top: 360px; color: #b45309; border-color: #d97706;">rdm_rx (J1)</div>

  <!-- Gap 5: FW to SoC (x=310..420, center=365) -->
  <div class="signal-label" style="left: 312px; top: 625px; color: #047857; border-color: #10b981;">boot (0x250000)</div>

  <!-- Gap 6: SoC to Flash (x=890..1030, width=140px) -->
  <div class="signal-label" style="left: 902px; top: 318px; color: #15803d; border-color: #16a34a;">CS, SCK, MOSI</div>
  <div class="signal-label" style="left: 935px; top: 383px; color: #15803d; border-color: #16a34a;">MISO</div>

  <!-- Gap 7: SoC to Host PC (x=890..1030, width=140px) -->
  <div class="signal-label" style="left: 910px; top: 558px; color: #6d28d9; border-color: #7c3aed;">uart_tx (A18)</div>
  <div class="signal-label" style="left: 910px; top: 623px; color: #6d28d9; border-color: #7c3aed;">uart_rx (B18)</div>

  <!-- Gap 8: Reset Button (Corner at x=970, y=705) -->
  <div class="signal-label" style="left: 915px; top: 688px; color: #be123c; border-color: #f43f5e;">rst_n (U18)</div>

  <!-- Gap 9: SoC to LEDs (y=750..785) -->
  <div class="signal-label" style="left: 450px; top: 755px; color: #0f172a; border-color: #0f172a;">leds_o[15:0] (16 Pins)</div>

  <!-- 1. POWER INPUT -->
  <div class="drawio-card card-power">
    <div class="card-title">
      <span>POWER INPUT</span>
      <span class="badge" style="background:#fde68a;color:#92400e;">USB 5V</span>
    </div>
    <div style="font-size: 13.5px; font-weight: 600; color: #451a03; line-height: 1.45;">
      • USB Type-B / Micro-USB VBUS<br>
      • +5.0V DC Regulated @ 500mA<br>
      • Onboard Filter & Fuse
    </div>
  </div>

  <!-- 2. REGULATOR -->
  <div class="drawio-card card-reg">
    <div class="card-title">
      <span>VOLTAGE REGULATORS</span>
      <span class="badge" style="background:#fecaca;color:#991b1b;">Dual LDO</span>
    </div>
    <div style="font-size: 13.5px; font-weight: 600; color: #450a0a; line-height: 1.45;">
      • <b>3.3V LDO:</b> I/O Pads, SPI Flash & RFID PMOD<br>
      • <b>1.8V LDO:</b> ASIC Core Logic (Sky130)
    </div>
  </div>

  <!-- 3. CLOCK OSCILLATOR -->
  <div class="drawio-card card-clk">
    <div class="card-title">
      <span>CLOCK GENERATOR</span>
      <span class="badge" style="background:#c7d2fe;color:#3730a3;">50 MHz</span>
    </div>
    <div style="font-size: 13.5px; font-weight: 600; color: #1e1b4b; line-height: 1.45;">
      • 50.0 MHz Quartz Crystal Osc<br>
      • Period: 20.0 ns (Master clk)<br>
      • Low Jitter Clock Buffer
    </div>
  </div>

  <!-- 4. CENTRAL SOC -->
  <div class="drawio-card card-soc">
    <div class="soc-header">
      <div class="soc-title">PicoRV32 RISC-V SoC</div>
      <div class="soc-modname">rdm6300_picorv32_soc</div>
      <div class="soc-desc">SkyWater 130nm Standard-Cell ASIC / Basys 3 FPGA Demo</div>
    </div>

    <div class="soc-grid">
      <div class="soc-pill">
        CPU Core: RV32I
        <span>PicoRV32 32-bit RISC-V</span>
      </div>
      <div class="soc-pill">
        Data SRAM: 1 KB
        <span>Single-Cycle 256x32 Local RAM</span>
      </div>
      <div class="soc-pill">
        Flash Controller
        <span>SPIMEMIO QSPI / Fast Read</span>
      </div>
      <div class="soc-pill">
        Dual UART Channels
        <span>Host PC + RFID Receiver</span>
      </div>
      <div class="soc-pill">
        Auto HW Decoder
        <span>1-Cycle XOR Engine & Watchdog</span>
      </div>
      <div class="soc-pill">
        GPIO Controller
        <span>16 Diagnostic Outputs</span>
      </div>
    </div>

    <!-- SoC Pinout Summary: Clean 4-column badges -->
    <div style="background:#ffffff; border: 1.8px solid #cbd5e1; border-radius: 8px; padding: 10px 12px; font-size: 13px;">
      <div style="font-weight: 800; color: #1e293b; margin-bottom: 6px; text-transform: uppercase;">Top-Level SoC Interfaces:</div>
      <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap: 6px; text-align: center; font-family:'Consolas',monospace; font-size:12px; font-weight:800;">
        <span style="background:#fee2e2; color:#b91c1c; padding:4px 2px; border-radius:5px; border:1px solid #fca5a5;">clk, rst_n</span>
        <span style="background:#fef3c7; color:#b45309; padding:4px 2px; border-radius:5px; border:1px solid #fcd34d;">rdm6300_rx</span>
        <span style="background:#dcfce7; color:#15803d; padding:4px 2px; border-radius:5px; border:1px solid #86efac;">flash_io[3:0]</span>
        <span style="background:#f3e8ff; color:#6d28d9; padding:4px 2px; border-radius:5px; border:1px solid #d8b4fe;">uart_rx, tx</span>
      </div>
    </div>
  </div>

  <!-- 5. RFID READER -->
  <div class="drawio-card card-rfid">
    <div class="card-title">
      <span>RFID READER</span>
      <span class="badge" style="background:#fde68a;color:#92400e;">125 kHz</span>
    </div>
    <div class="card-subtitle" style="color:#d97706;">RDM6300 PMOD Transceiver</div>
    <div style="font-size: 13.5px; font-weight: 600; color: #451a03; line-height: 1.45;">
      • External Tuned Coil Antenna<br>
      • EM4100 125 kHz Passive Tag<br>
      • Serial Stream: 9600 Baud 8-N-1<br>
      • 14-Byte ASCII Frame Protocol:<br>
      &nbsp;&nbsp;[0x02] + [10 Hex] + [CS] + [0x03]
    </div>
  </div>

  <!-- 6. FIRMWARE PROGRAM -->
  <div class="drawio-card card-fw">
    <div class="card-title">
      <span>ASM / C PROGRAM</span>
      <span class="badge" style="background:#a7f3d0;color:#065f46;">Firmware</span>
    </div>
    <div class="card-subtitle" style="color:#059669;">Bare-Metal RISC-V C Code</div>
    <div style="font-size: 13.5px; font-weight: 600; color: #064e3b; line-height: 1.45;">
      • Toolchain: riscv32-unknown-elf-gcc<br>
      • Source: <b>start.s</b> (C Runtime init)<br>
      • Firmware Logic: <b>firmware.c</b><br>
      • Binary: <b>firmware.hex</b><br>
      • Executed via Flash XIP at:<br>
      &nbsp;&nbsp;<b style="font-family:'Consolas',monospace;color:#047857;">Reset Vector: 0x0025_0000</b>
    </div>
  </div>

  <!-- 7. SPI FLASH MEMORY -->
  <div class="drawio-card card-flash">
    <div class="card-title">
      <span>SPI NOR FLASH MEMORY</span>
      <span class="badge" style="background:#bbf7d0;color:#14532d;">4 MB / 32 Mb</span>
    </div>
    <div class="card-subtitle" style="color:#15803d;">Spansion S25FL032P (XIP Boot + Whitelist Storage)</div>
    <table class="mem-table">
      <tr>
        <td class="mem-addr">Sector 0-36 (0x000000)</td>
        <td>FPGA Hardware Bitstream Configuration</td>
      </tr>
      <tr>
        <td class="mem-addr">Sector 37 (0x00250000)</td>
        <td>PicoRV32 Firmware Machine Code (XIP Mode)</td>
      </tr>
      <tr>
        <td class="mem-addr">Sector 48 (0x00300000)</td>
        <td>Authorized RFID Whitelist Database</td>
      </tr>
      <tr>
        <td class="mem-addr">Sector 49 (0x00310000)</td>
        <td>Non-Volatile Real-Time Access Logs Database</td>
      </tr>
    </table>
  </div>

  <!-- 8. HOST PC CONSOLE -->
  <div class="drawio-card card-host">
    <div class="card-title">
      <span>HOST PC CONSOLE</span>
      <span class="badge" style="background:#ddd6fe;color:#5b21b6;">Win32 C App</span>
    </div>
    <div class="card-subtitle" style="color:#6d28d9;">Management Application (host/main.c)</div>
    <div style="font-size: 13.5px; font-weight: 600; color: #3b0764; line-height: 1.45;">
      • FTDI FT2232 USB-to-UART Bridge @ 9600 Baud 8-N-1<br>
      • 13 Administrative Commands:<br>
      &nbsp;&nbsp;Ping SoC, Add/Delete Whitelist Cards, Check Status,<br>
      &nbsp;&nbsp;Simulate Virtual Scan, View Access Logs, Export/Import CSV
    </div>
  </div>

  <!-- 9. STATUS BUTTON -->
  <div class="drawio-card card-btn">
    <div class="card-title">
      <span>STATUS BUTTON</span>
      <span class="badge" style="background:#fecdd3;color:#9f1239;">RESET</span>
    </div>
    <div style="display:flex; align-items:center; gap: 16px; margin-top: 6px;">
      <div style="font-size: 36px; color: #e11d48; line-height: 1;">🔘</div>
      <div>
        <div style="font-size: 14.5px; font-weight: 800; color: #881337;">
          Manual Push Button
        </div>
        <div style="font-size: 13px; font-weight: 600; color: #9f1239; margin-top: 3px;">
          Active-Low System Reset<br>
          <span style="font-family:'Consolas',monospace; font-weight:800;">rst_n (Pin U18)</span>
        </div>
      </div>
    </div>
  </div>

  <!-- 10. 16 DIAGNOSTIC LEDS -->
  <div class="drawio-card card-leds">
    <div class="card-title">
      <span>16 DIAGNOSTIC LEDS (Basys 3 Prototyping Board)</span>
      <span class="badge" style="background:#e2e8f0;color:#1e293b;">16x LEDs</span>
    </div>
    <div class="led-row">
      <div class="led-item">
        <div class="led-dot"></div>
        <div class="led-name">LED[0]</div>
        <div class="led-func">Heartbeat (1Hz)</div>
      </div>
      <div class="led-item">
        <div class="led-dot"></div>
        <div class="led-name">LED[1]</div>
        <div class="led-func">Flash Busy (WIP)</div>
      </div>
      <div class="led-item">
        <div class="led-dot"></div>
        <div class="led-name">LED[2]</div>
        <div class="led-func">Tag Valid Strobe</div>
      </div>
      <div class="led-item">
        <div class="led-dot"></div>
        <div class="led-name">LED[3]</div>
        <div class="led-func">Whitelist Match OK</div>
      </div>
      <div class="led-item">
        <div class="led-dot"></div>
        <div class="led-name">LED[15:4]</div>
        <div class="led-func">Diagnostics & Self-Test</div>
      </div>
    </div>
  </div>
</div>

</body>
</html>
"""
    with open("fig1_drawio_style.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("[SUCCESS] HTML vector source written at: fig1_drawio_style.html")

    # Render via Chrome headless at 2x DPI
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    html_path = os.path.abspath("fig1_drawio_style.html")
    out_img = os.path.abspath("fig1_block_diagram.png")

    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--force-device-scale-factor=2",
        f"--screenshot={out_img}",
        "--window-size=1560,1060",
        f"file:///{html_path.replace(os.sep, '/')}"
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(out_img):
        print(f"[SUCCESS] Ultra-high resolution Draw.io rendered image generated at: {out_img} ({os.path.getsize(out_img)} bytes)")
    else:
        print("[ERROR] Chrome rendering failed:", res.stderr)

if __name__ == '__main__':
    create_drawio_xml()
    create_html_and_render_png()
