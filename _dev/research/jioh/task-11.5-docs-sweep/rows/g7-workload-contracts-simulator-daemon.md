# Rows — g7 (workload docs, contracts, references, vocabulary, simulator and daemon guides, dataset READMEs, root README)

| file | lines | hits read | rows (A/B/C/D/E) |
|---|---|---|---|
| `docs/workload/coreset-guide.md` | 1272 | 52 | 7/1/1/0/0 |
| `docs/workload/building-plan.md` | 273 | 30 | 0/1/1/0/0 |
| `docs/workload/measurement-overview.md` | 229 | 22 | 0/0/0/0/0 |
| `docs/workload/scenario-catalog.md` | 36 | 10 | 0/0/0/0/0 |
| `docs/workload/archetype-plan.md` | 127 | 9 | 0/1/0/0/0 |
| `docs/workload/grounding-sources.md` | 90 | 2 | 0/0/0/0/0 |
| `docs/data-contracts.md` | 623 | 44 | 2/0/0/2/0 |
| `docs/references.md` | 985 | 43 | 0/0/0/0/0 |
| `docs/recognition-vocabulary.md` | 188 | 7 | 0/0/0/1/0 |
| `docs/simulator/simulator-guide.md` | 339 | 16 | 0/0/0/3/0 |
| `docs/simulator/interpretation-contract.md` | 78 | 4 | 0/0/0/0/0 |
| `docs/daemon/daemon-guide.md` | 193 | 11 | 6/0/0/0/0 |
| `dataset/README.md` | 233 | 15 | 3/0/0/1/0 |
| `dataset/tools/meas/README.md` | 48 | 5 | 0/1/0/0/0 |
| `README.md` | 27 | 1 | 0/0/0/1/0 |

