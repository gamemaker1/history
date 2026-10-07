#!/usr/bin/env python3
"""Find what each 1961 village survey says about the number of households in the village.

Searches each village volume for a number followed by "households" (or
"families", "houses") and writes every match with its page and sentence to
analysis/household_candidates.csv. The total used in the analysis is then
chosen by reading the candidates against the page, and recorded with page and
words in data/village_households.csv (computational-analysis.md, A15). The
rule: prefer the households covered by the survey's own tables (the
population the livestock table counts), and say so where the survey gives
two figures (local households and all households, say).

Usage (from the project folder):
  python3 scripts/households.py

Standard library only.
"""

import csv
import re

from corpus import ANALYSIS, ROOT, VILLAGES, pages, text_path

COUNT = re.compile(r"[^.\n]{0,160}?\b(\d{1,4})\s+(?:local\s+)?(?:households|house-holds|families|houses)\b[^.\n]{0,120}",
                   re.IGNORECASE)
TOTAL = re.compile(r"total|village|consists|comprises|in all|there are|inhabited|population|resid", re.IGNORECASE)


def main():
    rows = []
    for village in VILLAGES:
        for n, page in enumerate(pages(text_path(village)), 1):
            text = re.sub(r"(\w)-\n(\w)", r"\1\2", page)
            for m in COUNT.finditer(text):
                sentence = " ".join(m.group(0).split())
                if TOTAL.search(sentence):
                    rows.append({"village": village, "pdf_page": n, "number": int(m.group(1)), "sentence": sentence})
    out = ANALYSIS / "household_candidates.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["village", "pdf_page", "number", "sentence"])
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} candidate statements written to {out.relative_to(ROOT)}")
    for v in VILLAGES:
        nums = {}
        for r in rows:
            if r["village"] == v:
                nums[r["number"]] = nums.get(r["number"], 0) + 1
        top = sorted(nums.items(), key=lambda kv: -kv[1])[:5]
        print(f"  {v:11s} " + ", ".join(f"{k} (x{c})" for k, c in top))


if __name__ == "__main__":
    main()
