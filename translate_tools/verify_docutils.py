# -*- coding: utf-8 -*-
"""通用 RST 语法验证脚本（docutils），过滤已知噪声。

用法:
    python3 translate_tools/verify_docutils.py <file1.rst> [file2.rst ...]

只输出真实问题（ERROR/SEVERE/WARNING），并过滤掉因禁用
file_insertion_enabled 等产生的无关警告。
"""
import io
import re
import sys

from docutils.core import publish_doctree

NOISE = [
    'Unknown directive type',
    'Unknown interpreted text role',
    'Error in "code-block" directive',
    'Problems with "include"',
    '"include" directive disabled',
    'Unknown target name',
    'Duplicate implicit target name',
    'Hyperlink target',
    'line 0',
    'image file not readable',
    'Explicit markup',
    'document isn\'t included in any toctree',
]

DIAG_RE = re.compile(r'\((?:ERROR|SEVERE|WARNING|INFO)/\d+\)')


def verify(path: str) -> int:
    with open(path, encoding='utf-8') as f:
        content = f.read()

    stream = io.StringIO()
    publish_doctree(content, source_path=path, settings_overrides={
        'report_level': 2,
        'halt_level': 6,
        'warning_stream': stream,
        'file_insertion_enabled': False,
    })
    out = stream.getvalue()
    real = []
    for line in out.splitlines():
        if not DIAG_RE.search(line):
            continue
        if any(n in line for n in NOISE):
            continue
        real.append(line)

    if real:
        print('%s: %d 个真实问题' % (path, len(real)))
        for line in real:
            print('  ' + line)
    else:
        print('%s: 0 个真实问题 (OK)' % path)
    return len(real)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    total = 0
    for path in sys.argv[1:]:
        total += verify(path)
    print('总计真实问题: %d' % total)
    return 0


if __name__ == '__main__':
    sys.exit(main())
