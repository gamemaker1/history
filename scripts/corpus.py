"""Shared paths and text helpers for the scripts in this folder.

The text files in text/ keep one form-feed character per PDF page, so page n
of a text file is the n-th chunk between form feeds. Page numbers are PDF
page numbers (the page counter in a PDF viewer), not the printed page numbers
on the scans.

The PDFs themselves live in sources/ (1931 and Rose) or inside the two zips
in sources/ (1961 and 1881). scripts/unpack_sources.py extracts the zips to
cache/pdf/, which is where pdf_path() looks for them.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT = ROOT / "text"
DATA = ROOT / "data"
ANALYSIS = ROOT / "analysis"
CACHE = ROOT / "cache"
PDF_CACHE = CACHE / "pdf"

ZIP_1961 = "sources/1961 Village surveys + census reports-20260926T175323Z-1-001.zip"
ZIP_1881 = "sources/Punjab 1881, Denzil Ibbetson-20260926T175319Z-1-001.zip"

PDF_1931 = {
    "1931 Part I Report": "sources/Census of India 1931, Vol 17 Punjab, Part I Report.pdf",
    "1931 Part II Tables": "sources/Census of India 1931, Vol 17 Punjab, Part II Tables.pdf",
}
_ROSE_STEM = "sources/2015.{}.Glossary-Of-The-Tribes-And-Castes-Of-The-Punjab-And-North-west-Frontier-Province-{}.pdf"
PDF_ROSE = {
    "Rose Vol1": _ROSE_STEM.format("69651", "Vol1_text"),
    "Rose Vol2": _ROSE_STEM.format("69652", "Vol2"),
    "Rose Vol3": _ROSE_STEM.format("69674", "Vol3_text"),
}

# Short name of each PDF, as cited in the idea files and claims.
PDF_FOR = {
    "1961": lambda name: f"{name}.pdf (inside {ZIP_1961})",
    "1961_layout": lambda name: f"{name}.pdf (inside {ZIP_1961})",
    "1881": lambda name: f"{name}.pdf (inside {ZIP_1881})",
    "1931": lambda name: PDF_1931[name],
    "rose": lambda name: {k: v.replace(
        "Glossary-Of-The-Tribes-And-Castes-Of-The-Punjab-And-North-west-Frontier-Province", "Glossary-...")
        for k, v in PDF_ROSE.items()}[name],
}

# The 25 Himachal village surveys, keyed by the name used in citations, with
# the text file stem. Kupha covers four Pangi villages in one volume.
VILLAGES = {
    "Basal": "1961 Census, Village Survey (Basal- Solon Mahasu)",
    "Batal": "1961 Census, Village Survey (Batal- Arki Mahasu)",
    "Brahmaur": "1961 Census, Village Survey (Bhrhmaur - Chamba)",
    "Bir": "1961 Census, Village Survey (Bir - Mandi)",
    "Chaunri": "1961 Census, Village Survey (Chaunri - Kasumpti Mahasu)",
    "Chauntra": "1961 Census, Village Survey (Chauntra - Jogindar Nagar Mandi)",
    "Chaupal": "1961 Census, Village Survey (Chaupal - Mahasu)",
    "Chergaon": "1961 Census, Village Survey (Chergaon - Rohru Mahasu)",
    "Chitrari": "1961 Census, Village Survey (Chitrari)",
    "Devi-Kothi": "1961 Census, Village Survey (Devi-Kothi, Chamba)",
    "Kalath": "1961 Census, Village Survey (Kalath Simla Dist)",
    "Kanum": "1961 Census, Village Survey (Kanum Kinnaur)",
    "Kot": "1961 Census, Village Survey (Kot - Sarkaghat Mandi)",
    "Kothi": "1961 Census, Village Survey (Kothi Kinnaur)",
    "Kupha": "44160_1961_KUP",
    "Maingal": "1961 Census, Village Survey (Maingal - Chamba)",
    "Moginand": "1961 Census, Village Survey (Moginand, Sirmur)",
    "Nachar": "1961 Census, Village Survey (Nachar - Kinnaur)",
    "Nalag": "1961 Census, Village Survey (Nalag - Mandi)",
    "Pangna": "1961 Census, Village Survey (Pangna - Karsog Mandi)",
    "Rajana": "1961 Census, Village Survey (Rajana - Rainka Sirmur)",
    "Shakrori": "1961 Census, Village Survey (Shakrori - Seoni Mahasu)",
    "Shathla": "1961 Census, Village Survey (Shathla - Kumarsain Mahasu)",
    "Tandi": "1961 Census, Village Survey (Tandi Lahaul-Spiti)",
}

# The ten villages named in ideas/research-question.pdf.
STUDY_VILLAGES = ["Brahmaur", "Chitrari", "Devi-Kothi", "Maingal", "Kanum",
                  "Kothi", "Nachar", "Shakrori", "Bir", "Tandi"]

# Other 1961 volumes used as sources, keyed by citation name.
REPORTS_1961 = {
    "Newell": "1961 Census, Report on SC and ST of Himachal Pradesh",
    "Weaving": "1961 Census, Himachal Pradesh Craft Survey - Weaving",
    "Mahasu": "1961 Census, District Handbook - Mahasu",
    "Simla": "1961 Census, District Census Handbook - Simla",
}

STEM_TO_NAME = {v: k for k, v in {**VILLAGES, **REPORTS_1961}.items()}

# Colonial sources by citation name: text file and the year of the layer.
COLONIAL = {
    "1881": ("1881/2. Census of the Punjab, 1881, Denzil Ibbetson, Results, pp 1-421.txt", 1881),
    "Rose Vol1": ("rose/Rose Vol1.txt", 1919),
    "Rose": ("rose/Rose Vol2.txt", 1911),
    "Rose Vol3": ("rose/Rose Vol3.txt", 1914),
    "1931": ("1931/1931 Part I Report.txt", 1931),
    "1931 Tables": ("1931/1931 Part II Tables.txt", 1931),
}


def source_text(name):
    """Text file for any citation name: a village, a 1961 report or a colonial source."""
    if name in COLONIAL:
        return TEXT / COLONIAL[name][0]
    return text_path(name)


def layer_year(name):
    return COLONIAL[name][1] if name in COLONIAL else 1961

WORD = re.compile(r"[a-z0-9]+")


def village_of(path):
    """Citation name of a 1961 village survey text file, or "" for any other file."""
    name = STEM_TO_NAME.get(Path(path).stem, "")
    return name if name in VILLAGES else ""


def source_name(path):
    """Citation name of a text file: a village, a 1961 report, or the file stem."""
    return STEM_TO_NAME.get(Path(path).stem, Path(path).stem)


def text_path(name, layout=False):
    """Text file for a citation name such as "Kanum" or "Newell"."""
    stem = {**VILLAGES, **REPORTS_1961}[name]
    return TEXT / ("1961_layout" if layout else "1961") / f"{stem}.txt"


def pdf_name(path):
    """Short PDF name for a text file, as used in citations."""
    path = Path(path)
    return PDF_FOR[path.parent.name](path.stem)


def pdf_path(path):
    """Local path of the PDF behind a text file (after unpack_sources.py)."""
    path = Path(path)
    folder, stem = path.parent.name, path.stem
    if folder in ("1961", "1961_layout"):
        return PDF_CACHE / "1961" / f"{stem}.pdf"
    if folder == "1881":
        return PDF_CACHE / "1881" / f"{stem}.pdf"
    if folder == "1931":
        return ROOT / PDF_1931[stem]
    if folder == "rose":
        return ROOT / PDF_ROSE[stem]
    raise ValueError(f"no PDF known for {path}")


def read(path):
    return Path(path).read_text(encoding="utf-8", errors="ignore")


def load(path):
    """Read a text file and rejoin words hyphenated across line breaks.

    Returns the text and a list of newline offsets for line-number lookup.
    The rejoin keeps the newline so line numbers stay correct.
    """
    text = re.sub(r"(\w)-\n(\w+)", r"\1\2\n", read(path))
    newlines = [i for i, c in enumerate(text) if c == "\n"]
    return text, newlines


def pages(path):
    """List of page texts. pages(path)[0] is PDF page 1."""
    return read(path).split("\f")


def page_text(path, n):
    """Text of PDF page n (1-based)."""
    p = pages(path)
    if n < 1 or n > len(p):
        raise IndexError(f"page {n} is outside {Path(path).name} (1 to {len(p)})")
    return p[n - 1]


def normalise(text):
    """Lower-case words with their character offsets, hyphenated breaks rejoined."""
    text = re.sub(r"(\w)-[ \t]*\n[ \t]*(\w)", r"\1\2", text)
    return text, [(m.group(0), m.start()) for m in WORD.finditer(text.lower())]


def tokens(text):
    """Lower-case word tokens of a text, hyphenated breaks rejoined."""
    return [w for w, _ in normalise(text)[1]]
