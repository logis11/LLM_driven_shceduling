# Reader output R09-tabs

Read date: 2026-09-13. All paths below are relative to `_dev/research/jioh/2026-09-13-verification/sources/`.

## Copies used

| source-id | copy | origin | identity check | sha256 |
|---|---|---|---|---|
| dubroy-chi10 | `dubroy-chi10/dubroy-chi10.pdf` (10 pp; text `dubroy-chi10.txt`; figure crops `fig3_hi.png`, `fig4_hi.png`, `page6.png`, `page6_hi.png`) | https://www.dgp.toronto.edu/~ravin/papers/chi2010_tabbedbrowsing.pdf (HTTP 200, application/pdf) | PDF metadata Title "A study of tabbed browsing among mozilla firefox users"; running footer "CHI 2010: Browsing … April 10–15, 2010, Atlanta, GA, USA", page numbers 673–682 | 8f1189484d86152d99ad64d67a96be9139bd33d510a86eb353148264040a33a3 |
| chang-chi21 | `chang-chi21/chang-chi21-joecat-wayback-2021.pdf` (15 pp; text `chang-chi21/chang-chi21.txt`; page render `chang-chi21/page6.png`) | reused pre-existing Wayback copy `chang-chi21-joecat-wayback-2021.pdf` (a second copy `...-2024.pdf` has the same size and differs in 138 bytes, not used) | p.1: title "When the Tab Comes Due: Challenges in the Cost Structure of Browser Tab Usage", "CHI '21, May 8–13, 2021, Yokohama, Japan", "https://doi.org/10.1145/3411764.3445585", "15 pages"; PDF CreationDate 2021-01-14. Identity confirmed. | bf20fa653e6c0bd6d945ac748017e64ce3d8bc86da883da3685793cb8f6f8718 |
| mozilla-testpilot10 | git clone `mozilla-testpilot10/testpilotweb` at commit **50d5f37341e30b53af16a1c56bc981fc9a52097b** (2019-03-28); file `testcases/a-week-life-2/aggregated-data.html` (last touched by commit a3236d39, 2010-11-30 "update WILv2 samples page") | https://github.com/mozilla/testpilotweb | page title "Test Pilot: A Week in the Life of a Browser - Version 2: Aggregated Data Samples" | — |
| mozilla-testpilot10 (Wayback) | `mozilla-testpilot10/aggregated-data-wayback-20110711.html` | web.archive.org/web/20110711092757id_/https://testpilot.mozillalabs.com/testcases/a-week-life-2/aggregated-data.html (200) | byte-identical to the git copy | edde45f0…f3db |
| mozilla-testpilot10 (Wayback) | `mozilla-testpilot10/aweeklife2-wayback-20110711.html` (+ `.txt`) — the study description page | web.archive.org/web/20110711102041id_/https://testpilot.mozillalabs.com/testcases/aweeklife2.html (200) | heading "A Week In the Life of A Browser – Version 2", posted Oct 22 2010 | a67e3678…a834 |
| mozilla-testpilot10 (Wayback) | `mozilla-testpilot10/witl_small-wayback-20110711.tar.gz` (extracted `users.csv`, `events_small.csv` under `witl_small_extract/`) | web.archive.org/web/20110711102216id_/https://testpilot.mozillalabs.com/testcases/a-week-life-2/witl_small.tar.gz (200, 7,746,321 bytes) | gzip header "witl_small.tar", mtime 2010-11-19 | 789ea6a5…c0d |
| singervine-slate10 (live) | `singervine-slate10/slate-live.html` (+ `slate-live.txt`) | https://slate.com/human-interest/2010/12/a-new-data-set-from-firefox-reveals-our-browsing-habits.html (200, fetched 2026-09-13) | `<h1 itemprop="headline">Open This Story in a New Tab</h1>`, dek "A new data set from Firefox reveals our browsing habits.", `article:published_time` 2010-12-05T20:44:00+00:00, author meta matches entry | 79e169b3…72b3 |
| singervine-slate10 (Wayback) | `singervine-slate10/slate-wayback-20111112-single.html` (+ `.txt`); charts `82_101203_hive_graph1.gif`, `…graph2.jpg`, `…graph3.jpg`, `…graph4.jpg` (combined views `graphs12.png`, `graphs34.png`) | web.archive.org/web/20111112122730id_/http://www.slate.com/articles/life/the_hive/2010/12/open_this_story_in_a_new_tab.single.html (200); images via web.archive.org/web/2011id_/http://www.slate.com/content/dam/slate/archive/2010/12/<file> (200) | body text matches live copy (same paragraphs, same numbers, same correction note) | de92d7b7…34b8 |
| chromium-process-model | `chromium-process-model/process_model_and_site_isolation@2ea96871.md` | https://chromium.googlesource.com/chromium/src/+/2ea968713a3de13a38d992a99b21102409b5dd1f/docs/process_model_and_site_isolation.md (?format=TEXT); commit = refs/heads/main at read time; identical to +/HEAD fetch | H1 "Process Model and Site Isolation" | 5a371fa5…1bab |
| chromium-process-model | `chromium-process-model/process-models-chromium-org.html` | https://www.chromium.org/developers/design-documents/process-models/ (200) | stub: "The most recent version of this page is now in the Chromium source tree." linking the file above | — |
| (C-testpilot-5 leads only) | `tabs-newer-data-search/BrowserUsageTelemetry.html` (+ `.txt`) | https://firefox-source-docs.mozilla.org/browser/BrowserUsageTelemetry.html (200) | — | — |