Read against item 9 (stage AF) as the brief asked: `docs/simulator/simulator-guide.md` §9.5, its §5 batch-class passage and its glossary's *runnable / blocked / running* row, and `docs/data-contracts.md`'s fork-slot lines (§4 Example B (3), §9's `fork_slot` cause and `blocked_on`). None states rule B1's voluntary blocks, and none says a fork-slot wait is not a block; §9.5 asks about fork-slot wakeup ordering, not B1. Nothing there is overtaken by stage AF, so no teammate row. `docs/workload/measurement-overview.md`, brought in line by 11.3, holds nothing another item overtakes. `docs/references.md`: no citation entry's text states anything an item overturned.

### g7-01 · `docs/workload/coreset-guide.md:5` · A · item 10 (the re-measurement and the second bless)
- **Now:** "숫자는 `dataset/build.manifest.json`이 hash로 고정한 `coreset-single`의 51개 파일(2026-10-16에 re-bless된 build)과 그 manifest의 `demand` 기록"
- **Becomes:** the build named is the one the second bless re-blessed (2026-11-21). That bless changed three core files beyond the library's hash (`c1-ml-train`, `c2-p1a`, `c7-ml-train`) and moved no demand.
- **From:** `harness/CHANGELOG.md`, 2026-11-21 re-measurement entry, "The second bless" (3 of the core set's 51; no demand moves); `dataset/build.manifest.json` as committed at `2e3fade3`
- **Flags:** for 인지오: this was already stale before Phase 10. The first bless (2026-10-31, the manifest the RQ0 gate spec pins, `27d347bc…`) replaced the 2026-10-16 build, and the guide's 2026-10-31 prose update brought in that build's numbers but did not change this line.

### g7-02 · `docs/workload/coreset-guide.md:143` · A · item 2 (the integration gate passed)
- **Now:** "reference simulator(`simulator/src/sim.cpp`)는 아직 구현하지 않아서 그 simulator에서는 `make`가 run 끝까지 거기서 막혀 있어요(12장)."
- **Becomes:** reference simulator도 이 규칙대로 그 WAIT를 완료해요. conformance 항목 (g)이고, 2026-11-14 integration gate가 binary에서 보였어요(`fix-object`·`fix-tree` fixture 재생, unit test `simulator/tests/test_spawn_children.py`). "(12장)" 지시는 빠져요(g7-08).
- **From:** `harness/CHANGELOG.md`, 2026-11-14 "the integration gate passed" (`simulator-conformance`: (g) on the replayed fixtures and in the black-box unit tests); `docs/memos/2026-11-15-integration-gate-and-cold-smoke.md` §2 (`test_spawn_children.py`, items (i) and (g))

### g7-03 · `docs/workload/coreset-guide.md:286` · B · item 10 (the re-measurement and the second bless)
- **Now:** "| `cpu-batch` | `meas-ci:background:2026-10-03`, `-10-03c` | batch loop | finite | normal | `python`, `kdenlive_render`, `chrome`(spoof) | 7 |"
- **Becomes:** 측정 출처 `meas-ci:background:2026-10-03`, `-11-20`(`python3`의 자발적 block 사이 run과 run 뒤 block, 11.3의 재측정), `-10-03c`
- **From:** `dataset/archetypes.yaml`, `cpu-batch` `params` (`python3_run` and `python3_block`, `source: "meas-ci:background:2026-11-20"`) and `validation_stats.run`; `harness/CHANGELOG.md`, 2026-11-21 re-measurement entry, "The fold-in"

### g7-04 · `docs/workload/coreset-guide.md:354` · A · item 10 (the re-measurement and the second bless)
- **Now:** "`c2-p1a`의 `python`: RUN 28개 / SLEEP 27개로 1,389.885 s. 측정된 training은 자발적 block 사이를 평균 69.49 s(±27.3 %) 달려서 RUN 하나가 수십 초예요."
- **Becomes:** RUN 48개 / SLEEP 47개로 1,389.885 s. 측정된 training은 자발적 block 사이를 평균 55.27 s(±5.89 %, 11.3의 107 repeat) 달려서 RUN 하나가 수십 초예요.
- **From:** `dataset/build/coreset-single/c2-p1a.workload.json`, the `hog` program: RUN 48, SLEEP 47 (the file's SHA-256 `0678efa6…` equals `dataset/build.manifest.json`'s pin); `dataset/archetypes.yaml`, `cpu-batch` `validation_stats.stats` ("python3 runs between blocks 55.27 s +-5.89 % … over 107 repeats"); `docs/rq0-run-record.md`, Corrections, 2026-11-21, the campaign table

### g7-05 · `docs/workload/coreset-guide.md:441` · A · item 10 (the re-measurement and the second bless)
- **Now:** "`\"program\": [ { \"op\": \"RUN\", \"us\": 192 }, { \"op\": \"SLEEP\", \"us\": 378 }, /* … */ { \"op\": \"RUN\", \"us\": 6407092 }, { \"op\": \"EXIT\" } ]`" (§6.4, the `c2-p1a` hog)
- **Becomes:** `RUN 191`, `SLEEP 472`, …, the last `RUN 15491555`, then `EXIT`
- **From:** `dataset/build/coreset-single/c2-p1a.workload.json`, the `hog` program (its SHA-256 equals the build manifest's pin). The first bless gave 192, 378 and 6407092, from compiling the timeline against `dataset/archetypes.yaml` at `bb16f63a`.

### g7-06 · `docs/workload/coreset-guide.md:768` · A · item 10 (the re-measurement and the second bless)
- **Now:** "| hog | python | cpu-batch (`program: python3`) | 60 → finite | RUN 28 / SLEEP 27, `total_work` 1,389.885 s …"
- **Becomes:** RUN 48 / SLEEP 47. The `total_work` and the source map stay as they are; they are the timeline's, which is unchanged.
- **From:** `dataset/build/coreset-single/c2-p1a.workload.json`, the `hog` program

### g7-07 · `docs/workload/coreset-guide.md:793` · A · item 10 (the re-measurement and the second bless)
- **Now:** "training 쪽은 thread 하나, 자발적 block 사이 run이 평균 69.49 s(±27.3 %), 기본 policy nice 0."
- **Becomes:** 자발적 block 사이 run이 평균 55.27 s(±5.89 %)
- **From:** `dataset/archetypes.yaml`, `cpu-batch` `validation_stats.stats`; `docs/rq0-run-record.md`, Corrections, 2026-11-21, the campaign table (55.27 s ±5.89 %)

### g7-08 · `docs/workload/coreset-guide.md:1202` · C · item 2 (the integration gate passed)
- **Now:** "**reference simulator가 아직 못 하는 것** - orchestrator가 spawn한 자식이 모두 끝났을 때 `WAIT children:<id>`를 완료하지 않아요(3장). `c1-compile`의 build turnaround term(판정, weight 1.0)이 읽히려면 필요해요."
- **Becomes:** the box goes, because nothing in it is still open. In its place, under "결정된 것과 남은 것", a plain statement: reference simulator는 orchestrator의 자식이 모두 끝나면 `WAIT children:<id>`를 완료해요. conformance (g)이고, 2026-11-14 integration gate가 binary에서 보였어요(`harness/CHANGELOG.md`, 2026-11-14).
- **From:** `harness/CHANGELOG.md`, 2026-11-14 "the integration gate passed"

### g7-09 · `docs/workload/coreset-guide.md:1208` · A · item 2 (the integration gate passed)
- **Now:** "`random` condition은 driver table의 32 row에서 uniform하게 뽑아요(`harness/tools/tests/mocks/daemon.py`)."
- **Becomes:** cite `daemon/daemon.py` (`recognize_random`). That is the daemon the runner runs since the 2026-11-14 integration gate, byte-identical to the mock daemon on the RQ0 gate spec's 19,425 runs.
- **From:** `daemon/daemon.py`, `recognize_random`; `daemon/README.md`, the `random` row; `harness/CHANGELOG.md`, 2026-11-14 "the integration gate passed"

### g7-10 · `docs/workload/building-plan.md:79` · B · item 10 (the re-measurement and the second bless)
- **Now:** "| `cpu-batch` | … | `meas-ci:background:2026-10-03`, `:2026-10-03c` | `python` (S12), `kdenlive_render` (S7); `chrome` in `c6-spoof` (S2) |"
- **Becomes:** source `meas-ci:background:2026-10-03`, `:2026-11-20` (`python3`'s run between voluntary blocks and block per run, re-measured in 11.3), `:2026-10-03c`
- **From:** `dataset/archetypes.yaml`, `cpu-batch` `params` and `validation_stats.run`; `harness/CHANGELOG.md`, 2026-11-21 re-measurement entry

### g7-11 · `docs/workload/building-plan.md:223` · C · item 2 (the integration gate passed); item 6 (the RQ0 run); item 11 (the verdict final); item 13 (the configuration search and the route); item 15 (Phase 12 next)
- **Now:** "(5) simulator Phase 0 built to the contract            DES core, MLFQ executor, canonical loader / → first integration test: one C1 workload end-to-end / (6) RQ0 gate                                           the prior driver table, random vs oracle against fixed, on the RQ0 gate spec's 19 judging files (harness/experiments/rq0-gate.yaml)". In a ladder where every other step carries `[done]`, these two carry no marker: not yet done.
- **Becomes:** (5) gets `[done: the integration gate passed 2026-11-14, simulator@0d323c84470a, daemon@62c71f0d2de0]`. (6) stays open, narrowed: it ran 2026-11-16 to 2026-11-18 and failed, final on 2026-11-21 at 5 of 19 against K = 10. The configuration search's route is that the table is rewritten. What is still open is the gate itself: Phase 12's table rewrite and second RQ0 run. (7) "on gate pass" stays.
- **From:** `harness/CHANGELOG.md`, 2026-11-14 "the integration gate passed"; `docs/rq0-run-record.md`, "The run" (started, finished) and Corrections 2026-11-21, "The closing"; `docs/rq0-run-record.md`, "The failure procedure", "Route: the table is rewritten"; `_dev/docs/spec/jioh/phase-11-rq0-failure-procedure-diagnosis.md`, decision 1 (still open)
- **Flags:** for 인지오: the ladder shows status only by `[done]`. Whether (6) gets a marker for a run that failed, and in what words, is a form choice.

### g7-12 · `docs/workload/archetype-plan.md:83` · B · item 10 (the re-measurement and the second bless)
- **Now:** "| `cpu-batch` | … | `background:2026-10-03`, `background:2026-10-03c` | `python`, `kdenlive_render`; `chrome` in `c6-spoof` |"
- **Becomes:** Campaign `background:2026-10-03`, `background:2026-11-20` (`python3`'s run between voluntary blocks and block per run, 11.3), `background:2026-10-03c`
- **From:** `dataset/archetypes.yaml`, `cpu-batch` `params` and `validation_stats.run`; `harness/CHANGELOG.md`, 2026-11-21 re-measurement entry

### g7-13 · `docs/data-contracts.md:94` · A · item 10 (the re-measurement and the second bless)
- **Now:** "`python3_run: {dist: quantiles, p: [14, 112, 132, 188, 228276, 43515311, 238567291, 348129382, 876756180, 997987710], min: 12, max: 1006372964, means: […], sampling: per-iteration, source: \"meas-ci:background:2026-10-03\"}` / `python3_block: {dist: quantiles, p: [32, 46, 99, 216, 350, 404, 478, 516, 548, 560], min: 12, max: 561, …, source: \"meas-ci:background:2026-10-03\"}`" (§2, Example A; §1 says the examples are real where the dataset holds them)
- **Becomes:** `python3_run`: `p: [14, 141, 155, 191, 1223, 20473778, 204750672, 334780629, 759669393, 1177733035], min: 7, max: 1297955204`, source `"meas-ci:background:2026-11-20"`. `python3_block`: `p: [9, 71, 102, 330, 446, 521, 591, 629, 713, 799], min: 1, max: 1109`, source `"meas-ci:background:2026-11-20"`. The `kdenlive_render` lines are unchanged.
- **From:** `dataset/archetypes.yaml`, `cpu-batch` `params` (`python3_run`, `python3_block`)

### g7-14 · `docs/data-contracts.md:542` · A · item 2 (the integration gate passed)
- **Now:** "The mock daemon and the mock simulator under `harness/tools/tests/mocks/` are its first two implementations; 인경민's simulator and 박이안's daemon meet it when they deliver."
- **Becomes:** the mocks were its first two implementations. The simulator (`simulator/src/sim`) and the daemon (`daemon/daemon.py`) meet it: the runner has run them since the integration gate passed on 2026-11-14, on `simulator@0d323c84470a` and `daemon@62c71f0d2de0`.
- **From:** `harness/CHANGELOG.md`, 2026-11-14 "the integration gate passed"; `daemon/README.md`, "`daemon.py` — the running skeleton"

### g7-21 · `docs/daemon/daemon-guide.md:34` · A · item 2 (the integration gate passed)
- **Now:** (§1 diagram, the mapper box) "인지오 builds the table; the mapper wires in after (owner TBD)"
- **Becomes:** 인지오 builds the table; the mapper is in `daemon/daemon.py`, which composes each condition's configuration from the table
- **From:** `daemon/README.md`, "`daemon.py` — the running skeleton" (the three conditions compose their configurations from the driver table); `daemon/daemon.py`, its docstring's pipeline
- **Flags:** for 인지오: no record names the mapper's owner. Leave "(owner TBD)" or restate it.

### g7-22 · `docs/daemon/daemon-guide.md:145` · A · item 2 (the integration gate passed)
- **Now:** "The mapper is built against the schema and the steps above (tentatively also 박이안's); until it is, the pipeline runs **up to and including the validator**."
- **Becomes:** the mapper is built: `daemon/daemon.py` runs `fixed`, `oracle` and `random` through the validator and the mapper and writes config schedules. The runner has run it since the integration gate passed (2026-11-14, `daemon@62c71f0d2de0`). The five conditions that need a recognizer exit non-zero.
- **From:** `daemon/README.md`, "`daemon.py` — the running skeleton"; `harness/CHANGELOG.md`, 2026-11-14 "the integration gate passed"

### g7-23 · `docs/daemon/daemon-guide.md:151` · A · item 2 (the integration gate passed)
- **Now:** "*Emitting these needs the config mapper (§5); the prior table it reads is in place.*" (line 151) and "*This output needs nothing beyond the validator, so it's fully buildable now.*" (line 152)
- **Becomes:** `daemon/daemon.py` emits both outputs for `fixed`, `oracle` and `random`. They are byte-identical to the mock daemon's on the RQ0 gate spec's 19,425 runs (the integration gate, 2026-11-14).
- **From:** `harness/CHANGELOG.md`, 2026-11-14 "the integration gate passed" (the daemon byte-identical to the mock daemon on the 19 425 runs); `daemon/README.md`

### g7-24 · `docs/daemon/daemon-guide.md:162` · A · item 2 (the integration gate passed); item 6 (the RQ0 run); item 11 (the verdict final)
- **Now:** "**박이안's scope, now:** … Concretely, the first milestone — no LLM and no driver table anywhere in it: 1. … 2. Run the `fixed`, `random` (seeded), and `oracle` recognizers … 3. Rerun everything and diff" and (line 168) "With them, the config mapper + latency stamping close the loop and the daemon starts emitting **config schedules** — at which point `fixed`/`random`/`oracle` become the exact three conditions of the **RQ0 gate**, the project's first real experiment … Your milestone plus the simulator's milestone 0 *is* that experiment's machinery."
- **Becomes:** the milestone and the closed loop are reached. `daemon/daemon.py` runs the three model-free conditions through the validator and the mapper, and the integration gate passed on it and the simulator on 2026-11-14. The RQ0 run ran on that machinery from 2026-11-16 to 2026-11-18; its verdict is fail, final on 2026-11-21 at 5 of 19 against K = 10. The next step, the name tables and then the LLM conditions, stays as written.
- **From:** `harness/CHANGELOG.md`, 2026-11-14 "the integration gate passed"; `docs/rq0-run-record.md`, "The run" (programs, started, finished) and Corrections 2026-11-21, "The closing"

### g7-25 · `docs/daemon/daemon-guide.md:178` · A · item 13 (the configuration search and the route); item 11 (the verdict final); item 15 (Phase 12 next)
- **Now:** "Where it stands: the prior table is filled and judged pair by pair (`prior-table-pair-review.md`) and runs the RQ0 gate; the calibrated table, tuned per row on the driver table tuning set, is still to come (`../data-contracts.md` §10)."
- **Becomes:** the prior table is filled, judged pair by pair, and ran the RQ0 gate: fail, final 2026-11-21, 5 of 19 against K = 10. The configuration search after the fail (2026-11-21) found spread the prior table missed on 8 of its 10 files, so the route is the table rewritten. The rewrite and the second RQ0 run are Phase 12's. The calibrated table is still to come.
- **From:** `docs/rq0-run-record.md`, Corrections 2026-11-21, "The closing"; `docs/rq0-run-record.md`, "The failure procedure", 2026-11-21, "Route: the table is rewritten" (8 of the 10 files at finding 3); `_dev/docs/spec/jioh/phase-11-rq0-failure-procedure-diagnosis.md`, decision 1

### g7-26 · `docs/daemon/daemon-guide.md:186` · A · item 14 (the hold-time plan's step 1 moved)
- **Now:** "First the need is measured with no rule — hold time 0, no hysteresis — right after Phase 10's integration, under `oracle` and `random` only, no LLM: the hold-time plan's no-rule measurement (its step 1)."
- **Becomes:** "… after Phase 12's second RQ0 run, on the table and programs that run uses, under `oracle` and `random` only, no LLM: …"
- **From:** `_dev/docs/spec/jioh/phase-11-rq0-failure-procedure-diagnosis.md`, decision 10

### g7-27 · `dataset/README.md:30` · A · item 10 (the re-measurement and the second bless); item 12 (the experiment lint)
- **Now:** "build.variants.manifest.json   # the variants' lockfile: each variant's hash, its base's hash, its transform and its utilization (the RQ0 gate spec pins it)"
- **Becomes:** the RQ0 gate spec pins the first bless's bytes, the tree its run read. The committed manifest is the second bless's (2026-11-21). The experiment lint reads the gate spec's pin as a note because the spec has been run.
- **From:** `harness/experiments/rq0-gate.yaml`, `pins.variants.all` (`de9802e7…`) against the committed `dataset/build.variants.manifest.json` (`3438be7f…`); `harness/CHANGELOG.md`, 2026-11-20 (the experiment lint) and 2026-11-21 re-measurement entry (the RQ0 gate spec not edited, its dataset and variants pins naming the first bless)

### g7-28 · `dataset/README.md:88` · A · item 10 (the re-measurement and the second bless)
- **Now:** "`{ \"op\": \"arrive\", \"t\": 60000000, \"id\": \"hog\", \"name\": \"python\", \"declared_class\": \"normal\", \"program\": [ { \"op\": \"RUN\", \"us\": 192 }, { \"op\": \"SLEEP\", \"us\": 378 }, /* … */ { \"op\": \"EXIT\" } ] }`" (the abridged excerpt of the compiled `c2-p1a`)
- **Becomes:** `RUN 191`, `SLEEP 472`
- **From:** `dataset/build/coreset-single/c2-p1a.workload.json`, the `hog` program (its SHA-256 equals `dataset/build.manifest.json`'s pin). The first bless gave 192 and 378.

### g7-29 · `dataset/README.md:128` · A · item 10 (the re-measurement and the second bless); item 12 (the experiment lint)
- **Now:** "recorded with its base's hash, its transform and its utilization in `build.variants.manifest.json`, which the RQ0 gate spec pins."
- **Becomes:** the same restatement as g7-27. The RQ0 gate spec pinned the first bless's manifest for its run, and since the second bless the committed manifest is not the pinned one.
- **From:** as g7-27

### g7-31 · `dataset/tools/meas/README.md:39` · B · item 10 (the re-measurement and the second bless)
- **Now:** "| `background/` | 9.7's background campaign and 9.10's background jobs (the upgrade, the DKMS build, Tracker, the MNIST training, the transcode, the Kdenlive export, Déjà Dup) | `meas-background.yml` | … | `analyze.py`, `nettrace.py`, `modbuild.py` | `pool.py` | `batch_fold_in.py` |"
- **Becomes:** add to the Campaign column, at the same detail: "and 11.3's re-measurement of the MNIST training (`meas-ci:background:2026-11-20`)". The tools are unchanged; 11.3's analysis lives in `analyze.py` (the fold of the runner agent's waits, `agent_woken`).
- **From:** `harness/CHANGELOG.md`, 2026-11-21 re-measurement entry, "The campaign" (`dataset/tools/meas/background/analyze.py`); `_dev/research/jioh/task-11.3-the-re-measurement/campaign/method.md`, §1 (workflow `meas-background.yml`, `run.sh`, `analyze.py`, `pool.py`) and §5, 2026-11-20, the fold

## Outside the fifteen items (class D)

### g7-15 · `docs/data-contracts.md:224` · D
- **Now:** "`\"sampled\": { \"seed\": 201, \"archetypes\": \"archetypes.yaml@c78d8cf…\" }`" — "the two above as built at this writing"
- **Why left:** the text dates itself ("at this writing"). `c78d8cf` is the 2026-10-17 library. It moved on 2026-10-31 (the first bless, `aa2f884`) and again at the second bless (`a25178d`, in the compiled `c2-p1a` now).

### g7-16 · `docs/data-contracts.md:245` · D
- **Now:** "`// …11,342 more WAIT/RUN pairs — 10,817 more on timer:editor, 525 on input:editor —`"
- **Why left:** stale since the 2026-10-31 rebuild, the wakes by origin, which is not one of the fifteen items. The compiled editor has 11,293 pairs (10,740 timer, 28 event, 525 input), as the same section's (1) paragraph and Example C already say. The first and second bless are equal here.

### g7-17 · `docs/recognition-vocabulary.md:70` · D
- **Now:** "The batch class is determined behaviorally by the executor (observed CPU-bound behavior — the same evidence MLFQ demotion uses); the classification rule is identical across algorithms, frozen in the simulator's docs, and not configurable."
- **Why left:** rules B1 and B2 are not in the simulator's docs. `docs/memos/2026-11-19-simulator-changes-by-jioh.md` §1 item 3 (item 9's record) states that the batch-class memo's §7 item 5, writing them into the simulator's semantics notes, is still open; the rule lives in `docs/memos/2026-09-09-batch-class-rule-for-the-simulator.md` with its 2026-11-19 correction. "the same evidence MLFQ demotion uses" has also been loose since 2026-10-30: MLFQ keeps a level's allotment across blocks, while B1 resets at each voluntary block. Both are older than stage AF; stage AF only adds the fork-slot wait to B1's list.

### g7-18 · `docs/simulator/simulator-guide.md:259` · D
- **Now:** "## 7. The first integration gate, and a suggested path to it — The one fixed goalpost the project needs from the simulator first … the RQ0 experiment (the project's first real measurement) becomes possible shortly after it."
- **Why left:** the goalpost, written as still ahead, was met before Phase 10: all four gate items are ✅ in `simulator/steps/README.md` §7, item 4 on 2026-11-11. If 인지오 wants the "becomes possible" clause restated, the RQ0 run (item 6) has since run on this simulator.

### g7-19 · `docs/simulator/simulator-guide.md:282` · D
- **Now:** "These are real ambiguities … where one has been decided (§9.1–§9.3), the answer." (with §9.4 "Depart mid-anything" and §9.5 "Fork-slot wakeups" still open)
- **Why left:** the simulator has decided both: `simulator/steps/README.md` D3 for §9.4 and the "§9.5 fork 슬롯" note for §9.5. These are outside the fifteen items. Stage AF (item 9) is not §9.5's matter: it is B1's counter at a fork-slot wait, which §9.5 does not ask about.

### g7-20 · `docs/simulator/simulator-guide.md:117` · D
- **Now:** "(`simulator/src/sim.cpp:210`, `:597`)"; at line 255 "`simulator/src/sim.cpp:734–738`, `:740–756` … `:686–695` … `:800–806`"; at line 299 "`:734–737`, `:753` … `:674`"
- **Why left:** the line numbers point at other code now. For example, D4's TIMER anchor is at `:1043` and `on_arrive` at `:1155`. They were already wrong before Phase 10: at `8dab1176` (2026-10-28) `on_arrive` was at `:1045`. Stages AD, AE and AF moved them again. Function names would hold where line numbers do not.

### g7-30 · `dataset/README.md:82` · D
- **Now:** "`{ \"op\": \"RUN\", \"us\": 22 }, /* … 22,689 instructions, the last a WAIT */ ] },`" and line 83 "`{ \"op\": \"wake\", \"t\": 2469, \"channel\": \"timer:editor\", \"target\": \"editor\" }`"
- **Why left:** stale since the 2026-10-31 rebuild. The compiled editor program has 22,587 instructions and its first timer wake is at t = 2470, the same at the first and second bless. Only the hog's values (g7-28) moved by item 10.

### g7-32 · `README.md:18` · D
- **Now:** "The [`dataset-build-2026-10-26`](…) release holds both, built at `6dec33a0`. Download `dataset-build-2026-10-26.tar.gz` from it and, from the repo root at that commit or a later one whose manifests are unchanged:"
- **Why left:** the manifests changed on 2026-10-31, and the release list already holds a later `dataset-build-2026-10-31` (built at `84ce79bf`) that the README does not name. Since the second bless (item 10), neither release matches the committed manifests. The sentence is conditional and so not false.
- **Flags:** for 인지오: no build release holds the second bless's build.

## Added at K8's review (2026-11-21)

### g7-33 · `docs/references.md:129` · A · item 10 (the re-measurement)
- **Now:** "… a width fixed at 5 % of the mean and a count of 5 to 77" (`chow-aoms65`'s role)
- **Becomes:** "… a count of 5 to 107"
- **From:** `docs/rq0-run-record.md`, Corrections, 2026-11-21, "The campaign" (107 fresh repeats); as g0-16

### g7-34 · `docs/references.md:134` · A · item 10 (the re-measurement)
- **Now:** "The campaigns' counts run 5 to 77, most below its 30" (`cochran-st77`'s role)
- **Becomes:** "5 to 107, most below its 30" — 11.3's 107 is the one campaign above 30
- **From:** as g7-33

## Added at the second search (2026-11-21)

### g7-35 · `docs/workload/coreset-guide.md:399` · A · item 10 (the second bless)
- **Now:** `"sampled": { "archetypes": "archetypes.yaml@c78d8cf9…", "seed": 201 }` — in §6, whose program lines (g7-05) and whose source line 5 (g7-01) now name the second bless's build
- **Becomes:** `archetypes.yaml@a25178d1…`
- **From:** `dataset/build/coreset-single/c2-p1a.workload.json`, `meta.sampled` (its SHA-256 `0678efa6…` is the entry in `dataset/build.manifest.json`)
