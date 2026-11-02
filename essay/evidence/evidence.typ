#set document(title: "Seasonal Herding in the Himachal Hills, 1881-1961: Evidence")
#set page(paper: "a4", numbering: "1")
#set text(font: "C059", size: 10.5pt, lang: "en")
#set par(justify: true)
#set heading(numbering: none)
#show heading: set text(weight: "bold")
#show heading.where(level: 2): set block(above: 1.6em, below: 0.9em)
#show heading.where(level: 3): set block(above: 1.3em, below: 0.7em)
#show link: set text(fill: rgb("#0064E0"))
#show raw: set text(font: "Nimbus Mono PS", size: 9pt)
#show figure.caption: set text(size: 9pt)
#set table(stroke: none, inset: (x: 4pt, y: 3pt))
#show table: set text(size: 8pt)
#show table: set par(justify: false)

#let snip(body) = block(width: 100%, fill: luma(245), inset: (left: 9pt, rest: 6pt),
  stroke: (left: 1.5pt + luma(150)), above: 0.6em, below: 0.6em, text(size: 9.5pt, body))

#let datatable(cols, header, ..cells) = block(above: 0.5em, below: 1em, table(
  columns: cols,
  table.hline(stroke: 0.6pt),
  ..header.map(h => text(weight: "bold", h)),
  table.hline(stroke: 0.4pt),
  ..cells,
  table.hline(stroke: 0.6pt),
))

#text(size: 17pt, weight: "bold")[Seasonal Herding in the Himachal Hills, 1881-1961: Evidence]

3 November 2026
#v(0.6em)

This file collects the evidence for each finding of the essay outline. Each finding has the source snippets that support it, the tables, charts and maps that hold its numbers, and an interpretation through Braudel's levels of historical time and through Marx's analysis of production.

The file follows these conventions.

- A citation such as (Brahmaur survey, PDF p. 55) consists of the source and the PDF page, which is the page counter of a PDF viewer. The page is in `essay/reading_pack.pdf` or in the original PDF.

- Every snippet is quoted from the OCR text of its page and was checked against that text by `scripts/build_evidence.py`. The check results are in `analysis/evidence/snippet_check.csv`. Spelling inside a snippet is that of the source.

- Numbers appear only in tables, charts, maps and snippets. Every table is computed by `scripts/build_evidence.py` from a file in `analysis/` or `data/`.

- Figures marked as read from page images were typed by Claude from the image of the page. No person has checked them, and the `checked_by` column is empty in `data/flocks.csv` and `data/fee_flocks.csv`.

- The maps are pages of the sources themselves: the 1931 census, the 1961 Punjab Census Atlas, the 1961 district handbooks and the 1961 village surveys. No source in the corpus maps the migration routes, the passes or the summer pastures, and the 1881 census volume has no maps.

- Readings from the course are cited by author, title and PDF page. The full references are in the section on readings at the end.

= Lenses

Braudel divides historical time into levels that move at different speeds. The longue durée is the slow time of geography and of structures, such as altitude, snow, routes and the herding calendar. The conjuncture is the medium time of economic and social cycles, measured by series such as prices, wages and fees. The event is the short time of single occurrences, such as a merger of states or the closing of a pass. The three levels are read together in Section 7.

#snip["The longue durée, cyclical phases (conjoncture), and events fit together easily, for they all are measurements on the same scale." (Braudel, "History and the Social Sciences", PDF p. 29.)]

#snip["For us historians, a structure is certainly an assemblage, an architecture, but even more it is a reality that time can only slowly erode, one that goes on for a long time." (Braudel, "History and the Social Sciences", PDF p. 9.)]

#snip["Let us call it the 'recitative' of the cyclical phase (conjoncture), the cycle, even the 'intercycle,' which offered us time lengths of a dozen years." (Braudel, "History and the Social Sciences", PDF p. 7.)]

#snip["An event is an explosion, something that has 'the sound of newness'." (Braudel, "History and the Social Sciences", PDF p. 5.)]

Bloch's comparative method compares societies that share conditions and differ in one respect, and his criticism of witnesses separates independent testimony from copies.

#snip["At the bottom of nearly all criticism there is a problem of comparison." (Bloch, #emph[The Historian's Craft], PDF p. 32.)]

#snip["should two witnesses describe the battle in exactly the same language or, despite a certain variation of phrasing, with exactly the same details, we should unhesitatingly conclude that one of them had copied the other or that both had copied a common model." (Bloch, #emph[The Historian's Craft], PDF p. 36.)]

The Marxist reading identifies the material basis of the society, which is the means of production and the relations of production. It asks who owned the means of production, who worked, and how a share of the product was taken. It then identifies the contradiction that ended each arrangement and the arrangement that followed.

#snip["Identify the 'Material Basis' of social formation" (Alam, "Marxist History" lecture slides, PDF p. 10.)]

#snip["Identify the 'Dialectical Contradictions' in social formation" (Alam, "Marxist History" lecture slides, PDF p. 10.)]

#snip["Means of Production and Relations of Production" (Alam, "Marxist History" lecture slides, PDF p. 15.)]

#snip["Extraction of Value Created by Labour" (Alam, "Marxist History" lecture slides, PDF p. 13.)]

= 1. Introduction

== 1.1. The Same Migration in 1881 and 1961

- In the 1881 census, the Gaddi year is described as half the year in Kangra and half across the range in Chamba. In the 1961 Brahmaur survey, the same movement is described in nearly the same terms.

- In both descriptions, the winter grounds are in Kangra, and the flocks move south over the Dhauladhar in winter and north in summer.

#snip["consists of flocks of sheep and goats, which they feed half the year (the winter months) in the valleys of Kangra, and for the other half drive across the range into the territories of Chamba" (1881 census, PDF p. 275.)]

#snip["in the beginning of the winter (October and November), the flocks are driven to the low hills of Kangra, Nurpur, Pathankot and Jammu" (Brahmaur survey, PDF p. 55.)]

- Braudel, at the level of the longue durée. The two descriptions bracket a period in which the movement of the flocks did not change. The cycle belongs to the slow time of mountain and season, which Braudel places beneath the faster time of economies and of events.

  #snip["The longue durée, cyclical phases (conjoncture), and events fit together easily, for they all are measurements on the same scale." (Braudel, "History and the Social Sciences", PDF p. 29.)]

- Marx, at the level of the mode of production. Both descriptions are of the same labour process, the moving of flocks between pastures. Neither description states who owned the flocks and the pastures or who took a share of the product. Those questions are covered in Sections 5 and 6.

  #snip["Identify the 'Material Basis' of social formation" (Alam, "Marxist History" lecture slides, PDF p. 10.)]

  #snip["Identify the 'Dialectical Contradictions' in social formation" (Alam, "Marxist History" lecture slides, PDF p. 10.)]

== 1.2. One Cycle Under Changing Rulers

- In the 1881 census and the 1931 census, a winter descent from the hills is recorded without months. In Rose (1911) and the 1961 surveys, the months are named, and they are the same in both (Table 3.2).

- Between these sources the hill states passed from princely rule to the new state of Himachal Pradesh, as recorded in the Kothi survey.

#snip["the yearly exodus to Kangra takes place in October and November, and the return journey in April and May" (Rose, vol. 2, PDF p. 297.)]

#snip["the hillmen of the lofty ranges leave their homes with their sheep and cattle to spend the winter in the valleys and plains of the neighbouring districts" (1931 census, PDF p. 142.)]

#snip["Before the formation of Himachal Pradesh on the 15th April 1948, Kinnaur formed a part of the erstwhile State of Rampur Bushahr." (Kothi survey, PDF p. 16.)]

- Braudel, at the level of the event against the structure. The merger of the hill states is an event. The migration calendar is a structure that the event did not alter.

  #snip["An event is an explosion, something that has 'the sound of newness'." (Braudel, "History and the Social Sciences", PDF p. 5.)]

- Marx, at the level of the superstructure. A change of state is a change in the political form above production. The flocks, the pastures and the labour of herding continued, and the change appears in the forms through which a share of the product was taken.

  #snip["The inhabitants gave themselves no trouble about the breaking up and divisions of kingdoms; while the village remains entire, they care not to what power it is transferred, or to what sovereign it devolves; its internal economy remains unchanged." (Marx, "The British Rule in India", PDF p. 3.)]

== 1.3. Changes in the Share of the Product

- Newell records that the raja of Chamba held all grazing rights before 1948 and that the Forest Department took over the grazing tax afterwards.

- According to the Maingal survey, every Gujjar household was in debt to moneylenders in Chamba.

