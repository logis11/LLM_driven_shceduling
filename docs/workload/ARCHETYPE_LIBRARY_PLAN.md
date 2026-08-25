# Archetype Library — Writing Plan

> Expands §2 of WORKLOAD_DATASET_BUILDING_PLAN.md into a buildable specification for `archetypes.yaml`. Normative for Layer 1. Source keys reference SOURCE_VETTING_rev2.md.

## 1. What an archetype is

An archetype is a **generative model of one process as the scheduler sees it**. To the scheduler a process has no name and no meaning — only an event stream: when it becomes runnable, how long it runs, what it blocks on, whom it wakes, when it forks and exits. An archetype is the rule-plus-parameters bundle that emits that stream.

**Event grammar** (five primitives — deliberately isomorphic to rt-app's event model, which we cite as the schema precedent):

```
RUN(duration)      burn CPU
SLEEP(duration)    voluntary wait (timer)
WAIT(channel)      event wait (IO, futex, pipe, upstream task)
WAKE(target)       make another task runnable
FORK(archetype) / EXIT
```

**Defining an archetype is three steps:**
1. **Pattern selection** — transcribe the source's behavioral description into the grammar (interbench's "wakes every 50 ms, needs 5% CPU" becomes a SLEEP/RUN loop).
2. **Parameter filling** — the source's numbers enter as *distributions*, not point values (LAVD itself reports "hundreds of µs average, few ms max" — a distribution statement). Every numeric carries `source: <key>`.
3. **Validation criterion** — an archetype's identity is not its code but the **statistics it must reproduce**: burst-length CDF, wakeup rate, instantaneous runnable count. "Correct" means the simulated trace matches the Role D measurement of the corresponding real scenario (§7 of the building plan; synthetic-vs-measured CDF appendix).

**Boundary rule (one sentence):** what the scheduler cannot observe cannot live in an archetype. Excluded by construction: process *names* (bound in Layer 2/3), *counts* (see §3), and *meaning* (mode/wanted are segment-label concerns).

## 2. Two-tier grounding of the inventory

The provenance requirement applies to the inventory itself, at two distinct tiers:

**Tier 1 — existence of each archetype: closed by harvesting.** The inventory was not invented and then sourced; it was *harvested from* sources that had already defined their own behavior categories. interbench defines the interactive menu (audio, video, X, gaming) and the load menu (Burn, Write/Read, Compile); LAVD defines the gaming task-chain characterization; the kernel-build literature defines the compile fork-burst; **ananicy's rule `type` field is literally a community-maintained archetype taxonomy** (`Heavy_CPU`, `Game`, `Player`, `BG_CPUIO`, …). Each entry therefore carries a `category_source:` field naming the taxonomy it was harvested from — machine-checkable by the linter. Three entries (network-bulk, electron-comms, system-daemon) have no literature taxonomy; their `category_source` is honestly `roleD` ("behavior class observed in our measurements").

**Tier 2 — sufficiency of the set: closed by verification, not citation.** No universal taxonomy of process behavior exists, so completeness cannot be cited — and must not be claimed. The claim is weaker and falsifiable: **this inventory spans S1–S18.** The referee is Role D: if any scenario's measured statistics cannot be reproduced by any composition of the inventory, the inventory is insufficient and an entry is added. (Same logic as the vocabulary's five modes: justified as a sufficient contract, never as a complete classification.)

## 3. Multiplicity (counts are numbers too — they obey the reference-only rule)

Counts never appear in the scenario catalog. Two kinds, handled differently:

- **Emergent (dynamic) multiplicity** — cc1 is the exemplar. Its count is not a static number; it emerges from the orchestrator's behavior (fork rate, parallelism cap, child lifetime). Specify the *orchestrator's* parameters (sourced), and the count time-series falls out of simulation. Bonus: this preserves churn, which the Q7 material-change test and canonicalization fold need as raw material — a hard-coded `cc1 × 16` would erase exactly the phenomenon under test.
- **Static multiplicity** — chrome renderers, discord helpers. Near-structural facts, specified as binding-time parameters with a source tag; the literature has no such numbers (LAVD's ~300 gaming tasks is the exception), so the source is Role D `/proc` snapshots (`source: roleD-mN`).

Observation: counts matter differently to the two consumers. The executor needs actual task counts to schedule; the recognizer sees only the post-fold annotation (`chrome (25 procs)`), so order-of-magnitude fidelity suffices for recognition experiments — precision matters only for executor-load realism, which Role D covers.

## 4. The inventory (12 entries)

### Periodic-interactive family — harvested from interbench's task menu
1. **`audio-playback`** — SLEEP/RUN loop, 50 ms period @ 5% CPU. category_source: interbench-audio; params: interbench-audio. Consumed by: S13; S9 audio path.
2. **`video-playback`** — SLEEP/RUN loop, 16.7 ms period @ 40% CPU. category_source + params: interbench-video. Consumed by: S13; S3 (provisional — see OQ-2).
3. **`desktop-interactive`** — input-driven variable bursts, 0–100% CPU. category_source + params: interbench-X (window-drag emulation). Consumed by: foreground of S1, S2, S4, S6.

### Compute/batch family — harvested from interbench loads + kernel-build literature
4. **`cpu-batch`** — run-to-completion, sustained core saturation. category_source: interbench-Burn (cross-confirmed by ananicy `Heavy_CPU`). Consumed by: S12 training loop; S7 render phases.
5. **`compiler-child`** — short RUN + disk WAIT, then EXIT; lifetime dist ~100 ms–3 s. category_source: kernel-build characterization (arxiv-1705.05937, 2,430 short-lived procs; cross-confirmed by interbench-Compile). Consumed by: S11 cc1/ld.
6. **`build-orchestrator`** — FORK/wait loop dispatching compiler-child up to a parallelism cap. category_source: kernel-build literature + make -jN convention. Consumed by: S11 make/cargo. cc1 counts emerge here (§3).

### IO family — harvested from interbench loads + ananicy types
7. **`io-stream`** — streaming sequential read/write, throughput-bound. category_source + params: interbench-Write/Read. Consumed by: S8, S15, S16.
8. **`background-crawler`** — low-priority filesystem walk, ioclass-idle. category_source: ananicy `BG_CPUIO`/indexer rule class. Consumed by: S14, S17.

### Structural-special family — harvested from LAVD
9. **`game-task-chain`** — waker–waiter chain topology: ~300 tasks, ~90% long-lived; per-schedule RUN 260 µs–1.65 ms; 70–75% wakeups from waiting syscalls; 16.7 ms frame budget. category_source + params: lavd-ossna24. Consumed by: S9. The only entry whose *topology* is itself a parameter.

### Role D family — category itself sourced from our measurements (no literature taxonomy exists)
10. **`network-bulk`** — link-saturating download, moderate CPU. category_source: roleD. Consumed by: S10.
11. **`electron-comms`** — mostly idle + periodic short wakes; renderer children. category_source: roleD. Consumed by: S5, S4 slack; candidate reuse for chrome renderers (OQ-3).
12. **`system-daemon`** — near-idle, intermittent sub-ms wakes. category_source: roleD. Consumed by: S18.

### Spanning check
S1–S18 all compose from these 12. Creative apps (S6/S7) are time-shared compositions of `desktop-interactive` (editing) + `cpu-batch` (filter/render moments) — consistent with CpsMark+ Table 4's signature (CA GPU-insensitive, CC GPU-sensitive). The spanning claim is provisional under the Tier-2 protocol: Role D failures add entries.

## 5. Schema fields (for `archetypes.yaml` + linter)

Per entry: `id`, `category_source` (Tier-1 provenance), `pattern` (grammar program), numeric params (each with `source:`), `lifetime` (segment-bound | finite | spawned), `spawns`/`spawned_by` (orchestration edges), `validation_stats` (which CDFs/rates Role D must match). Linter additions over the building plan: reject entries missing `category_source`; reject `roleD-pending` params after freeze.

## 6. Open questions

- **OQ-1 (GPU axis):** Only S9 has any GPU notion. If the simulator schedules CPU only, no change needed; if CpsMark+ Table 4's GPU-sensitivity is used as a resource-mix input, add a `gpu_bound` flag to the schema. Decide with the executor owners before freeze.
- **OQ-2 (video-conference split):** S3 is provisionally bound to `video-playback`, but conferencing adds encode + network components. Role D measurement decides: if S3's measured CDFs diverge from playback, add a `video-conference` archetype (Tier-2 protocol in action).
- **OQ-3 (renderer reuse):** Does `electron-comms` approximate chrome renderers, or do renderers need their own entry? Do not pre-split; let the Role D CDF comparison decide.
- **OQ-4 (parallelism default):** build-orchestrator's parallelism cap — a desktop-representative value between interbench's "make -j4" and SchedCP's "-j172" (provisionally 8–16, tied to simulated core count). Confirm with Role D or fix by convention and state it.
- **OQ-5 (distribution families):** lognormal is the working default for lifetime/burst distributions; per-archetype family choice is finalized against Role D fits (mirrors the naturalistic-set duration decision, building plan §9.6).
- **OQ-6 (grammar completeness):** the five primitives omit explicit IO bandwidth contention (WAIT(disk) models latency, not throughput competition). Sufficient if the executor models CPU only; revisit if the simulator adds an IO scheduler.
