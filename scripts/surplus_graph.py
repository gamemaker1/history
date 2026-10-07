#!/usr/bin/env python3
"""Who takes a share of whose product: the flows of fees, dues, interest, labour and produce, by conjuncture.

Reads analysis/graph/edges.csv and nodes.csv (build_graph.py) and keeps the
relations through which one party gives up part of its product or labour to
another. Each is turned into a directed flow from the party who gives to the
party who receives:

  COLLECTS_FEE_FROM   A collects from B      flow B -> A   fee or tax
  PAYS_DUES_TO        A pays B               flow A -> B   dues, revenue or begar
  LENDS_TO            A lends to B           flow B -> A   interest
  HIRES               A hires B              flow B -> A   labour
  AUCTIONS_RIGHT_TO   A sells a right to B   flow B -> A   price of a right
  ISSUES_PERMIT_TO    A issues to B          flow B -> A   permit (and its fee)
  SELLS_TO            A sells to B           flow A -> B   produce sold
  BUYS_FROM           A buys from B          flow B -> A   produce sold

Actors are the graph's entities with the village scoping removed (the
Rajputs of every village become "Rajput"), so the periods can be compared.
For each conjuncture the script counts, per actor, how many distinct parties
pay into it and how many claims say so, and it lists which relations
(giver type, receiver type, kind) appear in one conjuncture and not another.
This is the Marxist step of the plan: the change in who takes from whom.

Outputs in analysis/surplus/:
  flows.csv              one row per claim: giver, receiver, kind, conjuncture, source, page
  actors.csv             per conjuncture and actor: parties paying in and out, claims
  relations.csv          relation x conjuncture matrix (claims), for reading change
  surplus.html           one Cytoscape.js panel per conjuncture, same layout in each
  surplus_<conj>.cyjs    each panel for Cytoscape Desktop

Usage (from the project folder):
  .venv/bin/python scripts/surplus_graph.py
  .venv/bin/python scripts/surplus_graph.py --evidence ai     # only AI-checked or signed-off claims

Needs pandas and networkx. Based on the Programming Historian lesson
"Exploring and Analyzing Network Data with Python" (degree, in- and out-flows).
"""

import argparse
import json

import networkx as nx
import pandas as pd

from corpus import ANALYSIS, ROOT

GRAPH = ANALYSIS / "graph"
OUT = ANALYSIS / "surplus"

FLOW = {  # predicate: (reverse?, kind)
    "COLLECTS_FEE_FROM": (True, "fee or tax"),
    "PAYS_DUES_TO": (False, "dues, revenue or begar"),
    "LENDS_TO": (True, "interest"),
    "HIRES": (True, "labour"),
    "AUCTIONS_RIGHT_TO": (True, "price of a right"),
    "ISSUES_PERMIT_TO": (True, "permit"),
    "SELLS_TO": (False, "produce sold"),
    "BUYS_FROM": (True, "produce sold"),
}
PANELS = ["two_sovereigns", "princely_pastures", "forest_department", "trade_and_credit", "roads_and_wages"]
TITLES = {
    "two_sovereigns": "Two sovereigns, c. 1846 to 1947",
    "princely_pastures": "The rulers' pastures, to about 1950",
    "forest_department": "The Forest Department, 1948 to 1961",
    "trade_and_credit": "Trade and credit, to the early 1960s",
    "roads_and_wages": "Roads and wages, 1950s to 1961",
}
KIND_COLOUR = {  # categorical slots 1 to 3 for the three surplus kinds the argument turns on; the rest neutral
    "fee or tax": "#eb6834", "dues, revenue or begar": "#eb6834", "price of a right": "#eb6834", "permit": "#eb6834",
    "interest": "#2a78d6", "labour": "#1baf7a", "produce sold": "#52514e",
}
LEVEL = {"ai_rejected": -1, "image_unverified": 0, "auto": 1, "ai_partly": 1, "ai_checked": 2, "human": 3}


