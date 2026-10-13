# 9.21 — Consumer work for the generated layer — changelog

Sub-task 9.21 of Phase 9, on `jioh/dataset-rebuild`. Spec: `_dev/docs/spec/jioh/task-9.21-consumer-work-for-the-generated-layer.md` (the 2026-10-13 grill, nine decisions). Each entry below is one implementation decision or finding, with what it rests on.

## D1 — the manifest's record of a file: placements and segment labels (2026-10-13)

Spec decisions 1 and 4. The harness needs, per generated file, which C1 task set entered under which id suffix and which segments it is labelled in; the coverage tool needs each segment's mode, `background_wanted`, tier and `pre_committed_miss`. Neither is in the compiled artifact in that form (the distractor grid's two segments are both A while B's tasks carry `-s1`), and the generated timelines are not committed. So the generator writes both into the manifest's grid record (`gen.compose.compose_full` returns the placements beside the composed dict; `gen.compose.grid_record` reads the labels off it, the tier by the coverage tool's rule — the `familiarity` annotation, else the highest tier among the names of the tasks alive in the segment).

Shapes recorded: a composed grid file's k-th placement labels its k-th segment; the distractor grid's A is labelled in both segments and B in none; a program arrival (`element-desktop`, `7z`) is one task, not a placement; the ladder's one placement labels its one segment. `input` is whether the generator gave the placement an input window — false for a segment of `no_input_below` (4 s) or less (9.19 decision 3) and for a mode whose C1 file has no keystroke stream (media, meeting, gaming, idle, video-edit, photo, render, transcode, backup).

The five manifests re-blessed; `artifacts`, `demand` and `reports` byte-identical to the committed ones (checked section by section against `HEAD`), `inputs` moved on the generator's sources, `grid` gained `placements` and `segments`. Hashes: transition grid `e26aa8e667470fdcec9fc22b481e3c4618463091fcca3ad9bf60736317d4daad`, return grid `21826be3c642e5da021db075dbca114c370504e39b298acc2ef076e30c179608`, flap-stress `a8c271dd18a6bd50c67631bdb3626f052ed382c7e84fb12670a19c34919fa17d`, distractor grid `6d9192db966c209d5a1d34f46a154b8184158ef237ae4ed51c385a2f98050649`, familiarity ladder `2cb56e69e6cee4bc2f0cd2a94fd3b5a2934930147222bf985d7f324996dc9057`. The core set's and the variants' manifests unchanged (see D2).

## D2 — the coverage tables live beside the generator, not in `wlc` (2026-10-13)

Spec decision 4. The first implementation put the generated tables into `dataset/tools/wlc/grid.py`; the dataset suite then failed `test_manifest_pins_the_compile_inputs_by_content`, because the core set's manifest pins `wlc/*.py` by content (9.18 decision 5) — any edit there moves the core manifest and, through it, the variants manifest and the RQ0 gate spec's dataset pin, against the spec's invariant. The tables moved to `dataset/tools/gen/coverage.py`, which the generated manifests pin (they pin `gen/*.py`) and the core manifest does not; `wlc/grid.py` is byte-identical to 9.20's. `derive.py` writes the core grid and the generated tables into one artifact, `dataset/coverage-grid.json` (`generated.<set>`), and `--check` compares it.

The tables (from the committed manifests alone; `derive.py` output 2026-10-13):

| set | files | segments | per `true` cell | notes |
|---|---|---|---|---|
| transition grid | 480 | 960 | 60 | indexing/true: all 60 pre-committed misses (inherited from `c1-indexing`'s annotation) |
| return grid | 720 | 2,160 | 135 | indexing/true: 135 misses |
| flap-stress | 24 | 216 | mail 40, photo 32, meeting 40, gaming 64, render 40 | the three drawn pairs |
| distractor grid | 272 | 544 | 34 | misses: indexing 34; `code` modes 3 each (dev, compile, ml-train), `kdenlive` modes 3 each, `chrome` modes 1 each — the 26 of 9.20 decision 3 |
| familiarity ladder | 66 | 66 | 2–7 | t4 = t5 per mode (1 or 3 cells), 32 each in all; t3 for render and backup alone |

Every generated segment lands in a `true` cell: every C1 task set is the `true` side of its mode. No empty-cell rule applies (decision 4).

Observation, not a change: the tier column follows the coverage tool's convention that a finite task without `depart` is alive to the file's end, so the segment after a batch mode departs (the `departs` form, the return grid) still counts the finished job's names — `office/true` in the transition grid shows 5 t3 segments from compile's, indexing's and gaming's predecessors. The core set's table has the same convention; left as is.

## D3 — the scoring rule, and the chain head's suffix (2026-10-13)

Spec decisions 1–3. `scoring.with_generated(spec, manifest, only=None)` derives entries from the C1 ones per placement, as `with_variants` does per variant (9.14 decision 12); the rule's statement is in the scoring spec's header. Windows come from the manifest's `demand[rel].segments` (`t_start_us`, `t_end_us`), so the rule reads no compiled file; `lint_generated` then checks every derived term against the compiled file as `lint_terms` (the per-entry checks factored out of `lint_spec`, behaviour unchanged) checks an authored one.

Finding: the first lint over the five sets returned 282 errors, every one a gaming placement — `game.chain.1-s0: no task with that id`. The compiler forms a chain member's id from its task's id (`game-s0` → `game-s0.chain.1`), so the suffix belongs on the task id, before `.chain.<n>`; `scoring.suffixed` does that and the spec's text says so. Every other entity is a plain task id with the suffix appended.

Measured: the lint of the five sets' derived entries — 1,562 files read through `read_run_file` — takes about 2 min 50 s on the home machine (M1 Pro); it joins `make -C harness lint` (`scoring_lint.py`, skipped with `--no-generated`), which needs the generated build, as the core-set lint needs the core build.

Derived entries: see D10 for the per-set counts the lint prints.

## D4 — the distractor's arriving set carries no term (2026-10-13)

Spec decision 2 as implemented: B's placement is recorded with `segments: []`, and the rule derives nothing from a placement labelled in no segment. The score of a distractor file is A's C1 terms over the whole file (both segments are A, so the window spans the file and is omitted).

## D5 — no input window, no keystroke term (2026-10-13)

Spec decision 3 as implemented: a placement with `input: false` drops its `channel: input` terms and keeps its timer-channel and periodic terms. Consequences on the real sets: the return grid's 2 s middle and the flap-stress set's 2 s alternations carry no keystroke term for an interactive B; modes without a keystroke stream (D1's list) never carry one, as their C1 entries never did; the toy fixture's `tg-a` (dev → ml-train, the second placement without a window) derives the editor's keystroke P99 in the first segment and the training run's turnaround alone in the second.

## D6 — the manifest join, the selection and the pin (2026-10-13)

Spec decisions 5 and 6. `harness/tools/harness/manifests.py`: `records` (workload id → grid record), `keys` (the keys every record carries), `select(manifest, where)` (equality on each named key, a key no record carries a `KeyError`), `expand(spec, root)` (the spec's `files.select` entries expanded to ids and added to `reporting`, with the selected files' compiled paths under `dataset/build/<rel>` and their axes), `workload_path`. The experiment spec's schema gains `files.select` (manifest name + `where`, no `as`: a selection is reporting material) and `pins.generated` (one pin per manifest, like `pins.variants`); the evaluator's lint, the evaluator and the runner expand before anything else, the lint checks the pin's bytes and the keys, and the Layer-1 exclusion lint runs over the expanded list. The records' columns are unchanged; a line finds a file's axes by `workload_id` through `ctx["axes"]`.

The RQ0 gate spec is unchanged in its lists; its scoring-spec pin moved (D3's text), re-frozen at `0ff71b1ff946f5e45dceea3c13b4008d32a13255ed637d46989a2867b7474bbc`.

## D7 — the flip count and its cost over existing rows (2026-10-13)

Spec decision 7. `aggregates.flip_aggregates(agg_rows, schedule, log, grade_rows)` emits three `config_interval` aggregates for a recognizing run — `change_count`, `wrong_change_count`, `wrong_switch_excess_sum` — from the config schedule (an applied entry whose algorithm, params or cap differ from the entry before it; an entry stamped at or after `T_end` ignored, contract 7), the recognition log (entry k is query k − 1, contract 7's one-query-one-entry rule) and the run's graded queries (`config_correct` 0 at the query's `t_set_change`; an ungraded query never counts as wrong), summing the existing `excess_switch` rows over the wrong switches into MLFQ. The runner grades each recognizing run in its main loop, beside its aggregates, so the rows can read the grades; the later grading pass collects what the loop graded. The evaluator's `flip_cost` line prints the three per run with the file's score from the scores file.

Hand-worked on `mock-switch` (its schedule: boot MLFQ; a shorter-slice MLFQ entry; FIFO; MLFQ again — the switch whose per-switch excess the fixture's derivation gives as 100 µs) with a three-query log graded correct, wrong, wrong: 3 changes, 2 wrong, excess 100 µs (the wrong FIFO entry contributes none: no window into FIFO). The test also covers every-query-correct (0 wrong, 0 excess), an ungraded query, a one-entry schedule (0 changes) and an empty run.

The hold-time plan's table now says this line is what step 0 reads; a flip's cost beyond the per-switch excess is the RQ4 experiment spec session's to define, on real traces.

## D8 — build every run, with the criterion written down (2026-10-13)

Spec decision 8. No workflow changed. The dataset README states the strategy with the measurements (9.20 D10: 5 min 13 s of 12 min 04 s on the runner, 1,562 artifacts, `build/` 6.8 GB) and the revisit criterion — a set added, or the step's time or the build's size against the runner's storage. The storage figure rests on a new deployed-system reference, `gh-hosted-runners` (GitHub Docs, "GitHub-hosted runners reference", read 2026-10-13): the standard Linux runner for public repositories has 4 vCPU, 16 GB RAM and 14 GB SSD; the private-repository table's Linux row 2 vCPU, 8 GB, 14 GB. Entered in `docs/references.md` only (the dataset derives no value from it).

## D9 — documents restated (2026-10-13)

Spec decision 9. Dataset README (the record, the tables, the lints at generation, the CI strategy); `docs/harness/metrics.md` §8 (the flip row) and §13; `harness/tools/harness/README.md` (`manifests.py`, the rule, the line); `harness/experiments/README.md` (`files.select`, `pins.generated`, `flip_cost`); `harness/records/README.md` (the axes are not columns); the hold-time plan; `harness/CHANGELOG.md`. The harness guide, the coreset guide, the proposal, the research-claims chain and the daemon guide are 9.15's.

## D10 — verification (2026-10-13)

- Dataset: `make generated` 2 min 09 s (the five sets, 1,562 artifacts) on the home machine; the dataset suite 527 passed, 1 skipped (the generated-layer and coverage tests among them: the record's shapes, the tables' counts, the drift check); `check_build.py` on the committed manifests: 3,304 files, 7 manifests verified.
- Harness, the generated-layer lint (`scoring_lint.py`, 2026-10-13, after the chain-head fix): clean. Entries the rule derives — transition grid 480 files, 1,320 terms; return grid 716 files, 2,865 terms (the 4 without a term: idle → an interactive-only mode for 2 s → idle, whose middle placement has no input window and so no term); flap-stress 24 files, 248 terms; distractor grid 255 files, 374 terms (the 17 with A = idle derive none); familiarity ladder 64 files, 104 terms (the two idle cells derive none). Every derived entity exists in its compiled file and every window lies on its segment boundaries.
- Harness tests: the six files 9.21 touched or added (`test_manifests`, `test_scoring`, `test_scorer`, `test_experiment_spec`, `test_evaluator`, `test_runner`) 106 passed in 17 min 25 s (the runner's pipeline test and the ladder lint the slow ones); `experiment_lint.py` clean on the RQ0 gate spec (19 judging + 32 reporting files, the re-pinned scoring spec); the fixture lint and the guard-spec lint clean; the rest of the suite 192 passed in 16 min 38 s — 298 passed in all (284 before 9.21, 14 added), about 34 min on the home machine.
