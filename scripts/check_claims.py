#!/usr/bin/env python3
"""Check that each claim says what its page says: a second, independent model pass over every claim.

verify_claims.py proves that a claim's quote is on its page. It cannot tell
whether the claim reads the quote correctly. This script sends each page,
with all the claims drawn from it, to gpt-6-luna at high reasoning effort,
and asks for a verdict on each claim:

  supported         the page states it, with the right subject, object,
                    direction, numbers, months, place and time
  partly_supported  the relation is on the page but a field is wrong or
                    over-stated (wrong_fields says which)
  not_supported     the page does not say it, or says the opposite
  unclear           the OCR is too damaged to tell

Verdicts go to data/claim_checks.csv. build_graph.py and query_graph.py use
them as an evidence level, and leave not_supported claims out by default.
Claims read from page images (data/flocks.csv) are not checked here; they
have no text to check against.

How good is the checker itself? --sample draws a stratified random sample of
checked claims to analysis/claim_check_sample.csv with blank columns for the
group. Once the group has filled human_verdict, --agreement measures how often
the checker agrees with a person.

Usage (from the project folder):
  .venv/bin/python scripts/check_claims.py --limit 5        # try five pages
  .venv/bin/python scripts/check_claims.py                  # every page with claims
  .venv/bin/python scripts/check_claims.py --sample 50      # sample for the group
  .venv/bin/python scripts/check_claims.py --agreement      # after the group fills the sample

Needs the openai package and OPENAI_API_KEY (in .env).
"""

import argparse
import csv
import json
import random
from collections import Counter, defaultdict
from datetime import date

from corpus import ANALYSIS, DATA, ROOT, page_text, source_text
from kg_schema import predicate_table
from llm import run_cached

PROMPT_VERSION = "v2"
MODEL = "gpt-6-luna"
OUT = DATA / "claim_checks.csv"
SAMPLE = ANALYSIS / "claim_check_sample.csv"
VERDICTS = ["supported", "partly_supported", "not_supported", "unclear"]
FIELDS = ["subject", "predicate", "object", "resource", "qty", "unit", "months", "place", "when", "date_text"]

SCHEMA = {
    "type": "object",
    "properties": {
        "checks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "claim_id": {"type": "string"},
                    "verdict": {"type": "string", "enum": VERDICTS},
                    "wrong_fields": {"type": "array", "items": {"type": "string", "enum": FIELDS}},
                    "reason": {"type": "string"},
                },
                "required": ["claim_id", "verdict", "wrong_fields", "reason"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["checks"],
    "additionalProperties": False,
}

INSTRUCTIONS = """You check claims that another model extracted from one page of a historical source (a 1961 Census of India volume on Himachal Pradesh, or a colonial census or glossary). The claims will be used as evidence in a history essay, so be strict.

You receive the OCR text of the page and a list of claims. Each claim has a subject, a predicate from a fixed vocabulary, an object, and optional resource, quantity, unit, months, place, time ("when") and date text, plus the quote it was drawn from. Labels may have been normalised to a standard entity list (for example "Brahmaur" for "Bharmour", "sheep and goats" for "flocks"); that is not an error.

For each claim give one verdict:
- "supported": the page states this, with the right subject and object, the right direction (who lends to whom, who sells to whom, who pays whom), and correct numbers, units, months, place and time.
- "partly_supported": the relation is on the page, but at least one field is wrong, over-stated or misattributed: a number or unit misread, the wrong months, the wrong caste or village, a direction reversed, "when" wrong (for example a past practice given as the state at the survey), or a hedged statement made certain. List the wrong fields in wrong_fields.
- "not_supported": the page does not say this, or says the opposite (watch for negation: "have no rights of grazing" does not support GRAZES_AT), or the quote is about something else.
- "unclear": the OCR is too damaged to decide.

Predicate meanings (the same definitions the extracting model was given; the subject and object types are guides, not rules):
{predicates}

reason: one sentence, quoting the words on the page that decide it.
Return one check for every claim_id you are given, and no others.
"""


def claims_by_page():
    with open(DATA / "claims.csv", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["quote_match"] in ("exact", "fuzzy", "adjacent")]
    pages = defaultdict(list)
    for r in rows:
        pages[(r["source"], int(r["pdf_page"]))].append(r)
    return pages


def user_message(source, page, claims):
    listed = [{"claim_id": c["claim_id"], **{k: c[k] for k in FIELDS}, "quote": c["quote"]} for c in claims]
    return (f"Source: {source}, PDF page {page}.\n\n<page>\n{page_text(source_text(source), page)}\n</page>\n\n"
            f"Claims to check:\n{json.dumps(listed, ensure_ascii=False, indent=1)}")


def run(limit, budget, effort):
    pages = claims_by_page()
    keys = sorted(pages)[:limit] if limit else sorted(pages)
    jobs = [(f"{s} p. {p}", user_message(s, p, pages[(s, p)])) for s, p in keys]
    instructions = INSTRUCTIONS.replace("{predicates}", predicate_table())
    results = run_cached("check_claims", jobs, model=MODEL, effort=effort, instructions=instructions,
                         schema=SCHEMA, name="checks", prompt_version=PROMPT_VERSION, budget=budget)
    previous = {}
    if OUT.exists():
        with open(OUT, encoding="utf-8") as f:
            previous = {r["claim_id"]: r for r in csv.DictReader(f)}
    rows, missing = dict(previous), 0
    for (s, p) in keys:
        rec = results.get(f"{s} p. {p}")
        asked = {c["claim_id"] for c in pages[(s, p)]}
        got = {}
        if rec and rec["result"]:
            got = {c["claim_id"]: c for c in rec["result"]["checks"] if c["claim_id"] in asked}
        missing += len(asked - set(got))
        for cid, c in got.items():
            rows[cid] = {"claim_id": cid, "source": s, "pdf_page": p, "verdict": c["verdict"],
                         "wrong_fields": "|".join(c["wrong_fields"]), "reason": c["reason"],
                         "checker": f"{rec['model_served'] or MODEL} (check {PROMPT_VERSION}, effort {effort})",
                         "checked_on": date.today().isoformat()}
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["claim_id", "source", "pdf_page", "verdict", "wrong_fields", "reason",
                                          "checker", "checked_on"])
        w.writeheader()
        w.writerows(rows.values())
    counts = Counter(r["verdict"] for r in rows.values())
    print(f"{len(rows)} claims checked, written to {OUT.relative_to(ROOT)}: " +
          ", ".join(f"{v} {counts[v]}" for v in VERDICTS))
    if missing:
        print(f"  {missing} claims got no verdict (rerun to retry)")
    fields = Counter(f for r in rows.values() for f in r["wrong_fields"].split("|") if f)
    print("  wrong fields in partly_supported claims: " + ", ".join(f"{k} {v}" for k, v in fields.most_common()))


