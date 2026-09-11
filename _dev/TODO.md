# Dev TODO

Single team tracker: one `##` section per person, each with its own phase numbering — a phase is identified as `(person, N)`. Harness artifacts are namespaced by the person's slug (`_dev/docs/spec/<slug>/…`, branches `<slug>/phase-<N>/…` — conventions in `CLAUDE.md`). The daily-work-harness skills operate on 인지오's section; the other sections track the team.

## 인지오 (jioh)

### Phase 1 [done] — Workload dataset groundwork
Land every decision from the 2026-08-26 workload-generation grill (`_dev/archive/2026-08-26-workload-generation-grill.md`) into the docs. Docs and registry files only — no compiler/simulator code.

Execution order: 1.1 → 1.2 (needs 1.1's id rule) → 1.3 / 1.4 / 1.5 in any order (1.4 and 1.5 tag against 1.2's keys) → 1.6 → 1.7 → 1.8 last (links to the finished docs).

- [x] **1.1** `docs/references.md` — id-minting rule section (entry = one citable artifact; scholarly `<label>-<venue><yy>` / deployed-system project-name / `meas-ci`); one entry per reference with full citation, tier, role line, and citation-constituent fields (`url`, `accessed`, `pinned_version`); all sources verified in the grill session (Steam setting article, keystroke + tab-count + task-switching citations, DesktopBench/FOCAL status) plus the existing vetted sources and related-work bibkeys
- [x] **1.2** `dataset/sources.yaml` — machine registry keyed by bare source-id: `type`, `locator_pattern`, `notes` (source scope/limits only); subset relation to docs/references.md (every yaml id has a docs/references.md entry — lint rule stated in the header)
- [x] **1.3** Interpretation contract doc (the simulator spec): 6-primitive grammar (RUN/SLEEP/TIMER/WAIT/WAKE/FORK+EXIT), canonical op set `{arrive, wake}` + pinned departs for segment-bound tasks, the timing principle (compile time resolves all randomness; run time resolves all scheduling-influenced timing), runtime FORK with pre-sampled spawn tables, single lane, lane-scaling compile pass
- [x] **1.4** `docs/workload/building-plan.md` rewrite: adopted build order; four release artifacts (2 timeline sets × 2 compile modes → `coreset-native/-single`, `generalset-native/-single`, experiments on `-single` only); demand-budget rule; §7 → meas-ci with the scope-discipline package; D-live removed (literature reclassified to Role C; falsification-invitation framing for the released sampler+scrub tool); §4 distribution posture (stated assumption + two-family sensitivity); §9 closures (browser default, dual-active labels + third C6 file, OQ items)
- [x] **1.5** `docs/workload/archetype-plan.md` rewrite: `modeling_notes` field; `meas-pending` rename; OQ-1–OQ-6 resolutions; game-task-chain scaling note (LAVD concentration stats); wineserver + P1 tracker-miner binding notes
- [x] **1.6** Touch-ups: source-vetting corrections (Yun → Zhang chb15; Mark-line figures repointed — both the ~12-min and ~3-min figures belong to `gonzalez-chi04`, CHI 2008 carries neither, 23:15 is Gallup-interview-only); OPEN_QUESTIONS Q1 marked decided (single lane ratified); TERMINOLOGY additions (timeline, workload variants, archetype, meas-ci); CLAUDE.md pointer to the docs/references.md citation recipe
- [x] **1.7** `docs/workload/` cleanup: fix `grounding-sources (1).md` filename; one normative home per topic, superseded passages removed or marked
- [x] **1.8** Team memo (one page, links to the updated docs instead of restating): per-owner impact — simulator side (spec now exists before the simulator; single lane ratified; what was avoided), recognition side (canonical folds, C5 tiers, chrome-default multiplicity)

### Phase 2 [done] — Workload dataset generation
Build steps 1–4 of the adopted build order plus repo handoff. Spec: `_dev/docs/spec/jioh/phase-2-workload-dataset-generation.md`.

Execution order: 2.1 ∥ 2.2 in any order or parallel → 2.3 (needs both) → 2.4 → 2.5 last; 2.6 parallel from any point, its fold-in lands before 2.4's final compile.

