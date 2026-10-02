# -*- coding: utf-8 -*-
"""
Script: generate_drawio_bnw_diagram.py
Generates the authentic Draw.io Black & White schematic block diagram matching
the complete modular SoC architecture with 5 distinct Slaves:
- Master: PicoRV32 RISC-V CPU Core (rtl/picorv32.v)
- Bus: Internal Memory Bus Interconnect (rtl/soc_interconnect.v)
- Slave 0: 1KB Data SRAM (rtl/data_sram.v) - 0x0000_0000
- Slave 1: SPIMEMIO Flash Controller (rtl/spimemio.v) - 0x0010_0000 / 0x0200_0000
- Slave 2: RDM6300 RFID MMIO Peripheral (rtl/rdm6300_mmio.v) - 0x1000_0000
- Slave 3: Host PC UART MMIO Peripheral & FIFOs (rtl/host_uart_mmio.v) - 0x3000_0000
- Slave 4: GPIO MMIO Peripheral & LEDs (rtl/soc_gpio_mmio.v) - 0x4000_0000

Pure Black & White, high contrast, clean orthogonal routing, sharp arrowheads.
Outputs:
  1. rdm6300_picorv32_soc_complete_diagram.drawio (Draw.io XML)
  2. rdm6300_picorv32_soc_complete_diagram.svg (Clean Vector SVG)
  3. document/temp/fig1_block_diagram.png (High-Res 2x Retina PNG via Headless Chrome)
"""

import os
import subprocess
import shutil

