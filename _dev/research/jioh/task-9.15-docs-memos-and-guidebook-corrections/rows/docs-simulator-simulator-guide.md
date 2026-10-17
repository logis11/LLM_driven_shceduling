# Work-list rows — `docs/simulator/simulator-guide.md`

Chunk K09, Simulator and daemon docs (wave 2). 7 open rows. The file has 321 lines at `d5cc7711`.

### W-0442 · applied
- At: `docs/simulator/simulator-guide.md` ## 1 The machine at a glance, line 37 ("whether a schedule came from the oracle, a whitelist, or a model"); ## 11 A question worth keeping, line 317 ("the oracle, whitelist, and fixed conditions")
- Change: Name the two name-table conditions (`shipped_catalogue`, `strongest_name_table`) in place of "whitelist" in both sentences — e.g. "from the oracle, a name table, or a model" and "the oracle, name-table and fixed conditions".
- Final word: 9.12 D6 as amended by D91, D105, D109 and D115 (D1 for the Game Mode clause), applied to every frozen list by 9.14 D3 (the 9.14 spec's decision 7): the `whitelist` condition becomes two. The shipped-catalogue condition (`shipped_catalogue`) reproduces the CachyOS catalogue (`ananicy-rules` at `03ef03fb`) as CachyOS installs and enables it with ananicy-cpp, matched by the basename of each process's `argv[0]`, untruncated (D105); it answers RQ2 (research question 2, "does that reading beat what shipping systems do?"). The strongest-name-table condition (`strongest_name_table`) is a rule list in the catalogue's design covering the software the dataset presents as known, with no rule for Family 3's unregistered software or the invented names of familiarity tiers 4–5; it carries the paper's claim (D115), is the condition expected to score perfectly on the C1 (the single-situation calibration group) files, and fails structurally on world knowledge. "A faithful reproduction of what shipping systems do today" and "the whitelist approach real operating systems currently use" are restated to the two conditions (D91); neither is "a faithful reproduction of what Windows/macOS Game Mode does today" (D1); on ananicy-cpp's key the catalogue keys 19 of the 35 bound names and every name in only 7 of 50 files (D109).
- Sources: S12-044 (9.12 D6, `task-9.12-related-work-prose/changelog.md:114`); SX-0142 (TODO 9.15 line (from 9.12 D6), `_dev/TODO.md:179`)
- Notes: Condition ids in code: `harness/tools/harness/evaluator.py:47` CONDITIONS = fixed, random, shipped_catalogue, strongest_name_table, llm_vocab, llm_algo, llm_full, oracle; `harness/guards/guard-spec.yaml:126`. Minor: the sentences only list recognizer kinds.

### W-0443 · applied
- At: `docs/simulator/simulator-guide.md` ## 3, ### Input 1 — the workload's events: the arrive illustration lines 60–67 (`"fork_cap": 8`) and its reading at line 70 (the editor's "alternating" waits and CPU bursts)
- Change: Optionally note beside the illustration that compiled files carry larger caps (`c1-compile`'s `make`: `fork_cap` 48) and that a measured editor wakes mostly on its own timer components (`timer:<id>`), the alternating keystroke-wait picture being the illustration's simplification.
- Final word: Record-gaps §2 item 13 (compiled shapes against prose), checked at HEAD: `c1-compile`'s `make` carries a 17,448-entry spawn table (six processes per object job) and `fork_cap` 48; in every compiled interactive file the timer-component wakes (`timer:<id>`) outnumber the keystroke wakes (`input:<id>`) by one to two orders of magnitude (`c1-dev` 6,456 vs 186; `c1-office` 3,064 vs 270; `c1-mail` 5,371 vs 35); the periodic entries compile to LOOP bodies with no wake events.
- Sources: SX-0835 (record-gaps §2 item 13, `jioh/2026-10-14-record-gaps-and-doc-staleness-for-9.15.md:38`)
- Cross-ref: W-0444
- Notes: Low weight: the arrive illustration and §4½'s miniature are illustrations. The FORK passages naming `c1-compile`'s cap and children are row W-0444.

### W-0444 · applied
- At: `docs/simulator/simulator-guide.md` ### `{ "op": "FORK" }` and `{ "op": "EXIT" }`, line 149 ("e.g. 100 `cc1` entries"; "a `fork_cap` (e.g. 8, as in `make -j8`)") and the cap's worked example, line 151 ("`make` has `fork_cap: 8`"); ## 7, the "harder targets" paragraph, line 259 ("`make` + 100 `cc1` children at cap 8")
- Change: State `c1-compile`'s compiled shape at :259: 17,448 spawn-table entries (2,908 object jobs × six members: `sh`, `gcc`, `cc1`, `as`, `fixdep`, `rm`) at `fork_cap` 48 (the timeline's `parallelism_cap` 8 × 6); :149's 100 `cc1` entries and cap 8 and :151's worked example may stay as illustrations if labelled so.
- Final word: 9.6 D19–D22 and D25 (the three measured archetypes, 2026-09-19; D19 amended by D20, D22 corrected by D25; folded in at D31): `compiler-child` is the six-member object job (`sh`, `gcc`, `cc1`, `as`, `fixdep`, `rm`) with one measured quantile table per (role, structural step); `build-orchestrator` carries the measured `dispatch_overhead` table and six spawn-table entries per object job, the compiled `fork_cap` = parallelism_cap × 6 (`dataset/tools/wlc/compiler.py:699`); `cpu-batch` is a batch loop (RUN a measured run, SLEEP the block after it) whose tables the `program` binding chooses (at HEAD `python3` and `kdenlive_render`, `dataset/archetypes.yaml:884–964`). All three carry `category_source: meas`. `c1-compile` binds 2,908 object jobs at cap 8: spawn table 17,448 entries, `fork_cap` 48.
- Sources: SX-0026 (TODO 9.15 line (from 9.6, the three archetypes), `_dev/TODO.md:179`)
- Cross-ref: W-0443
- Notes: Checked at HEAD: `dataset/build/coreset-single/c1-compile.workload.json` (its SHA-256 equals `dataset/build.manifest.json`'s entry): `editor`/`code` arrives at 0 with depart 1,594,000,000 µs; `build`/`make` at 2,000,000 µs, `fork_cap` 48, a 17,448-entry spawn table, 2,908 of each of `sh`, `gcc`, `cc1`, `as`, `fixdep`, `rm`, all `declared_class` normal; `make`'s program ends `WAIT children:build`, `EXIT`. :149 is not named by the raw row but carries the same "100 `cc1` entries". The arrive illustration's `fork_cap: 8` (:66) is row W-0443.

### W-0445 · applied
- At: `docs/simulator/simulator-guide.md` ## 4½ A complete worked run, event by event, lines 156–186 (the editor's program lines 163–164, `[WAIT, RUN 3000, WAIT, RUN 2000]`; the table's 32000 row, line 182, "next instruction WAIT → blocks (no more wakes will come)")
- Change: Give the editor's program its trailing `{ "op": "WAIT", "channel": "input:e" }` after the second RUN, so the 32000 row's "next instruction WAIT → blocks" holds, and say in a sentence that a segment-bound program always ends blocked (WAIT, TIMER or an unbounded LOOP) and its depart removes it.
- Final word: 9.23 D16 (no program runs out, 2026-10-15, not amended), enforced by the 9.23 D14 canonical lint: the compiler completes a segment-bound program with the blocking step its loop takes next — a wake-driven program a trailing WAIT on its last wake's channel (N wakes meet N + 1 WAITs), a timer-driven program the next TIMER, whose tick falls at or past the depart — so it ends blocked (WAIT, TIMER or an unbounded LOOP) and the depart removes it; the resident single WAIT is unchanged; a task without a pinned depart, top-level or spawned, ends with EXIT. Nothing new executes inside the span. Not a TIMER-rule (backlog-versus-skip) item.
- Sources: SX-0373 (TODO 9.15 line (from 9.23 D16), `_dev/TODO.md:179`); SX-0644 (9.23 D16, `task-9.23-guidebook-findings/changelog.md:150`)
- Notes: Not a TIMER-rule row (spec decision 9). §6's trace of the same run (around :224) does not change: the trailing WAIT executes no CPU. The example's channel `input:e` against the id `editor` differs from the compiler's `input:<task id>` form (`input:editor`, as §3's own wake example at :75 shows); the editing agent may align it while there.

### W-0446 · applied
- At: `docs/simulator/simulator-guide.md` ## 5 The scheduler seat, the "Needed eventually …" paragraph, line 210 ("and per-class bandwidth caps, enforced by the executor regardless of what any config says")
- Change: Restate the clause to the one cap the configuration sets — the batch class's `batch_bandwidth_cap`, the driver table row's under every condition but `llm_full` (unset or 0.05–0.95 there) — which the executor is to enforce, not yet implemented; the harness's 30 s `starvation_floor` guard judges the run.
- Final word: 9.12 D30 as amended by D79 and D114: "It cannot remove starvation protection" leaves §4.7's list; §4.7 states what holds — the executor has no starvation window; FIFO and EDF's deadline class have no horizon, so beside them an unset cap can leave a task waiting without bound, and an idle-class task waits behind other classes by design; MLFQ's boost can be lengthened to 10 s but not removed; a run in which any task waits more than 30 s fails the harness's `starvation_floor` guard, and on a run the RQ0 (research question 0: does configuration matter on these workloads at all) criterion reads that makes the verdict invalid. The batch class's bandwidth cap is one configuration field — the driver table row's under every condition but `llm_full`, unset or 0.05–0.95 there — which the executor is to enforce (not yet implemented). D79 restates the simulator guide's per-class caps to the one cap the configuration sets, "to be enforced". `:756` (인경민's team area) leaves 9.12's restatements (D114).
- Sources: S12-142 (9.12 D30, `task-9.12-related-work-prose/changelog.md:499`); S12-148 (9.12 D79, `task-9.12-related-work-prose/changelog.md:1221`); SX-0163 (TODO 9.15 line (from 9.12 D30), `_dev/TODO.md:179`); SX-0164 (TODO 9.15 line (from 9.12 audit D79), `_dev/TODO.md:179`)
- Notes: Checked at HEAD: `simulator/src/sim.cpp` reads `batch_bandwidth_cap` (the one real number its JSON reader parses, `simulator/src/mini_json.hpp:3`) and enforces no cap. Not a TIMER row.

