# records

The records file is the harness's first product and the only thing every later stage reads from a trace: one row per raw observation, with the identity of the run it came from and the attributes its metric carries. Nothing in it is aggregated, weighted, or judged. If a number in the paper looks wrong, the records row it came from is where the trail starts.

## What a row is

A row is one observation of one entity at one time: a task's wait after it became ready, one job's latency against its period, one switch window's excess, one recognition query's grade. The columns are the run's identity (`workload_id`, `condition`, `table`, `seed`, `boot_default`), the trace's identity (`sim`, `source_sha256`), the observation (`entity`, `metric`, `t`, `value`), and the attributes a metric may carry (`cause`, `provenance`, `algorithm`, `index`, `period_us`, `predicted`, `truth`, `validation`, `familiarity`, `hogs`, `pre_committed_miss`). Empty cells mean the attribute does not apply. `schema/records.schema.json` is the machine form; `docs/harness/metrics.md` §5 is the definition and §6 lists every metric.

## How it is produced

`tools/records.py` builds one records file from one (run file, trace) pair, plus the daemon's config schedule when the run had one:

```
python3 tools/records.py --run RUN.json --trace TRACE.jsonl --schedule SCHEDULE.json --out records.csv \
        [--table prior|calibrated] [--seed N] [--boot-default STEM]
```

The readers validate the trace line by line and refuse it at the first violation. The primitives fold the event stream into rows and also emit guard messages, printed on stderr: a chain whose tail iterations do not match its head ticks, a stimulus count that disagrees with the run file, an applied config entry the schedule does not carry. The runner does the same in process for every run and records the messages in its manifest.

Recognition rows, entity `recognizer`, come from a different input, the recognition log, and are written by `tools/grade.py` as one recognition records file per run. Same schema, same columns.

## How it is read

`tools/score.py` reads records files, or directories of them, into aggregates and scores. The guards read a run's records for its identity and trace hash. `tools/check_mlfq_levels.py`, which is not part of the harness, reads the `x_mlfq_level` lines the readers skip and checks the switch windows against them.

## Conventions worth knowing

- Row order and column order are fixed, so two records files of the same run are byte-identical, which is what the determinism guard relies on.
- Times are integer microseconds; values are integers or decimal strings, never floats.
- `boot_default` is empty for a run on the primary boot default and names the stem of an alternative for a sensitivity `fixed` run.
- The six hand-written traces under `tools/tests/fixtures/` come with their expected records, computed by hand; `make lint` validates those against this schema.
