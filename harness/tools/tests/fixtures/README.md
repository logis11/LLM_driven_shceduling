# Mock fixtures — hand-written traces with hand-computed records

Five mock pairs for the harness's lower half (Phase 5, sub-task 5.1; `mock-switch` added in Phase 6, sub-task 6.1). Each directory holds:

- `run.json` — the run-file view (`workload_id` + `events`), reduced from a coreset file. This is the reader's second input: it supplies `T_end`, the chain topology, and each task's `demand`.
- `trace.jsonl` — the trace a simulator would emit for that run file under the scheduler behaviour stated in `worked.md`. Hand-written, 20–50 lines, every line in the frozen format (`docs/data-contracts.md` §9).
- `expected.csv` — the records the primitives must produce from this pair, byte for byte. Every row was derived by hand in `worked.md`; a script only formatted, sorted, and filled the identity columns.
- `worked.md` — the derivation: what happens at each instant, and how every row follows from the trace lines.
- `config-schedule.json` — only where the pair needs the reader's third input (data-contracts §7): the params of each applied entry, by `index`, for `switch_window`. The lint parses it when present; `build` takes it as `schedule_path`.

| mock | reduced from | exercises |
|---|---|---|
| `mock-office` | `c1-office` | focused editor with two keystrokes queued during one burst (zero-wait `ready` lines inside an occupancy), an unfocused task that never wakes, the `fixed` condition |
| `mock-media` | `c1-media` + a batch distractor | two TIMER tasks, backlog on the video task (instant TIMER completions inside one occupancy, two misses), a same-instant boot + oracle config pair (a zero-length `config_interval`), a batch task that completes |
| `mock-p1a` | `c2-p1a` | editor versus batch, the config switch at set change + latency, two preemptions, a batch task that cannot finish before `T_end` (its exit lies past the window and is clipped) |
| `mock-chain` | the game chain, three stages | frame latency reconstructed from the WAKE topology (ids deliberately not `.chain.N`), one late frame overlapping the next tick, the head's `deadline` lines disagreeing with frame latency by design; FIFO under an oracle entry beside the boot entry |
| `mock-switch` | an editor, a batch task, a third task, under MLFQ → FIFO → MLFQ | `switch_window` in both directions (zero-valued into FIFO; into MLFQ the lane-time window closing when the hog has its `W_single` of CPU, sized from the config schedule), a hog counted by its first preempt, `x_mlfq_level` lines the harness ignores and the check tool reads, the §8 excess aggregates worked by hand; the check tool passes at the window's edge |

## `mock-scores` — hand-written records with expected aggregates and scores (8.2)

Not a trace pair: `records/` holds five hand-written records files for one small workload (`fixed`, `oracle`, `random` × 2 seeds, `fixed` under an alternative `boot_default`), `scoring-spec.yaml` a four-term spec shaped to hit every scorer rule (a windowed P99, a no-headroom miss rate, a progress term, a turnaround censored under one seed), `expected-aggregates.csv` and `expected-scores.csv` the files `tools/score.py` must reproduce byte for byte, and `worked.md` the derivation of every share and score. `seam/` holds hand-written `fixed` and `oracle` records for `mock-p1a`, scored together with the records the writer produces from `mock-p1a`'s trace (the end-to-end seam test).

## Fixed here, documented in the metrics doc (5.2)

- **Row order:** `entity`, then `metric`, then `t` (numeric), then `cause`. Byte comparison needs one order.
- **Anchor `t`** for window-level rows (`cpu_delivered`, `demand`, `preempt_count`, `busy`, and `completed` when its value is 0) is `T_end`. `completed` with value 1 and `turnaround` are anchored at the `task_end` time.
- **`T_end`** is the largest pinned time in the run file: arrivals, departs, and wake events.
- **`demand`** rows exist only for programs whose RUN total is finite. A program with an unbounded LOOP has no `demand` row.
- **Window edges:** a `job` row is emitted only if its completion is at or before `T_end`; a `ready_wait` row only if its `run_start` is. Occupancy still open at `T_end` is clipped there.
- **Identity for mocks:** `sim` is `mock@0`; `source_sha256` is the SHA-256 of `trace.jsonl` as committed, so editing a trace means regenerating the hash.
- **`deadline` lines** in a trace are never the source of a `job` row. They are a cross-check for single-stage TIMER tasks and are expected to disagree for chains.

## Simulator behaviour the mocks assume

These are the assumptions sent to 인경민 (`docs/memos/2026-09-07-trace-clarifications-for-the-simulator.md`) plus the mock-local choices that fill gaps the contracts leave open. If a decision goes differently, the affected mock changes deliberately.

1. A `ready` line is emitted at every completion of a blocking primitive, at zero wait when it did not block. Inside an occupancy it appears after the `run_start` and pairs with wait 0.
2. Wakes queue with depth: two wakes sent to a busy task complete its next two WAITs.
3. TIMER's `t₀` is the task's arrival time (simulator-guide §9.2), so a TIMER task arriving at 0 consumes tick 0 at 0 without blocking.
4. An arriving task whose first instruction blocks is scheduled like any other: it reaches the WAIT and blocks. When the lane is free this is a zero-length occupancy (`run_start` and `run_end` at the same instant).
5. Same-instant order: config entries first, in list order; then arrivals in file order; ready before `run_start` of another task at the same instant is written in the order the scheduler acted.
6. The scheduler in each mock is stated in its `worked.md` (idle lane, FIFO, or MLFQ with a 2 ms slice). Any legal scheduler is acceptable; the primitives never depend on which one produced the trace. Since 2026-09-11 the boot default's slice is 10 ms (OSTEP's example), so `mock-p1a` and `mock-switch` stamp their 2 ms MLFQ by an explicit `unmodified` entry at 600 µs beside the boot entry, the way `mock-media` stamps FIFO beside it; the boot entry's own params govern no occupancy in either mock.
7. MLFQ in a mock follows the simulator guide's five rules and the 2026-09-08 switch memo: a task that consumes a full slice is demoted (with no `run_end` when nobody else is runnable), blocking keeps its level, a fresh slice at every dispatch and boost, a wake into a strictly higher queue preempts at once while a wake into the same or a lower queue waits for the slice boundary. An entry with the same algorithm applies at its stamped time with levels kept (`mock-p1a`); an entry with a different algorithm applies after the running task's current slice (the drain). At an algorithm switch (`mock-switch`): the boost timer restarts at `t_apply`; a switch out of FIFO applies at once with the running task treated as freshly dispatched (metrics doc §11, items 7–9, confirmed with 인경민). `x_mlfq_level` lines are written where the mock's author knows the level changed. The row's `batch_bandwidth_cap` is not modelled by any mock.
