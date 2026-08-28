# Background Guide — everything to know before building the simulator
> Status: draft · Created 2026-08-28 · Updated 2026-08-28

This is the first half of the simulator onboarding guide, written for a reader who has skimmed the research proposal once and has general CS knowledge but no OS background. It is deliberately self-contained: it re-explains everything it needs, in plain language, so you can read it top to bottom without opening another document. The second half — what the simulator itself must do — is `simulator-guide.md`, which assumes you've read this one.

---

## 1. The idea, in one story

Imagine two computers, side by side, running a game.

On the first computer, the user also started a big game download — they *want* it to finish, they're waiting for it. On the second computer, an antivirus scan kicked in on its own schedule — nobody asked for it, nobody is waiting.

To the operating system, these two machines look **identical**. Both have a game in the foreground and some heavy background work hammering the disk and CPU. Every measurement the OS can take — CPU usage, I/O rates, sleep patterns — comes out the same. And yet the *right thing to do* is opposite: the wanted download should be throttled but kept moving; the unwanted scan can be shoved out of the way entirely.

The difference between those two machines is not in any number. It's in the **meaning** of what's running — and the only place that meaning shows up is in the process *names*. A human glancing at the process list ("oh, that's Steam downloading" vs "oh, that's the virus scanner") knows instantly. The OS doesn't, because the OS has no idea what software *is for*.

Operating systems today patch over this with hand-written lists. Windows and macOS Game Mode ship with lists of known game executables. Linux scheduling classes wait for applications to politely declare "I am background work" (they rarely do, and when they do declare something, everyone claims to be important). Every such list is a human, at some point, writing down what software means — and every list is forever incomplete. Software nobody registered gets nothing.

**Our project replaces the list with inference.** A large language model already knows, from reading the internet, what Steam is, what `clamscan` is, what OBS does, that `cc1` is a compiler's guts and `tracker-miner-fs-3` is a file indexer. So: hand the LLM the list of running process names, let it work out "this machine is being used for gaming, and the background work is wanted," and turn that judgment into scheduler configuration.

## 2. The one constraint that shapes the whole design

A scheduler decides "who gets the CPU next" hundreds of thousands of times per second, in microseconds. An LLM takes hundreds of milliseconds to answer anything. That's a gap of five to six orders of magnitude, and it will never close.

So the LLM **never** makes scheduling decisions. The design is two loops:

```text
   SLOW LOOP (runs once in a while, when the process mix changes)
     process names  ──▶  LLM  ──▶  "this is a gaming session,
                                    background work is wanted"
                                        │
                                        ▼   (as configuration)
   FAST LOOP (runs constantly, microseconds per decision)
     an ordinary scheduler, running whatever configuration
     the slow loop last handed it
```

Think of a restaurant: the LLM is the manager who occasionally walks through the dining room, reads the situation ("big party arriving, one impatient regular at table 3"), and adjusts the service policy. The waiters — the actual scheduler — keep making every individual table-by-table decision at full speed, just under the current policy. The manager never carries a plate.

A nice safety property falls out of this: if the LLM is slow, wrong, or dead, the fast loop keeps running its last (or default) configuration. The worst case is a slightly mistuned ordinary scheduler — never a broken system.

## 3. What exactly are we testing?

Here's the part that makes this an *experiment* rather than a demo, and it's the single most important thing to understand about the project.

Any "smart" scheduler can be split into two components:

- the **recognizer** — figures out *what situation the machine is in* ("gaming with a wanted download");
- the **executor** — given a situation, applies a configuration and schedules accordingly.

We keep the executor **absolutely identical** across all experiments and swap in different recognizers. Then any difference in the results is attributable to recognition quality alone, because nothing else changed. The recognizers we swap in form a ladder:

| Recognizer | What it does | Why it's in the ladder |
|---|---|---|
| `fixed` | no recognition at all — always the default configuration | the floor: what "no situation awareness" scores |
| `random` | picks a random situation | the control: what a *useless* recognizer scores |
| `whitelist` | matches known process names from a hardcoded list | **what real OSes do today** (Game Mode) — the baseline to beat |
| `llm_*` | asks the LLM (in three variants, given progressively more authority) | the thing under test |
| `oracle` | reads the true answer straight from the workload file | the ceiling: what *perfect* recognition scores |

