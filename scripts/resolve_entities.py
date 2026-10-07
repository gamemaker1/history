#!/usr/bin/env python3
"""Map the names in claims that match no entity to existing entities or new ones, with a language model.

verify_claims.py lists every subject, object, place and resource name that
matches nothing in data/entities.csv in analysis/unresolved_entities.csv.
This script sends those names in batches, each with up to two example claims
for context and the whole entity list, to gpt-6-luna. For every name the model
answers either "alias" (the name is a spelling, OCR variant or synonym of an
existing entity) or "new" (a distinct entity, with label, type and subtype).

The answers are written to data/entity_resolution.csv, which is the audit
trail: one row per name, with the model's reason. --apply merges them into
data/entities.csv (aliases appended to existing entities; new entities added
with added_by recording the model). Names proposed as the same new label
become one entity. Rerun verify_claims.py afterwards.

Usage (from the project folder):
  .venv/bin/python scripts/resolve_entities.py              # ask the model, write the proposals
  .venv/bin/python scripts/resolve_entities.py --apply      # merge the proposals into entities.csv
  .venv/bin/python scripts/resolve_entities.py --min-claims 2

Needs the openai package and OPENAI_API_KEY (in .env). Cost is a few cents.
"""

import argparse
import csv
import json
import re
from collections import defaultdict
from datetime import date

from corpus import ANALYSIS, DATA, ROOT
from kg_schema import ENTITY_TYPES
from llm import nullable, run_cached

PROMPT_VERSION = "v1"
MODEL = "gpt-6-luna"
OUT = DATA / "entity_resolution.csv"
BATCH = 30

