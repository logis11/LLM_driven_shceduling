# Open Design Questions

Questions raised while sketching the module design. Each needs a team decision.
Nothing here is settled.

---

## Module sketch

The layout the questions below hang off. Not settled either.

```text
              WORKLOAD DEFINITION  (the experiment itself)
       +--------------+------------------+--------------+
       | names +      | burst / sleep    | ground-truth |
       | cmdlines     | patterns         | timeline     |
       +------+-------+--------+---------+------+-------+
              |                |                |
       only recognizer   only simulator   only oracle and
       sees this         sees this        grader see this
              |                |                |
              v                v                v
   +-------------------+  +-----------+   +-------------+
   |  POLICY DAEMON    |  | SIMULATOR |   |   HARNESS   |
   |     Python        |  |    C++    |   |   Python    |
   +---------+---------+  +-----+-----+   +------+------+
             |  config          | trace          |
             +------------------+----------------+
                        drives everything
```

The information asymmetry of section 5.5 is enforced by which module receives
which slice of the workload file, not by prompt wording.

### Policy daemon

```text
   telemetry in
        |
        v
   +-------------------------------------+
   | RECOGNIZER   the only swapped part  |
   |  fixed | random | whitelist | llm    |
   |  | oracle                            |
   |        prompt . model client         |
   |        (hosted API and local, one    |
   |         interface)                   |
   +------------------+------------------+
                      | proposal
                      v
   +-------------------------------------+
   | VALIDATOR    schema, clamp, fallback|
   | + PROVENANCE stamp                  |
   +------------------+------------------+
                      | system block
                      v
   +-------------------------------------+
   | CPU DRIVER   (mode, attrs) -> config|
   +------------------+------------------+
                      v  config out
```

Two stages fixed, one swapped. That is the experiment expressed as code.

The driver table sits downstream of the validator, inside the daemon. It must
be identical for `random`, `whitelist`, `oracle` and variant A, and the
simulator never learns that a recognizer exists.

A consequence worth stating plainly: a condition is a function from a workload
to a configuration schedule. Seven producers, one simulator binary.

### Simulator

```text
   config in --->+--------------------------------+
                 | EXECUTOR   identical always    |
                 |  class assignment . bandwidth  |
                 |  caps . starvation floor       |
                 +---------------+----------------+
                                 | selects
                 +---------------v----------------+
                 | ALGORITHMS  MLFQ EDF LOT FIFO  |  one interface
                 +---------------+----------------+
                 +---------------v----------------+
                 | EVENT ENGINE   virtual clock   |
                 | PROCESS MODEL  scripted bursts |
                 |                one RNG stream  |
                 |                per process     |
                 +---------------+----------------+
                                 v  trace out
```

The executor is the part that must never vary across conditions (section 5.1).

### Harness

```text
   matrix runner  --->  condition x workload x seed x repeat
        |
        +---> LAYER 1 grader   proposal vs ground truth, no simulator
        +---> LAYER 2 metrics  read off the trace
        +---> search engine    tunes the driver table, and produces
        |                      the perfect-configuration diagnostic
        +---> report and plots
```

The search engine drives the simulator repeatedly, so it belongs here rather
than in the daemon.

### Shared contracts

```text
   telemetry out . proposal in . config . workload file . trace
```

Not a module, but the artifact that decides whether the three areas can be
built in parallel. Section 8.3 requires it frozen early.

### Tech stack

| Component | Language | Rationale |
|---|---|---|
| Simulator | C++ | logic carries over to a `sched_ext` port; deterministic |
| Policy daemon | Python | prompts change constantly; model SDKs live here |
| Harness | Python | pandas and matplotlib |
| Wire format | JSON | survives the simulator being replaced by a real kernel |
| Workload files | YAML | hand-authored and human-reviewed |
| Model hosting | one client interface, two backends | hosted API for iteration, local quantised model for the measurements in the paper |

---

## Q1 — One core, or several?

The simulator primer assumes a single lane. The decision should be deliberate,
because core count changes the size of the effect being measured.

### What multi-core adds

```text
  SINGLE CORE                        MULTI-CORE
  scheduler = who runs next          + load balancing
                                     + migration cost
                                     + affinity and cache warmth
                                     + per-core queues
```

