# LLM-Guided OS — Implementation Plan & Team Structure

**Team:** 인경민 (security/systems) · 박이안 (ML/SWE) · 인지오 (SWE/infra)

**Status:** Draft for discussion. Nothing here is frozen yet.

This document has three parts:

- **Part 1** — roughly what we are building and why it is shaped this way. Written assuming no deep OS background.
- **Part 2** — who owns what, and which decisions we have to make together.
- **Part 3** — what we each need to learn before and during the build.

---

# Part 1 — What We Are Building

## 1.1 What a scheduler actually does

A CPU core runs exactly one thread at a time. But there are usually dozens or hundreds of processes that *could* run. So the kernel has to keep answering one question:

> **"On this core, for the next few milliseconds, who runs?"**

The component that answers this is the **scheduler**. Two things about it matter for our project:

**It runs constantly.** Thousands to tens of thousands of times per second, per core. Its own decision logic has a budget measured in **microseconds**. If the scheduler is slow, the scheduler *is* the overhead.

**It cannot see the future.** The kernel does not know whether a process will finish in 5 ms, run for another 30 seconds, or immediately go to sleep waiting on disk I/O. The theoretically optimal policy (Shortest Job First) requires knowing job lengths in advance — which nobody ever knows.

So **every real scheduler is a guessing machine**: a pile of heuristics that look at past behavior to estimate the future.

## 1.2 What existing schedulers guess

| Algorithm | What it assumes | Where it falls short |
|---|---|---|
| **Round Robin** | Nothing. Everyone takes turns equally | Interactive work gets buried under batch work |
| **Priority** | A human assigned importance up front (`nice`) | Static. Wrong as soon as the workload shifts. Starvation risk |
| **MLFQ** | *"Uses its full timeslice → batch job. Sleeps quickly → interactive job"* | Only sees observed behavior, never intent |

**MLFQ (Multi-Level Feedback Queue) is our real baseline.** It keeps several priority queues: use up your timeslice and you get demoted; block on I/O quickly and you stay high. In other words, it **infers a process's character by watching how it behaves**. Linux, macOS, and Windows all ship variants of this idea.

But MLFQ observes *behavior*, not *meaning*. A C++ compiler burning CPU and a crypto miner burning CPU look identical to it. Both are just "CPU-bound."

## 1.3 The bet this project is making

That gap is the whole project. In one sentence:

> **Is there information that never shows up in a CPU utilization graph, but does show up in a process name, a command line, or one sentence from the user — and is that information useful for scheduling?**

`npm run build` and `updatedb` can look nearly identical in telemetry, yet they are completely different: someone is waiting on one of them and nobody is waiting on the other. An LLM can *read* that difference.

Whether that actually helps is an open question, and answering it is the point. **A negative result is still a result** — "semantic context adds nothing beyond behavioral telemetry" would be a perfectly good finding, as long as we measure it honestly.

## 1.4 The constraint that determines the whole architecture

This is the single most important thing to understand.

```text
  Scheduler decision           ~1-10 microseconds
  Context switch               ~1-5 microseconds
  Timeslice                    ~1-10 milliseconds
  ------------------------------------------------
  One LLM inference            ~500-3000 milliseconds     <-- 5-6 orders of magnitude slower
```

**An LLM cannot make scheduling decisions.** In the time it takes to answer once, the scheduler has made hundreds of thousands of decisions.

So the LLM does not produce *decisions*. It produces **policy** — a handful of parameters that shape how the deterministic scheduler behaves:

```json
{ "scheduler": "MLFQ", "timeslice_ms": 10, "num_queues": 4, "boost_interval_ms": 100 }
```

A slow outer loop turns the dials; a fast inner loop keeps running at its own speed.

```text
   +---------------------------------------------------+
   |  SLOW LOOP  (seconds)                             |
   |                                                   |
   |   telemetry  -->  LLM  -->  validator  -->  policy|
   |                                                   |
   +--------------------------+------------------------+
                              |
                              | parameters only
                              v
   +---------------------------------------------------+
   |  FAST LOOP  (microseconds)                        |
   |                                                   |
   |   kernel scheduler: pick next process, run, repeat|
   |                                                   |
   +---------------------------------------------------+
```

If this separation ever breaks, the project does not work. Everything else follows from it:

- **Constrained output** — the LLM can only fill in a fixed set of fields, each with hard bounds. It cannot invent new powers for itself.
- **Validation** — a policy of `timeslice_ms: 0` would freeze the system. Every field gets schema-checked and clamped before it reaches the scheduler.
- **Fallback** — if the LLM is slow, unreachable, or returns garbage: keep the previous policy, and after repeated failures fall back to a conventional scheduler. The system must never depend on the LLM being available.

