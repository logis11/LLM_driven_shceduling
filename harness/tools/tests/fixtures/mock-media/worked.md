# mock-media — worked derivation

Reduced `c1-media`: a video player and a music player, plus a batch scan injected at 20 s to force backlog. Condition `oracle` on the prior table: the oracle's answer is stamped at t = 0 beside the boot entry. Scheduler: FIFO, run until block, no preemption (the oracle's row selects FIFO in this mock). All times µs.

## Run file

| task | name | arrive | depart | program | RUN total |
|---|---|---|---|---|---|
| `video` | `mpv` | 0 | 95000 | LOOP { TIMER 16667, RUN 6667 } | unbounded → no `demand` |
| `music` | `spotify` | 0 | 95000 | LOOP { TIMER 50000, RUN 2500 } | unbounded → no `demand` |
| `scan` | `clamscan` | 20000 | — | RUN 31000, EXIT | 31000 |

`T_end` = 95000. Ticks: `video` 0, 16667, 33334, 50001, 66668, 83335 (100002 is past `T_end`); `music` 0, 50000 (100000 is past `T_end`). Both TIMER tasks are chains of length one.

## What happens

| t | event |
|---|---|
| 0 | boot entry (index 0, MLFQ, `fallback`) then the oracle's entry (index 1, FIFO, `unmodified`) at the same instant. `video` and `music` arrive. `video` first (file order): `ready(arrive)`, `run_start`, executes TIMER — tick 0 is now, completes instantly → `ready(timer_tick)` inside the occupancy. RUN 6667. `music` is ready (arrive) and waits. |
| 6667 | `video` reaches TIMER, tick 1 not due → blocks. `deadline` for job 0: completion 6667, due 16667, slack 10000. `music` runs: TIMER tick 0 already passed → instant `ready(timer_tick)` inside its occupancy. RUN 2500. |
| 9167 | `music` blocks on TIMER. `deadline` job 0: due 50000, slack 40833. |
| 16667 | `video` tick 1: ready, lane free, runs. |
| 20000 | `scan` arrives, ready; `video` holds the lane (FIFO). |
| 23334 | `video` blocks (job 1 complete, due 33334, slack 10000). `scan` runs. |
| 33334 | `video` tick 2: ready; `scan` holds the lane. |
| 50000 | `music` tick 1: ready; `scan` holds the lane. |
| 50001 | `video` tick 3 passes while `video` is already runnable. No line: no blocking primitive completed. |
| 54334 | `scan` exits (31000 of CPU). FIFO order: `video` (ready 33334) before `music` (ready 50000). `video` runs. |
| 61001 | `video` finishes frame 2, reaches TIMER; tick 3 (50001) is past → instant completion, `ready(timer_tick)` inside the occupancy. `deadline` job 2: completion 61001, due 50001, slack −11000, missed. RUN continues. |
| 66668 | `video` tick 4 passes while `video` is running. No line. |
| 67668 | frame 3 done; tick 4 past → instant, `ready(timer_tick)` inside. `deadline` job 3: due 66668, slack −1000, missed. |
| 74335 | frame 4 done; tick 5 (83335) not due → blocks. `deadline` job 4: due 83335, slack 9000. `music` runs. |
| 76835 | `music` blocks. `deadline` job 1: due 100000, slack 23165. |
| 83335 | `video` tick 5: ready, runs. |
| 90002 | `video` blocks. `deadline` job 5: due 100002, slack 10000. |
| 95000 | `T_end`. `video` and `music` depart. |

## Rows

**`ready_wait`**

| ready | pairs with | value |
|---|---|---|
| `video` 0 `arrive` | `run_start` 0 | 0 |
| `video` 0 `timer_tick` | inside [0, 6667] | 0 |
| `music` 0 `arrive` | `run_start` 6667 | 6667 |
| `music` 6667 `timer_tick` | inside [6667, 9167] | 0 |
| `video` 16667 `timer_tick` | `run_start` 16667 | 0 |
| `scan` 20000 `arrive` | `run_start` 23334 | 3334 |
| `video` 33334 `timer_tick` | `run_start` 54334 | 21000 |
| `music` 50000 `timer_tick` | `run_start` 74335 | 24335 |
| `video` 61001 `timer_tick` | inside [54334, 74335] | 0 |
| `video` 67668 `timer_tick` | inside [54334, 74335] | 0 |
| `video` 83335 `timer_tick` | `run_start` 83335 | 0 |

Six `timer_tick` rows for `video` = six ticks in the window. A simulator that skipped backlogged ticks would show four.

**`job`** — per tick; completion = the instant the task next reaches its TIMER (the end of that iteration's RUN); value = completion − tick.

| task | k | tick | completion | value | vs period |
|---|---|---|---|---|---|
| `video` | 0 | 0 | 6667 | 6667 | met |
| `video` | 1 | 16667 | 23334 | 6667 | met |
| `video` | 2 | 33334 | 61001 | 27667 | **miss** |
| `video` | 3 | 50001 | 67668 | 17667 | **miss** |
| `video` | 4 | 66668 | 74335 | 7667 | met |
| `video` | 5 | 83335 | 90002 | 6667 | met |
| `music` | 0 | 0 | 9167 | 9167 | met |
| `music` | 1 | 50000 | 76835 | 26835 | met |

Cross-check: each `deadline` line's `t` equals the completion above and `slack_us` = period − value. They agree, as they must for length-one chains.

**Lifetime**

| task | occupancy | `cpu_delivered` | `demand` | `completed` | `turnaround` | `preempt_count` |
|---|---|---|---|---|---|---|
| `video` | [0,6667] [16667,23334] [54334,74335] [83335,90002] | 6667+6667+20001+6667 = 40002 | — | 0 | — | 0 |
| `music` | [6667,9167] [74335,76835] | 5000 | — | 0 | — | 0 |
| `scan` | [23334,54334] | 31000 | 31000 | 1 at 54334 | 54334 − 20000 = 34334 | 0 |

**`config_interval`**

| index | applied | until | value |
|---|---|---|---|
| 0 (`fallback`, MLFQ) | 0 | 0 (next entry) | 0 |
| 1 (`unmodified`, FIFO) | 0 | 95000 (`T_end`) | 95000 |

**`busy`** — 40002 + 5000 + 31000 = 76002.

Total 33 rows.
