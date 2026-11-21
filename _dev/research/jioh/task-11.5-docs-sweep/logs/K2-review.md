# K2 · Dataset guidebook 8 and 3 — review

Reviewed: `git diff -- docs/guidebook/dataset/08-decision-chronicle.md docs/guidebook/dataset/03-timeline-to-canonical-workload.md` against `rows/g2-dataset-guidebook-08-03.md`, the work list (R1–R7, Q1–Q7, Rows by file, the paragraph under Q7 on the phases "directly related to the dataset"), the editor brief and `logs/K2.md`.

**FINDINGS — 5** (four on the edits; one sentence beside an edit that no row names)

## Findings

### 1. `docs/guidebook/dataset/08-decision-chronicle.md:1859`: g2-09 says all eight items closed, then says item 2 did not

- **What is wrong.** The new text reads "여덟 항목은 아래처럼 닫혔습니다. 2는 닫히지 않고 Backlog로 옮겨졌습니다." The first sentence is false, because item 2 moved and did not close, and the second sentence contradicts it. The row's draft carried the same slip ("여덟 항목은 아래처럼 닫혔습니다(2는 Phase 10 밖으로 옮겨짐)").
- **Record.** Work list R2. Phase 10 spec, decision 9: "The Layer 1 and RQ4 item of the old Phase 10 list moves to the Backlog".
- **Fix.** "여덟 항목 가운데 일곱은 아래처럼 닫혔고, 2는 닫히지 않고 Backlog로 옮겨졌습니다."

### 2. `docs/guidebook/dataset/03-timeline-to-canonical-workload.md:11`: g2-27's "2026-11-21까지" claims more than the volume reflects

- **What is wrong.** "그 뒤 2026-10-17까지 바뀐 것(…)" became "그 뒤 2026-11-21까지 바뀐 것(…, 2026-10-31에 … re-bless, 2026-11-21의 second bless 뒤의 `c2-p1a` 학습 job)은 해당 절에 반영했습니다." Widening the date makes the parenthesis read as every change through 2026-11-21. It does not cover one compile change. Since 2026-10-31, each operation window has also carried that operation's measured largest run once, at the window's start, on its channel. §4.5 and §11.2 do not state this. They still say only that the operation's own components replace the usual ones (lines 639 and 1597). The volume never mentions `largest_run`.
- **Record.** `harness/CHANGELOG.md`, 2026-10-31, "each measured operation's largest run carried once per window"; `_dev/docs/spec/jioh/timer-wakes-by-origin.md`, decision 17; `dataset/tools/wlc/compiler.py:364` (`largest_run`, `largest_run_channel`).
- **Fix.** Keep the dated list as it stood and add the two later members without a completeness claim, for example: "그 뒤 2026-10-17까지 바뀐 것(… docstring)과, 2026-10-31에 측정된 프로그램 자신의 wake를 시작점에 따라 나눈 re-bless, 2026-11-21의 second bless 뒤의 `c2-p1a` 학습 job은 해당 절에 반영했습니다." Writing the largest-run carry into §4.5 or §11.2 would need a row of its own.

### 3. `docs/guidebook/dataset/08-decision-chronicle.md:1989`: g2-23's 2026-11-14 row says the second smoke ended without failure

- **What is wrong.** The cell reads "10.4: cold smoke(seed 둘, 129개 파일의 1,197 run; 둘째 smoke가 실패 없이 끝남)". The second smoke's 1,197 runs finished with none failed. The smoke itself was then stopped inside the guards stage before `guards.csv`, which is why the end stages were measured on the 2026-11-15 rerun. Chapter 8's own item 8 (line 1875) words this correctly: "22:20:57에 1,197 run을 실패 없이 끝냈습니다".
- **Record.** `_dev/research/jioh/task-10.4-cold-smoke-and-cost-response/README.md`, "The second smoke": "The 1,197 runs finished at 22:20:57, none failed. … stopped 2026-11-15T07:52:30 (exit 143) inside the guards … before `guards.csv`."
- **Fix.** "둘째 smoke의 1,197 run이 실패 없이 끝남".

### 4. `docs/guidebook/dataset/08-decision-chronicle.md:1759`: g2-06's 2026-11-21 re-reading leaves out 12.2's pin list

- **What is wrong.** The new member lists what this pass corrected: "12.4의 여덟 항목과 그 열린 자리, 12.2의 열린 자리, 12.5의 hold time 측정 시기, 12.7의 조건부 재측정". The same pass also rewrote 12.2's list of manifests and pins (line 1799, g2-07), adding every RQ0 gate spec re-pin after 9.16 and the second bless. It also restated that list's "최종 pin" sentence (line 1843). The neighbouring members name their content at this level of detail.
- **Record.** This chunk's diff (hunks at 1799 and 1843); `logs/K2.md`, g2-07.
- **Fix.** "…12.2의 pin 목록과 열린 자리, …".