### W-0447 · applied
- At: `docs/simulator/simulator-guide.md` ## 9 Questions the contract doesn't answer (yet), ### 9.1 A wake with no waiter, lines 275–277
- Change: Mark §9.1 answered: a wake with no waiter is held in the task's mailbox with depth, so the next WAITs complete at once (the simulator's step M; metrics doc §11 item 2), and drop it from the undecided list or mark it decided.
- Final word: The metrics doc's §11 item 2 (the trace contract's clarification, `docs/memos/2026-09-07-trace-clarifications-for-the-simulator.md`): wakes queue with depth — two wakes sent to a busy task complete its next two WAITs; the simulator implements it, a wake with no waiter going to a mailbox, never lost (`docs/harness/metrics.md:307`; `simulator/src/sim.cpp:25`, `:100`, step M). It also answers the heads-up memo's third executor question (a keystroke arriving while the editor runs).
- Sources: SX-0743 (record-gaps §1 item 1, `jioh/2026-10-14-record-gaps-and-doc-staleness-for-9.15.md:11`)
- Cross-ref: W-0448
- Notes: Not a TIMER row. §9's opening (:273, "none has a decided answer today") changes with §9.1 and §9.2 (row W-0448). The guide is written for 인경민; a short pointer is enough.

### W-0448 · applied
- At: `docs/simulator/simulator-guide.md` ## 9, ### 9.2 TIMER's t₀, lines 279–281 ("… the contract never says what **t₀** is … Pick the reading, confirm it …")
- Change: Close §9.2: t₀ is the task's first TIMER execution, as the simulator sets it (its decision D4); the dataset lint makes every TIMER-carrying program begin with its TIMER (since 9.13), so t₀ is the task's first dispatch; the harness reads it as the time of the first `ready(cause = timer_tick)` line (metrics doc §11 item 4).
- Final word: 9.11 D11 (2026-10-07) as scoped by D27 and D32, handed by D33: TIMER's t₀ is pinned to the task's first TIMER execution, as the simulator sets it (its decision D4; `simulator/src/notes.md` gap 3, "ours to pin, not a question"); since 9.13 the dataset lint enforces that a TIMER-carrying program begins, in execution order, with its TIMER, a LOOP head's body counting (`dataset/tools/wlc/linter.py:290–297`), so t₀ is the task's first dispatch and cannot come apart from the arrival silently; the harness reads it as the time of the first `ready(cause = timer_tick)` line (9.14 D1; `docs/harness/metrics.md` §11 item 4). At the committed build of 2026-10-08, 22 tasks carry a TIMER and 4 arrive mid-run (3 in `c3-evening`, 1 in `c6-fold`), all TIMER-first (D32).
- Sources: SX-0099 (TODO 9.15 line (from 9.11 D11), `_dev/TODO.md:179`); SX-0524 (9.11 D33, `task-9.11-scheduler-constants/changelog.md:452`)
- Cross-ref: W-0449; W-0447
- Notes: Not a backlog-versus-skip row, so not blocked, though the section's TIMER passages are (row W-0449). `simulator/src/notes.md:123–125` still records a t₀ conflict with metrics §11 item 4 that the metrics doc has since resolved (item 4 now says the first TIMER execution). The task counts are the 2026-10-08 build's; recount on the current build if quoted.