#snip["In Chamba all grazing rights belonged to the rajah of Chamba" (Newell, PDF p. 18.)]

#snip["these rights to grazing tax have now been taken over by the Government of India State Forest Department" (Newell, PDF p. 19.)]

#snip["Gujjar households are cent per cent under debt" (Maingal survey, PDF p. 42.)]

- Braudel, at the level of the conjuncture. Each arrangement of rights, fees and credit lasted for decades and then gave way to another. These are conjunctures, the medium-term movements that Braudel places between structure and event.

  #snip["Let us call it the 'recitative' of the cyclical phase (conjoncture), the cycle, even the 'intercycle,' which offered us time lengths of a dozen years." (Braudel, "History and the Social Sciences", PDF p. 7.)]

- Marx, at the level of surplus appropriation. The raja's fee, the Department's fee and the moneylender's interest are forms in which a share of the herders' product was taken. The first two are claims of the state on the product, which Marx counts as the state's department of finance, and which Habib separates from rent. The third is the gain of usurer's capital.

  #snip["There have been in Asia, generally, from immemorial times, but three departments of Government; that of Finance, or the plunder of the interior; that of War, or the plunder of the exterior; and, finally, the department of Public Works." (Marx, "The British Rule in India", PDF p. 2.)]

  #snip["Mal, which we render as land revenue, was not, formally speaking, rent from the land, but a tax on the crop." (Habib, "Potentialities of Capitalistic Development", PDF p. 8.)]

  #snip["The beneficiaries were not only zamindars (especially chaudhuris) and headmen, who thus added to their customary exactions, not only professional usurers, who thereby augmented their usurious capital, but also merchants (who often gave advances to the peasants to establish claims on their produce)" (Habib, "Potentialities of Capitalistic Development", PDF p. 14.)]

= 2. Sources and Method

The method runs from the scanned volumes to the evidence graph and then to the tables, charts and maps of this file. Each step is a script in `scripts/` and an entry in `computational-analysis.md`.

+ Every page of every volume was scored by the frequency of herding words, such as flock, shepherd, pasture, migration, permit and debt. The pages with the highest scores were selected, and in the colonial volumes only pages on which the hill districts are also named were kept (entries A2, A3, A13).

+ A language model read each selected page and proposed claims. A claim is one statement from one page, with a subject, a relation from a fixed list, an object, any quantity, months and place, and a verbatim quotation (entries A4, A5).

+ A script kept a claim only if its quotation is found on the cited page, word for word or with small OCR differences, and with every number of the quotation present on the page (entry A6).

+ The livestock tables of the village surveys have scrambled OCR, so their figures were read from page images and entered as claims. A few claims were entered by hand (entries A4, A9).

+ Names were resolved to one entity each, so that spellings such as Bharmour and Brahmaur meet at one node (entry A11).

+ A second model pass judged each claim against its page. Claims judged not supported were left out of every analysis (entry A12).

+ The claims form the evidence graph. Each table and chart of this file is a query on the graph or on the image-read tables (entries A7 to A18).

+ A text-reuse search compared every page with every page of the earlier sources, so that a passage copied from one source into another counts as one witness (entry A19).

Table 2.1. Counts at each step of the method.

#datatable((auto, auto, auto,), ([Step], [Quantity], [Count],), [1], [Pages of the 1961 volumes scored by herding vocabulary], [3754], [1], [Pages of the 1961 volumes selected], [428], [1], [Pages of the 1881, Rose and 1931 volumes scored], [2939], [1], [Pages of the 1881, Rose and 1931 volumes selected], [82], [2], [Claims proposed by the language model], [1843], [3], [Claims rejected because the quotation is not on the cited page], [44], [4], [Claims entered from livestock tables read from page images], [174], [4], [Claims entered by hand], [38], [5], [Claims kept in the evidence graph], [1964], [6], [Second model check: supported], [1135], [6], [Second model check: partly supported], [545], [6], [Second model check: not supported (left out of every analysis)], [108], [6], [Second model check: unclear], [1], [7], [Nodes in the graph used for the analyses], [854], [7], [Edges in the graph used for the analyses], [1856], [8], [Copied passages of twelve or more words between sources], [4698])

Table 2.2. Source pairs with the most copied text.

#datatable((auto, auto, auto, auto,), ([Later source], [Earlier source], [Copied passages], [Copied words],), [1961 Census, Special Tables on SC and ST, Himachal Pradesh], [Rose], [1273], [27617], [Rose Vol3], [1881], [836], [17996], [Rose], [1881], [770], [15739], [Rose Vol1], [1881], [389], [11823], [1961 Census, Special Tables on SC and ST, Himachal Pradesh], [Rose Vol3], [355], [7990], [1961 Census, Special Tables on SC and ST, Himachal Pradesh], [1881], [372], [7963], [Chaupal], [Rose Vol1], [74], [1649], [Newell], [Rose], [85], [1618])

- Bloch, at the level of method. Bloch's criticism of witnesses is applied to the census corpus by the text-reuse search. A later source that copies an earlier one adds no testimony.

  #snip["should two witnesses describe the battle in exactly the same language or, despite a certain variation of phrasing, with exactly the same details, we should unhesitatingly conclude that one of them had copied the other or that both had copied a common model." (Bloch, #emph[The Historian's Craft], PDF p. 36.)]

= 3. The Mountain Year

== 3.1. Altitude and Flock Size

- The altitude of each survey village, as stated by its own survey, and its sheep and goats per household are in Table 3.1 and Figure 3.1.

- In the Ravi, Sutlej and Chenab valleys, households in every village above a threshold of altitude keep large flocks, and households in every village below it keep few.

- In the 1881 census, cultivation is placed below a fixed height. In the 1961 surveys, the passes are under snow from late autumn to spring.

#snip["from an elevation of 3,500 or 4,000 feet up to 7,000 feet. Above this altitude there is little or no cultivation" (1881 census, PDF p. 275.)]

#snip["usually begins to fall on the passes in October and closes them by the middle of November" (Kupha survey, PDF p. 111.)]

#snip["it begins to disappear again in March and the passes re-open in May" (Kupha survey, PDF p. 111.)]

#snip["to take less than three days actually on the tops of the mountain" (Newell, PDF p. 18.)]

#snip["these tarkals are not sufficient for the upkeep of the entire sheep and goat wealth of the village and people have therefore to migrate to other pastures" (Brahmaur survey, PDF p. 55.)]

#snip["The people of Brahmaur are allowed to have timber from the Brahmni reserved forest" (Brahmaur survey, PDF p. 24.)]

#snip["The forests occupy the biggest area and are managed by State Forest Department. The villagers meet their demand of firewood, timber and grass from there." (Chitrari survey, PDF p. 38. Part of this page repeats Rose.)]

#snip["Sheep live mainly on grazing and, therefore, are numerous where either there is considerable fallowing of land or there are extensive waste lands." (Punjab Census Atlas, PDF p. 367.)]

Table 3.1. Altitude and sheep and goats per household in the survey villages. Altitudes are as stated by each survey, or from SRTM elevation where no altitude is stated in the survey. Livestock figures were read from page images.

#datatable((auto, auto, auto, auto, auto, auto, auto,), ([Village], [River system], [Altitude (m)], [Altitude from], [Households], [Sheep and goats], [Per household],), [Tandi], [Chenab], [3048], [survey], [18], [384], [21.3], [Kanum], [Sutlej], [2926], [survey], [113], [1827], [16.2], [Kothi], [Sutlej], [2515], [survey], [128], [2557], [20.0], [Chaupal], [Yamuna], [2342], [survey], [80], [126], [1.6], [Maingal], [Ravi], [2286], [survey], [31], [405], [13.1], [Devi-Kothi], [Ravi], [2164], [survey], [60], [1337], [22.3], [Brahmaur], [Ravi], [2134], [survey], [99], [4484], [45.3], [Nachar], [Sutlej], [2088], [survey], [213], [], [], [Shathla], [], [1937], [SRTM at geocoded point], [69], [], [], [Kalath], [], [1829], [survey], [8], [7], [0.9], [Chitrari], [Ravi], [1829], [survey], [80], [159], [2.0], [Chergaon], [Yamuna], [1829], [survey], [68], [143], [2.1], [Rajana], [Yamuna], [1676], [survey], [161], [559], [3.5], [Chaunri], [Yamuna], [1600], [survey], [58], [45], [0.8], [Pangna], [], [1498], [SRTM at geocoded point], [], [62], [], [Chauntra], [Beas], [1278], [SRTM at geocoded point], [53], [41], [0.8], [Kot], [Beas], [1219], [survey], [101], [207], [2.0], [Bir], [Beas], [1219], [survey], [36], [208], [5.8], [Batal], [], [1088], [SRTM at geocoded point], [140], [40], [0.3], [Nalag], [Sutlej], [982], [SRTM at geocoded point], [82], [359], [4.4], [Moginand], [], [792], [survey], [69], [160], [2.3], [Shakrori], [Sutlej], [518], [survey], [60], [76], [1.3], [Basal], [], [], [], [119], [139], [1.2], [Kupha], [Chenab], [], [], [119], [596], [5.0])

