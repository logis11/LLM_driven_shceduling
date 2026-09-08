# mock-office — worked derivation

Reduced `c1-office`: a focused writer and an unfocused browser. Condition `fixed`, no table. Scheduler: the lane is otherwise idle, so every task runs as soon as it is ready. All times µs.

## Run file

| task | name | arrive | depart | program | RUN total |
|---|---|---|---|---|---|
| `writer` | `soffice.bin` | 0 | 60000 | WAIT, RUN 8000, WAIT, RUN 3000, WAIT, RUN 5000, WAIT | 16000 |
| `browser` | `chrome` | 0 | 60000 | WAIT | 0 |

Keystrokes on `input:writer`: 10000, 15000, 16000. `T_end` = 60000 (the departs). No TIMER task, so no chains.

## What happens

| t | event |
|---|---|
| 0 | boot config applied. `writer` and `browser` arrive; each is scheduled in file order, reaches its first WAIT, and blocks at once (zero-length occupancy). |
| 10000 | keystroke 1. `writer` ready, runs immediately, starts RUN 8000. |
| 15000, 16000 | keystrokes 2 and 3 arrive while `writer` is mid-burst. They queue; no line. |
| 18000 | RUN 8000 ends. The next WAIT completes instantly on queued keystroke 2 → `ready(wake)` at 18000 inside the occupancy. RUN 3000 starts. |
| 21000 | RUN 3000 ends. WAIT completes instantly on queued keystroke 3 → `ready(wake)` at 21000 inside the occupancy. RUN 5000 starts. |
| 26000 | RUN 5000 ends. WAIT blocks (no keystroke queued). `run_end(block)`. |
| 60000 | `T_end`. Both tasks depart. |

## Rows

**`ready_wait`** — one per `ready` line, value = next `run_start` − t, or 0 inside the task's own occupancy.

| ready | pairs with | value |
|---|---|---|
| `writer` 0 `arrive` | `run_start` 0 | 0 |
| `browser` 0 `arrive` | `run_start` 0 | 0 |
| `writer` 10000 `wake` | `run_start` 10000 | 0 |
| `writer` 18000 `wake` | inside occupancy [10000, 26000] | 0 |
| `writer` 21000 `wake` | inside occupancy [10000, 26000] | 0 |

Three `cause=wake` rows for three keystrokes: the queued ones are counted, at zero wait.

**Lifetime**

| task | occupancy | `cpu_delivered` | `demand` | `completed` | `preempt_count` |
|---|---|---|---|---|---|
| `writer` | [0,0], [10000,26000] | 16000 | 16000 | 0 (`depart`) | 0 |
| `browser` | [0,0] | 0 | 0 | 0 (`depart`) | 0 |

No `turnaround` rows (nothing completed).

**`config_interval`** — one entry, in force from 0 to `T_end`: `schedule`, t 0, value 60000, `fallback`, `MLFQ`, index 0.

**`busy`** — 16000 + 0 = 16000 at `T_end`.

Total 15 rows.
