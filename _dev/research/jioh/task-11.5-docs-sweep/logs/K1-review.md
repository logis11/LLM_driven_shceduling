# K1 · Dataset guidebook 7 and 1 — review

**FINDINGS** (4, all small; no wrong number, no missing row).

Read: the task spec, the work list (R1–R7, Q1–Q7, the table), `rows/g1-dataset-guidebook-07-01.md`, `logs/K1.md`, the editor brief, and `git diff` of both files.

## Checked and holding

- **Coverage.** Every row that has to be applied is applied: ch7 g1-01 – g1-22, ch1 g1-25, g1-27 – g1-38, g1-40. The rows to be left are untouched: g1-23 (the CI triggers), g1-24 (ch7:633 "두 곳에서" kept), g1-26 (ch1:508), g1-39 (ch1:1460).
- **Scope.** Every hunk maps to a row. The relabels "Phase 10" → 9.24 (ch7 3.7's pin row and the generated table's two headers) follow the coordinator's instruction and the work list's Q1 note. Commit `14b96641` (2026-11-01) moved the 2026-10-31 items into Phase 9, and `_dev/TODO-done.md:186` files them as 9.24. Neither file has a "Phase 10" label for those rebuilds any more.
- **Hashes.** `git show <rev>:<manifest> | shasum -a 256` for all seven manifests:
  - At HEAD (= `2e3fade3`, the last commit to touch them): `9f30ea8f`, `3438be7f`, `d6ded38a`, `2189c0d2`, `879fd4d8`, `6091e382`, `b465bfbe`.
  - At `2e3fade3~1`: `27d347bc`, `de9802e7`, `eee6a020`, `b593144c`, `e3a94dc8`, `07d59e41`, `2b99f65e`.
  - These match every value the edit writes.
- **Library rows.** Each library row was recomputed with `git rev-parse` and `shasum`:
  - `658d7124` → `6267dbde`/`83faeac5`
  - `bb16f63a` → `aa2f8842`/`85570c57`
  - `2e3fade3` → `a25178d1`/`34efc7de`
  - The dates are 2026-10-31, 2026-10-31 and 2026-11-21.
  - No library commit since `1dc4af4d` is missing from the table.
- **`c1-dev`.** On disk: `fe5c4407`, report `42b34a07`, utilization 0.3319. `meta` holds `@7450b5e9`/`@a25178d1`.
- **Pin lists.** The RQ0 gate spec's `pins` (`rq0-gate.yaml:654–668`) equal the quoted block line for line. The configuration search spec's `pins` (`rq0-config-search.yaml:258–264`) match the new paragraph: second bless core manifest, prior table, scoring spec, guard spec 1.4, `simulator@841dc81131cb`, `daemon@62c71f0d2de0`, no variants pin.
- **Changelog Pins lines.**
  - 2026-10-31 ×2: `d80f06e0`/`4cb07941`, then `27d347bc`/`de9802e7`.
  - 2026-11-01: the three tables `58c1107e`/`4fe86c3f`/`9295b76e`.
  - 2026-11-14: `f693bfbe`, `6cbae471`/`1020d6ab`/`38f8de5e`, the two versions, the dataset unchanged.
  - These match ch7 1.7, 3.3 and 3.7 and ch1 7.5. The re-attribution of the dataset and variants pins (Q2) is correct.
- **Lists made whole (Q1).** Each added member checks out against its record:
  - **The ch7 ladder.** 9.17's line matches the 2026-10-11 9.17 entry's Pins line. The 9.24 ×2, 10.1, 10.2, 11.3 ×2 and 11.4 lines match their entries.
  - **The ch7 library table.** Covered under "Library rows" above.
  - **The ch1 chronology.** The 9.23 row matches the 2026-10-14 and 2026-10-15 entries (`c5f7fa5a`, `81d3213d`). The 9.24 and 11.3 rows match theirs.
  - **The ch1 Phase N list.** It gains Phase 11 only, as the work list's Q1 note says.
- **The 11.3 row's numbers.** 55.27 s ±5.89 %, 403.96 µs ±2.15 %, 3 of 51, 14 of 78, and 49/480, 70/720, 22/272, 5/66, 0/24 all match the 2026-11-21 entry. I diffed the generated manifests at `2e3fade3` against `2e3fade3~1`: every artifact moved; `inputs` moved on `dataset/archetypes.yaml` alone; `grid`, `demand` and `reports` are equal.
- **Experiment lint.** `harness/tools/experiment_lint.py` works as ch7 3.5 describes:
  - A spec counts as executed when `<experiment>/runs.sha256.csv` exists, and for a search spec when `<search>/report.json` exists.
  - A failed `pins/` check is printed as a note; every other error stays an error.
  - `_pin_errors` (`evaluator.py:92`) does not read `simulator` or `daemon`; `program_pin_errors` (`runner.py:685`) does.
  - Running it today gives the quoted output: two summary lines, both ending in "executed", two notes, and `lint clean`.
