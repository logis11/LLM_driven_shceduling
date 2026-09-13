# Read R10-task-switching — independent primary-source read

Read date: 2026-09-13. All paths below are relative to `_dev/research/jioh/2026-09-13-verification/sources/`. Text was pulled out of the PDFs with pypdf (`<id>/*.txt` next to each PDF). Every table cell quoted below was checked against a rendered page image (ghostscript, `render/*.png`) wherever the pypdf output lost the table layout (CHI 2004 Tables 2, 3, 4, 5 and 6; CHI 2005 Table 3).

## Copies used

| source-id | Copy used (saved file) | Where it came from | What kind of copy | Notes |
|---|---|---|---|---|
| zhang-chb15 | **none (COPY UNREACHABLE)** | see the C-zhang section for every URL tried and its response | — | Only publisher metadata was saved: `zhang-chb15/crossref.json`, `zhang-chb15/elsapi.xml` (coredata only), `zhang-chb15/openalex.json` |
| gonzalez-chi04 | `gonzalez-chi04/gmark-CHI2004.pdf` (sha256 988981bfff2408ba…) | https://ics.uci.edu/~gmark/CHI2004.pdf (linked from the author's publications page ics.uci.edu/~gmark/Home_page/Publications.html) | Author-hosted PDF in the proceedings layout: running header "CHI 2004 \| Paper", printed page numbers 113–120, ACM copyright block | 8 pages |
| mark-chi05 | `mark-chi05/gmark-CHI2005.pdf` (sha256 ec8ae49c99e17ff6…) | https://ics.uci.edu/~gmark/CHI2005.pdf (same publications page) | Author-hosted PDF in the proceedings layout: header "CHI 2005 \| PAPERS: Take a Number, Stand in Line (Interruptions & Attention 1)", printed page numbers 321–330 | 10 pages |
| mark-chi08 | `mark-chi08/gmark-chi08-mark.pdf` (sha256 e562bd16eca40a2a…) | https://ics.uci.edu/~gmark/chi08-mark.pdf (same publications page) | Author copy; PDF title "Microsoft Word - chi1038-mark.doc"; **no printed page numbers** | 4 pages. Locators below are PDF pages 1–4; the proceedings range 107–110 comes from the bibliographic entry and is not printed on this copy |
| mark-chi14 | `mark-chi14/gmark-Focus_1.pdf` (sha256 bfaa317691c9e67b…) | https://ics.uci.edu/~gmark/Home_page/Publications_files/Focus%20_1.pdf (the link on the publications page for "Bored Mondays and Focused Afternoons"). `Focus%20.pdf` was byte-identical (same md5) and was deleted as a duplicate | Author copy carrying the ACM copyright block and "http://dx.doi.org/10.1145/2556288.2557204"; **no printed page numbers** | pypdf reads 10 pages. Locators are PDF pages |
| czerwinski-chi04 | Primary: `czerwinski-chi04/interruptionsnet-p175.pdf` (sha256 42aebba4b2371961…). Cross-check: `czerwinski-chi04/horvitz-taskdiary.pdf` (sha256 67d370e0c3d7d3cb…) | Primary: https://www.interruptions.net/literature/Czerwinski-CHI04-p175-czerwinski.pdf. Cross-check: http://erichorvitz.com/taskdiary.pdf (a co-author's site). ACM DL https://dl.acm.org/doi/pdf/10.1145/985692.985715 returned **403** | Primary copy is in the proceedings layout with printed page numbers 175–182 (Acrobat Distiller, PDF metadata dated 2004-04-21). The cross-check copy is a Word-to-PDF version with pages numbered 1–8 | Every figure quoted below appears with the same wording in both copies (checked by grep: "Eleven", "0.7 interruptions per task", "53 minutes", "(40%)", "50 task") |
| mark-gallup06 | Primary: `mark-gallup06/wayback-20060621124938-p1.html` + `mark-gallup06/wayback-20060621124958-p2.html` (the 2006 capture). Cross-check: `mark-gallup06/gallup-live.html` (live page fetched 2026-09-13) | Wayback: `web.archive.org/web/20060621124938id_/http://gmj.gallup.com:80/content/23146/Too-Many-Interruptions-at-Work.aspx` and `…/20060621124958id_/…/content/23146/2/Too-Many-Interruptions-at-Work.aspx`. Live: https://news.gallup.com/businessjournal/23146/too-many-interruptions-work.aspx (HTTP 200) | 2006 capture: two-page article, logo alt text "Gallup Management Journal", dated "June 08, 2006", subtitle "A GMJ Q&A with Gloria Mark". Live page: labelled "Business Journal", "June 8, 2006", one page | The interview wording quoted below is the same in both copies |
| swell-icmi14 | Paper: `swell-icmi14/ru-ICMI2014-paper_final_cr.pdf` (sha256 a10bffe9ea55cb66…). Dataset record: `swell-icmi14/dans-api.json` (sha256 fa6e6ee01d0246d4…), `swell-icmi14/datacite-dans-x55-69zp.json`, plus two small byte-range file samples | Paper: http://cs.ru.nl/~skoldijk/Papers/ICMI%202014%20paper_final_cr.pdf, linked as "[pdf]" from the author's dataset page http://cs.ru.nl/~skoldijk/SWELL-KW/Dataset.html (saved as `ru-dataset-page.html`). Dataset: https://ssh.datastations.nl/api/datasets/:persistentId/?persistentId=doi:10.17026/dans-x55-69zp and https://api.datacite.org/dois/10.17026/dans-x55-69zp | Camera-ready author copy ("final_cr"; pdfTeX, 2014-09-03); ACM copyright block; **no printed page numbers** (TNO repository record `tno-record.html` gives "Pages 291-298") | 8 PDF pages. The DANS HTML landing page sits behind an Anubis bot challenge, but the Dataverse JSON API answered normally |

