# Metrics — primitives, records, and the aggregates the research reads

> Status: normative · Created 2026-09-08 · Updated 2026-09-11

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

**Run file** — the simulator's input, the run-file view of the workload (`../data-contracts.md` §4): `workload_id` and `events`. The reader takes it as a second input for three facts the trace does not carry:

| fact | how it is read |
|---|---|
| `T_end` | the largest pinned time in the file: arrival times, pinned departs, and wake events |
| chain topology | a **chain** is the WAKE path starting at a task whose program contains a TIMER: the head, then each task the previous stage's WAKE targets, until a stage wakes no one (the tail). A TIMER task that wakes no one is a chain of length one. |
| `demand` | a task's total RUN work, summed over its program; defined only when the program has no unbounded LOOP |

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

One CSV file per trace (or per recognition log), every row self-contained, twenty-two columns.

**Identity** — which run the row came from.

| column | meaning |
|---|---|
| `workload_id` | the workload |
| `condition` | the recognizer condition (`fixed`, `random`, `whitelist`, `llm_vocab`, `llm_algo`, `llm_full`, `oracle`) |
| `table` | `prior` or `calibrated`; empty for `fixed`, which uses no table |
| `seed` | `random`'s PRNG seed; empty otherwise |
| `boot_default` | the id of the boot configuration the run started in; empty for the primary. Only the `fixed` runs of the RQ0 gate spec's sensitivity check carry one; the scorer pairs a run with the `fixed` run of the same `boot_default` (added 2026-09-11, 8.2) |
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
| `provenance` | `config_interval` | `unmodified`, `clamped`, `held`, `fallback` |
| `algorithm` | `config_interval`, `switch_window` | `MLFQ`, `EDF`, `LOTTERY`, `FIFO` |
| `index` | `config_interval`, `switch_window` | the schedule entry's index |
| `period_us` | `job` | the TIMER period; a miss is `value > period_us`, slack is `period_us − value` |
| `predicted` | `mode_correct`, `attr_correct`, `algo_choice_correct` | what the recognizer answered |
| `truth` | `mode_correct`, `attr_correct`, `algo_choice_correct` | the answer key's value |
| `validation` | every recognition row | what the validator did with the answer |
| `familiarity` | every recognition row | the covering segment's familiarity tier, when the segment carries one |
| `hogs` | `switch_window` | the hog count H at the switch (§6.9) |
| `pre_committed_miss` | every recognition row | 1 when the covering segment carries the `pre_committed_miss` annotation, 0 otherwise; the headline accuracy excludes those rows and the second report line includes them (added 2026-09-11, 8.4) |

**Rules.**

- **Row order**: by `entity`, then `metric`, then `t` (numeric), then `cause`. Files compare byte for byte.
- **Anchors**: window-level rows (`cpu_delivered`, `demand`, `preempt_count`, `busy`, and `completed` with value 0) sit at `T_end`; `completed` with value 1 and `turnaround` sit at the `task_end` time; every other primitive names its anchor below.
- **No aggregates, no derived flags.** `met` is not stored (it is `value ≤ period_us`); progress is not stored (it is `cpu_delivered / demand`).
- **Machine schema**: lands beside the code that writes the file, in the harness tree (`harness/records/schema/`), enforced by its tests. Records are not a data contract: only the harness writes and reads them.

---

## 6. Trace primitives

Each primitive states what it measures, which trace lines produce it, and what the row carries.

### 6.1 `ready_wait`

*How long a task waited for the CPU after it became runnable.*

One row per `ready` line inside the window. `t` = the `ready` time. `value` = the task's next `run_start` minus `t`; **zero when the `ready` falls inside the task's own occupancy** (at or after a `run_start` and before its `run_end`), which is how a blocking primitive that completed without blocking appears. `cause` carried on the row.

The proposal's named metrics are filters and aggregates over it:

| name | filter / aggregate |
|---|---|
| interaction latency (per stimulus) | rows with `cause = wake` on the task the scoring spec names |
| response time (per task) | the row with `cause = arrive` |
| timer dispatch delay | rows with `cause = timer_tick` |
| starvation | a task's maximum `ready_wait` over the window, any cause — measured from `ready`, never from arrival: a task sleeping voluntarily is not starving |

