"""Shared helpers for the scripts that call a language model (OpenAI by default).

  load_env()        read KEY=value lines from .env into the environment
  PRICES, cost()    US dollars per million tokens, and the cost of one response
  openai_schema()   a JSON schema in the form OpenAI strict mode documents
  structured()      one Responses API call with a strict JSON schema, returning
                    (parsed JSON, error, usage, model served)
  run_cached()      run many such calls in parallel, cached on disk, under a
                    hard budget in US dollars

extract_claims.py keeps its own request code (it also supports Anthropic);
resolve_entities.py and check_claims.py use run_cached().
"""

import hashlib
import json
import os
import sys
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait

from corpus import CACHE, ROOT

# US dollars per million tokens, from the providers' pricing pages on 7 Oct 2026.
# OpenAI output tokens include reasoning tokens.
PRICES = {
    "gpt-6-luna": {"input": 0.10, "cached": 0.01, "cache_write": 0.10, "output": 0.50},
    "gpt-6.1-sol": {"input": 2.00, "cached": 0.10, "cache_write": 2.00, "output": 10.00},
    "claude-opus-5-5": {"input": 4.00, "cached": 0.20, "cache_write": 5.00, "output": 20.00},
}
MAX_OUTPUT_TOKENS = 16000


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


def cost(model, usage):
    p = PRICES.get(model)
    if not p:
        return 0.0
    return (usage["uncached_input"] * p["input"] + usage["cached_input"] * p["cached"]
            + usage["cache_write"] * p["cache_write"] + usage["output"] * p["output"]) / 1e6


def openai_schema(schema):
    """Nullable fields as "type": [t, "null"] rather than anyOf, as OpenAI strict mode documents."""
    if isinstance(schema, dict):
        alts = schema.get("anyOf")
        if alts and len(alts) == 2 and {"type": "null"} in alts:
            other = next(a for a in alts if a != {"type": "null"})
            rest = {k: v for k, v in schema.items() if k != "anyOf"}
            if "enum" in other:
                return {**rest, "type": [other["type"], "null"], "enum": other["enum"] + [None]}
            return {**rest, "type": [other["type"], "null"]}
        return {k: openai_schema(v) for k, v in schema.items()}
    if isinstance(schema, list):
        return [openai_schema(v) for v in schema]
    return schema


def nullable(t, enum=None):
    inner = {"type": t, **({"enum": enum} if enum else {})}
    return {"anyOf": [inner, {"type": "null"}]}


def structured(client, model, effort, instructions, user, schema, name, cache_key_prefix):
    """One OpenAI Responses API call constrained to a strict JSON schema."""
    response = client.responses.create(
        model=model,
        instructions=instructions,
        input=[{"role": "user", "content": user}],
        text={"format": {"type": "json_schema", "name": name, "schema": openai_schema(schema), "strict": True}},
        reasoning={"effort": effort},
        max_output_tokens=MAX_OUTPUT_TOKENS,
        prompt_cache_key=cache_key_prefix,
        store=False,
    )
    u = response.usage
    cached = (u.input_tokens_details.cached_tokens or 0) if u.input_tokens_details else 0
    usage = {"uncached_input": u.input_tokens - cached, "cached_input": cached, "cache_write": 0,
             "output": u.output_tokens,
             "reasoning": (u.output_tokens_details.reasoning_tokens or 0) if u.output_tokens_details else 0}
    if response.status == "incomplete":
        return None, f"incomplete: {getattr(response.incomplete_details, 'reason', None)}", usage, response.model
    message = next((item for item in response.output if item.type == "message"), None)
    part = message.content[0] if message and message.content else None
    if part is None:
        return None, "no output", usage, response.model
    if part.type == "refusal":
        return None, f"refusal: {part.refusal}", usage, response.model
    try:
        return json.loads(part.text), None, usage, response.model
    except json.JSONDecodeError as e:
        return None, f"bad json: {e}", usage, response.model


def key_for(*parts):
    h = hashlib.sha256()
    for part in parts:
        h.update(str(part).encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()[:32]


def run_cached(task, jobs, *, model, effort, instructions, schema, name, prompt_version,
               budget, workers=8, reserve_tokens=20000):
    """Run jobs [(job_id, user_message)] through structured(), with a disk cache and a budget.

    Results are cached in cache/llm_tasks/<task>/ under a hash of the prompt version, model,
    effort, instructions and user message. Returns {job_id: record}. Stops sending once the
    spend recorded for this task, plus a worst-case reserve for each request in flight,
    would pass the budget (US dollars).
    """
    import openai

    load_env()
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY is not set. Paste the key after OPENAI_API_KEY= in .env, or export it.")
    folder = CACHE / "llm_tasks" / task
    folder.mkdir(parents=True, exist_ok=True)

    def path_for(job_id, user):
        return folder / f"{key_for(prompt_version, model, effort, instructions, user)}.json"

    results, todo = {}, []
    for job_id, user in jobs:
        p = path_for(job_id, user)
        if p.exists():
            results[job_id] = json.loads(p.read_text(encoding="utf-8"))
        else:
            todo.append((job_id, user))
    spent = sum(json.loads(p.read_text(encoding="utf-8")).get("cost_usd", 0.0) for p in folder.glob("*.json"))
    price = PRICES.get(model, {"input": 0, "output": 0})
    reserve = (reserve_tokens * price["input"] + MAX_OUTPUT_TOKENS * price["output"]) / 1e6
    print(f"{task}: {len(jobs)} requests, {len(jobs) - len(todo)} cached, {len(todo)} to send to {model}; "
          f"spent so far ${spent:.4f} of a ${budget:.2f} budget")

    client = openai.OpenAI()

    def one(job_id, user):
        parsed, error, usage, served = structured(client, model, effort, instructions, user, schema, name,
                                                  f"{task}-{prompt_version}")
        rec = {"task": task, "job_id": job_id, "prompt_version": prompt_version, "model": model,
               "model_served": served, "effort": effort, "error": error, "usage": usage,
               "cost_usd": round(cost(model, usage), 6), "result": parsed}
        path_for(job_id, user).write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        return rec

    queue, in_flight, done, stopped = list(todo), {}, 0, False
    with ThreadPoolExecutor(max_workers=workers) as pool:
        while queue or in_flight:
            while queue and len(in_flight) < workers:
                if spent + reserve * (len(in_flight) + 1) > budget:
                    stopped = True
                    break
                job_id, user = queue.pop(0)
                in_flight[pool.submit(one, job_id, user)] = job_id
            if not in_flight:
                break
            finished, _ = wait(in_flight, return_when=FIRST_COMPLETED)
            for fut in finished:
                job_id = in_flight.pop(fut)
                done += 1
                try:
                    rec = fut.result()
                    spent += rec["cost_usd"]
                    results[job_id] = rec
                    flag = f" [{rec['error']}]" if rec["error"] else ""
                    print(f"  {done:4d}/{len(todo)} {job_id}: ${rec['cost_usd']:.4f} (task total ${spent:.4f}){flag}",
                          flush=True)
                except (openai.APIStatusError, openai.APIConnectionError) as e:
                    print(f"  {done:4d}/{len(todo)} {job_id}: API error: {e}", file=sys.stderr, flush=True)
            if stopped:
                queue.clear()
    if stopped:
        print(f"{task}: stopped at the ${budget:.2f} budget with requests left unsent; raise --budget to continue")
    print(f"{task}: spent ${spent:.4f} in total")
    return results
