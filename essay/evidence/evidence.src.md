# Seasonal Herding in the Himachal Hills, 1881-1961: Evidence

This file collects the evidence for each finding of the essay outline. Each
finding has the source snippets that support it, the tables, charts and maps
that hold its numbers, and an interpretation through Braudel's levels of
historical time and through Marx's analysis of production.

The file follows these conventions.

- A citation such as (Brahmaur survey, PDF p. 55) consists of the source and the PDF page, which is the page counter of a PDF viewer. The page is in
  `essay/reading_pack.pdf` or in the original PDF.
- Every snippet is quoted from the OCR text of its page and was checked
  against that text by `scripts/build_evidence.py`. The check results are in
  `analysis/evidence/snippet_check.csv`. Spelling inside a snippet is that of the source.
- Numbers appear only in tables, charts, maps and snippets. Every table is
  computed by `scripts/build_evidence.py` from a file in `analysis/` or
  `data/`.
- Figures marked as read from page images were typed by Claude from the
  image of the page. No person has checked them, and the `checked_by` column
  is empty in `data/flocks.csv` and `data/fee_flocks.csv`.
- The maps are pages of the sources themselves: the 1931 census, the 1961
  Punjab Census Atlas, the 1961 district handbooks and the 1961 village
  surveys. No source in the corpus maps the migration routes, the passes or
  the summer pastures, and the 1881 census volume has no maps.
- Readings from the course are cited by author, title and PDF page. The full
  references are in the section on readings at the end.

## Lenses

Braudel divides historical time into levels that move at different speeds.
The longue durée is the slow time of geography and of structures, such as
altitude, snow, routes and the herding calendar. The conjuncture is the
medium time of economic and social cycles, measured by series such as prices,
wages and fees. The event is the short time of single occurrences, such as a
merger of states or the closing of a pass. The three levels are read together
in Section 7. {{R braudel-levels}} {{R braudel-structure}} {{R braudel-conjuncture}} {{R braudel-event}}

Bloch's comparative method compares societies that share conditions and
differ in one respect, and his criticism of witnesses separates independent
testimony from copies. {{R bloch-compare}} {{R bloch-witness}}

The Marxist reading identifies the material basis of the society, which is
the means of production and the relations of production. It asks who owned
the means of production, who worked, and how a share of the product was
taken. It then identifies the contradiction that ended each arrangement and
the arrangement that followed. {{R marx-base}} {{R marx-relations}}

## 1. Introduction

### 1.1. The Same Migration in 1881 and 1961

- In the 1881 census, the Gaddi year is described as half the year in Kangra
  and half across the range in Chamba. In the 1961 Brahmaur survey, the same
  movement is described in nearly the same terms.
- In both descriptions, the winter grounds are in Kangra, and the flocks move
  south over the Dhauladhar in winter and north in summer.

{{snippets 1.1}}

- Braudel, at the level of the longue durée. The two descriptions bracket a
  period in which the movement of the flocks did not change. The cycle
  belongs to the slow time of mountain and season, which Braudel places
  beneath the faster time of economies and of events. {{R braudel-levels}}
- Marx, at the level of the mode of production. Both descriptions are of the
  same labour process, the moving of flocks between pastures. Neither description states who owned the flocks and the pastures or who took a share of the product.
  Those questions are covered in Sections 5 and 6. {{R marx-base}}

### 1.2. One Cycle Under Changing Rulers

- In the 1881 census and the 1931 census, a winter descent from the hills is
  recorded without months. In Rose (1911) and the 1961 surveys, the months are
  named, and they are the same in both (Table 3.2).
- Between these sources the hill states passed from princely rule to the new
  state of Himachal Pradesh, as recorded in the Kothi survey.

{{snippets 1.2}}

- Braudel, at the level of the event against the structure. The merger of
  the hill states is an event. The migration calendar is a structure that the
  event did not alter. {{R braudel-event}}
- Marx, at the level of the superstructure. A change of state is a change in
  the political form above production. The flocks, the pastures and the
  labour of herding continued, and the change appears in the forms through
  which a share of the product was taken. {{R marx-village}}

### 1.3. Changes in the Share of the Product

