# 9.23 — Guidebook findings on scoring, the dataset and the gate — changelog

Sub-task 9.23 of Phase 9, on `jioh/dataset-rebuild`. The findings: `_dev/docs/audit/jioh/2026-10-14-guidebook-findings.md` — A1–A8 on scoring and the dataset, B1–B5 on the gate, CI and lint. Decided by 인지오 in the 2026-10-14 grill, one finding at a time, each checked against the tree before its decision. D1–D9 are the decisions on section A, D10 their rebuild.

## D1 — `c6-fold`'s meeting segment is a pre-committed miss (A1, 2026-10-14)

By 인지오's decision. Since 9.10 D30 a `chrome` task on `video-call` arrives at 30 s beside the browser and its four hidden renderers, so the snapshot goes from `chrome ×5` to `chrome ×6`. Telemetry rule 1 (`docs/data-contracts.md` §5, frozen 2026-09-06) makes a count-only change a set change, so a query fires at 30 s; D30's "the canonical set does not change at the boundary" did not hold under it. Nothing in the 30 s snapshot says call — a sixth `chrome` is also what a new tab shows — so the meeting label cannot be reached from the names: the definition of `pre_committed_miss` (`docs/recognition-vocabulary.md` §1). The meeting segment (30–60 s) carries `pre_committed_miss: true`; the browsing segment keeps its graded 0 s point.

Finding corrected: the exclusion list is the RQ0 gate spec's `layer1_exclusions` (`harness/experiments/rq0-gate.yaml`), derived from the annotation and checked by the evaluator — not the scoring spec's.

Applied: `dataset/timelines/coreset/c6.variant.yaml` (the annotation; the recipe's comment restated); `c6-fold` re-derived and recompiled (D10); in `dataset/tools/tests/test_coreset.py` the comment of `test_c6_fold_names_unchanged` restated and `test_c6_limits_are_pre_committed_misses` added; the gate spec's `layer1_exclusions` and its comment; `harness/tools/tests/test_mock_daemon.py`'s graded-point counts, with D2's: 77 graded points over 50 files, nine in pre-committed-miss segments (seven before), 68 headline points over 44 files (70 before).

Hands to 9.15: `docs/workload/building-plan.md` §3 C6's fold sentence (`:120`; also handed by 9.10 D30) and every doc that says no query fires in `c6-fold` — a query fires at 30 s on the count change, the names do not say call, and the segment is a pre-committed miss.

## D2 — `c6-spoof` split at the spoof's arrival: `false` and a pre-committed miss from 20 s (A2, 2026-10-14)

By 인지오's decision. The file's one segment was browsing with `background_wanted: true` and `spoof: true`, the `true` inherited from `c1-browsing` with no recorded reason. `background_wanted` is whether the sustained background work is something the user asked for, `true` by convention only when none runs (`docs/recognition-vocabulary.md` §1). Before 20 s nothing unwanted runs; from 20 s the spoof is sustained CPU work nobody asked for, and the snapshot shows one more `chrome` and nothing else. The segments: 0–20 s browsing, `background_wanted: true`; 20–60 s browsing, `background_wanted: false`, `spoof: true`, `pre_committed_miss: true`; scenario `[S2]` on both.

Consequences: the oracle reads browsing/`false` from 20 s and applies that row (cap 0.05) to the miner; the coverage grid's browsing/`false` cell gains the segment, marked recognition-limited; `c6-spoof` joins `layer1_exclusions`. The driver table's browsing/`true` justification (`daemon/driver-table/prior.yaml:58`, the miner held to half the lane) describes the row a name-based recognizer applies to the spoof and stays.

Applied: `c6.variant.yaml` (`set-segments` in place of the `patch-segment`; the comment restated); D1's test; the gate spec as in D1.

Hands to 9.15: `docs/workload/building-plan.md` §3 C6 (`:103`, `:118`) and `docs/workload/coreset-guide.md`'s C6 narrative — the spoof's segment `false` and a pre-committed miss from its arrival; `docs/daemon/prior-table-pair-review.md:19` — the oracle reads browsing/`true` to 20 s and browsing/`false` from it.

## D3 — the generated layer's batch terms keep turnaround; a row under which the job does not finish scores censored (A3, 2026-10-14)

By 인지오's decision. Checked 2026-10-14, the reference simulator (`simulator/src/sim.cpp`, a scratch build) run under the boot default with no schedule: the generated-layer rule (9.21 spec decision 1) derives 1,350 `turnaround` terms in 898 of the 1,562 files; of the 1,062 jobs the simulator could run, 191 end after their file — 114 normal-class (ml-train 92, transcode 21, render 1) and 77 idle-class (indexing 56, backup 21), in every set but flap-stress; the 212 jobs in files holding a compile were not run (the simulator refuses their spawned children's wakes, 9.6 D19). `dataset/tools/end_bound.py` refuses 912 of the 1,350 jobs (an op beside the job it cannot time), stops on 78 (a WAIT with no wake left) and, for the compile build, counts the orchestrator's own runs alone. For all 1,350, arrival + own CPU + own blocked time fits inside the file: no job is sure to outlive its file under every row. The job's size is bound to the span it must be alive in, from C1's rate (9.19 spec decision 1), beside company its C1 file did not have, so it may finish under some rows and not others — a case the scoring spec's rule for the core set ("a job that finishes under every row scores its turnaround, one that cannot finish inside its file scores its delivered CPU") does not meet, each C1 file being sized so its job finishes under every policy (9.10 D78).

