# Reader output R08-typing

All paths below are relative to `_dev/research/jioh/2026-09-13-verification/sources/`.

## Copies used

| source-id | copy | what it is | identity check |
|---|---|---|---|
| dhakal-chi18 | `dhakal-chi18.pdf` (+ `dhakal-chi18.txt`) | Camera-ready CHI 2018 paper, 12 PDF pages, no printed page numbers (locators below are PDF pages 1–12). Carries the ACM permission block, "CHI 2018, April 21–26, 2018, Montreal, QC, Canada", ISBN 978-1-4503-5620-6/18/04 and DOI 10.1145/3173574.3174220 on p. 1. | PDF metadata title/authors match the entry. SHA-256 e5e72fac…96a2 is byte-identical to the copy the authors host at userinterfaces.aalto.fi/136Mkeystrokes/resources/chi-18-analysis.pdf (re-downloaded today and hashed). Key passages re-extracted independently with pypdf and matched to the .txt. |
| dhakal-chi18 | `dhakal-chi18/aalto-project-page.html` | Authors' project page (userinterfaces.aalto.fi/136Mkeystrokes), the URL the paper gives for the dataset. | Page title and bibliographic block match the paper. |
| dhakal-chi18 | `dhakal-chi18/Keystrokes__files__readme.txt`, `dhakal-chi18/metadata_participants.txt`, `dhakal-chi18/sample_100001_keystrokes.txt` | The dataset's own readme, participant metadata file, and one participant's keystroke file, pulled out of the released `data/Keystrokes.zip` (1,572,785,433 bytes) with HTTP range requests (the full zip was not downloaded). | Readme names the paper and URL. The zip's directory lists 168,593 `<id>_keystrokes.txt` files + readme + metadata. |
| roeser-rw24 | `roeser-ntu-1456856.pdf` (+ `.txt`) | Author manuscript (APA manuscript layout, running head "MODELLING TYPING DISFLUENCIES", 44 pages, PDF created 2021-08-12). Locators say "MS p. N". | SHA-256 3f777354…c713 is byte-identical to `manuscript.pdf` in the authors' OSF project osf.io/y3p4d (fetched today into `roeser-rw24/osf/manuscript.pdf`). |
| roeser-rw24 | `roeser-rw24/roeser-rw-springer-vor-wayback-20210825.pdf` (+ `.txt`) | **Publisher version obtained** (Springer online-first PDF, 26 pages, "© The Author(s) 2021", "Accepted: 11 August 2021", CC-BY 4.0 notice on p. 23). Retrieved from the Internet Archive capture of link.springer.com/content/pdf/10.1007/s11145-021-10203-z.pdf dated 2021-08-25; a direct fetch from Springer gets a JavaScript "Client Challenge" page again. Locators say "VoR p. N". | PDF metadata: title matches, `/doi` = 10.1007/s11145-021-10203-z, Creator Springer. Key passages and Table 2/3 values match the manuscript. |
| roeser-rw24 | `roeser-rw24/springer-landing-wayback-20241116.html` | Internet Archive capture (2024-11-16) of the Springer article landing page. | Its `citation_volume`/`issue`/`firstpage`/`lastpage` meta tags read 37 / 2 / 359 / 384, publication date 2024/02. Its full text repeats the same Table 3 values and "posterior mean" sentence. |
| roeser-rw24 | `roeser-rw24/crossref-20260913.json` | Crossref record, fetched today. | Volume 37, issue 2, pages 359-384, published-print 2024-02, published-online 2021-08-24, CC-BY 4.0. |
| roeser-rw24 | `roeser-osf/` (earlier download) + `roeser-rw24/osf/` (fetched today) + `roeser-osf-listing.json` | Authors' OSF materials: `manuscript.Rmd`, `walkthrough.Rmd`, Stan code (`ARKMoGpptbgs.stan`), R scripts, `stanin/README.txt`, full OSF file listing. | OSF node y3p4d title = paper title. The OSF project licence is CC0 1.0 Universal (from the OSF licence API). |

**Page mapping, Roeser.** The VoR copy is the 2021 online-first PDF, paginated 1–26 with no volume page numbers. The issue version runs 359–384, which is also 26 pages. *Inference (not checked against an issue-paginated PDF):* VoR p. N = journal p. 358+N. The passages cited below map as follows:

| content | MS p. | VoR p. | inferred journal p. |
|---|---|---|---|
| Fig. 1 (bimodality on log scale) | 6–7 | 4 | 362 |
| Log-normal footnote 3, Eq. 1 | 11–12 | 7–8 | 365–366 |
| Prior on β (Eq. 4) | 13–14 | 9 | 367 |
| Mixture model Eq. 7–8 | 16–18 | 10–11 | 368–369 |
| Eq. 9–10, Table 1 | 18–19 | 12 | 370 |
| Copy-task data (sample, exclusions, tasks) | 20 | 12–13 | 370–371 |
| Model fit, OSF statement | 24 | 15 | 373 |
| Parameter evaluation text, Table 2 | 24–26 | 16 | 374 |
| Table 3, text continuation | 27 | 17 | 375 |
| Fig. 5 text, δ/θ by-participant comparison | 28–30 | 17–19 | 375–377 |
| Discussion (one-quarter / two-thirds) | 33 | 20 | 378 |
| Open Access licence notice | — | 23 | 381 |

**Quoting conventions.** Quotations are copied from the PDF text layers. The only changes are: typographic ligatures (ﬁ, ﬂ) written as fi/fl; line-end hyphenation joined; and, where the Springer text layer garbles Greek letters (it renders them as "/u1D6FD" and similar), the Greek is taken from the byte-identical author manuscript. In every such case the wording was checked against the VoR text.

---

## dhakal-chi18

### C-dhakal-1: the mean inter-key interval, its dispersion statistic and unit, and the population

**(a) Verbatim**

1. p. 5, Results › Performance Measures › "INTER-KEY INTERVALS": "Average inter-key interval is 238.656 ms (SD = 111.6). A lower bound of about 60 ms can be observed. The IKI distribution shown in Figure 2 has a skewness of 1.98 and kurtosis measure of 7.1. The differences between typists are remarkable. For fast typists, the average IKI is ∼120 ms, with a standard deviation of only 11 ms, while slow typists have an IKI of over 480 ms, sometimes as high as 900 ms, with a large standard deviation: over 120 ms."
2. p. 5, Table 3, row "IKI (ms)", columns All X̄ / σ: "238.66 111.60". Legend: "X : Mean value σ : Standard deviation". Caption: "At the left are the mean and SD for each measure, correlation of each measure with WPM, and indication of significance." Same row: WPM corr "-0.84"; Fast "121.70 11.96"; Slow "481.03 123.36"; Trained "223.55 107.78"; Untrained "245.34 112.60".
3. p. 5, Results › Performance Measures: "Figure 2 shows the distribution of WPM, uncorrected error rate, IKI, and keypress duration over all participants."
4. p. 4, Preprocessing › Performance Measures: "If not otherwise noted, all keystrokes were included in the analysis." and "INTER-KEY INTERVAL (IKI) is the difference in timestamps between two keypress events. For IKI-based analysis, we removed keystrokes that were typed more than 5000 ms after the previous keystroke."
5. p. 4, Preprocessing and Data Analysis: "we include only participants who typed all 15 sentences and completed the demographic questionnaire. Of these, we exclude those with error rate > 25% and those with technical problems or cases of participants obviously getting distracted during sentences (IKIs of >50 s). This removed ∼12% of participants"
6. p. 5, Results: "The final dataset includes 136,857,600 keystrokes from 168,960 participants"
7. p. 3, Table 1 rows: "Physical keyboard 43.8% Rest on-screen (touch)" / "Laptop keyboard 54.15% or small physical keyboard"
8. p. 6, Differences between Hands: "Note that the left, right, alternation, and repetition IKI values are generally smaller than the overall average IKI, since their analysis excludes many slower bigrams, such as a letter following a space (word-initiation effect [34])."

