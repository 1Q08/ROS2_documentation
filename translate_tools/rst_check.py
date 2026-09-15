#!/usr/bin/env python3
"""docutils gate for translated RST: report real errors/warnings only.

Usage:
  python3 translate_tools/rst_check.py <file.rst | dir> [...]
  python3 translate_tools/rst_check.py --all <file.rst | dir> [...]   (print every message)

Sphinx-only constructs are ignored (unknown directive/role, missing
substitution, unresolved targets, long lines, and similar are not shown).
"""
import io
import os
import re
import sys

import docutils.core

IGNORE = (
    "Unknown directive type",
    "Unknown interpreted text role",
    "No directive entry for",
    "No role entry for",
    "Unknown target name",
    "Undefined substitution",
    "Unknown substitution",
    "Trying \"",
    "may not begin with a transition",
    "No role entry",
    "Unknown interpreted text role \"doc\"",
    "citation",
    "Hyperlink target",
    "Duplicate explicit target name",
    "Duplicate implicit target name",
    "Mismatch: both interpreted text role prefix and reference suffix",
    "Mismatch: anonymous hyperlink target and reference",
    "Unknown target name:",
    "Title underline too short",
    "Title overline & underline mismatch",
    "Inconsistent title style",
    "Unexpected section title",
    "Document may not end with a transition",
    "Explicit markup ends without a blank line",
    "Unexpected possible title overline or transition",
    "No newline at end of file",
    "Blank line required after table",
    "Definition list ends without a blank line",
    "directive disabled",
    "unknown option:",  # Sphinx-only options, e.g. :emphasize-lines:, :linenos:
    # INFO/1 only: numbered lists that restart at 2/3/... because each item is
    # followed by its own block. Present in the untranslated English baseline
    # (verified against git 447bca7), so not translation-induced.
    "Enumerated list start value not ordinal-1",
)

MSG_RE = re.compile(r"^(?P<path>[^:]*):(?P<line>\d+): \((?P<level>[^)]*)\) (?P<text>.*)$")


def iter_files(args):
    for arg in args:
        if os.path.isdir(arg):
            for root, _dirs, names in os.walk(arg):
                for n in sorted(names):
                    if n.endswith(".rst"):
                        yield os.path.join(root, n)
        else:
            yield arg


def check(path, show_all):
    stream = io.StringIO()
    src = open(path, encoding="utf-8").read()
    try:
        docutils.core.publish_doctree(
            source=src,
            source_path=path,
            settings_overrides={
                "report_level": 1,
                "halt_level": 5,
                "warning_stream": stream,
                "input_encoding": "utf-8",
                "traceback": True,
                "file_insertion_enabled": False,
                "raw_enabled": False,
                "halt_level": 5,
            },
        )
    except Exception as exc:  # pragma: no cover
        print("%s: FATAL %s" % (path, exc))
        return 1
    # Group each message with its continuation lines so that IGNORE patterns
    # can match text printed on the lines following the "path:line: (LEVEL)" one.
    groups = []  # list of (line_no, full_text)
    for line in stream.getvalue().splitlines():
        m = MSG_RE.match(line)
        if m:
            groups.append([m.group("line"), m.group("text")])
        elif groups and line.strip():
            groups[-1][1] += "\n" + line
    out = []
    for line_no, text in groups:
        if not show_all and any(ig in text for ig in IGNORE):
            continue
        out.append("  %s  %s" % (line_no.rjust(5), text.splitlines()[0]))
    if out:
        print("%s:" % path)
        print("\n".join(out))
        return len(out)
    return 0


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    show_all = "--all" in sys.argv
    total = 0
    files = 0
    for path in iter_files(args):
        files += 1
        total += check(path, show_all)
    print("FILES %d  MESSAGES %d" % (files, total))


if __name__ == "__main__":
    main()
