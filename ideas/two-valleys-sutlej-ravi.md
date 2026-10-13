# Two valleys: herding, pastures and trade on the upper Sutlej and the Ravi, 1881 to 1961

This version builds on
[seasonal-herding-himachal.md](seasonal-herding-himachal.md) (seasonal
herding). It turns
v6 into a comparison of two river valleys. Both herded sheep and goats between
high summer pastures and low winter grazing. They differed in which way their
trade faced, who owned the pastures, and what happened to them after 1948 and
after the 1962 closure of the Tibet border. The other idea files are in
this folder (see [README.md](README.md)).

The interpretation works in two steps. The Annales step reads the geography
of the two valleys and the time scales, and makes the comparison. The Marxist
step then looks inside each medium-term period (conjuncture) for the
contradictions that drove change in each valley. The interpretive framework
section sets this out.

The sections follow the three stages in `project.docx`.

---

## How to check a reference

Every claim cites a source name and a PDF page, for example "(Kanum, p. 16)".
The page is the PDF page number that a PDF viewer shows, not the number
printed on the scan. The table below gives the file for each source name.

| Source name | PDF file | Where it is |
| --- | --- | --- |
| Brahmaur, Chitrari, Devi-Kothi, Maingal, Kanum, Kothi, Nachar, Tandi, Chergaon, Shakrori, Chauntra, Rajana, Bir, Chaupal, Moginand, Kot, Nalag, Chaunri, Basal, Batal, Shathla | `1961 Census, Village Survey (<village> ...).pdf` | inside `sources/1961 Village surveys + census reports-...zip` |
| Kupha | `44160_1961_KUP.pdf` (Kupha, Parmas, Thamoh and Malet, Pangi) | same zip |
| Newell | `1961 Census, Report on SC and ST of Himachal Pradesh.pdf` (William H. Newell's study of the Gaddis) | same zip |
| Weaving | `1961 Census, Himachal Pradesh Craft Survey - Weaving.pdf` | same zip |
| Mahasu | `1961 Census, District Handbook - Mahasu.pdf` | same zip |
| 1881 | `2. Census of the Punjab, 1881, Denzil Ibbetson, Results, pp 1-421.pdf` | inside `sources/Punjab 1881, Denzil Ibbetson-...zip` |
| 1931 | `Census of India 1931, Vol 17 Punjab, Part I Report.pdf` | `sources/` |
| Rose | `2015.69652.Glossary-...-Vol2.pdf` (Rose, Vol. 2) | `sources/` |

To find the page of any other quote, run from the project folder:

```
python3 scripts/pageref.py find "words from the quote"
```

The script searches the text in `text/`, which keeps one page break per PDF
page. It ignores case, punctuation and line breaks.

**Table figures.** The extracted text scrambles many tables. Figures marked
**(image)** were read from the rendered PDF page. The other figures come from
the extracted text and need checking against the page.

---

### Terms used

- **Transhumance.** Seasonal movement of herds between high summer pastures and
  low winter grazing, by people who keep a fixed home and fields.
- **Gaddis.** Herding and farming people whose home is Brahmaur in Chamba, in
  the Ravi valley. They cross the Dhauladhar range to Kangra each winter.
- **Kinnauras.** The people of Kinnaur, on the upper Sutlej. Before 1948 Kinnaur
  was part of Bushahr State.
- **Dhar.** A high summer pasture.
- **Malundi, pohal, fawal.** Shepherds. A malundi tends his own flock. A pohal
  (Chamba) or fawal (Kinnaur) is hired.
- **Permit.** A Forest Department licence stating how many animals a shepherd
  may graze. Fees are charged per head.
- **Lavi fair.** A trade fair held each November at Rampur, on the Sutlej.
- **Pashm.** Fine goat wool (pashmina), which came from Tibet.
- **Longue durée, conjuncture, event.** Braudel's three time scales. The longue
  durée is geographical time, which changes over centuries: mountains, rivers,
  snow. A conjuncture is a period of a few decades with its own economic and
  political arrangement, such as princely rule over the pastures. An event is a
  single dated change, such as the 1948 merger.
- **Dialectic, contradiction.** In the Marxist reading, change comes from the
  conflict between two opposed forces inside one arrangement, for example
  between the shepherds who use a pasture and the ruler who owns it. The
  conflict produces a new arrangement, which carries its own contradictions.

---

## Connections to the original ideas

| Idea in `candidate-topics.md` | Role in this comparison |
| --- | --- |
| **10. The river as the unit of study** | Main. The two units are the upper Sutlej and the Ravi with its tributary the Budhal. Newell describes each Chamba valley as "a 40 mile length of river between high mountains" (Newell, p. 10). |
| **2. Trade with Tibet stops** | Main. Only the Sutlej valley traded with Tibet. The comparison measures what that trade and its closure meant. |
| **5. Whose forest is it?** | Main. Pasture ownership, Forest Department permits and closed forests, compared across the two valleys. |
| **12. Debt and caste** | Supporting. Debt levels and creditors in each valley. |
| **8. Scheduled Tribe status** | Background. Gaddis and Gujjars are Scheduled Tribes "since 1956" (Maingal, p. 17). `candidate-topics.md` gives 1950 from a secondary source. |
| **15. Women's status** | Background. On the Gaddi winter route "the wife usually accompanies her husband" (Newell, p. 36). |
| **1. Cash crops** | Background. Orchards appear in both valleys by 1961 (Kothi, p. 100. Brahmaur, p. 45). |

---

## Stage 1. Research question

### Research question

> **How did two Himalayan river valleys organise the same seasonal herding
> economy differently between 1881 and 1961? On the upper Sutlej, flocks
> carried trade to and from Tibet. In the Ravi valley, Gaddi flocks faced
> south to Kangra and the plains. How did geography, the ownership of flocks
> and pastures, forest rights and the direction of trade shape each valley,
> and what changed when the Forest Department took over the pastures after
> 1948 and the Tibet border closed in 1962?**

Sub-questions:

1. **The herding cycle.** Do the two valleys follow the same seasonal cycle?
   How far do the routes and months in 1961 match those recorded in 1881 and
   1910?
2. **Ownership and labour.** Who owns the flocks in each valley, by caste? Who
   does the herding, and how are hired shepherds paid?
3. **Pastures and forests.** Who owned the pastures before 1948 and after? What
   did grazing cost, and what did the Forest Department restrict?
4. **Trade.** What did the flocks carry, where to, and on what terms? How did
   trade with Tibet differ from trade with the plains?
5. **Change by 1961.** Which changes hit both valleys (permits, roads,
   orchards), and which hit only the Sutlej (the closed border)?

---

## Interpretive framework

### Step 1. Annales: geography, time and the comparison

**Geography of the two valleys.**

| Feature | Upper Sutlej | Ravi and Budhal |
| --- | --- | --- |
| Where the river leads | Up to Shipki La and Tibet. The Hindustan-Tibet road runs along the Sutlej below Nachar (Nachar, p. 9). Caravans crossed Shipki La until the India-China dispute (Kanum, p. 51) | The Budhal rises at the Kugti pass and joins the Ravi at Kharamukh (Brahmaur, p. 11). The passes lead north to Lahul and Pangi, not to Tibet. Crossing the Kugti pass takes "three days actually on the tops" (Newell, p. 18) |
| Where the flocks winter | Down the Sutlej to Bilaspur, Arki and Sirmur (Kanum, p. 85) | South over the Dhauladhar to Kangra, Nurpur, Pathankot and Jammu (Brahmaur, p. 55) |
| Nearest markets | The Lavi fair at Rampur, on the same river (Kanum, p. 16. Mahasu, p. 56) | Chamba town, then Pathankot and Amritsar (Brahmaur, p. 14. Chitrari, p. 39) |
| Unit of settlement | Villages 2 to 3 miles above the Sutlej (Kanum, p. 15. Nachar, p. 9. Kothi, p. 14) | "a 40 mile length of river between high mountains" (Newell, p. 10) |

**Time.** Both valleys keep the same longue-durée cycle: out in October,
back in April (Kanum, p. 85. Brahmaur, p. 55). For the Ravi the colonial
sources show the same cycle in 1881 (1881, p. 275) and 1910 (Rose, p. 297).
For the Sutlej they do not describe it. The events differ by valley: the
closed border reaches only the Sutlej, and the permit system is recorded
mainly on the Ravi.

**The comparison.** The two valleys share altitude, season and the herding
cycle. They differ in where the river leads. That makes the comparison a test
of how far the direction of trade, which geography sets, changes the rest of
the herding economy. The 16-village table in Stage 2 adds a second
comparison, between high and low villages across five river systems.

### Step 2. Marxist: contradictions within each conjuncture

The Marxist step takes each conjuncture and asks, for each valley, which two
forces pulled against each other and what came out of the conflict.

| Conjuncture | Upper Sutlej | Ravi and Budhal | What the comparison shows |
| --- | --- | --- | --- |
| **Princely property, to 1948** | The Bushahr ruler is "Primary Owner", but there is "no custom to partition the pastural land" (Kanum, p. 18). Dues "including 'Athada Begar'" were fixed by the size of holdings (Kanum, p. 18). The contradiction is between sovereign ownership and common use | The raja owns all grazing and sells the right to collect fees to "the highest bidder, who was usually a Gaddi" (Newell, p. 18). The contradiction runs inside the herding community, between the fee-farmer and the herders. Two sovereigns also claim the same Gaddis (1881, p. 275) | The Ravi's princely regime already turned grazing into a revenue farm. The Sutlej kept the pastures as undivided commons |
| **Trade, to the early 1960s** | Exchange across a border. Flocks carry wool, chilgoza and pashm down and salt and grain up (Kanum, p. 16. Nachar, p. 33). The contradiction is between a livelihood that depends on crossing the border and a state that closes it | Exchange through merchant-creditors. Gujjars sell ghee to a Chamba shopkeeper who "pays them much less than the market price" (Maingal, p. 60), and the Chamba weight is "a losing bargain" (Maingal, p. 42). Pangi Bhot traders take grain at "four times" the value of goods (Devi-Kothi, p. 53). The contradiction is between producers and the traders who lend to them | Trade was a source of loss in both valleys, by different mechanisms: a political border on the Sutlej, and debt and unequal exchange on the Ravi |
| **The state forest, 1948 to 1961** | The Forest Department fenced village grazing, with "restrictions on grazing goat and sheep" (Kanum, p. 133). Chilgoza collection runs "under the Forest Settlement" (Kothi, p. 79) | Permits cap flock numbers (Brahmaur, p. 46), are "freely bought and sold", and make shepherds "closed corporations" (Newell, p. 37). Closures stop erosion (Chitrari, p. 23) and cause "resentment" (Kupha, p. 136). Fee-paying flocks fall 25.7% (Newell, p. 38) | The Ravi's older revenue farm became a market in permits. The Sutlej's commons became fenced state land. The prior form of property shaped the new one |
| **Roads and wages, 1950s to 1961** | Hired shepherds leave: "Men and women now prefer to work on the roads rather than work as 'fawals'" (Kanum, p. 51) | Road and building work pays "about Rs. 2" a day (Brahmaur, p. 45). A jeep runs on "our beaten track for centuries" (Chitrari, p. 24) | Wage work pulls labour out of herding in both valleys. On the Sutlej it removes the hired shepherd. In Brahmaur, where families herd their own flocks (Brahmaur, p. 55), it adds a second income |

One contradiction runs through every conjuncture in both valleys. The
landholding castes own the flocks, and the Sipi, Koli and Lohar households own
few. Brahmans and Rajputs hold 97.9% of Brahmaur's sheep and goats (Brahmaur,
p. 54). Rajputs hold 94.5% of Kothi's (Kothi, p. 102).