#figure(image("../../analysis/geography/altitude_flock.png", width: 100%), caption: [Figure 3.1. Sheep and goats per household against altitude.], kind: image, supplement: none, numbering: none)

#figure(image("maps/atlas_p024_physiography.png", width: 100%), caption: [Map 3.1. Punjab Physiography, Punjab Census Atlas 1961, PDF p. 24.], kind: image, supplement: none, numbering: none)

#figure(image("maps/atlas_p028_mean_annual_rainfall.png", width: 100%), caption: [Map 3.2. Punjab Mean Annual Rainfall, Punjab Census Atlas 1961, PDF p. 28.], kind: image, supplement: none, numbering: none)

#figure(image("maps/atlas_p044_vegetation_types.png", width: 100%), caption: [Map 3.3. Punjab Vegetation Types, Punjab Census Atlas 1961, PDF p. 44.], kind: image, supplement: none, numbering: none)

#figure(image("maps/brahmaur_p002_notional_map.png", width: 100%), caption: [Map 3.4. Brahmaur Notional Map, Brahmaur survey, PDF p. 2.], kind: image, supplement: none, numbering: none)

#figure(image("maps/tandi_p017_sketch_map.png", width: 100%), caption: [Map 3.5. Sketch Map of Village Tandi, Tandi survey, PDF p. 17.], kind: image, supplement: none, numbering: none)

- Braudel, at the level of the longue durée. Altitude, snow and the closing of the passes are the geographical structure of the region. The herders did not choose the months of the migration, which followed from the height of the pastures and the snow line.

  #snip["Man is a prisoner for long centuries of climates, of vegetations, of animal populations, of types of crop, of slowly constructed equilibria, which he cannot transform without the risk of endangering everything. Take the role of transhumance in mountain life." (Braudel, "History and the Social Sciences", PDF p. 10.)]

- Marx, at the level of the forces of production. The high pastures are a means of production that can be used only in summer. A household needed enough animals to use them, so the scale of herding depended on the ownership of flocks as well as on altitude.

  #snip["Means of Production and Relations of Production" (Alam, "Marxist History" lecture slides, PDF p. 15.)]

  #snip["Extraction of Value Created by Labour" (Alam, "Marxist History" lecture slides, PDF p. 13.)]

== 3.2. The Valley as a Second Condition

- Chaupal stands as high as the herding villages but on the Yamuna side, and its households keep few animals (Table 3.1).

- In the notes of the Punjab Census Atlas, the sheep of Punjab are placed in the hill districts and in the dry south, where grazing land is available.

#snip["The village is at 7,685 feet." (Chaupal survey, PDF p. 12.)]

#snip["at a height of 1,700 ft. above sea level" (Shakrori survey, PDF p. 11.)]

#snip["on a ten thousand feet high flat ground" (Tandi survey, PDF p. 18.)]

#snip["They are more numerous in the hilly Districts of Kangra, Simla and parts of Lahaul & Spiti" (Punjab Census Atlas, PDF p. 367.)]

#figure(image("maps/atlas_p290_sheep_1961.png", width: 100%), caption: [Map 3.6. Distribution of Sheep 1961, Punjab Census Atlas, PDF p. 290.], kind: image, supplement: none, numbering: none)

#figure(image("maps/atlas_p291_goats_1961.png", width: 100%), caption: [Map 3.7. Distribution of Goats 1961, Punjab Census Atlas, PDF p. 291.], kind: image, supplement: none, numbering: none)

- Braudel, at the level of the longue durée and of space. Large flocks were possible only at altitude. Whether a village kept them depended on its valley, with its routes to particular winter grounds and markets. Braudel treats such regional differences inside one geographical frame as part of the structure.

  #snip["But all structures are simultaneously pillars and obstacles. As obstacles, they provide limitations (what mathematicians call envelopes) from which man and his experiences cannot liberate themselves. Think of how difficult it is to break through certain geographical frameworks." (Braudel, "History and the Social Sciences", PDF p. 9.)]

- Bloch, at the level of comparison. Chaupal and the Ravi villages share the condition of altitude and differ in valley. By comparing them, the valley is isolated as a second condition.

  #snip["At the bottom of nearly all criticism there is a problem of comparison." (Bloch, #emph[The Historian's Craft], PDF p. 32.)]

== 3.3. The Calendar and the Routes

- For the Gaddis and the Gujjars, the years of the sources in which each movement is described, and the months named in them, are in Table 3.2. Figure 3.2 shows the months by valley.

- In the 1881 census and the 1931 census, a winter descent is recorded without months. In Rose (1911) and the 1961 surveys, the months are named, and they agree. According to the text-reuse search, the 1961 descriptions and Rose's description of the Gaddi year do not copy the 1881 census.

- Each village lies in one river valley, and its flocks cross the ranges to the winter grounds of another valley. Women and whole households go with the flocks.

#snip["in the higher mountains of Pangi and Lahul; and the winters in the low hills bordering on the plains" (Rose, vol. 2, PDF p. 297.)]

#snip["as many as 61 move out in winter months" (Brahmaur survey, PDF p. 63.)]

#snip["visit Pangi with their flocks in July and remain in the valley till September" (Kupha survey, PDF p. 113.)]

#snip["the chilly months in these places till the end of April" (Kanum survey, PDF p. 85.)]

#snip["the Budhal stream which joins Ravi" (Brahmaur survey, PDF p. 11.)]

#snip["a 40 mile length of river between high mountains" (Newell, PDF p. 10.)]

#snip["the wife usually accompanies her husband" (Newell, PDF p. 36.)]

#snip["even during migration, she carries an equal load on her back and contributes equally to the family earnings" (Brahmaur survey, PDF p. 79.)]

Table 3.2. Movements of the Gaddis and Gujjars in the sources.

#datatable((auto, auto, auto, auto, auto,), ([Group], [Movement to], [Years of the sources], [Months named], [Pages],), [Gaddi], [summer pastures], [1911, 1961], [Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov], [Chitrari p. 58; Kupha p. 113; Newell p. 18; Newell p. 36; Rose p. 293; Rose p. 297], [Gaddi], [winter grounds], [1881, 1911, 1961], [Jan, Feb, Oct, Nov, Dec], [1881 p. 275; Brahmaur p. 12; Brahmaur p. 79; Brahmaur p. 87; Chitrari p. 26; Newell p. 101; Newell p. 18; Newell p. 36; Newell p. 37; Newell p. 9; Rose p. 297], [Gujjar], [summer pastures], [1881, 1911, 1961], [Apr, May], [1881 p. 267; Maingal p. 46; Maingal p. 52; Maingal p. 60; Maingal p. 9; Rose p. 346], [Gujjar], [winter grounds], [1961], [], [Maingal p. 18; Maingal p. 9])

#figure(image("../../analysis/calendar/calendar.png", width: 100%), caption: [Figure 3.2. The herding calendar from the evidence graph.], kind: image, supplement: none, numbering: none)

#figure(image("maps/atlas_p025_drainage_system.png", width: 100%), caption: [Map 3.8. Punjab Drainage System, Punjab Census Atlas 1961, PDF p. 25.], kind: image, supplement: none, numbering: none)

#figure(image("maps/devikothi_p002_hp_village_surveys_map.png", width: 100%), caption: [Map 3.9. Himachal Pradesh, Village Surveys, Devi-Kothi survey, PDF p. 2.], kind: image, supplement: none, numbering: none)

#figure(image("maps/tandi_p005_punjab_location_of_survey_villages.png", width: 100%), caption: [Map 3.10. Punjab, Location of Villages Selected for Socio-Economic Survey, Tandi survey, PDF p. 5.], kind: image, supplement: none, numbering: none)

#figure(image("maps/kupha_p002_notional_map.png", width: 100%), caption: [Map 3.11. Kupha Notional Map, Pangi survey, PDF p. 2.], kind: image, supplement: none, numbering: none)

