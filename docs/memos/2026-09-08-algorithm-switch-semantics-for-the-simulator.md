# Algorithm switch semantics for the simulator — the task queue, preemption, and overhead at a mid-run config change

> Status: memo · Created 2026-09-08 · Updated 2026-09-08
> From 인지오 to 인경민. Settles three questions about what the simulator does at the instant a config with a different algorithm lands mid-run. Builds on the Q3 lean in `_dev/archive/2026-08-23-design-meeting-open-questions.md` (drain to a slice boundary, then start cold) and does not overturn it. Absorb into `simulator/simulator-guide.md` once implemented.

## 1. The task queue: the new algorithm takes it immediately

At the switch, the new algorithm owns the pending queue at once. Pending tasks are not drained under the old algorithm first.

What this needs from the queue:

- The pending queue is algorithm-agnostic. It holds task facts only — arrival time, remaining demand, deadline where the process model gives one, observed class. An algorithm is a pick function over that set; switching is a re-sort.
- Remaining demand is stored, not original size. A task preempted under the old algorithm is an ordinary pending task to the new one.
- Every dispatch is stamped with the config index it was made under (the same index the existing `config_applied` event carries). Attribution is per decision, not per task.

Thrash guard: a controller flipping algorithms every few slices can push the same task to the back repeatedly. The executor's starvation safety net already bounds this; no extra rule.

## 2. Preemption: never by the switch, only by the new algorithm's own rule

Nothing is preempted at t_apply. From t_apply onward the new algorithm's preemption semantics govern the running task like any other.

- Into FIFO: the running task keeps the lane until it blocks or exits.
- Into MLFQ, EDF, LOTTERY: the running task is preempted when, and only when, that algorithm's own rule fires — slice expiry or a wake into a higher queue (MLFQ), an earlier-deadline wake (EDF), the next draw (LOTTERY).

Worked case, FIFO → MLFQ, hog running, editor woken and pending: MLFQ starts cold, both in Q0, hog holds a fresh 2000 µs slice. Slice expires → hog demoted to Q1. Editor in Q0 outranks Q1 → editor preempts. Preemption ≈ 2 ms after t_apply, from MLFQ's rule, not from the switch.

Apply instant: the current slice finishes first (the Q3 drain), so t_apply lags t_return by at most one slice of the outgoing algorithm.

**Open — FIFO outgoing.** FIFO has no slice, so "drain to the slice boundary" out of FIFO is unbounded (until the hog blocks or exits). Two candidate rules, not yet chosen:

- (a) apply immediately; the running task is treated as freshly dispatched by the new algorithm, so its tenure is bounded by the new algorithm's slice
- (b) bound the drain by the executor safety-net window

## 3. Overhead: measured, not charged

What the switch discards is scheduler state, never task progress.

| Algorithm | State discarded at switch | Lost? |
|---|---|---|
| MLFQ | queue level, learned from observed behaviour | yes — re-learned by demotion within a few slices |
| EDF | deadlines | no — from the process model |
| LOTTERY | tickets | no — from the config |
| FIFO | arrival order | no — always known |

Three costs, and what to do with each:

- **Re-learning transient** (switch into MLFQ only). CPU-bound tasks sit in Q0 with a fresh slice until demoted; interactive tasks see worse response in that window. Real, behavioural, emerges from the mechanics. Not modeled — it appears in the metrics on its own.
- **Apply delay.** t_apply − t_return, at most one outgoing slice. Real, already captured by the three instants in `terminology.md`.
- **Mechanical cost** (queue rebuild, context switch). Zero virtual time. Not modeled; no constant is added.

Reporting: the per-switch `config_applied` event is the hook. The harness can derive a post-switch window per transition (from t_apply until every CPU-bound task has been demoted once) and how much of each run was spent inside such windows. Whether that becomes a first-class metric is open.

## 4. What is settled and what is open

Settled: §1 (immediate takeover of the pending queue), §2 (no switch-triggered preemption; new algorithm's rule from t_apply), §3 (cold start; no invented switch cost).

Open: FIFO-outgoing apply rule (§2, a or b); post-switch window as a reported metric (§3).