---

## The two valleys compared

### 1. The herding cycle

| | Upper Sutlej (Kinnaur) | Ravi and Budhal (Gaddis) |
| --- | --- | --- |
| Rivers | Sutlej about 2 miles below Kanum (Kanum, p. 15), 3 miles below Nachar (Nachar, p. 9) and 2 miles below Kothi (Kothi, p. 14) | The Budhal "rises in the Kugti pass" and "empties into the Ravi at Kharamukh" (Brahmaur, p. 11). Ravi 2 miles below Chitrari (Chitrari, p. 16) |
| Summer pastures | "Pruti, Brati, Rao, Runang ... Hangrang Valley" (Kanum, p. 85). Alpine pastures of Lahaul-Spiti (Nachar, p. 33) | "dhars" in Pangi and Lahaul (Brahmaur, p. 55). Lahul and Bara Bangahal (Newell, p. 36) |
| Winter grazing | "During winter from October they migrate to Lower Hills" toward Bilaspur, Arki and Sirmur (Kanum, p. 85). Suni, Karsog, Arki, Bilaspur (Kothi, p. 91) | "In the beginning of the winter (October and November), the flocks are driven to the low hills of Kangra, Nurpur, Pathankot and Jammu" (Brahmaur, p. 55) |
| Who goes | Couples and children go to the low hills, and the elderly stay behind (Nachar, p. 33) | "Out of 99 local households, as many as 61 move out in winter months" (Brahmaur, p. 63) |
| Same cycle in colonial sources | not described for Kinnaur in the 1881 or Rose texts | 1881: flocks feed "half the year (the winter months) in the valleys of Kangra" (1881, p. 275). 1910: "The yearly exodus to Kangra takes place in October and November, and the return journey in April and May" (Rose, p. 297) |

