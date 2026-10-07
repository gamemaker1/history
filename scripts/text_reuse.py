#!/usr/bin/env python3
"""Find passages that later sources copy from earlier ones, and which claims rest on copied text.

Source criticism for the knowledge graph: if Rose (1911 to 1919) repeats Barnes
as quoted in the 1881 census, or a 1961 volume reprints either, the two are one
witness, not two. Method, after the Programming Historian lesson "Detecting
Text Reuse with Passim", in plain Python:

  1. Every page of the 1881 Results, Rose's three volumes, the 1931 Report and
     every 1961 volume is reduced to lower-case word tokens (OCR hyphenation
     rejoined) and cut into overlapping 7-word shingles.
  2. Shingles that occur more than --common times across the earlier sources
     (boilerplate, table headings) are ignored.
  3. Each page of a later source is compared with the pages of every strictly
     earlier source: a page pair sharing at least 3 shingles is a candidate.
  4. Shared shingles at consecutive positions are merged into runs; a run of at
     least --min-words words is a reused passage.

Outputs in analysis/text_reuse/:
  passages.csv   one row per reused passage: later source and page, earlier
                 source and page, length in words, and the passage text
  pairs.csv      reuse summed by pair of sources
  claims.csv     every claim whose quote lies inside a reused passage, with the
                 earlier page it repeats (its independent_sources is then lower)

Usage (from the project folder):
  python3 scripts/text_reuse.py
  python3 scripts/text_reuse.py --min-words 20

Standard library only.
"""

import argparse
import csv
import re
from collections import defaultdict

from corpus import ANALYSIS, COLONIAL, DATA, ROOT, TEXT, source_name, source_text

OUT = ANALYSIS / "text_reuse"
K = 7
WORD = re.compile(r"[a-z0-9]+")


def page_tokens(text):
    text = re.sub(r"(\w)-[ \t]*\n[ \t]*(\w)", r"\1\2", text.lower())
    return WORD.findall(text)


def documents():
    """(name, year, path) for every source; Rose's volumes count as one work."""
    docs = [(name, year, source_text(name)) for name, (_, year) in COLONIAL.items() if name != "1931 Tables"]
    for path in sorted((TEXT / "1961").glob("*.txt")):
        docs.append((source_name(path), 1961, path))
    return docs


def work(name):
    return "Rose" if name.startswith("Rose") else name


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--min-words", type=int, default=12, help="shortest run reported as reuse")
    ap.add_argument("--common", type=int, default=6, help="ignore shingles found more often than this")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)

    docs = documents()
    pages = {}  # (doc index, page) -> tokens
    for i, (name, year, path) in enumerate(docs):
        for n, text in enumerate(path.read_text(encoding="utf-8", errors="ignore").split("\f"), 1):
            toks = page_tokens(text)
            if len(toks) >= K:
                pages[(i, n)] = toks

    # Index every shingle of the sources older than 1961 (the only possible originals for 1961, and
    # for each other among themselves).
    index = defaultdict(list)
    for (i, n), toks in pages.items():
        if docs[i][1] < 1961:
            seen = set()
            for j in range(len(toks) - K + 1):
                h = hash(tuple(toks[j:j + K]))
                if h not in seen:
                    seen.add(h)
                    index[h].append((i, n))
    common = {h for h, locs in index.items() if len(locs) > args.common}

    passages = []
    for (i, n), toks in pages.items():
        name, year, _ = docs[i]
        shingles = [hash(tuple(toks[j:j + K])) for j in range(len(toks) - K + 1)]
        hits = defaultdict(list)  # earlier page -> positions in this page
        for pos, h in enumerate(shingles):
            if h in common:
                continue
            for (a, b) in index.get(h, ()):
                ea_name, ea_year, _ = docs[a]
                if ea_year < year and work(ea_name) != work(name):
                    hits[(a, b)].append(pos)
        for (a, b), positions in hits.items():
            if len(positions) < 3:
                continue
            runs, start, prev = [], positions[0], positions[0]
            for p in positions[1:]:
                if p - prev > 2:  # allow one OCR slip inside a run
                    runs.append((start, prev))
                    start = p
                prev = p
            runs.append((start, prev))
            for s, e in runs:
                words = e - s + K
                if words >= args.min_words:
                    passages.append({"later_source": name, "later_year": year, "later_page": n,
                                     "earlier_source": docs[a][0], "earlier_year": docs[a][1], "earlier_page": b,
                                     "words": words, "text": " ".join(toks[s:e + K])})

    passages.sort(key=lambda r: (-r["words"]))
    fields = ["later_source", "later_year", "later_page", "earlier_source", "earlier_year", "earlier_page", "words", "text"]
    with open(OUT / "passages.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(passages)

    pairs = defaultdict(lambda: [0, 0])
    for p in passages:
        k = (p["later_source"], p["earlier_source"])
        pairs[k][0] += 1
        pairs[k][1] += p["words"]
    with open(OUT / "pairs.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["later_source", "earlier_source", "passages", "words"])
        for (a, b), (n, words) in sorted(pairs.items(), key=lambda kv: -kv[1][1]):
            w.writerow([a, b, n, words])

    # Claims whose quote lies inside a reused passage.
    by_page = defaultdict(list)
    for p in passages:
        by_page[(p["later_source"], p["later_page"])].append(p)
    rows = []
    with open(DATA / "claims.csv", encoding="utf-8") as f:
        for c in csv.DictReader(f):
            if c["quote_match"] == "image":
                continue
            q = " ".join(page_tokens(c["quote"]))
            for p in by_page.get((c["source"], int(c["pdf_page"])), []):
                if q and len(q.split()) >= 5 and q in p["text"]:
                    rows.append({"claim_id": c["claim_id"], "source": c["source"], "pdf_page": c["pdf_page"],
                                 "claim": f"{c['subject']} {c['predicate']} {c['object']}",
                                 "repeats": f"{p['earlier_source']} p. {p['earlier_page']} ({p['earlier_year']})",
                                 "quote": c["quote"][:160]})
                    break
    with open(OUT / "claims.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["claim_id", "source", "pdf_page", "claim", "repeats", "quote"])
        w.writeheader()
        w.writerows(rows)

    print(f"{len(pages):,} pages compared; {len(passages)} reused passages of at least {args.min_words} words; "
          f"outputs in {OUT.relative_to(ROOT)}/")
    for (a, b), (n, words) in sorted(pairs.items(), key=lambda kv: -kv[1][1])[:12]:
        print(f"  {a} repeats {b}: {n} passages, {words:,} words")
    print(f"{len(rows)} claims rest on a passage copied from an earlier source")
    for r in rows[:10]:
        print(f"  {r['source']} p. {r['pdf_page']}: {r['claim']}  <- {r['repeats']}")


if __name__ == "__main__":
    main()
