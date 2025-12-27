#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import json

# 读取 JSON 数据
with open('rawData.json', 'r', encoding='utf-8') as f:
    json_data = f.read()

# 读取 HTML 文件
with open('index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 使用正则表达式替换 rawData
# 匹配 const rawData = [...]; 的内容
pattern = r'(const rawData = )\[[\s\S]*?\];'
replacement = f'\\1{json_data};'

new_html = re.sub(pattern, replacement, html_content)

# 写回 HTML 文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("替换完成！index.html 已更新")
