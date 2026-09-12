# the `harness` package

The modules that the command-line tools and the runner call. They form one line from a trace to a verdict, and each hands the next a typed, schema-validated set of rows.

```
reader ──► primitives ──► records ──► aggregates ──► scorer ──┐
                                                               ├──► evaluator
guards ◄── outputs ◄──────────────────────────────────────────┤
grader (with drivertable) ─────────────────────────────────────┘
runner: invokes the programs and drives all of the above
```

## Module by module

- **`reader.py`** reads the four inputs: the simulator's trace, streamed and validated line by line with a refusal on the first violation; the run-file view of a workload for the three facts a trace does not carry (the observation window's end, chain topology, per-task demand); the daemon's config schedule for the params of each applied entry; the recognition log for the query sequence.
- **`primitives.py`** folds the event stream into raw observation rows, one per metric occurrence, knowing nothing about which file or condition it is looking at. It also returns the consistency messages that the `tick_count` guard reads.
- **`records.py`** runs the readers and the primitives on one pair, stamps every row with the run's identity, and reads and writes the records CSV in its fixed column and row order.
- **`aggregates.py`** turns one run's records into every aggregate the metrics doc §8 lists, whether scored or not, over the whole file and over any window a scoring term names.
- **`scoring.py`** loads and lints the scoring spec; **`scorer.py`** pairs each run with its `fixed` baseline and its `oracle`, forms the normalised share per term with the no-headroom and censored rules, and sums the file score.
- **`guards.py`** is the registry of the eight guard functions and `evaluate`, which judges a whole run set at once because the two pair guards need a partner; it also lints the guard spec.
- **`drivertable.py`** reads the driver table and composes a row's default entry into the configuration the simulator receives, byte-identical with the daemon's own composition; it is separate from the grader so that the mock daemon does not import numpy through it.
- **`grader.py`** is Layer 1: one recognition log graded against ground truth into recognition records rows, then the pooled grades with a seeded cluster bootstrap over files.
- **`outputs.py`** writes and reads the long-format CSVs the stages exchange, aggregates, scores, guards, and grades, each validated against its schema.
- **`evaluator.py`** is the RQ0 gate evaluator: it lints a per-experiment spec, verifies its pins, checks the run set is complete, applies the criterion and the reporting lines, echoes the spec's statements, and renders the report to Markdown. The registries of criterion types and line types live here; adding a line type is one function and one schema branch.
- **`runner.py`** expands a spec into the run matrix, invokes the daemon and the simulator through the invocation contract, twice each with byte-identical outputs required, caches every invocation, and drives every stage above to the report.

## Where the definitions are

`docs/harness/metrics.md` for every number, `docs/data-contracts.md` for every input format and the invocation contract, and each module's docstring for the decisions it implements, cited by sub-task.
