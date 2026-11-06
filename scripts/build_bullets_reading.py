#!/usr/bin/env python3
"""Build essay/bullets/reading-first.pdf, the pages to read before writing the essay from the bullets.

Reads essay/bullets/report-bullets.tex and collects every citation of a PDF
page in a \\cit{...}, with the section and the text of each bullet that cites
it and the \\enquote{...} quotations that precede the citation. Citations of
appendix tables and project analyses are skipped.

The output holds the course readings first, in the order of
COURSE_ORDER, and then the primary-source pages, grouped by the bullet section
that first cites them. Each page is copied from the original PDF and widened
by a margin column on the right. The column lists every bullet that cites the
page, with its section. Each quotation is located on the page by a fuzzy
match of its words and highlighted, and the highlight carries the bullet text
as a pop-up note. Pages with no text layer are read with tesseract first. A
quotation that cannot be located is marked as such in the margin column.

A front matter, typeset from essay/bullets/reading-first.typ, gives the
reading order and the contents. It reads the contents from
essay/bullets/reading-first.json, which this script writes.

Usage (from the project folder):
  .venv/bin/python scripts/build_bullets_reading.py
"""

import json
import re
import subprocess
from collections import OrderedDict
from difflib import SequenceMatcher
from pathlib import Path

import pymupdf

from build_sources_pdf import title_of
from corpus import PDF_CACHE, ROOT, pdf_path, source_text

BULLETS = ROOT / "essay" / "bullets" / "report-bullets.tex"
OUT = ROOT / "essay" / "bullets" / "reading-first.pdf"
FRONT = ROOT / "essay" / "bullets" / "reading-first.typ"
CONTENTS = ROOT / "essay" / "bullets" / "reading-first.json"
SLIDES = ROOT.parent / "slides"
FONTS = Path("/usr/share/fonts/urw-fonts")

# Each course reading has a citation prefix, a PDF, a full title, and what the bullets take from it.
COURSE = OrderedDict([
    ("Braudel", (next((SLIDES / "quiz2").glob("*Braudel*")),
                 "Fernand Braudel, \"History and the Social Sciences: The Longue Durée\", trans. Immanuel Wallerstein, "
                 "Review (Fernand Braudel Center) 32, no. 2 (2009)",
                 "The three levels of historical time, the series that measure a conjuncture, and the claim that the "
                 "levels run together. The essay is ordered by these levels.")),
    ("Bloch", (next(SLIDES.glob("Marc Bloch*")),
               "Marc Bloch, The Historian's Craft, trans. Peter Putnam (New York: Vintage, 1953), chapter III",
               "Criticism of witnesses, copying between sources, and comparison. These pages justify the "
               "text-reuse check and the comparison of the Ravi and the Sutlej.")),
    ("Alam", (SLIDES / "Lectures 8 9 10 - Marxist History, Intro2Hist M2026.pdf",
              "Aniket Alam, \"Marxist History\", Lectures 8 to 10, Introduction to History, IIIT Hyderabad",
              "The material basis, the relations of production and the dialectical contradiction, as the course "
              "defines them.")),
    ("Marx, \\enquote{The British", (SLIDES / "The British Rule in India by Karl Marx.pdf",
                                  "Karl Marx, \"The British Rule in India\", New-York Daily Tribune, 25 June 1853",
                                  "The village community and the state's claim on the product.")),
    ("Marx, \\enquote{The Future", (SLIDES / "The Future Results of British Rule in India by Karl Marx.pdf",
                            "Karl Marx, \"The Future Results of British Rule in India\", New-York Daily Tribune, "
                            "8 August 1853",
                            "Roads and railways as the end of village isolation.")),
    ("Marx and Engels", (SLIDES / "Manifesto-14-21.pdf",
                         "Karl Marx and Friedrich Engels, Manifesto of the Communist Party, excerpt, pp. 14 to 21",
                         "Class relations and the market.")),
    ("Habib", (SLIDES / "Habib-PotentialitiesCapitalisticDevelopment-1969.pdf",
               "Irfan Habib, \"Potentialities of Capitalistic Development in the Economy of Mughal India\", "
               "Journal of Economic History 29, no. 1 (1969)",
               "Revenue, merchants and credit in an agrarian state, as a model for the raja's fee and the "
               "moneylender.")),
    ("Kosambi", (SLIDES / "Kosambi-SocialEconomicAspects-1961.pdf",
                 "D. D. Kosambi, \"Social and Economic Aspects of the Bhagavad Gita\", Journal of the Economic and "
                 "Social History of the Orient 4, no. 2 (1961)",
                 "Fusion and tolerance between social groups.")),
    ("Le Roy Ladurie", (next((SLIDES / "quiz2").glob("french-studies*")),
                        "Emmanuel Le Roy Ladurie, \"The History of Rain and Fine Weather\", in French Studies in "
                        "History, vol. 1, The Inheritance",
                        "The limit of climatic explanation.")),
    ("Aymard", (next((SLIDES / "quiz2").glob("vdoc*")),
                "Maurice Aymard, \"The Cost of War\", in French Studies in History, vol. 2, Departures",
                "A conjuncture read from a fiscal series.")),
])

