#!/usr/bin/env python3
"""Give coordinates and altitude to the places in the movement, trade and location claims.

Collects every place entity named in a GRAZES_AT, MIGRATES_TO, MOVES_VIA,
TRADES_AT or LOCATED_ON claim (as subject, object or place), looks each up in
OpenStreetMap's Nominatim geocoder, and adds an elevation from the SRTM
90 m elevation model through the OpenTopoData API. The 24 survey villages are
looked up with their 1961 district and tahsil (from sources/index.md), so
that Bir resolves to Bir in Mandi rather than Bir in Kangra.

Each place is tried under its label and then its aliases in data/entities.csv
(OSM spells Sirmur "Sirmaur"). If Nominatim finds nothing, Wikidata is tried:
its search API, then the item's coordinate location (P625). A match is
accepted only inside a box around the western Himalaya, the Punjab plains and
western Tibet (latitude 29.5 to 36, longitude 73 to 81.5). Generic places
("high pastures", "low hills") are not geocoded.

data/places_manual.csv, if present, overrides any row. A row may give
coordinates read off a map (lat, lon, basis), or name another place in
same_as: a fair takes the coordinates of the town it is held in (the Lavi
fair is at Rampur). A row with text in reject removes a match known to be
wrong (another village of the same name), keeping the reason. The group can
add rows there.

Writes data/places.csv: id, label, subtype, lat, lon, elevation_m, the query
used, the name OSM matched, and the method. Results are cached in
cache/geocode.json, so reruns do not repeat requests.

Usage (from the project folder):
  .venv/bin/python scripts/geocode.py
  .venv/bin/python scripts/geocode.py --no-wikidata   # no new Wikidata requests (use its cached answers)

Respects Nominatim's usage policy (one request a second, an identifying
User-Agent). Needs requests (requirements.txt) and a network connection.
Programming Historian: "Geocoding Historical Data using QGIS" and "Working
with Named Places: How and Why to Build a Gazetteer".
"""

import csv
import json
import time

import pandas as pd
import requests

from corpus import ANALYSIS, CACHE, DATA, ROOT

PREDICATES = ["GRAZES_AT", "MIGRATES_TO", "MOVES_VIA", "TRADES_AT", "LOCATED_ON"]
GENERIC = {"high_pastures", "low_hills", "pasture", "x_minor_ranges"}
BOX = (29.5, 36.0, 73.0, 81.5)  # western Himalaya, the Punjab plains, and western Tibet (Gartok)
HEADERS = {"User-Agent": "IIITH-history-coursework/1.0 (seasonal herding in Himachal, geocoding place names)"}
CACHE_FILE = CACHE / "geocode.json"

# The survey villages with their 1961 district and tahsil (sources/index.md).
VILLAGE_QUERY = {
    "basal": "Basal, Solan, Himachal Pradesh", "batal": "Batal, Arki, Solan, Himachal Pradesh",
    "brahmaur": "Bharmour, Chamba, Himachal Pradesh", "bir": "Bir, Mandi, Himachal Pradesh",
    "chaunri": "Junga, Shimla, Himachal Pradesh", "chauntra": "Chauntra, Jogindernagar, Mandi, Himachal Pradesh",
    "chaupal": "Chaupal, Shimla, Himachal Pradesh", "chergaon": "Chirgaon, Rohru, Shimla, Himachal Pradesh",
    "chitrari": "Chitrari, Chamba, Himachal Pradesh", "devi_kothi": "Devi Kothi, Chamba, Himachal Pradesh",
    "kalath": "Kalath, Solan, Himachal Pradesh", "kanum": "Kanam, Kinnaur, Himachal Pradesh",
    "kot": "Kot, Sarkaghat, Mandi, Himachal Pradesh", "kothi": "Kothi, Kalpa, Kinnaur, Himachal Pradesh",
    "kupha": "Kupha, Pangi, Chamba, Himachal Pradesh", "maingal": "Maingal, Chamba, Himachal Pradesh",
    "moginand": "Moginand, Sirmaur, Himachal Pradesh", "nachar": "Nichar, Kinnaur, Himachal Pradesh",
    "nalag": "Nalag, Mandi, Himachal Pradesh", "pangna": "Pangna, Karsog, Mandi, Himachal Pradesh",
    "rajana": "Rajana, Sirmaur, Himachal Pradesh", "shakrori": "Shakrori, Mandi, Himachal Pradesh",
    "shathla": "Shathla, Kotgarh, Shimla, Himachal Pradesh", "tandi": "Tandi, Lahaul and Spiti, Himachal Pradesh",
}