The batch term stays the C1 entry's turnaround. A row under which the job does not finish scores the censored bound, the file's end less the arrival, worse than every finishing value (`docs/harness/metrics.md` §9); two such rows tie. The idle-class placements (indexing, backup; 437 terms) end at the same time under every row and are expected to show no headroom. Whether RQ4 needs the size of the lag on jobs that do not finish is the RQ4 experiment spec's question.

Finding corrected: 9.14 decision 6 moved `c2-p3a`'s render term from progress to turnaround; the rule the finding meant is the scoring spec header's sentence citing it. The jobs past the end are far more than the three named.

Applied: `harness/scoring/scoring-spec.yaml`, header text only — the middle case and the expected no-headroom placements (D10).

Hands to 9.15: `docs/harness/harness-and-records-guide.md` where it states the generated layer's scoring rule (9.21's rows) — the middle case as the header states it.

## D4 — in the generated layer an arrival is a program start (A4, 2026-10-14)

By 인지오's decision: the generated layer exists to answer the research questions, not to make a claim. 9.10 D136 stands as the layer's behaviour: a task arriving mid-file replays one measured launch repeat from its arrival, its steady stream beginning when the phase ends. Every form has tasks arriving mid-file — B at the boundary (9.19 spec decision 3), the returning A, each flap alternation, each distractor arrival: 300 of the transition grid's 480 files (630 task instances), 630 of the return grid's 720 (1,890), all 24 flap-stress files (160), 166 of the distractor grid's 272 (331), none of the familiarity ladder's. Most launch phases outlast a 60 s segment — mail 409 s, browser 421 s, video editor 241 s, call 210 s, game client 906 s, hidden renderer 1,051 s; office writer, chat client and the two players 31–54 s — so those segments depict applications launching, and the C1 files stay the steady-state material. CPU in the first 60 s of the launch against steady C1 use per 60 s: mail 2.8–3.0 s against 0.08 s, browser 1.6–1.95 s against 0.18 s, the call 47.8–48.2 s against 14.3 s, binned into its cycles (9.10 D138).

Finding corrected: recognition (RQ1) is untouched — telemetry is a pure function of the pinned events, and Layer 1 runs no simulator. The replay reaches Layer 2: the terms of B and of the returning A, the per-switch excess and the `flip_cost` line.

Applied: nothing in the data.

Hands to 9.15: `dataset/README.md` (`:114–117`) and `docs/workload/building-plan.md`'s generated sets (`:142–147`) — an arrival in the generated layer is a program start replaying its measured launch (9.10 D136); the segments where tasks arrive depict applications launching, the C1 files the steady state.

## D5 — the return and flap sets keep their form: each boundary a close and a relaunch (A4, 2026-10-14)

