# Algorithm switch semantics for the simulator — the task queue, preemption, and overhead at a mid-run config change

> Status: memo · Created 2026-09-08 · Updated 2026-09-08
> From 인지오 to 인경민. Settles three questions about what the simulator does at the instant a config with a different algorithm lands mid-run, and how the MLFQ re-learning overhead is measured. Builds on the Q3 lean in `_dev/archive/2026-08-23-design-meeting-open-questions.md` (drain to a slice boundary, then start cold) and does not overturn it. Absorb into `simulator/simulator-guide.md` once implemented.

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

Reporting: §4.

## 4. Measuring the MLFQ re-learning overhead

A cold start into MLFQ places every task in the top queue — the same state MLFQ's own periodic boost produces. One switch into MLFQ is one extra boost, and it is measured in those units.

**Window.** A CPU-bound task reaches the bottom queue after one full slice at each upper level: `W_single = timeslice_us · Σ_{l=0}^{num_queues−2} timeslice_growth^l` (boot default: 2000 + 4000 = 6000 µs of lane time). The window after a switch into MLFQ is `[t_apply, t_apply + W_single · H]`, where H is the hog count below. The window is a function of the incoming params and H only; nothing is read off occupancy lengths.

**Hog count H.** A hog is a task alive at t_apply whose first occupancy after t_apply ends with `run_end(reason = preempt)`. Known bias: a task preempted by a wake into a higher queue is counted too, which widens the window by one `W_single`.

**The number.** Over the `ready_wait` rows with `cause = wake` on the scoring-spec-named interactive task: the excess of rows inside a window over the same task's rows in the rest of that config interval outside any window, per switch, in µs. Alongside: the share of `[0, T_end]` inside windows.

**Baseline.** The same excess over the windows that follow each periodic boost in the same run — boost instants on the grid `t_apply + k · boost_interval_us`. Switch excess ≈ boost excess means the switch cost one boost; the difference above that is backlog carried over from the outgoing algorithm.

**Ground truth.** The simulator emits `x_mlfq_level` `{t, task, from, to}` on every demotion and boost. The harness ignores it per the `x_` rule. A separate check tool reads it and verifies that each window covers the last demotion of every hog after the switch. A systematic miss is the evidence for proposing a field in the closed set; until then the trace contract stays frozen.

## 5. What is settled and what is open

Settled: §1 (immediate takeover of the pending queue), §2 (no switch-triggered preemption; new algorithm's rule from t_apply), §3 (cold start; no invented switch cost), §4 (window from config + behavioural hog count; excess wake `ready_wait` per switch; boost baseline; `x_mlfq_level` as ground truth).

Open: FIFO-outgoing apply rule (§2, a or b); whether the boost timer restarts at t_apply (§4 baseline grid).

## 6. Action plan

### Simulator side (인경민)

- Pending queue holds task facts and remaining demand only; the algorithm is a pick function over it. On `config_applied` with a new algorithm, re-sort the pending set under the new algorithm, cold.
- No preemption at t_apply. The running task finishes its current slice; the new algorithm's rule governs it from then on.
- Choose and document the FIFO-outgoing apply rule (§2 a or b) and the boost-timer behaviour at t_apply; add both to the simulator's written tie-break/semantics notes.
- Emit `x_mlfq_level` `{t, task, from, to}` on every MLFQ demotion and boost.
- Unit test: remaining demand conserved across a switch, in both directions between a preemptive algorithm and FIFO.

### Harness side (인지오)

- `metrics.md` §6: add the `switch_window` primitive — entity `schedule`, one row per `config_applied` whose algorithm differs from the previous entry's, `t` = t_apply, `value` = `W_single · H` for MLFQ and 0 for EDF, LOTTERY, FIFO; `algorithm`, `index`, `hogs` on the row.
- `metrics.md` §8: add the two aggregates — per-switch excess wake `ready_wait` (switch and boost variants) and share of the window inside switch windows.
- `metrics.md` §11: add the boost-timer assumption once 인경민 decides it.
- Mock fixture: one trace with a FIFO → MLFQ switch, hog + editor, values computed by hand.
- Check tool (outside the harness): reads `x_mlfq_level`, reports per switch whether the window covered the last hog demotion.
