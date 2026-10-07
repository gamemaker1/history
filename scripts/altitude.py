#!/usr/bin/env python3
"""Find what each 1961 village survey says about the village's altitude.

Searches the first --pages pages of each village volume for a figure in feet
or metres next to a word about height (altitude, elevation, height, above sea,
situated, feet high ...), and writes every match with its page and the
sentence to analysis/altitude_candidates.csv.

The altitude used in the analysis is then chosen by reading those candidates
against the page and is recorded, with the page and the words, in
data/village_altitudes.csv (see computational-analysis.md, A15). The
survey's own statement is preferred over a geocoded point, because it is
what the source says and does not depend on where a geocoder put the village.

Usage (from the project folder):
  python3 scripts/altitude.py
  python3 scripts/altitude.py --pages 60

Standard library only.
"""

import argparse
import csv
import re

from corpus import ANALYSIS, ROOT, VILLAGES, pages, text_path

FIGURE = re.compile(r"[^.\n]{0,200}?\b(\d{1,2}[,.]?\d{3}|\d{3,4})\s*(?:feet|ft\b|ft\.|'|metres|meters|m\b)[^.\n]{0,140}",
                    re.IGNORECASE)
HEIGHT = re.compile(r"altitude|above (?:the )?(?:mean )?sea|elevation|height|situated|feet high|ft\.? high|high flat|"
                    r"located|lies", re.IGNORECASE)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--pages", type=int, default=40, help="pages to search from the start of each volume")
    args = ap.parse_args()
    rows = []
    for village in VILLAGES:
        for n, page in enumerate(pages(text_path(village))[:args.pages], 1):
            text = re.sub(r"(\w)-\n(\w)", r"\1\2", page)
            for m in FIGURE.finditer(text):
                sentence = " ".join(m.group(0).split())
                if HEIGHT.search(sentence):
                    rows.append({"village": village, "pdf_page": n, "figure": m.group(1), "sentence": sentence})
    out = ANALYSIS / "altitude_candidates.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["village", "pdf_page", "figure", "sentence"])
        w.writeheader()
        w.writerows(rows)
    found = {r["village"] for r in rows}
    print(f"{len(rows)} candidate statements in {len(found)} of {len(VILLAGES)} villages, "
          f"written to {out.relative_to(ROOT)}")
    print("  none found: " + ", ".join(v for v in VILLAGES if v not in found))


if __name__ == "__main__":
    main()
