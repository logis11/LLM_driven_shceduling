# Workload dataset — inventory of claims taken from external sources

Repo: `/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling` at commit `e3d3c9a` (main; `_dev/TODO.md` modified, not read). Read-only inventory; nothing fetched from the web; no claim judged.

## Conventions

- **Locations** are `file:line` relative to the repo root. A range `a-b` means the quoted text wraps across those lines.
- **Claim (verbatim)** quotes the repo text at each location. Where several locations say the same thing, the first quote is given in full and the rest are quoted where wording differs; wording differences are listed under **Wording differences**.
- **Grounds** names what the claim justifies in the dataset (param, value, field, name, structure, decision), or "prose only".
- **Neutral topic** is what an independent reader should look up in the source, with no repo numbers, units, characterizations or conclusions.
- **Status** is the `status:` line of the source's entry in `docs/references.md` (line given).
- **borderline** marks text where it is unclear whether the repo is asserting something about the source.
- Scope read: `dataset/archetypes.yaml`, `dataset/sources.yaml`, `dataset/timelines/**` (all 55 files; the 27 GENERATED derived timelines carry only a two-line provenance header and inherit `scenario:` tags from their bases), `dataset/README.md`, `dataset/tools/**` (py/sh comments and docstrings), `dataset/schema/workload.schema.json` (no source claims), `docs/references.md`, `docs/workload/{archetype-plan,building-plan,scenario-catalog,source-vetting,grounding-sources,coreset-guide}.md`, `docs/simulator/interpretation-contract.md`, `docs/data-contracts.md` (§2–§4 workload parts), `daemon/driver-table/prior.yaml`, `docs/daemon/prior-table-pair-review.md`. Skipped: `docs/guidebook/`, `_dev/archive/`, `docs/memos/`.
- Excluded as sources per the brief: `meas-ci`, `meas-pending`. Statements tagged `meas-ci` that describe third-party software are listed as borderline in the "Unattributed / plain-text" group at the end of Part 1.
- `dataset/README.md` carries no source-specific claim. Its only citation-shaped statements are general: README.md:8 "behavior library — one entry per process kind (fully measured, v0.1)", README.md:130 "**Every parameter value is sourced.** Numbers carry a `source` tag resolving through `sources.yaml` → `docs/references.md`", README.md:132 "**Zero `meas-pending`.** The library is fully measured; the linter keeps it that way." These are cross-referenced in Part 2(a) flags.
- `docs/data-contracts.md:76` makes the general statement "Every number in the library is either taken from published measurements or measured by us in CI, and each value records its source." and :96 "Nothing in the library is an unsourced number." (cross-referenced in Part 2(a)).

---

# Part 1 — Claims by source

## `interbench`

Status (docs/references.md:140): verified-in-vetting (2026-08-25); pin commit at submission. Type: deployed-system. `locator_pattern: "^(man|src)-[a-z]+$"` (dataset/sources.yaml:31). Locators used: `man-audio`, `man-video`, `man-x` (archetypes.yaml tags); `man-write`, `man-read` (prose in archetypes.yaml, archetype-plan, building-plan); `man-burn` (building-plan.md:60 only).

### C-interbench-1 — audio interactive task: wake interval and CPU share
- Source/locator: `interbench:man-audio`
- Locations and verbatim text:
  - dataset/sources.yaml:33-34 — "Establishes the community's interactive task models: audio wakes every 50 ms needing 5% CPU (SCHED_FIFO variant exists)"
  - docs/references.md:139 — "the community's interactivity task models: audio 50 ms @ 5%"
  - dataset/archetypes.yaml:52-53 — `period: {dist: constant, value_us: 50000, sampling: per-task, source: "interbench:man-audio"}`
  - dataset/archetypes.yaml:54-56 — `burst: {dist: constant, value_us: 2500, sampling: per-task, source: "interbench:man-audio"}`
  - dataset/archetypes.yaml:62-64 — `stats: [wakeup-rate 20 Hz, cpu-share 5%]` / "values are interbench's community interactivity model, not a measured behavior; no meas-ci referee."
  - dataset/archetypes.yaml:66-68 — "interbench man-audio states \"wakes every 50 ms needing 5% CPU\"; the TIMER/RUN transcription and the duty-cycle-to-duration arithmetic (5% of 50 ms = 2,500 us per period) are ours."
  - docs/workload/archetype-plan.md:23 — "(interbench's \"wakes every 50 ms, needs 5% CPU\" becomes a TIMER/RUN loop)"
  - docs/workload/archetype-plan.md:47 — "`audio-playback` — TIMER/RUN loop, 50 ms period @ 5% CPU. category_source: interbench; params: `interbench:man-audio`."
  - docs/workload/building-plan.md:56 — "50 ms interval, 5% CPU (`interbench:man-audio`)"
  - docs/workload/source-vetting.md:15 — "audio = 50 ms interval @ 5% CPU"
  - docs/workload/source-vetting.md:52 — "**Audio** 50 ms intervals @ 5% CPU (also SCHED_FIFO variant)"
  - docs/workload/source-vetting.md:95 — "interactive fields from interbench (50 ms/5%, …)"
  - docs/workload/scenario-catalog.md:24 — S13 row: "interbench Audio (50 ms/5%) … task models"
  - docs/workload/coreset-guide.md:124 — heading "periodic-interactive family (interbench에서 가져옴)"; :130 "50 ms마다 2.5 ms. CPU 5%. interbench의 \"audio\" 모델 그대로."
  - docs/workload/grounding-sources.md:27 — "parameter values for audio/video/gaming interactivity"
  - daemon/driver-table/prior.yaml:217 — "Video and audio playback are two periodic consumers (60 Hz and 20 Hz ticks, scored as miss rates)" (borderline: derived rate, no source id)
- Wording differences: "wakes every 50 ms" (sources.yaml, archetypes notes) vs "50 ms interval(s)" (building-plan, source-vetting) vs "50 ms period" (archetype-plan). The archetypes.yaml quote uses "needing"; archetype-plan's quote uses "needs" — both are presented in quotation marks as interbench's words. coreset-guide says the model is taken "그대로" (as is), while archetypes notes call the duration arithmetic "ours".
- Grounds: `audio-playback.params.period` = 50000 us and `burst` = 2500 us (via arithmetic); `validation_stats` (20 Hz, 5%); `category_source: interbench`; S13 catalog row; tasks bound to `audio-playback` (`spotify` in c1-media.timeline.yaml:16, c3-evening.timeline.yaml:30; `zoom` voice in c1-meeting.timeline.yaml:20).
- Neutral topic: in interbench's man page/source, the audio interactive task — how often it wakes, how its CPU demand is specified (percentage, duration, or both) and at what value, and whether a real-time scheduling-policy variant of it exists.

### C-interbench-2 — video interactive task: rate/period and CPU share
- Source/locator: `interbench:man-video`
- Locations and verbatim text:
  - dataset/sources.yaml:34-35 — "video 60 Hz (16.7 ms) at 40% CPU"
  - docs/references.md:139 — "video 16.7 ms @ 40%"
  - dataset/archetypes.yaml:79-80 — `period: {dist: constant, value_us: 16667, sampling: per-task, source: "interbench:man-video"}`
  - dataset/archetypes.yaml:81-83 — `burst: {dist: constant, value_us: 6667, sampling: per-task, source: "interbench:man-video"}`
  - dataset/archetypes.yaml:89 — `stats: [wakeup-rate 60 Hz, cpu-share 40%]`
  - dataset/archetypes.yaml:93-94 — "interbench man-video states 60 Hz (16.7 ms) at 40% CPU; the 16,667 us period and 40%-duty burst (6,667 us) arithmetic are ours."
  - docs/workload/archetype-plan.md:48 — "`video-playback` — TIMER/RUN loop, 16.7 ms period @ 40% CPU. category_source + params: `interbench:man-video`."
  - docs/workload/building-plan.md:57 — "16.7 ms period, 40% CPU (`interbench:man-video`)"
  - docs/workload/source-vetting.md:15 — "video = 60 Hz (16.7 ms) @ 40% CPU"
  - docs/workload/source-vetting.md:52 — "**Video** 60 receipts/s (16.7 ms) @ 40% CPU"
  - docs/workload/source-vetting.md:95 — "16.7 ms/40%"
  - docs/workload/scenario-catalog.md:24 — "Video (16.7 ms/40%) task models"
  - docs/workload/coreset-guide.md:136 — "60 Hz, frame당 6.7 ms. CPU 40%."
  - daemon/driver-table/prior.yaml:217 — "(60 Hz and 20 Hz ticks …)" (borderline)
- Wording differences: "60 Hz" vs "60 receipts/s" (source-vetting:52) vs "16.7 ms period" (no rate). No location states whether 40% is of a frame period or of wall time.
- Grounds: `video-playback.params.period` = 16667 us, `burst` = 6667 us; validation stats; S13 row; also the binding of `gamescope` (c1-gaming.timeline.yaml:2, 21-22 — "gamescope -> video-playback: frame-periodic compositor approximation (ours)") and of `zoom` video (c1-meeting.timeline.yaml:18) and `mpv` (c1-media.timeline.yaml:14, c3-evening.timeline.yaml:28).
- Neutral topic: in interbench's man page/source, the video interactive task — its frame or receipt rate / period, the CPU demand it is given and how that demand is expressed.

### C-interbench-3 — X interactive task: variable CPU demand, window-drag emulation
- Source/locator: `interbench:man-x`
- Locations and verbatim text:
  - dataset/sources.yaml:35 — "X variable 0-100% (window-drag emulation)"
  - docs/references.md:139 — "X 0–100% variable"
  - dataset/archetypes.yaml:101 — `desktop-interactive: category_source: interbench`
  - dataset/archetypes.yaml:117-119 — `burst_fraction: {dist: uniform, min: 0.0, max: 1.0, sampling: per-iteration, source: "interbench:man-x"}`
  - dataset/archetypes.yaml:138-140 — "Burst CPU cost linearizes interbench man-x's \"variable 0-100%\" as a uniform fraction of the preceding input gap"
  - docs/workload/archetype-plan.md:49 — "input-driven variable bursts, 0–100% CPU … category_source + params: `interbench:man-x` (burst shape)"
  - docs/workload/building-plan.md:58 — "0–100% CPU on input (`interbench:man-x`)"
  - docs/workload/source-vetting.md:15 — "X = 0–100% variable"; :52 "**X** variable 0–100% (window-drag emulation)"; :95 "X 0–100%"
  - docs/workload/coreset-guide.md:144 — "`burst_fraction`: burst의 길이 = 직전 gap × uniform(0, 1). interbench의 \"0–100% 가변 CPU\"를 선형화한 것. 우리 modeling."
  - docs/data-contracts.md:100 — `category_source: interbench` (desktop-interactive excerpt); :114-119 `burst_fraction … source: interbench:man-x`
- Wording differences: archetype-plan calls it "burst shape" and "input-driven"; building-plan "on input"; sources.yaml "window-drag emulation" (no input framing).
- Grounds: `desktop-interactive.params.burst_fraction` (uniform 0–1) and `category_source`; foreground bindings of S1, S2, S4, S6 (archetype-plan.md:49).
- Neutral topic: in interbench's man page/source, the X interactive task — what user activity it emulates, how its CPU demand is specified, whether and how that demand varies (range and variation rule), and whether it is driven by input events.

### C-interbench-4 — gaming interactive task
- Source/locator: `interbench` (no locator)
- Locations: dataset/sources.yaml:35 — "gaming unbounded."; docs/workload/source-vetting.md:15 — "gaming = unbounded CPU"; :52 — "**Gaming** unbounded CPU, no deadlines"; docs/workload/grounding-sources.md:27 — "parameter values for audio/video/gaming interactivity"
- Wording differences: grounding-sources says interbench provides gaming "parameter values"; source-vetting says unbounded with no deadlines.
- Grounds: prose only (game-task-chain is parameterized from LAVD).
- Neutral topic: in interbench, the gaming interactive task — how its CPU demand is bounded and whether it carries deadlines.

### C-interbench-5 — Burn background load (thread count; saturation model; cpu-batch class)
- Source/locator: `interbench` / `interbench:man-burn` (building-plan only)
- Locations and verbatim text:
  - dataset/sources.yaml:36 — "Background loads: Burn (4 CPU-bound threads)"
  - docs/references.md:139 — "Burn/Write/Read/Compile loads"
  - dataset/archetypes.yaml:146 — `cpu-batch: category_source: interbench`
  - dataset/archetypes.yaml:158-159 — "interbench Burn is the community's saturation load model; no meas-ci referee needed for \"burns CPU until done\"."
  - dataset/archetypes.yaml:161-163 — "interbench Burn (cross-confirmed by ananicy-rules Heavy_CPU) defines the class: sustained core saturation. Burn's 4-thread structure is not carried"
  - docs/workload/archetype-plan.md:31 — "The inventory was harvested from sources that had already defined their own behavior categories: interbench's interactive and load menus"
  - docs/workload/archetype-plan.md:52 — "`cpu-batch` — run-to-completion, sustained core saturation. category_source: interbench (Burn; cross-confirmed by ananicy-rules `Heavy_CPU`)."
  - docs/workload/building-plan.md:60 — "full-core burn (`interbench:man-burn`)"
  - docs/workload/source-vetting.md:52 — "**Burn** (4 CPU-bound threads default)"
  - docs/workload/grounding-sources.md:27 — "Burn: CPU-bound threads"
  - docs/data-contracts.md:82, :92 — "`category_source: interbench` records where this behavior class comes from — the interbench benchmark's \"Burn\" load is the community's standard model of CPU saturation."
- Wording differences: "4 CPU-bound threads" vs "4 CPU-bound threads default" vs "CPU-bound threads" (no count); "full-core burn" vs "sustained core saturation" vs "community's standard model of CPU saturation"; data-contracts calls interbench "the interbench benchmark".
- Grounds: `cpu-batch.category_source`; `validation_stats.referee: self-consistency`; building-plan table locator `man-burn`.
- Neutral topic: in interbench, the Burn background load — what it runs, its default number of threads or processes, and what CPU behaviour each has.

### C-interbench-6 — Write background load
- Source/locator: `interbench:man-write`
- Locations: dataset/sources.yaml:36-37 — "Write/Read (RAM-scale streaming, cache-defeating)"; dataset/archetypes.yaml:260 — `io-stream: category_source: interbench`; dataset/archetypes.yaml:283-285 — "interbench man-write/man-read establish the class (RAM-scale sequential, cache-defeating streaming)"; docs/workload/archetype-plan.md:57 — "`io-stream` — streaming sequential read/write, throughput-bound. category_source + params: `interbench:man-write` / `interbench:man-read`; shapes refined by `meas-ci`."; docs/workload/building-plan.md:63 — "RAM-scale sequential IO (`interbench:man-write`, `interbench:man-read`)"; docs/workload/source-vetting.md:52 — "**Write** (streaming write, RAM-sized file)"; docs/workload/grounding-sources.md:27 — "Write: streaming disk writes"
- Wording differences: "RAM-scale" vs "RAM-sized file"; "sequential" appears only in archetypes/archetype-plan/building-plan; archetype-plan says params come from man-write/man-read, while archetypes.yaml tags the io-stream params `meas-ci:cli:3`.
- Grounds: `io-stream.category_source`; io-stream class description.
- Neutral topic: in interbench, the Write background load — what it writes, how the written size relates to system memory, and its access pattern.

### C-interbench-7 — Read background load, cache-defeating
- Source/locator: `interbench:man-read`
- Locations: dataset/sources.yaml:36-37 (as above); dataset/archetypes.yaml:283-285 (as above); dataset/archetypes.yaml:289-290 — "The cold-cache rsync copy (vm.drop_caches=3 — matching interbench's cache-defeating intent)"; docs/workload/source-vetting.md:52 — "**Read** (RAM-sized file, cache-defeating)"; docs/workload/archetype-plan.md:57; docs/workload/building-plan.md:63
- Wording differences: archetypes.yaml:283-285 applies "cache-defeating" to the class (write and read); source-vetting applies it to Read only.
- Grounds: io-stream class; the choice of the cold-cache rsync measurement as the io_wait referee (archetypes.yaml:289-291).
- Neutral topic: in interbench, the Read background load — what it reads, how the file size relates to memory, and whether/how it avoids the page cache.

### C-interbench-8 — no per-block timing published for Write/Read (negative claim)
- Locations: dataset/archetypes.yaml:284-285 — "but publish no per-block timing"
- Grounds: justification for io-stream `block_cpu`/`io_wait` carrying `meas-ci` tags and convention values.
- Neutral topic: whether interbench specifies any per-block, per-chunk or per-operation timing for its Write and Read loads.

### C-interbench-9 — Compile background load and its make parallelism
- Source/locator: `interbench` (no locator)
- Locations and verbatim text:
  - dataset/sources.yaml:37 — "Compile (Burn+Write+Read, \"heavy make -j4\")."
  - docs/references.md:139 — "Burn/Write/Read/Compile loads"
  - dataset/archetypes.yaml:248-250 — "parallelism_cap defaults to -j8 by stated convention (archetype-plan OQ-4: between interbench's documented -j4 and desktop nproc conventions)"
  - docs/workload/archetype-plan.md:53 — "(`ocallahan-atc17`: 2,430 mostly short-lived procs; cross-confirmed by interbench Compile, `coetzee-arxiv12`)"
  - docs/workload/archetype-plan.md:86 — "**OQ-4 (parallelism default): resolved — `-j8` by stated convention** (between interbench's documented `-j4` and desktop `nproc` conventions)"
  - docs/workload/source-vetting.md:52 — "**Compile** (Burn+Write+Read, \"heavy make -j4\")"
  - docs/workload/scenario-catalog.md:22 — S11 row "interbench Compile load"
  - docs/workload/grounding-sources.md:27 — "compile-like"
- Wording differences: "heavy make -j4" given in quotation marks as interbench's words; archetype-plan says interbench "documented -j4"; archetype-plan:53 says Compile "cross-confirms" the compiler-child class.
- Grounds: bracketing of the `parallelism_cap` default -j8 (bound as `parallelism_cap: 8` in c1-compile.timeline.yaml:15, c3-workday.timeline.yaml:26, c6-dual.timeline.yaml:18); compiler-child cross-confirmation; S11 row.
- Neutral topic: in interbench, the Compile background load — what it is composed of, whether it runs or emulates `make`, and any parallelism level stated for it.

### C-interbench-10 — the rest of the load/task menu (None, Video, X, Memload, Hack, Custom)
- Locations: docs/workload/source-vetting.md:52 — "**Custom** user CPU%+interval. Background loads: None; Video; X; … **Memload** (110% RAM); Hack (hackbench 50)."; docs/workload/scenario-catalog.md:29 — S18 row "interbench \"None/X\" baseline"
- Grounds: S18 catalog row (taxonomy); otherwise prose only.
- Neutral topic: the complete list of interbench interactive tasks and background loads with each one's definition, including any custom task option, any memory-pressure load and its sizing, and any hackbench-based load and its argument.

### C-interbench-11 — reported metrics, jitter threshold, default duration
- Locations: docs/workload/source-vetting.md:52 — "Metrics: avg latency of met deadlines, jitter SD, max latency, %desired CPU, %deadlines met; ~7 ms human jitter threshold; 30 s default duration."; docs/workload/grounding-sources.md:27 — "measuring latency, jitter, missed deadlines"
- Grounds: prose only.
- Neutral topic: which statistics interbench reports per task, whether it states a human-perception jitter threshold (and its value), and its default run length.

### C-interbench-12 — precedent for foreground-interactive + background-bulk structure
- Locations: docs/workload/grounding-sources.md:27 — "Emulates interactive tasks (audio, video, X, gaming) under background loads … | Direct precedent for the *foreground-interactive + background-bulk* structure of Family 2"
- Grounds: prose only (design precedent).
- Neutral topic: how interbench combines interactive tasks with background loads in a run.

### C-interbench-13 — artifact metadata and community standing (borderline)
- Locations: docs/references.md:138 — "Kolivas, C. interbench. github.com/ckolivas/interbench, GPL-2.0, v0.31 (pin master commit)."; docs/workload/source-vetting.md:52, :90 — "github.com/ckolivas/interbench, GPL-2.0, v0.31"; docs/workload/source-vetting.md:87 — "interbench: packaged in Debian/Gentoo/FreeBSD; scheduler-interactivity literature."; docs/workload/source-vetting.md:14 — "interbench/hackbench/rt-app/stress-ng have LWN-documented or peer-reviewed usage precedents"
- Grounds: citation form / precedent argument, prose only.
- Neutral topic: interbench's author, repository, license and version string; whether distributions package it.

---

## `rt-app`

Status (docs/references.md:145): verified-in-vetting (2026-08-25); pin commit. Type: deployed-system. No locator pattern.

### C-rt-app-1 — JSON task model with run/period/deadline in microseconds
- Locations and verbatim text:
  - dataset/sources.yaml:43-44 — "Establishes the JSON task-model precedent: run/period/deadline in microseconds"
  - docs/references.md:144 — "JSON task-model precedent (run/period/deadline in µs); schema-shape citation for archetypes"
  - docs/workload/source-vetting.md:16 — "rt-app provides the canonical JSON task-model precedent (run/runtime, period, sleep, timer, deadline, loop, instance) in microseconds."
  - docs/workload/source-vetting.md:55 — "libjson-c. JSON fields: instance, loop, run/runtime (µs), sleep (µs), timer{ref,period}, period, deadline; global{duration, calibration, default_policy OTHER/FIFO/RR/DEADLINE, pi_enabled, lock_pages, logdir}."
  - docs/workload/grounding-sources.md:26 — "Reproducible workload simulator; JSON specs of periodic tasks (period, runtime, deadline) | Our `pattern` schema is near-isomorphic to rt-app's task model"
  - docs/workload/building-plan.md:50 — "Format follows the rt-app JSON task model as explicit precedent."
  - docs/workload/archetype-plan.md:10 — "rt-app cited as the schema precedent"
  - docs/simulator/interpretation-contract.md:11 — "integer microseconds throughout (rt-app precedent)"
- Wording differences: field lists differ in length (3 fields vs 7 fields vs full list with `global`); grounding-sources says "periodic tasks".
- Grounds: archetype/canonical schema shape precedent; integer-microsecond time unit.
- Neutral topic: rt-app's JSON configuration format — the per-task and global fields it defines and the time unit of its duration fields.

### C-rt-app-2 — `timer{ref,period}` gives drift-free absolute periodic wakes
- Locations: dataset/sources.yaml:44-45 — "timer{ref,period} gives drift-free absolute periodic wakes (the precedent for our TIMER primitive)"; docs/references.md:144 — "the TIMER primitive (`timer{ref,period}`)"; docs/workload/archetype-plan.md:10 — "including `timer{ref,period}` for TIMER"; docs/simulator/interpretation-contract.md:31 — "`TIMER(period)` | absolute periodic wake: runnable at t₀+k·period regardless of when the previous iteration finished — drift-free (rt-app `timer{ref,period}`). Late iterations accumulate as backlog; they are not silently skipped"
- Wording differences: interpretation-contract places the backlog rule in the same cell as the rt-app attribution (borderline whether backlog behaviour is attributed to rt-app).
- Grounds: TIMER primitive semantics (drift-free absolute grid; borderline: backlog).
- Neutral topic: what rt-app's `timer` event does, what `ref` and `period` mean, whether wake times are absolute or relative to the previous wake, and what happens when an iteration overruns.

