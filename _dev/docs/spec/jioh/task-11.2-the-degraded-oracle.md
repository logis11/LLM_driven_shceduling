# 11.2 — The degraded oracle

Sub-task 11.2 of 인지오's Phase 11 (`_dev/docs/spec/jioh/phase-11-rq0-failure-procedure-diagnosis.md`, decisions 4, 5 and 7), decided on 2026-11-19: the cases in which the prior driver table's correct row scores worse than fixed by the floor or more, each classed as a program defect or a property of the configuration, the defects fixed, and the criterion's runs rerun on the fixed programs before the configuration search takes its picks.

## Scope

- The RQ0 run's traces for the cases of decision 2, read under the scorer with 11.1's sign rule.
- Each case classed by decision 1, with the evidence of decision 3.
- Each defect fixed by 인지오, its program's version string or changelog entry moved, its owner told afterwards (Phase 11 spec, decision 5).
- The rerun of the criterion's runs on the fixed programs, and the cases it brings (decisions 6 and 7).
- The record (decision 8) and the RQ0 run's outputs on disk at the end (decision 9).

## Locked decisions

### 1. The classification rule

A case is a **defect** when the trace departs from a written reference: the simulator breaks its contract or one of the ten behaviours, (a) to (j), the RQ0 gate spec's `simulator-conformance` statement lists; the daemon applies something other than the row; a row breaks the driver table's stated rules (`daemon/driver-table/prior.yaml`'s header); or the harness computes something other than the metrics doc defines. A case is a **property** when every program follows its reference and the correct row's configuration is worse. A case is **unexplained** until it is shown to be one of the two.

### 2. The cases

A case is a judging file's term whose oracle is worse than fixed by the floor or more. The cases are those at the primary boot default under the primary table, read there, and those found only at other combinations, each read at the combination where the oracle is furthest behind fixed, relative to fixed's value, among the combinations a line of the report reads — a boot default of the sweep under the primary table, or a cap band table at the primary boot default. The 100 ms boot default is excluded.

At the primary, nine:

| file | term |
|---|---|
| `c1-compile` | editor, input latency P99 |
| `c1-ml-train` | hog, turnaround |
| `c1-render` | bulk, turnaround |
| `c1-transcode` | batch, turnaround |
| `c2-p3a` | bulk, turnaround |
| `c7-compile` | editor, input latency P99 |
| `c7-dev` | editor, input latency P99 |
| `c7-ml-train` | editor, input latency P99 |
| `c7-video-edit` | editor, app latency P99 |

Elsewhere only, six:

| file | term | read at |
|---|---|---|
| `c1-transcode` | video-editor, app latency P99 | the 12 ms boot default, the primary table |
| `c2-p1a` | editor, input latency P99 | the 7 ms boot default, the primary table |
| `c2-p3a` | editor, app latency P99 | the 7 ms boot default, the primary table |
| `c7-photo` | photo-editor, app latency P99 | the 30 ms boot default, the primary table |
| `c7-render` | editor, app latency P99 | the 7 ms boot default, the primary table |
| `c7-transcode` | video-editor, app latency P99 | the primary boot default, the floor-0.333 table |

`c2-p1a`'s hog progress is oracle worse than fixed only under the 100 ms boot default, and `c7-office`'s writer input latency P99 only at combinations no line reads; neither is a case.

### 3. The evidence

A defect: the trace lines that show the departure, and a hand fixture that reproduces it, failing before the fix and passing after. A property: the mechanism traced, every program's lines on its path checked against their references, and one counterfactual run — the oracle on the case's own file with the named knob of the correct row moved — in which the term moves as predicted (decision 4). Without that, the case is unexplained.

### 4. The counterfactual's prediction

Before each counterfactual run, the case table records the knob, its new value and the direction the term will move. The term must move that way by at least its aggregate's floor: 1 ms for P99 and turnaround, 0.01 for miss rate and progress (`docs/harness/metrics.md` §10, its constants).

### 5. Closure

11.2 closes only when every case is a defect or a property. Unexplained is a working state only.

### 6. The rerun

After the last defect fix, the criterion's 1,938 runs — the 19 judging files, each under fixed, oracle and 100 random seeds, at the primary — are rerun once on the fixed programs. A judging file's runs change when any trace hash or records hash differs from the RQ0 run's hash manifest (`harness/experiments/rq0-gate/runs.sha256.csv`). The picks are taken from the rerun's scores under the fixed scorer.

### 7. New and vanished cases

A term the rerun shows oracle worse than fixed by the floor or more at the primary, not among decision 2's cases, joins the case table and is classed by the same rule and evidence. A defect among them is fixed and the criterion's runs are rerun again. 11.2 closes when a rerun shows no unclassified case. A case of decision 2 the rerun no longer shows is recorded against the fix that removed it.

### 8. The record

`_dev/research/jioh/task-11.2-the-degraded-oracle/` holds the case table — one row per case: the file, the term, the combination, the class, the evidence and the fixing commit — with the trace readings, the fixtures' outputs, the counterfactual runs and the reruns' hash comparisons. Each fix is recorded where its program records changes: the harness changelog (`harness/CHANGELOG.md`); the simulator's steps and its version string; the daemon's version string; the RQ0 gate spec re-pinned. If any case is a defect, the RQ0 run record (`docs/rq0-run-record.md`) gains a dated correction under "Corrections". One dated memo goes to the owners whose programs had a fix, after the fixes land.

### 9. The RQ0 run's outputs at the end

At 11.2's end the RQ0 run's traces and `runs/.cache` are deleted. `runs/rq0-gate/aggregates.csv` and `runs/rq0-gate/scores.csv` stay until Phase 12's second RQ0 run. What 11.3 reads stays until 11.3 ends.
