#!/usr/bin/env python3
"""Audit illegal adjacency of inline-markup markers in translated .rst files.

docutils Inliner rules (0.21.x), verified empirically with real CJK literals:

  start-string prefix : line start | whitespace | opener (Ps/Pi) | delimiter
                        (any other punctuation)          -> else marker is
                        *not* recognised (silent literal text, no warning)
  end-string suffix   : line end   | whitespace | closer (Pe/Pf) | delimiter
                        (any other punctuation)          -> else docutils emits
                        "Inline ... start-string without end-string" (fatal
                        under -W), or silently swallows a following literal.

A CJK ideograph is category Lo, i.e. neither whitespace nor punctuation, so a
marker tightened against Chinese text is illegal on that side.

Applies to: ``literal``  :role:`x`  `link`_  `default-role`  *emph*  **strong**

Usage:  python3 translate_tools/rst_marker_edge.py [root] [-v]
"""
import re
import sys
import subprocess
import pathlib
import unicodedata

from docutils.utils import punctuation_chars as _pc

# 仓库根目录 = 本脚本所在目录(translate_tools/)的上一级，不写死绝对路径
ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'source'

# Authoritative docutils inline-markup adjacency rules, taken verbatim from
# docutils/parsers/rst/states.py::Inliner.init_customizations:
#   start_string_prefix = (^|(?<=\s|[openers delimiters]))
#   end_string_suffix   = ($|(?=\s|[\x00 closing_delimiters delimiters closers]))
# `openers`/`closers`/`delimiters` are regex character-class fragments (they
# contain ranges such as \u055a-\u055f), so compile them instead of set()-ing.
START_CLASS = re.compile('[%s%s]' % (_pc.openers, _pc.delimiters))
END_CLASS = re.compile('[%s%s%s]' % (_pc.closing_delimiters, _pc.delimiters,
                                     _pc.closers))


def is_space(ch):
    return ch == '' or ch.isspace()


def pre_ok(ch):
    # A backslash before a marker escapes it, so markup never starts there
    # even though '\\' sits in docutils' delimiter class.
    if ch == '\\':
        return False
    return is_space(ch) or START_CLASS.match(ch) is not None


def post_ok(ch):
    return is_space(ch) or END_CLASS.match(ch) is not None


ROLE = re.compile(r':[a-zA-Z:+_-]+:`[^`\n]*`')
LIT = re.compile(r'``[^`\n]+``')
LINK = re.compile(r'`[^`\n]+`_')
SING = re.compile(r'`[^`\n]+`')
MARK = re.compile(r'(?<!\*)\*\*(?!\s)(?:[^*\n]+?)(?<!\s)\*\*(?!\*)'
                  r'|(?<!\*)\*(?!\*|\s)(?:[^*\n]+?)(?<!\s)\*(?!\*)')


def escaped(line, pos):
    """True if the character at ``pos`` is backslash-escaped.

    ``\\*`` / ``\\```` render as literal characters, so the marker is not
    markup at all and must not be reported.
    """
    n = 0
    k = pos
    while k > 0 and line[k - 1] == '\\':
        n += 1
        k -= 1
    return n % 2 == 1


def backtick_spans(line):
    """Non-overlapping backtick markup spans, longest-first.

    The span extends over a following run of ``_`` so that the anonymous /
    named hyperlink target suffix (``_``, ``__``) counts as part of the
    construct; otherwise every `` `text <url>`__ `` looks like a literal whose
    follower ``_`` is illegal, which is pure scanner noise.
    """
    cand = []
    for pat in (ROLE, LIT, LINK, SING):
        for m in pat.finditer(line):
            if escaped(line, m.start()) or escaped(line, m.end() - 1):
                continue
            cand.append((m.start(), m.end()))
    cand.sort(key=lambda s: (s[0], -s[1]))
    out, last = [], -1
    for s, e in cand:
        while e < len(line) and line[e] == '_':
            e += 1
        if s >= last:
            out.append((s, e))
            last = e
    return out


def em_spans(line):
    """Emphasis/strong spans on the raw line (backticks included).

    docutils does not parse inline markup inside emphasis/strong: the content
    of ``*...*`` / ``**...**`` is taken as plain text (verified with
    docutils.core.publish_parts: ``*a ``b`` c*`` renders
    ``<em>a ``b`` c</em>`` with visible backticks).  A literal or role sitting
    inside such a span is therefore never markup, and its neighbour comes from
    the upstream English text, not from the translation.
    """
    out = []
    for m in MARK.finditer(line):
        if escaped(line, m.start()) or escaped(line, m.end() - 1):
            continue
        out.append((m.start(), m.end()))
    return out