- Braudel, at the level of the longue durée. A winter descent is recorded in every source of the period, and where months are named, they are the same. It is the clearest case of geographical time in the sources.

  #snip["For us historians, a structure is certainly an assemblage, an architecture, but even more it is a reality that time can only slowly erode, one that goes on for a long time." (Braudel, "History and the Social Sciences", PDF p. 9.)]

- Bloch, at the level of method. The persistence is attested by independent witnesses, because no copied text links the sources in which the descent is recorded.

  #snip["If, then, results attained by the use of different data are confirmed by their agreement, it is basically because agreement in the errors of the data … seems inconceivable to us." (Bloch, #emph[The Historian's Craft], PDF p. 42.)]

  #snip["we can never interpret a document except by inserting it into a chronological series or a synchronous whole." (Bloch, #emph[The Historian's Craft], PDF p. 32.)]

- Marx, at the level of the labour process. The migration is family labour. The household, including the women who carry loads on the route, is the unit that works the flock.

  #snip["Identify the 'Material Basis' of social formation" (Alam, "Marxist History" lecture slides, PDF p. 10.)]

  #snip["Identify the 'Dialectical Contradictions' in social formation" (Alam, "Marxist History" lecture slides, PDF p. 10.)]

= 4. Comparisons

== 4.1. High Herders and Low Buyers

- Brahmaur and the low villages of Bir, Batal and Shakrori are set side by side in Table 4.1.

- The low villages kept a few sheep and goats, which they bought from the Gaddis and Kinnauras who passed through in winter, and bought wool from them.

#snip["purchased from Gaddis who wander near about in winter, for 10 to 12 rupees" (Bir survey, PDF p. 43.)]

#snip["The sheep are reared for obtaining wool" (Bir survey, PDF p. 43.)]

#snip["from the Kinnauras who stay near about the village" (Batal survey, PDF p. 46.)]

#snip["bought from the Kinnauras that go by" (Shakrori survey, PDF p. 75.)]

Table 4.1. A high herding village and three low villages. Livestock figures were read from page images.

#datatable((auto, auto, auto, auto, auto,), ([Village], [Altitude (m)], [Households], [Sheep and goats], [Per household],), [Brahmaur], [2134], [99], [4484], [45.3], [Bir], [1219], [36], [208], [5.8], [Batal], [1088], [140], [40], [0.3], [Shakrori], [518], [60], [76], [1.3])

#figure(image("maps/bir_p002_notional_map.png", width: 100%), caption: [Map 4.1. Bir Notional Map, Bir survey, PDF p. 2.], kind: image, supplement: none, numbering: none)

#figure(image("maps/shakrori_p002_notional_map.png", width: 100%), caption: [Map 4.2. Notional Map of Shakrori Village, Shakrori survey, PDF p. 2.], kind: image, supplement: none, numbering: none)

- Braudel, at the level of the longue durée and of region. Each winter the herders from the high villages passed through the low villages and traded with them. The unit of the cycle is a region of high and low ground, not a single village.

  #snip["Look at the endurance of roads and trade routes, and the surprising unchangeability of the geographical boundaries of civilizations." (Braudel, "History and the Social Sciences", PDF p. 10.)]

- Marx, at the level of exchange. The low villages took part in the herding economy as buyers of animals and wool, so they obtained the product of the high pastures as commodities.

  #snip["When the land revenue was collected in cash, the revenue payer was compelled to sell his produce in order to get money to pay for it." (Habib, "Potentialities of Capitalistic Development", PDF p. 11.)]

== 4.2. Herding Families and Settled Farmers

- In Brahmaur most families herded their own flocks, and hired shepherds were rare. In Devi-Kothi the farmers paid graziers to take their animals to the high pastures. The Gaddis of Maingal had settled as farmers.

- According to the Chitrari survey, the families who migrate are those with a large flock.

#snip["a shepherd who tends his own flock" (Brahmaur survey, PDF p. 55.)]

#snip["pohals are hired in summer season by a very few people in rare cases when they cannot spare some one from amongst the family to look after the flock" (Brahmaur survey, PDF p. 55.)]

#snip["may also send their sheep and goats with professional graziers to high hills" (Devi-Kothi survey, PDF p. 48.)]

#snip["The Gaddis of Maingal are different from the Gaddis of Brahmaur. They do not lead a pastoral life but have settled on agriculture as their principal occupation" (Maingal survey, PDF p. 52.)]

#snip["the majority of Gaddis are not shepherds" (Newell, PDF p. 37.)]

#snip["The persons who take to this seasonal migration are the ones who have a sizeable flock to tend." (Chitrari survey, PDF p. 23.)]

#figure(image("maps/devikothi_p004_notional_map.png", width: 100%), caption: [Map 4.3. Devi Kothi Notional Map, Devi-Kothi survey, PDF p. 4.], kind: image, supplement: none, numbering: none)

#figure(image("maps/maingal_p002_notional_map.png", width: 100%), caption: [Map 4.4. Maingal Notional Map, Maingal survey, PDF p. 2.], kind: image, supplement: none, numbering: none)

#figure(image("maps/chitrari_p002_notional_map.png", width: 100%), caption: [Map 4.5. Chitrari Notional Map, Chitrari survey, PDF p. 2.], kind: image, supplement: none, numbering: none)

- Bloch, at the level of comparison. The three villages lie in the same valley under the same ruler and differ in how the herding was organised. By comparing them, geography is ruled out as the explanation of the difference.

  #snip["At the bottom of nearly all criticism there is a problem of comparison." (Bloch, #emph[The Historian's Craft], PDF p. 32.)]

- Marx, at the level of the relations of production. The same means of production, the high pastures, were worked under different relations. The Brahmaur owner worked his own flock with his family. The Devi-Kothi farmer paid a grazier, which is a wage relation. The size of the flock a family owned determined which relation applied.

  #snip["Means of Production and Relations of Production" (Alam, "Marxist History" lecture slides, PDF p. 15.)]

  #snip["Extraction of Value Created by Labour" (Alam, "Marxist History" lecture slides, PDF p. 13.)]

== 4.3. Two Valleys, the Ravi and the Sutlej

- The frequency of trade words in the surveys of each valley is in Table 4.2.

- The Ravi herders sold their woollens in the low hills of Kangra in winter. The Sutlej herders carried goods down to the Lavi fair at Rampur and traded with Tibet in summer.

- The ruler of Bushahr held the Sutlej villages as Primary Owner, and every villager of Kanum could use the pastures. In Chamba the raja held all grazing rights.

- After the India-China dispute the trade with Tibet nearly ended, and the weavers and wool buyers of the lower hills were short of wool.

#snip["command a ready market in the low hills where people sell them during their stay there in winter months" (Brahmaur survey, PDF p. 59.)]

#snip["alongwith their flocks laden with chilgozas, wool, woollen patties, nuts, pasham, jira and other local herbs" (Kanum survey, PDF p. 16.)]

#snip["they brought wool, pasham, butter, ghee, goat, sheep and salt" (Kanum survey, PDF p. 131.)]

#snip["Lavi the biggest trade fair in Himachal is held there in the second week of November every year which attracts thousands of people and traders from far off places" (Mahasu handbook, PDF p. 56.)]

#snip["began in July and he was back in Kanum usually by November" (Kanum survey, PDF p. 132.)]

#snip["prior to the India-China dispute Shipki-La Pass was open to all traders without passport" (Kanum survey, PDF p. 51.)]

#snip["this trade has now practically come to an end" (Kanum survey, PDF p. 16.)]

#snip["the Pradesh had however a great set back after the trade with Tibet stopped. An acute shortage of wool and Pasham is being experienced" (Weaving survey, PDF p. 16.)]

#snip["used to go to Rampur to purchase wool during Lavi fair. But now-a-days, they prefer to buy wool from Dodra Kawar illaqa" (Chergaon survey, PDF p. 61.)]

Table 4.2. Trade, flock and debt words per 10,000 words of each survey.

#datatable((auto, auto, auto, auto, auto,), ([Village survey], [River system], [Trade words per 10,000], [Flock words per 10,000], [Debt words per 10,000],), [Kanum], [Sutlej], [33.6], [17.81], [8.03], [Kothi], [Sutlej], [14.33], [17.82], [10.1], [Nachar], [Sutlej], [13.0], [16.02], [10.45], [Devi-Kothi], [Ravi], [9.17], [14.74], [6.88], [Chitrari], [Ravi], [8.43], [20.16], [5.96], [Brahmaur], [Ravi], [8.29], [27.09], [4.67], [Kupha], [Chenab], [8.29], [15.36], [9.83], [Maingal], [Ravi], [6.62], [20.53], [17.55])

