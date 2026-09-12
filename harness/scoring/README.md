# scoring

`scoring-spec.yaml` says, for every coreset file, what a good outcome is: a list of terms, each an entity, a primitive, a filter, an aggregate, a direction, and a weight. A file's score is the weighted sum of its terms' normalised shares. The spec carries terms only. Which files judge RQ0, which report, and which are excluded from aggregation is the RQ0 gate spec's business, never this file's.

**Frozen on 2026-09-12** (`../CHANGELOG.md`). The RQ0 gate spec pins its SHA-256, and the evaluator refuses to judge against a spec whose bytes have moved. A change is a changelog entry before any run reads it, and a new pin.

## How to read a term

```yaml
c1-compile:
  terms:
    - {entity: editor, metric: ready_wait, cause: wake, aggregate: p99, direction: lower, weight: 1.0}
    - {entity: build,  metric: turnaround,              aggregate: turnaround, direction: lower, weight: 1.0}
```

The editor's wake latency at the 99th percentile, lower is better, weight one; the build's makespan, lower is better, weight one. A `window` on a term restricts it to part of the file, which the C2 pairs use to score only the segment where the two files differ. The patterns by mode class, and the weights' reasoning, are in the file's own header comments and in the Phase 6 and Phase 7 specs under `_dev/docs/spec/jioh/`.

A derived file declares `base:` and repeats its base's terms verbatim; a counterpart whose label flips the base's `background_wanted` to false drops the batch terms, because unwanted work carries no term.

## The lint

```
python3 tools/scoring_lint.py            # or: make lint
```

The schema (`schema/scoring-spec.schema.json`) checks shape. The lint in `tools/harness/scoring.py` checks what a schema cannot: every entity is a task id in that file's compiled workload or a reserved name; each metric and aggregate form a scored pair with the direction that pair has; weights are positive; windows lie inside the file; a derived file matches its base per the dataset's recipes; and a variant that declares no base must differ from it, because identical terms without the declaration are a forgotten line. It reads the compiled coreset, so `make -C ../dataset dataset` comes first.

## Expected no-headroom files

The header of the spec names, before any run, the files and terms where no configuration can improve on the boot default, with the arithmetic. Those are results the pre-registered statistic absorbs, not files to remove later.
