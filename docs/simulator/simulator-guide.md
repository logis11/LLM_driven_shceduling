# Simulator Guide — what to build, what's fixed, what's yours
> Status: draft · Created 2026-08-28 · Updated 2026-08-28

The second half of the simulator onboarding guide (read `background-guide.md` first — this one assumes it). It's a spec, but a deliberately breathing one: the **contract surface** (input format, execution semantics, determinism, output obligations) is fixed and stated here in full; the **inside of the machine** (language details, data structures, code layout, testing) is yours. Fixed things say "must." Everything else is a suggestion you may overrule in your own tree.

---

## 1. The machine at a glance

```text
   dataset/build/coreset-single/*.workload.json
                    │
                    ▼
            ┌──────────────┐
            │   loader     │  parse + validate one canonical file
            └──────┬───────┘
                   ▼
   ┌───────────────────────────────┐
   │   discrete-event core         │   virtual clock (integer µs)
   │                               │   event queue (arrivals, wakes,
   │   ┌─────────┐  ┌─────────┐    │    timers, slice expiries, departs)
   │   │ task VM │  │ task VM │ …  │   one tiny interpreter per task,
   │   └─────────┘  └─────────┘    │    stepping through its program
   │            ▲                  │
   │            │ "who runs now?"  │
   │      ┌─────┴─────┐            │
   │      │ scheduler │  ◀── swappable policy (MLFQ first)
   │      └───────────┘            │
   └──────────────┬────────────────┘
                  ▼
              trace file      →  the harness reads this and computes metrics
```

Four pieces: a **loader**, a **DES core** with one **task VM** per live task, a **scheduler** behind a narrow interface, and a **trace writer**. That's the whole simulator.

## 2. The non-negotiables

Everything in this section is contract, not preference.

1. **Input is canonical workload JSON only.** The simulator never reads timelines, never reads `archetypes.yaml`, never sees an archetype name. Validation reference: `dataset/schema/workload.schema.json`.
2. **One lane.** Exactly one simulated CPU. The scheduler answers one question: *who holds the lane until the next event*.
3. **Integer microseconds.** All times and durations are integer µs. No floats in time arithmetic, ever — floats drift, and drift breaks reproducibility.
4. **Zero runtime randomness.** The simulator contains no RNG. Same workload file + same scheduler + same configuration ⇒ **byte-identical trace**. (When lottery scheduling arrives later, its draws will come from a seeded PRNG whose seed is part of the configuration — still deterministic.) This property should be a test you run constantly, not a hope.
5. **The scheduler never sees `ground_truth` or `meta`.** Hand the scheduler the events and nothing else. The answer key stays sealed; enforce it with code structure (the scheduler module simply never receives those objects), not discipline.
6. **Names are labels, ids are identity.** All internal bookkeeping keys on `id` (unique per file, linter-enforced). `name` is what a future recognizer will see; names can repeat and can lie. Nothing in scheduling may branch on `name`.
7. **The timing principle.** Times pinned in the file (arrivals, wakes, departs) happen at exactly those times no matter what the scheduler does. Times *not* in the file (when a finite task finishes, when a forked child starts) emerge from scheduling. Never "helpfully" pin an emergent time or delay a pinned one.

## 3. The input, field by field

One file = one run. Top level: `meta`, `ground_truth`, `events`.

**`meta`** — read it for logging/provenance if you like; it must not influence execution. (`meta.expectations`, when present, is harness-owned grading data — skip it.)

**`ground_truth`** — do not deliver this to the scheduler (non-negotiable 5). The simulator itself has no use for it in Phase 0.

**`events`** — a flat list, sorted by `t`, with exactly two shapes:

```jsonc
// A task comes into existence:
{ "op": "arrive", "t": 0, "id": "editor", "name": "code",
  "depart": 180000000,          // present IFF the task is segment-bound
  "program": [ /* instructions, §4 */ ],
  "spawn_table": [ /* children, present iff program contains FORK */ ],
  "fork_cap": 8                 // parallelism cap, only with spawn_table
}

// An external stimulus (keystroke, network reply) at a pinned time:
{ "op": "wake", "t": 2098333, "channel": "input:editor", "target": "editor" }
```

Three task lifetime classes, distinguishable at a glance:

| class | how you spot it | how it ends |
|---|---|---|
| segment-bound | has `depart` | at `depart`, sharp — the "user" closed the app. Remove it whatever it was doing |
| finite | top-level arrive, no `depart` | its program reaches `EXIT`; *when* that happens is a scheduling outcome |
| spawned | never in `events` — lives inside a `spawn_table` | created at run time by its parent's `FORK`; ends via its own `EXIT` |

## 4. The instruction set

Each task's `program` is a list of instructions; the task VM steps through them in order. Seven opcodes (six primitives plus one VM-internal control-flow form). A useful mental model: each task VM is a tiny coroutine, and the DES core is the runtime that resumes them.

### `{ "op": "RUN", "us": N }`
Consume N microseconds of *lane time*. This is CPU demand, not wall time: if the task gets preempted after 300 µs of a 1000 µs RUN, the remaining 700 µs demand survives and continues whenever the task next holds the lane. A RUN's wall-clock extent is exactly what the experiment measures — never treat it as a fixed interval.

A concrete arithmetic check for your implementation: task A executes `RUN 1000` starting at t=5000. At t=5300 the scheduler preempts it for 2000 µs of other work, then lets it back on. A's remaining demand at re-entry is 700 µs, so the RUN completes at t=8000. Total demand delivered: exactly 1000 µs. Wall-time extent: 3000 µs. If your simulator ever "loses" or "duplicates" demand across a preemption, every downstream metric silently corrupts — worth a dedicated unit test.

### `{ "op": "SLEEP", "us": N }`
Leave the lane voluntarily; become runnable again at `now + N`. Relative to whenever the sleep starts.

### `{ "op": "TIMER", "period_us": P }`
The metronome. Block until the next tick of this task's period grid — ticks at t₀, t₀+P, t₀+2P, … regardless of how late previous iterations ran (that's the difference from SLEEP: a SLEEP-loop drifts later and later under load; a TIMER doesn't, which is what a 60 fps game actually does). Late ticks **accumulate as backlog**: if the task was stuck so long that two ticks passed, the next two TIMERs complete immediately — missed frames turn into pressure, not silence.

Worked example of the backlog rule, using the 60 fps grid (P = 16,667 µs, ticks at 0, 16667, 33334, 50001, …): a frame task finishes frame work and reaches its next TIMER at t=14000 — it blocks until the t=16667 tick. Fine so far. Now suppose a heavy stretch keeps the task off the CPU and it doesn't reach its TIMER again until t=40000. Two ticks (16667 and 33334… whichever it hadn't consumed yet) have passed unconsumed. The rule: those TIMERs complete *immediately*, one per loop iteration, so the task rattles off the overdue frames back-to-back, and only once it has caught up with the grid does a TIMER actually block again (until t=50001). The effect is that a starved periodic task piles up pressure and fights to catch up — like a real game engine — instead of quietly skipping frames, which would *reduce* CPU demand exactly when the scheduler misbehaves and mask the damage the experiment wants to see.

In the compiled coreset, TIMER appears in shapes like the frame producer of the gaming files:

```jsonc
{ "op": "LOOP", "count": "unbounded", "body": [
    { "op": "TIMER", "period_us": 16667 },   // 60 fps grid
    { "op": "RUN",   "us": 6667 }            // this frame's work
] }
```

### `{ "op": "WAIT", "channel": "…" }`
Block until a wake addressed to that channel arrives — either an exogenous `wake` event from the file, or a `WAKE` instruction executed by another task. This is how "editor waits for a keystroke" and "pipeline stage waits for its upstream" both work.

