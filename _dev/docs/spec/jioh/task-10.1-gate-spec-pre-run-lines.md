# Task 10.1 — The RQ0 gate spec's pre-run lines

Sub-task 10.1 of Phase 10 (`_dev/docs/spec/jioh/phase-10-integration-and-the-rq0-run.md`, decision 6), decided on 2026-11-01: the two lines the RQ0 gate spec (`harness/experiments/rq0-gate.yaml`) still owes before the RQ0 run — a falsification condition for link 2 of the research-claims chain and a cap band reporting line — with one harness changelog entry and one re-pin.

## Scope

- A reporting line in the RQ0 gate spec that reads link 2 of `docs/research-claims.md`'s chain (some of the differences where the correct config differs are invisible to behavioural observation), and the spec naming which of its readings tests link 1 and which link 2.
- A cap band reporting line: the verdict count beside the primary under other `batch_bandwidth_cap` values, with the driver tables it reads.
- The harness code the two line types need — their schema branches, evaluation and rendering, the runner's table axis for the cap band — with their tests.
- `docs/research-claims.md`, the harness guide's reporting-line table (`docs/harness/harness-and-records-guide.md` §19.4) and `harness/experiments/README.md`'s list of line types, changed in the same commits.
- One `harness/CHANGELOG.md` entry and one re-pin of the RQ0 gate spec.

Out of scope: the cost response to the runs the cap band adds (10.3); any change to the primary driver table's rows or to the wanted rows' cap values.

## Locked decisions

### 1. Link 2's falsification condition is existential over the judging set

A difference invisible to behavioural observation is, in RQ0's terms, headroom: the oracle condition improving on `fixed`, the boot default that schedules by behaviour alone, on a term the scoring spec already defines. Link 2 is falsified when no judging file has headroom — `fixed` reaching the oracle's outcome on every term of every judging file — and stands otherwise. The line prints the number of judging files with headroom under the primary and link 2's state. It is read apart from the K-of-N criterion's gap: a file whose headroom `random` captures fails link 1's reading and not link 2's.

### 2. The RQ0 gate spec names the link each reading tests

The K-of-N criterion reads link 1; the line of decision 1 reads link 2.

### 3. `docs/research-claims.md` changes with the spec

The sentence stating that link 2 has no falsification condition is restated to the condition of decision 1 and where it is read; the sentence on link 1 and RQ0 states the two readings side by side. Same commit as the spec's line.

### 4. The cap band moves the unwanted rows' floor only

Three driver tables, each the primary `daemon/driver-table/prior.yaml` with every unwanted row's cap — the schema floor 0.05 — replaced by one of the wanted rows' values, 0.2, 0.333 and 0.5; the wanted rows unchanged, every row's justification unchanged. The line reads how far the verdict rests on the floor's harshness; at 0.5 most unwanted rows share their wanted counterpart's cap, the band's end.

### 5. The cap band's runs: the oracle and random conditions re-run under each table, at the same N, on the judging files

`fixed` reads no driver table and is shared. Under each of the three tables the oracle condition and the random condition's N seeds are re-run on the judging files only, N the run's own (the `n-grounding` statement's rule for the sensitivity lines); if 10.3 changes N by a changelog entry, this line follows it. The `n-grounding` statement's multiple of the main judging run is restated to the new total.

### 6. The three tables are committed files, each pinned

The three tables are committed beside `prior.yaml`; the cap band line names each as the boot-default sweep names its alternatives, and the spec's pins block carries their SHA-256. The runner and the daemon take a table path and nothing else changes.

### 7. The reading rule is the existing one

The `sensitivity-lines` statement's rule — a verdict count that moves under any line makes the verdict a range over that axis — applies to the cap band without a rule of its own.

### 8. The harness guide and the experiments README change with the spec

The harness guide's reporting-line table gains the two lines' rows; `harness/experiments/README.md`'s list of line types gains the two types. Same commits as the spec.

### 9. One changelog entry, one re-pin

The two lines, the three tables' pins and the `n-grounding` restatement land under one `harness/CHANGELOG.md` entry and one re-pin of the RQ0 gate spec (Phase 10 spec, decision 6).

## Invariants

- The RQ0 gate spec's pinned inputs are committed files; the cap band adds files, not run-time derivation.
- Nothing in the run changes after execution begins except by a harness changelog entry made before any run; this sub-task's entry precedes 10.3 and the run.

## Open items

The design of the two line types in the evaluator and of the runner's table axis is the implementation's.
