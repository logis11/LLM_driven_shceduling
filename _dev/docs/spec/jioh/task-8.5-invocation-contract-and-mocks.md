# Task 8.5 — Invocation contract and mocks

The command shape through which the runner invokes the daemon and the simulator, written into the data-contracts doc, and the two mock programs that are its first implementations. Parent: `_dev/TODO.md` (jioh, 8), sub-task 8.5; Phase 8 spec decisions 9, 10, 11, and 15. Decided in the 2026-09-11 grill.

## Scope

- The invocation contract: a new contract in `docs/data-contracts.md` with a changelog entry, frozen in this sub-task.
- The mock daemon: `fixed`, `oracle`, and `random` over any coreset file, emitting contract-valid config schedules and recognition logs.
- The mock simulator: a trivial generator for any coreset file and schedule, and a replay of the hand-written fixture traces.
- The boot-default data files the runner passes to the daemon, with a schema.
- Tests, including three pinning tests, and the README rows for the new directories.

Out of scope: the runner and its cache (8.6), the whitelist and LLM conditions, a validator in the mock daemon, any change to the simulator tree or the daemon tree.

## Locked decisions

### 1. One run per invocation

One invocation of either program covers exactly one run: one workload file, one condition, one seed where the condition draws. The runner loops over the matrix and issues one process call per run. Batching is not part of the contract.

### 2. Named required flags

The runner passes every input and output as a named long flag on the command line. Every flag is required, no flag has a default, and there are no positional arguments. A missing input is a failure, never a silent default. The daemon's inputs are the workload file, the condition, the driver table, the boot default, and the seed under decision 6; its outputs are the config schedule and the recognition log. The simulator's inputs are the workload file and the config schedule; its output is the trace. The simulator receives no condition and copies the schedule's `condition` into the trace header.

### 3. Exit code and the streams

Exit 0 means every declared output was written. Any non-zero code is failure, and the runner treats the run's outputs as absent whatever is on disk. Contract-invalid input, such as a schedule without an entry at zero or a condition the program does not implement, is a non-zero exit like any other failure. Standard output is ignored. Standard error is captured to a log file beside the outputs for humans and is never parsed. The runner validates the outputs itself through the existing readers; the exit code is the only claim of success the process makes.

### 4. Frozen in this sub-task

The invocation contract is written as frozen, with a row in the contract table and a changelog entry. It is a new contract, not a change to a frozen one, so the three-signature rule of the freeze section does not gate it. 인지오 tells 인경민 and 박이안 directly.

### 5. Path discipline

The runner passes absolute paths and creates the output directory beforehand. The process writes exactly the declared output files and nothing else, so its working directory never matters and the output directory's contents are wholly the runner's to hash. Scratch space, if a program needs any, is the system temporary directory, about which the contract says nothing. The workload argument is always the canonical compiled file; each program's loader extracts its own view, as both guides already require. A trace is written gzipped exactly when its output path ends in `.gz`.

### 6. The seed flag

The seed is required for exactly the conditions that draw, `random` now and any LLM condition that samples later, and forbidden otherwise; the daemon exits non-zero on the wrong pairing. The seed is an integer. The recognition log's top-level `seed` is the given value or null as the frozen recognition-log contract already says, and the records' `seed` column stays empty for `fixed` and `oracle`.

### 7. Determinism as the one behavioural clause

The same argument line, seed included, must produce byte-identical declared outputs, and the seed is the only permitted source of randomness. This is the clause the determinism guard and the runner's cache stand on.

### 8. The boot default travels as a file

The daemon takes a required path to a small JSON file of the frozen configuration shape, algorithm plus params plus cap, copies it verbatim into the schedule's first entry, and uses it as its fallback. The runner owns the boot-default data; the daemon carries no copy of its own. The two alternative-default `fixed` runs are the same invocation with a different file.

### 9. Home and naming of the boot-default files

A new data directory `harness/boot-defaults/` with its own schema, following the harness convention that each data file gets a top-level directory beside the tools. It holds `ostep.json` for the OSTEP example now and the two alternatives later, named by content, never by role. The records' `boot_default` column, empty meaning the primary, becomes the file stem for the alternatives.

