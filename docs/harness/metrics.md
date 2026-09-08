# Metrics — primitives, records, and the aggregates the research reads

> Status: normative · Created 2026-09-08 · Updated 2026-09-08

Every number the project reports is defined here. The document fixes three things: the **primitives** — the raw observations the harness computes from a trace or a recognition log; the **records** file they land in; and the **aggregates** — the statistics, the normalisation rule, and the constants that turn records into the figures the research questions ask for. Per-file weights are not here; they belong to the scoring spec (Phase 6). The code that implements the trace primitives lives in `harness/`; the grader that implements the recognition primitives is built in Phase 7 to the definitions below.

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
primitives(run_file, trace)                       → records rows   (entities: tasks, lane, schedule)
grader(recognition_log, ground_truth, calibrated_table) → records rows   (entity: recognizer)
scoring(records, scoring_spec)                    → aggregates, normalised shares, scores
```

The first function is Phase 5's harness lower half. The second is Phase 7's grader, implementing §7. The third is Phase 6's scoring spec applied by Phase 7's scorer, using §8–§10. All three write or read the one records shape of §5.

---

## 3. Inputs

**Trace** — the simulator's output, frozen in `../data-contracts.md` §9: JSONL, a `meta` header line, then seven event types. The reader streams plain or gzipped files, validates that every non-`x_` line is one of the seven types with the fields the contract names, ignores `x_`-prefixed lines wholesale, captures the header (`workload_id`, `condition`, `sim`), and refuses a trace whose task ids collide with a reserved entity name.

**Run file** — the simulator's input, the run-file view of the workload (`../data-contracts.md` §4): `workload_id` and `events`. The reader takes it as a second input for three facts the trace does not carry:

| fact | how it is read |
|---|---|
| `T_end` | the largest pinned time in the file: arrival times, pinned departs, and wake events |
| chain topology | a **chain** is the WAKE path starting at a task whose program contains a TIMER: the head, then each task the previous stage's WAKE targets, until a stage wakes no one (the tail). A TIMER task that wakes no one is a chain of length one. |
| `demand` | a task's total RUN work, summed over its program; defined only when the program has no unbounded LOOP |

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

One CSV file per trace (or per recognition log), every row self-contained, nineteen columns.

**Identity** — which run the row came from.

| column | meaning |
|---|---|
| `workload_id` | the workload |
| `condition` | the recognizer condition (`fixed`, `random`, `whitelist`, `llm_vocab`, `llm_algo`, `llm_full`, `oracle`) |
| `table` | `prior` or `calibrated`; empty for `fixed`, which uses no table |
| `seed` | `random`'s PRNG seed; empty otherwise |
| `sim` | the simulator version from the trace header; empty for recognition rows |
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
| `algorithm` | `config_interval` | `MLFQ`, `EDF`, `LOTTERY`, `FIFO` |
| `index` | `config_interval` | the schedule entry's index |
| `period_us` | `job` | the TIMER period; a miss is `value > period_us`, slack is `period_us − value` |
| `predicted` | `mode_correct`, `attr_correct`, `algo_choice_correct` | what the recognizer answered |
| `truth` | `mode_correct`, `attr_correct`, `algo_choice_correct` | the answer key's value |
| `validation` | every recognition row | what the validator did with the answer |
| `familiarity` | every recognition row | the covering segment's familiarity tier, when the segment carries one |

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

**How it is computed.** Ticks are the head's `ready(cause = timer_tick)` lines. A stage's k-th iteration ends at its k-th `run_end` with reason `block`, `exit`, or `depart` — or, when the next iteration began without blocking, at the k+1-th `ready` line of that stage. The reader pairs iterations by index, which is valid because wakes queue with depth (§11).

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

### 6.9 `busy`

*How long the lane was occupied.* The sum of every task's clipped occupancy, entity `lane`, one row at `T_end`. Idle is `T_end − busy`; utilisation is `busy / T_end`.

### 6.10 Summary

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

An entry whose `proposal` is `null` (unparseable answer) grades `mode_correct` and `attr_correct` as 0 with an empty `predicted`.

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
| `busy` | utilisation `busy / T_end`; idle `T_end − busy` |
| recognition rows | mode accuracy; attribute accuracy; confusion matrix over (`truth`, `predicted`) for mode and for attribute; algorithm-choice accuracy and its confusion; latency P50/P99 over rows with `mode_correct = 1`; each also **per familiarity tier** |

Percentiles are computed on the raw values with linear interpolation. Mean is reported for sanity only, never as a headline. Counts (stimuli per task, ticks per chain) are guard inputs: stimulus count is checked against the workload's wake events, tick count against the window's tick grid.

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

**Sensitivity.** `fixed` is the boot default, whose values are stated assumptions (`../recognition-vocabulary.md` §2). The gate spec pre-registers `fixed` under two alternative boot defaults; where the sign or ordering of a share moves, the floor is reported as a range. That reporting rule is the gate spec's (Phase 7); the formula here does not change.

---

## 10. Constants

| constant | value | status |
|---|---|---|
| `T_interaction` — the perceptual threshold for interaction latency | **100 000 µs** (0.1 s) | grounded (`miller-fjcc68`, `nielsen-ue93`); see below |
| floor for latency-type aggregates (`ready_wait` mean/P50/P95/P99/max; `job` latency P50/P99; `turnaround`) | **1 000 µs** | stated assumption: half the boot default's `timeslice_us` (2 000 µs); below one half-slice, two configurations differ by less than one scheduling decision |
| floor for fraction-type aggregates (`over_threshold`, miss rate, progress, completion) | **0.01** | stated assumption: one percentage point |
| counts, provenance shares, utilisation | not normalised | guard and sanity inputs only |

**`T_interaction` = 0.1 s.** Miller (1968), Topic 1, "Response to control activation": the feedback that a key or control has been activated "should be immediate and perceived as a part of the mechanical action induced by the operator. Time delay: No more than 0.1 second"; for the echo of typed text, "the delay between depressing the key and the visual feedback should be no more than 0.1 to 0.2 seconds", with the caveat that "this delay in feedback may be far too slow for skilled keyboard users". Nielsen (1993), *Usability Engineering* ch. 5: "0.1 second is about the limit for having the user feel that the system is reacting instantaneously", which names Miller 1968 as its source. Shneiderman (1984) reports Long's 1976 finding that keystroke-echo delays of "approximately 0.1–0.5 second" already slowed both unskilled and skilled typists and raised their error rates, so 0.1 s is the loose end of the range, not a comfortable target; the percentile aggregates carry what the fraction discards. The constant applies to `ready_wait` rows with `cause = wake` on interactive tasks. It is one input to the `c1-media` weighting question in the scoring spec, not its answer.

Floors are stated assumptions and may be revised by the gate spec with a changelog entry here.

---

## 11. Simulator assumptions

The definitions above, and the mock traces that test them, assume the following simulator behaviour. Items 1–3 were sent to the simulator's owner as clarifications of the trace contract (`../memos/2026-09-07-trace-clarifications-for-the-simulator.md`); items 4–6 are mock-local choices that fill gaps the contracts leave open. A different decision on any of them changes the mocks deliberately, not the definitions.

1. A `ready` line is emitted at **every completion of a blocking primitive** (`WAIT`, `TIMER`, `SLEEP`, fork slot), at zero wait when it did not block; inside an occupancy it appears after the `run_start` and pairs with wait 0.
2. **Wakes queue with depth**: two wakes sent to a busy task complete its next two WAITs, so iteration k of every chain stage is tick k.
3. Same-instant events follow a **written, deterministic tie-break**; the mocks apply config entries first in list order, then arrivals in file order.
4. TIMER's `t₀` is the task's arrival time, so a TIMER task arriving at 0 consumes tick 0 at 0 without blocking.
5. An arriving task whose first instruction blocks is scheduled like any other, reaches the WAIT, and blocks: a zero-length occupancy when the lane is free.
6. The simulator keeps emitting `deadline` lines as the contract says; the harness uses them only as the §6.2 cross-check.

---

## 12. Mock fixtures

`harness/tools/tests/fixtures/` holds four hand-written pairs (run file, trace) with hand-computed expected records and a worked derivation each: `mock-office` (queued keystrokes, an unfocused task), `mock-media` (backlog, a same-instant config pair, a completing batch task), `mock-p1a` (config switch, preemptions, a batch task clipped at `T_end`), `mock-chain` (a three-stage frame pipeline with one late frame). They are the tests of §6 and the seeds of Phase 7's mock simulator.

---

## 13. Changelog

Every change to a primitive, an aggregate, a constant, or a floor lands here, dated, with the sub-task that made it.

- **2026-09-08 — first version (jioh 5.2).** Trace primitives §6, recognition primitives §7, aggregate list §8, per-aggregate normalisation with absolute floors §9, constants §10 (`T_interaction` grounded in `miller-fjcc68` and `nielsen-ue93`, with `shneiderman-csur84` on the range; floors as stated assumptions), simulator assumptions §11. Records take a `familiarity` attribute column for recognition rows, carried from `ground_truth` (data-contracts changelog, same date). The two definitions `../data-contracts.md` §9 deferred to this freeze — periodic job completion, and starvation from `ready` — are §6.2 and §6.1.
