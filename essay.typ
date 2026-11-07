#import "@preview/lilaq:0.5.0" as lq

#set document(title: "Seasonal Herding in the Himachal Hills, 1881 to 1961")
#set page(paper: "a4", margin: 2.5cm, numbering: "1")
#set text(font: "C059", size: 11pt, lang: "en")
#set par(justify: true)
#set heading(numbering: "1.1.")
#show heading: set text(size: 11pt)
#show heading: set block(above: 1.5em, below: 0.8em)
#set figure(placement: auto, gap: 0.6em)
#show figure: set block(above: 1.2em, below: 1.2em)
#set place(clearance: 1.2em)
#show figure.caption: set text(size: 9.5pt)
#set table(stroke: none, inset: (x: 5pt, y: 3pt))
#show table.cell.where(y: 0): set text(weight: "bold")
#set bibliography(style: "chicago-notes", title: [Bibliography], full: true)
#show bibliography: set text(size: 10pt)

#let ticks(..values) = values.pos().map(v => (v, str(v)))

#let src(..parts) = text(fill: rgb("#c58a9e"), size: 0.92em)[\[#parts.pos().join("; ")\]]
#let pg(page) = if type(page) == str [PDF pp. #page] else [PDF p. #page]
#let hp(village, page) = [Census of India 1961, Vol. XX (Himachal Pradesh), Part VI, Village Survey Monograph: #village, #pg(page)]
#let hps(..items) = [Census of India 1961, Vol. XX (Himachal Pradesh), Part VI, Village Survey Monographs: #items.pos().map(((village, page)) => [#village, #pg(page)]).join("; ")]
#let tandi(page) = [Census of India 1961, Vol. XIII (Punjab), Part VI, Village Survey Monograph: Tandi, #pg(page)]
#let atlas(page) = [Census of India 1961, Vol. XIII (Punjab), Part IX, Punjab Census Atlas, #pg(page)]
#let c1881(page) = [Report on the Census of the Panjab, 1881, Results, #pg(page)]
#let rose(page) = [A Glossary of the Tribes and Castes of the Punjab and North-West Frontier Province, Vol. 2, #pg(page)]
#let braudel(page) = [History and the Social Sciences: The Longue Durée, #pg(page)]
#let bloch(page) = [The Historian's Craft, #pg(page)]
#let leroy(page) = [The History of Rain and Fine Weather, #pg(page)]

#let villages = (
  ("Tandi", "3,048", 21.3, 92.2),
  ("Kanum", "2,926", 16.2, 95.5),
  ("Kothi", "2,515", 20.0, 94.5),
  ("Chaupal", "2,342", 1.6, 31.0),
  ("Maingal", "2,286", 13.1, 54.6),
  ("Devi-Kothi", "2,164", 22.3, none),
  ("Brahmaur", "2,134", 45.3, 97.9),
  ("Kalath", "1,829", 0.9, none),
  ("Chitrari", "1,829", 2.0, none),
  ("Chergaon", "1,829", 2.1, 90.9),
  ("Rajana", "1,676", 3.5, 40.1),
  ("Chaunri", "1,600", 0.8, 8.9),
  ("Kot", "1,219", 2.0, 98.6),
  ("Bir", "1,219", 5.8, none),
  ("Moginand", "792", 2.3, 26.2),
  ("Shakrori", "518", 1.3, 96.1),
)

