#!/usr/bin/env python3
"""Check RST heading underline widths (CJK=2 cols). Usage: rst_width.py <file>"""
import sys

def w(s):
    return sum(2 if ord(c) > 0x2E7F else 1 for c in s)

path = sys.argv[1]
lines = open(path, encoding='utf-8').read().split('\n')
chars = set('=-^"~+*#')
short = 0
for i in range(1, len(lines)):
    ul = lines[i]
    if len(ul) >= 3 and len(set(ul)) == 1 and ul[0] in chars and not ul.strip() == '':
        t = lines[i - 1]
        if t.strip() == '' or len(t) > 3 and len(set(t)) == 1 and t[0] in chars:
            continue
        u, tw = len(ul), w(t)
        st = 'OK' if u >= tw else 'SHORT'
        if st == 'SHORT':
            short += 1
        print(f'{i} {ul[0]} ulen={u} twidth={tw} delta={u - tw:+d} {st}')
print(f'SHORT count: {short}')
