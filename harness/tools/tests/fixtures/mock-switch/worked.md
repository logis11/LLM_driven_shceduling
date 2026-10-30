# mock-switch — worked derivation

An editor and a batch task under a schedule that switches algorithm twice: boot MLFQ → FIFO (the recognizer named FIFO at the batch task's arrival) → MLFQ (named at a third task's arrival). Condition `llm_algo` on the calibrated table. The fixture exercises the `switch_window` primitive (metrics doc §6.9) in both directions, the `boost_window` primitive (§6.10, added 2026-09-11), the config schedule as the harness's third input, and the `x_mlfq_level` check tool. All times µs.

Scheduler behaviour assumed here, beyond the fixtures README list: MLFQ with 3 queues, slice 2000 µs, growth 2, stamped by entry 1 at 600 µs beside the boot entry (the boot default's own slice is 10 ms since 2026-09-11 and governs nothing here, since no task runs before 600); a task that uses up its allotment at a level — the slice, counted across its bursts and kept when it blocks or is preempted — is demoted, and one that blocks before then keeps its level, so a burst ending at the instant its allotment does is demoted as it blocks (MLFQ rules 3–4, `docs/simulator/simulator-guide.md` §5; restated 2026-10-30 from a fresh slice at every dispatch, `simulator/memo/memo_261023.md` Part H3, with no line of this trace changed); the allotment starts afresh at a demotion, at every boost, and at a slice end in the bottom queue; at a slice boundary the lane goes to the head of the highest non-empty queue, a demoted or preempted task joining the tail of its queue (rule 2: always run from the highest non-empty queue, round-robin within a queue); a wake into a strictly higher queue preempts at once, a wake into the same or a lower queue waits for the slice boundary; slice expiry with no competitor demotes without a `run_end` (a competitor: a ready task in the holder's new queue or a higher one); a switch **out of** MLFQ stamped while a task holds the lane applies the next time the lane is free — when that task's slice or current RUN ends, or it is preempted or departs (the drain; `docs/data-contracts.md` §7, **Drain**), here the hog's slice end at 12000; a switch **out of** FIFO applies immediately and the running task is treated as freshly dispatched by MLFQ (the memo's rule (a)); the boost timer restarts at `t_apply` (metrics doc §11, items 7–8, both confirmed). `x_mlfq_level` lines are written for `hog` and `editor` whenever a demotion or a boost changes their level, up to `T_end` (`probe` never leaves Q0; the cold start at 40600 writes none).

Re-derived 2026-10-17 (9.15): `editor`, whose first instruction is a WAIT, blocks in its arrival step, with no `ready` line and no occupancy, as the reference simulator's arrival step does (`simulator/src/sim.cpp`, `on_arrive`; fixtures README, item 4). The earlier derivation scheduled it at 0 for a zero-length occupancy; it ran no work there and kept its level, so nothing after 0 changes.

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
| 0 | boot config. `editor` arrives and executes its first instruction, a WAIT, in its arrival step: it blocks there, with no `ready` line and no occupancy. Set change → query. |
| 600 | entry 1 applies (MLFQ, 2000 slice): same algorithm, levels kept, lane idle. |
| 10000 | `hog` arrives, lane free, runs in Q0. Set change → query. |
| 12000 | `hog`'s slice ends: demoted to Q1 (`x_mlfq_level` 0→1). Entry 2 (FIFO) applies here, after the drain. Under FIFO the hog keeps the lane. |
| 20000 | keystroke 1: `editor` ready; FIFO never preempts; it waits. |
| 40000 | `probe` arrives, ready, waits. Set change → query. |
| 40600 | entry 3 (MLFQ) applies at once. Cold start: `hog` running, treated as freshly dispatched in Q0 with a 2000 slice; `editor` (ready 20000) and `probe` (ready 40000) pending in Q0, in that order. |
| 42600 | `hog`'s cold slice ends → demoted to Q1 (0→1). Q0 is non-empty → `hog` preempted. `editor` runs (waited 22600), RUN 3000. |
| 44600 | `editor`'s Q0 slice ends with 1000 of the burst left → demoted to Q1 (0→1), behind `hog`. `probe` (Q0) outranks both → `editor` preempted. `probe` runs (waited 4600), RUN 500. |
| 45100 | `probe` blocks forever, in Q0. Q1 holds `hog` (since 42600), then `editor` (since 44600): `hog` runs, fresh 4000 slice. |
| 46000 | keystroke 2: `editor` is ready in Q1, mid-burst, not waiting → the wake is queued for its next WAIT. |
| 49100 | `hog`'s Q1 slice ends → Q2 (1→2); `editor` (Q1) outranks → `hog` preempted. `editor` runs, fresh 4000 slice. |
| 50100 | `editor` finishes the burst; its WAIT completes at once on the queued keystroke → `ready(wake)` inside the occupancy; RUN 3000. |
| 53100 | `editor`'s burst and its Q1 slice end together: it has burned the whole slice → Q2 (1→2) as it blocks. `hog` resumes in Q2. |
| 60600 | boost (40600 + 20000): everything to Q0 (`editor` 2→0, `hog` 2→0); `hog` gets a fresh 2000 slice. |
| 62000 | keystroke 3: `editor` ready in Q0; `hog` is Q0 → no preemption; `editor` waits. |
| 62600 | `hog`'s slice ends → Q1 (0→1); `editor` (Q0) outranks → `hog` preempted. `editor` runs (waited 600), RUN 3000. |
| 64600 | `editor`'s Q0 slice ends with 1000 left → Q1 (0→1), behind `hog` → `editor` preempted. `hog` runs in Q1, fresh 4000 slice. |
| 68600 | `hog`'s Q1 slice ends → Q2 (1→2); `editor` (Q1) outranks → `hog` preempted. `editor` runs, finishes the burst, blocks at 69600 before its slice ends, stays Q1. |
| 69600 | `hog` resumes in Q2; its 8000 slice expires at 77600 with no competitor: no `run_end`, no level change. |
| 80600 | boost: `editor` → Q0 (1→0), `hog` → Q0 (2→0); `hog` 82600 → Q1, 86600 → Q2, no competitor either time. |
| 90000 | keystroke 4: `editor` (Q0 since the 80600 boost) over `hog` Q2 → `hog` preempted at once; `editor` runs (waited 0). At 92000 its Q0 slice ends → Q1 (0→1), still above `hog` → keeps the lane; blocks at 93000. `hog` resumes. |
| 100000 | `T_end`. `editor` and `probe` depart. `hog` still holds the lane. |
| 322500 | `hog` exits (10000 + 300000 of work + 12500 of others' occupancy; past the window). |

## Rows

**`ready_wait`**

| ready | pairs with | value |
|---|---|---|
| `hog` 10000 `arrive` | `run_start` 10000 | 0 |
| `editor` 20000 `wake` | `run_start` 42600 | 22600 |
| `probe` 40000 `arrive` | `run_start` 44600 | 4600 |
| `editor` 50100 `wake` (keystroke 2, queued at 46000) | inside occupancy [49100, 53100] | 0 |
| `editor` 62000 `wake` | `run_start` 62600 | 600 |
| `editor` 90000 `wake` | `run_start` 90000 | 0 |

**`input_latency`** — one per keystroke at its wake event, value = the start of the service of the WAIT it completes − its wake time (metrics doc §6.12; added 2026-10-30): 20000 → `run_start` 42600, 22600; 46000 → served at 50100 inside the occupancy, 4100, where its `ready_wait` reads 0; 62000 → `run_start` 62600, 600; 90000 → 0; each `censored` 0.

**Lifetime**

| task | `arrival` | occupancy (clipped) | `cpu_delivered` | `demand` | `completed` | `preempt_count` |
|---|---|---|---|---|---|---|
| `editor` | 0 | [42600,44600] [49100,53100] [62600,64600] [68600,69600] [90000,93000] | 2000 + 4000 + 2000 + 1000 + 3000 = 12000 | 12000 | 0 (`depart`) | 2 (44600, 64600) |
| `hog` | 10000 | [10000,42600] [45100,49100] [53100,62600] [64600,68600] [69600,90000] [93000,100000 clip] | 32600 + 4000 + 9500 + 4000 + 20400 + 7000 = 77500 | 300000 | 0 | 5 (42600, 49100, 62600, 68600, 90000) |
| `probe` | 40000 | [44600,45100] | 500 | 500 | 0 (`depart`) | 0 |

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
| index 2, FIFO, t = 12000 | `editor`, `hog` | `editor` 44600 `preempt`; `hog` 42600 `preempt` | 2 (`editor`, `hog`) | 0 — not into MLFQ |
| index 3, MLFQ, t = 40600 | `editor`, `hog`, `probe` | `editor` 44600 `preempt`; `hog` 42600 `preempt`; `probe` 45100 `block` | 2 (`editor`, `hog`) | 12500 — see below |

The window closes when the last counted hog has received `W_single` = 6000 of CPU since 40600. `hog`: 2000 in [40600, 42600], 4000 in [45100, 49100] → 6000 at 49100. `editor`: 2000 in [42600, 44600], 4000 in [49100, 53100] → 6000 at 53100. `t_close` = 53100, value = 53100 − 40600 = 12500. Under the memo's first window, `W_single · H` on the wall clock (memo §4) — 12000 µs with the two hogs, [40600, 52600] — the hog's descent (49100) falls inside and the editor's (53100) 500 µs past it: a counted hog's descent outlasting the window, the case that led to the lane-time definition (memo §7).

The FIFO row's hog count is the memo's known bias in the other direction: both tasks' first `run_end` after 12000 is a preempt only because MLFQ took over at 40600. The count is informational there; the value is 0 regardless.

**`boost_window`** (§6.10) — inside the MLFQ interval entered at 40600 (entry 3, boost 20000), one row per boost instant `40600 + k · 20000` before the interval's end at `T_end`: 60600 and 80600 (100600 is past `T_end`). Each is sized like a switch window from its instant, with `W_single` = 6000 from entry 3, clipped at the next boost.

| boost | alive | first `run_end` after | hogs | window | value |
|---|---|---|---|---|---|
| 60600 | `editor`, `hog`, `probe` | `editor` 64600 `preempt`; `hog` 62600 `preempt`; `probe` none | 2 (`editor`, `hog`) | `hog`: 2000 in [60600, 62600], 4000 more in [64600, 68600] → 6000 at 68600; `editor`: 2000 in [62600, 64600], 1000 in [68600, 69600], then blocked until 90000 → 3000 by the next boost; clipped there → [60600, 80600] | 20000 |
| 80600 | `editor`, `hog`, `probe` | `editor` 93000 `block`; `hog` 90000 `preempt`; `probe` none | 1 (`hog`) | uninterrupted → [80600, 86600] | 6000 |

**`busy`** — 12000 + 77500 + 500 = 90000.

Total 34 rows.

## The aggregates, by hand (metrics doc §8)

The interactive task is `editor` (the one the scoring spec names). Wake rows: 20000 → 22600, 50100 → 0 (keystroke 2, queued at 46000 while the editor was mid-burst), 62000 → 600, 90000 → 0.

- **Switch window** for entry 3: [40600, 53100]. Inside: the 50100 row (0). Boost grid from `t_apply`: 60600, 80600 (100600 is past `T_end`). Each boost window by the same rule: at 60600 two hogs (first `run_end` after: `editor` 64600 `preempt`, `hog` 62600 `preempt`); the hog has its 6000 at 68600, the editor only 3000 by the next boost, so the window is clipped there → [60600, 80600]; at 80600 the hog (first `run_end` after: 90000 `preempt`) runs uninterrupted → [80600, 86600]. Inside the boost windows: the 62000 row (600). Rest of the MLFQ interval outside any window: the 90000 row (0).
- **Per-switch excess, switch variant**: 0 − 0 = **0 µs**. **Boost variant**: 600 − 0 = **600 µs**. The switch window's one keystroke reached the editor mid-burst and paired with zero wait, so the switch variant carries nothing; the boost variant carries the 600 µs the 62000 keystroke waited for the hog's Q0 slice to end.
- **Share of the window inside switch windows**: 12500 / 100000 = **0.125**.
- The 20000 row (22600) falls in the FIFO interval and belongs to no window: that is FIFO's own cost, carried by the P99 term, not by these aggregates.

## The check tool

`x_mlfq_level` shows the two counted hogs' demotions after the switch at 40600: `hog` 0→1 at 42600 and 1→2 (the bottom) at 49100; `editor` 0→1 at 44600 and 1→2 at 53100. The window closes at 53100, so both last demotions are **covered**, the editor's at the edge: the lane-time window and the simulator's demotion agree to the microsecond because both count the same 6000 µs of the editor's CPU. `check_mlfq_levels.py` reports that and exits 0. Its second test moves the 1→2 line at 53100 to 55000, a simulator whose demotion lags its CPU accounting, and sees the miss reported.
