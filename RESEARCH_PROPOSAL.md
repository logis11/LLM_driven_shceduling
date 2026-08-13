# Can an LLM Recognize What a Computer Is Doing, and Does That Help Scheduling?

**A research proposal**

**Team:** 인경민 (simulator / kernel side) · 박이안 (policy generation) · 인지오 (boundaries / experiment infrastructure)

**Status:** Draft for team review. Supersedes the parameter-tuning framing in `PROJECT_PLAN_DRAFT.md` §1.4–§1.5.

---

## Table of contents

- [Part 0 — Summary](#part-0--summary)
- [Part 1 — Background for readers with no OS experience](#part-1--background-for-readers-with-no-os-experience)
- [Part 2 — The gap we are targeting](#part-2--the-gap-we-are-targeting)
- [Part 3 — Research questions](#part-3--research-questions)
- [Part 4 — System design](#part-4--system-design)
- [Part 5 — Experimental design](#part-5--experimental-design)
- [Part 6 — Metrics](#part-6--metrics)
- [Part 7 — Risks and honest weaknesses](#part-7--risks-and-honest-weaknesses)
- [Part 8 — Team ownership and decisions to freeze](#part-8--team-ownership-and-decisions-to-freeze)
- [Part 9 — Milestones](#part-9--milestones)
- [Appendix A — Glossary](#appendix-a--glossary)

---

# Part 0 — Summary

Operating systems already change their scheduling behaviour based on *what the user is doing*. Windows and macOS both ship a "Game Mode." Linux has the Feral GameMode daemon. All of them work the same way: a hardcoded list of known game executables. If your program is on the list, the mode activates. If not, nothing happens.

The list is the limitation. It cannot cover software nobody registered, and it only expresses one bit of information — game, or not a game.

This project asks whether a language model can replace the list. Instead of matching against known names, an LLM reads the set of processes currently running and infers what the machine is being used for right now — gaming, compiling, video editing, idle background maintenance — and the scheduler is configured accordingly.

The central claim under test:

> **The meaning of a workload lives in the combination of processes, not in any single one of them. That combination cannot be enumerated in a lookup table, but a language model can read it.**

We will test this in a userspace scheduler simulator, against a ladder of baselines that includes a faithful reproduction of the whitelist approach real operating systems use today.

A negative result is a publishable result. "Mode inference is accurate but does not improve scheduling performance" would be a clean, useful finding, provided we measure it honestly.

---

# Part 1 — Background for readers with no OS experience

This section assumes no operating systems background. Readers who already know what MLFQ is can skip to [Part 2](#part-2--the-gap-we-are-targeting).

## 1.1 What a scheduler does

A CPU core runs exactly one thread at a time. But a typical machine has hundreds of processes that *could* run. So the kernel must continuously answer one question:

> **On this core, for the next few milliseconds, who runs?**

The component that answers is the **scheduler**. Two facts about it shape everything in this proposal.

**It runs constantly.** Thousands to tens of thousands of times per second, per core. Its decision logic has a budget measured in microseconds. A slow scheduler *is* the overhead.

**It cannot see the future.** The kernel does not know whether a process will finish in 5 ms, run for another 30 seconds, or immediately go to sleep waiting on the disk. The theoretically optimal policy — Shortest Job First — requires knowing job lengths in advance, which nobody ever does.

So every real scheduler is a guessing machine: a pile of heuristics that watch past behaviour to estimate the future.

## 1.2 Interactive vs. batch

The most important distinction a scheduler makes is between two kinds of work.

**Interactive** processes have a human waiting in front of them — a shell, a text editor, a browser. Their defining trait is that they do very little work and spend most of their time asleep. You press a key, the process wakes, works for a millisecond or two, and goes back to sleep waiting for the next keystroke.

**Batch** processes have nobody waiting — a compile, a backup, a file indexer, a video encode. Their defining trait is that they consume every cycle you give them. An eight-second compile computes for eight solid seconds.

```text
  bash (interactive)
  ▓  ░░░░░░░  ▓  ░░░░░░░░░░  ▓  ░░░░░  ▓  ░░░░░░░░░  ▓
     short burst, long sleep, repeat

  cc1plus (batch)
  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░
     runs continuously until finished

  ▓ = using CPU     ░ = waiting or finished
```

They want opposite treatment. Interactive work needs to *start* quickly — total runtime barely matters, but a 100 ms delay before the screen responds is perceived as lag. Batch work needs *total time* — being interrupted frequently wastes cycles on context switches and destroys cache locality.

The standard resolution is: give interactive work high priority but a very short turn on the CPU; give batch work low priority but a long turn when it does get one.

## 1.3 MLFQ, our baseline

**MLFQ (Multi-Level Feedback Queue)** is the algorithm family that Linux, macOS, and Windows all ship variants of. It maintains several priority queues and moves processes between them by watching behaviour:

- Used up your entire time slice? → probably batch → demote to a lower queue
- Went to sleep for I/O before your slice ran out? → probably interactive → stay high
- Periodically, boost everything back up so nothing starves forever

This is genuinely clever, and it explains why the diagram above works as a classifier: `bash` given a 2 ms slice uses 0.5 ms of it, while `cc1plus` burns all 2 ms. A few observations are enough to tell them apart.

**MLFQ is our real baseline.** Beating round-robin proves nothing.

## 1.4 What MLFQ cannot see

MLFQ observes *behaviour*, never *meaning*. A C++ compiler and a cryptocurrency miner both look like "CPU-bound." A file indexer and a chat client both look like "sleeps often, low CPU."

But `npm run build` and `updatedb` are completely different things: somebody is waiting on one of them and nobody is waiting on the other. That difference never appears in a CPU utilization graph. It appears in the *name*.

That gap is the entire project.

---

# Part 2 — The gap we are targeting

## 2.1 The mechanism already exists

An important correction to an assumption that is easy to make: **operating systems are not stuck with one static scheduling algorithm.** The machinery for varying scheduler behaviour is already present and shipping.

| System | Mechanism | How the decision is made |
|---|---|---|
| Linux | Scheduling classes (`SCHED_FIFO`, `SCHED_RR`, `SCHED_DEADLINE`, `SCHED_BATCH`, `SCHED_IDLE`) | Application or admin declares it via `sched_setscheduler` |
| macOS | Quality-of-Service classes (`user-interactive`, `user-initiated`, `utility`, `background`) | Developer declares it in code |
| macOS 14+ | Game Mode | Hardcoded detection of full-screen games |
| Windows | Game Mode | Hardcoded list of known game executables |
| Linux | Feral GameMode daemon | Explicit opt-in list, or game calls the API itself |

Any proposal that claims "existing schedulers are static" will be corrected in the first five minutes of a review. We should state this correctly and build on it.

## 2.2 The actual limitation is the list

The real problem is not the absence of mechanism. It is how the mechanism gets triggered:

- **Cooperation.** Linux scheduling classes and macOS QoS require the application to declare its own nature. Most applications never do. Those that do tend to claim they are the most important thing on the system. `updatedb` does not volunteer that it is background work.
- **Enumeration.** Game Mode works from a whitelist. Software nobody registered gets nothing.
- **Binary granularity.** Game Mode is on or off. There is no "gaming while streaming to Twitch, so the encoder must not drop frames" mode.

So the sharpened version of our research claim:

> Operating systems already accept that knowing *what the user is doing* is useful for scheduling — they built the mechanism. What they lack is a way to figure it out without a whitelist or developer cooperation. Can an LLM supply that?

## 2.3 Why the meaning is in the combination

The critical property that makes this an LLM problem rather than a regex problem: **no individual process reveals the situation.**

| Running processes | Situation | Scheduling implication |
|---|---|---|
| LoL, Discord, Chrome | Gaming | Frame latency is everything; suppress background work hard |
| Discord, Chrome | Casual browsing | Nothing special; ordinary MLFQ |
| LoL, Discord, Steam download | Gaming with background transfer | Same as gaming, but the download must be throttled, not starved |
| LoL, Discord, OBS | Gaming while streaming | Encoder is now latency-critical too — it cannot drop frames |
| cc1plus ×8, bash | Compiling | Throughput matters; interactive shell still needs to feel alive |

Discord appears in four of these and means something different each time. Chrome the same. The information exists only in the set.

With `n` possible processes there are `2^n` possible combinations. A lookup table cannot cover that space. This is precisely the kind of open-ended semantic judgment a language model is suited to, and precisely why the whitelist approach in shipping operating systems remains narrow.

---

# Part 3 — Research questions

**RQ1 — Recognition.** Given only the names and command lines of currently running processes, can an LLM correctly identify what the system is being used for?

**RQ2 — Value.** Does correct mode recognition produce measurably better scheduling than (a) no mode awareness, and (b) the whitelist approach real operating systems currently use?

**RQ3 — Division of labour.** How much authority should the LLM hold? Three nested levels: mode label only, mode plus algorithm choice, or mode plus algorithm plus parameters. Each level adds expressive power and validation burden. Where does the added authority stop paying for itself?

**RQ4 — Timing.** LLM inference takes on the order of seconds. Mode transitions take milliseconds. How long must a mode last before semantic scheduling pays for its own latency?

RQ1 and RQ2 can come apart, and that is the most interesting possible outcome. "The LLM recognizes modes accurately but scheduling performance does not improve" is a clean result that tells us the existing heuristics were already sufficient — a real contribution to the question of whether semantic context earns its keep.

---

# Part 4 — System design

## 4.1 The constraint that determines everything

```text
  Scheduler decision           ~1-10 microseconds
  Context switch               ~1-5 microseconds
  Time slice                   ~1-10 milliseconds
  ---------------------------------------------------------
  One LLM inference            ~500-3000 milliseconds
                               5-6 orders of magnitude slower
```

**An LLM cannot make scheduling decisions.** In the time it takes to answer once, the scheduler has made hundreds of thousands of decisions.

The LLM therefore never participates in a scheduling decision. It sets a **configuration** that the deterministic scheduler then runs against at full speed.

```text
   +--------------------------------------------------------+
   |  SLOW LOOP  (seconds)                                  |
   |    process list -> LLM -> validator -> mode + config    |
   +---------------------------+----------------------------+
                               |
                               | configuration only
                               v
   +--------------------------------------------------------+
   |  FAST LOOP  (microseconds)                             |
   |    pick next process, run it, repeat                    |
   +--------------------------------------------------------+
```

If this separation ever breaks, the project does not work.

An important consequence: because the LLM only sets configuration, a *stale* configuration is merely suboptimal, never broken. A slightly mistuned MLFQ is still a completely valid scheduler. **The floor of this design is "an ordinary scheduler," not "a broken system."**

## 4.2 Runtime flow

```text
   process set changes (launch / exit)
                │
                ▼
   ┌────────────────────────────────┐
   │  telemetry: process names,     │
   │  command lines, coarse stats   │
   └────────────┬───────────────────┘
                │  (asynchronous — the scheduler never waits)
                ▼
   ┌────────────────────────────────┐
   │  policy daemon                 │
   │   prompt -> LLM -> mode        │
   │   validate: known mode? clamp  │
   └────────────┬───────────────────┘
                │
                ▼
   ┌────────────────────────────────┐
   │  active scheduler configuration │
   │   algorithm + parameters        │
   │   + per-class bandwidth caps    │
   └────────────┬───────────────────┘
                │
   ═════════════╪═════════════ nothing below this line involves the LLM
                ▼
   ┌────────────────────────────────┐
   │  scheduling loop (1000s/sec)   │
   │   read current configuration   │
   │   pick next process, run it    │
   └────────────────────────────────┘
```

Three properties worth stating explicitly:

1. **The scheduler never blocks on the LLM.** While a query is in flight, the previous configuration stays active. On first boot, the default is plain MLFQ.
2. **Failure is invisible.** If the LLM is slow, unreachable, or returns garbage, we keep the current configuration. After repeated failures we fall back to plain MLFQ permanently. The system must never depend on the LLM being available.
3. **The mode is re-queried on change, not on a timer.** A gaming session may last an hour; polling every 30 seconds would produce 120 identical answers. Query when the process set changes materially, with a minimum hold time to prevent thrashing.

## 4.3 Mode vocabulary

The mode set must be fixed before we write oracle labels into workloads. Proposed starting set — deliberately small:

| Mode | Situation | Scheduling intent |
|---|---|---|
| `interactive` | User at the keyboard, light work | Favour responsiveness; default balanced config |
| `gaming` | Latency-critical foreground application | Short slices, hard cap on background work |
| `compile` | Throughput-oriented batch work | Long slices, keep one shell responsive |
| `media` | Encoding, streaming, real-time capture | Protect the deadline-sensitive process specifically |
| `idle` | No human present, maintenance only | Let background work run freely |

Five modes keeps the oracle enumerable and the classification-accuracy measurement meaningful. We can extend later; extending is cheap, and shrinking after workloads are labelled is not.

## 4.4 Algorithm menu

An algorithm earns a place in the menu only if there is a mode where it clearly beats the alternatives. Anything that is dominated everywhere is a baseline, not an option.

| Algorithm | Wins in | Why MLFQ loses there |
|---|---|---|
| **MLFQ** | `interactive`, `idle` | — this is the default and the right answer for mixed, unknown work |
| **EDF** (earliest deadline first) | `gaming`, `media` | MLFQ has no concept of a deadline. It knows priority, not "this must complete within 3 ms or a frame drops" |
| **Lottery / Stride** | `gaming` with contention, `media` | MLFQ cannot guarantee proportions. "Roughly less" is easy; "exactly 15% to background" is not |
| **FIFO** | `compile` | Pure throughput wants minimum context switching and maximum cache locality; MLFQ keeps interrupting |

**Round Robin is deliberately excluded from the menu.** RR is MLFQ with a single queue — a special case, not an alternative. It remains a baseline for reporting, but there is no mode where an LLM should choose it.

A note on lottery scheduling: its advantage is proportional guarantees and starvation-freedom, not speed. Selection is O(n) in the number of processes (O(log n) with a tree), which is slower per decision than popping an MLFQ queue head. It earns its place because ticket allocation is the natural way to express something like `batch_bandwidth_cap`, not because it is fast.

This mirrors what Linux already does — `SCHED_DEADLINE` is EDF, `SCHED_FIFO` is fixed-priority real-time, `SCHED_OTHER` is EEVDF, a deterministic relative of proportional-share scheduling. Again: the mechanism for varying the algorithm exists. Deciding *when* to use which is the open problem.

**Two consequences for other parts of this document:**

- EDF requires deadlines in the process model. Workload `pattern` entries for periodic work must carry `period_ms` and `deadline_ms`, not just burst sizes. This is a simulator-side model change that must land before the schema freeze.
- Configuration fields become algorithm-dependent. MLFQ uses `timeslice_ms` / `num_queues` / `boost_interval_ms`; lottery uses ticket allocations; EDF uses admission parameters. Validation is therefore conditional on the selected algorithm rather than a flat field list.

## 4.5 Three output variants — the RQ3 ladder

The LLM's output can be scoped at three levels of increasing authority. These are nested, not competing: each is a superset of the one above it.

**Variant A — mode only.** The LLM emits a label. Algorithm and parameters both come from an offline-tuned mapping table.

```json
{ "mode": "gaming", "confidence": 0.9 }
```

Validation is a single enum check. Unknown mode → reject and hold.

**Variant B — mode and algorithm.** The LLM picks the algorithm too, so the same mode can receive different algorithms depending on context.

```json
{ "mode": "gaming", "algorithm": "EDF", "confidence": 0.85 }
```

Validation is two enum checks plus a compatibility check: EDF is only admissible if the workload actually has deadline-bearing processes.

**Variant C — full configuration.** The LLM emits algorithm-specific parameters as well.

```json
{
  "mode": "gaming",
  "algorithm": "EDF",
  "params": {
    "admission_slack_ms": 2,
    "fallback_algorithm": "MLFQ"
  },
  "class_priority": ["realtime", "interactive", "batch", "idle"],
  "batch_bandwidth_cap": 0.15
}
```

Validation now requires per-field bounds, clamping, and cross-field consistency. A `timeslice_ms` of 0 would freeze the system.

**What each step buys, and what it must justify:**

| Step | Additional authority | Only justified if |
|---|---|---|
| A → B | Algorithm choice | Some mode genuinely splits — `gaming` alone wants EDF but `gaming` + streaming wants proportional share; `compile` alone wants FIFO but `compile` + an open editor wants MLFQ |
| B → C | Parameter tuning | Within a fixed mode and algorithm, the right constants vary by situation in a way a lookup table cannot capture |

If neither condition holds, the corresponding step adds validation burden and nondeterminism for nothing — and the experiment will say so. That is the point of measuring A, B, and C separately rather than assuming the most expressive version is best.

Note also that hand-tuning the mapping table offline makes variant A *stronger* as an experiment, not weaker: if the mapping is near-optimal, A's performance reflects purely how well the mode was recognized, with no contamination from algorithm or parameter quality.

## 4.6 What the LLM is never allowed to do

Bounding the LLM's authority is what makes the system defensible.

- It cannot invent new modes. Unknown labels are rejected.
- It cannot alter the relative priority ordering between scheduling classes.
- It cannot reference specific PIDs. PIDs identify instances; instances die and PIDs get recycled into unrelated processes. All configuration is system-wide or class-scoped.
- It cannot remove starvation protection. Per-class bandwidth caps are enforced by the kernel side regardless of what any configuration says. Without this, a `gaming` mode that fully suppresses background work would let a backup job wait forever.

Every applied configuration is stamped with **provenance**: whether it came through unmodified, was clamped, or is a fallback. Without this, a good result is unattributable — we would not know whether the LLM performed well or the fallback did.

## 4.7 Implementation

We build a userspace discrete-event simulator rather than modifying a real kernel. Booting, interrupt handling, and memory management are a full semester of work on their own and answer none of our research questions. The simulator gives us fast iteration, easy metric collection, and a deterministic replay for fair comparison.

| Component | Language | Rationale |
|---|---|---|
| Simulator | C++ | Logic carries over if we later port to xv6 or Linux `sched_ext` |
| Policy daemon | Python | We will edit prompts dozens of times a day; LLM SDKs live here |
| Bench harness | Python | pandas and matplotlib |

The two sides communicate over JSON across a process boundary. This matters more than it looks: if we later replace the simulator with a real kernel, the daemon does not change at all. Starting with a simulator is the migration path, not throwaway work.

---

# Part 5 — Experimental design

## 5.1 The core principle: swap one component

Any scheduler can be decomposed into two parts:

- **The recognizer** — what situation are we in?
- **The executor** — given that, how do we allocate CPU?

We hold the executor completely fixed across every condition and swap only the recognizer. Any performance difference is then attributable to recognition, because nothing else changed.

```text
   ┌─────────────────────┐
   │  fixed              │──┐
   │  no mode concept    │  │
   ├─────────────────────┤  │
   │  random             │  │      ┌──────────────────┐
   │  random mode        │  │      │  IDENTICAL       │
   ├─────────────────────┤  ├─────>│  EXECUTOR        │────> metrics
   │  whitelist          │  │      │                  │
   │  known-name matching│  │      │  same algorithms │
   ├─────────────────────┤  │      │  same parameters │
   │  llm_mode           │  │      │  same caps       │
   │  LLM reads set      │  │      └──────────────────┘
   ├─────────────────────┤  │
   │  llm_full           │  │
   │  LLM sets params too│  │
   ├─────────────────────┤  │
   │  oracle             │──┘
   │  ground-truth label │
   └─────────────────────┘
```

## 5.2 Conditions

| Condition | Mode recognition | Parameters | Role |
|---|---|---|---|
| `fixed` | none — always default MLFQ | fixed | Floor: no mode awareness at all |
| `random` | uniformly random mode | mapped | Control: what a useless recognizer scores |
| `whitelist` | hardcoded name matching | mapped | **Reproduces Windows / macOS Game Mode** |
| `llm_mode` | LLM reads the process set | algorithm + params mapped | Variant A |
| `llm_mode_algo` | LLM reads the process set | LLM picks algorithm, params mapped | Variant B |
| `llm_full` | LLM reads the process set | LLM picks algorithm and params | Variant C |
| `oracle` | ground-truth label from the workload file | mapped | Ceiling: perfect recognition |

The `whitelist` condition is the one that matters most for the paper. It is not a strawman we invented — it is what shipping operating systems actually do today. Beating it is the claim; failing to beat it is a legitimate finding.

## 5.3 The gap that must exist first

**`random` versus `oracle` defines the entire measurable space of this experiment.** If a perfect recognizer scores only marginally better than a random one, then no recognizer can demonstrate anything, and the experiment is dead before we write a single prompt.

This can happen for a concrete reason worth watching for: if the per-class heuristics are strong enough, they self-correct misclassification. Put a compiler in the interactive class and the MLFQ demotion rule will move it within a few time slices anyway. The heuristics do not steal credit from the LLM — they eliminate the variance we are trying to measure.

**Both `random` and `oracle` can be run before any LLM integration exists.** The oracle label is already written in the workload file; random is one line of code. This is the cheapest possible early kill check, and it should be the first experiment we run. If the gap is narrow, we redesign workloads or deliberately weaken the executor's self-correction before investing in prompt engineering.

## 5.4 Two layers of measurement

**Layer 1 — recognition accuracy.** Compare LLM output against the ground-truth mode label in the workload file. No scheduler involved at all. This is a pure labelling test, so heuristics cannot contaminate it.

- Accuracy, per-mode confusion matrix
- Latency from process-set change to correct label
- Run-to-run consistency (LLMs are nondeterministic; a single good output means nothing)

**Layer 2 — scheduling performance.** The condition ladder above.

Separating these makes the ambiguous outcome interpretable. If Layer 1 is high and Layer 2 is flat, the conclusion is precise:

> The LLM recognizes system modes accurately. That recognition does not improve scheduling performance, because existing behavioural heuristics were already sufficient.

## 5.5 Workloads

Workload definitions are the experiment. Each carries a ground-truth mode timeline that only the simulator and the oracle condition can see.

```yaml
name: gaming_to_compile
ground_truth_modes:
  - { t_ms: 0,     mode: gaming }
  - { t_ms: 45000, mode: compile }

processes:
  - name: League of Legends
    cmdline: "/opt/riot/LeagueClient --game"
    visible_to_llm: true
    pattern: { type: latency_critical, period_ms: 16, deadline_ms: 16, cpu_burst_ms: [4, 9] }
  - name: Discord
    cmdline: "/usr/bin/discord"
    visible_to_llm: true
    pattern: { type: interactive, cpu_burst_ms: [1, 4], io_wait_ms: [100, 800] }
  - name: updatedb
    cmdline: "/usr/bin/updatedb"
    visible_to_llm: true
    pattern: { type: io_heavy, cpu_burst_ms: [2, 10], io_wait_ms: [5, 20] }
```

**The information asymmetry is the core of the design:**

- `name` and `cmdline` — visible to the LLM only. No other condition receives them.
- `pattern` — visible to the simulator only. The LLM never sees ground truth about behaviour.
- `ground_truth_modes` — visible to the oracle condition and the Layer 1 grader only.

This must be written down and enforced in code. When results come out ambiguous there will be a temptation to "just give the LLM a bit more context," and without a recorded baseline the experiment loses its meaning.

**Required workload families:**

| Family | Purpose |
|---|---|
| Single-mode, long duration | Does mode awareness help at all in the easy case? |
| Ambiguous combinations | Same process set, different intent — tests whether combination reading is real |
| Unregistered software | Programs no whitelist would know — the central advantage claim |
| Phase-shift, varied speed | Mode changes every 60 s / 10 s / 2 s — answers RQ4 |
| Adversarial naming | Misleading names — how brittle is name-based recognition? |

The phase-shift family is what produces the most quotable finding, of the form: *"Semantic scheduling pays off only when a mode persists at least N times the LLM round-trip latency."*

---

# Part 6 — Metrics

## 6.1 Performance

Definitions must be agreed before any run, or every interpretation of results collapses.

| Metric | Definition | Matters for |
|---|---|---|
| Response time | arrival → first time on CPU | Interactive, gaming |
| Turnaround time | arrival → completion | Batch, compile |
| P99 frame latency | 99th percentile of periodic-task completion | Gaming, media |
| Deadline miss rate | fraction of periodic deadlines missed | Gaming, media |
| Throughput | batch work completed per unit time | Compile |
| Starvation | max time any process waited without running | All — safety check |

Report percentiles, not just means. For interactive work the tail is the experience; a good average with a bad P99 feels terrible to a human.

## 6.2 Recognition

- Mode accuracy, overall and per-mode
- Confusion matrix — which modes get mistaken for which
- Time-to-correct-label after a mode transition
- Consistency across repeated runs on identical input

## 6.3 System health

- **Configuration age** — how old the underlying observation was when a configuration took effect
- **Provenance breakdown** — fraction of applied configurations that were unmodified, clamped, held, or fallback
- **Transition count** — how often the mode changed, to detect oscillation
- **Token and latency cost** per query

## 6.4 Experiment hygiene

Seeded randomness. Repeated runs with variance reported. One variable changed at a time. Identical workload traces across all conditions. Every result that cannot be reproduced from a config file and a seed does not count.

---

# Part 7 — Risks and honest weaknesses

**The measurable window may be tiny.** A gaming session lasts an hour; the mode is stable for the whole thing. The only moments where recognition quality matters are transitions. If a one-hour run contains five interesting seconds, our workloads must be built around transitions rather than steady state. This is a design constraint, not a flaw, but it must be acknowledged.

**The whitelist baseline may simply win.** For common software, a hardcoded list is accurate, instant, free, and deterministic. Our advantage only appears on software the list does not cover. If our workloads consist mostly of well-known applications, we have designed an experiment we cannot win — and if they consist entirely of obscure software, we have designed one that is unrepresentative. The balance between these is a genuine methodological risk and should be decided deliberately.

**Modes may not differ enough to matter.** If `gaming` and `interactive` map to nearly identical configurations, recognizing the difference buys nothing. The mode-to-configuration mapping must produce genuinely distinct behaviour, and we should verify this before running the full matrix.

**Name-based recognition is spoofable.** A process named `chrome.exe` that is actually a miner will be misread. We test this deliberately in the adversarial workload family rather than pretending it does not exist.

**Nondeterminism is a confound.** The same process set may yield different answers across runs. Layer 1 consistency measurement exists specifically to quantify this, and hysteresis plus minimum hold time exist to prevent it from causing oscillation.

**Oracle cost grows multiplicatively.** With five modes and four algorithms the oracle must search twenty mode-algorithm pairs per workload segment, and variant C's parameter oracle requires a grid search on top of that. Simulator runs are cheap individually, but the matrix is not. If the full oracle becomes impractical we will compute it for a representative subset of workloads and report the ceiling only for those, rather than quietly dropping the ceiling.

**Conditional validation is a real cost.** Because configuration fields depend on the selected algorithm, the validator cannot be a flat schema check. It must branch on algorithm, and each branch needs its own bounds and clamping rules. This is the largest single piece of added complexity from the four-algorithm menu, and it lands on one person.

**Scope honesty.** This is a simulator. It does not prove anything about real kernel performance, cache effects, or multi-core interactions. It answers whether the semantic signal carries information, which is a prerequisite for anything further — not a substitute for it.

---

# Part 8 — Team ownership and decisions to freeze

## 8.1 Areas

**인경민 — simulator and executor.** The discrete-event engine, virtual clock, process model. All scheduling algorithms and the per-class executor. Bandwidth caps and starvation protection. Telemetry extraction. The zero-delay oracle mode. If we later port to a real kernel, that lands here.

**박이안 — recognition.** Prompt construction, LLM integration, mode schema design, Layer 1 evaluation. Also **the whitelist baseline** — putting the strongest counter-hypothesis in the hands of the person arguing for the LLM keeps the result honest.

**인지오 — boundaries and experiment infrastructure.** The IPC layer, validation state machine, clamping, fallback logic, provenance tracking. The mock policy generator that lets the other two work independently. The full bench harness: experiment matrix, metrics, plots.

This layout puts every integration point in one person's hands, making integration a daily activity rather than a late-semester event.

## 8.2 Decisions requiring all three

1. **The mode vocabulary.** Must be frozen before workload labelling begins.
2. **The two protocol schemas** — telemetry out, configuration in. The configuration fields are the complete set of powers the LLM has over the system.
3. **The mode-to-configuration mapping.** This is effectively the executor's behaviour specification.
4. **Metric definitions.** Ambiguity here invalidates every interpretation.
5. **Workload scenarios**, including the balance between well-known and obscure software discussed in Part 7.
6. **What the LLM may see.** Names, command lines, and coarse process counts are in. Ground-truth burst patterns and mode labels are out. Write this down.

## 8.3 Operating rule

**Freeze the protocol early.** Once v1 is agreed, changes require all three of us plus a changelog entry. Three people writing against three slightly different assumptions about one interface, discovering it at integration time, is exactly how projects like this fail.

---

# Part 9 — Milestones

| Phase | Deliverable | Gate |
|---|---|---|
| 0 | Discrete-event simulator, MLFQ executor, workload loader | A workload runs and produces metrics |
| 1 | `fixed`, `random`, `oracle` conditions | **Is the random-to-oracle gap large enough to measure?** If not, redesign before proceeding |
| 2 | Mode schema, mode-to-configuration mapping, `whitelist` condition | Whitelist beats fixed on gaming workloads |
| 3 | Mock generator, IPC, validator, provenance | Full pipeline runs end to end with no LLM |
| 4 | `llm_mode` (variant A) | Layer 1 accuracy measured |
| 5 | `llm_mode_algo` (variant B) | Does algorithm choice beat fixed mapping? |
| 6 | `llm_full` (variant C) | Does parameter authority add anything on top? |
| 7 | Phase-shift matrix at varied speeds | RQ4 answered |

Phase 1 is the critical gate. It requires no LLM, no prompts, and no API keys, and it can invalidate the entire premise cheaply. Run it first.

---

# Appendix A — Glossary

**Batch process** — work with no human waiting on it. Consumes all available CPU. Cares about total completion time.

**Context switch** — saving one process's state and restoring another's. Costs 1–5 μs and discards cache locality.

**Deadline** — the time by which a periodic task must complete to be useful. A game rendering at 60 fps has a 16 ms deadline every frame; missing it drops the frame.

**EDF (earliest deadline first)** — schedules whichever task has the nearest deadline. Optimal for meeting deadlines on a single core, but requires deadlines to be declared.

**Discrete-event simulation** — advancing a virtual clock by jumping to the next scheduled event rather than ticking in real time. Mechanically a priority queue of future events.

**Interactive process** — work with a human waiting on it. Short CPU bursts, long sleeps. Cares about response time.

**MLFQ** — Multi-Level Feedback Queue. Multiple priority levels; processes are demoted for using a full time slice and periodically boosted to prevent starvation. The basis of most production schedulers.

**Mode** — in this proposal, a label describing what the whole system is being used for at a moment in time, inferred from the set of running processes.

**Lottery scheduling** — each process holds tickets; a random draw picks the winner. Gives proportional CPU shares and freedom from starvation, at O(n) selection cost.

**Preemption** — the kernel forcibly taking the CPU away from a running process, made possible by timer interrupts.

**Provenance** — the record of how an applied configuration was produced: unmodified, clamped, held from a previous cycle, or fallback.

**Starvation** — a process being indefinitely denied CPU because higher-priority work keeps arriving.

**Time slice (quantum)** — how long a process may run before the scheduler reconsiders. Typically 1–10 ms.

**Turnaround time** — arrival to completion. The metric batch work cares about.

**Response time** — arrival to first execution. The metric interactive work cares about.
