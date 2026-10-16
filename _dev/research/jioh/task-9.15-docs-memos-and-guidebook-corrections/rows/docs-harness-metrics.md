# Work-list rows — `docs/harness/metrics.md`

Chunk K10, Harness guide and metrics (wave 3). 2 open rows. The file has 344 lines at `d5cc7711`.

### W-0479 · applied
- At: `docs/harness/metrics.md` ## 5 Records, line 67 ("One CSV file per trace (or per recognition log), every row self-contained, twenty-four columns.")
- Change: Restate "twenty-four columns" to twenty-five: the §5 tables already list all 25, `telemetry` (added 2026-10-11, 9.17) included.
- Final word: 9.14 D1 added the twenty-fourth column `skipped` (2026-10-09); 9.17 D4 (the telemetry shape through the harness, 2026-10-11) added the identity column `telemetry` after `boot_default`: `harness/tools/harness/records.py:19–23` COLUMNS holds 25, as does `harness/records/schema/records.schema.json`.
- Sources: merge finding (`harness/tools/harness/records.py:19`)
- Resolved at merge: Found while resolving the records' column count (row W-0466; raw row W-0466's notes saw it): `git log -L67,67:docs/harness/metrics.md` shows the line last changed in `cd3fd535` (9.14 D1, to "twenty-four"); 9.17 added the `telemetry` row at :78 without the count.
- Notes: —

### W-0480 · applied
- At: `docs/harness/metrics.md` ## 9 Normalisation and floors, the "Sensitivity." paragraph, line 281 ("The RQ0 gate spec pre-registers `fixed` under a sweep of nine alternative boot defaults")
- Change: Restate "nine alternative boot defaults" to ten — the top slice at 0.5, 0.7, 0.9, 1.2, 2, 3, 5, 14, 20 and 100 ms.
- Final word: 9.14 D7 (the RQ0 gate spec rewritten; the ten-point sweep, 2026-10-09), current in `harness/experiments/rq0-gate.yaml`: 19 judging files, K 10 (9.14 decision 2 as amended: the six idle-class files and `c7-mail` leave the judging set), g 0.5, N 100; the boot-default sweep at ten alternatives — the top slice at 0.5, 0.7, 0.9, 1.2, 2, 3, 5, 14, 20, 100 ms (9.11 D2's 0.7 for the 0.75 point; `ostep-slice-14000us` added by 9.14 D7).
- Sources: SX-0287 (TODO 9.15 line (from the 2026-10-11 audit), `_dev/TODO.md:179`); SX-0714 (audit 2026-10-10 docs-staleness additions (pre-registration numbers), `jioh/2026-10-10-dataset-audit-before-9.15.md:55`)
- Notes: `harness/experiments/rq0-gate.yaml` `boot_defaults`: primary `ostep`; alternatives `ostep-slice-500us`, `-700us`, `-900us`, `-1200us`, `-2000us`, `-3000us`, `-5000us`, `-14000us`, `-20000us`, `-100000us`. The hand-offs' :279 has drifted to :281.

### W-0870 · applied
- At: `docs/harness/metrics.md` §6.2, line 148 ("… fixes a task's first instruction, not its first dispatch, so a head arriving on a busy lane executes its first TIMER later than it arrives"); §11 item 4, line 309 ("so `t₀` is the task's first dispatch … later on a busy lane")
- Change: Once 인지오 answers K03's t₀ question (## Questions from the waves): under the simulator's reading, restate both to the arrival (the leading TIMER executes in the arrival step); under the harness mocks' reading, both stand.
- Final word: As W-0869: `simulator/src/sim.cpp:734–737`, `:674` execute the leading TIMER at arrival; the first-dispatch reading is 9.14 decision 1's.
- Sources: `logs/K03.md` ## Fix round 1 (rows for other chunks), mismatch 1
- Cross-ref: W-0869; W-0448
- Notes: found in K03. Waits on 인지오's answer. The harness code and fixtures with the same reading (`harness/tools/harness/primitives.py:282`'s comment, `harness/tools/tests/test_primitives.py:459–475`, `harness/tools/tests/fixtures/README.md` lines 14 and 55, the `mock-media` fixture) are code outside the sweep, 인지오's call with the answer. The dataset guidebook vol-07 `:1534` quotes `linter.py`'s comment and this line; it follows the answer (K14).

## Also on this file, not for editing from this list

- W-0481 · waits on 인지오 — Which number does the hold-time plan's no-rule measurement carry — the need for a hold time measured with hold time 0 and no hysteresis on the flap-stress set and the C4 files, under `oracle` and `random`, right after P… Blocks: The step label at `docs/harness/metrics.md:251` (§8, the flip-count row; the §13 entry at :328 is a dated record). Rows W-0454 and W-0456 (the daemon guide §9.…
- W-0482 · closed, already-applied — Line 74 lists `fixed`, `random`, `shipped_catalogue`, `strongest_name_table`, `llm_vocab`, `llm_algo`, `llm_full`, `oracle` and says "the two name-table condit…

### W-0850 · applied
- At: `docs/harness/metrics.md` §10 (the fixtures paragraph), line 320 ("`mock-switch` (MLFQ → FIFO → MLFQ with a config schedule, one hog, …)")
- Change: "one hog" → two hogs (the batch task and the editor, each counted by its first preempt after the switch), as the re-derived fixture has it.
- Final word: 인지오's answer to W-0804 (2026-10-16), applied by stage A (`logs/A4-fixture.md`).
- Sources: `harness/tools/tests/fixtures/mock-switch/expected.csv` (`hogs` 2 on both `switch_window` rows and the 60600 `boost_window` row); `harness/tools/tests/fixtures/README.md` (the `mock-switch` row).
- Notes: found in stage A (A5's reviewer).

### W-0935 · applied
- At: `docs/harness/metrics.md` §6.9, line 178 ("The simulator does not yet: `Mlfq::start()` keeps each task's level, so a switch MLFQ → FIFO → MLFQ resumes the old levels — owed"); §11 item 9, line 314 ("The simulator does not yet: `on_config_apply` re-arms the running task with the incoming params' slice at once — owed")
- Change: Restate both sentences to the code: since `6bf9d850` (2026-10-10) a switch into MLFQ resets every task to Q0 (U1), and a same-algorithm entry leaves the running task its granted slice (U2), as the RQ0 gate spec's conformance statement says ((c) done).
- Final word: `simulator/src/sim.cpp` at `6bf9d850`: U1 and U2 stated at `:47–48`, `Mlfq::start` (`:208–209`) and the same-algorithm branch (`:607`); `simulator/memo/memo_261010.md` Part B, D1; `harness/experiments/rq0-gate.yaml` `simulator-conformance`, "(c) and (f) the simulator does today" (W-0758's answer (a)).
- Sources: `logs/K17.md` ## Rows for other chunks (X1), ## Review round 1
- Cross-ref: W-0758; W-0687
- Notes: found in K17. K10's file: a follow-up chunk.