A chain stage's WAIT completing is also `cause = wake`; the trace does not name channels, so scoring tells keystrokes from stage hand-offs by entity.

### 6.2 `job`

*How long one periodic job took, from its tick to its completion.*

**Definition.** Job k of a TIMER task starts when tick k is consumed and is due at tick k + period. For a **single-stage** task, job k completes when the task next reaches its TIMER — the end of that iteration's work. For a **chain** (§3), frame k completes when the **tail** stage ends its k-th iteration; the head's own job boundary is not the frame.

One row per tick inside the window whose completion is also inside it. Entity = the chain head (for a single-stage task, the task itself). `t` = the tick. `value` = completion − tick. `period_us` on the row.

**How it is computed.** The head's k-th `ready(cause = timer_tick)` line marks the consumption of tick k; the tick itself is `t₀ + k·period` on the TIMER grid, `t₀` being the task's arrival (§11, assumption 4); a tick is consumed late whenever the lane was busy or the task was in backlog, so the line's time is never taken as the tick's. A stage's k-th iteration ends at its k-th `run_end` with reason `block`, `exit`, or `depart` — or, when the next iteration began without blocking, at the k+1-th `ready` line of that stage. The reader pairs iterations by index, which is valid because wakes queue with depth (§11).

**Guard.** For every chain, the tail's iteration count equals the head's tick count; a shortfall means a wake was lost. For a length-one chain, each `job` row must agree with the simulator's `deadline` line for that job (`slack_us = period_us − value`). `deadline` lines are never the source of a `job` row; for a chain longer than one they measure the head stage alone and are expected to differ from frame latency.

### 6.3 `cpu_delivered`

*How much CPU the task received in the window.* The sum of the task's occupancy intervals (`run_start` to `run_end`), clipped at `T_end`. One row per task, at `T_end`.

### 6.4 `demand`

*How much CPU the task needed.* The task's total RUN work read from the run file. One row per task whose program has no unbounded LOOP, at `T_end`. Progress, `cpu_delivered / demand`, is scoring's.

### 6.5 `completed`

*Did the task finish inside the window.* 1 with `t` = the time of a `task_end` with reason `exit` at or before `T_end`; otherwise 0 at `T_end`. A segment-bound task ends by `depart`, so its row is always 0.

### 6.6 `turnaround`

*From arrival to completion.* Only when `completed` is 1: `task_end` time minus `task_arrive` time, at the `task_end` time. A spawned child's arrival is its `task_arrive(source = spawn)` line, an emergent time. An orchestrator's turnaround is the build's makespan, since it exits only after its children.

### 6.7 `preempt_count`

*How often the task was forced off the CPU.* The count of the task's `run_end` lines with reason `preempt` inside the window. One row per task, at `T_end`.

### 6.8 `config_interval`

*How long each configuration was in force.* One row per `config_applied` line, entity `schedule`, `t` = the applied time, `value` = time until the next `config_applied` or `T_end`, with `provenance`, `algorithm`, `index`. Two entries at the same instant give the earlier a value of 0. Provenance shares (time-weighted and count-weighted), config age, and the fallback share are aggregates over these rows.

### 6.9 `switch_window`

*How long, after a switch into MLFQ, the scheduler was re-learning who is batch.* From the 2026-09-08 memo on algorithm-switch semantics (`../memos/2026-09-08-algorithm-switch-semantics-for-the-simulator.md` §4): a cold start into MLFQ puts every task in the top queue, the state MLFQ's own boost produces, so a switch is one extra boost and is measured in those units.

One row per `config_applied` line inside the window whose algorithm differs from the previous applied entry's; the boot entry has no predecessor and never produces a row, and an entry that changes only params or the cap is not a switch (it applies at its stamped time with queue levels kept, §11 item 9). Entity `schedule`, `t` = the applied time (`t_apply`), with `algorithm` (incoming), `index`, and `hogs` on the row.