The 1931 Report describes the same movement for the whole hill region: "the
hillmen of the lofty ranges leave their homes with their sheep and cattle to
spend the winter in the valleys and plains of the neighbouring districts"
(1931, p. 142).

### 2. Flocks, ownership and labour

| | Upper Sutlej | Ravi and Budhal |
| --- | --- | --- |
| Flock totals | Kanum: 1,744 sheep and goats held by 61 Kanet (Rajput) households (Kanum, p. 61). Kothi: Rajputs 2,416, Kolis 72, Lohars 58, Badhis 11 (Kothi, p. 102) | Brahmaur: 4,484 across 48 of 99 households (Brahmaur, p. 54). Devi-Kothi: 1,117 sheep and 220 goats (Devi-Kothi, p. 47) |
| Per family | "On an average, 100 to 200 sheep and goats are kept by a family." The lambardar has "about 1,100" (Nachar, p. 33) | Brahmans 20 households with 2,027 animals, Rajputs 20 with 2,364, Sipis 8 with 93 (Brahmaur, p. 54) |
| Hired shepherds | Landholders "found it difficult to engage labourers to attend to their sheep and goats. Men and women now prefer to work on the roads rather than work as 'fawals'" (Kanum, p. 51) | Pohals are hired "by a very few people in rare cases" and paid meals, clothing, wool, "two or four sheep per hundred" and Rs 2 a month (Brahmaur, p. 55). "The majority of Gaddis are not shepherds" (Newell, p. 37) |

