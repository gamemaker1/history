#!/usr/bin/env python3
"""Map the herding routes: home villages, summer pastures and passes, winter grounds and fairs.

Reads data/places.csv (geocode.py) and the movement and trade claims in
analysis/graph/edges.csv. Every claim whose two ends both have coordinates
becomes a line from where the claim holds (the village, or the subject place)
to its destination, coloured by destination class:

  winter grounds (blue), summer pastures and passes (orange), fairs and markets (aqua)

Each line's popup gives the claim, its quote and its source and page. Lines
are in layers by river valley, so the Ravi and the upper Sutlej can be
compared, and the survey villages are drawn on top with their altitude. The
base map is OpenTopoMap, which shows relief.

Outputs in analysis/maps/:
  routes.html         the interactive map (Folium / Leaflet)
  route_lines.csv     the lines drawn, with their claims
  villages.csv        survey villages with coordinates, altitude and flock size (data/flocks.csv)

Usage (from the project folder):
  .venv/bin/python scripts/map_routes.py
  .venv/bin/python scripts/map_routes.py --evidence ai
  .venv/bin/python scripts/map_routes.py --print     # also routes_print.html, OpenStreetMap base, for a static image

Needs folium and pandas. Programming Historian: "Web Mapping with Python and
Leaflet" and "Creating Choropleth Maps with Python and Folium".
"""

import argparse
import html

import folium
import pandas as pd

from corpus import ANALYSIS, DATA, ROOT
from calendar_chart import destination_class

OUT = ANALYSIS / "maps"
PREDICATES = ["GRAZES_AT", "MIGRATES_TO", "MOVES_VIA", "TRADES_AT"]
COLOUR = {"winter grounds": "#2a78d6", "summer pastures": "#eb6834", "fairs and markets": "#1baf7a"}
LEVEL = {"ai_rejected": -1, "image_unverified": 0, "auto": 1, "ai_partly": 1, "ai_checked": 2, "human": 3}


def load(min_evidence):
    e = pd.read_csv(ANALYSIS / "graph" / "edges.csv", dtype=str).fillna("")
    n = pd.read_csv(ANALYSIS / "graph" / "nodes.csv", dtype=str).fillna("")
    ents = pd.read_csv(DATA / "entities.csv", dtype=str).fillna("")
    p = pd.read_csv(DATA / "places.csv", dtype=str).fillna("")
    p = p[p.lat != ""].assign(lat=lambda d: d.lat.astype(float), lon=lambda d: d.lon.astype(float))
    floor = {"all": 0, "auto": 1, "ai": 2, "human": 3}[min_evidence]
    e = e[e.predicate.isin(PREDICATES) & (e.evidence.map(LEVEL) >= floor)]
    base = dict(zip(n.label, n.base_id))
    by_label = dict(zip(ents.label, ents.id))
    sub = dict(zip(ents.id, ents.subtype))
    e = e.assign(origin=[by_label.get(pl, "") or base.get(s, "") for pl, s in zip(e.place, e.subject)],
                 dest=e.object.map(lambda o: base.get(o, o)))
    e["dest_class"] = [destination_class(d, sub.get(d, ""), pr) for d, pr in zip(e.dest, e.predicate)]
    return e, p.set_index("id"), ents


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--evidence", choices=["all", "auto", "ai", "human"], default="all")
    ap.add_argument("--print", action="store_true", dest="print_version",
                    help="also write routes_print.html on the OpenStreetMap base (more reliable for screenshots)")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    for base in (["relief", "osm"] if args.print_version else ["relief"]):
        build(args, base)