### C-rt-app-3 — example template
- Locations: docs/workload/source-vetting.md:55 — "doc/examples/template.json: wake every 100 ms, run 10 ms, SCHED_OTHER, 6 s."
- Grounds: prose only.
- Neutral topic: the contents of rt-app's example template configuration.

### C-rt-app-4 — provenance, license, citation standing (borderline)
- Locations: docs/references.md:143 — "rt-app. github.com/scheduler-tools/rt-app, GPLv2."; docs/workload/grounding-sources.md:26 — "rt-app (ARM/Linaro)"; docs/workload/source-vetting.md:87 — "rt-app: referenced in kernel deadline docs and EAS/scheduler papers."
- Grounds: prose only.
- Neutral topic: rt-app's maintainer organization, license, and whether kernel documentation references it.

Note (not a claim about the source): dataset/sources.yaml:45-46 — "Schema-shape precedent only; no numeric values are derived from it."

---

## `lavd-ossna24`

Status (docs/references.md:171): verified (2026-08-26). Type: deployed-system (talk slides; footnote tier). `locator_pattern: "^s\\d+$"` (dataset/sources.yaml:51). Locators used: `s12`, `s13`, `s14`, `s16-s17` (prose). `frame_period` and `chain_length` carry the bare id.

General wording difference across the group: docs/workload/coreset-guide.md:64 and :184 call the source "LAVD 논문" (LAVD paper); sources.yaml:53 and references.md:169-170 call it talk slides. grounding-sources.md:30 names the source "LAVD design notes (LKML, LPC talks)".

### C-lavd-1 — about 300 tasks per game
- Source/locator: `lavd-ossna24:s12`
- Locations: dataset/sources.yaml:53 — "~300 tasks per game"; docs/references.md:170 — "~300 tasks"; dataset/archetypes.yaml:349-351 — `n_tasks: {dist: constant, value: 300, sampling: per-instance, source: "lavd-ossna24:s12"}`; docs/workload/archetype-plan.md:61 — "~300 tasks"; docs/workload/building-plan.md:59 — "~300 tasks"; docs/workload/source-vetting.md:17 — "~300 tasks/game"; :64 — "~300 tasks while gaming"; docs/workload/coreset-guide.md:191 — "compile 때 constructor가 **task 300개**로 펼쳐요."; :513 — "`game.exe` 300개 task"; docs/data-contracts.md:235 — "the compiled `c1-gaming` contains **300 tasks named `game.exe`**"
- Wording differences: "per game" vs "while gaming"; the constant 300 is a point value for an approximate figure.
- Grounds: `game-task-chain.params.n_tasks` = 300 (consumed by the chain constructor, dataset/tools/wlc/compiler.py:311); recognizer-visible count `game.exe ×300`.
- Neutral topic: on the slides, the number of tasks observed while a game runs, which game(s) and system it was measured on, and whether it is a count, average or range.

### C-lavd-2 — about 90% of tasks are long-lived
- Source/locator: `lavd-ossna24:s12`
- Locations: dataset/sources.yaml:53-54 — "~90% long-lived"; docs/references.md:170 — "~90% long-lived"; dataset/archetypes.yaml:352-354 — `frac_long_lived: {dist: constant, value: 0.90, sampling: per-instance, source: "lavd-ossna24:s12"}`; docs/workload/archetype-plan.md:61 — "~90% long-lived" and "(the source: ~90% long-lived, mostly waiting)"; docs/workload/building-plan.md:59; docs/workload/source-vetting.md:17, :64
- Wording differences: archetype-plan attaches "mostly waiting" to the long-lived figure as "the source".
- Grounds: `frac_long_lived` = 0.90. Factual note: no tool in dataset/tools reads `frac_long_lived` (grep over dataset/tools finds no reference).
- Neutral topic: on the slides, the share of tasks classified as long-lived versus short-lived during gaming, and how "long-lived" is defined.

### C-lavd-3 — wine/graphics/audio servers take 30–40% of scheduling
- Source/locator: `lavd-ossna24:s12`
- Locations: dataset/sources.yaml:54 — "wine/graphics/audio servers take 30-40% of scheduling (s12)"
- Grounds: prose only.
- Neutral topic: on the slides, which non-game server processes appear among scheduled tasks and what share of scheduling activity they account for, and how "share of scheduling" is measured.

### C-lavd-4 — wine is part of the game's task graph / cross-layer task chains
- Source/locator: `lavd-ossna24:s12`
- Locations: dataset/archetypes.yaml:513-516 — "wineserver -> system-daemon is a provisional approximation — LAVD treats wine as part of the game's task graph (lavd-ossna24:s12)"; docs/workload/archetype-plan.md:76 — "LAVD treats wine as part of the game's task graph (`lavd-ossna24:s12`)"; docs/workload/coreset-guide.md:995 — "LAVD는 wine을 게임 task graph의 일부로 봐요."; docs/workload/scenario-catalog.md:20 — S9 "LAVD characterization (wine/graphics/audio task chains)"; docs/workload/grounding-sources.md:30 — "cross-layer task chains (game engine, Wine, graphics driver)"
- Wording differences: "task graph" vs "task chains"; grounding-sources lists "graphics driver", scenario-catalog "audio".
- Grounds: binding note on `wineserver` → `system-daemon` (c1-gaming.timeline.yaml:19, c2-p2a.timeline.yaml:18, c3-evening.timeline.yaml:26, c6-dual.timeline.yaml:19); S9 names `wineserver`; open item interpretation-contract.md:62.
- Neutral topic: on the slides, whether wine/wineserver (and graphics/audio components) are shown as linked with game tasks in the waker/wakee relationships, and at which slide.

### C-lavd-5 — per-schedule runtime magnitudes (wineserver and worker figures)
- Source/locator: `lavd-ossna24:s13`
- Locations and verbatim text:
  - dataset/sources.yaml:55-56 — "per-schedule runtimes few-hundred-us average to few-ms max (wineserver ~260 us, worker ~1.65 ms)"
  - docs/references.md:170 — "per-schedule runtimes ~260 µs–1.65 ms"
  - dataset/archetypes.yaml:355-357 — `per_schedule_run: {dist: lognormal, anchor_min_us: 260, anchor_max_us: 1650, sampling: per-task, source: "lavd-ossna24:s13"}`
  - dataset/archetypes.yaml:390-393 — "anchors are the source's wineserver ~260 us and worker ~1.65 ms endpoints, lognormal family by OQ-5 convention (the compiler derives median/sigma treating the anchors as the p05/p95 span)."
  - dataset/tools/wlc/sampling.py:30-32 — "Derive (median, sigma) treating the anchors as the p05/p95 span (game-task-chain modeling_notes)."
  - docs/workload/archetype-plan.md:61 — "per-schedule RUN 260 µs–1.65 ms"
  - docs/workload/building-plan.md:59 — "per-schedule runtime ~260 µs–1.65 ms"
  - docs/workload/source-vetting.md:17 — "per-schedule runtimes few-hundred-µs to few-ms (wineserver ~260 µs, worker ~1.65 ms)"
  - docs/workload/source-vetting.md:64 — "per-schedule runtime few-100 µs avg to few-ms max (wineserver ≈260 µs, worker ≈1.65 ms)"
  - docs/workload/coreset-guide.md:192 — "각 stage의 RUN은 task마다 고정(260 µs–1.65 ms 범위의 lognormal)."
  - docs/workload/grounding-sources.md:30 — "Characterization of gaming workloads: very short task durations" / "burst lengths"
- Wording differences: sources.yaml and source-vetting:64 frame the magnitudes as "average" and "max"; references.md, archetype-plan, building-plan present a range "260 µs–1.65 ms"; archetypes.yaml calls them "endpoints" and the compiler treats them as 5th/95th percentiles; coreset-guide as a "범위" (range). Whether 260 µs and 1.65 ms are each an average for one task or the extremes of a distribution is stated differently across locations.
- Grounds: `per_schedule_run` anchors 260 / 1650 us → derived lognormal median/sigma (sampling.py:30-35); chain stage RUN values.
- Neutral topic: on the slides, the per-schedule runtime figures reported for game-related tasks — which tasks are named, what statistic each figure is (average, maximum, percentile), and the values.

### C-lavd-6 — per-task runtime is stable and predictable
- Source/locator: `lavd-ossna24:s13`
- Locations: dataset/sources.yaml:56 — "stable and predictable per task (s13)"; dataset/archetypes.yaml:389-390 — "per_schedule_run samples per-task because the source states per-task runtime is stable (s13)"; docs/workload/archetype-plan.md:61 — "(per-task sampling — the source says per-task runtime is stable)"; docs/simulator/interpretation-contract.md:58 — "*per-task* (one draw reused across iterations — e.g. per-schedule runtime, matching the source's \"stable per task\")"; docs/workload/coreset-guide.md:192 — "task마다 고정"
- Wording differences: interpretation-contract quotes "stable per task" as the source's words.
- Grounds: `per_schedule_run.sampling: per-task` (one draw per chain member).
- Neutral topic: on the slides, whether a task's runtime per scheduling is described as consistent over time, and in what terms.

### C-lavd-7 — 70–75% of scheduling initiated by waiting syscalls
- Source/locator: `lavd-ossna24:s14`
- Locations: dataset/sources.yaml:56-57 — "70-75% of scheduling initiated by waiting syscalls (s14)"; docs/references.md:170 — "70–75% wakeups from waiting syscalls"; dataset/archetypes.yaml:358-360 — `frac_wakeups_from_wait: {dist: uniform, min: 0.70, max: 0.75, sampling: per-instance, source: "lavd-ossna24:s14"}`; docs/workload/archetype-plan.md:61 — "70–75% wakeups from waiting syscalls"; docs/workload/building-plan.md:59 — same; docs/workload/source-vetting.md:17 — "70–75% of switches from waiting syscalls"; :64 — "25–30% timer preemption vs 70–75% waiting syscalls (epoll, pipe_read, futex_wait)"
- Wording differences: "scheduling initiated by" vs "wakeups from" vs "switches from"; source-vetting:64 adds the complementary timer-preemption share and syscall examples.
- Grounds: `frac_wakeups_from_wait` uniform [0.70, 0.75]. Factual note: no tool in dataset/tools reads this field.
- Neutral topic: on the slides, the breakdown of what causes scheduling events (e.g. blocking system calls vs timer preemption) during gaming, the shares, and any named system calls.

### C-lavd-8 — tasks linked in waiter–waker graphs; a task sequence serves one job from input to display
- Source/locator: `lavd-ossna24:s16-s17`
- Locations: dataset/sources.yaml:57-59 — "tasks tightly linked in waiter-waker graphs, a task sequence serving one job from input to display (s16-s17)"; dataset/archetypes.yaml:385-389 — "the compiler's chain constructor expands it into n_tasks ordinary tasks with WAIT/WAKE channels wired input -> engine -> ... -> display; the linearization of the s16-s17 waker-waiter graph into a chain, and every field name, are ours."; docs/workload/archetype-plan.md:61 — "waker–waiter chain topology"; docs/workload/building-plan.md:59 — "waker–waiter chain"; docs/workload/source-vetting.md:64 — "waiter–waker task chains (input→display)"; docs/simulator/interpretation-contract.md:62 — "(input → engine → … → display)"; docs/workload/coreset-guide.md:186-192
- Wording differences: "graph" (sources.yaml, archetypes notes) vs "chain(s)" (archetype-plan, building-plan, source-vetting); "engine" stage appears only in archetypes.yaml and interpretation-contract.
- Grounds: `game-task-chain` `constructor: chain` and WAIT/WAKE wiring (structure).
- Neutral topic: on the slides, how game-related tasks wake one another (the depicted structure, its shape, and the stages it names between input and output).

### C-lavd-9 — 16.7 ms frame budget; 15 ms targeted latency
- Source/locator: `lavd-ossna24` (no locator in sources.yaml notes or the archetypes tag)
- Locations: dataset/sources.yaml:59 — "16.7 ms frame budget, 15 ms targeted latency"; docs/references.md:170 — "16.7 ms frame budget"; dataset/archetypes.yaml:361-363 — `frame_period: {dist: constant, value_us: 16667, sampling: per-instance, source: "lavd-ossna24"}`; docs/workload/archetype-plan.md:61 — "16.7 ms frame budget"; docs/workload/building-plan.md:59 — same; docs/workload/source-vetting.md:17 — "16.7 ms frame deadline / 15 ms targeted latency"; :64 — "16.7 ms frame budget, 15 ms targeted latency"; docs/workload/grounding-sources.md:30 — "the 16ms-frame deadline"; docs/workload/coreset-guide.md:192 — "1번만 `TIMER(16667)`을 갖고"; docs/data-contracts.md:235 — "wait for the next tick of a 16,667 µs metronome (that's 60 frames per second)"; daemon/driver-table/prior.yaml:191 — "Game frames are periodic deadlines (the chain's 16.7 ms period, …)"
- Wording differences: "budget" vs "deadline" vs "period"; "16ms" vs "16.7 ms" vs 16,667 µs; data-contracts adds "60 frames per second".
- Grounds: `frame_period` = 16667 us (chain head TIMER period; also the lane-scaling denominator, compiler.py:314-321); prior table gaming rows' EDF justification.
- Neutral topic: on the slides, the frame time budget and any targeted latency value stated for the gaming scenario, and the frame rate it corresponds to.

### C-lavd-10 — top 30–40 tasks account for 95% of scheduling
- Source/locator: `lavd-ossna24` (no locator)
- Locations: dataset/sources.yaml:59-60 — "top 30-40 tasks = 95% of scheduling"; docs/references.md:170 — "top 30–40 tasks = 95% of scheduling … Also the concentration statistics defending our single-lane scaling of `game-task-chain`"; dataset/archetypes.yaml:397-399 — "Lane-scaling defense: LAVD's own concentration statistics (top 30-40 tasks = 95% of scheduling; 15-20 game tasks take 60-70%) justify scaling the frame-critical chain while keeping the near-idle tail"; docs/workload/archetype-plan.md:61 — "defended by the source's own concentration statistics (top 30–40 tasks = 95% of scheduling; 15–20 take 60–70%)"; docs/workload/building-plan.md:167 — "(`game-task-chain`'s defense: LAVD's own concentration statistics, top 30–40 tasks = 95% of scheduling)"; docs/workload/source-vetting.md:17 — "top 30–40 tasks = 95% of scheduling"; :64 — same
- Grounds: lane-scaling pass for game-task-chain (`scalable` rule, archetypes.yaml:375-379); `lane_share` binding.
- Neutral topic: on the slides, how concentrated scheduling activity is across tasks (how many top tasks account for what share) and how the share is measured.

### C-lavd-11 — 15–20 game tasks take 60–70% (and the "frame-critical" band)
- Source/locator: `lavd-ossna24` (no locator)
- Locations: dataset/sources.yaml:60 — "15-20 game tasks take 60-70%"; docs/references.md:170 — "(15–20 take 60–70%)"; dataset/archetypes.yaml:364-366 — `chain_length: {dist: constant, value: 16, sampling: per-instance, source: "lavd-ossna24"}`; dataset/archetypes.yaml:393-394 — "chain_length 16 sits in the source's 15-20 frame-critical band"; dataset/archetypes.yaml:398-399 (as C-lavd-10); docs/workload/archetype-plan.md:61 — "(top 30–40 tasks = 95% of scheduling; 15–20 take 60–70%)"; docs/workload/source-vetting.md:64 — "(15–20 game tasks take 60–70%)"; docs/workload/coreset-guide.md:291 — "LAVD 스스로 \"상위 15–20개 task가 scheduling의 60–70%를 차지한다\"고 하니, frame-critical chain의 aggregate demand를 lane 기준으로 잡고 tail은 거의 놀게 두는 게 방어 가능한 근사예요."
- Wording differences: "15-20 game tasks" (sources.yaml, source-vetting:64) vs "15-20 frame-critical band" (archetypes) vs "상위 15–20개 task" (top 15–20 tasks, coreset-guide, presented as a quote); coreset-guide cites this figure (not the 30–40/95% one) as the lane-scaling justification.
- Grounds: `chain_length` = 16; lane-scaling defense.
- Neutral topic: on the slides, the number of game (as opposed to non-game) tasks that dominate scheduling, their combined share, and whether they are described as frame-critical or as a pipeline.

### C-lavd-12 — the remaining tasks are "mostly waiting" (near-idle tail) (borderline)
- Source/locator: `lavd-ossna24:s12` (tag on tail params)
- Locations: dataset/archetypes.yaml:394-397 — "the tail (n_tasks - chain_length near-idle tasks) encodes the source's \"mostly waiting\" long tail — tail param values are our placeholder encoding of near-idle, provisional like any meas-pending value"; dataset/archetypes.yaml:367-372 — `tail_idle_gap … source: "lavd-ossna24:s12"`, `tail_run … source: "lavd-ossna24:s12"`; docs/workload/archetype-plan.md:61 — "the full task population is instantiated with the long tail near-idle (the source: ~90% long-lived, mostly waiting)"; docs/workload/coreset-guide.md:193 — "LAVD가 말하는 \"300개 중 대부분은 기다리는 중\"을 encoding."
- Wording differences: coreset-guide quotes "most of the 300 are waiting" as LAVD's statement; archetypes quotes "mostly waiting".
- Grounds: tail structure (284 near-idle tasks per game); tags on `tail_idle_gap`, `tail_run` (values called placeholders — see Part 2(a)).
- Neutral topic: on the slides, what is said about the activity of tasks outside the dominant set (idle, waiting, or otherwise), and at which slide.

### C-lavd-13 — CPU utilization while gaming
- Locations: docs/workload/source-vetting.md:64 — "CPU util 65–95%"
- Grounds: prose only.
- Neutral topic: on the slides, any CPU utilization figure reported during gaming.

### C-lavd-14 — metric correspondences (FPS vs throughput / tail)
- Locations: docs/workload/source-vetting.md:64 — "Avg FPS ≈ throughput, Low-1% FPS ≈ p99."
- Grounds: prose only.
- Neutral topic: on the slides, how game frame-rate metrics are related to scheduler performance metrics.

### C-lavd-15 — gaming numbers measured on multi-core machines (machine-aggregate) (borderline)
- Locations: docs/workload/building-plan.md:167 — "archetype values whose sources are machine-aggregate (measured on multi-core machines — the gaming chain's utilization and worker concurrency; almost nothing else …)"; docs/simulator/interpretation-contract.md:66 — "Archetype values whose sources are machine-aggregate (measured on multi-core machines)"; docs/workload/coreset-guide.md:291 — "LAVD의 숫자는 multi-core machine에서 잰 것이라 single lane에 그대로 넣으면 의미가 달라져요."
- Grounds: the decision to lane-scale only game-task-chain.
- Neutral topic: on the slides, the hardware (core count) and system on which the gaming observations were collected.

### C-lavd-16 — companion apps observed alongside games (borderline)
- Locations: docs/workload/scenario-catalog.md:16 — S5 row "LAVD gaming context (companion apps observed alongside games)"
- Grounds: S5 catalog row (discord overlay; c3-evening.timeline.yaml:11 tags S5; c4-gaming injects `discord`, c4.variant.yaml:9-10).
- Neutral topic: on the slides, whether non-game applications (chat/voice/overlay) are mentioned or shown running during gaming.

### C-lavd-17 — tail latency perceived as stutter; very short task durations
- Locations: docs/workload/grounding-sources.md:30 — "Characterization of gaming workloads: very short task durations, cross-layer task chains (game engine, Wine, graphics driver), tail latency perceived as stutter"
- Grounds: prose only (Role B justification).
- Neutral topic: on the slides, how task durations are characterized and how latency outliers relate to user-perceived frame problems.

### C-lavd-18 — production concern: Valve ships it; Meta adopted the scheduler server-side (borderline: may belong to `scx` or other sources)
- Locations: docs/workload/grounding-sources.md:30 — "also the claim that desktop/gaming scheduling is a live production concern (Valve ships it; Meta adopted the scheduler server-side)"
- Grounds: prose only.
- Neutral topic: which organizations are stated to ship or deploy the LAVD scheduler, and in what setting.

### C-lavd-19 — LAVD defines no spec format (borderline)
- Locations: dataset/sources.yaml:60-61 — "LAVD defines no spec format"
- Grounds: attribution of the chain schema encoding to "our modeling".
- Neutral topic: whether the talk or the scheduler provides any workload description format.

### C-lavd-20 — talk metadata
- Locations: docs/references.md:169 — "Min, C. (2024). \"Optimizing Scheduler for Linux Gaming.\" Talk, Open Source Summit North America 2024, Seattle, 2024-04-17. Slides: static.sched.com/hosted_files/ossna2024/9b/scx-lavd-oss-na24.pdf"; docs/workload/source-vetting.md:17 — "LAVD (Changwoo Min, OSS NA 2024)"; :64 — "github.com/sched-ext/scx (GPLv2); OSS NA 2024 slides (Changwoo Min); LWN LPC 2025 coverage."
- Grounds: citation form.
- Neutral topic: speaker, title, event, date and slide URL of the talk.

---

## `corbet-lwn24` (docs/references.md only; not in sources.yaml)

Status (docs/references.md:176): verified (2026-08-26).

### C-corbet-1 — LWN article covers scx_lavd in a dedicated section
- Locations: docs/references.md:175 — "prose-citable secondary for the LAVD characterization (dedicated \"Higher frame rates\" section on scx_lavd)"; docs/references.md:170 — "pair with `corbet-lwn24` for prose-citable coverage"; docs/workload/source-vetting.md:64 — "LWN LPC 2025 coverage"; docs/workload/grounding-sources.md:74 — "LAVD/LWN-covered work"
- Wording differences: references.md cites "Sched_ext at LPC 2024" (2024-09-26); source-vetting says "LWN LPC 2025 coverage".
- Grounds: prose only (secondary citation for C-lavd-* figures).
- Neutral topic: the LWN article on sched_ext at LPC — its date, which conference year it covers, whether it has a section on scx_lavd and what gaming characterization that section gives.

### C-corbet-2 — later LWN article (borderline)
- Locations: docs/references.md:175 — "Later option to evaluate: \"Lessons from creating a gaming-oriented scheduler\", LWN, Jan 2026 (lwn.net/Articles/1051430/ — byline unverified)."
- Grounds: none.
- Neutral topic: whether that LWN article exists, its date and author.

## `scx` (docs/references.md only) — borderline dataset-side use

Status (docs/references.md:166): verified-in-vetting (2026-08-25); re-confirmed 2026-09-12.

