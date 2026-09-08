# Phase 5 — Primitive metrics and the records pipeline

Stages 1–2 of `_dev/docs/rq0-preparation-notes.md`, as decided in the 2026-09-07 spec session. Parent: `_dev/TODO.md`, (jioh, 5). Work lands on `jioh/primitive-metrics`.

## Scope

- Define every metric the project measures — the primitives computed from traces, the primitives computed from recognition logs, and the aggregates the research reads off them — in one normative metrics doc.
- Fix the `records` format: the raw-observation file the primitives produce and scoring consumes.
- Hand-write mock traces with hand-computed expected records; they exercise the definitions and test the code.
- Build the harness's lower half — trace reader, primitives, records output — checked against the hand-computed values. No simulator needed.
- Correct the documents that defer to this freeze.

Out of scope: the scorer, guards, and the grader code (Phase 7); per-file weights (Phase 6); the daemon-side instrument for run-to-run consistency.

## Locked decisions

### 1. Vocabulary

Layer 1 and Layer 2 keep the meaning in `terminology.md`: recognition accuracy and consumer performance. The pipeline split in the preparation notes is named **primitives** (what lands in `records`) and **scoring** (what the scoring spec does). The phase title uses this wording.

### 2. One metrics doc, both families

A single normative doc with a changelog section opens the Harness section of `docs/`. It defines the trace primitives, the recognition primitives, the fixed aggregate list, the normalisation rule, and the constants. Recognition metrics are aggregates over per-query primitives. The grader that implements the recognition definitions is Phase 7's.

### 3. Records are raw observations

`records` holds one row per observation with an anchor time `t`; no aggregate is stored. Aggregation is scoring's, computed from records, never from traces. Changing a primitive means recomputation from traces; changing an aggregate does not.

### 4. Records schema

