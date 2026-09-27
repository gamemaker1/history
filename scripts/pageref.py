#!/usr/bin/env python3
"""Find the PDF file and page number for a quote or a line in text/.

The text files in text/ keep one form-feed character per PDF page, so the
page of any match is 1 + the number of form feeds before it. Page numbers are
PDF page numbers (the page counter in a PDF viewer), not the printed page
numbers on the scans.

Usage (from the project folder):
  python3 scripts/pageref.py find "grazing rights belonged to the rajah"
  python3 scripts/pageref.py find "grazing rights" --in Newell
  python3 scripts/pageref.py line "text/1961/1961 Census, Village Survey (Kanum Kinnaur).txt" 5059

`find` ignores case, punctuation, line breaks and words hyphenated across
lines, so a quote copied from the idea files matches the OCR text. `--in` limits the
search to files whose name contains the given text.
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT = ROOT / "text"

ZIP_1961 = "sources/1961 Village surveys + census reports-20260926T175323Z-1-001.zip"
ZIP_1881 = "sources/Punjab 1881, Denzil Ibbetson-20260926T175319Z-1-001.zip"

# Which PDF each text folder came from.
PDF_FOR = {
    "1961": lambda name: f"{name}.pdf (inside {ZIP_1961})",
    "1961_layout": lambda name: f"{name}.pdf (inside {ZIP_1961})",
    "1881": lambda name: f"{name}.pdf (inside {ZIP_1881})",
    "1931": lambda name: {
        "1931 Part I Report": "sources/Census of India 1931, Vol 17 Punjab, Part I Report.pdf",
        "1931 Part II Tables": "sources/Census of India 1931, Vol 17 Punjab, Part II Tables.pdf",
    }[name],
    "rose": lambda name: {
        "Rose Vol1": "sources/2015.69651.Glossary-...-Vol1_text.pdf",
        "Rose Vol2": "sources/2015.69652.Glossary-...-Vol2.pdf",
        "Rose Vol3": "sources/2015.69674.Glossary-...-Vol3_text.pdf",
    }[name],
}

WORD = re.compile(r"[a-z0-9]+")


def pdf_name(path):
    return PDF_FOR[path.parent.name](path.stem)


def normalise(text):
    """Lower-case words with their character offsets, hyphenated breaks rejoined."""
    text = re.sub(r"(\w)-[ \t]*\n[ \t]*(\w)", r"\1\2", text)
    return text, [(m.group(0), m.start()) for m in WORD.finditer(text.lower())]


def find(phrase, only=None):
    target = WORD.findall(phrase.lower())
    if not target:
        sys.exit("phrase has no words")
    hits = []
    folders = ["1961", "1881", "1931", "rose"]  # skip 1961_layout, same pages as 1961
    for folder in folders:
        for path in sorted((TEXT / folder).glob("*.txt")):
            if only and only.lower() not in path.name.lower():
                continue
            text, words = normalise(path.read_text(encoding="utf-8", errors="ignore"))
            tokens = [w for w, _ in words]
            n = len(target)
            for i in range(len(tokens) - n + 1):
                if tokens[i:i + n] == target:
                    offset = words[i][1]
                    page = text.count("\f", 0, offset) + 1
                    hits.append((pdf_name(path), page, str(path.relative_to(ROOT))))
    return hits


def line_to_page(path, line):
    text = Path(path).read_text(encoding="utf-8", errors="ignore")
    lines = text.split("\n")
    if line < 1 or line > len(lines):
        sys.exit(f"line {line} is outside the file (1 to {len(lines)})")
    return "\n".join(lines[:line - 1]).count("\f") + 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("find", help="find the page of a quote")
    f.add_argument("phrase")
    f.add_argument("--in", dest="only", help="only search files whose name contains this")
    l = sub.add_parser("line", help="convert a line number to a page")
    l.add_argument("file")
    l.add_argument("line", type=int)
    args = ap.parse_args()

    if args.cmd == "find":
        hits = find(args.phrase, args.only)
        if not hits:
            print("not found")
        seen = set()
        for pdf, page, txt in hits:
            if (pdf, page) not in seen:
                seen.add((pdf, page))
                print(f"PDF page {page:4d}  {pdf}")
    else:
        path = Path(args.file)
        if not path.is_absolute():
            path = ROOT / path
        page = line_to_page(path, args.line)
        print(f"PDF page {page}  {pdf_name(path)}")


if __name__ == "__main__":
    main()
