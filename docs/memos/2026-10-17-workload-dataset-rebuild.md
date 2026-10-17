# Phase 9 결과 — workload dataset을 다시 만들면서 생긴 것, 바뀐 것, 없어진 것

> Status: memo · Created 2026-10-17 · Updated 2026-10-17
> 열림 — 인경민: simulator의 loader가 spawn된 child를 target으로 하는 WAKE를 받는 것(§4.1, §6.1), RQ0 run 전에 남은 simulator conformance 항목 (a)·(b)·(d)·(e)·(g)·(h)를 hand fixture로 보여 주는 것과 (g)에 대한 동의(§6.2), rebuild된 core set에서 regression check와 EDF 재측정(§6.3). 박이안: recognition log에 formatted prompt를 남길지, chat template이 넣는 날짜를 고정할지 기록할지(§8.2). 셋이 같이: 제안 둘(§9). 담당 인경민, 박이안.
> From 인지오 to 인경민, 박이안.

## 0. 이 문서

Phase 9에서 workload dataset을 처음부터 다시 만들었어요. 이 문서는 dataset을 직접 만들지 않은 사람이 읽고, 자기 프로그램 — 인경민의 simulator, 박이안의 daemon — 에 무엇이 달라지는지 알 수 있게 정리한 보고서예요.

변경마다 같은 순서로 적었어요: **왜** 바꿨는지, **무엇이 어떻게** 바뀌었는지(전/후 예시), 그래서 **누구에게 무슨 영향**이 있는지. 결정의 자세한 근거는 각 항목에 적은 파일에 있어요. 급하면 §2의 표와 §6(인경민), §8(박이안)만 읽어도 돼요.

**workload dataset이 뭔지 한 번 더.** simulator가 돌리는 입력이에요. workload 파일 하나는 "가상의 desktop에서 어떤 program이 언제 도착해서, CPU를 얼마나 쓰고, 언제 잠들고 깨는지"를 시간순 event로 적은 JSON이에요. 만드는 순서는 이래요.

```text
archetype library   program 한 종류가 CPU를 어떻게 쓰는지 (측정값)      dataset/archetypes.yaml
      ↓
timeline            어떤 program이 언제 뜨고 지는지 (사람이 쓴 시나리오)  dataset/timelines/
      ↓  compiler
workload 파일       simulator가 읽는 event 목록                         dataset/build/ (make로 생성)
```

## 1. 왜 다시 만들었나

9월 중순에 archetype 값들의 출처를 원문과 하나씩 대조해 보니 맞지 않는 게 많았어요(`docs/memos/2026-09-13-critical-findings.md`). 예를 들어 "kernel build는 process 2,430개를 만든다"는 값은 Linux kernel build가 아니라 DynamoRIO build에서 나온 숫자였어요. 남의 논문에서 빌려 온 숫자가 우리 workload의 뼈대였기 때문에, 그 위에 올린 실험 결과도 믿기 어려웠어요.

그래서 값을 빌려 오는 대신 직접 쟀어요. GitHub Actions runner(AMD EPYC 7763 core 하나)에서 실제 program — VS Code, Chrome, Thunderbird, Kdenlive, kernel build, PyTorch 학습, 파일 색인기 등 — 을 돌리고, `perf sched`로 scheduler event를 trace해서 "얼마나 오래 돌고, 얼마나 자주 깨는지"를 분포로 뽑았어요.

결과적으로:

- archetype 29개 중 28개가 우리가 잰 값이에요. 남은 하나(`game-task-chain`, 게임이 frame마다 거치는 thread 사슬)만 LAVD scheduler 발표(`lavd-ossna24`)의 수치예요.
- 그 위에 서 있던 것들 — 점수 계산 규칙(scoring spec), run이 망가졌는지 보는 검사(guard spec), 첫 실험의 사전등록(RQ0 gate spec), daemon의 prior driver table — 도 새 파일 기준으로 다시 맞췄어요.
- 파일 형식에도 몇 가지가 생기고 바뀌었어요. 이게 이 문서의 대부분이에요.

## 2. 한눈에

| 구분 | 무엇 | 인경민(simulator) | 박이안(daemon) |
|---|---|---|---|
| 생김 | task마다 scheduling class, `declared_class` (§3.1) | **할 일**: 읽고 idle 규칙 적용 | projection에 class가 보여요 |
| 생김 | 지금 focus를 가진 window, `focus` (§3.2) | 없음 (run file 그대로) | **할 일**: snapshot에 focus, `--telemetry` flag |
| 생김 | generated layer 1,562개, sensitivity variant 78개 (§3.3) | 같은 형식 (일부는 §4.1에 걸림) | 같은 형식 |
| 바뀜 | compile 파일 안에서 child끼리 WAKE (§4.1) | **할 일**: loader 수정 | 없음 |
| 바뀜 | program이 끝나는 방식 (§4.2) | 없음 (이중 `task_end`가 사라짐) | 없음 |
| 바뀜 | config가 적용되는 시점: drain과 순서 (§4.3) | 없음 (이미 구현) | 없음 |
| 바뀜 | `render` mode의 설명 (§4.4) | 없음 | recognizer가 읽는 문구가 바뀜 |
| 바뀜 | 이름 몇 개 (§4.5) | regression 결과 대조 시 | log 다시 뽑을 때 |
| 없어짐 | native compile 결과, 옛 파일로 낸 결과 (§5) | regression 다시 | **할 일**: log 다시 뽑기 |
| 생김 | licence (§10) | — | — |

## 3. 생긴 것

### 3.1 task마다 scheduling class: `declared_class`