### Effect on the measurable gap

```text
  game (9ms of CPU per 16ms frame) + encoder + download

  on 1 core   they contend. the scheduler decides who loses.
  on 8 cores  everyone fits. the scheduler barely matters.
```

Section 5.3 makes the experiment conditional on a large gap between the random
and oracle recognizers. Additional cores shrink that gap by removing the need
to choose. Single core is where recognition quality is most visible.

EDF optimality also holds only on a single core.

### The objection

A reviewer will observe that the effect depends on a one-core machine while
real machines have eight or more.

### Options

```text
  (i)   single core, stated as scope
  (ii)  single core, with workloads whose total demand clearly exceeds
        one core, framed as the same contention regime as N cores
        carrying 3N worth of work
  (iii) N cores, global queue, no migration cost
```

**Current lean:** build (i), frame with (ii). Workloads are designed so total
demand exceeds one core, and the core count is stated as a deliberate choice
rather than left implicit.

---

## Q2 — Are the simulator and the daemon ever alive at the same time?

The simulator finishes a simulated hour in under a second. The daemon needs
hundreds of real milliseconds to answer once. They do not share a clock.

```text
   virtual time  |-------------------------------------|  1 hour
   real time     |-|                                       0.5 s
   daemon        |----------|                              0.6 s per answer
```

### Option A — live connection

```text
  SIM                              DAEMON
  virtual t=5000
  process set changes
       |  telemetry ----socket---->  prompt -> model -> validate -> map
       |  <---socket---- config + measured latency
  schedules config to take effect at virtual t = 5000 + measured latency
```

Real time is discarded; the measured latency is re-injected as virtual delay.

### Option B — precomputed timeline

The daemon's input is process names and launch times, which come from the
workload file and are therefore known before the simulator runs.

```text
  STEP 1  daemon alone   workload -> queries -> config schedule file
                            t=0     -> default
                            t=5600  -> EDF, cap 0.12, clamped

  STEP 2  simulator alone  reads the schedule as an input file
```

### Trade-off

| | A live | B precomputed |
|---|---|---|
| Build cost | protocol, async, failure handling | a file format |
| Determinism | requires care | free |
| Re-running the matrix | slow | instant |
| Deployment story | resembles a real system | offline experiment |

Both produce identical numbers.

### What forecloses B

B depends on the process timeline being independent of scheduling. Any
feedback from scheduling back into the workload creates a cycle:

```text
   config -> scheduling -> perceived lag -> user closes app -> process set
      ^                                                             |
      +-------------------------------------------------------------+
```

Two consequences. The config timeline can no longer be computed in advance.
And each condition produces a different process timeline, so conditions no
longer face identical workloads, which section 6.4 requires.

Accepting B means the experiment cannot model outcomes such as a user
abandoning a task because the machine felt slow.

**Current lean:** B.

---

## Q3 — What happens inside the simulator when a config lands mid-run?

At some virtual time the algorithm changes. Processes are already running and
already sorted into the outgoing algorithm's structures.

```text
        MLFQ state                          EDF state
   +------------------+              +-------------------+
   | Q0  bash, discord|   switch     | sorted by nearest |
   | Q1  steam        |  --------->  | deadline          |
   | Q2  cc1plus x8   |      ?       |                   |
   +------------------+              +-------------------+
```

The question has two independent halves.

**When does the switch happen?**

```text
  immediate    preempt whatever is running
  drain        finish the current time slice, then switch
```

**What carries across it?**

```text
  nothing      new algorithm starts cold
  mapped       translate outgoing state into incoming state
```

### Why it matters

Only transitions carry information (section 7). A switch that is free may
overstate the benefit. A switch that is lossy penalises the frequent-transition
workloads that answer RQ4, through an artifact of our own design.

### State each algorithm requires

| Algorithm | State needed | Source |
|---|---|---|
| EDF | deadlines | process model |
| Lottery | tickets | config |
| FIFO | arrival order | known |
| MLFQ | queue level | observed behaviour |

Only MLFQ loses anything on a cold start, and it rebuilds queue level by
demotion within a few time slices.

### Trade-off on the second half

Mapping outgoing state to incoming state requires inventing a correspondence
such as queue level to deadline urgency. Starting cold requires no invented
rule and makes the LLM conditions marginally worse rather than better.