SHORT = {"Braudel": "Braudel, Longue Durée", "Bloch": "Bloch, Historian's Craft", "Alam": "Alam, Marxist History slides",
         "Marx, \\enquote{The British": "Marx, British Rule in India",
         "Marx, \\enquote{The Future": "Marx, Future Results of British Rule",
         "Marx and Engels": "Marx and Engels, Manifesto", "Habib": "Habib, Capitalistic Development",
         "Kosambi": "Kosambi, Bhagavad Gita", "Le Roy Ladurie": "Le Roy Ladurie, Rain and Fine Weather",
         "Aymard": "Aymard, Cost of War", "1881": "1881 census", "1931": "1931 census", "Rose": "Rose, vol. 2",
         "Rose Vol1": "Rose, vol. 1", "Newell": "Newell", "Mahasu": "Mahasu handbook", "Weaving": "Weaving survey",
         "Atlas": "Punjab Census Atlas"}


def short_of(key):
    return SHORT.get(key, f"{key} survey")


# Each primary source has a citation prefix and the corpus name used by source_text.
PRIMARY = OrderedDict([
    ("1881 census", "1881"), ("1931 census", "1931"),
    ("Rose, vol.~1", "Rose Vol1"), ("Rose, vol.~2", "Rose"), ("Rose", "Rose"),
    ("Newell", "Newell"), ("Mahasu handbook", "Mahasu"), ("Weaving survey", "Weaving"),
    ("Punjab Census Atlas", "Atlas"),
])
SURVEY = re.compile(r"^([A-Z][A-Za-z-]+) survey")


def pdf_of(name):
    if name == "Atlas":
        return PDF_CACHE / "1961" / "1961 Punjab Census Atlas.pdf"
    return pdf_path(source_text(name))


def source_of(part):
    """(kind, key) for one citation part, or None if it names no known source."""
    for prefix in COURSE:
        if part.startswith(prefix):
            return ("course", prefix)
    for prefix, name in PRIMARY.items():
        if part.startswith(prefix):
            return ("primary", name)
    m = SURVEY.match(part)
    if m:
        return ("primary", m.group(1))
    return None


def pages_of(part):
    """PDF page numbers named in one citation part, ranges expanded."""
    m = re.search(r"PDF pp?\.~?([0-9 ,\-]+)", part)
    if not m:
        return []
    out = []
    for piece in m.group(1).split(","):
        piece = piece.strip()
        if "--" in piece:
            a, b = piece.split("--")
            out += list(range(int(a), int(b) + 1))
        elif piece.isdigit():
            out.append(int(piece))
    return out


def braces(text, start):
    """Index just after the brace group that opens at text[start]."""
    depth = 0
    for i in range(start, len(text)):
        depth += {"{": 1, "}": -1}.get(text[i], 0)
        if depth == 0:
            return i + 1
    raise ValueError("unbalanced braces")


