# Phase 11 — The RQ0 failure procedure: diagnosis

인지오's Phase 11 in `_dev/TODO.md`, decided on 2026-11-18: the RQ0 gate spec's failure procedure (`harness/experiments/rq0-gate.yaml`, statement `failure-procedure`) after the RQ0 run's fail, through the route its configuration search names. Phase 10 ended with the verdict (`docs/rq0-run-record.md`): fail at the primary, 6 of 19 judging files against K = 10, provisional on the re-measurement contingency.

## Scope

- The scorer's reading of a term whose oracle is worse than fixed. The scorer marks a term no headroom only when the oracle's improvement, taken without its sign, is under the aggregate's floor (`harness/tools/harness/scorer.py`; the metrics doc's floor rule, `docs/harness/metrics.md` §9); an oracle worse than fixed past the floor counts as headroom and the term's share changes sign. In the RQ0 run `c7-ml-train`'s gap of 2.512 is that inversion: `random` beats `oracle` there.
- The degraded oracle: the judging files on which the prior driver table's correct row scores worse than the boot default past the floor — every term of `c7-dev`, `c7-video-edit`, `c7-compile` and `c7-ml-train`, and a term of `c1-compile`, `c1-transcode`, `c1-render`, `c2-p3a` and `c1-ml-train`.
- The re-measurement the RQ0 gate spec's statement `re-measurement-contingency` names: the carried-half-width line at its lower bound moved `c7-ml-train` across g.
- The configuration search on the three failing judging files the statement `failure-procedure` picks by rule, and the route it names: no spread found means workload redesign; spread the prior table missed means the table is rewritten.
- The docs the phase changes brought to its end state.

Out of scope: Phase 12 — the route's fix (the table rewrite or the workload redesign), the second RQ0 gate spec pinned before its run, the second RQ0 run and its verdict; the hold-time plan's step 1 (decision 10); the RQ1–RQ4 experiment specs.

## Locked decisions

### 1. The phase is the diagnosis

Phase 11 closes when the route the configuration search names is recorded. The route's fix, the second RQ0 gate spec pinned before its run, and the second RQ0 run with its new verdict are Phase 12; what Phase 12 holds follows from the route.

### 2. The first verdict stands as run

The RQ0 run's verdict is not replaced: fail, 6 of 19, provisional. The run record and the result memo (`docs/memos/2026-11-18-rq0-run-result.md`) gain a dated correction stating the sign inversion, with the reading in which an oracle worse than fixed is no headroom beside it as post hoc — on the RQ0 run's scores, 4 of 19 judging files meet g and 12 of 19 have headroom. The defects are fixed, and the second RQ0 run gives a new verdict.

### 3. The fixed scorer's rule

A term whose oracle is worse than fixed by more than the aggregate's floor reads as no headroom — share 1, as a term under the floor — and carries its own mark, "oracle worse than fixed", on the term and in the report, so the headroom count, the failure procedure's table check and the reader tell the two apart. The rule lands by a harness changelog entry as the phase's first change. Every later reading, the picks and the search among them, reads it, but for decision 6's finding step.

### 4. The degraded oracle is looked at before the search

A sub-task reads the RQ0 run's traces for every judging file whose oracle is worse than fixed past the floor on some term, and classes each case as a defect in a program or a property of the configuration. A defect is fixed before the search, with its version string or changelog entry; a property is data for the search and the table check. The RQ0 run's outputs (`runs/rq0-gate`, `runs/.cache`) stay on disk until this sub-task ends.

### 5. 인지오 fixes the defects

A defect found in the simulator, the daemon, the driver table or the harness is fixed by 인지오, and its owner is told afterwards. Every fix to a program moves its version string.

### 6. The re-measurement as pre-registered

Phase 11 does the re-measurement the statement `re-measurement-contingency` names. The entry whose value moved `c7-ml-train` is found by moving one carried value at a time, re-scored under the scorer as run — the rule the line fired under, stated in its record. It is re-measured at the count the statement fixes, by a harness changelog entry and a second bless. The first verdict's provisional status closes on it.

### 7. The three picks

The configuration search's files are picked by the statement `failure-procedure`'s rule: the failing file with the largest oracle improvement over fixed in the nine-file duplicate-heavy class, the same in the low-duplicate class, and the failing file whose gap fell furthest below g; ties by workload id order; files with no headroom skipped for the first two. The improvement is read as the improvement divided by fixed's value, weighted over a file's terms, under the fixed scorer. The picks are taken after decision 4's sub-task — on the RQ0 run's scores if it fixed no defect that changes the judging files' runs, on the corrected runs if it did. On the RQ0 run's scores they are `c7-transcode`, `c7-gaming` and `c1-transcode`.

### 8. The search is pinned before it runs

Before any search run, the search's sub-task fixes and commits the configurations searched, what counts as spread on a file, what counts as spread the prior table missed, and how the three files' results combine into one route. The values are decided in that sub-task's own spec session.

### 9. Structure of the phase

Five sub-tasks: the scorer's sign rule (11.1); the degraded oracle (11.2); the re-measurement (11.3); the configuration search (11.4); the docs sweep (11.5) — the docs the phase changed, the docs index, the TODO. 11.1 first; 11.2 and 11.3 may run in parallel after it; 11.4 after both, so the search runs on the fixed programs and the re-blessed dataset; 11.5 last.

### 10. The hold-time plan's step 1 moves after Phase 12

The need for a hold rule measured with no rule — the flap-stress set and the C4 files under `oracle` and `random`, the wrong-flip count and its cost (`_dev/docs/plan/jioh/hold-time-and-hysteresis.md`, step 1; its When table numbers it 0) — runs after Phase 12's second RQ0 run, on the table and programs that run uses. The Backlog line is restated to it.