SCHEMA = {
    "type": "object",
    "properties": {
        "resolutions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "action": {"type": "string", "enum": ["alias", "new"]},
                    "entity_id": nullable("string"),
                    "new_label": nullable("string"),
                    "new_type": nullable("string", list(ENTITY_TYPES)),
                    "new_subtype": nullable("string"),
                    "reason": {"type": "string"},
                },
                "required": ["name", "action", "entity_id", "new_label", "new_type", "new_subtype", "reason"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["resolutions"],
    "additionalProperties": False,
}

INSTRUCTIONS = """You curate the entity list of a knowledge graph for a history project on seasonal herding in the Himachal hills, 1881 to 1961, built from the 1961 Census village surveys of Himachal Pradesh.

You receive names that appear in extracted claims but match no existing entity, each with its guessed type and one or two example claims. For each name decide:

- "alias": the name refers to an entity already in the list: a spelling or OCR variant, a plural, a fuller or shorter form, or a synonym used in the same sense (for example "Bharmour" is Brahmaur; "money lenders" is moneylender; "flocks of sheep and goats" is sheep and goats; "Gadis" is Gaddi). Give its entity_id exactly as listed. Set the new_ fields to null.
- "new": a distinct entity that deserves its own node: a named place, pass, pasture, stream, market or fair; a caste, tribe or community; a named person or household; an office or authority; a specific good, right, document or animal; an event; or a generic actor that recurs and has no close match (for example "forest guard", "porter"). Give new_label (short, singular, in the style of the list), new_type (one of the entity types) and new_subtype (for example village, pasture, pass, market, region, town, caste, office, good, animal, right, person). Set entity_id to null.

Prefer "alias" whenever the meaning is the same; do not create near-duplicates. Do not alias across meaning: a named person is not "households"; "Simla District" is a region, not the village of Kalath. Names that are a list of several things (for example "wool, woollens, chilgoza") should be aliased to the most important single entity in them, and the reason should say so.

reason: one short sentence.

Entity types:
{types}

Existing entities (id | label | type | subtype | aliases):
{entities}
"""


def load_entities():
    with open(DATA / "entities.csv", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def norm(s):
    return " ".join(re.findall(r"[a-z0-9]+", (s or "").lower().replace("_", " ")))


def contexts():
    """Up to two example claims for each unresolved name."""
    ex = defaultdict(list)
    with open(DATA / "claims.csv", encoding="utf-8") as f:
        for c in csv.DictReader(f):
            for role in ("subject", "object", "place", "resource"):
                if c.get(role) and not c.get(f"{role}_id"):
                    if len(ex[c[role]]) < 2:
                        other = c["object"] if role == "subject" else c["subject"]
                        ex[c[role]].append({"as": role, "claim": f"{c['subject']} {c['predicate']} {c['object']}",
                                            "place": c["place"], "source": f"{c['source']} p. {c['pdf_page']}",
                                            "quote": c["quote"][:220], "other": other})
    return ex


def propose(min_claims, budget):
    rejected = set()
    if OUT.exists():  # names a person has rejected are not asked again
        with open(OUT, encoding="utf-8") as f:
            rejected = {r["name"] for r in csv.DictReader(f) if r["accepted"].lower().startswith(("no", "reject"))}
    with open(ANALYSIS / "unresolved_entities.csv", encoding="utf-8") as f:
        names = [r for r in csv.DictReader(f) if int(r["claims"]) >= min_claims and r["name"] not in rejected]
    ex = contexts()
    ents = load_entities()
    instructions = INSTRUCTIONS.format(
        types="\n".join(f"- {k}: {v}" for k, v in ENTITY_TYPES.items()),
        entities="\n".join(f"{e['id']} | {e['label']} | {e['type']} | {e['subtype']} | {e['aliases'].replace('|', ', ')}"
                           for e in ents))
    jobs = []
    for i in range(0, len(names), BATCH):
        batch = [{"name": r["name"], "type_guess": r["type"], "claims": int(r["claims"]), "examples": ex.get(r["name"], [])}
                 for r in names[i:i + BATCH]]
        jobs.append((f"batch {i // BATCH + 1:02d}", json.dumps(batch, ensure_ascii=False, indent=1)))
    results = run_cached("resolve_entities", jobs, model=MODEL, effort="medium", instructions=instructions,
                         schema=SCHEMA, name="resolutions", prompt_version=PROMPT_VERSION, budget=budget)
    ids = {e["id"] for e in ents}
    asked = {r["name"]: r for r in names}
    rows, seen = [], set()
    for job_id, _ in jobs:
        rec = results.get(job_id)
        if not rec or not rec["result"]:
            continue
        for r in rec["result"]["resolutions"]:
            if r["name"] not in asked or r["name"] in seen:
                continue
            seen.add(r["name"])
            if r["action"] == "alias" and r["entity_id"] not in ids:
                r["reason"] += f" [model gave unknown id {r['entity_id']!r}; treated as new]"
                r["action"], r["new_label"] = "new", r["new_label"] or r["name"]
                r["new_type"] = r["new_type"] or asked[r["name"]]["type"] or "place"
            rows.append({**r, "claims": asked[r["name"]]["claims"], "model": rec["model_served"] or MODEL,
                         "proposed_on": date.today().isoformat(), "accepted": ""})
    missing = [n for n in asked if n not in seen]
    # Keep earlier decisions (and any edits to them): the file is an audit trail, not a scratch file.
    if OUT.exists():
        with open(OUT, encoding="utf-8") as f:
            earlier = [r for r in csv.DictReader(f) if r["name"] not in seen]
        rows = earlier + rows
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        fields = ["name", "claims", "action", "entity_id", "new_label", "new_type", "new_subtype", "reason",
                  "model", "proposed_on", "accepted"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    rows_now = [r for r in rows if r["name"] in seen]
    n_alias = sum(r["action"] == "alias" for r in rows_now)
    rows = rows_now
    print(f"{len(rows)} of {len(asked)} names resolved ({n_alias} alias, {len(rows) - n_alias} new) "
          f"written to {OUT.relative_to(ROOT)}")
    if missing:
        print(f"  {len(missing)} names got no answer: {', '.join(missing[:8])}")


def slug(label, taken):
    base = "_".join(re.findall(r"[a-z0-9]+", label.lower()))[:40] or "entity"
    eid, n = base, 2
    while eid in taken:
        eid, n = f"{base}_{n}", n + 1
    return eid


def apply():
    ents = load_entities()
    fields = list(ents[0].keys())
    if "added_by" not in fields:
        fields.append("added_by")
        for e in ents:
            e["added_by"] = "Claude (claude-opus-5-5), 7 Oct 2026"
    by_id = {e["id"]: e for e in ents}
    known = {}
    for e in ents:
        for n in [e["id"], e["label"]] + [a for a in e["aliases"].split("|") if a]:
            known.setdefault(norm(n), e["id"])
    with open(OUT, encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if not r["accepted"].lower().startswith(("no", "reject"))]

    def add_alias(eid, name):
        if norm(name) in known:
            return False
        e = by_id[eid]
        e["aliases"] = "|".join([a for a in e["aliases"].split("|") if a] + [name])
        known[norm(name)] = eid
        return True

    aliases = new = 0
    for r in rows:
        if r["action"] == "alias" and r["entity_id"] in by_id:
            aliases += add_alias(r["entity_id"], r["name"])
    for r in rows:
        if r["action"] != "new":
            continue
        label = r["new_label"] or r["name"]
        target = known.get(norm(label))
        if target:  # the proposed label already exists: the name becomes an alias of it
            aliases += add_alias(target, r["name"])
            continue
        eid = slug(label, by_id)
        e = {k: "" for k in fields}
        e.update(id=eid, label=label, type=r["new_type"] or "place", subtype=r["new_subtype"] or "",
                 note=r["reason"], added_by=f"{r['model']} via resolve_entities.py, {r['proposed_on']} (to check)")
        ents.append(e)
        by_id[eid] = e
        known[norm(label)] = eid
        add_alias(eid, r["name"])
        new += 1
    with open(DATA / "entities.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, restval="")
        w.writeheader()
        w.writerows(ents)
    print(f"entities.csv: {aliases} aliases added, {new} new entities; {len(ents)} entities in all")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--apply", action="store_true", help="merge data/entity_resolution.csv into entities.csv")
    ap.add_argument("--min-claims", type=int, default=1, help="only names used in at least this many claims")
    ap.add_argument("--budget", type=float, default=0.5, help="US dollars for this task")
    args = ap.parse_args()
    if args.apply:
        apply()
    else:
        propose(args.min_claims, args.budget)


if __name__ == "__main__":
    main()
