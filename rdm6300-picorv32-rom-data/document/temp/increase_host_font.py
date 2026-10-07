import os

def increase_terminal_font():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    target_file = os.path.join(cur_dir, "create_presentation.py")

    with open(target_file, "r", encoding="utf-8") as f:
        code = f.read()

    # Target line for Slide 5 code box
    old_call = 'add_code_box(s23, Inches(0.8), Inches(1.35), Inches(5.75), Inches(5.50), "Host Console C CLI (rdm6300_manager.exe)", host_menu_lines, status_text="=== UART COM3 @ 9600 bps | 10 CHỨC NĂNG QUẢN TRỊ TOÀN DIỆN ===", title_color=C_CYAN_ACCENT, font_size=8.8, line_spacing=1.18)'
    
    new_call = 'add_code_box(s23, Inches(0.8), Inches(1.35), Inches(5.75), Inches(5.50), "Host Console C CLI (rdm6300_manager.exe)", host_menu_lines, status_text="=== UART COM3 @ 9600 bps | 10 CHỨC NĂNG QUẢN TRỊ TOÀN DIỆN ===", title_color=C_CYAN_ACCENT, font_size=10.2, line_spacing=1.15)'

    if old_call in code:
        code = code.replace(old_call, new_call)
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(code)
        print("Increased Host Console font size to 10.2pt successfully!")
    else:
        print("Could not find exact old_call string, trying regex/partial search...")
        # fallback
        import re
        code = re.sub(r'add_code_box\(s23,.*?font_size=[\d\.]+,.*?line_spacing=[\d\.]+\)', new_call, code)
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(code)
        print("Replaced with regex!")

if __name__ == "__main__":
    increase_terminal_font()