- **`W_single`** is the CPU a CPU-bound task must receive to fall from the top queue to the bottom, one full slice per upper level: `timeslice_us · Σ_{l=0}^{num_queues−2} timeslice_growth^l`, rounded down to whole µs, from the **incoming** entry's params in the config schedule (6 000 µs at the boot default). No parameter is ever inferred from behaviour.
- **`H`**, the hog count, is behavioural: a task alive at `t_apply` (arrived at or before it, not ended at or before it) whose first `run_end` after `t_apply`, at or before `T_end`, has reason `preempt`. Known bias: a task preempted by a wake into a higher queue is counted too. `hogs` carries H for every switch row, including the zero-valued ones.
- **`value`** for a switch into MLFQ is the length of the window `[t_apply, t_close]`, where `t_close` is the instant the **last** counted hog has received `W_single` of CPU since `t_apply`, summed from its occupancy intervals (the sum `cpu_delivered` takes, started at `t_apply`). The window is therefore sized in lane time: other tasks holding the lane stretch it rather than escape it. If a hog has not received `W_single` by the next algorithm switch or by `T_end`, the window is clipped there and a guard names the hog. With no hogs the value is 0. For a switch into EDF, LOTTERY, or FIFO the value is 0: nothing those algorithms need is discarded (deadlines come from the process model, tickets from the config, arrival order is always known).

What the window can still miss — a hog boosted before it reaches the bottom, a hog the preempt rule did not count — is what the `x_mlfq_level` check (§12) measures.

### 6.10 `boost_window`

*How long, after each boost inside an MLFQ interval entered by a switch, the scheduler was re-learning who is batch.* The boost variant of §6.9, so the §8 excess aggregates can tell a switch's cost from an ordinary boost's. One row per boost instant `t_apply + k · boost_interval_us` (k ≥ 1) that falls before the interval's end (the next algorithm switch or `T_end`), the grid from the switch's incoming entry (§11 item 7: the boost timer restarts at `t_apply`). Entity `schedule`, `t` = the boost instant, with `algorithm` (`MLFQ`), `index` (the entry in force at the instant, so a params-only entry inside the interval is honoured), and `hogs`. `value` is the window's length by the §6.9 rule from that instant — H counted there, closing when the last counted hog has received `W_single` of CPU since it — clipped at the next boost instant or the interval's end without a guard, since a boost window running into the next boost is the normal case, not a hog escaping. With no hogs the value is 0. Added 2026-09-11 (8.10).

### 6.11 `busy`

*How long the lane was occupied.* The sum of every task's clipped occupancy, entity `lane`, one row at `T_end`. Idle is `T_end − busy`; utilisation is `busy / T_end`.

### 6.12 Summary

| metric | entity | rows | from the trace | from the run file | anchor `t` |
|---|---|---|---|---|---|
| `ready_wait` | task | per `ready` | `ready` → next `run_start`, or inside own occupancy | — | ready time |
| `job` | chain head | per tick | head ticks, stage iteration ends | chain topology | tick |
| `cpu_delivered` | task | 1 | occupancy intervals, clipped | `T_end` | `T_end` |
| `demand` | task | 0 or 1 | — | RUN total (finite only) | `T_end` |
| `completed` | task | 1 | `task_end(exit)` inside window | `T_end` | end time or `T_end` |
| `turnaround` | task | 0 or 1 | `task_arrive` → `task_end(exit)` | — | end time |
| `preempt_count` | task | 1 | `run_end(preempt)` count | — | `T_end` |
| `config_interval` | `schedule` | per entry | `config_applied` → next | `T_end` | applied time |
| `switch_window` | `schedule` | per algorithm change | `config_applied`, first `run_end` per alive task, the hogs' occupancy after it | `W_single` from params by `index` (config schedule) | applied time |
| `boost_window` | `schedule` | per boost instant inside an MLFQ interval entered by a switch | the boost grid from the switch, first `run_end` per alive task, the hogs' occupancy after it | `boost_interval_us` and `W_single` from params by `index` (config schedule) | boost instant |
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
| `ready_wait` rows (a filter by `cause` and entity applied first) | count; mean; P50; P95; P99; max; **`over_threshold`** — the fraction of rows with `value > T_interaction` (§10) |
| `job` rows | count; **miss rate** — the fraction with `value > period_us`; latency P50; latency P99 |
| `cpu_delivered`, `demand` | **progress** — `cpu_delivered / demand` |
| `completed`, `turnaround` | completion (0/1); turnaround as is |
| `preempt_count` | as is; summed over tasks for the lane |
| `config_interval` rows | time-weighted share per `provenance`; count share per `provenance`; **fallback share** (time-weighted `fallback` + `held`); config age — the distribution of `value` |
| `switch_window` rows with `ready_wait` rows | **per-switch excess** — for each switch into MLFQ, the mean of the `ready_wait(cause = wake)` values of the scoring spec's interactive task inside the switch window `[t, t + value]`, minus the mean of the same task's rows in the rest of that config interval outside any window, in µs; the **boost variant** takes the same excess over the boost windows of that interval, one at each instant `t + k · boost_interval_us` (k ≥ 1), each sized by the §6.9 rule from that instant (H counted there, closing when the last hog has its `W_single`) and clipped at the next boost; switch excess ≈ boost excess means the switch cost one boost, the difference above it is backlog carried from the outgoing algorithm. **Share inside switch windows** — Σ `value`, each clipped at `T_end`, over `T_end`. Neither is weighted in any score; both are reported beside it |
| `busy` | utilisation `busy / T_end`; idle `T_end − busy` |
| recognition rows | the grader's, not the aggregates module's (§7; 8.4), and they land in the `grades` file (`harness/grades/schema/`) rather than here: raw accuracy beside its **measured** majority baseline on every axis; **balanced accuracy** and the **Matthews correlation coefficient** on the binary attribute only; the confusion matrix over (`truth`, `predicted`) and per-class recall on mode and on algorithm choice; the configuration-correct rate and the share of errors that changed the configuration; latency P50/P99 over rows with `mode_correct = 1`. The familiarity tier rides on the row as a split key and **no per-tier aggregate is defined**: at the current coreset each annotated tier carries one graded query point and tiers 1 and 2 have none, so what the tiers demonstrate belongs to its own experiment |

