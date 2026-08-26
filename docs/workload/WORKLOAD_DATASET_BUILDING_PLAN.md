# Workload Dataset Building Plan

> Consolidates the dataset methodology decided across Q7 (segments, canonicalization, caches), SOURCE_VETTING_rev2 (per-source verdicts and extracted parameters), SCENARIO_CATALOG (S1–S18, names-only schema, source-column rules), REFERENCES.md + workload-dataset-sources.yaml (citation index and machine registry), and INTERPRETATION_CONTRACT.md (simulator-facing semantics). Those documents are normative for their own content; this plan defines how their pieces compose into the dataset and in what order it gets built. Decision record: `_dev/archive/2026-08-26-workload-generation-grill.md`.

## 0. Design tension and the two-set resolution

The dataset must satisfy two demands that pull in opposite directions:

- **Control** — the experiments require it. The load-bearing F2 pair must differ in exactly one segment; the familiarity axis must be balanced; every driver-table cell needs coverage; the condition ladder needs files where each recognizer predictably wins or loses.
- **Realism** — the grounding requires it. Segment durations must follow the measured literature; switching structure must match observed shapes; the query-economics numbers must come from something resembling a real session.

One dataset cannot defend both: a fully controlled suite invites "cherry-picked scenarios," a fully sampled suite invites "no hypothesis is actually tested." We therefore build **two sets with distinct roles**:

| | Core set | Naturalistic set |
|---|---|---|
| construction | timelines authored by hand | timelines sampled from a generation model |
| organizing principle | one file per claim (coverage grid) | distributions from Role C literature |
| carries | all controlled claims (Layer 1 accuracy, F2 pairs, familiarity, distractors, F5 limits, RQ0 gate) | ecological validity; query economics (novel canonical sets/hour, cache hit rate); distractor rates "in the wild" |
| segment durations | compressed event-time (long enough to generate query points; realism not required) | sampled from grounded distributions |
| size | ~24 files, ~50 segments | as many as the generator emits; regeneration is free |

Each set compiles in **two modes**, giving **four release artifacts** from one pipeline:

| artifact | demand | role |
|---|---|---|
| `coreset-single`, `generalset-single` | lane-scaled (§5a) | **the evaluated datasets** — every experiment runs on these |
| `coreset-native`, `generalset-native` | as measured on source machines | released for reuse; **not executed in this work** (stated in the release notes) |

Paper framing: "we validate the claims on a controlled suite, confirm ecological validity and deployment economics on a generated naturalistic suite, and release both, each in lane-scaled and native-demand form."

## 1. Three-layer architecture

Everything composes through three layers. Lower layers never reference higher ones.

```
Layer 1  ARCHETYPE LIBRARY   how one process behaves        (archetypes.yaml)
Layer 2  SCENARIO CATALOG    which processes co-occur       (SCENARIO_CATALOG.md, S1–S18)
Layer 3  TIMELINES           how scenarios arrange in time  (*.timeline.yaml, this plan §3–§4)
```

**Two workload formats.** Timelines are the human-facing authoring format (segments + labels + (name, archetype) bindings on a time axis, with `variants:`/`inherit()`/`inject:` sugar), consumed only by the derivation scripts. `make dataset` compiles them into the **canonical format** — the only thing the simulator and harness ever read: `archetypes.yaml + timeline (+ scenario catalog) + seed → workload`. Canonical semantics (event ops, lifetime classes, timing principle) are fixed by INTERPRETATION_CONTRACT.md. Same timeline + same library commit + same seed ⇒ byte-identical canonical file — which is what the controlled-experiment invariants diff (e.g. "P1a and P1b are byte-identical outside seg2's interval"), checked as CI tests on compiled artifacts. The naturalistic generator emits timelines too, so both sets share one compile path, one linter, and one provenance mechanism.

The binding rule: **numeric behavior parameters exist only in Layer 1.** Scenarios reference archetypes by id; timelines reference scenarios and archetypes by id; no file copies a number. Consequences: (a) a literature or measurement update touches one library entry, not dozens of files; (b) the provenance linter (§6) has a single layer to audit; (c) the familiarity ladder (C5) is definable as "same archetype, different name," guaranteeing that recognition differences come from the name alone.

