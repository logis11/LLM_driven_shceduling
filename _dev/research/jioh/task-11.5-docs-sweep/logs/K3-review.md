# K3 · Dataset guidebook 5 and 6 — review

Reviewed: `git diff -- docs/guidebook/dataset/05-the-generated-layer.md docs/guidebook/dataset/06-grounding-measurement-verification.md` against `rows/g3-dataset-guidebook-05-06.md`, the work list (R1–R7, Q1–Q7, Rows by file), the editor brief and `logs/K3.md`.

**FINDINGS — 1**

## Findings

### 1. `docs/guidebook/dataset/06-grounding-measurement-verification.md:1059` — g3-20, "처음 돌았습니다" is false

- **What is wrong.** The new sentence reads "이 variant들은 RQ0 run(2026-11-16–18)에서 처음 돌았습니다." The three measurement variants of §8.6 (venue, corner, replay) first ran in 10.4's cold smoke, 2026-11-14 to 2026-11-15, on the same programs, before the RQ0 run. The sentence it replaces ("Phase 10에서 처음 돌아갑니다") was true of that smoke, because 10.4 belongs to Phase 10. The row's Becomes introduced "처음 … RQ0 run", and the editor applied it as written.
- **Record.** `_dev/research/jioh/task-10.4-cold-smoke-and-cost-response/README.md`, "The first smoke" (started 2026-11-14T13:04, `simulator@0d323c84470a`; the slow run `c1-transcode@venue-x1.25/random-1~focus`). `second-smoke/run-times.csv` in the same folder (started 2026-11-14T18:54) holds 152 `@venue-*` runs, 88 `@corner-*` runs and 16 `@replay` runs, each `built` — for example `c1-compile@corner-high,fixed~focus`, `c2-p1a@replay`, `c7-browsing@replay`.
- **Fix.** Drop "처음", for example: "이 variant들은 RQ0 run(2026-11-16–18)에서 돌았습니다." The counts after it (7, 5; 5, 6; trace replay disagreeing; post hoc 5, 4 and 4, 4) match `docs/rq0-run-record.md` and stay. No new fact is needed.

## Checked and in order