In both valleys the landholding castes own almost all the animals. In
Brahmaur, Brahmans and Rajputs hold 4,391 of 4,484, which is 97.9% (our
arithmetic from Brahmaur, p. 54). In Kothi, Rajputs hold 2,416 of 2,557, which
is 94.5% (our arithmetic from Kothi, p. 102). The table also lists 2 Badhi households with 11 animals.

### 3. Pastures, grazing dues and forest rights

| | Upper Sutlej | Ravi and Budhal |
| --- | --- | --- |
| Owner before 1948 | The Bushahr ruler as "Primary Owner". There is "no custom to partition the pastural land" (Kanum, p. 18) | "In Chamba all grazing rights belonged to the rajah of Chamba" (Newell, p. 18). The right to collect fees was "auctioned by the rajah of Chamba to the highest bidder, who was usually a Gaddi" (Newell, p. 18) |
| Owner after 1948 | "Every villager has a right of utilizing the pastures" (Kanum, p. 133) | Fee rights "have now been taken over by the ... State Forest Department" (Newell, p. 19). Pastures "allotted direct to the shepherds by the Forest Department" (Brahmaur, p. 55) |
| Grazing dues | not stated in Kanum, Kothi or Nachar | 1950: 2 annas 6 pies per goat and 1 anna 6 pies per sheep (Newell, p. 18). 1961: Rs 15 per 100 head per season (Brahmaur, p. 55). Devi-Kothi permit fees per head, right-holders and others (Devi-Kothi, p. 47) |
| Permits | not stated | A receipt "is however not issued unless the shepherd has a permit" (Newell, p. 19). "Forest Department do not now grant any additional permit for more sheep and goats" (Brahmaur, p. 46). Permits "are freely bought and sold amongst shepherds so that shepherds have now become closed corporations" (Newell, p. 37) |
| Closed forests | The Forest Department fenced village grazing land. "Restrictions on grazing goat and sheep have now been imposed in the fenced area" (Kanum, p. 133) | In a Chitrari reserve, "Grazing or collecting fire wood ... is completely banned" (Chitrari, p. 17). Passes were issued because "intensive grazing for generations led to erosion" (Chitrari, p. 23). In Pangi, "certain pastures have also been closed ... soil conservation," which caused "a sense of resentment against the Forest Department" (Kupha, p. 136) |
| Older rights | Chilgoza collected "under the Forest Settlement, Sutlej Valley Bushahr State" (Kothi, p. 79) | Right-holders have rights "given to them by the early rulers of Chamba" (Devi-Kothi, p. 49). In Pangi, sheep and goats "are excluded" from forests in spring and autumn, and an 1874 attempt to lease the dhars "provoked much opposition" (Kupha, p. 113) |