- Newell records that the raja of Chamba held all grazing rights before 1948
  and that the Forest Department took over the grazing tax afterwards.
- According to the Maingal survey, every Gujjar household was in debt to
  moneylenders in Chamba.

{{snippets 1.3}}

- Braudel, at the level of the conjuncture. Each arrangement of rights,
  fees and credit lasted for decades and then gave way to another. These are
  conjunctures, the medium-term movements that Braudel places between
  structure and event. {{R braudel-conjuncture}}
- Marx, at the level of surplus appropriation. The raja's fee, the
  Department's fee and the moneylender's interest are forms in which a share
  of the herders' product was taken. The first two are claims of the state on
  the product, which Marx counts as the state's department of finance, and
  which Habib separates from rent. The third is the gain of usurer's capital.
  {{R marx-state}} {{R habib-revenue}} {{R habib-usury}}

## 2. Sources and Method

The method runs from the scanned volumes to the evidence graph and then to
the tables, charts and maps of this file. Each step is a script in
`scripts/` and an entry in `computational-analysis.md`.

1. Every page of every volume was scored by the frequency of herding words,
   such as flock, shepherd, pasture, migration, permit and debt. The pages
   with the highest scores were selected, and in the colonial volumes only
   pages on which the hill districts are also named were kept (entries A2, A3, A13).
2. A language model read each selected page and proposed claims. A claim is
   one statement from one page, with a subject, a relation from a fixed
   list, an object, any quantity, months and place, and a verbatim quotation
   (entries A4, A5).
3. A script kept a claim only if its quotation is found on the cited page,
   word for word or with small OCR differences, and with every number of the
   quotation present on the page (entry A6).
4. The livestock tables of the village surveys have scrambled OCR, so their
   figures were read from page images and entered as claims. A few claims
   were entered by hand (entries A4, A9).
5. Names were resolved to one entity each, so that spellings such as
   Bharmour and Brahmaur meet at one node (entry A11).
6. A second model pass judged each claim against its page. Claims judged not
   supported were left out of every analysis (entry A12).
7. The claims form the evidence graph. Each table and chart of this file is a
   query on the graph or on the image-read tables (entries A7 to A18).
8. A text-reuse search compared every page with every page of the earlier
   sources, so that a passage copied from one source into another counts as
   one witness (entry A19).

Table 2.1. Counts at each step of the method.

{{table pipeline}}

Table 2.2. Source pairs with the most copied text.

{{table reuse}}

- Bloch, at the level of method. Bloch's criticism of witnesses is applied to
  the census corpus by the text-reuse search. A later source that copies an
  earlier one adds no testimony. {{R bloch-witness}}

## 3. The Mountain Year

### 3.1. Altitude and Flock Size

- The altitude of each survey village, as stated by its own survey, and its
  sheep and goats per household are in Table 3.1 and Figure 3.1.
- In the Ravi, Sutlej and Chenab valleys, households in every village above a
  threshold of altitude keep large flocks, and households in every village
  below it keep few.
- In the 1881 census, cultivation is placed below a fixed height. In the 1961
  surveys, the passes are under snow from late autumn to spring.

{{snippets 3.1}}

Table 3.1. Altitude and sheep and goats per household in the survey
villages. Altitudes are as stated by each survey, or from SRTM elevation where no altitude is stated in the survey. Livestock figures were read from page images.

{{table altitude}}

![Figure 3.1. Sheep and goats per household against altitude.](../../analysis/geography/altitude_flock.png)

![Map 3.1. Punjab Physiography, Punjab Census Atlas 1961, PDF p. 24.](maps/atlas_p024_physiography.png)

![Map 3.2. Punjab Mean Annual Rainfall, Punjab Census Atlas 1961, PDF p. 28.](maps/atlas_p028_mean_annual_rainfall.png)

![Map 3.3. Punjab Vegetation Types, Punjab Census Atlas 1961, PDF p. 44.](maps/atlas_p044_vegetation_types.png)

![Map 3.4. Brahmaur Notional Map, Brahmaur survey, PDF p. 2.](maps/brahmaur_p002_notional_map.png)

![Map 3.5. Sketch Map of Village Tandi, Tandi survey, PDF p. 17.](maps/tandi_p017_sketch_map.png)