CSV, one file per trace, every row self-contained. Identity columns: `workload_id`, `condition`, `table` (prior or calibrated; empty for `fixed`), `seed`, `sim`, `source_sha256` (the trace or log the row came from). Observation columns: `entity`, `metric`, `t`, `value`. Nullable attribute columns, filled per metric: `cause`, `provenance`, `algorithm`, `index`, `period_us`, `predicted`, `truth`, `validation`, and `familiarity` (recognition rows: the covering segment's tier, carried through compilation into `ground_truth` — decided after the grill, 5.2). Entities are task ids from the trace plus the reserved names `lane`, `schedule`, and `recognizer`; the reader refuses a trace whose task id collides with a reserved name. The schema is described in the doc and enforced by a machine schema beside the harness code; it is not a data contract.

### 5. Observation window

Every primitive is measured over `[0, T_end]`, `T_end` being the workload's end read from the run file. Observations anchored after `T_end` are dropped and CPU accounting is clipped there. A task alive at `T_end` is "not completed within the window". Whether the simulator runs past `T_end` never affects a number.

### 6. `ready_wait`

One row per `ready` line: `t` = the ready time, value = the wait until that task's next `run_start`, or zero when the `ready` falls inside the task's own occupancy, `cause` carried on the row. Interaction latency, response time, timer dispatch delay, and starvation are filters and aggregates over it: interaction latency is `cause=wake` on the task scoring names; starvation is a task's maximum `ready_wait` over the window, measured from `ready`, never from arrival.

### 7. Periodic jobs and chain frames

Job k of a TIMER task starts when tick k is consumed and completes when the task next reaches a TIMER; `due` = tick k + period. For a chain — the WAKE path starting at a TIMER-headed task, taken from the run file's WAKE targets — frame k completes when the tail stage ends its k-th iteration. One `job` row per tick: `t` = the tick, value = completion − tick, `period_us` on the row; a miss is value > `period_us`. The harness builds these from `ready` and run lines plus the chain topology, one code path for single-stage tasks and chains alike; the simulator's `deadline` lines serve as a cross-check, and the harness guards that the tail's iteration count equals the head's tick count.

### 8. Task lifetime primitives

Per task: `cpu_delivered` (sum of run intervals, clipped at `T_end`), `completed` (a `task_end` with reason `exit` inside the window, at its time), `turnaround` when completed, `demand` (the task's total RUN work, read from the run file), and `preempt_count` (from `run_end` with reason `preempt`). Progress is scoring's ratio of `cpu_delivered` to `demand`.

### 9. Bookkeeping primitives

`config_interval` under entity `schedule`: one row per `config_applied` line, `t` = applied time, value = time in force until the next entry or `T_end`, with `provenance`, `algorithm`, `index`. `busy` under entity `lane`: the sum of all run intervals in the window; idle is `T_end − busy`. Provenance shares, config age, and utilisation are aggregates over these rows. Determinism stays a hash comparison on trace files.

### 10. Recognition primitives

One set of rows per graded query — a non-`ambiguous` segment covers its `t_set_change`; the terminal snapshot is skipped — under entity `recognizer`, `t` = `t_set_change`: `mode_correct` and `attr_correct` (0/1, with `predicted` and `truth`), `latency_us`, `validation`, and for `llm_algo` only `algo_choice_correct`, the named algorithm against the calibrated table's default for the true row. Mode and attribute accuracy, the confusion matrices, and latency to correct output are aggregates.

### 11. Aggregates

A fixed list per primitive, named in the doc. `ready_wait`: count, mean, P50, P95, P99, max, and `over_threshold`, the fraction above a named interaction-latency constant. `job`: count, miss rate, latency P50 and P99. Lifetime and bookkeeping rows: the derived shares and the progress fraction. Mean is never a headline.

### 12. Normalisation

`(fixed − condition) / (fixed − oracle)` is applied per aggregate, so each becomes a unit-free share of headroom before any weighting. Each aggregate has an absolute floor in its own units, stated beside its definition; when `fixed − oracle` is below the floor the ratio is undefined for that file and aggregate, and raw values are reported with "no headroom". Negative values are shown, never clipped.

### 13. Constants

The interaction-latency threshold and the floors are set in the sub-task, each cited from a primary source read in session or written as a stated assumption. No unverified citation.

### 14. Mock traces

Four mock pairs, each a reduced run file and its trace of twenty to forty lines, with a hand-computed expected records file: a reduced `c1-office` (focused editor, one keystroke queued mid-burst, an unfocused task that never wakes); `c1-media` (two TIMER tasks, one in backlog); `c2-p1a` (editor versus batch, the config switch at 60 s plus latency, the batch unfinished at `T_end`); a reduced chain (three stages, one late frame). The simulator assumptions the mocks encode are listed in one place in the doc.

### 15. Simulator assumptions carried

The harness assumes: wakes queue with depth, so iteration k of every chain stage is tick k; every completion of a blocking primitive emits a `ready` line, at zero wait when it did not block; a written tie-break order at shared instants. These go to 인경민 as a proposed clarification of the trace contract, not a format change.

### 16. Documents corrected

`data-contracts` §9: the two definitions it defers point at the metrics doc; the `deadline` example names the chain head; changelog line. `docs/README.md` gains the Harness doc. `terminology` carries the primitives/scoring wording.

### 17. Harness tree

`harness/` mirrors the daemon and dataset trees: Python package, Makefile with lint and test, pinned requirements, tests with the mock pairs and expected files as fixtures, a CI workflow. The reader streams plain and gzipped traces, validates the closed event set, ignores `x_` lines, captures the `meta` header, and takes the run file as its second input. Primitives are pure functions over what the reader yields. Pandas is not a dependency of this phase.

## Open items

- The three-signature line in proposal §8.2 for metric definitions versus 인지오 deciding: settled with the team, not here.
- Whether the dataset carries a familiarity tag per file or per name; checked before the familiarity split is defined.
- Run-to-run consistency needs several samples per query point and the log envelope has no repeat index. Note for 박이안.
- The C1-derived files' inherited demand class (Phase 3 archive) remains undecided.