### C-scx-1 — scx repository as a LAVD source; license
- Locations: docs/workload/source-vetting.md:64 — "github.com/sched-ext/scx (GPLv2)"; :90 — "scx_lavd github.com/sched-ext/scx GPLv2"
- Grounds: prose only.
- Neutral topic: whether scx_lavd lives in the sched-ext/scx repository and the repository's license.

---

## `ocallahan-atc17`

Status (docs/references.md:108): verified (2026-08-26). Type: scholarly. `locator_pattern: "^sec-[0-9.]+$"` (dataset/sources.yaml:68). Locator used: `sec-4.3` (prose only; no `source:` tag in archetypes.yaml carries this id — it appears as `category_source` and in modeling_notes).

### C-ocallahan-1 — "make forks and execs 2430 processes, mostly short-lived" in the kernel-build workload
- Source/locator: `ocallahan-atc17:sec-4.3`
- Locations and verbatim text:
  - dataset/sources.yaml:70-72 — "\"make forks and execs 2430 processes, mostly short-lived\" (sec-4.3, Linux kernel-build workload; written \"2430\" in the paper). Grounds the fork-burst count and short-lived character of compiler children only"
  - docs/references.md:107 — "\"make forks and execs 2430 processes, mostly short-lived\" (§4.3, kernel-build workload; written \"2430\" in the paper); grounds `compiler-child`/`build-orchestrator` structure."
  - dataset/archetypes.yaml:174, :224 — `category_source: ocallahan-atc17` (compiler-child, build-orchestrator)
  - dataset/archetypes.yaml:202-204 — "The kernel-build literature grounds the class's existence and short-lived character only (ocallahan-atc17 sec-4.3: \"make forks and execs 2430 processes, mostly short-lived\"; …)"
  - dataset/archetypes.yaml:247-248 — "spawn_count binds per timeline — the kernel-build default is 2,430 (ocallahan-atc17 sec-4.3)."
  - docs/workload/archetype-plan.md:31 — "the kernel-build literature's compile fork-burst"
  - docs/workload/archetype-plan.md:53 — "category_source: kernel-build characterization (`ocallahan-atc17`: 2,430 mostly short-lived procs; …)"
  - docs/workload/archetype-plan.md:54 — "category_source: kernel-build literature + make -jN convention."
  - docs/workload/building-plan.md:61 — "fork-burst under a parent; 2,430 procs per kernel build (`ocallahan-atc17`)"
  - docs/workload/building-plan.md:62 — "spawns compiler-child bursts (`ocallahan-atc17`, `coetzee-arxiv12`)"
  - docs/workload/source-vetting.md:70 — "kernel build forks/execs **2,430 mostly short-lived processes** (\"2430\" in the paper, §4.3; next workload: 89)"
  - docs/workload/source-vetting.md:95 — "hackbench + kernel-build (2,430 short-lived procs) for compile/IPC"; :123 — "Kernel build | B | Usable | 2,430 short-lived procs"
  - docs/workload/scenario-catalog.md:22 — S11 row "kernel-build characterization (2,430 short-lived procs, arXiv 1705.05937)"
  - docs/simulator/interpretation-contract.md:56 — "(e.g. 2,430 compiler children, lifetimes already drawn)" (borderline, no id)
- Wording differences: "processes" (quote) vs "procs" vs "compiler children" (sources.yaml:72, interpretation-contract); "mostly short-lived" vs "short-lived" (source-vetting:95, :123, scenario-catalog); "per kernel build" (building-plan) vs "kernel-build workload"; "the kernel-build default is 2,430" (archetypes) — no timeline binds 2,430 (bound spawn counts are 100, 4200, 85; see Part 2(b)). scenario-catalog cites the arXiv TR number rather than the id.
- Grounds: `compiler-child` and `build-orchestrator` `category_source`; the prose binding-time default `spawn_count` 2,430; S11 row.
- Neutral topic: in the paper's section describing its benchmark workloads, what the kernel-build workload builds and how it is configured; any stated count of processes forked/exec'd by make and any characterization of their lifetimes; the next workload listed and its count.

### C-ocallahan-2 — the paper gives no lifetime distribution (negative claim)
- Locations: dataset/sources.yaml:72-73 — "the paper gives no lifetime distribution."
- Grounds: justification for compiler-child lifetimes coming from meas-ci.
- Neutral topic: whether the paper reports any distribution or summary statistic of the lifetimes of the processes in its kernel-build workload.

### C-ocallahan-3 — bibliographic identity
- Locations: docs/references.md:106 — "O'Callahan, R., Jones, C., Froyd, N., Huey, K., Noll, A., & Partush, N. (2017). Engineering Record and Replay for Deployability. *Proc. USENIX ATC '17*, 377–389. Extended technical report: arXiv:1705.05937."; docs/workload/source-vetting.md:70 — "Record-and-replay study [rev.3 — identified]: **O'Callahan et al., \"Engineering Record and Replay for Deployability,\" USENIX ATC '17** (extended TR = arXiv 1705.05937; `ocallahan-atc17`)"
- Grounds: citation form. Note: the quoted count is attributed to "§4.3" of "the paper" while the identity pairs an ATC paper with an arXiv extended TR; which version carries §4.3 is not stated.
- Neutral topic: authors, title, venue, pages; whether arXiv:1705.05937 is an extended version; which version has a section numbered 4.3 with the workload description.

## `coetzee-arxiv12`

Status (docs/references.md:113): verified (2026-08-26). Type: scholarly (preprint). `locator_pattern: "^sec-[0-9.]+$"`. Locator used: `sec-9` (prose only).

### C-coetzee-1 — "the Linux kernel build's enormous number of short-lived processes"
- Source/locator: `coetzee-arxiv12:sec-9`
- Locations: dataset/sources.yaml:79-82 — "\"the Linux kernel build's enormous number of short-lived processes\" (sec-9). The characterization is specific to the Linux kernel build, not builds generally — cite it that way. Preprint (UCB TR); secondary corroboration behind ocallahan-atc17."; docs/references.md:112 — "\"the Linux kernel build's enormous number of short-lived processes\" (§9). Scope note: the quote is about the *Linux kernel build* specifically, not builds in general"; dataset/archetypes.yaml:204-205 — "coetzee-arxiv12 sec-9 corroborates, kernel-build-specific"; docs/workload/archetype-plan.md:53 — "cross-confirmed by interbench Compile, `coetzee-arxiv12`"; docs/workload/building-plan.md:62 — "spawns compiler-child bursts (`ocallahan-atc17`, `coetzee-arxiv12`)"; docs/workload/source-vetting.md:70 — "Build-systems paper [rev.3 — identified]: **Coetzee, Bhaskar & Necula** (arXiv 1203.2704, preprint/UCB TR only; `coetzee-arxiv12`): \"the Linux kernel build's enormous number of short-lived processes\" — kernel-build-specific"
- Wording differences: building-plan:62 cites it for build-orchestrator "compiler-child bursts" (spawn structure), beyond the short-lived characterization.
- Grounds: corroboration of compiler-child/build-orchestrator class existence.
- Neutral topic: in the paper's section 9 (or wherever it appears), what is said about the Linux kernel build's processes — their number and lifetimes — and whether the statement is specific to that build.

### C-coetzee-2 — bibliographic identity
- Locations: docs/references.md:111 — "Coetzee, D., Bhaskar, A., & Necula, G. (2012). A model and framework for reliable build systems. arXiv:1203.2704 / UC Berkeley TR UCB/EECS-2012-27. **Preprint — no venue.**"; dataset/sources.yaml:81 — "Preprint (UCB TR)"; docs/workload/source-vetting.md:70
- Neutral topic: authors, title, year, arXiv number, TR number, venue status.

## Kernel build — plain-text citations (no id)

### C-kernelbuild-1 — kernel documentation on make -j (borderline)
- Locations: docs/workload/source-vetting.md:70 — "Kernel docs: sched_child_runs_first, SCHED_AUTOGROUP motivated by make -j."
- Grounds: prose only.
- Neutral topic: in Linux kernel documentation, what `sched_child_runs_first` and `SCHED_AUTOGROUP` are and whether the documentation motivates either with parallel builds.

### C-kernelbuild-2 — kernel build as the standard compile workload in scheduler evaluations (borderline)
- Locations: docs/workload/grounding-sources.md:32 — "kernel build (make -jN) | The de facto standard compile workload in every scheduler evaluation, including SchedCP's | The compile Family's fork-heavy, short-lived-children structure"; docs/workload/source-vetting.md:70 — "Grounds compile family: fork-heavy burst of short-lived cc1/ld/as + few long-lived make/linker."
- Wording differences: source-vetting adds "few long-lived make/linker" (not in any quoted source).
- Grounds: compile family structure (prose).
- Neutral topic: whether scheduler evaluations commonly use a kernel build; what process structure (short-lived compiler processes vs long-lived make/linker) any cited source describes.

## `schedcp-mlsys25` — plain-text "SchedCP" citations on the dataset side (references.md entry is related-work only)

Status (docs/references.md:317): verified (2026-09-12; v4 full text).

### C-schedcp-1 — SchedCP benchmarks make -j172 on Linux 6.14
- Locations: docs/workload/source-vetting.md:70 — "SchedCP benchmarks make -j172 on Linux 6.14."; docs/workload/scenario-catalog.md:22 — S11 "SchedCP (make -j)"; docs/workload/grounding-sources.md:32 — "including SchedCP's"; docs/references.md:316 — "the kernel-compilation workload as \"tinyconfig, 'make -j 172' on 6.14 source\""
- Grounds: S11 row.
- Neutral topic: the kernel-compilation workload configuration in the SchedCP paper (config target, make parallelism, kernel version).

### C-schedcp-2 — SchedCP batch workloads include video transcoding and file compression
- Locations: docs/workload/scenario-catalog.md:19 — S8 "SchedCP batch workloads (video transcoding)"; :27 — S16 "SchedCP batch (file compression)"
- Grounds: S8, S16 rows.
- Neutral topic: the list of batch workloads evaluated in SchedCP.

### C-schedcp-3 — SchedCP evaluates batch/ML-adjacent workloads on desktop-class machines
- Locations: docs/workload/scenario-catalog.md:23 — S12 "SchedCP evaluation (batch/ML-adjacent workloads on desktops-class machines)"
- Grounds: S12 row.
- Neutral topic: the machines and workload categories used in SchedCP's evaluation.

### C-schedcp-4 — SchedCP cites schbench by git URL; venue
- Locations: docs/workload/source-vetting.md:14 — "SchedCP (arXiv 2509.01245, MLforSystems @ NeurIPS 2025) cites schbench by git URL"; :87 — "schbench: cited by SchedCP (MLforSystems @ NeurIPS 2025) by git URL — confirmed."; docs/references.md:149 — "cited by git URL in SchedCP (citation-precedent argument)"
- Wording differences: references.md:315 gives the venue as "ML for Systems 2025 (arXiv journal-ref)" without "@ NeurIPS".
- Grounds: citation-precedent argument (prose).
- Neutral topic: how SchedCP references schbench in its bibliography; SchedCP's venue.

### C-schedcp-5 — SchedCP notes a complete benchmark remains future work
- Locations: docs/workload/grounding-sources.md:60 — "(SchedCP's own evaluation notes that a complete benchmark remains future work)"; docs/references.md:316 — "\"All experiments successfully created working custom scheduler configurations or eBPF programs. Future evaluation requires a complete benchmark.\""
- Grounds: prose only (motivation for releasing the suite).
- Neutral topic: what SchedCP says about the completeness of its evaluation benchmark.

---

## `cpsmark-tbench23`

Status (docs/references.md:33): verified (source-vetting full-text review, 2026-08-25). Type: scholarly. `locator_pattern: "^(table-\\d+|sec-[0-9.]+)$"`. Locators used: `table-1`, `table-2`, `table-4` (prose); `cpsmark-tbench23:table-4` appears in docs/workload/archetype-plan.md:69.

### C-cpsmark-1 — four office usage scenarios merged into two modules (CA, CC) with weight classes and user types
- Locations: dataset/sources.yaml:90-91 — "four office usage scenarios merged into two modules (CA light/middleweight, CC heavyweight)"; docs/references.md:32 — "scenario taxonomy"; docs/workload/source-vetting.md:28 — "**Four usage scenarios**, merged into two modules: *Comprehensive Application* (CA = document manipulation + Internet service; light/middleweight, task & knowledge workers) and *Comprehensive Calculation* (CC = graphic design + multimedia processing; heavyweight, power users)."; docs/workload/scenario-catalog.md:33 — "CpsMark+'s four scenarios to S1+S16, S2+S4, S6, S7+S8"
- Grounds: scenario taxonomy (Role A); catalog coverage check.
- Neutral topic: CpsMark+'s usage scenarios — how many, their names, how they are grouped into modules, and the user types or weight classes associated with each module.

### C-cpsmark-2 — user-profile tiers (Table 1)
- Locations: dataset/sources.yaml:91 — "user-profile tiers (table-1)"; docs/workload/source-vetting.md:29 — "**User-profile tiers (Table 1):** Task workers / Knowledge workers / Power users, each with stated performance requirements"
- Grounds: prose only.
- Neutral topic: the content of CpsMark+ Table 1 — user categories and what is stated for each.

### C-cpsmark-3 — named applications with versions (Table 2)
- Locations: dataset/sources.yaml:92 — "named applications with versions (table-2)"; docs/references.md:32 — "named app lists (Table 2)"; docs/workload/source-vetting.md:30 — "PowerPoint/Word/Excel/Outlook 2016, Acrobat DC, WinRAR 5.91, Chrome 73, Photoshop CC 2019, AutoCAD 2018, 3ds Max 2018, Premiere Pro CC 2019, After Effects CC 2019, HandBrake CLI 1.3.0 — market-research-selected real process names"; docs/workload/scenario-catalog.md:5 — "The grounding sources attest to process *names* (CpsMark+ Table 2, SYSmark app lists, the ananicy catalog)"; docs/workload/source-vetting.md:94 — "**Borrow CpsMark+'s named app list (Table 2)**"
- Wording differences: source-vetting calls the list "market-research-selected real process names"; scenario-catalog says the source attests "process names" (Table 2 lists application products/versions).
- Grounds: names-only schema decision (scenario-catalog.md:5); S1, S2, S4, S6, S7, S8, S16 rows.
- Neutral topic: the content of CpsMark+ Table 2 — application names and versions, and how the applications were selected.

### C-cpsmark-4 — which applications belong to which CpsMark+ scenario (as used in the catalog)
- Locations: docs/workload/scenario-catalog.md:12 — S1 "CpsMark+ Table 2 document manipulation (Word/Excel/PowerPoint/Acrobat → LibreOffice/evince)"; :13 — S2 "CpsMark+ Internet service (Chrome 73)"; :15 — S4 "CpsMark+ Internet service (Outlook → Thunderbird)"; :17 — S6 "CpsMark+ graphic design (Photoshop CC 2019 → GIMP)"; :18 — S7 "CpsMark+ multimedia processing (Premiere/After Effects/3ds Max → kdenlive/Blender)"; :19 — S8 "CpsMark+ multimedia processing (HandBrake CLI 1.3.0 — verbatim, cross-platform)"; :27 — S16 "CpsMark+ document manipulation (WinRAR 5.91 → 7z)"
- Wording differences: the Linux targets after "→" are ours (sources.yaml:95-96 "the Linux name mapping is ours"); "verbatim, cross-platform" is asserted for HandBrake CLI.
- Grounds: S1, S2, S4, S6, S7, S8, S16 source column; names bound in timelines (soffice.bin, chrome, thunderbird, gimp, kdenlive, HandBrakeCLI, 7z).
- Neutral topic: in CpsMark+, which named application is used in which usage scenario/workload.

### C-cpsmark-5 — CA cooperative workflow ordering
- Locations and verbatim text:
  - dataset/sources.yaml:92-94 — "CA cooperative workflow ordering (Internet -> creation -> document processing -> email delivery)"
  - docs/references.md:32 — "CA workflow ordering (Role C)"
  - docs/workload/source-vetting.md:32 — "CA workloads execute as a coherent user-behavior sequence (resource preparation via Internet → content creation → document processing → email delivery), with earlier workloads' outputs feeding later workloads' inputs (Office docs → Acrobat PDF conversion → WinRAR archive → Outlook attachment)."
  - docs/workload/source-vetting.md:78, :94 — "(Internet → creation → document processing → email)", :96 — "ordering per CpsMark+ CA workflow"
  - docs/workload/building-plan.md:98 — "**workday arc** (~4 segments): chrome research → +soffice.bin writing → +make compile → mail send. Ordering grounded in the CpsMark+ CA cooperative workflow (`cpsmark-tbench23`)."
  - docs/workload/building-plan.md:137 — "the CpsMark+ CA workflow grounds the canonical excursion ordering around an office hub"
  - dataset/timelines/coreset/c3-workday.timeline.yaml:1-3 — "chrome research -> +soffice writing -> +make compile -> mail send. Ordering grounded in the CpsMark+ CA cooperative workflow (cpsmark-tbench23)."
  - docs/workload/coreset-guide.md:708 — "chrome 검색 → LibreOffice 글쓰기 → make 빌드 시작 → Thunderbird 메일 → 메일 전송. CpsMark+의 협업 workflow 순서."
  - docs/workload/scenario-catalog.md:15 — S4 "CpsMark+ CA workflow (email delivery stage)"
- Wording differences: the c3-workday arc inserts a compile stage (`make`) that none of the source-side descriptions of the CA workflow list; "content creation" vs "creation"; the output-to-input chain appears only in source-vetting:32.
- Grounds: c3-workday segment order (browsing 0–60 s, office 60–120 s, compile 120–360 s, mail 360–420 s; c3-workday.timeline.yaml:9-16); planned naturalistic excursion ordering; S4 row.
- Neutral topic: in CpsMark+, whether CA workloads run in a fixed order, what the stages are and their order, and whether outputs of one workload feed the next (and which files).

### C-cpsmark-6 — Table 4 hardware sensitivity (GPU sensitivity of CC vs CA; CPU/storage sensitivity of specific workloads)
- Locations: dataset/sources.yaml:94-95 — "per-workload hardware sensitivity (table-4: CC up to 1.77x GPU-sensitive, CA ~1.0x)"; docs/references.md:32 — "resource-mix sensitivity (Table 4, Role B)"; docs/workload/source-vetting.md:33 — "per-workload hardware sensitivity: CC workloads up to 1.77× sensitive to GPU while CA workloads are GPU-insensitive (~1.0×); Excel/WinRAR sensitive to CPU frequency and storage."; :95 — "Use CpsMark+ Table 4 sensitivity signatures to assign CPU/GPU/IO resource mixes"; :104; docs/workload/archetype-plan.md:69 — "Creative apps (S6/S7) are time-shared compositions of `desktop-interactive` + `cpu-batch` — consistent with CpsMark+ Table 4's signature (`cpsmark-tbench23:table-4`)."; :83 — "CpsMark+ Table 4's GPU-sensitivity remains a citation about resource mixes, recorded in notes."
- Wording differences: archetype-plan:69 uses Table 4 as consistency support for interactive+CPU-batch composition of S6/S7; sources.yaml mentions only GPU sensitivity.
- Grounds: archetype-plan spanning check (S6/S7 composition); OQ-1 (no GPU axis).
- Neutral topic: the content of CpsMark+ Table 4 — which hardware factors are varied, the sensitivity values per workload/module, and which workloads are sensitive to CPU frequency or storage.

### C-cpsmark-7 — scope limits: Windows 10 only; no gaming scenario; no process-level burst timing
- Locations: dataset/sources.yaml:95-97 — "Scope limits: Windows 10 applications — the Linux name mapping is ours; no gaming scenario; no process-level burst timing."; docs/workload/source-vetting.md:25 — "Windows 10 only."; :34 — "No gaming scenario (office-only) … No process-level burst/period numbers. Windows 10 applications"; :105 — "CpsMark+ has no gaming scenario and is Windows-10-only"
- Grounds: scope statement; Linux name mapping attributed to us.
- Neutral topic: the operating system CpsMark+ targets; whether it contains any gaming scenario; whether it reports per-process timing.

### C-cpsmark-8 — open-source artifact locations
- Locations: docs/references.md:32 — "Open-source artifact: github.com/wanghong3116/CpsMarkPLUS (pin commit) + NMDC resource package."; docs/workload/source-vetting.md:10 — "**open-source** (MCP at github.com/wanghong3116/CpsMarkPLUS; resource packages at the National Metrology Data Center of China)"; :25 — "resource + third-party application packages at the National Metrology Data Center of China (jc.nmdc.ac.cn)"; :90
- Neutral topic: whether CpsMark+ is released as open source, where its control program and resource packages are hosted.

### C-cpsmark-9 — CpsMark+ criticizes SYSmark/PCMark methodology; vendor-neutrality design criterion
- Locations: docs/workload/source-vetting.md:18 — "CpsMark+ itself criticizes SYSmark/PCMark methodology (subjective grouping, no cross-task cooperation, opaque scoring)"; :25 — "The paper positions open-source vendor-neutrality as a design criterion, explicitly against the opacity of SYSmark/PCMark"; :93 — "since CpsMark+ criticizes SYSmark/PCMark methodology directly"
- Grounds: scoping of the convergence sentence (prose).
- Neutral topic: what CpsMark+ says about SYSmark and PCMark methodology and about openness/vendor neutrality.

### C-cpsmark-10 — compares against SYSmark 2018 and PCMark 10; methodological precedent
- Locations: docs/workload/grounding-sources.md:17 — "CpsMark+ (2023, ScienceDirect) | Academic scenario-oriented office desktop benchmark; compares against SYSmark 2018 and PCMark 10 as state of the art | The *methodological* precedent"
- Neutral topic: which prior benchmarks (and versions) CpsMark+ compares itself against.

### C-cpsmark-11 — deployed in a real procurement with one-year user validation
- Locations: docs/workload/source-vetting.md:93 — "(peer-reviewed, open-source, deployed in a real procurement with one-year user validation)"
- Neutral topic: whether CpsMark+ reports a real procurement deployment and any user validation period.

### C-cpsmark-12 — CC grounds the creation arc (photo → video → transcode handoff)
- Locations: docs/workload/building-plan.md:100 — "**creation arc:** gimp → kdenlive → HandBrakeCLI batch handoff (grounded in CpsMark+ CC and SYSmark 30 ACC's photo↔video multitasking workload)."; dataset/timelines/coreset/c3-creation.timeline.yaml:1-2 — "gimp -> kdenlive -> HandBrakeCLI batch handoff (CpsMark+ CC; SYSmark 30 ACC photo<->video multitasking)."
- Grounds: c3-creation segment order (photo 0–120 s, video-edit 120–240 s, transcode 240–420 s).
- Neutral topic: what the CC module contains and whether its workloads are sequenced (and in what order).

### C-cpsmark-13 — bibliographic identity and peer review
- Locations: docs/references.md:31; docs/workload/source-vetting.md:25-26 — "Peer-reviewed in *BenchCouncil Transactions on Benchmarks, Standards and Evaluations* (Tbench), DOI 10.1016/j.tbench.2023.100084."
- Neutral topic: authors, title, journal, article number, DOI.

