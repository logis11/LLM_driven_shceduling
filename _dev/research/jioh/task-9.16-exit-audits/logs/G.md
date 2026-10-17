# 9.16 docs chunk G — the dataset guidebook

Files: `docs/guidebook/dataset/01-the-big-picture.md` (vol 01), `02-the-archetype-library.md` (vol 02), `03-timeline-to-canonical-workload.md` (vol 03), `04-the-coreset.md` (vol 04), `05-the-generated-layer.md` (vol 05), `06-grounding-measurement-verification.md` (vol 06), `08-decision-chronicle.md` (vol 08). Vol 07 and the guidebook README: no finding located there. Every changed volume's header already read `Updated 2026-10-17`. Not committed. Line numbers below are the current working-tree lines (they match `928aa8fd` except where vol 08 grew after 12.2).

## Trace audit, outside the dataset (`claims/outside-findings.md`, parts E and F), with the blind re-reads B3 and B4 winning where they differ

- **E-13** (the "five tabs in one window" reading of `glam`). vol 01:598 and vol 03:419: restated to B4's fix — the median client's largest number of tabs open across all windows, 4.67, rounded to five, with a median window maximum of 1.
- **E-16** (rt-app "widely used", time in µs). vol 03:244 and the glossary row vol 03:2397: "널리 쓰는" dropped; task-event times (run, sleep, timer period, deadline parameters) are integer µs, the use case's duration in seconds (B4).
- **E-17** (blind only, B4 WORDING-FIX; the periodic tools that "skip by default"). vol 01:289 and vol 02:137: interbench and the ROS 2 executor (and, in vol 02, Lipari and Palopoli's soft real-time thread, their Listing 2) skip late periods; rt-app's default re-anchors its timer to the late instant; none re-runs the missed periods. Not changed: vol 03:1196 (states the list D3 itself cited, then D17's correction), vol 08:1144 and :1656 (state what 9.11 D17 said; F-52 at those lines is SUPPORTED).
- **B4 observation 1** (Chromium's fake audio worker does say which tick a late job carries). vol 02:137: the worker runs one late callback with the earliest overdue tick's time, not the most recent one this rule picks, then jumps past now (`fake_audio_worker.cc`); Vulkan's FIFO mode left as "does not say". Applied because the passage contradicts the sentence; B4 marks it not blind.
- **E-18, E-42–E-47, E-54, F-52, F-56, F-58–F-60** (record below standard): the blind re-reads B3 and B4 found them SUPPORTED; their records now exist. No text change.
- **E-20, E-52, E-53, F-13, F-19**: SUPPORTED in B4. No change.
- **E-21** (SWELL-KW's 15.6 ms quantisation, no record). vol 02:537: stated as our reading of the extracted stream; the SWELL-KW material read does not state the timestamp resolution; the `sources.yaml` notes quote removed (the notes are the data chunk's). Left: the summary rows vol 01:1215 and vol 06:1692 ("15.6 ms 양자화", a property of the stream, not attributed to a source) and vol 06:1339 (a quoted table).
- **E-28** (the 1.4 schedules per wake under slide 14; B4 NOT IN SOURCE). vol 04:1919: a sentence after the quote — 1.4 is 9.4 D9's arithmetic 1/(1 − 0.2878) on slide 14's `sched_preempt` share, not a slide value. vol 02:730 (same claim): "that share, computed by 9.4 D9, our arithmetic".
- **E-29** (stale "Valve ships it" quote). vol 02:689: paraphrases `docs/workload/grounding-sources.md:30` as it now reads in the working tree (another chunk's A-09 fix): Valve holds the copyright of LAVD's code and ships it in SteamOS 3.8 as a scheduler the user selects. No "sponsors" (B4).
- **E-38** (interbench Burn "until it is done"; B4 NOT IN SOURCE). vol 02:1044: the line is the repository's own (`docs/data-contracts.md`), grounded on interbench's Burn load (fully CPU-bound threads that run until the benchmark stops them).
- **E-50** (González and Mark's populations). vol 01:1057: 3 min 08 s excludes formal meetings and unknown/personal events; 11 min 28 s is central and peripheral spheres only (B4's wording).
- **E-51**: B4 SUPPORTED (the paper's own phrase). vol 03:603 and vol 04:1564 not changed; the blind re-read wins over the trace fix.
- **E-55** (Spotify's account). vol 04:732: the account reason dropped; the reason is 9.10 D24's, the program `audio-player` observed is mpv.
- **F-08** (runner spec in quotation marks). vol 05:1979 and vol 08:1595: unquoted, as the table's row: processor 4, memory 16 GB, storage (SSD) 14 GB. vol 08:1595 also "저장 공간" → "사양".
- **F-14** ("no 60 fps on any slide"). vol 06:70 and vol 08:746: no slide states 16.7 ms, a frame budget or a 60 fps target; an uncommented 60 FPS / 16.5 ms readout appears only in slide 29's benchmark screenshot. Same wording fixed at vol 02:720, where the critical-findings memo's sentence is quoted ("확인했습니다" → "적었습니다" plus the screenshot note).
- **F-16** (slide 16 "centred on wineserver"; B4 CONTRADICTED). vol 06:539: B4's fix — slide 12 counts wine among the system tasks; the wineserver-centred graph is slide 11's; on slide 16 wineserver is a side loop with `Troy.exe` and `explorer.exe`.
- **F-20** ("many-core machine"). vol 08:259: after the archive quote, the slides name no trace machine (slide 5 names the 8-core Steam Deck as LAVD's target), so "many-core" is the archive's reading. Same quote at vol 03:1729: the same gloss.
- **F-30** (136M's 0.7 %). vol 08:954: the 0.7 % is the six-participant sample the 9.5 search read.
- **F-48** (Proton "runs only under the Steam client"). vol 02:712 and vol 06:1318 (quotes of `game-task-chain`'s `validation_stats.reason`) → "Proton is documented only as a tool for use with the Steam client"; vol 06:1380 likewise in Korean. **For the lead:** the quotes now carry the finding's fixed wording; `dataset/archetypes.yaml`'s reason is unchanged in the working tree as of this chunk — check the data chunk lands the same words.
- **F-49** (the 100–664 MHz Linux machines). vol 06:1400: Linux observations on 300–664 MHz machines of 2000–2006 (Flautner, Tsafrir/Etsion); the 100 MHz ones (Endo) on Windows NT and BSD/OS. The 9.5 D4 quote "100–664 MHz machines" at vol 02:766, vol 06:409, vol 08:952 left (the decision's words).
- **F-54** (`sched_waking`; B3 WORDING-FIX at :1027 only). vol 08:1027: fires only for a thread in a sleep state, in the waker, before it checks the thread has left its CPU, so on a short wait it can precede the switch-out. vol 08:1722 already says "can precede" on a short wait: unchanged.
- **F-55 / D-F5-06** ("no ceiling" grounded on Kalibera and Georges; B3 WORDING-FIX at vol 06:882 only). vol 06:882: "상한 없음(9.5 D33, …)"; Georges cited as §4.3 for adding runs to a set precision.
- **F-57**: UNVERIFIABLE in part (B3); the earlier record stands. No change.
- **Other — `linux-sched-bwc`** (stale "not added"). vol 08:698: the entry is in `docs/references.md`'s deployed-system section (existence claim only, verified 2026-09-10). vol 08:1864's open item (12.7) removed. vol 08:693 (a quote of the Phase 7 archive) left.

## Dataset-side trace and blind findings whose wording the guidebook repeats

- **D-F1-12** (the deck's 1.5 ms slice example; B1 NOT IN SOURCE). vol 02:730: "the deck's 1.5 ms slice example" → `scx_lavd`'s source-comment example, 15 ms shared by 10 tasks.
- **D-F1-19** (`perf sched record` attributed to the 2024 deck; B1 NOT IN SOURCE). vol 02:689: the tool removed from the deck's description, "the talk does not name its tool". vol 02:718 (9.4 D1's own words quoted): a sentence after the quote — the tool's name comes from `edge-lwn26`'s report of Min's LPC 2025 session (VaporMark), and tying it to this deck is 9.4 D1's reading.
- **D-F4-45** (Chromium occlusion on Linux; B3 CONTRADICTED), stated as the brief's limitation. vol 02:752 (the visible Steam window, 9.8 D5): Chromium on Linux computes no occlusion of its own and on X11 marks a window occluded when the X server reports it fully obscured; whether the depicted desktop delivers that report the measurement did not test. vol 02:1239 (`renderer-visible`, 9.8 D4): the "Windows-only" reason restated as 9.8 D4's, with the same X11 sentence.
- Checked, nothing to change: D-F1-46 (the guidebook's flap-interval table at vol 05:395–398 already gives GameMode's check interval, tuned's update interval with dynamic tuning off, systemd-oomd's duration), D-F1-27 and D-F2-12 (no occurrence).

## Handed-over checks (`handed/findings.md`) and 인지오's answers

- **F1 / D1** (`c7-meeting`'s "about a fifth"). vol 04:241: about one cycle in twenty, demoted in about 4 of 10 boost intervals, with 9.16 D1 named. vol 04:1720: the 9.14 decision 2 quote kept as "was"; the reason restated per D1 (one in twenty, 4.9 % table / 5.5 % compiled; 1 − 0.95¹⁰ arithmetic, cycles independent, ten per 100 ms boost). vol 08:1281: a sentence that "about a fifth" was the quantile table read as deciles and D1 restated it. vol 08:1299 ("12.2 ms ninth-decile"): 12.2 ms is the 99th percentile, the ninth decile 7.4 ms, relabelled in the RQ0 gate spec by D1.
- **F2** (the `systemd-oomd` branch read): `docs/references.md` only; the guidebook's oomd passage (vol 05:398) names no branch. No change.
- **F3** (`game-task-chain`'s `normal` not from the census). vol 02:1333 (10.1, the class census): `game-task-chain` is no measurement; its `normal` is the 9.13 spec's default and design, `lavd-ossna24` recording no class.
- **D2** (research guidebook vol-01's row): not this chunk's file; recorded in vol 08 12.2.

## Compiled-number audit (`compiled/findings.md`), the parts the guidebook repeats

- **F1 / D4** (`c2-p3b`'s backup). vol 04:952 (P3's two jobs finish and score turnaround), :954 (the b-file's term is turnaround 0.25), :1154 (the scoring paragraph: turnaround, the current scoring-spec comment quoted, the replay facts, the header rule; the old "162 s" comment named as from the manifest's even spread), :1156 (the backup finishes about 0.3 s before the end). **For the lead:** the `c2-p3a.timeline.yaml` head comment and `c2-p3b`'s recipe comment still say "the variant's backup does not end inside it and is scored by progress (9.14)"; the guidebook no longer quotes them.
- **F4, F5** (the call's demotion edge, decile labels): as D1 above.
- **F6** (chain ×1.4 lanes). vol 04:1919: "(1.14 and 1.26 lanes)" → "(1.33 and 1.26 lanes)", as `rq0-gate.yaml:177` now reads.
- **G1 / D3** (the `tick_count` guard): no current-state statement of the chain check in the guidebook; vol 06:572 and vol 08:773 are 2026-09-13 history. Recorded in vol 08 12.2.
- F3, F7–F16: no occurrence in the guidebook (grepped: "162 s", "1.14", "decile", "sixteen tasks", "26 of the", "textbook", the keystroke counts).

## Measurement audit (`meas/class-findings.md`, `meas-new/proposed-text.md`)

- **class F3** (`input_run` floored at zero). vol 02:316 already says "음수는 0으로 자릅니다". vol 06:807: the same sentence added, citing 9.5 D13.
- **class F4** (component = comm across the tree's processes for `chat-client` and `game-client`). vol 02:623 and vol 06:802: the exception added.
- **class F5** (stated as a fidelity gap). vol 02:1499 (compile-fidelity limits): the 12 hidden renderers wake together across processes (9.8 D15, 243 / 32 / 0), the 4 bound renderer tasks compile independently, not re-read on the current pool. vol 06:1039 and the limits list vol 06:1693: the same in short form.
- class F1, F2, F6: code and data only; the guidebook carries none of the affected sentences.
- **G1**. vol 02:1501: as proposed.
- **G2**. vol 06:1039: both replacements as proposed.
- **G3**. vol 06:1554: as proposed, with the script path `_dev/research/jioh/task-9.16-exit-audits/meas-new/stability_ledger.py`, which `measurement-overview.md:97` uses in the working tree (the script has not moved to `dataset/tools/meas/`). If C3 moves it, change both.
- The 9.16 hand-off lists (vol 06:1672–1673, vol 08's 12.2 bullet "9.15에서: …"): left for the exit record, as the proposed-text note says.

## Vol 08 — 9.16's own decisions

- 12.2 heading "(아직 시작 전)" → "(2026-10-17 시작, 진행 중)"; the "no task spec yet" sentence replaced by the spec's path and its method in four sentences (decisions 1, 2, 4, 5 of the 9.16 spec); the open-item box's "method not decided, no spec session" sentence removed.
- After the box: "9.16의 결정(2026-10-17)" and one entry per D1–D6 in the chronicle's "**N.M Dk(… 결정).**" form — what was found and what was decided, each with its numbers from `decisions.md`.
- 13장, the 2026-10-17 row: the 9.16 grill and spec and D1–D6 in a parenthesis; the records column adds the spec and `decisions.md`.