### 5. `docs/guidebook/dataset/08-decision-chronicle.md:1849`: "reference simulator가 아직 구현하지 않은 executor 규칙" left in the passage of the narrowed box (no row)

- **What is wrong.** The box directly under this paragraph (line 1851, g2-08) now states that (b), (d), (e) and (g) are implemented and that the 2026-11-14 integration gate showed (a)–(j) on the binary. The paragraph it points to ("위 목록의 문장들") still says, in the present tense, that those statements depend on "executor 규칙" that the reference simulator "아직 구현하지 않은". Item 2 of the fifteen, the integration gate, overtakes this sentence. The editor saw it and logged it as "not a row" (`logs/K2.md`, "For 인지오"). Applying a fix needs a new row.
- **Record.** `harness/CHANGELOG.md`, 2026-11-14, "the integration gate passed…" (where each item is shown).
- **Fix.** Dating the clause is enough: "…참인지가 그때(2026-10-17) reference simulator가 아직 구현하지 않은 executor 규칙에 달린 것은…".

## Checked and in order

- **The caller's four checks.**
  - **Chapter 8 §12.4.**
    - Every item keeps its place and its body. Items 1 and 3–8 each gain "— 닫힘." inside the bold heading, in chapter 3's form (`**2. … — 닫힘.**`, `**8. 종료 감사 — 닫힘.**`). Each then states its outcome with its date and its record.
    - Item 2 gains "— Backlog로 옮겨짐." and quotes Phase 10 spec decision 9 verbatim (R2).
    - The box under the items is removed. None of its matter is still open: the start's dependencies, (g), (h) and (j), the cost response, and the trace-replay pre-registration. The passage states the outcome as text, per decision 9: Phase 10 opened on 2026-11-01 on `daemon/daemon.py`, then the gate, the cost response and the run, ending fail, 6 of 19, provisional. After that it gives the final verdict of 2026-11-21 (5 of 19), the post hoc 4 of 19, the route and Phase 12. Each fact checks against `docs/rq0-run-record.md` and the Phase 10 and Phase 11 specs (Phase 10 decisions 2 and 3; Phase 11 decision 1).
  - **The per-statement checks.** They stay open with owner 인경민, per R1: in the narrowed box at chapter 8 line 1851, and at chapter 3 line 2255 (item 8, 종료 감사). `uncheckable-by-item.md` has no later record of those checks.
  - **The phase lists.** Both read 1, 2, 3, 7, 9, 11 (chapter 8 lines 54 and 2001). No added text calls the 2026-10-31 rebuilds Phase 10's. In 12.2's pin list they are named by content, and in chapter 3's records table the row is "9.24, timer-wakes-by-origin spec". `_dev/TODO-done.md` line 186 files 9.24 with both of that day's rebuilds, and commit `14b96641` made that move.
  - **The `c2-p1a` training job.** The SHA-256 of `dataset/build/coreset-single/c2-p1a.workload.json` is `0678efa68cef…`, equal to the `dataset/build.manifest.json` entry. The hog's program has 96 instructions (RUN 48, SLEEP 47, EXIT 1). Its first four are RUN 191, SLEEP 472, RUN 159, SLEEP 450. The largest RUN is 560,069,421 µs (9.33 min), and the RUNs sum to 1,389,885,000 µs. In `dataset/archetypes.yaml` lines 1256–1259, under header line 46's order (`p1, p5, p10, p25, p50, p75, p90, p95, p99, p99.9`), `python3_run`'s p90 is the seventh value, 204,750,672, and its max is 1,297,955,204. `python3_block`'s min is 1, so `_quantile_sample` (`dataset/tools/wlc/sampling.py:95`) never draws a zero and the merge never fires. The editor rightly fixed the draft's "p90 1,177,733,035", which is the p99.9. The `cpu-batch` scope supports "every other value of the program is the 9.10 campaign's".
- **Coverage.** All 28 rows due are applied:
  - Chapter 8: g2-04, -05 and -08 to -21; under Q1, g2-01, -06, -07, -23 and -24.
  - Chapter 3: g2-28, -30, -32 to -34 and -36 to -38; g2-27 and -29 under Q1; g2-31 and -35 under Q2.

  The rows to be left are untouched: g2-03 and g2-25 under Q4 (lines 695 and 2116), and g2-02, -22 and -26 as D rows (lines 59, 1930 and 109).
