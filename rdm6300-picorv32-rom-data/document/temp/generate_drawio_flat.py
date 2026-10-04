import xml.etree.ElementTree as ET

def generate_drawio():
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="2026-10-04T08:00:00.000Z" agent="Mozilla/5.0" version="21.0.0" type="device">
  <diagram id="soc_codesign_arch" name="SoC Co-Design Architecture">
    <mxGraphModel dx="1600" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="2500" pageHeight="1600" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- TIÊU ĐỀ BẢN VẼ -->
        <mxCell id="main_title" value="&lt;b style=&quot;font-size:24px;&quot;&gt;SƠ ĐỒ LIÊN KẾT ĐỒNG THIẾT KẾ PHẦN CỨNG &amp;amp; PHẦN MỀM (HARDWARE / SOFTWARE CO-DESIGN)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size:15px; color:#475569;&quot;&gt;Hệ Thống Vi Mạch SoC PicoRV32 RFID RDM6300 &amp;amp; SPI Flash XIP | Đối Chiếu RTL Verilog, Linker Script, Assembly &amp;amp; Firmware C&lt;/span&gt;" style="text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontFamily=Segoe UI;" vertex="1" parent="1">
          <mxGeometry x="550" y="25" width="1400" height="60" as="geometry" />
        </mxCell>

        <!-- ============================================================= -->
        <!-- PHÂN HỆ 1: BOOT & MEMORY                                      -->
        <!-- ============================================================= -->
        <mxCell id="bg_grp1" value="&lt;b style=&quot;font-size:14px; color:#0369A1;&quot;&gt;PHÂN HỆ 1: KHỞI ĐỘNG HỆ THỐNG &amp;amp; ĐỒNG BỘ BỘ NHỚ (BOOT VECTOR &amp;amp; STACK)&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F0F9FF;strokeColor=#0284C7;strokeWidth=2;verticalAlign=top;align=left;spacingLeft=20;spacingTop=12;fontFamily=Segoe UI;" vertex="1" parent="1">
          <mxGeometry x="40" y="100" width="1160" height="720" as="geometry" />
        </mxCell>

        <!-- CARD 1: rdm6300_picorv32_soc.v -->
        <mxCell id="card_top" value="&lt;b&gt;rtl/rdm6300_picorv32_soc.v&lt;/b&gt; [RTL Top Module]&lt;hr&gt;&lt;font face=&quot;Consolas&quot; size=&quot;2&quot;&gt;&lt;b&gt;// 1. Cấu hình Vector Khởi Động &amp;amp; Ngăn Xếp Top SoC&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#0284C7&quot;&gt;parameter&lt;/font&gt; [31:0] &lt;b&gt;&lt;font color=&quot;#D97706&quot;&gt;PROGADDR_RESET&lt;/font&gt;&lt;/b&gt; = 32&#39;h0025_0000; &lt;font color=&quot;#64748B&quot;&gt;// Flash XIP&lt;/font&gt;&lt;br&gt;&lt;font color=&quot;#0284C7&quot;&gt;parameter&lt;/font&gt; [31:0] &lt;b&gt;&lt;font color=&quot;#059669&quot;&gt;STACKADDR&lt;/font&gt;&lt;/b&gt;      = 32&#39;h0000_0400; &lt;font color=&quot;#64748B&quot;&gt;// Đỉnh 1KB RAM&lt;/font&gt;&lt;br&gt;&lt;font color=&quot;#0284C7&quot;&gt;parameter&lt;/font&gt; [0:0]  COMPRESSED_ISA = 1&#39;b0;          &lt;font color=&quot;#64748B&quot;&gt;// RV32I Base&lt;/font&gt;&lt;br&gt;&lt;br&gt;&lt;font color=&quot;#0284C7&quot;&gt;wire&lt;/font&gt; mem_valid, mem_ready;&lt;br&gt;&lt;font color=&quot;#0284C7&quot;&gt;wire&lt;/font&gt; [31:0] mem_addr, mem_wdata, mem_rdata;&lt;br&gt;&lt;br&gt;picorv32 #(&lt;br&gt;  .&lt;font color=&quot;#D97706&quot;&gt;PROGADDR_RESET&lt;/font&gt;(PROGADDR_RESET),&lt;br&gt;  .&lt;font color=&quot;#059669&quot;&gt;STACKADDR&lt;/font&gt;(STACKADDR)&lt;br&gt;) cpu (&lt;br&gt;  .clk(clk), .resetn(resetn),&lt;br&gt;  .mem_valid(mem_valid), .mem_ready(mem_ready),&lt;br&gt;  .mem_addr(mem_addr), .mem_rdata(mem_rdata)&lt;br&gt;);&lt;/font&gt;&lt;hr&gt;&lt;font size=&quot;1&quot; color=&quot;#334155&quot;&gt;&amp;bull; &lt;b&gt;PROGADDR_RESET&lt;/b&gt;: Ép CPU nhả reset là kéo lệnh thẳng từ Flash XIP.&lt;br&gt;&amp;bull; &lt;b&gt;STACKADDR&lt;/b&gt;: Đặt đỉnh ngăn xếp tại 1KB SRAM nội bộ, độ trễ 1 chu kỳ.&lt;/font&gt;" style="swimlane;whiteSpace=wrap;html=1;collapsible=1;startSize=28;fillColor=#FFFFFF;strokeColor=#1E293B;strokeWidth=2;align=left;verticalAlign=top;spacingLeft=12;spacingTop=8;fontFamily=Segoe UI;fontColor=#0F172A;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="70" y="150" width="530" height="300" as="geometry" />
        </mxCell>

        <!-- CARD 2: sections.lds -->
        <mxCell id="card_lds" value="&lt;b&gt;firmware/sections.lds&lt;/b&gt; [GNU Linker Script]&lt;hr&gt;&lt;font face=&quot;Consolas&quot; size=&quot;2&quot;&gt;&lt;b&gt;/* 2. Bản Đồ Bộ Nhớ GNU GCC Toolchain */&lt;/b&gt;&lt;br&gt;MEMORY {&lt;br&gt;  &lt;b&gt;&lt;font color=&quot;#D97706&quot;&gt;FLASH&lt;/font&gt;&lt;/b&gt; (rx) : ORIGIN = &lt;b&gt;&lt;font color=&quot;#D97706&quot;&gt;0x00250000&lt;/font&gt;&lt;/b&gt;, LENGTH = 0x000B0000 &lt;font color=&quot;#64748B&quot;&gt;/* 704KB */&lt;/font&gt;&lt;br&gt;  &lt;b&gt;&lt;font color=&quot;#059669&quot;&gt;RAM&lt;/font&gt;&lt;/b&gt;   (rwx): ORIGIN = 0x00000000, LENGTH = 0x00000400 &lt;font color=&quot;#64748B&quot;&gt;/* 1KB */&lt;/font&gt;&lt;br&gt;}&lt;br&gt;&lt;br&gt;.text : {&lt;br&gt;  *(.text.start)&lt;br&gt;  *(.text*)&lt;br&gt;} &amp;gt; &lt;font color=&quot;#D97706&quot;&gt;FLASH&lt;/font&gt;&lt;br&gt;&lt;br&gt;&lt;b&gt;&lt;font color=&quot;#059669&quot;&gt;_stack_top&lt;/font&gt;&lt;/b&gt; = &lt;b&gt;&lt;font color=&quot;#059669&quot;&gt;0x00000400&lt;/font&gt;&lt;/b&gt;; &lt;font color=&quot;#64748B&quot;&gt;/* Khớp STACKADDR phần cứng */&lt;/font&gt;&lt;/font&gt;&lt;hr&gt;&lt;font size=&quot;1&quot; color=&quot;#334155&quot;&gt;&amp;bull; &lt;b&gt;ORIGIN FLASH&lt;/b&gt;: Định vị mã C (.text) trùng khớp PROGADDR_RESET RTL.&lt;br&gt;&amp;bull; &lt;b&gt;_stack_top&lt;/b&gt;: Xuất nhãn đỉnh ngăn xếp cho assembly start.s nạp vào thanh ghi sp.&lt;/font&gt;" style="swimlane;whiteSpace=wrap;html=1;collapsible=1;startSize=28;fillColor=#FFFFFF;strokeColor=#15803D;strokeWidth=2;align=left;verticalAlign=top;spacingLeft=12;spacingTop=8;fontFamily=Segoe UI;fontColor=#0F172A;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="640" y="150" width="530" height="300" as="geometry" />
        </mxCell>

        <!-- CARD 3: picorv32.v -->
        <mxCell id="card_cpu" value="&lt;b&gt;rtl/core/picorv32.v&lt;/b&gt; [RISC-V CPU Core Master]&lt;hr&gt;&lt;font face=&quot;Consolas&quot; size=&quot;2&quot;&gt;&lt;b&gt;// 3. Khởi Tạo Thanh Ghi Nội Bộ CPU PicoRV32&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#0284C7&quot;&gt;module&lt;/font&gt; picorv32 #(&lt;br&gt;  &lt;font color=&quot;#0284C7&quot;&gt;parameter&lt;/font&gt; [31:0] &lt;font color=&quot;#D97706&quot;&gt;PROGADDR_RESET&lt;/font&gt; = 32&#39;h0010_0000,&lt;br&gt;  &lt;font color=&quot;#0284C7&quot;&gt;parameter&lt;/font&gt; [31:0] &lt;font color=&quot;#059669&quot;&gt;STACKADDR&lt;/font&gt;      = 32&#39;hffff_ffff&lt;br&gt;) (&lt;br&gt;  &lt;font color=&quot;#0284C7&quot;&gt;input&lt;/font&gt; clk, resetn, &lt;font color=&quot;#0284C7&quot;&gt;output reg&lt;/font&gt; mem_valid, &lt;font color=&quot;#0284C7&quot;&gt;input&lt;/font&gt; mem_ready,&lt;br&gt;  &lt;font color=&quot;#0284C7&quot;&gt;output reg&lt;/font&gt; [31:0] mem_addr, mem_wdata, &lt;font color=&quot;#0284C7&quot;&gt;input&lt;/font&gt; [31:0] mem_rdata,&lt;br&gt;  &lt;font color=&quot;#0284C7&quot;&gt;output reg&lt;/font&gt; cpu_trap&lt;br&gt;);&lt;br&gt;&lt;br&gt;cpuregs[2] &amp;lt;= &lt;font color=&quot;#059669&quot;&gt;STACKADDR&lt;/font&gt;;      &lt;font color=&quot;#64748B&quot;&gt;// Nạp con trỏ sp phần cứng&lt;/font&gt;&lt;br&gt;reg_pc     &amp;lt;= &lt;font color=&quot;#D97706&quot;&gt;PROGADDR_RESET&lt;/font&gt;; &lt;font color=&quot;#64748B&quot;&gt;// PC trỏ thẳng 0x0025_0000&lt;/font&gt;&lt;/font&gt;&lt;hr&gt;&lt;font size=&quot;1&quot; color=&quot;#334155&quot;&gt;&amp;bull; &lt;b&gt;Bắt tay Native Mem Bus&lt;/b&gt;: mem_valid + mem_ready trong 1 clock.&lt;br&gt;&amp;bull; &lt;b&gt;cpu_trap&lt;/b&gt;: Tích cực mức cao bảo vệ vi hệ thống khi có lệnh bất hợp pháp.&lt;/font&gt;" style="swimlane;whiteSpace=wrap;html=1;collapsible=1;startSize=28;fillColor=#FFFFFF;strokeColor=#1E293B;strokeWidth=2;align=left;verticalAlign=top;spacingLeft=12;spacingTop=8;fontFamily=Segoe UI;fontColor=#0F172A;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="70" y="490" width="530" height="300" as="geometry" />
        </mxCell>

        <!-- CARD 4: start.s -->
        <mxCell id="card_start" value="&lt;b&gt;firmware/start.s&lt;/b&gt; [Assembly Bootstrap]&lt;hr&gt;&lt;font face=&quot;Consolas&quot; size=&quot;2&quot;&gt;&lt;b&gt;# 4. Bootstrap Khởi Tạo Ngăn Xếp &amp;amp; Nhảy Sang C&lt;/b&gt;&lt;br&gt;.global _start&lt;br&gt;_start:&lt;br&gt;    &lt;font color=&quot;#7C3AED&quot;&gt;lui&lt;/font&gt;  sp, %hi(&lt;b&gt;&lt;font color=&quot;#059669&quot;&gt;_stack_top&lt;/font&gt;&lt;/b&gt;)       &lt;font color=&quot;#64748B&quot;&gt;# Nạp 20-bit cao (0x00000400)&lt;/font&gt;&lt;br&gt;    &lt;font color=&quot;#7C3AED&quot;&gt;addi&lt;/font&gt; sp, sp, %lo(&lt;b&gt;&lt;font color=&quot;#059669&quot;&gt;_stack_top&lt;/font&gt;&lt;/b&gt;)   &lt;font color=&quot;#64748B&quot;&gt;# Nạp 12-bit thấp&lt;/font&gt;&lt;br&gt;    &lt;font color=&quot;#0284C7&quot;&gt;call&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#E11D48&quot;&gt;main&lt;/font&gt;&lt;/b&gt;                      &lt;font color=&quot;#64748B&quot;&gt;# Chuyển quyền điều khiển sang C&lt;/font&gt;&lt;br&gt;&lt;br&gt;    &lt;font color=&quot;#EF4444&quot;&gt;ebreak&lt;/font&gt;&lt;br&gt;    &lt;font color=&quot;#7C3AED&quot;&gt;j&lt;/font&gt;    _start               &lt;font color=&quot;#64748B&quot;&gt;# Trap an toàn nếu main() return&lt;/font&gt;&lt;/font&gt;&lt;hr&gt;&lt;font size=&quot;1&quot; color=&quot;#334155&quot;&gt;&amp;bull; &lt;b&gt;sp&lt;/b&gt;: Trỏ vào mốc 0x0400 để các hàm C cấp phát Stack Frame.&lt;br&gt;&amp;bull; &lt;b&gt;call main&lt;/b&gt;: Bàn giao quyền điều hành sang hàm main() ứng dụng.&lt;/font&gt;" style="swimlane;whiteSpace=wrap;html=1;collapsible=1;startSize=28;fillColor=#FFFFFF;strokeColor=#6B21A8;strokeWidth=2;align=left;verticalAlign=top;spacingLeft=12;spacingTop=8;fontFamily=Segoe UI;fontColor=#0F172A;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="640" y="490" width="530" height="300" as="geometry" />
        </mxCell>

        <!-- ============================================================= -->
        <!-- PHÂN HỆ 2: SPI FLASH XIP & RAM ROUTINE                         -->
        <!-- ============================================================= -->
        <mxCell id="bg_grp2" value="&lt;b style=&quot;font-size:14px; color:#B45309;&quot;&gt;PHÂN HỆ 2: BỘ ĐIỀU KHIỂN SPI FLASH XIP &amp;amp; CƠ CHẾ CHẠY MÃ TRÊN RAM&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFBEB;strokeColor=#D97706;strokeWidth=2;verticalAlign=top;align=left;spacingLeft=20;spacingTop=12;fontFamily=Segoe UI;" vertex="1" parent="1">
          <mxGeometry x="1240" y="100" width="1160" height="720" as="geometry" />
        </mxCell>

        <!-- CARD 5: spimemio.v -->
        <mxCell id="card_spimem" value="&lt;b&gt;rtl/core/spimemio.v&lt;/b&gt; [SPI Flash Controller]&lt;hr&gt;&lt;font face=&quot;Consolas&quot; size=&quot;2&quot;&gt;&lt;b&gt;// 5. Bộ Điều Khiển Flash SPI (XIP + Bit-bang)&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#0284C7&quot;&gt;module&lt;/font&gt; spimemio (&lt;br&gt;  &lt;font color=&quot;#0284C7&quot;&gt;input&lt;/font&gt; valid, &lt;font color=&quot;#0284C7&quot;&gt;output&lt;/font&gt; ready, &lt;font color=&quot;#0284C7&quot;&gt;input&lt;/font&gt; [23:0] addr,&lt;br&gt;  &lt;font color=&quot;#0284C7&quot;&gt;output reg&lt;/font&gt; [31:0] rdata,&lt;br&gt;  &lt;font color=&quot;#0284C7&quot;&gt;output&lt;/font&gt; flash_csb, flash_clk, &lt;font color=&quot;#0284C7&quot;&gt;inout&lt;/font&gt; [3:0] flash_io,&lt;br&gt;  &lt;font color=&quot;#0284C7&quot;&gt;input&lt;/font&gt; [3:0] &lt;b&gt;&lt;font color=&quot;#E11D48&quot;&gt;cfgreg_we&lt;/font&gt;&lt;/b&gt;, &lt;font color=&quot;#0284C7&quot;&gt;input&lt;/font&gt; [31:0] cfgreg_di, &lt;font color=&quot;#0284C7&quot;&gt;output&lt;/font&gt; [31:0] cfgreg_do&lt;br&gt;);&lt;br&gt;&lt;br&gt;&lt;font color=&quot;#0284C7&quot;&gt;assign&lt;/font&gt; ready = valid &amp;amp;&amp;amp; (addr == rd_addr) &amp;amp;&amp;amp; rd_valid; &lt;font color=&quot;#64748B&quot;&gt;// XIP Hit&lt;/font&gt;&lt;br&gt;&lt;font color=&quot;#0284C7&quot;&gt;assign&lt;/font&gt; cfgreg_do[5] = flash_csb; &lt;font color=&quot;#64748B&quot;&gt;// Kênh Bit-bang MMIO&lt;/font&gt;&lt;/font&gt;&lt;hr&gt;&lt;font size=&quot;1&quot; color=&quot;#334155&quot;&gt;&amp;bull; &lt;b&gt;Đọc XIP&lt;/b&gt; (0x0010_0000): Tự phát xung đọc kéo opcode trong suốt.&lt;br&gt;&amp;bull; &lt;b&gt;Ghi/Xóa&lt;/b&gt; (0x0200_0000): Cho phép C bit-bang chân SPI ngoài.&lt;/font&gt;" style="swimlane;whiteSpace=wrap;html=1;collapsible=1;startSize=28;fillColor=#FFFFFF;strokeColor=#B45309;strokeWidth=2;align=left;verticalAlign=top;spacingLeft=12;spacingTop=8;fontFamily=Segoe UI;fontColor=#0F172A;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="1270" y="150" width="530" height="300" as="geometry" />
        </mxCell>

        <!-- CARD 6: flash.c -->
        <mxCell id="card_flashc" value="&lt;b&gt;firmware/flash.c &amp;amp; start.s&lt;/b&gt; [RAM Execution Routine]&lt;hr&gt;&lt;font face=&quot;Consolas&quot; size=&quot;2&quot;&gt;&lt;b&gt;// 6. Routine Nhảy Sang SRAM Ghi Flash Tránh Stall Bus&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#7C3AED&quot;&gt;flashio_worker&lt;/font&gt;:&lt;br&gt;    &lt;font color=&quot;#7C3AED&quot;&gt;li&lt;/font&gt; t0, &lt;b&gt;&lt;font color=&quot;#D97706&quot;&gt;0x02000000&lt;/font&gt;&lt;/b&gt; &lt;font color=&quot;#64748B&quot;&gt;# MMIO Bit-bang SPI Cfg&lt;/font&gt;&lt;br&gt;    &lt;font color=&quot;#7C3AED&quot;&gt;sh&lt;/font&gt; t1, 0(t0)&lt;br&gt;&lt;br&gt;&lt;font color=&quot;#0284C7&quot;&gt;static void&lt;/font&gt; &lt;b&gt;flashio&lt;/b&gt;(uint8_t *data, int len, uint8_t wrencmd) {&lt;br&gt;  &lt;font color=&quot;#059669&quot;&gt;// 1. Sao chép worker lên Stack SRAM (&amp;lt; 0x0000_0400)&lt;/font&gt;&lt;br&gt;  &lt;font color=&quot;#059669&quot;&gt;// 2. CPU nhảy sang SRAM chạy để xóa Sector / ghi Trang&lt;/font&gt;&lt;br&gt;  &lt;font color=&quot;#059669&quot;&gt;// 3. Sau khi ghi xong Sector 48 (Whitelist) / 49 (Log), quay lại XIP&lt;/font&gt;&lt;br&gt;}&lt;/font&gt;&lt;hr&gt;&lt;font size=&quot;1&quot; color=&quot;#334155&quot;&gt;&amp;bull; &lt;b&gt;Xung đột XIP&lt;/b&gt;: Flash không thể vừa đọc opcode vừa xóa chip.&lt;br&gt;&amp;bull; &lt;b&gt;Giải pháp&lt;/b&gt;: CPU tạm thời chạy hoàn toàn trên 1KB SRAM.&lt;/font&gt;" style="swimlane;whiteSpace=wrap;html=1;collapsible=1;startSize=28;fillColor=#FFFFFF;strokeColor=#7C3AED;strokeWidth=2;align=left;verticalAlign=top;spacingLeft=12;spacingTop=8;fontFamily=Segoe UI;fontColor=#0F172A;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="1840" y="150" width="530" height="300" as="geometry" />
        </mxCell>

        <!-- CARD 7: soc_interconnect.v Flash -->
        <mxCell id="card_ic_flash" value="&lt;b&gt;rtl/core/soc_interconnect.v&lt;/b&gt; [Flash Decoding &amp;amp; Mux]&lt;hr&gt;&lt;font face=&quot;Consolas&quot; size=&quot;2&quot;&gt;&lt;b&gt;// 7. Logic Phân Luồng Flash XIP (Đọc) &amp;amp; MMIO Bit-bang (Ghi/Xóa)&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#0284C7&quot;&gt;assign&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#0284C7&quot;&gt;sel_spimem&lt;/font&gt;&lt;/b&gt; = cpu_mem_valid &amp;amp;&amp;amp; (cpu_mem_addr &amp;gt;= &lt;b&gt;&lt;font color=&quot;#D97706&quot;&gt;32&#39;h0010_0000&lt;/font&gt;&lt;/b&gt; &amp;amp;&amp;amp; cpu_mem_addr &amp;lt; &lt;b&gt;&lt;font color=&quot;#D97706&quot;&gt;32&#39;h0100_0000&lt;/font&gt;&lt;/b&gt;); &lt;font color=&quot;#64748B&quot;&gt;// Dải XIP 15MB&lt;/font&gt;&lt;br&gt;&lt;font color=&quot;#0284C7&quot;&gt;assign&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#E11D48&quot;&gt;sel_spicfg&lt;/font&gt;&lt;/b&gt; = cpu_mem_valid &amp;amp;&amp;amp; (cpu_mem_addr == &lt;b&gt;&lt;font color=&quot;#E11D48&quot;&gt;32&#39;h0200_0000&lt;/font&gt;&lt;/b&gt;);                           &lt;font color=&quot;#64748B&quot;&gt;// Thanh ghi SPI MMIO&lt;/font&gt;&lt;br&gt;&lt;br&gt;&lt;font color=&quot;#0284C7&quot;&gt;assign&lt;/font&gt; cpu_mem_rdata = sel_spimem ? spimem_rdata :&lt;br&gt;                       sel_spicfg ? spimem_cfg_do : ...;&lt;br&gt;&lt;font color=&quot;#0284C7&quot;&gt;assign&lt;/font&gt; cpu_mem_ready = spimem_ready || sel_spicfg || ...;&lt;/font&gt;&lt;hr&gt;&lt;font size=&quot;1&quot; color=&quot;#334155&quot;&gt;&amp;bull; &lt;b&gt;Tách bạch hoàn toàn&lt;/b&gt;: Đọc opcode đi đường spimem, ghi xóa đi đường spicfg.&lt;br&gt;&amp;bull; &lt;b&gt;zero-delay&lt;/b&gt;: Mạch tổ hợp giải mã phân luồng tức thì trong 0 chu kỳ clock.&lt;/font&gt;" style="swimlane;whiteSpace=wrap;html=1;collapsible=1;startSize=28;fillColor=#FFFFFF;strokeColor=#0284C7;strokeWidth=2;align=left;verticalAlign=top;spacingLeft=12;spacingTop=8;fontFamily=Segoe UI;fontColor=#0F172A;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="1270" y="490" width="1100" height="300" as="geometry" />
        </mxCell>

        <!-- ============================================================= -->
        <!-- PHÂN HỆ 3: MMIO INTERCONNECT & PERIPHERALS                     -->
        <!-- ============================================================= -->
        <mxCell id="bg_grp3" value="&lt;b style=&quot;font-size:14px; color:#15803D;&quot;&gt;PHÂN HỆ 3: LIÊN KẾT BUS INTERCONNECT &amp;amp; DRIVER ĐIỀU KHIỂN NGOẠI VI MMIO (DUAL UART &amp;amp; GPIO)&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F0FDF4;strokeColor=#15803D;strokeWidth=2;verticalAlign=top;align=left;spacingLeft=20;spacingTop=12;fontFamily=Segoe UI;" vertex="1" parent="1">
          <mxGeometry x="40" y="860" width="2360" height="660" as="geometry" />
        </mxCell>

        <!-- CARD 8: soc_interconnect.v MMIO -->
        <mxCell id="card_ic_mmio" value="&lt;b&gt;rtl/core/soc_interconnect.v&lt;/b&gt; [Address Decoder &amp;amp; Master Mux]&lt;hr&gt;&lt;font face=&quot;Consolas&quot; size=&quot;2&quot;&gt;&lt;b&gt;// 8. Giải Mã 4-bit Cao Địa Chỉ (Top 4-bit Prefix Decoding)&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#0284C7&quot;&gt;assign&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#059669&quot;&gt;sel_sram&lt;/font&gt;&lt;/b&gt; = cpu_mem_valid &amp;amp;&amp;amp; (cpu_mem_addr &amp;lt; &lt;b&gt;32&#39;h0000_0400&lt;/b&gt;);         &lt;font color=&quot;#64748B&quot;&gt;// 1KB RAM&lt;/font&gt;&lt;br&gt;&lt;font color=&quot;#0284C7&quot;&gt;assign&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#D97706&quot;&gt;sel_rfid&lt;/font&gt;&lt;/b&gt; = cpu_mem_valid &amp;amp;&amp;amp; (cpu_mem_addr[31:28] == &lt;b&gt;4&#39;h1&lt;/b&gt;);         &lt;font color=&quot;#64748B&quot;&gt;// 0x1000_0000&lt;/font&gt;&lt;br&gt;&lt;font color=&quot;#0284C7&quot;&gt;assign&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#0284C7&quot;&gt;sel_uart&lt;/font&gt;&lt;/b&gt; = cpu_mem_valid &amp;amp;&amp;amp; (cpu_mem_addr[31:28] == &lt;b&gt;4&#39;h3&lt;/b&gt;);         &lt;font color=&quot;#64748B&quot;&gt;// 0x3000_0000&lt;/font&gt;&lt;br&gt;&lt;font color=&quot;#0284C7&quot;&gt;assign&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#7C3AED&quot;&gt;sel_gpio&lt;/font&gt;&lt;/b&gt; = cpu_mem_valid &amp;amp;&amp;amp; (cpu_mem_addr[31:28] == &lt;b&gt;4&#39;h4&lt;/b&gt;);         &lt;font color=&quot;#64748B&quot;&gt;// 0x4000_0000&lt;/font&gt;&lt;br&gt;&lt;br&gt;&lt;font color=&quot;#0284C7&quot;&gt;assign&lt;/font&gt; cpu_mem_ready = sram_ready || spimem_ready || sel_spicfg ||&lt;br&gt;                       rfid_ready || uart_ready   || gpio_ready;&lt;/font&gt;&lt;hr&gt;&lt;font size=&quot;1&quot; color=&quot;#334155&quot;&gt;&amp;bull; &lt;b&gt;Zero Wait-State&lt;/b&gt;: Mọi ngoại vi phản hồi ready = 1 tức thì, không stall CPU.&lt;br&gt;&amp;bull; &lt;b&gt;1 Master - 5 Slaves&lt;/b&gt;: Phân định mạch lạc, bus sạch không xung đột.&lt;/font&gt;" style="swimlane;whiteSpace=wrap;html=1;collapsible=1;startSize=28;fillColor=#FFFFFF;strokeColor=#0F172A;strokeWidth=2;align=left;verticalAlign=top;spacingLeft=12;spacingTop=8;fontFamily=Segoe UI;fontColor=#0F172A;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="70" y="910" width="720" height="280" as="geometry" />
        </mxCell>

        <!-- CARD 9: uart_mmio.v -->
        <mxCell id="card_uart" value="&lt;b&gt;rtl/uart/uart_mmio.v&lt;/b&gt; [Dual UART &amp;amp; FIFO 32B]&lt;hr&gt;&lt;font face=&quot;Consolas&quot; size=&quot;2&quot;&gt;&lt;b&gt;// 9. Khối Ghép Nối UART MMIO &amp;amp; FIFO Đệm 32 Byte&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#0284C7&quot;&gt;wire&lt;/font&gt; reg_div_sel = valid &amp;amp;&amp;amp; (addr[2] == &lt;b&gt;1&#39;b0&lt;/b&gt;); &lt;font color=&quot;#64748B&quot;&gt;// Offset 0x00: Baud Divider&lt;/font&gt;&lt;br&gt;&lt;font color=&quot;#0284C7&quot;&gt;wire&lt;/font&gt; reg_dat_sel = valid &amp;amp;&amp;amp; (addr[2] == &lt;b&gt;1&#39;b1&lt;/b&gt;); &lt;font color=&quot;#64748B&quot;&gt;// Offset 0x04: Data Register&lt;/font&gt;&lt;br&gt;&lt;br&gt;&lt;font color=&quot;#0284C7&quot;&gt;assign&lt;/font&gt; reg_dat_do = fifo_empty ? &lt;b&gt;&lt;font color=&quot;#E11D48&quot;&gt;32&#39;hFFFFFFFF&lt;/font&gt;&lt;/b&gt; : {24&#39;d0, fifo_dout};&lt;br&gt;&lt;font color=&quot;#0284C7&quot;&gt;assign&lt;/font&gt; ready = 1&#39;b1; &lt;font color=&quot;#64748B&quot;&gt;// Zero Wait-state response&lt;/font&gt;&lt;/font&gt;&lt;hr&gt;&lt;font size=&quot;1&quot; color=&quot;#334155&quot;&gt;&amp;bull; &lt;b&gt;Đọc không khóa&lt;/b&gt;: Có dữ liệu trả mã ký tự, rỗng trả về 0xFFFFFFFF.&lt;br&gt;&amp;bull; &lt;b&gt;FIFO 32 Byte&lt;/b&gt;: Hứng trọn 14 byte chuỗi thẻ RFID mà không bị tràn/rơi dữ liệu.&lt;/font&gt;" style="swimlane;whiteSpace=wrap;html=1;collapsible=1;startSize=28;fillColor=#FFFFFF;strokeColor=#1E3A8A;strokeWidth=2;align=left;verticalAlign=top;spacingLeft=12;spacingTop=8;fontFamily=Segoe UI;fontColor=#0F172A;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="840" y="910" width="700" height="280" as="geometry" />
        </mxCell>

        <!-- CARD 10: soc_regs.h -->
        <mxCell id="card_regs" value="&lt;b&gt;firmware/common/soc_regs.h&lt;/b&gt; [Firmware Memory Map]&lt;hr&gt;&lt;font face=&quot;Consolas&quot; size=&quot;2&quot;&gt;&lt;b&gt;// 10. Định Nghĩa Con Trỏ Volatile Ánh Xạ Phần Cứng C&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#0284C7&quot;&gt;#define&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#D97706&quot;&gt;REG_RFID_UART_DIV&lt;/font&gt;&lt;/b&gt; (*(&lt;font color=&quot;#0284C7&quot;&gt;volatile uint32_t*&lt;/font&gt;)&lt;b&gt;0x10000000&lt;/b&gt;)&lt;br&gt;&lt;font color=&quot;#0284C7&quot;&gt;#define&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#D97706&quot;&gt;REG_RFID_UART_DAT&lt;/font&gt;&lt;/b&gt; (*(&lt;font color=&quot;#0284C7&quot;&gt;volatile uint32_t*&lt;/font&gt;)&lt;b&gt;0x10000004&lt;/b&gt;)&lt;br&gt;&lt;font color=&quot;#0284C7&quot;&gt;#define&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#0284C7&quot;&gt;REG_PC_UART_DIV&lt;/font&gt;&lt;/b&gt;   (*(&lt;font color=&quot;#0284C7&quot;&gt;volatile uint32_t*&lt;/font&gt;)&lt;b&gt;0x30000000&lt;/b&gt;)&lt;br&gt;&lt;font color=&quot;#0284C7&quot;&gt;#define&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#0284C7&quot;&gt;REG_PC_UART_DAT&lt;/font&gt;&lt;/b&gt;   (*(&lt;font color=&quot;#0284C7&quot;&gt;volatile uint32_t*&lt;/font&gt;)&lt;b&gt;0x30000004&lt;/b&gt;)&lt;br&gt;&lt;font color=&quot;#0284C7&quot;&gt;#define&lt;/font&gt; &lt;b&gt;&lt;font color=&quot;#7C3AED&quot;&gt;REG_GPIO_LEDS&lt;/font&gt;&lt;/b&gt;     (*(&lt;font color=&quot;#0284C7&quot;&gt;volatile uint32_t*&lt;/font&gt;)&lt;b&gt;0x40000000&lt;/b&gt;)&lt;/font&gt;&lt;hr&gt;&lt;font size=&quot;1&quot; color=&quot;#334155&quot;&gt;&amp;bull; &lt;b&gt;volatile&lt;/b&gt;: Ép GCC luôn phát sinh lệnh load/store bus, không cache thanh ghi CPU.&lt;br&gt;&amp;bull; &lt;b&gt;Đồng bộ 100%&lt;/b&gt;: Tương ứng các tín hiệu sel_rfid, sel_uart, sel_gpio của Interconnect.&lt;/font&gt;" style="swimlane;whiteSpace=wrap;html=1;collapsible=1;startSize=28;fillColor=#FFFFFF;strokeColor=#15803D;strokeWidth=2;align=left;verticalAlign=top;spacingLeft=12;spacingTop=8;fontFamily=Segoe UI;fontColor=#0F172A;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="1590" y="910" width="780" height="280" as="geometry" />
        </mxCell>

        <!-- CARD 11: access_control.c -->
        <mxCell id="card_app" value="&lt;b&gt;firmware/access_control.c&lt;/b&gt; [Application Logic &amp;amp; Driver Polling]&lt;hr&gt;&lt;font face=&quot;Consolas&quot; size=&quot;2&quot;&gt;&lt;b&gt;// 11. Ứng Dụng C Polling Thẻ RFID Non-blocking &amp;amp; Điều Khiển Chốt Cửa&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#0284C7&quot;&gt;void&lt;/font&gt; &lt;b&gt;access_control_poll&lt;/b&gt;(void) {&lt;br&gt;    &lt;font color=&quot;#0284C7&quot;&gt;uint32_t&lt;/font&gt; d = &lt;b&gt;&lt;font color=&quot;#D97706&quot;&gt;REG_RFID_UART_DAT&lt;/font&gt;&lt;/b&gt;; &lt;font color=&quot;#64748B&quot;&gt;// Đọc FIFO phần cứng (Non-blocking)&lt;/font&gt;&lt;br&gt;    &lt;font color=&quot;#E11D48&quot;&gt;if&lt;/font&gt; (d != &lt;b&gt;&lt;font color=&quot;#E11D48&quot;&gt;0xFFFFFFFF&lt;/font&gt;&lt;/b&gt;) {&lt;br&gt;        rdm6300_push((&lt;font color=&quot;#0284C7&quot;&gt;uint8_t&lt;/font&gt;)d);  &lt;font color=&quot;#64748B&quot;&gt;// Nạp ký tự vào parser kiểm tra checksum XOR&lt;/font&gt;&lt;br&gt;    }&lt;br&gt;&lt;br&gt;    &lt;font color=&quot;#64748B&quot;&gt;// Khi thẻ hợp lệ trong Whitelist: Bật LED xanh &amp;amp; mở relay chốt cửa&lt;/font&gt;&lt;br&gt;    &lt;b&gt;&lt;font color=&quot;#7C3AED&quot;&gt;REG_GPIO_LEDS&lt;/font&gt;&lt;/b&gt; = (&lt;font color=&quot;#7C3AED&quot;&gt;REG_GPIO_LEDS&lt;/font&gt; &amp;amp; ~0x0002) | 0x0004; &lt;font color=&quot;#64748B&quot;&gt;// Bit 2: Door Open&lt;/font&gt;&lt;br&gt;}&lt;/font&gt;&lt;hr&gt;&lt;font size=&quot;1&quot; color=&quot;#334155&quot;&gt;&amp;bull; &lt;b&gt;Polling không khóa&lt;/b&gt;: Không sợ treo CPU nếu chưa có thẻ quẹt.&lt;br&gt;&amp;bull; &lt;b&gt;Độ trễ thấp&lt;/b&gt;: Thời gian từ lúc quẹt thẻ đến kích mở chốt cửa chỉ mất chưa đầy 10 µs.&lt;/font&gt;" style="swimlane;whiteSpace=wrap;html=1;collapsible=1;startSize=28;fillColor=#FFFFFF;strokeColor=#15803D;strokeWidth=2;align=left;verticalAlign=top;spacingLeft=12;spacingTop=8;fontFamily=Segoe UI;fontColor=#0F172A;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="70" y="1230" width="2300" height="260" as="geometry" />
        </mxCell>

        <!-- ============================================================= -->
        <!-- MŨI TÊN KẾT NỐI CO-DESIGN (ALL ON PARENT 1)                   -->
        <!-- ============================================================= -->

        <!-- Link 1: Top -> Linker -->
        <mxCell id="edge1" value="&lt;b&gt;Boot Vector: PROGADDR_RESET = ORIGIN FLASH = 0x0025_0000&lt;/b&gt;" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#D97706;strokeWidth=2.5;fontColor=#B45309;fontFamily=Segoe UI;fontSize=11;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="card_top" target="card_lds">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Link 2: Top -> CPU Core -->
        <mxCell id="edge2" value="&lt;b&gt;Nạp Tham Số Lõi CPU: PROGADDR_RESET &amp;amp; STACKADDR&lt;/b&gt;" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#0284C7;strokeWidth=2.5;fontColor=#0369A1;fontFamily=Segoe UI;fontSize=11;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="card_top" target="card_cpu">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Link 3: Linker -> Assembly start.s -->
        <mxCell id="edge3" value="&lt;b&gt;Khởi Tạo Ngăn Xếp: _stack_top (0x0400) -&amp;gt; lui sp, %hi(_stack_top)&lt;/b&gt;" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#059669;strokeWidth=2.5;fontColor=#059669;fontFamily=Segoe UI;fontSize=11;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="card_lds" target="card_start">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Link 4: Assembly start.s -> C Application -->
        <mxCell id="edge4" value="&lt;b&gt;Chuyển Giao Quyền Điều Khiển: call main() -&amp;gt; firmware C&lt;/b&gt;" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#E11D48;strokeWidth=2.5;fontColor=#BE123C;fontFamily=Segoe UI;fontSize=11;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="card_start" target="card_app">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="905" y="820" />
              <mxPoint x="500" y="820" />
              <mxPoint x="500" y="1230" />
            </Array>
          </mxGeometry>
        </mxCell>

        <!-- Link 5: Interconnect Flash -> spimemio -->
        <mxCell id="edge5" value="&lt;b&gt;sel_spimem: Kéo Opcode XIP (0x0010_0000 - 0x00FF_FFFF)&lt;/b&gt;" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#D97706;strokeWidth=2.5;fontColor=#B45309;fontFamily=Segoe UI;fontSize=11;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="card_ic_flash" target="card_spimem">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Link 6: Interconnect Flash -> flash.c -->
        <mxCell id="edge6" value="&lt;b&gt;sel_spicfg: Bit-bang Ghi Flash (0x0200_0000) từ RAM Routine&lt;/b&gt;" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#7C3AED;strokeWidth=2.5;fontColor=#6D28D9;fontFamily=Segoe UI;fontSize=11;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="card_ic_flash" target="card_flashc">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Link 7: Interconnect MMIO -> uart_mmio.v -->
        <mxCell id="edge7" value="&lt;b&gt;sel_rfid (4&#39;h1: 0x1000_0000) &amp;amp; sel_uart (4&#39;h3: 0x3000_0000)&lt;/b&gt;" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#0284C7;strokeWidth=2.5;fontColor=#0369A1;fontFamily=Segoe UI;fontSize=11;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="card_ic_mmio" target="card_uart">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Link 8: uart_mmio.v -> soc_regs.h -->
        <mxCell id="edge8" value="&lt;b&gt;Ánh Xạ Địa Chỉ MMIO: Offset 0x00 (Divider) &amp;amp; 0x04 (Data FIFO)&lt;/b&gt;" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#15803D;strokeWidth=2.5;fontColor=#15803D;fontFamily=Segoe UI;fontSize=11;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="card_uart" target="card_regs">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Link 9: soc_regs.h -> access_control.c -->
        <mxCell id="edge9" value="&lt;b&gt;REG_RFID_UART_DAT (0x10000004) &amp;amp; REG_GPIO_LEDS (0x40000000)&lt;/b&gt;" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#15803D;strokeWidth=2.5;fontColor=#15803D;fontFamily=Segoe UI;fontSize=11;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="card_regs" target="card_app">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="1980" y="1210" />
              <mxPoint x="1800" y="1210" />
            </Array>
          </mxGeometry>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
    with open(r"d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\soc_codesign_architecture.drawio", "w", encoding="utf-8") as f:
        f.write(xml_content.strip())
    print("Regenerated soc_codesign_architecture.drawio with flat parent='1' structure!")

if __name__ == "__main__":
    generate_drawio()
