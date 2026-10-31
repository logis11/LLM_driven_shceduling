# 3권 · Timeline에서 canonical workload로: 포맷과 compiler

> Status: draft · Created 2026-10-14 · Updated 2026-10-31

**사람이 쓴 timeline 파일 하나가 어떤 규칙으로 simulator가 읽는 workload JSON이 되나.**

---

이 연구의 workload dataset은 세 층으로 되어 있습니다. 맨 아래에는 **archetype** library(`dataset/archetypes.yaml`)가 있습니다. archetype은 "어떤 종류의 프로그램이 CPU를 어떻게 쓰는가"를 적어 둔 행동 모형이고, 29개 중 28개가 CI runner에서 직접 측정한 값입니다(나머지 하나, 게임 chain은 발표 자료에 기댑니다). 이름도, 개수도, 그 프로그램이 무슨 의미인지도 모릅니다. 그 위에 **timeline**(`dataset/timelines/coreset/*.timeline.yaml`)이 있습니다. timeline은 사람이 쓰는 연출 대본입니다. 어떤 이름의 process가 언제 등장해 언제 퇴장하는지, 그 순간 사용자가 실제로 무엇을 하고 있는지(정답 label), 사용자가 어느 창을 보고 어디에 타자를 치는지를 적습니다. 맨 위에는 **canonical workload**(`dataset/build/coreset-single/*.workload.json`)가 있습니다. 이것은 simulator, recognizer를 돌리는 daemon, 채점하는 harness가 실제로 먹는 파일입니다. 확률분포는 하나도 남아 있지 않고, 모든 값이 정수 microsecond로 확정되어 있습니다.

이 권은 가운데와 위 사이, 즉 **timeline이 canonical workload가 되는 길**을 다룹니다. 두 포맷의 field 하나하나가 무슨 뜻인지, 그리고 둘 사이를 잇는 compiler **wlc**(workload compiler, `dataset/tools/wlc/`)가 어떤 순서로 무엇을 하는지를 설명합니다. archetype이 어떻게 측정되었는지는 archetype library를 다루는 권에서, 51개 coreset 파일이 각각 어떤 질문에 답하는지는 coreset 파일을 하나씩 다루는 권에서, 1,562개의 generated 파일은 generated layer를 다루는 권에서, 민감도 variant와 build gate의 CI 운영은 각각 그 주제를 다루는 권에서 설명합니다. 이 권은 그 모든 권이 공유하는 "문법책"에 해당합니다. 설명하는 것은 2026-10-14 기준의 tree이고, 그 뒤 2026-10-17까지 바뀐 것(sub-task 9.23이 더한 canonical lint 셋과 program의 끝 규칙, launch stream의 고정, sub-task 9.15 안에서 지운 compiler 경로, timeline 머리 주석의 생략 문장, schema의 설명과 compiler·loader의 docstring)은 해당 절에 반영했습니다. 포맷과 compiler는 2026-08-27(Phase 2, 처음 compiler를 만든 날)부터 2026-10-17(sub-task 9.15 안에서 정한 dataset 수정이 두 번째 rebuild로 들어간 날)까지 여러 번 바뀌었고, 각 변화가 언제 왜 일어났는지는 15장에, 문서와 tree가 어긋나는 곳은 16장에 모았습니다.

웹 개발자의 세계에 비유하면 이렇습니다. timeline은 사람이 손으로 쓰는 `package.json`이고, canonical workload는 기계가 만든 `package-lock.json`입니다. lockfile에는 "대략 이 버전쯤"이 없고 정확한 해시가 박혀 있듯, canonical workload에는 "평균 5 ms쯤"이 없고 `{"op":"RUN","us":4832}` 같은 확정된 숫자만 있습니다. 그리고 같은 `package.json`과 같은 registry 상태에서 같은 lockfile이 나와야 하듯, 같은 timeline과 같은 archetype library와 같은 seed에서는 바이트 하나까지 같은 workload가 나와야 합니다. 이 결정성이 왜 실험의 생명줄인지, compiler가 그것을 어떻게 지키는지가 이 권의 중심 이야기입니다.

---

## 목차

1. [1장 · 이 권이 다루는 것](#1장--이-권이-다루는-것)
2. [2장 · Timeline의 뼈대: meta와 segments](#2장--timeline의-뼈대-meta와-segments)
3. [3장 · Timeline의 등장인물: tasks](#3장--timeline의-등장인물-tasks)
4. [4장 · 사용자를 그리는 세 track: input, focus, operations](#4장--사용자를-그리는-세-track-input-focus-operations)
5. [5장 · Variant recipe와 deriver](#5장--variant-recipe와-deriver)
6. [6장 · 두 timeline을 줄 단위로 읽기](#6장--두-timeline을-줄-단위로-읽기)
7. [7장 · Canonical workload 포맷](#7장--canonical-workload-포맷)
8. [8장 · 누가 어느 key를 읽나](#8장--누가-어느-key를-읽나)
9. [9장 · Compiler의 큰 흐름](#9장--compiler의-큰-흐름)
10. [10장 · Seed와 결정성](#10장--seed와-결정성)
11. [11장 · Archetype마다 다른 전개](#11장--archetype마다-다른-전개)
12. [12장 · Demand 추정과 compile report](#12장--demand-추정과-compile-report)
13. [13장 · Compile 안의 canonical lint와 manifest](#13장--compile-안의-canonical-lint와-manifest)
14. [14장 · Compile 전의 lint](#14장--compile-전의-lint)
15. [15장 · 포맷이 지금 모양이 되기까지](#15장--포맷이-지금-모양이-되기까지)
16. [16장 · 어긋난 문서와 열린 자리](#16장--어긋난-문서와-열린-자리)
17. [17장 · 용어 정리](#17장--용어-정리)

---

# 1장 · 이 권이 다루는 것

이 장은 "왜 포맷이 두 개이고, 그 사이에 compiler가 있어야 하는가"라는 질문에 답합니다. 이 질문이 먼저인 이유는, 이 구조를 이해하지 않으면 뒤의 모든 규칙이 임의의 관료주의처럼 보이기 때문입니다. 규칙 대부분은 하나의 원칙에서 나옵니다.

## 1.1 두 포맷, 두 독자

**timeline**은 사람이 쓰고 사람이 읽는 포맷입니다. YAML이고, 시간을 `60s`, `99.435s`, `8m30s`처럼 적습니다. 행동의 숫자는 적지 않습니다. 예를 들어 편집기 `code`가 키 하나에 CPU를 몇 µs 쓰는지는 timeline에 없습니다. 그것은 archetype `code-editor`의 몫입니다. timeline은 "`code`라는 이름의 task가 0 s에 나타나 60 s에 닫힌다, 그 행동은 `code-editor` archetype을 따른다, 2 s부터 58 s까지 사용자가 거기에 타자를 친다"만 적습니다.

`task` — 이 dataset에서 simulator가 스케줄하는 실행 단위 하나입니다. 실제 desktop의 process(때로는 process tree 전체)에 대응합니다. `process` — 운영체제가 실행 중인 프로그램 하나에 붙이는 단위입니다.

**canonical workload**(줄여서 workload 파일)는 기계가 쓰고 기계가 읽는 포맷입니다. JSON이고, 시간은 모두 정수 microsecond(µs)입니다. 확률분포가 없습니다. archetype의 이름도 없습니다. task마다 실행할 **program**, 즉 "CPU를 4,832 µs 쓴다 → 입력을 기다린다 → CPU를 120 µs 쓴다 → …" 같은 명령어 목록이 끝까지 풀려 있습니다.

둘을 나누는 이유는 독자가 다르기 때문입니다. timeline은 실험을 설계하는 사람이 "이 장면이 맞는가"를 검토하려고 읽습니다. `c1-dev` 하나만 해도 compile된 program의 명령어가 13,284개입니다. 그런 파일로는 그 검토를 할 수 없습니다. canonical workload는 simulator가 읽습니다. simulator는 확률분포를 해석하지 않아야 합니다(1.2절). 그래서 사람용 포맷과 기계용 포맷을 따로 두고, 그 사이를 compiler가 잇습니다.

> **왜 이렇게 정했나.** 두 포맷의 분리는 2026-08-26의 workload-generation grill에서 정해졌습니다(`_dev/archive/2026-08-26-workload-generation-grill.md`, D9). 그 결정은 입력 파일을 **timeline**(`*.timeline.yaml`), 즉 "segments + labels + bindings of (name, archetype) on a time axis"라고 부르고, 파이프라인을 `archetypes.yaml + timeline (+ scenario catalog) + seed → workload`로 정했습니다. 기록된 이유는 이렇습니다. 손으로 쓰는 core timeline과 나중에 만들 naturalistic generator가 모두 timeline을 내보내면 "one compile path, so linter/invariants/provenance apply uniformly", 즉 compile 경로가 하나라서 lint와 불변식 검사와 출처 추적이 모든 파일에 똑같이 적용됩니다.

## 1.2 지배 원칙: randomness는 compile이, timing은 run이

이 dataset의 포맷 규칙 대부분은 한 문장에서 나옵니다.

> *Compile time resolves all randomness; run time resolves all timing that scheduling can influence.*
> (compile 시점이 모든 무작위성을 확정하고, run 시점이 scheduling이 영향을 줄 수 있는 모든 timing을 확정한다.)

이 문장은 2026-08-26 grill의 D12로 정해졌고, simulator와 dataset 사이의 계약서인 `docs/simulator/interpretation-contract.md` §2에 그대로 적혀 있습니다. 그 계약서는 이 원칙을 두 종류의 시각으로 풀어 씁니다.

- **exogenous(외생) 시각** — 사용자의 행동이라서 scheduler가 바꿀 수 없는 시각입니다. top-level task의 도착, segment 경계, 사용자가 앱을 닫는 시각(segment-bound depart), 키 입력 같은 input wake가 여기에 속합니다. 이 시각들은 canonical 파일에 **절대 시각으로 박혀(pinned)** 있습니다.
- **endogenous(내생) 시각** — scheduling의 결과로 정해지는 시각입니다. 끝이 정해지지 않은 batch job이 언제 끝나는지, `make`가 자식 process를 언제 낳는지가 여기에 속합니다. 이 시각들은 파일에 없습니다. simulator가 돌면서 **창발(emergent)** 합니다.

`scheduler` — 지금 이 순간 CPU를 어느 task에게 줄지 고르는 운영체제의 부품입니다. 이 연구의 실험 대상입니다. `wake` — 무언가를 기다리며 잠들어(block) 있던 task를 다시 실행 가능한 상태로 만드는 사건입니다. 키 입력, timer 만료, 다른 task의 신호가 wake를 일으킵니다.

왜 이렇게 나누어야 할까요. 실험은 "좋은 scheduler 설정"과 "나쁜 scheduler 설정"을 같은 workload에 걸고 결과를 비교합니다. 만약 batch job이 끝나는 시각까지 파일에 박아 두면, 나쁜 설정이든 좋은 설정이든 job이 같은 시각에 끝납니다. 그러면 둘의 차이가 사라집니다. 반대로 사용자가 키를 누르는 시각을 simulator가 그때그때 뽑게 하면, 두 설정이 서로 다른 사용자를 상대하게 됩니다. 그러면 차이가 scheduler 때문인지 사용자 때문인지 알 수 없습니다. 그래서 사용자는 고정하고, scheduler가 만드는 결과는 풀어 둡니다.

웹 세계의 비유로는 부하 테스트를 생각하면 됩니다. 두 서버 설정을 비교하려면 같은 요청 trace를 같은 시각에 재생해야 합니다(외생). 하지만 각 요청의 응답 시각까지 trace에 적어 두면 비교할 것이 남지 않습니다(내생은 풀어 둠).

> **왜 이렇게 정했나.** 2026-08-26 grill의 D10은 lifetime을 이 원칙으로 나눴습니다. 사용자가 닫는 task는 `depart`를 가지고, 끝이 있는 job은 `depart` 없이 program의 `EXIT`로 끝납니다. 기각된 대안이 함께 기록되어 있습니다. "fully pinned arrive+depart trace — open-loop, deletes the good-vs-bad config divergence RQ0 measures"(도착과 퇴장을 모두 박은 trace는 open-loop가 되어, RQ0가 재려는 좋은 설정과 나쁜 설정의 차이를 지운다). D11은 같은 이유로 `FORK`를 run-time primitive로 남겼습니다. 기각된 대안은 "compile-time spawn expansion — pins cc1 arrivals, so a bad scheduler faces the same fork-storm pace as a good one"(자식 process를 compile 때 펼치면 `cc1`의 도착이 박혀서, 나쁜 scheduler도 좋은 scheduler와 같은 속도의 fork 폭풍을 맞는다)입니다.

`RQ0` — 이 연구의 첫 번째 관문 질문, Measurability입니다. 이 workload들에서 scheduler 설정의 선택이 측정할 만큼 결과를 바꾸는지를, 완벽한 인식(oracle)과 무작위 인식을 비교해 묻습니다(`docs/research-proposal.md`의 RQ0 절). 그 차이를 headroom이라고 부릅니다. 판정 규칙은 `harness/experiments/rq0-gate.yaml`(RQ0 gate spec)에 고정되어 있습니다.

## 1.3 파이프라인 한 장

timeline에서 소비자까지 가는 길을 그림으로 보면 이렇습니다.

```
 dataset/timelines/coreset/*.variant.yaml        (recipe: base + ops)
        │  tools/derive.py  →  wlc/deriver.py
        ▼
 dataset/timelines/coreset/*.timeline.yaml       (23 novel + 28 derived, 모두 commit됨)
        │
        │  tools/lint.py   (compile 전 검사: repo / timeline / source lint)
        │
        │  tools/compile.py →  wlc/timeline.py   (load + 구조 검사)
        │                   →  wlc/compiler.py   (sampling, 전개, 정렬)
        │                   →  wlc/linter.py     (canonical lint: schema + 구조)
        │                   →  wlc/estimate.py   (segment별 demand)
        ▼
 dataset/build/coreset-single/<id>.workload.json  + <id>.report.json   (commit 안 함)
 dataset/build.manifest.json                       (commit함: 입력·산출물·report의 hash, demand)
        │
        ├──▶ simulator   : events만 읽음 (run file)
        ├──▶ daemon      : 이름·개수·class·박힌 시각·focus만 읽음 (visible projection)
        └──▶ harness     : ground_truth를 읽어 채점 (oracle 조건과 grader)
```

`make` target으로 보면 `make lint` → `make dataset`(derive 후 compile) → `make variants` → `make generated` → `make test` → `make check` 순서입니다(`dataset/Makefile`, CI는 `.github/workflows/dataset.yml`에서 이 순서로 돕니다). 이 권은 앞의 두 단계, `lint`와 `dataset`을 자세히 다룹니다. `variants`와 `generated`는 같은 compiler를 다른 입력으로 부르는 단계라서 이 권에서는 compiler와 맞닿는 부분만 짚습니다.

> **코드로.** `dataset/Makefile`의 `dataset` target은 두 줄입니다. `$(PY) tools/derive.py`가 recipe로부터 파생 timeline을 다시 쓰고, `$(PY) tools/compile.py`가 모든 timeline을 compile해서 artifact와 report와 manifest를 씁니다. `lint` target은 `tools/lint.py` 한 줄이고 아무것도 쓰지 않습니다.

## 1.4 이 권에서 따라갈 파일들

추상적인 설명보다 파일 하나를 손으로 따라가는 편이 이해가 빠릅니다. 이 권은 다음 파일들을 예제로 씁니다. 각 파일이 coreset에서 맡은 역할은 coreset 권에서 다루고, 여기서는 포맷의 어느 부분을 보여 주는지만 적습니다.

| 파일 | 무엇을 보여 주나 |
|---|---|
| `c1-dev` | 가장 단순한 파일. task 하나, segment 하나, 입력 창 하나. |
| `c1-office` | 단순하지만 task 네 종류, `count: 4`, 그리고 `source` map 하나. 6장에서 줄 단위로 읽습니다. |
| `c2-p1a` / `c2-p1b` | segment 두 개, batch job, `bind`와 `source`, 그리고 recipe로 만든 짝. 6장에서 줄 단위로 읽습니다. |
| `c1-gaming` | chain constructor와 lane scaling. task 두 줄이 arrive event 18개가 됩니다. 6장과 11장에서 손으로 계산합니다. |
| `c7-dev` | 파생 파일의 `slice_of`. base `c1-dev`의 키 입력이 그대로 이어지는 것을 확인합니다. |
| `c1-compile` | spawn table과 `fork_cap`. task 두 줄이 spawn table 17,448칸이 됩니다. |
| `c3-workday` | segment 네 개, focus 이동, `operations`, 중간에 시작하는 앱의 launch phase. |
| `c6-dual` | `ambiguous` segment, focus 18칸, 입력 창 9개, 188 MB짜리 artifact. |

## 1.5 먼저 알아 둘 OS 용어

이 권의 뒷부분은 몇 가지 운영체제 개념을 계속 씁니다. 처음 나올 때마다 다시 풀겠지만, 미리 한 번 모아 둡니다.

- `lane` — 이 연구의 simulator가 가진 CPU 하나입니다. simulator는 CPU가 정확히 하나인 기계를 흉내 냅니다(`interpretation-contract.md` §1, "One lane"). "demand 1.0 lane"은 CPU 하나를 100 % 채우는 만큼의 일이라는 뜻입니다.
- `block` — task가 무언가를 기다리느라 CPU를 쓸 수 없는 상태입니다. 키 입력을 기다리는 편집기, 디스크를 기다리는 backup이 block 상태입니다.
- `preemption` — 실행 중인 task를 scheduler가 중간에 끌어내리고 다른 task에게 CPU를 주는 것입니다.
- `time slice` — task가 CPU를 한 번 잡았을 때 쓸 수 있는 최대 시간입니다.
- `periodic task` — 일정한 주기로 깨어나 일하는 task입니다. 영상 재생기는 33 ms마다 한 장을 그리고, 게임은 16.667 ms마다 한 frame을 만듭니다. 주기마다 마감(deadline)이 있습니다.
- `fork` — process가 자식 process를 만드는 것입니다. `make`가 컴파일러 `cc1`을 띄우는 것이 fork입니다.
- `comm` — Linux 커널이 process마다 기록하는 이름입니다. 끝의 NUL 문자를 포함해 16 byte이므로 보이는 글자는 최대 15자입니다(`include/linux/sched.h`의 `TASK_COMM_LEN`, `docs/references.md`의 `linux-sched-h` 항목). `ps`나 `top`이 보여 주는 이름이 이것입니다.
- `scheduling class` — 프로그램이 스스로 선언하는 scheduling 정책입니다. 이 dataset은 `normal`(기본)과 `idle`(Linux의 `SCHED_IDLE`, 다른 class의 task가 없을 때만 실행) 두 값을 씁니다. `nice`는 normal class 안에서의 가중치이고, class가 아닙니다.

## 1.6 이 권이 인용하는 결정 기록

이 권은 결정을 인용할 때 그 결정이 적힌 기록의 이름과 번호를 붙입니다. 번호만으로는 무엇인지 알 수 없으므로, 이 권에 나오는 기록을 한 번 모아 둡니다. 본문에서는 번호 옆에 그 결정의 내용을 함께 적습니다.

| 기록 | 무엇을 정한 자리인가 | 파일 |
|---|---|---|
| 2026-08-26 grill, D1–D22 | simulator를 만들기 전, workload 생성 방식을 정한 회의. D9–D16이 포맷의 원칙 | `_dev/archive/2026-08-26-workload-generation-grill.md` |
| task 2.3, 결정 1–7 | Phase 2에서 timeline 포맷과 compiler·linter를 처음 정한 spec | `_dev/docs/spec/jioh/task-2.3-timeline-compiler.md` |
| task 2.4, 결정 1–5 | Phase 2에서 recipe·deriver와 첫 core set의 관례를 정한 spec | `_dev/docs/spec/jioh/task-2.4-core-timelines.md` |
| Phase 3, 5, 7 | 검증과 계약 동결(3), 채점 지표(5), driver table 32칸 coverage(7) | `_dev/docs/spec/jioh/phase-*.md`, `_dev/archive/` |
| 9.4 | Phase 9의 게임 연구 slice. `game-task-chain` | `_dev/research/jioh/task-9.4-gaming/changelog.md` |
| 9.5 | 대화형 앱과 타자 연구 slice. 측정된 archetype, 키 입력 재생 | `_dev/research/jioh/task-9.5-interactive-typing/changelog.md`, follow-up spec |
| 9.6 | 컴파일 연구 slice. 빌드와 batch job | `_dev/research/jioh/task-9.6-compile/changelog.md` |
| 9.10 | scenario와 timeline 연구 slice. timeline의 내용 | `_dev/research/jioh/task-9.10-scenarios-timelines/changelog.md` |
| 9.11 | scheduler 쪽 상수 연구 slice. declared class, TIMER 규칙 | `_dev/research/jioh/task-9.11-scheduler-constants/changelog.md` |
| 9.13 | 재건 build. native 삭제, `declared_class`, bless | spec과 `_dev/research/jioh/task-9.13-rebuild/` |
| 9.14 | dataset을 읽는 쪽의 rework. demand window 은퇴, variant | spec과 `_dev/research/jioh/task-9.14-consumer-rework/` |
| 9.15, 9.16 | 문서·memo·guidebook 정정(2026-10-15부터)과 그 안에서 인지오가 정한 dataset·compiler 수정 / 종료 감사(2026-10-17/18) | `_dev/TODO.md`, 9.15의 work list와 chunk log(`_dev/research/jioh/task-9.15-docs-memos-and-guidebook-corrections/`), 9.16의 감사 기록과 인지오의 답(`_dev/research/jioh/task-9.16-exit-audits/`의 `README.md`, `decisions.md`) |
| 9.17 | focus를 telemetry에. `input`과 `focus` track | spec과 changelog |
| 9.18 | compiler, schema, build gate. `slice_of`, `source`, manifest | spec과 changelog |
| 9.19–9.21 | generated layer | spec과 changelog |
| 9.22 | build 시간. `jsonschema-rs`, 병렬 compile | spec과 changelog |
| 9.23 | 이 guidebook이 찾은 어긋남(2026-10-14–15). `c6-fold`·`c6-spoof`의 label, launch stream 고정, `check`의 파생 파일 비교, canonical lint 셋, 의존성 고정, program의 끝 | `_dev/research/jioh/task-9.23-guidebook-findings/changelog.md` |
| memo 2026-10-07, 2026-10-08 | TIMER skip 규칙, declared scheduling class | `docs/memos/` |
| 2026-10-10 audit, A1–A4 | 9.15 전에 dataset 전체를 점검한 기록 | `_dev/docs/audit/jioh/2026-10-10-dataset-audit-before-9.15.md` |

"9.10 D17" 같은 표기는 "sub-task 9.10의 changelog에 적힌 17번째 결정"이라는 뜻이고, "9.14의 결정 4"는 "sub-task 9.14의 spec에 적힌 locked decision 4"라는 뜻입니다. spec의 결정은 grill에서 정한 방향이고, changelog의 D 번호는 그것을 구현하면서 남긴 기록입니다.

---

# 2장 · Timeline의 뼈대: meta와 segments

이 장은 timeline 파일의 앞 두 덩어리, `meta`와 `segments`를 다룹니다. `meta`는 이 파일이 누구이고 어떤 주사위를 쓰는지를, `segments`는 이 파일의 각 순간에 사용자가 "정말로" 무엇을 하고 있는지를 적습니다. 두 덩어리 모두 짧지만, 실험의 정답(ground truth)과 재현성이 여기서 시작됩니다.

## 2.1 timeline 한 파일의 모양

timeline은 YAML 파일 하나입니다. top-level key는 여섯 개이고, loader(`dataset/tools/wlc/timeline.py`의 `Timeline` class)가 정확히 이 이름으로 읽습니다.

| key | 필수? | 한 줄 설명 | compile 후 어디로 가나 |
|---|---|---|---|
| `meta` | 필수 | 파일의 id, seed, demand class | canonical `meta`(id, seed), compile report(demand class) |
| `segments` | 필수, 비어 있으면 안 됨 | 시간 구간마다의 정답 label | canonical `ground_truth` |
| `tasks` | 필수 | 등장하는 process들과 그 행동 모형 | canonical `events`의 `arrive` |
| `input` | 선택(빈 목록 가능) | 사용자가 타자를 치는 창 | canonical `events`의 `wake`(compile 때 소비됨) |
| `focus` | **필수**(빈 목록 가능) | 어느 창이 앞에 있는가 | canonical `focus` |
| `operations` | 선택 | 앱 안의 무거운 동작(페이지 로드, 메일 전송 등) | program 안의 wake 묶음(compile 때 소비됨) |

loader는 이 순서대로 읽습니다. `_load_meta` → `_load_segments` → `_load_tasks` → `_load_input` → `_load_focus` → `_load_operations`. 순서에는 이유가 있습니다. `input`의 규칙(창이 task의 수명 안에 있어야 한다)을 검사하려면 task 목록이 먼저 있어야 하고, `focus`의 규칙(모든 입력 창이 같은 task의 focus 구간 안에 있어야 한다)을 검사하려면 input 목록이 먼저 있어야 합니다.

> **코드로.** `Timeline.__init__`은 파일을 `yaml.safe_load`로 읽고, 동시에 파일 바이트의 git blob hash(`git_blob_hex`, `wlc/library.py`)를 계산해 `self.blob_hex`에 둡니다. 이 hash가 나중에 canonical `meta.derived_from`의 `@` 뒤에 붙습니다(7.2절). 규칙 위반은 모두 `TimelineError`로 던져지고, 메시지 앞에 파일 이름이 붙습니다.

이 표에서 기억할 것은 하나입니다. `segments`와 `focus`와 `tasks`는 canonical 파일에 "보이는 모양으로" 남지만, `input`과 `operations`는 compile 때 **소비**됩니다. canonical 파일에는 "2 s부터 58 s까지 타자를 친다"라는 문장이 없습니다. 대신 그 구간에 떨어진 키 입력 하나하나가 `wake` event로 펼쳐져 있습니다.

## 2.2 `meta`: 파일의 신분증과 주사위

`meta`는 세 개의 key를 가집니다.

```yaml
meta:
  id: c1-office
  seed: 101
  demand: calibration
```

**`id`** — 파일의 이름입니다. 필수입니다. canonical `meta.id`로 그대로 옮겨지고, artifact 파일 이름(`<id>.workload.json`)이 됩니다. 파일 이름(`c1-office.timeline.yaml`)과 `id`가 같아야 한다는 lint는 없지만, 저장소의 모든 timeline은 같게 지어져 있습니다. 파생 파일의 `id`는 deriver가 recipe의 `id`로 덮어씁니다(5장).

**`seed`** — 이 파일의 모든 무작위 추출을 결정하는 정수입니다. 필수이고, 정수가 아니면 loader가 거절합니다(`meta.seed must be an integer`). canonical schema는 0 이상을 요구합니다. seed가 어떻게 쓰이는지는 10장에서 자세히 다룹니다. 지금은 "같은 seed면 같은 주사위 결과"라는 것만 기억하면 됩니다.

core set의 seed는 손으로 정한 고정값입니다. tree에서 읽으면 이렇습니다.

| 묶음 | seed |
|---|---|
| C1, 한 상황만 담은 calibration 파일 16개 | `c1-office` 101, `c1-gaming` 102, `c1-compile` 103, `c1-media` 104, `c1-browsing` 105, `c1-idle` 106, `c1-dev` 107, `c1-video-edit` 108, `c1-photo` 109, `c1-mail` 110, `c1-meeting` 111, `c1-ml-train` 112, `c1-render` 113, `c1-transcode` 114, `c1-indexing` 115, `c1-backup` 116 |
| C2, intent pair의 base 3개 | `c2-p1a` 201, `c2-p2a` 202, `c2-p3a` 203 |
| C3, 여러 상황을 잇는 arc 3개 | `c3-workday` 301, `c3-evening` 302, `c3-creation` 303 |
| C6의 손으로 쓴 파일 1개 | `c6-dual` 601 |
| 파생 파일 28개 | 자기 base의 seed를 물려받음(예: `c7-dev` 107, `c2-p1b` 201, `c5-t4` 104) |

core set의 일곱 묶음(`dataset/README.md`의 Coresets 절). `C1` calibration — mode마다 한 상황만 담은 16개. `C2` intent pair — 같은 전경 옆에서 사용자가 원하는 배경 job과 아무도 요청하지 않은 배경 job(이름과 행동이 다른, 따로 측정된 job)을 견주는 짝 셋과 bounding check 파일 하나, 7개. `C3` transition arc — 여러 상황을 잇는 arc 3개. `C4` distractor injection — C1 파일에 상황을 바꾸지 않는 프로그램을 끼운 3개. `C5` familiarity ladder — 이름만 알아보기 어렵게 바꾼 2개. `C6` resolution limit — 이름 인식이 설계상 실패하는 4개. `C7` attribute counterpart — C1 base의 배경 작업을 원하지 않는 쪽으로 바꾼 16개. 합계 51개입니다(tree에서 `ls dataset/timelines/coreset/*.timeline.yaml | wc -l`로 확인).

> **왜 이렇게 정했나.** seed를 timeline 안에 두는 결정은 task 2.3의 결정 5입니다(`_dev/docs/spec/jioh/task-2.3-timeline-compiler.md`, 2026-08-27). 기록된 이유는 "a timeline is self-contained and `timeline@commit + archetypes@commit` reproduce the bytes", 즉 timeline 하나가 자기완결적이어서 timeline의 commit과 archetype library의 commit만 있으면 바이트가 재현된다는 것입니다. 파생 파일이 seed를 물려받는 규칙은 task 2.4의 결정 4입니다(`_dev/docs/spec/jioh/task-2.4-core-timelines.md`, 2026-08-28). "Each novel base timeline carries a distinct fixed committed seed. Variant specs inherit the base seed and never override it silently … since a changed seed defeats the paired byte-discipline the derivation exists to provide." 짝을 이루는 두 파일이 다른 seed를 쓰면, 바꾼 한 군데 외에도 모든 무작위 값이 달라져서 "딱 이것만 다르다"는 짝의 의미가 무너진다는 뜻입니다.

**`demand`** — 이 파일의 **demand class**입니다. 선택이고, 값은 `oversubscribed`(기본값) 또는 `calibration` 둘 중 하나입니다(`DEMAND_CLASSES`, `timeline.py`). 다른 값을 쓰면 loader가 거절합니다.

`demand class` — 파일이 "CPU 경쟁을 일으키도록 설계되었는가"를 적는 설계 의도 표시입니다. `oversubscribed`는 CPU 하나에 일이 넘치도록 설계된 파일, `calibration`은 경쟁을 일으키려는 설계가 아닌 파일입니다. 이 class는 compile된 파일의 실제 CPU 수요를 말하지 않습니다(12장).

tree에서 세면 `oversubscribed`가 11개, `calibration`이 40개입니다(`dataset/build.manifest.json`의 `demand` 기록에서 `demand_class`를 세어 확인했습니다). `oversubscribed` 11개는 C2(intent pair 묶음)의 7개(`c2-p1a`, `c2-p1b`, `c2-p2a`, `c2-p2a-idle`, `c2-p2b`, `c2-p3a`, `c2-p3b`), C3(여러 상황을 잇는 arc 묶음)의 3개, `c6-dual`입니다. 나머지는 모두 `calibration`을 직접 적었거나, recipe의 `patch-meta`로 적었습니다.

`demand`는 canonical 파일에 들어가지 않습니다. compile report의 `demand_class`와 manifest의 `demand` 기록으로만 갑니다. 이 값이 예전에는 build를 실패시키는 관문이었고 지금은 아닌데, 그 역사는 12장에서 다룹니다.

## 2.3 시간 표기와 `units.py`

timeline의 모든 시간과 길이는 사람이 읽는 문자열로 씁니다. `dataset/tools/wlc/units.py`의 `parse_us` 함수 하나가 그것을 정수 µs로 바꿉니다.

규칙은 단순합니다. 숫자 하나와 단위 하나가 한 덩어리이고, 덩어리를 이어 붙일 수 있습니다. 단위는 `us`(µs), `ms`, `s`, `m`(분), `h`(시간) 다섯 개입니다. 공백은 무시합니다. 결과는 반올림한 정수입니다. YAML에 따옴표 없이 정수만 쓰면 이미 µs인 것으로 봅니다. `true`/`false` 같은 boolean, 음수, 단위 없는 문자열은 거절합니다.

이 권을 쓰며 `python3.12`로 직접 돌려 본 결과입니다.

| 입력 | `parse_us` 결과(µs) |
|---|---|
| `60s` | 60,000,000 |
| `99.435s` | 99,435,000 |
| `8m30s` | 510,000,000 |
| `50ms` | 50,000 |
| `1.5s` | 1,500,000 |
| `17.189821s` | 17,189,821 |
| `2000`(따옴표 없는 정수) | 2,000 |

왜 microsecond이고, 왜 정수일까요. interpretation contract §1은 simulator의 시간을 "Virtual time, discrete-event; integer microseconds throughout (rt-app precedent)"로 정합니다. 가상의 시계가 사건에서 사건으로 건너뛰는 discrete-event simulation이고, 그 시계의 눈금이 정수 µs입니다. 실수(float)를 쓰면 같은 계산이 기계마다 마지막 자리에서 달라질 수 있습니다. 정수는 그렇지 않습니다. 바이트 단위 재현(10장)을 지키려면 시간이 정수여야 합니다.

`discrete-event simulation` — 시계를 일정 간격으로 흘리지 않고, 다음 사건이 일어나는 시각으로 곧장 건너뛰는 simulation 방식입니다. 이 연구의 simulator가 이 방식입니다. `rt-app` — workload 생성 도구로, task 사건의 시간(run, sleep, timer 주기, deadline 매개변수)을 µs 정수로 다룹니다(use case 전체의 길이는 초 단위). contract가 그것을 선례로 듭니다.

## 2.4 `segments`: 시간 구간마다의 정답

`segments`는 파일의 시간축을 구간으로 나누고, 구간마다 "사용자가 정말로 하고 있는 일"을 적습니다. 이것이 canonical 파일의 `ground_truth`가 됩니다. 실험에서 recognizer는 이 정답을 볼 수 없고, 오직 채점자와 정답을 미리 아는 oracle 조건만 봅니다(8장).

`segment` — timeline 시간축의 한 구간입니다. 구간 하나에 정답 label(mode와 attribute) 하나가 붙습니다. `recognizer` — 화면에 보이는 process 이름과 개수 같은 정보를 보고 지금 사용자가 무엇을 하는지 맞히는 부품입니다. 이 연구에서는 LLM, 이름 목록 대조표, 무작위 추측 등이 recognizer 조건입니다. `oracle` — 정답을 그대로 읽는 recognizer 조건입니다. 맞힐 수 있는 최선이 얼마인지를 보여 주는 기준선입니다.

segment 하나는 다음 field를 가집니다(`_load_segments`).

```yaml
segments:
  - {from: 0s, to: 60s, mode: office, attributes: {background_wanted: true},
     scenario: [S1, S2, S4]}
```

- **`from`, `to`** — 구간의 시작과 끝입니다. 필수입니다. `from`이 `to`보다 작아야 합니다.
- **`mode`** — 이 구간의 상황 이름입니다. 필수입니다. recognizer가 고를 수 있는 메뉴의 열여섯 가지 중 하나이거나, 정답으로만 쓰는 특별한 값 `ambiguous`입니다.
- **`attributes`** — mode에 붙는 속성들입니다. 2.5절에서 자세히 봅니다.
- **`scenario`** — 이 조합이 실제 세상에 존재한다는 근거가 되는 scenario catalog의 id 목록입니다(예: `S1` 사무, `S2` 웹 browsing, `S4` 메일). compiler는 이 값을 읽지 않습니다. canonical 파일에도 들어가지 않습니다. 사람과 test와 coverage grid가 읽습니다.
- **`familiarity`** — 이 구간에 보이는 process 이름들이 얼마나 알아보기 쉬운지를 나타내는 등급 1–5입니다. 선택입니다. 적었을 때만 canonical 파일로 옮겨집니다.

`mode` — 사용자가 하는 일의 이름입니다. 메뉴는 열여섯 개입니다. `browsing`, `office`, `mail`, `dev`, `photo`, `meeting`, `gaming`, `media`, `video-edit`, `compile`, `ml-train`, `render`, `transcode`, `indexing`, `backup`, `idle`(`docs/recognition-vocabulary.md` §1). `scenario catalog` — 어떤 process들이 실제 desktop에서 함께 돌아가는지를 S1부터 S18까지 정리한 문서입니다(`docs/workload/scenario-catalog.md`). 예를 들어 S11은 소프트웨어 개발, S17은 malware scan입니다.

loader가 segments에 거는 규칙은 다섯 가지입니다.

1. 목록이 비어 있으면 안 됩니다(`missing segments track`).
2. 각 segment에 `from`, `to`, `mode`가 있어야 하고, `from < to`여야 합니다.
3. `familiarity`를 적었다면 1부터 5 사이의 정수여야 합니다.
4. `background_wanted` 규칙(2.5절)을 지켜야 합니다.
5. 시작 시각으로 정렬한 뒤 서로 겹치면 안 됩니다(`segments overlap at … µs`).

loader가 **하지 않는** 검사도 알아 둘 만합니다. segment들이 0 s부터 빈틈없이 이어져야 한다는 규칙은 없습니다. 실제로는 모든 core 파일이 빈틈없이 이어지지만, 그것은 저자의 관례입니다. 그리고 `mode`가 메뉴의 열여섯 개나 `ambiguous` 중 하나인지는 loader가 아니라 coverage grid 생성기(`wlc/grid.py`의 `build_grid`)가 검사합니다. 메뉴에 없는 mode를 만나면 `GridError`를 던지고, 이 생성기는 `derive.py`가 매번 돌립니다.

> **코드로.** `build_grid`는 모든 core timeline의 segment를 읽어 driver table의 32칸(mode 16개 × `background_wanted` 참/거짓)에 셉니다. `mode == "ambiguous"`인 segment는 표 밖(`outside`)에 따로 적고, 메뉴에 없는 mode는 `"… is neither on the menu nor 'ambiguous'"`라는 오류로 거절합니다. 그래서 `make lint`만으로는 잘못된 mode를 못 잡고, `make dataset`(derive 단계)이나 `make check`에서 잡힙니다.

`driver table` — 정답 label(mode, `background_wanted`) 한 칸마다 scheduler 설정을 적어 둔 표입니다. recognizer가 label을 내면 daemon이 이 표를 찾아 scheduler 설정으로 바꿉니다. 칸이 32개입니다. `coverage grid` — core set의 segment들이 driver table의 32칸을 빠짐없이 채우는지 세어 둔 표입니다(`dataset/coverage-grid.json`).

## 2.5 segment의 label들

`attributes`는 문자열, 숫자, boolean만 값으로 갖는 평평한 map입니다(canonical schema가 그렇게 요구합니다). core set에서 쓰는 key는 여섯 개입니다. tree의 51개 파일에서 센 횟수와 함께 적습니다.

**`background_wanted`**(boolean) — 이 구간의 배경 작업을 사용자가 원하는가입니다. driver table의 칸을 정하는 두 축 중 하나라서 가장 중요합니다. recognition-vocabulary §1이 정한 뜻은 이렇습니다. 지속되는 배경 작업을 사용자가 원하면 `true`이고, 배경 작업이 없으면 관례상 `true`입니다. 그리고 여섯 batch mode(`compile`, `ml-train`, `render`, `transcode`, `indexing`, `backup`)에서는 batch job 자체가 판단 대상인 배경 작업입니다. tree에서 `true`가 47개, `false`가 19개입니다.

loader는 이 attribute에 특별한 규칙을 겁니다(`_check_background_wanted`). `ambiguous`가 아닌 모든 segment는 이 key를 **반드시** 가져야 하고 값이 boolean이어야 합니다. `ambiguous` segment는 이 key를 **가지면 안 됩니다**.

> **왜 이렇게 정했나.** 이 규칙은 Phase 3(2026-09-06)에서 생겼습니다. 기록(`_dev/archive/2026-09-06-phase-3-verification-and-protocol-freeze.md`)에 따르면 그때 `c1-idle`의 attributes가 `{}`였습니다. 배경 작업이 없으면 `true`라는 관례가 지켜지지 않은 것이 발견되어 `background_wanted: true`로 고쳤고, 같은 실수를 막으려고 lint를 loader에 넣었습니다. `ambiguous`에서 key가 없어야 하는 이유는 loader의 docstring에 적혀 있습니다. "`ambiguous`, whose label is the explicit marker that no legal value exists", 즉 `ambiguous`라는 label 자체가 "적법한 값이 없다"는 표시이기 때문입니다.

**`ambiguous`**(mode 값) — 정답조차 정할 수 없는 구간입니다. core set에서는 `c6-dual` 하나뿐입니다. 게임을 하면서 동시에 컴파일을 기다리는 장면으로, 두 전경 작업이 똑같이 활발합니다. 이 segment는 driver table 밖에 있고 정확도 채점에서 빠집니다(recognition-vocabulary §1, "`ambiguous` ground-truth only, excluded from accuracy").

**`pre_committed_miss`**(boolean) — 이름과 행동만으로는 어떤 recognizer도 이 label에 닿을 수 없다고 **미리** 선언한 구간입니다. 이런 구간은 정확도에서 빼고 따로 보고합니다(recognition-vocabulary §1). tree에서 여덟 segment가 이 표시를 가집니다. `c1-indexing`(사용자가 직접 초기화한 뒤의 첫 색인, 원하지 않은 색인과 의도만 다름), `c6-alias`(재생기 두 개가 색인기의 실제 이름을 달고 있음), `c6-fold`의 30 s부터의 `meeting` segment(브라우저 안에서 시작한 통화가 `chrome`을 하나 더할 뿐 통화라는 단서가 없음), `c6-spoof`의 20 s부터의 `browsing` segment(아무도 시키지 않은 CPU 작업이 `chrome`이라는 이름으로 옴), `c7-ml-train`, `c7-render`, `c7-transcode`, `c7-backup`(같은 job, 같은 이름인데 원하지 않은 쪽으로 label만 뒤집은 짝)입니다. `c6-fold`와 `c6-spoof`의 두 segment는 9.23 D1, D2(2026-10-14)가 더했습니다.

`pre-committed miss` — 설계상 맞힐 수 없는 구간을 실험 전에 미리 표시해 둔 것입니다. 맞히지 못해도 실패로 세지 않고, 한계가 어디인지 측정해 보여 주려고 일부러 넣었습니다.

나머지 attribute들은 채점 분류와 실패 분석에만 쓰이는 설명용 key입니다. recognizer의 출력 형식에도, validator의 메뉴에도 없습니다(recognition-vocabulary §1).

- **`background`** — 배경 작업이 무엇인지. `package-upgrade` 11개(C7, 즉 attribute counterpart 묶음의 대화형 파일 10개와 `c2-p2b`), `download` 2개(`c2-p2a`, `c2-p2a-idle`).
- **`initiated`** — 누가 시작했는지. `user` 7개, `scheduled` 7개, `session` 2개(`c2-p1b`, `c7-indexing`, 로그인 직후의 첫 색인). recognition-vocabulary §1은 2026-10-16부터 `session`까지 세 값을 나열합니다(그 문서 §5의 2026-10-16 기록).
- **`dual_active`** — 두 전경이 동시에 활발함. `c6-dual` 1개.
- **`spoof`** — 다른 프로그램의 이름을 단 task가 있음. `c6-spoof`의 20 s부터의 segment(이름이 `chrome`인 batch job)와 `c6-alias`, 2개.

**`familiarity`** — segment의 field입니다(attribute가 아닙니다). 이름이 얼마나 알아보기 쉬운지의 등급(tier)입니다. 1은 투명한 이름(`firefox`), 2는 반쯤 불투명(`soffice.bin`), 3은 프로그램 자신의 뜻 없는 실제 이름(`cc1`, `tracker-miner-f`), 4는 존재하지 않지만 단어 뜻으로 추론 가능한 이름(`video-playback-`), 5는 존재하지도 않고 추론도 안 되는 이름(`qzvd`)입니다. core set에서는 `c5-t4`(4)와 `c5-t5`(5) 두 파일만 이 field를 적습니다. 적지 않은 segment의 tier는 coverage grid 생성기가 이름 표(`NAME_TIERS`, `wlc/grid.py`)로 추정하지만, 그 추정값은 canonical 파일에 들어가지 않습니다.

> **왜 이렇게 정했나.** `familiarity`를 canonical `ground_truth`로 옮기는 결정은 Phase 5(2026-09-08)의 것입니다(`_dev/archive/2026-09-07-phase-5-primitive-metrics.md`). 기록된 이유는 "the compiler dropped the annotation, so compiled `ground_truth` had no split key"입니다. compiler가 이 값을 버려서 채점자가 정확도를 tier별로 나눌 열쇠가 없었다는 것입니다. compiler 쪽 규칙은 `_ground_truth_segment`의 docstring에 있습니다. "`familiarity` is carried only when the timeline authored it — never null, never derived — so the grader's split key is exactly what the author declared." 적었을 때만 옮기고, null로도 채우지 않고, 추정해서 채우지도 않습니다.

## 2.6 segments가 정하는 파일의 길이

timeline에는 "파일 길이" field가 따로 없습니다. loader의 `duration_us` property가 계산합니다. **모든 segment의 끝과 모든 박힌 `depart` 중 가장 늦은 시각**이 파일의 길이입니다.

이 값은 두 군데에서 쓰입니다. 첫째, `depart`가 없는 task(끝이 정해지지 않은 batch job)의 수명을 계산할 때 "파일 끝까지"로 봅니다. 둘째, compile report의 `duration_us`와 utilization의 분모가 됩니다(12장).

예를 들어 `c2-p1a`는 segment가 0–60 s와 60–99.435 s이고, `editor`의 `depart`가 99.435 s입니다. 그래서 길이는 99,435,000 µs입니다. batch job `hog`는 60 s에 도착하는데 `depart`가 없으므로, 그 수명은 compile 시점에는 "60 s부터 파일 끝 99.435 s까지"로 계산됩니다. 그런데 이 job의 CPU 총량은 1,389.885 s입니다. 39.435 s 안에 다 끝날 수 없습니다. 즉 이 job은 파일이 끝난 뒤에도 계속 돌았을 것입니다. 이 사실이 demand 숫자에 어떤 이상한 값을 만드는지는 12.4절에서 봅니다.

---

# 3장 · Timeline의 등장인물: tasks

이 장은 `tasks` 목록을 다룹니다. task 한 줄은 "어떤 이름의 process가, 어떤 행동 모형으로, 언제 나타나 언제 사라지는가"를 적습니다. 행동의 숫자는 archetype library에 있고, timeline은 그 숫자를 **바꾸지 못합니다**. timeline이 할 수 있는 일은 archetype이 허락한 몇 개의 손잡이(`bind`)를 돌리고, 그 손잡이 값의 출처(`source`)를 적는 것뿐입니다. 이 경계가 왜 중요한지가 이 장의 중심입니다.

## 3.1 task 한 줄의 구조

`c1-office`의 task 한 줄을 보겠습니다.

```yaml
  - {id: renderers, name: chrome, archetype: renderer-hidden,
     arrive: 0s, depart: 60s, count: 4,
     source: {count: [glam, "meas-ci:desktop:2026-10-04"]}}
```

field는 여덟 개입니다(`_load_tasks`).

| field | 필수? | 뜻 |
|---|---|---|
| `id` | 필수 | 파일 안에서 유일한 task 식별자. 저자가 정합니다. compile된 task id가 여기서 결정적으로 만들어지고, 무작위 추출의 열쇠가 됩니다(10장). |
| `name` | 필수 | recognizer가 보는 process 이름. |
| `archetype` | 필수 | 행동 모형의 이름. library에 있어야 하고, lifetime이 `spawned`이면 안 됩니다. |
| `arrive` | 필수 | 나타나는 시각. |
| `depart` | 조건부 | 사용자가 닫는 시각. archetype의 lifetime이 `segment-bound`일 때 **반드시** 있고, 아닐 때 **반드시** 없습니다. |
| `bind` | 조건부 | archetype이 `binding_params`로 선언한 손잡이의 값. 선언된 key 전부, 그리고 그것만. |
| `count` | 선택 | 같은 task를 몇 개 띄울지. 기본 1. |
| `source` | 조건부 | `bind`와 `count`의 값마다 출처. lint가 검사합니다(14장). |

`id`와 `name`이 따로 있는 이유가 중요합니다. `name`은 recognizer가 보는 겉모습이고, `id`는 실험 장치가 task를 구별하는 속 이름입니다. 겉모습은 일부러 겹치게 만들 수 있습니다. `c1-office`에는 `chrome`이라는 이름의 task가 다섯 개(browser 하나와 renderer 넷) 있고, `c6-spoof`에는 브라우저가 아닌 batch job이 `chrome`이라는 이름을 달고 끼어듭니다. 그래도 `id`는 절대 겹치지 않습니다. canonical schema는 이것을 이렇게 적습니다. "names are the recognizer-facing process names and may collide by design (C6 name-collision files); ids never do (uniqueness is a linter invariant)."

`C6` — core set의 여섯 번째 묶음, resolution-limit 파일들입니다. 이름만 보는 인식이 설계상 실패하는 지점(이름 충돌, 한 process 안의 변화, 두 전경의 동시 활동)을 일부러 담은 네 파일(`c6-spoof`, `c6-alias`, `c6-fold`, `c6-dual`)입니다.

loader가 task에 거는 규칙을 모으면 이렇습니다.

1. `id`, `name`, `archetype`, `arrive`가 있어야 합니다.
2. `id`가 파일 안에서 유일해야 합니다(`duplicate task id`).
3. `archetype`이 library에 있어야 합니다(`unknown archetype`).
4. `bind`의 key 집합이 archetype의 `binding_params`와 정확히 같아야 합니다. 선언되지 않은 key가 있으면 "inline-numerics violation", 선언된 key가 빠지면 "missing bind keys"입니다.
5. archetype의 lifetime이 `spawned`이면 거절합니다("it lives in spawn tables, not the tasks track").
6. `depart`는 lifetime이 `segment-bound`일 때만, 그리고 그때는 반드시 있어야 합니다.
7. `count`는 양의 정수여야 합니다.
8. `depart`가 있다면 `arrive`보다 뒤여야 합니다.

`source`는 loader가 읽어서 들고만 있고 검사하지 않습니다. 검사는 lint의 몫입니다(14.3절). 그래서 `source`가 틀린 timeline도 compile은 됩니다. `make lint`가 막아 줄 뿐입니다.

## 3.2 lifetime: 누가 언제 끝나는가

`depart` 규칙을 이해하려면 archetype의 **lifetime class**를 알아야 합니다. interpretation contract §5가 세 가지를 정합니다.

| lifetime class | `depart` | 어떻게 끝나나 | library의 해당 archetype(tree, 29개 중) |
|---|---|---|---|
| `segment-bound` | arrive event에 박힘 | 외생: 사용자가 닫음 | 17개: `office-writer`, `code-editor`, `mail-client`, `web-browser`, `image-editor`, `video-editor`, `video-player`, `audio-player`, `video-call`, `renderer-hidden`, `chat-client`, `game-client`, `game-task-chain`, `compositor-shell`, `audio-server`, `service-manager`, `message-bus` |
| `finite` | 없음 | program이 `EXIT`에 닿을 때. 시각은 scheduling의 결과 | 10개: `cpu-batch`, `build-orchestrator`, `module-build-orchestrator`, `file-archiver`, `game-download`, `game-download-idle`, `package-upgrade`, `file-indexer`, `video-transcoder`, `incremental-backup` |
| `spawned` | 없음 | `FORK`로 run time에 태어나 `EXIT`로 끝남 | 2개: `compiler-child`, `module-compiler-child` |

`lifetime class` — task가 어떻게 끝나는지에 따른 분류입니다. `segment-bound`는 사용자가 닫는 앱, `finite`는 할 일을 다 하면 스스로 끝나는 job, `spawned`는 다른 task가 낳는 자식입니다.

이 표가 1.2절의 원칙과 그대로 맞물립니다. 편집기를 닫는 시각은 사용자의 행동이므로 박습니다. 컴파일이 끝나는 시각은 scheduler가 CPU를 얼마나 주느냐에 달렸으므로 박지 않습니다. 자식 process는 timeline의 `tasks`에 직접 쓸 수 없고, 부모의 spawn table 안에만 삽니다(11.7절).

> **코드로.** `_load_tasks`는 `library.lifetime(archetype)`으로 lifetime을 읽고, `(lifetime == "segment-bound") != has_depart`이면 오류를 냅니다. 메시지는 "depart missing but archetype lifetime is 'segment-bound' (depart iff segment-bound)" 같은 모양입니다. "iff"(if and only if)라는 말이 규칙을 그대로 요약합니다.

## 3.3 `bind`와 `binding_params`: 숫자는 archetype에만

timeline은 행동의 숫자를 쓸 수 없습니다. 그런데 어떤 값은 archetype이 정할 수 없고 장면이 정해야 합니다. 예를 들어 "이 batch job이 CPU를 총 몇 초 쓰는가"는 job의 종류(archetype)가 아니라 이 장면에서 어떤 job을 돌리는가에 달렸습니다. 이런 값을 위해 archetype은 `binding_params`라는 목록으로 "이 손잡이들은 timeline이 정하라"고 선언합니다. timeline은 `bind`로 그 손잡이에, 그리고 그 손잡이에만 값을 넣습니다.

tree의 library에서 `binding_params`가 비어 있지 않은 archetype은 이렇습니다.

| archetype | `binding_params` | core set에서 묶인 값의 예 |
|---|---|---|
| `cpu-batch` | `total_work`, `program` | `c2-p1a`: `{total_work: 1389.885s, program: python3}` |
| `build-orchestrator` | `spawn_count`, `parallelism_cap`, `child_name` | `c1-compile`: `{spawn_count: 2908, parallelism_cap: 8, child_name: cc1}` |
| `module-build-orchestrator` | `parallelism_cap`, `child_name` | `c7-compile`: `{parallelism_cap: 8, child_name: cc1}` |
| `file-archiver`, `game-download`, `game-download-idle`, `package-upgrade`, `file-indexer`, `video-transcoder`, `incremental-backup` | `total_work` | `c7-dev`의 `upgrade`: `{total_work: 26.385s}` |
| `game-task-chain` | `lane_share`, `member_names` | `c1-gaming`: `{lane_share: 0.9, member_names: [15개 이름]}` |

나머지 18개 archetype은 `binding_params`가 비어 있어서 `bind`를 쓸 수 없습니다.

각 손잡이의 뜻은 이렇습니다.

- `total_work` — batch job이 쓸 CPU 시간의 총량입니다. 예를 들어 `26.385s`는 Ubuntu의 무인 업그레이드가 측정에서 쓴 CPU 총량입니다.
- `program` — `cpu-batch`처럼 여러 프로그램의 측정표를 한 archetype에 담은 경우, 그중 어느 표를 쓸지 고릅니다. `python3`(PyTorch MNIST 학습), `kdenlive_render`(Kdenlive 내보내기), `spoof`(`c6-spoof`의 가짜 `chrome`)가 있습니다. 표는 task의 이름이 아니라 이 값으로 고릅니다.
- `spawn_count` — 빌드가 돌릴 object job의 수입니다. 2,908은 측정한 Linux kernel defconfig 빌드의 object job 수입니다.
- `parallelism_cap` — 동시에 돌 수 있는 job의 수, 즉 `make -j8`의 8입니다.
- `child_name` — 빌드가 낳는 컴파일러 자식의 이름입니다(`cc1`).
- `lane_share` — 게임의 frame chain이 CPU 하나 중 얼마를 쓰도록 맞출지입니다(11.9절).
- `member_names` — 게임 chain의 구성원 task들의 이름 15개입니다(11.9절).

`object job` — `make`가 소스 파일 하나를 object 파일 하나로 컴파일하는 작업 단위입니다. 이 dataset에서는 process 여섯 개(`sh`, `gcc`, `cc1`, `as`, `fixdep`, `rm`)의 묶음으로 모형화됩니다. `make -j8` — `make`에게 job을 최대 8개까지 동시에 돌리라는 옵션입니다. `make`의 jobserver가 이 수를 셉니다.

> **왜 이렇게 정했나.** "행동의 숫자는 archetype에만"이라는 규칙은 세 층 구조의 핵심입니다. `docs/workload/building-plan.md` §1은 층을 archetype library → scenario catalog → timeline으로 나누고(층은 번호가 아니라 이름으로 부릅니다. 이 프로젝트의 문서에서 "Layer 1", "Layer 2"는 평가의 두 층만 가리킵니다, 8.2절), "behaviour parameters live in the archetype library", 즉 행동의 숫자는 맨 아래 층에만 둔다고 정합니다. task 2.3의 결정 2(2026-08-27)가 이것을 포맷 규칙으로 만들었습니다. "`bind:` restricted to keys the archetype declares in `binding_params` (any other numeric is the inline-numerics lint violation)." 이 규칙이 있어야 모든 숫자가 측정이나 문헌으로 거슬러 올라가는 출처를 가집니다. timeline 저자가 "이 편집기는 좀 더 무겁게"라고 숫자를 슬쩍 바꿀 길이 없습니다.

`bind`의 값을 어떻게 정하는지에도 규칙이 있습니다. 9.10 D17은 "each batch job runs whole, at the input its decision fixed; files lengthen to hold it"이라고 정했습니다(2026-10-01, `_dev/research/jioh/task-9.10-scenarios-timelines/changelog.md`). batch job은 측정한 전체 크기로 묶고, 파일 길이를 job에 맞춰 늘린다는 뜻입니다. "No `total_work` or `spawn_count` describes part of a job." 기록된 이유는 "how large a user's job is has no source", 즉 사용자의 job이 얼마나 큰지에 대한 출처가 없으므로, 측정한 job을 통째로 쓰는 것 말고는 근거 있는 값이 없다는 것입니다. 그래서 `c1-compile`은 1,594 s, `c1-transcode`는 4,762 s, `c6-dual`은 12,072 s(3시간 21분)나 됩니다.

`9.10` — Phase 9(workload dataset 재건)의 sub-task 9.10, "Scenarios and timelines" 연구 slice입니다. timeline의 내용(어떤 task를 어떤 값으로 묶는가)을 2026-10-01부터 결정했습니다. `D17` 같은 번호는 그 slice의 changelog에 적힌 결정 번호입니다.

## 3.4 `count`: 같은 이름의 여러 instance

`count: 4`는 같은 task를 네 개 띄웁니다. compiler는 instance id를 `<id>.1`, `<id>.2`, …, `<id>.N`으로 만듭니다(`count`가 1이면 `<id>` 그대로). 네 instance는 같은 이름을 달지만, 무작위 추출의 열쇠에 instance id가 들어가므로 각자 다른 program을 가집니다(10장). `c1-office`를 compile하면 `renderers.1`부터 `renderers.4`까지 네 개의 arrive event가 생기고, 각각의 program 길이는 25, 23, 29, 19 명령어로 서로 다릅니다(tree에서 확인).

core set에서 `count`를 쓰는 곳은 브라우저의 숨은 탭 renderer 하나뿐입니다. `c1-browsing`, `c1-office`, `c3-workday`, `c3-evening`과 그 파생 파일들, 그리고 `c4-compile`에 끼어드는 `injected-renderers`가 모두 `count: 4`입니다.

> **왜 이렇게 정했나.** 4라는 숫자는 `c1-office` 머리 주석이 근거를 적습니다. 탭이 다섯 개라는 것은 Firefox의 Linux telemetry(`glam`, 9.10 D15, D16)에서 client마다 모든 창을 통틀어 연 탭 수의 최댓값, 그 중앙값 4.67을 다섯으로 올린 것이고(창 수 최댓값의 중앙값이 1이라 창 하나에 둠), 탭 하나에 renderer 하나라는 것은 CI runner에서 관찰한 Chrome(`meas-ci:desktop:2026-10-04`, 9.10 D126–D129, D131)에서 왔습니다. 그래서 앞에 보이는 탭을 뺀 나머지 네 탭의 page renderer가 네 개의 `renderer-hidden` task입니다. 이 넷은 실제 사이트를 보는 경우의 바닥값입니다. 실제 page의 cross-site iframe(광고, embed, 로그인 widget)은 site isolation 아래에서 renderer를 따로 띄우는데 이 count는 그것을 넣지 않고, 얼마나 더 되는지는 읽은 출처가 말하지 않습니다(9.10 D126, D131). 9.10 D32는 `count`도 묶인 값(bound value)으로 보아 출처를 요구합니다. 그래서 이 task는 `source: {count: [glam, "meas-ci:desktop:2026-10-04"]}`를 가집니다.

`count`가 1보다 큰 task에는 두 가지 제약이 따라옵니다. 첫째, focus를 받을 수 없습니다(4.4절). 실제 화면에서 focus를 받는 창은 하나인데, 네 instance 중 어느 것인지 timeline이 특정할 방법이 없기 때문입니다. 둘째, 중간에 시작하는 task가 launch phase를 재생할 때, 같은 묶음의 instance들은 측정 repeat 하나를 공유하고 그 안의 서로 다른 stream을 나눠 씁니다(11.3절).

## 3.5 `source` map: 묶인 값마다 출처를

`source`는 `bind`와 `count`의 값마다 출처를 적는 map입니다. key 집합은 "`bind`의 key 전부, 그리고 `count`를 적었다면 `count`"와 정확히 같아야 합니다. 값은 세 모양 중 하나입니다.

1. **registry tag 하나** — 예: `"meas-ci:background:2026-10-03"`. 출처 registry(`dataset/sources.yaml`)의 id, 그리고 필요하면 콜론 뒤에 그 출처 안의 위치(locator).
2. **registry tag의 목록** — 예: `[glam, "meas-ci:desktop:2026-10-04"]`. 여러 출처가 함께 값을 받칠 때.
3. **label 하나** — `design`, `convention`, `arithmetic` 중 하나. 이 셋은 출처가 아니라 값의 성격을 밝히는 말입니다. label은 단독으로만 쓸 수 있고 목록에 넣을 수 없습니다.

`registry tag` — `dataset/sources.yaml`에 등록된 출처 id에 위치 정보를 붙인 문자열입니다. 예를 들어 `lavd-ossna24:s16`은 LAVD 발표 자료의 16번째 slide입니다. `meas-ci` — 이 연구가 GitHub Actions runner에서 직접 측정한 결과라는 출처 id입니다. locator는 `<workflow>:<campaign 날짜>` 모양이라서 `meas-ci:background:2026-10-03`은 2026-10-03에 시작한 background 측정 campaign을 가리킵니다. `design` — 실험을 위해 저자가 정한 값이라는 label입니다. `convention` — 관례를 따른 값입니다. `arithmetic` — 다른 값에서 계산한 값입니다.

`c2-p1a`의 batch job을 보겠습니다.

```yaml
  - {id: hog, name: python, archetype: cpu-batch, arrive: 60s,
     bind: {total_work: 1389.885s, program: python3},
     source: {total_work: "meas-ci:background:2026-10-03", program: [pytorch-examples, "meas-ci:background:2026-10-03"]}}
```

`total_work`의 1,389.885 s는 2026-10-03 background campaign에서 측정한 MNIST 학습의 CPU 총량이고, `program`의 `python3`는 PyTorch의 기본 예제(`pytorch-examples`)를 그 campaign에서 돌린 것이라는 뜻입니다.

`c1-gaming`의 chain은 label을 씁니다.

```yaml
     source: {lane_share: design, member_names: "lavd-ossna24:s16"}
```

`lane_share` 0.9는 측정값이 아니라 실험을 위해 정한 값이고, 구성원 이름들은 LAVD 발표 자료 16번 slide의 process tree에서 왔다는 뜻입니다.

tree의 51개 timeline을 세면, 131개 task 중 53개가 `source`를 가집니다. key별로는 `total_work` 30, `count` 10, `lane_share` 8, `member_names` 8, `program` 7, `parallelism_cap` 5, `child_name` 5, `spawn_count` 4입니다. 값에 나오는 출처는 `meas-ci` 53회, label `design` 11회, `glam` 10회, `lavd-ossna24` 8회, label `convention` 5회(모두 `parallelism_cap`), `pytorch-examples` 3회, `kdenlive` 3회입니다. `arithmetic` label은 core timeline에서 한 번도 쓰이지 않습니다(2026-10-17의 tree에서 센 값입니다).

> **왜 이렇게 정했나.** 이 field의 근거는 9.10 D32입니다(2026-10-01). 결정은 "each bound value (`count`, `spawn_count`, `parallelism_cap`, `total_work`, `lane_share`, `member_names`, the bound program) carries `source: <id>:<locator>` or a label (design, convention, arithmetic), linted against `dataset/sources.yaml`"입니다. 기록된 이유는 세 가지입니다. building-plan §6의 출처 주장(모든 숫자가 출처를 가진다)이 library에만 적용되고 있었습니다. timeline 값에는 출처를 적을 자리 자체가 없었습니다(`timeline.py`, 2026-09-13 critical-findings memo의 B7). 그리고 archetype-plan은 count를 "binding-time parameters with a source tag"라고 부르면서도 그 tag를 둘 곳이 없었습니다. 9.10은 내용을 정하고 field와 lint는 9.13에 넘겼는데, 9.13은 이 일을 하지 않았습니다. 2026-10-10 dataset audit가 이것을 A2로 찾아냈고("Timeline bound values carry no source field … `timeline.py` has no source slot"), 9.18의 결정 4(2026-10-11)가 마침내 field와 lint를 만들었습니다(`_dev/docs/spec/jioh/task-9.18-compiler-schema-and-build-gate.md`).

`audit` — 2026-10-10에 다섯 명의 검토자가 dataset 전체를 점검한 기록입니다(`_dev/docs/audit/jioh/2026-10-10-dataset-audit-before-9.15.md`). 거기서 찾은 문제 중 A1–A4는 "class-A process findings"로, A1은 파생 파일의 키 입력이 base와 달랐던 문제, A2는 묶인 값에 출처 field가 없던 문제, A4는 build gate의 구멍입니다.

`design` label 뒤의 이유(왜 0.9인가)는 어디에 있을까요. 9.18의 결정 4가 정했습니다. "The reason behind a design label stays in `bound-values.md` and the timeline's comment." 즉 이유는 `_dev/research/jioh/task-9.10-scenarios-timelines/bound-values.md`와 timeline 파일의 주석에 남기고, `source` map에는 label만 씁니다. 예를 들어 `lane_share`의 네 값(0.9, 0.95, 1.45, 0.6)이 모두 design이라는 것과 각각의 전제는 9.10 D31에 기록되어 있습니다.

`source`도 `slice_of`(4.3절)처럼 compile 시점에만 쓰이는 정보입니다. canonical workload로 가지 않습니다(`docs/data-contracts.md` §3, "Neither field reaches the canonical workload"). 하지만 timeline 파일의 바이트는 바뀌므로, `meta.derived_from`의 blob hash가 바뀌고, 그래서 모든 artifact의 hash가 바뀝니다. 9.18이 이 field를 넣었을 때 전체 set을 다시 bless한 이유가 이것입니다(9.18 D2, "Every artifact's bytes change through `meta.derived_from`").

`bless` — 새로 compile한 artifact들의 hash를 manifest에 기록하고 commit해서, 이것이 공식 build라고 확정하는 일입니다. 그렇게 확정된 build를 `blessed build`라고 부릅니다.

## 3.6 이름의 규칙

task의 `name`에는 형식 lint가 없습니다. 비어 있지 않은 문자열이기만 하면 됩니다(canonical schema의 `minLength: 1`). 하지만 이름을 정하는 규칙은 기록되어 있습니다.

**이름은 커널의 `comm`입니다.** 9.10 D25(2026-10-01)는 "the name a task shows is the kernel's `comm` for its process — the exec'd file's basename cut to 15 bytes, a script keeping its own name, a process that renames itself with `prctl` taking its new name"이라고 정합니다. 실행 파일 이름에서 경로를 뺀 뒤 15 byte에서 자릅니다. 그래서 GNOME의 색인기 `tracker-miner-fs-3`는 `tracker-miner-f`로, 무인 업그레이드 `unattended-upgrade`는 `unattended-upgr`로 잘려 보이고, Thunderbird는 실제로 실행되는 파일의 이름인 `thunderbird-bin`으로 보입니다. 기록된 이유는 "it is what `/proc/<pid>/comm`, `ps`, `top` show", 즉 실제 기계에서 recognizer가 만날 이름이 이것이기 때문입니다. tree의 core timeline에 나오는 이름 35개(chain 구성원 이름과 `child_name` 포함)를 세어 보면 가장 긴 것이 정확히 15자입니다(`winepulse_timer`, `FAudio_AudioCli`, `Task worker thr`, `unattended-upgr`, `thunderbird-bin`, `video-playback-`).

> **코드로.** 15자 제한은 두 곳에서 lint됩니다. generated layer의 정의(`dataset/grids.yaml`의 `comm_limit: {chars: 15, source: linux-sched-h}`)가 정하는 이름은 `dataset/tools/gen/cells.py`의 `lint_grids`가 보고, compile된 모든 파일의 모든 이름(top-level task와 spawn table의 자식 모두)은 compile 안의 canonical lint가 봅니다(`wlc/linter.py`의 `COMM_LIMIT = 15`, 커널의 `TASK_COMM_LEN` 16에서 끝 문자를 뺀 값; 9.23 D14, 2026-10-15). 그 전에는 core timeline의 이름 길이를 검사하는 lint가 없었습니다(13.2절).

**이름만, 경로는 없습니다.** scenario catalog는 "names only, no paths"를 schema 결정으로 적습니다(`docs/workload/scenario-catalog.md`). 그래서 `c6-spoof`의 가짜 `chrome`은 진짜 `chrome`과 경로로 구별될 수 없고, 이름 충돌만으로 속입니다. 경로를 이용한 속임은 schema 밖입니다(`c6.variant.yaml` 주석, "path-mismatch spoofing is out of schema").

**이름을 바꾸는 두 가지 방법.** 파생 파일에서 이름을 바꾸려면 recipe의 `rename` op(같은 이름을 가진 모든 task의 이름을 바꿈)나 `patch-task` op(특정 `id`의 task 하나만 바꿈)를 씁니다. 지금 tree의 다섯 recipe는 `rename`을 한 번도 쓰지 않고, 이름 바꾸기를 모두 `patch-task`로 합니다(5.3절).

## 3.7 `declared_class`는 timeline에 없다

canonical 파일의 모든 task 기록에는 `declared_class`가 붙습니다(7.5절). 그런데 timeline에는 이 field를 쓸 자리가 없습니다. task의 scheduling class는 **바인딩한 archetype의 것**이고, timeline이 정할 수 없습니다.

compiler가 이 값을 옮기는 길은 세 가지입니다(`_TaskBuild`의 생성자와 각 전개 함수).

- 일반 task — archetype entry의 `declared_class`를 그대로 씁니다. `_compile_instance`가 `_TaskBuild(iid, task["name"], entry["declared_class"])`로 만듭니다.
- 빌드의 자식 — spawn table의 각 칸은 **자식 entry**의 class를 씁니다. `build-orchestrator`의 자식은 `compiler-child`의 class, `module-build-orchestrator`의 자식은 `module-compiler-child`의 class입니다.
- 게임 chain의 구성원 — 모두 `game-task-chain` entry의 class를 씁니다.

tree의 library에서 `idle`인 entry는 세 개입니다. `file-indexer`(GNOME Tracker), `incremental-backup`(Déjà Dup), `game-download-idle`(SteamCMD 다운로드의 idle 변형)입니다. 나머지 26개는 `normal`입니다.

> **왜 이렇게 정했나.** 이 field의 근거는 2026-10-08 memo(`docs/memos/2026-10-08-declared-scheduling-class.md`)와 9.13의 결정 2입니다. memo는 field가 "the scheduling policy a program sets for itself"를 나른다고 정의하고, 값의 근거를 적습니다. Tracker는 모든 thread에 SCHED_IDLE을 걸고, Déjà Dup은 backup을 `chrt --idle 0` 아래에서 시작합니다. 그리고 결정적인 문장이 있습니다. "The class is the entry's. A task carries the class of the entry it binds, never one inferred from its name." 그 예로 memo는 두 미디어 재생기에 색인기 이름(`tracker-miner-f`, `baloo_file`)을 단 파일을 들고, 그래도 class는 `normal`로 남는다고 적습니다(memo가 쓰인 2026-10-08에는 그 파일이 `c5-t3`였고, 2026-10-12에 `c6-alias`로 옮겨졌습니다). 이름을 보고 class를 정하면 이름 충돌 실험이 class로 새어 버립니다. 그래서 class는 행동 모형에 붙고, 이름과 독립입니다. nice 값은 싣지 않습니다. memo의 이유는 "Nice is a weight within the normal class, not a class, and of the four algorithms only LOTTERY has a weight to carry it."

`SCHED_IDLE` — Linux의 scheduling 정책 중 하나로, 다른 정책의 task가 실행 가능하지 않을 때만 CPU를 받습니다. 이 dataset의 `idle` class가 이것입니다. `nice` — normal 정책 안에서 task들 사이의 몫을 조정하는 가중치(−20부터 19)입니다. class를 바꾸지 않습니다. `LOTTERY` — 이 연구의 scheduler가 고를 수 있는 네 알고리즘(MLFQ, EDF, LOTTERY, FIFO) 중 하나로, 추첨권 수에 비례해 CPU를 줍니다.

simulator 쪽 규칙도 memo §2에 있습니다. `idle` task는 다른 class의 task가 하나도 실행 가능하지 않을 때만 돌고, 다른 class의 task가 깨어나면 즉시 밀려납니다. 이 규칙은 네 알고리즘 모두에서 알고리즘의 결정 **아래에** 적용됩니다. 기아(starvation)를 막는 안전망은 simulator가 만들지 않고, harness의 `starvation_floor` guard가 모든 task의 대기를 30 s로 제한합니다.

---

# 4장 · 사용자를 그리는 세 track: input, focus, operations

`segments`가 "사용자가 무엇을 하는가"의 정답이라면, 이 장의 세 track은 "사용자가 손과 눈으로 무엇을 하는가"입니다. `input`은 손이 어디에 타자를 치는지, `focus`는 눈앞에 어느 창이 있는지, `operations`는 사용자가 앱 안에서 무거운 동작(페이지 로드, 메일 전송, 필터 적용)을 언제 시작하는지를 적습니다. 이 셋은 compile 후 운명이 다릅니다. `focus`는 canonical 파일에 그대로 남아 recognizer에게 보이고, `input`과 `operations`는 compile 때 wake와 program으로 녹아 사라집니다.

## 4.1 왜 사용자 track이 둘로 나뉘었나

처음부터 둘이었던 것은 아닙니다. Phase 2(2026-08-27)의 timeline 포맷에는 사용자 track이 하나 있었고, 그 이름이 `focus`였습니다. task 2.3의 결정 3은 그것을 이렇게 정의했습니다. "`focus:` is a single timeline-wide list of `{from, to, task}` windows; overlap is impossible by construction, gaps mean no one receives input. The compiler samples input wake events from the focused task's archetype gap distribution inside each window." 즉 그때의 `focus`는 "어디에 타자를 치는가"였습니다.

2026-10-11, 9.17이 이것을 둘로 나눴습니다(`_dev/docs/spec/jioh/task-9.17-focus-in-the-telemetry.md`). 옛 `focus`는 `input`으로 이름을 바꾸고 규칙은 그대로 두었습니다. 그리고 "어느 창이 앞에 있는가"를 적는 새 track에 `focus`라는 이름을 주었습니다.

> **왜 이렇게 정했나.** 9.17의 결정 1은 두 track이 서로 다른 것이라고 적습니다. "that track is a compile-time stimulus placement, and the window focus is the real-desktop signal the experiment measures." 키 입력 창은 compile 때 stimulus를 놓을 자리를 정하는 장치이고, 창 focus는 실제 desktop에서 recognizer가 볼 수 있는 신호라는 뜻입니다. 사람이 타자를 멈춰도 창은 그대로 앞에 있습니다. 둘을 한 track에 두면 "타자를 안 치는 동안 focus가 없다"는 거짓 장면이 생깁니다. 결정 7은 이름을 이렇게 나눈 이유를 적습니다. "The window-focus track takes the name `focus`, so that the word has one meaning across the timeline, the workload, the projection and the telemetry." timeline, canonical 파일, recognizer가 보는 projection, telemetry 어디서나 `focus`가 같은 뜻이 되도록 한 것입니다.

결과적으로 지금의 timeline에서 `input`은 compile을 위한 장치이고 `focus`는 실험의 관측 대상입니다. 이 차이를 기억하면 두 track의 규칙이 왜 다른지 이해됩니다.

## 4.2 `input`: 키 입력이 떨어지는 창

`input`은 `{from, to, task, slice_of?}`의 목록입니다. 선택이고 빈 목록(`input: []`)이어도 됩니다. 게임(`c1-gaming`), 미디어(`c1-media`), 회의(`c1-meeting`), idle(`c1-idle`) 파일은 `input: []`입니다. 이 장면들에는 타자를 치는 사람이 없습니다.

```yaml
input:
  - {from: 2s, to: 58s, task: writer}
```

이 한 줄의 뜻은 "2 s부터 58 s까지 사용자가 `writer` task(LibreOffice Writer)에 타자를 친다"입니다. compile하면 이 56 s 동안 실제 사람의 타자 기록에서 잘라 온 키 입력들이 `input:writer` channel의 wake event로 펼쳐집니다. `c1-office`에서는 270개입니다(tree에서 확인).

loader의 규칙(`_load_input`)은 다섯 가지입니다.

1. `from`, `to`, `task`가 있고 `from < to`여야 합니다.
2. `task`가 존재해야 합니다.
3. 그 task의 archetype이 **input channel**을 가져야 합니다. `Library.has_input_channel`이 archetype의 program(`pattern.program`)에 `WAIT: input`이 있는지, `loop` 안까지 내려가 찾습니다.
4. 창이 task의 수명 안에 있어야 합니다. `from ≥ arrive`이고, `depart`가 있으면 `to ≤ depart`입니다.
5. 시작 시각으로 정렬한 뒤 서로 겹치면 안 됩니다. 오류 메시지가 이유를 말합니다. "(one user, one typing hand)", 사용자는 한 명이고 타자 치는 손은 하나입니다.

tree의 library에서 `WAIT: input`을 가진 archetype은 여섯입니다. `office-writer`, `code-editor`, `mail-client`, `web-browser`, `image-editor`, `video-editor`. 그중 앞의 넷은 재생할 키 입력 stream(`stimulus`)을 가집니다.

| archetype | stimulus stream | 출처 tag |
|---|---|---|
| `office-writer` | `swell-word-c1` | `swell-icmi14:word-c1` |
| `code-editor` | `swell-word-c1` | `swell-icmi14:word-c1` |
| `mail-client` | `swell-outlook-c23` | `swell-icmi14:outlook-c23` |
| `web-browser` | `swell-ie-c1` | `swell-icmi14:ie-c1` |

`stimulus` — task를 깨우는 외부 입력의 흐름입니다. 이 dataset에서는 실제 사람이 남긴 키보드 기록을 재생한 것입니다. `SWELL-KW` — 실험실에서 지식 노동 과제(Word로 보고서 쓰기, Outlook으로 메일, Internet Explorer로 browsing)를 한 학생과 인턴의 키보드·마우스 기록을 모은 공개 dataset입니다(`swell-icmi14`, 참가자 25명, 약 3시간씩). 그 기록에서 Word, Outlook, Internet Explorer를 쓰는 동안의 사건을 뽑아 `dataset/stimulus/*.jsonl`에 `{t_us, kind}` 줄로 저장했습니다. Word stream(`swell-word-c1.jsonl`)에는 사건이 82,634개 있습니다(`dataset/stimulus/streams.json`). 네 archetype은 그중 `kind`가 `key`인 사건만 재생합니다.

`image-editor`(GIMP)와 `video-editor`(Kdenlive)는 `WAIT: input`은 있지만 stimulus가 없습니다. 이 둘에게 입력 창은 "키 입력이 떨어지는 곳"이 아니라 "사용자가 앞에서 작업하는 동안의 활동 패턴(`focus_components`)으로 바뀌는 구간"입니다(11.2절). 9.14의 hand-off가 이 사실을 문서에 적으라고 남겼습니다. "keystroke streams for four applications, none for Kdenlive and GIMP."

> **왜 이렇게 정했나.** 키 입력을 분포에서 뽑지 않고 실제 기록을 재생하는 결정은 9.5 D18입니다(2026-09-15, `_dev/research/jioh/task-9.5-interactive-typing/changelog.md`). 기록된 이유는 "replay preserves the burst-and-pause structure that forms and drains an editor's queue, which independent sampling from a quantile table … cannot reproduce; the simulated stimulus is then the population the per-input runs (D13) were measured under."입니다. 사람의 타자는 몰아치다 멈추기를 반복하고, 그 리듬이 편집기의 대기열을 채웠다 비웁니다. 간격을 하나씩 독립적으로 뽑으면 그 리듬이 사라집니다. 그리고 편집기의 "키 하나당 CPU" 값을 측정할 때도 같은 SWELL-KW 기록을 재생했으므로, 재생한 입력을 쓰면 측정 조건과 실험 조건이 일치합니다.

**2 s의 여백.** core set의 거의 모든 입력 창은 segment가 시작한 뒤 2 s에 열리고 끝나기 2 s 전에 닫힙니다(`c1-office`의 2–58 s처럼). 9.10 D31(2026-10-01)은 이 여백을 design으로 기록합니다("focus windows open 2 s after/close 2 s before a segment" — 이때는 키 입력 창의 이름이 아직 `focus`였습니다). 함께 적힌 근거는 SWELL-KW에서 한 창에 머무는 시간의 중앙값이 9.1 s, 90번째 percentile이 55.6 s라서 56 s짜리 창이 그 90번째 percentile 가까이에 있다는 것입니다. 파생 파일이 길이를 줄일 때도 이 여백을 지킵니다. 9.10 D44는 "a cut counterpart keeps its base's placement in proportion: focus 2 s to C − 2 s"라고 정합니다(C는 줄인 길이).

입력 창 안에 키 입력이 실제로 몇 개 떨어질지는 재생하는 기록의 어느 부분을 잘라 오느냐에 달렸습니다. 사람의 기록이므로 한참 동안 아무 키도 누르지 않는 구간도 있습니다. 예를 들어 `c1-mail`의 키 입력 35개는 모두 45.9 s와 53.1 s 사이에 몰려 있고, 그래서 그 파일의 앞 26.385 s를 자른 `c7-mail`에는 키 입력이 하나도 없습니다(9.14의 결정 2에 덧붙인 2026-10-09 수정, `_dev/docs/spec/jioh/task-9.14-consumer-rework.md`). 이 때문에 `c7-mail`은 RQ0의 판정 파일 목록(judging set)에서 빠졌습니다.

## 4.3 `slice_of`: 파생 창이 base 창의 조각임을 적는 표시

`slice_of`는 입력 창 하나에 붙는 선택 field입니다. 모양은 `{from, to, index}`입니다.

```yaml
input:
- from: 2s
  slice_of:
    from: 2s
    index: 0
    to: 58s
  task: editor
  to: 24.385s
```

이것은 `c7-dev.timeline.yaml`의 입력 창입니다. 뜻은 "이 창(2–24.385 s)은 base 파일에서 같은 task의 0번째 입력 창(2–58 s)을 잘라 낸 조각이다"입니다. 사람이 쓰는 field가 아닙니다. deriver가 파생 파일을 만들 때 씁니다(5.6절). compiler는 이 표시를 보고, 키 입력 stream의 재생 위치를 **base 창 기준으로** 뽑습니다. 그래서 파생 파일의 키 입력이 base 파일의 키 입력과 같은 시각에 떨어집니다(11.4절에서 숫자로 확인합니다).

loader의 규칙은 세 가지입니다. `slice_of`에 `from`, `to`, `index`가 모두 있어야 하고, `index`는 0 이상의 정수여야 하며, 창이 자신이 가리키는 바깥 창 안에 있어야 합니다(`slice_of.from ≤ from`, `to ≤ slice_of.to`).

`slice_of`는 canonical 파일로 가지 않습니다. canonical schema도 바뀌지 않았습니다. 이 field는 오로지 compile 시점에 "재생 위치를 어디서 뽑을까"를 정하는 데 쓰입니다.

> **왜 이렇게 정했나.** 이 field는 2026-10-10 audit의 A1에서 시작했습니다. C7의 대화형 counterpart들(base `c1-<mode>`의 앞부분을 잘라 원하지 않는 업그레이드를 끼운 파일)은 "base의 첫 26.385 s"라고 문서에 적혀 있었는데, 실제로는 키 입력 시각이 base와 하나도 겹치지 않았습니다. audit가 센 공유 시각은 browsing 29개 중 0개, office 103개 중 0개, dev 78개 중 0개였습니다. 원인은 compiler가 재생 위치를 창의 길이로 뽑았기 때문입니다. counterpart의 창은 22.385 s, base의 창은 56 s라서 같은 seed로도 다른 위치가 나왔습니다. 9.18의 결정 1(2026-10-11)이 고친 방법은 이렇습니다. "The compiler draws the stimulus offset for the outer window — by its length and its index — and places inside the slice the keystrokes that fall in it, so a counterpart's keystrokes are byte-identical to its base's over the slice." audit의 두 선택지 중 이것(option ii)을 고른 이유는 "it realises the recorded decision and makes the pinned sentences true", 즉 이미 기록된 결정("counterpart는 base의 첫 C초")을 실제로 실현하고, 그 결정에 기대어 쓴 문장들을 참으로 만들기 때문이라고 기록되어 있습니다.

`counterpart` — C7 묶음의 파생 파일입니다. base(`c1-<mode>`)의 앞 C초(C는 job의 CPU 총량)에서 배경 작업을 원하지 않는 쪽으로 바꿔, driver table의 `false` 칸을 채웁니다. `C7` — core set의 일곱 번째 묶음, attribute counterpart 16개입니다.

## 4.4 `focus`: 어느 창이 앞에 있는가

`focus`는 `{from, to, task}`의 목록입니다. **필수**입니다. 창이 하나도 없는 장면이라도 빈 목록(`focus: []`)을 적어야 합니다. 빠뜨리면 loader가 "missing focus track (an empty list when no window holds the focus)"이라며 거절합니다. 필수로 만든 것은 "적는 것을 잊음"과 "창이 없음"을 구별하기 위해서입니다(9.17 spec의 invariant, "Every timeline states its `focus` track, empty when no window exists").

loader의 규칙(`_load_focus`)은 여섯 가지입니다.

1. 각 구간에 `from`, `to`, `task`가 있고 `from < to`여야 합니다.
2. `task`가 존재해야 합니다.
3. 그 task의 `count`가 1이어야 합니다("a counted task — the holder is one top-level task").
4. 구간이 task의 수명 안에 있어야 합니다.
5. 정렬한 뒤 서로 겹치면 안 됩니다("one user, one attention track").
6. **모든 입력 창은 같은 task의 focus 구간 하나 안에 들어 있어야 합니다**("the user types into the window in front").

규칙 3과 6이 이 track의 성격을 보여 줍니다. focus를 쥐는 것은 이름 하나로 지목할 수 있는 top-level task 하나입니다. spawn table의 자식은 박힌 시각이 없어서, 여러 instance로 펼쳐지는 task는 instance 하나를 특정할 수 없어서 focus를 쥘 수 없습니다. 그리고 사람은 앞에 있는 창에만 타자를 칩니다.

`input`에는 "그 task가 input channel을 가져야 한다"는 규칙이 있지만 `focus`에는 없습니다. 게임(`Troy.exe`)이나 영상 재생기(`mpv`)는 키 입력을 받지 않지만 창으로서 focus를 쥡니다. `c1-gaming`의 focus는 0–60 s 동안 `game`이고, `c1-media`의 focus는 `video`입니다.

**저자가 따르는 규칙.** 9.17의 결정 4가 core set의 focus를 쓰는 규칙을 정했습니다. "The focus stays on the window the user last brought to the front, does not leave when typing stops, and is none only when no window exists." 사용자가 마지막으로 앞으로 가져온 창에 focus가 머물고, 타자를 멈춰도 떠나지 않으며, 창이 하나도 없을 때만 비어 있습니다. 묶음별로는 이렇습니다.

| 파일 | focus |
|---|---|
| 한 mode만 담은 파일(C1 calibration, C2 의도 짝, C4 끼어들기, C5 이름 사다리, C7 attribute counterpart) | 그 mode의 전경 프로그램이 수명 내내. 게임은 `Troy.exe`, 미디어는 `mpv`(영상), 회의는 `chrome`(브라우저 안의 통화) |
| `c1-idle`, `c7-idle` | 없음(`focus: []`). 세션 daemon만 있고 창이 없습니다 |
| `c2-p2a` 가족 | 게임이 내내. 다운로드를 시작한 행동은 focus 이동이 아니라 segment의 `initiated` attribute로 적습니다 |
| `c3-workday` | 브라우저(0–60 s) → writer(60–1,485 s, compile 구간 내내 유지) → 메일(1,485–1,545 s) |
| `c3-creation` | GIMP(0–120 s) → Kdenlive(120–3,212 s, transcode 구간 내내 유지) |
| `c3-evening` | 브라우저 → 게임 → `mpv`, segment 경계에서 이동 |
| C4(끼어들기 묶음) 파일 | 원래 mode의 프로그램에 머묾. 끼어드는 프로그램은 뒤에서 등장 |
| `c6-spoof`, `c6-fold` | base의 규칙 |
| `c6-dual` | 편집기와 게임 사이를 688 s마다 번갈아 |

> **왜 이렇게 정했나.** `c6-dual`의 688 s는 9.17 D1(2026-10-11)에 근거가 있습니다. "the mean continuous segment in a working sphere before switching, 11 min 28 s, `gonzalez-chi04`". González와 Mark의 CHI 2004 연구가 보고한, 한 작업 영역(working sphere)에 머무는 평균 연속 시간입니다. 9.17 D1은 함께 "the regular alternation, the editor first and the typing's 2 s lead-in are design"이라고 적습니다. 규칙적으로 번갈아 바뀌는 것, 편집기가 먼저인 것, 타자가 2 s 뒤에 시작하는 것은 실험 설계로 정한 값입니다. 입력 창은 lint 규칙 6 때문에 편집기의 차례를 따라가야 해서, 이 파일의 입력 창은 12,068 s짜리 하나에서 686–688 s짜리 아홉 개로 바뀌었습니다.

**recognizer가 focus를 본다는 것.** canonical `focus`는 정답(`ground_truth`)이 아닙니다. recognizer에게 보여 주는 정보입니다. 9.17의 결정 3은 "`ground_truth` does not change: the focus is shown to the recognizer, so it is not part of the answer key"라고 적습니다. recognizer는 telemetry snapshot에서 이것을 봅니다. `docs/data-contracts.md` §5의 rule 6이 그 모양을 정합니다.

- snapshot은 지금 살아 있는 process 이름과 개수의 묶음(name → count multiset)에 더해, focus를 쥔 process의 **이름**(`focus`)을 가집니다. 창이 없으면 `null`입니다.
- focus가 바뀌면 묶음이 바뀐 것으로 보고 새 snapshot을 냅니다. 새 snapshot은 recognizer에게 다시 묻는 시점(query point)입니다.
- 같은 이름의 두 instance 사이에서 focus가 옮겨 가면 아무것도 바뀌지 않습니다. 실제 기계에서 `/proc/<pid>/comm`으로 보는 것과 같은 해상도라서, recognizer는 "그 이름의 process 중 하나가 focus를 쥐었다"까지만 압니다.

`telemetry` — daemon이 recognizer에게 보여 주는 관측 정보의 묶음입니다. 지금 살아 있는 process 이름과 개수, 그리고 focus를 쥔 process의 이름입니다. CPU 사용량이나 burst 길이는 들어가지 않습니다. `query point` — telemetry가 바뀌어서 recognizer에게 다시 묻는 시점입니다. `snapshot` — 한 query point에서 recognizer에게 보여 주는 telemetry 한 장입니다.

telemetry는 두 모양으로 보여 줄 수 있습니다(9.17의 결정 5). `focus` 모양은 위의 snapshot 그대로이고, `names` 모양은 `focus` field를 뺀 것입니다. query point는 두 모양에서 똑같습니다(결정 6, 묶음과 focus를 합친 전체 집합의 변화로 정의). 그래서 같은 파일을 두 모양으로 돌려 보면 focus 정보 하나의 가치를 잴 수 있습니다.

> **왜 이렇게 정했나.** focus를 telemetry에 넣는 결정은 2026-10-11 인지오가 audit 기록에 남긴 "Decision — focus enters the telemetry"입니다. 결정은 이렇습니다. "The recognizer's snapshot carries, beside the name → count multiset, which process holds the focus (none when no window does). … Behaviour (burst patterns, CPU use) stays out; labels stay out; PIDs stay out." 함께 기록된 결과 중 하나가 "Every condition can be run on the same files with the focus field present and absent; the difference is reported"입니다. 이 정보를 보여도 되는 근거는 `docs/data-contracts.md` §4가 적습니다. focus 구간은 "as public as the focused window", 즉 실제 기계에서 앞에 있는 창만큼 공개된 사실입니다.

이 결정이 core set의 채점에 미친 영향은 작습니다. 9.17 spec의 invariant는 "The graded query-point counts the RQ0 gate pins are unchanged on the core set: every focus move in the authored rule coincides with an arrival except `c6-dual`'s alternation, and that file is outside grading"이라고 적습니다. 대부분의 focus 이동은 어차피 새 프로그램이 도착하는 순간에 일어나서 query point가 늘지 않고, `c6-dual`의 17번 이동만 새 query point가 되는데 그 파일은 `ambiguous`라서 채점하지 않습니다. 9.17 D4가 센 결과로, mock daemon의 oracle 실행에서 query point는 51개 파일에 130개에서 147개로 늘었고, 채점되는 것은 50개 파일에 77개로 그대로였습니다.

## 4.5 `operations`: 앱 안의 무거운 동작

`operations`는 `{at, task, name}`의 목록입니다. 선택입니다. 측정된 archetype 중 일부는 평소의 잔잔한 활동과 별개로 "무거운 동작"을 측정해 두었습니다.

| archetype | operation 이름 | 뜻 |
|---|---|---|
| `web-browser` | `page-load` | 페이지 하나 불러오기 |
| `mail-client` | `send` | 메일 한 통 보내기 |
| `image-editor` | `unsharp-mask` | GIMP에서 unsharp mask 필터 적용 |
| `video-editor` | `preview-render` | Kdenlive에서 미리보기 렌더 |

```yaml
operations:
  - {at: 30s, task: browser, name: page-load}
  - {at: 1525s, task: mailer, name: send}
```

timeline이 적는 것은 **시작 시각뿐**입니다. 동작이 얼마나 걸리는지는 compile 때 측정된 길이 분포(`params.operations.<name>.duration`)에서 뽑습니다. `c3-workday`를 compile하면 page load는 465,188 µs, 메일 전송은 2,923,590 µs가 나옵니다(그 파일의 compile report `operations` 항목). 동작 구간 안에서는 동작 자체의 측정된 활동 패턴(`components`)이 평소 패턴을 대신하고, 그 구간에 떨어질 키 입력은 버립니다(11.2절).

loader의 규칙(`_load_operations`)은 셋입니다. `at`, `task`, `name`이 있어야 하고, `name`이 그 task archetype의 operation 이름 중 하나여야 하며, `at`이 task의 수명 안(`arrive ≤ at < depart`)이어야 합니다. operation이 그 task의 입력 창 안에서, 창 하나에 하나씩 시작해야 한다는 9.10 D20의 규칙(아래)은 loader가 보지 않습니다. 2026-10-17부터 loader의 docstring이 이것을 적고("the loader checks the task's lifetime alone, and tests/test_coreset.py holds the core set to the rule"), `test_every_operation_starts_inside_an_input_window_of_its_task_one_per_window`가 commit된 core set에 대해 지킵니다. 그날 core set의 operation 23개가 모두 규칙을 지켰습니다(9.15 기록 `logs/B1-data-rebuild.md`).

> **왜 이렇게 정했나.** operation을 timeline에 놓는 형식은 9.5 follow-up spec의 결정 8–9입니다(loader docstring이 "9.5 follow-ups spec, decisions 8–9"를 가리킵니다). 시각을 정하는 규칙은 9.10 D20(2026-10-01)입니다. "every focus window on a task whose entry carries an operation holds one of it, starting 28 s after the window opens", 즉 operation을 가진 앱의 입력 창마다 하나씩, 창이 열리고 28 s 뒤(2 s에 열리는 창이면 30 s)에 놓습니다. 이 값은 design입니다. 길이를 늘인 base 파일은 창의 비율을 지킵니다. 9.10 D96은 `c1-transcode`의 미리보기 렌더를 창의 한가운데에 두었습니다. 기록된 이유는 "at the literal 30 s the render would meet the encode's first 28 s (HandBrakeCLI's scan)", 30 s에 두면 인코딩 job이 처음 28 s 동안 하는 파일 스캔과 겹치기 때문입니다. 그래서 `c1-transcode`의 operation은 2,381 s, `c1-backup`의 것은 138.5 s에 있습니다. 길이를 줄인 counterpart도 같은 비율 규칙(9.10 D44)을 따라, `c7-mail`의 전송은 22.385 s 창의 38/56 지점인 17.189821 s에 있습니다.

## 4.6 세 track의 규칙 한눈에

| 규칙 | `input` | `focus` | `operations` |
|---|---|---|---|
| 필수인가 | 아니오(빈 목록 가능) | **예**(빈 목록 가능) | 아니오 |
| 대상 task의 조건 | archetype에 `WAIT: input`이 있어야 함 | `count`가 1이어야 함 | archetype에 그 이름의 operation이 있어야 함 |
| task 수명 안 | 예 | 예 | `arrive ≤ at < depart` |
| 서로 겹침 | 금지(손은 하나) | 금지(주의는 하나) | 해당 없음 |
| 다른 track과의 관계 | 같은 task의 focus 구간 안에 있어야 함 | 입력 창을 감싸야 함 | 없음(같은 task의 입력 창 안이라는 lint는 없음) |
| canonical 파일에 남나 | 아니오(wake event로 녹음) | **예**(`focus` key) | 아니오(program과 wake로 녹음, report에 기록) |

마지막 줄이 이 장의 요점입니다. recognizer가 보는 것은 `focus`뿐이고, `input`과 `operations`는 simulator가 겪는 사건으로만 존재합니다.

---

# 5장 · Variant recipe와 deriver

core set 51개 파일 중 28개는 사람이 직접 쓰지 않았습니다. 다른 파일(base)에서 몇 군데만 바꾸는 **recipe**를 쓰고, **deriver**라는 도구가 그 recipe를 실행해 파일을 만듭니다. 이 장은 왜 이런 방식을 쓰는지, recipe가 어떤 모양이고 어떤 명령(op)을 쓸 수 있는지, 그 결과물이 어떻게 생기는지를 다룹니다.

## 5.1 왜 recipe인가

core set의 여러 묶음은 "짝"으로 의미를 가집니다. C2는 같은 전경 옆에서 원하는 배경 job과 아무도 요청하지 않은 배경 job(이름과 행동이 다른, 따로 측정된 job)을 견주는 두 파일의 짝이고, C5는 같은 장면에서 이름만 알아보기 어렵게 바꾼 짝입니다. 이 두 묶음의 짝의 가치는 "딱 이것만 다르다"에 있습니다. C2의 두 파일은 segment 0, 파일 길이, 공유 task의 모든 event가 같고 한 segment(그 job과 label)만 다릅니다(building plan §3 C2). 두 파일 사이에 다른 차이가 하나라도 끼면, 실험 결과의 차이를 그 하나의 변화로 돌릴 수 없습니다. C7은 base에서 배경 작업을 원하지 않는 쪽으로 바꾼 짝이지만, 한 군데만 다른 짝은 아닙니다. counterpart는 base의 앞 C초(C는 job의 CPU 총량)이므로 원하지 않는 job(또는 module build, 또는 label) 말고도 파일 길이, 입력 창, operation 시각이 base와 다르고, 키 입력은 base의 같은 시각 것에서 자기 operation 안에 든 것을 뺀 부분집합입니다(building plan §3 C7, 9.18 D1; 4.3절, 11.4절).

두 파일을 손으로 따로 관리하면, 누군가 한쪽만 고치는 순간 짝이 깨집니다. 그래서 차이 자체를 파일로 씁니다. `docs/data-contracts.md` §3은 이렇게 설명합니다. "rather than maintaining two hand-written files that must stay identical except in one spot, we write the difference itself … the 'identical except for exactly this' property is enforced by machinery rather than by care." 손으로 조심하는 대신 기계가 강제한다는 뜻입니다.

웹 개발의 비유로는 database migration이 가깝습니다. 최종 schema를 직접 고치는 대신 "어디서 무엇을 바꾸는가"를 적은 migration 파일을 쓰고, 도구가 그것을 적용합니다. 차이가 파일로 남으니 리뷰할 수 있고, 같은 migration을 다시 돌리면 같은 결과가 나옵니다.

> **왜 이렇게 정했나.** 이 방식은 task 2.4의 결정 1입니다(2026-08-28, `_dev/docs/spec/jioh/task-2.4-core-timelines.md`). "Novel timelines are plain base-format files; each derived file is a small yaml variant spec (`from: <base>` plus a closed set of ops …) executed by a generic deriver inside `make dataset`." 기록된 이유는 "The C2/C4/C5 disciplines are structural: a derived file provably differs from its base by exactly its ops"입니다. 같은 결정이 설계 문서의 이름을 이렇게 대응시킵니다. building-plan이 말하던 authoring sugar `inherit()`는 recipe의 `from:`이고, `inject:`는 `add-task` op이며, `variants:`는 recipe 하나가 여러 파일을 내놓는 것입니다. `dataset/README.md`의 도구 지도가 `deriver.py`를 "variants: / inherit() / inject: sugar"라고 부르는 것은 이 대응을 말합니다. 실제 recipe 파일에 `inherit()`나 `inject:`라는 글자는 나오지 않습니다.

`base` — recipe가 출발점으로 삼는 timeline입니다. 지금 tree에서는 모든 base가 사람이 쓴 파일(novel timeline)입니다. `derived file` — recipe로 만든 timeline입니다. `novel timeline` — 사람이 직접 쓴 timeline입니다. tree에 23개 있습니다(16개 C1, 3개 C2 base, 3개 C3, `c6-dual`).

## 5.2 recipe 파일의 모양

recipe 파일은 `dataset/timelines/coreset/*.variant.yaml`입니다. tree에 다섯 개 있고, 모두 합쳐 28개 파일을 만듭니다.

| recipe | 만드는 파일 | base |
|---|---|---|
| `c2-pairs.variant.yaml` | `c2-p1b`, `c2-p2b`, `c2-p2a-idle`, `c2-p3b` | `c2-p1a`, `c2-p2a`, `c2-p2a`, `c2-p3a` |
| `c4.variant.yaml` | `c4-gaming`, `c4-office`, `c4-compile` | `c1-gaming`, `c1-office`, `c1-compile` |
| `c5.variant.yaml` | `c5-t4`, `c5-t5` | `c1-media` 둘 다 |
| `c6.variant.yaml` | `c6-spoof`, `c6-alias`, `c6-fold` | `c1-browsing`, `c1-media`, `c1-browsing` |
| `c7.variant.yaml` | `c7-<mode>` 16개 | 각 mode의 `c1-<mode>` |

모양은 이렇습니다.

```yaml
variants:
  - id: c2-p1b                       # 만들 파일의 meta.id이자 파일 이름
    from: c2-p1a.timeline.yaml       # base, recipe 파일 기준 상대 경로
    ops:                             # 순서대로 적용할 명령
      - patch-task: {...}
      - patch-segment: {...}
```

top-level key는 `variants` 하나이고, 그 아래 항목마다 `id`, `from`, `ops`가 있습니다. recipe 파일의 주석은 사람에게 매우 중요합니다. 각 op가 왜 그 값인지가 거의 모두 주석에 적혀 있습니다(예: `c7.variant.yaml`의 첫 70여 줄). deriver는 주석을 읽지 않습니다.

## 5.3 아홉 개의 op

op의 집합은 닫혀 있습니다. deriver의 `OPS` 튜플에 있는 아홉 개만 쓸 수 있고, 다른 이름을 쓰면 `unknown op`으로 거절합니다(`dataset/tools/wlc/deriver.py`). 각 op의 동작과, tree의 다섯 recipe에서 쓰인 횟수입니다.

| op | 인자 | 동작 | 쓰인 횟수 |
|---|---|---|---|
| `rename` | `{from, to}` | 이름이 `from`인 **모든** task의 이름을 `to`로. 하나도 안 맞으면 오류 | 0 |
| `patch-segment` | `{index, …}` | `index`번째 segment에 나머지 field를 덮어씀. 범위 밖이면 오류 | 9 |
| `patch-task` | `{id, …}` | 그 `id`의 task에 나머지 field를 덮어씀. 없으면 오류 | 41 |
| `add-task` | task 한 줄 | task를 끝에 추가. 같은 `id`가 있으면 오류 | 16 |
| `set-segments` | 목록 | segment 목록을 통째로 교체 | 18 |
| `set-input` | 목록 | 입력 창 목록을 통째로 교체. 각 창에 `slice_of`를 붙일지 판단(5.6절) | 12 |
| `set-focus` | 목록 | focus 목록을 통째로 교체 | 15 |
| `set-operations` | 목록 | operation 목록을 통째로 교체 | 7 |
| `patch-meta` | `{…}` | `meta`에 덮어씀. 단 `seed`와 `id`는 금지 | 24 |

몇 가지 동작은 처음 보면 놓치기 쉽습니다.

**덮어쓰기는 얕습니다.** `patch-task`와 `patch-segment`와 `patch-meta`는 Python dict의 `update`로 덮어씁니다. 그래서 중첩된 map은 통째로 바뀝니다. 예를 들어 `c7-compile`의 op는 이렇습니다.

```yaml
      - patch-task: {id: build, name: dkms, archetype: module-build-orchestrator, arrive: 0s,
                     bind: {parallelism_cap: 8, child_name: cc1},
                     source: {parallelism_cap: convention, child_name: "meas-ci:background:2026-10-02"}}
```

base `c1-compile`의 `build` task는 `bind`에 `spawn_count: 2908`이 있었습니다. 이 op는 `bind`를 통째로 새 map으로 바꾸므로 `spawn_count`가 사라집니다. 바뀐 archetype `module-build-orchestrator`는 `spawn_count`를 받지 않으므로(3.3절의 표) 그것이 맞습니다. 같은 이유로 `patch-segment`에 `attributes`를 주면 attribute 전체가 바뀝니다. `c2-p1b`의 op가 `background_wanted`만 바꾸는 것처럼 보여도 실제로는 attribute map 전체를 `{background_wanted: false, initiated: session}`으로 갈아 끼웁니다. 9.18의 결정 4가 "Variant ops that write a `bind` write its `source`"라고 정한 것도 이 때문입니다. `bind`를 통째로 바꾸면서 `source`를 그대로 두면 key 집합이 어긋나고, lint가 그것을 잡습니다.

**`rename`은 지금 쓰이지 않습니다.** 코드에는 남아 있지만 다섯 recipe 어디에도 없습니다. 이름 바꾸기는 모두 `patch-task`로 합니다(`c5-t4`의 `{id: video, name: video-playback-}`처럼). `rename`은 같은 이름을 가진 task 전부를 바꾸므로, 특정 task 하나만 바꾸려면 `patch-task`가 안전합니다. `docs/data-contracts.md` §3의 예제 B도 2026-10-16부터 `c2-p1b`의 recipe를 `patch-task`로 보여 줍니다.

**`set-*` op들은 통째로 바꿉니다.** 일부만 고치는 방법은 없습니다. 길이를 줄이는 C7 counterpart는 segment, 입력 창, focus, operation을 모두 새로 적습니다.

> **왜 이렇게 정했나.** op 목록은 처음부터 아홉 개가 아니었습니다. task 2.4의 결정 1은 "replace-task, add-task, rename, set-meta, …" 정도를 예로 들었습니다. `set-input`(당시 이름 `set-focus`)과 `set-operations`는 9.10 D44(2026-10-01)가 counterpart를 줄일 때 입력 창과 operation 위치를 비율대로 옮기려고 더했습니다. 기록된 이유는 "a literal cut at C ≈ 26.5 s drops the four operations at 30/40 s"입니다. base를 그냥 26.385 s에서 자르면 30 s와 40 s에 있던 operation 네 개가 잘려 나간다는 것입니다. 9.17(2026-10-11)이 `set-focus`를 `set-input`으로 바꾸고, 새 focus track을 위한 `set-focus`를 더했습니다(`deriver.py`의 `OPS` 주석: "set-input (as set-focus), set-operations: 9.10 D44; set-focus on the window-focus track: 9.17").

## 5.4 seed와 id는 바꿀 수 없다

recipe는 seed를 바꿀 수 없습니다. deriver는 두 곳에서 막습니다. `derive_spec`은 variant 항목에 `seed` key가 있거나 어느 `patch-meta`에 `seed`가 있으면 "variants may not change the seed"로 거절합니다. `apply_ops`의 `patch-meta`는 `seed`나 `id`를 쓰려 하면 "patch-meta may not set the seed or id"로 거절합니다. `id`는 op가 아니라 recipe 항목의 `id`로만 정해지고, deriver가 마지막에 `derived["meta"]["id"] = variant["id"]`로 씁니다.

seed를 물려받는 것이 왜 그렇게 중요한지는 10장에서 숫자로 보겠습니다. 미리 결론만 말하면, 무작위 추출이 "(seed, task id, …)"를 열쇠로 하므로, 같은 seed와 같은 task id를 가진 task는 base와 파생 파일에서 **같은 값을 뽑습니다.** `c7-dev`의 편집기가 `c1-dev`의 편집기와 처음 26.385 s 동안 바이트 단위로 같은 이유입니다.

> **왜 이렇게 정했나.** task 2.4의 결정 4는 "the deriver warns on an explicit override"라고 적었습니다. 경고만 하라는 뜻입니다. 그러나 deriver는 첫 commit(`63c677dc`, 2026-08-28, 결정 4가 기록된 날)부터 경고가 아니라 오류로 거절했습니다. 코드가 경고한 적은 없으니 나중에 바뀐 것도 없습니다. 거절하는 이유는 2026-10-16에 인지오가 남은 기억으로 쓴 archive(`_dev/archive/2026-08-27-phase-2-grills-rationales.md`)가 적습니다. seed의 상속은 파생 파일의 짝 byte 규율이 기대는 규칙이고, 규칙은 경고가 아니라 거절로 지킨다는 것, 그리고 spec의 "warns"는 잘못 적은 말이라는 것입니다. 결정 4의 취지("a changed seed defeats the paired byte-discipline")도 거절 쪽이 지킵니다.

`demand` class는 `patch-meta`로 바꿀 수 있습니다. C4(끼어들기), C5(이름 사다리), C6(이름 인식의 한계)의 파생 파일과 C7(attribute counterpart) 전부(합쳐 24개)가 `patch-meta: {demand: calibration}`을 가집니다. base가 C1 calibration 파일이라 이미 `calibration`인 경우에도 굳이 다시 적습니다.

> **왜 이렇게 정했나.** 이것은 Phase 7의 결정 7입니다(2026-09-09, `_dev/docs/spec/jioh/phase-7-coreset-attribute-coverage.md`). "Every C7 file and the eight existing C1-derived files (`c4-*`, `c5-*`, `c6-fold`, `c6-spoof`) declare `demand: calibration` as an authored `patch-meta` in their variant recipe." 기록된 이유(Phase 7 archive의 결정 8)는 "`oversubscribed` cannot hold for a uniform op (gaming's base alone is 1.46); admitting inheritance keeps the exception invisible"입니다. 같은 op를 모든 mode에 걸면 CPU 수요가 mode마다 크게 달라서 `oversubscribed`라는 class를 지킬 수 없고(게임 base 하나만 해도 당시 1.46 lane이었습니다), class를 상속에 맡기면 그 예외가 보이지 않는다는 뜻입니다. 그래서 recipe에 눈에 보이게 적습니다. 당시 class는 build를 실패시키는 관문이었으므로 이 차이가 중요했습니다(12장).

## 5.5 deriver가 쓰는 파일

deriver(`derive_spec`)는 recipe 항목마다 다음 순서로 일합니다.

1. base 파일을 YAML로 읽습니다.
2. 그것을 깊은 복사합니다(`yaml.safe_load(yaml.safe_dump(base))`). base는 건드리지 않습니다.
3. op를 적힌 순서대로 적용합니다(`apply_ops`).
4. `meta.id`를 recipe의 `id`로 씁니다.
5. 머리말 두 줄을 붙이고, 내용을 `yaml.safe_dump(derived, sort_keys=True)`로 씁니다.
6. recipe와 같은 디렉터리에 `<id>.timeline.yaml`로 저장합니다.

결과 파일의 머리말은 이렇습니다.

```yaml
# GENERATED by dataset/tools/derive.py from c7.variant.yaml — do not hand-edit.
# base: c1-dev.timeline.yaml + ops; seed inherited from the base (byte-discipline).
```

`sort_keys=True` 때문에 파생 파일의 top-level key는 알파벳 순서(`focus`, `input`, `meta`, `operations`, `segments`, `tasks`)이고, 사람이 쓴 파일의 관례(`meta`가 맨 위)와 다릅니다. 또 한 줄짜리 `{…}` 표기가 아니라 들여쓰기 block 표기로 풀립니다. 그래서 파생 파일은 사람이 쓴 파일보다 길어 보이지만 내용은 같은 문법입니다. 파생 파일도 commit합니다. 사람이 recipe를 고친 뒤 deriver를 돌리지 않고 commit하면, CI의 drift 검사(5.7절)가 잡습니다.

> **코드로.** 머리말 문자열은 `deriver.py`의 `HEADER` 상수입니다. 머리말도 파일 바이트의 일부라서 `meta.derived_from`의 blob hash에 들어갑니다. generated layer에서 실제로 이것 때문에 문제가 생긴 적이 있습니다. 9.20 D10은 "A first run had changed every generated artifact through `meta.derived_from` because the generated files' header comment had been reworded … the header is part of the timeline bytes the artifact pins"라고 기록합니다. 주석 한 줄을 고쳤더니 모든 artifact의 hash가 바뀌었다는 것입니다.

## 5.6 recipe 예제 넷

**`c2-p1b` — 짝의 한쪽을 바꾸기.** base `c2-p1a`는 편집기와 MNIST 학습(`python`)입니다. recipe는 op 두 개로 학습을 GNOME 색인기로 바꾸고 label을 뒤집습니다.

```yaml
  - id: c2-p1b
    from: c2-p1a.timeline.yaml
    ops:
      - patch-task: {id: hog, name: tracker-miner-f, archetype: file-indexer,
                     arrive: 60s, bind: {total_work: 39.435s}, source: {total_work: "meas-ci:background:2026-10-02b"}}
      - patch-segment: {index: 1, mode: indexing,
                        attributes: {background_wanted: false, initiated: session},
                        scenario: [S11, S14]}
```

두 파일을 같은 형식으로 정규화해 diff하면, 다른 곳은 정확히 `meta.id`, 두 번째 segment의 mode·attributes·scenario, 그리고 `hog` task의 archetype·bind·name·source뿐입니다(이 권을 쓰며 `yaml.safe_dump(sort_keys=True)`로 두 파일을 정규화해 비교했습니다). 편집기 task, 입력 창, focus, 첫 segment, seed는 한 글자도 다르지 않습니다.

**`c2-p2a-idle` — op 하나짜리 짝.** 이 파일은 op가 하나입니다. `patch-task: {id: download, archetype: game-download-idle}`. 다운로드 task의 archetype만 같은 측정표를 쓰되 class가 `idle`인 entry로 바꿉니다. 9.13 D4는 compile된 두 파일이 "`download` task's class"에서만 다르고 다른 모든 event와 wake와 정답이 바이트 단위로 같다는 것을 test로 고정했습니다(`test_idle_download_variant_differs_in_the_class_alone`).

**`c7-dev` — 길이를 줄이고 배경 작업을 끼우기.** 이 recipe는 op 여섯 개를 씁니다.

```yaml
  - id: c7-dev
    from: c1-dev.timeline.yaml
    ops:
      - add-task: {id: upgrade, name: unattended-upgr, archetype: package-upgrade,
                   arrive: 0s, bind: {total_work: 26.385s}, source: {total_work: "meas-ci:background:2026-10-01"}}
      - set-segments: [{from: 0s, to: 26.385s, mode: dev,
                         attributes: {background_wanted: false, background: package-upgrade},
                         scenario: [S11, S17]}]
      - patch-task: {id: editor, depart: 26.385s}
      - set-input: [{from: 2s, to: 24.385s, task: editor}]
      - set-focus: [{from: 0s, to: 26.385s, task: editor}]
      - patch-meta: {demand: calibration}
```

`add-task`가 원하지 않는 무인 업그레이드를 0 s에 넣습니다(building-plan의 `inject:`가 이것입니다). `set-segments`가 파일을 업그레이드의 CPU 총량 26.385 s 길이의 segment 하나로 만들고 label을 `false`로 뒤집습니다. `patch-task`가 편집기를 26.385 s에 닫습니다. `set-input`이 입력 창을 2 s 여백을 지켜 2–24.385 s로 줄입니다. `set-focus`가 focus를 줄입니다. `patch-meta`가 class를 적습니다.

여기서 `set-input`이 특별한 일을 합니다. deriver의 `_sliced` 함수는 새 입력 창 각각에 대해, base의 **원래** 입력 창 중 같은 task의 것을 시간 순으로 늘어놓고, 새 창을 통째로 품는 첫 번째 base 창을 찾습니다. 찾으면 그 창의 `from`, `to`와 순번(`index`)을 `slice_of`로 붙입니다. 못 찾으면 그대로 둡니다. 사람이 이미 `slice_of`를 적었다면 손대지 않습니다. `c7-dev`의 새 창 2–24.385 s는 base `c1-dev`의 0번째 창 2–58 s 안에 있으므로, 결과 파일에 `slice_of: {from: 2s, to: 58s, index: 0}`이 붙습니다(4.3절에서 본 그 블록입니다). recipe를 쓴 사람은 base의 창을 다시 적을 필요가 없습니다. 9.18의 결정 2가 이것을 요구했습니다. "The author's variant spec does not restate the base's windows."

tree에서 `slice_of`를 가진 파일은 열두 개입니다. 입력 창이 있는 C7 counterpart 전부(`c7-backup`, `c7-browsing`, `c7-compile`, `c7-dev`, `c7-indexing`, `c7-mail`, `c7-ml-train`, `c7-office`, `c7-photo`, `c7-render`, `c7-transcode`, `c7-video-edit`)입니다. 나머지 C7 네 개(`c7-gaming`, `c7-idle`, `c7-media`, `c7-meeting`)는 base에 입력 창이 없습니다.

**`c4-office` — 끼어드는 프로그램 하나.** C4(distractor injection, 끼어들기 묶음)는 C1 calibration 파일에 상황을 바꾸지 않는 프로그램 하나를 30 s에 끼웁니다.

```yaml
      - add-task: {id: injected-burst, name: 7z, archetype: file-archiver,
                   arrive: 30s, bind: {total_work: 6s}, source: {total_work: design}}
```

`7z` 압축의 6 s는 측정값이 아니라 design입니다. recipe 주석이 이유를 적습니다. "the 7z burst's 6 s is design, the injection's size … an exception to 9.10 D17 (9.10 D161)". batch job을 통째로 묶는 규칙(9.10 D17)의 예외로, 끼어드는 크기로 정한 값이라는 뜻입니다.

## 5.7 `derive.py`와 drift 검사

`dataset/tools/derive.py`는 deriver를 부르는 CLI입니다. 하는 일은 세 가지입니다.

1. `deriver.run`으로 `dataset/timelines/` 아래의 모든 `*.variant.yaml`을 경로 순으로 실행합니다. 기본 모드에서는 파생 파일을 씁니다. `--check` 모드에서는 쓰지 않고, 디스크의 파일이 지금 만들 결과와 바이트 단위로 같은지만 봅니다. 다르면 "differs from its variant spec (derive drift)", 없으면 "missing (derive drift)"입니다.
2. coverage grid(`dataset/coverage-grid.json`)를 만들거나(`--check`면 비교만) 합니다. core timeline과 generated set의 manifest에서 셉니다.
3. `--require-coverage`가 있으면 driver table의 32칸 중 빈 칸이 있을 때 실패합니다.

`make dataset`은 1과 2를 쓰기 모드로, `make check`는 `derive.py --check --require-coverage`로 돌립니다. 이것이 lockfile 패턴입니다. `deriver.py`의 docstring은 "Derived files are committed; `check` mode re-derives and fails on drift (lockfile pattern)"라고 적습니다. `package-lock.json`을 commit하고 CI에서 `npm ci`로 다시 만들어 비교하는 것과 같은 구조입니다. 다만 `derive.py --check`는 디스크의 파일을 새로 파생한 결과와 비교할 뿐이라, `make dataset`이 다시 쓰고 commit하지 않은 파생 파일은 이 검사를 통과합니다. 2026-10-15부터는 `make check`의 `check_build.py`가 파생 timeline과 `coverage-grid.json`을 commit된 byte(`git show HEAD:<path>`)와도 비교해 그것을 잡습니다(9.23 D12, 13.7절).

---

# 6장 · 두 timeline을 줄 단위로 읽기

지금까지 field 하나하나를 따로 보았습니다. 이 장에서는 실제 파일을 처음부터 끝까지 한 줄씩 읽고, 각 줄이 compile 후 canonical 파일의 어디가 되는지 숫자로 따라갑니다. 단순한 `c1-office`, 짝을 이루는 `c2-p1a`와 `c2-p1b`, 그리고 task 두 줄이 arrive event 18개가 되는 `c1-gaming`을 읽습니다. compile의 내부 동작은 9–13장에서 자세히 설명하므로, 여기서는 "무엇이 되는가"에 집중하고 "어떻게"는 뒤 장을 가리킵니다. 숫자는 모두 tree의 `dataset/build/coreset-single/`에 있는 blessed artifact와 report에서 읽었습니다.

## 6.1 단순한 파일: `c1-office`

전체 파일은 31줄입니다.

```yaml
# C1 — single-situation calibration: pure office (building-plan §3 C1).
# The four renderer-hidden tasks are the other tabs' page renderers of one
# five-tab window: five tabs from Firefox's Linux telemetry (glam; 9.10 D15,
# D16), one renderer per tab observed in Chrome (meas-ci:desktop:2026-10-04;
# 9.10 D126-D129, D131).
# The desktop's session processes are omitted, their active state unobservable on the runner (9.10 D28).
```

**주석 여섯 줄.** 이 파일이 C1, 즉 한 상황만 담은 calibration 묶음의 "순수 사무" 파일이라는 것, 숨은 renderer 네 개의 근거(3.4절), 그리고 desktop의 session process(`gnome-shell`, `pipewire` 같은)를 이 파일이 싣지 않는다는 것을 적습니다. 마지막 줄은 2026-10-16에 9.10 D28(session process는 idle 파일에만 싣는다는 결정)을 파일에 적으려고 더했습니다. compiler는 주석을 읽지 않지만, 주석도 파일 바이트이므로 blob hash에 들어갑니다. 주석 한 글자를 고쳐도 artifact의 hash가 바뀝니다.

`C1` — core set의 첫 번째 묶음입니다. 메뉴의 mode 열여섯 개마다 한 파일씩, 한 상황만 60 s 동안 담은 calibration 파일입니다(batch mode는 job이 끝날 때까지 길어집니다).

```yaml
meta:
  id: c1-office
  seed: 101
  demand: calibration
```

**`meta`.** id는 `c1-office`, seed는 101, demand class는 `calibration`입니다. compile 후 canonical `meta`는 이렇게 됩니다.

```json
"meta": {
  "derived_from": "dataset/timelines/coreset/c1-office.timeline.yaml@1b5295f96a851b62184a3a1dbe3f575f45bb3bbc",
  "id": "c1-office",
  "sampled": {"archetypes": "archetypes.yaml@c78d8cf911ecd820413602226ea8adb71945edd1", "seed": 101}
}
```

`@` 뒤의 `1b5295f9…`는 이 timeline 파일의 git blob hash입니다. `git hash-object dataset/timelines/coreset/c1-office.timeline.yaml`로 확인하면 같은 값이 나옵니다. `c78d8cf9…`는 `dataset/archetypes.yaml`의 blob hash입니다(2026-10-17 tree. timeline이나 library의 byte가 바뀔 때마다 두 hash도 바뀝니다). `demand: calibration`은 canonical `meta`에 없고 compile report의 `demand_class`로만 갑니다.

```yaml
segments:
  - {from: 0s, to: 60s, mode: office, attributes: {background_wanted: true},
     scenario: [S1, S2, S4]}
```

**segment 하나.** 0–60 s가 `office`이고, 배경 작업은 원하는 것(여기서는 배경 작업이 없으므로 관례상 `true`)입니다. scenario S1(사무), S2(웹 browsing), S4(메일)가 이 조합이 실재한다는 근거입니다. compile 후 `ground_truth`는 `[{"attributes": {"background_wanted": true}, "mode": "office", "t_end": 60000000, "t_start": 0}]`입니다. `scenario`는 사라졌고, 시간은 µs가 되었습니다.

```yaml
tasks:
  - {id: writer, name: soffice.bin, archetype: office-writer,
     arrive: 0s, depart: 60s}
  - {id: browser, name: chrome, archetype: web-browser,
     arrive: 0s, depart: 60s}
  - {id: renderers, name: chrome, archetype: renderer-hidden,
     arrive: 0s, depart: 60s, count: 4,
     source: {count: [glam, "meas-ci:desktop:2026-10-04"]}}
  - {id: mail, name: thunderbird-bin, archetype: mail-client,
     arrive: 0s, depart: 60s}
```

**task 네 줄.** LibreOffice Writer(`soffice.bin`), Chrome 브라우저(`chrome`), Chrome의 숨은 탭 renderer 넷(`chrome` × 4), Thunderbird(`thunderbird-bin`)입니다. 넷 다 segment-bound archetype이므로 `depart`가 있습니다. `bind`는 하나도 없습니다(이 archetype들의 `binding_params`가 비어 있습니다). `count`를 쓴 줄만 `source`를 가집니다.

넷 다 0 s에 도착합니다. `office-writer`, `web-browser`, `mail-client`는 실행 직후의 시작 활동(launch phase)을 측정해 두었지만, 0 s에 있는 task는 이미 안정 상태로 봅니다(9.10 D21, "one at 0 s is already steady"). 그래서 이 파일에서는 launch phase가 재생되지 않습니다.

compile 후 이 네 줄은 arrive event **일곱 개**가 됩니다. `count: 4` 때문입니다. tree의 artifact에서 읽은 각 arrive event의 program 길이와 wake 수입니다.

| arrive id | name | program 명령어 수 | 그 task를 깨우는 wake event |
|---|---|---|---|
| `browser` | `chrome` | 5,357 | `timer:browser` 2,678 |
| `mail` | `thunderbird-bin` | 271 | `timer:mail` 135 |
| `renderers.1` | `chrome` | 25 | `timer:renderers.1` 12 |
| `renderers.2` | `chrome` | 23 | `timer:renderers.2` 11 |
| `renderers.3` | `chrome` | 29 | `timer:renderers.3` 14 |
| `renderers.4` | `chrome` | 19 | `timer:renderers.4` 9 |
| `writer` | `soffice.bin` | 951 | `timer:writer` 205, `input:writer` 270 |

각 program은 `WAIT`와 `RUN`이 번갈아 나오는 목록입니다. 예를 들어 `browser`의 처음 네 명령어는 `WAIT timer:browser`, `RUN 13`, `WAIT timer:browser`, `RUN 23`입니다. "timer로 깨어날 때까지 기다렸다가 CPU를 13 µs 쓰고, 다시 기다렸다가 23 µs 쓴다"는 뜻입니다. 명령어 수가 wake 수의 두 배에 하나를 더한 값인 이유가 이것입니다. wake마다 WAIT 하나와 RUN 하나가 있고, 마지막 wake 뒤에 같은 channel의 WAIT 하나가 더 붙습니다(11.1절). 이 timer wake들은 측정한 프로그램의 thread들이 스스로 깨어나는 패턴(component)에서 뽑은 것입니다(11.1절).

`component` — 측정된 archetype의 활동을 thread 이름별로 나눈 조각입니다. 각 component는 "깨어나는 간격의 분포"와 "깨어날 때마다 쓰는 CPU의 분포"를 가집니다. 예를 들어 `code-editor`에는 `renderer/Compositor`, `utility/libuv-worker` 같은 component가 있습니다.

```yaml
input:
  - {from: 2s, to: 58s, task: writer}
```

**입력 창.** 2–58 s 동안 Writer에 타자를 칩니다. compile하면 이 줄은 `input:writer` channel의 wake event 270개가 됩니다. 첫 키 입력은 2,059,422 µs, 즉 2.059 s에 떨어집니다. 이 값이 어떻게 나오는지는 11.4절에서 손으로 계산합니다(미리 결과만 말하면, Word 타자 기록의 13,866,357,078 µs 지점부터 56 s를 잘라 온 것입니다).

브라우저(`web-browser`)와 메일(`mail-client`)도 stimulus를 가진 archetype이지만, 입력 창이 없으므로 키 입력을 받지 않습니다. 그 둘은 timer wake로만 깨어납니다. 사용자가 다른 창에 타자를 치는 동안 뒤에서 잔잔히 돌아가는 앱의 모습입니다.

```yaml
focus:
  - {from: 0s, to: 60s, task: writer}
```

**focus.** 처음부터 끝까지 Writer가 앞에 있습니다. compile 후 `focus`는 `[{"t_end": 60000000, "t_start": 0, "task": "writer"}]`입니다.

`operations` key는 없습니다. `web-browser`는 `page-load` operation을 가지지만, 9.10 D20의 규칙("every focus window on a task whose entry carries an operation holds one of it")은 그 앱에 입력 창이 있을 때 operation을 두라는 것이고, 이 파일에서 브라우저는 입력 창이 없습니다.

**결과 전체.** canonical 파일은 443,368 byte이고, event가 3,341개(arrive 7, wake 3,334)입니다. compile report에 따르면 일곱 task의 CPU 수요 합계는 1,617,440 µs이고, 60 s로 나눈 utilization은 0.02696입니다(manifest에는 소수 넷째 자리로 0.027). task별로는 Writer 1,358,623 µs, 브라우저 176,518 µs, 메일 80,359 µs, renderer 넷이 436·363·498·643 µs입니다. 사무 장면은 CPU를 3 %도 쓰지 않습니다. 이 파일이 "calibration"인 이유가 숫자로 보입니다.

## 6.2 짝을 이루는 파일: `c2-p1a`와 `c2-p1b`

`c2-p1a`도 31줄이지만 담긴 결정이 훨씬 많습니다.

```yaml
# C2 P1 (load-bearing pair, base) — {code, python}: a training run beside an
# editor, PyTorch's basic MNIST example, `cpu-batch`'s `python3` program
# (meas-ci:background:2026-10-03), shown as `python`, bound whole at its
# measured CPU total (9.10 D12, D17, D85); the variant (c2-pairs.variant.yaml)
# puts Tracker's first index of a home in its place, `file-indexer` shown as
# `tracker-miner-f` (D6, D80). Segment 1 is as long as the index's measured CPU
# total, 39.435 s, in both files, so each job is alive at every instant of it
# under every policy; the training runs on past the file's end (D80, D86).
# The desktop's session processes are omitted, their active state unobservable on the runner (9.10 D28).
```

**주석.** C2의 첫 번째 짝(P1)의 base입니다. 편집기(`code`) 옆에서 PyTorch MNIST 학습(`python`)이 돌고, 짝 파일에서는 그 자리에 GNOME Tracker의 첫 색인이 들어갑니다. 두 번째 segment의 길이는 색인의 CPU 총량인 39.435 s로, 두 파일에서 같습니다. "so each job is alive at every instant of it under every policy", 즉 어떤 scheduling 정책 아래에서도 그 segment 동안 job이 살아 있도록 길이를 정했다는 뜻입니다. 그리고 학습은 파일이 끝난 뒤에도 계속 돌았을 것이라고 적습니다. 마지막 줄은 6.1절의 `c1-office`와 같은 session process의 생략입니다.

`C2` — core set의 두 번째 묶음, intent pair입니다. 같은 전경 옆에서 사용자가 원하는 배경 job과 아무도 요청하지 않은 배경 job을 짝지어, 무엇이 둘을 가를 수 있는지 봅니다. 두 번째 파일의 job은 첫 파일의 것과 이름과 행동이 다른, 따로 측정된 job이고(P1과 P3은 선언된 class도 다름), 두 파일은 한 segment(그 job과 label)만 다릅니다. 짝이 셋(P1, P2, P3)이고, P2에는 bounding check용 파일 `c2-p2a-idle`이 하나 더 있습니다.

```yaml
meta:
  id: c2-p1a
  seed: 201
```

**`meta`.** `demand`가 없으므로 기본값 `oversubscribed`입니다. C2는 CPU 경쟁을 일으키도록 설계된 묶음입니다.

```yaml
segments:
  - {from: 0s, to: 60s, mode: dev, attributes: {background_wanted: true},
     scenario: [S11]}
  - {from: 60s, to: 99.435s, mode: ml-train, attributes: {background_wanted: true},
     scenario: [S11, S12]}
```

**segment 둘.** 0–60 s는 개발(`dev`), 60–99.435 s는 ML 학습(`ml-train`)입니다. 둘 다 배경 작업을 원합니다. 학습은 사용자가 시킨 것이기 때문입니다. compile 후 `ground_truth`의 두 항목은 `t_end` 60,000,000과 99,435,000을 가집니다.

```yaml
tasks:
  - {id: editor, name: code, archetype: code-editor,
     arrive: 0s, depart: 99.435s}
  - {id: hog, name: python, archetype: cpu-batch, arrive: 60s,
     bind: {total_work: 1389.885s, program: python3},
     source: {total_work: "meas-ci:background:2026-10-03", program: [pytorch-examples, "meas-ci:background:2026-10-03"]}}
```

**task 둘.** 편집기는 VS Code(`code`)이고 파일 끝까지 열려 있습니다. 학습 job `hog`는 60 s에 도착합니다. `cpu-batch`는 finite archetype이므로 `depart`가 없습니다. `bind`는 CPU 총량 1,389.885 s(약 23분)와 측정표 `python3`이고, `source`가 둘 다 2026-10-03 background campaign을 가리킵니다. 이름은 `python3`가 아니라 `python`입니다. 9.10 D84가 정한 대로, venv가 실제로 실행하는 파일 이름이 `python`이기 때문입니다(`cpu-batch`의 modeling note, "its process shows `python`, the name the venv executes").

compile 후 `hog`의 arrive event는 이렇습니다(앞부분).

```json
{"declared_class": "normal", "id": "hog", "name": "python", "op": "arrive", "t": 60000000,
 "program": [{"op": "RUN", "us": 192}, {"op": "SLEEP", "us": 378}, {"op": "RUN", "us": 135}, {"op": "SLEEP", "us": 359}, …, {"op": "EXIT"}]}
```

`depart`가 없고, program이 `EXIT`로 끝납니다. 명령어는 56개뿐입니다(RUN 28, SLEEP 27, EXIT 1). 23분짜리 job이 56개 명령어인 것은, 측정된 MNIST 학습이 거의 쉬지 않고 CPU를 쓰기 때문입니다. compiler는 "측정된 run 하나 → 그 뒤의 block 하나"를 반복해 뽑는데, block이 0으로 나오면(쉬지 않고 계속 돌았다는 측정값) 앞뒤 run을 하나로 합칩니다(11.6절). 그래서 RUN 하나가 685,714,830 µs, 약 11.4분짜리도 있습니다. RUN 28개를 모두 더하면 정확히 1,389,885,000 µs, 즉 `total_work`입니다.

```yaml
input:
  - {from: 2s, to: 97.435s, task: editor}

focus:
  - {from: 0s, to: 99.435s, task: editor}
```

**입력과 focus.** 2 s 여백을 두고 편집기에 타자를 치고, 편집기가 내내 앞에 있습니다. 학습 job은 창이 없으므로 focus를 쥐지 않습니다.

**결과 전체.** event는 11,346개(arrive 2, wake 11,344)이고, 편집기의 program은 22,689 명령어이고, 마지막 명령어는 마지막 wake의 channel 위의 `WAIT timer:editor`입니다(11.1절). 편집기를 깨우는 wake는 `timer:editor` 10,819개와 `input:editor` 525개입니다. 편집기는 사용자의 키 입력(525개)보다 자기 thread들의 timer(10,819개)로 훨씬 자주 깨어납니다. compile report의 utilization은 14.505이고, segment별로는 0.5272와 35.7721입니다. 이 이상하게 큰 숫자의 정체는 12.4절에서 설명합니다(학습의 23분어치 CPU를 39.435 s짜리 segment에 펼쳐 계산했기 때문입니다).

**짝 파일 `c2-p1b`.** 5.6절에서 본 두 op가 `hog`를 `tracker-miner-f`(archetype `file-indexer`, CPU 39.435 s)로 바꾸고 두 번째 segment를 `indexing`, `background_wanted: false`, `initiated: session`으로 바꿉니다. compile하면 무엇이 같고 무엇이 다를까요. 편집기는 task id(`editor`)와 seed(201)가 같으므로 program과 wake가 바이트 단위로 같습니다(10.4절). 첫 segment의 정답도 같습니다. 다른 것은 `hog`의 이름, class(`file-indexer`는 `idle`), program(색인기의 측정표에서 뽑음), 그리고 두 번째 segment의 정답입니다. recognizer가 볼 수 있는 차이는 이름(`python` 대 `tracker-miner-f`)과 class(`normal` 대 `idle`)뿐입니다.

## 6.3 constructor가 펼치는 파일: `c1-gaming`

```yaml
# C1 — single-situation calibration: pure gaming (building-plan §3 C1).
# The game's threads beyond the chain and `wineserver` are omitted: the source
# puts 95% of scheduling in its top 30-40 tasks and describes none outside
# them (lavd-ossna24 s12; 9.10 D19).
# The Steam client is in its measured state: logged out, no account, no
# library, no game behind it, no `gameoverlayui` (9.10 D22; 9.8 D6).
# The desktop's session processes are omitted, their active state unobservable on the runner (9.10 D28).
meta:
  id: c1-gaming
  seed: 102
  demand: calibration

segments:
  - {from: 0s, to: 60s, mode: gaming, attributes: {background_wanted: true},
     scenario: [S9]}

tasks:
  - {id: game, name: Troy.exe, archetype: game-task-chain,
     arrive: 0s, depart: 60s, bind: {lane_share: 0.9,
           member_names: ["Task worker thr", "Task worker thr", "Task worker thr", "Task worker thr", dxvk-cs, dxvk-submit, winepulse_mainl, winepulse_timer, FAudio_AudioCli, Troy.exe, Troy.exe, Troy.exe, Troy.exe, Troy.exe, Troy.exe]},
     source: {lane_share: design, member_names: "lavd-ossna24:s16"}}
  - {id: steam, name: steam, archetype: game-client,
     arrive: 0s, depart: 60s}

input: []

focus:
  - {from: 0s, to: 60s, task: game}
```

이 파일의 task는 두 줄입니다. 게임 `Troy.exe`와, 로그인하지 않은 Steam client입니다. `Troy.exe`는 LAVD 발표 자료(`lavd-ossna24`)의 16번 slide가 보여 준 process tree에서 게임의 main thread가 단 이름입니다. 출처는 그 게임과 기계가 무엇인지 밝히지 않습니다(9.4 D1, "one observation of an unnamed game on an unnamed machine"). Windows 게임이 Wine 위에서 돌면 process가 자기 `.exe` 이름으로 보입니다(9.10 D26). 입력 창은 없고, 게임이 내내 focus를 쥡니다. 머리 주석 일곱 줄 가운데 뒤의 여섯 줄은 2026-10-16에 더한 것으로, 이 파일이 싣지 않는 것(chain 밖의 게임 thread와 desktop의 session process)과 Steam client의 측정된 상태를 적습니다(9.10 D19, D22, D28).

`Wine` — Windows 프로그램을 Linux에서 돌리는 호환 계층입니다. `wineserver`는 Wine이 띄우는 조정용 process로, 게임 thread들 사이의 요청을 중계합니다. `Proton` — Steam이 쓰는 Wine 기반 호환 계층입니다.

**`game` 한 줄이 arrive event 17개가 됩니다.** archetype `game-task-chain`은 library에서 유일하게 "모양 자체가 parameter인" entry입니다. compiler의 **chain constructor**가 이 한 줄을 한 줄로 이어진 task 17개로 펼칩니다(11.9절). 머리(`game.chain.1`, 이름 `Troy.exe`), 그 다음 `game.wineserver`(이름 `wineserver`), 그리고 `game.chain.2`부터 `game.chain.16`까지(이름은 `member_names`의 15개를 순서대로)입니다. tree의 artifact에서 처음 세 구성원의 program은 이렇습니다.

```json
{"id": "game.chain.1", "name": "Troy.exe", "program": [{"op": "LOOP", "count": "unbounded", "body": [
    {"op": "TIMER", "period_us": 16667}, {"op": "RUN", "us": 631}, {"op": "WAKE", "target": "game.wineserver"}]}]}
{"id": "game.wineserver", "name": "wineserver", "program": [{"op": "LOOP", "count": "unbounded", "body": [
    {"op": "WAIT", "channel": "chain:game.wineserver"}, {"op": "RUN", "us": 341}, {"op": "WAKE", "target": "game.chain.2"}]}]}
{"id": "game.chain.2", "name": "Task worker thr", "program": [{"op": "LOOP", "count": "unbounded", "body": [
    {"op": "WAIT", "channel": "chain:game.chain.2"}, {"op": "RUN", "us": 1052}, {"op": "WAKE", "target": "game.chain.3"}]}]}
```

머리는 16,667 µs(1/60 s)마다 TIMER로 깨어나 631 µs 일하고 `wineserver`를 깨웁니다. `wineserver`는 깨어나면 341 µs 일하고 다음 구성원을 깨웁니다. 그렇게 양동이 릴레이처럼 frame 하나가 열일곱 단계를 거쳐 내려갑니다. 마지막 `game.chain.16`은 1,159 µs 일하고 아무도 깨우지 않습니다. 열일곱 단계의 RUN을 모두 더하면 14,999 µs이고, 이것은 0.9 × 16,667 = 15,000.3 µs에 반올림 오차만큼 가깝습니다. `lane_share: 0.9`가 "chain이 frame마다 CPU의 90 %를 쓰도록 맞춘다"는 뜻이기 때문입니다. 이 계산은 11.9절에서 처음부터 다시 합니다.

chain에는 wake **event**가 하나도 없습니다. 머리는 자기 TIMER로 깨어나고, 나머지는 앞 구성원의 `WAKE` **명령어**로 깨어납니다. 외부에서 시각을 박아 넣을 일이 없습니다. 이 파일의 wake event 18,062개는 모두 Steam client(`timer:steam`)의 것입니다.

**`wineserver`라는 이름은 timeline에 없습니다.** `member_names`는 15개이고, 구성원은 17개입니다. 머리는 task의 `name`(`Troy.exe`)을, `wineserver`는 compiler가 직접 붙인 이름을 가집니다. 이것은 generated layer의 이름 바꾸기 실험에서 중요한 제약이 됩니다. `dataset/README.md`는 familiarity ladder를 설명하며 "the chain's `wineserver`, named by the compiler, keeps its name"이라고 적습니다. timeline의 이름을 바꿔도 compiler가 붙이는 이름은 그대로 남는다는 뜻입니다.

**focus가 가리키는 것.** timeline의 focus는 `task: game`입니다. 그런데 canonical 파일에는 `game`이라는 id의 arrive event가 없습니다. compiler는 task 이름(`Troy.exe`)을 가진 첫 구성원, 즉 머리 `game.chain.1`을 focus의 주인으로 씁니다. 그래서 canonical `focus`는 `[{"t_end": 60000000, "t_start": 0, "task": "game.chain.1"}]`입니다(9.17 D2).

**결과 전체.** event 18,080개(arrive 18, wake 18,062), artifact 2,296,348 byte, utilization 0.9153입니다. task별 수요는 chain 구성원 열일곱이 합쳐 약 54.0 s, Steam client가 0.92 s입니다(compile report의 `per_task`).

## 6.4 더 큰 파일에서 보이는 것

**`c3-workday`.** segment 네 개(browsing 0–60 s → office 60–120 s → compile 120–1,485 s → mail 1,485–1,545 s), task 다섯 줄(브라우저, renderer × 4, Writer, `make`, Thunderbird), 입력 창 셋, focus 구간 셋, operation 둘(30 s의 page load, 1,525 s의 메일 전송)입니다. compile하면 arrive event 8개, `make`의 spawn table 17,448칸, wake event 92,827개(timer 92,621, input 206)가 됩니다. Writer는 60 s에, Thunderbird는 1,485 s에 도착하므로 둘 다 측정된 launch phase를 먼저 재생합니다(11.3절). 파일 머리 주석은 "the file ends inside Thunderbird's", 파일이 Thunderbird의 시작 구간이 끝나기 전에 끝난다고 적습니다.

**`c6-dual`.** segment 하나(0–12,072 s, `ambiguous`), task 셋(게임 chain, 편집기, `make`), 입력 창 아홉, focus 구간 열여덟입니다. compile하면 arrive event 19개(chain 17, 편집기, `make`), spawn table 17,448칸, wake event 1,371,292개, artifact 187,601,795 byte(약 188 MB)로 core set에서 가장 큰 파일입니다. wake event는 거의 모두 편집기의 것입니다. `timer:editor`가 1,357,541개, `input:editor`가 13,751개입니다(tree에서 센 값). 3시간 21분 동안 VS Code의 thread들이 스스로 깨어나는 사건 하나하나가 event로 적혀 있어서 파일이 커집니다.

---

# 7장 · Canonical workload 포맷

이 장은 compile의 결과물, canonical workload 파일의 모양을 field 하나하나 설명합니다. 기계 형태의 정의는 JSON Schema 파일 `dataset/schema/workload.schema.json`(255줄, JSON Schema 2020-12)이고, 의미의 정의는 `docs/simulator/interpretation-contract.md` §3–§5입니다. schema의 머리 설명은 이 파일을 "the only format the simulator ever reads"라고 부릅니다. simulator는 timeline도, archetype library도 읽지 않습니다. 오직 이 파일만 읽습니다.

## 7.1 네 개의 top-level key

canonical 파일은 JSON object 하나이고, key가 정확히 네 개입니다. 넷 다 필수이고, 다른 key는 허용되지 않습니다(schema의 `required`와 `additionalProperties: false`).

| key | 무엇 | 누가 읽나 |
|---|---|---|
| `meta` | 출처: 어느 timeline, 어느 library, 어느 seed에서 왔나 | 사람, harness의 추적. scheduler는 읽지 않음 |
| `ground_truth` | 정답 label의 구간 목록 | oracle 조건과 채점자만 |
| `focus` | 창 focus 구간 목록 | recognizer(projection과 telemetry를 거쳐). simulator는 읽지 않음 |
| `events` | task의 도착(arrive)과 외부 wake | simulator. recognizer는 이름·개수·박힌 시각만 |

"누가 읽나"는 8장에서 따로 다룹니다. 여기서는 모양만 봅니다.

**바이트 형태.** compiler는 canonical dict를 `json.dumps(canonical, sort_keys=True, separators=(",", ":"))`로 쓰고 끝에 줄바꿈 하나를 붙입니다(`wlc/compiler.py`의 `canonical_bytes`). 공백이 하나도 없고, 모든 key가 알파벳 순서입니다. 그래서 파일의 첫 key는 `meta`가 아니라 `events`입니다(`events` < `focus` < `ground_truth` < `meta`). `head -c` 로 파일을 열어 보면 `{"events":[{"declared_class":"normal","depart":60000000,"id":"browser",…`로 시작하는 이유가 이것입니다. key 순서를 정렬하는 것은 바이트 단위 재현을 위해서입니다. Python dict의 삽입 순서에 기대면 코드의 작은 변화가 바이트를 바꿀 수 있습니다. manifest가 hash하는 것도 이 바이트입니다.

## 7.2 `meta`: 출처

```json
"meta": {
  "derived_from": "dataset/timelines/coreset/c2-p1a.timeline.yaml@a0effee93e945b3d39f8aa3501475f31896d58d8",
  "id": "c2-p1a",
  "sampled": {"archetypes": "archetypes.yaml@c78d8cf911ecd820413602226ea8adb71945edd1", "seed": 201}
}
```

- **`id`** — 필수, 빈 문자열이 아닌 문자열. timeline의 `meta.id`입니다.
- **`derived_from`** — 필수. 모양이 `^.+@[0-9a-f]{7,40}$`이어야 합니다. `@` 앞은 저장소 root 기준의 timeline 경로, 뒤는 그 파일 내용의 git blob hash입니다.
- **`sampled`** — 필수. `seed`(0 이상의 정수)와 `archetypes`(`archetypes.yaml@<hex>`, library 파일의 git blob hash)를 가집니다.
- **`expectations`** — 선택. harness가 소유하는 자유 형식 채점 기대값입니다. 지금 compiler는 이 key를 쓰지 않습니다.

schema는 `sampled`를 이렇게 설명합니다. "every concrete number in this file traces to its distribution via this pair (contract §1, RNG-free simulator)." 파일 안의 어떤 숫자든, 이 두 hash가 가리키는 timeline과 library, 그리고 seed만 있으면 어느 분포에서 어떻게 뽑혔는지 다시 계산할 수 있다는 뜻입니다.

**git blob hash란.** `git_blob_hex`(`wlc/library.py`)는 파일 바이트 앞에 `blob <길이>\0`을 붙여 SHA-1을 계산합니다. `git hash-object`와 같은 값입니다. git 저장소가 없어도 계산할 수 있고, 내용이 같으면 언제 어디서 계산해도 같습니다. 이 값은 commit hash가 아니라 그 파일 내용의 hash입니다. schema의 설명은 2026-10-17부터 이것을 "the git blob hash of its content"라고 적고(그 전에는 "the commit it was compiled from", "the library commit"), interpretation contract §1, §4는 2026-10-16부터 `<git blob hash>`라고 적습니다. 그래서 commit하지 않은 수정본을 compile해도 `derived_from`이 바뀝니다.

> **코드로.** `compile_one`(`dataset/tools/compile.py`)이 `rel_path = path.relative_to(root).as_posix()`로 저장소 기준 경로를 만들어 `compile_timeline`에 넘기고, `compile_timeline`이 `f"{rel}@{timeline.blob_hex}"`로 `derived_from`을 만듭니다. library hash는 `Library` 생성자가 한 번 계산합니다.

**variant 파일의 `meta`.** 민감도 실험용 variant(`<base>@<set>.workload.json`, 예: `c2-p1a@replay`)는 `meta.id`만 `<base>@<set>`으로 바꾸고 `derived_from`과 `sampled`는 base의 것을 그대로 둡니다. 9.14 D8은 그 이유를 "the workload contract has no slot for a transform — and the manifest is the provenance"라고 적습니다. 어떤 변환을 했는지 적을 자리가 canonical 형식에 없으므로, 변환의 기록은 variant manifest(`dataset/build.variants.manifest.json`)가 맡습니다.

## 7.3 `ground_truth`: 정답

```json
"ground_truth": [
  {"attributes": {"background_wanted": true}, "mode": "dev", "t_end": 60000000, "t_start": 0},
  {"attributes": {"background_wanted": true}, "mode": "ml-train", "t_end": 99435000, "t_start": 60000000}
]
```

timeline의 `segments`가 시작 시각 순으로 그대로 옮겨진 것입니다. 항목마다 `t_start`, `t_end`, `mode`가 필수이고, `attributes`와 `familiarity`는 선택입니다. compiler는 `attributes`를 항상 씁니다(timeline에서 비어 있으면 `{}`). `familiarity`는 timeline에 적혀 있을 때만 씁니다. `scenario`는 옮기지 않습니다.

schema는 `mode`의 값을 열여섯 개로 제한하지 않습니다. 빈 문자열이 아니기만 하면 됩니다. 설명이 이유를 적습니다. "the mode vocabulary is owned by the driver table, not this schema." 메뉴는 driver table이 소유하고, 그 검사는 coverage grid 생성기가 합니다(2.4절).

## 7.4 `focus`: 창 focus

```json
"focus": [{"t_end": 60000000, "t_start": 0, "task": "game.chain.1"}]
```

timeline의 `focus` track이 옮겨진 것입니다. 항목마다 `t_start`, `t_end`, `task`가 필수입니다. `task`는 top-level `arrive` event의 `id`여야 합니다. 보통은 timeline의 task id 그대로이고, constructor로 펼친 task(게임 chain)라면 task의 이름을 가진 첫 구성원, 즉 머리입니다(6.3절). timeline에서 focus를 비워 두었다면 `[]`입니다.

schema의 설명은 이 key가 정답이 아니라는 것을 분명히 합니다. "Not an answer key: the recognizer is shown it."

## 7.5 `events`: 두 종류의 사건

`events`는 시각(`t`) 순으로 정렬된 목록이고, 항목은 두 종류 중 하나입니다(schema의 `oneOf`). contract §4가 "a closed op set of two"라고 부르는 것입니다.

**`arrive`** — task가 태어나는 사건입니다.

| field | 필수? | 뜻 |
|---|---|---|
| `t` | 필수 | 도착 시각(µs) |
| `op` | 필수 | 문자열 `"arrive"` |
| `id` | 필수 | 파일 안에서 유일한 task id |
| `name` | 필수 | recognizer가 보는 process 이름 |
| `declared_class` | 필수 | `"normal"` 또는 `"idle"` |
| `program` | 필수 | 명령어 목록(7.6절), 한 개 이상 |
| `depart` | segment-bound일 때만 | 사용자가 닫는 시각(µs) |
| `spawn_table` | program에 `FORK`가 있을 때만 | 자식 task 목록(7.8절) |
| `fork_cap` | spawn table과 함께 | 동시에 살아 있을 수 있는 자식 수(1 이상) |

**`wake`** — 외부에서 박아 넣은 깨우기 사건입니다.

| field | 필수? | 뜻 |
|---|---|---|
| `t` | 필수 | 깨우는 시각(µs) |
| `op` | 필수 | 문자열 `"wake"` |
| `target` | 필수 | 깨울 task의 id |
| `channel` | 필수 | 어느 channel로 깨우는가. task는 그 channel의 `WAIT`에서 깨어남 |

예를 들어 `c1-dev`의 첫 wake event는 `{"channel":"timer:editor","op":"wake","t":2670,"target":"editor"}`입니다. 2,670 µs에 편집기를 timer channel로 깨운다는 뜻입니다.

**정렬 규칙.** compiler는 event를 `(t, op, id 또는 target)`으로 정렬합니다(`compile_timeline`의 `events.sort`). 같은 시각이면 `"arrive"`가 `"wake"`보다 알파벳 순서로 앞이므로 도착이 먼저 오고, 그다음 id 순입니다. schema는 정렬을 표현할 수 없으므로, "sorted by `t`"는 canonical lint가 검사합니다(13.2절).

**`id`와 `declared_class`.** 2026-10-14까지 interpretation contract §4는 arrive event를 `{t, op: arrive, name, program, depart?}`로 적어 둘이 빠져 있었습니다. 2026-10-16부터 contract도 schema, compiler, `docs/data-contracts.md` §4처럼 둘을 필수로 적습니다(`{t, op: arrive, id, name, declared_class, program, depart?, spawn_table?, fork_cap?}`).

## 7.6 program과 명령어

task의 `program`은 명령어 목록입니다. contract §3이 정한 여섯 primitive에 VM 내부 제어문 `LOOP` 하나가 더해집니다. schema의 `instruction` 정의를 표로 옮깁니다.

| 명령어 | 모양 | 뜻 |
|---|---|---|
| `RUN` | `{op: RUN, us}` | CPU를 `us` µs 씁니다. 벽시계 시간이 아니라 CPU 수요입니다. 중간에 preemption될 수 있습니다. |
| `SLEEP` | `{op: SLEEP, us}` | 스스로 `us` µs 동안 실행 불가능 상태가 됩니다(상대 시간). |
| `TIMER` | `{op: TIMER, period_us}` | 절대 시각 격자 t₀ + k·period에서 깨어납니다. 앞 반복이 늦게 끝나도 격자가 밀리지 않습니다(drift-free). |
| `WAIT` | `{op: WAIT, channel}` | 그 channel로 `WAKE` 명령어나 외부 `wake` event가 올 때까지 block합니다. |
| `WAKE` | `{op: WAKE, target}` | `target` task를 실행 가능 상태로 만듭니다. |
| `FORK` | `{op: FORK}` | spawn table의 다음 자식을 태어나게 합니다. 자식 수가 `fork_cap`에 차 있으면 자리가 날 때까지 block합니다. |
| `EXIT` | `{op: EXIT}` | 이 task를 끝냅니다. |
| `LOOP` | `{op: LOOP, count, body}` | `body`를 반복합니다. `count`는 1 이상의 정수 또는 `"unbounded"`. |

contract는 primitive를 여섯 개라고 셉니다(`FORK`와 `EXIT`를 한 줄로). schema는 `LOOP`를 이렇게 설명합니다. "VM-internal control flow, not a seventh primitive — the DES core never sees it. `count: 'unbounded'` repeats until the task's pinned depart (segment-bound tasks only); its body carries per-task-sampled constants." simulator의 사건 엔진은 LOOP를 보지 않고, task별 해석기가 LOOP를 풀어서 primitive만 엔진에 넘긴다는 뜻입니다.

`DES core` — discrete-event simulation의 중심부, 사건 대기열을 시각 순으로 처리하는 엔진입니다. `VM` — 여기서는 task 하나의 program을 한 명령어씩 실행하는 simulator 안의 작은 해석기입니다.

**지금 compiler가 실제로 내보내는 것.** tree의 core set을 compile하면 위 명령어가 모두 나오지만 쓰임새가 정해져 있습니다. 코드를 읽어 정리하면 이렇습니다.

- `RUN`과 `WAIT`는 거의 모든 task에 나옵니다.
- `SLEEP`은 batch job(측정된 run 사이의 block)과 DKMS 빌드의 꼬리에서만 나옵니다.
- `TIMER`는 주기가 선언된 task에서만 나옵니다. 영상·음악 재생기와 영상 통화(periodic entry, 11.5절), 게임 chain의 머리입니다. tree의 core set에서 TIMER를 가진 task는 23개입니다(이 권을 쓰며 51개 artifact를 모두 읽어 셌습니다). 8개는 chain 머리로 LOOP 안에 있고, 15개는 재생기와 통화로 펼쳐진 목록의 첫 명령어입니다. 재생기와 통화의 목록은 TIMER로 끝납니다. 박힌 퇴장 시각이나 그 뒤에 떨어지는 다음 tick의 TIMER를 마지막에 붙이기 때문입니다(11.5절).
- `WAKE`는 게임 chain(구성원이 다음 구성원을 깨움)과 빌드의 object job(구성원끼리 깨움)에서만 나옵니다.
- `FORK`는 빌드 orchestrator(`make`, `dkms`)에서만, `EXIT`는 finite task와 spawn table의 자식에서만 나옵니다. 박힌 퇴장이 있는 segment-bound task의 program은 EXIT 없이 막힌 채로 끝납니다. 마지막 명령어가 `WAIT`, `TIMER`, unbounded `LOOP` 중 하나이고, 퇴장이 그 task를 지웁니다(9.23 D16, 2026-10-15).
- `LOOP`는 게임 chain의 구성원에서만 나오고, 항상 `count: "unbounded"`입니다. 정수 `count`를 가진 LOOP는 schema상 합법이지만 지금 compiler의 어느 경로도 내보내지 않습니다.

> **왜 이렇게 정했나.** "TIMER는 주기가 선언된 task에만"이라는 규칙은 9.5 D74(2026-09-26)입니다. 그 전에는 측정된 앱의 모든 timer 깨어남을 `TIMER` 명령어로 compile했는데, 그 주기는 "다음 깨어남까지의 간격"이라서 1 µs짜리 주기까지 생겼습니다. 그런데 소비자 셋(contract §3, EDF 알고리즘의 deadline class, harness의 `job` 지표)은 모두 `TIMER`를 "마감이 있는 주기적 job"으로 읽었습니다. 그래서 D74는 측정된 timer 깨어남을 "a `WAIT` on a per-task timer channel woken by an exogenous wake event at its measured absolute time; it carries no deadline"으로 바꾸었습니다. 마감이 없는 깨어남을 마감이 있는 명령어로 적지 않게 된 것입니다. 이때 compile된 TIMER 단계 약 160만 개가 사라졌다고 기록되어 있습니다.

**TIMER의 늦은 tick 처리.** TIMER의 격자에서 task가 늦게 도착하면(앞 frame이 오래 걸려 다음 TIMER에 늦게 닿으면) 무슨 일이 일어날까요. 규칙은 **skip 규칙**입니다. 늦게 TIMER에 닿으면 지금 시각 이전의 마지막 tick m을 즉시 소비해 그 frame을 실행하고(마감은 tick m + 1), m보다 앞의 소비되지 않은 tick들은 일 없이 건너뛰며 각각을 마감을 놓친 job으로 셉니다. 2026-10-07에 인지오가 9.11 D3으로 정했고, `docs/memos/2026-10-07-timer-skip-rule-for-the-simulator.md`가 규칙(§1), 60 fps 격자의 예시(§2), 근거(§4)를 적습니다. 그 전의 규칙은 backlog였습니다. 밀린 tick을 하나씩 다 실행하는 것입니다. D3은 근거로 interbench, ROS 2 executor, Lipari와 Palopoli의 주기 thread, rt-app의 기본 모드, 그리고 TIMER task가 대표하는 프로그램들(mpv는 늦은 영상 frame을 버림, GStreamer video sink는 5 ms 넘게 늦은 frame을 버림)을 듭니다. 2026-10-08의 정정(9.11 D17, memo 끝의 정정 절)은 memo의 "none replays them"이라는 문장을 고쳐, 출처들이 공유하는 것은 "by default each skips"이고 늦은 job이 어느 tick의 것인지는 출처마다 다르며, memo의 선택(지나간 마지막 tick을 즉시 실행)은 video playback에서는 GStreamer sink의 것이고 audio와 게임 TIMER task에 대해서는 design이라고 적습니다.

이 규칙은 simulator의 해석 규칙이지 파일의 모양이 아닙니다. canonical 파일의 `TIMER` 명령어는 규칙이 바뀌기 전과 후에 똑같습니다. harness의 `job` 지표는 이 규칙으로 읽습니다(`docs/harness/metrics.md` §6.2). reference simulator의 TIMER(`simulator/src/sim.cpp`)는 2026-10-23부터 이 규칙으로 돕니다. 인경민의 stage Y이고, 그 전의 step K("TIMER+backlog")를 대신합니다. 2026-10-17의 final memo(`docs/memos/2026-10-17-workload-dataset-rebuild.md` §6.2)가 RQ0 gate spec의 simulator 적합성 항목 (b)로 부탁한 것입니다(16.2절의 4). contract의 TIMER 행은 2026-10-30에 이 규칙으로 고쳐졌고, schema의 TIMER 설명 문장은 아직 backlog를 말합니다(16.1절).

`EDF` — Earliest Deadline First, 마감이 가장 이른 job부터 CPU를 주는 scheduling 알고리즘입니다. 이 연구의 scheduler가 고를 수 있는 넷 중 하나입니다. `job`(harness 지표) — 주기적 task의 한 주기 분량의 일입니다. harness는 job마다 마감을 지켰는지 셉니다.

## 7.7 channel의 이름

`WAIT`와 `wake`가 쓰는 channel은 그냥 문자열입니다. simulator에게 channel은 우편함 이름일 뿐입니다. 하지만 compiler는 일정한 규칙으로 이름을 짓고, harness는 접두어로 종류를 읽습니다(`docs/harness/metrics.md` §6.1, channel 종류 `input`, `timer`, `chain`, `job`, `children`).

| channel | 누가 만드나 | 누가 깨우나 | 예 |
|---|---|---|---|
| `timer:<task id>` | 측정된 archetype의 timer component, heavy event, launch phase | 외부 `wake` event(박힌 시각) | `timer:editor` |
| `input:<task id>` | 재생한 키 입력 | 외부 `wake` event(박힌 시각) | `input:writer` |
| `chain:<member id>` | 게임 chain의 구성원 | 앞 구성원의 `WAKE` 명령어 | `chain:game.wineserver` |
| `job:<job member id>` | 빌드 object job의 구성원 | 같은 job의 다른 구성원의 `WAKE` | `job:build.j1.gcc` |
| `children:<task id>` | 빌드 orchestrator가 모든 자식을 낳은 뒤 | 파일 안에는 깨우는 것이 없음. 자식이 모두 끝났을 때 executor가 완료(제안된 규칙, 아래) | `children:build` |

`timer:`와 `input:`을 나눈 것은 9.5 D74의 hand-off입니다. "the harness tells an input wake from a timer wake by channel". harness는 키 입력에 대한 반응 시간을 `input:` channel의 wake event, 곧 키 입력 하나하나에서부터 잽니다(`input_latency`: 키가 온 순간부터 그 키가 끝낸 WAIT의 처리가 시작될 때까지). 사용자가 느끼는 지연은 키를 누른 뒤의 지연이기 때문입니다.

tree에서 세면 core set 51개 파일의 wake event는 모두 4,502,685개입니다(이 권을 쓰며 `"op":"wake"`를 세었습니다). 키 입력 channel은 그중 작은 부분입니다. 편집기 하나만 보아도 `c1-dev`에서 timer wake가 6,456개, 키 입력이 186개입니다. "편집기 program = 키 입력 기다림과 CPU 사용의 반복"이라는 README와 data-contracts의 그림은 단순화이고, 실제 측정된 편집기는 사용자가 없어도 자기 thread들의 timer로 훨씬 자주 깨어납니다.

> **열린 자리.** `children:<id>` channel을 깨우는 사건은 canonical 파일에 없습니다. 이 channel의 뜻은 2026-10-16에 인지오가 정했습니다. executor는 orchestrator의 `WAIT children:<id>`를 그 orchestrator가 낳은 자식이 모두 끝났을 때 완료하고, WAIT에 닿았을 때 살아 있는 자식이 없으면 막지 않고 곧바로 완료합니다(대기 0의 `ready` 줄). 데이터는 바뀌지 않습니다. 이 규칙은 interpretation contract의 §3 `WAIT(channel)` 행과 §5 FORK 문단, `docs/data-contracts.md` §4 예제 B와 §14의 2026-10-16 기록에 "proposed"로 적혔습니다. 동결된 계약의 변경이라 simulator 담당 인경민의 동의가 필요했고(`docs/data-contracts.md` §13의 동결 규칙), 인경민이 구두로 동의해 효력을 가졌습니다(2026-10-31 기록, `docs/data-contracts.md` §14). 지금의 reference simulator는 이 channel을 보통 channel로 다루어(`simulator/src/sim.cpp`의 `on_task_end`는 fork 자리만 돌려줍니다), 자식이 다 끝나도 orchestrator가 막힌 채로 남습니다. 그래서 `c1-compile`의 build turnaround를 재려면 이 구현이 먼저 있어야 하고, RQ0 gate spec은 이것을 simulator 적합성 항목 (g)로 적습니다(`harness/experiments/rq0-gate.yaml`의 `simulator-conformance`).

## 7.8 spawn table과 `fork_cap`

`make` 같은 orchestrator는 자식 process를 낳습니다. 1.2절의 원칙에 따라 "어떤 자식이 무엇을 하는가"는 compile 때 정하고 "언제 태어나는가"는 run 때 정합니다. 그래서 orchestrator의 arrive event는 **spawn table**, 즉 미리 다 쓴 자식 목록을 들고 옵니다.

```json
{"id": "build", "name": "make", "t": 2000000, "fork_cap": 48,
 "program": [{"op":"RUN","us":229}, {"op":"FORK"}, {"op":"FORK"}, {"op":"FORK"}, {"op":"FORK"}, {"op":"FORK"}, {"op":"FORK"},
             {"op":"RUN","us":1564}, {"op":"FORK"}, …, {"op":"WAIT","channel":"children:build"}, {"op":"EXIT"}],
 "spawn_table": [
   {"id":"build.j1.sh", "name":"sh", "declared_class":"normal", "program":[{"op":"RUN","us":848}, {"op":"WAKE","target":"build.j1.gcc"}, …]},
   {"id":"build.j1.gcc", "name":"gcc", …},
   {"id":"build.j1.cc1", "name":"cc1", "declared_class":"normal",
    "program":[{"op":"WAIT","channel":"job:build.j1.cc1"}, {"op":"RUN","us":476877}, {"op":"WAKE","target":"build.j1.gcc"}, {"op":"WAIT","channel":"job:build.j1.cc1"}, {"op":"EXIT"}]},
   …
 ]}
```

이것은 tree의 `c1-compile` artifact에서 읽은 것입니다. spawn table의 항목(`spawn_entry`)은 `id`, `name`, `declared_class`, `program` 넷이 필수입니다. `t`도 `depart`도 없습니다. 태어나는 시각은 run time에 정해지기 때문입니다. `FORK` 하나가 table의 다음 항목 하나를 순서대로 소비합니다.

`c1-compile`에서 숫자를 맞춰 보면 이렇습니다. object job이 2,908개이고 job마다 자식이 6개이므로 spawn table은 2,908 × 6 = 17,448칸입니다. `make`의 program은 job마다 dispatch RUN 하나와 FORK 여섯 개(7 명령어)이고, 끝에 `WAIT children:build`와 `EXIT`가 붙으므로 2,908 × 7 + 2 = 20,358 명령어입니다. 둘 다 tree의 artifact와 일치합니다.

**`fork_cap`은 48입니다.** timeline은 `parallelism_cap: 8`(`make -j8`)을 묶었는데 canonical 파일의 `fork_cap`은 48입니다. job 하나가 자식 여섯 개라서 job 8개가 동시에 돌려면 자식 48개가 동시에 살아 있어야 하기 때문입니다. 9.6 D19(2026-09-19)가 정한 규칙입니다. "emitted `fork_cap` = `parallelism_cap` × 6". schema의 `fork_cap` 설명도 2026-10-16부터 "e.g. 48 for -j8"이라는 이 값을 예로 듭니다.

> **왜 이렇게 정했나.** object job을 자식 여섯 개로 펼치는 형식은 9.6 D19입니다(`_dev/research/jioh/task-9.6-compile/changelog.md`). 기록된 이유는 형식의 제약입니다. "the workload format lets only a top-level task create tasks", 즉 spawn table의 자식은 다시 자식을 낳을 수 없습니다. 그래서 실제로는 `make` → `sh` → `gcc` → `cc1`처럼 이어지는 process tree를 한 층으로 펴고, 구성원들이 WAIT/WAKE channel로 부모-자식 순서(`sh` → `gcc` → `cc1` → `gcc` → `as` → `gcc` → `sh` → `fixdep` → `sh` → `rm` → `sh`)를 흉내 냅니다. 일을 마친 구성원은 CPU를 쓰지 않고 `sh`가 job을 끝낼 때까지 기다리므로, `fork_cap`이 make의 jobserver처럼 동시에 도는 job 수를 제한합니다. 이 방식으로 정확한 것과 정확하지 않은 것도 함께 기록되어 있습니다. 구성원의 순서, CPU, wake마다의 run, 동시 job 수, 빌드 전체의 turnaround는 정확합니다. 구성원 하나하나의 도착과 끝 시각은 job의 것이 됩니다.

## 7.9 모든 시간은 정수 microsecond

schema의 `time_us` 정의는 "Virtual time / duration in integer microseconds (contract §1)", 0 이상의 정수입니다. `t`, `depart`, `t_start`, `t_end`, `RUN.us`, `SLEEP.us`가 모두 이것입니다. `TIMER.period_us`는 1 이상의 정수입니다. 실수는 어디에도 없습니다. 2.3절에서 본 것처럼 timeline의 사람용 시간은 `parse_us`가 반올림해 정수로 만들고, 분포에서 뽑은 값은 sampling 함수가 반올림해 정수로 만듭니다(10.3절).

## 7.10 schema가 말하지 못하는 것

schema는 `additionalProperties: false`를 모든 object에 걸어 오타 하나도 허용하지 않습니다. 하지만 JSON Schema로는 표현할 수 없는 규칙들이 있고, schema의 머리 설명이 그것을 직접 나열합니다. "Ordering of `events` by `t`, uniqueness of task ids, FORK⇔spawn_table consistency, and channel/target resolution are linter invariants, not expressible here." 이 규칙들은 compile 안의 canonical lint가 검사합니다(13장).

`program` 정의의 설명은 "A task whose program runs out without EXIT and without a pinned depart is a linter error"라고 적습니다. 2026-10-15부터 `wlc/linter.py`의 `lint_canonical`이 이것을 검사합니다(9.23 D14). 검사는 설명보다 한 걸음 더 갑니다. 박힌 퇴장이 없는 task(top-level이든 spawn table의 자식이든)는 `EXIT`로 끝나야 하고, 박힌 퇴장이 있는 segment-bound task는 `WAIT`, `TIMER`, unbounded `LOOP` 중 하나로 끝나야 합니다. segment-bound program도 퇴장 전에 할 일이 바닥나지 않고 막힌 채로 퇴장을 맞게 하는 9.23 D16의 규칙입니다(11.1절, 11.5절). 그래서 schema의 `program` 문장은 이제 lint가 지킵니다(13.2절).

---

# 8장 · 누가 어느 key를 읽나

canonical 파일 하나에는 정답과 문제가 함께 들어 있습니다. 이 장은 "그런데 어떻게 정답이 새지 않는가"라는 질문에 답합니다. 답은 파일을 나누는 것이 아니라 **읽는 쪽이 자기 몫만 꺼내고 나머지를 버리는 것**입니다. 이 설계를 이해하면 왜 `focus`는 canonical 파일에 있어도 되고 `ground_truth`는 recognizer에게 절대 가면 안 되는지가 분명해집니다.

## 8.1 information asymmetry

`information asymmetry` — 실험의 각 부품이 알아도 되는 정보가 서로 다르게 정해져 있다는 설계 원칙입니다. recognizer는 실제 기계에서 볼 수 있는 것만, simulator는 실행에 필요한 것만, 채점자는 정답을 봅니다.

`docs/data-contracts.md` §1이 이 원칙을 이렇게 적습니다. dataset tree는 raw canonical 파일만 내보내고 소비자에 대해 아무것도 모릅니다. 각 소비자의 **loader**가 자기에게 허락된 **view**를 꺼내고 나머지를 parse 경계에서 버립니다. "The information asymmetry is enforced by each loader discarding what its program may not see — structurally, at the boundary, so nothing downstream could branch on it even by accident." 버린 정보는 그 뒤의 코드에 아예 존재하지 않으므로, 실수로라도 그것에 따라 분기할 수 없다는 뜻입니다.

웹 개발의 비유로는 API 응답의 DTO가 가깝습니다. database row에는 password hash가 있어도, 응답용 DTO로 옮기는 순간 그 field를 빼 버리면 front-end 코드는 실수로도 그것을 쓸 수 없습니다. 여기서는 canonical 파일이 database row이고, run file과 visible projection이 DTO입니다.

## 8.2 세 독자와 그 view

**simulator — run file.** simulator의 loader는 `events`만 남기고, `meta`는 id 하나로 줄입니다. data-contracts §4의 "The two derived views"가 모양을 정합니다.

```jsonc
{ "workload_id": "c2-p1a",
  "events": [ /* arrive와 wake event 전부 */ ] }
```

`ground_truth`도 `focus`도 없습니다. scheduler는 정답을 알면 안 되고, focus로 할 일도 없기 때문입니다. 9.17 D2는 실제 simulator 코드를 확인하고 "the simulator reads `meta.id` and `events`; `simulator/src/sim.cpp` names no other key"라고 기록합니다. 모든 task 기록의 `declared_class`는 `events` 안에 있으므로 simulator에게 그대로 갑니다(3.7절의 idle 규칙을 적용하려면 필요합니다).

> **왜 이렇게 정했나.** run file이 `meta`에서 id만 남기는 것은 2026-09-06 protocol freeze에서 정한 것입니다(data-contracts §14). "Recorded choice for 3a: the run file keeps only `workload_id` of `meta`; a trace is tied to a build through the manifest and the simulator version in its header, not through the run file." simulator가 남기는 실행 기록(trace)이 어느 build에서 나왔는지는 run file이 아니라 manifest와 trace 머리의 simulator 버전으로 묶는다는 뜻입니다.

**daemon과 recognizer — visible projection.** daemon의 loader는 recognizer가 볼 자격이 있는 것만 꺼냅니다. data-contracts §4가 정한 내용은 이렇습니다. task마다 이름, `declared_class`, **박힌** 도착 시각(`t_arrive`), 박혀 있으면 퇴장 시각(`t_depart`), 그 task가 쥔 focus 구간들, 그리고 spawn table이 있으면 자식의 이름과 class별 개수입니다. program은 없습니다. RUN 길이도 없습니다. 정답 label도 없습니다.

```jsonc
{ "workload_id": "c1-compile",
  "tasks": [
    { "name": "code", "declared_class": "normal", "t_arrive": 0, "t_depart": 1594000000,
      "focus": [ { "t_start": 0, "t_end": 1594000000 } ] },
    { "name": "make", "declared_class": "normal", "t_arrive": 2000000,
      "children": [ { "name": "as", "declared_class": "normal", "count": 2908 },
                    { "name": "cc1", "declared_class": "normal", "count": 2908 }, … ] }
  ] }
```

이것은 contract의 규칙을 tree의 `c1-compile`에 적용한 모양입니다. 자식은 job마다 여섯 이름(`sh`, `gcc`, `cc1`, `as`, `fixdep`, `rm`)이므로 각 이름이 2,908개씩 셉니다. data-contracts §4의 예제도 2026-10-16부터 이 build의 여섯 자식 이름을 2,908개씩 보여 줍니다. `make`에는 `t_depart`가 없습니다. finite task라서 끝나는 시각이 run time의 결과이고, projection이 그것을 알 수 없습니다.

projection의 규칙 몇 가지가 recognizer가 보는 세계를 정합니다.

- **task instance 하나에 항목 하나, 접지 않음.** "one entry per canonical task instance, never folded"(2026-09-06 protocol freeze). 같은 이름 다섯 개는 다섯 항목이고, telemetry를 만들 때 `chrome × 5`로 셉니다.
- **자식은 개수로만.** spawn table의 자식은 박힌 시각이 없으므로 이름과 class별 개수로 접어 부모에 붙입니다. 자식들은 부모가 도착하는 순간 telemetry에 함께 나타납니다.
- **class를 보여 줌.** 9.13의 결정 3, "on the standing that a real machine exposes a process's class as it exposes its name"(실제 기계에서 `sched_getattr`로 class를 읽을 수 있으므로).
- **focus를 보여 줌.** 9.17의 결정 3, task 항목에 그 task의 focus 구간을 붙입니다.

> **코드로.** 이 규칙의 참조 구현은 harness의 mock daemon입니다(`harness/tools/tests/mocks/daemon.py`의 `projection`). 각 `arrive` event에서 `name`, `declared_class`, `t`를 꺼내 `t_arrive`로 쓰고, `depart`가 있으면 `t_depart`로 쓰고, `focus` 목록에서 그 id의 구간을 모아 붙이고, spawn table이 있으면 `(name, declared_class)`로 세어 `children`을 만듭니다. `ground_truth`는 건드리지 않습니다.

**oracle과 채점자 — `ground_truth`.** 정답을 읽는 것은 둘뿐입니다. oracle recognizer 조건은 projection 대신 `ground_truth`를 읽어 정답 label을 냅니다. 이것이 "맞힐 수 있는 최선"의 기준선입니다. Layer 1 채점자(grader)는 recognizer의 답을 `ground_truth`와 비교해 정확도를 셉니다. `familiarity`도 채점자만 읽고, 정확도를 tier별로 나누는 열쇠로 씁니다(schema, "A reporting split key for the grader, never a recognizer input").

`Layer 1` — 이 연구가 결과를 나누는 두 층 중 첫째, "recognizer가 상황을 맞혔는가"입니다. `Layer 2`는 "그 결과 scheduling이 좋아졌는가"입니다. `grader` — Layer 1의 채점자입니다.

data-contracts §1은 이 설계를 이렇게 요약합니다. "The dotted lines are the deliberate cheat paths, and they are the experiment's core design: `ground_truth` reaches only the oracle recognizer and the grader. The simulator never sees it (the run file doesn't contain it); the LLM never sees it (the projection doesn't contain it)."

## 8.3 key별로 다시 정리

| canonical key | simulator(run file) | recognizer(projection) | oracle | 채점자·harness |
|---|---|---|---|---|
| `meta.id` | 읽음(`workload_id`) | 읽음(`workload_id`) | — | 읽음 |
| `meta.derived_from`, `meta.sampled` | 버림 | 버림 | — | 추적용 |
| `ground_truth` | 버림 | 버림 | **읽음** | **읽음** |
| `focus` | 버림 | 읽음(task별 구간) | — | — |
| `events`의 arrive: `name`, `declared_class`, `t`, `depart` | 읽음 | 읽음 | — | trace를 통해 |
| `events`의 arrive: `program`, `spawn_table`의 program | 읽음 | 버림(자식은 이름·class·개수만) | — | — |
| `events`의 wake | 읽음 | 버림 | — | — |

이 표에서 놓치기 쉬운 줄이 둘 있습니다.

첫째, recognizer는 **wake event를 보지 못합니다.** 키 입력이 언제 몇 번 떨어지는지는 사용자의 행동이지만, 실제 기계에서 다른 프로그램이 그것을 엿볼 수는 없습니다. 그래서 projection에 없습니다. recognizer가 사용자의 행동에 대해 아는 것은 focus 하나뿐입니다.

둘째, recognizer는 **program을 보지 못합니다.** CPU를 얼마나 쓰는지, 얼마나 자주 깨어나는지는 이 실험이 "이름만 보고도 상황을 알 수 있는가"를 묻기 위해 일부러 감춘 정보입니다. data-contracts §5는 telemetry에서 빠진 것들을 나열하며 "no CPU or burst statistics (that is the hidden behavioral ground truth being tested against)"라고 적습니다.

## 8.4 무엇이 정답 쪽이고 무엇이 관측 쪽인가

canonical 파일의 key를 정답 쪽과 관측 쪽으로 나누면 이 dataset의 설계가 한눈에 보입니다.

- **정답 쪽**: `ground_truth`(mode, `background_wanted`, 그 밖의 설명 attribute, `familiarity`). 사람만 압니다.
- **관측 쪽**: process 이름과 개수, class, 박힌 도착·퇴장 시각, focus. 실제 기계에서 `/proc`, `sched_getattr`, 창 관리자로 볼 수 있는 것들입니다.
- **물리 쪽**: program, wake event. 기계가 겪는 일입니다. scheduler에게만 갑니다.

timeline 저자가 새 field를 넣을 때 가장 먼저 물어야 할 질문은 "이것은 셋 중 어느 쪽인가"입니다. `focus`가 9.17에서 들어올 때 결정 3이 정확히 이 질문에 답했습니다. 관측 쪽이므로 `ground_truth`가 아니라 새 top-level key로, run file이 아니라 projection으로 갑니다.

---

# 9장 · Compiler의 큰 흐름

여기서부터 compiler **wlc**의 안으로 들어갑니다. 이 장은 지도입니다. 어떤 파일이 무슨 일을 하는지, `make dataset`을 치면 어떤 함수가 어떤 순서로 불리는지를 봅니다. 10–13장이 각 단계를 자세히 다룹니다.

## 9.1 모듈 지도

compiler의 library는 `dataset/tools/wlc/` 디렉터리이고, 그것을 부르는 명령줄 도구(CLI)는 `dataset/tools/`에 있습니다. tree에서 센 줄 수(2026-10-17)와 함께 적습니다.

| 파일 | 줄 | 하는 일 |
|---|---|---|
| `wlc/__init__.py` | 12 | 바깥에 내보내는 이름들: `parse_us`, `Library`, `Timeline`, `TimelineError`, `compile_timeline`, `per_segment` |
| `wlc/units.py` | 29 | 사람용 시간 문자열 → 정수 µs(2.3절) |
| `wlc/library.py` | 59 | `archetypes.yaml` 읽기, git blob hash, entry 조회(`binding_params`, `lifetime`, `is_measured`, `operations`, `has_input_channel`) |
| `wlc/timeline.py` | 252 | timeline 읽기와 구조 검사(2–4장) |
| `wlc/sampling.py` | 189 | seed와 열쇠로 하는 결정적 추출, 분포별 표본(10장) |
| `wlc/compiler.py` | 758 | timeline + library → canonical dict + compile report(11장) |
| `wlc/estimate.py` | 35 | segment별 CPU 수요 기록(12장) |
| `wlc/linter.py` | 491 | repo lint, 묶인 값의 source lint, 측정 release 지도의 lint, canonical lint(13–14장) |
| `wlc/deriver.py` | 148 | variant recipe 실행(5장) |
| `wlc/grid.py` | 191 | coverage grid, mode 메뉴(`MODES`), 이름 tier 표 |
| `wlc/variants.py` | 257 | RQ0 gate spec의 민감도 variant 변환 |
| `compile.py` | 191 | CLI: 모든 timeline compile, artifact·report·manifest 쓰기 |
| `derive.py` | 65 | CLI: recipe 실행, coverage grid |
| `lint.py` | 65 | CLI: compile 전 lint |

`wlc/__init__.py`의 docstring은 compiler의 계약을 셋으로 적습니다. 의미는 interpretation contract, 포맷과 도구의 결정은 task 2.3 spec, 출력 모양은 workload schema입니다. `dataset/README.md`의 "Rules of the tree"는 여기에 우선순위를 덧붙입니다. "The docs define meaning. When code and a doc disagree, the latest recorded decision on the matter decides: a doc that missed a decision is corrected to it, and code that departs from the doc without one is fixed." 의미는 문서가 정하고, 코드와 문서가 어긋나면 그 일에 대한 가장 최근의 결정 기록이 정한다는 뜻입니다. 동결된 계약은 `docs/data-contracts.md` §13의 동결 규칙(세 사람의 동의와 §14 기록)으로만 바뀝니다.

## 9.2 `make dataset`에서 일어나는 일

`make dataset`은 `derive.py`를 먼저 돌리고(5.7절), 그다음 `compile.py`를 돌립니다. `compile.py`의 흐름을 함수 단위로 따라가면 이렇습니다.

```
main()
 └─ build_all(root, jobs)
     ├─ discover(timelines_dir)          # dataset/timelines/**/*.timeline.yaml, 이름 순
     ├─ jobs = min(--jobs 또는 CPU 수, 파일 수)
     ├─ ProcessPoolExecutor로 compile_one(root, path)를 파일마다 (jobs == 1이면 순서대로)
     │   ├─ _tools(root)                 # library와 schema를 worker process마다 한 번 읽음
     │   ├─ Timeline(path, library)      # 구조 검사. 실패하면 오류 문자열 반환
     │   └─ for mode in MODES ("single",):
     │       ├─ compile_timeline(timeline, library, mode, rel_path)
     │       ├─ lint_canonical(canonical, schema, …)     # 13장
     │       └─ (artifact 경로, canonical 바이트, demand 기록, report, id, mode)
     ├─ 결과를 모아 manifest dict를 만듦  # inputs, artifacts, demand, reports
     └─ 반환
 ├─ 파일마다 "  <id>[single]: demand 0.03 (calibration)"를 출력
 ├─ 오류가 하나라도 있으면: 오류를 출력하고 종료 코드 1. 아무것도 쓰지 않음
 ├─ --check이면: manifest 바이트를 commit된 것과 비교만
 └─ 아니면: build/에 artifact와 report를 쓰고, build.manifest.json을 씀
```

세 가지를 짚어 둡니다.

**전부 아니면 전무.** 51개 중 하나라도 loader 검사나 canonical lint에 걸리면 `compile.py`는 아무 파일도 쓰지 않고 실패합니다. 반쯤 갱신된 `build/` 디렉터리가 생기지 않습니다.

**artifact가 놓이는 곳.** `artifact_set` 함수는 timeline이 `dataset/timelines/` 아래 어느 디렉터리에 있는지 봅니다. `coreset/`에 있으면 set 이름이 `coreset`이고, 출력 경로는 `<set>-<mode>/<id>.workload.json`, 즉 `coreset-single/c1-office.workload.json`입니다. `dataset/timelines/` 바로 아래에 둔 파일은 `adhoc` set이 됩니다. `-single`이라는 꼬리는 compile mode의 이름입니다. mode는 지금 `single` 하나뿐이고(9.3절), 꼬리는 역사적인 이름으로 남았습니다.

**demand의 출력과 기록.** `compile.py`는 파일마다 utilization을 소수 둘째 자리로 출력하고, manifest의 `demand` 기록에는 소수 넷째 자리로 반올림해 적습니다(`round(…, 4)`). compile report에는 반올림하지 않은 값이 있습니다. 6.1절에서 `c1-office`의 report가 0.026957333…이고 manifest가 0.027인 이유입니다.

`artifact` — compile의 산출물 파일, 여기서는 `<id>.workload.json`입니다. `compile report` — artifact 옆에 놓이는 `<id>.report.json`, 그 파일의 CPU 수요 계산과 operation 길이 기록입니다(12.5절). `manifest` — artifact와 report와 입력 파일의 hash를 모아 둔 lockfile, `dataset/build.manifest.json`입니다(13.5절).

## 9.3 compile mode는 `single` 하나

`wlc/compiler.py`의 `MODES`는 `("single",)`입니다. `compile_timeline`은 다른 mode를 받으면 `ValueError("mode must be one of ('single',)")`로 거절합니다. `single`은 "lane scaling을 적용한 mode", 즉 CPU 하나짜리 simulator에 맞게 일부 값을 줄인 mode입니다(11.9절). 2026-10-09 전에는 측정값 그대로의 `native` mode도 있었고, 같은 timeline 하나가 artifact 두 개(`coreset-single`, `coreset-native`)가 되었습니다. 그 역사는 15장에서 다룹니다.

## 9.4 `compile_timeline`: timeline 하나가 dict 하나가 되기까지

`compile_timeline(timeline, library, mode, rel_path)`가 compiler의 심장입니다. 단계는 다섯입니다.

**1단계, instance로 펼치기.** timeline의 task를 순서대로 돌며, `count`가 1이면 instance id를 task id 그대로, 아니면 `<id>.1`부터 `<id>.N`까지 만듭니다. instance마다 `_compile_instance`를 불러 `_TaskBuild` 객체의 목록을 받습니다. 보통은 한 개이고, 게임 chain은 열일곱 개입니다. 외부 wake event는 이 과정에서 공용 목록 `wakes`에 `(t, target, channel)`로 쌓입니다.

**2단계, focus의 주인 찾기.** task마다 "focus가 이 task를 가리킬 때 canonical 파일에서는 어느 id를 써야 하는가"를 기록합니다. task 이름과 같은 이름을 가진 첫 build, 없으면 첫 build입니다(`heads.setdefault(…)`). 보통 task 자신이고, chain이면 머리입니다.

**3단계, event 만들기와 정렬.** build마다 `_arrive_event`로 arrive event를 만듭니다. `t`, `op`, `id`, `name`, `declared_class`, `program`을 넣고, `depart`가 있으면 넣고, spawn table이 있으면 `spawn_table`과 `fork_cap`을 넣습니다. `wakes` 목록의 항목마다 wake event를 만듭니다. 둘을 합쳐 `(t, op, id 또는 target)`으로 정렬합니다.

**4단계, canonical dict.** `meta`(id, `derived_from`, `sampled`), `ground_truth`(segment마다 `_ground_truth_segment`), `focus`(timeline의 focus 구간을 µs로, task는 2단계의 주인 id로), `events`를 모읍니다.

**5단계, compile report.** build마다 누적해 둔 CPU 수요(`demand_us`)를 모아 `duration_us`, `demand_us`, `utilization`, `per_task`, `per_segment`, `operations`, `demand_class`를 만듭니다(12장).

> **코드로.** `_TaskBuild`는 task 하나의 작업대입니다. `id`, `name`, `declared_class`, `program`(빈 목록에서 시작), `spawn_table`, `fork_cap`, `depart`, `replay`, `demand_us`(0에서 시작)를 가집니다. 각 전개 함수(11장)는 이 객체의 `program`에 명령어를 붙이면서 동시에 `demand_us`에 RUN의 µs를 더합니다. 그래서 compile이 끝나면 CPU 수요의 정확한 합계가 이미 계산되어 있습니다. 따로 program을 다시 훑을 필요가 없습니다.

## 9.5 `_compile_instance`: 어느 전개 경로로 갈까

instance 하나를 compile할 때, compiler는 archetype entry를 보고 전개 방식을 고릅니다. 판단 순서는 코드 그대로 이렇습니다.

1. `pattern.constructor`가 `chain`이면 → `_chain_constructor`(게임 chain).
2. 그 밖이면 `_TaskBuild`를 하나 만들고 `arrive`, `depart`를 넣은 뒤:
   1. `pattern.constructor`가 `module-build`이면 → `_module_build_unroll`(DKMS 모듈 빌드).
   2. 측정된 entry(`is_measured`: params에 `components`, `stimulus`, `focus_components`, `operations`, `cycle_run` 중 하나가 있음)이면 → `_measured_unroll`.
   3. program에 `FORK`가 있으면 → `_orchestrator_unroll`(빌드).
   4. `pattern.constructor`가 `batch-loop`이면 → `_batch_loop`.
   5. 그 밖이면 거절합니다. `ValueError("<iid>: archetype '<id>' matches no compile path — …")`로 build가 실패합니다.

tree의 library 29개 entry가 각각 어느 경로로 가는지 이 권을 쓰며 코드의 판단을 그대로 돌려 확인했습니다.

| 경로 | archetype |
|---|---|
| `_measured_unroll` | `office-writer`, `code-editor`, `mail-client`, `web-browser`, `image-editor`, `video-editor`, `renderer-hidden`, `chat-client`, `game-client`, `compositor-shell`, `audio-server`, `service-manager`, `message-bus` |
| `_measured_unroll`의 periodic 분기(`_periodic_unroll`) | `video-player`, `audio-player`, `video-call` |
| `_batch_loop` | `cpu-batch`, `file-archiver`, `game-download`, `game-download-idle`, `package-upgrade`, `file-indexer`, `video-transcoder`, `incremental-backup` |
| `_orchestrator_unroll` | `build-orchestrator` |
| `_module_build_unroll` | `module-build-orchestrator` |
| `_chain_constructor` | `game-task-chain` |
| (부모가 만듦) | `compiler-child`, `module-compiler-child` |

2026-10-16 전에는 경로가 셋 더 있었습니다. input channel이 있는 entry의 `_interactive_unroll`, finite entry의 `_finite_unroll`, 그 밖의 `_unbounded_loop`입니다. 재건 전 library의 문헌 기반 archetype(예: `desktop-interactive`, 입력 간격을 분포에서 뽑고 CPU를 "간격의 몇 분의 일"로 정하던 모형)을 위한 경로였습니다. 재건 뒤에는 compile되는 어떤 task도 이 셋에 닿지 않았습니다. `_interactive_unroll`에 닿지 않은 까닭은 재건으로 모든 대화형 entry가 측정된 entry가 되어 `_measured_unroll`이 먼저 받았기 때문입니다. `_finite_unroll`에 떨어질 finite entry는 없었습니다(finite entry는 모두 `batch-loop`, `module-build`이거나 `FORK`가 있는 빌드였습니다). `_unbounded_loop`에 떨어지는 entry는 lifetime이 `spawned`인 `compiler-child`와 `module-compiler-child` 둘이었지만, 둘 다 부모가 만드는 자식이어서 어느 timeline도 맨 위 task로 묶지 않습니다(위 표의 "(부모가 만듦)"; `git show 37c2e233^:dataset/tools/wlc/compiler.py`의 분기). 어디서도 불리지 않던 `_spawned_program`도 있었습니다. 인지오가 2026-10-16에 이 넷을 지우기로 정했고(9.15), 그 자리에 어느 경로에도 맞지 않는 entry를 거절하는 분기가 들어왔습니다. 경로를 지운 것만으로는 어느 artifact도 바뀌지 않았지만, `compiler.py`가 manifest의 `inputs`이므로 manifest를 다시 bless하고 RQ0 gate spec의 pin을 다시 걸었습니다(13.5절). 거절은 `dataset/tools/tests/test_canonical.py`의 `test_an_entry_matching_no_compile_path_is_refused`가 지킵니다.

---

# 10장 · Seed와 결정성

이 장은 이 권의 중심 질문, "같은 입력이면 왜 바이트 하나까지 같은 출력이 나오는가"에 답합니다. 답의 핵심은 무작위 추출을 **순서**가 아니라 **이름**으로 하는 것입니다. 이 한 가지 설계가 결정성과, 짝 파일의 "딱 이것만 다르다"를 동시에 보장합니다.

## 10.1 왜 결정성이 필요한가

`dataset/README.md`는 이렇게 적습니다. "Same timeline + same library + same seed ⇒ byte-identical output. That determinism is load-bearing (experiment hygiene), which is why `build/` isn't committed: CI recompiles and diffs hashes against the manifests instead." 이유가 셋 들어 있습니다.

첫째, **실험 조건들이 같은 workload를 상대해야 합니다.** oracle, LLM, 이름 대조표, 무작위 추측이라는 여러 recognizer 조건을 비교하려면, 모두 바이트 하나까지 같은 workload에서 돌아야 합니다. compile할 때마다 키 입력 시각이 달라지면 조건 사이의 차이가 recognizer 때문인지 주사위 때문인지 알 수 없습니다.

둘째, **build 산출물을 commit하지 않아도 됩니다.** core set만 해도 51개 파일이 678 MB입니다(tree에서 센 값). 이것을 git에 넣는 대신, 산출물의 hash만 manifest에 commit하고 CI가 다시 compile해서 hash를 비교합니다. 결정성이 없으면 이 방식이 불가능합니다.

셋째, **연구의 주장이 결정성에 기대고 있습니다.** 2026-09-20 dataset validity review memo(`docs/memos/2026-09-20-dataset-validity-review.md`)는 dataset이 "sound for the recognition claim"이라고 판정하면서, 그 이유를 "the recognizer reads identity, so the compile path's determinism carries the recognition claim"으로 적습니다. recognizer는 이름(정체)을 읽으므로, compile 경로가 결정적이라는 사실이 인식 실험의 주장을 받친다는 것입니다.

## 10.2 이름으로 뽑는 주사위: `uniform(seed, *key)`

모든 무작위 추출은 `dataset/tools/wlc/sampling.py`의 함수 하나에서 시작합니다.

```python
def uniform(seed, *key):
    material = "|".join([str(seed), *map(str, key)]).encode()
    digest = hashlib.sha256(material).digest()
    u = int.from_bytes(digest[:8], "big") / 2**64
    return min(max(u, _EPS), 1 - _EPS)
```

말로 풀면 이렇습니다. seed와 열쇠(key)들을 `|`로 이어 붙인 문자열을 만듭니다. 그 문자열의 SHA-256을 계산합니다. 앞 8 byte를 큰 정수로 읽어 2⁶⁴로 나눕니다. 그러면 0과 1 사이의 수가 나옵니다. 양 끝(정확히 0이나 1)은 2⁻⁵³만큼 안쪽으로 밀어 둡니다(뒤의 정규분포 역함수가 0과 1에서 무한대가 되기 때문입니다).

손으로 하나 계산해 보겠습니다. `c1-office`(seed 101)의 Writer 입력 창의 재생 위치를 정하는 추출은 `uniform(101, "writer", "stimulus", 0)`입니다. 재료 문자열은 `101|writer|stimulus|0`이고, 그 SHA-256의 앞 8 byte는 hex로 `6918dcb853ec7f7b`이며, 이것을 2⁶⁴로 나누면 0.4105356168765173입니다. 이 권을 쓰며 `python3.12`로 `hashlib`를 직접 불러 계산한 값과 `sampling.uniform`이 돌려준 값이 같았습니다. 이 수가 11.4절에서 Writer의 키 입력 위치를 정합니다.

중요한 것은 **같은 열쇠는 언제 어디서나 같은 수를 낸다**는 점입니다. 전역 난수 생성기처럼 "몇 번째로 뽑았는가"에 따라 값이 달라지지 않습니다. 웹 개발의 비유로는 content-addressed storage(내용의 hash가 곧 주소인 저장소)가 가깝습니다. 순서대로 번호를 매기는 auto-increment id는 앞에 하나가 끼면 뒤가 다 밀리지만, 내용 hash는 다른 항목의 존재와 무관합니다.

> **왜 이렇게 정했나.** task 2.3의 결정 5(2026-08-27)입니다. "Sampling uses keyed substreams derived from `(seed, task id, param, draw index)` — never one global draw sequence — so unrelated edits cannot shift another task's draws and C2 byte-identity holds by construction." `sampling.py`의 docstring이 같은 말에 한 문장을 더합니다. "All math is pure-Python and platform-deterministic." numpy 같은 외부 수치 library를 쓰지 않고 Python 표준 library(`hashlib`, `math`, `statistics.NormalDist`)만으로 계산해서, 기계가 달라도 같은 결과가 나오게 한다는 뜻입니다.

`keyed substream` — 열쇠마다 독립된 무작위 흐름입니다. 이 dataset에서는 `(seed, instance id, 이름표, 순번 …)`이 열쇠입니다.

## 10.3 분포에서 값 하나 뽑기: `sample`

`uniform`이 0과 1 사이의 수를 주면, `sample(param, seed, *key)`가 그것을 archetype의 분포에 맞는 값으로 바꿉니다. `sampling.py`가 지원하는 분포는 다섯 가지입니다.

| `dist` | parameter | 뽑는 방법 |
|---|---|---|
| `constant` | `value` 또는 `value_us` | 무작위 없이 그 값 |
| `uniform` | `min`, `max` | `min + u·(max − min)` |
| `lognormal` | `median_us`와 `sigma_log`, 또는 `anchor_min_us`와 `anchor_max_us` | 정규분포 역함수로 z를 구해 `median · e^(σ·z)`, 반올림, 최소 1 µs |
| `lognormal-mixture` | 멈춤 확률, 멈춤·흐름 각각의 평균과 σ | 먼저 어느 쪽인지 뽑고, 그쪽의 lognormal에서 |
| `quantiles` | 10개 percentile `p`, 선택적으로 `min`, `max`, 구간 평균 11개 `means` | 아래 설명 |

tree의 library에서 실제로 쓰이는 분포를 세면 `quantiles`가 292개(그중 `sampling: per-iteration` 225개, `per-instance` 67개), `constant`가 7개, `lognormal`이 1개(게임 chain의 `per_schedule_run`)입니다. `uniform`과 `lognormal-mixture`는 sampling 코드에 남아 있지만 지금 library에서 쓰지 않습니다.

**anchored lognormal.** 게임 chain의 `per_schedule_run`은 `anchor_min_us: 260`, `anchor_max_us: 1650`으로 적혀 있습니다. 출처(LAVD 발표 자료 13번 slide)가 "coordination task 260 µs, work task 1.65 ms"라는 두 예만 주기 때문에, 이 둘을 분포의 5번째와 95번째 percentile로 읽고 중앙값과 σ를 역산합니다(`anchored_lognormal_params`). 중앙값은 √(260 × 1650) ≈ 655.0 µs, σ는 ln(1650/655.0) ÷ 1.645 ≈ 0.562입니다(이 권을 쓰며 함수를 직접 불러 확인한 값입니다). 두 예를 p05/p95로 읽는 것과 lognormal을 쓰는 것은 modeling note에 "ours"로 적혀 있는 설계입니다.

**quantile table.** 측정된 값은 거의 모두 이 모양입니다. 예를 들어 `code-editor`의 `input_run`(키 하나당 CPU)은 이렇게 생겼습니다.

```yaml
input_run: {dist: quantiles,
  p: [12581, 13479, 15293, 55826, 79706, 108730, 179444, 230709, 550568, 1179716],
  min: 4494, max: 3040360,
  means: [9253.426, 12977.94, …, 1567494.516],
  sampling: per-iteration, source: "meas-ci:interactive:2026-09-25"}
```

`p`의 열 값은 1, 5, 10, 25, 50, 75, 90, 95, 99, 99.9번째 percentile(µs)입니다(`QUANTILE_PROBS`). `min`과 `max`는 표본의 최솟값과 최댓값입니다. `means` 열한 개는 `min`, 열 percentile, `max`가 만드는 열한 구간 각각의 실측 평균입니다. 뽑는 방법은 이렇습니다. `u`로 어느 구간에 떨어질지 고르고(예: u가 0.25와 0.50 사이면 넷째 구간), 그 구간 안의 위치 v를 0과 1 사이로 구한 뒤, `lo + (hi − lo)·v^a` 곡선 위의 값을 냅니다. 지수 `a`는 그 구간의 평균이 실측 평균과 같아지도록 정합니다. 그래서 percentile도 지키고 평균도 지킵니다. `min`, `max`, `means`가 없는 표는 percentile 사이를 직선으로 잇고 양 끝을 끝 값에 고정합니다.

> **왜 이렇게 정했나.** 측정값을 quantile table로 싣는 결정은 9.5 D17(2026-09-15)입니다. 기록된 이유는 측정 분포가 lognormal에 맞지 않는다는 것입니다. "the log-sigma implied by p90 and by p99 differ by 2–3× for VS Code's per-input run (0.41 vs 1.07), Thunderbird's (0.33 vs 0.92) … Writer's idle gap is bimodal (p50 102 ms, p90 600 ms)." p90으로 계산한 σ와 p99로 계산한 σ가 두세 배 차이 나고, 봉우리가 둘인 분포도 있어서, 하나의 lognormal로 요약하면 꼬리가 틀립니다. 구간 평균을 더한 것은 9.5 D71입니다("a table carries its `min`, `max` and interval `means`; draws keep the mean"). percentile만 맞추면 평균이 어긋날 수 있는데, CPU 수요는 평균이 좌우하기 때문입니다.

**0을 허용하는 표.** 보통 뽑은 값은 최소 1 µs로 올립니다. 그런데 batch job의 "run 뒤의 block" 표처럼 0이 실측값인 표가 있습니다(9.6 D25, "the block after a run is zero when the program ran on"). 이런 표는 `allow_zero=True`로 뽑아 0을 그대로 둡니다. 키 하나당 CPU(`input_run`)도 0을 허용합니다. 키가 task를 깨웠지만 CPU를 쓰지 않은 경우가 실제로 측정되었기 때문입니다(9.5 D48). 그런 키 입력은 canonical 파일에서 `WAIT`만 있고 뒤따르는 `RUN`이 없습니다.

## 10.4 열쇠를 어떻게 짓나

열쇠의 모양은 전개 경로마다 조금씩 다르지만, 원칙은 같습니다. **seed, instance id, 무엇을 뽑는지의 이름표, 몇 번째인지의 순번**입니다. compiler에서 읽은 대표적인 열쇠들입니다.

| 무엇 | 열쇠 |
|---|---|
| 측정 component의 첫 간격 | `(seed, iid, "idle", component 순번, comm, "first", …)` |
| 측정 component의 k번째 run | `(seed, iid, "idle", component 순번, comm, k, "run")` |
| 키 입력 재생 위치 | `(seed, iid, "stimulus", 바깥 창의 순번)` |
| k번째 키 입력의 CPU | `(seed, iid, "input", k)` |
| operation의 길이 | `(seed, iid, "operation", operation 순번)` |
| launch phase의 repeat 선택 | `(seed, task id, "launch", "repeat")` |
| batch loop의 k번째 run과 block | `(seed, iid, "batch_run", k)`, `(seed, iid, "batch_block", k)` |
| 빌드 job i의 구성원 단계 CPU | `(seed, 부모 iid, "job", i, 역할, 단계)` |
| chain 구성원 k의 RUN | `(seed, iid, "per_schedule_run", k)` |

여기서 `iid`는 instance id입니다(`count`가 1이면 task id 그대로, 아니면 `renderers.3` 같은 것). launch phase만 예외로 task id를 씁니다. 같은 `count` 묶음의 instance들이 측정 repeat 하나를 공유해야 하기 때문입니다(11.3절).

이 표에서 결정적인 성질이 나옵니다. **열쇠에 다른 task의 정보가 들어가지 않습니다.** 그래서 timeline에 task를 하나 더 넣어도 기존 task의 값은 하나도 바뀌지 않습니다. 또 **열쇠에 파일 이름이 들어가지 않습니다.** seed와 instance id가 같으면 다른 파일에서도 같은 값이 나옵니다. 파생 파일이 base와 같은 값을 갖는 이유가 이것입니다.

> **코드로.** 이 성질은 test로 고정되어 있습니다. `dataset/tools/tests/test_invariants.py`의 docstring은 "The task-2.3 spec's invariant charter"라고 적습니다. `test_byte_determinism`은 같은 fixture를 두 번 compile해서 바이트가 같은지 봅니다. `test_keyed_isolation_unrelated_task`는 task 하나(`extra`)를 더한 뒤 기존 task들의 arrive event와 wake event가 하나도 바뀌지 않았는지 봅니다. `test_one_entry_diff`는 task 하나의 이름만 바꾼 뒤 그 task의 `name` 말고는 아무것도 바뀌지 않았는지 봅니다. 마지막 것이 C2 짝의 원리("a one-field edit changes exactly that task's event")입니다.

## 10.5 실제로 확인하기: `c7-dev`와 `c1-dev`

`c7-dev`는 `c1-dev`에서 파생된 파일입니다(5.6절). seed가 107로 같고, 편집기의 task id가 `editor`로 같고, 도착 시각이 0 s로 같습니다. 다른 것은 편집기가 26.385 s에 닫힌다는 것, 입력 창이 짧다는 것, 그리고 업그레이드 task가 하나 더 있다는 것입니다. 열쇠의 성질이 맞다면, 처음 26.385 s 동안 편집기는 두 파일에서 똑같이 행동해야 합니다.

이 권을 쓰며 두 artifact를 읽어 비교했습니다.

- 편집기의 timer wake. `c1-dev`에서 26.385 s 전에 떨어지는 `timer:editor` wake는 2,774개이고, `c7-dev`의 `timer:editor` wake도 2,774개이며, 시각 목록이 완전히 같습니다. 두 파일 모두 첫 넷이 2,670 µs, 3,007 µs, 4,449 µs, 16,901 µs입니다.
- 편집기의 키 입력. `c1-dev`의 `input:editor` wake 186개 중 2–24.385 s에 떨어지는 것은 49개이고, `c7-dev`의 `input:editor` wake 49개와 시각 목록이 완전히 같습니다. 첫 키 입력은 두 파일 모두 12,752,609 µs입니다.
- program의 시작. 두 파일 모두 편집기 program이 `WAIT timer:editor`, `RUN 119`, `WAIT timer:editor`, `RUN 12`로 시작합니다.

timer wake가 같은 것은 열쇠 덕분입니다. component의 wake는 도착 시각부터 앞으로 하나씩 뽑고, 각 추출이 `(107, "editor", "idle", …, k, …)`로 열쇠가 붙으므로, 파일이 짧으면 긴 파일의 앞부분이 그대로 나옵니다. 키 입력이 같은 것은 열쇠에 더해 `slice_of` 덕분입니다(11.4절). 9.18 이전에는 이 둘째 줄이 성립하지 않았습니다.

## 10.6 manifest와 대조해 확인하기

결정성의 가장 직접적인 확인은 다시 compile해서 hash를 비교하는 것입니다. 이 권을 쓰며 `python3.12`로 `compile.py`의 `compile_one`을 다섯 파일(`c1-office`, `c1-dev`, `c7-dev`, `c2-p1a`, `c1-gaming`)에 불러, 결과 바이트의 SHA-256을 commit된 `dataset/build.manifest.json`과 비교했습니다. 다섯 파일 모두 artifact hash, report hash, demand 기록이 manifest와 같았습니다. 파일 하나에 0.1–0.5 s가 걸렸습니다.

기계가 달라도 같은지는 CI가 확인합니다. 9.22 D6이 기록한 run 38131040159는 GitHub의 Linux runner에서 core set과 variant를 다시 build했고, `check` 단계가 runner가 쓴 manifest를 commit된 바이트와 비교해 통과했습니다. 인지오의 Apple M1 Pro(macOS)에서 bless한 manifest를 Linux가 바이트 단위로 재현한 것입니다. "platform-deterministic"이라는 docstring의 주장을 실제로 시험한 기록입니다.

> **왜 이렇게 정했나.** 결정성은 Python과 library의 version에 기댈 수 있습니다. 기록된 build는 모두 Python 3.12에서 했고(9.13 reads "Python 3.12.4", 9.14 D12 "the default `python3` is 3.13 without `jsonschema`"), CI도 3.12입니다(`.github/workflows/dataset.yml`의 `python-version: "3.12"`). 2026-10-15에 9.23 D15가 직접 의존성 여섯(dataset 쪽 `PyYAML==6.0.1`, `jsonschema-rs==0.29.1`, `pytest==8.3.4`, `numpy==1.26.4`, harness 쪽 `jsonschema`, `pandas`)을 집 기계의 version에 정확히 고정했습니다. runner는 그날의 최신 version을 설치했고, pytest 9.1.1에서 dataset CI가 실패한 일이 있었기 때문입니다(run 38387283407). 2026-10-16에는 인지오가 Python도 3.12로 정했고, `dataset/README.md`가 "Needs Python 3.12"라고 적습니다. 다른 version에서 `statistics.NormalDist.inv_cdf`나 float 반올림이 같은 byte를 내는지는 확인하지 않았습니다(numpy 1.26.4에는 Python 3.13용 wheel이 없습니다). `dataset/Makefile`은 `PY ?= python3`이라서, 기본 `python3`이 3.12가 아닌 기계에서는 `make dataset PY=python3.12`처럼 줘야 합니다.

---

# 11장 · Archetype마다 다른 전개

9.5절에서 본 것처럼 compiler는 archetype의 종류에 따라 다른 전개 함수를 부릅니다. 이 장은 지금 쓰이는 다섯 경로를 하나씩 따라갑니다. 측정된 앱(대부분의 대화형 프로그램과 daemon), 주기적 재생기, batch job, 빌드, 게임 chain입니다. 각 절은 "이 archetype이 실제로 무엇을 흉내 내는가"에서 시작해 "compiler가 그것을 어떤 program으로 펴는가"로 내려갑니다. archetype 값이 어떻게 측정되었는지는 archetype library 권의 몫이고, 여기서는 그 값이 program이 되는 과정만 봅니다.

## 11.1 측정된 앱: component를 시간축에 뿌리기

`code-editor`, `web-browser`, `office-writer` 같은 측정된 앱은 CI runner에서 실제 프로그램을 돌려 `perf sched record`로 기록한 값에서 왔습니다. 기록에서 thread 이름(comm)별로 "깨어나는 간격"과 "깨어날 때마다 쓰는 CPU"의 분포를 뽑은 것이 **component**입니다(6.1절에서 풀어 쓴 용어). 사용자가 아무것도 하지 않아도 이 thread들은 저마다의 timer로 깨어납니다. 커서 깜빡임, 자동 저장, 메일 확인, 화면 합성 같은 것들입니다.

`_measured_unroll`은 이 component들을 task의 수명 위에 뿌립니다. `_component_events`가 component 하나마다 다음을 합니다.

1. 시작 시각 t₀에서 첫 깨어남까지의 간격을 뽑습니다. 이때 보통 간격이 아니라 **forward-recurrence 간격**을 씁니다(`sample_first_gap`).
2. 그 시각에 깨어남 하나를 놓고, 그 깨어남의 CPU(run)를 run 분포에서 뽑습니다.
3. 다음 간격을 간격 분포에서 뽑아 더하고, 끝 시각 t₁에 닿을 때까지 반복합니다.

모든 component의 깨어남을 모으면 `(시각, run, "timer")` 목록이 됩니다. 이것을 나중에 키 입력과 합쳐 시각 순으로 정렬하고(같은 시각이면 timer가 먼저), 깨어남마다 `wake` event 하나(`timer:<iid>` channel)와 program의 `WAIT`·`RUN` 한 쌍을 만듭니다. run이 0이면 `RUN`을 생략합니다. 그리고 마지막 깨어남 뒤에 그 깨어남의 channel로 `WAIT`을 하나 더 붙입니다(9.23 D16, 2026-10-15). 깨어남이 N개면 WAIT이 N + 1개이고, program은 할 일이 바닥나지 않고 막힌 채로 박힌 퇴장을 맞습니다. 측정된 대화형 앱은 대개 timer component로 마지막에 깨어나므로 그 WAIT은 보통 `timer:` channel입니다. core set에서는 키 입력을 받는 task 24개가 모두 `timer:`의 WAIT으로 끝납니다. 9.23 D16의 기록은 괄호 안에 "an interactive task's on its input"이라고 적었지만, 코드는 마지막 깨어남의 channel을 쓰고, 2026-10-16에 인지오가 코드 쪽을 그대로 두기로 정했습니다. 그 WAIT의 channel을 읽는 소비자는 없습니다.

**forward-recurrence 간격이 왜 필요한가.** 버스 정류장에 아무 때나 도착했을 때 다음 버스까지 기다리는 시간은 "버스 배차 간격"과 다릅니다. 긴 간격일수록 그 안에 도착할 확률이 높으니, 무작위로 떨어진 순간이 속한 간격은 평균보다 깁니다(length-biased). 그리고 그 간격 안의 아무 지점에나 떨어지므로 남은 시간은 그 간격의 일부입니다. task가 0 s에 "이미 돌고 있던 프로그램"으로 등장한다면, 첫 깨어남까지의 시간은 이 방식으로 뽑아야 맞습니다. `sample_first_gap`은 간격의 구간을 "그 구간의 확률 × 구간 평균"에 비례하게 고르고, 구간 안에서도 길이에 비례하게 고른 뒤, 그 간격의 균등한 일부를 첫 간격으로 씁니다.

> **왜 이렇게 정했나.** 9.5 D77(2026-09-26)입니다. "A component's wakes over a span (task lifetime, focus window, operation) are a stream already running at the span's start: the first wake falls one forward-recurrence gap after it." 기록된 이유는 측정이 틀어졌던 것입니다. 이전에는 첫 깨어남을 보통 간격으로 뽑았는데, 간격이 긴 component는 짧은 구간 안에서 깨어남 비율이 측정보다 크게 어긋났습니다. 60 s task에서 `message-bus`는 16.5배, `audio-server`는 6.85배, 숨은 renderer의 잔여 component는 3.70배였습니다. 이 수정으로 core set 100개 artifact 중 86개가 바뀌었다고 기록되어 있습니다(당시는 native와 single 두 mode가 있어서 artifact가 100개였습니다).

> **왜 이렇게 정했나.** "측정된 앱 하나 = task 하나, 깨어남을 하나의 사건 흐름으로 합침"이라는 모양은 9.5 D9(2026-09-14)입니다. "each D2 archetype compiles to one task whose program is one unrolled loop of WAIT then RUN over a merged, pre-sampled event stream of two kinds — input wakes from the timeline's stimulus and timer wakes from the archetype's measured idle cadence". 기록된 근거는 관측들이 모두 입력 말고도 timer로 깨어나는 활동을 보고한다는 것입니다(예: "timer messages 35.1 % vs UI 20.3 % of CPU", lorch2003의 Table 2). 결과로 "an unfocused application wakes on its timers for the whole segment", 앞에 있지 않은 앱도 segment 내내 timer로 깨어납니다.

## 11.2 입력 창, heavy event, operation

측정된 앱의 program에는 component 말고도 세 가지가 끼어들 수 있습니다.

**`focus_components`.** GIMP(`image-editor`)와 Kdenlive(`video-editor`)는 키 입력 stream이 없는 대신, 사용자가 앞에서 작업하는 동안의 활동 패턴을 따로 측정했습니다. 이 archetype은 입력 창 안에서는 평소 component를 빼고 `focus_components`로 바꿔 뿌립니다. 열쇠의 이름표가 `"idle"`이 아니라 `("focus", 창 순번)`이라서 창마다 독립된 흐름입니다.

**heavy event.** `web-browser`와 `game-client`는 측정 중 아주 드물게 일어난 큰 run을 "heavy event"로 따로 싣습니다. 한 측정 세션에 많아야 한 번 보였기 때문에 간격 분포가 없고, 측정된 비율(`rate_per_s`)만 있습니다. compiler는 지수분포로 간격을 뽑아 그 비율로 heavy event를 뿌리고(`_heavy_events`), run은 측정된 run 표에서 뽑습니다. 9.5 D64가 이 형식을 정했고, lint는 heavy event가 간격(`gap`)을 적으면 거절합니다("a heavy event states no gap — none is measured").

**operation.** timeline이 적은 operation(4.5절)마다 compiler는 측정된 길이 표에서 길이를 뽑아 `[at, at + 길이)` 구간을 만듭니다(파일 끝을 넘지 않게 자릅니다). 그 구간 안에서는 평소 component와 heavy event와 launch phase의 깨어남을 모두 빼고, 대신 operation 자신의 component를 뿌립니다. 키 입력도 그 구간 안에 떨어지는 것은 버립니다. 뽑은 길이는 `build.operations`에 `{name, at_us, duration_us}`로 남아 compile report의 `operations`가 됩니다.

> **왜 이렇게 정했나.** operation 구간 안의 키 입력을 버리는 것은 9.18의 결정 3이 counterpart의 키 입력을 "subset"으로만 시험하는 이유이기도 합니다. "Equality is not asserted: the counterpart's operations sit at their own positions (9.10 D44), and the compiler drops the keystrokes that fall inside an operation." 파생 파일은 operation을 base와 다른 시각에 두므로(창의 비율을 지키느라), base에서 살아남은 키 입력이 파생 파일에서는 operation 구간에 걸려 사라질 수 있습니다.

## 11.3 중간에 시작하는 앱의 launch phase

0 s보다 늦게 도착하는 앱은 "막 실행된 앱"입니다. 실행 직후의 프로그램은 안정 상태와 전혀 다르게 행동합니다. 9.10 D21의 근거 기록에 따르면 Chrome은 20–40 s에 몰아치고 65–180 s 사이에 약 880 ms짜리 run이 나오며, Thunderbird는 10–30 s와 70–90 s에 몰아칩니다. 그래서 측정 campaign은 앱마다 실행(exec)부터 안정될 때까지를 기록해 **launch phase**로 저장했습니다(`dataset/launch/launch-<entry>.json.gz`, tree에 10개).

`launch phase` — 앱이 실행된 직후부터 안정 상태에 이를 때까지의 활동입니다. 이 dataset은 그것을 측정해 두었다가, timeline에서 0 s보다 늦게 도착하는 task에 재생합니다.

`_launch_stream`은 이렇게 동작합니다. task의 archetype이 `launch` parameter를 갖고 도착 시각이 0보다 크면, 그 launch 파일의 측정 repeat 다섯 개 중 하나를 `(seed, task id, "launch", "repeat")`로 고릅니다. repeat 안의 stream(thread별 깨어남 기록)들을 열쇠 순서로 섞고, instance 번호에 맞는 stream을 고릅니다. 그 stream의 `(상대 시각, run)` 목록과 phase 길이를 돌려줍니다. `_measured_unroll`은 phase 길이 동안 이 기록을 timer 깨어남으로 그대로 재생하고, 평소 component는 phase가 끝난 시각(`t_steady`)부터 뿌립니다.

`c3-workday`로 계산하면, 60 s에 도착하는 Writer의 launch phase는 40.756 s 동안 깨어남 857개이고, 1,485 s에 도착하는 Thunderbird의 것은 408.917 s 동안 깨어남 13,110개입니다(이 권을 쓰며 `_launch_stream`을 직접 불러 계산했습니다). Thunderbird의 phase는 파일 끝(1,545 s)보다 훨씬 길어서, 파일이 그 phase 안에서 끝납니다. 0 s에 도착하는 브라우저와 renderer는 launch phase가 없습니다.

`count`가 1보다 큰 묶음(`c4-compile`의 `injected-renderers` × 4)은 repeat를 task id로 고르므로 네 instance가 같은 repeat를 공유하고, 그 안의 서로 다른 stream을 하나씩 씁니다. 같은 브라우저 창의 네 탭이 한 번의 실행에서 함께 열린 모습입니다(9.10 D133). repeat 안의 stream 수보다 instance가 많으면 build가 실패합니다.

periodic 재생기(11.5절)의 launch phase는 깨어남 대신 cycle 격자에 묶어 넣습니다. phase 안에서 시작하는 cycle은 그 cycle 구간에 떨어진 측정 CPU의 합을 run으로 씁니다(9.10 D138).

launch 파일 열 개는 2026-10-15부터 build manifest의 `inputs`에 고정되어 있습니다(9.23 D11, 13.5절).

## 11.4 키 입력 재생: 위치를 뽑고 잘라 붙이기

stimulus를 가진 앱(`office-writer`, `code-editor`, `mail-client`, `web-browser`)의 키 입력은 이렇게 만들어집니다(`_measured_unroll`의 마지막 부분).

1. archetype의 `stimulus.stream`이 가리키는 파일(`dataset/stimulus/<stream>.jsonl`)을 읽고, `stimulus.kinds`(네 앱 모두 `[key]`)에 해당하는 사건의 시각 목록을 만듭니다. stream의 전체 길이(span)는 마지막 사건의 시각입니다.
2. task의 입력 창마다(시간 순, 순번 j):
   1. 바깥 창을 정합니다. 창에 `slice_of`가 있으면 그것, 없으면 창 자신(순번 j).
   2. 재생 위치(offset)를 뽑습니다. `round(uniform(seed, iid, "stimulus", 바깥 창 순번) × max(0, span − 바깥 창 길이)) + (창 시작 − 바깥 창 시작)`.
   3. stream에서 `[offset, offset + 창 길이)`에 드는 사건들을 골라, 각 사건을 `창 시작 + (사건 시각 − offset)`에 놓습니다. operation 구간에 떨어지면 버립니다.
   4. 놓은 키 입력마다 CPU를 `input_run` 표에서 `(seed, iid, "input", k)`로 뽑습니다(k는 task 안에서 키 입력의 누적 순번).

**손으로 계산하기: `c1-office`의 Writer.** 입력 창은 2–58 s 하나(순번 0)이고 `slice_of`가 없습니다. stream `swell-word-c1`의 `key` 사건 span은 33,832,258,400 µs(약 9.4시간)입니다. 창 길이는 56,000,000 µs입니다. 10.2절에서 계산한 `uniform(101, "writer", "stimulus", 0)` = 0.4105356168765173을 쓰면, offset은 round(0.41053561… × (33,832,258,400 − 56,000,000)) = 13,866,357,078 µs입니다. 기록의 약 3시간 51분 지점부터 56 s를 잘라 온다는 뜻입니다. 그 구간에 `key` 사건이 270개 있고, 첫 사건은 창 시작 2 s에서 59,422 µs 뒤인 2,059,422 µs에 놓입니다. compile된 artifact의 `input:writer` wake도 270개이고 첫 wake가 2,059,422 µs입니다. 이 권을 쓰며 같은 계산을 코드 밖에서 다시 해서 artifact와 일치하는 것을 확인했습니다.

**`slice_of`가 하는 일: `c7-dev`.** `c7-dev`의 입력 창은 2–24.385 s이고 `slice_of: {from: 2s, to: 58s, index: 0}`을 가집니다. 그러면 2.2단계의 계산은 이렇게 됩니다.

- 바깥 창은 2–58 s(길이 56 s), 순번 0.
- offset = round(`uniform(107, "editor", "stimulus", 0)` × (span − 56 s)) + (2 s − 2 s).

이것은 `c1-dev`가 자기 입력 창 2–58 s(순번 0)에 대해 계산하는 offset과 **정확히 같은 식**입니다. seed(107), instance id(`editor`), 순번(0), 바깥 창 길이(56 s)가 모두 같기 때문입니다. 다른 것은 잘라 오는 길이(22.385 s 대 56 s)뿐이므로, `c7-dev`의 키 입력은 `c1-dev`의 키 입력의 앞부분이 됩니다. 10.5절에서 본 49개의 일치가 이것입니다.

`slice_of`가 없던 9.18 이전에는 2.2단계가 "창 자신의 길이"로 계산했습니다. `c7-dev`의 창 길이는 22.385 s라서 `span − 22.385 s`에 같은 u를 곱하면 다른 offset이 나왔고, 키 입력이 하나도 겹치지 않았습니다. 4.3절에서 본 audit A1의 "dev 0 of 78"이 그것입니다.

tree에서 입력 창이 있는 C7 counterpart의 키 입력을 base와 비교하면 이렇습니다. 표의 숫자는 시각의 수가 아니라 `input:<task>` wake **event**의 수이고, 괄호 안이 서로 다른 시각의 수입니다(재생한 흐름에서 키 입력 둘이 같은 µs에 떨어지는 일이 있습니다). 열은 base 전체, base에서 counterpart 길이 C 안에 드는 것, counterpart, 그리고 counterpart의 시각 집합이 base의 시각 집합의 부분집합인지입니다.

| mode | base 전체 | base의 [0, C) | counterpart | 부분집합? |
|---|---|---|---|---|
| browsing | 123 (118) | 90 (85) | 84 (79) | 예 |
| office | 270 (249) | 112 (102) | 101 (91) | 예 |
| dev | 186 (181) | 49 (47) | 49 (47) | 예 |
| mail | 35 (33) | 0 | 0 | 예 |
| indexing | 47 (46) | 28 (28) | 27 (27) | 예 |
| ml-train | 1,984 (1,844) | 1,754 (1,629) | 1,753 (1,628) | 예 |
| compile | 2,544 (2,354) | 398 (358) | 398 (358) | 예 |

counterpart가 base보다 적은 이유는 두 가지입니다. counterpart의 입력 창은 C − 2 s에서 닫히므로 base의 [C − 2 s, C) 키 입력이 빠지고, counterpart의 operation 구간에 걸린 키 입력이 빠집니다(browsing의 page load처럼). 어느 경우든 부분집합 관계는 성립합니다. 이것이 9.18의 test `test_c7_input_wakes_are_a_subset_of_the_bases_in_the_first_c_seconds`가 지키는 성질입니다.

9.18 D6은 같은 비교를 "browsing 85 → 79, office 102 → 91, dev 47 → 47, mail 0 → 0, indexing 46 → 27, compile 2354 → 358, ml-train 1844 → 1628"로 기록했습니다. 이 숫자는 event가 아니라 서로 다른 시각의 수입니다. browsing, office, dev, mail의 base 쪽은 counterpart 길이 안의 수(표 둘째 열의 괄호)이고, indexing, compile, ml-train의 base 쪽 46, 2,354, 1,844는 base 파일 전체의 수(첫째 열의 괄호)입니다. counterpart 길이 안으로 세면 28, 358, 1,629입니다. 9.23 D7(2026-10-14)이 이렇게 바로잡고 9.18 D6 옆에 그것을 가리키는 메모를 남겼습니다. 부분집합 관계는 어느 쪽으로 세어도 성립합니다.

## 11.5 주기적 재생기: TIMER 격자

`video-player`(mpv의 영상), `audio-player`(mpv의 음악), `video-call`(브라우저 안의 영상 통화)은 측정된 앱이지만 component를 뿌리지 않습니다. 이 셋은 매체의 한 주기마다 일정량의 일을 하는 **periodic entry**입니다. 영상은 frame 한 장, 음악은 오디오 버퍼 하나, 통화는 오디오 처리 한 주기입니다. archetype은 `period`(주기)와 `cycle_run`(한 주기 동안 프로세스 tree 전체가 쓰는 CPU)을 가집니다.

`_periodic_unroll`은 task의 수명 동안 주기마다 `TIMER(period)` 하나와 그 주기의 `RUN` 하나를 붙입니다. run은 `cycle_run` 표에서 `(seed, iid, "cycle", k)`로 뽑고, 0이 나오면 RUN을 생략합니다. LOOP를 쓰지 않고 주기 수만큼 펼칩니다.

`c1-media`로 확인하면, 영상 task의 주기는 33,348 µs이고 60 s 동안 tick이 1,800개(60,000,000 ÷ 33,348 ≈ 1,799.2를 올림)이므로 program은 TIMER와 RUN 1,800쌍에 끝의 TIMER 하나가 더 붙어 3,601 명령어입니다. 마지막 TIMER의 tick(1,800 × 33,348 = 60,026,400 µs)은 퇴장 시각 60 s 뒤에 떨어지므로, task는 그 TIMER에서 기다리다 퇴장합니다(9.23 D16). 음악 task의 주기는 49,635 µs, tick 1,209개에 끝의 TIMER 하나, 2,419 명령어입니다. 처음 네 명령어는 영상이 `TIMER 33348`, `RUN 3814`, `TIMER 33348`, `RUN 3014`입니다. 이 파일에는 wake event가 하나도 없습니다. 재생기는 외부 사건 없이 자기 격자로만 깨어나기 때문입니다.

TIMER의 의미는 contract §3의 절대 격자입니다. task의 t₀(첫 TIMER를 실행한 시각)에서 t₀ + k·period마다 깨어납니다. compiler의 docstring은 "tick 0 consumed at arrival"이라고 적습니다. 첫 TIMER는 도착 시각에 바로 소비되어 첫 frame이 곧장 시작됩니다. lane이 바빠도 마찬가지입니다. 첫 TIMER는 도착 단계에서 실행되므로 t₀는 task의 도착 시각입니다(reference simulator의 `on_arrive`, `simulator/src/sim.cpp`. 2026-10-16에 인지오가 이 읽기로 정했고, `docs/simulator/simulator-guide.md` §9.2가 적습니다). 이것이 canonical lint의 "TIMER first" 규칙(13.2절)과 맞물립니다. TIMER가 program의 첫 명령어여야 t₀가 도착 시각과 같아집니다.

> **왜 이렇게 정했나.** 재생기를 "주기마다 job 하나"로 싣는 것은 9.5 D75(2026-09-26)입니다. 기록된 근거는 `liu-jacm73`(Liu와 Layland의 고전 논문)의 주기적 job 모형, "each task must be completed before the next request for it occurs"입니다. 측정된 값은 음악 49.635 ms, 영상 33.348 ms(파일의 33.333 ms와 거의 같음), 통화 10.001 ms이고, 한 주기의 평균 CPU를 주기로 나눈 몫은 0.00710, 0.12182, 0.23710입니다. 통화는 cycle의 약 5 %가 주기를 넘깁니다. 같은 결정이 TIMER를 "주기와 마감을 가진" 명령어로 남기고, 마감이 없는 측정 timer 깨어남은 9.5 D74에 따라 WAIT으로 보냈습니다(7.6절).

## 11.6 batch job: run과 block의 반복

`cpu-batch`와 측정된 batch entry들(`file-indexer`, `package-upgrade`, `incremental-backup`, `video-transcoder`, `game-download`, `file-archiver`)은 `_batch_loop`로 갑니다. 하는 일은 이렇습니다(`_batch_ops`).

1. `bind.program`으로 측정표 묶음을 고릅니다(`<program>_run`, `<program>_block`). 묶음이 하나뿐인 archetype은 `program` 없이 그 하나를 씁니다.
2. 쓴 CPU가 `total_work`에 닿을 때까지 반복합니다. run 하나를 `<program>_run` 표에서 뽑고(남은 양을 넘지 않게 자름), 그 뒤의 block 하나를 `<program>_block` 표에서 0을 허용해 뽑습니다.
3. block이 1 µs 이상이면 그동안 모은 run을 `RUN` 하나로 내보내고 `SLEEP(block)`을 붙입니다. block이 0이면 run을 내보내지 않고 다음 run과 합칩니다.
4. 마지막에 남은 run을 `RUN`으로 내보내고 `EXIT`를 붙입니다.

`c2-p1a`의 학습 job이 56 명령어인 이유가 3단계입니다(6.2절). MNIST 학습의 측정 block 표는 0이 많아서, 대부분의 run이 합쳐져 수 분짜리 RUN이 됩니다.

`c6-spoof`의 가짜 `chrome`(`program: spoof`)은 예외입니다. 측정표가 없고, `RUN(total_work)` 하나와 `EXIT`입니다. 코드 주석은 "the chrome spoof is one uninterrupted RUN by construction (D7)"이라고 적습니다.

> **왜 이렇게 정했나.** batch job의 이 모양은 9.6 D21, D22, D25입니다(`_batch_loop` docstring). `cpu-batch`의 modeling note가 요약합니다. "a run drawn from the bound program's measured runs between voluntary blocks, then the block that followed such a run … until `total_work` of CPU is spent; the table set is chosen by the `program` binding, never by the task's display name … A zero block means the program ran on, so the runs it separates are emitted as one RUN." 측정표를 이름이 아니라 `program` binding으로 고르는 것이 중요합니다. 그래야 `c6-spoof`처럼 이름과 행동이 다른 task를 만들 수 있습니다.

`block` — 여기서는 프로그램이 스스로 CPU를 내려놓고 쉰 시간(디스크나 네트워크를 기다리는 등)입니다. 측정에서는 run이 끝난 뒤 다음 run이 시작할 때까지의 off-CPU 시간입니다.

## 11.7 빌드: object job과 spawn table

`build-orchestrator`(`make`)는 `_orchestrator_unroll`로 갑니다. 7.8절에서 결과의 모양을 보았으니 여기서는 과정을 봅니다.

1. `fork_cap = parallelism_cap × 6`을 정합니다(`OBJECT_JOB`의 역할이 여섯이므로).
2. object job i(0부터 `spawn_count − 1`까지)마다 `_object_job`으로 spawn table 항목 여섯 개를 만듭니다. 역할은 fork 순서대로 `sh`(4단계), `gcc`(3단계), `cc1`(1), `as`(1), `fixdep`(1), `rm`(1)입니다. 각 단계의 CPU는 `compiler-child` entry의 `(역할, 단계)` 표에서 `(seed, 부모 iid, "job", i, 역할, 단계)`로 뽑습니다. `cc1`의 이름만 `child_name`으로 바꿉니다.
3. 각 구성원의 program은 고정된 각본입니다. `sh`가 먼저 돌아 `gcc`를 깨우고, `gcc`가 `cc1`을 깨우고, … 하는 순서가 WAIT/WAKE로 짜여 있습니다. 일을 마친 구성원은 자기 channel에서 다시 기다리고, 마지막에 `sh`가 모든 구성원을 깨워 함께 `EXIT`합니다.
4. `make` 자신의 program은 job마다 `RUN(dispatch_overhead)` 하나와 `FORK` 여섯 개, 끝에 `WAIT children:<iid>`와 `EXIT`입니다.

`c1-compile`에서 첫 job의 `cc1` 단계는 476,877 µs(약 0.48 s)이고, `sh`의 첫 단계는 848 µs입니다. 컴파일러 본체가 일의 대부분을 합니다. 빌드 전체의 CPU는 compile report에서 1,315,906,652 µs(약 22분)이고, 편집기가 275,297,827 µs를 더해 utilization이 0.9982입니다. 9.10 D78/D90의 규칙이 파일 길이를 "어떤 정책 아래에서도 빌드가 끝나는 가장 작은 정수 초"로 정해서 1,594 s가 되었습니다.

> **왜 이렇게 정했나.** 단계별 CPU를 역할 하나의 표가 아니라 `(역할, 단계)`마다 따로 뽑는 것은 9.6 D20입니다. 기록된 이유는 측정된 2,857개 job에서 `cc1`은 99.3 %가 한 번만 깨어나는데 `sh`는 5–7번, `gcc`는 4–7번 깨어나고, 첫 run이 크고(중앙값 0.72 ms, 1.70 ms) 나중 run이 작아서(0.01–0.34 ms) "one table per role describes neither"였기 때문입니다.

## 11.8 DKMS 모듈 빌드

`module-build-orchestrator`는 `c7-compile`의 `dkms` 하나만 씁니다. Ubuntu의 무인 업그레이드가 커널 보안 업데이트 뒤에 NVIDIA의 open kernel module을 다시 빌드하는 장면을 측정한 것입니다(`c7.variant.yaml` 주석, 9.10 D4, D46–D57). 커널 빌드와 달리 job의 종류가 여럿입니다.

`_module_build_unroll`은 이렇게 동작합니다.

1. archetype의 `job_order`를 풉니다. 이것은 측정된 빌드가 job을 실행한 순서를 run-length로 줄인 문자열입니다(`"p21 C2 c1 p4 …"`, "p 21개, C 2개, c 1개, p 4개 …"). 글자는 job 종류를 뜻합니다. 자식 entry `module-compiler-child`의 `letters`에 따르면 `o`는 `object`, `p`는 `kprobe`, `c`는 `conftest_a`, `C`는 `conftest_b`입니다.
2. job마다 그 종류의 process tree(`trees`)를 `_tree_job`으로 spawn table 항목들로 펼칩니다. 뿌리가 먼저 돌고, 자식이 있는 구성원은 단계를 하나 돌고 다음 자식을 깨워 기다렸다가 다음 단계를 도는 식입니다. 단계 CPU는 `(종류, 구성원, 단계)` 표에서 뽑습니다. 이름은 `names` 표로 바꿉니다(예: `gcc` → `x86_64-linux-gn`, 15자에서 잘린 cross 컴파일러 이름).
3. job마다 `RUN(dispatch_overhead)`와 그 job의 항목 수만큼 `FORK`를 붙입니다.
4. `WAIT children:<iid>` 뒤에, 빌드의 직렬 꼬리를 batch loop로 붙입니다. `tail_work`(꼬리의 CPU 총량)를 한 번 뽑고, `tail_run`과 `tail_block` 표로 11.6절과 같은 방식의 RUN·SLEEP을 만듭니다. 마지막에 `EXIT`.
5. `fork_cap`은 `parallelism_cap × 6`, 커널 빌드와 같은 규칙입니다(9.10 D57).

tree의 `c7-compile` artifact에서 `dkms`는 `fork_cap` 48, spawn table 9,980칸(job 1,557개), program 15,828 명령어(FORK 9,980, RUN 3,702, SLEEP 2,144, WAIT 1, EXIT 1)입니다. 빌드의 CPU는 225,458,581 µs로, 파일 길이 225.458 s와 같습니다. `c7.variant.yaml` 주석이 "C = 225.458 s, the build's CPU as compiled under the file's seed"라고 적은 대로, 이 counterpart의 길이는 이 seed로 compile한 빌드의 CPU 총량에서 정했습니다.

## 11.9 게임 chain: constructor와 lane scaling

`game-task-chain`은 library에서 유일하게 측정값이 아니라 문헌(LAVD 발표 자료)에 기댄 entry이고, 유일하게 모양 자체가 parameter인 entry입니다. modeling note는 "The only entry whose topology is a parameter: the compiler's chain constructor expands it into chain_length members plus the wineserver member, chain_length + 1 ordinary tasks, with WAIT/WAKE channels wired from the head to the last member"라고 적습니다(2026-10-17부터. 그 전의 "`chain_length` ordinary tasks"는 `wineserver` 구성원을 세지 않았습니다).

`chain constructor` — archetype 하나를 compile 때 여러 개의 평범한 task로 펼치는 compiler의 특별한 경로입니다. contract §6은 이것을 "resolved at load time, not in the interpreter"라고 적습니다. 펼친 뒤에는 모든 구성원이 평범한 program이고, 특별함은 초기화에만 있습니다. `chain head` — chain의 첫 구성원, TIMER로 깨어나 frame을 시작하는 task입니다.

`_chain_constructor`의 단계를 `c1-gaming`(seed 102, instance id `game`)으로 손으로 따라가겠습니다. 이 권을 쓰며 각 추출을 `sampling.sample`로 직접 불러 확인했습니다.

**1단계, 구성원 수와 frame 주기.** `chain_length`는 상수 16(`lavd-ossna24:s12`, "There are 15-20 game-specific tasks"), `frame_period`는 상수 16,667 µs(`steamos-refresh`, Steam Deck LCD의 기본 60 Hz를 1/60 s로 계산한 design 값)입니다.

**2단계, 구성원 id와 이름.** id는 `game.chain.1`, `game.wineserver`, `game.chain.2`, …, `game.chain.16`의 17개입니다. 이름은 머리가 task 이름 `Troy.exe`, 둘째가 compiler가 붙인 `wineserver`, 나머지 15개가 `member_names`입니다. `member_names`가 `chain_length − 1`개가 아니면 build가 실패합니다.

**3단계, 구성원마다 RUN 뽑기.** 머리는 `per_schedule_run`을 순번 0으로, `wineserver`는 상수 `wineserver_run`(260 µs, slide 13의 "wineserver:260 usec")을, 나머지는 `per_schedule_run`을 순번 1–15로 뽑습니다. `per_schedule_run`은 10.3절의 anchored lognormal입니다. 뽑힌 값은 순서대로 481, 260, 801, 647, 856, 1094, 502, 218, 848, 355, 907, 892, 756, 834, 591, 501, 883 µs이고, 합계는 11,426 µs입니다.

**4단계, lane scaling.** mode가 `single`이므로 chain 전체의 frame당 CPU를 `lane_share`만큼으로 맞춥니다. 배율은 `lane_share × frame ÷ 합계` = 0.9 × 16,667 ÷ 11,426 = 1.31282입니다. 각 RUN에 이 배율을 곱해 반올림하면(최소 1) 631, 341, 1052, 849, 1124, 1436, 659, 286, 1113, 466, 1191, 1171, 992, 1095, 776, 658, 1159 µs가 되고, 합계는 14,999 µs입니다. 6.3절에서 artifact에서 읽은 값과 같습니다. `wineserver`가 260에서 341로 커진 것도 보입니다(9.4 D4가 기록한 "c1-gaming `single` RUN 341 µs after scaling"과 같습니다).

**5단계, program 짜기.** 구성원 k의 program은 `LOOP unbounded` 하나이고, 몸통은 머리면 `TIMER(frame)`, 아니면 `WAIT chain:<자기 id>`로 시작해, `RUN`, 그리고 마지막 구성원이 아니면 `WAKE <다음 구성원>`입니다. 모든 구성원의 도착과 퇴장은 task의 것(0 s, 60 s), class는 `game-task-chain` entry의 것(`normal`)입니다. CPU 수요는 구성원마다 `RUN ÷ frame × 수명`으로 계산합니다.

`lane scaling` — 여러 core를 가진 기계에서 측정한 수요를 이 연구의 CPU 하나짜리 simulator에 맞게 줄이는 compile 단계입니다. archetype이 `scalable`로 선언한 field에만 적용됩니다. `lane_share` — 게임 chain의 frame당 CPU를 CPU 하나의 몇 배로 맞출지 정하는 binding입니다. 0.9는 90 %, 1.45는 145 %(CPU 하나로 감당할 수 없는 양)입니다.

**왜 lane scaling이 필요한가.** LAVD 자료의 게임은 여러 core에서 돌았습니다. 그 per-schedule runtime을 그대로 열일곱 단계에 쓰면, frame 하나에 CPU를 얼마나 쓸지가 측정한 기계의 core 수와 무관하게 정해집니다. simulator는 CPU 하나뿐이므로, 그 값이 CPU 하나의 몇 %인지가 실험 조건을 좌우합니다. 그래서 chain의 총량을 timeline이 정하는 비율(`lane_share`)로 맞춥니다. 개별 RUN의 상대적 크기(어느 단계가 무거운가)는 뽑은 값을 따르고, 총량만 맞춥니다. tree의 library에서 `scalable`이 비어 있지 않은 entry는 `game-task-chain` 하나뿐이고, 그 rule은 "scale the chain's aggregate demand per frame to lane_share of the lane (building-plan §5a)"입니다.

> **왜 이렇게 정했나.** lane scaling은 2026-08-26 grill의 D15와 D16에서 시작합니다. D15는 CPU 하나짜리 simulator를 유지하기로 하면서 그 대가를 적습니다. "Multi-core-measured archetype demands (LAVD gaming: ~300 tasks at 65–95% of a many-core machine) cannot fit the simulator's single lane". LAVD 슬라이드는 trace를 잰 기계를 밝히지 않으므로 "many-core"는 archive의 읽기입니다. D16은 그 해결로 "Scaling is a per-archetype declared compiler pass (fields + rule + evidence in `modeling_notes`), never baked into `archetypes.yaml` values"를 정합니다. archetype의 값은 측정 그대로 두고, compile 단계에서만 줄인다는 뜻입니다. `lane_share`의 네 값(`c1-gaming` 0.9, `c2-p2a` 가족 0.95, `c3-evening` 1.45, `c6-dual` 0.6)은 9.10 D31이 design으로 기록했고, `source` map에 `design` label로 적혀 있습니다.

> **왜 이렇게 정했나.** `wineserver`가 chain 구성원인 것은 9.4 D4(2026-09-13)입니다. 이전에는 별도의 daemon task로 묶었는데, LAVD 자료의 slide 11(게임 dispatcher thread들의 hub), 13(coordination task), 16(가장 큰 edge가 `wineserver → Troy.exe` epoll 134,200회와 `Troy.exe → wineserver` pipe_read 58,134회)이 wineserver를 게임 그래프의 일부로 보여 준다는 것이 기록된 근거입니다. 요청-응답의 왕복을 한 방향 릴레이로 펴는 것은 "our linearisation"으로 modeling note에 적혀 있습니다. 구성원 이름 15개는 9.10 D26이 같은 slide 16의 process tree에서 가져왔습니다. 머리 뒤의 네 `Task worker thr`, `dxvk-cs`, `dxvk-submit`, 두 `winepulse_*`, `FAudio_AudioCli`, 그리고 이름이 나오지 않는 여섯 구성원은 process의 comm인 `Troy.exe`를 씁니다.

## 11.10 trace replay: variant에서만 쓰는 경로

`_measured_unroll`, `_periodic_unroll`, `_batch_loop`에는 하나의 분기가 더 있습니다. archetype params에 `replay`가 있으면, 측정에서 뽑은 분포 대신 측정 repeat 하나의 실제 기록(`dataset/replay/replay-<entry>.json.gz`, tree에 6개)을 그대로 씁니다. core set의 library에는 `replay` param이 없으므로 이 경로는 core set compile에서 쓰이지 않습니다. RQ0 gate spec의 민감도 variant 중 `replay` set(`c7-dev@replay`, `c7-browsing@replay`, `c7-meeting@replay`, `c2-p1a@replay`)을 만들 때만, `wlc/variants.py`가 library 사본에 `replay` param을 넣고 다시 compile합니다. 9.14 D10이 규칙을 정했습니다. 기록이 task보다 짧으면 build가 실패하고, "nothing is wrapped or padded"입니다. 이 경로의 결과는 compile report의 `replay` 항목에 stream 이름과 offset으로 남고, variant는 report를 쓰지 않으므로 variant manifest가 그것을 기록합니다(예: `c2-p1a@replay`의 편집기는 `replay-code-editor`의 243,964,687 µs 지점부터). variant의 나머지는 민감도 variant를 다루는 권의 몫입니다.

---

# 12장 · Demand 추정과 compile report

compile이 끝나면 compiler는 각 파일이 CPU를 얼마나 원하는지를 계산해 둡니다. 이 장은 그 숫자가 어떻게 계산되는지, 그 숫자가 한때 build를 실패시키는 관문이었다가 2026-10-09에 기록하는 숫자로 바뀐 역사, 그리고 그 숫자를 읽을 때 조심해야 할 점을 다룹니다.

## 12.1 demand는 compile하면서 쌓인다

`demand` — task가 수명 동안 쓰려는 CPU 시간의 총량(µs)입니다. 실제로 받게 될 CPU가 아니라 원하는 양입니다. `utilization` — 파일 전체의 demand를 파일 길이로 나눈 값입니다. 1.0이면 CPU 하나를 꽉 채우는 양, 1.0보다 크면 CPU 하나로는 다 줄 수 없는 양입니다.

9.4절에서 본 것처럼 각 전개 함수는 `RUN`을 붙일 때마다 `_TaskBuild.demand_us`에 그 µs를 더합니다. 그래서 compile이 끝나면 task마다 정확한 합계가 있습니다. 경로별로 무엇이 더해지는지 정리하면 이렇습니다.

| 경로 | `demand_us` |
|---|---|
| 측정된 앱 | 모든 timer 깨어남, heavy event, launch phase, operation, 키 입력의 run 합계 |
| 주기적 재생기 | 모든 cycle의 run 합계 |
| batch job | `total_work` 그대로(run의 합이 정확히 그것이 되도록 잘랐으므로) |
| 빌드(`make`) | dispatch run 합계 + spawn table의 모든 자식의 단계 CPU 합계 |
| DKMS 빌드 | 위와 같고 꼬리의 CPU를 더함 |
| 게임 chain 구성원 | `round(RUN ÷ frame × 수명)`. LOOP를 펼치지 않으므로, frame마다 한 번씩 수명 내내 돈다고 보고 계산 |

이 숫자는 **정적 추정**입니다. 실제 simulation에서 task가 이만큼의 CPU를 받는다는 보장은 없습니다. 예를 들어 chain의 수요는 "모든 frame이 제때 돈다"는 가정이고, TIMER skip 규칙(7.6절) 아래에서 굶은 chain은 frame을 건너뛰므로 실제로는 덜 씁니다. 자식 process의 CPU는 부모의 수요에 합쳐 셉니다.

## 12.2 utilization과 segment별 utilization

`compile_timeline`의 report는 두 가지 비율을 계산합니다.

**파일의 utilization.** 모든 task의 `demand_us` 합계를 파일 길이(`duration_us`, 2.6절)로 나눕니다.

**segment별 utilization.** `wlc/estimate.py`의 `per_segment`가 계산합니다. 규칙은 이렇습니다. task마다 그 demand를 수명(도착부터 박힌 퇴장까지, 퇴장이 없으면 파일 끝까지) 위에 **고르게 펼칩니다.** 그리고 segment마다 그 segment와 겹치는 부분의 몫을 더해 segment 길이로 나눕니다.

`c3-workday`로 보면 segment 넷의 utilization은 0.0031(browsing), 0.0053(office), 0.9597(compile), 1.0251(mail)입니다(compile report). 빌드가 도는 compile 구간이 CPU를 거의 채우고, 빌드의 꼬리와 Thunderbird의 launch phase가 겹친 mail 구간이 1.0을 조금 넘습니다. 9.14 D4는 이 숫자들을 "the contended segments the pair review reads"의 예로 기록합니다(`c3-workday`'s compile segment 0.96 and its mail segment 1.03).

segment들이 파일을 빈틈없이 덮으면, segment별 utilization을 길이로 가중 평균한 값은 파일의 utilization과 같습니다. 이것이 test로 고정되어 있습니다(`test_demand_is_recorded_per_segment`, "the segments' time-weighted mean is the file's utilization").

> **코드로.** `per_segment(builds, segments, duration_us)`는 segment마다 `total = Σ demand × overlap ÷ life`를 계산해 `{index, t_start_us, t_end_us, utilization}`을 냅니다. 수명이 0 이하인 task는 건너뜁니다. 이 함수가 있는 `estimate.py`의 이름은 Phase 2의 "static demand estimate"에서 왔고, docstring은 "The estimate itself is computed exactly during synthesis (compiler.py accumulates each task's CPU demand in context). This module turns it into the manifest's demand record"라고 적습니다.

## 12.3 ~100–150 % window: 관문에서 기록으로

demand에는 긴 역사가 있습니다. 기록이 정확히 무엇을 말하는지 시간 순으로 옮깁니다.

**2026-08-26, 규칙의 시작.** workload-generation grill의 D15는 simulator를 CPU 하나로 유지하기로 하면서 다음을 덧붙였습니다. "**Demand-budget rule (stated explicitly):** every compiled workload's aggregate demand lands in the measurable oversubscription regime (~100–150% of the lane); the per-file RQ0 admission test (OPEN_QUESTIONS Q8) is the enforcement mechanism." 모든 workload의 수요가 CPU 하나의 약 100–150 %, 즉 측정 가능한 과부하 영역에 들어와야 한다는 규칙입니다. 이 단계에서는 집행 수단이 파일별 RQ0 admission test였습니다.

**2026-08-27, build 관문이 됨.** task 2.3의 결정 7이 이 규칙을 compiler의 관문으로 만들었습니다. "The linter hard-fails a compiled `-single` file whose static demand estimate falls outside ~100–150% of the lane, unless the timeline's `meta:` declares the calibration demand class — an explicit, reviewable exemption. Estimates are printed for every file either way." `calibration` class는 이 관문을 피하는, 눈에 보이는 면제로 생겼습니다. task 2.4의 결정 3은 C1을 `calibration`으로, C2–C6을 기본값 `oversubscribed`("hard-checked 100–150%")로 정했습니다.

`demand window` — 이 ~100–150 % 구간을 가리키는 이름입니다. `admission test` — 파일 하나에서 oracle 조건과 무작위 조건의 결과에 차이가 있는지 보는 파일별 검사입니다. 차이가 없으면 그 파일은 scheduler 설정이 결과를 바꾸지 못하는 파일이라는 뜻입니다.

**2026-09-06, manifest에 기록.** Phase 3의 결정 6이 "The compiler writes each file's `utilization` and `demand_class` into `dataset/build.manifest.json`"을 더했습니다. archive에 적힌 이유는 "so the paper can cite a committed value", 그리고 확인된 사실로 "the compiler computed utilization and demand class but printed them to stdout only; the manifest carried hashes alone"입니다. 계산은 하고 있었지만 화면에만 찍고 남기지 않았다는 것입니다.

**2026-09-09, 파생 파일의 면제를 눈에 보이게.** 5.4절에서 본 Phase 7의 결정 7입니다. 파생 파일은 `patch-meta`로 `calibration`을 직접 적습니다.

**2026-10-09, 재건한 set이 window 밖에.** 9.13의 reads R5는 bless 직전의 set에 window 규칙(`estimate.py`의 당시 규칙, "a single-lane file's demand in [1.00, 1.50] lanes unless its demand class is `calibration`")을 적용했습니다. `calibration` 40개는 면제였고, `oversubscribed` 10개 중 9개가 window 밖이었습니다. `c2-p1a` 14.51, `c2-p2a` 9.38, `c6-dual` 1.00, `c2-p1b` 0.92, `c2-p3b` 0.90, `c3-evening` 0.90, `c3-creation` 0.94, `c3-workday` 0.89, `c2-p3a` 0.44. 기록된 원인은 "`c2-p1a`'s and `c2-p2a`'s demands follow the training run and the download bound whole at their CPU totals (9.10 D17, D90, D142) inside short files"입니다. 9.10 D17이 batch job을 측정한 전체 크기로 묶게 하면서(3.3절), 짧은 파일 안에 거대한 job이 들어간 것입니다. 9.13의 결정 10은 bless를 compiler의 허용 옵션(위반을 경고로만 내고 파일은 쓰는 옵션)으로 하고, "the CI gate stays strict, red on the window until 9.14 redoes the rule"이라고 적었습니다. CI는 9.14가 규칙을 다시 정할 때까지 빨간불로 두었습니다.

**2026-10-09, 관문이 물러남.** 같은 날 9.14의 결정 4가 규칙을 바꾸었습니다(`_dev/docs/spec/jioh/task-9.14-consumer-rework.md`).

> "The demand window retires as a gate. The compiler records demand per file, as now, and per segment, newly, in the manifest, and never fails on it. The pair review reads each judging file's contended segment's demand where it reports the regime per pair. The building plan's §5a paragraph is restated: the `oversubscribed` class marks a file designed to hold contention, its demand a measured fact reported, not a window held."

9.14 D4가 구현을 기록합니다. `estimate.py`에서 window 정책이 사라지고 `per_segment`가 들어왔고, compile report가 `per_segment`를 가지게 되었고, `linter.py`에서 window 검사가 사라졌고, `compile.py`의 manifest demand 기록에 `segments`가 더해졌고, `--allow-window` 옵션이 없어졌습니다. 이때 다시 compile한 51개 artifact의 hash는 하나도 바뀌지 않았습니다(demand는 artifact가 아니라 manifest와 report에만 있으므로).

**지금 기록이 말하는 것.** 정확히 옮기면 다음과 같습니다.

- `dataset/tools/wlc/estimate.py`의 docstring: "The demand window of the earlier policy — a single-lane file of demand class `oversubscribed` had to land in [1.00, 1.50] — retired as a gate on 2026-10-09 (9.14 decision 4): every file's demand is a measured fact the manifest reports and the pair review reads per contended segment; no build fails on it."
- `docs/workload/building-plan.md` §5a: "a timeline's demand class names its design — `oversubscribed` (the default) marks a file designed to hold contention, `demand: calibration` one that is not — and says nothing about the file's compiled demand, which is a measured fact: the compiler records each `-single` workload's utilization per file and per ground-truth segment in its set's manifest (`dataset/build.manifest.json` for the core set) and never fails a file on it."
- `compile.py`는 파일마다 utilization을 화면에 찍습니다(`demand 0.03 (calibration)` 모양).
- 어느 lint도, 어느 test도 utilization의 범위를 검사하지 않습니다. 오히려 test `test_no_file_fails_on_its_demand`가 "every file lints clean whatever its demand"를 고정합니다.

즉 2026-10-09 이후 ~100–150 %는 build를 실패시키는 관문이 아니고, compiler가 파일을 그 범위로 맞추는 목표값도 아닙니다. `oversubscribed` class는 "경쟁을 일으키도록 설계했다"는 의도의 표시로 남고, 실제 수요는 측정된 사실로 manifest에 기록되어 짝 검토(pair review)가 segment 단위로 읽습니다. 2026-09-20 validity review memo는 그 전에 이 window를 "state the demand window as a scoping decision"이라고 권했습니다. "Below contention no scheduling policy differs, so the regime is the right one to measure in — but it is chosen, not found."

> **왜 이렇게 정했나.** 9.14의 기록(spec decision 4와 changelog D4)은 무엇이 window를 대신하는지만 적고 왜 물러났는지는 적지 않았습니다. 2026-10-16에 인지오가 이유를 밝혔습니다. 9.10 D17이 모든 job을 측정한 그대로 통째로 묶은 뒤로는 파일의 수요가 측정에서 따라 나오므로, 그것을 window 안에 붙들어 두려면 측정한 길이를 구부려야 했다는 것입니다. 그래서 수요는 붙들지 않고 파일별, segment별로 보고하고, 짝 검토(`docs/daemon/prior-table-pair-review.md`)가 경쟁이 있는 segment를 읽습니다. 2026-10-14에 window를 아직 규칙으로 적던 문서들(`dataset/README.md`의 Coresets 표와 "Rules of the tree", interpretation contract §7의 "Demand budget", `docs/background-guide.md` §5)도 2026-10-16–17에 이 이유와 함께 고쳐졌고(9.15), README는 이것을 "Demand is reported, not held"라는 규칙으로 적습니다.

## 12.4 job이 파일보다 오래 살 때

manifest의 숫자 중 눈에 띄게 큰 것이 둘 있습니다. `c2-p1a`의 14.505와 `c2-p2a`(그리고 `c2-p2a-idle`)의 9.3829입니다. CPU 하나의 14배를 원하는 파일이라니, 무슨 뜻일까요.

원인은 12.2절의 "수명 위에 고르게 펼치기" 규칙과 9.10 D17의 "job을 통째로 묶기"가 만나는 지점입니다. `c2-p1a`의 학습 job은 CPU 1,389.885 s를 원하는데, `depart`가 없으므로 compile 시점의 수명은 "도착 60 s부터 파일 끝 99.435 s까지" 39.435 s로 계산됩니다. 1,389.885 s를 39.435 s에 펼치면 그 구간에서만 CPU 35.2개어치이고, 편집기를 더하면 두 번째 segment의 utilization이 35.7721이 됩니다. 실제로는 이 job이 파일이 끝난 뒤에도 20분 넘게 더 돌았을 것이고, 파일 안에서 job이 CPU 하나보다 많이 받을 수는 없습니다. 이 숫자는 "얼마나 과부하인가"의 척도가 아니라 "job이 파일보다 훨씬 크다"는 신호입니다.

`c2-p1a`의 머리 주석이 이것을 설계로 적습니다. "the training runs on past the file's end (D80, D86)". 두 번째 segment의 길이는 짝 파일의 색인 job(39.435 s)에 맞췄고, 학습 job은 그 segment 내내 살아 있도록 통째로 묶었습니다.

이 숫자는 계산에서 잘라 내지 않고, 문장으로 범위를 밝히기로 했습니다(9.15의 work list, 2026-10-15). 문서들은 이것을 lane이 진 부하가 아니라 **offered demand**, 곧 job이 파일 끝까지의 수명 위에 내놓은 수요로 읽으라고 적습니다. `dataset/README.md`의 "Demand is reported, not held" 규칙은 "a batch job that outlives its file reads as offered demand above one lane, not as the lane's load"라고, building plan §5a는 "these figures are not read as oversubscription"이라고 적습니다.

## 12.5 compile report

9.18 이후 compiler는 artifact마다 report를 옆에 씁니다. `c1-office.report.json` 전체는 이렇습니다.

```json
{
  "demand_class": "calibration",
  "demand_us": 1617440,
  "duration_us": 60000000,
  "operations": {},
  "per_segment": [
    {"index": 0, "t_end_us": 60000000, "t_start_us": 0, "utilization": 0.026957333333333333}
  ],
  "per_task": {
    "browser": 176518, "mail": 80359,
    "renderers.1": 436, "renderers.2": 363, "renderers.3": 498, "renderers.4": 643,
    "writer": 1358623
  },
  "utilization": 0.026957333333333333
}
```

| key | 뜻 |
|---|---|
| `duration_us` | 파일 길이(2.6절) |
| `demand_us` | 모든 task의 demand 합계 |
| `utilization` | `demand_us ÷ duration_us`, 반올림하지 않음 |
| `per_task` | instance id(chain 구성원과 빌드 포함)별 demand |
| `per_segment` | segment별 utilization(12.2절) |
| `operations` | task id별로 operation의 `{name, at_us, duration_us}` 목록. operation이 없으면 `{}` |
| `demand_class` | timeline의 `meta.demand`(기본 `oversubscribed`) |
| `replay` | trace replay를 쓴 compile에서만. task별 stream과 offset(11.10절) |

report의 바이트 형태는 artifact와 다릅니다. `json.dumps(report, sort_keys=True, indent=2)`에 줄바꿈 하나입니다(`compile.py`의 `report_bytes`). 사람이 읽기 쉽게 들여쓰기를 했습니다.

> **왜 이렇게 정했나.** report를 파일로 남기고 manifest에 hash를 기록하는 것은 9.18의 결정 8입니다. "The compile report is a blessed artifact. The compiler writes each artifact's report beside it in `build/`, and the manifest pins the reports' hashes in a section of their own; the `demand` section is unchanged." 9.18 D3가 이전 상태를 적습니다. "the compile report (duration, demand per task and per segment, operations, replay) existed only in memory, its rounded extract under `demand`." operation의 실제 길이처럼 artifact만 봐서는 알기 어려운 정보가 compile이 끝나면 사라졌던 것입니다. 같은 결정이 test의 `coreset` fixture가 artifact와 report를 `build/`에서 읽게 해서(hash가 manifest와 맞을 때), test가 set 전체를 다시 compile하지 않아도 되게 했습니다.

## 12.6 manifest의 `demand` 기록

manifest의 `demand` section은 artifact 경로마다 report의 요약을 담습니다.

```json
"coreset-single/c2-p1a.workload.json": {
  "demand_class": "oversubscribed",
  "segments": [
    {"index": 0, "t_end_us": 60000000, "t_start_us": 0, "utilization": 0.5272},
    {"index": 1, "t_end_us": 99435000, "t_start_us": 60000000, "utilization": 35.7721}
  ],
  "utilization": 14.505
}
```

utilization은 소수 넷째 자리로 반올림합니다. tree의 manifest에서 `oversubscribed` 11개 파일의 utilization을 읽으면 이렇습니다.

| 파일 | 파일 utilization | segment별 |
|---|---|---|
| `c2-p1a` | 14.505 | 0.5272, 35.7721 |
| `c2-p1b` | 0.9238 | 0.5272, 1.5272 |
| `c2-p2a`, `c2-p2a-idle` | 9.3829 | 0.9651, 28.5251 |
| `c2-p2b` | 1.2706 | 0.9651, 1.9651 |
| `c2-p3a` | 0.4401 | 0.3893, 0.4515 |
| `c2-p3b` | 0.8975 | 0.3893, 1.0122 |
| `c3-creation` | 0.9417 | 0.0151, 0.0169, 1.0165 |
| `c3-evening` | 0.9006 | 0.0139, 1.5062, 0.1327 |
| `c3-workday` | 0.888 | 0.0031, 0.0053, 0.9597, 1.0251 |
| `c6-dual` | 0.8388 | 0.8388 |

`calibration` 40개 중에도 1.0을 넘는 파일이 많습니다. C7 counterpart는 원하지 않는 쪽의 job(indexing과 batch mode 넷의 다섯은 label만 바꾼 base 자신의 job)을 그 CPU 총량 C 길이의 파일에 통째로 묶으므로 그 job 하나가 lane 하나를 채우고 나머지 task가 그 위에 더해져 16개 모두 1.0을 넘고(`c7-idle` 1.0007부터 `c7-gaming` 1.9149까지), C1 calibration 묶음의 batch 파일은 job이 segment를 거의 채우도록 길이를 맞췄으므로 0.99대입니다(`c1-compile` 0.9982, `c1-transcode` 0.9993). 이것이 building-plan §5a가 "a timeline's demand class … says nothing about the file's compiled demand"라고 강조하는 이유입니다. class는 의도이고, 숫자는 결과입니다.

`c6-dual`의 utilization은 9.13 R5의 기록(1.00)과 지금 manifest(0.8388)가 다릅니다. 9.23 D7(2026-10-14)이 그 사이를 기록합니다. R5의 1.00은 0.9997을 반올림한 값으로, 읽은 시점에는 맞았습니다. 0.8388이 된 것은 9.17의 다시 bless 때입니다. 9.17 D1이 편집기의 타자를 12,068 s짜리 창 하나에서 686–688 s짜리 창 아홉 개로 나누었기 때문입니다(4.4절). `39d8d815` 전후로 다시 compile하면 편집기의 CPU는 3,460.4 s → 1,518.6 s, 키 입력 wake는 33,518 → 13,751이 되고, 빌드와 게임 chain은 그대로입니다. 그 차이 0.161 lane이 줄어든 전부입니다. 이 값을 읽는 소비자는 없습니다. demand window는 관문이 아니고(9.14 결정 4), `c6-dual`은 보고 파일이며, guard 면제는 이 파일의 label에 기댑니다.

---

# 13장 · Compile 안의 canonical lint와 manifest

compiler는 artifact를 쓰기 전에 그것을 검사합니다. 이 장은 그 검사(canonical lint)가 무엇을 보는지, 왜 compile 안에서 하는지, 그리고 compile의 마지막 산출물인 manifest가 무엇을 기록하는지를 다룹니다. 끝으로 2026-10-11에 compile 시간을 24분에서 52초로 줄인 두 변화(`jsonschema-rs`와 파일별 병렬)를 봅니다.

## 13.1 왜 lint가 compile 안에 있나

lint에는 두 종류가 있습니다. timeline과 library를 보는 lint는 compile **전에** 할 수 있습니다(14장). 하지만 canonical 파일을 보는 lint는 canonical 파일이 있어야 합니다. 그래서 compiler가 artifact 하나를 만들 때마다 바로 검사하고, 하나라도 걸리면 아무것도 쓰지 않고 실패합니다(9.2절의 "전부 아니면 전무").

> **왜 이렇게 정했나.** 원래 `make lint`도 모든 timeline을 메모리에서 다시 compile해 canonical lint를 돌렸습니다. 9.22 D2(2026-10-11)가 이것을 없앴습니다. 기록된 이유는 중복입니다. "the compile already runs the same `lint_canonical` with the same arguments on every artifact it writes and fails on an error, so the pass repeated the build's check." 9.22의 결정 2는 역할을 이렇게 나눕니다. "`make lint` is the repo, timeline and bound-value lints alone. The canonical lints are the compiler's, run on every artifact as it is built." 그 결과 `make lint`는 약 42분에서 0.8초가 되었습니다(9.22 changelog의 "After" 표, M1 Pro).

## 13.2 `lint_canonical`이 보는 것

`dataset/tools/wlc/linter.py`의 `lint_canonical(canonical, schema, …)`은 오류 문자열의 목록을 돌려줍니다. 검사는 이 순서입니다.

**1. schema 검증.** canonical dict를 workload schema로 검증합니다. 오류가 하나라도 있으면 `schema: <메시지> at <위치>` 모양으로 모아 **곧바로 돌려줍니다.** 코드 주석이 이유를 적습니다. "structural failures make the rest unreliable", 모양이 틀린 파일에 뒤의 검사를 돌리면 엉뚱한 오류가 쏟아지기 때문입니다.

**2. event 정렬.** `events`의 `t`가 오름차순인지 봅니다("events not sorted by t").

**3. task id의 유일성.** 모든 arrive event의 `id`와 모든 spawn table 항목의 `id`를 한데 모아 중복을 찾습니다. top-level task와 자식이 같은 id를 가져도 안 됩니다.

**4. TIMER first.** arrive event와 spawn table 항목 하나하나의 program에 대해, TIMER가 어딘가에 있다면 **처음 실행되는 명령어**가 TIMER여야 합니다. "처음 실행되는 명령어"는 program의 첫 명령어이되, 그것이 LOOP면 LOOP의 몸통으로 내려가 다시 첫 명령어를 봅니다(`_first_executed`). 위반하면 "TIMER is not the first executed instruction — the program opens with RUN, so TIMER's t₀ would not be the arrival (9.11 D11)" 같은 오류를 냅니다.

**5. FORK와 spawn table의 짝.** program에 FORK가 있는데 spawn table이 없으면 오류, spawn table이 있는데 FORK가 없으면 오류, FORK 수가 table 항목 수보다 많으면 오류입니다. FORK가 항목보다 적은 것은 허용됩니다.

**6. wake event의 해소.** wake event마다 `target`이 알려진 task(top-level이든 자식이든)이고, 그 task의 program이 그 `channel`에서 WAIT하는지 봅니다. 아무도 기다리지 않는 channel로 깨우면 "wake channel … never awaited by …" 오류입니다.

**7. WAKE 명령어의 해소.** 모든 program(top-level task와 spawn table의 자식 모두)에 있는 `WAKE`의 `target`이 알려진 task인지 봅니다. 2026-10-15 전에는 top-level task의 program만 훑었습니다(9.23 D14).

**8. 이름의 길이.** 모든 이름(top-level과 자식)이 15자 안인지 봅니다(`COMM_LIMIT = 15`, 커널의 `TASK_COMM_LEN` 16에서 끝 문자를 뺀 값, `linux-sched-h`). 3.6절의 이름 규칙을 core set에서도 lint로 지킵니다(9.23 D14).

**9. program의 끝.** 박힌 퇴장이 없는 task(top-level과 자식)는 `EXIT`로 끝나야 하고, segment-bound task는 `WAIT`, `TIMER`, unbounded `LOOP` 중 하나로 끝나야 합니다(`_end_violation`). schema의 `program` 설명이 lint에 맡긴 규칙(7.10절)과, 어떤 program도 퇴장 전에 바닥나지 않는다는 9.23 D16의 규칙을 함께 지킵니다. 7–9번을 더하기 전에 1,691개 artifact(core 51, variant 78, generated 1,562)를 읽어 보니, 자식 program의 `WAKE` 855,150개는 모두 알려진 task를 가리켰고, 15자를 넘는 이름은 없었고, finite top-level task 1,569개와 자식 341,422개는 모두 `EXIT`로 끝났습니다(9.23 D14). 9번의 segment-bound 쪽은 지켜지지 않았습니다. 9.23 D16은 할 일이 퇴장 전에 바닥나는 segment-bound program 7,400개를 찾았습니다. core set과 variant에서 240개로 129개 파일 모두에 있었고, generated layer에서 7,160개였습니다. 그중 6,960개는 `RUN`으로 끝나 9번이 거절하는 모양이었고, compiler가 그 끝에 `WAIT`(6,215개)이나 `TIMER`(745개)를 붙이게 되었습니다(11.1절, 11.5절). 나머지 440개는 한 번도 깨어나지 않는 `WAIT` 하나뿐인 program이라 그대로입니다.

**10. focus의 규칙.** focus 구간마다 `task`가 top-level arrive event의 id이고, `t_start < t_end`이고, 그 task의 박힌 수명 안(도착 `t` 이후, `depart`가 있으면 그 이전)인지 봅니다. 구간들이 `t_start` 순으로 정렬되어 있고 서로 겹치지 않는지도 봅니다.

loader(2–4장)가 이미 timeline 단계에서 비슷한 규칙을 검사했는데 왜 canonical에서 또 검사할까요. loader는 사람이 쓴 것을 검사하고, canonical lint는 compiler가 만든 것을 검사합니다. 예를 들어 focus의 task는 timeline에서는 `game`이었지만 canonical에서는 compiler가 고른 `game.chain.1`입니다. compiler의 실수(잘못된 주인 id, 정렬 실수, 채널 이름 오타)는 canonical lint만 잡을 수 있습니다.

> **왜 이렇게 정했나.** TIMER first 규칙은 9.13의 결정 8(2026-10-09)이고, 근거는 9.11 D11과 D33입니다. simulator 담당자의 기록(9.11 D11이 인용하는 simulator의 결정 D4)은 TIMER의 t₀를 "그 task가 TIMER를 처음 실행한 순간"으로 정했습니다. harness는 t₀를 도착 시각으로 읽고 있었습니다. 둘이 같아지려면 TIMER가 첫 명령어여야 합니다. `_dev/TODO.md`의 9.13 줄은 이유를 "so TIMER's t₀, its first TIMER execution, is the task's arrival"로 적고, 코드 주석은 "the two cannot come apart silently"라고 적습니다. 9.11 D33은 "첫 명령어"를 "첫 **실행되는** 명령어"로 다듬었습니다. 게임 chain의 머리는 LOOP로 시작하고 그 몸통이 TIMER로 시작하므로, "program이 TIMER로 시작한다"를 글자 그대로 읽으면 머리가 위반이 되기 때문입니다.

tree의 core set에서 TIMER를 가진 task는 23개이고 모두 이 규칙을 지킵니다. 8개는 LOOP 머리를 거쳐(chain 머리), 15개는 글자 그대로(재생기와 통화)입니다(이 권을 쓰며 51개 artifact를 모두 읽어 셌습니다). 9.13 reads R2는 2026-10-09에 22개(LOOP 7, 글자 그대로 15)라고 기록했는데, 그 뒤 `c2-p2a-idle`이 chain 머리 하나를 더했습니다.

`t₀` — TIMER 격자의 기준 시각입니다. task는 t₀ + k·period마다 깨어납니다. `9.11` — Phase 9의 sub-task로, scheduler 쪽 상수와 근거(declared class, TIMER 규칙 등)를 조사한 연구 slice입니다.

## 13.3 lint가 보지 않는 것

canonical lint에 빠진 검사도 알아 둘 만합니다. 코드를 읽어 확인한 것들입니다.

- **`children:<id>` channel을 누가 깨우는가.** 7.7절에서 본 대로 이 channel에는 wake event가 없고, lint는 "기다리는데 아무도 깨우지 않는 channel"을 찾지 않습니다. 검사하는 것은 반대 방향(깨우는데 아무도 기다리지 않는 channel)뿐입니다. 이 channel은 executor가 완료하도록 제안되어 있습니다(7.7절).
- **demand의 범위.** 2026-10-09 이후로 없습니다(12.3절).

`lint_canonical`은 `report`와 `mode` 인자를 받지만 지금은 쓰지 않습니다. window 검사가 있던 시절의 흔적입니다.

## 13.4 schema 검증과 `jsonschema-rs`

1번 검사의 schema 검증은 Rust로 쓴 `jsonschema-rs` library로 합니다. schema 하나를 process마다 한 번만 compile해서 cache합니다(`_validator`).

> **왜 이렇게 정했나.** 9.22의 결정 3(2026-10-11)입니다. "The canonical lint validates against the unchanged workload schema with `jsonschema-rs`, a dependency of the dataset tools. The schema and the validation's meaning do not change." 9.22 D3이 측정을 기록합니다. 95 MB짜리 `c7-transcode` 하나를 검증하는 데 Python `jsonschema`는 141 s, `fastjsonschema`는 19.7 s, `jsonschema-rs`는 1.4 s가 걸렸고, 일부러 망가뜨린 event를 셋 다 잡았습니다. `fastjsonschema`는 draft-07 package라서 이 schema(2020-12)를 통과시키긴 했지만 "outside its stated support"였습니다. 9.18 D7은 그 전의 속도를 "about 0.6 MB/s — `c6-dual` 187.6 MB in 335 s"로 기록했고, 51개 파일 678 MB를 검증하는 데 compile 시간의 대부분이 들었습니다. `dataset/tools/requirements.txt`의 `jsonschema>=4.20`이 `jsonschema-rs>=0.29`로 바뀌었습니다.

2026-10-15부터 `dataset/tools/requirements.txt`는 version을 정확히 고정합니다(`PyYAML==6.0.1`, `jsonschema-rs==0.29.1`, `pytest==8.3.4`, `numpy==1.26.4`; 9.23 D15). `dataset/README.md`의 Commands 절은 "Needs Python 3.12 … with `pip install -r tools/requirements.txt` (PyYAML, jsonschema-rs, pytest, numpy, each at the exact version it names)"라고 적습니다(10.6절).

## 13.5 manifest: 무엇을 고정하나

compile의 마지막 산출물은 `dataset/build.manifest.json`입니다. git에 commit하는 것은 이 파일이고, `build/`의 artifact는 commit하지 않습니다(10.1절). manifest는 네 section을 가집니다.

| section | 내용 | tree의 항목 수 |
|---|---|---|
| `inputs` | compile이 timeline 말고 읽는 파일들의 SHA-256 | 33 |
| `artifacts` | `coreset-single/<id>.workload.json`마다 바이트의 SHA-256 | 51 |
| `reports` | `coreset-single/<id>.report.json`마다 바이트의 SHA-256 | 51 |
| `demand` | artifact마다 `demand_class`, `utilization`, `segments`(12.6절) | 51 |

`inputs`의 33개는 `compile.py`의 `input_files`가 정합니다. `dataset/archetypes.yaml`, `dataset/schema/workload.schema.json`, `dataset/tools/compile.py`, `dataset/tools/wlc/*.py` 11개, `dataset/stimulus/*.jsonl` 3개, `dataset/launch/*.json.gz` 10개, `dataset/replay/*.json.gz` 6개입니다(manifest의 key를 세어 확인했습니다). launch stream 열 개는 2026-10-15에 더해졌습니다(아래). timeline 파일 자체는 `inputs`에 없습니다. timeline은 각 artifact의 `meta.derived_from`에 blob hash로 박혀 있으므로, timeline이 바뀌면 artifact hash가 바뀝니다.

> **왜 이렇게 정했나.** `inputs`가 compiler 소스와 stream까지 고정하게 된 것은 9.18의 결정 5입니다. 2026-10-10 audit의 A4가 이전 상태를 적었습니다. "`build.manifest.json.inputs` pins archetypes and schema only …, streams and compiler unpinned (drift detected via artifact hashes, not attributed)." compiler나 stream이 바뀌면 artifact hash가 바뀌어 drift는 잡히지만, **무엇 때문에** 바뀌었는지는 알 수 없었다는 뜻입니다. `inputs`에 고정하면 manifest diff가 원인을 보여 줍니다.

이 고정에는 대가가 있습니다. `wlc/*.py`의 한 글자만 바꿔도 manifest의 `inputs`가 바뀌고, 그것을 입력으로 고정하는 variant manifest가 바뀌고, 그것들을 고정하는 RQ0 gate spec의 pin이 바뀝니다. 9.22 D5는 compiler 파일 셋을 고친 뒤 "every artifact, report and variant is byte-identical to the 9.18 build (the diff of the two manifests against `HEAD` is the `inputs` section alone)"라고 기록하면서도 두 manifest를 다시 bless하고 gate spec을 다시 pin했습니다. 9.21 D2는 이 대가를 피하려고 generated layer의 coverage 계산을 `wlc`가 아니라 generator 옆(`dataset/tools/gen/coverage.py`)에 두었습니다. "the core set's manifest pins `wlc/*.py` by content … any edit there moves the core manifest and, through it, the variants manifest and the RQ0 gate spec's dataset pin."

> **왜 이렇게 정했나.** 2026-10-14까지는 compiler가 읽는 파일 가운데 launch phase stream `dataset/launch/*.json.gz`(10개)가 `inputs`에 없었습니다. compiler의 `_load_launch`가 이 파일들을 읽어 중간에 시작하는 앱의 launch phase를 재생하는데(11.3절), `input_files`는 `stimulus/*.jsonl`과 `replay/*.json.gz`만 나열했고, 9.18의 결정 5도 "the stimulus and replay streams"만 적었습니다. 그래서 launch 파일이 바뀌면 그 파일을 쓰는 artifact의 hash만 바뀌고 `make check`는 통과해, audit A4가 고치려던 "not attributed" 상태가 launch stream에 남아 있었습니다. 9.23 D11(2026-10-15)이 `input_files`에 `launch/*.json.gz`를 더해, core manifest의 `inputs`가 33개, generated set의 manifest마다 55개(전에는 45개)가 되었습니다. test `test_every_stream_directory_the_tools_open_is_pinned`는 compiler와 linter가 여는 stream 파일이 모두 고정되어 있는지 봅니다. `dataset/README.md`가 manifest의 inputs를 "(library, schema, compiler sources, streams)"라고 묶어 적는 것도 이제 맞습니다.

**`reports` section의 key.** 각 report의 key는 report 자신의 경로(`coreset-single/c1-office.report.json`)입니다. 9.18 D6이 기록한 사고가 있습니다. 처음 구현은 report hash를 **artifact** 경로로 key를 지어서, `check_build`가 두 section을 합칠 때 report hash가 artifact hash를 덮어썼고, 첫 `check_build` 실행이 "102 errors"로 실패했습니다. 지금 코드는 `report_path(rel)`로 key를 만듭니다.

## 13.6 `--jobs`: 파일마다 worker 하나

`compile.py`는 timeline 하나를 worker process 하나에 맡깁니다. `--jobs N`으로 worker 수를 정하고, 기본값은 CPU 수입니다. worker마다 library와 schema를 한 번 읽어 cache합니다(`_PER_PROCESS`).

병렬로 돌려도 결과가 같은 이유는 `compile_one`이 입력만으로 결과가 정해지는 순수 함수이기 때문입니다. docstring은 "Pure in its inputs, so the timelines compile in parallel (9.22) and in any order; the manifest sorts"라고 적습니다. 결과가 어떤 순서로 돌아오든, manifest의 dict는 경로로 정렬해서 쓰므로 바이트가 순차 실행과 같습니다. 10장의 keyed sampling 덕분에 한 파일의 compile은 다른 파일의 compile과 어떤 상태도 공유하지 않습니다.

> **왜 이렇게 정했나.** 9.22 D4(2026-10-11)입니다. "`build_all` maps it over a `ProcessPoolExecutor` of `--jobs` workers (default the CPU count) and sorts the results, so the manifest bytes are those of the serial build." 배경은 9.18의 Linux 검증 실행이었습니다. 그때의 도구로는 CI의 `lint`, `dataset`, `test`, `check`가 저마다 set 전체를 compile해서 집 기계 기준으로 한 번 도는 데 약 3.5시간이 걸렸고, 4 vCPU runner에서는 GitHub의 job 시간 제한 6시간을 넘을 것이 분명해서 첫 실행(run 38129714928)을 23분 만에 인지오가 취소했습니다(9.18 D7, 9.22 D6).

9.22 changelog의 "After" 표가 효과를 기록합니다(M1 Pro, 10 core, Python 3.12).

| 단계 | 이전 | 이후 |
|---|---|---|
| `make lint` | 약 42분 | 0.8 s |
| `make dataset` | 22–24분 | 52 s |
| `make variants` | 33–35분 | 1분 46 s |
| `make test` | 44분 | 2분 01 s |
| `make check` | 56–59분 | 1.7 s |

`make dataset`의 24분 중 18분이 schema 검증이었고(9.18 D7의 측정), `jsonschema-rs`가 그것을 없앴습니다. 남은 약 6분의 계산을 10개 core의 pool이 52초로 줄였습니다. CI의 4 vCPU Linux runner에서는 `dataset` 단계가 1분 34초였습니다(run 38131040159).

## 13.7 `--check`와 build gate

`compile.py --check`는 artifact를 쓰지 않고 메모리에서 다시 compile해, 만들어질 manifest의 바이트가 commit된 manifest와 같은지만 봅니다. 9.22 전에는 `make check`가 이것을 불렀습니다. 9.22의 결정 1 이후로는 build 단계(`make dataset variants generated`)가 manifest를 다시 쓰고, `make check`는 compile하지 않고 비교만 합니다. `dataset/tools/check_build.py`가 두 가지를 봅니다. 디스크의 manifest 각각과 build 단계가 다시 쓰는 다른 파일(variant recipe가 이름을 대는 파생 timeline 전부와 `coverage-grid.json`)이 `git show HEAD:<path>`로 읽은 commit된 바이트와 같은가, 그리고 `dataset/build/`의 파일이 모든 manifest의 합집합과 정확히 같은가(고정된 파일은 모두 있고 hash가 맞으며, 어느 manifest에도 없는 파일은 없음)입니다. 파생 timeline과 grid를 비교하는 부분은 9.23 D12(2026-10-15)가 더했습니다. 그 전에는 `make dataset`이 다시 쓰고 commit하지 않은 파생 timeline이 `make check`를 통과했고, 그 artifact의 `derived_from`이 git에 없는 blob을 가리킬 수 있었습니다. 9.22의 결정 1은 "The build step proves reproducibility; `check` compares"라고 요약합니다. `--check` 옵션은 "independent verification"용으로 남았지만 gate에서는 빠졌습니다. build gate와 CI의 운영 전체는 그 주제를 다루는 권에서 설명합니다.

---

# 14장 · Compile 전의 lint

`make lint`는 compile하기 전에 돌리는 검사입니다. 아무 파일도 쓰지 않고, 2026-10-11 이후로는 1초 안팎이면 끝납니다(9.22 기록: 집 기계 0.8 s, CI 1 s). 이 장은 `dataset/tools/lint.py`가 무엇을 검사하는지, 그리고 그중 timeline의 묶인 값(`bind`, `count`)의 출처를 보는 lint가 어떻게 생겼는지를 다룹니다.

## 14.1 `lint.py`의 흐름

`lint.py`의 `run`은 다섯 가지를 차례로 합니다.

1. **repo lint**(`lint_repo`) — archetype library와 출처 registry를 검사합니다.
2. timeline 하나하나에 대해:
   1. **bound-value source lint**(`lint_bound_sources`) — 묶인 값마다 출처가 있는지.
   2. **timeline lint** — `Timeline(path, library)`를 불러 loader의 구조 검사(2–4장)를 그대로 돌립니다.
3. **grid lint**(`lint_grids`) — generated layer의 정의 파일 `dataset/grids.yaml`을 검사합니다.
4. **release map lint**(`lint_releases`) — library, timeline, variant recipe, `grids.yaml`이 인용하는 `meas-ci:<workflow>:<campaign>` tag마다, 그 campaign의 원자료를 담은 GitHub release가 `dataset/meas-releases.yaml`에 적혀 있는지(release tag, URL, asset마다의 sha256) 봅니다. 2026-10-16에 더해졌습니다(9.15).

오류가 없으면 "lint clean"을 찍고 0으로, 있으면 오류 목록을 찍고 1로 끝납니다. `--freeze`를 주면 출처 tag `meas-pending`(측정 대기 중이라는 자리표시)을 오류로 봅니다. `make lint`는 2026-10-15부터 `lint.py --freeze`로 돕니다(9.23 D13). 2026-10-16부터는 freeze가 library의 parameter뿐 아니라 timeline의 묶인 값에도 걸립니다(14.4절). 측정을 기다리는 값은 `meas-pending`을 달고 freeze가 그것을 거절하며, 따로 `placeholder` 같은 label은 없습니다.

`make lint`가 읽는 timeline은 `dataset/timelines/` 아래에 commit된 51개뿐입니다. generated layer의 timeline 1,562개는 commit하지 않으므로 `make lint`가 보지 않습니다. 대신 `tools/generate.py`가 그것을 만들 때 같은 source lint, loader 검사, 그리고 compile 안의 canonical lint를 돌립니다(`dataset/README.md`의 Generated layer 절).

## 14.2 repo lint: library와 registry

`lint_repo`는 timeline이 아니라 timeline이 기대는 두 파일을 봅니다. 이 권의 주제는 아니지만, timeline의 `source` 검사가 같은 함수(`_check_tag`)를 쓰므로 짧게 봅니다.

**registry는 references의 부분집합.** `dataset/sources.yaml`(출처 registry, tree에 19개. 2026-10-16에 어떤 dataset 파일도 값이나 구조를 끌어오지 않는 id 열하나를 뺐습니다)의 모든 id가 `docs/references.md`에 `### \`<id>\`` 제목으로 있어야 합니다. 2026-08-26 grill의 D5가 정한 구조입니다. `docs/references.md`가 모든 인용 문자열을 소유하고, yaml registry는 기계가 쓰는 field(`type`, `locator_pattern`, `notes`)만 가지며, 둘이 어긋나지 않게 "every yaml id must have a REFERENCES.md entry (subset lint, CI-checked)"라고 기록되어 있습니다.

**archetype entry의 필수 field.** `category_source`, `declared_class`, `pattern`, `params`, `lifetime`, `binding_params`, `scalable`, `validation_stats`, `modeling_notes` 아홉 개입니다. `lifetime`은 `segment-bound`, `finite`, `spawned` 중 하나, `declared_class`는 `normal`, `idle` 중 하나여야 하고, `spawned`면 `spawned_by`가 있어야 합니다.

**parameter마다 출처.** 모든 수치 parameter는 `source` tag를 가져야 하고, tag는 `_check_tag`를 통과해야 합니다. `_check_tag`의 규칙은 timeline에서도 똑같이 쓰입니다.

- tag의 모양은 `<id>` 또는 `<id>:<locator>`입니다(정규식 `([a-z0-9-]+)(?::(.+))?`).
- `<id>`가 registry에 있어야 합니다.
- locator가 있으면, 그 id의 registry 항목이 `locator_pattern`을 가져야 하고 locator가 그 정규식에 맞아야 합니다. pattern이 없는 id에 locator를 붙이면 오류입니다.

예를 들어 `meas-ci`의 pattern은 `^[a-z0-9_-]+:(\d+|\d{4}-\d{2}-\d{2}[a-z]?)$`이라서 `meas-ci:background:2026-10-02b`(workflow `background`, 2026-10-02에 시작한 두 번째 campaign)가 맞고, `lavd-ossna24`의 pattern은 `^s\d+$`이라서 `lavd-ossna24:s16`(16번 slide)이 맞습니다. `glam`은 pattern이 없으므로 locator 없이 `glam`으로만 씁니다.

> **왜 이렇게 정했나.** tag와 locator 검증은 2026-08-26 grill의 D3입니다. "Tags are `<source-id>:<locator>`; registry entries are keyed by bare source-id; each entry may carry an optional `locator_pattern` regex (e.g. `^s\d+$` for slide decks) that the linter validates full tags against. No pattern = bare-id tags only." task 2.3의 불변식 목록은 이것을 test 헌장에 넣었습니다. "Registry subset lint (every `dataset/sources.yaml` id in `docs/references.md`), provenance tags, locator patterns, `meas-pending` freeze gate — per building-plan §6."

**그 밖의 모양 검사.** `sampling`이 `per-instance`, `per-task`, `per-iteration` 중 하나인지, quantile table이 음이 아니고 줄지 않는 값 열 개인지, `min`·`max`·`means`가 셋 다 있거나 셋 다 없는지, `min`이 첫 percentile 이하이고 `max`가 마지막 percentile 이상인지, 구간 평균 열한 개가 각자 구간 안(반올림 여유 1 µs)에 있는지를 봅니다. component, operation, heavy event, stimulus, launch, replay param은 각자의 모양을 따로 검사하고, stimulus·launch·replay는 가리키는 파일이 `dataset/stimulus/`, `dataset/launch/`, `dataset/replay/`에 실제로 있는지도 봅니다.

## 14.3 timeline lint

timeline lint는 따로 구현된 것이 없습니다. `Timeline` 생성자를 부르고, `TimelineError`가 나면 그 메시지를 오류로 모읍니다(`lint_timeline`, 그리고 `lint.py`의 같은 동작). 즉 2–4장에서 본 loader의 규칙 전부가 timeline lint입니다. 정리하면 이렇습니다.

| 대상 | 규칙(장·절) |
|---|---|
| `meta` | `id`, `seed` 필수, `seed`는 정수, `demand`는 두 값 중 하나(2.2) |
| `segments` | 비어 있지 않음, `from < to`, `familiarity` 1–5, `background_wanted` 규칙, 겹치지 않음(2.4–2.5) |
| `tasks` | 필수 field, id 유일, archetype 존재, `bind` key = `binding_params`, spawned 금지, `depart` iff segment-bound, `count` 양의 정수, `depart > arrive`(3.1) |
| `input` | input channel 있는 task, 수명 안, 겹치지 않음, `slice_of`의 모양과 포함 관계(4.2–4.3) |
| `focus` | 필수, `count` 1인 task, 수명 안, 겹치지 않음, 모든 입력 창을 감쌈(4.4) |
| `operations` | 그 archetype의 operation 이름, 수명 안(4.5) |

loader는 첫 오류에서 멈춥니다(예외를 던지므로). 그래서 한 timeline에 오류가 여러 개 있으면 `make lint`는 첫 번째 것만 보여 주고, 고친 뒤 다시 돌려야 다음 것이 보입니다. repo lint와 source lint는 오류를 모두 모아 보여 줍니다.

## 14.4 bound-value source lint

`lint_bound_sources(path, registry, freeze)`는 timeline 파일을 **loader를 거치지 않고** YAML 그대로 읽어 task마다 다음을 봅니다.

1. 묶인 값의 집합을 만듭니다. `bind`의 key 전부, 그리고 task에 `count` key가 **적혀 있으면** `count`.
2. `source`가 없는데 묶인 값이 있으면 "bound values [...] carry no source map" 오류입니다. 묶인 값이 없으면 `source`가 없어도 됩니다.
3. `source`가 map이 아니면 오류입니다.
4. 묶인 값 중 `source`에 없는 것("have no source entry"), `source`에 있지만 묶인 값이 아닌 것("name no bound value")을 양방향으로 찾습니다.
5. 짝이 맞는 key마다 값을 봅니다. 목록이면 각 원소를, 아니면 그 값 하나를 봅니다. 빈 목록은 오류입니다. 문자열이 아니면 오류입니다. `design`, `convention`, `arithmetic` 중 하나면 label이고, 목록 안에 있으면 "a label stands alone" 오류입니다. 그 밖의 문자열은 `_check_tag`로 registry 검사를 합니다.
6. `freeze`면(`make lint`) `meas-pending` tag를 "meas-pending after freeze" 오류로 봅니다. 2026-10-16에 더해졌습니다(9.15). 그 전에는 freeze 검사가 library의 parameter에만 있어서, 묶인 값에 단 `meas-pending`은 통과했습니다.

YAML 그대로 읽기 때문에 생기는 성질이 하나 있습니다. `count: 1`을 굳이 적으면 그것도 묶인 값이 되어 출처가 필요합니다. loader는 `count`가 없으면 1로 보지만, lint는 "적었는가"를 봅니다. "값을 적었다면 그 값의 이유도 적어라"는 규칙이므로 자연스럽습니다.

> **왜 이렇게 정했나.** 3.5절에서 본 것처럼 9.10 D32가 규칙을 정했고(2026-10-01), 9.18의 결정 4가 field와 lint를 구현했습니다(2026-10-11). 결정 4는 처음에 `bind`만 말했다가 구현하면서 `count`를 더했습니다. 9.18 D2의 기록. "The spec's decision 4 is amended to name `count` among the bound values, as D32 does." 같은 기록이 이 lint의 한계를 9.16(종료 감사)에 넘깁니다. "`bound-values.md` and the timelines' `source` maps agree entry for entry (the lint checks form, not that each tag is the right ground)." lint는 tag가 registry에 있는지는 보지만, 그 출처가 정말 그 값을 받치는지는 보지 못합니다. 그것은 사람이 감사할 일입니다. 9.16이 2026-10-17에 이 감사를 했습니다. core timeline의 `source` map을 `bound-values.md`와 양방향으로 대조해 77개 항목의 tag와 값이 모두 일치했고(`_dev/research/jioh/task-9.16-exit-audits/handed/checks.md`의 9.18 decision 6 항목), dataset 쪽 claim audit이 tag를 slice의 읽기 기록과 대조한 결과 `parallelism_cap` 8의 꼬리표가 `design`에서 `convention`으로 바뀌었습니다(9.6 D4, compile slice가 `-j`와 cap을 정하면서 붙인 꼬리표; 같은 폴더의 `claims/dataset-findings.md` D-F3-08과 `decisions.md`).

이 lint의 test는 네 개입니다(`dataset/tools/tests/test_lint.py`). `test_real_timelines_bound_values_are_sourced`는 tree의 모든 timeline이 깨끗한지, `test_bound_values_carry_a_source_tag_or_a_label`은 13가지 경우(빠진 key, 남는 key, 목록 안의 label, registry에 없는 id 등)를 보고, 2026-10-16에 더한 `test_freeze_rejects_a_bound_value_tagged_meas_pending`과 `test_real_timelines_are_freeze_clean`이 freeze를 봅니다.

## 14.5 grid lint

`lint_grids`(`dataset/tools/gen/cells.py`)는 generated layer의 정의 파일을 봅니다. 정의의 모양, 각 구간 값의 출처(묶인 값과 같은 규칙: tag 또는 label), 그리고 정의가 정하는 모든 process 이름이 `comm_limit`(15자, 출처 `linux-sched-h`) 안인지입니다. generated layer는 그 주제를 다루는 권에서 설명합니다. 이 권에서 기억할 것은 하나입니다. 15자 제한은 여기와, 2026-10-15부터는 compile 안의 canonical lint(13.2절의 8번) 두 곳에서 lint됩니다(3.6절).

## 14.6 lint가 맡지 않는 것

`make lint`만 통과했다고 build가 통과하는 것은 아닙니다. 다음은 다른 단계가 맡습니다.

| 검사 | 맡는 곳 |
|---|---|
| segment의 `mode`가 메뉴 열여섯 개나 `ambiguous`인가 | `derive.py`의 coverage grid(`GridError`), 즉 `make dataset`과 `make check` |
| driver table 32칸이 모두 채워졌나 | `derive.py --require-coverage`, 즉 `make check` |
| 파생 파일이 recipe와 같은가 | `derive.py --check`, 즉 `make check` |
| canonical 파일의 schema와 구조 | compile 안의 `lint_canonical`, 즉 `make dataset` |
| 다시 build한 결과(manifest, 파생 timeline, `coverage-grid.json`)가 commit된 byte와 같은가 | `check_build.py`, 즉 `make check` |

CI(`.github/workflows/dataset.yml`)는 이 모두를 `lint` → `dataset` → `variants` → `generated` → `test` → `check` 순서로 돌립니다(`dataset/README.md`). 한 단계라도 실패하면 빨간불입니다.

---

# 15장 · 포맷이 지금 모양이 되기까지

앞 장들은 지금의 포맷과 compiler를 설명하면서 그때그때 결정의 기록을 인용했습니다. 이 장은 그 결정들을 시간 순으로 다시 놓습니다. 왜 이런 모양이 되었는지를 한 줄기로 보면, 지금 남아 있는 낡은 문서(16장)가 어느 시점의 모습을 적고 있는지도 알아볼 수 있습니다.

먼저 기록의 공백 하나를 밝혀 둡니다. 2026-08-28의 archive(`_dev/archive/2026-08-28-task-2.5-repo-prep-and-contracts.md`)는 "Still owed" 절에 이렇게 적습니다. "Archive docs for the 2026-08-27 sessions (phase-2 grill Q1–Q7; task-2.3 format grill) and pre-2.5 2026-08-28 sessions (2.6 grill; 2.4 grill; batch-tag supersession; grid sign-off) — their rationale lives only in those conversations and was not recoverable from this session." 즉 task 2.3과 2.4의 결정은 spec 파일에 결정문으로 남아 있지만, 결정을 내린 대화의 이유는 archive로 남지 않았습니다. 2026-10-16에 인지오가 남은 기억으로 그 이유를 archive로 썼습니다(`_dev/archive/2026-08-27-phase-2-grills-rationales.md`. 대화 기록 자체는 남아 있지 않습니다). 되찾은 이유는 셋입니다. task 2.4 결정 4의 seed 거절(5.4절), task 2.4 결정 3의 길이(design), task 2.3 결정 6의 lockfile 패턴입니다. 나머지는 결정문이나 다른 기록이 이유를 적거나, 뒤의 결정이 대체했거나, 일의 진행에 관한 결정이었다고 그 archive는 적습니다. 아래에서 이유가 어디에도 없는 것은 "따로 적힌 이유는 없습니다"로 적습니다.

## 15.1 한눈에 보는 연표

| 날짜 | 무엇이 바뀌었나 | 어디에 기록되었나 |
|---|---|---|
| 2026-08-26 | timeline이라는 이름, 지배 원칙, lifetime 분류, FORK와 TIMER, `{arrive, wake}` 두 op, CPU 하나, demand 규칙, 네 release artifact | workload-generation grill D9–D16 |
| 2026-08-27 | timeline 포맷(세 track), keyed sampling, lockfile, demand window 관문, 불변식 test | task 2.3 spec |
| 2026-08-28 | recipe와 deriver, seed 상속, demand class 관례, 첫 core set 24파일 × 2 mode | task 2.4 spec, Phase 2 |
| 2026-09-06 | manifest에 demand 기록, `background_wanted` lint, run file과 projection 동결 | Phase 3 |
| 2026-09-08 | `familiarity`를 canonical로 | Phase 5 |
| 2026-09-09/10 | 파생 파일의 `calibration`을 recipe에 명시, 32칸 coverage, `pre_committed_miss`, 50파일 | Phase 7 |
| 2026-09-13 | 게임 chain만 남김, `wineserver`를 chain 구성원으로 | 9.4 D3, D4 |
| 2026-09-14–26 | 측정된 archetype, quantile table, 키 입력 재생, timer channel, periodic job, forward recurrence | 9.5 D9, D17, D18, D74, D75, D77 |
| 2026-09-16 | native set을 내보내지 않기로 결정 | 9.5 follow-ups spec 결정 14 |
| 2026-09-19 | object job을 자식 여섯으로, `fork_cap` × 6 | 9.6 D19, D20 |
| 2026-10-01– | job을 통째로, launch phase, comm 이름, `member_names`, 묶인 값의 출처 규칙, `set-input`·`set-operations` | 9.10 D17, D21, D25, D26, D32, D44 |
| 2026-10-07 | TIMER backlog → skip 규칙 | memo 2026-10-07 |
| 2026-10-08 | declared scheduling class 제안 | memo 2026-10-08 |
| 2026-10-09 | native mode 삭제, `declared_class`, TIMER-first lint, `c2-p2a-idle`, bless | 9.13 |
| 2026-10-09 | demand window가 관문에서 물러남, segment별 demand, variant 변환, trace replay | 9.14 |
| 2026-10-11 | `input`과 `focus` 두 track, canonical의 네 번째 key | 9.17 |
| 2026-10-11 | `slice_of`, `source` map, manifest의 inputs와 reports, `check_build` | 9.18 |
| 2026-10-11 | lint를 compile 전 검사로, `jsonschema-rs`, 파일별 병렬, `check`는 비교만 | 9.22 |
| 2026-10-11–13 | generated layer가 같은 compiler를 씀 | 9.19–9.21 |
| 2026-10-14–15 | `c6-fold`·`c6-spoof`의 pre-committed miss, launch stream 고정, `check`의 파생 파일 비교, canonical lint 셋, 의존성 고정, program의 끝 | 9.23 |
| 2026-10-16 | 닿지 않는 compiler 경로 삭제, 묶인 값의 freeze, release 지도 lint, 머리 주석의 생략 문장 | 9.15 |

## 15.2 2026-08-26: 원칙이 정해진 날

simulator가 아직 없던 2026-08-26, workload-generation grill이 이 dataset의 뼈대를 정했습니다(`_dev/archive/2026-08-26-workload-generation-grill.md`). 포맷과 관련된 결정만 옮깁니다.

- **D9, timeline.** 입력 파일을 timeline이라고 부르고, 파이프라인을 `archetypes.yaml + timeline (+ scenario catalog) + seed → workload`로 정했습니다. 이유는 1.1절에서 본 "one compile path".
- **D10, lifetime.** 사용자가 닫는 task만 `depart`를 박고, 나머지는 `EXIT`로 끝납니다. 기각된 대안은 "fully pinned arrive+depart trace"(1.2절).
- **D11, FORK.** spawn table은 compile 때 미리 쓰고, 자식이 태어나는 시각은 run time에 정합니다. 기각된 대안은 compile 때 자식을 펼치는 것(1.2절).
- **D12, 지배 원칙.** "compile time resolves all randomness; run time resolves all timing that scheduling can influence." 결정문 자체가 "write into the format spec verbatim"을 요구했고, contract §2에 그대로 들어갔습니다.
- **D13, 절대 시각.** 주기적 task에는 TIMER, 입력에는 미리 박은 `{t, op: wake, target}` event, 그리고 op 집합을 `{arrive, wake}`로 닫았습니다. 기각된 대안과 이유가 기록되어 있습니다. "Relative-SLEEP encoding rejected: it drifts, systematically underloading the machine exactly under bad configs (biases Layer 2 toward 'bad configs aren't so bad')." SLEEP 반복으로 주기를 흉내 내면, 나쁜 설정 아래에서 task가 늦게 깨어날수록 다음 주기도 밀려서 수요가 저절로 줄어들고, 나쁜 설정이 실제보다 덜 나빠 보인다는 뜻입니다.
- **D14, 계약이 먼저.** "contract first, implementation second." interpretation contract는 simulator보다 먼저 쓰였습니다.
- **D15, CPU 하나와 demand 규칙.** 12.3절.
- **D16, 네 release artifact.** timeline set 둘(core, general) × compile mode 둘(`-native`, `-single`). `-native`는 측정 그대로, `-single`은 lane scaling을 한 것. 실험은 `-single`로만 하고, `-native`는 "released for reuse with an explicit unexecuted-status line"이었습니다. CI 불변식은 "variants of one timeline differ only in declared-scalable fields"였습니다.

## 15.3 Phase 2: compiler가 처음 생긴 날들

**task 2.3(2026-08-27).** spec(`_dev/docs/spec/jioh/task-2.3-timeline-compiler.md`)의 결정 일곱 개가 포맷의 첫 모양입니다.

1. timeline은 `meta`와 세 track(`segments`, `tasks`, `focus`). 이유: "The split mirrors the canonical `ground_truth`/`events` separation." 이때의 `focus`는 키 입력 창이었습니다.
2. task의 field(`id`, `name`, `archetype`, `arrive`, `depart` iff segment-bound, `bind`는 `binding_params`로 제한, `count`), 사람용 시간 문자열. 이 결정에 따로 적힌 이유는 없습니다(`bind` 제한의 근거는 3.3절의 building-plan §1).
3. `focus`(지금의 `input`)는 겹치지 않는 창의 목록이고, compiler가 "the focused task's archetype gap distribution"에서 입력 wake를 뽑는다. 지금은 분포가 아니라 기록을 재생합니다(9.5 D18). 이 결정에 따로 적힌 이유는 없습니다.
4. segment의 `scenario`는 compiler가 무시하고 linter가 읽는다. 따로 적힌 이유는 없습니다.
5. seed는 timeline의 `meta`에, 추출은 keyed substream으로. 이유는 10.2절.
6. build 산출물은 lockfile 패턴(gitignore한 `build/`와 commit한 hash manifest). 이유는 2026-10-16의 archive가 되찾았습니다. build는 입력(timeline, library, stream, compiler)에서 byte 그대로 다시 만들어지는 파생물이라 저장소에 두지 않고, lockfile이 설치된 tree 대신 hash로 의존성을 고정하듯 commit한 manifest가 build가 내야 할 것을 hash로 고정하며, CI가 다시 build해 비교한다는 것입니다. README도 같은 원리를 "That determinism is load-bearing … which is why `build/` isn't committed"로 적습니다.
7. demand window 관문. 12.3절.

**task 2.4(2026-08-28).** spec(`_dev/docs/spec/jioh/task-2.4-core-timelines.md`)은 recipe와 deriver(결정 1, 5장), coverage grid(결정 2, 뒤에 Phase 7이 대체), 길이와 demand class의 관례(결정 3: 기본 segment 120 s, C1 calibration 파일은 60 s — 둘 다 design이라고 2026-10-16의 archive가 적습니다 —, C1은 `calibration`, C2(의도 짝)부터 C6(한계 파일)까지는 `oversubscribed`), seed 정책(결정 4), 이름(결정 5: scenario catalog대로, 측정으로 확인한 이름 `soffice.bin`, `cc1`, `updatedb`)을 정했습니다.

Phase 2가 끝났을 때 core set은 24개 파일이었고(`_dev/TODO.md`의 2.4 줄, "13 novel + 11 derived, all windows green on cli:3 numbers" — Phase 2 측정 campaign의 CLI 세 번째 묶음 값으로 모든 파일이 당시의 demand window 안에 들었다는 뜻), 파일마다 두 mode로 compile해서 artifact가 48개였습니다. archetype은 문헌에 기댄 12개였습니다.

## 15.4 Phase 3, 5, 7: 정답과 기록을 다듬다

- **Phase 3(2026-09-06).** manifest가 파일마다 `utilization`과 `demand_class`를 기록하게 되었습니다(12.3절). `c1-idle`의 빈 attribute가 발견되어 `background_wanted` lint가 loader에 들어갔습니다(2.5절). 같은 날 protocol freeze가 run file, visible projection, telemetry 등 다섯 계약을 동결했습니다. run file이 `meta`에서 `workload_id`만 남기는 것과 projection이 instance마다 항목 하나라는 것이 이때 정해졌습니다(8.2절).
- **Phase 5(2026-09-08).** `familiarity`가 canonical `ground_truth`로 옮겨졌습니다(2.5절).
- **Phase 7(2026-09-09/10).** Phase 6의 짝 검토가 "coverage grid가 mode × familiarity만 세어 driver table 32칸 중 17칸만 채운다"는 것을 찾았습니다. Phase 7은 grid를 driver table의 32칸으로 바꾸고 빈 칸이 있으면 CI가 실패하게 했습니다(`--require-coverage`). 기록된 이유는 "the human sign-off had missed the attribute's `false` side"입니다. C1(calibration 묶음)을 mode마다 하나씩 16개로 늘리고 C7(attribute counterpart 묶음)을 새로 만들어 파일이 24개에서 50개로, artifact가 48개에서 100개로 늘었습니다. `pre_committed_miss` 표시가 생겼고, 파생 파일의 `calibration`을 recipe에 명시하게 되었습니다(5.4절).

## 15.5 Phase 9의 연구 slice들: 측정이 문헌을 대체하다

2026-09-13의 critical-findings memo(`docs/memos/2026-09-13-critical-findings.md`)가 archetype들의 문헌 근거를 원문과 대조해 finding 열셋(A1–A5, B1–B7, C)과 원문과 대조하지 못한 출처의 목록 하나(D)를 적었고, 이것이 Phase 9(dataset 재건)의 출발점이 되었습니다. 재건은 archetype을 거의 모두 CI runner에서 측정한 값으로 바꾸었는데, 그 과정에서 compiler와 포맷도 여러 번 바뀌었습니다.

- **9.4(2026-09-13), 게임.** `game-task-chain`에서 "~300개 task"의 꼬리를 없애고 chain만 남겼습니다(D3). 기록된 이유는 그 300이 게임 하나가 아니라 "Around 300 tasks are scheduled while running a game … including the system tasks"였고, 꼬리의 값은 근거 없는 자리표시였다는 것입니다. 이로써 recognizer가 보던 `game.exe × 300`이 사라졌습니다. `wineserver`가 chain 구성원이 되었습니다(D4, 11.9절).
- **9.5(2026-09-14–26), 대화형 앱.** 문헌 기반의 `desktop-interactive`, `audio-playback`, `video-playback` 대신 측정된 archetype 아홉 개가 들어왔습니다. compiler에는 측정된 앱의 경로(D9, 11.1절), quantile table(D17, 10.3절), 키 입력 재생(D18, 4.2절), timer channel(D74, 7.6절), periodic job(D75, 11.5절), forward recurrence(D77, 11.1절)가 차례로 들어왔습니다. follow-up spec의 결정 14(2026-09-16)는 native set을 내보내지 않기로 했습니다. spec은 이 결정이 결정 13과 "the same reasoning"에서 나왔다고 적습니다. 결정 13의 내용은 "The library's archetypes come from more than one observation venue, and their relative scales are not calibrated to each other"입니다. archetype들이 서로 다른 관측 환경(CI runner, 문헌 속의 기계)에서 왔고 그 크기가 서로 보정되지 않았다는 것입니다. 결정 14 자체는 이 이상의 이유를 적지 않습니다.
- **9.6(2026-09-19), 빌드.** object job을 spawn table의 자식 여섯으로 펴는 형식(D19)과 단계별 CPU 표(D20). 11.7절.
- **9.10(2026-10-01–), timeline.** 이 slice는 timeline의 내용을 정했지만 포맷에도 손을 댔습니다. batch job을 통째로 묶기(D17), launch phase(D21, 11.3절), 이름은 comm(D25, 3.6절), `member_names` binding(D26), design 값의 기록(D31), 묶인 값의 출처 규칙(D32, 3.5절), 파생 파일의 비율 유지와 deriver의 `set-focus`·`set-operations` op(D44, 5.3절).

## 15.6 9.11의 두 memo

scheduler 쪽 상수를 조사한 9.11은 simulator 담당 인경민과 projection 담당 박이안에게 두 memo를 보냈습니다.

- **2026-10-07, TIMER skip 규칙.** TIMER의 늦은 tick을 backlog로 몰아 실행하는 대신 지나간 마지막 tick만 실행하고 나머지는 놓친 job으로 셉니다(7.6절). canonical 파일의 모양은 바뀌지 않습니다. reference simulator는 2026-10-23부터 이 규칙을 돌리고, contract의 TIMER 행은 2026-10-30에 고쳐졌으며, schema의 TIMER 설명 문장은 아직 backlog를 말합니다(16장).
- **2026-10-08, declared scheduling class.** task가 바인딩한 entry의 class를 싣는 field를 제안했고, 두 사람이 동의해 9.13이 `declared_class`로 넣었습니다(3.7절). memo는 이것이 세 동결 계약(archetype, workload, run file)과 projection을 바꾸는 변경이라서 세 사람의 동의가 필요하다고 적습니다.

## 15.7 9.13(2026-10-09): 재건의 build

9.13은 연구 slice들의 결정을 한 번에 build한 sub-task입니다(`_dev/docs/spec/jioh/task-9.13-rebuild.md`). 포맷과 compiler에 관한 변화는 넷입니다.

1. **native mode 삭제(D1).** compiler의 `MODES`가 `("native", "single")`에서 `("single",)`로 바뀌었고, `native`를 요청하면 거절합니다. lint와 manifest도 mode를 하나만 압니다. 디렉터리 이름 `coreset-single`은 그대로 두었습니다(결정 5, "The single-lane set keeps the name `coreset-single`"). 2026-08-26 D16의 네 artifact가 여기서 끝났습니다.
2. **`declared_class`(D2).** library의 모든 entry와 canonical의 모든 task 기록(arrive event와 spawn table 항목)에 필수 field가 생겼습니다. schema는 닫힌 enum(`normal`, `idle`)으로, compiler는 바인딩한 entry에서 복사로, lint는 entry의 필수 field로 지킵니다. 이 field 때문에 모든 artifact의 바이트가 바뀌었습니다.
3. **TIMER-first lint(D3).** 13.2절.
4. **`c2-p2a-idle`(D4).** recipe op 하나로 만든 51번째 파일(5.6절).

결정 8은 이 sub-task가 더하는 lint와 test를 "Four, and no more"로 한정했습니다. 결정 10은 demand window를 아직 바꾸지 않고 경고로만 bless하게 했습니다(12.3절). bless의 기록(D7): 2026-10-09 15:18:40부터 15:40:47까지 M1 Pro에서 22분, artifact 51개, 680,806,752 byte, 외부 wake event 4,522,200개, 가장 큰 파일 `c6-dual` 190.3 MB. "the schema validation most of it"이라는 메모가 9.22의 출발점이 됩니다.

## 15.8 9.14(2026-10-09): 소비자 쪽 정비

9.14는 dataset을 읽는 쪽(채점 spec, guard spec, driver table, RQ0 gate spec)을 재건된 set에 맞춘 sub-task이지만, compiler에도 두 가지를 남겼습니다. 하나는 demand window의 은퇴와 segment별 demand(결정 4, 12.3절)이고, 다른 하나는 민감도 variant를 만드는 변환(결정 12)과 그중 trace replay를 위한 compiler의 `replay` 경로(D10, 11.10절)입니다.

## 15.9 9.17(2026-10-11): 사용자의 두 track

audit의 결정("focus enters the telemetry")을 구현하면서 키 입력 창의 이름이 `input`으로 바뀌고, 창 focus를 적는 새 `focus` track이 모든 timeline에 필수로 생겼습니다(4.1, 4.4절). canonical 파일에 네 번째 top-level key `focus`가 생겨 모든 artifact의 hash가 바뀌었고, set을 다시 bless했습니다(D6: compile 24분 20초, variant 34분 34초). 9.17 spec의 결정 8은 "The sub-task closes consistent", 즉 이 sub-task 안에서 rebuild와 re-bless와 re-pin을 끝내 `make check`가 통과하게 하라고 정했습니다.

## 15.10 9.18(2026-10-11): 감사의 지적을 고치다

2026-10-10 audit의 class-A 지적 셋을 고친 sub-task입니다(`_dev/docs/spec/jioh/task-9.18-compiler-schema-and-build-gate.md`).

- **A1 → `slice_of`(결정 1–3).** 파생 파일의 키 입력이 base와 같아지도록(4.3, 11.4절).
- **A2 → `source` map(결정 4).** 묶인 값마다 출처(3.5, 14.4절). `dataset/sources.yaml`에 `pytorch-examples`, `kdenlive`, `glam`이 더해졌습니다.
- **A4 → build gate(결정 5, 6, 8).** manifest의 `inputs`가 compiler 소스와 stream을 고정하고(13.5절), compile report를 artifact로 쓰고 고정하며(12.5절), `make check`가 디스크의 `build/`를 manifest와 대조합니다(`check_build.py`, 13.7절).

`source`와 `slice_of`는 canonical 형식을 바꾸지 않았지만 timeline의 바이트를 바꿔서 모든 artifact의 `derived_from`이 바뀌었고, 다시 bless했습니다.

## 15.11 9.22(2026-10-11): 한 번만 compile하기

9.18의 Linux 검증 실행이 6시간 제한을 넘을 것이 분명해 취소되면서 생긴 sub-task입니다. 결정 셋과 구현 하나가 13장에서 본 변화입니다. `check`는 비교만(결정 1), `lint`는 compile 전 검사만(결정 2), schema 검증은 `jsonschema-rs`로(결정 3), compile과 variant는 파일별 병렬로(D4). 결과로 집 기계에서 3.5시간 걸리던 한 바퀴가 약 5분이 되었고, CI의 Linux runner에서 6분 34초에 통과했습니다(D6, run 38131040159). invariant는 "No artifact or report byte changes"였고, 실제로 바뀐 것은 compiler 소스를 고정하는 manifest의 `inputs`뿐이었습니다(D5).

## 15.12 그 뒤: 같은 compiler, 더 많은 파일

9.19(2026-10-11)부터 9.21(2026-10-13)까지 generated layer가 생겼습니다. 9.19의 결정 4가 compiler와의 관계를 정했습니다. "The generator emits ordinary timeline YAML that the existing compiler compiles — no canonical artifact is produced directly." generated layer는 C1 timeline들을 조합하거나 이름을 바꾼 평범한 timeline 1,562개를 만들고, 이 권에서 설명한 compiler가 그것을 core set과 똑같이 compile합니다. 포맷도 compiler도 바뀌지 않았습니다. generated layer는 그 주제를 다루는 권에서 설명합니다.

## 15.13 9.23(2026-10-14–15)과 9.15(2026-10-16–17): 검사를 채우고 경로를 지우다

이 권(2026-10-14)이 찾은 어긋남 가운데 compiler와 build gate에 관한 것을 sub-task 9.23이 고쳤습니다(`_dev/research/jioh/task-9.23-guidebook-findings/changelog.md`). launch stream을 manifest의 `inputs`에 고정했고(D11, 13.5절), `make check`가 파생 timeline과 coverage grid를 commit된 byte와 비교하게 했고(D12, 13.7절), `make lint`가 freeze로 돌게 했고(D13, 14.1절), canonical lint 셋을 더했고(D14, 13.2절), 의존성 version을 정확히 고정했고(D15, 10.6절), segment-bound program이 퇴장 전에 바닥나지 않고 막힌 채로 끝나게 했습니다(D16, 11.1절, 11.5절). D16 때문에 모든 artifact의 byte가 바뀌었지만 새로 실행되는 것은 없고 compile report는 byte 그대로였습니다(D17). 이어 9.15(문서 정정 sub-task) 안에서 인지오가 정한 dataset 수정이 한 번의 rebuild로 들어갔습니다(2026-10-16). 닿지 않던 compiler 경로 넷을 지우고 맞는 경로가 없는 entry를 거절하게 했고(9.5절), freeze를 timeline의 묶인 값까지 넓혔고(14.4절), 측정 release 지도와 그 lint를 더했고(14.1절), 손으로 쓴 timeline의 머리 주석에 파일이 싣지 않는 것(session process, chain 밖의 게임 thread)과 Steam client의 측정된 상태를 적었습니다(6.1절, 6.3절). 머리 주석과 library의 byte가 바뀌었으므로 모든 artifact의 hash가 바뀌어, 일곱 manifest를 다시 bless하고 RQ0 gate spec을 다시 pin했습니다. 2026-10-17의 두 번째 rebuild는 정정 작업이 찾은 문장을 code와 data에서 고쳤습니다. schema의 `meta.derived_from`·`meta.sampled.archetypes`·`wake_event` 설명(git blob hash, 재생된 입력과 측정 entry의 timer 성분 wake), compiler module docstring의 chain 구성원 수(`chain_length` + 1), loader의 `_load_operations` docstring(9.10 D20의 operation 규칙, 4.5절)과 그 규칙의 test, variants module docstring의 replay stream 세 종류(`wakes`, `runs`, `cycles`), library의 머리 주석과 notes, `c1-idle`의 머리 주석입니다. core artifact는 `meta`에서만 바뀌었습니다. 같은 rebuild는 compiler 밖에서 행동도 바꿨습니다. generator가 9.10 D168의 꼬리표 규칙을 따르게 되어 transition grid `focus` 형태 timeline 214개의 두 번째 segment가 바뀌었고(5권 5.2절), `variants.yaml`의 `carried_values`에 숨은 탭 renderer의 두 thread가 더해져 corner variant 넷이 `meta` 밖에서도 바뀌었습니다(7권 2.11절). 다시 일곱 manifest를 bless하고 RQ0 gate spec을 pin했습니다(`harness/CHANGELOG.md`의 2026-10-17 항목).

---

# 16장 · 어긋난 문서와 열린 자리

이 장은 두 목록입니다. 하나는 저장소의 문서가 지금의 tree와 다르게 말하는 곳(어느 쪽이 맞는지와 그 근거), 다른 하나는 기록이 아직 정하지 않았거나 확인하지 않은 곳입니다. 2026-10-14에 이 장이 적은 어긋남 대부분은 Phase 9의 sub-task 9.15(문서·memo·guidebook 정정)가 2026-10-15부터 각 문서에서 고쳤습니다. 아래에는 그 뒤에도 남은 것을 적고, 고쳐진 것은 어디서 고쳐졌는지만 한 줄씩 적습니다.

## 16.1 문서가 tree와 다르게 말하는 곳

**TIMER의 늦은 tick.** workload schema의 TIMER 설명은 아직 늦은 tick을 backlog로 몰아 실행한다고 적습니다.

| 위치 | 문서가 말하는 것 | 지금의 진실과 근거 |
|---|---|---|
| workload schema의 TIMER 설명 | "late iterations accumulate as backlog (contract §3)" | skip 규칙. memo 2026-10-07; interpretation contract §3의 TIMER 행(2026-10-30) |

9.15는 이 문장과 interpretation contract §3의 TIMER 행, `docs/data-contracts.md` §4 예제 B의 backlog 문장을 일부러 남겼습니다. simulator의 동작과 TIMER의 뜻을 적은 문장은 인경민의 simulator가 skip 규칙을 구현할 때 함께 고치기로 하고 `_dev/TODO.md`의 Phase 10 TIMER 줄로 넘겼습니다(9.15 spec 결정 9). 그 구현은 2026-10-17의 final memo가 RQ0 gate spec의 simulator 적합성 항목 (b)로 부탁했고, 인경민이 2026-10-23에 넣었습니다(16.2절의 4). canonical 파일의 `TIMER` 명령어는 어느 규칙에서나 같습니다(7.6절).

**`docs/memos/2026-10-08-declared-scheduling-class.md` §1.** 이름이 class를 정하지 않는다는 예로 `c5-t3`을 듭니다. 그 파일은 2026-10-12에 `c6-alias`로 옮겨졌습니다(9.20). memo는 날짜가 박힌 기록이라 고쳐 쓰지 않고, 9.15가 memo 끝에 정정 절을 덧붙입니다.

**2026-10-14에 여기 있던 나머지는 고쳐졌습니다.**

- interpretation contract: §4 arrive event의 `id`와 `declared_class`, §5 FORK의 예(`c1-compile`의 17,448칸), §6의 `wineserver`, §7의 compile mode와 demand budget — 2026-10-16(9.15).
- workload schema의 설명: `attributes`의 예(`background_wanted`)와 `fork_cap`의 예(48) — 2026-10-16(9.15). `meta.derived_from`과 `meta.sampled.archetypes`(commit이 아니라 git blob hash), `wake_event`(재생된 입력과 측정 entry의 timer 성분 wake) — 2026-10-17(9.15). `program`의 문장은 2026-10-15부터 lint가 지킵니다(9.23 D14, 7.10절).
- `dataset/README.md`: canonical 예제의 `background_wanted`, demand window 문장("Demand is reported, not held"), Commands 절의 requirements(Python 3.12와 정확히 고정한 version), Layout 블록의 `stimulus/`·`launch/`·`replay/` — 2026-10-16(9.15). manifest의 inputs를 "(library, schema, compiler sources, streams)"라고 적는 문장은 9.23 D11이 launch stream을 고정한 뒤로 맞습니다.
- `docs/data-contracts.md`의 예제들: `c2-p1a`, `count`, `c2-p1b`의 recipe, `Troy.exe` chain, `make`의 17,448칸과 `fork_cap` 48, `c1-browsing`의 `chrome` 다섯 — 2026-10-16(9.15).
- `docs/background-guide.md` §5의 window 문장 — 2026-10-17(9.15).
- `docs/recognition-vocabulary.md` §1의 `initiated`(`session`) — 2026-10-16(9.15).
- 코드 안의 문서: `wlc/__init__.py`의 spec 경로, `wlc/deriver.py`의 docstring 예제, `wlc/timeline.py`의 다섯 번째 track `operations` — 2026-10-16(9.15). `wlc/compiler.py` module docstring의 chain 구성원 수, `wlc/timeline.py` `_load_operations` docstring의 9.10 D20 규칙, `wlc/variants.py` module docstring의 replay stream 세 종류 — 2026-10-17(9.15).
- task 2.4 결정 4의 "warns"와 deriver의 거절: 결정문이 잘못 적은 말이고, 거절하는 이유는 2026-10-16의 archive가 적습니다(5.4절).
- 9.18 D6의 키 입력 수: 9.23 D7이 바로잡았습니다(11.4절).
- interpretation contract §3의 TIMER 행("Late iterations accumulate as backlog; they are not silently skipped")과 `docs/data-contracts.md` §4 예제 B("missed ticks pile up as backlog"): memo 2026-10-07 §6의 문장과 skip 규칙으로 — 2026-10-30(`docs/data-contracts.md` §14).

## 16.2 기록이 아직 정하지 않은 곳

**1. launch stream의 고정 — 닫힘.** 9.23 D11(2026-10-15)이 `dataset/launch/*.json.gz` 10개를 manifest의 `inputs`에 더했습니다(13.5절).

**2. `children:<id>` channel을 누가 깨우나 — 규칙은 정해졌고 동의됨, 구현을 기다림.** 2026-10-16에 인지오가 정했습니다. executor는 orchestrator의 `WAIT children:<id>`를 자식이 모두 끝났을 때 완료하고, 살아 있는 자식이 없으면 곧바로 완료합니다. 이 규칙은 interpretation contract와 `docs/data-contracts.md`에 "proposed"로 적혔고, 동결된 계약의 변경이라 인경민의 동의가 필요했습니다(`docs/data-contracts.md` §13의 동결 규칙). 인경민이 구두로 동의해 효력을 가졌습니다(2026-10-31 기록). 구현될 때까지 reference simulator에서는 `c1-compile`의 build turnaround를 잴 수 없고, RQ0 gate spec이 그 구현을 simulator 적합성 항목 (g)로 요구합니다(7.7절). 인경민의 구현 대기.

**3. 파일보다 오래 사는 job의 demand — 닫힘.** 잘라 내지 않고, 문서들이 offered demand라고 문장으로 범위를 밝힙니다(12.4절).

**4. TIMER skip 규칙 — 닫힘.** 규칙은 2026-10-07에 인지오가 9.11 D3으로 정했습니다. 늦게 TIMER에 닿은 task는 지나간 마지막 tick을 즉시 소비하고 그 앞의 tick을 건너뛰며, 건너뛴 tick 하나하나가 일 없이 마감을 놓친 job입니다(memo 2026-10-07 §1, 7.6절). harness는 이 규칙으로 읽습니다(`docs/harness/metrics.md` §6.2). 9.14의 결정 1이 소비자 쪽을 모두 이 규칙에 맞춰 쓰고, 인경민의 구현을 "a named Phase 10 prerequisite"로 두었습니다. 2026-10-17의 final memo(`docs/memos/2026-10-17-workload-dataset-rebuild.md` §6.2)가 인경민에게 그 구현을 RQ0 gate spec의 simulator 적합성 항목 (b)로 부탁했고, 인경민이 2026-10-23에 simulator의 stage Y로 넣었습니다(커밋 `a62c10b0`; `simulator/memo/memo_261023.md` Part G). step K("TIMER+backlog")의 backlog를 대신합니다. interpretation contract §3의 TIMER 행은 2026-10-30에 memo §6이 적어 둔 문장, "absolute periodic wake on the grid t₀ + k·period, drift-free. Reached after one or more ticks have passed, the task consumes the last passed tick at once and skips the earlier ones, each a missed job with no work"로 확정되었습니다(`docs/data-contracts.md` §14). canonical 파일은 이 규칙에 따라 바뀌지 않습니다.

**5. 닿지 않는 compiler 경로 — 닫힘.** 2026-10-16에 인지오가 지우기로 정했고, 그 자리에 맞는 경로가 없는 entry를 거절하는 분기가 들어왔습니다(9.5절).

**6. lint의 빈 곳 — 닫힘.** core timeline의 이름 길이(15자), spawn table 자식의 `WAKE` 대상, program의 끝을 9.23 D14(2026-10-15)가 모두 canonical lint에 더했습니다(13.2절).

**7. Python 버전과 결정성 — 닫힘.** 2026-10-16에 인지오가 Python 3.12로 정했고, 직접 의존성은 9.23 D15가 정확한 version으로 고정했습니다. 다른 Python version에서 같은 byte가 나오는지는 확인하지 않았습니다(10.6절).

**8. 종료 감사 — 닫힘.** 이 권이 설명한 compile 경로의 재현(artifact, report, variant가 timeline에서 다시 만들어지는가)과 묶인 값의 출처가 정말 그 값을 받치는지는 9.16(종료 감사)이 2026-10-17에 확인했습니다. 재현은 9.15의 마지막 판(`2b080333`)에서 집의 dataset gate(372 s)와 dataset run 39014790007이, 9.16이 고친 data로 다시 build한 판(`17f28d7f`)에서 dataset run 39030123144가 통과했습니다. 그 재build에서 모든 artifact의 byte는 `meta`에서만 바뀌었고 compile된 workload(task, event, ground truth)는 어디서도 바뀌지 않았으며, RQ0 gate spec이 dataset을 `8e1eb753…`, variant를 `8e2948b1…`로 다시 pin했습니다(`_dev/research/jioh/task-9.16-exit-audits/README.md`, `logs/D.md`). 출처 쪽의 결과는 14.4절에 적었습니다. simulator가 구현해야 확인되는 문장은 RQ0 gate spec의 simulator 적합성 항목별로 같은 폴더의 `compiled/uncheckable-by-item.md`에 모였고, 각 항목이 구현될 때 인경민이 돌릴 확인입니다. 위의 2(`children:<id>` channel, 항목 (g))는 그대로 열려 있고, 4(TIMER skip 규칙, 항목 (b))는 2026-10-23에 구현되었습니다. (b)에 기대는 문장의 확인은 기록에 아직 없습니다.

---

# 17장 · 용어 정리

이 권에서 풀어 쓴 용어를 모았습니다. "종류"의 `project`는 이 저장소가 만들었거나 자기 뜻으로 쓰는 말, `OS`는 운영체제와 scheduling의 말입니다. 괄호 안은 처음 풀어 쓴 절입니다.

## 17.1 파일과 포맷

| 용어 | 종류 | 뜻 |
|---|---|---|
| `archetype` | project | 프로그램 한 종류가 CPU를 어떻게 쓰는지 적은 행동 모형. `dataset/archetypes.yaml`의 entry 하나. 이름·개수·의미를 모름(머리말) |
| `timeline` | project | 사람이 쓰는 연출 대본 YAML. 어떤 이름의 task가 언제 등장·퇴장하는지, 각 순간의 정답, 사용자의 손과 눈(1.1) |
| `canonical workload` | project | compile 결과물 JSON, simulator가 읽는 유일한 포맷. 분포 없이 정수 µs만(1.1, 7장) |
| `wlc` | project | workload compiler, `dataset/tools/wlc/`(머리말, 9장) |
| `task` | project | simulator가 스케줄하는 실행 단위 하나. 실제 desktop의 process(때로는 tree 전체)에 대응(1.1) |
| `program` | project | task가 실행할 명령어 목록(7.6) |
| `primitive` | project | program의 기본 명령어. `RUN`, `SLEEP`, `TIMER`, `WAIT`, `WAKE`, `FORK`/`EXIT`(7.6) |
| `LOOP` | project | program 안의 반복. primitive가 아닌 VM 내부 제어문. 지금은 게임 chain 구성원에서만 `count: "unbounded"`로 나옴(7.6) |
| `arrive` / `wake` event | project | canonical `events`의 두 종류. task의 탄생과, 박힌 시각의 외부 깨우기(7.5) |
| `channel` | project | `WAIT`와 `wake`가 쓰는 우편함 이름. `timer:`, `input:`, `chain:`, `job:`, `children:`(7.7) |
| `spawn table` | project | orchestrator가 들고 오는, 미리 다 쓴 자식 task 목록. `FORK`가 순서대로 소비(7.8) |
| `fork_cap` | project | 동시에 살아 있을 수 있는 자식 수. compiler가 `parallelism_cap × 6`으로 씀(7.8) |
| `object job` | project | `make`가 소스 하나를 컴파일하는 단위. 자식 여섯(`sh`, `gcc`, `cc1`, `as`, `fixdep`, `rm`)으로 모형화(3.3, 11.7) |
| `variant recipe` | project | `*.variant.yaml`. base에서 바꿀 것만 적은 파일(5장) |
| `deriver` | project | recipe를 실행해 파생 timeline을 쓰는 도구, `wlc/deriver.py`(5장) |
| `op` | project | recipe의 명령 하나. `rename`, `patch-segment`, `patch-task`, `add-task`, `set-segments`, `set-input`, `set-focus`, `set-operations`, `patch-meta`(5.3) |
| `base` / `derived file` / `novel timeline` | project | recipe의 출발점 / recipe로 만든 timeline(28개) / 사람이 직접 쓴 timeline(23개)(5.1) |
| `artifact` | project | compile의 산출물 `<id>.workload.json`(9.2) |
| `compile report` | project | artifact 옆의 `<id>.report.json`. 수요와 operation 길이(9.2, 12.5) |
| `manifest` | project | 입력·artifact·report의 hash와 demand를 모은 lockfile, `dataset/build.manifest.json`(9.2, 13.5) |
| `bless` / `blessed build` | project | 새 build의 hash를 manifest에 기록하고 commit해 공식 build로 확정하는 일 / 그렇게 확정된 build(3.5) |
| `run file` | project | simulator의 loader가 꺼내는 view. `events`와 `workload_id`만(8.2) |
| `visible projection` | project | daemon의 loader가 꺼내는 view. 이름·class·박힌 시각·focus·자식 개수만(8.2) |

## 17.2 timeline의 field와 label

| 용어 | 종류 | 뜻 |
|---|---|---|
| `segment` | project | timeline 시간축의 한 구간. 정답 label 하나가 붙음(2.4) |
| `mode` | project | 사용자가 하는 일의 이름. 메뉴 열여섯 개(2.4) |
| `ambiguous` | project | 정답조차 정할 수 없는 구간의 mode 값. `c6-dual` 하나. 채점에서 빠짐(2.5) |
| `background_wanted` | project | 배경 작업을 사용자가 원하는가. driver table의 두 번째 축. `ambiguous`가 아니면 필수(2.5) |
| `pre-committed miss` | project | 설계상 맞힐 수 없다고 미리 표시한 구간. tree에 8개(2.5) |
| `familiarity` (tier) | project | 이름이 알아보기 쉬운 정도 1–5. 적었을 때만 canonical로(2.5) |
| `scenario catalog` | project | 실제 desktop에서 함께 도는 process 조합 S1–S18. `scenario` field가 그 id를 가리킴(2.4) |
| `driver table` | project | 정답 label 한 칸마다 scheduler 설정을 적은 표. 32칸(2.4) |
| `coverage grid` | project | core set의 segment가 driver table 32칸을 채우는지 센 표(2.4) |
| `demand class` | project | `oversubscribed`(경쟁을 일으키도록 설계) 또는 `calibration`. 설계 의도의 표시(2.2, 12.3) |
| `lifetime class` | project | `segment-bound`(사용자가 닫음), `finite`(일을 마치면 끝), `spawned`(부모가 낳음)(3.2) |
| `binding_params` / `bind` | project | archetype이 timeline에 맡긴 손잡이 목록 / timeline이 그 손잡이에 넣은 값(3.3) |
| `count` | project | 같은 task의 instance 수. id는 `<id>.1`…(3.4) |
| `instance id` | project | `count`로 펼친 task의 id. 무작위 추출의 열쇠(3.4, 10.4) |
| `source` map | project | 묶인 값(`bind`의 key, 적은 `count`)마다 출처(3.5) |
| `registry tag` | project | `dataset/sources.yaml`의 출처 id에 위치를 붙인 문자열. 예: `lavd-ossna24:s16`(3.5) |
| `meas-ci` | project | 이 연구가 GitHub Actions runner에서 측정한 결과라는 출처 id. `meas-ci:<workflow>:<campaign 날짜>`(3.5) |
| `design` / `convention` / `arithmetic` | project | 출처 대신 쓰는 label. 실험 설계로 정한 값 / 관례 / 계산한 값(3.5) |
| `declared_class` | project | task가 바인딩한 archetype entry의 scheduling class, `normal` 또는 `idle`. timeline에는 없음(3.7) |
| `input` track | project | 사용자가 타자를 치는 창의 목록. compile 때 키 입력 wake로 녹음(4.2) |
| `stimulus` | project | task를 깨우는 외부 입력의 흐름. 여기서는 실제 타자 기록의 재생(4.2) |
| `SWELL-KW` | project | 실험실에서 지식 노동 과제를 한 학생과 인턴 25명의 키보드·마우스 기록 공개 dataset(`swell-icmi14`). stimulus의 원천(4.2) |
| `slice_of` | project | 파생 입력 창이 base 창의 조각임을 적는 표시. deriver가 씀. canonical에는 없음(4.3) |
| `focus` track | project | 어느 top-level task의 창이 앞에 있는가. 필수. canonical의 `focus` key가 됨(4.4) |
| `operation` | project | 앱 안의 무거운 동작(page load, 메일 전송 등). 시작 시각만 적고 길이는 compile 때 뽑음(4.5) |
| `counterpart` | project | C7의 파생 파일. base의 배경 작업을 원하지 않는 쪽으로 바꿈(4.3) |
| C1–C7 | project | core set의 일곱 묶음. C1 calibration, C2 intent pair, C3 transition arc, C4 distractor injection, C5 familiarity ladder, C6 resolution limit, C7 attribute counterpart(2.2) |

## 17.3 compiler와 검사

| 용어 | 종류 | 뜻 |
|---|---|---|
| `keyed substream` | project | `(seed, instance id, 이름표, 순번)`을 열쇠로 하는 독립된 무작위 흐름. 순서가 아니라 이름으로 뽑음(10.2) |
| `quantile table` | project | 측정 분포를 10개 percentile과 `min`, `max`, 구간 평균 11개로 싣는 모양(10.3) |
| `component` | project | 측정된 앱의 활동을 thread 이름별로 나눈 조각. 간격 분포와 run 분포를 가짐(6.1, 11.1) |
| forward-recurrence 간격 | project | 이미 돌던 흐름에 아무 때나 끼어들었을 때 첫 깨어남까지의 시간. 첫 간격을 이것으로 뽑음(11.1) |
| `heavy event` | project | 측정 중 드물게 일어난 큰 run. 비율만 있고 간격 분포는 없음(11.2) |
| `launch phase` | project | 앱이 실행 직후 안정될 때까지의 활동. 0 s보다 늦게 도착하는 task에 재생(11.3) |
| `periodic entry` | project | 매체의 주기마다 job 하나를 하는 archetype(영상, 음악, 통화). TIMER 격자로 펼침(11.5) |
| `chain constructor` | project | `game-task-chain` 한 줄을 열일곱 개의 평범한 task로 펼치는 compiler 경로(11.9) |
| `chain head` | project | chain의 첫 구성원, TIMER로 깨어나 frame을 시작. focus가 가리키는 id(6.3, 11.9) |
| `lane scaling` | project | 여러 core 기계의 수요를 CPU 하나에 맞게 줄이는 compile 단계. `scalable` field에만(11.9) |
| `lane_share` | project | chain의 frame당 CPU를 CPU 하나의 몇 배로 맞출지. design 값(11.9) |
| `demand` / `utilization` | project | task가 원하는 CPU 시간 총량 / 그것을 파일 길이로 나눈 값(12.1) |
| `demand window` | project | 예전의 ~100–150 % 관문. 2026-10-09 이후 관문이 아님(12.3) |
| `admission test` | project | 파일 하나에서 oracle과 무작위 조건의 차이를 보는 파일별 검사(12.3) |
| `t₀` | project | TIMER 격자의 기준 시각. TIMER를 처음 실행한 순간이고, 첫 TIMER는 도착 단계에서 실행되므로 task의 도착 시각(11.5, 13.2) |
| `TIMER first` | project | TIMER가 있는 program은 처음 실행되는 명령어가 TIMER여야 한다는 canonical lint(13.2) |
| `canonical lint` | project | compile 안에서 artifact마다 도는 검사. schema, 정렬, id, TIMER first, FORK, wake와 WAKE의 대상, 이름 15자, program의 끝, focus(13.2) |
| `repo lint` | project | library와 출처 registry의 검사(14.2) |
| release map | project | `dataset/meas-releases.yaml`. `meas-ci` campaign마다 원자료를 담은 GitHub release와 asset의 sha256. lint가 인용된 campaign마다 항목을 요구(14.1) |
| `timeline lint` | project | loader의 구조 검사 전부(14.3) |
| bound-value source lint | project | 묶인 값마다 출처가 있는지 보는 lint, `lint_bound_sources`(14.4) |
| `check` | project | build gate. manifest, 파생 timeline, coverage grid가 commit된 바이트와 같은지, `build/`가 manifest와 같은지 비교(13.7) |
| `jsonschema-rs` | project | schema 검증에 쓰는 Rust library. 2026-10-11부터(13.4) |
| `trace replay` | project | 분포 대신 측정 기록 하나를 그대로 쓰는 compile 경로. 민감도 variant에서만(11.10) |
| sensitivity variant | project | RQ0 gate spec이 읽는 `<base>@<set>` 파일. base를 변환해 만듦(7.2, 11.10) |

## 17.4 실험 장치

| 용어 | 종류 | 뜻 |
|---|---|---|
| `recognizer` | project | process 이름과 개수 등을 보고 사용자가 무엇을 하는지 맞히는 부품(2.4) |
| `oracle` | project | 정답을 그대로 읽는 recognizer 조건. 최선의 기준선(2.4, 8.2) |
| `grader` | project | Layer 1의 채점자. recognizer의 답을 `ground_truth`와 비교(8.2) |
| Layer 1 / Layer 2 | project | 결과의 두 층. 상황을 맞혔는가 / scheduling이 좋아졌는가(8.2) |
| `telemetry` | project | recognizer에게 보여 주는 관측. 이름→개수 묶음과 focus 주인의 이름(4.4) |
| telemetry shape | project | `focus`(focus 이름 포함) 또는 `names`(빼고). query point는 같음(4.4) |
| `query point` / `snapshot` | project | telemetry가 바뀌어 다시 묻는 시점 / 그때 보여 주는 한 장(4.4) |
| `information asymmetry` | project | 부품마다 알아도 되는 정보를 다르게 정하고, loader가 parse 경계에서 나머지를 버리게 하는 원칙(8.1) |
| `RQ0` | project | 첫 관문 실험. oracle과 무작위 조건 사이에 headroom이 있는지 묻는 것(1.2) |
| `audit` | project | 2026-10-10에 dataset 전체를 점검한 기록. A1–A4가 class-A 지적(3.5) |
| 9.x | project | Phase 9(dataset 재건)의 sub-task 번호. 9.10은 timeline 연구, 9.13은 재건 build 등(1.6) |
| `Wine` / `wineserver` / `Proton` | project | Windows 프로그램을 Linux에서 돌리는 호환 계층 / 그 조정 process, chain의 둘째 구성원 / Steam의 Wine 기반 계층(6.3) |

## 17.5 운영체제와 scheduling

| 용어 | 종류 | 뜻 |
|---|---|---|
| `scheduler` | OS | 지금 CPU를 어느 task에 줄지 고르는 부품. 실험 대상(1.2) |
| `process` | OS | 실행 중인 프로그램 하나에 운영체제가 붙이는 단위(1.1) |
| `wake` | OS | 잠들어 있던 task를 실행 가능하게 만드는 사건(1.2) |
| `lane` | OS | 이 연구의 simulator가 가진 CPU 하나. demand 1.0 lane은 CPU 하나를 꽉 채우는 양(1.5) |
| `block` | OS | 무언가를 기다리느라 CPU를 쓸 수 없는 상태. batch job에서는 run 사이의 off-CPU 시간(1.5, 11.6) |
| `preemption` | OS | 실행 중인 task를 scheduler가 중간에 끌어내리는 것(1.5) |
| `time slice` | OS | task가 CPU를 한 번 잡았을 때 쓸 수 있는 최대 시간(1.5) |
| `periodic task` / `deadline` | OS | 일정 주기로 깨어나 일하는 task / 그 주기의 일을 마쳐야 하는 시각(1.5) |
| `job` | OS | 주기적 task의 한 주기 분량의 일. harness가 마감 준수를 셈(7.6) |
| `fork` | OS | process가 자식 process를 만드는 것(1.5) |
| `comm` | OS | 커널이 process마다 기록하는 15자 이름. `ps`와 `top`이 보여 줌(1.5, 3.6) |
| `scheduling class` | OS | 프로그램이 스스로 선언하는 scheduling 정책(1.5, 3.7) |
| `SCHED_IDLE` | OS | 다른 정책의 task가 없을 때만 CPU를 받는 Linux 정책. 이 dataset의 `idle`(3.7) |
| `nice` | OS | normal 정책 안의 가중치. class가 아니며 싣지 않음(3.7) |
| `EDF` | OS | 마감이 가장 이른 job부터 CPU를 주는 알고리즘(7.6) |
| `LOTTERY` | OS | 추첨권 수에 비례해 CPU를 주는 알고리즘(3.7) |
| `make -j8` / jobserver | OS | `make`가 job을 최대 8개 동시에 돌리게 하는 옵션 / 그 수를 세는 장치(3.3) |
| discrete-event simulation | OS | 다음 사건 시각으로 곧장 건너뛰는 simulation 방식(2.3) |
| `DES core` / `VM` | project | simulator의 사건 엔진 / task 하나의 program을 실행하는 해석기(7.6) |
| `rt-app` | OS | task 사건의 시간(run, sleep, timer 주기, deadline 매개변수)을 µs 정수로 다루는 workload 생성 도구(use case의 길이는 초). contract가 선례로 듦(2.3) |
