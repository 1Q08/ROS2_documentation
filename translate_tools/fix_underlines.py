# -*- coding: utf-8 -*-
"""通用标题下划线修复脚本。

用法:
    python3 translate_tools/fix_underlines.py <file1.rst> [file2.rst ...]

规则（只改长度不匹配的下划线，其他一律不动）:
  1. 识别整行由同一字符（= - ^ ~ " # * + `）重复组成的下划线行。
  2. 上一行若为空 -> 判定为过渡线(transition)，跳过。
  3. 计算上一行文本的显示宽度（CJK 全角按 2 计）。
  4. 下划线长度 != 显示宽度 时，重新生成下划线（长度 = 显示宽度，
     至少 1 个字符）。相等则跳过。
"""
import re
import sys
import unicodedata

UNDERLINE = re.compile(r'^([=\-^~"#*+`])\1{1,}\s*$')


def disp_width(s: str) -> int:
    return sum(2 if unicodedata.east_asian_width(c) in ('F', 'W') else 1
               for c in s)


def fix(path: str) -> int:
    with open(path, encoding='utf-8') as f:
        lines = f.read().split('\n')

    changed = 0
    for i in range(1, len(lines)):
        m = UNDERLINE.match(lines[i])
        if not m:
            continue
        prev = lines[i - 1]
        if not prev.strip():
            continue  # 上一行为空 -> 过渡线，跳过
        ch = m.group(1)
        w = disp_width(prev.rstrip())
        if w <= 0:
            continue
        cur = len(lines[i].strip())
        if cur == w:
            continue
        lines[i] = ch * w
        changed += 1
        print('  %s:%d  [%s] %d -> %d  | %s'
              % (path, i + 1, ch, cur, w, prev.strip()[:40]))

    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    return changed


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    total = 0
    for path in sys.argv[1:]:
        n = fix(path)
        total += n
        print('%s: 修复 %d 处' % (path, n))
    print('总计修复 %d 处' % total)
    return 0


if __name__ == '__main__':
    sys.exit(main())