- [x] **2.1** `dataset/archetypes.yaml` v0.1 — 12 entries per archetype-plan §4–§5; `meas-pending` placeholders allowed; `modeling_notes` from day one incl. the two decided binding notes (wineserver provisional, P1 tracker-miner → cpu-batch)
- [x] **2.2** Canonical JSON Schema — machine form of interpretation-contract §4 (`meta` / `ground_truth` / `events`, closed `{arrive, wake}` op set)
- [x] **2.3** Timeline→canonical compiler + lane-scaling pass + linter + invariant tests, wired into GitHub Actions; emits per-file static demand estimate; base timeline format fixed in this sub-task's spec session
- [x] **2.4** Core timelines — ~6 novel designs + derivation scripts → ~24 files × 2 modes (`coreset-single`/`coreset-native`); coverage-grid fill; files land in the ~100–150% demand window by the static estimate; authoring sugar (`variants:`/`inherit()`/`inject:`) fixed in this sub-task's spec session — 13 novel + 11 derived, all windows green on cli:3 numbers; grid signed off 2026-08-28 (tier concentration by design; grid counts spawn-child names)
- [x] **2.5** Repo prep + onboarding docs — per-teammate reading paths + repo working-structure prep; contents decided in its own session — component trees + per-tree Makefiles; dataset README; background/simulator/daemon guides; data-contracts; recognition vocabulary + config schema + trace format frozen; team-wide TODO restructure; proposal/contract sweeps (archive: `_dev/archive/2026-08-28-task-2.5-repo-prep-and-contracts.md`)
- [x] **2.6** meas-ci campaign — three workflow families in `.github/workflows/` (headless CLI, Xvfb GUI, name verification; building-plan §7), N runs with spread; analysis folds measured parameters into `archetypes.yaml` replacing the 15 `meas-pending` tags (registry tags `meas-ci:<workflow>:<run>`); fold-in lands before 2.4's final compile — batches cli:1/gui:2/names:1; 11/15 folded, 4 stay pending with stated findings (cache-hot corpus, foreground no-throttle); raw data: release `meas-ci-2026-08-28`

### Phase 3 [done] — Verification and protocol freeze
Stage 0 of `_dev/docs/rq0-preparation-notes.md`. Spec: `_dev/docs/spec/jioh/phase-3-verification-and-protocol-freeze.md`.

