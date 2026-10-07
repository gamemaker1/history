#!/usr/bin/env python3
"""Does the mountain predict the flock? Altitude and river valley against sheep and goats per household.

The Annales test of sub-question 1: if geography sets the form of herding,
the high villages should keep far more sheep and goats per household than the
low ones, whatever their castes. Reads:

  data/village_altitudes.csv   altitude as each 1961 survey states it (A15)
  data/places.csv              SRTM altitude at the geocoded point, used only where
                               the survey states none, and as a check on the geocoding
  data/flocks.csv              sheep and goats per village (A9)
  data/village_households.csv  households per village, with page (A15)
  data/entities.csv            river system of each village

Writes to analysis/geography/:

  villages.csv        one row per village: altitude, its basis, households,
                      sheep and goats, per household, share owned by landholding castes
  checks.csv          survey altitude against SRTM at the geocoded point
  altitude_flock.png  sheep and goats per household against altitude

Prints the Spearman rank correlation between altitude and animals per
household. With about 20 villages this is description, not proof.

Usage (from the project folder):
  .venv/bin/python scripts/geography.py

Needs pandas and matplotlib.
"""

import matplotlib
import matplotlib.ticker
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from corpus import ANALYSIS, DATA, ROOT, VILLAGES  # noqa: E402

OUT = ANALYSIS / "geography"
FT = 0.3048
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#dcdbd6"
VALLEY_COLOUR = {"Ravi": "#2a78d6", "Sutlej": "#eb6834", "Chenab": "#1baf7a", "Beas": "#eda100",
                 "Yamuna": "#e87ba4", "": "#8a8983"}


