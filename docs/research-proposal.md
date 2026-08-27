# A Semantic Recognition Layer for Operating Systems
> Status: draft — for team review · Created 2026-08-15 · Updated 2026-08-27

**Removing hardcoded semantic knowledge from the OS, validated on CPU scheduling**

**A research proposal**

**Team:** 인경민 (simulator / kernel side) · 박이안 (policy generation) · 인지오 (boundaries / experiment infrastructure)

**Status:** Draft for team review.

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
- [Part 10 — Future work](#part-10--future-work)
- [Appendix A — Glossary](#appendix-a--glossary)
- [Appendix B — A worked example](#appendix-b--a-worked-example)

---

# Part 0 — Summary

Operating systems are full of hardcoded semantic knowledge — tables where a human wrote down what things *are*. Windows and macOS Game Mode carry lists of known game executables. Scheduling classes wait for applications to declare their own nature. Special-case rules key off process names. Every one of these tables is a person, at some point, enumerating meaning by hand.

The tables are the limitation. They cannot cover software nobody registered, and each one expresses only the narrow distinction it was built for.

This project proposes replacing that enumeration with inference, and doing it once for the whole system rather than separately in each place.

## The proposal in one paragraph

A language model reads the set of processes currently running and produces a compact description of what the machine is being used for. That description is a **shared signal**, not a scheduler input. Any subsystem that wants it registers a thin driver that translates the signal into its own configuration — the way a device driver translates a kernel interface into hardware operations. The model never learns any subsystem's parameters, and no subsystem learns about any other.

```text
              LLM  —  reads processes, describes the situation
                              │
                    mode + attributes                ← shared contract
                              │
        ┌─────────────┬───────┴───────┬──────────────────┐
        ▼             ▼               ▼                  ▼
   CPU scheduler  Power governor  Network QoS      existing subsystems
   (this project)                                   (ignore the signal)
```

## What this work contributes

| Layer | What it is |
|---|---|
| **Architecture** | The recognition layer: a shared semantic vocabulary, a driver interface, and rules for what may and may not cross it |
| **Validation** | One driver, built and measured. Does the signal actually improve CPU scheduling, against a faithful reproduction of what shipping systems do today? |
| **Future work** | Additional drivers. Each is a thin adapter; the recognition layer does not change |

The central claim under test:

> **The meaning of a workload lives in the combination of processes, not in any single one of them. That combination cannot be enumerated in a lookup table, and reading it requires knowing what the software is for — knowledge a language model already has and an operating system does not.**

The model's job is not to pick a label from a menu. It reads a process set, works out the situation, and explains its reasoning — so that we can tell a correct decision from a lucky one.

A negative result is a publishable result. "The model reads the situation correctly but CPU scheduling does not improve" is a clean finding: it tells us the existing behavioural heuristics were already sufficient *for that consumer*, which is information the architecture needs and which does not invalidate it.

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

The sharpest version of this blindness, and the one our experiment is built around: **a game download the user is impatiently waiting for, and a virus scan the user did not ask for, are behaviourally identical.** Both are sustained background bulk work hammering the disk. Both should be treated completely differently — one throttled but never starved, the other freely deferred. No CPU utilization graph will ever separate them.

That difference appears only in the *name*. That gap is the entire project.

---

# Part 2 — The gap we are targeting

## 2.1 The mechanism already exists

An important correction to an assumption that is easy to make: **operating systems are not stuck with one static scheduling algorithm.** The machinery for varying scheduler behaviour is already present and shipping.

| System | Mechanism | How the decision is made |
|---|---|---|
| Linux | Scheduling classes (`SCHED_FIFO`, `SCHED_RR`, `SCHED_DEADLINE`, `SCHED_BATCH`, `SCHED_IDLE`) | Application or admin declares it via `sched_setscheduler` |
| Linux | `sched_ext` | Pluggable schedulers loaded from userspace as BPF programs |
| macOS | Quality-of-Service classes (`user-interactive`, `user-initiated`, `utility`, `background`) | Developer declares it in code |
| macOS 14+ | Game Mode | Hardcoded detection of full-screen games |
| Windows | Game Mode | Hardcoded list of known game executables |
| Linux | Feral GameMode daemon | Explicit opt-in list, or game calls the API itself |

Any proposal that claims "existing schedulers are static" will be corrected in the first five minutes of a review. We should state this correctly and build on it. The `sched_ext` row matters for a second reason: it is the concrete deployment path for anything this project produces, and it means our simulator work is a prototype of something shippable rather than a purely academic exercise.

## 2.2 The actual limitation is the list

The real problem is not the absence of mechanism. It is how the mechanism gets triggered:

- **Cooperation.** Linux scheduling classes and macOS QoS require the application to declare its own nature. Most applications never do. Those that do tend to claim they are the most important thing on the system. `updatedb` does not volunteer that it is background work.
- **Enumeration.** Game Mode works from a whitelist. Software nobody registered gets nothing.
- **Binary granularity.** Game Mode is on or off. There is no "gaming while streaming to Twitch, so the encoder must not drop frames" mode.

So the sharpened version of our research claim:

> Operating systems already accept that knowing *what the user is doing* is useful — they built the mechanism. What they lack is a way to figure it out without a whitelist or developer cooperation. Can an LLM supply that, once, for the whole system?

## 2.3 Why the meaning is in the combination

The critical property that makes this a reading problem rather than a matching problem: **no individual process reveals the situation.**

| Running processes | Situation | Scheduling implication |
|---|---|---|
| LoL, Discord, Chrome | Gaming | Frame latency is everything; suppress background work hard |
| Discord, Chrome | Casual browsing | Nothing special; ordinary MLFQ |
| LoL, Discord, Steam download | Gaming, transfer the user wants | Same as gaming, but the download is throttled, not starved |
| LoL, Discord, antivirus scan | Gaming, work the user did not ask for | Behaviourally identical to the row above; correct answer is the opposite |
| LoL, Discord, OBS | Gaming while streaming | Encoder is now latency-critical too — it cannot drop frames |
| cc1plus ×8, bash | Compiling | Throughput matters; interactive shell still needs to feel alive |

Discord appears in five of these and means something different each time. Chrome the same. Rows 3 and 4 are the sharpest pair in the table: same process count, same behavioural signature, opposite correct policy.

With `n` possible processes there are `2^n` possible combinations. A lookup table cannot cover that space.

## 2.4 Why this needs world knowledge

Reading that table requires knowing things about software that an operating system has no way to learn on its own: that OBS is a real-time encoder, that a Steam download is something the user initiated and is waiting on, that a scheduled antivirus scan is not, that `cargo build` is a compiler and `updatedb` is maintenance.

None of that is observable from process behaviour, and none of it can be assembled by enumeration without recreating the whitelist problem in a different place. It is, however, ordinary general knowledge — the kind of thing a language model has absorbed from pretraining without anyone assembling it for this purpose.

That is the specific capability we are testing. Not classification accuracy on a fixed menu of situations, but whether a model that already knows what software is for can turn that knowledge into a decision on a machine it has never seen.

## 2.5 What this replaces, and what it does not

This distinction determines the scope of every claim in the rest of the document, and getting it wrong invites an easy objection.

**Replaced: hardcoded semantic knowledge.** Game Mode's executable list. Special-case rules keyed on process names. Any table where a human wrote down what a piece of software *is*. These were already semantic judgements — they were simply frozen at authoring time and limited to whatever the author enumerated.

**Not replaced: the execution mechanism.** MLFQ's demotion rule, priority queues, timer interrupts, context switching. These are not stale knowledge waiting to be improved; they answer a different question on a different timescale.

```text
  LLM        →  what is this machine being used for   (seconds, meaning)
  Heuristic  →  who runs on this core right now       (microseconds, mechanism)
```

The gap in §4.1 is five to six orders of magnitude and does not close with better models, because scheduling decisions happen tens of thousands of times per second and inference cannot. Behavioural heuristics are therefore permanent residents of this design, not legacy to be cleared out. The recognition layer configures them; it does not replace them.

Stating this plainly makes the proposal narrower and considerably more defensible than "an LLM runs the OS."

---

# Part 3 — Research questions

**RQ0 — Measurability.** Before any model exists: does the choice of scheduling configuration change outcomes enough to measure on these workloads at all? A random recognizer is compared against perfect recognition, with no model in the loop. If a perfect recognizer scores close to a random one, no recognizer can demonstrate anything and every question below is unanswerable. Section 5.3 develops this. It requires no prompt, no model, and no API key, and it is the cheapest available falsification of the premise.

**RQ1 — Reading the situation.** Given only the names and command lines of currently running processes, can an LLM correctly work out what the system is being used for?

**RQ2 — Value.** Does correct reading produce measurably better scheduling than (a) no situation awareness, and (b) the whitelist approach real operating systems currently use?

**RQ3 — Vocabulary sufficiency.** Is the shared signal — mode plus attributes — enough for a consumer to act well, or does the consumer need the model to hand it configuration directly? This is the architecture question: if the vocabulary is sufficient, drivers stay thin and new consumers cost nothing. Section 4.6 measures it.

**RQ4 — Timing.** LLM inference takes hundreds of milliseconds to seconds. Scheduling decisions take microseconds. How long must a situation last before semantic scheduling pays for its own latency?

**RQ5 — Instrument soundness.** Every conclusion about RQ2 and RQ3 is measured through the CPU driver's mapping table. If that table maps distinct situations to indistinguishable configurations, or maps them to configurations far from what the situation admits, a correct reading is discarded before it reaches the scheduler — and the result reads as a negative finding about the signal when it is a finding about the mapping. Three checks answer this, all without a model and all before the full matrix: whether different rows of the table yield different configurations; whether those configurations yield different metrics; and how far each row sits from the best configuration a search can find for that situation. The last of these is the gap between perfect recognition and perfect configuration, and a large gap invalidates the interpretation of every other result rather than merely weakening it.

RQ1 and RQ2 can come apart, and that is the most interesting possible outcome. "The model reads situations accurately but scheduling performance does not improve" tells us the existing heuristics were already sufficient for this particular consumer — a real result, and one the architecture survives.

---

# Part 4 — System design

## 4.1 The constraint that determines everything

```text
  Scheduler decision           ~1-10 microseconds
  Context switch               ~1-5 microseconds
  Time slice                   ~1-10 milliseconds
  ---------------------------------------------------------
  One LLM inference            ~200-3000 milliseconds
                               5-6 orders of magnitude slower
```

**An LLM cannot make scheduling decisions.** In the time it takes to answer once, the scheduler has made hundreds of thousands of decisions.

The LLM therefore never participates in a scheduling decision. It sets a **configuration** that the deterministic scheduler then runs against at full speed.

```text
   +--------------------------------------------------------+
   |  SLOW LOOP  (seconds)                                  |
   |    process list -> LLM -> validator -> configuration    |
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

A note on the latency figure. A quantized 3–8B model running locally emits a short structured output in roughly 200–800 ms on consumer hardware, well under the hosted-API figures usually quoted. Since the model fires only when the process set changes materially — a handful of times per hour in real use — local inference is the realistic deployment shape, and it is what we should measure against.

## 4.2 Runtime flow

```text
   process set changes (launch / exit)
                │
                ▼
   ┌────────────────────────────────┐
   │  telemetry: process names,     │
   │  command lines, coarse stats   │
   └────────────┬───────────────────┘
                │  (asynchronous — no consumer ever waits)
                ▼
   ┌────────────────────────────────┐
   │  policy daemon                 │
   │   prompt -> LLM -> proposal    │
   │   validate, clamp, hold        │
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

1. **No consumer blocks on the LLM.** While a query is in flight, the previous configuration stays active. On first boot, the default is plain MLFQ.
2. **Failure is invisible.** If the LLM is slow, unreachable, or returns garbage, we keep the current configuration. After repeated failures we fall back to plain MLFQ permanently. The system must never depend on the LLM being available.
3. **The model is re-queried on change, not on a timer.** A gaming session may last an hour; polling every 30 seconds would produce 120 identical answers. Query when the process set changes materially, with a minimum hold time to prevent thrashing.

## 4.3 What the model produces

The proposal has two layers, and keeping them separate is what makes the architecture extensible.

```json
{
  "reasoning": "LeagueClient is a game running in the foreground, so frame
                deadlines dominate. OBS is capturing and encoding that game
                in real time, which gives it a hard deadline of its own —
                it cannot be treated as background work. The Steam process
                is downloading, which the user started deliberately, so it
                should be throttled rather than deferred.",

  "situation": "Gaming while streaming, with a user-initiated download",

  "system": {
    "mode": "gaming",
    "has_realtime_encoder": true,
    "background_is_wanted": true
  },

  "subsystems": {
    "cpu_scheduler": {
      "algorithm": "EDF",
      "params": { "admission_slack_ms": 2 },
      "batch_bandwidth_cap": 0.12
    }
  }
}
```

**`system`** is about the world and is subsystem-neutral. Every consumer reads it. This is the contract described in §4.4.

**`subsystems`** is a namespace, one key per consumer. Adding a network QoS driver adds a `network_qos` key and changes nothing else — not the `system` block, not the existing consumers, not the validator branches already written. This project fills exactly one key.

**`reasoning` is mandatory and comes first.** Three reasons, in increasing order of importance:

- *Diagnosis.* When a configuration performs badly we need to know whether the model misread the situation or read it correctly and drew the wrong conclusion. Those are different failures with different fixes — one is a knowledge problem, the other a mapping problem — and without the reasoning field they are indistinguishable in the logs.
- *Quality.* Requiring the model to state its reading before committing to a decision tends to produce better decisions than asking for the decision alone.
- *Auditability.* A system that changes behaviour for reasons nobody can inspect is not something an OS vendor would ship. A log line explaining why the machine entered a particular configuration is the difference between a feature and a black box.

`reasoning` and `situation` never cross into any consumer. The validator ignores them entirely; they flow to the logs and the evaluation harness.

The cost is real and should be stated: reasoning tokens add latency and inference cost. Because the duty cycle is low, we judge this affordable — but the latency figure that goes in the paper must be measured with reasoning included, not without.

## 4.4 The contract: shared vocabulary and consumer drivers

### 4.4.1 Why a shared layer rather than direct configuration

If the model emitted configuration for every subsystem and nothing else, it would need to know the tuning constants of all of them. Three problems follow.

**Consumers are not known in advance.** The CPU scheduler is in the kernel; a network shaper is a separate daemon; a third party might add something we never anticipated. If a new consumer requires editing the prompt, consumers are coupled to the model. With a shared vocabulary, a new consumer subscribes and brings its own interpretation — the model need not know it exists.

**The model has never seen any of these subsystems.** It knows what Blender is; it does not know what `timeslice_ms: 4` does on this machine, and it knows even less about a shaper it was never told about. Trusting direct configuration multiplies that risk by the number of consumers. Trusting the vocabulary does not.

**Failures need to be isolated.** If the model's CPU block is malformed but its reading is sound, the CPU driver should fall back to its own mapping while every other consumer proceeds normally. A flat output makes that impossible.

### 4.4.2 Consumers are drivers

The right mental model is a device driver: a thin adapter implementing a fixed interface, translating a general signal into its own domain. The kernel does not know what a driver does internally; drivers do not know about each other.

Consumers come in three kinds, and all three are legitimate:

| Kind | How it interprets the signal | Example |
|---|---|---|
| **Table** | Static `(mode, attributes) → config` mapping | CPU scheduler, power governor |
| **Agent** | Its own model, taking the signal as context | A consumer with genuinely complex policy |
| **Passive** | Does not subscribe at all | Most existing subsystems |

Table is the default. Agents multiply latency and cost, and — more seriously — two agents can interpret the same situation inconsistently and issue conflicting configurations. Passive consumers matter because they are why this design can be added to an existing OS incrementally: **subscription is optional, and a subsystem that ignores the signal behaves exactly as it does today.**

### 4.4.3 The vocabulary

**Modes** — what the machine is primarily doing:

| Mode | Situation |
|---|---|
| `interactive` | User at the keyboard, light work |
| `gaming` | Latency-critical foreground application |
| `compile` | Throughput-oriented batch work |
| `media` | Encoding, streaming, real-time capture |
| `idle` | No human present, maintenance only |

**Attributes** — independent facts that a mode label alone cannot carry:

| Attribute | Question |
|---|---|
| `has_realtime_encoder` | Is a periodic real-time producer running (encoder, DAW, capture)? |
| `background_is_wanted` | Is the sustained background work something the user asked for? |

Five labels alone cannot express the §2.3 table — plain gaming, gaming with a stream, and gaming with a download all collapse into `gaming`. Adding more labels does not fix this, because every new situation multiplies against the existing ones and the same distinctions recur inside every mode. Adding *dimensions* does:

```text
  5 labels                  →  5 situations,   5 validation rules
  5 labels + 2 attributes   →  20 situations,  7 validation rules
```

Expressiveness grows multiplicatively while validation cost grows additively, and orthogonal attributes let "both true" be a natural answer rather than a conflict.

### 4.4.4 The admission test for vocabulary terms

A term belongs in the shared vocabulary only if it is meaningful to more than one consumer and not derivable from behavioural observation. If MLFQ's demotion rule would discover it within a few time slices anyway, it carries no semantic information; if only one consumer can act on it, it is that consumer's configuration, not vocabulary.

| Term | CPU scheduler | Power governor | I/O scheduler | Network QoS |
|---|---|---|---|---|
| `mode` | Algorithm selection | Clock ceiling, thermal budget | Queue depth, readahead | Shaping policy |
| `has_realtime_encoder` | EDF becomes admissible | Hold a clock floor | Raise write priority | Reserve uplink |
| `background_is_wanted` | Throttle vs. defer | Suppress deep sleep | Bandwidth split | Background class |

Every row is filled in at least three columns. Filling this table is the concrete procedure for the vocabulary freeze in §8.2: a candidate attribute that lands in one column is configuration wearing a vocabulary costume, and gets rejected.

We stop at two attributes deliberately — each one multiplies the oracle search space (Part 7) — and the design extends to more without restructuring.

## 4.5 Algorithm menu

This section describes the CPU scheduler driver specifically. An algorithm earns a place in the menu only if there is a situation where it clearly beats the alternatives. Anything dominated everywhere is a baseline, not an option.

| Algorithm | Wins in | Why MLFQ loses there |
|---|---|---|
| **MLFQ** | Ordinary interactive use, idle | — this is the default and the right answer for mixed, unknown work |
| **EDF** (earliest deadline first) | Gaming, media, anything with a real-time producer | MLFQ has no concept of a deadline. It knows priority, not "this must complete within 3 ms or a frame drops" |
| **Lottery / Stride** | Contention with background work the user wants finished | MLFQ cannot guarantee proportions. "Roughly less" is easy; "exactly 15% to background" is not |
| **FIFO** | Pure batch throughput | Throughput wants minimum context switching and maximum cache locality; MLFQ keeps interrupting |

Note what selects between EDF and Lottery inside a gaming session: not the mode, but the attributes. This is the concrete payoff of §4.4.3 — with mode labels alone there were two candidate algorithms for `gaming` and no principled way to choose.

**Round Robin is deliberately excluded.** RR is MLFQ with a single queue — a special case, not an alternative. It remains a baseline for reporting, but there is no situation where a model should choose it.

A note on lottery scheduling: its advantage is proportional guarantees and starvation-freedom, not speed. Selection is O(n) in the number of processes (O(log n) with a tree), slower per decision than popping an MLFQ queue head. It earns its place because ticket allocation is the natural way to express something like `batch_bandwidth_cap`.

This mirrors what Linux already does — `SCHED_DEADLINE` is EDF, `SCHED_FIFO` is fixed-priority real-time, `SCHED_OTHER` is EEVDF, a deterministic relative of proportional-share scheduling. The mechanism for varying the algorithm exists. Deciding *when* to use which is the open problem.

**Two consequences for other parts of this document:**

- EDF requires deadlines in the process model. Workload `pattern` entries for periodic work must carry `period_ms` and `deadline_ms`, not just burst sizes. This must land before the schema freeze.
- Configuration fields are algorithm-dependent. MLFQ uses `timeslice_ms` / `num_queues` / `boost_interval_ms`; lottery uses ticket allocations; EDF uses admission parameters. Validation is conditional on the selected algorithm rather than a flat field list.

## 4.6 Measuring whether the vocabulary is sufficient — the RQ3 ladder

If a consumer can act well on the `system` block alone, drivers stay thin and new consumers cost nothing. If it needs the model to fill its `subsystems` block, every future consumer inherits that burden. This is the architecture's central open question, and we measure it by running the CPU scheduler driver at three levels.

**Variant A — vocabulary only.** The `subsystems` block is empty. Algorithm and parameters come from the driver's own offline-tuned table.

**Variant B — vocabulary plus algorithm.** The model fills `algorithm` but not parameters.

**Variant C — full configuration.** The model fills the whole `cpu_scheduler` block, as in §4.3.

All three keep `reasoning`, `situation`, and `system`.

**What each level asks:**

| Variant | Asks whether the model has | Knowledge source |
|---|---|---|
| A | Understanding of what the software is for | World knowledge from pretraining |
| B | Understanding of which algorithm class fits a situation | General CS knowledge |
| C | Ability to calibrate constants for a system it has never seen | System-specific knowledge it does not have |

**Reading the outcome.** If A performs close to C, the vocabulary is sufficient and the architecture works as designed: thin drivers, cheap new consumers. If C substantially beats A, the vocabulary is under-specified for this consumer and we should ask what it is missing rather than accept that every driver must be thick.

We expect improvement to stop somewhere around B. The model knows what Blender is; it has never observed what `timeslice_ms: 4` does in *our* simulator, and no amount of authority supplies that. If B works and C does not, the finding is "the model should read the situation and choose the algorithm class; the driver tunes the constants" — a deployable architecture, not a failure.

Note that hand-tuning the driver's table offline makes A *stronger* as an experiment, not weaker: if the table is near-optimal, A's performance reflects purely how well the situation was read.

## 4.7 What the model is never allowed to do

Bounding the model's authority is what makes the system defensible.

- It cannot invent new modes or attributes. Unknown keys and unknown labels are rejected.
- It cannot write into a `subsystems` key that no registered driver claims.
- It cannot alter the relative priority ordering between scheduling classes.
- It cannot reference specific PIDs. PIDs identify instances; instances die and PIDs get recycled into unrelated processes. All configuration is system-wide or class-scoped. Enforced by omitting PIDs from the telemetry schema, not by instructing the model to ignore them.
- It cannot remove starvation protection. Per-class bandwidth caps are enforced by the executor regardless of what any configuration says.

Every applied configuration is stamped with **provenance**: unmodified, clamped, held, or fallback. Without this, a good result is unattributable — we would not know whether the model performed well or the fallback did.

## 4.8 Implementation

We build a userspace discrete-event simulator rather than modifying a real kernel. Booting, interrupt handling, and memory management are a full semester of work on their own and answer none of our research questions. The simulator gives us fast iteration, easy metric collection, and deterministic replay. See `docs/simulator/primer.md` for a non-technical explanation of what it does and does not model.

| Component | Language | Rationale |
|---|---|---|
| Simulator | C++ | Logic carries over if we later port to xv6 or Linux `sched_ext` |
| Policy daemon | Python | We will edit prompts dozens of times a day; LLM SDKs live here |
| Bench harness | Python | pandas and matplotlib |

The two sides communicate over JSON across a process boundary. If we later replace the simulator with a real kernel, the daemon does not change at all. Starting with a simulator is the migration path, not throwaway work.

**Model hosting.** The client module supports both a hosted API and a local server (Ollama or vLLM) behind one interface. We use the API for fast prompt iteration and a local quantized model for the measurements that go in the paper: a deployment story that sends the running process list to a remote server is not credible; local inference is substantially faster on short structured outputs; and constrained decoding (GBNF grammars, guided decoding) can make malformed output structurally impossible, removing an entire class of validator branches. Comparing a frontier API model against a local 8B model is a cheap and worthwhile appendix result — if a small local model reads situations nearly as well, the deployment claim stops being hypothetical.

**Record and replay.** Running the full condition matrix against a live model would be slow, expensive, and non-reproducible. The daemon therefore runs in two modes. In *record* mode it queries the model once per distinct telemetry snapshot and stores `(prompt hash → response, measured latency)`. In *replay* mode it serves from that cache with no model in the loop. Because the cache key is `(workload id, process set hash, prompt version)` and telemetry does not depend on scheduling order, one cache serves every condition. This makes the full matrix deterministic and free to re-run.

---

# Part 5 — Experimental design

## 5.1 The core principle: swap one component

Any consumer can be decomposed into two parts:

- **The recognizer** — what situation are we in?
- **The executor** — given that, what do we do?

We hold the executor completely fixed across every condition and swap only the recognizer. Any performance difference is then attributable to recognition, because nothing else changed. In code, every condition implements one `Recognizer` interface; the oracle and the random recognizer are implementations of it just as the LLM is.

```text
   ┌─────────────────────┐
   │  fixed              │──┐
   │  no situation concept│  │
   ├─────────────────────┤  │
   │  random             │  │      ┌──────────────────┐
   │  random proposal    │  │      │  IDENTICAL       │
   ├─────────────────────┤  ├─────>│  EXECUTOR        │────> metrics
   │  whitelist          │  │      │                  │
   │  known-name matching│  │      │  same algorithms │
   ├─────────────────────┤  │      │  same parameters │
   │  llm_* (A / B / C)  │  │      │  same caps       │
   ├─────────────────────┤  │      └──────────────────┘
   │  oracle             │──┘
   │  ground truth       │
   └─────────────────────┘
```

## 5.2 Conditions

| Condition | Recognition | Configuration | Role |
|---|---|---|---|
| `fixed` | none — always default MLFQ | fixed | Floor: no situation awareness at all |
| `random` | uniformly random proposal | driver table | Control: what a useless recognizer scores |
| `whitelist` | hardcoded name matching | driver table | **Reproduces Windows / macOS Game Mode** |
| `llm_vocab` | LLM fills `system` only | driver table | Variant A |
| `llm_algo` | LLM fills `system` + algorithm | params from table | Variant B |
| `llm_full` | LLM fills the whole block | LLM | Variant C |
| `oracle` | ground truth from the workload file | driver table | Ceiling: perfect recognition |

The `whitelist` condition is the one that matters most for the paper. It is not a strawman we invented — it is what shipping operating systems actually do today. Beating it is the claim; failing to beat it is a legitimate finding.

Ownership note: 박이안 builds the whitelist baseline as well as the LLM conditions. Putting the strongest counter-hypothesis in the hands of the person arguing for the LLM keeps the result honest.

## 5.3 The gap that must exist first

**`random` versus `oracle` defines the entire measurable space of this experiment.** If a perfect recognizer scores only marginally better than a random one, then no recognizer can demonstrate anything, and the experiment is dead before we write a single prompt.

This can happen for a concrete reason worth watching for: if the per-class heuristics are strong enough, they self-correct misclassification. Put a compiler in the interactive class and the MLFQ demotion rule will move it within a few time slices anyway. The heuristics do not steal credit from the model — they eliminate the variance we are trying to measure.

**Both `random` and `oracle` can be run before any LLM integration exists.** The ground truth is already written in the workload file; random is one line of code. This is the cheapest possible early kill check, and it should be the first experiment we run. If the gap is narrow, we redesign workloads or deliberately weaken the executor's self-correction before investing in prompt engineering.

Phase 1 runs with modes only and no attributes. Attributes multiply the oracle cost and are not needed to answer "is anything measurable here at all."

## 5.4 Two layers of measurement

**Layer 1 — recognition accuracy.** Compare the `system` block against the ground truth in the workload file. No consumer involved at all. This is a pure reading test, so heuristics cannot contaminate it.

- Mode accuracy and per-mode confusion matrix
- Per-attribute accuracy, reported separately from mode accuracy
- Latency from process-set change to correct output, measured with reasoning tokens included
- Run-to-run consistency (LLMs are non-deterministic; a single good output means nothing)
- Accuracy split by well-known vs. unregistered software

Attribute accuracy is reported separately because the two failure types have different consequences. Getting `background_is_wanted` wrong on a gaming workload produces a specific, predictable performance failure; getting the mode wrong produces a diffuse one.

The `reasoning` field is read during failure analysis, not scored automatically. When a run produces a wrong configuration, the reasoning tells us which of two very different things went wrong: the model did not know what the software was, or it knew and drew the wrong conclusion. The first is a limit of the approach; the second is a prompt or mapping problem we can fix.

**Layer 2 — consumer performance.** The condition ladder above.

Separating these makes the ambiguous outcome interpretable. If Layer 1 is high and Layer 2 is flat, the conclusion is precise:

> The model reads system situations accurately. That reading does not improve CPU scheduling, because existing behavioural heuristics were already sufficient for this consumer.

## 5.5 Workloads

Workload definitions are the experiment. Each carries a ground-truth timeline — mode and attributes — that only the simulator, the oracle condition, and the Layer 1 grader can see.

```yaml
name: gaming_wanted_vs_unwanted_bulk
ground_truth:
  - t_ms: 0
    mode: gaming
    has_realtime_encoder: false
    background_is_wanted: true

processes:
  - name: League of Legends
    cmdline: "/opt/riot/LeagueClient --game"
    visible_to_llm: true
    pattern: { type: latency_critical, period_ms: 16, deadline_ms: 16, cpu_burst_ms: [4, 9] }
  - name: Discord
    cmdline: "/usr/bin/discord"
    visible_to_llm: true
    pattern: { type: interactive, cpu_burst_ms: [1, 4], io_wait_ms: [100, 800] }
  - name: steam
    cmdline: "/usr/bin/steam -applaunch download"
    visible_to_llm: true
    pattern: { type: io_heavy, cpu_burst_ms: [2, 10], io_wait_ms: [5, 20] }
```

**The information asymmetry is the core of the design:**

- `name` and `cmdline` — visible to the model only. No other condition receives them.
- `pattern` — visible to the simulator only. The model never sees ground truth about behaviour.
- `ground_truth` — visible to the oracle condition and the Layer 1 grader only.

This must be enforced in code. When results come out ambiguous there will be a temptation to "just give the model a bit more context," and without a recorded baseline the experiment loses its meaning.

### Family 1 — Single situation, long duration

Does situation awareness help at all in the easy case?

| Scenario | Mode | Attributes |
|---|---|---|
| Nightly maintenance: indexer + backup + updater, no input | `idle` | — |
| Parallel compile ×8 + editor | `compile` | — |
| Document work + mail client | `interactive` | — |

### Family 2 — Same process set, different intent ★

**The paper's core evidence.** Pairs whose process sets and behavioural signatures are nearly identical and whose correct policies differ.

| Scenario | Mode | Attributes | What splits it |
|---|---|---|---|
| Game + Steam download | `gaming` | `wanted: true` | Throttle, never starve |
| Game + antivirus full scan | `gaming` | `wanted: false` | Freely defer |
| Game + OBS capture | `gaming` | `encoder: true` | Two deadlines |
| ML training run + editor | `compile` | `wanted: true` | Long batch the user asked for |
| File indexer + editor | `interactive` | `wanted: false` | Long batch nobody asked for |

The last two are the sharpest pair in the whole design: both are "one sustained CPU-bound process plus an editor," and no behavioural heuristic can separate them even in principle.

### Family 3 — Unregistered software ★

Where the whitelist fails structurally, and where the world-knowledge claim in §2.4 is decided.

| Scenario | Mode | Attributes |
|---|---|---|
| Audio DAW + plugin chain | `media` | `encoder: true` |
| Godot-built indie game + Discord | `gaming` | — |
| Blender background render + Resolve timeline playback | `media` | `encoder: true`, `wanted: true` |
| Local Kubernetes + database + dev server | `compile` | `wanted: true` |

The DAW case is the most valuable single workload we have. Its deadlines are 1–3 ms rather than gaming's 16 ms, buffer underruns are audible rather than a dropped frame, and no shipping Game Mode covers it. It is simultaneously our hardest deadline test and a clean whitelist-failure case.

### Family 4 — Phase shift at varied speed (RQ4)

The same scenario sequence repeated with transitions every 60 s / 10 s / 2 s.

```text
compile → interactive → compile → media → idle
```

Steady-state periods should be short here, because only the transitions carry information (Part 7, first risk). This family produces the most quotable finding, of the form: *"Semantic configuration pays off only when a situation persists at least N times the model's round-trip latency."*

### Family 5 — Adversarial and boundary

| Scenario | Expectation |
|---|---|
| Miner renamed to `chrome.exe` | Misreading expected — the structural limit of name-based recognition |
| Compile + music playback | Genuinely ambiguous; humans would disagree |
| Chrome with 40 tabs, one playing video | Invisible at process granularity — a resolution limit, not a recognition failure |

The third case should be reported as a scope boundary rather than an error. "This approach operates at process granularity and cannot see inside a browser" is an honest and useful statement about where the idea stops working.

### Balance requirements

A gaming-heavy scenario set would produce a result whose scope is exactly the scope Game Mode already covers. Two balance constraints apply and should be checked before the workload set is frozen:

| Domain | Scenarios |
|---|---|
| Gaming | 3 |
| Creative / media | 3 |
| Development | 3 |
| Office / general | 2 |
| ML / data | 1 |
| Maintenance | 1 |

| Software familiarity | Scenarios |
|---|---|
| Well-known | 6 |
| Niche / unregistered | 5 |
| Mixed | 2 |

Results must be reported split by the second table. A result where the model wins only on the unregistered group is not a weak result — it is precisely what §2.4 predicts, and reporting it split is what makes it evidence rather than an average.

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
- Confusion matrix — which situations get mistaken for which
- Per-attribute accuracy, reported separately
- Accuracy split by well-known vs. unregistered software
- Time-to-correct-output after a situation transition
- Consistency across repeated runs on identical input

## 6.3 System health

- **Configuration age** — how old the underlying observation was when a configuration took effect
- **Provenance breakdown** — fraction of applied configurations that were unmodified, clamped, held, or fallback
- **Transition count** — how often the configuration changed, to detect oscillation
- **Token and latency cost** per query, with reasoning tokens counted, reported separately for API and local models

The provenance breakdown must accompany every performance figure. A condition that scores well while 70% of its configurations were fallbacks did not demonstrate anything about recognition; it demonstrated that MLFQ is fine.

## 6.4 Experiment hygiene

Seeded randomness, with **one independent random stream per simulated process**. This is not a detail: with a single global stream, changing the scheduler changes the order in which random draws are consumed, so two conditions face different workloads and the comparison is void.

Beyond that: repeated runs with variance reported, one variable changed at a time, identical workload traces across all conditions. Every result that cannot be reproduced from a config file and a seed does not count.

---

# Part 7 — Risks and honest weaknesses

**One consumer cannot validate a general vocabulary.** This is the most significant honest weakness of the whole proposal. We designed the vocabulary partly with the CPU scheduler in mind, then measure it on the CPU scheduler. That the terms are meaningful to other consumers is argued in §4.4.4 and demonstrated nowhere. The mitigation available within this project's scope is to enforce the admission test strictly during the vocabulary freeze — a term that only one consumer can act on gets rejected, which is the discipline that keeps the vocabulary from silently becoming CPU scheduler configuration. Building a second driver is out of scope here (Part 10). Until one exists, the extensibility claim is a design argument rather than a result, and the paper should say so in those words.

**The measurable window may be tiny.** A gaming session lasts an hour; the situation is stable for the whole thing. The only moments where recognition quality matters are transitions. If a one-hour run contains five interesting seconds, our workloads must be built around transitions rather than steady state.

**The whitelist baseline may simply win on common software.** For registered applications, a hardcoded list is accurate, instant, free, and deterministic. Our advantage exists only on software the list does not cover, which is why Family 3 is primary and why results are reported split by familiarity.

**Situations may not differ enough to matter.** If gaming and ordinary interactive use map to nearly identical configurations, reading the difference buys nothing. The mapping from vocabulary to configuration must produce genuinely distinct behaviour, and we should verify this before running the full matrix.

**Name-based reading is spoofable.** A process named `chrome.exe` that is actually a miner will be misread. We test this deliberately in Family 5 rather than pretending it does not exist.

**Non-determinism is a confound.** The same process set may yield different answers across runs. Layer 1 consistency measurement quantifies this; hysteresis and minimum hold time prevent it from causing oscillation. Local inference with a fixed seed and temperature 0 reduces it substantially.

**Reasoning costs latency.** Requiring the model to explain itself adds tokens to every query. The low duty cycle should absorb this, but the RQ4 answer must be computed from latencies measured with reasoning included. Reporting a fast latency measured without it would be dishonest.

**Oracle cost grows multiplicatively.** With five modes, two attributes, and four algorithms, the oracle searches up to 80 combinations per workload segment, and variant C's parameter oracle requires a grid search on top. Mitigations, in order of preference: run the full oracle on a representative subset and report the ceiling only for those; prune structurally inadmissible combinations (EDF with no deadline-bearing processes); keep the attribute count at two. If the full oracle becomes impractical we report a partial ceiling explicitly rather than quietly dropping it.

**Conditional validation is a real cost.** The validator must dispatch on subsystem key, then branch on algorithm within the CPU driver, with its own bounds and clamping rules per branch. Attributes add cross-field consistency checks on top. This is the largest single piece of added complexity, and it lands on one person.

**Scope honesty.** This is a simulator. It does not prove anything about real kernel performance, cache effects, or multi-core interactions. It answers whether the semantic signal carries information, which is a prerequisite for anything further — not a substitute for it.

---

# Part 8 — Team ownership and decisions to freeze

## 8.1 Areas

**인경민 — simulator and executor.** The discrete-event engine, virtual clock, process model. All scheduling algorithms and the per-class executor. Bandwidth caps and starvation protection. Telemetry extraction. The zero-delay oracle mode. Per-process random streams (§6.4). If we later port to `sched_ext`, that lands here.

**박이안 — recognition.** Prompt construction, model integration and local hosting, output schema design, Layer 1 evaluation. Also **the whitelist baseline** — putting the strongest counter-hypothesis in the hands of the person arguing for the LLM keeps the result honest.

**인지오 — contract boundary and experiment infrastructure.** The IPC layer, validation state machine (subsystem dispatch, then per-algorithm branching), clamping, fallback logic, provenance tracking. The record/replay cache (§4.8). The mock policy generator that lets the other two work independently. The full bench harness: experiment matrix, metrics, plots.

This layout puts every integration point in one person's hands, making integration a daily activity rather than a late-semester event.

## 8.2 Decisions requiring all three

1. **The shared vocabulary** — five modes plus two attributes (§4.4.3). Frozen before workload labelling begins; adding a third attribute later requires re-labelling every workload and re-running every oracle. **Use the admission test in §4.4.4 as the procedure**: fill the cross-consumer table for each candidate term and reject anything that lands in one column.
2. **The two protocol schemas** — telemetry out, proposal in. The `system` block is the contract; the `subsystems` block is per-consumer namespace.
3. **The CPU driver's mapping table.** Twenty entries, `(mode, attributes) → configuration`. This is effectively the executor's behaviour specification.
4. **Metric definitions.** Ambiguity here invalidates every interpretation.
5. **Workload scenarios**, including the domain and familiarity balance in §5.5.
6. **What the model may see.** Names, command lines, and coarse process counts are in. PIDs, ground-truth burst patterns, and ground-truth labels are out. Enforced in the telemetry schema, not in the prompt.

## 8.3 Operating rule

**Freeze the protocol early.** Once v1 is agreed, changes require all three of us plus a changelog entry. Three people writing against three slightly different assumptions about one interface, discovering it at integration time, is exactly how projects like this fail.

---

# Part 9 — Milestones

| Phase | Deliverable | Gate |
|---|---|---|
| 0 | Discrete-event simulator, MLFQ executor, workload loader, per-process RNG streams | A workload runs and produces reproducible metrics |
| 1 | `fixed`, `random`, `oracle` — **modes only, no attributes** | **Is the random-to-oracle gap large enough to measure?** If not, redesign before proceeding |
| 2 | Full vocabulary, CPU driver mapping table, `whitelist` condition | Whitelist beats fixed on gaming workloads |
| 3 | Mock generator, IPC, validator, provenance, record/replay cache | Full pipeline runs end to end with no model |
| 4 | `llm_vocab` (variant A), local model hosting | Layer 1 accuracy measured, split by software familiarity |
| 5 | `llm_algo` (variant B) | Does algorithm choice beat the driver's table? |
| 6 | `llm_full` (variant C) | Does the vocabulary turn out to be insufficient? |
| 7 | Phase-shift matrix at varied speeds | RQ4 answered |

Phase 1 is the critical gate. It requires no model, no prompts, and no API keys, and it can invalidate the entire premise cheaply. Run it first.

---

# Part 10 — Future work

**Additional consumer drivers.** Power governor, I/O scheduler, network QoS. Each is a thin adapter implementing the same interface against the same signal, and none requires touching the recognition layer or the prompt. A second driver is what would turn the extensibility argument of §4.4 into a measured result — two consumers interpreting one signal independently — and is the most direct continuation of this work.

**Third-party drivers.** Because subscription is optional and the contract is small, nothing prevents a driver being written by someone other than the OS vendor — for a game launcher, a build system, a media application. This is the property that distinguishes a recognition layer from a feature.

**Sweeping up the rest of the hardcoded semantic knowledge.** Game Mode's executable list is the most visible instance of a pattern that recurs throughout an OS: tables where a human wrote down what software is. Each is a candidate consumer. The long-term version of this work is not a better scheduler but an OS that infers this class of knowledge instead of shipping it as data.

**Real kernel implementation.** Porting the CPU driver to Linux `sched_ext` would move the result from "the signal carries information" to "the signal improves a real machine," and the daemon side would not change (§4.8).

**Recognition below process granularity.** Family 5 shows the resolution limit: a browser with forty tabs is opaque. Extending the signal to threads, cgroups, or application-reported sub-activities is a natural follow-on and a different research problem.

---

# Appendix A — Glossary

**Attribute** — an independent fact about the running process set, orthogonal to the mode label. Two are specified: `has_realtime_encoder` and `background_is_wanted`.

**Batch process** — work with no human waiting on it. Consumes all available CPU. Cares about total completion time.

**Consumer / driver** — a subsystem that subscribes to the recognition signal and translates it into its own configuration. Subscription is optional.

**Context switch** — saving one process's state and restoring another's. Costs 1–5 μs and discards cache locality.

**Deadline** — the time by which a periodic task must complete to be useful. A game rendering at 60 fps has a 16 ms deadline every frame; missing it drops the frame. An audio buffer at 128 samples has a deadline nearer 3 ms; missing it is audible.

**Discrete-event simulation** — advancing a virtual clock by jumping to the next scheduled event rather than ticking in real time. Mechanically a priority queue of future events.

**EDF (earliest deadline first)** — schedules whichever task has the nearest deadline. Optimal for meeting deadlines on a single core, but requires deadlines to be declared.

**Interactive process** — work with a human waiting on it. Short CPU bursts, long sleeps. Cares about response time.

**Lottery scheduling** — each process holds tickets; a random draw picks the winner. Gives proportional CPU shares and freedom from starvation, at O(n) selection cost.

**MLFQ** — Multi-Level Feedback Queue. Multiple priority levels; processes are demoted for using a full time slice and periodically boosted to prevent starvation. The basis of most production schedulers.

**Mode** — a label describing what the whole system is primarily being used for. One of five values, part of the shared vocabulary in §4.4.3.

**Preemption** — the kernel forcibly taking the CPU away from a running process, made possible by timer interrupts.

**Proposal** — the model's complete output: reasoning, situation description, `system` block, and `subsystems` block.

**Provenance** — the record of how an applied configuration was produced: unmodified, clamped, held from a previous cycle, or fallback.

**Recognition layer** — the architecture proposed here: a model that reads the process set, a shared vocabulary, and a driver interface for consumers.

**Response time** — arrival to first execution. The metric interactive work cares about.

**`sched_ext`** — a Linux facility for loading scheduling policies from userspace as BPF programs. The realistic deployment path for this work.

**Starvation** — a process being indefinitely denied CPU because higher-priority work keeps arriving.

**Time slice (quantum)** — how long a process may run before the scheduler reconsiders. Typically 1–10 ms.

**Turnaround time** — arrival to completion. The metric batch work cares about.

---

# Appendix B — A worked example

One workload followed from file to metric. The workload file is specified in §5.5; the telemetry and trace shapes below are illustrative, not frozen — they are part of decision 2 in §8.2.

## B.1 One file, three audiences

The `gaming_wanted_vs_unwanted_bulk` definition in §5.5 is read by three consumers, each of which sees a different slice:

```text
   name / cmdline  ──►  recognizer only
   pattern         ──►  simulator only
   ground_truth    ──►  oracle and the Layer 1 grader only
```

The partition is enforced by which module is handed which slice, not by prompt wording.

## B.2 Telemetry — simulator to daemon

The projection of the workload the recognizer is permitted to see:

```json
{
  "t_ms": 12400,
  "processes": [
    { "name": "League of Legends", "cmdline": "/opt/riot/LeagueClient --game" },
    { "name": "Discord",           "cmdline": "/usr/bin/discord" },
    { "name": "steam",             "cmdline": "/usr/bin/steam -applaunch download" }
  ],
  "counts": { "total": 3, "runnable": 2 }
}
```

| In | Out | Why excluded |
|---|---|---|
| names, command lines | PIDs | §4.7 — instances die and PIDs are recycled |
| coarse counts | burst patterns | that is the ground truth being tested against |
| | mode and attribute labels | that is the answer |

Telemetry is a pure function of which processes exist, and launches and exits are scripted in the workload. Nothing here depends on scheduling order, which is why one record/replay cache serves every condition (§4.8).

## B.3 Trace — simulator to harness

The timetable, written down. Every performance metric is read off this; nothing is timed.

```text
  CPU │ Discord │   steam   │ LoL │   steam   │ LoL │ Discord │
      └─────────┴───────────┴─────┴───────────┴─────┴─────────┘
      0        3          11    15          23    27        30   ms
```

```jsonl
{"t_ms": 0,  "event": "run_start", "proc": "Discord", "class": "interactive"}
{"t_ms": 3,  "event": "block",     "proc": "Discord", "reason": "io_wait"}
{"t_ms": 3,  "event": "run_start", "proc": "steam",   "class": "background"}
{"t_ms": 11, "event": "preempt",   "proc": "steam",   "reason": "bandwidth_cap"}
{"t_ms": 15, "event": "deadline",  "proc": "LoL",     "met": true, "slack_ms": 1}
{"t_ms": 16, "event": "config",    "algorithm": "EDF", "provenance": "clamped"}
```

Two event kinds carry information that block boundaries alone do not:

- **`deadline`** — the outcome of one periodic job. P99 frame latency and deadline miss rate are computed from these.
- **`config`** — every configuration change, stamped with provenance. §6.3 requires this alongside every performance figure: a condition that scored well while most of its configurations were fallbacks demonstrated nothing about recognition.

## B.4 Reading the deadline metrics off the trace

A `latency_critical` process is not one job. `period_ms: 16` means a new job arrives every 16 ms, and `deadline_ms: 16` means each is due 16 ms after its own arrival.

```text
  frame 1        frame 2        frame 3        frame 4
  ├──────┤       ├──────┤       ├──────┤       ├──────┤
  0     16      16     32      32     48      48     64   ms
  ↑      ↑
  arrives  due
```

Each frame needs the same 4–9 ms of CPU regardless of policy. Whether it lands before its deadline depends entirely on what the scheduler ran ahead of it — which is the effect this experiment measures, reduced to one number per frame.

```text
  slack_ms  =  deadline  −  completion
              positive → room to spare
              negative → late by that much
```

**Deadline miss rate** is the fraction of `deadline` events with `met: false`.

```text
  frame:  ✓ ✓ ✓ ✗ ✓ ✓ ✓ ✓ ✗ ✓ ✓ ✓     →  2/12 = 17%
```

**P99 frame latency** keeps the distribution that a miss rate discards — it cannot distinguish "finished instantly" from "barely made it every time."

```text
  frames sorted by completion time
  │▁▁▁▁▂▂▂▃▃▃▃▃▃▄▄▄▄▃▃▂▂▁▁                       ▁ ▁
  └──────────────┬──────────────────────────────┬────►
              mean 7 ms                     P99 = 31 ms
```

Both are reported because they fail differently. At 60 fps the 99th percentile is reached roughly once per second — often enough to be perceived as stutter while the mean still looks healthy. A scheduler can also hold the miss rate at zero while the tail creeps toward the deadline, which is a system about to fail under slightly more load. This is the §6.1 requirement to report percentiles rather than means, made concrete.