#let village-figure = {
  let n = villages.len()
  let rows = villages.enumerate().map(((i, v)) => (n - 1 - i, ..v))
  let kept = rows.filter(r => r.at(3) != none)
  set text(size: 8.5pt)
  lq.diagram(
    width: 9cm, height: 7cm,
    title: [Sheep and goats per household],
    xlim: (0, 50), ylim: (-0.7, n - 0.3),
    xaxis: (ticks: ticks(..range(0, 51, step: 10)), subticks: none),
    yaxis: (ticks: rows.map(r => (r.at(0), [#r.at(1) #text(fill: gray)[#r.at(2) m]])), subticks: none),
    lq.hbar(kept.map(r => r.at(3)), kept.map(r => r.at(0)), fill: rgb("#2a78d6"), width: 0.55),
    lq.hlines(n - 7.5, stroke: (paint: gray, dash: "dashed")),
  )
}

#let band-figure = {
  set text(size: 8.5pt)
  lq.diagram(
    width: 12cm, height: 2.6cm,
    xlim: (0, 3200), ylim: (-0.6, 1.6),
    xlabel: [Altitude (m)],
    xaxis: (ticks: ticks(0, 500, 1000, 1500, 2000, 2500, 3000), subticks: none),
    yaxis: (ticks: ((1, [Punjab Census Atlas]), (0, [Barnes, 1881])), subticks: none),
    lq.hbar((1800, 3200), (1, 1), base: (900, 1800), fill: (rgb("#86b6ef"), rgb("#1c5cab")), width: 0.6),
    lq.hbar((2134, 3200), (0, 0), base: (1067, 2134), fill: (rgb("#f3a27d"), rgb("#c2471a")), width: 0.6),
    lq.place(1350, 1, [High hills]),
    lq.place(2500, 1, text(fill: white)[Mountainous areas]),
    lq.place(1600, 0, [Gaddi villages and fields]),
    lq.place(2667, 0, text(fill: white)[Little or no cultivation]),
  )
}

#let calendar-figure = {
  let months = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
  let low = rgb("#2a78d6")
  let moving = rgb("#eb6834")
  let high = rgb("#1baf7a")
  let key(color, label) = box[#box(width: 0.6em, height: 0.6em, fill: color) #label]
  set text(size: 8.5pt)
  stack(
    spacing: 0.3cm,
    lq.diagram(
      width: 12cm, height: 3cm,
      xlim: (0, 12), ylim: (-0.6, 2.6),
      legend: none,
      xaxis: (ticks: months.enumerate().map(((i, m)) => (i + 0.5, m)), subticks: none),
      yaxis: (ticks: ((2, [Rose, 1911 (Ravi)]), (1, [Brahmaur survey, 1961 (Ravi)]), (0, [Kanum survey, 1961 (Sutlej)])), subticks: none),
      lq.hbar((12, 12, 12, 3, 3, 4), (2, 1, 0, 2, 1, 0), base: (11, 11, 10, 0, 0, 0), fill: low, width: 0.5),
      lq.hbar((11, 11, 10, 5, 4, 6), (2, 1, 0, 2, 1, 0), base: (9, 9, 9, 3, 3, 4), fill: moving, width: 0.5),
      lq.hbar((9, 9, 9), (2, 1, 0), base: (5, 4, 6), fill: high, width: 0.5),
    ),
    align(center)[#key(low)[In the low hills] #h(1.2em) #key(moving)[On the move] #h(1.2em) #key(high)[Summer pastures and village]],
  )
}

#align(center)[
  #text(size: 15pt, weight: "bold")[Seasonal Herding in the Himachal Hills, 1881 to 1961]
  #v(0.6em)
  Vishak Kashyap K #h(2em) Vedant Kulkarni #h(2em) Himangi Sahoo
]
#v(1em)

= Introduction <sec-intro>

In the Himachal hills, many families move their flocks with the seasons, while keeping a fixed home and fields. They take the flocks up to high pastures in summer and down to low grazing in winter. This is called transhumance. For #cite(<braudel-longue-duree>, form: "author"), it is an example of a structure of the longue durée: _"Man is a prisoner for long centuries of climates, of vegetations, of animal populations ... Take the role of transhumance in mountain life"_ #src(braudel(10)).

We study the Gaddis of the Ravi valley and the Kinnauras of the upper Sutlej, who keep sheep and goats, and the Gujjars, who keep buffaloes. Their villages are on four rivers (@fig-village-map). Brahmaur, Chitrari, Devi-Kothi and Maingal are in Chamba on the Ravi. Kanum, Kothi and Nachar are in Kinnaur on the upper Sutlej, and Shakrori is lower down the Sutlej in Mahasu. Kupha in Pangi and Tandi in Lahaul are on the Chenab, and Bir is in Mandi on the Beas #src(hps(("Brahmaur", 55), ("Kanum", 16), ("Maingal", 52))).

#figure(
  image("figures/hp-village-surveys.jpg", width: 5.6cm),
  caption: [Census map of the 1961 village surveys of Himachal Pradesh, printed in the Devi-Kothi survey. The study villages in Chamba, Kinnaur, Mandi and Mahasu are marked on it, but Tandi in Punjab is not.],
) <fig-village-map>

Our period runs from the census of 1881 to the village surveys of 1961. Over these years, the people living in these regions had to face many changes, including in their rulers. In 1881, Kangra was British territory, while Chamba and Bushahr had their own rulers. In 1948, the hill states were joined to form Himachal Pradesh, but Kangra and Lahaul were still in Punjab in 1961 #src(c1881(275), hp("Kothi", 16), tandi(5), atlas(22)).

In this essay, we explore how the yearly movement of flocks shaped life in the hills from 1881 to 1961, who controlled it, and who gained from it. We ask whether the herding cycle was fixed by the mountains and seasons, or changed by the owners of the flocks, pastures and labour.

= Sources and Methods <sec-sources>

== Sources

Our main sources are the village surveys of the 1961 Census for Himachal Pradesh, together with the Tandi survey from the Punjab series. We also use four other books from the 1961 Census: Newell's study of the Gaddis, a survey of weaving, the Mahasu district handbook and the Punjab Census Atlas. For the earlier years, we use the 1881 census of the Punjab, Rose's Glossary of 1911 to 1919 and the 1931 census of the Punjab.

== Computational Methods

There are thousands of pages in these books, so we first scored each page by how often words related to herding appear on it, and read only the pages with the highest scores. From those pages, we used a language model to pull out claims. A claim is one statement from one page, together with the words it comes from, and we kept a claim only if those words appear on the page. We then used a second model to check each claim against its page, and dropped the claims marked as not supported.

We joined the claims we kept into a knowledge graph, in which the people, places and things named in the claims are linked by the claims themselves. We tagged each claim with its conjuncture and the year of its source, so that we can count the claims for each period. Of about 1,800 claims proposed, about 150 failed one of the two checks, and nearly 2,000 claims are in the graph, including those read from tables.

Some authors copied from earlier reports. A copied passage and its original are one piece of evidence, so we also searched for passages that appear word for word in two sources. When the same details are in two accounts, #cite(<bloch-craft>, form: "author") notes that either _"one of them had copied the other or ... both had copied a common model."_ In our search, there is no copied text in Newell's pages on grazing and migration, but the 1881 census's account of the Gujjars is in Rose's Glossary word for word, so we count those two as one piece of evidence #src(bloch(36), c1881(267), rose(346)).

== Historical Methods <sec-hist>

To read this evidence as history, we combine two schools, the Annales and Marxism. From the Annales, we take the order of the analysis. #cite(<braudel-longue-duree>, form: "author") divides historical time into three times of different speeds, all present at once: the longue durée, the slow time of geography and structures; the conjuncture, the time of medium-term cycles; and the event, the short time of single happenings. We call this temporal parallelism. The three times can be pictured as a river. The riverbed moves the slowest, like the longue durée, the deeper water moves at a middle speed, like the conjuncture, and the water at the surface rushes along, like the event. Following this order, we first set out the geography of the hills, then the economic and social trends of each conjuncture, and then the political events #src(braudel("5–10")).

The Annales historians also compare records. #cite(<bloch-craft>, form: "author") notes that _"we can never interpret a document except by inserting it into a chronological series or a synchronous whole."_ So we compare our sources across the years, and the Ravi valley with the Sutlej valley #src(bloch(32)).

To study the events in depth, we use Marxism, while keeping the longue durée and the conjunctures as the frame around them. In Marxist history, a society is built on its material basis, which is the way people produce what they live on and the question of who owns the means to do so. In the hills, the means of production were the flocks and the pastures, and the relations of production were those between the people who owned them and the people who did the work, such as owners and hired shepherds. The Marxist historian also looks for contradictions inside this basis, where one group gains from the labour of another. So for each event, we ask who owned the flocks and pastures, who did the labour, and who took a share of what that labour produced.

= Geography <sec-geography>

== Geographical Time

#cite(<braudel-longue-duree>, form: "author") writes that _"all structures are simultaneously pillars and obstacles."_ The mountains were both for the herders. The 1881 census and the Brahmaur survey both record summer grazing high in the mountains and winter grazing in the low hills of Kangra. But each kind of grazing was available for only part of the year. In Maingal, at about 2,300 m, the survey records heavy snow from November to March, about 1.5 m deep on average. In the low hills, the 1881 census records that the Gujjars left for the upper range _"during the hot weather."_ The herders therefore had to move between high and low ground, and the times and places of their moves were set by height, rain and snow #src(braudel(9), c1881("275, 267"), hps(("Brahmaur", 55), ("Maingal", 12))).

There are only a few weather records in the village surveys, so, as #cite(<leroyladurie-rain>, form: "author") does in his history of climate, we check the records of the herding year from 1881, 1911 and 1961, and from two valleys, against each other and against the rain and snow in the surveys #src(leroy(1)).

== Altitude

In 1881, Barnes reported the Gaddis living between about 1,070 or 1,220 m and 2,130 m, with little or no farming above (@fig-zones). The villages and fields lay in this band, the summer pastures above it, and the winter grazing in the low hills below it #src(c1881(275)).

#figure(
  band-figure,
  caption: [Bands of height in the Punjab Census Atlas and in Barnes's account of 1881. Barnes's heights are converted from feet to metres, and his band is drawn from the lower of his two figures.],
) <fig-zones>

