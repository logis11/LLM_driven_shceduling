# grades

The grades file is Layer 1: how well a recognizer read the situation, measured against the ground truth written in the workload file, with no simulator in the loop. Its rows are pooled across workloads, so a row is identified by condition, table, and seed, never by a single file.

## What a row is

`level` says what kind of number the row is: a `statistic` over an axis (balanced accuracy on the binary attribute, raw accuracy against a measured majority baseline on mode and on algorithm choice, the Matthews coefficient), a `class_recall`, one `confusion` cell, or a `paired` difference against another condition on the same draws. Every row carries `pre_committed_miss_excluded`, which says whether the segments annotated as unrecognizable by construction were left out, `over_seeds`, its sample count `n`, `n_files`, and `n_seeds`. Intervals `ci_low` and `ci_high` come from a cluster bootstrap over workload files, seeded and pinned. `schema/grades.schema.json` is the machine form; `docs/harness/metrics.md` §7 and §8 define the statistics and fix which one goes on which axis.

Two things the shape encodes on purpose. A seed is a repetition of the same question, so seeds are averaged over rather than pooled, and a mean row never reads as more evidence than one seed's. And there is no macro-average anywhere: the attribute is binary and gets balanced accuracy, the multi-class axes get raw accuracy beside their majority baseline and per-class recall.

## How it is produced

```
python3 tools/grade.py --manifest grade-manifest.json --out-grades grades.csv [--out-records DIR]
```

The manifest names, per run, the recognition log, the compiled workload, and the driver table. The grader turns each log into recognition records rows (one file per run under `--out-records`), then pools them into the grades file. It exits 2 when a consistency message fired, which means the oracle was not perfect on a graded point, and that is a bug to chase, not a result.

A query is graded only when a non-`ambiguous` ground-truth segment covers its `t_set_change`, so the terminal snapshot and `c6-dual`'s ambiguous segment drop out. The headline accuracy excludes `pre_committed_miss` segments; the RQ0 report prints accuracy with and without that exclusion side by side.

## How it is read

The RQ0 gate evaluator reads it for the Layer-1 headline line and the exclusion-accuracy line. `tools/tests/fixtures/mock-grades/` holds hand-written logs with the expected records and grades.