The Ravi valley records far more Forest Department control than the Sutlej
villages do. Fee-paying sheep and goats in Brahmaur tahsil fell from 42,176
sheep and 31,695 goats in 1952-53 to 30,515 and 24,406 in 1961-62, a 25.7% fall
in total (Newell, p. 38. Figures from the extracted text). Newell's own table
notes that sheep "were struck by disease" the year before 1959-60 (Newell,
p. 38). Permits and disease are two possible causes.

### 4. Trade

| | Upper Sutlej | Ravi and Budhal |
| --- | --- | --- |
| Direction | North to Tibet and south to the Lavi fair at Rampur | South to Chamba town, Kangra, Pathankot and Amritsar. North only to Pangi and Lahaul |
| Goods out | Flocks go down "laden with chilgozas, wool, woollen patties, nuts, pasham, jira" (Kanum, p. 16) | "The gardus ... command a ready market in the low hills" in winter (Brahmaur, p. 59). The wool clip "is sold to Kangra traders" (Newell, p. 36). Chitrari sells woollen thobis and pattus at Chamba, where "the Chamba market is better organised" (Chitrari, p. 39) |
| Goods in | Salt and grain carried on goats, which "carry small cloth or leather bags ... used for transporting grains, salt" (Nachar, p. 33) | Goods "imported from Chamba or in some cases from Amritsar" (Brahmaur, p. 14). Devi-Kothi buys cloth, oil, gur and salt at Tisa and other markets (Devi-Kothi, p. 21) |
| Tibet | Before the India-China dispute Shipki La was open, "but no more do caravans of mules, flocks of sheep and goats and laden human beings now wind through" (Kanum, p. 51). A Kanum man took a goat caravan to Tibet in 1940 to 1945 (Kanum, p. 132) | None. In 1881 the Tibet and Ladakh trade belongs to the Lahulis (1881, p. 407). Rose lists a Gaddi clan name "Lade, a trader to Laddakh" (Rose, p. 294) |
| Northern links | Kinnaur flocks graze in Lahaul-Spiti (Nachar, p. 33) | Devi-Kothi "exports surplus foodgrains to Pangi" (Devi-Kothi, p. 43). Pangi's Bhot traders sell small goods and "do not sell things in cash", taking grain "seldom less than four times of the original cost" (Devi-Kothi, p. 53). Pangi buys salt at Tarela and carries it on sheep and goats (Kupha, p. 69). Ladakh visitors attend the Trilokinath fair (Kupha, p. 52) |
| Fairs | The Lavi fair at Rampur (Kanum, p. 16. Kothi, p. 79). "Lavi the biggest trade fair in Himachal" (Mahasu, p. 56) | The Brahmaur jatra, attended by jewellers from Kangra and Amritsar (Brahmaur, p. 31). Minjar fair at Chamba (Maingal, p. 52) |
| Terms of trade | not stated beyond barter of salt and grain | Gujjars sell ghee to "a particular shopkeeper at Chamba who pays them much less than the market price" (Maingal, p. 60). The Chamba weight (tol) is "a losing bargain to the Gujjars" (Maingal, p. 42) |

