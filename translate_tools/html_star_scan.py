#!/usr/bin/env python3
"""Scan built HTML for literal '**' or lone '*' visible to readers (outside
<pre>, <code>, <script>, <style>). Ground-truth check for silent markup defects."""
import re
import sys
import pathlib

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else
                    '/home/nvidia/ROS2_documentation/build/html')
files = 0
total = 0
for p in sorted(root.rglob('*.html')):
    html = p.read_text(encoding='utf-8', errors='replace')
    html = re.sub(r'<(pre|code|script|style|tt)\b.*?</\1>', ' ', html, flags=re.S | re.I)
    text = re.sub(r'<[^>]+>', ' ', html)
    text = text.replace('&amp;', '&').replace('&#42;', '*')
    n = len(re.findall(r'\*\*', text))
    lone = len(re.findall(r'(?<!\*)\*(?!\*)', text))
    if n or lone:
        files += 1
        total += n + lone
        print('%-72s **:%d  *:%d' % (str(p.relative_to(root))[:72], n, lone))
print('HTML-FILES %d  LITERAL-MARKERS %d' % (files, total))