**(b) Locators.** PDF p. 5 (Results text and Table 3), p. 4 (Performance Measures definitions, Preprocessing), p. 3 (Table 1), p. 6 (Differences between Hands). No printed page numbers.

**(c) Plain-words reading**
- **Values.** Mean IKI 238.656 ms (Table 3: 238.66), SD 111.6 ms (Table 3: 111.60), in milliseconds on the raw scale. The IKI is the key-down to key-down timestamp difference.
- **Unit the SD is over.** The paper never states in words whether the mean and SD are over keystrokes or over per-participant means. The text only says Figure 2 shows the distributions "over all participants". Two things point to per-participant averages: a fast-typist SD of 11 ms could not be a keystroke-level spread, and the phrase "slow typists have an IKI of over 480 ms, sometimes as high as 900 ms" describes participant-level values.
- **Check against the released data (a dataset check, not a statement in the paper).** The released `metadata_participants.txt` has a per-participant `AVG_IKI` column ("Average inter-key interval"). Over its 168,594 rows, AVG_IKI has mean 238.656 ms, SD 111.596 ms, skewness 1.979 and excess kurtosis 7.099. These reproduce the paper's 238.656 / 111.6 / 1.98 / 7.1 exactly. So the reported mean and SD are **the mean and SD across participants of each participant's average IKI**, and the skewness and kurtosis describe that across-participant distribution.
  - The released WPM column does *not* reproduce the paper's figure: AVG_WPM_15 has mean 50.65 (SD 20.22) against the paper's 51.56 (SD 20.2).
- **Keystrokes included.** All keys count, not just letters ("all keystrokes were included"), minus keystrokes more than 5000 ms after the previous one.
  - A spot check of six participants' raw keystroke files against their released AVG_IKI (dataset reconstruction, not in the paper) matched within-sentence key-down intervals with the 5000 ms cut to within about 0.04–2.8 ms. Including the gaps between sentences (all consecutive key-downs, no cut) would give values 42–120 ms higher. See C-dhakal-4.
- **Population.** 168,960 self-selected online volunteers (the released metadata has 168,594 rows) who completed all 15 sentences and the questionnaire. Participants with error rate > 25% or any IKI > 50 s were excluded.
  - Mostly teenagers and young adults, 68% from the US, 72% had taken a typing course.
  - Keyboards per Table 1: 43.8% "physical" (desktop), 54.15% laptop, the rest on-screen (touch) or small physical. The released metadata counts are full 73,759; laptop 91,250; small 1,886; on-screen 1,699.
  - Task: transcription of English sentences (C-dhakal-4).
- **Caveats.**
  - Timing precision is stated as about 10–15 ms per keypress (p. 3–4, p. 10).
  - The bigram-category IKIs (Left/Right/Alternation/Repetition) are averages over selected frequent bigrams, not the overall IKI.

**(d) Verdict: PARTIAL.** The mean, the dispersion statistic (SD) and the population are FOUND in the paper. The unit the SD is computed over is not stated in the paper's words. It is resolved by the released per-participant data, which reproduces the numbers exactly.

### C-dhakal-2: shape of the inter-key-interval distribution

**(a) Verbatim**

1. p. 5: "A lower bound of about 60 ms can be observed. The IKI distribution shown in Figure 2 has a skewness of 1.98 and kurtosis measure of 7.1."
2. p. 5, Figure 2 caption: "Histogram and density estimate of WPM, uncorrected errors, IKI, and keypress duration."
3. p. 5, keypress durations: "The distribution has a skewness of 0.8 and a kurtosis of 2.36, far less than the IKI distribution has."
4. p. 5, Results: "As the data are not normally distributed and sample sizes are unequal, we use Mann–Whitney U tests to assess differences between groups."
5. p. 7, Figure 5 caption: "IKI distribution of example bigrams typed with one hand (left), hand alternation (middle), and repetition (right). Distributions differ greatly between fast and slow typists for one hand and hand alternation but are similar for repetition. Trained and untrained typists show similar distributions."
6. p. 7, text: "We further explore this phenomenon by looking at the IKI distribution of specific bigrams across participants, shown in Figure 5. In the top part, we compare IKI distributions of fast and slow typists. For letter repetitions, their distributions are similarly narrow (but shifted)."
7. p. 10, Summary: "We found a lower bound for IKI at 60 ms; the same was found by Hiraga et al. for professional typists [14]."

**(b) Locators.** p. 5 (text and Figure 2, right panel, "Inter-key interval / Keypress duration (ms)"), p. 7 (Figure 5 and text), p. 10 (Summary).

**(c) Plain-words reading**
- **Figure 2, right panel (my visual reading of a 300 dpi render).** The IKI curve is a dashed density line on a 0–600 ms axis. It is zero below about 60–70 ms, has a single peak at about 150–170 ms, and a long right tail still above zero at 600 ms. It is unimodal and right-skewed, and there is no second mode.
- **What that curve is a distribution of.** The quoted skewness 1.98 and kurtosis 7.1 are reproduced exactly by the per-participant AVG_IKI column (C-dhakal-1). So Figure 2 and those shape statistics describe **the distribution across participants of per-participant average IKIs**. It is not the distribution of individual keystroke intervals. The paper does not plot or characterise a pooled keystroke-level IKI distribution.
  - For reference only (dataset, not paper): the across-participant median of AVG_IKI is 208.8 ms, and its mode region in Figure 2 sits around 160 ms.
- **Kurtosis convention.** The paper says only "kurtosis measure of 7.1". The dataset reproduction gives 7.099 as *excess* kurtosis (Fisher definition).
- **Figure 5.** This figure does show keystroke-level IKI histograms, but only for three example bigrams ("as", "an", "ll") split by typist group, over 0–500 ms. The fast-typist distributions are narrow. The slow-typist "as"/"an" distributions are broad and flat with long right tails, and the "ll" distributions are narrow for both groups.
- **Not in the paper.** No functional form (log-normal, gamma, mixture) is fitted or named for any IKI distribution.

**(d) Verdict: FOUND.** The paper gives descriptive shape statistics and plots, for the per-participant average IKI.

### C-dhakal-3: numbers of keystrokes and participants, and recruitment

