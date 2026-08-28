# Simulator Guide — what to build, what's fixed, what's yours
> Status: draft · Created 2026-08-28 · Updated 2026-08-28

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

Note what is *not* in the picture: no daemon, no LLM, no network — the simulator is a pure function `(run file, config schedule) → trace`, and it neither knows nor cares whether a schedule came from the oracle, a whitelist, or a model. That ignorance is a design requirement, not an accident: it's what makes experimental conditions comparable. A related question that came up and is worth answering here: *in a real deployment the LLM runs on the same machine — shouldn't its inference occupy the lane, like a kernel operation?* No, and deliberately: the simulated machine contains only the workload's tasks, and recognition cost is modeled purely as **latency** (config entries take effect late by the measured inference time), never as lane occupancy. If inference consumed simulated CPU, each condition would face a *different* workload (the LLM conditions would carry extra load the oracle doesn't), which would destroy the controlled comparison — the whole experiment rests on every condition facing byte-identical demand. The CPU cost of local inference is real, but it's a deployment concern reported in the paper's cost accounting, not something the lane models.

## 2. The non-negotiables

Everything in this section is contract, not preference.

1. **Two inputs, nothing else.** A workload file and a **config schedule** from the daemon. The simulator never reads timelines, never reads `archetypes.yaml`, never sees an archetype name, and never talks to a daemon or a model. Parsing the workload file is the simulator's own job, by design: the dataset tree ships raw canonical files (`dataset/build/…/*.workload.json`) and knows nothing about its consumers — your loader extracts what the simulator is entitled to (`events` and `meta.id`; this extracted slice is what we call the **run file**) and discards the rest. Validation reference for event shapes: `dataset/schema/workload.schema.json`.
2. **One lane.** Exactly one simulated CPU. The scheduler answers one question: *who holds the lane until the next event*.
3. **Integer microseconds.** All times and durations are integer µs. No floats in time arithmetic, ever — floats drift, and drift breaks reproducibility.
4. **Zero runtime randomness.** The simulator contains no RNG. Same run file + same config schedule ⇒ **byte-identical trace**. (When lottery scheduling arrives later, its draws will come from a seeded PRNG whose seed is part of the configuration — still deterministic.) This property should be a test you run constantly, not a hope.
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
  "depart": 180000000,          // present IFF the task is segment-bound
  "program": [ /* the task's full script — instructions, §4 */ ],
  "spawn_table": [ /* children, present iff program contains FORK */ ],
  "fork_cap": 8                 // parallelism cap, only with spawn_table
}
```

Reading it in words: at time 0, a task exists; call it `editor` internally (`id`), it wears the process name `code` (`name` — bookkeeping label only, never scheduling input), the user will close it at exactly t = 180 s (`depart`), and here is its complete pre-written script (`program`) — the alternating waits and CPU bursts it will perform. The last two fields appear only on orchestrator tasks like `make`: the pre-written list of children it will launch, and how many may be alive at once.

**"An external stimulus arrives."** At its stated time, the outside world pokes a task — a keystroke lands, a network reply comes back:

```jsonc
{ "op": "wake", "t": 2098333, "channel": "input:editor", "target": "editor" }
```

In words: at t ≈ 2.098 s, something arrives on the mailbox named `input:editor`, and the task `editor` — if it's currently waiting on that mailbox — becomes runnable. These events are the simulated human's hands: hundreds of them per file, all pinned to absolute times so every experimental condition faces the identical user.

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
                  "params": { "num_queues": 3, "timeslice_us": 2000,
                              "timeslice_growth": 2, "boost_interval_us": 100000 },
                  "batch_bandwidth_cap": null },
      "provenance": "fallback" },
    { "t_us": 60450000,
      "config": { /* same shape, new values */ },
      "provenance": "unmodified" }
  ] }
```

The `config` payload's shape — the four algorithms, their exact `params` fields with ranges and defaults, and the `batch_bandwidth_cap` envelope field — is **frozen** in `../recognition-vocabulary.md` (the "Config schema" section). Build to it as law; if implementing it surfaces something awkward — a field that's hard to honor, a missing knob, a better shape — propose the edit rather than working around it. Frozen means "changed deliberately, together," not "untouchable."

