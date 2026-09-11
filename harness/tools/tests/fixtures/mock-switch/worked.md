# mock-switch — worked derivation

An editor and a batch task under a schedule that switches algorithm twice: boot MLFQ → FIFO (the recognizer named FIFO at the batch task's arrival) → MLFQ (named at a third task's arrival). Condition `llm_algo` on the calibrated table. The fixture exercises the `switch_window` primitive (metrics doc §6.9) in both directions, the `boost_window` primitive (§6.10, added 2026-09-11), the config schedule as the harness's third input, and the `x_mlfq_level` check tool. All times µs.

Scheduler behaviour assumed here, beyond the fixtures README list: MLFQ with 3 queues, slice 2000 µs, growth 2, stamped by entry 1 at 600 µs beside the boot entry (the boot default's own slice is 10 ms since 2026-09-11 and governs nothing here, since no task runs before 600); a task that consumes a full slice is demoted and one that blocks keeps its level; a fresh slice at every dispatch and at every boost; a wake into a strictly higher queue preempts at once, a wake into the same or a lower queue waits for the slice boundary; slice expiry with no competitor demotes without a `run_end`; a switch **out of** MLFQ applies at the running task's slice boundary (the drain); a switch **out of** FIFO applies immediately and the running task is treated as freshly dispatched by MLFQ (the memo's rule (a)); the boost timer restarts at `t_apply` (metrics doc §11, items 7–8, both confirmed). `x_mlfq_level` lines are written for the hog only, whenever its level changes.

## Run file

| task | name | arrive | depart | program | RUN total |
|---|---|---|---|---|---|
| `editor` | `code` | 0 | 100000 | WAIT, RUN 3000, WAIT, RUN 3000, WAIT, RUN 3000, WAIT, RUN 3000, WAIT | 12000 |
| `hog` | `python3` | 10000 | — | RUN 300000, EXIT | 300000 |
| `probe` | `gnome-calculator` | 40000 | 100000 | RUN 500, WAIT | 500 |

Keystrokes on `input:editor`: 20000, 46000, 62000, 90000. `T_end` = 100000.

## Config schedule

| index | `t_us` (t_return) | config | applied at (t_apply) |
|---|---|---|---|
| 0 | 0 | MLFQ 3 / 10000 / 2 / boost 100000, cap null, `fallback` (the boot default) | 0 |
| 1 | 600 | MLFQ 3 / 2000 / 2 / boost 100000, cap null, `unmodified` — the answer to the t = 0 snapshot; same algorithm, applied at its stamped time | 600 |
| 2 | 10600 | FIFO, cap 0.15, `unmodified` | 12000 — the hog's slice (10000 + 2000) drains first |
| 3 | 40600 | MLFQ 3 / 2000 / 2 / **boost 20000**, cap 0.15, `unmodified` | 40600 — FIFO has no slice; applied at once |

The trace carries the applied instants; the schedule carries the params. `W_single` for entry 3 = 2000 · (1 + 2) = 6000 µs of CPU per hog.

## What happens

| t | event |
|---|---|
| 0 | boot config. `editor` arrives, reaches WAIT, blocks (zero-length occupancy). Set change → query. |
| 600 | entry 1 applies (MLFQ, 2000 slice): same algorithm, levels kept, lane idle. |
| 10000 | `hog` arrives, lane free, runs in Q0. Set change → query. |
| 12000 | `hog`'s slice ends: demoted to Q1 (`x_mlfq_level` 0→1). Entry 2 (FIFO) applies here, after the drain. Under FIFO the hog keeps the lane. |
| 20000 | keystroke 1: `editor` ready; FIFO never preempts; it waits. |
| 40000 | `probe` arrives, ready, waits. Set change → query. |
| 40600 | entry 3 (MLFQ) applies at once. Cold start: `hog` running, treated as freshly dispatched in Q0 with a 2000 slice; `editor` (ready 20000) and `probe` (ready 40000) pending in Q0. |
| 42600 | `hog`'s cold slice ends → demoted to Q1 (0→1). Q0 is non-empty → `hog` preempted. `editor` runs (waited 22600), RUN 3000; its Q0 slice is consumed at 44600 → Q1. |
| 45600 | `editor` blocks. `probe` runs (waited 5600), RUN 500. |
| 46000 | keystroke 2: `editor` ready in Q1; `probe` runs in Q0 → no preemption; `editor` waits. |
| 46100 | `probe` blocks forever. `editor` runs in Q1 (waited 100; 3000 < the 4000 slice) → blocks at 49100, stays Q1. |
| 49100 | `hog` resumes in Q1, fresh 4000 slice. |
| 53100 | `hog`'s Q1 slice ends → Q2 (1→2), no competitor, keeps running. |
| 60600 | boost (40600 + 20000): everything to Q0; `hog` (2→0) gets a fresh 2000 slice. |
| 62000 | keystroke 3: `editor` ready in Q0; `hog` is Q0 → no preemption; `editor` waits. |
| 62600 | `hog`'s slice ends → Q1 (0→1); `editor` (Q0) outranks → `hog` preempted. `editor` runs (waited 600); Q0 slice consumed at 64600 → Q1; blocks at 65600. |
| 65600 | `hog` resumes in Q1; 69600 → Q2 (1→2). |
| 80600 | boost: `hog` → Q0 (2→0); 82600 → Q1; 86600 → Q2. |
| 90000 | keystroke 4: `editor` (Q0 since the 80600 boost) over `hog` Q2 → `hog` preempted at once; `editor` runs (waited 0) → blocks at 93000. `hog` resumes. |
| 100000 | `T_end`. `editor` and `probe` depart. `hog` still holds the lane. |
| 322500 | `hog` exits (10000 + 300000 of work + 12500 of others' occupancy; past the window). |

## Rows

**`ready_wait`**

| ready | pairs with | value |
|---|---|---|
| `editor` 0 `arrive` | `run_start` 0 | 0 |
| `hog` 10000 `arrive` | `run_start` 10000 | 0 |
| `editor` 20000 `wake` | `run_start` 42600 | 22600 |
| `probe` 40000 `arrive` | `run_start` 45600 | 5600 |
| `editor` 46000 `wake` | `run_start` 46100 | 100 |
| `editor` 62000 `wake` | `run_start` 62600 | 600 |
| `editor` 90000 `wake` | `run_start` 90000 | 0 |

**Lifetime**

| task | occupancy (clipped) | `cpu_delivered` | `demand` | `completed` | `preempt_count` |
|---|---|---|---|---|---|
| `editor` | [0,0] [42600,45600] [46100,49100] [62600,65600] [90000,93000] | 12000 | 12000 | 0 (`depart`) | 0 |
| `hog` | [10000,42600] [49100,62600] [65600,90000] [93000,100000 clip] | 32600 + 13500 + 24400 + 7000 = 77500 | 300000 | 0 | 3 (42600, 62600, 90000) |
| `probe` | [45600,46100] | 500 | 500 | 0 (`depart`) | 0 |

**`config_interval`**

| index | applied | until | value |
|---|---|---|---|
| 0 (`fallback`, MLFQ) | 0 | 600 | 600 |
| 1 (`unmodified`, MLFQ) | 600 | 12000 | 11400 |
| 2 (`unmodified`, FIFO) | 12000 | 40600 | 28600 |
| 3 (`unmodified`, MLFQ) | 40600 | 100000 | 59400 |

**`switch_window`** — entries 2 and 3 change the algorithm; entry 0 has no predecessor and entry 1 keeps MLFQ.

| switch | alive at t_apply | first `run_end` after t_apply | hogs | value |
|---|---|---|---|---|
| index 2, FIFO, t = 12000 | `editor`, `hog` | `editor` 45600 `block`; `hog` 42600 `preempt` | 1 (`hog`) | 0 — not into MLFQ |
| index 3, MLFQ, t = 40600 | `editor`, `hog`, `probe` | `editor` 45600 `block`; `hog` 42600 `preempt`; `probe` 46100 `block` | 1 (`hog`) | 12500 — see below |

The window closes when the hog has received `W_single` = 6000 of CPU since 40600: 2000 in [40600, 42600], nothing while the editor and the probe hold the lane, the remaining 4000 in [49100, 53100]. `t_close` = 53100, value = 53100 − 40600 = 12500. Under a wall-clock window of 6000 the same descent would have ended 6500 µs past the window — the case that led to the lane-time definition (memo §7).

The FIFO row's hog count is the memo's known bias in the other direction: the hog's first occupancy after 12000 ends in a preempt only because MLFQ took over 30 ms later. The count is informational there; the value is 0 regardless.

**`boost_window`** (§6.10) — inside the MLFQ interval entered at 40600 (entry 3, boost 20000), one row per boost instant `40600 + k · 20000` before the interval's end at `T_end`: 60600 and 80600 (100600 is past `T_end`). Each is sized like a switch window from its instant, with `W_single` = 6000 from entry 3, clipped at the next boost.

| boost | alive | first `run_end` after | hogs | window | value |
|---|---|---|---|---|---|
| 60600 | `editor`, `hog`, `probe` | `editor` 65600 `block`; `hog` 62600 `preempt`; `probe` none | 1 (`hog`) | 2000 in [60600, 62600], 4000 more in [65600, 69600] → [60600, 69600] | 9000 |
| 80600 | `editor`, `hog`, `probe` | `editor` 93000 `block`; `hog` 90000 `preempt`; `probe` none | 1 (`hog`) | uninterrupted → [80600, 86600] | 6000 |

**`busy`** — 12000 + 77500 + 500 = 90000.

Total 28 rows.

## The aggregates, by hand (metrics doc §8)

The interactive task is `editor` (the one the scoring spec names). Wake rows: 20000 → 22600, 46000 → 100, 62000 → 600, 90000 → 0.

- **Switch window** for entry 3: [40600, 53100]. Inside: the 46000 row (100). Boost grid from `t_apply`: 60600, 80600 (100600 is past `T_end`). Each boost window by the same rule: at 60600 the hog (first `run_end` after: 62600 `preempt`) receives 2000 in [60600, 62600] and 4000 more in [65600, 69600] → [60600, 69600]; at 80600 the hog (first `run_end` after: 90000 `preempt`) runs uninterrupted → [80600, 86600]. Inside the boost windows: the 62000 row (600). Rest of the MLFQ interval outside any window: the 90000 row (0).
- **Per-switch excess, switch variant**: 100 − 0 = **100 µs**. **Boost variant**: 600 − 0 = **600 µs**. The switch cost a sixth of a boost here: the pending editor took the lane at the hog's first cold slice.
- **Share of the window inside switch windows**: 12500 / 100000 = **0.125**.
- The 20000 row (22600) falls in the FIFO interval and belongs to no window: that is FIFO's own cost, carried by the P99 term, not by these aggregates.

## The check tool

`x_mlfq_level` shows the hog's demotions after the switch at 40600: 0→1 at 42600, 1→2 (the bottom) at 53100. The window closes at 53100, so the last demotion is **covered**, at the edge: the lane-time window and the simulator's demotion agree to the microsecond because both count the same 6000 µs of the hog's CPU. `check_mlfq_levels.py` reports that and exits 0. Its second test moves the 1→2 line to 55000, a simulator whose demotion lags its CPU accounting, and sees the miss reported.
