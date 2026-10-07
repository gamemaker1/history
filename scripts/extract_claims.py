#!/usr/bin/env python3
"""Propose knowledge-graph claims from the candidate pages with a language model.

For each page selected in analysis/candidate_pages.csv, sends the page text,
the predicate vocabulary (scripts/kg_schema.py) and the entity list
(data/entities.csv) to the model, and asks for claims as JSON matching
kg_schema.CLAIM_SCHEMA. Every claim must carry a verbatim quote from the page.
Nothing here is accepted as evidence: scripts/verify_claims.py checks every
quote against the page, and a person signs off claims used in the essay.

Two providers are supported. The default is OpenAI with gpt-6-luna (the
group's choice, for cost). Anthropic with claude-opus-5-5 is kept as an
alternative and is the only one with --batch.

Each response is cached in cache/llm/ under a hash of the prompt version,
model, effort, system prompt and page text, so reruns only call the API for
pages not yet done. Each cached response records its token usage and cost.
The script stops sending pages once the spend recorded for the provider,
plus a reserve for the requests in flight, would pass --budget (US dollars).
After every run it rewrites data/claims_raw.jsonl from the cache, in page order.

Usage (from the project folder):
  .venv/bin/python scripts/extract_claims.py --dry-run             # cost estimate, nothing sent
  .venv/bin/python scripts/extract_claims.py --limit 3             # try three pages
  .venv/bin/python scripts/extract_claims.py                       # study villages and 1961 reports
  .venv/bin/python scripts/extract_claims.py --scope all           # all 24 village volumes
  .venv/bin/python scripts/extract_claims.py --scope colonial      # 1881, Rose and 1931 hill pages
  .venv/bin/python scripts/extract_claims.py --sources Kanum,Newell
  .venv/bin/python scripts/extract_claims.py --budget 2            # stop at $2 of recorded spend
  .venv/bin/python scripts/extract_claims.py --no-api              # rebuild claims_raw.jsonl from the cache
  .venv/bin/python scripts/extract_claims.py --provider anthropic --batch submit
  .venv/bin/python scripts/extract_claims.py --provider anthropic --batch collect <batch_id>

Credentials come from the environment or from .env in the project folder
(OPENAI_API_KEY or ANTHROPIC_API_KEY). .env is in .gitignore; never commit a key.
Needs the openai or anthropic package (requirements.txt).
"""

import argparse
import csv
import hashlib
import json
import os
import sys
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait

from corpus import (ANALYSIS, CACHE, COLONIAL, DATA, REPORTS_1961, ROOT, STUDY_VILLAGES, VILLAGES, page_text,
                    source_text, text_path)
from kg_schema import CLAIM_SCHEMA, ENTITY_TYPES, WHEN, predicate_table

PROMPT_VERSION = "v3"
DEFAULT_MODEL = {"openai": "gpt-6-luna", "anthropic": "claude-opus-5-5"}
KEY_VAR = {"openai": "OPENAI_API_KEY", "anthropic": "ANTHROPIC_API_KEY"}
# US dollars per million tokens, from the providers' pricing pages on 7 Oct 2026.
# OpenAI output tokens include reasoning tokens.
PRICES = {
    "gpt-6-luna": {"input": 0.10, "cached": 0.01, "cache_write": 0.10, "output": 0.50},
    "gpt-6.1-sol": {"input": 2.00, "cached": 0.10, "cache_write": 2.00, "output": 10.00},
    "claude-opus-5-5": {"input": 4.00, "cached": 0.20, "cache_write": 5.00, "output": 20.00},
}
MAX_OUTPUT_TOKENS = 16000
LLM_CACHE = CACHE / "llm"
OUT = DATA / "claims_raw.jsonl"