**왜.** Linux에서 program은 자기 scheduling class를 스스로 정할 수 있어요. 파일 색인기 Tracker(`tracker-miner-f`)는 자기 thread 모두에 `SCHED_IDLE`을 걸고, 백업 도구 Déjà Dup은 백업을 `chrt --idle 0`으로 시작해요. idle class인 task는 "다른 task가 CPU를 원하지 않을 때만" 돌아요. 이전 dataset은 이걸 표현할 수 없어서, 색인기가 editor와 똑같은 자격으로 CPU를 두고 경쟁했어요. 실제 desktop과 다른 상황이고, 그러면 "어떤 scheduler 설정이 맞는가"의 답도 달라져요.

**무엇이 바뀌었나.** 모든 task — `arrive` event와 spawn table의 child 하나하나 — 에 `declared_class`가 필수로 붙어요. 값은 `normal`과 `idle` 둘뿐이고 기본값은 없어요. 예시는 `c1-indexing`에서 색인기가 도착하는 event예요(program은 줄였어요).

```jsonc
// 전
{ "op": "arrive", "t": 2000000, "id": "hog", "name": "tracker-miner-f",
  "program": [ { "op": "RUN", "us": 38048 }, { "op": "SLEEP", "us": 123 }, … ] }

// 후
{ "op": "arrive", "t": 2000000, "id": "hog", "name": "tracker-miner-f",
  "declared_class": "idle",
  "program": [ { "op": "RUN", "us": 38048 }, { "op": "SLEEP", "us": 123 }, … ] }
```

`idle`인 program은 세 종류예요: 파일 색인기, 증분 백업, 그리고 다운로드를 idle로 돌리는 경우를 보기 위한 `game-download-idle`. 이 program이 들어간 core 파일은 일곱 개예요(`c1-indexing`, `c7-indexing`, `c2-p1b`, `c1-backup`, `c7-backup`, `c2-p3b`, `c2-p2a-idle`). 나머지는 모두 `normal`이에요.

**규칙.** `idle` task는 `normal` task가 하나도 runnable하지 않을 때만 돌고, `normal` task가 깨어나면 바로 preempt돼요. FIFO를 포함해 어느 algorithm이든, 그 algorithm이 정하는 순서 아래 층으로 적용돼요(`docs/data-contracts.md` §4).

예를 들어 `c1-indexing`에서 색인기가 돌고 있을 때 editor(`code`, `normal`)가 키 입력으로 깨어나면, 색인기는 그 즉시 CPU를 내줘요. editor가 다시 WAIT로 잠들어야 색인기가 다시 돌아요. 전에는 둘이 같은 algorithm 안에서 똑같이 경쟁했어요.

**영향.**

- **인경민:** simulator의 loader가 `declared_class`를 읽고 이 규칙을 구현해야 해요. RQ0 run 전에 보여야 할 항목 (e)예요(§6.2). 지금은 이 field를 읽지 않아요.
- **박이안:** daemon이 보는 visible projection에 task마다 class가 보여요. spawn된 child는 이름과 class로 묶어 개수를 세요.
- harness의 mock daemon은 이미 이렇게 만들어요.

### 3.2 지금 focus를 가진 window: `focus`

**왜.** 같은 program들이 떠 있어도, 사용자가 지금 어느 window를 보고 있는지에 따라 상황이 달라요. 예를 들어 browser와 game이 둘 다 떠 있어도, game window를 보고 있으면 게임 중이고 browser를 보고 있으면 웹서핑 중이에요. 실제 OS도 이 정보를 써요: Windows의 Game Mode는 game이 foreground이고 focus를 가지고 있어야 켜져요(research proposal의 shipping system 표, `gamemode-docs`). 그래서 recognizer가 이 정보를 쓸 수 있게 넣었어요. 그리고 이게 실제로 얼마나 도움이 되는지 재기 위해, 같은 파일을 focus가 있는 입력과 없는 입력 두 가지로 돌려요.

**무엇이 바뀌었나.**

- workload 파일에 네 번째 top-level key `focus`가 생겼어요. 어느 task가 언제부터 언제까지 focus를 가졌는지예요. `c1-indexing`에서는 이래요:

  ```jsonc
  "focus": [ { "t_start": 0, "t_end": 60000000, "task": "editor" } ]
  ```

- daemon이 recognizer에게 보여 주는 telemetry snapshot이 두 모양(shape)으로 나뉘어요. 같은 순간의 snapshot이 shape마다 이렇게 달라요:

  ```jsonc
  // names shape: 전과 같은 모양
  { "t_us": 0, "processes": [ { "name": "code", "count": 1 } ] }

  // focus shape: focus를 가진 process의 이름이 더해짐 (아무도 없으면 null)
  { "t_us": 0, "processes": [ { "name": "code", "count": 1 } ], "focus": "code" }
  ```

- process 집합이 그대로여도 focus가 다른 program으로 옮겨 가면 새 snapshot과 query point가 생겨요(query point는 두 shape에서 같아요). 같은 이름의 window 두 개(예: `firefox` 창 두 개) 사이를 옮기는 건 아무것도 바꾸지 않아요.

**영향.**

- **박이안:** daemon은 shape를 필수 flag `--telemetry focus|names`로 받아서, snapshot을 그 shape로 만들고, recognition log의 top-level `telemetry`에 어느 shape를 보여 줬는지 적어야 해요(`docs/data-contracts.md` §5, §8, §11). run 하나는 workload 하나 × condition 하나 × shape 하나 × (난수를 쓰는 condition이면) seed 하나예요.
- **인경민:** simulator가 읽는 run file(`meta.id`와 `events`)은 그대로라서 바뀔 게 없어요.
- harness의 records에 shape를 적는 column `telemetry`가 생겼어요(column 25개). 첫 실험(RQ0)은 `focus` shape 하나만 돌려요 — RQ0의 세 condition은 telemetry를 읽지 않기 때문이에요.

### 3.3 generated layer와 sensitivity variant