def load(min_evidence):
    edges = pd.read_csv(GRAPH / "edges.csv", dtype=str).fillna("")
    nodes = pd.read_csv(GRAPH / "nodes.csv", dtype=str).fillna("")
    floor = {"all": 0, "auto": 1, "ai": 2, "human": 3}[min_evidence]
    edges = edges[edges.evidence.map(LEVEL) >= floor]
    return edges, nodes


def flows(edges, nodes):
    base = dict(zip(nodes.label, nodes.base_id))
    label_of = nodes.drop_duplicates("base_id").set_index("base_id").label.str.replace(r" \(.*\)$", "", regex=True)
    type_of = dict(zip(nodes.base_id, nodes.type))
    rows = []
    for e in edges[edges.predicate.isin(list(FLOW))].itertuples():
        reverse, kind = FLOW[e.predicate]
        s, o = base.get(e.subject, e.subject), base.get(e.object, e.object)
        giver, receiver = (o, s) if reverse else (s, o)
        if giver == receiver:
            continue
        rows.append({"conjuncture": e.conjuncture, "giver": giver, "giver_label": label_of.get(giver, giver),
                     "receiver": receiver, "receiver_label": label_of.get(receiver, receiver),
                     "giver_type": type_of.get(giver, ""), "receiver_type": type_of.get(receiver, ""),
                     "kind": kind, "predicate": e.predicate, "resource": e.resource, "qty": e.qty, "unit": e.unit,
                     "place": e.place, "valley": e.valley, "source": e.source, "pdf_page": e.pdf_page,
                     "evidence": e.evidence, "claim_id": e.claim_id, "quote": e.quote})
    return pd.DataFrame(rows)


def actors(f):
    rows = []
    for conj, g in f.groupby("conjuncture"):
        for actor in set(g.giver) | set(g.receiver):
            inn, out = g[g.receiver == actor], g[g.giver == actor]
            rows.append({"conjuncture": conj, "actor": actor,
                         "label": (inn.receiver_label.tolist() + out.giver_label.tolist())[0],
                         "parties_paying_in": inn.giver.nunique(), "claims_in": len(inn),
                         "parties_paid_to": out.receiver.nunique(), "claims_out": len(out),
                         "kinds_in": "; ".join(sorted(set(inn.kind)))})
    a = pd.DataFrame(rows)
    return a.sort_values(["conjuncture", "claims_in"], ascending=[True, False])


def relations(f):
    r = f.assign(relation=f.giver_label + " -> " + f.receiver_label + " (" + f.kind + ")")
    m = r.pivot_table(index="relation", columns="conjuncture", values="claim_id", aggfunc="count", fill_value=0)
    m["conjunctures"] = (m > 0).sum(axis=1)
    m["total"] = m.drop(columns="conjunctures").sum(axis=1)
    return m.sort_values("total", ascending=False)


def panel_elements(f, conj, pos, top):
    g = f[f.conjuncture == conj]
    weight = g.groupby(["giver", "receiver", "kind"]).size().reset_index(name="claims")
    degree = pd.concat([weight.groupby("giver").claims.sum(), weight.groupby("receiver").claims.sum()]).groupby(level=0).sum()
    keep = set(degree.sort_values(ascending=False).head(top).index)
    weight = weight[weight.giver.isin(keep) & weight.receiver.isin(keep)]
    labels = dict(zip(g.giver, g.giver_label)) | dict(zip(g.receiver, g.receiver_label))
    types = dict(zip(g.giver, g.giver_type)) | dict(zip(g.receiver, g.receiver_type))
    received = weight.groupby("receiver").claims.sum()
    els = []
    for n in sorted(set(weight.giver) | set(weight.receiver)):
        x, y = pos.get(n, (0, 0))
        els.append({"data": {"id": n, "label": labels.get(n, n), "type": types.get(n, ""),
                             "received": int(received.get(n, 0))},
                    "position": {"x": x, "y": y}})
    for r in weight.itertuples():
        els.append({"data": {"id": f"{conj}:{r.giver}>{r.receiver}:{r.kind}", "source": r.giver, "target": r.receiver,
                             "kind": r.kind, "claims": int(r.claims), "colour": KIND_COLOUR.get(r.kind, "#52514e")}})
    return els


