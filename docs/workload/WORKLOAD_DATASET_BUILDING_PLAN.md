# Workload Dataset Building Plan

> Consolidates the dataset methodology decided across Q7 (segments, canonicalization, caches), SOURCE_VETTING_rev2 (per-source verdicts and extracted parameters), SCENARIO_CATALOG (S1–S18, names-only schema, source-column rules), and WORKLOAD_GROUNDING_SOURCES (roles A–D, citation tiers). Those documents are normative for their own content; this plan defines how their pieces compose into the dataset and in what order it gets built.

## 0. Design tension and the two-set resolution

The dataset must satisfy two demands that pull in opposite directions:

- **Control** — the experiments require it. The load-bearing F2 pair must differ in exactly one segment; the familiarity axis must be balanced; every driver-table cell needs coverage; the condition ladder needs files where each recognizer predictably wins or loses.
- **Realism** — the grounding requires it. Segment durations must follow the measured literature; switching structure must match observed shapes; the query-economics numbers must come from something resembling a real session.

One dataset cannot defend both: a fully controlled suite invites "cherry-picked scenarios," a fully sampled suite invites "no hypothesis is actually tested." We therefore build **two sets with distinct roles**, both released as artifacts, both reported in the paper:

| | Core set | Naturalistic set |
|---|---|---|
| construction | authored by hand | sampled from a generation model |
| organizing principle | one file per claim (coverage grid) | distributions from Role C literature |
| carries | all controlled claims (Layer 1 accuracy, F2 pairs, familiarity, distractors, F5 limits, RQ0 gate) | ecological validity; query economics (novel canonical sets/hour, cache hit rate); distractor rates "in the wild" |
| segment durations | compressed event-time (long enough to generate query points; realism not required) | sampled from grounded distributions |
| size | ~23 files, ~50 segments | as many as the generator emits; regeneration is free |

Paper framing: "we validate the claims on a controlled suite, confirm ecological validity and deployment economics on a generated naturalistic suite, and release both."

## 1. Three-layer architecture

Everything composes through three layers. Lower layers never reference higher ones.

```
Layer 1  ARCHETYPE LIBRARY   how one process behaves        (this plan, §2)
Layer 2  SCENARIO CATALOG    which processes co-occur       (SCENARIO_CATALOG.md, S1–S18)
Layer 3  WORKLOAD FILES      how scenarios arrange in time  (this plan, §3–§4)
```

The binding rule: **numeric behavior parameters exist only in Layer 1.** Scenarios reference archetypes by id; workload files reference scenarios and archetypes by id; no file copies a number. Consequences: (a) a literature or Role D update touches one library entry, not dozens of files; (b) the provenance linter (§6) has a single layer to audit; (c) the familiarity ladder (C5) is definable as "same archetype, different name," guaranteeing that recognition differences come from the name alone — the load-bearing control for the familiarity axis.

## 2. Layer 1 — Archetype library (build first)

> **Pin:** this section is superseded in detail by **ARCHETYPE_LIBRARY_PLAN.md**, which is normative for Layer 1 — it adds the formal event grammar (RUN/SLEEP/WAIT/WAKE/FORK-EXIT), the two-tier grounding of the inventory itself (`category_source` harvesting for existence; falsifiable spanning-claim protocol for sufficiency), the emergent-vs-static multiplicity rule, per-entry `category_source` and `validation_stats` schema fields, and open questions OQ-1–OQ-6 (GPU axis, video-conference split, renderer reuse, parallelism default, distribution families, grammar completeness). The table below remains as the quick-reference inventory.

An archetype is a named, sourced behavior specification for one process kind. Format follows the rt-app JSON task model as explicit precedent (run/period/deadline in µs; cite rt-app for the schema shape). Every numeric field carries a `source:` tag (§6).

### 2.1 Initial archetype inventory (~12 entries)