How the simulator treats a schedule: each entry takes effect at its `t_us` — the natural implementation is one more event in the event queue, however you structure it. When it fires, the scheduler's settings are replaced; the running task is not disturbed beyond whatever the new policy implies at the next decision point; and a `config_applied` line (echoing `provenance`) goes to the trace. Requirements: the first entry is always at `t_us: 0` (reject a schedule without one); entries apply in order; the simulator never edits, reorders, or reinterprets a config — validation happened on the daemon side, and what arrives here is law. `condition` and `provenance` are opaque strings to you: log them, never branch on them.

## 4. The instruction set

Each task's `program` is a list of instructions the simulator steps through in order, advancing whenever the task holds the lane or a wait completes. Seven opcodes: six primitives plus one control-flow form. How you represent a task's position in its program is your design — the contract below fixes only what each instruction *means*.

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
Pure control flow — it generates no event of its own; the task simply cycles through the body's instructions. `count: N` repeats N times. `count: "unbounded"` repeats forever and is legal only for segment-bound tasks: the loop's true terminator is the task's pinned `depart`. (Bounded repetition with per-iteration variety is instead unrolled flat by the compiler — that's why editor programs are hundreds of literal WAIT/RUN pairs while a game frame loop is one compact unbounded LOOP.)

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
| 0 | arrive `editor` | its program starts, first instruction is WAIT → blocks instantly, consuming nothing | — |
| 0 | arrive `hog` | its program starts on RUN 20000 → runnable; lane is free, scheduler hands it over | hog |
| 10000 | wake `input:e` | editor's WAIT completes → editor runnable. Our scheduler doesn't preempt, so it merely joins the ready set | hog |
| 20000 | hog's RUN completes | next instruction EXIT → hog is gone. Scheduler picks the only runnable task | editor |
| 23000 | editor's RUN 3000 completes | next instruction WAIT → blocks. Nobody runnable | idle |
| 30000 | wake `input:e` | editor runnable again, takes the free lane | editor |
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

