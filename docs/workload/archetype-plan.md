# Archetype Library — Writing Plan
> Status: normative · Created 2026-08-25 · Updated 2026-08-27

> Expands §2 of docs/workload/building-plan.md into a buildable specification for `archetypes.yaml`. Normative for Layer 1. Source ids reference `dataset/sources.yaml`; citations live in docs/references.md; execution semantics live in docs/simulator/interpretation-contract.md.

## 1. What an archetype is

An archetype is a **generative model of one process as the scheduler sees it**. To the scheduler a process has no name and no meaning — only an event stream: when it becomes runnable, how long it runs, what it blocks on, whom it wakes, when it forks and exits. An archetype is the rule-plus-parameters bundle that emits that stream.

**Event grammar** (six primitives — semantics normative in interpretation-contract §3; rt-app cited as the schema precedent, including `timer{ref,period}` for TIMER):

```
RUN(duration)      burn CPU
SLEEP(duration)    voluntary relative wait
TIMER(period)      absolute periodic wake at t0+k·period — drift-free; periodic
                   tasks use TIMER, never SLEEP loops
WAIT(channel)      event wait (IO, futex, pipe, upstream task, input)
WAKE(target)       make another task runnable
FORK / EXIT        consume next spawn-table entry / terminate
```

**Defining an archetype is three steps:**
1. **Pattern selection** — transcribe the source's behavioral description into the grammar (interbench's "wakes every 50 ms, needs 5% CPU" becomes a TIMER/RUN loop).
2. **Parameter filling** — the source's numbers enter as *distributions*, not point values. Every numeric carries `source: <id>` or `<id>:<locator>`.
3. **Validation criterion** — an archetype's identity is not its code but the **statistics it must reproduce**: burst-length CDF, wakeup rate, instantaneous runnable count, declared per entry as `validation_stats`. "Correct" means the simulated trace matches the `meas-ci` re-enactment of the corresponding scenario — for the CI-runnable entries. Rescoped limits, stated per entry: `desktop-interactive` has no full behavioral referee (live-usage validation not performed — stated limitation); `game-task-chain` validation against LAVD would be circular (LAVD is also the parameter source) and is stated as such.

**Boundary rules (two sentences):** what the scheduler cannot observe cannot live in an archetype — process *names* (bound in Layer 2/3), *counts* (§3), and *meaning* (segment-label concerns) are excluded by construction. And a `source:` tag justifies the *values and described structure*, never the *field names* — field names are our schema's invention, and every entry whose shape leans on a source records that derivation in `modeling_notes` (§5).

## 2. Two-tier grounding of the inventory

**Tier 1 — existence of each archetype: closed by harvesting.** The inventory was harvested from sources that had already defined their own behavior categories: interbench's interactive and load menus, LAVD's gaming task-chain characterization, the kernel-build literature's compile fork-burst, and **`ananicy-rules`' `type` field — literally a community-maintained archetype taxonomy** (`Heavy_CPU`, `Game`, `Player`, `BG_CPUIO`, …). Each entry carries a `category_source:` naming the taxonomy it was harvested from — machine-checkable by the linter. Three entries (network-bulk, electron-comms, system-daemon) have no literature taxonomy; their `category_source` is honestly `meas` ("behavior class observed in our measurements").

**Tier 2 — sufficiency of the set: closed by verification, not citation.** No universal taxonomy of process behavior exists, so completeness cannot be cited — and must not be claimed. The claim is weaker and falsifiable: **this inventory spans S1–S18.** The referee is the `meas-ci` campaign: if a CI-runnable scenario's measured statistics cannot be reproduced by any composition of the inventory, the inventory is insufficient and an entry is added.

## 3. Multiplicity (counts are numbers too — they obey the reference-only rule)

Counts never appear in the scenario catalog. Two kinds, handled differently:

- **Emergent (dynamic) multiplicity** — cc1 is the exemplar. Its count emerges from the orchestrator's behavior (fork rate, parallelism cap, child lifetime): specify the *orchestrator's* parameters (sourced), and the count time-series falls out of simulation. This preserves churn, which the Q7 material-change test and canonicalization fold need as raw material. Parallelism cap: `-j8` by stated convention, overridable at binding time (OQ-4, resolved).
- **Static multiplicity** — chrome renderers, discord helpers. Binding-time parameters with a source tag: renderer counts from the tab-count literature (`dubroy-chi10`, `mozilla-testpilot10`, `chang-chi21` — defined against the Chromium process model) plus `meas-ci` Xvfb `/proc` counts.

Observation: counts matter differently to the two consumers. The executor needs actual task counts to schedule; the recognizer sees only the post-fold annotation (`chrome (25 procs)`), so order-of-magnitude fidelity suffices for recognition experiments — precision matters only for executor-load realism, which `meas-ci` covers for the CI-runnable entries.

## 4. The inventory (12 entries)

### Periodic-interactive family — harvested from interbench's task menu
1. **`audio-playback`** — TIMER/RUN loop, 50 ms period @ 5% CPU. category_source: interbench; params: `interbench:man-audio`. Consumed by: S13; S9 audio path.
2. **`video-playback`** — TIMER/RUN loop, 16.7 ms period @ 40% CPU. category_source + params: `interbench:man-video`. Consumed by: S13; S3 (stated approximation — see OQ-2, resolved).
3. **`desktop-interactive`** — input-driven variable bursts, 0–100% CPU; input arrives as pre-sampled exogenous wake events. category_source + params: `interbench:man-x` (burst shape); intra-burst input gaps `dhakal-chi18` (mean IKI 238.66 ms) with family shape `roeser-rw24`; burst/pause macro-structure is our modeling (recorded in `modeling_notes`). Consumed by: foreground of S1, S2, S4, S6.

### Compute/batch family — harvested from interbench loads + kernel-build literature
4. **`cpu-batch`** — run-to-completion, sustained core saturation. category_source: interbench (Burn; cross-confirmed by ananicy-rules `Heavy_CPU`). Consumed by: S12 training loop; S7 render phases.
5. **`compiler-child`** — short RUN + disk WAIT, then EXIT. category_source: kernel-build characterization (`ocallahan-atc17`: 2,430 mostly short-lived procs; cross-confirmed by interbench Compile, `coetzee-arxiv12`). Lifetime CDF: `meas-pending`. Consumed by: S11 cc1/ld.
6. **`build-orchestrator`** — FORK/wait loop consuming a pre-sampled spawn table up to the parallelism cap (interpretation-contract §5). category_source: kernel-build literature + make -jN convention. Consumed by: S11 make/cargo. cc1 counts emerge here (§3).

### IO family — harvested from interbench loads + ananicy types
7. **`io-stream`** — streaming sequential read/write, throughput-bound. category_source + params: `interbench:man-write` / `interbench:man-read`; shapes refined by `meas-ci`. Consumed by: S8, S15, S16.
8. **`background-crawler`** — low-priority filesystem walk, ioclass-idle. category_source: `ananicy-rules` (BG_CPUIO/indexer class); rates: `meas-pending`. Consumed by: S14, S17.

### Structural-special family — harvested from LAVD
9. **`game-task-chain`** — waker–waiter chain topology: ~300 tasks, ~90% long-lived; per-schedule RUN 260 µs–1.65 ms (per-task sampling — the source says per-task runtime is stable); 70–75% wakeups from waiting syscalls; 16.7 ms frame budget. category_source + params: `lavd-ossna24`. Consumed by: S9. The only entry whose *topology* is a parameter — expanded by the constructor at load time (interpretation-contract §6). **Lane scaling:** the full task population is instantiated with the long tail near-idle (the source: ~90% long-lived, mostly waiting) and the frame-critical chain's aggregate demand scaled to the lane regime — defended by the source's own concentration statistics (top 30–40 tasks = 95% of scheduling; 15–20 take 60–70%); declared scalable fields + this defense go in `modeling_notes`.

