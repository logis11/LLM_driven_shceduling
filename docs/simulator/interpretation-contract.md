# Interpretation Contract — workload ⇄ simulator
> Status: normative · Created 2026-08-26 · Updated 2026-08-27

The contract between the workload dataset and the simulator: what a canonical workload file contains and how the simulator turns it into scheduled tasks. Written before the simulator exists; simulator Phase 0 is built to this document. Decision record: `_dev/archive/2026-08-26-workload-generation-grill.md` (D10–D16).

The simulator reads **canonical workload files only** — never timelines, never `archetypes.yaml`. (Pipeline: `archetypes.yaml + timeline (+ scenario catalog) + seed → workload`; see docs/workload/building-plan.md.)

## 1. The simulated machine

- **One lane** (Q1 of the archived open-questions record, ratified — `_dev/archive/2026-08-23-design-meeting-open-questions.md`): the scheduler answers "who holds the lane until the next event." CPU-only; no GPU axis in any schema.
- **Virtual time**, discrete-event; integer microseconds throughout (rt-app precedent).
- **RNG-free simulator.** All randomness is resolved at compile time into the canonical file. Same file + same scheduler ⇒ identical run. (`meta.sampled` records `{seed, archetypes.yaml@commit}`, so every concrete number traces to its distribution.)

## 2. The governing timing principle

> **Compile time resolves all randomness; run time resolves all timing that scheduling can influence.**

- **Exogenous times — pinned absolute in canonical:** top-level process arrivals, segment boundaries, distractor injections, segment-bound departs (the user closing an app), input wake events. These are user behavior; the scheduler cannot affect them.
- **Endogenous times — emergent at run time:** departs of finite tasks (the program reaches EXIT when the scheduler lets its work finish), and spawn moments inside an orchestrator's fork loop. These are scheduling outcomes; pinning them would make the workload open-loop and erase the good-vs-bad-config divergence the experiments measure.

Every rule in this contract is an instance of this principle.

## 3. Event grammar — six primitives

Each task is a small program over six primitives; the interpreter is a per-task VM feeding the DES core (a 7-way switch counting EXIT). The DES core and executor never see archetype names — they exist only at compile time.

| primitive | semantics |
|---|---|
| `RUN(duration)` | burn CPU for `duration` of lane time (may be preempted; duration is CPU demand, not wall time) |
| `SLEEP(duration)` | voluntary relative wait; task not runnable until now+duration |
| `TIMER(period)` | absolute periodic wake: runnable at t₀+k·period regardless of when the previous iteration finished — drift-free (rt-app `timer{ref,period}`). Late iterations accumulate as backlog; they are not silently skipped |
| `WAIT(channel)` | block until a WAKE (or exogenous wake event) on `channel` |
| `WAKE(target)` | make `target` runnable (waker–waiter edges) |
| `FORK` / `EXIT` | create the next child from the spawn table (§5) / terminate this task |

Periodic tasks use TIMER, never SLEEP loops: relative sleeps drift under delay, silently lowering demand exactly under bad configs.

## 4. Canonical format (the only simulator-facing format)

One closed type per file; the parser has zero case-splits. The JSON Schema is a separate build artifact (backlog step 2); this section fixes its semantics.

- **`meta`** — id, `derived_from` (timeline@commit), `sampled: {seed, archetypes.yaml@commit}`, harness-only grading expectations. Not read by the scheduler.
- **`ground_truth`** — flat list of labeled intervals (mode + attributes). Visible to the oracle condition and the Layer-1 grader only.
- **`events`** — flat timestamped list with a **closed op set of two**:
  - `{t, op: arrive, name, program, depart?}` — a task comes into existence carrying its fully resolved program (every distribution already sampled to concrete values). `depart` is present **iff** the task is segment-bound (§5).
  - `{t, op: wake, target, channel}` — an exogenous wake (pre-sampled aperiodic input, e.g. keystrokes for interactive tasks). The task blocks on `WAIT(channel)`; these events supply the wakes at absolute times.

## 5. Lifetime classes

| class | depart | how it ends |
|---|---|---|
| `segment-bound` | pinned in the arrive event | exogenous — user closes it |
| `finite` | none | program reaches EXIT; time is a scheduling outcome |
| `spawned` | none | created at run time via FORK; ends via EXIT |

**FORK semantics:** an orchestrator's program carries a pre-sampled, ordered **spawn table** — one fully resolved child program per entry (e.g. 2,430 compiler children, lifetimes already drawn). At run time the fork/wait-for-slot loop (parallelism cap; cap value is a binding-time parameter, default `-j8` by stated convention) consumes the table in order. *Which* children exist and *what they do* is compile-time; *when* each arrives is emergent.

**Sampling granularity** (compile-side, per archetype field): *per-instance* (one draw per spawned task — spawn-table entries), *per-task* (one draw reused across iterations — e.g. per-schedule runtime, matching the source's "stable per task"), *per-iteration, only when bounded* (pre-sampled into the event stream — input wake events).

## 6. Constructor specialization — chain topology

`game-task-chain` is resolved at **load time**, not in the interpreter: the compiler expands the topology into N ordinary tasks with WAIT/WAKE channels wired (input → engine → … → display). After construction every task is a plain program; the specialness is confined to initialization. (Open item: whether wineserver joins this constructed graph or stays a separate `system-daemon` binding — decided at constructor implementation, recorded in `modeling_notes`.)

## 7. Lane scaling and the demand budget

- Archetype values whose sources are machine-aggregate (measured on multi-core machines) are scaled to the single lane by a **compile pass**, per-archetype declared fields with the evidence in `modeling_notes` — never by editing archetype values. Two compile modes per timeline: `-native` (as-measured, released only, never executed here) and `-single` (lane-scaled; the only thing this simulator runs).
- **Demand budget:** every compiled `-single` workload's aggregate demand lands in the measurable oversubscription regime (~100–150% of the lane); the per-file oracle-vs-random admission test (open-questions record Q8) is the enforcement mechanism.

## 8. Boundaries

- **What the numbers are for:** archetype numbers never reach the recognizer or the driver table — they build the simulated machine the executor schedules. They set the cost of misrecognition; realistic deadlines, fork storms, and chains are what make good and bad configs diverge in Layer 2.
- **Unaffected components:** DES core, executor, algorithms, config schedule, validator, driver table, condition ladder (the Q7 "unaffected" list). The interpreter is a new front-end that feeds events in; the executor still schedules plain tasks.
- **First integration test:** `archetypes.yaml` v0.1 + one C1 timeline, compiled and executed end-to-end.