def places():
    e = pd.read_csv(ANALYSIS / "graph" / "edges.csv", dtype=str).fillna("")
    n = pd.read_csv(ANALYSIS / "graph" / "nodes.csv", dtype=str).fillna("")
    ents = pd.read_csv(DATA / "entities.csv", dtype=str).fillna("")
    base = dict(zip(n.label, n.base_id))
    by_label = dict(zip(ents.label, ents.id))
    e = e[e.predicate.isin(PREDICATES)]
    ids = set(e.object.map(lambda x: base.get(x, x))) | set(e.subject.map(lambda x: base.get(x, x))) \
        | set(e.place.map(lambda x: by_label.get(x, "")))
    ids |= set(VILLAGE_QUERY)
    ents = ents[ents.id.isin(ids) & (ents.type == "place") & ~ents.id.isin(GENERIC)]
    return ents


def query_for(e):
    if e.id in VILLAGE_QUERY:
        return [VILLAGE_QUERY[e.id], f"{e.label}, Himachal Pradesh, India"]
    names = [e.label] + [a for a in e.aliases.split("|") if a and len(a) > 3][:3]
    return [f"{n}, Himachal Pradesh, India" for n in names] + [f"{n}, India" for n in names[:1]]


WIKIDATA_OFF = False


def wikidata_get(params):
    """One polite Wikidata API call: 2.5 s apart, honouring Retry-After on HTTP 429. None if refused."""
    global WIKIDATA_OFF
    if WIKIDATA_OFF:
        return None
    for attempt in range(3):
        time.sleep(2.5)
        r = requests.get("https://www.wikidata.org/w/api.php", headers=HEADERS, timeout=30,
                         params={**params, "format": "json"})
        if r.status_code == 200:
            return r.json()
        wait = int(r.headers.get("Retry-After", "20") or 20)
        print(f"  Wikidata answered {r.status_code}; waiting {wait} s", flush=True)
        time.sleep(min(wait, 60))
    WIKIDATA_OFF = True
    print("  Wikidata keeps refusing; skipping it for the rest of this run", flush=True)
    return None


def wikidata(name, cache):
    """Coordinates from Wikidata for a name: search, then P625 of the first hits."""
    key = f"wd:{name}"
    if key in cache:
        return cache[key]
    if WIKIDATA_OFF:
        return []
    found = wikidata_get({"action": "wbsearchentities", "search": name, "language": "en", "limit": 5})
    if found is None:
        return []
    ids = [h["id"] for h in found.get("search", [])]
    hits = []
    if ids:
        got = wikidata_get({"action": "wbgetentities", "ids": "|".join(ids), "props": "claims|labels|descriptions",
                            "languages": "en"})
        if got is None:
            return []
        for qid in ids:
            ent = got.get("entities", {}).get(qid, {})
            for c in ent.get("claims", {}).get("P625", [])[:1]:
                v = c["mainsnak"].get("datavalue", {}).get("value", {})
                if "latitude" in v:
                    desc = ent.get("descriptions", {}).get("en", {}).get("value", "")
                    label = ent.get("labels", {}).get("en", {}).get("value", "")
                    hits.append({"lat": v["latitude"], "lon": v["longitude"], "display_name": f"{label}, {desc} ({qid})"})
    cache[key] = hits
    return hits


def nominatim(q, cache):
    if q in cache:
        return cache[q]
    time.sleep(1.1)
    r = requests.get("https://nominatim.openstreetmap.org/search", headers=HEADERS, timeout=30,
                     params={"q": q, "format": "jsonv2", "limit": 5, "accept-language": "en"})
    r.raise_for_status()
    cache[q] = r.json()
    return cache[q]


def in_box(lat, lon):
    return BOX[0] <= lat <= BOX[1] and BOX[2] <= lon <= BOX[3]