---

## `pcmark10`

Status (docs/references.md:196): to-pin (submission-time, per standing task). Type: deployed-system. No locator pattern. Edition/URL not pinned (references.md:194).

### C-pcmark-1 — scenario groups and their test lists
- Locations: dataset/sources.yaml:102-106 — "Establishes existence of scenario groups and their application lists: Essentials (web browsing, video conferencing, app start-up), Productivity (spreadsheets, writing), Digital Content Creation (photo/ video editing, rendering), Gaming. Activity composition only; no per-process timing."; docs/references.md:195 — "scenario groups (Essentials/Productivity/DCC/Gaming) and their application lists. Taxonomy existence only."; docs/workload/source-vetting.md:37 — "Scenario groups: Essentials (Web Browsing, Video Conferencing, App Start-up), Productivity (Spreadsheets, Writing), Digital Content Creation (Photo Editing [ImageMagick], Video Editing, Rendering & Visualization), Gaming (2× GPU, Physics CPU, Combined)."; docs/workload/grounding-sources.md:14 — "Essentials (web browsing, video conferencing, app start-up), Productivity (spreadsheets, writing), Digital Content Creation (photo/video editing, rendering); technical whitepaper documents each scenario's real applications"; docs/workload/scenario-catalog.md:12 — S1 "PCMark 10 Productivity (Writing, Spreadsheets)"; :13 — S2 "PCMark 10 Essentials (Web Browsing)"; :14 — S3 "PCMark 10 Essentials (Video Conferencing)"; :17 — S6 "PCMark 10 DCC (Photo Editing, ImageMagick)"; :18 — S7 "PCMark 10 DCC (Video Editing, Rendering & Visualization)"; :20 — S9 "PCMark 10 Gaming"; :33 — "PCMark 10's three groups map to S1–S3, S6–S7, S13"
- Wording differences: grounding-sources omits Gaming; scenario-catalog:33 says "three groups" while four are listed elsewhere; grounding-sources says a "technical whitepaper" documents "real applications".
- Grounds: S1, S2, S3, S6, S7, S9 source column; mode categories (Role A).
- Neutral topic: in the PCMark 10 technical guide, the benchmark's scenario groups and the individual tests in each group, including any gaming group and its tests.

### C-pcmark-2 — Photo Editing uses ImageMagick
- Locations: docs/workload/source-vetting.md:37 — "Photo Editing [ImageMagick]"; docs/workload/scenario-catalog.md:17 — "(Photo Editing, ImageMagick)"
- Neutral topic: which software the PCMark 10 photo editing test uses.

### C-pcmark-3 — Applications benchmark uses Microsoft Edge and Office
- Locations: docs/workload/source-vetting.md:37 — "Applications benchmark uses Microsoft Edge and Office."
- Neutral topic: which applications PCMark 10's Applications benchmark uses.

### C-pcmark-4 — Battery Video profile
- Locations: docs/workload/scenario-catalog.md:24 — S13 "PCMark 10 Battery Video profile"; :33 — S13 in the PCMark mapping
- Grounds: S13 source column.
- Neutral topic: whether PCMark 10 has a battery-life video playback profile.

### C-pcmark-5 — activity composition only, no per-process timing
- Locations: dataset/sources.yaml:105-106; docs/workload/source-vetting.md:37 — "documents activity composition, not per-process timing."; :37 "Grounds five of six proposed families" (borderline, our judgement)
- Neutral topic: whether the technical guide documents per-process or per-task timing of its workloads.

## `sysmark30`