**(a) Verbatim**

1. p. 5, Results: "The final dataset includes 136,857,600 keystrokes from 168,960 participants with, on average, about 810 keypresses per participant."
2. p. 3, Sampling and Participants: "Participants in the study were self-selected from the user base of the commercial site. Our typing test was advertised on their web site as a 'scientific alternative' to their regular typing test. Users coming to the page could choose between the standard one-minute typing test with a fixed piece of text and our experiment. The user base of the company is composed mainly of younger people from the US who are interested in testing and improving their typing skills."
3. p. 3: "Table 1 summarises the demographics of 168,960 voluntary participants who completed all 15 sentences and filled in the demographic questionnaire."
4. p. 3: "As is common in online volunteer studies [28, 31], ours had a high dropout rate: of ∼406,000 participants starting the study, only ∼193,000 finished the test and questionnaire. Of these, we excluded 12% as detailed below."
5. p. 3, Data Collection: "The test was launched globally on the Internet in collaboration with a commercial organisation offering online typing courses and typing tests." and p. 3, Implementation: "We collected data for a duration of three months."
6. p. 3, Task and Procedure: "Most importantly, the participants were rewarded with interesting statistics about their performance in comparison to others, which is the main motivation for participation in the study."
7. p. 10, Acknowledgements: "Data collection was supported by Typing Master, Inc."
8. p. 1, Abstract: "We report on typing behaviour and performance of 168,000 volunteers in an online study."

**(b) Locators.** p. 5 (Results, first paragraph), p. 3 (Data Collection, Sampling and Participants, Task and Procedure, Implementation), p. 10 (Acknowledgements), p. 1 (Abstract).

**(c) Plain-words reading**
- **Counts.** 136,857,600 keystrokes; 168,960 participants after exclusions (the abstract rounds to "168,000"). Before exclusions, about 406,000 started and about 193,000 finished, and 12% of those were excluded.
- **Arithmetic check.** 136,857,600 / 168,960 = 810.0 exactly, which matches "about 810 keypresses per participant".
- **Recruitment.** Self-selected, unpaid volunteers from a commercial typing-test site's user base (Typing Master, Inc. is named as supporting data collection). The study was offered on the site as a "scientific alternative" to the regular one-minute test, and participants' only reward was feedback on their own performance. Collection ran three months, globally.
- **Released dataset (dataset, not paper).** 168,593 per-participant keystroke files and 168,594 metadata rows, a few hundred fewer than the paper's 168,960.

**(d) Verdict: FOUND.**

### C-dhakal-4: typing task, handling of between-sentence pauses, pointing-device input

**(a) Verbatim**

1. p. 2, Assessment of Typing Performance: "The experimental task employed in this work is transcription typing, the act of typing sequences of characters by looking at an existing written record."
2. p. 3, Task and Procedure: "The task was to transcribe 15 English sentences. Participants were shown instructions stating to first read through and memorise a sentence, then type it as quickly and accurately as possible. Breaks could be taken between sentences." … "Upon pressing Enter, the next sentence was displayed."
3. p. 3, Figure 1 caption: "Participants were shown one sentence at a time, with progress presented at the top right."
4. p. 3, Materials: "Sentences were drawn randomly from a set of 1,525 sentences, composed of the Enron mobile email corpus [38] and English gigaword newswire corpus [11]." … "random sentences were chosen that contained at least 3 words and at maximum 70 characters, fewer than five numerical symbols, and only simple punctuation marks"
5. p. 3, Implementation: "We recorded participants' demographics, the sentences presented and transcribed, and keystroke data (timestamps for key down and up and the associated character)."
6. p. 4, Performance Measures: "WORDS PER MINUTE (WPM) is calculated for each typed sentence as the length of the string transcribed (in words, where one word consists of any five characters) divided by the time from the first to the last keypress (in minutes)."
7. p. 4: "INTER-KEY INTERVAL (IKI) is the difference in timestamps between two keypress events. For IKI-based analysis, we removed keystrokes that were typed more than 5000 ms after the previous keystroke."
8. p. 4, Preprocessing: "cases of participants obviously getting distracted during sentences (IKIs of >50 s)"
9. p. 4, Error Corrections: "Note that edit operations were not restricted to backspace; they allowed use of the mouse and arrow keys to select and delete many characters at once. From log data it is difficult to assess how often this happened."
10. p. 10, Limitations: "Although edit operations (for deletion) were not limited to backspaces and deletion keys (e.g. mouse/keyboard multiple selection and deletion was permitted), the error analysis did not take these into account, as there was no way to track such operations."
11. Dataset readme (`Keystrokes__files__readme.txt`, lines 55–62): "TEST_SECTION_ID Unique ID of the presented sentence" … "USER_INPUT Sentence typed by the user after pressing Enter or Next button" … "PRESS_TIME Timestamp of the key down event (in ms)" … "RELEASE_TIME Timestamp of the key release event (in ms)"

**(b) Locators.** p. 2 (Background), p. 3 (Figure 1, Task and Procedure, Materials, Implementation), p. 4 (Performance Measures, Preprocessing), p. 10 (Limitations); dataset readme lines 53–62.

**(c) Plain-words reading**
- **Task.** Transcription (copy typing), not free composition. Participants memorised and typed 15 short English sentences (at most 70 characters), shown one at a time, and pressed Enter to advance. Breaks were allowed between sentences.
- **Between-sentence pauses.** The paper does **not** say explicitly whether the interval from one sentence's last key to the next sentence's first key counts as an IKI. What it does state:
  - IKI-based analyses drop keystrokes more than 5000 ms after the previous keystroke.
  - Participants with any in-sentence IKI above 50 s are excluded.
  - WPM is per sentence, first to last keypress.
  - No other pause or threshold rule is stated.
- **Dataset reconstruction (not in the paper).** For six participants (100001, 100003, 100007, 100008, 100013, 213331), the released AVG_IKI (119.43, 173.29, 205.44, 197.91, 242.21, 167.98 ms) matches the mean of within-sentence key-down intervals with the 5000 ms cut (119.59, 174.83, 208.19, 199.59, 242.82, 168.02 ms) to within 0.04–2.8 ms. The mean of all consecutive key-down intervals, between-sentence gaps included and no cut, would be 190.11, 222.46, 262.28, 317.91, 284.38 and 247.04 ms respectively.
  - Inference from this small check: the released per-participant averages exclude between-sentence gaps. Within-sentence hesitations up to 5000 ms stay in.
  - The match is close but not exact, so the precise rule is not fully reproduced.
- **Pointing device.** Mouse use was allowed for editing, but the paper states it was not tracked ("there was no way to track such operations"). Only key-down/key-up timestamps and characters were logged, so no pointing-device input was recorded.

**(d) Verdict: PARTIAL.**
- Task: FOUND.
- Pointing device: FOUND (not recorded).
- Between-sentence pause handling: not stated in the paper. The only stated rules are the 5000 ms per-keystroke cut and the 50 s participant exclusion.
- Search method: full text searched for "pause", "sentence", "Enter", "5000", "50 s", "break".

