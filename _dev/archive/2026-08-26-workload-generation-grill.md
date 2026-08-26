# Grill session — workload generation plan (2026-08-26)

Grill over the 8-topic agenda from the 2026-08-26 planning discussion, against the docs in `docs/workload/` plus `OPEN_QUESTIONS.md`, `RESEARCH_PROPOSAL_v2.md`, `SIMULATOR_PRIMER.md`. All decisions below are settled unless marked otherwise. Owner of contracts + workload dataset generation: 인지오. Teammates informed via memo (see TODO Phase 1); shared-contract items flagged for their attention there.

---

## A. Source registry & references (agenda items 1, 2, 4)

**D1 — Entry unit and id minting.** One registry entry = one citable artifact (one citation, one URL, one accessed date). LAVD is three artifacts (OSS NA 2024 slides, scx repo, LWN coverage), not one entry. Id derivation by `type`:
- scholarly → bibkey style `<label>-<venue><yy>` (label = first-author surname, or system name when the work is known by it): `dhakal-chi18`, `zhang-chb15`, `cpsmark-tbench23`, `lavd-ossna24`. Raw arXiv numbers banned as ids (they live in the citation fields).
- deployed-system → project name, no year (`pinned_version` carries freshness): `interbench`, `rt-app`, `ananicy-rules`, `steam-downloads`.
- measurement → `meas-ci` (see D5).
The minting rule lives as a section of `REFERENCES.md`; contributor recipe: read the id rule → add REFERENCES.md entry → add yaml entry only if the dataset derives from it.

**D2 — `roleD` renamed.** Key namespace never says "role": `meas-ci` for CI measurements, `meas-pending` for placeholders (linter rejects after freeze), `category_source: meas` for the three archetypes with no literature taxonomy. The A–D role letters survive only as doc-side vocabulary in the grounding doc.

**D3 — Locator validation.** Tags are `<source-id>:<locator>`; registry entries are keyed by bare source-id; each entry may carry an optional `locator_pattern` regex (e.g. `^s\d+$` for slide decks) that the linter validates full tags against. No pattern = bare-id tags only.

**D4 — Notes split by ownership.** `workload-dataset-sources.yaml` `notes:` records what the source establishes and its scope limits ("Dhakal IKIs are within-burst transcription only — no mouse, no think-pauses"). `archetypes.yaml` gets a per-entry `modeling_notes:` recording what our encoding invented on top ("`chain:` linearizes LAVD s16's graph; field names are our schema"). Boundary rule: a source tag justifies values and described structure, never field names.

**D5 — Citation ownership flipped.** `REFERENCES.md` owns every citation string and all citation-constituent fields (`cite`, `url`, `accessed`, `pinned_version`); the yaml registry (renamed `workload-dataset-sources.yaml`) keeps machine/derivation fields only: `type`, `locator_pattern`, `notes`. `cite` was unlintable presentation — dropped from the yaml. Drift is prevented structurally: every yaml id must have a REFERENCES.md entry (subset lint, CI-checked); REFERENCES.md additionally holds related-work-only bibkeys that never appear in the yaml.

## B. Measurement (agenda item 3)

**D6 — meas-ci adopted with the trust-scoping package.** CI-runner measurement supports structural/shape claims only (fork structure, counts, lifetime shapes, periods, heartbeat rates, comm strings); machine-relative absolutes (CPU %, IO throughput, io-wait fractions) are recorded with the runner spec and rank as "convention informed by measurement", never desktop truth. Each workflow runs N times and reports spread. Framing: characterization of software behavior, never desktop-performance measurement. Nearly everything meas-ci must supply is in the structural class (only compiler-child/io-stream have machine-relative absolutes).

**D7 — D-live dissolved by reclassification.** Parameters that would have needed live usage measurement are literature-grounded and move to Role C: input inter-arrival → `dhakal-chi18` (+ family shape from Roeser et al.), tab counts → `dubroy-chi10` / Test Pilot 2010 / `chang-chi21`. Role D's scope = exactly meas-ci.

**D8 — meas-live dropped from the research entirely.** No teammate Linux desktops known; a standing "validate later" conditional would leave published results provisional. The collection + privacy-scrub tool (a meas-ci byproduct) ships in the artifact anyway, framed as an open falsification invitation: "live-usage validation was not performed; we release the tool so any user can check our synthetic distributions against their own machine." No `meas-live` key is ever minted by us. Validation limitation stated for `desktop-interactive`; gaming validation would be circular against LAVD (also stated).

## C. Formats & interpretation contract (agenda items 6, 8)