def plain(tex):
    """Readable text from a bullet's LaTeX."""
    tex = tex.replace("\\Braudel", "Braudel, \\enquote{History and the Social Sciences}")
    tex = tex.replace("\\Habib", "Habib, \\enquote{Potentialities of Capitalistic Development}")
    tex = re.sub(r"\\(?:sec)?ref\{[^}]*\}", "", tex)
    while "\\enquote{" in tex:
        i = tex.index("\\enquote{")
        j = braces(tex, i + 8)
        tex = tex[:i] + "\u201c" + tex[i + 9:j - 1] + "\u201d" + tex[j:]
    tex = tex.replace("\\dots{}", "\u2026").replace("\\dots", "\u2026")
    tex = re.sub(r"\\(?:emph|textit|path|texttt)\{", "", tex)
    tex = tex.replace("~", " ").replace("\\,", " ").replace("\\@", "").replace("\\%", "%")
    tex = tex.replace("``", "\u201c").replace("''", "\u201d").replace("`", "\u2018").replace("'", "\u2019")
    tex = re.sub(r"(\d)--(\d)", r"\1 to \2", tex)
    tex = tex.replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", tex).strip()


def parse():
    """OrderedDict (kind, key, page) -> list of {section, bullet, quotes, image}."""
    tex = BULLETS.read_text(encoding="utf-8")
    tex = tex[tex.index("\\section{Introduction}"):tex.index("\\section{Data Tables}")]
    tex = re.sub(r"(?m)(?<!\\)%.*$", "", tex)
    heads = []
    sec = sub = 0
    for m in re.finditer(r"\\(section|subsection)\{([^}]*)\}", tex):
        if m.group(1) == "section":
            sec, sub = sec + 1, 0
            heads.append((m.start(), f"{sec}", plain(m.group(2))))
        else:
            sub += 1
            heads.append((m.start(), f"{sec}.{sub}", plain(m.group(2))))
    found = OrderedDict()
    items = [m.start() for m in re.finditer(r"\\item\b", tex)]
    ends = items[1:] + [len(tex)]
    for start, end in zip(items, ends):
        body = tex[start + 5:end]
        body = re.split(r"\\end\{itemize\}", body)[0]
        num, title = next((n, t) for p, n, t in reversed(heads) if p < start)
        section = f"{num} {title}"
        # Quotations in a bullet are attached to the next citation after them.
        pending, i = [], 0
        cites = []
        while i < len(body):
            if body.startswith("\\enquote{", i):
                j = braces(body, i + 8)
                pending.append(plain(body[i + 9:j - 1]))
                i = j
            elif body.startswith("\\cit{", i):
                j = braces(body, i + 4)
                cites.append((body[i + 5:j - 1], pending))
                pending = []
                i = j
            else:
                i += 1
        bullet = plain(cut_cits(body))
        for cite, quotes in cites:
            image = "image-read" in cite
            last = None
            for part in cite.replace("\\Braudel", "Braudel").replace("\\Habib", "Habib").split(";"):
                part = re.sub(r"\s+", " ", part.strip())
                src = source_of(part) or last
                last = src
                if src is None:
                    continue
                for page in pages_of(part):
                    found.setdefault((*src, page), []).append(
                        {"section": section, "bullet": bullet, "quotes": quotes, "image": image})
    return found


def cut_cits(body):
    out, i = [], 0
    while i < len(body):
        if body.startswith("\\cit{", i):
            i = braces(body, i + 4)
        else:
            out.append(body[i])
            i += 1
    return re.sub(r"\s+([.,;])", r"\1", "".join(out))


def norm(word):
    return re.sub(r"[^a-z0-9]", "", word.lower())


def tokens_of(words):
    """Page words as (key, boxes), with a word hyphenated across a line break joined into one key."""
    out = []
    for w in words:
        key = norm(w[4])
        if not key:
            continue
        if out and out[-1][2]:
            prev = out.pop()
            out.append((prev[0] + key, prev[1] + [w], w[4].endswith("-")))
        else:
            out.append((key, [w], w[4].endswith("-")))
    return [(k, b) for k, b, _ in out]


def locate(words, quote):
    """Word boxes on the page for each part of the quotation between ellipses, or [] if any part is not found."""
    boxes = []
    for part in quote.split("\u2026"):
        if len(part.split()) < 2 and "\u2026" in quote:
            continue
        found = locate_part(words, part)
        if not found:
            return []
        boxes += found
    return boxes


