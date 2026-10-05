# -*- coding: utf-8 -*-
import re

with open('create_presentation.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    m = re.match(r'^(\s*)add_header\(\s*(s\d+)\s*,\s*(.*?),\s*(.*?),\s*(\d+)(.*)\)', line)
    if m:
        indent = m.group(1)
        s_var = m.group(2)
        s_num = int(s_var[1:])
        cat = m.group(3)
        title = m.group(4)
        new_line = f"{indent}add_header({s_var}, {cat}, {title}, {s_num}, total_slides=TOTAL_SLIDES)\n"
        new_lines.append(new_line)
    else:
        new_lines.append(line)

with open('create_presentation.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Headers updated successfully!")
