# Task 8.2 — Scorer

The function from `records` plus the scoring spec to `scores`, with the aggregates module underneath it. Decided in the 2026-09-11 grill (paused for sub-task 8.1 and resumed after it). Parent: `_dev/TODO.md`, (jioh, 8), sub-task 8.2; phase spec `phase-8-harness-upper-half-through-pre-registration.md`, decisions 2, 3, 4, 12.

## Scope

- An aggregates module covering every trace-derived aggregate of the metrics doc's §8, scored or not, written to an `aggregates` file.
- The scorer: per-term shares by the metrics doc's §9 formula and floors, the file score as the scoring spec's weighted sum, written to a `scores` file.
- The records identity column that tells the alternative-boot-default `fixed` runs apart, in the records schema and the metrics doc.
- Metrics doc changes: the no-headroom term rule (phase decision 4), the censored turnaround rule, the percentile convention, the new identity column, with changelog entries.
- Tests: a hand-written records fixture and one end-to-end seam case.

Out of scope: the recognition aggregates and the L1 grader (8.4); guards (8.3); the mean over seeds, the per-file gap, and the verdict (8.7, the RQ0 gate evaluator); which files judge, report, or are excluded (the per-experiment spec); the alternative boot configurations' members (the team, written in 8.8).

## Locked decisions

### 1. Full §8 aggregates as a research-wide module

8.2 builds one aggregates module for every trace-derived aggregate in the metrics doc's §8 (over `ready_wait`, `job`, `cpu_delivered`, `demand`, `completed`, `turnaround`, `preempt_count`, `config_interval`, `switch_window`, `busy`), whether a term scores it or not. The guards and the report consume the same aggregates file; nothing recomputes an aggregate from records elsewhere.

### 2. Recognition aggregates belong to the grader

Mode and attribute accuracy, the confusion matrices, algorithm-choice accuracy, latency over correct rows, and their per-familiarity-tier forms are produced by the L1 grader with the recognition rows (8.4). 8.2 shares only its percentile and fraction helpers.

### 3. `boot_default` identity column

Records gain a nullable identity column, `boot_default`, carrying a short id of the boot configuration a run started in; empty means the primary. The scorer pairs `oracle` and `random` runs with the `fixed` run of the same `boot_default`, and the alternative-default shares reuse the same `oracle` and `random` rows against each alternative `fixed`. New `condition` values and directory layout were rejected.

### 4. Missing rows

A `turnaround` term whose task did not complete inside the window is scored as the window's end minus the task's arrival, a lower bound, with the term marked `censored` in `scores`; "did not finish" is worse than every finishing value. A term whose filter selects no rows (no `ready_wait` rows with its cause and entity inside its window, no `job` rows in its window) stops the scorer with an error: every scored entity is linted to exist, so an empty filter is a scoring-spec mistake, not a measurement. Treating either case by the no-headroom rule was rejected, since it would reward a condition that starved the job.

### 5. numpy and pandas

The aggregates module and the scorer use numpy and pandas, added to the harness's pinned requirements; the harness will carry them for the paper's tables and plots regardless. Percentiles call numpy with the interpolation method named explicitly, never the default, and the metrics doc states the convention. Every output value is written at one fixed decimal precision so identical records give identical files under the pinned versions and the tests stay byte for byte.

### 6. Two files with schemas beside the code

An `aggregates` file, one row per (workload, condition, table, seed, `boot_default`, entity, metric, aggregate, window) with its value, and a `scores` file with one row per term (the term's identity, the aggregate under `fixed`, `oracle`, and the condition, the improvement, the share, the weight, the `no_headroom` and `censored` marks) plus one row per file and condition for the weighted score. Both long-format CSV with a machine schema beside the code, as records has. The RQ0 gate evaluator and the report read `scores` and never recompute a share.

### 7. Pairing and windows

A run's `fixed` baseline is found by (`workload_id`, `boot_default`); `fixed` is shared across tables because its `table` column is empty by the metrics doc's rule. A term's `window` keeps rows whose anchor `t` lies in the closed interval, matching the observation window's "at or before" rule.

### 8. Tests

A new fixture of hand-written records files, not traces: one small workload with two terms under `fixed`, `oracle`, and `random` with two seeds, plus one `fixed` under an alternative `boot_default`; a `worked.md` deriving every aggregate, share, and score by hand; shaped to hit each rule above (a windowed P99, a miss rate, a progress term, a turnaround that finishes under `oracle` and is censored under `random`, one no-headroom term, the alternative-default pairing); the written `aggregates` and `scores` files compared byte for byte. One end-to-end case runs `mock-p1a`'s records as the `llm_vocab` run with hand-written `fixed` and `oracle` records for the same reduced workload, proving the seam between the records writer and the scorer.

## Invariants

- The scorer applies no constant that is not in the metrics doc's constants table or the scoring spec; the no-headroom term rule and the censored rule live in the metrics doc, not in code alone.
- Every number in `scores` is traceable to rows in `aggregates`, and every row in `aggregates` to rows in `records`.
