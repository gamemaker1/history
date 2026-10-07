# Computational analysis log

This file records every computational process run on the sources for the
project *Seasonal herding in the Himachal hills, 1881 to 1961*
([ideas/research-question.pdf](ideas/research-question.pdf)). Each entry names
the script and the exact command, so anyone in the group can rerun it and get
the same output. Every script is in [scripts/](scripts/). Generated outputs
are in [analysis/](analysis/), and hand-checked inputs are in [data/](data/).

Page numbers are PDF page numbers (the page counter in a PDF viewer), not the
numbers printed on the scans, as in the idea files.

**Sub-questions** (from [ideas/seasonal-herding-himachal.md](ideas/seasonal-herding-himachal.md)):

- **SQ1, the cycle.** The herding calendar and routes, and how far 1961 matches 1881 and 1910.
- **SQ2, ownership and labour.** Who owns the flocks and the pastures, who herds, and who collects dues.
- **SQ3, change by 1961.** Permits, roads, road wages, the closed border, orchards.

---

## Environment and run order

```
brew install git-lfs && git lfs install --local && git lfs pull   # sources/ are Git LFS objects
uv venv .venv --python 3.12 && uv pip install --python .venv/bin/python -r requirements.txt
```

`pageref.py`, `kwic.py` and `candidate_pages.py` use only the standard
library and run with any Python 3. The others need `.venv/bin/python`.

| Order | Command | Entry |
| --- | --- | --- |
| 1 | `.venv/bin/python scripts/unpack_sources.py` | A0 |
| 2 | `python3 scripts/kwic.py --all-villages` | A2 |
| 3 | `python3 scripts/kwic.py --terms labour --all-villages` | A2 |
| 4 | `python3 scripts/candidate_pages.py` | A3 |
| 5 | `.venv/bin/python scripts/extract_claims.py --scope all --budget 2 --workers 8` (key in `.env`) | A5 |
| 6 | `python3 scripts/verify_claims.py` | A6 |
| 7 | `.venv/bin/python scripts/build_graph.py` | A7 |
| 8 | `.venv/bin/python scripts/query_graph.py` | A8 |
| 9 | `.venv/bin/python scripts/find_tables.py --render` (then the tables are read from the images, A9) | A9 |
| 10 | `.venv/bin/python scripts/flocks.py` | A10 |
| 11 | `.venv/bin/python scripts/resolve_entities.py`, then `--apply` (then rerun 6) | A11 |
| 12 | `.venv/bin/python scripts/check_claims.py` (then rerun 7 and 8) | A12 |

`verify_claims.py` also reads `data/flocks.csv`, so after changing the
livestock tables rerun steps 6, 7, 8 and 10.

Tools on demand: `python3 scripts/pageref.py find "<quote>"` gives the PDF page
of a quote. `.venv/bin/python scripts/render_page.py <source> <page>` renders a
page image to `cache/pages/` for reading tables.

## Use of AI in this project

Two AI systems did work that a reader of the essay should know about. Every
such step is listed here, and the entries below say which outputs it touched.

| System | What it did | Entries |
| --- | --- | --- |
| **OpenAI `gpt-6-luna`**, through `scripts/extract_claims.py` | Proposed 1,728 claims (subject, predicate, object, quote, page) from the OCR text of 428 selected pages | A5 |
| **Claude (Anthropic `claude-opus-5-5`)**, working in Claude Code at the group's request | Wrote every script in `scripts/`. Designed the schema, the entity list and the caste classes. Entered the hand-written claims from the idea files and the evidence packet | A1 to A10 |
| Claude, **reading page images** | Read the livestock tables of all 24 village surveys from page images rendered by `render_page.py` and `find_tables.py`, and typed the figures into `data/flocks.csv`. Also read Brahmaur p. 54 and Kothi p. 102 first, which found the missing Badhi row (A4), and the Chitrari shepherd's speech (two-column OCR). A second pass re-read the small-print tables from close-up crops at 250 dpi | A4, A9 |
| **OpenAI `gpt-6-luna`**, through `scripts/resolve_entities.py` | Proposed, for each of 597 names in claims that matched no entity, either an alias of an existing entity or a new entity. Claude reviewed the proposals and overrode 4 | A11 |
| **OpenAI `gpt-6-luna`**, through `scripts/check_claims.py` | Judged every text-based claim against its page (supported, partly supported, not supported, unclear), as a second pass independent of the extraction | A12 |
| Claude, **looking at screenshots** | Took headless-browser screenshots of the graph viewer (`kg.html`) and looked at the rendered charts (`analysis/flocks/*.png`), to check legends, overlapping labels and layout before calling them done. This changed the layout code only, not any data | A7, A10 |

