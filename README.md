# The Mountain Year and Its Owners

**Seasonal herding in the Himachal hills, 1881–1961: a computational history.**
Course project for *Introduction to History* (HS3.201), IIIT Hyderabad, Monsoon 2026.
Vishak Kashyap, Vedant Kulkarni, Himangi Sahoo.

We asked how the seasonal movement of flocks between high summer pastures and
low winter grazing shaped life in the Himachal hills between 1881 and 1961,
and who controlled and profited from it. We read the 1961 Census village
surveys against the 1881 and 1931 Punjab censuses and H. A. Rose's *Glossary*,
and built an **evidence graph of 1,964 sourced claims**. Each claim is tied to
a verbatim quotation and the page it comes from, and the essay's argument is
built from queries on it.

**Our answer.** Geography fixed the *form* of the mountain year: the same
months and routes appear in 1881, 1911 and 1961, in independent sources, and
large flocks are found only above about 2,000 m in the Ravi, Sutlej and Chenab
valleys. Ownership of the flocks stayed with the landholding castes (89% of
the animals in the caste tables). What changed was who took a share of the
herders' product. It passed from the raja and his fee contractor to the Forest
Department and its permits, which became property in their own right, and to
moneylenders and shopkeepers.

## What to read

| File | What it is |
| --- | --- |
| [essay/essay.pdf](essay/essay.pdf) | The essay: 11 pages, two columns, about 6,000 words, 7 figures, 30 numbered references |
| [essay/sources.pdf](essay/sources.pdf) | An image of every source page the essay cites (64 pages), each labelled with its reference number |
| [computational-analysis.md](computational-analysis.md) | The log of every computational step (A0 to A20): command, inputs, method, result and caveats, plus the full run order and how AI was used |
| [ideas/research-question.pdf](ideas/research-question.pdf) | The one-page research question; [ideas/research-question-sources.pdf](ideas/research-question-sources.pdf) holds the source extracts behind it |
| [analysis/graph/kg.html](analysis/graph/kg.html) | The evidence graph, viewable in a browser (Cytoscape.js): filter by period, valley or source, and click an edge to see its quotation and page |
| [analysis/maps/routes.html](analysis/maps/routes.html) | Interactive map of the herding and trade routes |
| [docs/project.md](docs/project.md) | The course brief |

## Get the code and the source files

The scanned sources (PDFs and zips, about 580 MB) are stored with
**Git LFS**. A plain "Download ZIP" from GitHub gives only small pointer files
in their place, so use git:

```bash
# 1. Install Git LFS once.
#    Ubuntu/Debian: sudo apt install git-lfs    macOS: brew install git-lfs
#    Windows: included with Git for Windows
git lfs install

# 2. Clone the project branch. This downloads everything, about 700 MB.
git clone --branch "vishak's-attempts" https://github.com/gamemaker1/history.git
cd history

# 3. Check that the sources are real files, not pointers (each should be MBs, not ~130 bytes).
ls -lh sources/
#    If they are tiny, fetch them:
git lfs pull
```

