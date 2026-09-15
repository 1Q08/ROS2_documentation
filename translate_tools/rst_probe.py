#!/usr/bin/env python3
"""docutils AST probe for a concrete translated line.

Usage:
  python3 translate_tools/rst_probe.py <rel>:<lineno> [...] [--fix]
  python3 translate_tools/rst_probe.py --str 'text'

Reports, with CJK masked:
  * docutils warnings for the line as-is
  * the inline nodes produced (type + text)
  * with --fix: the same for every single-space-insertion variant that the
    adjacency auditor would propose
"""
import io
import re
import sys
import pathlib
import docutils.core
import docutils.nodes
from docutils.utils import punctuation_chars as _pc

ROOT = pathlib.Path('/home/nvidia/ROS2_documentation')
SRC = ROOT / 'source'

_EDGE = pathlib.Path(__file__).resolve().parent / 'rst_marker_edge.py'
_src = _EDGE.read_text(encoding='utf-8')
_src = _src.split("root = pathlib.Path(")[0]
_ns = {'__name__': 'edge_lib'}
exec(compile(_src, str(_EDGE), 'exec'), _ns)
scan_line = _ns['scan_line']


def mask(s):
    return ''.join('C' if ord(c) > 127 else c for c in s)


def parse_one(text):
    warn = io.StringIO()
    try:
        doc = docutils.core.publish_doctree(
            text, settings_overrides={'report_level': 2, 'halt_level': 6,
                                      'warning_stream': warn,
                                      'default_role': 'title-reference',
                                      'input_encoding': 'unicode'})
    except Exception as exc:  # pragma: no cover
        return ['EXC %s' % exc], ''
    out = []
    for n in doc.findall():
        if isinstance(n, docutils.nodes.Text):
            continue
        out.append('%s=%s' % (type(n).__name__, mask(n.astext())))
    return out, mask(warn.getvalue().strip())


def show(label, text):
    nodes, warn = parse_one(text)
    print('  [%s] %s' % (label, mask(text)))
    print('      nodes: %s' % (', '.join(nodes) if nodes else '(none)'))
    if warn:
        print('      WARN : %s' % ' | '.join(warn.split('\n')))


args = [a for a in sys.argv[1:] if not a.startswith('--')]
do_fix = '--fix' in sys.argv

if sys.argv[1] == '--str':
    show('str', sys.argv[2])
    sys.exit(0)

for arg in args:
    rel, lineno = arg.rsplit(':', 1)
    lineno = int(lineno)
    lines = (SRC / rel).read_text(encoding='utf-8').split('\n')
    line = lines[lineno - 1]
    print('%s:%d' % (mask(rel), lineno))
    show('as-is', line)
    if do_fix:
        for ln, side, kind, raw, off in scan_line(line, lineno):
            fixed = line[:off] + ' ' + line[off:]
            show('fix %s-%s off=%d' % (kind, side, off), fixed)
