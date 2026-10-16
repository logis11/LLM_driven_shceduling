# A5 — the fix-ups after stage A (the mock-switch tests, the fixture comments, the c2-pairs recipe comments, the rebuild, the re-pin)

Nothing staged or committed. Every change is in the working tree, on top of stage A's uncommitted edits, none of which was reverted. Files edited: `harness/tools/tests/test_scorer.py`, `harness/tools/tests/test_check_mlfq_levels.py`, `harness/tools/tests/fixtures/README.md`, `dataset/timelines/coreset/c2-pairs.variant.yaml`, `harness/CHANGELOG.md`. `harness/experiments/rq0-gate.yaml` was not edited: no manifest's sha256 changed.

During this step the main session committed A1's registry edit and the work-list findings (`3e6c6351`, `2849cf6d`); HEAD is `2849cf6d`.

## Changes

1. **`test_scorer.py::test_excess_aggregates_on_mock_switch`** (W-0804, the mock-switch fixture re-derived by A4). It now asserts `excess_switch` index 3 = `0.000000000000` (was `100.000000000000`). `excess_boost` 600 and `share_inside_switch_windows` 0.125 are unchanged. The docstring is restated from `worked.md` §8. The switch window [40600, 53100] holds the 50100 wake, value 0. Keystroke 2 reached the editor at 46000 while the editor was ready in Q1 mid-burst, preempted behind the hog, so the wake was queued and the next WAIT completed at 50100 with zero wait. The boost windows are [60600, 80600] (was [60600, 69600]) and [80600, 86600], and they hold the 62000 wake (600). The rest of the MLFQ interval holds the 90000 wake (0). Excess: 0 (switch), 600 (boost).
2. **`test_scorer.py::test_flip_aggregates_on_mock_switch`**. The fixture is kept. After `compute_aggregates`, the test finds the one aggregate row with `metric` `switch_window`, `aggregate` `excess_switch` and `index` `"3"`, asserts that there is exactly one and that its value is the fixture's `0.000000000000`, and replaces its value with a stand-in, `250.000000000000`. The expected `wrong_switch_excess_sum` is the stand-in. The all-correct case still expects `0.000000000000`, and it now runs against the stand-in, so it discriminates. The docstring states the schedule and the grading as before, then that the fixture's own switch excess for entry 3 is 0 µs (worked.md §8) and that the 250 µs stand-in is what makes the contribution visible: 250 µs when entry 3 is wrong, 0 when every query is correct.
3. **`test_check_mlfq_levels.py`**:
   - `:21` now reads "lane-time window [40600, 53100]: the editor's 1→2 demotion at 53100 is its edge (the hog's is at 49100)".
   - `:30` now reads "a simulator whose editor reaches the bottom later than its CPU accounting says" (was "hog").
   - The assertions are unchanged.
4. **`harness/tools/tests/fixtures/README.md:6`**: the `trace.jsonl` line count reads "Hand-written, 17–59 lines" (was "20–50").
5. **`c2-pairs.variant.yaml`, `c2-p2b` and `c2-p2a-idle`** (W-0729). Each recipe comment gains "The game's threads beyond the chain and `wineserver` are omitted: the source puts 95% of scheduling in its top 30-40 tasks and describes none outside them (lavd-ossna24 s12; 9.10 D19).", wrapped over three lines and placed before the Steam-client sentence.
6. **`c2-pairs.variant.yaml`, `c2-p3b`** (W-0747). The clause "segment 1 is as long in both files as the backup needs to end inside it (D123)." is gone. The first sentence now closes after "(meas-ci:background:2026-10-04; 9.10 D17, D119, D120)." and is followed by "Segment 1 runs 60–326 s in both files; the length is 9.10 D123's, set on a shared lane; under the idle class (9.13) the backup does not end inside it and is scored by progress (9.14); the base's export ends by about 99.5 s."
7. **`harness/CHANGELOG.md`, the 2026-10-16 entry, the core-set bullet**. Its list now reads "… the 22 hand-authored timelines other than `c1-idle` and the variant recipes — among the recipes, the game's threads beyond the chain and `wineserver` omitted in `c2-p2b`'s and `c2-p2a-idle`'s as in `c4-gaming`'s and `c7-gaming`'s (W-0729), and `c2-p3b`'s segment 1 restated as `c2-p3a`'s header states it (W-0747), a recipe comment reaching no artifact — and the dataset tools' docstrings." The entry's hashes and Pins bullet are unchanged, and no second entry was added.

## Decisions

