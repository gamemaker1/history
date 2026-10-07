#!/usr/bin/env python3
"""Check every proposed claim against its page and write the verified claims to data/claims.csv.

Reads the claims proposed by extract_claims.py (data/claims_raw.jsonl), the
claims entered by hand (data/claims_manual.csv), and the livestock tables
read from page images (data/flocks.csv), which become OWNS and
HAS_POPULATION claims. A claim passes only if
its quote is found on the cited page of the text in text/:

  exact     the quote's words appear in order on the page (case, punctuation,
            line breaks and hyphenation ignored, as in pageref.py);
  fuzzy     a stretch of the page matches the quote character by character
            with a similarity of at least --threshold (default 0.85), which
            allows for OCR noise and for quotes typed from the page image;
  adjacent  as above, but on the page before or after the one cited (the
            quote runs over a page break or the page was mis-cited). The
            page is corrected.

Hand-entered claims whose extracted_by starts with "image" were typed from
the rendered page image (tables, or two-column text that the OCR interleaves)
and cannot be matched against the text. They are kept with quote_match
"image" and status image_only, and count as evidence only once a person has
signed them off.

Claims whose quote is not found go to analysis/claims_rejected.csv. Subjects,
objects and places are matched to data/entities.csv by label, id or alias.
Names that match nothing are listed in analysis/unresolved_entities.csv, so
a person can add them to entities.csv as new entities or aliases.

Human columns in data/claims.csv (verified_by, verified_on, human_status,
human_note) are kept across reruns, matched by claim_id.

Usage (from the project folder):
  python3 scripts/verify_claims.py
  python3 scripts/verify_claims.py --threshold 0.9

Standard library only.
"""

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from difflib import SequenceMatcher

from corpus import ANALYSIS, DATA, ROOT, layer_year, pages, source_text, tokens
from kg_schema import CLAIM_FIELDS, PREDICATES

RAW = DATA / "claims_raw.jsonl"
MANUAL = DATA / "claims_manual.csv"
FLOCKS = DATA / "flocks.csv"
OUT = DATA / "claims.csv"
HUMAN = ["verified_by", "verified_on", "human_status", "human_note"]
FIELDS = ["claim_id", "source", "pdf_page", "layer_year", "subject", "subject_id", "predicate",
          "object", "object_id", "resource", "resource_id", "qty", "unit", "months", "place", "place_id", "when", "date_text",
          "quote", "note", "extracted_by", "quote_match", "match_score", "qty_in_quote", "entity_ok", "type_ok",
          "auto_status"] + HUMAN


def squash(text):
    """Lower-case letters and digits with single spaces, hyphenated line breaks and
    thousands separators (2,027) rejoined."""
    text = re.sub(r"(\w)-[ \t]*\n[ \t]*(\w)", r"\1\2", text.lower())
    text = re.sub(r"(\d),(\d{3})", r"\1\2", text)
    return " ".join(re.findall(r"[a-z0-9]+", text))


def numbers(text):
    return re.findall(r"\d+", text)


def best_fuzzy(page, quote):
    """Best character similarity between the quote and any stretch of the page.

    Returns (score, window). A small OCR slip in a word is tolerated, but a
    changed number is not: candidate windows must contain every number in the
    quote, because the figures are the evidence that matters most.
    """
    if not quote or not page:
        return 0.0, ""
    n = len(quote)
    q_numbers = Counter(numbers(quote))
    best, best_window = 0.0, ""
    starts = [0] + [m.end() for m in re.finditer(" ", page)]
    for i in starts:
        window = page[i:i + n]
        sm = SequenceMatcher(None, window, quote, autojunk=False)
        if sm.real_quick_ratio() <= best or sm.quick_ratio() <= best:
            continue
        score = sm.ratio()
        if score <= best:
            continue
        # Look a little beyond the window, in case the quote is a few characters short.
        if q_numbers - Counter(numbers(page[max(0, i - 10):i + n + 10])):
            continue
        best, best_window = score, window
        if best == 1.0:
            break
    return best, best_window


class PageCache:
    def __init__(self):
        self.files = {}

    def page(self, source, n):
        if source not in self.files:
            self.files[source] = pages(source_text(source))
        p = self.files[source]
        return p[n - 1] if 1 <= n <= len(p) else ""


