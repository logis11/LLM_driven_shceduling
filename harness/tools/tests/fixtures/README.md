# Mock fixtures — hand-written traces with hand-computed records

Four mock pairs for the harness's lower half (Phase 5, sub-task 5.1). Each directory holds:

- `run.json` — the run-file view (`workload_id` + `events`), reduced from a coreset file. This is the reader's second input: it supplies `T_end`, the chain topology, and each task's `demand`.
- `trace.jsonl` — the trace a simulator would emit for that run file under the scheduler behaviour stated in `worked.md`. Hand-written, 20–50 lines, every line in the frozen format (`docs/data-contracts.md` §9).
- `expected.csv` — the records the primitives must produce from this pair, byte for byte. Every row was derived by hand in `worked.md`; a script only formatted, sorted, and filled the identity columns.
- `worked.md` — the derivation: what happens at each instant, and how every row follows from the trace lines.

| mock | reduced from | exercises |
|---|---|---|
| `mock-office` | `c1-office` | focused editor with two keystrokes queued during one burst (zero-wait `ready` lines inside an occupancy), an unfocused task that never wakes, the `fixed` condition |
| `mock-media` | `c1-media` + a batch distractor | two TIMER tasks, backlog on the video task (instant TIMER completions inside one occupancy, two misses), a same-instant boot + oracle config pair (a zero-length `config_interval`), a batch task that completes |
| `mock-p1a` | `c2-p1a` | editor versus batch, the config switch at set change + latency, two preemptions, a batch task that cannot finish before `T_end` (its exit lies past the window and is clipped) |
| `mock-chain` | the game chain, three stages | frame latency reconstructed from the WAKE topology (ids deliberately not `.chain.N`), one late frame overlapping the next tick, the head's `deadline` lines disagreeing with frame latency by design |

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
6. The scheduler in each mock is stated in its `worked.md` (idle lane, FIFO, or MLFQ with a 2 ms slice). Any legal scheduler is acceptable; the primitives never depend on which one produced the trace.