### W-0869 · applied
- At: `docs/simulator/simulator-guide.md` ## 9, ### 9.2 TIMER's t₀, lines 279–281 (W-0448's place)
- Change: When applying W-0448, write t₀ as 인지오 answers K03's t₀ question (## Questions from the waves): under the simulator's reading, t₀ is the arrival — the simulator executes a TIMER-first program's leading TIMER in the arrival step, busy lane or not — not W-0448's "so t₀ is the task's first dispatch".
- Final word: K03's fix round 1 (review round 2 passed): `simulator/src/sim.cpp:734–737` (`on_arrive`) and `:753–754` (`spawn`) call `step()` at the arrival and `:674` sets `timer_next = now_`; on `c3-evening` with no schedule `video` arrives 300,000,000, first `run_start` 300,010,000, first `deadline` due 300,033,348 = arrival + P. 9.11 D11 and D33 carry no first-dispatch wording; the first-dispatch reading is 9.14 decision 1's and its changelog's.
- Sources: `logs/K03.md` ## Fix round 1 (items 2–3; rows for other chunks), ## Review round 2
- Cross-ref: W-0448; W-0870; W-0183
- Notes: found in K03. Waits on 인지오's answer to K03's t₀ question. W-0448's Final word paraphrases 9.11 D11 as "so t₀ is the task's first dispatch"; D11's text does not say that (K03 fix round 1 item 3).