### C-dhakal-5: dataset availability and licence

**(a) Verbatim**

1. p. 1, Abstract: "The code and dataset are released for scientific use."
2. p. 10, section "THE 136M KEYSTROKES DATASET": "The dataset (N > 168,000) and the code for the test are released at http://userinterfaces.aalto.fi/136Mkeystrokes. A subset is given in Supplementary Material."
3. Project page (`aalto-project-page.html`), Data section: "Text files of the keystrokes in a .zip file (1.4 GB zipped, 16 GB unzipped). The data contains the keystroke-by-keystroke entries typed by every participant. The package also includes a metadata file. See readme.txt for introduction and license. This data is free to use for research and non-commercial use with attribution to the authors."
4. Dataset readme, "LICENSE AND ATTRIBUTION" (lines 18–21): "You are free to use this data for non-commercial use in your own research or projects with attribution to the authors."
5. Dataset readme, line 87: "Note: For some users, Keystrokes are not logged or not displayed correctly. The corresponding javascript keycode is used instead."

**(b) Locators.** Paper p. 1 (Abstract) and p. 10 (dataset section). Project page, Data section. Readme lines 18–27 (licence and citation request) and 87.

**(c) Plain-words reading**
- **Availability.** The dataset is publicly downloadable today, no login needed. HEAD requests to `data/Keystrokes.zip` (1,572,785,433 bytes) and `resources/136m-keystrokes.zip` (the test code, 140,232,675 bytes) both return HTTP 200. The zip holds per-participant keystroke logs plus a participant metadata file with per-participant aggregates (AVG_WPM_15, AVG_IKI, ECPC, KSPC, AVG_KEYPRESS, ROR, demographics).
- **Licence.** The paper itself says only "released for scientific use". The licence terms are in the readme and on the project page: free for non-commercial use in research or projects, with attribution to the authors, citing the CHI '18 paper. No named standard licence (such as a Creative Commons licence) is given.
- **Paper's own licence (separate from the dataset's).** p. 1 carries the ACM "Copyright is held by the owner/author(s)" block, which allows personal/classroom copies.

**(d) Verdict: FOUND.** Availability is in the paper. The licence terms are in the dataset readme and project page, not the paper.

### C-dhakal-6: does the paper report a mixture model of IKIs, a fluent-component location, a pause probability, a pause-component location, or log-scale spreads?

**(a) Verbatim.** Nothing to quote for any of the five items. What the paper reports about IKIs instead (verbatim):
- p. 5: "Average inter-key interval is 238.656 ms (SD = 111.6). A lower bound of about 60 ms can be observed. The IKI distribution shown in Figure 2 has a skewness of 1.98 and kurtosis measure of 7.1."
- p. 4: "For IKI-based analysis, we removed keystrokes that were typed more than 5000 ms after the previous keystroke."
- p. 8, clustering: "Clustering refers to the identification of patterns whose distributions in feature space (here, normalised IKIs) are distinct."

**(b) Locators.** Whole paper (12 PDF pages), searched.

**(c) Plain-words reading.** The pypdf text of all 12 pages was searched, plus a visual check of Figures 2 and 5, for: "mixture" (0 hits), "log-normal"/"lognormal" (0), "log-" (0), "logarithm" (0), "log " (1 hit, "From log data", meaning log files), "Gaussian" (0), "bimodal" (0), "pause"/"Pause" (0), "median" (1 hit, the "median partitioning" clustering method), "mode " (0), "percentile" (1 hit, about error corrections).
- **Mixture model of IKIs:** not reported.
- **Fluent-component location:** not reported.
- **Pause probability:** not reported.
- **Pause-component location:** not reported.
- **Log-scale spreads:** not reported. All spreads are raw-millisecond SDs (Table 3), and no transformed-scale statistic appears.
- **What the paper reports instead.** Raw-scale means and SDs, both overall and by group (fast/slow, trained/untrained, 8 clusters). Also skewness, kurtosis, a roughly 60 ms lower bound, Pearson correlations with WPM, Mann–Whitney tests, Cohen's d, rollover ratio, and per-bigram IKI histograms. The only mixture-like analysis is k-medoids (PAM) clustering of participants on normalised bigram IKIs, which clusters typists, not keystroke intervals.
- **For any use of this paper as a source of those five quantities: PREMISE NOT IN SOURCE.**

**(d) Verdict: NOT FOUND** (all five items; search method above).

---

## roeser-rw24

### C-roeser-1: the model fitted to IKIs, distribution family, number of components, and whether alternatives were compared

**(a) Verbatim**

1. VoR p. 10–11 / MS p. 16 (Typing as mixture process): "For keystroke data, the assumed process is a combination of two processes: (1) normal typing, when activation flows smoothly from higher into lower levels; (2) typing disfluencies, when activation flow is interrupted at higher levels (e.g. for a buffer update). In other words, we fixed the number of underlying distributions to two, namely 2 log-Gaussian (log-normal) distributions, of which one represents fluent typing—shorter IKIs—and the other represents disfluencies—longer IKIs."
2. MS p. 16–17 / VoR p. 11: "The first and second line express that the data y are modelled as the sum of two weighted log-normal distributions: The first distribution has a weight – called mixing proportion – of θ and the other distribution receives a weight of 1−θ. The mixing proportion of both distributions must sum to 1. In this parameterisation, θ represents the unknown probability of process disfluencies. This was achieved by using an identical mean β for both distributions but adding a parameter δ, that was constrained to be positive, to the first distribution."
3. Eq. 7, MS p. 17 / VoR p. 11: "yij∼θi·LogNormal(β+δ+ui+wj, σ²e′) + (1−θi)·LogNormal(β+ui+wj, σ²e) where δ∼Normal(0,1) constraint: δ>0"
4. Eq. 10, MS p. 19 / VoR p. 12: "yij∼θi·LogNormal(β+δ+φi·log(yij−1)+ui+wj, σ²e′) + (1−θi)·LogNormal(β+φi·log(yij−1)+ui+wj, σ²e)"
5. MS p. 18 / VoR p. 11–12: "we constrained the variance σe′ associated with the distribution of typing disfluencies to be larger than the variance for normal typing σe; see equation 9"
6. Table 1, VoR p. 12 / MS p. 19: "M1 LMM 1 Baseline model / M2 AR 6 Autocorrelation between subsequent IKIs / M3 MoG 7 Mixture process of fluent and disfluent typing / M4 AR + MoG 10 As M3 but with autocorrelation component". Note: "All models were fitted with random intercepts for participants and bigrams".
7. VoR p. 15–16 / MS p. 24–25: "The predictive performance of the models was established using leave-one-out cross-validation." … "Model comparisons revealed higher predictive performance for both mixture models M3 and M4 for both copy-task components. The increase in predictive performance is larger for the LF bigrams task compared to the consonants task." … "For both tasks, the combination of the mixture model and the autoregressive-process model as implemented in model M4 (see Eq. 7) revealed the highest predictive performance with a small advantage over mixture model M3 (see Eq. 10). We therefore chose model M4 for parameter evaluation of both copy-task components."
8. Table 2 (VoR p. 16 / MS p. 26), Δelpd (SE):
   - Consonants: M3 "−38 (7)", M2 "−264 (25)", M1 "−318 (25)".
   - LF bigrams: M3 "−30 (8)", M2 "−1011 (64)", M1 "−1025 (64)".
