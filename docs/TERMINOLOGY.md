# Terminology

Terms this project uses for its own parts. Operating systems vocabulary —
MLFQ, EDF, preemption, turnaround time — is in Appendix A of
`RESEARCH_PROPOSAL_v2.md` and is not repeated here.

---

## Where everything sits

```text
   WORKLOAD                                    a file, compiled from a timeline
      |
      +--> names + cmdlines ---> RECOGNIZER          a component
      |                              |
      |                          PROPOSAL            data
      |                              |
      |                          VALIDATOR           a component
      |                              |
      |                          DRIVER TABLE        a lookup
      |                              |
      |                          CONFIG              data
      |                              |
      +--> patterns ----------> SIMULATOR            a component
      |                              |
      |                          TRACE               data
      |                              |
      +--> ground truth -------> HARNESS             a component
                                     |
                                  METRICS            data
```

Reading it once from the top: a workload file is split three ways; the
recognizer turns names into a proposal; the validator makes the proposal safe;
the driver table turns it into a config; the simulator runs against that config
and emits a trace; the harness turns traces and proposals into metrics.

---

## Artifacts

**Workload** — the experiment-ready canonical file: which processes exist, when
they start, how they behave, and what the true situation is. It is the
experiment itself, not an input to the experiment. Compiled from a timeline —
never hand-edited. Example in section 5.5.

**Timeline** — the human-facing authoring file a workload is compiled from:
segments with labels, plus (name, archetype) bindings on a time axis. Core
timelines are hand-authored; naturalistic timelines are emitted by the
generator. `archetypes.yaml + timeline (+ scenario catalog) + seed → workload`.

**Archetype** — a sourced generative model of how one process kind behaves, as
the scheduler sees it: a program over the six-primitive event grammar plus
parameter distributions. Layer 1 of the dataset; never carries a process name.
See ARCHETYPE_LIBRARY_PLAN.md and INTERPRETATION_CONTRACT.md.

**Workload variants** — each timeline compiles in two modes: `-single`
(lane-scaled; the only variant experiments run on) and `-native` (as-measured
demand; released for reuse, not executed in this work).

**meas-ci** — the source id for our CI measurement campaign
(`meas-ci:<workflow>:<run>`). Supports structural/shape claims about software
behavior only; see workload-dataset-sources.yaml.

**Pattern** — the part of a workload entry describing how a process behaves:
its CPU bursts, its sleeps, and for periodic work its period and deadline. A
pattern is a script the process follows regardless of what the scheduler
decides. Visible only to the simulator.

**Ground truth** — the part of a workload stating what situation the machine is
genuinely in, as a timeline of mode and attributes. Visible only to the oracle
condition and to the Layer 1 grader. Never visible to any recognizer.

**Telemetry** — what the machine reports about itself: process names, command
lines, coarse counts. This is the only view of the machine any recognizer gets.
What it excludes is deliberate: no PIDs, no patterns, no ground truth. The
exclusions are enforced by the shape of the telemetry, not by prompt wording
(section 8.2, decision 6).

**Proposal** — a recognizer's complete output: reasoning, situation
description, the `system` block, and the `subsystems` block. Example in
section 4.3.

**System block** — the part of a proposal that describes the world rather than
any subsystem: mode plus attributes. Every consumer reads it. This is the
shared contract.

**Subsystems block** — a namespace in a proposal, one key per consumer. This
project fills exactly one key. Adding a consumer adds a key and changes nothing
else.

**Config** — what a scheduler actually runs against: an algorithm plus its
parameters plus per-class bandwidth caps. Which parameters exist depends on
which algorithm was chosen, so validation branches on the algorithm rather than
checking a flat field list.

**Config schedule** — the sequence of configs a single run will apply, with the
times they take effect. If recognition is precomputed rather than live (Q2),
this is the file the simulator consumes, and it is the only thing that differs
between conditions.

**Trace** — the simulator's output. An event stream recording which process
held the CPU when, which deadlines were met, and when configs were proposed and
applied. Every performance metric is a read over this stream; nothing is timed.
Example in Appendix B.

---

## Components

**Simulator** — the discrete-event engine. Advances a virtual clock from one
event to the next, never in real time, and never executes any real work. It
draws the timetable a computer would have produced. See `SIMULATOR_PRIMER.md`.

**Executor** — the part of the simulator that applies a config: assigning
processes to classes, enforcing bandwidth caps, holding the starvation floor.
It must be byte-identical across every condition. Section 5.1 rests entirely on
this.

**Algorithm** — one of MLFQ, EDF, lottery, FIFO, behind a single interface. The
config selects which is active.

**Policy daemon** — the process that turns telemetry into a config. Contains
the recognizer, the validator, and the driver.

