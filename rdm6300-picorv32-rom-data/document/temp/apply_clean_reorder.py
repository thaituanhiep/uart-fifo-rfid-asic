# -*- coding: utf-8 -*-
"""
Script: apply_clean_reorder.py
Sắp xếp lại các slide sạch sẽ, không dùng re.sub để tránh lỗi escape ký tự tiếng Việt và ký tự xuống dòng \n.
"""
import os
import re

cur_dir = os.path.dirname(os.path.abspath(__file__))
target_file = os.path.join(cur_dir, "create_presentation.py")

with open(target_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Let's inspect slide markers by line index
slide_indices = []
for idx, line in enumerate(lines):
    m = re.match(r'^\s*# =+\s*# SLIDE (\d+):', line)
    if m:
        slide_indices.append((int(m.group(1)), idx))

print("Found slides:", slide_indices)
