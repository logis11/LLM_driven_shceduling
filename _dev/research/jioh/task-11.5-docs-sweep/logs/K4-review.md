# K4 review — dataset guidebook 2, 4 and README

**FINDINGS — 1**

Read against: the task spec, the work list (R1–R7, Q1–Q7, the "Rows by file" table), `rows/g4-dataset-guidebook-04-02.md`, `logs/K4.md`, the editor brief, and `git diff` of the three files.

## Findings

### F1 — the second bless rebuilt all 78 variants, not fourteen
- **Where:** `docs/guidebook/dataset/04-the-coreset.md:1969` (g4-09): "둘째 bless가 variant 78개 가운데 `python3`를 담은 열네 개를 다시 build해, 지금의 `dataset/build.variants.manifest.json`은 이 pin과 hash가 같지 않습니다." The same slip at `04-the-coreset.md:15` (g4-13): "`python3`의 block 값 둘을 다시 잰 뒤의 rebuild로 바뀐 세 파일의 byte 수".
- **What is wrong:** the bless rebuilt every variant and every core file. Fourteen variants, and three core files, changed in more than the library's hash. As written, line 1969 says only fourteen were rebuilt, and line 15 says only three files changed. In fact every artifact changed in its library hash, and only these three changed in byte count.
- **Record:** `harness/CHANGELOG.md`, 2026-11-21 re-measurement entry, "The second bless": "the core set, the 78 sensitivity variants and the five generated sets rebuilt on the re-measured library. Beyond the library's hash: 3 of the core set's 51 …, 14 of the 78 variants (those of the three)". `docs/rq0-run-record.md`, Corrections 2026-11-21: "The second bless rebuilt the core set, the 78 sensitivity variants and the five generated sets; beyond the library's hash only files holding `python3` changed". `_dev/research/jioh/task-11.3-the-re-measurement/bless-report.json`: `build.variants.manifest.json` has artifacts 78 and `beyond_hash` 14; `build.manifest.json` has 51 and 3. The current core artifacts' sizes equal chapter 4's stated byte counts for every file but these three (checked).
- **Fix:**
  - Line 1969: "…뒤의 rebuild(둘째 bless)가 variant 78개를 다시 build해(library의 hash 말고도 바뀐 것은 `python3`를 담은 열네 개), 지금의 `dataset/build.variants.manifest.json`은 이 pin과 hash가 같지 않습니다."
  - Line 15: "…다시 잰 뒤의 rebuild로 byte 수가 바뀐 세 파일의 byte 수와, …" (or: "…rebuild 뒤 byte 수가 바뀐 세 파일…").

## Checked and clean

- **Coverage.** These rows are applied: g4-01–07, 09, 12, 13, 15–18, 20–24, 27. These are untouched, per their disposition: g4-08 and g4-28 (Q4), g4-10, g4-11 and g4-25 (Q3), g4-14 and g4-19 (D), and g4-26 (outside the sweep). Line 660 carries both g4-18 and g4-19, and only g4-18's cell (the examples cell) changed.
- **Scope.** Every hunk maps to a row or to the header line. Nothing else in the three files changed.
- **Records.** Each figure was opened at its source and matches:
  - **Byte counts.** 24,217,608, 1,472,070 and 20,825,678 are the file sizes. Their SHA-256 values equal `build.manifest.json`.
  - **Utilizations.** They equal the manifest's `demand` entries.
  - **The first 11.3 table** (from the RQ0 run record, 2026-11-21): 55.27 s ±5.89 % (30.6–121.2 s) and 403.96 µs ±2.15 % (233–504 µs); 11–46 blocks, `khugepaged` 9–44, the start sleeps in 91 repeats, one `migration/1`; `provjobd` 2,890–8,343; 1,413.843 s ±0.34 % (all also in `campaign/method.md` §5).
  - **Quantiles** (`archetypes.yaml` `python3_run`): p50 1,223, p75 20,473,778, max 1,297,955,204 µs.
  - **Campaign count.** `meas-releases.yaml` has 24 campaigns, against 23 at `2487ba27^`.
  - **The 10.4 figures** (10.4 README; `harness/runner.yaml` `heavy_workers: 1`): 213 s, 110 s, 124 s, 9.4 GB, past 15 GB and swapping on 16 GB, `heavy_workers` 1, 50.33 h, `c6-dual` 30.59 h over 112 runs.
  - **The RQ0 run.** 45 h 26 min, 19,425 runs, run cold and once.
  - **The verdict** (fail, final, 5 of 19, the five files named, K = 10; 6 of 19 provisional as run).
  - **The pins.** The re-pin sequence 8e2948b1 → 4cb07941 (`0a941e1a`) → de9802e7 (`db2fda65`) comes from the history of `rq0-gate.yaml` line 665. The RQ0 run's report pins table shows de9802e7, and the current manifest is 3438be7f, which no longer matches.
  - **The tables.** `carried_values` source strings and the 9.6 D29 split between the two rows match. The count of 19 carried-value rows is correct. The 11.3 spec's decisions 5–10 are counts, fresh repeats, method, fold-in, status and second bless.
  - **Other dates.** `measurement-overview.md` has `Updated 2026-11-21` at HEAD. Commit `05f7a220` re-read every count, size and utilization and touched all eight volumes.