Search disclosure: one WebSearch query (looking for the CHI 2004 diary-study PDF) included the three author surnames from the bibliographic entry. After that, queries used titles, DOIs and URLs only.

---

## zhang-chb15 — Zhang, Sun, Chai & Aghajan (2015), *Computers in Human Behavior* 49, 237–244

### Access attempts (these apply to every C-zhang topic)

| URL / service | Response |
|---|---|
| https://api.openalex.org/works/doi:10.1016/j.chb.2015.03.012 | 200. `open_access.oa_status: "closed"`, `any_repository_has_fulltext: false`. The only location listed is doi.org, with no PDF |
| https://api.semanticscholar.org/graph/v1/paper/DOI:10.1016/j.chb.2015.03.012 | 200. `isOpenAccess: false`, `openAccessPdf.status: "CLOSED"` |
| https://api.crossref.org/works/10.1016/j.chb.2015.03.012 | 200. Metadata only, with no abstract deposited. Its text-mining links point to the Elsevier API |
| https://api.elsevier.com/content/article/PII:S0747563215001983?httpAccept=text/plain | 429 `RATE_LIMIT_EXCEEDED` |
| same, `httpAccept=text/xml` | 200, but `<coredata>` only (`openaccess 0`, `openaccessArticle false`) and no article body |
| https://www.sciencedirect.com/science/article/abs/pii/S0747563215001983 (curl) | 403 |
| https://www.sciencedirect.com/science/article/pii/S0747563215001983 (WebFetch) | 403 |
| Wayback CDX `sciencedirect.com/science/article/pii/S0747563215001983*` | 2 captures (2024-04-30, 2025-07-11), both recorded with status 403 |
| Wayback CDX for the `…/abs/pii/…` URL and for `researchgate.net/publication/273790535*` | no captures |
| https://api.core.ac.uk/v3/search/works?q=doi:"10.1016/j.chb.2015.03.012" | returned a redirect / Cloudflare challenge page instead of JSON |
| https://ouci.dntb.gov.ua/en/works/98b2Wkx4/ | 200. Metadata and reference list only, no full text |
| https://web.stanford.edu/group/SOL/profile_tongda.html (first author's profile page, found by searching for the lab) | 200. Lists the paper with a link to ScienceDirect only. No PDF. The dissertation listed there is on a different topic (motion-sensor and mind-wave data) |
| WebSearch on the exact title (with "filetype:pdf" and with "full text") | results were only ScienceDirect, ResearchGate "Request PDF" (no file) and OUCI. Search-result summaries were **not** used as evidence |

### C-zhang-1 — study duration, number of subjects, log records, distinct processes, data provider, data availability
- (a) No verbatim passage: no copy of the article was obtained.
- (b) —
- (c) Search-result summaries mentioned subject and log-record counts. Under the reading rules those are not evidence, so they are not repeated here as findings.
- (d) **COPY UNREACHABLE** (see the access table).

### C-zhang-2 — reported task-switching distribution (which quantity follows which law) and the term for highly connected tasks
- (d) **COPY UNREACHABLE**.

### C-zhang-3 — average interval between task switches and the definition of a task switch
- (d) **COPY UNREACHABLE**.

### C-zhang-4 — whether per-user distributions or fitted parameters are published, or only aggregates and figures
- (d) **COPY UNREACHABLE**.

### C-zhang-5 — anything on stability of application sets versus process-level churn
- (d) **COPY UNREACHABLE**.

### C-zhang-6 — author list, title, volume and pages
- (a) No article copy. Publisher-deposited **metadata** (not article text), from `crossref.json`: title "A look at task-switching and multi-tasking behaviors: From the perspective of the computer usage among a large number of people"; authors (given, family) ("Tongda", "Zhang"), ("Xiao", "Sun"), ("Yueting", "Chai"), ("Hamid", "Aghajan"); `volume` "49"; `page` "237-244"; container "Computers in Human Behavior"; issued 2015-08. The Elsevier API coredata (`elsapi.xml`) gives `<prism:coverDisplayDate>August 2015</prism:coverDisplayDate>` and doi 10.1016/j.chb.2015.03.012.
- (b) Crossref work record and Elsevier article API coredata.
- (c) The bibliographic entry's authors, title, volume 49 and pages 237–244 match the publisher's metadata record. This was not checked against the article's own first page.
- (d) **COPY UNREACHABLE**. The bibliographic fields are consistent with the publisher metadata only.

---

## gonzalez-chi04 — González & Mark (2004), "Constant, Constant, Multi-tasking Craziness", CHI 2004, 113–120

### C-gonzalez-1 — average continuous time in a working sphere before switching, with and without brief disruptions; definition of a working sphere
- (a) Verbatim:
  - Definition (p. 117, left column): "We define a working sphere as a set of interrelated events, which share a common motive (or goal), involves the communication or interaction with a particular constellation of people, uses unique resources and has its own individual time framework. With respect to tools, each working sphere might use different documents, reference materials, software, or hardware. It is the whole web of motives, people, resources, and tools that distinguishes it from other working spheres."
  - Event definition that the spheres are built from (p. 115): "We coded our data into events that we defined as any continuous use of a device or engagement in an interaction with other individuals (e.g. phone conversation, using a spreadsheet with the PC, annotating documents, or talking “through the wall”)."
  - Table 4, "Avg. no. of working spheres (WS) per person, and avg. time spent in each WS per day (hour:min:sec)" (p. 117). Row "Central and Peripheral WS only": Average WS/day (sd) "9.81 (3.39)"; Avg. Time/WS (sd) "0:33:32 (0:50:59)"; Avg. Time / segment (sd) "0:11:28 (0:10:54)". Row "All / All": "12.81 (3.39)", "0:40:41 (0:50:58)", "0:13:49 (0:16:14)".
  - Text (p. 117): "An individual spent about 33 min. 32 sec. per working sphere; however it does not occur as a continuous period of time. Instead the individual attends to a working sphere in small periods of time that we call segments. People frequently switch from one working sphere segment to another. Table 4 shows that the actual average duration of a working sphere segment is quite short (11 min, 28 sec.)."
  - Without brief disruptions. Method (p. 118): "We used a criteria of two minutes after reviewing the data and decided that this would make a feasible heuristic to begin with. … Thus, a segment was considered as “continuous” even if people turned to another working sphere for less than two minutes." Table 5, "Avg. time per WS segment without “nonsignificant” disruptions (hour:min:sec)" (p. 117), row "Both / All": "0:12:18 (0:11:53)". Central Default "0:14:13 (0:12:55)", Central Urgent "0:16:24 (0:12:25)", Peripheral Default "0:09:03 (0:09:38)", Peripheral Urgent "0:07:41 (0:07:30)".
  - Abstract (p. 113): "people spend about 12 minutes in a working sphere before they switch to another." Discussion (p. 119): "people spend on the average eleven and a half minutes in continuous work on a project or theme before they switch to another. After removing what we considered to be “nonsignificant” disruptions, we found that these segments of time were not much longer, averaging somewhat longer than 12 minutes."