To get **only the sources**, skip the other large files and fetch just that folder:

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone --branch "vishak's-attempts" https://github.com/gamemaker1/history.git
cd history
git lfs pull --include="sources/*"
```

What you get in `sources/`:

| File | Contents |
| --- | --- |
| `1961 Village surveys + census reports-...zip` | 25 village survey monographs (24 from the hills, one from Ambala) and 9 other 1961 reports, including Newell's study of the Gaddis |
| `Punjab 1881, Denzil Ibbetson-...zip` | The 1881 Punjab census report, in 6 parts |
| `Census of India 1931, Vol 17 Punjab, Part I Report.pdf` and `Part II Tables.pdf` | The 1931 Punjab census |
| `2015.6965x...Glossary-...Vol1/2/3.pdf` | Rose's *Glossary of the Tribes and Castes*, 3 volumes |
| `index.md` | A description of every source, with online copies |

Unzip the two archives with any unzip tool, or run
`.venv/bin/python scripts/unpack_sources.py` (see setup below), which also
checks them. If the Git LFS download fails (GitHub limits LFS bandwidth),
every source has an online copy listed in [sources/index.md](sources/index.md)
(Internet Archive and the Census of India catalogue).

The searchable text of every source is in `text/`, in plain git, so most of
the analysis can be re-run without the PDFs. The PDFs are needed only to
render page images.

## Repository layout

```
README.md                    this file
computational-analysis.md    log of every computational step (A0-A20) and the run order
requirements.txt             Python packages
.env.example                 template for the API key (copy to .env; only for the language-model steps)
docs/                        the course brief (project.docx, project.md)
ideas/                       research question, its source extracts, and the two idea papers it grew from
sources/                     the scanned sources (Git LFS) and index.md describing them
text/                        OCR text of every source, one form feed per PDF page
                             (1961_layout/ is the same 1961 text in page layout, kept for tables)
scripts/                     every process run on the sources, one Python script each
data/                        curated inputs: claims, entities, livestock tables read from page
                             images, fees, altitudes, households, places, AI check verdicts
analysis/                    generated outputs: graph (graph/), calendar, map, ownership, flows,
                             fees, geography, text reuse, keyword rates, the essay's evidence (essay/)
essay/                       essay.tex and essay.pdf, sources.pdf, and the generated reference files
```

Everything in `analysis/` and the PDFs in `essay/` can be regenerated from
`data/` and `text/` with the scripts.

## Set up and reproduce

Python 3.12, installed with [uv](https://docs.astral.sh/uv/). The interpreter goes inside the
project (`.python/`, not committed), so the scripts can also run inside Claude Code's command sandbox.

```bash
UV_PYTHON_INSTALL_DIR=$PWD/.python uv python install 3.12
UV_PYTHON_INSTALL_DIR=$PWD/.python uv venv .venv --python 3.12 --python-preference only-managed
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python scripts/unpack_sources.py        # unzip and check the sources into cache/
```

(With plain `python -m venv .venv` and `pip install -r requirements.txt` it works too.)

The full run order, 23 steps, is at the top of
[computational-analysis.md](computational-analysis.md). Three useful commands:

```bash
python3 scripts/pageref.py find "grazing rights belonged to the rajah"   # which PDF page a quotation is on
.venv/bin/python scripts/render_page.py Brahmaur 54                       # render a source page to cache/pages/
.venv/bin/python scripts/query_graph.py                                   # rebuild the queries; regression checks must PASS
```

To rebuild the essay and its sources file:

```bash
python3 scripts/essay_references.py               # numbered references, in order of first citation
python3 scripts/check_essay.py                    # every quotation must be found on its cited page
cd essay && pdflatex essay.tex && pdflatex essay.tex && pdflatex essay.tex && cd ..
.venv/bin/python scripts/build_sources_pdf.py     # essay/sources.pdf
```

The language-model steps (`extract_claims.py`, `resolve_entities.py`,
`check_claims.py`) need an OpenAI key in `.env` (copy `.env.example`). Their
responses are cached in `cache/`, which is not committed, and their outputs
are committed in `data/`, so nothing else needs the key.

## How AI was used

- **OpenAI `gpt-6-luna`** proposed the claims from 510 selected pages,
  resolved names to entities, and checked every claim against its page
  (USD 1.16 in all).
- **Anthropic's Claude** wrote the scripts, read the livestock tables and
  Newell's fee table from page images, and drafted the essay with the group.

Nothing an AI produced enters the graph unless its quotation is found on the
cited page, and every quotation in the essay is checked against its page by a
script. Figures read from page images are marked as such and await the
group's check (`checked_by` in `data/flocks.csv` and `data/fee_flocks.csv`).
A 50-claim sample for measuring the AI checker against human judgement is in
`analysis/claim_check_sample.csv`. The details are in the "Use of AI in this
project" section of [computational-analysis.md](computational-analysis.md).