By 인지오's decision. The return grid and the flap-stress set depart every task set at its boundary (9.19; `docs/workload/building-plan.md:143`, "A departing at each boundary"), so under D4 each boundary closes one mode's programs and launches the other's. Every boundary is a set change under both telemetry shapes, as the hold-time plan's flap-stress file is defined ("a generated workload whose process set changes several times at short intervals"). The launch load is the same under every condition: it sets the size of a stale configuration's cost, not its direction. A window-switch regime — A staying, the focus returning — is a question for the RQ4 experiment spec.

Applied: nothing in the data.

Hands to 9.15: the dataset docs' return grid and flap-stress set (`dataset/README.md`, `docs/workload/building-plan.md:143–144`) — each boundary closes one mode's programs and launches the other's.

## D6 — the twins are a recognition pair; their seeds stay (A5, 2026-10-14)

By 인지오's decision. The 240 pairs `dx-<A>-with-<B>` and `tr-<A>-to-<B>-focus` have identical task lists and different seeds (`dataset/tools/gen/cells.py`, SHA-256 over `seed|<set>|<cell id>`). Names-only telemetry is identical in all 240, focus telemetry in the 26 whose focus holders share a name. The workloads differ: per-task programs in 1,528 of 1,590 tasks, file demand by a median of 17 %. A shared seed would not align them — the keystroke offset is drawn over windows of different length — and their scoring terms differ by design (9.21 spec decision 2). No experiment spec or scoring rule pairs the twins; the focus field's Layer-2 worth is measured by running both telemetry shapes on the same files (9.17 spec decision 5).

Applied: nothing in the data.

Hands to 9.15: "differ in the focus alone" (`dataset/README.md:114`, `:117`; `docs/workload/building-plan.md:142`, `:147`) restated — the twins share the task set and the name sequence and differ in the focus, the input, the labels and the random draws; a recognition pair.

## D7 — two records corrected (A6, A7, 2026-10-14)

By 인지오's decision: a correction lives in this record, with a one-line forward note at the decision it corrects.

- **9.18 D6's base keystroke counts.** For indexing, compile and ml-train D6 gives the whole base file's distinct keystroke times, 46, 2,354 and 1,844; over the counterpart's span they are 28, 358 and 1,629. Browsing, office, dev and mail match the span. The subset relation holds either way, and the six artifacts are unchanged since D6 (their manifest hashes identical at `71a57a23` and `27340c3d`). Forward note at 9.18 D6.
- **`c6-dual`'s utilization.** 9.13 R5's 1.00 is 0.9997 rounded and was right when read. It became 0.8388 at the 9.17 re-bless: 9.17 D1 cut the editor's typing into nine windows of 686–688 s following its focus turns, in place of one of 12,068 s. Recompiled before and after `39d8d815`, the editor's CPU goes 3,460.4 s → 1,518.6 s and its input wakes 33,518 → 13,751, the build and the game chain unchanged — 0.161 lanes, the whole drop. No consumer reads the value: the demand window is no gate (9.14 decision 4), `c6-dual` reports, and its guard exemption rests on its label. Forward note at 9.17 D1.

Applied: the two forward notes.

Hands to 9.15: the guidebook's open notes on these closed — vol-03 `:1642` with its table (about `:1630`, which counts events, not distinct times), vol-04 `:1670`, vol-03 `:1879`.

## D8 — the code editor's validation scope restated: `c6-dual` held the editor focused for 12,068 s before 9.17 (A7, 2026-10-14)

By 인지오's decision. The `code-editor` entry's scope (`dataset/archetypes.yaml`, written by `dataset/tools/meas/campaign/fold_in.py`) read "Read over 12,068 s, the span `c6-dual` holds it focused, in two long-phase probes …"; since 9.17 the editor's longest focused stretch in `c6-dual` is 686–688 s. Restated: "the span `c6-dual` held it focused before its focus alternated with the game every 688 s (9.17 D1)"; the probes' length and readings unchanged. The library's bytes change, and with them every artifact's; rebuilt with D1 and D2 (D10).

Applied: `fold_in.py`, `dataset/archetypes.yaml`.

Hands to 9.15: the guidebook's copies of the clause — vol-02 `:815`, vol-04 `:1552`, vol-06 `:1038`; the final memo's file-size row (D10's sizes; the "190 MB … 681 MB" are 9.13's).

## D9 — P1 stays the load-bearing pair, stated as it stands (A8, 2026-10-14)