- (b) p. 115 (event definition); p. 117 (Table 4, Table 5, definition, segment text); p. 118 (two-minute criterion); p. 113 (abstract); p. 119 (discussion).
- (c) 14 workers were shadowed by a human observer who timed events to the second. The statistic is the **mean** duration of a working-sphere **segment**, i.e. one continuous stretch in a sphere before switching to another sphere. The table's "Avg. Time/WS" (33:32) is total time per sphere per day and is **not** a continuous stretch. Headline values: 11 min 28 s (sd 10:54) for central and peripheral spheres only; 13:49 when metawork, personal and unknown are included; 12 min 18 s (sd 11:53) once disruptions shorter than 2 minutes are ignored. The abstract's "about 12 minutes" is a rounding. The paper reports means and SDs only (see C-gonzalez-5).
- (d) **FOUND**.

### C-gonzalez-2 — average number of distinct working spheres per person per day
- (a) Verbatim (p. 117): "We identified that each person worked on an average of ten working spheres per day, during the three days of our observation. (Note that we observed a three-day “slice of time”, so it is possible that we did not count all the working spheres that an individual might have)." Table 4: "Central and Peripheral WS only" → Average WS/day (sd) "9.81 (3.39)". "All / All" → "12.81 (3.39)". The rows Metawork, Personal and Unknown each show "1 (0.0)". Abstract (p. 113): "People worked in an average of ten different working spheres."
- (b) p. 117, Table 4 and text; p. 113 abstract.
- (c) Mean 9.81 per day (sd 3.39) counting central and peripheral spheres. The "12.81" total adds metawork, personal and unknown, each counted as one sphere. Based on 14 people over 3 observed days.
- (d) **FOUND**.

### C-gonzalez-3 — average time on an event/task before switching
- (a) Verbatim: Table 2, "Average continuous time spent on events before switching (hour:min:sec)" (p. 116). Row "All events except “Formal meetings” and “Other”": % entire day "70.52%", Avg. Time/Day (sd) "0:45:56 (0:52:03)", Avg. Time/ Event (sd) "0:03:08 (0:02:27)". Row "All events total": "100%", "0:52:07 (0:55:25)", "0:08:55 (0:13:23)". Text (p. 116): "What was most surprising to us was that people spend on the average slightly over three minutes on an event (leaving out formal meetings, unknown, and personal events) before another event is initiated." Text (pp. 115–116): "Table 2 shows the average time spent on an event per person, per day, for all three roles combined (analyst, developer, managers). This time reflects the amount of time that people spent in continuous uninterrupted work on events." Abstract (p. 113): "People average about three minutes on a task".
- (b) pp. 115–116, Table 2.
- (c) The unit is the **event**: one continuous use of a device, or one interaction with someone, observed by a shadowing researcher. It is not a working sphere and not an application window. Mean 3 min 08 s (sd 2:27), excluding formal meetings and "Other". Including every event, the mean is 8 min 55 s. The abstract's word "task" refers to this event-level figure.
- (d) **FOUND**.

### C-gonzalez-4 — average time using one electronic tool or paper document before switching
- (a) Verbatim: Table 3, "Average time usage per device per person (hour:min:sec)" (p. 116). Row "All devices⁴": % entire day "51.59%", % of device usage only "100%", Avg. Time/Day (sd) "0:44:57 (1:13:27)", Avg. Time/Event (sd) "0:02:11 (0:01:52)". Footnote 4: "Weighted average". Row "PC¹": "37.01", "72.37", "3:12:52 (1:13:48)", "0:02:52 (0:00:51)"; footnote 1 "Includes using email". Text (p. 116): "Table 3 shows the length of time that people spent using different electronic devices and paper documents before they were interrupted or switched to another activity. People spent an average of 2 min. 11 sec. working with any device or paper before they switched to another device or event." Discussion (p. 119): "people spend on the average somewhat more than two minutes on any use of electronic tool, application, or paper document before they switch to use another tool. The longest duration of tool use is with PCs, yet this averages only slightly more than three minutes at any one time."
- (b) p. 116, Table 3; p. 119.
- (c) Weighted mean 2 min 11 s (sd 1:52) per stretch of continuous use of one device or paper item. The PC counts as one "device" (email included), so this does **not** measure switching between application windows. Caveat: the discussion says PC use averages "slightly more than three minutes", but Table 3 shows 0:02:52 and Table 2 shows 0:02:53 for PCs.
- (d) **FOUND**.

