#!/usr/bin/env python3
"""Keyword-in-context concordance of labour vocabulary across the source layers.

Reads the extracted text in text/ and writes two files to analysis/:

  kwic.csv        one row per match, with 20 words of context either side and
                  empty `code` and `note` columns for the group to fill in.
  term_rates.csv  matches per 10,000 words for each term group, by layer and
                  (for 1961) by village.

Usage (from the project folder):
  python3 scripts/kwic.py                  # the five study villages only
  python3 scripts/kwic.py --all-villages   # every 1961 village survey
  python3 scripts/kwic.py --window 30      # wider context

Standard library only. Based on the Programming Historian lessons
"Keywords in Context (Using n-grams) with Python" and
"Counting Word Frequencies with Python".
"""

import argparse
import bisect
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT = ROOT / "text"
OUT = ROOT / "analysis"

STUDY_VILLAGES = ["Chergaon", "Chaupal", "Shakrori", "Chaunri", "Kanum"]

# Source layers: label, folder, year of the source.
LAYERS = [
    ("1881 Ibbetson", "1881", 1881),
    ("1910 Rose", "rose", 1910),
    ("1931 Census", "1931", 1931),
    ("1961 Survey", "1961", 1961),
]

# Term groups. Each pattern is matched case-insensitively on whole words.
# Spellings cover OCR variants seen in the sources (begár, lamberdar, etc.).
TERMS = {
    "begar": r"beg[aá]r\w*|bega-?\s?ris?|bethu|baithu|corv[ée]e|forced\s+labou?r",
    "service_role": r"halbandis?|hal-\s?bandis?|kar[aá]waks?|kirawak|kir[aá]uk|kamas",
    "carrying": r"coolies?|porters?|carr(?:y|ied|ying)\s+loads?|jhampanis?",
    "tenancy": r"tenan(?:t|ts|cy|cies)|batai|occupancy|nautors?|landless\w*",
    "wage_work": r"wages?|daily\s+labou?r\w*|labou?rers?|road\s+construction|road\s+work",
    "authority": r"lamb[ae]rdars?|lumbardars?|zaildars?|wazirs?|raja|rana|ruler",
    "low_caste": r"kol[iy]s?|dagis?|chanals?|chamangs?|harijans?|scheduled\s+castes?",
    "water": r"kuhls?|kuhal|irrigation\s+channels?",
}
COMPILED = {k: re.compile(r"\b(?:%s)\b" % v, re.IGNORECASE) for k, v in TERMS.items()}

VILLAGE_RE = re.compile(r"Village Survey \(([A-Za-z]+)")


def village_of(path):
    m = VILLAGE_RE.search(path.name)
    return m.group(1) if m else ""


def load(path):
    """Read a text file and rejoin words hyphenated across line breaks.

    Returns the text and a list of newline offsets for line-number lookup.
    The rejoin keeps the newline so line numbers stay correct.
    """
    raw = path.read_text(encoding="utf-8", errors="ignore")
    text = re.sub(r"(\w)-\n(\w+)", r"\1\2\n", raw)
    newlines = [i for i, c in enumerate(text) if c == "\n"]
    return text, newlines


def context(text, start, end, window):
    left = text[max(0, start - window * 12):start].split()[-window:]
    right = text[end:end + window * 12].split()[:window]
    return " ".join(left), " ".join(right)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--all-villages", action="store_true",
                    help="include every 1961 village survey, not only the five study villages")
    ap.add_argument("--window", type=int, default=20, help="words of context on each side")
    args = ap.parse_args()

    OUT.mkdir(exist_ok=True)
    rows, rates = [], []

    for label, folder, year in LAYERS:
        files = sorted((TEXT / folder).glob("*.txt"))
        if folder == "1961":
            files = [f for f in files if village_of(f)]
            if not args.all_villages:
                files = [f for f in files if village_of(f) in STUDY_VILLAGES]

        # 1961 rates are per village. The other layers are pooled.
        groups = [(village_of(f), [f]) for f in files] if folder == "1961" else [("", files)]

        for village, group_files in groups:
            words = 0
            counts = {k: 0 for k in TERMS}
            for path in group_files:
                text, newlines = load(path)
                words += len(text.split())
                for group, rx in COMPILED.items():
                    for m in rx.finditer(text):
                        counts[group] += 1
                        left, right = context(text, m.start(), m.end(), args.window)
                        rows.append({
                            "layer": label,
                            "year": year,
                            "source": path.name,
                            "village": village_of(path),
                            "line": bisect.bisect_left(newlines, m.start()) + 1,
                            "term_group": group,
                            "match": " ".join(m.group(0).split()),
                            "left": left,
                            "right": right,
                            "code": "",
                            "note": "",
                        })
            rates.append({
                "layer": label,
                "village": village,
                "words": words,
                **{f"{k}_per_10k": round(v / words * 1e4, 2) if words else 0 for k, v in counts.items()},
                **{f"{k}_n": v for k, v in counts.items()},
            })

    rows.sort(key=lambda r: (r["year"], r["source"], r["line"]))
    for i, r in enumerate(rows, 1):
        r["id"] = i

    kwic_fields = ["id", "layer", "year", "source", "village", "line", "term_group",
                   "match", "left", "right", "code", "note"]
    with open(OUT / "kwic.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=kwic_fields)
        w.writeheader()
        w.writerows(rows)

    with open(OUT / "term_rates.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rates[0].keys()))
        w.writeheader()
        w.writerows(rates)

    print(f"{len(rows)} matches written to {OUT / 'kwic.csv'}")
    print(f"{len(rates)} rows written to {OUT / 'term_rates.csv'}")


if __name__ == "__main__":
    main()
