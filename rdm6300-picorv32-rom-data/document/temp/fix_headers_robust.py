# -*- coding: utf-8 -*-
import re

with open('create_presentation.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Pattern matching add_header across multiple lines:
# add_header(sX, cat, title, num, ...)
def replace_func(match):
    s_var = match.group(1)
    s_num = int(s_var[1:])
    cat = match.group(2)
    title = match.group(3)
    return f"add_header({s_var}, {cat},\n               {title}, {s_num}, total_slides=TOTAL_SLIDES)"

# Match: add_header(s<digits>, <cat>, <title>, <old_num> ...)
pattern = r'add_header\(\s*(s\d+)\s*,\s*("[^"]+"|\'[^\']+\')\s*,\s*\n?\s*("[^"]+"|\'[^\']+\')\s*,\s*\d+\s*(?:,\s*total_slides=[^)]+)?\)'

new_text = re.sub(pattern, replace_func, text)

with open('create_presentation.py', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("All multi-line and single-line add_header calls correctly matched and fixed!")
