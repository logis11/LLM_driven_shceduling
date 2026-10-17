# Final memo — the dataset rebuild's closing memo to 인경민 and 박이안 (spec decision 13)

Files written: `docs/memos/2026-10-17-dataset-rebuild-wrap-up.md` (new), `docs/README.md` (the open memo list and the Full index table, one line each). Read against HEAD `d0df65dc` on `jioh/dataset-rebuild` and re-checked at `5e9477f0` (the answers-2 follow-up and the language answer landed meanwhile; no change to the code, the data or `rows/final-memo.md`), the build tree at the second data rebuild (`57342aab`, 2026-10-17). Nothing staged or committed.

Sources: `rows/final-memo.md` (21 drafting rows and W-0727), the work list's "## Final memo" section and the answers it points to ("## For 인지오": W-0432, W-0727, W-0735, W-0736, W-0742, W-0743, W-0750, W-0732, W-0752, W-0753, W-0756, W-0758; "## Questions from the waves": K03, K04, K05, K09, K10 (X4), K17, F3 (M1), F3 (M2), N1, N3, B3), the 9.15 line of `_dev/TODO.md:179`, spec decisions 9, 10, 12 and 13.

## Rows carried

| Row | Memo section | Note |
|---|---|---|
| W-0713 | §1; the From line; §5.1 last bullet | framed against the heads-up's promises; the heads-up §3's "rebuild가 들어오면 알려드릴게요" is this notice, and its "recognition log는 rebuild 뒤에 다시 뽑아야 해요" restated for 박이안 |
| W-0714 | §2.1; §3.2 (e) | line numbers corrected (below) |
| W-0715 | §2.2; §5.1 | |
| W-0716 | §2.3 | the 188 generated files refused by the loader pointed to §3.1 |
| W-0717 | §2.4 | |
| W-0718 | §3.1 | counts re-run at HEAD (below); the memo is 인경민's first notice (W-0735's answer (b)) |
| W-0719 | §4.7 | sizes re-read at HEAD; the row's cost note (42 million trace lines) carried as one clause |
| W-0720 | §3.2 (a)–(h); §4.6; §2.6 | (g) as a proposal needing 인경민's agreement (K05 answer (c)); (h) per K17 answer (c); the notes' starvation-net line in §4.6; the notes' "freeze over bound values and the release map … in force, binding the dataset's side alone" in §2.6 |
| W-0721 | §3.3 | |
| W-0722 | §4.2; §3.3 last sentence | |
| W-0723 | §4.1 | Q2 pointed to §6.1 (W-0736's answer (a)); `fork_cap`'s answer stated as 9.6 D19 records it |
| W-0724 | §5.2 | |
| W-0725 | §7 | each open memo's ask and owner as its header line states it at HEAD, grouped per person |
| W-0726 | §8 | with the 136M Keystrokes windows' exclusion, as `dataset/LICENSE` states it at HEAD (K04 answer (b)) |
| W-0825 | §6.2 | |
| W-0826 | §2.8 | |
| W-0827 | §6.3 | |
| W-0828 | §6.1 | |
| W-0829 | §2.7 | |
| W-0894 | §4.4 | drafted as K09's option (b); held for 인지오's confirmation (review point 2) |
| W-0978 | §2.5 | |
| W-1001 | §4.3 | |
| W-1002 | §4.5 | |
| Spec decision 9 (skip rule, zero-wait `ready` line owed) | §3.2 (b), (a) | with the docs keeping the backlog rule until the skip rule lands |
| Spec decision 13 (every other owed conformance item, as the RQ0 gate spec states them) | §3.2 (d), (e), (g), (h); (c), (f) as in the code | |

## Rows not carried

- **W-0727** — 인지오's recorded answer (2026-10-16) is (b): nothing is asked, the final memo carries no item for it. Put in review point 1, not in the memo.

## Checked against the code and data at HEAD

- `simulator/src/sim.cpp` — last commit `6bf9d850` (2026-10-10); 988 lines.
  - `:662` a program past its last instruction is `Done`; `settled` (`:850–853`) emits `task_end` reason `exit`; `on_depart` (`:838–848`) emits `task_end` reason `depart` with no guard on `Done`.
  - `:674` `t0` = first TIMER execution; `:675–678` overdue ticks consumed at once (backlog), no `ready` line; `:686–691` a WAIT completed from the pending count or the mailbox continues with no `ready` line.
  - `:636–644` `advance` re-enqueues a task reaching its next RUN with `ready(cause=arrive)` and no `run_end`.
  - `:734–738` `on_arrive` executes the leading instructions in the arrival step.
  - `:759–768` `on_task_end` returns a fork slot only; no `children:` completion.
  - `:787–798` `deliver` carries the waker's deadline; `:34–38` the B2 periodic class comment.
  - `:205–210` `Mlfq::start`: U1 cold reset (`:208`), U2 levels kept (`:209`), boost armed at now + `boost_interval_us` (`:210`); `:582–610` `apply_config` (`:597` voids policy timers, `:603` `pol_->start`).
  - `:570–580` `on_config_apply` queues an entry while a drain is pending or a switch drains (U3); `:823–828` `dispatch` applies the queued entries once the lane is free.
  - `:329–334`, `:364–372` LOTTERY's two-stage draw.
  - `:876` dies "WAKE target is not a top-level task"; `:899–904` the id map from `arrive` events only; `:917` spawn-table programs compiled against it; `:921` `fork_cap` read with every spawn table.
  - `:892–928` `load_workload` reads `meta.id` and `events` only.
  - `:937–967` `load_schedule` keeps every entry and reads no `batch_bandwidth_cap`; `:540–545` `set_schedule` queues each; `:513–534` `run` processes every event.
  - `:970–988` `main`: positional `<workload.json> [<config-schedule.json>]`, trace to stdout; `:514–516` header `"sim":"src/sim"` hardcoded.
  - grep: no `declared_class`, no `bandwidth`, no `children:` handling.
- `harness/experiments/rq0-gate.yaml:325–357` — `simulator-conformance`, items (a)–(h), "(c) and (f) the simulator does today; the others its owner holds as owed"; `:23` `telemetry: [focus]`; `:55–65` judging (19) and reporting (32, `c2-p2a-idle` included); the eight compile variants at `:66–86` (`@venue-x0.8`, `@venue-x1.25`, `@corner-low`, `@corner-high` of `c1-compile` and `c7-compile`).
- `harness/scoring/scoring-spec.yaml:112` — `c1-compile`'s `build` turnaround, weight 1.0.
- `harness/guards/guard-spec.yaml:143–148` — `starvation_floor`, 30 000 000 µs.
- `harness/tools/harness/primitives.py:114–117` — `config_applied` at or after `t_end` dropped; `:241–275` `boost_window`'s grid restarted at each applied MLFQ entry.
- `harness/tools/harness/manifests.py:84`, `:88` — `files.select`, `pins.generated`.
- `harness/tools/tests/mocks/daemon.py:52`, `:58–59` — the mock daemon's projection with `declared_class` per task and per (name, class) child group; `harness/tools/tests/mocks/mock_daemon.py:35` the required `--telemetry` flag.
- `harness/tools/tests/fixtures/mock-switch/worked.md:42` — 44600, `probe` takes the lane (re-derived, `d5443eb0`, 2026-10-16).
- `dataset/schema/workload.schema.json:111` (`declared_class`, enum `normal`/`idle`), `:119` (required on `arrive_event`), `:163` (required on `spawn_entry`); `fork_cap` not required by the schema (`:141–145`).
- `dataset/archetypes.yaml` — header "(v0.2)"; 29 `declared_class` lines; `idle` at `:1456` (`game-download-idle`, key `:1454`), `:1528` (`file-indexer`, `:1526`), `:1653` (`incremental-backup`, `:1651`).
- `dataset/build/coreset-single/` — 51 core and 78 variant `*.workload.json`; the seven core files holding an `idle` task (grep): `c1-backup`, `c1-indexing`, `c2-p1b`, `c2-p2a-idle`, `c2-p3b`, `c7-backup`, `c7-indexing`.
- Sizes: `c6-dual.workload.json` 187,601,795 B, sha256 `6005d5e5…` = its `dataset/build.manifest.json` entry; the 51 core files 678,172,716 B; next largest `c1-transcode` 152,752,546 B; `dataset/build/` 6.8 GB.
- Manifests: `build.transition-grid` 480, `build.return-grid` 720, `build.flap-stress` 24, `build.distractor-grid` 272, `build.familiarity-ladder` 66 (1,562); `build.variants` 78; 51 + 78 + 1,562 = 1,691.
- Child-targeted WAKEs (scratchpad script `count_child_wakes.py`, every `*.workload.json` with a `spawn_table`): 201 files, every WAKE in a spawned program targets a spawned child (none a top-level id), 855,150 in all; `c1-compile`, `c3-workday`, `c4-compile`, `c6-dual` and `c1-compile`'s four variants 43,620 each; `c7-compile` and its four variants 25,269 each; generated: transition grid 60, return grid 90, distractor grid 32, familiarity ladder 6 files; flap-stress none.
- `fork_cap`: in the 201 files, the count of `"spawn_table"` equals the count of `"fork_cap"` in every file; `dataset/tools/wlc/compiler.py:128–130` emits it with every spawn table, `:605` (build) and `:693` (module build) set it to `parallelism_cap` × 6.
- `dataset/tools/wlc/compiler.py:620` (`_orchestrator_unroll`, build-orchestrator) and `:705` (`_module_build_unroll`, module-build-orchestrator) append `WAIT children:<iid>`.
- `dataset/tools/wlc/linter.py:394` (a spawned child's WAKE resolves as a top-level task's), `:408–417` (no program runs out), `:203` `lint_bound_sources`, `:276` `lint_releases`.
- `dataset/timelines/coreset/`: `c1-gaming` `lane_share` 0.9 (`:19`), `c2-p2a` 0.95 (`:29`), `c2-p2b` 0.95 (`:32`), `c3-evening` 1.45 (`:36`); `c2-p2b` binds `package-upgrade` named `unattended-upgr` (`:60`, `:65`).
- `.github/workflows/dataset.yml:21` — `make -C dataset generated` in CI.
- `daemon/driver-table/prior.yaml:209–232` — the two gaming rows as §4.2 states them.
- `docs/data-contracts.md` — §4 `:205` (build not committed, make targets), `:272` (the class rule; corrected in fix round 1 from `:267`, a comment inside Example B's code block), `:288` (run file), `:295` (visible projection with class and focus); §5 rule 6; §7 Order, Drain, End; §8 top-level `telemetry`; §11 contract 10; §13 freeze rule; §14 entries 2026-10-17, 2026-10-16, 2026-10-15, 2026-10-12, 2026-10-11 (×3), 2026-10-09.
- `docs/harness/metrics.md:67` (twenty-five columns), `:309` (§11 item 1), §6.2, §6.10 (`:192`), §11 item 9 (`:317`).
- `docs/simulator/simulator-guide.md:171–173` (the §4½ program ends with a third WAIT), `:221` (the one cap; no executor starvation window), §9.2 `:290` (t₀ decided, the arrival).
- `docs/research-claims.md:23–25` (the claim), `:313–321` (the new 'not claimed' entry), ### RQ5's ladder; `docs/recognition-vocabulary.md:34` (`render` gloss unchanged), §4 extension rule.
- `docs/references.md:334` (`linux-sched-core`), `:459` (`kdenlive`).
- `docs/data-contracts.md` and `daemon/` hold no "formatted prompt" or "Today Date" (grep, empty).
- `LICENSE` (MIT, the three holders); `dataset/LICENSE` (CC-BY-NC-SA-4.0; Licensed Material: `dataset/` minus code and the 136M Keystrokes windows, `dataset/build/`, the release assets; SWELL-KW credited; `aalto-*` outside the grant).
- `simulator/memo/memo_261010.md` Part B (`:75` regression on 24 files), Part C, Part D (`:118`), Part F (`:147–189`); `simulator/notes/note1010.md:97–140`; `simulator/notes/note-for-jioh-edf-chain-stage-class.md:57–65`; `simulator/src/notes.md` §4 gaps 1, 3, 4.
- Memo header lines read at HEAD and in the working tree for §7.

## Row text against the code (the code wins)

1. W-0714 cites `dataset/archetypes.yaml:1450`, `:1521`, `:1647`; at HEAD the `declared_class: idle` lines are `:1456`, `:1528`, `:1653`.
2. W-0714 cites `docs/data-contracts.md` §4 line 267 for the visible projection showing the class; at HEAD (and at `d0df65dc`) line 267 is a comment inside Example B's code block, the class rule paragraph is `:272` and the projection paragraph is `:295`. The memo cites 272 for the rule and "§4의 visible projection" for the projection (corrected in fix round 1; the first draft repeated 267).
3. W-0719 gives `c6-dual`'s hash `883bf5c9…` "as of the last re-bless (9.23 D17)"; at HEAD the last re-bless is the second data rebuild (`57342aab`, 2026-10-17) and the file hashes to `6005d5e5…`, matching the manifest; the sizes are unchanged. The memo dates them "2026-10-17 build".
4. W-0720 cites `harness/experiments/rq0-gate.yaml:323–342`; at HEAD `:325–357`, items (a)–(h).
5. W-0720 cites `docs/harness/metrics.md` §11 item 1 at line 306; at HEAD `:309`.
6. W-0743's answer (via the (g) item) cites `dataset/tools/wlc/compiler.py:714`, `:799`; at HEAD `:620`, `:705`.
7. W-0723's notes cite `compiler.py:659–661`, `:699`, `:787` for `fork_cap`; at HEAD `:128–130`, `:605`, `:693`. LOTTERY cited `sim.cpp:328–366`; at HEAD `:329–334`, `:364–372`.
8. W-0717 cites `on_depart` `:838–845`; the function spans `:838–848`. W-0718 cites `:899–905`; the id map is `:899–904`. W-1002 cites `primitives.py:114–115`; the drop is `:114–117`. W-0743's answer cites `on_task_end` `:758–768`; it starts at `:759`.
9. W-0720's change lists four owed items ((a), (b), (d), (e)); after its amendments and the RQ0 gate spec at HEAD, six are owed ((a), (b), (d), (e), (g), (h)). The 9.15 line of `_dev/TODO.md:179` still says "the four executor conformance items owed" (dev history, not edited).

## Decisions

1. **File name and form.** `docs/memos/2026-10-17-dataset-rebuild-wrap-up.md`, Korean (the spec's open item, answered (a) on 2026-10-17 in the work list), the heads-up memo's register and structure (H1 with an em-dash subtitle, the status line, one open line, the From line, numbered `##` sections).
2. **Grouping.** What changed for both (§2), then the asks and answers per person (§3–§5: 인경민's asks, 인경민's answers and notices, 박이안's), then the proposals needing all three (§6), the open memos per person (§7), the licences (§8). (g) sits with 인경민's asks, since the §14 2026-10-16 entry puts it in force once 인경민 agrees; the one-occupancy trace rule sits in §6, since the trace contract's change needs all three (§13).
3. **The open memos (§7)** are written from each memo's header line at HEAD. `docs/memos/2026-09-11-invocation-contract.md`'s open line gained the RQ0 gate spec's item (h) during drafting (W-1005, applied in Q3 and committed before `5e9477f0`); §7's entry, which points the simulator side to (h), agrees with it. W-1008 (optional, open) edits that memo's entry in `docs/README.md`'s open list (line 96); this step's two README lines are elsewhere in the file and do not touch it.
4. **`fork_cap`'s answer** is stated as 9.6 D19 records it (jobs in flight, six members a job, the B3 reading settled on make jobs), with the absent case checked over the data: no spawn table in the build lacks `fork_cap`.
5. **Optional clauses from row notes carried:** the starvation safety net (W-0720's notes; the declared-class memo already said it, so §4.6 points there), the `c6-dual` trace length (W-0719's notes; 9.14's count on the mock trace — `_dev/research/jioh/task-9.14-consumer-rework/changelog.md:108` — before the later re-blesses, which added no executed work), the dataset-only rules of the 2026-10-16 entry (W-0720's notes). Listed in review point 5.
6. **`docs/README.md`.** One line in "### Open" after the 2026-10-08 memo, in that list's form, and one row in the Full index table after the 2026-10-08 row (the index lists every doc). The README's `Updated` already reads 2026-10-17.

## For 인지오's review

1. **W-0727, the 2026-10-06 note.** Recorded answer (2026-10-16): (b), nothing asked. The memo carries nothing. Options: (a) ask 인경민 to commit the note so the TIMER memo's "your 2026-10-06 finding" resolves to a file; (b) as drafted, nothing.
2. **W-0894, §4.4 (`simulator/src/notes.md` gaps 1 and 3).** Included as K09's option (b). Options: (a) drop §4.4 — 인경민 reads the restated guide; (b) keep it as drafted.
3. **The WAIT-first arrival.** 인지오's answer (c) of 2026-10-17 to K10 (X4) made the mocks follow the reference simulator (metrics §11 item 5), which settles memo_261010 Part F's "Ours to decide and write down" row "Zero-length occupancy for an arriving task whose first instruction blocks — none, only `x_block`". No row carries it to the memo. Options: (a) add one line to §4 in §4.3's form (the row can be written down as decided); (b) leave it out.
4. **Optional clauses** (decision 5): §4.6 (starvation safety net), §4.7's last sentence (42 million trace lines), §2.6 (the dataset-only rules), §5.1's last bullet (recognition logs to regenerate). Options per clause: keep or drop.
5. **§6.3's framing.** `docs/recognition-vocabulary.md` §4 names adding or removing a mode, an attribute's semantics and the config schema as all-three decisions; a gloss change is not listed. The memo proposes the widened gloss for the three owners' agreement, as the recorded answer to W-0432 has it. Options: (a) as drafted, a proposal; (b) apply it now with a §5 entry and tell them.

6. **(g)'s wording in the English sources.** The memo now says the WAIT completes when every child it spawned has ended (the last live child ends), as `docs/harness/metrics.md:166` reads the orchestrator's turnaround ("it exits only after its children"). The sources state it as "when the last child it spawned ends", which also reads as "when the child spawned last ends" — wrong with eight jobs in flight: `harness/experiments/rq0-gate.yaml:343–345` (item (g)), `docs/data-contracts.md:274` (§4 Example B (3), "when the last child make spawned ends") and `:587` (§14, 2026-10-16), `docs/simulator/interpretation-contract.md:32` and `:59`, `docs/simulator/simulator-guide.md:157`, and the quote in `docs/guidebook/dataset/08-decision-chronicle.md:1817`. Options: (a) restate each as "when every child it spawned has ended"; (b) leave the sources as they are, the memo carrying the unambiguous reading.
7. **The core file renamed on 2026-10-12** (`c5-t3` is `c6-alias`: the same tasks, archetypes and seed, its segment carrying `spoof` and `pre_committed_miss`; `docs/data-contracts.md:589`). No row carries it and the memo does not name it, though 인경민's regression re-run (§3.3) and 박이안's regenerated recognition logs (§5.1) both meet the new id. Options: (a) add one clause to §1's "새 file set" bullet; (b) leave it to `docs/data-contracts.md` §14, to which §1 already points.

## Check round 1

Fresh check against HEAD `5e9477f0` and the working tree (`dataset/build/` on disk matches `dataset/build.manifest.json`: `c6-dual` sha256 `6005d5e5…`). Verdict: **not passed**. Two material findings (1, 2) and one factual overreach (3) need fixing; the rest are minor.

Re-checked and holding: every `simulator/src/sim.cpp` line the memo cites (`:34–38`, `:205–210`, `:329–334`, `:364–372`, `:513–534`, `:514–516`, `:540–545`, `:570–580`, `:582–610`, `:597`, `:603`, `:636–644`, `:662`, `:674`, `:675–678`, `:686–691`, `:734–738`, `:759–768`, `:787–798`, `:823–828`, `:838–848`, `:876`, `:892–928`, `:899–904`, `:917`, `:937–967`, `:970–988`; grep finds no `declared_class`, `bandwidth` or `children:`); `harness/experiments/rq0-gate.yaml:23`, `:55–65`, `:325–357`, items (a)–(h) and "(c) and (f) the simulator does today"; `scoring-spec.yaml:112`; `guard-spec.yaml:143–148`; `primitives.py:114–117`, `:241–275`; `manifests.py:84`, `:88`; `mocks/daemon.py:52`, `:58–59`; `mock_daemon.py:35`; `workload.schema.json:111`, `:119`, `:163`; `archetypes.yaml` (v0.2 header; `idle` only at `:1456`, `:1528`, `:1653`); the seven idle core files; `compiler.py:128–130`, `:605`, `:620`, `:693`, `:705` (`children:` WAIT already in `aaa45430`); `linter.py:203`, `:276`, `:394`, `:408–417`; timelines' `lane_share` and `c2-p2b`'s `unattended-upgr`; `prior.yaml:209–232`; `.github/workflows/dataset.yml:21`; manifests 51 + 78 + 480 + 720 + 24 + 272 + 66 = 1,691; `du` 6.8 GB; `c6-dual` 187,601,795 B, core total 678,172,716 B, no file in any set above 150 MB but `c6-dual`; recomputed independently: 201 files with a spawn table, 855,150 WAKEs in spawned programs, every one at a spawned child, none from a top-level program, per-file 43,620 / 25,269 and generated 60 / 90 / 32 / 6, `fork_cap` beside every spawn table; the 9.14 changelog's 42 million trace lines (`:108`); `metrics.md:67`, `:309`, `:317`, §6.10; `simulator-guide.md:171–173`, `:221`, §9.2; `research-claims.md` claim, ladder, 'not claimed' entry, link 1–7; `recognition-vocabulary.md:34`, §4, §5; `references.md:334`, `:459`; data-contracts §5 rule 6, §7 Order/Drain/End, §13, §14 entries; no "formatted prompt"/"Today Date" in data-contracts or `daemon/`; `LICENSE`, `dataset/LICENSE`; every memo header line against §7 (all nine open memos present, asks and owners match); `docs/README.md` open-list line and Full-index row in the lists' form; the TODO 9.15 line's final-memo items all carried; every row carried or (W-0727) soundly left out.

Findings:

1. **Memo :188 (§6.3) — wrong segment.** "`c2-p3a`의 첫 segment" is a render segment: false. `c2-p3a`'s first segment (0–60 s) is `video-edit`; its render segment is the second, 60–326 s (`dataset/timelines/coreset/c2-p3a.timeline.yaml:13`, `:15`; the compiled file's `ground_truth` agrees). The row's "segment 1" is zero-based. Fix: "`c2-p3a`의 두 번째 segment(60–326 s)".
2. **Memo :99 (§3.2 (g)) — the Korean fixes the wrong reading of the rule 인경민 is asked to implement.** "마지막으로 spawn한 child가 끝날 때 완료되고" = "when the child spawned last ends". With eight jobs in flight, the last-spawned child can end while an earlier job's members still run, so the WAIT would complete with live children — against `docs/harness/metrics.md:166` ("An orchestrator's turnaround is the build's makespan, since it exits only after its children") and W-0743's own framing ("wakes it when the children are done"). Fix: state it as all children ended, e.g. "spawn한 child가 모두 끝날 때(살아 있는 마지막 child가 끝날 때) 완료되고". For 인지오: the English sources (`rq0-gate.yaml` (g), data-contracts §4 Example B (3) and §14 2026-10-16, interpretation contract `:32`, `:59`) carry the same ambiguous "the last child it spawned ends".
3. **Memo :114 (§4.1, `fork_cap`) — stated more widely than the data.** "object job 하나는 spawn-table entry 여섯 개 … `fork_cap` = `parallelism_cap` × 6이 … 동시 실행 job 수를 정확히 묶어요" is given generally, with `compiler.py:693` (`module-build-orchestrator`) cited as the same rule. In `c7-compile` (`dkms`, a judging file) the 9,980 entries form 1,557 jobs of 6, 8 or 10 members (1,325 / 145 / 87) under `fork_cap` 48, so there the cap does not exactly bound jobs in flight. Fix: scope the sentence to `build-orchestrator` (`make` in `c1-compile`, `c3-workday`, `c4-compile`, `c6-dual`), or add `c7-compile`'s case.
4. **Memo :23 (§2.1) — wrong line.** "`docs/data-contracts.md` §4, 267번째 줄": line 267 is a comment inside Example B's code block; the class-rule paragraph is `:272` (at `d0df65dc` and at HEAD). This log's check list and its "Row text against the code" item 2 repeat the wrong number.
5. **Memo :35 (§2.2) — wording.** "25번째 identity column `telemetry`": `telemetry` is the 6th of the records' 25 columns (`metrics.md:67` counts all 25); there are not 25 identity columns. Suggest "identity column `telemetry`가 더해져 column이 25개가 됐어요".
6. **Memo :5 (From line) — reading guide drops an ask.** "급하면 §1, §3, §5만 읽어도 돼요" skips §6, which the open line (:4) lists as an ask of both owners (the three proposals). Add §6 or drop the sentence.
7. **Memo :212 (§7, 인지오) — bare tracker label.** "Phase 9 끝의 measurement audit": "Phase 9" is 인지오's `_dev/TODO.md` numbering, a bare label to the readers. E.g. "이번 dataset rebuild를 마무리하는 measurement audit".
8. **Review point, not a defect.** The core set's composition change on 2026-10-12 (`c5-t3` became `c6-alias`, data-contracts §14) is in no row and not in the memo's "실제로 바뀐 것". It is a core file id that 인경민's regression re-run (§3.3) and 박이안's regenerated logs (§5.1) will meet. Options: (a) add one clause to §1; (b) leave it to data-contracts §14, as §1 already points there.

## Fix round 1

Against HEAD `5e9477f0` and the build on disk. Memo edits only in `docs/memos/2026-10-17-dataset-rebuild-wrap-up.md`; `docs/README.md` unchanged (its two lines name the memo by file and topic, which did not change). Nothing staged or committed.

1. **§6.3, `c2-p3a`'s render segment — fixed.** `dataset/timelines/coreset/c2-p3a.timeline.yaml:13` is `0s–60s` `video-edit`, `:15` is `60s–326s` `render`; the file's header comment (`:4`, "Segment 1 runs 60–326 s") counts from zero. Memo: "`c2-p3a`의 두 번째 segment(60–326 s)".
2. **§3.2 (g) — fixed.** Memo: "spawn한 child가 모두 끝날 때(살아 있는 마지막 child가 끝날 때) 완료되고". Checked: the WAIT follows the last FORK (`compiler.py:620`, `:705`), so "no child live" is "every spawned child ended"; `docs/harness/metrics.md:166` reads the orchestrator's turnaround as the build's makespan. The English sources' ambiguity is review point 6.
3. **§4.1 `fork_cap` — fixed.** Recomputed over every spawn table in `dataset/build/` (scratchpad script `job_sizes.py`, jobs grouped by the `<iid>.j<n>.` id prefix): `build-orchestrator` (`make`: `c1-compile` and its four variants, `c3-workday`, `c4-compile`, `c6-dual`, 2,908 jobs of 6; every generated compile file, jobs of 6) — all six-member jobs under `fork_cap` 48; `module-build-orchestrator` (`dkms` in `c7-compile` and its four variants) — 9,980 entries, 1,557 jobs: 1,325 of 6, 145 of 8, 87 of 10, `fork_cap` 48. The compiler's own docstring states the module build's cap as tasks, not jobs (`compiler.py:686`, "at most `parallelism_cap` × 6 tasks in flight (D57)"). The memo now scopes the exact-job-count sentence to `make` (citing `:605`) and states `c7-compile`'s case (citing `:693`): the cap bounds 48 live children there, not jobs in flight.
   - **Found while fixing, same defect: §3.1's first bullet** said every compile tree's jobs are the six members `sh`, `gcc`, `cc1`, `as`, `fixdep`, `rm`. `c7-compile`'s jobs are `sh`, `mkdir`, `x86_64-linux-gn`, `cc1`, `as`, `rm` (1,125), `sh`, `x86_64-linux-gn`, `cc1`, `as`, `fixdep`, `rm` (200), and eight- and ten-member trees with `dirname` (145, 87). Fixed: `make`'s object job six members, `c7-compile`'s `dkms` job 6–10 members (`compiler.py:563` `_object_job`, `:641` `_tree_job`).
4. **§2.1 line number — fixed.** The class-rule paragraph is `docs/data-contracts.md:272` at `d0df65dc` and at HEAD; `:267` is a comment in Example B's code block. Memo: "272번째 줄". This log's check list and "Row text against the code" item 2 corrected in place.
5. **§2.2 column wording — fixed.** `telemetry` is the sixth of the records' 25 columns (`docs/harness/metrics.md:67`, the Identity table). Memo: "identity column `telemetry`가 더해져 column이 25개가 됐어요". Checked the count: the Records section's column table had 24 rows at `cd3fd535` (2026-10-09) and 25 after the 2026-10-11 `telemetry` column; the text's "twenty-four" was corrected to "twenty-five" in `b8475b7d` (2026-10-17).
6. **From line, reading guide — fixed.** "급하면 §1, §3, §5, §6만 읽어도 돼요": §6's three proposals are an ask of both owners in the open line.
7. **§7, the validity-review memo's entry — fixed.** Its header line names the sub-task number of the exit audits (`_dev/TODO.md:180`, "Exit audits — the claim, measurement and compiled-number audits re-run on the final state", under "Phase 9 — Workload dataset rebuild from the critical findings", `:101`). Memo: "이번 dataset rebuild를 마무리하는 measurement audit과 함께".
8. **The `c5-t3` → `c6-alias` rename — review point 7**, memo unchanged pending 인지오's choice. Verified: `docs/data-contracts.md:589` (§14, 2026-10-12).

Rows' carriage after this round: W-0718 (§3.1, member sets scoped), W-0720 ((g) restated as all children ended), W-0723 (§4.1, `fork_cap` scoped to `make` with `c7-compile`'s case), W-0827 (§6.3, the second segment) changed in wording only; no row added or dropped.

## Check round 2

Fresh check against HEAD `5e9477f0` and the working tree (memo, `docs/README.md` diff, this log), the build on disk (`dataset/build/` 6.8 GB; `c6-dual` 187,601,795 B, sha256 `6005d5e5…` = `dataset/build.manifest.json`). Verdict: **passed** — nothing material is wrong. Four minor points below; none blocks.

Re-checked and holding:

- Rows: every row of `rows/final-memo.md` (21 drafting rows) is carried where Fix round 1 says; W-0727 soundly left out (its recorded answer (b), 2026-10-16: nothing asked). The 9.15 line of `_dev/TODO.md:179`: every final-memo item is there — `declared_class` (closed set, the three `idle` entries, the run file, the executor rule under every algorithm, the projection per task, archetype contract v0.2), the sizes (187.6 MB / 678 MB in place of 190 / 681), the two recognition-log questions, the loader's refusal, the conformance items (six owed now, not "four"), the focus, the generated layer, no program running out. Spec decision 13's three additions (open memos, skip rule and zero-wait `ready` line owed, licences) and decision 9's backlog-until-skip line are there.
- `simulator/src/sim.cpp` (last commit `6bf9d850`, 988 lines), every cited line re-read: `:34–38`, `:205–210` (`:208` U1, `:209` U2, `:210` boost armed), `:329–334`, `:364–372`, `:513–534` (`:514–516` `"sim":"src/sim"`), `:540–545`, `:570–580` (drain condition: lane held, algorithm differs, not out of FIFO), `:582–610` (`:597`, `:603`), `:636–644` (`:642` `ready(cause=arrive)` with no `run_end`), `:662`, `:674`, `:675–678`, `:686–691`, `:734–738`, `:759–768` (slot returned only when the parent waits with `wait_chan < 0`), `:787–798`, `:823–828`, `:838–848` (no guard on `Done`), `:850–853`, `:876`, `:892–928`, `:899–905` (id map from `arrive` only), `:917`, `:921`, `:937–967` (no `batch_bandwidth_cap`), `:970–988` (positional args, trace to stdout). `arm()` (`:444–448`) never cuts the queue, so entries past the workload's end are applied (§4.5). grep: no `declared_class`, `bandwidth` or `children:` handling.
- (g)'s consequence: `c1-compile`'s `build` (`make`) has no `depart`, ends `FORK, WAIT children:build, EXIT`; `c7-compile`'s `dkms` has its `WAIT children:build` after its 9,980th FORK and a serial tail before EXIT; both block to the run's end under the present code. `compiler.py:271` at `aaa45430` already emits the WAIT.
- Counts recomputed independently (scratchpad `check2/wakes.py`, every `*.workload.json` holding a `spawn_table`, 24 s): 201 files (13 core-and-variant, transition 60, return 90, distractor 32, ladder 6), 855,150 WAKEs in spawned programs, every one at a spawned child, none from a top-level program; 43,620 in each `make` compile file and its four variants, 25,269 in `c7-compile` and its four; `fork_cap` (48) beside every spawn table; jobs grouped by `<iid>.j<n>.`: `make` 2,908 jobs of 6, `c7-compile` 1,557 jobs (1,325 of 6, 145 of 8, 87 of 10 = 9,980 entries), every generated job of 6. Manifests 51 + 78 + 480 + 720 + 24 + 272 + 66 = 1,691; core total 678,172,716 B; next largest `c1-transcode` 152,752,546 B.
- §4.1's "exactly bounds jobs in flight" for `make`: `compiler.py:563–600` — finished members wait on their `job:` channel until `sh`'s last step WAKEs them to EXIT, so a job's six members end in one instant and each freed slot is refilled by the blocked orchestrator; live children are six per job in flight between instants. Scoped correctly; `c7-compile`'s case (cap = 48 live children, not jobs) stated correctly (`:686` docstring, `:693`).
- `harness/experiments/rq0-gate.yaml:325–357`: (a)–(f), (h) in the memo match the statement's content item by item (including (a)'s "inside the occupancy after the run_start", (b)'s skipped tick a `deadline` line with `met` false and no work, (h)'s five clauses); "(c) and (f) the simulator does today" matches the code; the four owed besides (g), (h) match `sim.cpp`. (g) see point 3. `:23`, `:55–65`, `:66–86` hold.
- Schema `:111` (enum `normal`/`idle`, no default), `:119`, `:163`, WAKE target `task_id` (`:156`, `:214`); `archetypes.yaml` v0.2 header, `idle` at `:1456`, `:1528`, `:1653` (keys `:1454`, `:1526`, `:1651`); the seven idle core files by grep. `linter.py:203`, `:276`, `:394`, `:408–417`. `compiler.py:128–130`, `:560`, `:563`, `:605`, `:620`, `:641`, `:693`, `:705`.
- `docs/data-contracts.md` `:205` (build not committed, the make targets, `check`), `:272`, `:274`, `:288`, `:295`–`:312` (projection, children grouped by name and class), §5 rule 6 (incl. "the difference is the field's measured worth"), §7 Order, Drain, End, §8, §11, §12 'run', §13, §14 entries 2026-10-17, -16, -15, -12, -11 (×3), -09; `.gitignore:2` ignores `dataset/build/`; `dataset/Makefile` targets; `.github/workflows/dataset.yml:21`.
- Harness: `metrics.md:67`, `:166`, §6.2, §6.10, §11 items 1, 2, 9; `primitives.py:114–117`, `:241–275`; `manifests.py:84`, `:88`; `mocks/daemon.py:52`, `:58–59`; `mock_daemon.py:35`; `fixtures/mock-switch/worked.md:5`, `:42`, `:53–54`; `scoring-spec.yaml:112` (no `preempt_count` term); `guard-spec.yaml:143–148`.
- `prior.yaml:209–232` and the pair review (`:27`, `:45`, `:60`); timelines' `lane_share` 0.9 / 0.95 / 0.95 / 1.45, `c2-p2b`'s `unattended-upgr`, `c1-gaming` without a compositor; render segments: only `c1-render`, `c7-render` and `c2-p3a` (`:15`, 60–326 s) carry `mode: render`, each binding `kdenlive_render`.
- `simulator-guide.md:157`, `:171–173`, `:221`, §9.2 (`:292`); `interpretation-contract.md:31` (backlog kept), `:32`, `:59`; `memo_261010.md` Part B (`:75`, `:87`), Part D (`:118`), Part F (`:151–189`, the rows "TIMER t₀ (D4)" `:180` and "Same-algorithm MLFQ entry" `:188`); `note-for-jioh-edf-chain-stage-class.md:57–65`; `src/notes.md` §4 gaps 1, 3; `note1010.md`; critical-findings memo B3 (`:19`, `:134–138`); 9.6 D19.
- `research-claims.md:23–25`, RQ0/RQ1/RQ5 titles, the RQ5 table, `:313–321`, links 1–7; `recognition-vocabulary.md:34`, §4; `references.md:334`, `:459`; `terminology.md:231`, `:235`; no "formatted prompt"/"Today Date" in data-contracts or `daemon/`.
- `LICENSE` (MIT, three holders); `dataset/LICENSE` (CC-BY-NC-SA-4.0; scope: `dataset/` minus `dataset/tools/`, `dataset/Makefile` and the 136M Keystrokes windows, `dataset/build/`, the release assets; SWELL-KW credited for `dataset/stimulus/` and the `meas/streams/` windows; `aalto-*` outside the grant). §8 matches.
- §7 against all nine open memos' header lines (line 4 of each): every ask and owner matches; none missing.
- Form: path and H1 in the heads-up memo's form, status line, one open line (asks per person, owners), From line, numbered `##` sections, the heads-up's polite register, Korean with terms, paths and code in English; no W-/K-/chunk ids, no 9.xx or Phase numbers; labels used are stated with their meaning (U1·U2, U3, B3, RQ0/RQ1/RQ5, link 1–7, Layer 1/2, p2 pair, (a)–(h)). `docs/README.md`: the open-list line after the 2026-10-08 memo and the Full-index row after its row, both in the lists' form; README `Updated` 2026-10-17. Nothing staged or committed.

Minor points (non-blocking):

1. **Memo :109 (§4.1 heading) — register.** "인지오께 주신 질문의 답": the author honours himself with 께; the memo's own :118 and the heads-up write "인지오가 인경민께 드린 질문". Suggest "인지오에게 주신 질문의 답".
2. **Memo :12 (§1) — "인경민께는 이 memo가 이 일의 첫 알림이에요".** The heads-up memo's 2026-10-17 correction (`8e407e25`, committed before this memo) already states the loader's refusal, the 201 files and `sim.cpp:876`. The sentence rests on 인지오's recorded answer that no separate heads-up was sent and both land the same day, so it stands; optional for 인지오: keep, or drop the sentence.
3. **§3.2 (g) — not the gate's words, deliberately.** The memo renders `rq0-gate.yaml:343–345`'s "completes when the last child it spawned ends" as "spawn한 child가 모두 끝날 때(살아 있는 마지막 child가 끝날 때)" and adds the zero-wait `ready` line from data-contracts §14 2026-10-16. Confirmed the ambiguity the drafter names: with eight `make` jobs in flight, the child spawned last (the last job's `rm`) ends with its job while earlier jobs' members can still be live. Review point 6 carries the choice of wording in the English sources; the memo's reading is the one `metrics.md:166` takes.
4. **Trivial line/wording.** §3.1 cites the id map at `:899–904` (its loop closes at `:905`); §4.5 renders §7 End's "at or after the workload's end" as "이후". Neither misleads.
