# Research Claims and Questions
> Status: normative · Created 2026-08-23 · Updated 2026-10-17

What this project asserts, what would falsify it, and what it does not claim.

RQ0 through RQ5 are section 3 of `docs/research-proposal.md`, restated with the
reasoning behind them. The mechanism split under RQ1 and RQ2 is a proposed
addition and is marked as such.

---

## The claim

The proposal's headline claim:

> The meaning of a workload lives in the combination of processes, not in any
> single one of them. That combination cannot be enumerated in a lookup table,
> and reading it requires knowing what the software is for — knowledge a
> language model already has and an operating system does not.

The form the experiment can put at risk:

> On workloads where the correct policy differs and neither behaviour nor
> declared class settles it, a language model reading process names recovers
> the difference, and the strongest name table cannot.

The second is what the results section defends. The first is what it implies.

---

## The chain

The claim is not one proposition. It is seven links, each failing
independently.

```text
  link 1  there exist realistic situations where the correct config
          differs, and the difference is measurable
                                                  no model involved
  link 2  some of those differences are invisible to behavioural
          observation
                                                  no model involved
  link 3  they are present in the process names, their counts and
          which process holds the window focus
                                                  no model involved
  ------------------------------------------------------------------
  link 4  a language model can read them                     RQ1
  link 5  reading them beats what shipping systems do        RQ2
  link 6  stably and quickly enough to be a system component RQ4
  ------------------------------------------------------------------
  link 7  the signal generalises to other consumers  RQ3, argued only
```

Link 3 is what the recognizer is shown: the name → count multiset and the
focus holder (none when no window holds the focus). Behaviour, labels and PIDs
stay out of it.

Links 1 through 3 are properties of the workload space rather than of language
models. Phase 1's committed spec (`harness/experiments/rq0-gate.yaml`) tests
link 1, by RQ0: `random` against perfect recognition, before any prompt exists.
Link 3 is held by how the dataset is built, and its limits are measured by the
pre-committed misses: the segments shipped with `pre_committed_miss: true`
because no recognizer can reach their label from names and behaviour; the
headline accuracy excludes them and a second reported line includes them.
Link 2 has no falsification condition yet. If link 1 fails, no model recovers
the paper. This is why section 5.3 is a gate rather than a milestone.

Link 7 is argued in section 4.4.4 and demonstrated nowhere, because the project
builds one driver. Section 7 already states this as the proposal's most
significant weakness.

---

## Two mechanisms, currently measured as one

Sections 2.3 and 2.4 argue two different reasons a name table fails. The
research questions treat them as one.

```text
  MECHANISM 1 -- combination
  Discord means something different depending on what runs beside it.
  A flat list cannot express context.
        tested by Family 2, jobs that differ in intent beside
        the same situation

  MECHANISM 2 -- world knowledge
  A Godot-built indie game is a game that nobody registered.
  A finite list cannot cover software it never enumerated.
        tested by Family 3, unregistered software
```

They are separable results with different consequences.

```text
  only M1 holds   extend the name-keyed catalogue to read
                  combinations. a feature request, not an
                  architecture.

  only M2 holds   the list is the problem, but a longer list or
                  application self-declaration is a cheaper fix
                  than inference.

  both hold       neither cheap fix is available. this is the
                  argument for a recognition layer.
```

