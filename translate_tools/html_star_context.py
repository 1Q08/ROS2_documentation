#!/usr/bin/env python3
"""Show masked context around literal '*'/'**' markers in built HTML."""
import re
import sys
import pathlib

# 默认构建目录 = 本脚本所在目录(translate_tools/)上一级的 build/html，不写死绝对路径
DEFAULT_ROOT = pathlib.Path(__file__).resolve().parent.parent / 'build' / 'html'
root = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_ROOT
for p in sorted(root.rglob('*.html')):
    html = p.read_text(encoding='utf-8', errors='replace')
    html = re.sub(r'<(pre|code|script|style|tt)\b.*?</\1>', ' ', html, flags=re.S | re.I)
    text = re.sub(r'<[^>]+>', ' ', html)
    hits = [m.start() for m in re.finditer(r'\*\*|(?<!\*)\*(?!\*)', text)]
    if not hits:
        continue
    print('#### %s (%d)' % (p.relative_to(root), len(hits)))
    shown = 0
    for h in hits:
        snip = text[max(0, h - 55):h + 45]
        snip = re.sub(r'\s+', ' ', snip)
        print('   ...%s...' % re.sub(r'[^\x00-\x7f]', 'C', snip))
        shown += 1
        if shown >= 4:
            break