#figure(image("maps/mahasu_p005_mahasu_district_rivers.png", width: 100%), caption: [Map 4.6. Notional Map, Himachal Pradesh, Mahasu District 1961, Mahasu handbook, PDF p. 5.], kind: image, supplement: none, numbering: none)

#figure(image("maps/mahasu_p004_mahasu_fairs_and_festivals.png", width: 100%), caption: [Map 4.7. Notional Map, Mahasu District, Fairs and Festivals, Mahasu handbook, PDF p. 4.], kind: image, supplement: none, numbering: none)

#figure(image("maps/kanum_p002_notional_map.png", width: 100%), caption: [Map 4.8. Kanum Notional Map, Kanum survey, PDF p. 2.], kind: image, supplement: none, numbering: none)

#figure(image("maps/kothi_p013_notional_map.png", width: 100%), caption: [Map 4.9. Notional Map of Kothi Village, Kothi survey, PDF p. 13.], kind: image, supplement: none, numbering: none)

#figure(image("maps/nachar_p008_notional_map.png", width: 100%), caption: [Map 4.10. Nachar Notional Map, Nachar survey, PDF p. 8.], kind: image, supplement: none, numbering: none)

- Bloch, at the level of comparison. The two valleys share the mountain year and differ in the direction of their rivers and in their rulers. By comparing them, each difference can be traced to one of these conditions.

  #snip["At the bottom of nearly all criticism there is a problem of comparison." (Bloch, #emph[The Historian's Craft], PDF p. 32.)]

- Braudel, at the levels of structure and event. The direction of each river is a structure, and the direction of trade followed it. The closing of Shipki La is an event, and its effects were confined to the valley whose trade ran to Tibet.

  #snip["An event is an explosion, something that has 'the sound of newness'." (Braudel, "History and the Social Sciences", PDF p. 5.)]

- Marx, at the level of merchant capital. On the Sutlej the herders were also traders, and the flocks carried goods between Tibet and the lower hills. With the end of the trade, the Sutlej herders lost a source of income that the Ravi herders never had.

  #snip["For the long-distance carrying trade, there had developed the famous nomadic class of banjaras." (Habib, "Potentialities of Capitalistic Development", PDF p. 41.)]

= 5. Owners, Workers and Debtors

== 5.1. Ownership of the Flocks

- The sheep and goats of every survey caste table, grouped by caste class, are in Table 5.1. The share of the landholding castes in each village is in Table 5.2, and the Brahmaur table is in Table 5.3. Figure 5.1 shows the shares by village.

- In Nachar the Lambardar, the village headman, owned the largest flock.

#snip["The number of goats and sheep reared by the villagers is 4484, and the following table shows the ownership community-wise" (Brahmaur survey, PDF p. 54.)]

#snip["on an average, 100 to 200 sheep and goats are kept by a family" (Nachar survey, PDF p. 33.)]

#snip["the Lambardar of the village has about 1,100 strong flock" (Nachar survey, PDF p. 33.)]

Table 5.1. Sheep and goats by caste class across all caste tables. Figures were read from page images.

#datatable((auto, auto, auto,), ([Caste class], [Sheep and goats], [Share (%)],), [landholding], [10902], [89.3], [scheduled caste], [992], [8.1], [herding tribe], [190], [1.6], [other], [106], [0.9], [trading], [20], [0.2], [all caste tables], [12210], [100.0])

Table 5.2. Sheep and goats by village, with the share of the landholding castes. Figures were read from page images.

#datatable((auto, auto, auto, auto, auto, auto, auto,), ([Village], [River system], [PDF page], [Sheep and goats], [Landholding castes (%)], [Scheduled castes (%)], [Largest owning group],), [Kot], [Beas], [56], [207], [98.6], [1.4], [Rajput], [Chauntra], [Beas], [46], [41], [68.3], [4.9], [Rajput], [Kupha], [Chenab], [80], [596], [93.0], [4.9], [Rajput], [Tandi], [Chenab], [96], [384], [92.2], [7.8], [Bodh], [Brahmaur], [Ravi], [54], [4484], [97.9], [2.1], [Rajput], [Maingal], [Ravi], [48], [405], [54.6], [2.2], [Brahmin], [Kothi], [Sutlej], [102], [2557], [94.5], [5.5], [Rajput], [Kanum], [Sutlej], [61], [1827], [95.5], [4.5], [Kanet (Rajput)], [Nalag], [Sutlej], [31], [359], [98.6], [1.4], [Rajput], [Shakrori], [Sutlej], [76], [76], [96.1], [1.3], [Rajput], [Rajana], [Yamuna], [47], [559], [40.1], [59.9], [Koli], [Chergaon], [Yamuna], [56], [143], [90.9], [9.1], [Thakur], [Chaupal], [Yamuna], [48], [126], [31.0], [32.5], [Sunar], [Chaunri], [Yamuna], [34], [45], [8.9], [91.1], [Koli], [Moginand], [], [46], [160], [26.2], [42.5], [Koli], [Basal], [], [77], [139], [65.5], [34.5], [Rajput], [Pangna], [], [53], [62], [4.8], [67.7], [Koli], [Batal], [], [42], [40], [75.0], [20.0], [Brahmin])

Table 5.3. The Brahmaur livestock table (Brahmaur survey, PDF p. 54). Figures were read from the page image and compared with the scan by Claude.

#datatable((auto, auto, auto, auto,), ([Caste], [Households], [Households owning sheep or goats], [Sheep and goats],), [Brahman], [34], [20], [2027], [Rajput], [49], [20], [2364], [Sipi], [15], [8], [93], [Rehara], [1], [0], [0], [total], [99], [48], [4484])

#figure(image("../../analysis/flocks/ownership_shares.png", width: 100%), caption: [Figure 5.1. Share of sheep and goats by caste class in each village.], kind: image, supplement: none, numbering: none)

#figure(image("maps/census1931_p024_punjab_social_map.png", width: 100%), caption: [Map 5.1. Punjab Social Map, Census of India 1931, Punjab, Part I, PDF p. 24.], kind: image, supplement: none, numbering: none)

- Marx, at the level of the means of production. The flocks were the herders' capital, and the landholding castes owned them. Ownership of land and ownership of flocks lay with the same households.

  #snip["Means of Production and Relations of Production" (Alam, "Marxist History" lecture slides, PDF p. 15.)]

  #snip["Extraction of Value Created by Labour" (Alam, "Marxist History" lecture slides, PDF p. 13.)]

  #snip["The potail is still the head inhabitant, and still acts as the petty judge or magistrate, and collector or renter of the village." (Marx, "The British Rule in India", PDF p. 3.)]

- Braudel, at the level of the conjuncture. The caste tables were compiled once, in 1961. They are a description of the social structure at the end of the period and cannot by themselves establish a change.

  #snip["we can never interpret a document except by inserting it into a chronological series or a synchronous whole." (Bloch, #emph[The Historian's Craft], PDF p. 32.)]

== 5.2. Small Flocks of the Working Castes

- In Rajana, Pangna and Chaunri, where households kept a few goats, Koli households held most of the animals (Table 5.2).

- Across the villages, the share of the landholding castes is unrelated to altitude (entry A18).

- Marx, at the level of class. Concentration of flocks in the landholding castes belongs to the villages where herding produced a surplus for sale. Where a few goats served the household's own needs, the castes that worked the land owned them.

  #snip["Means of Production and Relations of Production" (Alam, "Marxist History" lecture slides, PDF p. 15.)]

  #snip["Extraction of Value Created by Labour" (Alam, "Marxist History" lecture slides, PDF p. 13.)]

== 5.3. Debt Among Flock Owners

- Every Gujjar household in Maingal owned buffaloes and every Gujjar household was in debt. The lenders also bought their milk products, and one shopkeeper bought their ghee below the market price.

- Gujjars owed grain debts to Gaddi Brahmins. In Kanum the landlord was the moneylender. In Chergaon tenants paid interest in labour.

- In the surveys, debt is tabulated by income group or by cause, not by caste. The debt tables are in the Maingal survey (PDF p. 42), the Kanum survey (PDF p. 55), the Devi-Kothi survey (PDF p. 53) and the Bir survey (PDF p. 35). Caste appears only in the prose.

#snip["all Gujjar households possess buffaloes" (Maingal survey, PDF p. 48.)]

#snip["Gujjars had to pay food grain debts to Gaddi brahmins" (Maingal survey, PDF p. 38.)]