def create_drawio_xml():
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="2026-10-02T08:00:00.000Z" agent="Mozilla/5.0" version="21.0.0" type="device">
  <diagram id="soc_architecture" name="SoC Block Diagram">
    <mxGraphModel dx="1600" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1580" pageHeight="920" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- ============================================================= -->
        <!-- 1. CHIP BOUNDARY (ASIC)                                       -->
        <!-- ============================================================= -->
        <mxCell id="chip" value="&lt;b style=&quot;font-size:21px;&quot;&gt;rdm6300_picorv32_soc (Top-Level ASIC Chip - rtl/rdm6300_picorv32_soc.v)&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2.5;verticalAlign=top;align=left;spacingLeft=30;spacingTop=12;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="250" y="25" width="1290" height="865" as="geometry" />
        </mxCell>

        <!-- Global Clock and Reset Inputs -->
        <mxCell id="w_clk_in" value="clk_i (50 MHz)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=13;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="140" y="85" as="sourcePoint" />
            <mxPoint x="275" y="85" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <mxCell id="w_rst_in" value="rst_n_i" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=13;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="140" y="125" as="sourcePoint" />
            <mxPoint x="275" y="125" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <!-- ============================================================= -->
        <!-- 2. EXTERNAL SPI FLASH (OFF-CHIP)                              -->
        <!-- ============================================================= -->
        <mxCell id="ext_flash" value="&lt;b style=&quot;font-size:17px;&quot;&gt;External&lt;br&gt;SPI Flash&lt;br&gt;(Off-Chip)&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;span style=&quot;font-size:14px;&quot;&gt;- Firmware&lt;br&gt;Storage&lt;br&gt;(W25Q128)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="25" y="260" width="155" height="320" as="geometry" />
        </mxCell>

        <!-- Flash Pins Wires & Labels -->
        <mxCell id="w_csb" value="flash_csb" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=14;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="ext_flash" target="spimemio">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="225" y="330" />
              <mxPoint x="225" y="330" />
            </Array>
          </mxGeometry>
        </mxCell>

        <mxCell id="w_clk" value="flash_clk" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=14;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="ext_flash" target="spimemio">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="225" y="420" />
              <mxPoint x="225" y="420" />
            </Array>
          </mxGeometry>
        </mxCell>

        <mxCell id="w_io" value="flash_io[3:0]" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#000000;startArrow=classic;startFill=1;endArrow=classic;endFill=1;fontSize=14;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="ext_flash" target="spimemio">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="225" y="510" />
              <mxPoint x="225" y="510" />
            </Array>
          </mxGeometry>
        </mxCell>

        <!-- ============================================================= -->
        <!-- 3. SLAVE 1: SPIMEMIO FLASH CONTROLLER                         -->
        <!-- ============================================================= -->
        <mxCell id="spimemio" value="&lt;b style=&quot;font-size:18px;&quot;&gt;SLAVE 1:&lt;br&gt;SPIMEMIO&lt;br&gt;Flash Controller&lt;/b&gt;&lt;br&gt;&lt;b style=&quot;font-size:15px;&quot;&gt;(rtl/core/spimemio.v)&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;span style=&quot;font-size:14px;&quot;&gt;0x0010_0000 -&lt;br&gt;0x00FF_FFFF&lt;br&gt;&lt;br&gt;(XIP Read &amp;amp;&lt;br&gt;SPI Bit-Bang&lt;br&gt;0x0200_0000)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="275" y="75" width="175" height="735" as="geometry" />
        </mxCell>

        <!-- ============================================================= -->
        <!-- 4. BUS: CENTRAL MEMORY BUS INTERCONNECT (soc_interconnect.v)  -->
        <!-- ============================================================= -->
        <mxCell id="bus" value="&lt;b style=&quot;font-size:17px;&quot;&gt;Internal Memory Bus Interconnect (rtl/core/soc_interconnect.v)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:13px;font-weight:bold;&quot;&gt;MMIO Address Decoder &amp;amp; Bus Multiplexer (1 Master ➔ 5 Dedicated Slaves)&lt;/span&gt;&lt;br&gt;&lt;hr style=&quot;border:0.5px solid #000;margin:4px 0;&quot;/&gt;&lt;span style=&quot;font-size:11px;font-weight:600;&quot;&gt;S0: rtl/core/data_sram.v (0x0000_0000) | S1: rtl/core/spimemio.v (0x0010_0000)&lt;br/&gt;S2: rtl/rdm6300/rdm6300_mmio.v (0x1000_0000) | S3: rtl/host/host_uart_mmio.v (0x3000_0000) | S4: rtl/core/soc_gpio_mmio.v (0x4000_0000)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2.5;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="475" y="75" width="610" height="120" as="geometry" />
        </mxCell>

        <!-- ============================================================= -->
        <!-- 5. SLAVE 0: 1KB DATA SRAM                                     -->
        <!-- ============================================================= -->
        <mxCell id="sram" value="&lt;b style=&quot;font-size:17px;&quot;&gt;SLAVE 0:&lt;br&gt;1KB Data SRAM&lt;/b&gt;&lt;br&gt;&lt;b style=&quot;font-size:14.5px;&quot;&gt;(rtl/core/data_sram.v)&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;span style=&quot;font-size:14px;&quot;&gt;0x0000_0000&lt;br&gt;(Stack &amp;amp; Variables)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="1115" y="75" width="225" height="135" as="geometry" />
        </mxCell>

        <!-- ============================================================= -->
        <!-- 6. MASTER: PICORV32 RISC-V CPU CORE                           -->
        <!-- ============================================================= -->
        <mxCell id="cpu" value="&lt;b style=&quot;font-size:19px;&quot;&gt;MASTER:&lt;br&gt;PicoRV32 RISC-V CPU&lt;/b&gt;&lt;br&gt;&lt;b style=&quot;font-size:15px;&quot;&gt;(rtl/core/picorv32.v)&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;b style=&quot;font-size:14px;&quot;&gt;(C Firmware Execution -&lt;br&gt;firmware/main.c)&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;span style=&quot;font-size:13px;&quot;&gt;RV32I Core (32 Registers)&lt;br&gt;PC Reset: 0x0025_0000 (Flash)&lt;br&gt;Stack Pointer: 0x0000_0400 (SRAM)&lt;br&gt;Native 32-bit Memory Bus&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontFamily=Arial,Helvetica,sans-serif;verticalAlign=top;spacingTop=16;" vertex="1" parent="1">
          <mxGeometry x="475" y="230" width="235" height="440" as="geometry" />
        </mxCell>

        <!-- ============================================================= -->
        <!-- 7. SLAVE 2: RDM6300 RFID MMIO MODULE (rtl/rdm6300_mmio.v)      -->
        <!-- ============================================================= -->
        <mxCell id="rfid_box" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2.2;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="770" y="230" width="625" height="245" as="geometry" />
        </mxCell>        <mxCell id="rfid_banner" value="&lt;b style=&quot;font-size:16px;&quot;&gt;SLAVE 2: rtl/rdm6300/rdm6300_mmio.v (RFID MMIO Peripheral Module)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:12px;font-weight:bold;&quot;&gt;MMIO Address: 0x1000_0000 - 0x1000_0008 | Bus Select: sel_rfid&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.5;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="770" y="230" width="625" height="42" as="geometry" />
        </mxCell>

        <mxCell id="rfid_reg" value="&lt;b style=&quot;font-size:14.5px;&quot;&gt;MMIO Registers&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:11px;font-weight:bold;&quot;&gt;(in rdm6300_mmio.v)&lt;/span&gt;&lt;br&gt;&lt;br&gt;&lt;span style=&quot;font-size:12px;&quot;&gt;STATUS (0x0)&lt;br&gt;TAG_HI (0x4)&lt;br&gt;TAG_LO (0x8)&lt;br&gt;&lt;br&gt;card_valid_o&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.6;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="785" y="285" width="130" height="175" as="geometry" />
        </mxCell>

        <mxCell id="rfid_dec" value="&lt;b style=&quot;font-size:14.5px;&quot;&gt;rdm6300_&lt;br&gt;frame_decoder&lt;/b&gt;&lt;br&gt;&lt;b style=&quot;font-size:11.5px;&quot;&gt;(frame_decoder.v)&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;span style=&quot;font-size:11.5px;&quot;&gt;14-Byte Frame&lt;br&gt;1-Cycle XOR Check&lt;br&gt;Watchdog 10ms&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.6;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="930" y="285" width="145" height="175" as="geometry" />
        </mxCell>

        <mxCell id="rfid_rx" value="&lt;b style=&quot;font-size:14.5px;&quot;&gt;uart_rx&lt;/b&gt;&lt;br&gt;&lt;b style=&quot;font-size:11.5px;&quot;&gt;(rtl/rdm6300/uart_rx.v)&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;span style=&quot;font-size:11.5px;&quot;&gt;9600 Baud&lt;br&gt;8-N-1 UART&lt;br&gt;Majority Sampler&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.6;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="1090" y="285" width="115" height="175" as="geometry" />
        </mxCell>

        <mxCell id="rfid_sync" value="&lt;b style=&quot;font-size:14.5px;&quot;&gt;sync_2ff&lt;/b&gt;&lt;br&gt;&lt;b style=&quot;font-size:11.5px;&quot;&gt;(rtl/core/sync_2ff.v)&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;span style=&quot;font-size:11.5px;&quot;&gt;2-FF CDC Sync&lt;br&gt;MTBF &gt; 1000 Yrs&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.6;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="1220" y="285" width="130" height="175" as="geometry" />
        </mxCell>

        <!-- RFID Internal Signal Connections -->
        <mxCell id="ar_rfid_in" value="rdm6300_rx_i" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=13.5;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="1530" y="372" as="sourcePoint" />
            <mxPoint x="1350" y="372" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <mxCell id="ar_s_rx" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=1.6;strokeColor=#000000;endArrow=classic;endFill=1;" edge="1" parent="1" source="rfid_sync" target="rfid_rx" />
        <mxCell id="ar_rx_dec" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=1.6;strokeColor=#000000;endArrow=classic;endFill=1;" edge="1" parent="1" source="rfid_rx" target="rfid_dec" />
        <mxCell id="ar_dec_reg" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=1.6;strokeColor=#000000;endArrow=classic;endFill=1;" edge="1" parent="1" source="rfid_dec" target="rfid_reg" />

        <!-- ============================================================= -->
        <!-- 8. SLAVE 3: HOST PC UART MMIO MODULE (rtl/host_uart_mmio.v)    -->
        <!-- ============================================================= -->
        <mxCell id="uart_box" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2.2;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="770" y="500" width="625" height="245" as="geometry" />
        </mxCell>

        <mxCell id="uart_banner" value="&lt;b style=&quot;font-size:16px;&quot;&gt;SLAVE 3: rtl/host/host_uart_mmio.v (Host PC UART MMIO Peripheral Module)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:12px;font-weight:bold;&quot;&gt;MMIO Address: 0x3000_0000 - 0x3000_0004 | Bus Select: sel_uart&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.5;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="770" y="500" width="625" height="42" as="geometry" />
        </mxCell>

        <mxCell id="u_mmio" value="&lt;b style=&quot;font-size:14.5px;&quot;&gt;UART MMIO&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:11px;font-weight:bold;&quot;&gt;(in host_uart_mmio.v)&lt;/span&gt;&lt;br&gt;&lt;br&gt;&lt;span style=&quot;font-size:11.5px;&quot;&gt;DIV (0x3000_0000)&lt;br&gt;DAT (0x3000_0004)&lt;br&gt;&lt;br&gt;FIFO Control&lt;br&gt;1-Cycle Ready&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.6;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="785" y="555" width="130" height="175" as="geometry" />
        </mxCell>

        <mxCell id="u_fifo" value="&lt;b style=&quot;font-size:14.5px;&quot;&gt;sync_fifo (x2)&lt;/b&gt;&lt;br&gt;&lt;b style=&quot;font-size:11.5px;&quot;&gt;(rtl/host/sync_fifo.v)&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;span style=&quot;font-size:11.5px;&quot;&gt;32-Byte RX FIFO&lt;br&gt;32-Byte TX FIFO&lt;br&gt;Zero Packet Drop&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.6;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="930" y="555" width="135" height="175" as="geometry" />
        </mxCell>

        <mxCell id="u_core" value="&lt;b style=&quot;font-size:14.5px;&quot;&gt;simpleuart&lt;/b&gt;&lt;br&gt;&lt;b style=&quot;font-size:11.5px;&quot;&gt;(rtl/host/simpleuart.v)&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;span style=&quot;font-size:11.5px;&quot;&gt;Full-Duplex UART&lt;br&gt;TX / RX Core&lt;br&gt;Baud Divisor 5208&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.6;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="1080" y="555" width="140" height="175" as="geometry" />
        </mxCell>

        <mxCell id="u_sync" value="&lt;b style=&quot;font-size:14px;&quot;&gt;sync_2ff&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;(rtl/core/sync_2ff.v)&lt;br&gt;CDC Sync&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.6;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="1235" y="555" width="120" height="80" as="geometry" />
        </mxCell>

        <!-- UART External Signals -->
        <mxCell id="ar_pc_rx" value="uart_rx_i" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=13.5;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="1530" y="595" as="sourcePoint" />
            <mxPoint x="1355" y="595" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <mxCell id="ar_pc_tx" value="uart_tx_o" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=13.5;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="1220" y="680" as="sourcePoint" />
            <mxPoint x="1530" y="680" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <mxCell id="ar_u_sync_core" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=1.6;strokeColor=#000000;endArrow=classic;endFill=1;" edge="1" parent="1" source="u_sync" target="u_core">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="1230" y="595" />
              <mxPoint x="1230" y="595" />
            </Array>
          </mxGeometry>
        </mxCell>

        <mxCell id="ar_core_fifo" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=1.6;strokeColor=#000000;startArrow=classic;startFill=1;endArrow=classic;endFill=1;" edge="1" parent="1" source="u_fifo" target="u_core" />
        <mxCell id="ar_mmio_fifo" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=1.6;strokeColor=#000000;startArrow=classic;startFill=1;endArrow=classic;endFill=1;" edge="1" parent="1" source="u_mmio" target="u_fifo" />

        <!-- ============================================================= -->
        <!-- 9. SLAVE 4: GPIO MMIO MODULE (rtl/soc_gpio_mmio.v)             -->
        <!-- ============================================================= -->
        <mxCell id="gpio" value="&lt;b style=&quot;font-size:14px;&quot;&gt;SLAVE 4: GPIO MMIO&lt;/b&gt;&lt;br&gt;&lt;b style=&quot;font-size:11.5px;color:#444;&quot;&gt;(rtl/core/soc_gpio_mmio.v)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:12px;font-weight:bold;&quot;&gt;GPIO MMIO Peripheral (0x4000_0000)&lt;/span&gt;&lt;br&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;16-bit LED Driver: Heartbeat (1Hz), Flash Busy, Card Valid&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="475" y="695" width="235" height="115" as="geometry" />
        </mxCell>

        <mxCell id="ar_gpio_led" value="leds_o[15:0]" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=13.5;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="710" y="752" as="sourcePoint" />
            <mxPoint x="1530" y="752" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <!-- ============================================================= -->
        <!-- 10. SYSTEM MEMORY BUS INTERCONNECTIONS                        -->
        <!-- ============================================================= -->
        <!-- Bus <-> SPIMEMIO (Slave 1) -->
        <mxCell id="b_bus_spi" value="sel_spimem" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=4.5;strokeColor=#000000;startArrow=classic;startFill=1;endArrow=classic;endFill=1;fontSize=12;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="475" y="132" as="sourcePoint" />
            <mxPoint x="450" y="132" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <!-- Bus <-> SRAM (Slave 0) -->
        <mxCell id="b_bus_sram" value="sel_sram" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=4.5;strokeColor=#000000;startArrow=classic;startFill=1;endArrow=classic;endFill=1;fontSize=12;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="1085" y="132" as="sourcePoint" />
            <mxPoint x="1115" y="132" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <!-- Bus <-> PicoRV32 CPU (Master) -->
        <mxCell id="b_bus_cpu" value="&lt;b style=&quot;font-size:12px;&quot;&gt;CPU Memory Bus (mem_valid, mem_ready, mem_addr, mem_wdata, mem_rdata)&lt;/b&gt;" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=4.5;strokeColor=#000000;startArrow=classic;startFill=1;endArrow=classic;endFill=1;fontSize=12;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="592" y="195" as="sourcePoint" />
            <mxPoint x="592" y="230" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <!-- Bus Trunk to Peripherals (Slave 2, Slave 3, Slave 4) -->
        <mxCell id="b_bus_rfid" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=4.5;strokeColor=#000000;startArrow=classic;startFill=1;endArrow=classic;endFill=1;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="740" y="372" as="sourcePoint" />
            <mxPoint x="785" y="372" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <mxCell id="b_bus_uart" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=4.5;strokeColor=#000000;startArrow=classic;startFill=1;endArrow=classic;endFill=1;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="740" y="642" as="sourcePoint" />
            <mxPoint x="785" y="642" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <mxCell id="b_bus_gpio" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=4.5;strokeColor=#000000;endArrow=classic;endFill=1;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="740" y="735" as="sourcePoint" />
            <mxPoint x="710" y="735" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <!-- ============================================================= -->
        <!-- 11. BOTTOM ARCHITECTURAL SUMMARY BANNER                       -->
        <!-- ============================================================= -->
        <mxCell id="arch_summary" value="&lt;b style=&quot;font-size:13.5px;&quot;&gt;Top-Level Modular SoC Architecture (rtl/rdm6300_picorv32_soc.v)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:11.5px;font-weight:600;&quot;&gt;Khu vực 1: rtl/core/ (CPU, SRAM, Flash, Interconnect, GPIO) | Khu vực 2: rtl/rdm6300/ (RFID MMIO) | Khu vực 3: rtl/host/ (Host UART)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.5;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="475" y="825" width="920" height="50" as="geometry" />
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
    return xml