### meas family — category itself sourced from our measurements (no literature taxonomy exists)
10. **`network-bulk`** — link-saturating download, moderate CPU. category_source: meas; params: `meas-pending`. Consumed by: S10.
11. **`electron-comms`** — mostly idle + periodic short wakes; renderer children. category_source: meas; params: `meas-pending` (Xvfb workflow). Consumed by: S5, S4 slack; chrome-renderer reuse refereed by `meas-ci` (OQ-3, resolved).
12. **`system-daemon`** — near-idle, intermittent sub-ms wakes. category_source: meas; params: `meas-pending`. Consumed by: S18.

### Spanning check
S1–S18 all compose from these 12. Creative apps (S6/S7) are time-shared compositions of `desktop-interactive` + `cpu-batch` — consistent with CpsMark+ Table 4's signature (`cpsmark-tbench23:table-4`). The spanning claim is provisional under the Tier-2 protocol: `meas-ci` failures add entries.

## 5. Schema fields (for `archetypes.yaml` + linter)

Per entry: `id`, `category_source` (Tier-1 provenance), `pattern` (grammar program), numeric params (each with `source:`), `sampling` (per-instance | per-task | per-iteration — interpretation-contract §5), `lifetime` (segment-bound | finite | spawned), `spawns`/`spawned_by` (orchestration edges), `scalable` (fields the lane-scaling pass may transform, with rule), `validation_stats` (which CDFs/rates `meas-ci` must match, or the stated reason none exist), and **`modeling_notes`** — prose recording what our encoding invented on top of the sources: field names, structure linearizations, scaling defenses, binding choices. The registry's `notes` records what a source establishes; `modeling_notes` records what we built on it — together they are the paper-writing guardrail against over-claiming.

**Binding notes to record in `modeling_notes` at authoring time (decided):**
- *wineserver → `system-daemon` is a provisional approximation* — LAVD treats wine as part of the game's task graph (`lavd-ossna24:s12`); whether wineserver joins the constructed chain instead is decided at constructor implementation (interpretation-contract §6).
- *P1 binds tracker-miner-fs-3 to `cpu-batch`, not `background-crawler`* — deliberate: P1 models an indexer in full-rescan (CPU-saturating) state so the pair is behaviorally identical; the everyday low-intensity indexer remains `background-crawler` elsewhere (C4/S14). Recorded so the two bindings of one name don't read as an inconsistency.

Linter rules for this layer: reject entries missing `category_source`; reject `meas-pending` params after freeze; reject `source:` ids absent from the registry or locators violating the entry's `locator_pattern`.

## 6. Open questions — resolutions

- **OQ-1 (GPU axis): resolved — no flag.** The simulator is CPU-only and single-lane; no `gpu_bound` field enters the schema. CpsMark+ Table 4's GPU-sensitivity remains a citation about resource mixes, recorded in notes.
- **OQ-2 (video-conference split): resolved — stated approximation.** S3 stays bound to `video-playback`; conferencing's encode + network components are out of measurement reach (no CI path, no literature CDFs), so the binding is recorded as a stated modeling approximation in `modeling_notes`, not given invented parameters.
- **OQ-3 (renderer reuse): referee re-pointed to `meas-ci`.** Do not pre-split; the Xvfb workflow compares chromium-renderer vs Electron-app CDFs and the comparison decides.
- **OQ-4 (parallelism default): resolved — `-j8` by stated convention** (between interbench's documented `-j4` and desktop `nproc` conventions), overridable at binding time; the per-file demand budget governs any given choice.
- **OQ-5 (distribution families): resolved — lognormal by convention**, with the naturalistic-set two-family sensitivity report (building plan §4) covering the assumption.
- **OQ-6 (grammar completeness): resolved — TIMER.** The gap was absolute time, not IO bandwidth: TIMER closes it (drift-free periodic demand). IO bandwidth contention remains out of scope while the executor models CPU only.
