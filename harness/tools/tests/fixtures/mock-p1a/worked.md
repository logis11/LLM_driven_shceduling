# mock-p1a — worked derivation

Reduced `c2-p1a`: an editor, and a training run arriving at 50 s with more work than the window holds. Condition `llm_vocab` on the prior table, recognition latency 600 µs. Scheduler: an MLFQ with 3 queues, a 2000 µs slice, growth 2, boost 100000, stamped by entry 1 at 600 µs (the recognizer's answer to the t = 0 snapshot, `unmodified`) beside the boot entry, whose own 10 ms slice governs nothing since no task runs before 600 (the boot default is OSTEP's example since 2026-09-11); under the rules of the simulator guide and the 2026-09-08 switch memo — a task that uses up its allotment at a level — the level's slice, counted across its bursts, kept when it blocks or is preempted — is demoted, its allotment starting afresh at the new level, at a boost, and at a slice end in the bottom queue; blocking keeps its level; a wake into a strictly higher queue preempts at once and a wake into the same or a lower queue waits for the slice boundary; entries 1 and 2 change params only, so each applies at its stamped time with queue levels kept (memo §7) and restarts the boost timer (metrics doc §11 item 9). The row's cap is not modelled. All times µs.

Re-derived 2026-10-17 (9.15): `editor`, whose first instruction is a WAIT, blocks in its arrival step, with no `ready` line and no occupancy, as the reference simulator's arrival step does (`simulator/src/sim.cpp`, `on_arrive`; fixtures README, item 4). The earlier derivation scheduled it at 0 for a zero-length occupancy; it ran no work there, so nothing after 0 changes. Re-derived again the same day: the boost at 100000 the derivation showed is gone, since the boost timer restarts at each applied entry and after entry 2 the next boost is 150600, past `T_end`; `hog` was alone on the lane there, so no trace line or row changes.

Re-derived 2026-10-30 (`simulator/memo/memo_261023.md` Part H3): the used allotment is kept across a block or a preemption, OSTEP §8.4's Rule 4 (simulator guide §5, rule 4), in place of a fresh slice at every dispatch. Up to 74000 only the comments change. At 74000 the editor has 2000 left of Q2's 8000, so it is preempted at 76000 and finishes its RUN at 85000; the editor's `preempt_count` becomes 1 and the hog's 3, every other row unchanged. The reference simulator writes these lines, caps null.

## Run file

| task | name | arrive | depart | program | RUN total |
|---|---|---|---|---|---|
| `editor` | `code` | 0 | 120000 | WAIT, RUN 4000, WAIT, RUN 6000, WAIT, RUN 2000, WAIT, RUN 3000, WAIT | 15000 |
| `hog` | `python3` | 50000 | — | RUN 90000, EXIT | 90000 |

Keystrokes on `input:editor`: 8000, 30000, 54500, 71000. `T_end` = 120000. The hog needs 90000 in a window of 70000: it cannot finish, as in the real file.

## What happens

| t | event |
|---|---|
| 0 | boot config (index 0, `fallback`, 10 ms slice). `editor` arrives in Q0 and executes its first instruction, a WAIT, in its arrival step: it blocks there, with no `ready` line and no occupancy. Set change → the recognizer is consulted. |
| 600 | entry 1 (`unmodified`, MLFQ, 2000 µs slice) applies: same algorithm, levels kept, the boost timer restarted (next boost 100600); the lane is idle. |
| 8000 | keystroke 1; lane free; RUN 4000: the Q0 allotment (2000) is used up at 10000 → demoted to Q1, no competitor so no `run_end`; blocks at 12000, stays Q1 having used 2000 of its 4000. |
| 30000 | keystroke 2; RUN 6000: the Q1 allotment's last 2000 is used up at 32000 → demoted to Q2; blocks at 36000, stays Q2 having used 4000 of its 8000. |
| 50000 | `hog` arrives in Q0, lane free, runs. Set change → the recognizer is consulted. |
| 50600 | entry 2 (`unmodified`, MLFQ with the row's cap) applies at its stamped time: same algorithm, levels kept, `hog` finishes its granted slice; the boost timer restarted (next boost 150600, past `T_end`). |
| 52000 | `hog`'s Q0 slice consumed → Q1, slice 4000. |
| 54500 | keystroke 3; `editor` is Q2, `hog` is Q1 → no preemption. `editor` waits. |
| 56000 | `hog`'s Q1 allotment used up → Q2, to the back; `editor` (Q2, ready 54500) runs: preempt. RUN 2000 → blocks at 58000, 6000 of Q2's 8000 used. |
| 58000 | `hog` resumes in Q2, slice 8000: boundaries 66000, 74000. |
| 71000 | keystroke 4; both Q2 → no preemption. `editor` waits. |
| 74000 | `hog`'s slice boundary: to the back with a fresh slice, `editor` runs (preempt). RUN 3000, with 2000 of its Q2 allotment left. |
| 76000 | `editor`'s Q2 allotment used up in the bottom queue: a fresh slice, to the back behind `hog`, which runs (preempt). |
| 84000 | `hog`'s slice boundary: to the back, `editor` runs (preempt) its last 1000 → blocks at 85000. `hog` resumes. |
| 120000 | `T_end`. `editor` departs. `hog` still holds the lane. |
| 145000 | `hog` exits (past the window; the trace records it, the harness ignores it). |

## Rows

**`ready_wait`**

| ready | pairs with | value |
|---|---|---|
| `editor` 8000 `wake` | `run_start` 8000 | 0 |
| `editor` 30000 `wake` | `run_start` 30000 | 0 |
| `hog` 50000 `arrive` | `run_start` 50000 | 0 |
| `editor` 54500 `wake` | `run_start` 56000 | 1500 |
| `editor` 71000 `wake` | `run_start` 74000 | 3000 |

**`input_latency`** — one per keystroke at its wake event, value = the start of the service of the WAIT it completes − its wake time (metrics doc §6.12; added 2026-10-30). No keystroke queues, so each equals its `ready_wait`: 8000 → 0, 30000 → 0, 54500 → 1500, 71000 → 3000, each `censored` 0.

**Lifetime**

| task | `arrival` | occupancy (clipped) | `cpu_delivered` | `demand` | `completed` | `preempt_count` |
|---|---|---|---|---|---|---|
| `editor` | 0 | [8000,12000] [30000,36000] [56000,58000] [74000,76000] [84000,85000] | 15000 | 15000 | 0 (`depart`) | 1 |
| `hog` | 50000 | [50000,56000] [58000,74000] [76000,84000] [85000,120000 clip] | 6000 + 16000 + 8000 + 35000 = 65000 | 90000 | 0 (`exit` at 145000 is past `T_end`) | 3 |

No `turnaround` rows. Progress for the hog, computed later by scoring: 65000 / 90000.

**`config_interval`**

| index | applied | until | value |
|---|---|---|---|
| 0 (`fallback`, MLFQ) | 0 | 600 | 600 |
| 1 (`unmodified`, MLFQ) | 600 | 50600 | 50000 |
| 2 (`unmodified`, MLFQ) | 50600 | 120000 | 69400 |

**`busy`** — 15000 + 65000 = 80000.

No `switch_window` row: entries 1 and 2 change params, not the algorithm.

Total 23 rows.
