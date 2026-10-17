# Work-list rows — the final memo to 인경민 and 박이안

Drafted after the doc chunks (spec decision 13). 21 rows.

### W-0713 · final-memo
- At: new
- Change: Frame the final memo as Phase 9's account of its actual changes, read against what the 2026-09-13 heads-up memo (`docs/memos/2026-09-13-dataset-rebuild-heads-up.md`) said would change and stay stable: the input format kept its fields except the declared class (the memo's own 2026-10-08 correction), and gained the canonical file's `focus` key (9.17) and a new use, spawned children waking children (9.6 D19), which the simulator's loader refuses.
- Final word: Phase 9 spec decision 7 (team communication): a heads-up memo at the start of the phase and a final memo to 인경민 and 박이안 at its end with the actual changes. 9.15 spec decision 13: the final memo comes last, after the doc chunks, drafted from the work list's memo rows and checked against the code, 인지오 and the main session going through it before it is committed; beyond the TODO line's items it carries the memos still open, the simulator's skip rule and zero-wait `ready` line as owed, and the licences; its language is the spec's open item.
- Sources: SX-0678 (Phase 9 spec decision 7, `jioh/phase-9-workload-dataset-rebuild.md:48`)
- Cross-ref: W-0702; W-0714; W-0715; W-0718
- Notes: The spec-derived items (the memos still open, the skip rule and zero-wait `ready` line owed, the licences) are added by the assembly, not by this list. Correction to the raw row's note: the heads-up memo's three executor questions were 인지오's questions to 인경민 (memo line 4), and all three are now answered — LOTTERY by the simulator's code (W-0702), the EDF chain-stage class on 2026-10-10 (`simulator/notes/note-for-jioh-edf-chain-stage-class.md:57–65`), a keystroke during RUN by `docs/harness/metrics.md:307`. The 'input format unchanged' promise (heads-up memo line 4 and §3) is the memos group's correction row (W-0701).