| archetype id | pattern | key parameters (source) | used by scenarios |
|---|---|---|---|
| `audio-playback` | periodic | 50 ms interval, 5% CPU (interbench-audio) | S13, S9 audio path |
| `video-playback` | periodic | 16.7 ms period, 40% CPU (interbench-video) | S13, S3 |
| `desktop-interactive` | variable | 0–100% CPU bursts on input (interbench-X) | S1, S2, S4, S6 foreground |
| `game-task-chain` | waker–waiter chain | per-schedule runtime ~260 µs–1.65 ms; ~300 tasks, ~90% long-lived; 70–75% wakeups from waiting syscalls; 16.7 ms frame budget (lavd-ossna24) | S9 |
| `cpu-batch` | run-to-completion, sustained | full-core burn (interbench-Burn) | S12 train loop, S7 render |
| `compiler-child` | run-to-completion, short-lived | lifetime ~100 ms–s; fork-burst under a parent; 2,430 procs per kernel build (arxiv-1705.05937) | S11 |
| `build-orchestrator` | fork/wait loop | spawns compiler-child bursts (kernel-build-lit) | S11 make/cargo |
| `io-stream` | streaming read/write | RAM-scale sequential IO (interbench-Write/Read) | S8, S15, S16 |
| `background-crawler` | low-priority scan | ioclass-idle IO walk (ananicy indexer class) | S14, S17 |
| `network-bulk` | throughput-bound download | saturating link, moderate CPU (roleD — no literature number) | S10 |
| `electron-comms` | mostly idle + periodic wake | renderer children; light periodic CPU (roleD) | S5, S4 slack |
| `system-daemon` | near-idle | occasional short wakeups (roleD baseline) | S18 |

Entries marked `roleD` ship with placeholder values and are finalized from the measurement campaign (§7); the linter accepts `source: roleD-pending` only until freeze.

### 2.2 Rules

- **Reference-only:** higher layers use archetype ids; the linter rejects inline numerics in Layers 2–3.
- **Name/behavior separation:** an archetype never fixes a process name. The (name, archetype) binding happens in the scenario catalog or the workload file — this is what makes C5's name-swap and C6's name-collision files expressible without touching behavior.
- **Multiplicity is a binding-time parameter:** `cc1 × N` binds compiler-child with a spawn count, not a new archetype.
- **Fewer archetypes than scenarios is expected** (~12 vs 18); sharing is a feature (discord and slack both bind electron-comms).

## 3. Layer 3a — Core set (authored; ~23 files)

Organizing frame: a coverage grid of driver-table cell × familiarity tier × distractor presence. Every file exists to make a specific measurement possible; if a file's absence breaks no RQ, it doesn't belong.

### C1 — Single-situation calibration (~6 files)
One file per mode, one segment each: pure office {soffice.bin, chrome, thunderbird}, pure gaming {steam, game.exe, wineserver, gamescope}, pure compile {code, make, cc1×N}, pure media {mpv, spotify}, pure browsing, idle/[system] only.
Role: recognition floor; executor mapping sanity; and the honest baseline — **this is where the whitelist should score perfectly** (famous names, single situations are its home ground), which we report as part of the condition-ladder narrative.

### C2 — Intent pairs, one-segment diffs (3 pairs = 6 files)
All segments identical except one:
- **P1 (load-bearing):** {code, python3-train} vs {code, tracker-miner-fs-3} — behaviorally identical CPU saturation beside an editor; opposite correct policies (S12 vs S14).
- **P2:** {game + steam download workers} vs {game + clamscan} — same game-plus-background shape; wanted flips (S10 vs S17).
- **P3:** {kdenlive + ffmpeg render} vs {kdenlive + borg} — user-initiated bulk vs scheduled bulk (S7/S8 vs S15).
Per Q7, each pair is a one-segment diff between two otherwise byte-identical files — a tighter control than two independently authored scenarios.