- **Check 1, chapter 4's table of the phases and sub-tasks the volume names (14.7).** Every added row names a phase or sub-task that the volume's prose names:
  - 3.2 (lines 924, 1564);
  - Phase 8 (236);
  - 9.4 D9 (1922);
  - 9.5 D57 (1939);
  - 9.6 D4 (775);
  - 9.7 D3 (627);
  - 9.8 D6 (712);
  - 9.9 (915);
  - 9.12 D105 (194);
  - 9.22 (1969);
  - Phase 10 (1572, 1875);
  - 10.4 (1572);
  - Phase 11 and 11.3 (800).

  Each description matches its `_dev/TODO-done.md` or `_dev/TODO.md` line: Phase 8's heading and stage line; Phase 10 opened 2026-11-01 and closed by 10.6's "Done 2026-11-18"; Phase 11's heading, opened 2026-11-18. The volume names no other phase or sub-task the table lacks: 9.1–9.3, 10.1–10.11 and 11.1–11.6 appear only as section numbers or values, and 9.24, 9.25, Phase 1 and Phase 4 do not appear.
- **Check 2, the 2026-10-31 rebuilds.** No passage in the three files names their phase. Chapter 4's opening paragraph and line 1969, and the README's line 7, each name them by date and content: wakes split by origin onto `timer:` and `event:`, and each operation's largest run carried once per window. These descriptions match the two 2026-10-31 changelog entries. Chapter 4's table row for Phase 10 does not mention them.
- **Form.** The edits are in Korean with the files' own sentence endings, and table cells keep note form. No section was added. The only passages about correction passes are the two Q1 lists of them: chapter 4's opening paragraph and the README's line 7. The open-spot box at `04:1571` was removed, and its outcome is stated with dates and records. Each of the three headers reads `Updated 2026-11-21`.

## Notes for the main session (not findings)

- **`04:2372`, the Phase 11 row "(2026-11-18부터)".** It is true while Phase 11 is open. When this sweep closes the TODO, the row could gain its end date, as the Phase 10 row has.
- **`04:986`, the decisions listed for `c2-p1a` (정한 결정).** The list has no 11.3 bullet, though the file was rebuilt on 11.3's values; `c1-ml-train` gained one (g4-03). There is no row for it, so it is a candidate absence (spec decision 6) for 인지오.
- **`02:1453`, the 2026-10-31 row of chapter 2's rebuild-order table (재건의 순서, section 11.4).** It names only the wakes-by-origin rebuild, not the same day's largest-run rebuild (timer-wakes-by-origin spec, decisions 17 and 18). That gap is outside the fifteen items and is not a Q1 row, so it is left for 인지오.
- **`04:87`, sub-task 2.5.** The volume names it only inside an archive path, which is not a sub-task named in the prose, so the table is right not to list it.
- **`02:1027`, "가끔 … `khugepaged`가 잠깐 막을 때만 멈춥니다".** It agrees with `archetypes.yaml`'s scope after the fold, where the agent's waits count as part of the run. No change is needed.

## Main session, 2026-11-21

F1 applied at both places: line 1969 now says the second bless rebuilt all 78 variants, fourteen changing beyond the library's hash; line 15 names the three files whose byte count changed.
