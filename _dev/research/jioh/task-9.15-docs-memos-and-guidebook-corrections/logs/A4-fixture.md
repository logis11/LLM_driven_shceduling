# A4 — the mock-switch fixture (W-0804)

Files changed: `harness/tools/tests/fixtures/mock-switch/worked.md`, `trace.jsonl`, `expected.csv`. `run.json` and `config-schedule.json` untouched. Nothing staged or committed.

## Outcome

**W-0804 (인경민's mock-switch question 1, `simulator/notes/note1010.md:103–114`): applied.** At 44600 `editor`'s Q0 slice ends with 1000 µs of its burst left; it is demoted to Q1 and preempted, and `probe` (Q0 since 40000) runs 44600–45100. Re-derived from 44600 to the end:

| t | new trace |
|---|---|
| 44600 | `x_mlfq_level` editor 0→1; `run_end` editor `preempt`; `run_start` probe |
| 45100 | `run_end` probe `block`; `run_start` hog (head of Q1, there since 42600; editor behind it since 44600) |
| 46000 | keystroke 2 reaches editor mid-burst (ready in Q1): queued, no trace line |
| 49100 | `x_mlfq_level` hog 1→2; `run_end` hog `preempt`; `run_start` editor |
| 50100 | `ready` editor `wake` (the queued keystroke, inside the occupancy) |
| 53100 | `x_mlfq_level` editor 1→2; `run_end` editor `block`; `run_start` hog |
| 60600 | boost: `x_mlfq_level` editor 2→0, hog 2→0 |
| 62000 | `ready` editor `wake` |
| 62600 | `x_mlfq_level` hog 0→1; `run_end` hog `preempt`; `run_start` editor |
| 64600 | `x_mlfq_level` editor 0→1; `run_end` editor `preempt`; `run_start` hog |
| 68600 | `x_mlfq_level` hog 1→2; `run_end` hog `preempt`; `run_start` editor |
| 69600 | `run_end` editor `block`; `run_start` hog |
| 80600 | boost: `x_mlfq_level` editor 1→0, hog 2→0; then hog 0→1 at 82600, 1→2 at 86600 |
| 90000 | `ready` editor `wake`; `run_end` hog `preempt`; `run_start` editor |
| 92000 | `x_mlfq_level` editor 0→1 (keeps the lane over hog in Q2) |
| 93000 | `run_end` editor `block`; `run_start` hog |
| 100000, 322500 | unchanged (`task_end` editor and probe `depart`; hog `exit` at 322500) |

`trace.jsonl`: 47 → 59 lines; lines 1–19 (to `run_start` editor at 42600) unchanged. SHA-256 `091d2374…` → `58f6eaaa020a743dc5ad35532d27fb8910e341cff3c71abcad67a183419b55cf`.

`expected.csv` (28 rows, as before) — values changed:

| row | old | new |
|---|---|---|
| every row's `source_sha256` | `091d2374…` | `58f6eaaa…` |
| editor `preempt_count` | 0 | 2 (44600, 64600) |
| editor `ready_wait` keystroke 2 | t 46000, 100 | t 50100, 0 (queued wake, inside occupancy [49100, 53100]) |
| hog `preempt_count` | 3 | 5 (42600, 49100, 62600, 68600, 90000) |
| probe `ready_wait` 40000 | 5600 | 4600 |
| `switch_window` 12000 (FIFO) `hogs` | 1 | 2 (editor's first `run_end` after 12000 is now the 44600 preempt) |
| `switch_window` 40600 (MLFQ) `hogs` | 1 | 2; value 12500 unchanged (hog has its 6000 µs at 49100, editor at 53100) |
| `boost_window` 60600 | 9000, `hogs` 1 | 20000, `hogs` 2 (editor counted by its 64600 preempt, has 3000 µs by 80600; clipped at the next boost) |

Unchanged: `cpu_delivered` (editor 12000, hog 77500, probe 500), `busy` 90000, hog's exit at 322500, every `config_interval` row, `boost_window` 80600 (6000, 1 hog).

`worked.md`: assumption paragraph, the "What happens" rows from 40600, the `ready_wait`, lifetime, `switch_window` and `boost_window` tables and their text, the §8 aggregates and the check-tool section rewritten to the new trace. §8 aggregates by hand: switch excess 0 µs (was 100), boost excess 600 µs, share inside switch windows 0.125.

## Decisions

1. **Within-queue order is round-robin, so the 64600 case changes too.** At 45100 Q1 holds hog (entered at 42600) ahead of editor (entered at 44600), so hog runs; at 64600 editor is demoted into Q1 behind hog (there since 62600) and hog runs. Reason: MLFQ rule 2, `docs/simulator/simulator-guide.md:201` ("Always run from the highest non-empty queue; round-robin within a queue"), the line W-0765's answer cites; the fixture's own "a wake into the same … queue waits for the slice boundary"; the simulator's `on_yield` pushes a slice-ended task to the back of its new queue (`simulator/src/sim.cpp:227–231`). note1010.md:112 had flagged the 64600 continuation as possibly the open within-queue choice; under the round-robin reading it is not open. Stated in the assumption paragraph.
2. **"Slice expiry with no competitor demotes without a `run_end`" kept verbatim** (인지오's W-0736 answer (a)), with "a competitor" defined in a parenthesis as a ready task in the holder's new queue or a higher one. That covers 92000 (editor demoted to Q1, hog in Q2: editor keeps the lane, no pair) and 77600 (hog's Q2 slice, nobody else ready), both as the old derivation had them.
3. **A burst ending at the instant its slice ends is demoted as it blocks** (editor at 53100: RUN 3000 from 50100 and the Q1 slice from 49100 both end at 53100). Reason: guide §5 rule 4 keeps the level only for a task that blocks "before its slice ends"; rule 3 demotes "a task that burns its whole slice". Records are the same either way (the 60600 boost resets editor's level before its next wake); only the `x_mlfq_level` line at 53100 depends on it. Added to the assumption paragraph. The simulator differs here: on a tie its RUN completion wins (`sim.cpp:813`), the task blocks with its allotment spent and keeps its level, and the demotion falls at its next pick (`sim.cpp:244`).
4. **`x_mlfq_level` lines now written for `editor` as well as `hog`.** Reason: editor is now a counted hog of the 40600 switch; `check_mlfq_levels.py` reports a counted hog with no demotion line as "not covered" and exits 1 (`harness/tools/check_mlfq_levels.py:95–98`). The fixtures README item 7 lets a mock write the lines "where the mock's author knows the level changed". Lines run up to `T_end`, as the old trace's did (none for hog's boosts at 100600 and after); the cold start at 40600 writes none (hog's 1→0 there was not written in the old trace either). `probe` never changes level. The assumption sentence states all three.
5. **Same-instant `x_mlfq_level` lines at a boost in run-file order** (editor, then hog). At a slice end: the `x_mlfq_level` line, then `run_end`, then `run_start`, as the old trace did at 42600 and 62600.
6. **The keystroke at 46000 is a queued wake.** editor is ready but mid-burst, so its next WAIT completes at once at 50100 with a `ready(wake)` inside the occupancy, paired with 0 (fixtures README items 1–2; `mock-office` writes queued keystrokes the same way). Its row moves from t 46000 to t 50100.
7. The FIFO row's "MLFQ took over 30 ms later" became "at 40600" (40600 − 12000 = 28600). The wall-clock comparison under the window is restated for the two hogs: [40600, 46600], hog 2500 µs past, editor 6500 µs past.

## Checks

- Independent replay: a 74-line event loop (scratchpad `mlfq_check.py`) from the 40600 cold-start state under the assumption paragraph's rules; its `run_start`/`run_end`/`ready`/`x_mlfq_level` lines in [42600, 100000) diffed against `trace.jsonl`: identical.
- `python3.12 harness/tools/records.py --run … --trace … --schedule …/config-schedule.json --table calibrated --telemetry names --out <scratch>`: 28 rows, `cmp` against the hand-edited `expected.csv`: byte-identical. `records.build` raised no guard.
- `compute_aggregates(rows, interactive=("editor",))`: `excess_switch` 0.000000000000, `excess_boost` 600.000000000000, `share_inside_switch_windows` 0.125000000000 — matches `worked.md` §8.
- `python3.12 harness/tools/check_mlfq_levels.py` on the fixture: "switch index 3 at 40600 (MLFQ, 2 hog(s), window 12500 -> until 53100)", editor last demotion 53100 covered, hog 49100 covered, "all covered", exit 0.
- `python3.12 -m pytest harness/tools/tests/test_check_mlfq_levels.py -q`: 4 passed.
- `python3.12 -m pytest harness/tools/tests/test_check_mlfq_levels.py harness/tools/tests/test_mock_simulator.py harness/tools/tests/test_reader.py harness/tools/tests/test_records.py harness/tools/tests/test_scorer.py -q -m "not coreset_wide"` (every test file that names `mock-switch`; `test_reader.py` and `test_records.py` are the ones conftest.py's `MOCKS` feeds): **77 passed, 2 failed, 1 deselected.** `test_check_mlfq_levels.py` 4/4, `test_mock_simulator.py` (the byte-for-byte replay among them), `test_reader.py`, `test_records.py` all pass. Failed: `test_scorer.py::test_excess_aggregates_on_mock_switch` (asserts `excess_switch` "100.000000000000"; now "0.000000000000") and `test_scorer.py::test_flip_aggregates_on_mock_switch` (asserts `wrong_switch_excess_sum` "100.000000000000"; now "0.000000000000"). Both hard-code the old derivation's switch excess; `test_scorer.py` is outside this step's files and was not edited. The deselected test (`coreset_wide`, `test_every_coreset_file_flows_through_records_with_no_message`) reads the compiled coreset, not the fixture.
- A first run of the same five files without `-m "not coreset_wide"` was stopped after 5 minutes in the coreset-wide test; no result taken from it. `make -C harness test PY=python3.12` was also started and stopped at 72 % (no failure up to there); not a result.

## Left for the main session (outside this step's files)

- `harness/tools/tests/test_scorer.py:137–149` and `:237–262`: the two failing tests and their docstrings ("the switch window [40600, 53100] holds the 46000 wake (100), the boost windows [60600, 69600] …", "the switch whose excess the worked derivation gives as 100 µs"). With the switch excess now 0, the flip test's `wrong_switch_excess_sum` no longer tells a contributing wrong switch from a non-contributing one.
- `harness/tools/tests/test_check_mlfq_levels.py:21` comment "the hog's 1→2 demotion at 53100 is its edge": the line at 53100 is now editor's; the tests pass unchanged.
- `docs/guidebook/dataset/05-the-generated-layer.md:1807` quotes the flip check as "3 changes, 2 wrong, excess 100 µs"; now 0 µs.
- `docs/harness/harness-and-records-guide.md:629`: "hog는 53100에야 맨 밑에 닿아서" — hog now reaches the bottom at 49100, editor at 53100; the window still closes at 53100.
- `harness/tools/tests/fixtures/README.md`: `trace.jsonl` described as "Hand-written, 20–50 lines"; mock-switch's is now 59.

## Review round 1

Reviewer: a fresh reviewer, 2026-10-16. Derivation written before the editor's new `worked.md`, `trace.jsonl` and `expected.csv` were read (only the HEAD versions, `run.json`, `config-schedule.json`, the fixtures README, `docs/simulator/simulator-guide.md` §5 and `docs/harness/metrics.md` §6, §8, §11 were read first).

### Independent derivation, 44600 to the end

Rules used: entry 3 (MLFQ, 3 queues, slices Q0 2000 / Q1 4000 / Q2 8000, boost every 20000 from `t_apply` 40600, so boosts at 60600 and 80600); a full slice demotes, a block before the slice ends keeps the level; a fresh slice at every dispatch and boost; always run the highest non-empty queue, round-robin (entry order) within a queue (guide §5 rule 2, `simulator-guide.md:201`, the line W-0765's answer cites); a wake into a strictly higher queue preempts at once, into the same or a lower queue waits for the slice boundary; slice expiry with no ready task in the holder's new queue or a higher one demotes without a `run_end` (인지오's answer to W-0736); a keystroke sent while the editor is not blocked is queued and completes its next WAIT with a zero-wait `ready` line inside the occupancy (fixtures README items 1–2, as `mock-office` does at 18000 and 21000).

State at 44600 (unchanged prefix): `editor` running in Q0 since 42600 (RUN 3000, 2000 done); `hog` in Q1 since 42600 (preempted, 34600 of CPU); `probe` ready in Q0 since 40000.

| t | event |
|---|---|
| 44600 | `editor`'s Q0 slice ends → Q1 (0→1). `probe` is ready in Q0 → `editor` preempted (`run_end preempt`), 1000 of its RUN left. Q1 = [`hog`, `editor`]. `probe` runs (waited 4600). |
| 45100 | `probe` RUN 500 ends, WAIT blocks forever (Q0 kept). Q1 round-robin → `hog` first (entered 42600), fresh 4000 slice. |
| 46000 | keystroke 2: `editor` is ready, not blocked → queued; no line. |
| 49100 | `hog`'s Q1 slice ends → Q2 (1→2); `editor` ready in Q1 → `hog` preempted. `editor` runs, fresh 4000 slice. |
| 50100 | `editor`'s RUN ends; WAIT completes on queued keystroke 2 → `ready(wake)` 50100 inside the occupancy (wait 0); RUN 3000 starts. |
| 53100 | RUN ends at the slice end (4000 since 49100); WAIT blocks (`run_end block`). Tie: demoted as it blocks (1→2) — rule 3 "burns its whole slice"; rule 4 keeps the level only "before its slice ends". Records unaffected either way. `hog` runs in Q2, fresh 8000 slice. |
| 60600 | boost: `hog` 2→0 (fresh 2000 slice), `editor` 2→0 (blocked); `probe` stays 0. |
| 62000 | keystroke 3: `editor` ready in Q0, same queue as `hog` → waits. |
| 62600 | `hog` → Q1 (0→1); `editor` in Q0 outranks → `hog` preempted. `editor` runs (waited 600). |
| 64600 | `editor`'s Q0 slice ends → Q1 (0→1); `hog` ready in Q1 ahead of it → `editor` preempted, 1000 left. `hog` runs, fresh 4000. |
| 68600 | `hog` → Q2 (1→2); `editor` ready in Q1 → `hog` preempted. `editor` runs, finishes RUN at 69600, WAIT blocks (nothing queued), stays Q1. |
| 69600 | `hog` runs in Q2; 77600 bottom-slice expiry, no competitor, no line. |
| 80600 | boost: `hog` 2→0, `editor` 1→0. |
| 82600 | `hog` 0→1, no competitor, no `run_end`. |
| 86600 | `hog` 1→2, no competitor. |
| 90000 | keystroke 4: `editor` wakes into Q0 over `hog` in Q2 → `hog` preempted at once; `editor` runs (waited 0). |
| 92000 | `editor`'s Q0 slice ends → Q1 (0→1); `hog` is in Q2, no competitor → no `run_end`. |
| 93000 | `editor` RUN ends, last WAIT blocks. `hog` runs. |
| 100000 | `T_end`; `editor`, `probe` depart. |
| 322500 | `hog` exits (10000 + 300000 + 12500 of others' occupancy). |

Occupancies: `editor` [0,0] [42600,44600] [49100,53100] [62600,64600] [68600,69600] [90000,93000] = 12000, 2 preempts (44600, 64600). `hog` [10000,42600] [45100,49100] [53100,62600] [64600,68600] [69600,90000] [93000,100000 clip] = 32600 + 4000 + 9500 + 4000 + 20400 + 7000 = 77500, 5 preempts (42600, 49100, 62600, 68600, 90000). `probe` [44600,45100] = 500, 0 preempts. `busy` 90000.

`ready_wait`: `editor` 0 arrive 0; `hog` 10000 arrive 0; `editor` 20000 wake 22600; `probe` 40000 arrive 4600; `editor` 50100 wake 0; `editor` 62000 wake 600; `editor` 90000 wake 0.

`switch_window`: index 2 (12000): alive `editor`, `hog`; first `run_end` after: `editor` 44600 preempt, `hog` 42600 preempt → hogs 2, value 0. Index 3 (40600): alive all three; `editor` 44600 preempt, `hog` 42600 preempt, `probe` 45100 block → hogs 2; `W_single` 6000; `hog` reaches it at 49100 (2000 + 4000), `editor` at 53100 (2000 + 4000) → `t_close` 53100, value 12500.

`boost_window`: 60600 — `editor` 64600 preempt, `hog` 62600 preempt, `probe` none → hogs 2; `hog` 6000 at 68600, `editor` only 3000 by 80600 → clipped at the next boost, value 20000. 80600 — `editor` 93000 block, `hog` 90000 preempt → hogs 1; `hog` 6000 at 86600 → value 6000.

`config_interval` unchanged (600, 11400, 28600, 59400). 28 rows.

Aggregates (`editor`, wake/input): inside the switch window [40600, 53100] the 50100 row (0); inside boost windows [60600, 80600] and [80600, 86600] the 62000 row (600); rest of the interval the 90000 row (0). Switch excess 0 − 0 = 0; boost excess 600 − 0 = 600; share 12500 / 100000 = 0.125.

`x_mlfq_level` lines from 42600 (if written for every task whose level changes): hog 0→1 42600; editor 0→1 44600; hog 1→2 49100; editor 1→2 53100; hog 2→0 and editor 2→0 60600; hog 0→1 62600; editor 0→1 64600; hog 1→2 68600; hog 2→0 and editor 1→0 80600; hog 0→1 82600; hog 1→2 86600; editor 0→1 92000. Expected trace length 59 lines.

### Comparison with the editor's files

- `trace.jsonl` (59 lines, SHA-256 `58f6eaaa020a743dc5ad35532d27fb8910e341cff3c71abcad67a183419b55cf`, recomputed): every line from 42600 on matches the derivation above. Lines 1–19 are byte-identical to HEAD (`git diff`). The only differences are the order of lines at the same instant, which is a free choice: at 53100 the editor's `x_mlfq_level` comes before its `run_end block` (this follows the 42600 and 62600 pattern), and at 60600 and 80600 the editor's boost line comes before the hog's (run-file order). Neither changes a record.
- `expected.csv`: all 28 rows match the derivation value for value. These rows changed: editor `preempt_count` 2; editor `ready_wait` 50100/0; hog `preempt_count` 5; probe `ready_wait` 4600; `boost_window` 60600 20000, hogs 2; `switch_window` hogs 2 on both rows. Every row carries the new `source_sha256`. The file ends in a newline, as HEAD does.
- `worked.md`: the assumption paragraph, the "What happens" table, the `ready_wait`, lifetime, `switch_window` and `boost_window` tables, the §8 aggregates and the check-tool section all agree with the derivation. Wall-clock overruns (hog 49100 − 46600 = 2500, editor 53100 − 46600 = 6500) checked. The assumption "slice expiry with no competitor demotes without a `run_end`" (the W-0736 answer) is kept verbatim.

### Checks rerun (python3.12)

- `records.py --run --trace --schedule --table calibrated --telemetry names`: 28 rows, `cmp` byte-identical to `expected.csv`.
- `compute_aggregates(..., interactive=("editor",))`: `excess_switch` 0, `excess_boost` 600, `share_inside_switch_windows` 0.125, the same as the derivation.
- `check_mlfq_levels.py`: index 3, 2 hogs, window until 53100; editor last demotion 53100 and hog 49100 both covered; "all covered", exit 0.
- `pytest test_check_mlfq_levels.py test_mock_simulator.py test_reader.py test_records.py -m 'not coreset_wide'`: 65 passed, 1 deselected.
- `pytest test_scorer.py`: 2 failed, 12 passed. `test_excess_aggregates_on_mock_switch` and `test_flip_aggregates_on_mock_switch` still expect 100 and now get 0. These tests read the fixture directly, not through `MOCKS`. `test_scorer.py` is outside this step's files.
- `git status`: under `harness/`, only the three fixture files changed. The `dataset/` changes belong to other steps.

### Findings

1. Blocking for the commit, outside this step's files: `harness/tools/tests/test_scorer.py:137–149` and `:237–262` fail on the corrected fixture. The docstrings there are stale too: "boost windows [60600, 69600]" is now [60600, 80600], and the switch excess of 100 is now 0. 인지오 needs to choose between (a) changing the expectations to 0 and (b) rebuilding the flip test so that the switch excess is non-zero. The editor gave the same two options.
2. Stale text the editor's hand-off list missed (outside this step's files):
   - `docs/harness/harness-and-records-guide.md:618`: "editor 45600 block / … / probe 46100 block → H = 1". The editor's first `run_end` is now the 44600 preempt, the probe's is the 45100 block, and H = 2.
   - The same doc at `:620` gives the hog's CPU as "[49100,53100] 4000". It is now [45100, 49100], and the editor's 6000 is reached at 53100.
   - The same doc at `:624` gives `hogs=1`; it is now 2. The `index=2` there and at `:616` was already wrong before this step: the 40600 entry is index 3.
   - `docs/harness/metrics.md:320` (§12) describes `mock-switch` as having "one hog".
   - The comment at `harness/tools/test_check_mlfq_levels.py:30` reads "a simulator whose hog reaches the bottom later". The line it moves (t 53100) is now the editor's. The editor flagged `:21` but not `:30`.
   - `harness/tools/tests/fixtures/README.md` item 7 demotes with no `run_end` "when nobody else is runnable". That is narrower than the competitor definition `worked.md` now states. At 92000 the hog is runnable in Q2 and the editor keeps the lane with no `run_end`. The trace was the same here before this step, so the narrower wording was already there; this step has only made the difference visible.
3. The step's own files have no defects. The derivation matches, the records are reproduced by the code, and the brief's tests pass.

Verdict: pass for this step's files. Finding 1 must be resolved before the fixture is committed.