**D9 — Terminology.** Input-2 files are **timelines** (`*.timeline.yaml`): segments + labels + bindings of (name, archetype) on a time axis. Pipeline: `archetypes.yaml + timeline (+ scenario catalog) + seed → workload` (canonical, the experiment-ready file — "workload" keeps its TERMINOLOGY.md meaning). Core timelines are hand-authored; the naturalistic generator emits timelines too — one compile path, so linter/invariants/provenance apply uniformly.

**D10 — Canonical lifetime split.** Segment-bound tasks carry pinned `depart` timestamps (the user closing an app is exogenous); `finite`/`spawned` tasks have no depart field — they end via their program's EXIT, at a scheduler-dependent time. Matches the archetype `lifetime` field one-to-one. (Rejected: fully pinned arrive+depart trace — open-loop, deletes the good-vs-bad config divergence RQ0 measures.)

**D11 — FORK stays a runtime primitive.** The compiler pre-samples the full ordered spawn table (child programs with concrete values) into the orchestrator's program; spawn *timing* emerges from the fork/wait-for-slot loop at run time. Simulator stays 100% RNG-free. (Rejected: compile-time spawn expansion — pins cc1 arrivals, so a bad scheduler faces the same fork-storm pace as a good one.)

**D12 — Governing principle (write into the format spec verbatim):** *compile time resolves all randomness; run time resolves all timing that scheduling can influence.* Exogenous times (top-level arrivals, segment boundaries, injections, segment-bound departs, input events) are pinned absolute in canonical; endogenous times (finite-task departs, spawn moments) are emergent.

**D13 — Absolute wake timing.** Sixth primitive `TIMER(period)` (wake at t₀+k·period, drift-free — rt-app's `timer` precedent) for periodic tasks; aperiodic input compiles to pre-pinned `{t, op: wake, target}` events in the canonical stream, tasks block on WAIT. Relative-SLEEP encoding rejected: it drifts, systematically underloading the machine exactly under bad configs (biases Layer 2 toward "bad configs aren't so bad"). Canonical op set closed: `{arrive, wake}` + pinned departs. OQ-6's real grammar gap was absolute time, not IO bandwidth.

**D14 — Contract status.** No simulator exists yet; the interpretation contract written from D10–D13 (+ single lane, + scaling pass) is part of the simulator's spec — contract first, implementation second. First integration test: one C1 workload end-to-end.

## D. Single lane & the four artifacts (new finding + resolution)

**D15 — The capacity collision, resolved at the dataset layer.** Multi-core-measured archetype demands (LAVD gaming: ~300 tasks at 65–95% of a many-core machine) cannot fit the simulator's single lane — but OPEN_QUESTIONS Q1 already chose single-core deliberately (more cores shrink the random-vs-oracle gap; EDF optimality; tuning pool built at 100–141% of one core). Multi-lane blast radius judged too large (Q1 overturned, Dhall's effect on EDF, executor fill-K semantics, tuning-pool redo, trace/metric changes). **Single lane stands, ratifying OPEN_QUESTIONS Q1(i)+(ii).** Additions to the workload plan:
- **Demand-budget rule (stated explicitly):** every compiled workload's aggregate demand lands in the measurable oversubscription regime (~100–150% of the lane); the per-file RQ0 admission test (OPEN_QUESTIONS Q8) is the enforcement mechanism.
- **game-task-chain scaling defense:** full ~300-task population with the long tail near-idle (LAVD: ~90% long-lived, mostly waiting) and the frame-critical chain scaled to the lane regime — justified by LAVD's own concentration stats (top 30–40 tasks = 95% of scheduling; 15–20 tasks = 60–70%). Recorded in `modeling_notes`.

**D16 — Four release artifacts, one pipeline.** 2 timeline sets × 2 compile modes: `coreset-native`, `coreset-single`, `generalset-native`, `generalset-single`. `-native` = as-measured demand, no lane scaling ("multi" rejected as a name: no specific core count or machine model is defined); `-single` = lane-scaling compile pass applied. Experiments run exclusively on `-single`; `-native` released for reuse with an explicit unexecuted-status line. Scaling is a per-archetype declared compiler pass (fields + rule + evidence in `modeling_notes`), never baked into `archetypes.yaml` values. CI invariant: variants of one timeline differ only in declared-scalable fields.

## E. Remaining plan closures

