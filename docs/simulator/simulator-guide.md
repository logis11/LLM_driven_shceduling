# Simulator Guide — what to build, what's fixed, what's yours
> Status: normative · Created 2026-08-28 · Updated 2026-10-17

The second half of the simulator builder's onboarding (read `../background-guide.md` first — this one assumes it). It's a spec, but a deliberately breathing one: the **contract surface** (input format, execution semantics, determinism, output obligations) is fixed and stated here in full; the **inside of the machine** (language details, data structures, code layout, testing) is yours. Fixed things say "must." Everything else is a suggestion you may overrule in your own tree.

---

## 1. The machine at a glance

```text
   run file (workload events,          config schedule (from the daemon:
   answer key stripped)                [{t, config, provenance}, …])
            │                                   │
            └────────────┬──────────────────────┘
                         ▼
                 ┌──────────────┐
                 │   loader     │  parse + validate both inputs
                 └──────┬───────┘
                        ▼
   ┌───────────────────────────────┐
   │   discrete-event core         │   virtual clock (integer µs)
   │                               │   event queue (arrivals, wakes,
   │   live tasks, each advancing  │    timers, slice expiries, departs,
   │   through its program         │    config applications)
   │            ▲                  │
   │            │ "who runs now?"  │
   │      ┌─────┴─────┐            │
   │      │ scheduler │  ◀── swappable policy (MLFQ first),
   │      └───────────┘      configured by the schedule entries
   └──────────────┬────────────────┘
                  ▼
              trace file      →  the harness reads this and computes metrics
```

Four responsibilities: a **loader**, a **DES core** that advances each live task through its program, a **scheduler** behind a narrow interface, and a **trace writer**. How you structure any of that internally — how task state is represented, how programs are stepped, what the main loop looks like — is entirely your design; the diagram names responsibilities, not modules.

Note what is *not* in the picture: no daemon, no LLM, no network — the simulator is a pure function `(run file, config schedule) → trace`, and it neither knows nor cares whether a schedule came from the oracle, a name table (`shipped_catalogue`, `strongest_name_table`), or a model. That ignorance is a design requirement, not an accident: it's what makes experimental conditions comparable. A related question that came up and is worth answering here: *in a real deployment the LLM runs on the same machine — shouldn't its inference occupy the lane, like a kernel operation?* No, and deliberately: the simulated machine contains only the workload's tasks, and recognition cost is modeled purely as **latency** (config entries take effect late by the measured inference time), never as lane occupancy. If inference consumed simulated CPU, each condition would face a *different* workload (the LLM conditions would carry extra load the oracle doesn't), which would destroy the controlled comparison — the whole experiment rests on every condition facing byte-identical demand. The CPU cost of local inference is real, but it's a deployment concern reported in the paper's cost accounting, not something the lane models.

## 2. The non-negotiables

Everything in this section is contract, not preference.

