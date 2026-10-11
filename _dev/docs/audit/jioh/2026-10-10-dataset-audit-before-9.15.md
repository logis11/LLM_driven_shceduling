# Dataset audit round before 9.15 — consolidated

> Status: record · Created 2026-10-10 · Updated 2026-10-11

Five independent auditors on `jioh/dataset-rebuild` at `fe19be86`: A consumer consistency, B provenance, C build reliability, D real-world fidelity, E external review. Items marked "re-verified" were reproduced by the coordinating session independently of the auditor. The per-auditor reports were working files and are not retained; this consolidation is the record.

## Answers to the four questions

| question | answer |
|---|---|
| Is `coreset-single` ready for the RQ0 run? | The dataset side is ready: every artifact, pin, schema check, class field and term resolves, and the set reproduces byte-for-byte on this machine. The run is blocked outside the dataset: the simulator at HEAD refuses five rebuilt files (two judging) and four of the six pre-registered executor conformance items are unimplemented. |
| Does it fit professional research? | Major revision, not reject. Per-value provenance, determinism and pin discipline are above the field's norm. What a reviewer rejects on: the public docs state a different dataset from the data; the C7 counterpart construction is weaker than the "one-diff pair" wording; the gaming archetype's numbers rest on a talk deck the project's own tier rule classes as footnote-only; timeline bound values carry no source field; raw-data availability is not stated. |
| How reliable is the build? | Reproduces exactly here: base set, variants, replay streams, batch tables, pins. Never compiled by CI (main holds the pre-rebuild manifest). Gate holes: `make check` never hashes on-disk `build/`; the variants manifest is drift-checked in no workflow; the manifest pins two of about 75 inputs. |
| How close to real-world usage? | At the individual program: more faithfully measured than any desktop-scheduler workload the repository cites (27 of 28 kinds on the real program, 5–77 repeats, raw traces released). Above the individual program: task mix, co-occurrence, order, durations, core count, display/GPU/audio path and the human are designed, proxied or absent. A pass on RQ0 claims that contended single-core situations composed from real program behaviour exist where the right configuration differs measurably; not how often desktops are in them, how large the benefit is on a multi-core GPU desktop, or how a live user would experience it. |

## Blockers for the RQ0 run (outside the dataset; both re-verified)

1. **Simulator loader refuses five files.** `simulator/src/sim.cpp:874-904` resolves `WAKE.target` against top-level `arrive` ids only. The rebuilt build trees wire each object job's six spawn-table members with WAIT/WAKE in parent–child order (9.6 D19: "each object job is six consecutive spawn-table entries … woken in the job's parent-child order"), so children wake children. Refused: `c1-compile`, `c7-compile` (judging), `c3-workday`, `c4-compile`, `c6-dual` (reporting). Stage-U binary on `c7-compile`: exit 2, "WAKE target 이 최상위 태스크가 아니다: build.j1.mkdir". Counts: `c7-compile` 25,269 child-targeted WAKEs, `c1-compile` 43,620. The schema allows any `task_id` as a target; the contract's prose example shows only top-level targets; the heads-up memo promised the input format unchanged. The usage is new; 경민 was not told. Belongs in the final memo and, given he is actively porting, a heads-up now.
2. **Executor conformance owed.** Gate spec `simulator-conformance` (rq0-gate.yaml:315-334): implemented (c) MLFQ cold start, (f) chain stages in EDF's deadline class; owed (a) zero-wait ready line, (b) TIMER skip rule, (d) `batch_bandwidth_cap` (field never read), (e) strict idle class (`declared_class` never read). 경민's memo of 2026-10-10 confirms (d) and the safety net unimplemented. Three open questions to 인지오 in that memo: TIMER backlog vs frame drop, `fork_cap` semantics, mock-switch Q1–Q3.
3. **Last simulator regression check was on the 24-file pre-rebuild set** (memo_261010.md:75,118,131).

## Dataset defects needing 인지오's decision (class A)

A1. **C7 counterparts' keystroke slices are not the base's first 26.385 s** (re-verified). Compiler: `offset = uniform(seed, iid, "stimulus", j) × (span − window length)`; the counterpart's window is 22.385 s vs the base's 56 s, so the same seed gives a different offset.

| mode | base input wakes in [0, 26.385 s) | counterpart | shared timestamps |
|---|---|---|---|
| browsing | 90 | 29 | 0 |
| office | 112 | 103 | 0 |
| dev | 49 | 78 | 0 |
| mail | 0 | 0 | 0 |

