# Terminology
> Status: normative · Created 2026-08-23 · Updated 2026-09-10

Terms this project uses for its own parts. Operating systems vocabulary —
MLFQ, EDF, preemption, turnaround time — is in Appendix A of
`docs/research-proposal.md` and is not repeated here.

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
See docs/workload/archetype-plan.md and docs/simulator/interpretation-contract.md.

**Records** — the harness's intermediate file: one CSV row per raw
observation computed from a trace or a recognition log, with an anchor time,
an entity, a metric, and a value. No aggregate is stored; scoring reads records
and never a trace. Defined in docs/harness/metrics.md.

**Workload variants** — each timeline compiles in two modes: `-single`
(lane-scaled; the only variant experiments run on) and `-native` (as-measured
demand; released for reuse, not executed in this work).

**meas-ci** — the source id for our CI measurement campaign
(`meas-ci:<workflow>:<run>`). Supports structural/shape claims about software
behavior only; see dataset/sources.yaml.

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
draws the timetable a computer would have produced. See `docs/background-guide.md`.

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
from `(mode, background_wanted)` to configuration. Thirty-two rows; each carries
a batch cap, a default algorithm, and one entry per algorithm (`docs/data-contracts.md`
§10). Identical across every condition that uses it: `system`-only conditions
receive the row's default, `llm_algo` the entry for the algorithm it named. It
exists because the model knows what OBS is and has never observed what a given
time slice does on this machine. Two instances: the prior table and the
calibrated table.

**Prior table** — the driver table written from scheduling theory before any
measurement: one entry per row, one sentence of justification each. Runs the
RQ0 gate and is the baseline of RQ5's fragility check. Never tuned.

**Calibrated table** — the driver table tuned per row on the disjoint throwaway
pool: four entries per row, the default being the algorithm whose tuned entry
scored best there. Produces every reported result.

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

**Primitives** — the raw observations the harness computes from a trace or a
recognition log, one row of records each: `ready_wait`, `job`, `cpu_delivered`,
`mode_correct`, and the rest. A primitive knows nothing about which file,
task role, or condition it is looking at. Changing one means recomputing from
traces.

**Scoring** — everything computed from records: aggregates, the normalisation
to a share of headroom, per-file weights, the gate. Changing scoring never
touches a trace. The records/scores boundary is the primitives/scoring
boundary.

**Entity** — whom a records row is about: a task id from the trace, or a
reserved name — `lane` (the CPU), `schedule` (the config schedule),
`recognizer` (the recognizer's answers).

**Familiarity tier** — how recognisable a process *name* is to a language
model from its training corpus, 1 (transparent: `firefox`) to 5
(nonexistent-opaque: `qzvd`), per docs/workload/building-plan.md C5. A property
of the name, never of behaviour; carried on ground-truth segments when
authored, and used only as a split key when recognition accuracy is reported.

**Counterpart (C7)** — the coreset file that instances the `false` cell of a mode, derived from that mode's C1 base by one op: an injected unwanted job (`clamscan`) in the interactive modes, the same batch job re-cast as unwanted in the batch modes. Base and counterpart are a one-diff pair, and a counterpart repeats its base's scored terms minus the batch term.

**Pre-committed miss** — a ground-truth segment whose label no recognizer can reach from names and behaviour, shipped anyway with `pre_committed_miss: true` so the limit is measured rather than claimed: the three C6 files and, on the attribute side, the segments that differ from their pair by intent alone (`c1-indexing`; the `ml-train`, `render`, `transcode`, `backup` counterparts). Excluded from accuracy and reported separately; the `oracle` condition still measures the cell's driver-table row.

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

**Mode** — what the machine is primarily doing. One of the sixteen ratified
labels in `recognition-vocabulary.md` §1 (`browsing`, `office`, `mail`, `dev`,
`photo`, `meeting`, `gaming`, `media`, `video-edit`, `compile`, `ml-train`,
`render`, `transcode`, `indexing`, `backup`, `idle`). Part of the shared
contract; a recognizer may not invent new ones. Ground truth may additionally
carry `ambiguous`, which is never on the recognizer's menu.

**Attribute** — an independent fact orthogonal to the mode label. One is
specified: `background_wanted` — whether the sustained background work is
something the user asked for. It exists because a mode label alone cannot
separate gaming during a wanted download from gaming during an unwanted scan.
`recognition-vocabulary.md` §1; proposal §4.4.3.

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
