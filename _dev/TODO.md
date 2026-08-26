# Dev TODO

## Phase 1 [WIP] — Post-grill documentation pass
Land every decision from the 2026-08-26 workload-generation grill (`_dev/archive/2026-08-26-workload-generation-grill.md`) into the docs. Docs and registry files only — no compiler/simulator code.

Execution order: 1.1 → 1.2 (needs 1.1's id rule) → 1.3 / 1.4 / 1.5 in any order (1.4 and 1.5 tag against 1.2's keys) → 1.6 → 1.7 → 1.8 last (links to the finished docs).

- [WIP] **1.1** `REFERENCES.md` — id-minting rule section (entry = one citable artifact; scholarly `<label>-<venue><yy>` / deployed-system project-name / `meas-ci`); one entry per reference with full citation, tier, role line, and citation-constituent fields (`url`, `accessed`, `pinned_version`); all sources verified in the grill session (Steam setting article, keystroke + tab-count + task-switching citations, DesktopBench/FOCAL status) plus the existing vetted sources and related-work bibkeys
- [ ] **1.2** `workload-dataset-sources.yaml` — machine registry keyed by bare source-id: `type`, `locator_pattern`, `notes` (source scope/limits only); subset relation to REFERENCES.md (every yaml id has a REFERENCES.md entry — lint rule stated in the header)
- [ ] **1.3** Interpretation contract doc (the simulator spec): 6-primitive grammar (RUN/SLEEP/TIMER/WAIT/WAKE/FORK+EXIT), canonical op set `{arrive, wake}` + pinned departs for segment-bound tasks, the timing principle (compile time resolves all randomness; run time resolves all scheduling-influenced timing), runtime FORK with pre-sampled spawn tables, single lane, lane-scaling compile pass
- [ ] **1.4** `WORKLOAD_DATASET_BUILDING_PLAN` rewrite: adopted build order; four release artifacts (2 timeline sets × 2 compile modes → `coreset-native/-single`, `generalset-native/-single`, experiments on `-single` only); demand-budget rule; §7 → meas-ci with the scope-discipline package; D-live removed (literature reclassified to Role C; falsification-invitation framing for the released sampler+scrub tool); §4 distribution posture (stated assumption + two-family sensitivity); §9 closures (browser default, dual-active labels + third C6 file, OQ items)
- [ ] **1.5** `ARCHETYPE_LIBRARY_PLAN` rewrite: `modeling_notes` field; `meas-pending` rename; OQ-1–OQ-6 resolutions; game-task-chain scaling note (LAVD concentration stats); wineserver + P1 tracker-miner binding notes
- [ ] **1.6** Touch-ups: SOURCE_VETTING author correction (Yun → Zhang, chb15); OPEN_QUESTIONS Q1 marked decided (single lane ratified); TERMINOLOGY additions (timeline, workload variants, archetype, meas-ci); CLAUDE.md pointer to the REFERENCES.md citation recipe
- [ ] **1.7** `docs/workload/` cleanup: fix `WORKLOAD_GROUNDING_SOURCES (1).md` filename; one normative home per topic, superseded passages removed or marked
- [ ] **1.8** Team memo (one page, links to the updated docs instead of restating): per-owner impact — simulator side (spec now exists before the simulator; single lane ratified; what was avoided), recognition side (canonical folds, C5 tiers, chrome-default multiplicity)

## Backlog
- Build pipeline, in the adopted order: (1) `archetypes.yaml` v0.1 → (2) canonical JSON Schema → (3) timeline→canonical compiler + scaling pass + linter + invariant tests → (4) core timelines → (5) simulator Phase 0 to the contract → (6) RQ0 gate; meas-ci workflows as a parallel track from any point after Phase 1
