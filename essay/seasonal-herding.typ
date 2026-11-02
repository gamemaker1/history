// Seasonal herding in the Himachal hills, 1881-1961. Essay skeleton.
//
// Build the PDF with "typst compile essay/seasonal-herding.typ".
// Count the words with "pdftotext essay/seasonal-herding.pdf - | wc -w". The
// count includes the footnotes and the bibliography.
//
// Each section below has a comment block with its word budget, the claim of
// the section, the source pages to cite, and the computed figures. The source
// pages are in essay/reading_pack.pdf under the same section number. The word
// budgets add up to 3,850 words of body text, and the brief allows 3,000 to
// 4,000 words.
//
// Citations are footnotes in the Chicago notes-bibliography style. A source
// page is cited as @brahmaur[p. 55]. Page numbers are PDF page numbers, which
// are the page counter of a PDF viewer. Section 2 states this once.
//
// Figures marked IMAGE were read by Claude from page images. No person has
// checked them, and the checked_by column is empty in data/flocks.csv and
// data/fee_flocks.csv. Each IMAGE figure is checked against the scan in the
// reading pack before it is used.

#set document(
  title: "Seasonal herding in the Himachal hills, 1881-1961",
  author: ("Vishak Kashyap K", "Vedant Kulkarni", "Himangi Sahoo"),
)
#set page(paper: "a4", margin: (x: 2.5cm, y: 2.5cm), numbering: "1")
#set text(font: "Libertinus Serif", size: 12pt, lang: "en")
#set par(justify: true, leading: 0.8em, first-line-indent: 1.2em, spacing: 0.8em)
#set heading(numbering: "1.1")
#show heading: set block(above: 1.4em, below: 0.8em)
#show heading.where(level: 1): set text(size: 14pt)
#show heading.where(level: 2): set text(size: 12pt, style: "italic", weight: "regular")
#set footnote.entry(separator: line(length: 30%, stroke: 0.5pt))

#align(center)[
  #text(size: 18pt, weight: "bold")[Seasonal herding in the Himachal hills, 1881--1961] \
  #v(0.8em)
  Vishak Kashyap K, Vedant Kulkarni, Himangi Sahoo \
  Introduction to History (HS3.201), IIIT Hyderabad, Monsoon 2026
]
#v(1em)

= Introduction
// Budget is 300 words.
// Claim. The months and routes of the migration were set by mountain and
// season. Property and the state determined who could take part in the
// migration and who received a share of its product.
// The section opens with two descriptions of the Gaddi year written eighty
// years apart. In @ibbetson1881[p. 275] the Gaddis spend the winter in Kangra
// and the summer across the range in Chamba. In @brahmaur[p. 55] the flocks go
// to Kangra, Nurpur and Pathankot in October and November.
// The section then states the research question as written in
// ideas/research-question.pdf, names the Annales reading (Braudel and Bloch)
// and the Marxist reading (class analysis and the dialectic), and lists the
// sections in order.

= Sources and method
// Budget is 400 words.
// The first paragraph describes the corpus. It holds the 1961 village surveys
// of the ten study villages named in the research question, Newell's study of
// the Gaddis, the Weaving survey, the Mahasu handbook, the 1961 Punjab Census
// Atlas, the 1881 census, Rose's Glossary and the 1931 census.
// The second paragraph describes the method. Keyword scores were used to
// select 510 pages. A language model proposed claims from those pages, and a
// script kept a claim only if its quotation is on the cited page. The 1,964
// kept claims form an evidence graph, and every chart is a query on that graph
// (computational-analysis.md, entries A2 to A19).
// The third paragraph covers source criticism. The text-reuse search found
// 4,698 copied passages. Barnes's account of the Gujars in
// @ibbetson1881[p. 267] is copied in @rose2[p. 346], so the two pages count as
// one witness. Rose's account of the Gaddi year in @rose2[p. 297] is not a
// copy. Newell's report repeats Rose and Rose Vol1 in 91 passages of 1,720
// words, all on PDF pages 52 to 99. Newell's pages on grazing, fees and
// permits (pages 9 to 38 and 101 to 105) hold no copied passage (entry A19).
// The section also states that page numbers are PDF pages and that the
// livestock tables were read from page images.

