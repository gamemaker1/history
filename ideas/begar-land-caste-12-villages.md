# Who carried the load? Begar, land and caste in the Shimla Hill States, 1881 to 1961

Earlier versions are [candidate-topics.md](candidate-topics.md) (16 topics) and
[shimla-hill-states-sutlej.md](shimla-hill-states-sutlej.md) (Shimla, the hill states and the Sutlej). This
version turns ideas 4, 9 and 10 into one research question. The project brief
(`project.docx`) requires the question, the theory and the computational method
to come from the sources. It requires three documented stages: research
question, analysis, and historical interpretation. The sections below follow
those stages.

All quotes were checked against the extracted text in `text/`. OCR errors are
corrected in the quotes. Section 6 lists the file and line of each key quote.

---

## Stage 1. Research question

### The problem in the sources

Before 1948 the Shimla Hill States exacted *begar*, unpaid labour owed to the
state, mostly the carrying of loads. Every source layer records it, and every
layer names the same castes as the people who performed it.

- **1881, Ibbetson**, quoting Barnes on Kangra: the hill menial castes "are
  always first impressed for begar, or forced labour, and, in addition to
  carrying loads, have to provide grass for the camp." Ibbetson adds that in
  the Punjab hills begar "is exacted, not by heads but by hearths."
- **1910, Rose's Glossary**: *Karawak* means "a man whose duty it is to call
  people together for begar." "In the Simla Hills the term Karawak is generally
  applied to a Koli." In Sirmur "the term Koli is almost synonymous with
  'serf'."
- **1920, Mandi State Gazetteer**, reprinted in the 1961 Chauntra survey: "the
  rich and the strong escaped, the poor and the weak had to bear a double
  burden." The superior Rajput clans, non-agricultural Brahmans, Khatris and
  shopkeepers were exempt from the longest form of begar.
- **1961, Chaupal (Jubbal State)**: the lambardar's "other function was to
  provide forced labour to the Ruler." "A Halbandi was always a Koli. He used to
  collect begaris under orders of the village Lumbardar."
- **1961, Chergaon (Bushahr State)**: the halbandi "belonged to Harijan
  community" and "was supposed to do all work free of charge as desired by
  zaildar or lambardar. This was known as begar."

The 1948 merger into Himachal Pradesh removed the rajas and their officials.
The 1961 surveys report the end of begar: "Forced labour-begar ... no longer
exists" (Chergaon), "The bethu system has been abolished" (Shakrori), and "All
of them knew that forced labour had been abolished" (Kalath). The surveys also
show that the Kolis did not all gain land after 1948:

- **Chergaon**: "Out of the total 14 families of Kolis, only 5 families own land
  and the others are working as tenants to rich Thakur families."
- **Shakrori**: Harijans "have been allotted nautor lands on payment of a
  nominal price" but "their holdings are very small and also of an inferior
  quality." *Nautor* is waste land newly granted for cultivation.
- **Chaupal**: Kolis' "ancestors first got the land on lease ... and now
  gradually have become the owners."
- **Kanum**: Scheduled Castes "have to wait their turn at some distance if
  someone from the higher caste is taking water from the kuhl."

Shimla drew labour from the hills throughout this period. In 1881 Ladakhi
coolies worked "on the hill roads of Simla as navvies and quarrymen." In 1931
the town held 18,144 people in winter and 51,706 in summer, a factor of 2.85.
The Batal survey says that before independence villagers "sought employment in
these offices as peons and daftries" when the Government of India moved to
Shimla for the summer.

### Research question

> **Did the end of princely rule in 1948 change who worked for whom in the
> villages of the former Shimla Hill States? What happened to the Koli and other
> Scheduled Caste households who had carried the states' begar: did they gain
> land and leave unpaid service, or did the same division of labour continue as
> tenancy and wage work?**

Sub-questions:

1. **Before 1948.** Who owed begar, who organised it, who was exempt, and where
   did the labour go (the raja, the village deity, colonial Shimla, the
   roads)? Sources: 1881, Rose, the Mandi Gazetteer extract, and the
   retrospective passages of the 1961 surveys.
2. **In 1961.** In each village, how do land ownership, tenancy, landlessness,
   occupation and access to water differ between Scheduled Castes and the
   landholding castes (Rajput, Kanet, Brahmin, Thakur)?
3. **Change or continuity.** Where Scheduled Caste households gained land or
   left service, what caused it: the merger, the 1953 Himachal Pradesh
   Abolition of Big Landed Estates and Land Reforms Act, nautor grants, or road
   and forest wage work? Which new jobs, such as Simla offices or road gangs,
   went to which castes?

### Why the question fits both theories

The two theories predict different answers from the same evidence, so the
essay can test them against each other instead of only applying them.

| | Annales reading | Marxist reading |
| --- | --- | --- |
| What explains the pattern | Physical structure. Steep terrain, small terraced plots, scarce kuhl water and isolation fix how much land exists and who can hold it. | Relations of production. Begar is surplus labour taken from a class without land, through the chain raja, lambardar, halbandi. |
| The three time scales | Long term: land, water and terrain. Medium term: Shimla's seasonal economy (1819 to 1947) and the roads. Event: the 1948 merger. | Change in the mode of extraction: from begar and service tenure to rent and wages. |
| What 1948 should change | Little. The event sits on top of a structure the surveys still record in 1961. | The legal form of extraction. The test is whether the material basis, land, moved too. |
| Evidence that would support it | The same caste division of labour described in similar words in 1881, 1910, 1931 and 1961. Kuhl queues and separate water sources persisting. | Kolis moving from begar to wage labour on roads while landholders keep the land. Tenants remaining tenants (Chergaon) or becoming owners (Chaupal, Pangna). |

Both readings need the same dataset: households by caste, land, tenure and
occupation in each village, set against the 1881, 1910 and 1931 descriptions.

---

## Stage 2. Analysis: sources and computational method

### Village sample

Nine surveyed villages lay in Shimla Hill States before 1948. Three villages
outside those states serve as comparisons.

| Village | State before 1948 | Distance to Shimla (stated) | SC households | SC share | Begar in survey | Simla jobs in survey |
| --- | --- | --- | --- | --- | --- | --- |
| Chaunri (Junga) | Keonthal (capital) | 12 miles | 25 of 58 | 43.1% | no | yes |
| Shakrori | Bhajji | not stated | 14 of 60 | 23.3% | yes (bethu) | yes |
| Chergaon | Bushahr | 80 miles to Rohru, then 9 | 16 of 68 | 23.5% | yes | no |
| Chaupal | Jubbal | not stated | 17 of about 79 | about 21.5% | yes | no |
| Batal | Baghal | 45 km to Arki, then 1 | 11 of 140 | 7.9% | no | yes |
| Basal | Baghat | not stated | 45 of 119 | 37.8% | no | no |
| Kanum | Bushahr | 186 miles | 25 of 113 | 22.1% | yes | no |
| Nachar | Bushahr | 114 miles | 55 of 213 | 25.8% | no | no |
| Kothi | Bushahr | "four days" | 49 of 128 | 38.3% | no | no |
| *Shathla* | *Kotgarh, British* | *52 miles* | *13 of 69* | *18.8%* | *no* | *no* |
| *Kalath* | *Baghat, then Patiala* | *45 miles* | *3 of 8* | *n/a* | *abolition noted* | *no* |
| *Chauntra* | *Mandi* | *n/a* | *n/a* | *n/a* | *Gazetteer extract* | *n/a* |

SC counts sum each survey's caste table for Koli, Chamar, Lohar, Bhangi,
Doomna, Turi, Rehar, Badhi and the other castes the survey lists as Scheduled.
They are our arithmetic and need checking against the page images. Chaupal's
table has a blank cell, so its total is approximate. Shathla, Kalath and
Chauntra are comparisons. Shathla had no raja, and Chauntra supplies the begar
classification.