#snip["borrow money at 30% annual interest" (Maingal survey, PDF p. 42.)]

#snip["to a particular shopkeeper at Chamba who pays them much less than the market price" (Maingal survey, PDF p. 60.)]

#snip["the Gujjars who are in debt are obliged to sell their produce to them in lieu of the interest as well as the principal amount" (Maingal survey, PDF p. 61.)]

#snip["being a landlord and money lender he has lent enough amount of money to the scheduled castes and others" (Kanum survey, PDF p. 53.)]

#snip["on the condition of annual charge of additional 5 seers per md., as interest" (Kanum survey, PDF p. 55.)]

#snip["instead of paying interest, the tenants-rigad are now doing agricultural labour to escape the fury of zamindars" (Chergaon survey, PDF p. 66.)]

- Marx, at the level of surplus appropriation. The Gujjars owned their means of production, yet a share of their product went to the lender as interest and to the shopkeeper as a low price. This is appropriation through usurer's capital and merchant capital, without ownership of the producer's means of production.

  #snip["The beneficiaries were not only zamindars (especially chaudhuris) and headmen, who thus added to their customary exactions, not only professional usurers, who thereby augmented their usurious capital, but also merchants (who often gave advances to the peasants to establish claims on their produce)" (Habib, "Potentialities of Capitalistic Development", PDF p. 14.)]

  #snip["than he is set upon by the other portions of the bourgeoisie, the landlord, the shopkeeper, the pawnbroker, etc." (Marx and Engels, #emph[Manifesto of the Communist Party], PDF p. 5.)]

- Marx, at the level of class. In Kanum the landlord was also the lender, and in Maingal the Gaddi Brahmins who owned flocks also held the Gujjars' grain debts.

  #snip["it was inevitable that the peasant should contract debts in order to pay the land revenue or to obtain his 'subsistence, food and cattle,'" (Habib, "Potentialities of Capitalistic Development", PDF p. 13.)]

= 6. Conjunctures and Their Contradictions

== 6.1. The Raja's Pastures and the Fee Contract

- In 1881 the Gaddis held land under two rulers, British Kangra and Chamba, and paid fines to both. Gaddis crossing into Lahul paid grazing tax to two rulers.

- In Chamba the raja owned the land and all grazing rights. He auctioned the right to collect the grazing fees, usually to a Gaddi. Near Brahmaur the ruler leased the pastures to a contractor, who allotted them to shepherds on condition that their flocks manure the fallow fields.

- In Bushahr the villagers owed the ruler a labour service called Athada Begar.

- An attempt in 1874 to lease the high pastures of Pangi was abandoned after opposition.

- The fee rates under the raja and under the Forest Department are in Table 6.1. The claims of payment in each conjuncture are counted in Table 6.4.

#snip["whenever fined by the Kangra authorities, to pay a similar penalty into the Chamba treasury" (1881 census, PDF p. 275.)]

#snip["our institutions have taught them greater independence" (1881 census, PDF p. 275.)]

#snip["would need to pay a grazing tax to both the Chamba and Lahuli ruler" (Newell, PDF p. 18.)]

#snip["could only dispose of the right to use the land" (Newell, PDF p. 16.)]

#snip["was auctioned by the rajah of Chamba to the highest bidder, who was usually a Gaddi" (Newell, PDF p. 18.)]

#snip["during the state period the Ruler of the state used to lease out the pastures near the village (Brahmani in case of Brahmaur) on contract" (Brahmaur survey, PDF p. 55.)]

#snip["The contractor further used to allot these pastures to the shepherds subject to the condition that they would keep their sheep and goats in the fallow cultivable fields at night." (Brahmaur survey, PDF p. 55.)]

#snip["including 'Athada Begar'" (Kanum survey, PDF p. 18.)]

#snip["in 1874 an attempt was made to lease the dhars or bigger grazing grounds" (Kupha survey, PDF p. 113.)]

#snip["it provoked much opposition and was finally abandoned" (Kupha survey, PDF p. 113.)]

#snip["the whole of Chamba State was nationalised, that is belonged to the nation in the person of the rajah" (Newell, PDF p. 19.)]

#snip["Land could thus not be used as security for debt" (Newell, PDF p. 19.)]

Table 6.1. Grazing fees under the raja and under the Forest Department. The units differ by row. The raja's contractor charged per head for each grazing district (Newell, PDF p. 18), and the Department charged per head for a season, twice a year in Brahmaur (Brahmaur survey, PDF p. 55). The Devi-Kothi rows were read from the image of Table XIV (Devi-Kothi survey, PDF p. 47), and the 1962 rates from the image of Newell, PDF p. 19. Newell does not state the period of the 1962 rates.

#datatable((auto, auto, auto, auto, auto, auto, auto, auto, auto,), ([Year], [Place], [Collector], [Animal], [Rate as printed], [Rupees], [Per], [Source], [PDF page],), [1950], [Chamba State (grazing districts)], [fee contractor (auction buyer of the Raja's right)], [goat], [2 annas 6 pies], [0.15625], [head per grazing district], [Newell], [18], [1950], [Chamba State (grazing districts)], [fee contractor (auction buyer of the Raja's right)], [sheep], [1 anna 6 pies], [0.09375], [head per grazing district], [Newell], [18], [1961], [Brahmaur], [Forest Department], [sheep or goat], [Rs. 15/- per hundred heads], [0.15], [head per summer season], [Brahmaur], [55], [1961], [Devi-Kothi], [Forest Department], [sheep], [Rs. 0.10], [0.1], [head per season (permits valid 1 June to 15 October)], [Devi-Kothi], [47], [1961], [Devi-Kothi], [Forest Department], [goat], [Rs. 0.25], [0.25], [head per season], [Devi-Kothi], [47], [1961], [Devi-Kothi], [Forest Department], [sheep], [Rs. 0.10], [0.1], [head per season], [Devi-Kothi], [47], [1961], [Devi-Kothi], [Forest Department], [goat], [Rs. 0.25], [0.25], [head per season], [Devi-Kothi], [47], [1961], [Devi-Kothi], [Forest Department], [buffalo], [Rs. 6.00], [6.0], [head per season], [Devi-Kothi], [47], [1961], [Devi-Kothi], [Forest Department], [buffalo], [Rs. 4.50], [4.5], [head per season], [Devi-Kothi], [47], [1962], [Lahul], [Forest Department], [goat], [4 annas], [0.25], [head (period not stated)], [Newell], [19], [1962], [Lahul], [Forest Department], [sheep], [2 annas], [0.125], [head (period not stated)], [Newell], [19], [1962], [Brahmaur], [Forest Department], [sheep or goat], [2 annas], [0.125], [head (period not stated)], [Newell], [19], [1962], [Kangra], [Forest Department], [sheep], [8 n.p.], [0.08], [head (period not stated)], [Newell], [19], [1962], [Kangra], [Forest Department], [goat], [4 annas], [0.25], [head (period not stated)], [Newell], [19])

Table 6.4. Relations of payment named in the evidence graph, counted by conjuncture.

#datatable((auto, auto, auto, auto, auto, auto,), ([Who gives to whom (kind)], [Two sovereigns], [Raja's pastures], [Forest Department], [Roads and wages], [Trade and credit],), [households -\> moneylender (interest)], [0], [0], [0], [0], [42], [households -\> cooperative society (interest)], [0], [0], [0], [0], [18], [households -\> shopkeeper (produce sold)], [0], [0], [0], [0], [10], [households -\> shopkeeper (interest)], [0], [0], [0], [0], [8], [grazier -\> Forest Department (dues, revenue or begar)], [0], [0], [8], [0], [0], [shepherd -\> Forest Department (fee or tax)], [0], [0], [8], [0], [0], [shopkeeper -\> households (produce sold)], [0], [0], [0], [0], [6], [households -\> wealthy villagers (interest)], [0], [0], [0], [0], [6], [Gaddi -\> households (produce sold)], [0], [0], [0], [0], [5], [shepherd -\> Forest Department (permit)], [0], [0], [5], [0], [0], [households -\> Raja of Chamba (dues, revenue or begar)], [0], [4], [0], [0], [0], [society members -\> Co-operative Society Menthapal (interest)], [0], [0], [0], [0], [4], [households -\> friends and relatives (interest)], [0], [0], [0], [0], [4], [Kinnaura -\> households (produce sold)], [0], [0], [0], [0], [4], [Gujjar -\> moneylender (interest)], [0], [0], [0], [0], [4])

#figure(image("../../analysis/surplus/flows.png", width: 100%), caption: [Figure 6.1. Who takes a share of whose product, by conjuncture.], kind: image, supplement: none, numbering: none)