**Current lean:** drain to a slice boundary, then start cold.

Independent of the choice: emit a trace event at every algorithm change, so the
harness can report how much of each run was spent immediately after a switch.

### Q3 follow-up — which instant does a config trace event record?

Three instants are distinct and separately meaningful.

```text
  t_observe          t_return              t_apply
     |                  |                     |
     |  model thinking  |  draining the slice |
     |----------------->|-------------------->|
     |      ~600 ms     |       <=10 ms       |
     |                                        |
     +--------- configuration age ------------+
```

- `t_observe` — process set changed, telemetry snapshotted
- `t_return` — daemon's answer lands
- `t_apply` — after the drain, new algorithm active

Configuration age (section 6.3) is measured to `t_apply`.

**Proposal:** emit two events rather than one.

```text
  at t_return   config_proposed   algorithm, params, provenance,
                                  and the t_observe it was based on
  at t_apply    config_applied    which proposal took effect
```

Not every proposal becomes an application. A held proposal never applies, and a
fallback may be a no-op. Logging only at `t_apply` erases them, and section 6.3
requires the provenance breakdown to accompany every performance figure.

Edge case to define: if a second config returns while the first is draining,
last write wins on the pending slot.

---

## Q4 — How is the driver table built in the first place?

Section 4.6 states that the table is hand-tuned offline. It does not state
against what. The table is section 8.2 decision 3, and every conclusion about
RQ2 and RQ3 is measured through it.

### What the table is

Roughly twenty rows. Each answers one question: given this situation, what
should the scheduler do.

```text
  SITUATION                          CONFIG
  gaming, encoder=no, wanted=yes  -> EDF, cap 0.12
  gaming, encoder=no, wanted=no   -> EDF, cap 0.02
  compile, wanted=yes             -> FIFO, long slice
  interactive                     -> MLFQ, default
```

The build problem is where the right-hand values come from.

### The overfitting exposure

```text
  tune the table on the evaluation workloads
       |
  the table has seen the test set
       |
  variant A and the oracle condition both inherit that knowledge
```

Section 4.6 argues that tuning the table offline makes variant A a stronger
experiment rather than a weaker one. That holds only if the tuning did not see
the workloads the results are reported on.

### The ordering constraint

```text
  the Phase 1 gate needs the oracle condition
  the oracle condition needs the table
  tuning the table needs the search engine
  the search engine needs the simulator
```

A tuned table cannot exist before the gate, and should not.

---

### Proposal: build it twice, in five steps

```text
  1  write v0 by hand              theory only, no data
  2  run the Phase 1 gate with v0  may stop the project here
  3  write throwaway workloads     separate from the evaluation set
  4  search each row against them  produces v1
  5  freeze v1, run the matrix     on the evaluation workloads
```

#### Step 1 — v0 from theory

Each row is reasoned out, not measured. Search moves only the constants later.

```text
  (gaming, encoder=false, wanted=true)
     frame deadlines dominate          -> EDF
     download is wanted, must progress -> batch cap nonzero
     but must never cost a frame       -> cap small

  (gaming, encoder=false, wanted=false)
     same deadlines                    -> EDF
     background nobody asked for       -> cap at the starvation floor,
                                          not zero (section 4.7)

  (compile, wanted=true)
     throughput wants long slices      -> FIFO in the contended class
     the shell must stay alive         -> interactive class unchanged
```

The last row shows that the algorithm applies inside a fixed class structure
rather than globally. Section 4.7 already forbids altering priority ordering
between classes, so a row is an algorithm for the contended class, its
parameters, and the per-class caps.

The constants in v0 are guesses. That is acceptable, because v0 is not used for
any performance claim.

#### Step 2 — the gate runs on v0

The Phase 1 gate compares a random recognizer against the oracle condition, and
the oracle condition needs a table. v0 is that table.

v0 may be run against the evaluation workloads freely. It was tuned against
nothing, so there is nothing to contaminate.

If the gate fails, the project stops and v1 is never built.

#### Step 3 — the tuning workloads

During tuning no model runs. Nothing reads process names. The tuning workloads
are therefore behaviour plus a label, with generic names and no command lines.