1. **Two inputs, nothing else.** A workload file and a **config schedule** from the daemon. The simulator never reads timelines, never reads `archetypes.yaml`, never sees an archetype name, and never talks to a daemon or a model. Parsing the workload file is the simulator's own job, by design: the dataset tree ships raw canonical files (`dataset/build/…/*.workload.json`) and knows nothing about its consumers — your loader extracts what the simulator is entitled to (`events` and `meta.id`; this extracted slice is what we call the **run file**) and discards the rest. Validation reference for event shapes: `dataset/schema/workload.schema.json`.
2. **One lane.** Exactly one simulated CPU. The scheduler answers one question: *who holds the lane until the next event*.
3. **Integer microseconds.** All times and durations are integer µs. No floats in time arithmetic, ever — floats drift, and drift breaks reproducibility.
4. **Zero runtime randomness.** The simulator contains no RNG. Same run file + same config schedule ⇒ **byte-identical trace**. (Lottery scheduling's draws come from a PRNG the simulator seeds once per run from the workload id — not a config field — so it stays deterministic; `../recognition-vocabulary.md`, LOTTERY.) This property should be a test you run constantly, not a hope.
5. **The answer key never enters the building.** The workload file's `ground_truth` block (and `meta` beyond the id) must die at your loader's parse boundary — no simulator data structure holds it, so no scheduler code could ever branch on it. Enforce with structure, not discipline.
6. **Names are labels, ids are identity.** All internal bookkeeping keys on `id` (unique per file, linter-enforced). `name` is what the recognizer sees on the daemon side; names can repeat and can lie. Nothing in scheduling may branch on `name`.
7. **The timing principle.** Times pinned in the file (arrivals, wakes, departs) happen at exactly those times no matter what the scheduler does. Times *not* in the file (when a finite task finishes, when a forked child starts) emerge from scheduling. Never "helpfully" pin an emergent time or delay a pinned one.

## 3. The two inputs, explained properly

One run of the simulator plays **one workload** under **one sequence of scheduler settings**. Those are the two inputs, and they answer two different questions: the workload answers *"what happens on this machine?"* — every task that will exist, every keystroke that will arrive, all pre-scripted; the config schedule answers *"how should the scheduler behave, and from when?"* — the settings some recognizer decided on, finished ahead of time. The simulator's job is to combine them: play the scripted workload out while obeying whichever settings are in force at each moment, and write down what happened.

### Input 1 — the workload's events

Open any file in `dataset/build/coreset-single/` and look at its `events` key. It is one flat list, sorted by time, and every entry in it is one of exactly **two kinds of happening**:

**"A task comes into existence."** At its stated time, a new task appears, carrying everything the simulator will ever need to know about it — there is no second lookup anywhere:

```jsonc
{ "op": "arrive", "t": 0, "id": "editor", "name": "code",
  "declared_class": "normal",   // the class the program declares: "normal" or "idle"
  "depart": 180000000,          // present IFF the task is segment-bound
  "program": [ /* the task's full script — instructions, §4 */ ],
  "spawn_table": [ /* children, present iff program contains FORK */ ],
  "fork_cap": 8                 // parallelism cap, only with spawn_table
}
```

Reading it in words: at time 0, a task exists; call it `editor` internally (`id`), it wears the process name `code` (`name` — bookkeeping label only, never scheduling input), the user will close it at exactly t = 180 s (`depart`), and here is its complete pre-written script (`program`) — the alternating waits and CPU bursts it will perform. The last two fields appear only on orchestrator tasks like `make`: the pre-written list of children it will launch, and how many may be alive at once. `declared_class` is the scheduling class the program declares for itself — `normal`, or `idle` for a program that sets SCHED_IDLE on itself (e.g. the file indexer and the backup): an `idle` task runs only when no task of another class is runnable and is preempted at once when one wakes, under every algorithm, below whatever the configured policy decides (`../data-contracts.md` §4). Every task record carries it, each spawn-table entry included.

The illustration simplifies what the compiled files show: `c1-compile`'s `make` carries `fork_cap` 48 (§4, FORK), and a measured editor waits for its own timer components' wakes (`timer:<id>`) as well as for keystrokes — `c1-dev`'s editor gets 6,456 of those against 186 keystrokes.

**"An external stimulus arrives."** At its stated time, the outside world pokes a task — a keystroke lands, a network reply comes back:

```jsonc
{ "op": "wake", "t": 2098333, "channel": "input:editor", "target": "editor" }
```

In words: at t ≈ 2.098 s, something arrives on the mailbox named `input:editor`, and the task `editor` — if it's currently waiting on that mailbox — becomes runnable. Wakes on `input:<id>` are the simulated human's hands; most wake events, though, are a measured program's own timer-component wakes on `timer:<id>`. All are pinned to absolute times, so every experimental condition faces the identical user and the identical program.

That's the entire input format: arrivals and wakes, nothing else. Which leaves one question — how does a task *end*? Three ways, and you can tell which applies from the arrive event alone:

| class | how you spot it | how it ends |
|---|---|---|
| segment-bound | has `depart` | at `depart`, sharp — the "user" closed the app. Remove it whatever it was doing |
| finite | top-level arrive, no `depart` | its program reaches `EXIT`; *when* that happens is a scheduling outcome |
| spawned | never in `events` — lives inside a parent's `spawn_table` | created at run time by the parent's `FORK`; ends via its own `EXIT` |

### Input 2 — the config schedule

The daemon's finished output for this workload under one experimental condition (full contract and rationale: `../data-contracts.md`). It is a short list of "at virtual time T, the scheduler's settings become C":

```jsonc
{ "workload_id": "c2-p1a",
  "condition": "llm_vocab",
  "schedule": [
    { "t_us": 0,
      "config": { "algorithm": "MLFQ",
                  "params": { "num_queues": 3, "timeslice_us": 10000,
                              "timeslice_growth": 2, "boost_interval_us": 100000 },
                  "batch_bandwidth_cap": null },
      "provenance": "fallback" },
    { "t_us": 60450000,
      "config": { /* same shape, new values */ },
      "provenance": "unmodified" }
  ] }
```

The `config` payload's shape — the four algorithms, their exact `params` fields with ranges and defaults, and the `batch_bandwidth_cap` envelope field — is **frozen** in `../recognition-vocabulary.md` (the "Config schema" section). Build to it as law; if implementing it surfaces something awkward — a field that's hard to honor, a missing knob, a better shape — propose the edit rather than working around it. Frozen means "changed deliberately, together," not "untouchable."

Three mechanics were fixed with the contract's freeze (2026-09-06; `../data-contracts.md` §7): the list is ordered — boot entry first, then by `t_us`, and same-time entries apply in list order with the last one in force (this happens at t = 0 for zero-latency conditions, whose first answer lands alongside the boot entry); every `config` must be valid under the schema, and a violation rejects the **whole file** — never repair or skip an entry, a malformed one is a daemon bug and silent repair would hide it from the provenance counts; entries at or after the workload's end are ignored (every file has one — the terminal telemetry snapshot). Where a schedule entry and a task event share a microsecond, the entry is processed first — your §9.3 tie-break rule.

How the simulator treats a schedule: each entry takes effect at its `t_us` — the natural implementation is one more event in the event queue, however you structure it — unless it is a switch that drains, or is stamped while one drains (next paragraph). When it fires, the scheduler's settings are replaced; the running task is not disturbed beyond whatever the new policy implies at the next decision point; and a `config_applied` line (echoing `provenance`) goes to the trace at the instant the entry applied. Requirements: the first entry is always at `t_us: 0` (reject a schedule without one); entries apply in order; the simulator never edits, reorders, or reinterprets a config — validation happened on the daemon side, and what arrives here is law. `condition` and `provenance` are opaque strings to you: log them, never branch on them.

A change of algorithm follows the algorithm-switch memo (`../memos/2026-09-08-algorithm-switch-semantics-for-the-simulator.md`), its rules confirmed with you on 2026-09-09 and in your simulator since 2026-10-10 (U1–U3, `simulator/memo/memo_261010.md` Part B). When a switch applies, the incoming algorithm takes the waiting tasks at once. A switch out of FIFO applies at its `t_us`, the running task freshly dispatched by the incoming algorithm; a switch out of MLFQ, EDF or LOTTERY applies the next time the lane is free — the running task's slice end, block, preemption, exit or depart, or at once when no task holds the lane — and entries stamped meanwhile wait behind it, so every index applies in order. A switch into MLFQ is a cold start: every task in the top queue, the boost timer restarting at the applied instant. An entry with the same algorithm is not a switch: queue levels are kept, and the running task finishes the slice it was granted, the new params governing from its next dispatch; under MLFQ the boost timer restarts at the applied instant, as on a switch into it (`simulator/src/sim.cpp:210`, `:597`). The harness's side of these rules is `../harness/metrics.md` §11 items 7–9.

## 4. The instruction set

Each task's `program` is a list of instructions the simulator steps through in order, advancing whenever the task holds the lane or a wait completes. Seven opcodes: six primitives plus one control-flow form. How you represent a task's position in its program is your design — the contract below fixes only what each instruction *means*.

### `{ "op": "RUN", "us": N }`
Consume N microseconds of *lane time*. This is CPU demand, not wall time: if the task gets preempted after 300 µs of a 1000 µs RUN, the remaining 700 µs demand survives and continues whenever the task next holds the lane. A RUN's wall-clock extent is exactly what the experiment measures — never treat it as a fixed interval.

A concrete arithmetic check for your implementation: task A executes `RUN 1000` starting at t=5000. At t=5300 the scheduler preempts it for 2000 µs of other work, then lets it back on. A's remaining demand at re-entry is 700 µs, so the RUN completes at t=8000. Total demand delivered: exactly 1000 µs. Wall-time extent: 3000 µs. If your simulator ever "loses" or "duplicates" demand across a preemption, every downstream metric silently corrupts — worth a dedicated unit test.

### `{ "op": "SLEEP", "us": N }`
Leave the lane voluntarily; become runnable again at `now + N`. Relative to whenever the sleep starts.

### `{ "op": "TIMER", "period_us": P }`
The metronome. Block until the next tick of this task's period grid — ticks at t₀, t₀+P, t₀+2P, … regardless of how late previous iterations ran (that's the difference from SLEEP: a SLEEP-loop drifts later and later under load; a TIMER doesn't, as a display-paced frame loop doesn't: a frame presented in Vulkan's FIFO mode waits for the next vertical blank, `vulkan`). Late ticks **accumulate as backlog**: if the task was stuck so long that two ticks passed, the next two TIMERs complete immediately — missed frames turn into pressure, not silence.

Worked example of the backlog rule, using the 60 fps grid (P = 16,667 µs, ticks at 0, 16667, 33334, 50001, …): a frame task finishes frame work and reaches its next TIMER at t=14000 — it blocks until the t=16667 tick. Fine so far. Now suppose a heavy stretch keeps the task off the CPU and it doesn't reach its TIMER again until t=40000. Two ticks (16667 and 33334… whichever it hadn't consumed yet) have passed unconsumed. The rule: those TIMERs complete *immediately*, one per loop iteration, so the task rattles off the overdue frames back-to-back, and only once it has caught up with the grid does a TIMER actually block again (until t=50001). The effect is that a starved periodic task piles up pressure and fights to catch up instead of quietly skipping frames, which would *reduce* CPU demand exactly when the scheduler misbehaves and mask the damage the experiment wants to see.