**왜.** core set 51개는 사람이 장면 하나씩 쓴 시나리오라서, "상황이 바뀌는 순간을 따라가는가", "모르는 이름이어도 읽는가" 같은 질문을 체계적으로 묻기엔 수가 적어요. 그래서 mode마다 하나씩 있는 측정 기반 파일 16개의 task 집합을 기계적으로 조합해서, 질문마다 파일 묶음을 만들었어요. 모두 설계된 파일이고, 실제 desktop에서 그런 순서가 얼마나 자주 나오는지는 주장하지 않아요.

| set | 묻는 질문 | 개수 | 예시 파일과 뜻 |
|---|---|---|---|
| transition grid | 상황이 A에서 B로 바뀌면 따라가는가 | 480 | `tr-backup-to-browsing-focus`: backup 중에 browsing으로 넘어가요. `-focus`는 backup이 남은 채 focus만 옮겨 가고, `-departs`는 backup이 떠나요 |
| return grid | B에 잠깐 갔다가 A로 돌아오면 | 720 | `rt-backup-to-browsing-10s`: backup → browsing 10 s → backup |
| flap-stress set | A와 B가 계속 번갈아 나오면 설정이 흔들리지 않는가 | 24 | `flap-mail-to-gaming-10s-tuning`: mail과 gaming이 10 s 간격으로 번갈아 나와요 |
| distractor grid | 상관없는 program이 끼어들어도 답이 그대로인가 | 272 | `dx-backup-with-7z`: backup 중간에 vocabulary 밖의 `7z`가 끼어들어요. 정답은 그대로 backup |
| familiarity ladder | 덜 알려진 이름이어도 읽는가 | 66 | `fl-backup-t3`: 같은 backup 장면에서 `deja-dup`을 `duplicity`로 바꿔요 |

**sensitivity variant 78개**는 첫 실험(RQ0)의 결론이 측정 오차나 machine 차이에 흔들리지 않는지 보려고 core 파일을 변형한 사본이에요. 예를 들어 `c1-compile@corner-high`는 측정값을 범위의 위쪽 끝으로 민 것이고, `c1-compile@venue-x1.25`는 CPU 시간을 1.25배로 늘린 거예요.

**영향.**

- 형식이 core set과 같아서 simulator와 daemon은 core set처럼 읽으면 돼요.
- 다만 이 중 188개는 §4.1의 loader 문제에 걸려요.
- 실험 spec은 manifest에 적힌 축(A, B, 간격 등)으로 파일을 골라요. 파일은 commit되지 않고 `make -C dataset dataset variants generated`로 만들어요. 다 만들면 약 6.8 GB예요.

## 4. 바뀐 것

### 4.1 compile 파일: spawn된 child가 다른 child를 깨워요

**배경.** compile workload는 `make`가 Linux kernel을 build하는 걸 흉내 내요. 실제로 `.c` 파일 하나를 object로 만들 때 process 여섯이 차례로 일을 넘겨요: `sh` → `gcc` → `cc1`(실제 compile) → `as`(assembler) → `fixdep` → `rm`. 이번 rebuild는 이 hand-off를 측정한 그대로 재현해요. job 하나 안의 member들이 WAKE로 서로 일을 넘기니까, spawn된 child가 다른 spawn된 child를 깨워요. `make` 자신은 이 job들을 FORK로 띄우고, 마지막에 자식이 다 끝나기를 기다려요.

**예시.** `c1-compile`의 `make`와 첫 job의 앞부분이에요(줄였어요).

```jsonc
{ "op": "arrive", "id": "build", "name": "make", "declared_class": "normal", "fork_cap": 48,
  "program": [ { "op": "RUN", "us": 229 }, { "op": "FORK" }, …,
               { "op": "WAIT", "channel": "children:build" }, { "op": "EXIT" } ],
  "spawn_table": [
    { "id": "build.j1.sh",  "name": "sh",  "declared_class": "normal",
      "program": [ { "op": "RUN", "us": 848 }, { "op": "WAKE", "target": "build.j1.gcc" }, … ] },
    { "id": "build.j1.gcc", "name": "gcc", "declared_class": "normal",
      "program": [ { "op": "WAIT", "channel": "job:build.j1.gcc" }, { "op": "RUN", "us": 1731 },
                   { "op": "WAKE", "target": "build.j1.cc1" }, … ] },
    … ] }
```

`build.j1.sh`가 깨우는 `build.j1.gcc`는 `arrive` event가 아니라 spawn table에만 있는 id예요.

**영향.**

- **인경민 — 할 일.** 지금 simulator의 loader는 WAKE target을 `arrive` event의 id(여기서는 `build`)에서만 찾아요(`simulator/src/sim.cpp:899–905`, `:917`). 그래서 이 파일들에서 "WAKE target is not a top-level task"로 멈춰요(`:876`). loader가 spawn table의 child id 중에서도 WAKE target을 찾도록 고쳐 줘요. dataset은 이 쓰임을 유지해요.
- 걸리는 파일은 지금 build 1,691개 중 201개예요.
  - core 다섯: `c1-compile`, `c7-compile`(점수를 내는 judging 파일), `c3-workday`, `c4-compile`, `c6-dual`(보고만 하는 reporting 파일).
  - RQ0가 돌리는 compile variant 여덟: `c1-compile`과 `c7-compile`의 `@corner-high`, `@corner-low`, `@venue-x0.8`, `@venue-x1.25`.
  - generated 188개: transition grid 60, return grid 90, distractor grid 32, familiarity ladder 6.
- spawn된 program 안의 WAKE는 모두 이런 child끼리의 WAKE예요: `c1-compile` 하나에 43,620개, 201개 파일 전체에 855,150개.

### 4.2 program이 끝나는 방식

**왜.** 전에는 어떤 program이 정해진 depart(떠나는 시각)보다 먼저 instruction을 다 써 버릴 수 있었어요. 그러면 simulator는 그 자리에서 task가 끝난 것으로 보고(`task_end`, reason `exit`), depart 시각에 `task_end`를 한 번 더 냈어요. 화면에는 아직 떠 있어야 할 program이 simulation 안에서는 먼저 사라지는 셈이에요.