def build(args, base):
    e, places, ents = load(args.evidence)

    lines = e[e.origin.isin(places.index) & e.dest.isin(places.index) & (e.origin != e.dest)
              & e.dest_class.isin(list(COLOUR))].copy()
    lines.to_csv(OUT / "route_lines.csv", index=False,
                 columns=["origin", "dest", "dest_class", "predicate", "subject", "object", "months", "valley",
                          "source", "pdf_page", "layer_year", "evidence", "quote"])

    m = folium.Map(location=[32.0, 77.0], zoom_start=8, tiles=None, control_scale=True)
    # Relief is the default; the plain layer is standard OpenStreetMap (CartoDB tiles now need an API key).
    # The print version shows OpenStreetMap first, because its tiles load reliably for a screenshot.
    folium.TileLayer("OpenStreetMap", name="Plain (OpenStreetMap)", show=(base == "osm")).add_to(m)
    folium.TileLayer("https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png", name="Relief (OpenTopoMap)",
                     show=(base == "relief"),
                     attr="Map data: OpenStreetMap contributors, SRTM | Style: OpenTopoMap (CC-BY-SA)").add_to(m)

    for valley, g in lines.groupby(lines.valley.where(lines.valley != "", "other or none")):
        layer = folium.FeatureGroup(name=f"Routes: {valley} ({len(g)} claims)", show=True)
        for (o, d, cls), lg in g.groupby(["origin", "dest", "dest_class"]):
            a, b = places.loc[o], places.loc[d]
            items = "".join(
                f"<li>{html.escape(r.subject)} {r.predicate} {html.escape(r.object)}"
                f"{' (' + r.months.replace('|', ', ') + ')' if r.months else ''}: "
                f"<i>{html.escape(r.quote[:180])}</i> [{html.escape(r.source)}, p. {r.pdf_page}, {r.layer_year}]</li>"
                for r in lg.itertuples())
            popup = folium.Popup(f"<b>{html.escape(a.label)} → {html.escape(b.label)}</b> ({cls})<ul>{items}</ul>",
                                 max_width=420)
            folium.PolyLine([(a.lat, a.lon), (b.lat, b.lon)], color=COLOUR[cls], weight=1.5 + min(len(lg), 6) * 0.6,
                            opacity=0.8, dash_array="6 4" if cls == "summer pastures" else None,
                            tooltip=f"{a.label} → {b.label}: {cls}, {len(lg)} claim(s)", popup=popup).add_to(layer)
        layer.add_to(m)

    dests = folium.FeatureGroup(name="Pastures, passes, winter grounds and fairs", show=True)
    used = set(lines.dest)
    for pid in used:
        r = places.loc[pid]
        cls = lines[lines.dest == pid].dest_class.iloc[0]
        folium.CircleMarker([r.lat, r.lon], radius=4, color=COLOUR[cls], fill=True, fill_opacity=0.9, weight=1,
                            tooltip=f"{r.label} ({r.subtype}, {r.elevation_m} m)").add_to(dests)
    dests.add_to(m)

    flocks = pd.read_csv(DATA / "flocks.csv", dtype=str).fillna("")
    flocks["n"] = pd.to_numeric(flocks.sheep_and_goats, errors="coerce")
    flocks.loc[flocks.n.isna(), "n"] = pd.to_numeric(flocks.sheep, errors="coerce").fillna(0) + \
        pd.to_numeric(flocks.goats, errors="coerce").fillna(0)
    size = flocks.groupby("village").n.sum()
    vil = ents[ents.subtype == "village"]
    rows = []
    villages = folium.FeatureGroup(name="Survey villages (1961)", show=True)
    for v in vil.itertuples():
        if v.id not in places.index:
            continue
        r = places.loc[v.id]
        n = size.get(v.label)
        rows.append({"village": v.label, "river_system": v.river_system, "lat": r.lat, "lon": r.lon,
                     "elevation_m": r.elevation_m, "sheep_and_goats": n})
        folium.CircleMarker([r.lat, r.lon], radius=5 + (min(n, 5000) ** 0.5) / 8 if n == n and n else 5,
                            color="#0b0b0b", weight=1.5, fill=True, fill_color="#fcfcfb", fill_opacity=1,
                            tooltip=f"{v.label}: {r.elevation_m} m, {int(n) if n == n and n else 'no'} sheep and goats "
                                    f"({v.river_system or 'river system not assigned'})").add_to(villages)
        folium.map.Marker([r.lat, r.lon], icon=folium.DivIcon(
            html=f'<div style="font:600 11px system-ui;color:#0b0b0b;transform:translate(8px,-6px);'
                 f'text-shadow:0 0 3px #fff,0 0 3px #fff">{html.escape(v.label)}</div>')).add_to(villages)
    villages.add_to(m)
    pd.DataFrame(rows).sort_values("elevation_m", ascending=False).to_csv(OUT / "villages.csv", index=False)

    legend = ('<div style="position:fixed;bottom:18px;left:12px;z-index:9999;background:#fcfcfb;padding:8px 10px;'
              'border:1px solid #dcdbd6;border-radius:6px;font:12px system-ui;color:#0b0b0b">'
              '<b>Routes in the 1961 surveys and colonial sources</b><br>'
              + "".join(f'<span style="display:inline-block;width:26px;border-top:3px {"dashed" if k == "summer pastures" else "solid"} {c};'
                        f'vertical-align:middle;margin-right:6px"></span>{k}<br>' for k, c in COLOUR.items())
              + '<span style="display:inline-block;width:10px;height:10px;border:1.5px solid #0b0b0b;border-radius:50%;'
                'margin:0 8px 0 8px;vertical-align:middle"></span>survey village (size: flock)<br>'
                '<span style="color:#52514e">Click a line for its claims, quotes and pages.</span></div>')
    m.get_root().html.add_child(folium.Element(legend))
    # Zoom to the routes and villages drawn, and keep the layer list folded into its button.
    pts = [(places.loc[o].lat, places.loc[o].lon) for o in set(lines.origin) | set(lines.dest)] + \
          [(r["lat"], r["lon"]) for r in rows]
    if pts:
        lats, lons = [p[0] for p in pts], [p[1] for p in pts]
        m.fit_bounds([[min(lats) - 0.15, min(lons) - 0.15], [max(lats) + 0.15, max(lons) + 0.15]])
    folium.LayerControl(collapsed=True).add_to(m)
    m.save(OUT / ("routes.html" if base == "relief" else "routes_print.html"))
    if base != "relief":
        return
    print(f"{len(lines)} claims drawn as {lines.groupby(['origin', 'dest', 'dest_class']).ngroups} lines "
          f"(evidence: {args.evidence}); {len(rows)} survey villages; outputs in {OUT.relative_to(ROOT)}/")
    print("  by destination: " + ", ".join(f"{k} {v}" for k, v in lines.dest_class.value_counts().items()))
    print("  by valley: " + ", ".join(f"{k or 'other'} {v}" for k, v in lines.valley.value_counts().items()))
    skipped = e[~(e.origin.isin(places.index) & e.dest.isin(places.index))]
    print(f"  {len(skipped)} movement claims not drawn (an end without coordinates or a generic place)")


if __name__ == "__main__":
    main()
