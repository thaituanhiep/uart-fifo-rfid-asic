# -*- coding: utf-8 -*-
import os

pres_path = r"d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\create_presentation.py"
with open(pres_path, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "    all_rows_bus = ["
end_marker = "    s11 = add_bus_table_slide(11,"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

new_all_rows = '''    all_rows_bus = [
        {
            "time": "T = 0",
            "task": "(Boot Flash XIP)",
            "rtl_file": "[rdm6300_picorv32_soc.v & soc_interconnect.v]",
            "rtl_code": "parameter [31:0] PROGADDR_RESET = 32\\'h0025_0000;\\nassign sel_spimem = cpu_mem_valid && (cpu_mem_addr >= 32\\'h0010_0000 && cpu_mem_addr < 32\\'h0100_0000);",
            "c_file": "[sections.lds & start.s]",
            "c_code": "FLASH (rx) : ORIGIN = 0x00250000, LENGTH = 0x000B0000\\n_start: lui sp, %hi(_stack_top)",
            "meaning": "Cấu hình vector reset trỏ thẳng vào Flash SPI để CPU tự động nạp và thực thi trực tiếp opcode firmware (XIP) ngay sau khi nhả reset mà không cần nạp vào RAM."
        },
        {
            "time": "T = 1..100",
            "task": "(Tạo Stack RAM)",
            "rtl_file": "[rdm6300_picorv32_soc.v & soc_interconnect.v]",
            "rtl_code": "parameter [31:0] STACKADDR = 32\\'h0000_0400;\\nassign sel_sram = cpu_mem_valid && (cpu_mem_addr < 32\\'h0000_0400);\\nassign sram_ready = 1\\'b1;",
            "c_file": "[sections.lds & start.s]",
            "c_code": "RAM (rwx) : ORIGIN = 0x00000000, LENGTH = 0x00000400\\nlui sp, %hi(_stack_top); addi sp, sp, %lo(_stack_top);",
            "meaning": "C sử dụng không gian SRAM 1KB (< 0x0400) qua con trỏ ngăn xếp sp để cấp phát biến cục bộ, lưu stack frame và địa chỉ trả về hàm, phản hồi tức thì trong 1 chu kỳ clock."
        },
        {
            "time": "T = 101",
            "task": "(Vào hàm main)",
            "rtl_file": "[soc_interconnect.v]",
            "rtl_code": "assign sel_spimem = cpu_mem_valid && (cpu_mem_addr >= 32\\'h0010_0000 && ...);\\nassign cpu_mem_rdata = sel_spimem ? spimem_rdata : sel_sram ? sram_rdata : ...;",
            "c_file": "[start.s & main.c]",
            "c_code": "call main;\\nint main(void) { access_control_init(); while (1) access_control_poll(); }",
            "meaning": "Chuyển giao quyền điều khiển từ assembly khởi động sang code C bậc cao. Hàm main() chạy trực tiếp từ Flash XIP, giải phóng toàn bộ 1KB SRAM chỉ dùng cho dữ liệu động."
        },
        {
            "time": "T = 105",
            "task": "(Set Baud Dual UART)",
            "rtl_file": "[soc_interconnect.v & uart_mmio.v]",
            "rtl_code": "assign sel_rfid = cpu_mem_valid && (cpu_mem_addr[31:28] == 4\\'h1);\\nif (reg_div_sel && |cpu_mem_wstrb) uart_div <= cpu_mem_wdata;",
            "c_file": "[soc_regs.h & access_control.c]",
            "c_code": "#define REG_RFID_UART_DIV (*(volatile uint32_t*)0x10000000)\\nREG_RFID_UART_DIV = 5208; // 50 MHz / 9600 Baud",
            "meaning": "C ghi giá trị chia tần 5208 vào địa chỉ 0x10000000 và 0x30000000 để cài đặt tốc độ baud 9600 bps cho cả đầu đọc RFID RDM6300 và cổng máy tính PC (50 MHz / 9600)."
        },
        {
            "time": "T = 200",
            "task": "(Đọc thẻ RFID)",
            "rtl_file": "[uart_mmio.v & simpleuart_fifo.v]",
            "rtl_code": "wire reg_dat_sel = valid && (addr[2] == 1\\'b1);\\nassign reg_dat_do = fifo_empty ? 32\\'hFFFFFFFF : {24\\'d0, fifo_dout};",
            "c_file": "[soc_regs.h & access_control.c]",
            "c_code": "#define REG_RFID_UART_DAT (*(volatile uint32_t*)0x10000004)\\nuint32_t d = REG_RFID_UART_DAT; if (d != 0xFFFFFFFF) rdm6300_push(d);",
            "meaning": "C đọc từ 0x10000004 rút (pop) 1 byte từ FIFO 32B (đọc không khóa: trả về byte mã thẻ nếu có, hoặc trả về 0xFFFFFFFF nếu FIFO rỗng để CPU không bị nghẽn bus)."
        },
        {
            "time": "T = 250",
            "task": "(Giao tiếp PC UART)",
            "rtl_file": "[soc_interconnect.v & uart_mmio.v]",
            "rtl_code": "assign sel_uart = cpu_mem_valid && (cpu_mem_addr[31:28] == 4\\'h3);\\nwire dat_we = reg_dat_sel && (|wstrb); // Write TX FIFO",
            "c_file": "[soc_regs.h & uart.c]",
            "c_code": "#define REG_PC_UART_DAT (*(volatile uint32_t*)0x30000004)\\nREG_PC_UART_DAT = c; /* Ghi TX */ | d = REG_PC_UART_DAT; /* Doc RX */",
            "meaning": "C ghi byte vào 0x30000004 để đẩy ký tự vào TX FIFO truyền lên Host PC, và đọc từ địa chỉ này để nhận chuỗi lệnh quản trị (Ping, thêm/xóa thẻ Whitelist, xuất log CSV)."
        },
        {
            "time": "T = 300",
            "task": "(Bật LED / Mở Cửa)",
            "rtl_file": "[soc_interconnect.v & soc_gpio_mmio.v]",
            "rtl_code": "assign sel_gpio = cpu_mem_valid && (cpu_mem_addr[31:28] == 4\\'h4);\\nif (sel_gpio && |wstrb) gpio_led_reg[7:0] <= wdata[7:0];",
            "c_file": "[soc_regs.h & access_control.c]",
            "c_code": "#define REG_GPIO_LEDS (*(volatile uint32_t*)0x40000000)\\nREG_GPIO_LEDS = (REG_GPIO_LEDS & ~0x0002) | 0x0004; // Bit 2: Granted",
            "meaning": "C ghi giá trị bitmask vào 0x40000000 điều khiển 16 LED chẩn đoán trên bo mạch và đóng/ngắt relay mở chốt cửa điện từ (Bit 0: Alive 1Hz, Bit 1: Denied, Bit 2: Granted)."
        },
        {
            "time": "T = 400",
            "task": "(Ghi Flash từ RAM)",
            "rtl_file": "[soc_interconnect.v & spimemio.v]",
            "rtl_code": "assign sel_spicfg = cpu_mem_valid && (cpu_mem_addr == 32\\'h0200_0000);\\n.cfgreg_we(sel_spicfg ? mem_wstrb : 4\\'b0000), .cfgreg_di(mem_wdata)",
            "c_file": "[start.s & flash.c]",
            "c_code": "flashio_worker: li t0, 0x02000000; sh t1, 0(t0);\\nstatic void flashio(uint8_t *data, int len, uint8_t wrencmd);",
            "meaning": "Khi chạy từ SRAM, hàm của C phát lệnh bit-bang SPI vào 0x02000000 để xóa sector và ghi dữ liệu thẻ mới vào Flash Whitelist / Log mà không gây xung đột bus với các lệnh XIP."
        }
    ]
    '''

updated_content = content[:start_idx] + new_all_rows + content[end_idx:]
with open(pres_path, "w", encoding="utf-8") as f:
    f.write(updated_content)
print("Successfully fixed all_rows_bus in create_presentation.py")