### Comparison with 1931

The 1931 Punjab census (Part II, Table II and Table XVII, figures read from the
page images) gives state totals and Hindu "Dagi and Koli" counts.

| State | Population 1931 | Dagi and Koli | Share | 1961 village share |
| --- | --- | --- | --- | --- |
| Bashahr | 104,389 | 26,298 | 25.2% | Chergaon 23.5, Kanum 22.1, Nachar 25.8, Kothi 38.3 |
| Keonthal | 48,093 | 12,274 | 25.5% | Chaunri 43.1 |
| Jubbal | 27,172 | 6,458 | 23.8% | Chaupal about 21.5 |
| Baghal | 26,352 | 1,889 | 7.2% | Batal 7.9 |

The categories differ. The 1931 column counts Dagi and Koli only. The 1961
column counts all Scheduled Castes. The 1931 caste table also totals 313,836
for the Simla Hill States against 330,850 in the population table, and we have
not found the reason. Chaunri's high share fits its role as a former capital
with service castes (Bhangi, Chamar, Darzi). Batal is a Brahmin village of 140
households, 119 of them Brahmin.

The 1931 occupation table (Table X) separates cultivating owners, tenants and
agricultural labourers by state. In Keonthal it records 7,156 male cultivating
owners and 3,301 male tenants. In Bashahr it records 20,184 owners and 98
tenants. Bashahr's figure of 98 tenants needs explaining, since Chergaon, also
in Bashahr, has Koli tenants in 1961.

### Computational method

These steps follow the kinds of lesson on programminghistorian.org, which the
brief names.

1. **Corpus preparation (done).** Text extraction with `pdftotext` for all
   PDFs with a text layer, and Tesseract OCR for Rose Vol. 2 (614 pages, 16
   blank). The 43 files in the 1961 zip reduce to 34 after removing 9
   duplicates by checksum.
2. **Keyword-in-context concordance.** Extract every occurrence of the labour
   vocabulary (begar, bethu, halbandi, karawak, coolie, Koli, Dagi, tenant,
   nautor, kuhl) with 20 words either side, tagged by source layer (1881, 1910,
   1931, 1961) and village. Count frequency per 10,000 words in each layer.
   This measures how the vocabulary of unfree labour gives way to the
   vocabulary of tenancy and wages.
3. **Structured village dataset.** One CSV row per village and caste group:
   households, land owned, tenant or owner, landless, main and secondary
   occupation, Simla or road employment, separate water source. The source
   tables are in each survey's economy chapter. The LLM-assisted extraction in
   `candidate-topics.md` can speed this up, and every row needs checking against the
   page image.
4. **Comparison tables and charts.** SC share, landlessness and tenancy by
   village against the 1931 state figures, and against distance from Shimla.
5. **Map.** Plot the 12 villages with their former state boundaries and
   distance from Shimla, using the 1961 Punjab Census Atlas as a base.
6. **Close reading.** Chergaon, Chaupal and Shakrori have the longest passages
   on begar, tenancy and the merger. Read them in full alongside the
   Chauntra Gazetteer extract.

---

## Stage 3. Historical interpretation (plan)

The essay argues from the dataset toward one of three findings:

- **Continuity.** Begar ended in law, but land, water and tenancy still divide
  the same castes in 1961. This supports the Annales reading.
- **Transformation.** Scheduled Caste households moved from unpaid service to
  wage work and tenancy, and in some villages to ownership, after 1948 and
  1953. This supports the Marxist reading of a change in the mode of
  extraction.
- **Divergence by village.** The outcome depends on factors the dataset can
  show, such as the state's land system, distance from Shimla, or road access.
  Chergaon and Chaupal already point in opposite directions.

The essay is 3,000 to 4,000 words. A possible outline:

