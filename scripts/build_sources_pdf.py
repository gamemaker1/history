#!/usr/bin/env python3
"""Build essay/sources.pdf: an image of every source page the essay cites.

Reads essay/essay.tex, collects every \\src{source}{page} and
\\srcimg{source}{page} (page lists and ranges are expanded), notes the
sections of the essay that cite each page and the quotations taken from it,
and renders each cited page from the original PDF. The output has:

  - a title page explaining what the file is;
  - an index: every cited page, with its source, file and the essay sections
    that cite it;
  - one page per cited source page: a header (number, full title of the
    source, PDF file, PDF page, the sections citing it, the quotations taken
    from it) above the image of the page.

Pages are PDF page numbers, as in the essay. Needs pymupdf and the unpacked
PDFs (scripts/unpack_sources.py).

Usage (from the project folder):
  .venv/bin/python scripts/build_sources_pdf.py
  .venv/bin/python scripts/build_sources_pdf.py --dpi 130
"""

import argparse
import re
from collections import OrderedDict

import pymupdf

from check_essay import CITE, QUOTE, pages_of, plain
import csv

from corpus import ANALYSIS, ROOT, pdf_path, source_text

ESSAY = ROOT / "essay" / "essay.tex"
OUT = ROOT / "essay" / "sources.pdf"
A4 = pymupdf.paper_rect("a4")
MARGIN = 36
MAROON = (0x7A / 255, 0x1F / 255, 0x2B / 255)  # the essay's heading colour
GREY = (0.42, 0.42, 0.42)

VILLAGE_DISTRICT = {
    "Basal": "Solon tahsil, Mahasu District", "Batal": "Arki tahsil, Mahasu District",
    "Brahmaur": "Chamba District", "Bir": "Mandi District", "Chaunri": "Kasumpti tahsil, Mahasu District",
    "Chauntra": "Jogindar Nagar tahsil, Mandi District", "Chaupal": "Mahasu District",
    "Chergaon": "Rohru tahsil, Mahasu District", "Chitrari": "Chamba District", "Devi-Kothi": "Chamba District",
    "Kanum": "Kinnaur District", "Kot": "Sarkaghat tahsil, Mandi District", "Kothi": "Kinnaur District",
    "Kupha": "Pangi, Chamba District (Kupha, Parmas, Thamoh and Malet)", "Maingal": "Chamba District",
    "Moginand": "Sirmur District", "Nachar": "Kinnaur District", "Nalag": "Mandi District",
    "Pangna": "Karsog tahsil, Mandi District", "Rajana": "Rainka tahsil, Sirmur District",
    "Shakrori": "Seoni sub-tahsil, Mahasu District", "Shathla": "Kumarsain sub-tahsil, Mahasu District",
}
TITLES = {
    "1881": "Denzil Ibbetson, Report on the Census of the Panjab, 1881, Results (Calcutta, 1883)",
    "Rose": "H. A. Rose, A Glossary of the Tribes and Castes of the Punjab and North-West Frontier Province, vol. 2 (Lahore, 1911)",
    "Rose Vol1": "H. A. Rose, A Glossary of the Tribes and Castes of the Punjab and North-West Frontier Province, vol. 1 (Lahore, 1919)",
    "Rose Vol3": "H. A. Rose, A Glossary of the Tribes and Castes of the Punjab and North-West Frontier Province, vol. 3 (Lahore, 1914)",
    "1931": "Khan Ahmad Hasan Khan, Census of India 1931, Vol. XVII: Punjab, Part I, Report (Lahore, 1933)",
    "Newell": "W. H. Newell, 'The Gaddi and Affiliated Castes of the Western Himalayas', in Census of India 1961, "
              "Report on Scheduled Castes and Scheduled Tribes of Himachal Pradesh",
    "Weaving": "Census of India 1961, Himachal Pradesh, Craft Survey: Weaving",
    "Mahasu": "Census of India 1961, Himachal Pradesh, District Census Handbook: Mahasu",
    "Simla": "Census of India 1961, Punjab, District Census Handbook: Simla",
    "Tandi": "Census of India 1961, Vol. XIII (Punjab), Part VI, Village Survey Monograph: Tandi (Lahaul and Spiti District)",
    "Kalath": "Census of India 1961, Vol. XIII (Punjab), Part VI, Village Survey Monograph: Kalath (Simla District)",
}


