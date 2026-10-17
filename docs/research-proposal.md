# A Semantic Recognition Layer for Operating Systems
> Status: draft — for team review · Created 2026-08-15 · Updated 2026-10-17

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

Operating systems are full of hardcoded semantic knowledge — tables where a human wrote down what things *are*. CachyOS, a Linux distribution, installs and enables by default a community-maintained catalogue that gives each listed process name a priority class (`ananicy-rules`, run by ananicy-cpp; `cachyos-settings`). Special-case rules key off process names. Scheduling classes wait for programs to declare their own nature. Windows and macOS ship a Game Mode for the game in the foreground, and how either recognises a game their documentation does not state (`gamemode-docs`, `apple-gamemode`). Every name table of this kind is a person, at some point, enumerating meaning by hand.

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
| **Validation** | One driver, built and measured. Does the signal actually improve CPU scheduling, against the name-keyed catalogue a shipping Linux distribution enables by default (CachyOS's `ananicy-rules`, run by ananicy-cpp) and the strongest name table in its design? |
| **Future work** | Additional drivers. Each is a thin adapter; the recognition layer does not change |

The central claim under test:

> **The meaning of a workload lives in the combination of processes, not in any single one of them. That combination cannot be enumerated in a lookup table, and reading it requires knowing what the software is for — knowledge a language model already has and an operating system does not.**

The model's job is not to pick a label from a menu. It reads a process set, works out the situation, and explains its reasoning — so that we can tell a correct decision from a lucky one.

A negative result is a publishable result. "The model reads the situation correctly but CPU scheduling does not improve" is a clean finding: it tells us the existing behavioural heuristics were already sufficient *for that consumer*, which is information the architecture needs and which does not invalidate it.

---

# Part 1 — Background for readers with no OS experience

This section assumes no operating systems background. Readers who already know what MLFQ is can skip to [Part 2](#part-2--the-gap-we-are-targeting).

## 1.1 What a scheduler does

Each CPU runs one task at a time (the kernel's CFS design document, `linux-sched-cfs`). An idle, locked Ubuntu 24.04 desktop session on the dataset's machine holds about 66 processes and 320 threads; the whole machine, the runner's own services among them, about 125 processes and 500 threads beside some 115 kernel threads (`meas-ci:session:2026-09-24`, the session census). The scheduler chooses among those ready to run, so the kernel must continuously answer one question:

> **On this core, for the next few milliseconds, who runs?**

The component that answers is the **scheduler**. Two facts about it shape everything in this proposal.

**It runs constantly.** The kernel switches tasks hundreds to thousands of times a second on each CPU, more under some loads: on one CPU running one of the dataset's programs, 13 to 12 497 switches a second over the repeats the measurement campaigns pooled, the median program phase 422, two phases above 10 000 (SteamCMD's download) — each switch at least one pick of the next task. A pick, the fair class's `pick_next_task_fair`, takes about half a microsecond on the dataset's machine (`meas-ci:costs:2026-10-08`). A slow scheduler *is* the overhead.

**It cannot see the future.** The kernel does not know whether a process will finish in 5 ms, run for another 30 seconds, or immediately go to sleep waiting on the disk. Shortest job first minimises average turnaround when every job arrives at once, runs to completion, uses only the CPU and has a known length, and shortest time-to-completion first does so without the simultaneous arrival — turnaround being the only metric (`ostep` §7.4–§7.6). A general-purpose OS usually knows little of a job's length (§7.9).

No scheduler knows how long a job will run; each acts on what it has — the CPU a task has used against its fair share (CFS, EEVDF; `linux-sched-eevdf`), what a program or its unit declares (a scheduling class, a QoS class, a requested slice; `man-sched`, `apple-qos`), and recent behaviour (MLFQ's demotion, `ostep`; Windows' boosts, `win-priority-boosts`; XNU's usage decay, `xnu-sched`).

## 1.2 Interactive vs. batch

The most important distinction a scheduler makes is between two kinds of work.

**Interactive** processes have a human waiting in front of them — a text editor, a browser, a mail composer. They spend most of their time asleep: you press a key, the process wakes, works, and goes back to sleep waiting for the next keystroke. Per key the dataset measured a few milliseconds of CPU for an office editor, a browser field and a mail composer — medians 3.23 ms for LibreOffice Writer, 4.07 ms for a Chrome text field and 4.65 ms for Thunderbird's compose window, 0.2–1.4 % of their CPU while typing — and tens of milliseconds where an IDE's language server re-checks the file: 79.7 ms for VS Code, its TypeScript server re-checking a file being filled with letter runs, 14–45 % of its CPU (each entry's `input_run`, `dataset/archetypes.yaml`). These are the application's process tree on one CPU of the dataset's AMD EPYC 7763 runner, the X server's drawing left out, SWELL-KW keystrokes replayed (`swell-icmi14`).

**Batch** processes have nobody waiting on each step — a compile, a backup, a file indexer, a video encode — and run long. Every batch job the dataset measured keeps a CPU busy, using nearly every cycle while it works: a kernel build at 99.7 % (the CPU's busy share), a video encode at 99.9 % and a backup at 99.4–99.5 % (saturation over the job), a first index of a home at 88–91 % once it starts indexing. The indexer runs short by count (a median 0.06 ms between blocks) yet 84–85 % of its CPU past a 10 ms slice. What sets the indexer and the backup apart is that they declare themselves background — the indexer `SCHED_IDLE` at nice 19 (`tracker-miners`), the backup in the idle class (`deja-dup`) — and the indexer first waits out a 15 s start. An eight-second compile computes for eight solid seconds.

```text
  soffice.bin (LibreOffice Writer, typing)
  ▓  ░░░░░░░  ▓  ░░░░░░░░░░  ▓  ░░░░░  ▓  ░░░░░░░░░  ▓
     short burst, long sleep, repeat

  cc1 (one object of a -j8 kernel build)
  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░
     runs continuously until finished

  ▓ = using CPU     ░ = waiting or finished
```

They want opposite treatment. Interactive work needs to *start* quickly — total runtime barely matters, but a delay near 100 ms before the screen responds is where these sources place perceptible lag: Miller's guideline puts a keystroke's echo at 0.1–0.2 s and a control's own response at 0.1 s, his "best calculated guesses" (`miller-fjcc68`), and Deber et al. measured a mean detection threshold of 96 ms for tapping on an indirect touch surface, near "the textbook threshold of 100 ms" (`deber-chi15`). Batch work needs *total time*, and each interruption costs it the switch itself and the cache state the program built, by an amount that depends on whether its data still fit the cache and on its access pattern — Li, Ding & Shen measured 4.2–8.7 µs while the data fit the L2 cache, 38.6–203.2 µs beyond it, and up to 1 496 µs with a 128-byte stride (`li-expcs07`).

MLFQ's resolution, as OSTEP describes most of its variants, gives interactive work high priority but a short turn on the CPU and batch work low priority but a long turn when it does get one — 10 ms or less at the top, hundreds of milliseconds at the bottom (`ostep` §8.5; Solaris's table, as OSTEP describes it, 20 ms to a few hundred; CTSS's 2^ℓ quanta at level ℓ, `corbato-sjcc62`). It is not every scheduler's: Linux's EEVDF selects the task with the earliest virtual deadline, which lets a task with a shorter slice run sooner, a task requesting its slice through `sched_setattr()` (`linux-sched-eevdf`).

## 1.3 MLFQ, our baseline

**MLFQ (Multi-Level Feedback Queue)** is our baseline because it is the textbook form of classification by behaviour (`ostep` ch. 8; `corbato-sjcc62`), not a family every OS ships: Windows' priority boosts and decay are an MLFQ form (`win-sched-priorities`, `win-priority-boosts`; OSTEP names Windows NT); macOS's Clutch/Edge scheduler is EDF over QoS buckets, with a variation of FreeBSD's ULE across thread groups and Mach's usage-decayed priority at the thread level (`xnu-sched`); Linux's default is EEVDF (`linux-sched-eevdf`), proportional share (`eevdf-tr95`). MLFQ maintains several priority queues and moves processes between them by watching behaviour — OSTEP's revised rules, which the simulator implements:

- Used up your allotment at this level — a slice's worth of CPU, counted across every sleep along the way? → demoted to the next queue (Rule 4)
- Gave up the CPU before using it up? → stay at your level, the CPU you used still counted. The first version reset the allotment on every sleep (Rule 4b), which a program could game by sleeping just before its slice ran out (`ostep` §8.4)
- Every boost interval, everything returns to the top queue, so no job starves (Rule 5)

This is genuinely clever, and it explains why the diagram above works as a classifier. On the dataset's machine an editor's threads (LibreOffice Writer's `soffice.bin`, SWELL-KW keystrokes; `meas-ci:interactive:2026-09-18`) run a few hundredths of a millisecond between blocks (median 0.046 ms; a few milliseconds at the 99th percentile), while `cc1` runs a median 368 ms of CPU from its start to its exit, unblocked in 99.4 % of object jobs (`cc1_step_1`, a warm `-j8` linux-6.6 build; `meas-ci:build:2026-09-18`): the first gives up a 10 ms slice almost at once, the second uses every slice. A few observations are enough to tell them apart.

**MLFQ is our real baseline.** Beating round-robin proves nothing.

## 1.4 What MLFQ cannot see

MLFQ observes *behaviour*, never *meaning*. A compiler and a training run both look CPU-bound. A chat client sleeps often at low CPU; the file indexer does not once it is indexing — about nine-tenths busy from Tracker's `Initializing`. The training run and the indexer both keep a CPU busy, and differ in how their work is cut and in the class they declare.

One pair our experiment is built around: **a game download the user started, and an upgrade nobody started** — the dataset's P2 pair: `c2-p2a`, the install of another game the user begins during play (`game-download`), against `c2-p2b`, Ubuntu 24.04's stock unattended upgrade (`package-upgrade`; `unattended-upgrades`). Both keep a CPU 91–99 % busy beside the game. They differ in how their work is cut (163 µs against 1.8 ms between voluntary blocks), in structure (one process of 83–84 threads against 916 short-lived processes), in size (727 s of CPU against 26 s) and in declared priority (the wanted download runs three quarters of its CPU at nice 10; the upgrade's nice 19 covers 2.67 % of its CPU). Their correct treatments are opposite — the download throttled by the batch class's cap, its waits judged by the 30 s guard, not guaranteed (§4.7); the upgrade freely deferred. The pair tests what recognition adds over a behavioural and declared-priority baseline.

Whether the user wants the work is not in its behaviour, and its declared class does not settle it; the *name*, read with what is known of the software, carries it. What recognition adds over behaviour and declared class is what the experiment measures.

---

# Part 2 — The gap we are targeting

## 2.1 The mechanism already exists

An important correction to an assumption that is easy to make: **operating systems are not stuck with one static scheduling algorithm.** The machinery for varying scheduler behaviour is already present and shipping.

| System | Mechanism | How the decision is made |
|---|---|---|
| Linux | Scheduling policies (`SCHED_OTHER`, the default; `SCHED_BATCH`, `SCHED_IDLE`, `SCHED_FIFO`, `SCHED_RR`, `SCHED_DEADLINE`; `SCHED_EXT` since 6.12, the row below) | Declared by the program itself, its systemd unit (`CPUSchedulingPolicy=`, `Nice=`) or a wrapper (`chrt`), through `sched_setscheduler(2)`, or for `SCHED_DEADLINE` `sched_setattr(2)`; an unprivileged thread may only lower its priority or leave real time, its real-time priority capped by `RLIMIT_RTPRIO`, and `SCHED_DEADLINE` needs `CAP_SYS_NICE` (`man-sched`, `man-sched-setattr`) |
| Linux | `sched_ext` | Pluggable schedulers loaded from userspace as BPF programs |
| macOS | Quality-of-Service classes (`user-interactive`, `user-initiated`, `utility`, `background`) | Developer declares it in code; work left undeclared is treated as `default` (`apple-qos`; `apple-energy-guide`, 2016-09-13) |
| macOS (Sonoma 14 or later, Apple silicon) | Game Mode | Turns on when a game enters full screen (`apple-gamemode`); from macOS 26 an app declares support with `LSSupportsGameMode` (`apple-lssupportsgamemode`); how the system recognises a game is not documented |
| Windows | Game Mode | On by default for most games, the mechanism undocumented; an optional `expandedResources` declaration; foreground and focus required (`gamemode-docs`). While a game runs, Windows Update's driver installations and restart notifications are held back (`xbox-gamemode`) |
| Linux | Feral GameMode daemon | The game requests the mode through the library (`gamemode_request_start()`) or an integrating launcher, or the user launches it under `gamemoderun`; an optional user-set whitelist only restricts which requesters are accepted (`feral-gamemode`) |

Any proposal that claims "existing schedulers are static" will be corrected in the first five minutes of a review. We should state this correctly and build on it. The `sched_ext` row matters for a second reason: it is the path by which the CPU driver could run on a real kernel the depicted desktop already carries — Ubuntu 24.04's HWE kernel 7.0.0-34 sets `CONFIG_SCHED_CLASS_EXT=y` for amd64 (`ubuntu-hwe-config`; `schedext-docs`) — with operators running sched_ext schedulers in production, as Meta's speakers report it (`schedext-lpc24`, `lu-lpc25`), and SteamOS shipping LAVD as a scheduler the user selects (`steamos-lavd`). No algorithm or executor of this project has a sched_ext implementation — the simulator models one CPU lane — and the port is future work (Part 10); we intend the simulator work as a prototype of something shippable rather than a purely academic exercise.

## 2.2 The actual limitation is the list

The real problem is not the absence of mechanism. It is how the mechanism gets triggered:

- **Cooperation.** Linux's scheduling classes and macOS's QoS classes wait for a declaration: on Linux from the program itself, its installed unit or a wrapper; on macOS from the developer in code (`man-sched`, `apple-qos`). Few make one: of the 1 438 Debian unstable source packages that install a systemd service unit, 56 (3.9 %) carry `Nice=`, `IOSchedulingClass=` or `CPUSchedulingPolicy=` — a floor, since a class set in code or by a wrapper is not counted — 40 of them only lowering their priority and 16 only raising it, mostly latency-bound daemons, a raise not by itself an over-claim (`debian-sid-indexes`, `debian-code-search`). Background tools differ: LocalSearch (Tracker) and Baloo set background classes on themselves (`tracker-miners`, `baloo`); Déjà Dup wraps its backup in `chrt --idle 0` (`deja-dup`); ClamAV, borg and restic declare nothing, restic's documentation leaving `nice` and `ionice` to the user (`clamav`, `borg`, `restic`). On the depicted Ubuntu 24.04 desktop `updatedb` is not installed (`ubuntu-desktop-manifest`). The plocate 1.1.19 a user installs declares only the idle I/O class, its CPU priority the default (`plocate-ubuntu`), so its `updatedb` does not volunteer that it is background work for the CPU, and does for I/O. Debian's units — plocate's from 1.1.23 and findutils' `locate.service` — declare both (`plocate-debian`, `findutils-debian`), and Ubuntu's findutils `locate` runs its `updatedb` from a daily cron job at nice 10 in the idle I/O class (`locate-ubuntu`). A declaration is fixed per program by its author or packager. Apple's scheduler document gives priority inflation across the platform — individual subsystems raising their priority to avoid starvation and timesharing with unrelated threads — as an artifact of the traditional Mach scheduler and a motivation for the Clutch scheduler (`xnu-sched`).
- **Enumeration.** A name-keyed catalogue covers what someone wrote a rule for. CachyOS installs and enables by default ananicy-cpp with a community-maintained catalogue of rules keyed on process names (`ananicy-rules`, `cachyos-settings`); software the catalogue does not carry gets no rule.
- **Binary granularity.** Game Mode is on or off. There is no "gaming while streaming, so the encoder keeps its frame deadline" mode (an encoder that falls behind skips frames, which OBS counts and reports; `obs-studio`).

So the sharpened version of our research claim:

> Operating systems already accept that knowing *what the user is doing* is useful — they built the mechanism. What they lack is a way to figure it out without a hand-written name table or developer cooperation. Can an LLM supply that, once, for the whole system?

## 2.3 Why the meaning is in the combination

The critical property that makes this a reading problem rather than a matching problem: **no individual process reveals the situation.**

| Running processes | Situation | Scheduling implication |
|---|---|---|
| LoL, Discord, Chrome | Gaming | Frame latency is everything; suppress background work hard |
| Discord, Chrome | Casual browsing | Nothing special; ordinary MLFQ |
| LoL, Discord, Steam installing another game the user just started | Gaming, transfer the user wants | Same as gaming, but the download is throttled by the batch class's cap, its waits judged by the 30 s guard, not guaranteed |
| LoL, Discord, Ubuntu's unattended upgrade | Gaming, work the user did not ask for | Both jobs keep a CPU busy beside the game; the correct answer is the opposite |
| LoL, Discord, OBS | Gaming while streaming | OBS records and streams, encoding as it goes, so its encoder has a deadline per frame; an encoder that falls behind skips frames, which OBS counts and reports ("Skipped frames due to encoding lag"; `obs-studio`, `obs-kb-encoding`) |
| `make`, `cc1` ×8 (a `-j8` build), `code` | Compiling | Throughput matters; the editor still needs to feel alive |

Discord appears in five of these and means something different each time. Chrome the same. Rows 3 and 4 are the sharpest pair in the table: the same foreground beside two background jobs that both keep a CPU busy, and opposite correct policies.

With `n` possible processes there are `2^n` possible combinations. A lookup table cannot cover that space.

## 2.4 Why this needs world knowledge

Reading that table requires knowing things about software that an operating system has no way to learn on its own: that OBS records and streams, encoding as it goes, so its encoder has a deadline per frame (`obs-studio`); that a Steam download beside a game may be the install of another game the user just started or an update nobody started — Steam queues updates itself and by default pauses queued downloads when a game launches (`steam-downloads`), while an install begun during play starts at once (`steam-for-linux-8821`), so the name `steam` alone does not settle which; that Ubuntu's unattended upgrade is not something the user started; that `cargo build` compiles a Rust package and its dependencies, Cargo invoking `rustc` (`cargo-book`).

What a process is for, and whether the user is waiting on it, is not stated by its behaviour; its run shape and declared class are, and the experiment tests what recognition adds over them. None of that knowledge can be assembled by enumeration without recreating the name table's problem (§2.2) in a different place. It is, however, ordinary general knowledge — the kind of thing a language model has absorbed from pretraining without anyone assembling it for this purpose.

That is the specific capability we are testing. Not classification accuracy on a fixed menu of situations, but whether a model that already knows what software is for can turn that knowledge into a decision on a machine it has never seen.

## 2.5 What this replaces, and what it does not

This distinction determines the scope of every claim in the rest of the document, and getting it wrong invites an easy objection.

**Replaced: hardcoded semantic knowledge.** Hand-written name tables like the CachyOS catalogue (`ananicy-rules`). Special-case rules keyed on process names. Any table where a human wrote down what a piece of software *is*. These were already semantic judgements — they were simply frozen at authoring time and limited to whatever the author enumerated.

**Not replaced: the execution mechanism.** MLFQ's demotion rule, priority queues, timer interrupts, context switching. These are not stale knowledge waiting to be improved; they answer a different question on a different timescale.

```text
  LLM        →  what is this machine being used for   (seconds, meaning)
  Heuristic  →  who runs on this core right now       (microseconds, mechanism)
```

The gap in §4.1 is four to eight orders of magnitude across the settings measured and does not close with better models, because the kernel picks the next task hundreds to thousands of times a second per CPU, in about half a microsecond each, and inference cannot. Behavioural heuristics are therefore permanent residents of this design, not legacy to be cleared out. The recognition layer configures them; it does not replace them.

Stating this plainly makes the proposal narrower and considerably more defensible than "an LLM runs the OS."

---

# Part 3 — Research questions

**RQ0 — Measurability.** Before any model exists: does the choice of scheduling configuration change outcomes enough to measure on these workloads at all? A random recognizer is compared against perfect recognition, with no model in the loop. If a perfect recognizer scores close to a random one, no recognizer can demonstrate anything and every question below is unanswerable. Section 5.3 develops this. It requires no prompt, no model, and no API key, and it is the cheapest available falsification of the premise.

**RQ1 — Reading the situation.** Given the names of the running processes with their counts, and which one holds the window focus, can an LLM correctly work out what the system is being used for?

**RQ2 — Value.** Does correct reading produce measurably better scheduling than (a) no situation awareness, and (b) the name-keyed catalogue a shipping Linux distribution enables by default and the strongest name table in its design?

**RQ3 — Vocabulary sufficiency.** Is the shared signal — mode plus attributes — enough for a consumer to act well, or does the consumer need the model to hand it configuration directly? This is the architecture question: if the vocabulary is sufficient, drivers stay thin and new consumers cost nothing. Section 4.6 measures it.

**RQ4 — Timing.** One LLM answer took seconds on the hardware measured; the kernel picks the next task in about half a microsecond, hundreds to thousands of times a second per CPU (§4.1). How long must a situation last before semantic scheduling pays for its own latency?

**RQ5 — Instrument soundness.** Every conclusion about RQ2 and RQ3 is measured through the CPU driver's mapping table. If that table maps distinct situations to indistinguishable configurations, or maps them to configurations far from what the situation admits, a correct reading is discarded before it reaches the scheduler — and the result reads as a negative finding about the signal when it is a finding about the mapping. Three checks answer this, all without a model and all before the full matrix: whether different rows of the table yield different configurations; whether those configurations yield different metrics; and how far each row sits from the best configuration a search can find for that situation. The last of these is the gap between perfect recognition and perfect configuration, and a large gap invalidates the interpretation of every other result rather than merely weakening it.

RQ1 and RQ2 can come apart, and that is the most interesting possible outcome. "The model reads situations accurately but scheduling performance does not improve" tells us the existing heuristics were already sufficient for this particular consumer — a real result, and one the architecture survives.

---

# Part 4 — System design

## 4.1 The constraint that determines everything

```text
  Pick of the next task      ~0.5 µs        the fair class's pick, the dataset's machine
  Context switch             ~2.4 µs        lmbench lat_ctx, the dataset's machine
  Time slice                 0.5 ms–500 ms  per system (below)
  ---------------------------------------------------------------------------------
  One LLM answer             1.2–5.3 s      one consumer laptop (Apple M1 Pro, Metal)
                             14–43 s        four server vCPUs, no GPU
                             four to eight orders of magnitude slower than a pick
                             (six to seven on the laptop)
```

The pick is the fair class's `pick_next_task_fair`, traced per call at 0.80 µs under a pipe ping-pong and 0.89 µs under 80 messaging processes — upper bounds — and about 0.45–0.54 µs and 0.54–0.63 µs once the tracer's share is taken out; the switch, lmbench's `lat_ctx`, 2.38 µs, or 2.41 µs a switch with its wakeup by Li, Ding & Shen's subtraction on the ping-pong (`meas-ci:costs:2026-10-08`, one CPU of an AMD EPYC 7763). The slices: Linux's base slice 0.70 ms × (1 + log₂ of the online CPUs, counted up to 8) since v6.15, 2.1 ms on the runner's four CPUs (`linux-sched-fair`); `SCHED_RR`'s 100 ms on the runner's kernel (`meas-ci:sched:2026-10-07`); scx_lavd 0.5–5 ms with a boost to 500 ms, scx_rusty 20 ms or 1 ms (`scx`); MLFQ variants 10 ms or less at the top and hundreds of milliseconds at the bottom, Solaris's table 20 ms to a few hundred as OSTEP describes it (`ostep` §8.5). The answers are those of the latency note below. Each ratio is an answer on its machine over a pick on the dataset's machine: four to eight orders of magnitude across the settings measured and reported — the low end AKTS's reported 13.5 ms median for a single-digit answer from a 0.5B model on an A100 (`akts-arxiv26`) — and six to seven on a consumer laptop.

**An LLM cannot make scheduling decisions.** In the laptop's 1.19 s answer, one CPU of the dataset's machine running the median program phase switches about 500 times, and running SteamCMD's download about 14 900 times — each switch at least one pick — and a machine has several CPUs.

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

A note on the latency figure. A quantized 3–8B model answered one stand-in recognizer request of about 440–450 tokens in 1.2–3.0 s for the `system` block on one consumer laptop — an Apple M1 Pro with Metal; 2.3–5.3 s with reasoning first (`meas-local:m1pro-llm:2026-10-08`) — and in 14–36 s on four server vCPUs without a GPU, the 8B's reasoning-first answer 43.18 s (`meas-ci:costs:2026-10-08`). The `subsystems` block was not measured. Published figures elsewhere, as their pages compute them, are not short-prompt measurements: LocalScore's 0.88 s average time to first token for Llama 3.1 8B on a 12 GB RTX 3060 is the mean over submitted runs, each the mean of nine tests of 16–4 096-token prompts (`localscore`); Artificial Analysis's per-provider 72-hour medians of time to first token on a ~10 000-token prompt ran 0.66–1.14 s as read 2026-10-07 (`artificialanalysis`). The model is consulted only when the process set changes, which we assume is rare in real use — no source found measures how often a desktop's process set changes — so a latency of seconds delays a configuration, not a scheduling decision. Local inference is the deployment shape we measure against: the process list never leaves the machine (§4.8).

## 4.2 Runtime flow

```text
   process set changes (launch / user-close / focus move)
                │
                ▼
   ┌────────────────────────────────┐
   │  telemetry: process names,     │
   │  counts, focus holder          │
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
   │   + the batch class's cap       │
   └────────────┬───────────────────┘
                │
   ═════════════╪═════════════ nothing below this line involves the LLM
                ▼
   ┌────────────────────────────────┐
   │  scheduling loop, per CPU:     │
   │   100s–1000s of switches/s,    │
   │   each ≥ one pick of ~0.5 µs   │
   │   read current configuration   │
   │   pick next process, run it    │
   └────────────────────────────────┘
```

Three properties worth stating explicitly:

1. **No consumer blocks on the LLM.** While a query is in flight, the previous configuration stays active. On first boot, the default is plain MLFQ.
2. **Failure is invisible.** If the LLM is slow, unreachable, or returns garbage, we keep the current configuration. After repeated failures we fall back to plain MLFQ permanently. The system must never depend on the LLM being available.
3. **The model is re-queried on change, not on a timer.** Polling every 30 s asks the same question 120 times in an hour of play. How long play lasts depends on the game: on one World of Warcraft realm (TW-Light's Hope, Horde) the median avatar's average session was 1.8 h, its 5th–95th percentile 0.4–5.5 h (`wowah-mmsys11`, Table 4), while on one Counter-Strike server most sessions lasted minutes — a Weibull fit (shape 0.5, scale 20 min), whose median works out to about 9.6 min (our arithmetic) — and more than 99 % under 2 h (`chambers-imc05`). The daemon queries at every change of the set — the name → count multiset or the focus holder (`docs/data-contracts.md` §5); whether it needs a minimum hold time or hysteresis against flapping is open, measured first with no rule (§6.3, Part 7).

## 4.3 What the model produces

The proposal has two layers, and keeping them separate is what makes the architecture extensible.

```json
{
  "reasoning": "LeagueClient is a game running in the foreground, so frame
                deadlines dominate. The Steam process is downloading, most
                plausibly another game the user just started installing, so
                it should be throttled rather than deferred.",

  "situation": "Gaming, with a user-initiated download",

  "system": {
    "mode": "gaming",
    "background_wanted": true
  },

  "subsystems": {
    "cpu_scheduler": {
      "algorithm": "EDF",
      "params": { "residual_timeslice_us": 10000 },
      "batch_bandwidth_cap": 0.12
    }
  }
}
```

**`system`** is about the world and is subsystem-neutral. Every consumer reads it. This is the contract described in §4.4.

**`subsystems`** is a namespace, one key per consumer. Adding a network QoS driver adds a `network_qos` key and changes nothing else — not the `system` block, not the existing consumers, not the validator branches already written. This project fills exactly one key.

**`reasoning` is mandatory and comes first.** Two reasons and one open question:

- *Diagnosis.* When a configuration performs badly we need to know whether the model misread the situation or read it correctly and drew the wrong conclusion. Those are different failures with different fixes — one is a knowledge problem, the other a mapping problem — and without the reasoning field they are indistinguishable in the logs.
- *Quality* — a question, not a claim, which Layer 1 can answer by running the recognizer with and without the `reasoning` field. For classification-like, non-math questions the literature finds little or no gain from reasoning first, while models of 7–9B do gain on math, so scale alone does not rule a gain out (`sprague-iclr25`). Under a JSON schema, constrained decoding helped classification and hurt reasoning, and an answer generated before its reasoning turned chain-of-thought into direct answering (`tam-emnlp24`) — so the comparison holds only if `reasoning` is generated before `system`, as the contract and the stand-in schema order them (`docs/data-contracts.md` §6; `dataset/tools/meas/llm/schema.full.json`). No source compares a classification with and without a reasoning field.
- *Auditability.* A system that changes behaviour for reasons nobody can inspect is not something an OS vendor would ship. A log line explaining why the machine entered a particular configuration is the difference between a feature and a black box.

`reasoning` and `situation` never cross into any consumer. The validator ignores them entirely; they flow to the logs and the evaluation harness.

The cost is real and should be stated: reasoning tokens add latency and inference cost. The model is consulted only when the process set changes, which we assume is rare in real use (no source), so we judge the cost affordable — but the latency figure that goes in the paper must be measured with reasoning included, not without.

## 4.4 The contract: shared vocabulary and consumer drivers

### 4.4.1 Why a shared layer rather than direct configuration

If the model emitted configuration for every subsystem and nothing else, it would need to know the tuning constants of all of them. Three problems follow.

**Consumers are not known in advance.** The CPU scheduler is in the kernel; a network shaper is a separate daemon; a third party might add something we never anticipated. If a new consumer requires editing the prompt, consumers are coupled to the model. With a shared vocabulary, a new consumer subscribes and brings its own interpretation — the model need not know it exists.

**The model has never seen any of these subsystems.** It knows what Blender is; it does not know what `timeslice_us: 10000` does on this machine, and it knows even less about a shaper it was never told about. Trusting direct configuration multiplies that risk by the number of consumers. Trusting the vocabulary does not.

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

The vocabulary is ratified and normative in `docs/recognition-vocabulary.md`; this section summarizes it and keeps the design argument.

**Modes** — what the machine is primarily doing. Sixteen, taken verbatim from the dataset's source-backed ground-truth labels: `browsing`, `office`, `mail`, `dev`, `photo`, `meeting`, `gaming`, `media`, `video-edit`, `compile`, `ml-train`, `render`, `transcode`, `indexing`, `backup`, `idle`. (`ambiguous` exists as a ground-truth-only label for the C6 boundary case; it is not on the recognizer menu.)

**Attribute** — an independent fact that a mode label alone cannot carry:

| Attribute | Question |
|---|---|
| `background_wanted` | Is the sustained background work something the user asked for? |

Mode labels alone cannot express the §2.3 table — gaming with a wanted download and gaming with an unwanted upgrade both collapse into `gaming`. Adding more labels does not fix this, because the same wanted-vs-unwanted distinction recurs inside every mode. Adding a *dimension* does:

```text
  16 labels                       →  16 situations,  16 validation entries
  16 labels + 1 boolean attribute →  32 situations,  17 validation entries
```

Expressiveness grows multiplicatively while validation cost grows additively.

### 4.4.4 The admission test for vocabulary terms

A term belongs in the shared vocabulary only if it is meaningful to more than one consumer and not derivable from behavioural observation. If MLFQ's demotion rule would discover it within a few time slices anyway, it carries no semantic information; if only one consumer can act on it, it is that consumer's configuration, not vocabulary.

| Term | CPU scheduler | Power governor | I/O scheduler | Network QoS |
|---|---|---|---|---|
| `mode` | Algorithm selection | Clock ceiling, thermal budget | Queue depth, readahead | Shaping policy |
| `background_wanted` | Throttle vs. defer | Suppress deep sleep | Bandwidth split | Background class |

Every row is filled in at least three columns. Filling this table is the concrete procedure for admitting any future vocabulary term: a candidate attribute that lands in one column is configuration wearing a vocabulary costume, and gets rejected.

We ship one graded attribute deliberately — each additional one multiplies the oracle search space (Part 7) — and the design extends to more without restructuring (promotion is governed by the extension rule in `docs/recognition-vocabulary.md`).

## 4.5 Algorithm menu

This section describes the CPU scheduler driver specifically. An algorithm earns a place in the menu only if there is a situation where it clearly beats the alternatives. Anything dominated everywhere is a baseline, not an option.

| Algorithm | Wins in | Why MLFQ loses there |
|---|---|---|
| **MLFQ** | Ordinary interactive use, idle | — this is the default and the right answer for mixed, unknown work |
| **EDF** (earliest deadline first) | Gaming, media, anything with a real-time producer | MLFQ has no concept of a deadline; a periodic job's deadline is its next period — a frame every 16.7 ms at 60 Hz, a 128-frame audio buffer every 2.67 ms at 48 kHz (Appendix A, **Deadline**) |
| **Lottery** | Contention with background work the user wants finished | MLFQ cannot set proportions. Lottery gives shares proportional to tickets in expectation, its accuracy improving with √n of the draws, so background gets, in expectation, its ticket share — `batch_share`, 15 % at the boot default, a design value no source names (`waldspurger-osdi94` for the proportionality) |
| **FIFO** | Pure batch throughput | A job switched out loses cache state it built, at a cost that depends on whether its data still fit in the cache and how it accesses them (`li-expcs07`); FIFO switches only when a job blocks or ends. *Note (2026-09-09): the simulator charges no context-switch cost and models no cache (switch memo §3), so inside this experiment this advantage does not exist and what remains of FIFO is non-preemption, which only hurts the foreground term every scored file carries; the prior driver table therefore names FIFO on no row. FIFO stays in the menu as a choice the LLM conditions can make and be scored on, a point in the `random` draw and the configuration search, and an entry every calibrated row carries.* |

Note what tunes the treatment of background work inside a gaming session: not the mode, but the attribute — `background_wanted` decides whether the bulk work is capped-but-progressing or freely deferred. This is the concrete payoff of §4.4.3: the mode picks the algorithm family, the attribute picks how the rest of the machine is treated under it.

**Round Robin is deliberately excluded.** RR is MLFQ with a single queue — a special case, not an alternative. It remains a baseline for reporting, but there is no situation where a model should choose it.

A note on lottery scheduling: its shares are proportional in expectation, not exactly, and a client holding tickets eventually wins, after 1/p lotteries on average with p its share of the tickets, with no bound on the wait (`waldspurger-osdi94` §2.2). Selection is O(n) with a list of clients and O(lg n) with a tree (§4.2), slower per decision than popping an MLFQ queue head. It earns its place because ticket allocation is the natural way to express something like `batch_bandwidth_cap`.

This mirrors what Linux already does — `SCHED_DEADLINE` is EDF with a Constant Bandwidth Server (`linux-sched-deadline`), `SCHED_FIFO` fixed-priority real time without time slicing (`man-sched`), `SCHED_OTHER` EEVDF since Linux 6.6 (`linux-sched-eevdf`), a proportional-share algorithm (`eevdf-tr95`). The mechanism for varying the algorithm exists. Deciding *when* to use which is the open problem.

**Two consequences for other parts of this document:**

- EDF requires deadlines in the process model. Satisfied: periodic work carries `TIMER(period)` and deadlines in the archetype grammar (`docs/simulator/interpretation-contract.md` §3).
- Configuration fields are algorithm-dependent, and the per-algorithm field lists are frozen in `docs/recognition-vocabulary.md` (MLFQ: `num_queues`/`timeslice_us`/`timeslice_growth`/`boost_interval_us`; EDF: `residual_timeslice_us`; lottery: `batch_share`/`timeslice_us`; FIFO: none — plus the cross-algorithm `batch_bandwidth_cap`). Validation is conditional on the selected algorithm rather than a flat field list.

## 4.6 Measuring whether the vocabulary is sufficient — the RQ3 ladder

If a consumer can act well on the `system` block alone, drivers stay thin and new consumers cost nothing. If it needs the model to fill its `subsystems` block, every future consumer inherits that burden. This is the architecture's central open question, and we measure it by running the CPU scheduler driver at three levels.

In the large, the project asks two questions in order. First, **does reading names semantically improve scheduling?** That is `llm_vocab` against the two name-table conditions and the oracle, and it needs nothing beyond the `system` block. Second, **if it does, how much can be delegated to the model?** That is the three-rung ladder below.

**Variant A — `llm_vocab`, vocabulary only.** The `subsystems` block is unread. Algorithm and parameters come from the driver table's default entry for the row the model's reading selects.

**Variant B — `llm_algo`, vocabulary plus algorithm.** The model fills `algorithm` but not parameters. The daemon takes the row's entry for that algorithm — the driver table carries one tuned entry per algorithm per row (§8.2 decision 3) — so the choice is the algorithm class alone; the cap and the constants remain the table's.

**Variant C — `llm_full`, full configuration.** The model fills the whole `cpu_scheduler` block, as in §4.3. Runs as a subset diagnostic against perfect configuration, not as a scored rung (archive Q5).

All three keep `reasoning`, `situation`, and `system`. The read scope is applied before validation: the validator checks the configuration the simulator will actually receive.

**What each level asks:**

| Variant | Asks whether the model has | Knowledge source |
|---|---|---|
| A | Understanding of what the software is for | World knowledge from pretraining |
| B | Understanding of which algorithm class fits a situation | General CS knowledge |
| C | Ability to calibrate constants for a system it has never seen | System-specific knowledge it does not have |

**Two tables.** The **prior table** is written from scheduling theory before any measurement and is used only for the pre-registered headroom gate (RQ0). The **calibrated table** is tuned per row on the disjoint driver table tuning set (workload building plan §4) and produces every reported result; its default per row is the algorithm whose tuned entry scored best there.

**Reading the outcome — and the tie built into it.** Because the calibrated default is, by construction, the best-scoring algorithm for the row, `llm_algo` cannot beat `llm_vocab` on it when the situation reading is correct: naming the default reproduces `llm_vocab`, naming anything else gets a tuned-but-worse entry. The only way `llm_algo` gains is when the reading was wrong and the named algorithm suits the true situation better than the misread row's default. The delegation rung is therefore scored three ways, none of which asks for a gain that the design forbids:

1. **Algorithm-choice accuracy** — the model's named algorithm against the calibrated default for the true row, graded like a Layer-1 metric: agreement rate, a four-class confusion matrix, split by software familiarity. No simulator involved. This is the direct measurement of "does the model know which algorithm class fits."
2. **Cost of delegation** — `llm_algo` against `llm_vocab` on the calibrated table, read as non-inferiority: what handing the model the algorithm choice costs in headroom, or whether it costs nothing. A deployment number: it is the case of a driver with no table, or a situation the table does not cover.
3. **Delegation under vocabulary gaps** — *proposed, deferred until the main experiments are complete.* If `llm_algo` scores close to `llm_vocab` on covered situations, the model's algorithm knowledge can act where the vocabulary has no row and `llm_vocab` can only fall back. Measurable by blanking rows of the calibrated table to the schema defaults and comparing the two conditions on the files that exercise those rows. Not observable in the main design, because the validator forces a legal mode on every condition. *Design fixed 2026-09-10 (Phase 7):* since every one of the 32 rows now has a single-segment coreset pair, the files per blanked row are fixed by rule, not picked — the row's C1 base for a `true` row, its C7 counterpart for a `false` row, plus any C2 or C3 segment labelled with that row; blanking means the schema defaults, so the table format needs no new field; the arm runs on the calibrated table after the main experiments, and its row set is pre-registered in the RQ0 gate spec as "every row" unless a stated reason excludes one.

`llm_full` against perfect configuration answers whether generated constants can beat a hand-tuned table at all; we expect not — the model knows what Blender is but has never observed what `timeslice_us: 2000` does in *our* simulator, and no amount of authority supplies that.

Note that calibrating the table offline makes A *stronger* as an experiment, not weaker: if the table is near-optimal, A's performance reflects purely how well the situation was read. The same fact is what makes the tie above unavoidable, and we state it rather than handicap the table to give B room.

## 4.7 What the model is never allowed to do

Bounding the model's authority is what makes the system defensible.

- It cannot invent new modes or attributes. Unknown keys and unknown labels are rejected.
- It cannot write into a `subsystems` key that no registered driver claims.
- It cannot alter the relative priority ordering between scheduling classes.
- It cannot reference specific PIDs. PIDs identify instances; instances die and PIDs get recycled into unrelated processes. All configuration is system-wide or class-scoped. Enforced by omitting PIDs from the telemetry schema, not by instructing the model to ignore them.

Starvation is not among these bounds. The executor has no starvation window; FIFO and EDF's deadline class have no horizon, so beside them an unset cap can leave a task waiting without bound, and an idle-class task waits behind other classes by design; MLFQ's boost can be lengthened to 10 s but not removed (`docs/recognition-vocabulary.md` §2). A run in which any task waits more than 30 s fails the harness's `starvation_floor` guard, and on a run the RQ0 criterion reads that makes the verdict invalid. The batch class's bandwidth cap is one configuration field — the driver table row's under every condition but `llm_full`, unset or 0.05–0.95 there — which the executor is to enforce (not yet implemented).

Every applied configuration is stamped with **provenance**: unmodified, clamped, held, or fallback. Without this, a good result is unattributable — we would not know whether the model performed well or the fallback did.

## 4.8 Implementation

We build a userspace discrete-event simulator rather than modifying a real kernel. Booting, interrupt handling, and memory management are a full semester of work on their own and answer none of our research questions. The simulator gives us fast iteration, easy metric collection, and deterministic replay. See `docs/background-guide.md` for a non-technical explanation of what it does and does not model.

| Component | Language | Rationale |
|---|---|---|
| Simulator | C++ | Logic carries over if we later port to xv6 or Linux `sched_ext` |
| Policy daemon | Python | We will edit prompts dozens of times a day; LLM SDKs live here |
| Bench harness | Python | pandas and matplotlib |

The two sides communicate over JSON across a process boundary. If we later replace the simulator with a real kernel, the daemon does not change at all. Starting with a simulator is the migration path, not throwaway work.

**Model hosting.** The client module supports both a hosted API and a local server (llama.cpp's server, Ollama or vLLM; `llamacpp`, `ollama-docs`, `vllm-docs`) behind one interface. We use the API for fast prompt iteration and a local quantized model for the measurements that go in the paper: a deployment story that sends the running process list to a remote server is not credible, and the local model's latency is measured, not assumed (§4.1). Constrained decoding restricts every generated token to the grammar compiled from the schema, so an answer that completes is well-formed (an `eos` stop implies the grammar completed); llama.cpp converts a subset of JSON Schema — keywords it does not read are ignored without notice, a pattern it cannot express is accepted as any string with only a server-log warning, and some unsupported constructs fail the request (`llamacpp`). The schema carries the algorithm menu (an `enum`) but not the number ranges, the clamping rule or the cross-field rule, and the validator's parse-failure branch stays for answers ended by the token limit or the context. Comparing a frontier API model against a local 8B model is a cheap and worthwhile appendix result — if a small local model reads situations nearly as well, the deployment claim stops being hypothetical.

**Record and replay.** Running the full condition matrix against a live model would be slow, expensive, and non-reproducible. The daemon therefore runs in two modes. In *record* mode it queries the model once per distinct telemetry snapshot and stores `(prompt hash → response, measured latency)`. In *replay* mode it serves from that cache with no model in the loop. Because the cache key is `(workload id, snapshot hash, prompt version)`, one cache serves every condition for every set it visits. Set changes are defined by pinned events only — arrivals and scripted user-closes (decision 2026-08-28; finite-task exits do not appear in telemetry) and, since 2026-10-11, moves of the window focus (`docs/data-contracts.md` §5, rule 6) — so query points are scheduler-independent by construction, and the full matrix is deterministic and free to re-run.

---

# Part 5 — Experimental design

## 5.1 The core principle: swap one component

Any consumer can be decomposed into two parts:

- **The recognizer** — what situation are we in?
- **The executor** — given that, what do we do?

We hold the executor completely fixed across every condition and swap only the recognizer. Any performance difference is then attributable to recognition, because nothing else changed. In code, every condition implements one `Recognizer` interface; the oracle and the random recognizer are implementations of it just as the LLM is.

```text
   ┌──────────────────────┐
   │  fixed               │──┐
   │  no situation concept│  │
   ├──────────────────────┤  │
   │  random              │  │      ┌───────────────────┐
   │  random proposal     │  │      │  IDENTICAL        │
   ├──────────────────────┤  ├─────>│  EXECUTOR         │────> metrics
   │  shipped_catalogue   │  │      │                   │
   │  CachyOS's catalogue │  │      │  runs the         │
   ├──────────────────────┤  │      │  algorithm,       │
   │  strongest_name_table│  │      │  parameters and   │
   │  rules in its design │  │      │  cap each config  │
   ├──────────────────────┤  │      │  sets             │
   │  llm_* (A / B / C)   │  │      └───────────────────┘
   ├──────────────────────┤  │
   │  oracle              │──┘
   │  ground truth        │
   └──────────────────────┘
```

## 5.2 Conditions

| Condition | Recognition | Configuration | Role |
|---|---|---|---|
| `fixed` | none — always default MLFQ | fixed | Floor: no situation awareness at all |
| `random` | uniformly random proposal | driver table | Control: what a useless recognizer scores |
| `shipped_catalogue` | the name-keyed catalogue CachyOS ships enabled (`ananicy-rules` at `03ef03fb`, as CachyOS installs and enables it with ananicy-cpp), matched on the basename of each process's `argv[0]`, untruncated (`ananicy`) | driver table | What a shipping distribution does by default |
| `strongest_name_table` | a rule list in the catalogue's design covering the software the dataset presents as known | driver table | **The strongest counter-hypothesis** |
| `llm_vocab` | LLM fills `system` only | driver table | Variant A |
| `llm_algo` | LLM fills `system` + algorithm | driver table — the row's entry for the named algorithm | Variant B |
| `llm_full` | LLM fills the whole block | LLM | Variant C |
| `oracle` | ground truth from the workload file | driver table | Ceiling: perfect recognition |

Each name-table condition answers its own question. Beating the shipped catalogue answers RQ2's question about what shipping systems do: a comparison with what a deployed, community-maintained daemon does on a distribution that enables it — what a shipping Linux distribution, CachyOS, does by default (`cachyos-settings`). Beating the strongest name table is the paper's claim, the one that matters most. Failing to beat either is a legitimate finding.

Every condition runs on the same files under each telemetry shape the experiment spec lists — `focus`, the name → count multiset with the focus holder's name, and `names`, the multiset alone, at the same query points (`docs/data-contracts.md` §5) — and the difference is reported as the focus field's measured worth. The RQ0 gate spec runs `[focus]` alone, since its three conditions (`fixed`, `random`, `oracle`) read no telemetry.

Ownership note: 박이안 builds the two name-table conditions' rule lists as well as the LLM conditions. Putting the strongest counter-hypothesis in the hands of the person arguing for the LLM keeps the result honest.

## 5.3 The gap that must exist first

**`random` versus `oracle` defines the entire measurable space of this experiment.** If a perfect recognizer scores only marginally better than a random one, then no recognizer can demonstrate anything, and the experiment is dead before we write a single prompt.

This can happen for a concrete reason worth watching for: if the per-class heuristics are strong enough, they self-correct misclassification. Put a compiler in the interactive class and the MLFQ demotion rule will move it within a few time slices anyway. The heuristics do not steal credit from the model — they eliminate the variance we are trying to measure.

**Both `random` and `oracle` can be run before any LLM integration exists.** The ground truth is already written in the workload file; random is one line of code. This is the cheapest possible early kill check, and it should be the first experiment we run. If the gap is narrow, we redesign workloads or deliberately weaken the executor's self-correction before investing in prompt engineering.

*Pre-registered 2026-09-12, re-pinned 2026-10-09:* the criterion is committed as data in `harness/experiments/rq0-gate.yaml`, the RQ0 gate spec — at least 10 of 19 judging files must show a gap of at least 0.5 between perfect and random recognition (13 of 25 until the re-pin of 2026-10-09, sub-task 9.14, the consumer rework), `random` over 100 seeds, with the boot-default sweep at ten alternatives (the top slice at 0.5, 0.7, 0.9, 1.2, 2, 3, 5, 14, 20 and 100 ms), the latency-floor and threshold sensitivity lines, the sensitivity lines over the rebuilt files' variants, the failure procedure (configuration search before any workload change), and the grounding of every number written beside it. The harness's RQ0 gate evaluator reads that file and nothing else.

Phase 1 runs on the full ratified vocabulary — sixteen modes plus `background_wanted`. The attribute is not optional there: the RQ0 judging set is built from label-varying pairs — the C2 pairs' normal-class halves (`c2-p1a`, `c2-p2a`, `c2-p2b`, `c2-p3a`), the four batch C1 bases whose job the row's share reaches, and eleven C7 counterparts (`files.judging`) — most of whose two sides differ in `background_wanted`, so a modes-only gate could not express its own judging set.

## 5.4 Two layers of measurement

**Layer 1 — recognition accuracy.** Compare the `system` block against the ground truth in the workload file. No consumer involved at all. This is a pure reading test, so heuristics cannot contaminate it.

- Mode accuracy and per-mode confusion matrix
- Per-attribute accuracy, reported separately from mode accuracy
- Latency from process-set change to correct output, measured with reasoning tokens included
- Run-to-run consistency — for the two models and the one request measured, the same input on the same hardware returned the same answer at temperature 0 with a fixed seed, one request at a time, so on one machine this measure reads what changes in the input, not sampling noise; the longer answers differed across hardware, answers can differ under batched serving, and an input that carries the day changes from one day to the next (Part 7)
- Accuracy split by well-known vs. unregistered software

Attribute accuracy is reported separately because the two failure types have different consequences. Getting `background_wanted` wrong on a gaming workload produces a specific, predictable performance failure; getting the mode wrong produces a diffuse one.

The `reasoning` field is read during failure analysis, not scored automatically. When a run produces a wrong configuration, the reasoning tells us which of two very different things went wrong: the model did not know what the software was, or it knew and drew the wrong conclusion. The first is a limit of the approach; the second is a prompt or mapping problem we can fix.

**Layer 2 — consumer performance.** The condition ladder above.

Separating these makes the ambiguous outcome interpretable. If Layer 1 is high and Layer 2 is flat, the conclusion is precise:

> The model reads system situations accurately. That reading does not improve CPU scheduling, because existing behavioural heuristics were already sufficient for this consumer.

## 5.5 Workloads

Workload definitions are the experiment. Each carries a ground-truth timeline — mode and attributes — that only the oracle condition and the harness, which grades and scores against it, see; the simulator's run file drops it (`docs/data-contracts.md` §4).

The workloads are synthetic because no public trace gives desktop process trees with names over time — the negative result of `docs/workload/grounding-sources.md`. The nearest data falls short: cluster and VM traces carry no consumer applications; DARPA OpTC's process-create events, with image paths, come from Windows 10 enterprise endpoints in an instrumented exercise (`darpa-optc`); BEHACOM gives the foreground program's name per minute from natural use, without the process-level detail beside it — children and background processes (`behacom-dib20`).

> **Normative home:** the workload set is specified by `docs/workload/building-plan.md`: the core set C1–C7, 51 files (67 labelled segments), balance counted per segment, authored as timelines and compiled to canonical files — behaviour parameters live in archetypes, never inline. Beside it, five generated sets composed from the sixteen C1 task sets, each with its manifest — the transition grid (480), the return grid (720), the flap-stress set (24), the distractor grid (272) and the familiarity ladder (66) — carry the rate claims (recognition at a transition, a stale configuration's cost, distractors, familiarity), the authored C3, C4 and C5 files standing as existence cases. A generated file has no scoring entry of its own: it is scored by one rule over the C1 entries, per placement its manifest records (`harness/scoring/scoring-spec.yaml`); an experiment spec selects generated files from a pinned manifest by their grid axes (`files.select`, `pins.generated`), the axes read by joining `workload_id` to the manifest, not as records columns. The Family tables below remain the *claims* framing — each Family maps onto core-set groups or generated sets — and the YAML example below is illustrative of the information asymmetry only, not the file format.

```yaml
name: gaming_wanted_vs_unwanted_bulk
ground_truth:
  - t_ms: 0
    mode: gaming
    background_wanted: true

processes:
  - name: League of Legends
    visible_to_llm: true
    pattern: { type: latency_critical, period_ms: 16, deadline_ms: 16, cpu_burst_ms: [4, 9] }
  - name: Discord
    visible_to_llm: true
    pattern: { type: interactive, cpu_burst_ms: [1, 4], io_wait_ms: [100, 800] }
  - name: steam
    visible_to_llm: true
    pattern: { type: io_heavy, cpu_burst_ms: [2, 10], io_wait_ms: [5, 20] }
```

**The information asymmetry is the core of the design:**

- `name` — what a recognizer is shown, names only: no paths, no command lines (the ratified telemetry decision), with each name's count and the focus holder's name. The LLM conditions and the two name-table conditions read it; `fixed`, `random` and `oracle` read none.
- `pattern` — visible to the simulator, which runs it, and to the harness, which reads each task's demand, WAIT channels and chain topology from it; never to a recognizer. The model never sees ground truth about behaviour.
- `ground_truth` — visible to the oracle condition and the harness's grading and scoring only.

This must be enforced in code. When results come out ambiguous there will be a temptation to "just give the model a bit more context," and without a recorded baseline the experiment loses its meaning.

### Family 1 — Single situation, long duration

Does situation awareness help at all in the easy case?

| Scenario | Mode | Attributes |
|---|---|---|
| Nightly maintenance: indexer + backup + updater, no input | `idle` | — |
| Parallel compile ×8 + editor | `compile` | — |
| Document work + mail client | `office` | — |

### Family 2 — Jobs that differ in intent beside the same situation ★

**The paper's core evidence.** Pairs of real jobs whose correct policies differ, which also differ in behaviour as measured — P1's jobs in declared class too, P2's programs in declared priority (nice), which the task model does not carry, both P2 files declaring `normal`; each pair tests what recognition adds over them. The dataset carries the first two rows as its C2 pair P2 and the last two as P1 (`docs/workload/building-plan.md` §3).

| Scenario | Mode | Attributes | What splits it |
|---|---|---|---|
| Game + Steam installing another game the user just started (`c2-p2a`) | `gaming` | `background_wanted: true` | Throttled by the batch class's cap, its waits judged by the 30 s guard, not guaranteed |
| Game + Ubuntu's unattended upgrade (`c2-p2b`) | `gaming` | `background_wanted: false` | Freely defer |
| Game + OBS capture | `gaming` | — | Two deadlines (encoder distinctions are carried by mode under the ratified vocabulary) |
| Training run (PyTorch's basic MNIST example on the CPU) + editor (`c2-p1a`) | `ml-train` | `background_wanted: true` | Long batch the user asked for |
| File indexer + editor (`c2-p1b`) | `indexing` | `background_wanted: false` | Long batch nobody asked for |

The last two are the P1 pair, the load-bearing one: two real jobs beside an editor with opposite correct policies, differing in behaviour and in declared class. The training run (`c2-p1a`; `pytorch-examples` — an actual training run, with no claim that desktop users train MNIST) is one thread, 69.49 s ±27.3 % between voluntary blocks, at the default policy and nice 0. GNOME's Tracker indexing a home folder (`c2-p1b`; `tracker-miners`) is five processes, 1.876 ms between voluntary blocks on average, `SCHED_IDLE` at nice 19 with the idle I/O class, set by the program on itself, and runs 0.844–0.849 of its CPU past a 10 ms slice. The pair carries the recognition claim — the model must tell the wanted training run from the unwanted indexer, which a name table cannot — and its scheduling headroom on `c2-p1a`'s side: the RQ0 gate judges `c2-p1a` and reports `c2-p1b`, the indexer's declared idle class settling its side.

### Family 3 — Unregistered software ★

Software the shipped catalogue (`ananicy-rules` at `03ef03fb`) carries no rule for, and that the strongest name table, written for the software the dataset presents as known, does not cover either — where name matching fails structurally, and where the world-knowledge claim in §2.4 is decided. The dataset measures the family's question on the generated C5 familiarity ladder (66 files: each mode's task set renamed at tiers 4 and 5, and render's and backup's jobs at tier 3 under the names their campaign records show, `melt-7` and `duplicity`; the authored `c5-t4` and `c5-t5` standing as existence cases); the rows below are registration failures in the claims framing.

| Scenario | Mode | Attributes |
|---|---|---|
| An audio workstation the catalogue lacks (e.g. `zrythm`, `qtractor`) + plugin chain | `media` | — |
| A game built with Godot whose own process name the catalogue does not carry + Discord (registered, `Chat`) | `gaming` | — |
| Local Kubernetes + database + dev server — the cluster's and the databases' programs have no entry; `node` is registered (`BG_CPUIO`, the idle class) | `compile` | `background_wanted: true` |

The audio-workstation row is the deadline end of the family. No game mode's documentation addresses audio workstations, and Feral's can be applied by the user (`feral-gamemode`); the shipped catalogue registers the major ones — `reaper`, `bitwig-studio`, `ArdourGUI`, `lmms`, `audacity` — as `Player-Audio`, the music players' class (`ananicy-rules`), so the row stands for a workstation it lacks. No source states "1–3 ms": Ardour's manual sets a recording target below 5 ms round trip, which under jackd's default two periods at 48 kHz takes a 32-frame period (0.67 ms, arithmetic), and notes that studios usually monitor through an external console (`ardour-manual`, `jackd-man`); a 128-frame buffer at 48 kHz comes due every 2.67 ms, against a game's frame every 16.7 ms at 60 Hz. A late audio buffer is an xrun, heard as "clicks, pops and crackles" (`ardour-manual`); a late game frame is shown at the next vertical blank (`vulkan`).

### Family 4 — Phase shift at varied speed (RQ4)

The generated return grid: A → B → A over the 240 ordered mode pairs, every task set departing at its boundary, the middle segment 60 s, 10 s or 2 s (720 files), split by pair into a tuning half and a measurement half (120 pairs each, a pair's three variants on one side) for the hold-time plan. Beside it the transition grid (480 files: the 240 pairs in the `departs` and `focus` forms) carries recognition at a transition (`docs/workload/building-plan.md` §3a; `dataset/grids.yaml`).

Steady-state periods should be short here, because only the transitions carry information (Part 7, first risk). This family produces the most quotable finding, of the form: *"Semantic configuration pays off only when a situation persists at least N times the model's round-trip latency."*

### Family 5 — Adversarial and boundary

| Scenario | Expectation |
|---|---|
| A sustained CPU-bound job nobody asked for, named `chrome`, arriving at 20 s beside the browser's five (`c6-spoof`) | Misreading expected from its arrival — the structural limit of name-based recognition (a pre-committed miss) |
| Two media players under two indexers' real names, `baloo_file` and `tracker-miner-f` (`c6-alias`) | Misreading expected — another program's real name on the whole foreground (a pre-committed miss) |
| Gaming while actively awaiting a `-j8` kernel build (`c6-dual`) | Genuinely ambiguous: the ground truth is `ambiguous`, outside grading |
| A video call opened at 30 s in the running browser, a sixth `chrome` (`c6-fold`) | Invisible at process granularity — a resolution limit, not a recognition failure (a pre-committed miss from the call's arrival) |

These are the dataset's C6 resolution-limit files (`docs/workload/building-plan.md` §3). The last case should be reported as a scope boundary rather than an error. "This approach operates at process granularity and cannot see inside a browser" is an honest and useful statement about where the idea stops working.

### Balance requirements

A gaming-heavy scenario set would produce a result whose scope is exactly the scope Game Mode already covers. The dataset counts its balance per segment, over the driver-table cells (mode × `background_wanted`) and the familiarity tiers, in `dataset/coverage-grid.json`, checked in CI: every one of the 32 cells holds at least one core-set segment (`docs/workload/building-plan.md` §3, Balance check). Familiarity runs over five tiers — transparent (`chrome`), semi-opaque (`soffice.bin`), opaque (`cc1`), nonexistent-compositional (`audio-stream-he`), nonexistent-opaque (`qzvd`) — and the generated C5 familiarity ladder renames each mode's task set at tiers 4 and 5, and render's and backup's jobs at tier 3 (`melt-7`, `duplicity`) — 66 files.

Results must be reported split by familiarity tier. A result where the model wins only on the unregistered or invented names is not a weak result — it is precisely what §2.4 predicts, and reporting it split is what makes it evidence rather than an average.

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

Report percentiles, not just means: a mean hides the rare long waits. Shneiderman's review finds modest variation in response time tolerable, with frustration emerging when delays are unusually long — at least twice the anticipated time — in studies of second-scale responses (`shneiderman-csur84` §5.3, p. 282).

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
- **Transition count** — how often the configuration changed, to detect oscillation: the evaluator's `flip_cost` reporting line prints per recognizing run the configuration changes applied (`change_count`), those on a query graded config-incorrect (`wrong_change_count`) and the per-switch excess summed over the wrong switches into MLFQ (`wrong_switch_excess_sum`), beside the file's score (`docs/harness/metrics.md` §8)
- **Token and latency cost** per query, with reasoning tokens counted, reported separately for API and local models

The provenance breakdown must accompany every performance figure. A condition whose run spent half or more of its time under fallback or held configurations fails the `provenance_share` guard, and its score is not read as evidence about recognition: the part of that time under fallback measured the boot default, MLFQ, and held time ran whatever configuration was last in force (definitions in `docs/data-contracts.md` §7).

## 6.4 Experiment hygiene

**The workload holds no randomness at run time.** Every distribution is sampled at dataset-compile time with a recorded seed (`docs/simulator/interpretation-contract.md` §1); the simulator replays concrete values, and its one policy-internal draw, LOTTERY's, comes from a PRNG it seeds deterministically per run from the workload id. Two conditions therefore face byte-identical workloads by construction — the concern that scheduler-dependent draw order could make conditions face different workloads cannot arise, because no workload value is drawn at run time.

Beyond that: repeated runs with variance reported, one variable changed at a time, identical workload traces across all conditions. Every result that cannot be reproduced from a config file and a seed does not count.

---

# Part 7 — Risks and honest weaknesses

**One consumer cannot validate a general vocabulary.** This is the most significant honest weakness of the whole proposal. We designed the vocabulary partly with the CPU scheduler in mind, then measure it on the CPU scheduler. That the terms are meaningful to other consumers is argued in §4.4.4 and demonstrated nowhere. The mitigation available within this project's scope is to enforce the admission test strictly during the vocabulary freeze — a term that only one consumer can act on gets rejected, which is the discipline that keeps the vocabulary from silently becoming CPU scheduler configuration. Building a second driver is out of scope here (Part 10). Until one exists, the extensibility claim is a design argument rather than a result, and the paper should say so in those words.

**The measurable window may be tiny.** A gaming session lasts from minutes to hours depending on the game (§4.2), and we take as a premise that the situation is stable for the whole of it. The only moments where recognition quality matters are transitions. If a one-hour run contains five interesting seconds, our workloads must be built around transitions rather than steady state: the generated transition grid (480 files: the 240 ordered mode pairs × the `departs` and `focus` forms) and return grid (720 files, A → B → A) test them, with the distractor grid (272 files) for arrivals while the user stays put; the authored C3 arcs (the mode-transition group's three files) and C4 injections (the distractor group's three files) stand as existence cases.

**The strongest name table may simply win on common software.** For registered applications, a hand-written name table is accurate, instant, free, and deterministic. Our advantage exists only on software the table does not cover, which is why Family 3 is primary and why results are reported split by familiarity.

**Situations may not differ enough to matter.** If gaming and ordinary interactive use map to nearly identical configurations, reading the difference buys nothing. The mapping from vocabulary to configuration must produce genuinely distinct behaviour, and we should verify this before running the full matrix.

**Name-based reading is spoofable.** A sustained CPU-bound job named `chrome` will be misread, and so will programs wearing other programs' real names. We test this deliberately in Family 5 (`c6-spoof`, `c6-alias`) rather than pretending it does not exist.

**Non-determinism is a confound.** The same process set may yield different answers across runs. For the two models and the one request measured, the same input on the same hardware returned the same answer at temperature 0 with a fixed seed, one request at a time, so Layer 1's consistency measure on one machine reads what changes in the input, not sampling noise. The longer answers differed across hardware — the 8B's reasoning-first decision was `background_wanted` `false` on the M1 Pro and `true` on the EPYC 7763 on one prompt (`meas-local:m1pro-llm:2026-10-08`, `meas-ci:costs:2026-10-08`); answers can differ under batched serving, and an input that carries the day (Llama 3.1's "Today Date") changes from one day to the next. In the literature, hosted models configured to be deterministic varied in accuracy by up to 15 % across runs (`atil-eval4nlp25`), and the same model and prompt give different greedy outputs on different GPU architectures (`cooper-arxiv26`). The record/replay cache (§4.8) holds answers fixed for the experiment. Whether the daemon needs a hold time or hysteresis against oscillation is the hold-time plan's open question: the need is measured first with no rule (its step 1, the `flip_cost` line over the flap-stress set and the C4 files), and a rule's form and values, if any, are fixed before the RQ4 run.

**Reasoning costs latency.** Requiring the model to explain itself adds tokens to every query. The model is consulted only when the process set changes, which we assume is rare in real use (no source), so we expect the cost to be absorbed; but the RQ4 answer must be computed from latencies measured with reasoning included. Reporting a fast latency measured without it would be dishonest.

**Perfect-configuration search cost grows multiplicatively.** The oracle condition itself is free — it reads the true `(mode, background_wanted)` from the workload file and passes through the same driver table as every other condition (perfect recognition). The expensive ceiling is **perfect configuration**: ignoring labels and sweeping the configuration space per workload — four algorithms with their parameter grids and the cap — which is also the search that calibrates the table (one tool, in the harness). Mitigations, in order of preference: run the search on a representative subset and report that ceiling only for those; prune structurally inadmissible combinations (EDF with no deadline-bearing processes); keep the graded attribute count at one. If the full search becomes impractical we report a partial ceiling explicitly rather than quietly dropping it.

**Conditional validation is a real cost.** The validator must dispatch on subsystem key, then branch on algorithm within the CPU driver, with its own bounds and clamping rules per branch. Attributes add cross-field consistency checks on top. This is the largest single piece of added complexity, and it lands on one person.

**Scope honesty.** This is a simulator. It does not prove anything about real kernel performance, cache effects, or multi-core interactions. Its workloads are measured on one CPU of a hosted runner's AMD EPYC 7763, under Xvfb, with no GPU, no sound device and no human; another CPU model changes each program's speed by its own factor, which the venue variants' common factor of 0.8–1.25 does not reproduce, so the scheduling result is not claimed to transfer to another CPU or another machine's configuration (`docs/research-claims.md`, What is not claimed; `docs/workload/measurement-overview.md` §11). It answers whether the semantic signal carries information, which is a prerequisite for anything further — not a substitute for it.

---

# Part 8 — Team ownership and decisions to freeze

## 8.1 Areas

**인경민 — simulator and executor.** The discrete-event engine, virtual clock, process model. All scheduling algorithms and the per-class executor. Bandwidth caps and starvation protection. Telemetry extraction. The zero-delay oracle mode. The canonical workload loader and task-program interpreter, built to `docs/simulator/interpretation-contract.md`. If we later port to `sched_ext`, that lands here.

**박이안 — recognition.** Prompt construction, model integration and local hosting, output schema design, Layer 1 evaluation. Also **the two name-table baselines**, the shipped catalogue and the strongest name table — putting the strongest counter-hypothesis in the hands of the person arguing for the LLM keeps the result honest.

**인지오 — contract boundary and experiment infrastructure.** The IPC layer, validation state machine (subsystem dispatch, then per-algorithm branching), clamping, fallback logic, provenance tracking. The record/replay cache (§4.8). The mock policy generator that lets the other two work independently. The full bench harness: experiment matrix, metrics, plots.

This layout puts every integration point in one person's hands, making integration a daily activity rather than a late-semester event.

## 8.2 Decisions requiring all three

1. **The shared vocabulary** — ratified 2026-08-28: the dataset's sixteen modes plus `background_wanted` (normative: `docs/recognition-vocabulary.md`, together with the frozen `cpu_scheduler` config schema). Adding an attribute later requires re-labelling every workload and re-running every oracle. **Use the admission test in §4.4.4 as the procedure** for any candidate: fill the cross-consumer table and reject anything that lands in one column.
2. **The two protocol schemas** — telemetry out, proposal in. The `system` block is the contract; the `subsystems` block is per-consumer namespace.
3. **The CPU driver's mapping table.** Format frozen 2026-09-07 (`docs/data-contracts.md` §10): thirty-two rows keyed by `(mode, background_wanted)`; each row carries a `batch_bandwidth_cap`, a `default` algorithm, and one to four per-algorithm entries with their provenance (`theory` / `schema-default` / `tuned`). `system`-only conditions receive the default; `llm_algo` receives the entry for the algorithm it named. Two instances of one schema — the **prior table** (one entry per row, theory) and the **calibrated table** (four, tuned). Filling it is effectively the executor's behaviour specification.
4. **Metric definitions.** Ambiguity here invalidates every interpretation.
5. **Workload scenarios**, including the balance over the driver-table cells and the familiarity tiers in §5.5.
6. **What the model may see.** The names with their counts and the focus holder's name are in (names only — no paths or command lines). PIDs, ground-truth burst patterns, and ground-truth labels are out. Enforced in the telemetry schema, not in the prompt.

## 8.3 Operating rule

**Freeze the protocol early.** Once v1 is agreed, changes require all three of us plus a changelog entry. Three people writing against three slightly different assumptions about one interface, discovering it at integration time, is exactly how projects like this fail.

---

# Part 9 — Milestones

| Phase | Deliverable | Gate |
|---|---|---|
| 0 | Discrete-event simulator, MLFQ executor, canonical workload loader (per `docs/simulator/interpretation-contract.md`) | A workload runs and produces reproducible metrics |
| 1 | `fixed`, `random`, `oracle` on the full vocabulary (16 modes + `background_wanted`), through the prior driver table; criterion pre-registered in `harness/experiments/rq0-gate.yaml` | **Is the random-to-oracle gap large enough to measure?** If not, the pre-registered failure procedure: configuration search first, then redesign |
| 2 | `shipped_catalogue` and `strongest_name_table` conditions; the calibrated driver table, tuned on the driver table tuning set | Each name-table condition beats `fixed` on gaming workloads |
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

**Sweeping up the rest of the hardcoded semantic knowledge.** Hand-written name tables like the CachyOS catalogue are the most visible instance of a pattern that recurs throughout an OS: tables where a human wrote down what software is. Each is a candidate consumer. The long-term version of this work is not a better scheduler but an OS that infers this class of knowledge instead of shipping it as data.

**Real kernel implementation.** Porting the CPU driver to Linux `sched_ext` would move the result from "the signal carries information" to "the signal improves a real machine," and the daemon side would not change (§4.8).

**Recognition below process granularity.** Family 5 shows the resolution limit: a call opened inside a running browser is a sixth `chrome` and nothing more (`c6-fold`). Extending the signal to threads, cgroups, or application-reported sub-activities is a natural follow-on and a different research problem.

---

# Appendix A — Glossary

**Attribute** — an independent fact about the running process set, orthogonal to the mode label. One is graded: `background_wanted`.

**Batch process** — work with no human waiting on each step. Keeps a CPU busy, using nearly every cycle while it works (§1.2). Cares about total completion time.

**Consumer / driver** — a subsystem that subscribes to the recognition signal and translates it into its own configuration. Subscription is optional.

**Context switch** — saving one process's state and restoring another's. About 2.4 µs on the dataset's machine (`meas-ci:costs:2026-10-08`); 0.6–3.8 µs for the switch itself on others' machines, and on one laptop a frequent value of about 30 000 cycles, about 10.7 µs at its nominal 2.8 GHz (arithmetic) (`ghost-sosp21`, `li-expcs07`, `becker-arxiv18`), more with the cache state it disturbs.

**Deadline** — the time by which a periodic task's job must complete, its next period. A game frame every 16.7 ms at 60 Hz (the Steam Deck's LCD up to 60 Hz, its OLED up to 90 Hz; `steamdeck-store`); a 128-frame audio buffer at 48 kHz every 2.67 ms, a low-latency setting below the 1 024-frame default (PipeWire's `default.clock.quantum`, `pipewire-conf`; jackd's ALSA backend's `-r 48000`, `-p 1024`, `jackd-man`). A miss, per kind: a late game frame is shown at the next vertical blank under FIFO presentation (`vulkan`), a video sink drops a frame later than its allowed lateness (`gstreamer`), and a late audio buffer is an xrun, "clicks, pops and crackles" (`ardour-manual`).

**Discrete-event simulation** — advancing a virtual clock by jumping to the next scheduled event rather than ticking in real time. Mechanically a priority queue of future events.

**EDF (earliest deadline first)** — priority by the deadline of each task's current request (`liu-jacm73`, p. 55). On one processor, for independent periodic tasks whose deadline is the next request (Liu and Layland's assumptions (A1)–(A5)), EDF schedules every task set any algorithm can (p. 58) — exactly those whose utilisation is at most 1 (Theorem 7, p. 56); above 1 none can (p. 56). It needs each task's period or deadline (Linux's `SCHED_DEADLINE` takes them through `sched_setattr(2)`, `man-sched-setattr`).

**Interactive process** — work with a human waiting on it. Short CPU bursts, long sleeps: a few milliseconds of CPU per key for an office editor, a browser field and a mail composer, 0.2–1.4 % of their CPU while typing; tens of milliseconds per key where an IDE's language server re-checks the file, VS Code at 14–45 % of its CPU while typing (§1.2). Cares about response time.

**Lottery scheduling** — each process holds tickets; a random draw picks the winner. Shares are proportional in expectation, their accuracy improving with √n of the draws; a client holding tickets eventually wins, after 1/p lotteries on average, with no bound on the wait; selection is O(n) with a list, O(lg n) with a tree (`waldspurger-osdi94` §2.2, §4.2).

**MLFQ** — Multi-Level Feedback Queue. Multiple priority levels; processes are demoted for using up their allotment at a level and periodically boosted to prevent starvation (`ostep` ch. 8). The textbook form of classification by behaviour; Windows' priority boosts and decay are one form of it (§1.3).

**Mode** — a label describing what the whole system is primarily being used for. One of sixteen values, part of the shared vocabulary (`docs/recognition-vocabulary.md`).

**Preemption** — the kernel forcibly taking the CPU away from a running process, made possible by timer interrupts.

**Proposal** — the model's complete output: reasoning, situation description, `system` block, and `subsystems` block.

**Provenance** — the record of how an applied configuration was produced: unmodified, clamped, held from a previous cycle, or fallback.

**Recognition layer** — the architecture proposed here: a model that reads the process set, a shared vocabulary, and a driver interface for consumers.

**Response time** — arrival to first execution. The metric interactive work cares about.

**`sched_ext`** — a Linux facility for loading scheduling policies from userspace as BPF programs. The realistic deployment path for this work.

**Starvation** — a process being indefinitely denied CPU because higher-priority work keeps arriving.

**Time slice (quantum)** — how long a process may run before the scheduler reconsiders. Per system: Linux's base slice 0.70 ms × (1 + log₂ of the online CPUs, counted up to 8) since v6.15; `SCHED_RR`'s 100 ms; scx_lavd 0.5–5 ms with a boost to 500 ms; scx_rusty 20 ms or 1 ms; MLFQ variants 10 ms or less at the top, hundreds of milliseconds at the bottom (§4.1).

**Turnaround time** — arrival to completion. The metric batch work cares about.

---

# Appendix B — A worked example

One workload followed from file to metric. The workload file is §5.5's illustration, not the canonical format (`docs/data-contracts.md` §4); the telemetry and trace lines below follow their frozen contracts (§5, §9), abridged.

## B.1 One file, three audiences

The `gaming_wanted_vs_unwanted_bulk` definition in §5.5 is split into three slices, each handed only to its own readers:

```text
   name            ──►  recognizers; the simulator and harness also get it in the run file, but key each task by its id
   pattern         ──►  simulator and harness, never a recognizer
   ground_truth    ──►  oracle and the harness's grading and scoring only
```

The partition is enforced by which module is handed which slice, not by prompt wording.

## B.2 Telemetry — what the daemon shows the recognizer

One snapshot, built inside the daemon from the workload's visible projection (`docs/data-contracts.md` §4, §5) — what the recognizer is permitted to see:

```json
{
  "t_us": 12400000,
  "processes": [
    { "name": "Discord",           "count": 1 },
    { "name": "League of Legends", "count": 1 },
    { "name": "steam",             "count": 1 }
  ],
  "focus": "League of Legends"
}
```

| In | Out | Why excluded |
|---|---|---|
| names, counts | PIDs | §4.7 — instances die and PIDs are recycled |
| the focus holder's name (`null` when no window holds it) | burst patterns, CPU statistics | that is the ground truth being tested against |
| | mode and attribute labels | that is the answer |

Telemetry is a pure function of pinned events — launches, scripted user-closes and moves of the window focus — so the visited set sequence is scheduler-independent by construction (finite-task exits do not appear). A focus change is a set change and a query point (`docs/data-contracts.md` §5, rule 6). The daemon shows the set in one of two telemetry shapes, `focus`, as above, or `names`, the same snapshot without the `focus` field, at the same query points. The cache is keyed by snapshot hash, so it serves every condition for the sets visited.

## B.3 Trace — simulator to harness

The timetable, written down. Every performance metric is read off this; nothing is timed.

```text
  CPU │ Discord │   steam   │ LoL │   steam   │ LoL │ Discord │
      └─────────┴───────────┴─────┴───────────┴─────┴─────────┘
      0        3          11    15          23    27        30   ms
```

```jsonl
{"event":"run_start",      "t":0,     "task":"discord"}
{"event":"run_end",        "t":3000,  "task":"discord", "reason":"block", "blocked_on":"wait"}
{"event":"run_start",      "t":3000,  "task":"steam"}
{"event":"run_end",        "t":11000, "task":"steam",   "reason":"preempt"}
{"event":"deadline",       "t":15000, "task":"lol",     "due":16000, "met":true, "slack_us":1000}
{"event":"config_applied", "t":16000, "index":1, "algorithm":"EDF", "provenance":"clamped"}
```

Two event kinds carry information that block boundaries alone do not:

- **`deadline`** — the outcome of one periodic job. P99 frame latency and deadline miss rate are computed from these.
- **`config_applied`** — every configuration change taking effect, stamped with provenance. §6.3 requires the provenance breakdown alongside every performance figure: a condition whose run spent half or more of its time under fallback or held configurations fails the `provenance_share` guard, and its score is not read as evidence about recognition.

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
  slack_us  =  due  −  completion
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

Both are reported because they fail differently. At 60 fps one frame in a hundred, about one every 1.7 s, lands past the 99th percentile while the mean looks healthy. A scheduler can also hold the miss rate at zero while the tail creeps toward the deadline, which is a system about to fail under slightly more load. This is the §6.1 requirement to report percentiles rather than means, made concrete.