### C-gonzalez-5 — study population (roles, organization, sample size); distributions or only averages
- (a) Verbatim (p. 114): "we conducted an observational study at ITS¹, an investment management company located on the west coast of the U.S. ITS acts as an outsourcer, providing information technology and accounting services for a major fund manager. … More than 250 employees work at the ITS branch where we conducted the study. We concentrated our work on the day-to-day operations of one team that we call the JEB team. … Twenty-five information workers form the team including software developers, database administrators, financial analysts, and managers." Footnote 1: "This name, and all other names, are pseudonyms." Method (p. 114): "The study was based on two main ethnographic techniques: participant observation and use of long interviews. … we decided to use a “shadowing” observation technique". p. 114: "A total of 477 hours was spent in observation at the field site." p. 115: "Fourteen people were observed over a seven-month period. Each person was observed for a period of three and a half days. … the average time of formal observation for each individual was 26 hours. Some days after the observation we conducted a two-hour semi-structured long interview". p. 115: "six of these were business analysts … Four team members were developers … Four individuals were managers". Limitations (p. 120): "Our observations are limited to one fieldsite. … We also only observed 14 people."
- (b) pp. 114–115, 120.
- (c) N = 14 (6 analysts, 4 developers, 4 managers) from one 25-person team at one US financial IT outsourcing firm. Human shadowing with to-the-second timing, plus interviews. Every table gives **means with SDs**. Role comparisons use ANOVA and Tukey tests. I searched the text for "median", "distribut", "histogram", "skew" and "percentile" and found no median, percentile or distribution plot; the only "distribution" hits are about time-distribution studies in the literature.
- (d) **FOUND**.

### C-gonzalez-6 — interruption statistics (frequency, source)
- (a) Verbatim: Table 6, "Avg. number and types of interruptions per day" (p. 118; columns Type / Average Interruptions per day (S.D) / % all types / Internal / External).
  - Internal rows: "Checking/Using Paper Docs 0.52 (0.86) 1.87"; "Checking/Using Computer 1.54 (1.47) 10.98"; "Talking t/wall 1.93 (2.15) 6.89"; "Phone call 1.14 (1.56) 4.09"; "Email use 1.04 (1.47) 7.40"; "Leaves cubicle 5.00 (2.56) 17.87%". Internal share "49.11%".
  - External rows: "New email notif. 3.55 (3.18) 12.68%"; "Person arrives 6.00 (3.03) 21.45%"; "Status on terminals 0.36 (0.82) 1.28%"; "Phone ringing 2.62 (2.01) 9.36%"; "Voice message light 0.19 (0.45) 0.68%"; "Call through wall 1.33 (1.75) 4.77%"; "Reminder notification 0.19 (0.40) 0.68%". External share "50.89%".
  - "Total 25.40 (8.23) 100% 100%".
  - Text (p. 118): "An Internal interruption refers to self-initiated switching among working spheres. An External interruption is a condition in the environment that motivates switching." "Our data confirms previous studies indicating that people interrupt themselves as often as they are interrupted [12]." "About two-thirds of the time people resume work in their working sphere after interruption. Most “significant” interruptions can range from two minutes up to 40 minutes. About one-third of the time people switched to another working sphere without returning to the first working sphere." "With external interruptions, individuals switch between working spheres more often due to verbal-based interruptions (such as visitors or phone calls) than to notification mechanisms from their e-mail or voice mail."
- (b) p. 118, Table 6 and the section "External and internal interruptions".
- (c) Mean of 25.40 interruptions per person per day (sd 8.23), from observation. Internal (self-initiated) 49.11%, external 50.89%. The largest single sources are "Person arrives" (21.45%) and "Leaves cubicle" (17.87%). Caveat from my own arithmetic, not the paper: the "% all types" values are not the row mean divided by 25.40. Most rows equal roughly mean × 3.57, which implies a denominator near 28, and two internal rows ("Checking/Using Computer", "Email use") are about double that ratio. So the percentages were probably computed from pooled counts and cannot be derived from the means.
- (d) **FOUND**.

### C-gonzalez-7 — cross-reference of C-gonzalez-1, -3, -4 and C-mark08-1
- (a)/(b) The figures and their exact homes:

| Figure | Unit measured | Paper and locator |
|---|---|---|
| 0:03:08 (sd 0:02:27) | event (continuous device use or interaction), excluding formal meetings and "Other" | González & Mark CHI 2004, Table 2, p. 116 |
| 0:02:11 (sd 0:01:52) | continuous use of one device or paper item (weighted) | González & Mark CHI 2004, Table 3, p. 116 |
| 0:11:28 (sd 0:10:54) | working-sphere segment, central and peripheral spheres | González & Mark CHI 2004, Table 4, p. 117 |
| 0:12:18 (sd 0:11:53) | working-sphere segment, ignoring disruptions under 2 min | González & Mark CHI 2004, Table 5, p. 117 |
| 11 min 4 sec (sd 18 min 9 sec) | working-sphere segment, central and peripheral, 24 informants | Mark, González & Harris CHI 2005, p. 324 (see C-mark05-1) |
| none of the above | — | Mark, Gudith & Klocke CHI 2008 is a lab experiment and has no time-per-event, time-per-device or time-per-working-sphere figures (see C-mark08-1) |

- (c) The event, device and working-sphere durations belong to the 2004 and 2005 field studies. The CHI 2008 paper only cites the 2004 study (its ref [6]) as the basis for its 2-minute interruption interval.
- (d) **FOUND**.

---

## mark-chi05 — Mark, González & Harris (2005), "No Task Left Behind?", CHI 2005, 321–330