def generate_svg():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1580 920" width="100%" height="100%" style="background-color: #ffffff; font-family: Arial, Helvetica, sans-serif;">
  <defs>
    <!-- Sharp arrowheads -->
    <marker id="arr_end" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="11" markerHeight="11" markerUnits="userSpaceOnUse" orient="auto">
      <path d="M 1 2 L 10 6 L 1 10 z" fill="#000000" />
    </marker>
    <marker id="arr_start" viewBox="0 0 12 12" refX="2" refY="6" markerWidth="11" markerHeight="11" markerUnits="userSpaceOnUse" orient="auto">
      <path d="M 10 2 L 1 6 L 10 10 z" fill="#000000" />
    </marker>

    <!-- Thick Bus Arrowheads -->
    <marker id="bus_head_end" viewBox="0 0 14 14" refX="12" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto">
      <path d="M 1 1.5 L 12 7 L 1 12.5 z" fill="#000000" />
    </marker>
    <marker id="bus_head_start" viewBox="0 0 14 14" refX="2" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto">
      <path d="M 12 1.5 L 1 7 L 12 12.5 z" fill="#000000" />
    </marker>
  </defs>

  <!-- ===================================================================== -->
  <!-- 1. CHIP BOUNDARY (ASIC)                                               -->
  <!-- ===================================================================== -->
  <rect x="250" y="25" width="1290" height="865" fill="#ffffff" stroke="#000000" stroke-width="2.5" />
  <text x="280" y="58" font-size="21" font-weight="bold" fill="#000000">rdm6300_picorv32_soc (Top-Level ASIC Chip - rtl/rdm6300_picorv32_soc.v)</text>

  <!-- Global Clock and Reset Inputs -->
  <g stroke="#000000" stroke-width="1.8" fill="none">
    <path d="M 140 85 L 275 85" marker-end="url(#arr_end)" />
    <path d="M 140 125 L 275 125" marker-end="url(#arr_end)" />
  </g>
  <text x="207" y="78" font-size="13" font-weight="bold" fill="#000000" text-anchor="middle">clk_i (50 MHz)</text>
  <text x="207" y="118" font-size="13" font-weight="bold" fill="#000000" text-anchor="middle">rst_n_i</text>

  <!-- ===================================================================== -->
  <!-- 2. EXTERNAL SPI FLASH (OFF-CHIP)                                      -->
  <!-- ===================================================================== -->
  <rect x="25" y="260" width="155" height="320" fill="#ffffff" stroke="#000000" stroke-width="2" />
  <text x="102" y="325" font-size="17" font-weight="bold" fill="#000000" text-anchor="middle">External</text>
  <text x="102" y="350" font-size="17" font-weight="bold" fill="#000000" text-anchor="middle">SPI Flash</text>
  <text x="102" y="375" font-size="16" font-weight="bold" fill="#000000" text-anchor="middle">(Off-Chip)</text>
  <text x="102" y="415" font-size="14" fill="#000000" text-anchor="middle">- Firmware</text>
  <text x="102" y="435" font-size="14" fill="#000000" text-anchor="middle">Storage</text>
  <text x="102" y="455" font-size="13" fill="#444444" text-anchor="middle">(W25Q128)</text>

  <!-- Flash Connection Wires -->
  <g stroke="#000000" stroke-width="1.8" fill="none">
    <path d="M 180 330 L 275 330" marker-end="url(#arr_end)" />
    <path d="M 180 420 L 275 420" marker-end="url(#arr_end)" />
    <path d="M 180 510 L 275 510" marker-start="url(#arr_start)" marker-end="url(#arr_end)" />
  </g>
  <text x="227" y="318" font-size="14" font-weight="bold" fill="#000000" text-anchor="middle">flash_csb</text>
  <text x="227" y="408" font-size="14" font-weight="bold" fill="#000000" text-anchor="middle">flash_clk</text>
  <text x="227" y="498" font-size="14" font-weight="bold" fill="#000000" text-anchor="middle">flash_io[3:0]</text>

  <!-- ===================================================================== -->
  <!-- 3. SLAVE 1: SPIMEMIO FLASH CONTROLLER                                 -->
  <!-- ===================================================================== -->
  <rect x="275" y="75" width="175" height="735" fill="#ffffff" stroke="#000000" stroke-width="2" />
  <text x="362" y="340" font-size="17" font-weight="bold" fill="#000000" text-anchor="middle">SLAVE 1:</text>
  <text x="362" y="365" font-size="18" font-weight="bold" fill="#000000" text-anchor="middle">SPIMEMIO</text>
  <text x="362" y="390" font-size="18" font-weight="bold" fill="#000000" text-anchor="middle">Flash</text>
  <text x="362" y="415" font-size="18" font-weight="bold" fill="#000000" text-anchor="middle">Controller</text>
  <text x="362" y="450" font-size="15" font-weight="bold" fill="#000000" text-anchor="middle">(rtl/core/spimemio.v)</text>
  <text x="362" y="490" font-size="14" fill="#222222" text-anchor="middle">0x0010_0000 -</text>
  <text x="362" y="512" font-size="14" fill="#222222" text-anchor="middle">0x00FF_FFFF</text>
  <text x="362" y="555" font-size="13" fill="#444444" text-anchor="middle">(XIP Read &amp;</text>
  <text x="362" y="573" font-size="13" fill="#444444" text-anchor="middle">SPI Bit-Bang</text>
  <text x="362" y="591" font-size="13" fill="#444444" text-anchor="middle">0x0200_0000)</text>

  <!-- ===================================================================== -->
  <!-- 4. BUS: CENTRAL MEMORY BUS INTERCONNECT (soc_interconnect.v)          -->
  <!-- ===================================================================== -->
  <rect x="475" y="75" width="610" height="120" fill="#ffffff" stroke="#000000" stroke-width="2.5" />
  <text x="780" y="105" font-size="17" font-weight="bold" fill="#000000" text-anchor="middle">Internal Memory Bus Interconnect (rtl/core/soc_interconnect.v)</text>
  <text x="780" y="128" font-size="13.5" font-weight="bold" fill="#222222" text-anchor="middle">MMIO Address Decoder &amp; Bus Multiplexer (1 Master ➔ 5 Dedicated Slaves)</text>
  <line x1="495" y1="140" x2="1065" y2="140" stroke="#888888" stroke-width="1" />
  <!-- Left column -->
  <text x="500" y="160" font-size="10.5" font-weight="bold" fill="#000000">• S0: rtl/core/data_sram.v (0x0000_0000)</text>
  <text x="500" y="180" font-size="10.5" font-weight="bold" fill="#000000">• S1: rtl/core/spimemio.v (0x0010_0000)</text>
  <!-- Right column -->
  <text x="785" y="155" font-size="10.5" font-weight="bold" fill="#000000">• S2: rtl/rdm6300/rdm6300_mmio.v (0x1000_0000)</text>
  <text x="785" y="172" font-size="10.5" font-weight="bold" fill="#000000">• S3: rtl/host/host_uart_mmio.v (0x3000_0000)</text>
  <text x="785" y="189" font-size="10.5" font-weight="bold" fill="#000000">• S4: rtl/core/soc_gpio_mmio.v (0x4000_0000)</text>

  <!-- ===================================================================== -->
  <!-- 5. SLAVE 0: 1KB DATA SRAM                                             -->
  <!-- ===================================================================== -->
  <rect x="1115" y="75" width="225" height="135" fill="#ffffff" stroke="#000000" stroke-width="2" />
  <text x="1227" y="112" font-size="17" font-weight="bold" fill="#000000" text-anchor="middle">SLAVE 0: 1KB Data SRAM</text>
  <text x="1227" y="138" font-size="15" font-weight="bold" fill="#000000" text-anchor="middle">(rtl/core/data_sram.v)</text>
  <text x="1227" y="165" font-size="14" fill="#000000" text-anchor="middle">0x0000_0000</text>
  <text x="1227" y="192" font-size="13" fill="#333333" text-anchor="middle">(Stack &amp; Variables)</text>

  <!-- ===================================================================== -->
  <!-- 6. MASTER: PICORV32 RISC-V CPU CORE                                   -->
  <!-- ===================================================================== -->
  <rect x="475" y="230" width="235" height="440" fill="#ffffff" stroke="#000000" stroke-width="2" />
  <text x="592" y="265" font-size="18" font-weight="bold" fill="#000000" text-anchor="middle">MASTER:</text>
  <text x="592" y="292" font-size="19" font-weight="bold" fill="#000000" text-anchor="middle">PicoRV32 RISC-V CPU</text>
  <text x="592" y="318" font-size="15" font-weight="bold" fill="#000000" text-anchor="middle">(rtl/core/picorv32.v)</text>

  <line x1="500" y1="345" x2="685" y2="345" stroke="#000000" stroke-width="1.2" />

  <text x="592" y="380" font-size="14" font-weight="bold" fill="#000000" text-anchor="middle">(C Firmware Execution -</text>
  <text x="592" y="402" font-size="14" font-weight="bold" fill="#000000" text-anchor="middle">firmware/main.c)</text>

  <text x="592" y="455" font-size="13" fill="#222222" text-anchor="middle">RV32I Core (32 Registers)</text>
  <text x="592" y="485" font-size="13" fill="#222222" text-anchor="middle">PC Reset: 0x0025_0000 (Flash)</text>
  <text x="592" y="515" font-size="13" fill="#222222" text-anchor="middle">Stack Pointer: 0x0000_0400 (SRAM)</text>
  <text x="592" y="545" font-size="13" fill="#222222" text-anchor="middle">Native 32-bit Memory Bus</text>

  <!-- ===================================================================== -->
  <!-- 7. SLAVE 2: RDM6300 RFID MMIO MODULE (rtl/rdm6300_mmio.v)             -->
  <!-- ===================================================================== -->
  <rect x="770" y="230" width="625" height="245" fill="#ffffff" stroke="#000000" stroke-width="2.2" />
  <rect x="770" y="230" width="625" height="42" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
  <text x="1082" y="250" font-size="16" font-weight="bold" fill="#000000" text-anchor="middle">SLAVE 2: rtl/rdm6300/rdm6300_mmio.v (RFID MMIO Peripheral Module)</text>
  <text x="1082" y="266" font-size="12" font-weight="bold" fill="#333333" text-anchor="middle">MMIO Address: 0x1000_0000 - 0x1000_0008 | Bus Select: sel_rfid</text>

  <!-- RFID Submodules -->
  <rect x="785" y="285" width="130" height="175" fill="#ffffff" stroke="#000000" stroke-width="1.6" />
  <text x="850" y="320" font-size="14.5" font-weight="bold" fill="#000000" text-anchor="middle">MMIO Registers</text>
  <text x="850" y="338" font-size="11" font-weight="bold" fill="#444444" text-anchor="middle">(in rdm6300_mmio.v)</text>
  <line x1="795" y1="350" x2="905" y2="350" stroke="#aaaaaa" />
  <text x="850" y="375" font-size="11.5" fill="#222222" text-anchor="middle">STATUS (0x0)</text>
  <text x="850" y="395" font-size="11.5" fill="#222222" text-anchor="middle">TAG_HI (0x4)</text>
  <text x="850" y="415" font-size="11.5" fill="#222222" text-anchor="middle">TAG_LO (0x8)</text>
  <text x="850" y="445" font-size="11.5" font-weight="bold" fill="#000000" text-anchor="middle">card_valid_o</text>

  <rect x="930" y="285" width="145" height="175" fill="#ffffff" stroke="#000000" stroke-width="1.6" />
  <text x="1002" y="325" font-size="14" font-weight="bold" fill="#000000" text-anchor="middle">rdm6300_</text>
  <text x="1002" y="345" font-size="14" font-weight="bold" fill="#000000" text-anchor="middle">frame_decoder</text>
  <text x="1002" y="365" font-size="11" font-weight="bold" fill="#444444" text-anchor="middle">(frame_decoder.v)</text>
  <line x1="945" y1="375" x2="1060" y2="375" stroke="#aaaaaa" />
  <text x="1002" y="400" font-size="11" fill="#333333" text-anchor="middle">14-Byte ASCII Frame</text>
  <text x="1002" y="420" font-size="11" fill="#333333" text-anchor="middle">1-Cycle XOR Check</text>
  <text x="1002" y="440" font-size="11" fill="#333333" text-anchor="middle">Watchdog 10ms</text>

  <rect x="1090" y="285" width="115" height="175" fill="#ffffff" stroke="#000000" stroke-width="1.6" />
  <text x="1147" y="325" font-size="14.5" font-weight="bold" fill="#000000" text-anchor="middle">uart_rx</text>
  <text x="1147" y="345" font-size="9.5" font-weight="bold" fill="#444444" text-anchor="middle">(rtl/rdm6300/uart_rx.v)</text>
  <line x1="1105" y1="365" x2="1190" y2="365" stroke="#aaaaaa" />
  <text x="1147" y="395" font-size="11.5" fill="#333333" text-anchor="middle">9600 Baud</text>
  <text x="1147" y="415" font-size="11.5" fill="#333333" text-anchor="middle">8-N-1 UART</text>
  <text x="1147" y="435" font-size="11.5" fill="#333333" text-anchor="middle">Majority Sampler</text>

  <rect x="1220" y="285" width="130" height="175" fill="#ffffff" stroke="#000000" stroke-width="1.6" />
  <text x="1285" y="325" font-size="14.5" font-weight="bold" fill="#000000" text-anchor="middle">sync_2ff</text>
  <text x="1285" y="345" font-size="9.5" font-weight="bold" fill="#444444" text-anchor="middle">(rtl/core/sync_2ff.v)</text>
  <line x1="1235" y1="365" x2="1335" y2="365" stroke="#aaaaaa" />
  <text x="1285" y="395" font-size="11.5" fill="#333333" text-anchor="middle">2-FF CDC</text>
  <text x="1285" y="415" font-size="11.5" fill="#333333" text-anchor="middle">Synchronizer</text>
  <text x="1285" y="435" font-size="11.5" fill="#333333" text-anchor="middle">MTBF &gt; 1000 Yrs</text>

  <!-- RFID Signal Connections -->
  <g stroke="#000000" stroke-width="1.8" fill="none">
    <path d="M 1530 372 L 1350 372" marker-end="url(#arr_end)" />
    <path d="M 1220 372 L 1205 372" marker-end="url(#arr_end)" />
    <path d="M 1090 372 L 1075 372" marker-end="url(#arr_end)" />
    <path d="M 930 372 L 915 372" marker-end="url(#arr_end)" />
  </g>
  <rect x="1385" y="347" width="125" height="25" fill="#ffffff" stroke="#000000" stroke-width="1.2" />
  <text x="1447" y="364" font-size="13" font-weight="bold" fill="#000000" text-anchor="middle">rdm6300_rx_i</text>

  <!-- ============================================================= -->
  <!-- 8. SLAVE 3: HOST PC UART MMIO MODULE (rtl/host_uart_mmio.v)    -->
  <!-- ============================================================= -->
  <rect x="770" y="500" width="625" height="245" fill="#ffffff" stroke="#000000" stroke-width="2.2" />
  <rect x="770" y="500" width="625" height="42" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
  <text x="1082" y="520" font-size="16" font-weight="bold" fill="#000000" text-anchor="middle">SLAVE 3: rtl/host/host_uart_mmio.v (Host PC UART MMIO Peripheral Module)</text>
  <text x="1082" y="536" font-size="12" font-weight="bold" fill="#333333" text-anchor="middle">MMIO Address: 0x3000_0000 - 0x3000_0004 | Bus Select: sel_uart</text>

  <!-- UART Submodules -->
  <rect x="785" y="555" width="130" height="175" fill="#ffffff" stroke="#000000" stroke-width="1.6" />
  <text x="850" y="590" font-size="14.5" font-weight="bold" fill="#000000" text-anchor="middle">UART MMIO</text>
  <text x="850" y="608" font-size="11" font-weight="bold" fill="#444444" text-anchor="middle">(in host_uart_mmio.v)</text>
  <line x1="795" y1="620" x2="905" y2="620" stroke="#aaaaaa" />
  <text x="850" y="645" font-size="11.5" fill="#222222" text-anchor="middle">DIV (0x3000_0000)</text>
  <text x="850" y="665" font-size="11.5" fill="#222222" text-anchor="middle">DAT (0x3000_0004)</text>
  <text x="850" y="695" font-size="11" fill="#333333" text-anchor="middle">FIFO Control</text>
  <text x="850" y="715" font-size="11" fill="#333333" text-anchor="middle">1-Cycle Ready</text>

  <rect x="930" y="555" width="135" height="175" fill="#ffffff" stroke="#000000" stroke-width="1.6" />
  <text x="997" y="595" font-size="14.5" font-weight="bold" fill="#000000" text-anchor="middle">sync_fifo (x2)</text>
  <text x="997" y="615" font-size="9.5" font-weight="bold" fill="#444444" text-anchor="middle">(rtl/host/sync_fifo.v)</text>
  <line x1="945" y1="628" x2="1050" y2="628" stroke="#aaaaaa" />
  <text x="997" y="655" font-size="11.5" fill="#333333" text-anchor="middle">32-Byte RX FIFO</text>
  <text x="997" y="675" font-size="11.5" fill="#333333" text-anchor="middle">32-Byte TX FIFO</text>
  <text x="997" y="705" font-size="11.5" font-weight="bold" fill="#000000" text-anchor="middle">Zero Packet Drop</text>

  <rect x="1080" y="555" width="140" height="175" fill="#ffffff" stroke="#000000" stroke-width="1.6" />
  <text x="1150" y="595" font-size="14.5" font-weight="bold" fill="#000000" text-anchor="middle">simpleuart</text>
  <text x="1150" y="615" font-size="9.5" font-weight="bold" fill="#444444" text-anchor="middle">(rtl/host/simpleuart.v)</text>
  <line x1="1095" y1="628" x2="1205" y2="628" stroke="#aaaaaa" />
  <text x="1150" y="655" font-size="11.5" fill="#333333" text-anchor="middle">Full-Duplex UART</text>
  <text x="1150" y="675" font-size="11.5" fill="#333333" text-anchor="middle">TX / RX Core</text>
  <text x="1150" y="705" font-size="11.5" fill="#333333" text-anchor="middle">Baud Divisor 5208</text>

  <rect x="1235" y="555" width="120" height="80" fill="#ffffff" stroke="#000000" stroke-width="1.6" />
  <text x="1295" y="588" font-size="14" font-weight="bold" fill="#000000" text-anchor="middle">sync_2ff</text>
  <text x="1295" y="608" font-size="9.5" fill="#444444" text-anchor="middle">(rtl/core/sync_2ff.v)</text>
  <text x="1295" y="624" font-size="10.5" fill="#444444" text-anchor="middle">CDC Sync</text>

  <!-- UART Internal & External Signal Lines -->
  <g stroke="#000000" stroke-width="1.8" fill="none">
    <path d="M 1530 595 L 1355 595" marker-end="url(#arr_end)" />
    <path d="M 1235 595 L 1220 595" marker-end="url(#arr_end)" />
    <path d="M 915 642 L 930 642" marker-start="url(#arr_start)" marker-end="url(#arr_end)" />
    <path d="M 1065 642 L 1080 642" marker-start="url(#arr_start)" marker-end="url(#arr_end)" />
    <path d="M 1220 680 L 1530 680" marker-end="url(#arr_end)" />
  </g>
  <rect x="1395" y="570" width="105" height="25" fill="#ffffff" stroke="#000000" stroke-width="1.2" />
  <text x="1447" y="587" font-size="13" font-weight="bold" fill="#000000" text-anchor="middle">uart_rx_i</text>
  <rect x="1395" y="655" width="105" height="25" fill="#ffffff" stroke="#000000" stroke-width="1.2" />
  <text x="1447" y="672" font-size="13" font-weight="bold" fill="#000000" text-anchor="middle">uart_tx_o</text>

  <!-- ============================================================= -->
  <!-- 9. SLAVE 4: GPIO MMIO MODULE (rtl/soc_gpio_mmio.v)             -->
  <!-- ============================================================= -->
  <rect x="475" y="695" width="235" height="115" fill="#ffffff" stroke="#000000" stroke-width="2" />
  <text x="592" y="722" font-size="14" font-weight="bold" fill="#000000" text-anchor="middle">SLAVE 4: GPIO MMIO</text>
  <text x="592" y="738" font-size="11" font-weight="bold" fill="#444444" text-anchor="middle">(rtl/core/soc_gpio_mmio.v)</text>
  <text x="592" y="755" font-size="11" font-weight="bold" fill="#000000" text-anchor="middle">0x4000_0000 (16-bit LED Driver)</text>
  <line x1="495" y1="763" x2="690" y2="763" stroke="#aaaaaa" />
  <text x="592" y="780" font-size="10.5" fill="#222222" text-anchor="middle">16-bit Output Driver</text>
  <text x="592" y="798" font-size="10" fill="#444444" text-anchor="middle">Heartbeat (1Hz), Flash Busy, Card Valid</text>

  <!-- leds_o[15:0] -->
  <path d="M 710 752 L 1530 752" stroke="#000000" stroke-width="1.8" fill="none" marker-end="url(#arr_end)" />
  <rect x="1390" y="729" width="115" height="25" fill="#ffffff" stroke="#000000" stroke-width="1.2" />
  <text x="1447" y="746" font-size="13" font-weight="bold" fill="#000000" text-anchor="middle">leds_o[15:0]</text>

  <!-- ============================================================= -->
  <!-- 10. SYSTEM MEMORY BUS INTERCONNECTIONS (THICK SOLID BLACK ARROWS) -->
  <!-- ============================================================= -->
  <!-- Bus <-> SPIMEMIO (Slave 1) -->
  <path d="M 475 132 L 450 132" stroke="#000000" stroke-width="4.5" fill="none" marker-start="url(#bus_head_start)" marker-end="url(#bus_head_end)" />

  <!-- Bus <-> 1KB SRAM (Slave 0) -->
  <path d="M 1085 132 L 1115 132" stroke="#000000" stroke-width="4.5" fill="none" marker-start="url(#bus_head_start)" marker-end="url(#bus_head_end)" />

  <!-- Bus <-> PicoRV32 CPU (Master) -->
  <path d="M 592 195 L 592 230" stroke="#000000" stroke-width="4.5" fill="none" marker-start="url(#bus_head_start)" marker-end="url(#bus_head_end)" />
  <rect x="507" y="203" width="170" height="20" fill="#ffffff" stroke="#000000" stroke-width="1" />
  <text x="592" y="217" font-size="11" font-weight="bold" fill="#000000" text-anchor="middle">CPU Memory Bus (MMIO)</text>

  <!-- Bus Trunk from Interconnect to Peripherals (Vertical Bus Backbone) -->
  <path d="M 740 195 L 740 735" stroke="#000000" stroke-width="4.5" fill="none" />
  <!-- Branch to RFID Subsystem (Slave 2) -->
  <path d="M 740 372 L 785 372" stroke="#000000" stroke-width="4.5" fill="none" marker-end="url(#bus_head_end)" />

  <!-- Branch to Host PC UART Subsystem (Slave 3) -->
  <path d="M 740 642 L 785 642" stroke="#000000" stroke-width="4.5" fill="none" marker-end="url(#bus_head_end)" />

  <!-- Branch to GPIO Status LEDs (Slave 4) -->
  <path d="M 740 735 L 710 735" stroke="#000000" stroke-width="4.5" fill="none" marker-end="url(#bus_head_end)" />

  <!-- Corner junction dots on Bus Backbone -->
  <circle cx="740" cy="195" r="4.5" fill="#000000" />
  <circle cx="740" cy="372" r="4.5" fill="#000000" />
  <circle cx="740" cy="642" r="4.5" fill="#000000" />
  <circle cx="740" cy="735" r="4.5" fill="#000000" />

  <!-- ============================================================= -->
  <!-- 11. BOTTOM ARCHITECTURAL SUMMARY BANNER                               -->
  <!-- ============================================================= -->
  <rect x="475" y="825" width="920" height="50" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
  <text x="935" y="846" font-size="13.5" font-weight="bold" fill="#000000" text-anchor="middle">Top-Level Modular SoC Architecture (rtl/rdm6300_picorv32_soc.v)</text>
  <text x="935" y="865" font-size="11.5" font-weight="bold" fill="#222222" text-anchor="middle">Khu vực 1: rtl/core/ (CPU, SRAM, Flash, Interconnect, GPIO) | Khu vực 2: rtl/rdm6300/ (RFID MMIO) | Khu vực 3: rtl/host/ (Host UART)</text>

