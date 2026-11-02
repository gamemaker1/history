#!/usr/bin/env python3
"""Build essay/evidence/evidence.md, the evidence file for the essay outline.

Reads the template essay/evidence/evidence.src.md and replaces two kinds of
placeholder. A line "{{snippets 3.1}}" is replaced by every snippet of item 3.1
in data/evidence_snippets.csv, as quotations with their source and PDF page.
A line "{{table NAME}}" is replaced by a Markdown table computed from the data
and analysis files, so that every number in the evidence file comes from a
file in the repository.

Every snippet is checked against the OCR text of its page with the matcher of
scripts/check_essay.py. The results go to analysis/evidence/snippet_check.csv,
and the script stops if a snippet is not found on its page. A page that also
appears in a copied passage of the text-reuse search (analysis/text_reuse/
passages.csv) is marked in the citation.

Usage (from the project folder):
  .venv/bin/python scripts/build_evidence.py
"""

import csv
import re
import sys

import pandas as pd

from build_sources_pdf import title_of
from check_essay import PageCache, match_quote
from corpus import ANALYSIS, DATA, ROOT, TEXT, page_text

SRC = ROOT / "essay" / "evidence" / "evidence.src.md"
OUT = ROOT / "essay" / "evidence" / "evidence.md"
CHECK = ANALYSIS / "evidence" / "snippet_check.csv"
ATLAS = TEXT / "1961" / "1961 Punjab Census Atlas.txt"
READINGS = {
    "braudel": ("Braudel, \"History and the Social Sciences\"",
                "Braudel, Fernand. \"History and the Social Sciences: The Longue Durée.\" Translated by Immanuel "
                "Wallerstein. *Review (Fernand Braudel Center)* 32, no. 2 (2009): 171-203."),
    "ladurie": ("Le Roy Ladurie, \"The History of Rain and Fine Weather\"",
                "Le Roy Ladurie, Emmanuel. \"The History of Rain and Fine Weather.\" In *French Studies in History*, "
                "vol. 1, *The Inheritance*, 192-214."),
    "aymard": ("Aymard, \"The Cost of War\"",
               "Aymard, Maurice. \"The Cost of War.\" In *French Studies in History*, vol. 2, *Departures*, 418-427."),
    "bloch": ("Bloch, *The Historian's Craft*",
              "Bloch, Marc. *The Historian's Craft*. Translated by Peter Putnam. New York: Vintage, 1953. Chapter III, "
              "\"Historical Criticism.\""),
    "alam": ("Alam, \"Marxist History\" lecture slides",
             "Alam, Aniket. \"Marxist History.\" Lectures 8 to 10, Introduction to History (HS3.201), IIIT "
             "Hyderabad, Monsoon 2026."),
    "british-rule": ("Marx, \"The British Rule in India\"",
                     "Marx, Karl. \"The British Rule in India.\" *New-York Daily Tribune*, June 25, 1853."),
    "future-results": ("Marx, \"The Future Results of British Rule in India\"",
                       "Marx, Karl. \"The Future Results of British Rule in India.\" *New-York Daily Tribune*, "
                       "August 8, 1853."),
    "manifesto": ("Marx and Engels, *Manifesto of the Communist Party*",
                  "Marx, Karl, and Friedrich Engels. *Manifesto of the Communist Party*. Excerpt, pp. 14-21."),
    "habib": ("Habib, \"Potentialities of Capitalistic Development\"",
              "Habib, Irfan. \"Potentialities of Capitalistic Development in the Economy of Mughal India.\" "
              "*Journal of Economic History* 29, no. 1 (1969): 32-78."),
    "kosambi": ("Kosambi, \"Social and Economic Aspects of the Bhagavad Gita\"",
                "Kosambi, D. D. \"Social and Economic Aspects of the Bhagavad Gita.\" *Journal of the Economic and "
                "Social History of the Orient* 4, no. 2 (1961): 198-224."),
}
SHORT = {
    "1881": "1881 census", "1931": "1931 census", "Rose": "Rose, vol. 2", "Rose Vol1": "Rose, vol. 1",
    "Newell": "Newell", "Atlas": "Punjab Census Atlas", "Mahasu": "Mahasu handbook", "Weaving": "Weaving survey",
}


class Pages(PageCache):
    """PageCache that also serves the 1961 Punjab Census Atlas."""

    def page(self, source, n):
        if source == "Atlas":
            return page_text(ATLAS, n)
        return super().page(source, n)