### W-0936 · applied
- At: `docs/simulator/simulator-guide.md` ## 9, ### 9.3 Simultaneous events (line 292), still written as an open question
- Change: Mark §9.3 decided, as §9.1 and §9.2 are: the simulator's rule D1, config entries first and then insertion order; the RQ0 gate spec's `executor-assumptions` (2) takes it; 인경민's formal reply is still pending (the declared-class memo §4 item 4).
- Final word: `simulator/steps/README.md:97` (D1, §9.3's same-instant order: kind priority, then insertion sequence, the config apply first); `simulator/memo/memo_261001.md` §6; `docs/harness/metrics.md` §11 item 3; `harness/experiments/rq0-gate.yaml` `executor-assumptions` (2); `docs/memos/2026-10-08-declared-scheduling-class.md` §4 item 4 (the formal reply asked).
- Sources: `logs/K17.md` ## Rows for other chunks (X2)
- Cross-ref: W-0447; W-0448
- Notes: found in K17. K09's file: a follow-up chunk. Line 113 ("your §9.3 tie-break rule decides"), §9.5 (`:302`) and the glossary's tie-break row (`:318`) refer to §9.3's rule.

### W-0985 · applied
- At: `docs/simulator/simulator-guide.md` §3, the switch paragraph's same-algorithm sentence, line 117
- Change: Add that under MLFQ the boost timer restarts at the applied instant, as on a switch into it. N3's drafted text: "under MLFQ the boost timer restarts at the applied instant, as on a switch into it (`simulator/src/sim.cpp:210`, `:597`)".
- Final word: 인지오's answer (b) of 2026-10-17 to F3 (M1) (the simulator's restart holds), which names no change in this guide; `simulator/src/sim.cpp:210` (`Mlfq::start` re-arms the boost at `now + boost_interval_us`), `:597` (`++pol_epoch_` voids the earlier timer). Waits on N3's question under "Questions from the waves".
- Sources: `logs/N3.md` ## Answers that land in this file (F3 (M1)), ## Fix round 1
- Cross-ref: W-0986; W-0988; W-0974
- Notes: found in N3, held back by its brief (reverted in its fix round 1). K09's file: a follow-up chunk, if 인지오's answer takes it. B3's log (not yet folded) lists the same site.

