# A3 — the harness: the RQ0 gate spec, the driver table, the harness changelog (W-0758, W-0777, W-0801, the re-pins of A2's rebuild)

Nothing staged or committed. Every change is in the working tree. Files edited: `harness/experiments/rq0-gate.yaml`, `daemon/driver-table/prior.yaml`, `harness/CHANGELOG.md`.

## Outcomes

- **W-0758 (the RQ0 gate spec's conformance statement): applied, with (g).** `simulator-conformance`'s last sentences now read: "…(f) the frame chain's woken stages in EDF's deadline class with the frame's deadline (recognition-vocabulary §2, 2026-10-06); (g) an orchestrator's WAIT children:<id> completes when the last child it spawned ends, and without blocking when none is live at the WAIT (9.15 W-0743). (c) and (f) the simulator does today; the others its owner holds as owed. The run does not start until each is shown." Checked against `simulator/src/sim.cpp` (last changed `6bf9d850`, 2026-10-10, "sim_t + sim_u"; no working-tree change under `simulator/`):
  - (c): U1 (`:47`, `:208`, a switch into MLFQ resets every task to Q0) and U2 (`:48–51`, `:209`, `:596`, `:607`, a same-algorithm entry leaves the holder and queue order alone) are in the code; `git log -S"U1 a switch into MLFQ"` names `6bf9d850`.
  - (f): the B2 periodic class takes every task reachable through WAKE targets from a TIMER task (`:35–37`); `deadline()` returns a task's own TIMER job deadline, else its inherited `chain_dl` (`:405–408`); `deliver()` passes the waker's deadline to the woken stage (`:786–795`); EDF's `preempts` orders by `deadline()` (`:320–323`).
  - (g): not in the code. `on_task_end` (`:758–768`) decrements the parent's `live_children` and unblocks the parent only when it is blocked on a fork slot (`wait_chan < 0`); `children:` is an ordinary channel. (g) is covered by "the others its owner holds as owed".
- **W-0777 (the driver table's closing clause): applied.** `prior.yaml:298`, the wanted compile row's LOTTERY justification: "How LOTTERY splits tickets inside the batch class while the editor's own burst tail is batch class is the simulator's rule (batch-class memo §7 item 3), asked of 인경민 in the heads-up memo and not yet answered." → "Inside a class every task holds equal tickets, the editor's own burst tail included while it is batch class — the reference simulator's rule (simulator/src/sim.cpp:328–366: the class drawn by batch_share when both are runnable, uniform within it, only runnable tasks holding tickets; recognition-vocabulary §2, waldspurger-osdi94)." Checked: `sim.cpp:328–333` (the LOTTERY comment: tickets split by share, equal tickets per task within a class, a two-stage draw, only runnable tasks holding tickets) and `:362–366` (`pick()`: the class drawn by `share_bp` only when both classes are non-empty, else the non-empty one); `docs/recognition-vocabulary.md:98`, under §2, "equal tickets per task within a class". `sources` stays `[waldspurger-osdi94]`. The file parses; no value changed. SHA-256 `6e271dd042b38c23b85459cec7545fde990aec9be5a2c8bd6081690d98243f7f` → `0fba4b3c9822054fad19ef150d1395d91e679d42b6299166b9a89f50ad27960c`.
- **The re-pins: applied.** `rq0-gate.yaml` `pins`: `driver_table` `0fba4b3c9822054fad19ef150d1395d91e679d42b6299166b9a89f50ad27960c`; `dataset` `b6017a10c0ae6644492836a92ee5ab35205397c8c8d6912d2fbcf43870a430c0`; `variants.all` `087ef27ca434a21ea346baf3ed454997255bc1e8e2379238169994f27060edcd` (both measured with `sha256sum` on the working tree; equal to `A2-rebuild.md`'s table). `scoring_spec` and `guard_spec` unchanged (their files hash to the pinned values). The comment above `pins` names the new changelog entry first: "(harness/CHANGELOG.md, 2026-10-16, the 9.15 entry; 2026-10-15 and 2026-10-14, the 9.23 entries; …)".
- **`harness/CHANGELOG.md`: one new entry,** "2026-10-16 — the conformance statement's (c) and (g); the driver table's ticket rule; the dataset re-pinned on the compiler and lint cleanup (jioh 9.15)", above the 2026-10-15 entry. Bullets: the RQ0 gate spec (W-0758, the (c)/(f) sentence and (g)); the driver table (W-0777, its clause and re-pin); the core set and the variants (what A2's rebuild moved); the pins (core, variants, the five generated manifests); the correction (W-0801); the decisions and checks pointers. The 2026-10-09 entry is not edited.
- **W-0801: applied** as the entry's correction bullet: "the 2026-10-09 entry's "`input` on 25" is 24, the other 15 on `timer` (the scoring spec frozen that day, `5d8a3243…`: 75 terms, 24 on `channel: input`, 15 on `channel: timer`)".

## Decisions

1. **The (g) citation is "(9.15 W-0743)".** The other items cite their contract source; the contract text W-0743's answer names (the interpretation contract's FORK and WAIT text, `docs/data-contracts.md` and its §14 entry) is another step's and was not yet in the working tree when this step ran (`git status docs/simulator docs/data-contracts.md` clean; `interpretation-contract.md` has no `children:` completion rule). "9.15 W-0743" is the form A2's code comments use ("9.15 (W-0746)") and the decision-number form the statement already uses ("9.11 D3, D17"). Once the contract text lands, the citation could name it instead; that is the main session's call.
2. **"The run does not start until each is shown" kept verbatim**, read from the step's "the run does not start until each is shown still holds"; (g) is folded into the item list before the closing sentences, so "the others" covers (a), (b), (d), (e) and (g).
3. **The driver-table clause keeps the editor's burst tail as its subject** ("the editor's own burst tail included while it is batch class"), since the clause it replaces asked about exactly that case; the rule is otherwise the answer's wording. "vocabulary §2" is written "recognition-vocabulary §2", the name `prior.yaml` uses elsewhere (`:12`, `:35`).
4. **The changelog entry lists the five generated manifests' new hashes** in its Pins bullet, as the 2026-10-15 and 2026-10-14 entries do, though nothing pins them yet.
5. **"No artifact's behaviour changed" was verified by a build, not taken from A2's log.** HEAD's `dataset/` tree (`git archive HEAD dataset`) was extracted to the scratchpad and built there (`make dataset variants generated PY=python3.12`); its seven manifests hash to HEAD's committed ones. Each working-tree artifact was compared with HEAD's, `meta` removed (results under Checks). The generated artifacts differ in `meta.sampled.archetypes` alone (not in `derived_from`), so the Pins bullet says "the library's hash alone, their `inputs` pinning the edited C1 timelines and tools"; a first draft that said "the library's and the C1 timelines' hashes" was corrected.
6. **The W-0801 counts were re-derived** from the scoring spec at `9c80113e` (the file hashing to `5d8a3243…`, the 2026-10-09 freeze) by parsing it: 49 files, 75 terms, `channel: input` 24, `channel: timer` 15. The working-tree spec parses to the same (a plain `grep -c 'channel: input'` gives 25 on it because one comment line carries the string).

## Checks

- `sha256sum dataset/build*.manifest.json`: core `b6017a10…`, variants `087ef27c…`, transition grid `a8eebb33…`, return grid `2e57a6c1…`, flap-stress `dd6a7c24…`, distractor grid `264d3333…`, familiarity ladder `58a34d65…` — equal to `A2-rebuild.md`'s "after" column.
- `sha256sum harness/scoring/scoring-spec.yaml harness/guards/guard-spec.yaml`: `2ad757b6…`, `24ccb875…`, equal to their pins.
- HEAD build in the scratchpad: `make dataset variants PY=python3.12` exit 0, `make generated PY=python3.12` exit 0; the seven manifests equal `git show HEAD:<manifest>` byte for byte.
- HEAD build vs working-tree build, each artifact's JSON with `meta` removed: core 51/51 equal (`meta` differs in `sampled.archetypes` on 51, `derived_from` on 22 — `c1-*` but `c1-idle`, `c2-p1a`, `c2-p2a`, `c2-p3a`, `c3-*`, `c6-dual`); variants 78/78 equal (`sampled` 78, `derived_from` 31; entry fields `sha256` and `base_sha256` differ, `set`, `transform`, `utilization` unchanged); transition grid 480/480, return grid 720/720, flap-stress 24/24, distractor grid 272/272, familiarity ladder 66/66 equal (`sampled` alone). `reports`, `demand` and `grid` unchanged in every manifest that carries them.
- `python3.12 -c "yaml.safe_load(…)"` on `prior.yaml` and `rq0-gate.yaml`: both parse; the rendered `simulator-conformance` text read back.
- `make -C harness lint PY=python3.12`: exit 0, 3 min 16 s — `tools/lint.py` "lint clean"; `scoring_lint.py` "scoring spec: 49 files, 75 terms", the five generated sets derived, "lint clean"; `guards_lint.py` "guard spec 1.1: 8 guards, 3 C2 pairs", "lint clean"; `experiment_lint.py` "rq0-gate.yaml: experiment rq0-gate, 3 conditions, 19 judging + 32 reporting files, criterion k_of_n_gap", "lint clean" (it checks the pins' bytes, `evaluator._pin_errors`).
- `make -C harness test PY=python3.12`: **exit 2 — 294 passed, 2 failed, 2 deselected, 17 min 5 s.** Failed: `tools/tests/test_scorer.py::test_excess_aggregates_on_mock_switch` (`assert out[("excess_switch", "3")] == "100.000000000000"`, got `"0.000000000000"`, `test_scorer.py:146`) and `test_scorer.py::test_flip_aggregates_on_mock_switch` (`wrong_switch_excess_sum` `"100.000000000000"` expected, `"0.000000000000"` got, `:258`). Both read the mock-switch fixture, which A4 re-derived concurrently (W-0804: the switch excess is now 0 µs, was 100); `A4-fixture.md` logs the same two failures and leaves `test_scorer.py`, outside both steps' files, to the main session.
- Isolation of the two failures: HEAD's `harness/` and `daemon/` (`git archive HEAD harness daemon`) extracted to the scratchpad, this step's three files copied over them (`dataset/`, `docs/`, `simulator/` linked to the working tree), `python3.12 -m pytest tools/tests/test_scorer.py -q -m "not coreset_wide"`: 14 passed. With HEAD's fixture the two tests pass under this step's edits; they fail on A4's fixture alone.
- Re-measured at the end: `dataset/build.manifest.json`, `dataset/build.variants.manifest.json`, `daemon/driver-table/prior.yaml`, the scoring spec and the guard spec each hash to their pin in `rq0-gate.yaml` (5/5).

## Left for the main session

- `harness/tools/tests/test_scorer.py:137–149` and `:237–262` hard-code the old mock-switch switch excess (100 µs); `make -C harness test` passes only once they follow A4's fixture (excess 0 µs). Not this step's file.
- The (g) citation "(9.15 W-0743)" in `rq0-gate.yaml` can name the contract text once the step writing W-0743's interpretation-contract and `docs/data-contracts.md` §14 text lands; nothing pins the RQ0 gate spec, so that edit re-pins nothing.

## Review round 1

Verdict: **pass.** All four edit items are done. Each agrees with its W-row answer in `work-list.md` and with the code. `make -C harness lint` passes. `make -C harness test` fails on two tests, and those failures come from A4's mock-switch fixture, not from this step (isolated below). The commit cannot go in until `test_scorer.py` follows that fixture.

### Items

- **W-0758 (the RQ0 gate spec's conformance statement): correct.**
  - The closing sentence reads "(c) and (f) the simulator does today; the others its owner holds as owed. The run does not start until each is shown."
  - (g) reads as the answer gives it: "an orchestrator's WAIT children:<id> completes when the last child it spawned ends, and without blocking when none is live at the WAIT".
  - Checked against `simulator/src/sim.cpp`. Its last commit is `6bf9d850` (2026-10-10), and nothing under `simulator/` has changed in the working tree.
    - (c), the switch semantics: U1 is at `:47` and `:208` (a switch into MLFQ is a cold start, every task back to Q0). U2 is at `:48`, `:209` and `:607` (a same-algorithm entry leaves the holder and its pending slice alone).
    - (f), the frame chain's deadline: `deadline()` at `:404–408` falls back to the inherited `chain_dl`, and `deliver()` at `:786–795` carries the waker's deadline down the chain.
    - (g) is not in the code. `on_task_end` at `:758–768` unblocks a parent only when it is blocked on a fork slot (`wait_chan < 0`). "The others its owner holds as owed" therefore covers (g) correctly.
- **W-0777 (the driver table's LOTTERY clause, `prior.yaml:298`): correct.**
  - The old clause, which said the rule was "asked of 인경민 … and not yet answered", is gone. In its place is the answer's rule with its citation: `sim.cpp:328–366`, the class drawn by `batch_share` only when both classes are runnable, uniform within it, only runnable tasks holding tickets.
  - That citation range covers the LOTTERY comment block (`:328–333`) and `pick()`'s two-stage draw (`:362–371`). `docs/recognition-vocabulary.md` §2 says "equal tickets per task within a class".
  - No value changed. The only diff line is the justification string.
  - It differs from the answer's wording in two places, both noted in the editor's decision 3 and neither blocking:
    - It adds "the editor's own burst tail included while it is batch class". This keeps the subject of the clause it replaces and is true of the code: class membership is `view.batch(id)`, and the B1 rule at `:38–39` puts a task in the batch class after one slice.
    - It expands "vocabulary §2" to "recognition-vocabulary §2", the name `prior.yaml` uses at `:12`, `:35`, `:64` and `:194`.
- **The re-pins: correct.** Recomputed with `shasum -a 256`:
  - `dataset/build.manifest.json` `b6017a10…`, `dataset/build.variants.manifest.json` `087ef27c…` and `daemon/driver-table/prior.yaml` `0fba4b3c…` each equal their pin in `rq0-gate.yaml`.
  - The scoring spec (`2ad757b6…`) and the guard spec (`24ccb875…`) are unchanged and match their pins.
  - HEAD's `prior.yaml` hashes to `6e271dd0…`, the old pin.
  - The pins comment names the 2026-10-16 entry first.
- **The `harness/CHANGELOG.md` entry: correct, newest first, in the file's own style** (bold subject, the file, the decision row, the facts, then a Pins bullet and a pointer bullet, as in the 2026-10-14 and 2026-10-15 entries).
  - Every fact in the core-set and Pins bullets was checked. HEAD's `dataset/` tree was rebuilt in the scratchpad (`make dataset variants generated PY=python3.12`, exit 0, 4 min 54 s), and its seven manifests equal HEAD's committed ones byte for byte. Each working-tree artifact was then compared with HEAD's, with `meta` removed:
    - core: 51/51 equal; `meta` differs in `sampled.archetypes` on 51 and in `derived_from` on 22;
    - variants: 78/78 equal; `sampled.archetypes` 78, `derived_from` 31; the entries' `sha256` and `base_sha256` move, `set` and `transform` do not;
    - transition grid 480/480, return grid 720/720, flap-stress 24/24, distractor grid 272/272, familiarity ladder 66/66: equal, `sampled.archetypes` alone.
  - `reports`, `demand` and `grid` are equal in every manifest that has them.
  - Changed `inputs`: in the core manifest, the library, the schema and six `wlc` files; in each generated manifest, those plus `gen/__init__.py` and the 15 C1 timelines other than `c1-idle`. This matches "their `inputs` pinning the edited C1 timelines and tools".
  - All 3,304 pinned `build/` files in the working tree hash to their manifest entries.
  - The other facts match `A2-rebuild.md` and the code:
    - none of the five removed functions is left in `compiler.py`, and the refusal is a `ValueError` at `:157`;
    - `lint_bound_sources` under `--freeze` rejects a bound value tagged `meas-pending` (`linter.py:241`);
    - `dataset/meas-releases.yaml` has 23 campaigns, `lint.py:43` runs `lint_releases`, and the file is in no manifest's `inputs`;
    - 22 hand-authored timelines changed, and no derived one did.
  - The five generated manifest hashes in the Pins bullet equal the files on disk.
- **W-0801 (the input count correction): correct.**
  - The scoring spec at `a473070d`, the commit that wrote the 2026-10-09 entry, hashes to `5d8a3243…`, the same bytes as at `9c80113e` and as the RQ0 gate spec's pin then.
  - Parsed, it has 49 files and 75 terms: 24 on `channel: input` and 15 on `channel: timer`. The 15 timer terms sit in 14 files: `c1-` and `c7-` backup, photo, render, transcode and video-edit, `c2-p3a`, `c2-p3b`, `c3-creation`, and `c7-mail`. The working-tree spec parses to the same counts.
  - The 2026-10-09 entry is untouched: `git diff` on the file removes no line.
  - "c1-compile's build-turnaround term (judging, weight 1.0)" checks out: `c1-compile` is in `files.judging`, and its `build` turnaround term has weight 1.0.

### Checks rerun

- `make -C harness lint PY=python3.12`: exit 0, 3 min 25 s. All four lints say "lint clean". `experiment_lint` reports "rq0-gate.yaml: experiment rq0-gate, 3 conditions, 19 judging + 32 reporting files, criterion k_of_n_gap".
- `python3.12 -m pytest tools/tests/test_scorer.py -m "not coreset_wide"` on the working tree: 2 failed, 12 passed. The failures are `test_excess_aggregates_on_mock_switch` and `test_flip_aggregates_on_mock_switch`, the expected `"100.000000000000"` against `"0.000000000000"` at `:258`.
- The same run on HEAD's `harness/` and `daemon/` with this step's three files laid over them (`dataset/`, `docs/`, `simulator/` linked to the working tree): 14 passed. The two failures come from A4's fixture edit (`harness/tools/tests/fixtures/mock-switch/*`) alone.
- The full `make -C harness test` was not rerun. The editor's run (294 passed, 2 failed) plus the isolation above cover it.
- Scope: this step's three files are the only ones it changed. The other entries in `git status` belong to A1 (`dataset/sources.yaml`), A2 (the rest of `dataset/`) and A4 (the mock-switch fixture).

### For the main session

1. **Blocking the commit, not this step:** `harness/tools/tests/test_scorer.py:137–149` and `:237–262` still expect the old fixture's 100 µs switch excess. They must follow A4's fixture before `make -C harness test` passes. With the excess now 0, `wrong_switch_excess_sum` no longer tells a contributing wrong switch from a non-contributing one, so the flip test may need a different fixture case and not just a new number.
2. (g) cites "(9.15 W-0743)". Once the interpretation contract's FORK/WAIT text and the `docs/data-contracts.md` §14 entry land, (g) could cite them instead. Nothing pins the RQ0 gate spec, so that edit re-pins nothing.
3. The core-set bullet cites "W-0732", but A2 applied only its first part (the release map and its lint). "W-0732, first part" would be exact.
4. `docs/guidebook/dataset/07-build-gate-manifests-ci-tests.md:507` still quotes the old `driver_table` pin `6e271dd0…`. That file belongs to another step's chunk.