The closure of the Tibet trade reached beyond Kinnaur. The Weaving Craft
Survey states: "The Pradesh had however a great set back after the trade with
Tibet stopped. An acute shortage of wool and Pasham is being experienced for
the last few years. Particularly Pasham is no more there. Pasham producing
goats are available only in Tibet" (Weaving, p. 16). Downstream on the Sutlej,
Chergaon "used to go to Rampur to purchase wool during Lavi fair. But
now-a-days, they prefer to buy wool from Dodra Kawar illaqa" (Chergaon,
p. 61).

### 5. Debt

| | Upper Sutlej | Ravi and Budhal |
| --- | --- | --- |
| Level | Kanum: "113 households 76 are in debt," Rs 250 to Rs 1,900 per household (Kanum, p. 55). Kothi: loans mostly from village moneylenders at 12.5% (Kothi, p. 86) | Brahmaur: "only 4 reported cases" of debt (Brahmaur, p. 62). Maingal: "Gujjar households are cent per cent under debt" at 30% (Maingal, p. 42), with "grain debts to Gaddi brahmins" (Maingal, p. 38) |

### 6. Change by 1961

| | Upper Sutlej | Ravi and Budhal |
| --- | --- | --- |
| Border | The Shipki La trade stopped (Kanum, p. 51) | not affected |
| Permits and closures | Fenced grazing land (Kanum, p. 133) | No new permits (Brahmaur, p. 46). Fee-paying flocks down 25.7% (Newell, p. 38) |
| Labour | Road work preferred to herding for wages (Kanum, p. 51) | Road and timber work at the approach road (Brahmaur, p. 45) |
| Roads | Fewer Kinnaur families came down to the low hills this year "though not as many as in" earlier years (Kothi, p. 92) | A Gaddi shepherd says a jeep now runs on "our beaten track for centuries" (Chitrari, p. 24) |
| Orchards | Orchards laid out "on some ambitious scale" (Kothi, p. 100) | Apple planting beginning (Brahmaur, p. 45) |

---

## Stage 2. Analysis

### Context: herding across 16 villages and five river systems

A short comparative section places the two valleys among all the surveyed
villages that name a river. Villages high on the Sutlej, Ravi and Chenab keep
many more animals per household than villages on the Beas and Yamuna systems.

