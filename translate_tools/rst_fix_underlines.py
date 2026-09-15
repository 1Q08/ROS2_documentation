#!/usr/bin/env python3
"""Normalize RST heading rules to exactly match title display width (CJK=2).

Overline titles ("rule / title / rule") are normalized as a whole.  Fixing
only the underline leaves the overline disagreeing with it, which docutils
reports as "Title overline & underline mismatch" (a hard error under -W).

Usage: python3 translate_tools/rst_fix_underlines.py <file> [--apply]
Skips lines inside literal/code blocks.
"""
import sys, re

def w(s):
    return sum(2 if ord(c) > 0x2E7F else 1 for c in s)

path = sys.argv[1]
apply = '--apply' in sys.argv
lines = open(path, encoding='utf-8').read().split('\n')
n = len(lines)

# mark code/literal block line indices (0-based)
code = set()
i = 0
while i < n:
    s = lines[i].strip()
    iscode = s.startswith('.. code-block::') or s.startswith('.. code::') or s.startswith('.. parsed-literal::')
    islit = lines[i].rstrip().endswith('::') and not lines[i].startswith((' ', '\t'))
    if iscode or islit:
        j = i + 1
        opt = 0
        while j < n and lines[j].strip() == '':
            j += 1
        # skip directive options
        if iscode:
            while j < n and re.match(r'\s+:\w', lines[j]):
                j += 1
            while j < n and lines[j].strip() == '':
                j += 1
        if j < n and lines[j].startswith((' ', '\t')):
            ind = len(lines[j]) - len(lines[j].lstrip())
            while j < n:
                if lines[j].strip() == '':
                    j += 1
                    continue
                if lines[j].startswith((' ', '\t')) and (len(lines[j]) - len(lines[j].lstrip())) >= ind:
                    code.add(j)
                    j += 1
                else:
                    break
        i = j
    else:
        i += 1

chars = set('=-^"~+*#')


def is_rule(s):
    """True for a heading adornment line: >=3 copies of one punctuation char."""
    return len(s) >= 3 and len(set(s)) == 1 and s[0] in chars


changed = []
handled = set()

# 1) overline titles: "rule / title / rule" -> normalize BOTH rules together
#    (docutils requires overline and underline to agree on the title width).
for k in range(0, n - 2):
    if k in code or (k + 1) in code or (k + 2) in code:
        continue
    if not is_rule(lines[k]) or not is_rule(lines[k + 2]):
        continue
    # an overline title uses ONE adornment char for both rules; differing chars
    # mean this is just two adjacent underline titles, not an overline title
    if lines[k][0] != lines[k + 2][0]:
        continue
    t = lines[k + 1]
    if t.strip() == '' or t.startswith((' ', '\t')) or is_rule(t):
        continue
    want = w(t)
    for idx in (k, k + 2):
        if len(lines[idx]) != want:
            changed.append((idx + 1, t, len(lines[idx]), want))
            if apply:
                lines[idx] = lines[idx][0] * want
    handled.update((k, k + 1, k + 2))

# 2) plain underline titles
for i in range(1, n):
    if i in code or (i - 1) in code:
        continue
    if i in handled or (i - 1) in handled:
        continue
    ul = lines[i]
    if not is_rule(ul):
        continue
    t = lines[i - 1]
    if t.strip() == '' or t.startswith((' ', '\t')):
        continue
    if is_rule(t):
        continue
    want = w(t)
    if len(ul) != want:
        changed.append((i + 1, t, len(ul), want))
        if apply:
            lines[i] = ul[0] * want

for ln, t, old, new in changed:
    print(f'line {ln}: ulen {old} -> {new}')
print(f'{"Would change" if not apply else "Changed"}: {len(changed)}')
if apply and changed:
    open(path, 'w', encoding='utf-8').write('\n'.join(lines))
