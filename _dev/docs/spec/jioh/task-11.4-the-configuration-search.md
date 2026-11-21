# 11.4 — The configuration search

Sub-task 11.4 of 인지오's Phase 11 (`_dev/docs/spec/jioh/phase-11-rq0-failure-procedure-diagnosis.md`, decisions 7 and 8), decided on 2026-11-21: the configuration search the RQ0 gate spec's statement `failure-procedure` names (`harness/experiments/rq0-gate.yaml`) — the files searched, the configurations searched, what counts as spread on a file, what counts as spread the prior driver table missed, how the files combine into one route, the tool, and the record.

## Scope

- The files: the three picks and the judging files with no headroom on every term (decisions 1 and 2).
- The reading of a searched configuration and the three findings a file can have (decisions 3 to 6).
- The route (decision 7).
- The grid and which of its points are read (decisions 8 to 11).
- The re-reading under the other boot defaults (decision 12).
- The tool and the search spec (decision 13).
- The record and what stays on disk (decisions 14 and 15).

Amendment to the Phase 11 spec's scope, which names the search on the three picked files: the search also runs on the seven judging files of decision 2.

## Locked decisions

### 1. The three picks

The picks are taken on the corrected runs: 11.2's rerun of the criterion's runs on the fixed simulator (`runs/rq0-gate-rerun`) for sixteen judging files, and 11.3's runs on the current programs (`runs/rq0-gate-11-3-current`) for the three files rebuilt on the second bless (`c2-p1a`, `c1-ml-train`, `c7-ml-train`). On them 4 of 19 judging files meet g = 0.5 and 15 fail.

| pick rule (statement `failure-procedure`) | file | oracle improvement over fixed, as a fraction of fixed's value | gap |
|---|---|---|---|
| the failing file with headroom and the largest oracle improvement in the nine-file duplicate-heavy class | `c7-transcode` | 0.865 | 0.123 |
| the same in the low-duplicate class | `c7-gaming` | 1.000 | 0.427 |
| the failing file whose gap fell furthest below g | `c1-transcode` | — | −2.011 |

A term whose oracle is worse than fixed counted at zero or at its signed value gives the same three picks. They are the picks the Phase 11 spec's decision 7 names on the RQ0 run's scores.

### 2. The seven files of the statement's fourth item

The statement `failure-procedure` ends: a judging file with no headroom on every term is an additional trigger for the table check. On the corrected runs seven judging files are in that state:

| kind | files |
|---|---|
| the row worse than the boot default by the floor or more on a term | `c7-dev`, `c7-video-edit`, `c7-compile`, `c1-render` (its turnaround term; its latency term equal) |
| the row changing nothing past the floor | `c7-photo`, `c7-ml-train`, `c7-render` |

The search runs the same grid on all seven and reads each under the same three findings as the picks. The search's files are these ten.

### 3. A point

A point of the search is one configuration applied where the oracle applies its row, the labels ignored (`_dev/docs/rq0-preparation-notes.md` §4.3: ignore labels, sweep the configuration space, observe the spread).

### 4. The quantity a point is read in

Per file, a point's quantity is, per scored term, its improvement over fixed divided by fixed's value — signed, zero when the improvement is under the term's floor — weighted over the file's terms by the scoring spec's weights (`harness/scoring/scoring-spec.yaml`). It is the quantity the Phase 11 spec's decision 7 ranks the picks by. Fixed is the file's run under the primary boot default. Every term's raw value and its reading against the floor are recorded beside the quantity.

The floors are the metrics doc's (`docs/harness/metrics.md` §10): 1,000 µs for latency-type aggregates, turnaround among them, and 0.01 for fraction-type aggregates.

### 5. The three findings

Over a file's read points (decision 9):

- **Finding 1 — no spread.** No two points differ on a scored term by the term's floor or more. The floor is the value below which a difference between two configurations is not read (metrics doc §10).
- **Finding 3 — spread the prior table missed.** The row's quantity is at most (1 − g) of the quantity of the best point, g = 0.5, and the best point is better than the row on a scored term by the floor or more. The row is the configuration the oracle applies; the best point is the read point with the highest quantity. g is the gate's stated minimum effect of interest (statement `g-grounding`: recognition accounts for at least half of the achievable improvement); read on the table, the row captures at most half of the improvement the best point reaches over fixed. No source grounds a value.
- **Finding 2 — spread the prior table's row holds.** Neither of the two.

### 6. The g band

Each file's finding is printed under g at 0.25, 0.33, 0.5 and 0.67, the gate's g band, beside the primary 0.5. A finding that changes inside the band is reported as a range over g.

### 7. The route

- A file at finding 1 or finding 2 points to workload redesign. For a file at finding 2 the record states how many of the prior table's 8 distinct configurations have a quantity at least the row's.
- A file at finding 3 points to the table rewrite.
- The route is one: the table is rewritten if any of the ten files is at finding 3; otherwise workload redesign.

This rule is fixed after the RQ0 run's data were seen. On the runs on disk the four files of decision 2's first kind are at finding 3 before any search run — the boot default is a point of the grid and their row is worse than it by the floor or more — so the route is known before the search: the table is rewritten. On `c7-gaming` the row reaches a frame miss rate of 0 against fixed's 1, so no point can beat it; on `c7-transcode` the row's quantity is 0.865; on `c1-transcode` the row's quantity is 0.005, and 62 of the file's 100 `random` runs exceed it by more than 0.01, the best at 0.153. The search runs as the statement `failure-procedure` requires, and its per-file findings are what Phase 12 is designed from.

