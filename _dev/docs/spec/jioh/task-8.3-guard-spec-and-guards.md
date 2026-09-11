# Task 8.3 — Guard spec and guards

The guard spec data file, the guard code that reads it, the `guards` output file, the hand-written fixture, and tests. Parent: `_dev/TODO.md` (jioh, 8), sub-task 8.3; Phase 8 spec decisions 6, 7, and 11. Decided in the 2026-09-11 grill.

## Scope

- The guard spec: the eight guards with their parameters and groundings, a schema, a lint.
- Guard code producing a `guards` long-format file with its own schema.
- A new shared recognition-log reader.
- The `mock-guards` fixture and unit tests for the two pair guards.
- Doc touches: the harness guide's guard table, the metrics doc changelog and §8 pointer, the harness README, the fixtures README.

Out of scope: the rerun policy for determinism (8.6), the runner that writes the manifest (8.6), the `random-beats-oracle` report flag (8.7), guard exemptions (RQ0 gate spec, 8.8), the freeze (8.8), terminology entries and the docs index (8.9).

## Locked decisions

### 1. Unit and output

A guard judges one run, one (workload, condition, seed, boot default) invocation. The determinism guard and the C2 pair check compare two runs and write a row against each run in the pair. Results go to a `guards` long-format file with a schema, beside `aggregates` and `scores`.

### 2. Named code, parameters as data

Each of the eight guards is a named function in guard code. The guard spec supplies its parameters and grounding. The lint checks that the spec's ids equal the code registry's ids, that every entry has a non-empty grounding, that a version is present, and that the C2 pair list equals the pairs in the coreset variant recipe.

### 3. Result vocabulary

`pass`, `fail`, `not_applicable`. One row per (run, guard) always, so the file is a dense grid. `not_applicable` is reserved for a guard whose scope excludes the run by construction. A missing input is `fail` with a reason.

### 4. Determinism

The guard takes two traces and compares them by byte identity. Both hashes are recorded in the row. When and how the second execution happens belongs to 8.6.

### 5. Location

A new `harness/guards/` directory holds the guard spec, its schema, and the `guards` output schema. The guard spec's comment header carries the groundings. The lint runs as a third line under the harness `lint` target.

### 6. Provenance share

Quantity: the time-weighted `fallback_share` aggregate. Threshold 0.5, direction below, a stated assumption. `not_applicable` under `fixed`. The `c6-dual` case remains an exemption in the RQ0 gate spec.

### 7. Config age as a structural staleness check

For every non-boot schedule entry, the entry's apply time must fall before the end of the ground-truth segment containing its query's `t_set_change`. No numeric threshold. The latency distribution is recorded as the row's value. `not_applicable` under `fixed`. Ground truth is read from the compiled workload file. The `config_age_*` aggregates keep their meaning of time in force. The harness guide's guard table is corrected in this sub-task.

### 8. Starvation floor

Per task, the maximum `ready_wait` across all causes over the whole file, at or below 1 000 000 µs of virtual time. A stated assumption, superseded by the executor's declared starvation window when 인경민 states it, with a changelog entry. Applies under every condition.

### 9. Utilisation sanity

Utilisation at or below 1.0, and strictly above 0 for any workload the scoring spec carries terms for. Grounded as arithmetic; no reference.

### 10. Tick count

The primitives module's existing guard messages are the source. They are threaded through the records build into the `guards` file. The records CLI keeps its exit-2 behaviour for standalone use.

### 11. `validation` equals `provenance`

The guard reads the recognition log directly through a new `read_recognition_log` in the shared reader module and compares the log's `validation` sequence to the schedule's `provenance` sequence minus the boot entry, positionally. The reason names the first mismatching index. `not_applicable` under `fixed`. 8.4 reuses the reader.

### 12. C2 pair check

The guard spec carries the pair list as data, each pair with a `fixed_identical` flag: true for the P1 pair, false for P2 and P3. Under `fixed` the guard checks identical traces where the flag is true and is `not_applicable` where false. Under `random` it is `not_applicable`. Under every other condition it checks that the two traces differ. Pairing key: same condition, seed, and boot default. Identity is the trace hash.

*Amended 2026-09-11 (after the 8.6 smoke run): identity is the trace's body hash, every line after the header, and the manifest names each run's trace beside its rerun trace. The header carries the workload id, so two files' traces are never byte-identical as wholes: the whole-file hash failed every `fixed` pair and passed every recognition-driven pair vacuously. The determinism guard (decision 4) keeps the whole-file hash, since it compares one file with its own rerun.*

### 13. `random-beats-oracle` is not a guard

Handed to 8.7 as a non-blocking, per-judging-file flag in the report.

### 14. Fixture

One new fixture directory, `mock-guards`, in the shape of `mock-p1a`: a run file, a trace, a config schedule mixing `fallback`, `unmodified`, `clamped`, and `held`, a recognition log whose `validation` sequence mirrors it, a workload file carrying ground-truth segments, a `worked.md`, and an `expected-guards.csv`. The fixture carries a deliberate fail for the staleness guard and for the starvation guard, with the other run-level guards passing. A second recognition-log variant with one swapped `validation` gives the mismatch case. The two pair guards are covered by unit tests over pairs of hashes. The fixture lint validates `expected-guards.csv` against the `guards` schema.

### 15. Columns and spec fields

`guards` file columns: the run identity (`workload_id`, `condition`, `table`, `seed`, `boot_default`), `guard`, `result`, `value` (decimal string, twelve places, empty when not measured), `threshold` (the bound in force, copied from the spec), `partner` (the other run's workload id for the C2 pair check, the rerun's hash for determinism, otherwise empty), `reason` (non-empty on `fail`). Guard spec entry: `id`, `reads`, `threshold` with its unit, `direction`, `applies_to`, `grounding`. Top level: `version` and `pairs`.

### 16. Entry point

The library function `evaluate(runs, spec)` evaluates the whole run set at once, so pair guards find their partners. The CLI takes one manifest JSON listing the runs. The manifest is defined minimally here: identity fields, the input paths, and an optional rerun trace path. The runner in 8.6 writes it.

### 17. Doc touches

The metrics doc gets a changelog entry stating that no primitive, aggregate, constant, or floor changed and that guard thresholds live in the guard spec, plus a pointer in §8 where provenance shares and utilisation are named guard inputs. The harness README and the fixtures README gain entries. The data-contracts doc is untouched.

## Invariants

- Every threshold is either an arithmetic identity, a structural check, or a stated assumption written as such in the guard spec's grounding.
- Names in full: guard spec, RQ0 gate spec, RQ0 gate evaluator.

## Open items

- The guard spec starts at version 0.1; the freeze in 8.8 bumps it.
- `evaluate` also takes the scoring spec path, for decision 9's "where the file has terms".
- The starvation bound awaits 인경민's executor window.