**무엇이 바뀌었나.** depart가 정해진 program은 이제 항상 "자기가 다음에 할 block"으로 끝나서, block된 채 기다리다가 depart가 지워요. 깨워지는 program이면 마지막에 WAIT 하나를 더 두고(wake N번에 WAIT N + 1개), timer로 도는 program이면 depart 뒤에 tick이 떨어지는 TIMER 하나를 둬요. `c1-indexing`의 editor(60 s에 depart)의 끝은 이렇게 바뀌었어요:

```jsonc
// 전: 마지막 wake를 처리한 RUN에서 instruction이 끝남 → depart 전에 사라짐
…, { "op": "WAIT", "channel": "timer:editor" }, { "op": "RUN", "us": 75 } ]

// 후: 다음 WAIT에서 block된 채 60 s의 depart를 기다림
…, { "op": "WAIT", "channel": "timer:editor" }, { "op": "RUN", "us": 75 },
   { "op": "WAIT", "channel": "timer:editor" } ]
```

depart가 정해지지 않은 task는 top-level이든 spawn된 것이든 `EXIT`로 끝나요. 예를 들어 같은 파일의 색인기는 일을 다 하면 `{ "op": "EXIT" }`로 끝나요.

**영향.** CPU 사용량, wake, tick은 하나도 바뀌지 않았고 파일의 byte만 바뀌었어요. dataset의 lint가 이 규칙을 검사해요.

- **인경민:** depart 전에 instruction이 바닥나서 `task_end`가 두 번 나오는 경우가 이제 data에서 생기지 않아요. 할 일은 없어요.

### 4.3 config가 적용되는 시점: drain과 순서

**배경.** daemon은 run 도중에 scheduler 설정을 바꿔요. 그 목록이 config schedule이에요: "시각 T에 설정이 C가 된다"는 entry의 목록. 문제는 algorithm을 바꾸는 순간 지금 CPU를 잡고 있는 task를 어떻게 하느냐예요. 이번에 두 규칙이 contract(`docs/data-contracts.md` §7)에 들어갔어요.

- **Drain.** MLFQ, EDF, LOTTERY에서 다른 algorithm으로 바꾸는 entry가, 어떤 task가 CPU를 잡고 있을 때 오면 바로 적용되지 않아요. 그 task가 CPU를 놓을 때 — slice나 지금 RUN이 끝나거나, preempt되거나, depart할 때 — 적용돼요. CPU가 비어 있을 때의 switch, FIFO에서 나가는 switch, 같은 algorithm 안에서 params만 바꾸는 entry는 찍힌 시각에 바로 적용돼요.
- **순서.** entry는 목록 순서대로 적용돼요. switch가 drain 중일 때 찍힌 entry는 같은 algorithm이어도 그 뒤에 줄 서서, 같은 순간에 그 다음으로 적용돼요.

**예시.** MLFQ로 돌던 중에 이런 schedule이 왔다고 해요.

```text
index 1   t = 100 ms   MLFQ → FIFO로 switch        (100 ms에 task A가 slice를 잡고 있고, 그 slice는 104 ms에 끝남)
index 2   t = 102 ms   FIFO, batch_bandwidth_cap만 바꿈
```

- **지금 규칙:** index 1은 A의 slice가 끝나는 104 ms에 적용(drain)되고, index 2는 그 뒤에 줄 서 있다가 같은 104 ms에 바로 이어서 적용돼요.
- **전 규칙(2026-09-09):** "같은 algorithm entry는 찍힌 시각에 바로"였어요. 그래서 index 2가 102 ms에, index 1이 104 ms에 적용돼서 목록의 순서가 뒤집힐 수 있었어요.

**영향.** reference simulator는 2026-10-10부터 이미 이렇게 해요(인경민의 drain 규칙 U3). harness는 실제 적용 시각을 trace에서 읽어요.

- **인경민, 박이안:** 둘 다 할 일은 없어요. daemon 쪽에서는 "entry는 목록 순서대로 적용된다"고 보면 돼요.

### 4.4 `render` mode의 설명

**왜.** recognizer는 정해진 mode 16개 중 하나로 답하고, mode마다 짧은 설명이 붙어 있어요(`docs/recognition-vocabulary.md` §1). dataset의 render 장면은 전부 동영상 편집기 Kdenlive가 project를 파일로 export하는 일이고 3D 장면은 없는데, 설명은 "3D/graphics render"였어요.

**무엇이 바뀌었나.**

```text
전: render — an offline 3D/graphics render
후: render — an offline render — a 3D scene or a video project rendered to a file
```

mode 이름 `render`와 정답 label, 파일은 그대로예요. `transcode`(이미 있는 media의 변환)와는 그대로 구별돼요.

**영향.**

- **박이안:** recognizer가 읽는 mode 설명 문구가 바뀌어요. prompt가 vocabulary를 그대로 싣는다면 그 문구도 바뀌어요. 9.12의 latency 측정에 쓴 prompt(`dataset/tools/meas/llm/prompt.json`)는 측정한 그대로 옛 문구로 남겨 뒀어요.

### 4.5 이름 몇 개

내용은 그대로이고 이름만 바뀌었어요.

- **core 파일 하나:** `c5-t3`이 2026-10-12부터 `c6-alias`예요. task, archetype, seed는 같아요. 예전 결과와 맞춰 볼 때 "파일이 사라지고 새 파일이 생겼다"가 아니라 이름만 바뀐 거예요.
- **연구 주장의 사슬:** `docs/research-claims.md`의 chain은 'link 1'–'link 7', 일곱 개예요(전에는 'six links'라고 적혀 있었어요). C1–C7은 core set의 파일 그룹 이름으로만 남아요.
- **dataset의 층:** 번호 대신 이름으로 불러요 — archetype library, scenario catalog, timelines. 'Layer 1/2'는 평가의 두 층(recognition 정확도, scheduling 성능)만 뜻해요.

