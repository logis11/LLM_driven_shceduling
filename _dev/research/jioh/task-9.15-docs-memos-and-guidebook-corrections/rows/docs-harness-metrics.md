# Work-list rows — `docs/harness/metrics.md`

Chunk K10, Harness guide and metrics (wave 3). 2 open rows. The file has 344 lines at `d5cc7711`.

### W-0479 · open
- At: `docs/harness/metrics.md` ## 5 Records, line 67 ("One CSV file per trace (or per recognition log), every row self-contained, twenty-four columns.")
- Change: Restate "twenty-four columns" to twenty-five: the §5 tables already list all 25, `telemetry` (added 2026-10-11, 9.17) included.
- Final word: 9.14 D1 added the twenty-fourth column `skipped` (2026-10-09); 9.17 D4 (the telemetry shape through the harness, 2026-10-11) added the identity column `telemetry` after `boot_default`: `harness/tools/harness/records.py:19–23` COLUMNS holds 25, as does `harness/records/schema/records.schema.json`.
- Sources: merge finding (`harness/tools/harness/records.py:19`)
- Resolved at merge: Found while resolving the records' column count (row W-0466; raw row W-0466's notes saw it): `git log -L67,67:docs/harness/metrics.md` shows the line last changed in `cd3fd535` (9.14 D1, to "twenty-four"); 9.17 added the `telemetry` row at :78 without the count.
- Notes: —

### W-0480 · open
- At: `docs/harness/metrics.md` ## 9 Normalisation and floors, the "Sensitivity." paragraph, line 281 ("The RQ0 gate spec pre-registers `fixed` under a sweep of nine alternative boot defaults")
- Change: Restate "nine alternative boot defaults" to ten — the top slice at 0.5, 0.7, 0.9, 1.2, 2, 3, 5, 14, 20 and 100 ms.
- Final word: 9.14 D7 (the RQ0 gate spec rewritten; the ten-point sweep, 2026-10-09), current in `harness/experiments/rq0-gate.yaml`: 19 judging files, K 10 (9.14 decision 2 as amended: the six idle-class files and `c7-mail` leave the judging set), g 0.5, N 100; the boot-default sweep at ten alternatives — the top slice at 0.5, 0.7, 0.9, 1.2, 2, 3, 5, 14, 20, 100 ms (9.11 D2's 0.7 for the 0.75 point; `ostep-slice-14000us` added by 9.14 D7).
- Sources: SX-0287 (TODO 9.15 line (from the 2026-10-11 audit), `_dev/TODO.md:179`); SX-0714 (audit 2026-10-10 docs-staleness additions (pre-registration numbers), `jioh/2026-10-10-dataset-audit-before-9.15.md:55`)
- Notes: `harness/experiments/rq0-gate.yaml` `boot_defaults`: primary `ostep`; alternatives `ostep-slice-500us`, `-700us`, `-900us`, `-1200us`, `-2000us`, `-3000us`, `-5000us`, `-14000us`, `-20000us`, `-100000us`. The hand-offs' :279 has drifted to :281.

## Also on this file, not for editing from this list

- W-0481 · waits on 인지오 — Which number does the hold-time plan's no-rule measurement carry — the need for a hold time measured with hold time 0 and no hysteresis on the flap-stress set and the C4 files, under `oracle` and `random`, right after P… Blocks: The step label at `docs/harness/metrics.md:251` (§8, the flip-count row; the §13 entry at :328 is a dated record). Rows W-0454 and W-0456 (the daemon guide §9.…
- W-0482 · closed, already-applied — Line 74 lists `fixed`, `random`, `shipped_catalogue`, `strongest_name_table`, `llm_vocab`, `llm_algo`, `llm_full`, `oracle` and says "the two name-table condit…