### 10. Program identity is not the program's to report

The contract carries no version channel. The runner's own configuration names each command together with a version string and hashes that into the cache key; the trace's existing `sim` header is cross-checked against it. The form of the version string is 8.6's decision.

### 11. The command prefix is the program's own

The runner appends the contract's flags to a configured command. Whatever the command prefix carries is the program's own business; this is how a real program takes its own options and how the mock simulator takes its replay flag.

### 12. Where the mocks live

Both mocks are command-line scripts under one new directory `harness/tools/tests/mocks/`, each a thin argument layer over a small importable module beside it, so tests call the functions and the runner calls the scripts. The directory says "test double, discarded in Phase 9" for both. Their paths are not part of any contract.

### 13. The mock daemon's conditions

The mock daemon implements `fixed`, `oracle`, and `random` and exits non-zero on any other condition. `fixed` writes the one-entry schedule and a log with an empty query list, since it consults no recognizer; the telemetry rules produce query points for `oracle` and `random` only. It emits `unmodified` only and has no validator.

### 14. The oracle inside an `ambiguous` segment

At a query point covered by an `ambiguous` segment, the mock oracle writes the query with a null proposal, `fallback` as its validation, and a source naming the off-menu mode it read; the matching schedule entry repeats the boot default with provenance `fallback`. This is the daemon guide's own wording. The mock does not commit to one of the active modes; that decision stays deferred.

### 15. `random`'s draw in the mock

One draw per snapshot from Python's seeded generator over the 32 driver-table rows in sorted `(mode, background_wanted)` order, independent of previous draws and of the telemetry, recorded in the query's source. The real daemon's generator need not match, since the mock is discarded.

### 16. Spawn children in telemetry

Children enter telemetry with their parent and never leave. No coreset task carries both a spawn table and a pinned depart, so this is the only case the mock handles.

### 17. The trivial generator's rule

One unit run per stimulus: at every stimulus instant, meaning a pinned arrival, a pinned wake, a periodic task's tick, and each chain stage's wake in turn, the stimulated task becomes ready, runs for exactly 1 µs, and ends its run. A finite task exits after its first run, a segment-bound task departs at its pinned depart, spawn children arrive with their parent, every periodic job gets a met deadline line, and each schedule entry before the end gets its applied line at its stamped time. The generator models no queue. Its numbers are meaningless by design; the replay covers the checkable values.

### 18. Replay selection

A mock-only flag naming the fixture trace to replay, placed in the command prefix for replay runs. When present the mock copies that trace to the output path after checking its workload id matches the schedule's, refusing a mismatch; when absent it generates.

### 19. Pinning tests

Three tests pin the mocks to things already written down: the mock daemon run over all 50 compiled coreset files reproduces the 8.4 spec's measured graded-set facts, 134 query points with 50 terminal and 2 `ambiguous` skipped, 82 graded over 49 files, 10 carrying `pre_committed_miss`, and a disagreement is investigated with whichever side is wrong corrected, the 8.4 spec amended if it is the spec; `ostep.json` equals the composition of the daemon's config-schema defaults, on the precedent of `compose_row` against the daemon's `compose`; the replay's output is byte-identical to each fixture trace. The generator's test is the records build with no consistency message plus the utilisation and tick-count guards passing on all 50 files.

### 20. Documentation

The new contract goes into `docs/data-contracts.md` as contract 10 after the driver table section, so the later sections renumber by one, with a row in the contract table and a dated changelog entry. The condition vocabulary is referenced from the daemon guide, not restated. The harness README gains rows for the two new directories; the fixtures README is untouched.

## Invariants

- The harness never imports the daemon's or the dataset's modules; where the mocks reproduce their logic, a test pins the two together.
- Everything the mocks emit is contract-valid under the frozen schedule, log, and trace contracts, so nothing above the readers changes.
- Names are written in full: invocation contract, mock daemon, mock simulator, boot default.