def cite(source, page):
    name = SHORT.get(source, f"{source} survey")
    return f"{name}, PDF p. {page}"


def snippets():
    cache = Pages()
    reuse = pd.read_csv(ANALYSIS / "text_reuse" / "passages.csv")
    copied = {(s, int(p)): e for s, p, e in zip(reuse.later_source, reuse.later_page, reuse.earlier_source)}
    with open(DATA / "evidence_snippets.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    results, blocks, failed = [], {}, 0
    for r in rows:
        page = int(r["pdf_page"])
        kind, score, _ = match_quote(cache, r["source"], page, r["quote"], 0.85)
        failed += kind == "none"
        results.append({**r, "match": kind, "score": round(score, 3)})
        note = f" Part of this page repeats {copied[(r['source'], page)]}." if (r["source"], page) in copied else ""
        blocks.setdefault(r["item"], []).append(f"> \"{r['quote']}\"\n> ({cite(r['source'], page)}.{note})\n")
    CHECK.parent.mkdir(parents=True, exist_ok=True)
    with open(CHECK, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0]))
        w.writeheader()
        w.writerows(results)
    for r in results:
        if r["match"] == "none":
            print(f"  [NOT FOUND] {r['source']} p. {r['pdf_page']} (best {r['score']}): {r['quote'][:100]}")
    print(f"snippets found on their page: {len(results) - failed} of {len(results)}")
    if failed:
        sys.exit(1)
    return {k: "\n".join(v) for k, v in blocks.items()}


def md(df):
    df = df.astype(object).where(df.notna(), "")
    head = "| " + " | ".join(df.columns) + " |"
    rule = "| " + " | ".join("---" for _ in df.columns) + " |"
    body = ["| " + " | ".join(str(v) for v in row) + " |" for row in df.itertuples(index=False)]
    return "\n".join([head, rule] + body)


def t_pipeline():
    pages61 = pd.read_csv(ANALYSIS / "candidate_pages.csv")
    pagescol = pd.read_csv(ANALYSIS / "candidate_pages_colonial.csv")
    with open(DATA / "claims_raw.jsonl", encoding="utf-8") as f:
        proposed = sum(1 for line in f if line.strip())
    claims = pd.read_csv(DATA / "claims.csv")
    rejected = pd.read_csv(ANALYSIS / "claims_rejected.csv")
    checks = pd.read_csv(DATA / "claim_checks.csv").verdict.value_counts()
    nodes = pd.read_csv(ANALYSIS / "graph" / "nodes.csv")
    edges = pd.read_csv(ANALYSIS / "graph" / "edges.csv")
    reuse = pd.read_csv(ANALYSIS / "text_reuse" / "passages.csv")
    kind = claims.extracted_by.str.split(" ").str[0].str.rstrip(":")
    rows = [
        ("1", "Pages of the 1961 volumes scored by herding vocabulary", len(pages61)),
        ("1", "Pages of the 1961 volumes selected", int(pages61.selected.sum())),
        ("1", "Pages of the 1881, Rose and 1931 volumes scored", len(pagescol)),
        ("1", "Pages of the 1881, Rose and 1931 volumes selected", int(pagescol.selected.sum())),
        ("2", "Claims proposed by the language model", proposed),
        ("3", "Claims rejected because the quotation is not on the cited page", len(rejected)),
        ("4", "Claims entered from livestock tables read from page images", int((kind == "image").sum())),
        ("4", "Claims entered by hand", int((kind == "manual").sum())),
        ("5", "Claims kept in the evidence graph", len(claims)),
        ("6", "Second model check: supported", int(checks.get("supported", 0))),
        ("6", "Second model check: partly supported", int(checks.get("partly_supported", 0))),
        ("6", "Second model check: not supported (left out of every analysis)", int(checks.get("not_supported", 0))),
        ("6", "Second model check: unclear", int(checks.get("unclear", 0))),
        ("7", "Nodes in the graph used for the analyses", len(nodes)),
        ("7", "Edges in the graph used for the analyses", len(edges)),
        ("8", "Copied passages of twelve or more words between sources", len(reuse)),
    ]
    return md(pd.DataFrame(rows, columns=["Step", "Quantity", "Count"]))


def t_reuse():
    p = pd.read_csv(ANALYSIS / "text_reuse" / "pairs.csv").head(8)
    return md(p.rename(columns={"later_source": "Later source", "earlier_source": "Earlier source",
                                "passages": "Copied passages", "words": "Copied words"}))


