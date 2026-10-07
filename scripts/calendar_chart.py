#!/usr/bin/env python3
"""The mountain year: when the flocks and people are where, by village and source layer.

Reads analysis/graph/edges.csv (build_graph.py) and keeps every claim that
names months: movement (GRAZES_AT, MIGRATES_TO, MOVES_VIA), fairs and markets
(TRADES_AT) and seasonal work (WORKS_AS, HIRES). Each claim's destination is
classed from its entity:

  winter grounds    winter_ground, low hills, plains towns, regions below the range
  summer pastures   pasture, dhar, pass, high pastures, alpine regions
  fairs and markets market, fair
  other             anything else (home village, work)

and drawn as one row of month cells, grouped by river valley and ordered by
source year, so the same route recorded in 1911 and 1961 sits side by side.
That is the Annales test of the plan (sub-question 1): do the months and
routes of 1961 match those of the colonial sources?

Outputs in analysis/calendar/:
  calendar.csv     one row per claim with months, destination class, source and year
  persistence.csv  for each herding group and destination class: the source years that attest it
  calendar.png     the month chart

Usage (from the project folder):
  .venv/bin/python scripts/calendar_chart.py
  .venv/bin/python scripts/calendar_chart.py --evidence ai

Needs pandas and matplotlib.
"""

import argparse

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Patch, Rectangle  # noqa: E402

from corpus import ANALYSIS, DATA, ROOT  # noqa: E402

GRAPH = ANALYSIS / "graph"
OUT = ANALYSIS / "calendar"
PREDICATES = ["GRAZES_AT", "MIGRATES_TO", "MOVES_VIA", "TRADES_AT", "WORKS_AS", "HIRES"]
WINTER_SUB = {"winter_ground", "town", "plains"}
WINTER_IDS = {"low_hills", "kangra", "nurpur", "pathankot", "jammu", "shahpur", "bilaspur", "arki", "sirmur", "suni",
              "karsog", "seoni", "mehlog", "suket", "mandi", "amritsar", "kulu"}
SUMMER_SUB = {"pasture", "pass", "range"}
SUMMER_IDS = {"high_pastures", "lahaul", "pangi", "bara_bangahal", "hangrang", "spiti", "kugti_pass", "rohtang"}
CLASS_COLOUR = {"winter grounds": "#2a78d6", "summer pastures": "#eb6834", "fairs and markets": "#1baf7a",
                "other": "#b8b7b0"}
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
LEVEL = {"ai_rejected": -1, "image_unverified": 0, "auto": 1, "ai_partly": 1, "ai_checked": 2, "human": 3}
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#dcdbd6"
VALLEY_ORDER = ["Ravi", "Sutlej", "Chenab", "Beas", "Yamuna", ""]


def destination_class(object_id, subtype, predicate):
    if predicate == "TRADES_AT" or subtype in ("market",):
        return "fairs and markets"
    if object_id in SUMMER_IDS or subtype in SUMMER_SUB:
        return "summer pastures"
    if object_id in WINTER_IDS or subtype in WINTER_SUB:
        return "winter grounds"
    return "other"


def load(min_evidence):
    e = pd.read_csv(GRAPH / "edges.csv", dtype=str).fillna("")
    n = pd.read_csv(GRAPH / "nodes.csv", dtype=str).fillna("")
    floor = {"all": 0, "auto": 1, "ai": 2, "human": 3}[min_evidence]
    e = e[(e.evidence.map(LEVEL) >= floor) & e.predicate.isin(PREDICATES)]
    base = dict(zip(n.label, n.base_id))
    ents = pd.read_csv(DATA / "entities.csv", dtype=str).fillna("").set_index("id")
    e = e.assign(subject_base=e.subject.map(lambda s: base.get(s, s)),
                 object_base=e.object.map(lambda s: base.get(s, s)))
    e["object_subtype"] = e.object_base.map(ents.subtype).fillna("")
    e["subject_label"] = e.subject_base.map(ents.label).fillna(e.subject)
    e["dest_class"] = [destination_class(o, s, p) for o, s, p in zip(e.object_base, e.object_subtype, e.predicate)]
    e["months_list"] = e.months.str.split("|").map(lambda ms: sorted({int(m) for m in ms if m}))
    e["valley"] = e.valley.where(e.valley != "", "")
    return e


def persistence(e):
    """Which source years attest each herding group's movement to each class of destination.

    This counts every movement claim, with or without month names: Barnes in 1881 says "the
    winter months" and the 1931 Report "spend the winter", which name a season but no month."""
    move = e[e.predicate.isin(["GRAZES_AT", "MIGRATES_TO", "MOVES_VIA"])]
    rows = []
    for (who, cls), g in move.groupby(["subject_label", "dest_class"]):
        months = sorted({m for ms in g.months_list for m in ms})
        rows.append({"group": who, "destination_class": cls,
                     "source_years": ", ".join(sorted(set(g.layer_year))),
                     "years_with_months": ", ".join(sorted(set(g[g.months != ""].layer_year))),
                     "months_named": ", ".join(MONTHS[m - 1] for m in months),
                     "claims": len(g), "sources": "; ".join(sorted(set(g.source + " p. " + g.pdf_page)))})
    return pd.DataFrame(rows).sort_values(["group", "destination_class"])


