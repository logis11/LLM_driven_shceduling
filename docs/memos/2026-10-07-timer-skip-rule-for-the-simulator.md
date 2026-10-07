# TIMER skips missed ticks — the rule for the simulator

> Status: memo · Created 2026-10-07 · Updated 2026-10-07
> From 인지오 to 인경민. Answers your note `simulator/notes/note-for-jioh-timer-backlog-vs-drop.md` (2026-09-29): TIMER's backlog rule is replaced by a skip rule. Decision D3 of task 9.11 (`_dev/research/jioh/task-9.11-scheduler-constants/changelog.md`). Absorb into the simulator guide and the interpretation contract once implemented.

## 1. The rule

A TIMER task with period P keeps its grid t₀ + k·P. When it reaches a TIMER at time `now`:

- **Its next unconsumed tick is later than `now`:** it blocks until that tick. Unchanged.
- **Otherwise:** let m be the last grid index whose tick is at or before `now`. The task consumes tick m at once — job m is released at `now` and is due at tick m + 1. Every unconsumed tick before m is **skipped**: no work runs for it, and it is a job that missed its deadline. The next tick is m + 1.

One overdue tick is consumed at once, exactly as today. Only the ticks beyond it change: they are skipped instead of run back to back, and the job that runs late is the current tick's, not the oldest's.

## 2. A worked example

The 60 fps grid, P = 16 667 µs: ticks at 0, 16 667, 33 334, 50 001, 66 668. The task consumes tick 0 at 0 and runs frame 0, but a heavy stretch keeps it off the lane, so it reaches its next TIMER at t = 55 000. Ticks 1, 2 and 3 have all passed unconsumed; m = 3.

| | backlog (today) | skip (this rule) |
|---|---|---|
| job 0 (due 16 667) | completes at 55 000, missed | the same |
| ticks 1 and 2 | each TIMER completes at once; frames 1 and 2 run back to back | skipped: no work, two missed jobs |
| tick 3 | consumed after frames 1 and 2; frame 3 starts later still | consumed at 55 000; frame 3 runs at once, due 66 668 |
| next block | at 66 668 only if frames 1–3 are done by then | at 66 668 if frame 3 is done |

Under backlog the task's lateness carries into every frame until it catches up, and a task that needs more than the lane never does. Under skip it resumes on the grid with the current tick's frame.

## 3. Your note's three points

- **A RUN's demand survives preemption.** Kept. Skipping happens only when the task reaches a TIMER, so work already started always finishes. Nothing voids a RUN.
- **Executed load becomes scheduler-dependent.** Yes: a starved task runs fewer frames, as a real player does. Offered load is unchanged, and every skipped tick is counted as a missed job, so the damage is measured, not hidden.
- **Chains.** A chain skips at its head only. A frame the head has started runs through every stage; no frame is dropped mid-chain.

## 4. Why

Every program and periodic framework read for 9.11 skips missed activations; none replays them:

- interbench's audio and video emulations count a missed period as missed deadlines and move the deadline past the current time by whole periods (`interbench.c:398–436`, `interbench`).
- ROS 2's executor: "the next activation time point is determined by increasing the current activation time by the minimal multiple of the timer period, such that it is greater than the current time. As a result, the executor may skip timer jobs" (`teper-arxiv24`, §II).
- Lipari and Palopoli's reference periodic thread for Linux skips all late instances: `while (timespec_cmp (&now, &next) > 0) { // Skip late instances` (`lipari-arxiv15`, Listing 2).
- rt-app's default "relative" mode re-anchors the next activation to the current time on an overrun; only its "absolute" mode keeps the grid and catches up (`tutorial.txt:507–509`, `rt-app.c:589–597` at `d6f8be4`; `rt-app`).
- The programs the TIMER tasks stand for: mpv drops late video frames by default (`mpv`); Chromium's fake audio worker runs a late callback once and moves to the next on-time interval (`chromium`); a frame presented in Vulkan's FIFO mode takes the next vertical blank (`vulkan`).

The `job` miss rate is 26 of the scoring spec's 78 terms. Under backlog a stall's overdue ticks run late one after another, the cascade longest for a task whose work fills most of its period, and a chain that needs more than the lane — `c3-evening`'s game segment at `lane_share` 1.45, your 2026-10-06 finding — never drains, so nearly every frame misses under every condition. Under skip the miss rate is the share of ticks not served on time, which still differs between policies under overload. (Reference ids: `../references.md`.)

## 5. What the simulator does

- **TIMER** (`simulator/src/sim.cpp`, your step K, "TIMER + backlog"): the rule of §1.
- **`ready(cause = timer_tick)`**: one line per consumed tick, at the time it is consumed, as today. The harness reads the consumed tick's index as the last tick at or before the line's time, and counts the indices between two consumed ticks as skipped jobs.
- **`deadline`**: one line per job, the skipped ones included. A skipped tick k's line has `met: false`, `due` = tick k + P, `t` = the time of the TIMER that skipped it, and `slack_us` = `due` − `t`. No new event type or field.

The harness side — the `job` primitive in `docs/harness/metrics.md` §6.2, `harness/tools/harness/primitives.py`, and the `mock-media` fixture, which pins backlog today — is 9.14's, the rebuild's consumer rework, and follows this rule.

## 6. What I need from you

1. The rule implemented in the simulator.
2. The interpretation contract's TIMER row (`docs/simulator/interpretation-contract.md:31`) ratified as: "absolute periodic wake on the grid t₀ + k·period, drift-free. Reached after one or more ticks have passed, the task consumes the last passed tick at once and skips the earlier ones, each a missed job with no work."
3. Anything in §1 or §5 that conflicts with the simulator's other invariants, before you build it.
