# Rows — g6, harness docs and the READMEs under harness/

| file | lines | hits read | rows (A/B/C/D/E) |
|---|---|---|---|
| `docs/harness/harness-and-records-guide.md` | 1558 | 98 | 2/0/0/1/0 |
| `docs/harness/metrics.md` | 385 | 45 | 1/0/0/0/0 |
| `harness/README.md` | 82 | 14 | 0/4/0/0/0 |
| `harness/aggregates/README.md` | 25 | 3 | 0/0/0/0/0 |
| `harness/boot-defaults/README.md` | 16 | 1 | 0/0/0/0/0 |
| `harness/experiments/README.md` | 58 | 16 | 1/3/0/2/0 |
| `harness/grades/README.md` | 23 | 2 | 0/0/0/0/0 |
| `harness/guards/README.md` | 35 | 4 | 0/1/0/0/0 |
| `harness/records/README.md` | 32 | 2 | 0/0/0/0/0 |
| `harness/scores/README.md` | 20 | 5 | 0/0/0/0/0 |
| `harness/scoring/README.md` | 30 | 2 | 0/0/0/0/0 |
| `harness/tools/README.md` | 39 | 7 | 2/2/0/0/0 |
| `harness/tools/harness/README.md` | 31 | 5 | 0/2/0/0/0 |
| `harness/tools/tests/README.md` | 27 | 10 | 1/0/0/1/0 |
| `harness/tools/tests/fixtures/README.md` | 64 | 27 | 0/1/0/0/0 |
| `harness/tools/tests/mocks/README.md` | 31 | 11 | 0/0/0/0/0 |

