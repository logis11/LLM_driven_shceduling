# Second-search review — g7-35, g3-26, g5-46, g5-47 and the integration-gate gloss

Reviewed 2026-11-21 against commits `219aee71`, `f8f070e2` and `d7e4643b` (`git show`), the rows files `rows/g7-workload-contracts-simulator-daemon.md`, `rows/g3-dataset-guidebook-05-06.md` and `rows/g5-research-guidebook-and-claims.md`, the work list, the task spec and the editor brief.

**FINDINGS — 3**

## Findings

### 1. g5-46 and g5-47 contradict three D rows on the same matter, and volume 3 now says both

- **Where:** the edit is at `docs/guidebook/vol-03-the-research.md:640`. The left lines are:
  - `docs/guidebook/vol-03-the-research.md:1339`, "설정에 있는 상한은 batch class의 상한 하나이고, 시뮬레이터는 아직 그것을 집행하지 않습니다." (row g5-03, D)
  - `docs/research-proposal.md:480`, "which the executor is to enforce (not yet implemented)." (row g5-31, D)
  - `docs/terminology.md:142`, "enforcing the batch class's cap (to be implemented)." (row g5-36, D)
- **What is wrong:**
  - g5-46 counts "시뮬레이터는 아직 이 값을 읽지 않습니다. 구현해야 할 항목입니다" as overtaken by item 2, the integration gate showing conformance item (d), the cap, on the binary.
  - g5-03, g5-31 and g5-36 say the same thing about the same item (d). The work list leaves all three as "stale before Phase 10, no item".
  - K5's editor and reviewer had also classed lines 640 and 1111 that way: D-type, no row (`logs/K5.md:76–77`, `logs/K5-review.md:35`).
  - The two classifications cannot both hold. After `f8f070e2`, volume 3 says the cap is enforced at lines 640, 1103 and 3796, and not yet enforced at line 1339.
- **Record:**
  - `docs/memos/2026-09-09-batch-class-rule-for-the-simulator.md`, status line: item (d) "is in it since stage V (2026-10-20)".
  - `harness/CHANGELOG.md`, 2026-11-14 "the integration gate passed": (d) is shown by black-box unit tests on the binary under `simulator/tests/`.
- **Fix:** give the matter one disposition. The recommended way is to re-row g5-03, g5-31 and g5-36 as A rows on item 2, with g5-46's records, and apply them:
  - line 1339: "…상한 하나이고, 시뮬레이터는 2026-10-20부터 그것을 집행합니다."
  - research proposal: "which the executor enforces (the reference simulator since 2026-10-20)", the form `docs/terminology.md:119` already uses.
  - terminology: "(the reference simulator since 2026-10-20)".

  Both status headers already read `Updated 2026-11-21`. 인지오 reviewed these three as D rows, so the change is his to confirm (spec decision 12: what he overturns becomes a new row). The other way is to put g5-46 and g5-47 back to D and revert `f8f070e2`, but then lines 640 and 1111 stay false.

### 2. g7-35's reasoning also covers dataset guidebook chapter 3, line 1096, and that line has no row

- **Where:** `docs/guidebook/dataset/03-timeline-to-canonical-workload.md:1096`. This is §7.2, "`meta`: 출처", which reads `"sampled": {"archetypes": "archetypes.yaml@c78d8cf911ecd820413602226ea8adb71945edd1", "seed": 201}` for `c2-p1a`.
- **What is wrong:**
  - Like the coreset guide's §6.1 before g7-35, this is the `c2-p1a` meta with no date. `c78d8cf9…` is the library at 9.16 (`git rev-parse 17f28d7f:dataset/archetypes.yaml`).
  - The same chapter, at line 986, shows `c2-p1a`'s hog program as the second bless built it (RUN 191, SLEEP 472). So the chapter shows one file from two builds. That is exactly the case g7-35 corrects ("as its program lines already are").
  - K2's reviewer handed this line to the main session (`logs/K2-review.md:78–83`).
  - Line 866 (`c1-office`) is dated "(2026-10-17 tree …)" at line 870, so it can stay.
- **Record:**
  - `dataset/build/coreset-single/c2-p1a.workload.json`, `meta.sampled.archetypes` = `archetypes.yaml@a25178d113f04f0ee2b03aa3d1228f02c2880186`.
  - That file's SHA-256 `0678efa6…` is its entry in `dataset/build.manifest.json`, and `git rev-parse HEAD:dataset/archetypes.yaml` = `a25178d1…`.
- **Fix:** add a row (A, item 10) and write the full hash at line 1096: `a25178d113f04f0ee2b03aa3d1228f02c2880186`. The chapter's examples print all 40 hex digits.
- **Related, for 인지오:** `docs/data-contracts.md:224` (row g7-15, D, "the text dates itself ('at this writing')") holds the same `c2-p1a` value, `c78d8cf…`. "At this writing" under a header that reads `Updated 2026-11-21` now reads as 2026-11-21.

### 3. In volume 3, the gloss's "계약" does not say which contract

