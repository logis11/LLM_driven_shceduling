# Background Guide — everything to know before building your part
> Status: normative · Created 2026-08-28 · Updated 2026-10-17

This is the shared first half of onboarding for both builders — the simulator (인경민) and the daemon (박이안) — written for a reader who has skimmed the research proposal once and has general CS knowledge but no OS background. It is deliberately self-contained: it re-explains everything it needs, in plain language, so you can read it top to bottom without opening another document. The component-specific second halves — what your program must do — are `simulator/simulator-guide.md` and `daemon/daemon-guide.md`, each of which assumes you've read this one.

---

## 1. The idea, in one story

Imagine two computers, side by side, running a game.

On the first computer, the user also started a big game install through Steam — they *want* it to finish, they're waiting for it. On the second computer, Ubuntu's unattended upgrade kicked in on its own and is installing updates — nobody started it just now, nobody is waiting.

To the operating system, these two machines look alike. Both have a game in the foreground and one heavy background job keeping a CPU 91–99 % busy beside it. The two jobs do differ in what the OS can measure: the download's work is cut into runs of about 163 µs between voluntary blocks, the upgrade's into runs of about 1.8 ms; the download is one process of 83–84 threads, the upgrade 916 short-lived processes; the download takes about 700 s of CPU, the upgrade 26 s; and the download runs three quarters of its CPU at nice 10, the upgrade 2.7 % of its at nice 19. None of those differences says which job the user wants. And yet the *right thing to do* is opposite: the wanted download should be throttled but kept moving — held to the batch class's cap, its waits judged by a 30 s starvation guard, though no executor rule guarantees it a floor; the unwanted upgrade can be deferred.

Whether the user wants the work is not in its behaviour, and its declared class does not settle it. The name, read with what is known of the software, carries it. A human glancing at the process list ("oh, that's Steam downloading" vs "oh, that's the system updating itself") knows instantly. The OS doesn't, because the OS has no idea what software *is for*.

Shipping systems today patch over this with hand-written lists and declarations. A Linux distribution, CachyOS, ships such a list enabled by default: ananicy-cpp with a community catalogue of process names, each mapped to a priority class. (Windows' and macOS's Game Mode are something else: they give the game in the foreground resources — on Windows by default for most games, on macOS when a game goes full screen — and neither documents how it recognises a game.) And there are declarations: on Linux a program's scheduling policy, nice value and I/O class are declared by the program itself, its installed unit or a wrapper, and on macOS a QoS class by the developer in code. Declaration is partial and fixed per program: of the 1 438 Debian unstable source packages that install a systemd service unit, 56 (3.9 %, a floor) declare any of them, 40 only lowering their priority and 16 only raising it (mostly latency-bound daemons); some background tools declare themselves (Tracker and Baloo set background classes on themselves, Déjà Dup wraps its backup in `chrt --idle 0`), others declare nothing (ClamAV, borg, restic). Every such list is a human, at some point, writing down what software means — and every list is forever incomplete. Software nobody registered gets nothing.

**Our project replaces the list with inference.** A large language model already knows, from reading the internet, what Steam is, what `unattended-upgr` is, what OBS does, that `cc1` is a compiler's guts and `tracker-miner-f` — the 15-character name the kernel shows for Tracker's `tracker-miner-fs-3` — is a file indexer. So: hand the LLM the list of running process names, let it work out "this machine is being used for gaming, and the background work is wanted," and turn that judgment into scheduler configuration.

## 2. The one constraint that shapes the whole design

A scheduler decides "who gets the CPU next" hundreds to thousands of times a second on each CPU, more under some loads — over the dataset's measured programs, 13 to 12 497 context switches a second, the median program phase 422, and a switch is only a lower bound on picks — and each pick takes about half a microsecond on the dataset's machine. One answer from a local language model takes seconds: about 1–3 s for the `system` block on a consumer laptop, 14–36 s on four server vCPUs without a GPU. That's a gap of four to eight orders of magnitude across the settings measured, six to seven on a consumer laptop.

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