### 4.6 '주장하지 않는 것'이 하나 늘었어요

`docs/research-claims.md`의 'What is not claimed'에, scheduling 결과가 다른 CPU나 다른 machine 구성으로 옮겨 간다고 주장하지 않는다는 항목이 생겼어요. CPU 값은 모두 runner의 AMD EPYC 7763 core 하나에서 잰 것이고(화면은 Xvfb, GPU·sound device·사람 없음), 다른 CPU에서는 program마다 빨라지는 정도가 달라요. 예를 들어 Xeon Platinum 8573C에서 `cc1`은 EPYC 시간의 0.72배, `fixdep`은 0.50배였어요. variant의 공통 배율(0.8–1.25배)은 이런 program별 차이를 재현하지 않아요. recognition은 CPU 값을 읽지 않아서 이 한계와 상관없어요.

## 5. 없어진 것

- **native compile 결과.** 전에는 compile 결과가 여러 CPU lane용(native)과 한 lane용(single) 두 가지였는데, 이제 한 lane용 set(`dataset/build/coreset-single/`)만 남았어요. simulator가 lane 하나로 돌기 때문이에요.
- **옛 파일로 낸 결과.** rebuild 전 파일로 낸 결과는 새 파일과 맞지 않아요. 인경민의 마지막 regression check(rebuild 전 24개 파일)와 박이안이 뽑은 recognition log가 여기에 해당해요(§6.3, §8.1).
- **"같은 algorithm entry는 찍힌 시각에 바로 적용"이라는 2026-09-09의 규칙.** §4.3의 순서 규칙으로 바뀌었어요.

## 6. 인경민에게 — 부탁할 것

### 6.1 loader: spawn된 child를 target으로 하는 WAKE

§4.1이에요. compile 파일 201개가 지금 loader에서 멈춰요. loader가 spawn table의 child id 중에서도 WAKE target을 찾도록 고쳐 줘요.

### 6.2 RQ0 run 전에 simulator가 보여야 할 것: conformance (a)–(h)

**배경.** RQ0는 첫 실험이에요: 상황을 완벽하게 알아보는 경우(`oracle`)가 무작위로 고르는 경우(`random`)보다 잴 만큼 좋은가. 그 결과를 믿으려면 simulator가 정해진 동작을 해야 해서, RQ0 gate spec(`harness/experiments/rq0-gate.yaml`)이 여덟 항목을 정해 뒀어요. 손으로 유도한 작은 fixture를 simulator로 돌려서 trace가 줄 단위로 맞는 걸 보이기 전에는 RQ0 run을 시작하지 않아요. 지금 (c)와 (f)는 코드에 있고, 여섯이 남았어요.

| 항목 | 쉬운 말로 | 상태 |
|---|---|---|
| (a) zero-wait `ready` line | block하는 instruction을 지날 때마다 `ready` line 하나, 실제로 안 기다렸으면 wait 0으로 | 남음 |
| (b) TIMER skip rule | 밀린 timer tick은 가장 최근 것만 처리하고 나머지는 건너뜀 | 남음 |
| (c) algorithm switch | MLFQ로 바꾸면 모든 task가 맨 위 queue에서 다시 시작; 같은 algorithm entry는 받은 slice를 끝까지 | 됨 |
| (d) `batch_bandwidth_cap` | 쉬지 않고 CPU를 쓰는 batch class가 CPU를 이 비율까지만 쓰게, 다른 task가 없으면 넘어도 됨 | 남음 |
| (e) strict idle class | §3.1의 idle 규칙 | 남음 |
| (f) EDF의 chain stage | 게임 frame 사슬의 깨어난 stage가 frame의 deadline을 물려받음 | 됨 |
| (g) `WAIT children:<id>` | `make`가 자식이 모두 끝날 때까지 기다리는 step | 동의와 구현 |
| (h) invocation contract | harness가 정한 command 모양으로 실행되는 것 | 남음 |

남은 항목 중 예시가 있으면 이해가 쉬운 넷이에요.

- **(a)** task가 RUN 중에 이미 와 있던 wake(mailbox) 덕분에 WAIT를 block 없이 지나가면, 지금은 trace에 아무 줄도 안 남아요. 규칙은 그 자리에 wait 0인 `ready` line을 남기는 거예요. 밀린 TIMER tick을 바로 처리할 때도, RUN이 block 없이 다음 RUN으로 이어질 때도 같아요(지금은 `run_end` 없이 `ready(cause=arrive)`로 다시 줄을 세워요, `advance` `:636–644`).

  ```jsonc
  // 지금
  {"event":"run_start","t":4000,"task":"editor"}
  {"event":"run_end","t":6000,"task":"editor","reason":"block","blocked_on":"wait"}

  // 규칙: 5000에 mailbox로 지나간 WAIT 자리에 ready line 하나
  {"event":"run_start","t":4000,"task":"editor"}
  {"event":"ready","t":5000,"task":"editor","cause":"wake"}
  {"event":"run_end","t":6000,"task":"editor","reason":"block","blocked_on":"wait"}
  ```