Unreachable: live `https://testpilot.mozillalabs.com/testcases/a-week-life-2/aggregated-data.html` — curl exit 6 (host did not resolve). Wayback copies used instead. Nothing else unreachable.

---

## dubroy-chi10

### C-dubroy-1 — distribution of simultaneously open tabs logged per user: most common value, range of per-user medians, maximum

(a) Verbatim

- p.676 (CHI 2010 p. 676), "Analysis Methods": "Number of concurrent tabs and windows.  We measured the number of windows and tabs that were open when a navigation event occurred, as in Weinreich et al. [18]. For simplicity, we ignored all navigation events caused by Firefox's session restore feature in calculating this measure." (txt lines 400–404)
- p.678, text beside Figure 3: "Figure 3 shows the number of tabs open when a navigation action occurred. The most common number of tabs to have open is one, with a steady descent down to 9. There is a second peak at 16 tabs, but this was almost entirely due to just two of the participants, P14 and P20." (txt 549–553)
- p.678: "For further insight, we examine the median and maximum number of tabs that each participant had open (Figure 4). Participant 8's data is omitted as he dropped out part way through the study." (txt 554–557)
- p.678: "Participant 14 had by far the highest median number of tabs open with 17, while no other participant had a median higher than 6. Participant 20 had the highest number of tabs open at once, with 42." (txt 558–562)
- p.678: "P19 is interesting—he had a median of only one tab open, but a max of 27. Participant 2 is similar, but not nearly as extreme: a median of 4 and a max of 20." (txt 572–574)
- p.680: "As we saw in Figure 3, the largest portion of navigation events during the study happened with only one tab open, and Figure 6 showed that 7 participants had a median of only one or two tabs open." (txt 758–761)
- Figure 3 caption: "Figure 3: Number of tabs open on navigation"; axes "Number of tabs open on navigation" / "Number of navigation events"; legend "P14 & P20", "Other tab power users", "Other participants".
- Figure 4 caption: "Figure 4: Median and maximum number of open tabs"; legend "Max tabs open", "Median tabs open on navigation"; x-axis "Participant", y-axis "Number of tabs".

(b) Locator: p.676 "Analysis Methods"; p.678 Figures 3 and 4 and adjacent text; p.680 "Measuring Tab Revisitation". Figures viewed as images (500 dpi crops `fig3_hi.png`, `fig4_hi.png`).

Figure 4 values as read off the image (bar heights on a 0–45 axis; reading precision about ±0.5 tab; not printed as numbers in the paper except where quoted above):

| Participant | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| median (dark) | 4 | 4 | 4 | 4 | 4 | 2 | 4 | 2 | 2 | 1 | 2 | 3 | 17 | 1 | 4 | 4 | 1 | 1 | 6 | 6 | 3 |
| max (light) | 14 | 20 | 13 | 12 | 14 | 9 | 12 | 8 | 5 | 5 | 5 | 10 | 28 | 7 | 11 | 11 | 5 | 27 | 42 | 18 | 14 |

Figure 3 as read: tallest bar at 1 tab (~24,000 navigation events), then ~16,000 (2), ~13,300 (3), ~11,500 (4), ~8,200 (5), ~5,200 (6), declining; x-axis plotted 0–25.

(c) Plain reading: Firefox (extension compatible with 1.5–3.0), 21 recruited active tab/window users, **logged** by a custom click-stream extension. The count is the number of tabs open **at each navigation event** (session-restore navigations excluded), so it is sampled per navigation, not time-weighted. The text does not say whether the count is per window or summed over all windows. Most common value across all navigation events pooled: 1 tab. Per-user medians range from 1 (P19 stated; also P11, P15, P18 from figure) to 17 (P14); all others ≤ 6. Largest per-user maximum: 42 (P20). Notes from the figure: (i) the text says "7 participants had a median of only one or two tabs open" and cites "Figure 6", but the median-per-participant chart is Figure 4, and my read of Figure 4 gives 8 participants at 1 or 2 (P6, P9, P10, P11, P12, P15, P18, P19) — the 2-tab bars are small, so this rests on figure reading; (ii) Figure 4 labels 21 bars as 1–7 and 9–22 (P8 omitted), i.e. participant IDs up to 22, while the Methodology says 21 participants; (iii) Figure 4 carries an unexplained horizontal gray line at about 13.

(d) Verdict: **FOUND** (most common value = 1; per-user medians 1–17; maximum 42).

### C-dubroy-2 — number and recruitment of participants, browser and version, study period, data availability

(a) Verbatim