def locate_part(words, quote):
    """Word boxes on the page that best match the words of the quotation, or [] if the best match is weak."""
    target = [norm(w) for w in quote.split() if norm(w)]
    toks = tokens_of(words)
    keys = [k for k, _ in toks]
    if len(target) == 1:
        return [w for k, b in toks if k == target[0] for w in b]
    n = len(target)
    joined = " ".join(target)
    best, best_at = 0.0, None
    for i in range(0, max(1, len(keys) - n + 1)):
        r = SequenceMatcher(None, " ".join(keys[i:i + n]), joined, autojunk=False).ratio()
        if r > best:
            best, best_at = r, i
    if best < 0.72 or best_at is None:
        return []
    return [w for _, b in toks[best_at:best_at + n] for w in b]


def line_rects(boxes):
    """Merge word boxes into one rectangle per text line."""
    lines = OrderedDict()
    for w in boxes:
        lines.setdefault((w[5], w[6]), []).append(pymupdf.Rect(w[:4]))
    out = []
    for rects in lines.values():
        r = rects[0]
        for x in rects[1:]:
            r |= x
        out.append(r)
    return out


def page_words(doc, index):
    page = doc[index]
    words = page.get_text("words")
    if len(words) > 20:
        return words, False
    tp = page.get_textpage_ocr(dpi=300, full=True, language="eng")
    return page.get_text("words", textpage=tp), True


CSS = """
@font-face {font-family: C059; src: url(C059-Roman.otf);}
@font-face {font-family: C059; src: url(C059-Bold.otf); font-weight: bold;}
@font-face {font-family: C059; src: url(C059-Italic.otf); font-style: italic;}
* {font-family: C059; color: #222;}
h1 {font-size: 1.15em; margin: 0 0 0.3em 0;}
p {margin: 0 0 0.45em 0; text-align: left;}
.meta {color: #555; font-size: 0.9em;}
.sec {font-weight: bold; color: #0050b0;}
.q {font-style: italic;}
.miss {color: #a03000;}
.img {color: #a03000; font-weight: bold;}
"""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def add_page(out, src_doc, kind, key, page, uses, number, hits, anywhere):
    """Copy one page with a margin column and highlights. Returns located and missed quotation counts."""
    sp = src_doc[page - 1]
    w, h = sp.rect.width, sp.rect.height
    side = max(0.55 * w, 0.42 * h)
    newp = out.new_page(width=w + side, height=h)
    newp.show_pdf_page(pymupdf.Rect(0, 0, w, h), src_doc, page - 1)
    ocr = hits["ocr"]
    # show_pdf_page keeps the page's coordinates when the target rectangle equals its size.
    seen, located, missed = set(), [], []
    for use in uses:
        for q in use["quotes"]:
            if q in seen:
                continue
            seen.add(q)
            boxes = hits["quotes"][q]
            if boxes:
                rects = line_rects(boxes)
                annot = newp.add_highlight_annot(rects)
                annot.set_colors(stroke=(1.0, 0.86, 0.35))
                annot.set_info(title=use["section"], content=use["bullet"])
                annot.update()
                located.append(q)
            elif q not in anywhere:
                missed.append(q)
    title = COURSE[key][1] if kind == "course" else title_of(key)
    title = re.sub(r'"([^"]*)"', "\u201c\\1\u201d", title).replace("'", "\u2019")
    html = [f"<h1>{number}. {esc(title)}</h1>",
            f"<p class='meta'>PDF page {page}{' (text read by OCR for the highlights)' if ocr else ''}</p>"]
    if any(u["image"] for u in uses):
        html.append("<p class='img'>Figures on this page were read from the page image and no person has "
                    "checked them. Check them against this scan.</p>")
    done = set()
    for use in uses:
        k = (use["section"], use["bullet"])
        if k in done:
            continue
        done.add(k)
        html.append(f"<p><span class='sec'>Bullets {esc(use['section'])}.</span> {esc(use['bullet'])}</p>")
    if missed:
        html.append("<p class='miss'>Quotations not located on the page by the search. Find them by eye:</p>")
        html += [f"<p class='q miss'>{esc(q)}</p>" for q in missed]
    box = pymupdf.Rect(w + 0.06 * side, 0.04 * h, w + side - 0.06 * side, h - 0.04 * h)
    newp.draw_rect(pymupdf.Rect(w, 0, w + side, h), color=None, fill=(0.96, 0.96, 0.96))
    newp.draw_line((w, 0), (w, h), color=(0.6, 0.6, 0.6), width=0.8)
    size = h / 62
    spare, scale = newp.insert_htmlbox(box, "".join(html), css=CSS + f"* {{font-size: {size:.1f}px;}}",
                                       archive=pymupdf.Archive(str(FONTS)), scale_low=0)
    return len(located), len(missed)


