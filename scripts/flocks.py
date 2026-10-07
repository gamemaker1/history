#!/usr/bin/env python3
"""Who owns the flocks: sheep and goats by caste and caste class in the 24 village surveys.

Reads data/flocks.csv (livestock tables read from the page images),
data/caste_classes.csv (landholding, scheduled caste, herding tribe, trading,
other) and data/entities.csv (each village's river system). Writes to
analysis/flocks/:

  checks.csv           row sums against the totals the tables themselves print
  by_group.csv         animals and owning households per caste and village
  village_summary.csv  per village: total, share by caste class, top group
  ownership_shares.png share of sheep and goats by caste class, per village
  flock_size.png       sheep and goats per village, by river system

Usage (from the project folder):
  .venv/bin/python scripts/flocks.py

Needs pandas and matplotlib (requirements.txt). Based on the Programming
Historian lesson "Visualizing Data with Bokeh and Pandas" (pandas part).
"""

import sys

import matplotlib
import matplotlib.ticker
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from corpus import ANALYSIS, DATA, ROOT  # noqa: E402

OUT = ANALYSIS / "flocks"

# Totals printed in the tables (or stated beside them), for checking the reading.
PRINTED = [
    ("Brahmaur", 54, "sheep_and_goats", 4484, "Total row"),
    ("Brahmaur", 54, "hh_owning_flock", 48, "Total row"),
    ("Chergaon", 56, "sheep_and_goats", 143, "Total row"),
    ("Chergaon", 56, "hh_owning_flock", 16, "Total row"),
    ("Moginand", 46, "sheep_and_goats", 160, "Total row"),
    ("Moginand", 46, "hh_owning_flock", 23, "Total row"),
    ("Chauntra", 46, "sheep_and_goats", 41, "Total row; prose: fourteen households possess 41"),
    ("Chauntra", 46, "hh_owning_flock", 14, "Total row"),
    ("Tandi", 96, "sheep", 363, "Total row"),
    ("Tandi", 96, "goats", 21, "Total row"),
    ("Tandi", 96, "hh_owning_sheep", 17, "Total row"),
    ("Shakrori", 76, "sheep", 23, "Total row"),
    ("Shakrori", 76, "goats", 53, "Total row"),
    ("Kupha", 80, "sheep_and_goats", 596, "Text: 596 held by 82 households (Kupha p. 81)"),
    ("Kupha", 80, "hh_owning_flock", 82, "Text, Kupha p. 81"),
]

RIVER_ORDER = ["Ravi", "Sutlej", "Chenab", "Beas", "Yamuna", ""]
CLASS_ORDER = ["landholding", "scheduled caste", "herding tribe", "trading", "other"]
# Categorical slots 1 to 5 of the reference palette, validated for adjacent pairs
# (stacked bars) in light mode; text stays in neutral ink.
CLASS_COLOUR = dict(zip(CLASS_ORDER, ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]))
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#dcdbd6"


def load():
    f = pd.read_csv(DATA / "flocks.csv", dtype=str).fillna("")
    for c in ["households_in_group", "hh_owning_sheep", "sheep", "hh_owning_goats", "goats",
              "hh_owning_flock", "sheep_and_goats"]:
        f[c] = pd.to_numeric(f[c], errors="coerce")
    # Where a table gives sheep and goats separately (or goats only, as in Chaupal), the
    # flock is their sum.
    parts = f[["sheep", "goats"]]
    f["sheep_and_goats"] = f["sheep_and_goats"].fillna(parts.sum(axis=1, min_count=1))
    classes = pd.read_csv(DATA / "caste_classes.csv", dtype=str).set_index("group")["class"]
    f["class"] = f["group"].map(classes).fillna("")
    ents = pd.read_csv(DATA / "entities.csv", dtype=str).fillna("")
    rivers = ents[ents.subtype == "village"].set_index("label")["river_system"]
    f["river_system"] = f["village"].map(rivers).fillna("")
    # Owning households where the table gives sheep and goats separately: the larger of the two
    # is a lower bound on households owning either.
    sep = f["hh_owning_flock"].isna() & (f["hh_owning_sheep"].notna() | f["hh_owning_goats"].notna())
    f.loc[sep, "hh_owning_flock"] = f.loc[sep, ["hh_owning_sheep", "hh_owning_goats"]].max(axis=1)
    return f


def checks(f):
    rows = []
    for village, page, col, printed, basis in PRINTED:
        v = f[(f.village == village) & (f.group != "all households")]
        got = v[col].sum(min_count=1)
        rows.append({"village": village, "pdf_page": page, "column": col, "printed": printed,
                     "sum_of_rows": got, "ok": got == printed, "basis": basis})
    return pd.DataFrame(rows)


