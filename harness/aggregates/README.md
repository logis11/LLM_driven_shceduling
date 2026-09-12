# aggregates

The aggregates file collapses a run's records into one value per (entity, metric, aggregate, filter, window): a p99 of wake latency, a miss rate, a turnaround, a provenance share. Every aggregate the metrics doc §8 defines is here for every run, whether a scoring term weights it or not, so the scorer, the guards, and the report all read the same file and nothing is computed twice in two places.

## What a row is

Identity columns as in records (`workload_id`, `condition`, `table`, `seed`, `boot_default`), then what was aggregated (`entity`, `metric`, `aggregate`), the filter (`cause`, empty for no filter), the window (`window_start_us`, `window_end_us`, both empty for the whole file), `index` where the aggregate is per switch, and `value` as a twelve-place decimal string. `schema/aggregates.schema.json` is the machine form.

Windows: the whole file always, plus any window a scoring term names for that entity and metric. A window keeps rows whose anchor time lies inside the closed interval.

## How it is produced and read

`tools/score.py` writes it, together with the scores file, from records:

```
python3 tools/score.py --records RECORDS.csv [RECORDS2.csv …] --out-aggregates aggregates.csv --out-scores scores.csv
```

The runner writes one aggregates file per experiment at `runs/<experiment>/aggregates.csv`. The scorer reads it to form shares; the guards read it for utilisation, provenance shares, and starvation; the RQ0 gate evaluator reads it for the provenance breakdown it prints beside every scored run and for the floor band, which re-scores the file in memory at other latency floors.

## Conventions worth knowing

- Percentiles follow the convention in `docs/harness/metrics.md` §8; a censored turnaround, a job still running at the observation window's end, is aggregated by the censored rule there.
- The recognition aggregates, accuracy and its kin, are not in this file; they are the grades file's.
- `tools/tests/fixtures/mock-scores/` holds hand-written records with their expected aggregates, and `make lint` validates the expectation against this schema.