Nothing an AI produced counts as checked until a person has checked it. The
AI-read figures carry `read_by` in `data/flocks.csv` and are marked
`image_unverified` in the graph until someone fills `checked_by` /
`verified_by`.

---

## A0. Source download and unpacking

- **Question served.** None directly. This makes the PDFs available for reading tables and checking quotes.
- **Script and command.** `git lfs pull`, then `.venv/bin/python scripts/unpack_sources.py`.
- **Inputs.** The 10 Git LFS objects in `sources/` (576 MB): the 1961 and 1881 zips, the 1931 Report and Tables, Rose Vols. 1 to 3, and the OCR text files.
- **Method.** Extract every PDF from both zips into `cache/pdf/1961/` and `cache/pdf/1881/`, keeping one copy per SHA-256 checksum. Where copies are duplicates, keep the one whose name matches a file in `text/`. Then count the pages of every PDF and compare with the number of form feeds in its text file.
- **Outputs.** `analysis/source_manifest.csv` (one row per PDF: pages, checksum, text file, page match), and `analysis/zip_members.csv` (every zip member and what it duplicates). `cache/pdf/` is not committed.
- **Result.** The zips hold 49 PDFs, of which 40 are distinct: 34 from 1961 and 6 from 1881. This agrees with [sources/index.md](sources/index.md). 44 of the 45 PDFs used have a text file, and **all 44 have exactly one form feed per PDF page**, so every page reference made through `text/` points to the right PDF page. The one PDF without text is `47123_1961_MAH.pdf` (Mahsa Tibba, Ambala, outside Himachal), which was left out on purpose. Spot check: `render_page.py Brahmaur 54` shows the flocks-by-caste table (Brahman 34 / 20 / 2,027; Rajput 49 / 20 / 2,364; Sipi 15 / 8 / 93; total 99 / 48 / 4,484), as cited in the idea files.
- **Caveats.** None.
- **Run.** 7 Oct 2026, Vishak, on commit `5f07457` plus uncommitted scripts.

## A1. Shared corpus helpers

- **Question served.** None directly. Every later script uses the same paths, page counting and text normalisation.
- **Script.** [scripts/corpus.py](scripts/corpus.py), which holds the shared code formerly in `pageref.py` and `kwic.py` (PDF names, hyphen rejoining, normalised tokens), plus the list of the 24 village volumes and the four 1961 reports with their citation names.
- **Check.** `pageref.py find "grazing rights belonged to the rajah"`, `find "Pohals are hired in summer season"` and `line ... Kanum ... 5059` give identical output before and after the change: Newell p. 18, Brahmaur p. 55 and Kanum p. 51.
- **Note on the corpus.** There are **24 village volumes**, not 25. Kupha's volume covers four Pangi villages (Kupha, Parmas, Thamoh, Malet), and the 25th monograph in the zip, Mahsa Tibba, is outside Himachal.
- **Run.** 7 Oct 2026, Vishak.

## A2. Herding vocabulary across the four source layers