def summarise(f):
    tables = f[(f.group != "all households") & f.sheep_and_goats.notna()]
    summary = []
    for village, v in tables.groupby("village"):
        total = v.sheep_and_goats.sum()
        row = {"village": village, "river_system": v.river_system.iloc[0], "pdf_page": v.pdf_page.iloc[0],
               "sheep_and_goats": total, "households_owning": v.hh_owning_flock.sum(min_count=1)}
        for c in CLASS_ORDER:
            row[f"{c}_pct"] = round(v[v["class"] == c].sheep_and_goats.sum() / total * 100, 1) if total else None
        top = v.sort_values("sheep_and_goats", ascending=False).iloc[0]
        row["top_group"] = top.group
        row["top_group_pct"] = round(top.sheep_and_goats / total * 100, 1) if total else None
        row["per_owning_household"] = round(total / row["households_owning"], 1) if row["households_owning"] else None
        summary.append(row)
    totals_only = f[f.group == "all households"]
    for r in totals_only.itertuples():
        summary.append({"village": r.village, "river_system": r.river_system, "pdf_page": r.pdf_page,
                        "sheep_and_goats": r.sheep_and_goats, "households_owning": r.hh_owning_flock,
                        "top_group": "(no caste table)"})
    s = pd.DataFrame(summary)
    s["river_order"] = s.river_system.map({r: i for i, r in enumerate(RIVER_ORDER)})
    return s.sort_values(["river_order", "sheep_and_goats"], ascending=[True, False]).drop(columns="river_order")


def style(ax):
    ax.set_facecolor(SURFACE)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=9, length=0)


def plot_shares(s):
    s = s[s[f"{CLASS_ORDER[0]}_pct"].notna()].iloc[::-1]
    labels = [f"{v}  ({r or 'river system not assigned'})" for v, r in zip(s.village, s.river_system)]
    fig, ax = plt.subplots(figsize=(8.5, 0.34 * len(s) + 1.6), facecolor=SURFACE)
    left = [0.0] * len(s)
    for c in CLASS_ORDER:
        vals = s[f"{c}_pct"].fillna(0).tolist()
        ax.barh(labels, vals, left=left, height=0.62, color=CLASS_COLOUR[c], label=c,
                edgecolor=SURFACE, linewidth=1.5)
        left = [a + b for a, b in zip(left, vals)]
    for i, n in enumerate(s.sheep_and_goats):
        ax.text(101.5, i, f"{int(n):,}", va="center", fontsize=8.5, color=INK2)
    ax.text(101.5, len(s) - 0.3, "animals", fontsize=8, color=INK2, va="bottom")
    style(ax)
    ax.set_xlim(0, 112)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(["0", "25", "50", "75", "100%"])
    ax.xaxis.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    ax.legend(ncol=5, loc="lower left", bbox_to_anchor=(0, 1.0), frameon=False, fontsize=8.5,
              labelcolor=INK, handlelength=1.2)
    ax.set_title("Who owned the sheep and goats in 1961: share by caste class, per village",
                 loc="left", fontsize=11, color=INK, pad=26)
    fig.text(0.01, 0.005, "Source: livestock tables in the 1961 Census village surveys, read from the page images "
             "(data/flocks.csv). Villages ordered by river system, then flock size.", fontsize=7.5, color=INK2)
    fig.tight_layout()
    fig.savefig(OUT / "ownership_shares.png", dpi=200, facecolor=SURFACE)
    plt.close(fig)


def plot_sizes(s):
    s = s[s.sheep_and_goats.notna()].iloc[::-1]
    labels = [f"{v}  ({r or 'river system not assigned'})" for v, r in zip(s.village, s.river_system)]
    fig, ax = plt.subplots(figsize=(7.5, 0.3 * len(s) + 1.2), facecolor=SURFACE)
    ax.hlines(labels, 1, s.sheep_and_goats, color=GRID, linewidth=1)
    ax.plot(s.sheep_and_goats, labels, "o", color="#2a78d6", markersize=6)
    for i, n in enumerate(s.sheep_and_goats):
        ax.text(n * 1.15, i, f"{int(n):,}", va="center", fontsize=8, color=INK2)
    style(ax)
    ax.set_xscale("log")
    ax.set_xlim(1, 20000)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.xaxis.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    ax.set_title("Sheep and goats per village, 1961 (log scale)", loc="left", fontsize=11, color=INK)
    fig.text(0.01, 0.005, "Source: data/flocks.csv. Nachar and Shathla give no figures.", fontsize=7.5, color=INK2)
    fig.tight_layout()
    fig.savefig(OUT / "flock_size.png", dpi=200, facecolor=SURFACE)
    plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    f = load()
    unclassified = sorted(set(f[(f.group != "all households") & (f["class"] == "")].group))
    if unclassified:
        sys.exit(f"groups missing from data/caste_classes.csv: {unclassified}")

    c = checks(f)
    c.to_csv(OUT / "checks.csv", index=False)
    f.to_csv(OUT / "by_group.csv", index=False)
    s = summarise(f)
    s.to_csv(OUT / "village_summary.csv", index=False)
    plot_shares(s)
    plot_sizes(s)

    print(f"{len(f)} rows from {f.village.nunique()} villages; outputs in {OUT.relative_to(ROOT)}/")
    print(f"printed-total checks: {int(c.ok.sum())} of {len(c)} pass")
    for r in c[~c.ok].itertuples():
        print(f"  [FAIL] {r.village} p. {r.pdf_page} {r.column}: printed {r.printed}, rows sum to {r.sum_of_rows}")
    tab = f[(f.group != "all households") & f.sheep_and_goats.notna()]
    pooled = tab.groupby("class").sheep_and_goats.sum()
    print("pooled over the caste tables: " + ", ".join(
        f"{k} {v / pooled.sum() * 100:.1f}%" for k, v in pooled.reindex(CLASS_ORDER).dropna().items())
        + f" of {int(pooled.sum()):,} animals")
    cols = ["village", "river_system", "sheep_and_goats", "landholding_pct", "scheduled caste_pct", "top_group",
            "top_group_pct"]
    print(s[cols].to_string(index=False))


if __name__ == "__main__":
    main()
