import os

def update_presentation():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    target_file = os.path.join(cur_dir, "create_presentation.py")

    with open(target_file, "r", encoding="utf-8") as f:
        code = f.read()

    # Define the improved map_rows_data
    old_block_start = "    map_rows_data = ["
    old_block_end = "    for r_idx, r_tuples in enumerate(map_rows_data, 1):"

    new_map_rows = '''    map_rows_data = [
        (
            [("0x0000_0000", True, C_BLUE_ACCENT), ("\\n- 0x0000_03FF", False, C_TEXT_DARK), ("\\n(1KB Data SRAM)", True, C_TEXT_MUTED)],
            [("• C/Linker: ", True, C_BLUE_ACCENT), ("sections.lds\\n  (RAM: 0x0, _stack_top: 0x400)\\n", False, C_TEXT_DARK),
             ("• RTL: ", True, C_PURPLE), ("soc_interconnect.v\\n  (sel_sram < 0x400), data_sram.v", False, C_TEXT_DARK)],
            [("👉 Cách dùng: ", True, C_BLUE_ACCENT), ("Linker gán sp = 0x400. Trình biên dịch C tự sinh lệnh sw/lw để quản lý Stack frame và biến cục bộ.\\n", False, C_TEXT_DARK),
             ("🎯 Tác dụng: ", True, C_GREEN), ("Bộ nhớ RAM tĩnh 1 chu kỳ clock (20ns), giúp CPU thực thi hàm C không bị stall và không trễ luồng UART.", False, C_TEXT_MUTED)]
        ),
        (
            [("0x0010_0000", True, C_BLUE_ACCENT), ("\\n- 0x00FF_FFFF", False, C_TEXT_DARK), ("\\n(SPI Flash XIP 4MB)", True, C_GREEN)],
            [("• C/Linker: ", True, C_BLUE_ACCENT), ("sections.lds (FLASH: 0x250000)\\n  soc_regs.h (USER: 0x300000, LOG: 0x310000)\\n", False, C_TEXT_DARK),
             ("• RTL: ", True, C_PURPLE), ("soc_interconnect.v\\n  (sel_spimem), spimemio.v", False, C_TEXT_DARK)],
            [("👉 Cách dùng: ", True, C_BLUE_ACCENT), ("Đọc trực tiếp qua con trỏ C: (uint32_t*)USER_FLASH_ADDR hoặc CPU tự nạp lệnh tại 0x0025_0000.\\n", False, C_TEXT_DARK),
             ("🎯 Tác dụng: ", True, C_GREEN), ("Thực thi Firmware tại chỗ (XIP); tra cứu 4.096 thẻ Whitelist và đọc 512 log điểm danh an toàn, không mất khi tắt nguồn.", False, C_TEXT_MUTED)]
        ),
        (
            [("0x0200_0000", True, C_BLUE_ACCENT), ("\\n(SPIMEMIO Cfg)", True, C_TEXT_MUTED)],
            [("• C/ASM: ", True, C_BLUE_ACCENT), ("start.s (li t0, 0x02000000)\\n  Hàm nạp RAM flashio_worker()\\n", False, C_TEXT_DARK),
             ("• RTL: ", True, C_PURPLE), ("soc_interconnect.v\\n  (sel_spicfg == 0x02000000), spimemio.v", False, C_TEXT_DARK)],
            [("👉 Cách dùng: ", True, C_BLUE_ACCENT), ("Nạp hàm vào RAM, ghi 0x120 để chuyển sang Bit-bang, phát xung ghi/xóa, sau đó ghi 0x80 về lại XIP.\\n", False, C_TEXT_DARK),
             ("🎯 Tác dụng: ", True, C_GREEN), ("Cho phép xóa Sector (0x20) và ghi trang (0x02) Flash ngoài để lưu thẻ/log mới an toàn mà không nghẽn bus CPU.", False, C_TEXT_MUTED)]
        ),
        (
            [("0x1000_0000 (DIV)\\n0x1000_0004 (DAT)", True, C_BLUE_ACCENT), ("\\n(RFID RDM6300 UART)", True, C_ROSE)],
            [("• C Driver: ", True, C_BLUE_ACCENT), ("soc_regs.h\\n  REG_RFID_UART_DIV, REG_RFID_UART_DAT\\n", False, C_TEXT_DARK),
             ("• RTL: ", True, C_PURPLE), ("soc_interconnect.v (sel_rfid)\\n  u_rfid_uart (uart_mmio.v)", False, C_TEXT_DARK)],
            [("👉 Cách dùng: ", True, C_BLUE_ACCENT), ("Ghi DIV = 5208 (9600 baud). Vòng lặp C đọc: uint32_t d = REG_RFID_UART_DAT; if (d != 0xFFFFFFFF) buffer[i++] = d & 0xFF;\\n", False, C_TEXT_DARK),
             ("🎯 Tác dụng: ", True, C_GREEN), ("Rút từng byte từ RX FIFO 32B, tự ghép 14-byte frame thẻ RFID (STX/ETX/Checksum) và chống rớt gói tin khi CPU bận.", False, C_TEXT_MUTED)]
        ),
        (
            [("0x3000_0000 (DIV)\\n0x3000_0004 (DAT)", True, C_BLUE_ACCENT), ("\\n(Host PC Console UART)", True, C_AMBER)],
            [("• C Driver: ", True, C_BLUE_ACCENT), ("soc_regs.h\\n  REG_PC_UART_DIV, REG_PC_UART_DAT\\n", False, C_TEXT_DARK),
             ("• RTL: ", True, C_PURPLE), ("soc_interconnect.v (sel_uart)\\n  u_host_uart (uart_mmio.v)", False, C_TEXT_DARK)],
            [("👉 Cách dùng: ", True, C_BLUE_ACCENT), ("Ghi DIV = 434 (115200 baud). Nhận phím: cmd = REG_PC_UART_DAT; và gửi log: REG_PC_UART_DAT = c;\\n", False, C_TEXT_DARK),
             ("🎯 Tác dụng: ", True, C_GREEN), ("Truyền nhận 2 chiều có FIFO với Host PC Console (xử lý 10 menu lệnh điều khiển CLI và xuất dữ liệu điểm danh).", False, C_TEXT_MUTED)]
        ),
        (
            [("0x4000_0000", True, C_BLUE_ACCENT), ("\\n(GPIO Status LEDs)", True, C_GREEN)],
            [("• C Driver: ", True, C_BLUE_ACCENT), ("soc_regs.h\\n  REG_GPIO_LEDS\\n", False, C_TEXT_DARK),
             ("• RTL: ", True, C_PURPLE), ("soc_interconnect.v (sel_gpio)\\n  soc_gpio_mmio.v", False, C_TEXT_DARK)],
            [("👉 Cách dùng: ", True, C_BLUE_ACCENT), ("Thao tác bitmask C: REG_GPIO_LEDS |= (1<<2); (bật Granted), REG_GPIO_LEDS &= ~(1<<1); (tắt Warn).\\n", False, C_TEXT_DARK),
             ("🎯 Tác dụng: ", True, C_GREEN), ("Điều khiển 5 LED hiển thị trực quan trạng thái: Alive (hệ thống sống), Warn (thẻ sai), Granted (mở cửa), Flash, Save OK.", False, C_TEXT_MUTED)]
        )
    ]'''

    idx_start = code.find(old_block_start)
    idx_end = code.find(old_block_end)

    if idx_start != -1 and idx_end != -1:
        code = code[:idx_start] + new_map_rows + "\n\n" + code[idx_end:]
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(code)
        print("Updated create_presentation.py with 'Cách dùng' and 'Tác dụng'!")
    else:
        print(f"Failed to find target block: start={idx_start}, end={idx_end}")

if __name__ == "__main__":
    update_presentation()
