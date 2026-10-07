#!/usr/bin/env python3
"""Build the knowledge graph from the verified claims and export it for Cytoscape.

Nodes are the entities in data/entities.csv that appear in at least one claim
(plus any unresolved names, marked uncurated). Edges are the claims in
data/claims.csv, one edge per claim, each carrying its predicate, family,
quantity, months, place, time, conjuncture, source, PDF page, quote and
evidence level.

The conjuncture of each claim is assigned by the ordered rules in
conjuncture() below, so the periodisation is visible and can be argued with.
The conjunctures follow ideas/seasonal-herding-himachal.md (Step 2) and
ideas/two-valleys-sutlej-ravi.md (the trade conjuncture).

Outputs in analysis/graph/:
  kg.cyjs                Cytoscape JSON of the whole graph (opens in Cytoscape Desktop)
  kg_<conjuncture>.cyjs  one file per conjuncture
  kg.graphml             the whole graph, for Gephi or other tools
  kg.html                standalone Cytoscape.js viewer with filters, an edge
                         detail panel and a table view
  edges.csv, nodes.csv   flat tables of the graph

Usage (from the project folder):
  .venv/bin/python scripts/build_graph.py
  .venv/bin/python scripts/build_graph.py --evidence human    # only claims signed off by a person

Needs networkx (requirements.txt). The viewer loads Cytoscape.js from a CDN.
"""

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

import networkx as nx

from corpus import ANALYSIS, DATA, ROOT
from kg_schema import PREDICATES

OUT = ANALYSIS / "graph"
STYLE = Path(__file__).with_name("cytoscape_style.json")

CONJUNCTURES = {
    "cycle": "The mountain year (longue durée): recurring movement and the geography it follows",
    "two_sovereigns": "Two sovereigns, c. 1846 to 1947: British Kangra and Chamba claim the same Gaddis",
    "princely_pastures": "The rulers' pastures, to about 1950: grazing rights, fee auctions, begar",
    "forest_department": "The Forest Department, 1948 to 1961: permits, fees, closures",
    "trade_and_credit": "Trade and credit, to the early 1960s: Tibet, fairs, merchants, moneylenders",
    "roads_and_wages": "Roads and wages, 1950s to 1961: road work, hired shepherds leave",
    "standing": "Standing structure at the survey: who owns the flocks and how many households",
}

# Evidence levels, lowest first. A claim the AI checker (check_claims.py) found not supported is
# left out unless --evidence everything is given.
RANK = {"ai_rejected": -1, "image_unverified": 0, "auto": 1, "ai_partly": 1, "ai_checked": 2, "human": 3}
LEVELS = {"everything": -1, "all": 0, "auto": 1, "ai": 2, "human": 3}


def conjuncture(r):
    """Assign a claim to a conjuncture. The first rule that matches wins."""
    ids = {r["subject_id"], r["object_id"], r["resource_id"]}
    pred, when, colonial = r["predicate"], r["when"], int(r["layer_year"]) < 1948
    # Two sovereigns: British Kangra, or a colonial source on Gaddi dues and land across the range.
    if "british_kangra" in ids or (colonial and pred == "PAYS_DUES_TO") or \
            (colonial and pred == "OWNS" and r["object_id"] == "land"):
        return "two_sovereigns"
    # Who owns the flocks and how many households there are: the standing contradiction.
    if pred in ("OWNS", "HAS_POPULATION") and r["object_id"] not in ("land", "grazing_permit", "grazing_right"):
        return "standing"
    if "forest_department" in ids or "grazing_permit" in ids or pred in ("ISSUES_PERMIT_TO", "CLOSES"):
        return "forest_department"
    if ids & {"raja_chamba", "bushahr_ruler", "mandi_ruler", "fee_contractor"}:
        return "princely_pastures"
    if pred == "WORKS_AS" or ids & {"road_labourer", "road_construction", "fawal"}:
        return "roads_and_wages"
    if ids & {"india_china_dispute", "tibet", "gartok", "shipki_la"} or \
            pred in ("CARRIES", "TRADES_AT", "SELLS_TO", "BUYS_FROM", "LENDS_TO"):
        return "trade_and_credit"
    if when == "before_1948":
        return "princely_pastures"
    if when == "recurring" or PREDICATES[pred][0] in ("movement", "geography"):
        return "cycle"
    return "standing"