1. **The stand-in is 250 µs.** It differs from the fixture's old 100 µs and from every other value the test meets, including the boost excess of 600. A sum equal to 250 can therefore come only from the replaced row.
2. **The replacement is guarded.** It asserts exactly one matching row whose value is `0.000000000000`. If the fixture loses that row, or its value changes, the test fails instead of silently running without the stand-in. The row is selected the way `flip_aggregates` reads it (`harness/tools/harness/aggregates.py:270–272`): `metric == "switch_window"`, `aggregate == "excess_switch"`, `index != ""`, summed per `int(index)`. In the list, the row is replaced by a copy (`dict(row, value=…)`). Every later `flip_aggregates` call in the test reads the replaced list: the all-correct, ungraded and one-entry cases.
3. **The `:30` comment was restated as well as `:21`.** Both state the same stale fact. The second test moves the `x_mlfq_level` line at t 53100, which is now the editor's (`trace.jsonl:29`; the hog's 1→2 is at 49100, `:25`). The A4 reviewer's finding 2 names `:30`.
4. **The README range comes from the six traces' line counts:** `mock-office` 17, `mock-guards` 26, `mock-p1a` 30, `mock-media` 41, `mock-chain` 47, `mock-switch` 59. Each file ends in a newline, so `wc -l` equals `splitlines()`. `mock-office` was already 17 at HEAD, so "20–50" was wrong before A4.
5. **The game-threads wording is the c4-gaming and c7-gaming recipe comments' wording** (`c4.variant.yaml:11–13`, `c7.variant.yaml:166–168`), with typography as there ("95%", "30-40"). It is capitalised and closes with a period, which is how `c2-pairs`' comments that precede `- id:` are written (A2 decision 5). It is placed before the Steam-client sentence, in the order game threads, Steam client, session processes (A2 decision 6).
6. **The `c2-p3b` restatement is `c2-p3a.timeline.yaml:4–6`'s wording,** with two words adjusted for the variant's recipe. "the variant's backup" becomes "the backup", because this recipe is the variant. "the export" becomes "the base's export", because the export is `c2-p3a`'s task `bulk` (`kdenlive_render`, `c2-p3a.timeline.yaml:21`), which this recipe's `patch-task` turns into the backup. The restatement is its own sentence, not a further semicolon clause, so the semicolons inside it read as they do in the header.
7. **No re-pin.** All seven manifests hash after the rebuild to A2's "after" values, so `rq0-gate.yaml` and the entry's hashes stay. The reason is that a recipe file is an input of no manifest:
   - The core manifest's `inputs` are the library, the launch, replay and stimulus streams, the schema, `tools/compile.py` and `tools/wlc/*.py`.
   - The variants manifest's `inputs` are `archetypes.yaml`, `build.manifest.json` and `variants.yaml`.
   - The derived timelines' bytes carry no recipe comment: `derive.py --check` passed, and no derived timeline shows in `git status`.
8. **One mutation is still not caught, and the test was not widened for it.** A `flip_aggregates` that adds every entry's excess, not only a switch into MLFQ's, passes the test. This was already so at HEAD. `compute_aggregates` emits `excess_switch` only for switch windows into MLFQ (`aggregates.py:218`), so the FIFO entry has no row. "The wrong FIFO entry contributes nothing" therefore holds by the data. A stand-in on an index-2 row would feed an input the aggregates never produce.

## Checks