def match_quote(cache, source, page_no, quote, threshold):
    """Return (match kind, score, page where found)."""
    q_tokens = tokens(quote)
    q_squash = squash(quote)
    if len(q_tokens) < 3:
        return "none", 0.0, page_no
    for kind, n in (("exact", page_no), ("adjacent", page_no - 1), ("adjacent", page_no + 1)):
        page = cache.page(source, n)
        if f" {' '.join(q_tokens)} " in f" {' '.join(tokens(page))} ":
            return kind, 1.0, n
    best = (0.0, page_no)
    for n in (page_no, page_no - 1, page_no + 1):
        score, _ = best_fuzzy(squash(cache.page(source, n)), q_squash)
        if score > best[0]:
            best = (score, n)
    if best[0] >= threshold:
        return ("fuzzy" if best[1] == page_no else "adjacent"), round(best[0], 3), best[1]
    return "none", round(best[0], 3), page_no


def qty_in_quote(qty, quote):
    """Whether a whole-number qty appears as a number in the quote ("" when there is no qty
    or it is derived, such as 2.5 annas from "2 annas 6 pies")."""
    try:
        q = float(qty)
    except (TypeError, ValueError):
        return ""
    if q != int(q):
        return ""
    return str(int(q)) in numbers(squash(quote))


def entity_index():
    with open(DATA / "entities.csv", encoding="utf-8") as f:
        entities = list(csv.DictReader(f))
    index = {}
    for e in entities:
        for name in [e["id"], e["label"]] + [a for a in e["aliases"].split("|") if a]:
            index.setdefault(norm_name(name), e)
    return index


def norm_name(name):
    return " ".join(re.findall(r"[a-z0-9]+", (name or "").lower().replace("_", " ")))


def resolve(index, name):
    key = norm_name(name)
    if not key:
        return None
    if key in index:
        return index[key]
    if key.endswith("s") and key[:-1] in index:
        return index[key[:-1]]
    if key + "s" in index:
        return index[key + "s"]
    return None


def claim_id(c):
    key = "|".join(str(c.get(k, "")).lower() for k in ("source", "pdf_page", "predicate", "subject", "object", "qty"))
    key += "|" + " ".join(tokens(c.get("quote", "")))
    return "c" + hashlib.sha256(key.encode("utf-8")).hexdigest()[:10]


