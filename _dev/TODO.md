# Dev TODO

## Phase 1 [done] — Workload dataset groundwork
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

## Phase 2 [WIP] — Workload dataset generation
Build steps 1–4 of the adopted build order plus repo handoff. Spec: `_dev/docs/spec/phase-2-workload-dataset-generation.md`.

Execution order: 2.1 ∥ 2.2 in any order or parallel → 2.3 (needs both) → 2.4 → 2.5 last; 2.6 parallel from any point, its fold-in lands before 2.4's final compile.

- [WIP] **2.1** `dataset/archetypes.yaml` v0.1 — 12 entries per archetype-plan §4–§5; `meas-pending` placeholders allowed; `modeling_notes` from day one incl. the two decided binding notes (wineserver provisional, P1 tracker-miner → cpu-batch)
- [WIP] **2.2** Canonical JSON Schema — machine form of interpretation-contract §4 (`meta` / `ground_truth` / `events`, closed `{arrive, wake}` op set)
- [WIP] **2.3** Timeline→canonical compiler + lane-scaling pass + linter + invariant tests, wired into GitHub Actions; emits per-file static demand estimate; base timeline format fixed in this sub-task's spec session
- [ ] **2.4** Core timelines — ~6 novel designs + derivation scripts → ~24 files × 2 modes (`coreset-single`/`coreset-native`); coverage-grid fill; files land in the ~100–150% demand window by the static estimate; authoring sugar (`variants:`/`inherit()`/`inject:`) fixed in this sub-task's spec session
- [ ] **2.5** Repo prep + onboarding docs — per-teammate reading paths + repo working-structure prep; contents decided in its own session
- [ ] **2.6** meas-ci campaign — three workflow families in `.github/workflows/` (headless CLI, Xvfb GUI, name verification; building-plan §7), N runs with spread; analysis folds measured parameters into `archetypes.yaml` replacing the 15 `meas-pending` tags (registry tags `meas-ci:<workflow>:<run>`); fold-in lands before 2.4's final compile

## Backlog
- Remaining build pipeline after Phase 2: (5) simulator Phase 0 to the contract → (6) RQ0 gate → (7) naturalistic generator + generalset + full condition matrix; meas-ci workflows as a parallel track from any point after Phase 1