def shared_layout(f, top):
    """One spring layout over every panel's actors, so an actor sits in the same place in each panel."""
    g = nx.Graph()
    for conj in PANELS:
        sub = f[f.conjuncture == conj]
        w = sub.groupby(["giver", "receiver"]).size()
        deg = pd.concat([sub.groupby("giver").size(), sub.groupby("receiver").size()]).groupby(level=0).sum()
        keep = set(deg.sort_values(ascending=False).head(top).index)
        for (a, b), n in w.items():
            if a in keep and b in keep:
                g.add_edge(a, b, weight=g.get_edge_data(a, b, {"weight": 0})["weight"] + n)
    pos = nx.spring_layout(g, k=1.6 / max(len(g), 1) ** 0.5, weight="weight", seed=7, iterations=300)
    return {n: (float(x) * 420, float(y) * 300) for n, (x, y) in pos.items()}


def write_html(f, pos, top):
    panels = {c: panel_elements(f, c, pos, top) for c in PANELS if (f.conjuncture == c).any()}
    for c, els in panels.items():
        (OUT / f"surplus_{c}.cyjs").write_text(json.dumps({"elements": els}, ensure_ascii=False, indent=1),
                                               encoding="utf-8")
    html = HTML.replace("__PANELS__", json.dumps(panels, ensure_ascii=False)) \
        .replace("__TITLES__", json.dumps(TITLES)) \
        .replace("__COUNTS__", json.dumps(f.groupby("conjuncture").size().to_dict()))
    (OUT / "surplus.html").write_text(html, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--evidence", choices=["all", "auto", "ai", "human"], default="all")
    ap.add_argument("--top", type=int, default=18, help="actors shown per panel (by number of flow claims)")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)

    edges, nodes = load(args.evidence)
    f = flows(edges, nodes)
    f.to_csv(OUT / "flows.csv", index=False)
    a = actors(f)
    a.to_csv(OUT / "actors.csv", index=False)
    r = relations(f)
    r.to_csv(OUT / "relations.csv")
    write_html(f, shared_layout(f, args.top), args.top)

    print(f"{len(f)} flow claims (evidence: {args.evidence}) written to {OUT.relative_to(ROOT)}/")
    print("  by conjuncture: " + ", ".join(f"{k} {v}" for k, v in f.conjuncture.value_counts().items()))
    print("  by kind: " + ", ".join(f"{k} {v}" for k, v in f.kind.value_counts().items()))
    for conj in PANELS:
        top = a[a.conjuncture == conj].head(4)
        if len(top):
            print(f"  {conj}: main receivers " + "; ".join(
                f"{t.label} ({t.claims_in} claims from {t.parties_paying_in} parties: {t.kinds_in})" for t in top.itertuples()))


HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Who takes from whom: flows of surplus by conjuncture</title>
<script src="https://unpkg.com/cytoscape@3/dist/cytoscape.min.js"></script>
<style>
  .viz-root { color-scheme: light; --surface-1: #fcfcfb; --rule: #dcdbd6; --ink: #0b0b0b; --ink2: #52514e;
              background: var(--surface-1); color: var(--ink); font: 14px/1.4 system-ui, sans-serif; padding: 12px 16px; }
  body { margin: 0; }
  h1 { font-size: 17px; margin: 0 0 4px; }
  p.lede { margin: 0 0 10px; color: var(--ink2); font-size: 13px; }
  .key { display: flex; flex-wrap: wrap; gap: 6px 18px; font-size: 13px; margin-bottom: 10px; }
  .sw { display: inline-block; width: 28px; border-top: 3px solid; vertical-align: middle; margin-right: 6px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(560px, 1fr)); gap: 12px; }
  .panel { border: 1px solid var(--rule); border-radius: 6px; background: var(--surface-1); }
  .panel h2 { font-size: 14px; margin: 8px 10px 0; }
  .panel .n { font-weight: normal; color: var(--ink2); font-size: 12px; }
  .cy { height: 430px; }
  #tip { position: fixed; pointer-events: none; background: var(--surface-1); border: 1px solid var(--rule);
         border-radius: 4px; padding: 4px 8px; font-size: 12px; display: none; }
