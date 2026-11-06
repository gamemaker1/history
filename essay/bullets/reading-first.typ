#set page(paper: "a4", numbering: none)
#set text(font: "C059", size: 10.5pt, lang: "en")
#set par(justify: true)
#set heading(numbering: none)
#show heading: set text(weight: "bold")
#show link: set text(fill: rgb("#0064E0"))

#let c = json("reading-first.json")

#let note(body) = block(fill: luma(245), stroke: (left: 2pt + luma(160)), inset: 8pt, width: 100%, body)

#text(size: 17pt, weight: "bold")[Readings for the Essay]
#v(-4pt)
6 November 2026

This file holds every PDF page that the bullet points for the essay cite, in
the order in which they are best read. The course readings come first,
because the essay is ordered by Braudel's levels of historical time and
explained in Marx's categories, and every section of the bullets depends on
them. The primary-source pages follow, grouped by the section of the bullets
that first cites them. A page cited by two or more sections appears once, under
its first section.

Each page is the original PDF page with a grey margin column on its right.
The column names the source and the PDF page and lists every bullet that
cites the page, with the number of its section. Each quotation that a bullet
takes from the page is highlighted in yellow on the page, and the highlight
carries the bullet as a pop-up note in a PDF viewer. A quotation that the
search did not locate is printed in red at the foot of the column. Of the
quotations, #c.located were highlighted and #c.missed were not located. Pages
whose figures were read from the page image carry a red notice, because no
person has checked those figures.

#note[Page numbers in the margin column and in the bullets are PDF page
numbers, which count from the first page of the PDF file. Page numbers in the
tables below are pages of this file.]

== Reading Order

+ Braudel, pages 5 to 10, 18, 29 and 32. These pages define the longue durée,
  the conjuncture and the event, and state that the three levels run at the
  same time. Twelve bullets cite them, in Sections 1.1, 2.3, 3.1 and 6.
+ Bloch, chapter III, pages 23, 32, 36 and 42. These pages give the rules for
  judging witnesses, for detecting copying between sources, and for
  comparison. Five bullets cite them, in Sections 2.2, 2.3 and 6.4.
+ Alam's slides on Marxist history, then Marx's two articles on British rule
  in India and the excerpt of the Manifesto. These define the material basis,
  the relations of production and the contradiction. Twelve bullets cite
  them, mostly in Section 6.3.
+ Habib, then Kosambi, Le Roy Ladurie and Aymard. Habib is cited by five
  bullets in Section 6. The other three are cited by one bullet each, Le Roy
  Ladurie in Section 3.1 and the other two in Section 6.3.
+ The primary-source pages, section by section, while drafting that section.
  The 13 pages cited by four or more bullets are listed in the second table
  below.

== Course Readings

#context {
  let off = counter(page).final().first()
  table(
    columns: (6%, 34%, 10%, 38%, 12%),
    stroke: none,
    inset: (x: 4pt, y: 3pt),
    table.hline(),
    [*No.*], [*Reading*], [*PDF page*], [*Bullet sections*], [*Page here*],
    table.hline(),
    ..c.course.map(r => (str(r.n), r.short, str(r.page), r.sections.join(", "), str(off + r.at + 1))).flatten(),
    table.hline(),
  )
}

#for k in c.course.map(r => r.key).dedup() {
  let r = c.course.find(x => x.key == k)
  par(justify: false)[#emph(r.short). #r.source. #r.role]
}

== Most Cited Primary Pages

#context {
  let off = counter(page).final().first()
  let top = c.primary.filter(r => r.uses >= 4).sorted(key: r => -r.uses)
  table(
    columns: (6%, 30%, 10%, 10%, 32%, 12%),
    stroke: none,
    inset: (x: 4pt, y: 3pt),
    table.hline(),
    [*No.*], [*Source*], [*PDF page*], [*Bullets*], [*Bullet sections*], [*Page here*],
    table.hline(),
    ..top.map(r => (str(r.n), r.short, str(r.page), str(r.uses), r.sections.join(", "), str(off + r.at + 1))).flatten(),
    table.hline(),
  )
}

== Primary Sources by Section

#context {
  let off = counter(page).final().first()
  table(
    columns: (6%, 30%, 10%, 10%, 32%, 12%),
    stroke: none,
    inset: (x: 4pt, y: 3pt),
    table.hline(),
    [*No.*], [*Source*], [*PDF page*], [*Bullets*], [*Bullet sections*], [*Page here*],
    table.hline(),
    ..c.primary.map(r => (
      str(r.n), r.short + if r.image [ (image-read)], str(r.page), str(r.uses), r.sections.join(", "),
      str(off + r.at + 1),
    )).flatten(),
    table.hline(),
  )
}