- Abstract p.673: "The detailed web browsing usage of 21 participants was logged over a period of 13 to 21 days each, and was supplemented by qualitative data from diary entries and interviews." (txt 13–16)
- p.675 "Participants": "21 people (13 female, 8 male; 15 aged 18-29, 4 in their 30s, and 2 in their 50s) were recruited via email through the extended network of the researchers, and by posters on bulletin boards around campus. The study was advertised as "a research study exploring how people use web browsers", looking for participants who "use Mozilla Firefox for several hours a day, and often use multiple tabs or windows."" (txt 241–248)
- p.675: "6 of the participants were full-time students, and 15 were working in office environments where they spent most of their time on the computer." (txt 266–268)
- p.675 "Click-stream Data": "Click-stream data was collected using a custom extension for Firefox that was compatible with Firefox versions 1.5 through 3.0 so that it could be installed without upgrading or significantly changing the user's browsing environment." (txt 277–280)
- p.675: "First, the actual URLs and sites that participants visited were not made available to the researchers." (txt 288–289)
- p.675: "All of the click-stream data was stored in a human-readable format, which the participants could review before manually submitting to the researchers via email." (txt 299–302)
- p.676 "Procedure": "At the end of the two week period, participants were given instructions on how to remove the Firefox extension and all associated logs. For participants who had only installed the extension on their work computer, an effort was made to extend the study to a full 14 days of use. After the extension was uninstalled, participants were paid $50 for their participation in the study. One participant (participant 8) opted to end participation part way through the study." (txt 347–354)
- p.682 "Study Limitations": "The study population was limited to Firefox users who often used multiple windows or tabs during browsing." and "Internet Explorer … did not support tabbed browsing by default until version 7.0 (the most recent at the time of the study)" (txt 929–938)

(b) Locator: Abstract p.673; Methodology (Participants, Instruments and Data Collection, Procedure) pp.675–676; Study Limitations p.682.

