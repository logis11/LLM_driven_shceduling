# K9 review — the docs index, the memos' status lines, the hold-time plan file

Reviewed 2026-11-21 against `git diff` of the six files, rows g0-01 – g0-14, the K9 log, the work list (Q5) and the records each row names.

**FINDINGS — 2**, both on index lines K9 did not touch and no row covers. Every applied row is correct.

## What checks out

- **Coverage and scope.** g0-01 (`docs/README.md:40`), g0-02 (:124), g0-03 (:115), g0-04 (:113), g0-05 (:94), g0-06 (:97–99), g0-07, g0-08, g0-13, g0-14 are applied. g0-09 is g0-04. g0-10, g0-11, g0-12 are left (the 2026-10-17 memo's line and `_dev/TODO.md` untouched). Every hunk maps to one of these rows.
- **Memos, status only (spec decision 4).** In each of the four memos only the header's `Updated` (to 2026-11-21) and the line under it changed. No body text changed.
- **The three new status lines (Q5).** Each names only what its own "## 1. 경민이 할 일" asks. 2026-11-13: §1 item 2, reading AD and AE; item 1, the rebuild, handed to the 2026-11-19 memo at `simulator@841dc81131cb`; item 3, the batch memo's §7 item 5, kept open by that memo. 2026-11-15: item 2, reading the new tests (its §2 table lists `mutants.py` among them); item 1 handed on; item 3 a standing rule. 2026-11-19: items 1 and 2 open; item 3, the batch memo's §7 item 5. Each is in Korean 해요체, opens "열림 —" and closes "담당 인경민." in the form the 2026-10-17 memo uses. `git log --since=2026-11-12 -- simulator` shows no commit by 인경민, so no ask was answered.
- **The 2026-09-08 memo's line.** In `simulator/memo/memo_261010.md` Part D, D2 is the switch-demand test, D3 the semantics notes and D4 `x_mlfq_level`, and `memo_261111.md:83` confirms the test is D2. The new "D3–D4" (owed) and "D2" (done) are right. `2ee49785` (2026-11-11, km1q1q8i) adds `simulator/tests/test_switch_demand.py`. The gate's `unit.json` lists it among the seven tests run on the binary.
- **Index lines against the memos and the record.** :94 agrees with the 2026-09-08 line. :97–99 agree with the three new lines. :115 agrees with the 2026-11-18 memo's "정정 (2026-11-18)" (4 of 19, 12 of 19) and "정정 (2026-11-21)" (fail, 5 of 19, K = 10), and its "Closed" with the memo's 닫힘. :40 and :124 agree with `docs/rq0-run-record.md`: corrections 2026-11-18, 2026-11-20 and 2026-11-21 (line 192); the failure procedure (line 204); two reports and two hash manifests (lines 104–105, 121, 243). :113 agrees with `harness/CHANGELOG.md` 2026-11-01 (the `cap-band` statement and line) and the record's cap band row (line 88).
- **The hold-time plan file.** Row 0's "when" is Phase 11 spec decision 10 word for word, and the needs column is unchanged. "Both later blocks" are 인지오's Backlog lines for step 1 and for steps 2, 4, 5, 6 (`_dev/TODO.md`, the two hold-time lines).
- **The docs the sweep changed.** For every doc under `docs/` in `git diff --stat ba0a6874..HEAD` and in the uncommitted diff, the index line and the full-index row still describe the doc, apart from F2. No status changed. The header already read `Updated 2026-11-21`.

## Findings

### F1 · `docs/README.md:116` — the configuration search memo's line reads the route's invariance as the count's

- **Now:** "the route, the driver table rewritten, 8 of 10 files at finding 3 at every g of the band and under every boot default"
- **Wrong:** Read naturally, this says 8 of 10 files are at finding 3 under every boot default. That holds for every g of the band but not for every boot default. Under the boot defaults, a finding changes on three files:
  - `c7-transcode` moves to finding 3 under 30 ms;
  - `c1-render` moves to finding 2 under 100 ms;
  - `c7-photo` moves to finding 2 under 0.5, 0.7, 1.2, 2, 5, 7 and 20 ms;
  - under 100 ms, three files have no reading.

  What stays the same everywhere is the route.
- **Record:** `docs/rq0-run-record.md:204`, "8 of the 10 files are at finding 3 … The route is the same at every g of the band … and under each of the ten alternative boot defaults"; :238, the boot-default bullet. The memo says the same at its line 21: "10개 중 8개가 finding 3이에요. … 열 개의 다른 boot default 모두에서 route가 같아요."
- **Fix:** "the route, the driver table rewritten — 8 of 10 files at finding 3 — the same at every g of the band and under every boot default". This needs a new row: an A row on item 13, the configuration search and its route.

### F2 · `docs/README.md:22` — the dataset guidebook's list of its checking passes lacks three of five

- **Now:** "every count checked against the tree when written (2026-10-14), and in the docs-correction task (9.15) each volume's corrections checked against the 2026-10-17 tree"
- **Wrong:** K4 made the guidebook README's own list whole under Q1 (g4-27). It now also names:
  - the pass after 9.16 and Phase 9's end, against 9.16's record and the 2026-10-20 tree;
  - the 2026-10-31 pass, on that day's rebuilt dataset;
  - this sweep's 2026-11-21 pass, against the records of Phases 10 and 11 and that day's tree.

  The index's description of the same volumes stops at the second pass. Q1's rule ("a list that presents itself as current or whole gains … every older member it lacks …, this sweep's own pass among them in the guidebook's lists of its correction passes") reaches this sentence too.
- **Record:** `docs/guidebook/dataset/README.md:7`.
- **Fix:** Append the three passes as the README states them: "; after 9.16 and Phase 9's end (2026-10-18), the passages still calling them in progress against 9.16's record and the 2026-10-20 tree; on 2026-10-31, each volume to that day's rebuilt dataset; on 2026-11-21, the passages Phases 10 and 11 overtook, against their records and the 2026-11-21 tree". This needs a new row: a B row under Q1.

## Notes, not findings

- `docs/README.md:31` describes the decision chronicle as "the decisions from the 2026-08-23 design meeting to 9.23 … what is open". Its decision chapters still end at 9.23, and spec decision 14 writes no section for the re-measurement, so the line is not false. Since K2, though, 12.4 holds Phase 10's items with their outcomes, and the one-page timeline runs to 2026-11-21.
- The 2026-11-15 memo's §1 item 1 also runs `make -C simulator/src mutants`. The 2026-11-19 memo's §1 item 1, which the new line says takes over the rebuild, runs build, version and check only. Q5 decided to point the rebuild there. Whether the mutant run should be named is for 인지오.

## Main session, 2026-11-21

F1 and F2 applied as new rows g0-18 and g0-19. The 2026-11-15 memo's mutant run: its status line names the reading of the new tests and mutants as the open ask (§1 item 2); the rebuild handed to the 2026-11-19 memo is the build, version and check that memo names, as Q5 decided.
