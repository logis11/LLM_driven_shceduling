# mock-media — worked derivation

Reduced `c1-media`: a video player and a music player, plus a batch scan injected at 20 s long enough to make the video player pass two of its ticks in one stall. Condition `oracle` on the prior table: the oracle's answer is stamped at t = 0 beside the boot entry. Scheduler: FIFO, run until block, no preemption (the oracle's row selects FIFO in this mock). All times µs.

Derived under the ratified TIMER rules: a TIMER consumes the latest grid tick at or before the instant it is reached and **skips** every unconsumed tick before it (9.11 D3; `docs/memos/2026-10-07-timer-skip-rule-for-the-simulator.md`); the grid's `t₀` is the task's first TIMER execution (metrics doc §11, item 4), which is its arrival: each player's first instruction is its TIMER, and the executor executes it in the arrival step, without the lane, on a free lane or a busy one (fixtures README, item 3); a skipped tick is a job that missed with no work and no completion, and the simulator writes one `deadline` line for it with `met: false` (9.11 D17).

Re-derived 2026-10-17 (9.15, t₀ at the arrival): `music`'s grid moves from its first dispatch (6667; ticks 6667, 56667) to its arrival (0; ticks 0, 50000), and both players' tick-0 `ready(timer_tick)` lines are written in the arrival step, before the first `run_start`. The 2026-10-09 derivation (9.14) brought in the skip rule, the 46 666 µs scan and the first-dispatch grid; the one before it pinned the backlog rule (every overdue tick run back to back) and the arrival-time grid, with a 31 000 µs scan and no tick ever two deep.

## Run file

| task | name | arrive | depart | program | RUN total |
|---|---|---|---|---|---|
| `video` | `mpv` | 0 | 95000 | LOOP { TIMER 16667, RUN 6667 } | unbounded → no `demand` |
| `music` | `spotify` | 0 | 95000 | LOOP { TIMER 50000, RUN 2500 } | unbounded → no `demand` |
| `scan` | `clamscan` | 20000 | — | RUN 46666, EXIT | 46666 |

`T_end` = 95000. Both TIMER tasks are chains of length one.

Grids. Both players execute their first TIMER in their arrival step at 0. `video`'s ticks are 0, 16667, 33334, 50001, 66668, 83335 (100002 is past `T_end`); `music`'s are 0 and 50000 (100000 is past `T_end`), though it first runs at 6667, when `video` blocks.

## What happens

| t | event |
|---|---|
| 0 | boot entry (index 0, MLFQ, `fallback`) then the oracle's entry (index 1, FIFO, `unmodified`) at the same instant. `video` and `music` arrive, in file order, and each executes its TIMER in its arrival step: tick 0 is now, consumed without blocking → `ready(arrive)` and `ready(timer_tick)` at 0, `video`'s then `music`'s, before any dispatch. `video` runs first (file order): RUN 6667. `music` waits for the lane. |
| 6667 | `video` reaches TIMER, tick 1 (16667) not due → blocks. `deadline` job 0: completion 6667, due 16667, slack 10000. `music` runs for the first time: its tick 0 was consumed at its arrival, so RUN 2500. |
| 9167 | `music` reaches TIMER, tick 1 (50000) not due → blocks. `deadline` job 0: completion 9167, due 50000, slack 40833. |
| 16667 | `video` tick 1: ready, lane free, runs. |
| 20000 | `scan` arrives, ready; `video` holds the lane (FIFO). |
| 23334 | `video` blocks (job 1 complete, due 33334, slack 10000). `scan` runs. |
| 33334 | `video` tick 2: ready; `scan` holds the lane. |
| 50000 | `music` tick 1: ready; `scan` holds the lane. |
| 50001 | `video` tick 3 passes while `video` is already runnable. No line: no blocking primitive completed. |
| 66668 | `video` tick 4 passes while `video` is still waiting. No line. |
| 70000 | `scan` exits (46666 of CPU). FIFO order: `video` (ready 33334) before `music` (ready 50000). `video` runs job 2. |
| 76667 | `video` finishes job 2 and reaches TIMER. Ticks 3 (50001) and 4 (66668) have passed; tick 5 (83335) has not. The skip rule: the latest passed tick, 4, is consumed at once and tick 3 is **skipped** — no work runs for it. Lines, in tick order: `deadline` job 2 (completion 76667, due 50001, slack −26666, missed); `deadline` for tick 3 (due 66668, `met: false`, no completion — the slack written is due − now, −9999, and the reader reads `met` alone); `ready(timer_tick)` inside the occupancy for tick 4. RUN 6667 for job 4. |
| 83334 | `video` finishes job 4 and reaches TIMER; tick 5 (83335) is 1 µs away → blocks. `deadline` job 4: completion 83334, due 83335, slack 1, met. `music` runs (ready since 50000); its TIMER for tick 1 completed when it woke, so RUN 2500. |
| 83335 | `video` tick 5: ready; `music` holds the lane (FIFO, no preemption). |
| 85834 | `music` reaches TIMER (tick 2 at 100000 not due) → blocks. `deadline` job 1: completion 85834, due 100000, slack 14166. `video` runs job 5. |
| 92501 | `video` blocks (tick 6 at 100002 not due). `deadline` job 5: completion 92501, due 100002, slack 7501. |
| 95000 | `T_end`. `video` and `music` depart. |

