# mock-chain — worked derivation

A three-stage frame pipeline, the game chain reduced: the head ticks on a TIMER and wakes the engine, the engine wakes the display. A batch task arrives at 15 s and holds the lane through one tick. Condition `oracle` on the prior table: the oracle's entry (FIFO) is stamped at t = 0 beside the boot entry, as in `mock-media`, so the scheduler stated here is the one the config lines name. Scheduler: FIFO, run until block, no preemption. All times µs.

The ids are `input`, `engine`, `display` on purpose: the reader must find the chain by following WAKE targets from the TIMER-headed task, not by a naming convention.

## Run file

| task | name | arrive | depart | program | RUN total |
|---|---|---|---|---|---|
| `input` | `game.exe` | 0 | 50000 | LOOP { TIMER 16667, RUN 900, WAKE `engine` } | unbounded |
| `engine` | `game.exe` | 0 | 50000 | LOOP { WAIT `chain:engine`, RUN 2600, WAKE `display` } | unbounded |
| `display` | `game.exe` | 0 | 50000 | LOOP { WAIT `chain:display`, RUN 2100 } | unbounded |
| `hog` | `7z` | 15000 | — | RUN 14000, EXIT | 14000 |

Chain: `input` → `engine` → `display` (head `input`, tail `display`). Frame work = 900 + 2600 + 2100 = 5600. `T_end` = 50000. Ticks: 0, 16667, 33334 (50001 is past `T_end`).

## What happens

| t | event |
|---|---|
| 0 | all three chain tasks arrive; `input` first. `input` runs: tick 0 is now → instant `ready(timer_tick)` inside the occupancy; RUN 900. `engine` and `display` are ready (arrive) and wait. |
| 900 | `input` wakes `engine` (`engine` has not yet executed its WAIT, so the wake is stored) and reaches TIMER; tick 1 not due → blocks. `deadline` for the head's job 0: completion 900, due 16667. `engine` runs: its WAIT completes instantly on the stored wake → `ready(wake)` at 900 inside the occupancy. RUN 2600. |
| 3500 | `engine` wakes `display` (stored) and blocks on WAIT. `display` runs: WAIT instant → `ready(wake)` at 3500 inside. RUN 2100. |
| 5600 | `display` blocks. **Frame 0 complete at 5600.** |
| 15000 | `hog` arrives, lane free, runs. |
| 16667 | tick 1: `input` ready; `hog` holds the lane (FIFO). |
| 29000 | `hog` exits. `input` runs: RUN 900. |
| 29900 | `input` wakes `engine` (blocked in WAIT → `ready(wake)` 29900) and blocks on TIMER (tick 2 at 33334 not due). `deadline` head job 1: completion 29900, due 33334, met. `engine` runs. |
| 32500 | `engine` wakes `display` (`ready(wake)` 32500) and blocks. `display` runs. |
| 33334 | tick 2: `input` ready; `display` holds the lane. |
| 34600 | `display` blocks. **Frame 1 complete at 34600** — 17933 after its tick, a miss, while the head's `deadline` line for job 1 says met. `input` runs (only ready task). |
| 35500 | `input` wakes `engine`, blocks on TIMER (tick 3 at 50001 not due). `deadline` head job 2: completion 35500, due 50001. `engine` runs. |
| 38100 | `engine` wakes `display`, blocks. `display` runs. |
| 40200 | `display` blocks. **Frame 2 complete at 40200.** |
| 50000 | `T_end`. Chain tasks depart. |

## Rows

**`ready_wait`**

| ready | pairs with | value |
|---|---|---|
| `input` 0 `arrive` | `run_start` 0 | 0 |
| `input` 0 `timer_tick` | inside [0, 900] | 0 |
| `engine` 0 `arrive` | `run_start` 900 | 900 |
| `display` 0 `arrive` | `run_start` 3500 | 3500 |
| `engine` 900 `wake` | inside [900, 3500] (line follows `run_start`) | 0 |
| `display` 3500 `wake` | inside [3500, 5600] | 0 |
| `hog` 15000 `arrive` | `run_start` 15000 | 0 |
| `input` 16667 `timer_tick` | `run_start` 29000 | 12333 |
| `engine` 29900 `wake` | `run_start` 29900 | 0 |
| `display` 32500 `wake` | `run_start` 32500 | 0 |
| `input` 33334 `timer_tick` | `run_start` 34600 | 1266 |
| `engine` 35500 `wake` | `run_start` 35500 | 0 |
| `display` 38100 `wake` | `run_start` 38100 | 0 |

Chain stages' WAIT completions are `cause=wake`, indistinguishable from keystrokes by cause alone; scoring tells them apart by entity.

**`job`** — entity is the chain head; frame k completion = the end of the tail's k-th iteration; value = completion − tick k.

| k | tick | tail iteration end | value | vs period |
|---|---|---|---|---|
| 0 | 0 | 5600 | 5600 | met |
| 1 | 16667 | 34600 | 17933 | **miss** |
| 2 | 33334 | 40200 | 6866 | met |

Guard: tail iterations (3) = head ticks (3).

The head's `deadline` lines say 900 / 29900 / 35500, all met. They measure the input stage alone and are expected to disagree with frame latency; the reader does not derive `job` rows from them for a chain longer than one.

**Lifetime**

| task | `cpu_delivered` | `demand` | `completed` | `turnaround` | `preempt_count` |
|---|---|---|---|---|---|
| `input` | 3 × 900 = 2700 | — | 0 | — | 0 |
| `engine` | 3 × 2600 = 7800 | — | 0 | — | 0 |
| `display` | 3 × 2100 = 6300 | — | 0 | — | 0 |
| `hog` | 14000 | 14000 | 1 at 29000 | 14000 | 0 |

**`config_interval`** — two entries at the same instant: index 0 (`fallback`, MLFQ) with value 0, superseded at once; index 1 (`unmodified`, FIFO) with value 50000.

**`switch_window`** — index 1 changes the algorithm (MLFQ → FIFO) at t 0: value 0 (not into MLFQ), `hogs` 0 (`input`, `engine`, `display` are alive at 0 and each blocks first; `hog` arrives later).

**`busy`** — 2700 + 7800 + 6300 + 14000 = 30800.

Total 34 rows.
