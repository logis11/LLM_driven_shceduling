# Escalating to a deployment claim — what it would take

> Status: **personal working notes, not ratified** · Created 2026-09-06 · Revised 2026-09-06
> Author: 인지오. Nothing here has been through team sign-off.
> Items marked **[proposal]** are suggestions from a review session, not
> decisions. Items marked **[verified]** are quotations from or direct readings
> of committed documents.

---

## 1. The question this answers

The coreset is a **discriminative construction**, not a sample (archive Q8).
That makes it sound for existence arguments and limit arguments, and unsound
for frequency arguments and generalisation. The boundary is currently where it
should be.

This note asks a separate question: *if we wanted the paper to support "this
architecture is worth deploying on a real desktop," what would have to change?*

It is written so the answer can be rejected as a whole. Escalating badly is
worse than not escalating: one unsupported claim discounts every supported one
in the same paper.

---

## 2. The claim is three claims

"Worth deploying on a real desktop" is not one proposition. It decomposes into
three, each of which can fail independently, and each of which needs different
evidence.

| Sub-claim | What it asserts | Current status |
|---|---|---|
| **Frequency** | Situations where recognition matters occur often enough on real machines to justify the mechanism | Not addressed at all |
| **Transfer** | The measured benefit survives real hardware and a real kernel | **Actively threatened by a design decision** (§3) |
| **Cost** | The benefit exceeds the cost of obtaining it | RQ4 covers latency only; resource occupancy unexamined |

Nothing in the current plan targets any of the three. That is not an oversight
— the plan was scoped to existence — but it means "deployment value" is not one
increment away from where we are.

---

## 3. Transfer — the most urgent, because it is self-inflicted

### The problem — **[verified]**

Archive D15 records single lane as ratified, and among the reasons given for
Q1's original single-core choice:

> more cores shrink the random-vs-oracle gap

This is an honest record and correctly placed. It is also, read by a reviewer,
a statement that the experimental configuration was chosen partly because it
maximises the effect being measured. Real desktops have 8–16 cores; the paper
measures on one; and the archive shows the authors knew the gap shrinks with
core count. If the archive ships with the artifact — and it should — a reviewer
will find this.

No amount of careful phrasing repairs that. It has to be measured.

### The proposal — **[proposal]**

Do **not** move the matrix to multi-lane. D15's blast-radius judgement stands:
overturning Q1 pulls in EDF optimality under Dhall's effect, executor fill-K
semantics, a tuning-pool redo, and trace/metric changes. That is a different
project.

Instead, run a bounded sensitivity sweep:

> **C2's six files × `random` and `oracle` only, at lane counts 1, 2, 4, 8,
> with demand scaled with lane count so that per-lane demand stays constant.
> Report the gap as a function of lane count.**

No other conditions, no other families, no tuning, no LLM.

**Why demand must scale with lanes — [revised 09-06].** The first draft of this
sweep ran the fixed-demand workloads at more lanes. That is wrong as written:
scaling touched only the gaming files, so most workloads were authored at
1-lane scale, and running a 1.29-utilisation file at 4 lanes turns it into 0.32.
The gap would vanish — not because parallelism dilutes recognition value, but
because contention was removed outright. That is a tautology, not evidence.

Corrected form:

```
1 lane  → total demand 1.2
2 lanes → total demand 2.4
4 lanes → total demand 4.8
8 lanes → total demand 9.6
```

This asks the question actually at issue: holding contention intensity fixed,
does parallelism itself dilute the gap? That is what archive D15's recorded
"more cores shrink the random-vs-oracle gap" claims, and the only version worth
answering.

**Why C2 specifically makes this tractable.** The Dhall's-effect objection
attaches to EDF, and C2 is not an EDF-dominated group: P1 is `dev`/`ml-train`
vs `dev`/`indexing`, P3 is `video-edit`/`render` vs `video-edit`/`backup`.
Restricting the sweep to the MLFQ and LOTTERY rows those files exercise sidesteps
the multiprocessor-EDF question entirely. **[proposal, needs checking against
the v0 table's actual rows for C2 — if P2 (gaming) resolves to EDF, exclude P2
from the sweep or accept the caveat explicitly.]**

**Cost — [verified 09-06, partly].** The compiler's lane-scaling path exists and
is what produces `coreset-single`, but it scales only declared-scalable fields,
and the only archetype declaring any is `game-task-chain` (every other entry in
`archetypes.yaml` carries `scalable: []`; RUN durations are intrinsic and never
edited by design). So:

- **P2** (game + background): the existing path applies at other multipliers —
  reuse, not new work.
- **P1, P3**: nothing the compiler can scale. Holding per-lane demand constant
  needs a mechanism that does not exist yet — replicating the batch and
  interactive tasks per lane at compile time, or authoring K-lane timeline
  variants. **[open — which route is a dataset decision, not decided here.]**

Plus parameterising the executor's lane count, and the sweep itself: 1.5× the
C2 gate runs at three additional lane settings. Raise with 인경민 as part of the
Phase-2 scope conversation, not added afterwards.

**One open risk.** Files binding `lane_share` compress many-core-measured
archetypes (D15: LAVD gaming, ~300 tasks) down to one lane. Re-expanding them
to 8 is a round trip through a lossy transform. This applies to P2 inside the
sweep, and to `c1-gaming` if its separate reporting line is ever swept. Either
exclude those files from the sweep or use `-native` as their reference point.

### Why this is worth doing either way

- **If the gap survives at 4–8 lanes**, it is the single most valuable result
  this project can produce. It converts the single-lane decision from a
  convenience into an informed scoping choice, and it is the load-bearing
  evidence for any deployment claim.
- **If the gap vanishes**, we need to know before submission, not after. The
  claim reverts to existence, and the attenuation curve itself is an honest
  contribution: *semantic recognition's benefit decays with core count in this
  way*. That is publishable and it is true.

**This is a no-lose experiment**, and it is the only item in this note that is
worth doing regardless of whether the deployment claim is attempted at all.

---

## 4. Frequency — currently empty, cheapest to fill

Going from "such situations exist" to "such situations are common" cannot be
done with a constructed suite, in principle. It requires observation.

### The instrument already exists — **[verified]**

`building-plan` §7 commits to shipping the collection + privacy-scrub tool in
the artifact as an **open falsification invitation**: any user can run it
against their own machine and check our synthetic distributions.

**The proposal is to run it ourselves before shipping it.** — **[proposal]**

### Minimum viable version

- Three team machines plus whatever else is available; a few days of process-set
  snapshots.
- Extract three numbers only:
  - **(a) canonical-set change rate** — how many novel sets per hour.
    **RQ4's payoff statement is empty without this**: "semantic configuration
    pays off when a situation persists at least N times the round-trip latency"
    is unfalsifiable if we do not know how long situations persist in the wild.
  - **(b)** what fraction of observed sets carry a mode plus sustained
    background work at all;
  - **(c)** of those, what fraction are cases where `background_wanted` is
    **not** determinable from behaviour alone.

**(c) is the real-world frequency estimate for the C2 structure.** It is the
number the entire architecture argument implicitly assumes and currently never
states.

### Two conditions that make it worth anything

1. **Labelling must be done by someone who did not design the coreset.** If the
   coreset's author labels the snapshots, §4.5's author-overlap threat is
   reproduced exactly, and the measurement demonstrates nothing.
2. **State the sample honestly.** Three developer machines is a convenience
   sample and generalises to nothing. That is fine. **Going from zero machines
   to three is a larger epistemic step than going from three to thirty** — the
   claim moves from *unmeasured* to *weakly estimated*, which is a change of
   kind, not degree.

Half a day to a day. Best defensive return per unit cost on this list.

---

## 5. Cost — an unexamined self-contradiction

**The model runs on the machine it is optimising.** If a local model holds
2 GB of VRAM and periodically occupies CPU or GPU in order to "improve gaming
performance," the mechanism may be net negative and the paper would not know.

RQ4 measures **latency** — round-trip time with reasoning tokens included,
which is the right call. It does not measure **occupancy**. The reviewer's
question writes itself: *how do you know the scheduling benefit exceeds what
the model consumes?*

### What is needed — **[proposal]**

Not an energy study. A one-page accounting:

- model resident memory;
- compute per query;
- **query frequency** — this is §4's number (a), reused;
- placed in the same units as the measured scheduling benefit.

### Why this may strengthen rather than weaken the design

The slow-loop / fast-loop separation and the deployment cache exist precisely to
make the claim *"the model is not called often."* Right now that is an assertion
in the architecture section. With query-economics numbers it becomes a
measurement: *at N queries per hour, resident cost is negligible relative to the
measured benefit.*