The other six interactive counterparts have no keystroke stream. The 9.10 counterpart decision (D41) states "its base's first C seconds" and is tested for tasks, arrivals and departures only; D44 re-places operations proportionally by design; nothing decided the keystroke slice. Two pinned documents state a wrong mechanism: pair review finding 8 and the scoring spec's `c7-mail` comment ("the counterpart is the base's first 26.385 s and holds no keystroke — c1-mail's 35 fall between 45.9 s and 53.1 s"); the conclusion holds anyway since the base's first 26 s hold none. "The pair comparison is on the same wakes" (pair review finding 10; gate spec input-wake-count line) is true read as the condition comparison on one file, false read as base vs counterpart; the external reviewer read it the second way. No RQ0 confound: headroom is within-file across conditions. The cross-file "one-diff pair" wording (README:89, building-plan §3 C7) overstates: length, window, operation times and keystroke slice all differ.
Options: (i) record as design, correct the two statements, re-pin the scoring spec, amend the gate wording; (ii) add a compiler rule drawing a derived file's stimulus offset from its base's window so the counterpart's keystrokes are literally the base's first C seconds, rebuild the ten counterparts and their variants, re-bless, re-pin, add the test "c7 input wakes ⊂ c1 input wakes in [0, C)". Recommendation: (ii), it realises the recorded decision and makes the pinned sentences true; cost about a compiler rule plus a rebuild and re-pin.

A2. **Timeline bound values carry no source field.** 9.10 D32 decided `source:`/label on every bound value with a lint, "the field and the lint are 9.13's"; `timeline.py` has no source slot; `c2-p2a.timeline.yaml:28` binds `total_work: 727.170s` untagged. The grounding exists only in `_dev/research/jioh/task-9.10-scenarios-timelines/bound-values.md` (12 measured values + labels). `dataset/README.md:130` "every parameter value is sourced" is true of the library only. Adding the field changes timeline blobs, hence `meta.derived_from`, hence artifact hashes → re-bless and re-pin.

A3. **`game-task-chain` paces 8 of 51 files (3 judging: c2-p2a, c2-p2b, c7-gaming) on a talk deck.** `lavd-ossna24` role line: "Talk slides — footnote tier despite carrying numbers"; tier rule (references.md:18-22): footnote tier supports existence claims only. Decided knowingly (9.4 D1, one observation by decision); 9.12 D113 minted a talk type whose numbers are "stated only as its report" but the entry is not yet re-typed; `referee: none`. Options: apply D113 to the entry and state the chain's values as the speaker's reported figures with the chain form as design; or a measured chain (own CI measurement of a native game was considered and not taken, 9.4 D1).

A4. **Build-gate holes (process, not content).** `make check` compares an in-memory manifest to the committed one and never hashes `build/` on disk (compile.py:35-111); `variants.py --check` runs in no workflow and `harness*.yml` run `make variants` in write mode; `build.manifest.json.inputs` pins archetypes and schema only (compile.py:67-73), streams and compiler unpinned (drift detected via artifact hashes, not attributed); CI has never compiled this manifest (dataset.yml on push:main/PR; the only PR closed 2026-10-04 pre-rebuild). Fixes: `variants.py --check` in `check` and `dataset.yml` with a build step; hash `build/` in `check`; pin streams + compiler commit in `inputs`; one CI run on Linux.

## Sound, and verified

| area | evidence |
|---|---|
| Machine consistency (A) | 129/129 artifacts match both manifests; 5 gate pins equal current bytes; 129/129 schema-valid; 863 arrive + 189,484 spawn records all carry `declared_class`, idle in exactly the 7 predicted files; 19 judging / 32 reporting / 78 variants; dataset lint clean; harness suite 279 passed; no live stale names |
| Reproduction here (C) | `make check` 1517 s exit 0 (manifest bytes equal); `variants.py --check` 2098 s exit 0 (78); `replay_fold_in.py --check` 14 s exit 0 (6 streams byte-identical from landings); `batch_fold_in.py --check` exit 0; `build/` 680,806,752 bytes = bless entry |
| Determinism (C) | keyed SHA-256 draws, no global RNG, sorted-key JSON, sorted discovery, loud failures on short/wrong streams; residual risk: libm `pow`/`exp`/`log` before `round()` cross-platform (PLAUSIBLE, closes with one Linux CI run) |
| Library provenance (B) | 29 entries, 28 measured on own campaigns with version, runner, instrument, repeats, stability rule; 6,953 leaf numerics 96.6 % measured; 312 tagged objects 97.4 % `meas-ci`; the 13 + 6 critical findings each resolved against a primary read; session/build entries regenerate byte-for-byte |
| Per-program fidelity (D) | 27 of 28 kinds measured on the real stock Ubuntu 24.04 program; recorded human keystroke timing; declared classes read from source + /proc census |

## Docs-staleness found that is NOT on the 9.15 TODO line (additions)