- `python3.12 -m pytest tests/test_scorer.py tests/test_check_mlfq_levels.py -q -m "not coreset_wide"` (in `harness/tools`): 18 passed.
- Mutation check on a scratchpad copy of `harness/tools` (the other `harness/` subdirectories and `dataset/`, `docs/`, `simulator/`, `daemon/` linked to the working tree), running `test_flip_aggregates_on_mock_switch`:

  | aggregates code | with the stand-in | without it (stand-in set to the fixture's 0) |
  |---|---|---|
  | unmutated | passes | — |
  | a wrong switch adds nothing | fails (sum 0 ≠ 250) | passes |
  | every switch into MLFQ adds its excess, wrong or not | fails (all-correct gives 250 ≠ 0) | passes |
  | every entry's excess added (decision 8) | passes | — |

  The stand-in is what makes the test tell the two wrong implementations apart from the correct one.
- `make -C dataset lint PY=python3.12`: "lint clean", exit 0.
- `make -C dataset dataset variants generated PY=python3.12`: exit 0, 4 min 46 s. It wrote 51 core artifacts, 78 variants, and 480 / 720 / 24 / 272 / 66 generated artifacts.
- Manifest sha256 after the rebuild (`shasum -a 256`), each equal to A2's "after" value and to the value before this step:
  - `build.manifest.json` `b6017a10c0ae6644492836a92ee5ab35205397c8c8d6912d2fbcf43870a430c0`
  - `build.variants.manifest.json` `087ef27ca434a21ea346baf3ed454997255bc1e8e2379238169994f27060edcd`
  - `build.transition-grid.manifest.json` `a8eebb3322d4798aed6966b3d751b66e97aa06898a0acc2a88669162c3a6c71b`
  - `build.return-grid.manifest.json` `2e57a6c172e2964adb989b9b0ebe70306e2e32e673281c991321dcc9379582cf`
  - `build.flap-stress.manifest.json` `dd6a7c2444edf22f05fef71d5e4c855aab3edf233d72a7b4e203f903e72ae76b`
  - `build.distractor-grid.manifest.json` `264d33330d016ae776b3e75c6ee6b260944865dffca943e1bea58985345d96d1`
  - `build.familiarity-ladder.manifest.json` `58a34d65a0cd614e80bf6c08d0614496a56ceada2681bdd024fbfc20066b1fa6`
  - `coverage-grid.json` is unchanged (`4c35216e…`).
- `python3.12 tools/derive.py --check --require-coverage` (in `dataset/`; `make check` compares the manifests with HEAD and cannot pass before the commit): "verified — 67 segments on the grid", 0 empty cells, exit 0.
- `make -C dataset test PY=python3.12`: 539 passed, 1 skipped, 2 min 11 s.
- `make -C harness lint PY=python3.12`: exit 0, 3 min 5 s. `lint.py` "lint clean"; `scoring_lint.py` "49 files, 75 terms", "lint clean"; `guards_lint.py` "8 guards, 3 C2 pairs", "lint clean"; `experiment_lint.py` "rq0-gate.yaml: experiment rq0-gate, 3 conditions, 19 judging + 32 reporting files, criterion k_of_n_gap", "lint clean".
- The RQ0 gate spec's five pins (scoring spec, guard spec, driver table, dataset manifest, variants manifest) each equal their file's sha256 on disk (5/5).
- `make -C harness test PY=python3.12` (`pytest tools/tests -q -m "not coreset_wide"`): 296 passed, 2 deselected, 0 failed, exit 0, 17 min 12 s. Stage A's run had 294 passed and 2 failed; those two were the mock-switch tests changed here.

## Left for the main session

- The 2026-10-16 changelog entry does not record the mock-switch re-derivation (W-0804) or the two `test_scorer.py` changes. The 9.14 D1 entry did record `mock-media`'s re-derivation ("The `mock-media` fixture re-derived by hand").
- `harness/tools/tests/fixtures/README.md` item 7 ("with no `run_end` when nobody else is runnable") is narrower than the competitor definition in `worked.md` (the A4 reviewer's finding 2). It is not in this brief and is unchanged.
- `test_mock_switch_window_covers_the_hogs_last_demotion` still asserts "hog" and "53100" separately. The 53100 demotion is now the editor's. The test passes, but it does not check that the editor's demotion is the one reported at the edge.

## Review round 1

Reviewer: a fresh reviewer, 2026-10-16. Read: `git diff HEAD` of the five edited files, this log, A4's log, `worked.md`, `trace.jsonl`, `expected.csv` (HEAD and working tree), `harness/tools/harness/aggregates.py:195–296`, `c4.variant.yaml`, `c7.variant.yaml`, `c2-p3a.timeline.yaml`'s header, the derived `c2-p3b.timeline.yaml`, the manifests' `inputs`.

### Checks

- `python3.12 -m pytest tests/test_scorer.py tests/test_check_mlfq_levels.py -q` (in `harness/tools`): 18 passed.
- `python3.12 -m pytest tests -q -m "not coreset_wide" -k "switch or mock or fixture or lint"`: 85 passed.
- Mutation of `flip_aggregates`, patched in-process (script in the session scratchpad; the tree not touched), running `test_flip_aggregates_on_mock_switch`: unmutated passes; the wrong switch's excess dropped (`excess_sum += 0`) fails at `test_scorer.py:267` (sum 0, stand-in 250 expected); every switch into MLFQ adding its excess whether wrong or not fails at `:277` (all-correct gives 250). The test discriminates.
- `shasum -a 256` of the seven manifests: each equals this log's value. The RQ0 gate spec's five pins (`rq0-gate.yaml:488–493`) equal the sha256 of `scoring-spec.yaml`, `guard-spec.yaml`, `prior.yaml`, `build.manifest.json`, `build.variants.manifest.json` (5/5). The 2026-10-16 changelog entry's eight hashes (driver table, core, variants, the five generated manifests) equal the files' (8/8).
- No manifest's `inputs` names a variant recipe (core: library, streams, schema, `compile.py`, `wlc/*.py`; variants: `archetypes.yaml`, `build.manifest.json`, `variants.yaml`); the derived timelines carry only the GENERATED header, no recipe comment. `derive.py --check --require-coverage`: "verified — 67 segments on the grid", 0 empty cells, exit 0. `make -C dataset lint PY=python3.12`: "lint clean".
- Manifests' mtimes (19:44–19:48) follow the last recipe edit (19:42:23): the rebuild ran on the edited recipe.

### Items

1. (a) Done. `excess_switch` 3 = 0, boost 600, share 0.125, as `worked.md`'s aggregates section derives them; the docstring's 50100 / 46000 / Q1 / boost-window facts match `worked.md` and `trace.jsonl`.
   (b) Done. The row is selected as `flip_aggregates` reads it (`aggregates.py:270–272`), guarded (exactly one row, value 0), replaced by a copy; the wrong-switch sum equals the stand-in, all-correct gives 0. Docstring states the fixture's 0 and the stand-in's role.
2. Done. `:21` and `:30` match `trace.jsonl:25` (hog 1→2 at 49100) and `:29` (editor 1→2 at 53100). README `17–59` matches `wc -l` of the six traces.
3. (a) Done. The sentence is `c4.variant.yaml:11–13` / `c7.variant.yaml:166–168` word for word, capitalised and closed with a period as `c2-pairs`' other pre-`- id:` comments are; `lavd-ossna24` still has its entry (`docs/references.md:661`, `dataset/sources.yaml:47`).
   (b) Done. The restatement is `c2-p3a.timeline.yaml:4–6` with "the variant's backup" → "the backup" and "the export" → "the base's export"; the facts hold (derived `c2-p3b` segment 1 from 60 s to 326 s; `incremental-backup` `declared_class: idle`, `archetypes.yaml:1647`).
4. Done (manifests unchanged, as logged).
5. Done. No re-pin needed; the list clause added in the entry's style; no second entry.

### Findings

1. Not in the brief, same stale fact as `:21`: `harness/tools/tests/fixtures/README.md:18`, the `mock-switch` row, "into MLFQ the lane-time window closing when the hog has its `W_single` of CPU". That is HEAD's `worked.md` wording ("The window closes when the hog has received `W_single`"), from when one hog was counted. After A4 two are counted (`expected.csv` `hogs` 1 → 2 on both `switch_window` rows) and the window closes when the last of them, the editor, reaches 6000 µs at 53100 (`worked.md`: "when the last counted hog has received `W_single`"). Neither A4's nor this log lists it. For the main session.
2. Minor: `test_scorer.py:243` cites "worked.md §8". `worked.md` has no numbered sections; the derivation is its section "The aggregates, by hand (metrics doc §8)". This log's change 1 uses the same cite.
3. Minor: the 2026-10-16 changelog entry's last bullet points to `logs/A2-rebuild.md` and `logs/A3-harness.md` for checks; the rebuild after the recipe edits and the harness lint and test runs are in `logs/A5-fixups.md`.
4. Not this step's: `docs/references.md` differs from HEAD in the working tree (header `Updated 2026-10-16`, the id and tier rules, entries), mtime 20:11:11, after this log (20:08:36); no stage A log claims it (A1: "`docs/references.md` untouched"). It is presumably the references chunk running concurrently; it is not part of this review.
5. Carry-forward, not this step's: A4's reviewer listed stale mock-switch text no work-list row covers — `docs/harness/harness-and-records-guide.md:618` (H = 1; now 2), `:620` (the hog's CPU interval), `:624` (`hogs=1`), `:616`/`:624` (`index=2`; the 40600 entry is index 3), `docs/harness/metrics.md:320` ("one hog"). W-0830 covers only `:629`. This log's own leftovers (the changelog's missing W-0804 line, README item 7, the `"hog"` assertion in `test_mock_switch_window_covers_the_hogs_last_demotion`) are confirmed.

Verdict: pass. Every briefed item is done and checked; findings 1–3 are wording, finding 1 for the main session to fold in or row.