9. VoR p. 18 / MS p. 30: "To test this possibility we also implemented two models that are largely identical to model M3 (see Eq. 7): first, we allowed both the disfluency probability θ and the disfluency magnitude δ to vary by participant; second, δ but not θ was allowed to vary by participant. We compared the predictive performance of either model to model M3. Neither model was convincingly better than model M3, neither for the consonants task nor for the LF-bigrams task."
10. Footnote 3, VoR p. 7 / MS p. 11: "We discussed above that the heavy tail associated with keystroke data is not necessarily fitting a log-normal distribution. We use a log-normal models as this is equivalent to the standard statistical method used in the field (e.g. fitting parametric models to log-transformed data)."
11. VoR p. 22–23 / MS p. 36–37 (Discussion): "If the size of the disfluency is assumed to depend on the inhibited process upstream or combination of processes, this can be implemented as additional mixture component(s)"

**(b) Locators.** Method sections "Log-normal mixed-effects model of typing", "Typing as autoregressive process", "Typing as mixture process" and "Typing as autoregressive mixture process" (Eq. 1–10, Table 1): MS pp. 11–19 / VoR pp. 7–12. "Model fit" and Table 2: MS pp. 24–26 / VoR pp. 15–16. Extra model variants: MS p. 30 / VoR p. 18.

**(c) Plain-words reading**
- **Family.** Log-normal. The final model (M4) is a **two-component mixture of log-normals** fitted by Bayesian hierarchical estimation in Stan (3 chains, 30,000 iterations with 15,000 warm-up).
  - **Fluent component:** location β + φ_i·log(previous IKI) + u_i + w_j, with scale σ_e.
  - **Disfluent component:** the same location plus δ > 0, with a larger scale σ_e′.
  - **Weights:** participant-specific θ_i (disfluent) and 1 − θ_i (fluent).
  - **Random intercepts:** participants (u_i) and bigram *positions/identities* (w_j).
  - **Autoregression:** a by-participant first-order coefficient φ_i on the log of the previous IKI.
- **Number of components.** Fixed at two by the authors; the number was not selected from the data. Only one-component models (M1, M2) and two-component models (M3, M4) were compared, so no three-or-more-component model was fitted. More components are raised only as future work for free composition.
- **Alternatives compared.** Yes: M1 log-normal LMM, M2 autoregressive log-normal, M3 mixture, M4 mixture plus autoregression, compared by PSIS-LOO expected log predictive density.
  - M4 was best for both tasks, narrowly ahead of M3 and far ahead of the one-component models.
  - Two further M3 variants (δ varying by participant, with and without θ varying) were not convincingly better.
- **Fitted to what.** Key-down to key-down IKIs, with spaces and editing operations removed, from 250 participants aged 18–25 doing the Dutch Inputlog copy task. Two sub-tasks were fitted separately (see C-roeser-4).
- **Caveats.**
  - **Cross-reference slip.** The text's cross-references for M3/M4 are swapped: it says "M4 (see Eq. 7)" and "M3 (see Eq. 10)", while Table 1 assigns Eq. 7 to M3 and Eq. 10 to M4.
  - **Prior mismatch.** The deposited Stan file `ARKMoGpptbgs.stan` (OSF) sets `beta_mu ~ normal(5, 1)`, `tau_phi ~ normal(0, 3)` and `tau_theta ~ normal(0, 2.5)`. The paper states μβ ∼ Normal(5, 2), η ∼ Cauchy(0, 1) and τ ∼ Cauchy(0, 1).
  - **Missing code.** The fitting scripts on OSF (`scripts/consonants/ARKMoGpptbgs.R`, `scripts/LF/ARKMoGpptbgs.R`) load `stanin/ARKMoGpptbgs2.stan`, and no file of that name is in the OSF deposit (full listing checked). So the exact Stan code behind the reported fits is not available for inspection.

**(d) Verdict: FOUND.**

### C-roeser-2: fitted location of the fluent component per task, scale, and which statistic

**(a) Verbatim**

1. VoR p. 16 / MS p. 25: "Table 3 summarises the population and variance estimates as posterior mean with 95% probability intervals (PI). Estimates are shown for the LF-bigrams task and the consonants task. After accounting for process disfluencies, keystroke intervals were longer for the consonants task (429 msecs, PI: 356–515) compared to the LF-bigrams task (158 msecs, PI: 139–180)."
2. Table 3, VoR p. 17 / MS p. 27, columns "LF bigrams / Consonants":
   - "β (fluent typing) 158 [139, 180] 429 [356, 515]"
   - "δ (disfluency slowdown) 95 [76, 116] 414 [333, 509]"
   - "θ (disfluency probability) 0.34 [0.31, 0.38] 0.73 [0.66, 0.8]"
   - "φ (autoregressor) 0 [-0.02, 0.02] -0.08 [-0.1, -0.05]"
   - "Variance estimates": "σ² (residual error) 0.73 [0.7, 0.75] 0.54 [0.52, 0.56]"; "σ²e (fluent typing) 0.29 [0.27, 0.3] 0.29 [0.26, 0.32]"; "σ²e′ (disfluency) 1.16 [1.12, 1.21] 0.79 [0.77, 0.81]"; "η² (autoregressor) 0.04 [0.04, 0.05] 0.01 [0, 0.02]"; "σ²u (between-participants) 0.03 [0, 0.08] 0.27 [0.23, 0.31]"; "σ²w (between-bigrams) 0.22 [0.17, 0.3] 0.24 [0.17, 0.33]"
   - Caption: "Parameter estimates with 95% PIs separated into population estimates and estimates for variance components."
3. MS p. 12 / VoR p. 8: "The population mean is then captured by the parameter β after accounting for variance associated with participants and bigrams."
4. MS p. 13 / VoR p. 9: "The parameter of interest, the mean β in equation 1, is the marginalised value after taking into account random variation between participants and bigrams."
5. MS p. 13–14 / VoR p. 9 (prior on β): "we used a prior that is normally distributed around a value of 5 log msecs (i.e. ≈150 msecs) with a variance of 2 log msecs which is putting the majority of prior probability of the true parameter for fluent key transitions between ≈80 msecs and ≈215 msecs"
6. MS p. 16–17 / VoR p. 11: "In other words the population mean of the first distribution is β+δ but only β for the second distribution."
7. Eq. 10 (MS p. 19 / VoR p. 12): the fluent component is "(1−θi)·LogNormal(β+φi·log(yij−1)+ui+wj, σ²e)".
8. VoR p. 17 / MS p. 27: "Further autocorrelation between subsequent keystrokes was non-different from zero in the LF-bigrams task; keystroke transitions in the consonants task were in general followed by a –0.08 times faster keystroke transition; PI: –0.10 to –0.05."
9. Authors' OSF walkthrough (`walkthrough.Rmd`, lines 341 and 358–363, a companion document fitting a related model, not the paper's Table 3 code): "The values for $\beta$ and $\delta$ are shown on a log-scale. To transform their values back to msecs we can extract the posterior samples" … "This code is then transforming `beta` and `delta` to msecs using the exponential function `exp` to un-log the values. In order to transform the slowdown `delta` into msecs we need to add `beta` before using the exponential function; we can then subtract beta again." with code "delta = exp(beta + delta) - exp(beta), beta = exp(beta),"