## 2. Layer 1 — Archetype library (build first)

> **Pin:** this section is superseded in detail by **ARCHETYPE_LIBRARY_PLAN.md**, which is normative for Layer 1. The table below remains as the quick-reference inventory.

An archetype is a named, sourced behavior specification for one process kind. Format follows the rt-app JSON task model as explicit precedent. Every numeric field carries a `source:` tag (§6).

### 2.1 Initial archetype inventory (~12 entries)

| archetype id | pattern | key parameters (source) | used by scenarios |
|---|---|---|---|
| `audio-playback` | periodic (TIMER) | 50 ms interval, 5% CPU (`interbench:man-audio`) | S13, S9 audio path |
| `video-playback` | periodic (TIMER) | 16.7 ms period, 40% CPU (`interbench:man-video`) | S13, S3 |
| `desktop-interactive` | input-driven bursts | 0–100% CPU on input (`interbench:man-x`); intra-burst input gaps (`dhakal-chi18`, `roeser-rw24`) | S1, S2, S4, S6 foreground |
| `game-task-chain` | waker–waiter chain | per-schedule runtime ~260 µs–1.65 ms; ~300 tasks, ~90% long-lived; 70–75% wakeups from waiting syscalls; 16.7 ms frame budget (`lavd-ossna24`) | S9 |
| `cpu-batch` | run-to-completion, sustained | full-core burn (`interbench:man-burn`) | S12 train loop, S7 render |
| `compiler-child` | run-to-completion, short-lived | fork-burst under a parent; 2,430 procs per kernel build (`ocallahan-atc17`); lifetime CDF (`meas-pending`) | S11 |
| `build-orchestrator` | fork/wait loop | spawns compiler-child bursts (`ocallahan-atc17`, `coetzee-arxiv12`); cap `-j8` by convention | S11 make/cargo |
| `io-stream` | streaming read/write | RAM-scale sequential IO (`interbench:man-write`, `interbench:man-read`) | S8, S15, S16 |
| `background-crawler` | low-priority scan | ioclass-idle IO walk (`ananicy-rules`) | S14, S17 |
| `network-bulk` | throughput-bound download | saturating link, moderate CPU (`meas-pending`) | S10 |
| `electron-comms` | mostly idle + periodic wake | renderer children; light periodic CPU (`meas-pending`) | S5, S4 slack |
| `system-daemon` | near-idle | occasional short wakeups (`meas-pending`) | S18 |

Entries tagged `meas-pending` ship with placeholder values and are finalized from the CI measurement campaign (§7); the linter accepts `source: meas-pending` only until freeze.

### 2.2 Rules

- **Reference-only:** higher layers use archetype ids; the linter rejects inline numerics in Layers 2–3.
- **Name/behavior separation:** an archetype never fixes a process name. The (name, archetype) binding happens in the scenario catalog or the timeline — this is what makes C5's name-swap and C6's name-collision files expressible without touching behavior.
- **Multiplicity is a binding-time parameter:** `cc1 × N` binds compiler-child with a spawn count, not a new archetype.
- **Fewer archetypes than scenarios is expected** (~12 vs 18); sharing is a feature.

## 3. Layer 3a — Core set (authored timelines; ~24 files)

Organizing frame: a coverage grid of driver-table cell × familiarity tier × distractor presence. Every file exists to make a specific measurement possible; if a file's absence breaks no RQ, it doesn't belong.

**Browser default:** chrome wherever a file needs "a browser"; firefox appears only where the coverage-grid fill wants name variety. Renderer multiplicity is defined against the Chromium process model (`dubroy-chi10`, `mozilla-testpilot10`, `chang-chi21` + `meas-ci` Xvfb counts); firefox bindings reuse it as a stated approximation.

### C1 — Single-situation calibration (~6 files)
One file per mode, one segment each: pure office {soffice.bin, chrome, thunderbird}, pure gaming {steam, game.exe, wineserver, gamescope}, pure compile {code, make, cc1×N}, pure media {mpv, spotify}, pure browsing, idle/[system] only.
Role: recognition floor; executor mapping sanity; and the honest baseline — **this is where the whitelist should score perfectly**, reported as part of the condition-ladder narrative.