def evidence(r, check):
    if r["verified_by"] and r["human_status"] not in ("rejected", "wrong"):
        return "human"
    if r["quote_match"] == "image":
        return "image_unverified"
    verdict = check.get("verdict", "")
    return {"supported": "ai_checked", "partly_supported": "ai_partly", "not_supported": "ai_rejected"}.get(verdict, "auto")


def slug(name):
    return "x_" + "_".join(re.findall(r"[a-z0-9]+", name.lower()))


def load(min_level):
    with open(DATA / "entities.csv", encoding="utf-8") as f:
        entities = {e["id"]: e for e in csv.DictReader(f)}
    with open(DATA / "claims.csv", encoding="utf-8") as f:
        claims = [r for r in csv.DictReader(f) if r["human_status"] not in ("rejected", "wrong")]
    checks = {}
    if (DATA / "claim_checks.csv").exists():
        with open(DATA / "claim_checks.csv", encoding="utf-8") as f:
            checks = {c["claim_id"]: c for c in csv.DictReader(f)}
    keep = []
    for r in claims:
        check = checks.get(r["claim_id"], {})
        ev = evidence(r, check)
        if RANK[ev] >= LEVELS[min_level]:
            r["ai_verdict"], r["ai_reason"] = check.get("verdict", ""), check.get("reason", "")
            keep.append((r, ev))
    return entities, keep


def build(entities, claims):
    """One node per entity, except that groups and roles are scoped to their village:
    the Rajputs of Brahmaur and the Rajputs of Kothi are different people, and a
    generic "households" node would join every village into one hub."""
    g = nx.MultiDiGraph()

    def node(eid, label, typ, place_id):
        e = entities.get(eid)
        typ = e["type"] if e else (typ or "place")
        place = entities.get(place_id)
        scoped = typ in ("group", "role") and place and place["subtype"] == "village"
        nid = f"{eid}@{place_id}" if scoped else eid
        if nid in g:
            return nid
        name = e["label"] if e else label
        g.add_node(nid, label=f"{name} ({place['label']})" if scoped else name, type=typ,
                   base_id=eid, village=place["label"] if scoped else "",
                   subtype=e["subtype"] if e else "", river_system=(place or {}).get("river_system", "") if scoped
                   else (e["river_system"] if e else ""), note=e["note"] if e else "", uncurated=not e)
        return nid

    for r, ev in claims:
        s_id = node(r["subject_id"] or slug(r["subject"]), r["subject"], r.get("subject_type", ""), r["place_id"])
        o_id = node(r["object_id"] or slug(r["object"]), r["object"], r.get("object_type", ""), r["place_id"])
        place = entities.get(r["place_id"], {})
        valley = place.get("river_system") or g.nodes[s_id]["river_system"] or g.nodes[o_id]["river_system"]
        g.add_edge(s_id, o_id, key=r["claim_id"],
                   predicate=r["predicate"], family=PREDICATES[r["predicate"]][0],
                   resource=r["resource"], resource_id=r["resource_id"],
                   qty=r["qty"], unit=r["unit"], months=r["months"],
                   place=r["place"], place_id=r["place_id"], valley=valley,
                   when=r["when"], date_text=r["date_text"],
                   conjuncture=conjuncture(r), source=r["source"], pdf_page=int(r["pdf_page"]),
                   layer_year=int(r["layer_year"]), quote=r["quote"], note=r["note"],
                   quote_match=r["quote_match"], evidence=ev, verified_by=r["verified_by"],
                   extracted_by=r["extracted_by"], ai_verdict=r["ai_verdict"], ai_reason=r["ai_reason"])
    for n in g.nodes:
        g.nodes[n]["degree"] = g.degree(n)
    return g