### C-mark05-1 — average time in a working sphere before switching
- (a) Verbatim (p. 324): "The average length of time that the informants spent in central and peripheral working spheres was 11 min. 4 sec., (sd=18 min. 9 sec.) before switching to another working sphere or being interrupted." p. 325: "The majority of working spheres are interrupted and people spend about 11 minutes in a working sphere before switching to another." Table 4 (p. 327), "Overview" row, "Time spent in WS" column: "11 min. before switching". Sub-results: p. 324–325 "segments that were interrupted lasted significantly longer (12 min. 40 sec., sd=14 min. 33 sec.) than those not interrupted (8 min. 58 sec, sd=14 min. 43 sec.)". p. 325 "collocated people spend longer, on average, in a working sphere (11 min. 56 sec., sd=15 min. 33 sec.) compared to distributed people (9 min. 56 sec., sd=13 min. 29 sec.)". Sample (p. 323): "Twenty-four people in total were observed in detail: 7 managers, 9 analysts, and 8 developers."
- (b) pp. 323–325, 327 (Table 4).
- (c) Shadowing observation of 24 people, including the 14 from the 2004 study (p. 323: "Fourteen members from the JEB team were shadowed and in the second phase ten members of the AUG team were shadowed"). The statistic is the mean duration of a working-sphere **segment** in central and peripheral spheres: 11:04, sd 18:09, a wide spread. The segment count is N = 2246 (Table 1). Caveat: the morning figure is printed as "10 min. 72 sec." (p. 327), a malformed value in the source.
- (d) **FOUND**.

### C-mark05-2 — proportions of self-initiated (internal) vs external interruptions, overall and by job role
- (a) Verbatim:
  - Table 3, "Percent of internal/external interruptions according to the source of the interruption. Data in parentheses are percentages within internal/external. N=1282." (p. 326). Columns Internal / External / Total (row avg.):
    - "Central WS 38.0% (28.8%)* | 62.0% (43.3%) | 100% (36.3%)"
    - "Peripheral WS 20.0% (7.6%) | 80.0% (28.2%) | 100% (18.3%)"
    - "Other WS (personal, metawork, unknown) 67.3% (63.6%) | 32.7% (28.5%) | 100% (45.3%)"
    - "Column avg. 52.0% | 48.0% | 100%"
  - By role (p. 326): "There is a significant difference of internal/external interruptions and work role. Managers are more likely to experience external interruptions (59.2%) than internal interruptions (40.8%), whereas analysts and developers experience internal and external interruptions about equally, X2(2)=.10.1, p<.006." (The superscript and subscript are flattened here; the source prints "X²₍₂₎=.10.1".)
  - Scope (p. 324): "In analyses in this paper we focus only on interruptions outside of one’s current working sphere context".
  - Definition (p. 322): "External interruptions are those that stem from events in the environment … Internal interruptions are those in which one stops a task of their own volition."
  - Discussion (p. 328): "in other work roles (developers and analysts), people were just as likely to interrupt themselves as to be externally interrupted."
- (b) p. 322 (definitions), p. 324 (scope), p. 326 (Table 3 and role result; checked on the rendered image), p. 328.
- (c) Overall, from Table 3's "Column avg." row: 52.0% internal and 48.0% external, over 1,282 interruptions that took a person out of their current working sphere. By role, numbers are given **only for managers** (40.8% internal, 59.2% external). Analysts and developers are described only as "about equally", with no percentages. **Consistency caveat (my arithmetic, not stated by the paper):** the cells do not reproduce the "Column avg." row. Take internal share = x. Central row: 0.288·x / 0.363 = 0.380 gives x ≈ 0.48. Peripheral: 0.076·x / 0.183 = 0.200 gives x ≈ 0.48. Other: 0.636·x / 0.453 = 0.673 gives x ≈ 0.48. So the row and column percentages imply about **48% internal and 52% external**, the reverse of the printed "52.0% / 48.0%". Either the column-average row has its two values swapped, or some other cells are wrong. The paper does not resolve this. Separately, the earlier González & Mark CHI 2004 paper (Table 6) reports 49.11% internal and 50.89% external for its 14-person sample.
- (d) **PARTIAL**: the overall split is present but internally inconsistent; by role, only managers get numbers.

### C-mark05-3 — does the 2005 paper state what fraction of switches/interruptions are self-initiated?
- (a) Verbatim: Table 3 "Column avg. 52.0% 48.0% 100%" (Internal / External; see C-mark05-2). p. 324: "we found that 57.1% of all informants’ working sphere segments were interrupted, on the average." Table 1 (p. 324) "Column avg (57.1%) (42.9%) 100%" for Interrupted / Not Interrupted, "N=2246". Resumption, not switching (p. 327): "Of interrupted work that was resumed on the same day, only a small proportion was due to externally initiated resumptions (9.9%) compared to work that was resumed by one’s self (90.1%)."
- (b) pp. 324, 326, 326–327.
- (c) The paper gives an internal share of **interruptions**: 52.0% as printed, with the inconsistency described in C-mark05-2. It gives **no** self-initiated share of **all working-sphere switches**. 42.9% of segments were not interrupted at all; they ended when work in the sphere was finished, and the paper does not classify those endings as self- or externally initiated. The 90.1% figure is the share of **resumptions** that were self-initiated, not the share of switches.
- (d) **PARTIAL**: stated for interruptions, not for switches in general.

---

## mark-chi08 — Mark, Gudith & Klocke (2008), "The Cost of Interrupted Work: More Speed and Stress", CHI 2008

### C-mark08-1 — study design; does it report time-per-task or time-per-working-sphere figures?
- (a) Verbatim:
  - Design (PDF p. 2): "A 3x2 factorial experimental design was used. The within-subject factor was interruption context with three levels: no interruption (B, baseline), same-context interruption (S), and different-context interruption (D). … The between-subjects factor was media type: subjects were interrupted with telephone or IM."
  - Participants: "Forty-eight subjects participated. 81% of subjects were German university students with a mean age of 26".
  - Task: "We simulated an office environment in the lab and chose an email task … For each interruption type condition, subjects had to answer 12 emails."
  - Interruption interval: "Interruption frequency was set to two minutes, based on observations from [6] and the pilot experiments." Ref. [6] (PDF p. 4) is "Gonzáles, V. & Mark, G. Constant, constant, multi-tasking craziness: managing multiple working spheres. Proceedings of CHI ‘04, (2004), 113-120."
  - DV: "Our primary variable of interest was the total time to perform the task. … The time to perform the task was computed as [total time to perform task – time spent on interruptions]."
  - Table 1 (PDF p. 3), "Mean measures of task performance (s.d.)", column "Time to perform task* (minutes)": Baseline "22.77 (7.60)", Same context "20.31 (5.94)", Different context "20.60 (4.93)".
  - Discussion (PDF p. 4): "After only 20 minutes of interrupted performance people reported significantly higher stress, frustration, workload, effort, and pressure."
