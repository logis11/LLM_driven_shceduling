# Work-list rows — `docs/guidebook/dataset/08-decision-chronicle.md`

Chunk K14, Dataset guidebook, volumes 7-8 (wave 4). 8 open rows. The file has 2053 lines at `d5cc7711`.

### W-0599 · applied
- At: `docs/guidebook/dataset/08-decision-chronicle.md` §1 the RQ1–RQ5 bullet, line 92 ('RQ2는 … (무인식, whitelist 대비)'); already stating the split: lines 522, 1165, 1293, 1718, 1993; dated quotations: lines 519, 1841; the 2026-10-11 result paraphrase: line 1430
- Change: Restate line 92's RQ2 to 9.12 D6 and D115: RQ2 compares against no recognition and against the shipped catalogue (`shipped_catalogue`), the condition that answers it; leave the dated quotations (519, 1841) and the lines that already state the split.
- Final word: 9.12 D6, amended by D91, D105, D109 and D115: the `whitelist` condition becomes two. The shipped-catalogue condition (`shipped_catalogue`) reproduces the CachyOS catalogue (`ananicy-rules` at `03ef03fb`) as CachyOS installs and enables it with ananicy-cpp, matched by the basename of each process's `argv[0]`, untruncated (D105); on ananicy-cpp's key it keys 19 of the 35 bound names and every name in only 7 of 50 files (D109); it answers RQ2 (research question 2, value: 'does that reading beat what shipping systems do?', D115). The strongest-name-table condition (`strongest_name_table`) is a rule list in the catalogue's design covering the software the dataset presents as known, with no rule for Family 3's unregistered software or the invented names of familiarity tiers 4–5; it carries the paper's claim (D115), is the condition expected to score perfectly on the C1 (the single-situation calibration group) files, and fails structurally on world knowledge. 'A faithful reproduction of what shipping systems do today' and 'the whitelist approach real operating systems currently use' are restated to the two conditions (D91).
- Sources: S12-052 (9.12 D6, `task-9.12-related-work-prose/changelog.md:114`); SX-0153 (TODO 9.15 line (from 9.12 D6), `_dev/TODO.md:179`)
- Resolved at merge: Both raw rows marked the file already applied; S12-052 flagged `:92` as the one present-tense description. Read the target: `:92` paraphrases the proposal's RQ2 now ('whitelist 대비') and 9.12 D115 has the shipped catalogue answer RQ2, so an edit is owed there alone; `:1430` ('whitelist 조건도 focus를 받습니다') paraphrases the 2026-10-11 audit review's result — a record of its day, left to the editing agent's judgement.
- Notes: Condition identifiers in code: `harness/tools/harness/evaluator.py:47`, `harness/guards/guard-spec.yaml:126` (S12-052's ':116' is `:126`).

### W-0600 · applied
- At: `docs/guidebook/dataset/08-decision-chronicle.md` §8.5 9.14가 만난 크기의 문제, open note line 1316; §12.4 item 5, line 1797 ('아직 TODO에 줄이 없습니다')
- Change: Restate the note and §12.4 item 5 with 인지오's answer on `c6-dual`'s records cost: a cheaper records path on its own `_dev/TODO.md` line (name it), or the 40-minutes-a-run cost over 100 `random` seeds planned into Phase 10's RQ0 run; with no answer they stay.
- Final word: `c6-dual`'s records build costs about 40 minutes a run, with 100 `random` seeds planned for the RQ0 run; the 9.14 handoff says 'a cheaper records path is a task of its own'; no `_dev/TODO.md` line exists for it; 인지오 decides.
- Sources: SX-1135 (guidebook dataset vol-08 open note (§8.5), `dataset/08-decision-chronicle.md:1316`)
- Waits on: W-0757 (인지오's answer; the row applies once it is given, or is logged as waiting)
- Notes: Waits on the for-인지오 row from W-0757. Checked at HEAD: no `_dev/TODO.md` line names a cheaper records path.

### W-0601 · applied
- At: `docs/guidebook/dataset/08-decision-chronicle.md` §11.5 archetype library, open note line 1692; §12.8 table row line 1853 (library v0.1)
- Change: Close the note and the §12.8 row once `dataset/archetypes.yaml`'s header reads v0.2 (an outside-sweep edit, 인지오's: the file is a compile input of all seven manifests, so the edit re-blesses them and re-pins the RQ0 gate spec); if the header stays, restate the note to that decision.
- Final word: 9.13 decision 9: the library's stated version moves from v0.1 to v0.2 in the data-contracts §2 and the dataset README; `dataset/archetypes.yaml:1` still says '(v0.1)'; the TODO 9.15 line carries '`dataset/archetypes.yaml:1` "(v0.1)"'.
- Sources: SX-1137 (guidebook dataset vol-08 open note (§11.5), `dataset/08-decision-chronicle.md:1692`)
- Cross-ref: W-0606
- Notes: Waits on the outside-sweep rows on the header (another row: W-0778). Checked: `dataset/archetypes.yaml:1` at HEAD '# dataset/archetypes.yaml — Layer 1 archetype library (v0.1)'.

### W-0602 · open
- At: `docs/guidebook/dataset/08-decision-chronicle.md` §12.1 9.15 — heading line 1741 ('WIP, 2026-10-14부터'), body lines 1743–1759 (incl. line 1745's 18,441-byte count), open note line 1761
- Change: At 9.15's end, restate §12.1 from plan to outcome and close the note: the work list and chunk grouping reviewed by 인지오 (spec decision 1), the final memo's language decided, 9.15 finished on spec decision 14's conditions; the heading's WIP status and the TODO line's byte count follow.
- Final word: 9.15 spec (2026-10-14): decision 1 — one combined work list, reviewed by 인지오 with the chunk grouping before any edit; the spec's only open item — the final memo's language, decided at the memo step; decision 14 — 9.15 is done when every work-list row is closed, every chunk has passed its reviewer and is committed, 인지오 has read every chunk log and every overturned decision is applied, every logged code-versus-decision mismatch has 인지오's answer, every memo carries its open or closed line, and the final memo is committed.
- Sources: SX-1138 (guidebook dataset vol-08 open note (§12.1), `dataset/08-decision-chronicle.md:1761`)
- Cross-ref: W-0603; W-0580
- Deferred: after the final memo is committed (9.15 spec decision 13): applied by a follow-up on this file, not in the chunk's wave
- Notes: Sequencing: as the vol-06 §14.1 row (W-0580), this runs last, with or after the final memo's commit (spec decision 13 puts the memo after the doc chunks).

### W-0603 · applied
- At: `docs/guidebook/dataset/08-decision-chronicle.md` §12.1, the '최종 memo가 실을 것' paragraph line 1763 (the quotation '… the simulator loads files up to 190 MB (`c6-dual`), the set 681 MB in all')
- Change: After the quotation, note that the final memo carries 9.23's sizes — `c6-dual` 187.6 MB (187,601,795 B), the core set 678 MB (678,172,716 B over 51 files) — the quoted 190 MB and 681 MB being 9.13's; the quotation stays as written.
- Final word: 9.23 D8 (hand-off to 9.15): the final memo's file-size row carries 9.23 D10's sizes; 'the "190 MB … 681 MB" are 9.13's'; the TODO 9.15 line now also reads 'the final memo's sizes `c6-dual` 187.6 MB, the set 678 MB'; 9.23 D17's rebuild: `c6-dual` 187,601,795 B, the core set 678,172,716 B over 51 files.
- Sources: SX-1139 (9.23 D8 (stale passage in guidebook dataset vol-08 §12.1), `dataset/08-decision-chronicle.md:1763`)
- Cross-ref: W-0602
- Notes: Checked on HEAD's build: `c6-dual.workload.json` 187,601,795 B; the 51 core artifacts sum to 678,172,716 B. Line 1267 (9.13 D7's hand-off of 681 MB and 190 MB) is a dated account and stays.

### W-0604 · applied
- At: `docs/guidebook/dataset/08-decision-chronicle.md` §12.2 9.16 — exit audit, the list item line 1775 ('sub-task마다의 manifest와 pin(9.17 … scoring spec `0ff71b1f…`)')
- Change: Add the 9.16 line's 9.23 item (9.23 D15: the full smoke at home, `make -C harness smoke`, on the final build, its time recorded) to the list, and name the current pins as 9.23 D17's (dataset `81d3213d…`, variants `7079e677…`, scoring spec `2ad757b6…`, generated `826c719c…`, `392d6071…`, `97ba813f…`, `919bb2c0…`, `b6f82df5…`). Whether the chronicle gains an account of 9.23 itself (its chapters stop at 2026-10-14; 9.23's D1–D17 ran 2026-10-14/15) is the editing agent's call, logged (spec decision 2): new volumes are out of scope, sections within a volume are not.
- Final word: 9.23 D10 (2026-10-14) and D17 (2026-10-15) re-blessed after 9.21: D10 dataset `c5f7fa5a…`, variants `8986b58a…`, scoring spec `2ad757b6…`, generated `3035cfe3…`/`2e381b42…`/`90cc782a…`/`e61fd777…`/`1a7d35d7…`; D17 — the current pins — dataset `81d3213d…`, variants `7079e677…` (the RQ0 gate spec, `harness/experiments/rq0-gate.yaml:485–490`), the scoring spec at D10's `2ad757b6…`, generated `826c719c…`/`392d6071…`/`97ba813f…`/`919bb2c0…`/`b6f82df5…`. The 9.16 TODO line (`_dev/TODO.md:180`) carries from 9.23 only D15's full smoke at home on the final build.
- Sources: SX-0627 (9.23 D10, `task-9.23-guidebook-findings/changelog.md:98`)
- Cross-ref: W-0581
- Resolved at merge: As W-0581: the list mirrors the 9.16 TODO line, which carries from 9.23 only D15's smoke; D17's pins supersede D10's and are what the 2026-10-11 review's item checks.
- Notes: Same change as the vol-06 §14.2 table row (W-0581). No volume 05–08 of the dataset guidebook names 9.23 (grep at HEAD).

### W-0605 · applied
- At: `docs/guidebook/dataset/08-decision-chronicle.md` §12.6 executor 질문들 — 두 방향, items 2–3 of 인경민's questions (lines 1830–1831, '확인 필요') and open note line 1833
- Change: Restate the note and the two '확인 필요' items with 인지오's answers — whether the 2026-10-10 audit's recommended heads-up and replies were sent; the `fork_cap` items; `mock-switch` Q1–Q3 — or, where the final memo carries the answers, say so once it is committed; 인경민's LOTTERY answer stays 인경민's.
- Final word: The 2026-10-10 audit's 'Recommended order before 9.15 proper' opens with a heads-up to 인경민 on the loader refusal and answers to 인경민's three open questions; no record shows answers to `fork_cap`'s meaning and `mock-switch` Q1–Q3 (`simulator/notes/note1010.md`) nor whether the reply was sent; 인경민's answer to the LOTTERY question (how LOTTERY splits the batch share when the editor's burst tail is batch-class) is not found either. Answered elsewhere: the EDF chain-stage class (`simulator/notes/note-for-jioh-edf-chain-stage-class.md:57–65`, 2026-10-10) and a keystroke during RUN (`docs/harness/metrics.md:307`).
- Sources: SX-1143 (guidebook dataset vol-08 open note (§12.6), `dataset/08-decision-chronicle.md:1833`)
- Waits on: W-0735, W-0736 (인지오's answer; the row applies once it is given, or is logged as waiting)
- Notes: Waits on the for-인지오 rows from W-0764 (`fork_cap`), W-0765 and W-0736 (`mock-switch` Q1, Q2), W-0735 (heads-up sent) and the final-memo row from W-0723; its W-0766 reads Q3 ('guide §4½ needs a fifth instruction') as met by 9.23 D16 (the editor's program gains its trailing WAIT).

### W-0606 · applied
- At: `docs/guidebook/dataset/08-decision-chronicle.md` §12.8 문서와 tree의 불일치 (2026-10-14 현재), table row 1 line 1851 ('51개, 66개 … `segments_total` 66'); §8.3 line 1269 ('`segments_total`은 66')
- Change: Restate the tree's segment count to 67 (`dataset/coverage-grid.json` `segments_total`, since 9.23 D2 split `c6-spoof`) in the §12.8 row and line 1269's current-tree check, or mark them as of 2026-10-14; whether §12.8 is updated row by row or closed once 9.15's rows are applied is the editing agent's call, logged.
- Final word: The core set has 67 segments since 9.23 D2 (`c6-spoof` split at the spoof's arrival, 20 s), re-derived in 9.23 D10 (`dataset/coverage-grid.json` `segments_total` 67); 51 files (`dataset/build.manifest.json` `artifacts` 51).
- Sources: SX-1104 (guidebook dataset vol-08 ch.12 §12.8 mismatch table row 1, `dataset/08-decision-chronicle.md:1851`)
- Cross-ref: W-0601
- Notes: Line 1256's quotation of 9.13 D7 ('at 66 segments') is a record of its day and stays. Line 1269 is found by the same fact (not in the raw row).

### W-0857 · applied
- At: `docs/guidebook/dataset/08-decision-chronicle.md` §12.8 문서와 tree의 불일치 (2026-10-14 현재), table lines 1851–1860 — the rows whose stale docs include the coreset guide: 1851 (core set 50, 64 segments), 1852 (twelve archetypes), 1854 (the demand window as a rule), 1856 (two compile modes, `coreset-native`), 1857 (`clamscan`), 1859 (`c5-t3`)
- Change: Restate or close these rows' mentions of the coreset guide once wave 1 lands: `docs/workload/coreset-guide.md` now states the tree — 51 files and 67 segments, the 29 entries, one compile mode, demand reported and never a gate, `package-upgrade` (`unattended-upgr`) in place of `clamscan`, `c6-alias` in place of `c5-t3`.
- Final word: K03 (wave 1, review passed 2026-10-16): the coreset guide's full pass (W-0154) with W-0155 (51 files, 67 segments), W-0161 (the 29 entries), W-0166 (`package-upgrade`), W-0174 (the native mode removed), W-0175 (demand reported, no lint), W-0178 (`c6-alias`).
- Sources: `logs/K03.md` ## Rows for other chunks; W-0154; W-0155; W-0161; W-0166; W-0174; W-0175; W-0178
- Cross-ref: W-0601; W-0606
- Notes: found in K03. W-0606 covers only row 1's segment count, W-0601 only the v0.1 row (1853). Row 1852's other doc, `docs/data-contracts.md` §2, now lists the 29 entries (K05, W-0245); the other docs these rows name land with their own chunks. Whether §12.8 is updated row by row or closed once 9.15's rows are applied is the editing agent's call (W-0606).

### W-0868 · applied
- At: `docs/guidebook/dataset/08-decision-chronicle.md` §12.8 문서와 tree의 불일치 (2026-10-14 현재), table rows 1 (line 1851, "core set 50개, segment 64개(building plan, …)"), 6 (line 1856, two compile modes, `coreset-native`) and 7 (line 1857, C7's `clamscan`)
- Change: Restate or close these rows' building-plan and scenario-catalog side: both now state the tree — 51 files and 67 segments (W-0086), one compile mode (W-0087), no `clamscan` (W-0128) and S17 the unattended upgrade (W-0149).
- Final word: K02 (wave 1, review passed 2026-10-16).
- Sources: `logs/K02.md` ## Rows for other chunks (X7)
- Cross-ref: W-0606; W-0857; W-0601
- Notes: found in K02. X7's other parts are carried by open rows whose apply-after rows K02 has applied: the dataset guidebook vol-01's §5.1, §5.2 and §5.6 notes (W-0498, W-0499, W-0500, W-0503) and vol-04 §13.8 (W-0549). Whether §12.8 is updated row by row or closed once 9.15's rows are applied is the editing agent's call (W-0606), as W-0857 says.

### W-0934 · open
- At: `docs/guidebook/dataset/08-decision-chronicle.md` §12.1 (9.15's section, W-0602's place); §10.7's closing sentence; §13's 2026-10-16 row
- Change: In W-0602's pass, state in 9.15's outcome its 2026-10-16 batched rebuild (`37c2e233`) and the batch after wave 4; §10.7's closing sentence and §13's 2026-10-16 row point there.
- Final word: K14's decisions 5 and 8: vol-08 gains §10.7, the account of 9.23; 9.15's own account stays W-0602's, deferred until the final memo is committed (9.15 spec decision 13). `37c2e233` (2026-10-16) is 9.15's batched rebuild (`harness/CHANGELOG.md`'s 2026-10-16 entry; W-0729's answer: one rebuild for the data and code edits answered before the waves).
- Sources: `logs/K14.md` ## Rows for other chunks (X2), ## Decisions 5 and 8
- Cross-ref: W-0602; W-0580; W-0932; W-0933
- Notes: found in K14. K14's file: with W-0602, after the final memo.

### W-0955 · open
- At: `docs/guidebook/dataset/08-decision-chronicle.md` §8.4, the **replay** definition, line 1304 ("측정된 반복 하나의 실제 wake 순서를 그대로 재생해 task를 만드는 방식"); §14.2's glossary, the **replay** row, line 1982 (the same words)
- Change: Restated to the three stream kinds (wakes, runs with the block after each, cycles) where the text means the trace-replay variant. In the volume's Korean.
- Final word: W-0876, applied 2026-10-17 in the batched data rebuild (`7b024003`): each `dataset/replay/*.json.gz` carries its `kind` — `wakes` (`code-editor`, `web-browser`, `renderer-hidden`), `runs` with the block after each (`package-upgrade`, `cpu-batch`'s `python3`), `cycles` (`video-call`); `dataset/tools/wlc/compiler.py` `_replay_window` checks the kind; `dataset/variants.yaml`'s `trace-replay` comment and `dataset/tools/wlc/variants.py`'s docstring name the three kinds. The variants manifest's `replay` fields: the upgrade's runs in `c7-dev`, `c7-browsing` and `c7-meeting`, `python3`'s in `c2-p1a`, the call's cycles in `c7-meeting` — every replay file replays a batch job's runs. G3 applied the same restatement in vol-04 (its N2: §11.3's table, §11.4's replay axis, the glossary's `replay` row).
- Sources: `logs/G3.md` ## Rows for other chunks (X1); `dataset/replay/*.json.gz` `kind`; `dataset/tools/wlc/compiler.py` `_replay_window`; `dataset/variants.yaml`'s `trace-replay` comment since `7b024003`
- Cross-ref: W-0876; W-0951
- Notes: found in G3. K14's file: a follow-up chunk.

### W-0956 · open
- At: `docs/guidebook/dataset/08-decision-chronicle.md` §12.8's table, rows 1 and 2, their 2026-10-17 cells, lines 1873–1874 ("`docs/README.md`의 coreset guide 설명 줄에는 "all 50 coreset files"가 남아 있음"; "… "the twelve archetypes"가 남아 있음")
- Change: Mark both cells fixed: `docs/README.md`'s coreset-guide line now reads "the 29 archetypes" and "all 51 core-set files".
- Final word: W-0710, applied 2026-10-17 in K18: `docs/README.md:77` restated (29 entries in `dataset/archetypes.yaml`; 51 artifacts in `dataset/build.manifest.json`; the coreset guide's §4 "archetype 29개" and §10 "51개 파일 상세").
- Sources: `logs/K18.md` ## Rows for other chunks (X1); `dataset/archetypes.yaml`; `dataset/build.manifest.json`
- Cross-ref: W-0710; W-0602; W-0934
- Notes: found in K18. K14's file: with W-0602's pass, after the final memo (K18's note), as W-0934.

## Also on this file, not for editing from this list

- W-0607 · closed, already-applied — vol-08:271 already states the final word, accurate at HEAD; the generalset's backlog line is `_dev/TODO.md:196`.
- W-0608 · closed, already-applied — vol-08:371 already states the final word; whether the rationales are recovered and archived is the for-인지오 row from W-0741 — a recovered archive would be a new…
- W-0609 · closed, already-applied — vol-08:419 already states the final word; `system-daemon` has left the library, so the cli:1 clause is history; the archive question is the for-인지오 row from W-…
- W-0610 · closed, already-applied — vol-08:1009 already says the fix is 인경민's and the final memo announces it; 9.23 D14's lint (`dataset/tools/wlc/linter.py:325`) checks that spawned WAKE targets…
- W-0611 · closed, already-applied — vol-08:1136 already states the final word; the question of a reason is the for-인지오 row from W-0740, whose change says no doc edit follows.
- W-0612 · closed, carried — Waits on 9.16, nothing owed in 9.15: the 9.16 line `_dev/TODO.md:180` carries it; the note stays true when 9.15 ends.
- W-0613 · closed, carried — Waits on Phase 10, nothing owed in 9.15: the Phase 10 section `_dev/TODO.md:189–193` carries it (the trace-replay check's conditions at `:191`); the note is ac…
- W-0614 · closed, carried — Waits on the backlog, nothing owed in 9.15: the backlog lines `_dev/TODO.md:196–201` carry the five items with their deciding places, as the note states.