### 8. The grid

Algorithm, cap, slice and MLFQ's boost interval are crossed. MLFQ's queue count and slice growth are moved one at a time, at the boot slice and boost interval, under each cap. LOTTERY's batch share follows the cap.

| knob | values | grounding |
|---|---|---|
| algorithm | MLFQ, EDF, LOTTERY, FIFO | the menu (`docs/recognition-vocabulary.md` §2) |
| batch bandwidth cap | none, 0.05, 0.2, 0.333, 0.5, 0.95 | none the boot default; 0.05 and 0.95 the schema's bounds; 0.2, 0.333 and 0.5 the prior table's wanted-row values (statement `cap-band`) |
| slice — MLFQ's top slice, EDF's residual slice, LOTTERY's slice | 0.5, 0.7, 1.2, 2, 5, 7, 10, 12, 20, 30, 100 ms | 10 ms the boot default; the other ten the gate's boot-default sweep (statement `boot-default-sweep`) |
| MLFQ boost interval | 10 ms, 100 ms, 1 s, 10 s | the schema's bounds; 100 ms the boot default (OSTEP Figure 8.4); 1 s the Solaris Time-Sharing class raising every process's priority once a second (the Arpaci-Dusseau handout's entry in `docs/references.md`) |
| MLFQ queue count | 2, 3, 8 | the schema's bounds and the boot default |
| MLFQ slice growth | 1, 2, 8 | the schema's bounds and the boot default |
| LOTTERY batch share | equal to the cap; 0.9 under cap 0.95; under no cap 0.05, 0.2, 0.333, 0.5 and 0.9 | the prior table's rule that a LOTTERY row's share equals its cap; 0.9 the schema's maximum |

470 configurations: MLFQ 288, LOTTERY 110, EDF 66, FIFO 6. On the RQ0 run's measured run times, about 12 CPU-hours for the three picks and about 3.5 for the seven files.

The cap and the slice are crossed on 11.2's trace of the cap reaching a task only while it is in the batch class, which a task enters after one full slice of CPU since its last voluntary block (`_dev/research/jioh/task-11.2-the-degraded-oracle/cases.md`, the `c7-dev` case); the slice and the boost interval on the demotion rule, a task demoted when its CPU within a boost interval reaches the slice (statement `boot-default-sweep`). The record states that queue count and slice growth were not crossed.

The grid holds the boot default and each of the prior table's 8 distinct configurations.

### 9. The points read

A point whose run fails a guard, or holds a wait over 30 s that `simulator/tools/wait_check.py` finds, is out of every reading — not a candidate for the best point, not counted toward spread — and is listed in the record with what it failed. It is the gate's rule: a failed guard on a run makes the gap that reads it unavailable (statement `sensitivity-lines`).

### 10. The two checks

Before the grid is read, on each file: the boot default's point reproduces the file's fixed run, and the row's point reproduces its oracle run.

### 11. LOTTERY's draw

The simulator seeds the lottery from the workload's id, so a LOTTERY point has one draw sequence per file. Each point is run once, under the file's own id. The record flags any finding that would change with the LOTTERY points removed.

### 12. The other boot defaults

The search runs at the primary alone: the blessed files, fixed at the primary boot default. Each of the gate's ten alternative boot defaults is a point of the grid — MLFQ with no cap at that slice — so each file's finding is recomputed with that point in place of fixed and printed beside the primary. A finding that changes is reported as a range over the boot default. The record states the limit: no variant file was searched.

### 13. The tool and the search spec

The search is a harness tool that reads a committed search spec, a data file as the RQ0 gate spec is. The search spec holds the ten files, the grid, the two lines — g with its band, and the floors — the rule of decision 9, and the pins: the simulator's version and the hashes of the dataset manifest, the prior table, the scoring spec and the guard spec. The tool runs what the file says; its report carries the file's hash. The tool lands with a harness changelog entry (`harness/CHANGELOG.md`).

For 11.4 the tool runs the grid, applies decision 9, and writes the per-file findings and the route.

### 14. The record

11.4 writes:

- the tool's report, committed beside the search spec — per file: the finding at the primary, under the g band and under each boot default; the best point; for a file at finding 2, the count of decision 7; the points decision 9 leaves out; decision 11's flag — and the route;
- a dated entry in `docs/rq0-run-record.md`: the failure procedure's result, the per-file findings and the route;
- a new dated memo to the team in `docs/memos/`;
- the sub-task's research folder, with its README and the scripts that read the results.

Every other doc the search touches, the docs index and the guidebook among them, is 11.5's.

### 15. On disk

At 11.4's end the search's traces are deleted, and with them 11.3's runs on the current programs, which its spec keeps whole until 11.4 ends. The aggregates, the scores and the report are kept. Every run is reproducible from the search spec on the pinned simulator.

## Invariants

- The search spec is committed before any search run (Phase 11 spec, decision 8).
- A check of decision 10 that does not reproduce its run stops the search; the search does not proceed past a mismatch.
- The runs are on the fixed simulator, `simulator@841dc81131cb`, the re-blessed dataset and the pinned prior table.
- The search is read-only: nothing it finds is written into a table (`_dev/docs/rq0-preparation-notes.md` §4.3).
