#!/usr/bin/env python3
"""Insert a single space on illegal inline-markup marker boundaries.

Detection is delegated to ``translate_tools/rst_marker_edge.py::scan_line`` (single source
of truth: escape-aware, ``_``-hyperlink-suffix aware, emphasis-nested-literal
aware, grid-table ``|`` aware), then the *silent* translation defects (a marker
tightened against Chinese text) are repaired by inserting exactly one space on
the illegal side:

    中文**粗体**中文              -> 中文 **粗体** 中文
    中文``代码``中文              -> 中文 ``代码`` 中文
    中文:ref:`标题`中文            -> 中文 :ref:`标题` 中文
    中文``AddressBook.msg``（x）   -> 中文 ``AddressBook.msg`` （x）
    （``x``）中文                  -> （``x``） 中文

Safety rules
  * only translation-introduced hits: a line byte-identical (after whitespace
    normalisation) to its ``git show HEAD:`` counterpart is inherited and is
    never touched;
  * only hits whose offending neighbour character is non-ASCII are repaired
    (the remaining ASCII neighbours are cross-line hyperlink / table artefacts
    already triaged as false positives);
  * offsets are de-duplicated and applied right-to-left, so every insert keeps
    the positions of the later ones valid and the operation is idempotent;
  * ``--verify`` re-parses every affected line as-is and fully fixed with
    docutils and reports a line only as OK when the fix adds real inline markup
    (literal/reference/emphasis/strong/title_reference) without adding a
    warning.

Usage:  python3 translate_tools/rst_fix_markers.py [root]
            [--apply] [--verify] [--codes] [--quiet]
"""
import pathlib
import re
import subprocess
import sys
import tempfile
import unicodedata
import shutil

# 检测逻辑复用同目录的 rst_marker_edge.py（单一事实源），
# 因此工具从仓库检出即可运行，不依赖任何 /tmp 绝对路径
_HERE = pathlib.Path(__file__).resolve().parent
_EDGE = _HERE / 'rst_marker_edge.py'
_src = _EDGE.read_text(encoding='utf-8')
_src = _src.split("root = pathlib.Path(")[0]
_ns = {'__name__': 'edge_lib'}
exec(compile(_src, str(_EDGE), 'exec'), _ns)

ROOT = pathlib.Path('/home/nvidia/ROS2_documentation')
SRC = ROOT / 'source'
BAK = pathlib.Path(tempfile.gettempdir()) / 'rst_bak_markers'
walk = _ns['walk']
scan_line = _ns['scan_line']
norm = _ns['norm']

APPLY = '--apply' in sys.argv
VERIFY = '--verify' in sys.argv
CODES = '--codes' in sys.argv
QUIET = '--quiet' in sys.argv

BULLET = re.compile(r'^\s*[*#+-]\s*$')


def mask(s):
    return re.sub(r'[^\x00-\x7f]', 'C', s)


def describe(ch):
    if ch == '':
        return 'EOL'
    u = 'U+%04X' % ord(ch)
    return '%s/%s/%s' % (mask(ch), u, unicodedata.category(ch))


MARKUP_NODES = ('literal', 'reference', 'emphasis', 'strong', 'title_reference')


def detections(line):
    """Return [(offset, side, kind, neighbour)] for repairable hits."""
    out = []
    for _, side, kind, _l, off in scan_line(line, 1):
        if off == 0:
            continue
        nb = line[off - 1] if side == 'pre' else (line[off] if off < len(line) else '')
        if nb == '' or ord(nb) < 0x80:
            continue                      # cross-line / ASCII artefact
        if nb in ('`', '_'):
            continue                      # scanner artefact
        if BULLET.match(line[:off]):
            continue                      # would turn '* x' into '*  x'
        out.append((off, side, kind, nb))
    return out


def fix_line(line):
    """Return (newline, [(offset, side, kind, neighbour)])."""
    hits = detections(line)
    if not hits:
        return line, []
    # dedupe offsets, apply right-to-left
    offs = sorted({off for off, _, _, _ in hits}, reverse=True)
    new = line
    for off in offs:
        new = new[:off] + ' ' + new[off:]
    return new, hits