**D17 — Naturalistic distributions.** "Validated against Role D" is dead. Posture: means/switch-rates from literature (`mark-chi08`; `zhang-chb15` independently corroborates ~3-min switching); the family choice (lognormal vs power-law) is a stated assumption, with headline generalset numbers reported under **both** families (regeneration is one parameter + recompile). DesktopBench inter-action timings optionally as a secondary sanity check (license permits analysis, not redistribution). **General principle: every doc sentence of the form "Role D will validate X" must name its replacement — literature, meas-ci, sensitivity analysis, or stated limitation.**

**D18 — Build order adopted:** (0) REFERENCES.md + workload-dataset-sources.yaml → (1) archetypes.yaml v0.1 (meas-pending allowed) → (2) interpretation contract + canonical JSON Schema → (3) timeline→canonical compiler (scaling pass, linter, invariant tests) → (4) core timelines → (5) simulator Phase 0 built to the contract → (6) RQ0 gate (v0 table, coreset-single C1/C2) → (7) generator + generalset + full matrix. meas-ci workflows: independent parallel track from (0). Core timelines before simulator so authoring stresses the format while fixes are cheap.

**D19 — Archetype-plan OQ closures.** OQ-1: no `gpu_bound` flag (simulator CPU-only, single-lane) — closed by fact. OQ-2: S3 stays bound to `video-playback` as a stated modeling approximation in `modeling_notes` (conferencing unmeasurable on CI; inventing encode parameters forbidden). OQ-3: referee re-pointed to meas-ci (chromium vs Electron app under Xvfb, CDF comparison; do not pre-split). OQ-4: parallelism cap fixed by convention at `-j8` (between interbench's `-j4` and desktop `nproc` conventions), overridable at binding time; on one lane it shapes fork-storm width/queue depth, not throughput. OQ-5: lognormal by convention + sensitivity per D17. OQ-6: closed by D13's TIMER.

**D20 — Browser default.** Chrome wherever a file needs "a browser"; firefox introduced only where the coverage-grid fill wants name variety. Renderer-multiplicity parameter is defined against the Chromium process model (tab-count literature + meas-ci Xvfb); firefox bindings reuse it as a stated approximation.

**D21 — Dual-active label totality (§9.8) ratified:** (a) core authors only author defensibly-labeled mixtures, (b) the generator's hub defines the label, (c) genuinely ambiguous dual-actives are a documented resolution limit — **and shipped as a third C6 file** ("even the oracle cannot assign a label"), consistent with C6's pre-registered-miss pattern.

**D22 — Binding notes to record (agenda item 7):** wineserver → `system-daemon` is a provisional approximation (LAVD treats wine as part of the game graph; decide at topology-constructor implementation); P1 binds tracker-miner-fs-3 to `cpu-batch` deliberately (full-rescan state; everyday indexer stays `background-crawler` in C4/S14) — both go in `modeling_notes`.

---

## Verified sources (session research; all → REFERENCES.md in Phase 1)

- **Steam "Allow Downloads During Gameplay":** Valve, "Downloads automatically pause when launching a game," help.steampowered.com/en/faqs/view/**4F9E-6328-E9B8-47F9** (accessed 2026-08-26); documents the checkbox at Steam → Settings → Downloads and default pause-during-gameplay. Secondary: `71AB-698D-57EB-178C` (per-game setting). Article capitalizes title-case; current client UI sentence-case.
- **Keystroke inter-arrival:** Dhakal, Feit, Kristensson, Oulasvirta, "Observations on Typing from 136 Million Keystrokes," CHI 2018, DOI 10.1145/3173574.3174220 — mean IKI 238.66 ms (SD 111.60); dataset public (Aalto). Roeser, De Maeyer, Leijten, Van Waes, *Reading and Writing* 37:359–384 (2024), DOI 10.1007/s11145-021-10203-z — two-component log-normal mixture (fluent ~158 ms; pause component p≈0.34); OSF data. Killourhy & Maxion, DSN 2009, DOI 10.1109/DSN.2009.5270346 — public raw latency dataset (CMU). Scope caveat for notes: within-burst transcription intervals; no mouse, no think-pauses — grounds intra-burst gaps only; burst/pause macro-structure remains our modeling.
- **Tab counts:** Dubroy & Balakrishnan, CHI 2010, DOI 10.1145/1753326.1753426 — per-user medians mostly 1–6, long tail (max 42); N=21, biased sample. Mozilla Test Pilot "A Week in the Life of a Browser" v2 (2010), N≈27k — mean concurrent tabs ≈3.2, median weekly max <8, 25% hit ≥11; only aggregate tables survive (GitHub mirror); analysis is a Slate article (tier care). Chang et al., "When the Tab Comes Due," CHI 2021, DOI 10.1145/3411764.3445585 — median overwhelm threshold 8 (Q1–Q3 5–12), self-report. Limitation line: no post-2010 large-scale logged tab distribution exists publicly.
- **Task-switching study — author correction:** **Zhang, T., Sun, X., Chai, Y., & Aghajan, H.** (2015), "A look at task-switching and multi-tasking behaviors: From the perspective of the computer usage among a large number of people," *Computers in Human Behavior* 49:237–244, DOI 10.1016/j.chb.2015.03.012. (SOURCE_VETTING's "Yun et al." is wrong.) Verified: 31 days, 3,000 subjects, 15M+ records, 16,406 processes, CNNIC data, power-law **hub** structure ("star" is our paraphrase), avg switch ~every 3 min (corroborates Mark independently). Dataset unreleased.
- **DesktopBench/FOCAL:** dataset **released** — HuggingFace `HaoranYin/desktopbench` v0.1.0 (2026-07-19): 320 multitask + 100 A→B→A sessions + ground truth; data terms restrictive ("research inspection", no redistribution), scripts MIT. FOCAL still an arXiv preprint (2604.19541, v2 2026-07-18) — supports precedent claims only. Cite: Yin, Wen, Cao, Yuan, Yang; co-cite VideoGUI (arXiv 2406.10227) for session provenance. Methodological reuse unrestricted.

## Session outputs

- `_dev/TODO.md` Phase 1 = the documentation pass landing all of the above.
- Team memo written after the docs (links, not restatements); simulator-side items for 인경민 flagged there: single lane ratified, interpretation contract as the pre-built simulator spec, lane-scaling pass, what multi-lane would have cost.

---

## Addendum — sub-task 1.1 citation verification (same day)

Written during 1.1 (`REFERENCES.md`); every entry there is verified or explicitly marked `to-pin`/`provisional`. Corrections found beyond the session ledger above:

- **Mark-line reattribution:** both headline figures — ~12 min/working sphere (~10/day) AND ~3 min/task (>2 min/tool) — are **González & Mark, CHI 2004** (`gonzalez-chi04`, DOI 10.1145/985692.985707), verified against full text. CHI 2005 (`mark-chi05`) carries the companion ~11-min figure and the internal/external interruption split. **CHI 2008 contains neither figure** (it's the interruption-stress lab experiment). The "half of switches self-initiated" claim is NOT in the CHI 2014 paper. The 23:15 figure exists only in the 2006 Gallup Business Journal interview (`mark-gallup06`) — confirmed absent from all peer-reviewed papers. Cascades into 1.4 (§4 text) and 1.6 (vetting doc).
- **arXiv 1705.05937 identified:** O'Callahan et al., "Engineering Record and Replay for Deployability," **USENIX ATC '17** (extended TR = the arXiv id) → `ocallahan-atc17`; "make forks and execs 2430 processes, mostly short-lived" confirmed verbatim (§4.3).
- **arXiv 1203.2704 identified:** Coetzee, Bhaskar & Necula, "A model and framework for reliable build systems," preprint/UCB TR only → `coetzee-arxiv12`; the short-lived-processes quote is specifically about the *Linux kernel build*.
- **LAVD talk pinned:** Min, "Optimizing Scheduler for Linux Gaming," OSS NA 2024 (2024-04-17); slides `static.sched.com/hosted_files/ossna2024/9b/scx-lavd-oss-na24.pdf`. LWN secondary: Corbet, "Sched_ext at LPC 2024" (lwn.net/Articles/991205/) → `corbet-lwn24`.
- **Related-work corrections:** Park's title is "Learning-**Augmented** Computer Systems" (NeurIPS 2019); EEVDF is Stoica & Abdel-Wahab **1995** (ODU TR-95-22); Kgent's authors differ from SchedCP's (Zheng, Yang, Chen & Quinn, eBPF '24, DOI 10.1145/3672197.3673434); ASA = Wang et al., "Mixture-of-Schedulers…" (arXiv:2511.11628, no venue); SchedCP = "Towards Agentic OS…" (arXiv:2509.01245 v4, MLforSystems@NeurIPS 2025) — **no conference successor as of 2026-08-26** (re-check each submission); TuneAgent = arXiv:2508.12551; hpc-llm = Jadhav et al., arXiv:2506.02025 (alternate: 2511.11612); ghOSt/Decima/Firm confirmed as believed with DOIs; sched_ext + EEVDF kernel doc URLs verified live.
- **Still to-pin (submission-time, per standing policy):** PCMark 10 / SYSmark 30/25 / Procyon / Game Mode doc URLs + editions; OSTEP edition; VideoGUI full author list; SWELL-KW author list re-confirm; repo commit pins.