| River system | Village | Sheep and goats | Households | Per household (our arithmetic) | Page |
| --- | --- | --- | --- | --- | --- |
| Chenab | Tandi | 363 sheep, 21 goats | 18 surveyed | 21.3 | Tandi, p. 56 |
| Chenab | Kupha cluster | 596, held by 82 households | not stated | | Kupha, p. 80 |
| Ravi | Brahmaur | 4,484 | 99 | 45.3 | Brahmaur, p. 54 |
| Ravi | Devi-Kothi | 1,117 sheep, 220 goats | not stated | | Devi-Kothi, p. 47 |
| Ravi | Maingal | 114 sheep and 106 goats (Gaddi Brahmins), 217 buffaloes (Gujjars) | 31 | | Maingal, p. 48 |
| Sutlej | Kanum | 1,744 (Kanets) and 83 (Kolis) | 113 | 16.2 | Kanum, p. 61 |
| Sutlej | Kothi | 2,557 **(image)** | 128 | 20.0 | Kothi, p. 102 |
| Sutlej | Nachar | "100 to 200" per family | 213 | | Nachar, p. 33 |
| Sutlej | Shakrori | 23 sheep, 53 goats **(image)** | 60 | 1.3 | Shakrori, p. 76 |
| Sutlej | Nalag | 118 sheep, 241 goats **(image)** | not checked | | Nalag, p. 31 |
| Beas | Bir | 139 goats, 69 sheep | 36 | 5.8 | Bir, p. 43 |
| Beas | Chauntra | 41, held by 14 households | not checked | | Chauntra, p. 46 |
| Beas | Kot | at least 207 | not checked | | Kot, p. 56 |
| Yamuna (Pabbar) | Chergaon | 143, held by 16 households | 68 | 2.1 | Chergaon, p. 56 |
| Yamuna (Giri) | Rajana | about 554 (partial sum) | 161 | 3.4 | Rajana, p. 47 |
| Yamuna (Tons) | Chaupal | 126 goats **(image)**. A second column, 107 animals, has no printed heading | 80 (1964) | 1.6 goats | Chaupal, p. 48 |
| Yamuna (Ashni Khud) | Chaunri | 45 goats and sheep, held by 12 households **(image)** | 58 | 0.8 | Chaunri, p. 34 |
| none named | Basal | 139 goats and sheep, held by 43 households **(image)** | 119 | 1.2 | Basal, p. 77 |

The lower villages still take part in herding, because migrant flocks pass
through them. Shakrori buys animals "from the Kinnauras that go by" (Shakrori,
p. 75). Bir buys from "Gaddis who wander near about in winter" (Bir, p. 43).
Rajana's people buy from Gaddis who camp on the Giri in March and April
(Rajana, p. 70). Chauntra "was, at one time, a pasture land where Gaddis grazed
their flocks" (Chauntra, p. 63). The Mahasu Handbook lists by tahsil the
pastures used by "mobile Gujjars, Gaddis and Kannauras", with fees (Mahasu,
pp. 334 to 336).

### Computational method

| Method | What it measures | Lesson on programminghistorian.org | Output |
| --- | --- | --- | --- |
| 1. Two-valley dataset | One row per village and variable in the six comparison tables above, each with its PDF page | *Cleaning Data with OpenRefine* | CSV |
| 2. Seasonal calendar | For each valley and month: where the flocks are, who is away, what is sown or harvested, which fair is held | *Cleaning Data with OpenRefine* | Calendar chart, one row per valley |
| 3. Route and trade map | Home villages, summer pastures, passes, winter grazing, fairs and markets, with trade goods on each route. Tibet routes on the Sutlej, plains routes on the Ravi | *Georeferencing in QGIS 2.0*, *Geocoding Historical Data using QGIS* | One map on the 1961 Punjab Census Atlas base |
| 4. Ownership and dues | Flocks by caste (Brahmaur, Kanum, Kothi), grazing fees, permits, debt | *Creating Interactive Visualizations with Plotly* | 2 charts |
| 5. Time series | Fee-paying sheep and goats in Brahmaur tahsil, 1952-53 to 1961-62 | *Visualizing Data with Bokeh and Pandas* | One line chart |
| 6. 16-village context | Sheep and goats per household by river system | *Creating Interactive Visualizations with Plotly* | One chart |
| 7. Concordance | Terms for trade (Tibet, Lavi, salt, wool, barter), grazing (permit, fee, dhar) and forest (reserve, closed) in each valley's sources, coded by topic | *Keywords in Context (Using n-grams) with Python* | Coded CSV, one table per valley |

`scripts/pageref.py` finds the PDF page of any passage, so every row in the
datasets can carry its page. `scripts/kwic.py` covers the concordance. Its term
list needs these terms before use.

### Division of work

