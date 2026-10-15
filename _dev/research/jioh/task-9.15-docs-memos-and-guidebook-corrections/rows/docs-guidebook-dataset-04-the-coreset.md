# Work-list rows — `docs/guidebook/dataset/04-the-coreset.md`

Chunk K12, Dataset guidebook, volumes 3-4 (wave 3). 17 open rows. The file has 2371 lines at `d5cc7711`.

### W-0533 · open
- At: `docs/guidebook/dataset/04-the-coreset.md` §1.7 ground truth에만 붙는 annotation들, open note line 149
- Change: Close the note once `docs/recognition-vocabulary.md` §1 lists `session` among `initiated`'s values.
- Final word: 9.10 D79 (2026-10-03): `initiated: session`, 'work the desktop session itself starts, unasked, at login', used by `c2-p1b` and `c7-indexing`; its addition to the recognition vocabulary was handed to 9.15.
- Sources: SX-0995 (guidebook dataset vol-04 open note (§1.7), `dataset/04-the-coreset.md:149`)
- Cross-ref: W-0484
- Notes: Apply after the vocabulary `initiated` row (W-0430; its W-0429–0986 come from this volume's §13.8). At HEAD `docs/recognition-vocabulary.md:50` reads '`initiated` (`user` | `scheduled`)'.

### W-0534 · open
- At: `docs/guidebook/dataset/04-the-coreset.md` §1.8 pre-committed miss와 `ambiguous`, table lines 161–168, line 170 and open note line 174; §1.11 judging set과 전체 set, 코드로 note line 240; §14.4 실험과 채점, glossary line 2270
- Change: Restate to 9.23 D1 and D2: the table gains `c6-fold` (meeting/`true`, from 30 s: the call runs inside the browser and the snapshot shows one more `chrome`, nothing that says call) and `c6-spoof` (browsing/`false`, from 20 s: sustained CPU work nobody asked for under a trusted name); line 170's count, line 240's `layer1_exclusions` and the glossary's 'Layer 1에서 빠지는 파일 여섯' become eight files (`[c1-indexing, c6-alias, c6-fold, c6-spoof, c7-backup, c7-ml-train, c7-render, c7-transcode]`). Close the line-174 note with D1 and D2 (68 headline points over 44 files, 70 before).
- Final word: 9.23 D1 (2026-10-14): since 9.10 D30 a `chrome` task on `video-call` arrives at 30 s, so `c6-fold`'s snapshot goes from `chrome ×5` to `chrome ×6`; telemetry rule 1 makes a count-only change a set change, so a query fires at 30 s and nothing in the snapshot says call — the meeting segment (30–60 s) carries `pre_committed_miss: true`, the browsing segment keeps its graded 0 s point. 9.23 D2: `c6-spoof` split at the spoof's arrival — 0–20 s browsing, `background_wanted: true`; 20–60 s browsing, `background_wanted: false`, `spoof: true`, `pre_committed_miss: true`. Both join the RQ0 gate spec's `layer1_exclusions` (eight files); the oracle's graded set is 77 points over 50 files, nine in pre-committed-miss segments (seven before), 68 headline points over 44 files (70 before).
- Sources: SX-0996 (guidebook dataset vol-04 open note (§1.8), `dataset/04-the-coreset.md:174`)
- Cross-ref: W-0501; W-0542; W-0543
- Notes: Checked at HEAD: `harness/experiments/rq0-gate.yaml:94`; `dataset/timelines/coreset/c6.variant.yaml:5–59`; `dataset/tools/tests/test_grid.py:27–29`. 9.23 D1's finding correction: the exclusion list is the RQ0 gate spec's `layer1_exclusions`, derived from the annotation and checked by the evaluator, not the scoring spec's. The line-174 note covers both files; the per-file passages are W-0542 (`c6-spoof`) and W-0543 (`c6-fold`).

### W-0535 · open
- At: `docs/guidebook/dataset/04-the-coreset.md` §1.9 familiarity tier, line 190; §3.2 일곱 그룹의 표, the C1 row line 431; §4.1 C1이 답하는 질문, line 517; §8.1 C5가 답하는 질문, line 1382; §14.3 recognition과 label, glossary line 2249
- Change: Restate `whitelist` to the two conditions, `shipped_catalogue` and `strongest_name_table`, and drop '실제 OS들이 쓰는 방식' (lines 190, 2249); quotations of the building plan (lines 431, 517 — C1, the calibration group, 'where the whitelist should score perfectly'; line 1382 — C5, the familiarity ladder group, 'scores structurally zero on tiers 4–5') follow its restated sentences, `strongest_name_table` being the condition expected to score perfectly on C1 and to have no rule for tiers 4–5's invented names. Line 2066 quotes the 2026-08-26 grill as history and stays.
- Final word: 9.12 D6 as amended by D91, D105, D109 and D115: the `whitelist` condition becomes two. The shipped-catalogue condition (`shipped_catalogue`) reproduces the CachyOS catalogue (`ananicy-rules` at `03ef03fb`) as CachyOS installs and enables it with ananicy-cpp, matched by the basename of each process's `argv[0]`, untruncated (D105); on that key the catalogue keys 19 of the 35 bound names and every name in only 7 of 50 files (D109); it answers RQ2 (research question 2, whether the reading beats what shipping systems do). The strongest-name-table condition (`strongest_name_table`) is a rule list in the catalogue's design covering the software the dataset presents as known, with no rule for Family 3's unregistered software or the invented names of familiarity tiers 4–5; it carries the paper's claim (D115), is the condition expected to score perfectly on the C1 (the single-situation calibration group) files, and fails structurally on world knowledge. 'A faithful reproduction of what shipping systems do today' and 'the whitelist approach real operating systems currently use' are restated to the two conditions (D91).
- Sources: S12-049 (9.12 D6, `task-9.12-related-work-prose/changelog.md:114`); SX-0151 (TODO 9.15 line (from 9.12 D6), `_dev/TODO.md:179`)
- Cross-ref: W-0483
- Resolved at merge: S12-049 lists line 2066 among the mentions to restate; SX-0151 keeps it as a historical quotation. Read the passage (`04-the-coreset.md:2066`): it quotes the 2026-08-26 grill's record ('behaviour and whitelists structurally cannot') as dated history, which 9.12 D6's restatement of the current docs does not reach; kept.
- Notes: Condition ids in code: `harness/tools/harness/evaluator.py:47`, `harness/guards/guard-spec.yaml:126` (the raw rows' `:116` is stale). Write in Korean.

### W-0536 · open
- At: `docs/guidebook/dataset/04-the-coreset.md` §2.5 timeline 파일의 나머지 규칙, open note line 382
- Change: Close the note once `dataset/README.md`'s Coresets table (`:92`) and Rules of the tree (`:170`) state the demand window as reported.
- Final word: 9.14 decision 4 (2026-10-09): the ~100–150 % demand window retired as a gate; every file's demand is a measured fact the manifest reports and no build fails on it (`dataset/tools/wlc/estimate.py` docstring; `docs/workload/building-plan.md` §5a).
- Sources: SX-0997 (guidebook dataset vol-04 open note (§2.5), `dataset/04-the-coreset.md:382`)
- Cross-ref: W-0497
- Notes: Apply after the README demand-window row (W-0202).

### W-0537 · open
- At: `docs/guidebook/dataset/04-the-coreset.md` §3.2 일곱 그룹의 표, line 440; §5.6 `c2-p2a-idle`, line 1092; §10.1 C7이 답하는 질문, line 1570; §12.2 파일의 구성, table line 1969; §12.5 표를 읽어 보기, the printout lines 2002 (browsing/false), 2011 (meeting/true) and 2034 (total), line 2040; §13.6, line 2153
- Change: Restate the current counts to 9.23 D10's coverage grid: 67 segments, 66 on the 32 cells and `c6-dual`'s `ambiguous` one outside (lines 440, 1969's `segments_total`, 2034); in the printout browsing/`false` is 2 segments with 1 miss and meeting/`true` 2 segments with 1 miss; line 1570's `false` count is 19 of 66 grid segments (always-`true` then scores 47/66, about 71 %); line 2040's 'fourteen `false` cells hold one segment' becomes thirteen, browsing/`false` joining gaming and indexing with two, and the `false` side rests on 19 segments. Keep the 9.13 history at 66 (lines 1092, 2153) and add that 9.23 D2's split of `c6-spoof` made 67.
- Final word: 9.23 D10 (2026-10-14): `coverage-grid.json` `segments_total: 67`; browsing/`false` gains `c6-spoof`'s second segment and meeting/`true` `c6-fold`'s pre-committed miss, each cell carrying one pre-committed miss; `test_grid.py`'s pre-committed-miss cells gain the two.
- Sources: SX-0599 (9.23 D10, `task-9.23-guidebook-findings/changelog.md:97`)
- Cross-ref: W-0498; W-0534
- Notes: Checked at HEAD: `dataset/coverage-grid.json` — 66 segments on cells, 19 `false`, browsing/`false` 2 segments and 1 miss, meeting/`true` 2 segments and 1 miss, `outside` [`c6-dual`]. The printout is dated 2026-10-14 (line 1997); `python3.12 tools/derive.py --check --require-coverage` prints the current table. Not named by 9.23's hand-off.

### W-0538 · open
- At: `docs/guidebook/dataset/04-the-coreset.md` §4.5 `c1-browsing` — 웹 browsing, the decision notes lines 574–576 (9.10 D15, D16, D127)
- Change: Add 9.10 D126's stated floor to the count's statement, in Korean: the four `renderer-hidden` tasks are a floor — a real page's cross-site iframes take renderers this count leaves out.
- Final word: 9.10 D131 (2026-10-04) hands 9.10 D126's stated floor to 9.15 'wherever the docs state the renderer count: a real page's cross-site iframes take renderers this count leaves out'.
- Sources: S10-135 (9.10 D131, `task-9.10-scenarios-timelines/changelog.md:2417`)
- Cross-ref: W-0518
- Notes: —

### W-0539 · open
- At: `docs/guidebook/dataset/04-the-coreset.md` §5.2 'behaviorally identical'이 더 이상 참이 아니게 된 일, open note line 940
- Change: Close the note once `docs/workload/building-plan.md` §3 C2 (C2, the intent pair group; lines 89–95) is restated to the rebuilt state.
- Final word: The 2026-10-11 audit's C2 direction (on the 9.15 TODO line): C2's 'behaviorally identical' and 'differ only in intent' restated to the rebuilt state, P3 flipping mode and `initiated`.
- Sources: SX-0998 (guidebook dataset vol-04 open note (§5.2), `dataset/04-the-coreset.md:940`)
- Notes: Apply after the building plan's C2 rows.

### W-0540 · open
- At: `docs/guidebook/dataset/04-the-coreset.md` §5.4 P1 — `c2-p1a` 대 `c2-p1b`, open note line 1006
- Change: Close the note with 9.23 D9: P1 stays the load-bearing pair, stated as it stands — it carries the recognition claim (the wanted training run against the unwanted indexer, which a whitelist cannot tell apart) and its scheduling headroom on `c2-p1a`'s side; RQ0 judges `c2-p1a` and reports `c2-p1b` by design (9.14 decision 2), the indexer's declared idle class settling its side; the audit's sentence is a record and stays.
- Final word: 9.23 D9 (2026-10-14; forward note at 9.12 D14): P1 stays the load-bearing pair, stated as it stands; 9.12 D14 defined what the pair tests and 9.14 decision 2 measured its headroom on `c2-p1b` as zero (the executor's strict idle rule places the idle-class indexer below every row), so `c2-p1b` reports and `c2-p1a` judges; the 2026-10-10 audit's 'the P1 pair the RQ0 load-bearing one' (`:127`) is a record and stays.
- Sources: SX-0621 (9.23 D9, `task-9.23-guidebook-findings/changelog.md:90`); SX-0999 (guidebook dataset vol-04 open note (§5.4), `dataset/04-the-coreset.md:1006`)
- Cross-ref: W-0487
- Notes: Not named by 9.23 D9's hand-off (it names `docs/research-claims.md:205–220`, `docs/workload/building-plan.md:91`, `docs/workload/coreset-guide.md:601`); the note is the A8 finding D9 answers.

### W-0541 · open
- At: `docs/guidebook/dataset/04-the-coreset.md` §5.7 P3, open note line 1124
- Change: Close the note: 9.10 D162 found the comment's 'the export ends by about 99.5 s' still true — the export ends by 88.713 s under every policy — so the comment holds and no fix or re-bless is owed (`_dev/research/jioh/task-9.10-scenarios-timelines/changelog.md:2893`); the note's reading of D162 as an unapplied correction is restated.
- Final word: No record assigns the fix: `c2-p3a.timeline.yaml`'s header comment 'the export ends by about 99.5 s' (`:6`) is 9.10 D125's figure (segment 1 read as 60–120 s); 9.10 D162 (2026-10-06) re-read it at the current length as 88.713 s.
- Sources: SX-1000 (guidebook dataset vol-04 open note (§5.7), `dataset/04-the-coreset.md:1124`)
- Cross-ref: the for-인지오 row W-0776 and the outside-sweep row W-0794 on `c2-p3a.timeline.yaml`; W-0776
- Notes: Answered at merge by 9.10 D162.

### W-0542 · open
- At: `docs/guidebook/dataset/04-the-coreset.md` §9.1 C6가 답하는 질문, table row line 1443; §9.3 `c6-spoof`, the recipe block lines 1464–1471, the segment line 1473, 'compile된 모양' line 1477 and open note line 1484
- Change: Restate to 9.23 D2: the recipe's `set-segments` in place of the `patch-segment` (0–20 s browsing, `background_wanted: true`; 20–60 s browsing, `background_wanted: false`, `spoof: true`, `pre_committed_miss: true`; `[S2]` on both), the segment line and the table row's annotation; the compiled shape's demand per segment, 0.0164 to 20 s and 0.7664 after (0.5164 over the file). Close the note with D2's decision and reason: from 20 s the spoof is sustained CPU work nobody asked for and the snapshot shows one more `chrome` and nothing else; the oracle reads browsing/`false` from 20 s and applies that row (cap 0.05) to the miner; the file joins `layer1_exclusions`.
- Final word: 9.23 D2 (2026-10-14): `c6-spoof` split at the spoof's arrival — 0–20 s browsing, `background_wanted: true`; 20–60 s browsing, `background_wanted: false`, `spoof: true`, `pre_committed_miss: true`; scenario `[S2]` on both; the oracle reads browsing/`false` from 20 s and applies that row (cap 0.05) to the miner; the coverage grid's browsing/`false` cell gains the segment, marked recognition-limited; `c6-spoof` joins the RQ0 gate spec's `layer1_exclusions`; the driver table's browsing/`true` justification (`daemon/driver-table/prior.yaml:58`, the miner held to half the lane) describes the row a name-based recognizer applies to the spoof and stays.
- Sources: SX-0592 (9.23 D2, `task-9.23-guidebook-findings/changelog.md:23`); SX-1004 (guidebook dataset vol-04 open note (§9.3), `dataset/04-the-coreset.md:1484`)
- Cross-ref: W-0534; W-0543; W-0544
- Notes: Recipe at HEAD: `dataset/timelines/coreset/c6.variant.yaml:5–24`; the manifest's demand for `c6-spoof`: segments 0.0164 (0–20 s) and 0.7664 (20–60 s), file 0.5164. The compiled byte count at line 1477 (514,103) is W-0544's; the C6 statement at line 1448 and §9.2's `layer1_exclusions` sentence are W-0543's.

### W-0543 · open
- At: `docs/guidebook/dataset/04-the-coreset.md` §9.1 C6가 답하는 질문, table row line 1445 and line 1448; §9.2 C6의 채점과 RQ0에서의 역할, line 1454; §9.5 `c6-fold`, the recipe block lines 1511–1519, the segment line 1521 and open note line 1530
- Change: Restate to 9.23 D1: the table row's annotation becomes `pre_committed_miss: true` on the meeting segment; line 1448 says three C6 files carry the annotation (`c6-alias` whole, `c6-fold` from 30 s, `c6-spoof` from 20 s; `c6-dual` is `ambiguous`); line 1454's `layer1_exclusions` holds `c6-alias`, `c6-fold` and `c6-spoof`; the recipe block's meeting segment carries `pre_committed_miss: true`. Close the note: a query fires at 30 s on the `chrome` 5 → 6 count change, nothing in the snapshot says call, and the meeting segment is a pre-committed miss excluded from the Layer-1 (recognition-accuracy) headline.
- Final word: 9.23 D1 (2026-10-14): since 9.10 D30 a `chrome` task on `video-call` arrives at 30 s, so the snapshot goes from `chrome ×5` to `chrome ×6`; telemetry rule 1 (`docs/data-contracts.md` §5, frozen 2026-09-06) makes a count-only change a set change, so a query fires at 30 s and D30's 'the canonical set does not change at the boundary' did not hold; nothing in the snapshot says call (a sixth `chrome` is also what a new tab shows), so the meeting segment (30–60 s) carries `pre_committed_miss: true`; the browsing segment keeps its graded 0 s point; the exclusion list is the RQ0 gate spec's `layer1_exclusions`, derived from the annotation and checked by the evaluator.
- Sources: SX-0588 (9.23 D1, `task-9.23-guidebook-findings/changelog.md:13`); SX-1005 (guidebook dataset vol-04 open note (§9.5), `dataset/04-the-coreset.md:1530`)
- Cross-ref: W-0499; W-0534; W-0542; W-0544
- Notes: Recipe at HEAD: `c6.variant.yaml:39–59` (the comment restated by D1); `harness/experiments/rq0-gate.yaml:94`. §9.4 line 1505's history (71 → 70 headline points at 9.20 D10) stays; 9.23 D1–D2 then made it 68 over 44 files. The compiled byte count at line 1523 (680,862) is W-0544's.

### W-0544 · open
- At: `docs/guidebook/dataset/04-the-coreset.md` §9.6 `c6-dual`, 'compile된 모양' line 1544 (and the other files' 'compile된 모양' byte counts in the volume, e.g. lines 1477, 1501, 1523)
- Change: Update `c6-dual`'s byte count to 187,601,795 (9.23 D17) and the other files' compiled byte counts to the current build, or mark the figures as the 2026-10-14 build; the arrive, wake and spawn-table counts stand.
- Final word: 9.23 D17 (2026-10-15): every artifact's bytes changed through 9.23 D16 (the trailing WAIT or TIMER on segment-bound programs), nothing new executing — the CPU, the wakes and the ticks unchanged, the compile reports byte-identical, so no demand moved; `c6-dual` 187,601,795 B, the core set 678,172,716 B over 51 files.
- Sources: SX-0625 (9.23 D17, `task-9.23-guidebook-findings/changelog.md:158`)
- Cross-ref: W-0542; W-0543
- Notes: Checked at HEAD's build (`dataset/build/coreset-single/`): `c6-dual` 187,601,795; `c6-spoof` 514,442 (the volume: 514,103); `c6-fold` 681,137 (680,862); `c6-alias` 168,027 (167,961); the 51 core files sum to 678,172,716. Not named by 9.23's hand-offs.

### W-0545 · open
- At: `docs/guidebook/dataset/04-the-coreset.md` §9.6 `c6-dual`, the decision bullet line 1552
- Change: Restate the bullet as the library now reads: the 12,068 s is the span `c6-dual` held the editor focused before 9.17 D1 made its focus alternate with the game every 688 s (since then 686–688 s stretches); the probes' length and readings are unchanged.
- Final word: 9.23 D8 (2026-10-14): the `code-editor` entry's scope reads 'Read over 12,068 s, the span `c6-dual` held it focused before its focus alternated with the game every 688 s (9.17 D1)'; since 9.17 the editor's longest focused stretch in `c6-dual` is 686–688 s; the probes' length and readings unchanged (`dataset/archetypes.yaml:181`, written by `dataset/tools/meas/campaign/fold_in.py`).
- Sources: SX-0361 (TODO 9.15 line (from 9.23 D8), `_dev/TODO.md:179`); SX-0613 (9.23 D8, `task-9.23-guidebook-findings/changelog.md:80`); SX-1007 (9.23 D8 (guidebook copy of the library's 12,068 s clause), `dataset/04-the-coreset.md:1552`)
- Cross-ref: W-0514
- Notes: Named by 9.23 D8's hand-off (vol-04 `:1552`) and the 9.15 TODO line.

### W-0546 · open
- At: `docs/guidebook/dataset/04-the-coreset.md` §10.5 keystroke slice 규칙, open note line 1670 (the table lines 1658–1666)
- Change: Close the note with 9.23 D7: 9.18 D6's base figures for indexing, compile and ml-train (46, 2,354, 1,844) count the whole base file's distinct keystroke times; over the counterpart's span they are 28, 358 and 1,629, the table's bracketed counts; a forward note sits at 9.18 D6.
- Final word: 9.23 D7 (2026-10-14; forward note at 9.18 D6, `_dev/research/jioh/task-9.18-compiler-schema-and-build-gate/changelog.md:41`): for indexing, compile and ml-train 9.18 D6 gave the whole base file's distinct keystroke times, 46, 2,354 and 1,844; over the counterpart's span they are 28, 358 and 1,629; browsing, office, dev and mail match the span; the subset relation holds either way; the six artifacts were unchanged since D6 (their manifest hashes identical at `71a57a23` and `27340c3d`).
- Sources: SX-0358 (TODO 9.15 line (from 9.23 D7), `_dev/TODO.md:179`); SX-0610 (9.23 D7, `task-9.23-guidebook-findings/changelog.md:72`); SX-1008 (guidebook dataset vol-04 open note (§10.5), `dataset/04-the-coreset.md:1670`)
- Cross-ref: W-0524
- Notes: Named by 9.23 D7's hand-off (vol-04 `:1670`) and the 9.15 TODO line. The table already gives events with distinct times in brackets.

### W-0547 · open
- At: `docs/guidebook/dataset/04-the-coreset.md` §10.7 `c7-compile`, open note line 1755
- Change: Once the final memo to 인경민 and 박이안 is committed, restate the note: the memo carries the refusal (with the generated files holding a compile, 9.23 D3) and 인지오's answer on whether the simulator or the dataset changes; it stays open until the simulator accepts the files. 9.23 D14's lint that a spawned child's WAKE targets resolve leaves the refusal as it was.
- Final word: TODO 9.15 line (`_dev/TODO.md:179`, from the 2026-10-11 audit): the final memo carries the simulator loader's refusal of child-targeted WAKEs (`simulator/src/sim.cpp:874-904`; `c1-compile`, `c7-compile`, `c3-workday`, `c4-compile`, `c6-dual`; 9.6 D19, six processes per object job waking each other); 9.23 D3 adds the generated files holding a compile (the 212 jobs in them could not be run); 9.23 D14 lints that a spawned child's WAKE targets resolve, which leaves the simulator's refusal as it was.
- Sources: SX-1009 (guidebook dataset vol-04 open note (§10.7), `dataset/04-the-coreset.md:1755`)
- Cross-ref: W-0506
- Notes: Checked at HEAD: `simulator/src/sim.cpp:876`. Apply with or after the final memo: the final-memo row W-0718 and the for-인지오 row W-0774.

### W-0548 · open
- At: `docs/guidebook/dataset/04-the-coreset.md` §12.4 CI가 강제하는 방식, line 1991
- Change: Add that since 9.23 D12 `make check`'s `check_build.py` also holds the derived timelines and `coverage-grid.json` to their committed bytes (`git show HEAD:<path>`), beside `derive.py --check`'s drift check against a fresh derive, so a regenerated grid or derived timeline left uncommitted fails.
- Final word: 9.23 D12 (2026-10-15): `check_build.py`'s `rewritten` names every derived timeline a variant spec names and `coverage-grid.json`; `check_committed` holds them to their committed bytes as it holds the manifests, so a derived timeline regenerated and left uncommitted fails `make check`; the dataset README's `make check` and `check_build.py` lines restated.
- Sources: SX-0636 (9.23 D12, `task-9.23-guidebook-findings/changelog.md:116`)
- Cross-ref: W-0494; W-0528
- Notes: `derive.py --check` re-derives and compares with the files on disk (`dataset/tools/derive.py:6`); before D12 a file `make dataset` had rewritten and left uncommitted passed it. Code: `dataset/tools/check_build.py:43–65`; the `dataset/Makefile` check target. Not named by 9.23's hand-off.

### W-0549 · open
- At: `docs/guidebook/dataset/04-the-coreset.md` §13.8 무엇이 어디서 낡았나, the doc list lines 2165–2181 and open note line 2183
- Change: Restate §13.8 after the docs it lists are corrected: drop or restate each named doc's entry as its rows are applied, keep what stays stale (the blocked TIMER rows; the tree items left to outside-sweep rows — `c2-p3a.timeline.yaml`'s 'about 99.5 s', `grid.py`'s `NAME_TIERS`), and close the note: the two items the volume found, `c6-fold`'s 30 s query point and `c6-spoof`'s label, were decided by 9.23 D1 and D2.
- Final word: 9.23 D1 and D2 (2026-10-14) decided the two items the guidebook found off the 9.15 list (`c6-fold`'s meeting segment a pre-committed miss from 30 s; `c6-spoof` `false` and a pre-committed miss from 20 s); the other entries are 9.15 rows on the docs named.
- Sources: SX-1011 (guidebook dataset vol-04 open note (§13.8), `dataset/04-the-coreset.md:2183`)
- Cross-ref: W-0530
- Notes: Apply after the listed docs are corrected. Line 2173 calls the README's '51개 파일, 66개 segment' current — since 9.23 D10 it is 67 (the README count row is another row's). Line 2177's terminology 'the three C6 files' now holds (three carry `pre_committed_miss`).

## Also on this file, not for editing from this list

- W-0550 · closed, carried — `_dev/TODO.md:200` (Backlog: 'Unwanted jobs to measure — how many the attribute's `false` side needs is decided in the RQ1 experiment spec's session …') carrie…
- W-0432 · waits on 인지오 — The ratified vocabulary glosses the mode `render` as 'an offline 3D/graphics render' (`docs/recognition-vocabulary.md:34`). Since 9.10 D10 every render file binds an offline video export — Kdenlive's `kdenlive_render` e… Blocks: the `render` row at docs/recognition-vocabulary.md:34 (and its §5 changelog entry if it changes); also the open note at docs/guidebook/dataset/04-the-coreset.m…
- W-0747 · waits on 인지오 — Does pair P3's segment 1 (`c2-p3a` / `c2-p3b`, 60–326 s) stay as sized? What the records and code say: 9.10 D123 sized it so the backup ends under every policy; the idle class (9.13) makes the backup run only in the edi… Blocks: The dataset guidebook vol-04 §5.7 note; the coreset guide's P3 narrative.; also the open note at docs/guidebook/dataset/04-the-coreset.md:1148
- W-0757 · waits on 인지오 — Plan `c6-dual`'s records cost into Phase 10, or open a task for a cheaper records path? What the records say: about 40 minutes a run, 100 `random` seeds planned (`changelog.md:108`); the run's memory peak is `c6-dual`'s… Blocks: The dataset guidebook vol-08 §8.5 note (W-0600) and §12.4.; also nothing; the note at docs/guidebook/dataset/04-the-coreset.md:1556 stays accurate meanwhile
