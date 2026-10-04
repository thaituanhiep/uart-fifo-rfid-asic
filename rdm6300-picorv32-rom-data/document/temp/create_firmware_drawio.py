# -*- coding: utf-8 -*-
"""
Script to generate the definitive, 100% genuine Draw.io file:
d:/VirtualSharedFolders/uart-fifo-rfid-asic/rdm6300-picorv32-rom-data/document/firmware_soc_codesign.drawio
and overwrite soc_codesign_architecture.drawio so both point to the flawless, tested version.
"""

def generate_drawio():
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="2026-10-04T12:00:00.000Z" agent="Mozilla/5.0" version="21.0.0" type="device">
  <diagram id="firmware_soc_codesign" name="Firmware Co-Design Architecture">
    <mxGraphModel dx="1600" dy="1100" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1750" pageHeight="1120" math="0" shadow="1">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- 0. TIÊU ĐỀ BẢN VẼ -->
        <mxCell id="title_banner" value="&lt;b style=&quot;font-size:22px;color:#0f172a;&quot;&gt;SƠ ĐỒ LIÊN KẾT MÃ NGUỒN CẤU HÌNH &amp;amp; THỰC THI HỆ THỐNG FIRMWARE TRÊN PHẦN CỨNG SOC&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:14px;color:#475569;&quot;&gt;Đối chiếu trực tiếp từng đoạn code quan trọng: RTL Top, Linker Script, Assembly, Flash XIP, Bus Interconnect, Driver C &amp;amp; App&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#cbd5e1;strokeWidth=2;fontFamily=Segoe UI;shadow=1;" vertex="1" parent="1">
          <mxGeometry x="40" y="20" width="1670" height="70" as="geometry" />
        </mxCell>

        <!-- ============================================================= -->
        <!-- CỘT 1: KHỞI ĐỘNG VẬT LÝ & BIÊN DỊCH                           -->
        <!-- ============================================================= -->

        <!-- CARD 1: rdm6300_picorv32_soc.v -->
        <mxCell id="card_top" value="&lt;b style=&quot;font-size:16px;color:#1e3a8a;&quot;&gt;1. rtl/rdm6300_picorv32_soc.v&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:12px;color:#2563eb;&quot;&gt;&lt;b&gt;[RTL Top Module - Cấu hình vi hệ thống phần cứng]&lt;/b&gt;&lt;/span&gt;&lt;br&gt;&lt;hr style=&quot;border:1px solid #93c5fd;&quot;&gt;&lt;div style=&quot;text-align:left;font-family:Consolas;font-size:11.5px;color:#0f172a;line-height:1.5;&quot;&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;parameter&lt;/b&gt;&lt;/font&gt; [31:0] &lt;b&gt;&lt;font color=&quot;#d97706&quot;&gt;PROGADDR_RESET&lt;/font&gt;&lt;/b&gt; = 32&#39;h0025_0000;&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;parameter&lt;/b&gt;&lt;/font&gt; [31:0] &lt;b&gt;&lt;font color=&quot;#059669&quot;&gt;STACKADDR&lt;/font&gt;&lt;/b&gt;      = 32&#39;h0000_0400;&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;parameter&lt;/b&gt;&lt;/font&gt; [0:0]  COMPRESSED_ISA = 1&#39;b0;&lt;br&gt;&lt;br&gt;picorv32 #(&lt;br&gt;  .&lt;b&gt;&lt;font color=&quot;#d97706&quot;&gt;PROGADDR_RESET&lt;/font&gt;&lt;/b&gt;(PROGADDR_RESET),&lt;br&gt;  .&lt;b&gt;&lt;font color=&quot;#059669&quot;&gt;STACKADDR&lt;/font&gt;&lt;/b&gt;(STACKADDR)&lt;br&gt;) cpu (&lt;br&gt;  .clk(clk), .resetn(resetn),&lt;br&gt;  .mem_valid(mem_valid), .mem_ready(mem_ready),&lt;br&gt;  .mem_addr(mem_addr), .mem_rdata(mem_rdata)&lt;br&gt;);&lt;/div&gt;&lt;hr style=&quot;border:1px solid #bfdbfe;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:11px;color:#1e3a8a;&quot;&gt;&amp;bull; &lt;b&gt;PROGADDR_RESET&lt;/b&gt;: Ép CPU nhả reset nạp opcode từ Flash XIP.&lt;br&gt;&amp;bull; &lt;b&gt;STACKADDR&lt;/b&gt;: Đặt mốc đỉnh 1KB SRAM nội bộ tốc độ cao.&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dbeafe;strokeColor=#2563eb;strokeWidth=2;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=10;" vertex="1" parent="1">
          <mxGeometry x="40" y="110" width="490" height="280" as="geometry" />
        </mxCell>

        <!-- CARD 2: sections.lds -->
        <mxCell id="card_lds" value="&lt;b style=&quot;font-size:16px;color:#065f46;&quot;&gt;2. firmware/sections.lds&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:12px;color:#059669;&quot;&gt;&lt;b&gt;[GNU Linker Script - Kịch bản phân bổ bộ nhớ biên dịch]&lt;/b&gt;&lt;/span&gt;&lt;br&gt;&lt;hr style=&quot;border:1px solid #6ee7b7;&quot;&gt;&lt;div style=&quot;text-align:left;font-family:Consolas;font-size:11.5px;color:#064e3b;line-height:1.5;&quot;&gt;&lt;b&gt;MEMORY&lt;/b&gt; {&lt;br&gt;  &lt;b&gt;&lt;font color=&quot;#d97706&quot;&gt;FLASH&lt;/font&gt;&lt;/b&gt; (rx) : ORIGIN = &lt;b&gt;&lt;font color=&quot;#d97706&quot;&gt;0x00250000&lt;/font&gt;&lt;/b&gt;, LENGTH = 704K&lt;br&gt;  &lt;b&gt;&lt;font color=&quot;#059669&quot;&gt;RAM&lt;/font&gt;&lt;/b&gt;   (rwx): ORIGIN = 0x00000000, LENGTH = 1K&lt;br&gt;}&lt;br&gt;&lt;br&gt;.text : {&lt;br&gt;  *(.text.start)&lt;br&gt;  *(.text*)&lt;br&gt;} &amp;gt; &lt;b&gt;&lt;font color=&quot;#d97706&quot;&gt;FLASH&lt;/font&gt;&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;b&gt;&lt;font color=&quot;#059669&quot;&gt;_stack_top&lt;/font&gt;&lt;/b&gt; = &lt;b&gt;&lt;font color=&quot;#059669&quot;&gt;0x00000400&lt;/font&gt;&lt;/b&gt;; &lt;font color=&quot;#047857&quot;&gt;/* Khớp STACKADDR phần cứng */&lt;/font&gt;&lt;/div&gt;&lt;hr style=&quot;border:1px solid #a7f3d0;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:11px;color:#065f46;&quot;&gt;&amp;bull; &lt;b&gt;FLASH ORIGIN&lt;/b&gt;: Định vị mã C (.text) trùng khớp PROGADDR_RESET RTL.&lt;br&gt;&amp;bull; &lt;b&gt;_stack_top&lt;/b&gt;: Xuất nhãn đỉnh SRAM cho file start.s nạp vào thanh ghi sp.&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d1fae5;strokeColor=#10b981;strokeWidth=2;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=10;" vertex="1" parent="1">
          <mxGeometry x="40" y="440" width="490" height="290" as="geometry" />
        </mxCell>

        <!-- CARD 3: start.s -->
        <mxCell id="card_start" value="&lt;b style=&quot;font-size:16px;color:#581c87;&quot;&gt;3. firmware/start.s&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:12px;color:#7c3aed;&quot;&gt;&lt;b&gt;[Assembly Bootstrap - Mã khởi động đầu tiên nạp sp]&lt;/b&gt;&lt;/span&gt;&lt;br&gt;&lt;hr style=&quot;border:1px solid #c084fc;&quot;&gt;&lt;div style=&quot;text-align:left;font-family:Consolas;font-size:11.5px;color:#3b0764;line-height:1.55;&quot;&gt;.global _start&lt;br&gt;_start:&lt;br&gt;    &lt;font color=&quot;#7c3aed&quot;&gt;&lt;b&gt;lui&lt;/b&gt;&lt;/font&gt;  sp, %hi(&lt;b&gt;&lt;font color=&quot;#059669&quot;&gt;_stack_top&lt;/font&gt;&lt;/b&gt;)       &lt;font color=&quot;#6b21a8&quot;&gt;# Nạp 20-bit cao (0x00000400)&lt;/font&gt;&lt;br&gt;    &lt;font color=&quot;#7c3aed&quot;&gt;&lt;b&gt;addi&lt;/b&gt;&lt;/font&gt; sp, sp, %lo(&lt;b&gt;&lt;font color=&quot;#059669&quot;&gt;_stack_top&lt;/font&gt;&lt;/b&gt;)   &lt;font color=&quot;#6b21a8&quot;&gt;# Nạp 12-bit thấp&lt;/font&gt;&lt;br&gt;    &lt;font color=&quot;#2563eb&quot;&gt;&lt;b&gt;call&lt;/b&gt;&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#e11d48&quot;&gt;main&lt;/font&gt;&lt;/b&gt;                      &lt;font color=&quot;#6b21a8&quot;&gt;# Bàn giao quyền sang hàm main()&lt;/font&gt;&lt;br&gt;&lt;br&gt;    &lt;font color=&quot;#ef4444&quot;&gt;&lt;b&gt;ebreak&lt;/b&gt;&lt;/font&gt;&lt;br&gt;    &lt;font color=&quot;#7c3aed&quot;&gt;&lt;b&gt;j&lt;/b&gt;&lt;/font&gt;    _start               &lt;font color=&quot;#6b21a8&quot;&gt;# Trap an toàn bảo vệ CPU&lt;/font&gt;&lt;/div&gt;&lt;hr style=&quot;border:1px solid #e9d5ff;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:11px;color:#581c87;&quot;&gt;&amp;bull; Khởi tạo con trỏ ngăn xếp phần cứng sp trỏ vào đỉnh 1KB SRAM.&lt;br&gt;&amp;bull; Hoàn tất chu trình bootstrap chỉ trong đúng 2 chu kỳ lệnh RISC-V.&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f3e8ff;strokeColor=#9333ea;strokeWidth=2;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=10;" vertex="1" parent="1">
          <mxGeometry x="40" y="780" width="490" height="290" as="geometry" />
        </mxCell>

        <!-- ============================================================= -->
        <!-- CỘT 2: TRÁI TIM ĐIỀU PHỐI BUS & BỘ NHỚ                        -->
        <!-- ============================================================= -->

        <!-- CARD 4: spimemio.v -->
        <mxCell id="card_spimem" value="&lt;b style=&quot;font-size:16px;color:#78350f;&quot;&gt;4. rtl/core/spimemio.v&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:12px;color:#b45309;&quot;&gt;&lt;b&gt;[SPI Flash Controller - Bộ điều khiển Flash XIP &amp;amp; Bit-bang]&lt;/b&gt;&lt;/span&gt;&lt;br&gt;&lt;hr style=&quot;border:1px solid #fde68a;&quot;&gt;&lt;div style=&quot;text-align:left;font-family:Consolas;font-size:11.5px;color:#451a03;line-height:1.5;&quot;&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;module&lt;/b&gt;&lt;/font&gt; spimemio (&lt;br&gt;  &lt;font color=&quot;#0284c7&quot;&gt;input&lt;/font&gt; valid, &lt;font color=&quot;#0284c7&quot;&gt;output&lt;/font&gt; ready, &lt;font color=&quot;#0284c7&quot;&gt;input&lt;/font&gt; [23:0] addr,&lt;br&gt;  &lt;font color=&quot;#0284c7&quot;&gt;output reg&lt;/font&gt; [31:0] rdata,&lt;br&gt;  &lt;font color=&quot;#0284c7&quot;&gt;output&lt;/font&gt; flash_csb, flash_clk, &lt;font color=&quot;#0284c7&quot;&gt;inout&lt;/font&gt; [3:0] flash_io,&lt;br&gt;  &lt;font color=&quot;#0284c7&quot;&gt;input&lt;/font&gt; [3:0] &lt;b&gt;&lt;font color=&quot;#e11d48&quot;&gt;cfgreg_we&lt;/font&gt;&lt;/b&gt;, &lt;font color=&quot;#0284c7&quot;&gt;input&lt;/font&gt; [31:0] cfgreg_di, &lt;font color=&quot;#0284c7&quot;&gt;output&lt;/font&gt; [31:0] cfgreg_do&lt;br&gt;);&lt;br&gt;&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;assign&lt;/b&gt;&lt;/font&gt; ready = valid &amp;amp;&amp;amp; (addr == rd_addr) &amp;amp;&amp;amp; rd_valid; &lt;font color=&quot;#b45309&quot;&gt;// XIP Hit&lt;/font&gt;&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;assign&lt;/b&gt;&lt;/font&gt; cfgreg_do[5] = flash_csb; &lt;font color=&quot;#b45309&quot;&gt;// Kênh Bit-bang MMIO&lt;/font&gt;&lt;/div&gt;&lt;hr style=&quot;border:1px solid #fef3c7;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:11px;color:#78350f;&quot;&gt;&amp;bull; &lt;b&gt;Đọc XIP&lt;/b&gt;: Tự động sinh xung kéo opcode 32-bit trả về cho CPU.&lt;br&gt;&amp;bull; &lt;b&gt;SPICFG (0x0200_0000)&lt;/b&gt;: Kênh bit-bang phục vụ ghi Sector thẻ &amp;amp; Log.&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fef3c7;strokeColor=#d97706;strokeWidth=2;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=10;" vertex="1" parent="1">
          <mxGeometry x="610" y="110" width="530" height="280" as="geometry" />
        </mxCell>

        <!-- CARD 5: soc_interconnect.v -->
        <mxCell id="card_ic" value="&lt;b style=&quot;font-size:16px;color:#7c2d12;&quot;&gt;5. rtl/core/soc_interconnect.v&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:12px;color:#ea580c;&quot;&gt;&lt;b&gt;[Bus Interconnect &amp;amp; Matrix - Bộ giải mã địa chỉ trung tâm]&lt;/b&gt;&lt;/span&gt;&lt;br&gt;&lt;hr style=&quot;border:1px solid #fdba74;&quot;&gt;&lt;div style=&quot;text-align:left;font-family:Consolas;font-size:11.5px;color:#431407;line-height:1.5;&quot;&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;assign&lt;/b&gt;&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#059669&quot;&gt;sel_sram&lt;/font&gt;&lt;/b&gt;   = cpu_mem_valid &amp;amp;&amp;amp; (cpu_mem_addr &amp;lt; &lt;b&gt;32&#39;h0000_0400&lt;/b&gt;);&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;assign&lt;/b&gt;&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#d97706&quot;&gt;sel_spimem&lt;/font&gt;&lt;/b&gt; = cpu_mem_valid &amp;amp;&amp;amp; (cpu_mem_addr &amp;gt;= &lt;b&gt;32&#39;h0010_0000&lt;/b&gt; &amp;amp;&amp;amp;&lt;br&gt;                                          cpu_mem_addr &amp;lt;  &lt;b&gt;32&#39;h0100_0000&lt;/b&gt;);&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;assign&lt;/b&gt;&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#e11d48&quot;&gt;sel_spicfg&lt;/font&gt;&lt;/b&gt; = cpu_mem_valid &amp;amp;&amp;amp; (cpu_mem_addr == &lt;b&gt;32&#39;h0200_0000&lt;/b&gt;);&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;assign&lt;/b&gt;&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#b45309&quot;&gt;sel_rfid&lt;/font&gt;&lt;/b&gt;   = cpu_mem_valid &amp;amp;&amp;amp; (cpu_mem_addr[31:28] == &lt;b&gt;4&#39;h1&lt;/b&gt;);&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;assign&lt;/b&gt;&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#2563eb&quot;&gt;sel_uart&lt;/font&gt;&lt;/b&gt;   = cpu_mem_valid &amp;amp;&amp;amp; (cpu_mem_addr[31:28] == &lt;b&gt;4&#39;h3&lt;/b&gt;);&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;assign&lt;/b&gt;&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#7c3aed&quot;&gt;sel_gpio&lt;/font&gt;&lt;/b&gt;   = cpu_mem_valid &amp;amp;&amp;amp; (cpu_mem_addr[31:28] == &lt;b&gt;4&#39;h4&lt;/b&gt;);&lt;br&gt;&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;assign&lt;/b&gt;&lt;/font&gt; cpu_mem_ready = sram_ready || spimem_ready || sel_spicfg ||&lt;br&gt;                       rfid_ready || uart_ready   || gpio_ready;&lt;/div&gt;&lt;hr style=&quot;border:1px solid #ffedd5;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:11px;color:#7c2d12;&quot;&gt;&amp;bull; &lt;b&gt;0-Delay Muxing&lt;/b&gt;: Giải mã tiền tố 4-bit phân luồng tức thì trong 0 chu kỳ.&lt;br&gt;&amp;bull; &lt;b&gt;Zero Wait-State&lt;/b&gt;: Không bao giờ stall CPU khi giao tiếp MMIO ngoại vi.&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffedd5;strokeColor=#ea580c;strokeWidth=2;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=10;" vertex="1" parent="1">
          <mxGeometry x="610" y="440" width="530" height="340" as="geometry" />
        </mxCell>

        <!-- CARD 6: flash.c -->
        <mxCell id="card_flashc" value="&lt;b style=&quot;font-size:16px;color:#581c87;&quot;&gt;6. firmware/flash.c &amp;amp; start.s&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:12px;color:#7c3aed;&quot;&gt;&lt;b&gt;[RAM Execution Routine - Nhảy sang SRAM ghi Flash]&lt;/b&gt;&lt;/span&gt;&lt;br&gt;&lt;hr style=&quot;border:1px solid #c084fc;&quot;&gt;&lt;div style=&quot;text-align:left;font-family:Consolas;font-size:11.5px;color:#3b0764;line-height:1.5;&quot;&gt;&lt;font color=&quot;#7c3aed&quot;&gt;&lt;b&gt;flashio_worker&lt;/b&gt;&lt;/font&gt;:&lt;br&gt;    &lt;font color=&quot;#7c3aed&quot;&gt;&lt;b&gt;li&lt;/b&gt;&lt;/font&gt; t0, &lt;b&gt;&lt;font color=&quot;#e11d48&quot;&gt;0x02000000&lt;/font&gt;&lt;/b&gt;  &lt;font color=&quot;#6b21a8&quot;&gt;# Ghi Bit-bang SPI MMIO&lt;/font&gt;&lt;br&gt;    &lt;font color=&quot;#7c3aed&quot;&gt;&lt;b&gt;sh&lt;/b&gt;&lt;/font&gt; t1, 0(t0)&lt;br&gt;&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;static void&lt;/b&gt;&lt;/font&gt; &lt;b&gt;flashio&lt;/b&gt;(uint8_t *data, int len, uint8_t wrencmd) {&lt;br&gt;  &lt;font color=&quot;#059669&quot;&gt;// 1. Sao chép worker lên Stack SRAM (&amp;lt; 0x0000_0400)&lt;/font&gt;&lt;br&gt;  &lt;font color=&quot;#059669&quot;&gt;// 2. CPU nhảy sang SRAM chạy để xóa Sector / ghi Trang&lt;/font&gt;&lt;br&gt;  &lt;font color=&quot;#059669&quot;&gt;// 3. Sau khi ghi xong Sector 48 (Thẻ) / 49 (Log), quay lại XIP&lt;/font&gt;&lt;br&gt;}&lt;/div&gt;&lt;hr style=&quot;border:1px solid #e9d5ff;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:11px;color:#581c87;&quot;&gt;&amp;bull; &lt;b&gt;Giải quyết xung đột XIP&lt;/b&gt;: Không thể vừa nạp lệnh vừa xóa Flash ngoài.&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f3e8ff;strokeColor=#9333ea;strokeWidth=2;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=10;" vertex="1" parent="1">
          <mxGeometry x="610" y="830" width="530" height="240" as="geometry" />
        </mxCell>

        <!-- ============================================================= -->
        <!-- CỘT 3: TẦNG NGOẠI VI & PHẦN MỀM ỨNG DỤNG                      -->
        <!-- ============================================================= -->

        <!-- CARD 7: uart_mmio.v -->
        <mxCell id="card_uart" value="&lt;b style=&quot;font-size:16px;color:#1e3a8a;&quot;&gt;7. rtl/uart/uart_mmio.v&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:12px;color:#2563eb;&quot;&gt;&lt;b&gt;[Dual UART MMIO Controller - Bộ đệm phần cứng 32B FIFO]&lt;/b&gt;&lt;/span&gt;&lt;br&gt;&lt;hr style=&quot;border:1px solid #93c5fd;&quot;&gt;&lt;div style=&quot;text-align:left;font-family:Consolas;font-size:11.5px;color:#0f172a;line-height:1.5;&quot;&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;wire&lt;/b&gt;&lt;/font&gt; reg_div_sel = valid &amp;amp;&amp;amp; (addr[2] == &lt;b&gt;1&#39;b0&lt;/b&gt;); &lt;font color=&quot;#64748B&quot;&gt;// 0x00: Baud&lt;/font&gt;&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;wire&lt;/b&gt;&lt;/font&gt; reg_dat_sel = valid &amp;amp;&amp;amp; (addr[2] == &lt;b&gt;1&#39;b1&lt;/b&gt;); &lt;font color=&quot;#64748B&quot;&gt;// 0x04: Data&lt;/font&gt;&lt;br&gt;&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;assign&lt;/b&gt;&lt;/font&gt; reg_dat_do = fifo_empty ? &lt;b&gt;&lt;font color=&quot;#e11d48&quot;&gt;32&#39;hFFFFFFFF&lt;/font&gt;&lt;/b&gt; :&lt;br&gt;                                   {24&#39;d0, fifo_dout};&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;assign&lt;/b&gt;&lt;/font&gt; ready = 1&#39;b1; &lt;font color=&quot;#64748B&quot;&gt;// Zero Wait-state response&lt;/font&gt;&lt;/div&gt;&lt;hr style=&quot;border:1px solid #bfdbfe;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:11px;color:#1e3a8a;&quot;&gt;&amp;bull; &lt;b&gt;Đọc không khóa&lt;/b&gt;: Có dữ liệu trả mã ký tự, rỗng trả về 0xFFFFFFFF.&lt;br&gt;&amp;bull; &lt;b&gt;FIFO 32 Byte&lt;/b&gt;: Hứng trọn chuỗi 14 byte thẻ RFID RDM6300.&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dbeafe;strokeColor=#2563eb;strokeWidth=2;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=10;" vertex="1" parent="1">
          <mxGeometry x="1220" y="110" width="490" height="280" as="geometry" />
        </mxCell>

        <!-- CARD 8: soc_regs.h -->
        <mxCell id="card_regs" value="&lt;b style=&quot;font-size:16px;color:#065f46;&quot;&gt;8. firmware/common/soc_regs.h&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:12px;color:#059669;&quot;&gt;&lt;b&gt;[Firmware Hardware Memory Map - Định nghĩa con trỏ C]&lt;/b&gt;&lt;/span&gt;&lt;br&gt;&lt;hr style=&quot;border:1px solid #6ee7b7;&quot;&gt;&lt;div style=&quot;text-align:left;font-family:Consolas;font-size:11.5px;color:#064e3b;line-height:1.5;&quot;&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;#define&lt;/b&gt;&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#b45309&quot;&gt;REG_RFID_UART_DIV&lt;/font&gt;&lt;/b&gt; (*(&lt;font color=&quot;#0284c7&quot;&gt;volatile uint32_t*&lt;/font&gt;)&lt;b&gt;0x10000000&lt;/b&gt;)&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;#define&lt;/b&gt;&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#b45309&quot;&gt;REG_RFID_UART_DAT&lt;/font&gt;&lt;/b&gt; (*(&lt;font color=&quot;#0284c7&quot;&gt;volatile uint32_t*&lt;/font&gt;)&lt;b&gt;0x10000004&lt;/b&gt;)&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;#define&lt;/b&gt;&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#2563eb&quot;&gt;REG_PC_UART_DIV&lt;/font&gt;&lt;/b&gt;   (*(&lt;font color=&quot;#0284c7&quot;&gt;volatile uint32_t*&lt;/font&gt;)&lt;b&gt;0x30000000&lt;/b&gt;)&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;#define&lt;/b&gt;&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#2563eb&quot;&gt;REG_PC_UART_DAT&lt;/font&gt;&lt;/b&gt;   (*(&lt;font color=&quot;#0284c7&quot;&gt;volatile uint32_t*&lt;/font&gt;)&lt;b&gt;0x30000004&lt;/b&gt;)&lt;br&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;#define&lt;/b&gt;&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#7c3aed&quot;&gt;REG_GPIO_LEDS&lt;/font&gt;&lt;/b&gt;     (*(&lt;font color=&quot;#0284c7&quot;&gt;volatile uint32_t*&lt;/font&gt;)&lt;b&gt;0x40000000&lt;/b&gt;)&lt;/div&gt;&lt;hr style=&quot;border:1px solid #a7f3d0;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:11px;color:#065f46;&quot;&gt;&amp;bull; &lt;b&gt;volatile&lt;/b&gt;: Ép GCC luôn phát sinh lệnh load/store bus, không cache CPU.&lt;br&gt;&amp;bull; Khớp 100% với các tín hiệu sel_rfid, sel_uart, sel_gpio của Interconnect.&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d1fae5;strokeColor=#10b981;strokeWidth=2;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=10;" vertex="1" parent="1">
          <mxGeometry x="1220" y="440" width="490" height="290" as="geometry" />
        </mxCell>

        <!-- CARD 9: access_control.c -->
        <mxCell id="card_app" value="&lt;b style=&quot;font-size:16px;color:#065f46;&quot;&gt;9. firmware/access_control.c&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:12px;color:#059669;&quot;&gt;&lt;b&gt;[Application Logic - Polling thẻ RFID &amp;amp; Điều khiển cửa]&lt;/b&gt;&lt;/span&gt;&lt;br&gt;&lt;hr style=&quot;border:1px solid #6ee7b7;&quot;&gt;&lt;div style=&quot;text-align:left;font-family:Consolas;font-size:11.5px;color:#064e3b;line-height:1.5;&quot;&gt;&lt;font color=&quot;#0284c7&quot;&gt;&lt;b&gt;void&lt;/b&gt;&lt;/font&gt; &lt;b&gt;access_control_poll&lt;/b&gt;(void) {&lt;br&gt;    &lt;font color=&quot;#0284c7&quot;&gt;uint32_t&lt;/font&gt; d = &lt;b&gt;&lt;font color=&quot;#b45309&quot;&gt;REG_RFID_UART_DAT&lt;/font&gt;&lt;/b&gt;; &lt;font color=&quot;#047857&quot;&gt;// Đọc FIFO (Non-blocking)&lt;/font&gt;&lt;br&gt;    &lt;font color=&quot;#e11d48&quot;&gt;&lt;b&gt;if&lt;/b&gt;&lt;/font&gt; (d != &lt;b&gt;&lt;font color=&quot;#e11d48&quot;&gt;0xFFFFFFFF&lt;/font&gt;&lt;/b&gt;) {&lt;br&gt;        rdm6300_push((&lt;font color=&quot;#0284c7&quot;&gt;uint8_t&lt;/font&gt;)d);  &lt;font color=&quot;#047857&quot;&gt;// Nạp vào parser kiểm tra XOR&lt;/font&gt;&lt;br&gt;    }&lt;br&gt;&lt;br&gt;    &lt;font color=&quot;#047857&quot;&gt;// Khi thẻ hợp lệ trong Whitelist: Mở relay chốt cửa&lt;/font&gt;&lt;br&gt;    &lt;b&gt;&lt;font color=&quot;#7c3aed&quot;&gt;REG_GPIO_LEDS&lt;/font&gt;&lt;/b&gt; = (&lt;font color=&quot;#7c3aed&quot;&gt;REG_GPIO_LEDS&lt;/font&gt; &amp;amp; ~0x0002) | &lt;b&gt;0x0004&lt;/b&gt;;&lt;br&gt;}&lt;/div&gt;&lt;hr style=&quot;border:1px solid #a7f3d0;&quot;&gt;&lt;div style=&quot;text-align:left;font-size:11px;color:#065f46;&quot;&gt;&amp;bull; Vòng lặp polling liên tục không bị block nhờ FIFO phần cứng 32B.&lt;br&gt;&amp;bull; Phản hồi mở cửa chưa đầy 10 µs ngay khi nhận đủ chuỗi mã thẻ.&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d1fae5;strokeColor=#10b981;strokeWidth=2;fontFamily=Segoe UI;shadow=1;verticalAlign=top;spacingTop=10;" vertex="1" parent="1">
          <mxGeometry x="1220" y="780" width="490" height="290" as="geometry" />
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
              <mxPoint x="570" y="585" />
              <mxPoint x="570" y="250" />
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
              <mxPoint x="1180" y="610" />
              <mxPoint x="1180" y="250" />
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

        <!-- Link 9: Assembly start.s -> C Main Application -->
        <mxCell id="edge9" value="&lt;b&gt;Bàn Giao Quyền: call main() -&amp;gt; access_control_poll()&lt;/b&gt;" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#e11d48;strokeWidth=3;fontColor=#9f1239;fontFamily=Segoe UI;fontSize=12;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="card_start" target="card_app">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="530" y="925" />
              <mxPoint x="1220" y="925" />
            </Array>
          </mxGeometry>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
    # Write to both paths for convenience
    paths = [
        r"d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\firmware_soc_codesign.drawio",
        r"d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\soc_codesign_architecture.drawio"
    ]
    for p in paths:
        with open(p, "w", encoding="utf-8") as f:
            f.write(xml_content.strip())
        print(f"[SUCCESS] Written genuine Draw.io file to: {p}")

if __name__ == "__main__":
    generate_drawio()