- Braudel, at the level of the longue durée. Altitude, snow and the closing
  of the passes are the geographical structure of the region. The herders
  did not choose the months of the migration, which followed from the height
  of the pastures and the snow line. {{R braudel-geography}}
- Marx, at the level of the forces of production. The high pastures are a
  means of production that can be used only in summer. A household needed
  enough animals to use them, so the scale of herding depended on the
  ownership of flocks as well as on altitude. {{R marx-relations}}

### 3.2. The Valley as a Second Condition

- Chaupal stands as high as the herding villages but on the Yamuna side, and
  its households keep few animals (Table 3.1).
- In the notes of the Punjab Census Atlas, the sheep of Punjab are placed in
  the hill districts and in the dry south, where grazing land is available.

{{snippets 3.2}}

![Map 3.6. Distribution of Sheep 1961, Punjab Census Atlas, PDF p. 290.](maps/atlas_p290_sheep_1961.png)

![Map 3.7. Distribution of Goats 1961, Punjab Census Atlas, PDF p. 291.](maps/atlas_p291_goats_1961.png)

- Braudel, at the level of the longue durée and of space. Large flocks were
  possible only at altitude. Whether a village kept them depended on its
  valley, with its routes to particular winter grounds and markets. Braudel
  treats such regional differences inside one geographical frame as part of
  the structure. {{R braudel-envelope}}
- Bloch, at the level of comparison. Chaupal and the Ravi villages share the
  condition of altitude and differ in valley. By comparing them, the valley is
  isolated as a second condition. {{R bloch-compare}}

### 3.3. The Calendar and the Routes

- For the Gaddis and the Gujjars, the years of the sources in which each movement is described, and the
  months named in them, are in Table 3.2. Figure 3.2 shows the
  months by valley.
- In the 1881 census and the 1931 census, a winter descent is recorded without
  months. In Rose (1911) and the 1961 surveys, the months are named, and they
  agree. According to the text-reuse search, the 1961 descriptions and Rose's
  description of the Gaddi year do not copy the 1881 census.
- Each village lies in one river valley, and its flocks cross the ranges to
  the winter grounds of another valley. Women and whole households go with
  the flocks.

{{snippets 3.3}}

Table 3.2. Movements of the Gaddis and Gujjars in the sources.

{{table persistence}}

![Figure 3.2. The herding calendar from the evidence graph.](../../analysis/calendar/calendar.png)

![Map 3.8. Punjab Drainage System, Punjab Census Atlas 1961, PDF p. 25.](maps/atlas_p025_drainage_system.png)

![Map 3.9. Himachal Pradesh, Village Surveys, Devi-Kothi survey, PDF p. 2.](maps/devikothi_p002_hp_village_surveys_map.png)

![Map 3.10. Punjab, Location of Villages Selected for Socio-Economic Survey, Tandi survey, PDF p. 5.](maps/tandi_p005_punjab_location_of_survey_villages.png)

![Map 3.11. Kupha Notional Map, Pangi survey, PDF p. 2.](maps/kupha_p002_notional_map.png)

- Braudel, at the level of the longue durée. A winter descent is recorded in
  every source of the period, and where months are named, they are the same. It is the clearest case of
  geographical time in the sources. {{R braudel-structure}}
- Bloch, at the level of method. The persistence is attested by independent
  witnesses, because no copied text links the sources in which the descent is
  recorded. {{R bloch-agreement}} {{R bloch-series}}
- Marx, at the level of the labour process. The migration is family labour.
  The household, including the women who carry loads on the route, is the
  unit that works the flock. {{R marx-base}}

## 4. Comparisons

### 4.1. High Herders and Low Buyers

- Brahmaur and the low villages of Bir, Batal and Shakrori are set side by
  side in Table 4.1.
- The low villages kept a few sheep and goats, which they bought from the
  Gaddis and Kinnauras who passed through in winter, and bought wool from
  them.

{{snippets 4.1}}

Table 4.1. A high herding village and three low villages. Livestock figures
were read from page images.

{{table low_high}}

![Map 4.1. Bir Notional Map, Bir survey, PDF p. 2.](maps/bir_p002_notional_map.png)

