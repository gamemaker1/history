#!/usr/bin/env python3
"""Convert essay/evidence/evidence.md to essay/evidence/evidence.typ and compile it to PDF.

The converter handles the Markdown that scripts/build_evidence.py writes:
headings, paragraphs, bullet and numbered lists, block quotations (also inside
list items), pipe tables, images with captions, inline code and emphasis. Text
is escaped for Typst markup. The PDF is written next to the Typst file.

Usage (from the project folder):
  .venv/bin/python scripts/build_evidence.py
  .venv/bin/python scripts/evidence_typst.py
"""

import re
import subprocess

from corpus import ROOT

SRC = ROOT / "essay" / "evidence" / "evidence.md"
OUT = ROOT / "essay" / "evidence" / "evidence.typ"

PREAMBLE = r'''#set document(title: "Seasonal Herding in the Himachal Hills, 1881-1961: Evidence")
#set page(paper: "a4", numbering: "1")
#set text(font: "C059", size: 10.5pt, lang: "en")
#set par(justify: true)
#set heading(numbering: none)
#show heading: set text(weight: "bold")
#show heading.where(level: 2): set block(above: 1.6em, below: 0.9em)
#show heading.where(level: 3): set block(above: 1.3em, below: 0.7em)
#show link: set text(fill: rgb("#0064E0"))
#show raw: set text(font: "Nimbus Mono PS", size: 9pt)
#show figure.caption: set text(size: 9pt)
#set table(stroke: none, inset: (x: 4pt, y: 3pt))
#show table: set text(size: 8pt)
#show table: set par(justify: false)

#let snip(body) = block(width: 100%, fill: luma(245), inset: (left: 9pt, rest: 6pt),
  stroke: (left: 1.5pt + luma(150)), above: 0.6em, below: 0.6em, text(size: 9.5pt, body))

#let datatable(cols, header, ..cells) = block(above: 0.5em, below: 1em, table(
  columns: cols,
  table.hline(stroke: 0.6pt),
  ..header.map(h => text(weight: "bold", h)),
  table.hline(stroke: 0.4pt),
  ..cells,
  table.hline(stroke: 0.6pt),
))

#text(size: 17pt, weight: "bold")[Seasonal Herding in the Himachal Hills, 1881-1961: Evidence]

3 November 2026
#v(0.6em)
'''


def esc(s):
    """Escape plain text for Typst markup, keeping inline code and *emphasis*."""
    out, pos = [], 0
    for m in re.finditer(r"`([^`]+)`|\*([^*]+)\*", s):
        out.append(esc_plain(s[pos:m.start()]))
        if m.group(1) is not None:
            out.append("`" + m.group(1) + "`")
        else:
            out.append("#emph[" + esc_plain(m.group(2)) + "]")
        pos = m.end()
    out.append(esc_plain(s[pos:]))
    return "".join(out)


def esc_plain(s):
    s = s.replace("\\", "\\\\")
    for ch in "#$@<>[]_*~=":
        s = s.replace(ch, "\\" + ch)
    s = s.replace("//", "/\\/").replace("--", "-\\-")
    return s


def table(lines):
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in lines]
    header, body = rows[0], rows[2:]
    n = len(header)
    cols = "(" + ", ".join(["auto"] * n) + ",)"
    head = "(" + ", ".join(f"[{esc(h)}]" for h in header) + ",)"
    cells = ", ".join(f"[{esc(c)}]" for r in body for c in (r + [""] * n)[:n])
    return f"#datatable({cols}, {head}, {cells})\n"


def figure(line):
    m = re.match(r"!\[(.*)\]\((.*)\)", line.strip())
    cap, path = m.groups()
    return (f'#figure(image("{path}", width: 100%), caption: [{esc(cap)}], kind: image, '
            f'supplement: none, numbering: none)\n')


def main():
    lines = SRC.read_text(encoding="utf-8").split("\n")
    out, i = [PREAMBLE], 0
    title_skipped = False
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        if s.startswith("# ") and not title_skipped:
            title_skipped = True
            i += 1
            continue
        m = re.match(r"(#{2,3}) (.*)", s)
        if m:
            out.append("=" * (len(m.group(1)) - 1) + " " + esc(m.group(2)) + "\n")
            i += 1
            continue
        if s.startswith("|"):
            block = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                block.append(lines[i])
                i += 1
            out.append(table(block))
            continue
        if s.startswith("!["):
            out.append(figure(s))
            i += 1
            continue
        if s.startswith(">"):
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip()[1:].strip())
                i += 1
            indent = "  " if line.startswith("  ") else ""
            out.append(indent + "#snip[" + esc(" ".join(quote)) + "]\n")
            continue
        m = re.match(r"(- |\d+\. )(.*)", line)
        if m:
            text = [m.group(2)]
            i += 1
            while i < len(lines) and lines[i].startswith("  ") and not lines[i].strip().startswith(">") \
                    and lines[i].strip():
                text.append(lines[i].strip())
                i += 1
            marker = "-" if m.group(1) == "- " else "+"
            out.append(f"{marker} {esc(' '.join(text))}\n")
            continue
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r"(#|\||!\[|>|- |\d+\. )", lines[i].strip()):
            para.append(lines[i].strip())
            i += 1
        out.append(esc(" ".join(para)) + "\n")
    OUT.write_text("\n".join(out), encoding="utf-8")
    subprocess.run(["typst", "compile", "--root", str(ROOT), str(OUT)], check=True)
    print(f"written {OUT.relative_to(ROOT)} and {OUT.with_suffix('.pdf').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