1. K priority queues. New/woken tasks enter the top queue.
2. Always run from the highest non-empty queue; round-robin within a queue.
3. A task that burns its whole slice at level i is demoted to i+1 (it's acting like batch work).
4. A task that blocks (WAIT/SLEEP/TIMER) before its slice ends stays at its level (it's acting interactive).
5. Every `boost_interval`, everything returns to the top queue — the anti-starvation reset.

To see the rules bite, replay the §4½ miniature under a 3-level MLFQ with a 2000 µs slice: both tasks start in Q0. The hog burns its full 2000 µs slice → demoted to Q1; burns another → Q2, the bottom, where it grinds on. At t=10000 the keystroke makes the editor runnable *in Q0*, which outranks Q2 — the editor preempts, runs its 3000 µs burst (blocking once at slice end and resuming, or spanning slices, depending on your within-queue rule — decide and document), then WAITs again, never demoted because it always blocks early. Keystroke response: ~0 ms instead of the 10 ms the naive scheduler produced. The hog resumes in Q2 and finishes around t=23000 instead of 20000. MLFQ *learned* which task was interactive from behavior alone, in two observations — that's the self-tuning quality every experimental condition stands on.

Its configuration is exactly the frozen MLFQ `params` from `../recognition-vocabulary.md` — `num_queues`, `timeslice_us`, `timeslice_growth` (level *i*'s slice = `timeslice_us · growth^i`), `boost_interval_us` — plus the envelope's `batch_bandwidth_cap`. That schema is frozen for all four algorithms; if implementing a field turns out awkward, propose the edit there rather than deviating quietly.

**Needed eventually, in whatever order suits you** — worth keeping in mind while shaping the interface, but nothing requires building them early: EDF, lottery, and FIFO policies; *mid-run config applications* from multi-entry schedules — in particular cross-algorithm switches, which means policy state handoff (what happens to MLFQ's queue positions when EDF takes over at t=60.45 s?) needs a story at some point; and per-class bandwidth caps, enforced by the executor regardless of what any config says. If the scheduler interface is narrow, each of these is an addition, not a rewrite.

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

Read the walkthrough's headline number straight off it: keystroke #1's latency is `run_start(20000) − ready(10000)` = 10 ms, while keystroke #2's is `30000 − 30000` = 0. The hog's turnaround is `task_end(20000) − task_arrive(0)` = 20 ms. (One deliberate simplification to notice: the editor's arrival-instant WAIT blocks it without any `ready`/`run_start` pair — whether an arriving task whose first instruction immediately blocks costs a zero-length occupancy is exactly the kind of semantic you'll pin down alongside §9's questions; whatever you decide, the trace makes the decision visible.)

Plus the two properties the freeze bakes in: **deterministic** (same inputs ⇒ byte-identical trace, `x_` lines included — trace stability is your reproducibility test) and **flat/streamable** (these files get big; gzip on disk is fine). Frozen is not final-forever: if emitting some event turns out awkward mid-implementation, or a field you need is missing, propose the change in `data-contracts.md` — the format bends deliberately, together, not silently per-tree.

## 7. The first integration gate, and a suggested path to it

The one fixed goalpost the project needs from the simulator first: **one workload runs end-to-end and produces reproducible results.** That moment matters beyond your tree — it's the first time the dataset, the contract, and the simulator prove they agree, and the RQ0 experiment (the project's first real measurement) becomes possible shortly after it. What "reproducible end-to-end" means concretely:

1. A real coreset workload loads (`dataset/build/coreset-single/c1-office.workload.json`, or any C1 file — they're the simplest: one segment, modest task counts).
2. It runs under a hand-written one-entry config schedule — the boot default, MLFQ at t = 0. (Multi-entry schedules and cross-algorithm switches only matter once more than one policy exists; nothing about the first gate needs them.)
3. It emits a trace; run twice, the traces are byte-identical.
4. The trace passes sanity checks: total delivered CPU ≤ elapsed virtual time; every completed task's RUN demand fully delivered; segment-bound tasks gone at their departs; no event processed out of time order.

**Everything past that goalpost — the working order, the intermediate steps, what to build first — is entirely your call.** For whatever it's worth, one path that would work: clock + event queue first with hand-written fake tasks; the instructions one at a time (RUN/SLEEP → WAIT/WAKE → TIMER → LOOP → FORK/EXIT), each with a tiny fixture; the loader against real coreset files; MLFQ last (a trivial run-until-block stub is enough scheduler while building everything else). Take it, reorder it, or ignore it.

If you want harder targets after the gate: `c1-compile.workload.json` exercises FORK/spawn-table/fork_cap hard (`make` + 100 `cc1` children at cap 8), and `c1-gaming` is the stress test (TIMER chains, a 16-stage WAKE brigade, hundreds of sleeper tasks).

## 8. Yours to decide

Entirely your call, inside `simulator/`:

- **Language.** The proposal drafts C++ (reasoning: logic could port to `sched_ext` later). If you have a strong preference otherwise, raise it — it's a draft, not a verdict.
- Internal architecture and data structures — how the event queue, task state, and program-stepping are represented; file layout; naming.
- Build system — your tree owns its own Makefile (or CMake, or cargo…); nothing at repo root constrains you.
- Testing approach and framework. (The dataset tree solved reproducibility-testing with golden-hash manifests; steal the idea if it fits.)
- A `simulator/README.md` in the spirit of `dataset/README.md` — layout, commands, rules of your tree — once there's something to describe.

## 9. Questions the contract doesn't answer (yet)

These are real ambiguities you will hit while implementing — none has a decided answer today, and this guide deliberately doesn't invent one. Each entry explains the situation, why it matters, and what the candidate answers are. When you hit one, decide it together with 인지오 and get the decision recorded, because these tend to become contract lines. Running the whole list to ground early — even before writing code — would make a good first working session.

### 9.1 A wake with no waiter

The contract says a `WAIT(channel)` blocks until a wake arrives on that channel. But what if the *wake arrives first*? Concretely: the editor is mid-RUN, chewing on its previous burst, when the next keystroke's `wake` event fires — the editor isn't waiting on anything right now. Is that keystroke **remembered** (the editor's next WAIT completes instantly, like a mailbox holding a letter), or **lost** (a wake only means something if someone is already waiting)? And if remembered, does *depth* matter — if three keystrokes pile up during one long burst, do the next three WAITs all complete instantly, or do the three collapse into one pending flag? The choice changes how much demand the interactive tasks actually express under load, so it isn't cosmetic: a lost keystroke means less work for a starved editor, which softens exactly the signal the experiment measures. (The mailbox-with-depth reading is probably the realistic one, but it should be decided, not assumed.)

### 9.2 TIMER's t₀

A TIMER's tick grid is t₀ + k·P — but the contract never says what **t₀** is. The candidates: the task's arrival time (each periodic task runs its own grid, anchored to when it appeared), the moment the task first *executes* a TIMER instruction (subtly later than arrival if instructions precede it), or global time zero (all periodic tasks share one universal grid). For tasks that arrive at t = 0, all three coincide — which is why the compiled coreset doesn't force the answer — but a periodic task arriving mid-run behaves differently under each. The choice also decides whether two 60 fps tasks tick in lockstep or staggered, which changes contention patterns. Pick the reading, confirm it against how the compiled files are authored, and pin it.

### 9.3 Simultaneous events

Two events carry the same integer microsecond — a wake and a depart at t = 60000000, say, or two arrivals at t = 0 (every C1 file opens with several). Which is processed first? Any policy is fine — file order, a fixed priority by event kind, id order as a final tie-break — but it must be **deterministic and written down**, because the trace-stability guarantee (non-negotiable 4) dies the moment tie-breaking depends on hash order, pointer values, or anything else that varies between runs. This question quietly underlies 9.5 too.

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
| **config-application event** | the event-queue entry created for each config-schedule row; when it fires, the scheduler's settings are replaced and `config_applied` is traced |
| **backlog (of a TIMER)** | grid ticks that passed while the task couldn't consume them; each completes a TIMER instantly until the task catches up |
| **tie-break rule** | your written, deterministic answer to "two events at the same microsecond — who first?" (§9.3) |
| **golden trace** | a committed known-good trace for a fixture workload; tests diff current output against it byte-for-byte — the cheapest strong regression net for a deterministic simulator |
| **idle** | the lane with no runnable task; virtual time jumps straight to the next event (never "spin") |

## 11. A question worth keeping — "shouldn't LLM inference occupy the lane?"

Asked by 경민, and good enough to record with its answer. In a real deployment the daemon runs on the same machine, so wouldn't calling the LLM be something like a kernel operation — taking over the CPU between tasks while it thinks?

**No — and by design, not by oversight.** The simulated machine contains only the workload's tasks; recognition cost enters the experiment purely as **latency** (each config-schedule entry is stamped late by the measured inference time), never as lane occupancy. The reason is the experiment's foundation: every condition must face **byte-identical demand**. If inference burned simulated CPU, the LLM conditions would carry extra load that the oracle, whitelist, and fixed conditions don't — and any measured difference would be part recognition quality, part self-inflicted overhead, inseparably. The real CPU cost of local inference is acknowledged where it belongs: in the paper's deployment cost accounting (and in practice a deployed daemon would run on efficiency cores or an NPU/GPU, off the contended path). So if you ever find yourself tempted to model the daemon as a task — don't; that would be the experiment measuring itself.

---

*The binding fine print behind sections 2–4 lives in `docs/simulator/interpretation-contract.md` (semantics) and `dataset/schema/workload.schema.json` (shapes); this guide restates them completely, but if a discrepancy ever slips in, those two win — and tell 인지오, since a discrepancy is a bug in this guide.*
