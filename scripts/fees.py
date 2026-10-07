#!/usr/bin/env python3
"""Grazing fees and fee-paying flocks: the rulers' rates against the Forest Department's, and Newell's series.

Reads data/fee_rates.csv (rates as printed, with their rupee value) and
data/fee_flocks.csv (Newell's grazing statement for Brahmaur tahsil,
1952-53 to 1961-62, read from the page image). Writes to analysis/fees/:

  rates.csv          every rate in rupees per head, with who collected it and when
  series.csv         the yearly series with totals and change on the first year
  phases.csv         change within three phases: 1952-57, 1957-60, 1960-62
  fee_flocks.png     sheep and goats paying fees, 1952-53 to 1961-62

Money: before 1957 one rupee was 16 annas and one anna 12 pies; from 1957
one rupee was 100 naya paise. So 2 annas 6 pies is 2.5 annas, Rs 0.156.

The question the series bears on (SQ3): Newell attributes the fall in flocks
to the Forest Department's permits, but his own table notes a sheep disease.
A fall that stops and does not recover after the disease is what a cap on
permits would produce, since only permitted animals pay fees; a recovery
would point to disease alone.

Usage (from the project folder):
  .venv/bin/python scripts/fees.py

Needs pandas and matplotlib.
"""

import matplotlib
import matplotlib.ticker
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from corpus import ANALYSIS, DATA, ROOT  # noqa: E402

OUT = ANALYSIS / "fees"
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#dcdbd6"
SERIES = {"sheep": "#2a78d6", "goats": "#eb6834"}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rates = pd.read_csv(DATA / "fee_rates.csv", dtype=str).fillna("")
    rates["rupees"] = rates.rupees.astype(float)
    rates.to_csv(OUT / "rates.csv", index=False)

    s = pd.read_csv(DATA / "fee_flocks.csv", dtype=str).fillna("")
    s["sheep"], s["goats"] = s.sheep.astype(int), s.goats.astype(int)
    s["total"] = s.sheep + s.goats
    first = s.iloc[0]
    for c in ("sheep", "goats", "total"):
        s[f"{c}_change_pct"] = ((s[c] / first[c] - 1) * 100).round(1)
    s.to_csv(OUT / "series.csv", index=False)

    idx = {y: i for i, y in enumerate(s.year)}
    phases = []
    for a, b, name in [("1952-53", "1956-57", "before the fall"), ("1956-57", "1959-60", "the fall"),
                       ("1959-60", "1961-62", "after the fall")]:
        ra, rb = s.iloc[idx[a]], s.iloc[idx[b]]
        phases.append({"phase": name, "from": a, "to": b,
                       **{f"{c}_change_pct": round((rb[c] / ra[c] - 1) * 100, 1) for c in ("sheep", "goats", "total")}})
    phases = pd.DataFrame(phases)
    phases.to_csv(OUT / "phases.csv", index=False)

    fig, ax = plt.subplots(figsize=(8, 4.2), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    x = range(len(s))
    for c, col in SERIES.items():
        ax.plot(x, s[c], color=col, linewidth=2, marker="o", markersize=5, label=c)
        ax.text(len(s) - 1 + 0.15, s[c].iloc[-1], f"{c} {s[c].iloc[-1]:,}", color=INK, fontsize=8.5, va="center")
        ax.text(-0.15, s[c].iloc[0], f"{s[c].iloc[0]:,}", color=INK2, fontsize=8, va="center", ha="right")
    d = idx["1959-60"]
    ax.axvspan(d - 1.5, d - 0.5, color=GRID, alpha=0.6, linewidth=0)
    ax.text(d - 1, 44500, "sheep disease\n(Newell: the year\nbefore 1959-60)", fontsize=7.5, color=INK2,
            ha="center", va="top")
    ax.set_xticks(list(x))
    ax.set_xticklabels(s.year, fontsize=8, color=INK2, rotation=0)
    ax.set_ylim(0, 46000)
    ax.set_xlim(-1.2, len(s) + 1.3)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.tick_params(colors=INK2, labelsize=8, length=0)
    ax.yaxis.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.legend(frameon=False, fontsize=8.5, loc="lower left")
    fig.suptitle("Sheep and goats paying grazing fees in Brahmaur tahsil, 1952-53 to 1961-62",
                 x=0.01, ha="left", fontsize=11, color=INK)
    fig.text(0.01, 0.01, "Source: Newell, grazing statement from the Brahmaur Forest Officer (Report on SC and ST of "
             "Himachal Pradesh, PDF p. 38), read from the page image.", fontsize=7, color=INK2)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(OUT / "fee_flocks.png", dpi=200, facecolor=SURFACE)
    plt.close(fig)

    last = s.iloc[-1]
    print(f"outputs in {OUT.relative_to(ROOT)}/")
    print(f"fee-paying flocks {first.year} to {last.year}: sheep {last.sheep_change_pct}%, goats "
          f"{last.goats_change_pct}%, total {last.total_change_pct}% ({first.total:,} to {last.total:,})")
    print(phases.to_string(index=False))
    print("rates in rupees per head:")
    for r in rates.itertuples():
        print(f"  {r.year} {r.place}: {r.animal} {r.rupees:.3f} ({r.rate_as_printed}, per {r.per}; "
              f"collected by {r.collector}) [{r.source} p. {r.pdf_page}]")


if __name__ == "__main__":
    main()
