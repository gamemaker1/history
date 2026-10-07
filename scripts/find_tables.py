#!/usr/bin/env python3
"""Find the livestock table pages in each 1961 village survey and render them for reading.

Every village survey prints a table of livestock by caste or community, but
the OCR of tables is scrambled, so the figures have to be read from the page
image. This script scores each page of each village volume for "livestock
table": livestock words (sheep, goats, cattle, buffaloes, livestock ...)
together with a high density of numbers. It writes the best pages per village
to analysis/table_pages.csv and, with --render, renders them to cache/pages/.

The figures read from those images go into data/flocks.csv (see
computational-analysis.md, entry A9).

Usage (from the project folder):
  python3 scripts/find_tables.py                  # list candidate pages
  .venv/bin/python scripts/find_tables.py --render --top 2

Rendering needs pymupdf (requirements.txt).
"""

import argparse
import csv
import re

from corpus import ANALYSIS, ROOT, VILLAGES, pages, text_path

ANIMALS = re.compile(r"\b(?:sheep|goats?|cattle|buffal\w+|livestock|bullocks?|cows?|mules?|horses?|ponies|yaks?|"
                     r"churu|zo|donkeys?|poultry)\b", re.IGNORECASE)
HEADING = re.compile(r"livestock|live-stock|animal husbandry|cattle wealth", re.IGNORECASE)
NUMBER = re.compile(r"\b\d[\d,]*\b")


def score(page):
    words = max(len(page.split()), 1)
    animals = len(ANIMALS.findall(page))
    numbers = len(NUMBER.findall(page))
    heading = bool(HEADING.search(page))
    # A table page has both: many animal words and many numbers relative to its length.
    return animals * (numbers / words) * (2 if heading else 1), animals, numbers, heading


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--top", type=int, default=3, help="pages to keep per village")
    ap.add_argument("--render", action="store_true", help="render the kept pages to cache/pages/")
    ap.add_argument("--dpi", type=int, default=130)
    args = ap.parse_args()

    rows = []
    for village in VILLAGES:
        scored = []
        for n, page in enumerate(pages(text_path(village)), 1):
            s, animals, numbers, heading = score(page)
            if animals >= 3:
                scored.append((s, n, animals, numbers, heading))
        scored.sort(reverse=True)
        for rank, (s, n, animals, numbers, heading) in enumerate(scored[:args.top], 1):
            rows.append({"village": village, "rank": rank, "pdf_page": n, "score": round(s, 2),
                         "animal_words": animals, "numbers": numbers, "livestock_heading": heading})

    ANALYSIS.mkdir(exist_ok=True)
    out = ANALYSIS / "table_pages.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} candidate pages for {len(VILLAGES)} villages written to {out.relative_to(ROOT)}")
    for v in VILLAGES:
        print(f"  {v:12s} " + ", ".join(f"p. {r['pdf_page']}" for r in rows if r["village"] == v))

    if args.render:
        from render_page import render
        for v in VILLAGES:
            render(v, [r["pdf_page"] for r in rows if r["village"] == v], args.dpi)
        print("rendered to cache/pages/")


if __name__ == "__main__":
    main()