- Braudel, at the level of the conjuncture. Under the princely grazing regime, which lasted until about 1950, the use of the pastures was organised by the raja and his contractors.

  #snip["Let us call it the 'recitative' of the cyclical phase (conjoncture), the cycle, even the 'intercycle,' which offered us time lengths of a dozen years." (Braudel, "History and the Social Sciences", PDF p. 7.)]

- Marx, at the level of the forms of surplus. The raja was both ruler and owner of the pastures, so his grazing fee was at once a tax and a payment for the use of land. The surplus was taken as a fee in cash, as labour under the Athada Begar, as wool in place of revenue (Newell, PDF p. 14), and as manure under the contract. Under the fee contract, one Gaddi stood between the raja and the other Gaddis, so the fee was collected through the herding community itself.

  #snip["Mal, which we render as land revenue, was not, formally speaking, rent from the land, but a tax on the crop." (Habib, "Potentialities of Capitalistic Development", PDF p. 8.)]

  #snip["rent in kind and rent in cash are both covered by Form A, but the latter type of rent has been regarded as of considerable significance in encouraging commodity production." (Habib, "Potentialities of Capitalistic Development", PDF p. 6.)]

- Marx, at the level of contradiction. The raja's ownership of the pastures conflicted with the herders' customary use. The lease of 1874 was abandoned after opposition, so customary use limited the ruler's claim.

  #snip["they became so many fetters. They had to be burst asunder; they were burst asunder." (Marx and Engels, #emph[Manifesto of the Communist Party], PDF p. 4.)]

- Braudel, at the level of the event. The lease attempt of 1874 is an event. After it failed, customary grazing continued as before.

  #snip["An event is an explosion, something that has 'the sound of newness'." (Braudel, "History and the Social Sciences", PDF p. 5.)]

== 6.2. Forest Department Permits

- After incorporation into Himachal Pradesh, private property in land was introduced, and a Settlement of Brahmaur tahsil began in 1953 (Newell, PDF p. 19).

- After 1948 the Forest Department took over the grazing tax. Its officers issued a receipt only to a shepherd with a permit, allotted each shepherd a fixed pasture for a fixed number of animals, and granted no additional permits.

- The Department distinguished graziers with rights from the former rulers from other graziers. In the Devi-Kothi table of charges, right holders pay less only for buffaloes, and sheep, goats and cattle pay the same (Table 6.1).

- The Department's officers issued passes to check erosion, closed some pastures for soil conservation, and punished grazing without a pass by a fine or by forfeiture of the animal.

- The sheep and goats that paid grazing fees in Brahmaur tahsil each year are in Table 6.2 and Figure 6.2, and the change by phase is in Table 6.3. Most of the decline lies in one phase, and the number did not rise again. Newell notes a sheep disease in the year of the fall and attributes the loss to the permit system.

#snip["The tax is now collected by an employee of the Forest Department and a receipt issued." (Newell, PDF p. 19.)]

#snip["This receipt is however not issued unless the shepherd has a permit issued by the Forest Department" (Newell, PDF p. 19.)]

#snip["today the power of the forest department is paramount" (Newell, PDF p. 15.)]

#snip["each shepherd has his own fixed dhar which only he can use as pasture land for his flock consisting of a fixed number of sheep and goats" (Brahmaur survey, PDF p. 55.)]

#snip["the Forest Department do not now grant any additional permit for more sheep and goats" (Brahmaur survey, PDF p. 46.)]

#snip["A distinction is made between right holder graziers and others in payment of fee and penalty." (Devi-Kothi survey, PDF p. 47.)]

#snip["given to them by the early rulers of Chamba" (Devi-Kothi survey, PDF p. 49.)]

#snip["Intensive grazing for generations led to erosion. To check this trouble passes are issued." (Chitrari survey, PDF p. 23.)]

#snip["certain pastures have also been closed in order to undertake extensive measures for soil conservation" (Kupha survey, PDF p. 136.)]

#snip["a sense of resentment against the Forest Department" (Kupha survey, PDF p. 136.)]

#snip["this is the year after the sheep were struck by disease" (Newell, PDF p. 38.)]

#snip["the number of sheep and goats was reduced by about a quarter due to the Forest Department permit system" (Newell, PDF p. 37.)]

#snip["Perhaps one of the most fundamental changes instituted by the Indian Union when it incorporated Chamba in Himachal Pradesh was to introduce the idea of private property in land" (Newell, PDF p. 19.)]

#snip["in 1953 a Settlement was instituted in Brahmaur tahsil" (Newell, PDF p. 19.)]

Table 6.2. Sheep and goats paying grazing fees in Brahmaur tahsil (Newell, PDF p. 38). Figures were read from the page image.

#datatable((auto, auto, auto, auto, auto, auto,), ([Year], [Sheep], [Goats], [Total], [Change since 1952-53 (%)], [Remark on the page],), [1952-53], [42176], [31695], [73871], [0.0], [], [1953-54], [40515], [28301], [68816], [-6.8], [], [1954-55], [41220], [30831], [72051], [-2.5], [], [1955-56], [41117], [32458], [73575], [-0.4], [], [1956-57], [40600], [30896], [71496], [-3.2], [], [1957-58], [38346], [28921], [67267], [-8.9], [], [1958-59], [35733], [25098], [60831], [-17.7], [], [1959-60], [30828], [24864], [55692], [-24.6], [This is the year after the sheep were struck by disease.], [1960-61], [30715], [24629], [55344], [-25.1], [], [1961-62], [30515], [24406], [54921], [-25.7], [])

Table 6.3. Change in fee-paying sheep and goats by phase.

#datatable((auto, auto, auto, auto, auto, auto,), ([Phase], [From], [To], [Sheep (%)], [Goats (%)], [Total (%)],), [before the fall], [1952-53], [1956-57], [-3.7], [-2.5], [-3.2], [the fall], [1956-57], [1959-60], [-24.1], [-19.5], [-22.1], [after the fall], [1959-60], [1961-62], [-1.0], [-1.8], [-1.4])

#figure(image("../../analysis/fees/fee_flocks.png", width: 100%), caption: [Figure 6.2. Sheep and goats paying grazing fees in Brahmaur tahsil.], kind: image, supplement: none, numbering: none)

- Braudel, at the level of the conjuncture. The fee series is a measured conjuncture, a medium-term movement read from a yearly series. The sheep disease is an event inside it. The series does not recover after the disease, so the disease alone cannot explain the level that follows. The Department collected the fee through its own employee, without the contractor who had stood between the raja and the herders. The unit of the charge also changed, from a fee per head for each grazing district to a fee per head for the season under a permit (Table 6.1). Aymard records a comparable removal of middlemen from the collection of a tax.

  #snip["But if one wanted to measure a price curve, a demographic progression, wage trends, variations in interest rates, the study of production (more hoped for than achieved), a close analysis of trade, it required much longer measures of time." (Braudel, "History and the Social Sciences", PDF p. 7.)]

  #snip["Economic cycles, the ebb and flow of material life, are measurable." (Braudel, "History and the Social Sciences", PDF p. 30.)]

  #snip["The short term is the most capricious, the most deceptive of time periods." (Braudel, "History and the Social Sciences", PDF p. 6.)]

  #snip["the drastic elimination of middlemen, 'partisans' and 'managers', so that it achieves a real lowering of the tax." (Aymard, "The Cost of War", PDF p. 3.)]

- Marx, at the level of rent. The state replaced the raja as landlord of the pastures and took a money rent per head. The distinction between right holders and others, which came from the former rulers, survived as a lower charge for buffaloes, so part of the old order of privilege was carried into the new one.

  #snip["Colonial Relations Can Continue Even After Political Independence" (Alam, "Marxist History" lecture slides, PDF p. 17.)]

- Marx, at the level of contradiction. Conservation of the pastures conflicted with the herders' subsistence. Under the cap on permits, the conflict was settled in favour of the existing permit holders.

  #snip["Fusion and tolerance become impossible when the crisis deepens, when there is not enough of the surplus product to go around." (Kosambi, "Social and Economic Aspects of the Bhagavad Gita", PDF p. 21.)]

== 6.3. Permits as Property, and Roads as Wages

- Newell records that shepherds bought and sold permits and had become closed corporations.

- In Kanum the landowners could not find labourers for their flocks, because men and women preferred road work at higher wages. In the Brahmaur, Kothi and Nachar surveys, villagers are recorded working as road labourers.

