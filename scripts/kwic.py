#!/usr/bin/env python3
"""Keyword-in-context concordance of herding or labour vocabulary across the source layers.

Reads the extracted text in text/ and writes two files to analysis/:

  kwic_<terms>.csv        one row per match, with 20 words of context either
                          side, the PDF page, and empty `code` and `note`
                          columns for the group to fill in.
  term_rates_<terms>.csv  matches per 10,000 words for each term group, by
                          layer and (for 1961) by village or report.

Usage (from the project folder):
  python3 scripts/kwic.py                      # herding terms, the ten study villages
  python3 scripts/kwic.py --all-villages       # every 1961 village survey
  python3 scripts/kwic.py --terms labour       # the begar and labour terms
  python3 scripts/kwic.py --window 30          # wider context

The 1961 layer also includes the Newell, Weaving, Mahasu and Simla volumes.

Standard library only. Based on the Programming Historian lessons
"Keywords in Context (Using n-grams) with Python" and
"Counting Word Frequencies with Python".
"""

import argparse
import bisect
import csv
import re

from corpus import ANALYSIS, REPORTS_1961, STUDY_VILLAGES, TEXT, VILLAGES, load, source_name, text_path

# Source layers: label, folder, year of the source.
LAYERS = [
    ("1881 Ibbetson", "1881", 1881),
    ("1910 Rose", "rose", 1910),
    ("1931 Census", "1931", 1931),
    ("1961 Survey", "1961", 1961),
]

# Term groups. Each pattern is matched case-insensitively on whole words.
# Spellings cover OCR variants seen in the sources (begár, lamberdar, pasham, etc.).
TERM_SETS = {
    "labour": {
        "begar": r"beg[aá]r\w*|bega-?\s?ris?|bethu|baithu|corv[ée]e|forced\s+labou?r",
        "service_role": r"halbandis?|hal-\s?bandis?|kar[aá]waks?|kirawak|kir[aá]uk|kamas",
        "carrying": r"coolies?|porters?|carr(?:y|ied|ying)\s+loads?|jhampanis?",
        "tenancy": r"tenan(?:t|ts|cy|cies)|batai|occupancy|nautors?|landless\w*",
        "wage_work": r"wages?|daily\s+labou?r\w*|labou?rers?|road\s+construction|road\s+work",
        "authority": r"lamb[ae]rdars?|lumbardars?|zaildars?|wazirs?|raja|rana|ruler",
        "low_caste": r"kol[iy]s?|dagis?|chanals?|chamangs?|harijans?|scheduled\s+castes?",
        "water": r"kuhls?|kuhal|irrigation\s+channels?",
    },
    "herding": {
        # The animals and the people who move them.
        "flocks": r"flocks?|sheep|goats?|buffal(?:o|oes|os)|herds?|herdsm[ae]n",
        "shepherds": r"shepherds?|graziers?|malundis?|pohals?|fawals?|phogalas?",
        # Herding peoples, kept apart so that a Gujjar village does not read as all shepherds.
        "herding_peoples": r"gaddis?|gadd?is|gujj?ars?|kinn?aura?s?|kann?auras?",
        # Where they graze.
        "pasture": r"pastures?|pastoral\w*|dhars?|odhwari|jots?|grazing|graze[sd]?|alpine|meadows?",
        # The seasonal route.
        "season_route": r"winter|summer|migrat\w+|transhuman\w*|passes|kugti|dhauladhar|rohtang|lahu?l|pangi|kangra",
        # Who owns the pasture and what it costs.
        "rights_dues": r"permits?|tirni|grazing\s+(?:fees?|tax|dues|rights?)|right[\s-]?holders?|auction\w*|fees?",
        # The state forest.
        "forest_state": r"forest\s+department|reserved?\s+forests?|protected\s+forests?|forest\s+settlement|erosion|closures?",
        # Trade carried by the flocks.
        "trade": r"tibet\w*|shipki\w*|gartok|lavi|salt|pash[a]?m\w*|wool\w*|chilgoz\w*|barter\w*|caravans?",
        # Credit.
        "debt": r"debts?|indebted\w*|money[\s-]?lenders?|loans?|mortgag\w*|sahukars?|interest",
        # Wage work that competes with herding.
        "wage_work": r"wages?|daily\s+labou?r\w*|labou?rers?|road\s+construction|road\s+work",
    },
}


def files_1961(all_villages):
    names = list(VILLAGES) if all_villages else STUDY_VILLAGES
    return [text_path(n) for n in names] + [text_path(n) for n in REPORTS_1961]


def context(text, start, end, window):
    left = text[max(0, start - window * 12):start].split()[-window:]
    right = text[end:end + window * 12].split()[:window]
    return " ".join(left), " ".join(right)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--terms", choices=sorted(TERM_SETS), default="herding",
                    help="which set of term groups to search for")
    ap.add_argument("--all-villages", action="store_true",
                    help="include every 1961 village survey, not only the ten study villages")
    ap.add_argument("--window", type=int, default=20, help="words of context on each side")
    args = ap.parse_args()

    terms = TERM_SETS[args.terms]
    compiled = {k: re.compile(r"\b(?:%s)\b" % v, re.IGNORECASE) for k, v in terms.items()}

    ANALYSIS.mkdir(exist_ok=True)
    rows, rates = [], []

    for label, folder, year in LAYERS:
        if folder == "1961":
            files = files_1961(args.all_villages)
        else:
            files = sorted((TEXT / folder).glob("*.txt"))

        # 1961 rates are per village or report. The other layers are pooled.
        groups = [(source_name(f), [f]) for f in files] if folder == "1961" else [("", files)]

        for group_name, group_files in groups:
            words = 0
            counts = {k: 0 for k in terms}
            for path in group_files:
                text, newlines = load(path)
                words += len(text.split())
                for group, rx in compiled.items():
                    for m in rx.finditer(text):
                        counts[group] += 1
                        left, right = context(text, m.start(), m.end(), args.window)
                        rows.append({
                            "layer": label,
                            "year": year,
                            "source": path.name,
                            "village": source_name(path) if folder == "1961" else "",
                            "page": text.count("\f", 0, m.start()) + 1,
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
                "village": group_name,
                "words": words,
                **{f"{k}_per_10k": round(v / words * 1e4, 2) if words else 0 for k, v in counts.items()},
                **{f"{k}_n": v for k, v in counts.items()},
            })

    rows.sort(key=lambda r: (r["year"], r["source"], r["line"]))
    for i, r in enumerate(rows, 1):
        r["id"] = i

    kwic_fields = ["id", "layer", "year", "source", "village", "page", "line", "term_group",
                   "match", "left", "right", "code", "note"]
    kwic_out = ANALYSIS / f"kwic_{args.terms}.csv"
    with open(kwic_out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=kwic_fields)
        w.writeheader()
        w.writerows(rows)

    rates_out = ANALYSIS / f"term_rates_{args.terms}.csv"
    with open(rates_out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rates[0].keys()))
        w.writeheader()
        w.writerows(rates)

    print(f"{len(rows)} matches written to {kwic_out.relative_to(ANALYSIS.parent)}")
    print(f"{len(rates)} rows written to {rates_out.relative_to(ANALYSIS.parent)}")


if __name__ == "__main__":
    main()
