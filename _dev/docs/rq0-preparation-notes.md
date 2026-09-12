# Preparing the RQ0 Gate — working notes

> Status: **personal working notes, not ratified** · Created 2026-08-30 · Revised 2026-09-06
> Author's scope: 인지오's work items toward the RQ0 gate.
> Nothing here has been through team sign-off. Items marked **[proposal]** are
> suggestions, not decisions. Items marked **[unverified]** rest on assumptions
> that have not been checked against the repo. Items marked **[new 09-06]** were
> surfaced in the second review session and are not in the original notes.

**Revision summary (2026-09-06).** Two findings changed the plan rather than
adding to it:

1. **The driver table's shape is not settled, and the proposal's account of it
   is wrong** (§4.7). Previously assumed resolved. It blocks Stage 3, it is
   §8.2 decision 3, and it cannot be deferred past the gate — a new **Stage
   0.5** now sits ahead of table authorship.
2. **Two ratified documents carry stale lines that contradict the current RQ0
   design** (§4.8). Folded into Stage 0 as item 0.4.

---

## 1. What this document is

A record of design conversations about what has to happen before the RQ0 gate
can be run, organized as an ordered work plan. It does three things:

- restates where the project stands, so the plan has a starting point;
- collects the open questions those conversations surfaced, separating what is
  established in the repo from what is inference;
- lays out an ordered sequence of work items for the contracts/infrastructure
  owner.

It deliberately does **not** re-decide anything already ratified. Where it
touches a ratified decision, it says so and points at the normative document.
Where it finds a ratified document to be *wrong*, it says that too, and names
the line (§4.7, §4.8).

---

## 2. Where the project stands

Established, from the repo:

- The research framing, vocabulary (16 modes + `background_wanted`),
  `cpu_scheduler` config schema, trace format, canonical workload schema, and
  interpretation contract are all frozen.
- The workload dataset is complete: `coreset-single` / `coreset-native`,
  13 novel + 11 derived timelines, all inside the demand window, coverage grid
  signed off. The meas-ci campaign folded 11 of 15 pending parameters; 4 remain
  pending with stated findings.
- Onboarding docs exist for both builders (`background-guide`,
  `simulator-guide`, `daemon-guide`, `data-contracts`, `recognition-vocabulary`).
- **No simulator, daemon, or harness code exists yet.** Contracts and data are
  in place; execution is at zero.

Remaining in the backlog before RQ0: **the driver table's format decision**, the
driver table v0 itself, the RQ0 gate, the experiment harness.

---

## 3. What RQ0 actually requires

RQ0 is one question — "is the random-to-oracle gap large enough to measure?" —
but answering it requires the whole offline pipeline to run end to end:

```
coreset-single  [done]
   ├─ visible projection ─→ daemon: recognizer (fixed/random/oracle)
   │                                 → validator → driver table v0
   │                                 → config schedule + recognition log
   └─ run file ──────────────────→ simulator: (run file, schedule) → trace
                                                      │
                                        harness: trace → metrics → gap statistic
```

Three consequences worth stating plainly:

**The simulator needs more than its first integration gate.** The gate as
specified in `simulator-guide` §7 is one C1 workload under a one-entry MLFQ
schedule. RQ0 additionally needs the other three algorithms (EDF, Lottery,
FIFO), the batch class with bandwidth caps and the starvation floor, EDF's
period-implicit deadlines, and mid-run config switching — because the driver
table names those algorithms. Running RQ0 with an MLFQ-only executor would mean
restricting the table to MLFQ parameter variation, which shrinks the gap
artificially and biases the gate toward failure.

**Three of the four remaining contract drafts are effectively settled.** The
config schedule, telemetry/visible projection, and recognition log are marked
`draft` in `data-contracts.md`, but each is fully exampled and the builder
guides instruct building to them as law. The remaining work there is the
protocol-freeze signature, not design.

**The driver table's format is a fourth contract, and it is genuinely open**
— **[new 09-06]**. It was not on the original list because the proposal reads as
if it were settled. It is not; see §4.7.

The genuinely open decisions are therefore: **the driver table's format**
(§8.2 decision 3), **metric definitions** (§8.2 decision 4, with two items
explicitly deferred to it), and the **simulator semantics questions** in
`simulator-guide` §9.

---

## 4. Open questions

### 4.1 C1's demand class — **[closed 09-06]**

`task-2.4` spec §3 fixes C1 as demand class `calibration` and C2–C6 as
`oversubscribed` (hard-checked 100–150%). The TODO's RQ0 entry scopes the gate
to "coreset-single C1/C2".

The inference drawn earlier — that `calibration` implies low contention, and
therefore that C1 may show little random-vs-oracle separation by design —
**has not been checked.** The compiler emits a per-file static demand estimate;
reading it settles the question directly. `c1-gaming` in particular carries a
`lane_share: 0.9` game task chain plus a 40%-duty compositor, so it may be
tighter than the class name suggests.