![Map 4.2. Notional Map of Shakrori Village, Shakrori survey, PDF p. 2.](maps/shakrori_p002_notional_map.png)

- Braudel, at the level of the longue durée and of region. Each winter the
  herders from the high villages passed through the low villages and traded
  with them. The unit of the cycle is a region of high and low ground, not a
  single village. {{R braudel-routes}}
- Marx, at the level of exchange. The low villages took part in the herding
  economy as buyers of animals and wool, so they obtained the product of the
  high pastures as commodities. {{R habib-cash}}

### 4.2. Herding Families and Settled Farmers

- In Brahmaur most families herded their own flocks, and hired shepherds were
  rare. In Devi-Kothi the farmers paid graziers to take their animals to the
  high pastures. The Gaddis of Maingal had settled as farmers.
- According to the Chitrari survey, the families who migrate are those with a
  large flock.

{{snippets 4.2}}

![Map 4.3. Devi Kothi Notional Map, Devi-Kothi survey, PDF p. 4.](maps/devikothi_p004_notional_map.png)

![Map 4.4. Maingal Notional Map, Maingal survey, PDF p. 2.](maps/maingal_p002_notional_map.png)

![Map 4.5. Chitrari Notional Map, Chitrari survey, PDF p. 2.](maps/chitrari_p002_notional_map.png)

- Bloch, at the level of comparison. The three villages lie in the same
  valley under the same ruler and differ in how the herding was organised. By
  comparing them, geography is ruled out as the explanation of the
  difference.
  {{R bloch-compare}}
- Marx, at the level of the relations of production. The same means of
  production, the high pastures, were worked under different relations. The
  Brahmaur owner worked his own flock with his family. The Devi-Kothi farmer
  paid a grazier, which is a wage relation. The size of the flock a family
  owned determined which relation applied. {{R marx-relations}}

### 4.3. Two Valleys, the Ravi and the Sutlej

- The frequency of trade words in the surveys of each valley is in
  Table 4.2.
- The Ravi herders sold their woollens in the low hills of Kangra in winter.
  The Sutlej herders carried goods down to the Lavi fair at Rampur and traded
  with Tibet in summer.
- The ruler of Bushahr held the Sutlej villages as Primary Owner, and every
  villager of Kanum could use the pastures. In Chamba the raja held all
  grazing rights.
- After the India-China dispute the trade with Tibet nearly ended, and the
  weavers and wool buyers of the lower hills were short of wool.

{{snippets 4.3}}

Table 4.2. Trade, flock and debt words per 10,000 words of each survey.

{{table trade}}

![Map 4.6. Notional Map, Himachal Pradesh, Mahasu District 1961, Mahasu handbook, PDF p. 5.](maps/mahasu_p005_mahasu_district_rivers.png)

![Map 4.7. Notional Map, Mahasu District, Fairs and Festivals, Mahasu handbook, PDF p. 4.](maps/mahasu_p004_mahasu_fairs_and_festivals.png)

![Map 4.8. Kanum Notional Map, Kanum survey, PDF p. 2.](maps/kanum_p002_notional_map.png)

![Map 4.9. Notional Map of Kothi Village, Kothi survey, PDF p. 13.](maps/kothi_p013_notional_map.png)

![Map 4.10. Nachar Notional Map, Nachar survey, PDF p. 8.](maps/nachar_p008_notional_map.png)

- Bloch, at the level of comparison. The two valleys share the mountain year
  and differ in the direction of their rivers and in their rulers. By
  comparing them, each difference can be traced to one of these conditions. {{R bloch-compare}}
- Braudel, at the levels of structure and event. The direction of each river
  is a structure, and the direction of trade followed it. The closing of
  Shipki La is an event, and its effects were confined to the valley whose
  trade ran to Tibet.
  {{R braudel-event}}
- Marx, at the level of merchant capital. On the Sutlej the herders were also
  traders, and the flocks carried goods between Tibet and the lower hills.
  With the end of the trade, the Sutlej herders lost a source of income that
  the Ravi herders never had. {{R habib-banjaras}}

## 5. Owners, Workers and Debtors

### 5.1. Ownership of the Flocks

