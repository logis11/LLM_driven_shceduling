# 9.16 docs chunk W — `docs/workload/*.md`, `docs/references.md`, `dataset/README.md`

Files changed: `docs/references.md`, `docs/workload/measurement-overview.md`, `building-plan.md`, `coreset-guide.md`, `scenario-catalog.md`, `grounding-sources.md`, `archetype-plan.md`, `source-vetting.md`, `dataset/README.md`. Every changed `docs/` header already read `Updated 2026-10-17`. No doc added, renamed or re-statused, so `docs/README.md` is untouched. Not committed. Line numbers are the files as they stand after this chunk.

## Trace audit — dataset side (`claims/dataset-findings.md`), with the blind re-reads (`reads/B1`–`B3-compare.md`)

- **D-F1-12** (the deck's 1.5 ms slice example) — `dataset/archetypes.yaml` only; not mine.
- **D-F1-14** (six chain members named `Troy.exe` under the slide-16 tag) — `coreset-guide.md:252`, `scenario-catalog.md:20` and `:36`, `archetype-plan.md:102`: slide 16 shows one `Troy.exe` node; six members carry the process name by our `comm` rule (a Wine thread that sets no name keeps its process's; 9.10 D26). The timelines' `member_names` and the `modeling_notes` are the data chunk's.
- **D-F1-19** (the deck's traces "collected with perf sched record", NOT IN SOURCE per B1) — `coreset-guide.md:242`: the tool dropped from the deck's description; `perf sched record` named as what Min's later VaporMark analyses (`edge-lwn26`). `archetypes.yaml:1756` is the data chunk's.
- **D-F1-22** (Proton "runs only under the Steam client") — the same wording in `archetype-plan.md:34`, restated "documented only as a tool for use with the Steam client". The `validation_stats.reason` is the data chunk's.
- **D-F1-27** (the per-game download setting) — `references.md:295`: the per-game setting moved to FAQ 71AB-698D-57EB-178C with its sentence; status `:296` points to `B1-compare.md`.
- **D-F1-30** (SteamOS 3.8, "not enabled by default") — UNVERIFIABLE in B1; skipped, the earlier record stands.
- **D-F1-31** ("Valve sponsors LAVD"; also outside A-09's wording) — `references.md:310` and `grounding-sources.md:30`: Valve holds the copyright of scx_lavd's code, which its author develops as part of his work at Igalia on SteamOS (the `lat_cri.bpf.c` line, Edge's sentence); status `:311`.
- **D-F1-43** (tuned's quotations not in the 9.19 record) — `references.md:588`: status points to `handed/checks.md` (9.19 decision 5 item, `tuned-main.conf` v2.28.0 lines 9–18) and `reads/B1-reads.md` §8, both holding the three quoted lines.
- **D-F1-45** and handed **F2** (`systemd-oomd` read on `main`) — `references.md:591`: cite moved to release v262.1 (commit `73612ea5…`, published 2026-10-16), accessed 2026-10-17, the same text at v255 (`db11bab3…`), Ubuntu 24.04's major version; `:593` status gives the line numbers at both tags and points to `handed/checks.md`.
- **D-F1-46** ("debounce" values) — `building-plan.md:185`, `coreset-guide.md:588`, `dataset/README.md:150`: GameMode's 5 s reaper check interval, tuned's 10 s dynamic-tuning update interval (off by default), systemd-oomd's 30 s pressure sustain duration. `grids.yaml` is the data chunk's.
- **D-F1-49** (the `sched.h` comment passages "at v6.17", no 2026-10-12 read recorded) — `references.md:387`: status points to `handed/checks.md` (9.20 decision 10 item, v6.17 lines 315–316, 320, 1156–1161, 1165) and 9.10 S4-09.
- **D-F2-02** (SWELL-KW log content) — `references.md:69`: character keystrokes with application and window title, special keys without; pointer events with cursor position and distance since the previous event, no motion samples; `measurement-overview.md:48` "character keystrokes"; status `:70`.
- **D-F2-06** (dwell 9.1 s, returns 83.4 %) — `references.md:69`, `grounding-sources.md:43`, `building-plan.md:205`: the filtered focus sequence named, the unfiltered median 5.1 s (9.10 S3-01's `app_raw`).
- **D-F2-07** (136M licence quotation) — `references.md:38`: readme.txt:21 quoted exactly. `dataset/README.md:218` paraphrases without quotation marks; unchanged.
- **D-F2-09** (gap shares; "D6's") — `references.md:39`: "9.5 D4's alternative not taken", the 0.7 % kept as six participants', B1's 2,000-participant 2.1 % added.
- **D-F2-10** (3 min 08 s exclusions) — `references.md:44`, `grounding-sources.md:40`, `building-plan.md:203`, `source-vetting.md:139`: "formal meetings, unknown and personal events excluded". `sources.yaml` is the data chunk's.
- **D-F2-12** (population, statistics) — `grounding-sources.md:40` "means and SDs, with ANOVAs" ("information workers" already there). `sources.yaml` is the data chunk's.
- **D-F2-18** (Roeser "fluent spread"; also the "Other notes" pointer slip at `:59`) — `references.md:59`: "fluent-typing variance σ²e 0.29 (log scale)"; status `:60`.
- **D-F2-19** (CMU "raw" dataset; also the pointer slip at `:64`) — `references.md:64`: a table of 31 timing features per repetition, 51 typists × 400 repetitions of one password; status `:65`.
- **D-F2-27** (interbench's 7 ms) — `source-vetting.md:162` (correction item "Line 52"): the man page's unsourced statement, quoted, not an established perception threshold.
- **D-F2-29** (interbench loads at the pin) — `source-vetting.md:162`: the correction's Line 52 item extended — Write and Read cap at about 1 GB, Hack never runs, an undocumented Ring load, the man page and v0.31 describing the older behaviour (`2026-09-13-verification/reads/R01-interbench-rtapp-benchtools.md`, C-interbench-10).
- **D-F2-39** (Ananicy / ananicy-cpp fields) — `references.md:202`: the self-description, the required-field quote and `cmdlines` placed in upstream Ananicy's README; ananicy-cpp's README field list without `cmdlines`; status `:204`. `source-vetting.md:158` holds; unchanged.
- **D-F2-43** (audio servers' nice) — `source-vetting.md:158`: the audio servers are `LowLatency_RT`, nice −12 (−11 in 2022–2025), `Player-Audio` nice −4 for players. `grounding-sources.md:18` holds; unchanged.
- **D-F2-44** (the 7-of-50 count) — `building-plan.md:121`: dated to the 2026-10-09 build. `dataset/README.md:114` holds on the final build (B2); unchanged.
- **D-F3-02** (O'Callahan's "compiler children") — `references.md:84`, `building-plan.md:101`: a parallel `make` build forks and execs many processes, mostly short-lived; status `:85`. `sources.yaml`, `archetypes.yaml` are the data chunk's.
- **D-F3-04** (Coetzee's reach) — `references.md:89`: "the Linux kernel build spawns"; status `:90`.
- **D-F3-07** (CONTRADICTED in B2: documented defaults "follow `nproc`") — `measurement-overview.md:52`: `-j8` the `nproc` rule on an eight-thread desktop (9.6 D4); DKMS and NVIDIA's `dkms.conf` read `nproc`, GNU make defaults to one job.
- **D-F3-08** (`parallelism_cap` 8's label; decisions.md, taken without a question: 9.6 D4 says convention) — `building-plan.md:101`, `coreset-guide.md:234`, `:660`: "convention". The timelines' labels and `archetypes.yaml:1134` are the data chunk's.
- **D-F3-11**, **D-F3-31**, **D-F3-35**, **D-F4-47**, **D-F1-11** — `dataset/` only; not mine.
- **D-F3-29** ("production branch") — the phrase is in `archetypes.yaml` only; `references.md:501`, `building-plan.md:93`, `:162`, `coreset-guide.md:238` do not carry it. Skipped.
- **D-F4-01, -02, -04, -05, -06, -24** (CpsMark+, SYSmark 2018) — UNVERIFIABLE in B3; skipped, earlier records stand.
- **D-F4-15** (PCMark 10's video playback as a "group") — `scenario-catalog.md:24`, `:33`, `references.md:224`: the Battery Life Profile's Video scenario; status `:225`.
- **D-F4-21** (SYSmark 30's background encode and Outlook, cited to the guide) — `references.md:228`: the whitepaper v1.2 added to the cite (Wayback 2025-04-23, SHA-256 `4111c36e…`); `:229` role quotes its §2.2 for both facts; `building-plan.md:135`, `scenario-catalog.md:15`, `:33` point to the whitepaper. `c3-creation.timeline.yaml` is the data chunk's.
- **D-F4-22** (the SYSmark 30 copy read) — `references.md:228`, `:230`: cite and status give the 2025-08-21 capture of R05 (retrieved 2026-09-13) and B3's 2025-04-23 capture (2026-10-17), same SHA-256.
- **D-F4-26** (Procyon's AI count) — `grounding-sources.md:16`, `references.md:239`: four on-device AI inference benchmarks, Android's the fourth; status `:240`.
- **D-F4-31** ("five tabs per window") — `coreset-guide.md:197`: "탭 다섯과 창 하나".
- **D-F4-43** (Chromium's grace) — overview `:51` holds per B3; `archetypes.yaml:738` is the data chunk's.
- **D-F4-45** (CONTRADICTED in B3; brief's D-F4-45 restatement) — `measurement-overview.md:51`: the Steam-window sentence restated as a limitation the measurement did not test, with Chromium's Linux behaviour as the brief states it.
- **D-F4-46** (Matrix 30 s) — `measurement-overview.md:51`: "matrix-js-sdk's 30 s `/sync` long poll".
- **D-F4-49** (evening arc order) — `building-plan.md:136`: "the dataset holds transitions of these shapes, in these orders". The `c3-evening` header is the data chunk's.
- **D-F5-06** ("No ceiling") — `measurement-overview.md:76`: "No ceiling (9.5 D33)", Georges cited for §4.3 runs added to a precision.
- **D-F5-09** (.929) — `measurement-overview.md:77`: "in the normal case with a t rule (Starr's computations, reported p. 461)".
- **D-F5-11** (tolerances beside Feller) — `measurement-overview.md:108`: "the tolerances ours; the count's standard error `feller-ipta50`'s".
- **D-F5-14** (what RFC 8290 grounds) — `measurement-overview.md:199`: "why `fq_codel` was the queue tried (its adoption: 9.7 D25)".
- **F-RBS-1** (D-F5-01 to -05, -07, -08, -10, D-F4-33, D-F4-39; with D-F5-09 and D-F5-14's record) and the lead's instruction for the registry-only sources — status lines point to `reads/B3-reads.md` as the record, with each copy's identification and what was not re-read: `georges-oopsla07` `:115` (§B2), `kalibera-ismm13` `:120` (§B1), `maricq-osdi18` `:125` (§B3; §5, §7.2, §7.5 not re-read), `chow-aoms65` `:130` (§B4), `cochran-st77` `:135` (§B5; §6.4 p. 155 OCR only), `feller-ipta50` `:140` (§B6; p. 249 and §12.2 not re-read), `fqcodel-rfc18` `:145` (§B12), `gh-artifact-retention` `:382` (§B11), `systemd-ubuntu` `:402` (§B8), `netplan` `:405` cite pinned to commit 5cb27ab = tag `import/1.1.2-8ubuntu1_24.04.3`, `:407` (§B9; `parse.c` not re-read), `livecd-rootfs` `:417` (§B10; the presets clause not checked), `glean` `:422` (§B7). `georges-oopsla07` `:114`: "a cap of about thirty runs" → "caps at a preset number of runs (its example: 30)" (B3's WORDING-FIX on the entry).
- **D-X-01** (enterprise/VDI/cloud traces) — `grounding-sources.md:59`: the row restricted to the cluster traces 9.12 S3-08 read (Google 2011 and 2019, Alibaba v2018) and what their schemas hold; "process identity absent or hashed" (no record), Azure and VDI dropped.
- **D-X-02** ("never released, largely for privacy", unsourced) — `grounding-sources.md:61`: "the trace searches found no raw timeline with names released by these studies", with the 9.10 and 9.12 S3 records.
- **Other notes** — the stale "5 to 45": `references.md:129` (`chow-aoms65`), `:134` (`cochran-st77`) → "5 to 77". Pointer slips `:38`, `:39`, `:59`, `:64` as above. `c6-dual.timeline.yaml:33` is the data chunk's.

## Trace audit — outside (`claims/outside-findings.md`), the parts in my files

- **A-09** wording at `grounding-sources.md:30` — applied with D-F1-31.
- **B-17** overlap, `linux-sched-bwc` role — `references.md:326`: "per-class" → "per-group".
- **D-42** overlap, `cpsmark-tbench23` role — `references.md:34`: sensitivity per workload (Table 4) and per module (Table 5, §4.7.2), as the earlier record R04 states (B4 and B3 UNVERIFIABLE on this point, so R04 stands).
- **C-42** wording in `procyon`'s role — `references.md:239`: "three vendors' taxonomies" → two (UL makes Procyon and PCMark 10, BAPCo SYSmark 30).
- **E-29**, **E-50**, **F-48** and the rest — guidebook or other files; not mine.

## Measurement audit (`meas/class-findings.md`, `meas-new/proposed-text.md`)

- **F3** (typing `input_run` floored at zero) — doc part, `measurement-overview.md:63`: "bounded below by zero, a window quieter than the idle rate carrying no input work (9.5 D13)". Scope text is the data chunk's.
- **F4** (component definition) — `measurement-overview.md:61`: for `chat-client` and `game-client`, one thread comm across the tree's processes.
- **F5** (renderers' alignment) — `measurement-overview.md:108` (§8 Compile fidelity), as the brief states it: the 12 hidden renderers wake together across processes in the measurement (9.8 D15's counts), the four bound tasks compile independently. Scope is the data chunk's.
- **F1, F2, F6** — code and data; not mine.
- **O1** — `measurement-overview.md:108`: the dispersion sentence replaced per the proposed text.
- **O2** — `measurement-overview.md:106`: the `video-editor` exception sentence deleted.
- **O3** — `measurement-overview.md:95`: `ThreadPoolForeg` and `mail-client`'s `SwComposite` added to the 1 µs floor sentence.
- **O4** — `measurement-overview.md:97`: the ledger paragraph added. Its script is cited at `_dev/research/jioh/task-9.16-exit-audits/meas-new/stability_ledger.py`, the proposed text's fallback, because `dataset/tools/meas/stability_ledger.py` does not exist at this chunk's time (C3 not applied). If the data chunk moves it, this citation changes to the new path.
- **G1–G3**, the memo and `docs/README.md` items — not mine.

## Handed-over checks (`handed/findings.md`)

- **F1** — no mention in my files.
- **F2** — applied with D-F1-45 above.
- **F3** — `archetype-plan.md:102`: `game-task-chain`'s `declared_class` `normal` labelled design, the 9.13 rebuild spec's default ("`normal` on every other entry"), `lavd-ossna24` recording no class and the 9.11 class census recording the entry as no measurement.

## Compiled-number audit (`compiled/findings.md`)

No location in my files.

## Not applied, for the lead

- `fiedler-gaffer04`, `mpv` and `chromium` also rest only on the registry author's reads (outside-findings B-32 to B-34, C-18, D-13, E-18, F-52); `reads/B4-reads.md` T-02 holds a blind read of all three. They were not in this chunk's list of entries to point, so their status lines are unchanged.