### C2 — Intent pairs, one-segment diffs (3 pairs = 6 files)
All segments identical except one:
- **P1 (load-bearing):** {code, python3-train} vs {code, tracker-miner-fs-3} — behaviorally identical CPU saturation beside an editor; opposite correct policies (S12 vs S14).
- **P2:** {game + steam download workers} vs {game + clamscan} — same game-plus-background shape; wanted flips (S10 vs S17).
- **P3:** {kdenlive + ffmpeg render} vs {kdenlive + borg} — user-initiated bulk vs scheduled bulk (S7/S8 vs S15).
Per Q7, each pair is a one-segment diff between two otherwise byte-identical files — a tighter control than two independently authored scenarios.

### C3 — Mode-transition arcs (~3 files)
Multi-segment sequences whose boundaries are real label changes (query points that must flip):
- **workday arc** (~4 segments): chrome research → +soffice.bin writing → +make compile → mail send. Ordering grounded in the CpsMark+ CA cooperative workflow (`cpsmark-tbench23`).
- **evening arc:** browsing → gaming (+discord overlay) → media playback.
- **creation arc:** gimp → kdenlive → HandBrakeCLI batch handoff (grounded in CpsMark+ CC and SYSmark 30 ACC's photo↔video multitasking workload).
Role: transition recognition latency and correctness at segment boundaries.

### C4 — Distractor injection (~3 files)
Clones of C1/C3 files with a label-invariant process injected mid-segment: discord launch during gaming; 7z burst during office; chrome open during compile. Paired with their clean originals, giving Q7's within-segment distractor-robustness as a **paired measurement**.

### C5 — Familiarity ladder (~3 files)
Same structure and archetypes; only the name tier changes:
1. transparent (firefox, blender)
2. semi-opaque (soffice.bin, gamescope)
3. opaque (tracker-miner-fs-3, cc1, baloo_file)
4. nonexistent-compositional (e.g. `video-encoder-pro` — inferable from word semantics)
5. nonexistent-opaque (e.g. `qzvd` — neither recall nor inference possible)
Tiers 4–5 separate **corpus-recall from name-composition inference** — familiarity is defined corpus-relative, not human-relative. The whitelist scores structurally zero on tiers 4–5; that contrast is a headline result. Because all tiers bind identical archetypes, any recognition difference is attributable to the name alone.

### C6 — Resolution-limit files (3 files, pre-committed misses)
- **name-collision spoof:** a process *named* chrome bound to cpu-batch — the stated limit of name-based recognition (F5). Authored by name collision only; path-mismatch spoofing is out of schema (names-only decision) and noted as future work.
- **fold-internal change:** browser tabs become a video call; the canonical set is unchanged, so no query fires — a guaranteed miss, pre-registered as a scope boundary.
- **dual-active ambiguity:** equally-active dual foregrounds (e.g. gaming while actively awaiting a compile) — the point where even the oracle cannot assign a label (§9 of the previous revision, ratified). Shipped as a file so the limit is concrete, not rhetorical.

### Counts and reuse
C1×6 + C2×6 + C3×3 + C4×3 + C5×3 + C6×3 ≈ 24 files, ~50 segments. The groups are orthogonal transforms: C4 = C1/C3 + injection; C5 = C1 with name substitution; C2 pairs share all but one segment. Genuinely novel timeline designs number ~6–7; the rest are scripted derivations — build the derivation scripts, not the files.

### Balance check
Per Q7, §5.5 balance counts **segments, not files**. Before authoring, lay the ~50 segments on the domain × familiarity grid and fill coverage holes; the grid ships in the paper as the dataset-design table.

### Label rule for mixtures
Scenario mixing is the norm; most mixtures resolve to one driver-table cell because the attributes exist to describe them ("game + Steam download" = gaming, wanted=true). Core authors only author mixtures with a defensible label (the Q7 author-specifies principle); genuinely ambiguous dual-active states are the C6 boundary above, never accidental.

## 4. Layer 3b — Naturalistic set (generated timelines)

A small generation model emitting timelines, sampled to any size (regeneration is free once built):

- **Segment durations:** heavy-tailed. Means anchored to the working-sphere literature: ~3 min per task, ~12 min per working sphere (`gonzalez-chi04`; companion ~11 min figure `mark-chi05`; the ~3-min switch rate independently corroborated by `zhang-chb15`). **The distribution family (lognormal vs power-law) is a stated assumption: headline naturalistic-set numbers are reported under both families** — if conclusions hold under either, the assumption is shown not to matter. (The "23 minutes to resume" figure exists only in a 2006 interview, `mark-gallup06` — cite as interview or omit.)
- **Switching structure: hub-and-spoke, not uniform-random.** `zhang-chb15`'s core finding is that a few hub tasks dominate switching. Each generated session draws one hub scenario (editor, browser, or game) and samples excursions to satellite scenarios with returns to the hub. DesktopBench's A→B→A interruption split (`focal-arxiv26`) is the special case of one excursion; the CpsMark+ CA workflow grounds the canonical excursion ordering around an office hub. Optional sanity check: DesktopBench inter-action timings (license permits analysis, not redistribution).
- **Distractor injection:** label-invariant processes (S5, S16) injected within segments at rates anchored to the interruption statistics in `gonzalez-chi04`/`mark-chi05`.
- **Labels:** derived from the generating hub/excursion structure — the hub defines the label; each sampled segment carries its mode/attributes by construction (the generator is the author).

Role: ecological validity, and the **query-economics numbers** — novel canonical sets per hour and deployment-cache hit rate, measured with the simulator counters from Q7. Controlled claims never rest on this set.

## 5. Build order (and why)

```
(0) REFERENCES.md + workload-dataset-sources.yaml      [done]
(1) archetypes.yaml v0.1        meas-pending placeholders allowed; modeling_notes from day one
(2) INTERPRETATION_CONTRACT + canonical JSON Schema    [contract done]
(3) compiler: timeline → canonical                     scaling pass, linter, invariant tests
(4) core timelines                                     ~6 novel designs + derivation scripts → ~24 files × 2 modes
(5) simulator Phase 0 built to the contract            DES core, MLFQ executor, canonical loader
                                                       → first integration test: one C1 workload end-to-end
(6) RQ0 gate                                           v0 driver table, random vs oracle, on coreset-single C1/C2
(∥) meas-ci workflows                                  independent track from (0); results land before freeze
(7) on gate pass: generator → naturalistic set (both distribution families) → full condition matrix
```

Contract-first: compiler (3) and simulator (5) are built to the same written contract (2). Core timelines (4) precede the simulator so authoring stresses the format while fixes are cheap; (4) depends only on (2)+(3). The RQ0 gate needs authored labels, so naturalistic files are unsuitable for it; running the gate before investing in the generator is the point of the gate. meas-ci never blocks the critical path — placeholders carry archetypes v0.1 until freeze.

### 5a. Lane scaling and the demand budget

The simulated machine has one lane (Q1 of the archived open-questions record, ratified — `_dev/archive/2026-08-23-design-meeting-open-questions.md`; INTERPRETATION_CONTRACT §1). Two rules connect the dataset to it:

- **Lane-scaling compile pass:** archetype values whose sources are machine-aggregate (measured on multi-core machines — the gaming chain's utilization and worker concurrency; almost nothing else, since RUN durations are intrinsic CPU demands) are scaled to the lane by a per-archetype declared compile pass — declared fields, declared rule, evidence in `modeling_notes` (`game-task-chain`'s defense: LAVD's own concentration statistics, top 30–40 tasks = 95% of scheduling). Archetype values themselves are never edited. CI invariant: the `-native` and `-single` variants of one timeline differ only in the declared-scalable fields.
- **Demand budget:** every compiled `-single` workload's aggregate demand lands in the measurable oversubscription regime (~100–150% of the lane). The per-file oracle-vs-random admission test (open-questions record Q8) is the enforcement mechanism; a file outside the regime is redesigned, not scaled further.

## 6. Provenance manifest and linter

- Every numeric field in the archetype library carries `source: <id>` or `source: <id>:<locator>` — ids from **workload-dataset-sources.yaml**. The linter validates: the id exists in the registry; when the entry declares `locator_pattern`, the locator matches it.
- The registry is a **subset of REFERENCES.md** (every registry id has a REFERENCES.md entry — CI-checked); citation strings live only in REFERENCES.md.
- Layers 2–3 carry no inline numerics (reference-only rule); the linter enforces both.
- CI fails on: untagged numerics anywhere; inline numerics above Layer 1; `meas-pending` after freeze; an id absent from the registry; a locator violating its pattern; a registry id absent from REFERENCES.md.
- Payoff: the paper states, machine-checkably, **"every numeric parameter in the dataset traces to an external source or to our released measurements."**

## 7. Measurement campaign — meas-ci

One campaign on public CI runners (GitHub Actions): workflow files released, anyone can re-run. Outputs get registry tags `meas-ci:<workflow>:<run>`.

**Workflows:**
1. *Headless CLI measurements:* real `make -jN` build, `tar`/`xz`, `rsync`, `clamscan`, `updatedb` with a sidecar sampling `/proc` at 1 s → lifetime CDFs, fork rates, wakeup patterns. Covers: compiler-child, build-orchestrator, io-stream, background-crawler, network-bulk, system-daemon baselines.
2. *GUI app-intrinsic measurements:* Electron apps / a browser under **Xvfb** — heartbeat periods, renderer-children counts, multiplicities. Open-source substitutes for account-gated apps, substitution stated. Also referees OQ-3 (electron-comms vs chromium renderer CDF comparison).
3. *Name verification:* install packages in distro containers, record actual `comm`/`cmdline` strings (soffice.bin vs soffice, updatedb.plocate, cc1 path) — SCENARIO_CATALOG Note 4.

**Scope discipline (the trust package, mirrored in the registry's `meas-ci` entry):** CI measurements support **structural and shape claims about software behavior only** — fork structure, counts, lifetime shapes, periods, heartbeats, name strings. Machine-relative absolutes (CPU %, IO throughput, io-wait fractions) are recorded with the runner spec and rank as *convention informed by measurement*, never desktop truth. Each workflow runs N times; spread is reported. Framing: characterization of software behavior, never desktop-performance measurement.

**User-behavioral parameters are literature-grounded (Role C), not measured:** input inter-arrival (`dhakal-chi18`, family shape `roeser-rw24`), tab counts (`dubroy-chi10`, `mozilla-testpilot10`, `chang-chi21`), segment durations (§4). **Live-usage validation was not performed and is a stated limitation.** The collection + privacy-scrub tool (a CI-sidecar byproduct) ships in the artifact regardless, as an open falsification invitation: any user can run it against their own machine and check our synthetic distributions. Validation notes: `desktop-interactive`'s validation is rescoped accordingly; gaming validation against LAVD would be circular (LAVD is also the parameter source) and is stated as such.

## 8. Standing rules inherited by all of the above

- **Names only** in the workload schema; no executable paths (SCENARIO_CATALOG header).
- **No circular grounding:** our own Family/driver-table definitions never appear as sources; internal cross-references live in notes, not source columns.
- **Citation tiers** are carried per-entry in REFERENCES.md: scholarly (numbered bib) vs deployed-system (footnote; existence claims only).
- **Caches:** record/replay cache on during all measurement (it is the instrument); deployment cache off during Layer 1 measurement, on only in deployment/demo (Q7).
- **Canonicalization is structural-only** (ancestry, cgroup, string identity — never name semantics); it defines query points and the cache key (Q7).

## 9. Remaining open before schema freeze

1. **Ratify Q7's rule sentences with the team** (canonicalization structural-only rule; segment schema) — flagged in the Phase-1 team memo; the rest of the open-questions record's Q7 lean is adopted by this plan.
2. **Coverage grid fill** for the ~50 core segments (build step 4); sign off holes or add files.
3. **Wineserver's place in the game-task-chain topology** — decided at constructor implementation (INTERPRETATION_CONTRACT §6), recorded in `modeling_notes`.
4. **Submission-time pins** — the `to-pin` entries in REFERENCES.md (benchmark-guide URLs/editions, repo commits, remaining author-list confirmations).