def title_of(source):
    if source in TITLES:
        return TITLES[source]
    if source in VILLAGE_DISTRICT:
        return (f"Census of India 1961, Vol. XX (Himachal Pradesh), Part VI, Village Survey Monograph: "
                f"{source} ({VILLAGE_DISTRICT[source]})")
    return source


def citations():
    """OrderedDict (source, page) -> {"sections": [...], "quotes": [...], "image": bool}, in order of first citation."""
    tex = ESSAY.read_text(encoding="utf-8")
    tex = tex[tex.index("\\begin{document}"):]
    heads = [(m.start(), m.group(1), m.group(2)) for m in re.finditer(r"\\(section|subsection)\*?\{([^}]*)\}", tex)]
    numbered, sec, sub = {}, 0, 0
    for pos, kind, title in heads:
        starred = tex[pos:pos + 20].startswith(f"\\{kind}*")
        if kind == "section" and not starred:
            sec, sub = sec + 1, 0
            numbered[pos] = f"§{sec} {plain(title)}"
        elif kind == "subsection" and not starred:
            sub += 1
            numbered[pos] = f"§{sec}.{sub} {plain(title)}"
        else:
            numbered[pos] = plain(title)
    found = OrderedDict()
    last = 0
    for m in CITE.finditer(tex):
        kind, source, spec = m.groups()
        where = "abstract or front matter"
        for pos in sorted(numbered):
            if pos < m.start():
                where = numbered[pos]
        if tex.rfind("\\caption{", 0, m.start()) > tex.rfind("}", 0, m.start() - 1) - 400 and "\\caption{" in tex[max(0, m.start() - 600):m.start()]:
            where += " (figure caption)"
        span = tex[last:m.start()]
        cut = max(span.rfind(". "), span.rfind(".\n"))
        span = span if cut < 0 else span[cut + 1:]
        last = m.end()
        quotes = [plain(q) for q in QUOTE.findall(span)]
        for p in pages_of(spec):
            entry = found.setdefault((source, p), {"sections": [], "quotes": [], "image": False, "text": False})
            if where not in entry["sections"]:
                entry["sections"].append(where)
            for q in quotes:
                if q not in entry["quotes"]:
                    entry["quotes"].append(q)
            entry["image"] |= kind == "srcimg"
            entry["text"] |= kind == "src"
    return found


def image_note(info):
    if info["image"] and info["text"]:
        return "partly read from the page image"
    return "read from the page image" if info["image"] else ""


def add_text_page(out, title, lines, size=9):
    page = out.new_page(width=A4.width, height=A4.height)
    y = MARGIN
    page.draw_rect(pymupdf.Rect(0, 0, A4.width, 22), color=MAROON, fill=MAROON)
    page.insert_text((MARGIN, 15), "The Mountain Year and Its Owners  |  sources.pdf", fontsize=8, fontname="helv",
                     color=(1, 1, 1))
    page.insert_text((MARGIN, y + 14), title, fontsize=14, fontname="hebo", color=MAROON)
    y += 34
    for line in lines:
        rect = pymupdf.Rect(MARGIN, y, A4.width - MARGIN, A4.height - MARGIN)
        h = page.insert_textbox(rect, line, fontsize=size, fontname="helv")
        used = (rect.height - h) if h >= 0 else rect.height
        y += used + 2
        if y > A4.height - MARGIN - 20:
            page = out.new_page(width=A4.width, height=A4.height)
            y = MARGIN
    return page


