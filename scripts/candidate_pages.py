#!/usr/bin/env python3
"""Score every page of the 1961 volumes by herding vocabulary and pick the pages to extract claims from.

Reads the 1961 text in text/ and writes analysis/candidate_pages.csv, one row
per PDF page, with the hits for each herding term group (the groups in
kwic.py), a score and a `selected` flag. scripts/extract_claims.py reads the
selected pages.

A page is selected when any of three rules holds:
  1. at least --min-hits matches across at least --min-groups term groups;
  2. rights, dues, the forest or debt together with flocks or pasture, which
     keeps short passages on fees and permits that a pure count would miss;
  3. at least --dense hits in a single group, which keeps pages given over to
     one topic, such as debt or the wool trade.

Recall is checked against the pages cited in the idea files (see
computational-analysis.md). Pages whose only evidence is a printed table
are often missed, because table OCR is garbled. Those figures are read from
the page images into data/flocks.csv instead.

With --colonial the same scoring runs over the 1881 Results, Rose's Glossary
(three volumes) and the 1931 Report, which cover the whole Punjab. There a
page must also mention the hills (HILLS below: Gaddi, Kangra, Chamba, Lahul,
Kinnaur, the Simla hill states ...) at least twice, so that plains pastoralism
is left out. Output: analysis/candidate_pages_colonial.csv.

Usage (from the project folder):
  python3 scripts/candidate_pages.py                    # all 24 village volumes and the 1961 reports
  python3 scripts/candidate_pages.py --colonial         # 1881, Rose and 1931
  python3 scripts/candidate_pages.py --min-hits 8       # stricter

Standard library only. Distant reading to pick pages for close reading.
"""

import argparse
import csv
import re

from corpus import ANALYSIS, COLONIAL, DATA, REPORTS_1961, STUDY_VILLAGES, VILLAGES, load, source_text
from kwic import TERM_SETS

TERMS = TERM_SETS["herding"]
COMPILED = {k: re.compile(r"\b(?:%s)\b" % v, re.IGNORECASE) for k, v in TERMS.items()}
CRITICAL = ["rights_dues", "forest_state", "debt"]
CORE = ["flocks", "pasture", "shepherds"]
HILLS = re.compile(r"\b(?:gadd?is?|gadi|kangra|chamba|brahmaur|barmor|bharmour|lahu?l|spiti|pangi|kul[lu]u|kunawar|kanaw\w*|"
                   r"kinnaur\w*|bashahr|bushahr|rampur|simla|hill states?|dhaula ?dhar|mandi|suket|kanets?|"
                   r"gujars? of the hills|hill gujars?|himalaya\w*)\b", re.IGNORECASE)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--min-hits", type=int, default=6, help="matches needed on a page")
    ap.add_argument("--min-groups", type=int, default=3, help="distinct term groups needed on a page")
    ap.add_argument("--dense", type=int, default=8, help="hits in one group that select a page on their own")
    ap.add_argument("--colonial", action="store_true", help="score the 1881, Rose and 1931 texts instead")
    args = ap.parse_args()

    ANALYSIS.mkdir(exist_ok=True)
    rows = []
    if args.colonial:
        sources = [(n, "colonial") for n in COLONIAL if n != "1931 Tables"]
    else:
        sources = [(n, "village") for n in VILLAGES] + [(n, "report") for n in REPORTS_1961]
    for name, kind in sources:
        text, _ = load(source_text(name))
        for n, page in enumerate(text.split("\f"), 1):
            words = len(page.split())
            if not words:
                continue
            hits = {k: len(rx.findall(page)) for k, rx in COMPILED.items()}
            total = sum(hits.values())
            groups = sum(1 for v in hits.values() if v)
            critical = any(hits[k] for k in CRITICAL) and any(hits[k] for k in CORE)
            dense = max(hits.values()) >= args.dense
            selected = (total >= args.min_hits and groups >= args.min_groups) or critical or dense
            hills = len(HILLS.findall(page))
            if args.colonial:
                selected = selected and hills >= 2
            rows.append({
                "source": name,
                "kind": kind,
                "study_village": name in STUDY_VILLAGES,
                "page": n,
                "words": words,
                **{f"{k}_n": v for k, v in hits.items()},
                "hits": total,
                "hill_terms": hills,
                "groups": groups,
                "score": round(total * groups / max(words, 1) * 100, 2),
                "selected": selected,
            })

    out = ANALYSIS / ("candidate_pages_colonial.csv" if args.colonial else "candidate_pages.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    chosen = [r for r in rows if r["selected"]]
    print(f"{len(rows)} pages scored, {len(chosen)} selected, written to {out.relative_to(ANALYSIS.parent)}")
    by_source = {}
    for r in chosen:
        by_source[r["source"]] = by_source.get(r["source"], 0) + 1
    for name, _ in sources:
        print(f"  {name:12s} {by_source.get(name, 0):4d}")

    # Recall against the pages the idea files cite (data/cited_pages.csv).
    with open(DATA / "cited_pages.csv", encoding="utf-8") as f:
        scored = {name for name, _ in sources}
        cited = [(r["source"], int(r["page"]), r["cited_for"]) for r in csv.DictReader(f) if r["source"] in scored]
    picked = {(r["source"], r["page"]) for r in chosen}
    missed = [c for c in cited if (c[0], c[1]) not in picked]
    print(f"recall on cited pages: {len(cited) - len(missed)} of {len(cited)}")
    for source, page, why in missed:
        print(f"  missed {source} p. {page}: {why}")


if __name__ == "__main__":
    main()