- The sheep and goats of every survey caste table, grouped by caste class,
  are in Table 5.1. The share of the landholding castes in each village is in
  Table 5.2, and the Brahmaur table is in Table 5.3. Figure 5.1 shows the
  shares by village.
- In Nachar the Lambardar, the village headman, owned the largest flock.

{{snippets 5.1}}

Table 5.1. Sheep and goats by caste class across all caste tables. Figures
were read from page images.

{{table class}}

Table 5.2. Sheep and goats by village, with the share of the landholding
castes. Figures were read from page images.

{{table villages_owners}}

Table 5.3. The Brahmaur livestock table (Brahmaur survey, PDF p. 54). Figures
were read from the page image and compared with the scan by Claude.

{{table brahmaur}}

![Figure 5.1. Share of sheep and goats by caste class in each village.](../../analysis/flocks/ownership_shares.png)

![Map 5.1. Punjab Social Map, Census of India 1931, Punjab, Part I, PDF p. 24.](maps/census1931_p024_punjab_social_map.png)

- Marx, at the level of the means of production. The flocks were the herders'
  capital, and the landholding castes owned them. Ownership of land and
  ownership of flocks lay with the same households. {{R marx-relations}} {{R marx-headman}}
- Braudel, at the level of the conjuncture. The caste tables were compiled
  once, in 1961. They are a description of the social structure at the end of the period
  and cannot by themselves establish a change. {{R bloch-series}}

### 5.2. Small Flocks of the Working Castes

- In Rajana, Pangna and Chaunri, where households kept a few goats, Koli
  households held most of the animals (Table 5.2).
- Across the villages, the share of the landholding castes is unrelated to
  altitude (entry A18).

- Marx, at the level of class. Concentration of flocks in the landholding
  castes belongs to the villages where herding produced a surplus for sale.
  Where a few goats served the household's own needs, the castes that worked
  the land owned them. {{R marx-relations}}

### 5.3. Debt Among Flock Owners

- Every Gujjar household in Maingal owned buffaloes and every Gujjar household
  was in debt. The lenders also bought their milk products, and one
  shopkeeper bought their ghee below the market price.
- Gujjars owed grain debts to Gaddi Brahmins. In Kanum the landlord was the
  moneylender. In Chergaon tenants paid interest in labour.
- In the surveys, debt is tabulated by income group or by cause, not by
  caste. The debt tables are in the Maingal survey (PDF p. 42), the Kanum
  survey (PDF p. 55), the Devi-Kothi survey (PDF p. 53) and the Bir survey
  (PDF p. 35). Caste appears only in the prose.

{{snippets 5.3}}

- Marx, at the level of surplus appropriation. The Gujjars owned their means
  of production, yet a share of their product went to the lender as interest
  and to the shopkeeper as a low price. This is appropriation through usurer's
  capital and merchant capital, without ownership of the producer's means of
  production. {{R habib-usury}} {{R marx-lenders}}
- Marx, at the level of class. In Kanum the landlord was also the lender, and
  in Maingal the Gaddi Brahmins who owned flocks also held the Gujjars' grain
  debts. {{R habib-debt}}

## 6. Conjunctures and Their Contradictions

### 6.1. The Raja's Pastures and the Fee Contract

- In 1881 the Gaddis held land under two rulers, British Kangra and Chamba,
  and paid fines to both. Gaddis crossing into Lahul paid grazing tax to two
  rulers.
- In Chamba the raja owned the land and all grazing rights. He auctioned the
  right to collect the grazing fees, usually to a Gaddi. Near Brahmaur the
  ruler leased the pastures to a contractor, who allotted them to shepherds on
  condition that their flocks manure the fallow fields.
- In Bushahr the villagers owed the ruler a labour service called Athada
  Begar.
- An attempt in 1874 to lease the high pastures of Pangi was abandoned after
  opposition.
- The fee rates under the raja and under the Forest Department are in
  Table 6.1. The claims of payment in each conjuncture are counted in
  Table 6.4.

{{snippets 6.1}}