### `{ "op": "WAKE", "target": "<task-id>" }`
Make the target task runnable (it's the sending half of task-to-task WAIT/WAKE edges). The gaming files use chains of these: a frame source ticks on a TIMER, RUNs, WAKEs the next stage, which RUNs and WAKEs the next — a 16-task bucket brigade, once per frame.

### `{ "op": "FORK" }` and `{ "op": "EXIT" }`
`EXIT` terminates the executing task. `FORK` is for orchestrators like `make`: the arrive event carries a `spawn_table` — an ordered, fully pre-written list of children (their ids, names, and complete programs — e.g. 100 `cc1` entries) — and a `fork_cap` (e.g. 8, as in `make -j8`). Each `FORK` instruction creates the *next* unconsumed table entry as a live task. The cap is a wait-for-slot rule: at most `fork_cap` of this parent's children alive at once; a `FORK` while the cap is full blocks until a child exits. So *which* children exist and *what they do* is fixed in the file; *when* each one starts is an emergent, scheduler-dependent time — under a generous scheduler the build fans out fast, under a starved one it crawls. That divergence is signal, not a bug.

Worked example of the cap: `make` has `fork_cap: 8` and rattles off eight FORKs — children c1…c8 now exist and compete for the lane alongside everyone else. Make reaches its ninth FORK while all eight are still alive: the FORK **blocks**. At some later, scheduler-dependent moment c3 happens to finish and EXITs; a slot opens; make's blocked FORK completes and c9 is born. Note what this implies: c9's start time depends on how the scheduler treated c1–c8 — starve the compile family and the whole table drains slowly; favor it and the pipeline stays full. The total *work* is identical either way; the *shape in time* is not.

### `{ "op": "LOOP", "count": N | "unbounded", "body": [ … ] }`
VM-internal repetition — the DES core never sees it as an event; your VM just cycles the body. `count: N` repeats N times. `count: "unbounded"` repeats forever and is legal only for segment-bound tasks: the loop's true terminator is the task's pinned `depart`. (Bounded repetition with per-iteration variety is instead unrolled flat by the compiler — that's why editor programs are hundreds of literal WAIT/RUN pairs while a game frame loop is one compact unbounded LOOP.)

## 4½. A complete worked run, event by event

Nothing builds intuition for a discrete-event core like tracing one tiny run by hand. Here's a miniature workload — two tasks, two keystrokes, all times in µs:

```jsonc
"events": [
  { "op": "arrive", "t": 0, "id": "editor", "name": "code", "depart": 50000,
    "program": [ { "op": "WAIT", "channel": "input:e" }, { "op": "RUN", "us": 3000 },
                 { "op": "WAIT", "channel": "input:e" }, { "op": "RUN", "us": 2000 } ] },
  { "op": "arrive", "t": 0, "id": "hog", "name": "python3",
    "program": [ { "op": "RUN", "us": 20000 }, { "op": "EXIT" } ] },
  { "op": "wake", "t": 10000, "channel": "input:e", "target": "editor" },
  { "op": "wake", "t": 30000, "channel": "input:e", "target": "editor" }
]
```

Run it under the dumbest legal scheduler — non-preemptive run-until-block ("whoever has the lane keeps it until they block or exit"):

| clock | event popped | what happens | lane |
|---|---|---|---|
| 0 | arrive `editor` | its VM starts, first instruction is WAIT → blocks instantly, consuming nothing | — |
| 0 | arrive `hog` | its VM starts on RUN 20000 → runnable; lane is free, scheduler hands it over | hog |
| 10000 | wake `input:e` | editor's WAIT completes → editor runnable. Our scheduler doesn't preempt, so it merely joins the ready set | hog |
| 20000 | hog's RUN completes | next instruction EXIT → hog is gone. Scheduler picks the only runnable task | editor |
| 23000 | editor's RUN 3000 completes | next instruction WAIT → blocks. Nobody runnable | idle |
| 30000 | wake `input:e` | editor runnable again, takes the free lane | editor |
| 32000 | editor's RUN 2000 completes | next instruction WAIT → blocks (no more wakes will come) | idle |
| 50000 | editor's `depart` | segment-bound task removed while blocked. Event queue empty → run over | — |

Now read the metrics off it, exactly as the harness will: the hog's turnaround is 20000 − 0 = 20 ms, and its response time is 0 (it ran immediately). The editor's response to keystroke #1 is 20000 − 10000 = **10 ms** — the keystroke sat unserved while the hog finished — versus effectively 0 for keystroke #2, which arrived to an idle lane. Total lane utilization: 25 ms of work in 50 ms of virtual time, 50%.

The punchline: replace the scheduler with one that preempts on wake, rerun the *identical file*, and keystroke #1's response drops from 10 ms to ~0 while the hog's turnaround stretches from 20 ms to 23 ms. Same input, different timetable, different numbers — that difference is the entire experiment, in miniature. (Also notice everything the walkthrough needed: a clock, an ordered future-event queue, per-task VM state, a ready set, and a policy consulted at decision points. That's your whole architecture checklist.)

## 5. The scheduler seat

The scheduler sits behind a narrow interface, because *swapping it is the entire experiment*. Shape it however feels right in your language; the obligations are:

- The core consults it only at decision points: a task arrives/wakes, the running task blocks/exits/departs, its time slice expires. Between events, nothing to decide.
- It picks who holds the lane next (or idle), and may set a preemption horizon (e.g. "slice of 4 ms").
- It never sees ground truth, names, or archetypes — only scheduling-relevant task state.
- Adding a second policy must not require touching the core.

**Build MLFQ first**, since it's the default policy and every experiment's floor. The concrete rules (this is the standard textbook construction; parameters are configuration, not constants in code):

1. K priority queues. New/woken tasks enter the top queue.
2. Always run from the highest non-empty queue; round-robin within a queue.
3. A task that burns its whole slice at level i is demoted to i+1 (it's acting like batch work).
4. A task that blocks (WAIT/SLEEP/TIMER) before its slice ends stays at its level (it's acting interactive).
5. Every `boost_interval`, everything returns to the top queue — the anti-starvation reset.

To see the rules bite, replay the §4½ miniature under a 3-level MLFQ with a 2000 µs slice: both tasks start in Q0. The hog burns its full 2000 µs slice → demoted to Q1; burns another → Q2, the bottom, where it grinds on. At t=10000 the keystroke makes the editor runnable *in Q0*, which outranks Q2 — the editor preempts, runs its 3000 µs burst (blocking once at slice end and resuming, or spanning slices, depending on your within-queue rule — decide and document), then WAITs again, never demoted because it always blocks early. Keystroke response: ~0 ms instead of the 10 ms the naive scheduler produced. The hog resumes in Q2 and finishes around t=23000 instead of 20000. MLFQ *learned* which task was interactive from behavior alone, in two observations — that's the self-tuning quality every experimental condition stands on.

Its configuration is roughly `{ num_queues, timeslice_ms (per level or schedule), boost_interval_ms }` — exact schema is one of the protocol decisions the three of us freeze together, so keep it in one obvious struct.

**Coming later — design for their existence, but do not build them now:** EDF, lottery, FIFO policies; *runtime configuration swaps* (a "config changed" event mid-run — which means policy state handoff needs a story eventually); per-class bandwidth caps; and telemetry taps (the future daemon needs "the set of live task names changed" notifications — trivial to emit from arrive/depart/exit handling when the time comes). If the scheduler interface is narrow, each of these is an addition, not a rewrite.

## 6. The output: a trace

The simulator's product is a **trace**: a machine-readable record from which every metric is computed *after the fact* by the harness. The simulator times nothing and computes no statistics; it writes down what happened.

The exact format is deliberately **not frozen here** — it's one of the protocol schemas the team freezes together, and you should come to that conversation with a proposal shaped by what was convenient to emit. What it must be able to answer, since all metrics derive from these:

- when each task arrived, first ran, and ended (→ response time, turnaround);
- every interval of lane occupancy: who, from when, to when, and why it ended (block? preempt? exit?) (→ throughput, starvation);
- for TIMER-driven work: each tick's due time and actual completion (→ deadline miss rate, P99 frame latency);
- later, config-change events with provenance (→ the "was the LLM actually driving?" accounting).

Plus two properties: **deterministic** (bit-identical across reruns — trace stability is your reproducibility test) and **append-only simple** (a flat event log, e.g. JSONL, beats a clever nested structure; logs get big, and the harness will stream them).

## 7. Milestone 0 — definition of done

From the project milestones, Phase 0 is: **a workload runs end-to-end and produces reproducible results.** Concretely:

1. Load `dataset/build/coreset-single/c1-office.workload.json` (or any C1 file — they're the simplest: one segment, no forks in some, modest task counts).
2. Run it under MLFQ with some sane default configuration.
3. Emit a trace; run it twice; the traces are identical.
4. The trace passes sanity checks: total delivered CPU ≤ elapsed virtual time; every RUN's demand fully delivered for tasks that completed; segment-bound tasks gone at their departs; no event processed out of time order.

A build-order suggestion (take or leave): clock + event queue first, with fake hand-written tasks; then the VM opcodes one at a time (RUN/SLEEP → WAIT/WAKE → TIMER → LOOP → FORK/EXIT), each with a tiny fixture; then the loader against real coreset files; MLFQ last (a trivial FIFO stub is enough scheduler while building everything else). The first end-to-end run against a real C1 file is *the* integration milestone for the whole project — the dataset side is waiting to see it too.

`c1-compile.workload.json` is the natural second target (exercises FORK/spawn-table/fork_cap hard: `make` + 100 `cc1` children at cap 8), and `c1-gaming` the third (TIMER chains + 16-stage WAKE brigade + hundreds of sleeper tasks — the stress test).

## 8. Yours to decide

Entirely your call, inside `simulator/`:

- **Language.** The proposal drafts C++ (reasoning: logic could port to `sched_ext` later). If you have a strong preference otherwise, raise it — it's a draft, not a verdict.
- Internal architecture, data structures (priority queue choice, VM representation), file layout, naming.
- Build system — your tree owns its own Makefile (or CMake, or cargo…); nothing at repo root constrains you.
- Testing approach and framework. (The dataset tree solved reproducibility-testing with golden-hash manifests; steal the idea if it fits.)
- A `simulator/README.md` in the spirit of `dataset/README.md` — layout, commands, rules of your tree — once there's something to describe.

## 9. Questions the contract doesn't answer (yet)

Real ambiguities you'll hit; none has a decided answer today. When you hit one, decide together with 인지오 and get it recorded (these tend to become contract lines):

1. **A wake with no waiter.** A `wake` event fires (or a `WAKE` executes) while the target isn't currently blocked in `WAIT` on that channel. Queue it (the next WAIT consumes it instantly)? Drop it? Does depth matter (three queued keystrokes = three instant WAIT completions?)?
2. **TIMER's t₀.** The tick grid is t₀+k·P — is t₀ the task's arrival time, its first TIMER execution, or global zero? (Compiled files currently pair unbounded LOOPs with TIMER from arrival; pick the reading that matches and pin it.)
3. **Simultaneous events.** Two events at the same integer microsecond: ordering policy? (File order? Event-type priority? Explicit tie-break rule?) Any answer is fine; it just must be deterministic and written down.
4. **Depart mid-anything.** A segment-bound task's depart lands mid-RUN or with backlogged timer ticks: presumably remove immediately and discard remainders — confirm, and define what the trace records for the truncated interval.
5. **Fork-slot wakeups.** Cap-full parent with several children exiting at once, or a child exiting at the same instant the parent would fork: exact unblock ordering (interacts with question 3).

Running this list to ground early — even before code — would make a good first working session with the dataset side.

## 10. Terms for the inside of the machine

The background guide's glossary covers the project vocabulary; these are the extra words this guide uses for simulator internals.

| Term | Meaning here |
|---|---|
| **event queue** | the priority queue of future moments the core must handle: arrivals, wakes, timer ticks, slice expiries, departs. The main loop pops the earliest, always |
| **decision point** | any moment the scheduler is consulted: a task arrived/woke, the running task blocked/exited/departed, or its slice expired. Between decision points, nothing to decide |
| **runnable / blocked / running** | the three task states: wants the lane / waiting on something (WAIT, SLEEP, TIMER, a fork slot) / currently holding the lane |
| **ready set** | the runnable tasks the scheduler chooses among (in MLFQ, structured as the queues) |
| **task VM** | the tiny per-task interpreter stepping through its program; a coroutine in spirit — it advances until the program blocks or ends |
| **remaining demand** | the unconsumed portion of a preempted RUN; must be conserved exactly across preemptions |
| **slice expiry** | the scheduled future event "if this task still holds the lane at t, preempt it"; cancelled if the task blocks first |
| **backlog (of a TIMER)** | grid ticks that passed while the task couldn't consume them; each completes a TIMER instantly until the task catches up |
| **tie-break rule** | your written, deterministic answer to "two events at the same microsecond — who first?" (open question 3) |
| **golden trace** | a committed known-good trace for a fixture workload; tests diff current output against it byte-for-byte — the cheapest strong regression net for a deterministic simulator |
| **idle** | the lane with no runnable task; virtual time jumps straight to the next event (never "spin") |

---

*The binding fine print behind sections 2–4 lives in `docs/simulator/interpretation-contract.md` (semantics) and `dataset/schema/workload.schema.json` (shapes); this guide restates them completely, but if a discrepancy ever slips in, those two win — and tell 인지오, since a discrepancy is a bug in this guide.*
