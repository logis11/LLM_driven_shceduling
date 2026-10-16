# Work-list rows — `docs/workload/grounding-sources.md`

Chunk K06, Measurement and grounding docs (wave 2). 15 open rows. The file has 85 lines at `d5cc7711`.

### W-0283 · open · full pass
- At: `docs/workload/grounding-sources.md` the whole file
- Change: Full pass against the code: check every statement about the dataset in the file against `dataset/` (the timelines, `archetypes.yaml`, the manifests, `coverage-grid.json`, the tools) and correct what is stale; each correction not already a row is logged as a new row in the chunk log.
- Final word: 9.15 spec decision 4: the docs that explain the dataset — `docs/workload/`, `dataset/README.md`, `docs/data-contracts.md`, the harness guide's records and dataset chapters — get a full pass against the code; staleness an agent notices outside its rows becomes a new row. Precedence by decision 3: the code and data as they stand (`dataset/`, `harness/`, `simulator/`, the committed manifests) first.
- Sources: 9.15 spec decision 4 (`jioh/task-9.15-docs-memos-and-guidebook-corrections.md:30`)
- Notes: —

### W-0284 · open
- At: `docs/workload/grounding-sources.md` Role A table, SYSmark 30 / 25 (BAPCo) row, line 15
- Change: Restate the row to the recorded verdict: the Productivity/Creativity/Responsiveness taxonomy is SYSmark 25's (and SYSmark 2018's), not SYSmark 30's, and its ML item is "facial detection" / "ML based image recognition", not "ML face recognition"; SYSmark 25's inclusion of software development stays as the compile family's scenario precedent, "mainstream" being our inference.
- Final word: 9.12 D103 (scope-card item 63, 9.6's hand-off, passed through from its recorded verdicts): `grounding-sources.md:15` applied from the 2026-09-13 verification — K5 (a comparison report of that verification) C-sysmark25-2, MISATTRIBUTED: the taxonomy belongs to SYSmark 25 (and 2018), not SYSmark 30, and the source says "facial detection"; the software-development inclusion SUPPORTED, "mainstream" the project's inference (K5:230, :238).
- Sources: S12-222 (9.12 D103, `task-9.12-related-work-prose/changelog.md:1559`)
- Cross-ref: W-0293
- Resolved at merge: Item 63 names "K1, K3 verdicts" for its lines; the verdicts recorded on :15 itself are K5's (_dev/research/jioh/2026-09-13-verification/compare/K5.md:36, :230, :238). 9.6's scope card (task-9.6-compile/scope-card.md:36) lists :15 beside :32 without a verdict of its own.
- Notes: W-0293 also names :15; it is merged into the :32 row (W-0293).

### W-0285 · open
- At: `docs/workload/grounding-sources.md` Role A table, UL Procyon row, line 16
- Change: Keep the Procyon row as a scenario-existence precedent only (local-AI inference scenarios exist in a shipped commercial benchmark, its page listing ten benchmarks) and drop its offer for the ML family: the training scenario is grounded on PyTorch's basic MNIST example (9.10 D12), and no dataset scenario rests on Procyon.
- Final word: 9.10 D34 (procyon leaves the registry; no catalog row or job cites it after D12 and D33) as superseded for the references entry by 9.12 D102: `procyon` stays, cited by the research guidebook's vol-02 ch. 8.4 and corrected to its verdicts (9.12 D53: the page lists ten benchmarks, not nine); the workload docs citing it include `grounding-sources.md:16`.
- Sources: S10-081 (9.10 D34, `task-9.10-scenarios-timelines/changelog.md:741`)
- Resolved at merge: The raw row offers restate or drop. 9.12 D102 (2026-10-09, later than 9.10 D34) keeps the entry and lists this line among its citations, so the row stays and its justification is restated to what remains true (read: _dev/research/jioh/task-9.12-related-work-prose/changelog.md:1544).
- Notes: dataset/sources.yaml:137 still holds `procyon` (9.10 D34 said it leaves the registry); that is a registry matter outside this doc. The Role A table's other instances (ananicy, Game Mode) are W-0286's.

### W-0286 · open
- At: `docs/workload/grounding-sources.md` Role A table, "Windows Game Mode docs / ananicy catalog" row, line 18
- Change: Restate the row to what the instances ground: the gaming category (Windows Game Mode, Apple's macOS Game Mode, Feral GameMode), background work held back during play by vendor rule (Windows Update's driver installs and restart notifications in Game Mode, dated by the Xbox Wire post of 2018-10-02; Steam's downloads pausing at game launch), and a per-name priority catalogue (`ananicy-rules`) — not a wanted/unwanted-background distinction drawn by any of them.
- Final word: 9.12 D45 as amended by D74: Microsoft's Xbox Support article "Use Game Mode while gaming on your Windows device" (rendered 2026-10-09, undated; earliest dated copy the Internet Archive capture of 2018-12-30) states that while a game runs Game Mode prevents Windows Update from performing driver installations and sending restart notifications; Microsoft's dated statement is Xbox Wire, 2018-10-02; how a game is recognised stays undocumented. `grounding-sources.md:18` grounds the gaming category (Windows, macOS, Feral), background work held back during play by vendor rule (Windows Update in Game Mode; Steam's downloads, 9.12 D16) and a per-name priority catalogue (`ananicy-rules`, 9.12 D3) — not a wanted/unwanted judgement by any of them (K3 C-gamemode-1 and C-ananicy-rules-4: NOT IN SOURCE).
- Sources: S12-208 (9.12 D45, `task-9.12-related-work-prose/changelog.md:721`); SX-0159 (TODO 9.15 line (from 9.12 D45), `_dev/TODO.md:179`)
- Notes: File unchanged since 2026-08-27; the hand-off line holds. The references entries the text cites (the Xbox Wire post, Apple's Game Mode page, Feral GameMode) are minted by the references chunk (9.12's hand-offs).

### W-0287 · open
- At: `docs/workload/grounding-sources.md` Role B table, interbench (Kolivas) row, line 27
- Change: Restate the "what it justifies" column: interbench is the precedent for the foreground-interactive + background-bulk structure of Family 2 (the desktop-with-background family) only and supplies no parameter values — its Audio/Video/X emulations are no longer cited by the dataset, and its gaming load uses as much CPU as it can get, with no deadlines.
- Final word: 9.12 D47 (amended by D76, D103) passes scope-card items 62 and 66 (the 9.5 and 9.7 hand-offs) through from their recorded verdicts: K1 (a comparison report of the 2026-09-13 claim verification) C-interbench-4, WORDING-FIX on :27 — "parameter values for audio/video interactivity; a CPU-bound gaming load that uses as much CPU as it can get, with no deadlines"; the load list (Burn, Write, compile-like) and "measuring latency, jitter, missed deadlines" SUPPORTED. 9.5 D11: interbench's Audio/Video/X emulations are no longer cited by the dataset (the `interbench` entry, docs/references.md:189).
- Sources: S12-216 (9.12 D47, `task-9.12-related-work-prose/changelog.md:748`); S12-328 (9.12 scope card (boundary), `task-9.12-related-work-prose/scope-card.md:19`)
- Cross-ref: W-0288; W-0289
- Resolved at merge: K1's wording fix (2026-09-13) keeps "parameter values for audio/video interactivity"; 9.5 D11, later, retired the emulations' values from the dataset (measured per-application entries replace them), so the line claims no parameter values.
- Notes: S12-216 also covers item 68's :28–29 (memo B7: no chat/IPC archetype exists), carried by W-0288 and W-0289, and item 69's "`grounding-sources.md` where it names the class" (9.9): no line of the doc names a daemon class (grep for daemon/class: only :18's "per-app priority classes"), so nothing is owed there. S12-328 is the 9.12 scope card's boundary (every docs/ edit is 9.15's; items 61–70 applied from their recorded verdicts).

### W-0288 · open
- At: `docs/workload/grounding-sources.md` Role B table, schbench (Mason, 2016) row, line 28
- Change: Keep schbench as the precedent for tail-focused latency metrics (at v1.0 it prints wakeup and request latency at p50/p90/p99/p99.9 and RPS at p20/p50/p90) and drop "also the messaging/wakeup-heavy process archetype": it grounds no archetype.
- Final word: 9.11 D12 (the precedent registry entries corrected), extended by 9.11 D33 to the precedent lines D12 did not name: `schbench` is a scheduler benchmark reporting tail percentiles, cited for the citation precedent and tail-focused metrics; none of the precedent entries grounds a dataset value. Item 68 of 9.12's scope card (9.8): `schbench`/`hackbench` as grounding for a "chat/IPC-heavy archetype" that does not exist (critical-findings memo B7).
- Sources: SX-0073 (TODO 9.15 line (from 9.11 D12), `_dev/TODO.md:179`); SX-0510 (9.11 D33, `task-9.11-scheduler-constants/changelog.md:452`); SX-0519 (9.11 scope card, Out of 9.11, `task-9.11-scheduler-constants/scope-card.md:25`)
- Cross-ref: W-0287; W-0292
- Resolved at merge: 9.11 D33 names :28 without stating the fault. Read against 9.11 D12 (changelog.md:161–176: none of the entries grounds a dataset value) and 9.8's hand-off (task-9.8-browser-comms/scope-card.md:36: the archetype does not exist), the fault is the archetype clause. K1:473 found the first two columns SUPPORTED (2016 copyright), so "(Mason, 2016)" and "(P99)" stay.
- Notes: SX-0510 also covers the stress-ng row (:31), applied by W-0292; SX-0519 is the 9.11 scope card's routing umbrella for :28–31. The `schbench` entry: docs/references.md:197–200.

### W-0289 · open
- At: `docs/workload/grounding-sources.md` Role B table, hackbench row, line 29
- Change: Restate hackbench as "a benchmark and a stress test for the Linux kernel scheduler" (many communicating tasks; LWN notes it is most often used for load-balancing changes), existence only, cited for the contrast with schbench, and drop "The chat/IPC-heavy archetype's burst structure": it grounds no archetype.
- Final word: 9.11 D12: `hackbench` is existence only — in its man page's words "both a benchmark and a stress test for the Linux kernel scheduler" — cited for the contrast with `schbench`, grounding no archetype (no IPC archetype exists, critical-findings memo B7); K1 C-hackbench-1 WORDING-FIX on "load-balancing stressor": load balancing is LWN 725238's note on who most often uses it.
- Sources: SX-0071 (TODO 9.15 line (from 9.11 D12), `_dev/TODO.md:179`); SX-0508 (9.11 D12, `task-9.11-scheduler-constants/changelog.md:174`)
- Cross-ref: W-0287
- Notes: grounding-sources.md is normative (header line 2): edit in place. The `hackbench` entry: docs/references.md:202–205.

### W-0290 · open
- At: `docs/workload/grounding-sources.md` Role B table, "LAVD design notes (LKML, LPC talks)" row, line 30 (source column and the production clause); Citation-tier rule, scholarly list, line 74 ("LAVD/LWN-covered work")
- Change: Restate :30's source column to the OSS NA 2024 slides (`lavd-ossna24`), scx_lavd's source and README at `v1.1.3` (`scx`) and LWN's reports of the LPC 2024 and 2025 talks (`corbet-lwn24`; Jake Edge's LWN 1051430), and its production clause "Valve ships it; Meta adopted the scheduler server-side" to: Valve sponsors LAVD and ships it in SteamOS 3.8 as a scheduler the user selects, not enabled by default, and Meta presented it as a candidate default fleet scheduler; remove "LAVD/LWN-covered work" from :74's scholarly list.
- Final word: 9.12 D11 as amended by D100 and D113: LAVD has no scholarly citation; every LAVD source is footnote tier — `lavd-ossna24`, scx_lavd at `v1.1.3`, `corbet-lwn24` (LWN 991205, an attributed report, qualitative only), LWN 1051430 (Jake Edge, 2026-01-07), the SteamOS sources (D9), the LPC slides and abstracts (D8); `lavd-ossna24` and `corbet-lwn24` are of the talk, conference-abstract or news-report type (D113). The production clause per 9.12 D9 and D8. 9.11 D12 marked "Meta adopted the scheduler server-side" MISATTRIBUTED (C-lavd-18b): `scx` supports "Meta is in the process of mass production deployment" of sched_ext (README.md:33–35 at v1.1.3), not of LAVD.
- Sources: S12-067 (9.12 D11, `task-9.12-related-work-prose/changelog.md:199`); SX-0072 (TODO 9.15 line (from 9.11 D12), `_dev/TODO.md:179`); SX-0160 (TODO 9.15 line (from 9.12 D11), `_dev/TODO.md:179`); SX-0509 (9.11 D12, `task-9.11-scheduler-constants/changelog.md:174`)
- Cross-ref: W-0291; W-0297
- Notes: The "16ms-frame deadline" in the same cell is W-0291's. :74's "CNNIC study" is W-0297's. LWN 1051430 is not yet its own entry at HEAD (docs/references.md:225 mentions it inside `corbet-lwn24`); 9.12 D11 mints it in the references chunk.

### W-0291 · open
- At: `docs/workload/grounding-sources.md` Role B table, LAVD row line 30 ("the 16ms-frame deadline"); Standing verification tasks item 4, line 84 ("SWELL-KW — cited qualitatively (`swell-icmi14`, REFERENCES-only; not in the registry)")
- Change: Drop "the 16ms-frame deadline" from the LAVD row's justification (the game chain's 16,667 µs frame period is a design value on `steamos-refresh`, the Steam Deck's 60 Hz refresh); restate item 4: `swell-icmi14` is in the registry and its keystroke streams are the typing entries' replayed stimulus (open under CC BY-NC-SA 4.0), not a qualitative, references-only citation.
- Final word: K2 (a comparison report of the 2026-09-13 claim verification) C-lavd-9, NOT IN SOURCE: no slide states a frame budget, deadline or period; 9.4 D2: the deck states no frame period, and 16.7 ms is a design frame period on `steamos-refresh`. K4 C-swell-1, CONTRADICTED: the DANS record is open access under CC BY-NC-SA 4.0; 9.5 D4/D18: the typing entries replay SWELL-KW keystroke streams (dataset/stimulus/).
- Sources: SX-1045 (guidebook dataset vol-06 ch.14 mismatch table row 13, `dataset/06-grounding-measurement-verification.md:1713`)
- Cross-ref: W-0290; W-0287; W-0297
- Notes: Code: dataset/archetypes.yaml `game-task-chain` `frame_period: {value_us: 16667, source: "steamos-refresh"}`; dataset/sources.yaml:29 `swell-icmi14`; dataset/stimulus/streams.json (`licence: CC-BY-NC-SA-4.0`). SX-1045 (the dataset guidebook's vol-06 mismatch row) also names Role B's precedent-only reading (W-0287–W-0289, W-0292), the Meta claim (W-0290) and `zhang-chb15` (W-0297); this row carries what no per-decision row does. The guidebook note at vol-06 :289 waits on this file's correction.

### W-0292 · open
- At: `docs/workload/grounding-sources.md` Role B table, stress-ng row, line 31 ("Fallback archetypes only (pure CPU hog, I/O hog); prefer the above where possible")
- Change: Restate the stress-ng row as existence only, grounding no archetype: a stress tool whose `--workload` stressor emulates bursty scheduled compute and whose `--cyclic` stressor reports wake-latency percentiles, its README disclaiming precise benchmarking.
- Final word: 9.11 D12 (extended by D33 to :31): `stress-ng`'s role "fallback archetypes only" → existence only; `--workload` "emulates bursty scheduled compute" (`stress-ng.1:11793–11809`), `--cyclic` reports wake-latency percentiles (`:2744–2752`), its README disclaims precise benchmarking; pinned at commit `3ac9d7a8`, GPL-2.0-or-later; it grounds no archetype.
- Sources: SX-0074 (TODO 9.15 line (from 9.11 D12), `_dev/TODO.md:179`)
- Cross-ref: W-0288
- Notes: K1:500 found the old row SUPPORTED against its source; the change is 9.11 D12's role decision. The `stress-ng` entry: docs/references.md:207–210.

### W-0293 · open
- At: `docs/workload/grounding-sources.md` Role B table, kernel build (make -jN) row, line 32
- Change: Restate the row: a compile workload SchedCP's evaluation uses (kernel compilation, "make -j 172" on 6.14 tinyconfig, 1.79× over EEVDF); the compile family's short-lived structure keeps `ocallahan-atc17` ("make forks and execs 2430 processes, mostly short-lived", a DynamoRio build) and is otherwise grounded in the dataset's measured build (a warm `-j8` linux-6.6 build, 5 957 forks under 719 make processes, 2 857 six-member object jobs; `cc1_step_1` p50 367.6 ms); SchedCP's "short-lived processes" is attributed as its Observation Agent's generated profile text; "in every scheduler evaluation" leaves.
- Final word: 9.12 D47 as amended by D76 (SchedCP's evaluation, singular; `ocallahan-atc17` kept; `cc1_step_1`) and D103: as the change states. K1 C-kernelbuild-2: "every scheduler evaluation" NOT IN SOURCE, "including SchedCP's" SUPPORTED; the fork-heavy short-lived structure SUPPORTED only as "many short-lived processes".
- Sources: S12-215 (9.12 D47, `task-9.12-related-work-prose/changelog.md:748`); S12-220 (9.12 D76, `task-9.12-related-work-prose/changelog.md:1179`); SX-0161 (TODO 9.15 line (from 9.12 D47), `_dev/TODO.md:179`); SX-0165 (TODO 9.15 line (from 9.12 audit, grounding-sources), `_dev/TODO.md:179`)
- Cross-ref: W-0284
- Notes: S12-220 (D76) restates D47's wording; the merged change carries D76's. SX-0165 also names :15 (item 63), applied by W-0284. "also our canonicalization example (hundreds of cc1 children folding into one canonical app)" is not addressed by the decisions; K1:531 marks "hundreds of cc1 children" as ours.

### W-0294 · open
- At: `docs/workload/grounding-sources.md` Role C table, lines 38–42 (the task-switching log studies row :40, SWELL-KW :41, DesktopBench :42)
- Change: Rewrite the Role C table to what each source supports: drop the 15M-log study (`zhang-chb15`); state the Mark line's figures in their sources' units (`gonzalez-chi04`: about 3 min per event, 11 min 28 s per central and peripheral working-sphere segment; `mark-chi05` with its wording fixes); restate Czerwinski et al. as a one-week self-report diary of user-defined tasks reporting means and SDs, not app-switching distributions; SWELL-KW as a lab dataset of 25 students and interns (Windows 7, 2012, open under CC BY-NC-SA 4.0) and a candidate observation for the naturalistic generator; add BEHACOM as a candidate; DesktopBench as the precedent for an evaluation shape only (its interruption a separately labelled task switch, not a within-segment distractor; its sessions composed from templates, not observed; a fixed 6.0 s per action).
- Final word: 9.10 D35 (2026-10-01), unamended: Role C restated — segment durations from `gonzalez-chi04` as they are (C-gonzalez-1, -3) and `mark-chi05` with C-mark05-2, -3; hub-and-spoke switching unsourced (its only source `zhang-chb15` dropped, 9.10 D1); DesktopBench (`focal-arxiv26`) cited only as the precedent for an evaluation shape (C-focal-1, C-focal-4); the generator's candidate observations SWELL-KW (dwell median 9.1 s, A → B → A returns after 83.4 % of episodes; 25 students and interns, C-swell-1) and BEHACOM (foreground program and switches per minute, 12 users, 4 on Linux). 9.10 D31 with D35 for DesktopBench. 9.10 D169 with 9.12 D102: C-czerwinski-1 — "a one-week self-report diary of user-defined tasks (10 people analysed), reporting means and SDs. It is not a log study of app-switching distributions".
- Sources: S10-093 (9.10 D35, `task-9.10-scenarios-timelines/changelog.md:755`); S10-072 (9.10 D31, `task-9.10-scenarios-timelines/changelog.md:663`); SX-0054 (TODO 9.15 line (from 9.10 D169), `_dev/TODO.md:179`); S10-155 (9.10 scope card, `task-9.10-scenarios-timelines/scope-card.md:36`)
- Cross-ref: W-0291; W-0296; W-0297
- Notes: BEHACOM has no docs/references.md entry at HEAD; 9.10 D35 hands minting one "where the docs cite it" (a verified passage needed, 9.15 spec decision 3) — the references chunk's. K4 also marks :40's "the claim that app-granularity sets are stable while PID-granularity churns" NOT IN SOURCE (C-zhang-5) and "Empirical distributions" a WORDING-FIX (C-zhang-4). S10-155 is the 9.10 scope card's coverage umbrella (Role A :16, Role C, the negative result, :81), carried by W-0285, W-0296 and W-0297. The Q7 within-segment distractor wording also lives in building-plan §3 C4 (another row).

### W-0295 · open
- At: `docs/workload/grounding-sources.md` Role D, superseded note, line 48 ("with the collection + privacy-scrub tool released as an open falsification invitation")
- Change: Remove the claim that a collection + privacy-scrub tool is released; the repository holds no such tool, and live-usage validation stays a stated limitation.
- Final word: The critical-findings memo's B7 (docs/memos/2026-09-13-critical-findings.md:162): the privacy-scrub tool that the building plan says "ships in the artifact" is not in the repository; 9.5's scope card hands the "released sampler + privacy-scrub tool" sentence to 9.15 (task-9.5-interactive-typing/scope-card.md:26). No record resolves it otherwise.
- Sources: SX-1050 (guidebook dataset vol-06 ch.14 mismatch table row 17, `dataset/06-grounding-measurement-verification.md:1717`)
- Resolved at merge: Code first (9.15 spec decision 3): no privacy-scrub or collection tool exists under dataset/tools/ or elsewhere in the tree (grep "privacy-scrub"), so the doc describes the code and the claim leaves.
- Notes: The same claim stands in building-plan.md:189 (another row) and the old research guidebook vol-06 :1465, :3431.

### W-0296 · open
- At: `docs/workload/grounding-sources.md` The negative result — why the suite is synthetic, lines 50–60 ("no public trace of desktop process timelines with process names exists")
- Change: Narrow the claim: no public trace gives desktop process trees with names over time; name the nearest data that exists — BEHACOM (foreground executable names per minute from natural use on Linux and Windows) and DARPA OpTC (process-create events with image paths on Windows 10 enterprise endpoints) — and note under the mobile datasets' exclusion (foreground exclusivity) Carat's several running apps per sample.
- Final word: 9.10 D35, unamended: the negative result narrowed — no public trace gives desktop process trees with names over time; BEHACOM publishes foreground executable names per minute from natural use on Linux and Windows (S3-02); DARPA OpTC publishes process-create events with image paths on Windows 10 enterprise endpoints (C-plain-7); mobile datasets stay excluded for foreground exclusivity, Carat's several running apps per sample noted (C-plain-8).
- Sources: S10-094 (9.10 D35, `task-9.10-scenarios-timelines/changelog.md:755`)
- Cross-ref: W-0294
- Notes: BEHACOM, DARPA OpTC and Carat have no docs/references.md entries at HEAD; cite them only with entries minted on a verified passage (9.15 spec decision 3), else mark unverified. The anti-roles bullet on mobile datasets (line 65) states the same exclusion.

### W-0297 · open
- At: `docs/workload/grounding-sources.md` Citation-tier rule, scholarly list, line 74 ("CNNIC study"); Standing verification tasks item 1, line 81 ("resolved: `zhang-chb15` (authors corrected …; see docs/references.md)")
- Change: Restate item 1: the task-switching study was dropped on 2026-10-01 for want of a reachable copy and has no docs/references.md entry; remove "CNNIC study" from :74's scholarly list.
- Final word: 9.10 D1 (2026-10-01), unamended: a reference with no reachable copy is dropped; `zhang-chb15` (Zhang, Sun, Chai and Aghajan, Computers in Human Behavior 49, 2015) has none, so its dataset/sources.yaml and docs/references.md entries leave (both gone at HEAD) and the prose that cites it is rewritten without it. 9.12 D102: none of 9.12's owned prose cites it.
- Sources: S10-003 (9.10 D1, `task-9.10-scenarios-timelines/changelog.md:13`); SX-0046 (TODO 9.15 line (from 9.10 D1), `_dev/TODO.md:179`)
- Cross-ref: W-0290; W-0294
- Notes: The hand-off names :81; :74's "CNNIC study" is the same study by name. :40's "15M-log / ~3k-user" study is W-0294's. Verified: no `zhang-chb15` in docs/references.md or dataset/sources.yaml at HEAD.

### W-0839 · open
- At: `docs/workload/grounding-sources.md` line 77, the scope-discipline paragraph ('a deployed-system citation may support only *existence claims* ("this scenario/setting/category exists in shipped software") — never empirical, behavioral, or statistical claims'); the Role C table, line 40
- Change: Restate line 77's rule to the citation-tier rule as `docs/references.md` now states it (9.12 D112's three clauses for deployed-system; the talk, conference abstract or news report type at the footnote tier, 9.12 D113). In Role C, the entries K01 left for its sources: `behacom-dib20` (new — BEHACOM, the Data in Brief article and its Mendeley deposit, one entry) and `czerwinski-chi04` (kept, its role corrected to C-czerwinski-1: a one-week self-report diary of user-defined tasks, 10 people analysed, means and SDs).
- Final word: 9.12 D112 and D113, applied in K01 to the citation-tier and id-minting rules (W-0002, W-0001). K01's decisions 2 (`czerwinski-chi04` kept: `grounding-sources.md:40` cites it and W-0294's rewrite keeps it) and 4 (BEHACOM as one entry, W-0014).
- Sources: W-0002; W-0014; `logs/K01.md` ## Decisions, 2 and 4
- Cross-ref: W-0294; W-0296; W-0836; W-0848
- Notes: found in K01. W-0294 rewrites the Role C table (Czerwinski et al. restated); W-0296 names BEHACOM in the negative-result paragraph and can cite `behacom-dib20`. The dataset guidebook vol-02 quotes line 77 (W-0848).

## Also on this file, not for editing from this list

- W-0734 · waits on 인지오 — Is the collection and privacy-scrub tool still promised? What the records and code say: grill 2026-08-26 D8 (`_dev/archive/2026-08-26-workload-generation-grill.md:29`) promised it ships 'as an open falsification invitat… Blocks: `docs/workload/building-plan.md:209`, `docs/workload/grounding-sources.md:48` (W-0295), the dataset guidebook vol-02 §12.2 note and vol-06's mismatch row, the…