Table 6.1. Grazing fees under the raja and under the Forest Department. The
units differ by row. The raja's contractor charged per head for each grazing
district (Newell, PDF p. 18), and the Department charged per head for a
season, twice a year in Brahmaur (Brahmaur survey, PDF p. 55). The Devi-Kothi
rows were read from the image of Table XIV (Devi-Kothi survey, PDF p. 47), and
the 1962 rates from the image of Newell, PDF p. 19. Newell does not state the
period of the 1962 rates.

{{table rates}}

Table 6.4. Relations of payment named in the evidence graph, counted by
conjuncture.

{{table flows}}

![Figure 6.1. Who takes a share of whose product, by conjuncture.](../../analysis/surplus/flows.png)

- Braudel, at the level of the conjuncture. Under the princely grazing
  regime, which lasted until about 1950, the use of the pastures was
  organised by the raja and his contractors. {{R braudel-conjuncture}}
- Marx, at the level of the forms of surplus. The raja was both ruler and
  owner of the pastures, so his grazing fee was at once a tax and a payment
  for the use of land. The surplus was taken as a fee in cash, as labour
  under the Athada Begar, as wool in place of revenue (Newell, PDF p. 14),
  and as manure under the contract. Under the fee contract, one Gaddi
  stood between the raja and the other Gaddis, so the fee was collected
  through the herding community itself. {{R habib-revenue}} {{R habib-rent-forms}}
- Marx, at the level of contradiction. The raja's ownership of the pastures
  conflicted with the herders' customary use. The lease of 1874 was abandoned
  after opposition, so customary use limited the ruler's claim.
 {{R marx-fetters}}
- Braudel, at the level of the event. The lease attempt of 1874 is an event.
  After it failed, customary grazing continued as before.
  {{R braudel-event}}

### 6.2. Forest Department Permits

- After incorporation into Himachal Pradesh, private property in land was
  introduced, and a Settlement of Brahmaur tahsil began in 1953 (Newell, PDF
  p. 19).
- After 1948 the Forest Department took over the grazing tax. Its officers
  issued a receipt only to a shepherd with a permit, allotted each shepherd a
  fixed pasture for a fixed number of animals, and granted no additional
  permits.
- The Department distinguished graziers with rights from the former rulers
  from other graziers. In the Devi-Kothi table of charges, right holders pay
  less only for buffaloes, and sheep, goats and cattle pay the same (Table 6.1).
- The Department's officers issued passes to check erosion, closed some pastures for
  soil conservation, and punished grazing without a pass by a fine or by
  forfeiture of the animal.
- The sheep and goats that paid grazing fees in Brahmaur tahsil each year are
  in Table 6.2 and Figure 6.2, and the change by phase is in Table 6.3. Most of
  the decline lies in one phase, and the number did not rise again. Newell notes
  a sheep disease in the year of the fall and attributes the loss to the
  permit system.

{{snippets 6.2}}

Table 6.2. Sheep and goats paying grazing fees in Brahmaur tahsil (Newell,
PDF p. 38). Figures were read from the page image.

{{table series}}

Table 6.3. Change in fee-paying sheep and goats by phase.

{{table phases}}

![Figure 6.2. Sheep and goats paying grazing fees in Brahmaur tahsil.](../../analysis/fees/fee_flocks.png)

- Braudel, at the level of the conjuncture. The fee series is a measured
  conjuncture, a medium-term movement read from a yearly series. The sheep
  disease is an event inside it. The series does not recover after the
  disease, so the disease alone cannot explain the level that follows. The
  Department collected the fee through its own employee, without the contractor
  who had stood between the raja and the herders. The unit of the charge also
  changed, from a fee per head for each grazing district to a fee per head for
  the season under a permit (Table 6.1). Aymard records a comparable removal of
  middlemen from the collection of a tax.
 {{R braudel-measure}} {{R braudel-short}} {{R aymard-middlemen}}
- Marx, at the level of rent. The state replaced the raja as landlord of the
  pastures and took a money rent per head. The distinction between right holders and others, which came from the former
  rulers, survived as a lower charge for buffaloes, so part of the old order of
  privilege was carried into the new one. {{R marx-continuity}}
- Marx, at the level of contradiction. Conservation of the pastures
  conflicted with the herders' subsistence. Under the cap on permits, the
  conflict was settled in favour of the existing permit holders. {{R kosambi-surplus}}