def cyjs(g):
    data = nx.cytoscape_data(g)
    for e in data["elements"]["edges"]:
        e["data"]["id"] = e["data"]["key"]
    return data


def write_tables(g):
    with open(OUT / "nodes.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "base_id", "label", "type", "subtype", "village", "river_system", "degree", "uncurated"])
        for n, d in g.nodes(data=True):
            w.writerow([n, d["base_id"], d["label"], d["type"], d["subtype"], d["village"], d["river_system"],
                        d["degree"], d["uncurated"]])
    fields = ["claim_id", "subject", "predicate", "object", "family", "resource", "qty", "unit", "months", "place",
              "valley", "when", "date_text", "conjuncture", "source", "pdf_page", "layer_year",
              "evidence", "ai_verdict", "extracted_by", "quote"]
    with open(OUT / "edges.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(fields)
        for s, o, k, d in g.edges(keys=True, data=True):
            w.writerow([k, g.nodes[s]["label"], d["predicate"], g.nodes[o]["label"]] +
                       [d[x] for x in fields[4:]])


def write_html(g, data):
    style = json.loads(STYLE.read_text(encoding="utf-8"))
    families = sorted({d["family"] for _, _, d in g.edges(data=True)})
    valleys = sorted({d["valley"] for _, _, d in g.edges(data=True) if d["valley"]})
    layers = sorted({d["layer_year"] for _, _, d in g.edges(data=True)})
    html = HTML.replace("__ELEMENTS__", json.dumps(data["elements"], ensure_ascii=False)) \
        .replace("__STYLE__", json.dumps(style)) \
        .replace("__CONJUNCTURES__", json.dumps(CONJUNCTURES)) \
        .replace("__FAMILIES__", json.dumps(families)) \
        .replace("__VALLEYS__", json.dumps(valleys)) \
        .replace("__LAYERS__", json.dumps(layers))
    (OUT / "kg.html").write_text(html, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--evidence", choices=list(LEVELS), default="all",
                    help="everything: all kept claims, even those the AI checker rejected; all (default): "
                         "leave those out; auto: also drop unchecked image claims; ai: only claims the "
                         "AI checker supported or a person signed off; human: only signed-off claims")
    args = ap.parse_args()

    entities, claims = load(args.evidence)
    g = build(entities, claims)
    OUT.mkdir(parents=True, exist_ok=True)

    data = cyjs(g)
    (OUT / "kg.cyjs").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    for c in CONJUNCTURES:
        edges = [(s, o, k) for s, o, k, d in g.edges(keys=True, data=True) if d["conjuncture"] == c]
        sub = g.edge_subgraph(edges).copy()
        (OUT / f"kg_{c}.cyjs").write_text(json.dumps(cyjs(sub), ensure_ascii=False, indent=1), encoding="utf-8")
    nx.write_graphml(g, OUT / "kg.graphml")
    write_tables(g)
    write_html(g, data)

    print(f"{g.number_of_nodes()} nodes, {g.number_of_edges()} edges (evidence: {args.evidence}) "
          f"written to {OUT.relative_to(ROOT)}/")
    print("  by conjuncture: " + ", ".join(f"{k} {v}" for k, v in
                                           Counter(d["conjuncture"] for *_, d in g.edges(data=True)).most_common()))
    print("  by family: " + ", ".join(f"{k} {v}" for k, v in
                                      Counter(d["family"] for *_, d in g.edges(data=True)).most_common()))
    print("  by evidence: " + ", ".join(f"{k} {v}" for k, v in
                                        Counter(d["evidence"] for *_, d in g.edges(data=True)).most_common()))
    unc = [d["label"] for _, d in g.nodes(data=True) if d["uncurated"]]
    if unc:
        print(f"  {len(unc)} uncurated nodes (add them to data/entities.csv): {', '.join(unc[:10])}")


HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Seasonal herding in the Himachal hills: knowledge graph</title>
<script src="https://unpkg.com/cytoscape@3/dist/cytoscape.min.js"></script>
<style>
  .viz-root {
    color-scheme: light;
    --surface-1: #fcfcfb; --surface-2: #f0efec; --rule: #dcdbd6;
    --text-primary: #0b0b0b; --text-secondary: #52514e; --text-muted: #77766f;
    --movement: #2a78d6; --extraction: #eb6834; --property: #1baf7a; --neutral: #52514e; --light: #b8b7b0;
  }
  body { margin: 0; font: 14px/1.4 system-ui, sans-serif; }
  .viz-root { background: var(--surface-1); color: var(--text-primary); min-height: 100vh; }
  header { padding: 12px 16px 8px; border-bottom: 1px solid var(--rule); }
  h1 { font-size: 17px; margin: 0 0 8px; }
  .filters { display: flex; flex-wrap: wrap; gap: 12px 18px; align-items: center; font-size: 13px; }
  .filters label { color: var(--text-secondary); }
  select { font: inherit; max-width: 300px; }
  main { display: grid; grid-template-columns: 1fr 340px; height: calc(100vh - 92px); min-height: 520px; }
  #cy { border-right: 1px solid var(--rule); }
  aside { overflow-y: auto; padding: 12px 14px; font-size: 13px; }
  aside h2 { font-size: 13px; text-transform: uppercase; letter-spacing: .04em; color: var(--text-secondary); margin: 14px 0 6px; }
  .key { display: grid; grid-template-columns: 40px 1fr; gap: 4px 8px; align-items: center; }
  .swatch { height: 0; border-top: 3px solid; width: 34px; }
  #detail { background: var(--surface-2); border-radius: 6px; padding: 10px; min-height: 60px; }
  #detail blockquote { margin: 6px 0; padding-left: 8px; border-left: 3px solid var(--rule); font-style: italic; }
  .muted { color: var(--text-muted); }
  #tip { position: fixed; pointer-events: none; background: var(--surface-1); border: 1px solid var(--rule);
         border-radius: 4px; padding: 4px 8px; font-size: 12px; display: none; box-shadow: 0 2px 6px rgba(0,0,0,.12); }
  section.table { padding: 8px 16px 24px; }
  table { border-collapse: collapse; width: 100%; font-size: 12px; }
  th, td { text-align: left; padding: 4px 6px; border-bottom: 1px solid var(--rule); vertical-align: top; }
  th { color: var(--text-secondary); font-weight: 600; }
</style>
</head>
<body>
<div class="viz-root">
<header>
  <h1>Seasonal herding in the Himachal hills, 1881–1961: knowledge graph of sourced claims</h1>
  <div class="filters">
    <label>Conjuncture <select id="f-conj"><option value="">All</option></select></label>
    <label>Valley <select id="f-valley"><option value="">All</option></select></label>
    <label>Source layer <select id="f-layer"><option value="">All</option></select></label>
    <label>Evidence <select id="f-ev">
      <option value="">All claims in the graph</option>
      <option value="auto">Quote verified on the page</option>
      <option value="ai_checked">AI checker: supported</option>
      <option value="human">Signed off by a person</option></select></label>
    <span id="f-fam"></span>
    <span class="muted" id="count"></span>
  </div>
</header>
<main>
  <div id="cy"></div>
  <aside>
    <h2>Selected claim</h2>
    <div id="detail"><span class="muted">Click an edge to see its quote, source and page. Click a node to show only its claims.</span></div>
    <h2>Relations (edges)</h2>
    <div class="key" id="edge-key"></div>
    <h2>Entities (nodes)</h2>
    <div class="key" id="node-key"></div>
    <p class="muted">Faint edges are figures typed from page images that no one has signed off yet. Dashed node borders mark names not yet in data/entities.csv.</p>
  </aside>
</main>
<section class="table">
  <h2 style="font-size:14px">Visible claims (table view)</h2>
  <table><thead><tr><th>Subject</th><th>Relation</th><th>Object</th><th>Resource</th><th>Qty</th><th>Place</th><th>Conjuncture</th><th>Source, PDF page</th><th>Evidence</th></tr></thead>
  <tbody id="rows"></tbody></table>
</section>
<div id="tip"></div>
</div>
<script>
const ELEMENTS = __ELEMENTS__;
const STYLE = __STYLE__;
const CONJ = __CONJUNCTURES__;
const FAMILIES = __FAMILIES__;
const VALLEYS = __VALLEYS__;
const LAYERS = __LAYERS__;
const FAMILY_KEY = {
  movement: ["var(--movement)", "dashed", "movement and season"],
  extraction: ["var(--extraction)", "solid", "extraction: fees, dues, auctions, permits, interest"],
  property: ["var(--property)", "solid", "property: ownership and rights"],
  exchange: ["var(--neutral)", "dotted", "exchange: trade, fairs, sales"],
  labour: ["var(--neutral)", "dashed", "labour: hiring and wage work"],
  geography: ["var(--light)", "solid", "geography: rivers and regions"],
  event: ["var(--light)", "solid", "affected by an event"],
  voice: ["var(--light)", "solid", "direct speech"],
};
const G = 'fill="#f0efec" stroke="#52514e" stroke-width="1.5"';
const NODE_KEY = [
  [`<circle cx="12" cy="9" r="7" ${G}/>`, "place"],
  [`<rect x="2" y="3" width="20" height="12" rx="5" ${G} stroke-width="3"/>`, "river"],
  [`<rect x="3" y="3" width="18" height="12" rx="3" ${G}/>`, "group (caste, tribe)"],
  [`<polygon points="3,3 16,3 21,9 16,15 3,15" ${G}/>`, "person"],
  [`<polygon points="12,1 21,9 12,17 3,9" ${G}/>`, "role"],
  [`<polygon points="7,2 17,2 22,9 17,16 7,16 2,9" ${G} stroke-width="2.5"/>`, "authority"],
  [`<polygon points="12,2 21,16 3,16" ${G} stroke-linejoin="round"/>`, "resource"],
  [`<polygon points="12,1 14.4,6.6 20.5,7.2 15.9,11.2 17.3,17 12,14 6.7,17 8.1,11.2 3.5,7.2 9.6,6.6" ${G}/>`, "event"]];

const cy = cytoscape({ container: document.getElementById("cy"), elements: ELEMENTS, style: STYLE,
  layout: { name: "cose", animate: false, nodeRepulsion: 40000, idealEdgeLength: 110, nodeOverlap: 40,
            componentSpacing: 90, gravity: 0.6, numIter: 2500, randomize: false },
  wheelSensitivity: 0.3 });

const $ = id => document.getElementById(id);
for (const [k, v] of Object.entries(CONJ)) $("f-conj").add(new Option(v, k));
for (const v of VALLEYS) $("f-valley").add(new Option(v, v));
for (const y of LAYERS) $("f-layer").add(new Option(y, y));
$("f-fam").innerHTML = FAMILIES.map(f => `<label><input type="checkbox" value="${f}" checked> ${f}</label>`).join(" ");
$("edge-key").innerHTML = FAMILIES.map(f => {
  const [c, s, t] = FAMILY_KEY[f] || ["var(--light)", "solid", f];
  return `<span class="swatch" style="border-top-color:${c};border-top-style:${s}"></span><span>${t}</span>`; }).join("");
$("node-key").innerHTML = NODE_KEY.map(([svg, t]) => `<svg width="34" height="18" viewBox="0 0 24 18" aria-hidden="true">${svg}</svg><span>${t}</span>`).join("");

const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
const rank = { ai_rejected: -1, image_unverified: 0, auto: 1, ai_partly: 1, ai_checked: 2, human: 3 };
let focus = null;

function apply() {
  const conj = $("f-conj").value, valley = $("f-valley").value, layer = $("f-layer").value, ev = $("f-ev").value;
  const fams = new Set([...document.querySelectorAll("#f-fam input:checked")].map(i => i.value));
  const shown = [];
  cy.batch(() => {
    cy.edges().forEach(e => {
      const d = e.data();
      const ok = (!conj || d.conjuncture === conj) && (!valley || d.valley === valley) &&
        (!layer || String(d.layer_year) === layer) && (!ev || rank[d.evidence] >= rank[ev]) &&
        fams.has(d.family) && (!focus || d.source_node === focus || d.target_node === focus || e.source().id() === focus || e.target().id() === focus);
      e.style("display", ok ? "element" : "none");
      if (ok) shown.push(e);
    });
    cy.nodes().forEach(n => n.style("display", n.connectedEdges().some(e => e.style("display") === "element") ? "element" : "none"));
  });
  $("count").textContent = `${shown.length} claims shown`;
  $("rows").innerHTML = shown.map(e => { const d = e.data();
    return `<tr><td>${esc(e.source().data("label"))}</td><td>${esc(d.predicate)}</td><td>${esc(e.target().data("label"))}</td><td>${esc(d.resource)}</td>
      <td>${esc(d.qty)} ${esc(d.unit)}</td><td>${esc(d.place)}</td><td>${esc(d.conjuncture)}</td>
      <td>${esc(d.source)}, p. ${d.pdf_page}</td><td>${esc(d.evidence)}</td></tr>`; }).join("");
}

function showEdge(e) {
  const d = e.data();
  $("detail").innerHTML = `<strong>${esc(e.source().data("label"))}</strong> ${esc(d.predicate)} <strong>${esc(e.target().data("label"))}</strong>
    ${d.resource ? `<div>Resource: ${esc(d.resource)}</div>` : ""}
    ${d.qty !== "" ? `<div>${esc(d.qty)} ${esc(d.unit)}</div>` : ""}
    <blockquote>${esc(d.quote)}</blockquote>
    <div>${esc(d.source)}, PDF page ${d.pdf_page} (${d.layer_year})</div>
    ${d.place ? `<div>Place: ${esc(d.place)}</div>` : ""}
    ${d.months ? `<div>Months: ${esc(d.months.split("|").join(", "))}</div>` : ""}
    <div>When: ${esc(d.when)}${d.date_text ? ` (${esc(d.date_text)})` : ""}</div>
    <div>Conjuncture: ${esc(CONJ[d.conjuncture])}</div>
    ${d.note ? `<div class="muted">Note: ${esc(d.note)}</div>` : ""}
    ${d.ai_verdict ? `<div>AI check: <strong>${esc(d.ai_verdict.replace("_", " "))}</strong>. <span class="muted">${esc(d.ai_reason)}</span></div>` : ""}
    <div class="muted">Evidence: ${esc(d.evidence)}; quote match: ${esc(d.quote_match)}${d.verified_by ? `; signed off by ${esc(d.verified_by)}` : ""}</div>`;
}

cy.on("tap", "edge", ev => showEdge(ev.target));
cy.on("tap", "node", ev => { focus = focus === ev.target.id() ? null : ev.target.id(); apply(); });
cy.on("tap", ev => { if (ev.target === cy && focus) { focus = null; apply(); } });
const tip = $("tip");
cy.on("mouseover", "edge", ev => { const e = ev.target; e.addClass("hover");
  tip.innerHTML = `${esc(e.source().data("label"))} → ${esc(e.data("predicate"))} → ${esc(e.target().data("label"))}<br><span class="muted">${esc(e.data("source"))}, p. ${e.data("pdf_page")}</span>`;
  tip.style.display = "block"; });
cy.on("mouseover", "node", ev => { tip.innerHTML = `${esc(ev.target.data("label"))} <span class="muted">(${esc(ev.target.data("type"))}, ${ev.target.data("degree")} claims)</span>`; tip.style.display = "block"; });
cy.on("mouseout", "edge, node", ev => { ev.target.removeClass("hover"); tip.style.display = "none"; });
document.addEventListener("mousemove", ev => { tip.style.left = ev.clientX + 12 + "px"; tip.style.top = ev.clientY + 12 + "px"; });
document.querySelectorAll("select, #f-fam input").forEach(el => el.addEventListener("change", apply));
apply();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