- **(b)** 60 fps로 도는 task(주기 16,667 µs)가 오래 밀려서 40,000 µs에야 TIMER에 닿았다고 해요. 그 사이 16,667과 33,334의 tick이 지나갔어요. 지금 코드(backlog rule)는 밀린 tick을 하나씩 다 처리해서 frame 두 개를 연달아 만들어요. skip rule은 가장 최근 tick(33,334)만 처리하고, 건너뛴 16,667 tick은 일 없이 `met: false`인 `deadline` line 하나로 남아요(놓친 job으로 세요). 실제 player나 주기 작업 framework도 밀린 주기를 다시 돌리지 않고 건너뛰어요(2026-10-07 TIMER memo §4). harness는 이미 skip rule로 읽어요. simulator가 구현하기 전까지 simulator 문서들은 backlog rule을 그대로 적어 두고, 구현되면 고칠게요.
- **(g)** `make`는 job 8개를 동시에 돌리다가 마지막 FORK 뒤에 `WAIT children:build`에 닿아요. 이 WAIT는 그때 살아 있는 job이 모두 끝나야 지나가고, 살아 있는 job이 없으면 block 없이 지나가요. 지금 simulator는 `children:build`를 보통 channel로 봐서, 아무도 그 channel을 WAKE하지 않으니 `make`가 run 끝까지 block돼요. 그러면 점수에 들어가는 `c1-compile`의 build 시간(weight 1.0)이 모든 condition에서 똑같이 잘린 값이 돼요. 이 규칙은 contract에 "제안, 인경민이 동의하면 유효"로 적혀 있어요. RQ0 gate spec은 run에 이걸 요구해요.
- **(h)** 지금 simulator는 입력을 위치 인자로 받고 trace를 stdout에 써요. contract 10은 이름 붙은 flag로 받고 trace를 지정한 파일에 써요.

  ```text
  지금:     src/sim c1-compile.workload.json schedule.json > trace.jsonl
  contract: src/sim --workload c1-compile.workload.json --schedule schedule.json --out-trace trace.jsonl
  ```

  그 밖에: trace를 썼을 때만 exit 0, 같은 argument면 byte가 똑같은 trace, trace header의 `sim`에 runner가 정한 version string(지금은 `"src/sim"`으로 고정이에요).

### 6.3 rebuild된 core set에서 regression check와 EDF 재측정

- 마지막 regression check는 rebuild 전 24개 파일에서였어요(`simulator/memo/memo_261010.md` Part B, D). §6.1의 loader가 고쳐지면 rebuild된 core set 51개와 variant 78개에서 다시 돌려 줘요.
- 함께, 인경민 backlog의 EDF 재측정이에요(memo_261010 Part F; `simulator/notes/note-for-jioh-edf-chain-stage-class.md`의 Answer): rebuild된 `c1-gaming`과 `c2-p2b`에서, 두 EDF row가 게임의 frame(`game.chain.1`)에 대해 여전히 차이가 없는지. rebuild로 장면이 조금 바뀌었어요: `c1-gaming`에는 compositor가 없고, `c2-p2b`의 background는 이제 OS의 자동 업데이트(`package-upgrade`, 이름 `unattended-upgr`)예요. 대조할 prior table의 gaming row는 §7.2에 있어요.

## 7. 인경민에게 — 답과 알림

### 7.1 저한테 물었던 질문의 답

memo_261010 Part F의 'Questions for jioh' 표 순서예요.

- **TIMER가 밀리면 backlog로 처리할지, frame을 버릴지**(`simulator/notes/note-for-jioh-timer-backlog-vs-drop.md`): 버리는 쪽, skip rule로 정했어요(2026-10-07 TIMER memo). 구현은 §6.2의 (b)예요.
- **`fork_cap`이 무엇을 세는가**(`simulator/notes/note1010.md`): kernel build 파일들(`c1-compile`, `c3-workday`, `c4-compile`, `c6-dual`, generated의 compile 파일)에서 job 하나는 child 여섯이고, 일을 마친 member는 `sh`가 job을 끝낼 때까지 CPU 없이 기다려요. 그래서 `fork_cap` = `make -jN`의 N × 6(`c1-compile`은 8 × 6 = 48)이 동시에 도는 job 수를 정확히 N개로 묶어요 — `-jN`의 단위는 process가 아니라 make job이에요. `c7-compile`의 DKMS module build도 같은 48을 쓰지만 그 job은 member가 6, 8, 10개라서(job 1,557개: 6개짜리 1,325, 8개짜리 145, 10개짜리 87), 거기서는 동시에 살아 있는 child 48개를 묶고 job 수를 정확히 묶지는 않아요. spawn table이 있는 파일에는 모두 `fork_cap`이 있어요.
- **`mock-switch` 질문 1**(slice가 끝났을 때 더 높은 queue에 task가 기다리는 경우): mock이 틀렸어요. MLFQ 규칙대로 44600에 `probe`가 CPU를 가져가도록 fixture를 다시 만들었어요(`harness/tools/tests/fixtures/mock-switch/worked.md`).
- **질문 2**(경쟁자 없이 slice가 끝나는 경우): §9.1의 제안이에요.
- **질문 3**(simulator guide의 예시 program에 instruction 하나가 모자람): 끝의 WAIT는 이제 data의 규칙이고(§4.2), guide의 예시도 세 번째 WAIT로 끝나요.
- **제가 물었던 executor 질문 셋**도 답이 있어요: LOTTERY에서 non-batch class가 비었으면, 두 class가 다 runnable할 때만 `batch_share`로 class를 고르고 아니면 runnable한 class 안에서 균등하게 뽑아요(simulator가 정한 대로); EDF에서 게임 사슬의 깨어나는 stage는 deadline class예요(2026-10-10 답); RUN 중에 온 키 입력은 mailbox에 쌓여요.

### 7.2 prior table의 gaming row

2026-10-10의 답(게임 frame 사슬 전체가 EDF deadline class이고 head의 deadline을 물려받음)을 기준으로, daemon의 prior table(`daemon/driver-table/prior.yaml`)에서 gaming row 둘과 그 검토 문서(`docs/daemon/prior-table-pair-review.md`)를 rebuild된 파일 기준으로 다시 썼어요.

- EDF가 어떤 다른 task보다 frame을 먼저 처리하니, row마다 다른 batch 상한(cap 0.333과 0.05)이 frame 쪽 점수에 닿지 않아요. 그래서 두 row는 frame 점수에서 같아요.
- 기본 MLFQ와의 차이는 EDF 대 MLFQ의 차이예요: MLFQ의 100 ms boost가, 여유가 1.7 ms도 안 되는 frame 도중에 업데이트에게 10 ms slice를 줘요.
- 게임 사슬이 CPU를 쓰는 비율은 `c1-gaming`에서 0.9, `c2-p2a`·`c2-p2b`에서 0.95라 CPU 하나에 들어가지만, `c3-evening`에서는 1.45로 넘쳐요. 1을 넘으면 EDF도 miss를 막지 못하고 순서만 정해요.
- `c2-p2a`의 다운로드는 쉬지 않고 돌아서 batch class예요.

