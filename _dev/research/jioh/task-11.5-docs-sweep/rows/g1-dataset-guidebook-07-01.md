# Rows — g1, dataset guidebook chapters 7 and 1

| file | lines | hits read | rows (A/B/C/D/E) |
|---|---|---|---|
| `docs/guidebook/dataset/07-build-gate-manifests-ci-tests.md` | 1781 | 166 | 15/6/0/2/1 |
| `docs/guidebook/dataset/01-the-big-picture.md` | 1648 | 54 | 11/3/1/0/1 |

Hashes this group writes that no changelog or spec lists were computed on 2026-11-21 as `git show HEAD:<manifest> | shasum -a 256` (commit `2e3fade3`, the second bless, the last commit to touch all seven manifests); the same at `2e3fade3~1` reproduces every value the chapter 7 tables now label 현재, so those columns are the first bless. `_dev/research/jioh/task-11.3-the-re-measurement/bless-report.json` holds no manifest hash: it holds `library_blob` (head `aa2f8842…`, working tree `a25178d1…`) and, per manifest, the `beyond_hash` list and an empty `demand_moves`. "The experiment lint, 2026-11-21" below is `python3.12 harness/tools/experiment_lint.py` run that day: `rq0-config-search.yaml: search rq0-config-search, 10 files, 470 points; executed, its report in rq0-config-search/report.json`; `rq0-gate.yaml: experiment rq0-gate, 3 conditions, 19 judging + 32 reporting files, criterion k_of_n_gap; executed, its run recorded in rq0-gate/runs.sha256.csv`; two notes, `pins/dataset` (`9f30ea8f…` != pinned `27d347bc…`) and `pins/variants/all` (`3438be7f…` != pinned `de9802e7…`), each "— the pin names the tree the run read"; `lint clean`.

## Chapter 7 — build gate, manifests, CI, tests

### g1-01 · `docs/guidebook/dataset/07-build-gate-manifests-ci-tests.md:143` · E · items 2, 10, 12, 13 (the integration gate; the second bless; the experiment lint's notes; the configuration search)
- **Now:** "이 권이 다루는 장치들은 한 번에 생기지 않았습니다. 기록에 남은 순서는 이렇습니다." … last line "2026-10-17  9.16  최종 build 위의 full smoke를 집에서 손으로: 이튿날 02:22에 exit 0, 4 h 32 min (호출 392번 중 250번이 cache에서)"
- **Becomes:** (if the ladder is meant whole) lines at its detail: `2026-11-01  10.1  RQ0 gate spec이 cap band의 세 table을 driver_table_alternatives로 pin`; `2026-11-14  10.2  RQ0 gate spec이 simulator와 daemon의 version을 pin, runner가 다른 version을 run 전에 거부: driver table과 세 table re-pin`; `2026-11-20  11.3  experiment lint가 실행된 spec(옆에 run record가 commit된 spec)의 pin을 note로 읽음`; `2026-11-21  11.3  cpu-batch의 python3 두 값을 107 repeat로 다시 재어 fold-in: rebuild, 두 번째 bless, RQ0 gate spec은 re-pin하지 않음`; `2026-11-21  11.4  configuration search spec이 두 번째 bless의 core manifest를 pin`.
- **From:** `harness/CHANGELOG.md`, 2026-11-01 entry (spec `task-10.1-gate-spec-pre-run-lines.md`; "Pins"); 2026-11-14 entry "the integration gate passed" (spec `task-10.2-integration-gate.md`; "Spec schema, runner and evaluator", "Pins"); 2026-11-20 entry "Experiment lint"; 2026-11-21 re-measurement entry, opening paragraph and "The second bless"; 2026-11-21 configuration search entry, "Search spec" (its pins)
- **Flags:** for 인지오: cannot decide — the ladder stops at Phase 9's end and already lacks the two 2026-10-31 rebuilds that 3.7 carries (outside the fifteen items); whether it is a Phase 9 chronology (left) or the whole one (extended, the 2026-10-31 lines with it).