**Which statistic goes on which axis is decided, not free.** Balanced accuracy is defined for two classes (`brodersen-icpr10`, which defines it off a two-by-two matrix and gives no K-class form), and it earns its place where a degenerate answer would otherwise score well. Measured on the compiled coreset on 2026-09-11, a constant answer scores 69.5 per cent on the attribute and 11.0 per cent on mode, because Phase 7 instanced all thirty-two cells. So the attribute is corrected and mode is not: mode and algorithm choice report raw accuracy against the measured baseline with the confusion matrix and per-class recall, and **no macro-average is computed on any axis**. The Matthews correlation coefficient (`chicco-bmcg20`) sits beside balanced accuracy on the attribute, computed over the points whose prediction names one of the two classes, so its count is its own; a null answer still costs recall.

**Intervals and comparisons.** Query points inside one workload file share its process names and its situation, so they are not independent observations. Every interval therefore comes from a **cluster bootstrap that resamples workload files**, not query points (`field-jrssb07`, whose consistency is in the number of clusters and which is anti-conservative at very few). Condition comparisons are computed **paired**, on the same drawn files, because every condition is graded on identical query points (`dietterich-neco98`, which names this case and rules out both a difference of two proportions and a resampled t test). Determinism here means reproducibility: the seed and the repetition count are constants (§10), so a rerun gives byte-identical bounds.

Percentiles are computed on the raw values with linear interpolation: position `(n − 1) · p / 100` on the sorted values, interpolating between the two neighbours (numpy's `linear` method, R's type 7), computed exactly on the integer records. Mean is reported for sanity only, never as a headline. Counts (stimuli per task, ticks per chain) are guard inputs: stimulus count is checked against the workload's wake events, tick count against the window's tick grid. The guards themselves — the eight checks, their thresholds, and the grounding behind each — are the guard spec, `../../harness/guards/guard-spec.yaml` (8.3), read by `harness/tools/harness/guards.py` into a `guards` file beside `aggregates` and `scores`. The `config_age` aggregates above measure time in force and are reported; the config-age guard measures something else, whether an entry took effect before the ground-truth segment its query was observed in had ended.

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