One important thing about *our experiment specifically*: in a deployed system these two loops would run live, side by side. In our experiment they don't even run at the same time. Because every workload is fully pre-scripted (more on that in section 5), the slow loop can be run **entirely in advance**: the daemon reads what a recognizer would have seen, does all its recognition work offline, and writes down a finished *schedule* of configurations — "at t = 0 use these settings; from t = 60.45 s use those." The simulator then runs the fast loop alone, consuming that schedule as one of its inputs. The two programs never talk to each other; they only pass files. This buys enormous simplicity (each side can be built and tested completely independently) and costs nothing in fidelity, because everything the live loop would have known is derivable in advance — including the LLM's slowness, which is honestly preserved by stamping each configuration to take effect *late* by the measured recognition latency.

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
| `shipped_catalogue` | matches process names against the catalogue CachyOS installs and enables with ananicy-cpp (`ananicy-rules` at `03ef03fb`), keyed by each process's `argv[0]` basename, untruncated | **what a shipping Linux distribution does by default** — the baseline for RQ2 (research question 2: does the reading beat what shipping systems do?) |
| `strongest_name_table` | matches process names against a rule list in the catalogue's design covering the software the dataset presents as known | the name table at its best — **the baseline whose defeat is the paper's claim** |
| `llm_*` | asks the LLM (in three variants, given progressively more authority) | the thing under test |
| `oracle` | reads the true answer straight from the workload file | the ceiling: what *perfect* recognition scores |

The oracle deserves a beat of explanation, because it sounds like cheating. Every workload file in our dataset carries a hidden **ground truth**: a label saying what situation the file represents at every moment, written by whoever authored the file. The oracle recognizer just reads that label. It can't be wrong. That gives us the *ceiling*: the best any recognizer could possibly do on this executor. The interesting question is always "where between `random` and `oracle` does the LLM land, and does it clear the two name tables, `shipped_catalogue` and `strongest_name_table`?"

What does a recognizer's answer actually look like? Two parts, fixed by the ratified vocabulary contract (`recognition-vocabulary.md` — the normative list). A **mode** — exactly one label from a closed menu of 16 saying what the machine is primarily being used for (`gaming`, `compile`, `dev`, `ml-train`, `browsing`, `office`, `idle`, …). And one **attribute** — an independent fact the mode label can't carry: `background_wanted: true|false`, "is the sustained background work here something the user asked for?" The two-part shape matters: "gaming", "gaming while a wanted download runs", and "gaming while an unwanted upgrade runs" are all `mode: gaming`, and only the attribute separates the last two — which is exactly the game-download-vs-unattended-upgrade story from section 1. That's why the design uses an orthogonal dimension instead of minting extra labels: the same wanted-vs-unwanted distinction recurs inside *every* mode, so it multiplies against the menu rather than growing it.