### g1-02 · `docs/guidebook/dataset/07-build-gate-manifests-ci-tests.md:237` · A · items 10, 12, 13 (the second bless; the experiment lint's notes; the configuration search)
- **Now:** "harness/experiments/rq0-gate.yaml / pins.dataset = sha256(build.manifest.json) / pins.variants.all = sha256(build.variants.manifest.json)" and "그리고 실험 쪽의 RQ0 gate spec이 core manifest와 variants manifest의 SHA-256을 `pins`로 적습니다. 이 사슬 덕분에, 입력 파일 한 바이트가 바뀌면 그 변화가 실험 사양의 hash 한 줄까지 전파되어 눈에 보입니다."
- **Becomes:** 그림에 `harness/experiments/rq0-config-search.yaml  pins.dataset = sha256(build.manifest.json)`을 더함(variants pin 없음). RQ0 gate spec의 두 pin은 실행된 spec의 pin이라 그 run이 읽은 첫 bless(`27d347bc…`, `de9802e7…`)를 가리키고, 2026-11-21의 두 번째 bless 뒤 지금의 manifest(`9f30ea8f…`, `3438be7f…`)와 다름. 바뀐 바이트는 실행 전의 spec에서는 pin 오류로, 실행된 spec에서는 experiment lint의 note로 보임.
- **From:** `harness/experiments/rq0-config-search.yaml`, lines 254–264 (the pins' comment and block); `harness/experiments/rq0-gate.yaml`, lines 663, 665; `harness/CHANGELOG.md`, 2026-11-21 re-measurement entry, opening paragraph ("its dataset and variants pins name the first bless"); 2026-11-20 entry; the committed manifests' SHA-256 and the experiment lint, 2026-11-21 (above)

### g1-03 · `docs/guidebook/dataset/07-build-gate-manifests-ci-tests.md:266` · B · item 10 (the second bless)
- **Now:** "library의 두 값은 이렇게 움직였습니다 …" last row "| `17f28d7f` (2026-10-17, 9.16) | 출구 감사가 찾은 문장과 꼬리표: … | `c78d8cf9…` | `1e308606…` |"; line 277 "뒤의 다섯 번은 값이 아니라 문장과 꼬리표만 바뀌었지만 …"
- **Becomes:** 행 더함: "| `2e3fade3` (2026-11-21, 11.3) | `cpu-batch`의 `python3` 두 값(voluntary block 사이의 run, run마다의 block)을 campaign `meas-ci:background:2026-11-20`의 107 repeat 값으로 바꾸고 scope가 두 campaign을 적음 | `a25178d1…` | `34efc7de…` |". 277행의 "뒤의 다섯 번"은 Phase 9의 다섯 행에 한정(새 행은 값이 바뀜).
- **From:** `bless-report.json`, `library_blob.working_tree` = `a25178d113f0…` (= `git rev-parse HEAD:dataset/archetypes.yaml`); the committed core manifest at `2e3fade3`, `inputs["dataset/archetypes.yaml"]` = `34efc7de60f7…` (at `2e3fade3~1`: `85570c57ac83…`); `harness/CHANGELOG.md`, 2026-11-21 re-measurement entry, "The campaign" and "The fold-in"
- **Flags:** for 인지오: the table, like 1.7's ladder, also lacks the two 2026-10-31 library versions (`6267dbde…`, then `aa2f8842…`; outside the fifteen items) — add the item-10 row alone, or all three.

### g1-04 · `docs/guidebook/dataset/07-build-gate-manifests-ci-tests.md:287` · A · items 10, 12 (the second bless; the experiment lint's notes)
- **Now:** "5. core manifest와 variants manifest의 SHA-256이 바뀌므로 RQ0 gate spec의 두 pin을 다시 적어야 합니다."
- **Becomes:** 실행 전의 실험 사양이면 두 pin을 다시 적음. 실행된 spec(옆에 run record가 commit된 spec; RQ0 gate spec의 `experiments/rq0-gate/runs.sha256.csv`)은 다시 적지 않음: 그 pin은 run이 읽은 tree를 가리키고 experiment lint가 맞지 않는 pin을 note로 출력함. 2026-11-21의 두 번째 bless가 그 예.
- **From:** `harness/CHANGELOG.md`, 2026-11-20 entry "Experiment lint"; 2026-11-21 re-measurement entry, opening paragraph; `harness/tools/experiment_lint.py`, docstring

### g1-05 · `docs/guidebook/dataset/07-build-gate-manifests-ci-tests.md:489` · A · items 10, 12 (the second bless; the experiment lint's notes)
- **Now:** "| 고친 것 | core manifest | variants manifest | generated manifest 5개 | RQ0 gate spec pin | 기록된 사례 |" with "`dataset`, `variants`" in that column on every row
- **Becomes:** 열이 뜻하는 것: 그 바이트와 어긋나는 pin. 실행 전의 spec이면 re-pin할 pin, 실행된 RQ0 gate spec에서는 experiment lint의 note(2026-11-20부터). 지금 core manifest를 pin하는 configuration search spec에는 `dataset` 줄만 해당(variants pin 없음).
- **From:** `harness/CHANGELOG.md`, 2026-11-20 entry; `harness/experiments/rq0-config-search.yaml`, lines 258–264

### g1-06 · `docs/guidebook/dataset/07-build-gate-manifests-ci-tests.md:549` · A · items 2, 13 (the integration gate; the configuration search)
- **Now:** "dataset 바깥에서 dataset을 pin하는 파일은 지금 하나입니다. RQ0 gate spec(`harness/experiments/rq0-gate.yaml`)입니다. … 지금의 block은 이렇습니다(… driver table은 2026-10-31의 driver table 항목의 re-pin, 세 table pin은 2026-11-01의 pre-run lines 항목)." block "driver_table: {… sha256: 36267c38…}", "floor-0.2: {… 58c1107e…}", "floor-0.333: {… 4fe86c3f…}", "floor-0.5: {… 9295b76e…}"; the list below it ends at "`variants.all` — variants manifest입니다."
- **Becomes:** dataset을 pin하는 파일은 둘: RQ0 gate spec과 configuration search spec(`harness/experiments/rq0-config-search.yaml`, `pins.dataset` `9f30ea8f…`, 두 번째 bless의 core manifest; variants pin 없음). block은 `rq0-gate.yaml` 654–668행 그대로: driver_table `f693bfbe…`, floor-0.2 `6cbae471…`, floor-0.333 `1020d6ab…`, floor-0.5 `38f8de5e…`, dataset `27d347bc…`과 variants `de9802e7…`은 그대로, 그리고 `simulator: {version: simulator@0d323c84470a}`, `daemon: {version: daemon@62c71f0d2de0}`. 괄호: driver table과 세 table과 두 program pin은 2026-11-14의 통합 gate 항목(compile row의 LOTTERY 설명이 `struct Lottery`를 이름으로 인용, 값은 그대로). 목록에 `simulator`, `daemon`: 통합 gate가 통과한 version 문자열, runner가 machine configuration의 version과 다르면 run 전에 거부.
- **From:** `harness/experiments/rq0-gate.yaml`, lines 654–668; `harness/CHANGELOG.md`, 2026-11-14 entry "the integration gate passed", "Driver tables", "Pins" and "Spec schema, runner and evaluator"; `harness/experiments/rq0-config-search.yaml`, lines 254–264
- **Flags:** D inside the passage: the parenthetical credits the dataset and variants pins to the 2026-10-31 entry "a measured program's own wakes by origin", whose pins are `d80f06e0…`/`4cb07941…`; `27d347bc…`/`de9802e7…` are the same day's entry "each measured operation's largest run" (`harness/CHANGELOG.md`, lines 140–145) — a misattribution outside the fifteen items.

### g1-07 · `docs/guidebook/dataset/07-build-gate-manifests-ci-tests.md:574` · A · items 10, 12 (the second bless; the experiment lint's notes)
- **Now:** "2026-10-31에 이 다섯 경로의 파일을 `shasum -a 256`으로 계산해 보면 다섯 값 모두 pin과 같습니다. 즉 지금 저장소의 상태는 RQ0 gate spec이 사전 등록한 상태와 일치합니다. 2026-11-01에 더해진 세 table pin도 같습니다."
- **Becomes:** 2026-10-31의 확인은 그날의 사실로 둠. 2026-11-21의 두 번째 bless 뒤 dataset과 variants의 두 파일은 pin과 다름(`9f30ea8f…`, `3438be7f…`). RQ0 gate spec은 실행된 spec이라 다시 pin하지 않았고 두 pin은 run이 읽은 첫 bless를 가리킴; experiment lint는 둘을 note로 출력하고 `lint clean`. 나머지 pin(scoring spec, guard spec, driver table, 세 table)은 지금 파일과 같음(lint가 note를 내지 않음).
- **From:** the experiment lint, 2026-11-21 (above); `harness/CHANGELOG.md`, 2026-11-21 re-measurement entry, opening paragraph; 2026-11-20 entry

### g1-08 · `docs/guidebook/dataset/07-build-gate-manifests-ci-tests.md:593` · A · items 10, 12, 13 (the second bless; the experiment lint's notes; the configuration search)
- **Now:** "`re-pin`은 dataset이 다시 bless되어 manifest의 hash가 바뀌었을 때, RQ0 gate spec의 `pins` 값을 새 hash로 고쳐 적는 것입니다. 기록에 남은 절차는 매번 같습니다."
- **Becomes:** re-pin은 실행 전의 실험 사양에 하는 일(절차 1–5는 그 경우 그대로). 실행된 spec은 다시 pin하지 않음: 2026-11-21의 두 번째 bless에서 RQ0 gate spec은 고쳐지지 않았고(그 pin은 첫 bless), 그 뒤 commit된 configuration search spec이 두 번째 bless의 core manifest를 pin함.
- **From:** `harness/CHANGELOG.md`, 2026-11-21 re-measurement entry, opening paragraph; 2026-11-20 entry; 2026-11-21 configuration search entry, "Search spec" ("the pins — the dataset manifest of the second bless"); `harness/experiments/rq0-config-search.yaml`, lines 254–255

### g1-09 · `docs/guidebook/dataset/07-build-gate-manifests-ci-tests.md:603` · A · items 2, 12, 13 (the integration gate; the experiment lint's notes; the configuration search)
- **Now:** "이 함수는 두 곳에서 불립니다. 하나는 `make -C harness lint`가 부르는 `tools/experiment_lint.py`이고 … 예를 들어 dataset만 다시 bless하고 re-pin을 잊었다면 다음과 같은 모양이 됩니다 … `2 error(s)`" and (622) "manifest는 commit했지만 re-pin을 잊었다면 dataset check는 통과하고 harness lint에서 멈춥니다."
- **Becomes:** experiment lint는 run record(`experiments/<experiment>/runs.sha256.csv`)가 옆에 commit된 spec을 실행된 spec으로 읽음: 요약 줄 끝에 "; executed, its run recorded in rq0-gate/runs.sha256.csv", 맞지 않는 pin은 "note: pins/… — the pin names the tree the run read"이고 오류가 아님(지금의 RQ0 gate spec이 그 경우). 예시의 `2 error(s)`는 run record가 없는 spec의 모양. `search` key가 있는 spec은 search의 lint가 보고, report가 옆에 commit되면 그 pin도 note. `simulator`·`daemon` version pin은 `_pin_errors`가 아니라 runner의 `program_pin_errors`가 run 전에 machine configuration과 대조. 622행: 실행된 spec이면 re-pin을 잊어도 harness lint는 멈추지 않음.
- **From:** `harness/tools/experiment_lint.py`, docstring and `main`; `harness/CHANGELOG.md`, 2026-11-20 entry; 2026-11-21 configuration search entry, "Experiment lint"; 2026-11-14 entry "the integration gate passed", "Spec schema, runner and evaluator"; `harness/tools/harness/runner.py`, `program_pin_errors` (line 685); the experiment lint, 2026-11-21

### g1-10 · `docs/guidebook/dataset/07-build-gate-manifests-ci-tests.md:643` · B · item 10 (the second bless)
- **Now:** "RQ0 gate spec의 dataset과 variants pin이 지금까지 어떻게 움직였는지를 harness changelog와 sub-task changelog에서 모읍니다." — last row "| 2026-10-31 | 같은 항목의 결정 17, 18 | `27d347bc…` | `de9802e7…` | … |"
- **Becomes:** 행 더함: "| 2026-11-21 | 11.3 (재측정과 두 번째 bless) | `9f30ea8f…` | `3438be7f…` | `cpu-batch`의 `python3`의 voluntary block 사이의 run(55.27 s ±5.89 %)과 run마다의 block(403.96 µs ±2.15 %)을 campaign `meas-ci:background:2026-11-20`의 107 repeat로 다시 재어 library에 넣음, `carried_values`가 새 반폭. library hash 너머로 바뀐 것은 core 51개 중 3개(`c1-ml-train`, `c2-p1a`, `c7-ml-train`)와 variant 78개 중 14개, 모두 `python3`를 품은 파일, demand는 그대로. RQ0 gate spec은 고치지 않음(그 pin은 첫 bless, experiment lint가 note로 읽음); configuration search spec이 이 core manifest를 pin |". 머리 문장: 표는 manifest의 hash와 그것을 pin한 spec — 2026-10-31까지는 RQ0 gate spec의 pin, 2026-11-21 행은 configuration search spec의 pin.
- **From:** core `9f30ea8f3a99…`: the committed `dataset/build.manifest.json`'s SHA-256 (above); the same value in `harness/experiments/rq0-config-search.yaml` line 259 (`pins.dataset`), in `dataset/build.variants.manifest.json` line 912 (its `inputs` entry for the core manifest), in `harness/experiments/rq0-config-search/report.json` line 9, and in the experiment lint's note, 2026-11-21. Variants `3438be7f516f…`: the committed `dataset/build.variants.manifest.json`'s SHA-256, and the experiment lint's note, 2026-11-21. RQ0 gate spec's pins unchanged: `harness/experiments/rq0-gate.yaml` lines 663, 665. What changed: `harness/CHANGELOG.md`, 2026-11-21 re-measurement entry, "The campaign", "The fold-in", "The second bless"; `bless-report.json`, `manifests."build.manifest.json".beyond_hash` and `manifests."build.variants.manifest.json".beyond_hash`
- **Flags:** for 인지오: the variants manifest's hash is held by no changelog entry or spec — only by the committed manifest and the lint's output (`rq0-config-search.yaml` pins no variants manifest).

### g1-11 · `docs/guidebook/dataset/07-build-gate-manifests-ci-tests.md:663` · B · items 1, 2 (the pre-run lines; the integration gate)
- **Now:** "이 기간에 scoring spec pin은 … 같은 날 operation마다 가장 큰 run을 따로 싣는 rebuild(결정 17, 18) 뒤 `27d347bc…`와 `de9802e7…`가 되었습니다."
- **Becomes:** 끝에 더함: 2026-11-01에 cap band의 세 table pin이 생김(`floor-0.2` `58c1107e…`, `floor-0.333` `4fe86c3f…`, `floor-0.5` `9295b76e…`; 10.1). 2026-11-14의 통합 gate 항목이 driver table을 `f693bfbe…`, 세 table을 `6cbae471…`, `1020d6ab…`, `38f8de5e…`로 다시 pin하고(compile row의 LOTTERY 설명이 `struct Lottery`를 이름으로 인용, 값은 그대로) `simulator@0d323c84470a`와 `daemon@62c71f0d2de0`의 version pin을 더함(10.2). 그 뒤 RQ0 gate spec의 pin은 움직이지 않음(2026-11-21의 두 번째 bless에서도).
- **From:** `harness/CHANGELOG.md`, 2026-11-01 entry, "Pins"; 2026-11-14 entry "the integration gate passed", "Driver tables" and "Pins"; 2026-11-21 re-measurement entry, opening paragraph; `harness/experiments/rq0-gate.yaml`, lines 654–668

### g1-12 · `docs/guidebook/dataset/07-build-gate-manifests-ci-tests.md:667` · B · item 10 (the second bless)
- **Now:** "| set | 9.19 (2026-10-11) | … | Phase 10 (2026-10-31) | Phase 10, 결정 17·18 (2026-10-31, 현재) |" — its last column `eee6a020…`, `b593144c…`, `e3a94dc8…`, `07d59e41…`, `2b99f65e…`
- **Becomes:** 열 더함 "11.3, 두 번째 bless (2026-11-21, 현재)": transition grid `d6ded38a…`, return grid `2189c0d2…`, flap-stress `879fd4d8…`, distractor grid `6091e382…`, familiarity ladder `b465bfbe…`. 앞 열에서 "현재"를 뺌.
- **From:** the committed `dataset/build.<set>.manifest.json` of each set, SHA-256 at `2e3fade3` (above); at `2e3fade3~1` the five values the column now labelled 현재 holds
- **Flags:** for 인지오: no record but the committed manifests holds the five new hashes (the 2026-11-21 changelog entry and `bless-report.json` list none; grep over `_dev/`, `docs/`, `harness/` finds none) — whether a committed manifest counts as the row's named record under spec decision 11.

### g1-13 · `docs/guidebook/dataset/07-build-gate-manifests-ci-tests.md:675` · B · item 10 (the second bless)
- **Now:** "… 2026-10-31의 rebuild에서는 측정된 프로그램 자신의 wake가 … `wlc/linter.py`의 줄이 움직였습니다. 2026-10-31에 일곱 manifest의 SHA-256을 계산하면 표의 "현재" 열 및 RQ0 pin과 모두 같습니다."
- **Becomes:** 더함: 2026-11-21의 두 번째 bless에서는 다섯 set의 모든 generated artifact가 library hash에서 움직였고, `python3`를 품은 파일은 그 밖에서도 움직임(transition grid 480개 중 49, return grid 720개 중 70, distractor grid 272개 중 22, familiarity ladder 66개 중 5, flap-stress 24개 중 0). `inputs`에서는 library 줄만 움직이고 `grid`, `demand`, `reports`는 그대로. 마지막 문장: 2026-11-21에 일곱 manifest의 SHA-256은 표의 새 "현재" 열과 같고, RQ0 gate spec의 dataset·variants pin은 첫 bless(결정 17·18 열)를 가리킴.
- **From:** `harness/CHANGELOG.md`, 2026-11-21 re-measurement entry, "The second bless" (the counts); `bless-report.json`, the `beyond_hash` lists and empty `demand_moves`; the committed generated manifests at `2e3fade3` against `2e3fade3~1` (every artifact hash moved; `inputs` only `dataset/archetypes.yaml`; `grid`, `demand`, `reports` equal), read 2026-11-21
- **Flags:** for 인지오: "every generated artifact moved by the library hash" and "inputs, the library line alone" are read off the two committed manifests, not stated in a record.

### g1-14 · `docs/guidebook/dataset/07-build-gate-manifests-ci-tests.md:846` · A · item 12 (the experiment lint's notes)
- **Now:** (846) "고치는 법: 두 manifest를 commit하고(re-bless), RQ0 gate spec의 두 pin을 다시 적고 harness changelog에 항목을 남깁니다(3.4)." (863) "… 그리고 re-pin합니다."
- **Becomes:** 두 줄 모두: 실행 전의 실험 사양이면 re-pin하고 changelog 항목을 남김. 실행된 RQ0 gate spec은 다시 pin하지 않음(그 pin은 run이 읽은 tree, lint가 note로 읽음).
- **From:** `harness/CHANGELOG.md`, 2026-11-20 entry; 2026-11-21 re-measurement entry, opening paragraph

### g1-15 · `docs/guidebook/dataset/07-build-gate-manifests-ci-tests.md:848` · A · item 12 (the experiment lint's notes)
- **Now:** "사례 1에서 manifest만 commit하고 `rq0-gate.yaml`은 그대로 두었다고 합시다. … `make -C harness lint`가 실패합니다. 3.5의 모양 그대로 `pins/dataset: sha256 … != pinned 8e1eb753…`와 `pins/variants/all: …` 두 줄이 나오고 `2 error(s)`로 끝납니다. … `harness.yml`이 `make -C harness lint` 단계에서 빨갛게 됩니다."
- **Becomes:** `rq0-gate.yaml`은 실행된 spec이라(옆에 `experiments/rq0-gate/runs.sha256.csv`) 두 줄이 `note: … — the pin names the tree the run read`로 나오고 `lint clean`; harness lint는 실패하지 않음(2026-11-21의 두 번째 bless 뒤 실제 출력). 이 사례의 실패는 run record가 없는 spec에서 일어남.
- **From:** `harness/CHANGELOG.md`, 2026-11-20 entry, "Experiment lint" and "Tests" ("a moved dataset pin is an error without the run record, a note with it"); `harness/tools/experiment_lint.py`; the experiment lint, 2026-11-21
- **Flags:** D inside the passage: the pinned value in the example, `8e1eb753…`, predates the 2026-10-31 re-pin (outside the fifteen items).

### g1-16 · `docs/guidebook/dataset/07-build-gate-manifests-ci-tests.md:1084` · A · items 2, 5, 12, 13 (the integration gate; the runner and results cache; the experiment lint's notes; the configuration search)
- **Now:** "harness 쪽 Makefile도 dataset을 읽는 target을 가집니다. 18줄입니다." — the block (lint, test, test-full, smoke; lint's comment ending "every experiment spec against schema, coreset, pins") and "`lint`의 `experiment_lint.py`는 3.5에서 본 pin 검사를 합니다."
- **Becomes:** 27줄. block을 지금 파일대로: `lint` 주석 끝에 "(an executed spec's pins as notes)"(2026-11-20), `test-quick`(`-m "not slow and not coreset_wide"`, 2026-11-14), `gate`와 `gate-status`(통합 gate, `tools/integration_gate.py --machine runner.yaml`, 2026-11-14), `.PHONY`도. experiment_lint 줄: 실행된 spec의 pin은 note, search spec(`rq0-config-search.yaml`)은 search의 lint로 봄; 2026-11-21의 출력은 search spec 줄과 RQ0 gate spec 줄(둘 다 "executed"), note 둘, `lint clean`. `smoke` 줄(mock으로)은 Makefile과 맞음.
- **From:** `harness/Makefile` (27 lines; commits `b1b08b07`, `cde59541` on 2026-11-14, `8718bf23` on 2026-11-20); `harness/CHANGELOG.md`, 2026-11-14 entry "the integration gate passed" ("`make gate`, `make gate-status`"), 2026-11-14 entry "the runner: runs at once and a results cache; the suite's quick tier" ("`make test-quick`"), 2026-11-20 entry ("Commands, `Makefile`: the `lint` target's help line"); the experiment lint, 2026-11-21

### g1-17 · `docs/guidebook/dataset/07-build-gate-manifests-ci-tests.md:1118` · A · items 10, 12 (the second bless; the experiment lint's notes)
- **Now:** "| timeline, variant recipe, … | `make lint dataset variants generated test check` | … | RQ0 gate spec의 `dataset`·`variants` pin, `harness/CHANGELOG.md` 항목, `make -C harness lint` |" and "| `variants.yaml` | `make variants check` | … | `variants` pin, changelog |"
- **Becomes:** "그 다음" 열: 실행 전의 실험 사양의 pin과 changelog 항목, `make -C harness lint`. 실행된 RQ0 gate spec과 configuration search spec은 다시 pin하지 않음(lint가 note로 읽음) — 2026-11-21의 두 번째 bless가 그렇게 함.
- **From:** `harness/CHANGELOG.md`, 2026-11-20 entry; 2026-11-21 re-measurement entry, opening paragraph; 2026-11-21 configuration search entry, "Experiment lint"

### g1-18 · `docs/guidebook/dataset/07-build-gate-manifests-ci-tests.md:1251` · A · item 10 (the second bless)
- **Now:** "**39030123144** — … 커밋 `17f28d7f`를 손으로 돌린 run이고, 지금의 manifest 일곱 개(3.7의 "현재" 열), 파생 timeline, coverage grid가 Linux에서 바이트 단위로 재현되었습니다."
- **Becomes:** "지금의" → "그때의"(9.16의 판). 지금의 manifest는 2026-11-21 두 번째 bless(커밋 `2e3fade3`)의 것.
- **From:** `git log -1 -- dataset/build*.manifest.json` (all seven `2e3fade3`, 2026-11-21); `harness/CHANGELOG.md`, 2026-11-21 re-measurement entry, "The second bless"
- **Flags:** D inside the passage: the two 2026-10-31 blesses had already moved "지금" (outside the fifteen items). For 인지오: no record names a Linux CI run on the 2026-10-31 or 2026-11-21 manifests; whether one ran is a `gh run list` question.

### g1-19 · `docs/guidebook/dataset/07-build-gate-manifests-ci-tests.md:1330` · A · item 10 (the second bless)
- **Now:** "9.16의 rebuild가 쓴 지금의 manifest(커밋 `17f28d7f`, 3.7의 "현재" 열)는 dataset run 39030123144(약 17분)가 초록으로 통과했습니다"
- **Becomes:** "그때의 manifest"; 2026-10-31의 두 bless와 2026-11-21의 두 번째 bless가 쓴 manifest를 Linux에서 재현한 run은 기록에 없음.
- **From:** as g1-18
- **Flags:** as g1-18.

### g1-20 · `docs/guidebook/dataset/07-build-gate-manifests-ci-tests.md:1493` · B · items 2, 5, 12, 13 (the integration gate; the runner and cold smoke; the experiment lint's notes; the configuration search)
- **Now:** "| `test_runner.py`의 pipeline test (`@needs_build` 5곳) | mock daemon과 mock simulator로 runner 전체를 compiled 파일 위에서 돌림 |" … "| `make -C harness lint`의 `experiment_lint.py` | 3.5의 pin 검사 |"
- **Becomes:** 행 더함: "| `test_search.py` (`@needs_build` 2곳) | committed search spec이 compiled core set과 scoring 항에 대해 lint를 통과하고 그 point들을 가짐, lint가 틀린 개수와 빠진 boot default를 거부 |". `test_runner.py`: `@needs_build` 9곳(통합 gate, runner와 results cache, cold smoke 전의 records 경로, cap band run의 table 이름표가 더함), 여전히 `runner.example.yaml`의 mock으로, 작은 세 파일(`c1-office`, `c1-photo`, `c7-mail`) 위에서. experiment_lint 행: 3.5의 pin 검사, 실행된 spec의 pin은 note, search spec은 search의 lint(파일을 compiled build에 대조).
- **From:** `harness/tools/tests/test_search.py`, lines 18, 66–82; `harness/tools/tests/test_runner.py` (`grep -c "^@needs_build"` = 9; 5 at `b5c38398`, 6 at `b1b08b07`, 8 at `cde59541` and `cabebef5`, 9 at `df0b9348`), `_machine` (lines 32–38) over `harness/runner.example.yaml`; `harness/tools/tests/README.md` ("The pipeline tests run on three small files"); `harness/CHANGELOG.md`, 2026-11-21 configuration search entry, "Tests" and "Experiment lint"; the four 2026-11-14 entries' "Tests" lines
- **Flags:** for 인지오: code and record disagree — the 2026-11-14 entry "the rows' table column takes a cap-band run's label" says its test runs "on `c7-mail` through the real programs to the report", but `test_a_cap_band_run_goes_through_to_the_report_with_its_label_in_every_row` builds its machine from `harness/runner.example.yaml`, which drives the two mocks. Also one A within: the count "5곳".

### g1-21 · `docs/guidebook/dataset/07-build-gate-manifests-ci-tests.md:1735` · A · items 10, 12 (the second bless; the experiment lint's notes)
- **Now:** "`re-pin` — dataset이 다시 bless되어 manifest hash가 바뀌었을 때 RQ0 gate spec의 pin을 새 값으로 고치고 harness changelog에 항목을 남기는 것. (3.4)"
- **Becomes:** "… 실행 전의 실험 사양의 pin을 새 값으로 고치고 … . 실행된 spec(옆에 run record가 commit된 spec)은 다시 pin하지 않고, experiment lint가 맞지 않는 pin을 note로 읽음."
- **From:** `harness/CHANGELOG.md`, 2026-11-20 entry; 2026-11-21 re-measurement entry, opening paragraph

### g1-22 · `docs/guidebook/dataset/07-build-gate-manifests-ci-tests.md:1744` · A · item 2 (the integration gate)
- **Now:** "`mock daemon` / `mock simulator` — 진짜 daemon과 simulator가 호출 계약(`docs/data-contracts.md` §11)으로 돌기 전까지 그 계약으로 대신 도는 harness의 test용 program. daemon program은 아직 저장소에 없고, reference simulator(`simulator/src/sim.cpp`)는 두 입력을 위치 인자로 받아 trace를 표준 출력에 씁니다. Phase 10(통합과 RQ0 run)이 진짜 program으로 바꿉니다. (6.10)"
- **Becomes:** 호출 계약(§11)으로 도는 harness의 test용 program; `make -C harness smoke`와 runner의 test가 부름(`runner.example.yaml`). 진짜 daemon(`daemon/daemon.py`)과 reference simulator(`simulator/src/sim`, `--workload`/`--schedule`/`--out-trace`, 위치 인자 없음)는 2026-11-14에 통합 gate를 통과했고(`simulator@0d323c84470a`, `daemon@62c71f0d2de0`), RQ0 run(2026-11-16–18)이 이 둘로 돌았음.
- **From:** `harness/CHANGELOG.md`, 2026-11-14 entry "the integration gate passed", first paragraph; `harness/runner.example.yaml`, lines 1–17; `simulator/src/sim.cpp`, lines 1489–1519 (the flags and usage); `daemon/README.md`, "`daemon.py` — the running skeleton"; `docs/rq0-run-record.md`, "The run" (programs, started, finished)

### g1-23 · `docs/guidebook/dataset/07-build-gate-manifests-ci-tests.md:1149` · D · —
- **Now:** "on:\n  push:\n    branches: [main]\n  pull_request:" (the quoted `dataset.yml`; also the 6.2 table's trigger cells and 6.5's "push에는 `main` branch에서만 반응")
- **Why left:** since 2026-10-31 (`b24f8c89`) `dataset.yml`, `harness.yml` and `daemon.yml` skip a push changing only `.github/campaign.json` (`paths-ignore`); widened 2026-11-20 (`f3cc77b3`) to `.github/campaign-background.json` for 11.3's campaign. The first change is outside the fifteen items; the second serves item 10's campaign but changes CI, not a statement item 10 makes.

### g1-24 · `docs/guidebook/dataset/07-build-gate-manifests-ci-tests.md:611` · D · —
- **Now:** "이 함수는 두 곳에서 불립니다."
- **Why left:** `_pin_errors` is also reached through `lint_spec`, which the runner calls before a run (`harness/tools/harness/runner.py`, lines 865, 908) and `harness/tools/lint.py` calls (line 110); the runner's pre-run pin check predates the fifteen items (`harness/CHANGELOG.md`, 2026-11-20: "checks every pin before a run as before").

## Chapter 1 — the big picture

### g1-25 · `docs/guidebook/dataset/01-the-big-picture.md:144` · A · items 10, 12 (the second bless; the experiment lint's notes)
- **Now:** "**pin**: spec은 데이터셋을 SHA-256으로 못 박습니다. `pins.dataset`은 `dataset/build.manifest.json`의 hash `8e1eb753…`이고, `pins.variants.all`은 `dataset/build.variants.manifest.json`의 hash `8e2948b1…`입니다(출구 감사 9.16의 2026-10-17 re-pin, …). 2026-10-17에 두 파일의 hash를 계산해 보았고, 둘 다 pin과 같았습니다."
- **Becomes:** `pins.dataset`은 `27d347bc…`, `pins.variants.all`은 `de9802e7…`(2026-10-31 "each measured operation's largest run" 항목의 re-pin), RQ0 run이 읽은 첫 bless. 2026-11-21의 두 번째 bless 뒤 지금의 두 파일은 `9f30ea8f…`, `3438be7f…`라 pin과 다르고, RQ0 gate spec은 실행된 spec이라 다시 pin하지 않음 — experiment lint가 둘을 note로 읽음. 지금의 core manifest는 configuration search spec이 pin.
- **From:** `harness/experiments/rq0-gate.yaml`, lines 663, 665; `harness/CHANGELOG.md`, 2026-10-31 entry "each measured operation's largest run", "Pins"; 2026-11-21 re-measurement entry, opening paragraph; 2026-11-20 entry; `harness/experiments/rq0-config-search.yaml`, line 259; the committed manifests and the experiment lint, 2026-11-21
- **Flags:** for 인지오: the pin values themselves moved on 2026-10-31, outside the fifteen items (D); the item-10/12 statement cannot be written without them.

### g1-26 · `docs/guidebook/dataset/01-the-big-picture.md:508` · E · item 10 (the re-measurement)
- **Now:** "| compile과 batch | `cpu-batch`, `compiler-child`, `build-orchestrator` | 9.6(compile). `cpu-batch`의 두 program(`python3`, `kdenlive_render`)은 9.10의 campaign |" (table introduced "2026-10-14 현재의 29개를 …")
- **Becomes:** (if read as current) "… `python3`의 voluntary block 사이의 run과 run마다의 block은 11.3의 campaign `meas-ci:background:2026-11-20`(107 repeat, 2026-11-21)".
- **From:** `harness/CHANGELOG.md`, 2026-11-21 re-measurement entry, "The campaign" and "The fold-in"; `dataset/archetypes.yaml`, `cpu-batch`'s scope (line 1269: both campaigns)
- **Flags:** for 인지오: cannot decide — the table is explicitly dated 2026-10-14, so by the brief's rule it is not overtaken; left, or one clause added.

### g1-27 · `docs/guidebook/dataset/01-the-big-picture.md:672` · A · item 10 (the second bless)
- **Now:** "`sampled`는 `{"seed": 107, "archetypes": "archetypes.yaml@aa2f8842…"}`가 됩니다. … 같은 날 operation마다 측정한 조작별 가장 큰 run을 따로 싣는 재빌드(timer-wakes-by-origin spec 결정 17, 18)가 지금의 `@aa2f8842…`로 바꾸었습니다(2026-10-31에 `git hash-object`로 확인)."
- **Becomes:** `sampled`의 library 값은 `archetypes.yaml@a25178d1…`. 끝에 더함: 2026-11-21의 두 번째 bless(11.3, `cpu-batch`의 `python3` 두 값을 107 repeat로 다시 잰 fold-in)가 지금의 `@a25178d1…`로 바꿈; `@aa2f8842…`는 그 전 판.
- **From:** `bless-report.json`, `library_blob` (head `aa2f8842…`, working_tree `a25178d1…`); `git rev-parse HEAD:dataset/archetypes.yaml` = `a25178d113f0…`; `harness/CHANGELOG.md`, 2026-11-21 re-measurement entry, "The fold-in"

### g1-28 · `docs/guidebook/dataset/01-the-big-picture.md:686` · A · item 10 (the second bless)
- **Now:** "`build.manifest.json`에 이 파일의 hash(`9b657fb1…`), report의 hash(`42b34a07…`), 그리고 수요 기록(`calibration`, utilization 0.3319)을 적습니다. 2026-10-31에 디스크의 `c1-dev.workload.json`을 `shasum -a 256`으로 계산해 보았고, manifest의 값과 같았습니다."
- **Becomes:** 파일의 hash는 `fe5c4407…`(두 번째 bless 뒤; `meta.sampled`의 library hash만 바뀜, `c1-dev`는 `python3`를 품지 않음). report hash `42b34a07…`와 수요는 그대로; 크기 864,736 byte도 그대로. 확인 날짜를 그에 맞춤.
- **From:** the committed core manifest, `artifacts["coreset-single/c1-dev.workload.json"]`, `fe5c4407…` at `2e3fade3` against `9b657fb1…` at `2e3fade3~1`, `reports` and `demand` equal; `bless-report.json`, `manifests."build.manifest.json".beyond_hash` (three files, `c1-dev` not among them); `ls -l dataset/build/coreset-single/c1-dev.workload.json`, 2026-11-21

### g1-29 · `docs/guidebook/dataset/01-the-big-picture.md:724` · A · item 10 (the second bless)
- **Now:** "> **마지막 bless의 runner 재현.** … 9.16의 판(커밋 `17f28d7f`)은 dataset run 39030123144(2026-10-17, 약 17분)가 `lint`부터 `check`까지 초록이었습니다. …"
- **Becomes:** 마지막 bless는 2026-11-21의 두 번째 bless(11.3; core manifest `9f30ea8f…`, 커밋 `2e3fade3`), 그 전에 2026-10-31의 두 bless. 9.16의 판까지의 재현은 그대로 두고, 그 뒤 세 bless를 runner에서 재현한 run은 기록에 없음.
- **From:** `harness/CHANGELOG.md`, 2026-11-21 re-measurement entry, "The second bless"; the committed core manifest; `git log -1 -- dataset/build*.manifest.json`
- **Flags:** D inside the passage: the 2026-10-31 blesses (outside the fifteen items). For 인지오: a correction naming a runner run on `2e3fade3` needs a fact no record holds (`gh run list`).

### g1-30 · `docs/guidebook/dataset/01-the-big-picture.md:771` · A · items 10, 12 (the second bless; the experiment lint's notes)
- **Now:** "이 파일은 모든 manifest의 입력이라 주석 한 줄을 고쳐도 일곱 manifest가 다시 bless되고 RQ0 gate spec이 다시 pin됩니다. 두 재빌드 모두 그랬습니다."
- **Becomes:** "… 일곱 manifest가 다시 bless됩니다. 실행 전의 실험 사양은 다시 pin되고(두 재빌드 모두 그랬습니다), 실행된 RQ0 gate spec은 다시 pin되지 않습니다 — 2026-11-21의 두 번째 bless에서 그 pin은 run이 읽은 첫 bless에 남고 experiment lint가 note로 읽었습니다."
- **From:** `harness/CHANGELOG.md`, 2026-11-21 re-measurement entry, opening paragraph; 2026-11-20 entry

### g1-31 · `docs/guidebook/dataset/01-the-big-picture.md:904` · A · items 10, 12 (the second bless; the experiment lint's notes)
- **Now:** "core manifest가 바뀌면 variants manifest의 `inputs`가 바뀌고, 둘 다 RQ0 gate spec이 hash로 고정하므로 spec의 pin도 다시 맞춰야 합니다(harness의 changelog 항목과 함께)"
- **Becomes:** "… 그것을 hash로 고정한 실험 사양이 실행 전이면 pin도 다시 맞춤(changelog 항목과 함께). 실행된 RQ0 gate spec은 다시 맞추지 않고 experiment lint가 note로 읽음(2026-11-21의 두 번째 bless)."
- **From:** `harness/CHANGELOG.md`, 2026-11-20 entry; 2026-11-21 re-measurement entry, opening paragraph

### g1-32 · `docs/guidebook/dataset/01-the-big-picture.md:1087` · B · item 10 (the second bless)
- **Now:** "## 5.9 데이터셋이 지금 모양이 되기까지" … last row "| 2026-10-17 – 18 | 9.16 출구 감사, Phase 9 끝 | … 한 번의 재빌드(core manifest `8e1eb753…`), 최종 build의 전체 smoke exit 0 |"
- **Becomes:** 행 더함: "| 2026-11-21 | 11.3 재측정과 두 번째 bless | `cpu-batch`의 `python3` 두 값(voluntary block 사이의 run, run마다의 block)을 campaign `meas-ci:background:2026-11-20`의 107 repeat로 다시 잼, core set·variant 78개·generated 다섯 set을 다시 bless(core manifest `9f30ea8f…`), library hash 너머로는 `python3`를 품은 파일만 바뀌고 demand는 그대로 |"
- **From:** `harness/CHANGELOG.md`, 2026-11-21 re-measurement entry; `docs/rq0-run-record.md`, "Corrections", 2026-11-21 (line 182); the committed core manifest
- **Flags:** D inside the passage: the two 2026-10-31 rebuilds (a measured program's own wakes by origin; each operation's largest run) are also absent — outside the fifteen items.

### g1-33 · `docs/guidebook/dataset/01-the-big-picture.md:1214` · C · items 2, 6 (the integration gate; the RQ0 run)
- **Now:** "> **열린 자리.** 출구 감사는 compile된 숫자의 문장 가운데 simulator가 아직 보이지 않은 동작에 기대는 것들을 … 이 목록은 각 항목이 simulator에 들어올 때 인경민이 돌릴 확인이고(9.16 spec 결정 6), 그때까지 이 문장들은 확인되지 않은 채 열려 있습니다. … (h)는 (g)와 함께 simulator 담당이 아직 갚을 항목이며, 항목마다 보여지기 전에는 RQ0 run이 시작되지 않습니다(…)."
- **Becomes:** 상자는 남기고 좁힘. 상자 밖의 문장으로: 2026-11-14에 통합 gate가 `simulator@0d323c84470a`에서 통과해 conformance 항목 (a)–(j)가 binary 위에 보여졌음(손으로 쓴 fixture의 재생 (a), (b), (c), (g), (i), (j); black-box unit test (d), (e), (f), (g), (i), (h)), RQ0 run은 그 program으로 2026-11-16–18에 돌았음. 상자에 남는 것: (b), (d), (e), (g)에 기대는 compile된 숫자 문장의 확인(9.16 `compiled/uncheckable-by-item.md`) — 했다는 기록이 없고, `simulator/memo/memo_261021.md`의 행 M이 (d)의 확인을 인경민이 갚을 항목으로 적음.
- **From:** `harness/CHANGELOG.md`, 2026-11-14 entry "the integration gate passed", first paragraph and "RQ0 gate spec" line; `docs/rq0-run-record.md`, "The run" (programs, started, finished); `simulator/memo/memo_261021.md`, line 52 (row M); no later record names the per-item checks done (grep for `uncheckable` over the tree)
- **Flags:** for 인지오: whether showing (b), (d), (e), (g) on the binary also discharges the per-statement checks 9.16 spec decision 6 assigned — read here as not.

### g1-34 · `docs/guidebook/dataset/01-the-big-picture.md:1345` · B · item 13 (the configuration search)
- **Now:** "**manifest.** harness는 manifest도 읽습니다. RQ0 gate spec은 core manifest와 variants manifest를 hash로 고정하고(7.5), 앞으로의 experiment spec은 generated manifest의 `grid` 축 … `pins.generated`로 고정할 수 있습니다"
- **Becomes:** 더함: configuration search spec(`harness/experiments/rq0-config-search.yaml`)은 두 번째 bless의 core manifest(`9f30ea8f…`)를 고정하고, search 도구(`harness/tools/search.py`)의 lint가 그 열 파일을 compiled core set과 scoring 항에 대조함.
- **From:** `harness/experiments/rq0-config-search.yaml`, lines 254–264; `harness/CHANGELOG.md`, 2026-11-21 configuration search entry, "Search spec" and "Search tool"

### g1-35 · `docs/guidebook/dataset/01-the-big-picture.md:1351` · A · items 1, 2 (the pre-run lines; the integration gate)
- **Now:** "RQ0 gate spec(`harness/experiments/rq0-gate.yaml`)의 `pins`는 다섯 파일을 SHA-256으로 고정합니다. 채점 spec, guard spec, prior driver table, 그리고 데이터셋의 두 manifest입니다."
- **Becomes:** 여덟 파일을 SHA-256으로(위 다섯에 cap band의 세 table `prior-floor-0.2.yaml`, `prior-floor-0.333.yaml`, `prior-floor-0.5.yaml`, 2026-11-01), 그리고 두 program의 version(`simulator@0d323c84470a`, `daemon@62c71f0d2de0`, 2026-11-14; runner가 다른 version을 run 전에 거부)을 고정.
- **From:** `harness/experiments/rq0-gate.yaml`, lines 654–668; `harness/CHANGELOG.md`, 2026-11-01 entry, "Evaluator, runner and the spec schema" and "Pins"; 2026-11-14 entry "the integration gate passed", "Spec schema, runner and evaluator" and "Pins"

### g1-36 · `docs/guidebook/dataset/01-the-big-picture.md:1353` · A · items 10, 12, 13 (the second bless; the experiment lint's notes; the configuration search)
- **Now:** "… 데이터셋을 바꾼 사람은 manifest를 다시 commit하고(re-bless), harness changelog에 항목을 쓰고, spec의 pin을 다시 맞춰야(re-pin) 합니다. … 출구 감사 9.16의 재빌드(2026-10-17)가 남긴 `8e1eb753…`이 지금의 값입니다(…)."
- **Becomes:** re-pin은 실행 전의 spec에서. 값의 줄: 9.16의 `8e1eb753…` 뒤 2026-10-31에 `d80f06e0…`, 그다음 `27d347bc…` — 이것이 RQ0 gate spec의 지금 값이고 RQ0 run이 읽은 첫 bless. 2026-11-21의 두 번째 bless는 core manifest를 `9f30ea8f…`로 바꿨지만 실행된 RQ0 gate spec은 다시 pin하지 않았고(experiment lint가 note로 읽음), 그 값은 configuration search spec이 pin.
- **From:** `harness/CHANGELOG.md`, the two 2026-10-31 entries' "Pins"; `harness/experiments/rq0-gate.yaml`, line 663; 2026-11-21 re-measurement entry, opening paragraph; 2026-11-20 entry; `harness/experiments/rq0-config-search.yaml`, line 259
- **Flags:** for 인지오: the two 2026-10-31 values lie outside the fifteen items (D), but "지금의 값" cannot be corrected without them.

### g1-37 · `docs/guidebook/dataset/01-the-big-picture.md:1362` · A · item 12 (the experiment lint's notes)
- **Now:** "→ rq0-gate.yaml pins.dataset / pins.variants 불일치 / → harness/CHANGELOG.md 항목 + re-pin"
- **Becomes:** 마지막 두 단계: 실행 전의 spec이면 pin 불일치(오류) → changelog 항목 + re-pin; 실행된 spec(RQ0 gate spec)이면 experiment lint의 note, pin은 run이 읽은 tree로 남음.
- **From:** `harness/CHANGELOG.md`, 2026-11-20 entry; `harness/tools/experiment_lint.py`, docstring

### g1-38 · `docs/guidebook/dataset/01-the-big-picture.md:1437` · A · item 12 (the experiment lint's notes)
- **Now:** "**이럴 때 펴세요**: … RQ0 gate spec의 pin을 다시 맞춰야 할 때."
- **Becomes:** "실험 사양의 pin을 다시 맞춰야 할 때(실행된 RQ0 gate spec은 다시 맞추지 않음)."
- **From:** `harness/CHANGELOG.md`, 2026-11-20 entry

### g1-39 · `docs/guidebook/dataset/01-the-big-picture.md:1454` · A · items 6, 15 (the RQ0 run; Phase 12 next)
- **Now:** "| RQ0 문지기 실험의 실행 전에 데이터셋 쪽 준비를 점검하기 | 4권(판정 파일, variant) → 7권(pin, gate) → 8권(열린 자리) |"
- **Becomes:** RQ0 run은 2026-11-16–18에 돌았음; 행은 "두 번째 RQ0 run(Phase 12) 전에 데이터셋 쪽 준비를 점검하기".
- **From:** `docs/rq0-run-record.md`, "The run" (started, finished); `_dev/docs/spec/jioh/phase-11-rq0-failure-procedure-diagnosis.md`, decision 1
- **Flags:** for 인지오: the row names a task, not a state — it may stand as is.

### g1-40 · `docs/guidebook/dataset/01-the-big-picture.md:1462` · B · item 10 (the re-measurement and second bless)
- **Now:** "**Phase N** — `_dev/TODO.md`의 인지오 절에 있는 작업 단계 번호입니다. 데이터셋과 직접 관련된 것은 Phase 1(기초), 2(첫 생성), 3(검증과 동결), 7(attribute coverage), 9(재구축)입니다."
- **Becomes:** Phase 11(RQ0 실패 절차: 진단 — sub-task 11.3이 `cpu-batch`의 `python3`를 다시 재어 두 번째 bless를 함)을 더함.
- **From:** `harness/CHANGELOG.md`, 2026-11-21 re-measurement entry (decided under `_dev/docs/spec/jioh/task-11.3-the-re-measurement.md`); `docs/rq0-run-record.md`, "Corrections", 2026-11-21 ("sub-task 11.3")
- **Flags:** D inside the passage: Phase 10 (통합과 RQ0 run) also rebuilt the dataset twice on 2026-10-31 — chapter 7's 3.7 calls it a "Phase 10 항목" — outside the fifteen items.