</style>
</head>
<body>
<div class="viz-root">
  <h1>Who takes a share of whose product: flows of surplus in each conjuncture</h1>
  <p class="lede">Arrows run from the party who gives up product, labour or money to the party who receives it. Line width is the number of sourced claims. Each actor sits in the same place in every panel, so relations that appear or vanish between periods can be compared by eye. Node size is the number of claims flowing in.</p>
  <div class="key">
    <span><span class="sw" style="border-color:#eb6834"></span>fees, taxes, dues, begar, permits, rights sold</span>
    <span><span class="sw" style="border-color:#2a78d6"></span>interest</span>
    <span><span class="sw" style="border-color:#1baf7a"></span>labour</span>
    <span><span class="sw" style="border-color:#52514e;border-top-style:dotted"></span>produce sold</span>
  </div>
  <div class="grid" id="grid"></div>
  <div id="tip"></div>
</div>
<script>
const PANELS = __PANELS__, TITLES = __TITLES__, COUNTS = __COUNTS__;
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
const tip = document.getElementById("tip");
document.addEventListener("mousemove", e => { tip.style.left = e.clientX + 12 + "px"; tip.style.top = e.clientY + 12 + "px"; });
const style = [
  { selector: "node", style: { "label": "data(label)", "font-size": 10, "color": "#0b0b0b", "text-valign": "bottom",
      "text-margin-y": 3, "text-wrap": "wrap", "text-max-width": 90, "background-color": "#f0efec",
      "border-width": 1.5, "border-color": "#52514e",
      "width": "mapData(received, 0, 20, 14, 40)", "height": "mapData(received, 0, 20, 14, 40)" } },
  { selector: "node[type = 'authority']", style: { "shape": "hexagon", "border-width": 2.5 } },
  { selector: "node[type = 'role']", style: { "shape": "diamond" } },
  { selector: "node[type = 'group']", style: { "shape": "round-rectangle" } },
  { selector: "node[type = 'person']", style: { "shape": "tag" } },
  { selector: "edge", style: { "curve-style": "bezier", "target-arrow-shape": "triangle", "arrow-scale": 0.9,
      "line-color": "data(colour)", "target-arrow-color": "data(colour)", "opacity": 0.85,
      "width": "mapData(claims, 1, 12, 1.5, 7)" } },
  { selector: "edge[kind = 'produce sold']", style: { "line-style": "dotted" } },
];
for (const [conj, els] of Object.entries(PANELS)) {
  const div = document.createElement("div"); div.className = "panel";
  div.innerHTML = `<h2>${esc(TITLES[conj])} <span class="n">(${COUNTS[conj] || 0} flow claims)</span></h2><div class="cy"></div>`;
  document.getElementById("grid").appendChild(div);
  const cy = cytoscape({ container: div.querySelector(".cy"), elements: els, style, layout: { name: "preset", fit: true, padding: 30 },
                         userZoomingEnabled: true, wheelSensitivity: 0.3 });
  cy.on("mouseover", "edge", e => { const d = e.target.data();
    tip.innerHTML = `${esc(e.target.source().data("label"))} → ${esc(e.target.target().data("label"))}<br>${esc(d.kind)}, ${d.claims} claim(s)`;
    tip.style.display = "block"; });
  cy.on("mouseover", "node", e => { tip.innerHTML = `${esc(e.target.data("label"))}: ${e.target.data("received")} claim(s) flowing in`; tip.style.display = "block"; });
  cy.on("mouseout", "edge, node", () => { tip.style.display = "none"; });
}
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