## 1.5 Stale policy: the direct consequence of that delay

If the LLM takes seconds to answer, then by the time a policy arrives it was computed from a system state that no longer exists.

```text
  t=0.0s   telemetry snapshot taken        ──┐
  t=0.0s   compiler is burning CPU           │
                                             │  LLM inference (~2s)
  t=1.2s   compiler finishes (!)             │
  t=1.5s   test runner starts                │
  t=2.0s   policy arrives  ──────────────────┘
           "prioritize the compiler"
           -> a policy for a process that no longer exists
```

This is the classic control-theory problem of **dead time**: a controller in a delayed feedback loop always reacts to the past. Same as a shower with long pipes — you turn up the hot water, nothing happens, you turn it up more, and five seconds later you are scalded. Delay plus aggressive correction produces **oscillation**.

### Why this is survivable

The distinction that saves us is **stale decision vs. stale policy**:

- A stale *decision* — "run PID 4821 next" — is meaningless or dangerous if that process is gone.
- A stale *policy* — "MLFQ, 4 queues, 10 ms timeslice, interactive boost" — is suboptimal but **still a completely valid scheduler configuration**.

A slightly mistuned MLFQ is just a slightly mistuned MLFQ. Nothing breaks. **The floor is "an ordinary scheduler," not "a broken system"** — and that floor is exactly what the slow-loop/fast-loop split buys us.

So the question is never *does it break*. It is *how much does it cost*.

### Three real risks that remain

**1. Instance-scoped policy.** Any policy field keyed by PID is a landmine — PIDs identify *instances*, instances die, and PIDs get recycled into unrelated processes. Policy should target **classes**, not instances:

```json
{
  "class_rules": [
    { "match": "cmdline~=cc1plus|clang", "class": "user_blocking", "boost":  2 },
    { "match": "name==updatedb",         "class": "background",    "boost": -3 }
  ]
}
```

A compiler can exit and restart and the policy stays meaningful. This is the most fundamental defense against staleness, and it needs to be settled when we freeze the schema.

**2. Oscillation.** Standard mitigations, all cheap:
- rate-limit how far a policy can move in one step (hysteresis)
- send a **windowed summary** rather than an instantaneous snapshot, so the LLM sees trend instead of noise
- enforce a minimum hold time before a new policy can replace the current one

**3. No validation at apply time.** Stamp each policy with the telemetry snapshot it was derived from, and check it on arrival:

```text
  policy derived from:  seq=142, processes {bash, cc1plus, updatedb}
  current state:        seq=147, processes {bash, pytest,  updatedb}
  -> process set changed substantially -> apply weakly, or discard
```

This is optimistic concurrency control (compare-and-swap) applied to scheduling policy: version stamp, verify at apply time, reject on mismatch.

### A more interesting direction

If we cannot remove the delay, we can design policy that **assumes** it. Instead of constants fitted to the current instant, the LLM emits conditional rules covering the next few seconds:

```json
{
  "base": { "scheduler": "MLFQ", "timeslice_ms": 10 },
  "conditional": [
    { "if": "cc1plus exits",        "then": "shift boost to whatever wakes next" },
    { "if": "interactive idle >5s", "then": "raise background quota" }
  ]
}
```

The kernel can then adapt inside the fast loop without waiting for the next LLM call — the same idea as a Smith predictor in control theory.

**The honest catch:** the more expressive those conditional rules get, the closer the design drifts toward the `rule_adaptive` baseline. At the limit, the LLM merely authored some rules and a rule-based scheduler did the work — which makes "what did the LLM actually contribute?" a much sharper question. Worth deciding deliberately rather than drifting into.

### This is a measurement target, not a bug

Staleness should be instrumented, not just mitigated. Two metrics to add:

- **Policy age** — how old was the underlying data at the moment a policy took effect
- **Staleness regret** — re-run the same workload against a zero-delay oracle (policies applied instantly) and diff. That number is exactly what the delay cost us.

And build **phase-shift workloads at several speeds** — workload character changing every 30 s, every 5 s, every 1 s. That yields a result of the form:

> *"Semantic scheduling only pays off when workload phases last at least N× the LLM round-trip."*

That is a far better finding than "it worked" or "it didn't," and it maps directly onto research question 3 (how often should the LLM be consulted).

## 1.6 The three pieces