The oracle deserves a beat of explanation, because it sounds like cheating. Every workload file in our dataset carries a hidden **ground truth**: a label saying what situation the file represents at every moment, written by whoever authored the file. The oracle recognizer just reads that label. It can't be wrong. That gives us the *ceiling*: the best any recognizer could possibly do on this executor. The interesting question is always "where between `random` and `oracle` does the LLM land, and does it clear `whitelist`?"

And before any LLM enters the picture, there's a cheap kill-check called **RQ0**: run just `random` and `oracle` first. If perfect recognition barely beats random guessing, then recognition quality doesn't matter on these workloads — the experiment is dead and no prompt engineering can revive it. That check needs no model, no API key, just the simulator. It's the first real experiment the simulator will run.

One more mindset note: **a negative result is a real result here.** "The LLM reads situations correctly but scheduling doesn't improve" is a publishable finding — it means the ordinary scheduler's behavioral heuristics were already good enough. We are set up so that honest failure is informative, not embarrassing.

## 4. What the simulator is (and isn't)

We do not run real processes. Nothing in this project executes a real game or a real compiler. Instead, the simulator **works the schedule out on paper**.

The classic picture: a bank with exactly one open counter and a line of customers. The counter serves one person at a time, so someone must repeatedly decide *who gets called next*. That decision rule is the scheduler. If you want to compare two decision rules, you can either staff a real bank for a day — or sit down with each customer's errand list and *write out the appointment book*: "9:00 customer A, 9:03 customer B, 9:05 back to A…". Same answer, no bank.

The simulator is the appointment-book approach:

- Each **task** (process) is a customer carrying a fully pre-written script: "need the counter for 4 ms, then step away for 20 ms, then need it for 2 ms…". The scripts come from the workload dataset and never change.
- The **scheduler** decides, at each decision point, which waiting customer holds the counter.
- The output is a **timetable**: which task held the CPU during which interval of time.

```text
  CPU  │ editor │   cc1    │ editor │      cc1      │ editor │
       └────────┴──────────┴────────┴───────────────┴────────┘
       0        3         11       12              25        26   (virtual ms)
```

Time in this world is **virtual**. The clock is just an integer (we count in microseconds). Nothing "waits" in real time — when the simulator knows nothing interesting happens between t=11 and t=12, it jumps the clock straight there. This is called **discrete-event simulation**: keep a queue of future events (task wakes up at t=X, time slice expires at t=Y), repeatedly pop the earliest one, update the world, repeat. A simulated hour finishes in seconds of real time, which is what makes running a large experiment matrix affordable.

All performance numbers are then *read off the timetable*, not measured with any stopwatch:

| Metric | How it's read off the timetable | Who cares |
|---|---|---|
| Response time | from a task's arrival to the first moment it holds the CPU | interactive apps — this is "does the UI feel laggy" |
| Turnaround time | from arrival to completion | batch work — "when did my compile finish" |
| Deadline miss rate | fraction of periodic jobs (frames) finishing after their due time | games, audio/video |
| P99 latency | the 99th-percentile completion time of periodic jobs — the *bad* frames | games; a good average with a bad tail still feels like stutter |
| Throughput | total CPU time delivered to batch work per unit time | compiles |
| Starvation | the longest stretch any task went without CPU at all | everyone — the safety check |

Because the scripts are fixed and the simulator has no randomness of its own (more on that below), two runs with the same workload and same scheduler produce **byte-identical** timetables. Perfect reproducibility is the reason we simulate instead of using a real machine, where thermal throttling and background noise would drown the effect we're measuring.

