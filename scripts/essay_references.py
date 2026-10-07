#!/usr/bin/env python3
"""Build the essay's numbered reference list, in order of first citation.

The essay cites primary pages as \\src{Source}{page} and secondary works as
\\citep{key}. This script reads essay/essay.tex, numbers every cited work in
the order of its first citation (primary and secondary together), and
writes:

  essay/srckeys.tex      maps each source name used in \\src to its BibTeX-style
                         key (\\input in the preamble, so \\src can \\citep it)
  essay/references.tex   the numbered reference list (\\input at the end)
  analysis/essay/reference_numbers.csv
                         number, key, source name and full reference; used by
                         build_sources_pdf.py to label each page with its number

Rerun it whenever the essay's citations change, then run pdflatex twice.

Usage (from the project folder):
  python3 scripts/essay_references.py

Standard library only.
"""

import csv
import re

from corpus import ANALYSIS, ROOT

ESSAY = ROOT / "essay" / "essay.tex"

VILLAGE_DISTRICT = {
    "Basal": "Solon tahsil, Mahasu District", "Batal": "Arki tahsil, Mahasu District",
    "Brahmaur": "Chamba District", "Bir": "Mandi District", "Chaunri": "Kasumpti tahsil, Mahasu District",
    "Chauntra": "Jogindar Nagar tahsil, Mandi District", "Chaupal": "Mahasu District",
    "Chergaon": "Rohru tahsil, Mahasu District", "Chitrari": "Chamba District", "Devi-Kothi": "Chamba District",
    "Kanum": "Kinnaur District", "Kot": "Sarkaghat tahsil, Mandi District", "Kothi": "Kinnaur District",
    "Kupha": "Pangi, Chamba District; covers Kupha, Parmas, Thamoh and Malet", "Maingal": "Chamba District",
    "Moginand": "Sirmur District", "Nachar": "Kinnaur District", "Nalag": "Mandi District",
    "Pangna": "Karsog tahsil, Mandi District", "Rajana": "Rainka tahsil, Sirmur District",
    "Shakrori": "Seoni sub-tahsil, Mahasu District", "Shathla": "Kumarsain sub-tahsil, Mahasu District",
}

PRIMARY = {
    "1881": r"Denzil Ibbetson, \emph{Report on the Census of the Panjab, 1881}, Results volume (Calcutta, 1883). "
            r"The settlement reports of Barnes and Lyall are quoted in it.",
    "Rose": r"H.~A.~Rose, \emph{A Glossary of the Tribes and Castes of the Punjab and North-West Frontier Province}, "
            r"vol.~2 (Lahore, 1911).",
    "Rose Vol1": r"H.~A.~Rose, \emph{A Glossary of the Tribes and Castes of the Punjab and North-West Frontier Province}, "
                 r"vol.~1 (Lahore, 1919).",
    "Rose Vol3": r"H.~A.~Rose, \emph{A Glossary of the Tribes and Castes of the Punjab and North-West Frontier Province}, "
                 r"vol.~3 (Lahore, 1914).",
    "1931": r"Khan Ahmad Hasan Khan, \emph{Census of India, 1931, Vol.~XVII: Punjab}, Part~I, Report "
            r"(Lahore: Civil and Military Gazette Press, 1933).",
    "Newell": r"William H.~Newell, \enquote{The Gaddi and Affiliated Castes of the Western Himalayas}, in "
              r"Census of India 1961, \emph{Report on Scheduled Castes and Scheduled Tribes of Himachal Pradesh}.",
    "Weaving": r"Census of India 1961, Himachal Pradesh, \emph{Craft Survey: Weaving}.",
    "Mahasu": r"Census of India 1961, Himachal Pradesh, \emph{District Census Handbook: Mahasu}.",
    "Simla": r"Census of India 1961, Punjab, \emph{District Census Handbook: Simla}.",
    "Tandi": r"Census of India 1961, Vol.~XIII (Punjab), Part~VI, \emph{Village Survey Monograph: Tandi} "
             r"(Lahaul and Spiti District).",
    "Kalath": r"Census of India 1961, Vol.~XIII (Punjab), Part~VI, \emph{Village Survey Monograph: Kalath} "
              r"(Simla District).",
}

