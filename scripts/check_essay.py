#!/usr/bin/env python3
"""Check the essay's citations: every quotation on its cited page, every cited page in the evidence graph.

Reads essay/essay.tex and checks three things:

  1. Each \\enquote{...} that precedes a \\src{source}{page} in the same
     sentence is found on that page of the source's text (or on one of the
     pages, for a list), with the same fuzzy match verify_claims.py uses for
     the graph: word for word, or character similarity of at least 0.85 with
     every number present. Quotations before \\srcimg (read from a page image)
     are listed, not checked.
  2. Each cited page holds at least one claim in data/claims.csv (the evidence
     graph), or is a page read from an image (data/flocks.csv,
     data/fee_flocks.csv, data/village_altitudes.csv, data/village_households.csv).
  3. The word count of the essay's body (abstract to conclusion), with detex.

Writes analysis/essay/citation_check.csv and prints a summary. Exits 1 if a
quotation is not found.

Usage (from the project folder):
  python3 scripts/check_essay.py

Standard library only (and the detex program for the word count).
"""

import csv
import re
import subprocess
import sys

from corpus import ANALYSIS, DATA, ROOT
from corpus import tokens
from verify_claims import PageCache, match_quote

ESSAY = ROOT / "essay" / "essay.tex"
CITE = re.compile(r"\\(src|srcimg)\{([^}]*)\}\{([^}]*)\}")
QUOTE = re.compile(r"\\enquote\{((?:[^{}]|\{[^{}]*\})*)\}")


def pages_of(spec):
    out = []
    for part in re.split(r",\s*", spec.replace("~", " ")):
        part = part.strip()
        m = re.match(r"(\d+)\s*(?:--|-)\s*(\d+)$", part)
        if m:
            out += list(range(int(m.group(1)), int(m.group(2)) + 1))
        elif part.isdigit():
            out.append(int(part))
    return out


def plain(tex):
    tex = re.sub(r"\\(?:textonehalf)", "½", tex)
    tex = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", tex)
    tex = tex.replace("\\ ", " ").replace("~", " ").replace("--", "-").replace("\\%", "%").replace("\\&", "&")
    tex = tex.replace("``", '"').replace("''", '"')
    return re.sub(r"\\[a-zA-Z]+", "", tex)


def graph_pages():
    pages = set()
    with open(DATA / "claims.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            pages.add((r["source"], int(r["pdf_page"])))
    for name, scol, pcol in [("flocks.csv", "village", "pdf_page"), ("fee_flocks.csv", "source", "pdf_page"),
                             ("village_altitudes.csv", "village", "pdf_page"),
                             ("village_households.csv", "village", "pdf_page")]:
        with open(DATA / name, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r.get(pcol, "").strip().isdigit():
                    pages.add((r[scol], int(r[pcol])))
    return pages


def main():
    tex = ESSAY.read_text(encoding="utf-8")
    body = tex[tex.index("\\MakeUppercase{Abstract}"):tex.index("\\appendix")]
    cache = PageCache()
    in_graph = graph_pages()
    rows, failed = [], 0
    last = 0
    for m in CITE.finditer(body):
        kind, source, spec = m.groups()
        pages = pages_of(spec)
        # quotations between the previous citation (or sentence start) and this one
        span = body[last:m.start()]
        cut = max(span.rfind(". "), span.rfind(".\n"))
        span = span if cut < 0 else span[cut + 1:]
        last = m.end()
        quotes = [plain(q) for q in QUOTE.findall(span)]
        backed = any((source, p) in in_graph for p in pages)
        if not quotes:
            rows.append({"kind": kind, "source": source, "pages": spec, "quote": "", "match": "no quotation",
                         "score": "", "page_in_graph": backed})
        for q in quotes:
            if kind == "srcimg":
                rows.append({"kind": kind, "source": source, "pages": spec, "quote": q, "match": "image (not checked)",
                             "score": "", "page_in_graph": backed})
                continue
            best = ("none", 0.0, None)
            q_tok = tokens(q)
            for p in pages:
                if len(q_tok) < 3:  # too short for the fuzzy matcher: require the exact words
                    page_tok = " " + " ".join(tokens(cache.page(source, p))) + " "
                    res = ("exact", 1.0, p) if f" {' '.join(q_tok)} " in page_tok else ("none", 0.0, p)
                else:
                    res = match_quote(cache, source, p, q, 0.85)
                if res[0] != "none" or res[1] > best[1]:
                    best = res
                    if res[0] != "none":
                        break
            failed += best[0] == "none"
            rows.append({"kind": kind, "source": source, "pages": spec, "quote": q, "match": best[0],
                         "score": best[1], "page_in_graph": backed})
    out = ANALYSIS / "essay" / "citation_check.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["kind", "source", "pages", "quote", "match", "score", "page_in_graph"])
        w.writeheader()
        w.writerows(rows)

    cites = len(CITE.findall(body))
    quotes = [r for r in rows if r["quote"]]
    checked = [r for r in quotes if r["kind"] == "src"]
    not_in_graph = sorted({(r["source"], r["pages"]) for r in rows if not r["page_in_graph"]})
    words = len(subprocess.run(["detex", "-n"], input=body, capture_output=True, text=True).stdout.split())
    print(f"{cites} citations of primary sources; {len(quotes)} quotations "
          f"({len(checked)} checked against the text, {len(quotes) - len(checked)} read from images)")
    print(f"  quotations found on their page: {len(checked) - failed} of {len(checked)}")
    for r in quotes:
        if r["kind"] == "src" and r["match"] == "none":
            print(f"  [NOT FOUND] {r['source']} p. {r['pages']} (best {r['score']}): {r['quote'][:110]}")
    print(f"  cited pages holding a graph claim or an image-read table: "
          f"{len({(r['source'], r['pages']) for r in rows}) - len(not_in_graph)} of {len({(r['source'], r['pages']) for r in rows})}")
    for s, p in not_in_graph:
        print(f"  [not in graph] {s} p. {p}")
    print(f"essay body: about {words:,} words (detex)")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