def villages():
    return pd.read_csv(ANALYSIS / "geography" / "villages.csv")


def t_altitude():
    v = villages().sort_values("altitude_m", ascending=False)
    v = v[["village", "river_system", "altitude_m", "altitude_basis", "households", "sheep_and_goats",
           "per_household"]]
    v["altitude_m"] = v.altitude_m.round().astype("Int64")
    v["households"] = v.households.astype("Int64")
    v["sheep_and_goats"] = v.sheep_and_goats.astype("Int64")
    return md(v.rename(columns={"village": "Village", "river_system": "River system", "altitude_m": "Altitude (m)",
                                "altitude_basis": "Altitude from", "households": "Households",
                                "sheep_and_goats": "Sheep and goats", "per_household": "Per household"}))


def t_persistence():
    p = pd.read_csv(ANALYSIS / "calendar" / "persistence.csv")
    p = p[p.group.isin(["Gaddi", "Gujjar"]) & p.destination_class.isin(["winter grounds", "summer pastures"])]
    return md(p[["group", "destination_class", "source_years", "months_named", "sources"]].rename(columns={
        "group": "Group", "destination_class": "Movement to", "source_years": "Years of the sources",
        "months_named": "Months named", "sources": "Pages"}))


def t_low_high():
    v = villages().set_index("village").loc[["Brahmaur", "Bir", "Batal", "Shakrori"]].reset_index()
    v["households"] = v.households.astype("Int64")
    v["sheep_and_goats"] = v.sheep_and_goats.astype("Int64")
    v["altitude_m"] = v.altitude_m.round().astype("Int64")
    return md(v[["village", "altitude_m", "households", "sheep_and_goats", "per_household"]].rename(columns={
        "village": "Village", "altitude_m": "Altitude (m)", "households": "Households",
        "sheep_and_goats": "Sheep and goats", "per_household": "Per household"}))


def t_trade():
    t = pd.read_csv(ANALYSIS / "term_rates_herding.csv")
    t = t[t.village.isin(["Kanum", "Kothi", "Nachar", "Brahmaur", "Chitrari", "Devi-Kothi", "Maingal", "Kupha"])]
    t = t.sort_values("trade_per_10k", ascending=False)
    valley = villages().set_index("village").river_system
    t["river"] = t.village.map(valley).fillna("Chenab")
    return md(t[["village", "river", "trade_per_10k", "flocks_per_10k", "debt_per_10k"]].rename(columns={
        "village": "Village survey", "river": "River system", "trade_per_10k": "Trade words per 10,000",
        "flocks_per_10k": "Flock words per 10,000", "debt_per_10k": "Debt words per 10,000"}))


def t_class():
    g = pd.read_csv(ANALYSIS / "flocks" / "by_group.csv")
    g = g[g.source_kind == "table"]
    s = g.groupby("class").sheep_and_goats.sum().sort_values(ascending=False)
    out = pd.DataFrame({"Caste class": s.index, "Sheep and goats": s.astype(int).values,
                        "Share (%)": (100 * s / s.sum()).round(1).values})
    total = pd.DataFrame([{"Caste class": "all caste tables", "Sheep and goats": int(s.sum()), "Share (%)": 100.0}])
    return md(pd.concat([out, total]))


def t_villages_owners():
    v = pd.read_csv(ANALYSIS / "flocks" / "village_summary.csv").dropna(subset=["landholding_pct"])
    v = v.sort_values(["river_system", "sheep_and_goats"], ascending=[True, False])
    v["sheep_and_goats"] = v.sheep_and_goats.astype(int)
    return md(v[["village", "river_system", "pdf_page", "sheep_and_goats", "landholding_pct", "scheduled caste_pct",
                 "top_group"]].rename(columns={
        "village": "Village", "river_system": "River system", "pdf_page": "PDF page",
        "sheep_and_goats": "Sheep and goats", "landholding_pct": "Landholding castes (%)",
        "scheduled caste_pct": "Scheduled castes (%)", "top_group": "Largest owning group"}))


def t_brahmaur():
    g = pd.read_csv(ANALYSIS / "flocks" / "by_group.csv")
    g = g[g.village == "Brahmaur"]
    out = g[["group", "households_in_group", "hh_owning_flock", "sheep_and_goats"]].copy()
    out.loc[len(out)] = ["total", g.households_in_group.sum(), g.hh_owning_flock.sum(), g.sheep_and_goats.sum()]
    for c in out.columns[1:]:
        out[c] = out[c].astype(int)
    return md(out.rename(columns={"group": "Caste", "households_in_group": "Households",
                                  "hh_owning_flock": "Households owning sheep or goats",
                                  "sheep_and_goats": "Sheep and goats"}))


