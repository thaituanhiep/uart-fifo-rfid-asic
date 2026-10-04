# -*- coding: utf-8 -*-
"""
Script: generate_drawio_bnw_diagram.py
Generates the authentic Draw.io Black & White schematic block diagram:
- Master: PicoRV32 RISC-V CPU Core (rtl/core/picorv32.v) with configuration parameters
- Bus: Interconnect & Decoder (rtl/core/soc_interconnect.v) with explicit decoding logic
- Slave 0: 1KB Data SRAM (rtl/core/data_sram.v) with parameters
- Slave 1: SPIMEMIO Flash Controller (rtl/core/spimemio.v) with XIP & bit-bang settings
- Slave 2 & 3: Dual UART MMIO (rtl/uart/uart_mmio.v - u_rfid_uart & u_host_uart)
- Slave 4: GPIO MMIO Module (rtl/core/soc_gpio_mmio.v)

Pure Black & White textbook style, high contrast, clean orthogonal routing.
"""

import os
import subprocess
import shutil

def create_drawio_xml():
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="2026-10-04T08:00:00.000Z" agent="Mozilla/5.0" version="21.0.0" type="device">
  <diagram id="soc_architecture" name="SoC Block Diagram">
    <mxGraphModel dx="1600" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1580" pageHeight="920" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- 1. CHIP BOUNDARY -->
        <mxCell id="chip" value="&lt;b style=&quot;font-size:20px;&quot;&gt;Top-Level ASIC Chip: rdm6300_picorv32_soc (rtl/rdm6300_picorv32_soc.v)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:12px;font-weight:bold;&quot;&gt;SkyWater 130nm ASIC Sign-off (OpenLane 2) / Digilent Basys 3 FPGA Hardware Prototyping Platform&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2.5;verticalAlign=top;align=left;spacingLeft=30;spacingTop=10;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="230" y="20" width="1320" height="875" as="geometry" />
        </mxCell>

        <!-- Global Clock & Reset -->
        <mxCell id="w_clk_in" value="clk_i (50 MHz)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=13;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="120" y="70" as="sourcePoint" />
            <mxPoint x="255" y="70" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <mxCell id="w_rst_in" value="rst_n_i" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=13;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="120" y="110" as="sourcePoint" />
            <mxPoint x="255" y="110" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <!-- 2. EXTERNAL SPI FLASH -->
        <mxCell id="ext_flash" value="&lt;b style=&quot;font-size:17px;&quot;&gt;External&lt;br&gt;SPI Flash&lt;br&gt;(Off-Chip)&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;span style=&quot;font-size:13px;&quot;&gt;W25Q128 / S25FL032P&lt;br&gt;(32 Mbit / 4MB)&lt;br&gt;&lt;br&gt;&lt;b&gt;• 0x0025_0000:&lt;/b&gt; Firmware&lt;br&gt;&lt;b&gt;• 0x0030_0000:&lt;/b&gt; Whitelist&lt;br&gt;&lt;b&gt;• 0x0031_0000:&lt;/b&gt; Logs&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="25" y="270" width="165" height="310" as="geometry" />
        </mxCell>

        <mxCell id="w_csb" value="flash_csb" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=13.5;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="ext_flash" target="spimemio">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="220" y="330" />
              <mxPoint x="220" y="330" />
            </Array>
          </mxGeometry>
        </mxCell>

        <mxCell id="w_clk" value="flash_clk" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=13.5;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="ext_flash" target="spimemio">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="220" y="420" />
              <mxPoint x="220" y="420" />
            </Array>
          </mxGeometry>
        </mxCell>

        <mxCell id="w_io" value="flash_io[3:0]" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#000000;startArrow=classic;startFill=1;endArrow=classic;endFill=1;fontSize=13.5;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="ext_flash" target="spimemio">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="220" y="510" />
              <mxPoint x="220" y="510" />
            </Array>
          </mxGeometry>
        </mxCell>

        <!-- 3. SLAVE 1: SPIMEMIO FLASH CONTROLLER -->
        <mxCell id="spimemio" value="&lt;b style=&quot;font-size:16px;&quot;&gt;SLAVE 1: SPIMEMIO Flash Controller&lt;/b&gt;&lt;br&gt;&lt;b style=&quot;font-size:13.5px;&quot;&gt;(rtl/core/spimemio.v)&lt;/b&gt;&lt;br&gt;&lt;hr style=&quot;border:0.5px solid #000;margin:6px 0;&quot;/&gt;&lt;div style=&quot;text-align:left;padding-left:8px;font-size:12px;line-height:1.4;&quot;&gt;&lt;b&gt;Cấu hình Vùng Nhớ Firmware:&lt;/b&gt;&lt;br/&gt;• &lt;b&gt;XIP Read:&lt;/b&gt; 0x0010_0000 - 0x00FF_FFFF&lt;br/&gt;&amp;nbsp;&amp;nbsp;(&lt;i&gt;sel_spimem = 1&lt;/i&gt;, lấy Opcode trực tiếp)&lt;br/&gt;• &lt;b&gt;SPI Bit-Bang Cfg:&lt;/b&gt; 0x0200_0000&lt;br/&gt;&amp;nbsp;&amp;nbsp;(&lt;i&gt;sel_spicfg = 1&lt;/i&gt;, Ghi/Xóa từ SRAM)&lt;br/&gt;• &lt;b&gt;Giao tiếp SPI:&lt;/b&gt; CSB, CLK, IO[3:0]&lt;br/&gt;• &lt;b&gt;Phản hồi:&lt;/b&gt; spimem_ready (sau 4B SPI)&lt;/div&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontFamily=Arial,Helvetica,sans-serif;verticalAlign=top;spacingTop=10;" vertex="1" parent="1">
          <mxGeometry x="255" y="95" width="225" height="705" as="geometry" />
        </mxCell>

        <!-- 4. BUS: CENTRAL INTERCONNECT & DECODER LOGIC -->
        <mxCell id="bus" value="&lt;b style=&quot;font-size:16.5px;&quot;&gt;BUS INTERCONNECT &amp;amp; DECODER LOGIC (rtl/core/soc_interconnect.v)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:12.5px;font-weight:bold;&quot;&gt;Logic Giải Mã Địa Chỉ C &amp;amp; Ghép Kênh Bus Tập Trung (1 Master ➔ 5 Dedicated Slaves)&lt;/span&gt;&lt;br&gt;&lt;hr style=&quot;border:0.5px solid #000;margin:4px 0;&quot;/&gt;&lt;div style=&quot;text-align:left;padding-left:14px;font-size:11.5px;font-family:Consolas,monospace;line-height:1.35;&quot;&gt;&lt;b&gt;assign sel_sram&amp;nbsp;&amp;nbsp;&amp;nbsp;= cpu_mem_valid &amp;amp;&amp;amp; (cpu_mem_addr &amp;lt; 32'h0000_0400);&lt;/b&gt;&lt;br/&gt;&lt;b&gt;assign sel_spimem = cpu_mem_valid &amp;amp;&amp;amp; (cpu_mem_addr &amp;gt;= 32'h0010_0000 &amp;amp;&amp;amp; cpu_mem_addr &amp;lt; 32'h0100_0000);&lt;/b&gt;&lt;br/&gt;&lt;b&gt;assign sel_spicfg = cpu_mem_valid &amp;amp;&amp;amp; (cpu_mem_addr == 32'h0200_0000);&lt;/b&gt;&lt;br/&gt;&lt;b&gt;assign sel_rfid&amp;nbsp;&amp;nbsp;&amp;nbsp;= cpu_mem_valid &amp;amp;&amp;amp; (cpu_mem_addr[31:28] == 4'h1);&lt;/b&gt;&amp;nbsp;&amp;nbsp;// 0x1000_0000&lt;br/&gt;&lt;b&gt;assign sel_uart&amp;nbsp;&amp;nbsp;&amp;nbsp;= cpu_mem_valid &amp;amp;&amp;amp; (cpu_mem_addr[31:28] == 4'h3);&lt;/b&gt;&amp;nbsp;&amp;nbsp;// 0x3000_0000&lt;br/&gt;&lt;b&gt;assign sel_gpio&amp;nbsp;&amp;nbsp;&amp;nbsp;= cpu_mem_valid &amp;amp;&amp;amp; (cpu_mem_addr[31:28] == 4'h4);&lt;/b&gt;&amp;nbsp;&amp;nbsp;// 0x4000_0000&lt;br/&gt;assign cpu_mem_rdata = sel_sram ? sram_rdata : sel_spimem ? spimem_rdata : sel_rfid ? rfid_rdata : sel_uart ? uart_rdata : gpio_rdata;&lt;br/&gt;assign cpu_mem_ready = sel_sram ? sram_ready : sel_spimem ? spimem_ready : sel_rfid ? rfid_ready : sel_uart ? uart_ready : gpio_ready;&lt;/div&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2.5;fontFamily=Arial,Helvetica,sans-serif;verticalAlign=top;spacingTop=8;" vertex="1" parent="1">
          <mxGeometry x="510" y="95" width="670" height="195" as="geometry" />
        </mxCell>

        <!-- 5. SLAVE 0: 1KB DATA SRAM -->
        <mxCell id="sram" value="&lt;b style=&quot;font-size:16px;&quot;&gt;SLAVE 0: 1KB Data SRAM&lt;/b&gt;&lt;br&gt;&lt;b style=&quot;font-size:13.5px;&quot;&gt;(rtl/core/data_sram.v)&lt;/b&gt;&lt;br&gt;&lt;hr style=&quot;border:0.5px solid #000;margin:4px 0;&quot;/&gt;&lt;div style=&quot;text-align:left;padding-left:8px;font-size:11.5px;line-height:1.35;&quot;&gt;• &lt;b&gt;Tham số:&lt;/b&gt; WORDS = 256 (32-bit)&lt;br/&gt;• &lt;b&gt;Vùng địa chỉ:&lt;/b&gt; &amp;lt; 0x0000_0400&lt;br/&gt;• &lt;b&gt;Địa chỉ từ CPU:&lt;/b&gt; addr[9:2]&lt;br/&gt;• &lt;b&gt;Phản hồi:&lt;/b&gt; sram_ready = 1 (1 clock)&lt;br/&gt;• &lt;b&gt;Vai trò C:&lt;/b&gt; Stack &lt;i&gt;sp = 0x400&lt;/i&gt;,&lt;br/&gt;&amp;nbsp;&amp;nbsp;vùng biến .data / .bss &amp;amp; đệm flashio&lt;/div&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontFamily=Arial,Helvetica,sans-serif;verticalAlign=top;spacingTop=8;" vertex="1" parent="1">
          <mxGeometry x="1215" y="95" width="300" height="195" as="geometry" />
        </mxCell>

        <!-- 6. MASTER: PICORV32 RISC-V CPU CORE -->
        <mxCell id="cpu" value="&lt;b style=&quot;font-size:17.5px;&quot;&gt;MASTER: PicoRV32 RISC-V CPU Core&lt;/b&gt;&lt;br&gt;&lt;b style=&quot;font-size:14px;&quot;&gt;(rtl/core/picorv32.v)&lt;/b&gt;&lt;br&gt;&lt;hr style=&quot;border:0.5px solid #000;margin:6px 0;&quot;/&gt;&lt;div style=&quot;text-align:left;padding-left:12px;font-size:12px;line-height:1.45;&quot;&gt;&lt;b&gt;Cấu hình Chạy Firmware C (Setting RTL):&lt;/b&gt;&lt;br/&gt;• &lt;b&gt;parameter PROGADDR_RESET = 32'h0025_0000;&lt;/b&gt;&lt;br/&gt;&amp;nbsp;&amp;nbsp;&lt;i&gt;(Vector reset Flash SPI XIP để nạp opcode firmware)&lt;/i&gt;&lt;br/&gt;• &lt;b&gt;parameter STACKADDR&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;= 32'h0000_0400;&lt;/b&gt;&lt;br/&gt;&amp;nbsp;&amp;nbsp;&lt;i&gt;(Đỉnh ngăn xếp 1KB SRAM, cấp phát biến &amp;amp; stack frame)&lt;/i&gt;&lt;br/&gt;• &lt;b&gt;Kiến trúc RV32I:&lt;/b&gt; 32 thanh ghi (x0..x31), Freestanding C&lt;br/&gt;&lt;br/&gt;&lt;b&gt;Giao diện Bus Master Chuẩn:&lt;/b&gt;&lt;br/&gt;• output &lt;b&gt;cpu_mem_valid&lt;/b&gt; : Bắt đầu chu kỳ bus&lt;br/&gt;• output [31:0] &lt;b&gt;cpu_mem_addr&lt;/b&gt; : Địa chỉ truy xuất 32-bit&lt;br/&gt;• output [31:0] &lt;b&gt;cpu_mem_wdata&lt;/b&gt;: Dữ liệu ghi ra ngoại vi&lt;br/&gt;• output [3:0]&amp;nbsp;&amp;nbsp;&lt;b&gt;cpu_mem_wstrb&lt;/b&gt;: Mask byte (4'b1111 ghi / 4'b0000 đọc)&lt;br/&gt;• input&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&lt;b&gt;cpu_mem_ready&lt;/b&gt;: Báo hoàn thành chu kỳ bus&lt;br/&gt;• input&amp;nbsp;&amp;nbsp;[31:0] &lt;b&gt;cpu_mem_rdata&lt;/b&gt;: Dữ liệu đọc về CPU&lt;/div&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontFamily=Arial,Helvetica,sans-serif;verticalAlign=top;spacingTop=10;" vertex="1" parent="1">
          <mxGeometry x="510" y="315" width="375" height="375" as="geometry" />
        </mxCell>

        <!-- 7. SLAVE 2: RFID READER UART MMIO -->
        <mxCell id="rfid_uart" value="&lt;b style=&quot;font-size:16px;&quot;&gt;SLAVE 2: RFID Reader UART MMIO&lt;/b&gt;&lt;br&gt;&lt;b style=&quot;font-size:13.5px;&quot;&gt;u_rfid_uart (rtl/uart/uart_mmio.v)&lt;/b&gt;&lt;br&gt;&lt;hr style=&quot;border:0.5px solid #000;margin:6px 0;&quot;/&gt;&lt;div style=&quot;text-align:left;padding-left:10px;font-size:12px;line-height:1.4;&quot;&gt;• &lt;b&gt;Bus Select:&lt;/b&gt; sel_rfid (Địa chỉ tiền tố 4'h1)&lt;br/&gt;• &lt;b&gt;REG_RFID_UART_DIV:&lt;/b&gt; 0x1000_0000 (Baud = 5208)&lt;br/&gt;• &lt;b&gt;REG_RFID_UART_DAT:&lt;/b&gt; 0x1000_0004 (Đọc FIFO 32B)&lt;br/&gt;• &lt;b&gt;Tín hiệu chân ngoại vi:&lt;/b&gt; rdm6300_rx_i (UART 9600 8-N-1)&lt;br/&gt;• &lt;b&gt;Phản hồi Bus:&lt;/b&gt; rfid_ready = 1 (1 chu kỳ clock)&lt;/div&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontFamily=Arial,Helvetica,sans-serif;verticalAlign=top;spacingTop=10;" vertex="1" parent="1">
          <mxGeometry x="915" y="315" width="385" height="170" as="geometry" />
        </mxCell>

        <!-- rdm6300_rx_i Pin Wire -->
        <mxCell id="w_rfid_rx" value="rdm6300_rx_i" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=13.5;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="1530" y="400" as="sourcePoint" />
            <mxPoint x="1300" y="400" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <!-- 8. SLAVE 3: HOST PC UART MMIO -->
        <mxCell id="host_uart" value="&lt;b style=&quot;font-size:16px;&quot;&gt;SLAVE 3: Host PC UART MMIO &amp;amp; FIFOs&lt;/b&gt;&lt;br&gt;&lt;b style=&quot;font-size:13.5px;&quot;&gt;u_host_uart (rtl/uart/uart_mmio.v)&lt;/b&gt;&lt;br&gt;&lt;hr style=&quot;border:0.5px solid #000;margin:6px 0;&quot;/&gt;&lt;div style=&quot;text-align:left;padding-left:10px;font-size:12px;line-height:1.4;&quot;&gt;• &lt;b&gt;Bus Select:&lt;/b&gt; sel_uart (Địa chỉ tiền tố 4'h3)&lt;br/&gt;• &lt;b&gt;REG_PC_UART_DIV:&lt;/b&gt; 0x3000_0000 (Baud = 5208)&lt;br/&gt;• &lt;b&gt;REG_PC_UART_DAT:&lt;/b&gt; 0x3000_0004 (Đọc RX / Ghi TX FIFO 32B)&lt;br/&gt;• &lt;b&gt;Tín hiệu chân ngoại vi:&lt;/b&gt; uart_rx_i &amp;amp; uart_tx_o&lt;br/&gt;• &lt;b&gt;Phản hồi Bus:&lt;/b&gt; uart_ready = 1 (1 chu kỳ clock)&lt;/div&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontFamily=Arial,Helvetica,sans-serif;verticalAlign=top;spacingTop=10;" vertex="1" parent="1">
          <mxGeometry x="915" y="510" width="385" height="180" as="geometry" />
        </mxCell>

        <!-- Host UART Wires -->
        <mxCell id="w_uart_rx" value="uart_rx_i" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=13.5;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="1530" y="565" as="sourcePoint" />
            <mxPoint x="1300" y="565" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <mxCell id="w_uart_tx" value="uart_tx_o" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=13.5;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="1300" y="635" as="sourcePoint" />
            <mxPoint x="1530" y="635" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <!-- 9. SLAVE 4: GPIO MMIO MODULE -->
        <mxCell id="gpio" value="&lt;b style=&quot;font-size:15.5px;&quot;&gt;SLAVE 4: GPIO MMIO Module (rtl/core/soc_gpio_mmio.v)&lt;/b&gt;&lt;br&gt;&lt;div style=&quot;font-size:12px;margin-top:4px;&quot;&gt;&lt;b&gt;Địa chỉ REG_GPIO_LEDS:&lt;/b&gt; 0x4000_0000 (sel_gpio = 1) | &lt;b&gt;Ngõ ra phần cứng:&lt;/b&gt; leds_o[15:0]&lt;br/&gt;Bit 0: Nhịp tim Alive (1Hz) | Bit 1: Cảnh báo Denied | Bit 2: Mở chốt cửa Granted | Bit 3: Flash Busy&lt;/div&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontFamily=Arial,Helvetica,sans-serif;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="510" y="710" width="790" height="90" as="geometry" />
        </mxCell>

        <mxCell id="w_leds" value="leds_o[15:0]" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#000000;endArrow=classic;endFill=1;fontSize=13.5;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="1300" y="755" as="sourcePoint" />
            <mxPoint x="1530" y="755" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <!-- 10. SYSTEM MEMORY BUS INTERCONNECTIONS -->
        <mxCell id="b_bus_spi" value="sel_spimem, sel_spicfg" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=4.5;strokeColor=#000000;startArrow=classic;startFill=1;endArrow=classic;endFill=1;fontSize=12;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="510" y="165" as="sourcePoint" />
            <mxPoint x="480" y="165" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <mxCell id="b_bus_sram" value="sel_sram" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=4.5;strokeColor=#000000;startArrow=classic;startFill=1;endArrow=classic;endFill=1;fontSize=12;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="1180" y="165" as="sourcePoint" />
            <mxPoint x="1215" y="165" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <mxCell id="b_bus_cpu" value="cpu_mem_valid, addr, wdata, wstrb, rdata, ready" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=4.5;strokeColor=#000000;startArrow=classic;startFill=1;endArrow=classic;endFill=1;fontSize=11.5;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="690" y="290" as="sourcePoint" />
            <mxPoint x="690" y="315" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <mxCell id="b_bus_rfid" value="sel_rfid" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=4.5;strokeColor=#000000;startArrow=classic;startFill=1;endArrow=classic;endFill=1;fontSize=12;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="885" y="400" as="sourcePoint" />
            <mxPoint x="915" y="400" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <mxCell id="b_bus_uart" value="sel_uart" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=4.5;strokeColor=#000000;startArrow=classic;startFill=1;endArrow=classic;endFill=1;fontSize=12;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="885" y="600" as="sourcePoint" />
            <mxPoint x="915" y="600" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <mxCell id="b_bus_gpio" value="sel_gpio" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=4.5;strokeColor=#000000;startArrow=classic;startFill=1;endArrow=classic;endFill=1;fontSize=12;fontStyle=1;labelBackgroundColor=#ffffff;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="690" y="690" as="sourcePoint" />
            <mxPoint x="690" y="710" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <!-- 11. BOTTOM ARCHITECTURAL SUMMARY BANNER -->
        <mxCell id="arch_summary" value="&lt;b style=&quot;font-size:13.5px;&quot;&gt;Top-Level Modular SoC Architecture (rtl/rdm6300_picorv32_soc.v)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:11.5px;font-weight:600;&quot;&gt;Liên kết bus trung tâm soc_interconnect.v định tuyến trong suốt: Flash XIP (0x0010_0000), 1KB SRAM (0x0000_0000), RFID UART MMIO (0x1000_0000), Host UART MMIO (0x3000_0000), GPIO MMIO (0x4000_0000)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.5;fontFamily=Arial,Helvetica,sans-serif;" vertex="1" parent="1">
          <mxGeometry x="255" y="820" width="1260" height="50" as="geometry" />
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
    <!-- Arrowheads -->
    <marker id="arr_end" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="11" markerHeight="11" markerUnits="userSpaceOnUse" orient="auto">
      <path d="M 1 2 L 10 6 L 1 10 z" fill="#000000" />
    </marker>
    <marker id="arr_start" viewBox="0 0 12 12" refX="2" refY="6" markerWidth="11" markerHeight="11" markerUnits="userSpaceOnUse" orient="auto">
      <path d="M 10 2 L 1 6 L 10 10 z" fill="#000000" />
    </marker>
    <marker id="bus_head_end" viewBox="0 0 14 14" refX="12" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto">
      <path d="M 1 1.5 L 12 7 L 1 12.5 z" fill="#000000" />
    </marker>
    <marker id="bus_head_start" viewBox="0 0 14 14" refX="2" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto">
      <path d="M 12 1.5 L 1 7 L 12 12.5 z" fill="#000000" />
    </marker>
  </defs>

  <!-- 1. CHIP BOUNDARY -->
  <rect x="230" y="20" width="1320" height="875" fill="#ffffff" stroke="#000000" stroke-width="2.5" />
  <text x="260" y="52" font-size="20" font-weight="bold" fill="#000000">Top-Level ASIC Chip: rdm6300_picorv32_soc (rtl/rdm6300_picorv32_soc.v)</text>
  <text x="260" y="73" font-size="12" font-weight="bold" fill="#333333">SkyWater 130nm ASIC Sign-off (OpenLane 2) / Digilent Basys 3 FPGA Hardware Prototyping Platform</text>

  <!-- Clock & Reset -->
  <g stroke="#000000" stroke-width="1.8" fill="none">
    <path d="M 120 70 L 240 70" marker-end="url(#arr_end)" />
    <path d="M 120 110 L 240 110" marker-end="url(#arr_end)" />
  </g>
  <text x="180" y="63" font-size="12" font-weight="bold" fill="#000000" text-anchor="middle">clk_i (50 MHz)</text>
  <text x="180" y="103" font-size="12" font-weight="bold" fill="#000000" text-anchor="middle">rst_n_i</text>

  <!-- 2. EXTERNAL SPI FLASH -->
  <rect x="20" y="270" width="160" height="310" fill="#ffffff" stroke="#000000" stroke-width="2" />
  <text x="100" y="325" font-size="17" font-weight="bold" fill="#000000" text-anchor="middle">External</text>
  <text x="100" y="350" font-size="17" font-weight="bold" fill="#000000" text-anchor="middle">SPI Flash</text>
  <text x="100" y="375" font-size="16" font-weight="bold" fill="#000000" text-anchor="middle">(Off-Chip)</text>
  <text x="100" y="415" font-size="13" font-weight="bold" fill="#000000" text-anchor="middle">W25Q128 / S25FL032P</text>
  <text x="100" y="435" font-size="12" fill="#444444" text-anchor="middle">(32 Mbit / 4MB)</text>
  <line x1="35" y1="450" x2="165" y2="450" stroke="#000000" stroke-width="1" />
  <text x="35" y="475" font-size="11.5" font-weight="bold" fill="#000000">• 0x0025_0000: Firmware</text>
  <text x="35" y="500" font-size="11.5" font-weight="bold" fill="#000000">• 0x0030_0000: Whitelist</text>
  <text x="35" y="525" font-size="11.5" font-weight="bold" fill="#000000">• 0x0031_0000: Logs</text>

  <!-- Flash Connection Wires -->
  <g stroke="#000000" stroke-width="1.8" fill="none">
    <path d="M 180 330 L 240 330" marker-end="url(#arr_end)" />
    <path d="M 180 420 L 240 420" marker-end="url(#arr_end)" />
    <path d="M 180 510 L 240 510" marker-start="url(#arr_start)" marker-end="url(#arr_end)" />
  </g>
  <text x="210" y="320" font-size="12" font-weight="bold" fill="#000000" text-anchor="middle">flash_csb</text>
  <text x="210" y="410" font-size="12" font-weight="bold" fill="#000000" text-anchor="middle">flash_clk</text>
  <text x="210" y="500" font-size="12" font-weight="bold" fill="#000000" text-anchor="middle">flash_io[3:0]</text>

  <!-- 3. SLAVE 1: SPIMEMIO FLASH CONTROLLER -->
  <rect x="240" y="95" width="220" height="705" fill="#ffffff" stroke="#000000" stroke-width="2" />
  <text x="350" y="128" font-size="16" font-weight="bold" fill="#000000" text-anchor="middle">SLAVE 1: SPIMEMIO</text>
  <text x="350" y="148" font-size="12.5" font-weight="bold" fill="#000000" text-anchor="middle">Flash Controller (spimemio.v)</text>
  <line x1="255" y1="160" x2="445" y2="160" stroke="#000000" stroke-width="1.2" />
  <text x="255" y="195" font-size="13" font-weight="bold" fill="#000000">Cấu hình Vùng Nhớ Firmware:</text>
  <text x="255" y="230" font-size="12.5" font-weight="bold" fill="#000000">• XIP Instruction Fetch:</text>
  <text x="268" y="253" font-size="12" fill="#222222">0x0010_0000 - 0x00FF_FFFF</text>
  <text x="268" y="273" font-size="11.5" font-style="italic" fill="#444444">(sel_spimem = 1, Opcode Flash)</text>
  <text x="255" y="320" font-size="12.5" font-weight="bold" fill="#000000">• SPI Bit-Bang Cfg Reg:</text>
  <text x="268" y="343" font-size="12" fill="#222222">0x0200_0000</text>
  <text x="268" y="363" font-size="11.5" font-style="italic" fill="#444444">(sel_spicfg = 1, Ghi/Xóa từ SRAM)</text>
  <text x="255" y="410" font-size="12.5" font-weight="bold" fill="#000000">• Giao tiếp SPI Physical:</text>
  <text x="268" y="433" font-size="12" fill="#222222">flash_csb, flash_clk, flash_io[3:0]</text>
  <text x="255" y="480" font-size="12.5" font-weight="bold" fill="#000000">• Phản hồi Bus:</text>
  <text x="268" y="503" font-size="12" fill="#222222">spimem_ready (sau 4 byte SPI)</text>

  <!-- 4. BUS: CENTRAL INTERCONNECT & DECODER LOGIC -->
  <rect x="525" y="95" width="650" height="195" fill="#ffffff" stroke="#000000" stroke-width="2.5" />
  <text x="850" y="122" font-size="16.5" font-weight="bold" fill="#000000" text-anchor="middle">BUS INTERCONNECT &amp; DECODER LOGIC (rtl/core/soc_interconnect.v)</text>
  <text x="850" y="142" font-size="12" font-weight="bold" fill="#222222" text-anchor="middle">Logic Giải Mã Địa Chỉ C &amp; Ghép Kênh Bus Tập Trung (1 Master ➔ 5 Dedicated Slaves)</text>
  <line x1="540" y1="152" x2="1160" y2="152" stroke="#000000" stroke-width="1.2" />
  <text x="540" y="172" font-size="11.5" font-family="Consolas,monospace" font-weight="bold" fill="#000000">assign sel_sram   = cpu_mem_valid &amp;&amp; (cpu_mem_addr &lt; 32'h0000_0400);</text>
  <text x="540" y="190" font-size="11.5" font-family="Consolas,monospace" font-weight="bold" fill="#000000">assign sel_spimem = cpu_mem_valid &amp;&amp; (cpu_mem_addr &gt;= 32'h0010_0000 &amp;&amp; cpu_mem_addr &lt; 32'h0100_0000);</text>
  <text x="540" y="208" font-size="11.5" font-family="Consolas,monospace" font-weight="bold" fill="#000000">assign sel_spicfg = cpu_mem_valid &amp;&amp; (cpu_mem_addr == 32'h0200_0000);</text>
  <text x="540" y="226" font-size="11.5" font-family="Consolas,monospace" font-weight="bold" fill="#000000">assign sel_rfid   = cpu_mem_valid &amp;&amp; (cpu_mem_addr[31:28] == 4'h1);  // 0x1000_0000</text>
  <text x="540" y="244" font-size="11.5" font-family="Consolas,monospace" font-weight="bold" fill="#000000">assign sel_uart   = cpu_mem_valid &amp;&amp; (cpu_mem_addr[31:28] == 4'h3);  // 0x3000_0000</text>
  <text x="540" y="262" font-size="11.5" font-family="Consolas,monospace" font-weight="bold" fill="#000000">assign sel_gpio   = cpu_mem_valid &amp;&amp; (cpu_mem_addr[31:28] == 4'h4);  // 0x4000_0000</text>
  <text x="540" y="280" font-size="10.5" font-family="Consolas,monospace" fill="#333333">MUX: cpu_mem_rdata &lt;= sel_sram ? sram_rdata : sel_spimem ? spimem_rdata : ...</text>

  <!-- 5. SLAVE 0: 1KB DATA SRAM -->
  <rect x="1240" y="95" width="280" height="195" fill="#ffffff" stroke="#000000" stroke-width="2" />
  <text x="1380" y="125" font-size="16" font-weight="bold" fill="#000000" text-anchor="middle">SLAVE 0: 1KB Data SRAM</text>
  <text x="1380" y="145" font-size="13.5" font-weight="bold" fill="#000000" text-anchor="middle">(rtl/core/data_sram.v)</text>
  <line x1="1255" y1="155" x2="1505" y2="155" stroke="#000000" stroke-width="1.2" />
  <text x="1255" y="178" font-size="12" font-weight="bold" fill="#000000">• Tham số:</text>
  <text x="1335" y="178" font-size="12" fill="#222222">WORDS = 256 (32-bit)</text>
  <text x="1255" y="200" font-size="12" font-weight="bold" fill="#000000">• Vùng địa chỉ:</text>
  <text x="1345" y="200" font-size="12" fill="#222222">&lt; 0x0000_0400 (1KB)</text>
  <text x="1255" y="222" font-size="12" font-weight="bold" fill="#000000">• Phản hồi:</text>
  <text x="1325" y="222" font-size="12" fill="#222222">sram_ready = 1 (1 clock)</text>
  <text x="1255" y="245" font-size="12" font-weight="bold" fill="#000000">• Vai trò C:</text>
  <text x="1325" y="245" font-size="11.5" fill="#222222">Stack (sp = 0x400),</text>
  <text x="1255" y="265" font-size="11.5" fill="#444444">biến .data / .bss &amp; đệm flashio</text>

  <!-- 6. MASTER: PICORV32 RISC-V CPU CORE -->
  <rect x="525" y="315" width="365" height="375" fill="#ffffff" stroke="#000000" stroke-width="2.5" />
  <text x="707" y="347" font-size="17.5" font-weight="bold" fill="#000000" text-anchor="middle">MASTER: PicoRV32 RISC-V CPU Core</text>
  <text x="707" y="367" font-size="14" font-weight="bold" fill="#000000" text-anchor="middle">(rtl/core/picorv32.v)</text>
  <line x1="540" y1="380" x2="875" y2="380" stroke="#000000" stroke-width="1.2" />
  <text x="540" y="407" font-size="13" font-weight="bold" fill="#000000">Cấu hình Chạy Firmware C (Setting RTL):</text>
  <text x="540" y="435" font-size="12" font-weight="bold" fill="#000000">• parameter PROGADDR_RESET = 32'h0025_0000;</text>
  <text x="555" y="455" font-size="11.5" font-style="italic" fill="#444444">(Vector reset Flash SPI XIP để nạp opcode firmware)</text>
  <text x="540" y="483" font-size="12" font-weight="bold" fill="#000000">• parameter STACKADDR      = 32'h0000_0400;</text>
  <text x="555" y="503" font-size="11.5" font-style="italic" fill="#444444">(Đỉnh ngăn xếp 1KB SRAM, cấp phát biến &amp; stack frame)</text>
  <text x="540" y="530" font-size="12" font-weight="bold" fill="#000000">• Tập lệnh RV32I: 32 thanh ghi (x0..x31), Freestanding C</text>

  <line x1="540" y1="550" x2="875" y2="550" stroke="#aaaaaa" stroke-width="1" />
  <text x="540" y="575" font-size="13" font-weight="bold" fill="#000000">Giao diện Bus Master Chuẩn:</text>
  <text x="540" y="600" font-size="11.5" fill="#222222">• output <tspan font-weight="bold">cpu_mem_valid</tspan> : Bắt đầu chu kỳ bus</text>
  <text x="540" y="620" font-size="11.5" fill="#222222">• output [31:0] <tspan font-weight="bold">cpu_mem_addr</tspan> : Địa chỉ truy xuất 32-bit</text>
  <text x="540" y="640" font-size="11.5" fill="#222222">• output [31:0] <tspan font-weight="bold">cpu_mem_wdata</tspan>: Dữ liệu ghi ra ngoại vi</text>
  <text x="540" y="660" font-size="11.5" fill="#222222">• output [3:0] <tspan font-weight="bold">cpu_mem_wstrb</tspan>: Byte write strobe</text>
  <text x="540" y="680" font-size="11.5" fill="#222222">• input <tspan font-weight="bold">cpu_mem_ready</tspan> &amp; [31:0] <tspan font-weight="bold">cpu_mem_rdata</tspan></text>

  <!-- 7. SLAVE 2: RFID READER UART MMIO -->
  <rect x="930" y="315" width="370" height="170" fill="#ffffff" stroke="#000000" stroke-width="2" />
  <text x="1115" y="343" font-size="16" font-weight="bold" fill="#000000" text-anchor="middle">SLAVE 2: RFID Reader UART MMIO</text>
  <text x="1115" y="363" font-size="13.5" font-weight="bold" fill="#000000" text-anchor="middle">u_rfid_uart (rtl/uart/uart_mmio.v)</text>
  <line x1="945" y1="375" x2="1285" y2="375" stroke="#000000" stroke-width="1.2" />
  <text x="945" y="398" font-size="12" font-weight="bold" fill="#000000">• Bus Select:</text>
  <text x="1030" y="398" font-size="12" fill="#222222">sel_rfid (cpu_mem_addr[31:28] == 4'h1)</text>
  <text x="945" y="420" font-size="12" font-weight="bold" fill="#000000">• REG_RFID_UART_DIV:</text>
  <text x="1095" y="420" font-size="12" fill="#222222">0x1000_0000 (Baud=5208)</text>
  <text x="945" y="442" font-size="12" font-weight="bold" fill="#000000">• REG_RFID_UART_DAT:</text>
  <text x="1095" y="442" font-size="12" fill="#222222">0x1000_0004 (Đọc FIFO 32B)</text>
  <text x="945" y="464" font-size="12" font-weight="bold" fill="#000000">• Chân ngoại vi:</text>
  <text x="1055" y="464" font-size="12" fill="#222222">rdm6300_rx_i (UART 9600 8-N-1)</text>
  <text x="945" y="484" font-size="12" font-weight="bold" fill="#000000">• Phản hồi Bus:</text>
  <text x="1055" y="484" font-size="12" fill="#222222">rfid_ready = 1 (1 chu kỳ clock)</text>

  <!-- rdm6300_rx_i Pin Wire -->
  <path d="M 1530 400 L 1300 400" stroke="#000000" stroke-width="2" fill="none" marker-end="url(#arr_end)" />
  <text x="1415" y="392" font-size="13" font-weight="bold" fill="#000000" text-anchor="middle">rdm6300_rx_i</text>

  <!-- 8. SLAVE 3: HOST PC UART MMIO -->
  <rect x="930" y="510" width="370" height="180" fill="#ffffff" stroke="#000000" stroke-width="2" />
  <text x="1115" y="538" font-size="16" font-weight="bold" fill="#000000" text-anchor="middle">SLAVE 3: Host PC UART MMIO &amp; FIFOs</text>
  <text x="1115" y="558" font-size="13.5" font-weight="bold" fill="#000000" text-anchor="middle">u_host_uart (rtl/uart/uart_mmio.v)</text>
  <line x1="945" y1="568" x2="1285" y2="568" stroke="#000000" stroke-width="1.2" />
  <text x="945" y="590" font-size="12" font-weight="bold" fill="#000000">• Bus Select:</text>
  <text x="1030" y="590" font-size="12" fill="#222222">sel_uart (cpu_mem_addr[31:28] == 4'h3)</text>
  <text x="945" y="612" font-size="12" font-weight="bold" fill="#000000">• REG_PC_UART_DIV:</text>
  <text x="1095" y="612" font-size="12" fill="#222222">0x3000_0000 (Baud=5208)</text>
  <text x="945" y="634" font-size="12" font-weight="bold" fill="#000000">• REG_PC_UART_DAT:</text>
  <text x="1095" y="634" font-size="12" fill="#222222">0x3000_0004 (Đọc RX / Ghi TX)</text>
  <text x="945" y="656" font-size="12" font-weight="bold" fill="#000000">• Chân ngoại vi:</text>
  <text x="1055" y="656" font-size="12" fill="#222222">uart_rx_i &amp; uart_tx_o</text>
  <text x="945" y="678" font-size="12" font-weight="bold" fill="#000000">• Phản hồi Bus:</text>
  <text x="1055" y="678" font-size="12" fill="#222222">uart_ready = 1 (1 chu kỳ clock)</text>

  <!-- Host UART Wires -->
  <g stroke="#000000" stroke-width="2" fill="none">
    <path d="M 1530 565 L 1300 565" marker-end="url(#arr_end)" />
    <path d="M 1300 635 L 1530 635" marker-end="url(#arr_end)" />
  </g>
  <text x="1415" y="557" font-size="13" font-weight="bold" fill="#000000" text-anchor="middle">uart_rx_i</text>
  <text x="1415" y="627" font-size="13" font-weight="bold" fill="#000000" text-anchor="middle">uart_tx_o</text>

  <!-- 9. SLAVE 4: GPIO MMIO MODULE -->
  <rect x="525" y="710" width="775" height="90" fill="#ffffff" stroke="#000000" stroke-width="2" />
  <text x="912" y="738" font-size="15.5" font-weight="bold" fill="#000000" text-anchor="middle">SLAVE 4: GPIO MMIO Module (rtl/core/soc_gpio_mmio.v)</text>
  <text x="912" y="758" font-size="12.5" font-weight="bold" fill="#222222" text-anchor="middle">Địa chỉ REG_GPIO_LEDS: 0x4000_0000 (sel_gpio = 1) | Ngõ ra phần cứng: leds_o[15:0]</text>
  <text x="912" y="782" font-size="11.5" fill="#444444" text-anchor="middle">Bit 0: Nhịp tim Alive (1Hz) | Bit 1: Cảnh báo Denied | Bit 2: Mở chốt cửa Granted | Bit 3: Flash Busy</text>

  <!-- LEDs Wire -->
  <path d="M 1300 755 L 1530 755" stroke="#000000" stroke-width="2" fill="none" marker-end="url(#arr_end)" />
  <text x="1415" y="747" font-size="13" font-weight="bold" fill="#000000" text-anchor="middle">leds_o[15:0]</text>

  <!-- 10. SYSTEM MEMORY BUS INTERCONNECTIONS -->
  <g stroke="#000000" stroke-width="4.5" fill="none">
    <path d="M 525 165 L 460 165" marker-start="url(#bus_head_start)" marker-end="url(#bus_head_end)" />
    <path d="M 1175 165 L 1240 165" marker-start="url(#bus_head_start)" marker-end="url(#bus_head_end)" />
    <path d="M 700 290 L 700 315" marker-start="url(#bus_head_start)" marker-end="url(#bus_head_end)" />
    <path d="M 890 400 L 930 400" marker-start="url(#bus_head_start)" marker-end="url(#bus_head_end)" />
    <path d="M 890 600 L 930 600" marker-start="url(#bus_head_start)" marker-end="url(#bus_head_end)" />
    <path d="M 700 690 L 700 710" marker-end="url(#bus_head_end)" />
  </g>
  <text x="492" y="152" font-size="11" font-weight="bold" fill="#000000" text-anchor="middle">sel_spimem</text>
  <text x="1207" y="152" font-size="11" font-weight="bold" fill="#000000" text-anchor="middle">sel_sram</text>
  <text x="715" y="306" font-size="11" font-weight="bold" fill="#000000" text-anchor="start">cpu_mem_bus</text>
  <text x="910" y="390" font-size="11" font-weight="bold" fill="#000000" text-anchor="middle">sel_rfid</text>
  <text x="910" y="590" font-size="11" font-weight="bold" fill="#000000" text-anchor="middle">sel_uart</text>
  <text x="715" y="703" font-size="11" font-weight="bold" fill="#000000" text-anchor="start">sel_gpio</text>

  <!-- 11. BOTTOM ARCHITECTURAL SUMMARY BANNER -->
  <rect x="255" y="820" width="1260" height="50" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
  <text x="885" y="842" font-size="13" font-weight="bold" fill="#000000" text-anchor="middle">Top-Level Modular SoC Architecture (rtl/rdm6300_picorv32_soc.v)</text>
  <text x="885" y="860" font-size="11.5" font-weight="600" fill="#333333" text-anchor="middle">Liên kết bus trung tâm soc_interconnect.v định tuyến trong suốt: Flash XIP (0x0010_0000), 1KB SRAM (0x0000_0000), RFID UART MMIO (0x1000_0000), Host UART MMIO (0x3000_0000), GPIO MMIO (0x4000_0000)</text>

</svg>'''
    return svg

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    
    # 1. Generate Draw.io XML
    xml_content = create_drawio_xml()
    drawio_path = os.path.join(root_dir, "document", "temp", "rdm6300_picorv32_soc_complete_diagram.drawio")
    with open(drawio_path, "w", encoding="utf-8") as f:
        f.write(xml_content)
    print(f"[SUCCESS] Generated Draw.io XML: {drawio_path}")

    # 2. Generate Clean Vector SVG
    svg_content = generate_svg()
    svg_path = os.path.join(root_dir, "document", "temp", "rdm6300_picorv32_soc_complete_diagram.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"[SUCCESS] Generated Vector SVG: {svg_path}")

    # 3. Create standalone HTML wrapper for headless rendering
    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    background-color: #ffffff;
    display: flex;
    justify-content: center;
    align-items: center;
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