def plot(e):
    e = e[e.months != ""].copy()
    e["valley_order"] = e.valley.map({v: i for i, v in enumerate(VALLEY_ORDER)}).fillna(len(VALLEY_ORDER))
    e["row"] = (e.place.where(e.place != "", "(general)") + " · " + e.subject_label + " → " + e.object
                + "  [" + e.source + " " + e.layer_year + "]")
    # Movement and fairs only (seasonal work stays in calendar.csv). Claims that give the same row
    # are merged: the row shows every month any of them names.
    e = e[e.predicate.isin(["GRAZES_AT", "MIGRATES_TO", "MOVES_VIA", "TRADES_AT"])]
    merged = e.groupby("row").agg(months_list=("months_list", lambda ms: sorted({m for x in ms for m in x})),
                                  dest_class=("dest_class", "first"), valley=("valley", "first"),
                                  valley_order=("valley_order", "first"), layer_year=("layer_year", "first"),
                                  place=("place", "first"), subject_label=("subject_label", "first"),
                                  object=("object", "first")).reset_index()
    rows = merged.sort_values(["valley_order", "valley", "subject_label", "layer_year", "place", "object"])
    h = 0.26 * len(rows) + 1.6
    fig, ax = plt.subplots(figsize=(10, h), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    labels, valleys = [], []
    for i, r in enumerate(rows.itertuples()):
        y = len(rows) - 1 - i
        for m in r.months_list:
            ax.add_patch(Rectangle((m - 1 + 0.06, y - 0.36), 0.88, 0.72, color=CLASS_COLOUR[r.dest_class], linewidth=0))
        labels.append(r.row)
        valleys.append(r.valley)
    ax.set_xlim(0, 13.4)
    ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.set_xticks([m + 0.5 for m in range(12)])
    ax.set_xticklabels(MONTHS, fontsize=8.5, color=INK2)
    ax.xaxis.tick_top()
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels(labels[::-1], fontsize=7.2, color=INK)
    for x in range(13):
        ax.plot([x, x], [-0.6, len(rows) - 0.4], color=GRID, linewidth=0.5, zorder=0)
    # rules between valleys, with the valley named in the right margin
    prev = None
    for i, v in enumerate(valleys):
        y = len(rows) - 1 - i
        if v != prev:
            if prev is not None:
                ax.plot([0, 13.4], [y + 0.5, y + 0.5], color=INK2, linewidth=0.8)
            ax.text(12.15, y, v or "other or none", fontsize=8.5, color=INK, va="center", fontweight="bold")
        prev = v
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=0)
    ax.legend(handles=[Patch(color=c, label=k) for k, c in CLASS_COLOUR.items()], ncol=4, loc="upper left",
              bbox_to_anchor=(0, -0.01), frameon=False, fontsize=8.5)
    fig.suptitle("The mountain year: months named for each movement, by valley and source year",
                 x=0.01, ha="left", fontsize=11, color=INK)
    fig.text(0.01, 0.003, "Source: claims with named months (analysis/graph/edges.csv). Rows grouped by river valley "
             "(rules), then by the year of the source.", fontsize=7.5, color=INK2)
    fig.tight_layout()
    fig.savefig(OUT / "calendar.png", dpi=200, facecolor=SURFACE)
    plt.close(fig)
    return len(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--evidence", choices=["all", "auto", "ai", "human"], default="all")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    e = load(args.evidence)
    cols = ["valley", "place", "subject_label", "predicate", "object", "dest_class", "months", "when",
            "source", "pdf_page", "layer_year", "evidence", "quote"]
    e[e.months != ""][cols].to_csv(OUT / "calendar.csv", index=False)
    p = persistence(e)
    p.to_csv(OUT / "persistence.csv", index=False)
    n = plot(e)
    m = e[e.months != ""]
    print(f"{len(e)} seasonal claims, {len(m)} with months (evidence: {args.evidence}), {n} rows drawn; "
          f"outputs in {OUT.relative_to(ROOT)}/")
    print("  with months, by destination: " + ", ".join(f"{k} {v}" for k, v in m.dest_class.value_counts().items()))
    print("  all movement claims, by source year: " + ", ".join(
        f"{k} {v}" for k, v in e[e.predicate.isin(['GRAZES_AT', 'MIGRATES_TO', 'MOVES_VIA'])]
        .layer_year.value_counts().sort_index().items()))
    multi = p[p.source_years.str.contains(",")]
    print(f"  groups and destinations attested in more than one source year: {len(multi)}")
    for r in multi.itertuples():
        print(f"    {r.group} → {r.destination_class}: {r.source_years} (months named in {r.years_with_months or 'none'}: "
              f"{r.months_named or '-'})")


if __name__ == "__main__":
    main()