def spearman(x, y):
    rx, ry = pd.Series(x).rank(), pd.Series(y).rank()
    return rx.corr(ry)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    alt = pd.read_csv(DATA / "village_altitudes.csv", dtype=str).fillna("")
    alt["survey_m"] = (alt.feet_low.astype(float) + alt.feet_high.astype(float)) / 2 * FT
    places = pd.read_csv(DATA / "places.csv", dtype=str).fillna("")
    ents = pd.read_csv(DATA / "entities.csv", dtype=str).fillna("")
    # The 24 survey villages only (entity curation added other villages to entities.csv).
    vil = ents[(ents.subtype == "village") & ents.label.isin(list(VILLAGES))][["id", "label", "river_system"]] \
        .rename(columns={"label": "village"})
    vil = vil.merge(places[["id", "elevation_m", "method"]], on="id", how="left")
    vil["srtm_m"] = pd.to_numeric(vil.elevation_m, errors="coerce").where(vil.method.isin(["nominatim", "wikidata"]))
    vil = vil.merge(alt[["village", "survey_m", "feet_low", "feet_high", "pdf_page"]], on="village", how="left")
    vil["altitude_m"] = vil.survey_m.fillna(vil.srtm_m)
    vil["altitude_basis"] = ["survey" if s == s else ("SRTM at geocoded point" if t == t else "")
                             for s, t in zip(vil.survey_m, vil.srtm_m)]

    chk = vil[vil.survey_m.notna() & vil.srtm_m.notna()][["village", "survey_m", "srtm_m"]].copy()
    chk["difference_m"] = (chk.srtm_m - chk.survey_m).round(0)
    chk["agrees_within_300_m"] = chk.difference_m.abs() <= 300
    chk.round(0).to_csv(OUT / "checks.csv", index=False)

    hh = pd.read_csv(DATA / "village_households.csv", dtype=str).fillna("")
    hh["households"] = hh.households.astype(int)
    vil = vil.merge(hh[["village", "households"]], on="village", how="left")

    f = pd.read_csv(DATA / "flocks.csv", dtype=str).fillna("")
    for c in ("sheep", "goats", "sheep_and_goats"):
        f[c] = pd.to_numeric(f[c], errors="coerce")
    f["n"] = f.sheep_and_goats.fillna(f[["sheep", "goats"]].sum(axis=1, min_count=1))
    classes = pd.read_csv(DATA / "caste_classes.csv", dtype=str).set_index("group")["class"]
    f["class"] = f.group.map(classes)
    flock = f.groupby("village").n.sum(min_count=1).rename("sheep_and_goats")
    land = f[f["class"] == "landholding"].groupby("village").n.sum() / f[f.group != "all households"] \
        .groupby("village").n.sum()
    vil = vil.merge(flock, on="village", how="left").merge((land * 100).round(1).rename("landholding_pct"),
                                                            on="village", how="left")
    vil["per_household"] = (vil.sheep_and_goats / vil.households).round(2)
    cols = ["village", "river_system", "altitude_m", "altitude_basis", "feet_low", "feet_high", "pdf_page",
            "srtm_m", "households", "sheep_and_goats", "per_household", "landholding_pct"]
    vil = vil[cols].sort_values("altitude_m", ascending=False)
    vil.round(1).to_csv(OUT / "villages.csv", index=False)

    d = vil.dropna(subset=["altitude_m", "per_household"])
    rho = spearman(d.altitude_m, d.per_household)
    rho_land = spearman(d.dropna(subset=["landholding_pct"]).altitude_m, d.dropna(subset=["landholding_pct"]).landholding_pct)

    fig, ax = plt.subplots(figsize=(7.5, 4.8), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    for valley, g in d.groupby("river_system"):
        ax.scatter(g.altitude_m, g.per_household, s=46, color=VALLEY_COLOUR.get(valley, "#8a8983"),
                   edgecolor=SURFACE, linewidth=1.5, label=valley or "river system not assigned", zorder=3)
    placed = []
    for r in d.sort_values("per_household", ascending=False).itertuples():
        dy = 3
        # push a label down if another label already sits at nearly the same point
        while any(abs(r.altitude_m - a) < 120 and abs(dy - b) < 9 and abs(r.per_household - p) / max(p, 0.1) < 0.25
                  for a, b, p in placed):
            dy -= 10
        placed.append((r.altitude_m, dy, r.per_household))
        ax.annotate(r.village, (r.altitude_m, r.per_household), xytext=(5, dy), textcoords="offset points",
                    fontsize=7.5, color=INK)
    ax.set_yscale("symlog", linthresh=1)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}"))
    ax.set_xlabel("altitude of the village (m; the survey's own figure where it gives one)", fontsize=8.5, color=INK2)
    ax.set_ylabel("sheep and goats per household", fontsize=8.5, color=INK2)
    ax.tick_params(colors=INK2, labelsize=8, length=0)
    ax.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.legend(frameon=False, fontsize=8, loc="upper left", title="valley", title_fontsize=8)
    fig.suptitle(f"Altitude and flocks in the 1961 village surveys (Spearman rank correlation {rho:.2f}, "
                 f"{len(d)} villages)", x=0.01, ha="left", fontsize=10.5, color=INK)
    fig.text(0.01, 0.005, "Sources: village_altitudes.csv, flocks.csv, village_households.csv. Log-like scale "
             "above 1.", fontsize=7, color=INK2)
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    fig.savefig(OUT / "altitude_flock.png", dpi=200, facecolor=SURFACE)
    plt.close(fig)

    print(f"outputs in {OUT.relative_to(ROOT)}/")
    print(f"altitude check: {int(chk.agrees_within_300_m.sum())} of {len(chk)} geocoded villages within 300 m of "
          f"the survey's altitude")
    for r in chk[~chk.agrees_within_300_m].itertuples():
        print(f"  {r.village}: survey {r.survey_m:.0f} m, SRTM at geocoded point {r.srtm_m:.0f} m")
    print(f"Spearman rank correlation, altitude against sheep and goats per household: {rho:.2f} "
          f"({len(d)} villages)")
    print(f"Spearman rank correlation, altitude against landholding castes' share: {rho_land:.2f}")
    print(vil[["village", "river_system", "altitude_m", "altitude_basis", "households", "sheep_and_goats",
               "per_household", "landholding_pct"]].round(1).to_string(index=False))


if __name__ == "__main__":
    main()
