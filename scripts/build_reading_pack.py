#!/usr/bin/env python3
"""Build essay/reading_pack.pdf, which holds the source pages for each section of the essay outline.

Reads data/reading_pack.csv, which has one row per page with the essay
section, the research-question item, the source, the PDF page and what to read
the page for. Each page is copied unchanged from the original PDF, and the
pages are grouped by section in the order of the outline
(essay/seasonal-herding.typ).

The file opens with a plain text page that describes the file and lists each
item the research question promises, with the sections and the number of
pages for each item. Each section opens with a plain text page that lists its
pages and what to read them for. Under each page whose figures were read from
the page image (data/flocks.csv, data/fee_flocks.csv), that list also holds the
figures, so that a reader can check them against the scan.

A page used by two sections is copied into both. Pages are PDF page numbers.
Needs pymupdf and the unpacked PDFs (scripts/unpack_sources.py).

Usage (from the project folder):
  .venv/bin/python scripts/build_reading_pack.py
"""

import csv
from collections import OrderedDict

import pymupdf

from build_sources_pdf import title_of
from corpus import DATA, ROOT, TEXT, pdf_path, source_text

PACK = DATA / "reading_pack.csv"
OUT = ROOT / "essay" / "reading_pack.pdf"
ATLAS = TEXT / "1961" / "1961 Punjab Census Atlas.txt"
A4 = pymupdf.paper_rect("a4")
MARGIN = 56

RQ_ITEMS = OrderedDict([
    ("question", "The research question and its two framing quotations"),
    ("A1 longue duree", "Annales, longue duree: relief, climate, rivers, forests and pasture"),
    ("A2 map routes", "Annales: map the routes, passes and pastures, using the 1961 Punjab Census Atlas"),
    ("A3 events", "Annales: the time of events (1948 merger, end of the Tibet trade)"),
    ("B1 compare sources", "Bloch 1: the herding cycle in 1881, Rose (1911) and 1961"),
    ("B2 Brahmaur and Bir", "Bloch 2: high villages with large flocks against low villages that buy animals"),
    ("B3 Brahmaur and Devi-Kothi", "Bloch 3: herding families against settled farmers with hired graziers"),
    ("B4 Ravi and Sutlej", "Bloch 4: the raja's grazing rights and Kangra against commons and the Tibet trade"),
    ("C1 owners", "Marx: who owned the flocks (livestock tables by caste)"),
    ("C2 labour", "Marx: who did the herding"),
    ("C3 debt", "Marx: debt by caste and household, and interest"),
    ("D1 dual landholding", "Dialectic, conjuncture 1: Gaddi land in British Kangra and Chamba, 1881"),
    ("D2 raja and auction", "Dialectic, conjuncture 2: the raja's grazing rights and fee auction, to 1950"),
    ("D3 forest permits", "Dialectic, conjuncture 3: Forest Department permits, and the raja's fees against the Department's fees"),
    ("D4 roads", "Dialectic, conjuncture 4: road and building work, to 1961"),
])


def pdf_of(source):
    return pdf_path(ATLAS) if source == "Atlas" else pdf_path(source_text(source))


def full_title(source):
    if source == "Atlas":
        return "Census of India 1961, Vol. XIII, Part IX: Punjab Census Atlas"
    return title_of(source)