def flock_claims():
    """OWNS and HAS_POPULATION claims from the livestock tables read from page images."""
    if not FLOCKS.exists():
        return []
    claims = []
    with open(FLOCKS, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            subject = "households" if r["group"] == "all households" else r["group"]
            base = {"source": r["village"], "pdf_page": int(r["pdf_page"]), "subject": subject,
                    "subject_type": "group", "predicate": "OWNS", "object_type": "resource", "resource": "",
                    "months": "", "place": r["village"], "when": "at_survey", "date_text": "",
                    "extracted_by": f"image: {r['read_by']}", "note": r["note"]}
            parts = []
            if r["sheep"] != "" or r["goats"] != "":
                if r["sheep"] != "":
                    parts.append(("sheep", r["sheep"], r["hh_owning_sheep"]))
                if r["goats"] != "":
                    parts.append(("goats", r["goats"], r["hh_owning_goats"]))
            elif r["sheep_and_goats"] != "":
                parts.append(("sheep and goats", r["sheep_and_goats"], r["hh_owning_flock"]))
            for obj, n, hh in parts:
                owning = f", {hh} households owning" if hh != "" else ""
                claims.append({**base, "object": obj, "qty": n, "unit": obj,
                               "quote": f"{r['group']}: {n} {obj}{owning} ({r['source_kind']}, read from the page image)"})
            if r["households_in_group"]:
                claims.append({**base, "predicate": "HAS_POPULATION", "object": "households", "object_type": "group",
                               "qty": r["households_in_group"], "unit": "households",
                               "quote": f"{r['group']}: {r['households_in_group']} households (table, read from the page image)"})
    return claims


def load_raw():
    claims = []
    if RAW.exists():
        with open(RAW, encoding="utf-8") as f:
            for line in f:
                c = json.loads(line)
                c["months"] = "|".join(str(m) for m in c.get("months") or [])
                claims.append(c)
    if MANUAL.exists():
        with open(MANUAL, encoding="utf-8") as f:
            for c in csv.DictReader(f):
                c["pdf_page"] = int(c["pdf_page"])
                c.setdefault("extracted_by", "manual")
                claims.append(c)
    claims += flock_claims()
    return claims


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--threshold", type=float, default=0.85, help="minimum similarity for a fuzzy match")
    args = ap.parse_args()

    previous = {}
    if OUT.exists():
        with open(OUT, encoding="utf-8") as f:
            previous = {r["claim_id"]: r for r in csv.DictReader(f)}

    index = entity_index()
    cache = PageCache()
    kept, rejected, unresolved = [], [], Counter()
    seen = set()

    for c in load_raw():
        c = {k: ("" if v is None else v) for k, v in c.items()}
        cited_page = int(c["pdf_page"])
        if str(c.get("extracted_by", "")).startswith("image"):
            kind, score, found = "image", "", cited_page
        else:
            kind, score, found = match_quote(cache, c["source"], cited_page, c["quote"], args.threshold)
        c["pdf_page"] = found

        ids = {}
        for role in ("subject", "object", "place", "resource"):
            e = resolve(index, c.get(role, ""))
            ids[role] = e["id"] if e else ""
            if c.get(role) and not e:
                unresolved[(c[role], c.get(f"{role}_type", {"place": "place", "resource": "resource"}.get(role, "")))] += 1
        pred = PREDICATES.get(c["predicate"])
        type_ok = bool(pred) and c.get("subject_type", "") in pred[2] and c.get("object_type", "") in pred[3]
        entity_ok = bool(ids["subject"] and ids["object"] and (ids["place"] or not c.get("place"))
                         and (ids["resource"] or not c.get("resource")))

        row = {
            **{k: c.get(k, "") for k in CLAIM_FIELDS},
            "source": c["source"],
            "pdf_page": found,
            "layer_year": layer_year(c["source"]),
            "subject_id": ids["subject"], "object_id": ids["object"], "place_id": ids["place"],
            "resource_id": ids["resource"],
            "extracted_by": c.get("extracted_by", ""),
            "quote_match": kind, "match_score": score,
            "qty_in_quote": qty_in_quote(c.get("qty"), c["quote"]),
            "entity_ok": entity_ok, "type_ok": type_ok,
        }
        row["claim_id"] = claim_id(row)
        if kind == "none":
            rejected.append({**row, "cited_page": cited_page})
            continue
        if row["claim_id"] in seen:
            continue
        seen.add(row["claim_id"])
        if not pred:
            row["auto_status"] = "bad_predicate"
        elif kind == "image":
            row["auto_status"] = "image_only"
        else:
            row["auto_status"] = "auto_ok" if entity_ok else "needs_entity"
        for h in HUMAN:
            row[h] = previous.get(row["claim_id"], {}).get(h, "")
        kept.append(row)

    ANALYSIS.mkdir(exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(kept)
    with open(ANALYSIS / "claims_rejected.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS + ["cited_page"], extrasaction="ignore")
        w.writeheader()
        w.writerows(rejected)
    with open(ANALYSIS / "unresolved_entities.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["name", "type", "claims"])
        for (name, typ), n in unresolved.most_common():
            w.writerow([name, typ, n])

    total = len(kept) + len(rejected)
    matches = Counter(r["quote_match"] for r in kept)
    status = Counter(r["auto_status"] for r in kept)
    signed = sum(1 for r in kept if r["verified_by"])
    print(f"{total} claims checked: {len(kept)} kept in {OUT.relative_to(ROOT)}, "
          f"{len(rejected)} rejected (quote not on the page)")
    print("  quote match: " + ", ".join(f"{k} {v}" for k, v in matches.most_common()))
    print("  status: " + ", ".join(f"{k} {v}" for k, v in status.most_common()))
    print(f"  signed off by a person: {signed}")
    print(f"  {len(unresolved)} unresolved entity names in analysis/unresolved_entities.csv")


if __name__ == "__main__":
    main()