```text
   +--------------------+                    +---------------------+
   |    SIMULATOR       |   telemetry JSON   |   POLICY DAEMON     |
   |    (C++)           | -----------------> |   (Python)          |
   |                    |                    |                     |
   |  virtual clock     |                    |  prompt building    |
   |  processes         |                    |  LLM call           |
   |  event loop        | <----------------- |  validate / clamp   |
   |  schedulers:       |   policy JSON      |  fallback logic     |
   |   RR / Priority    |                    |                     |
   |   MLFQ / adaptive  |                    |  (or mock generator,|
   |   policy-driven    |                    |   no LLM needed)    |
   +--------------------+                    +---------------------+
             |
             | run logs
             v
   +--------------------+
   |  BENCH HARNESS     |
   |  (Python)          |
   |                    |
   |  scheduler x       |
   |  workload x seed   |
   |  -> metrics, plots |
   +--------------------+
```

**Why the language split:**

| Component | Language | Reason |
|---|---|---|
| Simulator | **C++** | Logic carries over if we later port to a real kernel (xv6 / `sched_ext`). Kernel-land is C/C++ by default |
| Policy daemon | **Python** | We will edit prompts fifty times a day. Also where the LLM SDKs live |
| Bench harness | **Python** | pandas + matplotlib. Not really debatable |

**The two sides talk over JSON across a process boundary** (unix socket or stdin/stdout). This matters more than it looks: if we later replace the simulator with a real kernel, **the daemon does not change at all**. The C++ side gets swapped out; the protocol stays. Starting with a simulator is therefore not throwaway work — it is the migration path.

## 1.7 Why a simulator first

The original roadmap started with "boot, interrupt handling, memory management, context switching." That is a full semester-long OS course project on its own, and finishing it answers **none** of our research questions. Our stated non-goals already say we are not building a production OS.

Three viable starting points:

1. **Userspace simulator** — simulate processes, advance a virtual clock. Fastest iteration, easiest metric collection, no kernel debugging. Less "real."
2. **xv6** — MIT's teaching Unix. Boot, interrupts, and context switching already work; its scheduler is ~100 lines of round robin and is easy to replace.
3. **Linux `sched_ext`** — lets you write a scheduler in BPF and plug it into a real running kernel. Built exactly for pluggable schedulers. Real, but has a learning curve.

**Suggested path: start at (1), get an answer to the research question, then port to (2) or (3) if results justify it.** If the simulator shows semantic context does nothing, we learn that before spending three months on kernel work.

## 1.8 Where the experiment actually lives

The workload definitions are the experiment. Roughly:

```yaml
name: interactive_vs_batch
user_intent: "I'm actively using the terminal. The compile should finish
               reasonably fast. The indexer doesn't matter."
processes:
  - name: bash
    cmdline: "/bin/bash"
    pattern: { type: interactive, cpu_burst_ms: [1,5], io_wait_ms: [200,2000] }
  - name: cc1plus
    cmdline: "cc1plus -O2 render.cpp"
    pattern: { type: cpu_bound, total_cpu_ms: 8000 }
  - name: updatedb
    cmdline: "/usr/bin/updatedb"
    pattern: { type: io_heavy, cpu_burst_ms: [2,10], io_wait_ms: [5,20] }
```

Note the information asymmetry, which is the core of the experimental design:

- `name`, `cmdline`, `user_intent` — **visible to the LLM only.** No other scheduler gets them.
- `pattern` — **visible to the simulator only.** The LLM never sees ground truth.

If the LLM wins, semantic information earns its keep. If it doesn't, behavioral observation was already enough. Either way we get an answer.

## 1.9 Proposed folder structure

> ⚠️ **AI-generated draft, not a decision.** This was produced by an LLM as a starting point for discussion. Treat it as a sketch of the moving parts, not as a structure anyone has committed to. Expect it to change once we start writing code.

```text
llm-os/
├── sim/                          # C++ — the virtual OS
│   ├── clock.hpp                 # virtual clock / event queue
│   ├── process.hpp               # PCB: state, burst pattern, metadata
│   ├── workload.cpp              # trace file -> processes
│   ├── engine.cpp                # main loop
│   ├── telemetry.cpp             # periodic snapshot -> JSON
│   ├── ipc.cpp                   # socket to the daemon
│   └── sched/
│       ├── scheduler.hpp         # the common interface
│       ├── round_robin.cpp
│       ├── priority.cpp
│       ├── mlfq.cpp              # the real baseline
│       ├── rule_adaptive.cpp     # adaptive WITHOUT an LLM — ablation
│       └── policy_driven.cpp     # MLFQ whose parameters are injected
│
├── daemon/                       # Python — policy generation
│   ├── main.py                   # socket loop, timeouts, lifecycle
│   ├── prompt.py                 # telemetry -> prompt
│   ├── llm.py                    # API call, retries
│   ├── schema.py                 # policy shape
│   ├── validator.py              # validate / clamp / fallback
│   └── mock.py                   # fake generator, no LLM required
│
├── workloads/                    # experiment scenarios
│   ├── interactive_vs_batch.yaml
│   ├── phase_shift.yaml          # workload character changes mid-run
│   └── ...
│
├── bench/                        # Python — experiment harness
│   ├── run_matrix.py             # scheduler x workload x seed
│   ├── metrics.py
│   └── plot.py
│
└── protocol/
    ├── telemetry.schema.json     # kernel -> daemon
    └── policy.schema.json        # daemon -> kernel
```

