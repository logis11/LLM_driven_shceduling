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

### Phase 6 — Driver table v0 and the scoring spec
Stage 3. Scope the rows C1–C4 exercise; write v0 with one-sentence justifications; the Layer-2 scoring spec (C2 pair weighting, `c1-compile` trade-off, `c1-media` audio/video weighting); fill the remaining rows with defaults; pair review of same-mode `wanted=true/false` rows for distinctness.

### Phase 7 — Harness upper half through pre-registration
Stages 4–5. Scorer, guards, L1 grader, mock daemon + mock simulator with the full pipeline run on mocks, runner with execution cache, report with provenance. Ends at the committed gate spec: judging set, threshold, `random` draw definition and seed count (with 박이안), failure procedure, frozen scoring spec.

### Phase 8 — Integration and the RQ0 run
Stage 6. Swap mocks for the real simulator and daemon, end-to-end smoke, run all coreset files × 3 conditions, check guards before looking at results, judge per the gate spec; on failure, config search before workload redesign. Depends on 경민's integration gate and algorithm extension and 이안's daemon.

### Backlog
- Naturalistic generator + generalset + full condition matrix

## 인경민 (kyungmin)

### Phase 1 — Simulator to the first integration gate
Build the simulator per `docs/simulator/simulator-guide.md` (binding fine print: `docs/simulator/interpretation-contract.md`). The gate: one C1 workload runs end-to-end under a one-entry config schedule with byte-identical traces across reruns. Working order and sub-tasks are 경민's to define.

- [ ] **1.1** (sub-tasks to be defined by 경민)

## 박이안 (ian)

### Phase 1 — Daemon through the validator
Build the daemon per `docs/daemon/daemon-guide.md`: telemetry builder → recognizer interface with `fixed`/`random`/`oracle` → validator, emitting recognition logs for all 24 workloads, bit-identical across reruns; local LLM inference setup (hosting, client interface, record/replay skeleton) in parallel. The milestone is `daemon-guide` §8: recognition logs for 24 × 3, byte-identical on rerun. No driver table and no LLM anywhere in the graded path — config schedules wait on (jioh, 6).

Execution order: 1.1 → 1.2 → 1.3 → 1.4 → 1.5 → 1.6; 1.7 runs in parallel from any point and does not gate the milestone.

- [ ] **1.1** Tree scaffolding + projection loader — package layout under `daemon/tools/`, `make lint`/`make test` extended beyond the driver-table tooling, CI workflow stub. Loader reads a compiled `*.workload.json` and returns the visible projection only (`workload_id`, per-task `name`/`t_arrive`/pinned `t_depart`/`children` name+count); `events`, task programs and `ground_truth` are dropped **at the parse boundary** so nothing downstream can reach them (`daemon-guide` §2.1, §3). Ground truth is readable only through a separate oracle-only module that the other recognizers cannot import — enforced by a test, not by convention. Inputs come from `dataset/build/` (`make dataset` in the dataset tree); pin the `build.manifest.json` hashes the run was made against.
- [ ] **1.2** Telemetry builder — walk the projection's pinned events in time order over the name→count multiset, emitting one snapshot per set change. All five rules of `data-contracts` §5 are tested explicitly: count-only changes emit (`c6-spoof`'s 14th chrome), same-timestamp events coalesce into one snapshot, `processes` sorted by name for byte-identical reruns, the terminal snapshot is emitted, nothing else emits. Hand-checked snapshot counts for `c1-compile`, `c1-idle`, `c4-*` and `c6-spoof` recorded as fixtures.
- [ ] **1.3** Recognizer seat + the three trivial recognizers — the narrow interface (snapshot → proposal) that every condition plugs into, plus `fixed` (no consultation), `random` (uniform draw over the 16 modes × `background_wanted` from a seeded PRNG, seed recorded), and `oracle` (reads the covering `ground_truth` segment). Oracle hard requirement from `daemon-guide` §4: it must terminate normally and emit valid output for **every** coreset file — `c6-dual`'s `mode: ambiguous` / missing `background_wanted` may produce a rejected answer but must never raise. Semantics there stay undefined and deferred.
- [ ] **1.4** Validator — imports `daemon/tools/drivertable/config_schema.py` rather than re-typing menus or ranges, so validator and table lint cannot disagree. Mode/attribute menu checks, the five config rules of `recognition-vocabulary` §2 on the *composed* configuration (only the menu half is exercised in this phase — the three trivial conditions are `system`-only, so build the config half against the schema and leave it dormant until the mapper), and the four-verdict stamp `unmodified`/`clamped`/`held`/`fallback` with the carry-forward state machine behind `held` and the retreat rule behind `fallback`. Unparseable answers → `proposal: null`, `validation: "held"`, verbatim text kept in `raw`.
- [ ] **1.5** Recognition log writer — the §8 envelope (`workload_id`, `condition`, `seed`, `queries[]` with `t_set_change`, embedded `telemetry`, `proposal`, `validation`, `latency_us`), the per-condition `source` object (oracle: the segment it read; random: its draw; whitelist later: the rule that matched), `latency_us` 0 for non-LLM conditions. Machine schema beside the code, in the shape `harness/records/schema/` uses. Every condition fills `proposal.system` identically; `reasoning`/`situation` may be absent for non-LLM conditions.
- [ ] **1.6** Full sweep + determinism gate — run 24 workloads × {`fixed`, `random`, `oracle`}, validate every log against 1.5's schema, rerun and diff byte-for-byte; wire the sweep and the diff into CI. Cross-check with the harness: the `validation` sequence is what §7's `provenance` sequence must equal minus the boot entry, and the terminal snapshot's entry is expected to be ungraded (no covering segment). Hand off a sample log to 인지오 for the grader's log reader.
- [ ] **1.7** LLM inference setup (parallel, no graded output) — one client interface over two hostings: a hosted API for prompt iteration and a locally hosted quantized model for recorded runs (`daemon-guide` §7). Record/replay skeleton with the cache keyed `(workload_id, snapshot hash, prompt version)`, latency measured at record time including reasoning tokens. Decide the repeat-index design from `docs/memos/2026-09-07-repeat-samples-for-the-daemon.md` — record mode draws the model **N times per distinct snapshot**, each sample keeping its own `latency_us`, and the index lives either in N files or a top-level `repeat` field; the decision lands as one line in `data-contracts` §8 plus a changelog entry (on `main`, with 인지오).

### Backlog
- **Config mapper + config schedules** — the five mapper steps of `daemon-guide` §5 and latency stamping; blocked on the driver table from (jioh, 6). Closing this turns `fixed`/`random`/`oracle` into the RQ0 gate together with (kyungmin, 1).
- **Open decision §9.2** — which latency number is stamped into schedules on replay: raw per-query, one constant per model, or seeded draws from the measured distribution. Decide before the first schedule-emitting run; it shapes the RQ4 claim.
- **Open decision §9.3** — hold time / hysteresis. Instinct is no flap protection for the coreset; the C4 mid-segment distractor is the one case that could flip a config that should have been left alone. Decide consciously, revisit for the naturalistic set.
- **`whitelist` recognizer** — the hand-written rule list reproducing shipping Game Mode behaviour; no model needed, comes after the RQ0 gate.
- **LLM conditions** — `llm_vocab` / `llm_algo` / `llm_full` on top of 1.7's record/replay, with the read-scope rule applied before validation.