Every file but the harness guide was read whole; the guide was read whole in §1, §3–§5, §13–§22 and at every hit elsewhere. Enumerating passages were compared with `ls` of `harness/`, `harness/tools/`, `harness/tools/harness/`, `harness/tools/tests/`, `harness/tools/tests/fixtures/`, `harness/experiments/` and `harness/experiments/schema/`, with `harness/Makefile`'s targets, and with the evaluator's line registry (`LINES`, `harness/tools/harness/evaluator.py`: sixteen line types, all sixteen in the guide's §19.4 table and in `harness/experiments/README.md`).

## Rows on the fifteen items

### g6-01 · `docs/harness/harness-and-records-guide.md:596` · A · item 2 (the integration gate passed)
- **Now:** "그 `WAIT`은 자식이 모두 끝났을 때 완료돼요 — … RQ0 gate spec의 simulator-conformance 항목 (g)예요. reference simulator는 아직 이 `WAIT`을 깨우지 않아서, 그 전까지는 `make`가 `EXIT`에 못 가고 이 row가 안 나와요."
- **Becomes:** reference simulator는 이 `WAIT`을 마지막 자식이 끝날 때 완료하고(simulator의 stage AA), 2026-11-14의 통합 gate(10.2)가 그것을 binary에서 보였어요. 그래서 `make`는 마지막 자식 뒤에 `EXIT`하고 이 row가 나와요. (The clause "interpretation contract에 제안된 규칙" in the same passage is row g6-22.)
- **From:** `harness/CHANGELOG.md`, 2026-11-14 "the integration gate passed" — statement `simulator-conformance`: (g) shown on the hand fixtures replayed through the binary and by black-box unit tests under `simulator/tests/`; `docs/memos/2026-11-15-integration-gate-and-cold-smoke.md` §2, the `test_spawn_children.py` row ((i), (g): `WAIT children:build` ends at the last child's `task_end`); `simulator/steps/README.md`, the stage aa row.

### g6-02 · `docs/harness/harness-and-records-guide.md:1473` · A · item 11 (the verdict final), with item 7 (the scorer's sign rule) and item 13 (the configuration search) as absences
- **Now:** "RQ0 run의 보고서는 `harness/experiments/rq0-gate/`에 gzip으로 commit돼 있어요(`docs/rq0-run-record.md`). 안에는 verdict와 그 근거, 파일별 gap과 seed별 점수, …"
- **Becomes:** 보고서의 verdict는 run이 낸 그대로 — fail, judging 파일 19개 중 6개, provisional — 이고 run 자신의 기록으로 남아요. 재측정 뒤의 final verdict는 fail, 19개 중 5개가 g를 넘음(K = 10)이고, run record의 Corrections(2026-11-21)에 있어요. sign rule로 다시 채점한 post hoc reading은 verdict가 아니고 `rq0-gate/post-hoc/`에 있어요(11.1). (item 13, optional) configuration search의 보고서는 `harness/experiments/rq0-config-search/`에 있어요(schema `search-report.schema.json`, 11.4).
- **From:** `docs/rq0-run-record.md`, "The outcome" (fail, provisional, 6 of 19 against K = 10); "Corrections", 2026-11-18 (the verdict stands as run; the post hoc reading at `harness/experiments/rq0-gate/post-hoc/`); "Corrections", 2026-11-21, "The closing" and the line after it (final: fail, 5 of 19 against K = 10); "The failure procedure", its last paragraph (the search's report folder); `harness/CHANGELOG.md`, 2026-11-21 configuration-search entry ("Report schema").
- **Flags:** for 인지오: the guide states no verdict anywhere else, so whether its report paragraph should carry the final one is a choice; and the search's report is not an experiment run's report, so the item-13 clause is optional.

### g6-03 · `docs/harness/metrics.md:335` · A · item 2 (the integration gate passed)
- **Now:** "A FORK that takes a free slot completes its fork-slot wait without blocking and is owed its zero-wait `ready(cause = fork_slot)` line (decided 2026-10-30; `../../simulator/memo/memo_261023.md` Part H)."
- **Becomes:** … completes its fork-slot wait without blocking and writes its zero-wait `ready(cause = fork_slot)` line, item (a)'s last case (the simulator's stage AB), shown on the binary by the integration gate of 2026-11-14 (10.2) on the hand fixtures replayed through it.
- **From:** `harness/CHANGELOG.md`, 2026-11-13 entry (`fix-object`, `fix-tree`: "every FORK writes its `ready(cause = fork_slot)` line, at zero wait when it took a free slot (item (a)'s last case)"); 2026-11-14 "the integration gate passed" (statement `simulator-conformance`: (a) on the hand fixtures replayed through the binary); `simulator/steps/README.md`, the stage ab row.

### g6-04 · `harness/README.md:33` · B · item 13 (the configuration search)
- **Now:** "| `experiments/` | the per-experiment specs and the report schema; `rq0-gate.yaml` is the RQ0 gate spec | …"
- **Becomes:** the per-experiment specs, the search spec, and their schemas (spec and report each); `rq0-gate.yaml` is the RQ0 gate spec, `rq0-config-search.yaml` the configuration search's search spec, each with its committed report in a folder beside it.
- **From:** `harness/CHANGELOG.md`, 2026-11-21 configuration-search entry ("Search spec", schema `experiments/schema/search-spec.schema.json`; "Report schema", `experiments/schema/search-report.schema.json`); `docs/rq0-run-record.md`, "The failure procedure", last paragraph.

### g6-05 · `harness/README.md:36` · B · item 2 (the integration gate passed), with item 5 (the runner and the cost)
- **Now:** "`Makefile`, the three targets below; …" and the block below it, which lists `make lint`, `make test-quick`, `make test`, `make test-full`, `make smoke`.
- **Becomes:** the Makefile's seven targets; the block gains `make gate` (the integration gate on `runner.yaml`'s real programs: unit tests and mutants, fixture replay, daemon comparison, short run) and `make gate-status` (its parts against the RQ0 gate spec's version pins). The count "three" becomes seven, or goes.
- **From:** `harness/Makefile` as it stands (lint, test-quick, test, test-full, smoke, gate, gate-status, and their help lines); `harness/CHANGELOG.md`, 2026-11-14 "the integration gate passed" (`make gate`, `make gate-status`); 2026-11-14 "the runner: runs at once and a results cache; the suite's quick tier" (`make test-quick`).

### g6-06 · `harness/README.md:52` · B · item 13 (the configuration search)
- **Now:** "To run a real experiment, copy `runner.example.yaml` to `runner.yaml` (git-ignored), point it at the real programs, and run: … `python3 tools/run.py --spec experiments/rq0-gate.yaml --machine runner.yaml`"
- **Becomes:** beside it, the search: `python3 tools/search.py --spec experiments/rq0-config-search.yaml --machine runner.yaml [--checks-only | --read-only]`; outputs under `runs/<search>/`; exit 1 when the spec is refused, a run failed or a check did not reproduce its run, otherwise 0.
- **From:** `harness/tools/search.py`, its docstring (code as it stands); `harness/CHANGELOG.md`, 2026-11-21 configuration-search entry, "Search tool".
- **Flags:** for 인지오: a row only if "Running it" counts as a passage that enumerates the tools (decision 6); otherwise left.

### g6-07 · `harness/README.md:72` · B · item 13 (the configuration search)
- **Now:** "Three files are data the code obeys and never a constant in code: the scoring spec, the guard spec, and the per-experiment spec."
- **Becomes:** four: … and the search spec, the data file the search tool reads, committed before any search run.
- **From:** `harness/CHANGELOG.md`, 2026-11-21 configuration-search entry, opening paragraph ("the search is a harness tool that reads a committed search spec, a data file as the RQ0 gate spec is, committed before any search run").

### g6-08 · `harness/experiments/README.md:5` · B · item 13 (the configuration search)
- **Now:** "`rq0-gate.yaml` is the RQ0 gate spec, committed 2026-09-12. Only pre-registered experiments live here; …"
- **Becomes:** add: `rq0-config-search.yaml` is the configuration search's search spec (the RQ0 gate spec's statement `failure-procedure`), committed 2026-11-21 before any search run (`79608bff`), its schema `schema/search-spec.schema.json`, run by `tools/search.py`.
- **From:** `docs/rq0-run-record.md`, "The failure procedure", 2026-11-21 (search spec, committed before any search run, `79608bff`, run by `harness/tools/search.py`); `harness/CHANGELOG.md`, 2026-11-21 configuration-search entry ("Search spec").

### g6-09 · `harness/experiments/README.md:7` · B · item 13 (the configuration search)
- **Now:** "`rq0-gate/` holds the RQ0 run's report (2026-11-18; `docs/rq0-run-record.md`): … `rq0-gate/post-hoc/` holds the run's post hoc reading, not its verdict: …"
- **Becomes:** add: `rq0-config-search/` holds the search's report (2026-11-21; `docs/rq0-run-record.md`, "The failure procedure"): `report.json` and `report.md` (schema `schema/search-report.schema.json`), `points.csv` — every term of every point, the file the report is read from again — and `runs.sha256.csv`, every run's trace hash and records hash, 4,700 lines.
- **From:** `docs/rq0-run-record.md`, "The failure procedure", last paragraph; `harness/CHANGELOG.md`, 2026-11-21 configuration-search entry ("Report schema").

### g6-10 · `harness/experiments/README.md:36` · B · item 4 (the unavailable rule)
- **Now:** "A failed non-exempt guard on a run the criterion reads makes the verdict `invalid` instead of pass or fail."
- **Becomes:** add: a failed non-exempt guard on a run a gap reads marks that gap unavailable on every listed file, and a line that reads an unavailable gap — a boot default's count, a band table's count, a variant line's count, the trace replay's agreement, the bounding pair's difference — gives no reading, marked unavailable with the failed guards beside it (2026-11-14, 10.3).
- **From:** `harness/CHANGELOG.md`, 2026-11-14 "a line that reads a gap from a run with a failed guard gives no reading" (Evaluator; statement `sensitivity-lines`); 2026-11-01 entry (a cap-band table's count marked unavailable "as it marks a boot default's").
- **Flags:** for 인지오: the paragraph names one effect of a failed guard rather than listing them; a decision-6 absence only if it is read as the whole set.

### g6-11 · `harness/experiments/README.md:52` · A · item 12 (the experiment lint), with item 13 (the configuration search) as an absence
- **Now:** "`python3 tools/experiment_lint.py [--spec experiments/rq0-gate.yaml]      # schema, files against the build, terms, registries, pins`", and no search command in the block.
- **Becomes:** the lint's comment: "… pins — an executed spec's as notes; a search spec by the search's lint"; a line `python3 tools/search.py --spec experiments/rq0-config-search.yaml --machine runner.yaml [--checks-only | --read-only]` — the checks, every point, the reading, the route, the report.
- **From:** `harness/CHANGELOG.md`, 2026-11-20 entry, "Experiment lint" (an executed spec's moved pin printed as a note, every other error still an error); 2026-11-21 configuration-search entry, "Experiment lint" and "Search tool"; `harness/tools/experiment_lint.py` and `harness/tools/search.py`, their docstrings.

### g6-12 · `harness/guards/README.md:35` · B · item 4 (the unavailable rule)
- **Now:** "A non-exempt failure on a run the RQ0 criterion reads turns the verdict into `invalid`, naming the guard and the run."
- **Becomes:** add: on a run a gap reads, it marks that gap unavailable, and a reporting line that reads the gap gives no reading (10.3, 2026-11-14).
- **From:** `harness/CHANGELOG.md`, 2026-11-14 "a line that reads a gap from a run with a failed guard gives no reading".
- **Flags:** for 인지오: as g6-10.

### g6-13 · `harness/tools/README.md:3` · A · item 2 (the integration gate passed)
- **Now:** "All of the harness's code: … the tests, and the two mocks that stand in for the daemon and the simulator until the real programs land."
- **Becomes:** … and the two mocks, test doubles kept in the test tree that the suite and `make smoke` run (`runner.example.yaml`); since the integration gate of 2026-11-14 (10.2) the runner's machine configuration runs the real programs, `simulator/src/sim` and `daemon/daemon.py`.
- **From:** `harness/CHANGELOG.md`, 2026-11-14 "the integration gate passed"; `harness/runner.example.yaml`, its header comment (the example drives the two mocks; the real programs named by the version their source prints); `harness/Makefile` (`smoke` on `runner.example.yaml`, `gate` on `runner.yaml`).

### g6-14 · `harness/tools/README.md:7` · B · item 13 (the configuration search)
- **Now:** the commands table — `records.py`, `score.py`, `guards.py`, `grade.py`, `evaluate.py`, `run.py`, `smoke.py`, `integration_gate.py` — with no row for `search.py`.
- **Becomes:** a row `search.py` | a search spec and a machine configuration → the boot default's and the row's points run and checked against the corrected runs, then every point of the grid on every file the spec names, the reading and the route; `report.json` and `report.md` under `runs/<search>/` (`--out-dir` also beside the spec); `--checks-only`, `--read-only` | 1 a refused spec, a failed run or a check that did not reproduce its run, else 0.
- **From:** `harness/tools/search.py`, its docstring; `harness/CHANGELOG.md`, 2026-11-21 configuration-search entry, "Search tool".

### g6-15 · `harness/tools/README.md:25` · A · item 12 (the experiment lint), with item 13 (the configuration search)
- **Now:** "| `experiment_lint.py` | every per-experiment spec against its schema, the build, the pinned scoring spec's terms, the registries, and its pins |"
- **Becomes:** … and its pins — on an executed spec, one whose run record is committed beside it, a pin the tree no longer matches is a note, not an error; a search spec (a top-level `search` key) by the search's own lint, its pins read as an executed spec's once its report is committed beside it.
- **From:** `harness/CHANGELOG.md`, 2026-11-20 entry, "Experiment lint"; 2026-11-21 configuration-search entry, "Experiment lint"; `harness/tools/experiment_lint.py`, its docstring.

### g6-16 · `harness/tools/README.md:39` · B · item 13 (the configuration search)
- **Now:** "Every judgement is data: the scoring spec, the guard spec, and the per-experiment spec. A constant in code is a bug."
- **Becomes:** … the per-experiment spec, and the search spec.
- **From:** `harness/CHANGELOG.md`, 2026-11-21 configuration-search entry, opening paragraph; `harness/tools/harness/search.py`, the docstring's last line ("Every judgement applied here is data in the spec, never a constant in code").

### g6-17 · `harness/tools/harness/README.md:5` · B · item 13 (the configuration search)
- **Now:** the module diagram, ending "runner: invokes the programs and drives all of the above".
- **Becomes:** a line beside it: search: a search spec's points run through the runner, read per file, the route.
- **From:** `harness/tools/harness/search.py`, its module docstring.

### g6-18 · `harness/tools/harness/README.md:15` · B · item 13 (the configuration search)
- **Now:** "## Module by module" — `reader.py` … `runner.py`, `integration.py`; no `search.py`.
- **Becomes:** a bullet: **`search.py`** is the configuration search (11.4): it lints a search spec and expands its grid, gives each point its table — every row the point's configuration, the oracle condition run under it — runs each point through the runner's `process_run` with the guards and the wait check beside it, checks the boot default's and the row's points against the corrected runs before the grid, reads every point per file at the primary, under the g band and under each alternative boot default, gives the route, and renders the report.
- **From:** `harness/tools/harness/search.py`, its module docstring; `harness/CHANGELOG.md`, 2026-11-21 configuration-search entry ("The point's run", "Search tool").

### g6-19 · `harness/tools/tests/README.md:27` · A · item 2 (the integration gate passed)
- **Now:** "They are what `make smoke` and the runner tests invoke, and they are discarded when the real programs land."
- **Becomes:** … the runner tests invoke; since the integration gate (10.2, 2026-11-14) the runner's machine configuration runs the real programs and the mocks stay in the test tree — `runner.example.yaml` drives them, and the gate compared `daemon/daemon.py` with the mock daemon on the RQ0 gate spec's run list.
- **From:** `harness/CHANGELOG.md`, 2026-11-14 "the integration gate passed" (the daemon byte-identical to the mock daemon on the 19 425 runs of the spec's run list); `harness/runner.example.yaml`; `harness/Makefile` (`smoke`); `harness/tools/tests/test_runner.py`, `_machine` (loads `runner.example.yaml`).

### g6-20 · `harness/tools/tests/fixtures/README.md:23` · B · item 7 (the scorer's sign rule)
- **Now:** "`scoring-spec.yaml` a four-term spec shaped to hit every scorer rule (a windowed P99, a no-headroom miss rate, a progress term, a turnaround censored under one seed) … `seam/` holds hand-written `fixed` and `oracle` records for `mock-p1a`, scored together with the records the writer produces from `mock-p1a`'s trace (the end-to-end seam test)."
- **Becomes:** the seam case carries the oracle-worse rule: the hog's progress term, the oracle 0.111111 worse than `fixed`, is no headroom and marked *oracle worse than fixed*, the file at 1.214286 (2026-11-18, 11.1); the expected scores carry `oracle_worse` and `n_oracle_worse`.
- **From:** `harness/CHANGELOG.md`, 2026-11-18 entry, "Tests"; `harness/tools/tests/fixtures/mock-scores/worked.md:107`; the header of `harness/tools/tests/fixtures/mock-scores/expected-scores.csv`.

## Stale outside the fifteen items (left alone)

### g6-21 · `harness/experiments/README.md:27` · D
- **Now:** "criterion: {type: k_of_n_gap, k: 13, g: 0.5, reference: oracle, compared: random, seed_statistic: mean}"
- **Why stale:** the RQ0 gate spec's K is 10 since 2026-10-09 (9.14; `harness/experiments/rq0-gate.yaml`, `criterion.k` and statement `k-grounding`); not one of the fifteen items.

### g6-22 · `docs/harness/harness-and-records-guide.md:596` · D
- **Now:** "그 `WAIT`은 자식이 모두 끝났을 때 완료돼요 — interpretation contract에 제안된 규칙이고 …"
- **Why stale:** the rule is in force since 인경민 agreed to it, recorded 2026-10-31 (`docs/data-contracts.md` §14, the 2026-10-31 entry; `harness/CHANGELOG.md`, 2026-10-31 "인경민's two replies recorded"); before Phase 10's items.

### g6-23 · `harness/experiments/README.md:32` · D
- **Now:** "… the executor assumptions pending confirmation, …"
- **Why stale:** 인경민 confirmed assumptions (1) and (2), recorded 2026-10-31 (`harness/CHANGELOG.md`, 2026-10-31; statement `executor-assumptions`); before Phase 10's items.

### g6-24 · `harness/tools/tests/README.md:11` · D
- **Now:** "About 300 tests."
- **Why stale:** written 2026-10-14 (`2e0a887c`); `grep -c "def test_"` over `harness/tools/tests/*.py` counts 364 test functions, parametrized cases not counted. The growth spans many changes, Phase 10's and Phase 11's tests among them, and no record holds a current count.
