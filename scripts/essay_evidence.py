#!/usr/bin/env python3
"""Pull the evidence for each section of the essay out of the knowledge graph.

The essay is written from the graph, not from memory: every quotation and
page it cites should be a claim (an edge) in analysis/graph/edges.csv, or a
figure read from a page image (data/flocks.csv, data/fee_flocks.csv) or an
analysis output. This script runs one graph query per section of the essay
and writes the matching claims, best evidence first, to analysis/essay/:

  evidence_<section>.csv   claim id, subject, predicate, object, quantity, months,
                           place, valley, conjuncture, source, PDF page, year of the
                           source, evidence level, AI verdict and the quote

Evidence order: signed off by a person, then supported by the AI checker,
then image-read, then partly supported. Claims the checker found not
supported are never used.

check_essay.py then confirms that every page the essay cites holds a graph
claim (or an image-read table) and that every quotation is on its page.

Usage (from the project folder):
  .venv/bin/python scripts/essay_evidence.py
  .venv/bin/python scripts/essay_evidence.py --show 12     # print more claims per section

Needs pandas.
"""

import argparse

import pandas as pd

from corpus import ANALYSIS, ROOT

GRAPH = ANALYSIS / "graph"
OUT = ANALYSIS / "essay"
RANK = {"human": 0, "ai_checked": 1, "image_unverified": 2, "ai_partly": 3, "auto": 4}
GADDI = {"gaddi", "malundi", "pohal", "shepherd", "brahman", "rajput", "sipi", "households"}


def load():
    e = pd.read_csv(GRAPH / "edges.csv", dtype=str).fillna("")
    n = pd.read_csv(GRAPH / "nodes.csv", dtype=str).fillna("")
    base = dict(zip(n.label, n.base_id))
    e["subject_id"] = e.subject.map(lambda x: base.get(x, x))
    e["object_id"] = e.object.map(lambda x: base.get(x, x))
    e["rank"] = e.evidence.map(RANK).fillna(9)
    e = e[e.evidence != "ai_rejected"]
    return e


def sections(e):
    move = e.predicate.isin(["GRAZES_AT", "MIGRATES_TO", "MOVES_VIA"])
    trade = e.predicate.isin(["CARRIES", "TRADES_AT", "SELLS_TO", "BUYS_FROM"])
    return {
        # 3. The mountain year: the cycle, its months and routes, across the source layers
        "3_cycle_colonial": e[move & (e.layer_year != "1961")],
        "3_cycle_gaddi_1961": e[move & (e.layer_year == "1961") & e.source.isin(["Brahmaur", "Newell", "Chitrari", "Kupha"])],
        "3_cycle_sutlej_1961": e[move & e.source.isin(["Kanum", "Kothi", "Nachar"])],
        "3_cycle_gujjar": e[move & (e.subject_id == "gujjar")],
        "3_low_villages_buy": e[e.predicate.eq("BUYS_FROM") & e.object_id.isin(["gaddi", "kinnaura", "x_gaddis"])
                                | (e.source.isin(["Bir", "Shakrori", "Rajana", "Chauntra"]) & (move | trade))],
        "3_rivers": e[e.predicate.isin(["LOCATED_ON"])],
        # 4. Two valleys: trade, the border, the commons
        "4_trade_sutlej": e[trade & (e.valley == "Sutlej")],
        "4_trade_ravi": e[trade & (e.valley == "Ravi")],
        "4_border_tibet": e[e.object_id.isin(["india_china_dispute", "tibet_trade_end", "tibet", "gartok", "shipki_la"])
                            | e.subject_id.isin(["tibetan_traders"])],
        "4_pastures_rights": e[e.predicate.isin(["HOLDS_RIGHTS_OVER", "CLOSES"])],
        # 5. Who owned the flocks; who herded; debt
        "5_ownership_text": e[e.predicate.eq("OWNS") & e.object.isin(["sheep and goats", "sheep", "goats", "buffaloes"])
                              & ~e.extracted_by.str.startswith("image")],
        "5_shepherds_labour": e[e.predicate.isin(["HIRES", "WORKS_AS"])
                                & (e.object_id.isin(["pohal", "fawal", "grazier", "malundi", "shepherd", "rigri"])
                                   | e.subject_id.isin(["pohal", "fawal", "grazier", "malundi"]))],
        "5_debt": e[e.predicate.eq("LENDS_TO")],
        # 6. Who took the surplus, conjuncture by conjuncture
        "6_two_sovereigns": e[e.conjuncture == "two_sovereigns"],
        "6_princely": e[(e.conjuncture == "princely_pastures") & e.predicate.isin(
            ["COLLECTS_FEE_FROM", "AUCTIONS_RIGHT_TO", "PAYS_DUES_TO", "HOLDS_RIGHTS_OVER", "OWNS"])],
        "6_forest": e[e.conjuncture == "forest_department"],
        "6_roads_wages": e[e.conjuncture == "roads_and_wages"],
        "6_orchards_change": e[e.object_id.isin(["apples", "road_construction", "merger_1948", "sheep_disease"])
                               | e.subject_id.isin(["apples"])],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--show", type=int, default=0, help="print this many claims per section")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    e = load()
    cols = ["claim_id", "subject", "predicate", "object", "resource", "qty", "unit", "months", "place", "valley",
            "conjuncture", "source", "pdf_page", "layer_year", "evidence", "ai_verdict", "quote"]
    total = 0
    for name, df in sections(e).items():
        df = df.sort_values(["rank", "layer_year", "source", "pdf_page"])
        df[cols].to_csv(OUT / f"evidence_{name}.csv", index=False)
        total += len(df)
        print(f"{name:22s} {len(df):4d} claims, {int((df.evidence.isin(['ai_checked', 'human'])).sum()):4d} supported "
              f"or signed off, from {df.source.nunique()} sources")
        for r in df.head(args.show).itertuples():
            q = " ".join(r.quote.split())[:150]
            print(f"    [{r.evidence[:9]}] {r.source} p. {r.pdf_page} ({r.layer_year}): {r.subject} {r.predicate} "
                  f"{r.object} {r.qty} {r.unit} {r.months} | \"{q}\"")
    print(f"{total} claim rows written to {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