- **Other facts.**
  - `harness/Makefile` has 27 lines; the quoted block matches it, with `PY` and `.PHONY` left out as before.
  - `test_runner.py` has 9 `@needs_build` tests; there were 5 at `b5c38398`, and the four added on 2026-11-14 are in `b1b08b07`, `cde59541` and `df0b9348`. `test_search.py` has 2.
  - `sim.cpp` takes `--workload`/`--schedule`/`--out-trace` with no positional argument.
  - `rq0-run-record.md` gives the programs and 2026-11-16 to 2026-11-18.
  - The conformance items (a)–(j) were shown the way the 2026-11-14 entry says.
  - Row M of `memo_261021.md` matches.
  - Stage AF matches the 2026-11-19 memo.
- **Form.** Both headers read `Updated 2026-11-21`. No new section. No sentence about the sweep. Ch1 6.6's open-spot box is narrowed per R1, with the outcome stated as ordinary text, dated, and its records named.

## Findings

1. **`docs/guidebook/dataset/07-build-gate-manifests-ci-tests.md:593`** — "…두 pin은 RQ0 run이 읽은 2026-10-31의 판을 가리킵니다. **그날** experiment lint는 이 둘을 note로 출력하고 `lint clean`으로 끝나며…"
   - What is wrong: the nearest date before "그날" is 2026-10-31. On that day the two pins matched the files, and executed specs were not yet read this way (that reading dates from 2026-11-20). So the sentence as written says something false.
   - Record: the experiment lint run of 2026-11-21 (rows file header); `harness/CHANGELOG.md`, the 2026-11-20 entry.
   - Fix: "그날" → "2026-11-21에".

2. **`07-build-gate-manifests-ci-tests.md:711`** (the paragraph's last sentence) — "2026-11-21에 일곱 manifest의 SHA-256을 계산하면 표의 "현재" 열과 모두 같고…"
   - What is wrong: the generated table's "현재" column holds only the five generated manifests. The core and variants manifests (`9f30ea8f`, `3438be7f`) appear only in the pin table's 2026-11-21 row. Before the edit, "및 RQ0 pin" covered those two; the edit dropped it.
   - Record: the committed manifests at `2e3fade3` (R3).
   - Fix: "…다섯 generated manifest는 표의 "현재" 열과, core manifest와 variants manifest는 위 pin 표의 2026-11-21 행과 모두 같고…".

3. **`07-build-gate-manifests-ci-tests.md:1164`** (5.12 table, first row, "그 다음") — "실행된 RQ0 gate spec과 configuration search spec은 다시 pin하지 않음(lint가 note로 읽음; 2026-11-21의 두 번째 bless)".
   - What is wrong: the second bless is given as the instance for both specs. But the configuration search spec was committed after the second bless (`79608bff` follows `2e3fade3`) and pins its manifest. That bless left nothing unpinned in it, so the instance holds for the RQ0 gate spec alone.
   - Record: `harness/CHANGELOG.md`, 2026-11-21 configuration search entry, "Search spec" and "Experiment lint"; `git log`.
   - Fix: "실행된 RQ0 gate spec은 다시 pin하지 않음(2026-11-21의 두 번째 bless), report가 commit된 configuration search spec도 다시 pin하지 않음(lint가 둘의 맞지 않는 pin을 note로 읽음)".

4. **`07-build-gate-manifests-ci-tests.md:600–606`** (3.3, the Merkle figure). No row covers this.
   - What is wrong: the figure says, in the present tense, `build.manifest.json (그 바이트의 SHA-256이 27d347bc…)`, `inputs: archetypes.yaml → 85570c57…` and `meta.sampled = archetypes.yaml@aa2f8842…`. That is the first bless's tree. Since the second bless (item 10), the working tree's manifest is `9f30ea8f`, its library input `34efc7de`, and `meta.sampled` `@a25178d1`.
   - After this chunk's edits the section says the RQ0 gate spec's pins name the 2026-10-31 판, so the figure reads correctly as the tree that pin names. It is still unlabelled, and it sits in a section the chunk edited.
   - Record: the committed manifests at `2e3fade3` and `2e3fade3~1`; `git rev-parse HEAD:dataset/archetypes.yaml`.
   - Fix, for the coordinator to make a row or leave: label the figure's lead-in as the RQ0 gate spec's pin and the tree the RQ0 run read, for example "RQ0 gate spec의 pin(RQ0 run이 읽은 2026-10-31의 판)으로 따라가면".

## Notes, not findings

- Ch1:1086 "9.16 출구 감사, Phase 9 끝" now sits directly above the 9.24 row, and 9.24 is a Phase 9 sub-task (filed there on 2026-11-01). This is outside the fifteen items, and it is a historical label, not false. Ch7 1.7 explains the filing; ch1 does not.
- The ch7 ladder labels the 2026-11-20 lint change "11.3". Its commit `8718bf23` carries only `phase-11`, and the changelog says it was decided "beside" 11.3's decision 10. The paragraph after the ladder says exactly that, so the label reads as intended.
- Ch7 7.6's `test_search.py` cell names two of the four refusals the second test makes (the wrong count and the missing boot default). It leaves out the moved pin and the illegal point. The cell is incomplete, not false.

## Main session, 2026-11-21

The four findings applied by the editor (logs/K1.md, "Review fixes"); the fixed lines read in the diff.
