# -*- coding: utf-8 -*-
import os
import subprocess

html_content = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Firmware SoC Co-Design Architecture</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1750px;
    height: 1120px;
    background: #ffffff;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    position: relative;
    overflow: hidden;
  }

  /* Title Banner */
  .title-banner {
    position: absolute;
    left: 40px;
    top: 20px;
    width: 1670px;
    height: 70px;
    background: #f8fafc;
    border: 2px solid #cbd5e1;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.06);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
  }
  .title-banner h1 {
    font-size: 21px;
    color: #0f172a;
    font-weight: 800;
    letter-spacing: 0.3px;
  }
  .title-banner p {
    font-size: 13.5px;
    color: #475569;
    margin-top: 3px;
  }

  /* Cards */
  .card {
    position: absolute;
    border-radius: 10px;
    padding: 12px 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    display: flex;
    flex-direction: column;
  }
  .card-title {
    font-size: 15px;
    font-weight: 800;
  }
  .card-sub {
    font-size: 11.5px;
    font-weight: 700;
    margin-top: 2px;
  }
  .divider {
    height: 1px;
    margin: 8px 0;
  }
  .code-box {
    font-family: "Consolas", monospace;
    font-size: 11px;
    line-height: 1.48;
    background: rgba(255,255,255,0.7);
    border-radius: 6px;
    padding: 6px 10px;
    border: 1px solid rgba(0,0,0,0.08);
    flex-grow: 1;
  }
  .card-footer {
    font-size: 10.5px;
    margin-top: 6px;
    line-height: 1.4;
  }

  /* Color themes */
  .theme-blue {
    background: #dbeafe;
    border: 2px solid #2563eb;
    color: #0f172a;
  }
  .theme-blue .card-title { color: #1e3a8a; }
  .theme-blue .card-sub { color: #2563eb; }
  .theme-blue .divider { background: #93c5fd; }
  .theme-blue .card-footer { color: #1e3a8a; }

  .theme-green {
    background: #d1fae5;
    border: 2px solid #10b981;
    color: #064e3b;
  }
  .theme-green .card-title { color: #065f46; }
  .theme-green .card-sub { color: #059669; }
  .theme-green .divider { background: #6ee7b7; }
  .theme-green .card-footer { color: #065f46; }

  .theme-purple {
    background: #f3e8ff;
    border: 2px solid #9333ea;
    color: #3b0764;
  }
  .theme-purple .card-title { color: #581c87; }
  .theme-purple .card-sub { color: #7c3aed; }
  .theme-purple .divider { background: #c084fc; }
  .theme-purple .card-footer { color: #581c87; }

  .theme-amber {
    background: #fef3c7;
    border: 2px solid #d97706;
    color: #451a03;
  }
  .theme-amber .card-title { color: #78350f; }
  .theme-amber .card-sub { color: #b45309; }
  .theme-amber .divider { background: #fde68a; }
  .theme-amber .card-footer { color: #78350f; }

  .theme-orange {
    background: #ffedd5;
    border: 2px solid #ea580c;
    color: #431407;
  }
  .theme-orange .card-title { color: #7c2d12; }
  .theme-orange .card-sub { color: #ea580c; }
  .theme-orange .divider { background: #fdba74; }
  .theme-orange .card-footer { color: #7c2d12; }

  /* SVG layer */
  svg.wires {
    position: absolute;
    left: 0;
    top: 0;
    width: 1750px;
    height: 1120px;
    pointer-events: none;
    z-index: 10;
  }

  /* Badge labels */
  .badge {
    position: absolute;
    z-index: 20;
    background: #ffffff;
    border-radius: 6px;
    padding: 3px 8px;
    font-size: 11px;
    font-weight: 700;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    white-space: nowrap;
  }
</style>
</head>
<body>

  <!-- Title -->
  <div class="title-banner">
    <h1>SƠ ĐỒ LIÊN KẾT MÃ NGUỒN CẤU HÌNH & THỰC THI HỆ THỐNG FIRMWARE TRÊN PHẦN CỨNG SOC</h1>
    <p>Đối chiếu trực tiếp từng đoạn code quan trọng: RTL Top, Linker Script, Assembly, Flash XIP, Bus Interconnect, Driver C & App</p>
  </div>

  <!-- SVG Wires -->
  <svg class="wires">
    <defs>
      <marker id="arr-amber" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
        <path d="M0,0 L0,6 L8,3 z" fill="#d97706" />
      </marker>
      <marker id="arr-green" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
        <path d="M0,0 L0,6 L8,3 z" fill="#059669" />
      </marker>
      <marker id="arr-blue" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
        <path d="M0,0 L0,6 L8,3 z" fill="#2563eb" />
      </marker>
      <marker id="arr-purple" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
        <path d="M0,0 L0,6 L8,3 z" fill="#7c3aed" />
      </marker>
      <marker id="arr-rose" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
        <path d="M0,0 L0,6 L8,3 z" fill="#e11d48" />
      </marker>
      <marker id="arr-orange" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
        <path d="M0,0 L0,6 L8,3 z" fill="#ea580c" />
      </marker>
    </defs>

    <!-- Wire 1: Top -> Linker (Vertical in Col 1: y=390 to 440 at x=285) -->
    <path d="M 285 390 L 285 440" stroke="#d97706" stroke-width="3.5" fill="none" marker-end="url(#arr-amber)"/>

    <!-- Wire 2: Linker -> start.s (Vertical in Col 1: y=730 to 780 at x=285) -->
    <path d="M 285 730 L 285 780" stroke="#059669" stroke-width="3.5" fill="none" marker-end="url(#arr-green)"/>

    <!-- Wire 3: Linker -> Spimem (x=530 to 610, y=585 to 250) -->
    <path d="M 530 585 L 570 585 L 570 250 L 610 250" stroke="#d97706" stroke-width="2.5" fill="none" marker-end="url(#arr-amber)"/>

    <!-- Wire 4: Interconnect -> Spimem (Vertical in Col 2: y=440 up to 390 at x=875) -->
    <path d="M 875 440 L 875 390" stroke="#ea580c" stroke-width="3" fill="none" marker-end="url(#arr-orange)"/>

    <!-- Wire 5: Interconnect -> flash.c (Vertical in Col 2: y=780 down to 830 at x=875) -->
    <path d="M 875 780 L 875 830" stroke="#7c3aed" stroke-width="3.5" fill="none" marker-end="url(#arr-purple)"/>

    <!-- Wire 6: Interconnect -> UART (x=1140 to 1220, y=610 to 250) -->
    <path d="M 1140 610 L 1180 610 L 1180 250 L 1220 250" stroke="#2563eb" stroke-width="2.5" fill="none" marker-end="url(#arr-blue)"/>

    <!-- Wire 7: UART -> soc_regs (Vertical in Col 3: y=390 down to 440 at x=1465) -->
    <path d="M 1465 390 L 1465 440" stroke="#2563eb" stroke-width="3.5" fill="none" marker-end="url(#arr-blue)"/>

    <!-- Wire 8: soc_regs -> App (Vertical in Col 3: y=730 down to 780 at x=1465) -->
    <path d="M 1465 730 L 1465 780" stroke="#059669" stroke-width="3.5" fill="none" marker-end="url(#arr-green)"/>

    <!-- Wire 9: start.s -> App (Bottom bridge: x=530 to 1220 at y=925) -->
    <path d="M 530 925 L 1220 925" stroke="#e11d48" stroke-width="3.5" fill="none" marker-end="url(#arr-rose)"/>
  </svg>

  <!-- Badges -->
  <div class="badge" style="left: 125px; top: 405px; color: #b45309; border: 1.5px solid #d97706;">
    Khớp Khởi Động: PROGADDR_RESET = FLASH ORIGIN = 0x0025_0000
  </div>

  <div class="badge" style="left: 128px; top: 745px; color: #059669; border: 1.5px solid #059669;">
    Khởi Tạo Ngăn Xếp: _stack_top (0x0400) -> lui sp, %hi(_stack_top)
  </div>

  <div class="badge" style="left: 545px; top: 350px; color: #b45309; border: 1.5px solid #d97706;">
    Flash XIP: 0x0010_0000..0x00FF_FFFF
  </div>

  <div class="badge" style="left: 775px; top: 405px; color: #c2410c; border: 1.5px solid #ea580c;">
    sel_spimem (Đọc Opcode XIP)
  </div>

  <div class="badge" style="left: 710px; top: 795px; color: #581c87; border: 1.5px solid #7c3aed;">
    sel_spicfg: Bit-bang Ghi Flash (0x0200_0000) từ RAM Routine
  </div>

  <div class="badge" style="left: 1140px; top: 350px; color: #1e3a8a; border: 1.5px solid #2563eb;">
    sel_rfid (0x1000_0000) & sel_uart (0x3000_0000)
  </div>

  <div class="badge" style="left: 1275px; top: 405px; color: #1e3a8a; border: 1.5px solid #2563eb;">
    Ánh Xạ MMIO: Offset 0x00 (Divider) & 0x04 (Data FIFO 32B)
  </div>

  <div class="badge" style="left: 1285px; top: 745px; color: #065f46; border: 1.5px solid #059669;">
    REG_RFID_UART_DAT (Đọc Thẻ) & REG_GPIO_LEDS (Mở Chốt)
  </div>

  <div class="badge" style="left: 720px; top: 910px; color: #9f1239; border: 1.5px solid #e11d48; font-size: 12px;">
    Bàn Giao Quyền Điều Khiển: call main() -> access_control_poll()
  </div>

  <!-- CARD 1: rdm6300_picorv32_soc.v -->
  <div class="card theme-blue" style="left: 40px; top: 110px; width: 490px; height: 280px;">
    <div class="card-title">1. rtl/rdm6300_picorv32_soc.v</div>
    <div class="card-sub">[RTL Top Module - Cấu hình vi hệ thống phần cứng]</div>
    <div class="divider"></div>
    <div class="code-box">
<span style="color:#0284c7;font-weight:bold;">parameter</span> [31:0] <b style="color:#d97706;">PROGADDR_RESET</b> = 32'h0025_0000;<br>
<span style="color:#0284c7;font-weight:bold;">parameter</span> [31:0] <b style="color:#059669;">STACKADDR</b>      = 32'h0000_0400;<br>
<span style="color:#0284c7;font-weight:bold;">parameter</span> [0:0]  COMPRESSED_ISA = 1'b0;<br><br>
picorv32 #(<br>
&nbsp;&nbsp;.<b style="color:#d97706;">PROGADDR_RESET</b>(PROGADDR_RESET),<br>
&nbsp;&nbsp;.<b style="color:#059669;">STACKADDR</b>(STACKADDR)<br>
) cpu (<br>
&nbsp;&nbsp;.clk(clk), .resetn(resetn),<br>
&nbsp;&nbsp;.mem_valid(mem_valid), .mem_ready(mem_ready),<br>
&nbsp;&nbsp;.mem_addr(mem_addr), .mem_rdata(mem_rdata)<br>
);
    </div>
    <div class="card-footer">
      • <b>PROGADDR_RESET</b>: Ép CPU nhả reset nạp opcode từ Flash XIP.<br>
      • <b>STACKADDR</b>: Đặt mốc đỉnh 1KB SRAM nội bộ tốc độ cao.
    </div>
  </div>

  <!-- CARD 2: sections.lds -->
  <div class="card theme-green" style="left: 40px; top: 440px; width: 490px; height: 290px;">
    <div class="card-title">2. firmware/sections.lds</div>
    <div class="card-sub">[GNU Linker Script - Kịch bản phân bổ bộ nhớ biên dịch]</div>
    <div class="divider"></div>
    <div class="code-box">
<b>MEMORY</b> {<br>
&nbsp;&nbsp;<b style="color:#d97706;">FLASH</b> (rx) : ORIGIN = <b style="color:#d97706;">0x00250000</b>, LENGTH = 704K<br>
&nbsp;&nbsp;<b style="color:#059669;">RAM</b>   (rwx): ORIGIN = 0x00000000, LENGTH = 1K<br>
}<br><br>
.text : {<br>
&nbsp;&nbsp;*(.text.start)<br>
&nbsp;&nbsp;*(.text*)<br>
} &gt; <b style="color:#d97706;">FLASH</b><br><br>
<b style="color:#059669;">_stack_top</b> = <b style="color:#059669;">0x00000400</b>; <span style="color:#047857;">/* Khớp STACKADDR phần cứng */</span>
    </div>
    <div class="card-footer">
      • <b>FLASH ORIGIN</b>: Định vị mã C (.text) trùng khớp PROGADDR_RESET RTL.<br>
      • <b>_stack_top</b>: Xuất nhãn đỉnh SRAM cho file start.s nạp vào thanh ghi sp.
    </div>
  </div>

  <!-- CARD 3: start.s -->
  <div class="card theme-purple" style="left: 40px; top: 780px; width: 490px; height: 290px;">
    <div class="card-title">3. firmware/start.s</div>
    <div class="card-sub">[Assembly Bootstrap - Mã khởi động đầu tiên nạp sp]</div>
    <div class="divider"></div>
    <div class="code-box">
.global _start<br>
_start:<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#7c3aed;font-weight:bold;">lui</span>  sp, %hi(<b style="color:#059669;">_stack_top</b>)       <span style="color:#6b21a8;"># Nạp 20-bit cao (0x00000400)</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#7c3aed;font-weight:bold;">addi</span> sp, sp, %lo(<b style="color:#059669;">_stack_top</b>)   <span style="color:#6b21a8;"># Nạp 12-bit thấp</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#2563eb;font-weight:bold;">call</span> <b style="color:#e11d48;">main</b>                      <span style="color:#6b21a8;"># Bàn giao quyền sang hàm main()</span><br><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#ef4444;font-weight:bold;">ebreak</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#7c3aed;font-weight:bold;">j</span>    _start               <span style="color:#6b21a8;"># Trap an toàn bảo vệ CPU</span>
    </div>
    <div class="card-footer">
      • Khởi tạo con trỏ ngăn xếp phần cứng sp trỏ vào đỉnh 1KB SRAM.<br>
      • Hoàn tất chu trình bootstrap chỉ trong đúng 2 chu kỳ lệnh RISC-V.
    </div>
  </div>

  <!-- CARD 4: spimemio.v -->
  <div class="card theme-amber" style="left: 610px; top: 110px; width: 530px; height: 280px;">
    <div class="card-title">4. rtl/core/spimemio.v</div>
    <div class="card-sub">[SPI Flash Controller - Bộ điều khiển Flash XIP & Bit-bang]</div>
    <div class="divider"></div>
    <div class="code-box">
<span style="color:#0284c7;font-weight:bold;">module</span> spimemio (<br>
&nbsp;&nbsp;<span style="color:#0284c7;">input</span> valid, <span style="color:#0284c7;">output</span> ready, <span style="color:#0284c7;">input</span> [23:0] addr,<br>
&nbsp;&nbsp;<span style="color:#0284c7;">output reg</span> [31:0] rdata,<br>
&nbsp;&nbsp;<span style="color:#0284c7;">output</span> flash_csb, flash_clk, <span style="color:#0284c7;">inout</span> [3:0] flash_io,<br>
&nbsp;&nbsp;<span style="color:#0284c7;">input</span> [3:0] <b style="color:#e11d48;">cfgreg_we</b>, <span style="color:#0284c7;">input</span> [31:0] cfgreg_di, <span style="color:#0284c7;">output</span> [31:0] cfgreg_do<br>
);<br><br>
<span style="color:#0284c7;font-weight:bold;">assign</span> ready = valid &amp;&amp; (addr == rd_addr) &amp;&amp; rd_valid; <span style="color:#b45309;">// XIP Hit</span><br>
<span style="color:#0284c7;font-weight:bold;">assign</span> cfgreg_do[5] = flash_csb; <span style="color:#b45309;">// Kênh Bit-bang MMIO</span>
    </div>
    <div class="card-footer">
      • <b>Đọc XIP</b>: Tự động sinh xung kéo opcode 32-bit trả về cho CPU.<br>
      • <b>SPICFG (0x0200_0000)</b>: Kênh bit-bang phục vụ ghi Sector thẻ & Log.
    </div>
  </div>

  <!-- CARD 5: soc_interconnect.v -->
  <div class="card theme-orange" style="left: 610px; top: 440px; width: 530px; height: 340px;">
    <div class="card-title">5. rtl/core/soc_interconnect.v</div>
    <div class="card-sub">[Bus Interconnect & Matrix - Bộ giải mã địa chỉ trung tâm]</div>
    <div class="divider"></div>
    <div class="code-box">
<span style="color:#0284c7;font-weight:bold;">assign</span> <b style="color:#059669;">sel_sram</b>   = cpu_mem_valid &amp;&amp; (cpu_mem_addr &lt; <b style="color:#059669;">32'h0000_0400</b>);<br>
<span style="color:#0284c7;font-weight:bold;">assign</span> <b style="color:#d97706;">sel_spimem</b> = cpu_mem_valid &amp;&amp; (cpu_mem_addr &gt;= <b style="color:#d97706;">32'h0010_0000</b> &amp;&amp;<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;cpu_mem_addr &lt;  <b style="color:#d97706;">32'h0100_0000</b>);<br>
<span style="color:#0284c7;font-weight:bold;">assign</span> <b style="color:#e11d48;">sel_spicfg</b> = cpu_mem_valid &amp;&amp; (cpu_mem_addr == <b style="color:#e11d48;">32'h0200_0000</b>);<br>
<span style="color:#0284c7;font-weight:bold;">assign</span> <b style="color:#b45309;">sel_rfid</b>   = cpu_mem_valid &amp;&amp; (cpu_mem_addr[31:28] == <b style="color:#b45309;">4'h1</b>);<br>
<span style="color:#0284c7;font-weight:bold;">assign</span> <b style="color:#2563eb;">sel_uart</b>   = cpu_mem_valid &amp;&amp; (cpu_mem_addr[31:28] == <b style="color:#2563eb;">4'h3</b>);<br>
<span style="color:#0284c7;font-weight:bold;">assign</span> <b style="color:#7c3aed;">sel_gpio</b>   = cpu_mem_valid &amp;&amp; (cpu_mem_addr[31:28] == <b style="color:#7c3aed;">4'h4</b>);<br><br>
<span style="color:#0284c7;font-weight:bold;">assign</span> cpu_mem_ready = sram_ready || spimem_ready || sel_spicfg ||<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;rfid_ready || uart_ready   || gpio_ready;
    </div>
    <div class="card-footer">
      • <b>0-Delay Muxing</b>: Giải mã tiền tố 4-bit phân luồng tức thì trong 0 chu kỳ.<br>
      • <b>Zero Wait-State</b>: Không bao giờ stall CPU khi giao tiếp MMIO ngoại vi.
    </div>
  </div>

  <!-- CARD 6: flash.c -->
  <div class="card theme-purple" style="left: 610px; top: 830px; width: 530px; height: 240px;">
    <div class="card-title">6. firmware/flash.c & start.s</div>
    <div class="card-sub">[RAM Execution Routine - Nhảy sang SRAM ghi Flash]</div>
    <div class="divider"></div>
    <div class="code-box">
<span style="color:#7c3aed;font-weight:bold;">flashio_worker</span>:<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#7c3aed;font-weight:bold;">li</span> t0, <b style="color:#e11d48;">0x02000000</b>  <span style="color:#6b21a8;"># Ghi Bit-bang SPI MMIO</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#7c3aed;font-weight:bold;">sh</span> t1, 0(t0)<br><br>
<span style="color:#0284c7;font-weight:bold;">static void</span> <b>flashio</b>(uint8_t *data, int len, uint8_t wrencmd) {<br>
&nbsp;&nbsp;<span style="color:#059669;">// 1. Sao chép worker lên Stack SRAM (&lt; 0x0000_0400)</span><br>
&nbsp;&nbsp;<span style="color:#059669;">// 2. CPU nhảy sang SRAM chạy để xóa Sector / ghi Trang</span><br>
&nbsp;&nbsp;<span style="color:#059669;">// 3. Sau khi ghi xong Sector 48 (Thẻ) / 49 (Log), quay lại XIP</span><br>
}
    </div>
    <div class="card-footer">
      • <b>Giải quyết xung đột XIP</b>: Không thể vừa nạp lệnh vừa xóa Flash ngoài.
    </div>
  </div>

  <!-- CARD 7: uart_mmio.v -->
  <div class="card theme-blue" style="left: 1220px; top: 110px; width: 490px; height: 280px;">
    <div class="card-title">7. rtl/uart/uart_mmio.v</div>
    <div class="card-sub">[Dual UART MMIO Controller - Bộ đệm phần cứng 32B FIFO]</div>
    <div class="divider"></div>
    <div class="code-box">
<span style="color:#0284c7;font-weight:bold;">wire</span> reg_div_sel = valid &amp;&amp; (addr[2] == <b style="color:#0f172a;">1'b0</b>); <span style="color:#64748B;">// 0x00: Baud</span><br>
<span style="color:#0284c7;font-weight:bold;">wire</span> reg_dat_sel = valid &amp;&amp; (addr[2] == <b style="color:#0f172a;">1'b1</b>); <span style="color:#64748B;">// 0x04: Data</span><br><br>
<span style="color:#0284c7;font-weight:bold;">assign</span> reg_dat_do = fifo_empty ? <b style="color:#e11d48;">32'hFFFFFFFF</b> :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{24'd0, fifo_dout};<br>
<span style="color:#0284c7;font-weight:bold;">assign</span> ready = 1'b1; <span style="color:#64748B;">// Zero Wait-state response</span>
    </div>
    <div class="card-footer">
      • <b>Đọc không khóa</b>: Có dữ liệu trả mã ký tự, rỗng trả về 0xFFFFFFFF.<br>
      • <b>FIFO 32 Byte</b>: Hứng trọn chuỗi 14 byte thẻ RFID RDM6300.
    </div>
  </div>

  <!-- CARD 8: soc_regs.h -->
  <div class="card theme-green" style="left: 1220px; top: 440px; width: 490px; height: 290px;">
    <div class="card-title">8. firmware/common/soc_regs.h</div>
    <div class="card-sub">[Firmware Hardware Memory Map - Định nghĩa con trỏ C]</div>
    <div class="divider"></div>
    <div class="code-box">
<span style="color:#0284c7;font-weight:bold;">#define</span> <b style="color:#b45309;">REG_RFID_UART_DIV</b> (*(<span style="color:#0284c7;">volatile uint32_t*</span>)<b style="color:#b45309;">0x10000000</b>)<br>
<span style="color:#0284c7;font-weight:bold;">#define</span> <b style="color:#b45309;">REG_RFID_UART_DAT</b> (*(<span style="color:#0284c7;">volatile uint32_t*</span>)<b style="color:#b45309;">0x10000004</b>)<br>
<span style="color:#0284c7;font-weight:bold;">#define</span> <b style="color:#2563eb;">REG_PC_UART_DIV</b>   (*(<span style="color:#0284c7;">volatile uint32_t*</span>)<b style="color:#2563eb;">0x30000000</b>)<br>
<span style="color:#0284c7;font-weight:bold;">#define</span> <b style="color:#2563eb;">REG_PC_UART_DAT</b>   (*(<span style="color:#0284c7;">volatile uint32_t*</span>)<b style="color:#2563eb;">0x30000004</b>)<br>
<span style="color:#0284c7;font-weight:bold;">#define</span> <b style="color:#7c3aed;">REG_GPIO_LEDS</b>     (*(<span style="color:#0284c7;">volatile uint32_t*</span>)<b style="color:#7c3aed;">0x40000000</b>)
    </div>
    <div class="card-footer">
      • <b>volatile</b>: Ép GCC luôn phát sinh lệnh load/store bus, không cache CPU.<br>
      • Khớp 100% với các tín hiệu sel_rfid, sel_uart, sel_gpio của Interconnect.
    </div>
  </div>

  <!-- CARD 9: access_control.c -->
  <div class="card theme-green" style="left: 1220px; top: 780px; width: 490px; height: 290px;">
    <div class="card-title">9. firmware/access_control.c</div>
    <div class="card-sub">[Application Logic - Polling thẻ RFID & Điều khiển cửa]</div>
    <div class="divider"></div>
    <div class="code-box">
<span style="color:#0284c7;font-weight:bold;">void</span> <b>access_control_poll</b>(void) {<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#0284c7;">uint32_t</span> d = <b style="color:#b45309;">REG_RFID_UART_DAT</b>; <span style="color:#047857;">// Đọc FIFO (Non-blocking)</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#e11d48;font-weight:bold;">if</span> (d != <b style="color:#e11d48;">0xFFFFFFFF</b>) {<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;rdm6300_push((<span style="color:#0284c7;">uint8_t</span>)d);  <span style="color:#047857;">// Nạp vào parser kiểm tra XOR</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;}<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#047857;">// Khi thẻ hợp lệ trong Whitelist: Mở relay chốt cửa</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<b style="color:#7c3aed;">REG_GPIO_LEDS</b> = (<b style="color:#7c3aed;">REG_GPIO_LEDS</b> &amp; ~0x0002) | <b style="color:#059669;">0x0004</b>;<br>
}
    </div>
    <div class="card-footer">
      • Vòng lặp polling liên tục không bị block nhờ FIFO phần cứng 32B.<br>
      • Phản hồi mở cửa chưa đầy 10 µs ngay khi nhận đủ chuỗi mã thẻ.
    </div>
  </div>

</body>
</html>
"""

html_path = r"d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\firmware_soc_codesign.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"[SUCCESS] Written HTML source to: {html_path}")

# Render to PNG
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out_img = r"d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\firmware_soc_codesign.png"

cmd = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--force-device-scale-factor=2",
    f"--screenshot={out_img}",
    "--window-size=1750,1120",
    f"file:///{html_path.replace(os.sep, '/')}"
]

res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0 and os.path.exists(out_img):
    print(f"[SUCCESS] Generated ultra-sharp 2x DPI image: {out_img} ({os.path.getsize(out_img)} bytes)")
else:
    print("[ERROR] Chrome rendering failed:", res.stderr)
