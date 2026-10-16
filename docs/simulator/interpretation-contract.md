# Interpretation Contract — workload ⇄ simulator
> Status: normative · Created 2026-08-26 · Updated 2026-10-16

The contract between the workload dataset and the simulator: what a canonical workload file contains and how the simulator turns it into scheduled tasks. Written before the simulator exists; simulator Phase 0 is built to this document. Decision record: `_dev/archive/2026-08-26-workload-generation-grill.md` (D10–D16).

The simulator reads **canonical workload files only** — never timelines, never `archetypes.yaml`. (Pipeline: `archetypes.yaml` + timeline (its seed in its `meta`) → workload; see docs/workload/building-plan.md.)

## 1. The simulated machine

- **One lane** (Q1 of the archived open-questions record, ratified — `_dev/archive/2026-08-23-design-meeting-open-questions.md`): the scheduler answers "who holds the lane until the next event." CPU-only; no GPU axis in any schema.
- **Virtual time**, discrete-event; integer microseconds throughout (rt-app precedent).
- **RNG-free simulator.** All randomness is resolved at compile time into the canonical file. Same workload file + same config schedule ⇒ identical run; any policy-internal randomness (e.g. lottery draws) comes from a PRNG the simulator seeds deterministically per run. (`meta.sampled` records `{seed, archetypes.yaml@<git blob hash>}`, the library named by the hash of its content, so every concrete number traces to its distribution.)

## 2. The governing timing principle

> **Compile time resolves all randomness; run time resolves all timing that scheduling can influence.**

- **Exogenous times — pinned absolute in canonical:** top-level process arrivals, segment boundaries, distractor injections, segment-bound departs (the user closing an app), wake events — keystrokes, and a measured program's timer-component wakes at their sampled times. These are user behavior or the program's own measured timing; the scheduler cannot affect them.
- **Endogenous times — emergent at run time:** departs of finite tasks (the program reaches EXIT when the scheduler lets its work finish), and spawn moments inside an orchestrator's fork loop. These are scheduling outcomes; pinning them would make the workload open-loop and erase the good-vs-bad-config divergence the experiments measure.

Every rule in this contract is an instance of this principle.

## 3. Event grammar — six primitives

Each task is a small program over six primitives; the interpreter is a per-task VM feeding the DES core (a 7-way switch counting EXIT). The DES core and executor never see archetype names — they exist only at compile time.

| primitive | semantics |
|---|---|
| `RUN(duration)` | burn CPU for `duration` of lane time (may be preempted; duration is CPU demand, not wall time) |
| `SLEEP(duration)` | voluntary relative wait; task not runnable until now+duration |
| `TIMER(period)` | absolute periodic wake: runnable at t₀+k·period regardless of when the previous iteration finished — drift-free (rt-app `timer{ref,period}`). Late iterations accumulate as backlog; they are not silently skipped |
| `WAIT(channel)` | block until a WAKE (or exogenous wake event) on `channel`. Proposed (2026-10-16, `docs/data-contracts.md` §14), in force once 인경민 agrees: an orchestrator's `WAIT children:<id>` completes when the last child it spawned ends, and without blocking, with a zero-wait `ready` line, when none is live at the WAIT (§5) |
| `WAKE(target)` | make `target` runnable (waker–waiter edges). `target` is any task id of the file, a spawn-table child included: the build trees' object jobs wire their members child to child |
| `FORK` / `EXIT` | create the next child from the spawn table (§5) / terminate this task |

Periodic tasks use TIMER, never SLEEP loops: relative sleeps drift under delay, silently lowering demand exactly under bad configs.

## 4. Canonical format (the only simulator-facing format)

One closed type per file; the parser has zero case-splits. The JSON Schema is `dataset/schema/workload.schema.json`; this section fixes its semantics.

- **`meta`** — id, `derived_from` (`<timeline path>@<git blob hash>`), `sampled: {seed, archetypes.yaml@<git blob hash>}` — each file named by the git blob hash of its content; the schema also admits harness-only grading expectations, which no compiled file carries. Not read by the scheduler.
- **`ground_truth`** — flat list of labeled intervals (mode + attributes). Visible to the oracle condition and the Layer-1 grader only.
- **`focus`** — the window-focus track, `[{t_start, t_end, task}]`: which top-level task holds the window focus over which pinned intervals (2026-10-11, data-contracts §4 and §14). Shown to the recognizer through the visible projection; not read by the scheduler — the run file is the `events` alone.
- **`events`** — flat timestamped list with a **closed op set of two**:
  - `{t, op: arrive, id, name, declared_class, program, depart?, spawn_table?, fork_cap?}` — a task comes into existence carrying its fully resolved program (every distribution already sampled to concrete values). `id` is its identity, unique in the file, spawn-table children included; `name` is the process name the recognizer sees. `declared_class` is the scheduling class the program declares for itself, `normal` or `idle` — an `idle` task runs only when no task of another class is runnable and is preempted at once when one wakes, under every algorithm (data-contracts §4) — required on every task record, each spawn-table entry included. `depart` is present **iff** the task is segment-bound (§5). An orchestrator carries its `spawn_table` and `fork_cap` (§5).
  - `{t, op: wake, target, channel}` — an exogenous wake, pre-sampled at compile time: a keystroke on `input:<id>`, or — most of them — one of a measured program's own timer-component wakes on `timer:<id>`. The task blocks on `WAIT(channel)`; these events supply the wakes at absolute times.

