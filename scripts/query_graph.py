#!/usr/bin/env python3
"""Named queries on the knowledge graph, and a regression check of figures already cited.

Each query reads analysis/graph/edges.csv and nodes.csv (from build_graph.py)
and writes one CSV to analysis/queries/. The check at the end recomputes
figures that the idea files cite, so a change to the claims, the entities or
the graph code that breaks them is caught at once.

Queries:
  flock_shares     sheep and goats owned per caste in each village, with the
                   share of the village total and animals per owning household
  conjunctures     claims per conjuncture, family and valley
  extraction       every extraction edge: who takes what from whom, by conjuncture
  single_source    claims resting on one source only, by predicate and subject

Usage (from the project folder):
  .venv/bin/python scripts/query_graph.py
  .venv/bin/python scripts/query_graph.py --evidence human   # only signed-off claims

Needs pandas (requirements.txt).
"""

import argparse
import sys

import pandas as pd

from corpus import ANALYSIS, ROOT

GRAPH = ANALYSIS / "graph"
OUT = ANALYSIS / "queries"

# Figures cited in the idea files, recomputed from the graph.
# Kothi: the idea files give 94.9%, from three castes. The page image shows a
# fourth row (Badhi, 11 animals), so the correct share is 94.5%.
EXPECTED = [
    ("Brahmaur: Brahman + Rajput share of sheep and goats (%)", 97.9),
    ("Brahmaur: sheep and goats in the village", 4484),
    ("Brahmaur: sheep and goats per household (all 99)", 45.3),
    ("Kothi: Rajput share of sheep and goats (%)", 94.5),
    ("Kothi: sheep and goats in the village", 2557),
]

LEVEL = {"ai_rejected": -1, "image_unverified": 0, "auto": 1, "ai_partly": 1, "ai_checked": 2, "human": 3}


def load(min_evidence):
    edges = pd.read_csv(GRAPH / "edges.csv", dtype=str).fillna("")
    nodes = pd.read_csv(GRAPH / "nodes.csv", dtype=str).fillna("")
    floor = {"all": 0, "auto": 1, "ai": 2, "human": 3}[min_evidence]
    edges = edges[edges["evidence"].map(LEVEL) >= floor]
    edges["qty_n"] = pd.to_numeric(edges["qty"], errors="coerce")
    return edges, nodes


def flock_shares(edges):
    # Livestock tables only: claims read from the page images (data/flocks.csv). The model's
    # extractions from the same tables' OCR text would count the same animals twice.
    own = edges[(edges.predicate == "OWNS") & (edges.object.isin(["sheep and goats", "sheep", "goats"]))
                & edges.extracted_by.str.startswith("image")]
    own = own[(own.place != "") & own.qty_n.notna()]  # counted ownership only
    pop = edges[(edges.predicate == "HAS_POPULATION") & (edges.unit == "households")
                & edges.extracted_by.str.startswith("image")]
    rows = []
    for (place, subject), grp in own.groupby(["place", "subject"]):
        rows.append({"village": place, "group": subject.replace(f" ({place})", ""),
                     "animals": grp.qty_n.sum(), "sources": "; ".join(sorted(set(grp.source + " p. " + grp.pdf_page)))})
    df = pd.DataFrame(rows)
    df["village_total"] = df.groupby("village").animals.transform("sum")
    df["share_pct"] = (df.animals / df.village_total * 100).round(1)
    hh = {(r.place, r.subject.replace(f" ({r.place})", "")): r.qty_n for r in pop.itertuples()}
    df["households"] = [hh.get((v, g)) for v, g in zip(df.village, df.group)]
    return df.sort_values(["village", "animals"], ascending=[True, False])


def checks(shares, edges):
    got = {}
    b = shares[shares.village == "Brahmaur"]
    k = shares[shares.village == "Kothi"]
    if len(b):
        got[EXPECTED[0][0]] = round(b[b.group.isin(["Brahman", "Rajput"])].animals.sum() / b.animals.sum() * 100, 1)
        got[EXPECTED[1][0]] = int(b.animals.sum())
        households = b.households.sum()
        got[EXPECTED[2][0]] = round(b.animals.sum() / households, 1) if households else None
    if len(k):
        got[EXPECTED[3][0]] = round(k[k.group == "Rajput"].animals.sum() / k.animals.sum() * 100, 1)
        got[EXPECTED[4][0]] = int(k.animals.sum())
    return got


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--evidence", choices=["all", "auto", "ai", "human"], default="all")
    args = ap.parse_args()

    edges, nodes = load(args.evidence)
    OUT.mkdir(parents=True, exist_ok=True)

    shares = flock_shares(edges)
    shares.to_csv(OUT / "flock_shares.csv", index=False)

    conj = edges.groupby(["conjuncture", "family", "valley"]).size().reset_index(name="claims")
    conj.to_csv(OUT / "conjunctures.csv", index=False)

    extraction = edges[edges.family == "extraction"][
        ["conjuncture", "subject", "predicate", "object", "resource", "qty", "unit", "place", "source", "pdf_page", "evidence"]]
    extraction.sort_values(["conjuncture", "place"]).to_csv(OUT / "extraction.csv", index=False)

    key = edges.subject + "|" + edges.predicate + "|" + edges.object
    n_sources = edges.groupby(key).source.nunique()
    single = edges[key.map(n_sources) == 1][["subject", "predicate", "object", "source", "pdf_page"]]
    single.to_csv(OUT / "single_source.csv", index=False)

    print(f"queries on {len(edges)} edges (evidence: {args.evidence}) written to {OUT.relative_to(ROOT)}/")
    print(f"  flock_shares: {len(shares)} rows in {shares.village.nunique()} villages")
    print(f"  extraction: {len(extraction)} edges; single_source: {len(single)} of {len(edges)} claims rest on one source")

    got = checks(shares, edges)
    failed = 0
    print("regression check against figures cited in the idea files:")
    for name, want in EXPECTED:
        have = got.get(name)
        ok = have is not None and abs(float(have) - want) < 0.05
        failed += not ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}: expected {want}, got {have}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