In @fig-villages, we see the height of each village and the number of sheep and goats per household. In the Ravi, Sutlej and Chenab valleys, the village surveys record more than ten animals per household in every village above 2,000 m. Only two survey villages in these valleys lie below 2,000 m, Chitrari and Shakrori, and they have one or two #src(hps(("Kanum", 61), ("Kothi", 102), ("Maingal", 48), ("Devi-Kothi", 47), ("Brahmaur", 54), ("Chitrari", 52), ("Shakrori", 76)), tandi(96)).

#figure(
  village-figure,
  caption: [Sheep and goats per household in each survey village, ordered by stated altitude. The dashed line is at 2,000 m, and Chaupal, on the Yamuna, is the only high village with few animals.],
) <fig-villages>

== Rain and Vegetation

On the Atlas map, rain is heavier towards the hills (@fig-rain-veg). Inside the Himachal hills, the Kanum survey describes Kinnaur beyond Kalpa as arid, and the Tandi survey records only about 13 cm of rain a year in Lahaul, which is out of reach of the monsoon. In the rainfall tables of Shakrori and Maingal, July, August and September have about half to three-fifths of the year's rain. In these wettest months, the Gaddi flocks are in the dry inner mountains of Pangi and Lahaul #src(atlas(28), hps(("Kanum", 19), ("Shakrori", 12), ("Maingal", 13), ("Brahmaur", 55)), tandi(19), rose(297)).