**(b) Locators.**
- Results › Parameter evaluation: MS p. 25 / VoR p. 16.
- Table 3: MS p. 27 / VoR p. 17.
- Model definitions (Eq. 1, 4, 7, 10): MS pp. 12–19 / VoR pp. 8–12.
- OSF `walkthrough.Rmd` lines 338–365.
- OSF `markdown/manuscript.Rmd` lines 470–496, which build Table 3 by `source("scripts/get_posterior_table.R")`; that script is **not** in the OSF deposit (complete listing in `roeser-osf-listing.json`).

**(c) Plain-words reading**
- **Reported fluent location (model M4, population level).** LF-bigrams task 158 ms [95% PI 139, 180]; consonants task 429 ms [356, 515].
- **Statistic.** The paper states these are **posterior means with 95% probability intervals**.
- **Scale.** In the model, β is a **log-scale** parameter: the location of a log-normal, i.e. the mean of log-IKI for the fluent component. The paper calls it the "population mean" and gives its prior in "log msecs". Table 3 nevertheless reports β in **milliseconds**, so a back-transformation was applied, but the paper does not say which one.
- **The transformation (partly inference).** The authors' companion walkthrough back-transforms each posterior draw with exp(β), and gives the slowdown as exp(β+δ) − exp(β), before averaging.
  - Inference: Table 3's "158"/"429" are probably posterior means of exp(β), and "95"/"414" posterior means of exp(β+δ) − exp(β).
  - Evidence for this: the slowdown ratio quoted in the text ("about four times longer": 414/95 ≈ 4.4) is on the millisecond scale.
  - Not confirmed: the Table 3 script is not deposited.
- **Mean or median in millisecond terms (inference; standard log-normal algebra, not stated in the paper).**
  - exp(location) of a log-normal is its **median**, not its mean. The mean would be exp(location + σ²/2).
  - So exp(β) is the median of the fluent component for a participant with u_i = 0 and a bigram with w_j = 0, and (see next point) with φ_i·log(y_prev) = 0.
  - The paper reports no millisecond mean of the fluent component.
