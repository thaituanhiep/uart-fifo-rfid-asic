# -*- coding: utf-8 -*-
"""
Script: generate_complete_diagram.py
Generates the updated, high-precision SoC Block Diagram reflecting the new dedicated
module: soc_interconnect.v (Central 32-bit Memory Bus Interconnect & Address Decoder).

Features:
- Perfectly centered wire badges (pill tags) with dominant-baseline="central"
- Clean, non-overlapping signal routes
- Authentic typography using Segoe UI and Consolas
- Full 1920x1080 Full HD canvas, 2x Retina screenshot via Headless Chrome
"""

import os
import subprocess

def generate_svg():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="100%" height="100%" style="background-color: #ffffff; font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;">
  <defs>
    <style>
      text {
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
      }
      .wire-text {
        font-family: Consolas, 'SF Mono', Menlo, Monaco, 'Courier New', monospace;
        font-size: 11px;
        font-weight: 600;
        dominant-baseline: central;
        text-anchor: middle;
      }
      .code-text {
        font-family: Consolas, 'SF Mono', Menlo, Monaco, 'Courier New', monospace;
        font-size: 10.5px;
        dominant-baseline: central;
      }
    </style>

    <!-- Arrow Markers -->
    <marker id="arrow" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#1e293b" />
    </marker>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#2563eb" />
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#059669" />
    </marker>
    <marker id="arrow-red" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#dc2626" />
    </marker>
    <marker id="arrow-orange" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#d97706" />
    </marker>

    <!-- Drop Shadow Filter -->
    <filter id="shadow" x="-3%" y="-3%" width="106%" height="106%">
      <feDropShadow dx="2" dy="3.5" stdDeviation="4" flood-opacity="0.08"/>
    </filter>
  </defs>

  <!-- ===================================================================== -->
  <!-- 1. ASIC CHIP BOUNDARY                                                 -->
  <!-- ===================================================================== -->
  <rect x="300" y="30" width="1580" height="1010" rx="18" fill="#f8fafc" stroke="#0f172a" stroke-width="2.8" filter="url(#shadow)" />
  
  <!-- ASIC Top Banner -->
  <rect x="325" y="44" width="560" height="34" rx="6" fill="#0f172a" />
  <text x="340" y="67" font-size="16" font-weight="700" fill="#ffffff" letter-spacing="0.5">rdm6300_picorv32_soc.v</text>
  <text x="550" y="67" font-size="14" font-weight="500" fill="#94a3b8">| ASIC Chip Top-Level Architecture</text>

  <!-- ===================================================================== -->
  <!-- 2. OFF-CHIP EXTERNAL SPI NOR FLASH                                    -->
  <!-- ===================================================================== -->
  <g id="external_flash">
    <rect x="35" y="520" width="220" height="385" rx="12" fill="#ffffff" stroke="#d97706" stroke-width="2.2" stroke-dasharray="6 4" filter="url(#shadow)" />
    <rect x="45" y="530" width="200" height="365" rx="8" fill="#fffbeb" stroke="#fde68a" stroke-width="1.5" />
    
    <rect x="58" y="545" width="174" height="46" rx="6" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.2" />
    <text x="145" y="565" font-size="14" font-weight="700" fill="#92400e" text-anchor="middle">External SPI Flash</text>
    <text x="145" y="583" font-size="12" font-weight="600" fill="#b45309" text-anchor="middle">(Off-Chip NOR Flash)</text>

    <rect x="58" y="605" width="174" height="275" rx="6" fill="#ffffff" stroke="#f59e0b" stroke-width="1.2" />
    <text x="145" y="632" font-size="13" font-weight="700" fill="#b45309" text-anchor="middle">Firmware &amp; DB Storage</text>
    <line x1="70" y1="645" x2="220" y2="645" stroke="#fde68a" stroke-width="1.5" />

    <text x="70" y="670" font-size="12" font-weight="700" fill="#92400e">Offset: 0x0025_0000</text>
    <text x="70" y="690" font-size="11" fill="#78350f">• Compiled C firmware</text>
    <text x="70" y="708" font-size="11" fill="#78350f">• Reset boot vector</text>
    <text x="70" y="726" font-size="11" fill="#78350f">• Non-volatile persistence</text>

    <line x1="70" y1="742" x2="220" y2="742" stroke="#fde68a" stroke-width="1.5" />
    <text x="70" y="768" font-size="12" font-weight="700" fill="#92400e">Sector 48 (0x30_0000)</text>
    <text x="70" y="788" font-size="11" fill="#78350f">• 4096 Authorized Cards</text>
    <text x="70" y="814" font-size="12" font-weight="700" fill="#92400e">Sector 49 (0x31_0000)</text>
    <text x="70" y="834" font-size="11" fill="#78350f">• Non-volatile Access Logs</text>
  </g>

  <!-- Flash Connection Pins (Crossing Chip Boundary) -->
  <g id="flash_pins" stroke="#d97706" stroke-width="2" fill="none">
    <path d="M 255 590 L 325 590" marker-end="url(#arrow-orange)" />
    <rect x="258" y="579" width="64" height="22" rx="4" fill="#ffffff" stroke="#f59e0b" stroke-width="1" />
    <text x="290" y="590" class="wire-text" fill="#b45309">flash_csb</text>

    <path d="M 255 670 L 325 670" marker-end="url(#arrow-orange)" />
    <rect x="258" y="659" width="64" height="22" rx="4" fill="#ffffff" stroke="#f59e0b" stroke-width="1" />
    <text x="290" y="670" class="wire-text" fill="#b45309">flash_clk</text>

    <path d="M 255 765 L 325 765" marker-start="url(#arrow-orange)" marker-end="url(#arrow-orange)" />
    <rect x="254" y="754" width="72" height="22" rx="4" fill="#ffffff" stroke="#f59e0b" stroke-width="1" />
    <text x="290" y="765" class="wire-text" fill="#b45309">flash_io</text>
  </g>

  <!-- ===================================================================== -->
  <!-- 3. CPU MASTER: PICORV32 RISC-V CORE                                  -->
  <!-- ===================================================================== -->
  <g id="cpu">
    <rect x="325" y="100" width="255" height="390" rx="10" fill="#ffffff" stroke="#1e3a8a" stroke-width="2" filter="url(#shadow)" />
    
    <rect x="337" y="112" width="231" height="50" rx="6" fill="#dbeafe" stroke="#93c5fd" stroke-width="1.2" />
    <text x="452" y="132" font-size="14" font-weight="700" fill="#1e3a8a" text-anchor="middle">picorv32.v (u_picorv32)</text>
    <text x="452" y="151" font-size="12.5" font-weight="600" fill="#2563eb" text-anchor="middle">PicoRV32 RISC-V CPU Core</text>

    <rect x="337" y="172" width="231" height="305" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1" />
    <text x="452" y="198" font-size="13" font-weight="700" fill="#0f172a" text-anchor="middle">RV32I Instruction Set</text>
    <line x1="350" y1="210" x2="555" y2="210" stroke="#e2e8f0" stroke-width="1" />

    <text x="350" y="232" font-size="11.5" font-weight="600" fill="#334155">• Reset Vector: 0x0025_0000</text>
    <text x="350" y="252" font-size="11.5" font-weight="600" fill="#334155">• Stack Pointer: 0x0000_0400</text>
    <text x="350" y="272" font-size="11.5" font-weight="600" fill="#334155">• 32 Registers (x0 - x31)</text>
    <text x="350" y="292" font-size="11.5" font-weight="600" fill="#334155">• Native 32-bit Memory Bus</text>

    <rect x="348" y="312" width="209" height="120" rx="6" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1" />
    <text x="452" y="335" font-size="12" font-weight="700" fill="#1e40af" text-anchor="middle">C Firmware Execution</text>
    <line x1="360" y1="345" x2="545" y2="345" stroke="#bfdbfe" stroke-width="1" />
    <text x="358" y="366" font-size="11" fill="#1e3a8a">• firmware/main.c while(1)</text>
    <text x="358" y="386" font-size="11" fill="#1e3a8a">• RFID polling &amp; DB lookup</text>
    <text x="358" y="406" font-size="11" fill="#1e3a8a">• Host PC UART parser</text>
    <text x="358" y="423" font-size="10.5" font-weight="700" fill="#dc2626">• Core status: cpu_trap</text>
  </g>

  <!-- ===================================================================== -->
  <!-- 4. SLAVE 1: SPIMEMIO FLASH CONTROLLER                                 -->
  <!-- ===================================================================== -->
  <g id="spimemio">
    <rect x="325" y="520" width="255" height="385" rx="10" fill="#ffffff" stroke="#0f172a" stroke-width="2" filter="url(#shadow)" />
    
    <rect x="337" y="532" width="231" height="50" rx="6" fill="#fef3c7" stroke="#fcd34d" stroke-width="1.2" />
    <text x="452" y="552" font-size="14" font-weight="700" fill="#92400e" text-anchor="middle">spimemio.v (u_spimemio)</text>
    <text x="452" y="571" font-size="12.5" font-weight="600" fill="#b45309" text-anchor="middle">SPI Flash XIP Controller</text>

    <rect x="337" y="592" width="231" height="300" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1" />
    <text x="452" y="620" font-size="13" font-weight="700" fill="#0f172a" text-anchor="middle">XIP Protocol Engine</text>
    <line x1="350" y1="630" x2="555" y2="630" stroke="#e2e8f0" stroke-width="1" />

    <text x="350" y="654" font-size="11.5" fill="#334155">• 32-bit Bus to Serial QSPI</text>
    <text x="350" y="676" font-size="11.5" fill="#334155">• Fast Read Cmd 0x03 / 0xEB</text>
    <text x="350" y="698" font-size="11.5" fill="#334155">• 0x0010_0000 - 0x00FF_FFFF</text>
    <text x="350" y="720" font-size="11.5" fill="#334155">• Config Reg @ 0x0200_0000</text>
    <text x="350" y="742" font-size="11.5" fill="#334155">• Bit-bang SPI for Write/Erase</text>

    <rect x="348" y="765" width="209" height="70" rx="6" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1" />
    <text x="452" y="788" font-size="11.5" font-weight="700" fill="#1e40af" text-anchor="middle">External Status Pins</text>
    <text x="452" y="810" font-size="11" font-weight="600" fill="#2563eb" text-anchor="middle">flash_busy_o | flash_done_o</text>
  </g>

  <!-- ===================================================================== -->
  <!-- 5. CENTRAL MODULE: soc_interconnect.v (NEW DEDICATED MODULE FILE)     -->
  <!-- ===================================================================== -->
  <g id="interconnect">
    <rect x="730" y="100" width="340" height="805" rx="12" fill="#eff6ff" stroke="#2563eb" stroke-width="2.5" filter="url(#shadow)" />
    
    <!-- Header Badge -->
    <rect x="742" y="112" width="316" height="70" rx="8" fill="#dbeafe" stroke="#93c5fd" stroke-width="1.5" />
    <text x="900" y="137" font-size="15.5" font-weight="800" fill="#1e3a8a" text-anchor="middle">soc_interconnect.v</text>
    <text x="900" y="156" font-size="13" font-weight="700" fill="#1d4ed8" text-anchor="middle">Central Memory Bus Interconnect</text>
    <text x="900" y="173" font-size="11" font-weight="600" fill="#3b82f6" text-anchor="middle">Instance: u_interconnect</text>

    <!-- Sub-Block 1: Address Decoder -->
    <rect x="742" y="195" width="316" height="345" rx="8" fill="#ffffff" stroke="#bfdbfe" stroke-width="1.5" />
    <text x="900" y="222" font-size="13" font-weight="700" fill="#1e40af" text-anchor="middle">1. Address Decoding Logic (Decoders)</text>
    <line x1="755" y1="233" x2="1045" y2="233" stroke="#e2e8f0" stroke-width="1" />

    <g>
      <!-- SRAM -->
      <rect x="752" y="244" width="296" height="42" rx="4" fill="#f8fafc" stroke="#e2e8f0" />
      <text x="762" y="259" class="code-text" font-weight="700" fill="#059669">sel_sram</text>
      <text x="762" y="275" class="code-text" fill="#334155">= valid &amp;&amp; (addr &lt; 32'h0000_0400)</text>

      <!-- SPIMEM -->
      <rect x="752" y="292" width="296" height="46" rx="4" fill="#f8fafc" stroke="#e2e8f0" />
      <text x="762" y="307" class="code-text" font-weight="700" fill="#b45309">sel_spimem</text>
      <text x="762" y="321" class="code-text" fill="#334155">= valid &amp;&amp; (addr &gt;= 32'h0010_0000</text>
      <text x="762" y="332" class="code-text" fill="#334155">         &amp;&amp; addr &lt; 32'h0100_0000)</text>

      <!-- SPICFG -->
      <rect x="752" y="344" width="296" height="42" rx="4" fill="#f8fafc" stroke="#e2e8f0" />
      <text x="762" y="359" class="code-text" font-weight="700" fill="#b45309">sel_spicfg</text>
      <text x="762" y="375" class="code-text" fill="#334155">= valid &amp;&amp; (addr == 32'h0200_0000)</text>

      <!-- RFID -->
      <rect x="752" y="392" width="296" height="42" rx="4" fill="#f8fafc" stroke="#e2e8f0" />
      <text x="762" y="407" class="code-text" font-weight="700" fill="#4338ca">sel_rfid</text>
      <text x="762" y="423" class="code-text" fill="#334155">= valid &amp;&amp; (addr[31:28] == 4'h1)</text>

      <!-- UART -->
      <rect x="752" y="440" width="296" height="42" rx="4" fill="#f8fafc" stroke="#e2e8f0" />
      <text x="762" y="455" class="code-text" font-weight="700" fill="#0d9488">sel_uart</text>
      <text x="762" y="471" class="code-text" fill="#334155">= valid &amp;&amp; (addr[31:28] == 4'h3)</text>

      <!-- GPIO -->
      <rect x="752" y="488" width="296" height="40" rx="4" fill="#f8fafc" stroke="#e2e8f0" />
      <text x="762" y="503" class="code-text" font-weight="700" fill="#475569">sel_gpio</text>
      <text x="762" y="519" class="code-text" fill="#334155">= valid &amp;&amp; (addr[31:28] == 4'h4)</text>
    </g>

    <!-- Sub-Block 2: Return MUX -->
    <rect x="742" y="552" width="316" height="338" rx="8" fill="#ffffff" stroke="#bfdbfe" stroke-width="1.5" />
    <text x="900" y="578" font-size="13" font-weight="700" fill="#1e40af" text-anchor="middle">2. Response Multiplexing (Return to CPU)</text>
    <line x1="755" y1="589" x2="1045" y2="589" stroke="#e2e8f0" stroke-width="1" />

    <g>
      <rect x="752" y="600" width="296" height="142" rx="4" fill="#f8fafc" stroke="#e2e8f0" />
      <text x="762" y="618" class="code-text" font-weight="700" fill="#059669">assign cpu_mem_rdata =</text>
      <text x="772" y="635" class="code-text" fill="#334155">sel_sram   ? sram_rdata    :</text>
      <text x="772" y="652" class="code-text" fill="#334155">sel_spimem ? spimem_rdata  :</text>
      <text x="772" y="669" class="code-text" fill="#334155">sel_spicfg ? spimem_cfg_do :</text>
      <text x="772" y="686" class="code-text" fill="#334155">sel_rfid   ? rfid_rdata    :</text>
      <text x="772" y="703" class="code-text" fill="#334155">sel_uart   ? uart_rdata    :</text>
      <text x="772" y="720" class="code-text" fill="#334155">sel_gpio   ? gpio_rdata    : 0;</text>

      <rect x="752" y="750" width="296" height="125" rx="4" fill="#f8fafc" stroke="#e2e8f0" />
      <text x="762" y="769" class="code-text" font-weight="700" fill="#dc2626">assign cpu_mem_ready =</text>
      <text x="772" y="788" class="code-text" fill="#334155">sram_ready   ||</text>
      <text x="772" y="805" class="code-text" fill="#334155">spimem_ready || sel_spicfg ||</text>
      <text x="772" y="822" class="code-text" fill="#334155">rfid_ready   || uart_ready ||</text>
      <text x="772" y="839" class="code-text" fill="#334155">gpio_ready;</text>
    </g>
  </g>

  <!-- ===================================================================== -->
  <!-- WIRING: CPU MASTER <-> soc_interconnect (150px WIDE CHANNEL)          -->
  <!-- ===================================================================== -->
  <g id="wires_cpu_interconnect" stroke="#1e293b" stroke-width="1.8" fill="none">
    <!-- cpu_mem_valid -->
    <path d="M 580 145 L 730 145" marker-end="url(#arrow)" />
    <rect x="590" y="134" width="130" height="22" rx="4" fill="#ffffff" stroke="#94a3b8" stroke-width="1" />
    <text x="655" y="145" class="wire-text" fill="#0f172a">cpu_mem_valid</text>

    <!-- cpu_mem_addr[31:0] -->
    <path d="M 580 190 L 730 190" marker-end="url(#arrow)" />
    <rect x="585" y="179" width="140" height="22" rx="4" fill="#ffffff" stroke="#94a3b8" stroke-width="1" />
    <text x="655" y="190" class="wire-text" fill="#0f172a">cpu_mem_addr[31:0]</text>

    <!-- mem_wdata[31:0] -->
    <path d="M 580 235 L 730 235" marker-end="url(#arrow)" />
    <rect x="592" y="224" width="126" height="22" rx="4" fill="#ffffff" stroke="#94a3b8" stroke-width="1" />
    <text x="655" y="235" class="wire-text" fill="#334155">mem_wdata[31:0]</text>

    <!-- mem_wstrb[3:0] -->
    <path d="M 580 280 L 730 280" marker-end="url(#arrow)" />
    <rect x="597" y="269" width="116" height="22" rx="4" fill="#ffffff" stroke="#94a3b8" stroke-width="1" />
    <text x="655" y="280" class="wire-text" fill="#334155">mem_wstrb[3:0]</text>

    <!-- cpu_mem_rdata[31:0] (Return Line) -->
    <path d="M 730 365 L 580 365" marker-end="url(#arrow-green)" stroke="#059669" stroke-width="2.2" />
    <rect x="585" y="354" width="140" height="22" rx="4" fill="#ffffff" stroke="#10b981" stroke-width="1.2" />
    <text x="655" y="365" class="wire-text" fill="#059669">cpu_mem_rdata[31:0]</text>

    <!-- cpu_mem_ready (Return Line) -->
    <path d="M 730 430 L 580 430" marker-end="url(#arrow-red)" stroke="#dc2626" stroke-width="2.2" />
    <rect x="592" y="419" width="126" height="22" rx="4" fill="#ffffff" stroke="#ef4444" stroke-width="1.2" />
    <text x="655" y="430" class="wire-text" fill="#dc2626">cpu_mem_ready</text>
  </g>

  <!-- ===================================================================== -->
  <!-- WIRING: soc_interconnect <-> SPIMEMIO (150px WIDE CHANNEL)            -->
  <!-- ===================================================================== -->
  <g id="wires_interconnect_spimemio" stroke="#1e293b" stroke-width="1.8" fill="none">
    <!-- sel_spimem -->
    <path d="M 730 565 L 580 565" marker-end="url(#arrow)" />
    <rect x="600" y="554" width="110" height="22" rx="4" fill="#ffffff" stroke="#f59e0b" stroke-width="1" />
    <text x="655" y="565" class="wire-text" fill="#b45309">sel_spimem</text>

    <!-- sel_spicfg -->
    <path d="M 730 610 L 580 610" marker-end="url(#arrow)" />
    <rect x="600" y="599" width="110" height="22" rx="4" fill="#ffffff" stroke="#f59e0b" stroke-width="1" />
    <text x="655" y="610" class="wire-text" fill="#b45309">sel_spicfg</text>

    <!-- addr[23:0] -->
    <path d="M 730 655 L 580 655" marker-end="url(#arrow)" />
    <rect x="605" y="644" width="100" height="22" rx="4" fill="#ffffff" stroke="#94a3b8" stroke-width="1" />
    <text x="655" y="655" class="wire-text" fill="#334155">addr[23:0]</text>

    <!-- spimem_rdata[31:0] -->
    <path d="M 580 730 L 730 730" marker-end="url(#arrow-green)" stroke="#059669" stroke-width="2.2" />
    <rect x="585" y="719" width="140" height="22" rx="4" fill="#ffffff" stroke="#10b981" stroke-width="1.2" />
    <text x="655" y="730" class="wire-text" fill="#059669">spimem_rdata[31:0]</text>

    <!-- spimem_ready -->
    <path d="M 580 805 L 730 805" marker-end="url(#arrow-red)" stroke="#dc2626" stroke-width="2.2" />
    <rect x="597" y="794" width="116" height="22" rx="4" fill="#ffffff" stroke="#ef4444" stroke-width="1.2" />
    <text x="655" y="805" class="wire-text" fill="#dc2626">spimem_ready</text>
  </g>

  <!-- ===================================================================== -->
  <!-- 6. SLAVE 0: 1KB DATA SRAM                                             -->
  <!-- ===================================================================== -->
  <g id="sram">
    <rect x="1220" y="100" width="280" height="210" rx="10" fill="#ffffff" stroke="#059669" stroke-width="2" filter="url(#shadow)" />
    
    <rect x="1232" y="112" width="256" height="48" rx="6" fill="#d1fae5" stroke="#a7f3d0" stroke-width="1.2" />
    <text x="1360" y="132" font-size="14" font-weight="700" fill="#065f46" text-anchor="middle">data_sram.v (u_data_sram)</text>
    <text x="1360" y="150" font-size="12" font-weight="600" fill="#047857" text-anchor="middle">1KB High-Speed Synchronous SRAM</text>

    <rect x="1232" y="170" width="256" height="128" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1" />
    <text x="1360" y="194" font-size="13" font-weight="700" fill="#0f172a" text-anchor="middle">0x0000_0000 - 0x0000_03FF</text>
    <line x1="1245" y1="204" x2="1475" y2="204" stroke="#e2e8f0" stroke-width="1" />

    <text x="1245" y="225" font-size="11.5" fill="#334155">• 256 Words × 32-bit Array</text>
    <text x="1245" y="245" font-size="11.5" fill="#334155">• Stack Pointer (SP = 0x400)</text>
    <text x="1245" y="265" font-size="11.5" fill="#334155">• C Local/Global Variables</text>
    <text x="1245" y="285" font-size="11.5" font-weight="700" fill="#059669">• 1-cycle access latency</text>
  </g>

  <!-- WIRING: interconnect <-> SRAM (150px WIDE CHANNEL) -->
  <g id="wires_interconnect_sram" stroke="#1e293b" stroke-width="1.8" fill="none">
    <!-- sel_sram -->
    <path d="M 1070 135 L 1220 135" marker-end="url(#arrow)" />
    <rect x="1095" y="124" width="100" height="22" rx="4" fill="#ffffff" stroke="#10b981" stroke-width="1.2" />
    <text x="1145" y="135" class="wire-text" fill="#059669">sel_sram</text>

    <!-- addr[9:0] -->
    <path d="M 1070 170 L 1220 170" marker-end="url(#arrow)" />
    <rect x="1100" y="159" width="90" height="22" rx="4" fill="#ffffff" stroke="#94a3b8" stroke-width="1" />
    <text x="1145" y="170" class="wire-text" fill="#334155">addr[9:0]</text>

    <!-- wdata & wstrb -->
    <path d="M 1070 205 L 1220 205" marker-end="url(#arrow)" />
    <rect x="1085" y="194" width="120" height="22" rx="4" fill="#ffffff" stroke="#94a3b8" stroke-width="1" />
    <text x="1145" y="205" class="wire-text" fill="#334155">wdata &amp; wstrb</text>

    <!-- sram_rdata[31:0] -->
    <path d="M 1220 245 L 1070 245" marker-end="url(#arrow-green)" stroke="#059669" stroke-width="2.2" />
    <rect x="1080" y="234" width="130" height="22" rx="4" fill="#ffffff" stroke="#10b981" stroke-width="1.2" />
    <text x="1145" y="245" class="wire-text" fill="#059669">sram_rdata[31:0]</text>

    <!-- sram_ready -->
    <path d="M 1220 285 L 1070 285" marker-end="url(#arrow-red)" stroke="#dc2626" stroke-width="2.2" />
    <rect x="1095" y="274" width="100" height="22" rx="4" fill="#ffffff" stroke="#ef4444" stroke-width="1.2" />
    <text x="1145" y="285" class="wire-text" fill="#dc2626">sram_ready</text>
  </g>

  <!-- ===================================================================== -->
  <!-- 7. SLAVE 2: RDM6300 RFID SUBSYSTEM                                    -->
  <!-- ===================================================================== -->
  <g id="rfid_subsystem">
    <rect x="1220" y="335" width="540" height="260" rx="10" fill="#ffffff" stroke="#4338ca" stroke-width="2" filter="url(#shadow)" />
    
    <rect x="1232" y="347" width="516" height="34" rx="6" fill="#e0e7ff" stroke="#c7d2fe" stroke-width="1.2" />
    <text x="1245" y="370" font-size="14" font-weight="800" fill="#312e81">RDM6300 RFID Subsystem (0x1000_0000 - 0x1000_0007)</text>

    <!-- Submodule 1: sync_2ff -->
    <rect x="1635" y="395" width="105" height="175" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" />
    <rect x="1643" y="405" width="89" height="30" rx="4" fill="#ede9fe" />
    <text x="1687" y="425" font-size="11.5" font-weight="700" fill="#4338ca" text-anchor="middle">sync_2ff.v</text>
    <text x="1687" y="450" font-size="10" fill="#64748b" text-anchor="middle">u_sync_rdm</text>
    <line x1="1643" y1="462" x2="1732" y2="462" stroke="#e2e8f0" />
    <text x="1687" y="485" font-size="10" font-weight="600" fill="#1e293b" text-anchor="middle">2-FF CDC</text>
    <text x="1687" y="505" font-size="9.5" fill="#475569" text-anchor="middle">Metastability</text>
    <text x="1687" y="525" font-size="9.5" fill="#475569" text-anchor="middle">Filter</text>
    <text x="1687" y="550" font-size="9" font-weight="700" fill="#059669" text-anchor="middle">MTBF &gt; 1000yr</text>

    <!-- Submodule 2: uart_rx -->
    <rect x="1500" y="395" width="120" height="175" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" />
    <rect x="1508" y="405" width="104" height="30" rx="4" fill="#ede9fe" />
    <text x="1560" y="425" font-size="11.5" font-weight="700" fill="#4338ca" text-anchor="middle">uart_rx.v</text>
    <text x="1560" y="450" font-size="10" fill="#64748b" text-anchor="middle">u_rdm_rx</text>
    <line x1="1508" y1="462" x2="1612" y2="462" stroke="#e2e8f0" />
    <text x="1560" y="482" font-size="10" font-weight="600" fill="#1e293b" text-anchor="middle">9600 Baud 8-N-1</text>
    <text x="1560" y="500" font-size="9.5" fill="#475569" text-anchor="middle">16x Oversample</text>
    <text x="1560" y="518" font-size="9.5" fill="#475569" text-anchor="middle">Majority Voter</text>
    <text x="1560" y="536" font-size="9.5" fill="#475569" text-anchor="middle">(Ticks 7,8,9)</text>
    <text x="1560" y="555" font-size="9" font-weight="700" fill="#059669" text-anchor="middle">Noise Filter</text>

    <!-- Submodule 3: rdm6300_frame_decoder -->
    <rect x="1350" y="395" width="135" height="175" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" />
    <rect x="1358" y="405" width="119" height="30" rx="4" fill="#ede9fe" />
    <text x="1417" y="425" font-size="11" font-weight="700" fill="#4338ca" text-anchor="middle">frame_decoder.v</text>
    <text x="1417" y="450" font-size="10" fill="#64748b" text-anchor="middle">u_rdm_decoder</text>
    <line x1="1358" y1="462" x2="1477" y2="462" stroke="#e2e8f0" />
    <text x="1417" y="482" font-size="10" font-weight="600" fill="#1e293b" text-anchor="middle">14-Byte Frame</text>
    <text x="1417" y="500" font-size="9.5" fill="#475569" text-anchor="middle">STX(02) &amp; ETX(03)</text>
    <text x="1417" y="518" font-size="9.5" fill="#475569" text-anchor="middle">1-Cycle XOR Engine</text>
    <text x="1417" y="536" font-size="9.5" fill="#475569" text-anchor="middle">Parallel Checksum</text>
    <text x="1417" y="555" font-size="9" font-weight="700" fill="#059669" text-anchor="middle">Hardware Check</text>

    <!-- RFID Registers -->
    <rect x="1235" y="395" width="100" height="175" rx="6" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.5" />
    <text x="1285" y="422" font-size="12" font-weight="700" fill="#1e40af" text-anchor="middle">RFID</text>
    <text x="1285" y="440" font-size="12" font-weight="700" fill="#1e40af" text-anchor="middle">Registers</text>
    <line x1="1245" y1="452" x2="1325" y2="452" stroke="#bfdbfe" />
    <text x="1285" y="472" font-size="10" font-weight="600" fill="#1d4ed8" text-anchor="middle">status (0x00)</text>
    <text x="1285" y="490" font-size="9" fill="#475569" text-anchor="middle">bit 0: valid</text>
    <text x="1285" y="512" font-size="10" font-weight="600" fill="#1d4ed8" text-anchor="middle">tag_hi (0x04)</text>
    <text x="1285" y="530" font-size="9" fill="#475569" text-anchor="middle">version byte</text>
    <text x="1285" y="552" font-size="10" font-weight="600" fill="#1d4ed8" text-anchor="middle">tag_lo (0x08)</text>

    <!-- RFID Pipeline Arrows -->
    <!-- External Pin into sync_2ff -->
    <path d="M 1835 482 L 1740 482" stroke="#1e293b" stroke-width="2.2" fill="none" marker-end="url(#arrow)" />
    <rect x="1748" y="471" width="94" height="22" rx="4" fill="#ffffff" stroke="#94a3b8" stroke-width="1" />
    <text x="1795" y="482" class="wire-text" fill="#0f172a">rdm6300_rx_i</text>

    <!-- sync to uart_rx -->
    <path d="M 1635 482 L 1620 482" stroke="#1e293b" stroke-width="1.6" fill="none" marker-end="url(#arrow)" />
    
    <!-- uart_rx to decoder -->
    <path d="M 1500 482 L 1485 482" stroke="#1e293b" stroke-width="1.6" fill="none" marker-end="url(#arrow)" />
    <text x="1492" y="472" font-size="9" fill="#475569" text-anchor="middle">byte</text>

    <!-- decoder to registers -->
    <path d="M 1350 482 L 1335 482" stroke="#1e293b" stroke-width="1.6" fill="none" marker-end="url(#arrow)" />
    <text x="1342" y="472" font-size="9" fill="#475569" text-anchor="middle">UID</text>

    <!-- External Strobe Pin card_event_o (Routed cleanly below the submodules) -->
    <path d="M 1417 570 L 1417 583 L 1835 583" stroke="#d97706" stroke-width="2" fill="none" marker-end="url(#arrow-orange)" />
    <rect x="1748" y="572" width="94" height="22" rx="4" fill="#ffffff" stroke="#f59e0b" stroke-width="1.2" />
    <text x="1795" y="583" class="wire-text" fill="#b45309">card_event_o</text>
  </g>

  <!-- WIRING: interconnect <-> RFID Registers (150px WIDE CHANNEL) -->
  <g id="wires_interconnect_rfid" stroke="#1e293b" stroke-width="1.8" fill="none">
    <!-- sel_rfid -->
    <path d="M 1070 420 L 1235 420" marker-end="url(#arrow)" />
    <rect x="1095" y="409" width="100" height="22" rx="4" fill="#ffffff" stroke="#818cf8" stroke-width="1.2" />
    <text x="1145" y="420" class="wire-text" fill="#4338ca">sel_rfid</text>

    <!-- rfid_rdata[31:0] -->
    <path d="M 1235 480 L 1070 480" marker-end="url(#arrow-green)" stroke="#059669" stroke-width="2.2" />
    <rect x="1080" y="469" width="130" height="22" rx="4" fill="#ffffff" stroke="#10b981" stroke-width="1.2" />
    <text x="1145" y="480" class="wire-text" fill="#059669">rfid_rdata[31:0]</text>

    <!-- rfid_ready -->
    <path d="M 1235 540 L 1070 540" marker-end="url(#arrow-red)" stroke="#dc2626" stroke-width="2.2" />
    <rect x="1095" y="529" width="100" height="22" rx="4" fill="#ffffff" stroke="#ef4444" stroke-width="1.2" />
    <text x="1145" y="540" class="wire-text" fill="#dc2626">rfid_ready</text>
  </g>

  <!-- ===================================================================== -->
  <!-- 8. SLAVE 3: HOST PC UART SUBSYSTEM                                    -->
  <!-- ===================================================================== -->
  <g id="uart_subsystem">
    <rect x="1220" y="625" width="540" height="260" rx="10" fill="#ffffff" stroke="#0d9488" stroke-width="2" filter="url(#shadow)" />
    
    <rect x="1232" y="637" width="516" height="34" rx="6" fill="#ccfbf1" stroke="#99f6e4" stroke-width="1.2" />
    <text x="1245" y="660" font-size="14" font-weight="800" fill="#115e59">Host PC UART Subsystem (0x3000_0000 - 0x3000_0007)</text>

    <!-- Submodule 1: sync_2ff for PC -->
    <rect x="1635" y="685" width="105" height="185" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" />
    <rect x="1643" y="695" width="89" height="30" rx="4" fill="#e6fffa" />
    <text x="1687" y="715" font-size="11.5" font-weight="700" fill="#0d9488" text-anchor="middle">sync_2ff.v</text>
    <text x="1687" y="740" font-size="10" fill="#64748b" text-anchor="middle">u_sync_pcrx</text>
    <line x1="1643" y1="752" x2="1732" y2="752" stroke="#e2e8f0" />
    <text x="1687" y="775" font-size="10" font-weight="600" fill="#1e293b" text-anchor="middle">2-FF CDC</text>
    <text x="1687" y="795" font-size="9.5" fill="#475569" text-anchor="middle">Metastability</text>
    <text x="1687" y="815" font-size="9.5" fill="#475569" text-anchor="middle">Filter for PC</text>
    <text x="1687" y="845" font-size="9" font-weight="700" fill="#059669" text-anchor="middle">Asynchronous Rx</text>

    <!-- Submodule 2: simpleuart -->
    <rect x="1420" y="685" width="195" height="185" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" />
    <rect x="1428" y="695" width="179" height="30" rx="4" fill="#e6fffa" />
    <text x="1517" y="715" font-size="12" font-weight="700" fill="#0d9488" text-anchor="middle">simpleuart.v</text>
    <text x="1517" y="740" font-size="10" fill="#64748b" text-anchor="middle">u_simpleuart_core</text>
    <line x1="1428" y1="752" x2="1607" y2="752" stroke="#e2e8f0" />
    <text x="1517" y="775" font-size="10" font-weight="600" fill="#1e293b" text-anchor="middle">Full-Duplex UART Core</text>
    <text x="1517" y="795" font-size="9.5" fill="#475569" text-anchor="middle">• TX 8-bit Shift Register</text>
    <text x="1517" y="815" font-size="9.5" fill="#475569" text-anchor="middle">• RX Bit Center Sampler</text>
    <text x="1517" y="835" font-size="9.5" fill="#475569" text-anchor="middle">• Prescaler Divisor @ 0x00</text>
    <text x="1517" y="855" font-size="9" font-weight="700" fill="#059669" text-anchor="middle">Standard Baud: 9600</text>

    <!-- Submodule 3: sync_fifo (32-byte) -->
    <rect x="1235" y="685" width="165" height="185" rx="6" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.5" />
    <rect x="1243" y="695" width="149" height="30" rx="4" fill="#dbeafe" />
    <text x="1317" y="715" font-size="12" font-weight="700" fill="#1e40af" text-anchor="middle">sync_fifo.v (u_rx_fifo)</text>
    <text x="1317" y="740" font-size="10" font-weight="600" fill="#1d4ed8" text-anchor="middle">32-Byte RX FIFO</text>
    <line x1="1243" y1="752" x2="1392" y2="752" stroke="#bfdbfe" />
    <text x="1317" y="775" font-size="10" fill="#1e3a8a" text-anchor="middle">• Auto-Push from UART</text>
    <text x="1317" y="795" font-size="10" fill="#1e3a8a" text-anchor="middle">• CPU Pop on Read @ 0x04</text>
    <text x="1317" y="815" font-size="10" fill="#1e3a8a" text-anchor="middle">• Status Flags: empty/full</text>
    <text x="1317" y="845" font-size="9.5" font-weight="700" fill="#059669" text-anchor="middle">Zero-Packet-Drop!</text>

    <!-- UART Wires & External Pins -->
    <!-- PC RX into sync_2ff -->
    <path d="M 1835 730 L 1740 730" stroke="#1e293b" stroke-width="2.2" fill="none" marker-end="url(#arrow)" />
    <rect x="1755" y="719" width="80" height="22" rx="4" fill="#ffffff" stroke="#94a3b8" stroke-width="1" />
    <text x="1795" y="730" class="wire-text" fill="#0f172a">uart_rx_i</text>

    <!-- sync to simpleuart -->
    <path d="M 1635 730 L 1615 730" stroke="#1e293b" stroke-width="1.6" fill="none" marker-end="url(#arrow)" />

    <!-- simpleuart into FIFO -->
    <path d="M 1420 770 L 1400 770" stroke="#1e293b" stroke-width="1.6" fill="none" marker-end="url(#arrow)" />
    <text x="1410" y="760" font-size="9" fill="#475569" text-anchor="middle">push</text>

    <!-- simpleuart TX out to Pad -->
    <path d="M 1615 820 L 1835 820" stroke="#1e293b" stroke-width="2.2" fill="none" marker-end="url(#arrow)" />
    <rect x="1755" y="809" width="80" height="22" rx="4" fill="#ffffff" stroke="#94a3b8" stroke-width="1" />
    <text x="1795" y="820" class="wire-text" fill="#0f172a">uart_tx_o</text>
  </g>

  <!-- WIRING: interconnect <-> UART Subsystem (150px WIDE CHANNEL) -->
  <g id="wires_interconnect_uart" stroke="#1e293b" stroke-width="1.8" fill="none">
    <!-- sel_uart -->
    <path d="M 1070 705 L 1235 705" marker-end="url(#arrow)" />
    <rect x="1095" y="694" width="100" height="22" rx="4" fill="#ffffff" stroke="#14b8a6" stroke-width="1.2" />
    <text x="1145" y="705" class="wire-text" fill="#0d9488">sel_uart</text>

    <!-- uart_rdata[31:0] -->
    <path d="M 1235 765 L 1070 765" marker-end="url(#arrow-green)" stroke="#059669" stroke-width="2.2" />
    <rect x="1080" y="754" width="130" height="22" rx="4" fill="#ffffff" stroke="#10b981" stroke-width="1.2" />
    <text x="1145" y="765" class="wire-text" fill="#059669">uart_rdata[31:0]</text>

    <!-- uart_ready -->
    <path d="M 1235 825 L 1070 825" marker-end="url(#arrow-red)" stroke="#dc2626" stroke-width="2.2" />
    <rect x="1095" y="814" width="100" height="22" rx="4" fill="#ffffff" stroke="#ef4444" stroke-width="1.2" />
    <text x="1145" y="825" class="wire-text" fill="#dc2626">uart_ready</text>
  </g>

  <!-- ===================================================================== -->
  <!-- 9. SLAVE 4: GPIO LEDS & HEARTBEAT LOGIC                               -->
  <!-- ===================================================================== -->
  <g id="gpio_leds">
    <rect x="730" y="930" width="340" height="65" rx="8" fill="#ffffff" stroke="#475569" stroke-width="2" filter="url(#shadow)" />
    <rect x="742" y="938" width="316" height="49" rx="6" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1" />
    <text x="900" y="958" font-size="13" font-weight="700" fill="#1e293b" text-anchor="middle">GPIO &amp; Status LEDs (0x4000_0000)</text>
    <text x="900" y="976" font-size="11" font-family="monospace" fill="#64748b" text-anchor="middle">sel_gpio | gpio_rdata | gpio_ready</text>

    <!-- Path from GPIO to Pad -->
    <path d="M 1070 955 L 1835 955" stroke="#1e293b" stroke-width="2.2" fill="none" marker-end="url(#arrow)" />
    <rect x="1350" y="943" width="410" height="24" rx="4" fill="#ffffff" stroke="#94a3b8" stroke-width="1" />
    <text x="1555" y="955" font-size="11.5" font-weight="700" fill="#0f172a" text-anchor="middle" dominant-baseline="central">leds_o[15:0] (Diagnostic LEDs: Alive, Grant, Deny, Flash Active, Saved)</text>
  </g>

</svg>
'''
    return svg

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    svg_content = generate_svg()

    # 1. Save SVG in root workspace
    svg_path = os.path.join(root_dir, "rdm6300_picorv32_soc_complete_diagram.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"[SUCCESS] Wrote SVG to: {svg_path}")

    # 2. Prepare HTML wrapper for pixel-perfect Headless Chrome rendering
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
    width: 1920px;
    height: 1080px;
  }}
  .diagram-container {{
    width: 1920px;
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
    html_path = os.path.join(root_dir, "document", "temp", "render_diagram.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[SUCCESS] Wrote HTML wrapper to: {html_path}")

    # 3. Render High-Resolution PNG via Headless Chrome at 1920x1080 (Retina factor = 2 -> 3840x2160!)
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    png_path = os.path.join(root_dir, "document", "temp", "fig1_block_diagram.png")
    
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--force-device-scale-factor=2",
        f"--screenshot={png_path}",
        "--window-size=1920,1080",
        f"file:///{html_path.replace(os.sep, '/')}"
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(png_path):
        size = os.path.getsize(png_path)
        print(f"[SUCCESS] Rendered PNG via Headless Chrome: {png_path} ({size} bytes)")
    else:
        print(f"[ERROR] Chrome screenshot failed. Return code: {res.returncode}")
        print(res.stderr)

    # 4. Copy to Brain Artifacts directory
    art_path = r"C:\Users\thait\.gemini\antigravity-ide\brain\40d01579-3c16-4b85-9b12-c0e7d33bcd21\fig1_soc_block_diagram.png"
    if os.path.exists(png_path):
        import shutil
        shutil.copyfile(png_path, art_path)
        print(f"[SUCCESS] Copied to Artifacts: {art_path}")

if __name__ == "__main__":
    main()