# ---------------------------------------------------------------- verify mode
def _nodes(text):
    """Return (inline markup node signatures, non-role warnings) for ``text``.

    Signature = ``ClassName=masked_text``.  Comparing the *text* as well as
    the class matters: a repair can keep the node count identical while
    changing what the node contains (e.g. a reference whose literal link
    text was swallowed and re-appears as the CJK link text), and a
    class-only comparison would misreport that repair as NONEW.
    """
    import io
    from docutils.core import publish_doctree
    from docutils import nodes as dn
    warn = io.StringIO()
    doc = publish_doctree(text, settings_overrides={
        'report_level': 2, 'halt_level': 6, 'warning_stream': warn,
        'default_role': 'title-reference', 'input_encoding': 'unicode'})
    names = ['%s=%s' % (n.__class__.__name__, mask(n.astext()))
             for n in doc.findall() if isinstance(n, dn.Inline)]
    noise = ('Unknown interpreted text role', 'No role entry for',
             'Unknown directive type', 'Unknown target name')
    msgs = [l for l in warn.getvalue().split('\n')
            if l.strip() and not any(k in l for k in noise)]
    return names, msgs


def verify(pairs):
    """Report whether the full-line fix really restores inline markup."""
    ok = True
    for rel, i, line, new in pairs:
        n0, w0 = _nodes(line)
        n1, w1 = _nodes(new)
        added = [n for n in set(n1) if n1.count(n) > n0.count(n)]
        new_warn = [w for w in w1 if w not in w0]
        tag = 'OK'
        if not added:
            tag, ok = 'NONEW', False
        if new_warn:
            tag, ok = 'WARN', False
        if CODES or tag != 'OK':
            print('%-6s %s:%d  +%s%s' % (
                tag, mask(rel), i,
                ','.join(sorted(added)) or '-',
                ('  !! ' + ' | '.join(mask(w[:90]) for w in new_warn))
                if new_warn else ''))
    return ok


def git_lines(rel):
    r = subprocess.run(['git', 'show', 'HEAD:source/' + rel],
                       cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        return None
    return {norm(l) for l in r.stdout.split('\n')}


total_fix = total_inh = 0
changed_files = []
pending = []

root = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else SRC
for p in sorted(root.rglob('*.rst')):
    if p.name.endswith('-Complete-Changelog.rst'):
        continue
    rel = str(p.relative_to(SRC))
    text = p.read_text(encoding='utf-8')
    head = git_lines(rel)
    lines = text.split('\n')
    edits = {}
    for i, line in walk(text):
        if head is not None and norm(line) in head:
            if not QUIET and detections(line):
                total_inh += 1
                if CODES:
                    print('INH %s:%d  %s' % (mask(rel), i, mask(line.strip())[:90]))
            continue
        new, hits = fix_line(line)
        if hits:
            edits[i] = new
            if not QUIET and not VERIFY:
                for off, side, kind, nb in hits:
                    print('%s %s:%d  L%d %s-%s nb=%s' % (
                        'FIX' if APPLY else 'DRY', mask(rel), i, i,
                        kind, side, describe(nb)))
                print('       %s' % mask(line.strip())[:100])
            total_fix += len(hits)
            pending.append((rel, i, line, new))
    if edits:
        changed_files.append(rel)
        if APPLY:
            BAK.mkdir(parents=True, exist_ok=True)
            dst = BAK / rel.replace('/', '__')
            if not dst.exists():
                shutil.copy2(p, dst)
            for i, new in edits.items():
                lines[i - 1] = new
            p.write_text('\n'.join(lines), encoding='utf-8')

if VERIFY:
    print('== VERIFY %d line(s)' % len(pending))
    print('VERIFY %s' % ('ALL-OK' if verify(pending) else 'PROBLEMS'))

print('%-8s INSERTS %d  FILES %d  inherited-skipped %d'
      % ('APPLIED' if APPLY else 'DRY-RUN', total_fix, len(changed_files),
         total_inh))