SECONDARY = {
    "braudel": r"Fernand Braudel, \emph{The Mediterranean and the Mediterranean World in the Age of Philip~II}, "
               r"trans.\ Si\^an Reynolds, 2 vols (London: Collins, 1972).",
    "bloch": r"Marc Bloch, \enquote{Pour une histoire compar\'ee des soci\'et\'es europ\'eennes}, "
             r"\emph{Revue de synth\`ese historique} 46 (1928).",
    "marx3": r"Karl Marx, \emph{Capital: A Critique of Political Economy}, vol.~3, Part~VI, "
             r"\enquote{Transformation of Surplus-Profit into Ground-Rent} (1894).",
    "ph-kwic": r"\emph{The Programming Historian}, \enquote{Keywords in Context (Using n-grams) with Python} and "
               r"\enquote{Counting Word Frequencies with Python}, \url{https://programminghistorian.org/en/lessons/}.",
    "ph-passim": r"\emph{The Programming Historian}, \enquote{Detecting Text Reuse with Passim}, "
                 r"\url{https://programminghistorian.org/en/lessons/detecting-text-reuse-with-passim}.",
}


def reference(source):
    if source in PRIMARY:
        return PRIMARY[source]
    return (rf"Census of India 1961, Vol.~XX (Himachal Pradesh), Part~VI, \emph{{Village Survey Monograph: {source}}} "
            rf"({VILLAGE_DISTRICT.get(source, 'Himachal Pradesh')}).")


def key(source):
    return "src-" + "-".join(re.findall(r"[a-z0-9]+", source.lower()))


def main():
    tex = ESSAY.read_text(encoding="utf-8")
    body = tex[tex.index("\\begin{document}"):]
    order = []
    for m in re.finditer(r"\\(?:src|srcimg)\{([^}]*)\}\{[^}]*\}|\\cite[pt]?(?:\[[^\]]*\])?\{([^}]*)\}", body):
        if m.group(1) is not None:
            item = ("primary", m.group(1))
        else:
            for k in m.group(2).split(","):
                k = k.strip()
                src = next((x for x in list(PRIMARY) + list(VILLAGE_DISTRICT) if key(x) == k), None)
                item = ("secondary", k) if k in SECONDARY else ("primary", src) if src else ("key", k)
                if item not in order:
                    order.append(item)
            continue
        if item not in order:
            order.append(item)

    rows, keys_tex, bib = [], [], []
    for n, (kind, name) in enumerate(order, 1):
        if kind == "primary":
            k, text = key(name), reference(name)
            keys_tex.append(rf"\expandafter\def\csname srckey@{name}\endcsname{{{k}}}")
        elif kind == "secondary":
            k, text = name, SECONDARY[name]
        else:  # a \citep to a primary key written by hand, e.g. \citep{src-1881}
            k = name
            src = next((s for s in list(PRIMARY) + list(VILLAGE_DISTRICT) if key(s) == name), None)
            text = reference(src) if src else name
        bib.append(rf"\bibitem{{{k}}} {text}")
        rows.append({"number": n, "key": k, "source": name if kind == "primary" else "", "reference": text})

    out = ROOT / "essay"
    (out / "srckeys.tex").write_text("% generated by scripts/essay_references.py\n" + "\n".join(keys_tex) + "\n",
                                     encoding="utf-8")
    (out / "references.tex").write_text(
        "% generated by scripts/essay_references.py, in order of first citation\n"
        "\\begin{thebibliography}{99}\\small\n" + "\n".join(bib) + "\n\\end{thebibliography}\n", encoding="utf-8")
    csv_out = ANALYSIS / "essay" / "reference_numbers.csv"
    csv_out.parent.mkdir(parents=True, exist_ok=True)
    with open(csv_out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["number", "key", "source", "reference"])
        w.writeheader()
        w.writerows(rows)
    prim = sum(1 for k, _ in order if k != "secondary")
    print(f"{len(order)} numbered references ({prim} primary sources, {len(order) - prim} secondary works) "
          f"written to essay/references.tex and essay/srckeys.tex")


if __name__ == "__main__":
    main()