#figure(
  grid(
    columns: 2,
    column-gutter: 0.5cm,
    image("figures/p028-mean-annual-rainfall.jpg", width: 6.2cm),
    image("figures/p044-vegetation-types.jpg", width: 6.2cm),
  ),
  caption: [Mean annual rainfall and vegetation types, Maps 8 and 13 of the Punjab Census Atlas, 1961. The maps are of the Punjab of 1961 only, without Chamba, Kinnaur, Mandi or Mahasu.],
) <fig-rain-veg>

On the Atlas map of vegetation, the belts from the low hills of Kangra to Lahaul and Spiti are subtropical pine forest, moist temperate forest, alpine forest and dry temperate mixed forest, and the flocks pass through each of them on their way up and down #src(atlas(44)).

== Seasons

The Kupha survey records the passes of Pangi closed by snow from mid-November to May, and the Tandi survey records the route into Lahaul closed from the end of October to the end of April. The flocks that spend the summer in Pangi and Lahaul have to cross these passes twice a year, after they open in spring and before they close in autumn #src(hp("Kupha", 111), tandi(18)).

The records of the Gaddi year are within these dates. The 1881 census names no months, but it records that the flocks spent _"half the year (the winter months) in the valleys of Kangra."_ In 1911, #cite(<rose2>, form: "author") wrote that _"the yearly exodus to Kangra takes place in October and November, and the return journey in April and May."_ The Brahmaur survey of 1961 records the flocks going down in October and November and coming back in April. Since we found no copied text between these three passages, we treat them as separate pieces of evidence #src(c1881(275), rose(297), hp("Brahmaur", 55)).

The herders of the Sutlej valley used the same calendar. The Kanum survey records the people of Kanum leaving for the lower hills in October, spending _"the chilly months"_ there, and returning in May and June #src(hp("Kanum", "85, 16")). We compare the dated records in @fig-calendar.

#figure(
  calendar-figure,
  placement: none,
  caption: [The herding year in the dated records of the Ravi and Sutlej valleys. The months in the summer pastures are inferred from the months of leaving and of return in each record.],
) <fig-calendar>

Across the eighty years of our records and in both valleys, the herding calendar was the same, which fits a structure of the longue durée.

= Economy and Society <sec-socio>

== Movement <sec-movement>

== Flocks <sec-flocks>

== Trade <sec-trade>

== Social Structure <sec-social>

= Political Events <sec-events>

= Interpretation <sec-interp>

== Three Levels of Time <sec-clocks>

== Limits of Geography <sec-limits>

== Conjunctures <sec-conjunctures>

== Evidence Graph <sec-graph>

== Events and Structures <sec-meet>

== Ravi and Sutlej <sec-ravi-sutlej>

== Findings <sec-insights>

= Conclusion <sec-conclusion>

#pagebreak()
#bibliography("references.yaml")
