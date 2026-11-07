#import "@preview/lilaq:0.5.0" as lq

#set document(title: "Seasonal Herding in the Himachal Hills, 1881 to 1961")
#set page(paper: "a4", margin: 2.5cm, numbering: "1")
#set text(font: "C059", size: 11pt, lang: "en")
#set par(justify: true)
#set heading(numbering: "1.1.")
#show heading.where(level: 1): set text(size: 13pt)
#show heading.where(level: 2): set text(size: 11pt)
#show heading: set block(above: 1.5em, below: 0.8em)
#set figure(placement: auto, gap: 0.6em)
#show figure: set block(above: 1.2em, below: 1.2em)
#set place(clearance: 1.2em)
#show figure.caption: set text(size: 9.5pt)
#set table(stroke: none, inset: (x: 5pt, y: 3pt))
#show table.cell.where(y: 0): set text(weight: "bold")
#show table: set text(size: 9.5pt)
#show table: set par(justify: false)
#set bibliography(style: "chicago-notes", title: [Bibliography], full: false)
#show bibliography: set text(size: 10pt)

#let slate = rgb("#3f6e9a")
#let mist = rgb("#9cc3e0")
#let sage = rgb("#5f9e6e")
#let sand = rgb("#e9b85c")
#let clay = rgb("#c8553d")

#let ticks(..values) = values.pos().map(v => (v, str(v)))