- **Autoregressive term (inference from the paper's own Eq. 10 and the deposited Stan code).**
  - In M4 the lag term φ_i·log(y_{i,j−1}) enters the location uncentered. The deposited Stan code uses `logy = log(y)`, and the paper writes log(y_{ij−1}). So β is the intercept at log(previous IKI) = 0, i.e. a previous IKI of 1 ms.
  - **LF task:** φ ≈ 0 [−0.02, 0.02], so this barely matters at the posterior mean.
  - **Consonants:** φ = −0.08. Illustrative arithmetic, not in the paper: with a previous IKI of 429 ms, the location shifts by −0.08 × ln 429 ≈ −0.49, so the fluent-component median would be about 429 × e^−0.49 ≈ 265 ms.
  - So the 429 ms figure should not be read directly as the typical fluent IKI in the consonants task without accounting for the lag term. The paper itself reads it as fluent typing speed ("keystroke intervals were longer for the consonants task (429 msecs…)").
  - The Stan file actually run (`ARKMoGpptbgs2.stan`) is not deposited, so the centring could differ in it.
- **Spread of the fluent component.** Table 3 gives "σ²e (fluent typing)" 0.29 for both tasks, on the log scale.
  - Inference: the tabulated numbers behave like **SDs (scale parameters), not variances**. Eq. 9 defines σe′ = σ + σdiff and σe = σ − σdiff, so σ = (σe′ + σe)/2 on the SD scale, and posterior means preserve this linear relation.
  - The table values satisfy it: LF (1.16 + 0.29)/2 = 0.725 ≈ 0.73; consonants (0.79 + 0.29)/2 = 0.54. The squared quantities would not.
  - The deposited Stan code also passes `sigma_e`/`sigmap_e` as the log-normal scale (SD) argument.
  - So the "σ²" labels in Table 3 appear to mislabel log-scale SDs. Not confirmed, because the table script is missing.
- **Population and filtering.**
  - 250 randomly sampled participants (175 female, 71 male, 4 unknown), aged 18–25 (median 22), from the Dutch Inputlog copy-task corpus. Participants are the same across both tasks.
  - Key-down to key-down intervals; spaces and editing operations excluded; LF task restricted to the first of seven repetitions of "een chaotische cowboy".
  - Consonants task: one pass of "tjxgfl pgkfkq dtdrgt npwdvf".
  - No pause threshold; no trimming is described.
  - The OSF `get_data.R` (code, not paper) additionally keeps session 1, IKI > 0 and age 18–25. It drops participants missing a task component and those whose bigram count exceeds 1.75 × the component mean, then samples 250 with seed 125.
- **Other caveats.**
  - These are not transcription-of-sentences IKIs. They are within-word IKIs in two short copy strings, one a non-lexical consonant string.
  - The LF task's `extract_posterior.R` on OSF writes a file named `LF_posterior_MoG.csv` and does not extract φ, yet Table 3 reports φ for LF. The provenance of the LF column cannot be fully traced from the deposit.

**(d) Verdict: PARTIAL.**
- The values, their unit (msecs), the parameter's log-scale definition and "posterior mean with 95% PI" are FOUND.
- The paper does not state the log-to-millisecond transformation. The Table 3 script is absent from the deposit, and the walkthrough's exp-per-draw method is inference by analogy.
- That exp(β) is a conditional median, and that the consonants figure is an intercept at log(previous IKI) = 0, are inferences, labelled as such above.

### C-roeser-3: mixing proportion of the slower component per task, and its interpretation

**(a) Verbatim**

1. Table 3 (VoR p. 17 / MS p. 27): "θ (disfluency probability) 0.34 [0.31, 0.38] 0.73 [0.66, 0.8]" (LF bigrams, Consonants).
2. VoR p. 16–17 / MS p. 25: "For the LF-bigrams task, the model determined a slowdown of 95 msecs (PI: 76–116) with a probability of 0.34 (PI: 0.31–0.38); for the consonants task we found a slowdown of 414 msecs (PI: 333–509) with a probability of 0.73 (PI: 0.66–0.80). In other words, in the consonants disfluent keystroke transitions were three times more likely to occur than fluent transitions; in the LF-bigrams task, only one out of three transitions constitutes a disfluency."
3. VoR p. 17 / MS p. 25: "The size of the slowdown in the consonants task suggest higher level processes such as reading of the target string. This is unlikely to be the case for the short slowdown in the LF-bigrams task. Instead, the slowdown in the LF-bigrams task might be a bigram-frequency effect. Four out of 16 bigrams in the LF-bigrams have a low frequency (i.e. 4/16≈0.19). In other words, the magnitude for disfluencies and hence their cognitive source in the typing process is task-specific."
4. MS p. 17 / VoR p. 11: "The δ parameter is therefore capturing the hesitation size of process disfluencies with θ indicating the probability of disfluencies to occur. The probability of disfluent IKIs was allowed to vary across participants i and stored in θi. This is because the probability to exhibit disfluencies can be assumed to depend on individual typing style (and skills)."
5. Eq. 8 (MS p. 18 / VoR p. 11): "θi = Logit−1(αi) αi∼Normal(µα,τ²) µα∼Normal(0,1) τ∼Cauchy(0,1)"; text MS p. 17 / VoR p. 11: "a mean µα that captures the logit of the population disfluency-probability"
6. Discussion, VoR p. 20 / MS p. 33: "From the present analysis we know that merely one-quarter of the data from the consonants task and two-thirds of the data from the LF-bigrams task were found to correspond to fluent keystroke transitions."
7. VoR p. 21 / MS p. 34: "However, our results did not support a trade-off between typing speed and disfluency probability. This might be because disfluencies are not merely the result of a memory-representation update but are also related to difficulty finding the correct key and individual memory-span differences. Therefore the disfluency probability can be understood as an estimate for all non-typing related activities. As such the disfluency probability may be an indicator of memory span (Grabowski et al., 2010; Olive, 2014), low level reading skill (De Smet et al., 2018) and individual typing skills."
8. Footnote 7 (VoR p. 20 / MS p. 31–32): "This model is just one possibility of how the mixture-model parameters map onto copy-typing. Disfluencies might as well arise on a lower level, for example, when the typist is struggling to find the correct key."
9. Figure 6 caption (VoR p. 19 / MS p. 32): "Disfluencies are the sum of α and δ, where δ is the additional time that results from updating the letters buffered for motor encoding. The probability of disfluencies is indicated as θ mapping onto looks to the target string."

**(b) Locators.** Table 3 (MS p. 27 / VoR p. 17). Parameter evaluation text (MS p. 25 / VoR pp. 16–17). Eq. 7–8 (MS pp. 16–18 / VoR p. 11). Discussion (MS pp. 31–34 / VoR pp. 19–21). Figure 6.

**(c) Plain-words reading**
- **Values (M4, population level).** θ is the weight on the slower (disfluent) component, reported as posterior mean [95% PI] on the probability scale:
  - LF bigrams: 0.34 [0.31, 0.38]
  - Consonants: 0.73 [0.66, 0.80]
- **What θ is, per Eq. 7.** The weight on LogNormal(β+δ+…), the component with the larger location and larger scale.
  - In the deposited Stan code, `prob = 1 - inv_logit(theta)` and `prob_s = 1 - inv_logit(theta_s)`, and `log1m_inv_logit(theta_s)` weights the β+δ component. So the "probability" is the disfluent weight, and Table 3's θ corresponds to `prob`.
- **Population value versus average of participants (inference).** The population θ appears to be the inverse-logit of the population logit mean. That is the disfluency probability of a typical participant, not the average of the 250 participants' θ_i. The paper does not state which.
- **The paper's interpretation of the slower component.**
  - "Typing disfluencies", i.e. interrupted activation flow at higher levels, such as a buffer update after re-reading the target string.
  - In the consonants task, the large slowdown "suggest[s] higher level processes such as reading of the target string". In the LF task, it "might be a bigram-frequency effect".
  - In the Discussion, θ is read as "an estimate for all non-typing related activities", possibly indexing memory span, low-level reading skill and typing skill.
  - Footnote 7 allows that disfluencies may also be lower level (key-finding).
- **Complement.** Fluent share is about 0.27 (consonants) and 0.66 (LF), matching the Discussion's "one-quarter" and "two-thirds".
- **Caveat: symbol clash.** Figure 6 uses α for the fluent IKI, which collides with α_i as the logit of θ_i in Eq. 8.

**(d) Verdict: FOUND.**

### C-roeser-4: whether and how the fitted parameters differ across tasks

**(a) Verbatim**

1. VoR p. 13 / MS p. 20: "In this analysis we focus on the consonants task and the low-frequency (LF) bigrams task." … "We repeated the analysis for the LF-bigrams task to contrast the non-lexical consonants task and a more natural lexical copy task."
2. VoR p. 16 / MS p. 25: "After accounting for process disfluencies, keystroke intervals were longer for the consonants task (429 msecs, PI: 356–515) compared to the LF-bigrams task (158 msecs, PI: 139–180). The slowdown for disfluencies was about four times longer for the consonants task."
3. VoR p. 18 / MS p. 30: "The correlations show that individuals with longer keystroke intervals for the LF-bigrams task also show longer keystroke intervals in the consonants task (Fig. 5c); a similar relationship can be seen for autoregression although in the consonants task participants generally show faster keystroke intervals across bigrams while for the LF bigrams task some participants speedup and other slowdown (Fig. 5d). No such correlation was found for the disfluency probability (Fig. 5e). Participants that exhibit many disfluencies in the consonants task do not necessarily show more disfluencies in the LF-bigrams task. In other words, the model parameters do not just capture individual differences but also task-specific differences with regards to typing speed and pausing behaviour."
4. VoR p. 17 / MS p. 28: "Although, on the population level, disfluencies are likely to occur in the consonants task, not all all participants show a more disfluent than fluent keystrokes (as indicated by individual estimates below 0.5 in Fig. 5b representing a larger probability of fluent keystroke transitions) or more disfluencies in the consonants task than in the LF-bigrams task. In fact, some participants paused more often in the LF-bigrams task than in the consonants task (see Fig. 5e)."
5. VoR p. 19 / MS p. 31: "Overall, the values of the three process-central model parameters—fluent typing speed, disfluency probability, and slowdown magnitude for disfluencies—were found to be task sensitive. The LF-bigrams task shows shorter typing intervals, a lower disfluency probability compared to the consonants task and a shorter slowdown magnitude for typing disfluencies. Individual typing style was characterized by random variation in typing speed and in the probability but not in the magnitude of process disfluencies."
6. VoR p. 20 / MS p. 33: "Even after accounting for disfluent keystroke transitions, fluent typing was found to be two times slower in the consonants task compared to the LF-bigrams task." … "Across participants the probability of typing disfluencies was relatively homogeneous in the LF-bigrams task but showed a larger variability in the consonants task. Similarly the average by-participant typing speed was more diverse in the consonants task compared to the LF-bigrams task."
7. VoR p. 18 / MS p. 30: "For the consonants data, allowing δ and θ to vary by participant resulted in negligibly better predictive performance compared to model M3 (Δelpd=7, SE=4); holding the disfluency probability θ constant while allowing the disfluency magnitude δ to vary by participant revealed a lower predictive performance (Δelpd = −100, SE=50). The same patterns was found for LF bigrams: allowing δ to vary rendered no predictive gain (Δelpd=−1, SE=0.5); fixing θ and allowing δ to vary showed a decrease in predictive performance (Δelpd=−30, SE=8)."

**(b) Locators.** Copy-task data (MS p. 20 / VoR p. 13). Parameter evaluation and Table 3 (MS pp. 25–31 / VoR pp. 16–19). Figure 5 (MS p. 29 / VoR p. 18). Discussion (MS p. 33 / VoR p. 20). Table 2 (MS p. 26 / VoR p. 16).

**(c) Plain-words reading.** The two conditions are two copy-task components done by the same 250 participants: LF bigrams (lexical phrase, first repetition only) and consonants (non-lexical string). Posterior means [95% PI], LF vs consonants, from Table 3:

| parameter | LF bigrams | consonants |
|---|---|---|
| fluent β | 158 ms [139, 180] | 429 ms [356, 515] (about 2.7×; the Discussion says "two times slower") |
| slowdown δ | 95 ms [76, 116] | 414 ms [333, 509] (about 4×) |
| disfluency probability θ | 0.34 [0.31, 0.38] | 0.73 [0.66, 0.80] |
| autoregressor φ | 0 [−0.02, 0.02] | −0.08 [−0.10, −0.05] |
| between-participant σ²u | 0.03 [0, 0.08] | 0.27 [0.23, 0.31] |
| σ²e′ (disfluent spread) | 1.16 | 0.79 |
| σ²e (fluent spread) | 0.29 | 0.29 |

- **Direction.** All three central parameters are larger in the consonants task, with non-overlapping PIs.
- **Participant rank order across tasks.** It carries over for fluent speed and the autoregressor (correlations in Fig. 5c–d) but not for disfluency probability (Fig. 5e).
- **Which parameters vary between participants.** Model comparison indicates that θ, not δ, varies across participants.
- **How the comparison was made.** The two tasks were fitted as **separate models**: Table 2 gives separate elpd per task, and the OSF scripts filter on `component == "Consonants"` / `"LF"`. The paper reports **no formal posterior contrast** (difference distribution) between tasks. Its "task sensitive" conclusion rests on comparing the separate posteriors and PIs.
  - The OSF walkthrough does compute task differences, but for a different, jointly fitted demonstration model, and those numbers are not in the paper.
- **Caveat (inference).** Because of the uncentered lag term (C-roeser-2), the consonants β comparison mixes in φ = −0.08, while LF has φ ≈ 0. The raw 158 vs 429 contrast is therefore not a like-for-like comparison of median fluent IKIs.

**(d) Verdict: FOUND.**

### C-roeser-5: authors, title, journal, volume/pages/year, DOI; data and code availability

**(a) Verbatim**

1. VoR p. 1: "Reading and Writing" / "https://doi.org/10.1007/s11145-021-10203-z" / "Modelling typing disfluencies as finite mixture process" / "Jens Roeser1 · Sven De Maeyer2 · Mariëlle Leijten3 · Luuk Van Waes3" / "Accepted: 11 August 2021" / "© The Author(s) 2021"
2. VoR p. 1, affiliations: "1 Department of Psychology, Nottingham Trent University, 50 Shakespeare St, Nottingham NG1 4FQ, UK" / "2 Department of Education and Training Sciences, University of Antwerp, Antwerp, Belgium" / "3 Department of Management, University of Antwerp, Antwerp, Belgium"
3. Springer landing page (Wayback 2024-11-16): "Open access Published: 24 August 2021 Volume 37 , pages 359–384, ( 2024 )" and "Accepted : 11 August 2021 Published : 24 August 2021 Issue Date : February 2024 DOI : https://doi.org/10.1007/s11145-021-10203-z"
4. Crossref record (fetched 2026-09-13): volume "37", issue "2", page "359-384", published-print 2024-02, published-online 2021-08-24, licence "https://creativecommons.org/licenses/by/4.0".
5. VoR p. 15 / MS p. 24: "Data, R scripts and Stan code are available on OSF (osf.io/y3p4d). A detailed walkthrough document shows how R can be used to apply the Stan code of a mixture model to copy-task data (rpubs.com/jensroes/765467)."
6. VoR p. 12–13 / MS p. 19: "The copy-task corpus consists of keystroke data collected via a Javascript-based web application as part of Inputlog 8 (available on www.inputlog.net) with the source code released on github.com/lvanwaes/Inputlog-Copy-Task and zenodo.org/record/2908966."
7. VoR p. 23: "Open Access This article is licensed under a Creative Commons Attribution 4.0 International License, which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if changes were made."

**(b) Locators.** VoR p. 1 (title block), p. 15 (OSF statement), pp. 12–13 (corpus source), p. 23 (licence). Springer landing page capture (bibliographic block). Crossref JSON. OSF node y3p4d (API).

**(c) Plain-words reading**
- **Authors:** Jens Roeser, Sven De Maeyer, Mariëlle Leijten, Luuk Van Waes.
- **Title:** "Modelling typing disfluencies as finite mixture process".
- **Journal:** *Reading and Writing*, vol. 37, issue 2, pp. 359–384, issue dated February 2024. Published online 24 August 2021 (accepted 11 August 2021).
- **DOI:** 10.1007/s11145-021-10203-z.
- **Entry check.** The bibliographic entry given (authors, title, *Reading and Writing* 37, 359–384, 2024, DOI) matches all primary metadata. The issue number (2) is not in the entry. Year-of-record choice: online 2021, issue 2024.
- **Article licence:** CC BY 4.0.
- **Data and code.** The paper points to OSF osf.io/y3p4d. The project is public, and its licence per the OSF API is **CC0 1.0 Universal**. The OSF listing (checked today) contains:
  - `data/ct.csv` (86.5 MB)
  - R fitting scripts for both tasks
  - Stan models (`stanin/`)
  - `markdown/manuscript.Rmd`
  - the walkthrough (Rmd, html, example data, `MoG.stan`)
  - `manuscript.pdf` (identical to the NTU author manuscript)
- **Gaps in the deposit.** It lacks `stanin/ARKMoGpptbgs2.stan`, which both M4 fitting scripts load, and the `scripts/get_posterior_*.R`, `get_loo_table.R` and `get_descriptives_plot.R` files that `manuscript.Rmd` sources to build Tables 2–3 and the figures. Fitted model outputs (`stanout/`) are not deposited either.
- **Upstream data collection.** The Inputlog copy-task software is cited on GitHub and Zenodo (not fetched in this read).

**(d) Verdict: FOUND.**

---

## Verdict counts

| verdict | count | topics |
|---|---|---|
| FOUND | 7 | C-dhakal-2, C-dhakal-3, C-dhakal-5, C-roeser-1, C-roeser-3, C-roeser-4, C-roeser-5 |
| PARTIAL | 3 | C-dhakal-1, C-dhakal-4, C-roeser-2 |
| NOT FOUND | 1 | C-dhakal-6 |
| PREMISE NOT IN SOURCE | 0 | none (C-dhakal-6 notes that any claim this paper supplies mixture or pause parameters would be PREMISE NOT IN SOURCE) |
| COPY UNREACHABLE | 0 | none |