= The mountain year: geography and the longue durée

== Relief, snow, forest and pasture
// Budget is 300 words. This section covers the longue durée item of the
// research question, which is relief, climate, rivers, forests and pasture.
// Claim. Snow and altitude determined when and where the flocks could graze.
// In @ibbetson1881[p. 275] cultivation lies between 3,500 and 7,000 feet, with
// little above. In @kupha[p. 111] the passes are closed by snow from the middle
// of November until May. In @newell[p. 18] the Kugti pass is over 16,000 feet
// high, and the pasture lower down lies among forests. In @newell[p. 10] the
// Gaddi country is a series of river sections of about 40 miles. In
// @brahmaur[p. 24] and @chitrari[p. 38] the villagers take timber, firewood and
// grass from forests held by the Forest Department.
// The rank correlation between altitude and sheep and goats per household is
// 0.54 across 19 villages (entry A18). In the Ravi, Sutlej and Chenab valleys,
// every village above about 2,000 m keeps 13 to 45 sheep and goats per
// household, and every village below that height keeps fewer than six.
// Shakrori stands at 1,700 feet (@shakrori[p. 11]) and Tandi at ten thousand
// feet (@tandi[p. 18]). Chaupal stands at 7,685 feet on the Yamuna side and
// keeps 1.6 animals per household (@chaupal[p. 12]). Brahmaur keeps 45.3 per
// household (IMAGE, @brahmaur[p. 54]).

== The calendar from 1881 to 1961
// Budget is 250 words. This section covers Bloch's first comparison, which
// sets the 1881 census, Rose and the 1961 surveys side by side.
// Claim. The same months are recorded by independent witnesses over eighty
// years.
// The witnesses are @ibbetson1881[p. 275], @rose2[p. 297],
// @census1931[p. 142] and @brahmaur[p. 55]. In @brahmaur[p. 63], 61 of 99
// households move out in winter. In @kupha[p. 113] the Gaddis stay in Pangi
// from July to September. In @maingal[p. 52] the Gujjars go up in May and
// return in September. In @kanum[p. 85] the Kinnaur flocks stay in the lower
// hills until the end of April.
// Women go with the flocks, as recorded in @newell[p. 36] and
// @brahmaur[p. 79].
// The calendar chart is in analysis/calendar/calendar.png.

== Routes and the 1961 Atlas
// Budget is 200 words. This section covers the mapping item of the research
// question, which names the Atlas.
// Claim. Each village lies in one valley, and its flocks cross the ranges into
// other river valleys each year.
// Maps 252 and 253 in @atlas[p. 290] and @atlas[p. 291] give the sheep and
// goats in each tahsil. The notes in @atlas[p. 367] state that sheep "live
// mainly on grazing" and "are more numerous" in Kangra, Simla, and Lahaul and
// Spiti. The Atlas covers only the districts then in Punjab, which are Kangra,
// Kulu, Lahaul and Spiti, and Simla. Chamba and the other Himachal districts
// are not in it.
// The Sutlej route to the Lavi fair is in @kanum[p. 15] and @kanum[p. 16].
// The route map is in analysis/maps/routes.png.

= Comparisons

== High herders and low buyers: Brahmaur and Bir
// Budget is 150 words. This section covers Bloch's second comparison.
// Claim. The low villages took part in the migration as buyers of animals and
// wool.
// In @bir[p. 43], 24 households own 139 goats and 69 sheep, bought from
// Gaddis for 10 to 12 rupees. In @batal[p. 46] and @shakrori[p. 75] the
// villagers buy wool and animals from passing Kinnauras.