## Rows

**`ready_wait`**

| ready | pairs with | value |
|---|---|---|
| `video` 0 `arrive` | `run_start` 0 | 0 |
| `video` 0 `timer_tick` | `run_start` 0 | 0 |
| `music` 0 `arrive` | `run_start` 6667 | 6667 |
| `music` 0 `timer_tick` | `run_start` 6667 | 6667 |
| `video` 16667 `timer_tick` | `run_start` 16667 | 0 |
| `scan` 20000 `arrive` | `run_start` 23334 | 3334 |
| `video` 33334 `timer_tick` | `run_start` 70000 | 36666 |
| `music` 50000 `timer_tick` | `run_start` 83334 | 33334 |
| `video` 76667 `timer_tick` | inside [70000, 83334] | 0 |
| `video` 83335 `timer_tick` | `run_start` 85834 | 2499 |

Five `timer_tick` rows for `video` for six ticks in the window: the skipped tick 3 has no line. Under the backlog rule it would have had one. `music`'s tick-0 line falls at its arrival, outside any occupancy, so it pairs with its first dispatch like its `arrive` line: 6667 µs of `video` holding the lane.

**`job`** — per tick; a consumed tick's completion is the instant the task next reaches its TIMER (the end of that iteration's RUN); value = completion − tick. A skipped tick's row has no completion and `skipped` 1; it counts as missed.

| task | k | tick | completion | value | skipped | vs period |
|---|---|---|---|---|---|---|
| `video` | 0 | 0 | 6667 | 6667 | 0 | met |
| `video` | 1 | 16667 | 23334 | 6667 | 0 | met |
| `video` | 2 | 33334 | 76667 | 43333 | 0 | **miss** |
| `video` | 3 | 50001 | — | — | 1 | **miss (skipped)** |
| `video` | 4 | 66668 | 83334 | 16666 | 0 | met |
| `video` | 5 | 83335 | 92501 | 9166 | 0 | met |
| `music` | 0 | 0 | 9167 | 9167 | 0 | met |
| `music` | 1 | 50000 | 85834 | 35834 | 0 | met |

The consumed ticks of `video` are five and its iteration ends five, so the chain guard holds; its miss rate is 2 of 6. `music` consumes both its ticks and meets both (miss rate 0 of 2). Cross-check: the six `deadline` lines of `video` and the two of `music` pair with the rows by tick order; each consumed tick's line has `t` equal to the completion and `slack_us` = period − value (`music`'s 40833 and 14166); the skipped tick's line says `met: false`.

**Lifetime**

| task | `arrival` | occupancy | `cpu_delivered` | `demand` | `completed` | `turnaround` | `preempt_count` |
|---|---|---|---|---|---|---|---|
| `video` | 0 | [0,6667] [16667,23334] [70000,83334] [85834,92501] | 6667+6667+13334+6667 = 33335 | — | 0 | — | 0 |
| `music` | 0 | [6667,9167] [83334,85834] | 5000 | — | 0 | — | 0 |
| `scan` | 20000 | [23334,70000] | 46666 | 46666 | 1 at 70000 | 70000 − 20000 = 50000 | 0 |

`busy` = 33335 + 5000 + 46666 = 85001.

**`config_interval`** — index 0 at 0 with value 0 (the boot entry governs no time: the oracle's entry lands at the same instant), index 1 at 0 with value 95000.

**`switch_window`** — index 1 changes the algorithm (MLFQ → FIFO) at t 0: value 0 (not into MLFQ), `hogs` 0 (both players block before their first slice would end; `scan` arrives later).