| Person | Work | Output |
| --- | --- | --- |
| 1 | Upper Sutlej: Kanum, Kothi, Nachar, Shakrori, Weaving Survey, Mahasu Handbook | Its half of the dataset, trade routes for the map |
| 2 | Ravi and Budhal: Brahmaur, Chitrari, Devi-Kothi, Maingal, Newell, Kupha | Its half of the dataset, fee time series |
| 3 | Map, calendar, 16-village context chart, concordance | Map, 2 charts, coded CSV |

---

## Stage 3. Historical interpretation (plan)

The essay argues in two moves, following the framework.

1. **Annales: the frame and the comparison.** Altitude, snow and the herding
   cycle are the same in both valleys. Where each river leads is different.
   Geography therefore decides which outside forces reach each valley: the
   Tibet border reaches the Sutlej, and the plains market and the Chamba
   state reach the Ravi.
2. **Marxist: the contradictions inside each conjuncture.** In each period the
   two valleys show different contradictions: sovereign ownership against
   common use, producers against merchant-creditors, conservation against
   subsistence, and flock owners against labourers with wage work. The form of
   property each valley had before 1948 shaped the form it took after 1948: a
   revenue farm became a permit market on the Ravi, and commons became fenced
   state land on the Sutlej.

The conclusion states which explains more of the difference between the two
valleys. The evidence so far suggests that geography decides which shock
reaches a valley, and the contradictions of property and exchange decide who
inside the valley bears it.

### Essay outline

| Section | Words |
| --- | --- |
| Introduction and question | 400 |
| Sources, method and the two valleys | 500 |
| The herding cycle in both valleys, 1881 to 1961 | 600 |
| Flocks, pastures and forest rights | 700 |
| Trade: Tibet against the plains | 700 |
| Change by 1961: permits, roads, the closed border | 500 |
| Interpretation: the Annales frame and the contradictions within it | 400 |
| Conclusion | 200 |
| **Total** | **4,000** |

### Timeline

The essay is due on 4 November 2026. The earlier dates are a proposal.

| Stage | Output | Proposed date |
| --- | --- | --- |
| 1. Research question | This document, agreed by the group | 4 October 2026 |
| 2. Analysis | Dataset, calendar, map, charts | 25 October 2026 |
| 3. Interpretation | Full essay draft | 1 November 2026 |
| Submission | Final essay | 4 November 2026 |

---

## Cautions

- **Table readings.** Earlier versions said the livestock tables for Chaupal,
  Nalag, Basal and Chaunri were too garbled to use. That judgement came from
  the extracted text. The PDF pages are readable (Chaupal, p. 48. Nalag, p. 31.
  Basal, p. 77. Chaunri, p. 34), and the figures above come from the page
  images. Shakrori's goat total is 53 on the page (Shakrori, p. 76). The "153"
  was an OCR error.
- **Chaupal's second column.** One column of Chaupal's Table 24 has no printed
  heading (Chaupal, p. 48). Its 107 animals may be sheep, but the page does not
  say so.
- **Kinnaur grazing dues.** Kanum, Kothi and Nachar do not state grazing fees.
  The Mahasu Handbook table (Mahasu, pp. 334 to 336) may fill this, but its OCR
  is damaged and the pages need reading from the image.
- **Colonial sources on Kinnaur herding.** The 1881 and Rose texts describe the
  Gaddi cycle but not the Kinnaur one. The long-term comparison is stronger
  for the Ravi valley.
- **Date of the border closure.** No source in the folder names 1962 or the
  date Shipki La closed. Kanum says only "India-China dispute" (Kanum, p. 51).
  The essay needs an outside source for the date.
- **Fall in flocks.** Permits and the 1958-59 disease are two possible causes
  (Newell, p. 38).
- **Text reuse.** Rose's passage on hill Gujjars (Rose, p. 346) repeats Barnes
  in the 1881 census (1881, p. 267), so it is not independent evidence.
- **Figures from extracted text.** Figures not marked (image) need checking
  against the page before they go into the essay.