== Herding families and settled farmers: Brahmaur and Devi-Kothi
// Budget is 200 words. This section covers Bloch's third comparison.
// Claim. The same mountain supported different relations of production.
// In @brahmaur[p. 55] the malundi tends his own flock, and hired shepherds,
// called pohals, are employed only in rare cases. Their wage is on the same
// page. In @devikothi[p. 48] farmers send their animals up with paid graziers
// at 20 to 25 naye paise a head. In @newell[p. 37] most Gaddis are not
// shepherds. In @maingal[p. 52] the Gaddis of Maingal are settled farmers.

== Two valleys: the Ravi and the Sutlej
// Budget is 250 words. This section covers Bloch's fourth comparison.
// Claim. Ravi herders traded south to Kangra and the plains. Sutlej herders
// traded with Tibet, and their pastures were commons under a ruler who held
// the title of Primary Owner.
// In @brahmaur[p. 59] the Gaddis sell gardus in the low hills. The Tibet trade
// and its calendar are in @kanum[p. 131] and @kanum[p. 132]. The Lavi fair is
// in @mahasu[p. 56], and Tibetan trade sheep are in @rose1[p. 523]. The
// Primary Owner and the labour service called Athada Begar are in
// @kanum[p. 18]. In @kanum[p. 133] every villager may use the pastures. In
// @newell[p. 18] all grazing rights in Chamba belonged to the raja.
// Trade words occur 33.6 times per 10,000 words in the Kanum survey and 8.3
// times in the Brahmaur survey (entry A2).

= Owners, workers and debtors
// Budget is 550 words. This section covers Marx's class analysis, which asks
// who owned the flocks, who herded them and who took a share of the product.
// It also covers the tables of livestock and debt.
// Claim. The landholding castes owned the flocks. Households without flocks
// took part in the herding economy as hired shepherds and as debtors.
// Landholding castes hold 89.3% of the 12,210 sheep and goats in the caste
// tables (IMAGE, entry A10). In @brahmaur[p. 54] Brahmans and Rajputs are 83
// of 99 households. Forty of these households own flocks, and they hold 4,391
// of the 4,484 sheep and goats. The old draft wrote "40 of the village's 99
// households", which does not match the table. Further caste tables are in
// @kothi[p. 102], @kanum[p. 61], @tandi[p. 96] and @kupha[p. 80]. In
// @nachar[p. 33] a family keeps 100 to 200 animals and the Lambardar keeps
// about 1,100. In @rajana[p. 47] Kolis hold 302 of 488 goats, which is an
// exception to the pattern.
// On hired labour, @kanum[p. 132] records fawals paid Rs 60 a year. In
// @tandi[p. 65] each household pays the village shepherd one patha of
// buckwheat per animal.
// The surveys arrange their debt tables by income group or by cause, not by
// caste (@maingal[p. 42], @kanum[p. 55], @devikothi[p. 53], @bir[p. 35]).
// Caste appears only in the prose. In @maingal[p. 38] Gujjars owe debts in food
// grain to Gaddi Brahmins. In @maingal[p. 42], @maingal[p. 60] and
// @maingal[p. 61] every Gujjar household is in debt at 30% interest and sells
// its ghee to the lender. In @kanum[p. 53] the landlord lends to the Scheduled
// Castes. In @chergaon[p. 66] tenants pay their interest in labour.

= Conjunctures and their contradictions
// Budget is 800 words for the four subsections. This section covers the
// dialectic, applied to each conjuncture named in the research question.

== Two sovereigns, 1881
// Budget is 100 words.
// Contradiction. Two states made claims on one population.
// In @ibbetson1881[p. 275] the Gaddis hold land in Kangra and Chamba, and a
// fine paid in Kangra was paid again in Chamba. In @newell[p. 18] Gaddis
// crossing into Lahul paid grazing tax to both the Chamba ruler and the Lahul
// ruler.

== The raja's pastures, to 1950
// Budget is 200 words.
// Contradiction. The raja owned the pastures and the shepherds used them. The
// fees were collected through a revenue farm, in which one Gaddi collected
// from other Gaddis.
// In @newell[p. 16] the raja could dispose only of the right to use the land.
// In @newell[p. 18] the raja auctioned the right to collect grazing fees,
// usually to a Gaddi, and the 1950 rates per animal are listed. In
// @brahmaur[p. 55] the ruler's contractor allotted the pastures in return for
// manure. In @newell[p. 14] an official was paid in wool. In @kupha[p. 113] an
// attempt in 1874 to lease the high pastures was abandoned after opposition.

