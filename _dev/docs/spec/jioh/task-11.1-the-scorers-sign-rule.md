# 11.1 — The scorer's sign rule

Sub-task 11.1 of 인지오's Phase 11 (`_dev/docs/spec/jioh/phase-11-rq0-failure-procedure-diagnosis.md`, decisions 2 and 3), decided on 2026-11-18: the scorer's reading of a term whose oracle is worse than fixed, the docs that state it, and the post hoc reading of the RQ0 run beside its verdict.

## Scope

- The rule in the scorer (`harness/tools/harness/scorer.py`): today a term is no headroom only when the oracle's improvement, taken without its sign, is under the aggregate's floor, so an oracle worse than fixed past the floor counts as headroom and the term's share changes sign.
- The "oracle worse than fixed" mark in the scores file and the report.
- Every doc that states the no-headroom rule, and the harness changelog entry.
- The RQ0 run re-scored under the fixed rule, its report re-rendered as a post hoc reading, and the dated correction in the RQ0 run record (`docs/rq0-run-record.md`) and the result memo (`docs/memos/2026-11-18-rq0-run-result.md`).

## Locked decisions

### 1. The rule

A term whose oracle is worse than fixed by more than the aggregate's floor is no headroom — share 1, as a term under the floor — and carries the mark "oracle worse than fixed". Every reading that re-scores — the variant lines, the floor band, the cap band — reads it through the same scorer. No pin moves, and the RQ0 gate spec is not edited.

### 2. The mark

The scores file carries `oracle_worse` on each term row, a subset of `no_headroom`, and `n_oracle_worse` on each file row. The report carries the same count on its per-file gap rows and on the headroom-count line's rows, and the rendering prints it in both tables. `no_headroom` keeps its meaning: a file whose every term is no headroom, under the floor or oracle worse, has no headroom.

### 3. The docs change with the rule

In this sub-task: the metrics doc's floor rule (`docs/harness/metrics.md` §9) and its changelog; the scorer's docstring and the descriptions in the scores schema (`harness/scores/schema/scores.schema.json`) and the report schema (`harness/experiments/schema/report.schema.json`); the harness guide's floor passage, its passage on the two no-headroom rules and its glossary row for floor (`docs/harness/harness-and-records-guide.md`); the research guidebook volume 4's glossary rows for floor and no headroom (`docs/guidebook/vol-04-experiment-design.md`); the harness changelog entry (`harness/CHANGELOG.md`). 11.5 sweeps only what 11.2 to 11.4 change.

### 4. The post hoc reading covers the whole report

The RQ0 run's outputs on disk are re-scored under the fixed rule and the whole report is re-rendered, every reporting line among it; the guards and the grades are reused, since neither reads the scorer. It is labelled post hoc throughout, never as a verdict. Its scores are what 11.4 picks from if 11.2 changes no run.

### 5. Where the post hoc report lives

`harness/experiments/rq0-gate/post-hoc/`, as `report.json.gz` and `report.md`. The rendering's header states that it is the post hoc reading under the fixed rule, not the verdict, and cites the harness changelog entry. The `rq0-gate/` line of `harness/experiments/README.md` gains the folder. The first report's folder keeps what the RQ0 run produced.

### 6. The correction

The RQ0 run record and the result memo gain a dated correction stating the sign inversion and citing the post hoc report with its counts. The first verdict and the first report stay as they are.