Backlog is a measurement choice, not a model of the programs the TIMER tasks stand for: none of them replays a late frame or callback. mpv drops late video frames by default and its audio output refills a drained buffer in one write (`mpv`); Chromium's fake audio output runs a late callback once and moves to the next on-time interval (`chromium`); a FIFO-presented frame takes the next vertical blank (`vulkan`); a fixed-timestep game loop replays its simulation steps, capped, but renders once per loop (`fiedler-gaffer04`). A starved TIMER task therefore spends more CPU, and misses more of its later jobs, than the program it stands for: the damage a configuration does to periodic work is overstated, not understated. (Reference ids: `../references.md`.)

In the compiled coreset, TIMER appears in shapes like the frame producer of the gaming files (`c1-gaming`'s chain head):

```jsonc
{ "op": "LOOP", "count": "unbounded", "body": [
    { "op": "TIMER", "period_us": 16667 },          // 60 fps grid
    { "op": "RUN",   "us": 631 },                   // the head's work this frame
    { "op": "WAKE",  "target": "game.wineserver" }  // hand the frame to the next stage
] }
```

### `{ "op": "WAIT", "channel": "…" }`
Block until a wake addressed to that channel arrives — either an exogenous `wake` event from the file, or a `WAKE` instruction executed by another task. This is how "editor waits for a keystroke" and "pipeline stage waits for its upstream" both work. No `wake` event or `WAKE` in a file targets an orchestrator, so nothing completes its `WAIT children:<id>` this way; its proposed rule is under FORK below.

### `{ "op": "WAKE", "target": "<task-id>" }`
Make the target task runnable (it's the sending half of task-to-task WAIT/WAKE edges). The gaming files use chains of these: a frame source ticks on a TIMER, RUNs, WAKEs the next stage, which RUNs and WAKEs the next — a 17-task bucket brigade (the head, `wineserver` and fifteen further members), once per frame. The target may be any task of the file, a spawn-table child included: a build's object job wires its six members to one another this way, each waking the next in the job's parent-child order, and `sh`, ending the job, wakes the other five to their EXITs.

### `{ "op": "FORK" }` and `{ "op": "EXIT" }`
`EXIT` terminates the executing task. `FORK` is for orchestrators like `make`: the arrive event carries a `spawn_table` — an ordered, fully pre-written list of children (their ids, names, and complete programs — in `c1-compile`, 17,448 entries: 2,908 object jobs of six processes each, `sh`, `gcc`, `cc1`, `as`, `fixdep`, `rm`) — and a `fork_cap` (48 there: the build's parallelism cap of 8, as in `make -j8`, times the six members of a job). Each `FORK` instruction creates the *next* unconsumed table entry as a live task. The cap is a wait-for-slot rule: at most `fork_cap` of this parent's children alive at once; a `FORK` while the cap is full blocks until a child exits. So *which* children exist and *what they do* is fixed in the file; *when* each one starts is an emergent, scheduler-dependent time — under a generous scheduler the build fans out fast, under a starved one it crawls. That divergence is signal, not a bug.

After its last FORK an orchestrator waits on `children:<id>`, its own id — `make` in `c1-compile` ends `WAIT children:build`, then `EXIT` — and no `WAKE` or `wake` event in the file targets it. Proposed (2026-10-16, `../data-contracts.md` §14; `interpretation-contract.md` §3 and §5), in force once 인경민 agrees: the executor completes an orchestrator's `WAIT children:<id>` when every child it spawned has ended, and without blocking, with a zero-wait `ready` line, when none is live at the WAIT.

Worked example of the cap, on an illustrative table of single-process children: `make` has `fork_cap: 8` and rattles off eight FORKs — children c1…c8 now exist and compete for the lane alongside everyone else. Make reaches its ninth FORK while all eight are still alive: the FORK **blocks**. At some later, scheduler-dependent moment c3 happens to finish and EXITs; a slot opens; make's blocked FORK completes and c9 is born. Note what this implies: c9's start time depends on how the scheduler treated c1–c8 — starve the compile family and the whole table drains slowly; favor it and the pipeline stays full. The total *work* is identical either way; the *shape in time* is not.

### `{ "op": "LOOP", "count": N | "unbounded", "body": [ … ] }`
Pure control flow — it generates no event of its own; the task simply cycles through the body's instructions. `count: N` repeats N times. `count: "unbounded"` repeats forever and is legal only for segment-bound tasks: the loop's true terminator is the task's pinned `depart`. (Bounded repetition with per-iteration variety is instead unrolled flat by the compiler — that's why editor programs are thousands of literal WAIT/RUN pairs — 6,642 in `c1-dev`'s editor — while a game frame loop is one compact unbounded LOOP.)

## 4½. A complete worked run, event by event

Nothing builds intuition for a discrete-event core like tracing one tiny run by hand. Here's a miniature workload — two tasks, two keystrokes, all times in µs:

```jsonc
"events": [
  { "op": "arrive", "t": 0, "id": "editor", "name": "code", "declared_class": "normal", "depart": 50000,
    "program": [ { "op": "WAIT", "channel": "input:editor" }, { "op": "RUN", "us": 3000 },
                 { "op": "WAIT", "channel": "input:editor" }, { "op": "RUN", "us": 2000 },
                 { "op": "WAIT", "channel": "input:editor" } ] },
  { "op": "arrive", "t": 0, "id": "hog", "name": "python3", "declared_class": "normal",
    "program": [ { "op": "RUN", "us": 20000 }, { "op": "EXIT" } ] },
  { "op": "wake", "t": 10000, "channel": "input:editor", "target": "editor" },
  { "op": "wake", "t": 30000, "channel": "input:editor", "target": "editor" }
]
```

The editor's two wakes meet three WAITs: no program runs out of instructions. A segment-bound program always ends blocked — on a WAIT, a TIMER or an unbounded LOOP — and its depart removes it; a wake-driven program's last WAIT is on its last wake's channel (in the compiled files, for the measured interactive entries usually their timer channel — in the core set and its sensitivity variants always). The hog, finite, ends with EXIT.

Run it under the dumbest legal scheduler — non-preemptive run-until-block ("whoever has the lane keeps it until they block or exit"):

| clock | event popped | what happens | lane |
|---|---|---|---|
| 0 | arrive `editor` | its program starts, first instruction is WAIT → blocks instantly, consuming nothing | — |
| 0 | arrive `hog` | its program starts on RUN 20000 → runnable; lane is free, scheduler hands it over | hog |
| 10000 | wake `input:editor` | editor's WAIT completes → editor runnable. Our scheduler doesn't preempt, so it merely joins the ready set | hog |
| 20000 | hog's RUN completes | next instruction EXIT → hog is gone. Scheduler picks the only runnable task | editor |
| 23000 | editor's RUN 3000 completes | next instruction WAIT → blocks. Nobody runnable | idle |
| 30000 | wake `input:editor` | editor runnable again, takes the free lane | editor |
| 32000 | editor's RUN 2000 completes | next instruction WAIT → blocks (no more wakes will come) | idle |
| 50000 | editor's `depart` | segment-bound task removed while blocked. Event queue empty → run over | — |

Now read the metrics off it, exactly as the harness will: the hog's turnaround is 20000 − 0 = 20 ms, and its response time is 0 (it ran immediately). The editor's response to keystroke #1 is 20000 − 10000 = **10 ms** — the keystroke sat unserved while the hog finished — versus effectively 0 for keystroke #2, which arrived to an idle lane. Total lane utilization: 25 ms of work in 50 ms of virtual time, 50%.

The punchline: replace the scheduler with one that preempts on wake, rerun the *identical file*, and keystroke #1's response drops from 10 ms to ~0 while the hog's turnaround stretches from 20 ms to 23 ms. Same input, different timetable, different numbers — that difference is the entire experiment, in miniature. (Also notice everything the walkthrough needed: a clock, an ordered future-event queue, each task's position in its program, a ready set, and a policy consulted at decision points. Those are the concepts the contract requires — how they become code is yours.)

## 5. The scheduler seat

The scheduler sits behind a narrow interface, because *swapping it is the entire experiment*. Shape it however feels right in your language; the obligations are:

- The core consults it only at decision points: a task arrives/wakes, the running task blocks/exits/departs, its time slice expires. Between events, nothing to decide.
- It picks who holds the lane next (or idle), and may set a preemption horizon (e.g. "slice of 4 ms").
- It never sees ground truth, names, or archetypes — only scheduling-relevant task state.
- Adding a second policy must not require touching the core.

Of the four policies, **MLFQ is the one the project needs soonest** — it's the default configuration and every experiment's floor — so it's the natural first pick, though the order you build things in is yours. Its concrete rules (the standard textbook construction; parameters are configuration, not constants in code):

1. K priority queues. A new task enters the top queue; a woken one returns to the level it blocked at (rule 4).
2. Always run from the highest non-empty queue; round-robin within a queue.
3. A task that burns its whole slice at level i is demoted to i+1 (it's acting like batch work).
4. A task that blocks (WAIT/SLEEP/TIMER) before its slice ends stays at its level (it's acting interactive).
5. Every `boost_interval`, everything returns to the top queue — the anti-starvation reset.

To see the rules bite, replay the §4½ miniature under a 3-level MLFQ with a 2000 µs slice (an illustration chosen to fit the miniature's 20 ms hog, not the boot default, whose slice is 10 ms): both tasks start in Q0. The hog burns its full 2000 µs slice → demoted to Q1; burns another → Q2, the bottom, where it grinds on. At t=10000 the keystroke makes the editor runnable *in Q0*, which outranks Q2 — the editor preempts, runs its 3000 µs burst (blocking once at slice end and resuming, or spanning slices, depending on your within-queue rule — decide and document), then WAITs again, never demoted because it always blocks early. Keystroke response: ~0 ms instead of the 10 ms the naive scheduler produced. The hog resumes in Q2 and finishes around t=23000 instead of 20000. MLFQ *learned* which task was interactive from behavior alone, in two observations — that's the self-tuning quality every experimental condition stands on.

Its configuration is exactly the frozen MLFQ `params` from `../recognition-vocabulary.md` — `num_queues`, `timeslice_us`, `timeslice_growth` (level *i*'s slice = `timeslice_us · growth^i`), `boost_interval_us` — plus the envelope's `batch_bandwidth_cap`. That schema is frozen for all four algorithms; if implementing a field turns out awkward, propose the edit there rather than deviating quietly.

**Needed eventually, in whatever order suits you** — worth keeping in mind while shaping the interface, but nothing requires building them early: EDF, lottery, and FIFO policies; *mid-run config applications* from multi-entry schedules — in particular cross-algorithm switches, whose policy state handoff (what happens to MLFQ's queue positions when EDF takes over at t=60.45 s?) the algorithm-switch memo settles (§3, after the schedule example) — all of these in your simulator, the switch rules since 2026-10-10; and the one cap the configuration sets, the batch class's `batch_bandwidth_cap` — the driver table row's under every condition but `llm_full` (unset, or 0.05–0.95, there) — which the executor is to enforce as a work-conserving ceiling on the batch class (`../memos/2026-09-09-batch-class-rule-for-the-simulator.md`; not yet implemented). The executor keeps no starvation window of its own: a run in which any task waits more than 30 s fails the harness's `starvation_floor` guard (`harness/guards/guard-spec.yaml`). If the scheduler interface is narrow, each of these is an addition, not a rewrite.

## 6. The output: a trace

The simulator's product is a **trace**: a machine-readable record from which every metric is computed *after the fact* by the harness. The simulator times nothing and computes no statistics; it writes down what happened.

The format is **frozen** in `../data-contracts.md` §9 (ratified 2026-08-28): JSONL, one `meta` header line, then seven event types — `task_arrive`, `task_end`, `ready`, `run_start`, `run_end`, `deadline`, `config_applied` — with `x_`-prefixed event names free for your own diagnostics (the harness ignores them). The full field lists, the metric-to-event mapping, and the rationale (notably why `ready` is its own event) live there; the shape of what you must be able to answer:

- when each task arrived (spawned children included — their start times are emergent), first ran, and ended (→ response time, turnaround);
- when each task *became runnable* and why (→ per-stimulus interaction latency, starvation);
- every interval of lane occupancy: who, from when, to when, and why it ended (→ throughput, context switches);
- for TIMER-driven work: each job's due time and outcome (→ deadline miss rate, P99 frame latency);
- each config-schedule entry taking effect, echoing its provenance (→ the "was the LLM actually driving?" accounting).

To make it concrete, here is the complete trace of the §4½ worked run — the two-task miniature under the non-preemptive run-until-block scheduler:

```jsonl
{"event":"meta", "workload_id":"mini", "condition":"fixed", "sim":"simulator@dev", "schedule_entries":1}
{"event":"config_applied", "t":0, "index":0, "algorithm":"MLFQ", "provenance":"fallback"}
{"event":"task_arrive", "t":0, "task":"editor", "source":"file"}
{"event":"task_arrive", "t":0, "task":"hog", "source":"file"}
{"event":"ready", "t":0, "task":"hog", "cause":"arrive"}
{"event":"run_start", "t":0, "task":"hog"}
{"event":"ready", "t":10000, "task":"editor", "cause":"wake"}
{"event":"run_end", "t":20000, "task":"hog", "reason":"exit"}
{"event":"task_end", "t":20000, "task":"hog", "reason":"exit"}
{"event":"run_start", "t":20000, "task":"editor"}
{"event":"run_end", "t":23000, "task":"editor", "reason":"block", "blocked_on":"wait"}
{"event":"ready", "t":30000, "task":"editor", "cause":"wake"}
{"event":"run_start", "t":30000, "task":"editor"}
{"event":"run_end", "t":32000, "task":"editor", "reason":"block", "blocked_on":"wait"}
{"event":"task_end", "t":50000, "task":"editor", "reason":"depart"}
```

Read the walkthrough's headline number straight off it: keystroke #1's latency is `run_start(20000) − ready(10000)` = 10 ms, while keystroke #2's is `30000 − 30000` = 0. The hog's turnaround is `task_end(20000) − task_arrive(0)` = 20 ms. Notice too what the editor's arrival leaves out: its first instruction is a WAIT, and it blocks at t = 0 with no `ready` line and no `run_start`, so it has no zero-length occupancy. That is your simulator's behaviour: `on_arrive` and `spawn` run a task's leading instructions in its arrival step, without the lane (`simulator/src/sim.cpp:734–738`, `:740–756`), and `step`'s WAIT blocks there unless a wake is already stored for it (`:686–695`). So a task whose first instruction is a WAIT (a LOOP's body counting, a spawned child included), with no wake stored for it, has its `task_arrive` line and no `ready` line at its arrival (your simulator adds only its own `x_block` diagnostic there), and its first `ready` line, if it is ever woken and the instructions after that WAIT reach a RUN without blocking or ending it, is the wake that completes that WAIT (`on_unblock`, `:800–806`). The harness's mock simulator blocks a WAIT-first task in its arrival step too (`../harness/metrics.md` §11 item 5).

Plus the two properties the freeze bakes in: **deterministic** (same inputs ⇒ byte-identical trace, `x_` lines included — trace stability is your reproducibility test) and **flat/streamable** (these files get big; gzip on disk is fine). Frozen is not final-forever: if emitting some event turns out awkward mid-implementation, or a field you need is missing, propose the change in `data-contracts.md` — the format bends deliberately, together, not silently per-tree.

## 7. The first integration gate, and a suggested path to it

The one fixed goalpost the project needs from the simulator first: **one workload runs end-to-end and produces reproducible results.** That moment matters beyond your tree — it's the first time the dataset, the contract, and the simulator prove they agree, and the RQ0 experiment (the project's first real measurement) becomes possible shortly after it. What "reproducible end-to-end" means concretely:

1. A real coreset workload loads (`dataset/build/coreset-single/c1-office.workload.json`, or any other C1 file but `c1-compile`, a harder target below — they're the simplest: one segment, modest task counts).
2. It runs under a hand-written one-entry config schedule — the boot default, MLFQ at t = 0. (Multi-entry schedules and cross-algorithm switches only matter once more than one policy exists; nothing about the first gate needs them.)
3. It emits a trace; run twice, the traces are byte-identical.
4. The trace passes sanity checks: total delivered CPU ≤ elapsed virtual time; every completed task's RUN demand fully delivered; segment-bound tasks gone at their departs; no event processed out of time order.

**Everything past that goalpost — the working order, the intermediate steps, what to build first — is entirely your call.** For whatever it's worth, one path that would work: clock + event queue first with hand-written fake tasks; the instructions one at a time (RUN/SLEEP → WAIT/WAKE → TIMER → LOOP → FORK/EXIT), each with a tiny fixture; the loader against real coreset files; MLFQ last (a trivial run-until-block stub is enough scheduler while building everything else). Take it, reorder it, or ignore it.

If you want harder targets after the gate: `c1-compile.workload.json` exercises FORK/spawn-table/fork_cap hard (`make` with 17,448 spawn-table entries — 2,908 object jobs of six members, which WAKE one another — at `fork_cap` 48), and `c1-gaming` exercises TIMER and WAKE chains (a TIMER-paced head driving a 17-task WAKE brigade, 18 tasks in all with the Steam client).

## 8. Yours to decide

Entirely your call, inside `simulator/`:

- **Language.** The proposal drafts C++ (reasoning: logic could port to `sched_ext` later). If you have a strong preference otherwise, raise it — it's a draft, not a verdict.
- Internal architecture and data structures — how the event queue, task state, and program-stepping are represented; file layout; naming.
- Build system — your tree owns its own Makefile (or CMake, or cargo…); nothing at repo root constrains you.
- Testing approach and framework. (The dataset tree solved reproducibility-testing with golden-hash manifests; steal the idea if it fits.)
- A `simulator/README.md` in the spirit of `dataset/README.md` — layout, commands, rules of your tree — once there's something to describe.

## 9. Questions the contract doesn't answer (yet)

These are real ambiguities you will hit while implementing, and this guide deliberately doesn't invent answers to them. Each entry explains the situation, why it matters, and what the candidate answers are — or, where one has been decided (§9.1–§9.3), the answer. When you hit one, decide it together with 인지오 and get the decision recorded, because these tend to become contract lines. Running the whole list to ground early — even before writing code — would make a good first working session.

### 9.1 A wake with no waiter — decided

What if the *wake arrives first* — the editor mid-RUN on its previous burst when the next keystroke's `wake` event fires? Decided: the wake is **remembered, with depth**. A wake that finds no waiter is held for the task, like a letter in a mailbox, so its next WAIT completes at once; three wakes that pile up during one long burst complete the next three WAITs (`../harness/metrics.md` §11 item 2, from the trace clarifications of `../memos/2026-09-07-trace-clarifications-for-the-simulator.md`; your simulator's mailbox, step M, does this). A lost or collapsed wake would mean less work for a starved editor, softening exactly the signal the experiment measures.

### 9.2 TIMER's t₀ — decided

A TIMER's tick grid is t₀ + k·P, and the contract's TIMER row doesn't define **t₀**. The candidates: the task's arrival time (each periodic task runs its own grid, anchored to when it appeared), the moment the task first *executes* a TIMER instruction (later than arrival if instructions precede it), or global time zero (all periodic tasks share one universal grid). Decided: t₀ is the task's **arrival** — a spawned child's, the FORK that creates it — on a busy lane as on an idle one. Two rules make the first-execution reading and the arrival one instant. Every program that carries a TIMER, spawn-table entries included, begins with it in execution order, a LOOP head's body counting; the dataset's canonical lint holds it (`dataset/tools/wlc/linter.py`, `lint_canonical`'s TIMER-first check). And your simulator executes a task's leading instructions in its arrival step, without waiting for the lane — `on_arrive` and `spawn` call `step()` at the arrival (`simulator/src/sim.cpp:734–737`, `:753`) — so the leading TIMER runs then, and the first TIMER execution, where your simulator anchors the grid (`:674`), is the arrival. Each periodic task runs its own grid: two 60 fps tasks that arrive at different instants tick staggered, not in lockstep.

### 9.3 Simultaneous events — decided

Two events carry the same integer microsecond — a wake and a depart at t = 60000000, say, or two arrivals at t = 0 (every C1 file opens with several). Which is processed first? Any policy is fine — file order, a fixed priority by event kind, id order as a final tie-break — but it must be **deterministic and written down**, because the trace-stability guarantee (non-negotiable 4) dies the moment tie-breaking depends on hash order, pointer values, or anything else that varies between runs. Decided: your simulator's rule D1 — config entries first, then every other event in the order it entered the event queue, so arrivals in file order (`simulator/src/sim.cpp`, the event order under D1; `simulator/steps/README.md`, D1). The harness assumes the same (`../harness/metrics.md` §11 item 3), and the RQ0 gate spec commits it as an executor assumption (its `executor-assumptions` statement, item 2), in place of the boot-default memo's proposal of a wake before a slice boundary (`../memos/2026-09-11-boot-default-from-ostep.md` §5, question 2). Your formal reply confirming it is asked in the declared-class memo (`../memos/2026-10-08-declared-scheduling-class.md` §4 item 4) and still outstanding; a differing answer becomes a harness changelog entry before any run. This rule quietly underlies 9.5 too.

### 9.4 Depart mid-anything

A segment-bound task's `depart` is sharp: the user closed the app, the task goes away. But the depart can land at an awkward instant — mid-RUN with demand still unconsumed, with backlogged TIMER ticks it never caught up on, or while it's the one currently holding the lane. The presumable rule is *remove immediately, discard all remainders* — but "presumable" isn't a spec: it needs confirming, and the trace's story for the truncated interval needs defining (does the cut-short RUN appear as a completed occupancy interval with a `departed` reason? does a pending deadline count as missed or as never-due?). The grading side cares, because C3's transition files depart whole casts of tasks at segment boundaries, and the metrics right at those boundaries shouldn't be implementation accidents.

### 9.5 Fork-slot wakeups

The `fork_cap` rule blocks a parent's FORK while `cap` children are alive. The fuzzy edges: two children EXIT at the same microsecond — does the parent's blocked FORK unblock once or is there a defined order with other same-instant events? A child exits at the *exact* instant the parent reaches its next FORK — does that FORK block at all? If several orchestrators are cap-blocked (not in the current coreset, but legal), who unblocks first? All of it interacts with 9.3's tie-break rule, and all of it is observable in `c1-compile`'s trace, so two implementations that disagree here produce different "correct" traces. Decide once, write it next to the tie-break rule.

## 10. Terms for the inside of the machine

The background guide's glossary covers the project vocabulary; these are the extra words this guide uses for simulator internals.

| Term | Meaning here |
|---|---|
| **event queue** | the priority queue of future moments the core must handle: arrivals, wakes, timer ticks, slice expiries, departs. The main loop pops the earliest, always |
| **decision point** | any moment the scheduler is consulted: a task arrived/woke, the running task blocked/exited/departed, or its slice expired. Between decision points, nothing to decide |
| **runnable / blocked / running** | the three task states: wants the lane / waiting on something (WAIT, SLEEP, TIMER, a fork slot) / currently holding the lane |
| **ready set** | the runnable tasks the scheduler chooses among (in MLFQ, structured as the queues) |
| **remaining demand** | the unconsumed portion of a preempted RUN; must be conserved exactly across preemptions |
| **slice expiry** | the scheduled future event "if this task still holds the lane at t, preempt it"; cancelled if the task blocks first |
| **config-application event** | the event-queue entry created for each config-schedule row; when it fires — or, for a switch that drains and every entry stamped behind it, once the lane is free (§3) — the scheduler's settings are replaced and `config_applied` is traced |
| **backlog (of a TIMER)** | grid ticks that passed while the task couldn't consume them; each completes a TIMER instantly until the task catches up |
| **tie-break rule** | your written, deterministic answer to "two events at the same microsecond — who first?" (§9.3): config entries first, then insertion order (your rule D1) |
| **golden trace** | a committed known-good trace for a fixture workload; tests diff current output against it byte-for-byte — the cheapest strong regression net for a deterministic simulator |
| **idle** | the lane with no runnable task; virtual time jumps straight to the next event (never "spin") |

## 11. A question worth keeping — "shouldn't LLM inference occupy the lane?"

Asked by 경민, and good enough to record with its answer. In a real deployment the daemon runs on the same machine, so wouldn't calling the LLM be something like a kernel operation — taking over the CPU between tasks while it thinks?

**No — and by design, not by oversight.** The simulated machine contains only the workload's tasks; recognition cost enters the experiment purely as **latency** (each config-schedule entry is stamped late by the measured inference time), never as lane occupancy. The reason is the experiment's foundation: every condition must face **byte-identical demand**. If inference burned simulated CPU, the LLM conditions would carry extra load that the oracle, name-table, and fixed conditions don't — and any measured difference would be part recognition quality, part self-inflicted overhead, inseparably. The real CPU cost of local inference is acknowledged where it belongs: in the paper's deployment cost accounting (and in practice a deployed daemon would run on efficiency cores or an NPU/GPU, off the contended path). So if you ever find yourself tempted to model the daemon as a task — don't; that would be the experiment measuring itself.

---

*The binding fine print behind sections 2–4 lives in `docs/simulator/interpretation-contract.md` (semantics) and `dataset/schema/workload.schema.json` (shapes); this guide restates them completely, but if a discrepancy ever slips in, those two win — and tell 인지오, since a discrepancy is a bug in this guide.*