| Section | Words |
| --- | --- |
| Introduction and question | 400 |
| Sources and method | 600 |
| Begar in the hill states, 1881 to 1948 | 800 |
| The villages in 1961: land, tenure, labour, water | 1,200 |
| Interpretation: Annales and Marxist readings compared | 700 |
| Conclusion | 300 |

### Timeline

The final essay is due on 4 November 2026. The dates for the earlier stages
are a proposal.

| Stage | Output | Proposed date |
| --- | --- | --- |
| 1. Research question | This document, agreed by the group | 4 October 2026 |
| 2. Analysis | Concordance CSV, village dataset, tables, map | 25 October 2026 |
| 3. Interpretation | Full essay draft | 1 November 2026 |
| Submission | Final essay | 4 November 2026 |

---

## Section 4. Supporting ideas kept from version 2

These remain available as context or as a narrower essay if the full question
proves too large.

- **Chaunri as a former capital.** The survey was written to study "its
  reduction from the capital of a princely state to an ordinary village." After
  1948 "all the State courts and offices located there had to be closed" and
  "the ruling family also shifted to Simla."
- **Shimla's electricity from Chaba.** The Chaba power house next to Shakrori
  has lit Shimla since 15 July 1913. The Shakrori villagers "had never hoped
  that they would ever see their homes electrified."
- **The Hindustan-Tibet Road.** Nachar and Kanum sit on the old mule road along
  the Sutlej. By 1961 road construction is the main wage work for landless
  Scheduled Caste households in Kanum, Nachar and Kothi.
- **Deities as landholders.** Rose records deity jagirs granted by the
  Kumharsain state, worth Rs. 506 for Kot Ishwar and Rs. 76-6-3 for Nag of
  Dhar. Shathla's villagers are tenants of Devta Chaturmukh on a 225-bigha
  jagir. Kothi's Chandika temple holds 87 acres let to tenants.

---

## Section 5. Gaps and cautions

- The Barnes passage on begar describes Kangra, not the Simla States.
  Ibbetson quotes it for the hills in general.
- No 1961 survey names the 1953 Act correctly. Pangna cites the "Abolition of
  Big Landed Estates and Land Reform Act, 1963," which is probably an error for
  1953.
- The 1881 per-state tables are unreadable in the OCR. The 1931 figures above
  come from the page images.
- The 1931 census found nothing on begar or on the Praja Mandal movements in
  the states.
- Rose has no passage on hill people working in Simla town.
- The surveys that mention Simla jobs (Chaunri, Batal, Shakrori) do not give
  the castes of the job holders. The village dataset needs to check this.

---

## Section 6. Source files and line references

The searchable text of every source is in `text/`, in four folders: `1881`,
`1931`, `1961` (34 files, duplicates removed) and `rose`. The line numbers
below refer to those files.

| Quote | File | Line |
| --- | --- | --- |
| "always first impressed for begar" | 1881 Results, pp 1-421 | 97520 to 97523 |
| begar "by hearths" | 1881 Results, pp 1-421 | 13349 to 13351 |
| Ladakhi coolies on Simla roads | 1881 Results, pp 1-421 | 17826 to 17828 |
| Karawak "generally applied to a Koli" | Rose Vol. 2 OCR | 36531 to 36545 |
| Koli "synonymous with 'serf'" | Rose Vol. 2 OCR | 36824 to 36831 |
| rickshaw coolies in Simla | 1931 Part I Report OCR | 39782 to 39786 |
| "Halbandi was always a Koli" | 1961 Chaupal | 4364 to 4370 |
| halbandi and begar | 1961 Chergaon | 5198 to 5204 |
| Koli tenants of Thakurs | 1961 Chergaon | 981 to 986 |
| nautor land "very small" | 1961 Shakrori | 3185 to 3190 |
| waiting turn at the kuhl | 1961 Kanum | 4455 to 4460 |
| "double burden" | 1961 Chauntra | 4294 to 4297 |
| peons and daftries in Simla | 1961 Batal | 1869 to 1872 |