```text
  EVALUATION workload                TUNING workload
  the model reads the names          nothing reads the names
  names must be believable           names are placeholders
  reported                           never reported
```

Full example for one row, `(gaming, encoder=false, wanted=true)`. Illustrative:
only the workload file of section 5.5 is specified.

```yaml
name: tune_gaming_wanted_02
set: tuning
duration_ms: 30000
primary_metric: p99_frame_latency_ms

ground_truth:
  - t_ms: 0
    mode: gaming
    has_realtime_encoder: false
    background_is_wanted: true

processes:
  - name: proc_a                 # stands in for the game
    start_ms: 0
    pattern:
      type: latency_critical
      period_ms: 16
      deadline_ms: 16
      cpu_burst_ms: [4, 9]

  - name: proc_b                 # stands in for a chat client
    start_ms: 0
    pattern:
      type: interactive
      cpu_burst_ms: [1, 4]
      io_wait_ms: [100, 800]

  - name: proc_c                 # stands in for the wanted download
    start_ms: 0
    pattern:
      type: io_heavy
      cpu_burst_ms: [2, 10]
      io_wait_ms: [1, 5]
```

Three variants per row, differing in one knob only.

```text
             deadline process   background   interactive   total demand
  01 light   burst [3, 6]        ~70%         ~2%          ~100%
  02 medium  burst [4, 9]        ~70%         ~2%          ~113%
  03 heavy   burst [8, 14]       ~70%         ~2%          ~141%
```

Every variant exceeds one core. A variant that fits comfortably gives the
scheduler nothing to decide, and that row of the search returns noise. This is
Q1's oversubscribed framing made concrete.

Only the deadline process's demand varies. Period, deadline, background greed
and duration are held fixed, so a change in the winning config is attributable
to one cause.

Two constraints worth stating:

- No command lines, and placeholder names. This is a guard rather than
  laziness. Real software names in the tuning pool could be pointed at a
  recognizer by accident, and the separation from the evaluation set would leak
  silently.
- The same `primary_metric` as the evaluation workloads for that situation. A
  constant tuned on the mean and reported on the tail was optimised for the
  wrong thing.

#### Step 4 — the search

Per row, sweep candidate configurations across that row's tuning workloads and
keep the best average.

```text
  ROW: (gaming, encoder=no, wanted=yes)

                   | tune_01 | tune_02 | tune_03 |  avg
  EDF cap 0.02     |   19    |   22    |   31    |  24.0
  EDF cap 0.05     |   12    |   14    |   21    |  15.7   <- winner
  EDF cap 0.12     |   14    |   18    |   24    |  18.7
  EDF cap 0.30     |   21    |   26    |   34    |  27.0
  MLFQ tuned       |   30    |   35    |   44    |  36.3
  FIFO             |   80    |   88    |  101    |  89.7

  ROW: (gaming, encoder=no, wanted=yes) -> EDF, cap 0.05
```

Averaging across load levels is what makes the constant a property of the
situation rather than of one burst range.

Rows no tuning workload reaches keep their v0 values.

#### Step 5 — freeze and run

```text
  +-- step 3 ------------+        +-- step 5 --------------+
  | TUNING workloads     |        | EVALUATION workloads   |
  | placeholder names    |        | real software names    |
  | ~3 per row           |        | the section 5.5 set    |
  +----------+-----------+        +-----------+------------+
             |                                |
        step 4 search                    the experiment
             |                                |
             v                                v
       +-----------+                    +-----------+
       |  v1 TABLE |------------------->|  results  |
       +-----------+  frozen, unchanged +-----------+

       the two workload pools never meet
```

---

### Which table each result uses

```text
  v0   untuned, from theory
       Phase 1 gate                          RQ0
       reported beside v1                    RQ5

  v1   tuned on the throwaway pool
       the condition ladder                  RQ2, RQ3
       the transition sweep                  RQ4
       table headroom                        RQ5

  no table at all
       Layer 1 recognition accuracy          RQ1
```

RQ1 never touches the table. Layer 1 compares labels against labels with no
simulator involved, which is why section 5.4 separates the two layers.

### Two consequences

