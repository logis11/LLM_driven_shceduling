# Metrics — primitives, records, and the aggregates the research reads

> Status: normative · Created 2026-09-08 · Updated 2026-10-30

Every number the project reports is defined here. The document fixes three things: the **primitives** — the raw observations the harness computes from a trace or a recognition log; the **records** file they land in; and the **aggregates** — the statistics, the normalisation rule, and the constants that turn records into the figures the research questions ask for. Per-file weights are not here; they are data, in the scoring spec (`harness/scoring/scoring-spec.yaml`, §2). The code that implements the trace primitives lives in `harness/`; the grader that implements the recognition primitives is built in Phase 8 to the definitions below.

Changing a primitive invalidates every records file and requires recomputation from traces. Changing an aggregate, a constant, or a floor requires re-reading records only. Both kinds of change land in the changelog (§13).

---

## 1. Vocabulary

- **Layer 1** and **Layer 2** keep their meaning from `../terminology.md`: recognition accuracy, and consumer performance.
- **Primitives** — the raw observations computed from a trace (Layer 2 material) or from a recognition log (Layer 1 material). One observation is one row of records. A primitive never knows which file it is looking at, which task is the editor, or which condition produced the trace.
- **Scoring** — everything computed from records: aggregates, normalisation, weights, the gate. The boundary between records and scores is the boundary between what needs a trace and what does not.
- **Entity** — whom an observation is about: a task id from the trace, or one of three reserved names — `lane` (the CPU), `schedule` (the config schedule), `recognizer` (the recognizer's answers).
- **Observation window** — the interval `[0, T_end]` every primitive is measured over (§4).
- **Aggregate** — a statistic over a set of records rows: a percentile, a fraction, a maximum. Aggregates are never stored in records.
- **Familiarity tier** — the tier (1–5) of a segment's process names, as defined in `../workload/building-plan.md` C5 and carried in `ground_truth`. A split key for reporting, never a primitive input.

---

## 2. The pipeline

```
primitives(run_file, trace, config_schedule)      → records rows   (entities: tasks, lane, schedule)
grader(recognition_log, ground_truth, calibrated_table) → records rows   (entity: recognizer)
scoring(records, scoring_spec)                    → aggregates, normalised shares, scores
```

The first function is Phase 5's harness lower half. The second is Phase 8's grader, implementing §7. The third is Phase 8's scorer applying the **scoring spec** — `harness/scoring/scoring-spec.yaml`, with its schema and lint beside it: per coreset file, the terms (entity, primitive, `cause`, time window, aggregate, direction, weight) whose normalised shares (§9) the file's score sums — using §8–§10. All three write or read the one records shape of §5.

---

## 3. Inputs

**Trace** — the simulator's output, frozen in `../data-contracts.md` §9: JSONL, a `meta` header line, then seven event types. The reader streams plain or gzipped files, validates that every non-`x_` line is one of the seven types with the fields the contract names, ignores `x_`-prefixed lines wholesale, captures the header (`workload_id`, `condition`, `sim`), and refuses a trace whose task ids collide with a reserved entity name.

**Run file** — the simulator's input, the run-file view of the workload (`../data-contracts.md` §4): `workload_id` and `events`. The reader takes it as a second input for four facts the trace does not carry:

| fact | how it is read |
|---|---|
| `T_end` | the largest pinned time in the file: arrival times, pinned departs, and wake events |
| chain topology | a **chain** is the WAKE path starting at a task whose program contains a TIMER: the head, then each task the previous stage's WAKE targets, until a stage wakes no one (the tail). A TIMER task that wakes no one is a chain of length one. |
| `demand` | a task's total RUN work, summed over its program; defined only when the program has no unbounded LOOP |
| channels | each task's WAITs in program order, a LOOP's body repeated, with the **kind** of the channel each names: the channel's name before its colon (`input`, `timer`, `chain`, `job`, `children`); and, per task, the wake events on an `input` channel — its stimuli |

**Config schedule** — the daemon's input to the simulator (`../data-contracts.md` §7). The reader takes it as a third input for the one fact neither of the others carries: the **params** of each applied entry, looked up by the `index` the trace's `config_applied` line names. Only `switch_window` (§6.9) reads it, for a switch into MLFQ. The schedule's `t_us` is the daemon's stamp (`t_return`); the trace's `config_applied` time is the applied instant (`t_apply`), which is what every schedule row anchors on. When the schedule is not given, a switch into MLFQ produces a guard and no row; an applied entry the schedule lacks, or carries with another algorithm, is a guard.

Recognition primitives read the recognition log (`../data-contracts.md` §8), `ground_truth` from the canonical workload file, and the calibrated driver table (§10 of the same document).

---

## 4. Observation window

Every primitive is measured over `[0, T_end]`.

- An observation is emitted only if it completes inside the window: a `ready_wait` needs its `run_start` at or before `T_end`; a `job` needs its completion at or before `T_end`.
- CPU accounting is clipped at `T_end`: an occupancy still open there counts up to `T_end` only.
- A task alive at `T_end` is *not completed within the window*. It is never "completed late".
- Whether the simulator keeps running past `T_end` has no effect on any number.

---

## 5. Records

One CSV file per trace (or per recognition log), every row self-contained, twenty-six columns.

**Identity** — which run the row came from.

| column | meaning |
|---|---|
| `workload_id` | the workload |
| `condition` | the recognizer condition (`fixed`, `random`, `shipped_catalogue`, `strongest_name_table`, `llm_vocab`, `llm_algo`, `llm_full`, `oracle`; the two name-table conditions replaced `whitelist` on 2026-10-09, 9.12 D6 and 9.14 decision 7) |
| `table` | `prior` or `calibrated`; empty for `fixed`, which uses no table |
| `seed` | `random`'s PRNG seed; empty otherwise |
| `boot_default` | the id of the boot configuration the run started in; empty for the primary. Only the `fixed` runs of the RQ0 gate spec's sensitivity check carry one; the scorer pairs a run with the `fixed` run of the same `boot_default` (added 2026-09-11, 8.2) |
| `telemetry` | the telemetry shape the run's daemon showed the recognizer (data-contracts §5, rule 6): `focus`, the name → count multiset with the focus holder, or `names`, the multiset alone. An axis of every experiment, orthogonal to the condition: the scorer pairs a run with the `fixed` run of its own shape, the grader groups by it, and a `paired` grades row of one condition under its two shapes is the field's measured difference (added 2026-10-11, 9.17) |
| `sim` | the simulator version from the trace header; absent on recognition rows, which come from a log and not a trace, so the schema does not require it (8.4) |
| `source_sha256` | SHA-256 of the trace or log file the row was computed from |

**Observation** — one measurement.

| column | meaning |
|---|---|
| `entity` | whom it is about (§1) |
| `metric` | which primitive (§6, §7) |
| `t` | anchor time in µs (§6 names each primitive's anchor) |
| `value` | the measurement, an integer or 0/1 |

**Attributes** — nullable, filled only by the metrics named.

| column | filled by | meaning |
|---|---|---|
| `cause` | `ready_wait` | why the task became runnable: `arrive`, `wake`, `sleep_end`, `timer_tick`, `fork_slot` |
| `channel` | `ready_wait` with `cause = wake` | the kind of the channel the completed WAIT named (§6.1): `input`, `timer`, `chain`, `job`, `children` |
| `provenance` | `config_interval` | `unmodified`, `clamped`, `held`, `fallback` |
| `algorithm` | `config_interval`, `switch_window`, `boost_window` | `MLFQ`, `EDF`, `LOTTERY`, `FIFO` |
| `index` | `config_interval`, `switch_window`, `boost_window` | the schedule entry's index |
| `period_us` | `job` | the TIMER period; a miss is `value > period_us`, slack is `period_us − value` |
| `predicted` | `mode_correct`, `attr_correct`, `algo_choice_correct` | what the recognizer answered |
| `truth` | `mode_correct`, `attr_correct`, `algo_choice_correct` | the answer key's value |
| `validation` | every recognition row | what the validator did with the answer |
| `familiarity` | every recognition row | the covering segment's familiarity tier, when the segment carries one |
| `hogs` | `switch_window`, `boost_window` | the hog count H at the switch or the boost instant (§6.9, §6.10) |
| `pre_committed_miss` | every recognition row | 1 when the covering segment carries the `pre_committed_miss` annotation, 0 otherwise; the headline accuracy excludes those rows and the second report line includes them (added 2026-09-11, 8.4) |
| `skipped` | `job` | 1 when the tick was skipped under the TIMER skip rule (§6.2) — no work ran for it, it has no completion, so `value` is empty and the job counts as missed; 0 on a consumed tick's row (added 2026-10-09, 9.14) |
| `censored` | `input_latency` | 1 when the task never served the keystroke inside the window, so `value` is the lower bound from the keystroke to the task's end or `T_end`, whichever is first; 0 on a served keystroke's row (added 2026-10-30) |

**Rules.**

- **Row order**: by `entity`, then `metric`, then `t` (numeric), then `cause`, then `channel`. Files compare byte for byte.
- **Anchors**: window-level rows (`arrival`, `cpu_delivered`, `demand`, `preempt_count`, `busy`, and `completed` with value 0) sit at `T_end`; `completed` with value 1 and `turnaround` sit at the `task_end` time; every other primitive names its anchor below.
- **No aggregates, no derived flags.** `met` is not stored (it is `value ≤ period_us`); progress is not stored (it is `cpu_delivered / demand`).
- **Machine schema**: lands beside the code that writes the file, in the harness tree (`harness/records/schema/`), enforced by its tests. Records are not a data contract: only the harness writes and reads them.

---

## 6. Trace primitives

Each primitive states what it measures, which trace lines produce it, and what the row carries.

### 6.1 `ready_wait`

*How long a task waited for the CPU after it became runnable.*

One row per `ready` line inside the window. `t` = the `ready` time. `value` = the task's next `run_start` minus `t`; **zero when the `ready` falls inside the task's own occupancy** (at or after a `run_start` and before its `run_end`), which is how a blocking primitive that completed without blocking appears. A `ready` line followed by its task's next `ready` line at a later instant, with no `run_start` between, is a zero wait too: no RUN lay between the two, so the task went on to its next blocking primitive at once. `cause` carried on the row.

A `ready` line with `cause = wake` completes the task's next WAIT in program order (§11, items 1–2), so its row also carries that WAIT's `channel` kind, read from the run file (§3). A keystroke is `input`; a measured timer wake, a chain stage's hand-off, a job member's hand-off, and an orchestrator's wait for its children are `timer`, `chain`, `job`, and `children`. A wake line past the last WAIT of its task's program is a guard, and its row carries no channel.

The proposal's named metrics are filters and aggregates over it:

| name | filter / aggregate |
|---|---|
| interaction latency (per stimulus) | not a filter of `ready_wait`: the `input_latency` rows of the task the scoring spec names, each from a keystroke's wake event (§6.12) |
| response time (per task) | the row with `cause = arrive` |
| timer dispatch delay | rows with `cause = timer_tick` |
| starvation | a task's maximum `ready_wait` over the window, any cause — measured from `ready`, never from arrival: a task sleeping voluntarily is not starving |


### 6.2 `job`

*How long one periodic job took, from its tick to its completion — or that it was skipped.*

**Definition.** A TIMER task's ticks lie on the grid `t₀ + k·period`, `t₀` its first TIMER execution (§11, item 4). When the task reaches its TIMER it consumes the latest tick at or before that instant and **skips** every unconsumed tick before it (the TIMER skip rule, 9.11 D3; `../memos/2026-10-07-timer-skip-rule-for-the-simulator.md`). Job k starts when tick k is consumed and is due at tick k + period. For a **single-stage** task, job k completes when the task next reaches its TIMER — the end of that iteration's work. An iteration with no RUN — a TIMER directly after the TIMER — reaches it at once: the job completes when its tick is consumed, value 0, with no occupancy. For a **chain** (§3), frame k completes when the **tail** stage ends the iteration the consumption of tick k started; the head's own job boundary is not the frame. A skipped tick is a job that ran no work and has no completion: it missed.

One row per tick inside the window — consumed with its completion also inside it, or skipped by a consumption inside it. Entity = the chain head (for a single-stage task, the task itself). `t` = the tick. `value` = completion − tick on a consumed tick's row, empty on a skipped tick's. `period_us` and `skipped` (0 or 1) on the row.

**How it is computed.** Each `ready(cause = timer_tick)` line of the head marks the consumption of one tick: the latest grid tick at or before the line's time, the grid anchored at the head's first such line, which is at the task's arrival: the dataset lint makes a periodic task's first instruction its TIMER (the TIMER-first invariant), and the executor executes that leading TIMER in the task's arrival step, so tick 0 is the arrival and is consumed there without blocking, on a free lane or a busy one — the line is item 1's zero-wait `ready` (§11, items 1 and 4). A tick is consumed late whenever the lane was busy, so the line's time is never taken as the tick's. The ticks between two consecutive consumptions are the skipped ones. The j-th consumption is the tail's j-th iteration, because a skipped tick sends no wake down the chain and wakes queue with depth (§11): a stage's iteration ends at its `run_end` with reason `block`, `exit`, or `depart` — or, when the next iteration began without blocking, at the next `ready` line of that stage. Under the earlier backlog rule every overdue tick was run back to back and the k-th line was tick k; the rule decided for the simulator changed on 2026-10-07 and this reading with it (9.14). The reference simulator runs the skip rule since its stage Y (2026-10-23), item (b) of the RQ0 gate spec's simulator-conformance statement.

**Guard.** For every chain, the tail's iterations completed inside the window are no more than the head's ticks consumed inside it; more means a wake the head never sent. A shortfall is not a guard: an iteration still running at `T_end` is not completed within the window (§4), and a tick consumed shortly before `T_end` may leave its frame no time to finish (9.16 D3). Its weakness: a wake the simulator drops mid-run also leaves the tail short, and this guard no longer catches it. A consumption that does not advance the tick index is a guard too. For a length-one chain, the simulator's `deadline` lines are paired with the ticks in tick order — one line per tick, consumed or skipped, a skipped tick's written at the instant of the skip after the late job's own line — and each consumed tick's line must agree with the row (`t` = completion, `slack_us = period_us − value`), while a skipped tick's line must say `met: false`, read by `met` alone and not by the slack's sign (9.11 D17). `deadline` lines are never the source of a `job` row; for a chain longer than one they measure the head stage alone and are expected to differ from frame latency.

### 6.3 `cpu_delivered`

*How much CPU the task received in the window.* The sum of the task's occupancy intervals (`run_start` to `run_end`), clipped at `T_end`. One row per task, at `T_end`.

### 6.4 `demand`

*How much CPU the task needed.* The task's total RUN work read from the run file. One row per task whose program has no unbounded LOOP, at `T_end`. Progress, `cpu_delivered / demand`, is scoring's.

### 6.5 `completed`

*Did the task finish inside the window.* 1 with `t` = the time of a `task_end` with reason `exit` at or before `T_end`; otherwise 0 at `T_end`. A segment-bound task ends by `depart`, so its row is always 0.

### 6.6 `turnaround`

*From arrival to completion.* Only when `completed` is 1: `task_end` time minus `task_arrive` time, at the `task_end` time. A spawned child's arrival is its `task_arrive(source = spawn)` line, an emergent time. An orchestrator's turnaround is the build's makespan, since it exits only after its children.

The arrival is a row of its own, `arrival`: one per task, at `T_end`, `value` = the time of the task's `task_arrive` line. §9's censored bound reads it. Added 2026-10-17 (9.15).

### 6.7 `preempt_count`

*How often the task was forced off the CPU.* The count of the task's `run_end` lines with reason `preempt` inside the window. One row per task, at `T_end`.

### 6.8 `config_interval`

*How long each configuration was in force.* One row per `config_applied` line, entity `schedule`, `t` = the applied time, `value` = time until the next `config_applied` or `T_end`, with `provenance`, `algorithm`, `index`. Two entries at the same instant give the earlier a value of 0. Provenance shares (time-weighted and count-weighted), config age, and the fallback share are aggregates over these rows.

### 6.9 `switch_window`

*How long, after a switch into MLFQ, the scheduler was re-learning who is batch.* From the 2026-09-08 memo on algorithm-switch semantics (`../memos/2026-09-08-algorithm-switch-semantics-for-the-simulator.md` §4): a cold start into MLFQ puts every task in the top queue, the state MLFQ's own boost produces, so a switch is one extra boost and is measured in those units. The simulator does so since 2026-10-10: on a switch into MLFQ, `Mlfq::start()` resets every task's level and allotment, so a switch MLFQ → FIFO → MLFQ starts every task in the top queue (its rule U1, `../../simulator/memo/memo_261010.md` Part B; the RQ0 gate spec's simulator-conformance item (c)).

One row per `config_applied` line inside the window whose algorithm differs from the previous applied entry's; the boot entry has no predecessor and never produces a row, and an entry that changes only params or the cap is not a switch (it applies with queue levels kept, at its stamped time unless it waits behind a draining switch, §11 item 9). Entity `schedule`, `t` = the applied time (`t_apply`), with `algorithm` (incoming), `index`, and `hogs` on the row.

- **`W_single`** is the CPU a CPU-bound task must receive to fall from the top queue to the bottom, one full slice per upper level: `timeslice_us · Σ_{l=0}^{num_queues−2} timeslice_growth^l`, rounded down to whole µs, from the **incoming** entry's params in the config schedule (30 000 µs at the boot default since 2026-09-11: 10 000 · (1 + 2); 6 000 µs under the former 2 ms slice). No parameter is ever inferred from behaviour.
- **`H`**, the hog count, is behavioural: a task alive at `t_apply` (arrived at or before it, not ended at or before it) whose first `run_end` after `t_apply`, at or before `T_end`, has reason `preempt`. Known bias: a task preempted by a wake into a higher queue is counted too. `hogs` carries H for every switch row, including the zero-valued ones.
- **`value`** for a switch into MLFQ is the length of the window `[t_apply, t_close]`, where `t_close` is the instant the **last** counted hog has received `W_single` of CPU since `t_apply`, summed from its occupancy intervals (the sum `cpu_delivered` takes, started at `t_apply`). The window is therefore sized in lane time: other tasks holding the lane stretch it rather than escape it. If a hog has not received `W_single` by the next algorithm switch or by `T_end`, the window is clipped there and a guard names the hog. With no hogs the value is 0. For a switch into EDF, LOTTERY, or FIFO the value is 0: nothing those algorithms need is discarded (deadlines come from the process model, tickets from the config, arrival order is always known).

What the window can still miss — a hog boosted before it reaches the bottom, a hog the preempt rule did not count — is what the `x_mlfq_level` check (§12) measures.

### 6.10 `boost_window`

*How long, after each boost inside an MLFQ interval entered by a switch, the scheduler was re-learning who is batch.* The boost variant of §6.9, so the §8 excess aggregates can tell a switch's cost from an ordinary boost's. The boost timer restarts at every applied MLFQ entry of the interval — at `t_apply` (§11 item 7) and at each same-algorithm entry after it (§11 item 9) — so the boost instants are `t_e + k · boost_interval_us` (k ≥ 1), `t_e` the applied time of the latest applied entry and `boost_interval_us` from its params, before the next entry applies. One row per boost instant that falls before the interval's end (the next algorithm switch or `T_end`). Entity `schedule`, `t` = the boost instant, with `algorithm` (`MLFQ`), `index` (the entry whose grid the instant is on), and `hogs`. `value` is the window's length by the §6.9 rule from that instant, `W_single` from that entry's params — H counted there, closing when the last counted hog has received `W_single` of CPU since it — clipped at the next boost instant or the interval's end without a guard, since a boost window running into the next boost is the normal case, not a hog escaping. With no hogs the value is 0. Added 2026-09-11 (8.10); the grid restarts at a same-algorithm entry since 2026-10-17 (9.15).

### 6.11 `busy`

*How long the lane was occupied.* The sum of every task's clipped occupancy, entity `lane`, one row at `T_end`. Idle is `T_end − busy`; utilisation is `busy / T_end`.

### 6.12 `input_latency`

*How long each keystroke took to be served, from the keystroke itself.*

One row per input wake event of the run file — a keystroke — on its target task. `t` = the keystroke's wake time. The task's k-th `ready(cause = wake)` line on an input channel completes the WAIT the k-th keystroke serves, wakes queuing with depth (§11, item 2); `value` = the start of that service — the line's `run_start`, or the line's own time when it falls inside the task's occupancy or a zero wait (§6.1) — minus the wake time, `censored` 0. A keystroke the task never serves inside the window — still queued at its depart, or its line still waiting for the lane at `T_end` — has a row too: `value` = the task's end or `T_end`, whichever is first, minus the wake time, a lower bound, `censored` 1. A keystroke at or after its task's end has no row.

`ready_wait` measures from the `ready` line, the instant the task reached the WAIT: a keystroke that queued while the task was behind in its program shows there as a zero wait. `input_latency` counts that queueing, as `T_interaction`'s grounding measures, from the key to its echo (§10). A served keystroke's line before its wake time is a guard. Added 2026-10-30 (`../../simulator/memo/memo_261023.md` Part H2).

### 6.13 Summary

| metric | entity | rows | from the trace | from the run file | anchor `t` |
|---|---|---|---|---|---|
| `ready_wait` | task | per `ready` | `ready` → next `run_start`, or inside own occupancy | — | ready time |
| `input_latency` | task | per keystroke | the k-th input `ready` line's service start; the task's end | input wake events | wake time |
| `job` | chain head | per tick | head ticks, stage iteration ends | chain topology | tick |
| `cpu_delivered` | task | 1 | occupancy intervals, clipped | `T_end` | `T_end` |
| `demand` | task | 0 or 1 | — | RUN total (finite only) | `T_end` |
| `completed` | task | 1 | `task_end(exit)` inside window | `T_end` | end time or `T_end` |
| `turnaround` | task | 0 or 1 | `task_arrive` → `task_end(exit)` | — | end time |
| `arrival` | task | 1 | `task_arrive` | `T_end` | `T_end` |
| `preempt_count` | task | 1 | `run_end(preempt)` count | — | `T_end` |
| `config_interval` | `schedule` | per entry | `config_applied` → next | `T_end` | applied time |
| `switch_window` | `schedule` | per algorithm change | `config_applied`, first `run_end` per alive task, the hogs' occupancy after it | `W_single` from params by `index` (config schedule) | applied time |
| `boost_window` | `schedule` | per boost instant inside an MLFQ interval entered by a switch | the boost grid from each applied MLFQ entry of the interval, first `run_end` per alive task, the hogs' occupancy after it | `boost_interval_us` and `W_single` from params by `index` (config schedule) | boost instant |
| `busy` | `lane` | 1 | all occupancy, clipped | `T_end` | `T_end` |

---

## 7. Recognition primitives

*Rows graded from the recognition log against `ground_truth`. No simulator is involved.*

**Grading scope.** A log entry is graded when a `ground_truth` segment with a mode other than `ambiguous` covers its `t_set_change`. The terminal snapshot (telemetry rule 4) has no covering segment and is skipped; `ambiguous` segments are excluded by `../recognition-vocabulary.md` §1.

Per graded entry, entity `recognizer`, `t` = `t_set_change`, every row carrying `validation` and, when the covering segment has one, `familiarity`:

| metric | value | `predicted` / `truth` |
|---|---|---|
| `mode_correct` | 1 if `proposal.system.mode` equals the segment's mode, else 0 | the two modes |
| `attr_correct` | 1 if `proposal.system.background_wanted` equals the segment's attribute, else 0 | the two booleans |
| `latency_us` | the entry's `latency_us` | — |
| `algo_choice_correct` | `llm_algo` only: 1 if the named algorithm equals the calibrated table's default algorithm for the true row `(mode, background_wanted)`, else 0 | the two algorithms |
| `config_correct` | 1 if the configuration composed from the *predicted* row `(mode, background_wanted)` is identical to the one composed from the true row — algorithm, params and cap together, canonical bytes — else 0. Composed from the table the run itself used, named in the row's `table` column, which is not necessarily the calibrated one (added 2026-09-11, 8.4) | — |

An entry whose `proposal` is `null` (unparseable answer) grades `mode_correct` and `attr_correct` as 0 with an empty `predicted`. A predicted mode outside the sixteen-mode menu, or a named algorithm outside the four, is likewise graded 0 with the answer recorded verbatim in `predicted`, so the confusion matrix shows where it went; a *ground-truth* mode outside the menu is refused rather than graded, because a malformed answer key is a broken input and not a result. A row whose prediction names no legal `(mode, background_wanted)` pair grades `config_correct` 0.

**The pre-committed-miss exclusion.** A segment annotated `pre_committed_miss` carries a label no recognizer can reach from names and behaviour (`../recognition-vocabulary.md` §1). Its entries are graded like any other and marked with the `pre_committed_miss` column (§5); the headline accuracy excludes them and the same figure including them is a second reported line (Phase 8 spec, decision 13). The per-experiment spec's exclusion list is derived from the same annotation and linted against it, never authoritative.

Mode accuracy, attribute accuracy, the two confusion matrices, algorithm-choice accuracy and its four-class confusion, and latency to a correct answer are aggregates (§8). Run-to-run consistency and distractor robustness are aggregates over several graded samples of one query point; they need a repeat index the log envelope does not yet carry (see the memo to the daemon's owner, `../memos/2026-09-07-repeat-samples-for-the-daemon.md`).

---

## 8. Aggregates

A fixed list, computed from records at scoring time, always per workload, condition, table, and seed, and per entity where the primitive is per task. A scoring spec may restrict rows to a time window by `t` before aggregating; primitives never do.

| over | aggregate |
|---|---|
| `ready_wait` rows (a filter by `cause` — for `cause = wake` also by `channel` — and entity applied first) | count; mean; P50; P95; P99; max; **`over_threshold`** — the fraction of rows with `value > T_interaction` (§10) |
| `input_latency` rows (entity applied first) | count; **`censored_count`** — the rows with `censored` 1; mean; P50; P95; P99; max; **`over_threshold`** — the fraction of rows with `value > T_interaction` (§10). A censored row enters as its lower bound |
| `job` rows | count; **miss rate** — the fraction with `value > period_us`; latency P50; latency P99 |
| `cpu_delivered`, `demand` | **progress** — `cpu_delivered / demand` |
| `completed`, `turnaround` | completion (0/1); turnaround as is |
| `preempt_count` | as is; summed over tasks for the lane |
| `config_interval` rows | time-weighted share per `provenance`; count share per `provenance`; **fallback share** (time-weighted `fallback` + `held`); config age — the distribution of `value` |
| `switch_window` rows with `ready_wait` rows | **per-switch excess** — for each switch into MLFQ, the mean of the `ready_wait(cause = wake, channel = input)` values of the scoring spec's interactive task inside the switch window `[t, t + value]`, minus the mean of the same task's rows in the rest of that config interval outside any window, in µs; the **boost variant** takes the same excess over the boost windows of that interval, one at each instant `t + k · boost_interval_us` (k ≥ 1), each sized by the §6.9 rule from that instant (H counted there, closing when the last hog has its `W_single`) and clipped at the next boost; switch excess ≈ boost excess means the switch cost one boost, the difference above it is backlog carried from the outgoing algorithm. **Share inside switch windows** — Σ `value`, each clipped at `T_end`, over `T_end`. Neither is weighted in any score; both are reported beside it |
| `config_interval` rows with the config schedule, the recognition log and the run's graded queries | **flip count and cost** (9.21; read by the hold-time plan's no-rule measurement, its step 1) — `change_count`, the applied entries whose algorithm, params or cap differ from the entry before them (an entry stamped at or after `T_end` is ignored, data-contracts §7); `wrong_change_count`, those whose query the grader marked `config_correct` 0 (one query yields one schedule entry, so entry k is query k − 1's; a query without a `config_correct` row — ungraded, or no driver table — never counts as wrong); `wrong_switch_excess_sum`, the per-switch excess (the row above) summed over the wrong changes that were switches into MLFQ, where the excess is defined. Emitted for a recognizing run only; `fixed` consults no recognizer. The `flip_cost` reporting line prints them per run beside the file's score. Neither is weighted in any score |
| `busy` | utilisation `busy / T_end`; idle `T_end − busy` |
| recognition rows | the grader's, not the aggregates module's (§7; 8.4), and they land in the `grades` file (`harness/grades/schema/`) rather than here: raw accuracy beside its **measured** majority baseline on every axis; **balanced accuracy** and the **Matthews correlation coefficient** on the binary attribute only; the confusion matrix over (`truth`, `predicted`) and per-class recall on mode and on algorithm choice; the configuration-correct rate and the share of errors that changed the configuration; latency P50/P99 over rows with `mode_correct = 1`. The familiarity tier rides on the row as a split key and **no per-tier aggregate is defined**: at the current core set each annotated tier (4 and 5) carries one graded query point and tiers 1 to 3 have none, so what the tiers demonstrate belongs to its own experiment |

**Which statistic goes on which axis is decided, not free.** Balanced accuracy is defined for two classes (`brodersen-icpr10`, which defines it off a two-by-two matrix and gives no K-class form), and it earns its place where a degenerate answer would otherwise score well. Measured on the rebuilt core set the RQ0 gate spec pins, a constant answer scores 75.3 per cent on the attribute (58 of the 77 graded points are `true`; 79.4 per cent over the 68 headline points) and 14.3 per cent on mode (11 of 77, `gaming`; 16.2 per cent over the headline points), because the core set instances all thirty-two cells (on the Phase 7 set, 2026-09-11: 69.5 and 11.0 per cent). So the attribute is corrected and mode is not: mode and algorithm choice report raw accuracy against the measured baseline with the confusion matrix and per-class recall, and **no macro-average is computed on any axis**. The Matthews correlation coefficient (`chicco-bmcg20`) sits beside balanced accuracy on the attribute, computed over the points whose prediction names one of the two classes, so its count is its own; a null answer still costs recall. When a whole row or column of the confusion matrix is zero the formula is undefined (`chicco-bmcg20`: "MCC is undefined when a whole row or column of M is zero"); Chicco and Jurman derive values for those cases — 1 or −1 when only one cell is non-zero, otherwise 0 as a limit — and the grader instead reports the coefficient as undefined, by design.

**Seeds.** A seed is a repetition of the same question, not a new question, so each statistic is computed per seed and then averaged, exactly as §9's rule does for Layer 2, and both readings are kept: the `grades` file's `over_seeds` column is 0 on one seed's own value and 1 on the mean, which leaves `seed` empty and records `n_seeds`. The sample count stays the per-seed count. Pooling the seeds instead would multiply the observation count while the query points stayed the same, and return intervals that are too narrow. Rates average this way; raw confusion cell counts do not, because averaging counts gives fractional cells, so those are emitted per seed only. Paired comparisons run between distinct conditions, on seed-averaged values.

**Intervals and comparisons.** Query points inside one workload file share its process names and its situation, so they are not independent observations. Every interval therefore comes from a **cluster bootstrap that resamples workload files**, not query points (`field-jrssb07`: for clusters of equal size, the variance estimates are consistent as the number of clusters grows with their size fixed; in its simulations at 5 and at 15 clusters of 4 the cluster bootstrap "consistently underestimates the bootstrap variance for all the statistics", the authors noting "we are essentially working with five and 15 observations"; the coreset's files are more than 15 and of unequal size, outside both the theory and the simulations, so whether an interval reaches its nominal level is untested and it may be narrower). Condition comparisons are computed **paired**, on the same drawn files, because every condition is graded on identical query points (`dietterich-neco98`, which names this case and rules out both a difference of two proportions and a resampled t test). Determinism here means reproducibility: the seed and the repetition count are constants (§10), so a rerun gives byte-identical bounds.

Percentiles are computed on the raw values with linear interpolation, a convention: position `(n − 1) · p / 100` on the sorted values, interpolating between the two neighbours, computed exactly on the integer records. Mean is reported for sanity only, never as a headline. Counts (stimuli per task, ticks per chain) are guard inputs: the stimulus guard fails a task with more input-channel wake lines than the run file's input wake events, or one that ends blocked on an input WAIT while an input wake sent to it before its end went unconsumed — a lost wake; a task that ends with input it has not reached is not a message, the task behind its program; tick count against the window's tick grid. The guards themselves — the eight checks, their thresholds, and the grounding behind each — are the guard spec, `../../harness/guards/guard-spec.yaml` (8.3), read by `harness/tools/harness/guards.py` into a `guards` file beside `aggregates` and `scores`. The `config_age` aggregates above measure time in force and are reported; the config-age guard measures something else, whether an entry took effect before the ground-truth segment its query was observed in had ended.

---

## 9. Normalisation and floors

**Formula.** For one workload and one aggregate `A`, a condition's **share of headroom captured** is

```
share = improvement(condition) / improvement(oracle)
improvement(c) = fixed_A − c_A        when lower A is better
               = c_A − fixed_A        when higher A is better
```

with `fixed` and `oracle` the same workload under the same table. The rule applies **per aggregate**, so every share is unit-free before any weighting; weights are the scoring spec's. Values are shown as computed: negative when a condition scored worse than `fixed`, above 1 when it beat the oracle; never clipped.

**Floor.** Each aggregate has an absolute floor in its own units (§10). When `|improvement(oracle)|` is below the floor, the share is **undefined** for that workload and aggregate: the raw values are reported with the mark *no headroom*, and no ratio is formed.

**Composition.** A file's score is the scoring spec's weighted sum of its terms' shares. A term marked *no headroom* keeps its weight and enters the sum as if the condition had captured all of the headroom (share 1), so it never makes a file easier to pass; the mark is carried on the term (Phase 8 spec, decision 4; 8.2). A `turnaround` term whose task did not complete inside the window has no `turnaround` row (§6.6); it is scored on the censored lower bound `T_end − arrival`, the row marked *censored*, so not finishing is worse than every finishing value (8.2 spec, decision 4). An `input_latency` term's aggregate carries its censored keystrokes at their lower bounds, and the term is marked *censored* when its window holds one. A term whose filter selects no rows stops the scorer: every scored entity is linted to exist, so an empty filter is a scoring-spec mistake. The `aggregates` file carries twelve decimal places and the `scores` file six, so a six-place share is exact to its last digit (`harness/aggregates/schema/`, `harness/scores/schema/`).

**Sensitivity.** `fixed` is the boot default, whose values are OSTEP's worked examples' for MLFQ and design for EDF and LOTTERY (`../recognition-vocabulary.md` §2). The RQ0 gate spec pre-registers `fixed` under a sweep of ten alternative boot defaults — the top slice at 0.5, 0.7, 0.9, 1.2, 2, 3, 5, 14, 20 and 100 ms; where the sign or ordering of a share moves, the floor is reported as a range. That reporting rule is the RQ0 gate spec's (Phase 8); the formula here does not change.

---

## 10. Constants

| constant | value | status |
|---|---|---|
| `T_interaction` — the interaction-latency threshold | **100 000 µs** (0.1 s) | design: the strict end of a guideline's range (`miller-fjcc68`), cross-checked against a measured detection threshold (`deber-chi15`); see below |
| floor for latency-type aggregates (`ready_wait` and `input_latency` mean/P50/P95/P99/max; `job` latency P50/P99; `turnaround`) | **1 000 µs** | design, tied to no scheduler parameter (2026-09-11): one millisecond, below which a latency difference between two configurations is not read; the RQ0 gate spec pre-registers a floor-sensitivity line, the verdict recomputed under a band of floors at scoring time |
| floor for fraction-type aggregates (`over_threshold`, miss rate, progress, completion) | **0.01** | design: one percentage point |
| counts, provenance shares, utilisation | not normalised | guard and sanity inputs only; the guards' thresholds are the guard spec's (`../../harness/guards/guard-spec.yaml`), each an identity, a structural rule, or a design value |
| cluster-bootstrap seed; repetitions (§8) | **20260911**; **10 000** | design, pinned, not estimated: a fixed seed makes an interval byte-identical on a rerun, so the harness keeps its own determinism rule. Both are pinned in the grader (`harness/tools/harness/grader.py:69–70`) |
| interval level (§8) | **95 per cent** | convention |

**`T_interaction` = 0.1 s.** Miller (1968), Topic 1, "Response to control activation", gives two delays. The indication that a key, switch or other control member "has been physically activated" — "the click of the typewriter key" — "should be immediate and perceived as a part of the mechanical action induced by the operator. Time delay: No more than 0.1 second"; for the echo of typed text, "the delay between depressing the key and the visual feedback should be no more than 0.1 to 0.2 seconds", with the caveat that "this delay in feedback may be far too slow for skilled keyboard users". The constant reads a keystroke's response, the second statement's object, measured as Miller's is from the key: `input_latency` (§6.12); 0.1 s is the strict end of its range, taken by design on Miller's caveat on skilled typists. The values are a guideline, not a measurement: Miller calls his delays "the best calculated guesses by the author", to be accepted "as indicative rather than conclusive", tests no subjects and cites no source for 0.1 s. Nielsen (1993), *Usability Engineering* ch. 5, restates it — "0.1 second is about the limit for having the user feel that the system is reacting instantaneously" — citing Miller 1968 and Card et al. 1991, so it is not a second grounding. The measured cross-check is Deber et al. (2015): latency just-noticeable differences of 69 ms for tapping a touchscreen and 96 ms for tapping a touchpad-like indirect surface (12 tapping sessions, run by 14 participants with the dragging sessions); the authors place key typing among the indirect tapping tasks behind the 100 ms textbook value, which falls within their 95 % confidence interval. No measurement of keyboard echo is known to this project; every input wake in the dataset is a keystroke. Shneiderman (1984) reports Long's 1976 study of "delays of approximately 0.1-0.5 second in the time for a keystroke to produce a character on an impact printer": typists "worked more slowly and made more errors with longer response times", and "even these brief delays were distracting" — a trend within that range, not a slowdown measured at 0.1 s; the percentile aggregates carry what the fraction discards. The constant is read on `ready_wait` rows with `cause = wake` and `channel = input`, the keystrokes; the harness emits the fraction on every filter. A `ready_wait` is only the scheduler's share of a keystroke's response — ready to the next `run_start` — while every source above bounds the whole delay from key to feedback, so `over_threshold` is a lower bound on the share of keystrokes answered later than 0.1 s.

Floors are design values and may be revised by the RQ0 gate spec with a changelog entry here.

---

## 11. Simulator assumptions

The definitions above, and the mock traces that test them, assume the following simulator behaviour. Items 1–3 are the trace contract's clarifications (`../memos/2026-09-07-trace-clarifications-for-the-simulator.md`); item 4 is the simulator's own reading, pinned here; item 5 is the reference simulator's behaviour, which the mocks follow; item 6 is a mock-local choice that fills a gap the contracts leave open. The simulator's state is its owner's record (`../../simulator/src/notes.md` §4, `../../simulator/memo/memo_261001.md`, `../../simulator/memo/memo_261010.md`). A different decision on any of them changes the mocks deliberately, not the definitions.

1. A `ready` line is emitted at **every completion of a blocking primitive** (`WAIT`, `TIMER`, `SLEEP`, fork slot), at zero wait when it did not block; inside an occupancy it appears after the `run_start` and pairs with wait 0. The simulator does so since its stage X (2026-10-23; `../../simulator/memo/memo_261023.md` Part B): a WAIT met from the mailbox and a TIMER consuming a passed tick write their line at that instant, inside the holder's occupancy, and RUNs joined without a block are one occupancy, marked by the simulator's `x_run_cont` line, which the harness ignores by the `x_` rule. A FORK that takes a free slot completes its fork-slot wait without blocking and is owed its zero-wait `ready(cause = fork_slot)` line (decided 2026-10-30; `../../simulator/memo/memo_261023.md` Part H). It is item (a) of the RQ0 gate spec's simulator-conformance statement (9.14 decision 1), since §6.2's reading of the TIMER skip rule rests on it.
2. **Wakes queue with depth**: two wakes sent to a busy task complete its next two WAITs, so iteration k of every chain stage is tick k. The simulator implements it: a wake with no waiter goes to a mailbox, never lost (notes, step M).
3. Same-instant events follow a **written, deterministic tie-break**; the mocks apply config entries first in list order, then arrivals in file order. The simulator applies config entries first, then events in insertion order (its rule D1; memo_261001 §6).
4. TIMER's `t₀` is the task's first TIMER execution, as the simulator sets it (its decision D4), and that execution is the task's arrival. Every periodic task's first executed instruction is its TIMER — the dataset lint enforces it since 9.13 — and the executor executes that leading TIMER in the task's arrival step, without the lane (the simulator's `on_arrive`; a spawned child's in the FORK that creates it), so tick 0 is consumed at the arrival without blocking, on a free lane or a busy one (9.11 D11; decided 2026-10-16 in 9.15, in place of 9.14 decision 1's first dispatch). The harness reads `t₀` off the trace as the time of the task's first `ready(cause = timer_tick)` line, which item 1's zero-wait line puts at the arrival. The mocks do the same: `mock-media`'s music player, first dispatched at 6 667 µs behind the video player, has its grid anchored at its arrival (re-derived 2026-10-17 in 9.15).
5. A task whose first instruction is a WAIT — a LOOP's body counting, a spawned child included — blocks in its arrival step when no wake is already stored for it (item 2), with no `ready` line and no occupancy: the executor's arrival step executes the task's leading instructions without the lane, and the WAIT blocks there (the simulator's `on_arrive`; a spawned child's in `spawn`). Such a task has no `cause = arrive` row at its arrival (§6.1); if it is woken and the instructions after that WAIT reach a RUN without blocking or ending it, its first `ready` line is the wake that completes that WAIT. §9's censored bound reads its arrival off its `arrival` row (§6.6), the `task_arrive` line's time. A wake already stored for it completes the WAIT at once and the arrival step goes on: a RUN next gives the task its `ready(cause = arrive)` line at its arrival, as for any other task. The mocks do the same (decided 2026-10-17 in 9.15, in place of their zero-length occupancy at the arrival). Since `mock-simulator@2` the mock simulator stores a wake sent to a task before its arrival — for its target, whatever its channel — and a WAIT-first task completes its WAIT on it in the arrival step; the mock also writes item 1's zero-wait `ready(cause = wake)` line for that WAIT beside `ready(cause = arrive)`, as the simulator does since its stage X. No fixture has a wake before its target's arrival.
6. The simulator keeps emitting `deadline` lines as the contract says; the harness uses them only as the §6.2 cross-check.
7. **The boost timer restarts at `t_apply`** after a switch into MLFQ, so the boost grid of §8 is `t_apply + k · boost_interval_us`. Confirmed with 인경민 on 2026-09-09 (memo §5, §7).
8. A switch out of FIFO applies immediately and the running task is treated as freshly dispatched by the incoming algorithm (the memo's rule (a)). A switch out of any other algorithm stamped while a task holds the lane applies the next time the lane is free — when that task's slice or current RUN ends, or it is preempted or departs (the drain); on a free lane it applies at its stamped time. Confirmed with 인경민 on 2026-09-09; the drain's end, the lane falling free in place of the running task's slice boundary, is the simulator's (its owner's U3: `on_config_apply` queues the switch, `dispatch` applies it once the lane is free), decided 2026-10-17 in 9.15 (`../data-contracts.md` §7, **Drain**). The primitives read the applied instant off the trace either way.
9. **An entry with the same algorithm is not a switch.** It has no drain of its own: it applies at its stamped time unless it waits behind a draining switch (below), queue levels kept; the running task finishes the slice it was granted and the new params govern from its next dispatch; the cap takes effect at once. Confirmed with 인경민 on 2026-09-09 (memo §7). The simulator does so since 2026-10-10 (its rule U2, `../../simulator/memo/memo_261010.md` Part B; the RQ0 gate spec's simulator-conformance item (c)), and reads the cap since its stage V (2026-10-20, item (d)): the running task keeps the slice end it was granted, the queue order is kept, MLFQ levels are clamped to a smaller `num_queues`, and a task whose allotment exceeds a shrunken slice is demoted when next picked. Entries apply in index order: one stamped while a switch is still draining (item 8) waits behind it and applies after it, at the drained instant. Under MLFQ the boost timer restarts at the entry's applied time, so §6.10's grid restarts there. Both are the simulator's (its owner's U3, and `Mlfq::start` arming the boost at every applied entry, memo_261010 Part B), decided 2026-10-17 in 9.15.

---

## 12. Mock fixtures

`harness/tools/tests/fixtures/` holds five hand-written pairs (run file, trace) with hand-computed expected records and a worked derivation each, plus `mock-scores` (8.2): hand-written records for one small workload under `fixed`, `oracle`, `random` × 2 seeds, and `fixed` under an alternative boot default, with the expected `aggregates` and `scores` files and a worked derivation, shaped to hit every scorer rule of §9. The five pairs: `mock-office` (queued keystrokes, an unfocused task), `mock-media` (a TIMER task passing two ticks in one stall, one of them skipped under §6.2's reading; a same-instant config pair that is also a switch into FIFO, a completing batch task), `mock-p1a` (config change without an algorithm switch, preemptions, a batch task clipped at `T_end`), `mock-chain` (a three-stage frame pipeline with one late frame), `mock-switch` (MLFQ → FIFO → MLFQ with a config schedule, two hogs — the batch task and the editor, each counted by its first preempt after the switch — the §8 excess aggregates worked by hand). `mock-media` and `mock-chain` run FIFO under an oracle entry stamped beside the boot entry, so their stated scheduler and their config lines agree. They are the tests of §6 and the seeds of Phase 8's mock simulator. Beside them, `mock-guards` (8.3) is a sixth pair, for the guards, `mock-grades` (8.4) and `mock-experiment` (8.7) are the grader's and the RQ0 gate evaluator's fixtures, and `fix-object` and `fix-tree` are the reference simulator's evidence for the RQ0 gate spec's conformance item (i), each a compiled workload with the simulator's `reference-trace.jsonl` and no `trace.jsonl`, so no harness test reads them; the fixtures' README (`harness/tools/tests/fixtures/README.md`) describes each.

**`x_mlfq_level` check.** The simulator is to emit `x_mlfq_level` `{t, task, from, to}` on every MLFQ demotion and boost (the 2026-09-08 memo, §6); the harness ignores it by the `x_` rule. The simulator does not yet: it emits `x_mlfq_demote` `{t, task}` and `x_mlfq_boost` `{t}`, without levels — owed, its owner's record (memo_261010 Part D, D4). `harness/tools/check_mlfq_levels.py`, beside the harness and not part of it, reads those lines and reports, per switch into MLFQ, whether the window covered each hog's last demotion (the run of demotions after `t_apply`, ending at the next boost or the bottom queue). A systematic miss is the evidence for proposing a field in the closed trace set; until then the trace contract stays frozen. On `mock-switch` the check passes at the window's edge; under the memo's original wall-clock window it failed there, which is what led to the lane-time definition (memo §7).

---

## 13. Changelog

- **2026-10-30 — interaction latency from the keystroke: `input_latency`; the records' twenty-sixth column (jioh).** A new primitive, `input_latency` (§6.12): one row per keystroke at its wake event, value the start of the service of the WAIT it completes minus the wake time, a keystroke never served inside the window censored at its task's end or `T_end`, marked in a new records column, `censored` (§5). Interaction latency is its rows, not `ready_wait` filtered to the input channel (§6.1), which measured from the `ready` line and read a keystroke queued while its task was behind as a zero wait. §8: its aggregates, with `censored_count`; §9: a term over it is marked *censored* when its window holds a censored keystroke; §10: the latency floor covers it, and `T_interaction` reads it. `ready_wait` and every aggregate over it are unchanged, the per-switch excess included. The scoring spec's 24 input-channel terms read `input_latency` (`../../simulator/memo/memo_261023.md` Part H2; `harness/CHANGELOG.md`, 2026-10-30).
- **2026-10-30 — the stimulus guard reads a lost wake; an iteration with no RUN (jioh).** No aggregate, constant, floor or records column changed. §8: the stimulus guard fails a task with more input-channel wake lines than the run file's input wake events, or one that ends blocked on an input WAIT while an input wake sent to it before its end went unconsumed — a lost wake; a task that ends with input it has not reached is not a message, in place of requiring the input-channel wake rows to equal the input wake events (`../../simulator/memo/memo_261023.md` Part H2). §6.1: a `ready` line followed by its task's next one at a later instant with no `run_start` between is a zero wait; §6.2: an iteration with no RUN completes when its tick is consumed, value 0 (Part H6). The primitives follow; guard spec 1.3 states the stimulus rule (`harness/CHANGELOG.md`, 2026-10-30).
- **2026-10-30 — the simulator's conformance as it stands (jioh).** No primitive, aggregate, constant, floor or records column changed, and no harness computation. §6.2 and §11 items 1, 5 and 9 now state as the reference simulator's behaviour what they stated as owed: the zero-wait `ready` line, written inside the holder's occupancy, RUN→RUN being one occupancy (its stage X, 2026-10-23; the RQ0 gate spec's simulator-conformance item (a)), owed for a FORK that takes a free slot; the TIMER skip rule (its stage Y, 2026-10-23; item (b)); and the cap read (its stage V, 2026-10-20; item (d)). §12 names `fix-object` and `fix-tree`, item (i)'s evidence (`harness/CHANGELOG.md`, 2026-10-30).
- **2026-10-17 — the chain guard allows a tail short at `T_end` (jioh 9.16).** No primitive, aggregate, constant, floor or records column changed. §6.2's chain guard fails only when a chain's tail completed more iterations inside the window than its head consumed ticks there, in place of requiring the two counts equal: an iteration still running at `T_end` is not completed within the window (§4), and a frame whose tick is consumed shortly before `T_end` cannot finish — on `c7-gaming` the last consumed tick lies 1,139 µs before `T_end` and a frame needs 14,999 µs, so under the equal-count rule every run failed the `tick_count` guard and the RQ0 verdict came out invalid. The stated weakness: a wake the simulator drops mid-run is no longer caught by this guard. `harness/tools/harness/primitives.py` follows; the guard spec's `tick_count` grounding states the same (`harness/CHANGELOG.md`, 2026-10-17).
- **2026-10-17 — the arrival row; the boost grid at a same-algorithm entry; entries in index order; the drain until the lane is free; the stored wake (jioh 9.15).** Records gain a primitive, `arrival` (§6.6): one row per task at `T_end`, its value the time of the task's `task_arrive` line. The censored turnaround (§9) reads the arrival off it in place of the task's `cause = arrive` row, so a task whose first instruction is a WAIT (§11 item 5) keeps its bound; for every other task the value is the same. §6.10: the boost timer restarts at every applied MLFQ entry of the interval, a same-algorithm one included, so after such an entry the boost instants are its applied time plus multiples of its `boost_interval_us` and the windows are sized with its `W_single`, in place of the switch's grid through the whole interval. §11 item 9 states as rules the two simulator behaviours it listed as differences: entries apply in index order, one stamped during a drain waiting behind it, and the boost timer restarts at a same-algorithm entry. §11's opening states item 5 as the reference simulator's behaviour the mocks follow, and item 4 that `mock-media`'s music player is anchored at its arrival. §11 item 8 states the drain as data-contracts §7's **Drain** rule and the simulator have it: a switch out of MLFQ, EDF or LOTTERY stamped while a task holds the lane applies the next time the lane is free — the slice or current RUN ends, or the task is preempted or departs — in place of the running task's slice boundary; item 9's rule and §6.9 name the wait behind a draining switch. §11 item 5 states its condition: a WAIT-first task blocks in its arrival step when no wake is already stored for it, a stored wake completing the WAIT at once; its first `ready` line is the wake that completes the WAIT when the instructions after it reach a RUN without blocking or ending the task; the mocks do the same, the mock simulator (`mock-simulator@2`) storing a wake sent before a task's arrival and writing item 1's zero-wait `ready(cause = wake)` line for the WAIT it completes beside `ready(cause = arrive)`, a case no fixture has. No column, aggregate, constant or floor changed. The primitives, the aggregates and the fixtures follow the arrival row and §6.10's grid (`harness/CHANGELOG.md`, 2026-10-17).
- **2026-10-17 — the WAIT-first arrival (jioh 9.15).** No primitive, aggregate, constant, floor or records column changed, and no harness computation. §11 item 5 states one behaviour in place of two: a task whose first instruction is a WAIT, a spawned child included, blocks in its arrival step with no `ready` line and no occupancy, as the reference simulator does, and the mocks now do the same in place of a zero-length occupancy at the arrival. Such a task has no `cause = arrive` row, so neither its `ready_wait` aggregates over that cause nor its censored turnaround (§9) are written. The mock simulator and the fixtures follow (`harness/CHANGELOG.md`, 2026-10-17).
- **2026-10-17 — the simulator's switch rules as they stand (jioh 9.15).** No primitive, aggregate, constant, floor or records column changed, and no harness computation. §6.9 and §11 item 9 now state that the simulator has carried since 2026-10-10 what they assume — a switch into MLFQ is a cold start, every task in the top queue (its rule U1), and a same-algorithm entry leaves the running task the slice it was granted (its rule U2) — in place of "the simulator does not yet". §11 item 9 states the two differences that stand: a same-algorithm entry stamped during a switch's drain waits behind it, and the simulator restarts MLFQ's boost timer at a same-algorithm entry, where §6.10 keeps the grid of the switch. §12 states that the simulator emits `x_mlfq_demote` and `x_mlfq_boost`, without levels, and not yet `x_mlfq_level`.
- **2026-10-17 — TIMER's `t₀` at the arrival (jioh 9.15).** No primitive, aggregate, constant, floor or records column changed, and no harness computation: `t₀` is still read off the trace as the head's first `ready(cause = timer_tick)` line. §6.2 and §11 item 4 now state where that line falls: the executor executes a periodic task's leading TIMER in its arrival step, as the reference simulator does, so `t₀` is the arrival on a busy lane too (9.11 D11), in place of 9.14 decision 1's first dispatch. `mock-media`'s music player still anchors its grid at its first dispatch (§11 item 4). §11 item 5 states the reference simulator's case beside the mocks': a leading WAIT blocks in the arrival step, with no `ready` line and no occupancy.
- **2026-10-13 — the generated layer's consumers (jioh 9.21).** No primitive, constant, floor or records column changed. §8 gains the flip count and cost, three `config_interval` aggregates over rows that already exist — the configuration changes applied, those on a query graded config-incorrect, the per-switch excess summed over the wrong switches into MLFQ — computed per recognizing run in `aggregates.flip_aggregates` and printed per run beside the file's score by the `flip_cost` reporting line (the hold-time plan's step 1). The generated layer's files are scored by a rule, not by entries: `scoring.with_generated` derives each generated file's terms from the C1 entries per placement the set's manifest records (its task id suffix on the entity, its labelled segments as the window), as `with_variants` derives a variant's from its base's; the rule's statement is in the scoring spec's text and its expansion is linted against the compiled generated files. A generated file's axes — the pair, the form, the middle length, the interval, the split, the relation, the tier, the carrier — stay in its set's manifest and reach a reporting line by joining `workload_id` to the manifest's record (`harness/tools/harness/manifests.py`), not as records columns; an experiment spec selects files from a pinned manifest by those axes (`files.select`, `pins.generated`), the selection expanded to ids before anything else runs. Spec: `_dev/docs/spec/jioh/task-9.21-consumer-work-for-the-generated-layer.md`.
- **2026-10-11 — the telemetry shape as an identity column (jioh 9.17).** Records gain a twenty-fifth column, `telemetry` (§5), after `boot_default`: the shape the run's daemon showed, `focus` or `names` (data-contracts §5, rule 6). It is an identity column of aggregates, scores, guards and grades alike — the grades file's rows are identified by condition, table, seed and `telemetry`, and a `paired` row carries `partner_telemetry` beside `partner_condition`, so one condition under its two shapes is paired like two conditions. The per-experiment spec lists the shapes to run (`telemetry`, every condition under every shape listed; the criterion judged on the first), the runner passes `--telemetry` to the daemon and keys its cache on it, a run directory is `<condition>[-seed][+boot]~<shape>`. The fixtures' expected records, aggregates, scores, guards and grades gain the column at `names`, the shape their hand-written logs show. No primitive, constant, or floor changed.

Every change to a primitive, an aggregate, a constant, or a floor lands here, dated, with the sub-task that made it.

- **2026-10-09 — the TIMER skip rule in the `job` primitive; the records' twenty-fourth column (jioh 9.14).** §6.2 reads the simulator's skip rule (9.11 D3, D17; the 2026-10-07 memo): a `ready(cause = timer_tick)` line consumes the latest grid tick at or before it, the ticks between two consumptions are skipped, and a skipped tick is a `job` row with no completion, counted as missed. Records gain `skipped` (§5), 1 on a skipped tick's row, where `value` is empty, and 0 on a consumed tick's; the `job` aggregates count skipped ticks in `count` and `miss_rate` and leave them out of the latency percentiles. `t₀` is read off the trace as the first `timer_tick` line's time (§11 item 4), the arrival no longer standing in for it. The chain guard counts consumed ticks; the `deadline` cross-check pairs lines with ticks in tick order and reads `met` on a skipped tick's line. `mock-media` re-derived with a longer scan so one tick is skipped. No constant or floor changed.
- **2026-10-08 — scheduler-side constants and groundings (jioh 9.11).** No aggregate and no value changed. §10: `T_interaction`'s grounding — Miller's two delays, 0.1 s the strict end of his 0.1–0.2 s key-to-echo range by design, cross-checked against Deber et al.'s tapping thresholds (12 sessions), Nielsen a restatement rather than a second grounding, Long's finding a trend within its range; read on input-channel wakes. The floors and the bootstrap seed and repetitions labelled design, the latter pinned in the grader; the guard thresholds' kinds. §8: the percentile rule labelled a convention; the cluster bootstrap's coverage at the coreset's file count and sizes stated as untested; the coefficient's undefined case labelled design against Chicco and Jurman's convention. §9: the boot default's provenance and the sweep's nine points. §11's items 1–4 and 9, and §6.9's premise, stated against the simulator's state, its deviations as owed; TIMER's `t₀` is the task's first TIMER execution, as the simulator sets it, equal to its arrival on every current file (§6.2's cross-reference with it).
- **2026-09-26 — wake rows carry their channel (jioh 9.5).** A measured timer wake now compiles as a WAIT on the task's `timer` channel, woken by a wake event at its measured time, so a `ready(cause = wake)` line is a keystroke or a timer wake alike. The run file's fourth fact is each task's WAIT channels in program order and its input wake events (§3). Records gain a twenty-third column, `channel` (§5): on a `ready_wait` row with `cause = wake`, the kind of the channel of the WAIT the line completed (§6.1). Interaction latency and the per-switch excess read `channel = input` (§6.1, §8); the `ready_wait` aggregates over `cause = wake` also come per channel; the stimulus count compares the input-channel rows with the run file's input wake events, and a wake line past the last WAIT of its task's program is a guard. A scoring-spec `ready_wait` term with `cause: wake` may name `channel`; the frozen spec's interaction-latency terms gain `channel: input` in 9.14's change to it, and until then read every channel. The fixtures' expected records, aggregates, and scores gain the column. No constant or floor changed.
- **2026-09-12 — `W_single`'s worked value (jioh 8.9).** No rule changed. §6.9's parenthetical example of `W_single` still quoted the 2 ms boot slice's 6 000 µs; at the OSTEP boot default of 2026-09-11 the same formula gives 30 000 µs. The formula and the incoming-entry rule are unchanged.
- **2026-09-11 — the Layer-1 grader (jioh 8.4).** Records gain a twenty-second column, `pre_committed_miss` (§5), and `sim` stops being required, since a recognition row comes from a log and not a trace. §7 gains a fifth recognition primitive, `config_correct`, the exclusion rule for pre-committed misses, and the off-menu rules. §8's recognition row is the grader's and lands in a `grades` file (`harness/grades/schema/`, `harness/tools/harness/grader.py`, CLI `tools/grade.py`): balanced accuracy and the Matthews coefficient on the binary attribute only, raw accuracy against a measured majority baseline with confusion matrix and per-class recall on mode and algorithm choice, no macro-average anywhere, the configuration-distance line, and clustered intervals with paired condition comparisons. The familiarity tier is carried and no longer aggregated: the earlier "each also per familiarity tier" required numbers the coreset cannot support, one graded query point per annotated tier. §10 gains the bootstrap seed, repetitions and interval level. Seeds are averaged over rather than pooled, mirroring §9's Layer-2 rule, with both readings kept (`over_seeds`, `n_seeds`). Fixture `mock-grades`. No trace primitive, constant, or floor changed.
- **2026-09-11 — guard spec and guards (jioh 8.3).** No primitive, aggregate, constant, or floor changed. The guards' list, thresholds, and groundings now live in the guard spec, `harness/guards/guard-spec.yaml` (schema and lint beside it, in CI), read by `harness/tools/harness/guards.py` into a `guards` file (`harness/guards/schema/guards.schema.json`): provenance share below 0.5 and starvation at or below 1 000 000 µs as stated assumptions, utilisation as arithmetic, the rest structural; the config-age guard checks observation staleness against the ground-truth segments and is distinct from §8's `config_age_*` aggregates (time in force), which §8 now says. The reader gains `read_recognition_log` (data-contracts §8). Fixture `mock-guards`.
- **2026-09-11 — boost windows (jioh 8.10).** New primitive `boost_window` (§6.10), one row per boost instant inside an MLFQ interval entered by a switch, on `switch_window`'s columns with a new `metric` value; `busy` is §6.11, the summary §6.12. With it the aggregates module computes §8's per-switch excess in both variants (the switch window against the rest of the config interval outside any window; the boost windows against the same), closing the gap 8.2 left. `mock-switch` gains its two hand-worked boost rows. No simulator or daemon output changes: the grid and the windows come from the trace and the config schedule the harness already reads.
- **2026-09-11 — aggregates and scores (jioh 8.2).** Records gain a twenty-first column, `boot_default` (§5). §8 states the percentile convention. §9 gains the composition rules: the no-headroom term's share 1, the censored turnaround, the empty filter as an error, the file precisions. The trace-derived aggregates of §8 land in code (`harness/tools/harness/aggregates.py`) writing an `aggregates` file, the scorer (`scorer.py`) a `scores` file, both with schemas beside them and the `score.py` CLI; the recognition aggregates are the grader's (8.4). The per-switch excess and its boost variant followed in 8.10, once `boost_window` rows existed. No primitive, constant, or floor changed.
- **2026-09-11 — latency floor untied from the slice (jioh 8.1).** No value changed: the latency floor stays 1 000 µs. Its stated reason was half the boot default's 2 000 µs slice; the boot default is now OSTEP's example with a 10 ms slice (`recognition-vocabulary.md` §2, changelog), and the floor is not moved with it. It is a plain stated assumption, defended by a pre-registered floor-sensitivity reporting line in the RQ0 gate spec (the verdict recomputed under a band of floors at scoring time, no reruns) rather than by a derivation. §10's row says so.
- **2026-09-09 — scoring spec (jioh 6.2).** The per-file terms land as data in the harness tree (`harness/scoring/scoring-spec.yaml`, schema and lint beside it, in CI): scored aggregates are `ready_wait` P99, `job` miss rate, progress, `turnaround`; C2 latency and frame terms windowed 60 s–`T_end`; derived files carry their base's terms verbatim. §2 points at it. No primitive, aggregate, constant, or floor changed.
- **2026-09-09 — switch overhead (jioh 6.1).** New primitive `switch_window` (§6.9) with the `hogs` attribute, the twentieth records column; the config schedule becomes the third input (§3), read by `index`; two aggregates over switch windows (§8: per-switch excess wake `ready_wait`, switch and boost variants; share inside switch windows), reported and never weighted; §11 gains 7 (boost timer restarts at `t_apply`), 8 (FIFO-outgoing rule (a)) and 9 (a same-algorithm entry applies at its stamped time), all three confirmed with 인경민 on 2026-09-09; fixture `mock-switch` and the `x_mlfq_level` check tool (§12). From the 2026-09-08 memo on algorithm-switch semantics, whose window the same day's spec session re-sized in lane time (memo §7) after the mock showed the wall-clock window closing before the hog's descent. `mock-media`'s same-instant boot + oracle pair is a switch into FIFO and gains a zero-valued row; `mock-chain` gains the same oracle FIFO entry so its scheduler matches its config line; `mock-p1a` now follows the guide's MLFQ rules (its editor falls to the bottom queue on its own bursts).
- **2026-09-08 — first version (jioh 5.2).** Trace primitives §6, recognition primitives §7, aggregate list §8, per-aggregate normalisation with absolute floors §9, constants §10 (`T_interaction` grounded in `miller-fjcc68` and `nielsen-ue93`, with `shneiderman-csur84` on the range; floors as stated assumptions), simulator assumptions §11. Records take a `familiarity` attribute column for recognition rows, carried from `ground_truth` (data-contracts changelog, same date). The two definitions `../data-contracts.md` §9 deferred to this freeze — periodic job completion, and starvation from `ready` — are §6.2 and §6.1.