- **Question served.** SQ1 and SQ3, both readings. Does the language of seasons and routes persist from 1881 to 1961? Does the language of permits, fees and the forest appear beside it?
- **Script and command.** [scripts/kwic.py](scripts/kwic.py): `python3 scripts/kwic.py --all-villages` (herding terms) and `python3 scripts/kwic.py --terms labour --all-villages` (the earlier begar and labour terms, kept for comparison).
- **Inputs.** All of `text/1881`, `text/rose`, `text/1931`, the 24 village volumes in `text/1961`, and the Newell, Weaving, Mahasu and Simla volumes.
- **Method.** Keyword in context and counts per 10,000 words for ten term groups: flocks, shepherds, herding peoples, pasture, season and route, rights and dues, forest and state, trade, debt, and wage work. The patterns and the OCR spellings they cover are in `TERM_SETS` in the script. The names of herding peoples (Gaddi, Gujjar, Kinnaura) are a separate group from shepherd roles (malundi, pohal, fawal), because otherwise a Gujjar village reads as all shepherds. *Programming Historian:* "Keywords in Context (Using n-grams) with Python", "Counting Word Frequencies with Python".
- **Outputs.** `analysis/kwic_herding.csv` (14,283 matches, each with its PDF page and 20 words of context either side, plus empty `code` and `note` columns for hand coding), `analysis/term_rates_herding.csv`, `analysis/kwic_labour.csv` (4,755 matches) and `analysis/term_rates_labour.csv`.
- **Result** (rates per 10,000 words):
  - **Trade vocabulary separates the two valleys.** Kanum 33.6, Kothi 14.3 and Nachar 13.0 on the upper Sutlej, against Brahmaur 8.3, Chitrari 8.4 and Maingal 6.6 on the Ravi. The Weaving survey is the highest of all at 81.0, which fits its account of wool and pashm after the Tibet trade stopped.
  - **Herding vocabulary picks out the high herding villages.** Flocks: Brahmaur 27.1, Maingal 20.5, Chitrari 20.2, Kothi 17.8, Kanum 17.8, against 6 to 7 for Chaunri, Pangna, Shathla and Shakrori. Season and route: Kupha 38.9 and Brahmaur 25.1, against 4.6 to 7.3 for Basal, Bir, Pangna and Shakrori.
  - **Rights and dues are densest where Newell and the Chamba surveys describe the permit system.** Newell 6.0, Devi-Kothi 5.7, Brahmaur 3.8. The Kinnaur villages score 1.1 to 2.2 and the colonial layers 0.3 to 1.4. Forest-state vocabulary is almost absent before 1961 (0.00 in 1881 and Rose, 0.04 in 1931).
  - **Debt vocabulary is highest in Chergaon (19.0), Maingal (17.6) and Rajana (15.5).** Maingal is the Gujjar village recorded as "cent per cent under debt".
- **Caveats.**
  - The 1881, 1910 and 1931 layers are pooled over the whole of Punjab, so their rates are diluted by plains material. Compare them with each other, not with single villages.
  - Some patterns catch unrelated senses: "fees" matches school fees, "interest" matches non-financial uses, and "Kangra" appears in many contexts. The rates are a first map. Claims must come from coded KWIC rows or the pages themselves.
  - Garbled table OCR undercounts terms that appear mainly in tables.
- **Run.** 7 Oct 2026, Vishak.

## A3. Candidate pages for claim extraction

- **Question served.** All three sub-questions. This picks the pages from which the knowledge-graph claims are drawn, which is the step from distant reading to close reading.
- **Script and command.** [scripts/candidate_pages.py](scripts/candidate_pages.py): `python3 scripts/candidate_pages.py`.
- **Inputs.** Every page of the 24 village volumes and the four 1961 reports, using the herding term groups from A2. Recall is checked against [data/cited_pages.csv](data/cited_pages.csv), the 65 pages cited in the idea files and the evidence packet.
- **Method.** For each page, count hits per term group. Select the page if any of these holds:
  1. at least 6 hits across at least 3 groups;
  2. any rights, dues, forest or debt term together with a flocks, pasture or shepherd term;
  3. at least 8 hits in a single group.

  The third rule was added after a first run (rules 1 and 2 only) selected 364 pages with recall of 52 of 65, missing pages given over to one topic, such as Kanum p. 55 on debt and Weaving p. 16 on wool.
- **Outputs.** `analysis/candidate_pages.csv`: one row per page with hits per group, score and `selected`.
- **Result.** **3,754 pages scored, 428 selected (11%).** Recall on cited pages is **56 of 65 (86%)**. Selections per volume run from 1 (Chaunri) to 43 (Brahmaur). Newell has 35, Kanum 32, Kupha 22, and Chitrari and Maingal 20 each. The nine misses are:
  - three pages that place a village on its river (Brahmaur p. 11, Chitrari p. 16, Tandi p. 11). These go into the graph by hand from the river table in the idea file.
  - four livestock table pages (Kothi p. 102, Tandi p. 56, Chergaon p. 56, Chauntra p. 46). These are read from the page images into `data/flocks.csv`.
  - two passing mentions on otherwise off-topic pages (Newell p. 14, wool "in lieu of revenue"; Chitrari p. 39, woollens sold at Chamba). These are entered by hand.
- **Caveats.** The thresholds are judgement calls, tuned against pages we already knew about, so recall on unknown pages may be lower. The selection favours villages with a lot of herding text, which is intended, but it means low villages contribute fewer claims.
- **Run.** 7 Oct 2026, Vishak.

## A4. Knowledge-graph schema, entities and hand-entered claims