**Composition.** A file's score is the scoring spec's weighted sum of its terms' shares. A term marked *no headroom* keeps its weight and enters the sum as if the condition had captured all of the headroom (share 1), so it never makes a file easier to pass; the mark is carried on the term (Phase 8 spec, decision 4; 8.2). A `turnaround` term whose task did not complete inside the window has no `turnaround` row (§6.6); it is scored on the censored lower bound `T_end − arrival`, the row marked *censored*, so not finishing is worse than every finishing value (8.2 spec, decision 4). A term whose filter selects no rows stops the scorer: every scored entity is linted to exist, so an empty filter is a scoring-spec mistake. The `aggregates` file carries twelve decimal places and the `scores` file six, so a six-place share is exact to its last digit (`harness/aggregates/schema/`, `harness/scores/schema/`).

**Sensitivity.** `fixed` is the boot default, whose values are stated assumptions (`../recognition-vocabulary.md` §2). The RQ0 gate spec pre-registers `fixed` under two alternative boot defaults; where the sign or ordering of a share moves, the floor is reported as a range. That reporting rule is the RQ0 gate spec's (Phase 8); the formula here does not change.

---

## 10. Constants

| constant | value | status |
|---|---|---|
| `T_interaction` — the perceptual threshold for interaction latency | **100 000 µs** (0.1 s) | grounded (`miller-fjcc68`, `nielsen-ue93`); see below |
| floor for latency-type aggregates (`ready_wait` mean/P50/P95/P99/max; `job` latency P50/P99; `turnaround`) | **1 000 µs** | stated assumption, tied to no scheduler parameter (2026-09-11): one millisecond, below which a latency difference between two configurations is not read; the RQ0 gate spec pre-registers a floor-sensitivity line, the verdict recomputed under a band of floors at scoring time |
| floor for fraction-type aggregates (`over_threshold`, miss rate, progress, completion) | **0.01** | stated assumption: one percentage point |
| counts, provenance shares, utilisation | not normalised | guard and sanity inputs only; the guards' thresholds are the guard spec's (`../../harness/guards/guard-spec.yaml`), each an identity, a structural rule, or a stated assumption |
| cluster-bootstrap seed; repetitions (§8) | **20260911**; **10 000** | pinned, not estimated: a fixed seed makes an interval byte-identical on a rerun, so the harness keeps its own determinism rule. The RQ0 gate spec pins both |
| interval level (§8) | **95 per cent** | convention |

**`T_interaction` = 0.1 s.** Miller (1968), Topic 1, "Response to control activation": the feedback that a key or control has been activated "should be immediate and perceived as a part of the mechanical action induced by the operator. Time delay: No more than 0.1 second"; for the echo of typed text, "the delay between depressing the key and the visual feedback should be no more than 0.1 to 0.2 seconds", with the caveat that "this delay in feedback may be far too slow for skilled keyboard users". Nielsen (1993), *Usability Engineering* ch. 5: "0.1 second is about the limit for having the user feel that the system is reacting instantaneously", which names Miller 1968 as its source. Shneiderman (1984) reports Long's 1976 finding that keystroke-echo delays of "approximately 0.1–0.5 second" already slowed both unskilled and skilled typists and raised their error rates, so 0.1 s is the loose end of the range, not a comfortable target; the percentile aggregates carry what the fraction discards. The constant applies to `ready_wait` rows with `cause = wake` on interactive tasks. It is one input to the `c1-media` weighting question in the scoring spec, not its answer.

Floors are stated assumptions and may be revised by the RQ0 gate spec with a changelog entry here.

---

## 11. Simulator assumptions

The definitions above, and the mock traces that test them, assume the following simulator behaviour. Items 1–3 were sent to the simulator's owner as clarifications of the trace contract (`../memos/2026-09-07-trace-clarifications-for-the-simulator.md`); items 4–6 are mock-local choices that fill gaps the contracts leave open. A different decision on any of them changes the mocks deliberately, not the definitions.