**v0 is not discarded.** Running the ladder on both tables costs one extra
sweep and answers most of RQ5 directly. If v0 and v1 score alike, the table is
not a fragile artifact and no reader can claim the result hinges on tuning
choices. If v1 is far better, the size of the gap is itself worth reporting.

**Re-run the gate on v1.** The gate asks whether there is room to measure
anything. The honest version of that question uses the table the experiment
actually runs on.

```text
  gate on v0   early, cheap, may stop the project
  gate on v1   the figure that goes in the paper
```

### Row count

Some combinations are unreachable, such as an idle mode carrying a real-time
encoder. Others are reachable but produced by no workload. Both still need an
entry, because an unreachable row reached at runtime is a validator event
rather than a crash, but both take textbook defaults and never enter the
search.

Counting the rows any workload actually exercises gives the real size of
section 8.2 decision 3, and the real size of the tuning pool: roughly three
files per reachable row, most of them one file with different numbers.

---

## Q5 — The ladder needs two ceilings, and the proposal names only one

Two sentences in the proposal describe different machines under the same word.

```text
  section 5.2   oracle = ground truth from the workload file, fed to the
                         driver table
  section 7     oracle = searches up to 80 combinations per workload segment
                         (5 modes x 2 attrs x 2 attrs x 4 algorithms)
```

The first is perfect recognition. The second is a search over configurations.

### The two ceilings

```text
  PERFECT RECOGNITION                 PERFECT CONFIGURATION
  read the true mode and attributes   ignore labels entirely, run every
  from the workload file, then use    config against the workload, keep
  the same driver table as everyone   whichever measured best
  cost: free                          cost: 80+ sim runs per segment
```

### Why one number cannot score the ladder

Variants A and B pass through the shared driver table. Perfect recognition
plus that table is therefore their exact upper bound; they cannot exceed it.

Variant C bypasses the table and emits configuration directly. It is bounded
only by what any configuration can achieve, so it can land on either side of
the perfect-recognition figure.

```text
   perfect configuration ---------- perfect recognition ---------> worse
            |                              |
            +-------- C can be here -------+------ A, B only here ------
```

Scoring A against the configuration ceiling attributes the driver table's
shortfall to the model. Scoring C against the recognition ceiling cannot
express the outcome where C exceeds it.

### What each comparison answers

| Comparison | Question |
|---|---|
| A vs perfect recognition | did the model read the situation correctly |
| C vs perfect recognition | did generated constants beat the hand-written table |
| C vs perfect configuration | total headroom on this workload |
| perfect recognition vs perfect configuration | is the driver table itself any good |

The last row is a check on the instrument. Section 4.6 claims that tuning the
table offline makes variant A a stronger experiment. That claim holds only if
the gap between the two ceilings is small.

### Practical note

Section 4.6 specifies that the driver table is hand-tuned offline. Tuning means
running configurations against workloads and keeping what wins, which is the
same search that produces the configuration ceiling. One tool, used twice. It
drives the simulator repeatedly, so it belongs in the harness.

**Needs deciding:** whether both ceilings enter the paper, and reconciling the
two uses of the word in sections 5.2 and 7.

---

## Q6 — Grading strategy across heterogeneous workloads

Each workload is scored on a different metric, so raw values cannot be averaged.

```text
  workload            primary metric
  gaming + download   P99 frame latency     ms, lower better
  parallel compile    throughput            jobs/sec, higher better
  document + mail     response time         ms, lower better
  DAW + plugins       deadline miss rate    %, lower better
```

The workload file declares its own primary metric. Otherwise the harness
guesses, or a separate table exists and drifts from the workloads.

### Three measuring instruments, easily confused

```text
  1  LAYER 1 ACCURACY       LLM labels vs ground-truth labels.
                            No simulator. Output: mode and attribute
                            accuracy. This is what measures whether the
                            model reads the situation correctly.

  2  PERFECT RECOGNITION    Ground-truth labels fed to the shared driver
                            table, then simulated. Not a test of the model.
                            It is the upper bound for every condition that
                            passes through the table.

  3  PERFECT CONFIGURATION  No labels. Brute-force search over algorithms
                            and parameters, best measured result kept. The
                            model appears nowhere. It bounds what any
                            configuration could achieve.
```

Two research questions map onto the first two.