By 인지오's decision. 9.12 D14 defined what the pair tests — "whether recognition improves on a baseline that already honours the indexer's declared class … the RQ0 gate then measures that headroom as it is" — and 9.14 decision 2 measured that headroom as zero: the executor's strict idle rule places the idle-class indexer below every row, so `c2-p1b` reports and `c2-p1a` judges. The pair carries the recognition claim — the model must tell the wanted training run from the unwanted indexer, which a whitelist cannot — and its scheduling headroom on `c2-p1a`'s side; the indexer's declared class settles its own side. The C2 wording is already decided and handed by 9.10 D6 and 9.12 D14, D15 and D88.

Finding corrected: `docs/research-claims.md` says "behaviour is identical", not "behaviourally identical". The 2026-10-10 audit's "the P1 pair the RQ0 load-bearing one" (`:127`) is a record and stays.

Applied: the forward note at 9.12 D14.

Hands to 9.15: where P1 is called load-bearing — `docs/research-claims.md:205–220`, `docs/workload/building-plan.md:91`, `docs/workload/coreset-guide.md:601` — RQ0 judges `c2-p1a` and reports `c2-p1b` (9.14 decision 2), the indexer's declared idle class settling its side.

## D10 — the rebuild, re-bless and re-pin for D1, D2, D3 and D8 (2026-10-14)

One local build, `make -C dataset dataset variants generated` (`python3.12`, M1 Pro): 4 min 54 s wall — the core set's 51 artifacts, the 78 variants, the five generated sets' 1,562.

- **What moved.** The library's bytes changed (D8), so every artifact's did through its library hash. `beyond_hash.py`: 2 of the core set's 51 change beyond it, `c6-fold` and `c6-spoof`; one demand moves, `c6-spoof`'s, now per segment — 0.0164 to 20 s, 0.7664 after, 0.5164 over the file as before. The 1,562 generated artifacts differ from HEAD's in the library hash alone (hashed with it swapped back). The 78 variants carry their own transformed library's hash, so the swap does not apply: HEAD's variants rebuilt in a scratch worktree (2 min 37 s) and compared, all 78 differ in `meta` alone.
- **The coverage grid.** browsing/`false` gains `c6-spoof`'s second segment, meeting/`true` `c6-fold`'s; each cell carries one pre-committed miss; 67 segments (66 before). `test_grid.py`'s pre-committed-miss cells gain the two.
- **Pins.** Dataset manifest `c5f7fa5a59f34bc88f8bb22acd6ec58b0e1ade91b806166a7bbb49c38b0bc23a`, variants manifest `8986b58a2de1f1b1f2d621917f224f0d8218b3cb56fc82e5900b115ff0a60b99`, scoring spec `2ad757b6196ae1839a76b4f1b2a96d156eee84b40375dec9bd5f66116b6ca14e` — the three the RQ0 gate spec carries. Generated: transition grid `3035cfe3649275c803eab712a727d1dd9e9f3dc1c3f5b8958cc027fc899c0f30`, return grid `2e381b42a3e70e3c5c0fc5a2576c5de487a6cda50b8677a379ea9351c04b3c55`, flap-stress `90cc782aad6d0b8984676000d90f81d6873b114305edbb1b6cadd7e3fd5df0c8`, distractor grid `e61fd777bb8fae30d60fcb1ac99850b68f9d6324538b1ec6fd0aaec5992bd203`, familiarity ladder `1a7d35d7a934a396902bd850e757832bce4e391c4448f60f6150b234acd6c317`. `harness/CHANGELOG.md` entry of 2026-10-14.
- **Sizes.** `c6-dual` 187,601,756 B, the core set 678,168,083 B over 51 files — 9.18 D7's.
- **Checks.** `make -C dataset lint` clean; `derive.py --check --require-coverage` clean; `make -C dataset test` 528 passed, 1 skipped (2 min 10 s; the first run failed `test_coreset_instances_all_32_cells` alone, on the two new pre-committed-miss cells); `make -C harness lint` clean — the experiment lint's derived `layer1_exclusions` among it; `make -C harness test` 296 passed, 2 deselected (17 min 03 s); the coreset-wide `test_oracle_over_the_coreset_reproduces_the_measured_graded_set` passed on its restated counts — 147 query points, 51 terminal, 19 ambiguous; 77 graded over 50 files, nine in pre-committed-miss segments; 68 headline over 44 files. `check_build.py` before the commit: `build/` equal to the union of the seven manifests, the seven manifests differing from their committed bytes — the re-bless.