- (b) PDF pp. 2–4 (author copy with no printed page numbers).
- (c) Laboratory experiment, N = 48, mostly students, with a simulated email task. The only time figures are minutes to finish a block of 12 emails, minus the time spent on interruptions, plus NASA-TLX ratings. There is **no** field time-per-task, time-per-event or time-per-working-sphere measurement, and no resumption-lag figure (I searched for "23", "resum", "min" contexts). The "20 minutes" in the discussion is roughly how long a block took, not a resumption time.
- (d) **FOUND** (design located; no time-per-task or time-per-working-sphere figures reported).

---

## mark-chi14 — Mark, Iqbal, Czerwinski & Johns (2014), "Bored Mondays and Focused Afternoons", CHI 2014

### C-mark14-1 — what it reports about attention over the day; does it state the share of self-initiated switches?
- (a) Verbatim:
  - Method (PDF p. 4): "We conducted an in situ study in the fall of 2012 at a large U.S. corporation. We used a mixed-methods approach where we combined automatic data collection of digital activity with experience sampling." "Thirty-two people (17 females, 15 males) participated. Participants included researchers (15), managers, administrators, an engineer, a department director, a designer, and a consultant." "This included beginning and end times for the lifespan of every window, and the beginning and end times for every instance of every foreground window."
  - Data volume (PDF p. 5): "We collected data on each of the 32 participants for 5 days each, for a total of 160 person-days, or 1,509 hours of data collection. Our computer logging software collected 91,409 computer window switches. We collected 2,809 experience sampling probes."
  - Day rhythm (PDF p. 6): "Overall, participants report being more focused than bored in the workplace. People are most focused in their work mid-afternoon, with a peak at 2-3 p.m. when the use of productivity apps (e.g., Word, Excel, Visual studio), Email, and viewing the Inbox/Calendar app are at their highest usage. Focus is also high at 11 a.m., which is generally". PDF p. 7 continues: "before a break for lunch, when the reports then dip. After peaking mid-afternoon, Focus reports continue to decline until when most people typically leave work. The majority of participants report being most Bored at the beginning of the day (9 a.m.), and Bored reports peak at 1 p.m. Boredom is at the lowest at 2 p.m."
  - Weekday (PDF pp. 7–8): "Win Switches were significantly higher on Monday (M=661.2 switches/day, SE=69.60) than Friday (M=390.7 Win switches/day, SE=28.7)". The text of this sentence is split by the Figure 3 caption in the PDF.
  - Discussion (PDF p. 9): "Thus, our work raises the question: it may not be the interruptions that break focus; it may be that lack of focus comes first, leading to susceptibility to interruptions."
- (b) PDF pp. 4–9 (author copy with no printed page numbers); Figure 2 on PDF p. 6.
- (c) 32 information workers at one US corporation, 5 workdays each. Windows foreground-window logging was combined with pop-up self-reports of engagement and challenge, which the authors grouped into "Focus", "Rote" and "Bored". Time-of-day results are counts of self-reports averaged over subjects and days (Figure 2, with exact values only in the graphic). Window switches are logged counts, e.g. per-day means by weekday and counts in the 10 minutes before each probe. **Self-initiated share:** I searched the full text for "self-init", "self init", "self-interrupt", "initiat", "internal" and "external". No hit concerns the origin of switches ("internal" and "external" appear only for mindfulness, validity and a citation). The paper does not classify window switches as self- or externally initiated and states no such share.
- (d) **PARTIAL**: the attention-over-the-day findings were FOUND; the share of self-initiated switches was NOT FOUND (full-text search as listed).

---

## czerwinski-chi04 — Czerwinski, Horvitz & Wilhite (2004), "A Diary Study of Task Switching and Interruptions", CHI 2004, 175–182

### C-czerwinski-1 — method and main task-switching/interruption findings
- (a) Verbatim:
  - Method (p. 176): "Eleven experienced Microsoft Windows™ users (3 female) participated in the study. All of the participants reported multitasking among more than three major projects or tasks (as defined by the users) on the job … Participants’ occupations spanned a spectrum of domains, including a stock broker, professor of Computer Science, web designer, software developer, boat salesman, and network administrator." "A Microsoft Excel XP™ spreadsheet, with worksheets for each day of the week and another for participant instructions, were created with columns for each tracked parameter." "We were careful not to instruct the participants about what they should consider tasks to be—we asked them to define them for us."
  - Exclusion (p. 177): "One outlier participant was removed from the rest of the analyses because the subject did not switch among more than two tasks on any given day of the week".
  - Task types (p. 178): "45% of the reported tasks in participants’ diaries were described as project-related or routine tasks that comprised the participants’ jobs. We found that 23% of the tasks reported could best be described as “email.” … participants reported “task tracking” as comprising 13% of their reported task switches."
  - Interruptions (p. 178): "users reported an average of 0.7 interruptions per task, almost a one-to-one interruption to task ratio! This should also be taken as a conservative estimate".
  - Task length (p. 178): "Reported task lengths averaged 53 minutes, with a large standard deviation of 90.9 minutes. The distribution of task lengths was highly negatively skewed, with the majority of the tasks reported being shorter than the average length."
  - Switch initiators (p. 178): "We found that the largest category of task switches (40%) were self initiated … 19% of the task switches were simply moving on to a new task that was on a to-do list … Telephone calls prompted 14% of the reported task switches, while meetings and appointment reminders prompted another 10%. Deadlines and emergencies accounted for only 3% … Email content prompted task switches in 3% of the reported cases, and a new information need or request from a colleague or client prompted another 3%."
  - Returned-to tasks (p. 179): "average task length = 120 minutes v. 45 minutes, respectively"; "returned-to tasks comprised 4.5 hours out of a 40 hour work week, or 11.25% of a user’s work week"; "(1.5 interruptions, on average, v. 0.7, respectively)".
  - Discussion (p. 179): "Participants in our study reported an average of 50 task shifts over the week."