```text
  RQ1  can the model read the world?     instrument 1, and the distance
                                         from a condition to instrument 2
  RQ2  does reading it help?             the gap between `fixed` and
                                         instrument 2 (the section 5.3 gate)
```

Instrument 3 belongs to neither. It is a check on the driver table, and
therefore on whether the other two can be trusted.

### Why the two ceilings cannot share a denominator

A normalised score has the form `(fixed - condition) / (fixed - ceiling)`.

Variants A and B pass through the driver table, so perfect recognition is
their exact upper bound. Grading them against perfect configuration caps them
below 1.0 by construction, and the unreachable band reads as shortfall.

Variant C bypasses the table and is bounded only by perfect configuration.
Grading it against perfect recognition permits scores above 1.0.

```text
  perfect configuration ---------- perfect recognition ---------> worse
           |                              |
           +-------- C can be here -------+------ A, B only here ------
```

### Resolution

**Variant C is demoted from a scored rung to a subset diagnostic.** It runs on
a representative subset of workloads and is reported alongside instrument 3,
not on the ladder. Section 7 already applies this pattern to the oracle.

Consequences: every remaining condition passes through the same driver table,
so perfect recognition is the single denominator and the grading asymmetry
disappears. Instrument 3 stops being a denominator and becomes a diagnostic.

What is given up: RQ3 asks whether the vocabulary is sufficient or whether the
consumer needs configuration handed to it directly. The subset run is evidence
for the second half rather than a full-matrix result.

### The loss decomposition

Total headroom splits exactly into two named components.

```text
  fixed                perfect recog        perfect config
   42 --------------------> 18 ----------------> 14
   |                        |                    |
   +------- 24 ------------>+-------- 4 -------->|
     recognition headroom     table headroom
   +--------------- 28 --------------------------+
                total headroom
```

```text
  total headroom = recognition headroom + table headroom
       28        =         24           +       4
```

Per condition, the same identity attributes a condition's shortfall.

```text
  A scores 20:
      20 - 14  =  (20 - 18)  +  (18 - 14)
         6     =      2      +      4
                        |           |
                   A misread   the table's limit
```

Reported as fractions of total headroom: A captured 79%; of the 21% it missed,
7% is recognition and 14% is the table.

The decomposition is exact, not an approximation. It requires two conditions:
the search space producing perfect configuration must contain every row of the
driver table, and the metric must be one where differences are meaningful.

### Worked example

The Family 2 pair. Behaviourally identical, opposite correct policy.

```text
  WORKLOAD P   LoL (16ms deadline) + Discord + Steam download
               ground truth: gaming, encoder=false, wanted=TRUE
               correct policy: throttle the download, never starve it

  WORKLOAD Q   LoL (16ms deadline) + Discord + antivirus full scan
               ground truth: gaming, encoder=false, wanted=FALSE
               correct policy: defer the scan freely
```

Layer 1 on P, ten runs: mode correct ten times, attribute correct nine times.
Reported alone, before any simulation.

Ladder on P (illustrative numbers, P99 frame latency in ms):

```text
  fixed                       42
  random                      33
  whitelist                   19
  A  llm_vocab                20
  B  llm_algo                 19
  ---------------------------------
  perfect recognition         18     denominator
  perfect configuration       14     diagnostic
  C  (subset)                 24     diagnostic
```

The pair, side by side:

```text
                        P (wanted)      Q (unwanted)
  fixed                     42              38
  whitelist                 19              24
  A  llm_vocab              20              16
  perfect recognition       18              15
  perfect configuration     14              12
```

On P the whitelist ties with A. On Q they are eight milliseconds apart. The
whitelist recognises a known game name, fires, and applies the same
configuration to both workloads, because a name list cannot express why the
background work exists.

### Reporting rules

```text
  per workload   its declared primary metric, raw value.
                 never averaged across workloads in raw units.

  summary        percentage of headroom captured, graded against
                 perfect recognition. negative values shown, never
                 clipped: scoring worse than `fixed` is a finding.

  loss split     recognition-attributable vs table-attributable.

  diagnostics    perfect configuration per workload. a large table
                 headroom means A and B are being judged on a poor
                 table and conclusions about them are suspect.

  provenance     alongside every performance figure (section 6.3).

  split          well-known vs unregistered software (section 5.5).
```

---