The proposal already plans to collect query-economics counters from the
naturalistic set (`building-plan` §4). The gap is that they are not currently
joined to a resource-cost figure, and the naturalistic set's rate is generated
rather than observed — §4's collection would ground it.

---

## 6. The metrics are proxies

"Deployment value" is ultimately about perception. P95 stimulus latency is a
stand-in for it.

**Cheap strengthening — [proposal]:** report the **fraction of stimuli crossing
a perceptual threshold**, not raw percentiles. Frame deadlines already work this
way (16 ms, literature-grounded); applying the same treatment to interaction
latency costs nothing at metric-definition time and is a materially stronger
sentence. *"8% of stimuli exceeded the perceptual threshold"* travels further
than *"P95 was 47 ms"*, and it makes cross-file comparison meaningful.

This also relieves a known open item: `c1-media`'s audio/video weighting
(rq0-preparation-notes §6) is currently headed for "record it as a stated
assumption." Anchoring to perceptual literature converts a stated assumption
into a grounded choice.

Fold into Stage 1 (metric definitions) rather than treating it as extra work.

---

## 7. Kernel implementation — honestly, a second paper

A `sched_ext` implementation, real workloads, real users. This does not fit the
current timeline, and forcing it in would hollow out everything else. It is
already in the proposal's future work and belongs there.

One observation: **writing future work concretely makes the present scope more
defensible.** "A kernel implementation remains" is weaker than "measured on a
single-lane DES; attenuation with core count reported in §X; `sched_ext` port is
the next step." The second tells a reviewer the authors know exactly where the
boundary is.

---

## 8. Recommended priority

Attempting all of it produces a thin version of each. Ordered by defensive
return:

| # | Item | Cost | What it buys |
|---|---|---|---|
| 1 | **C2 lane sweep (1/2/4/8), per-lane demand held constant** | Executor lane parameterisation + demand scaling for P1/P3 (mechanism open) + small sweep | The only item touching **transfer**. Wins either way (§3) |
| 2 | **Run the collection tool ourselves** | Half a day to a day | Moves **frequency** from unmeasured to weakly estimated |
| 3 | **Query economics + resource accounting** | Reuses §4's numbers | Closes the self-contradiction; converts the slow-loop argument into a measurement |
| 4 | **Perceptual-threshold reporting** | Absorbed into Stage 1 | Reduces proxy distance and one Layer-2 assumption |

With all four, the supportable claim becomes:

> *Situations exist where semantic recognition improves scheduling; such
> situations occur roughly N times per hour on observed machines; the benefit
> persists up to K lanes; and the recognition cost is X% of the benefit.*

That is **not** "this architecture is worth deploying." It is *"we have
identified the conditions under which this architecture would be worth
deploying."*

**The second is stronger under review than the first**, because a
simulation-based study cannot honestly reach the first, and a reviewer can see
when a claim outruns its evidence. The conditional version is exactly supported
by what we would then have.

---

## 9. The case for not escalating

This should be weighed seriously rather than treated as the fallback.

The existing claim — existence plus limits — is a publishable contribution on
its own, and some of its properties are rare: pre-registered failure cases (C6),
CI-enforced minimal pairs, a generated coverage grid that cannot drift from the
files it describes. Those are strengths a reviewer will notice.

**Escalating badly is worse than not escalating.** A single unsupported claim
discounts every supported claim beside it. If items 1–4 cannot all be done
properly, the correct move is to keep the existence framing, state the scope
boundary explicitly in the methodology section, and carry Q8's rejection of the
two naive generators over into the paper nearly verbatim — it is a better
defence of the design than anything written after the fact.

**One exception.** Item 1, the lane sweep, should happen either way. Independent
of any deployment claim, it is what shows the single-lane choice was informed
rather than convenient — and the archive already contains the sentence that
makes the question unavoidable.

---

## 10. To raise with the team

1. **Lane sweep scope** — with 인경민, folded into the Phase-2 scope conversation
   (rq0-preparation-notes §11 item 5), since it is a lane parameterisation on top
   of work he is already being asked to do. Verify the C2 rows' algorithms first
   (§3).
2. **Whether to escalate at all** — a framing decision affecting what the paper
   claims, so all three, not a unilateral call.
3. **Collection-tool run and independent labelling** — needs someone other than
   the coreset author to label; that is a person-assignment question.
4. **Perceptual-threshold reporting** — belongs to the metric-definitions freeze
   (§8.2 decision 4), so it should enter that discussion rather than run beside
   it.