- (b) pp. 176–179; Figure 2 and Figure 3 on p. 178.
- (c) Self-report diary kept for one work week by 11 people, analysed for 10. The unit is a **user-defined task**, and granularity varies by person (p. 176: "different participants in the study chose to encode “task switches” at different levels of detail"). Reported task duration: mean 53 min (SD 90.9). Mean of 50 task shifts per person over the week. 40% of switches self-initiated. Mean 0.7 interruptions per task. Caveats: (1) the text calls the distribution "negatively skewed" yet says most tasks were shorter than the mean, which describes a right (positive) skew; (2) the Figure 3 pie labels ("Appointment 9%", "Deadline 2%", "Emergency 1%", "Return to Task 7%") do not add up exactly to the text's groupings ("meetings and appointment reminders … 10%", "Deadlines and emergencies … 3%"); (3) only means and SDs are reported, apart from the skew remark.
- (d) **FOUND**.

---

## mark-gallup06 — "Too Many Interruptions at Work?" Q&A with Gloria Mark, Gallup Management Journal, 2006-06-08

### C-gallup-1 — does the interview state a time to resume an interrupted task, and its value; does that figure appear in the Mark et al. CHI papers?
- (a) Verbatim (interview; same wording in the 2006 capture, page 2, and in the live page):
  - "GMJ: How long does it take to get back to work after an interruption? Mark: There's good news and bad news. To have a uniform comparison, we looked at all work that was interrupted and resumed on the same day. The good news is that most interrupted work was resumed on the same day -- 81.9 percent -- and it was resumed, on average, in 23 minutes and 15 seconds, which I guess is not so long."
  - "There are about two intervening tasks before you go back to your original task".
  - Other interview figures (2006 capture, page 1): "we shadowed 36 managers, financial analysts, software developers, engineers, and project leaders for three days"; "three minutes and five seconds, on average"; "2 minutes and 11 seconds"; "each person worked on an average of 12.2 different working spheres every day. We also found that they switched working spheres, on average, every 10 minutes and 29 seconds"; "people still worked 12 minutes and 18 seconds in a working sphere before switching"; "They interrupted themselves about 44% of the time."
  - Masthead of the 2006 capture: logo alt text "Gallup Management Journal"; "June 08, 2006"; "A GMJ Q&A with Gloria Mark". Byline: "-- Interviewed by Jennifer Robison".
  - Closest CHI 2005 passages (p. 326): "77.2% of interrupted work was resumed on the same day." "When people did resume work on the same day, it took an average length of time of 25 min. 26 sec (sd=54 min. 48 sec.). … our informants worked in an average of 2.26 (sd=2.79) working spheres." Also: "(82.0%)" for interrupted **central** working spheres resumed the same day; "22 min. 37 sec." for externally interrupted spheres; "29 min. 1 sec." for internally interrupted ones. p. 327: "21 min. 28 sec." for self-resumed spheres and "61 min. 37 sec." for externally resumed ones.
- (b) Interview: 2006 capture page 2 (`wayback-20060621124958-p2.html`) and live page. CHI 2005: pp. 326–327.
- (c) The interview states a same-day resumption time of **23 min 15 s** (mean), with 81.9% resumed the same day. **This figure is not in any of the four Mark et al. CHI papers read here.** I searched the full text of González & Mark CHI 2004, Mark et al. CHI 2005, Mark et al. CHI 2008 and Mark et al. CHI 2014 for "23 min", "15 sec", "81.9" and "resum", using both line-by-line and whitespace-normalised text. CHI 2005 has the comparable measure with **different values**: 25 min 26 s and 77.2%. CHI 2004 reports only that "About two-thirds of the time people resume work" (p. 118), with no time. CHI 2008 and CHI 2014 have no resumption-time figure. The interview also describes 36 shadowed people, which matches neither CHI 2004 (14) nor CHI 2005 (24). Its "12.2" spheres, "10 minutes and 29 seconds" and "44%" match neither paper's tables (CHI 2004: 9.81 or 12.81, 11:28, 49.11% internal; CHI 2005: 11.7, 11:04, 52.0% internal as printed). Its "12 minutes and 18 seconds" equals CHI 2004 Table 5, "2 minutes and 11 seconds" equals CHI 2004 Table 3, and "three minutes and five seconds" is close to but not equal to CHI 2004 Table 2 (0:03:08). The interview appears to draw on a larger or later pooled dataset that none of these papers reports. Note on the bibliographic entry: it names the venue "Gallup Business Journal", which is the live page's label; the 2006 original was branded Gallup Management Journal.
- (d) **FOUND** in the interview; the figure is **not** in the CHI papers (full-text search as listed).

---

## swell-icmi14 — Koldijk, Sappelli, Verberne, Neerincx & Kraaij (2014), SWELL-KW dataset, ICMI 2014