</svg>
'''
    return svg

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    # 1. Generate Draw.io XML file (.drawio) in temp folders
    drawio_content = create_drawio_xml()
    drawio_path = os.path.join(root_dir, "document", "temp", "rdm6300_picorv32_soc_complete_diagram.drawio")
    with open(drawio_path, "w", encoding="utf-8") as f:
        f.write(drawio_content)
    # Also save as fig1_block_diagram.drawio in temp folders
    shutil.copyfile(drawio_path, os.path.join(root_dir, "document", "temp", "fig1_block_diagram.drawio"))
    shutil.copyfile(drawio_path, os.path.join(root_dir, "temp", "fig1_block_diagram.drawio"))
    shutil.copyfile(drawio_path, os.path.join(root_dir, "temp", "rdm6300_picorv32_soc_complete_diagram.drawio"))
    print(f"[SUCCESS] Wrote B&W Draw.io XML to: {drawio_path}")

    # 2. Generate Vector SVG file (.svg) in temp folders
    svg_content = generate_svg()
    svg_path = os.path.join(root_dir, "document", "temp", "rdm6300_picorv32_soc_complete_diagram.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    shutil.copyfile(svg_path, os.path.join(root_dir, "temp", "rdm6300_picorv32_soc_complete_diagram.svg"))
    print(f"[SUCCESS] Wrote B&W SVG to: {svg_path}")

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
    width: 1580px;
    height: 920px;
  }}
  .diagram-container {{
    width: 1580px;
    height: 920px;
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
    html_path = os.path.join(root_dir, "document", "temp", "render_diagram.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # 4. Render High-Resolution PNG via Headless Chrome (2x retina)
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    png_path = os.path.join(root_dir, "document", "temp", "fig1_block_diagram.png")
    
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--force-device-scale-factor=2",
        f"--screenshot={png_path}",
        "--window-size=1580,920",
        f"file:///{html_path.replace(os.sep, '/')}"
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(png_path):
        size = os.path.getsize(png_path)
        print(f"[SUCCESS] Rendered PNG via Headless Chrome: {png_path} ({size} bytes)")
    else:
        print(f"[ERROR] Chrome screenshot failed: {res.stderr}")

    # 5. Distribute PNG to all document locations
    shutil.copyfile(png_path, os.path.join(root_dir, "document", "fig1_block_diagram.png"))
    shutil.copyfile(png_path, os.path.join(root_dir, "fig1_block_diagram.png"))

    # 6. Copy to Brain Artifacts directory
    art_path = r"C:\Users\thait\.gemini\antigravity-ide\brain\40d01579-3c16-4b85-9b12-c0e7d33bcd21\fig1_soc_block_diagram.png"
    if os.path.exists(png_path):
        shutil.copyfile(png_path, art_path)
        print(f"[SUCCESS] Copied to Artifacts: {art_path}")

if __name__ == "__main__":
    main()