## D11 — the launch streams pinned in the manifests' inputs (B1, 2026-10-15)

By 인지오's decision. The compiler reads the ten launch streams `dataset/launch/launch-<entry>.json.gz` for every task the file starts after 0 s (`wlc/compiler.py`'s `_load_launch`; 9.10 D136, and D4 above for the generated layer), and `compile.py`'s `input_files` — the files 9.18 spec decision 5 pins by content — named the library, the schema, the compiler's sources, the stimulus and the replay streams, not them: the core manifest's 23 inputs and the generated manifests' 45 held none, and a changed launch stream passed `make check`.

Applied: `input_files` adds `launch/*.json.gz` — the core manifest's inputs 33, the generated manifests' 55; the variants manifest pins the core manifest's bytes. `test_manifest.py`: the pinned set holds a launch stream; `test_every_stream_directory_the_tools_open_is_pinned` reads every `<dir>/<name><ext>` stream path the compiler and the linter open (`stimulus/*.jsonl`, `launch/*.json.gz`, `replay/*.json.gz`) and requires every such file pinned.

Hands to 9.15: guidebook vol-07's input counts and its open note on the launch streams (`:203`, `:221`, `:259`, `:295`, `:394`, `:451`).

## D12 — `check` compares every file the build rewrites with its committed bytes (B2, 2026-10-15)

By 인지오's decision. `make dataset` runs `derive.py`, which rewrites the derived timelines and `coverage-grid.json`; `make check`'s `derive.py --check` then compared them with a fresh derive of the same recipes, and `check_build.py` compared the manifests alone with their committed bytes (9.22 spec decision 1). A derived timeline regenerated and left uncommitted passed CI, its artifact's `derived_from` naming a blob not in git — read in the code, not run.

Applied: `check_build.py`'s `rewritten` names every derived timeline a variant spec names (`<id>.timeline.yaml` beside the spec, as the deriver writes it) and `coverage-grid.json`; `check_committed` holds them to their committed bytes as it holds the manifests. `test_check_build.py`: a derived timeline rewritten and the grid removed in a committed scratch repository are each named. The dataset README's `make check` and `check_build.py` lines restated.

Hands to 9.15: guidebook vol-07's `make check` (its chapter 4 and the gate's figure).

## D13 — `make lint` runs the freeze lint (B3, 2026-10-15)

By 인지오's decision. `lint.py` rejects a `meas-pending` tag under `--freeze` alone (`wlc/linter.py`, "meas-pending after freeze"); `make lint` ran it without, and the rule was held by `test_lint.py::test_repo_is_freeze_clean`, which runs after the build in CI — while the dataset README said "the linter keeps it that way".

Applied: `make lint` runs `lint.py --freeze`; the test stays. Clean: no `meas-pending` tag in the library (one comment names it, `archetypes.yaml:38`). The README's `make lint` and `lint.py` lines name it.

Hands to 9.15: guidebook vol-07 `:951` and its rule-7 passage (§8.8).

## D14 — three canonical lints (B4, 2026-10-15)

By 인지오's decision. `lint_canonical` checked a top-level program's WAKE targets and no spawn-table entry's; checked no name's length, the ladder's renamed names alone being held to the comm limit (`gen/cells.py`, 9.20); and checked no program's end, while the workload schema's `program` description says "A task whose program runs out without EXIT and without a pinned depart is a linter error."

Applied, in `wlc/linter.py`: a spawned child's WAKE targets resolve as a top-level task's; every name, top-level and spawned, within 15 characters — `TASK_COMM_LEN` 16 less the terminator (`linux-sched-h`); every program ends as its lifetime requires — D16's rule, which holds the schema's sentence and the segment-bound side too. The schema is unchanged. Tests in `test_canonical.py`: a spawned child's WAKE to an unknown task, a 16-character name on a task and on a child (15 passes), a segment-bound program without its trailing step and a spawned one without EXIT, each named.