Two files in here are worth calling out even at draft stage:

- **`sched/rule_adaptive.cpp`** — an adaptive scheduler with no LLM, just rules. This is the scariest baseline in the project. If twenty lines of heuristics match what the LLM does, our conclusion flips. We want this baseline to be strong.
- **`daemon/mock.py`** — a policy generator that needs no LLM. It lets the simulator side and the prompt side develop independently instead of blocking on each other. Worth building early.

---

# Part 2 — Ownership and Shared Decisions

## 2.1 Areas

### 인경민 — simulator / kernel side

The virtual OS itself: clock, processes, event loop. All the scheduler implementations, including the three baselines (Round Robin, Priority, MLFQ) and the policy-driven variant. The telemetry extraction side — whatever the "kernel" reports outward.

If we later port to a real kernel (xv6 or `sched_ext`), that lands here too.

### 박이안 — policy generation

Turning telemetry into a prompt, calling the LLM, deciding what context is worth including and what it costs in tokens. Evaluating whether generated policies are any good.

Also **the non-LLM adaptive scheduler**. Putting the strongest counter-hypothesis in the hands of the person arguing for the LLM keeps the result honest — you want to attack your own claim as hard as you can before someone else does.

### 인지오 — boundaries and experiment infrastructure

The communication layer between the two worlds. Policy validation: schema checking, clamping, the fallback state machine, and tracking **provenance** — whether a given policy was pure LLM output, clamped, or a fallback. Without that, a good result is unattributable; we would not know whether the LLM did well or the fallback did.

Also the mock policy generator, and the entire bench harness: running the experiment matrix, computing metrics, producing the results.

### Why it splits this way

The classic failure mode for a three-person project is *everyone builds their piece and integrates in the final week.*

This layout puts **every integration point in one person's hands** — the C++ end of the wire, the Python end, and the validator in between all belong to 인지오. Integration becomes a daily activity rather than a late-semester event, and the other two only need to honor their own interface.

The mock generator does the same thing from the other direction: it decouples 인경민 and 박이안 so neither is waiting on the other to have something runnable.

## 2.2 Decisions nobody makes alone

1. **The shape of the two protocols** — what the kernel reports, and what comes back as policy. 인지오 drafts, all three agree. The policy fields in particular are *the complete set of powers the LLM has over the system* — that is not a one-person call.

   Sub-decision, from §1.5: **policy must be class-scoped, not instance-scoped.** No PID-keyed fields. We need to agree on how a class rule expresses matching, and whether policy carries conditional rules at all — the latter has real consequences for how the `rule_adaptive` comparison reads.

2. **The scheduler interface** — changing it affects all three of us.

3. **Telemetry snapshot interval** — 박이안 wants it frequent, the kernel side worries about overhead, 인지오 worries about log volume. Related: whether telemetry carries an instantaneous snapshot or a windowed summary, which is both a staleness question and a prompt-design question.

4. **Metric definitions** — e.g. is "response time" measured arrival→first-run or arrival→completion? If this is vague, every interpretation of our results collapses. Also whether we commit to *policy age* and *staleness regret* from §1.5, since the second one requires building a zero-delay oracle mode into the simulator.

5. **Workload scenarios** — this is the experimental design itself. Should include phase-shift variants at several speeds so staleness cost is measurable rather than assumed.

6. **What information the LLM is allowed to see** — process name, command line, and user intent are in; the simulator's ground-truth burst pattern is out.

Point 6 should be written down explicitly. When results come out ambiguous there will be a temptation to "just give the LLM a bit more context," and without a recorded baseline the experiment loses its meaning.

## 2.3 One operating rule

**Freeze the protocol early.** Once we agree on v1, changes require all three of us plus a changelog entry.

Three people writing against three slightly different assumptions about the same interface, then discovering it at integration time, is exactly how projects like this fail.

---

# Part 3 — What to Study

Assumption: everyone has solid SWE fundamentals and DSA. Nobody has deep OS background.