- **Question served.** All three sub-questions. This is the evidence base that the calendar, the map, the ownership tables and the payment-flow graph are drawn from.
- **Files.**
  - [scripts/kg_schema.py](scripts/kg_schema.py): 7 entity types and 22 predicates in 8 families (movement, geography, property, extraction, exchange, labour, event, voice), the `when` values, and the JSON schema for extracted claims.
  - [data/entities.csv](data/entities.csv): 135 entities with aliases for OCR and spelling variants (Bhrhmaur/Barmor, Gadi/Gaddi, Chandrabhaga/Chenab ...), and the river system of each village where the survey names it.
  - [data/claims_manual.csv](data/claims_manual.csv): 61 claims entered by hand from the idea files and the evidence packet. These cover the colonial layers (1881, Rose, 1931), Newell, the river locations, and the passages the page selection in A3 misses.
- **Design.** A claim is *subject, predicate, object*, plus optional resource (what is sold, lent or charged for), quantity, unit, months, place, `when` and date text. It always carries the source, PDF page and verbatim quote. The `resource` field was added after the first graph build. Without it, Newell's "permits are freely bought and sold amongst shepherds" could not be told apart from an ordinary sale, and was put in the trade conjuncture instead of the Forest Department one.
- **Correction to the idea files.** Kothi's livestock table (Kothi p. 102, read from the page image) has **four** caste rows. The idea files list three: Rajput 2,416, Koli 72, Lohar 58. They leave out **Badhi: 2 households, 11 goats and sheep**. The village total is therefore 2,557, not 2,546, and the Rajput share is **94.5%, not 94.9%**.
- **Run.** 7 Oct 2026, Vishak.

## A5. Claim extraction with a language model

