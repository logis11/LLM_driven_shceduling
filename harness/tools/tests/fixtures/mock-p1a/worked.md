# mock-p1a — worked derivation

Reduced `c2-p1a`: an editor, and a training run arriving at 50 s with more work than the window holds. Condition `llm_vocab` on the prior table, recognition latency 600 µs. Scheduler: the boot MLFQ (3 queues, 2000 µs slice, growth 2, boost 100000) under the rules of the simulator guide and the 2026-09-08 switch memo — a task that consumes a full slice is demoted, blocking keeps its level, a fresh slice at every dispatch, a wake into a strictly higher queue preempts at once and a wake into the same or a lower queue waits for the slice boundary; entry 1 changes params only, so it applies at its stamped time with queue levels kept (memo §7). The row's cap is not modelled. All times µs.

## Run file

| task | name | arrive | depart | program | RUN total |
|---|---|---|---|---|---|
| `editor` | `code` | 0 | 120000 | WAIT, RUN 4000, WAIT, RUN 6000, WAIT, RUN 2000, WAIT, RUN 3000, WAIT | 15000 |
| `hog` | `python3` | 50000 | — | RUN 90000, EXIT | 90000 |

Keystrokes on `input:editor`: 8000, 30000, 54500, 71000. `T_end` = 120000. The hog needs 90000 in a window of 70000: it cannot finish, as in the real file.

## What happens

| t | event |
|---|---|
| 0 | boot config (index 0, `fallback`). `editor` arrives in Q0, reaches WAIT, blocks (zero-length occupancy). |
| 8000 | keystroke 1; lane free; RUN 4000: the Q0 slice (2000) is consumed at 10000 → demoted to Q1; blocks at 12000, stays Q1. |
| 30000 | keystroke 2; RUN 6000: the Q1 slice (4000) is consumed at 34000 → demoted to Q2; blocks at 36000, stays Q2. |
| 50000 | `hog` arrives in Q0, lane free, runs. Set change → the recognizer is consulted. |
| 50600 | entry 1 (`unmodified`, MLFQ with the row's cap) applies at its stamped time: same algorithm, levels kept, `hog` finishes its granted slice. |
| 52000 | `hog`'s Q0 slice consumed → Q1, slice 4000. |
| 54500 | keystroke 3; `editor` is Q2, `hog` is Q1 → no preemption. `editor` waits. |
| 56000 | `hog`'s Q1 slice consumed → Q2, to the back; `editor` (Q2, ready 54500) runs: preempt. RUN 2000 → blocks at 58000. |
| 58000 | `hog` resumes in Q2, slice 8000: boundaries 66000, 74000. |
| 71000 | keystroke 4; both Q2 → no preemption. `editor` waits. |
| 74000 | `hog`'s slice boundary: to the back, `editor` runs (preempt). RUN 3000 → blocks at 77000. `hog` resumes. |
| 100000 | boost: everything to Q0; `hog` alone on the lane, keeps running. |
| 120000 | `T_end`. `editor` departs. `hog` still holds the lane. |
| 145000 | `hog` exits (past the window; the trace records it, the harness ignores it). |

## Rows

**`ready_wait`**

| ready | pairs with | value |
|---|---|---|
| `editor` 0 `arrive` | `run_start` 0 | 0 |
| `editor` 8000 `wake` | `run_start` 8000 | 0 |
| `editor` 30000 `wake` | `run_start` 30000 | 0 |
| `hog` 50000 `arrive` | `run_start` 50000 | 0 |
| `editor` 54500 `wake` | `run_start` 56000 | 1500 |
| `editor` 71000 `wake` | `run_start` 74000 | 3000 |

**Lifetime**

| task | occupancy (clipped) | `cpu_delivered` | `demand` | `completed` | `preempt_count` |
|---|---|---|---|---|---|
| `editor` | [0,0] [8000,12000] [30000,36000] [56000,58000] [74000,77000] | 15000 | 15000 | 0 (`depart`) | 0 |
| `hog` | [50000,56000] [58000,74000] [77000,120000 clip] | 6000 + 16000 + 43000 = 65000 | 90000 | 0 (`exit` at 145000 is past `T_end`) | 2 |

No `turnaround` rows. Progress for the hog, computed later by scoring: 65000 / 90000.

**`config_interval`**

| index | applied | until | value |
|---|---|---|---|
| 0 (`fallback`, MLFQ) | 0 | 50600 | 50600 |
| 1 (`unmodified`, MLFQ) | 50600 | 120000 | 69400 |

**`busy`** — 15000 + 65000 = 80000.

No `switch_window` row: entry 1 changes params, not the algorithm.

Total 17 rows.