def scan_line(line, i, rel=None, skip_head=False):
    """Return list of (line_no, side, kind, masked_line, insert_offset).

    ``insert_offset`` is the position at which a space must be inserted to
    legalise the adjacency ('pre' -> span start, 'post' -> span end).
    """
    spans = backtick_spans(line)
    nested = em_spans(line)
    hits = []
    for s, e in spans:
        if any(a < s and e <= b for a, b in nested):
            continue
        pre = line[s - 1] if s else ''
        post = line[e] if e < len(line) else ''
        if pre != '`' and not pre_ok(pre):
            hits.append((i, 'pre', 'literal', line, s))
        if post not in ('`', '_') and not post_ok(post):
            hits.append((i, 'post', 'literal', line, e))
    masked = line
    for s, e in reversed(spans):
        masked = masked[:s] + ' ' * (e - s) + masked[e:]
    for m in MARK.finditer(masked):
        if escaped(masked, m.start()) or escaped(masked, m.end() - 1):
            continue
        if '|' in line[m.start():m.end()]:
            continue          # cross-cell span in a grid table: literal '*'
        pre = masked[m.start() - 1] if m.start() else ''
        post = masked[m.end()] if m.end() < len(masked) else ''
        if pre != '*' and not pre_ok(pre):
            hits.append((i, 'pre', 'marker', line, m.start()))
        if post != '*' and not post_ok(post):
            hits.append((i, 'post', 'marker', line, m.end()))
    return hits


def walk(text):
    """Yield (lineno, line) for prose lines, skipping code/directive bodies."""
    inblock, base = False, None
    for i, line in enumerate(text.split('\n'), 1):
        if inblock:
            if line.strip() == '' or (len(line) - len(line.lstrip())) >= base:
                continue
            inblock = False
        if re.search(r'(?<!:):\s*$', line) or re.match(
                r'\s*\.\. (code-block|literalinclude|parsed-literal|code)::',
                line):
            base = len(line) - len(line.lstrip()) + 1
            inblock = True
            continue
        if re.match(r'\s*\.\. ', line):
            continue
        yield i, line


def git_show(rel):
    r = subprocess.run(['git', 'show', 'HEAD:source/' + rel],
                       cwd=ROOT, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def norm(line):
    return re.sub(r'\s+', '', line)


root = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else SRC
verbose = '-v' in sys.argv

tot = {'literal-pre': 0, 'literal-post': 0, 'marker-pre': 0, 'marker-post': 0}
inh = dict(tot)
wt_only = dict(tot)
files, inh_files, wt_files = set(), set(), set()

for p in sorted(root.rglob('*.rst')):
    if p.name.endswith('-Complete-Changelog.rst'):
        continue
    rel = str(p.relative_to(SRC))
    text = p.read_text(encoding='utf-8')
    head = git_show(rel)
    head_lines = head.split('\n') if head is not None else None
    for i, line in walk(text):
        for ln, side, kind, raw, off in scan_line(line, i, rel, False):
            key = '%s-%s' % (kind, side)
            tot[key] += 1
            files.add(rel)
            is_inh = (head_lines is not None and i <= len(head_lines)
                      and norm(head_lines[i - 1]) == norm(raw))
            if is_inh:
                inh[key] += 1
                inh_files.add(rel)
            else:
                wt_only[key] += 1
                wt_files.add(rel)
            if verbose:
                tag = 'INH' if is_inh else 'WT '
                print('%s L%-4d %-13s %s  %s' % (
                    tag, ln, key,
                    re.sub(r'[^\x00-\x7f]', 'C', rel),
                    re.sub(r'[^\x00-\x7f]', 'C', raw.strip())[:100]))

print('TOTAL   ' + '  '.join('%s=%d' % (k, tot[k]) for k in sorted(tot)))
print('HEAD-dup' + '  '.join('%s=%d' % (k, inh[k]) for k in sorted(inh)))
print('WT-ONLY ' + '  '.join('%s=%d' % (k, wt_only[k]) for k in sorted(wt_only)))
print('FILES total=%d inherited-only=%d wt=%d'
      % (len(files), len(inh_files), len(wt_files)))