(c) Plain reading: 21 participants, convenience/purposive recruitment (researchers' email network + campus posters), screened for heavy Firefox use with multiple tabs/windows; paid $50; one dropout (P8). Browser: Mozilla Firefox; the logger supported versions 1.5–3.0 — the versions participants actually ran are not reported. Period: 13–21 days per participant (nominally two weeks); calendar dates of the study are not stated (only "IE 7.0 … the most recent at the time"). Data availability: no statement that the logs or dataset are released; searched the text for "availab", "dataset", "data set", "release" — only hit is URLs "not made available to the researchers".

(d) Verdict: **PARTIAL** — participants, recruitment, browser, per-user period FOUND; exact browser versions used and calendar dates not stated; data availability NOT FOUND (no statement).

---

## chang-chi21

### C-chang-1 — number of open tabs at which participants reported feeling overwhelmed: central value and spread

(a) Verbatim

- §3.2 p.4: "The first part focused on their general experiences with tab management, such as how often they feel overwhelmed by the number of open tabs, or what were their thresholds for the number of open tabs." (txt 373–376)
- §5 pp.4–5: "To better understand this limitation, we asked participants in the survey about the number of tabs they would start feeling overwhelmed and experiencing difficulty managing them. The responses followed an long-tailed distribution showing that people have different tolerances (Figure 1), with the median number being eight tabs (N=103, first quartile: 5 tabs; third quartile: 12 tabs). We further asked them how frequently they reach this threshold. The majority (67%) of our participants responded at least once a week (17% daily; 9% 4-6 times per week; 25% 2-3 times per week; and 16% once per week)" (txt 418–429)
- Figure 1 caption p.6: "Figure 1: When asked about having how many open tabs they would start experiencing issues managing them, responses from the survey participants in Study 2 (N=103) followed a long-tailed distribution with the median number being 8 tabs (first quartile: 5 tabs; third quartile: 12 tabs). When further asked about frequently they reach their thresholds. The majority (67%) of our participants reported at least once a week." (txt 530–533)
- Figure 1 left panel title (image): "If I have more than __ tabs, I would start having issues managing them."; x-axis "Number of Tabs"; y-axis "Number of Participants (N=103)".

(b) Locator: §3.2 (p.4), §5 opening (pp.4–5), Figure 1 (p.6). Figure viewed as image (`chang-chi21/page6.png`).

Figure 1 left histogram as read (bin width 5): 0–5: 30; 5–10: 44; 10–15: 10; 15–20: 7; 20–25: 2; 25–30: 2; 30–40: no bars; ">40": 8. Sum 103. Right panel bar labels: Daily 17.5%, 4-6 times/week 8.7%, 2-3 times/week 25.2%, Once/week 15.5%, Once/month 13.6%, Once/year 3.9%, Never 15.5%.

(c) Plain reading: Study 2, 103 Amazon Mechanical Turk workers, **self-reported** threshold (a single number each), browser unspecified. Central value: median 8 tabs; spread: IQR 5–12; long right tail with 8 respondents above 40. Wording caveat: the body text frames it as "start feeling overwhelmed and experiencing difficulty managing them", while the survey item shown in the figure reads "If I have more than __ tabs, I would start having issues managing them." — the figure's item text does not contain the word "overwhelmed". No mean or SD is given.

(d) Verdict: **FOUND** (median 8, Q1 5, Q3 12, N=103; item wording as noted).

### C-chang-2 — reported distribution of currently open tabs among participants and any cap on the reported value

(a) Verbatim

- §3.2 p.4: "For this, participants gave a short description for each of their open browser tabs at the time when the survey took place (excluding tabs related to Mechanical Turk tasks, such as our survey page). … To control for survey duration, participants reported up to 10 browser tabs if they had more than 10, which accounted for 7.8% of all participants (N=103). On average, each participant labeled 6.15 tabs (SD = 3.69), or a total of 633 tabs." (txt 378–387)
- §3.2 p.4: "Here, we explicitly asked our participants to only include their tabs that were unrelated to crowdsourcing tasks in their responses" (txt 359–361)
- §3.1 p.3 (Study 1 screening): "2) people who self-reported often reaching 12 or more tabs open on their work computer." (txt 285–286)

(b) Locator: §3.2 "Study 2: Survey with Mechanical Turk" (p.4); §3.1 "Participants" (p.3).

(c) Plain reading: The paper does **not** report a distribution (histogram, median, quartiles) of how many tabs participants currently had open. What it reports is the number of tabs each participant *labeled* in the survey: capped at 10 (participants with more than 10 open tabs reported only 10), 7.8% of the 103 were above the cap (≈8 people), mean labeled = 6.15 (SD 3.69), total 633 labeled tabs. Because of the cap and the exclusion of MTurk-related tabs, 6.15 is a mean of a capped, filtered count, not a mean of open tabs. Study 1's "12 or more tabs" is a recruitment screen, not a reported distribution. Searched text for "[0-9]+ tabs", "open tabs", "tabs open", "N=" across all 15 pages; no other count distribution.

(d) Verdict: **PARTIAL** — cap (10) and share above cap (7.8%), mean/SD of labeled tabs FOUND; a distribution of currently open tabs is PREMISE NOT IN SOURCE.

### C-chang-3 — self-reported or logged tab counts

(a) Verbatim

- Abstract p.1: "We interviewed ten information workers asking about their tab management strategies and walk through each open tab on their work computers four times over two weeks. … We then surveyed 103 participants to estimate the frequencies of these pressures at scale." (txt 45–51)
- §1 p.2 (preliminary survey N=64): "Based on self-reporting, 59% of our participants agreed that …" (txt 112–113)
- §3.1 p.3: "people who self-reported often reaching 12 or more tabs open on their work computer" (txt 285–286); "Participants then were asked to walk through each of the browser tabs currently open in their work computers" (txt 309–310)
- §3.2 p.4: "participants gave a short description for each of their open browser tabs at the time when the survey took place" (txt 378–380); "participants reported up to 10 browser tabs if they had more than 10" (txt 384–385)

(b) Locator: Abstract; §1; §3.1; §3.2; §8 Limitations (p.12, no mention of logging).

(c) Plain reading: All tab counts in the paper come from **self-report** (online survey answers: thresholds, frequencies, labeled tab lists) or from interview walk-throughs of the tabs open at interview time. No logging software, browser extension or telemetry was used to record tab counts; searched for "log", "logg", "extension", "telemetry", "instrument" — the only "extension" hit (p.10) is about commercial browser extensions as design examples.

(d) Verdict: **FOUND** (self-reported / interview-observed; not logged).

---

## mozilla-testpilot10

Note on the premise of C-testpilot-1/2/3: the "aggregated-data.html" page is a data-description and download page. It contains no summary statistics of any kind (no mean, median or percentile of tabs). Searched the page and the whole repo (`grep -rni "median|average number of tabs|mean number|max.*tabs"` over *.html/*.php, plus git history for deleted Week-in-the-Life files): the only tab statistics in the repo are on `testcases/tab-open-close/results.html`, which is a **different** Test Pilot study (Tab Open/Close, Firefox 3.5, ~5,000 users, Sept 2009) and presents them only as a density plot with prose. The Week in the Life v1 results page (`testcases/a-week-life/results.html`) has statistics for bookmarks/folders only.

### C-testpilot-1 — in the aggregated tables: mean number of open tabs, number of participants, study length and year

(a) Verbatim (`testcases/a-week-life-2/aggregated-data.html` @50d5f37)

- line 16: "A Week in the Life of a Browser - Version 2: Aggregated Data Samples"
- line 22: "Test duration: 7 days"
- line 24: "Firefox versions covered: Fx 3.5 and Fx 3.6, Fx4 Beta"
- line 25: "Data submission: 527,817 test sets submitted in November 2010."
- lines 36–38 (table rows, cells "Filename | Download Size | Num. of Tables | Num. of Users | Description"): "witl.db.gz | 1.1 GB | 3 | About 27,000 | Gzipped SQL dump of all three tables"; "witl_large.tar.gz | 469 MB | 3 | About 27,000 | Gzipped Tar archive of three CSV files, one for each table"; "witl_small.tar.gz | 7.4 MB | 3 | About 27,000, 387 w/ event data | Gzipped Tar archive of three CSV files, one for each table"
- line 127 (event-code table): "26 | NUM_TABS | Recorded whenever memory is recorded (at startup and every 15 minutes) and also whenever a window or tab is opened or closed. | 'data1' is number of windows, 'data2' is number of tabs (including the one just opened)."
- line 115: "Memory usage is recorded once every 15 minutes (although this was originally set to 1hr so data prior to Nov 6 will be 1 hour intervals), and upon startup."

Study page (`aweeklife2-wayback-20110711.txt` lines 22, 24): "This study will be running from October 2010 to October 2011,  periodically collect data on the browser's basic performance for one week, running the same study again every month." / "Test Duration: Periodical study*, run 1 week every 30 days"

Mean tabs — found only in the Slate article (see singervine-slate10): "Thanks to some particularly prolific tabbers (for reasons unfathomable, a participant once had 1,103 tabs open), the average of these averages is 3.2 tabs." (slate-live.txt line 14; Wayback single-page txt line 18)

(b) Locator: aggregated-data.html lines 16, 22, 24, 25, 36–38, 115, 127 at commit 50d5f37 (identical to Wayback 2011-07-11 capture); aweeklife2 Wayback capture lines 22, 24.

Data check (form only, not a statistic of tabs): `users.csv` in witl_small has 27,267 user rows; `fx_version` prefixes 4.0: 26,391, 3.6: 850, 3.5: 26; `events_small.csv` holds event rows for 387 users, including 191,487 NUM_TABS (code 26) rows.

(c) Plain reading: Firefox (3.5, 3.6, 4.0 beta — the sample's users are overwhelmingly 4.0 beta), about 27,000 submissions ("each submission is assumed to be a different user", line 56), a 7-day logging window, data submitted November 2010 (the recurring study ran Oct 2010–Oct 2011; this release is the November 2010 set). "527,817 test sets" (line 25) and "About 27,000" users (lines 36–38) are both stated; the page does not reconcile the two numbers. Tab counts were **logged** (NUM_TABS events at startup, every 15 min, and on each tab/window open/close). The page gives **no mean number of open tabs**. The 3.2 figure is a third-party (Slate) computation: the mean over users of each user's average open-tab count; how each user's average was computed (per-event vs time-weighted) is not stated.

(d) Verdict: **PARTIAL** — participants (~27,000), length (7 days), year (Nov 2010) FOUND; mean open tabs: PREMISE NOT IN SOURCE for the Test Pilot tables (the value 3.2 exists only in the Slate article).

### C-testpilot-2 — median of each user's maximum tab count over the week

(a) Verbatim: none in the Test Pilot pages. Slate: "One-half of the participants maxed out at fewer than eight tabs, but one-quarter of users had 11 or more tabs open at least once during the study." (slate-live.txt line 17; Wayback txt line 19)

(b) Locator: absent from aggregated-data.html, aweeklife2 study page, and all repo HTML (search described above). Present in Slate article paragraph beginning "What about the extremes of our browsing habits?"

(c) Plain reading: The Test Pilot material does not state it. Slate (own analysis of the logged Week in the Life v2 data, ~27,000 Firefox users) says the median of per-user weekly maximum is below 8 ("fewer than eight"), stated as a bound rather than an exact median. Slate's "User Distribution: Maximum Tabs Open" histogram (viewed as image) peaks at 5–6 tabs (~10.8% of users) and is plotted only to 20.

(d) Verdict: **PREMISE NOT IN SOURCE** (not in Test Pilot tables; Slate reports "fewer than eight").

### C-testpilot-3 — tab count reached by the top quarter of users

(a) Verbatim: none in the Test Pilot pages. Slate: "one-quarter of users had 11 or more tabs open at least once during the study" (line 17 / 19, as above); for per-user averages: "About one-half of users kept an average of more than 2.38 tabs open, and one-quarter kept an average of at least 3.59 tabs open." (slate-live.txt line 14; Wayback txt line 18)

(b) Locator: as C-testpilot-2.

(c) Plain reading: Not in Test Pilot material. Slate gives two top-quartile figures: per-user **maximum** ≥ 11 tabs for the top quarter; per-user **average** ≥ 3.59 tabs for the top quarter (median per-user average 2.38).

(d) Verdict: **PREMISE NOT IN SOURCE** (not in Test Pilot tables; Slate reports 11 for maximum, 3.59 for average).

### C-testpilot-4 — location, licence and form (raw vs aggregate) of surviving data; recruitment

(a) Verbatim

- aggregated-data.html line 33: "Anyone is welcome to download and use the aggregated data files below."
- line 41: "All of this data has been collected and is being shared under the terms of the Test Pilot Privacy Policy  from Mozilla Labs.  We license this data for use by anyone under the terms of the Creative Commons Attribution 3.0 United States License.. This license allows derived works as well as commercial use, as long as you give attribution for the source of the data." (link href `http://creativecommons.org/licenses/by/3.0/`; badge at line 188 links `http://creativecommons.org/licenses/by/3.0/us/`)
- line 43: "There is no personally-identifiable information, and no URLs, contained in this data set."
- line 51: "Main table of users and the metadata associated with each user."
- line 56: "All rows that have the same user number came from the same submission. Each submission is assumed to be a different user, but there are various ways that a single user could make multiple submissions (e.g. multiple computers, multiple Firefox profiles, etc.)"
- line 66: "Main table of users and recorded events." with columns user_id, event_code, data1–3, "timestamp | The time at which the event occurred, given in milliseconds since epoch"
- line 134: "Note that because the survey was optional, the table does not include all users."
- line 182: "The following extensions are known to cause major changes to the relationship between tab use and memory in Firefox.  Data submissions from users who had one of these extensions installed have been filtered out of the data sets provided on this page" — list: "Bar Tab"
- First rows of `witl_small/events_small.csv`: `User_id,event_code,data1,data2,data3,timestamp,session_id` / `0,26,"1 windows","4 tabs","",1288742315024,""`
- Recruitment, `faq.php` line 51 (file last changed 2010-07-14, commit 1326541): "If you are a user of Firefox version 3.5 or above, you just need to download and install the Test Pilot add-on. Once you've installed the add-on, you will automatically become a Test Pilot."; line 61: "Studies automatically log data while you use Firefox.  At the end of the study, you will be prompted to submit your log data and/or survey answers."; line 80: "After a study is complete, we will also publish sanitized and aggregated data under the Creative Commons Attribution License, as public resources."
- Study page (Wayback) line 153: "Become a Test Pilot and help us make Firefox better! As a non-profit organization, we rely upon the support of volunteers to help us understand how people are using the Web"
- Slate (live line 2): "Since mid-2009, the folks behind Firefox have encouraged its users to install Test Pilot, a plug-in that collects anonymized browser usage."; (line 10) "Because Mozilla wants to recruit as many participants as possible and isn't paying them, Test Pilot collects much less personal information than Nielsen does."

(b) Locator: aggregated-data.html lines 33, 41, 43, 51, 56, 66, 134, 182, 188 @50d5f37; faq.php lines 51, 61, 80 @50d5f37; Wayback CDX for `testpilot.mozillalabs.com/testcases/a-week-life-2/*` lists 200 captures of witl.db.gz (20110711095832, 1,006,358,942 bytes), witl_large.tar.gz (20110711101127, 490,768,224 bytes), witl_small.tar.gz (20110711102216, 7,738,884 bytes); witl.tar.gz linked at line 46 is a 404 capture.

(c) Plain reading: Location — the description page survives in the GitHub mirror (mozilla/testpilotweb) and in Wayback; the data files themselves are **not** in the GitHub repo (only the HTML), but Wayback holds 200-status captures of all three archives; I downloaded and opened only witl_small. The original host testpilot.mozillalabs.com does not resolve. Licence: CC BY 3.0 United States (text), link targets both /by/3.0/ and /by/3.0/us/. Form: despite the page title "Aggregated Data Samples", the files are **event-level logs** (one row per logged event with millisecond timestamps, per anonymized user id) plus per-user metadata and an optional survey table; no URLs/PII; submissions from Bar Tab users removed. witl_small carries event data for 387 users only (users table ~27,000). Recruitment: opt-in, unpaid volunteers who installed the Test Pilot add-on (Firefox 3.5+) and chose to submit; a self-selected population (Slate notes technophilic skew and 6.5% female among survey respondents).

(d) Verdict: **FOUND**.

### C-testpilot-5 — publicly available large-scale logged browser tab-count data newer than 2010

(a) Verbatim

- Slate (live line 34): "(Google and Microsoft have collected similar user information for Chrome and Internet Explorer, but they don't have immediate plans to release the raw data publicly, their press officers tell me.)"
- Firefox Source Docs, BrowserUsageTelemetry (txt line 202): "tab and window engagement: counts the number of non-private tabs and windows opened in a subsession, after the session is restored (see e.g. browser.engagement.max_concurrent_tab_count);"

(b) Locator: Slate paragraph beginning "These data alone won't offer us deeper insight"; firefox-source-docs.mozilla.org/browser/BrowserUsageTelemetry.html section "Tab and window interactions".

(c) Plain reading: None of the four sources identifies a public logged tab-count dataset newer than 2010 (Dubroy's logs are not released; Chang 2021 is self-report; the Test Pilot data are Nov 2010; Slate says in 2010 that Google and Microsoft had no plans to release). How searched: full-text reads of all four sources; repo-wide grep of testpilotweb; two web searches ("public dataset logged browser open tab counts telemetry large-scale"; "Firefox telemetry max_concurrent_tab_count public aggregate data"). Lead only: Firefox still collects a logged tab-count probe (`browser.engagement.max_concurrent_tab_count`), per Mozilla's source docs; whether its aggregates are publicly downloadable was **not verified** (a search-engine summary claimed so without a primary citation; not relied on). A universal "does not exist" cannot be established from this read.

(d) Verdict: **NOT FOUND** (in the sources and in the limited search; existence not ruled out).

---

## singervine-slate10

### C-singervine-1 — whether the Slate article analyses the Test Pilot browsing dataset and which figures it reports

(a) Verbatim (live copy `slate-live.txt`; same text in Wayback 2011 single-page copy)

- H1/dek (HTML): "Open This Story in a New Tab" / "A new data set from Firefox reveals our browsing habits."
- line 2: "Last month, Mozilla Labs released its most comprehensive Test Pilot data set, the second version of what it's calling "A Week in the Life of a Browser.""
- line 3: "The abundance of data in "Week in the Life," which covers a week's worth of 27,000 users' browsing activities, can be paralyzing. Faced with several gigabytes of decompressed data, where do you start? Tab usage, I decided."
- line 10: "In fact, only about 4,000 of the 27,000 users in the latest data dump answered such basic questions as: "What is your gender?," "How old are you?," and "How much time do you spend on the Web each day?""
- line 11: "just 6.5 percent of the "Week in the Life" survey respondents said they were female. There are so few female-identifying participants—just 257—that we can have very little confidence whether the women in this study are representative of most other women."
- line 14: "Test Pilot recorded the number of tabs users had open every 15 minutes and every time they opened a new tab or window. In "A Week in the Life of a Browser," the 27,000 participants quietly logged more than 12 million of these tab-related events. (Two earlier Test Pilot studies also logged tab data, but for fewer participants and in the absence of demographic details.) Let's start with the most obvious question: How many tabs do users have open, on average? About one-half of users kept an average of more than 2.38 tabs open, and one-quarter kept an average of at least 3.59 tabs open. Thanks to some particularly prolific tabbers (for reasons unfathomable, a participant once had 1,103 tabs open), the average of these averages is 3.2 tabs."
- line 17: "What about the extremes of our browsing habits? One-half of the participants maxed out at fewer than eight tabs, but one-quarter of users had 11 or more tabs open at least once during the study."
- line 21: "That said, men kept more tabs open than women—an average of 4.45 tabs versus 3.86 tabs. Men also kept more tabs open at the heights of their browsing, maxing out at an average of 11.33 to women's 10.38."
- line 36: "(To find what sorts of numbers are available for crunching, see the tables on this page.)" — link target https://testpilot.mozillalabs.com/testcases/a-week-life-2/aggregated-data.html
- line 37: "Correction,  Dec. 6, 2010: This article originally stated that Firefox was the world's most popular browser. Internet Explorer commands a larger usage share. (Return to the corrected sentence.) Also, originally the article's first graph, labeled "User Distribution: Average Tabs Open," mistakenly showed the data set for a distribution of maximum tabs open."
- Chart titles (Wayback images, alt text and image text): "User Distribution: Average Tabs Open", "User Distribution: Maximum Tabs Open", "Average Tabs Open by Age", "Average Tabs Open by Age and Gender".

(b) Locator: live slate-live.txt lines 2, 3, 10, 11, 14, 17, 21, 36, 37 (Wayback single-page txt lines 11, 12, 16, 17, 18, 19, 20, 27, 28). Charts: Wayback images listed in the copies table; the live 2026 page no longer embeds them.

Charts as read (images): Average-tabs histogram — tallest bin ~33.5% of users at 1–2, ~27% at 2–3, ~15.5% at 3–4, ~7.5% at 4–5, ~4.5% at 0–1 and 5–6, tail to 20. Maximum-tabs histogram — peak ~10.8% at 5–6, ~10.7% at 4–5, ~9.5% at 3–4 and 6–7, declining to ~1% at 19–20; plotted 0–20. By age (all): roughly 3.7 (under 18), 4.7 (18–25), 5.2 (26–35), 3.6 (36–45), 3.3 (46–55), 2.8 (older than 55). The 2011 capture's first chart (filename prefix "82_" unlike the others' "1_123125_…") shows a distribution peaked at 1–2 tabs, consistent with averages, i.e. presumably the corrected chart; the capture does not say which version it is.

(c) Plain reading: Yes — the article is the author's own analysis of the logged Test Pilot "A Week in the Life of a Browser" v2 data (Firefox, ~27,000 opt-in users, one week, Nov 2010 release). Figures reported: >12 million tab events; per-user average open tabs — median 2.38, 75th percentile 3.59, mean of per-user averages 3.2; single highest count 1,103; per-user weekly maximum — median below 8, 75th percentile ≥ 11; by sex (survey respondents only, ~4,000; 257 female) average 4.45 (men) vs 3.86 (women), mean maximum 11.33 vs 10.38; age and age-by-sex charts. How a user's "average" was computed (per event vs time-weighted, idle time in or out) is not stated. Observed without resolution: both sex-specific averages (4.45, 3.86) exceed the overall 3.2; the article does not explain (the subgroups are the survey-respondent subset). The article's headline matches the bibliographic entry ("Open This Story in a New Tab"); the entry's URL slug is the dek.

(d) Verdict: **FOUND**.

---

## tabshared

### C-tabs-1 — per source: browser studied and anything about processes per tab; Chromium's documented process model

(a) Verbatim

Dubroy (Firefox): "Click-stream data was collected using a custom extension for Firefox that was compatible with Firefox versions 1.5 through 3.0" (p.675). Search for "process" in the full text: only hit "many links at once can be termed a process of elimination." (p.679, txt 653). Nearest resource mention: "Only three people cited resource usage or performance reasons for using tabs instead of multiple windows." (p.677, txt 488–489)

Chang (browser not specified): Table 1 row "Close C3: Limited Computing Power Drains processing power causing browser and other applications to slow down" (p.4, txt 334); §5.2: "participants who sometimes keep a large number of tabs around mentioned having too many tabs drains the limited processing power and memory space from their computers, causing their browsers to become too slow." (p.5, txt 483–486); participant quote "usually the only time that I do that is if Chrome is starting to get really slow." (txt 488–490); §8: "it is possible that mobile browser tabs may involve different usage patterns due to differences in screen real-estate and memory constraints" (p.12, txt 1183–1185). No "renderer", "multi-process" or process-per-tab statement (searched "process", "renderer", "multiprocess", "content process").

Test Pilot Week in the Life v2 (Firefox 3.5/3.6/4 beta): aggregated-data.html line 24 "Firefox versions covered: Fx 3.5 and Fx 3.6, Fx4 Beta"; line 115 MEMORY_USAGE "iterate through all the reporters in the memory manager"; line 182 Bar Tab filter "known to cause major changes to the relationship between tab use and memory in Firefox". No statement about processes (only "process" hit is the survey answer "Online word processing"). A public reader comment on the study page (not Mozilla's text) says Firefox "doesn't launch a new process for each tab, a  la chrome" (aweeklife2 Wayback txt line 51).

Slate (Firefox): no mention of processes (searched "process"); mentions Chrome only as "Google and Microsoft have collected similar user information for Chrome and Internet Explorer".

Chromium (`docs/process_model_and_site_isolation.md` @2ea96871):
- lines 27–28: "At a high level, Chromium aims to use separate processes for different instances of web sites when possible."
- lines 97–100: "A principal instance is the core unit of Chromium's process model. Any two documents with the same principal in the same browsing context group (see below) must live in the same process, because they have synchronous access to each other's content."
- lines 115–118: "Note that the user may visit multiple instances of a given principal in the browser, sometimes in unrelated tabs (i.e., separate browsing context groups). These separate instances do not need synchronous access to each other and can safely run in separate processes."
- lines 122–124: "A browsing context group is a group of tabs and frames (i.e., containers of documents) that have references to each other (e.g., frames within the same page, popups with window.opener references, etc)."
- lines 141–147: "### Full Site Isolation (site-per-process)" / "_Used on: Desktop platforms (Windows, Mac, Linux, ChromeOS)._" / "In (one-)site-per-process mode, each process is locked to documents from a single site."
- lines 166–169 (Partial Site Isolation, Android 2+ GB): "Chromium usually creates one unlocked process per browsing context group."
- lines 187–188: "On Android devices with less than 2 GB of RAM, Site Isolation is disabled to avoid requiring multiple renderer processes in a given tab (for out-of-process iframes)."
- lines 269–271 (Historical Modes): "**Process-per-tab**: This model used a separate process for each browsing context group (i.e., possibly multiple related tabs), but did not attempt to switch processes on cross-site navigations."
- lines 261–264: "**Process-per-site**: This model consolidated all instances of a given site into a single process (per profile), to reduce the process count. It generally led to poor usability when a single process was used for too many tabs."
- lines 322–331: "**Soft Process Limit**: On desktop platforms, Chromium sets a "soft" process limit based on the memory available on a given client. While this can be exceeded (e.g., if Site Isolation is enabled and the user has more open sites than the limit), Chromium makes an attempt to start randomly reusing same-site processes when over this limit. For example, if the limit is 100 processes and the user has 50 open tabs to `example.com` and 50 open tabs to `example.org`, then a new `example.com` tab will share a process with a random existing `example.com` tab, while a `chromium.org` tab will create a 101st process. Note that Chromium on Android does not set this soft process limit, and instead relies on the OS to discard processes."
- lines 334–338: "Out-of-process iframes (OOPIFs) and fenced frames use this approach, such that an `example.com` iframe in a cross-site page will be placed in an existing `example.com` process (in any browsing context group), even if the process limit has not been reached."
- www.chromium.org/developers/design-documents/process-models/: "The most recent version of this page is now in the Chromium source tree." (links the file above)

(b) Locator: as given per item (page/txt line for papers; file:line at commit for repo files).

(c) Plain reading: Dubroy, Test Pilot and Slate all study **Firefox** (Dubroy 1.5–3.0; Test Pilot 3.5/3.6/4 beta, ~97% 4.0 beta in the sample users table); Chang does not restrict or report the browser (participants mention Chrome and Firefox). **None of the four tab sources says anything about the number of OS processes per tab**; Chang only reports self-perceived CPU/memory/battery pressure from many tabs, and Test Pilot logs memory, not processes. Chromium's current documented model is not "one process per tab": on desktop it is site-per-process — renderer processes are locked to a site; same-site documents that can reference each other (same browsing context group) must share a process; same-site pages in unrelated tabs may run in separate processes; one tab with cross-site iframes can span multiple renderer processes; above a memory-based soft process limit, new tabs reuse existing same-site processes, so many same-site tabs can share one process; Android (partial isolation) usually uses one unlocked process per browsing context group; "process-per-tab" is listed only as a historical mode.

(d) Verdict: **FOUND** (browser per source and Chromium model found; "processes per tab" content is absent from all four tab sources — stated, not inferred).

---

## Verdict counts

| verdict | count | topics |
|---|---|---|
| FOUND | 6 | C-dubroy-1, C-chang-1, C-chang-3, C-testpilot-4, C-singervine-1, C-tabs-1 |
| PARTIAL | 3 | C-dubroy-2, C-chang-2, C-testpilot-1 |
| NOT FOUND | 1 | C-testpilot-5 |
| PREMISE NOT IN SOURCE | 2 | C-testpilot-2, C-testpilot-3 |
| COPY UNREACHABLE | 0 | — |

Unreachable URLs (substituted, not blocking): https://testpilot.mozillalabs.com/testcases/a-week-life-2/aggregated-data.html (host does not resolve, curl exit 6) — replaced by the byte-identical GitHub mirror and Wayback capture.