### W-0986 · applied
- At: `docs/simulator/simulator-guide.md` §3's schedule paragraph, line 115 ("unless it is a switch that drains (next paragraph)"); the glossary's config-application row, line 318 ("or, for a switch that drains, once the lane is free (§3)")
- Change: Line 318: "or, for a switch that drains and every entry stamped behind it, once the lane is free (§3)". Line 115, optional (F3's reviewer held it unneeded, line 117 already stating the queued entry): "unless it is a switch that drains, or is stamped while one drains (next paragraph)".
- Final word: 인지오's answer (b) of 2026-10-17 to F3 (M2) (the simulator's order holds), which names no change in this guide; `simulator/src/sim.cpp:574–577` (an entry queued while `pending_` is non-empty), `:825–828` (`dispatch` applies the queue in index order once the lane is free). Waits on N3's question under "Questions from the waves".
- Sources: `logs/N3.md` ## Rows found and applied in this file (R1, R2), ## Fix round 1
- Cross-ref: W-0985; W-0973; W-0949
- Notes: found in N3, held back by its brief (reverted in its fix round 1). K09's file: a follow-up chunk, if 인지오's answer takes it.

### W-0987 · applied
- At: `docs/simulator/simulator-guide.md` §6, the paragraph after the trace, line 255 ("its first `ready` line, if it is ever woken, is the wake that completes that WAIT")
- Change: Optional: scope the sentence to the case the code holds, the instruction after that WAIT settling on a RUN, e.g. "…, if it is ever woken and its next instruction is a RUN, is the wake that completes that WAIT"; the same change in metrics §11 item 5's wording (W-0981).
- Final word: `simulator/src/sim.cpp:800–806` (`on_unblock` advances past the WAIT and calls `step`; a following WAIT, SLEEP, EXIT, the program's end or a FORK at its cap leaves no `ready` line at that wake). True of every WAIT-first program in the core set today: WAIT then RUN, a LOOP whose body starts WAIT then RUN, and four lone-WAIT tasks no wake targets.
- Sources: `logs/N3.md` ## Review round 2 (non-blocking note 1)
- Cross-ref: W-0981
- Notes: found in N3's last review (optional). K09's file: a follow-up chunk.

## Also on this file, not for editing from this list

- W-0449 · blocked, simulator TIMER (on the spec's list) — ## 4 The instruction set, ### `{ "op": "TIMER", "period_us": P }`, lines 126–141 (the backlog sentence :127, "Worked example of the backlog…
- W-0450 · blocked, simulator TIMER (outside the spec's list) — ## 9, ### 9.4 Depart mid-anything, line 289 ("with backlogged TIMER ticks it never caught up on")