This matters because it determines whether the gate's judging set is 6 files or
12.

**Closed 2026-09-06 (task 3.1).** Read from the compiled estimates, now recorded
per file in `dataset/build.manifest.json` under `demand`: five C1 files sit at
0.00–0.54 of the lane, `c1-gaming` at 1.46. Judging set = the six C2 files, all
inside the demand window; C1 stays reporting-only.

**Re-decided 2026-09-10 (Phase 7, 7.7).** C1 is sixteen files (the ten new
bases sit at 0.45–0.97) and C7 adds one counterpart per mode (interactive ones
at 1.45–1.53, `c7-gaming` 2.46, batch ones equal to their bases), every derived
file `calibration` by authored declaration. The judging set is no longer the
six C2 files: a file judges when it is one side of a label-varying pair and its
scored term registers the rows' difference by design — demand is not a
criterion (Q8's per-file headroom admission test is the gate's own per-file
criterion, §8). Twenty-seven files: C2, the six batch C1 bases, the fifteen C7
counterparts with a term. The ten interactive and periodic C1 bases stay
reporting-only, and the building plan's "whitelist scores perfectly here" line
covers all sixteen. Pair review findings 4–5
(`docs/daemon/prior-table-pair-review.md`) are notes on judging members, not
exclusions. Full lists and reasons in §8.

The inference above does not hold as stated. Demand bounds *throughput*
headroom, not *latency* headroom: at 0.8 utilisation two tasks still become
runnable at the same instant, and a keystroke arriving while a batch task holds
the lane still waits a slice. C1 is excluded from judging because its designed
role is the baseline where the whitelist scores perfectly — not because it has
no headroom. Nonzero C1 gap numbers are expected, not a contradiction.

### 4.2 The gate is asymmetric — **[proposal]**

C2 is three pairs, each a one-task diff between otherwise byte-identical files
(enforced by `dataset/tools/tests/test_coreset.py`). That structure makes it a
strong *existence* argument: it shows that situations exist where behaviour is
indistinguishable and correct policy is opposite, and that recognition helps
there. Three pairs is sufficient for that claim, and adding a fourth would not
strengthen it.

It is **not** a representative sample, and was never designed to be. So:

- **Passing** the gate on C2 is a valid result. The premise survives.
- **Failing** the gate on C2 does not license the conclusion "there is nothing
  to measure here." Three non-independent pairs cannot support that.

The proposal is to declare the gate one-directional: pass = premise verified,
proceed; fail = **diagnostic trigger**, not rejection.

### 4.3 Failure has three causes, and the current plan conflates them — **[proposal]**

If the gap does not appear, the cause is one of:

1. the workloads genuinely have no headroom — what RQ0 is meant to detect;
2. the executor's heuristics self-correct misclassification — anticipated in
   proposal §5.3;
3. **v0 is simply a badly written table** — unrelated to the premise.

The proposal's stated failure response (redesign workloads, or deliberately
weaken the executor's self-correction) addresses only 1 and 2. If cause 3 is
operative and that response is applied, a sound dataset gets torn up and a
correct executor gets damaged.

Cause 3 is not remote. C2 pairs differ only in `background_wanted`, so the gap
there rests almost entirely on how far apart the two rows' configurations sit —
principally `batch_bandwidth_cap`. If the table's author writes 0.15 against
0.10 without thinking about it, the gap is small for reasons that have nothing
to do with the hypothesis.

**Proposed failure procedure:** before touching workloads, run a config
brute-force search on two or three failing files — ignore labels, sweep the
configuration space, observe the spread.

- Search finds no spread → cause 1 or 2. Proceed to workload redesign.
- Search finds spread that v0 failed to capture → cause 3. Rewrite the table.