### 7.3 MLFQ boost timer는 적용된 entry마다 다시 시작

harness는 reference simulator가 하는 그대로 읽어요: boost timer는 MLFQ entry가 적용될 때마다, 같은 algorithm entry여도 다시 시작해요(`simulator/src/sim.cpp:597`, `:603`, `:210`). 예를 들어 boost 주기가 100 ms이고 0 ms와 250 ms에 MLFQ entry가 적용되면, boost는 100, 200 ms 다음에 300 ms가 아니라 350, 450 ms…에 와요. harness의 `boost_window`도 이제 entry마다 grid를 새로 깔아요. 그래서 memo_261010 Part F의 'Ours to decide and write down' 표의 "Same-algorithm MLFQ entry: restart the boost grid?" 줄은 지금 동작(restarts)으로 정해졌다고 적어도 돼요.

### 7.4 첫 instruction이 block하는 task의 도착

harness의 mock도 이제 reference simulator와 같아요: 첫 instruction이 WAIT인 task(spawn된 child 포함)는 미리 와 있는 wake가 없으면 도착하자마자 block되고, `ready` line도 길이 0인 CPU 점유도 없어요(simulator의 `on_arrive`, `spawn`). 그래서 같은 표의 "Zero-length occupancy for an arriving task whose first instruction blocks" 줄("none, only `x_block`. The mock has one")도 지금 동작(점유 없이 `x_block`만)으로 정해졌다고 적어도 돼요.

### 7.5 `simulator/src/notes.md` §4의 gap 1과 gap 3

두 gap이 인용한 simulator guide 문장이 고쳐졌어요. 인경민의 tree는 건드리지 않았어요.

- **gap 1**(`batch_bandwidth_cap`을 안 읽음): guide는 이제 "configuration이 정하는 cap 하나, batch class의 상한, 아직 구현 안 됨"이라고 적어요. gap 자체는 그대로 §6.2의 (d)예요.
- **gap 3**(TIMER가 언제부터 세기 시작하는가): guide가 "task가 도착한 시각부터"로 닫혔어요. simulator가 도착할 때 첫 TIMER를 실행하니 이미 그렇게 하고 있어요. 남은 일은 없어요.

### 7.6 workload가 끝난 뒤의 config entry

contract(`docs/data-contracts.md` §7의 End 규칙)는 workload가 끝나는 시각이나 그 뒤에 찍힌 entry를 simulator가 무시한다고 해요. reference simulator는 그런 entry도 적용하고 trace에 적어요. 예를 들어 60 s에 끝나는 workload에 60 s에 찍힌 entry가 있으면 trace에 `{"event":"config_applied","t":60000000,…}`이 남아요. 숫자는 바뀌지 않아요 — harness가 끝 시각이나 그 뒤의 `config_applied` line을 버리기 때문이에요. contract와 harness는 그대로 두고, 차이가 있다는 것만 알려요.

### 7.7 starvation safety net은 만들지 않아요

memo_261010 Part F의 'Implementation owed'에 있는 starvation safety net(오래 굶은 task를 구제하는 장치)은 2026-10-08 declared-class memo에 적은 대로 만들지 않아요. executor에는 그런 장치가 없고, 어떤 task가 30 s보다 오래 기다린 run은 harness의 `starvation_floor` guard가 실패로 처리해요.

### 7.8 파일 크기

simulator가 load할 core 파일 중 가장 큰 건 `c6-dual`(187,601,795 B, 약 187.6 MB), core set 51개 합은 약 678 MB예요(2026-10-17 build). variant 78개와 generated 1,562개는 따로예요. `c6-dual` 하나의 trace는 mock simulator로 약 4,200만 줄이었어요.

## 8. 박이안에게

### 8.1 daemon에 들어오는 것이 바뀌었어요

- visible projection에 task마다 `declared_class`(§3.1)와 focus 구간(§3.2)이 생겼어요.
- telemetry: snapshot의 `focus` field, shape 두 가지(`focus`/`names`), 필수 flag `--telemetry`, recognition log의 top-level `telemetry`(§3.2).
- recognizer가 읽는 `render` 설명이 바뀌었어요(§4.4).
- generated layer 1,562개도 core set과 같은 형식이에요(§3.3).
- rebuild 전 파일로 뽑은 recognition log는 다시 뽑아야 해요. `c5-t3`은 이제 `c6-alias`예요(§4.5).

### 8.2 정해야 할 것: formatted prompt와 chat template의 날짜

recognition log(`docs/data-contracts.md` §8)는 고정된(frozen) contract라서, 바꾸려면 우리 셋의 동의와 기록이 필요해요. 같은 telemetry snapshot이 어느 날 돌려도 같은 입력이 되게 하려고 두 가지를 물어볼게요.

1. recognition log에 formatted prompt(chat template을 적용한 뒤 model이 실제로 받는 text)를 남길까요?
2. chat template이 넣는 날짜 — 예를 들어 Llama 3.1은 prompt에 "Today Date: …"를 넣어요 — 를 prompt에서 고정할까요, 아니면 log에 기록할까요? 날짜가 바뀌면 같은 snapshot이어도 model 입력이 달라져요.

지금 contract와 `daemon/`에는 둘 다 정해진 게 없어요.

## 9. 셋이 같이 정할 제안

### 9.1 경쟁자 없이 MLFQ slice가 끝날 때의 trace (`mock-switch` 질문 2)

**상황.** MLFQ에서 CPU를 잡은 task의 slice가 끝났는데, 기다리는 다른 task가 없어요. task는 한 level 내려가고(demote) 그대로 계속 돌아요. 이걸 trace에 어떻게 적을까요?