== Forest Department permits, 1948 to 1961
// Budget is 300 words.
// Contradiction. Conservation of the pastures conflicted with the herders'
// living. The permit became a form of property.
// In @newell[p. 19] and @newell[p. 15] the Forest Department takes over the
// grazing tax. In @brahmaur[p. 55] each shepherd has a fixed pasture and pays
// Rs 15 per hundred animals, and in @brahmaur[p. 46] no additional permits are
// granted. In @devikothi[p. 47] the Department charges right holders less only
// for buffaloes (Table XIV, read from the page image), and @devikothi[p. 49]
// records that the rights came from the early rulers. The Rs 5 and Re 1 fees on
// @devikothi[p. 48] are for permits to extract dhup, not for grazing. Erosion, closures and the
// villagers' resentment are in @chitrari[p. 23] and @kupha[p. 136].
// The raja's contractor took about Rs 0.09 per sheep and Rs 0.16 per goat for
// each grazing district a flock entered in 1950. The Department took a fee per
// head for the season in 1961, twice a year in Brahmaur (@brahmaur[p. 55]). The
// units differ, and no source gives the number of districts a flock grazed, so
// the two fees cannot be compared per head per year.
// The number of fee-paying sheep and goats fell by 25.7% between the 1952-53
// and 1961-62 counts. It fell by 3.2% between 1952-53 and 1956-57, by 22.1%
// between 1956-57 and 1959-60, and by 1.4% between 1959-60 and 1961-62 (IMAGE,
// @newell[p. 38]). A note on the same page describes 1959-60 as the year after
// a sheep disease. In @newell[p. 37] shepherds buy and sell permits, and Newell
// calls them "closed corporations".
// The fee chart is in analysis/fees/fee_flocks.png.

== Roads and wages, to 1961
// Budget is 200 words.
// Contradiction. Flock owners needed hired shepherds, and the shepherds could
// now be paid higher wages on the roads.
// In @kanum[p. 51] labourers prefer road work to work as fawals. In
// @brahmaur[p. 45] road work pays about Rs 2 a day. In @kothi[p. 79] 24 persons
// work on the roads, and @nachar[p. 32] records the same work in Nachar. In
// @chitrari[p. 24] a shepherd reports a jeep on the old shepherds' track. In
// @tandi[p. 57] the Rohtang route has been made jeepable. The roads of 1947 and
// 1961 are in @atlas[p. 372], @atlas[p. 308] and @atlas[p. 309], and road
// labourers in Lahaul are in @atlas[p. 331]. In @brahmaur[p. 87] the surveyor
// writes that the roads are "likely to change the cycle of their life".

= Interpretation: three times of the mountain year
// Budget is 300 words. This section covers Braudel's three scales of time.
// The longue durée is the calendar and the altitude threshold, which stayed
// the same, as set out in Section 3.
// The conjunctures are the four arrangements of Section 6, with the people who
// gained in each.
// The events are the 1948 merger (@kothi[p. 16]), the end of the Tibet trade
// (@kanum[p. 51], @weaving[p. 16], @chergaon[p. 61]) and the 1959 sheep
// disease (@newell[p. 38]).
// The answer to the question is that the migration continued as an
// adaptation to mountain and season, and that by 1961 fewer owners, each
// holding a permit, took part in it.

= Conclusion and limits
// Budget is 150 words.
// The limits are listed here. A language model proposed the claims, and a
// script filtered them. A count of claims measures how often the sources
// mention a relation, not the size of the payment. The 19 villages were chosen
// by the Census. Copied colonial passages are counted once. No source dates
// the closing of Shipki La. The section states whether the group has checked
// the IMAGE figures.

#bibliography("refs.yml", style: "chicago-notes", title: "Bibliography")