def sample(n, seed=7):
    with open(OUT, encoding="utf-8") as f:
        checks = list(csv.DictReader(f))
    with open(DATA / "claims.csv", encoding="utf-8") as f:
        claims = {r["claim_id"]: r for r in csv.DictReader(f)}
    rng = random.Random(seed)
    by_verdict = defaultdict(list)
    for c in checks:
        if c["claim_id"] in claims:
            by_verdict[c["verdict"]].append(c)
    # Over-sample the rarer verdicts so the checker's errors in each direction can be measured.
    quota = {"supported": n * 2 // 5, "partly_supported": n // 4, "not_supported": n // 4, "unclear": n // 10}
    picked = []
    for v, q in quota.items():
        pool = by_verdict.get(v, [])
        picked += rng.sample(pool, min(q, len(pool)))
    rest = [c for v in VERDICTS for c in by_verdict.get(v, []) if c not in picked]
    picked += rng.sample(rest, max(0, min(n - len(picked), len(rest))))
    rng.shuffle(picked)
    with open(SAMPLE, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["n", "claim_id", "source", "pdf_page", "subject", "predicate", "object", "resource", "qty", "unit",
                    "months", "place", "when", "quote", "ai_verdict", "ai_wrong_fields", "ai_reason",
                    "human_verdict", "human_note", "checked_by"])
        for i, c in enumerate(picked, 1):
            k = claims[c["claim_id"]]
            w.writerow([i, c["claim_id"], k["source"], k["pdf_page"], k["subject"], k["predicate"], k["object"],
                        k["resource"], k["qty"], k["unit"], k["months"], k["place"], k["when"], k["quote"],
                        c["verdict"], c["wrong_fields"], c["reason"], "", "", ""])
    print(f"{len(picked)} claims sampled to {SAMPLE.relative_to(ROOT)} (by AI verdict: "
          + ", ".join(f"{v} {sum(c['verdict'] == v for c in picked)}" for v in VERDICTS) + ")")
    print("For each row open the page (render_page.py) and fill human_verdict with one of: " + ", ".join(VERDICTS))


def agreement():
    with open(SAMPLE, encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["human_verdict"].strip()]
    if not rows:
        print(f"no human_verdict filled in {SAMPLE.relative_to(ROOT)} yet")
        return
    agree = sum(r["human_verdict"].strip() == r["ai_verdict"] for r in rows)
    print(f"{len(rows)} claims judged by the group; the checker agrees on {agree} ({agree / len(rows):.0%})")
    table = Counter((r["ai_verdict"], r["human_verdict"].strip()) for r in rows)
    with open(ANALYSIS / "claim_check_agreement.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ai_verdict"] + VERDICTS)
        for a in VERDICTS:
            w.writerow([a] + [table[(a, h)] for h in VERDICTS])
            print(f"  AI {a:17s} -> human: " + ", ".join(f"{h} {table[(a, h)]}" for h in VERDICTS if table[(a, h)]))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--limit", type=int, help="only the first N pages")
    ap.add_argument("--budget", type=float, default=1.5, help="US dollars for this task")
    ap.add_argument("--effort", default="high", choices=["low", "medium", "high", "xhigh"])
    ap.add_argument("--sample", type=int, help="draw a sample of N checked claims for the group")
    ap.add_argument("--agreement", action="store_true", help="measure the checker against the group's verdicts")
    args = ap.parse_args()
    if args.sample:
        sample(args.sample)
    elif args.agreement:
        agreement()
    else:
        run(args.limit, args.budget, args.effort)


if __name__ == "__main__":
    main()