- **Question served.** All three. It proposes claims from the 428 selected pages (A3), for checking in A6.
- **Script and command.** [scripts/extract_claims.py](scripts/extract_claims.py): `.venv/bin/python scripts/extract_claims.py --scope all --budget 2 --workers 8`. `--dry-run` prints a cost estimate without sending anything. `--no-api` rebuilds `data/claims_raw.jsonl` from the cache.
- **Model.** OpenAI `gpt-6-luna` at reasoning effort `medium`, chosen by the group for cost (USD 0.10 per million input tokens, 0.01 cached, 0.50 output, from OpenAI's pricing page on 7 Oct 2026). There is no "gpt-6.1-luna": the 6.1 family has only `gpt-6.1-sol`, at 20 times the price. The script also supports Anthropic (`--provider anthropic`, `claude-opus-5-5`, with a Batch API option), which was not used.
- **Method.**
  - **Request.** Each request sends one page of OCR text. Output is structured JSON constrained by OpenAI strict mode to `kg_schema.CLAIM_SCHEMA`, with nullable fields written as `"type": [t, "null"]`. The system prompt holds the research question, the rules, the predicate list and the entity list, and is the same for every page, so it is served from OpenAI's prompt cache (`prompt_cache_key`). Responses are not stored by OpenAI (`store=False`).
  - **Rules.** The prompt requires every quote to be copied character for character from the page.
  - **Caching.** Responses are cached in `cache/llm/`, keyed by prompt version, model, effort, prompt and page, with token usage and cost. Reruns cost nothing.
  - **Budget.** The script stops sending once the recorded spend, plus the worst case for every request in flight, would pass `--budget`.
- **Test on one page (Newell p. 9).** The request returned 7 claims, and all 7 quotes verified exactly (A6). Two place names were missing from the entity list: Gadaren, the Gaddi homeland, and Kashmir. Both were added. Token use was 5,122 input and 3,752 output, of which 3,016 were reasoning. Cost: USD 0.0024 for the page, which projects to about USD 1 for all 428 pages.
- **Caveats.** The model can misread a page even when its quote is genuine. A6 catches invented, altered or mis-paged quotes, but not a wrong reading of a real one. That is why a person signs off every claim used in the essay. Luna is OpenAI's smallest current model, so expect more misreadings than from a larger one. The sign-off sample in A6 measures how many.
- **Result of the full run.**
  - **Volume.** All 428 pages were sent with no errors, in 809 seconds with 8 parallel requests. The model returned **1,728 claims** from 301 pages; the other 127 pages gave none.
  - **Tokens.** 461,988 uncached input, 1,650,355 cached input (the shared prompt), and 756,881 output, of which 573,734 were reasoning.
  - **Cost.** **USD 0.44**, plus USD 0.0024 for the one-page test, against a USD 2 cap.
  - **What it returned.** The commonest predicates were OWNS (278 kept), HAS_POPULATION (160), MIGRATES_TO (150), LENDS_TO (145), WORKS_AS (144) and GRAZES_AT (116).
- **Run.** 7 Oct 2026, Vishak (run by Claude in Claude Code, at the group's request).

## A6. Claim verification

- **Question served.** Source criticism for all three. No claim enters the graph unless its quote is on the cited page.
- **Script and command.** [scripts/verify_claims.py](scripts/verify_claims.py): `python3 scripts/verify_claims.py`.
- **Method.** For each claim in `claims_raw.jsonl` and `claims_manual.csv`, the script searches the cited page of the text in `text/`:
  - **exact:** the quote's words appear in order;
  - **fuzzy:** character similarity of at least 0.85 against some stretch of the page, **and every number in the quote present in that stretch**;
  - **adjacent:** found on the page before or after, and the page is corrected.

  Claims typed from page images (tables, or two-column text the OCR interleaves) are marked `image` and count only after sign-off. Subject, object, place and resource are matched to `entities.csv`. Each claim also gets a `qty_in_quote` flag. Human sign-off columns survive reruns.
- **Tests** (run by hand on 7 Oct; inputs and results below):

  | Test quote | Result |
  | --- | --- |
  | Real quote, right page | exact |
  | Real quote, OCR differs ("I n the hills the Gujnrs ...", 1881 p. 267) | fuzzy 0.977 |
  | Real quote, page off by one | adjacent, page corrected |
  | Real quote, page off by two | rejected |
  | Invented sentence | rejected |
  | Paraphrase of a real sentence | rejected (0.56) |
  | **Real quote with "Rs. 15" changed to "Rs. 25"** | **accepted at 0.989 by the first version**; rejected after the number rule was added |
  | Real quote with the year changed (1950 to 1951) | rejected |
  | Real quote, correct number, an OCR slip in one word | fuzzy 0.989 |
- **Result.** All 61 hand-entered claims kept: 45 exact, 3 fuzzy, 13 image. All entities resolved. The `qty_in_quote` flag caught two weak hand entries, which were then corrected:
  - Maingal's 30% interest was attached to a quote without the figure;
  - Bir's price was entered as 11, a midpoint of "10 to 12", as if the source said it.

  One flag remains, legitimately: Rehara's 0 animals, printed as "..".
- **Result on the model's claims (A5).** Of 1,728 claims:
  - **1,639 kept** (94.8%): 1,563 exact quotes, 76 fuzzy;
  - **43 rejected** (2.5%), with quotes not found on the cited page or the pages beside it;
  - 46 dropped as exact duplicates.

  Most rejections are quotes stitched together from scrambled table OCR (for example Mahasu p. 26), or paraphrases (best match 0.63 to 0.85).

  Of the kept claims, 828 name only entities already in `entities.csv`. 811 use at least one new name, 601 distinct names in all, listed in `analysis/unresolved_entities.csv`: people (Lal Chand Negi), places (Simla District, Goshen, Lower Kugti) and generic words (farmers, milk). Those still enter the graph, as dashed "uncurated" nodes.

  A quote being genuine does not make the claim right. In the sample read on 7 Oct, one claim had Gaddis grazing in Pangi's demarcated forests. Its quote says they have *no rights* there but trespass. A semantic check of claims against their pages is still to do.
- **Note on OCR.** Newell's "wool in lieu of revenue" (p. 14) is correctly cited, but the OCR reads `I('Cci \'ed ,,'ool in lieu of rC\CtlliC`, which is why `pageref.py` could not find it. Quotes for the essay should be checked against the page image.
- **Run.** 7 Oct 2026, Vishak.

## A7. Building the graph and the Cytoscape views

- **Question served.** SQ2 and SQ3 (Marxist): who takes a share from whom in each conjuncture. SQ1 (Annales): the movement network.
- **Script and command.** [scripts/build_graph.py](scripts/build_graph.py): `.venv/bin/python scripts/build_graph.py` (`--evidence human` keeps only signed-off claims).
- **Method.**
  - **Graph.** A networkx MultiDiGraph with one edge per claim. Groups and roles are scoped to their village (for example "Rajput (Brahmaur)" and "Rajput (Kothi)"). Without this, a single "households" node joined every village into one hub.
  - **Conjunctures.** Each claim is assigned by ordered rules in `conjuncture()`:
    1. two sovereigns;
    2. standing ownership;
    3. Forest Department;
    4. princely pastures;
    5. roads and wages;
    6. trade and credit;
    7. the cycle.

    The first build misplaced three claims, all fixed: Barnes on Gaddi fines to Chamba, the Gartok trade, and the permit market.
  - **Visual encoding.** Shape encodes node type. Colour is kept for three edge families: movement (blue, dashed), extraction (orange) and property (aqua). Exchange and labour are dark grey, dotted and dashed. The rest are light grey. Five colours failed the all-pairs check for colour-blind and normal vision (magenta against orange, normal-vision ΔE 12.9 below the floor of 15). The three used pass all pairs: worst colour-blind ΔE 9.2, normal-vision 24.0. Aqua is below 3:1 contrast, so the viewer has a table view of the visible claims and shows each edge's quote on click.
- **Outputs** in `analysis/graph/`:
  - `kg.html`: the viewer, with filters for conjuncture, valley, source layer, evidence and relation family;
  - `kg.cyjs`, plus one `kg_<conjuncture>.cyjs` per conjuncture, for Cytoscape Desktop;
  - `kg.graphml`;
  - `nodes.csv` and `edges.csv`.
- **Result with all claims (7 Oct, evening).** 878 nodes and 1,854 edges: 1,680 with a quote verified against the text, and 174 read from page images and not yet checked by a person.

  | Conjuncture | Claims |
  | --- | --- |
  | standing | 769 |
  | trade and credit | 387 |
  | cycle | 380 |
  | roads and wages | 180 |
  | princely pastures | 75 |
  | Forest Department | 59 |
  | two sovereigns | 4 |

  517 nodes are uncurated (see A6).
- **Checking the layout.** Claude took headless Chrome screenshots of `kg.html` and looked at them. The first version printed the names of node shapes in the legend, where they overflowed, and its central labels collided. It was changed to draw the shapes and to spread the layout. The screenshots also showed that a single "households" node joined every village into one hub, which led to scoping groups and roles by village.
- **Result** (first build, hand-entered claims only). 61 nodes and 61 edges:

  | Conjuncture | Claims |
  | --- | --- |
  | standing | 18 |
  | cycle | 13 |
  | trade and credit | 9 |
  | princely pastures | 7 |
  | Forest Department | 7 |
  | roads and wages | 4 |
  | two sovereigns | 3 |
- **Run.** 7 Oct 2026, Vishak.

## A8. Graph queries and regression check

- **Question served.** SQ2. Also a check that the graph reproduces the figures already cited.
- **Script and command.** [scripts/query_graph.py](scripts/query_graph.py): `.venv/bin/python scripts/query_graph.py`. It exits 1 if a check fails.
- **Outputs.** In `analysis/queries/`:
  - `flock_shares.csv`: animals by caste and village, share, households;
  - `conjunctures.csv`;
  - `extraction.csv`: every edge where one party takes a share;
  - `single_source.csv`.
- **Result.** All five checks pass on all kept claims:
  - Brahmaur: Brahman and Rajput share of sheep and goats 97.9%, village total 4,484, 45.3 animals per household;
  - Kothi: Rajput share **94.5%**, village total **2,557** (corrected, see A4).

  With `--evidence auto` the checks fail, as they should: the table figures were typed from page images and are not yet signed off. Every one of the 61 claims rests on a single source so far.
- **Run.** 7 Oct 2026, Vishak.

## A9. Livestock tables read from page images (by Claude)

- **Question served.** SQ2 (who owns the flocks) and the Annales comparison of high and low villages.
- **Scripts and command.**
  - [scripts/find_tables.py](scripts/find_tables.py): `.venv/bin/python scripts/find_tables.py --render`. It scores every page of the 24 village volumes for livestock words plus density of numbers, and renders the best pages. Output: `analysis/table_pages.csv`.
  - [scripts/render_page.py](scripts/render_page.py): renders further pages, and `--find WORD --dpi 250` makes close-up crops around a table.
- **Who read the figures.** **Claude** (`claude-opus-5-5` in Claude Code) read every table from the rendered images and typed the figures into [data/flocks.csv](data/flocks.csv). The table has 131 rows, one per caste per village, plus village totals where no caste table is printed. Each row has its page, `read_by` and an empty `checked_by` for the group. Castes printed as ".." are entered as 0, because who owns nothing matters for the analysis.
- **Coverage.**
  - **Caste tables (18 villages):** Brahmaur, Maingal, Kanum, Kothi, Shakrori, Nalag, Kupha, Tandi, Chauntra, Kot, Chergaon, Rajana, Chaupal (goats only), Chaunri, Basal, Batal, Moginand, Pangna.
  - **Village totals only (4 villages):** Devi-Kothi and Kalath (cattle census figures), Chitrari (cattle census, rabi 1960), and Bir (prose).
  - **No figures (2 villages):** Nachar ("100 to 200 sheep and goats are kept by a family") and Shathla ("owned by two or three families", p. 46).
- **Finding tables.** `find_tables.py` put a livestock table first or second for most villages. It missed Tandi, whose table is in an appendix at p. 96, and Chitrari, whose figures are in a list at p. 52. Claude found those by following the text ("Table 12") and by searching for figures quoted in the idea files.
- **Errors found by the second pass.** At 140 dpi Claude read Nalag's Rajput goats as **230**. A 260 dpi crop shows **239**, which makes the total 241 and agrees with the idea file. After that, 13 small-print tables were re-read from 250 dpi crops. All 13 matched the first reading (Kanum, Kupha, Rajana, Basal, Kothi, Shakrori, Chauntra, Batal, Pangna, Kot, Chaunri, Nalag, and Brahmaur through its printed total). The remaining tables are in large print, or their rows add up to a printed total (see A10).
- **Doubts recorded in the notes column.**
  - **Chaupal.** One column (total 107) has no printed heading.
  - **Pangna.** The table gives 1 Mahajan household with 9 sheep and goats, but the prose on the same page says Mahajans keep none.
  - **Maingal.** The table gives Gujjars 139 sheep, while the prose speaks only of the Gaddi brahmins' flocks.
- **Run.** 7 Oct 2026. Figures read by Claude; not yet checked by the group.

## A10. Who owned the flocks: ownership by caste class

- **Question served.** SQ2 (Marxist: ownership of the means of production), and the Annales comparison of high and low villages.
- **Script and command.** [scripts/flocks.py](scripts/flocks.py): `.venv/bin/python scripts/flocks.py`.
- **Inputs.**
  - `data/flocks.csv` (A9).
  - [data/caste_classes.csv](data/caste_classes.csv): every caste name in the tables classed as landholding, scheduled caste, herding tribe, trading or other. This is our classification, written by Claude. Rows marked `check` need checking against the *1961 Special Tables on Scheduled Castes and Scheduled Tribes, Himachal Pradesh* (in `sources/`).
  - The river system of each village, from `entities.csv`.
- **Checks.** The rows of each table are summed against the totals the table prints, or the text beside it states. **15 of 15 pass**: Brahmaur, Chergaon, Moginand, Chauntra, Tandi, Shakrori and Kupha.
- **Outputs.** In `analysis/flocks/`:
  - `checks.csv`, `by_group.csv` and `village_summary.csv`;
  - `ownership_shares.png`: stacked bars by caste class per village;
  - `flock_size.png`: sheep and goats per village, log scale.

  Colours are slots 1 to 5 of the reference palette, validated for adjacent pairs. A legend is present and each bar is labelled with its total. Claude looked at both charts before finishing; one axis label was changed from scientific notation.
- **Result.**
  - **Pooled** over the caste tables (12,210 sheep and goats), landholding castes own **89.3%**, scheduled castes 8.1%, Gujjars 1.6%, trading castes 0.2%, others 0.9%.
  - **The high herding villages** on the Ravi, Sutlej, Chenab and Beas give landholding castes 92 to 99%: Brahmaur 97.9, Kothi 94.5, Kanum 95.5, Nalag 98.6, Kupha 93.0, Tandi 92.2, Kot 98.6. Maingal is the exception (54.6%), where the Gujjars, a herding tribe, hold 43%.
  - **The pattern reverses in the Yamuna-side and Shimla-hills villages**, where flocks are small and mostly goats. Koli households (a scheduled caste) hold the majority: Chaunri 91.1% scheduled caste, Pangna 67.7%, Rajana 59.9%, Moginand 42.5%.

  Concentration in the landholding castes therefore holds in the large herding economies but not in every hill village. **Correction (A16):** it is not an effect of altitude. Low Shakrori (518 m), Kot and Nalag are over 95% landholding too, and the rank correlation between altitude and the landholding share is −0.05. The reversal is regional: it follows the caste structure of the Yamuna side and the Shimla hills, where Kolis are a large part of the cultivating population.
- **Caveats.** Shares are by caste, not by household, so they say nothing about inequality inside a caste. Village household totals, needed for animals per household across all villages, are not yet collected. The caste classes need checking. Four villages have totals but no caste table.
- **Run.** 7 Oct 2026, Vishak (scripts run by Claude).

## A11. Entity resolution

- **Question served.** All three. Claims about the same thing have to meet at the same node, or the graph splits one pasture, caste or moneylender into many.
- **Scripts and command.**
  - [scripts/resolve_entities.py](scripts/resolve_entities.py): `.venv/bin/python scripts/resolve_entities.py`, then `--apply`.
  - [scripts/llm.py](scripts/llm.py): the shared OpenAI call, cache and budget code.
- **Method.**
  - **Request.** The 597 names that matched no entity after A6 were sent to `gpt-6-luna` (effort medium) in batches of 30. Each name went with up to two example claims and the whole entity list. For each name the model answered "alias" (an existing entity id) or "new" (label, type, subtype), with a reason.
  - **Audit trail.** The answers are in [data/entity_resolution.csv](data/entity_resolution.csv), one row per name with an `accepted` column. `--apply` merges them into `entities.csv`. New entities carry `added_by`, which names the model and marks them "to check". Names proposed under the same new label become one entity.
  - **New type.** A `person` type was added to the schema first, because named individuals (Lal Chand Negi, Padam Ram, the Jethu household) were being forced into "group".
- **Claude's review of the proposals.** The 110 alias proposals were read, and most were right: Bharmour variants, "mahlundi" to malundi, "odhwaries" to pasture, "unspecified lenders" to moneylender. Four were overridden:
  - **"ban".** Proposed as an alias of pasture. Claude first took *ban* to be the oak whose leaves are winter fodder, but the claims come from Newell p. 18: "Each ban in Kangra is claimed by a Gaddi as its warisi (inheritance)". There a *ban* is a winter grazing run, so it became its own entity, "ban (grazing run)": hereditary Gaddi rights in Kangra's grazing runs are evidence for SQ2.
  - **"the valley".** Its meaning depends on context, so it cannot be a global alias. Rejected; 3 claims stay unresolved.
  - **"Tibetans from Kinnaur".** The model aliased it to Bhot, a different community. Made a new entity.
  - **"mobile Gujjars, Gaddis and Kannaura".** Aliasing to Gaddi would drop two of the three groups. Made a new entity.

  The 487 new-entity proposals were spot-checked. "Goshen", in 23 claims, is the hamlet below Brahmaur that Newell studied (Newell p. 30), so it is correct as a new place.
- **Result.** 123 aliases added and 463 new entities, so 627 entities in all. Claims resolving to entities rose **from 869 to 1,677 of 1,680** text-based claims; the 3 left are the "the valley" claims. Cost: **USD 0.042**.
- **Caveats.** 463 new entities came from the model and are marked to check. Some are near-duplicate roles ("sheep breeder", "sheep and goat rearer", "shepherd") that a person may want to merge. Aliases are global, so a context-bound alias ("Ruling Chief" for the Bushahr ruler, from Kanum) would be wrong in another village; there is one such case.
- **Also changed.** `extract_claims.py` used to key its cache on the whole system prompt, which includes the entity list, so any change to `entities.csv` would have orphaned all 428 paid responses. The key is now prompt version, model, effort and page text. `--reindex-cache` renamed the existing files. The rebuilt `claims_raw.jsonl` is byte-identical to the one before (checked with `cmp`).
- **Run.** 7 Oct 2026 (run by Claude).

---

## Methods considered and not used

- **Topic modelling** (*Getting Started with Topic Modeling and MALLET*). All 24 volumes follow the same Census chapter template, so the topics would reproduce the chapter headings rather than anything about herding.
- **Word embeddings** (*Understanding and Creating Word Embeddings*). The village volumes total about 1.15 million words (1.6 million with the four reports), with noisy OCR. That is too small for stable vectors.
- **Sentiment analysis.** Modern sentiment lexicons say nothing reliable about bureaucratic census prose.
- **Neo4j or RDF triple store** (*Dealing with Big Data and Network Analysis Using Neo4j*, *Intro to Linked Open Data*). The knowledge graph has a few thousand claims, and CSV plus networkx handles that without a database server. Places will carry Wikidata QIDs, so the data can still link out.
