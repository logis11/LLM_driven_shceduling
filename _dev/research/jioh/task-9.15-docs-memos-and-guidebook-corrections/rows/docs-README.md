# Work-list rows — `docs/README.md`

Chunk K18, Docs index (wave 5). 4 open rows. The file has 156 lines at `d5cc7711`.

### W-0709 · applied
- At: `docs/README.md` ## Memos (`memos/`), lines 86–102; the Full index table's memo rows, lines 135–147
- Change: Split the memo list into an open list and a closed list, each memo under the heading its header line gives (the memos chunk's outcome), and keep the Full index table's memo rows consistent with it.
- Final word: 9.15 spec decision 10: each memo carries one header line — closed, with where its content now lives, or open, with the ask and its owner; a memo's original text is never edited; a correction is an appended `## Correction (<date>)` section in the memo's own language, the header's `Updated` bumped; no memo is moved or deleted.
- Sources: 9.15 spec decision 10 (`jioh/task-9.15-docs-memos-and-guidebook-corrections.md:54`)
- Notes: Depends on the memos chunk: each memo's open or closed header line is written there first.

### W-0710 · applied
- At: `docs/README.md` ## Guidebook (`guidebook/`), line 18 (vol-06: 'the twelve entries'); ## Workload (`workload/`), line 77 (coreset guide: 'the twelve archetypes, how compile works, and all 50 coreset files'); ## Full index, line 131 (vol-06: 'the twelve entries')
- Change: Restate the coreset-guide row (line 77) to the rebuilt set — the 29-entry library and the 51 core-set files in place of 'the twelve archetypes' and 'all 50 coreset files' — and the old guidebook vol-06 rows (lines 18, 131) so they no longer present twelve entries as the library, each following what the coreset-guide and vol-06 chunks make of those docs.
- Final word: The core set has 51 files (`dataset/build.manifest.json`, 51 artifacts; 67 segments); the archetype library has 29 entries, 28 measured (`category_source: meas`) and `game-task-chain` from `lavd-ossna24` (`dataset/archetypes.yaml`). The record-gaps audit (§2 items 1 and 2): the README's coreset-guide row says 50 files, and it and the vol-06 rows describe twelve literature-grounded entries that mostly no longer exist.
- Sources: SX-0797 (record-gaps §2 item 2, `jioh/2026-10-14-record-gaps-and-doc-staleness-for-9.15.md:27`); SX-0790 (record-gaps §2 item 1, `jioh/2026-10-14-record-gaps-and-doc-staleness-for-9.15.md:26`)
- Notes: Checked at HEAD: 29 entries under `archetypes:`; 51 artifacts in the core manifest. The old guidebook vol-06 describes the library of its time; its index line follows whatever the vol-06 chunk does (e.g. 'the twelve entries of its time').

### W-0711 · applied
- At: `docs/README.md` ## Workload (`workload/`), line 71 (building plan: 'how the dataset is built: two sets, four artifacts, build order')
- Change: Restate the index line once the building plan drops the native artifacts: no 'four artifacts' — the core set and the generated layer, single-lane only, the naturalistic set in the backlog.
- Final word: 9.5 follow-ups spec decision 14 (native compiled set dropped), applied in code by 9.13 D1: the dataset ships the single-lane set only (`dataset/tools/wlc/compiler.py:31`, MODES = ("single",)); the naturalistic generator is on the backlog (`_dev/TODO.md:196`).
- Sources: SX-0005 (TODO 9.15 line (from 9.5, follow-ups spec decision 14), `_dev/TODO.md:179`)
- Notes: The building plan still names `coreset-native`, `generalset-native` (`docs/workload/building-plan.md:28`) — the building plan's rows (another row). Historical mentions of the native set in the dataset guidebook (01 :805, :1002; 03 :2094–2161; 07 :150, :310, :1260; 08 :266, :474, :969–974, :1856) describe the past correctly; the 2026-09-10 memo's '100 artifacts (50 × 2 mode)' (:119) was true at its date.

### W-0712 · applied
- At: `docs/README.md` ## Workload (`workload/`), line 74 ('which processes co-occur (S1–S18) and their taxonomy sources'); ## Full index, line 123 ('which processes co-occur and their sources')
- Change: Restate both index lines to what the scenario catalog answers after its rewrite: the scenarios and the names the dataset binds, each with its existence ground.
- Final word: 9.10 D33 (2026-10-01, amended by D163: S12's name is `python`) with D2: the scenario catalog lists, per row, the names the files bind, each name with its existence ground (its package on Ubuntu 24.04 and the observation that showed its `comm`), the scenario's existence cited from a benchmark definition only where one defines it; the catalog is not a record of co-occurrence (D2: the core set's task sets are design).
- Sources: S10-078 (9.10 D33, `task-9.10-scenarios-timelines/changelog.md:719`)
- Notes: The catalog itself is not yet rewritten (`docs/workload/scenario-catalog.md` header Updated 2026-09-10); its rewrite is another row, and spec decision 6 has the index follow a doc's changed content.

### W-0874 · applied
- At: `docs/README.md` line 69 (the workload docs' reading order and the developer README); the archetype plan's entries, line 72 and the Full index line 121 ("how one process kind is specified and grounded")
- Change: Add to the dataset reading path `dataset/tools/meas/README.md` (the measurement tooling's map), `dataset/meas-releases.yaml` (the release map) and the licences `LICENSE` and `dataset/LICENSE`; lines 72 and 121 may add "and the library's inventory".
- Final word: K04 (wave 1, review passed 2026-10-16): `LICENSE` and `dataset/LICENSE` (9.15 spec decision 12; W-0239, W-0240), `dataset/tools/meas/README.md` (W-0751's answer), the release map (W-0732's answer); the archetype plan's §4 holds the 29-entry inventory (W-0231).
- Sources: `logs/K04.md` ## Rows for other chunks
- Cross-ref: W-0711; W-0710
- Notes: found in K04.

### W-0915 · applied
- At: `docs/README.md` ## Full index, the guidebook vol-03 row, line 128 ("the claim's six links")
- Change: "the claim's six links" → seven links, written "link 1"–"link 7".
- Final word: 인지오's answer to W-0742 (2026-10-16, (a)), applied in K08 to `docs/research-claims.md` ## The chain ("link 1"–"link 7", seven links).
- Sources: `logs/K08.md` ## Rows for other chunks (X2)
- Cross-ref: W-0742; W-0916
- Notes: found in K08.

### W-0937 · applied
- At: `docs/README.md` ## Guidebook (`guidebook/`), the vol-02 line, line 14 ("what the three citation tiers may support"; "the two places nothing published could settle are marked as open rather than filled"), and the vol-03 line, line 15 ("the five things a proposal may never do"; "the six-link chain"); the Full index's vol-03 row, line 128 ("the claim's six links"), is W-0915's
- Change: vol-02's line: the three citation tiers → four kinds (the deployed-system tier widened; the talk, conference-abstract and news-report type added), and no place left open (the Windows Update question settled by Microsoft's Xbox Support article, the TuneAgent venue by its DOI record). vol-03's line: the five prohibitions → four, starvation not among them; the six-link chain → the seven-link chain (link 1–link 7).
- Final word: K15 (wave 4, review passed 2026-10-17): vol-02 §1.5's citation tiers restated to four kinds after `docs/references.md:22–24` (N14; the deployed-system tier per 9.12 D112, the talk type per D113); the two open places closed (W-0644: the Xbox Support article answers the third question; W-0642: TuneAgent at KDD '26, DOI 10.1145/3770855.3817987); vol-03 §4.2 "네 가지 금지", starvation no longer a prohibition (W-0656); the chain as link 1–link 7 (W-0916, 인지오's answer to W-0742 (a)).
- Sources: `logs/K15.md` ## Rows for other chunks (X1); ## Review round 2, finding 7
- Cross-ref: W-0915; W-0656; W-0916; W-0742; W-0939
- Notes: found in K15. Line 128's "six links" → seven is already W-0915; K15's X1 names it too.

### W-0939 · applied
- At: `docs/README.md` ## Guidebook (`guidebook/`), the paragraph's "the four in-text devices" (line 11), the vol-04 line (line 16: "the seven conditions and what each isolates") and the vol-06 line (line 18: "the twelve entries"); the Full index's vol-06 row (line 131)
- Change: vol-04's line: the seven conditions → eight (the two name-table conditions, `shipped_catalogue` and `strongest_name_table`). vol-06's line and row: scoped to the 2026-09-13 library, pointing to the dataset guidebook vol 2 for the current one. The device list: the guidebook README now also lists vol-06's "재구축 이후" mark.
- Final word: K16 (wave 4, review passed 2026-10-17): vol-04's conditions are the eight of `harness/tools/harness/evaluator.py` `CONDITIONS` (`fixed`, `random`, `shipped_catalogue`, `strongest_name_table`, `llm_vocab`, `llm_algo`, `llm_full`, `oracle`; W-0662, 9.12 D6); vol-06 gains a head note scoping it to the 2026-09-13 library of twelve, the current 29-entry library in the dataset guidebook vol 2 (W-0673); the guidebook README's device list gains the "재구축 이후 (2026-10-17)" mark (K16 decision 2).
- Sources: `logs/K16.md` ## Rows for other chunks (X1)
- Cross-ref: W-0710; W-0662; W-0673; W-0937
- Notes: found in K16. The vol-06 part meets W-0710's lines 18 and 131 (the twelve entries); one edit serves both.

### W-1008 · applied
- At: `docs/README.md` ## Memos (`memos/`), ### Open, the invocation memo's entry, line 96 ("Open: both programs run in that command shape — the simulator still takes positional arguments and writes the trace to stdout, and no daemon program is in the repository yet; owners 인경민 (simulator), 박이안 (daemon)")
- Change: Optional, mirroring W-1005: the Open summary adds that the RQ0 gate spec's `simulator-conformance` item (h) requires the simulator side before the RQ0 run.
- Final word: 인지오's answer (c) of 2026-10-17 to K17 (item (h)); `harness/experiments/rq0-gate.yaml:348–357` (item (h): the simulator run as the runner invokes it, `--workload`, `--schedule`, `--out-trace`, no positional argument, the trace written to that file; "The run does not start until each is shown."); W-1005 (applied 2026-10-17 in Q3: the memo's open header line says so).
- Sources: `logs/Q3.md` ## Rows for other chunks (X1); `harness/experiments/rq0-gate.yaml:348–357`
- Cross-ref: W-1005; W-0997
- Notes: found in Q3 (optional). K18's file: a follow-up chunk. The memo's status and name are unchanged, so no other index change follows.
