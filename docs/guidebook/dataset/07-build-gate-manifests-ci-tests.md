# 7권 · Build gate, manifest, CI, tests: 같은 바이트를 보장하는 장치

> Status: draft · Created 2026-10-14 · Updated 2026-10-14

**아무도 commit하지 않는 `build/`가 어떻게 모두에게 같은 파일임이 보장되고, 무엇이 그것을 지키나.**

---

이 시리즈의 앞 권들은 workload dataset이 무엇으로 이루어져 있는지를 다룹니다. 사람이 쓰는 `timeline` 파일(시간축 위에 segment, task, focus를 적은 YAML), 측정으로 채운 behaviour library인 `archetypes.yaml`, 그리고 이 둘을 받아 simulator가 읽는 JSON으로 바꾸는 compiler `wlc`가 그것입니다. compiler가 내놓는 결과물은 `dataset/build/` 아래에 쌓입니다. core set 51개, 그 위의 sensitivity variant 78개, generated layer 1,562개가 모두 이 디렉터리에 들어갑니다. 2026-10-14 현재 이 디렉터리는 6.8 GB입니다.

그런데 이 6.8 GB는 git에 하나도 들어 있지 않습니다. `.gitignore`의 첫 두 항목이 `dataset/build/`와 `dataset/generated/`입니다. 실험은 이 파일들 위에서 돌아가고, 실험의 신뢰성은 "모든 조건이 바이트 하나 다르지 않은 같은 workload를 본다"는 데 걸려 있습니다. 그렇다면 commit되지 않은 파일이 집의 M1 Pro에서 만든 것과 GitHub runner에서 만든 것이 같다는 것을 누가, 어떻게 보장할까요. 이 권은 그 질문에 답합니다.

답은 네 가지 장치로 이루어져 있습니다. 첫째, `manifest`라는 committed lockfile 일곱 개가 build의 입력과 출력을 hash로 고정합니다. 둘째, `make check`라는 gate가 방금 만든 build를 committed manifest와 바이트 단위로 비교합니다. 셋째, GitHub Actions의 CI가 깨끗한 Linux 기계에서 처음부터 다시 build하고 같은 비교를 합니다. 넷째, dataset과 harness의 test suite가 compiler의 불변식과 build의 모양을 확인합니다. 그리고 이 manifest들의 hash를 다시 실험 쪽의 사전 등록 파일이 `pin`으로 붙잡습니다. 이 권은 이 사슬을 입력 파일 하나에서 실험 사양의 hash 한 줄까지 따라갑니다.

이 권은 compiler의 내부(무엇을 어떻게 sampling하는지), core set의 설계, generated layer의 grid 설계, sensitivity variant의 의미, 측정 campaign 자체는 다루지 않습니다. 그것들은 각각 compiler 권, coreset 권, generated layer 권, variants 권, 측정 campaign 권에서 다룹니다. 여기서는 그것들이 만든 바이트가 어떻게 고정되고 검증되는지만 봅니다.

---

## 목차

