# mock-p1a — worked derivation

Reduced `c2-p1a`: an editor, and a training run arriving at 50 s with more work than the window holds. Condition `llm_vocab` on the prior table, recognition latency 600 µs. Scheduler: MLFQ with a 2000 µs slice; a woken interactive task preempts the batch task at the batch task's next slice boundary; interactive bursts run to completion. All times µs.

## Run file

| task | name | arrive | depart | program | RUN total |
|---|---|---|---|---|---|
| `editor` | `code` | 0 | 120000 | WAIT, RUN 4000, WAIT, RUN 6000, WAIT, RUN 2000, WAIT, RUN 3000, WAIT | 15000 |
| `hog` | `python3` | 50000 | — | RUN 90000, EXIT | 90000 |

Keystrokes on `input:editor`: 8000, 30000, 54500, 71000. `T_end` = 120000. The hog needs 90000 in a window of 70000: it cannot finish, as in the real file.

## What happens

| t | event |
|---|---|
| 0 | boot config (index 0, `fallback`). `editor` arrives, reaches WAIT, blocks (zero-length occupancy). |
| 8000 | keystroke 1; lane free; RUN 4000 → blocks at 12000. |
| 30000 | keystroke 2; RUN 6000 → blocks at 36000. |
| 50000 | `hog` arrives, lane free, runs. Set change → the recognizer is consulted. |
| 50600 | recognizer's answer applied (index 1, `unmodified`, MLFQ with the row's cap). |
| 54500 | keystroke 3; `hog` holds the lane. `editor` waits. |
| 56000 | `hog`'s slice boundary (50000 + 3 × 2000): preempted. `editor` runs RUN 2000 → blocks at 58000. `hog` resumes. |
| 71000 | keystroke 4; `editor` waits. |
| 72000 | `hog`'s slice boundary (58000 + 7 × 2000): preempted. `editor` runs RUN 3000 → blocks at 75000. `hog` resumes. |
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
| `editor` 71000 `wake` | `run_start` 72000 | 1000 |

**Lifetime**

| task | occupancy (clipped) | `cpu_delivered` | `demand` | `completed` | `preempt_count` |
|---|---|---|---|---|---|
| `editor` | [0,0] [8000,12000] [30000,36000] [56000,58000] [72000,75000] | 15000 | 15000 | 0 (`depart`) | 0 |
| `hog` | [50000,56000] [58000,72000] [75000,120000 clip] | 6000 + 14000 + 45000 = 65000 | 90000 | 0 (`exit` at 145000 is past `T_end`) | 2 |

No `turnaround` rows. Progress for the hog, computed later by scoring: 65000 / 90000.

**`config_interval`**

| index | applied | until | value |
|---|---|---|---|
| 0 (`fallback`, MLFQ) | 0 | 50600 | 50600 |
| 1 (`unmodified`, MLFQ) | 50600 | 120000 | 69400 |

**`busy`** — 15000 + 65000 = 80000.

Total 17 rows.