- **Where:** `docs/guidebook/vol-03-the-research.md:640`, "통합 gate(실제 시뮬레이터와 daemon으로 첫 관문 실험을 돌리기 전에, 계약이 요구하는 행동을 하나씩 확인한 점검)".
- **What is wrong:**
  - Up to line 640, the only contract volume 3 names is the 공유 계약, the recognizer's `system` block (lines 350 and 529). The gate does not check that block.
  - Volume 3 never names the contracts the executor is held to: the data contracts and the interpretation contract.
  - So the gloss explains one term with another the volume has not explained.
  - Volume 4's gloss is fine. It follows "데이터 계약은 실행부가 idle 등급을 … 지키도록 정합니다" in the same paragraph.
- **Record:** `harness/experiments/rq0-gate.yaml`, statement `simulator-conformance`: "Every consumer this spec pins is written against the ratified contract … Before the RQ0 run the simulator must show: (a) … (j)".
- **Fix:** name what was checked without the bare word, e.g. "…돌리기 전에, 시뮬레이터가 지켜야 한다고 문서로 정해 둔 실행 규칙을 하나씩 확인한 점검". Low severity.

## Checked and passing

- **Coverage and scope.**
  - `219aee71`: one hunk for g3-26 (chapter 6:1691) and one for g7-35 (coreset guide:399).
  - `f8f070e2`: one hunk for g5-46 (volume 3:640) and one for g5-47 (volume 4:1111).
  - `d7e4643b`: the gloss, one hunk in each volume.
  - Nothing else in the files changed.
- **g7-35.**
  - The artifact's `meta.sampled.archetypes` is `a25178d1…`, and its SHA-256 `0678efa68ceff929…` equals the manifest's entry.
  - `derived_from` `a0effee9…` still equals `git rev-parse HEAD:dataset/timelines/coreset/c2-p1a.timeline.yaml`.
  - The block now agrees with line 5's source note and with §6.4's hog line (RUN 191, SLEEP 472).
- **g3-26.**
  - 2026-10-17 is the 9.16 grill's date (`_dev/docs/spec/jioh/task-9.16-exit-audits.md`, line 3). Chapter 6 itself says so two paragraphs above.
  - The form matches chapter 8:1849 (g2-39). The box under the passage, at line 1719 (g3-24, per R1), carries the per-statement checks still open.
- **g5-46.**
  - Stage V on 2026-10-20 is from the batch-class memo's status line.
  - "2026-11-14 … 실행 파일 위에서 보였습니다" is from the `harness/CHANGELOG.md` entry of 2026-11-14, which shows (d) by black-box unit tests on the binary, and from the `test_cap_ceiling.py` row of `docs/memos/2026-11-15-integration-gate-and-cold-smoke.md`.
  - The passage's other sentences hold. "다른 작업이 실행을 기다리고 있을 때만 걸리는 상한" still holds after stage AE, the cap beside the idle class, because AE narrows the condition without breaking "only when" (`simulator/memo/memo_261111.md` L4).
- **g5-47.**
  - Stage Z on 2026-10-28 is from the declared-class memo's status line, and the gate's showing of (e) is from the same `harness/CHANGELOG.md` entry and the memo's `test_idle_class.py` row.
  - The rest of the passage holds: `c2-p1b` is report-only (`rq0-gate.yaml`, the six idle-class files).
- **The gloss.**
  - Each volume uses "통합 gate" or "integration gate" only once, so the gloss sits at the first use in both.
  - "첫 관문 실험" in volume 3 follows the volume's own usage before RQ0 is glossed at line 1586.
- **Form.**
  - Korean, in each file's sentence endings. No new section and no sentence about the sweep.
  - Volumes 3 and 4 have no status header and no section-number cross-references.
  - Chapter 6 and the coreset guide read `Updated 2026-11-21`.
  - No suite reads any of the four files.

## Notes (not findings)

- The gloss hunks in `d7e4643b` have no row in any rows file. Adding them to g5-46's and g5-47's "Becomes" lines would put every hunk in the sweep's record.
- The gloss covers the conformance half of the gate. The gate's four parts also include the daemon byte-identical to the mock daemon on the 19,425 runs, and the short run through the smoke tool (`harness/CHANGELOG.md`, 2026-11-14). The gloss is not false, only partial.
- Volume 4:1111 now says "RQ0을 돌리기 전에" twice in one sentence, once for the spec's requirement and once in the gloss. Rewording is optional and only a matter of style.

## Main session, 2026-11-21

- F1 applied for consistency with g5-46: g5-03 (`vol-03-the-research.md:1339`), g5-31 (`research-proposal.md:480`) and g5-36 (`terminology.md:142`), each a D row on the cap "not yet" enforced, now read as overtaken by item 2 with Q2's earlier fact — the cap enforced since stage V (2026-10-20), shown on the binary by the integration gate (2026-11-14). `terminology.md`'s header set to Updated 2026-11-21.
- F2 applied as a new row, g2-40: chapter 3 §7.2's `c2-p1a` meta to `archetypes.yaml@a25178d113f04f0ee2b03aa3d1228f02c2880186`, the committed build's (`dataset/build/coreset-single/c2-p1a.workload.json`).
- F3 applied: the gloss names the contract — in volume 3 "그 실험의 명세가 시뮬레이터에 요구하는 행동", in volume 4 "RQ0 gate spec이 시뮬레이터에 요구하는 행동" (statement `simulator-conformance`).
