# mock-experiment — worked derivation

A per-experiment spec over the `mock-scores` workload (sub-task 8.7), with the guards and grades files it needs, the expected report the RQ0 gate evaluator must reproduce byte for byte, and the arithmetic behind every number in it. The scores and aggregates come from `../mock-scores/expected-scores.csv` and `expected-aggregates.csv` (derived in `../mock-scores/worked.md`); the guards and grades files here are hand-written inputs, not derived from traces or logs.

## The experiment (`experiment.yaml`)

One judging file, `mock-score`, no reporting files. Conditions `fixed`, `oracle`, `random`; two seeds (`s1`, `s2` in the scores file — the evaluator checks the count, the runner will label seeds 1..N); the primary boot default `ostep` and one alternative, `alt`. Criterion `k_of_n_gap` with K = 1, g = 0.5, reference `oracle`, compared `random`, seed statistic mean. Pins name fixture copies (`guard-spec.yaml` here, `../mock-scores/scoring-spec.yaml`, `../mock-grades/driver-table.yaml`, `build.manifest.json` here) so the fixture does not move when the committed specs change.

`layer1_exclusions: [mock-score]` because `workloads/mock-score.workload.json` carries a `pre_committed_miss` segment (50000–100000); the lint derives the same list from the file.

The three variants differ from the base by one field each:

| file | change | verdict |
|---|---|---|
| `experiment.yaml` | — | pass |
| `experiment-fail.yaml` | g = 0.6 | fail |
| `experiment-invalid.yaml` | no exemption | invalid |

## Per-file gap (Phase 8 spec, decisions 2–4)

A file's score under a condition is the scores file's file-level row; the oracle's is the weight sum, 2.5 (four terms, weights 1.0 + 0.5 + 0.5 + 0.5). The `random` score is the mean over seeds; the gap is one minus that mean over the reference.

| scored against | s1 | s2 | mean | gap = 1 − mean / 2.5 |
|---|---|---|---|---|
| primary | 1.639359 | 0.433333 | (1.639359 + 0.433333) / 2 = **1.036346** | 1 − 0.4145384 = **0.585462** |
| `alt` | 1.533876 | 0.210172 | (1.533876 + 0.210172) / 2 = **0.872024** | 1 − 0.3488096 = **0.651190** |

One of four terms (the video miss rate) is no-headroom in every run, so `n_no_headroom` is 1 of 4 and `all_no_headroom` is false. `random` does not beat the oracle (mean < 2.5).

**Verdict.** K = 1 judging file must show gap ≥ g. Base: 0.585462 ≥ 0.5 → met 1 of 1 → **pass**. Fail variant: 0.585462 < 0.6 → met 0 → **fail**; under `alt` 0.651190 ≥ 0.6, so the sensitivity line shows the alternative passing while the primary fails.

## Guards (`guards.csv`) and the invalid variant

Five runs × eight guards, all `pass` or `not_applicable` (`c2_pair` for every run; `provenance_share`, `config_age`, `validation_matches_provenance` for the two `fixed` runs), except `starvation_floor` on `random` s2: value 1 500 000 µs against the 1 000 000 µs threshold, **fail**. `random` s2 is a run the criterion reads on a judging file, so:

- base and fail variants exempt it (`guard_exemptions`: `starvation_floor` on `mock-score` under `random`, with a reason) → the failure is reported with `exempt: true`, `invalidating: false`, and the verdict stands;
- the invalid variant carries no exemption → `invalidating: true`, `verdict_detail.invalid_runs` names the run and the guard, verdict **invalid**, and the gap rows are still computed (0.585462) and reported.

## Sensitivity line (decision 12)

Verdict counts per boot default: primary met 1 (base) / 0 (fail); `alt` met 1 in both. A count is `available` when no non-exempt guard failed on the runs its gaps read — the `fixed` run of that boot default plus the shared `oracle` and `random` runs. In the invalid variant every count is unavailable (verdict `null`) since `random` s2 feeds both.

## Floor band (8.1 decision 4; 8.7 decision 11)

The judging file is re-scored in memory with the latency floor at 500, 1 000, and 40 000 µs (the fraction floor stays 0.01). At 500 and 1 000 nothing changes. At 40 000 two more terms fall below the floor — the editor P99 (oracle improvement 35 430) and the build turnaround (30 000) — and count at share 1:

| seed | editor (1.0) | video (0.5, nh) | train (0.5) | build (0.5, nh) | score |
|---|---|---|---|---|---|
| s1 | 1 | 0.5 | 0.5 · 0.5 = 0.25 | 0.5 | **2.25** |
| s2 | 1 | 0.5 | 0.5 · 0.2 = 0.1 | 0.5 | **2.1** |

Mean 2.175, gap 1 − 0.87 = **0.130000** < 0.5 → met 0 → the band reads pass, pass, fail.

## Layer-1 lines (`grades.csv`)

Hand-written for `oracle` (one seed) and `random` (`s1`, `s2`, and their mean, `over_seeds` 1): four graded points, two in the dev / wanted-true segment and two in the ml-train / wanted-false segment that carries `pre_committed_miss`, so the excluded set has n = 2.

| condition | statistic | excluded (headline) | included |
|---|---|---|---|
| oracle | attribute balanced accuracy | 1.0 | 1.0 |
| oracle | mode raw accuracy | 1.0 | 1.0 |
| random | attribute balanced accuracy | (0.5 + 1.0) / 2 = **0.75** | (0.5 + 0.75) / 2 = **0.625** |
| random | mode raw accuracy | (0.5 + 0.5) / 2 = **0.5** | (0.25 + 0.5) / 2 = **0.375** |

The headline line carries the excluded balanced accuracy per condition with the per-seed attribute confusion cells (counts, excluded set): oracle 2 true→true; `random` s1 1 true→true and 1 true→false; s2 2 true→true.

## Provenance breakdown

From the aggregates' `config_interval` shares per run: the two `fixed` runs are all `fallback` (fallback share 1), the other three all `unmodified` (fallback share 0), as `../mock-scores/worked.md` states for their schedule rows.