What simulation costs us, honestly: no cache effects (real context switches trash CPU caches; our timetable doesn't model that), one CPU lane only (no multi-core interactions), no real kernel overheads. The claim we can make is "the semantic signal carries usable information for scheduling" — a prerequisite for a real implementation, not a substitute for one.

## 5. The dataset: what the simulator eats

The simulator's entire input is a directory of **canonical workload files** — one JSON file per experiment scenario. Here's a real one, abbreviated (`c2-p1a`, "an editor plus an ML training run"):

```jsonc
{
  "meta": {
    "id": "c2-p1a",
    "derived_from": "dataset/timelines/coreset/c2-p1a.timeline.yaml@2aa49c7…",
    "sampled": { "seed": 201, "archetypes": "archetypes.yaml@99495a3…" }
  },

  "ground_truth": [
    { "t_start": 0,        "t_end": 60000000,  "mode": "dev",      "attributes": { "wanted": true } },
    { "t_start": 60000000, "t_end": 180000000, "mode": "ml-train", "attributes": { "wanted": true } }
  ],

  "events": [
    { "op": "arrive", "t": 0, "id": "editor", "name": "code", "depart": 180000000,
      "program": [
        { "op": "WAIT", "channel": "input:editor" },
        { "op": "RUN",  "us": 23439 },
        { "op": "WAIT", "channel": "input:editor" },
        { "op": "RUN",  "us": 253642 }
        // …hundreds more, all concrete numbers
      ] },
    { "op": "wake", "t": 2098333, "channel": "input:editor", "target": "editor" }
    // …hundreds more wakes: this is the "user typing"
  ]
}
```

Three blocks, three different audiences:

- **`meta`** — provenance. Where this file came from, which random seed produced it. Nobody's scheduler reads this; it exists so every number in the file can be traced back to its origin.
- **`ground_truth`** — the answer key, sealed in an envelope. A list of time intervals, each labeled with a **mode** (what the machine is being used for during that interval: `dev`, `ml-train`, `gaming`, `office`…) and **attributes** (independent extra facts, like `wanted: true` — "the background work here is something the user asked for"). Only the oracle recognizer and the grading code ever open this envelope. The simulator's scheduler never sees it; the LLM never sees it. All times are integer **microseconds** — `60000000` is the 60-second mark.
- **`events`** — the workload itself. This is what the simulator actually executes, and there are only two kinds of event, ever:
  - **`arrive`** — a task pops into existence, carrying its complete pre-written script (its `program`). The editor above arrives at t=0 and its script says: wait for a keystroke, compute for 23.4 ms, wait for the next keystroke, compute for 253.6 ms… Its `depart` field says the user closes it at t=180 s sharp.
  - **`wake`** — an external stimulus arrives: a keystroke, a network reply. The wake at t≈2.098 s above is "the user pressed a key in the editor." A task sitting in a `WAIT` gets unblocked by it. This is how "a human is using the machine" exists in the simulation without simulating a human.

Notice what this means: **everything the user does is pre-scripted** (arrivals, keystrokes, app-closings — pinned to absolute times), but **everything the scheduler influences is not** (when a compile finishes depends on how much CPU the scheduler gave it). That split is deliberate, and it's the whole trick: user behavior must not depend on the scheduler (else conditions wouldn't be comparable), while outcomes must (else there'd be nothing to measure).

Also notice each task has both an `id` and a `name`. The `id` (`editor`) is unique within the file — bookkeeping identity. The `name` (`code`) is the process name a recognizer would see in a process list — and names may repeat, or even lie: one dataset file deliberately contains a CPU-hogging task *named* `chrome`, to test what name-based recognition does with an impostor. Schedule by `id`; treat `name` as a label someone chose to wear.

### How these files get made (the two-minute version)

You won't build any of this — it's already built and frozen in `dataset/` — but knowing the shape helps:

1. **Archetypes** (`dataset/archetypes.yaml`): a library of *process behavior kinds* — "a code editor behaves like this," "a compiler child behaves like that" — with every number either taken from published literature or **measured by us in CI**: we actually ran editors, compilers, games and indexers on GitHub-Actions machines and recorded their burst patterns. Numbers in an archetype are *distributions* ("burst length is lognormal with these parameters"), not constants.
2. **Timelines** (`dataset/timelines/`): hand-authored scenario scripts — "an editor from 0–180 s; at 60 s a training run starts" — that say *who* is present *when* and what each moment should be labeled. Timelines reference archetypes by name and carry the ground-truth labels.
3. **wlc**, the workload compiler (`dataset/tools/wlc/`): takes a timeline + the archetype library + a seed, and **samples every distribution down to a concrete number**, producing the canonical JSON above. All randomness happens here, at compile time, recorded by the seed. That's why the simulator itself must contain no randomness: the dice were already rolled, the results are in the file, and rerunning anything reproduces it exactly.

The compiled set the simulator will run is the **coreset**: 24 workload files, each a scenario designed to probe one specific question — six "pure single situation" calibration files, six paired files that behave identically but mean different things (the story from section 1, made literal), transition arcs where the situation changes mid-run, files with deliberate distractions, files where familiar software is renamed to gibberish, and files designed to fool name-based recognition on purpose. A second, generated set (the **generalset**) comes much later.

One practical note: the compiled files live in `dataset/build/`, which is *not* checked into git (a manifest of hashes is). After cloning, run `make dataset` inside `dataset/` once to produce them.

## 6. The three of us

- **인지오** — owns the dataset above and the experiment infrastructure: the harness that runs conditions, computes metrics from traces, and produces plots; plus the contract documents that pin down formats.
- **인경민** — owns the simulator: everything in `simulator-guide.md`.
- **박이안** — owns recognition: the LLM prompts and model hosting, and also the `whitelist` baseline (the strongest competitor deliberately lives with the person arguing for the LLM).

The trees in the repo mirror this: `dataset/`, `simulator/`, `daemon/` (recognition), `harness/`. Ownership as listed is the current draft and can shift — the tree boundaries are what's stable.

## 7. The words we use

A reference table — skim now, return when a term bites you. These are the meanings *in this project*; some are narrower than general usage.

| Term | Meaning here |
|---|---|
| **task / process** | one scheduled entity in the simulator, carrying a program. We use the words interchangeably |
| **program** | a task's pre-written script: an ordered list of instructions (RUN, SLEEP, WAIT…) with all numbers concrete |
| **scheduler** | the decision rule answering "who holds the CPU lane until the next event" |
| **lane** | our word for the single simulated CPU. One lane, always — no multi-core |
| **virtual time** | the simulator's integer clock, in microseconds. Jumps event-to-event; no relation to real time |
| **discrete-event simulation (DES)** | the jump-between-events technique from section 4 |
| **preemption** | the scheduler forcibly pausing a running task mid-computation to run someone else |
| **time slice / quantum** | the maximum turn length a scheduler gives a task before reconsidering |
| **interactive task** | short bursts of CPU, long waits in between (an editor). Cares about response time |
| **batch task** | consumes all CPU it's given until done (a compiler). Cares about turnaround/throughput |
| **MLFQ** | Multi-Level Feedback Queue — the default scheduler family real OSes use. Several priority queues; burn your whole slice → demoted (probably batch), sleep before it ends → stay high (probably interactive); periodic boost so nothing starves |
| **EDF** | Earliest Deadline First — always run the task whose deadline is nearest. The right tool when tasks *have* deadlines (frames, audio buffers) |
| **lottery scheduling** | each task holds tickets; draw a ticket to pick who runs. Gives proportional shares ("background gets ~15%") |
| **FIFO** | run to completion in arrival order. Maximal throughput, no interactivity |
| **deadline** | for periodic work: each job must finish within its period or the frame drops / audio pops |
| **mode** | the ground-truth label for what the machine is being used for in an interval (`gaming`, `office`, `dev`…) |
| **attribute** | an orthogonal ground-truth fact alongside the mode, e.g. `wanted: true` |
| **segment** | one labeled interval of a workload: a stretch with a constant mode+attributes |
| **recognizer / executor** | the two halves from section 3: situation-reader / configuration-applier |
| **condition** | one rung of the experiment ladder (`fixed`, `random`, `whitelist`, `llm_*`, `oracle`) |
| **oracle** | the recognizer that reads ground truth — the ceiling |
| **workload (file)** | one canonical JSON file: meta + ground_truth + events |
| **canonical (format)** | the compiled, simulator-facing JSON format. The only thing the simulator ever reads |
| **timeline** | the human-authored source format that compiles *into* canonical. The simulator never reads these |
| **archetype** | a reusable process-behavior template in the library, with sourced distributions |
| **wlc** | the workload compiler: timeline + archetypes + seed → canonical file |
| **seed** | the recorded RNG seed used at compile time; same seed ⇒ byte-identical file |
| **coreset** | the 24 hand-designed workloads (in `-single`, the lane-scaled variant we run) |
| **generalset** | the future generated naturalistic set. Not built yet |
| **channel** | a named mailbox a task can WAIT on; wakes are addressed to channels |
| **spawn table** | a pre-written list of children an orchestrator task (like `make`) creates at run time via FORK |
| **trace** | the simulator's output: the timetable plus everything that happened, from which all metrics are computed |

---

*Next: `simulator-guide.md` — what the simulator must do, in what order to build it, and which decisions are yours.*