- **Coverage.** All 19 rows due are applied: g3-01–04, g3-08–20 and g3-22–25 (g3-17 under Q2, g3-22 under Q1). Q1 leaves g3-05, g3-07 and g3-21 because they are dated, and D leaves g3-06. Those four passages are untouched.
- **Scope.** Each hunk maps to one row. The only other changes are the two header lines, each set to `Updated 2026-11-21`.
- **Records, by row.**
  - **g3-01.** Matches `harness/CHANGELOG.md`: the 2026-11-20 entry ("a spec whose run record is committed beside it … a pin the working tree no longer matches is printed as a note") and the opening of the 2026-11-21 re-measurement entry ("its dataset and variants pins name the first bless").
  - **g3-02, g3-03, g3-04 and g3-09.** Match decision 10 of the Phase 11 spec ("after Phase 12's second RQ0 run, on the table and programs that run uses"). They agree with K9's g0-13 and with `_dev/TODO.md` line 32. In §16.4 the "미실행" heading stays, because the no-rule measurement (the hold-time plan's step 1) has not run.
  - **g3-08.** The run record is `runs.sha256.csv`, as the 2026-11-20 changelog entry names it. The search spec counts as executed once `report.json` is committed beside it (the 2026-11-21 search entry's "Experiment lint" bullet). Both files are tracked.
  - **g3-10.** Matches `method.md` §4 and §5: kernel `7.0.0-1017-azure` against the original's `6.17.0-1022-azure`, transparent huge pages `madvise` by default, `always` written after the warm start, and the `provjobd` waits folded into the run they interrupt.
  - **g3-11.** Matches `.github/campaign-background.json` (`mnist`, `[74, 102]`, `attempt` 284) and commit `03723634` (2026-11-21).
  - **g3-12, g3-13 and g3-14.** Match `method.md` §1 and the run record's 2026-11-21 campaign table (55.27 s ±5.89 % and 403.96 µs ±2.15 % over 107 repeats; ±27.3 % and ±10.8 % over the 9.10 campaign's 6). They also match `dataset/variants.yaml` `carried_values` (0.0589, 0.0215, khugepaged).
  - **g3-15.** Matches the run record. The Outcome section gives 2.512 → 0.000 and 5 to 6. The 2026-11-21 correction gives the finding table (`python3` run between voluntary blocks at −27.3 % moving the file alone), the campaign, and "final … fail — 5 of 19 … K = 10".
  - **g3-16 and g3-17.** Checked against the records named by rows g0-16 and g0-15. The 107 repeats are in the run record's 2026-11-21 correction, "The campaign". The 15.7 % is line 564 of `measurement-campaign-record.md`: "680 jobs — 107 landed … (15.7 %". The upper bound of 83 % is that record's 83.3 % draw, which was already in the overview's range.
  - **g3-18, g3-19 and g3-25.** Match the run record's trace-replay bullet and its post hoc table (`c7-dev` 0.000 against 0.000; `c7-browsing` 1.121 against 0.475). The label "compile된 build의 gap 대 재생 build의 gap" follows the `gap` and `replayed gap` columns of `harness/experiments/rq0-gate/report.md`, "Line: trace_replay".
  - **g3-20.** Every count matches the reporting-lines table and the post hoc table (venue factor 7, 5 → 5, 4; carried half-widths 5, 6 → 4, 4). Only the word "처음" is wrong (finding 1).
  - **g3-22.** Matches the campaign record: line 12 (GIMP repeats 8–13, not pooled), lines 42 and 69 (2026-10-31, re-pooled by origin), line 25 (11.3's row), the 11.3 section and line 564. The overview's header reads `Updated 2026-11-21`.
  - **g3-23.** Matches the campaign record's Campaigns table, which has 15 tags with `meas-ci:background:2026-11-20` last, and §9 of the overview, which lists `meas-ci-background-2026-11-20`.
  - **g3-24.** Follows R1. It matches the 2026-11-14 changelog entry (`simulator@0d323c84470a`, `daemon@62c71f0d2de0`, the hand fixtures for (a), (b), (c), (g), (i), (j), and the black-box unit tests under `simulator/tests/` for (d), (e), (f), (g), (i), (h)) and decision 6 of the 9.16 spec ("the check for 인경민 to run once each item lands").
- **Form.** The new text is in Korean with `-습니다` endings, and no new section is added. No sentence is about the sweep. Three open-spot boxes are handled per spec decision 9: the §7.5 box is removed, and the §8.5 and §14.2 boxes are narrowed to what is still open. The "미실행" markers are removed in §7.5 and §8.6, each outcome carrying its date and its record.

## Notes (no fix required of K3)

- **The overview quotes need a re-read after K8.** Lines 961 and 967 quote `docs/workload/measurement-overview.md` as rows g0-16 ("5 to 107") and g0-15 ("15.7–83 %") will make it. Today the overview still reads "5 to 77" and "40–83 %". The quotes are exact only if K8 keeps the sentences and changes just the numbers. Read the two quotes again after K8 lands.
- **"runner" is worded two ways.** Line 713 says "같은 runner이되 kernel …", while line 824 says "runner가 바뀌어 생긴 차이는 6.2절". Neither is false: the run record says "The runners had moved to kernel `7.0.0-1017-azure`". A reader may still stumble on the pair. "runner의 kernel이 바뀌어 생긴 차이" at line 824 would align them.
- **Chapter 5 line 1117 stays true after K9.** The line says the plan's When table was left untouched as development history. It remains true after K9's g0-13 restates that table's When cell, because g0-13 keeps the row's number "0", as row g3-02's flag judged.

## Main session, 2026-11-21

The finding at `06-grounding-measurement-verification.md:1059` applied: "처음" dropped; the cold smoke of 2026-11-14–15 ran the variants before the RQ0 run (`_dev/research/jioh/task-10.4-cold-smoke-and-cost-response/second-smoke/run-times.csv`). The two quotes of the measurement overview are re-read after K8.