- The Rohtang route was made jeepable. According to the Atlas, Kangra and Lahaul and Spiti had few metalled roads in 1947 and more by 1961.

#snip["from personal knowledge I know that these permits are freely bought and sold amongst shepherds so that shepherds have now become closed corporations" (Newell, PDF p. 37.)]

#snip["found it difficult to engage labourers to attend to their sheep and goats" (Kanum survey, PDF p. 51.)]

#snip["Men and women now prefer to work on the roads rather than work as 'fawals', agricultural labourers and 'rigries' for obvious reason that they get better wages" (Kanum survey, PDF p. 51.)]

#snip["8 able-bodied persons are working there as unskilled labour at a daily wage of about Rs. 2/-" (Brahmaur survey, PDF p. 45.)]

#snip["All castes in the village avail of this opportunity and on an average 24 persons were found to be working as unskilled labourers on roads" (Kothi survey, PDF p. 79.)]

#snip["The traditional trade route to western Tibet over the Rohtang Pass which was previously only a bridle path has now been made jeepable right from Manali to Keylong" (Tandi survey, PDF p. 57.)]

#snip["Similarly the Lahaul & Spiti and Kangra Districts were generally without metalled roads." (Punjab Census Atlas, PDF p. 372.)]

#snip["In Lahaul & Spiti also the in-migration of labourers engaged in road building activity has raised the proportion of males" (Punjab Census Atlas, PDF p. 331.)]

#snip["with the opening roads, new avenues of earning livelihood are available to them, and this is likely to change the cycle of their life followed since ages" (Brahmaur survey, PDF p. 87.)]

#figure(image("maps/atlas_p308_roads_1947.png", width: 100%), caption: [Map 6.1. Metalled and Unmetalled Roads 1947, Punjab Census Atlas, PDF p. 308.], kind: image, supplement: none, numbering: none)

#figure(image("maps/atlas_p309_roads_1961.png", width: 100%), caption: [Map 6.2. Metalled and Unmetalled Roads 1961, Punjab Census Atlas, PDF p. 309.], kind: image, supplement: none, numbering: none)

- Marx, at the level of property in land. Under the raja the whole state belonged to the nation in the person of the raja, and land could not secure a debt. The Settlement of 1953 introduced private property in land, as the British settlements had done in the plains.

  #snip["The Zemindari and Ryotwar themselves, abominable as they are, involve two distinct forms of private property in land." (Marx, "The Future Results of British Rule in India", PDF p. 1.)]

- Marx, at the level of property. A state licence to graze became a commodity that established shepherds bought and sold. Newcomers could not obtain one, so the permit holders became a closed group.

  #snip["owing to monetization, the zamindari right became a fully salable commodity." (Habib, "Potentialities of Capitalistic Development", PDF p. 15.)]

  #snip["A sufficiently large change in quantity changes the nature of the thing" (Alam, "Marxist History" lecture slides, PDF p. 8.)]

- Marx, at the level of wage labour. Villagers could earn a cash wage on road work, outside the herding economy. Flock owners who depended on hired shepherds lost their labour, and families who herded their own flocks gained a second income.

  #snip["The village isolation produced the absence of roads in India, and the absence of roads perpetuated the village isolation." (Marx, "The Future Results of British Rule in India", PDF p. 2.)]

  #snip["has left remaining no other nexus between man and man than naked self-interest, than callous 'cash payment'." (Marx and Engels, #emph[Manifesto of the Communist Party], PDF p. 2.)]

- Braudel, at the level of the conjuncture. Road building from the 1950s is a conjuncture that the Brahmaur surveyor expected to change "the cycle of their life followed since ages". In 1961 the change had begun and the calendar still held.

  #snip["for even more important than the deep structures of life are its moments of rupture, its brusque or slow deterioration under the impact of contradictory pressures." (Braudel, "History and the Social Sciences", PDF p. 26.)]

= 7. Interpretation

== 7.1. The Two Lenses Together

- The persistence of the cycle is explained in the Annales reading (Section 3). The change in who took a share of its product is explained in the Marxist reading (Sections 5 and 6).

- Under Braudel's levels of time, the evidence falls into order. The calendar and the altitude threshold are the longue durée. The princely fee regime, the Forest Department regime, the Tibet trade and road building are conjunctures. The merger of 1948, the India-China dispute and the sheep disease are events.

  #snip["The longue durée, cyclical phases (conjoncture), and events fit together easily, for they all are measurements on the same scale." (Braudel, "History and the Social Sciences", PDF p. 29.)]

- Marx's analysis is applied at each conjuncture. It asks who owned the means of production, who worked, how a share of the product was taken, and what contradiction ended the arrangement.

  #snip["Identify the 'Material Basis' of social formation" (Alam, "Marxist History" lecture slides, PDF p. 10.)]

  #snip["Identify the 'Dialectical Contradictions' in social formation" (Alam, "Marxist History" lecture slides, PDF p. 10.)]

  #snip["The genius of Marx, the secret of his lasting power, is that he was the first to invent real social models, based on the historical longue durée." (Braudel, "History and the Social Sciences", PDF p. 32.)]

== 7.2. Continuity of Property Forms Across 1948

- On the Ravi the raja's revenue farm was followed by a market in Forest Department permits. On the Sutlej the common pastures became state forest.

#snip["every villager has a right of utilizing the pastures" (Kanum survey, PDF p. 133.)]

#snip["Outside this area were lands controlled by the rajah's agents (such as the Forest Department) but to which villagers had access." (Newell, PDF p. 17.)]

- Marx, at the level of the dialectic. Each new arrangement was built from the one before it. The distinction between right holders and others under the rajas survived in the Department's charges (Section 6.2).

  #snip["The Zemindari and Ryotwar themselves, abominable as they are, involve two distinct forms of private property in land." (Marx, "The Future Results of British Rule in India", PDF p. 1.)]

== 7.3. Gains and Losses by 1961

- By 1961 the migration took place on fixed pastures under tradable permits, with fewer fee-paying animals (Table 6.2) and with hired shepherds leaving for the roads (Section 6.3).

- Herders without permits, Scheduled Caste households that owned few animals (Table 5.1) and indebted Gujjars (Section 5.3) lost by the change. Permit holders and the state gained.

- Marx, at the level of class. After the change, access to the pastures depended on property. The holders of permits kept access, and those without permits lost it.

  #snip["The history of all hitherto existing society is the history of class struggles." (Marx and Engels, #emph[Manifesto of the Communist Party], PDF p. 1.)]

  #snip["Do not think only in the short term. Do not believe that only those actors who make noise are the most authentic. There are others who matter but who are silent." (Braudel, "History and the Social Sciences", PDF p. 18.)]

= 8. Limits

- A count of claims is a measure of how often the sources mention a relation, not of the size of the payment (Table 6.4).

- The village surveys cover villages chosen by the Census, not a random sample (Table 3.1).

- Copied passages are counted once (Table 2.2).

- No source in the corpus dates the closing of Shipki La. In the Kanum survey, only the "India-China dispute" is named (Kanum survey, PDF p. 51).

- The livestock tables and the fee series were read from page images and have not been checked by a person, apart from the Brahmaur table, which was compared with the scan by Claude.

- No source in the corpus maps the migration routes, the passes or the summer pastures.

= Readings

- Alam, Aniket. "Marxist History." Lectures 8 to 10, Introduction to History (HS3.201), IIIT Hyderabad, Monsoon 2026.

- Aymard, Maurice. "The Cost of War." In #emph[French Studies in History], vol. 2, #emph[Departures], 418-427.

- Bloch, Marc. #emph[The Historian's Craft]. Translated by Peter Putnam. New York: Vintage, 1953. Chapter III, "Historical Criticism."

- Braudel, Fernand. "History and the Social Sciences: The Longue Durée." Translated by Immanuel Wallerstein. #emph[Review (Fernand Braudel Center)] 32, no. 2 (2009): 171-203.

- Habib, Irfan. "Potentialities of Capitalistic Development in the Economy of Mughal India." #emph[Journal of Economic History] 29, no. 1 (1969): 32-78.

- Kosambi, D. D. "Social and Economic Aspects of the Bhagavad Gita." #emph[Journal of the Economic and Social History of the Orient] 4, no. 2 (1961): 198-224.

- Marx, Karl, and Friedrich Engels. #emph[Manifesto of the Communist Party]. Excerpt, pp. 14-21.

- Marx, Karl. "The British Rule in India." #emph[New-York Daily Tribune], June 25, 1853.

- Marx, Karl. "The Future Results of British Rule in India." #emph[New-York Daily Tribune], August 8, 1853.