### 6.3. Permits as Property, and Roads as Wages

- Newell records that shepherds bought and sold permits and had become closed
  corporations.
- In Kanum the landowners could not find labourers for their flocks, because
  men and women preferred road work at higher wages. In the Brahmaur, Kothi and Nachar surveys, villagers are recorded working
  as road labourers.
- The Rohtang route was made jeepable. According to the Atlas, Kangra and
  Lahaul and Spiti had few metalled roads in 1947 and more by 1961.

{{snippets 6.3}}

![Map 6.1. Metalled and Unmetalled Roads 1947, Punjab Census Atlas, PDF p. 308.](maps/atlas_p308_roads_1947.png)

![Map 6.2. Metalled and Unmetalled Roads 1961, Punjab Census Atlas, PDF p. 309.](maps/atlas_p309_roads_1961.png)

- Marx, at the level of property in land. Under the raja the whole state
  belonged to the nation in the person of the raja, and land could not secure
  a debt. The Settlement of 1953 introduced private property in land, as the
  British settlements had done in the plains. {{R marx-property}}
- Marx, at the level of property. A state licence to graze became a commodity
  that established shepherds bought and sold. Newcomers could not obtain one,
  so the permit holders became a closed group. {{R habib-commodity}} {{R marx-quantity}}
- Marx, at the level of wage labour. Villagers could earn a cash wage on road
  work, outside the herding economy. Flock owners who depended on hired shepherds lost their
  labour, and families who herded their own flocks gained a second income.
 {{R marx-roads}} {{R marx-cash}}
- Braudel, at the level of the conjuncture. Road building from the 1950s is a
  conjuncture that the Brahmaur surveyor expected to change "the cycle of
  their life followed since ages". In 1961 the change had begun and the
  calendar still held. {{R braudel-rupture}}

## 7. Interpretation

### 7.1. The Two Lenses Together

- The persistence of the cycle is explained in the Annales reading
  (Section 3). The change in who took a share of its product is explained in
  the Marxist reading (Sections 5 and 6).
- Under Braudel's levels of time, the evidence falls into order. The calendar and the
  altitude threshold are the longue durée. The princely fee regime, the
  Forest Department regime, the Tibet trade and road building are
  conjunctures. The merger of 1948, the India-China dispute and the sheep
  disease are events. {{R braudel-levels}}
- Marx's analysis is applied at each conjuncture. It asks who owned the means
  of production, who worked, how a share of the product was taken, and what
  contradiction ended the arrangement. {{R marx-base}} {{R braudel-marx}}

### 7.2. Continuity of Property Forms Across 1948

- On the Ravi the raja's revenue farm was followed by a market in Forest
  Department permits. On the Sutlej the common pastures became state forest.

{{snippets 7.2}}

- Marx, at the level of the dialectic. Each new arrangement was built from the
  one before it. The distinction between right holders and others under the rajas survived in
  the Department's charges (Section 6.2). {{R marx-property}}

### 7.3. Gains and Losses by 1961

- By 1961 the migration took place on fixed pastures under tradable permits, with
  fewer fee-paying animals (Table 6.2) and with hired shepherds leaving for
  the roads (Section 6.3).
- Herders without permits, Scheduled Caste households that owned few
  animals (Table 5.1) and indebted Gujjars (Section 5.3) lost by the change.
  Permit holders and the state gained.

- Marx, at the level of class. After the change, access to the pastures
  depended on property. The holders of permits kept access, and those without
  permits lost it. {{R marx-class}} {{R braudel-silent}}

## 8. Limits

- A count of claims is a measure of how often the sources mention a relation,
  not of the size of the payment (Table 6.4).
- The village surveys cover villages chosen by the Census, not a random
  sample (Table 3.1).
- Copied passages are counted once (Table 2.2).
- No source in the corpus dates the closing of Shipki La. In the Kanum survey, only the "India-China dispute" is named (Kanum survey, PDF p. 51).
- The livestock tables and the fee series were read from page images and
  have not been checked by a person, apart from the Brahmaur table, which was
  compared with the scan by Claude.
- No source in the corpus maps the migration routes, the passes or the
  summer pastures.

## Readings

{{readings}}