def elevations(points, cache):
    todo = [p for p in points if f"{p[0]:.5f},{p[1]:.5f}" not in cache]
    for i in range(0, len(todo), 90):
        chunk = todo[i:i + 90]
        time.sleep(1.1)
        r = requests.get("https://api.opentopodata.org/v1/srtm90m", timeout=60,
                         params={"locations": "|".join(f"{a},{b}" for a, b in chunk)})
        r.raise_for_status()
        for (a, b), res in zip(chunk, r.json()["results"]):
            cache[f"{a:.5f},{b:.5f}"] = res["elevation"]
    return {p: cache.get(f"{p[0]:.5f},{p[1]:.5f}") for p in points}


def main():
    global WIKIDATA_OFF
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--no-wikidata", action="store_true",
                    help="use only Wikidata answers already cached (Wikidata rate-limits anonymous clients)")
    args = ap.parse_args()
    WIKIDATA_OFF = args.no_wikidata
    cache = json.loads(CACHE_FILE.read_text()) if CACHE_FILE.exists() else {}
    ents = places()
    rows = []
    for e in ents.itertuples():
        hit, used = None, ""
        for q in query_for(e):
            for cand in nominatim(q, cache):
                lat, lon = float(cand["lat"]), float(cand["lon"])
                if in_box(lat, lon):
                    hit, used = cand, q
                    break
            if hit:
                break
        method = "nominatim" if hit else "not found"
        if not hit:
            for name in [e.label] + [a for a in e.aliases.split("|") if a and len(a) > 3][:2]:
                for cand in wikidata(name, cache):
                    if in_box(float(cand["lat"]), float(cand["lon"])):
                        hit, used, method = cand, f"wikidata: {name}", "wikidata"
                        break
                if hit:
                    break
        rows.append({"id": e.id, "label": e.label, "subtype": e.subtype,
                     "lat": round(float(hit["lat"]), 5) if hit else "", "lon": round(float(hit["lon"]), 5) if hit else "",
                     "elevation_m": "", "query": used, "osm_name": hit["display_name"][:120] if hit else "",
                     "method": method, "checked_by": ""})
        CACHE_FILE.write_text(json.dumps(cache))
    manual = DATA / "places_manual.csv"
    if manual.exists():
        over = {r["id"]: r for r in csv.DictReader(open(manual, encoding="utf-8"))}
        by_id = {r["id"]: r for r in rows}
        for r in rows:
            o = over.get(r["id"])
            if not o:
                continue
            if o.get("reject", "").strip():
                r.update(lat="", lon="", elevation_m="", method=f"rejected: {o['reject']}", osm_name=r["osm_name"])
            elif o.get("same_as"):
                src = by_id.get(o["same_as"])
                if src and src["lat"] != "":
                    r.update(lat=src["lat"], lon=src["lon"], method=f"same as {o['same_as']}: {o.get('basis', '')}",
                             osm_name=src["osm_name"], checked_by=o.get("checked_by", ""))
            elif o.get("lat"):
                r.update(lat=float(o["lat"]), lon=float(o["lon"]), method=f"manual: {o.get('basis', '')}",
                         checked_by=o.get("checked_by", ""))
    pts = [(r["lat"], r["lon"]) for r in rows if r["lat"] != ""]
    elev = elevations(pts, cache.setdefault("_elev", {}))
    for r in rows:
        if r["lat"] != "":
            r["elevation_m"] = elev.get((r["lat"], r["lon"]), "")
    CACHE_FILE.write_text(json.dumps(cache))
    with open(DATA / "places.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(sorted(rows, key=lambda r: (r["method"] == "not found", r["subtype"], r["label"])))
    found = [r for r in rows if r["lat"] != ""]
    print(f"{len(rows)} places: {len(found)} with coordinates, {len(rows) - len(found)} not found; "
          f"written to {(DATA / 'places.csv').relative_to(ROOT)}")
    villages = [r for r in found if r["id"] in VILLAGE_QUERY]
    print(f"  survey villages located: {len(villages)} of {len(VILLAGE_QUERY)}")
    for r in sorted(villages, key=lambda r: -(r["elevation_m"] or 0)):
        print(f"    {r['label']:11s} {r['elevation_m']} m  ({r['osm_name'][:60]})")


if __name__ == "__main__":
    main()