### C-swell-1 — participants, conditions, logged modalities (including application names / window switching), access terms
- (a) Verbatim (paper):
  - Participants (PDF p. 4, §3.7): "25 students participated in our experiment, of which 8 were female and 17 male. The average age was 25 (standard deviation 3.25). Most participants were native Dutch. They were interns from TNO and students from Delft University of Technology who were approached by advertising."
  - Conditions (PDF p. 3, §3.1): "• Neutral: the participant was allowed to work on the tasks as long as he/she needed. After a maximum of 45 minutes the participant was asked to stop and told that enough data of ‘normal working’ was collected. • Stressor ‘Time pressure’: the time to finish all tasks was 2/3 of the time the participant needed in the neutral condition (and maximally 30 minutes). • Stressor ‘Interruptions’: 8 emails were sent to the participant during the task." And: "All participants worked under all 3 conditions. The neutral condition was always the first condition … The order of the two stressor conditions was counterbalanced". Figure 1 caption: "For 13 participants order A was used, for 12 participants order B."
  - Setting (PDF p. 4, §3.4): "Participants performed their tasks on a computer (Dell Latitude E6400) with Windows 7 Professional … Office 2010 was installed, which the participants used for email (Outlook), report writing (Word) and making presentations (Powerpoint). As a browser, Internet Explorer was used". §3.2: "The participants performed knowledge worker tasks on a desktop computer in a controlled lab setting."
  - Sensors (PDF p. 4, §3.6): "Computer interactions were logged with the key-logging application uLog (version 3.2.5, by Noldus Information Technology)". Also video analysed with FaceReader, a Kinect depth camera, and "ECG was recorded using a Mobi device (TMSI)" plus skin conductance.
  - Raw computer logs (PDF p. 5, §4.2): "The computer logging software recorded detailed timestamped information in XML format about each computer event. Examples of computer events are mouse clicks, mouse scrolls and application changes."
  - Table 2 (PDF p. 5), "Computer interaction features (aggregated per minute)", Applications rows: "AppChanges Number of application changes"; "TabfocusChange Number of tab focus changes".
  - Feature data (PDF p. 5, §4.1): "Per participant three times 6 minutes relaxation data are included, ca. 45 minutes of working under normal conditions, ca. 45 minutes working with email interruptions and ca. 30 minutes working under time pressure."
  - Availability (PDF p. 2): "we will make the anonymized dataset available for access by the scientific community". PDF p. 8: "More information on the dataset and its access can be found at http://persistent-identifier.nl/?identifier=urn:nbn:nl:ui:13-kwrv-3e".
  - Author's dataset page (`ru-dataset-page.html`): "The dataset can be accessed medio 2015 here: SWELL-KW dataset."
- (a) Verbatim (current DANS record, `dans-api.json` and DataCite JSON, fetched 2026-09-13): `"license": {"name": "CC-BY-NC-SA-4.0", …}`; `"termsOfAccess": "N/a"`; `"fileAccessRequest": false`; `"versionNumber": 4`, `"versionMinorNumber": 1`; `"releaseTime": "2025-06-04T08:57:35Z"`. DataCite `rightsList` includes `"info:eu-repo/semantics/openAccess"` and "Creative Commons Attribution Non Commercial Share Alike 4.0 International". Of 919 files, the `restricted` flag is true for 0.
- (b) Paper PDF pp. 2–5, 8 (TNO record: proceedings pp. 291–298); DANS Dataverse API and DataCite record for DOI 10.17026/dans-x55-69zp.
- (c) 25 students or interns (lab setting, not in-situ workers), about 3 hours each, three within-subject conditions: neutral first, then interruptions and time pressure in counterbalanced order, with relaxation phases. Modalities: uLog computer interaction (mouse, keyboard, application and tab-focus changes), FaceReader facial features, Kinect posture, and ECG-derived heart rate, HRV and skin conductance; also questionnaires (NASA-TLX, RSME, SAM, stress VAS). **Application names:** the paper mentions "application changes" events and per-minute AppChanges and TabfocusChange **counts**, but never says outright that application names are recorded. Dataset evidence (not the paper): I fetched a 40 KB byte range of the raw file `a_pp1_c1_uLog_20120918_131425.xml` anonymously. It contains `<EventAction>Window Activated</EventAction>` events and a `<ControlApplication>` element with process or application names (e.g. `<ControlApplication>explorer</ControlApplication>`, `<ControlApplication>uLog 3.2</ControlApplication>`). The per-minute feature CSV header includes `SnAppChange,SnTabfocusChange`. **Access:** the current DANS record is CC BY-NC-SA 4.0, labelled open access, with no restricted files and no access-request requirement. Anonymous downloads of two files returned HTTP 206 from the object store without login. **The bibliographic entry's "(registration required)" is not supported by the current record.** Earlier dataset versions may have had other terms; the record was updated 2025-06-04, and I did not examine earlier versions.
- (d) **FOUND**, with a discrepancy: the current access terms contradict "(registration required)", and application names are evidenced by the dataset files rather than stated in the paper.

---

## Verdict counts (one verdict per topic; 21 topics)

| Verdict | Count | Topics |
|---|---|---|
| FOUND | 12 | C-gonzalez-1, C-gonzalez-2, C-gonzalez-3, C-gonzalez-4, C-gonzalez-5, C-gonzalez-6, C-gonzalez-7, C-mark05-1, C-mark08-1, C-czerwinski-1, C-gallup-1 (found in the interview; the figure is absent from the CHI papers), C-swell-1 (with the access-terms discrepancy) |
| PARTIAL | 3 | C-mark05-2 (overall split printed but internally inconsistent; by role, numbers only for managers), C-mark05-3 (share given for interruptions, not for all switches), C-mark14-1 (day rhythm found; self-initiated share not in paper) |
| NOT FOUND | 0 | none as a whole-topic verdict. Sub-parts not found: the self-initiated share in CHI 2014; the 23 min 15 s figure in the four CHI papers |
| PREMISE NOT IN SOURCE | 0 | — |
| COPY UNREACHABLE | 6 | C-zhang-1, C-zhang-2, C-zhang-3, C-zhang-4, C-zhang-5, C-zhang-6 |

Unreachable copy: Zhang, Sun, Chai & Aghajan (2015), *Computers in Human Behavior* 49, 237–244 (DOI 10.1016/j.chb.2015.03.012). No open-access copy exists per OpenAlex and Semantic Scholar. ScienceDirect returned 403, the Elsevier API returned 429 or metadata only, the Wayback captures are 403 pages, and the first author's profile page links only to ScienceDirect.
