# Research Claims and Questions

What this project asserts, what would falsify it, and what it does not claim.

RQ0 through RQ5 are section 3 of `RESEARCH_PROPOSAL_v2.md`, restated with the
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

> On workloads where behaviour is identical and the correct policy differs, a
> language model reading process names recovers the difference, and a name
> whitelist cannot.

The second is what the results section defends. The first is what it implies.

---

## The chain

The claim is not one proposition. It is six links, each failing independently.

```text
  C1  there exist realistic situations where the correct config
      differs, and the difference is measurable
                                                  no model involved
  C2  some of those differences are invisible to behavioural
      observation
                                                  no model involved
  C3  they are present in names and command lines
                                                  no model involved
  ------------------------------------------------------------------
  C4  a language model can read them                        RQ1
  C5  reading them beats what shipping systems do           RQ2
  C6  stably and quickly enough to be a system component    RQ4
  ------------------------------------------------------------------
  C7  the signal generalises to other consumers    RQ3, argued only
```

C1 through C3 are properties of the workload space rather than of language
models. They are what Phase 1 tests, with `random` against perfect recognition,
before any prompt exists. If C1 fails, no model recovers the paper. This is why
section 5.3 is a gate rather than a milestone.

C7 is argued in section 4.4.4 and demonstrated nowhere, because the project
builds one driver. Section 7 already states this as the proposal's most
significant weakness.

---

## Two mechanisms, currently measured as one

Sections 2.3 and 2.4 argue two different reasons the whitelist fails. The
research questions treat them as one.

```text
  MECHANISM 1 -- combination
  Discord means something different depending on what runs beside it.
  A flat list cannot express context.
        tested by Family 2, same process set, different intent

  MECHANISM 2 -- world knowledge
  A Godot-built indie game is a game that nobody registered.
  A finite list cannot cover software it never enumerated.
        tested by Family 3, unregistered software
```

They are separable results with different consequences.

```text
  only M1 holds   extend Game Mode to read combinations.
                  a feature request, not an architecture.

  only M2 holds   the list is the problem, but a longer list or
                  application self-declaration is a cheaper fix
                  than inference.

  both hold       neither cheap fix is available. this is the
                  argument for a recognition layer.
```

Section 5.5 already requires results split by software familiarity, which
separates M2. Nothing currently separates M1. **Proposed:** report the
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

### RQ1 — Can a model read the situation from names and command lines?

Layer 1: the proposal's system block against ground-truth labels, with no
simulator involved, so scheduling heuristics cannot contaminate the result.

Reported as mode accuracy, per-attribute accuracy separately, a confusion
matrix, and **run-to-run consistency on identical input**. Split by the two
mechanisms above.

Consistency is currently filed in section 7 as a risk. It belongs here: a
component that answers differently on identical input is not deployable at any
accuracy.

### RQ2 — Does that reading beat what shipping systems do?

Against two baselines: `fixed`, which has no situation awareness, and
`whitelist`, which reproduces Game Mode. The second is the claim.

Split by mechanism. An average across both mechanisms hides which one is doing
the work.

The whitelist is expected to win on well-known software. Section 7 states this
plainly, and it is why Family 3 is primary.

### RQ3 — How much authority does the model need?

The variant ladder. Vocabulary only, versus vocabulary plus algorithm, with
full configuration writing demoted to a subset diagnostic (Q6 of
`OPEN_QUESTIONS.md`).

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

Produces a statement of the form: semantic configuration pays off only when a
situation persists at least N times the model's round-trip latency.

### RQ5 — Is the instrument sound?

Every conclusion about RQ2 and RQ3 is measured through the driver table. If the
table is poor, a correct reading is discarded before it reaches the scheduler,
and the result reads as a negative finding about the signal.

```text
  GOOD TABLE                        BAD TABLE
  fixed                42           fixed                42
  whitelist            19           whitelist            34
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
  ML training run + editor      compile,     background wanted
  file indexer + editor         interactive, background not wanted
```

Both are one sustained CPU-bound process beside an editor. No behavioural
heuristic separates them, even in principle. The difference exists only in the
names.

If the model separates that pair and the whitelist does not, the claim is
demonstrated by construction and the remaining workloads are generalisation. If
it does not, no amount of matrix recovers it.

The Family 2 gaming pair — download versus antivirus scan — is the same
argument on a workload with a hard deadline, which makes the consequence
measurable as frame latency rather than as response time.

---

## What is not claimed

```text
  not  a language model should make scheduling decisions
       section 4.1 forbids it. inference is five to six orders of
       magnitude slower than a scheduling decision.

  not  this beats a whitelist on well-known software
       section 7 expects it to lose there. the advantage exists on
       software the list does not cover.

  not  this improves real kernel performance
       it is a simulator. no cache effects, no multi-core
       interaction, no kernel overhead.

  not  the vocabulary generalises across consumers
       one driver is built. the extensibility argument is a design
       argument, not a result.

  not  name-based reading is robust
       Family 5 tests a renamed miner and expects to fail.
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