def reference_numbers():
    """Source name -> its number in the essay's reference list (scripts/essay_references.py)."""
    path = ANALYSIS / "essay" / "reference_numbers.csv"
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return {r["source"]: r["number"] for r in csv.DictReader(f) if r["source"]}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dpi", type=int, default=120, help="resolution of the page images")
    args = ap.parse_args()
    cites = citations()
    refs = reference_numbers()
    out = pymupdf.open()

    add_text_page(out, "Sources cited in 'The Mountain Year and Its Owners'", [
        "This file reproduces every page of a primary source that the essay cites, in the order in which the "
        "essay first cites it. A citation such as [5, p. 55] in the essay is reference [5] of its numbered "
        "reference list, PDF page 55; this file has that page under the header 'Reference [5], PDF page 55'. "
        "Each page carries a header with the reference number, the full title of the "
        "source, the PDF file it comes from, the PDF page number (the page counter of a PDF viewer, as used in "
        "the essay's citations), the sections of the essay that cite it, and any words the essay quotes from it.",
        "",
        "Pages marked 'read from the page image' are cited for figures (tables, or text the OCR garbles) that "
        "were read from the image rather than from the OCR text; every other quotation in the essay was checked "
        "automatically against the OCR text of its page (scripts/check_essay.py, analysis/essay/citation_check.csv).",
        "",
        "Built by scripts/build_sources_pdf.py from essay/essay.tex. The 1961 volumes and the 1881 Results are "
        "inside the zip files in sources/; the 1931 Report and Rose's Glossary are PDFs in sources/.",
        "",
        f"{len(cites)} pages from {len({s for s, _ in cites})} sources.",
    ], size=10)

    index = []
    for i, ((source, page), info) in enumerate(cites.items(), 1):
        mark = f" [{image_note(info)}]" if image_note(info) else ""
        ref = f"[{refs[source]}] " if source in refs else ""
        index.append(f"{i:3d}.  {ref}{source}, PDF p. {page}{mark}  -  cited in: {'; '.join(info['sections'])}")
    add_text_page(out, "Index of cited pages", index, size=8)

    for i, ((source, page), info) in enumerate(cites.items(), 1):
        pdf = pdf_path(source_text(source))
        with pymupdf.open(pdf) as doc:
            pix = doc[page - 1].get_pixmap(dpi=args.dpi)
            img = pix.tobytes("jpeg", jpg_quality=80)
        p = out.new_page(width=A4.width, height=A4.height)
        ref = f"Reference [{refs[source]}]" if source in refs else source
        header = [f"{ref}, PDF page {page}   -   {title_of(source)}   (page {i} of {len(cites)})",
                  f"File: {pdf.name}   |   PDF page {page}" + (f"   |   {image_note(info)}" if image_note(info) else ""),
                  f"Cited in: {'; '.join(info['sections'])}"]
        if info["quotes"]:
            q = "; ".join(f'"{x[:140]}{"..." if len(x) > 140 else ""}"' for x in info["quotes"][:3])
            header.append(f"Quoted: {q}")
        p.draw_rect(pymupdf.Rect(0, 0, A4.width, 6), color=MAROON, fill=MAROON)
        left = p.insert_textbox(pymupdf.Rect(MARGIN, MARGIN - 18, A4.width - MARGIN, MARGIN + 16), header[0],
                                fontsize=8.5, fontname="hebo", color=MAROON)
        if left < 0:
            raise SystemExit(f"header too long for {source} p. {page}")
        rect = pymupdf.Rect(MARGIN, MARGIN + 16, A4.width - MARGIN, MARGIN + 92)
        p.insert_textbox(rect, "\n".join(header[1:]), fontsize=7.5, fontname="helv", color=GREY)
        p.draw_line((MARGIN, MARGIN + 94), (A4.width - MARGIN, MARGIN + 94), color=MAROON, width=0.8)
        box = pymupdf.Rect(MARGIN, MARGIN + 100, A4.width - MARGIN, A4.height - MARGIN)
        p.insert_image(box, stream=img, keep_proportion=True)

    out.save(OUT, garbage=4, deflate=True)
    print(f"{len(cites)} cited pages from {len({s for s, _ in cites})} sources written to "
          f"{OUT.relative_to(ROOT)} ({OUT.stat().st_size / 1e6:.1f} MB, {out.page_count} pages)")


if __name__ == "__main__":
    main()
