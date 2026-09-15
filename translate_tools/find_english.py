#!/usr/bin/env python3
"""Detect residual English prose lines (no CJK chars, >=3 ascii words)."""
import re
import sys
from pathlib import Path

words = re.compile(r"[A-Za-z][A-Za-z'\-]{2,}")
han = re.compile(r"[\u4e00-\u9fff]")
SKIP_DIRECTIVES = {
    "code-block", "code", "literalinclude", "parsed-literal", "tabs",
    "toctree", "include", "raw", "redirect-from", "sourcecode",
}


def main(paths):
    tot = 0
    for arg in paths:
        p = Path(arg)
        lines = p.read_text(encoding="utf-8").splitlines()
        inblock = False
        bindent = 0
        hits = []
        for i, line in enumerate(lines, 1):
            s = line.strip()
            if inblock:
                if s == "":
                    continue
                ind = len(line) - len(line.lstrip())
                if ind > bindent:
                    continue
                inblock = False
            m = re.match(r"^(\s*)\.\.\s+([a-z\-]+)::", line)
            if m:
                if m.group(2) in SKIP_DIRECTIVES:
                    inblock = True
                    bindent = len(m.group(1))
                continue
            if s.startswith(".."):
                continue
            if s.startswith(("=====", "-----", "^^^^^", "~~~~~", "*****", ".....")):
                continue
            if not s:
                continue
            core = re.sub(r"``[^`]*``", " ", line)
            core = re.sub(r"`[^`]*<[^>]*>`_{1,2}", " ", core)
            core = re.sub(r":(doc|ref|term|numref|class|meth|func|mod|file):`[^`]*`", " ", core)
            core = re.sub(r"https?://\S+", " ", core)
            core = re.sub(r"\{[A-Z_]+\}", " ", core)
            if han.search(core):
                continue
            w = words.findall(core)
            if len(w) >= 3:
                hits.append((i, s))
        if hits:
            tot += len(hits)
            print(f"== {arg} : {len(hits)}")
            for ln, t in hits:
                print(f"   {ln}: {t[:130]}")
    print(f"总计纯英文行: {tot}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        args = sorted(str(x) for x in Path("source/Installation").rglob("*.rst"))
    main(args)
