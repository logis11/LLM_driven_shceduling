# Task 8.7 — Per-experiment spec schema, RQ0 gate evaluator, report

The per-experiment spec's schema and lint, the RQ0 gate evaluator that reads a spec and the harness's output files into a verdict, and the machine-readable report with its rendering. Parent: `_dev/TODO.md` (jioh, 8), sub-task 8.7; Phase 8 spec decisions 1 to 8, 12 to 14, and 21. Decided in the 2026-09-11 grill. Taken up before 8.6 so the spec's schema is decided once and the runner consumes it.

## Scope

- The per-experiment spec: a data file with a schema and a lint, and a fixture instance.
- The RQ0 gate evaluator: the generic part shared by every experiment and RQ0's criterion.
- The report: one machine-readable file per experiment run under a schema, and its human-readable rendering.
- The scorer's floors made overridable for the floor-sensitivity line, with the same default.
- A hand-worked `mock-experiment` fixture and tests.
- Doc touches: the harness README and the fixtures README.

Out of scope: the values of K, g, and N and the committed RQ0 gate spec (8.8); the runner (8.6); harness guide chapters and terminology (8.9); the metrics doc, since the gap is RQ0's rule and belongs in the RQ0 gate spec.

## Locked decisions

### 1. The runner reads the spec's generic part

Carried in from the 8.6 grill: the runner takes its run matrix from the per-experiment spec's generic part, so the matrix has one committed source, and a separate, uncommitted machine configuration names the two commands with their version strings and the local directories. The generic fields therefore serve both the evaluator and the runner.

### 2. Format and home

The per-experiment spec is a YAML data file in a new top-level harness directory for experiments, with its JSON schema beside it and a lint under the harness lint target, on the pattern of the scoring spec and the guard spec. 8.7 ships the schema, the lint, and a fixture instance; 8.8 commits the RQ0 gate spec there as the first real instance.

### 3. The generic part

Every experiment names its id, its conditions, its seed count with seeds running from one to that count, its boot defaults as the primary file stem and a list of alternative stems, its driver table, its judging and reporting file lists, its Layer-1 exclusions derived from the `pre_committed_miss` annotation and linted to match, its guard exemptions, its reporting lines, and its pins. The lint checks that every judging file has scoring terms, every listed file exists in the compiled coreset, every condition is one of the seven known names, every exempted guard exists in the guard spec's registry, every criterion and reporting-line type is registered, and every pin matches its file.

### 4. Pins are hashes

Each pin is the SHA-256 of the pinned file's bytes as committed: the scoring spec, the guard spec, the driver table, and the dataset build manifest. The guard spec's version string is carried beside its hash as a human label. The evaluator recomputes the four hashes from the files it is given.

### 5. A pin mismatch is a refusal

A pin that does not match is not a verdict: the evaluator exits non-zero naming the pin and writes no report. The same holds for a judging file missing any run the criterion reads; a report is produced only over a complete run set.

### 6. A typed criterion section

The criterion section carries a type, `k_of_n_gap` for RQ0, and that type's parameters: K, g, the two conditions the gap compares, and the seed statistic. The schema is a discriminated union over the known types and the evaluator keeps a registry with one entry today, so a later experiment adds a type rather than forking the evaluator. The lint refuses an unknown type.

### 7. Reporting lines are typed

The spec's reporting lines are a list of typed entries with parameters, over a registry of line types in the evaluator: the sensitivity counts under the alternative boot defaults, the floor band, accuracy with and without the exclusion, the Layer-1 headline, the `random-beats-oracle` flag, and a note type carrying pre-registered free text bound to a workload, which is how the Phase 7 judging notes and `c1-gaming`'s separate line are declared. The lint refuses an unknown type. The Layer-1 headline reports every graded condition present in the grades file.

### 8. The shape of an exemption

An exemption is an entry naming a guard, a workload, optionally the conditions it covers, and a required non-empty reason. An exempted guard's failure on the matching runs is reported and does not invalidate the verdict.

### 9. Which failures invalidate

Only the runs the criterion reads can invalidate a judging file: the primary-default `fixed` run, the `oracle` run, and every `random` seed. A non-exempt failure on an alternative-default run marks that default's sensitivity count as unavailable and leaves the verdict alone. A failure on a reporting-only file is reported and never invalidates. Under `invalid` the per-file table is still computed and reported.

### 10. The evaluator's inputs and arithmetic

The evaluator reads the spec and the aggregates, scores, guards, and grades files. A file's score under a condition is the scores file's file-level row; `random`'s is the mean over its seeds, with every per-seed value kept; the oracle's is the file's weight sum. A judging file whose every term is no-headroom counts as not meeting g and is marked. The verdict is `pass`, `fail`, or `invalid`.

### 11. The floor-sensitivity line

The scorer gains an optional floors argument defaulting to its constants. The evaluator re-scores the judging files in memory once per floor in the band the spec names and reports the verdict count per floor. The committed scores file stays the one scored at the pinned floor.

### 12. The report

One JSON document per experiment run under its own schema, beside the experiment schema: a header with the spec id, the pins, and the verdict, then sections that are arrays of row objects, each row carrying the fields that locate it, for the per-file gaps, the per-seed scores beside the mean, the guard results, the provenance breakdown taken from the aggregates' provenance shares, and each reporting line. The human-readable rendering is Markdown written by the same invocation to a second path and never edited by hand.

### 13. Fixture

A `mock-experiment` fixture: an experiment spec over the `mock-scores` workload with its `fixed`, `oracle`, two `random` seeds, and the alternative-default `fixed` run; a guards file and a grades file shaped for it; a worked derivation of the per-file gap, the seed mean, the verdict, and each reporting line; and the expected report. Three variants of the spec exercise a pass, a fail, and an `invalid` from a non-exempt guard failure, with one exemption turning the `invalid` back into a verdict.

### 14. Entry points and documentation

An evaluator module in the harness package with an evaluate CLI and an experiment-lint CLI beside the existing ones. The harness README gains rows for the new directory and modules; the fixtures README gains the `mock-experiment` entry.

## Amendments

- *2026-09-12 (sub-task 8.8):* the schema gains an optional `statements` list the evaluator echoes verbatim into the report, per-point `reasons` on the sensitivity line, a `g_band` line (the verdict count recomputed under each gap threshold), and a `seed_standard_error` line (per judging file, the compared condition's sd, standard error, and error as a share of the reference); the report schema gains `statements`. Made in place: the gate had not run.

## Invariants

- Every judgement the evaluator applies is data in the committed spec, never a constant in code.
- Names are written in full: RQ0 gate spec, RQ0 gate evaluator, per-experiment spec, guard spec.