This is the "perfect configuration" instrument (archive Q5, RQ5's third check).
It already exists in the plan; the proposal is only to move it earlier, from
just-before-the-full-matrix to just-after-a-failed-gate. It is read-only and
never folded into the table, so it introduces no tuning contamination.

### 4.4 Row distinctness must be checked before the gate, not after — **[proposal]**

The subset of rows C1/C2 actually exercise should be verified to produce
distinguishable configurations before the gate runs. Without that check, a
failed gate is uninterpretable. This is RQ5's first check; the parts that make
failure diagnosable belong before RQ0, not after.

### 4.5 Author overlap — **[observation]**

The driver table and the workloads share an owner. v0 is written from theory
with no measurement, so this is not test-set contamination in the usual sense,
but the person writing the table knows what is in the coreset. For RQ0
(headroom detection) this is minor. For RQ2 it matters, and the existing design
already handles it by tuning v1 on the separate driver table tuning set. If any v0-based
number reaches the paper, the overlap should be stated.

### 4.6 `c6-dual` uses vocabulary outside the ratified set — **[unverified]**

`c6-dual.timeline.yaml` carries `mode: ambiguous` and
`attributes: {dual_active: true}`. `ambiguous` is a ground-truth-only label by
design (`recognition-vocabulary` §1) and `dual_active` is a ground-truth
annotation, so neither is on the recognizer's menu. What the *oracle* does when
it reads a segment it cannot legally propose is undefined. Outside RQ0's scope;
noted so it is not lost.

### 4.7 The driver table's format is unsettled, and the proposal is wrong about it — **[new 09-06, blocking]**

**This is the finding that reorders the plan.**

#### The mechanical problem

Variant B (`llm_algo`) is specified as: the LLM fills `system` **plus the
`algorithm` field**; `params` and `batch_bandwidth_cap` come from the driver
table (`recognition-vocabulary` §3, `research-proposal` §5.2).

But `params` field sets are algorithm-specific:

| algorithm | `params` fields |
|---|---|
| MLFQ | `num_queues`, `timeslice_us`, `timeslice_growth`, `boost_interval_us` |
| EDF | `residual_timeslice_us` |
| LOTTERY | `batch_share`, … |
| FIFO | … |

And validation rule 2 (`recognition-vocabulary` §2) states that `params` must
contain **exactly** the declared fields for the chosen algorithm — missing,
extra, or wrongly typed fields reject the config (`held`).

So if the table row for `(gaming, wanted=false)` holds EDF with EDF's params,
and the model proposes LOTTERY, the table has no legal `params` to supply.
**Under the current specification, a variant-B proposal that changes the
algorithm is structurally always rejected.** Variant B does not work as written.

#### Two candidate fixes, both rejected or unclear

**Extending the key to `(mode, background_wanted, algorithm)` — rejected.**
It breaks the invariant below. A recognizer that emits only the `system` block
(`random`, `whitelist`, `llm_vocab`, `oracle`) would face several algorithm rows
per situation with no basis for choosing among them. That is not merely
inconvenient: it breaks §5.1, because a table read differently by different
conditions destroys the attribution of performance differences to recognition
quality.

**A per-algorithm default-params function — unclear.** The idea is that a row
carries an algorithm-independent "disposition" and the concrete field values are
derived per algorithm. But *disposition* is undefined. Without a stated set of
axes it is a rename of the problem, not a solution.

#### The invariant any fix must preserve

> Every condition that emits only the `system` block — `random`, `whitelist`,
> `llm_vocab`, `oracle` — receives **exactly the same configuration** for the
> same `(mode, background_wanted)`.

This is what makes §5.1's "byte-identical executor across conditions" true at
the table as well as in the simulator. **It is the acceptance criterion for any
candidate design.**

#### A second-order consequence: archive Q5's ceiling claim

Archive Q5 argues that variants A and B both pass through the shared driver
table, so *perfect recognition is their exact upper bound and they cannot exceed
it.* If B can choose the algorithm directly, it can pick a better algorithm than
the table's default for that situation and **land above the oracle**. That
would:

- break the headroom decomposition (`total = recognition + table`) for B, and
- reopen what the correct denominator for scoring B is.

This may need settling *before* the format question, since the answer changes
whether B should pass through the table at all.

#### Documentation to correct

- `research-proposal` §5.2, the `llm_algo` row: "params from table" — does not
  hold, per above.
- `research-proposal` §4.6, the corresponding narrative.
- Whatever in `daemon-guide` §5 implies the config-mapper stage is a
  straightforward wiring job once the table lands.

#### Why this cannot be deferred past the gate

The earlier instinct was to defer it, on the grounds that RQ0 uses only
`fixed`/`random`/`oracle`, all of which pass a complete `(mode,
background_wanted)` key through the table. That reasoning is wrong, for three
reasons:

1. **v0 and v1 must be instances of the same schema.** Archive Q5's plan keeps
   v0 rather than discarding it — running the ladder on both tables costs one
   extra sweep and answers most of RQ5 directly ("if v0 and v1 score alike, the
   table is not a fragile artifact"). That comparison is meaningless if the two
   are not the same kind of object.
2. **The gate is re-run on v1**, and that is the figure that goes in the paper.
   A format change between the two runs makes them incomparable.
3. **Stage 5 is pre-registration.** Fixing a pass threshold while the shape of
   the measuring instrument is undecided is not pre-registration.

It is §8.2 decision 3 and needs three signatures, which is a further argument
for starting it early rather than late.

### 4.8 Stale lines in ratified documents contradict the current design — **[new 09-06, verified]**

Two concrete instances, both found by reading rather than inferred:

- **`research-proposal` Part 9, milestone table, Phase 1** reads
  `fixed`, `random`, `oracle` — **"modes only, no attributes."** The current RQ0
  design requires `background_wanted` (Stage 3.1): C2 pairs differ *only* in
  that attribute, so dropping it makes the entire judging set inexpressible.
  The milestone table is stale relative to the plan.
- **`terminology.md`** still carries the **old five-mode vocabulary**
  (`interactive`, `gaming`, `compile`, `media`, `idle`) and the attribute
  **`has_realtime_encoder`**. The ratified vocabulary is 16 modes plus
  `background_wanted` alone.

These are not cosmetic. §8.3's named failure mode is three people building
against three slightly different assumptions about one interface; a stale line
in a normative document is exactly how that happens. Fix them alongside the
protocol-freeze signature (Stage 0.4).

Worth a broader sweep at the same time: several items were carried as "draft"
long after they were settled, and at least two documents lag the vocabulary
freeze. Auditing status labels periodically is cheap; discovering a divergence
at integration time is not.

---

## 5. Metric definitions split into two layers

The main structural conclusion. "Deciding what to measure" is two separate
pieces of work, and separating them is what makes re-scoring cheap.

### Layer 1 — primitive metric definitions (project-wide, lives in code)

How each raw number is computed. Global: `editor` stimulus latency must mean
the same thing in `c1-office` and `c2-p1a`.

The trace→metric mapping in `data-contracts` §9 already fixes the event
arithmetic. What remains:

- **Aggregation statistic** for stimulus latency — P95, P99, both, plus mean?
- **Wakes outside the focus window** — `c1-office`'s `browser` never receives
  focus. Are its stimuli counted? (Suggestion: count, but report separately.)
- **Multi-task rollup** — when a file has several interactive tasks, how are
  they combined, or are they kept separate?
- **Periodic job completion** — explicitly deferred to this freeze. A working
  definition is already written in `data-contracts` §9; the decision is whether
  to adopt it.
- **Starvation measured from `ready`** — effectively settled; needs writing down.
- **Deadline slack summarisation** — miss rate only, or miss rate plus P99 slack?
- **Normalisation formula** — `(fixed − condition) / (fixed − oracle)`, proposed
  in archive Q6. Global rule, applied at scoring time. Needs a **denominator
  floor**: files with near-zero headroom make the ratio explode.

Changing Layer 1 invalidates previously computed results and requires
recomputation from traces.

### Layer 2 — per-file weighting (lives in a committed data file)

Which primitives matter in which file, and in which direction. This is a
research judgement, not an implementation detail: it should be reviewable,
versioned, and possibly reported in the paper. It must not be buried in code.

Changing Layer 2 requires only re-scoring existing records.

---

## 6. Per-file metric inventory (coreset)

Derived from the timeline files' `focus` tracks and archetype bindings. The
`focus` track is effectively authoritative for "where the user's attention is."

| File | focus | Candidate primary metric |
|---|---|---|
| `c1-office` | `soffice.bin` | writer stimulus latency (P95/P99) |
| `c1-browsing` | `chrome` | browser stimulus latency |
| `c1-compile` | `code` | **two-sided** — editor latency + build makespan |
| `c1-gaming` | none | frame deadline miss rate + P99 frame latency |
| `c1-media` | none | deadline miss rate for `mpv` (60 Hz) and `spotify` (20 Hz) |
| `c1-idle` | none | **no performance metric** — see below |
| `c2-p1a/b` | `code` | editor latency + batch task turnaround |
| `c2-p2a/b` | none | frame deadline + background progress |
| `c2-p3a/b` | (kdenlive) | editor latency + bulk turnaround |

### Three places where a real decision is required

**C2 cannot be scored per-file.** `c2-p1a` and `c2-p1b` are behaviourally
identical — both bind `desktop-interactive` + `cpu-batch`, differing only in the
name (`python3` vs `tracker-miner-fs-3`). The raw numbers come out the same. The
difference lives entirely in how those numbers should be valued:

- `p1a` (training, wanted): editor latency low **and** batch progress high
- `p1b` (indexing, unwanted): editor latency low; batch progress should carry
  **zero weight**

So the scoring spec must be a **weight vector over shared primitives**, differing
across the pair — **[proposal]**:

```yaml
c2-p1a:
  editor.stimulus_p95: {weight: 1.0, direction: lower}
  trainer.turnaround:  {weight: 0.4, direction: lower}
c2-p1b:
  editor.stimulus_p95: {weight: 1.0, direction: lower}
  # crawler progress deliberately absent
```

Nothing in the current docs specifies this, and all of C2 depends on it.

**`c1-compile`'s trade-off.** Editor latency and build makespan pull against
each other, and `batch_bandwidth_cap` is exactly the knob that sets the exchange
rate. Without an agreed exchange rate the cap value has no basis. Suggested form
— **[proposal]** — a constrained objective ("minimise editor latency subject to
makespan degrading no more than X% against uncapped") rather than a scalar sum;
easier to defend.

**`c1-media`'s audio/video weighting.** `video-playback` runs 60 Hz at 40% duty,
`audio-playback` 20 Hz at 5%. Audio dropout is more perceptible than a dropped
frame. Equal weighting would push the scheduler toward the wrong optimisation.
If no literature basis is found, record it as a stated assumption.

### Files with no Layer-2 information

Should be declared excluded **in advance**, not discovered afterwards:

- **C5 (t3/t4/t5)** — identical to `c1-media` except for process names; the test
  suite enforces `identical but for the name`. Layer-2 numbers are necessarily
  the same as `c1-media`'s. These are Layer-1 (recognition accuracy) files.
  Useful side effect: if their Layer-2 numbers *differ*, that is a bug signal.
- **`c1-idle`** — five `system-daemon` tasks, near-idle, no contention. Its role
  is "does the recognizer say idle."
- **C6 (3)** — pre-registered misses; diagnostic, not scored.
- **C4 (3)** — meaningful as a **delta against the clean C1 base**, not as an
  absolute.

### Global checks — pass/fail, not scores

Must accompany every reported number:

- provenance breakdown (`fallback` / `held` share) — a condition that scored
  well while mostly running fallback demonstrated nothing; exemptions live in
  the RQ0 gate spec as data (`guard_exemptions`), never in guard code;
- config age;
- starvation floor respected in every condition;
- determinism (same input twice → byte-identical trace);
- total delivered CPU ≤ elapsed virtual time; utilisation sanity.

---

## 7. Harness structure — **[proposal]**

```
   workload files          daemon outputs           simulator output
   (ground_truth)     (config schedule, recog log)      (trace)
        │                      │      │                    │
        │              ┌───────┘      │                    ▼
        │              ▼              │             ┌─────────────┐
        │         ┌─────────┐         │             │ trace reader│
        │         │ runner  │─────────┼────────────▶└──────┬──────┘
        │         └─────────┘         │                    ▼
        │                             ▼             ┌─────────────┐
        │                      ┌────────────┐       │ primitives  │
        └─────────────────────▶│ L1 grader  │       └──────┬──────┘
                               └──────┬─────┘              │
                                      └────────┬───────────┘
                                               ▼
                                        ┌─────────────┐
                                        │  records    │   intermediate file
                                        └──────┬──────┘
                                               ▼
                     scoring spec ─────▶┌─────────────┐
                     (declarative)      │   scorer    │
                                        └──────┬──────┘
                                               ▼
                                        ┌─────────────┐
                                        │   scores    │   intermediate file
                                        └──────┬──────┘
                                    ┌──────────┼──────────┐
                                    ▼          ▼          ▼
                                 guards      gate      report
```

Module responsibilities:

- **runner** — expands the condition × workload × seed matrix, invokes daemon
  and simulator, caches on `(run file hash, schedule hash, simulator version)`.
  Executes; computes nothing.
- **trace reader** — the only place that knows the trace format. Never
  re-implements simulator semantics; `ready` is an explicit event precisely so
  it doesn't have to.
- **primitives** — computes the raw metrics. Knows nothing about which file or
  condition it is looking at.
- **L1 grader** — recognition log vs `ground_truth`. No simulator on this path,
  so it is kept physically separate.
- **scorer** — applies per-file weights and the normalisation formula.
- **guards / gate / report** — validity checks, pass-fail decision, output.

**The two intermediate files are the important part.** `records` in long form —
one row per observation (`workload_id, condition, seed, entity, metric, value`).
Writing them to disk makes re-scoring free when Layer 2 changes, makes a null
result debuggable, and makes every number in the paper traceable to a trace.

The boundary between `records` and `scores` is exactly the boundary between
Layer 1 and Layer 2.

**The search engine belongs in the harness** (archive's placement, and correct —
it drives the simulator repeatedly). It is needed only for failure diagnosis, so
it can be built later, sharing the runner's cache.

**Mock generators unblock all of this.** A mock daemon and mock simulator that
emit hand-written schedules, recognition logs, and traces let the entire harness
be built and validated before either builder delivers. A useful side effect:
hand-writing a mock trace forces Layer-1 gaps into the open immediately.

---

## 8. Gate design

Judging scope — **[§4.1 closed 09-06; re-decided 09-10 with Phase 7's coreset]**:

- **Rule.** A file judges when it is one side of a label-varying pair and its
  scored term registers the rows' difference by design. Demand is not a
  criterion: the per-file headroom admission test (open-questions Q8) is the
  gate's own per-file criterion, below.
- **Judging (27):** C2 (6); the six batch C1 bases (their wanted LOTTERY share
  is what a random row removes, the turnaround term registers it); the fifteen
  C7 counterparts with a term.
- **Reporting-only, by the same rule:** the ten interactive and periodic C1
  bases (nothing runs behind the foreground) — still the honest baseline where
  the whitelist should score perfectly (`building-plan` §3 C1); C3 (no pair;
  transition costs are reported through the switch-window aggregates, not mixed
  into the gate); C4 (label-invariant pairs, read as deltas against their
  originals); `c1-idle`, `c7-idle` (no term).
- **C5, C6** — run, but excluded from Layer-2 aggregation.
- **Layer-1 exclusion (new):** the five pre-committed-miss files judge (the
  gate needs labels, not recognizability) but leave recognition accuracy.

The pass criterion should be **fixed in a committed file before execution**, not
in a meeting. Written down as data, a change after seeing the numbers leaves a
git trace.

```yaml
rq0:
  judging_rule: >
    Decided 2026-09-10 (Phase 7, 7.7). A file judges when it is one side of a
    label-varying pair and its scored term registers the rows' difference by
    design. Demand is not a criterion; the per-file admission test below is.
  judging_files: [c2-p1a, c2-p1b, c2-p2a, c2-p2b, c2-p3a, c2-p3b, c1-compile, c1-ml-train, c1-render, c1-transcode, c1-indexing, c1-backup, c7-browsing, c7-office, c7-mail, c7-dev, c7-photo, c7-meeting, c7-gaming, c7-media, c7-video-edit, c7-compile, c7-ml-train, c7-render, c7-transcode, c7-indexing, c7-backup]
  reporting_only: [c1-browsing, c1-office, c1-mail, c1-dev, c1-photo, c1-meeting, c1-media, c1-video-edit,
                   c1-idle, c7-idle, c3-*, c4-*]
  judging_notes:                     # caveats on members — how to read the number, never a reason to drop it
    c7-gaming: >
      Base already needs 1.46 lanes; with the scan, frames miss under every
      row, so only the gap between rows reads, not the absolute miss rate.
    c7-meeting: >
      Both of its rows are EDF; TIMER consumers sit in the deadline class and
      one residual slice (10 ms since the 2026-09-11 boot default) equals
      video's tick tolerance exactly, and fixed no longer demotes the video
      burst, so on the arithmetic the rows tie and fixed ties too: expected no
      headroom on every term, on a knife edge that two executor rules decide
      (memo 2026-09-11 §5, asked of 인경민). Membership re-decided in the
      pre-registration sub-task once the rules are in (pair review finding 5
      addendum).
    c7-media: same as c7-meeting.
  excluded_layer1: [c1-indexing, c7-ml-train, c7-render, c7-transcode, c7-backup]   # pre_committed_miss segments: out of recognition accuracy, in Layer 2
  per_file_criterion: >
    The open-questions record's Q8 admission test, applied as the gate's own
    rule: pass = at least K of the judging files show a per-file oracle-vs-random
    gap of at least g. K and g set here before execution (Stage 5). No file is
    removed after its gap is seen; a statistic no single file can dominate.
  separate_reporting:
    c1-gaming:
      reason: >
        Added 2026-09-06 after reading demand estimates (task 3.1), before
        execution. Single-situation file at demand 1.46, the highest in the
        coreset; lets gap size be read against demand level separately from
        family type. Not in the judging set: no pair, so no attribute
        variation (C2 asks whether attribute recognition matters, this file
        asks whether mode recognition matters, with a different primary
        metric); and selecting the highest-demand file after reading demand
        numbers is selection along an axis correlated with expected gap size.
  excluded_layer2: [c5-*, c6-*]
  guard_exemptions:
    c6-dual:
      guards: [random-beats-oracle, fallback-share]   # audit the full guard list in Stage 4
      reason: >
        Ground truth is `mode: ambiguous` with no `background_wanted`; the
        vocabulary admits no legal oracle answer, so the oracle condition runs
        the file on fallback/held by construction (task 3.2). Random draws legal
        answers and may beat it; the fallback share is 100% by design.
  threshold: <set after metric definitions are fixed>
  random_seeds: <N>
  on_failure: config-search-first
  driver_table_version: v0
  driver_table_schema: <set in Stage 0.5>
```

**`c1-gaming` as an accidental natural experiment — [decided 09-06].** The
confound that family membership changes both what is tested and how much
headroom exists is partly broken by one file:

```
c1-gaming    single situation  ·  demand 1.46   ← highest in the coreset
other C1     single situation  ·  demand < 1.0
C2           intent pairs      ·  demand 1.12–1.29
```

This makes it possible to ask whether gap size tracks family type or demand
level. It is **not** added to the judging set — no pair, so no attribute
variation; and choosing the highest-demand file after reading demand numbers
is an optimistic choice (demand is an input property, not an outcome, so not
p-hacking — but selection along an axis correlated with expected gap size). It
is a pre-registered separate reporting line in the RQ0 gate spec, reason recorded
in-file, so whichever way the result lands the timing of the choice is in git.

Note that `random` as a condition is **not yet defined**: what it draws
uniformly from (one of 16 modes? one of the table's rows? the whole config
space?) is unspecified anywhere, and a single draw is a point rather than a
distribution. Both the draw definition and the seed count need agreement with
박이안 — this is half of RQ0's x-axis.

### What passing does and does not establish

Passing supports exactly this: *on at least K of the twenty-seven judging
files — the three C2 pairs, the six batch C1 bases with their counterparts, and
the interactive and periodic counterparts — perfect recognition through the v0
table beats random recognition by at least g, so recognition quality has room
to matter.* That is what RQ0 asks, and it is enough to proceed.

Passing with an untuned table is, if anything, stronger evidence than passing
with a tuned one — the "you tuned it to the test set" objection does not apply.

It does not establish that the interactive C1 bases, C3, or C4 will show gaps, and it does not establish
that the table chose *good* configurations — only that its rows differ. A bad
table can produce a gap. That question is RQ5's third check and remains open
after the gate.

---

## 9. Ordered work plan

### Stage 0 — verification (half a day)

- [ ] **0.1** Read the per-file static demand estimates in `dataset/build/`.
      Settles §4.1 and determines whether the judging set is 6 files or 12.
      **Do this first.**
- [ ] **0.2** Check `c6-dual`'s out-of-vocabulary labels against oracle and
      validator behaviour. Record; out of RQ0 scope.
- [ ] **0.3** Protocol freeze signature — flip config schedule, telemetry, and
      recognition log from `draft` to `frozen`; one changelog line. Not a design
      session. Worth doing promptly: a doc marked `draft` invites a builder to
      deviate quietly, which is the failure mode §8.3 warns about.
- [ ] **0.4** **[new 09-06]** Correct the stale documentation lines in §4.8 —
      `research-proposal` Part 9 Phase 1 ("modes only, no attributes"), and
      `terminology.md`'s five-mode vocabulary and `has_realtime_encoder`. Same
      changelog entry as 0.3. While in there, sweep for other status labels that
      lag the freezes.

### Stage 0.5 — driver table format — **[new 09-06, team decision, blocks Stage 3]**

§8.2 decision 3. Three signatures. **Kick this off at the start of the week and
run Stages 1–2 solo while it is in flight** — it is a discussion item, not a
sit-and-wait item.

- [ ] **0.5.1** Write the invariant down as a sentence and get agreement on it
      as the acceptance criterion (§4.7): every `system`-only condition receives
      an identical configuration for the same `(mode, background_wanted)`.
- [ ] **0.5.2** Enumerate candidate formats with their consequences for the
      invariant, the A/B/C ladder, and validator rule 2. Key extension is
      already ruled out (§4.7); "disposition + per-algorithm derivation" needs
      its axes defined before it counts as a candidate. **Bring options to the
      team; do not decide alone.**
- [ ] **0.5.3** Settle whether archive Q5's ceiling claim survives a variant B
      that can out-choose the table's algorithm. This may have to precede
      0.5.2 — the answer determines whether B passes through the table at all.
- [ ] **0.5.4** Correct `research-proposal` §5.2 (`llm_algo` row) and §4.6, and
      the `daemon-guide` §5 implication that the config mapper is simple wiring.
- [ ] **0.5.5** Promote the table to a data contract with the same status as the
      others, so **v0 and v1 are instances of one schema** (required by RQ5's
      two-table ladder and by the v1 gate re-run).
- [ ] **0.5.6** Sign and changelog.

### Stage 1 — fix Layer 1 (parallel with 0.5)

Metric definitions are independent of the table's format, so these run
concurrently. Do this by hand-writing mock traces; defining it abstractly hides
the gaps.

- [ ] **1.1** Hand-write three mock traces — a reduced `c1-office` (focused
      interactive), `c1-media` (two TIMER tasks), `c2-p1a` (interactive vs
      batch). The miniature in `data-contracts` §9 is the seed; 20–40 lines each.
- [ ] **1.2** Decide the Layer-1 questions as they surface (§5).
- [ ] **1.3** Write the decisions up — a `docs/metrics.md` or equivalent. This is
      §8.2 decision 4, so it needs three signatures, but the draft is faster
      written alone.
- [ ] **1.4** Fix the `records` schema.

### Stage 2 — harness lower half (no simulator needed)

- [ ] **2.1** trace reader — validated against the mocks.
- [ ] **2.2** primitives — pure functions, no knowledge of file or condition.
- [ ] **2.3** records output. **Check against hand-computed values.** Errors here
      propagate into everything downstream.

### Stage 3 — driver table v0 and Layer 2 (iterative) — **requires 0.5**

With the format fixed, this becomes content authorship. These two feed back into
each other; expect to alternate.

- [ ] **3.1** Fix scope: include `background_wanted` (omitting it makes C2
      inexpressible). Extract the rows C1–C4 actually exercise by scanning
      `ground_truth` — likely under ten.
- [ ] **3.2** Write v0 for those rows: algorithm + params + `batch_bandwidth_cap`,
      each with **one sentence of justification**. A row whose justification
      cannot be written signals a Layer-2 gap — go to 3.3.
- [ ] **3.3** Write the scoring spec. The three decisions in §6 are unavoidable
      here.
- [ ] **3.4** Fill the remaining rows, including unreachable ones, with textbook
      defaults so the validator raises an event rather than crashing.
- [ ] **3.5** **Pair review** — put same-mode `wanted=true/false` rows side by
      side and check the configurations are meaningfully far apart, especially
      the six rows C2 exercises (§4.3, §4.4). This is RQ5's first check, pulled
      forward.

### Stage 4 — harness upper half

- [ ] **4.1** scorer — weights plus normalisation, with the denominator floor.
- [ ] **4.2** guards, including: do the two files of a C2 pair produce
      *identical* traces? If so, the configuration never actually changed — catch
      this before a zero gap gets interpreted. Plus the §6 global checks.
- [ ] **4.3** mock daemon + mock simulator; run the whole pipeline on mocks.
- [ ] **4.4** runner with the execution cache.
- [ ] **4.5** report — every number accompanied by its provenance breakdown.

### Stage 5 — pre-registration (the point of no return)

Meaningful only once the table's format (0.5) and both metric layers (1, 3) are
fixed — the shape of the instrument has to be settled before a threshold on its
output means anything.

- [ ] **5.1** Commit the RQ0 gate spec file.
- [ ] **5.2** Set the threshold — possible only now that both layers are fixed,
      and necessarily before seeing any numbers.
- [ ] **5.3** Fix the `random` condition's draw definition and seed count
      **with 박이안**.
- [ ] **5.4** Write down the failure procedure (config search before workload
      redesign).
- [ ] **5.5** Freeze the scoring spec; later changes need a changelog and three
      signatures.

### Stage 6 — integration and execution

Dependent on the two builders.

- [ ] **6.1** 인경민's integration gate: one C1 file, MLFQ, byte-identical reruns.
- [ ] **6.2** Swap mock simulator for the real one; confirm records come out in
      the same shape.
- [ ] **6.3** 인경민's algorithm extension — EDF/Lottery/FIFO, batch class, caps,
      EDF deadlines, mid-run switching. **The critical path.**
- [ ] **6.4** 박이안's daemon through the config mapper.
- [ ] **6.5** End-to-end smoke: one file, `fixed`, daemon → simulator → harness.
- [ ] **6.6** Run RQ0: all coreset files × 3 conditions, `random` across N seeds.
- [ ] **6.7** **Check guards before looking at results.**
- [ ] **6.8** Judge per the RQ0 gate spec. On failure, config search before anything
      else (§4.3).

---

## 10. Parallelism

Stages 0, 1, 2, 4, and 5 are entirely independent of the simulator and the
daemon. They are the contracts/infrastructure owner's work and can start now.

Stage 0.5 is the one new dependency, and it is a *team* dependency rather than a
builder one. Sequencing:

```
  solo track   0 ──▶ 1 ──▶ 2 ──▶ [3] ──▶ 4 ──▶ 5 ──▶ [6]
  team track   0.5 ─────────────┘                     │
  builders     ─────────────────────────── 6.1/6.3 ───┘
```

Stage 3 is gated on 0.5; Stage 4 is gated on 6.3. If 0.5 has not landed by the
end of Stage 2, useful work in the window:

- the Layer-1 grader (needs only recognition logs — no simulator);
- scoring specs for C3/C4 (outside RQ0, needed for RQ2);
- the search engine skeleton (failure diagnosis);
- the related-work section differentiating from SchedCP.

---

## 11. To raise with the team

1. **Driver table format** (§4.7) — **new, and now first.** Blocks Stage 3, is
   §8.2 decision 3, and cannot be deferred past the gate because v0 and v1 must
   share a schema. Bring 0.5.2's candidate list and 0.5.3's ceiling question.
   Includes correcting `research-proposal` §5.2/§4.6.
2. **Metric definitions** (§8.2 decision 4) — the Stage 1 output. Three
   signatures required.
3. **`random` condition definition and seed count** — with 박이안. Currently
   unspecified anywhere; half of RQ0's x-axis.
4. **Simulator semantics** (`simulator-guide` §9) — with 인경민, before or during
   his implementation. §9.1 (wake with no waiter) and §9.2 (TIMER t₀) change how
   much demand interactive tasks express, so they are not cosmetic.
5. **Phase-2 scope for the simulator** — the current TODO stops 인경민's Phase 1
   at the integration gate, but RQ0 needs the algorithm set beyond it. 6.3 is the
   critical path and he does not currently know it is his. Making that explicit
   is probably the single most useful thing to hand him now.
6. **Gate one-directionality and the failure procedure** (§4.2, §4.3) — a change
   to how the proposal frames RQ0 failure, so it needs agreement rather than
   unilateral adoption.
7. **Documentation status audit** (§4.8) — two ratified documents lag the
   vocabulary and attribute freezes. Cheap to fix now; §8.3's named failure mode
   if left.