1. A `ready` line is emitted at **every completion of a blocking primitive** (`WAIT`, `TIMER`, `SLEEP`, fork slot), at zero wait when it did not block; inside an occupancy it appears after the `run_start` and pairs with wait 0.
2. **Wakes queue with depth**: two wakes sent to a busy task complete its next two WAITs, so iteration k of every chain stage is tick k.
3. Same-instant events follow a **written, deterministic tie-break**; the mocks apply config entries first in list order, then arrivals in file order.
4. TIMER's `t₀` is the task's arrival time, so a TIMER task arriving at 0 consumes tick 0 at 0 without blocking.
5. An arriving task whose first instruction blocks is scheduled like any other, reaches the WAIT, and blocks: a zero-length occupancy when the lane is free.
6. The simulator keeps emitting `deadline` lines as the contract says; the harness uses them only as the §6.2 cross-check.
7. **The boost timer restarts at `t_apply`** after a switch into MLFQ, so the boost grid of §8 is `t_apply + k · boost_interval_us`. Confirmed with 인경민 on 2026-09-09 (memo §5, §7).
8. A switch out of FIFO applies immediately and the running task is treated as freshly dispatched by the incoming algorithm (the memo's rule (a)); a switch out of any other algorithm applies at the running task's slice boundary (the drain). Confirmed with 인경민 on 2026-09-09. The primitives read the applied instant off the trace either way.
9. **An entry with the same algorithm is not a switch.** It applies at its stamped time, no drain, queue levels kept; the running task finishes the slice it was granted and the new params govern from its next dispatch; the cap takes effect at once. Confirmed with 인경민 on 2026-09-09 (memo §7).

---

## 12. Mock fixtures

`harness/tools/tests/fixtures/` holds five hand-written pairs (run file, trace) with hand-computed expected records and a worked derivation each, plus `mock-scores` (8.2): hand-written records for one small workload under `fixed`, `oracle`, `random` × 2 seeds, and `fixed` under an alternative boot default, with the expected `aggregates` and `scores` files and a worked derivation, shaped to hit every scorer rule of §9. The five pairs: `mock-office` (queued keystrokes, an unfocused task), `mock-media` (backlog, a same-instant config pair that is also a switch into FIFO, a completing batch task), `mock-p1a` (config change without an algorithm switch, preemptions, a batch task clipped at `T_end`), `mock-chain` (a three-stage frame pipeline with one late frame), `mock-switch` (MLFQ → FIFO → MLFQ with a config schedule, one hog, the §8 excess aggregates worked by hand). `mock-media` and `mock-chain` run FIFO under an oracle entry stamped beside the boot entry, so their stated scheduler and their config lines agree. They are the tests of §6 and the seeds of Phase 8's mock simulator.

**`x_mlfq_level` check.** The simulator emits `x_mlfq_level` `{t, task, from, to}` on every MLFQ demotion and boost; the harness ignores it by the `x_` rule. `harness/tools/check_mlfq_levels.py`, beside the harness and not part of it, reads those lines and reports, per switch into MLFQ, whether the window covered each hog's last demotion (the run of demotions after `t_apply`, ending at the next boost or the bottom queue). A systematic miss is the evidence for proposing a field in the closed trace set; until then the trace contract stays frozen. On `mock-switch` the check passes at the window's edge; under the memo's original wall-clock window it failed there, which is what led to the lane-time definition (memo §7).

---

## 13. Changelog

Every change to a primitive, an aggregate, a constant, or a floor lands here, dated, with the sub-task that made it.

- **2026-09-11 — the Layer-1 grader (jioh 8.4).** Records gain a twenty-second column, `pre_committed_miss` (§5), and `sim` stops being required, since a recognition row comes from a log and not a trace. §7 gains a fifth recognition primitive, `config_correct`, the exclusion rule for pre-committed misses, and the off-menu rules. §8's recognition row is the grader's and lands in a `grades` file (`harness/grades/schema/`, `harness/tools/harness/grader.py`, CLI `tools/grade.py`): balanced accuracy and the Matthews coefficient on the binary attribute only, raw accuracy against a measured majority baseline with confusion matrix and per-class recall on mode and algorithm choice, no macro-average anywhere, the configuration-distance line, and clustered intervals with paired condition comparisons. The familiarity tier is carried and no longer aggregated: the earlier "each also per familiarity tier" required numbers the coreset cannot support, one graded query point per annotated tier. §10 gains the bootstrap seed, repetitions and interval level. Fixture `mock-grades`. No trace primitive, constant, or floor changed.
- **2026-09-11 — guard spec and guards (jioh 8.3).** No primitive, aggregate, constant, or floor changed. The guards' list, thresholds, and groundings now live in the guard spec, `harness/guards/guard-spec.yaml` (schema and lint beside it, in CI), read by `harness/tools/harness/guards.py` into a `guards` file (`harness/guards/schema/guards.schema.json`): provenance share below 0.5 and starvation at or below 1 000 000 µs as stated assumptions, utilisation as arithmetic, the rest structural; the config-age guard checks observation staleness against the ground-truth segments and is distinct from §8's `config_age_*` aggregates (time in force), which §8 now says. The reader gains `read_recognition_log` (data-contracts §8). Fixture `mock-guards`.
- **2026-09-11 — boost windows (jioh 8.10).** New primitive `boost_window` (§6.10), one row per boost instant inside an MLFQ interval entered by a switch, on `switch_window`'s columns with a new `metric` value; `busy` is §6.11, the summary §6.12. With it the aggregates module computes §8's per-switch excess in both variants (the switch window against the rest of the config interval outside any window; the boost windows against the same), closing the gap 8.2 left. `mock-switch` gains its two hand-worked boost rows. No simulator or daemon output changes: the grid and the windows come from the trace and the config schedule the harness already reads.
- **2026-09-11 — aggregates and scores (jioh 8.2).** Records gain a twenty-first column, `boot_default` (§5). §8 states the percentile convention. §9 gains the composition rules: the no-headroom term's share 1, the censored turnaround, the empty filter as an error, the file precisions. The trace-derived aggregates of §8 land in code (`harness/tools/harness/aggregates.py`) writing an `aggregates` file, the scorer (`scorer.py`) a `scores` file, both with schemas beside them and the `score.py` CLI; the recognition aggregates are the grader's (8.4). The per-switch excess and its boost variant followed in 8.10, once `boost_window` rows existed. No primitive, constant, or floor changed.
- **2026-09-11 — latency floor untied from the slice (jioh 8.1).** No value changed: the latency floor stays 1 000 µs. Its stated reason was half the boot default's 2 000 µs slice; the boot default is now OSTEP's example with a 10 ms slice (`recognition-vocabulary.md` §2, changelog), and the floor is not moved with it. It is a plain stated assumption, defended by a pre-registered floor-sensitivity reporting line in the RQ0 gate spec (the verdict recomputed under a band of floors at scoring time, no reruns) rather than by a derivation. §10's row says so.
- **2026-09-09 — scoring spec (jioh 6.2).** The per-file terms land as data in the harness tree (`harness/scoring/scoring-spec.yaml`, schema and lint beside it, in CI): scored aggregates are `ready_wait` P99, `job` miss rate, progress, `turnaround`; C2 latency and frame terms windowed 60 s–`T_end`; derived files carry their base's terms verbatim. §2 points at it. No primitive, aggregate, constant, or floor changed.
- **2026-09-09 — switch overhead (jioh 6.1).** New primitive `switch_window` (§6.9) with the `hogs` attribute, the twentieth records column; the config schedule becomes the third input (§3), read by `index`; two aggregates over switch windows (§8: per-switch excess wake `ready_wait`, switch and boost variants; share inside switch windows), reported and never weighted; §11 gains 7 (boost timer restarts at `t_apply`), 8 (FIFO-outgoing rule (a)) and 9 (a same-algorithm entry applies at its stamped time), all three confirmed with 인경민 on 2026-09-09; fixture `mock-switch` and the `x_mlfq_level` check tool (§12). From the 2026-09-08 memo on algorithm-switch semantics, whose window the same day's spec session re-sized in lane time (memo §7) after the mock showed the wall-clock window closing before the hog's descent. `mock-media`'s same-instant boot + oracle pair is a switch into FIFO and gains a zero-valued row; `mock-chain` gains the same oracle FIFO entry so its scheduler matches its config line; `mock-p1a` now follows the guide's MLFQ rules (its editor falls to the bottom queue on its own bursts).
- **2026-09-08 — first version (jioh 5.2).** Trace primitives §6, recognition primitives §7, aggregate list §8, per-aggregate normalisation with absolute floors §9, constants §10 (`T_interaction` grounded in `miller-fjcc68` and `nielsen-ue93`, with `shneiderman-csur84` on the range; floors as stated assumptions), simulator assumptions §11. Records take a `familiarity` attribute column for recognition rows, carried from `ground_truth` (data-contracts changelog, same date). The two definitions `../data-contracts.md` §9 deferred to this freeze — periodic job completion, and starvation from `ready` — are §6.2 and §6.1.