1. [1장 · 왜 같은 바이트가 필요한가](#1장--왜-같은-바이트가-필요한가)
2. [2장 · Manifest 일곱 개의 해부](#2장--manifest-일곱-개의-해부)
3. [3장 · Bless와 pin: 누가 무엇을 고정하나](#3장--bless와-pin-누가-무엇을-고정하나)
4. [4장 · Gate: `make check`와 네 개의 `--check`](#4장--gate-make-check와-네-개의---check)
5. [5장 · `make` target의 순서, 시간, 병렬화](#5장--make-target의-순서-시간-병렬화)
6. [6장 · CI: GitHub runner 위의 dataset](#6장--ci-github-runner-위의-dataset)
7. [7장 · Test suite: dataset이 지키는 불변식](#7장--test-suite-dataset이-지키는-불변식)
8. [8장 · Rules of the tree: 각 규칙과 그 이유](#8장--rules-of-the-tree-각-규칙과-그-이유)
9. [9장 · 용어 정리](#9장--용어-정리)

---

# 1장 · 왜 같은 바이트가 필요한가

## 1.1 이 장의 질문

이 장은 두 가지를 묻습니다. 하나는 "왜 workload 파일은 바이트 단위로 같아야 하나"이고, 다른 하나는 "그렇게 중요한 파일을 왜 commit하지 않나"입니다. 두 질문은 서로 반대 방향을 가리키는 것처럼 보입니다. 중요한 파일이면 commit해서 고정하는 것이 자연스러워 보이기 때문입니다. 이 장은 두 질문이 사실 같은 답에서 나온다는 것을 보입니다. 파일이 입력에서 결정론적으로 만들어지기 때문에 바이트가 같을 수 있고, 같은 이유로 파일 자체를 commit할 필요가 없습니다.

먼저 용어 세 개를 정리합니다.

- `timeline` — 사람이 쓰는 workload 설계 파일입니다(`dataset/timelines/coreset/<id>.timeline.yaml`). 시간축 위에 segment(같은 상황이 이어지는 구간과 그 정답 label), task(어떤 이름의 process가 어떤 archetype으로 언제 도착하는지), focus(어느 창이 사용자의 focus를 가졌는지)를 적습니다.
- `artifact` — compiler가 timeline 하나에서 만든 canonical workload 파일입니다(`dataset/build/<set>-single/<id>.workload.json`). simulator와 harness가 읽는 것은 이 파일입니다.
- `wlc` — 이 저장소의 workload compiler입니다(`dataset/tools/wlc/`). timeline과 library를 받아 artifact를 씁니다.

## 1.2 실험에서 workload가 하는 일

이 프로젝트의 실험은 같은 workload 위에서 여러 `condition`을 비교합니다. condition은 "workload 하나를 받아 configuration schedule 하나를 내놓는 함수"입니다(`docs/terminology.md`의 정의). 예를 들어 첫 실험의 사전 등록 파일인 RQ0 gate spec(`harness/experiments/rq0-gate.yaml`)은 `conditions: [fixed, random, oracle]`를 적습니다. `fixed`는 처음부터 끝까지 한 configuration을 유지하는 조건이고, `random`은 인식 시점마다 configuration을 무작위로 고르는 조건이며, `oracle`은 workload 파일의 정답 label을 읽어 그 상황에 맞는 configuration을 고르는 조건입니다. RQ0는 프로젝트의 첫 연구 질문으로, "모델이 없는 상태에서, configuration 선택이 이 workload들에서 측정 가능한 차이를 만드는가"를 묻습니다(`docs/research-proposal.md`의 RQ0 문단). 즉 `random`과 `oracle`이 같은 파일 위에서 얼마나 다른 점수를 내는지가 첫 실험의 핵심 숫자입니다.

여기서 같은 파일이라는 말이 바이트 단위여야 하는 이유가 나옵니다. 두 condition의 점수 차이는 오직 configuration의 차이에서 와야 합니다. 만약 `random` 조건의 run이 본 workload와 `oracle` 조건의 run이 본 workload가 RUN 길이 하나, 키 입력 시각 하나라도 다르다면, 점수 차이에는 configuration의 효과와 workload sampling의 잡음이 섞입니다. 섞인 다음에는 둘을 분리할 방법이 없습니다. `dataset/README.md`의 첫 문단이 이 점을 직접 적습니다. "wlc resolves all randomness at compile time, so the simulator replays concrete values and two conditions always face byte-identical workloads." 같은 README의 Pipeline 절은 이것을 "That determinism is load-bearing (experiment hygiene)"이라고 부릅니다. 실험의 위생이라는 뜻입니다.

웹 개발의 비유로 말하면, 이것은 A/B test에서 두 그룹이 같은 traffic을 받아야 한다는 요구와 비슷합니다. 다만 여기서는 traffic을 통계적으로 맞추는 것이 아니라, 아예 같은 요청 log를 두 번 재생하는 쪽입니다. replay가 정확하려면 log가 바이트 단위로 같아야 합니다.

이 요구는 dataset에서 끝나지 않고 harness까지 이어집니다. harness의 runner는 simulator와 daemon을 부를 때 모든 호출을 두 번 실행하고 두 출력이 바이트 단위로 같아야 받아들입니다. 그리고 실행 결과를 cache에 넣는데, cache key에는 입력 파일들의 SHA-256이 들어갑니다(`harness/tools/harness/runner.py`의 `cache_key`). 입력 파일의 바이트가 같으면 같은 key가 되어 다시 실행하지 않고, 바이트가 하나라도 다르면 다른 key가 됩니다. 2026-09-06의 Phase 3 기록은 이 성질을 이렇게 적습니다. "a label correction must not change what the simulator runs, and the harness cache keyed on the run-file hash gets that for free" (`_dev/archive/2026-09-06-phase-3-verification-and-protocol-freeze.md`). 여기서 `run file`은 simulator가 실제로 읽는, artifact에서 `events`만 남긴 view입니다.

## 1.3 Compile time이 모든 randomness를 푼다

workload에는 무작위가 많습니다. 여기서 `wake`는 기다리던 task가 다시 실행 가능해지는 사건이고, `RUN`은 task가 CPU를 정해진 시간만큼 쓰는 program 명령입니다. 편집기의 timer wake 간격, 각 RUN의 길이, replay할 키 입력 stream의 시작 offset, build의 각 object job이 쓰는 CPU 시간이 모두 측정된 분포에서 뽑힙니다. 이 무작위를 언제 푸느냐가 결정론의 출발점입니다.

2026-08-26의 workload-generation grill은 이 원칙을 D12로 못 박았습니다. 원문은 이렇습니다. "*compile time resolves all randomness; run time resolves all timing that scheduling can influence.*" (`_dev/archive/2026-08-26-workload-generation-grill.md`). compile time에 모든 무작위를 구체적인 숫자로 바꿔 파일에 적고, simulator는 무작위를 전혀 쓰지 않습니다. 같은 grill의 D11은 "Simulator stays 100% RNG-free"라고 적습니다. scheduling이 영향을 주는 시각(예를 들어 어떤 task가 실제로 언제 CPU를 받는지)만 run time에 정해집니다.

> **왜 이렇게 정했나.** 2026-08-26 grill의 D11은 build의 child process를 compile time에 펼쳐 도착 시각까지 고정하는 안을 버렸습니다. 기록된 이유는 "pins cc1 arrivals, so a bad scheduler faces the same fork-storm pace as a good one"입니다. 즉 scheduler가 영향을 줄 수 있는 시각까지 미리 고정하면, 나쁜 scheduler와 좋은 scheduler가 같은 속도의 fork 폭풍을 보게 되어 비교가 무의미해집니다. 그래서 무작위는 compile time에, scheduling이 바꾸는 시각은 run time에 둡니다.

compile time에 무작위를 푸는 방식에도 규칙이 있습니다. 하나의 전역 난수열을 순서대로 쓰지 않고, 모든 draw를 주소로 부릅니다. `dataset/tools/wlc/sampling.py`의 `uniform(seed, *key)`는 `"<seed>|<key1>|<key2>|…"`라는 문자열을 SHA-256으로 hash하고, 앞 8바이트를 2^64로 나눈 값을 0과 1 사이의 균등 난수로 씁니다. key에는 task id, parameter 이름, 몇 번째 draw인지가 들어갑니다. 이런 방식을 이 저장소는 `keyed draw`라고 부릅니다.

> **왜 이렇게 정했나.** task-2.3 spec의 decision 5(2026-08-27, `_dev/docs/spec/jioh/task-2.3-timeline-compiler.md`)는 "Sampling uses keyed substreams derived from `(seed, task id, param, draw index)` — never one global draw sequence — so unrelated edits cannot shift another task's draws and C2 byte-identity holds by construction"이라고 적습니다. C2는 intent pair 그룹, 즉 한 segment에서만 다른 두 파일의 쌍입니다. 전역 난수열을 쓰면 task 하나를 추가하는 순간 그 뒤의 모든 draw가 한 칸씩 밀려, 바꾸지 않은 task의 값까지 바뀝니다. keyed draw에서는 task 하나를 더해도 다른 task의 draw 주소가 그대로이므로 값도 그대로입니다.

seed는 timeline마다 하나씩 `meta.seed`에 적혀 있습니다. 예를 들어 `c1-dev.timeline.yaml`의 seed는 107입니다. 파생 파일(variant recipe로 만든 timeline)은 base의 seed를 물려받고 바꿀 수 없습니다. task-2.4 spec의 decision 4는 "a changed seed defeats the paired byte-discipline the derivation exists to provide"라고 그 이유를 적고, 지금의 deriver는 seed를 바꾸는 op 자체를 갖고 있지 않습니다(`test_coreset.py::test_variant_cannot_change_seed`가 `set-seed`라는 op가 "unknown op"로 거부되는지 확인합니다).

## 1.4 같은 입력이면 같은 바이트: canonical bytes

무작위를 모두 숫자로 바꿨다고 바이트가 저절로 같아지지는 않습니다. JSON을 쓰는 방식이 매번 같아야 합니다. dictionary의 key 순서, 공백, 숫자 표기, 줄 끝이 모두 고정되어야 합니다. compiler는 artifact를 다음 한 함수로 바이트로 만듭니다.

```python
def canonical_bytes(canonical):
    """The byte form the manifest hashes and the invariants diff."""
    return (json.dumps(canonical, sort_keys=True, separators=(",", ":"))
            + "\n").encode()
```

`sort_keys=True`는 key를 사전순으로 정렬합니다. `separators=(",", ":")`는 공백 없는 가장 짧은 표기를 고릅니다. 마지막에 줄바꿈 하나를 붙입니다. 이 밖에도 결정론을 위한 장치가 여럿 있습니다.

- 모든 시각은 정수 microsecond입니다. 소수점 표기의 흔들림이 없습니다.
- `events`는 `(t, op, id 또는 target)` 순으로 정렬됩니다(`wlc/compiler.py`).
- compile할 timeline 목록은 `sorted(…glob("**/*.timeline.yaml"))`로 정렬된 순서로 찾습니다(`tools/compile.py`의 `discover`).
- 여러 worker process가 병렬로 compile해도, 결과를 모은 뒤 정렬해서 manifest를 씁니다. 그래서 병렬 build의 manifest가 직렬 build의 manifest와 같은 바이트입니다(5장).

2026-10-10의 dataset audit(다섯 auditor가 `fe19be86` 시점의 branch를 독립적으로 점검한 기록, `_dev/docs/audit/jioh/2026-10-10-dataset-audit-before-9.15.md`)은 결정론을 이렇게 평가했습니다. "keyed SHA-256 draws, no global RNG, sorted-key JSON, sorted discovery, loud failures on short/wrong streams; residual risk: libm `pow`/`exp`/`log` before `round()` cross-platform (PLAUSIBLE, closes with one Linux CI run)". 마지막 구절이 중요합니다. compiler는 몇몇 값을 `math.exp` 같은 부동소수점 함수로 계산한 뒤 정수로 반올림합니다. 운영체제의 수학 library(libm)가 macOS와 Linux에서 마지막 비트까지 같은 값을 준다는 보장은 없습니다. 그러면 반올림 경계에 걸린 값 하나가 다르게 나올 수 있습니다. audit는 이것을 "그럴 법한 위험"으로 남기고, Linux CI에서 한 번 build해 보면 닫힌다고 적었습니다. 이 위험은 6장에서 보듯 2026-10-11 이후의 Linux CI run들이 committed manifest를 바이트 단위로 재현하면서 이 build에 대해서는 실제로 닫혔습니다.

손으로 하나 따라가 봅시다. `c1-dev`는 편집기 하나가 60초 동안 열려 있는 C1(calibration 그룹, 한 파일에 한 상황) 파일입니다. compile된 artifact의 `meta`는 다음과 같습니다(2026-10-14, `build/coreset-single/c1-dev.workload.json`에서 읽음).

```json
{"derived_from": "dataset/timelines/coreset/c1-dev.timeline.yaml@cbf1349a49dc465502d000b43a4d417532e61f40",
 "id": "c1-dev",
 "sampled": {"archetypes": "archetypes.yaml@a2cc1957dfe13c6a7c8a900a1f3d3644bb3935b4", "seed": 107}}
```

`derived_from`의 `@` 뒤는 timeline 파일의 git blob hash이고, `sampled.archetypes`의 `@` 뒤는 library 파일의 git blob hash입니다. 즉 artifact는 자신이 어떤 timeline 바이트, 어떤 library 바이트, 어떤 seed에서 나왔는지를 스스로 적고 있습니다. 같은 세 가지가 주어지면 같은 artifact가 나온다는 것이 task-2.3 spec의 첫 불변식입니다. "Same timeline + same library commit + same seed ⇒ byte-identical canonical output." 이 artifact의 SHA-256은 `build.manifest.json`의 `artifacts` 절에 적혀 있고, 2장에서 이것이 어떻게 이어지는지 봅니다.

## 1.5 그런데 왜 `build/`를 commit하지 않나

build가 결정론적이라면, build의 결과물은 입력이 정해지는 순간 함께 정해집니다. 입력(timeline, library, schema, compiler source, stimulus stream)은 모두 git에 있습니다. 그러니 결과물을 따로 저장할 필요가 없고, 결과물이 입력에서 나온 그대로인지만 확인하면 됩니다. README는 이 논리를 이렇게 적습니다. "That determinism is load-bearing (experiment hygiene), which is why `build/` isn't committed: CI recompiles and diffs hashes against the manifests instead."

generated layer의 timeline(`dataset/generated/<set>/`)도 같은 이유로 commit하지 않습니다. generated layer는 C1 파일들의 task set을 규칙에 따라 조합하거나 이름을 바꿔 만든 다섯 개의 설계 집합입니다(generated layer 권에서 다룹니다). sub-task 9.19(generator와 C3 grid를 만든 작업)의 spec decision 4는 이렇게 적습니다. "The timelines and their artifacts are build products, not committed; committed are the generator, its grid definition and each set's manifest. The generator is pure: its inputs are committed files only, its draws keyed, its output ordered." generator가 committed 파일만 읽고, keyed draw만 쓰고, 정렬된 순서로 출력하므로, generated timeline은 언제든 다시 만들 수 있는 build product입니다.

크기도 봅시다. 2026-10-14에 이 저장소의 working tree에서 `du`로 잰 값입니다.

| 경로 | 크기 | 파일 수 |
|---|---|---|
| `dataset/build/` 전체 | 6.8 GB | 3,304 |
| `build/coreset-single/` | 1.6 GB | 180 (core artifact 51 + report 51 + variant 78) |
| └ core artifact 51개 | 678,167,934 bytes (약 0.68 GB) | |
| └ variant 78개 | 1,030,349,631 bytes (약 1.03 GB) | |
| └ compile report 51개 | 28,523 bytes | |
| `build/transition-grid-single/` | 1.5 GB | 960 |
| `build/return-grid-single/` | 2.6 GB | 1,440 |
| `build/flap-stress-single/` | 209 MB | 48 |
| `build/distractor-grid-single/` | 844 MB | 544 |
| `build/familiarity-ladder-single/` | 96 MB | 132 |
| `dataset/generated/` (generated timeline) | 6.2 MB | 1,562 |

가장 큰 단일 파일은 `c6-dual.workload.json`으로 187,601,756 bytes입니다. 그 다음이 `c1-transcode`(152.8 MB), `c7-transcode`(95.1 MB)입니다.

> **왜 이렇게 정했나.** `build/`를 commit하지 않는다는 결정은 2026-08-27의 task-2.3 spec(timeline compiler를 정한 spec) decision 6에 있습니다. "`dataset/build/` is gitignored; a committed hash manifest (per-artifact content hashes + the input commits they derive from) is regenerated by `make dataset` and verified by CI recompilation." 이 결정에 적힌 이유는 lockfile pattern이라는 이름 자체와 결정론입니다. 크기는 이유로 적혀 있지 않습니다. 당시 build는 작았습니다. sub-task 9.13(rebuild)의 reads 기록은 2026-09-26 시점의 set을 50 files, 84 MB로 적습니다(`_dev/research/jioh/task-9.13-rebuild/reads.md` R4). 6.8 GB라는 크기는 결정 이후에 생긴 사실이고, 그 크기가 이제는 CI runner의 저장 공간과 맞서는 문제가 되었습니다(6장).

## 1.6 Lockfile에 비유하면

웹 개발자에게 가장 가까운 비유는 `package-lock.json`입니다. 대응은 이렇습니다.

| npm 세계 | 이 dataset |
|---|---|
| `package.json` — 원하는 것을 적은 파일 | timeline, `archetypes.yaml`, `grids.yaml`, `variants.yaml` — 원하는 workload를 적은 파일 |
| `package-lock.json` — 실제로 무엇이 설치되었는지 정확한 버전과 `integrity` hash | `build.manifest.json` 등 일곱 개 manifest — 실제로 무엇이 build되었는지 정확한 입력 hash와 출력 hash |
| `node_modules/` — commit하지 않음, 언제든 다시 만듦 | `dataset/build/`, `dataset/generated/` — commit하지 않음, 언제든 다시 만듦 |
| `npm ci` — lockfile대로 설치하고, `package.json`과 어긋나면 실패 | `make dataset variants generated` 후 `make check` — 다시 만들고, committed manifest와 어긋나면 실패 |
| lockfile 갱신 후 commit | `bless`: build를 다시 돌려 manifest를 새로 쓰고 commit |

비유가 맞지 않는 곳도 짚어 둡니다. npm의 lockfile은 "어디서 무엇을 내려받을지"를 고정합니다. 내려받은 tarball이 lockfile의 `integrity`와 같은지만 보면 됩니다. 이 dataset의 build는 내려받는 것이 아니라 계산하는 것입니다. 그래서 manifest는 입력(`inputs`)과 함께 출력(`artifacts`, `reports`)까지 hash로 고정합니다. 계산 과정이 같은 결과를 냈는지는 출력 hash로만 확인할 수 있기 때문입니다.

그래서 더 정확한 비유는 snapshot test입니다. Jest의 snapshot test는 component를 render한 결과를 `.snap` 파일로 commit해 두고, CI에서는 `--ci` 모드로 render 결과를 snapshot과 비교해 다르면 실패합니다. 의도한 변경이면 개발자가 `jest -u`로 snapshot을 갱신해 commit합니다. 이 dataset의 manifest가 바로 build 전체의 snapshot입니다. 다만 결과물이 GB 단위라 결과물 자체 대신 결과물의 hash를 snapshot으로 commit합니다. `make check`는 `jest --ci`에 해당하고, re-bless는 `jest -u` 후 commit에 해당합니다. 실제로 gate가 실패할 때 내는 메시지가 "re-bless (commit it) if the change is intended"입니다(4장).

## 1.7 이 장치들이 생긴 순서

이 권이 다루는 장치들은 한 번에 생기지 않았습니다. 기록에 남은 순서는 이렇습니다.

```
2026-08-27  task-2.3 decision 6  lockfile pattern: build/는 gitignore, committed hash manifest
2026-08-27  phase-2 decision 4   linter와 invariant test를 GitHub Actions에 연결
2026-09-06  Phase 3              manifest에 파일별 demand(utilization, demand_class) 추가
2026-09-09  Phase 7 decision 11  coverage grid의 빈 cell이 CI를 실패시킴 (7.3에서 --require-coverage 채택)
2026-10-09  9.13 D7              rebuild 후 첫 bless: 51 artifacts (native set 제거)
2026-10-09  9.14 decision 4      demand window가 gate에서 은퇴, demand를 segment별로 기록
2026-10-10  audit A4             gate의 구멍 네 가지 발견
2026-10-11  9.18                 compiler·stream을 inputs에 pin, report를 blessed artifact로,
                                 check_build.py가 on-disk build/를 검사, workflow_dispatch
2026-10-11  9.22                 gate가 다시 compile하지 않고 비교만: 3.5 h → 약 5 min
2026-10-11  9.19                 generated set 세 개와 그 manifest가 gate에 합류
2026-10-12  9.20                 generated set 두 개 추가, manifest 일곱 개
2026-10-13  9.21                 grid record에 placements·segments, build every run 결정
2026-10-14  9.21 D13             coreset_wide marker: 두 harness test를 CI에서 제외
```

여기서 9.13, 9.14, 9.17, 9.18, 9.19, 9.20, 9.21, 9.22는 Phase 9(workload dataset rebuild)의 sub-task 번호입니다. 각각 rebuild 실행(9.13), 소비자 쪽 재작업(9.14), window focus를 telemetry에 넣은 작업(9.17), compiler·schema·build gate 정비(9.18), generator와 C3 grid(9.19), C4·C5 grid(9.20), generated layer의 소비자 작업(9.21), build 시간 단축(9.22)을 맡았습니다. 실행 순서는 번호 순이 아니라 `_dev/TODO.md`에 적힌 대로 9.13 → 9.14 → 9.17 → 9.18 → 9.22 → 9.19 → 9.20 → 9.21입니다. 9.22는 9.18의 검증 run이 너무 오래 걸린 것을 보고 2026-10-11에 추가되어 9.19보다 먼저 돌았습니다.

> **열린 자리.** task-2.3 decision 6의 마지막 문장은 "Release artifacts publish from tagged CI builds, not the repo tree"입니다. 즉 dataset의 build를 tag된 CI build에서 release로 공개한다는 계획입니다. 2026-10-14 현재 `.github/workflows/` 아래의 어떤 workflow도 dataset build를 release로 올리지 않습니다(`dataset.yml`은 build하고 비교할 뿐 업로드 단계가 없습니다). sub-task 9.15(문서 정비, 2026-10-14 WIP)의 spec은 저장소 root의 `LICENSE`와 `dataset/LICENSE`를 추가한다고 정했지만(decision 12), build artifact의 release 공개는 다루지 않습니다. 공개 시점과 방식(tag된 CI run에서 GitHub release로 올릴지, 다른 보관소를 쓸지)은 기록에 정해져 있지 않으며 인지오가 정할 일입니다.

---

# 2장 · Manifest 일곱 개의 해부

## 2.1 이 장의 질문

이 장은 "manifest에는 정확히 무엇이 적혀 있고, 그 hash 하나하나는 어떻게 만들어지나"를 묻습니다. 1장에서 manifest를 lockfile 또는 snapshot이라고 불렀습니다. 그 비유가 실제로 어떤 field와 어떤 hash로 구현되어 있는지 보지 않으면, 3장의 bless와 pin, 4장의 gate가 무엇을 비교하는지 알 수 없습니다. 또 파일 하나를 고쳤을 때 manifest의 어느 줄이 움직이는지 미리 알 수 있어야 실수를 피할 수 있습니다. 이 장의 끝(2.11)에 그 표가 있습니다.

`manifest`는 이 저장소에서 "build 하나의 입력과 출력을 hash로 고정한 committed JSON 파일"을 뜻합니다. 모두 `dataset/` 바로 아래에 있고, `build.`로 시작해 `.manifest.json`으로 끝납니다.

## 2.2 일곱 개의 목록과 그 관계

2026-10-14 현재 manifest는 일곱 개입니다. 아래 표의 section 수와 entry 수는 `python3.12 -c`로 각 파일을 열어 센 값이고, 크기는 `ls -l`의 바이트 수입니다.

| manifest | 무엇의 lockfile인가 | section과 entry 수 | 크기 |
|---|---|---|---|
| `build.manifest.json` | core set 51개 | `inputs` 23, `artifacts` 51, `reports` 51, `demand` 51 | 30,626 B |
| `build.variants.manifest.json` | sensitivity variant 78개 | `inputs` 3, `artifacts` 78 | 36,061 B |
| `build.transition-grid.manifest.json` | generated set: transition grid | `inputs` 45, `artifacts`·`reports`·`demand`·`grid` 각 480 | 733,513 B |
| `build.return-grid.manifest.json` | generated set: return grid | `inputs` 45, 나머지 각 720 | 1,408,337 B |
| `build.flap-stress.manifest.json` | generated set: flap-stress | `inputs` 45, 나머지 각 24 | 116,191 B |
| `build.distractor-grid.manifest.json` | generated set: distractor grid | `inputs` 45, 나머지 각 272 | 417,964 B |
| `build.familiarity-ladder.manifest.json` | generated set: familiarity ladder | `inputs` 45, 나머지 각 66 | 84,222 B |

일곱 manifest가 고정하는 `build/` 아래의 파일은 합쳐서 51 + 51 + 78 + 2 × 1,562 = 3,304개입니다. 4장의 gate가 2026-10-14에 출력한 줄이 정확히 이 숫자입니다. "build verified (3304 files, 7 manifests)".

몇 가지 용어를 먼저 정리합니다.

- `core set` (`coreset`) — 사람이 설계한 51개의 workload입니다(`dataset/timelines/coreset/`). RQ0 실험이 이 파일들 위에서 돌아갑니다.
- `sensitivity variant` — RQ0 gate spec이 결론의 견고함을 확인하려고 쓰는, core set 파일을 한 가지 방식으로 변형한 사본입니다. 측정값을 0.8배나 1.25배로 키우거나(venue factor), 첫 segment 길이를 바꾸거나, 측정된 wake 순서를 그대로 재생하는 식입니다(variants 권에서 다룹니다). `dataset/variants.yaml`이 아홉 개 set을 정의합니다.
- `mode` — 사용자가 지금 어떤 상황에 있는지의 이름입니다. `dev`, `office`, `gaming`, `compile`, `idle` 등 16개가 있고, segment의 정답 label이 이것입니다. C1 그룹은 mode마다 그 mode 하나만 담은 파일을 하나씩 가집니다.
- `generated layer` — C1 파일들의 task set을 규칙에 따라 조합한 다섯 개의 설계 집합입니다(`dataset/grids.yaml`). transition grid(두 mode 사이의 전환 480개), return grid(A → B → A 720개), flap-stress(빠른 전환 반복 24개), distractor grid(상황은 그대로인데 다른 process가 끼어드는 272개), familiarity ladder(process 이름만 낯설게 바꾼 66개)입니다.

일곱 manifest는 서로 hash로 이어져 있습니다.

```
 archetypes.yaml · schema · compile.py · wlc/*.py · stimulus/*.jsonl · replay/*.json.gz
                          │  (각 파일의 SHA-256, 23개)
          ┌───────────────┴─────────────────────────────┐
          ▼                                             ▼
 build.manifest.json  ◀── sha256 ── build.variants.manifest.json
   inputs 23                         inputs: variants.yaml, archetypes.yaml,
   artifacts/reports/demand 51               build.manifest.json  (3)
          │                          artifacts 78 (각각 base_sha256 포함)
          │
          │   + grids.yaml · generate.py · gen/*.py · c1-*.timeline.yaml 16개
          ▼
 build.<set>.manifest.json × 5   inputs 45 (= 23 + 22)
   artifacts/reports/demand/grid

 harness/experiments/rq0-gate.yaml
   pins.dataset      = sha256(build.manifest.json)
   pins.variants.all = sha256(build.variants.manifest.json)
```

variants manifest는 core manifest의 SHA-256을 자신의 입력으로 적습니다. generated manifest 다섯 개는 core manifest와 같은 23개 compile 입력을 직접 다시 적고, 거기에 generator의 입력 22개를 더합니다. 그리고 실험 쪽의 RQ0 gate spec이 core manifest와 variants manifest의 SHA-256을 `pins`로 적습니다. 이 사슬 덕분에, 입력 파일 한 바이트가 바뀌면 그 변화가 실험 사양의 hash 한 줄까지 전파되어 눈에 보입니다.

## 2.3 Hash는 어떻게 만들어지나

이 dataset에는 hash가 두 종류 있고, 그 둘을 섞으면 헷갈립니다.

**하나는 SHA-256입니다.** manifest의 모든 값은 파일 바이트의 SHA-256(64자리 hex)입니다. `compile.py`의 함수는 단순합니다.

```python
def sha256(data):
    return hashlib.sha256(data).hexdigest()
```

`inputs`의 값은 입력 파일을 디스크에서 읽은 바이트의 SHA-256입니다. `artifacts`의 값은 artifact의 canonical bytes(1.4에서 본, key 정렬된 공백 없는 JSON과 줄바꿈)의 SHA-256입니다. `reports`의 값은 compile report를 `json.dumps(report, sort_keys=True, indent=2) + "\n"`으로 바이트로 만든 것의 SHA-256입니다(`report_bytes`). artifact는 공백 없는 형태로, report는 사람이 읽기 쉬운 두 칸 들여쓰기 형태로 쓰이는데, 각각 정해진 한 가지 형태로만 쓰이므로 hash가 흔들리지 않습니다. manifest 파일 자체도 `json.dumps(manifest, indent=2, sort_keys=True) + "\n"`로 씁니다. RQ0 gate spec의 pin은 이렇게 쓰인 manifest 파일 바이트의 SHA-256입니다.

**다른 하나는 git blob hash입니다.** artifact 안의 `meta.derived_from`과 `meta.sampled.archetypes`에 붙는 `@` 뒤의 40자리 hex가 이것입니다. `wlc/library.py`의 `git_blob_hex`는 `sha1(b"blob <길이>\0" + 파일 바이트)`를 계산합니다. 이것은 `git hash-object`와 같은 값입니다. docstring은 이렇게 적습니다. "Git blob sha1 of a file's content — the deterministic `@<hex>` pin used in canonical meta (matches `git hash-object`)." git blob hash를 쓰면 그 값으로 git history에서 정확히 그 바이트의 파일을 찾을 수 있습니다.

같은 파일에 두 hash가 붙는 예를 봅시다. 2026-10-14의 `dataset/archetypes.yaml`은 다음 두 값을 가집니다.

| 어디에 쓰이나 | 종류 | 값 |
|---|---|---|
| 모든 artifact의 `meta.sampled.archetypes` | git blob SHA-1 | `a2cc1957dfe13c6a7c8a900a1f3d3644bb3935b4` |
| 모든 manifest의 `inputs["dataset/archetypes.yaml"]` | SHA-256 | `c6af7623c5164bdf1eb267f6335d4269dcbb6c7508fbc6331aab2724f782762d` |

> **코드로.** 기록 하나가 이 둘을 섞어 부릅니다. sub-task 9.13의 changelog D7(2026-10-09의 bless)은 "the final library (`dataset/archetypes.yaml` blob `c6af7623…`)"라고 적는데, `c6af7623…`은 git blob hash가 아니라 manifest의 SHA-256입니다(`_dev/research/jioh/task-9.13-rebuild/changelog.md`). 같은 파일을 가리키므로 내용상 문제는 없지만, `git show c6af7623`처럼 blob으로 찾으면 찾을 수 없습니다. git으로 찾을 때는 `a2cc1957…`을 씁니다. library는 9.13의 커밋 `1dc4af4d`(2026-10-09) 이후 바뀌지 않았으므로 두 값 모두 그때부터 같습니다.

이 두 hash가 어떻게 연쇄를 만드는지 따라가 봅시다. `archetypes.yaml`에 주석 한 줄을 더하면 무엇이 바뀔까요.

1. 파일의 git blob hash가 바뀝니다.
2. 모든 artifact의 `meta.sampled.archetypes`가 바뀝니다. 주석은 어떤 sampling 값도 바꾸지 않지만, artifact가 library의 hash를 스스로 적고 있으므로 artifact의 바이트가 바뀝니다.
3. 그래서 51개 core artifact, 78개 variant, 1,562개 generated artifact의 SHA-256이 전부 바뀝니다.
4. 일곱 manifest가 모두 바뀌고, `inputs`의 `dataset/archetypes.yaml` 줄도 바뀝니다.
5. core manifest와 variants manifest의 SHA-256이 바뀌므로 RQ0 gate spec의 두 pin을 다시 적어야 합니다.

이 성질 때문에 "library를 고쳤는데 실제로 값이 바뀐 artifact는 무엇인가"를 따로 알아내는 도구가 있습니다. `dataset/tools/beyond_hash.py`는 새로 compile한 artifact 안의 새 library blob hash를 HEAD의 blob hash로 되돌려 끼운 뒤 HEAD manifest의 hash와 비교합니다. 그래도 다른 artifact만이 "library의 hash 너머로" 바뀐 것입니다. docstring은 "The changelogs' 'N of 100 artifacts changing beyond the library's hash' and their demand moves are this report"라고 적습니다(100은 native set이 있던 시절의 artifact 수입니다).

## 2.4 `inputs` — build가 읽은 것

core manifest의 `inputs`는 23개입니다. 2026-10-14의 목록은 다음과 같습니다(값은 SHA-256의 앞 12자리).

| 경로 | SHA-256 앞부분 |
|---|---|
| `dataset/archetypes.yaml` | `c6af7623c516` |
| `dataset/schema/workload.schema.json` | `a323b4df7046` |
| `dataset/tools/compile.py` | `1e6b1dd3d7a4` |
| `dataset/tools/wlc/__init__.py` | `8af88d31985d` |
| `dataset/tools/wlc/compiler.py` | `35d1bcee6ff1` |
| `dataset/tools/wlc/deriver.py` | `6e725a858c8a` |
| `dataset/tools/wlc/estimate.py` | `746294053801` |
| `dataset/tools/wlc/grid.py` | `7079592c6064` |
| `dataset/tools/wlc/library.py` | `9ada360cbe79` |
| `dataset/tools/wlc/linter.py` | `c91f9ffed857` |
| `dataset/tools/wlc/sampling.py` | `93d9b773490a` |
| `dataset/tools/wlc/timeline.py` | `a35727817d21` |
| `dataset/tools/wlc/units.py` | `2c32e9ee9ed0` |
| `dataset/tools/wlc/variants.py` | `15b597b31e08` |
| `dataset/stimulus/swell-ie-c1.jsonl` | `ebdf89572297` |
| `dataset/stimulus/swell-outlook-c23.jsonl` | `491d6ead5277` |
| `dataset/stimulus/swell-word-c1.jsonl` | `1175db0cd291` |
| `dataset/replay/replay-code-editor.json.gz` | `153143212589` |
| `dataset/replay/replay-cpu-batch-python3.json.gz` | `9dbe1e282b55` |
| `dataset/replay/replay-package-upgrade.json.gz` | `3496e4263bd0` |
| `dataset/replay/replay-renderer-hidden.json.gz` | `aa97e9b3f780` |
| `dataset/replay/replay-video-call.json.gz` | `fbf0b9e9833b` |
| `dataset/replay/replay-web-browser.json.gz` | `c433285bdea5` |

여기 나온 두 종류의 stream을 정리합니다. `stimulus stream`은 SWELL-KW 연구의 실제 키 입력 기록에서 뽑은 키 입력 시각열로, 편집기 같은 interactive task의 `input` 창에 재생됩니다(`dataset/stimulus/`). `replay stream`은 측정 campaign에서 관찰한 한 번의 wake 순서 전체로, `trace-replay` variant가 sampling 대신 그대로 재생합니다(`dataset/replay/`).

목록은 `compile.py`의 `input_files` 함수가 만듭니다. library, schema, `compile.py`, `wlc/*.py`(정렬), `stimulus/*.jsonl`(정렬), `replay/*.json.gz`(정렬)입니다. timeline 파일은 이 목록에 없습니다. timeline은 각 artifact의 `meta.derived_from`에 git blob hash로 이미 들어가 있어서, timeline을 고치면 그 timeline의 artifact hash가 바뀌기 때문입니다. docstring이 "everything the compile reads besides the timelines"라고 적는 이유입니다.

> **왜 이렇게 정했나.** 2026-10-11 이전의 `inputs`는 library와 schema 두 개뿐이었습니다. 2026-10-10 audit의 A4(build gate의 구멍들)는 이렇게 적었습니다. "`build.manifest.json.inputs` pins archetypes and schema only (compile.py:67-73), streams and compiler unpinned (drift detected via artifact hashes, not attributed)". 같은 audit의 답변 표는 "the manifest pins two of about 75 inputs"라고도 적습니다. 핵심은 "detected but not attributed"입니다. compiler나 stream이 바뀌어 artifact가 달라지면 artifact hash로 *무엇인가* 바뀌었다는 것은 알 수 있지만, *무엇이* 바뀌었는지는 manifest만 봐서는 알 수 없었습니다. sub-task 9.18(compiler, schema and build gate)의 spec decision 5가 이 구멍을 닫았습니다. "`build.manifest.json`'s `inputs` gains the compiler's source files and the stimulus and replay streams, each as path → SHA-256 of its bytes, as the archetype library and the schema are pinned today." (`_dev/docs/spec/jioh/task-9.18-compiler-schema-and-build-gate.md`)

compiler source를 pin했다는 것은 출력이 바뀌지 않는 compiler 수정도 manifest를 움직인다는 뜻입니다. 이것은 의도된 동작입니다. 9.22(build 시간 단축)가 그 예입니다. 9.22는 `compile.py`, `wlc/linter.py`, `wlc/variants.py` 세 파일을 고쳐 병렬화하고 schema validator를 바꿨는데, 모든 artifact, report, variant는 바이트 하나 바뀌지 않았습니다. 그래도 manifest의 `inputs`가 바뀌었고, 9.22 changelog의 D5(manifest들을 다시 bless하고 RQ0 pin을 다시 적은 결정)는 이렇게 기록합니다. "the diff of the two manifests against `HEAD` is the `inputs` section alone". 그래서 core manifest가 `976a943c…`에서 `d10bcd42…`로, variants manifest가 `6c244f17…`에서 `831a854e…`로 바뀌고 RQ0 gate spec의 pin이 따라 바뀌었습니다.

> **열린 자리.** compiler가 읽는데 `inputs`에 없는 입력이 하나 있습니다. `dataset/launch/` 아래의 launch stream 열 개(`launch-<entry>.json.gz`)입니다. launch stream은 application이 파일 중간에 시작될 때 그 시작 단계의 wake들을 관찰된 그대로 재생하는 데 쓰입니다(측정 campaign 권). `wlc/compiler.py`의 `_load_launch`가 이 파일들을 읽지만, `compile.py`의 `input_files`는 `stimulus/*.jsonl`과 `replay/*.json.gz`만 모읍니다. 2026-10-14의 core manifest `inputs` 23개에도 `dataset/launch/`는 없습니다(위 표). 9.18 spec decision 5의 문구가 "the stimulus and replay streams"만 이름으로 들었고, launch stream은 그보다 먼저, sub-task 9.10(scenario와 timeline 연구)의 D139–D140(열 개 application entry가 관찰된 launch 단계를 재생하게 한 결정, 커밋 `34a5ebb0`, 2026-10-05)에서 들어왔습니다. 그래서 launch stream이 바뀌면 그것을 쓰는 파일들의 artifact hash로는 드러나지만, audit A4가 지적한 그대로 "detected via artifact hashes, not attributed" 상태입니다. `test_manifest.py::test_manifest_pins_the_compile_inputs_by_content`도 stimulus와 replay만 확인하므로 이 빈자리를 잡지 않습니다. 선택지는 `input_files`에 `dataset/launch/*.json.gz`를 더하는 것(그러면 일곱 manifest의 `inputs`가 모두 바뀌고 RQ0 gate spec을 다시 pin해야 합니다)과, 지금처럼 두고 그 사실을 문서에 적는 것입니다. 인지오가 정할 일입니다.

같은 기준으로 보면, build 도구 중 manifest가 pin하지 않는 것이 몇 개 더 있습니다. `tools/variants.py`(variant CLI), `tools/derive.py`, `tools/lint.py`, `tools/check_build.py`입니다. 코드에서 보이는 사실은 이렇습니다. `derive.py`의 결과물(파생 timeline)은 commit되고, 각 artifact의 `derived_from`이 그 바이트를 git blob hash로 고정합니다. `tools/variants.py`는 variant를 build하고 manifest를 쓰는 CLI이고, 변형 논리 자체는 `wlc/variants.py`에 있어 그쪽은 core manifest가 pin합니다. `lint.py`와 `check_build.py`는 아무것도 쓰지 않습니다. 이 네 도구를 `inputs`에 넣지 않은 이유는 기록에 따로 적혀 있지 않습니다.

## 2.5 `artifacts` — 만들어진 것

`artifacts`는 `build/` 아래 상대 경로에서 SHA-256으로 가는 map입니다. core manifest의 첫 두 줄은 이렇습니다.

```json
"coreset-single/c1-backup.workload.json": "e1926dad3199345cb86989458bb7c4856a5617eb31e5038cd22997c9ab4fa844",
"coreset-single/c1-browsing.workload.json": "6944f6aa4b05af87908559fc5eb37aa8b827241ac5c2eb5eb8212d3ee118558b",
```

경로의 첫 부분 `coreset-single`은 timeline이 놓인 디렉터리 이름(`coreset`)에 compile mode(`single`)를 붙인 것입니다(`compile.py`의 `artifact_set`과 `compile_one`). `single`은 single-lane mode, 즉 simulator의 CPU 하나(`lane`)에 맞춰 scaling한 compile을 뜻합니다. 지금은 이 mode 하나만 있습니다(`wlc/compiler.py`의 `MODES = ("single",)`).

> **왜 이렇게 정했나.** 원래는 측정값 그대로의 `-native`와 single-lane `-single` 두 mode가 있어 artifact가 두 배였습니다(Phase 7 시절 100개). 9.5 spec decision 14(2026-09-16)가 native set을 버리기로 했고, 9.13 spec decision 5(2026-10-09)가 그것을 compiler에서 지웠습니다. 기록된 이유는 library의 archetype들이 서로 다른 측정 환경에서 왔고 그 상대적 크기가 서로 보정되어 있지 않다는 9.5 spec decision 13의 한계에서 같은 추론으로 나왔다는 것입니다(`_dev/docs/spec/jioh/task-9.5-interactive-typing-follow-ups.md`). 그래서 9.13의 bless에서 manifest는 "the 50 native entries gone, 51 single-lane entries"가 되었습니다.

## 2.6 `reports` — compile report도 blessed artifact다

`reports`는 각 artifact 옆에 쓰인 compile report의 hash입니다. key는 `coreset-single/<id>.report.json`입니다. `compile report`는 compiler가 artifact를 만들며 계산한 수요 정보를 적은 작은 JSON입니다. `c1-dev`의 report는 다음과 같습니다(2026-10-14).

```json
{"demand_class": "calibration", "demand_us": 19913142, "duration_us": 60000000,
 "operations": {}, "per_segment": [{"index": 0, "t_end_us": 60000000, "t_start_us": 0, "utilization": 0.3318857}],
 "per_task": {"editor": 19913142}, "utilization": 0.3318857}
```

편집기 하나가 60초 중 약 19.9초의 CPU를 요구하므로 utilization이 약 0.33입니다. 여기서 `utilization`은 파일의 모든 task가 요구하는 CPU 시간을 파일 길이로 나눈 정적 추정치입니다(`wlc/estimate.py`). simulator에서 실제로 측정한 값이 아니라 compile 시점의 계산입니다.

> **왜 이렇게 정했나.** report를 build의 산출물로 쓰고 manifest가 그 hash를 따로 고정하게 한 것은 9.18 spec decision 8입니다. "The compile report is a blessed artifact. The compiler writes each artifact's report beside it in `build/`, and the manifest pins the reports' hashes in a section of their own; the `demand` section is unchanged. The `coreset` fixture reads an artifact and its report from `build/` when both hash to the manifest's entries, and compiles otherwise." 이유는 결정의 둘째 문장에 붙어 있습니다. test가 report를 필요로 하는데, report가 디스크에 없으면 test가 51개 timeline을 다시 compile해야 했습니다. sub-task 9.17(focus를 telemetry에 넣은 작업)의 인계 기록은 그 비용을 "`test_coreset.py`'s module fixture recompiled the 51 timelines in-process, about 25 of the suite's 50 minutes"라고 적습니다. report가 blessed artifact가 되면 test는 hash를 확인한 뒤 디스크의 report를 그대로 읽을 수 있습니다(7장).

이 section을 처음 넣었을 때 gate가 자기 버그를 잡은 일이 있습니다. 9.18 changelog의 D6(rebuild, re-bless, re-pin)은 이렇게 기록합니다. "The first `check_build` run failed on 102 errors and exposed a defect in D3's code: `compile.py` keyed the manifest's `reports` section by the artifact's path, not the report's, so the section overwrote the artifact hashes in `check_build`'s union". 즉 report의 hash를 artifact의 경로로 적는 바람에, gate가 manifest들을 합칠 때 report hash가 artifact hash를 덮어써서 51개 artifact가 모두 틀린 hash로 보였고 51개 report는 고정되지 않은 파일로 보였습니다(51 + 51 = 102). 수정은 `report_path(rel)`을 key로 쓰는 것이었고, 이 함수가 지금 `compile.py`에 있습니다. 같은 기록은 "`test_manifest.py` asserts the right keys and would have caught it; it compiles the set, 24 min, and had not been run"이라고 덧붙입니다. 느린 test가 돌지 않아 놓친 버그를 빠른 gate가 잡은 경우입니다.

report에는 파일 id가 들어 있지 않습니다. 그래서 timeline의 이름만 바꾸면 report hash는 그대로입니다. 9.20(C4·C5 grid)에서 `c5-t3`가 `c6-alias`로 이름을 바꿨을 때 changelog D10은 "the report's hash equal: the report carries no id"라고 적었습니다.

## 2.7 `demand` — 파일별, segment별 수요

`demand`는 artifact마다 `{demand_class, utilization, segments}`를 적습니다. `utilization`은 report의 값을 소수 넷째 자리로 반올림한 것이고, `segments`는 정답 segment마다 `{index, t_start_us, t_end_us, utilization}`입니다. `c3-workday`(한 사람의 근무일을 browsing → office → compile → mail로 이은 C3, 즉 transition arc 그룹의 파일)의 entry는 이렇습니다.

```json
{"demand_class": "oversubscribed", "utilization": 0.888,
 "segments": [{"index": 0, "t_start_us": 0,          "t_end_us": 60000000,   "utilization": 0.0031},
              {"index": 1, "t_start_us": 60000000,   "t_end_us": 120000000,  "utilization": 0.0053},
              {"index": 2, "t_start_us": 120000000,  "t_end_us": 1485000000, "utilization": 0.9597},
              {"index": 3, "t_start_us": 1485000000, "t_end_us": 1545000000, "utilization": 1.0251}]}
```

`demand_class`는 timeline의 `meta.demand`에서 옵니다. `oversubscribed`는 "경합을 담도록 설계한 파일"이고 `calibration`은 "경합을 담지 않는 파일"입니다. 2026-10-14의 core manifest에서는 `calibration` 40개, `oversubscribed` 11개입니다.

> **왜 이렇게 정했나.** 수요를 manifest에 적기 시작한 것은 Phase 3입니다. 2026-09-06 기록은 "Demand estimate becomes a build artifact in `dataset/build.manifest.json` rather than an archive-only number, so the paper can cite a committed value"라고 적고, 그 전 상태를 "the compiler computed utilization and demand class but printed them to stdout only; the manifest carried hashes alone"라고 확인했습니다. 논문이 인용할 수 있는 commit된 숫자를 남기기 위해서입니다. segment별 값은 9.14 spec decision 4(2026-10-09)가 더했습니다. 같은 결정이 이른바 demand window, 즉 `oversubscribed` 파일이 lane의 약 100–150 % 수요여야 한다는 규칙을 gate에서 은퇴시켰습니다. "The compiler records demand per file, as now, and per segment, newly, in the manifest, and never fails on it." 그 근거는 9.13의 reads R5가 보인 사실입니다. `oversubscribed` 파일 열 개 중 아홉 개가 창 밖에 있었고, 그 이유가 결함이 아니라 설계였습니다. 학습 run과 다운로드의 CPU 총량을 짧은 파일 안에 통째로 묶었기 때문입니다.

이 마지막 사실은 `demand`를 읽을 때 주의할 점을 남깁니다. `c2-p1a`의 utilization은 14.505이고 둘째 segment는 35.7721입니다. `c2-p2a`는 9.3829, 둘째 segment 28.5251입니다. CPU 하나에 14배, 35배의 수요라는 뜻이 아닙니다. 정적 추정은 batch job의 `total_work` 전체(MNIST 학습 1,389.885 s, SteamCMD 다운로드 727.170 s)를 그 task의 수명 동안 고르게 펼치는데, 파일이 job보다 훨씬 짧게 끝나므로 숫자가 커집니다. 이 점을 문서에 한 문장으로 한정하거나 값을 잘라 적는 일은 9.15(문서 정비)의 작업 목록에 있습니다("the manifest's `demand` for a job outliving its file (`c2-p1a`, `c2-p2a`) scoped in a sentence or clipped", `_dev/TODO.md`의 9.15 줄).

## 2.8 Variants manifest

variants manifest는 구조가 다릅니다. `inputs` 세 개와 `artifacts` 78개뿐이고, `reports`와 `demand`가 없습니다.

```json
"inputs": {
  "dataset/archetypes.yaml":     "c6af7623c5164bdf1eb267f6335d4269dcbb6c7508fbc6331aab2724f782762d",
  "dataset/build.manifest.json": "fad7192d2a290c9d0b9f9563a45a0f9834b8c48403c4c88d84ae1869107accd3",
  "dataset/variants.yaml":       "6ad716708aabc29483007c86e3b7e3026369ef683d0c868b54378e59bcf8c454"
}
```

`artifacts`의 값은 hash 하나가 아니라 record입니다. 2026-10-14의 실제 예 세 개입니다.

```json
"coreset-single/c1-compile@venue-x0.8.workload.json":
  {"base": "coreset-single/c1-compile.workload.json",
   "base_sha256": "843eb86575f1a58fde29f4f874e19ab150b71f9a96540b086397ad3f9b4d5978",
   "set": "venue-x0.8", "sha256": "550a85af11ac72a39c97634aaae64ca8cfef267702d38c686710f7974b5de4d9",
   "transform": {"factor": 0.8, "transform": "scale-runs"}}

"coreset-single/c1-compile@corner-high.workload.json":
  {"base": "coreset-single/c1-compile.workload.json", "base_sha256": "843eb865…",
   "set": "corner-high", "sha256": "e6bf2847…",
   "transform": {"side": "high", "transform": "carried-bounds"}, "utilization": 0.9982}

"coreset-single/c2-p1a@replay.workload.json":
  {"base": "coreset-single/c2-p1a.workload.json", "base_sha256": "a7b48292…",
   "replay": {"editor": {"offset_us": 243964687, "stream": "replay-code-editor"},
              "hog": {"offset_us": 0, "stream": "replay-cpu-batch-python3"}},
   "set": "replay", "sha256": "8baf988a…",
   "transform": {"streams": {…}, "transform": "trace-replay"}, "utilization": 14.5036}
```

record의 field는 이렇습니다. `base`는 원본 artifact의 경로, `base_sha256`은 core manifest에 적힌 원본의 hash, `set`은 variant set 이름, `sha256`은 variant 자신의 hash, `transform`은 그 set의 변형 방식과 parameter입니다. `utilization`은 다시 compile한 variant에만 있습니다. 78개 중 34개로, `segment-length` 8개, `carried-bounds` 22개, `trace-replay` 4개입니다. `scale-runs`와 `scale-chain`은 다시 compile하지 않고 blessed artifact의 RUN 값에 곱하기만 하므로(`variants.yaml`의 주석: "on the blessed artifact, no recompile") report가 없고 utilization도 없습니다. `replay`는 trace-replay variant 네 개에만 있고, task별로 어느 stream의 어느 offset을 재생했는지 적습니다.

set별 개수는 `venue-x0.8` 19, `venue-x1.25` 19, `corner-low` 11, `corner-high` 11, `seg1-30s` 4, `seg1-120s` 4, `replay` 4, `chain-x1.2` 3, `chain-x1.4` 3으로 78개입니다. 원본은 19개의 judging file입니다. `judging file`은 RQ0의 판정에 실제로 쓰이는 파일이고, 나머지 32개는 보고만 하는 `reporting file`입니다(RQ0 gate spec의 `files`).

> **왜 이렇게 정했나.** variant의 출처를 artifact 안이 아니라 manifest에 적는 이유는 `variants.yaml`의 머리 주석과 9.14 changelog D8이 같은 말로 적습니다. "A variant keeps its base's `meta.derived_from` and `sampled` (the workload contract has no slot for a transform); the manifest is the provenance." canonical workload 형식에는 "이 파일은 어떤 변형을 거쳤다"를 적을 자리가 없으므로, variant의 `meta`는 base와 같고, 무엇을 했는지는 manifest의 `transform`이 말합니다. 그래서 variants manifest는 hash 목록이면서 동시에 출처 기록입니다.

variants manifest가 core manifest의 hash를 입력으로 적는 이유도 같은 데서 나옵니다. `scale-runs`와 `scale-chain` variant는 blessed core artifact를 직접 읽어 변형합니다. 그러니 variant가 옳으려면 그것이 만들어진 core build가 committed core manifest와 같아야 합니다. core manifest의 hash를 입력으로 적으면, core가 바뀌는 순간 variants manifest도 바뀌어 다시 bless해야 한다는 것이 드러납니다. 9.20에서 `c5-t3`가 `c6-alias`로 바뀌었을 때가 그 예입니다. changelog D10은 "78 artifacts byte-identical; the manifest's `inputs` entry for the dataset manifest moved"라고 적습니다. variant 78개는 하나도 안 바뀌었지만 manifest는 바뀌었습니다.

> **코드로.** `tools/variants.py`의 `build`가 manifest를 만듭니다. `--sets a,b`로 일부 set만 build하면 artifact는 쓰지만 manifest는 쓰지 않습니다("manifest not written"). 일부만 담은 manifest가 committed manifest를 덮어쓰지 않게 하려는 것입니다. variant artifact는 base와 같은 디렉터리 `build/coreset-single/`에 `<base>@<set>.workload.json`으로 놓입니다. 그래서 `coreset-single/`의 180개 파일 중 78개는 variant입니다.

## 2.9 Generated manifest 다섯 개

generated manifest는 core manifest의 네 section에 `grid` section 하나를 더합니다. `inputs`는 45개입니다. core의 23개 compile 입력이 같은 hash로 그대로 들어가고(2026-10-14에 return grid manifest로 확인: 23개 모두 core manifest와 같은 값), generator의 입력 22개가 더해집니다. `dataset/grids.yaml`(generated layer의 정의), `dataset/tools/generate.py`, `dataset/tools/gen/` 아래의 `__init__.py`, `cells.py`, `compose.py`, `coverage.py`, 그리고 C1 timeline 16개(`c1-backup` … `c1-video-edit`)입니다.

> **코드로.** 9.19 changelog D3은 generated manifest의 입력을 "44 paths"라고 적습니다. 지금은 45개입니다. 차이는 `gen/coverage.py`로, 9.21의 D2(coverage table을 `wlc`가 아니라 generator 옆에 둔 결정)가 2026-10-13에 더했습니다. `generate.py`의 `generator_inputs`가 `gen/*.py`를 glob하므로 새 파일이 자동으로 들어갔습니다.

> **왜 이렇게 정했나.** generated manifest가 generator와 C1 timeline까지 pin하는 이유는, generated timeline이 commit되지 않기 때문입니다. commit되지 않은 timeline이 무엇에서 나왔는지 기록할 committed 장소는 manifest뿐입니다. 9.19 spec decision 4가 "The generator is pure: its inputs are committed files only"라고 한 것은, 바로 이 45개 입력이 generated set 전체를 결정한다는 뜻입니다. set마다 manifest를 하나씩 둔 것은 9.19 spec decision 5입니다. "One manifest per generated set … The manifest is the set's pin; no experiment spec pins it yet (the RQ1 and RQ4 experiment specs will …)". 나중에 어떤 실험이 return grid만 쓴다면 그 manifest 하나만 pin하면 됩니다.

`grid` section은 artifact마다 그 파일의 좌표와 내용 요약을 적습니다. set마다 좌표의 key가 다릅니다(2026-10-14의 manifest에서 모든 record의 key 합집합).

| set | `grid` record의 key |
|---|---|
| transition grid | `a`, `b`, `form`, `placements`, `segments` |
| return grid | `a`, `b`, `middle`, `placements`, `segments`, `split` |
| flap-stress | `a`, `b`, `interval`, `interval_source`, `placements`, `segments`, `split` |
| distractor grid | `a`, `b`, `focus_name_shared`, `placements`, `relation`, `segments` |
| familiarity ladder | `carrier`, `carriers`, `mode`, `placements`, `renamed`, `segments`, `sources`, `tier` |

return grid의 첫 record를 그대로 옮깁니다. backup으로 시작해 browsing으로 10초 갔다가 backup으로 돌아오는 파일입니다.

```json
"return-grid-single/rt-backup-to-browsing-10s.workload.json": {
  "a": "backup", "b": "browsing", "middle": "10s", "split": "measurement",
  "placements": [
    {"input": true, "mode": "backup",   "segments": [0], "suffix": 0},
    {"input": true, "mode": "browsing", "segments": [1], "suffix": 1},
    {"input": true, "mode": "backup",   "segments": [2], "suffix": 2}],
  "segments": [
    {"background_wanted": true, "mode": "backup",   "pre_committed_miss": false, "tier": 1},
    {"background_wanted": true, "mode": "browsing", "pre_committed_miss": false, "tier": 1},
    {"background_wanted": true, "mode": "backup",   "pre_committed_miss": false, "tier": 1}]}
```

`a`, `b`, `middle`은 이 파일이 grid의 어느 칸인지입니다. `split`은 이 파일이 tuning 절반과 measurement 절반 중 어디에 속하는지입니다. return grid는 240개 mode 쌍을 120쌍씩 나누고 한 쌍의 세 길이 변형을 같은 쪽에 두므로, 2026-10-14의 manifest에서 `measurement` 360개, `tuning` 360개입니다. `placements`는 "어느 mode의 C1 task set이 어떤 id 접미사(`-s0`, `-s1`, …)로 들어갔고, 어느 segment에 label되었으며, keystroke 입력 창이 있는가"입니다. `segments`는 각 segment의 정답 label입니다. mode, `background_wanted`(그 배경 작업을 사용자가 원했는가), `tier`(process 이름이 얼마나 알아보기 쉬운가, 1–5), `pre_committed_miss`(이름과 행동만으로는 어떤 인식기도 맞힐 수 없다고 미리 선언한 segment인가)입니다.

> **코드로.** placement의 `input`은 "generator가 그 placement에 input 창을 주었는가"입니다(`gen/compose.py`: `"input": bool(windows)`). 9.21 changelog D1은 이 값이 2초 같은 짧은 segment에서, 그리고 "a mode whose C1 file has no keystroke stream (media, meeting, gaming, idle, video-edit, photo, render, transcode, backup)"에서 false라고 적습니다. 그런데 2026-10-14의 transition grid manifest를 세어 보면 `input`이 false인 placement는 gaming, idle, media, meeting 네 mode뿐이고, backup, video-edit, photo, render, transcode는 모두 true입니다. 이 다섯 mode의 C1 timeline에는 input 창이 있기 때문입니다(예: `c1-backup`의 `input: [{from: 2s, to: 275s, task: editor}]`, `c1-photo`의 `photo-editor` 창). input 창이 있으면 `input`은 true이고, 그 창의 application이 재생할 keystroke stream을 갖지 않으면 창은 있어도 키 입력 wake는 생기지 않습니다(`_dev/TODO.md`의 9.15 줄이 옮긴 9.14 D2의 인계: "keystroke streams for four applications, none for Kdenlive and GIMP"). 기록의 문장과 트리가 다르며, 현재의 사실은 트리와 코드입니다.

> **왜 이렇게 정했나.** `placements`와 `segments`는 9.21 changelog D1(2026-10-13)이 더했습니다. 이유는 둘입니다. harness는 generated 파일의 scoring 항을 C1 entry에서 규칙으로 만들어야 하는데, 그러려면 어느 C1 task set이 어떤 접미사로 어느 segment에 들어갔는지 알아야 합니다. coverage 도구는 segment마다의 label을 세야 합니다. 둘 다 compiled artifact에는 그 형태로 없고("the distractor grid's two segments are both A while B's tasks carry `-s1`"), generated timeline은 commit되지 않습니다. 그래서 "the generator writes both into the manifest's grid record"가 되었습니다. 이때 다섯 manifest는 다시 bless되었는데, `artifacts`, `demand`, `reports`는 HEAD와 section별로 비교해 바이트가 같았고 `inputs`와 `grid`만 움직였습니다.

generated 파일의 `demand_class`는 모두 `calibration`입니다(9.19 changelog D5: "every file `calibration`"). 위 return grid 파일의 `demand`는 세 segment가 0.7706, 0.4363, 1.3554이고 파일 전체가 1.0148입니다.

## 2.10 `coverage-grid.json` — manifest는 아니지만 gate가 보는 파일

`dataset/coverage-grid.json`은 hash를 담은 lockfile이 아니라 계산된 표입니다. 그래도 gate가 이 파일을 확인하므로 여기서 짚습니다. 이 파일은 `driver-table cell`마다 몇 개의 segment가 있는지를 셉니다. driver-table cell은 이 프로젝트의 configuration 표가 가진 32개 행, 즉 16개 mode × `background_wanted`의 참·거짓입니다. core set의 66개 segment 중 65개가 32개 cell에 들어가고, `c6-dual`의 `ambiguous` segment 하나가 표 밖에 있습니다. 빈 cell은 0개입니다. 그리고 9.21 이후로는 generated set마다 표가 하나씩 더 있습니다(`generated.<set>`).

`derive.py`가 이 파일을 쓰고, `derive.py --check`가 다시 계산해 비교합니다. core 표는 committed timeline에서, generated 표는 committed generated manifest의 `grid.segments`에서 계산합니다. generated timeline 자체는 commit되지 않으므로, manifest가 이 표의 유일한 committed 원천입니다.

## 2.11 무엇을 고치면 무엇이 움직이나

여기까지의 구조를 모아 표로 만듭니다. 이 표는 위의 코드(`input_files`, `generator_inputs`, variants의 `inputs`, artifact의 `meta`)를 따라 만든 것이고, 오른쪽 열의 실제 사례는 changelog에 기록된 것입니다.

| 고친 것 | core manifest | variants manifest | generated manifest 5개 | RQ0 gate spec pin | 기록된 사례 |
|---|---|---|---|---|---|
| C1이 아닌 core timeline 하나 (예: `c3-workday`) | 그 파일의 `artifacts`·`reports`·`demand` 줄 | `inputs`의 core manifest hash. 그 파일이 variant의 base면 그 variant들도 | 안 움직임 | `dataset`, `variants` | 9.20 D10: `c5-t3` → `c6-alias`, variant 78개는 바이트 동일, manifest만 이동 |
| C1 timeline 하나 (예: `c1-dev`) | 그 파일의 줄 | 위와 같음 | `inputs`의 그 C1 줄, 그 task set을 쓰는 generated artifact들 | `dataset`, `variants` | |
| variant recipe (`*.variant.yaml`) | 파생 timeline이 바뀌어 그 파일들의 줄 | 위와 같음 | 안 움직임 (C1 파일은 파생 파일이 아님) | `dataset`, `variants` | |
| `archetypes.yaml` (주석 하나라도) | `inputs`와 모든 artifact | `inputs` 두 줄과 모든 variant | `inputs`와 모든 artifact | `dataset`, `variants` | |
| `compile.py` 또는 `wlc/*.py` (출력이 같아도) | `inputs` | `inputs`의 core hash | `inputs` | `dataset`, `variants` | 9.22 D5: `inputs`만 이동, artifact 동일 |
| schema, stimulus stream, replay stream | `inputs`, 그리고 그 stream을 쓰는 artifact | `inputs`의 core hash, 해당 variant | `inputs`, 해당 artifact | `dataset`, `variants` | |
| launch stream (`dataset/launch/`) | `inputs`는 안 움직임, 해당 artifact만 | 해당 variant | 해당 artifact | 해당 artifact가 있으면 | 2.4의 열린 자리 |
| `variants.yaml` | 안 움직임 | `inputs`와 해당 variant | 안 움직임 | `variants` | |
| `grids.yaml`, `generate.py`, `gen/*.py` | 안 움직임 | 안 움직임 | `inputs`, 출력이 바뀌면 artifact와 `grid` | 지금은 없음 (generated를 pin한 spec이 없음) | 9.21 D1(grid record에 placements를 더해 다섯 manifest가 `inputs`와 `grid`만 움직임), 9.20 D10(generator가 바뀌어 앞 세 set의 `inputs`만 움직임) |
| generated timeline의 머리 주석 문구 | 안 움직임 | 안 움직임 | 모든 generated artifact (`derived_from`) | 없음 | 9.20 D10(머리 주석 문구 때문에 모든 generated artifact가 바뀌었다가 되돌림) |

마지막 행은 실제로 일어난 일입니다. 9.20 changelog D10은 이렇게 적습니다. "A first run had changed every generated artifact through `meta.derived_from` because the generated files' header comment had been reworded ('composed or renamed'); the wording was restored and the sets regenerated — the header is part of the timeline bytes the artifact pins." generated timeline 맨 위의 주석 한 줄을 다듬었더니 generated artifact의 hash가 전부 바뀐 것입니다. 주석도 timeline 바이트의 일부이고, artifact는 timeline의 git blob hash를 적기 때문입니다.

## 2.12 손으로 따라가는 예: `wlc/grid.py`를 고쳤다면

9.21의 D2(coverage table을 generator 옆에 둔 결정)는 이 표가 실제로 어떻게 작동하는지 보여 주는 사례입니다. changelog의 서술을 그대로 따라갑니다.

1. 9.21은 generated layer의 coverage table을 만들어야 했습니다. 첫 구현은 그 코드를 core set의 grid 코드가 있는 `dataset/tools/wlc/grid.py`에 넣었습니다.
2. dataset test suite를 돌리자 `test_manifest_pins_the_compile_inputs_by_content`가 실패했습니다. 이 test는 committed core manifest의 `inputs`가 지금 디스크의 파일 hash와 같은지 확인합니다. `wlc/grid.py`가 바뀌었으니 같지 않았습니다.
3. 이것을 통과시키려면 core manifest를 다시 bless해야 합니다. 그러면 core manifest의 hash가 바뀌고, variants manifest의 입력이 바뀌어 그것도 다시 bless해야 하고, RQ0 gate spec의 두 pin을 다시 적어야 합니다. 9.21 spec decision 9는 "the core set's and the variants' manifests are unchanged"라고 적고, spec의 불변식은 "The schema, the compiler, the lints and every artifact are unchanged"라고 적습니다. compiler의 source를 건드리는 것 자체가 이 둘에 어긋났습니다.
4. 그래서 코드를 `dataset/tools/gen/coverage.py`로 옮겼습니다. generated manifest는 `gen/*.py`를 pin하고 core manifest는 pin하지 않습니다. `wlc/grid.py`는 9.20의 바이트로 되돌렸습니다.

changelog는 이유를 이렇게 적습니다. "because the core set's manifest pins `wlc/*.py` by content (9.18 decision 5) — any edit there moves the core manifest and, through it, the variants manifest and the RQ0 gate spec's dataset pin, against the spec's invariant." `gen/coverage.py`의 docstring에도 같은 말이 남아 있습니다. "This module lives beside the generator, not in `wlc`, because the core set's manifest pins `wlc/*.py` by content". 코드를 어느 디렉터리에 두느냐가 어떤 lockfile을 움직이느냐를 결정하는 셈입니다. 웹 개발로 치면, monorepo에서 공용 package를 건드리면 그것에 의존하는 모든 package의 lockfile과 cache가 무효화되므로 변경을 의존 범위가 좁은 쪽에 두는 것과 같은 판단입니다.

---

# 3장 · Bless와 pin: 누가 무엇을 고정하나

## 3.1 이 장의 질문

2장은 manifest가 무엇을 담는지 보았습니다. 이 장은 "manifest를 누가, 언제 바꾸고, 그 변화가 실험 쪽에서 어떻게 붙잡히나"를 묻습니다. 이 저장소의 기록에는 두 동사가 계속 나옵니다. `bless`와 `pin`입니다. 둘은 비슷해 보이지만 고정하는 주체와 대상이 다릅니다. bless는 dataset이 자기 build를 고정하는 행위이고, pin은 실험 사양이 dataset의 manifest를 고정하는 행위입니다. 이 구분을 놓치면 "manifest를 commit했는데 왜 harness CI가 실패하나" 같은 상황을 이해할 수 없습니다.

## 3.2 Bless: build를 다시 돌려 manifest를 commit하는 것

이 저장소에서 `bless`는 "build를 다시 돌려 manifest를 새로 쓰고, 그 manifest를 commit하는 것"을 뜻합니다. 그리고 `blessed build`는 "디스크의 `build/`가 committed manifest와 hash 단위로 일치하는 상태의 build"를 뜻합니다. 이 정의는 어느 용어 문서에 따로 적혀 있지 않고, 코드와 기록의 쓰임에서 나옵니다.

- gate가 manifest 불일치를 보고할 때의 메시지가 "the build wrote a manifest that differs from the committed one — re-bless (commit it) if the change is intended"입니다(`dataset/tools/check_build.py`). 즉 re-bless는 "새로 쓰인 manifest를 commit하라"입니다.
- README의 layout 설명은 `build.manifest.json`을 "lockfile: hashes of the last blessed build"라고 부릅니다.
- 9.13 changelog D7의 제목이 "the bless"이고, 그 내용은 "The dataset target's two steps — the deriver, then the compiler … — run on the final library … 51 artifacts under `coreset-single/` alone, `dataset/build.manifest.json` rewritten"입니다.

bless의 절차를 순서대로 쓰면 이렇습니다.

```
1. 입력을 고친다                (timeline, library, compiler, grids.yaml …)
2. make dataset variants generated   → build/ 를 다시 쓰고, 일곱 manifest를 다시 쓴다
3. git diff dataset/build*.manifest.json   → 무엇이 움직였는지 본다
4. 의도한 변화면 manifest를 commit한다    ← 이것이 bless
5. make check                    → build/ 가 committed manifest와 같은지 확인
```

3단계가 실제로 중요합니다. manifest의 diff는 변화의 범위를 정확히 보여 줍니다. 예를 들어 compiler의 속도만 고쳤다면 diff는 `inputs`의 몇 줄뿐이어야 합니다. 9.22 changelog D5가 바로 이 확인을 기록했습니다. "every artifact, report and variant is byte-identical to the 9.18 build (the diff of the two manifests against `HEAD` is the `inputs` section alone)". 반대로 diff에 `artifacts` 줄이 섞여 있다면, 속도만 고쳤다고 생각한 수정이 출력을 바꾼 것입니다.

> **코드로.** bless를 하는 별도의 명령은 없습니다. `make dataset`, `make variants`, `make generated`가 각각 manifest를 쓰고(`compile.py`, `variants.py`, `generate.py`의 write 경로), commit은 사람이 git으로 합니다. 거꾸로 말하면, build를 돌리기만 하고 commit하지 않은 상태가 언제든 생길 수 있고, 그 상태를 잡는 것이 4장의 `check_committed`입니다.

## 3.3 Pin: 실험 사양이 manifest를 고정하는 것

`pin`은 "다른 파일이 이 파일의 SHA-256을 적어 두고, 실행 전에 그 값이 지금의 바이트와 같은지 확인하는 것"을 뜻합니다. dataset 바깥에서 dataset을 pin하는 파일은 지금 하나입니다. RQ0 gate spec(`harness/experiments/rq0-gate.yaml`)입니다. 이 파일은 RQ0 실험의 사전 등록을 harness가 실행할 수 있는 데이터로 적은 것으로, 조건, seed 수, 판정 파일 목록, 판정 기준, 보고 항목과 함께 맨 아래에 `pins` block을 가집니다. 2026-10-14의 block은 이렇습니다.

```yaml
pins:
  scoring_spec: {path: harness/scoring/scoring-spec.yaml, sha256: 0ff71b1ff946f5e45dceea3c13b4008d32a13255ed637d46989a2867b7474bbc}
  guard_spec:   {path: harness/guards/guard-spec.yaml, version: "1.1", sha256: 24ccb875ff666615de75d80bc5351b7f5c62713d605438844938f9ab6ef1676c}
  driver_table: {path: daemon/driver-table/prior.yaml, sha256: 6e271dd042b38c23b85459cec7545fde990aec9be5a2c8bd6081690d98243f7f}
  dataset:      {path: dataset/build.manifest.json, sha256: fad7192d2a290c9d0b9f9563a45a0f9834b8c48403c4c88d84ae1869107accd3}
  variants:
    all: {path: dataset/build.variants.manifest.json, sha256: 03f14b2c5520edaf304915a2c773f8ac30436a9f88ea9cd2d8b319949c3605d5}
```

다섯 pin을 하나씩 풀면 이렇습니다.

- `scoring_spec` — 파일별로 어떤 성능 항(term)을 어떤 가중치로 점수에 넣을지 정한 frozen 파일입니다.
- `guard_spec` — run의 숫자를 읽기 전에 run이 통과해야 하는 여덟 개 연구 전반의 guard와 그 임계값을 적은 frozen 파일입니다.
- `driver_table` — `prior table`, 즉 측정 전에 scheduling 이론으로 쓴 configuration 표입니다. 32개 행(mode × `background_wanted`)마다 configuration을 하나씩 적습니다. RQ0 gate는 이 표로 돌아갑니다.
- `dataset` — core manifest입니다.
- `variants.all` — variants manifest입니다.

2026-10-14에 이 다섯 경로의 파일을 `shasum -a 256`으로 계산해 보면 다섯 값 모두 pin과 같습니다. 즉 지금 저장소의 상태는 RQ0 gate spec이 사전 등록한 상태와 일치합니다.

pin이 dataset에 대해 무엇을 보장하는지 따라가 봅시다. pin은 manifest 파일의 hash만 적습니다. 그런데 manifest는 artifact 51개의 hash를 적고, artifact는 자신이 나온 timeline과 library의 git blob hash와 seed를 적습니다. 그러므로 pin 한 줄이 51개 artifact의 모든 바이트를, 그리고 간접적으로 그 바이트를 만든 입력까지를 고정합니다.

```
rq0-gate.yaml  pins.dataset.sha256 = fad7192d…
   └─ build.manifest.json (그 바이트의 SHA-256이 fad7192d…)
        ├─ inputs:    archetypes.yaml → c6af7623…, wlc/compiler.py → 35d1bcee…, …
        └─ artifacts: coreset-single/c1-dev.workload.json → <sha256>
                        └─ meta.derived_from = …c1-dev.timeline.yaml@cbf1349a…
                           meta.sampled      = archetypes.yaml@a2cc1957…, seed 107
```

이것은 git이 commit hash 하나로 tree 전체를 고정하는 방식, 즉 Merkle tree와 같은 구조입니다. 위쪽의 hash 하나가 같으면 그 아래 전부가 같습니다.

> **왜 이렇게 정했나.** RQ0 gate spec의 머리 주석은 이 파일이 어떻게 바뀔 수 있는지를 적습니다. "Nothing changes after execution begins except by an entry in harness/CHANGELOG.md made before any run." 그리고 `docs/terminology.md`의 per-experiment spec 정의는 "hash pins of the scoring spec, guard spec, driver table, and dataset"을 사전 등록의 일부로 듭니다. pin의 목적은 사전 등록 이후에 판정의 재료(점수 규칙, guard, configuration 표, workload)가 몰래 바뀌는 것을 막는 것입니다. 실행이 시작된 뒤에는 pin을 바꿀 수 없고, 실행 전에 바꾸려면 harness changelog에 항목을 남겨야 합니다.

## 3.4 Re-pin의 절차

`re-pin`은 dataset이 다시 bless되어 manifest의 hash가 바뀌었을 때, RQ0 gate spec의 `pins` 값을 새 hash로 고쳐 적는 것입니다. 기록에 남은 절차는 매번 같습니다.

1. dataset을 다시 bless합니다(3.2).
2. `shasum -a 256 dataset/build.manifest.json dataset/build.variants.manifest.json`으로 새 hash를 얻습니다.
3. `harness/experiments/rq0-gate.yaml`의 `pins.dataset`과 `pins.variants.all`을 고칩니다.
4. `harness/CHANGELOG.md`에 항목을 하나 씁니다. 무엇이 왜 바뀌었는지, 새 hash가 무엇인지를 적습니다.
5. `make -C harness lint`로 pin이 맞는지 확인합니다.

4단계의 changelog는 형식이 아니라 규칙입니다. `harness/CHANGELOG.md`의 머리말은 "a change to either after its freeze is an entry below before any run reads it, and the RQ0 gate spec (`experiments/rq0-gate.yaml`) pins the frozen bytes by hash"라고 적습니다. 2026-10-14의 changelog에는 dataset pin이 움직인 항목이 2026-10-09(9.14), 2026-10-11(9.17, 9.18, 9.22 세 번), 2026-10-12(9.20)에 있습니다.

## 3.5 Pin이 맞지 않으면 무엇이 실패하나

pin을 확인하는 코드는 `harness/tools/harness/evaluator.py`의 `_pin_errors`입니다. 이 함수는 `scoring_spec`, `guard_spec`, `driver_table`, `dataset` 네 이름과, `variants` 아래의 모든 이름, `generated` 아래의 모든 이름을 돌며 각 경로의 파일을 SHA-256으로 계산해 pin과 비교합니다. 다르면 이런 줄을 냅니다.

```
pins/dataset: sha256 <지금 파일의 hash> of dataset/build.manifest.json != pinned fad7192d2a29…
```

이 함수는 두 곳에서 불립니다. 하나는 `make -C harness lint`가 부르는 `tools/experiment_lint.py`이고, 다른 하나는 실험이 끝난 뒤 판정을 쓰는 RQ0 gate evaluator입니다. experiment lint의 출력은 spec마다 요약 한 줄과 오류 줄들입니다. 예를 들어 dataset만 다시 bless하고 re-pin을 잊었다면 다음과 같은 모양이 됩니다(형식은 `experiment_lint.py`의 `print` 문 그대로, hash는 예시).

```
rq0-gate.yaml: experiment rq0-gate, 3 conditions, 19 judging + 32 reporting files, criterion k_of_n_gap
  pins/dataset: sha256 9a1b…(새 값) of dataset/build.manifest.json != pinned fad7192d…
  pins/variants/all: sha256 4c2d…(새 값) of dataset/build.variants.manifest.json != pinned 03f14b2c…
2 error(s)
```

variants pin도 함께 실패한다는 점에 주의합니다. variants manifest의 입력이 core manifest의 hash이므로, core를 다시 bless하면 variants manifest도 다시 써지고 hash가 바뀝니다(2.8).

이 실패는 CI에서 어느 단계에서 보일까요. `harness.yml`은 dataset을 build하고 `make -C dataset check`를 한 뒤에 `make -C harness lint`를 돌립니다(6장). 그러니 manifest를 commit하지 않았다면 dataset check에서 먼저 멈추고, manifest는 commit했지만 re-pin을 잊었다면 dataset check는 통과하고 harness lint에서 멈춥니다. 두 실패가 서로 다른 단계에서 나므로, 어느 단계에서 멈췄는지가 곧 무엇을 잊었는지를 알려 줍니다.

## 3.6 `pins.generated`와 `files.select`

generated manifest 다섯 개는 지금 어떤 실험 사양도 pin하지 않습니다. RQ0 gate spec은 judging과 reporting 목록을 파일 이름으로 직접 적고, generated 파일을 쓰지 않습니다. 하지만 나중의 실험(전환 인식을 묻는 RQ1, 짧은 상황 변화의 비용을 묻는 RQ4)은 generated set을 쓸 것이고, 그때를 위한 장치가 9.21에서 미리 만들어졌습니다.

9.21 spec decision 6은 "An experiment spec selects files from a manifest by its axes, built now"라고 정했습니다. 실험 사양의 `files` 아래에 `select`를 쓰면, harness가 pin된 generated manifest의 `grid` record를 읽어 조건에 맞는 파일 id 목록으로 펼칩니다. `harness/experiments/README.md`의 예는 다음과 같습니다.

```yaml
files:
  select: [{manifest: return-grid, where: {split: measurement}}]   # 추가로 reporting에 들어감
pins:
  generated: {return-grid: {path: dataset/build.return-grid.manifest.json, sha256: …}}
```

`where`는 `grid` record의 key와 값입니다. `split: measurement`(return grid나 flap-stress의 measurement 절반), `form: focus`(transition grid의 한 형태), `tier: 5`(ladder의 한 단계) 같은 조건을 씁니다. 펼쳐진 파일은 언제나 `reporting`에 들어가고 `judging`에는 들어가지 않습니다(9.21 spec의 불변식: "Every generated file is reporting material"). harness 쪽 구현은 `harness/tools/harness/manifests.py`의 `select`와 `expand`이고, 존재하지 않는 key를 `where`에 쓰면 "the manifest's records carry no key …"라는 `KeyError`로 거부합니다.

> **왜 이렇게 정했나.** 9.21 spec decision 6은 이 장치를 RQ1이나 RQ4의 spec session으로 미루지 않고 지금 만든다고 적었습니다("Not deferred to the RQ1 or RQ4 experiment spec sessions"). decision 5는 generated 파일의 좌표를 records의 열로 만들지 않고 manifest join으로 읽는다고 정했습니다. "The file-level axes reach the harness by a manifest join; the records are unchanged … the manifest pinned by the spec as the RQ0 gate spec pins the dataset's." 이렇게 하면 generated manifest 하나를 pin하는 것만으로 그 실험이 쓰는 파일 집합과 그 좌표가 함께 고정됩니다. 파일 목록을 손으로 적지 않으므로, 1,562개 중 수백 개를 고르는 실험에서도 사전 등록이 manifest hash 한 줄로 끝납니다.

## 3.7 Pin의 역사

RQ0 gate spec의 dataset과 variants pin이 지금까지 어떻게 움직였는지를 harness changelog와 sub-task changelog에서 모읍니다. 각 줄은 dataset을 다시 bless하게 만든 원인과 함께 적습니다.

| 날짜 | sub-task | core manifest | variants manifest | 무엇이 바뀌었나 |
|---|---|---|---|---|
| 2026-10-09 | 9.14 (소비자 재작업) | `c3767e10…` | `2a8893a9…` | 9.13의 rebuild 위에서 demand를 segment별로 기록. artifact는 변화 없음. variant 78개가 처음 생김 |
| 2026-10-11 | 9.17 (focus를 telemetry에) | `625e431f…` | `328560cf…` | 모든 artifact에 `focus` key가 생겨 51개 artifact가 모두 바뀜 |
| 2026-10-11 | 9.18 (compiler, schema, build gate) | `976a943c…` | `6c244f17…` | 모든 timeline에 `source` map이 생겨 `derived_from`이 모두 바뀜. 파생 파일의 keystroke가 base의 slice가 됨. `inputs`에 compiler와 stream, `reports` section 추가 |
| 2026-10-11 | 9.22 (build 시간) | `d10bcd42…` | `831a854e…` | compiler 세 파일 수정. `inputs`만 이동, artifact 동일 |
| 2026-10-11 | 9.19 (generator, C3 grid) | 변화 없음 | 변화 없음 | generated manifest 세 개가 새로 생김 |
| 2026-10-12 | 9.20 (C4·C5 grid) | `fad7192d…` | `03f14b2c…` | `c5-t3`가 `c6-alias`로 이름이 바뀜. 50개 artifact와 78개 variant는 동일 |
| 2026-10-13 | 9.21 (generated layer 소비자) | 변화 없음 | 변화 없음 | scoring spec만 re-freeze (`0ff71b1f…`) |

이 기간에 scoring spec pin은 `5d8a3243…`(9.14) → `1f7e9e30…`(9.18, 주석만) → `9cd9a155…`(9.20) → `0ff71b1f…`(9.21, 머리글의 규칙 문장)으로 움직였습니다. guard spec(`24ccb875…`)과 driver table(`6e271dd0…`)은 9.14 이후 그대로입니다.

generated manifest의 hash도 같은 방식으로 기록되어 있습니다(각 sub-task changelog). 어떤 실험도 이것을 pin하지 않지만, 9.16(최종 audit)이 이 값들을 재현 대상으로 받습니다.

| set | 9.19 (2026-10-11) | 9.20 (2026-10-12) | 9.21 (2026-10-13, 현재) |
|---|---|---|---|
| transition grid | `899efa53…` | `593dc23a…` | `e26aa8e6…` |
| return grid | `7a758f6e…` | `183deedb…` | `21826be3…` |
| flap-stress | `8c4c6fce…` | `d2686e73…` | `a8c271dd…` |
| distractor grid | — | `7236f4b2…` | `6d9192db…` |
| familiarity ladder | — | `0b8b76ce…` | `2cb56e69…` |

9.20에서 앞의 세 set이 다시 bless된 이유는 generator(`grids.yaml`, `gen/cells.py`, `gen/compose.py`, `generate.py`)가 바뀌어 `inputs`가 움직였기 때문입니다. artifact, report, demand, grid record는 바이트가 같았습니다(9.20 changelog D10). 9.21에서는 다섯 set 모두 `inputs`(generator source)와 `grid`(placements와 segments 추가)만 움직였습니다(9.21 changelog D1). 2026-10-14에 일곱 manifest의 SHA-256을 계산하면 표의 "현재" 열 및 RQ0 pin과 모두 같습니다.

---

# 4장 · Gate: `make check`와 네 개의 `--check`

## 4.1 이 장의 질문

이 장은 "무엇이 build를 committed manifest와 비교하고, 무엇이 다르면 어떤 메시지로 실패하나"를 묻습니다. 이 저장소에서 `gate`라는 말은 `make -C dataset check`를 가리킵니다. Makefile 주석이 "CI gate"라고 부르고, README가 "the gate"라고 부릅니다. 그 밖에 `--check`라는 같은 이름의 flag를 가진 도구가 네 개 있는데, 그중 하나만 gate 안에 있고 셋은 gate 밖에 있습니다. 이 구분이 이 장의 뼈대입니다.

## 4.2 Gate의 정의: build가 재현을 증명하고, check는 비교한다

`dataset/Makefile`의 `check` target은 두 줄입니다.

```make
check:              ## CI gate, after `dataset variants generated`: derived files, grid (all 32 cells), every manifest equal to its committed bytes, build/ equal to their union
	$(PY) tools/derive.py --check --require-coverage
	$(PY) tools/check_build.py
```

이 두 줄이 지금의 모양이 된 것은 2026-10-11입니다. 그 전에는 gate가 build 전체를 메모리에서 다시 compile했습니다. 역사를 짧게 정리합니다.

| 시점 | `make check`가 한 일 | 문제 |
|---|---|---|
| 2026-10-10 이전 | derive drift, `compile.py --check`(메모리에서 다시 compile해 manifest와 비교) | audit A4: 디스크의 `build/`는 hash하지 않음, variants는 어떤 workflow에서도 검사하지 않음, manifest가 입력 두 개만 pin, CI가 이 manifest를 한 번도 compile한 적 없음 |
| 2026-10-11, 9.18 | derive drift, `compile.py --check`, `variants.py --check`, `check_build.py`(디스크의 `build/`가 두 manifest의 합집합과 같은지) | 집 기계에서 56분 27초. CI 한 run이 약 3.5시간 |
| 2026-10-11, 9.22 이후 | derive drift, `check_build.py`(각 manifest가 committed 바이트와 같은지 + `build/`가 합집합과 같은지) | — |

> **왜 이렇게 정했나.** 9.22 spec decision 1의 문장은 "The build step proves reproducibility; `check` compares"입니다. 원문 전체는 "`make dataset variants` rewrites the two manifests; `make check` is derive drift, both manifests equal to their committed bytes, and `build/` equal to the manifests. The in-memory recompile flags of `compile.py` and `variants.py` remain for independent verification and leave the gate." 이유는 9.18의 검증 run이 보여 준 중복입니다. 9.18 changelog D7과 9.22 spec의 머리말은 "`lint`, `dataset`, `test` and `check` each compile it, 3.5 h a run"이라고 적습니다. 한 CI run 안에서 같은 set을 네 번 compile하고 있었던 것입니다. 9.22 changelog D1은 새 방식이 같은 것을 증명한다고 설명합니다. "The build step rewrote the manifests, so equality states that the recompile reproduces the committed set — the same statement the in-memory flags made at twice the compile." build 단계가 이미 manifest를 새로 썼으니, 그 manifest가 committed 것과 같다는 것은 곧 다시 compile한 결과가 committed set을 재현했다는 뜻입니다. 같은 명제를 compile 한 번으로 증명합니다.

그래서 gate는 반드시 build 다음에 돌아야 합니다. Makefile 주석의 "after `dataset variants generated`"가 그 뜻입니다. build를 돌리지 않고 `make check`만 돌리면, 디스크의 manifest는 지난번 build가 쓴 것이고, `build/`도 지난번 것입니다. 그 둘이 committed manifest와 같으면 gate는 통과하지만, 그것은 "지난번 build가 committed와 같았다"는 뜻일 뿐 "지금의 입력이 committed를 재현한다"는 뜻은 아닙니다.

## 4.3 `derive.py --check --require-coverage`

gate의 첫 줄은 세 가지를 확인합니다.

**하나, 파생 timeline이 그 recipe와 같은가.** core set의 파일 중 일부는 다른 파일에서 파생됩니다. `dataset/timelines/coreset/*.variant.yaml` 다섯 개가 recipe이고, `deriver`(`wlc/deriver.py`)가 base timeline에 op들(`rename`, `patch-segment`, `patch-task`, `add-task`, `set-segments`, `set-input`, `set-focus`, `set-operations`, `patch-meta`)을 적용해 파생 timeline을 씁니다. 파생 timeline은 commit되고, 첫 줄에 `# GENERATED by dataset/tools/derive.py from <spec> — do not hand-edit.`이라는 머리글이 붙습니다. `--check` mode에서는 recipe에서 다시 만든 바이트와 디스크의 파일을 비교하고, 다르면 이렇게 보고합니다.

```
1 error(s):
  - c7-dev.timeline.yaml: differs from its variant spec (derive drift)
```

파일이 아예 없으면 `c7-dev.timeline.yaml: missing (derive drift)`입니다.

**둘, `coverage-grid.json`이 timeline과 generated manifest에서 다시 계산한 표와 같은가.** 다르면 `coverage-grid.json differs from the timelines and the generated manifests (grid drift)`입니다.

**셋, 32개 driver-table cell이 모두 core set의 segment를 하나 이상 가지는가.** 이것이 `--require-coverage`입니다. 앞의 두 확인이 오류 없이 끝났을 때만 돌고, 빈 cell이 있으면 `coverage: 1 empty driver-table cell(s) — office/false`처럼 빈 cell을 모두 이름으로 적습니다(`wlc/grid.py`의 `coverage_errors`, cell 이름은 `<mode>/<true|false>`).

> **왜 이렇게 정했나.** 빈 cell을 CI 실패로 만든 것은 Phase 7 spec decision 11(2026-09-09)입니다. 2026-09-11의 Phase 7 기록은 그 이유를 "Report-only was rejected as the failure mode of August"라고 적습니다. building plan §3은 그 8월의 실패를 구체적으로 적습니다. "before it the tool counted mode × tier only, which is how the attribute's `false` side went unfilled". 즉 보고만 하던 시절에 `background_wanted`가 거짓인 쪽 cell들이 비어 있는 채로 지나갔고, 그래서 이제는 빈 cell이 build를 멈춥니다. 단, generated layer의 표에는 빈 cell 규칙이 적용되지 않습니다. 9.21 spec decision 4는 "No empty-cell rule applies to it: the sets' full enumeration is asserted by the generator's tests, and the ladder fills one cell per mode by design"이라고 적습니다.

2026-10-14에 이 줄을 돌린 실제 출력의 앞부분입니다(0.6초).

```
verified — 66 segments on the grid
cell                t1  t2  t3  t4  t5  segs  miss
browsing/true        5   0   0   0   0     5     0
browsing/false       1   0   0   0   0     1     0
office/true          0   3   0   0   0     3     0
…
idle/false           0   1   0   0   0     1     0
outside the grid: ambiguous ×1 (c6-dual, tier 3)
total segments: 66 (65 on the grid, 1 outside)
empty cells: 0
generated distractor-grid: 272 files, 544 segments
…
```

## 4.4 `check_build.py`

gate의 둘째 줄이 이 권의 중심입니다. 114줄짜리 파일이고, 두 함수가 두 가지를 확인합니다. 아무것도 쓰지 않습니다.

**`manifests(root)` — 어떤 manifest를 볼 것인가.** 고정된 두 개(`dataset/build.manifest.json`, `dataset/build.variants.manifest.json`)에, `dataset/grids.yaml`의 `sets` 아래 이름마다 `dataset/build.<name>.manifest.json`을 더합니다. generated set을 새로 정의하면 그 manifest가 자동으로 gate의 대상이 됩니다.

**`check_committed(root)` — 디스크의 manifest가 commit된 manifest와 같은가.** 각 manifest를 `git show HEAD:<path>`로 읽은 바이트와 디스크의 바이트로 비교합니다. 세 가지 오류가 있습니다.

| 상황 | 메시지 |
|---|---|
| 디스크에 manifest가 없음 | `` <path>: missing (run `make dataset variants generated` first) `` |
| git의 HEAD에 그 manifest가 없음 | `<path>: not in git at HEAD` |
| 둘이 다름 | `<path>: the build wrote a manifest that differs from the committed one — re-bless (commit it) if the change is intended` |

**`check(root)` — `build/`가 모든 manifest의 합집합과 같은가.** 모든 manifest의 `artifacts`와 `reports`를 하나의 `{build/ 아래 경로: sha256}` map으로 모읍니다(variants manifest의 record에서는 `sha256` field를 꺼냅니다). 그 다음 `build/` 아래의 모든 파일을 찾아 세 방향으로 비교합니다.

| 상황 | 메시지 |
|---|---|
| `build/` 디렉터리가 없음 | `` dataset/build: missing (run `make dataset variants generated` first) `` |
| manifest에는 있는데 디스크에 없음 | `build/<path>: pinned by a manifest, missing on disk` |
| 디스크에는 있는데 어떤 manifest에도 없음 | `build/<path>: on disk, pinned by no manifest` |
| 둘 다 있는데 hash가 다름 | `build/<path>: sha256 <앞 12자리>… differs from the pinned <앞 12자리>…` |

마지막으로 오류가 있으면 `N build error(s):` 아래에 모든 오류를 적고 exit 1, 없으면 `build verified (<파일 수> files, <manifest 수> manifests)`를 적고 exit 0입니다. 오류는 `check_committed`의 것이 먼저, `check`의 것이 나중에 나오고, `check` 안에서는 "없음", "고정되지 않음", "hash 다름" 순서로 각각 경로 순으로 나옵니다.

> **왜 이렇게 정했나.** 디스크의 `build/`를 직접 hash하게 한 것은 9.18 spec decision 6입니다. "`check` verifies the on-disk build … `build/` equal to the two manifests — every file in `build/` matching an entry, every entry present, no file in neither. A missing `build/` fails." 근거는 audit A4의 첫 구절 "`make check` compares an in-memory manifest to the committed one and never hashes `build/` on disk"입니다. 그 전의 gate는 "지금 compile하면 committed manifest와 같은 것이 나온다"까지만 확인했고, simulator와 harness가 실제로 읽는 디스크의 파일이 그것과 같은지는 확인하지 않았습니다. 디스크의 파일은 예전 build의 찌꺼기일 수도, 손으로 고친 것일 수도 있습니다. 세 방향 비교 중 "고정되지 않은 파일"을 실패로 보는 것도 같은 이유입니다. harness는 `build/coreset-single/*.workload.json`을 glob으로 읽는 곳이 있어서(`harness/tools/tests/test_mock_daemon.py`가 `@`가 없는 파일을 세어 51개인지 확인합니다), 남은 파일 하나가 실험의 입력에 섞일 수 있습니다.

> **왜 이렇게 정했나.** manifest를 `git show HEAD:<path>`와 비교하는 `check_committed`는 9.22 spec decision 1이 더했습니다. 9.22 changelog D1의 서술은 "it is derive drift and `check_build.py`, which now also compares each manifest on disk with its bytes at `HEAD` (`check_committed`: `git show HEAD:<path>`)"입니다. 이것이 메모리에서의 재compile을 대신합니다.

이 동작을 직접 보이기 위해, 이 권을 쓰면서 scratchpad 안에 manifest 두 개와 파일 두 개만 가진 작은 git 저장소를 만들고 실제 `check_build.py`를 `--repo`로 그곳에 돌려 보았습니다. 출력은 그대로입니다.

```
--- 1. 깨끗한 상태
build verified (2 files, 2 manifests)
exit 0

--- 2. build/에 고정되지 않은 파일 하나를 두고, core manifest 끝에 공백 하나를 더함
2 build error(s):
  - dataset/build.manifest.json: the build wrote a manifest that differs from the committed one — re-bless (commit it) if the change is intended
  - build/coreset-single/c5-t3.workload.json: on disk, pinned by no manifest
exit 1

--- 3. build/ 디렉터리를 치움
2 build error(s):
  - dataset/build.manifest.json: the build wrote a manifest that differs from the committed one — re-bless (commit it) if the change is intended
  - dataset/build: missing (run `make dataset variants generated` first)
exit 1
```

그리고 2026-10-14에 이 저장소의 실제 build에 돌린 결과는 `build verified (3304 files, 7 manifests)`, 6.0초였습니다. 6.8 GB를 모두 SHA-256으로 읽는 시간입니다.

> **코드로.** `dataset/tools/tests/test_check_build.py`의 네 test가 이 동작을 고정합니다. 일치하면 통과(`test_a_build_equal_to_the_manifests_passes`), `build/`가 없으면 정확히 위 메시지 한 줄(`test_a_missing_build_fails`), 없는 파일·고정되지 않은 파일·hash가 다른 파일이 각각 이름으로 보고됨(`test_a_missing_pinned_file_an_unpinned_file_and_a_drifted_file_are_each_named`), `grids.yaml`이 set을 정의하면 그 manifest가 합집합에 들어가고 아직 쓰이지 않은 manifest는 아무것도 고정하지 않음(`test_a_generated_sets_manifest_joins_the_union_when_the_grid_definition_names_it`)입니다. 이 test들은 `check()`만 부르고 `check_committed()`는 부르지 않습니다. git 저장소가 필요한 쪽은 test가 직접 다루지 않습니다.

## 4.5 Gate 밖의 세 `--check`

`compile.py`, `variants.py`, `generate.py`는 모두 `--check` flag를 가집니다. 셋 다 같은 일을 합니다. build를 메모리에서 다시 하고, 만들어질 manifest의 바이트를 디스크의 committed manifest와 비교하며, artifact는 쓰지 않습니다.

| 명령 | 통과 시 출력 | 실패 시 출력 |
|---|---|---|
| `compile.py --check` | `manifest verified (51 artifacts)` | `build.manifest.json drift: recompiled artifacts do not match the committed manifest` |
| `variants.py --check` | `variants manifest verified (78 artifacts)` | `build.variants.manifest.json drift: rebuilt variants do not match the committed manifest` |
| `generate.py --check` | `<set>: manifest verified (<N> artifacts)` (set마다) | `build.<set>.manifest.json drift: the regenerated set does not match the committed manifest` |

committed manifest가 아예 없으면 셋 다 "no committed manifest to check against" 꼴의 메시지로 실패합니다.

> **코드로.** `generate.py --check`는 artifact와 manifest는 쓰지 않지만, generated timeline은 디스크에 씁니다. `write_timelines`가 `--check` 분기보다 먼저 돌기 때문입니다(바뀐 파일만 다시 쓰고, 정의에 없는 오래된 timeline은 지웁니다). generated timeline은 commit되지 않는 build product이므로 이것이 문제가 되지는 않지만, "`--check`는 아무것도 쓰지 않는다"는 말은 `derive.py --check`와 `check_build.py`에만 정확합니다.

이 세 flag가 gate에서 빠진 뒤에도 남은 이유는 9.22 spec decision 1의 "remain for independent verification"입니다. 실제 쓰임은 기록에 이렇게 남아 있습니다.

- 2026-10-10 audit는 `make check`(당시는 재compile 포함, 1,517초)와 `variants.py --check`(2,098초)로 집 기계에서 set이 바이트 단위로 재현됨을 확인했습니다.
- 9.19 changelog D5는 generated set 세 개를 `generate.py --check`로 2분 15초에 재현했습니다.
- 9.16(최종 audit, 아직 열림)의 TODO 줄은 각 sub-task가 넘긴 재현 확인을 이 flag들로 적습니다. 예를 들어 "the variants manifest reproduces from `dataset/variants.yaml`, the library and the blessed manifest with `dataset/tools/variants.py --check`"입니다.

웹 개발로 비유하면, gate의 `check_committed`는 CI에서 "lockfile이 바뀌었는데 commit되지 않았나"를 보는 검사이고, 세 `--check`는 "lockfile을 지우고 처음부터 resolve해도 같은 lockfile이 나오나"를 별도로 보는 재현성 검사입니다. 후자는 비싸서 매 push마다 돌리지 않고, audit 같은 때에 돌립니다.

## 4.6 손으로 따라가는 실패들

이제 "X를 고치고 Y를 잊으면 무엇이 실패하고 무엇을 출력하나"를 하나씩 따라갑니다. 각 사례에서 집 기계의 순서와 CI의 순서를 나누어 봅니다. CI의 순서는 `dataset.yml` 기준으로 `lint` → `dataset` → `variants` → `generated` → `test` → `check`입니다(6장). 메시지는 모두 위의 코드에서 그대로 옮긴 것입니다.

### 사례 1. timeline을 고치고 build를 돌렸지만 manifest를 commit하지 않았다

`c3-workday.timeline.yaml`의 한 task arrive 시각을 바꾸고 `make dataset variants generated`를 돌린 뒤, timeline만 commit하고 manifest는 commit하지 않았다고 합시다.

- 집에서 `make check`: `derive.py --check`는 통과합니다(파생 파일이 아니므로). `check_build.py`는 이렇게 실패합니다.
  ```
  2 build error(s):
    - dataset/build.manifest.json: the build wrote a manifest that differs from the committed one — re-bless (commit it) if the change is intended
    - dataset/build.variants.manifest.json: the build wrote a manifest that differs from the committed one — re-bless (commit it) if the change is intended
  ```
  variants manifest도 같이 나오는 이유는 그 `inputs`가 core manifest의 hash이기 때문입니다(2.8). `c3-workday`는 variant의 base가 아니므로 variant 78개 자체는 바뀌지 않았습니다.
- CI: `make dataset`이 새 timeline으로 compile해 core manifest를 다시 쓰고, `make check`가 같은 두 줄로 실패합니다.
- 고치는 법: 두 manifest를 commit하고(re-bless), RQ0 gate spec의 두 pin을 다시 적고 harness changelog에 항목을 남깁니다(3.4).

### 사례 2. manifest는 commit했지만 re-pin을 잊었다

사례 1에서 manifest만 commit하고 `rq0-gate.yaml`은 그대로 두었다고 합시다.

- dataset의 `make check`는 통과합니다. dataset 쪽에서는 모든 것이 일치합니다.
- `make -C harness lint`가 실패합니다. 3.5의 모양 그대로 `pins/dataset: sha256 … != pinned fad7192d…`와 `pins/variants/all: …` 두 줄이 나오고 `2 error(s)`로 끝납니다.
- CI에서는 `dataset.yml`은 초록이고 `harness.yml`이 `make -C harness lint` 단계에서 빨갛게 됩니다. workflow가 갈라지는 지점이 곧 진단입니다.

### 사례 3. compiler를 고치고 아무것도 다시 돌리지 않았다

`wlc/compiler.py`의 주석 한 줄을 고치고, build 없이 commit했다고 합시다.

- 집에서 `make test`: `test_manifest.py::test_manifest_pins_the_compile_inputs_by_content`가 실패합니다. 이 test는 committed core manifest의 `inputs` 각 줄을 디스크의 파일 hash와 비교하는데, `dataset/tools/wlc/compiler.py`의 hash가 다르므로 그 경로 이름을 assertion message로 내며 실패합니다. 9.21에서 실제로 일어난 일이 이것입니다(2.12).
- 집에서 build 없이 `make check`: 통과합니다. 디스크의 manifest와 `build/`는 지난번 build의 것이고 committed와 같기 때문입니다. 4.2에서 말한 "build 다음에만 의미가 있다"는 점이 여기서 드러납니다.
- CI: `make dataset`이 manifest의 `inputs`를 새로 쓰고, `make generated`가 generated manifest 다섯 개의 `inputs`도 새로 씁니다(generated manifest도 compile 입력 23개를 pin합니다). `make check`가 일곱 manifest 모두에 대해 "differs from the committed one"으로 실패합니다.
- 고치는 법: README의 규칙 그대로입니다. "If you edit any timeline, variant file, `archetypes.yaml`, a stream or the compiler, run `make dataset variants generated` and commit every manifest with it". 그리고 re-pin합니다.

### 사례 4. timeline 하나를 지우거나 이름을 바꿨다

`c5-t3.timeline.yaml`을 `c6-alias.timeline.yaml`로 바꾸고 `make dataset`을 돌렸다고 합시다. 9.20에서 실제로 있었던 일입니다.

- `compile.py`는 새 이름으로 artifact와 report를 쓰고 manifest를 새로 씁니다. 하지만 `build/` 안의 옛 `c5-t3.workload.json`과 `c5-t3.report.json`을 지우지 않습니다. compile은 쓰기만 하고 정리는 하지 않습니다.
- `make check`가 실패합니다.
  ```
    - build/coreset-single/c5-t3.report.json: on disk, pinned by no manifest
    - build/coreset-single/c5-t3.workload.json: on disk, pinned by no manifest
  ```
- 9.20 changelog D10은 이것을 이렇게 처리했다고 적습니다. "The stale `c5-t3` artifacts removed from `build/` by hand." 깨끗한 checkout에서 시작하는 CI에서는 옛 파일이 애초에 없으므로 이 실패가 나지 않습니다. 집 기계에서만 나는 실패입니다.

> **코드로.** generated set은 사정이 조금 다릅니다. `generate.py`의 `write_timelines`는 정의에 없는 오래된 generated *timeline*을 지웁니다("removes stale ones"). 하지만 `build/<set>-single/` 아래의 오래된 *artifact*는 지우지 않습니다. 그래서 grid 정의에서 cell을 줄이면 집 기계의 `build/`에는 옛 artifact가 남고 `make check`가 같은 "pinned by no manifest"로 실패합니다.

### 사례 5. `build/` 안의 artifact를 손으로 고쳤다

디버깅 중에 `build/coreset-single/c1-dev.workload.json`의 숫자 하나를 직접 바꿨다고 합시다.

- `make check`: `build/coreset-single/c1-dev.workload.json: sha256 1a2b3c4d5e6f… differs from the pinned <원래 hash 앞 12자리>…`.
- 이 상태에서 `make test`를 돌리면 dataset test의 `coreset` fixture는 hash가 맞지 않는 이 파일을 읽지 않고 그 timeline을 다시 compile합니다(7장). 즉 test는 고친 파일에 속지 않습니다.
- harness의 build 의존 test는 hash를 확인하지 않고 파일을 읽습니다. 그래서 harness CI의 workflow는 harness 단계 전에 반드시 `make -C dataset check`를 돌립니다(6장).

### 사례 6. variant recipe를 고치고 `make dataset`을 잊었다

`c7.variant.yaml`의 op 하나를 바꾸고 바로 `make check`를 돌렸다고 합시다.

- `derive.py --check`가 먼저 실패합니다. 영향을 받는 파생 파일마다 `<id>.timeline.yaml: differs from its variant spec (derive drift)` 한 줄씩입니다. 이 줄이 하나라도 있으면 `--require-coverage`는 돌지 않고, `make`는 첫 줄의 실패로 멈추므로 `check_build.py`도 돌지 않습니다.
- 고치는 법: `make dataset`(derive가 파생 timeline을 다시 씁니다), `make variants generated`, 그리고 파생 timeline과 manifest를 함께 commit합니다.

### 사례 7. segment를 지워 cell 하나가 비었다

2026-10-14의 표에서 `office/false` cell은 segment가 1개이고, 그 하나는 `c7-office`(C7, 즉 attribute counterpart 그룹의 파일로, `c1-office`에 원하지 않은 배경 작업을 더한 파생 파일)의 유일한 segment입니다(`coverage-grid.json`의 `per_file`). `c7-office`는 `c7.variant.yaml`에서 파생되므로, 그 recipe에 segment의 label을 다른 mode로 바꾸는 op를 넣었다고 합시다.

- build 없이 `make check`: `derive.py --check`가 `c7-office.timeline.yaml: differs from its variant spec (derive drift)`를 보고합니다. 이때 coverage 표는 아직 디스크의 옛 파생 timeline으로 계산되므로 grid drift는 나오지 않고, 오류가 이미 있으므로 `--require-coverage`도 돌지 않습니다.
- `make dataset`을 돌리면 `derive.py`가 파생 timeline과 `coverage-grid.json`을 다시 쓰고, 표 출력의 마지막에 `empty cells: 1`이 찍히지만 flag가 없으므로 실패하지는 않습니다. 그 다음 `make check`에서 drift는 없고, `--require-coverage`가 `coverage: 1 empty driver-table cell(s) — office/false`로 실패합니다.
- 이것은 build의 실수가 아니라 설계의 실수를 잡는 실패입니다. Phase 7 spec decision 11의 취지대로, 32개 행 중 하나라도 실험 재료가 없으면 build가 멈춥니다.

### 사례 8. generated set을 하나 새로 정의했다

`grids.yaml`의 `sets` 아래에 여섯째 set을 추가하고 `make generated`를 돌린 뒤, 새 manifest를 commit하지 않았다고 합시다.

- `check_build.py`의 `manifests()`가 `grids.yaml`을 읽어 새 manifest를 gate 목록에 넣습니다.
- `check_committed`: `dataset/build.<new>.manifest.json: not in git at HEAD`.
- 새 set을 정의만 하고 `make generated`도 안 돌렸다면, 그 대신 `` dataset/build.<new>.manifest.json: missing (run `make dataset variants generated` first) ``입니다. 반면 `check()` 쪽은 아직 쓰이지 않은 manifest를 건너뛰므로 그 set에 대해서는 아무것도 요구하지 않습니다(`test_check_build.py`의 넷째 test가 확인하는 "a manifest not yet written pins nothing").

### 사례 9. variant의 일부 set만 다시 build했다

`tools/variants.py --sets replay`로 trace-replay set만 다시 만들었다고 합시다.

- `variants.py`는 그 set의 artifact 네 개를 쓰지만 manifest는 쓰지 않습니다("manifest not written").
- artifact가 바뀌었다면 `make check`가 `build/coreset-single/c2-p1a@replay.workload.json: sha256 … differs from the pinned …`처럼 실패합니다. 바뀌지 않았다면 통과합니다.
- 고치는 법: 전체 `make variants`로 manifest까지 쓴 뒤 commit합니다. 부분 build는 실험용이지 bless용이 아닙니다.

### 사례 10. compile 자체가 실패했다

timeline이나 library를 고쳐 compiled program이 canonical lint를 어기게 되었다고 합시다. 예를 들어 TIMER를 가진 program이 TIMER가 아닌 명령으로 시작하게 되었다면, `make dataset`이 compile 단계에서 이렇게 실패합니다.

```
1 error(s):
  - c1-media[single]: player: TIMER is not the first executed instruction — the program opens with RUN, so TIMER's t₀ would not be the arrival (9.11 D11)
```

(id와 첫 명령은 예시이고, 문장 형식은 `wlc/linter.py` 그대로입니다. 마지막 괄호의 9.11 D11은 sub-task 9.11, 즉 scheduler 쪽 상수 연구가 정한 "TIMER의 기준 시각은 그 task의 도착이다"라는 결정입니다.) 이 경우 `compile.py`는 오류가 하나라도 있으면 artifact도 manifest도 쓰지 않고 exit 1을 냅니다. 즉 잘못된 artifact는 애초에 `build/`에 들어가지 못하고, gate까지 가지 않습니다.

## 4.7 Gate가 보지 않는 것

gate가 무엇을 보장하는지와 함께, 무엇을 보장하지 않는지도 정리합니다. 아래 셋은 코드를 따라가서 본 것이고, 첫째는 기록에 아직 없는 관찰입니다.

> **열린 자리.** CI에서 commit되지 않은 파생 파일이 통과할 수 있습니다. 이것은 코드와 workflow를 따라가서 본 관찰이고, 실제로 재현해 보지는 않았습니다(미실행). 어떤 기록도 이 경우를 다루지 않습니다. 경로는 이렇습니다. `make dataset`의 첫 단계 `derive.py`(flag 없음)는 파생 timeline과 `coverage-grid.json`을 무조건 다시 씁니다(`wlc/deriver.py`의 `run`이 `out_path.write_bytes(content)`, `gen/coverage.py`의 `write`가 `out_path.write_bytes(content)`). CI는 `make dataset`을 `make check`보다 먼저 돌립니다. 그래서 CI의 `derive.py --check`는 방금 다시 쓴 파일을 recipe와 비교하게 되고 항상 통과합니다. 한편 `check_build.py`가 git의 HEAD와 비교하는 것은 manifest뿐입니다. 그러므로 recipe를 고치고 집에서 `make dataset variants generated`를 돌린 뒤 recipe와 manifest만 commit하고 다시 쓰인 파생 timeline을 commit하지 않으면, CI는 같은 파생 timeline을 다시 만들어 같은 manifest를 얻고 초록이 됩니다. 그 결과 git에 남은 파생 timeline의 바이트와, artifact의 `meta.derived_from`이 가리키는 git blob hash가 서로 다르게 됩니다. 즉 artifact가 가리키는 blob이 저장소에 없는 상태가 됩니다. `coverage-grid.json`도 같은 경로로 commit 누락이 CI를 통과할 수 있습니다. 집 기계에서 `make dataset` 없이 `make check`를 돌릴 때는 잡히지만, 그것은 gate가 정의된 순서("after `dataset variants generated`")가 아닙니다. 선택지(제안)는 workflow에서 `make dataset` 전에 `derive.py --check`를 한 번 돌리는 것, 또는 build 뒤에 `git diff --exit-code -- dataset/timelines dataset/coverage-grid.json` 같은 단계를 두는 것입니다. 둘 다 gate의 정의를 바꾸는 일이라 인지오가 정할 일입니다.

**둘, gate는 pin하지 않은 입력의 변화를 원인별로 보여 주지 않습니다.** launch stream(2.4의 열린 자리)이 바뀌면 그것을 쓰는 artifact의 hash 변화로 드러나지만, manifest의 `inputs`에는 원인이 보이지 않습니다.

**셋, gate는 한 기계 안의 재현만 봅니다.** `check_build.py`는 "이 기계에서 방금 build한 것이 committed manifest와 같은가"를 봅니다. 다른 기계, 다른 운영체제에서도 같은지는 그 기계에서 gate를 돌려야 알 수 있습니다. 1.4에서 본 libm의 위험이 바로 이것입니다. 그래서 집의 M1 Pro(macOS)에서 bless한 manifest를 GitHub의 Linux runner에서 다시 build해 gate를 통과시키는 CI가 필요하고, 6장이 그 이야기입니다.

---

# 5장 · `make` target의 순서, 시간, 병렬화

## 5.1 이 장의 질문

이 장은 "dataset을 다루는 명령은 무엇이 있고, 어떤 순서로 돌며, 각각 무엇을 읽고 쓰고, 얼마나 걸리나"를 묻습니다. 4장의 gate가 build 다음에만 의미가 있었듯이, 이 target들은 순서에 의미가 있습니다. 또 시간은 이 dataset의 역사에서 결정을 여러 번 바꾼 변수입니다. 한 CI run이 3.5시간에서 12분으로 줄어든 과정이 이 장의 후반부입니다.

## 5.2 `dataset/Makefile` 전체와 그 순서

`dataset/Makefile`은 24줄입니다. 여섯 target이 있고, 각 target의 `##` 주석이 그 target이 하는 일을 적습니다.

```make
PY ?= python3

dataset:            ## derive variants + grid, compile timelines -> build/ + manifest
	$(PY) tools/derive.py
	$(PY) tools/compile.py

variants:           ## the RQ0 gate spec's sensitivity variants -> build/ + variants manifest (needs `dataset`)
	$(PY) tools/variants.py

generated:          ## the generated layer: the sets grids.yaml names, composed or renamed from the C1 task sets -> generated/ (not committed) + build/ + one manifest per set
	$(PY) tools/generate.py

lint:               ## the checks before a compile: repo + timeline lints (no writes; the canonical lints run inside the compile)
	$(PY) tools/lint.py

test:               ## invariant test suite
	$(PY) -m pytest tools/tests -q

check:              ## CI gate, after `dataset variants generated`: derived files, grid (all 32 cells), every manifest equal to its committed bytes, build/ equal to their union
	$(PY) tools/derive.py --check --require-coverage
	$(PY) tools/check_build.py

.PHONY: dataset variants generated lint test check
```

Makefile에는 target 사이의 의존(`dataset: lint` 같은 것)이 적혀 있지 않습니다. 순서는 사람이나 CI가 정합니다. CI(`dataset.yml`)의 순서는 `lint` → `dataset` → `variants` → `generated` → `test` → `check`이고, 이 순서에는 각각 이유가 있습니다.

```
lint ──▶ dataset ──▶ variants ──▶ generated ──▶ test ──▶ check
 │         │            │             │           │         │
 │         │            │             │           │         └ 모든 build 뒤: 쓴 manifest를 HEAD와, build/를 manifest와 비교
 │         │            │             │           └ build 뒤: blessed build를 읽어 compile을 건너뜀
 │         │            │             └ core와 독립 (C1 timeline과 compile 입력만 읽음)
 │         │            └ dataset 뒤: blessed core artifact와 core manifest를 읽음
 │         └ derive가 먼저: 파생 timeline이 compile의 입력
 └ 가장 먼저: 쓰지 않고 몇 초 만에 구조 오류를 잡음
```

- `lint`가 처음인 것은 쓰기 없이 몇 초 만에 끝나는 검사로 구조 오류를 먼저 잡기 위해서입니다. 9.22 spec decision 2가 "`lint` is the pre-compile check"라고 정했습니다.
- `dataset` 안에서 `derive.py`가 `compile.py`보다 먼저인 것은 파생 timeline이 compile의 입력이기 때문입니다.
- `variants`가 `dataset` 뒤인 것은 Makefile 주석의 "(needs `dataset`)" 그대로입니다. `scale-runs`와 `scale-chain` variant는 blessed core artifact를 읽어 변형하고, manifest에는 core manifest의 hash를 적습니다.
- `generated`는 core build에 의존하지 않습니다. C1 timeline과 compile 입력만 읽습니다. 그래도 `check` 전에 돌아야 일곱 manifest가 모두 새로 쓰입니다.
- `test`가 build 뒤인 것은 test가 디스크의 blessed build를 읽어 compile을 건너뛰기 때문입니다(7장). `dataset.yml`의 주석이 "the coreset fixture reads the build just written (9.18)"이라고 적습니다.
- `check`가 마지막인 것은 4.2에서 본 대로입니다.

## 5.3 각 target이 읽고 쓰는 것, 걸리는 시간

아래 표의 시간은 모두 기록된 측정입니다. 집 기계는 Apple M1 Pro, 10 cores, 16 GB, Python 3.12입니다. runner는 GitHub의 표준 Linux runner(`ubuntu-latest`, 4 vCPU)입니다. runner 열의 값은 2026-10-13의 CI run 38390052552(dataset workflow, 성공, 11분 58초)의 것입니다.

| target | 읽는 것 | 쓰는 것 | 집 기계 | runner |
|---|---|---|---|---|
| `lint` | `archetypes.yaml`, `sources.yaml`, `docs/references.md`, committed timeline 전부, `grids.yaml`, library가 가리키는 stream 파일의 존재 | 없음 | 0.8 s (9.22) | 0 s |
| `dataset` | variant recipe, timeline 전부, compile 입력 23개, launch stream, committed generated manifest(coverage 표용) | 파생 timeline, `coverage-grid.json`, `build/coreset-single/` 의 artifact와 report 102개, `build.manifest.json` | 52 s (9.22, 9.20) | 1 min 35 s |
| `variants` | `variants.yaml`, library, `build.manifest.json`, blessed core artifact, 다시 compile할 timeline, replay stream | `build/coreset-single/<base>@<set>.workload.json` 78개, `build.variants.manifest.json` | 1 min 46 s (9.22), 1 min 53 s (9.20) | 2 min 51 s |
| `generated` | `grids.yaml`, `sources.yaml`, C1 timeline 16개, compile 입력 | `generated/<set>/` timeline 1,562개, `build/<set>-single/` 3,124개, generated manifest 5개 | 2 min 17 s (9.20), 2 min 09 s (9.21) | 5 min 06 s |
| `test` | 거의 전부 (build는 hash가 맞을 때만) | 임시 디렉터리와 pytest cache뿐 | 2 min 01 s (9.22, 500 passed) ~ 2 min 15 s (9.20, 520 passed) | 2 min 05 s |
| `check` | 일곱 manifest, git HEAD, `build/` 전체, timeline | 없음 | 6 s (9.20, 3,304 files); 2026-10-14 측정 6.0 s + derive 0.6 s | 5 s |

표의 괄호 안 번호는 그 측정을 기록한 sub-task입니다. 9.20은 C4·C5 grid 작업(2026-10-12), 9.21은 generated layer 소비자 작업(2026-10-13), 9.22는 build 시간 단축 작업(2026-10-11)입니다.

## 5.4 `make lint`

`tools/lint.py`는 세 종류의 lint를 돌립니다.

- **repo lint** (`wlc/linter.py`의 `lint_repo`) — `sources.yaml`의 모든 id가 `docs/references.md`에 있는지(registry가 인용 목록의 부분집합이라는 규칙), library의 모든 entry가 필수 field(`category_source`, `declared_class`, `pattern`, `params`, `lifetime`, `binding_params`, `scalable`, `validation_stats`, `modeling_notes`)를 가졌는지, 모든 숫자 parameter가 `source` tag를 가졌고 그 tag가 registry에서 풀리는지, stimulus·launch·replay stream 파일이 실제로 있는지 등입니다.
- **bound-source lint** (`lint_bound_sources`) — timeline의 각 task가 `bind`나 `count`를 가지면, 같은 key를 가진 `source` map이 있는지, 각 값이 registry tag, tag의 목록, 또는 `design`·`convention`·`arithmetic` label 중 하나인지 봅니다(8장).
- **timeline lint** — `Timeline` loader의 구조 검사(segment가 겹치지 않는지, `depart`가 segment-bound archetype에만 있는지, focus 구간이 task 수명 안에 있는지 등)와, `grids.yaml`의 정의 검사(`lint_grids`)입니다.

통과하면 `lint clean`, 실패하면 `N lint error(s):` 아래에 줄마다 오류를 적습니다.

> **왜 이렇게 정했나.** 9.22 이전의 `lint.py`는 위의 lint 뒤에 모든 timeline을 메모리에서 compile해 canonical lint까지 돌렸고, 그것이 집 기계에서 약 42분이었습니다. 9.22 changelog D2는 이렇게 적습니다. "the compile already runs the same `lint_canonical` with the same arguments on every artifact it writes and fails on an error, so the pass repeated the build's check." 같은 검사가 compile 안에서 이미 돌기 때문에, `lint`는 compile 전의 검사만 남기고 0.8초가 되었습니다. `lint.py`의 docstring이 "a `lint` pass repeats none of it (9.22 spec, decision 2)"이라고 적습니다.

`make lint`는 `--freeze` 없이 `lint.py`를 부릅니다. 그래서 `make lint` 자체는 `meas-pending` tag를 거부하지 않습니다. `meas-pending`은 측정 전의 임시값을 표시하던 tag이고, 그것을 거부하는 검사는 test suite의 `test_lint.py::test_repo_is_freeze_clean`이 `lint_repo(…, freeze=True)`로 돌립니다(8장).

## 5.5 `make dataset`

`derive.py`(flag 없음)가 먼저 돕니다. 다섯 recipe를 적용해 파생 timeline을 쓰고, core 표와 generated 표를 계산해 `coverage-grid.json`을 쓰고, 32행 표를 출력합니다. 이때의 generated 표는 디스크에 있는 generated manifest, 즉 보통은 committed manifest에서 계산됩니다.

그 다음 `compile.py`가 돕니다. `timelines/**/*.timeline.yaml`을 정렬된 순서로 찾아, 각 timeline을 worker process 하나에서 compile하고, compile 결과마다 canonical lint를 돌립니다. canonical lint는 schema 검증(`jsonschema-rs`), event 정렬, task id 유일성, TIMER가 첫 명령인지, FORK와 spawn table의 대응, WAKE 대상과 channel이 실제로 기다려지는지, focus 구간의 유효성을 봅니다. 여기서 `FORK`는 child process를 만드는 program 명령이고, `spawn table`은 compiler가 미리 sampling해 둔 child들의 program 목록입니다(FORK가 있는 program에는 spawn table이 있어야 하고, 그 반대도 마찬가지입니다). `WAKE`는 다른 task를 깨우는 명령이고, `channel`은 task가 `WAIT`로 기다리는 이름 붙은 신호(예: `input:editor`)입니다. 오류가 하나라도 있으면 아무것도 쓰지 않고 exit 1입니다. 오류가 없으면 파일마다 `c1-dev[single]: demand 0.33 (calibration)` 같은 줄을 찍고, artifact, report, manifest를 쓰고 `wrote 51 artifacts + reports + manifest`로 끝납니다.

## 5.6 `make variants`

`variants.py`는 `variants.yaml`의 아홉 set과 각 set의 파일 목록에서 (set, base) 쌍 78개를 만들고, 쌍마다 worker 하나에서 변형합니다. `scale-runs`와 `scale-chain`은 blessed artifact의 RUN 값에 곱하고, `segment-length`, `carried-bounds`, `trace-replay`는 고친 timeline, 고친 library 사본, 또는 replay stream으로 base timeline을 다시 compile합니다. 결과마다 canonical lint를 돌리고, 모두 통과하면 artifact와 manifest를 씁니다. 출력은 `wrote 78 variant artifacts + manifest`입니다.

## 5.7 `make generated`

`generate.py`는 먼저 `grids.yaml`을 lint하고(`lint_grids`), 다섯 set의 cell을 열거하고(`gen.cells.cells`), cell마다 timeline을 `generated/<set>/`에 씁니다(바뀐 것만 다시 쓰고 정의에 없는 옛 timeline은 지웁니다). 그 다음 set마다, 각 timeline에 bound-source lint를 돌리고, compile을 worker pool로 돌리고(`chunksize=8`), canonical lint를 통과하면 artifact, report, manifest를 씁니다. set마다 `transition-grid: wrote 480 artifacts + reports + manifest` 같은 줄이 나옵니다. 한 set이 실패해도 다른 set은 계속 처리하고, 마지막에 exit 1을 냅니다.

## 5.8 `make test`와 `make check`

`make test`는 `python3 -m pytest tools/tests -q`입니다. 7장이 suite 전체를 다룹니다. `make check`는 4장이 다룬 두 줄입니다.

## 5.9 병렬화: `--jobs`와 바이트가 같은 이유

compile, variants, generated는 모두 `--jobs N` flag를 가지며, 기본값은 CPU 수입니다(`os.cpu_count()`). 세 도구 모두 Python의 `concurrent.futures.ProcessPoolExecutor`를 씁니다. thread 대신 process를 고른 이유는 기록에 적혀 있지 않습니다. 일반적인 사정을 덧붙이면, compile은 CPU를 쓰는 순수 Python 계산이고, CPython에서는 GIL 때문에 thread 여러 개가 CPU 계산을 동시에 하지 못하므로 process로 나누는 것이 보통입니다. 웹 개발로 치면 Node에서 CPU 작업을 cluster나 `worker_threads`로 나누는 것에 가깝습니다.

병렬화가 결정론을 깨지 않게 하는 장치가 셋 있습니다.

- **입력이 순수합니다.** `compile_one`의 docstring은 "Pure in its inputs, so the timelines compile in parallel (9.22) and in any order; the manifest sorts"라고 적습니다. 각 timeline의 compile은 다른 timeline에 의존하지 않고, keyed draw를 쓰므로 실행 순서가 값을 바꾸지 않습니다(1.3).
- **결과를 정렬해서 씁니다.** `build_all`은 결과를 모은 뒤 경로순으로 정렬해 manifest를 만듭니다. 9.22 changelog D4는 "sorts the results, so the manifest bytes are those of the serial build"라고 적습니다. `variants.py`는 결과를 spec의 순서로 다시 정렬합니다.
- **worker마다 library와 schema를 한 번만 읽습니다.** `compile.py`의 `_tools`가 process마다 cache합니다. `variants.py`는 (set, file) 쌍마다 별도의 작업 디렉터리를 씁니다(`build_job`).

`--jobs 1`을 주면 pool 없이 직렬로 돕니다. 직렬과 병렬의 manifest가 같은 바이트라는 것이 9.22의 불변식이었고, 9.22 changelog의 After 절은 그 결과를 "The compile's 24 minutes were mostly the schema validation (18 of them, by 9.18 D7's measurement), which `jsonschema-rs` removes; the parallel pool takes the rest from about 6 min of compute to 52 s of wall time on 10 cores"라고 정리합니다. 9.18 D7은 sub-task 9.18의 검증 run 기록입니다.

## 5.10 3.5시간에서 5분으로: 9.22의 전후

9.22 changelog는 고치기 전과 후를 같은 기계에서 쟀습니다.

| step | 전 (2026-10-11, 9.18 시점) | 그때 무엇을 했나 | 후 (2026-10-11, 9.22) |
|---|---|---|---|
| `make lint` | 약 42 min | 51개 timeline을 메모리에서 compile(24)하고 schema 검증(18) | 0.8 s |
| `make dataset` | 22–24 min | 51개 artifact를 직렬로, 각각 schema 검증 | 52 s |
| `make variants` | 33–35 min | 78개 variant를 직렬로 | 1 min 46 s |
| `make test` | 44 min | `test_manifest`가 set을 다시 compile(23), `test_no_file_fails_on_its_demand`가 다시 검증(19) | 2 min 01 s (500 passed, 1 skipped, 가장 느린 test 28 s) |
| `make check` | 56–59 min | set을 다시 compile(24)하고 variants를 다시 build(35) | 1.7 s |

괄호 안의 숫자는 그 step 안에서 해당 작업이 차지한 분입니다. changelog의 결론은 "One local `make lint dataset variants test check` is about 5 min against 3.5 h"입니다.

줄어든 원인은 네 가지입니다.

1. **같은 compile의 반복 제거.** `lint`, `test`, `check`가 각자 하던 재compile을 없앴습니다(9.22 decision 1, 2).
2. **schema 검증의 교체.** 9.22 changelog D3은 95 MB짜리 `c7-transcode` 하나로 세 validator를 쟀습니다. `jsonschema` 141 s, `fastjsonschema` 19.7 s, `jsonschema-rs` 1.4 s입니다. 셋 다 일부러 망가뜨린 event를 잡았습니다. `fastjsonschema`는 draft-07용 package라 이 schema(draft 2020-12)를 통과시키긴 했지만 "outside its stated support"였습니다. 그래서 Rust로 구현된 `jsonschema-rs`를 골랐습니다(9.22 spec decision 3, `requirements.txt`의 `jsonschema>=4.20` → `jsonschema-rs>=0.29`). schema 자체와 검증의 의미는 바뀌지 않았습니다.
3. **병렬화.** compile과 variants를 파일 단위로 나눴습니다(9.22 changelog D4).
4. **test가 blessed build를 읽음.** 9.18 decision 8의 규칙, 즉 hash가 manifest와 맞으면 디스크의 blessed build를 읽고 아니면 compile한다는 규칙을 `test_manifest.py`에도 적용했습니다(7장).

> **왜 이렇게 정했나.** 9.22는 원래 계획에 없던 sub-task입니다. 9.18의 Linux 검증 run 38129714928이 2026-10-11에 23분째 아직 `lint` 단계에 있었고, 인지오가 그 run을 취소했습니다. 9.18 changelog D7은 이유를 "on the 4-vCPU runner the five steps would have run past the 6 h job limit"라고 적습니다. 집 기계에서 3.5시간 걸리는 작업이 4 vCPU runner에서는 GitHub Actions의 job 시간 제한을 넘길 것이었습니다. 그래서 9.22가 같은 날 추가되어 9.19보다 먼저 실행되었습니다(`_dev/TODO.md`: "9.22 added 2026-10-11 after 9.18's verification run, before the generated layers").

> **열린 자리.** "6 h job limit"이라는 숫자는 9.18 changelog D7과 9.22 changelog D6에 적혀 있지만, `docs/references.md`에는 그 근거가 될 GitHub 문서 항목이 없습니다. runner의 사양을 근거로 둔 `gh-hosted-runners` 항목은 processor, memory, storage만 인용합니다. 이 숫자는 이후의 결정(9.21의 build every run, 6장)을 판단할 때도 쓰이는 값이므로, `docs/references.md`의 인용 규칙대로 GitHub Actions의 사용 한도 문서를 읽어 항목을 더할지는 인지오가 정할 일입니다(확인 필요).

## 5.11 `harness/Makefile`

harness 쪽 Makefile도 dataset을 읽는 target을 가집니다. 18줄입니다.

```make
lint:               ## fixture pairs under the frozen contracts; the scoring spec against schema, coreset, recipes; the guard spec against schema, registry, recipes; every experiment spec against schema, coreset, pins
	$(PY) tools/lint.py
	$(PY) tools/scoring_lint.py
	$(PY) tools/guards_lint.py
	$(PY) tools/experiment_lint.py

test:               ## the suite without the two coreset-wide mock tests (what CI runs; they exceed a 16 GB runner)
	$(PY) -m pytest tools/tests -q -m "not coreset_wide"

test-full:          ## the whole suite, the coreset-wide tests included (about 10 GB resident; run at home)
	$(PY) -m pytest tools/tests -q

smoke:              ## the full pipeline on the mocks over every scored coreset file (8.6): a generated throwaway spec, runs under runs/
	$(PY) tools/smoke.py --machine runner.example.yaml
```

dataset과 맞닿는 부분은 이렇습니다.

- `lint`의 `scoring_lint.py`는 scoring spec이 compiled core set과 맞는지 보고, 9.21 이후로는 generated set 다섯 개의 manifest에서 규칙으로 scoring 항을 만들어 compiled generated 파일과 대조합니다. 집 기계에서 약 2분 50초(harness changelog 2026-10-13), runner에서 `make -C harness lint` 전체가 5분 03초와 4분 58초였습니다(9.21 changelog D11).
- `lint`의 `experiment_lint.py`는 3.5에서 본 pin 검사를 합니다. 2026-10-14에 돌린 결과는 `rq0-gate.yaml: experiment rq0-gate, 3 conditions, 19 judging + 32 reporting files, criterion k_of_n_gap`과 `lint clean`이었습니다.
- `test`와 `test-full`의 차이는 6장의 memory 이야기입니다.
- `smoke`는 mock daemon과 mock simulator로 scored core 파일 전부에 대해 pipeline 전체를 돌립니다. 9.14 changelog D14는 2026-10-10에 집 기계에서 4시간 50분이 걸렸고 그중 `c6-dual`의 네 run이 약 3시간이었다고 적습니다.

## 5.12 무엇을 고쳤을 때 무엇을 돌리나

README의 Commands 절과 2.11의 표를 합치면, 일상 작업의 규칙은 이렇습니다.

| 고친 것 | 돌릴 것 | commit할 것 | 그 다음 |
|---|---|---|---|
| timeline, variant recipe, `archetypes.yaml`, stream, compiler (`compile.py`, `wlc/*.py`), schema | `make lint dataset variants generated test check` | 고친 파일, 파생 timeline, `coverage-grid.json`, 일곱 manifest 중 움직인 것 | RQ0 gate spec의 `dataset`·`variants` pin, `harness/CHANGELOG.md` 항목, `make -C harness lint` |
| `grids.yaml`, `generate.py`, `gen/*.py` | `make lint generated test check` | 고친 파일, generated manifest, `coverage-grid.json`(표가 바뀌면) | 지금은 pin 없음 |
| C1 timeline | 첫 행과 같음 (core이면서 generated의 입력) | 첫 행과 같음 | 첫 행과 같음 |
| `variants.yaml` | `make variants check` | `variants.yaml`, variants manifest | `variants` pin, changelog |

README의 문장은 이렇습니다. "If you edit any timeline, variant file, `archetypes.yaml`, a stream or the compiler, run `make dataset variants generated` and commit every manifest with it; if you edit `grids.yaml`, the generator or a C1 timeline, `make generated` and the generated manifests, one per set — otherwise `check` fails." 표의 "commit할 것"에 파생 timeline과 `coverage-grid.json`을 넣은 것은 4.7의 열린 자리 때문입니다. README의 문장은 manifest만 말하지만, gate가 CI에서 잡지 못하는 commit 누락을 사람이 피하려면 이 둘도 함께 commit해야 합니다.

---

# 6장 · CI: GitHub runner 위의 dataset

## 6.1 이 장의 질문

이 장은 "집 기계에서 bless한 build가 다른 기계에서도 같은 바이트로 나온다는 것을 무엇이 확인하고, 그 확인에는 어떤 비용과 한계가 있나"를 묻습니다. 4.7의 마지막에서 보았듯이 gate는 그 gate가 돈 기계 하나에 대해서만 말합니다. 그래서 깨끗한 Linux 기계에서 checkout부터 다시 build하고 같은 gate를 돌리는 CI가 필요합니다. CI는 GitHub Actions 위에서 돌고, 그 runner의 CPU, memory, 디스크, 시간 제한이 이 dataset의 결정 몇 가지를 실제로 바꿨습니다.

## 6.2 Workflow 지도

`.github/workflows/` 아래에는 2026-10-14 현재 15개 workflow가 있습니다.

| workflow | 언제 도나 | 무엇을 하나 |
|---|---|---|
| `dataset.yml` | `main`에 push, 모든 pull request, 손으로(`workflow_dispatch`) | dataset의 `lint`, `dataset`, `variants`, `generated`, `test`, `check` |
| `harness.yml` | `main`에 push, 모든 pull request, 손으로 | dataset을 build하고 `check`한 뒤 harness의 `lint`, `test` |
| `harness-smoke.yml` | `main`에 push, 손으로, `harness/`·`dataset/`·`daemon/driver-table/`·자기 자신을 건드린 pull request | dataset을 build하고 `check`한 뒤 harness의 `smoke` |
| `daemon.yml` | `main`에 push, 모든 pull request | driver table의 lint와 test (dataset과 무관) |
| `meas-*.yml` 11개 | campaign 설정 파일을 바꾼 push, 일부는 손으로 | 측정 campaign (측정 campaign 권) |

dataset을 build하는 workflow는 세 개입니다(`dataset.yml`, `harness.yml`, `harness-smoke.yml`). 셋은 서로 독립된 job이라 각자 처음부터 build합니다.

## 6.3 `dataset.yml` 한 줄씩

```yaml
name: dataset

on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:    # one run on a branch compiles its blessed manifests on Linux (9.18)

jobs:
  dataset:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r dataset/tools/requirements.txt
      - run: make -C dataset lint
      - run: make -C dataset dataset
      - run: make -C dataset variants
      - run: make -C dataset generated  # the generated layer: one manifest per set (9.19)
      - run: make -C dataset test      # the coreset fixture reads the build just written (9.18)
      - run: make -C dataset check     # every manifest reproduces; build/ equals their union
```

- `actions/checkout@v4`는 저장소를 받아옵니다. `build/`와 `generated/`는 git에 없으므로 이 시점의 runner에는 없습니다. 모든 build가 처음부터입니다.
- `setup-python@v5`로 Python 3.12를 씁니다. 집 기계도 Python 3.12입니다.
- `pip install -r dataset/tools/requirements.txt`는 네 package를 설치합니다. `PyYAML>=6.0`, `jsonschema-rs>=0.29`, `pytest>=8.0`, `numpy>=1.26`입니다. 하한만 있고 상한이나 고정 버전은 없습니다(6.8에서 이것이 한 번 문제가 됩니다).
- 마지막 `check`는 runner가 방금 쓴 일곱 manifest를 checkout된 commit의 manifest와 비교합니다. 이 비교가 통과하면, macOS에서 bless한 manifest가 Linux에서 처음부터 재현되었다는 뜻입니다.

> **코드로.** `dataset/README.md`의 Commands 절은 아직 "Needs Python 3.12+ with `pip install -r tools/requirements.txt` (PyYAML, jsonschema, pytest)"라고 적습니다. 실제 `requirements.txt`는 `jsonschema` 대신 `jsonschema-rs`를 쓰고(9.22 changelog D3) `numpy`도 있습니다. README의 이 괄호는 9.22 이전 상태이고, 이 정정은 9.15(문서 정비)의 작업 목록에 있습니다(`_dev/TODO.md`의 9.15 줄: "`dataset/README.md` … `:99` numpy").

## 6.4 `harness.yml`과 `harness-smoke.yml`

```yaml
# harness.yml
      - run: pip install -r harness/tools/requirements.txt -r dataset/tools/requirements.txt
      - run: make -C dataset dataset
      - run: make -C dataset variants    # the RQ0 gate spec lists the variant files (9.14); the scoring lint reads the compiled coreset
      - run: make -C dataset generated   # the generated layer's sets; `check` reads every manifest (9.19)
      - run: make -C dataset check       # the build the harness reads is the blessed one (9.18)
      - run: make -C harness lint
      - run: make -C harness test    # without the two coreset-wide mock tests, which exceed the runner's 16 GB; `make -C harness test-full` at home (9.21)
```

`harness-smoke.yml`은 같은 build와 `check` 뒤에 `make -C harness smoke`를 돌립니다.

두 harness workflow는 dataset의 `lint`와 `test`를 건너뛰지만 `check`는 반드시 harness 단계 앞에서 돌립니다. 주석이 이유를 적습니다. "the build the harness reads is the blessed one (9.18)". harness의 test와 lint는 `build/`의 파일을 hash 확인 없이 읽으므로, 그 파일이 committed manifest와 같다는 것을 바로 앞에서 확인해 두어야 합니다.

> **왜 이렇게 정했나.** 9.18 이전에는 `harness.yml`과 `harness-smoke.yml`이 variants를 write mode로 build하고 "read whatever came out"이었습니다(9.18 changelog D4). audit A4는 이것을 "`harness*.yml` run `make variants` in write mode"라고 지적했습니다. 9.18 spec decision 6의 마지막 문장 "The harness workflows run the dataset check after their build step"이 이것을 고쳤고, harness changelog의 2026-10-11 항목은 결과를 "so a harness run reads the blessed build or fails"라고 적습니다.

## 6.5 언제 도나: `main`, pull request, `workflow_dispatch`

세 workflow 모두 push는 `main` branch에서만 반응합니다. 그런데 Phase 9의 모든 작업은 `jioh/dataset-rebuild` branch에서 이루어졌고(`_dev/TODO.md`의 Phase 9 규칙: "always work on branch `jioh/dataset-rebuild`"), 2026-10-14 현재 `main`은 rebuild 이전 상태를 가지고 있습니다. 9.21 changelog D11은 이 사실을 "the harness workflow runs on a push to `main`, which holds the pre-rebuild state"라고 적습니다. 그래서 rebuild branch의 push는 CI를 깨우지 않습니다.

9.14 시점까지는 이 때문에 CI가 rebuild된 set을 한 번도 보지 못했습니다. 9.14 changelog D12는 "The three CI workflows (`dataset`, `harness`, `harness-smoke`) run on pushes to `main` alone, so on this branch their steps were run locally"라고 적고, 2026-10-10 audit는 이것을 "CI has never compiled this manifest"라고 A4의 한 항목으로 지적했습니다.

해결은 손으로 돌리는 trigger였습니다. 9.18 spec decision 7은 "`dataset.yml` gains `workflow_dispatch`. One run on this branch, on Linux, compiles the blessed manifest; its run id is recorded in the sub-task changelog. The run is started on 인지오's confirmation."이라고 정했습니다. `harness.yml`도 9.21에서 같은 trigger를 얻었습니다(9.21 changelog D11: "the workflow made dispatchable in this sub-task"). 이후 sub-task마다 끝에 dispatch run을 한 번 돌리고 그 run id를 changelog에 적는 것이 관행이 되었습니다.

## 6.6 Runner: 4 vCPU, 16 GB, 14 GB

세 workflow 모두 `runs-on: ubuntu-latest`입니다. 이 runner의 사양은 `docs/references.md`의 `gh-hosted-runners` 항목이 GitHub 문서를 인용해 적습니다. "Standard GitHub-hosted runners for public repositories: the Linux x64 row (`ubuntu-latest`, `ubuntu-24.04`, `ubuntu-22.04`) — processor 4, memory 16 GB, storage (SSD) 14 GB; the private-repository table's Linux row 2 / 8 GB / 14 GB" (2026-10-13 확인). changelog들은 실제 run이 4 vCPU runner에서 돌았다고 적습니다.

이 세 숫자가 각각 이 dataset의 결정 하나씩과 맞닿아 있습니다.

- **4 vCPU** — compile이 CPU 수만큼 병렬이므로, 10 core인 집 기계보다 느립니다. 그리고 9.22 이전의 3.5시간짜리 gate는 이 runner에서 시간 제한을 넘길 것이었습니다(5.10).
- **14 GB 디스크** — `build/`가 6.8 GB입니다. 9.21의 "build every run" 결정이 이 비율을 기준으로 다시 볼 시점을 정합니다(6.9).
- **16 GB memory** — harness의 두 test가 이것을 넘어 kill되었습니다(6.10).

README는 디스크를 "`build/` 6.8 GB of the runner's 14 GB of storage with the core set's 0.7 GB beside it"이라고 적습니다. 이 문장의 "beside it"은 6.8 GB에 더해지는 것처럼 읽히지만, 2026-10-14의 `du`로 보면 6.8 GB는 `build/` 전체이고 core artifact 51개(0.68 GB)와 variant 78개(1.03 GB)가 들어 있는 `coreset-single/` 1.6 GB를 이미 포함합니다(1.5).

## 6.7 기록된 CI run들

다음은 rebuild 이후 changelog에 run id와 함께 기록된 CI run 전부입니다.

| run id | 날짜 | workflow | commit | 결과 | lint | dataset | variants | generated | test | check | 합계 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 38129714928 | 2026-10-11 | dataset | `61f245ff` | 취소 | 23 min 넘게 진행 중 | | | | | | — |
| 38131040159 | 2026-10-11 | dataset | `232cf22d` | 성공 | 1 s | 1:34 | 2:49 | (없음) | 1:54 | 2 s | 6:34 |
| 38135623993 | 2026-10-11 | dataset | `4394dbb5` | 성공 | 2 s | 3:02 | 5:17 | 7:53 (세 set) | 3:47 | 6 s | 20:24 |
| 38243554308 | 2026-10-12 | dataset | `ab96cfd6` | 성공 | <1 s | 1:36 | 2:48 | 5:13 (다섯 set) | 2:05 | 5 s | 12:04 |
| 38387283407 | 2026-10-13 | dataset | `4872a585` | test 실패 | 통과 | 3:02 | 5:16 | 10:02 | 실패 | — | — |
| 38390052552 | 2026-10-13 | dataset | `c879f96d` | 성공 | 0 s | 1:35 | 2:51 | 5:06 | 2:05 | 5 s | 11:58 |
| 38387289484 | 2026-10-13 | harness | `4872a585` | test kill | build와 check 10 min, harness lint 5:03, harness test kill | | | | | | — |
| 38396745220 | 2026-10-13 | harness | `724828c9` | test kill | build와 check 18:32, harness lint 4:58, harness test 6:30에 kill | | | | | | — |

각 run이 무엇을 확인했는지 짧게 적습니다.

- **38129714928** — 9.18의 tooling 그대로 처음 dispatch한 run입니다. 인지오가 23분 후 취소했습니다(5.10).
- **38131040159** — 9.22의 tooling으로 9.18의 set을 build한 run입니다. 9.18 changelog D7과 9.22 changelog D6이 둘 다 이 run을 자기 Linux run으로 기록합니다. core manifest와 variants manifest가 Linux에서 재현되었습니다. 1.4의 libm 위험이 이 build에 대해서는 여기서 닫혔습니다.
- **38135623993** — 9.19 changelog D7. generated set 세 개가 들어간 첫 run이고, `check`가 2,628개 파일과 manifest 다섯 개를 비교했습니다(180 + 2 × 1,224).
- **38243554308** — 9.20 changelog D11. manifest 일곱 개가 Linux에서 재현되었습니다. README와 9.21 decision 8(generated layer를 매 CI run마다 build한다는 결정, 6.9)이 인용하는 "5 min 13 s of a 12 min 04 s run"이 이 run입니다.
- **38387283407** — 9.21 changelog D11. build는 통과했는데 `make -C dataset test`가 실패했습니다. 6.8에서 다룹니다.
- **38390052552** — 9.21 changelog D11. 위 실패를 고친 commit `c879f96d`로 성공했습니다. "The seven manifests and the coverage artifact reproduce on Linux."
- **38387289484, 38396745220** — 9.21 changelog D11. dataset 쪽은 모두 통과했고 harness lint도 통과했지만 harness test가 runner에 의해 kill되었습니다. 6.10에서 다룹니다.

> **코드로.** 같은 step이라도 run마다 시간이 두 배 가까이 다릅니다. 9.19 changelog D7은 38135623993에 대해 "This runner ran the unchanged steps about 1.9× slower than run 38131040159's (`dataset` 1 min 34 s, `variants` 2 min 49 s there), so the generated step's share on a runner of that speed is about 4 min"이라고 적습니다. 9.21의 38387283407(dataset 3:02, generated 10:02)과 38396745220(build 18:32)도 changelog가 "a slower runner"라고 적습니다. GitHub가 어떤 하드웨어에 job을 배정하느냐에 따라 같은 `ubuntu-latest`도 속도가 다르다는 것입니다. 그래서 이 권의 runner 시간은 범위로 읽어야 합니다. 대략 "빠른 runner에서 12분, 느린 runner에서 20분 이상"입니다.

## 6.8 Pytest 버전이 갈라놓은 run

38387283407의 실패는 dataset 쪽 CI가 잡은 유일한 cross-machine 차이였는데, 바이트의 차이가 아니라 도구 버전의 차이였습니다. 9.21 changelog D11의 서술은 이렇습니다. "`test_grid.py` imported the new coverage module as `coverage`, the name of the file's own fixture, which the runner's pytest 9.1.1 wraps in a `FixtureFunctionDefinition` (the home machine's 8.3.4 let the tests pass). Fixed by importing the module under its own name (`c879f96d`)."

풀어 쓰면, test 파일 안에서 module 이름과 fixture 이름이 같은 `coverage`였는데, 집의 pytest 8.3.4는 그대로 통과시켰고 runner가 새로 설치한 pytest 9.1.1은 fixture 함수를 감싸는 방식이 달라 module 이름을 가려 버렸습니다. 고친 방법은 module을 다른 이름으로 import하는 것이었습니다(현재 `test_grid.py`는 `gen_coverage`라는 이름을 씁니다).

> **열린 자리.** 이 실패의 뿌리는 `requirements.txt`가 하한만 적는다는 데 있습니다(`pytest>=8.0`). runner는 매 run마다 그 시점의 최신 버전을 설치하므로, 집 기계와 runner의 도구 버전이 언제든 갈라질 수 있습니다. 기록은 이 test를 고쳤을 뿐, 도구 버전을 고정할지에 대해서는 아무것도 정하지 않았습니다. 버전 차이가 artifact의 바이트를 바꿀 수 있는 package는 compile 경로에 있는 `PyYAML`(timeline과 library를 읽음)과 `jsonschema-rs`(검증만 하고 바이트를 쓰지 않음) 정도이고, 지금까지의 Linux run들은 manifest를 바이트 단위로 재현했습니다. 버전을 고정할지(예: `requirements.txt`를 정확한 버전으로 적거나 lock 파일을 둘지)는 인지오가 정할 일입니다.

## 6.9 Build every run: 9.21 decision 8

generated layer가 생기면서 CI의 비용이 크게 늘었습니다. 한 run에서 generated step이 5분 13초, `build/`가 6.8 GB가 되었습니다. 9.21 spec은 이것을 어떻게 다룰지 정해야 했습니다. 결정은 "지금처럼 매 run마다 전부 build한다"였습니다.

> **왜 이렇게 정했나.** 9.21 spec decision 8의 전문입니다. "The three workflows keep building the five sets on every run (5 min 13 s of a 12 min 04 s run on the 4-vCPU runner; 1,562 artifacts, `build/` 6.8 GB; 9.20 D10, CI run 38243554308). The dataset README states the strategy with the measurements and the criterion for revisiting it — the generated step's time and the build's size against the runner's disk, the next set added being the occasion. On-demand builds and pinned subsets are not taken: both put an exception into the gate's rule that `build/` equals the union of every manifest." 인용 안의 9.20 D10은 sub-task 9.20(C4·C5 grid)의 build 측정 기록입니다. 버린 두 안의 이유가 핵심입니다. "필요할 때만 generated를 build"하거나 "generated의 일부만 build"하면, 그 run에서는 `build/`가 일곱 manifest의 합집합이 아니게 됩니다. 그러면 gate의 규칙 "`build/` equals the union of every manifest"에 예외를 넣어야 합니다. 이 결정은 gate의 규칙을 예외 없이 지키는 쪽을 골랐고, 그 비용으로 매 run 5분 남짓을 냅니다.

README는 다시 볼 기준을 이렇게 적습니다. "The strategy is revisited when a set is added — the naturalistic set on the backlog would be the occasion — or when the generated step's time or the build's size against the runner's storage moves the whole run past what a push can wait for; an on-demand build or a pinned subset would then be weighed, each at the cost of an exception to `check`'s rule that `build/` equals the union of every manifest." 여기서 naturalistic set은 실제 desktop의 전환 빈도를 따라 생성하려는 아직 만들지 않은 set으로, backlog에 있습니다(`_dev/TODO.md`: "its prerequisite is a source for Linux-desktop co-occurrence and transition frequency, which 9.10's search did not find").

9.21 changelog D8은 이 결정을 위해 runner의 디스크 크기를 처음으로 인용 가능한 근거로 만들었습니다. "The storage figure rests on a new deployed-system reference, `gh-hosted-runners` (GitHub Docs, 'GitHub-hosted runners reference', read 2026-10-13) … Entered in `docs/references.md` only (the dataset derives no value from it)." dataset이 이 값에서 어떤 숫자도 만들지 않으므로 `dataset/sources.yaml`에는 넣지 않았다는 뜻입니다.

> **열린 자리.** 기준에 쓰인 "what a push can wait for"에는 숫자가 없습니다. 몇 분, 또는 디스크의 몇 %가 되면 다시 볼지는 기록에 정해져 있지 않습니다. 또 세 workflow가 각자 build하므로 한 push가 dataset을 세 번 build합니다(`dataset.yml`, `harness.yml`, `harness-smoke.yml`). 이 중복은 9.21 decision 8의 "The three workflows keep building"이 받아들인 상태입니다. 하나의 job에서 build해 나머지가 artifact로 받는 구조는 기록에서 검토된 적이 없습니다. 다음 set이 추가될 때 인지오가 함께 볼 수 있는 항목입니다.

## 6.10 Harness의 memory 한계: `coreset_wide`

9.21의 두 harness run이 kill된 이야기는 runner의 16 GB가 실제로 무엇을 막는지 보여 줍니다. changelog D11–D13의 순서를 따라갑니다.

**무엇이 kill되었나.** `make -C harness test`가 suite의 약 55 % 지점에서 `make: *** [Makefile:10: test] Killed`로 끝났습니다. 그 지점에서 도는 test는 둘이었습니다.

- `test_mock_simulator.py::test_every_coreset_file_flows_through_records_with_no_message` — 51개 core 파일 전부를 `fixed`와 `oracle` 두 조건으로 mock simulator에 돌리고, 모든 record row를 만들어 guard가 깨끗한지 봅니다.
- `test_mock_daemon.py::test_oracle_over_the_coreset_reproduces_the_measured_graded_set` — 51개 파일 전부에 mock daemon의 oracle을 돌려, 채점되는 query point의 수가 측정된 값과 같은지 봅니다.

두 test 모두 9.21 이전부터 있었지만, runner에서 rebuild된 set으로 돈 적은 없었습니다(main이 rebuild 이전 상태였으므로). changelog의 문장은 "Both tests predate 9.21 and had never run on a runner against the rebuilt set"입니다. 집 기계(16 GB)에서는 macOS의 memory 압축 덕분에 통과했습니다.

**왜 그렇게 큰가.** `c6-dual`은 compiled JSON이 changelog의 표현으로 179 MB(디스크에서 187,601,756 bytes)이고, record row가 약 1,400만 개입니다. D12는 test가 이 파일 하나에 대해 동시에 들고 있던 것을 적습니다. "the parsed workload (`doc`), the mock simulator's whole trace as a list of line objects *and* as one string (`"".join(...)`), the run-file view (`read_run_file`, a second parse), and `compute`'s rows; the next file's objects were allocated on top before the previous ones were collected."

**첫 시도: 한 번에 한 파일의 객체만.** D12(2026-10-13)는 test 도구만 고쳤습니다. mock simulator가 trace를 한 줄씩 쓰고, test가 쓰고 난 객체를 바로 버리게 했습니다. 집에서 두 test의 최대 resident memory를 쟀더니 9.97 GB, 12분 04초였습니다(고치기 전 두 test file 전체 7.66 GB보다 높은 것은 압축되는 양이 훨씬 줄었기 때문이라고 changelog가 설명합니다). 그런데 runner의 다음 run 38396745220에서도 같은 지점, 48 % 진행 줄 다음에 6분 30초 만에 다시 kill되었습니다. "Holding one file's objects at a time is not enough on the runner".

**두 번째: marker로 분리.** D13(2026-10-14)의 결정입니다. "The two tests … carry a `coreset_wide` marker, registered in `harness/tools/tests/conftest.py`; `make -C harness test` runs the suite with `-m "not coreset_wide"` (296 of 298 tests) and is what `harness.yml` runs; `make -C harness test-full` runs the whole suite and is run at home, where the two pass (D12: 9.97 GB resident, 12 min 04 s)." 집에서 `make test`는 296 passed, 2 deselected, 17분 23초였고, 전체 suite는 약 34분이었습니다. 2026-10-14에 `pytest --collect-only`로 세어 보면 전체 298개, marker 제외 296개입니다.

> **왜 이렇게 정했나.** D13은 test 안에서 set을 잘라 runner에 맞추는 대신 test를 통째로 CI 밖으로 뺀 이유를 이렇게 적습니다. "Marking the tests rather than slicing the set inside them keeps each test's assertion whole — 51 files, the 8.4 measured graded set — where it runs." 두 test의 단언은 "51개 파일 전부"와 "sub-task 8.4가 측정한 채점 집합 전체"에 대한 것입니다. 일부 파일만 돌리면 그 단언이 다른 단언이 됩니다. 그래서 단언은 그대로 두고, 그것이 도는 장소를 집 기계로 옮겼습니다. 그리고 memory의 바닥은 피할 수 없다고 적습니다. "`compute` returns every row of a file as a list, the runner holds a run's rows until its aggregates exist, and a c6-dual pass needs that much."

> **코드로.** marker 등록은 `harness/tools/tests/conftest.py`의 `pytest_configure`입니다. 설명 문자열이 "reads all 51 compiled coreset files and builds every record row of each; needs more memory than a 16 GB runner holds (c6-dual), so `make test` leaves these out and `make test-full` runs them (9.21 D13)"입니다. 두 test에는 `@needs_build`도 붙어 있어, `dataset/build/coreset-single`이 없으면 skip됩니다. `harness/tools/tests/README.md`가 두 target을 모두 적습니다.

이 결정의 결과로, CI는 이 두 test를 더 이상 돌리지 않습니다. 두 test가 지키는 성질(51개 파일이 record pipeline을 오류 없이 통과한다, oracle의 채점 집합이 측정값과 같다)은 집 기계의 `make -C harness test-full`이 지킵니다. 즉 이 두 성질은 사람이 test-full을 돌려야만 확인됩니다.

> **열린 자리.** `harness-smoke.yml`은 2026-10-14에도 머리 주석에 "about eight minutes"라고 적습니다. 이것은 Phase 8의 48개 파일 시절 측정입니다. 9.14 changelog D13은 "The 8.6 smoke's 'about eight minutes' was measured on the old, far smaller files"라고 적고, D14는 rebuild된 set에서의 smoke가 집 기계에서 4시간 50분, 그중 `c6-dual`의 네 run이 약 3시간이었다고 적습니다. 같은 D13은 "a runner with less than about 8 GB free should expect to swap on that file"이라고도 적습니다. rebuild 이후 `harness-smoke.yml`이 runner에서 돈 기록은 changelog에 없습니다(이 workflow는 `main` push와 손으로만 돌고, dispatch run이 기록되지 않았습니다). 이 branch가 `main`에 합쳐지면 첫 push가 이 workflow를 깨웁니다. 그 run이 runner의 시간 제한(5.10의 확인 필요 항목)과 memory 안에 끝날지는 실행해 보지 않았습니다(미실행). 합치기 전에 dispatch로 한 번 돌려 볼지, smoke의 범위를 runner에 맞출지는 인지오가 정할 일입니다.

## 6.11 `meas-*` workflow들

나머지 11개 workflow는 build를 검증하지 않고 측정을 합니다. 측정 campaign 권에서 자세히 다루므로 여기서는 이 권과 맞닿는 점만 적습니다.

- 이름은 `meas-background`, `meas-build`, `meas-costs`, `meas-desktop`, `meas-interactive`, `meas-long-probe`, `meas-names`, `meas-playback`, `meas-probe`, `meas-sched`, `meas-session`입니다. 대부분 `ubuntu-24.04` runner에서 돌고(`meas-names`만 `ubuntu-latest`), `.github/campaign-*.json` 같은 설정 파일을 바꾸는 push로 시작하거나(`meas-names`와 `meas-probe`는 손으로) 합니다.
- 결과는 Actions artifact로 남고, 정리된 원자료는 GitHub release로 공개됩니다. 그 측정값에서 나온 library의 숫자는 `meas-ci:<workflow>:<launch date>` 꼴의 source tag를 답니다(예: `meas-ci:build:2026-09-18`). 즉 이 workflow들은 dataset의 *입력*(`archetypes.yaml`의 값)을 만드는 쪽이고, 이 권의 workflow들은 그 입력에서 나온 *출력*을 검증하는 쪽입니다.
- 둘 다 같은 GitHub runner에서 돈다는 점이 흥미롭습니다. 측정 쪽은 runner를 "측정 대상 기계"로 쓰고, build 쪽은 runner를 "재현을 확인하는 다른 기계"로 씁니다.

## 6.12 CI가 실제로 증명한 것

6.7의 성공한 run들을 모으면, CI가 지금까지 증명한 것은 이렇게 요약됩니다.

- **2026-10-11, run 38131040159** — core manifest와 variants manifest가 Linux에서 바이트 단위로 재현됨. audit가 남긴 libm의 cross-platform 위험이 이 build에서는 나타나지 않음.
- **2026-10-11, run 38135623993** — generated set 세 개의 manifest가 Linux에서 재현됨.
- **2026-10-12, run 38243554308** — manifest 일곱 개 모두 Linux에서 재현됨.
- **2026-10-13, run 38390052552** — 9.21 이후의 manifest 일곱 개와 `coverage-grid.json`이 Linux에서 재현됨. dataset test suite도 Linux에서 통과.
- **2026-10-13, run 38387289484와 38396745220** — harness lint(scoring spec, guard spec, 실험 사양의 pin, generated layer의 scoring 규칙)가 Linux에서 통과. harness test는 memory로 kill되어 이후 marker로 분리됨.

이 기록들은 sub-task 9.16(최종 audit)의 TODO 줄에 "hands to 9.16"으로 넘겨져 있습니다. 예를 들어 "CI run 38243554308 reproduces the seven manifests on Linux (D11)"가 그 줄에 있습니다. 즉 이 run들은 최종 audit가 다시 확인할 재현의 증거로 쓰입니다.

---

# 7장 · Test suite: dataset이 지키는 불변식

## 7.1 이 장의 질문

gate는 "build가 committed manifest와 같은가"만 봅니다. 그런데 committed manifest 자체가 틀렸다면, 즉 compiler가 잘못된 것을 결정론적으로 만들고 있다면 gate는 그것을 충실히 재현할 뿐입니다. snapshot test가 처음 찍힌 snapshot이 틀렸을 때 아무것도 잡지 못하는 것과 같습니다. 그래서 build의 *내용*이 지켜야 할 성질을 따로 확인하는 장치가 필요하고, 그것이 test suite입니다. 이 장은 "dataset의 test는 무엇을 확인하고, build와 어떻게 맞물리나"를 묻습니다.

## 7.2 Dataset suite의 전체 모양

dataset의 test는 `dataset/tools/tests/`에 있습니다. 2026-10-14에 센 숫자는 이렇습니다.

- `test_*.py` 파일 33개 (`ls test_*.py | wc -l`).
- `def test_` 함수 476개 (`grep -c`).
- parametrize로 펼친 test 528개 (`pytest --collect-only`). 9.21 changelog D10의 "527 passed, 1 skipped"와 합이 같습니다.
- `conftest.py` 하나와 `fixtures/` 아래의 작은 timeline 세 개(`fx-game`, `fx-mixed`, `fx-oversub`).

33개 파일은 두 무리로 나뉩니다. 17개 파일(176개 test 함수)이 compiler, build, manifest, 생성 규칙을 확인하고, 16개 `test_meas*.py` 파일(300개 test 함수)은 측정 campaign 도구(`dataset/tools/meas/`)를 확인합니다. 후자는 dataset의 *입력*을 만드는 도구의 test이므로 측정 campaign 권의 영역이고, 이 장은 전자를 주로 봅니다.

이 suite의 헌장은 2026-08-27의 task-2.3 spec이 "Invariants (the test suite's charter)"라는 제목으로 적었습니다.

- "Same timeline + same library commit + same seed ⇒ byte-identical canonical output."
- "A one-entry diff between two timelines changes only that entry's compiled events."
- "`-native` and `-single` variants of one timeline differ only in declared-scalable fields." (native set이 사라져 지금은 `test_single_is_the_only_mode`로 바뀌었습니다)
- "Compiled output validates against `dataset/schema/workload.schema.json`; the schema-declared linter invariants (event ordering, id uniqueness, FORK ⇔ spawn_table, channel resolution) are enforced."
- "Registry subset lint …, provenance tags, locator patterns, `meas-pending` freeze gate".

> **왜 이렇게 정했나.** test를 CI에 연결하는 것 자체가 결정이었습니다. Phase 2 spec decision 4(2026-08-27)는 "The linter and invariant tests are wired into GitHub Actions as part of 2.3's deliverable, not left local-only"라고 적습니다. 처음부터 test는 개발자의 기계에만 있는 것이 아니라 CI의 단계였습니다.

## 7.3 Blessed build를 읽는 fixture

이 suite에서 build와 가장 직접 맞물리는 장치는 `test_coreset.py`의 `coreset` fixture입니다. module 단위로 한 번 만들어지고, 51개 timeline 각각의 (artifact, report) 쌍을 제공합니다. 동작은 이렇습니다.

```python
def _blessed(build_dir, rel, manifest):
    """The artifact and its report read from the blessed build when both hash to the manifest's entries (9.18 spec,
    decision 8); None otherwise."""
    …
        if pinned is None or not path.is_file():
            return None
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != pinned:
            return None
    …

@pytest.fixture(scope="module")
def coreset(repo_root, library):
    …
        blessed = _blessed(dataset / "build", rel, manifest)
        if blessed is not None:
            compiled[blessed[0]["meta"]["id"]] = blessed
            continue
        timeline = Timeline(path, library)
        canonical, report = compile_timeline(timeline, library, "single")
        compiled[timeline.id] = (canonical, report)
```

timeline마다 `build/coreset-single/<id>.workload.json`과 그 report를 읽어 SHA-256을 계산하고, 디스크의 manifest(`dataset/build.manifest.json`)에 적힌 값과 둘 다 같으면 그 파일을 씁니다. 하나라도 다르거나 없으면 그 timeline을 메모리에서 compile합니다. 그래서 build를 막 끝낸 상태에서는 compile 비용이 0이고, build가 없거나 낡았으면 test가 스스로 compile해서 여전히 올바른 대상을 검사합니다. 4.6의 사례 5처럼 `build/`의 파일을 손으로 고쳤어도 test는 속지 않습니다.

> **왜 이렇게 정했나.** 9.18 spec decision 8(compile report를 blessed artifact로 만든 결정)의 둘째 문장이 이 fixture입니다. 근거는 9.17의 인계입니다. 9.17 changelog D6–D7은 dataset suite 전체를 돌리다가 "stopped at about a fifth after 44 minutes … its `coreset` fixture recompiles the 51 timelines in-process (about 25 min alone)"라고 적었습니다. 9.18 changelog D5는 결과를 "A run after `make dataset` costs the tests alone"이라고 적고, D7은 "The `coreset` fixture reads the 51 pairs from the blessed build in 5 s"라고 쟀습니다. 9.22 changelog D4는 같은 규칙을 `test_manifest.py`의 `built` fixture에도 적용했습니다("`test_manifest.py` reads the blessed build when every artifact and report hashes to the committed manifest … and compiles otherwise").

웹 개발로 비유하면, build cache를 쓰는 test runner와 같습니다. Jest나 Vitest가 transform 결과를 content hash로 cache하고, hash가 맞으면 다시 transform하지 않는 것과 같은 원리입니다. 차이는 cache key가 committed manifest라는 점입니다. 그래서 이 cache는 "지난번에 만든 것"이 아니라 "bless된 것"만 재사용합니다.

## 7.4 파일별로 무엇을 확인하나

### Compiler의 불변식

| 파일 | test 수 | 무엇을 확인하나 |
|---|---|---|
| `test_invariants.py` | 6 | 헌장의 핵심. 같은 fixture를 두 번 compile하면 바이트가 같다(`test_byte_determinism`). task 하나를 더해도 다른 task의 draw가 바뀌지 않는다(`test_keyed_isolation_unrelated_task`). 이름 하나를 바꾸면 그 task의 `name`만 바뀐다(`test_one_entry_diff`). `single`이 유일한 mode다. chain의 lane scaling과 구성원 수 |
| `test_canonical.py` | 12 | fixture 세 개가 canonical lint를 통과한다. 모든 task record가 bound entry의 `declared_class`를 가진다. schema가 그것을 요구한다. event가 정렬되고 id가 유일하다. build orchestrator의 spawn table이 여섯 구성원짜리 object job이다. `count` 전개. keystroke wake가 input 창 안에 있다. demand 추정. `familiarity`가 ground truth로 옮겨진다. batch job의 RUN·block |
| `test_units.py` | 3 | `60s`, `8m30s`, `50ms` 같은 시간 표기가 정수 µs로 바뀐다 |

`test_byte_determinism`은 같은 process 안에서 두 번 compile합니다. 그래서 이 test는 "같은 기계, 같은 process에서의 결정론"만 증명합니다. 다른 기계, 다른 운영체제에서의 결정론은 CI의 Linux build가 증명합니다(6.12). 두 증명은 역할이 다릅니다.

### Core set의 설계 규칙

`test_coreset.py`(27개)는 실제 51개 파일이 core set의 설계 규칙을 지키는지 봅니다. 모두 위의 `coreset` fixture를 씁니다.

- **파생의 일관성** — `test_derive_idempotent`는 `derive.py --check`와 같은 확인을 합니다. `test_variant_cannot_change_seed`는 seed를 바꾸는 op가 없음을, `test_set_input_writes_the_bases_window_as_slice_of`, `test_every_counterpart_keystroke_window_is_its_bases_slice`, `test_segment_shift_moves_a_slice_with_its_window`는 파생 파일의 keystroke 창이 base 창의 slice로 쓰이는 규칙(8장)을 봅니다.
- **C2, 즉 intent pair 그룹** — 짝을 이룬 두 파일이 정해진 한 곳에서만 다름: `test_p1_pair_differs_in_segment_one_only`, `test_pair_one_task_diff`, `test_p3_pair_segment_one_holds_the_backup_in_both_files`, 그리고 `c2-p2a`와 `c2-p2a-idle`이 다운로드 task의 `declared_class` 하나에서만 다름을 보는 `test_idle_download_variant_differs_in_the_class_alone`.
- **C4, C5, C6 그룹** — distractor 주입 파일이 주입 하나만 더함(`test_c4_injection_only`), familiarity 파일이 이름만 바꿈(`test_c5_names_only`), `c6-alias`가 tier 없는 pre-committed miss임, `c6-fold`의 이름이 그대로임.
- **C7, 즉 attribute counterpart 그룹** — 원하지 않은 배경 작업을 더한 파생 파일들: interactive counterpart가 package upgrade를 주입함, counterpart의 keystroke wake가 base의 것의 부분집합임(`test_c7_input_wakes_are_a_subset_of_the_bases_in_the_first_c_seconds`), batch counterpart 다섯 개가 각각 base의 처음 C초임(indexing, ml-train, transcode, render, backup), 같은 이름의 counterpart는 label만 뒤집힘, C7과 파생 파일이 `calibration` class를 선언함.
- **수요** — `test_no_file_fails_on_its_demand`, `test_demand_is_recorded_per_segment` (7.5).
- **scenario tag** — `test_every_segment_tags_the_scenarios_of_the_programs_it_shows`.

### Manifest와 gate

| 파일 | test 수 | 무엇을 확인하나 |
|---|---|---|
| `test_manifest.py` | 2 | `test_manifest_records_demand_per_artifact`: manifest의 `demand`가 report의 값과 같고, segment별 기록이 report의 `per_segment`와 맞고, `reports` section의 key가 report 경로이며 hash가 report 바이트의 hash임. `test_manifest_pins_the_compile_inputs_by_content`: `inputs`의 key 집합이 `input_files`와 같고 모든 hash가 디스크의 파일과 같음 |
| `test_check_build.py` | 4 | 4.4에서 본 `check_build.check`의 네 경우 |
| `test_grid.py` | 20 | coverage grid의 32행 순서, tier 열, core set이 32 cell을 모두 채움, C7 counterpart가 base의 `false` cell임, `ambiguous`가 표 밖임, committed `coverage-grid.json`이 timeline과 generated manifest에서 다시 계산한 것과 같음(`test_committed_grid_matches_the_timelines_and_the_generated_manifests`), generated 표가 `true` cell만 채움, segment label 없는 manifest를 거부함, committed JSON이 정렬되어 안정적임 |
| `test_lint.py` | 14 | 실제 repo가 lint를 통과함, freeze 상태임(`meas-pending` 없음), registry 부분집합 규칙, `declared_class` 요구, TIMER-first, timeline 구조 규칙, bound value의 `source` 규칙, demand window가 아무 파일도 막지 않음 |

### Generated layer

`test_generated.py`(21개)는 generator가 정의대로 열거하는지 봅니다. 첫 test가 전체 모양을 고정합니다.

```python
def test_the_definition_names_the_sixteen_modes_the_240_pairs_and_the_five_sets(layer):
    assert layer["modes"] == MODES
    assert len(ordered_pairs(layer["modes"])) == 240 == len({p for p in ordered_pairs(layer["modes"])})
    assert {k: len(v) for k, v in layer["by_set"].items()} == {"transition-grid": 480, "return-grid": 720,
                                                              "flap-stress": 24, "distractor-grid": 272,
                                                              "familiarity-ladder": 66}
    assert len(layer["by_id"]) == 1562
```

나머지는 두 전환 형태의 배치, 2초 segment에 input 창이 없음, return grid의 tuning·measurement 반분, flap-stress의 두 seed, seed가 cell id의 keyed draw임, 모든 cell이 loader와 bound-source lint를 통과함, `grids.yaml`의 lint, distractor와 ladder의 규칙, 그리고 manifest에 관한 test입니다. 마지막 무리 중 `test_the_committed_manifests_pin_the_generator_and_record_each_cells_coordinates`는 committed generated manifest마다 section이 정확히 다섯 개(`inputs`, `artifacts`, `demand`, `reports`, `grid`)인지, `inputs`가 generator 입력을 모두 포함하고 hash가 디스크와 같은지, `grid` record가 cell 열거에서 다시 계산한 좌표와 같은지 봅니다. 즉 2.9에서 본 manifest의 모양이 test로 고정되어 있습니다.

> **코드로.** README는 generated layer에 빈 cell 규칙이 없는 이유를 "each set's enumeration is asserted by the generator's tests (`tools/tests/test_generated.py`)"라고 적습니다. 4.3의 `--require-coverage`가 core set에서 하는 일을, generated layer에서는 이 test들의 개수 단언이 합니다.

### Variants, replay, launch

| 파일 | test 수 | 무엇을 확인하나 |
|---|---|---|
| `test_variants_replay.py` | 2 | trace-replay set의 library 사본이 각 entry를 그 stream으로 가리키는지, replay variant의 report가 task별 재생 내용을 적는지. compiled core가 없으면 skip |
| `test_replay_compile.py` | 12 | replay stream으로 compile하는 규칙: seed로 정한 연속 구간, operation이 replay보다 우선, task group이 서로 다른 stream을 받음, stream이 task보다 짧으면 build 실패, kind가 틀리면 build 실패, linter가 stream 파일을 요구 |
| `test_launch_compile.py` | 6 | 파일 중간에 시작한 task가 launch 단계를 재생한 뒤 정상 상태로 감, 0초에 시작한 task는 그대로, linter가 launch stream 파일을 요구 |

### 측정된 entry의 재현

| 파일 | test 수 | 무엇을 확인하나 |
|---|---|---|
| `test_measured.py` | 10 | 측정된 archetype의 compile: quantile 표 분포, 합쳐진 event stream, timer wake가 task의 timer channel에, playback의 주기 job, 재생되는 stimulus |
| `test_measured_fidelity.py` | 31 | compiled library가 측정한 것을 재현함: 표가 열 개 quantile과 평균을 유지, gap이 측정 구간을 감싸 합이 구간 길이와 같음, 모든 측정 component가 측정된 wake rate로 compile됨, batch 표가 pool된 기록에서 다시 만들어짐 |

### 도구들

| 파일 | test 수 | 무엇을 확인하나 |
|---|---|---|
| `test_beyond_hash.py` | 2 | library hash만 다른 artifact를 "움직이지 않음"으로 봄, demand가 HEAD와 다르면 이동으로 봄 (2.3의 `beyond_hash.py`) |
| `test_end_bound.py` | 3 | batch job이 모든 work-conserving 정책에서 언제 끝나는지의 산술(`end_bound.py`) |
| `test_splice.py` | 1 | YAML anchor가 붙은 library entry를 splice 도구가 따로 된 block으로 봄 |

## 7.5 Demand에 관한 두 test

`test_coreset.py`의 두 test는 9.14 decision 4(demand window의 은퇴)를 test로 바꾼 것입니다.

```python
def test_no_file_fails_on_its_demand(coreset, schema):
    """9.14 decision 4: the demand window retired as a gate; every file lints clean whatever its demand."""
    for name, (canonical, report) in coreset.items():
        assert lint_canonical(canonical, schema, report=report,
                              mode="single", name=name) == []
```

51개 파일 전부에 canonical lint를 다시 돌려, 수요가 얼마든 lint가 깨끗한지 봅니다. `c2-p1a`의 14.505도 통과해야 합니다. 둘째 test `test_demand_is_recorded_per_segment`는 report의 segment 구간이 ground truth의 segment와 같고, segment utilization의 시간 가중 평균이 파일 utilization과 1e-6 안에서 같은지 봅니다.

이 둘 중 첫째는 9.22 이전 suite에서 가장 느린 test 중 하나였습니다. 9.18 changelog D7은 "`test_coreset.py::test_no_file_fails_on_its_demand` (1,153 s, `lint_canonical`'s jsonschema pass)"라고 적습니다. 678 MB를 Python `jsonschema`로 약 0.6 MB/s에 검증했기 때문입니다. `jsonschema-rs`로 바뀐 뒤 suite에서 가장 느린 test가 28초가 되었습니다(9.22 After).

## 7.6 Harness 쪽에서 dataset을 읽는 test와 lint

harness의 suite(`harness/tools/tests/`, 2026-10-14에 298개 collect)도 dataset을 읽습니다. 이 test들은 hash를 확인하지 않고 `dataset/build/coreset-single/`을 바로 읽으므로, 6.4에서 본 것처럼 workflow가 그 앞에서 `make -C dataset check`를 돌립니다. 또 많은 test가 `needs_build = pytest.mark.skipif(not BUILD.exists(), reason="compiled coreset absent")`를 달고 있어서, build가 없으면 skip됩니다. `harness/tools/tests/README.md`는 "A handful drive the runner end to end on the mocks over compiled coreset files and are skipped when `dataset/build/coreset-single` is absent"라고 적습니다.

| 어디 | 무엇을 읽고 무엇을 확인하나 |
|---|---|
| `test_scoring.py::test_committed_spec_lints_clean` | scoring spec을 compiled core set에 대해 lint |
| `test_scoring.py::test_every_coreset_file_but_idle_has_terms` | compiled core 파일 목록에서 scoring spec의 파일을 빼면 정확히 `{c1-idle, c7-idle}`. 즉 idle 파일 둘만 점수 항이 없음 |
| `test_runner.py`의 pipeline test (`@needs_build` 5곳) | mock daemon과 mock simulator로 runner 전체를 compiled 파일 위에서 돌림 |
| `test_mock_daemon.py` (`@needs_build` 4곳) | `c1-compile`, `c2-p1a` 같은 실제 파일로 mock daemon의 동작 확인. 그중 하나가 `coreset_wide` |
| `test_mock_simulator.py` (`@needs_build` 1곳) | 그 하나가 `coreset_wide` test |
| `test_manifests.py::test_the_committed_manifests_carry_the_record_and_split_as_the_specs_will_read_them` | committed generated manifest 다섯 개에서 `split` 반분, transition grid의 `form: focus` 240개, distractor grid의 out-of-vocabulary 32개와 `focus_name_shared` 26개, ladder의 tier 5 `all` 16개와 tier 3 두 개(`fl-backup-t3`, `fl-render-t3`) |
| `make -C harness lint`의 `scoring_lint.py` | generated set 다섯 개의 manifest에서 규칙으로 scoring 항을 만들어 compiled generated 파일과 대조. 9.21 changelog D10의 결과: transition grid 480개 파일 1,320항, return grid 716개 2,865항, flap-stress 24개 248항, distractor grid 255개 374항, ladder 64개 104항 |
| `make -C harness lint`의 `experiment_lint.py` | 3.5의 pin 검사 |

## 7.7 Test 시간의 역사

dataset suite의 크기와 시간은 Phase 9 동안 이렇게 움직였습니다(집 기계).

| 날짜 | sub-task 기록 | 결과 | 시간 |
|---|---|---|---|
| 2026-10-09 | 9.13 D8 | 438 passed, 4 failed | 32 min |
| 2026-10-09/10 | 9.14 D12 | 464 passed | 50 min |
| 2026-10-11 | 9.17 D6 | 약 1/5 지점에서 중단 | 44 min 경과 |
| 2026-10-11 | 9.18 D7 | 501 collected, 497 passed, 1 skipped, 3 failed (첫 run) | 44 min 03 s |
| 2026-10-11 | 9.22 After | 500 passed, 1 skipped | 2 min 01 s |
| 2026-10-11 | 9.19 D7 | 513 passed, 1 skipped | 2 min 08 s |
| 2026-10-12 | 9.20 D10 | 520 passed, 1 skipped | 2 min 15 s |
| 2026-10-13 | 9.21 D10 | 527 passed, 1 skipped | (기록 없음) |

표의 "sub-task 기록" 열은 그 숫자를 적은 sub-task와 changelog 항목입니다. 9.13 D8은 rebuild 직후 library 도구를 고친 항목, 9.14 D12는 variant를 build하고 re-pin한 항목, 9.17 D6은 focus 작업 후의 rebuild 항목, 9.18 D7은 build gate의 검증 run, 9.22 After는 build 시간 단축 후의 측정, 9.19 D7은 generator 작업의 CI run 항목, 9.20 D10은 C4·C5 grid의 build 항목, 9.21 D10은 generated layer 소비자 작업의 검증 항목입니다.

9.18의 세 실패는 9.17이 keystroke track의 이름을 `focus`에서 `input`으로 바꾼 뒤 `test_measured.py`의 helper가 옛 이름을 쓰고 있었던 것이었습니다(9.18 changelog D7). 9.13의 네 실패와 harness 쪽 실패들(9.13 reads R6: 264개 중 9개)도 rebuild로 바뀐 사실에 test의 기대값이 따라가지 못한 것이었습니다. 즉 이 suite는 rebuild 동안 "새 사실이 옛 문장과 어긋나는 곳"을 찾는 역할도 했습니다.

harness suite는 9.18에서 284개 중 283개 통과(26분 44초), 9.19에서 284개(30분 19초), 9.20에서 284개(32분 11초), 9.21에서 298개(약 34분)였고, 9.21 D13 이후 CI가 돌리는 `make test`는 296개 17분 23초입니다.

> **코드로.** 2026-10-14에 집 기계에서 확인하면 dataset suite의 skip 하나는 `test_meas_send.py`의 SMTP test입니다. `pytest.importorskip("aiosmtpd")`가 `aiosmtpd` package가 없어서 skip합니다(`SKIPPED [1] tools/tests/test_meas_send.py:48: could not import 'aiosmtpd'`). `requirements.txt`에 `aiosmtpd`가 없으므로 CI에서도 같은 test가 skip될 것입니다. 이 test는 측정 도구(Thunderbird의 `send` 측정에 쓰는 SMTP 상대)의 test이고 build와는 관계가 없습니다.

---

# 8장 · Rules of the tree: 각 규칙과 그 이유

## 8.1 이 장의 질문

`dataset/README.md`의 끝에는 "Rules of the tree"라는 절이 있고, 아홉 개의 규칙이 적혀 있습니다. 이 규칙들은 build의 바이트를 직접 다루지는 않지만, 바이트를 만드는 입력이 어떤 모양이어야 하는지를 정합니다. 그리고 대부분은 이 권에서 본 장치(lint, canonical lint, test, manifest) 중 하나로 강제됩니다. 이 장은 규칙 하나하나에 대해 "무엇을 요구하나, 왜 그런가(기록된 이유), 무엇이 그것을 강제하나"를 묻습니다. 하나는 이미 은퇴한 규칙이 README에 남아 있는 경우이고, 하나는 다른 기록과 문자 그대로 충돌합니다. 그 둘도 함께 봅니다.

## 8.2 규칙 1 · Canonical semantics live in the docs, not here

**규칙.** "The compiler implements `docs/simulator/interpretation-contract.md`; the build order and set design follow `docs/workload/building-plan.md`; archetype authoring follows `docs/workload/archetype-plan.md`. When code and doc disagree, the doc wins — fix the code."

`interpretation contract`는 canonical workload의 각 op와 field가 무엇을 뜻하는지를 simulator 쪽에 대해 정하는 문서입니다. README의 다른 곳은 이 관계를 "Field semantics are normative in `docs/simulator/interpretation-contract.md`; the schema is the machine check, not the definition"이라고 적습니다. 즉 schema(`workload.schema.json`)는 모양만 검사하고, 의미는 문서가 정합니다.

**기록된 이유.** README가 2026-08-28에 처음 쓰일 때(커밋 `bf6aea4c`) 들어간 규칙이고, 이 규칙의 이유를 따로 적은 기록은 없습니다. 기록된 이유는 없습니다. 위의 "the schema is the machine check, not the definition"이 규칙의 취지를 보여 주는 가장 가까운 문장입니다.

**무엇이 강제하나.** 자동으로 강제하는 장치는 없습니다. 사람이 지키는 규칙입니다.

> **열린 자리.** 이 규칙은 2026-10-14 현재 문자 그대로 적용할 수 없는 곳이 있습니다. interpretation contract의 몇 부분은 rebuild 이전 상태를 적고 있습니다. 예를 들어 그 §7(67행)은 "Two compile modes per timeline: `-native` (as-measured, released only, never executed here) and `-single`"이라고 적고, 바로 다음 줄은 "every compiled `-single` workload's aggregate demand lands in the measurable oversubscription regime (~100–150% of the lane)"이라고 적습니다. 코드에는 `single` mode 하나뿐이고(2.5) 그것은 9.13 spec decision 5(native mode를 compiler에서 지운 결정)라는 더 나중의 결정을 따른 것이며, demand window는 9.14 decision 4로 은퇴했습니다(8.7). 이 경우 "fix the code"가 아니라 문서를 고쳐야 합니다. 또 sub-task 9.15(문서 정비)의 spec decision 3(2026-10-14)은 문서를 고치는 작업의 우선순위를 "Highest first: the code and data as they stand … the latest decision record … the hand-off text … the current docs, never an authority"라고 정했고, "Where code contradicts its own latest decision, the doc describes the code and the mismatch is logged as a finding for 인지오"라고 적습니다. 두 규칙은 다루는 질문이 다릅니다. README의 규칙은 "의미를 어디서 정의하나"이고, 9.15의 규칙은 "지금 상태를 무엇에서 읽어 문서에 옮기나"입니다. 그래도 문자 그대로는 반대 방향을 가리킵니다. 9.15가 contract를 코드와 결정에 맞춘 뒤 README의 이 규칙을 그대로 둘지, 범위를 한정하는 문장을 더할지는 인지오가 정할 일입니다.

## 8.3 규칙 2 · Behavior parameters live in `archetypes.yaml`, never inline in a timeline

**규칙.** "Timelines bind `(name, archetype)` and supply only the knobs listed in the archetype's `binding_params`."

`archetype`은 한 종류의 process 행동(예: `code-editor`, `build-orchestrator`, `cpu-batch`)을 측정된 분포로 적은 library entry입니다. `binding_params`는 그 entry가 timeline에서 값을 받을 수 있다고 선언한 손잡이들입니다(예: `build-orchestrator`의 `spawn_count`, `parallelism_cap`, `child_name`). timeline은 "이 이름의 process가 이 archetype으로 이때 도착한다"와 그 손잡이 값만 적습니다.

**기록된 이유.** building plan의 §2.2가 두 가지를 적습니다. 첫째, "Reference-only: higher layers use archetype ids; the linter rejects inline numerics in Layers 2–3." 둘째, "Name/behavior separation: an archetype never fixes a process name. The (name, archetype) binding happens in the scenario catalog or the timeline — this is what makes C5's name-swap and C6's name-collision files expressible without touching behavior." C5는 familiarity ladder 그룹(같은 행동, 낯선 이름), C6는 resolution limit 그룹(같은 이름, 다른 행동)입니다. 이름과 행동이 분리되어 있어야 둘 중 하나만 바꾼 파일을 만들 수 있습니다. 그리고 §6의 "Payoff"는 이 분리가 출처 추적을 가능하게 한다고 적습니다(8.4).

이 권의 관점에서 보면 이 규칙에는 또 하나의 효과가 있습니다. 모든 행동이 `archetypes.yaml` 한 파일에 있으므로, 모든 artifact의 `meta.sampled.archetypes`에 적힌 library hash 하나가 그 artifact의 행동 전부를 고정합니다(2.3). 행동 값이 timeline 여기저기에 흩어져 있었다면 그 값들은 각 timeline의 blob hash로만 고정되었을 것입니다.

**무엇이 강제하나.** `Timeline` loader(`wlc/timeline.py`)가 `bind`의 key가 archetype의 `binding_params`와 정확히 같은지 확인합니다. task-2.3 spec decision 2는 "any other numeric is the inline-numerics lint violation"이라고 적습니다. `make lint`와 compile이 모두 이 loader를 거칩니다.

## 8.4 규칙 3 · Every parameter value is sourced

**규칙.** "Numbers carry a `source` tag resolving through `sources.yaml` → `docs/references.md`. Measured values are tagged `meas-ci:<workflow>:<run>`; raw data lives on the GitHub release named in the tag's registry entry. A timeline's bound values too (9.10 D32): a task's `source` map mirrors its `bind` keys and its `count`, each entry a tag, a list of tags, or one of the labels `design` / `convention` / `arithmetic`; the linter checks the key sets and the tags."

여기서 9.10 D32는 sub-task 9.10(scenario와 timeline 연구)의 결정으로, timeline이 묶는 값에도 출처나 label을 달고 lint로 확인한다는 것입니다. `c6-dual`의 build task를 예로 들면 이렇게 생겼습니다.

```yaml
bind:   {spawn_count: 2908, parallelism_cap: 8, child_name: cc1}
source: {spawn_count: "meas-ci:build:2026-09-18", parallelism_cap: design, child_name: "meas-ci:build:2026-09-18"}
```

`spawn_count`와 `child_name`은 2026-09-18의 build 측정 campaign에서 왔고, `parallelism_cap: 8`은 설계로 정한 값이라 `design` label을 답니다.

**기록된 이유.** library 쪽은 building plan §6의 "Payoff"입니다. "the paper states, machine-checkably, 'every numeric parameter in the dataset traces to an external source or to our released measurements.'" 논문이 이 문장을 기계적으로 확인 가능한 형태로 말할 수 있게 하는 것이 목적입니다. timeline 쪽은 2026-10-10 audit의 A2가 계기였습니다. "Timeline bound values carry no source field. 9.10 D32 decided `source:`/label on every bound value with a lint, 'the field and the lint are 9.13's'; `timeline.py` has no source slot". 같은 audit의 답변 표는 외부 검토자가 거절할 이유로 "timeline bound values carry no source field"를 들었습니다. 9.18 spec decision 4가 이것을 구현했습니다.

이 규칙이 이 권의 장치와 만나는 지점이 하나 있습니다. `source` map을 더하자 모든 timeline의 바이트가 바뀌었고, 그래서 모든 artifact의 `derived_from`이 바뀌어 set 전체를 다시 bless하고 re-pin해야 했습니다(3.7의 9.18 행). audit A2는 이 비용을 미리 적었습니다. "Adding the field changes timeline blobs, hence `meta.derived_from`, hence artifact hashes → re-bless and re-pin."

**무엇이 강제하나.** library 쪽은 `lint_repo`(숫자 parameter마다 tag가 있고 registry에서 풀리고 locator 형식이 맞는지, registry의 모든 id가 `docs/references.md`에 있는지), timeline 쪽은 `lint_bound_sources`(key 집합이 양방향으로 같고, tag가 registry에 있는지)입니다. 둘 다 `make lint`에서 돌고, generated timeline에 대해서는 `generate.py`가 생성할 때 돌립니다. test로는 `test_lint.py::test_real_timelines_bound_values_are_sourced`와 13개 경우를 가진 `test_bound_values_carry_a_source_tag_or_a_label`이 있습니다. 9.18 changelog D2는 lint의 한계도 적습니다. "the lint checks form, not that each tag is the right ground". tag가 올바른 근거인지는 9.16(최종 audit)이 `bound-values.md`와 대조해 확인할 일로 넘겨져 있습니다.

## 8.5 규칙 4 · The generated layer is design

**규칙.** "A generated file composes or renames the C1 task sets by `grids.yaml`'s rules and claims nothing about real desktops; its only authored numbers and names are the definition's, each number with a source or a label, the tier-4 name table design and the tier-3 names sourced. The values the generator scales (a batch job's work over its span) are `design` in the file's `source` map; the ones it carries unchanged keep the C1's tags."

**기록된 이유.** Phase 9 spec decision 9(2026-10-11 추가)가 generated layer를 만들며 이 성격을 정했습니다. "A generated layer stands beside the core set. Each group whose claim is a rate has a generated set that enumerates the factor in full from the C1 task sets, labelled design with no realism claim; the authored files remain as existence cases. The naturalistic set stays in the backlog." 배경은 2026-10-11에 인지오가 audit 기록에 남긴 열린 항목입니다. core set의 C3 그룹은 세 개의 arc로 약 여덟 개의 segment 경계만 가지고 있어서 "It cannot carry a statistical claim on transition recognition (RQ1), on recognition accuracy per cell, or on the phase-shift family (RQ4 …)". 그래서 요인을 빠짐없이 열거하는 설계 집합을 더했고, 그 집합은 실제 desktop에서 어떤 전환이 얼마나 자주 일어나는지에 대해서는 아무 주장도 하지 않습니다. 빈도에 대한 주장은 아직 만들지 않은 naturalistic set의 몫입니다.

이 권의 관점에서는, generated layer가 설계라는 사실이 "commit하지 않는다"는 결정과 맞물립니다. generated timeline은 사람이 쓴 것이 아니라 정의(`grids.yaml`)와 C1 timeline에서 순수하게 계산된 것이므로, 정의와 generator와 manifest만 commit하면 됩니다(1.5, 2.9).

**무엇이 강제하나.** `generate.py`가 생성 시점에 모든 generated timeline에 bound-source lint, loader의 구조 검사, canonical lint를 돌립니다(README: "The generated timelines pass the same lints as the authored ones … at generation"). `lint_grids`가 정의의 모양과 간격 값의 출처, 그리고 모든 이름이 kernel의 15자 `comm` 한계 안에 있는지 봅니다. `comm`은 Linux kernel이 process마다 저장하는 실행 파일 이름으로, `TASK_COMM_LEN`이 NUL 포함 16바이트라서 15자까지만 보입니다(`docs/references.md`의 `linux-sched-h`). `test_generated.py`의 `test_an_unscaled_bound_value_keeps_its_source_tag`가 "scale하지 않은 값은 C1의 tag를 유지한다"를 확인합니다.

## 8.6 규칙 5 · A derived file's keystrokes are its base's

**규칙.** "A derived input window lying inside a base window of its task is written as that window's slice (`slice_of: {from, to, index}`, the deriver's doing), and the compiler draws the stimulus offset for the base window, so a counterpart's keystrokes are byte-identical to its base's over the slice."

C7 그룹의 interactive counterpart는 C1 base의 처음 C초를 잘라 원하지 않은 배경 작업(package upgrade, C = 26.385 s)을 더한 파일입니다. 이 규칙은 잘라 낸 구간의 키 입력이 base의 같은 구간 키 입력과 같은 시각이어야 한다는 것입니다.

**기록된 이유.** 2026-10-10 audit의 A1입니다. compiler는 각 input 창의 stimulus offset을 `uniform(seed, iid, "stimulus", j) × (span − window length)`로 뽑았는데, counterpart의 창은 22.385초이고 base의 창은 56초라서 같은 seed로도 다른 offset이 나왔습니다. audit의 표는 처음 26.385초 안에서 base와 counterpart가 공유한 keystroke 시각이 browsing 0개, office 0개, dev 0개였다고 적습니다. 9.10 D41(counterpart는 base의 처음 C초라는 결정)이 의도한 바와 달랐고, 그 의도를 적은 고정된 문장들(pair review, scoring spec의 주석)이 틀린 상태였습니다. audit는 두 선택지 중 compiler 규칙을 권했습니다. "(ii), it realises the recorded decision and makes the pinned sentences true". 9.18 spec decision 1–3이 그것을 구현했습니다.

**무엇이 강제하나.** deriver가 `set-input` op에서 base 창 안에 놓인 새 창에 `slice_of`를 자동으로 씁니다(9.18 spec decision 2: "The author's variant spec does not restate the base's windows"). test는 등식이 아니라 부분집합입니다. 9.18 spec decision 3은 "Equality is not asserted: the counterpart's operations sit at their own positions (9.10 D44), and the compiler drops the keystrokes that fall inside an operation"이라고 적습니다. 여기서 9.10 D44는 잘라 낸 파일이 base의 operation(예: 페이지 로드)을 비례해 다시 배치한다는 재배치 규칙입니다. `test_c7_input_wakes_are_a_subset_of_the_bases_in_the_first_c_seconds`가 그 부분집합을 확인하고, 9.18 changelog D6은 rebuild 후의 숫자를 적습니다. "browsing 85 → 79 (the six inside the page load), office 102 → 91, dev 47 → 47, mail 0 → 0, indexing 46 → 27, compile 2354 → 358, ml-train 1844 → 1628; every counterpart's set a subset of its base's."

## 8.7 규칙 6 · Demand window — 은퇴한 규칙

**README의 문장.** "Every compiled `-single` file of demand class `oversubscribed` must land in the ~100–150% window by the static estimate (`compile.py` prints per-file demand and records it under `demand` in the manifest); `calibration` files are exempt. Files outside it get redesigned, not waved through."

**지금의 사실.** 이 규칙은 2026-10-09에 gate에서 은퇴했습니다. 9.14 spec decision 4의 문장은 "The demand window retires as a gate. The compiler records demand per file, as now, and per segment, newly, in the manifest, and never fails on it." 코드도 그렇습니다. `wlc/estimate.py`의 docstring은 "retired as a gate on 2026-10-09 (9.14 decision 4)"라고 적고, 어떤 lint도 창을 확인하지 않습니다. test 두 개가 오히려 반대를 단언합니다. `test_lint.py::test_no_demand_window_gates_a_file`은 수요가 1/3인 `oversubscribed` 파일이 lint를 통과함을, `test_coreset.py::test_no_file_fails_on_its_demand`는 51개 파일 모두가 수요와 상관없이 lint를 통과함을 확인합니다(7.5). 2026-10-14의 core manifest에서 `oversubscribed` 11개 중 10개가 이 창 밖에 있고, 창 안은 `c2-p2b`(1.2706) 하나입니다(예: `c2-p1a` 14.505, `c6-dual` 0.8388, `c2-p3a` 0.4401).

**은퇴의 기록된 이유.** 9.13의 reads R5가 bless 시점에 `oversubscribed` 파일 열 개 중 아홉 개가 창 밖에 있음을 보였고, 그 원인이 설계였습니다. "`c2-p1a`'s and `c2-p2a`'s demands follow the training run and the download bound whole at their CPU totals (9.10 D17, D90, D142) inside short files." 괄호의 세 결정은 학습 run과 다운로드 같은 batch job을 측정된 CPU 총량 그대로 묶기로 한 sub-task 9.10(scenario와 timeline 연구)의 결정들입니다. 즉 측정된 CPU 총량을 그대로 쓰는 원칙과 창을 맞추는 원칙이 충돌했고, 측정을 택했습니다. building plan §5a는 이제 `oversubscribed`를 "a file designed to hold contention"으로, 그 수요를 "a measured fact"로 적습니다(2.7).

**README가 아직 이 규칙을 적고 있는 이유.** README의 이 절과 coreset 표의 "lane-scaled so total demand targets one CPU lane (~100–150%)"는 9.14 이전 상태 그대로입니다. 이 정정은 9.15(문서 정비)의 작업 목록에 있습니다(`_dev/TODO.md`의 9.15 줄: "`dataset/README.md` … the demand window stated as a rule"). 이 권은 은퇴한 규칙을 현재 규칙으로 옮기지 않습니다. 현재의 규칙은 "수요는 파일별, segment별로 manifest에 기록되고, 어떤 파일도 수요 때문에 실패하지 않는다"입니다.

## 8.8 규칙 7 · Zero `meas-pending`

**규칙.** "The library is fully measured; the linter keeps it that way."

`meas-pending`은 측정 전의 임시값에 붙이던 source tag입니다. building plan §1은 "Entries tagged `meas-pending` ship with placeholder values and are finalized from the CI measurement campaign (§7); the linter accepts `source: meas-pending` only until freeze"라고 적습니다.

**기록된 이유.** building plan §6의 CI 실패 조건 목록에 "`meas-pending` after freeze"가 있고, 그 목적은 8.4의 Payoff 문장입니다. 임시값은 외부 근거도 공개된 측정도 아니므로, freeze 이후에는 남아 있으면 안 됩니다.

**무엇이 강제하나.** 정확히 말하면 `make lint`가 아니라 `make test`입니다. `dataset/Makefile`의 `lint` target은 `lint.py`를 `--freeze` 없이 부르므로 `meas-pending`을 거부하지 않습니다(`_check_param`은 `freeze`가 참일 때만 "meas-pending after freeze"를 냅니다). freeze 검사는 `test_lint.py::test_repo_is_freeze_clean`이 `lint_repo(…, freeze=True)`로 하고, 그 docstring은 "All meas-pending placeholders have been folded in (cli:3/gui:2)"입니다. `test_freeze_rejects_meas_pending`은 같은 entry가 freeze 없이는 통과하고 freeze에서는 "probe.x: meas-pending after freeze"로 실패함을 확인합니다. README의 "the linter keeps it that way"는 linter 함수가 test 안에서 freeze mode로 돌기 때문에 맞는 말입니다.

## 8.9 규칙 8 · Declared class on every entry and every task

**규칙.** "The repo lint requires `declared_class` on every archetype entry, from the closed set `normal` and `idle`, with no default; the schema requires it on every `arrive` event and spawn-table entry; the tests check that each compiled task carries its bound entry's class."

`declared_class`는 실제 program이 스스로 선언하는 scheduling class입니다. Linux에서 process는 자신을 `SCHED_IDLE` 같은 class로 둘 수 있고, `idle` class의 task는 다른 class의 task가 실행 가능한 동안에는 CPU를 받지 못합니다. 이 dataset에서는 `file-indexer`(Tracker가 모든 thread를 `SCHED_IDLE`로 둠)와 `incremental-backup`(Déjà Dup이 `chrt --idle 0`으로 시작함)이 `idle`이고, 나머지는 `normal`입니다(2026-10-08 memo).

**기록된 이유.** 2026-10-08의 memo `docs/memos/2026-10-08-declared-scheduling-class.md`와 9.13 spec decision 2입니다. memo는 이 field를 "The scheduling policy a program sets for itself, read from its source and from the class census of the carried work"라고 정의하고, simulator의 executor 규칙을 함께 정했습니다. "A task whose class is `idle` runs only when no task of another class is runnable, and a task of another class that becomes runnable preempts it at once." 여기서 `preempt`는 실행 중인 task를 중간에 내려놓고 다른 task에게 CPU를 넘기는 것입니다. 그리고 "never read from its name"의 이유도 적습니다. "A task carries the class of the entry it binds, never one inferred from its name: `c5-t3` shows two media players as `tracker-miner-f` and `baloo_file`, and they stay `normal`." 이름을 indexer처럼 바꾼 media player가 행동까지 idle이 되면, 이름과 행동을 분리한 규칙 2가 깨집니다(`c5-t3`는 지금의 `c6-alias`입니다).

**무엇이 강제하나.** 세 겹입니다. repo lint가 library의 모든 entry에 field를 요구합니다(`REQUIRED_ARCHETYPE_FIELDS`, `DECLARED_CLASSES = {"normal", "idle"}`). schema가 모든 `arrive` event와 spawn-table entry에 field를 요구하므로 canonical lint가 compile마다 확인합니다. test가 compiled task의 class가 bound entry의 class와 같은지 봅니다(`test_canonical.py::test_tasks_carry_their_entrys_declared_class`, `test_schema_requires_declared_class_on_every_task_record`, `test_lint.py::test_repo_lint_requires_declared_class`, `test_library_declared_classes`). 9.13 spec decision 8은 이 lint와 test를 "Four [lints and tests], and no more"라고 범위를 정했습니다.

## 8.10 규칙 9 · TIMER first

**규칙.** "A compiled program that contains a TIMER anywhere has a TIMER as its first executed instruction — a LOOP head's body counting — so TIMER's t₀, its first execution, is the task's arrival (canonical lint; `docs/harness/metrics.md` §11)."

`TIMER(period)`는 canonical program의 primitive 중 하나로, 기준 시각 t₀에서 `t₀ + k·period`마다 task를 깨웁니다. 영상 재생처럼 주기적으로 일하는 task가 이것을 씁니다. `LOOP`는 program의 반복 구조이고, 반복 몸체의 첫 명령이 TIMER면 그것도 첫 명령으로 칩니다.

**기록된 이유.** 9.13 spec decision 8이 sub-task 9.11(scheduler 쪽 상수 연구)의 D11과 D33을 적용한 것입니다. `wlc/linter.py`의 주석이 이유를 적습니다. "a TIMER-carrying program begins, in execution order, with its TIMER — a LOOP head's body counting — so TIMER's t₀, its first execution, is the task's arrival and the two cannot come apart silently". harness의 metrics 문서 §11 item 4는 이 규칙이 무엇을 가능하게 하는지 적습니다. "Every periodic task's first executed instruction is its TIMER — the dataset lint enforces it since 9.13 — so `t₀` is the task's first dispatch". harness는 주기 task의 deadline을 t₀ 기준의 격자로 재는데, TIMER 앞에 RUN이 있으면 t₀가 도착 시각과 어긋나고, 그 어긋남이 조용히 측정값에 섞입니다.

**무엇이 강제하나.** canonical lint가 compile마다 top-level program과 spawn-table program 모두에서 확인합니다(4.6 사례 10의 메시지). test는 `test_lint.py::test_timer_first_invariant`(parametrize된 여러 program 모양)와 `test_timer_first_invariant_covers_spawned_tasks`입니다. 9.13 reads R2는 bless 시점에 TIMER를 가진 task 22개가 모두 통과했다고 적습니다(LOOP head로 7개, 문자 그대로 15개).

## 8.11 README 안의 다른 오래된 문장들

이 권의 주제와 맞닿는 README의 오래된 문장을 모아 둡니다. 모두 9.15(문서 정비)의 정정 범위에 있거나 그 범위에 넣을 수 있는 것들입니다.

| README의 문장 | 지금의 사실 | 근거 |
|---|---|---|
| Commands: "Needs Python 3.12+ with `pip install -r tools/requirements.txt` (PyYAML, jsonschema, pytest)" | `jsonschema-rs`와 `numpy`도 있고 `jsonschema`는 없음 | `dataset/tools/requirements.txt`, 9.22 D3(schema validator를 `jsonschema-rs`로 바꾼 결정) |
| Rules: "Demand window … must land in the ~100–150% window" | 은퇴. 기록만 하고 실패시키지 않음 | 9.14 decision 4(demand window의 은퇴), 이 권의 8.7 |
| Coresets 표: "lane-scaled so total demand targets one CPU lane (~100–150%)" | 위와 같음 | 같음 |
| Commands: "`build/` 6.8 GB of the runner's 14 GB of storage with the core set's 0.7 GB beside it" | 6.8 GB가 core set을 이미 포함함. `coreset-single/`은 variant까지 1.6 GB | `du`, 6.6 |
| Layout: `launch/`, `replay/`, `stimulus/` 디렉터리가 없음 | compile이 셋 다 읽음 (launch는 manifest가 pin하지 않음) | 2.4 |

---

# 9장 · 용어 정리

이 권에서 풀어 쓴 용어를 모읍니다. 앞의 무리는 이 저장소가 만든 이름이거나 이 저장소만의 뜻으로 쓰는 말이고, 뒤의 무리는 웹 개발에서는 잘 만나지 않는 운영체제와 scheduling의 말입니다. 괄호 안은 처음 나온 곳입니다.

## 9.1 이 저장소의 용어

**build와 그 산출물**

- `timeline` — 사람이 쓰는 workload 설계 파일. 시간축 위에 segment, task, focus를 적은 YAML입니다. (1.1)
- `segment` — 같은 상황이 이어지는 구간과 그 정답 label. (1.1)
- `focus` — 어느 창이 사용자의 window focus를 가졌는지를 적은 track. (1.1)
- `artifact` — compiler가 timeline 하나에서 만든 canonical workload 파일, `build/<set>-single/<id>.workload.json`. (1.1)
- `wlc` — 이 저장소의 workload compiler, `dataset/tools/wlc/`. (1.1)
- `canonical bytes` — artifact를 바이트로 쓰는 단 하나의 형태. key를 정렬하고 공백 없이 쓴 JSON에 줄바꿈 하나를 붙인 것입니다. (1.4)
- `run file` — artifact에서 `events`만 남긴, simulator가 실제로 읽는 view. (1.2)
- `compile report` — compiler가 artifact 옆에 쓰는 수요 정보 JSON(`<id>.report.json`). 지금은 blessed artifact의 하나입니다. (2.6)
- `utilization` — 파일의 모든 task가 요구하는 CPU 시간을 파일 길이로 나눈 compile 시점의 정적 추정치. (2.6)
- `demand_class` — timeline이 선언하는 설계 의도. `oversubscribed`는 경합을 담도록 설계한 파일, `calibration`은 그렇지 않은 파일입니다. (2.7)
- `demand window` — `oversubscribed` 파일의 수요가 lane의 약 100–150 %여야 한다던 규칙. 2026-10-09에 gate에서 은퇴했습니다. (2.7, 8.7)
- `keyed draw` — 전역 난수열 대신 `(seed, task id, parameter, 순번)` 같은 주소를 SHA-256으로 hash해 얻는 난수. 다른 task를 더하거나 고쳐도 값이 밀리지 않습니다. (1.3)
- `derived timeline` (파생 timeline) — variant recipe가 base timeline에 op를 적용해 만든 commit되는 timeline. `# GENERATED by dataset/tools/derive.py` 머리글을 가집니다. (4.3)
- `variant recipe` — 파생 timeline을 만드는 `*.variant.yaml` 파일. (4.3)
- `deriver` — variant recipe를 실행하는 `wlc/deriver.py`. (4.3)
- `slice_of` — 파생 파일의 input 창이 base의 어느 창을 잘라 낸 것인지 적는 field. compiler는 base 창 기준으로 stimulus offset을 뽑습니다. (8.6)
- `stimulus stream` — 실제 키 입력 기록(SWELL-KW)에서 뽑은 키 입력 시각열, `dataset/stimulus/`. (2.4)
- `replay stream` — 측정에서 관찰한 wake 순서 전체를 재생용으로 담은 파일, `dataset/replay/`. (2.4)
- `launch stream` — application이 파일 중간에 시작될 때의 시작 단계 wake를 담은 파일, `dataset/launch/`. compiler가 읽지만 manifest의 `inputs`에는 없습니다. (2.4)
- `build product` — 입력에서 언제든 다시 만들 수 있어 commit하지 않는 산출물. `build/`와 `generated/`가 그렇습니다. (1.5)

**집합과 그룹**

- `core set` (`coreset`) — 사람이 설계한 51개 workload. RQ0 실험이 이 위에서 돕니다. (2.2)
- `C1`–`C7` — core set의 일곱 그룹. C1 calibration(한 파일에 한 mode), C2 intent pair(한 segment에서만 다른 쌍), C3 transition arc(여러 mode를 이은 하루), C4 distractor injection(상황 중에 무관한 process가 끼어듦), C5 familiarity ladder(같은 행동, 낯선 이름), C6 resolution limit(이름만으로는 원리적으로 못 맞히는 경우), C7 attribute counterpart(원하지 않은 배경 작업을 더한 파생 파일). (1.4, 7.4)
- `mode` — 사용자의 상황 이름. 16개가 있고 segment의 정답 label입니다. (2.2)
- `sensitivity variant` — RQ0 gate spec이 결론의 견고함을 보려고 쓰는, core 파일을 한 방식으로 변형한 사본. 아홉 set, 78개입니다. (2.2, 2.8)
- `generated layer` — C1 task set을 규칙으로 조합한 다섯 설계 집합(transition grid, return grid, flap-stress, distractor grid, familiarity ladder), 1,562개. (2.2)
- `generated timeline` — generator가 cell마다 쓰는, commit되지 않는 timeline, `dataset/generated/<set>/`. (1.5)
- `grid record` — generated manifest의 `grid` section에서 파일 하나의 좌표, split, placements, segment label을 적은 항목. (2.9)
- `placement` — generated 파일 안에 한 mode의 C1 task set이 어떤 id 접미사로 어느 segment에 들어갔는지의 기록. (2.9)
- `split` — return grid와 flap-stress 파일이 tuning 절반과 measurement 절반 중 어디에 속하는지. (2.9)
- `tier` — process 이름이 얼마나 알아보기 쉬운지의 단계, 1–5. (2.9)
- `background_wanted` — segment의 배경 작업을 사용자가 원했는지의 정답 attribute. (2.9)
- `pre-committed miss` — 이름과 행동만으로는 어떤 인식기도 맞힐 수 없다고 미리 선언한 segment. (2.9)
- `coverage grid` — driver-table cell마다 segment 수를 센 표, `dataset/coverage-grid.json`. (2.10)
- `driver-table cell` — configuration 표의 32개 행, 즉 16개 mode × `background_wanted`의 참·거짓. (2.10)
- `judging file` / `reporting file` — RQ0 판정에 쓰이는 19개 파일 / 보고만 하는 32개 파일. (2.8)

**고정과 검증**

- `manifest` — build 하나의 입력과 출력을 hash로 고정한 committed JSON, `dataset/build*.manifest.json`. 일곱 개가 있습니다. (2.1)
- `inputs` — manifest에서 build가 읽은 파일의 경로 → SHA-256. core 23개, generated 45개, variants 3개. (2.4)
- `artifacts` / `reports` — manifest에서 build가 쓴 artifact와 report의 경로 → SHA-256 (variants는 record). (2.5, 2.6)
- `demand` — manifest에서 파일별·segment별 utilization과 demand class. (2.7)
- `grid` — generated manifest에만 있는, 파일별 grid record. (2.9)
- `git blob hash` — `git hash-object`와 같은 SHA-1. artifact의 `meta.derived_from`과 `meta.sampled.archetypes`에 쓰입니다. manifest의 SHA-256과 다른 값입니다. (2.3)
- `bless` — build를 다시 돌려 manifest를 새로 쓰고 그것을 commit하는 것. `re-bless`도 같은 뜻입니다. (3.2)
- `blessed build` — 디스크의 `build/`가 committed manifest와 hash 단위로 일치하는 상태. (3.2)
- `pin` — 다른 파일이 이 파일의 SHA-256을 적어 두고 실행 전에 지금의 바이트와 대조하는 것. (3.3)
- `re-pin` — dataset이 다시 bless되어 manifest hash가 바뀌었을 때 RQ0 gate spec의 pin을 새 값으로 고치고 harness changelog에 항목을 남기는 것. (3.4)
- `pins.generated` / `files.select` — 실험 사양이 generated manifest를 pin하고 그 grid record의 key로 파일을 고르는 장치(9.21). (3.6)
- `gate` — `make -C dataset check`. 파생 파일과 coverage의 drift, 일곱 manifest가 committed 바이트와 같은지, `build/`가 그 합집합과 같은지를 봅니다. (4.1)
- `check_committed` — 디스크의 manifest를 `git show HEAD:<path>`의 바이트와 비교하는 `check_build.py`의 함수. (4.4)
- `derive drift` / `grid drift` — 파생 timeline이 recipe와, `coverage-grid.json`이 다시 계산한 표와 다른 상태. (4.3)
- `canonical lint` — compile마다 artifact에 도는 검사: schema, event 정렬, id 유일성, TIMER-first, FORK와 spawn table, WAKE 대상과 channel, focus 구간. (5.5)
- `coreset` fixture — dataset test가 51개 (artifact, report)를 얻는 장치. hash가 manifest와 맞으면 blessed build를 읽고, 아니면 compile합니다. (7.3)
- `coreset_wide` — harness의 두 test에 붙은 pytest marker. CI의 `make -C harness test`는 이 둘을 빼고, 집에서 `make -C harness test-full`이 돌립니다. (6.10)
- `smoke` — mock daemon과 mock simulator로 scored core 파일 전부에 pipeline 전체를 돌리는 `make -C harness smoke`. (5.11)
- `mock daemon` / `mock simulator` — 진짜 daemon과 simulator가 나오기 전까지 같은 호출 계약으로 대신 도는 harness의 test용 program. (6.10)

**실험 쪽**

- `harness` — 실험 실행기. run matrix를 돌리고, 인식을 채점하고, trace에서 성능 지표를 계산하고, 보고서를 씁니다. (1.2)
- `condition` — workload 하나를 받아 configuration schedule을 내놓는 함수. RQ0에서는 `fixed`, `random`, `oracle`입니다. (1.2)
- `oracle` — workload 파일의 정답을 읽어 인식하는 조건. 완벽한 인식이지 완벽한 configuration은 아닙니다. (1.2)
- `RQ0` — 첫 연구 질문. 모델 없이, configuration 선택이 이 workload들에서 측정 가능한 차이를 만드는가. (1.2)
- `RQ0 gate spec` — RQ0 실험의 사전 등록 파일, `harness/experiments/rq0-gate.yaml`. 조건, 판정 파일, 기준, 보고 항목, pin을 담습니다. (1.2, 3.3)
- `scoring spec` — 파일별 성능 항과 가중치를 정한 frozen 파일, `harness/scoring/scoring-spec.yaml`. (3.3)
- `guard spec` — run이 숫자를 읽히기 전에 통과해야 하는 여덟 guard를 정한 frozen 파일, `harness/guards/guard-spec.yaml`. (3.3)
- `driver table` / `prior table` — mode × `background_wanted`의 32행에서 configuration으로 가는 표 / 그중 측정 전에 이론으로 쓴 판, `daemon/driver-table/prior.yaml`. (3.3)
- `interpretation contract` — canonical workload의 op와 field의 의미를 정하는 문서, `docs/simulator/interpretation-contract.md`. (8.2)

**입력 쪽**

- `archetype` — 한 종류의 process 행동을 측정된 분포로 적은 library entry. (8.3)
- `library` — archetype 29개를 담은 `dataset/archetypes.yaml`. (2.3)
- `binding_params` — archetype이 timeline에서 값을 받을 수 있다고 선언한 손잡이 목록. (8.3)
- `source` tag / `source` map — 숫자의 출처. library에서는 parameter마다, timeline에서는 `bind`와 같은 key를 가진 map으로 답니다. 값은 registry tag, tag의 목록, 또는 `design`·`convention`·`arithmetic` label입니다. (8.4)
- `meas-ci:<workflow>:<date>` — 이 저장소의 GitHub Actions 측정 campaign에서 온 값의 source tag. (6.11, 8.4)
- `meas-pending` — 측정 전 임시값에 붙이던 tag. freeze 이후 금지입니다. (8.8)
- `declared_class` — program이 스스로 선언하는 scheduling class, `normal` 또는 `idle`. (8.9)
- `TIMER` / `t₀` — `t₀ + k·period`마다 task를 깨우는 program primitive / 그 격자의 기준 시각, task의 첫 TIMER 실행. (8.10)
- `LOOP` — program의 반복 구조. 반복 몸체의 첫 명령이 TIMER면 첫 명령으로 칩니다. (8.10)
- `RUN` — task가 CPU를 정해진 µs만큼 쓰는 program 명령. (1.3)
- `FORK` / `spawn table` — child process를 만드는 명령 / compiler가 미리 sampling한 child program 목록. (5.5)
- `WAKE` / `channel` — 다른 task를 깨우는 명령 / task가 `WAIT`로 기다리는 이름 붙은 신호. (5.5)

## 9.2 운영체제와 scheduling의 용어

- `lane` — simulator가 모사하는 CPU 하나. 이 dataset은 single-lane, 즉 CPU 하나에 맞춰 compile합니다. (2.5)
- `wake` — 기다리던 task가 다시 실행 가능해지는 사건. (1.3)
- `scheduling class` — kernel이 task를 어떤 규칙 묶음으로 schedule할지. Linux의 `SCHED_IDLE` class task는 다른 class의 task가 실행 가능한 동안 CPU를 받지 못합니다. (8.9)
- `preempt` — 실행 중인 task를 중간에 내려놓고 다른 task에게 CPU를 넘기는 것. (8.9)
- `comm` — Linux kernel이 process마다 저장하는 실행 파일 이름. `TASK_COMM_LEN`이 NUL 포함 16바이트라 15자까지 보입니다. (8.5)