Status (docs/references.md:201): verified (2026-09-12), with a retrieval caveat (read from an Internet Archive capture of BAPCo's URL; scenario names corroborated against store.bapco.com). Type: deployed-system.

### C-sysmark30-1 — four scenarios and their descriptions
- Locations: dataset/sources.yaml:111-114 — "Establishes existence of scenario/application lists: Office Applications, General Productivity (incl. archiving/compression, OCR, browsing), Photo Editing, Advanced Content Creation (incl. a multitasking workload switching photo<->video editing)."; docs/references.md:200 — (four scenarios quoted: Office Applications "models office environment like usage including word processing (mail merge, document comparison, and PDF conversion), spreadsheet data manipulation (data modeling, financial forecasting), presentation editing"; General Productivity "models OCR of documents, web browsing, application installation, and archiving and unpacking a mixed file data set"; Photo Editing "models editing digital photos (applying filters and creating HDR photos), cataloging digital photos (organizing catalog, use of facial detection to group people)"; Advanced Content Creation "encodes video with a CPU render and GPU accelerated workload for SUTs configured with a supported accelerated GPU. A multitasking workload switches between photo editing and video editing workloads."); docs/workload/source-vetting.md:40 — "Office Applications (…), General Productivity (Acrobat, Audacity 2.3.2, WinZip 26, Chrome 106; OCR, browsing, app install, archiving), Photo Editing (…), Advanced Content Creation (Photoshop + Premiere CC 22; includes a multitasking workload switching between photo and video editing)"; docs/workload/scenario-catalog.md:12 — S1 "SYSmark 30 Office Applications"; :18 — S7 "SYSmark 30 Advanced Content Creation"; :33 — "SYSmark 30's four scenarios to S1, S2+S16, S6, S7"
- Wording differences: sources.yaml "archiving/compression"; references.md "archiving and unpacking a mixed file data set"; scenario-catalog:27 "file compression/unpacking".
- Grounds: S1, S2, S6, S7, S15, S16 source column; Role A taxonomy.
- Neutral topic: in the SYSmark 30 user guide, the scenario names and the activities each scenario models.

### C-sysmark30-2 — General Productivity: browsing (Chrome 106), archiving (WinZip), used for S2, S15, S16
- Locations: docs/workload/scenario-catalog.md:13 — S2 "SYSmark 30 General Productivity (Chrome 106)"; :26 — S15 "SYSmark 30 General Productivity (archiving analogue)"; :27 — S16 "SYSmark 30 General Productivity (file compression/unpacking, WinZip → 7z)"
- Wording differences: S15 (backup/sync) is supported by "archiving analogue" — an analogy, not a backup scenario.
- Grounds: S2, S15, S16 source column.
- Neutral topic: which applications and activities the General Productivity scenario includes (browser and version, archiving tool and version).

### C-sysmark30-3 — ACC multitasking workload switching photo and video editing
- Locations: dataset/sources.yaml:113-114; docs/references.md:200; docs/workload/source-vetting.md:40; docs/workload/building-plan.md:100 — "SYSmark 30 ACC's photo↔video multitasking workload"; dataset/timelines/coreset/c3-creation.timeline.yaml:2 — "SYSmark 30 ACC photo<->video multitasking"
- Grounds: c3-creation arc (photo → video-edit segments).
- Neutral topic: whether the Advanced Content Creation scenario includes a workload that switches between photo and video editing, and in what order.

### C-sysmark30-4 — named applications with versions per scenario
- Locations: docs/references.md:200 — "Microsoft Excel / Outlook / PowerPoint / Word 2021 Professional Plus VL; Adobe Acrobat Pro DC, Audacity 2.3.2 (listed \"for app install\" — the installation itself is the workload), Corel WinZip 26.0, Google Chrome 106.0.5249.103; Adobe Lightroom Classic 11 and Photoshop CC 23; Photoshop CC 23 and Premiere CC 22."; docs/workload/source-vetting.md:40 — "Office Applications (Word/Excel/PowerPoint/Outlook 2021) … Photo Editing (Lightroom Classic 11, Photoshop CC 23)"; docs/workload/scenario-catalog.md:17 — S6 "SYSmark 30 Photo Editing (Lightroom/Photoshop → darktable/GIMP)"
- Wording differences: "WinZip 26" vs "WinZip 26.0"; "Chrome 106" vs full version.
- Grounds: S6 names (darktable, gimp); names-only schema (scenario-catalog.md:5 "SYSmark app lists").
- Neutral topic: the applications and versions listed per scenario in the SYSmark 30 user guide.

### C-sysmark30-5 — scenario lists documented separately from scoring; 2011 vendor departures concerned scoring
- Locations: dataset/sources.yaml:115-116 — "Scenario lists are documented separately from the contested scoring."; docs/references.md:200 — "Note in paper: the 2011 vendor departures concerned scoring, not scenario lists."; docs/workload/source-vetting.md:40 — "2011 AMD/Nvidia/VIA departure concerned scoring weights, not scenario lists — state this explicitly in the paper."
- Grounds: prose only.
- Neutral topic: whether the user guide separates scenario descriptions from scoring; the 2011 departures of vendors from BAPCo and their stated reasons (needs a separate source).

### C-sysmark30-6 — document version metadata
- Locations: docs/references.md:199 — "*SYSmark 30 User Guide*. bapco.com/wp-content/uploads/2025/04/bapco-sysmark30-user-guide-v1.2.pdf, 40 pp. … Cover reads \"Revision: 1.1\"; the revision history runs through 1.2"; docs/workload/source-vetting.md:40 — "**SYSmark 30 primary** (2022, User Guide v1.1 2024)"
- Wording differences: v1.1 2024 (source-vetting) vs v1.2 file with 1.1 cover (references.md).
- Neutral topic: the user guide's revision number(s), date, page count, and product release year.

## `sysmark25`

Status (docs/references.md:206): to-pin. Type: deployed-system.

### C-sysmark25-1 — adds software development (code compilation) and a Responsiveness scenario
- Locations: dataset/sources.yaml:121-123 — "Adds software development (code compilation) and a Responsiveness scenario to the BAPCo taxonomy — grounds compile as a mainstream desktop scenario."; docs/references.md:205 — "adds software development (code compilation) and Responsiveness."; docs/workload/source-vetting.md:40 — "**SYSmark 25 secondary**: adds software development (code compilation) and a Responsiveness scenario."; :93 — "SYSmark 25 for compile"; docs/workload/grounding-sources.md:15 — "SYSmark 25's inclusion of *software development* grounds the compile Family as a mainstream desktop scenario"; docs/workload/scenario-catalog.md:22 — S11 "SYSmark 25 Productivity (software development / code compilation)"; :33 — "SYSmark 25 adds S11"
- Wording differences: scenario-catalog places software development under a "Productivity" scenario; sources.yaml says "adds … to the BAPCo taxonomy" (relative to SYSmark 30, which is newer).
- Grounds: S11 source column; compile mode as a mainstream scenario.
- Neutral topic: in SYSmark 25 documentation, the scenario list, whether a software-development/code-compilation workload exists and under which scenario, and whether a Responsiveness scenario exists.

### C-sysmark25-2 — combined SYSmark 30/25 taxonomy as described in grounding-sources (borderline attribution)
- Locations: docs/workload/grounding-sources.md:15 — "SYSmark 30 / 25 (BAPCo) | Scenario benchmark built from real commercial applications: Productivity (word processing, spreadsheets, software development, email), Creativity (photo/video, ML face recognition), Responsiveness"
- Wording differences: this three-scenario taxonomy differs from SYSmark 30's four scenarios (C-sysmark30-1); it does not say which product each scenario belongs to.
- Grounds: Role A (prose).
- Neutral topic: which SYSmark version defines scenarios named Productivity, Creativity and Responsiveness, and the activities listed under each (email, face recognition).

## `procyon`

Status (docs/references.md:211): verified (2026-09-12; suite overview page read in full). Type: deployed-system.

### C-procyon-1 — a local-AI-inference desktop scenario exists in a shipped benchmark
- Locations: dataset/sources.yaml:128-130 — "Establishes existence of a local-AI-inference desktop scenario (S12 precedent). Public docs are light on internals; scenario-existence citation only."; docs/references.md:210 — "Local-AI desktop scenarios exist in a shipped commercial benchmark (S12 precedent): of the nine benchmarks, three are AI workloads — **AI Text Generation** … **AI Image Generation** … **AI Computer Vision** …"; docs/workload/source-vetting.md:43 — "Adds a local AI-inference desktop scenario beyond PCMark 10. Public docs are light on internals; scenario-existence citation only."; docs/workload/grounding-sources.md:16 — "Newer UL suite: office productivity, photo/video editing, AI inference scenarios"; docs/workload/scenario-catalog.md:23 — S12 "UL Procyon (local AI inference scenario)"; :33 — "Procyon adds S12"
- Grounds: S12 source column (python3 training / ollama); ml-train mode.
- Neutral topic: the list of benchmarks in the UL Procyon suite and whether any run AI inference locally, with their names and descriptions.

### C-procyon-2 — the other six benchmarks and their applications
- Locations: docs/references.md:210 — "The other six: Essentials (…), Office Productivity (Word, Excel, PowerPoint, Outlook), Photo Editing (Adobe Lightroom, Adobe Photoshop), Video Editing (Adobe Premiere Pro), Battery Life, One-Hour Battery Consumption."
- Neutral topic: the non-AI benchmarks in the Procyon suite and the applications each uses.

### C-procyon-3 — public docs light on internals
- Locations: dataset/sources.yaml:129; docs/workload/source-vetting.md:43
- Neutral topic: how much workload detail Procyon's public documentation provides.

---

## `gamemode-docs`

Status (docs/references.md:217): verified (2026-09-12; `previous-versions/windows/desktop/gamemode/game-mode-portal` plus three `windows/win32/api/expandedresources/` function pages read). One open question left unresolved (update/notification deferral). Type: deployed-system. Cite line reads "[Exact URLs to pin.]" (references.md:214).

### C-gamemode-1 — a foreground-game resource-priority category ships in a major OS
- Locations: dataset/sources.yaml:135-137 — "Establishes that a foreground-game resource-priority category ships in a major OS: exclusive/priority CPU access for the focused foreground game"; docs/references.md:215 — "shipped foreground-game resource-priority category. Existence only."; docs/workload/source-vetting.md:46 — "Documented: foreground game granted exclusive/priority resource access"; docs/workload/grounding-sources.md:18 — "Windows Game Mode docs / ananicy catalog | Shipping systems' own categories (gaming; per-app priority classes) | That the *gaming* mode and the wanted/unwanted-background distinction are categories deployed systems already act on"; docs/workload/scenario-catalog.md:20 — S9 "Windows Game Mode (foreground-game category)"; :33 — "Game Mode/LAVD/ananicy add S9–S10, S14–S17"
- Wording differences: grounding-sources groups Game Mode with the wanted/unwanted distinction; sources.yaml limits it to the category's existence.
- Grounds: S9 source column; gaming mode as a deployed category.
- Neutral topic: in Microsoft's Game Mode documentation, what Game Mode does for games and which resources it affects.

### C-gamemode-2 — exclusive CPU sets granted to an app in the foreground with focus; GPU prioritization
- Locations: dataset/sources.yaml:137-138 — "granted as exclusive CPU sets to an app that is in the foreground and has focus"; docs/references.md:216 — "Resource model: exclusive CPU sets plus \"increased GPU prioritization\". … Grant condition: \"The app must be in the foreground and have focus before exclusive resources are granted\" (repeated on all three function pages). Revocation differs by resource: exclusive CPUs go \"when the game loses focus\", whereas \"memory resources, once granted, will never be revoked\"."; docs/workload/source-vetting.md:46 — "must be foreground and focused; CPU exclusivity + GPU prioritization"
- Grounds: prose only.
- Neutral topic: the resources Game Mode grants, the condition for granting them, and when each resource is revoked.

### C-gamemode-3 — user opt-out in Settings; API surface; deprecation
- Locations: dataset/sources.yaml:138-139 — "with a user opt-out in Settings; documented APIs (expandedresources.h)"; docs/references.md:216 — "User opt-out: `GetExpandedResourceExclusiveCpuCount` \"returns 0 if no exclusive CPU sets are available, or if the customer opted out of Game Mode via the Settings in Windows 10\". … \"The Game Mode APIs are deprecated in Windows 10, version 1809 and later.\""; docs/workload/source-vetting.md:46 — "`<expandedresources.h>` APIs (GetExpandedResourceExclusiveCpuCount, SetProcessDefaultCpuSets, ReleaseExclusiveCpuSets, HasExpandedResources)"
- Wording differences: source-vetting lists `SetProcessDefaultCpuSets` among expandedresources.h APIs; references.md names three function pages without listing them.
- Neutral topic: which functions the expandedresources header documents, whether users can opt out and how that is reported, and any deprecation notice.

### C-gamemode-4 — "whitelist design point" (conflicting wording across locations)
- Locations: dataset/sources.yaml:139-140 — "Existence of the category and of the whitelist design point only."; docs/references.md:215 — "**The role has narrowed: this entry can no longer be cited as the whitelist design point we reconstruct.** … Microsoft's documentation does not state how a game is recognised. What it states is the outcome — \"Game Mode works by default for most Windows games, requiring no action or opt-in by the customer, and no work by the game developer\" — beside an optional developer declaration, the `expandedResources` capability, which is \"granted on a per-title basis; contact your account manager for more information\". No list, no executable-name matching, no detection mechanism on any of the four pages."
- Wording differences: sources.yaml still lists the whitelist design point as established; references.md says it cannot be cited for it.
- Grounds: prose only (framing of name-table approach).
- Neutral topic: whether Microsoft documents how Game Mode recognizes a game (list, name matching, declaration, other), what it says about default coverage of games, and how the `expandedResources` capability is granted.

### C-gamemode-5 — background preemption reduced; updates/notifications deferred (conflicting status)
- Locations: docs/workload/source-vetting.md:46 — "background preemption reduced; updates/notifications deferred."; dataset/sources.yaml:140-144 — "NOT established here … how a game is detected, and whether background activity is suppressed, updates deferred or notifications held. The conceptual portal page carrying those claims has not been read; do not derive them from this source."; docs/references.md:216 — "Background work is excluded from the reserved cores rather than throttled — opting out of exclusivity means \"having to share them with other processes\", at \"a higher latency due to other processes and system activities being scheduled on the same cores as the game\"."; :217 — "whether Microsoft documents that Game Mode defers Windows Update driver installs or restart/notification prompts during play. No page reachable at this check says so"
- Wording differences: source-vetting states deferral as documented; sources.yaml says not established and that the portal page "has not been read"; references.md says the portal page has been read and deferral is not found.
- Grounds: prose only.
- Neutral topic: what Microsoft documentation says about how background processes are treated during Game Mode, and whether it mentions deferring updates, driver installs, restarts or notifications.

## `ananicy-rules`

Status (docs/references.md:191): verified (2026-09-12; catalogue cloned and counted at commit `03ef03fbf7e834385377432ccecaedd32e3414bb`). Type: deployed-system. No locator pattern. Used as `category_source` for `background-crawler` (dataset/archetypes.yaml:295).

### C-ananicy-rules-1 — the catalogue defines behaviour-class `type`s (Game, Heavy_CPU, BG_CPUIO, Doc-View, LowLatency_RT, Player-Audio, Player-Video, …)
- Locations: dataset/sources.yaml:149-151 — "Community-maintained process-name -> behavior-class taxonomy: rule `type` classes (Game, Heavy_CPU, BG_CPUIO, Doc-View, LowLatency_RT, Player-Audio, Player-Video, ...) with nice / ioclass / sched values"; docs/references.md:186 — "a community-maintained process-name → behavior-class taxonomy (`Heavy_CPU`, `Game`, `BG_CPUIO`, …)"; docs/workload/archetype-plan.md:31 — "**`ananicy-rules`' `type` field — literally a community-maintained archetype taxonomy** (`Heavy_CPU`, `Game`, `Player`, `BG_CPUIO`, …)"; docs/workload/coreset-guide.md:64 — "ananicy 카탈로그"
- Wording differences: archetype-plan lists `Player` (references.md lists `Player-Audio`, `Player-Video`); archetype-plan calls the type field "literally a … archetype taxonomy".
- Grounds: Tier-1 harvesting of the archetype inventory; `background-crawler.category_source`.
- Neutral topic: in the CachyOS ananicy-rules repository, the defined rule `type` names and what each type sets.

### C-ananicy-rules-2 — per-type nice/ioclass/sched values
- Locations: dataset/sources.yaml:151-153 — "background CPU/IO runs ioclass idle at nice 16, Player-Audio and Player-Video at nice -4, LowLatency_RT at nice -12, Game at nice -5"; docs/references.md:187 — "`00-types.types` sets `Game` nice −5 (ioclass best-effort, sched normal); `Player-Audio`, `Player-Video`, `Image-View` and `Doc-View` nice −4; `LowLatency_RT` nice −12 (ioclass best-effort); `BG_CPUIO` nice 16 (ioclass idle, sched idle); `BG_CPU` nice 14; `Launcher` nice 16; `Heavy_CPU` nice 9; `Chat` nice −3; `Service` nice 10; `IN_DIFF` nice 0; and `OOM_KILL` / `OOM_NO_KILL` set only `oom_score_adj` to 1000 / −1000."; docs/workload/scenario-catalog.md:24 — S13 "ananicy audio class (nice −11)"; docs/workload/source-vetting.md:47 — "audio nice −11"
- Wording differences: audio class nice −11 (scenario-catalog, source-vetting) vs Player-Audio nice −4 (sources.yaml, references.md).
- Grounds: S13 source column; prose on priority classes.
- Neutral topic: in `00-types.types` at a pinned commit, the nice, ioclass, sched and oom_score_adj values set for each type, including the audio-player type.

### C-ananicy-rules-3 — Proton/wine vs native game classes
- Locations: dataset/sources.yaml:154 — "Proton/wine vs native game classes."; docs/workload/source-vetting.md:47 — "games via Proton/wine vs linux-native"; docs/workload/scenario-catalog.md:20 — S9 "ananicy/CachyOS (Proton vs linux-native game classes)"; docs/references.md:188 — path "`00-default/Games/linux-native/linux-native_d.rules:315`"
- Wording differences: "classes" (sources.yaml, scenario-catalog) vs grouping of games (source-vetting); references.md shows the distinction as a directory, all games carrying type `Game`.
- Grounds: S9 source column (Proton `<game>.exe` naming).
- Neutral topic: how the catalogue separates Proton/Wine games from Linux-native games (directories, types, or both).

### C-ananicy-rules-4 — wanted/unwanted-background distinction as deployed practice (borderline)
- Locations: dataset/sources.yaml:154-156 — "Establishes the classes' existence, deployed name->class mappings, and the wanted/unwanted-background distinction as deployed practice (category_source for harvested archetypes)."; docs/references.md:186 — "grounds the wanted/unwanted-background distinction as deployed practice"; docs/workload/source-vetting.md:47 — "Grounds the wanted/unwanted-background distinction and provides real process-name → priority-class mappings."; docs/workload/grounding-sources.md:18
- Grounds: the `background_wanted` attribute as a deployed distinction (prose).
- Neutral topic: whether the catalogue or its documentation distinguishes background work the user wants from background work to be deprioritized, and how (types, comments, documentation).

### C-ananicy-rules-5 — BG_CPUIO / indexer class at ioclass idle; carries no rates
- Locations: dataset/archetypes.yaml:319-320 — "ananicy-rules establishes the class (BG_CPUIO/indexer, ioclass idle — deployed practice) but carries no rates."; dataset/archetypes.yaml:331-332 — "the ioclass-idle character is expressed through low scheduling priority at binding, not encoded here."; docs/workload/archetype-plan.md:58 — "`background-crawler` — low-priority filesystem walk, ioclass-idle. category_source: `ananicy-rules` (BG_CPUIO/indexer class)"; docs/workload/building-plan.md:64 — "ioclass-idle IO walk (`ananicy-rules`)"; docs/workload/source-vetting.md:47 — "indexers ioclass idle"; docs/workload/scenario-catalog.md:25 — S14 "ananicy/CachyOS catalog (ioclass idle indexer class)"
- Wording differences: "BG_CPUIO/indexer" — whether indexers are a named type or entries under BG_CPUIO is not stated.
- Grounds: `background-crawler.category_source`; S14 row.
- Neutral topic: which type(s) the catalogue assigns to file indexers (e.g. tracker, baloo, updatedb) and the ioclass/nice/sched of that type; whether the catalogue carries any timing or rate values.

### C-ananicy-rules-6 — Heavy_CPU cross-confirms cpu-batch; compilers batch/idle
- Locations: dataset/archetypes.yaml:161 — "interbench Burn (cross-confirmed by ananicy-rules Heavy_CPU)"; docs/workload/archetype-plan.md:52 — "(Burn; cross-confirmed by ananicy-rules `Heavy_CPU`)"; docs/workload/source-vetting.md:47 — "compilers batch/idle"
- Grounds: cpu-batch class corroboration.
- Neutral topic: what the catalogue's Heavy_CPU type sets and which processes are assigned to it; which type(s) compiler processes receive and their sched policy.

### C-ananicy-rules-7 — class names cited in scenario-catalog rows (comms, download, backup, AV/scan)
- Locations: docs/workload/scenario-catalog.md:16 — S5 "ananicy/CachyOS catalog (comms class)"; :21 — S10 "ananicy catalog (download class)"; :26 — S15 "ananicy catalog (backup class, ioclass idle)"; :28 — S17 "ananicy catalog (AV/scan class)"
- Wording differences: references.md:187 lists types `Chat`, `BG_CPUIO`, `Service`, etc.; no type named comms, download, backup or AV/scan appears in references.md's list (borderline: "class" may mean a directory or grouping).
- Grounds: S5, S10, S15, S17 source column.
- Neutral topic: how the catalogue classifies voice/chat clients, download clients (e.g. transmission), backup/sync tools (rsync, borg, rclone) and antivirus scanners (clamscan, freshclam) — type and ioclass for each.

### C-ananicy-rules-8 — catalogue attests real process names (borderline)
- Locations: docs/workload/scenario-catalog.md:5 — "The grounding sources attest to process *names* (CpsMark+ Table 2, SYSmark app lists, the ananicy catalog)"; docs/workload/source-vetting.md:47 — "hundreds of process names"; dataset/sources.yaml:155 — "deployed name->class mappings"
- Grounds: names-only schema decision.
- Neutral topic: whether catalogue entries match on executable/process names and roughly how many distinct names it lists.

### C-ananicy-rules-9 — counts at a pinned commit
- Locations: docs/references.md:187 — "**Measured at commit `03ef03fbf7e834385377432ccecaedd32e3414bb` (authored 2026-09-08, counted 2026-09-12):** 361 `.rules` files; 15 813 rule entries; 13 528 of them carry `\"type\": \"Game\"` (85.5 per cent), then `BG_CPUIO` 1 615, `Service` 194, `Doc-View` 160, `LowLatency_RT` 109, `Chat` 51, `Heavy_CPU` 33, `Image-View` 32, `Player-Audio` 28, `Player-Video` 24, `Launcher` 24, `IN_DIFF` 10, `OOM_NO_KILL` 2, `TODO` 1, and 2 entries with no `type` key."; :189 (counting method); dataset/sources.yaml:157-158 — "Values and entry counts measured at the commit named in docs/references.md (2026-09-12)"
- Grounds: enumeration-cost argument (prose, non-dataset).
- Neutral topic: at the named commit, the number of rules files, rule entries, and entries per type, counted per file.

### C-ananicy-rules-10 — type definitions count and anomalies
- Locations: docs/references.md:188 — "`00-types.types` defines **fifteen** types; **thirteen** are used by at least one entry (`BG_CPU` and `OOM_KILL` have none). A fourteenth string, `TODO`, appears on one entry without being defined anywhere, and one entry is not valid JSON (a stray `+` at end of line, `00-default/Games/linux-native/linux-native_d.rules:315`)."
- Neutral topic: at the named commit, how many types the types file defines, which are unused, any undefined type strings, and any malformed rule lines.

### C-ananicy-rules-11 — maintainers, contribution convention, multiple entries per game
- Locations: docs/references.md:186 — "it is maintained \"by the CachyOS team and the community\" and contributors are asked to paste the game's store URL beside each entry."; :187 — "One game can hold several entries under different types — the catalogue's own example gives one title an orchestrator executable as `BG_CPUIO` and its shipping executable as `Game`."
- Neutral topic: the catalogue README's maintainer statement, contribution instructions for game entries, and any example assigning different types to executables of one game.

### C-ananicy-rules-12 — capitalized type vocabulary belongs to this catalogue, not upstream Ananicy
- Locations: dataset/sources.yaml:158-160 — "the capitalized type vocabulary belongs to this catalogue, not to upstream Ananicy, whose current types file marks those types deprecated."; docs/references.md:181, :186
- Neutral topic: see C-ananicy-2 (upstream types file) and the CachyOS types file.

## `ananicy` (upstream Ananicy / ananicy-cpp; docs/references.md only)

Status (docs/references.md:182): verified-in-vetting (2026-08-25); lineage split and field list re-confirmed 2026-09-12.

### C-ananicy-1 — rule schema fields and an example rule
- Locations: docs/workload/source-vetting.md:47 — "JSON rules in /etc/ananicy.d/*.rules: name, type, nice [-20..19], latency_nice, sched {fifo,rr,normal,batch,idle}, ioclass, ionice, oom_score_adj, cgroup. Example: {\"name\":\"gcc\",\"type\":\"Heavy_CPU\",\"nice\":19,\"ioclass\":\"best-effort\",\"ionice\":7,\"cgroup\":\"cpu90\"}."; docs/references.md:180 — "`name` is the only required field (\"used for match processes by exec bin name\"), with `cmdlines`, `type`, `nice`, `latency_nice`, `sched`, `rtprio`, `ioclass`, `ionice`, `oom_score_adj`, `cpuset` and `cgroup` optional (field list from the ananicy-cpp README)."
- Wording differences: references.md adds `cmdlines`, `rtprio`, `cpuset`.
- Neutral topic: the rule fields documented by ananicy/ananicy-cpp, which are required, value ranges, the rules directory, and any example rule for gcc.

### C-ananicy-2 — upstream types file: lowercase types and deprecated capitalized types
- Locations: docs/references.md:181 — "Upstream Ananicy's current `ananicy.d/00-types.types` uses lowercase types (`game`, `compiler`, `file-sync`, `service`) and carries the capitalized ones (`Heavy_CPU`, `BG_CPUIO`, `LowLatency_RT`) commented out beneath a heading reading \"Depricated types\"."; dataset/sources.yaml:159-160
- Neutral topic: the type names in upstream Ananicy's types file at HEAD and how older type names are marked.

### C-ananicy-3 — self-description, licenses, versions, repositories
- Locations: docs/references.md:179-180 — "Nefelim4ag. Ananicy. github.com/Nefelim4ag/Ananicy (GPL); ananicy-cpp: gitlab.com/ananicy-cpp/ananicy-cpp (GPL-3.0)." / "\"a shell daemon created to manage processes' IO and CPU priorities, with community-driven set of rules for popular applications … mainly for desktop usage\""; docs/workload/source-vetting.md:47 — "ananicy-cpp at gitlab.com/ananicy-cpp/ananicy-cpp (GPL-3.0, ~1.2.0)"; :87 — "ananicy: distro-wiki documented; pair with Game Mode as the \"deployed systems already act on this\" citation."; :90
- Neutral topic: Ananicy's README self-description, repository locations, licenses and ananicy-cpp version; whether distribution wikis document it.

---

## `steam-downloads`

Status (docs/references.md:222): verified (2026-08-26). Type: deployed-system.

### C-steam-1 — the "Allow Downloads During Gameplay" setting and its location
- Locations: dataset/sources.yaml:165-166 — "Establishes the \"Allow Downloads During Gameplay\" checkbox (Steam -> Settings -> Downloads)"; docs/references.md:221 — "documents the \"Allow Downloads During Gameplay\" checkbox (Steam → Settings → Downloads)"; docs/workload/scenario-catalog.md:21 — S10 "Steam client \"Allow downloads during gameplay\" setting (Valve — documents both the scenario and the wanted/unwanted decision as a real user-facing toggle)"; docs/workload/coreset-guide.md:629 — "Valve의 \"게임 중 다운로드 허용\" 설정이 이 상황의 근거."
- Wording differences: title case (sources.yaml, references.md) vs sentence case (scenario-catalog); references.md:221 notes the 2021 article title-cases and the current client sentence-cases.
- Grounds: S10 source column; c2-p2a segment 2 (`background: download`, scenario [S9, S10], c2-p2a.timeline.yaml:10-11).
- Neutral topic: in Steam Support articles, the name and menu location of the setting controlling downloads while a game runs.

### C-steam-2 — downloads pause during gameplay by default
- Locations: dataset/sources.yaml:166-167 — "that downloads pause during gameplay by default"; docs/references.md:220 — article title "Downloads automatically pause when launching a game."; :221 — "default pause-during-gameplay"
- Neutral topic: what Steam does with downloads when a game launches, by default.

### C-steam-3 — per-game override
- Locations: dataset/sources.yaml:167 — "and the per-game override"; docs/references.md:221 — "and the per-game counterpart"
- Wording differences: "override" vs "counterpart".
- Neutral topic: whether Steam offers a per-game setting for downloads during gameplay, and what it does.

### C-steam-4 — the setting is the wanted/unwanted background toggle as a real user-facing setting (borderline characterization)
- Locations: dataset/sources.yaml:167-168 — "the wanted/unwanted background toggle as a real user-facing setting (S10). Existence only."; docs/references.md:221 — "the wanted/unwanted toggle as a real user-facing setting"; docs/workload/scenario-catalog.md:21 — "documents both the scenario and the wanted/unwanted decision"
- Grounds: S10 as a "wanted" background scenario.
- Neutral topic: see C-steam-1 to C-steam-3 (the setting's existence and user control).

### C-steam-5 — secondary article
- Locations: docs/references.md:220 — "Secondary: \"Managing Steam Downloads & Updates\", …/71AB-698D-57EB-178C (updated 2024-09-24)."
- Neutral topic: the title and last-updated date of the named Steam Support article.

### C-steam-6 — Steam downloads run as `steam` download worker processes (borderline; no source cited)
- Locations: docs/workload/scenario-catalog.md:21 — S10 "steam (download workers)"; dataset/timelines/coreset/c2-p2a.timeline.yaml:1 — "{game + steam download workers}"; :20-21 — `{id: download, name: steam, archetype: network-bulk, …}`; docs/workload/building-plan.md:92 — "{game + steam download workers}"
- Grounds: task name `steam` for the download task in c2-p2a.
- Neutral topic: under what process name(s) the Steam client performs downloads on Linux.

## `dkms-man`

Status (docs/references.md:227): verified (2026-09-10). Type: deployed-system. dkms(8), dkms 3.0.11, Ubuntu noble (references.md:225).

### C-dkms-man-1 — DKMS framework exists: modules dynamically built for each kernel
- Locations: dataset/sources.yaml:173 — "Establishes the DKMS framework"; docs/references.md:226 — "existence of the DKMS framework (\"kernel modules to be dynamically built for each kernel on your system\")"
- Neutral topic: the dkms(8) man page's description of what DKMS is.

### C-dkms-man-2 — autoinstall action / autoinstaller service rebuild modules for a new kernel without user action
- Locations and verbatim text:
  - dataset/sources.yaml:173-175 — "and its autoinstall action / autoinstaller service: kernel modules rebuilt and installed for a newly booted kernel without user action"
  - docs/references.md:226 — "its `autoinstall` action and `dkms_autoinstaller` service, which build and install module revisions for a newly booted kernel without user action"
  - dataset/timelines/coreset/c7.variant.yaml:15-17 — "compile: make -> dkms, the kernel-module rebuild the distro runs on a kernel change (dkms-man, dkms-debian;"
  - docs/workload/building-plan.md:121 — "`compile` renames `make` to `dkms`, the module rebuild the distro runs on a kernel change"
  - docs/workload/scenario-catalog.md:22 — "dkms (unwanted counterpart: the module rebuild the distro runs on a kernel change, C7) | … dkms: `dkms-man`, `dkms-debian`"
  - docs/workload/coreset-guide.md:916 — "`compile`은 `make`→`dkms`(kernel 업데이트 때 배포판이 알아서 돌리는 module rebuild)"; :930 — "`make` → `dkms` rename (kernel 업데이트 뒤 module rebuild, meas-ci:names:2로 검증)"
  - daemon/driver-table/prior.yaml:281 — "A build nobody asked for (c7-compile's dkms module rebuild after a kernel update)"
  - docs/daemon/prior-table-pair-review.md:55 — "half for a build the user waits on, the floor for one the distro started"
  - dataset/tools/meas/verify_names.py:50-52 — "compile/false candidate — the kernel-module rebuild framework's orchestrator, run by the distro on kernel change, not by the user (dkms(8) autoinstall)."
- Wording differences: "for a newly booted kernel" (sources.yaml, references.md) vs "on a kernel change" (c7.variant, building-plan, scenario-catalog, verify_names) vs "kernel 업데이트 때/뒤" / "after a kernel update" (coreset-guide, prior.yaml); "run by the distro" vs "without user action"; prior.yaml says "nobody asked for".
- Grounds: c7-compile rename `make` → `dkms` (c7.variant.yaml:127-133) with `background_wanted: false, initiated: scheduled`; S11 row; prior table `compile/false` row sentence.
- Neutral topic: in dkms(8), what the autoinstall action and the autoinstaller service do, when they run (boot, kernel install, other), and whether user action is required.

### C-dkms-man-3 — `dkms` is the orchestrator's process name; dkms is a shell script
- Locations: dataset/sources.yaml:175 — "under the process name `dkms`"; docs/references.md:226 — "`dkms` as the orchestrator's process name"; dataset/tools/meas/verify_names.py:52 — "A shell script: comm is the script name." (borderline: no source id; meas-ci also observed it)
- Grounds: the name `dkms` in c7-compile; tier-3 name table (dataset/tools/wlc/grid.py:46-47).
- Neutral topic: the command/executable name DKMS runs under and how it is implemented (script or binary).

## `dkms-debian`

Status (docs/references.md:232): verified (2026-09-10). Type: deployed-system. Package `dkms` 3.0.10-8+deb12u1 (bookworm).

### C-dkms-debian-1 — package description: rebuilding modules as kernels are upgraded
- Locations: dataset/sources.yaml:181-183 — "Establishes that dkms is a packaged distribution component whose stated purpose includes rebuilding modules as kernels are upgraded (S11 unwanted counterpart, C7). Existence only."; docs/references.md:231 — "the package description (\"very easy to rebuild modules as you upgrade kernels\")"; dataset/timelines/coreset/c7.variant.yaml:16-17 (as C-dkms-man-2)
- Neutral topic: the Debian bookworm `dkms` package description text.

### C-dkms-debian-2 — packaged in the distributions the names workflow covers
- Locations: docs/references.md:231 — "and the fact that the framework is packaged in the distributions the names workflow covers"; docs/references.md:230 — "Debian package `dkms` 3.0.10-8+deb12u1 (bookworm)"
- Wording differences: the cited page is Debian's; the names workflow covers Ubuntu, Fedora and Arch (dataset/tools/meas/verify_names.py:53).
- Neutral topic: the version of `dkms` packaged in Debian bookworm (and whether the cited page speaks to other distributions).

---

## `dhakal-chi18`

Status (docs/references.md:68): verified (2026-08-26). Type: scholarly. No locator pattern (bare tags only).

### C-dhakal-1 — mean inter-key interval and its standard deviation
- Locations: dataset/sources.yaml:216-217 — "Mean inter-key interval 238.66 ms (SD 111.60 across participants' means)"; docs/references.md:67 — "input inter-arrival: mean inter-key interval 238.66 ms (SD 111.60)"; dataset/archetypes.yaml:112-113 — `overall_mean_us: 238660, sampling: per-iteration, source: "dhakal-chi18"`; dataset/archetypes.yaml:134-136 — "pause_mean_us is our arithmetic closing the mixture on dhakal's overall mean: (238,660 - 0.66*158,000)/0.34 ~ 395,235 us."; docs/workload/archetype-plan.md:49 — "intra-burst input gaps `dhakal-chi18` (mean IKI 238.66 ms)"; docs/workload/coreset-guide.md:143 — "전체 평균 238.66 ms. 출처는 dhakal-chi18(타이핑 연구)"; :262 — "`gap = draw(input_gap)          # ~238 ms 평균의 mixture`"
- Wording differences: "SD 111.60 across participants' means" (sources.yaml) vs "SD 111.60" (references.md).
- Grounds: `input_gap.overall_mean_us` = 238660; derived `pause_mean_us` = 395235.
- Neutral topic: the mean inter-key interval the paper reports, the dispersion statistic reported with it and over what unit (keystrokes, participants' means), and the population it is computed over.

### C-dhakal-2 — the inter-key interval distribution is right-skewed
- Locations: dataset/sources.yaml:217 — "right-skewed"
- Grounds: supports a skewed (lognormal-family) input gap (prose).
- Neutral topic: the shape of the inter-key-interval distribution as described or plotted.

### C-dhakal-3 — dataset scale
- Locations: dataset/sources.yaml:217-218 — "136M keystrokes, 169k volunteers"; docs/references.md:66 — title "Observations on Typing from 136 Million Keystrokes"
- Neutral topic: the number of keystrokes and participants in the study, and how participants were recruited.

### C-dhakal-4 — scope: within-burst transcription typing; no mouse; no inter-burst think-pauses
- Locations: dataset/sources.yaml:218-220 — "Scope limit: within-burst transcription typing — no mouse events, no inter-burst think-pauses. Grounds the intra-burst input gap of interactive archetypes only; burst/pause macro-structure is not established here."; docs/references.md:67 — "Scope limit: within-burst transcription typing only — no mouse, no think-pauses; grounds intra-burst gaps, not burst/pause macro-structure."; dataset/archetypes.yaml:130-132 — "Inter-key gaps ground intra-burst input only (dhakal-chi18 scope: within-burst transcription, no mouse, no think-pauses)"; docs/workload/archetype-plan.md:49 — "burst/pause macro-structure is our modeling"; docs/workload/building-plan.md:189 — "input inter-arrival (`dhakal-chi18`, family shape `roeser-rw24`)"
- Wording differences: docs/data-contracts.md:110 — "about a third of gaps are think-pauses instead" and :124 — "with probability 0.34 the gap is a longer think-pause instead" (under `source: dhakal-chi18`), and docs/workload/coreset-guide.md:143 — "34% 확률로 멈춤" — describe the pause component as think-pauses, while the scope statements say the source contains no think-pauses.
- Grounds: scoping of `input_gap` to intra-burst gaps; `validation_stats.referee: none`.
- Neutral topic: the typing task participants performed (transcription or free composition), whether pauses between sentences/phrases are included or excluded from the reported intervals, and whether any pointing-device input was recorded.

### C-dhakal-5 — dataset is public for research use
- Locations: docs/references.md:67 — "Dataset public (Aalto, research use)."
- Neutral topic: availability and licence of the study's dataset.

### C-dhakal-6 — the whole `input_gap` parameter object is tagged dhakal-chi18 (tag-level claim)
- Locations: dataset/archetypes.yaml:108-113 — `input_gap: {dist: lognormal-mixture, fluent_mean_us: 158000, fluent_sigma_log: 0.35, pause_probability: 0.34, pause_mean_us: 395235, pause_sigma_log: 0.6, overall_mean_us: 238660, sampling: per-iteration, source: "dhakal-chi18"}`; docs/data-contracts.md:107-113 — `input_gap: dist: lognormal-mixture / fluent_mean_us: 158000 # ~158 ms between keystrokes while typing fluently / pause_probability: 0.34 # about a third of gaps are think-pauses instead / pause_mean_us: 395235 / … source: dhakal-chi18`; docs/data-contracts.md:124 — "the `source` tags say exactly which paper or measurement each number comes from"
- Wording differences: archetypes.yaml modeling_notes (:132-138) attribute 158 ms and 0.34 to roeser-rw24, the pause mean to "our arithmetic" and the sigmas to "our convention"; the tag names dhakal-chi18 for all; data-contracts says the tags say "exactly which paper … each number comes from".
- Grounds: all `input_gap` numerics (see Part 2(a)).
- Neutral topic: which of the following the paper reports: a mixture model of inter-key intervals, a fluent-component location, a pause probability, a pause-component location, log-scale spreads.

## `roeser-rw24`

Status (docs/references.md:73): verified (2026-08-26). Type: scholarly.

### C-roeser-1 — inter-key-interval distribution family: two-component log-normal mixture
- Locations: dataset/sources.yaml:225-226 — "Establishes the inter-key-interval distribution family: two-component log-normal mixture"; docs/references.md:72 — "inter-key-interval distribution family: two-component log-normal mixture … Cite the mixture shape, not a single parameter set."; dataset/archetypes.yaml:114-116 — `input_gap_family: {dist: family-declaration, family: two-component-lognormal, sampling: per-iteration, source: "roeser-rw24"}`; dataset/archetypes.yaml:132-133 — "the two-component log-normal family is roeser-rw24's"; docs/workload/archetype-plan.md:49 — "with family shape `roeser-rw24`"; docs/workload/building-plan.md:58 — "intra-burst input gaps (`dhakal-chi18`, `roeser-rw24`)"; :189 — "family shape `roeser-rw24`"; docs/workload/coreset-guide.md:143 — "두 성분 lognormal mixture … roeser-rw24(분포 family)"; docs/data-contracts.md:124 — "drawn from a two-component lognormal"
- Grounds: `input_gap.dist: lognormal-mixture`; `input_gap_family` declaration; sampler implementation (dataset/tools/wlc/sampling.py:53-60).
- Neutral topic: the statistical model the paper fits to inter-keystroke intervals — distribution family and number of components — and whether alternatives were compared.

### C-roeser-2 — fluent component around 158 ms
- Locations: dataset/sources.yaml:226 — "(fluent component ~158 ms;"; docs/references.md:72 — "(fluent ~158 ms;"; dataset/archetypes.yaml:109 — `fluent_mean_us: 158000` (tag dhakal-chi18); dataset/archetypes.yaml:133 — "(fluent ~158 ms, pause component p~0.34 — task-dependent, cite the family not a parameter set)"; docs/workload/coreset-guide.md:143 — "유창하게 칠 때 평균 158 ms"; docs/data-contracts.md:109 — "~158 ms between keystrokes while typing fluently"; :124 — "fluent typing averages about 158 ms between keys"
- Wording differences: the source statistic is unspecified ("~158 ms") in sources.yaml/references.md/notes, but the field is named `fluent_mean_us`, coreset-guide says "평균" (mean) and data-contracts says "averages"; the sampler treats the value as the lognormal mean and converts to a median (dataset/tools/wlc/sampling.py:59).
- Grounds: `input_gap.fluent_mean_us` = 158000; derived `pause_mean_us`.
- Neutral topic: the fitted location parameter of the fluent component per task/condition, whether reported on log or raw scale, and whether it is a mean, median or other statistic.

### C-roeser-3 — pause/disfluency component probability around 0.34
- Locations: dataset/sources.yaml:226-227 — "disfluency/pause component at probability ~0.34"; docs/references.md:72 — "pause component p≈0.34"; dataset/archetypes.yaml:110 — `pause_probability: 0.34` (tag dhakal-chi18); :133; docs/workload/coreset-guide.md:143 — "34% 확률로 멈춤(평균 395 ms)"; docs/data-contracts.md:110 — "about a third of gaps are think-pauses instead"; :124 — "with probability 0.34 the gap is a longer think-pause instead"
- Wording differences: "disfluency" vs "pause" vs "think-pause"; coreset-guide attaches "평균 395 ms" (our arithmetic) alongside.
- Grounds: `input_gap.pause_probability` = 0.34.
- Neutral topic: the fitted mixing proportion of the slower component per task/condition, and how the paper interprets that component.

### C-roeser-4 — parameters are task-dependent; no single parameter set is citable
- Locations: dataset/sources.yaml:227-228 — "parameters are task-dependent). Cite the family shape, never a single parameter set."; docs/references.md:72; dataset/archetypes.yaml:133-134, :136-138 — "The sigma_log values are our convention within the cited log-normal family (roeser-rw24 states the family; its parameters are task-dependent, so no single set is citable)."
- Grounds: sigma values declared convention.
- Neutral topic: whether and how the fitted parameters differ across the tasks or conditions in the paper.

### C-roeser-5 — data, code and bibliographic identity
- Locations: docs/references.md:71-72 — "Roeser, J., De Maeyer, S., Leijten, M., & Van Waes, L. (2024). Modelling typing disfluencies as finite mixture process. *Reading and Writing*, 37, 359–384. DOI 10.1007/s11145-021-10203-z." / "Data + code on OSF (osf.io/y3p4d)."
- Neutral topic: authors, title, journal volume/pages/year, DOI; data and code availability.

---

## `zhang-chb15`

Status (docs/references.md:38): verified (2026-08-26; corrects source-vetting's "Yun et al." misattribution). Type: scholarly.

### C-zhang-1 — study scale and data provenance
- Locations: dataset/sources.yaml:190-191 — "31 days, 3,000 subjects, 15M+ log records, 16,406 distinct processes (CNNIC data, unreleased)."; docs/references.md:37 — "31 days / 3,000 subjects / 15M+ records / 16,406 processes, CNNIC data. Dataset unreleased."; docs/workload/source-vetting.md:75 — "31 days, 3,000 subjects, 15M+ records, 16,406 distinct processes — all verified in the paper … dataset not released."; docs/workload/grounding-sources.md:40 — "the 15M-log / ~3k-user computer interaction study"; :74 — "CNNIC study"
- Neutral topic: the study's duration, number of subjects, number of log records and distinct processes, data provider, and data availability.

### C-zhang-2 — power-law task switching concentrated on hub tasks
- Locations: dataset/sources.yaml:191-193 — "Establishes power-law task-switching structure concentrated on hub tasks (\"hub\" is the paper's term; \"star\" is our paraphrase)"; docs/references.md:37 — "power-law switching, hub task structure (\"star\" is our paraphrase — say \"hub\")"; docs/workload/source-vetting.md:75 — "power-law switching concentrated on **hub** tasks (the paper's term; \"star\" is our paraphrase)"; :11 — "the CNNIC 15M-log study gives power-law shapes"; :96 — "heavy-tailed shape from CNNIC"; docs/workload/building-plan.md:137 — "**Switching structure: hub-and-spoke, not uniform-random.** `zhang-chb15`'s core finding is that a few hub tasks dominate switching."
- Wording differences: "power-law" vs "heavy-tailed"; building-plan calls it the paper's "core finding" and "hub-and-spoke".
- Grounds: naturalistic-set generator design (hub scenario + excursions; not built).
- Neutral topic: the distribution the paper reports for task-switching (which quantity follows which law), and what term it uses for highly connected tasks.

### C-zhang-3 — average PC task switch roughly every 3 minutes
- Locations: dataset/sources.yaml:193-194 — "an average PC-task switch roughly every 3 minutes (independently corroborates gonzalez-chi04)"; docs/references.md:37 — "~3-min average PC-task switch (independently corroborates `gonzalez-chi04`)"; docs/workload/source-vetting.md:75 — "average PC-task switch ~every 3 minutes"; docs/workload/building-plan.md:136 — "the ~3-min switch rate independently corroborated by `zhang-chb15`"
- Grounds: naturalistic segment-duration mean (planned).
- Neutral topic: the average interval between task switches the paper reports, and how a task switch is defined.

### C-zhang-4 — shapes and averages only; no sampled distributions
- Locations: dataset/sources.yaml:195 — "Shapes and averages only — no sampled distributions."; docs/workload/source-vetting.md:11 — "no source provides sampled per-user segment-duration distributions"; :77 — "exact distribution parameters must be fitted/assumed and flagged"; :102
- Wording differences: docs/workload/grounding-sources.md:40 — "Empirical distributions of app-switching frequency, session lengths, interruption rates for knowledge workers" (says these studies provide distributions).
- Neutral topic: whether the paper publishes per-user distributions or fitted parameters for switch intervals/session durations, or only aggregate statistics and figures.

### C-zhang-5 — task-switching studies justify app-granularity stability vs PID churn (borderline attribution; group of Role C studies)
- Locations: docs/workload/grounding-sources.md:40 — "Segment duration ranges (minutes, not seconds) and label-change frequency per hour; the claim that app-granularity sets are stable while PID-granularity churns"
- Grounds: prose only (Q7 layer).
- Neutral topic: whether the paper says anything about stability of application sets versus process-level churn.

### C-zhang-6 — authorship correction
- Locations: docs/references.md:36, :38; docs/workload/source-vetting.md:75 — "**Zhang, T., Sun, X., Chai, Y., & Aghajan, H.** (not \"Yun et al.\")"
- Neutral topic: the author list, title, volume and pages of the CHB 2015 paper.

## `gonzalez-chi04`

Status (docs/references.md:43): verified (2026-08-26, against full text). Type: scholarly.

### C-gonzalez-1 — time per working sphere
- Locations: dataset/sources.yaml:200-202 — "~12 min per working sphere (11 min 28 s raw; 12 min 18 s excluding brief disruptions)"; docs/references.md:42 — "~12 min per working sphere"; docs/workload/source-vetting.md:11 — "~12 min per working sphere"; :76 — "~12 min per working sphere (~10 spheres/day)"; :96 — "(3 min / 2 min / 12 min)"; docs/workload/building-plan.md:136 — "~12 min per working sphere (`gonzalez-chi04`; …)"
- Wording differences: two sub-figures appear only in sources.yaml.
- Grounds: naturalistic segment-duration mean (planned).
- Neutral topic: the average continuous time spent in a working sphere before switching, with and without brief disruptions, and how a working sphere is defined.

### C-gonzalez-2 — number of working spheres per day
- Locations: dataset/sources.yaml:202 — "~10 spheres per person-day"; docs/references.md:42 — "(~10 spheres/day)"; docs/workload/source-vetting.md:76
- Neutral topic: the average number of distinct working spheres per person per day.

### C-gonzalez-3 — time per task before switching
- Locations: dataset/sources.yaml:202-203 — "~3 min per task"; docs/references.md:42 — "~3 min per task"; docs/workload/source-vetting.md:11, :76, :96; docs/workload/building-plan.md:136 — "~3 min per task"
- Neutral topic: the average time spent on an event/task before switching.

### C-gonzalez-4 — time per tool/document before switching
- Locations: dataset/sources.yaml:203 — "~2 min 11 s per tool/document before switching"; docs/references.md:42 — ">2 min per tool"; docs/workload/source-vetting.md:11 — "~2 min per tool"; :76 — ">2 min per tool"; :96 — "2 min"
- Wording differences: "~2 min 11 s" vs ">2 min" vs "~2 min"; "tool/document" vs "tool".
- Neutral topic: the average time spent using one electronic tool or paper document before switching.

### C-gonzalez-5 — population and scope
- Locations: dataset/sources.yaml:203-204 — "Averages only, knowledge workers."
- Neutral topic: the study population (roles, organization, sample size) and whether distributions or only averages are reported.

### C-gonzalez-6 — contains interruption statistics used to anchor distractor rates
- Locations: docs/workload/building-plan.md:138 — "**Distractor injection:** label-invariant processes (S5, S16) injected within segments at rates anchored to the interruption statistics in `gonzalez-chi04`/`mark-chi05`."
- Grounds: planned naturalistic distractor rates.
- Neutral topic: what interruption statistics (frequency, source) the paper reports.

### C-gonzalez-7 — the headline figures belong here, not to CHI 2005/2008
- Locations: dataset/sources.yaml:204 — "(The figures our earlier docs attributed to CHI 2005/2008 live here.)"; docs/references.md:42 — "THE home of both headline figures … (Our earlier docs attributed these to CHI 2005/2008 — wrong; repoint here.)"; docs/workload/source-vetting.md:76 — "both headline figures … belong to **González & Mark, CHI 2004**"
- Neutral topic: see C-gonzalez-1, -3, -4, and C-mark08-1.

## `mark-chi05`

Status (docs/references.md:48): verified (2026-08-26). Type: scholarly.

### C-mark05-1 — about 11 minutes per working sphere
- Locations: dataset/sources.yaml:209 — "Companion figure ~11 min per working sphere before switching"; docs/references.md:47 — "~11-min working-sphere companion figure"; docs/workload/source-vetting.md:76 — "CHI 2005 (\"No Task Left Behind?\", `mark-chi05`) carries the companion ~11-min figure"; docs/workload/building-plan.md:136 — "companion ~11 min figure `mark-chi05`"
- Neutral topic: the average time spent in a working sphere before switching reported in the 2005 paper.

### C-mark05-2 — internal vs external interruptions roughly equal (managers' split)
- Locations: dataset/sources.yaml:209-210 — "internal vs external interruptions roughly equal (managers 59.2%/40.8%)."; docs/references.md:47 — "internal vs. external interruption split (managers 59.2%/40.8%)."; docs/workload/source-vetting.md:76 — "the internal/external interruption split"; docs/workload/building-plan.md:138 (as C-gonzalez-6)
- Wording differences: "roughly equal" (sources.yaml) alongside a 59.2/40.8 split; which share is internal is not stated.
- Grounds: planned distractor rates.
- Neutral topic: the proportions of self-initiated (internal) vs external interruptions, overall and by job role.

### C-mark05-3 — "half of switches self-initiated" lives in mark-chi05 / mark-gallup06 (borderline)
- Locations: docs/references.md:57 — "Does NOT contain the \"half of switches self-initiated\" claim (that lives in `mark-chi05` / `mark-gallup06`)."
- Neutral topic: whether the 2005 paper states what fraction of switches/interruptions are self-initiated.

## `mark-chi08` (references.md only)

Status (docs/references.md:53): verified (2026-08-26).

### C-mark08-1 — interruption/stress lab experiment; carries neither the 3-min nor the 12-min figure
- Locations: docs/references.md:52 — "interruption/stress lab experiment ONLY. Carries neither the 3-min nor the 12-min figure"; docs/workload/source-vetting.md:76 — "**CHI 2008 (\"The Cost of Interrupted Work\") contains neither figure** — it is the interruption-stress lab experiment"
- Neutral topic: the study design of the CHI 2008 paper and whether it reports time-per-task or time-per-working-sphere figures.

## `mark-chi14` (references.md only)

Status (docs/references.md:58): verified (2026-08-26).

### C-mark14-1 — attentional rhythms by time of day; no "half of switches self-initiated" claim
- Locations: docs/references.md:57; docs/workload/source-vetting.md:76 — "The CHI 2014 rhythm-of-attention paper does **not** contain the \"~half of switches self-initiated\" claim."
- Neutral topic: what the CHI 2014 paper reports about attention over the day and whether it states the share of self-initiated switches.

## `czerwinski-chi04` (references.md only)

Status (docs/references.md:63): verified (2026-08-26).

### C-czerwinski-1 — diary study of task switching and interruptions
- Locations: docs/references.md:62 — "diary-study evidence on task switching and interruptions."; docs/workload/source-vetting.md:76 — "Czerwinski/Horvitz/Wilhite CHI 2004 diary study confirmed as stated."; docs/workload/grounding-sources.md:40 — "Czerwinski/Horvitz diary studies"
- Neutral topic: the method and main task-switching/interruption findings of the CHI 2004 diary study.

## `mark-gallup06` (references.md only)

Status (docs/references.md:253): verified (2026-08-26).

### C-gallup-1 — the "23 min 15 s to resume" figure appears only in a 2006 Gallup interview
- Locations: docs/references.md:252 — "the ONLY source of the \"23 min 15 s to resume\" figure — appears in no peer-reviewed paper (independently audited)."; docs/workload/building-plan.md:136 — "(The \"23 minutes to resume\" figure exists only in a 2006 interview, `mark-gallup06` — cite as interview or omit.)"; docs/workload/source-vetting.md:76 — "**The \"23 min 15 s to resume\" figure exists only in the 2006 Gallup interview (`mark-gallup06`) — verified absent from all the peer-reviewed papers"
- Wording differences: "23 minutes" vs "23 min 15 s".
- Grounds: exclusion of the figure (prose).
- Neutral topic: whether the Gallup interview states a time to resume an interrupted task and its value; whether that figure appears in the Mark et al. CHI papers.

## `swell-icmi14` (references.md only)

Status (docs/references.md:93): verified-in-vetting (2026-08-25); author list to re-confirm at submission.

### C-swell-1 — SWELL-KW dataset contents and access
- Locations: docs/references.md:91-92 — "Data: DANS, DOI 10.17026/dans-x55-69zp (registration required)." / "qualitative citation for knowledge-worker computer logging with app names"; docs/workload/source-vetting.md:81 — "25 participants, knowledge-work tasks under interruption/time-pressure conditions; computer logging present but oriented to stress/task-recognition."; docs/workload/grounding-sources.md:41 — "Public multimodal knowledge-worker dataset including computer logging (application usage, window switching) — one of the few public datasets with app names intact"
- Wording differences: "Public" (grounding-sources) vs "request/registration required" (references.md, source-vetting).
- Grounds: prose only.
- Neutral topic: the SWELL-KW dataset's participants, conditions, logged modalities (including application names/window switching), and access terms.

---

## `dubroy-chi10`

Status (docs/references.md:83): verified (2026-08-26). Type: scholarly.

### C-dubroy-1 — logged concurrent-tab distributions: mode, per-user medians, tail
- Locations: dataset/sources.yaml:233-234 — "Logged concurrent-tab distributions: modal count 1, per-user medians mostly 1-6, long right tail (max 42)."; docs/references.md:82 — "logged concurrent-tab distributions: per-user medians mostly 1–6, long tail (max 42)."
- Wording differences: "modal count 1" only in sources.yaml.
- Grounds: renderer `count` bindings (see C-tabs-1).
- Neutral topic: the distribution of simultaneously open tabs logged per user — most common value, range of per-user medians, maximum.

### C-dubroy-2 — scope: participants, browser, data availability
- Locations: dataset/sources.yaml:234-235 — "Scope limits: N=21 recruited tab users, 2009 single-process Firefox. No public dataset."; docs/references.md:82 — "Caveats: N=21 recruited tab users, 2009 Firefox. No public dataset."
- Wording differences: "single-process" only in sources.yaml.
- Neutral topic: number and recruitment of participants, browser and version studied, study period, data availability.

## `chang-chi21`

Status (docs/references.md:88): verified (2026-08-26). Type: scholarly.

### C-chang-1 — tab-overwhelm threshold
- Locations: dataset/sources.yaml:240 — "median tab-overwhelm threshold 8 tabs (IQR 5-12)"; docs/references.md:87 — "median overwhelm threshold 8 tabs (Q1–Q3 = 5–12)"
- Neutral topic: the number of open tabs at which participants reported feeling overwhelmed — central value and spread.

### C-chang-2 — share of participants with many tabs at a snapshot
- Locations: dataset/sources.yaml:240-241 — "~8% of participants had >10 tabs open at a capped snapshot."; docs/references.md:87 — "~8% had >10 open at snapshot."
- Wording differences: "capped snapshot" only in sources.yaml.
- Neutral topic: the reported distribution of currently open tabs among participants and any cap on the reported value.

### C-chang-3 — self-report, not logging
- Locations: dataset/sources.yaml:242 — "Self-report, not logging"; docs/references.md:87 — "Self-report, not logged."
- Neutral topic: whether tab counts were self-reported or logged.

## `mozilla-testpilot10`

Status (docs/references.md:243): verified (2026-08-26). Type: deployed-system.

### C-testpilot-1 — mean tab count, sample size, duration, year
- Locations: dataset/sources.yaml:248-249 — "Only large-N logged concurrent-tab data: mean ~3.2 tabs (N~27k, one week, 2010)"; docs/references.md:241-242 — "\"A Week in the Life of a Browser\" study v2 (2010), N≈27,000 …" / "only large-N logged concurrent-tab data: mean ≈3.2 tabs"
- Neutral topic: in the aggregated Test Pilot tables, the mean number of open tabs, the number of participants, the study length and year.

### C-testpilot-2 — median per-user weekly maximum
- Locations: dataset/sources.yaml:249 — "median per-user weekly max <8"; docs/references.md:242 — "median weekly max <8"
- Neutral topic: the median of each user's maximum tab count over the week.

### C-testpilot-3 — upper quartile of users' tab counts
- Locations: dataset/sources.yaml:249-250 — "25% of users reached >=11."; docs/references.md:242 — "25% of users ≥11."
- Neutral topic: the tab count reached by the top quarter of users.

### C-testpilot-4 — only aggregate tables survive; licence; participant bias
- Locations: dataset/sources.yaml:250 — "Only aggregate tables survive (mirror)."; docs/references.md:241-242 — "CC-BY 3.0 US; aggregate tables mirrored at github.com/mozilla/testpilotweb (testcases/a-week-life-2/aggregated-data.html)." / "Caveats: 2010 opt-in enthusiasts; raw dumps no longer hosted."
- Neutral topic: the location, licence and form (raw vs aggregate) of the surviving Test Pilot study data; how participants were recruited.

### C-testpilot-5 — no post-2010 large-scale logged tab distribution exists publicly (borderline: claim about the literature)
- Locations: dataset/sources.yaml:250-251 — "Carries the honest-limitation line: no post-2010 large-scale logged tab distribution exists publicly."; docs/references.md:242 — "Honest-limitation line: no post-2010 large-scale logged tab distribution exists publicly."
- Neutral topic: whether any publicly available large-scale logged browser tab-count data newer than 2010 exists.

## `singervine-slate10` (references.md only)

Status (docs/references.md:248): verified (2026-08-26).

### C-singervine-1 — Slate article is the published analysis of the Test Pilot aggregates
- Locations: docs/references.md:246-247 — "Singer-Vine, J. \"Open This Story in a New Tab.\" *Slate*, 2010-12-05." / "the published analysis of `mozilla-testpilot10` — journalism, not peer review"
- Neutral topic: whether the Slate article analyses the Mozilla Test Pilot browsing dataset and which figures it reports.

## Tab-count literature — shared claim

### C-tabs-1 — renderer counts bind against the Chromium process model from the tab-count literature (dubroy-chi10, mozilla-testpilot10, chang-chi21) (borderline)
- Locations: dataset/archetypes.yaml:477-482 — "Renderer-children multiplicity is a static binding-time count (archetype-plan §3), expressed through the timeline task entry's count field: values bind against the Chromium process model from the tab-count literature (dubroy-chi10, mozilla-testpilot10, chang-chi21) plus meas-ci Xvfb counts"; docs/workload/archetype-plan.md:40 — "renderer counts from the tab-count literature (`dubroy-chi10`, `mozilla-testpilot10`, `chang-chi21` — defined against the Chromium process model) plus `meas-ci` Xvfb `/proc` counts."; docs/workload/building-plan.md:82 — "Renderer multiplicity is defined against the Chromium process model (`dubroy-chi10`, `mozilla-testpilot10`, `chang-chi21` + `meas-ci` Xvfb counts); firefox bindings reuse it as a stated approximation."; :189 — "tab counts (`dubroy-chi10`, `mozilla-testpilot10`, `chang-chi21`)"; docs/data-contracts.md:159 — "That is deliberate realism: a real process list during browsing shows a dozen identically-named Chrome processes, one per tab group."; docs/workload/coreset-guide.md:478 — "chrome 하나에 탭 12개." (c1-browsing described as 12 tabs)
- Wording differences: archetype-plan says the literature is "defined against the Chromium process model" (the three sources study Firefox or self-report); data-contracts says "one per tab group"; coreset-guide equates 12 renderers with 12 tabs. No timeline comment ties a specific count to any of the three sources (see Part 2(b)).
- Grounds: `count:` on chrome renderer tasks — 8 (c1-office.timeline.yaml:17; c3-workday.timeline.yaml:22), 12 (c1-browsing.timeline.yaml:16), 10 (c3-evening.timeline.yaml:19), 6 (c4.variant.yaml:27); steamwebhelper 3 (c1-gaming.timeline.yaml:18).
- Neutral topic: for each of the three sources, the browser studied and whether it says anything about processes per tab; separately, Chromium's documented process model (how renderer processes relate to tabs/sites).

---

## `focal-arxiv26`

Status (docs/references.md:98): verified (2026-08-26). Type: scholarly (preprint).

### C-focal-1 — A→B→A interruption sessions: 100 sessions, long creative task interrupted by short browsing
- Locations: dataset/sources.yaml:256-257 — "Establishes the A->B->A interruption session structure (100 sessions: long creative task interrupted by short browsing)"; docs/references.md:97 — "precedent for the A→B→A interruption timeline shape (DesktopBench: 320 multitask + 100 interruption sessions …)"; docs/workload/source-vetting.md:84 — "Interruption (100 sessions, controlled A→B→A: long creative task interrupted by short YouTube browsing)"; docs/workload/grounding-sources.md:42 — "evaluates context-switch robustness via A→B→A interruption splits (long creative task interrupted by short browsing) | Direct precedent for the within-segment distractor experiment (Q7)"; docs/workload/building-plan.md:137 — "DesktopBench's A→B→A interruption split (`focal-arxiv26`) is the special case of one excursion"
- Wording differences: "YouTube browsing" only in source-vetting; "controlled" only in source-vetting.
- Grounds: naturalistic generator excursion structure (planned); within-segment distractor (C4) precedent (prose).
- Neutral topic: in the FOCAL paper's DesktopBench description, the interruption split — number of sessions, the structure of a session, what the primary and interrupting activities are.

### C-focal-2 — 320 interleaved multitask sessions with app names and window titles; 20 templates
- Locations: dataset/sources.yaml:257-258 — "and 320 interleaved multitask sessions with app names + window titles."; docs/references.md:97 — "320 multitask"; docs/workload/source-vetting.md:84 — "Actions carry foreground app name + window title. Splits: Multitask (320 sessions, 20 interleaved cross-app templates)"
- Neutral topic: the multitask split — number of sessions, number of templates, and what fields each recorded action carries.

### C-focal-3 — sessions are scripted reconstructions from VideoGUI, not natural usage
- Locations: dataset/sources.yaml:259-260 — "Structure precedent only: preprint, and the sessions are scripted reconstructions from VideoGUI, not natural usage."; docs/references.md:97 — "co-cite `videogui-arxiv24` for session provenance"; :102 — "upstream source of DesktopBench's sessions"; docs/workload/source-vetting.md:84 — "DesktopBench is the benchmark inside the FOCAL paper, reconstructed from VideoGUI."
- Neutral topic: how DesktopBench sessions were produced (recorded natural use vs constructed from another dataset) and from which dataset.

### C-focal-4 — release location and data terms
- Locations: dataset/sources.yaml:260-261 — "Data terms restrict redistribution; methodological reuse is unrestricted."; docs/references.md:97 — "released on HuggingFace `HaoranYin/desktopbench` v0.1.0; data terms restrictive — research inspection only, no redistribution; scripts MIT"; docs/workload/grounding-sources.md:82 — "released on HuggingFace, restrictive data terms, MIT scripts; methodological reuse unrestricted"; docs/workload/building-plan.md:137 — "Optional sanity check: DesktopBench inter-action timings (license permits analysis, not redistribution)."
- Wording differences: building-plan implies the release contains inter-action timings.
- Neutral topic: where DesktopBench is released, its version, the data licence terms and the script licence; whether per-action timestamps are included.

### C-focal-5 — bibliographic identity
- Locations: docs/references.md:96 — "Yin, H., Wen, Z., Cao, J., Yuan, B., & Yang, R. (2026). FOCAL: Filtered On-device Continuous Activity Logging for Efficient Personal Desktop Summarization. arXiv:2604.19541 (v2, 2026-07-18). **Preprint — no venue.**"; docs/workload/source-vetting.md:83 — "DesktopBench (in FOCAL, arXiv 2604.19541, 2026)"
- Neutral topic: authors, title, arXiv number, version and date, venue status.

## `videogui-arxiv24` (references.md only)

Status (docs/references.md:103): provisional — full author list/title to pin before citing.

### C-videogui-1 — upstream source of DesktopBench sessions
- Locations: docs/references.md:101-102 — "Lin et al. (2024). VideoGUI. arXiv:2406.10227." / "upstream source of DesktopBench's sessions"; docs/workload/source-vetting.md:84
- Neutral topic: the VideoGUI paper's identity and whether DesktopBench derives from it.

---

## `schbench` (references.md only)

Status (docs/references.md:150): verified-in-vetting (2026-08-25).

### C-schbench-1 — design and reported percentiles
- Locations: docs/workload/source-vetting.md:58 — "github.com/masoncl/schbench (mirror on kernel.googlesource.com), pin v1.0. Message threads + worker threads; request = 2× usleep + matrix math; per-CPU spinlock. Reports wakeup latency, request latency, RPS as percentile distributions (20/50/75/90/95/99/99.5/99.9)."; docs/references.md:148-149 — "Mason, C. schbench. github.com/masoncl/schbench, v1.0." / "tail-latency metric precedent (P99-focused reporting)"; docs/workload/grounding-sources.md:28 — "schbench (Mason, 2016) | Wakeup-latency benchmark reporting tail percentiles (P99) | Precedent for our latency metrics (tail-focused, not mean); also the messaging/wakeup-heavy process archetype"
- Wording differences: "(Mason, 2016)" year only in grounding-sources; "Chris Mason / Meta" in source-vetting:57 heading.
- Grounds: prose only (metric precedent; no archetype uses it).
- Neutral topic: schbench's thread structure, what a request does, which latencies and percentiles it reports, its version and author.

### C-schbench-2 — cited by SchedCP by git URL
- See C-schedcp-4 (same locations).

## `hackbench` (references.md only)

Status (docs/references.md:155): verified (2026-09-12; repository cloned from git.kernel.org and both files read).

### C-hackbench-1 — pairs of tasks communicating over sockets/pipes; default task count; message size
- Locations: docs/workload/source-vetting.md:61 — "In rt-tests (github.com/jlelli/rt-tests, src/hackbench, GPL-2.0) and perf bench sched messaging. Pairs of tasks over sockets/pipes; defaults 10 groups × 40 fds = 400 tasks, 100 msgs × 100 B. Grounds many-task IPC burst archetype."; docs/references.md:154 — "Defaults read from the source: `datasize = 100`, `loops = 100`, `num_groups = 10`, `num_fds = 20`. The printed banner is \"Running in process mode with 10 groups using 40 file descriptors each (== 400 tasks)\" because, per the man page, \"the effective number will be twice the amount you set here, as the sender and receiver children will each open the given amount of file descriptors\" — 10 × 20 × 2 = 400. Reports a single completion time; no latency distribution"; docs/workload/grounding-sources.md:29 — "Kernel-community load-balancing stressor (many communicating tasks) | The chat/IPC-heavy archetype's burst structure"; docs/workload/source-vetting.md:52 — interbench "Hack (hackbench 50)"
- Wording differences: "10 groups × 40 fds" (source-vetting) vs `num_fds = 20` doubled to 40 (references.md); "load-balancing stressor" (grounding-sources) vs "benchmark and a stress test for the Linux kernel scheduler" (references.md man-page quote); no archetype in archetypes.yaml is an IPC archetype.
- Grounds: prose only.
- Neutral topic: hackbench's defaults (groups, file descriptors, message size, loops), how many tasks those defaults create, what it reports, and where it is distributed (rt-tests, perf).

### C-hackbench-2 — community standing
- Locations: docs/workload/source-vetting.md:87 — "hackbench: \"a stalwart of kernel scheduler testing\" (LWN survey, Articles/725238); in perf + rt-tests."
- Neutral topic: the wording of the LWN article at that number about hackbench.

## `stress-ng` (references.md only)

Status (docs/references.md:160): verified-in-vetting (2026-08-25).

### C-stress-ng-1 — generic stressors, no behavioural timing
- Locations: docs/workload/source-vetting.md:67 — "github.com/ColinIanKing/stress-ng, GPL-2.0. Generic CPU/VM/IO stressors; no behavioral timing."; docs/references.md:158-159 — "King, C. I. stress-ng. github.com/ColinIanKing/stress-ng, GPL-2.0." / "Role B fallback archetypes only"; docs/workload/grounding-sources.md:31 — "Configurable stressor collection | Fallback archetypes only (pure CPU hog, I/O hog)"; docs/workload/source-vetting.md:87 — "stress-ng: widely cited in systems/energy papers."
- Grounds: prose only.
- Neutral topic: stress-ng's author, licence, stressor categories, and whether it models timing of real application behaviour.

---

## Unattributed / plain-text external claims (no docs/references.md id)

### C-plain-1 — Chromium process model (renderer processes per tab) (borderline)
- Locations: dataset/archetypes.yaml:479 — "the Chromium process model"; docs/workload/archetype-plan.md:40; docs/workload/building-plan.md:82; docs/data-contracts.md:159 — "a real process list during browsing shows a dozen identically-named Chrome processes, one per tab group"
- Grounds: renderer `count` bindings (see C-tabs-1).
- Neutral topic: Chromium's documented process model — which processes a browser session runs, how renderer processes map to tabs or sites, and their process name on Linux.

### C-plain-2 — ClamAV's stock scheduled-scan deployment pattern
- Locations: docs/workload/scenario-catalog.md:28 — S17 "ClamAV stock scheduled-scan deployment pattern"
- Grounds: S17 row (clamscan as unwanted-now background; injected into c2-p2b and ten C7 files).
- Neutral topic: whether ClamAV packages ship a scheduled scan by default (timer/cron) and which process performs it (clamscan, clamd, freshclam).

### C-plain-3 — indexers are stock background services: GNOME tracker-miner, KDE baloo, plocate timers
- Locations: docs/workload/scenario-catalog.md:25 — S14 "shipped defaults (GNOME tracker-miner, KDE baloo, plocate timers are stock background services)"; docs/data-contracts.md:173 — "rename the process `python3` to `tracker-miner-fs-3` (the GNOME file indexer)"
- Grounds: S14 row; names `tracker-miner-fs-3`, `baloo_file`, `updatedb`.
- Neutral topic: whether GNOME ships tracker-miner-fs(-3), KDE ships baloo_file, and plocate ships an updatedb timer enabled by default; the process names each runs under.

### C-plain-4 — Jellyfin's transcoder runs as plain `ffmpeg`
- Locations: dataset/timelines/coreset/c7.variant.yaml:20-21 — "(transcode: Jellyfin installs its transcoder as plain `ffmpeg`)"; docs/workload/building-plan.md:121 — "(Jellyfin's transcoder runs as plain `ffmpeg`)"; docs/workload/coreset-guide.md:916 — "(Jellyfin의 transcoder도 process 이름은 그냥 `ffmpeg`)"; docs/daemon/prior-table-pair-review.md:58 — "(Jellyfin's transcoder runs as plain `ffmpeg`, so no distinct unwanted name exists)"
- Wording differences: "installs its transcoder as" vs "transcoder runs as" vs "process name is just".
- Grounds: c7-transcode shipped as label-flip-only `pre_committed_miss` (c7.variant.yaml:158-164).
- Neutral topic: the executable/process name Jellyfin uses for transcoding on Linux (and whether it ships a renamed build).

### C-plain-5 — no distro or vendor runs an unwanted ml-train/render/transcode/backup job under a distinct name (borderline; negative existence claim)
- Locations: dataset/timelines/coreset/c7.variant.yaml:19-22 — "ml-train, render, transcode, backup: no same-mode orchestrator a distro or vendor runs unasked under a distinct name exists … so the label flips alone and the file ships as a pre-committed miss."; docs/workload/building-plan.md:121 — "`ml-train`, `render`, `transcode`, `backup` have no same-mode unwanted name a distro or vendor runs under a distinct string"; docs/workload/coreset-guide.md:916 — "나머지 넷은 배포판·vendor가 다른 이름으로 돌리는 같은 mode의 unwanted job이 없어서"
- Grounds: c7-ml-train, c7-render, c7-transcode, c7-backup as `pre_committed_miss`.
- Neutral topic: for scheduled/automatic ML training, media rendering, transcoding and backup jobs that distributions or vendors start without the user, the process names they run under.

### C-plain-6 — Proton games appear as `<game>.exe` (borderline)
- Locations: docs/workload/scenario-catalog.md:20 — S9 "<game>.exe (Proton)"; docs/workload/coreset-guide.md:513 — "Proton 게임. `game.exe` 300개 task"; bindings `name: game.exe` in c1-gaming.timeline.yaml:13, c2-p2a.timeline.yaml:14, c3-evening.timeline.yaml:20, c6-dual.timeline.yaml:13
- Grounds: task name `game.exe` for all game-task-chain members.
- Neutral topic: the process names under which Windows games run through Proton/Wine on Linux, and whether all game threads/processes share one name.

### C-plain-7 — no public trace of desktop process timelines with process names exists; why candidate datasets fail (borderline; claims about the literature)
- Locations: docs/workload/grounding-sources.md:52 — "**no public trace of desktop process timelines with process names exists.**"; :56 — "Enterprise / VDI / cloud workload traces (Azure, Google cluster traces, VDI characterization studies) | Server/VM granularity; no consumer applications; process identity absent or hashed"; :57 — "Desktop trace studies (older workload characterization literature) | Aggregate statistics survive; raw timelines with names were never released, largely for privacy"; :58 — "HCI logging datasets (beyond SWELL) | App-level events without the process-level detail"; docs/workload/source-vetting.md:101 — "No public desktop process-timeline trace with process names exists — confirmed; synthesis justified."; :60 — "which no prior work in the LLM-scheduling line has done"
- Grounds: rationale for a synthetic dataset (prose).
- Neutral topic: whether public traces of desktop process activity with process names exist; what process-identity fields Azure/Google cluster traces carry.

### C-plain-8 — anti-roles: Phoronix/UnixBench; mobile app-usage datasets (borderline)
- Locations: docs/workload/grounding-sources.md:64 — "**Phoronix Test Suite / UnixBench**: performance measurement of a machine, not scenario definitions"; :65 — "**Mobile app-usage datasets (launch prediction, screen-time)**: … mobile foreground-exclusivity makes the concurrency structure disanalogous to desktop multitasking"
- Grounds: prose only (source exclusion).
- Neutral topic: what Phoronix Test Suite and UnixBench measure; whether mobile app-usage datasets record concurrent foreground apps.

### C-plain-9 — citation precedents for community artifacts (borderline)
- Locations: docs/workload/source-vetting.md:14 — "Citing community open-source tools is normal practice; … interbench/hackbench/rt-app/stress-ng have LWN-documented or peer-reviewed usage precedents."; :87 — "Verdict: citing community tools by git URL + pinned commit is established practice."
- Grounds: prose only.
- Neutral topic: examples of peer-reviewed papers citing these tools by repository URL.

### C-plain-10 — meas-ci-tagged statements that describe third-party software (borderline; listed for completeness, source excluded)
- dataset/timelines/coreset/c7.variant.yaml:17-19 — "names workflow meas-ci:names:2 observed comm `dkms` at runtime level on all three distros, Fedora shipping a kernel-install hook and a dkms.service unit — dataset/meas/names/run-2/)" — topic: whether Fedora's dkms package ships a kernel-install plugin and a systemd `dkms.service`.
- dataset/timelines/coreset/c2-pairs.variant.yaml:16-17 — "clamscan binds cpu-batch: full-scan state is CPU-saturating (meas-ci:cli:3 finding: foreground clamscan per-proc duty ~1.0)."; c7.variant.yaml:7-8 — "clamscan bound cpu-batch (full-scan state is CPU-saturating, meas-ci:cli:3)"; dataset/archetypes.yaml:328-330 — "foreground scans never throttle (clamscan per-proc duty ~1.0 warm AND ~0.98 cold)".
- dataset/archetypes.yaml:466-469 — "Element Desktop idling unauthenticated under Xvfb (stated substitute for account-gated comms apps; idle lacks message-traffic wakes — stated limitation)".
- dataset/archetypes.yaml:320-325 — "tracker-miner-fs-3 under dbus-run-session indexing a corpus copy for 300 s per repeat".
- dataset/archetypes.yaml:205-208 — "meas-ci:cli:3 (linux-6.6 defconfig, make -j8, 5 repeats): ~11.9k compiler-family children per build".
- dataset/tools/meas/verify_names.py:40, :80 — "expect updatedb.plocate on plocate systems"; "binary-only; runtime topology decided at constructor time" (wineserver).
- docs/workload/building-plan.md:185 — "(soffice.bin vs soffice, updatedb.plocate, cc1 path)".

---

# Part 2(a) — Every numeric value in `dataset/archetypes.yaml`, with its source tag

"Notes say" quotes the entry's own `modeling_notes` (or `validation_stats`) about that value. **FLAG** marks a value carrying an external (non-meas) tag while its own notes call it ours / convention / placeholder / arithmetic, or where the notes attribute it to a different source than the tag. `meas-ci` rows are listed for completeness (tag excluded as a source by the brief); flags on them note convention statements only.

File-level conventions that apply to every row: dataset/archetypes.yaml:19 — "distribution family defaults to lognormal by stated convention (archetype-plan OQ-5)"; :8-9 — "source tags justify values and described structure, never field names"; :31-33 — "`meas-pending` params carry explicit placeholder values … the tag marks every number in that param as provisional". Related repo-level statements: dataset/README.md:132 "The library is fully measured"; docs/data-contracts.md:76 "Every number in the library is either taken from published measurements or measured by us in CI"; docs/data-contracts.md:96 "Nothing in the library is an unsourced number."

| # | archetype.param | field = value | line | source tag | notes say | flag |
|---|---|---|---|---|---|---|
| 1 | audio-playback.period | dist constant, value_us = 50000 | 52 | `interbench:man-audio` | :66-68 "interbench man-audio states \"wakes every 50 ms needing 5% CPU\"; the TIMER/RUN transcription … are ours" | — (value restates source figure in µs) |
| 2 | audio-playback.burst | dist constant, value_us = 2500 | 55 | `interbench:man-audio` | :67-68 "the duty-cycle-to-duration arithmetic (5% of 50 ms = 2,500 us per period) are ours" | **FLAG: arithmetic (ours) under external tag** |
| 3 | audio-playback.validation_stats | "wakeup-rate 20 Hz, cpu-share 5%" | 62 | (none; note :63-64 "values are interbench's community interactivity model") | derived rate 20 Hz | borderline: 20 Hz is derived |
| 4 | video-playback.period | dist constant, value_us = 16667 | 80 | `interbench:man-video` | :93-94 "the 16,667 us period and 40%-duty burst (6,667 us) arithmetic are ours" | **FLAG: arithmetic (ours) under external tag** (conversion/rounding of 16.7 ms / 60 Hz) |
| 5 | video-playback.burst | dist constant, value_us = 6667 | 82 | `interbench:man-video` | :93-94 (same) | **FLAG: arithmetic (ours) under external tag** |
| 6 | video-playback.validation_stats | "wakeup-rate 60 Hz, cpu-share 40%" | 89 | (none; note :90-91) | — | — |
| 7 | desktop-interactive.input_gap | dist lognormal-mixture | 109 | `dhakal-chi18` | :132-133 "the two-component log-normal family is roeser-rw24's" | **FLAG: family attributed to roeser-rw24 in notes, tag is dhakal-chi18** |
| 8 | desktop-interactive.input_gap | fluent_mean_us = 158000 | 109 | `dhakal-chi18` | :133 "(fluent ~158 ms, pause component p~0.34 — task-dependent, cite the family not a parameter set)" attributed to roeser-rw24 | **FLAG: notes attribute to roeser-rw24 and say not to cite a single parameter set; tag is dhakal-chi18** |
| 9 | desktop-interactive.input_gap | fluent_sigma_log = 0.35 | 110 | `dhakal-chi18` | :136-138 "The sigma_log values are our convention within the cited log-normal family" | **FLAG: convention (ours) under external tag** |
| 10 | desktop-interactive.input_gap | pause_probability = 0.34 | 110 | `dhakal-chi18` | :133 attributed to roeser-rw24, "task-dependent" | **FLAG: notes attribute to roeser-rw24; tag is dhakal-chi18** |
| 11 | desktop-interactive.input_gap | pause_mean_us = 395235 | 111 | `dhakal-chi18` | :134-136 "pause_mean_us is our arithmetic closing the mixture on dhakal's overall mean: (238,660 - 0.66*158,000)/0.34 ~ 395,235 us." | **FLAG: arithmetic (ours) under external tag**; arithmetic mixes a dhakal figure with roeser figures |
| 12 | desktop-interactive.input_gap | pause_sigma_log = 0.6 | 111 | `dhakal-chi18` | :136-138 "our convention" | **FLAG: convention (ours) under external tag** |
| 13 | desktop-interactive.input_gap | overall_mean_us = 238660 | 112 | `dhakal-chi18` | :134-135 "dhakal's overall mean" | — (factual note: dataset/tools/wlc/sampling.py:53-60, 78-80 do not read this field; the sampled mean is (1−p)·fluent + p·pause) |
| 14 | desktop-interactive.input_gap_family | family = two-component-lognormal (no numeric) | 115 | `roeser-rw24` | :132-133 | — |
| 15 | desktop-interactive.burst_fraction | dist uniform, min = 0.0 | 118 | `interbench:man-x` | :138-141 "Burst CPU cost linearizes interbench man-x's \"variable 0-100%\" as a uniform fraction of the preceding input gap; the burst/pause macro-structure beyond the mixture is our modeling" | **FLAG: uniform family and fraction-of-gap mapping are our linearization under external tag** |
| 16 | desktop-interactive.burst_fraction | max = 1.0 | 118 | `interbench:man-x` | same | **FLAG** (as 15) |
| 17 | compiler-child.cpu_burst | lognormal median_us = 12900, sigma_log = 1.91 | 183 | `meas-ci:cli:3` | :210-214 "median cpu = (cpu_mean/life_mean) x life_median ~ 14.4 ms; sigma_log 1.91 from mean/median = 6.25"; :214 "The 90/10 burst/tail split is ours." | flag (meas): 90 % split of 14.4 ms is ours |
| 18 | compiler-child.cpu_tail | lognormal median_us = 1440, sigma_log = 1.91 | 186 | `meas-ci:cli:3` | :214 "The 90/10 burst/tail split is ours." | flag (meas): split ours |
| 19 | compiler-child.disk_wait | lognormal median_us = 3600, sigma_log = 0.8 | 189 | `meas-ci:cli:3` | :214-218 "median 3.6 ms is that measured bound (machine-relative, runner spec recorded)"; sigma 0.8 not explained | note: sigma_log 0.8 has no stated derivation |
| 20 | build-orchestrator.dispatch_overhead | lognormal median_us = 234, sigma_log = 0.5 | 234 | `meas-ci:cli:3` | :252-255 "(5-repeat medians 183-262 us; observed fork rate ~24 children/s at -j8); sigma_log is our convention." | flag (meas): sigma convention |
| 21 | build-orchestrator (prose default) | spawn_count default 2,430 | 247-248 | prose cite `ocallahan-atc17 sec-4.3` | "spawn_count binds per timeline — the kernel-build default is 2,430" | note: binding-time default in prose; archetypes.yaml:25-26 says counts never carry values in the file, defaults live in modeling_notes prose; no timeline binds 2,430 |
| 22 | build-orchestrator (prose default) | parallelism_cap default -j8 | 248-250 | prose, "archetype-plan OQ-4: between interbench's documented -j4 and desktop nproc conventions" | "by stated convention" | **FLAG (prose): convention bracketed by an interbench figure** |
| 23 | io-stream.block_cpu | lognormal median_us = 3000, sigma_log = 0.6 | 269 | `meas-ci:cli:3` | :286-288 "the 3 ms block granularity and sigmas are our convention; the measured quantity is the per-process cpu:wall duty of a stream" | flag (meas): value and sigma convention |
| 24 | io-stream.io_wait | lognormal median_us = 10000, sigma_log = 0.6 | 272 | `meas-ci:cli:3` | :289-291 "measures 0.231 (spread 0.155-0.267) -> io_wait = block_cpu x (1/0.231 - 1) ~ 10 ms"; sigma convention | flag (meas): arithmetic from a convention block size; sigma convention; references interbench cache-defeating intent (C-interbench-7) |
| 25 | background-crawler.scan_burst | lognormal median_us = 1608, sigma_log = 0.639 | 304 | `meas-ci:cli:3` | :323-324 "cpu-per-wake median ~1.6 ms sigma_log ~0.64" | — |
| 26 | background-crawler.io_wait | lognormal median_us = 5870, sigma_log = 0.6 | 307 | `meas-ci:cli:3` | :326-328 "io_wait derives from the cold-cache updatedb duty 0.215 (spread 0.147-0.244): scan_burst x (1/0.215 - 1) ~ 5.9 ms; its sigma is our convention." | flag (meas): arithmetic; sigma convention |
| 27 | background-crawler.throttle | lognormal median_us = 3800000, sigma_log = 0.428 | 310 | `meas-ci:cli:3` | :324-325 "inter-wake gap median ~3.8 s sigma_log ~0.43" | — |
| 28 | game-task-chain.n_tasks | constant value = 300 | 350 | `lavd-ossna24:s12` | :386 "expands it into n_tasks ordinary tasks" | — (point value for "~300") |
| 29 | game-task-chain.frac_long_lived | constant value = 0.90 | 353 | `lavd-ossna24:s12` | not discussed in notes | note: not read by any tool in dataset/tools |
| 30 | game-task-chain.per_schedule_run | lognormal anchor_min_us = 260 | 356 | `lavd-ossna24:s13` | :390-393 "anchors are the source's wineserver ~260 us and worker ~1.65 ms endpoints, lognormal family by OQ-5 convention (the compiler derives median/sigma treating the anchors as the p05/p95 span)" | **FLAG: lognormal family (convention) and p05/p95 reading (ours) under external tag** |
| 31 | game-task-chain.per_schedule_run | anchor_max_us = 1650 | 356 | `lavd-ossna24:s13` | same | **FLAG** (as 30) |
| 32 | game-task-chain.frac_wakeups_from_wait | uniform min = 0.70 | 359 | `lavd-ossna24:s14` | not discussed; uniform family not justified in notes | note: not read by any tool in dataset/tools; borderline flag (uniform over a reported range is a modeling choice) |
| 33 | game-task-chain.frac_wakeups_from_wait | max = 0.75 | 359 | `lavd-ossna24:s14` | same | same |
| 34 | game-task-chain.frame_period | constant value_us = 16667 | 362 | `lavd-ossna24` (no locator) | not discussed beyond the chain wiring | borderline flag: µs rounding of 16.7 ms (same arithmetic the video entry calls ours) |
| 35 | game-task-chain.chain_length | constant value = 16 | 365 | `lavd-ossna24` (no locator) | :393-394 "chain_length 16 sits in the source's 15-20 frame-critical band" | **FLAG (borderline): a choice within a source range; "frame-critical" is the repo's characterization** |
| 36 | game-task-chain.tail_idle_gap | lognormal median_us = 500000, sigma_log = 0.5 | 368 | `lavd-ossna24:s12` | :395-397 "tail param values are our placeholder encoding of near-idle, provisional like any meas-pending value" | **FLAG: placeholder (ours) under external tag** (also contrasts with README.md:132 "fully measured") |
| 37 | game-task-chain.tail_run | lognormal median_us = 200, sigma_log = 0.5 | 371 | `lavd-ossna24:s12` | same | **FLAG: placeholder (ours) under external tag** |
| 38 | game-task-chain (prose) | "top 30-40 tasks = 95% of scheduling; 15-20 game tasks take 60-70%" | 397-399 | prose, LAVD | "Lane-scaling defense" | — (C-lavd-10/11) |
| 39 | network-bulk.chunk_cpu | lognormal median_us = 1000, sigma_log = 0.5 | 417 | `meas-ci:cli:3` | :432-434 "the 1 ms chunk granularity and sigmas are our convention" | flag (meas): value and sigma convention |
| 40 | network-bulk.net_wait | lognormal median_us = 16700, sigma_log = 0.5 | 420 | `meas-ci:cli:3` | :434-437 "wget's cpu:wall duty … ~0.057, wide spread 0.013-0.1 and only 2 of 5 repeats' downloads ran long enough to sample — stated) -> net_wait = chunk_cpu x (1/0.057 - 1) ~ 16.7 ms" | flag (meas): arithmetic from convention chunk; sigma convention |
| 41 | electron-comms.heartbeat | lognormal median_us = 1850000, sigma_log = 1.09 | 451 | `meas-ci:gui:2` | :468-470 "voluntary-wakeup gap median ~1.85 s sigma_log ~1.09"; :470-472 "The TIMER encoding approximates the observed aperiodic-ish wake stream as periodic — stated simplification." | — |
| 42 | electron-comms.heartbeat_work | lognormal median_us = 289, sigma_log = 0.713 | 454 | `meas-ci:gui:2` | :470 "cpu-per-wake median ~289 us" | — |
| 43 | electron-comms (prose) | "Chromium at 10 file tabs peaked at 21-22 processes" | 475-476 | meas-ci (prose) | "binding guidance for renderer counts" | note: renderer counts also bound "against the Chromium process model from the tab-count literature (dubroy-chi10, mozilla-testpilot10, chang-chi21)" (C-tabs-1) |
| 44 | system-daemon.idle_gap | lognormal median_us = 11240000, sigma_log = 1.9 | 493 | `meas-ci:gui:2` | :511 "voluntary-wakeup gap median ~11.2 s sigma_log ~1.9" | — |
| 45 | system-daemon.wake_burst | lognormal median_us = 155, sigma_log = 0.809 | 496 | `meas-ci:gui:2` | :511 "cpu-per-wake median ~155 us" | — |

Archetypes with no numeric params: `cpu-batch` (params: {}, :151). `binding_params` carry names only.

Summary of FLAGs on externally tagged values: interbench — rows 2, 4, 5, 15, 16 (plus prose row 22); dhakal-chi18 tag — rows 7, 8, 9, 10, 11, 12; lavd-ossna24 — rows 30, 31, 35, 36, 37 (borderline 32-34). Values tagged external with no flag: rows 1, 13, 28, 29.

---

# Part 2(b) — Numbers in `dataset/timelines/**` and whether a citation in comments justifies them

## Numbers justified by a citation in a comment

| file:line | number in comment | citation | what it justifies |
|---|---|---|---|
| dataset/timelines/coreset/c2-pairs.variant.yaml:16-17 | "foreground clamscan per-proc duty ~1.0" | `meas-ci:cli:3` (excluded source) | binding `clamscan` → `cpu-batch` in c2-p2b (:21-22, `total_work: 25s` itself not justified) |
| dataset/timelines/coreset/c7.variant.yaml:7-8 | (no number) "full-scan state is CPU-saturating, meas-ci:cli:3" | `meas-ci:cli:3` | binding `clamscan` → `cpu-batch` in the ten interactive C7 files |
| dataset/timelines/coreset/c7.variant.yaml:17-19 | "on all three distros" | `meas-ci:names:2` (and `dkms-man`, `dkms-debian` for the rebuild semantics) | rename `make` → `dkms` in c7-compile (:130) |

No timeline comment cites an external (non-meas) source for any number. External citations in timeline comments justify structure/order only:

| file:line | citation in comment | what it justifies (no number) |
|---|---|---|
| c3-workday.timeline.yaml:1-3 | "CpsMark+ CA cooperative workflow (cpsmark-tbench23)" | segment order browsing → office → compile → mail (C-cpsmark-5) |
| c3-creation.timeline.yaml:1-2 | "CpsMark+ CC; SYSmark 30 ACC photo<->video multitasking" | segment order photo → video-edit → transcode (C-cpsmark-12, C-sysmark30-3) |
| c7.variant.yaml:15-17 | "dkms-man, dkms-debian" | `make` → `dkms` rename and label `initiated: scheduled`, `background_wanted: false` (C-dkms-man-2) |
| c7.variant.yaml:20-21 | "Jellyfin installs its transcoder as plain `ffmpeg`" (no id) | c7-transcode as label-flip-only miss (C-plain-4) |
| c1-meeting.timeline.yaml:4-7 | "archetype-plan OQ-2" (internal); "zoom per the S3 catalog row" | zoom bound to video-playback/audio-playback/electron-comms |
| c1-gaming.timeline.yaml:2 | "(ours)" | gamescope → video-playback |

## All numeric bindings in authored timelines/recipes, none justified by a comment citation

Durations of segments, arrive/depart and focus windows are authored design values (building-plan §3 "compressed event-time"); they are omitted from the table except where a comment gives a reason.

| file:line | binding | comment justification |
|---|---|---|
| c1-backup.timeline.yaml:17-18 | borg `total_work: 30s` | :3-4 "total_work resized from 75 s to 30 s so the job finishes inside the 60 s segment (turnaround term)" (internal, Phase 7 spec decision 8) |
| c1-compile.timeline.yaml:15 | `spawn_count: 100, parallelism_cap: 8, child_name: cc1` | none (parallelism 8 matches archetypes.yaml:248-250 convention; count ≠ the 2,430 default in archetypes.yaml:247-248) |
| c1-browsing.timeline.yaml:16 | chrome renderers `count: 12` | none (C-tabs-1 prose elsewhere) |
| c1-gaming.timeline.yaml:14 | `lane_share: 0.9` | none |
| c1-gaming.timeline.yaml:18 | steamwebhelper `count: 3` | none |
| c1-indexing.timeline.yaml:21-22 | tracker-miner-fs-3 `total_work: 30s` | :4-5 "resized from 130 s to 30 s" (internal) |
| c1-mail.timeline.yaml:17-18 | thunderbird send `total_work: 3s` | none |
| c1-ml-train.timeline.yaml:17-18 | python3 `total_work: 30s` | :3-4 "resized from 130 s to 30 s" (internal) |
| c1-office.timeline.yaml:17 | chrome renderers `count: 8` | none |
| c1-render.timeline.yaml:17-18 | ffmpeg `total_work: 30s` | :3-4 "resized from 75 s to 30 s" (internal) |
| c1-transcode.timeline.yaml:17-18 | HandBrakeCLI `total_work: 30s` | :3-4 "resized from 320 s to 30 s" (internal) |
| c2-p1a.timeline.yaml:18-19 | python3 `total_work: 130s` | none |
| c2-p2a.timeline.yaml:15 | `lane_share: 0.95` | none |
| c2-p2a.timeline.yaml:20-21 | steam download `total_work: 25s` | none |
| c2-p3a.timeline.yaml:16-17 | ffmpeg `total_work: 75s` | none |
| c2-pairs.variant.yaml:21-22 | clamscan `total_work: 25s` | archetype choice only (meas-ci:cli:3) |
| c2-pairs.variant.yaml:31-32 | borg `total_work: 75s` | none |
| c3-creation.timeline.yaml:20-21 | HandBrakeCLI `total_work: 320s` | none |
| c3-evening.timeline.yaml:19 | chrome renderers `count: 10` | none |
| c3-evening.timeline.yaml:21 | `lane_share: 1.45` | none |
| c3-workday.timeline.yaml:22 | chrome renderers `count: 8` | none |
| c3-workday.timeline.yaml:26 | `spawn_count: 4200, parallelism_cap: 8` | none (count ≠ 2,430 default) |
| c3-workday.timeline.yaml:29-30 | thunderbird send `total_work: 3s` | none |
| c4.variant.yaml:16-17 | 7z `total_work: 6s` | none |
| c4.variant.yaml:25-27 | injected chrome renderers `count: 6` | none |
| c6.variant.yaml:11-12 | spoof chrome `total_work: 30s` | none |
| c6-dual.timeline.yaml:14 | `lane_share: 0.6` | none |
| c6-dual.timeline.yaml:17-18 | `spawn_count: 85, parallelism_cap: 8` | none |
| c7.variant.yaml:30-121 (×10) | clamscan `total_work: 60s` | :10-11 "Arrives at 0 s with total_work equal to the segment, so the label holds at every instant under every policy." (internal) |
| c5.variant.yaml:11, :19, :27 | `familiarity: 3/4/5` | :6, :14, :22 tier comments (internal definitions, building-plan §3 C5) |
| all authored timelines `meta.seed` | 101–116, 201–203, 301–303, 601 | none (reproducibility, not grounding) |

---

# Part 3 — Scenario-tag index (timeline `scenario:` tags → catalog row → sources the row names)

Catalog rows are docs/workload/scenario-catalog.md:12-29. Locations are the authored timeline/recipe lines carrying the tag; GENERATED derived timelines inherit tags from their bases unless a recipe patches them.

| tag | authored locations | catalog line | sources named in the row (claim entries) |
|---|---|---|---|
| S1 | c1-office.timeline.yaml:9; c3-workday.timeline.yaml:12; c7.variant.yaml:44 | :12 | CpsMark+ Table 2 document manipulation; SYSmark 30 Office Applications; PCMark 10 Productivity (C-cpsmark-3/4, C-sysmark30-1, C-pcmark-1) |
| S2 | c1-browsing.timeline.yaml:10; c1-office.timeline.yaml:9; c3-workday.timeline.yaml:10, :12; c3-evening.timeline.yaml:9; c6.variant.yaml:25; c7.variant.yaml:34, :44 | :13 | PCMark 10 Essentials; CpsMark+ Internet service (Chrome 73); SYSmark 30 General Productivity (Chrome 106) (C-pcmark-1, C-cpsmark-4, C-sysmark30-2) |
| S3 | c1-meeting.timeline.yaml:15; c6.variant.yaml:27; c7.variant.yaml:84 | :14 | PCMark 10 Essentials (Video Conferencing) (C-pcmark-1) |
| S4 | c1-mail.timeline.yaml:12; c1-office.timeline.yaml:9; c3-workday.timeline.yaml:16; c7.variant.yaml:44, :54 | :15 | CpsMark+ Internet service (Outlook); CpsMark+ CA workflow (email stage) (C-cpsmark-4/5) |
| S5 | c3-evening.timeline.yaml:11 | :16 | ananicy/CachyOS comms class; LAVD companion apps (C-ananicy-rules-7, C-lavd-16) |
| S6 | c1-photo.timeline.yaml:10; c3-creation.timeline.yaml:9; c7.variant.yaml:74 | :17 | PCMark 10 DCC Photo Editing (ImageMagick); SYSmark 30 Photo Editing; CpsMark+ graphic design (C-pcmark-1/2, C-sysmark30-4, C-cpsmark-4) |
| S7 | c1-backup.timeline.yaml:12; c1-video-edit.timeline.yaml:11; c1-render.timeline.yaml:12; c2-p3a.timeline.yaml:9, :11; c2-pairs.variant.yaml:35; c3-creation.timeline.yaml:11; c7.variant.yaml:114 | :18 | PCMark 10 DCC; CpsMark+ multimedia processing; SYSmark 30 ACC (C-pcmark-1, C-cpsmark-4, C-sysmark30-1) |
| S8 | c1-transcode.timeline.yaml:12; c1-render.timeline.yaml:12; c2-p3a.timeline.yaml:11; c3-creation.timeline.yaml:13 | :19 | CpsMark+ multimedia processing (HandBrake CLI 1.3.0); SchedCP batch (C-cpsmark-4, C-schedcp-2) |
| S9 | c1-gaming.timeline.yaml:10; c2-p2a.timeline.yaml:9, :11; c2-pairs.variant.yaml:25; c3-evening.timeline.yaml:11; c6-dual.timeline.yaml:10; c7.variant.yaml:94 | :20 | PCMark 10 Gaming; Windows Game Mode; LAVD; ananicy/CachyOS Proton vs native (C-pcmark-1, C-gamemode-1, C-lavd-4, C-ananicy-rules-3, C-plain-6) |
| S10 | c2-p2a.timeline.yaml:11 | :21 | Steam "Allow downloads during gameplay"; ananicy download class (C-steam-1..4, C-ananicy-rules-7) |
| S11 | c1-dev.timeline.yaml:10; c1-compile.timeline.yaml:9; c1-indexing.timeline.yaml:16; c1-ml-train.timeline.yaml:12; c2-p1a.timeline.yaml:11, :13; c3-workday.timeline.yaml:14; c6-dual.timeline.yaml:10; c7.variant.yaml:64 | :22 | SYSmark 25; kernel-build characterization (arXiv 1705.05937); interbench Compile; SchedCP make -j; dkms-man, dkms-debian (C-sysmark25-1, C-ocallahan-1, C-interbench-9, C-schedcp-1, C-dkms-*) |
| S12 | c1-ml-train.timeline.yaml:12; c2-p1a.timeline.yaml:13 | :23 | UL Procyon; SchedCP evaluation (C-procyon-1, C-schedcp-3) |
| S13 | c1-media.timeline.yaml:11; c3-evening.timeline.yaml:13; c7.variant.yaml:104 | :24 | PCMark 10 Battery Video; interbench Audio + Video; ananicy audio class nice −11 (C-pcmark-4, C-interbench-1/2, C-ananicy-rules-2) |
| S14 | c1-indexing.timeline.yaml:16 | :25 | ananicy/CachyOS ioclass idle indexer class; GNOME/KDE/plocate shipped defaults (C-ananicy-rules-5, C-plain-3) |
| S15 | c1-backup.timeline.yaml:12; c2-pairs.variant.yaml:35 | :26 | ananicy backup class; SYSmark 30 General Productivity archiving analogue (C-ananicy-rules-7, C-sysmark30-2) |
| S16 | (no `scenario:` tag anywhere; c4.variant.yaml:16 injects `7z` without patching tags) | :27 | SYSmark 30 General Productivity; CpsMark+ WinRAR; SchedCP compression (C-sysmark30-2, C-cpsmark-4, C-schedcp-2) |
| S17 | c2-pairs.variant.yaml:25; c7.variant.yaml:34, :44, :54, :64, :74, :84, :94, :104, :114, :124 | :28 | ananicy AV/scan class; ClamAV scheduled-scan pattern (C-ananicy-rules-7, C-plain-2) |
| S18 | c1-idle.timeline.yaml:8; c7.variant.yaml:124 | :29 | interbench "None/X" baseline (C-interbench-10) |

Catalog coverage note (scenario-catalog.md:33) — "PCMark 10's three groups map to S1–S3, S6–S7, S13; SYSmark 30's four scenarios to S1, S2+S16, S6, S7; SYSmark 25 adds S11; CpsMark+'s four scenarios to S1+S16, S2+S4, S6, S7+S8; Procyon adds S12; Game Mode/LAVD/ananicy add S9–S10, S14–S17." Note that S15 is also mapped to SYSmark 30 in its row (:26) but not in this note.

---

# Part 4 — Counts per source

| source id | entries | of which borderline | status in docs/references.md |
|---|---|---|---|
| interbench | 13 | 1 (13) | verified-in-vetting (2026-08-25); pin commit |
| rt-app | 4 | 1 (4; 2 partly) | verified-in-vetting (2026-08-25); pin commit |
| lavd-ossna24 | 20 | 5 (12, 15, 16, 18, 19) | verified (2026-08-26) |
| corbet-lwn24 | 2 | 1 | verified (2026-08-26) |
| scx | 1 | 1 | verified-in-vetting; re-confirmed 2026-09-12 |
| ocallahan-atc17 | 3 | 0 | verified (2026-08-26) |
| coetzee-arxiv12 | 2 | 0 | verified (2026-08-26) |
| kernel build, plain text | 2 | 2 | (no id) |
| schedcp-mlsys25 (plain "SchedCP") | 5 | 0 | verified (2026-09-12) |
| cpsmark-tbench23 | 13 | 0 | verified (2026-08-25) |
| pcmark10 | 5 | 0 | to-pin |
| sysmark30 | 6 | 0 | verified (2026-09-12) with retrieval caveat |
| sysmark25 | 2 | 1 | to-pin |
| procyon | 3 | 0 | verified (2026-09-12) |
| gamemode-docs | 5 | 0 | verified (2026-09-12); one open question |
| ananicy-rules | 12 | 3 (4, 7, 8) | verified (2026-09-12) at commit 03ef03fb |
| ananicy | 3 | 0 | verified-in-vetting; re-confirmed 2026-09-12 |
| steam-downloads | 6 | 2 (4, 6) | verified (2026-08-26) |
| dkms-man | 3 | 1 (3, partly) | verified (2026-09-10) |
| dkms-debian | 2 | 0 | verified (2026-09-10) |
| dhakal-chi18 | 6 | 0 | verified (2026-08-26) |
| roeser-rw24 | 5 | 0 | verified (2026-08-26) |
| zhang-chb15 | 6 | 1 (5) | verified (2026-08-26) |
| gonzalez-chi04 | 7 | 0 | verified (2026-08-26) |
| mark-chi05 | 3 | 1 (3) | verified (2026-08-26) |
| mark-chi08 | 1 | 0 | verified (2026-08-26) |
| mark-chi14 | 1 | 0 | verified (2026-08-26) |
| czerwinski-chi04 | 1 | 0 | verified (2026-08-26) |
| mark-gallup06 | 1 | 0 | verified (2026-08-26) |
| swell-icmi14 | 1 | 0 | verified-in-vetting (2026-08-25) |
| dubroy-chi10 | 2 | 0 | verified (2026-08-26) |
| chang-chi21 | 3 | 0 | verified (2026-08-26) |
| mozilla-testpilot10 | 5 | 1 (5) | verified (2026-08-26) |
| singervine-slate10 | 1 | 0 | verified (2026-08-26) |
| tab-count literature, shared (C-tabs-1) | 1 | 1 | (dubroy / testpilot / chang) |
| focal-arxiv26 | 5 | 0 | verified (2026-08-26) |
| videogui-arxiv24 | 1 | 0 | provisional |
| schbench | 1 (+1 cross-reference to C-schedcp-4) | 0 | verified-in-vetting (2026-08-25) |
| hackbench | 2 | 0 | verified (2026-09-12) |
| stress-ng | 1 | 0 | verified-in-vetting (2026-08-25) |
| unattributed / plain text (C-plain-1..10) | 10 | 7 (1, 5, 6, 7, 8, 9, 10) | (no id) |
| **total** | **177** (176 distinct + 1 cross-reference) | 29 | |

Part 2(a): 45 numeric rows in archetypes.yaml (39 param-field rows; 6 validation-stat or prose rows: 3, 6, 21, 22, 38, 43). 17 FLAG rows on externally tagged or externally bracketed values — interbench 6 (rows 2, 4, 5, 15, 16, and prose row 22), dhakal-chi18 tag 6 (rows 7–12), lavd-ossna24 5 (rows 30, 31, 35, 36, 37); borderline flags 4 (rows 3, 32, 33, 34); unused-field notes 2 (rows 13, 29).
Part 2(b): 0 numbers in timelines justified by an external (non-meas) citation; 1 number justified by a meas-ci citation (c2-pairs.variant.yaml:16-17).