SYSTEM_TEMPLATE = """You extract sourced claims for a history project on seasonal herding in the Himachal hills, 1881 to 1961.

The research question: how did the seasonal movement of flocks between high summer pastures and low winter grazing shape life in the Himachal hills, and who controlled and profited from it? As rule over the hills and control of the pastures, roads and trade changed, did the herding cycle persist as an adaptation to mountain and season, or did the ownership of flocks, pastures and shepherds' labour reshape it?

You will receive the OCR text of one page of a source: a 1961 Census of India volume (a village survey monograph or a report), the 1881 Punjab census report (Ibbetson), H. A. Rose's Glossary of the Tribes and Castes of the Punjab (volumes of 1911 to 1919), or the 1931 Punjab census report. Return every claim on that page that bears on the question, as JSON matching the schema. The colonial sources cover the whole Punjab: take only claims about the hills (Kangra, Kulu, Lahul and Spiti, Chamba, Mandi, Suket, Bushahr and Kinnaur, the Simla hill states) and the hill peoples (Gaddis, hill Gujars, Kanets, Kinnauras, Lahulas, Pangwals).

What counts as relevant: the seasonal movement of flocks, herds and people (where, when, by which route); summer and winter pastures; who owns sheep, goats, buffaloes and other livestock, by caste, tribe or household, with numbers; how many households a village or caste has; hired shepherds and graziers and their pay; who owns or controls pastures, forests and grazing rights, before and after 1948; grazing fees, taxes, permits, auctions of rights, closures of pastures and forests; dues and begar paid to rulers; debt, interest and creditors; trade carried by the flocks, fairs and markets, and the terms of exchange; road work and other wage work that competes with herding; orchards replacing herding; the closure of the Tibet trade; where the village lies on its river; and direct speech by herders. Skip everything else (schools, temples, health, dress) unless it bears on these.

Rules:
1. Only claims stated on this page. Do not use outside knowledge.
2. The quote must be copied character for character from the page text, as one continuous passage of about 5 to 40 words that supports the claim. Keep OCR errors and odd spellings exactly as they appear. Do not fix, shorten with ellipses, or join separate passages. A verification script will reject any quote not found on the page.
3. One fact per claim. A sentence saying Brahmans own 2,027 sheep and goats and Rajputs 2,364 gives two claims.
4. For subject, object and place, use the label from the entity list exactly when an entity matches (matching its aliases too). Otherwise write a short new label in the same style and give its type.
5. resource names what changes hands or is charged for in exchange, extraction and labour claims (ghee, wool, salt, grain, money, grazing fees, grazing permit, wages), using an entity label where one matches. Use null when the predicate's object already is the resource or nothing changes hands.
6. place is where the claim holds, usually the village the survey describes. Use null only for general statements.
7. qty is a number as stated (2,027 becomes 2027; one-fourth becomes 0.25). unit says what is counted or what the rate is, for example "sheep and goats", "households", "Rs per 100 head per season", "per cent interest per year", "Rs per day". Use null for both when there is no number.
8. months lists the months named, as integers (October and November is [10, 11]). Leave it empty when no month is named.
9. when must be one of: {when}. date_text holds any explicit year or period written in the text (for example "1950", "1952-53", "before the merger"), otherwise null. In a colonial source (1881, Rose, 1931), a statement about the time of writing is "before_1948", and date_text gives the year of the source unless the text names another.
10. Printed tables in OCR are often scrambled. Extract a figure from a table only when its row and column are unambiguous on this page. Otherwise skip the table.
11. note is for anything a historian needs to read the claim correctly (terms of trade, conditions, doubts about OCR), otherwise null.
12. If nothing on the page is relevant, return {{"claims": []}}.

Entity types:
{entity_types}

Predicates (choose the closest; the subject and object types are guides):
{predicates}

Entity list (label | type | aliases):
{entities}
"""