#let mark(letters) = if letters != "" { super(letters) }
#let again(lab, letters) = { h(0pt, weak: true); footnote(lab); mark(letters) }
#show footnote.entry: set par(justify: false)

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
    yaxis: (ticks: rows.map(r => (r.at(0), [#r.at(1) #text(fill: luma(85))[#r.at(2) m]])), subticks: none),
    lq.hbar(kept.map(r => r.at(3)), kept.map(r => r.at(0)), fill: slate, width: 0.55),
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
    yaxis: (ticks: ((1, [Punjab Census Atlas]), (0, [Barnes, in the 1881 census])), subticks: none),
    lq.hbar((1800, 3200), (1, 1), base: (900, 1800), fill: (mist, slate), width: 0.6),
    lq.hbar((2134, 3200), (0, 0), base: (1067, 2134), fill: (sand, clay), width: 0.6),
    lq.place(1350, 1, [High hills]),
    lq.place(2500, 1, text(fill: white)[Mountainous areas]),
    lq.place(1600, 0, [Gaddi villages and fields]),
    lq.place(2667, 0, text(fill: white)[Little or no cultivation]),
  )
}

#let own-figure = {
  let rows = (("Brahmaur", "4,484", 97.9, "Rajput"), ("Kothi", "2,557", 94.5, "Rajput"), ("Kanum", "1,827", 95.5, "Kanet (Rajput)"), ("Kupha", "596", 93.0, "Rajput"), ("Tandi", "384", 92.2, "Bodh"), ("Maingal", "405", 54.6, "Brahmin"), ("Rajana", "559", 40.1, "Koli"), ("Pangna", "62", 4.8, "Koli"), ("Chaunri", "45", 8.9, "Koli"))
  let n = rows.len()
  set text(size: 8.5pt)
  lq.diagram(
    width: 10cm, height: 5.4cm,
    xlim: (0, 125), ylim: (-0.6, n - 0.4),
    xlabel: [Share held by landholding castes (%)],
    xaxis: (ticks: ticks(0, 25, 50, 75, 100), subticks: none),
    yaxis: (ticks: rows.enumerate().map(((i, r)) => (n - 1 - i, [#r.at(0) #text(fill: luma(85))[#r.at(1)]])), subticks: none),
    lq.hbar(rows.map(r => r.at(2)), range(n).rev(), fill: slate, width: 0.55),
    ..rows.enumerate().map(((i, r)) => lq.place(r.at(2) + 2, n - 1 - i, text(fill: luma(85))[#r.at(3)], align: left)),
  )
}

#let series-figure = {
  let years = ("1952–53", "1956–57", "1959–60", "1961–62")
  let sheep = (42176, 40600, 30828, 30515)
  let goats = (31695, 30896, 24864, 24406)
  let totals = ("73,871", "71,496", "55,692", "54,921")
  set text(size: 8.5pt)
  lq.diagram(
    width: 9cm, height: 5.5cm,
    xlim: (-0.6, 3.6), ylim: (0, 100000),
    ylabel: [Fee-paying animals],
    legend: (position: top + right),
    xaxis: (ticks: years.enumerate(), subticks: none),
    yaxis: (ticks: ((0, [0]), (20000, [20,000]), (40000, [40,000]), (60000, [60,000]), (80000, [80,000])), subticks: none),
    lq.bar(range(4), sheep, fill: slate, width: 0.55, label: [Sheep]),
    lq.bar(range(4), goats.zip(sheep).map(((g, s)) => g + s), base: sheep, fill: sand, width: 0.55, label: [Goats]),
    ..range(4).map(i => lq.place(i, sheep.at(i) + goats.at(i) + 1500, totals.at(i), align: bottom)),
  )
}

#let calendar-figure = {
  let months = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
  let low = sand
  let moving = clay
  let high = sage
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

In the Himachal hills, many families move their flocks with the seasons, while keeping a fixed home and fields. They take the flocks up to high pastures in summer and down to low grazing in winter. This is called transhumance. For Fernand Braudel, it is an example of a structure of the longue durée: _"Man is a prisoner for long centuries of climates, of vegetations, of animal populations ... Take the role of transhumance in mountain life"_.#h(0pt, weak: true)#footnote[#cite(<braudel-longue-duree>, style: "short-title.csl"), PDF p. 10.]

We study the Gaddis of the Ravi valley and the Kinnauras of the upper Sutlej, who keep sheep and goats, and the Gujjars, who keep buffaloes. Most of their villages are on four rivers (@fig-village-map). Brahmaur, Chitrari, Devi-Kothi and Maingal are in Chamba on the Ravi. Kanum, Kothi and Nachar are in Kinnaur on the upper Sutlej, and Shakrori is lower down the Sutlej in Mahasu. Kupha in Pangi and Tandi in Lahaul are on the Chenab, and Bir is in Mandi on the Beas.#h(0pt, weak: true)#footnote[Gaddis: #cite(<brahmaur1961>, style: "short-title.csl"), PDF p. 55. Kinnauras: #cite(<kanum1961>, style: "short-title.csl"), PDF p. 16. Gujjars: #cite(<maingal1961>, style: "short-title.csl"), PDF p. 52.]

#figure(
  image("figures/hp-village-surveys.jpg", width: 7.5cm),
  caption: [Census map of the 1961 village surveys of Himachal Pradesh. The villages in the districts of Chamba, Kinnaur, Mandi and Mahasu are marked, but Tandi in Punjab is not.#h(0pt, weak: true)#footnote[#cite(<devikothi1961>, style: "short-title.csl"), PDF p. 2.]],
) <fig-village-map>

Our period runs from the census of 1881 to the village surveys of 1961. Over these years, the people living in these regions had to face many changes, including in their rulers. In 1881, Kangra was British territory, while Chamba and Bushahr had their own rulers. In 1948, the hill states were joined to form Himachal Pradesh, but Kangra and Lahaul were still in Punjab in 1961.#h(0pt, weak: true)#footnote[Rulers in 1881: #cite(<ibbetson1881>, style: "short-title.csl"), PDF p. 275. Merger of 1948: #cite(<kothi1961>, style: "short-title.csl"), PDF p. 16. Kangra and Lahaul in Punjab: #cite(<tandi1961>, style: "short-title.csl"), PDF p. 5; #cite(<atlas1961>, style: "short-title.csl"), PDF p. 22.]

In this essay, we explore how the yearly movement of flocks shaped life in the hills from 1881 to 1961, who controlled it, and who gained from it. We ask whether the herding cycle was fixed by the mountains and seasons, or changed by the owners of the flocks, pastures and labour.

= Sources and Methods <sec-sources>

== Sources

Our main sources are the village surveys of the 1961 Census for Himachal Pradesh, together with the Tandi and Kalath surveys from the Punjab series. We also use four other books from the 1961 Census: Newell's study of the Gaddis, a survey of weaving, the Mahasu district handbook and the Punjab Census Atlas. For the earlier years, we use the 1881 census of the Punjab, Rose's Glossary of 1911 to 1919 and the 1931 census of the Punjab.

== Computational Methods

There are thousands of pages in these books, so we first scored each page by how often words related to herding appear on it, and read only the pages with the highest scores. From those pages, we used a language model to pull out claims. A claim is one statement from one page, together with the words it comes from, and we kept a claim only if those words appear on the page. We then used a second model to check each claim against its page, and dropped the claims marked as not supported.

We joined the claims we kept into a knowledge graph, in which the people, places and things named in the claims are linked by the claims themselves. We tagged each claim with its conjuncture and the year of its source, so that we can count the claims for each period. The code, the data, the analysis and this essay are at #link("https://github.com/gamemaker1/history")[github.com/gamemaker1/history].

Some authors copied from earlier reports. A copied passage and its original are one piece of evidence, so we also searched for passages that appear word for word in two sources. When the same details are in two accounts, Marc Bloch notes that either _"one of them had copied the other or ... both had copied a common model."_ In our search, there is no copied text in Newell's pages on grazing and migration, but the 1881 census's account of the Gujjars is in Rose's Glossary word for word, so we count those two as one piece of evidence.#h(0pt, weak: true)#footnote[Bloch on copying: #cite(<bloch-craft>, style: "short-title.csl"), PDF p. 36. Gujjars in 1881: #cite(<ibbetson1881>, style: "short-title.csl"), PDF p. 267. The same account in Rose: #cite(<rose2>, style: "short-title.csl"), PDF p. 346.]

== Historical Methods <sec-hist>

To read this evidence as history, we combine two schools, the Annales and Marxism. From the Annales, we take the order of the analysis. Braudel divides historical time into three times of different speeds, all present at once: the longue durée, the slow time of geography and structures; the conjuncture, the time of medium-term cycles; and the event, the short time of single happenings. We call this temporal parallelism. The three times can be pictured as a river. The riverbed moves the slowest, like the longue durée, the deeper water moves at a middle speed, like the conjuncture, and the water at the surface rushes along, like the event. Following this order, we first set out the geography of the hills, then the economic and social life of the hills, and then the political events.#h(0pt, weak: true)#footnote[#cite(<braudel-longue-duree>, style: "short-title.csl"), PDF pp. 5–10.]

The Annales historians also compare records. Bloch notes that _"we can never interpret a document except by inserting it into a chronological series or a synchronous whole."_ So we compare our sources across the years, and the Ravi valley with the Sutlej valley.#h(0pt, weak: true)#footnote[#cite(<bloch-craft>, style: "short-title.csl"), PDF p. 32.]

To study the events in depth, we use Marxism, while keeping the longue durée and the conjunctures as the frame around them. In Marxist history, a society is built on its material basis, which is the way people produce what they live on and the question of who owns the means to do so. In the hills, the means of production were the flocks and the pastures, and the relations of production were those between the people who owned them and the people who did the work, such as owners and hired shepherds. The Marxist historian also looks for contradictions inside this basis, where one group gains from the labour of another. So for each event, we ask who owned the flocks and pastures, who did the labour, and who took a share of what that labour produced.

= Geography <sec-geography>

== Geographical Time

Braudel writes that _"all structures are simultaneously pillars and obstacles."_ The mountains were both a support and an obstacle for the herders. The 1881 census and the Brahmaur survey both record summer grazing high in the mountains and winter grazing in the low hills of Kangra. But each kind of grazing was available for only part of the year. In Maingal, at about 2,300 m, the survey records heavy snow from November to March, about 1.5 m deep on average. In the low hills, the 1881 census records that the Gujjars left for the upper range _"during the hot weather."_ The herders therefore had to move between high and low ground, and the times and places of their moves were set by height, rain and snow.#h(0pt, weak: true)#footnote[Braudel: #cite(<braudel-longue-duree>, style: "short-title.csl"), PDF p. 9. Summer and winter grazing: #cite(<ibbetson1881>, style: "short-title.csl"), PDF p. 275; #cite(<brahmaur1961>, style: "short-title.csl"), PDF p. 55. Snow in Maingal: #cite(<maingal1961>, style: "short-title.csl"), PDF p. 12. Gujjars in the hot weather: #cite(<ibbetson1881>, style: "short-title.csl"), PDF p. 267.]

There are only a few weather records in the village surveys, so, as Emmanuel Le Roy Ladurie does in his history of climate, we check the records of the herding year from 1881, 1911 and 1961, and from two valleys, against each other and against the rain and snow in the surveys.#h(0pt, weak: true)#footnote[#cite(<leroyladurie-rain>, style: "short-title.csl"), PDF p. 1.]

== Altitude

Barnes, quoted in the 1881 census, placed the Gaddis between about 1,070 or 1,220 m and 2,130 m, with little or no farming above (@fig-zones). In his account, the villages and fields lay in this band, the summer pastures above it, and the winter grazing in the low hills below it.#h(0pt, weak: true)#footnote[#cite(<ibbetson1881>, style: "short-title.csl"), PDF p. 275.]

#figure(
  band-figure,
  caption: [Bands of height in the Punjab Census Atlas and in Barnes's account in the 1881 census. Barnes's heights are converted from feet to metres, and his band is drawn from the lower of his two figures.#h(0pt, weak: true)#footnote[#cite(<atlas1961>, style: "short-title.csl"), PDF p. 317; #cite(<ibbetson1881>, style: "short-title.csl"), PDF p. 275.]],
) <fig-zones>

In @fig-villages, we see the height of each village and the number of sheep and goats per household. Every village in the figure above 2,000 m has more than ten animals per household, except Chaupal on the Yamuna. The two villages of the Ravi and Sutlej below 2,000 m in the figure, Chitrari and Shakrori, have one or two.#h(0pt, weak: true)#footnote[Villages above 2,000 m: #cite(<kanum1961>, style: "short-title.csl"), PDF p. 61; #cite(<kothi1961>, style: "short-title.csl"), PDF p. 102; #cite(<maingal1961>, style: "short-title.csl"), PDF p. 48; #cite(<devikothi1961>, style: "short-title.csl"), PDF p. 47; #cite(<brahmaur1961>, style: "short-title.csl"), PDF p. 54; #cite(<tandi1961>, style: "short-title.csl"), PDF p. 96. Chitrari and Shakrori: #cite(<chitrari1961>, style: "short-title.csl"), PDF p. 52; #cite(<shakrori1961>, style: "short-title.csl"), PDF p. 76.]

#figure(
  village-figure,
  caption: [Sheep and goats per household in each survey village, ordered by stated altitude. The dashed line is at 2,000 m, and Chaupal, on the Yamuna, is the only high village with few animals.],
) <fig-villages>

== Rain and Vegetation

On the Atlas map, rain is heavier towards the hills (@fig-rain-veg). Inside the Himachal hills, the Kanum survey describes Kinnaur beyond Kalpa as arid, and the Tandi survey records only about 13 cm of rain a year in Lahaul, which is out of reach of the monsoon. In the rainfall tables of Shakrori and Maingal, July, August and September have about half to three-fifths of the year's rain. In these wettest months, the Gaddi flocks are in the dry inner mountains of Pangi and Lahaul.#h(0pt, weak: true)#footnote[Rainfall map: #cite(<atlas1961>, style: "short-title.csl"), PDF p. 28. Arid Kinnaur: #cite(<kanum1961>, style: "short-title.csl"), PDF p. 19. Rain in Lahaul: #cite(<tandi1961>, style: "short-title.csl"), PDF p. 19. Rainfall tables: #cite(<shakrori1961>, style: "short-title.csl"), PDF p. 12; #cite(<maingal1961>, style: "short-title.csl"), PDF p. 13. Flocks in Pangi and Lahaul: #cite(<brahmaur1961>, style: "short-title.csl"), PDF p. 55; #cite(<rose2>, style: "short-title.csl"), PDF p. 297.]

#figure(
  grid(
    columns: 2,
    column-gutter: 0.5cm,
    image("figures/p028-mean-annual-rainfall.jpg", width: 6.2cm),
    image("figures/p044-vegetation-types.jpg", width: 6.2cm),
  ),
  caption: [Mean annual rainfall and vegetation types, Maps 8 and 13 of the Punjab Census Atlas, 1961. The maps are of the Punjab of 1961 only, without Chamba, Kinnaur, Mandi or Mahasu.#h(0pt, weak: true)#footnote[#cite(<atlas1961>, style: "short-title.csl"), PDF pp. 28, 44.]],
) <fig-rain-veg>

On the Atlas map of vegetation, the belts from the low hills of Kangra to Lahaul and Spiti are subtropical pine forest, moist temperate forest, alpine forest and dry temperate mixed forest, and the flocks pass through each of them on their way up and down.#h(0pt, weak: true)#footnote[#cite(<atlas1961>, style: "short-title.csl"), PDF p. 44.]

== Seasons

A forest report of 1891, printed as an appendix to the Kupha survey, records the passes of Pangi closed by snow from mid-November to May, and the Tandi survey records the route into Lahaul closed from the end of October to the end of April. The flocks that spend the summer in Pangi and Lahaul have to cross these passes twice a year, after they open in spring and before they close in autumn.#h(0pt, weak: true)#footnote[Passes of Pangi: #cite(<kupha1961>, style: "short-title.csl"), PDF p. 111. Route into Lahaul: #cite(<tandi1961>, style: "short-title.csl"), PDF p. 18.]

The records of the Gaddi year are within these dates. The 1881 census names no months, but it records that the flocks spent _"half the year (the winter months) in the valleys of Kangra."_ In 1911, Rose wrote that _"the yearly exodus to Kangra takes place in October and November, and the return journey in April and May."_ The Brahmaur survey of 1961 records the flocks going down in October and November and coming back in April. Since we found no copied text between these three passages, we treat them as separate pieces of evidence.#h(0pt, weak: true)#footnote[1881: #cite(<ibbetson1881>, style: "short-title.csl"), PDF p. 275. 1911: #cite(<rose2>, style: "short-title.csl"), PDF p. 297. 1961: #cite(<brahmaur1961>, style: "short-title.csl"), PDF p. 55.]

The herders of the Sutlej valley used the same calendar. The Kanum survey records the people of Kanum leaving for the lower hills in October, spending _"the chilly months"_ there, and returning in May and June. We compare the dated records in @fig-calendar.#h(0pt, weak: true)#footnote[#cite(<kanum1961>, style: "short-title.csl"), PDF pp. 16, 85.]

#figure(
  calendar-figure,
  placement: none,
  caption: [The herding year in the dated records of the Ravi and Sutlej valleys. The months in the summer pastures are inferred from the months of leaving and of return in each record.#h(0pt, weak: true)#footnote[#cite(<rose2>, style: "short-title.csl"), PDF p. 297; #cite(<brahmaur1961>, style: "short-title.csl"), PDF p. 55; #cite(<kanum1961>, style: "short-title.csl"), PDF pp. 16, 85.]],
) <fig-calendar>

Across the eighty years of our records and in both valleys, the herding calendar was the same, which fits a structure of the longue durée.

= Socio-economy <sec-socio>

== Routes and Roads <sec-movement>

In Section 3.4, we set out the months of the Gaddi year. The 1931 census also records that the hillmen _"leave their homes with their sheep and cattle to spend the winter in the valleys and plains"_, but it names no months. In 1961, Brahmaur's flocks came back from the low hills to the village in April. In summer they grazed for two months on the dhars, the high pastures of Pangi and Lahaul, and in early September they started back over the ranges. The forest report of 1891 in the Kupha survey records the Gaddis in Pangi from July to September, so the summer months were the same seventy years earlier. In Brahmaur, out of 99 households, _"as many as 61 move out in winter months"_.#h(0pt, weak: true)#footnote[1931: #cite(<census1931>, style: "short-title.csl"), PDF p. 142. Brahmaur in 1961: #cite(<brahmaur1961>, style: "short-title.csl"), PDF p. 55. Pangi in 1891: #cite(<kupha1961>, style: "short-title.csl"), PDF p. 113. Households that move: #cite(<brahmaur1961>, style: "short-title.csl"), PDF p. 63.]

Other groups kept calendars of their own. The Gujjars of Maingal took their buffaloes up in May and returned in September. According to the Kanum survey, Kinnaur flocks went down the Sutlej to Bilaspur, Arki, Karsog, Seoni and Sirmur and stayed there _"till the end of April"_.#h(0pt, weak: true)#footnote[Gujjars of Maingal: #cite(<maingal1961>, style: "short-title.csl"), PDF p. 52. Kinnaur flocks: #cite(<kanum1961>, style: "short-title.csl"), PDF p. 85.]

By 1961, change in transport was visible. The Atlas records that Kangra and Lahaul and Spiti _"were generally without metalled roads"_ in 1947 and had better road links by 1961. The route over the Rohtang Pass, which was earlier _"only a bridle path"_, was made jeepable from Manali to Keylong. A Gaddi shepherd near Gehra, in the Chitrari survey, said that a jeep now ran on _"our beaten track for centuries"_, and a jeepable road had also reached Kanum.#h(0pt, weak: true)#footnote[Roads in 1947 and 1961: #cite(<atlas1961>, style: "short-title.csl"), PDF p. 372. Rohtang Pass: #cite(<tandi1961>, style: "short-title.csl"), PDF p. 57. Jeep at Gehra: #cite(<chitrari1961>, style: "short-title.csl"), PDF p. 24. Road to Kanum: #cite(<kanum1961>, style: "short-title.csl"), PDF p. 133.]

== Flocks and Grazing Rights <sec-flocks>

Castes with major landholdings held 89.3 per cent of the 12,210 sheep and goats in the caste tables. In Brahmaur, Brahmins and Rajputs held 4,391 of 4,484 animals, the Sipis 93, and the one Rehara household none. In Kothi the Rajputs held 2,416 of 2,557, and in Kanum the Kanets held 1,744 (@fig-own). Even among landholders, flock distribution was unequal. In Nachar, an ordinary family kept _"100 to 200 sheep and goats"_, while the Lambardar, the village headman, _"has about 1,100 strong flock"_ and was _"one of the richer shepherds of Kinnaur"_. In Rajana, Pangna and Chaunri, Koli households held more of the animals than any other caste (@fig-own).#h(0pt, weak: true)#footnote[Brahmaur's animals: #cite(<brahmaur1961>, style: "short-title.csl"), PDF p. 54. Kothi and Kanum: #cite(<kothi1961>, style: "short-title.csl"), PDF p. 102; #cite(<kanum1961>, style: "short-title.csl"), PDF p. 61. Nachar's headman: #cite(<nachar1961>, style: "short-title.csl"), PDF p. 33.]


#figure(
  own-figure,
  caption: [Share of sheep and goats held by landholding castes in selected villages of the 1961 surveys. Grey numbers give the village's animals, and grey names the caste group that held the most.],
) <fig-own>

Labour was arranged in several ways. Most Brahmaur families herded their own animals, and the survey notes that hired shepherds, called pohals, _"are hired in summer season by a very few people in rare cases"_. A pohal was paid in meals, clothing and wool for the family, _"two or four sheep per hundred"_ and _"Rs. 2/- in cash per month"_. In 1940–45, a Kanum trader had four fawals and paid each of them Rs 60 a year with meals, wool, shoes and clothes. In Tandi every household paid the village shepherd _"one patha … of buckwheat per sheep or goat for the season"_, whereas Devi-Kothi farmers sent their animals to the high hills with professional graziers. According to Newell, the majority of Gaddis are not shepherds, and in Chitrari those who migrated were _"the ones who have a sizeable flock to tend"_.#h(0pt, weak: true)#footnote[Pohals: #cite(<brahmaur1961>, style: "short-title.csl"), PDF p. 55. Fawals in Kanum: #cite(<kanum1961>, style: "short-title.csl"), PDF p. 132. Tandi's shepherd: #cite(<tandi1961>, style: "short-title.csl"), PDF p. 65. Graziers in Devi-Kothi: #cite(<devikothi1961>, style: "short-title.csl"), PDF p. 48. Gaddis who are not shepherds: #cite(<newell1961>, style: "short-title.csl"), PDF p. 37. Who migrates in Chitrari: #cite(<chitrari1961>, style: "short-title.csl"), PDF p. 23.]

The holders of grazing rights changed over the period, and they differed from one valley to another. In Chamba, _"all grazing rights belonged to the rajah of Chamba"_, and his subjects had only the right to use the land. The right to collect fees _"was auctioned by the rajah of Chamba to the highest bidder, who was usually a Gaddi"_. Near Brahmaur the Raja leased pastures to a contractor, who allotted them to shepherds on condition that their flocks spent the night in the villagers' fallow fields, and the owners of those fields paid the contractor in grain. In Kanum, by contrast, _"every villager has a right of utilizing the pastures"_ under the Bushahr ruler as Primary Owner.#h(0pt, weak: true)#footnote[Raja's rights and the fee contractor: #cite(<newell1961>, style: "short-title.csl"), PDF pp. 16, 18. Contractor near Brahmaur: #cite(<brahmaur1961>, style: "short-title.csl"), PDF p. 55. Pastures in Kanum: #cite(<kanum1961>, style: "short-title.csl"), PDF pp. 18, 133.]

By 1961, the Forest Department allotted the pastures directly to the shepherds. Each shepherd had a fixed dhar for _"a fixed number of sheep and goats"_, and the Department granted no more permits. In Devi-Kothi, the right holders, whose rights came from the early rulers of Chamba, paid less than others only for buffaloes (@tab-fees).#h(0pt, weak: true)#footnote[Permits by 1961: #cite(<brahmaur1961>, style: "short-title.csl"), PDF pp. 46, 55. Right holders in Devi-Kothi: #cite(<devikothi1961>, style: "short-title.csl"), PDF pp. 47, 49.]

#figure(
  table(
    columns: 5,
    align: (left, right, right, right, right),
    table.hline(),
    table.header(
      [], table.cell(colspan: 2, align: center)[Fee], table.cell(colspan: 2, align: center)[Penalty],
      [*Animal*], [*Others*], [*Right holders*], [*Others*], [*Right holders*],
    ),
    table.hline(stroke: 0.5pt),
    [Buffalo], [6.00], [4.50], [9.00], [6.00],
    [Cow or bull], [1.00], [1.00], [not known], [not known],
    [Goat], [0.25], [0.25], [1.00], [1.00],
    [Sheep], [0.10], [0.10], [0.50], [0.50],
    table.hline(),
  ),
  caption: [Grazing fees and penalties in Devi-Kothi, in rupees per animal, for graziers with and without inherited rights. Only the charges for buffaloes differ.#h(0pt, weak: true)#footnote[#cite(<devikothi1961>, style: "short-title.csl"), PDF p. 47.]],
) <tab-fees>


The number of fee-paying animals in Brahmaur tahsil fell from 73,871 in 1952–53 to 54,921 in 1961–62, mostly between 1957 and 1960 (@fig-series).#h(0pt, weak: true)#footnote[#cite(<newell1961>, style: "short-title.csl"), PDF p. 38.]

#figure(
  series-figure,
  caption: [Sheep and goats that paid the grazing fee in Brahmaur tahsil from 1952–53 to 1961–62. The total fell by 22.1 per cent between 1956–57 and 1959–60.#h(0pt, weak: true)#footnote[#cite(<newell1961>, style: "short-title.csl"), PDF p. 38.]],
) <fig-series>

== Trade and Commerce <sec-trade>

The herders also traded along their routes. Gaddi woollens _"command a ready market in the low hills where people sell them during their stay there in winter months"_. Kanum's people went down with their flocks carrying chilgozas, wool, woollen strips, nuts, pasham, jira (cumin) and other local herbs. They sold them at the Lavi fair at Rampur, the biggest trade fair in Himachal, held in the second week of November, or in other lower villages.#h(0pt, weak: true)#footnote[Gaddi woollens: #cite(<brahmaur1961>, style: "short-title.csl"), PDF p. 59. Kanum's trade and the Lavi fair: #cite(<kanum1961>, style: "short-title.csl"), PDF p. 16; #cite(<mahasu1961>, style: "short-title.csl"), PDF p. 56.]

Kanum's trade also reached across the border. In 1940–45, a Kanum trader began his journey to Tibet in July and was usually back by November, bringing wool, pasham, butter, ghee, goat, sheep and salt. Only 10 or 12 of Kanum's 113 families took part in this trade. Words related to trade occur 33.6 times per 10,000 words in the Kanum survey, against 8.3 in Brahmaur and 6.6 in Maingal.#h(0pt, weak: true)#footnote[#cite(<kanum1961>, style: "short-title.csl"), PDF pp. 131–132.]




Credit ran alongside trade, as households used to borrow from moneylenders, shopkeepers and co-operative societies, and often sold their produce to the same lenders. In the evidence graph, interest paid by households to moneylenders is the most frequent payment relation, with co-operative societies also appearing as lenders in 7 of the surveys. In Maingal, the Gujjars borrowed _"at 30% annual interest"_ from moneylenders who also bought their milk products.#h(0pt, weak: true)#footnote[#cite(<maingal1961>, style: "short-title.csl"), PDF p. 42.]


== Family, Caste and Custom <sec-social>

The whole household took part in the migration. On the spring and autumn journeys _"the wife usually accompanies her husband"_, cooking and taking care of the children while he looks after the sheep. _"Even during migration, she carries an equal load on her back and contributes equally to the family earnings"_.#h(0pt, weak: true)#footnote[Wife on the route: #cite(<newell1961>, style: "short-title.csl"), PDF p. 36. Wife's load: #cite(<brahmaur1961>, style: "short-title.csl"), PDF p. 79.]

Occupation followed caste. In Maingal _"Occupations are classified better on caste basis"_: Gujjars reared buffaloes, Gaddi Brahmins and Rajputs farmed and kept sheep and goats, and _"Gujjars had to pay food grain debts to Gaddi brahmins"_. Elsewhere, debt crossed caste lines, as the landlord-moneylender of Kanum had lent to _"the scheduled castes and others"_, and Bushahr's subjects owed their ruler labour service, _"including 'Athada Begar'"_.#h(0pt, weak: true)#footnote[Occupations in Maingal: #cite(<maingal1961>, style: "short-title.csl"), PDF p. 38. Kanum's moneylender: #cite(<kanum1961>, style: "short-title.csl"), PDF p. 53. Labour service: #cite(<kanum1961>, style: "short-title.csl"), PDF p. 18.]


= Political Events <sec-events>

The forest report of 1891 records that in 1874 _"an attempt was made to lease the dhars or bigger grazing grounds"_ of Pangi, but it _"provoked much opposition"_ and was abandoned.#h(0pt, weak: true)#footnote[#cite(<kupha1961>, style: "short-title.csl"), PDF p. 113.]

Barnes, quoted in the 1881 census, describes Gaddis who held land in both Kangra and Chamba. By an older rule, whenever the Kangra authorities fined them, they also paid _"a similar penalty into the Chamba treasury"_, but in his time the rule was broken more often than kept. Barnes adds that _"our institutions have taught them greater independence"_. On the summer routes, Gaddis who crossed to the Lahaul side of the river _"would need to pay a grazing tax to both the Chamba and Lahuli ruler"_.#h(0pt, weak: true)#footnote[Two treasuries: #cite(<ibbetson1881>, style: "short-title.csl"), PDF p. 275. Two grazing taxes: #cite(<newell1961>, style: "short-title.csl"), PDF p. 18.]

On 15 April 1948 the hill states were merged into a single state and became Himachal Pradesh, and Kinnaur left the state of Rampur Bushahr. The right to levy the grazing tax was taken over by the Government of India State Forest Department, and the tax receipt _"is however not issued unless the shepherd has a permit issued by the Forest Department"_.#h(0pt, weak: true)#footnote[Merger of 1948: #cite(<kothi1961>, style: "short-title.csl"), PDF p. 16. Permits and receipts: #cite(<newell1961>, style: "short-title.csl"), PDF p. 19.]

Newell writes that when Chamba became part of Himachal Pradesh, the Indian Union brought in _"the idea of private property in land"_, and in 1953 a Settlement was begun in Brahmaur tahsil.#h(0pt, weak: true)#footnote[#cite(<newell1961>, style: "short-title.csl"), PDF p. 19.]

The Department's rules were enforced on the ground. In Chitrari, where _"intensive grazing for generations led to erosion"_, passes were issued to check it, and those who broke the rules faced the penalty _"either by cash penalty or forfeiture of the animal"_. Beside the fee series, Newell marks one year as _"the year after the sheep were struck by disease"_. By 1961, a shepherd had to pay the grazing tax twice a year.#h(0pt, weak: true)#footnote[Penalties in Chitrari: #cite(<chitrari1961>, style: "short-title.csl"), PDF p. 23. Sheep disease: #cite(<newell1961>, style: "short-title.csl"), PDF p. 38. Tax twice a year: #cite(<brahmaur1961>, style: "short-title.csl"), PDF p. 55.]

On the Sutlej, before the India-China dispute, Shipki La _"was open to all traders without passport"_. But after the dispute began, the Gartok trade practically came to an end.#h(0pt, weak: true)#footnote[#cite(<kanum1961>, style: "short-title.csl"), PDF pp. 16, 51.]

= Interpretation <sec-interp>

== Limits of the Braudelian Framework <sec-limits>

In our case, the months of the moves and the height of the pastures belong to the longue durée. In the 1881 census the flocks spent the same half-year in the low hills, and in the records of 1891, 1911 and 1961 the months are the same. The Raja's grazing fee, the Forest Department's permits, the Tibet trade and the roads belong to the time of conjunctures. The lease attempt of 1874, the merger of 1948, the sheep disease of the late 1950s and the India-China dispute belong to the time of events. The Brahmaur surveyor puts these levels together when he writes that the yearly migration _"is on the decline"_, that with the opening of roads _"new avenues of earning livelihood are available to them"_, and that this is _"likely to change the cycle of their life followed since ages"_.#h(0pt, weak: true)#footnote[#cite(<brahmaur1961>, style: "short-title.csl"), PDF p. 87.]

With Braudel's levels, we can explain why the herding cycle lasted. We cannot explain why villages with the same height and ruler lived so differently, and for that we need the Marxist lens, to find out who owned the means of production and what formed the material basis.

== Material Basis <sec-material>

Large flocks needed high pastures, but who kept the flocks depended on other things. Chaupal stands at _"7,685 feet"_, as high as the herding villages of the Ravi (Section 3.2), yet its _"Sheep and goats are not taken to grazing pastures outside Chaupal"_. In Chitrari only those _"who have a sizeable flock to tend"_ migrate, and they are barely 15 per cent of the village. Brahmaur, Devi-Kothi and Maingal lie on the Ravi under the same Raja of Chamba, between about 2,130 and 2,290 m, so with Bloch's comparative method we can compare them while height and ruler stay nearly the same.#h(0pt, weak: true)#footnote[Chaupal's height: #cite(<chaupal1961>, style: "short-title.csl"), PDF p. 12. Chaupal's flocks: #cite(<chaupal1961>, style: "short-title.csl"), PDF p. 49. Chitrari: #cite(<chitrari1961>, style: "short-title.csl"), PDF p. 23.]

In Brahmaur, 40 Brahmin and Rajput households owned almost all the sheep and goats (Section 4.2). They herded them as malundis and hired a pohal _"to look after the flock on wages"_ only when they had to. Their grain is _"not sufficient to go far. This is why they have to migrate for the winter months"_. The flock was the main means of production, so the family went with it. In Devi-Kothi, farmers _"may also send their sheep and goats with professional graziers to high hills"_, paying a fee per animal, and the grazier _"has no responsibility if the animal is killed"_. Here the owner and the herder were different people tied by cash, and the risk stayed with the owner. _"The Gaddis of Maingal are different from the Gaddis of Brahmaur. They do not lead a pastoral life but have settled on agriculture as their principal occupation"_, and the reason lies in land, since their three Gaddi Brahmin households _"own the largest holdings"_ in the village.#h(0pt, weak: true)#footnote[Pohals: #cite(<brahmaur1961>, style: "short-title.csl"), PDF p. 55. Brahmaur's grain: #cite(<brahmaur1961>, style: "short-title.csl"), PDF p. 45. Graziers in Devi-Kothi: #cite(<devikothi1961>, style: "short-title.csl"), PDF p. 48. Gaddis of Maingal: #cite(<maingal1961>, style: "short-title.csl"), PDF p. 52. Maingal's holdings: #cite(<maingal1961>, style: "short-title.csl"), PDF p. 47.]

In Marxist terms, the means of production here were land, flocks and pastures, and the relations of production were the ways these were held and worked: the malundi on his own flock, the pohal on wages, the grazier paid by the head, and the household with no animals at all. Brahmaur's fields could not feed its households, so the flock was their material basis. Maingal's Gaddis held the most land, so farming was theirs. The three villages had nearly the same height and the same ruler. What differed was which means of production a household controlled, and on that depended whether it migrated.

== Grazing Taxes and Permit Limits <sec-conjunctures>

Under the princely state the Raja owned the pastures and the herders used them. The Raja took a share of the herders' product through a grazing fee, and he auctioned the right to collect it to the highest bidder, _"who was usually a Gaddi"_. Because he both owned the land and ruled the state, this fee was rent and tax at the same time. The contradiction of this conjuncture was between his ownership and the herders' customary use, and its limit was set by custom. In 1874 an attempt to lease the grazing grounds of Pangi _"provoked much opposition"_ and was abandoned.#h(0pt, weak: true)#footnote[Fee contractor: #cite(<newell1961>, style: "short-title.csl"), PDF p. 18. Lease of 1874: #cite(<kupha1961>, style: "short-title.csl"), PDF p. 113.]

== The 1948 Merger and Its Impacts <sec-merger>

After the merger, the pastures had a new owner. The grazing tax was _"taken over by the Government of India State Forest Department"_, and a forest officer took the place of the fee contractor. Under the Raja anyone who paid the fee could graze on a high pasture (dhar). Under the Department a shepherd could graze only the number of animals on his permit, and the forest officer fixed how many each dhar could hold. In Brahmaur, sheep and wool were the _"main profession in terms of money return"_, but the Department did _"not now grant any additional permit for more sheep and goats"_. A family could no longer raise its income by raising its flock.#h(0pt, weak: true)#footnote[Takeover by the Department: #cite(<newell1961>, style: "short-title.csl"), PDF p. 19. Permit limits: #cite(<newell1961>, style: "short-title.csl"), PDF p. 37. No new permits: #cite(<brahmaur1961>, style: "short-title.csl"), PDF p. 46.]

After the merger there was also a new contradiction, between the state's conservation of the pastures and the herders' need to live from them. Where pastures were closed for soil conservation in Pangi, this _"has given rise to a sense of resentment against the Forest Department in this area"_. The herders resolved the tension by turning the permits into property. Because their number was capped, they gained value, and Newell writes that they were _"freely bought and sold amongst shepherds so that shepherds have now become closed corporations"_. Once the number of permits was capped, the permit became something owned and traded, where before it had been a licence to graze.#h(0pt, weak: true)#footnote[Resentment in Pangi: #cite(<kupha1961>, style: "short-title.csl"), PDF p. 136. Sale of permits: #cite(<newell1961>, style: "short-title.csl"), PDF p. 37.]

== Monetised Labour and Credit <sec-labour>

With the roads of the 1950s came a contradiction over labour. A pohal in Brahmaur was paid mostly in kind, with meals, clothes, wool, a few sheep and two rupees a month, while a road labourer earned _"a daily wage of about Rs. 2/-"_. In cash, the road paid in a day what the flock paid in a month, and in Kanum labourers _"prefer to work on the roads rather than work as 'fawals'"_ because _"they get better wages"_. Flock owners now had to compete with road work for shepherds. Lenders took a share of the surplus even from those who owned their animals. The Gujjars of Maingal owned their buffaloes, but _"Gujjar households are cent per cent under debt"_, and those in debt _"are obliged to sell their produce to them in lieu of the interest as well as the principal amount"_.#h(0pt, weak: true)#footnote[Pohal's pay: #cite(<brahmaur1961>, style: "short-title.csl"), PDF p. 55. Road wage: #cite(<brahmaur1961>, style: "short-title.csl"), PDF p. 45. Fawals in Kanum: #cite(<kanum1961>, style: "short-title.csl"), PDF p. 51. Gujjar debt: #cite(<maingal1961>, style: "short-title.csl"), PDF p. 42. Sale of produce to lenders: #cite(<maingal1961>, style: "short-title.csl"), PDF p. 61.]

== Ravi and Sutlej <sec-ravi-sutlej>

The Ravi and the upper Sutlej share mountain and season but differ in two ways. On the Ravi, where _"all grazing rights belonged to the rajah"_, the Department's permits replaced the Raja's fee and became a market. In Kanum the pasture was _"a common pasture land of the villagers"_, and the change came as a fenced area closed for soil conservation. The form of property after 1948 depended on the form before it. The valleys also differed in the direction of their trade. The India-China dispute closed the Shipki La pass and ended Kanum's trade with Tibet, in which 10 or 12 of its 113 families had taken part. Brahmaur's herders sold their blankets in the low hills, so their market did not depend on the pass. Braudel calls an event _"an explosion"_, but where the explosion was felt depended on the structure of each valley.#h(0pt, weak: true)#footnote[Raja's rights: #cite(<newell1961>, style: "short-title.csl"), PDF p. 18. Kanum's common pasture: #cite(<kanum1961>, style: "short-title.csl"), PDF p. 133. Fenced area: #cite(<kanum1961>, style: "short-title.csl"), PDF p. 132. Shipki La and Kanum's trade: #cite(<kanum1961>, style: "short-title.csl"), PDF pp. 51, 131. Brahmaur's market: #cite(<brahmaur1961>, style: "short-title.csl"), PDF p. 59. Braudel: #cite(<braudel-longue-duree>, style: "short-title.csl"), PDF p. 5.]

== Representation in the Sources <sec-representation>

Our sources speak through surveyors, settlement officers and headmen. The Lambardar of Nachar _"has about 1,100 strong flock"_, so the man who speaks for the village is also one of its richest shepherds. In Brahmaur, the Sipis held 93 of 4,484 animals and the one Rehara household held none, and like the pohals, fawals and indebted Gujjars, they never speak for themselves in our sources. As Braudel writes, _"There are others who matter but who are silent"_.#h(0pt, weak: true)#footnote[Nachar's headman: #cite(<nachar1961>, style: "short-title.csl"), PDF p. 33. Brahmaur's livestock table: #cite(<brahmaur1961>, style: "short-title.csl"), PDF p. 54. Braudel: #cite(<braudel-longue-duree>, style: "short-title.csl"), PDF p. 18.]



= Conclusion <sec-conclusion>

Our research question asked how the seasonal movement of flocks shaped life in the Himachal hills between 1881 and 1961, and who controlled and profited from it. With the Annales approach, specifically Braudel's levels of time and Bloch's comparative method, we showed that the yearly cycle of herding stayed the same across eighty years, since it was set by the mountains and the seasons: the months and routes recorded in 1891, 1911 and 1961 are the same, and large flocks were kept only in the high villages. Yet villages sharing nearly the same geography still lived very differently. With the Marxist approach, we explained why those differences existed. Whether a family migrated depended on who owned the flocks and the land, and who profited depended on who controlled access to the pastures. In 1961 the flocks were held mostly by the landholding castes, while the right over the herders' product passed from the Raja and his fee contractor to the Forest Department, and by 1961 the moneylender and the shopkeeper also took their share. By 1961 the migration was based on fixed dhars, under capped permits that were bought and sold. Fewer animals paid grazing fees in Brahmaur tahsil than a decade earlier, and hired shepherds were leaving for road work in Kinnaur. With new roads and credit, both labour and surplus moved into a cash economy. Those who held permits, and the state that issued them, benefited from this arrangement, whereas shepherds without permits, castes with few animals and indebted Gujjars bore the costs.

With Braudel's framework, we could see what stayed the same and how quickly each layer of history changed, but we could not explain why the profits shifted from one group to another. With Marx's categories, we could explain why those gains shifted, but we needed Braudel's levels of time to show how a slow seasonal cycle carried a fast-changing system of property and claims. Taken together, we use the levels of time to see where to look, and the material basis to see why things changed.

Our evidence has limits. We focused on the 1961 surveys, and almost all the claims in the knowledge graph come from them. A count of claims shows how often the sources mention a relation (e.g. a moneylender taking interest), not how large it was (e.g. not how much money or produce was involved). The villages were chosen by the Census, the livestock and fee figures were read from page images, and no source dates the closing of Shipki La.

#pagebreak()
#bibliography("references.yaml")
