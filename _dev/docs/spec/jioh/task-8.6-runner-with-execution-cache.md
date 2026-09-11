# Task 8.6 — Runner with execution cache

The runner: the per-experiment spec's generic part expanded into a run matrix, every run invoked through the invocation contract with its outputs cached, and the whole pipeline driven from those outputs to the report. Parent: `_dev/TODO.md` (jioh, 8), sub-task 8.6; Phase 8 spec decisions 9, 10, 11, and 12; contract 10 (data-contracts §11, 8.5); the per-experiment spec (8.7). Decided in the 2026-09-11 grill, after 8.7 so the spec it reads already exists.

## Scope

- Matrix expansion from the per-experiment spec's generic part.
- Invocation of the daemon and the simulator through contract 10, with the determinism reruns.
- The execution cache.
- The run directory layout, the run manifests the guards and grade commands read, and the pipeline from records through the RQ0 gate evaluator.
- The uncommitted machine configuration with a committed example.
- A runner command, a make target for the full 50-file smoke run over the compiled coreset with a CI step, and tests that drive the same path on a handful of files.
- Doc touches: the harness README.

Out of scope: the RQ0 gate spec and the alternative boot-default pair (8.8); harness guide chapters and terminology (8.9); any change to the frozen contracts or to the guards.

## Locked decisions

### 1. The runner reads the spec's generic part

The run matrix has one committed source: the per-experiment spec's generic part as 8.7 defined it. A separate, uncommitted machine configuration names each program's command prefix and version string, the compiled build directory, the runs directory, and the cache directory, and carries nothing experiment-shaped; a committed example sits beside it. The trace header's simulator identity is cross-checked against the configured version string, and a mismatch is a failed invocation.

### 2. Every run is executed twice, both programs

The runner executes the simulator twice for every run, since the determinism guard fails any run without a rerun trace, and the daemon twice as well, comparing the schedule and log bytes itself and treating a difference as a failed invocation, since contract 10 makes byte-identical outputs a requirement of both programs. No sampling.

### 3. Traces are uncompressed in this phase

The runner never asks for a gzipped trace, because a gzip header carries a timestamp and both the records' trace hash and the determinism guard hash raw file bytes. The space cost is noted for Phase 9, when the real simulator's trace sizes are known; nothing frozen changes.

### 4. A cache entry holds both executions

The cache is keyed on a hash over the program's version string, its command prefix, the condition and seed, and the content hashes of its input files. One entry per key holds both executions' outputs, the captured stderr logs, and a metadata record, so a hit reproduces the determinism evidence as well as the outputs and a known key is never re-executed. A failed invocation is never cached.

### 5. The matrix

For every listed file: `fixed` under the primary boot default and once under each alternative stem; every other condition in the spec under the primary; a drawing condition once per seed from one to the seed count. The records' table column comes from the pinned driver table's role; seeds are written as the integer's string.

### 6. Run directories and the pipeline

One directory per experiment, per workload, per run, holding the daemon and simulator outputs, their reruns, the stderr logs, and the records file; the aggregates, scores, guards, grades, both manifests, the report, and its rendering sit at the experiment level. The stages run in-process through the library modules, with the records build's guard messages recorded as an explicit list; the manifests are still written as files because the guards and grade commands read them. The grader uses the spec's pinned driver table and its own pinned bootstrap settings. A non-zero exit or a rerun mismatch leaves the run's outputs absent; the runner names the failed runs and stops before scoring. Execution is sequential with no timeouts in this phase.

### 7. The 50-file run is a make target

The routine test suite drives the whole pipeline, runner through report, on a handful of coreset files; the full 50-file run on the mocks is a make target with its own CI step after the suite.

### 8. The smoke spec is generated, never committed

The make target and the suite generate a throwaway experiment spec at run time, computing the pins from the files as they are, listing every coreset file with scoring terms as judging, with a placeholder criterion and no alternative boot defaults, and discard it afterwards. `harness/experiments/` holds pre-registered experiments only.

### 9. Entry points and documentation

One runner command beside the existing ones, the make target, and the CI step. The harness README gains its rows.

## Invariants

- Nothing crosses between the runner and a program except what contract 10 allows: the command line, the files it names, and the exit code.
- Names are written in full: invocation contract, per-experiment spec, RQ0 gate evaluator, boot default.
