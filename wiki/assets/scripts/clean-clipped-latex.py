#!/usr/bin/env python3
r"""Clean LaTeX rendering issues in Obsidian-Web-Clipper-captured Markdown files.

Substance preserved; only rendering syntax inside $$...$$ display-math blocks
is changed. Per AGENTS.md, raw files are substantively immutable but allow
rendering-only fixes; this script implements those fixes deterministically and
idempotently so every cleanup pass is reproducible.

Fixes:
  - \left(\right.   → \left(       (and friends for ), |, {, }, [, ])
  - sim<sp>         → \sim<sp>     (stripped backslash on common operators)
  - log/exp/cos/... + U+2061  →  \log etc.
  - softmax + U+2061           →  \text{softmax}
  - any remaining U+2061 invisible-function-application chars stripped
  - ` ;\text{` → ` \quad\text{` (clipper artifact for inline annotations)
  - $$ ... & ... \\ ... $$ blocks wrapped in `\begin{aligned}...\end{aligned}`
    so MathJax in Obsidian actually renders the alignment

Usage:
  python3 clean-clipped-latex.py path/to/file1.md path/to/file2.md ...
"""
import re
import sys
from pathlib import Path

INVIS = "⁡"  # invisible function-application character

REGEX_REPLACEMENTS = [
    (r"\\left\(\\right\.", r"\\left("),
    (r"\\left\.\\right\)", r"\\right)"),
    (r"\\left\|\\right\.", r"\\mid "),
    (r"\\left\.\\right\|", r"\\right|"),
    (r"\\left\{\\right\.", r"\\left\\{"),
    (r"\\left\.\\right\}", r"\\right\\}"),
    (r"\\left\[\\right\.", r"\\left["),
    (r"\\left\.\\right\]", r"\\right]"),
    (r"(?<![\\a-zA-Z])sim(\s)", r"\\sim\1"),
    (r"\s;\\text\{", r" \\quad\\text{"),
]

FUNC_NAMES = ["log", "exp", "cos", "sin", "tan", "sec", "cot",
              "min", "max", "sup", "inf", "lim", "ln", "arg"]
FUNC_PAT = re.compile(
    r"(?<![\\a-zA-Z])(" + "|".join(FUNC_NAMES) + r")\s*" + INVIS
)
SOFTMAX_PAT = re.compile(r"(?<![\\a-zA-Z])softmax\s*" + INVIS)


def clean_math(body: str) -> str:
    body = FUNC_PAT.sub(r"\\\1 ", body)
    body = SOFTMAX_PAT.sub(r"\\text{softmax}", body)
    body = body.replace(INVIS, "")
    for pat, repl in REGEX_REPLACEMENTS:
        body = re.sub(pat, repl, body)
    return body


def wrap_aligned(body: str) -> str:
    if re.search(r"(?<!\\)&", body) and "\\\\" in body:
        if not any(env in body for env in
                   ["begin{aligned}", "begin{align}", "begin{eqnarray}",
                    "begin{cases}", "begin{matrix}", "begin{array}"]):
            return "\n\\begin{aligned}\n" + body.strip() + "\n\\end{aligned}\n"
    return body


def clean_file(path: Path) -> bool:
    original = path.read_text()

    def fix_display(m: "re.Match[str]") -> str:
        body = m.group(1)
        body = clean_math(body)
        body = wrap_aligned(body)
        return "$$" + body + "$$"

    content = re.sub(r"\$\$(.*?)\$\$", fix_display, original, flags=re.DOTALL)
    if content != original:
        path.write_text(content)
        return True
    return False


def main(argv):
    for arg in argv[1:]:
        p = Path(arg)
        if not p.is_file():
            print(f"skipped (not a file): {p}", file=sys.stderr)
            continue
        changed = clean_file(p)
        print(f"{'cleaned' if changed else 'no change'}: {p}")


if __name__ == "__main__":
    main(sys.argv)
