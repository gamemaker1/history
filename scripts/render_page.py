#!/usr/bin/env python3
"""Render PDF pages to PNG, for reading tables and checking claims against the page image.

Pages are PDF page numbers, as everywhere in this project. Images go to
cache/pages/ (not committed) and the script prints their paths.

Usage (from the project folder):
  .venv/bin/python scripts/render_page.py Brahmaur 54
  .venv/bin/python scripts/render_page.py Newell 37 38 --dpi 200
  .venv/bin/python scripts/render_page.py "text/1931/1931 Part I Report.txt" 142
  .venv/bin/python scripts/render_page.py Nalag 31 --find Sheep --dpi 260   # crop around a table

--find crops the page to a band starting just above the first match of the
word in the page's OCR layer, which makes small table figures easier to read.
If the word is not found, the whole page is rendered.

The source is a citation name (a village such as Kanum, or Newell, Weaving,
Mahasu, Simla) or the path of a text file in text/.

Needs pymupdf (requirements.txt) and the unpacked PDFs (scripts/unpack_sources.py).
"""

import argparse
from pathlib import Path

import pymupdf

from corpus import CACHE, REPORTS_1961, ROOT, VILLAGES, pdf_path, text_path

OUT = CACHE / "pages"


def resolve(source):
    if source in VILLAGES or source in REPORTS_1961:
        return source, pdf_path(text_path(source))
    path = Path(source)
    if not path.is_absolute():
        path = ROOT / path
    return path.stem, pdf_path(path)


def render(source, page_numbers, dpi=150, find=None, band=330):
    """Render pages of a source and return the PNG paths.

    With find, crop to a band of `band` points starting 60 points above the
    first match of `find` on the page."""
    label, pdf = resolve(source)
    if not pdf.exists():
        raise SystemExit(f"{pdf.relative_to(ROOT)} not found. Run scripts/unpack_sources.py first.")
    OUT.mkdir(parents=True, exist_ok=True)
    paths = []
    with pymupdf.open(pdf) as doc:
        for n in page_numbers:
            if n < 1 or n > doc.page_count:
                raise SystemExit(f"page {n} is outside {pdf.name} (1 to {doc.page_count})")
            page = doc[n - 1]
            clip, suffix = None, ""
            hits = page.search_for(find) if find else []
            if hits:
                r = page.rect
                top = max(r.y0, hits[0].y0 - 60)
                clip = pymupdf.Rect(r.x0, top, r.x1, min(r.y1, top + band))
                suffix = f" {find}"
            out = OUT / f"{label} p{n:03d}{suffix}.png"
            page.get_pixmap(dpi=dpi, clip=clip).save(out)
            paths.append(out)
    return paths


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("source", help="citation name (Kanum, Newell ...) or a text file path")
    ap.add_argument("pages", type=int, nargs="+", help="PDF page numbers")
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--find", help="crop to a band around the first match of this word")
    ap.add_argument("--band", type=int, default=330, help="height of the crop in points")
    args = ap.parse_args()
    for p in render(args.source, args.pages, args.dpi, args.find, args.band):
        print(p.relative_to(ROOT))


if __name__ == "__main__":
    main()