Before the rule was written, the 1,691 artifacts (51 core, 78 variants, 1,562 generated) held none of the three faults: 855,150 WAKEs in spawned programs, all resolving; no name past 15 characters; 1,569 finite top-level tasks and 341,422 spawned children, each ending with EXIT.

Hands to 9.15: guidebook vol-07's list of what the lints check.

## D15 — exact requirements; the smoke on demand (B5, 2026-10-15)

By 인지오's decision. **Requirements.** `dataset/tools/requirements.txt` and `harness/tools/requirements.txt` set minimum versions, and the runner installed the day's newest: on harness CI run 38547043521 numpy 2.5.4, pandas 3.0.6, pytest 9.1.1, jsonschema-rs 0.58.6, jsonschema 4.26.0, PyYAML 6.0.3, against the home machine's 1.26.4, 2.2.2, 8.3.4, 0.29.1, 4.23.0, 6.0.1 — the versions every blessed manifest and recorded home result was made with. Dataset CI run 38387283407 failed on pytest 9.1.1 where 8.3.4 passed (9.21's `coverage` import, fixed in `c879f96d`). Both files now pin the six direct dependencies exactly at the home versions; their own dependencies stay unpinned. The dataset README's requirements line restated.

**Smoke.** `harness-smoke.yml` ran on every push to `main`, on demand, and on pull requests touching `harness/`, `dataset/` or the driver table, its comment "about eight minutes" — the 8.6 figure on the old files. Over the rebuilt set it took 4 h 50 min at home (9.14 D14), `c6-dual`'s four runs about three hours of it; it has not run on a runner since the rebuild (the last, run 38051784588 on `main`, 2026-10-10), where the job limit is 6 h and the two coreset-wide mock tests were killed at `c6-dual` (9.21). It now runs on demand alone, the comment restated; `test_runner.py` in `harness.yml`'s `make test` runs the smoke path over one to three files on every push. The harness README's smoke lines restated.

Hands to 9.15: guidebook vol-07's workflow table and §6.4 (`:1065`, `:1119`), its open note on the comment (`:1215`), its requirements passage (`:1101`). Hands to 9.16: the full smoke at home on the final build.

## D16 — no program runs out (found in B4, 2026-10-15)

By 인지오's decision. 7,400 segment-bound programs ended before their pinned depart with nothing left to execute — 240 over the core set and the variants (every one of the 129 files), 7,160 over the generated layer — in three shapes: 6,215 driven by wake events, `[WAIT, RUN] × N` with N the wakes sent to the task in every case; 745 driven by a frame timer, `[TIMER, RUN] × N` over the ticks before the depart, the next tick at or past it in every case; 440 resident with nothing to do, a single never-woken WAIT. The silent stretch from the last wake to the depart is one gap of the program's own stream (median 0.3 s), long only where the stream is sparse — the idle daemons at 0.03–0.1 wakes/s — or where the user left the program (`gimp` in the transition grid's `focus` form, up to 63 s). The file stated what the process did until its depart for the resident 440 alone; the interpretation contract (§5: the segment-bound task ends when the user closes it) and the harness's mock simulator (it ends the task at its depart) read the others as blocked, the simulator (`simulator/src/sim.cpp:662`, 2026-10-10) as exited, with a second `task_end` at the depart (`on_depart`, `:838`).

Applied, in `wlc/compiler.py`: a program completes with the blocking step its loop takes next — a wake-driven program a WAIT on its last wake's channel (an interactive task's on its input), so N wakes meet N + 1 WAITs; a timer-driven program the next TIMER, whose tick falls at or past the depart, each TIMER returning no earlier than its own tick; the resident unchanged. The rule `lint_canonical` holds (D14): a task without a pinned depart, top-level or spawned, ends with EXIT; a segment-bound task with WAIT, TIMER or an unbounded LOOP. Nothing new executes: the CPU, the wakes and the ticks inside the span are unchanged, every artifact's bytes change. The harness reads a wake's WAIT by its order and a job by a tick consumed inside the span, so neither meets the trailing step. Tests: `test_no_program_runs_out` over the three fixtures; `test_input_wakes_inside_windows` counts the editor's WAITs as its wakes plus one.