def t_rates():
    r = pd.read_csv(ANALYSIS / "fees" / "rates.csv")
    return md(r[["year", "place", "collector", "animal", "rate_as_printed", "rupees", "per", "source", "pdf_page"]]
              .rename(columns={"year": "Year", "place": "Place", "collector": "Collector", "animal": "Animal",
                               "rate_as_printed": "Rate as printed", "rupees": "Rupees", "per": "Per",
                               "source": "Source", "pdf_page": "PDF page"}))


def t_series():
    s = pd.read_csv(ANALYSIS / "fees" / "series.csv")
    return md(s[["year", "sheep", "goats", "total", "total_change_pct", "remark"]].rename(columns={
        "year": "Year", "sheep": "Sheep", "goats": "Goats", "total": "Total",
        "total_change_pct": "Change since 1952-53 (%)", "remark": "Remark on the page"}))


def t_phases():
    p = pd.read_csv(ANALYSIS / "fees" / "phases.csv")
    return md(p.rename(columns={"phase": "Phase", "from": "From", "to": "To", "sheep_change_pct": "Sheep (%)",
                                "goats_change_pct": "Goats (%)", "total_change_pct": "Total (%)"}))


def t_flows():
    r = pd.read_csv(ANALYSIS / "surplus" / "relations.csv")
    cols = ["two_sovereigns", "princely_pastures", "forest_department", "roads_and_wages", "trade_and_credit"]
    r = r[r[cols].sum(axis=1) > 0].sort_values("total", ascending=False).head(15)
    return md(r[["relation"] + cols].rename(columns={
        "relation": "Who gives to whom (kind)", "two_sovereigns": "Two sovereigns",
        "princely_pastures": "Raja's pastures", "forest_department": "Forest Department",
        "roads_and_wages": "Roads and wages", "trade_and_credit": "Trade and credit"}))


def readings():
    """Key -> list of (reading, PDF page, quotation) from data/evidence_readings.csv."""
    out = {}
    with open(DATA / "evidence_readings.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["reading"] not in READINGS:
                raise SystemExit(f"unknown reading {r['reading']}")
            out.setdefault(r["key"], []).append((r["reading"], r["pdf_page"], r["quote"]))
    return out


def add_readings(text, quotes):
    """Replace {{R key}} placeholders by the quotations of that key, placed after the line that holds them."""
    used, lines = set(), []
    for line in text.split("\n"):
        keys = re.findall(r"\{\{R ([\w-]+)\}\}", line)
        if not keys:
            lines.append(line)
            continue
        lines.append(re.sub(r"\s*\{\{R [\w-]+\}\}", "", line))
        indent = "  " if line.startswith((" ", "- ")) else ""
        for k in keys:
            if k not in quotes:
                raise SystemExit(f"no reading quotation for key {k}")
            for reading, page, quote in quotes[k]:
                used.add(reading)
                lines += ["", f"{indent}> \"{quote}\" ({READINGS[reading][0]}, PDF p. {page}.)"]
        lines.append("")
    refs = "\n".join(f"- {READINGS[r][1]}" for r in sorted(used, key=lambda r: READINGS[r][1]))
    return "\n".join(lines).replace("{{readings}}", refs)


TABLES = {
    "pipeline": t_pipeline, "reuse": t_reuse, "altitude": t_altitude, "persistence": t_persistence,
    "low_high": t_low_high, "trade": t_trade, "class": t_class, "villages_owners": t_villages_owners,
    "brahmaur": t_brahmaur, "rates": t_rates, "series": t_series, "phases": t_phases, "flows": t_flows,
}


def main():
    blocks = snippets()
    text = SRC.read_text(encoding="utf-8")

    def fill(m):
        kind, key = m.group(1), m.group(2)
        if kind == "snippets":
            if key not in blocks:
                raise SystemExit(f"no snippets for item {key}")
            return blocks[key]
        return TABLES[key]()

    text = re.sub(r"^\{\{(snippets|table) ([\w.]+)\}\}$", fill, text, flags=re.M)
    text = add_readings(text, readings())
    text = re.sub(r"\n{3,}", "\n\n", text)
    OUT.write_text(text, encoding="utf-8")
    print(f"written {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
