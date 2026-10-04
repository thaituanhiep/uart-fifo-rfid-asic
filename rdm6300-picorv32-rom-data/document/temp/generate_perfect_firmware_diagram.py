# -*- coding: utf-8 -*-
"""
Perfect Layout Generator for:
1. firmware_soc_codesign.drawio (Draw.io genuine XML)
2. soc_codesign_architecture.drawio (Draw.io genuine XML)
3. firmware_soc_codesign.png (2x DPI vector render)
"""
import os
import subprocess

def generate_both():
    # -------------------------------------------------------------
    # 1. DRAW.IO XML GENERATION (Exact parent="1", generous clearances)
    # -------------------------------------------------------------
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="2026-10-04T13:00:00.000Z" agent="Mozilla/5.0" version="21.0.0" type="device">
  <diagram id="firmware_soc_codesign" name="Firmware Co-Design Architecture">
    <mxGraphModel dx="1600" dy="1100" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1780" pageHeight="1240" math="0" shadow="1">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- 0. TIÊU ĐỀ BẢN VẼ -->
        <mxCell id="title_banner" value="&lt;b style=&quot;font-size:22px;color:#0f172a;&quot;&gt;SƠ ĐỒ LIÊN KẾT MÃ NGUỒN CẤU HÌNH &amp;amp; THỰC THI HỆ THỐNG FIRMWARE TRÊN PHẦN CỨNG SOC&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:14px;color:#475569;&quot;&gt;Đối chiếu trực tiếp từng đoạn code quan trọng: RTL Top, Linker Script, Assembly, Flash XIP, Bus Interconnect, Driver C &amp;amp; App&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#cbd5e1;strokeWidth=2;fontFamily=Segoe UI;shadow=1;" vertex="1" parent="1">
          <mxGeometry x="40" y="20" width="1700" height="70" as="geometry" />
        </mxCell>

        <!-- ============================================================= -->
        <!-- CỘT 1: KHỞI ĐỘNG VẬT LÝ & BIÊN DỊCH                           -->
        <!-- ============================================================= -->

        <!-- CARD 1: rdm6300_picorv32_soc.v -->
        <mxCell id="card_top" value="&lt;b style=&quot;font-size:16px;color:#1e3a8a;&quot;&gt;1. rtl/rdm6300_picorv32_soc.v&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:12px;color:#2563eb;&quot;&gt;&lt;b&gt;[RTL Top Module - Cấu hình vi hệ thống phần cứng]&lt;/b&gt;&lt;/span&gt;&lt;br&gt;&lt;hr style=&quot;border:1px solid #93c5fd;&quot;&gt;&lt;div style=&quot;text-align:left;font-family:Consolas;font-size:11.5px;color:#0f172a;line-height:1.5;&quot;&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;parameter&lt;/b&gt;&lt;/font&gt; [31:0] &lt;b&gt;&lt;font color=&quot;#d97706&quot;&gt;PROGADDR_RESET&lt;/font&gt;&lt;/b&gt; = 32&#39;h0025_0000;&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;parameter&lt;/b&gt;&lt;/font&gt; [31:0] &lt;b&gt;&lt;font color=&quot;#059669&quot;&gt;STACKADDR&lt;/font&gt;&lt;/b&gt;      = 32&#39;h0000_0400;&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;parameter&lt;/b&gt;&lt;/font&gt; [0:0]  COMPRESSED_ISA = 1&#39;b0;&lt;br&gt;&lt;br&gt;picorv32 #(&lt;br&gt;  .&lt;b&gt;&lt;font color=&quot;#d97706&quot;&gt;PROGADDR_RESET&lt;/font&gt;&lt;/b&gt;(PROGADDR_RESET),&lt;br&gt;  .&lt;b&gt;&lt;font color=&quot;#059669&quot;&gt;STACKADDR&lt;/font&gt;&lt;/b&gt;(STACKADDR)&lt;br&gt;) cpu (&lt;br&gt;  .clk(clk), .resetn(resetn),&lt;br&gt;  .mem_valid(mem_valid), .mem_ready(mem_ready),&lt;br&gt;  .mem_addr(mem_addr), .mem_rdata(mem_rdata)&lt;br&gt;);&lt;/div&gt;&lt;hr style=&quot;border:1px solid #bfdbfe;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:11px;color:#1e3a8a;&quot;&gt;&amp;bull; &lt;b&gt;PROGADDR_RESET&lt;/b&gt;: Ép CPU nhả reset nạp opcode từ Flash XIP.&lt;br&gt;&amp;bull; &lt;b&gt;STACKADDR&lt;/b&gt;: Đặt mốc đỉnh 1KB SRAM nội bộ tốc độ cao.&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dbeafe;strokeColor=#2563eb;strokeWidth=2;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=10;" vertex="1" parent="1">
          <mxGeometry x="40" y="110" width="490" height="315" as="geometry" />
        </mxCell>

        <!-- CARD 2: sections.lds -->
        <mxCell id="card_lds" value="&lt;b style=&quot;font-size:16px;color:#065f46;&quot;&gt;2. firmware/sections.lds&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:12px;color:#059669;&quot;&gt;&lt;b&gt;[GNU Linker Script - Kịch bản phân bổ bộ nhớ biên dịch]&lt;/b&gt;&lt;/span&gt;&lt;br&gt;&lt;hr style=&quot;border:1px solid #6ee7b7;&quot;&gt;&lt;div style=&quot;text-align:left;font-family:Consolas;font-size:11.5px;color:#064e3b;line-height:1.5;&quot;&gt;&lt;b&gt;MEMORY&lt;/b&gt; {&lt;br&gt;  &lt;b&gt;&lt;font color=&quot;#d97706&quot;&gt;FLASH&lt;/font&gt;&lt;/b&gt; (rx) : ORIGIN = &lt;b&gt;&lt;font color=&quot;#d97706&quot;&gt;0x00250000&lt;/font&gt;&lt;/b&gt;, LENGTH = 704K&lt;br&gt;  &lt;b&gt;&lt;font color=&quot;#059669&quot;&gt;RAM&lt;/font&gt;&lt;/b&gt;   (rwx): ORIGIN = 0x00000000, LENGTH = 1K&lt;br&gt;}&lt;br&gt;&lt;br&gt;.text : {&lt;br&gt;  *(.text.start)&lt;br&gt;  *(.text*)&lt;br&gt;} &amp;gt; &lt;b&gt;&lt;font color=&quot;#d97706&quot;&gt;FLASH&lt;/font&gt;&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;b&gt;&lt;font color=&quot;#059669&quot;&gt;_stack_top&lt;/font&gt;&lt;/b&gt; = &lt;b&gt;&lt;font color=&quot;#059669&quot;&gt;0x00000400&lt;/font&gt;&lt;/b&gt;; &lt;font color=&quot;#047857&quot;&gt;/* Khớp STACKADDR phần cứng */&lt;/font&gt;&lt;/div&gt;&lt;hr style=&quot;border:1px solid #a7f3d0;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:11px;color:#065f46;&quot;&gt;&amp;bull; &lt;b&gt;FLASH ORIGIN&lt;/b&gt;: Định vị mã C (.text) trùng khớp PROGADDR_RESET RTL.&lt;br&gt;&amp;bull; &lt;b&gt;_stack_top&lt;/b&gt;: Xuất nhãn đỉnh SRAM cho file start.s nạp vào thanh ghi sp.&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d1fae5;strokeColor=#10b981;strokeWidth=2;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=10;" vertex="1" parent="1">
          <mxGeometry x="40" y="480" width="490" height="300" as="geometry" />
        </mxCell>

        <!-- CARD 3: start.s -->
        <mxCell id="card_start" value="&lt;b style=&quot;font-size:16px;color:#581c87;&quot;&gt;3. firmware/start.s&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:12px;color:#7c3aed;&quot;&gt;&lt;b&gt;[Assembly Bootstrap - Mã khởi động đầu tiên nạp sp]&lt;/b&gt;&lt;/span&gt;&lt;br&gt;&lt;hr style=&quot;border:1px solid #c084fc;&quot;&gt;&lt;div style=&quot;text-align:left;font-family:Consolas;font-size:11.5px;color:#3b0764;line-height:1.55;&quot;&gt;.global _start&lt;br&gt;_start:&lt;br&gt;    &lt;font color=&quot;#7c3aed&quot;&gt;&lt;b&gt;lui&lt;/b&gt;&lt;/font&gt;  sp, %hi(&lt;b&gt;&lt;font color=&quot;#059669&quot;&gt;_stack_top&lt;/font&gt;&lt;/b&gt;)       &lt;font color=&quot;#6b21a8&quot;&gt;# Nạp 20-bit cao (0x00000400)&lt;/font&gt;&lt;br&gt;    &lt;font color=&quot;#7c3aed&quot;&gt;&lt;b&gt;addi&lt;/b&gt;&lt;/font&gt; sp, sp, %lo(&lt;b&gt;&lt;font color=&quot;#059669&quot;&gt;_stack_top&lt;/font&gt;&lt;/b&gt;)   &lt;font color=&quot;#6b21a8&quot;&gt;# Nạp 12-bit thấp&lt;/font&gt;&lt;br&gt;    &lt;font color=&quot;#2563eb&quot;&gt;&lt;b&gt;call&lt;/b&gt;&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#e11d48&quot;&gt;main&lt;/font&gt;&lt;/b&gt;                      &lt;font color=&quot;#6b21a8&quot;&gt;# Bàn giao quyền sang hàm main()&lt;/font&gt;&lt;br&gt;&lt;br&gt;    &lt;font color=&quot;#ef4444&quot;&gt;&lt;b&gt;ebreak&lt;/b&gt;&lt;/font&gt;&lt;br&gt;    &lt;font color=&quot;#7c3aed&quot;&gt;&lt;b&gt;j&lt;/b&gt;&lt;/font&gt;    _start               &lt;font color=&quot;#6b21a8&quot;&gt;# Trap an toàn bảo vệ CPU&lt;/font&gt;&lt;/div&gt;&lt;hr style=&quot;border:1px solid #e9d5ff;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:11px;color:#581c87;&quot;&gt;&amp;bull; Khởi tạo con trỏ ngăn xếp phần cứng sp trỏ vào đỉnh 1KB SRAM.&lt;br&gt;&amp;bull; Hoàn tất chu trình bootstrap chỉ trong đúng 2 chu kỳ lệnh RISC-V.&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f3e8ff;strokeColor=#9333ea;strokeWidth=2;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=10;" vertex="1" parent="1">
          <mxGeometry x="40" y="835" width="490" height="275" as="geometry" />
        </mxCell>

        <!-- ============================================================= -->
        <!-- CỘT 2: TRÁI TIM ĐIỀU PHỐI BUS & BỘ NHỚ                        -->
        <!-- ============================================================= -->

        <!-- CARD 4: spimemio.v -->
        <mxCell id="card_spimem" value="&lt;b style=&quot;font-size:16px;color:#78350f;&quot;&gt;4. rtl/core/spimemio.v&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:12px;color:#b45309;&quot;&gt;&lt;b&gt;[SPI Flash Controller - Bộ điều khiển Flash XIP &amp;amp; Bit-bang]&lt;/b&gt;&lt;/span&gt;&lt;br&gt;&lt;hr style=&quot;border:1px solid #fde68a;&quot;&gt;&lt;div style=&quot;text-align:left;font-family:Consolas;font-size:11.5px;color:#451a03;line-height:1.5;&quot;&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;module&lt;/b&gt;&lt;/font&gt; spimemio (&lt;br&gt;  &lt;font color=&quot;#0284c7&quot;&gt;input&lt;/font&gt; valid, &lt;font color=&quot;#0284c7&quot;&gt;output&lt;/font&gt; ready, &lt;font color=&quot;#0284c7&quot;&gt;input&lt;/font&gt; [23:0] addr,&lt;br&gt;  &lt;font color=&quot;#0284c7&quot;&gt;output reg&lt;/font&gt; [31:0] rdata,&lt;br&gt;  &lt;font color=&quot;#0284c7&quot;&gt;output&lt;/font&gt; flash_csb, flash_clk, &lt;font color=&quot;#0284c7&quot;&gt;inout&lt;/font&gt; [3:0] flash_io,&lt;br&gt;  &lt;font color=&quot;#0284c7&quot;&gt;input&lt;/font&gt; [3:0] &lt;b&gt;&lt;font color=&quot;#e11d48&quot;&gt;cfgreg_we&lt;/font&gt;&lt;/b&gt;, &lt;font color=&quot;#0284c7&quot;&gt;input&lt;/font&gt; [31:0] cfgreg_di, &lt;font color=&quot;#0284c7&quot;&gt;output&lt;/font&gt; [31:0] cfgreg_do&lt;br&gt;);&lt;br&gt;&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;assign&lt;/b&gt;&lt;/font&gt; ready = valid &amp;amp;&amp;amp; (addr == rd_addr) &amp;amp;&amp;amp; rd_valid; &lt;font color=&quot;#b45309&quot;&gt;// XIP Hit&lt;/font&gt;&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;assign&lt;/b&gt;&lt;/font&gt; cfgreg_do[5] = flash_csb; &lt;font color=&quot;#b45309&quot;&gt;// Kênh Bit-bang MMIO&lt;/font&gt;&lt;/div&gt;&lt;hr style=&quot;border:1px solid #fef3c7;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:11px;color:#78350f;&quot;&gt;&amp;bull; &lt;b&gt;Đọc XIP&lt;/b&gt;: Tự động sinh xung kéo opcode 32-bit trả về cho CPU.&lt;br&gt;&amp;bull; &lt;b&gt;SPICFG (0x0200_0000)&lt;/b&gt;: Kênh bit-bang phục vụ ghi Sector thẻ &amp;amp; Log.&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fef3c7;strokeColor=#d97706;strokeWidth=2;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=10;" vertex="1" parent="1">
          <mxGeometry x="640" y="110" width="510" height="315" as="geometry" />
        </mxCell>

        <!-- CARD 5: soc_interconnect.v -->
        <mxCell id="card_ic" value="&lt;b style=&quot;font-size:16px;color:#7c2d12;&quot;&gt;5. rtl/core/soc_interconnect.v&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:12px;color:#ea580c;&quot;&gt;&lt;b&gt;[Bus Interconnect &amp;amp; Matrix - Bộ giải mã địa chỉ trung tâm]&lt;/b&gt;&lt;/span&gt;&lt;br&gt;&lt;hr style=&quot;border:1px solid #fdba74;&quot;&gt;&lt;div style=&quot;text-align:left;font-family:Consolas;font-size:11.5px;color:#431407;line-height:1.5;&quot;&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;assign&lt;/b&gt;&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#059669&quot;&gt;sel_sram&lt;/font&gt;&lt;/b&gt;   = cpu_mem_valid &amp;amp;&amp;amp; (cpu_mem_addr &amp;lt; &lt;b&gt;32&#39;h0000_0400&lt;/b&gt;);&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;assign&lt;/b&gt;&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#d97706&quot;&gt;sel_spimem&lt;/font&gt;&lt;/b&gt; = cpu_mem_valid &amp;amp;&amp;amp; (cpu_mem_addr &amp;gt;= &lt;b&gt;32&#39;h0010_0000&lt;/b&gt; &amp;amp;&amp;amp;&lt;br&gt;                                          cpu_mem_addr &amp;lt;  &lt;b&gt;32&#39;h0100_0000&lt;/b&gt;);&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;assign&lt;/b&gt;&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#e11d48&quot;&gt;sel_spicfg&lt;/font&gt;&lt;/b&gt; = cpu_mem_valid &amp;amp;&amp;amp; (cpu_mem_addr == &lt;b&gt;32&#39;h0200_0000&lt;/b&gt;);&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;assign&lt;/b&gt;&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#b45309&quot;&gt;sel_rfid&lt;/font&gt;&lt;/b&gt;   = cpu_mem_valid &amp;amp;&amp;amp; (cpu_mem_addr[31:28] == &lt;b&gt;4&#39;h1&lt;/b&gt;);&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;assign&lt;/b&gt;&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#2563eb&quot;&gt;sel_uart&lt;/font&gt;&lt;/b&gt;   = cpu_mem_valid &amp;amp;&amp;amp; (cpu_mem_addr[31:28] == &lt;b&gt;4&#39;h3&lt;/b&gt;);&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;assign&lt;/b&gt;&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#7c3aed&quot;&gt;sel_gpio&lt;/font&gt;&lt;/b&gt;   = cpu_mem_valid &amp;amp;&amp;amp; (cpu_mem_addr[31:28] == &lt;b&gt;4&#39;h4&lt;/b&gt;);&lt;br&gt;&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;assign&lt;/b&gt;&lt;/font&gt; cpu_mem_ready = sram_ready || spimem_ready || sel_spicfg ||&lt;br&gt;                       rfid_ready || uart_ready   || gpio_ready;&lt;/div&gt;&lt;hr style=&quot;border:1px solid #ffedd5;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:11px;color:#7c2d12;&quot;&gt;&amp;bull; &lt;b&gt;0-Delay Muxing&lt;/b&gt;: Giải mã tiền tố 4-bit phân luồng tức thì trong 0 chu kỳ.&lt;br&gt;&amp;bull; &lt;b&gt;Zero Wait-State&lt;/b&gt;: Không bao giờ stall CPU khi giao tiếp MMIO ngoại vi.&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffedd5;strokeColor=#ea580c;strokeWidth=2;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=10;" vertex="1" parent="1">
          <mxGeometry x="640" y="480" width="510" height="330" as="geometry" />
        </mxCell>

        <!-- CARD 6: flash.c -->
        <mxCell id="card_flashc" value="&lt;b style=&quot;font-size:16px;color:#581c87;&quot;&gt;6. firmware/flash.c &amp;amp; start.s&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:12px;color:#7c3aed;&quot;&gt;&lt;b&gt;[RAM Execution Routine - Nhảy sang SRAM ghi Flash]&lt;/b&gt;&lt;/span&gt;&lt;br&gt;&lt;hr style=&quot;border:1px solid #c084fc;&quot;&gt;&lt;div style=&quot;text-align:left;font-family:Consolas;font-size:11.5px;color:#3b0764;line-height:1.5;&quot;&gt;&lt;font color=&quot;#7c3aed&quot;&gt;&lt;b&gt;flashio_worker&lt;/b&gt;&lt;/font&gt;:&lt;br&gt;    &lt;font color=&quot;#7c3aed&quot;&gt;&lt;b&gt;li&lt;/b&gt;&lt;/font&gt; t0, &lt;b&gt;&lt;font color=&quot;#e11d48&quot;&gt;0x02000000&lt;/font&gt;&lt;/b&gt;  &lt;font color=&quot;#6b21a8&quot;&gt;# Ghi Bit-bang SPI MMIO&lt;/font&gt;&lt;br&gt;    &lt;font color=&quot;#7c3aed&quot;&gt;&lt;b&gt;sh&lt;/b&gt;&lt;/font&gt; t1, 0(t0)&lt;br&gt;&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;static void&lt;/b&gt;&lt;/font&gt; &lt;b&gt;flashio&lt;/b&gt;(uint8_t *data, int len, uint8_t wrencmd) {&lt;br&gt;  &lt;font color=&quot;#059669&quot;&gt;// 1. Sao chép worker lên Stack SRAM (&amp;lt; 0x0000_0400)&lt;/font&gt;&lt;br&gt;  &lt;font color=&quot;#059669&quot;&gt;// 2. CPU nhảy sang SRAM chạy để xóa Sector / ghi Trang&lt;/font&gt;&lt;br&gt;  &lt;font color=&quot;#059669&quot;&gt;// 3. Sau khi ghi xong Sector 48 (Thẻ) / 49 (Log), quay lại XIP&lt;/font&gt;&lt;br&gt;}&lt;/div&gt;&lt;hr style=&quot;border:1px solid #e9d5ff;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:11px;color:#581c87;&quot;&gt;&amp;bull; &lt;b&gt;Giải quyết xung đột XIP&lt;/b&gt;: Không thể vừa nạp lệnh vừa xóa Flash ngoài.&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f3e8ff;strokeColor=#9333ea;strokeWidth=2;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=10;" vertex="1" parent="1">
          <mxGeometry x="640" y="865" width="510" height="245" as="geometry" />
        </mxCell>

        <!-- ============================================================= -->
        <!-- CỘT 3: TẦNG NGOẠI VI & PHẦN MỀM ỨNG DỤNG                      -->
        <!-- ============================================================= -->

        <!-- CARD 7: uart_mmio.v -->
        <mxCell id="card_uart" value="&lt;b style=&quot;font-size:16px;color:#1e3a8a;&quot;&gt;7. rtl/uart/uart_mmio.v&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:12px;color:#2563eb;&quot;&gt;&lt;b&gt;[Dual UART MMIO Controller - Bộ đệm phần cứng 32B FIFO]&lt;/b&gt;&lt;/span&gt;&lt;br&gt;&lt;hr style=&quot;border:1px solid #93c5fd;&quot;&gt;&lt;div style=&quot;text-align:left;font-family:Consolas;font-size:11.5px;color:#0f172a;line-height:1.5;&quot;&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;wire&lt;/b&gt;&lt;/font&gt; reg_div_sel = valid &amp;amp;&amp;amp; (addr[2] == &lt;b&gt;1&#39;b0&lt;/b&gt;); &lt;font color=&quot;#64748B&quot;&gt;// 0x00: Baud&lt;/font&gt;&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;wire&lt;/b&gt;&lt;/font&gt; reg_dat_sel = valid &amp;amp;&amp;amp; (addr[2] == &lt;b&gt;1&#39;b1&lt;/b&gt;); &lt;font color=&quot;#64748B&quot;&gt;// 0x04: Data&lt;/font&gt;&lt;br&gt;&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;assign&lt;/b&gt;&lt;/font&gt; reg_dat_do = fifo_empty ? &lt;b&gt;&lt;font color=&quot;#e11d48&quot;&gt;32&#39;hFFFFFFFF&lt;/font&gt;&lt;/b&gt; :&lt;br&gt;                                   {24&#39;d0, fifo_dout};&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;assign&lt;/b&gt;&lt;/font&gt; ready = 1&#39;b1; &lt;font color=&quot;#64748B&quot;&gt;// Zero Wait-state response&lt;/font&gt;&lt;/div&gt;&lt;hr style=&quot;border:1px solid #bfdbfe;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:11px;color:#1e3a8a;&quot;&gt;&amp;bull; &lt;b&gt;Đọc không khóa&lt;/b&gt;: Có dữ liệu trả mã ký tự, rỗng trả về 0xFFFFFFFF.&lt;br&gt;&amp;bull; &lt;b&gt;FIFO 32 Byte&lt;/b&gt;: Hứng trọn chuỗi 14 byte thẻ RFID RDM6300.&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dbeafe;strokeColor=#2563eb;strokeWidth=2;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=10;" vertex="1" parent="1">
          <mxGeometry x="1250" y="110" width="490" height="315" as="geometry" />
        </mxCell>

        <!-- CARD 8: soc_regs.h -->
        <mxCell id="card_regs" value="&lt;b style=&quot;font-size:16px;color:#065f46;&quot;&gt;8. firmware/common/soc_regs.h&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:12px;color:#059669;&quot;&gt;&lt;b&gt;[Firmware Hardware Memory Map - Định nghĩa con trỏ C]&lt;/b&gt;&lt;/span&gt;&lt;br&gt;&lt;hr style=&quot;border:1px solid #6ee7b7;&quot;&gt;&lt;div style=&quot;text-align:left;font-family:Consolas;font-size:11.5px;color:#064e3b;line-height:1.5;&quot;&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;#define&lt;/b&gt;&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#b45309&quot;&gt;REG_RFID_UART_DIV&lt;/font&gt;&lt;/b&gt; (*(&lt;font color=&quot;#0284c7&quot;&gt;volatile uint32_t*&lt;/font&gt;)&lt;b&gt;0x10000000&lt;/b&gt;)&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;#define&lt;/b&gt;&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#b45309&quot;&gt;REG_RFID_UART_DAT&lt;/font&gt;&lt;/b&gt; (*(&lt;font color=&quot;#0284c7&quot;&gt;volatile uint32_t*&lt;/font&gt;)&lt;b&gt;0x10000004&lt;/b&gt;)&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;#define&lt;/b&gt;&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#2563eb&quot;&gt;REG_PC_UART_DIV&lt;/font&gt;&lt;/b&gt;   (*(&lt;font color=&quot;#0284c7&quot;&gt;volatile uint32_t*&lt;/font&gt;)&lt;b&gt;0x30000000&lt;/b&gt;)&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;#define&lt;/b&gt;&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#2563eb&quot;&gt;REG_PC_UART_DAT&lt;/font&gt;&lt;/b&gt;   (*(&lt;font color=&quot;#0284c7&quot;&gt;volatile uint32_t*&lt;/font&gt;)&lt;b&gt;0x30000004&lt;/b&gt;)&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;#define&lt;/b&gt;&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#7c3aed&quot;&gt;REG_GPIO_LEDS&lt;/font&gt;&lt;/b&gt;     (*(&lt;font color=&quot;#0284c7&quot;&gt;volatile uint32_t*&lt;/font&gt;)&lt;b&gt;0x40000000&lt;/b&gt;)&lt;/div&gt;&lt;hr style=&quot;border:1px solid #a7f3d0;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:11px;color:#065f46;&quot;&gt;&amp;bull; &lt;b&gt;volatile&lt;/b&gt;: Ép GCC luôn phát sinh lệnh load/store bus, không cache CPU.&lt;br&gt;&amp;bull; Khớp 100% với các tín hiệu sel_rfid, sel_uart, sel_gpio của Interconnect.&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d1fae5;strokeColor=#10b981;strokeWidth=2;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=10;" vertex="1" parent="1">
          <mxGeometry x="1250" y="480" width="490" height="300" as="geometry" />
        </mxCell>

        <!-- CARD 9: access_control.c -->
        <mxCell id="card_app" value="&lt;b style=&quot;font-size:16px;color:#065f46;&quot;&gt;9. firmware/access_control.c&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:12px;color:#059669;&quot;&gt;&lt;b&gt;[Application Logic - Polling thẻ RFID &amp;amp; Điều khiển cửa]&lt;/b&gt;&lt;/span&gt;&lt;br&gt;&lt;hr style=&quot;border:1px solid #6ee7b7;&quot;&gt;&lt;div style=&quot;text-align:left;font-family:Consolas;font-size:11.5px;color:#064e3b;line-height:1.5;&quot;&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;void&lt;/b&gt;&lt;/font&gt; &lt;b&gt;access_control_poll&lt;/b&gt;(void) {&lt;br&gt;    &lt;font color=&quot;#0284c7&quot;&gt;uint32_t&lt;/font&gt; d = &lt;b&gt;&lt;font color=&quot;#b45309&quot;&gt;REG_RFID_UART_DAT&lt;/font&gt;&lt;/b&gt;; &lt;font color=&quot;#047857&quot;&gt;// Đọc FIFO (Non-blocking)&lt;/font&gt;&lt;br&gt;    &lt;font color=&quot;#e11d48&quot;&gt;&lt;b&gt;if&lt;/b&gt;&lt;/font&gt; (d != &lt;b&gt;&lt;font color=&quot;#e11d48&quot;&gt;0xFFFFFFFF&lt;/font&gt;&lt;/b&gt;) {&lt;br&gt;        rdm6300_push((&lt;font color=&quot;#0284c7&quot;&gt;uint8_t&lt;/font&gt;)d);  &lt;font color=&quot;#047857&quot;&gt;// Nạp vào parser kiểm tra XOR&lt;/font&gt;&lt;br&gt;    }&lt;br&gt;&lt;br&gt;    &lt;font color=&quot;#047857&quot;&gt;// Khi thẻ hợp lệ trong Whitelist: Mở relay chốt cửa&lt;/font&gt;&lt;br&gt;    &lt;b&gt;&lt;font color=&quot;#7c3aed&quot;&gt;REG_GPIO_LEDS&lt;/font&gt;&lt;/b&gt; = (&lt;font color=&quot;#7c3aed&quot;&gt;REG_GPIO_LEDS&lt;/font&gt; &amp;amp; ~0x0002) | &lt;b&gt;0x0004&lt;/b&gt;;&lt;br&gt;}&lt;/div&gt;&lt;hr style=&quot;border:1px solid #a7f3d0;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:11px;color:#065f46;&quot;&gt;&amp;bull; Vòng lặp polling liên tục không bị block nhờ FIFO phần cứng 32B.&lt;br&gt;&amp;bull; Phản hồi mở cửa chưa đầy 10 µs ngay khi nhận đủ chuỗi mã thẻ.&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d1fae5;strokeColor=#10b981;strokeWidth=2;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=10;" vertex="1" parent="1">
          <mxGeometry x="1250" y="835" width="490" height="275" as="geometry" />
        </mxCell>

        <!-- ============================================================= -->
        <!-- MŨI TÊN KẾT NỐI CO-DESIGN TRỰC QUAN (CONNECTORS)              -->
        <!-- ============================================================= -->

        <!-- Link 1: Top -> Linker -->
        <mxCell id="edge1" value="&lt;b&gt;Khớp Khởi Động: PROGADDR_RESET = FLASH ORIGIN = 0x0025_0000&lt;/b&gt;" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#d97706;strokeWidth=3;fontColor=#b45309;fontFamily=Segoe UI;fontSize=11.5;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="card_top" target="card_lds">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Link 2: Linker -> Assembly start.s -->
        <mxCell id="edge2" value="&lt;b&gt;Khởi Tạo Ngăn Xếp: _stack_top (0x0400) -&amp;gt; lui sp, %hi(_stack_top)&lt;/b&gt;" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#059669;strokeWidth=3;fontColor=#059669;fontFamily=Segoe UI;fontSize=11.5;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="card_lds" target="card_start">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Link 3: Linker -> Flash Controller (XIP Region) -->
        <mxCell id="edge3" value="&lt;b&gt;Kéo Lệnh Flash XIP: 0x0010_0000 - 0x0100_0000&lt;/b&gt;" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#d97706;strokeWidth=2.5;fontColor=#b45309;fontFamily=Segoe UI;fontSize=11;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="card_lds" target="card_spimem">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="585" y="630" />
              <mxPoint x="585" y="265" />
            </Array>
          </mxGeometry>
        </mxCell>

        <!-- Link 4: Interconnect -> spimemio (sel_spimem) -->
        <mxCell id="edge4" value="&lt;b&gt;sel_spimem (Đọc Opcode XIP)&lt;/b&gt;" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#ea580c;strokeWidth=2.5;fontColor=#7c2d12;fontFamily=Segoe UI;fontSize=11;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="card_ic" target="card_spimem">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Link 5: Interconnect -> flash.c (sel_spicfg) -->
        <mxCell id="edge5" value="&lt;b&gt;sel_spicfg: Bit-bang Ghi Flash (0x0200_0000) từ Routine RAM&lt;/b&gt;" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#7c3aed;strokeWidth=3;fontColor=#581c87;fontFamily=Segoe UI;fontSize=11.5;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="card_ic" target="card_flashc">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Link 6: Interconnect -> UART MMIO -->
        <mxCell id="edge6" value="&lt;b&gt;sel_rfid (0x1000_0000) &amp;amp; sel_uart (0x3000_0000)&lt;/b&gt;" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#2563eb;strokeWidth=2.5;fontColor=#1e3a8a;fontFamily=Segoe UI;fontSize=11;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="card_ic" target="card_uart">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="1200" y="645" />
              <mxPoint x="1200" y="265" />
            </Array>
          </mxGeometry>
        </mxCell>

        <!-- Link 7: UART MMIO -> soc_regs.h -->
        <mxCell id="edge7" value="&lt;b&gt;Ánh Xạ MMIO: Offset 0x00 (Divider) &amp;amp; 0x04 (Data FIFO 32B)&lt;/b&gt;" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#2563eb;strokeWidth=3;fontColor=#1e3a8a;fontFamily=Segoe UI;fontSize=11.5;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="card_uart" target="card_regs">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Link 8: soc_regs.h -> access_control.c -->
        <mxCell id="edge8" value="&lt;b&gt;REG_RFID_UART_DAT (Đọc Thẻ) &amp;amp; REG_GPIO_LEDS (Mở Chốt Cửa)&lt;/b&gt;" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#059669;strokeWidth=3;fontColor=#065f46;fontFamily=Segoe UI;fontSize=11.5;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="card_regs" target="card_app">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Link 9: Assembly start.s -> C Main Application (Routing UNDER Card 6) -->
        <mxCell id="edge9" value="&lt;b&gt;Bàn Giao Quyền Điều Khiển: call main() -&amp;gt; access_control_poll()&lt;/b&gt;" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#e11d48;strokeWidth=3;fontColor=#9f1239;fontFamily=Segoe UI;fontSize=12;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="card_start" target="card_app">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="285" y="1170" />
              <mxPoint x="1495" y="1170" />
            </Array>
          </mxGeometry>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
    # Write to both drawio files
    with open(r"d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\firmware_soc_codesign.drawio", "w", encoding="utf-8") as f:
        f.write(xml_content.strip())
    with open(r"d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\soc_codesign_architecture.drawio", "w", encoding="utf-8") as f:
        f.write(xml_content.strip())
    print("[SUCCESS] Updated both Draw.io XML files!")

    # -------------------------------------------------------------
    # 2. HTML VECTOR & HIGH-DPI PNG RENDERING (Generous clearances!)
    # -------------------------------------------------------------
    html_content = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Firmware SoC Co-Design Architecture</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1780px;
    height: 1220px;
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
    width: 1700px;
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
    padding: 10px 12px;
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
    margin: 6px 0;
  }
  .code-box {
    font-family: "Consolas", monospace;
    font-size: 11px;
    line-height: 1.45;
    background: rgba(255,255,255,0.7);
    border-radius: 6px;
    padding: 6px 8px;
    border: 1px solid rgba(0,0,0,0.08);
    flex-grow: 1;
  }
  .card-footer {
    font-size: 10.5px;
    margin-top: 5px;
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
    width: 1780px;
    height: 1220px;
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

    <!-- Wire 1: Top -> Linker (Vertical in Col 1: y=425 to 480 at x=285) -->
    <path d="M 285 425 L 285 480" stroke="#d97706" stroke-width="3.5" fill="none" marker-end="url(#arr-amber)"/>

    <!-- Wire 2: Linker -> start.s (Vertical in Col 1: y=780 to 835 at x=285) -->
    <path d="M 285 780 L 285 835" stroke="#059669" stroke-width="3.5" fill="none" marker-end="url(#arr-green)"/>

    <!-- Wire 3: Linker -> Spimem (x=530 to 640, y=630 to 265) -->
    <path d="M 530 630 L 585 630 L 585 265 L 640 265" stroke="#d97706" stroke-width="2.5" fill="none" marker-end="url(#arr-amber)"/>

    <!-- Wire 4: Interconnect -> Spimem (Vertical in Col 2: y=480 up to 425 at x=895) -->
    <path d="M 895 480 L 895 425" stroke="#ea580c" stroke-width="3" fill="none" marker-end="url(#arr-orange)"/>

    <!-- Wire 5: Interconnect -> flash.c (Vertical in Col 2: y=810 down to 865 at x=895) -->
    <path d="M 895 810 L 895 865" stroke="#7c3aed" stroke-width="3.5" fill="none" marker-end="url(#arr-purple)"/>

    <!-- Wire 6: Interconnect -> UART (x=1150 to 1250, y=645 to 265) -->
    <path d="M 1150 645 L 1200 645 L 1200 265 L 1250 265" stroke="#2563eb" stroke-width="2.5" fill="none" marker-end="url(#arr-blue)"/>

    <!-- Wire 7: UART -> soc_regs (Vertical in Col 3: y=425 down to 480 at x=1495) -->
    <path d="M 1495 425 L 1495 480" stroke="#2563eb" stroke-width="3.5" fill="none" marker-end="url(#arr-blue)"/>

    <!-- Wire 8: soc_regs -> App (Vertical in Col 3: y=780 down to 835 at x=1495) -->
    <path d="M 1495 780 L 1495 835" stroke="#059669" stroke-width="3.5" fill="none" marker-end="url(#arr-green)"/>

    <!-- Wire 9: start.s -> App (CLEAN BOTTOM ROUTING UNDER CARD 6: y=1110 down to 1160, across to 1495, up to 1110) -->
    <path d="M 285 1110 L 285 1160 L 1495 1160 L 1495 1110" stroke="#e11d48" stroke-width="3.5" fill="none" marker-end="url(#arr-rose)"/>
  </svg>

  <!-- Badges in wide open clearances -->
  <div class="badge" style="left: 105px; top: 440px; color: #b45309; border: 1.5px solid #d97706;">
    Khớp Khởi Động: PROGADDR_RESET = FLASH ORIGIN = 0x0025_0000
  </div>

  <div class="badge" style="left: 110px; top: 795px; color: #059669; border: 1.5px solid #059669;">
    Khởi Tạo Ngăn Xếp: _stack_top (0x0400) -> lui sp, %hi(_stack_top)
  </div>

  <div class="badge" style="left: 545px; top: 390px; color: #b45309; border: 1.5px solid #d97706; text-align: center; line-height: 1.3;">
    Kéo Lệnh Flash XIP<br>0x0010_0000..0x00FF_FFFF
  </div>

  <div class="badge" style="left: 800px; top: 440px; color: #c2410c; border: 1.5px solid #ea580c;">
    sel_spimem (Đọc Opcode XIP)
  </div>

  <div class="badge" style="left: 710px; top: 825px; color: #581c87; border: 1.5px solid #7c3aed;">
    sel_spicfg: Bit-bang Ghi Flash (0x0200_0000) từ RAM Routine
  </div>

  <div class="badge" style="left: 1160px; top: 390px; color: #1e3a8a; border: 1.5px solid #2563eb; text-align: center; line-height: 1.3;">
    sel_rfid (4'h1)<br>& sel_uart (4'h3)
  </div>

  <div class="badge" style="left: 1290px; top: 440px; color: #1e3a8a; border: 1.5px solid #2563eb;">
    Ánh Xạ MMIO: Offset 0x00 (Divider) & 0x04 (Data FIFO 32B)
  </div>

  <div class="badge" style="left: 1300px; top: 795px; color: #065f46; border: 1.5px solid #059669;">
    REG_RFID_UART_DAT (Đọc Thẻ) & REG_GPIO_LEDS (Mở Chốt)
  </div>

  <!-- Bottom Badge: completely clear of Card 6! -->
  <div class="badge" style="left: 710px; top: 1145px; color: #9f1239; border: 1.5px solid #e11d48; font-size: 12px;">
    Bàn Giao Quyền Điều Khiển: call main() -> access_control_poll()
  </div>

  <!-- CARD 1: rdm6300_picorv32_soc.v -->
  <div class="card theme-blue" style="left: 40px; top: 110px; width: 490px; height: 315px;">
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
  <div class="card theme-green" style="left: 40px; top: 480px; width: 490px; height: 300px;">
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
  <div class="card theme-purple" style="left: 40px; top: 835px; width: 490px; height: 275px;">
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
  <div class="card theme-amber" style="left: 640px; top: 110px; width: 510px; height: 315px;">
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
  <div class="card theme-orange" style="left: 640px; top: 480px; width: 510px; height: 330px;">
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
  <div class="card theme-purple" style="left: 640px; top: 865px; width: 510px; height: 245px;">
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
  <div class="card theme-blue" style="left: 1250px; top: 110px; width: 490px; height: 315px;">
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
  <div class="card theme-green" style="left: 1250px; top: 480px; width: 490px; height: 300px;">
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
  <div class="card theme-green" style="left: 1250px; top: 835px; width: 490px; height: 275px;">
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

    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    out_img = r"d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\firmware_soc_codesign.png"

    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--force-device-scale-factor=2",
        f"--screenshot={out_img}",
        "--window-size=1780,1220",
        f"file:///{html_path.replace(os.sep, '/')}"
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(out_img):
        print(f"[SUCCESS] High-res image generated at: {out_img} ({os.path.getsize(out_img)} bytes)")

if __name__ == "__main__":
    generate_both()