The executor's side of the bargain is a **configuration**: a small bundle of scheduler settings like "use the MLFQ algorithm with these queue parameters" or "switch to deadline-first scheduling and cap background work at 12% of the CPU." A fixed lookup table — the **driver table**, living on the daemon side — maps (mode, attributes) to configuration; the recognizer's only job is to land on the right row. (In the most permissive LLM variant the model proposes the configuration itself — that's variant C — but the table is the default path.)

And before any LLM enters the picture, there's a cheap kill-check called **RQ0**: run just `fixed`, `random` and `oracle` first. If perfect recognition barely beats random guessing, then recognition quality doesn't matter on these workloads — the experiment is dead and no prompt engineering can revive it. That check needs no model, no API key, just the simulator. It's the first real experiment the simulator will run.

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
| Starvation | the longest any task waited for the CPU while runnable (a run with a wait over 30 s fails the harness's starvation guard) | everyone — the safety check |

Let's read one metric off the little timetable above to make this concrete. Suppose the editor's keystroke arrived at t=2.5 ms, while `cc1` held the CPU, and the editor's next block starts at t=11. Then the editor's response time for that keystroke is 11 − 2.5 = 8.5 ms — the user waited 8.5 ms to see their character appear, because the scheduler chose to let the compiler finish its stretch first. A different scheduler might have preempted `cc1` at 2.5 ms and gotten the editor's response time near zero, at the cost of stretching the compile. Neither choice is free; the whole game is *which* trade-off each configuration makes, and whether knowing the situation lets you pick the right one.

### How the default scheduler thinks — MLFQ in one story

Since every experiment stands on MLFQ (Multi-Level Feedback Queue), it's worth seeing how it actually behaves. MLFQ maintains several priority queues and *learns* what each task is by watching it:

- A task that uses up its allotment at its level — a **time slice**'s worth of CPU, counted across every sleep along the way — looks like batch work: demote it one queue down (OSTEP's Rule 4).
- A task that gives up the CPU before using up its allotment, to wait for a keystroke or the disk, stays at its level — but the CPU it used still counts. Without that count a task could game the scheduler by blocking just before its slice ends (Rule 4 again).
- Every boost interval, everything returns to the top queue, so no task starves forever (Rule 5).

Watch it run on our two customers, as measured on the dataset's machine. The editor — LibreOffice Writer's `soffice.bin`, typed into by SWELL-KW's recorded keystrokes — runs a median 0.046 ms between blocks (a few milliseconds at the 99th percentile), so it gives up a 10 ms slice almost at once: it stays in the top queue, and the next keystroke gets served almost instantly. The compiler's `cc1` runs a median 368 ms of CPU from its start to its exit, unblocked in 99.4 % of object jobs, so it uses every slice: demoted; demoted again; and it settles at the bottom, where it runs in long uninterrupted stretches whenever nothing interactive is awake. Nobody told MLFQ which task was which — three or four observations were enough. That's why MLFQ is the honest baseline: it's *genuinely good*, and any claimed improvement has to beat this self-tuning behavior, not a strawman. It's also why the project's sharpest workloads are ones where behavior-watching cannot settle the question. A wanted training run and an unwanted indexer, each beside an editor, are two real jobs with opposite correct policies that differ in behaviour and in declared class: PyTorch's basic MNIST example on the CPU runs 69.49 s between voluntary blocks at nice 0, nearly all its CPU past any slice; Tracker's first index of a home runs 0.844–0.849 of its CPU past a 10 ms slice and sets `SCHED_IDLE`, nice 19 and the idle I/O class on itself. The pair tests what recognition adds over a baseline that already honours the indexer's declared class — on the indexer's side, nothing, so the gate experiment judges the training run's file and reports the indexer's — and only something that knows what the software *is* can tell whether the training run is wanted.

Because the scripts are fixed and the simulator has no randomness of its own (more on that below), two runs with the same workload and same scheduler produce **byte-identical** timetables. Perfect reproducibility is the reason we simulate instead of using a real machine, where thermal throttling and background noise would drown the effect we're measuring.

What simulation costs us, honestly: no cache effects (a real context switch can cost the cache state a program built — nothing visible while the data fit in the cache, up to hundreds of microseconds or more when they do not — and our timetable models none of it), one CPU lane only (no multi-core interactions), no real kernel overheads. The claim we can make is "the semantic signal carries usable information for scheduling" — a prerequisite for a real implementation, not a substitute for one.

## 5. The dataset: what everything eats

The whole experiment's raw material is a directory of **canonical workload files** — one JSON file per experiment scenario. Neither of your programs reads a whole file: each gets a derived *view* containing only its permitted slice (the simulator gets the events without the answer key; the daemon gets the names without the behavior — details in `data-contracts.md` and your own guide). But you should know what the master file contains. Here's a real one, abbreviated (`c2-p1a`, "an editor plus an ML training run"):

```jsonc
{
  "meta": {
    "id": "c2-p1a",
    // the hashes after @ are the source files' git blobs; they move with each file's bytes
    "derived_from": "dataset/timelines/coreset/c2-p1a.timeline.yaml@a0effee…",
    "sampled": { "seed": 201, "archetypes": "archetypes.yaml@c78d8cf…" }
  },

  "ground_truth": [
    { "t_start": 0,        "t_end": 60000000, "mode": "dev",      "attributes": { "background_wanted": true } },
    { "t_start": 60000000, "t_end": 99435000, "mode": "ml-train", "attributes": { "background_wanted": true } }
  ],

  "focus": [
    { "task": "editor", "t_start": 0, "t_end": 99435000 }
  ],

  "events": [
    { "op": "arrive", "t": 0, "id": "editor", "name": "code", "declared_class": "normal", "depart": 99435000,
      "program": [
        { "op": "WAIT", "channel": "timer:editor" },
        { "op": "RUN",  "us": 22 },
        { "op": "WAIT", "channel": "timer:editor" },
        { "op": "RUN",  "us": 250 }
        // …thousands more, all concrete numbers
      ] },
    { "op": "wake", "t": 2469, "channel": "timer:editor", "target": "editor" },
    { "op": "wake", "t": 2090485, "channel": "input:editor", "target": "editor" },
    // …11,344 wakes for the editor in all: 525 keystrokes, the rest its own timer wakes
    { "op": "arrive", "t": 60000000, "id": "hog", "name": "python", "declared_class": "normal",
      "program": [
        { "op": "RUN", "us": 192 },
        { "op": "SLEEP", "us": 378 }
        // …until its measured 1,389.885 s of CPU is spent, then EXIT: it runs on past the file's end
      ] }
  ]
}
```

Four blocks, each for a different audience:

- **`meta`** — provenance. Where this file came from, which random seed produced it. Nobody's scheduler reads this; it exists so every number in the file can be traced back to its origin.
- **`ground_truth`** — the answer key, sealed in an envelope. A list of time intervals, each labeled with a **mode** (what the machine is being used for during that interval: `dev`, `ml-train`, `gaming`, `office`…) and **attributes** (independent extra facts, like `background_wanted: true` — "the background work here is something the user asked for"). Only the oracle recognizer and the grading code ever open this envelope. The simulator's scheduler never sees it; the LLM never sees it. All times are integer **microseconds** — `60000000` is the 60-second mark.
- **`focus`** — which task holds the window focus, and when: pinned like an arrival, because it is something the user does. The daemon sees it (the recognizer is shown which process holds the focus); the simulator's scheduler does nothing with it and never gets it.
- **`events`** — the workload itself. This is what the simulator actually executes, and there are only two kinds of event, ever:
  - **`arrive`** — a task pops into existence, carrying its complete pre-written script (its `program`) and its declared class (`normal`, or `idle` for work that declares itself background, which runs only when nothing else wants the CPU). The editor above arrives at t=0 and its script says: wait for the next wake, compute for 22 µs, wait, compute for 250 µs… Its `depart` field says the user closes it at t = 99.435 s sharp. The training run has no `depart`: it runs until its measured work is done, past the file's end.
  - **`wake`** — an external stimulus arrives: a keystroke, a timer firing inside a program, a network reply. The wake at t ≈ 2.090 s above, on `input:editor`, is "the user pressed a key in the editor"; the one at 2.469 ms, on `timer:editor`, is one of the editor's own timer wakes, as measured. A task sitting in a `WAIT` gets unblocked by it. This is how "a human is using the machine" exists in the simulation without simulating a human.

Notice what this means: **everything the user does is pre-scripted** (arrivals, keystrokes, focus changes, app-closings — pinned to absolute times), but **everything the scheduler influences is not** (when a compile finishes depends on how much CPU the scheduler gave it). That split is deliberate, and it's the whole trick: user behavior must not depend on the scheduler (else conditions wouldn't be comparable), while outcomes must (else there'd be nothing to measure).

Also notice each task has both an `id` and a `name`. The `id` (`editor`) is unique within the file — bookkeeping identity. The `name` (`code`) is the process name a recognizer would see in a process list — and names may repeat, or even lie: one dataset file deliberately contains a CPU-hogging task *named* `chrome`, to test what name-based recognition does with an impostor. Schedule by `id`; treat `name` as a label someone chose to wear.

### How these files get made (the two-minute version)

You won't build any of this — it's already built and frozen in `dataset/` — but knowing the shape helps:

1. **Archetypes** (`dataset/archetypes.yaml`): a library of *process behavior kinds* — "a code editor behaves like this," "a compiler child behaves like that." 28 of its 29 entries are **measured by us in CI**: we actually ran editors, browsers, compilers, the Steam client, indexers, a training run and system jobs on GitHub-Actions machines and recorded how they run and block; the game's frame chain alone comes from published figures instead. Numbers in an archetype are *distributions* (mostly a measured quantile table to draw from), not constants.
2. **Timelines** (`dataset/timelines/`): scenario scripts — "an editor from 0 s; at 60 s a training run starts" — that say *who* is present *when* and what each moment should be labeled, written by hand or derived from one by a recipe. Timelines reference archetypes by name and carry the ground-truth labels.
3. **wlc**, the workload compiler (`dataset/tools/wlc/`): takes a timeline + the archetype library + a seed, and **samples every distribution down to a concrete number**, producing the canonical JSON above. All randomness happens here, at compile time, recorded by the seed. That's why the simulator itself must contain no randomness: the dice were already rolled, the results are in the file, and rerunning anything reproduces it exactly.

The compiled set the simulator will run is the **coreset**: 51 workload files, each a scenario designed to probe one specific question — sixteen "pure single situation" calibration files, one per mode; seven C2 files: three intent pairs — in `c2-p1a`/`c2-p1b` (a training run against a first index of the home) and `c2-p2a`/`c2-p2b` (a game download against an unattended upgrade, the story from section 1, made literal), a job the user wants against one nobody asked for, beside the same foreground, with opposite correct policies; in `c2-p3a`/`c2-p3b`, a video export against a scheduled backup, both wanted, the job's label differing in mode and in who initiated it — and `c2-p2a-idle`, which differs from `c2-p2a` in the download's declared class alone; transition arcs where the situation changes mid-run, files with deliberate distractions, files where familiar software is renamed to gibberish, files designed to fool name-based recognition on purpose, and, since Phase 7, one counterpart per mode in which the background work is something nobody asked for, so every row of the driver table has a matched pair. Beside it sits a generated layer of five sets, 1,562 files, built the same way: every ordered pair of modes as a transition, as a return (A → B → A) and with the other mode's programs — or a program outside every mode — arriving as distractors, the familiarity ladder over the sixteen modes, and a flap-stress set for the daemon's hold time. It is design, with no claim about how often desktops see these situations; a naturalistic set is in the backlog.

One limit of the files is worth knowing because it bends one pair in the hypothesis's favour: the task model carries no nice value. SteamCMD's download does 75 % of its CPU at nice 10 (over the 30 pooled repeats of `game-download`), yet in `c2-p2a` it competes with the game at full standing, so its interference with the game — and the headroom there — is overstated. The bounding pair `c2-p2a` / `c2-p2a-idle`, the same download under the declared class `idle`, brackets it. The upgrade's nice-19 work, 2.7 % of its CPU, is likewise carried at full standing.

One design property worth understanding, because it explains why some files look "too busy": a file of demand class **`oversubscribed`** — the seven C2 files, the three transition arcs and `c6-dual`, eleven of the 51 — is designed to hold contention. That's not sloppiness; it's the precondition for measuring anything there. If total demand were, say, 20% of the lane, every task would get all the CPU it wants no matter how dumb the scheduler is, all conditions would score identically, and the experiment would be blind. Scarcity is what forces the scheduler to make real choices, and real choices are what recognition quality can improve. The other 40 files are `calibration` files, not designed to hold contention. Demand is reported, not held: the build computes each file's demand, per file and per segment, into its manifest and never fails on it. Every job is bound whole as measured, so a file's demand follows from the measurement; holding it to a window would have meant bending measured lengths.

One practical note: the compiled files live in `dataset/build/`, which is *not* checked into git (the manifests of their hashes are). After cloning, run `make dataset variants generated PY=python3.12` inside `dataset/` once to produce them — the builds are made with Python 3.12.

## 6. The three of us

- **인지오** — owns the dataset above and the experiment infrastructure: the harness that runs conditions, computes metrics from traces, and produces plots; plus the contract documents that pin down formats.
- **인경민** — owns the simulator: everything in `simulator/simulator-guide.md`.
- **박이안** — owns the daemon: everything in `daemon/daemon-guide.md` — the LLM prompts and model hosting, and also the two name-table baselines, `shipped_catalogue` and `strongest_name_table` (the strongest competitor deliberately lives with the person arguing for the LLM).

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
| **MLFQ** | Multi-Level Feedback Queue — the textbook form of classifying tasks by their behaviour (OSTEP ch. 8; Corbató 1962) and this project's baseline, not a family every OS ships: Windows' priority boosts and decay are an MLFQ form, macOS's Clutch/Edge scheduler runs EDF over QoS buckets with usage-decayed priority per thread, and Linux's default, EEVDF, is a proportional-share algorithm. Several priority queues; use up your allotment at a level (a slice's worth of CPU, counted across sleeps) → demoted (probably batch); give up the CPU before using it up → stay at your level, the CPU still counted (probably interactive); every boost interval everything returns to the top queue, so nothing starves |
| **EDF** | Earliest Deadline First — always run the task whose deadline is nearest. The right tool when tasks *have* deadlines (frames, audio buffers) |
| **lottery scheduling** | each task holds tickets; draw a ticket to pick who runs. Gives shares proportional to tickets in expectation |
| **FIFO** | run to completion in arrival order. Maximal throughput, no interactivity |
| **deadline** | for periodic work: each job must finish within its period, or the frame is shown late or dropped, or the audio clicks — a late game frame is shown at the next vertical blank under FIFO presentation (Vulkan's `VK_PRESENT_MODE_FIFO_KHR`), a video sink drops a frame later than its allowed lateness, a late audio buffer is an xrun |
| **mode** | the ground-truth label for what the machine is being used for in an interval (`gaming`, `office`, `dev`…) |
| **attribute** | an orthogonal ground-truth fact alongside the mode; the one graded attribute is `background_wanted` |
| **segment** | one labeled interval of a workload: a stretch with a constant mode+attributes |
| **recognizer / executor** | the two halves from section 3: situation-reader / configuration-applier |
| **condition** | one rung of the experiment ladder (`fixed`, `random`, `shipped_catalogue`, `strongest_name_table`, `llm_*`, `oracle`) |
| **oracle** | the recognizer that reads ground truth — the ceiling |
| **workload (file)** | one canonical JSON file: meta + ground_truth + focus + events |
| **canonical (format)** | the compiled, simulator-facing JSON format. The only thing the simulator ever reads |
| **timeline** | the source format that compiles *into* canonical — written by hand, derived from another by a recipe, or emitted by the generator. The simulator never reads these |
| **archetype** | a reusable process-behavior template in the library, with sourced distributions |
| **wlc** | the workload compiler: timeline + archetypes + seed → canonical file |
| **seed** | the recorded RNG seed used at compile time; same seed ⇒ byte-identical file |
| **coreset** | the 51 core workload files, 23 written by hand and 28 derived from them by recipes (compiled in `single`, the lane-scaled mode and the compiler's only one) |
| **generated layer** | five generated sets (1,562 files) built from the sixteen calibration files' task sets: the transition grid, the return grid, the distractor grid, the familiarity ladder and the flap-stress set. Design, with no realism claim |
| **generalset** | the naturalistic set: workloads a generator would emit with realistic co-occurrence and transitions. Not built and not scheduled (backlog) |
| **channel** | a named mailbox a task can WAIT on; wakes are addressed to channels |
| **spawn table** | a pre-written list of children an orchestrator task (like `make`) creates at run time via FORK |
| **trace** | the simulator's output: the timetable plus everything that happened, from which all metrics are computed |
| **daemon** | the recognition-side program (박이안's tree): reads a workload's visible projection, runs a recognizer over it offline, emits a config schedule + recognition log |
| **run file** | the simulator's view of a workload: the events, with the answer key stripped |
| **visible projection** | the daemon's view of a workload: process names, counts, pinned lifetimes, each task's declared class and its pinned focus intervals — no behavior, no labels |
| **config schedule** | the daemon's output for the simulator: a list of (virtual time, configuration) pairs, applied as the run plays out |
| **recognition log** | the daemon's output for the grader: per query point, the telemetry shown, the full proposal, validation outcome, latency |
| **query point** | a moment the process set or the focus holder changes (per pinned events), triggering one recognizer consultation |
| **driver / consumer** | any subsystem that subscribes to the recognition signal and translates it into its own settings; the CPU scheduler is the one driver this project builds |
| **validator** | the gatekeeper between the daemon's proposal and the executor: rejects unknown vocabulary, clamps out-of-range values, falls back when proposals fail |
| **provenance** | the stamp on every applied configuration saying how it came to be: `unmodified`, `clamped`, `held`, or `fallback` — reported next to every result |
| **RQ0** | the first experiment: is the random-to-oracle gap even big enough to measure? Run before any LLM work |
| **Layer 1 / Layer 2** | the two measurement layers: recognition accuracy (was the situation read correctly?) vs. consumer performance (did scheduling actually improve?) — kept separate so "read right, didn't help" is a distinguishable outcome |
| **oversubscription / demand** | how much CPU the tasks collectively want, relative to the lane; a file of demand class `oversubscribed` is designed to hold contention so schedulers must make real choices. Every file's demand is computed and reported in the build manifest, never held to a window |
| **telemetry** | the "which processes exist right now" snapshots the daemon derives from the visible projection — names with their counts and the name of the process holding the window focus, never behavior or labels |
| **proposal** | a recognizer's full answer to one snapshot: reasoning + situation summary + `system` block (mode/attributes) + optional per-subsystem suggestions |
| **configuration (config)** | the validated scheduler settings the executor actually applies — algorithm choice plus its parameters plus the batch class's bandwidth cap; one entry of a config schedule |

---

*Next: your component's own guide — `simulator/simulator-guide.md` or `daemon/daemon-guide.md` — what your program must do, in what order to build it, and which decisions are yours. `data-contracts.md` is the shared reference for every format both guides mention.*