This is a topic list, not a syllabus. The point is to know what the unknowns are.

## 3.1 Shared — everyone needs these

**Process fundamentals**
- What a process is from the kernel's point of view (the PCB, and what fields live in it)
- Process states and the transitions between them: ready / running / blocked
- Why a process blocks, and what wakes it up
- Context switching: what actually gets saved and restored, and what it costs

**How the kernel keeps control**
- Timer interrupts, and why a timeslice can exist at all
- Preemptive vs. cooperative scheduling
- The kernel/userspace boundary and how they communicate

**Scheduling algorithms**
- FIFO, Shortest Job First, Round Robin — and why SJF is optimal but unbuildable
- Priority scheduling, and the starvation problem
- **MLFQ** — queues, demotion on timeslice exhaustion, periodic priority boost. This is the one to actually understand, not skim
- CPU-bound vs. I/O-bound workloads, and how a scheduler infers which is which

**Measuring schedulers**
- Turnaround time, response time, throughput, fairness, starvation — precise definitions of each
- Percentiles (P95/P99) and why tail latency matters more than the mean for interactive work
- Experiment hygiene: seeded randomness, repeated runs, reporting variance, changing one variable at a time

**Discrete-event simulation**
- The core technique: a priority queue of future events, jump the clock to the next one, process, repeat
- Virtual time vs. wall-clock time
- Underrated — probably none of us has built one, and it is the foundation of the whole simulator. Mechanically it is just a heap.

**Feedback control, conceptually**
- Control loop, dead time, oscillation, hysteresis, damping
- No math needed — just enough shared vocabulary to discuss §1.5 without talking past each other

## 3.2 인경민 — simulator / kernel side

- Everything in 3.1, but at implementation depth rather than reading depth
- MLFQ's exact rules — they are subtle and easy to get subtly wrong
- Discrete-event engine design: event types, clock advancement, tie-breaking
- C++ patterns for this: priority queues, virtual interfaces for pluggable schedulers, RAII
- How real systems do it — Linux CFS/EEVDF at a conceptual level, for context

Later, only if we port to a real kernel:
- Kernel boot, interrupts, and context switching in a small teaching kernel
- BPF and pluggable scheduler interfaces in modern Linux

## 3.3 박이안 — policy generation

- Everything in 3.1, with MLFQ solid — you are describing scheduling to an LLM, so you need to know what the knobs do
- Structured output from LLMs: JSON mode, constrained decoding, tool/function calling, schema enforcement
- Prompt evaluation as a methodology: fixed eval sets, ablations, repeated runs. LLMs are nondeterministic, so one good output means nothing
- Context construction: what telemetry to include, summarization, token budgeting
- Model size vs. latency as a tradeoff — this is directly the staleness question in §1.5, and worth running as an experiment
- Rule-based adaptive control: classic adaptive heuristics, since you own the non-LLM baseline and it should be as strong as we can honestly make it
- Related work worth knowing: classical autotuning (database knob tuning, compiler flag search) — the same problem shape, pre-LLM

## 3.4 인지오 — boundaries and experiment infrastructure

- Everything in 3.1, plus enough of the PCB to know which telemetry fields a kernel could realistically produce
- JSON Schema properly: bounds, `additionalProperties`, versioning, evolving a contract without breaking both sides
- IPC between C++ and Python: unix domain sockets, message framing, blocking vs. non-blocking, timeouts
- Serialization across a language boundary and where it goes wrong
- Validation as an explicit state machine: `fresh / clamped / held / fallback`, with transitions and counters
- Provenance tracking — attributing every applied policy to a state, or the results are uninterpretable
- Optimistic concurrency control: version stamps, compare-and-swap, validating at apply time. This is exactly the mechanism for rejecting stale policies
- Rate limiting and hysteresis as concrete mechanisms, since you own the staleness mitigations
- Reproducible experiment harnesses: config-driven matrices, seeded runs, tidy data output, plotting

## 3.5 What nobody needs to study

Worth saying out loud, because OS material is bottomless and the roadmap looks more intimidating than it is:

- Virtual memory, paging, TLBs
- File systems, disk layout, journaling
- Concurrency primitives beyond casual familiarity
- Bootloaders, BIOS/UEFI, device drivers
- Anything about making a *fast* kernel

We are touching **one subsystem**. That is the entire OS surface area of this project.

## 3.6 Sequencing

Scheduling algorithms and metrics first, together, before the protocol meeting. Most of the shared decisions in Part 2 are unanswerable without MLFQ in everyone's head.

Getting three people onto the same page about one algorithm is cheap. Discovering mid-semester that we each meant something different by "priority" is not.