Execution order: 3.3 → 3.4 (the sweep checks labels against 3.3's freeze); 3.1 and 3.2 independent, any time.

- [x] **3.1** Demand estimate into the build manifest — compiler writes per-file `utilization` and `demand_class` into `dataset/build.manifest.json`, tests cover it; run the check, record the six C1 values and the judging-set conclusion (6 or 12 files) in the session archive
- [x] **3.2** `c6-dual` check — state what oracle and validator do with `mode: ambiguous` / `dual_active`; one sentence in `daemon-guide` at the oracle spec (out-of-menu labels undefined for the oracle, deferred past RQ0); finding in the archive
- [x] **3.3** Protocol freeze — run file, visible projection, telemetry, config schedule, recognition log → `frozen` by ratified decision (table + section leads); proposal stays `draft` with its Phase 4 note; glossary `frozen` definition amended; changelog section added to `data-contracts` with the freeze as first entry
- [x] **3.4** Vocabulary and status sweep — grep `docs/` for the retired vocabulary and audit every status label against the two freezes; fix stale lines (`terminology.md` five-mode paragraph + attributes, proposal Part 9 Phase 1 row, proposal Part 5 `interactive` mode values, building-plan's `demand: calibration` sentence); list variant-B divergences for Phase 4 in the archive

### Phase 4 [done] — Driver table format
Stage 0.5. Spec: `_dev/docs/spec/jioh/phase-4-driver-table-format.md`. Branch: `jioh/driver-table-v0`.

Execution order: 4.1 → 4.2 → 4.3.

- [x] **4.1** Ground the boot default — each config-schema default traced to a primary source (`docs/references.md` entry) or marked an unverified stated assumption with the `fixed`-under-alternative-defaults sensitivity check written down; changelog entry in `recognition-vocabulary`
- [x] **4.2** Driver table contract — JSON schema + lint (structure, legality, byte-identical `wanted` pairs, calibrated-full) with tests and fixtures in the daemon tree; `data-contracts` driver-table section with the row structure and an example; proposal contract frozen with the `llm_algo` read-scope rule; changelog
- [x] **4.3** Doc corrections — proposal §5.2 / §4.6 + RQ3 (delegation rung reframed; prior/calibrated naming; held-out-rows arm as a proposal) / §8.2 decision 3; `daemon-guide` §5 mapper steps; vocabulary variant row; terminology; archive note superseding Q4's row shape

### Phase 5 [done] — Primitive metrics and the records pipeline
Stages 1–2. Spec: `_dev/docs/spec/jioh/phase-5-primitive-metrics-and-records.md`. Branch: `jioh/primitive-metrics`.

Execution order: 5.1 → 5.2 ∥ 5.3 → 5.4.

- [x] **5.1** Mock traces — four reduced run-file + trace pairs (`c1-office` with a queued keystroke and an unfocused task; `c1-media` with backlog; `c2-p1a` with the config switch and an unfinished batch; a three-stage chain with one late frame) and their hand-computed expected records CSVs
- [x] **5.2** Metrics doc — trace and recognition primitives, the aggregate list, normalisation and floors, constants with verified sources, the simulator assumptions, the records schema description; doc corrections (`data-contracts` §9 pointers + `deadline` example + changelog, docs index, terminology wording)
- [x] **5.3** Trace reader — streams plain/gzipped JSONL, validates the closed event set, ignores `x_`, captures `meta`; run-file inputs (chain topology, demand, `T_end`); test-first against the mocks
- [x] **5.4** Primitives + records output — `ready_wait`, `job` with chain reconstruction, lifetime rows, `config_interval`, `preempt_count`, `busy`; CSV writer + machine schema beside the code; CI workflow; byte-for-byte match against 5.1's expected CSVs

### Phase 6 [done] — Driver table v0 and the scoring spec
Stage 3 plus the harness side of the 2026-09-08 switch-semantics memo. Spec: `_dev/docs/spec/jioh/phase-6-driver-table-v0-and-scoring-spec.md`. Branch: `jioh/driver-table-v0`.

Execution order: 6.1 → 6.2 → 6.3 → 6.4.

- [x] **6.1** Switch overhead — `switch_window` primitive in the metrics doc and in code; `hogs` records column; the two aggregates (per-switch excess wake `ready_wait`, switch and boost variants; share of the window inside switch windows); FIFO → MLFQ mock fixture with hand-computed values; `x_mlfq_level` check tool beside the harness; boost-timer restart at `t_apply` as a stated assumption
- [x] **6.2** Scoring spec — the terms and weights locked in the spec (P99 / miss rate / progress / makespan; C2 window 60 s–`T_end`; derived files equal their base; `c6-dual` two foregrounds; `c1-idle` none) as YAML in the harness tree with schema, lint (entity exists in the compiled workload, legal metric/aggregate pairs, fixed direction, positive weights, windows in range, derived-equals-base), tests, CI; metrics doc pointer, docs index, harness study guide
- [x] **6.3** Prior table — all 32 rows, any algorithm by theory, `basis: theory`, one sentence on row and entry, references ids only where they exist; `make -C daemon lint` green
- [x] **6.4** Pair review — the 16 same-mode pairs and the three C2 row-pairs as exercised (`ml-train/true`–`indexing/false`, `gaming/true`–`gaming/false`, `render/true`–`backup/true`); one sentence each naming the knob, the scored term it moves, and agreement with the weights; fixes fed back into 6.3; recorded in the phase archive with the intended file classification for Phase 7

### Phase 7 [done] — Coreset attribute coverage
Fix from the Phase 6 pair review: the coverage grid tracked mode × familiarity only, so the coreset instances 17 of the 32 driver-table cells. All 32 cells in the coreset, paired. Spec: `_dev/docs/spec/jioh/phase-7-coreset-attribute-coverage.md`. Branch: `jioh/coreset-fix`. Archive: `_dev/archive/2026-09-11-phase-7-coreset-attribute-coverage.md`.

Execution order: 7.1 → 7.2 → 7.3 → 7.4 → 7.5; 7.6 parallel with 7.4 and 7.5; 7.7 after 7.5 and 7.6 (added 2026-09-10).

- [x] **7.1** Grid attribute axis — one row per driver-table cell (32 × five tiers), `ambiguous` outside, recognition-limited cells marked; CI fails on an empty cell; committed grid regenerated; the recounted 17-cell baseline recorded
- [x] **7.2** Ten new C1 bases — `mail`, `dev`, `photo`, `meeting`, `video-edit`, `ml-train`, `render`, `transcode`, `indexing`, `backup`; task sets lifted from their source segments with the source in the header, batch jobs sized to 60 s, `meeting` designed as a live call with a periodic consumer, `c1-indexing` the user-initiated `true` cell
- [x] **7.3** C7 counterparts — the C7 variant file and sixteen `c7-<mode>` files: interactive modes inject `clamscan`/`cpu-batch` at 0 s for 60 s; batch modes swap the orchestrator name (name search + name-verification workflow, tier rule, `docs/references.md` entries where cited); cells with no visible cue shipped as pre-committed misses with `initiated`; authored `demand: calibration` on all C7 files and the eight existing derived files; the vocabulary's batch-mode clause + changelog
- [x] **7.4** (absorbed into 7.3 on 2026-09-10 so CI is green after 7.3) Scoring entries — the ten bases by the mode-class pattern with the mode's existing weight (exact entities and numbers fixed here), the sixteen C7 entries with `base` and the "unwanted work carries no term" rule, the lint clause, tests green; `indexing/true` cap fed to the prior table as derived
- [x] **7.5** Pair review — one sentence per new pair (16), per-pair window landing from the manifest, tier mismatches and pre-committed-miss cells recorded; fixes fed back into `prior.yaml`; `make -C daemon lint` green
- [x] **7.6** Docs sweep — building plan §3 C1/C7 entries and counts, §5a demand-budget paragraph naming C7 among the exempt families with the reason, §4 generalset all-32 requirement, throwaway pool named as open; dataset-design table; dataset README; terminology; docs index; coreset guide and harness guide; Phase 8 note on C1 at sixteen files
- [x] **7.7** RQ0 judging set after the coreset change — re-decide the judging set now, in its own grill, with C1 at sixteen files and C7's sixteen counterparts in view (Phase 3 set it as the six C2 files when C1 was six); write the decision as a Phase 7 spec decision and into every place that names the set: the harness study guide §15.1, the team memo §8, the RQ0 preparation notes §4.1 and the §8 gate sketch (file lists, separate lines, Layer-1 exclusion of pre-committed misses), the building plan's build-order line (6) and §3 C1 role sentence, the proposal's Phase 1 sentence; threshold, `random` draw, and failure procedure stay Phase 8's

### Phase 8 [WIP] — Harness upper half through pre-registration
Stages 4–5. The harness from `records` to a verdict, run end to end on mocks, ending at the committed RQ0 gate spec. Spec: `_dev/docs/spec/jioh/phase-8-harness-upper-half-through-pre-registration.md`. Branches: `jioh/harness-upper` for 8.1–8.7 and 8.10 (PR to `main`); `jioh/rq0-gate-spec` off `main` for 8.8–8.9.

Execution order: 8.1 first (added 2026-09-11; every later sub-task reads the boot default) → 8.2 ∥ 8.3 ∥ 8.4 ∥ 8.5 in any order or parallel → 8.6 after 8.5 → 8.10 after 8.2 and before 8.7 (added 2026-09-11; the report shows the aggregates it completes) → 8.7 after 8.2, 8.3, and 8.10 → 8.8 after 8.6 and 8.7 → 8.9 last.

- [x] **8.1** Boot default from OSTEP — the MLFQ boot default re-sourced whole from OSTEP §8 (3 queues, 10 ms, doubling, 100 ms boost, allotment equal to slice, caveat quoted); EDF and LOTTERY slices equal to it by the same-granularity rule stated as the project's own; the latency floor untied at 1 000 µs with a floor-sensitivity line pre-registered; vocabulary provenance table and changelog, config-schema code, prior table, the two MLFQ fixtures, prose examples; pair-review finding 5 redone on the 10 ms residual slice (knife edge: two executor rules asked of 인경민 in the memo decide `c7-meeting`/`c7-media`; their judging-set membership re-decided in 8.8 once answered); team memo `docs/memos/2026-09-11-boot-default-from-ostep.md`. Spec: `_dev/docs/spec/jioh/task-8.1-boot-default-from-ostep.md`
- [x] **8.2** Scorer — the aggregates module (every §8 trace aggregate) and the scorer: records plus scoring spec to `aggregates` and `scores` (two long-format files with schemas); `boot_default` records column; censored turnaround and empty-filter rules; numpy and pandas adopted; the no-headroom term rule, the censored rule, and the percentile convention into the metrics doc with changelog entries; hand-written records fixture plus one end-to-end seam case. Spec: `_dev/docs/spec/jioh/task-8.2-scorer.md`
- [x] **8.3** Guard spec and guards — the guard spec data file beside the scoring spec (the eight guards, thresholds with grounding, schema, lint); guard code; the hand-written `held`/`clamped` schedule fixture; tests. Spec: `_dev/docs/spec/jioh/task-8.3-guard-spec-and-guards.md`
- [x] **8.4** L1 grader — recognition log against ground truth: recognition records rows plus a `grades` file (balanced accuracy with the Matthews coefficient on the binary attribute; raw accuracy with its majority baseline, confusion matrix and per-class recall on mode and algorithm choice); `pre_committed_miss` as a 22nd records column with the with-and-without-exclusion line; seeded cluster bootstrap over files and paired condition comparisons; the configuration-distance line; tests. Spec: `_dev/docs/spec/jioh/task-8.4-l1-grader.md`
- [x] **8.5** Invocation contract and mocks — the command shape into the data-contracts doc with a changelog entry; the mock daemon (faithful for `fixed`/`oracle`/`random`, no validator) and the mock simulator (trivial generator plus replay of the hand fixtures), under `harness/`. Spec: `_dev/docs/spec/jioh/task-8.5-invocation-contract-and-mocks.md`
- [x] **8.6** Runner with execution cache — matrix expansion (conditions including the two alternative-default `fixed` runs, seeds), invocation through the contract, cache keyed on input hashes and program versions; the full pipeline on mocks across all 50 coreset files. Spec: `_dev/docs/spec/jioh/task-8.6-runner-with-execution-cache.md`
- [x] **8.7** Per-experiment spec schema, RQ0 gate evaluator, report — the schema (generic part plus criterion section) with lint; the evaluator (generic part, RQ0's K-of-27 criterion, `invalid` on a failed guard); the machine-readable report and its rendering. Spec: `_dev/docs/spec/jioh/task-8.7-experiment-spec-evaluator-report.md`
- [ ] **8.8** Pre-registration — the RQ0 gate spec committed: K, g, N with their groundings in its own grill, the failure procedure, reporting lines, exemptions, pins; the scoring and guard specs frozen with the harness changelog; the driver table tuning set rule into the building plan §4 with the rename sweep and terminology entry; the memo to 박이안 and 인경민 (invocation contract, `random` reading, N pending)
- [ ] **8.9** Docs sweep — harness guide chapters for the upper half, docs index, terminology (RQ0 gate evaluator, per-experiment spec, guard spec), RQ0 preparation notes' stage ticks, proposal pointers
- [x] **8.10** Boost windows — a new primitive `boost_window` (one records row per boost instant inside an MLFQ interval, sized by the §6.9 rule and clipped at the next boost, on `switch_window`'s columns with a new `metric` value); the aggregates module computes the per-switch excess and its boost variant; `mock-switch`'s expected records gain its two hand-worked boost rows; metrics doc §6 primitive, §8, changelog; no simulator or daemon change (decided 2026-09-11 from 8.2's finding; 8.2 spec decision 9)

### Phase 9 — Integration and the RQ0 run
Stage 6. Swap mocks for the real simulator and daemon, end-to-end smoke, run all coreset files × 3 conditions, check guards before looking at results, judge per the RQ0 gate spec; on failure, config search before workload redesign. Depends on 경민's integration gate and algorithm extension and 이안's daemon.

### Backlog
- Naturalistic generator + generalset + full condition matrix
- Held-out-rows arm (research-proposal §4.6 item 3) — after the main experiments, on the calibrated table: blank a row to the schema defaults, compare `llm_vocab` and `llm_algo` on the files that exercise it. Design fixed by Phase 7 (2026-09-10): every row has a fixed pair, so the files per row are the C1 base (`true`) or C7 counterpart (`false`) plus any C2/C3 segment on that row; the row set is pre-registered as every row unless a stated reason excludes one; the RQ0 gate spec carries the pre-registration line. Needs the calibrated table, whose per-row tuning pool must itself cover all 32 cells (the generalset requirement, building plan §4) — the throwaway pool's definition (7.7 / Phase 8) decides that

## 인경민 (kyungmin)

### Phase 1 — Simulator to the first integration gate
Build the simulator per `docs/simulator/simulator-guide.md` (binding fine print: `docs/simulator/interpretation-contract.md`). The gate: one C1 workload runs end-to-end under a one-entry config schedule with byte-identical traces across reruns. Working order and sub-tasks are 경민's to define.

- [ ] **1.1** (sub-tasks to be defined by 경민)

## 박이안 (ian)

### Phase 1 — Daemon through the validator
Build the daemon per `docs/daemon/daemon-guide.md`: telemetry builder → recognizer interface with `fixed`/`random`/`oracle` → validator, emitting recognition logs for all 50 workloads (24 before Phase 7; format unchanged), bit-identical across reruns; local LLM inference setup (hosting, client interface, record/replay skeleton) in parallel. Working order and sub-tasks are 이안's to define.

- [ ] **1.1** (sub-tasks to be defined by 이안)
