#!/usr/bin/env python3
"""Unpack the 1961 and 1881 zips in sources/ into cache/pdf/ and write a manifest of every PDF.

The zips hold duplicate copies of several village surveys under catalogue
numbers (for example 23212_1961_KAN.pdf is the Kanum survey). This script
keeps one copy of each distinct file, by SHA-256, and prefers the copy whose
name matches a text file in text/. It skips desktop.ini.

It then writes analysis/source_manifest.csv, one row per PDF used by the
project (the unpacked ones and the 1931 and Rose PDFs in sources/), with its
page count, checksum, matching text file, and whether the text file has one
form feed per PDF page. scripts/pageref.py and every page reference rely on
that last check.

Usage (from the project folder):
  .venv/bin/python scripts/unpack_sources.py

Needs pymupdf (requirements.txt) for page counts. Requires `git lfs pull`
first: the files in sources/ are Git LFS objects.
"""

import csv
import hashlib
import zipfile
from pathlib import Path

import pymupdf

from corpus import ANALYSIS, PDF_1931, PDF_CACHE, PDF_ROSE, ROOT, TEXT, ZIP_1881, ZIP_1961, read

ZIPS = [(ZIP_1961, "1961"), (ZIP_1881, "1881")]


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def unpack(zip_rel, folder):
    """Extract distinct PDFs from one zip. Returns rows describing each zip member."""
    zip_path = ROOT / zip_rel
    with open(zip_path, "rb") as f:
        if f.read(40).startswith(b"version https://git-lfs"):
            raise SystemExit(f"{zip_rel} is a Git LFS pointer. Run `git lfs pull` first.")
    out_dir = PDF_CACHE / folder
    out_dir.mkdir(parents=True, exist_ok=True)
    text_stems = {p.stem for p in (TEXT / folder).glob("*.txt")}

    zf = zipfile.ZipFile(zip_path)
    members = [m for m in zf.infolist() if m.filename.lower().endswith(".pdf")]
    by_hash = {}
    for m in members:
        by_hash.setdefault(sha256(zf.read(m)), []).append(m)

    rows = []
    for digest, copies in by_hash.items():
        # Prefer the copy that has a text file, then the descriptive name.
        copies.sort(key=lambda m: (Path(m.filename).stem not in text_stems,
                                   not Path(m.filename).name.startswith("1961 Census"),
                                   m.filename))
        keep = copies[0]
        target = out_dir / Path(keep.filename).name
        if not target.exists():
            target.write_bytes(zf.read(keep))
        for m in copies:
            rows.append({"zip": Path(zip_rel).name, "member": m.filename, "sha256": digest,
                         "kept_as": str(target.relative_to(ROOT)) if m is keep else "",
                         "duplicate_of": "" if m is keep else Path(keep.filename).name})
    return rows


def text_for(pdf_path, folder):
    t = TEXT / folder / f"{pdf_path.stem}.txt"
    return t if t.exists() else None


def main():
    zip_rows = []
    for zip_rel, folder in ZIPS:
        zip_rows += unpack(zip_rel, folder)

    pdfs = [(p, "1961") for p in sorted((PDF_CACHE / "1961").glob("*.pdf"))]
    pdfs += [(p, "1881") for p in sorted((PDF_CACHE / "1881").glob("*.pdf"))]
    pdfs += [(ROOT / v, "1931") for v in PDF_1931.values()]
    pdfs += [(ROOT / v, "rose") for v in PDF_ROSE.values()]
    text_stem = {**{v: k for k, v in PDF_1931.items()}, **{v: k for k, v in PDF_ROSE.items()}}

    manifest = []
    for pdf, folder in pdfs:
        rel = str(pdf.relative_to(ROOT))
        txt = text_for(pdf, folder) if folder in ("1961", "1881") else TEXT / folder / f"{text_stem[rel]}.txt"
        with pymupdf.open(pdf) as doc:
            n_pages = doc.page_count
        form_feeds = read(txt).count("\f") if txt else None
        manifest.append({
            "pdf": rel,
            "layer": folder,
            "pdf_pages": n_pages,
            "text_file": str(txt.relative_to(ROOT)) if txt else "",
            "text_form_feeds": form_feeds if form_feeds is not None else "",
            "pages_match": (form_feeds == n_pages) if txt else "",
            "sha256": sha256(pdf.read_bytes()),
        })

    ANALYSIS.mkdir(exist_ok=True)
    with open(ANALYSIS / "source_manifest.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(manifest[0].keys()))
        w.writeheader()
        w.writerows(manifest)
    with open(ANALYSIS / "zip_members.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(zip_rows[0].keys()))
        w.writeheader()
        w.writerows(zip_rows)

    kept = [r for r in zip_rows if r["kept_as"]]
    print(f"zip members: {len(zip_rows)} PDFs, {len(kept)} distinct, unpacked to {PDF_CACHE.relative_to(ROOT)}/")
    with_text = [m for m in manifest if m["text_file"]]
    bad = [m for m in with_text if not m["pages_match"]]
    print(f"manifest: {len(manifest)} PDFs, {len(with_text)} with a text file, "
          f"{len(with_text) - len(bad)} with one form feed per PDF page")
    for m in bad:
        print(f"  page mismatch: {m['pdf']} has {m['pdf_pages']} pages, text has {m['text_form_feeds']} form feeds")
    for m in manifest:
        if not m["text_file"]:
            print(f"  no text file: {m['pdf']}")


if __name__ == "__main__":
    main()