def load_entities():
    with open(DATA / "entities.csv", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def system_prompt():
    entities = "\n".join(
        f"{e['label']} | {e['type']} | {e['aliases'].replace('|', ', ')}" for e in load_entities())
    return SYSTEM_TEMPLATE.format(
        when=", ".join(f'"{k}" ({v})' for k, v in WHEN.items()),
        entity_types="\n".join(f"- {k}: {v}" for k, v in ENTITY_TYPES.items()),
        predicates=predicate_table(),
        entities=entities,
    )


def selected_pages(scope, only_sources):
    if scope == "colonial":
        with open(ANALYSIS / "candidate_pages_colonial.csv", encoding="utf-8") as f:
            rows = [r for r in csv.DictReader(f) if r["selected"] == "True"]
        order = list(COLONIAL)
        rows = [r for r in rows if not only_sources or r["source"] in only_sources]
        rows.sort(key=lambda r: (order.index(r["source"]), int(r["page"])))
        return [(r["source"], int(r["page"])) for r in rows]
    with open(ANALYSIS / "candidate_pages.csv", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["selected"] == "True"]
    allowed = set(REPORTS_1961) | set(STUDY_VILLAGES if scope == "study" else VILLAGES)
    if only_sources:
        allowed = set(only_sources)
    order = list(REPORTS_1961) + STUDY_VILLAGES + [v for v in VILLAGES if v not in STUDY_VILLAGES]
    rows = [r for r in rows if r["source"] in allowed]
    rows.sort(key=lambda r: (order.index(r["source"]), int(r["page"])))
    return [(r["source"], int(r["page"])) for r in rows]


def every_page():
    """All selected pages, 1961 and colonial: claims_raw.jsonl is rebuilt from all of them."""
    return selected_pages("all", None) + selected_pages("colonial", None)


def cache_index(model, effort):
    """Newest cached response for each (source, page), whatever the prompt version, so a new
    PROMPT_VERSION does not re-send (and re-bill) pages already done. --refresh overrides."""
    index = {}
    for path in sorted(LLM_CACHE.glob("*.json"), key=lambda p: p.stat().st_mtime):
        rec = json.loads(path.read_text(encoding="utf-8"))
        if rec.get("model") == model and rec.get("effort") == effort:
            index[(rec["source"], rec["page"])] = path
    return index


def load_env():
    """Read KEY=value lines from .env into the environment (existing variables win)."""
    path = ROOT / ".env"
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip().strip('"').strip("'")
        if value and key.strip() not in os.environ:
            os.environ[key.strip()] = value


def openai_schema(schema):
    """CLAIM_SCHEMA in the form OpenAI strict mode documents: nullable fields as
    "type": [t, "null"] rather than anyOf."""
    if isinstance(schema, dict):
        alts = schema.get("anyOf")
        if alts and len(alts) == 2 and {"type": "null"} in alts:
            other = next(a for a in alts if a != {"type": "null"})
            return {**{k: v for k, v in schema.items() if k != "anyOf"}, "type": [other["type"], "null"]}
        return {k: openai_schema(v) for k, v in schema.items()}
    if isinstance(schema, list):
        return [openai_schema(v) for v in schema]
    return schema


def user_message(source, page):
    if source in COLONIAL:
        path = source_text(source)
        return (f"Source: {source} (colonial source, year {COLONIAL[source][1]}), file {path.name}, PDF page {page}.\n\n"
                f"<page>\n{page_text(path, page)}\n</page>")
    kind = "village survey" if source in VILLAGES else "report"
    path = text_path(source)
    return (f"Source: {source} ({kind}), file {path.name}, PDF page {page}.\n\n"
            f"<page>\n{page_text(path, page)}\n</page>")


def cache_key(system, source, page, model, effort, prompt_version=PROMPT_VERSION):
    """Cache key for one page. The system prompt is not hashed: its instructions are
    versioned by PROMPT_VERSION (bump it when they change), and its entity list grows
    as entities are curated, which must not orphan the responses already paid for.
    `system` is kept as an argument so the call sites stay unchanged."""
    h = hashlib.sha256()
    for part in (prompt_version, model, effort, user_message(source, page)):
        h.update(part.encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()[:32]


def reindex_cache():
    """Rename cached responses to the current cache_key scheme (from their own records)."""
    moved = kept = 0
    for path in sorted(LLM_CACHE.glob("*.json"), key=lambda p: p.stat().st_mtime):
        rec = json.loads(path.read_text(encoding="utf-8"))
        target = cache_file(cache_key(None, rec["source"], rec["page"], rec["model"], rec["effort"],
                                      rec["prompt_version"]))
        if target == path:
            kept += 1
            continue
        path.replace(target)  # later files win, so the newest response for a page is kept
        moved += 1
    print(f"cache re-indexed: {moved} files renamed, {kept} already current")


def cache_file(key):
    return LLM_CACHE / f"{key}.json"


def cost(model, usage):
    p = PRICES.get(model)
    if not p:
        return 0.0
    return (usage["uncached_input"] * p["input"] + usage["cached_input"] * p["cached"]
            + usage["cache_write"] * p["cache_write"] + usage["output"] * p["output"]) / 1e6


def page_reserve(model, system, source, page):
    """Most a single request could cost: its whole input uncached and the output cap used up."""
    p = PRICES.get(model, {"input": 0, "output": 0})
    tokens_in = (len(system) + len(user_message(source, page))) / 3
    return (tokens_in * p["input"] + MAX_OUTPUT_TOKENS * p["output"]) / 1e6


# -- OpenAI --------------------------------------------------------------------

def call_openai(client, system, source, page, model, effort):
    response = client.responses.create(
        model=model,
        instructions=system,
        input=[{"role": "user", "content": user_message(source, page)}],
        text={"format": {"type": "json_schema", "name": "claims",
                         "schema": openai_schema(CLAIM_SCHEMA), "strict": True}},
        reasoning={"effort": effort},
        max_output_tokens=MAX_OUTPUT_TOKENS,
        prompt_cache_key=f"herding-claims-{PROMPT_VERSION}",
        store=False,
    )
    u = response.usage
    cached = (u.input_tokens_details.cached_tokens or 0) if u.input_tokens_details else 0
    usage = {"uncached_input": u.input_tokens - cached, "cached_input": cached, "cache_write": 0,
             "output": u.output_tokens,
             "reasoning": (u.output_tokens_details.reasoning_tokens or 0) if u.output_tokens_details else 0}
    if response.status == "incomplete":
        reason = getattr(response.incomplete_details, "reason", None)
        return [], f"incomplete: {reason}", usage, response.model
    message = next((item for item in response.output if item.type == "message"), None)
    part = message.content[0] if message and message.content else None
    if part is None:
        return [], "no output", usage, response.model
    if part.type == "refusal":
        return [], f"refusal: {part.refusal}", usage, response.model
    try:
        return json.loads(part.text)["claims"], None, usage, response.model
    except (json.JSONDecodeError, KeyError) as e:
        return [], f"bad json: {e}", usage, response.model


# -- Anthropic -----------------------------------------------------------------

def anthropic_params(system, source, page, model, effort):
    return {
        "model": model,
        "max_tokens": MAX_OUTPUT_TOKENS,
        "system": [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        "messages": [{"role": "user", "content": user_message(source, page)}],
        "output_config": {"effort": effort, "format": {"type": "json_schema", "schema": CLAIM_SCHEMA}},
    }


def parse_anthropic(message):
    u = message.usage
    usage = {"uncached_input": u.input_tokens, "cached_input": u.cache_read_input_tokens or 0,
             "cache_write": u.cache_creation_input_tokens or 0, "output": u.output_tokens, "reasoning": 0}
    if message.stop_reason == "refusal":
        return [], f"refusal: {getattr(message.stop_details, 'category', None)}", usage, message.model
    if message.stop_reason == "max_tokens":
        return [], "max_tokens", usage, message.model
    text = next((b.text for b in message.content if b.type == "text"), "")
    try:
        return json.loads(text)["claims"], None, usage, message.model
    except (json.JSONDecodeError, KeyError) as e:
        return [], f"bad json: {e}", usage, message.model


def call_anthropic(client, system, source, page, model, effort):
    # Server-side fallback re-runs a declined request on another model inside the same call.
    message = client.beta.messages.create(
        **anthropic_params(system, source, page, model, effort),
        betas=["server-side-fallback-2026-07-01"], fallbacks="default")
    return parse_anthropic(message)


# -- shared --------------------------------------------------------------------

def save(key, provider, source, page, model, effort, result):
    claims, error, usage, served = result
    record = {
        "source": source, "page": page, "prompt_version": PROMPT_VERSION, "provider": provider,
        "model": model, "model_served": served, "effort": effort, "error": error,
        "usage": usage, "cost_usd": round(cost(model, usage), 6), "claims": claims,
    }
    cache_file(key).write_text(json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8")
    return record


def make_client(provider):
    if provider == "openai":
        import openai
        return openai.OpenAI(), (openai.APIStatusError, openai.APIConnectionError), call_openai
    import anthropic
    return anthropic.Anthropic(), (anthropic.APIStatusError, anthropic.APIConnectionError), call_anthropic


def spent(provider):
    """Spend recorded in the cache for one provider, in US dollars."""
    total = 0.0
    for path in LLM_CACHE.glob("*.json"):
        rec = json.loads(path.read_text(encoding="utf-8"))
        if rec.get("provider") == provider:
            total += rec.get("cost_usd", 0.0)
    return total


def run_api(pages, system, provider, model, effort, workers, budget, refresh=False):
    client, errors, call = make_client(provider)
    done = {} if refresh else cache_index(model, effort)
    todo = [(s, p) for s, p in pages if (s, p) not in done]
    total = spent(provider)
    print(f"{len(pages)} pages selected, {len(pages) - len(todo)} cached, {len(todo)} to send to {model}")
    print(f"recorded spend for {provider} so far: ${total:.4f} of a ${budget:.2f} budget")

    def one(s, p):
        result = call(client, system, s, p, model, effort)
        return save(cache_key(system, s, p, model, effort), provider, s, p, model, effort, result)

    queue = list(todo)
    in_flight, done_n, stopped = {}, 0, False
    with ThreadPoolExecutor(max_workers=workers) as pool:
        while queue or in_flight:
            # Send more only while the spend so far plus the worst case for every request in flight fits.
            while queue and len(in_flight) < workers:
                s, p = queue[0]
                reserve = sum(page_reserve(model, system, *sp) for sp in list(in_flight.values()) + [(s, p)])
                if total + reserve > budget:
                    stopped = True
                    break
                queue.pop(0)
                in_flight[pool.submit(one, s, p)] = (s, p)
            if not in_flight:
                break
            finished, _ = wait(in_flight, return_when=FIRST_COMPLETED)
            for fut in finished:
                s, p = in_flight.pop(fut)
                done_n += 1
                try:
                    rec = fut.result()
                    total += rec["cost_usd"]
                    flag = f"  [{rec['error']}]" if rec["error"] else ""
                    print(f"  {done_n:4d}/{len(todo)}  {s} p. {p}: {len(rec['claims'])} claims, "
                          f"${rec['cost_usd']:.4f} (total ${total:.4f}){flag}")
                except errors as e:
                    print(f"  {done_n:4d}/{len(todo)}  {s} p. {p}: API error: {e}", file=sys.stderr)
            if stopped:
                queue.clear()
    if stopped:
        print(f"stopped at the ${budget:.2f} budget with pages left unsent; raise --budget to continue")


def batch_submit(pages, system, model, effort):
    import anthropic
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request

    client = anthropic.Anthropic()
    todo = {}
    for s, p in pages:
        key = cache_key(system, s, p, model, effort)
        if not cache_file(key).exists():
            todo[key] = (s, p)
    if not todo:
        print("every selected page is already cached")
        return
    # The Batch API does not take the server-side fallback parameter; refusals are recorded instead.
    requests = [Request(custom_id=key, params=MessageCreateParamsNonStreaming(**anthropic_params(system, s, p, model, effort)))
                for key, (s, p) in todo.items()]
    batch = client.messages.batches.create(requests=requests)
    (LLM_CACHE / "batches").mkdir(exist_ok=True)
    (LLM_CACHE / "batches" / f"{batch.id}.json").write_text(json.dumps({
        "model": model, "effort": effort, "prompt_version": PROMPT_VERSION,
        "pages": {k: list(v) for k, v in todo.items()}}, indent=1), encoding="utf-8")
    print(f"submitted batch {batch.id} with {len(requests)} pages")
    print(f"collect with: .venv/bin/python scripts/extract_claims.py --provider anthropic --batch collect {batch.id}")


def batch_collect(batch_id):
    import anthropic

    client = anthropic.Anthropic()
    meta = json.loads((LLM_CACHE / "batches" / f"{batch_id}.json").read_text(encoding="utf-8"))
    batch = client.messages.batches.retrieve(batch_id)
    if batch.processing_status != "ended":
        c = batch.request_counts
        print(f"batch {batch_id} is {batch.processing_status}: {c.processing} processing, {c.succeeded} succeeded")
        return False
    n = 0
    for result in client.messages.batches.results(batch_id):
        source, page = meta["pages"][result.custom_id]
        if result.result.type == "succeeded":
            parsed = parse_anthropic(result.result.message)
            rec = save(result.custom_id, "anthropic", source, page, meta["model"], meta["effort"], parsed)
            rec["cost_usd"] = round(rec["cost_usd"] / 2, 6)  # batch price is half
            cache_file(result.custom_id).write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
            n += 1
        else:
            print(f"  {source} p. {page}: {result.result.type}", file=sys.stderr)
    print(f"collected {n} pages from batch {batch_id}")
    return True


def write_jsonl(pages, system, model, effort):
    """Rewrite data/claims_raw.jsonl from the cache, in page order, for every selected page
    (1961 and colonial), whichever run produced it."""
    index = cache_index(model, effort)
    pages = every_page()
    n_pages = n_claims = errors = 0
    usage = {"uncached_input": 0, "cached_input": 0, "cache_write": 0, "output": 0, "reasoning": 0}
    dollars = 0.0
    with open(OUT, "w", encoding="utf-8") as f:
        for source, page in pages:
            path = index.get((source, page))
            if path is None:
                continue
            rec = json.loads(path.read_text(encoding="utf-8"))
            n_pages += 1
            errors += bool(rec["error"])
            dollars += rec.get("cost_usd", 0.0)
            for k in usage:
                usage[k] += rec["usage"].get(k, 0)
            for i, claim in enumerate(rec["claims"], 1):
                f.write(json.dumps({
                    "raw_id": f"{source}:{page}:{i}",
                    "source": source,
                    "pdf_page": page,
                    "text_file": str(source_text(source).relative_to(ROOT)),
                    "extracted_by": f"{rec['model_served'] or rec['model']} ({rec['prompt_version']}, effort {rec['effort']})",
                    **claim,
                }, ensure_ascii=False) + "\n")
                n_claims += 1
    print(f"{n_claims} claims from {n_pages} pages ({errors} pages with errors) written to {OUT.relative_to(ROOT)}")
    print("tokens: " + ", ".join(f"{k} {v:,}" for k, v in usage.items()) + f"; cost ${dollars:.4f}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--provider", choices=list(DEFAULT_MODEL), default="openai")
    ap.add_argument("--model", help="default: gpt-6-luna for openai, claude-opus-5-5 for anthropic")
    ap.add_argument("--effort", default="medium", choices=["none", "low", "medium", "high", "xhigh", "max"],
                    help="reasoning effort ('none' is OpenAI only)")
    ap.add_argument("--scope", choices=["study", "all", "colonial"], default="study",
                    help="study: the ten study villages and the 1961 reports; all: every village volume; "
                         "colonial: the 1881, Rose and 1931 pages in candidate_pages_colonial.csv")
    ap.add_argument("--refresh", action="store_true", help="re-send pages even if a cached response exists")
    ap.add_argument("--sources", help="comma-separated citation names, overrides --scope")
    ap.add_argument("--limit", type=int, help="only the first N pages")
    ap.add_argument("--budget", type=float, default=9.0,
                    help="US dollars: stop sending once recorded spend for the provider would pass this")
    ap.add_argument("--workers", type=int, default=4, help="concurrent requests")
    ap.add_argument("--batch", nargs="+", metavar=("submit|collect", "BATCH_ID"), help="Anthropic Batch API")
    ap.add_argument("--dry-run", action="store_true", help="print a cost estimate and stop")
    ap.add_argument("--no-api", action="store_true", help="only rebuild claims_raw.jsonl from the cache")
    ap.add_argument("--reindex-cache", action="store_true", help="rename cached responses to the current key scheme")
    args = ap.parse_args()
    model = args.model or DEFAULT_MODEL[args.provider]
    if args.provider == "anthropic" and args.effort == "none":
        ap.error("effort 'none' is not available for anthropic")
    if args.batch and args.provider != "anthropic":
        ap.error("--batch is only implemented for --provider anthropic")

    load_env()
    LLM_CACHE.mkdir(parents=True, exist_ok=True)
    if args.reindex_cache:
        reindex_cache()
    system = system_prompt()
    pages = selected_pages(args.scope, args.sources.split(",") if args.sources else None)
    if args.limit:
        pages = pages[:args.limit]

    if args.dry_run:
        done = cache_index(model, args.effort)
        todo = [(s, p) for s, p in pages if (s, p) not in done]
        sys_tok = len(system) / 4
        page_tok = sum(len(user_message(s, p)) for s, p in todo) / 4
        p = PRICES.get(model)
        print(f"{len(pages)} pages, {len(pages) - len(todo)} cached, {len(todo)} to send to {model}")
        print(f"system prompt about {sys_tok:,.0f} tokens; page text about {page_tok:,.0f} tokens in total")
        if p and todo:
            for out_per_page in (1500, 3000, 6000):
                est = (page_tok * p["input"] + sys_tok * p["input"] + sys_tok * (len(todo) - 1) * p["cached"]
                       + out_per_page * len(todo) * p["output"]) / 1e6
                print(f"  estimate at {out_per_page:,} output tokens a page: ${est:.2f}")
        print(f"recorded spend for {args.provider} so far: ${spent(args.provider):.4f}; budget ${args.budget:.2f}")
        return

    if not args.no_api and not os.environ.get(KEY_VAR[args.provider]) and \
            not (args.provider == "anthropic" and os.environ.get("ANTHROPIC_AUTH_TOKEN")):
        sys.exit(f"{KEY_VAR[args.provider]} is not set. Paste the key after {KEY_VAR[args.provider]}= in .env "
                 f"in the project folder, or export it.")

    if args.batch:
        if args.batch[0] == "submit":
            batch_submit(pages, system, model, args.effort)
            return
        if args.batch[0] == "collect" and len(args.batch) == 2:
            meta = json.loads((LLM_CACHE / "batches" / f"{args.batch[1]}.json").read_text(encoding="utf-8"))
            if not batch_collect(args.batch[1]):
                return
            model, args.effort = meta["model"], meta["effort"]
        else:
            ap.error("--batch takes 'submit' or 'collect BATCH_ID'")
    elif not args.no_api:
        t = time.time()
        run_api(pages, system, args.provider, model, args.effort, args.workers, args.budget, args.refresh)
        print(f"done in {time.time() - t:.0f} s")

    write_jsonl(pages, system, model, args.effort)


if __name__ == "__main__":
    main()
