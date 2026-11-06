// Page and text setup for a history essay with Chicago footnote citations.
// A document applies it with `#show: essay.with(title: ..., authors: ...)`.

#let essay(
  title: none,
  authors: (),
  course: none,
  date: none,
  // The bibliography element, as `bibliography("refs.yml")`. It is placed
  // after the body, with a heading and the Chicago notes style.
  bib: none,
  body,
) = {
  set document(title: title, author: authors)
  set page(paper: "a4", margin: (x: 2.5cm, y: 2.5cm), numbering: "1", number-align: center)
  set text(font: "C059", size: 11pt, lang: "en", region: "us")
  set par(justify: true, leading: 0.72em, spacing: 0.72em, first-line-indent: (amount: 1.5em, all: false))

  set heading(numbering: "1.")
  show heading: set text(size: 11pt, weight: "bold")
  show heading: set block(above: 1.5em, below: 0.8em)

  // A quotation longer than about four lines is set as a block quotation
  // without quotation marks, and its footnote goes after the final period.
  set quote(block: true)
  show quote.where(block: true): it => block(inset: (left: 1.5em, right: 1.5em), above: 1em, below: 1em)[
    #set text(size: 10pt)
    #set par(first-line-indent: 0pt)
    #it.body
  ]

  set footnote.entry(separator: line(length: 30%, stroke: 0.5pt), gap: 0.5em, indent: 0em)
  show footnote.entry: set text(size: 9pt)
  show footnote.entry: set par(justify: true, first-line-indent: 0pt, hanging-indent: 0pt)

  set figure(placement: auto)
  show figure.caption: set text(size: 9.5pt)
  set table(stroke: none, inset: (x: 5pt, y: 3pt))
  show table.cell.where(y: 0): set text(weight: "bold")

  show link: set text(fill: rgb("#0064E0"))

  // In the Chicago notes and bibliography style, a citation becomes a footnote. The first
  // note for a source is a full note, and later notes are short notes.
  set bibliography(style: "chicago-notes", title: heading(numbering: none)[Bibliography], full: false)
  show bibliography: set par(hanging-indent: 1.5em, first-line-indent: 0pt, justify: false)
  show bibliography: set text(size: 10pt)

  block(below: 1.6em)[
    #set par(first-line-indent: 0pt)
    #text(size: 16pt, weight: "bold", title)
    #v(0.2em)
    #authors.join(", ")
    #if course != none [ \ #course]
    #if date != none [ \ #date]
  ]

  body

  if bib != none {
    pagebreak(weak: true)
    bib
  }
}