- **Scope.** Every hunk maps to a row. The hunk at chapter 8 line 1843 changes "항목 끝에" to "항목에", which g2-07 makes necessary. Both headers read `Updated 2026-11-21`.
- **Records**, checked against the record itself:
  - **12.2's pins.** Every hash in the post-9.16 pin list matches its `harness/CHANGELOG.md` entry: 2026-10-30 (`7029308e`, `1c738540`, `205add64`), the 2026-10-31 entries in their order, 2026-11-01 (`58c1107e`, `4fe86c3f`, `9295b76e`) and 2026-11-14 (`f693bfbe`, `6cbae471`, `1020d6ab`, `38f8de5e`, the two versions). `rq0-gate.yaml` `pins` still holds `27d347bc`/`de9802e7`. The committed manifests hash to `9f30ea8f…` and `3438be7f…`, and `rq0-config-search.yaml` pins `9f30ea8f…`.
  - **The 2026-11-11 stages.** AA, AB, AC and (h) match `simulator/memo/memo_261111.md` Parts B–E. That includes `c1-compile`'s `build` ending at 1,514,650,775 µs, which g2-33 adds.
  - **Stages AD and AE.** They match the 2026-11-13 memo's TL;DR and Parts K1 and L4.
  - **Cost and cold smoke.** The cost figures (14,031,957 rows, 7.5 min, 9.4 GB, 40 min past 15 GB) and the smoke figures (13:04:18, 1,151, 153, 18:54:22, 22:20:57, 50.33 h, 273.5 GB, 30.59 h over 112 runs) match the 2026-11-14 and 2026-11-15 changelog entries and the 10.4 README.
  - **The RQ0 run.** Its figures match `docs/rq0-run-record.md`: trace replay 0.377/0.367, 0.279/0.261, 1.121/0.475 and 0.254/0.000; post hoc 0.000/0.000; headroom 17 and 12 of 19; cap band 6, 6, 7, 7 and post hoc 4, 4, 4, 5; 45 h 26 min; the contingency 5 to 6 and 2.512 → 0.000; 55.27 s ±5.89 % and 403.96 µs ±2.15 %; final 5 of 19; 470 configurations, 4,700 runs, 8 of 10 at finding 3.
  - **The contingency quote.** "the training run's runs between blocks and block per run" is in the `re-measurement-contingency` statement of `rq0-gate.yaml`.
  - **The 2026-11-21 campaign date.** It matches `campaign/method.md` ("2026-11-21, the campaign's result").
  - **The spec decisions.** Phase 10 decisions 6, 7 and 9 and Phase 11 decisions 1 and 10 match the specs.
  - **The daemon.** `daemon/daemon.py:70` holds `def projection`. The 10.2 README's `daemon` part reads "schedule and log compared byte for byte".
  - **The fixtures and tests.** `fix-object` and `fix-tree` and `simulator/tests/test_spawn_children.py` are item (g)'s evidence, per the 2026-11-13 changelog entry and §2 of the 2026-11-15 memo.
  - **The starvation net.** The decision matches §7 and the TL;DR of the 2026-11-15 memo, and the two unread waits match the 2026-11-15 `sensitivity-lines` entry.
  - **Chapter 13's added rows.** They check against the memos and the changelog they cite, including memo_261021 H2, memo_261024 Parts A and B, and memo_261023 Part B (Q2). One exception is finding 3.
- **Form.**
  - **Language.** The new text is in Korean with English terms and `-습니다` endings. No section is added, so chapter 13's new rows are rows only (Q1).
  - **Sweep sentence.** Only the guidebook's own list of re-readings names this pass (Q1).
  - **Boxes.** They are handled per spec decision 9:
    - Removed: chapter 8 lines 1318 and 1877, and chapter 3 line 1222.
    - Kept and narrowed: chapter 8 line 1851, to the per-item checks.
    - Kept with its one changed place: chapter 8 line 1893.

## Outside the rows (for the main session)

- **Chapter 3's two `meta` examples show the 2026-10-17 library hash.**
  - Lines 866 (`c1-office`) and 1096 (`c2-p1a`) show `"archetypes": "archetypes.yaml@c78d8cf911ecd820413602226ea8adb71945edd1"`, the library at `1a092508`.
  - Both committed artifacts carry `archetypes.yaml@a25178d113f04f0ee2b03aa3d1228f02c2880186`, the library after the second bless (`2e3fade3`).
  - The hash went stale on 2026-10-31, outside the fifteen items, and changed again at item 10.
  - §6.2 now presents `c2-p1a`'s program as the post-second-bless one, so its §7.2 `meta` disagrees with it.
  - No reader row names these lines, and the second search's terms would not find a hash.
- **12.5's "Backlog의 데이터셋 관련 줄은 다섯입니다"** (line 1881) and the box at 1893 ("다섯 backlog 항목").
  - Item 2 now reads "Backlog로 옮겨짐", and 12.4 counts it among the "데이터셋과 관계된" items.
  - `_dev/TODO.md`'s Backlog holds that line (the "Layer-1 and RQ4 items of 9.12" line).
  - The editor logged it for 인지오, and so did row g2-11's flag.

## Main session, 2026-11-21

The five findings applied by the editor (logs/K2.md, "Review fixes"); each fixed line read in the files.