**Recognizer** — the only part swapped between conditions. It reads telemetry
and produces a proposal. `fixed`, `random`, `whitelist`, the LLM variants, and
`oracle` are all implementations of one interface.

**Validator** — the trust boundary. Checks a proposal against the schema,
clamps out-of-range values, rejects unknown keys and labels, falls back when a
proposal is unusable, and stamps every result with provenance. Section 4.7
lists what a proposal may never do.

**Driver** — a consumer's adapter: it translates the shared vocabulary into its
own configuration. The analogy is a device driver. The kernel does not know
what a driver does internally; drivers do not know about each other. Section
4.4.2.

**Driver table** — this project's CPU driver, implemented as a static lookup
from mode and attributes to config. Roughly twenty rows, hand-written and tuned
offline. Identical across every condition that uses it. It exists because the
model knows what OBS is and has never observed what a given time slice does on
this machine.

**Harness** — the experiment runner. Executes the matrix, grades recognition
against ground truth, computes performance metrics from traces, and produces
reports.

**Search engine** — the part of the harness that runs many configs against one
workload and keeps the best. Used twice: to tune the driver table offline, and
to produce the perfect-configuration diagnostic.

---

## Experiment vocabulary

**Condition** — one row of the experiment ladder. Concretely, a function from a
workload to a config schedule. `fixed`, `random`, `whitelist`, `llm_vocab`,
`llm_algo`, `llm_full`, `oracle`. Section 5.2.

**Variant A, B, C** — the three levels at which the LLM is given authority.
A fills the system block only and the table does the rest. B also names the
algorithm. C fills the whole config and bypasses the table. The ladder is how
RQ3 is answered. Section 4.6.

**Whitelist** — the condition that reproduces what shipping operating systems
do today: hardcoded matching on known executable names. Not a strawman; it is
the baseline the paper has to beat, and it is expected to win on well-known
software.

**Oracle** — a recognizer that reads ground truth from the workload file
instead of inferring it. Perfect recognition, not perfect configuration; the
two are distinguished below.

**Layer 1** — recognition accuracy. A proposal's system block compared against
ground truth labels. No simulator involved, so scheduling heuristics cannot
contaminate it.

**Layer 2** — consumer performance. Metrics computed from traces across the
condition ladder.

**Perfect recognition** — the result of feeding ground-truth labels through the
shared driver table. The upper bound for every condition that passes through
that table, and the denominator for grading.

**Perfect configuration** — the best result the search engine can find on a
workload, ignoring labels entirely. No model is involved. It bounds what any
config could achieve, and is reported as a diagnostic rather than used as a
denominator.

**Headroom** — the improvement available on a workload, measured from the
`fixed` condition. It splits exactly in two: recognition headroom, from `fixed`
to perfect recognition, and table headroom, from perfect recognition to perfect
configuration. A condition's shortfall decomposes the same way, which is what
lets a result say how much of a miss was the model and how much was the table.
Q6 of the archived open-questions record
(`_dev/archive/2026-08-23-design-meeting-open-questions.md`).

---

## Signal vocabulary

**Mode** — what the machine is primarily doing. One of `interactive`, `gaming`,
`compile`, `media`, `idle`. Part of the shared contract; a recognizer may not
invent new ones.

**Attribute** — an independent fact orthogonal to the mode label. Two are
specified: `has_realtime_encoder` and `background_is_wanted`. They exist
because five labels cannot express the distinction between gaming, gaming while
streaming, and gaming during a download. Section 4.4.3.

**Admission test** — the rule deciding whether a candidate term belongs in the
shared vocabulary: it must be meaningful to more than one consumer, and not
derivable from behavioural observation. A term only one consumer can act on is
that consumer's configuration, not vocabulary. Section 4.4.4.

**Provenance** — how an applied config was produced: unmodified, clamped, held
from a previous cycle, or fallback. Reported alongside every performance
figure. A condition that scored well while most of its configs were fallbacks
demonstrated nothing about recognition.

**Configuration age** — how old the underlying observation was when a config
took effect. Measured from the moment telemetry was snapshotted to the moment
the new config became active.

---

## Timing

**Virtual time** — the simulator's clock. It jumps from event to event and
bears no relation to real elapsed time.

**Slice** — how long a process may run before the scheduler reconsiders.
Typically single-digit milliseconds.

**Drain** — waiting for the current slice to finish before applying a new
config, rather than preempting mid-slice.

**t_observe, t_return, t_apply** — the three instants around a config change:
when telemetry was snapshotted, when the daemon's answer landed, and when the
new config became active after the drain. Configuration age is measured from
the first to the last. Q3 of the archived open-questions record
(`_dev/archive/2026-08-23-design-meeting-open-questions.md`).