### W-0714 · final-memo
- At: new
- Change: Tell 인경민 the shipped field `declared_class`: required on every task record — each `arrive` event and each spawn-table entry (`dataset/schema/workload.schema.json:119`, `:163`) — from the closed set `normal`/`idle`; `idle` on `file-indexer`, `incremental-backup` and `game-download-idle`, so seven core files carry an idle task (`c1-indexing`, `c7-indexing`, `c2-p1b`, `c1-backup`, `c7-backup`, `c2-p3b`, `c2-p2a-idle`); the run file carries it with the events; the executor's strict idle rule under every algorithm, FIFO included (an idle task runs only when no task of another class is runnable and is preempted at once when one wakes). Tell 박이안 the visible projection shows each task's class (`docs/data-contracts.md` §4, line 267), as the harness's mock daemon carries it per task and per folded child group. List the other 9.13 decisions taken without them: `c2-p2a-idle` beside `c2-p2a`, outside the judging set; the single-lane set alone, the native compile mode dropped; the archetype contract at v0.2 (`docs/data-contracts.md` §14, entry of 2026-10-09).
- Final word: 9.13 D2 (2026-10-09; applying 9.13 spec decisions 1–5, 8 and 9, from 9.11 D4–D6, D16, D18, D34), with 9.13 D4 and 9.13 spec decision 3: every archetype entry and every task record (each `arrive` event and spawn-table entry) carries `declared_class`, required, no default, from the closed set `normal` and `idle`, a task's class its bound entry's (a spawned child's that of its child entry); `idle` on `file-indexer`, `incremental-backup` and (9.13 D4) `game-download-idle`; the run file carries it with the events; the executor applies 9.11 D5's strict idle rule under every algorithm, FIFO included (9.11 D18); the visible projection shows the class per task (9.13 spec decision 3; the mock daemon per task and per folded child group, 9.14 D1); `c2-p2a-idle` beside `c2-p2a`, outside the judging set; the native compile mode dropped, the dataset ships the single-lane set alone (9.13 D1); the archetype contract at v0.2 (`docs/data-contracts.md` §14, 2026-10-09). 9.13 spec decision 1: 인경민 and 박이안 agreed the contract change of the 2026-10-08 declared-scheduling-class memo; throughout 9.13 인지오 decides and the teammates are told in the phase's final memo.
- Sources: SX-0249 (TODO 9.15 line (from 9.13 D2, D4, R4), `_dev/TODO.md:179`); SX-0537 (9.13 D2, `task-9.13-rebuild/changelog.md:15`); SX-0538 (9.13 D2, `task-9.13-rebuild/changelog.md:15`); SX-0679 (9.13 spec decision 1, `jioh/task-9.13-rebuild.md:21`)
- Cross-ref: W-0720
- Notes: Checked at HEAD: `dataset/schema/workload.schema.json:111` defines `declared_class`, required at `:119` (arrive) and `:163` (spawn-table entry); `dataset/archetypes.yaml:1450` (`game-download-idle`), `:1521` (`file-indexer`), `:1647` (`incremental-backup`) carry `idle`; the seven core artifacts holding an idle task are those listed (grep of `dataset/build/coreset-single/` at HEAD). The simulator reads no `declared_class` (no occurrence in `simulator/src/sim.cpp`): the strict idle class is conformance item (e), owed (W-0720). The 2026-10-08 memo already carries 9.13's dated line naming the field (§1, the 2026-10-09 bullet), so 9.13 spec decision 11's memo line is applied; the final memo carries what shipped.

### W-0715 · final-memo
- At: new
- Change: Name the focus change (9.17) to both: the canonical file's fourth top-level key `focus` (pinned focus intervals per top-level task) — the run file the simulator reads (`meta.id`, `events`) unchanged, which is all 인경민 needs; to 박이안, the visible projection's per-task focus intervals, the snapshot's focus holder beside the name → count multiset (none when no window holds it), a focus change emitting a snapshot and a query point as a count change does (`docs/data-contracts.md` §5, rule 6), the two telemetry shapes `focus`/`names` with the recognition log's top-level `telemetry` field and the daemon's `--telemetry focus|names` flag (§8, §11), every condition runnable with the field present and absent, the records' 25th identity column `telemetry`; the RQ0 gate spec runs `telemetry: [focus]`.
- Final word: The 2026-10-10 dataset audit's 'Decision — focus enters the telemetry' (2026-10-11, 인지오's grill), implemented by 9.17 (D1, D4, D5): the timeline's two tracks `input` (keystroke placement) and `focus`; the canonical workload's fourth top-level key `focus`, the run file unchanged (the simulator reads `meta.id` and `events`); the visible projection's per-task focus intervals; telemetry rule 6 — the snapshot carries the focus holder beside the name → count multiset, a focus change emits a snapshot and a query point; the shapes `focus` and `names`, the log's top-level `telemetry` field and the mock daemon's required `--telemetry` flag; the records' 25th identity column `telemetry`; `docs/data-contracts.md` §14 entry of 2026-10-11 ('Decided by 인지오 alone … the phase's final memo carries the change'). The audit: 'the simulator's telemetry extraction and the daemon's prompt follow the memo'.
- Sources: SX-0311 (TODO 9.15 line (from the 2026-10-11 audit), `_dev/TODO.md:179`); SX-0732 (audit 2026-10-10 decision: focus enters the telemetry, 'Lands in', `jioh/2026-10-10-dataset-audit-before-9.15.md:113`); SX-0666 (9.17 spec scope, `jioh/task-9.17-focus-in-the-telemetry.md:12`)
- Notes: Checked at HEAD: a compiled core file's top-level keys are `events`, `focus`, `ground_truth`, `meta`; `docs/data-contracts.md:370` (`"telemetry": "focus"`), `:498` (`--telemetry focus`), `:554` (the §14 entry); `harness/experiments/rq0-gate.yaml:23` (`telemetry: [focus]`). The daemon guide (line 82) calls adding a projection field a protocol change all three sign off on; 9.17 was decided by 인지오 alone, so the memo is where the teammates learn of it.

### W-0716 · final-memo
- At: new
- Change: Tell 인경민 and 박이안 the generated layer exists beside the core set: five sets — `transition-grid` 480, `return-grid` 720, `flap-stress` 24, `distractor-grid` 272, `familiarity-ladder` 66, 1,562 files — design with no realism claim, compiled the same way into `build/<set>-single/`, each with its own manifest, built in every CI run; the simulator and daemon read them as they read the core set; an experiment spec selects files from a pinned manifest by its axes (`files.select`, `pins.generated`).
- Final word: The 2026-10-10 dataset audit's direction (2026-10-11) and 9.19–9.21: a generated layer beside the core set — the transition grid (480), the return grid (720), the flap-stress set (24), the C4 distractor grid (272) and the C5 familiarity ladder (66), 1,562 files — composed from the C1 task sets by `dataset/grids.yaml`, design with no realism claim, compiled into `build/<set>-single/` with one manifest per set; built in every CI run (9.21 decision 8); the experiment spec selects files from a pinned manifest by its axes, read by manifest join, not as records columns (9.21).
- Sources: SX-0312 (TODO 9.15 line (from the 2026-10-11 audit), `_dev/TODO.md:179`)
- Cross-ref: W-0718
- Notes: Checked at HEAD: the five manifests hold 480, 720, 24, 272 and 66 artifacts; `dataset/README.md:14–18`. 188 of the generated files hold child-targeted WAKEs (W-0718), so the loader refuses them too. `build/` is 6.8 GB with the generated layer (9.20 D10 as the 9.21 TODO entry records).

### W-0717 · final-memo
- At: new
- Change: Name 9.23 D16's rule to 인경민 and 박이안: no program runs out — every segment-bound program now ends blocked, on a trailing WAIT (a wake-driven program: N wakes meet N + 1 WAITs) or a trailing TIMER (a timer-driven program: the next tick at or past the depart) or an unbounded LOOP, and is removed by its pinned depart; every task without a pinned depart, top-level or spawned, ends with EXIT; the canonical lint enforces it. The simulator's reading of a run-out program as exited (`simulator/src/sim.cpp:662`) with a second `task_end` at the depart (`on_depart`, `:838–845`) no longer arises in the data.
- Final word: 9.23 D16 (no program runs out, 2026-10-15, by 인지오's decision), enforced by 9.23 D14's canonical lint: a segment-bound program completes with the blocking step its loop takes next — a wake-driven program a WAIT on its last wake's channel, a timer-driven program the next TIMER, whose tick falls at or past the depart — so it ends blocked (WAIT, TIMER or an unbounded LOOP) and the depart removes it; a task without a pinned depart, top-level or spawned, ends with EXIT. Nothing new executes: the CPU, the wakes and the ticks inside the span are unchanged, every artifact's bytes change (re-blessed by 9.23 D17). Before it, 7,400 segment-bound programs ran out (240 over the core set and variants, 7,160 over the generated layer): 6,215 wake-driven gained a trailing WAIT, 745 timer-driven a trailing TIMER, 440 resident single-WAIT programs and 5,559 unbounded-LOOP programs unchanged (9.23 D16, D17). Not a TIMER-rule (backlog-versus-skip) item.
- Sources: SX-0375 (TODO 9.15 line (from 9.23 D16), `_dev/TODO.md:179`); SX-0646 (9.23 D16, `task-9.23-guidebook-findings/changelog.md:150`)
- Notes: Checked at HEAD: `simulator/src/sim.cpp:662` (`if (t.pc >= t.prog.size()) { t.st = State::Done; return; }`), `:838–845` (`on_depart` emits `task_end` reason depart). The interpretation contract's §5 and the simulator guide's §4½ edits are 9.23 D16's own doc hand-offs, other groups' rows.

### W-0718 · final-memo
- At: new
- Change: Tell 인경민 the loader must resolve a WAKE target among spawn-table children: the rebuilt build trees wire each object job's members with WAIT/WAKE in parent-child order (9.6 D19), so spawned children wake children, a use the format allows and the loader refuses — `simulator/src/sim.cpp:876` dies with 'WAKE target is not a top-level task', its id map filled from `arrive` events only (`:899–905`), spawn-table programs compiled against it (`:917`). Refused: five core files — `c1-compile` and `c7-compile` (judging), `c3-workday`, `c4-compile`, `c6-dual` (reporting); the eight compile variants the RQ0 gate spec runs (`c1-compile` and `c7-compile` at `@corner-high`, `@corner-low`, `@venue-x0.8`, `@venue-x1.25`); 188 generated files (transition grid 60, return grid 90, distractor grid 32, familiarity ladder 6). Counts: 43,620 child-targeted WAKEs each in `c1-compile`, `c3-workday`, `c4-compile`, `c6-dual`, 25,269 in `c7-compile`; 855,150 over 201 of the 1,691 artifacts. The dataset keeps the usage: 9.23 D14's canonical lint checks every spawned WAKE target resolves.
- Final word: The 2026-10-10 dataset audit's blocker 1 ('Blockers for the RQ0 run (outside the dataset)'), unchanged at HEAD: the reference simulator's loader resolves a WAKE target against top-level `arrive` ids only, while 9.6 D19 (the object job in the frozen format: six spawn-table entries per job, woken in the job's parent-child order) has children wake children; the schema allows any `task_id` as a target, the contract's prose example shows only top-level targets, and the heads-up memo promised the input format unchanged — the usage is new and 인경민 was not told. 9.23 D14 (by 인지오's decision, 2026-10-15) made the canonical lint resolve a spawned child's WAKE targets as a top-level task's, so the dataset keeps the usage and the fix is the simulator's. The 9.15 TODO line routes the refusal to the final memo (`simulator/src/sim.cpp:874-904`; 9.6 D19).
- Sources: SX-0309 (TODO 9.15 line (from the 2026-10-11 audit), `_dev/TODO.md:179`); SX-0685 (audit 2026-10-10 blocker 1, `jioh/2026-10-10-dataset-audit-before-9.15.md:18`); SX-0785 (record-gaps §1 item 9, `jioh/2026-10-14-record-gaps-and-doc-staleness-for-9.15.md:19`); SX-0887 (guidebook dataset vol-01 open note (§7.2), `dataset/01-the-big-picture.md:1252`); SX-1132 (guidebook dataset vol-08 open note (§7.6), `dataset/08-decision-chronicle.md:1009`)
- Cross-ref: W-0735; W-0774; W-0743
- Notes: Counted at HEAD on `dataset/build/` (2026-10-15): every WAKE in a spawned program targets a spawned child, none a top-level task; the 855,150 equal 9.23 D14's count of WAKEs in spawned programs; the flap-stress set holds none. The audit recorded the stage-U binary's refusal on `c7-compile` (exit 2, 'WAKE target 이 최상위 태스크가 아니다: build.j1.mkdir'). The dataset guidebook's vol-08 note says 인경민's 2026-10-10 memo put the fix under 'Implementation owed'; that line (`simulator/memo/memo_261010.md` Part E/F, 'the loader reads the wake's `target`') concerns the external `wake` events' `target` field, not WAKE-instruction resolution among spawned children. Whether a heads-up already went to 인경민 is W-0735. The orchestrator's `WAIT children:<id>` is a separate open matter (W-0743).

### W-0719 · final-memo
- At: new
- Change: Tell 인경민 the simulator must load core files up to 187,601,795 B (about 187.6 MB, `c6-dual`, the largest), the core set 678,172,716 B (about 678 MB) over 51 files, as of the last re-bless (9.23 D17), in place of 9.13's 190 MB and 681 MB; the 78 variants and the 1,562 generated files are further sets.
- Final word: 9.13 spec decision 11 (the measured size handed to 9.14 and the final memo) and 9.13 D7 / reads R4 (190 MB, `c6-dual` measured at 189.8 MB, the set 681 MB; 2026-10-09), superseded in value by 9.23 D10 (2026-10-14: `c6-dual` 187,601,756 B, the core set 678,168,083 B) and then 9.23 D17 (2026-10-15, the last re-bless): `c6-dual` 187,601,795 B, the core set 678,172,716 B over 51 files. 9.23 D8 hands 'the final memo's file-size row (D10's sizes; the "190 MB … 681 MB" are 9.13's)'; the 9.15 TODO line's 9.23 segment names 187.6 MB and 678 MB.
- Sources: SX-0250 (TODO 9.15 line (from 9.13 D2, D4, R4), `_dev/TODO.md:179`); SX-0363 (TODO 9.15 line (from 9.23 D8, D10), `_dev/TODO.md:179`); SX-0545 (9.13 D7, `task-9.13-rebuild/changelog.md:56`); SX-0546 (9.13 reads R4, `task-9.13-rebuild/reads.md:61`); SX-0615 (9.23 D8, `task-9.23-guidebook-findings/changelog.md:80`); SX-0680 (9.13 spec decision 11, `jioh/task-9.13-rebuild.md:61`)
- Notes: Verified on disk at HEAD (2026-10-15): `dataset/build/coreset-single/c6-dual.workload.json` is 187,601,795 B and hashes to its `dataset/build.manifest.json` entry (`883bf5c9…`); the 51 core artifacts sum to 678,172,716 B; next largest `c1-transcode` 152,752,546 B. Re-read at the memo step if a later re-bless moves them. A cost note the memo may carry beside the size: `c6-dual`'s records are 14.5 million rows a run and its trace about 42 million lines (9.14 changelog, Phase 10 hand-offs).

### W-0720 · final-memo
- At: new
- Change: Name the executor conformance items still owed before the RQ0 run, each with its contract source: (a) a `ready` line at every completion of a blocking primitive, at zero wait when it did not block (`docs/harness/metrics.md` §11 item 1, line 306; the 2026-09-07 trace-clarifications memo §4); (b) the TIMER skip rule (the 2026-10-07 TIMER memo; 9.11 D3, D17); (d) `batch_bandwidth_cap` read and applied as a work-conserving ceiling on the batch class (the 2026-09-09 batch-class memo); (e) the strict idle class under every algorithm (the 2026-10-08 declared-class memo). Say that (c), a switch into MLFQ as a cold start with a same-algorithm entry letting the granted slice finish, and (f), the chain's woken stages in EDF's deadline class, are in the code, and that the run does not start until each is shown on the hand fixtures (`harness/experiments/rq0-gate.yaml:323–342`).
- Final word: The RQ0 gate spec's `simulator-conformance` statement (`harness/experiments/rq0-gate.yaml:323–342`, 9.14 decision 1; RQ0 is the gate experiment): before the RQ0 run the simulator must show, on the hand fixtures replayed with their traces compared line by line, (a) the zero-wait ready line, (b) the TIMER skip rule, (c) a switch into MLFQ as a cold start and a same-algorithm entry letting the granted slice finish, (d) `batch_bandwidth_cap` as a work-conserving ceiling, (e) the strict idle class, (f) the chain's woken stages in EDF's deadline class; the run does not start until each is shown. The code at HEAD (`simulator/src/sim.cpp`, last commit `6bf9d850`, 2026-10-10) implements (c) and (f) and owes (a), (b), (d), (e), as the 2026-10-10 audit's blocker 2 found.
- Sources: SX-0310 (TODO 9.15 line (from the 2026-10-11 audit), `_dev/TODO.md:179`); SX-0688 (audit 2026-10-10 blocker 2, `jioh/2026-10-10-dataset-audit-before-9.15.md:19`); 9.15 spec decision 9 (`jioh/task-9.15-docs-memos-and-guidebook-corrections.md:50`); 9.15 spec decision 13 (`jioh/task-9.15-docs-memos-and-guidebook-corrections.md:66`)
- Cross-ref: W-0714; W-0758
- Notes: Checked at HEAD: (a) a WAIT satisfied from a mailbox or a passed TIMER continues with no `ready` line (`sim.cpp:675–678`, `:686–691`), and `advance()` re-enqueues with cause `arrive` (memo_261010 Part C); (b) `sim.cpp:675` consumes overdue ticks at once (backlog); (d) no occurrence of `bandwidth` in `sim.cpp` (memo_261010 Part A item 4, 'not implemented'); (e) no occurrence of `declared_class`; (c) U1/U2 at `sim.cpp:44–52`, `:205–208`, `:589–605`, shown against the `mock-switch` trace (memo_261010 Part B); (f) B2 periodic class with the waker's deadline carried down the chain (`sim.cpp:34–38`, `deliver()`), answered 2026-10-10. The gate statement's own sentence '(f) the simulator does today; the others its owner holds as owed' predates the U port and is logged for 인지오 (W-0758). The assembly's spec-derived line (9.15 spec decision 9: the skip rule and zero-wait `ready` line owed) overlaps (a) and (b). memo_261010 Part A item 6 still lists a starvation safety net as owed on the simulator's side; 9.12 D114 records that no executor starvation bound is planned (9.11 D7 took no executor net; 9.11 D19 reconsiders one with 인경민 only if the dry runs show waits near 30 s) — the memo can say so. It carries 9.15 spec decisions 9 and 13: the final memo names the simulator's TIMER skip rule (item (b)) and the zero-wait `ready` line (item (a)) as owed; the docs keep the backlog rule until the skip rule lands (the Phase 10 TIMER line). Amended 2026-10-16 (W-0758's answer): the list gains (g), an orchestrator's `WAIT children:<id>` completed when the last child it spawned ends and without blocking when none is live (W-0743), owed by the simulator today. Per 인지오's answer to the frozen-contract question (work list, "Questions from the waves", K05, 2026-10-16, (c)): (g) is asked as a proposal for 인경민's agreement — the contracts carry it as proposed, in force once agreed, as W-0736's rule; the freeze over bound values and the release map are stated as in force, binding the dataset's side alone. Amended 2026-10-17 (인지오's answer (c) to K17's question, work list "Questions from the waves"): the list gains (h), the simulator run through the invocation contract (`docs/data-contracts.md` §11, contract 10: `--workload`, `--schedule`, `--out-trace`, the trace written to that file), as the RQ0 gate spec's `simulator-conformance` now states it; the simulator at `6bf9d850` takes its inputs positionally and prints the trace to stdout (`sim.cpp` `main`; its owner's `notes.md` gap 7, memo_261010 Part F), so (h) is owed.

### W-0721 · final-memo
- At: new
- Change: Ask 인경민 to re-run their simulator regression check, last run on the 24-file pre-rebuild set, on the rebuilt core set (51 files) and its 78 variants once the loader accepts child-targeted WAKEs, and with it their own backlog item: re-measure EDF on the rebuilt `c1-gaming` and `c2-p2b` (whether the p2 pair's two EDF rows still differ on `game.chain.1`'s frames).
- Final word: The 2026-10-10 dataset audit's blocker 3: the last simulator regression check ran on the 24-file pre-rebuild set (`simulator/memo/memo_261010.md` Part B 'all 24 coreset files', Part D1 '25 workloads (24 coreset files plus `mock-switch`)'); no later record shows a run on the rebuilt set. The audit routes it to no task; it is the simulator owner's work.
- Sources: SX-0689 (audit 2026-10-10 blocker 3, `jioh/2026-10-10-dataset-audit-before-9.15.md:20`)
- Cross-ref: W-0718; W-0722
- Notes: Checked at HEAD: no commit under `simulator/` after `6bf9d850` (2026-10-10); memo_261010 Part F lists 'Re-measure EDF after jioh's dataset rework' as 인경민's own item (also `simulator/notes/note-for-jioh-edf-chain-stage-class.md:63–65`). Five core files and eight variants are refused until the loader fix (W-0718).

### W-0722 · final-memo
- At: new
- Change: Point 인경민 to the prior table's restated gaming rows (`daemon/driver-table/prior.yaml:209–232`) and the pair review as the written form of the 2026-10-10 answer to 인경민's EDF note: the whole frame chain in EDF's deadline class, inheriting the head's deadline, the cap inert on the chain term, the gap against the boot MLFQ an EDF-against-MLFQ result, `c1-gaming` at `lane_share` 0.9 fitting the lane and `c3-evening` at 1.45 not, the download batch class; and name what that note left to re-check after the rebuild (whether the p2 pair's two EDF rows differ on `game.chain.1`'s frames, `c2-p2b`'s background now the unattended upgrade).
- Final word: 9.14 spec decision 8: the restated gaming rows are the reply to 인경민's EDF chain-stage note, carried by 9.15's final memo; 9.14 D5 restated the prior table's sentences on the rebuilt files. The note itself was answered 2026-10-10: stages 2–16 in EDF's deadline class, inheriting the waker's deadline, no code change (`simulator/notes/note-for-jioh-edf-chain-stage-class.md:57–65`).
- Sources: SX-0681 (9.14 spec decision 8, `jioh/task-9.14-consumer-rework.md:54`)
- Cross-ref: W-0721
- Notes: The note's 'Consequences' (lines 63–65) put the p2 re-check on 인경민's own backlog (W-0721).

### W-0723 · final-memo
- At: new
- Change: Answer 인경민's written-up questions to 인지오 (`simulator/memo/memo_261010.md` Part F, 'Questions for jioh — all written up'): TIMER backlog versus frame drop — the 2026-10-07 TIMER memo's skip rule (9.11 D3); `fork_cap` — 9.6 D19's answer (W-0764); mock-switch question 1 — the mock is wrong and the harness fixes it (W-0804, W-0765); question 2 — 인지오's answer once given (W-0736); question 3 — 9.23 D16's trailing WAIT (W-0766); and say that 인지오's three heads-up questions to 인경민 are answered (W-0702).
- Final word: The 2026-10-14 record-gaps audit §1 item 1 and the 2026-10-10 dataset audit's recommended order item 1 ('answer his three open questions'): 인경민's open questions to 인지오 are the TIMER backlog-versus-frame-drop note (answered 2026-10-07, before the audit), `fork_cap` (rationale, the absent field, critical-findings row B3) and mock-switch Q1–Q3 (`simulator/notes/note1010.md`); 인지오's three questions to 인경민 (heads-up memo §4) are LOTTERY's draw, the EDF chain-stage class and a keystroke during RUN.
- Sources: SX-0750 (record-gaps §1 item 1, `jioh/2026-10-14-record-gaps-and-doc-staleness-for-9.15.md:11`)
- Cross-ref: W-0804; W-0702; W-0735; W-0764; W-0765; W-0736; W-0766
- Notes: State of each at HEAD after this merge: answered — TIMER (2026-10-07 memo), `fork_cap` (9.6 D19, `_dev/research/jioh/task-9.6-compile/changelog.md:103–109`; `dataset/tools/wlc/compiler.py:659–661`, `:699`, `:787`; `simulator/src/sim.cpp:921`), mock-switch Q1 (W-0765), Q3 (9.23 D16), LOTTERY (`simulator/src/sim.cpp:328–366`), EDF (2026-10-10 note), keystroke (`docs/harness/metrics.md:307`); open — mock-switch Q2 (W-0736). Also on 인경민's side and not in this list's rows: 인경민's reply to 인지오's three boot-default questions (`docs/memos/2026-09-11-boot-default-from-ostep.md` §5), which memo_261010 Part F ('Ours to decide') records as 'Q1 and Q2 answerable now; Q3 waits on the safety net'.

### W-0724 · final-memo
- At: new
- Change: Ask 박이안, as a change to a frozen contract (the recognition log, `docs/data-contracts.md` §8; the freeze rule §13 needs all three), whether the recognition log keeps the formatted prompt, and how the chat template's inserted date (Llama 3.1's "Today Date") is fixed or recorded, so that one telemetry snapshot is one input on every day.
- Final word: 9.12 D52 with 9.14 spec decision 11 and its hand-off table (`_dev/research/jioh/task-9.14-consumer-rework/changelog.md:74`): the recognizer's prompt fixes or records what its chat template inserts — Llama 3.1's "Today Date" — so the same snapshot is the same input on every day, and the recognition log keeps the formatted prompt; to 박이안 through 9.15's final memo, as a frozen-contract question. D52's third clause — Layer 1 (the recognition-accuracy measurement)'s consistency measure states its hardware — goes to the Layer-1 experiment spec (the Phase 10 line, `_dev/TODO.md:192`).
- Sources: S12-256 (9.12 D52, `task-9.12-related-work-prose/changelog.md:833`); SX-0273 (TODO 9.15 line (from 9.14 decision 11), `_dev/TODO.md:179`); SX-0562 (9.14 spec decision 11 (hand-off table, 9.12 D52), `task-9.14-consumer-rework/changelog.md:74`); SX-0682 (9.14 spec decision 11, `jioh/task-9.14-consumer-rework.md:66`)
- Notes: Checked at HEAD: `docs/data-contracts.md` and `daemon/` hold no 'formatted prompt' or 'Today Date' text (the raw rows' grep), so the question is open.

### W-0725 · final-memo
- At: new
- Change: List the memos still open after the memos chunk, each with its ask and its owner, as their header lines state them.
- Final word: 9.15 spec decision 13: beyond the TODO line's items the final memo carries the memos still open, the simulator's skip rule and zero-wait `ready` line as owed, and the licences chosen.
- Sources: 9.15 spec decision 13 (`jioh/task-9.15-docs-memos-and-guidebook-corrections.md:66`)
- Notes: Depends on the memos chunk's header lines.

### W-0726 · final-memo
- At: new
- Change: State the licences chosen: the code under MIT (root `LICENSE`), the dataset's data and release assets under CC-BY-NC-SA-4.0 (`dataset/LICENSE`), holders Jioh In, Kyungmin Inn and Ian Park, SWELL-KW credited for the stimulus streams.
- Final word: 9.15 spec decision 13: beyond the TODO line's items the final memo carries the memos still open, the simulator's skip rule and zero-wait `ready` line as owed, and the licences chosen.
- Sources: 9.15 spec decision 12 (`jioh/task-9.15-docs-memos-and-guidebook-corrections.md:62`)
- Notes: —

### W-0825 · final-memo
- At: new
- Change: Propose to 인경민 and 박이안 that the claim the experiment puts at risk be stated in scheduling-score terms: the configuration selected from the model's reading of the process names scores better than the strongest name table's on the RQ0 judging files; recognition accuracy (RQ1) becomes the account of the gap, and the RQ5 ladder's share of perfect recognition's gain the model captures — (fixed − model) / (fixed − perfect recognition) — the headline. A proposal: the claims document is the three owners'; 9.15 does not apply it.
- Final word: 인지오, 2026-10-16 (answering W-0753's discussion): the paper's weight belongs on whether the model's recognition improves scheduling. Grounds on record: the claim at `docs/research-claims.md:23–25`, as 9.12 D88 and D6 restate it (W-0392, W-0393), still reads 'recovers the difference', a recognition criterion, and ## The load-bearing experiment calls the claim 'demonstrated by construction' when the model separates the pair; 9.14 decision 2 and 9.23 D9 measured P1's headroom on `c2-p1b` as zero (the indexer's own `SCHED_IDLE`, below every row), so P1's scheduling headroom is `c2-p1a`'s alone and P2 (`c2-p2a`, `c2-p2b`) is the one label pair with both sides judged.
- Sources: 인지오's answer of 2026-10-16; `harness/experiments/rq0-gate.yaml:55–61` (judging and reporting lists); 9.23 D9 (`task-9.23-guidebook-findings/changelog.md:82`)
- Cross-ref: W-0392; W-0393; W-0400; W-0752; W-0753
- Notes: The RQ5 ladder is `docs/research-claims.md` ### RQ5's illustrative table (fixed, name table, variant A, perfect recognition, perfect config).

### W-0826 · final-memo
- At: new
- Change: Tell 인경민 and 박이안 the 'What is not claimed' entry 9.15 adds to `docs/research-claims.md`: the scheduling result is not claimed to transfer to another CPU or another machine's configuration — every CPU value one AMD EPYC 7763 core's on a hosted runner (Xvfb, no GPU, no sound device, no human); another CPU changes each program's speed by its own factor (a Xeon Platinum 8573C: `cc1` 0.72×, `fixdep` 0.50× the EPYC's time), which the venue variants' common factor of 0.8–1.25 does not reproduce; recognition reads no CPU value.
- Final word: 인지오's answers to W-0752 and W-0753 (2026-10-16).
- Sources: W-0752; W-0753; `docs/workload/measurement-overview.md` §11; `dataset/variants.yaml:35–44`
- Cross-ref: W-0825
- Notes: —

### W-0827 · final-memo
- At: new
- Change: Propose to 인경민 and 박이안 that the `render` gloss in `docs/recognition-vocabulary.md` §1 widen from 'an offline 3D/graphics render' to 'an offline render — a 3D scene or a video project rendered to a file'; no label or file changes; applied with a §5 entry once agreed (the vocabulary's §4: a change to a mode is an all-three decision).
- Final word: 인지오's answer to W-0432 (2026-10-16).
- Sources: W-0432; `dataset/tools/meas/llm/prompt.json` (the 9.12 stand-in prompt carrying §1's menu verbatim); `kdenlive` in `docs/references.md` (the render dialog starts `kdenlive_render`)
- Cross-ref: W-0825
- Notes: Every render segment (`c1-render`, `c7-render`, `c2-p3a` segment 1, the generated files over the render mode) binds Kdenlive's export (9.10 D10).

### W-0828 · final-memo
- At: new
- Change: Propose to 인경민 and 박이안 the trace rule for an MLFQ slice expiring with no other task runnable: one continuing occupancy — the holder demoted (`x_mlfq_level`) and kept on the lane, no `run_end(preempt)`/`run_start` pair — answering 인경민's mock-switch Q2 (`simulator/notes/note1010.md`); 인경민 implements it with the RUN→RUN fix (`simulator/memo/memo_261010.md` Part C), one change to the MLFQ baseline traces; the harness mock stands. Written into the metrics doc and the interpretation contract with a `docs/data-contracts.md` §14 entry once agreed.
- Final word: 인지오's answer to W-0736 (2026-10-16).
- Sources: W-0736; Linux v6.12 `kernel/sched/core.c:6655` (`__schedule()`: no switch counted when `prev == next`)
- Cross-ref: W-0723
- Notes: The CPU each task receives is the same under either reading; `preempt_count` is reported, in no scored term.

### W-0829 · final-memo
- At: new
- Change: Tell 인경민 and 박이안 two renamings in the docs, no content with them: the research-claims chain's links are 'link 1'–'link 7' (seven links; the doc said 'six'), the core set's file groups keeping C1–C7; the dataset's layers are named (the archetype library, the scenario catalog, the timelines), 'Layer 1/2' keeping the evaluation layers.
- Final word: 인지오's answer to W-0742 (2026-10-16).
- Sources: W-0742
- Cross-ref: W-0825
- Notes: —

### W-0894 · final-memo
- At: new
- Change: Tell 인경민 that the simulator guide's wording quoted by `simulator/src/notes.md` §4 gaps 1 and 3 is restated: §5 now names the one cap the configuration sets, `batch_bandwidth_cap`, a work-conserving ceiling on the batch class, not yet implemented — gap 1 stays owed as conformance item (d) (W-0720); §9.2 is closed on TIMER's t₀ being the arrival, which the simulator already does (`simulator/src/sim.cpp:674`, `:734–737`) — gap 3 owes nothing. No edit to 인경민's tree.
- Final word: drafted as option (b) of K09's question from the waves; 인지오 confirms or drops it at the final memo's review (9.15 spec decision 13).
- Sources: `simulator/src/notes.md` §4; `docs/simulator/simulator-guide.md` §5, §9.2; W-0446; W-0448; W-0869; 인지오's answer to K03's t₀ question (2026-10-16)
- Cross-ref: W-0720
- Notes: —

### W-0978 · final-memo
- At: new
- Change: Tell 인경민 and 박이안 the 2026-10-17 entry of `docs/data-contracts.md` §14: the drain (a switch out of MLFQ, EDF or LOTTERY stamped while a task holds the lane applies the next time the lane is free) and the index order (the entries apply in list order, one stamped while a switch drains — a same-algorithm one included — waiting behind it and applying at the same instant, after it) are contract rules, in force as written; the reference simulator already applies both (its U3, since 2026-10-10); the 2026-09-09 rule (the switch memo's §7: a same-algorithm entry applied at its stamped time) is amended so.
- Final word: 인지오's answer (c) of 2026-10-17 to W-0949 (in force as written, the phase's final memo carrying it to 인경민 and 박이안) and answer (b) of 2026-10-17 to F3 (M2) (a final-memo row telling 인경민 and 박이안 the 2026-09-09 rule is amended so).
- Sources: `logs/N1.md` ## Rows for other chunks (X5); `docs/data-contracts.md` §7, §14 (the 2026-10-17 entry); `simulator/src/sim.cpp:570–580`, `:823–836`; `simulator/memo/memo_261010.md` Part B (U3)
- Cross-ref: W-0720; W-0949; W-0975
- Notes: found in N1, one row with the F3 (M2) answer's final-memo row. Nothing is owed by the simulator.

## Also aimed at the final memo, not for drafting from this list

- W-0727 · waits on 인지오 — Should the final memo ask 인경민 to commit their 2026-10-06 note? What the records say: 9.11 D33 records only that the note — `c3-evening`'s game chain at `lane_share` 1.45 never drains, nearly every frame misses under every…

### W-1001 · final-memo
- At: new
- Change: Tell 인경민 the harness reads the MLFQ boost timer as the reference simulator runs it: restarted at every applied MLFQ entry, a same-algorithm one included (`simulator/src/sim.cpp:597`, `:603`, `:210`) — `boost_window` lays the grid from each applied entry (`docs/harness/metrics.md` §6.10, §11 item 9; the harness's second step, 2026-10-17), so the open row of `simulator/memo/memo_261010.md` Part B ("Still open"; the "ours to decide and write down" table, current behaviour "restarts") can be written down as decided.
- Final word: 인지오's answer (b) of 2026-10-17 to F3 (M1) (work list, "Questions from the waves").
- Sources: `logs/F3.md` (M1); `logs/B3-harness.md` item 2.
- Cross-ref: W-0978; W-0720

### W-1002 · final-memo
- At: new
- Change: Tell 인경민 the reference simulator applies and traces config-schedule entries stamped at or after the workload's end (`load_schedule` keeps every entry, `set_schedule` queues each, `run` processes every event; `simulator/src/sim.cpp:540–545`, `:937–967`), against `docs/data-contracts.md` §7's End rule (frozen 2026-09-06: such entries are ignored); no number moves, the harness dropping `config_applied` lines at or after `T_end` (`harness/tools/harness/primitives.py:114–115`; `docs/harness/metrics.md` §4). The contract and the harness are unchanged.
- Final word: 인지오's answer (b) of 2026-10-17 to N1 (work list, "Questions from the waves").
- Sources: `logs/N1.md` (its mismatch).
- Cross-ref: W-0720; W-0978