def main():
    found = parse()
    course = [(k, v) for k, v in found.items() if k[0] == "course"]
    primary = [(k, v) for k, v in found.items() if k[0] == "primary"]
    order = list(COURSE)
    course.sort(key=lambda kv: (order.index(kv[0][1]), kv[0][2]))
    # Primary pages keep the order of their first citation, grouped by its section.
    sec_order = []
    for _, uses in primary:
        if uses[0]["section"] not in sec_order:
            sec_order.append(uses[0]["section"])
    primary.sort(key=lambda kv: sec_order.index(kv[1][0]["section"]))

    docs, hits = {}, {}
    for (kind, key, page), uses in course + primary:
        path = COURSE[key][0] if kind == "course" else pdf_of(key)
        doc = docs.setdefault(path, pymupdf.open(path))
        words, ocr = page_words(doc, page - 1)
        hits[(kind, key, page)] = {"ocr": ocr, "quotes": {
            q: locate(words, q) for u in uses for q in u["quotes"]}}
    # A citation of two or more pages attaches its quotations to each of them.
    anywhere = {q for h in hits.values() for q, boxes in h["quotes"].items() if boxes}
    body = pymupdf.open()
    contents = {"course": [], "primary": [], "pages": 0, "located": 0, "missed": 0, "ocr_sources": []}
    number = 0
    for group, rows in (("course", course), ("primary", primary)):
        for (kind, key, page), uses in rows:
            path = COURSE[key][0] if kind == "course" else pdf_of(key)
            doc = docs[path]
            number += 1
            start = len(body)
            got, miss = add_page(body, doc, kind, key, page, uses, number,
                                 hits[(kind, key, page)], anywhere)
            contents["located"] += got
            contents["missed"] += miss
            sections = list(OrderedDict.fromkeys(u["section"].split(" ")[0] for u in uses))
            contents[group].append({
                "n": number, "key": key, "short": short_of(key), "source": COURSE[key][1] if kind == "course" else title_of(key),
                "role": COURSE[key][2] if kind == "course" else "",
                "page": page, "first": uses[0]["section"], "sections": sections,
                "image": any(u["image"] for u in uses), "at": start,
                "uses": len({u["bullet"] for u in uses})})
    contents["pages"] = len(body)
    CONTENTS.write_text(json.dumps(contents, indent=1, ensure_ascii=False), encoding="utf-8")

    front_pdf = FRONT.with_suffix(".front.pdf")
    subprocess.run(["typst", "compile", "--root", str(ROOT), str(FRONT), str(front_pdf)], check=True)
    front = pymupdf.open(front_pdf)
    offset = len(front)
    out = pymupdf.open()
    out.insert_pdf(front)
    out.insert_pdf(body)
    toc = [[1, "Reading order and contents", 1], [1, "Course readings", offset + 1]]
    last = None
    for row in contents["course"]:
        if row["key"] != last:
            toc.append([2, row["short"], offset + row["at"] + 1])
            last = row["key"]
    toc.append([1, "Primary sources", offset + contents["primary"][0]["at"] + 1])
    last = None
    for row in contents["primary"]:
        if row["first"] != last:
            toc.append([2, "Bullets " + row["first"], offset + row["at"] + 1])
            last = row["first"]
    out.set_toc(toc)
    out.save(OUT, garbage=4, deflate=True)
    front_pdf.unlink()
    print(f"{OUT.relative_to(ROOT)}: {len(out)} pages, {number} cited pages, "
          f"{contents['located']} quotations highlighted, {contents['missed']} not located")


if __name__ == "__main__":
    main()