```jsonc
// 점유를 끊는 방식
{"event":"x_mlfq_level","t":12000,"task":"hog","from":0,"to":1}
{"event":"run_end","t":12000,"task":"hog","reason":"preempt"}
{"event":"run_start","t":12000,"task":"hog"}

// 제안: 점유 하나가 이어짐
{"event":"x_mlfq_level","t":12000,"task":"hog","from":0,"to":1}
```

- **근거.** Linux(v6.12 `kernel/sched/core.c`의 `__schedule()`)는 다음에 돌 task가 지금 task와 같으면 switch로 세지 않아요.
- **바뀌는 것.** task가 받는 CPU는 어느 쪽이든 같아요. 바뀌는 건 MLFQ trace의 `run_end(preempt)` 개수뿐이고, 그 수는 보고만 하고 점수에는 안 들어가요. harness의 mock은 이미 제안대로 해요. 인경민이 RUN→RUN 수정(memo_261010 Part C)과 같이 구현하면 MLFQ trace가 한 번 바뀌어요.
- 셋 다 동의하면 metrics 문서와 interpretation contract에 적고 contract 변경 기록을 남길게요.

### 9.2 주장을 어떻게 적을까

- 지금 `docs/research-claims.md`의 주장은 recognition 기준이에요: "a language model reading process names recovers the difference, and the strongest name table cannot" — model이 이름을 읽고 상황을 알아보는데, 이름 표로는 못 한다.
- **제안.** scheduling 점수 기준으로 적어요: model이 process 이름을 읽고 고른 설정이, RQ0의 판정 파일들에서 가장 강한 이름 표가 고른 설정보다 점수가 좋다. recognition 정확도(RQ1)는 그 차이를 설명하는 쪽이 되고, 대표 숫자는 "완벽하게 알아봤을 때 얻는 이득 중 model이 얼마를 잡는가", 즉 (fixed − model) / (fixed − perfect recognition)이에요.
- claims 문서는 우리 셋의 것이라 동의 전에는 안 고쳐요.

## 10. 아직 열린 memo

각 memo의 첫머리에 적힌 부탁과 담당 그대로예요.

**인경민**

- `2026-09-07-trace-clarifications-for-the-simulator.md` — zero-wait `ready` line(§6.2의 (a)). 나머지 항목은 답이 있어요.
- `2026-09-08-algorithm-switch-semantics-for-the-simulator.md` — demotion과 boost마다 level을 단 `x_mlfq_level {t, task, from, to}`(지금은 level 없는 `x_mlfq_demote`, `x_mlfq_boost`), 정해진 세 규칙을 simulator의 semantics notes에 적기, switch를 지나도 남은 일이 보존되는지의 unit test.
- `2026-09-09-batch-class-rule-for-the-simulator.md` — `batch_bandwidth_cap`과 그 계산 window(§6.2의 (d)), semantics notes의 규칙, unit test 둘.
- `2026-09-11-invocation-contract.md` — simulator가 contract 10의 command 모양으로 실행되는 것(§6.2의 (h)).
- `2026-10-07-timer-skip-rule-for-the-simulator.md` — skip rule(§6.2의 (b))과 zero-wait `ready` line((a)), 그 뒤 interpretation contract의 TIMER 규칙 확정.
- `2026-10-08-declared-scheduling-class.md` — executor의 idle 규칙(§6.2의 (e)), 그리고 status memo(`simulator/memo/memo_261001.md`) §6의 답 1·2를 RQ0 gate spec이 기다리는 정식 답으로 확인.

**박이안**

- `2026-09-07-repeat-samples-for-the-daemon.md` — 한 query point에서 뽑은 독립 sample N개를 묶는 repeat index를 recognition log에 두고 contract에 한 줄로 정하기(run마다 답이 얼마나 일관된지 재는 측정이 이걸 기다려요).
- `2026-09-11-invocation-contract.md` — daemon이 contract 10의 command 모양으로 실행되는 것. daemon program은 아직 이 저장소에 없어요.
- `2026-09-12-rq0-pre-registration.md` — `random` condition을 어떻게 읽는지와 N = 100을 daemon 쪽에서 확인.

**인지오**

- `2026-09-20-dataset-validity-review.md` — 측정의 안정성 요약(허용오차를 만족한 양, 예외로 실린 양, 가장 큰 불확실성 폭)을 측정 기록에서 script로 계산해, 이번 dataset rebuild를 마무리하는 measurement audit과 함께 `docs/workload/measurement-overview.md`에 실을게요.

## 11. licence

- **code:** MIT, 저장소 root의 `LICENSE`.
- **dataset의 data:** CC-BY-NC-SA-4.0, `dataset/LICENSE`. 대상은 `dataset/` 아래에서 code(`dataset/tools/`, `dataset/Makefile`)와 136M Keystrokes window를 뺀 모든 파일, 거기서 compile된 workload(`dataset/build/`, commit된 manifest가 pin하는 그대로), 측정 campaign의 raw record를 담은 release asset(`dataset/meas-releases.yaml`이 나열하는 것)이에요.
- 저작권자는 둘 다 Jioh In, Kyungmin Inn, Ian Park이에요.
- `dataset/stimulus/`의 입력 stream과 `dataset/meas/streams/`의 SWELL-KW window는 SWELL Knowledge Work dataset(Koldijk et al., 2014; DANS, CC-BY-NC-SA-4.0)에서 가져왔고, `dataset/LICENSE`가 출처를 밝혀요.
- `dataset/meas/streams/aalto-*` window와 `aalto-windows.json`(136M Keystrokes dataset, Dhakal et al., 2018)은 licence의 대상이 아니에요: 출처의 조건(비상업적 사용, 저자 표시) 그대로 배포되고, `dataset/LICENSE`는 그것에 대한 권리를 주지 않아요.