Hands to 9.15: the simulator guide's worked run (§4½) — the editor's program gains its trailing WAIT, so its "next instruction WAIT → blocks" holds; the interpretation contract's §5 — a segment-bound program ends blocked, and the depart removes it; the final memo to 인경민 and 박이안 names the rule.

## D17 — the rebuild, re-bless and re-pin for D11–D16 (2026-10-15)

One local build, `make -C dataset dataset variants generated` (`python3.12`, M1 Pro): 4 min 56 s wall — the core set's 51 artifacts, the 78 variants, the five generated sets' 1,562, the canonical lints with D14's three inside the compile on every one.

- **What moved.** Every artifact, through D16 alone: each of the 1,691 with its segment-bound programs' trailing step removed hashes to HEAD's manifest entry — 6,215 trailing WAITs and 745 trailing TIMERs, the 440 single-WAIT and 5,559 unbounded-LOOP programs unchanged; the 1,613 compile reports byte-identical, so no demand moves. The derived timelines and `coverage-grid.json` unchanged. The core manifest's inputs 33 and the generated manifests' 55 (D11).
- **Pins.** Dataset manifest `81d3213d0443283a0eb456e19dee2b4216305db4e0c134f18ddd66ca74031ae0`, variants manifest `7079e677bab864d21ef4a674079ac9ec2fa9758ba3a53a87879f77542cb282d9` — the RQ0 gate spec carries them; the scoring spec at D10's `2ad757b6…`. Generated: transition grid `826c719c61715de2f5454cb88d563e3f589edfadbc627ac8ce08bbf725440e28`, return grid `392d60717e0b936377603da04e212fffadfc3a724d806985131a0a2429da5b2e`, flap-stress `97ba813f6785d759f57a4b06f469a9964ef3b18ef487678730f682e9c4ca78e6`, distractor grid `919bb2c02efd71e70a9122763b0073331cc3fa4c5c6314eff9b105c2ab6879f9`, familiarity ladder `b6f82df5977ae4ac258851f0505a3665fd7ebe0769ecad7c855f89c9a4d5ca01`. `harness/CHANGELOG.md` entry of 2026-10-15.
- **Sizes.** `c6-dual` 187,601,795 B, the core set 678,172,716 B over 51 files (39 B and 4,633 B over D10's).
- **Checks.** `make -C dataset lint` (now `--freeze`) clean; `derive.py --check --require-coverage` clean; `make -C dataset test` 534 passed, 1 skipped (2 min 11 s; the first run failed 12 tests that counted a program's WAITs or TIMERs or built a hand-made artifact without its trailing step, each restated to the rule, and the stream test's pattern, which had matched `variants.py`'s timeline path, narrowed to the stream directories); `make -C harness lint` clean; `make -C harness test-full` 298 passed (29 min 00 s), the two coreset-wide tests among them — the oracle's graded set unchanged at 77 points over 50 files, 68 headline over 44. `check_build.py` before the commit: `build/` equal to the union of the seven manifests, the derived timelines and the grid equal to their committed bytes, the seven manifests differing from theirs — the re-bless.

## D18 — the two workflows on a runner (2026-10-15)

`jioh/dataset-rebuild` at `d5cc7711`, by hand (`workflow_dispatch`), the runner installing the pinned versions (D15) — numpy 1.26.4, pandas 2.2.2, pytest 8.3.4, jsonschema 4.23.0, jsonschema-rs 0.29.1, PyYAML 6.0.1.

- **dataset.yml, run 38722675475**, green in 17 min 04 s: `make lint` (with `--freeze`) clean; `dataset` 2 min 09 s, `variants` 4 min 00 s, `generated` 7 min 23 s; `test` 534 passed, 1 skipped (3 min 11 s); `check` "build verified (3304 files, 7 manifests)" — the runner reproduces the seven re-blessed manifests, the derived timelines and the coverage grid byte for byte.
- **harness.yml, run 38722678829**, green in 1 h 00 min 40 s: the build and `check` as above; `make -C harness lint` clean (5 min 03 s); `make -C harness test` 296 passed, 2 deselected (36 min 15 s), one warning — a `SyntaxWarning` for the escape `` \` `` in `daemon/tools/drivertable/lint.py:25`'s docstring, raised where the runner compiles the module afresh.