Section 5.5 already requires results split by software familiarity, which
separates M2. The dataset's material for it is the familiarity ladder
(`familiarity-ladder`, 66 generated files): tiers 4 and 5 over the sixteen
modes in three carrier forms — the focus holder's name, the other names, every
name — and two tier-3 cells, render's `melt-7` and backup's `duplicity`;
tier 3 is otherwise the single-situation calibration files (C1) whose
programs already carry an opaque real name (`cc1`, `tracker-miner-f`, the game
chain's members). Nothing currently separates M1. **Proposed:** report the
combination axis explicitly, not only the familiarity axis.

---

## The research questions

### RQ0 — Does configuration matter on these workloads at all?

Compare a random recognizer against perfect recognition, with no model in the
loop. If a perfect recognizer scores close to a random one, no recognizer can
demonstrate anything.

The named failure mode: per-class heuristics strong enough to self-correct
misclassification. Put a compiler in the interactive class and MLFQ demotion
moves it within a few slices anyway. The heuristics do not steal credit from
the model; they eliminate the variance being measured.

Runs before any prompt exists. Cheapest possible falsification of the whole
premise.

### RQ1 — Can a model read the situation from the process names and the focus holder?

Layer 1: the proposal's system block against ground-truth labels, with no
simulator involved, so scheduling heuristics cannot contaminate the result.

Reported as mode accuracy, per-attribute accuracy separately, a confusion
matrix, and **run-to-run consistency on identical input**. Split by the two
mechanisms above. Every condition can run under both telemetry shapes — the
focus holder shown (`focus`) and hidden (`names`), the query points the same —
and the difference is reported.

Consistency is currently filed in section 7 as a risk. It belongs here: a
component that answers differently on identical input is not deployable at any
accuracy.

The rates — recognition at a transition, with its direction, and under a
distractor — are read on the generated layer: the transition grid (the 240
ordered mode pairs in two forms, 480 files) and the distractor grid (272
files), design with no realism claim. An experiment selects them by their grid
axes from a pinned manifest (`files.select`, `pins.generated`).

### RQ2 — Does that reading beat what shipping systems do?

Against three baselines. `fixed` has no situation awareness.
`shipped_catalogue` reproduces the name-keyed catalogue a shipping Linux
distribution enables by default: CachyOS's catalogue (`ananicy-rules` at
`03ef03fb`) as CachyOS installs and enables it with ananicy-cpp, matched by
each process's `argv[0]` basename, untruncated. `strongest_name_table` is a
rule list in the catalogue's design covering the software the dataset
presents as known. Beating the shipped catalogue answers RQ2; beating the
strongest name table is the claim, the one that matters most. Failing to beat
either is a finding.

Split by mechanism. An average across both mechanisms hides which one is doing
the work.

The strongest name table is expected to win on well-known software. Section 7
states this plainly, and it is why Family 3 is primary.

### RQ3 — How much authority does the model need?

The variant ladder. Vocabulary only, versus vocabulary plus algorithm, with
full configuration writing demoted to a subset diagnostic (Q6 of the archived
open-questions record, `_dev/archive/2026-08-23-design-meeting-open-questions.md`).

```text
  A close to B      vocabulary is sufficient. drivers stay thin.
                    new consumers are cheap.

  B beats A         the model should choose the algorithm class and
                    the driver should tune the constants. deployable.

  C beats both      the hand-written table is worse than generated
                    constants. drivers must be thicker than designed.
```

Section 4.6 predicts improvement stops around B. The prediction is not the
result, which is why the subset run exists.

### RQ4 — How long must a situation last to pay for the latency?

The transition-speed sweep. Latency measured with reasoning tokens included,
because reporting a figure measured without them would be dishonest.

The sweep runs on the return grid: A → B → A over the 240 ordered mode pairs,
each task set departing at its boundary, the middle segment 60 s, 10 s or
2 s — 720 files, split by pair into a tuning half and a measurement half of 120 pairs
each — RQ4's phase-shift family, measuring a stale configuration's cost. A
generated file is scored by one rule over the single-situation (C1) entries'
terms, not by an entry of its own. The three authored arcs of the core set's
mode-transition group (C3: `c3-workday`, `c3-evening`, `c3-creation`) are
existence cases with no statistical claim.

Before any hold-time rule is adopted, the `flip_cost` reporting line measures
whether wrong flips cost anything: `change_count`, `wrong_change_count` and
`wrong_switch_excess_sum` per recognizing run (the hold-time plan's no-rule
measurement, its step 1).

Produces a statement of the form: semantic configuration pays off only when a
situation persists at least N times the model's round-trip latency.

### RQ5 — Is the instrument sound?

Every conclusion about RQ2 and RQ3 is measured through the driver table. If the
table is poor, a correct reading is discarded before it reaches the scheduler,
and the result reads as a negative finding about the signal.

```text
  GOOD TABLE                        BAD TABLE
  fixed                42           fixed                42
  strongest name table 19           strongest name table 34
  variant A            20           variant A            34
  perfect recognition  18           perfect recognition  33
  perfect config       14           perfect config       14
  table headroom        4           table headroom       19
```

The right column reads as "semantic recognition does not improve scheduling."
Recognition was perfect in both columns. In the right one the mapping discarded
the benefit.

Three checks, all without a model, all before the matrix:

```text
  1  do different rows of the table yield different configs?
     if the wanted=true and wanted=false rows are identical, the
     attribute is inert and every Family 2 result comes out flat

  2  do those different configs yield different metrics?
     section 7 names this risk: situations may not differ enough
     to matter

  3  is each row near the best achievable for its situation?
     the search engine answers this; the gap is table headroom
```

---

## The load-bearing experiment

The paper does not rest on the matrix. It rests on one pair.

```text
  ML training run + editor      ml-train,  background wanted
  file indexer + editor         indexing,  background not wanted
```

Two real jobs beside an editor, with opposite correct policies. They differ in
behaviour — the training run (`c2-p1a`, PyTorch's basic MNIST example on the
CPU, an actual training run that does not claim desktop users train MNIST) is
one thread, 69.49 s ±27.3 % between voluntary blocks, at nice 0; Tracker's
first index of a home (`c2-p1b`) is five processes, 1.876 ms between voluntary
blocks, 0.844–0.849 of its CPU past a 10 ms slice — and in declared class: the
indexer sets `SCHED_IDLE`, nice 19 and the idle I/O class on itself. The pair
tests what recognition adds over a baseline that already honours the
indexer's declared class.

On the indexer's side that headroom is zero: the executor's strict idle rule
places the idle-class indexer below every driver-table row. So RQ0 judges
`c2-p1a` and reports `c2-p1b`, the indexer's declared class settling its own
side. P1, the training-run-against-indexer pair, stays the load-bearing pair:
it carries the recognition claim — telling the wanted training run from the
unwanted indexer — and the scheduling headroom on `c2-p1a`'s side.

If the model separates that pair and the strongest name table does not, the
claim is demonstrated by construction and the remaining workloads are
generalisation. If it does not, no amount of matrix recovers it.

The P2 pair — the game download the user started (`c2-p2a`) against Ubuntu
24.04's stock unattended upgrade (`c2-p2b`) — is the same argument on a
workload with a hard deadline, which makes the consequence measurable as frame
latency rather than as response time. They are two real jobs beside a game,
each keeping a CPU 91–99 % busy, that differ in run shape (163 µs against
1.8 ms between voluntary blocks), structure (one process of 83–84 threads
against 916 processes), size (about 700 s of CPU against 26 s) and declared
priority (three quarters of the download's CPU at nice 10; 2.7 % of the
upgrade's at nice 19). The wanted download is throttled by the batch class's
cap, its waits judged by the 30 s starvation guard, no floor guaranteed; the
unwanted upgrade is deferred.

---

## What is not claimed

```text
  not  a language model should make scheduling decisions
       section 4.1 forbids it. an answer takes four to eight orders
       of magnitude longer than a scheduling decision across the
       settings measured, six to seven on a consumer laptop.

  not  this beats the strongest name table on well-known software
       section 7 expects it to lose there. the advantage exists on
       software the list does not cover.

  not  this improves real kernel performance
       it is a simulator. no cache effects, no multi-core
       interaction, no kernel overhead.

  not  the scheduling result transfers to another CPU or another
       machine's configuration
       every CPU value is one AMD EPYC 7763 core's, on a hosted
       runner: Xvfb, no GPU, no sound device, no human.
       another CPU model changes each program's speed by its own
       factor (a Xeon Platinum 8573C ran cc1 at 0.72x and fixdep at
       0.50x the EPYC's time), which no common scale reproduces;
       the venue variants test a common factor of 0.8-1.25 only.
       recognition reads no CPU value.

  not  the vocabulary generalises across consumers
       one driver is built. the extensibility argument is a design
       argument, not a result.

  not  name-based reading is robust
       three of the four resolution limits (C6) ship as
       pre-committed misses: a CPU job named chrome (c6-spoof, a
       miss from its arrival at 20 s), a call running under the
       browser's own name (c6-fold, a miss from its arrival at
       30 s) and two media players under the indexers' names
       baloo_file and tracker-miner-f (c6-alias, a miss over the
       whole file).
```

---

## The outcome the project pre-commits to

High recognition accuracy with flat scheduling performance is a result, not a
failure.

> The model reads system situations accurately. That reading does not improve
> CPU scheduling, because existing behavioural heuristics were already
> sufficient for this consumer.

It tells the architecture something it needs to know, it is specific to this
consumer rather than to the recognition layer, and the two-layer measurement
design is what makes it interpretable instead of ambiguous.
