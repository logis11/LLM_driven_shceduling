# Handoff — Phase 8 (jioh), written 2026-09-11

Phase 8's code half is finished on `jioh/harness-upper`: 8.1 to 8.7 and 8.10 are ticked, and a PR from that branch to `main` carries all of it, `_dev/` included. **8.8 and 8.9 are worked on a new branch, `jioh/rq0-gate-spec`, cut from `main` after the PR merges.** Nothing on `main` is needed from anywhere else first.

## Where things stand

- Phase spec: `_dev/docs/spec/jioh/phase-8-harness-upper-half-through-pre-registration.md` (21 decisions, three dated amendments). Sub-task specs for 8.1 to 8.7 sit beside it; 8.3's carries a dated amendment to decision 12 from this session.
- Done: 8.1 boot default, 8.2 scorer, 8.10 boost windows, 8.3 guards, 8.4 L1 grader, 8.5 invocation contract and mocks, 8.7 per-experiment spec, RQ0 gate evaluator, report, 8.6 runner with execution cache. Order was 8.7 before 8.6 so the runner reads a spec that already had its schema.
- **246 tests green**, four lints clean, under `/usr/local/bin/python3.12` (`PY=/usr/local/bin/python3.12` on every make call; the harness lint needs the compiled coreset, `make -C dataset dataset`). `make -C harness smoke` runs the whole pipeline on the mocks over all 48 scored coreset files, 192 runs, 384 invocations, and CI runs it after the suite; about eight minutes cold, five on a warm cache.

## Next: 8.8 — pre-registration

Its own grill decides K, g, and N with their groundings written beside the numbers (phase spec decisions 5, 16; K after g, N after both). What already exists for it to fill:

- **The per-experiment spec's schema and lint** (`harness/experiments/schema/experiment-spec.schema.json`, `tools/experiment_lint.py`). The RQ0 gate spec is `harness/experiments/rq0-gate.yaml`, the first real instance; the `mock-experiment` fixture (`harness/tools/tests/fixtures/mock-experiment/experiment.yaml`) shows every field filled. The generic part: conditions, `seed_count`, `boot_defaults` (primary stem plus alternative stems, files under `harness/boot-defaults/`), judging and reporting files, `layer1_exclusions` derived from `pre_committed_miss` and linted, `guard_exemptions` each with a reason, typed `reporting_lines`, and `pins` as SHA-256 hashes of the scoring spec, guard spec, driver table, and `dataset/build.manifest.json`. The criterion section is typed: `k_of_n_gap` with `k`, `g`, `reference`, `compared`, `seed_statistic`.
- **The reporting-line types** the evaluator knows: `sensitivity` (the alternative boot defaults), `floor_band` (latency floors), `exclusion_accuracy`, `layer1_headline`, `random_beats_oracle`, and `note` bound to a workload, which is how the `c7-gaming`, `c7-meeting`, `c7-media` judging notes and `c1-gaming`'s separate line are declared (decision 21).
- **The judging set** is still only prose: 27 files in `_dev/docs/rq0-preparation-notes.md` §8's YAML sketch and the rule at its "Judging (27)" paragraph (C2's six, the six batch C1 bases, the fifteen C7 counterparts with a term). The scoring spec disclaims owning it. The lint requires every judging file to have scoring terms.
- **Exemptions the smoke run predicts**: `c6-dual`'s `provenance_share` under `oracle` (the oracle is undefined inside its `ambiguous` segment and runs on `fallback`, so the share is 1). The old sketch also named `random-beats-oracle` and `fallback-share`, which are not guard ids; the first is a report line now.
- **The freeze** (decision 19): 인지오 alone, in a harness changelog that does not exist yet; the guard spec bumps from 0.1 there; the RQ0 gate spec pins the frozen hashes. The driver table tuning set rule into the building plan §4 with the rename sweep across nine files and the terminology entry (decision 18). The memo to 박이안 and 인경민 with the `random` reading and N pending (decision 20); the invocation contract was already told to both in `docs/memos/2026-09-11-invocation-contract.md`.
- **The alternative boot-default pair** is still the team's to pick (decision 12, amended in 8.1). Until it lands as two files under `harness/boot-defaults/`, the RQ0 gate spec's `alternatives` list is empty and the sensitivity line has no rows.

Then **8.9** docs sweep: the harness guide's chapters for the upper half (scorer, guards, grader, mocks and the invocation contract, evaluator and report, runner and cache), the docs index, terminology (RQ0 gate evaluator, per-experiment spec, guard spec, driver table tuning set), the RQ0 preparation notes' stage 4 and 5 ticks, the proposal pointers. The runner's README row is the only prose on the runner today.

## Conventions worth not relearning

- Segments are half-open, `t_start <= t < t_end`; the terminal snapshot at `t_end` is uncovered by design.
- The harness never imports the daemon's or the dataset's modules; where it must reproduce their logic a test pins the two (`compose_row` against the daemon's `compose`; `ostep.json` against the config schema's defaults). The driver-table reader now lives in `harness/drivertable.py`, re-exported by the grader.
- `fixed` runs carry an empty `table`; the scorer stamps its score rows with the group's table, and the evaluator maps them back. The scores' `boot_default` names the baseline scored against, the records' and guards' the run's own.
- The evaluator checks the compared condition's seed **count**, not the labels; the runner labels seeds 1 to N.
- Traces are asked for uncompressed: a gzip header carries a timestamp, so a `.gz` trace is never byte-stable across writes.
- The `c2_pair` guard compares trace **bodies**, header excluded, since the header names the workload; the determinism guard compares whole files with their own rerun.

## Measured facts worth not rediscovering

- Graded set on the coreset, now reproduced by the mock daemon in a test: 134 query points, 50 terminal and 2 `ambiguous` skipped, 82 graded over 49 files, 10 carrying `pre_committed_miss`, 72 over 44 headline.
- The mock daemon starts in 0.1 s after the driver-table split; the records build costs up to eight seconds on the heaviest mock trace (`c1-gaming`, 193k lines), which is what the smoke's runtime is.
- Smoke guard failures on the mocks, all expected: `c6-dual` provenance share under `oracle`; the P2 and P3 pairs under `oracle`, whose trace bodies are identical because the mock simulator models no scheduling, so a params-only change leaves its output untouched.

## Open threads

- **인경민's three questions** (8.1 memo §5): the two executor rules deciding `c7-meeting`/`c7-media` and their judging-set membership, re-decided in 8.8 once answered; the executor's starvation window, which replaces the `starvation_floor` guard's 1 000 000 µs stated assumption.
- **The alternative boot-default pair** (above).
- **Layer 1 is underpowered** for the whitelist comparison at 44 to 49 independent units; the familiarity contrast at tiers 4 and 5 rests on one graded point per tier (8.4 spec).
- **Run-to-run consistency** stays blocked on the recognition log's missing repeat index (memo 2026-09-07).
- **The CI smoke step** adds several minutes to every push; if that grows with the real programs, it can move to a schedule.
- **No archive written** for Phase 8 (archives only on request).