### C3 — Mode-transition arcs (~3 files)
Multi-segment sequences whose boundaries are real label changes (query points that must flip):
- **workday arc** (~4 segments): chrome research → +soffice.bin writing → +make compile → mail send. Ordering grounded in the CpsMark+ CA cooperative workflow (Internet → creation → document processing → email delivery).
- **evening arc:** browsing → gaming (+discord overlay) → media playback.
- **creation arc:** gimp → kdenlive → HandBrakeCLI batch handoff (grounded in CpsMark+ CC and SYSmark 30 ACC's photo↔video multitasking workload).
Role: transition recognition latency and correctness at segment boundaries.

### C4 — Distractor injection (~3 files)
Clones of C1/C3 files with a label-invariant process injected mid-segment: discord launch during gaming; 7z burst during office; chrome open during compile. Paired with their clean originals, giving Q7's within-segment distractor-robustness as a **paired measurement** (same file, injection the only difference).

### C5 — Familiarity ladder (~3 files)
Same structure and archetypes; only the name tier changes:
1. transparent (firefox, blender)
2. semi-opaque (soffice.bin, gamescope)
3. opaque (tracker-miner-fs-3, cc1, baloo_file)
4. nonexistent-compositional (e.g. `video-encoder-pro` — inferable from word semantics)
5. nonexistent-opaque (e.g. `qzvd` — neither recall nor inference possible)
Tiers 4–5 separate **corpus-recall from name-composition inference** — familiarity is defined corpus-relative, not human-relative (soffice.bin is easy for the model, hard for humans; a fresh app is the reverse). The whitelist scores structurally zero on tiers 4–5; that contrast is a headline result. Because all tiers bind identical archetypes, any recognition difference is attributable to the name alone.

### C6 — Resolution-limit files (~2 files, pre-committed misses)
- **name-collision spoof:** a process *named* chrome bound to cpu-batch — the stated limit of name-based recognition (F5). Authored by name collision only; path-mismatch spoofing is out of schema (names-only decision) and noted as future work.
- **fold-internal change:** browser tabs become a video call; the canonical set is unchanged, so no query fires — a guaranteed miss, pre-registered as a scope boundary (Q7 edge case) and shipped as a file so the limit is concrete, not rhetorical.

### Counts and reuse
C1×6 + C2×6 + C3×3 + C4×3 + C5×3 + C6×2 ≈ 23 files, ~50 segments. The groups are orthogonal transforms: C4 = C1/C3 + injection; C5 = C1 with name substitution; C2 pairs share all but one segment. Genuinely novel timeline designs number ~6–7; the rest are scripted derivations — build the derivation scripts, not the files.

### Balance check
Per Q7, §5.5 balance counts **segments, not files**. Before authoring, lay the ~50 segments on the domain × familiarity grid and fill coverage holes; the grid ships in the paper as the dataset-design table.

## 4. Layer 3b — Naturalistic set (generated)

A small generation model, sampled to any size (regeneration is free once built):

- **Segment durations:** heavy-tailed (lognormal or power-law). Means anchored to Gloria Mark: ~3 min per task, ~12 min per working sphere (CHI 2005/2008). Tail shape justified by CNNIC's power-law observations. **Stated honestly in the paper: means from literature; the distribution family is an assumption, validated against Role D.** (Do not use the 23-minute resumption figure without citing it as the 2006 Gallup interview.)
- **Switching structure: hub-and-spoke, not uniform-random.** CNNIC's core finding is that a few hub tasks dominate switching in a star structure. Each generated session draws one hub scenario (editor, browser, or game) and samples excursions to satellite scenarios with returns to the hub. DesktopBench's A→B→A interruption split is the special case of one excursion; the CpsMark+ CA workflow grounds the canonical excursion ordering around an office hub.
- **Distractor injection:** label-invariant processes (S5, S16) injected within segments at rates anchored to Mark's interruption-frequency statistics.
- **Labels:** derived from the generating hub/excursion structure — each sampled segment carries its mode/attributes by construction (the Q7 principle: the author specifies; here the generator is the author).

Role: ecological validity, and the **query-economics numbers** — novel canonical sets per hour and deployment-cache hit rate, measured with the simulator counters from Q7. Controlled claims never rest on this set.

## 5. Build order (and why)

```
(1) archetype library  →  (2) core set  →  (3) RQ0 gate  →  (4a) Role D campaign ∥ (4b) generator  →  (5) naturalistic set  →  (6) full condition matrix
```

1. **Archetype library first** — both sets depend on it; literature-sourced entries can be filled today from SOURCE_VETTING_rev2; roleD-pending entries get placeholders.
2. **Core set second** — hand-authorable in days once Layer 1 exists (~6 novel designs + scripts); does not wait on Role D.
3. **RQ0 gate on core** — random vs oracle gap, measured on C1/C2 where labels are certain. This is the cheapest possible refutation of the whole premise; running it before investing in the generator is the point of the gate. Naturalistic files are unsuitable for the gate (labels derive from the generator being validated).
4. **On gate pass:** Role D measurement campaign (§7) and generator development proceed in parallel; Role D outputs finalize the roleD-pending archetypes and the duration/switching distributions.
5. **Naturalistic set** sampled from the finished generator.
6. **Full matrix** across the condition ladder on both sets.

Rationale for core-before-naturalistic: dependency length (naturalistic waits on Role D + generator; core doesn't), gate economics (RQ0 needs authored labels), and design-learning cost (schema problems surface during hand-authoring, where fixes are cheap; a generator built on a schema that then changes is full rework — while regeneration after the fact is free).

## 6. Provenance manifest and linter

- Every numeric field in the archetype library carries `source: <key>` — a key into SOURCE_VETTING_rev2 (`interbench-video`, `lavd-ossna24`, `arxiv-1705.05937`, `mark-chi2008`, …) or a Role D measurement id (`roleD-m3`).
- Layers 2–3 carry no inline numerics (reference-only rule); the linter enforces both.
- CI fails on: untagged numerics anywhere; inline numerics above Layer 1; `roleD-pending` after freeze; a source key absent from the vetting report.
- Payoff: the paper states, machine-checkably, **"every numeric parameter in the dataset traces to an external source or to our released measurements"** — the terminal defense against "imagined scenarios," and the artifact-evaluation centerpiece. This automates the same principle as the names-only schema decision and the no-circular-sources column rule.

## 7. Role D measurement campaign (one campaign, two purposes)

On the three team desktops, re-enact each Family scenario for real; collect `/proc` snapshots at 1 s (comm, cmdline, pid, ppid, cgroup) plus per-process CPU/IO deltas. Outputs:

1. **Archetype completion:** numbers for the roleD-pending entries (network-bulk, electron-comms, system-daemon; office-app burst timing; S12 training loop — the families SOURCE_VETTING_rev2 flags as numerically thinnest).
2. **Validation:** synthetic-vs-measured CDFs per family (appendix figure); measured canonical-set change rate vs scripted rate.
3. **Name verification:** actual comm strings per distro (soffice.bin vs soffice, updatedb.plocate, cc1 visibility) — SCENARIO_CATALOG Note 4.
4. Raw dumps (paths included — raw data sits outside the names-only schema) released under `validation/`.

## 8. Standing rules inherited by all of the above

- **Names only** in the workload schema; no executable paths (SCENARIO_CATALOG header).
- **No circular grounding:** our own Family/driver-table definitions never appear as sources; internal cross-references (which experiment consumes which file) live in notes, not source columns.
- **Citation tiers:** scholarly (numbered bib) vs deployed-system (footnote, URL + accessed date + pinned version); deployed-system citations support existence claims only (WORKLOAD_GROUNDING_SOURCES).
- **Caches:** record/replay cache on during all measurement (it is the instrument); deployment cache off during Layer 1 measurement, on only in deployment/demo (Q7).
- **Canonicalization is structural-only** (ancestry, cgroup, string identity — never name semantics); it defines query points and the cache key (Q7).

## 9. Open items before schema freeze

1. Ratify Q7 (segment framing, canonicalization rule sentence, two-cache separation) — items 1 and 4 block the freeze.
2. Approve the archetype inventory (§2.1) and the reference-only rule.
3. Fill the coverage grid for the ~50 core segments; sign off holes or add files.
4. Pin the Steam "Allow downloads during gameplay" documentation coordinates (S10 footnote).
5. Decide default browser per file (chrome vs firefox) or vary for familiarity balance.
6. Decide the naturalistic distribution family (lognormal vs power-law) — provisional until Role D fit.
7. Resolve ARCHETYPE_LIBRARY_PLAN.md open questions OQ-1 (GPU axis flag) and OQ-4 (build parallelism default) — these two touch the schema; OQ-2/3/5/6 are deferred to Role D by design and need no pre-freeze decision.