def image_figures():
    """(source, page) -> lines of figures read from the page image."""
    figs = {}
    with open(DATA / "flocks.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            line = (f"{r['group']}: households {r['households_in_group'] or '-'}, sheep {r['sheep'] or '-'}, "
                    f"goats {r['goats'] or '-'}, households owning sheep or goats {r['hh_owning_flock'] or '-'}, "
                    f"sheep and goats {r['sheep_and_goats'] or '-'}" + (f" ({r['note']})" if r["note"] else ""))
            figs.setdefault((r["village"], int(r["pdf_page"])), []).append(line)
    with open(DATA / "fee_flocks.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            line = f"{r['year']}: sheep {r['sheep']}, goats {r['goats']}" + (f" ({r['remark']})" if r["remark"] else "")
            figs.setdefault((r["source"], int(r["pdf_page"])), []).append(line)
    return figs


def text_pages(out, heading, paragraphs):
    """Add plain pages with a heading and paragraphs. A (text, indent) tuple is an indented paragraph."""
    page = out.new_page(width=A4.width, height=A4.height)
    page.insert_text((MARGIN, MARGIN + 6), heading, fontsize=14, fontname="tibo")
    y = MARGIN + 26
    for para in paragraphs:
        text, indent, size = (para, 0, 10.5) if isinstance(para, str) else (para[0], para[1], 9.5)
        rect = pymupdf.Rect(MARGIN + indent, y, A4.width - MARGIN, A4.height - MARGIN)
        left = page.insert_textbox(rect, text, fontsize=size, fontname="tiro")
        if left < 0:
            page = out.new_page(width=A4.width, height=A4.height)
            y = MARGIN
            rect = pymupdf.Rect(MARGIN + indent, y, A4.width - MARGIN, A4.height - MARGIN)
            left = page.insert_textbox(rect, text, fontsize=size, fontname="tiro")
        y += rect.height - left + (2 if indent else 6)


def main():
    with open(PACK, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    sections = OrderedDict()
    for r in rows:
        sections.setdefault(r["section"], []).append(r)
    figs = image_figures()
    out = pymupdf.open()

    intro = [
        "This file holds the source pages for each section of the essay outline in essay/seasonal-herding.typ, in "
        "the order of the outline. Each section starts with a page that lists its source pages and what to read "
        "each one for. The source pages follow, copied unchanged from the original PDFs. Page numbers are PDF "
        "page numbers, which are the page counter of a PDF viewer.",
        "Some tables have scrambled OCR text, and Claude read their figures from the page image into "
        "data/flocks.csv and data/fee_flocks.csv. No person has checked these figures yet, and the checked_by "
        "column is empty in every row. Each section page lists the figures under the page they come from. A "
        "reader who confirms a row against the scan enters their name in its checked_by column.",
        f"The file holds {len(rows)} pages in {len(sections)} sections, from "
        f"{len({r['source'] for r in rows})} sources. It is built by scripts/build_reading_pack.py from "
        "data/reading_pack.csv.",
        "Each line below names an item that the research question promises, with the sections and the number "
        "of pages for that item.",
    ]
    for key, text in RQ_ITEMS.items():
        hit = [r for r in rows if r["rq_item"] == key]
        secs = sorted({r["section"].split()[0] for r in hit}, key=lambda s: [int(x) for x in s.split(".")])
        intro.append((f"{text}. Section {', '.join(secs) or 'NONE'}, {len(hit)} pages.", 14))
    text_pages(out, "Reading Pack for the Essay Outline", intro)

    for name, items in sections.items():
        lines = []
        for r in items:
            key = (r["source"], int(r["pdf_page"]))
            lines.append(f"{r['source']}, PDF p. {r['pdf_page']}. {r['read_for']}")
            lines.append((full_title(r["source"]), 14))
            if key in figs:
                lines.append(("Figures read from the page image, to be checked against the scan", 14))
                lines += [(x, 28) for x in figs[key]]
        text_pages(out, f"Section {name}", lines)
        for r in items:
            with pymupdf.open(pdf_of(r["source"])) as doc:
                n = int(r["pdf_page"]) - 1
                out.insert_pdf(doc, from_page=n, to_page=n)

    out.save(OUT, garbage=4, deflate=True)
    print(f"{len(rows)} pages in {len(sections)} sections written to {OUT.relative_to(ROOT)} "
          f"({OUT.stat().st_size / 1e6:.1f} MB, {out.page_count} pages)")


if __name__ == "__main__":
    main()