- `docs/simulator/interpretation-contract.md:31` TIMER "late iterations accumulate as backlog" (skip rule ratified).
- Pre-registration numbers: `research-proposal.md:548` "13 of 25", `terminology.md:229-230` "25 judging, K = 13", `recognition-vocabulary.md:122` and `metrics.md:279` "nine alternative boot defaults" (gate: 19, K 10, ten points).
- `dataset/README.md:77,131` the retired 100–150 % demand window stated as a rule; README:99 omits numpy; README C7 row "unwanted scan"; `measurement-overview.md` §9 release table stops at 9.9 (omits ~14 9.10 releases) and lists retired `file-backup`; campaign-record master table omits 10 of 22 cited campaigns.
- `docs/references.md`: `dhakal-chi18` duplicated (:35, :65) with conflicting roles; `gamemode-docs` "[Exact URLs to pin.]" while verified; `lavd-ossna24`/`cpsmark-tbench23`/`chang-chi21` statuses pre-date the memo; `lavd-ossna24` not re-typed per 9.12 D113.
- `dataset/sources.yaml`: 18 of 23 ids ground nothing; grounding sources of timeline values absent (`glam`, `pytorch-examples`, `handbrake`, `tracker-miners`); `ocallahan-atc17` note still "Linux kernel-build workload" (memo finding A1).
- `dataset/archetypes.yaml:1` header "(v0.1)"; `harness/CHANGELOG.md:7` "25 input terms" (frozen: 24 input + 15 timer).
- `dataset/meas/summary.json` orphaned pre-rebuild analysis (README:18 calls it the campaign summary).
- Data availability: no release URL/asset hash beside values (only replay streams carry release+asset); no LICENSE; SWELL-derived `dataset/stimulus/` is CC-BY-NC-SA; releases made manually (workflows end at upload-artifact).
- Manifest `demand` for a job outliving its file reads offered demand (c2-p1a 14.5 lanes, c2-p2a 9.4; segment 1 at 35.8 and 28.5): a scoping sentence or an in-file clip (2026-09-20 memo §4 asks for it).
- Pair review finding 8 / scoring spec `c7-mail` comment / "same wakes" wording (A1 above).

## Fidelity map (D, compact)

| dimension | rating | gap |
|---|---|---|
| CPU behaviour, 27 measured kinds | PROXY, strong | one pinned vCPU of an EPYC 7763 Azure VM under Xvfb, no GPU/refresh/sound, under perf; measured venue effects 0.72–0.98 tracing, ×1.144 huge pages, Xeon vs EPYC 0.50–0.72×; GPU-less raster threads overcount by an unstated amount |
| game chain | STYLISED → DESIGN | 260/1650 µs slide anchors, lognormal by convention, 16-stage chain ours, 60 Hz from a Steam Deck spec, demand by `lane_share` |
| wake timing structure | STYLISED | rate/gap/run tables within 2 %; order and co-waking lost; measured/compiled dispersion at 1–100 ms: chat 3.3–11×, editor 2.6–3.4×, browser 2.8–3.4×, mail 1.9–3.0×, Steam client 1.9–3.0× (compiled is the smoother one); mitigation: 4-file trace-replay line |
| input stimulus | PROXY, large | SWELL-KW 2012 Windows lab, keys only, 15.6 ms quantised; Word stream drives both LibreOffice and VS Code; no pointer input; none for GIMP/Kdenlive and six other modes |
| task mix per scenario | DESIGN | 9.10 D2: "the core set's task sets are design" |
| co-occurrence / order | DESIGN / UNGROUNDED | no Linux-desktop co-occurrence observation found in four source classes |
| durations | DESIGN | compressed event time; 60 s interactive files; counterparts 26.385 s |
| process population | PROXY (names faithful) | 1–26 tasks per file vs ~300 system-wide; stand-ins (SteamCMD, WebRTC loopback, Element, mpv); X11 under Xvfb; no RT threads |
| hardware / scale | PROXY → DESIGN | one server vCPU measured, one lane simulated; "eight-thread desktop" by convention; only the chain is lane-scaled; venue sweep ×0.8–1.25 narrower than the measured 0.50–0.72× cross-CPU spread |
| scheduling classes | FAITHFUL class / DESIGN rule | read from source + /proc; strict idle = 0 % vs `background.slice` ~23 % on a depicted desktop |

## Recommended order before 9.15 proper

1. Heads-up to 경민 now on the loader refusal (blocker 1) with the counts and the contract reading; answer his three open questions.
2. Decide A1 (recommend the compiler rule + rebuild), A2 (field + lint now or deferred with a stated limitation), A3 (re-type the entry per D113 and state the chain as reported-then-designed).
3. Close A4's gate holes in one small change set; push a CI run that compiles this manifest on Linux.
4. Fold the additions above into the 9.15 line; then run 9.15.