## 5. Lifetime classes

| class | depart | how it ends |
|---|---|---|
| `segment-bound` | pinned in the arrive event | exogenous — user closes it |
| `finite` | none | program reaches EXIT; time is a scheduling outcome |
| `spawned` | none | created at run time via FORK; ends via EXIT |

No program runs out of instructions. A segment-bound program ends blocked — its last step a WAIT, a TIMER whose tick falls at or past the depart, or an unbounded LOOP — and its pinned depart removes it; a finite or spawned task ends with EXIT. The compiler builds every program so, and the canonical lint checks each program's last step against its lifetime class (`dataset/tools/wlc/linter.py`, `lint_canonical`).

**FORK semantics:** an orchestrator's program carries a pre-sampled, ordered **spawn table** — one fully resolved child program per entry, every lifetime already drawn (e.g. `c1-compile`'s `make`: 17,448 entries, 2,908 object jobs of six processes each — `sh`, `gcc`, `cc1`, `as`, `fixdep`, `rm`). At run time the fork/wait-for-slot loop consumes the table in order, at most `fork_cap` of the orchestrator's children alive at once. The cap is a binding-time parameter: the timeline's `parallelism_cap` (8 in `c1-compile`, design) times the six members of an object job — `fork_cap` 48 there, eight jobs in flight as in `make -j8`. *Which* children exist and *what they do* is compile-time; *when* each arrives is emergent. After its last FORK an orchestrator waits on `children:<id>`, `<id>` its own (`dataset/tools/wlc/compiler.py`, `build-orchestrator` and `module-build-orchestrator`; `make` in `c1-compile` waits on `children:build`, then EXITs), and no WAKE or wake event in the file targets the orchestrator. Proposed (2026-10-16, `docs/data-contracts.md` §14), in force once 인경민 agrees in answer to Phase 9's final memo: the executor completes that WAIT when the last child the orchestrator spawned ends, and without blocking, with a zero-wait `ready` line, when none is live at the WAIT.

**Sampling granularity** (compile-side, per archetype field): *per-instance* (one draw per spawned task — spawn-table entries), *per-task* (one draw reused across iterations — e.g. per-schedule runtime, matching the source's "stable per task"), *per-iteration, only when bounded* (pre-sampled into the event stream — input wake events).

## 6. Constructor specialization — chain topology

`game-task-chain` is resolved at **compile time**, not in the interpreter: the compiler expands the topology into ordinary tasks with WAIT/WAKE channels wired from the head to the last member, one linear relay standing in for the source's frame path "from a user input to display update" (`lavd-ossna24`), which names no intermediate stage — the linearisation is the dataset's. `wineserver` is a member of the constructed chain: the constructor inserts one member, `<iid>.wineserver`, named `wineserver`, right after the head, so a chain of `chain_length` members compiles to `chain_length` + 1 tasks (17 in `c1-gaming`). After construction every task is a plain program; the specialness is confined to initialization.

## 7. Lane scaling and the demand budget

- Archetype values are scaled to the single lane by a **compile pass** over the fields an entry declares `scalable`, with the evidence in `modeling_notes` — never by editing archetype values. One entry declares any: `game-task-chain`, whose chain RUN values are scaled so that the chain's aggregate demand per frame is the timeline's `lane_share` of the lane; every other entry's values are its software's CPU on one pinned core. Every timeline compiles once, lane-scaled (`single`), the one mode the compiler knows.
- **Demand budget:** a compiled file's demand is reported, not held. The compiler records its static estimate — each task's CPU spread over its lifetime, its arrival to its depart or the file's end — per file and per ground-truth segment in the set's manifest (`dataset/tools/wlc/estimate.py`) and fails no file on it. Every job is bound whole as measured, so a file's demand follows from the measurement; holding it to a window — the ~100–150 % of the lane that gated files until 2026-10-09 — would have meant bending measured lengths; the pair review reads the contended segments. The RQ0 gate's per-file criterion — `random` read against the oracle's headroom over `fixed` — is the gate's own reading of each judging file, not a demand check.

## 8. Boundaries

- **Scope of this contract:** the workload file and its execution semantics only. The simulator's second input (the config schedule) and every runtime-side contract are specified in `docs/data-contracts.md`; the scheduler-configuration language is frozen in `docs/recognition-vocabulary.md`.

- **What the numbers are for:** archetype numbers never reach the recognizer or the driver table — they build the simulated machine the executor schedules. They set the cost of misrecognition; realistic deadlines, fork storms, and chains are what make good and bad configs diverge in Layer 2.
- **Unaffected components:** DES core, executor, algorithms, config schedule, validator, driver table, condition ladder (the Q7 "unaffected" list). The interpreter is a new front-end that feeds events in; the executor still schedules plain tasks.
- **First integration test:** `archetypes.yaml` + one C1 timeline, compiled and executed end-to-end.
