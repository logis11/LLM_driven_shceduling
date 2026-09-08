# Harness와 records 이해하기 — trace에서 논문의 숫자까지

> Status: draft · Created 2026-09-08 · Updated 2026-09-08

이 문서는 **공부용 문서**예요. Phase 5(primitive metrics and the records pipeline)를 직접 수행하기 위해, harness가 무엇을 읽고 무엇을 쓰는지, `records`의 row 하나가 무슨 뜻인지, 그리고 그 위에 어떤 score가 올라가는지를 OS/시스템 지식이 거의 없는 사람 기준으로 바닥부터 풀어 쓴 거예요. 규범적(normative)인 정의는 Phase 5의 sub-task 5.2에서 쓰게 될 metrics doc이 갖고, 이 문서는 그 문서를 읽고 쓸 수 있게 만드는 다리예요.

읽는 규칙 두 가지. 첫째, term은 영어 그대로 써요. `ready_wait`, `entity`, `trace`, `records` 같은 말은 번역하지 않아요. 둘째, 다른 문서를 가리킬 때 절 번호 대신 내용으로 말해요. "data-contracts 문서의 trace 절"처럼요.

긴 문서예요. 처음 읽을 때는 1장부터 순서대로, 두 번째부터는 목차에서 필요한 곳으로 바로 가면 돼요.

---

## 목차

1. 큰 그림 — harness는 pipeline의 어디에 있나
2. 바닥 지식 — 의자 하나, 손님 여럿
3. simulator가 남기는 것 — trace
4. trace만으로는 모자란 것 — run file
5. Phase 5의 함수 한 줄 — `(run file, trace) → records`
6. records의 모양 — 왜 long format인가, `entity`는 뭔가
7. primitive 하나하나 — 실제 예시로
8. recognition primitives — recognizer의 답을 채점한 row
9. observation window — `T_end` 규칙
10. mock trace 하나를 처음부터 끝까지 손으로 계산하기
11. 두 번째 mock — backlog 상태의 frame task
12. 세 번째 mock — 3단 chain과 늦은 frame 하나
13. harness가 simulator에 기대는 가정
14. records 위에 올라가는 것 — aggregate, normalisation, score
15. 어떤 score가 좋을까 — 파일별로
16. guard — score와 별개로 항상 확인하는 것
17. Phase 5의 sub-task와 이 문서의 대응, harness tree
18. 용어 정리

---

## 1. 큰 그림 — harness는 pipeline의 어디에 있나

이 프로젝트의 실험은 파일을 주고받는 pipeline 하나예요. 세 프로그램이 서로 직접 대화하지 않고, 파일만 넘겨요.

```
 workload dataset                daemon                      simulator                 harness
 (run file, 24개)     ──▶   recognizer + validator   ──▶   scheduler 실행   ──▶   trace 읽기
                                    │                            │                    │
                                    ├─▶ config schedule ─────────┘                    │
                                    │   (언제 어떤 설정으로 바꿀지)                        │
                                    │                                                 │
                                    └─▶ recognition log ─────────────────────────────┤
                                        (recognizer가 뭐라고 답했나)                    │
                                                                                      ▼
                                                                            records ──▶ scores ──▶ report
```

run file 하나(예: `c2-p1a`)는 세 사람에게 세 조각으로 나뉘어 보여요.

- **recognizer**는 process 이름만 봐요. `code`, `python3`. 이름을 보고 "개발 중이고 training run이 돌고 있다"를 맞히는 게 그 일이에요.
- **simulator**는 각 process가 어떻게 행동하는지(program)만 봐요. 이름은 몰라요. 그냥 "이 task는 3 ms 일하고 keystroke를 기다린다"만 알아요.
- **harness**는 정답(`ground_truth`)을 봐요. 이 시간 구간의 진짜 mode가 무엇이었는지. 그리고 simulator가 남긴 trace를 읽어서 숫자를 뽑아요.

이 정보 비대칭이 실험의 핵심이에요. recognizer가 정답을 볼 수 없고, simulator가 이름을 볼 수 없어야 "이름에서 의미를 읽어내는 게 scheduling에 도움이 되나"를 깨끗하게 물을 수 있어요.

harness는 이 그림의 맨 오른쪽이에요. 두 가지를 해요.

1. **recognition을 채점**해요. recognition log의 답을 `ground_truth`와 비교. simulator와 무관해요. 이걸 프로젝트에서는 Layer 1(recognition accuracy)이라고 불러요.
2. **성능을 측정**해요. trace에서 "editor가 keystroke마다 얼마나 기다렸나", "frame이 몇 개 늦었나" 같은 숫자를 뽑아요. Layer 2(consumer performance)예요.

그리고 이 두 가지의 결과를 같은 모양의 파일, `records`에 써요. `records` 위에서 aggregate를 내고 weight를 곱해 score를 만들고, guard를 확인하고, RQ0 gate를 판정하는 건 그 다음 단계예요.

Phase 5는 이 중 **trace를 읽어 records를 쓰는 부분**과, **records에 들어갈 모든 숫자의 정의**를 담당해요. score, guard, gate는 Phase 6과 7이에요.

---

## 2. 바닥 지식 — 의자 하나, 손님 여럿

여기서부터는 OS를 몰라도 돼요. 그림 하나만 갖고 가요.

**CPU는 의자 하나예요.** 이 프로젝트의 simulated machine은 single lane, 즉 의자가 진짜로 하나예요. 프로그램(task)은 손님이고, 의자에 앉아야만 일을 할 수 있어요. 동시에 한 명만 앉아요. **누가 언제 앉을지 정하는 게 scheduler**예요.

손님은 항상 세 상태 중 하나예요.

| 상태 | 뜻 | 비유 |
|---|---|---|
| **running** | 의자에 앉아서 일하는 중 | 앉아 있음 |
| **ready** (runnable) | 일하고 싶은데 의자가 차서 기다리는 중 | 줄 서 있음 |
| **blocked** | 일할 게 없어서 쉬는 중. keystroke나 timer를 기다림 | 소파에서 자는 중 |

scheduler가 하는 일은 딱 하나예요. running인 손님이 의자를 놓을 때(스스로 일이 없어져서, 또는 scheduler가 끌어내려서) ready 줄에서 다음 손님을 고르는 것. 어떤 규칙으로 고르느냐가 algorithm(MLFQ, EDF, LOTTERY, FIFO)이고, 그 규칙의 손잡이가 config예요.

**시간은 virtual time이에요.** simulator는 실제로 프로그램을 돌리지 않아요. "이 task가 3000 µs짜리 일을 시작했다"면 시계를 3000 µs 뒤로 돌려요. 그래서 실행이 몇 초 만에 끝나든 상관없고, 같은 입력이면 항상 같은 결과가 나와요. 모든 시각은 정수 microsecond(µs)예요. 1 ms = 1000 µs, 1 s = 1,000,000 µs.

**task는 작은 program을 따라요.** 각 task는 여섯 가지 명령으로 된 script를 갖고 있어요.

| 명령 | 뜻 | 손님 비유 |
|---|---|---|
| `RUN(N)` | N µs만큼 CPU를 씀 | 앉아서 N만큼 일함 |
| `SLEEP(N)` | N µs 동안 스스로 쉼 | 소파에서 N만큼 잠 |
| `TIMER(P)` | P µs마다 오는 tick을 기다림 | 알람이 P마다 울림 |
| `WAIT(channel)` | 누가 깨워줄 때까지 기다림 | 부를 때까지 소파에서 기다림 |
| `WAKE(target)` | 다른 task를 깨움 | 옆 손님을 깨움 |
| `FORK` / `EXIT` | 자식 task를 만듦 / 자신을 끝냄 | 동행을 부름 / 집에 감 |

editor는 `WAIT(input) → RUN(3000) → WAIT(input) → RUN(4000) → …`예요. keystroke가 올 때까지 자다가, 오면 잠깐 일하고, 다시 자요. 동영상 player는 `LOOP { TIMER(16667) → RUN(6667) }`예요. 16.7 ms마다 알람이 울리고, 울리면 frame 하나를 6.7 ms 동안 그려요. batch job은 `RUN(130000000) → EXIT`예요. 130초짜리 일을 하고 집에 가요.

이 정도면 trace를 읽을 수 있어요. dataset 쪽의 자세한 얘기(archetype, timeline, compile)는 workload 폴더의 coreset 안내 문서(`docs/workload/coreset-guide.md`)에 따로 있어요.

---

## 3. simulator가 남기는 것 — trace

simulator는 **통계를 하나도 계산하지 않아요.** 일어난 일을 시간순으로 적기만 해요. 그 일지가 trace예요.

형식은 JSONL. 한 줄이 JSON object 하나이고, `t` 순서로 정렬되어 있어요. 파일은 `*.trace.jsonl` 또는 gzip으로 눌린 `*.trace.jsonl.gz`이고, harness는 둘 다 stream으로 읽어요.

첫 줄은 header예요.

```jsonc
{"event":"meta", "workload_id":"c1-office", "condition":"fixed",
 "sim":"simulator@<version-or-commit>", "schedule_entries":1}
```

어느 workload를, 어느 condition으로, 어느 simulator 버전이 돌렸는지. records의 identity column이 여기서 나와요.

그 뒤로는 **일곱 종류의 event line**만 와요. 이 일곱 개가 harness가 읽는 closed set이고, 그 외의 것은 `x_`로 시작하는 이름으로만 올 수 있어요(simulator의 debugging용, harness는 통째로 무시).

### 3.1 task의 등장과 퇴장

```jsonc
{"event":"task_arrive", "t":2000000, "task":"build",    "source":"file"}
{"event":"task_arrive", "t":2000105, "task":"build.c1", "source":"spawn", "parent":"build"}
{"event":"task_end",    "t":2158000, "task":"build.c1", "reason":"exit"}
```

`task_arrive`는 손님이 가게에 들어온 것. `source`가 `file`이면 run file에 적힌 시각에 온 것이고, `spawn`이면 부모가 `FORK`로 만든 자식이에요. 자식의 등장 시각은 run file에 없어요. 부모가 언제 `FORK`에 도달하느냐는 scheduler에 달렸으니까요. 그래서 trace에 적어요.

`task_end`는 퇴장. `reason`이 `exit`이면 program이 `EXIT`에 도달해서 스스로 끝난 것, `depart`면 run file에 적힌 시각에 사용자가 앱을 닫은 것.

### 3.2 ready — 일하고 싶어진 순간

```jsonc
{"event":"ready", "t":10000, "task":"editor", "cause":"wake"}
```

task가 blocked에서 ready로 바뀐 순간. `cause`는 왜 깨어났나.

| cause | 뜻 |
|---|---|
| `arrive` | 방금 등장해서 |
| `wake` | 누가 깨워서. keystroke 같은 외부 자극, 또는 다른 task의 `WAKE` |
| `sleep_end` | `SLEEP`이 끝나서 |
| `timer_tick` | `TIMER`의 tick이 와서 |
| `fork_slot` | `FORK`가 slot이 없어 막혀 있다가 자리가 나서 |

이 line이 따로 있는 이유가 중요해요. "keystroke가 온 시각"은 run file에 적혀 있지만, "editor가 그 keystroke를 받을 수 있게 된 시각"은 다를 수 있어요. editor가 이전 burst를 아직 처리 중이면 keystroke는 큐에 쌓여요. harness가 그 순간을 simulator의 semantics를 다시 구현해서 알아내면 안 되니까, simulator가 직접 적어주는 거예요.

Phase 5에서 인경민에게 요청한 규칙 하나가 이 line에 걸려 있어요. **blocking primitive(`WAIT`, `TIMER`, `SLEEP`, fork-slot 대기)가 완료될 때마다 `ready` line을 내라. 실제로는 block되지 않고 즉시 완료됐더라도.** 즉 `ready`는 "task가 runnable해졌다"가 아니라 "blocking primitive 하나가 완료됐다"는 뜻이에요. 왜 필요한지는 11장과 13장에서 나와요.

### 3.3 run_start / run_end — 의자에 앉고 일어남

```jsonc
{"event":"run_start", "t":20000, "task":"editor"}
{"event":"run_end",   "t":23000, "task":"editor", "reason":"block", "blocked_on":"wait"}
```

한 쌍이 occupancy interval 하나예요. 20000에 앉아서 23000에 일어남. 3000 µs 동안 CPU를 썼음.

`run_end`의 `reason`:

| reason | 뜻 |
|---|---|
| `block` | 일이 없어져서 스스로 일어남. `blocked_on`에 뭘 기다리는지(`wait`, `sleep`, `timer`, `fork_slot`) |
| `preempt` | scheduler가 끌어내림. 다른 task 차례라서 |
| `exit` | program이 끝나서 |
| `depart` | 사용자가 앱을 닫아서 |

`preempt`가 특별해요. 일이 남았는데 강제로 일어난 거니까, 그 task는 바로 ready 줄로 돌아가요. 그리고 다음 `run_start`에서 남은 일을 이어서 해요. 1000 µs짜리 `RUN`을 300 µs 하다가 끌려나면 다음에 700 µs를 마저 해요. 총 CPU 사용량은 항상 정확히 1000이에요.

### 3.4 deadline — 주기 작업 하나의 결과

```jsonc
{"event":"deadline", "t":15625, "task":"mpv", "due":16667, "met":true, "slack_us":1042}
```

`TIMER`를 가진 task의 job 하나(frame 하나)가 끝났을 때. `due`는 마감, `met`은 맞췄나, `slack_us`는 여유. harness는 이 line을 **cross-check용**으로만 써요. 자기 계산(7장의 `job`)과 비교해서 다르면 어느 한쪽의 bug예요. 왜 직접 쓰지 않는지는 7장에서.

### 3.5 config_applied — scheduler 설정이 바뀜

```jsonc
{"event":"config_applied", "t":60450000, "index":1, "algorithm":"MLFQ", "provenance":"unmodified"}
```

config schedule의 entry 하나가 적용된 순간. `index`는 schedule에서 몇 번째 entry인지, `algorithm`은 어떤 algorithm으로 바뀌었는지, `provenance`는 이 설정이 어디서 왔는지.

| provenance | 뜻 |
|---|---|
| `unmodified` | recognizer의 답을 validator가 손대지 않고 적용 |
| `clamped` | 답의 숫자가 범위 밖이라 경계로 잘라서 적용 |
| `held` | 답이 거부돼서 이전 설정을 그대로 유지 |
| `fallback` | 기본값. boot 때, 또는 계속 실패해서 |

논문의 모든 성능 숫자 옆에는 이 provenance의 비율이 같이 적혀요. 어떤 condition이 점수를 잘 받았는데 알고 보니 시간의 대부분을 `fallback`으로 돌았다면, recognition이 잘한 게 아니라 기본 MLFQ가 괜찮았던 거예요.

### 3.6 정리: trace 한 조각을 읽어보기

```jsonc
{"event":"meta", "workload_id":"x", "condition":"fixed", "sim":"s@1", "schedule_entries":1}
{"event":"config_applied", "t":0,     "index":0, "algorithm":"MLFQ", "provenance":"fallback"}
{"event":"task_arrive",    "t":0,     "task":"hog", "source":"file"}
{"event":"ready",          "t":0,     "task":"hog", "cause":"arrive"}
{"event":"run_start",      "t":0,     "task":"hog"}
{"event":"ready",          "t":250,   "task":"editor", "cause":"wake"}
{"event":"run_end",        "t":260,   "task":"hog", "reason":"preempt"}
{"event":"run_start",      "t":260,   "task":"editor"}
{"event":"run_end",        "t":263,   "task":"editor", "reason":"block", "blocked_on":"wait"}
{"event":"run_start",      "t":263,   "task":"hog"}
```

말로 풀면: 0에 boot 설정(MLFQ, fallback)이 켜지고, `hog`가 와서 바로 앉았다. 250에 keystroke가 와서 `editor`가 일하고 싶어졌지만 의자에 `hog`가 있다. 260에 scheduler가 `hog`를 끌어내리고 `editor`를 앉혔다. `editor`는 3 µs 일하고 다음 keystroke를 기다리러 갔고, `hog`가 다시 앉았다.

여기서 이미 숫자 하나가 보여요. editor는 250에 일하고 싶어졌고 260에 앉았으니 **10 µs 기다렸다.** 이게 `ready_wait`예요.

---

## 4. trace만으로는 모자란 것 — run file

trace는 **일어난 일**만 적어요. **일어났어야 하는 일**은 안 적어요. 그래서 harness는 run file을 두 번째 input으로 받아요. 세 가지를 읽어요.

### 4.1 `T_end` — 언제까지를 볼 것인가

run file의 `ground_truth`는 label이 붙은 시간 구간(segment)의 목록이에요.

```jsonc
"ground_truth": [
  { "t_start": 0,        "t_end": 60000000,  "mode": "dev",      "attributes": { "background_wanted": true } },
  { "t_start": 60000000, "t_end": 180000000, "mode": "ml-train", "attributes": { "background_wanted": true } }
]
```

마지막 segment의 `t_end`가 workload의 끝이에요. harness는 이걸 `T_end`라 부르고 `[0, T_end]`만 봐요. 자세한 규칙은 9장.

### 4.2 chain topology — 누가 누구를 깨우나

게임 파일에서 frame 하나는 task 16개를 릴레이로 지나가요. run file의 `events`에 각 task의 program이 있으니 거기서 "TIMER를 가진 task에서 시작해 WAKE target을 따라가면 어디서 끝나나"를 읽을 수 있어요. 이게 chain topology이고, frame latency를 계산하려면 꼭 필요해요. 7장의 `job`에서 설명.

### 4.3 demand — 원래 얼마나 일해야 했나

batch task의 program은 `RUN(130000000) → EXIT`예요. 즉 130초짜리 일. trace는 이 task가 CPU를 80초 받았다는 것까지만 말해요. "130초 중 80초"라는 비율을 내려면 130이 필요하고, 그건 run file에서 각 task의 `RUN` 총합으로 읽어요.

세 가지 다 "scheduler가 바꿀 수 없는 것"이에요. `T_end`는 사용자가 정한 시간, chain topology는 프로그램의 구조, demand는 일의 양. scheduler가 바꾸는 건 "언제"뿐이고, "언제"는 trace가 갖고 있어요.

---

## 5. Phase 5의 함수 한 줄 — `(run file, trace) → records`

Phase 5가 만드는 것을 함수 하나로 쓰면 이거예요.

```
primitives(run_file, trace) → records.csv
```

- 실행 파일을 호출하지 않아요. 파일 둘을 읽어서 파일 하나를 써요.
- simulator도 daemon도 필요 없어요. 손으로 쓴 mock trace로 test할 수 있어요.
- trace 하나당 records 파일 하나예요. 24 workload × N condition이면 그만큼의 CSV.
- 이 함수는 "이 파일에서 editor가 interactive task다" 같은 걸 **몰라요.** `ready` line이 있으면 row 하나를 내요. 어느 row가 중요한지는 다음 단계(scoring)가 정해요.

recognition 쪽은 같은 모양의 row를 내지만 input이 달라요.

```
grader(recognition_log, ground_truth, calibrated_table) → records rows (entity=recognizer)
```

이 함수의 **정의**는 Phase 5의 metrics doc에 들어가고, **code**는 Phase 7에서 만들어요.

---

## 6. records의 모양 — 왜 long format인가, `entity`는 뭔가

### 6.1 표를 어떻게 생기게 할 것인가

측정값을 표에 넣는 방법이 둘 있어요.

**wide format**: metric마다 column 하나.

| task | ready_wait | cpu_delivered | turnaround |
|---|---|---|---|
| editor | ??? | 120000 | |

바로 안 되는 게 보여요. editor는 keystroke를 234번 받으니 `ready_wait`가 234개인데 cell 하나에 못 넣어요. `cpu_delivered`는 task당 하나. metric마다 개수가 다르니 한 줄에 못 펴요.

**long format**: "무엇을 쟀는가"를 column 이름이 아니라 cell 값으로 내리는 것.

| entity | metric | t | value |
|---|---|---|---|
| editor | ready_wait | 10000 | 0 |
| editor | ready_wait | 25000 | 3000 |
| editor | ready_wait | 41000 | 0 |
| editor | cpu_delivered | 180000000 | 120000 |

**한 row = 측정 한 번.** 234개면 234 row. metric 종류가 늘어도 column은 안 늘어요. 건강검진 기록과 같아요. "김철수, 혈압, 3월 1일, 120", "김철수, 체중, 3월 1일, 70". 사람마다 혈압 column을 만드는 게 아니라 측정 한 번이 한 줄.

records는 long format이에요. 이유는 셋.

1. metric마다 개수가 달라서 wide로는 표현이 안 돼요.
2. 손으로 계산한 expected value가 그대로 CSV fixture가 돼요. review에서 diff로 보고, CI에서 byte 비교해요.
3. row 하나가 self-contained라서 실험 matrix 전체를 그냥 이어 붙일 수 있어요.

### 6.2 column 18개

세 묶음이에요.

**identity 6개** — 이 row가 어느 실험의 어느 trace에서 왔나.

| column | 뜻 | 예 |
|---|---|---|
| `workload_id` | 어느 workload | `c2-p1a` |
| `condition` | 어느 recognizer | `llm_vocab` |
| `table` | 어느 driver table. `prior` 또는 `calibrated`. `fixed`는 table을 안 쓰니 빈칸 | `prior` |
| `seed` | `random` condition의 PRNG seed. 나머지는 빈칸 | `7` |
| `sim` | simulator 버전 | `simulator@abc123` |
| `source_sha256` | 이 row가 나온 trace(또는 recognition log)의 hash | `9f3a…` |

**observation 4개** — 측정 한 번.

| column | 뜻 |
|---|---|
| `entity` | **누구에 대한** 측정인가 |
| `metric` | **무엇을** 쟀나 |
| `t` | **언제**의 일인가 (anchor time, µs) |
| `value` | **얼마**였나 |

**attribute 8개** — metric에 따라 채워지는 부가 정보. 해당 없으면 빈칸.

| column | 어느 metric이 채우나 | 뜻 |
|---|---|---|
| `cause` | `ready_wait` | 왜 runnable해졌나 (`wake`, `timer_tick`, …) |
| `provenance` | `config_interval` | 설정이 어디서 왔나 |
| `algorithm` | `config_interval` | 어떤 algorithm이었나 |
| `index` | `config_interval` | schedule의 몇 번째 entry였나 |
| `period_us` | `job` | 이 주기 작업의 period. `value > period_us`면 miss |
| `predicted` | `mode_correct`, `attr_correct` | recognizer가 뭐라고 답했나 |
| `truth` | `mode_correct`, `attr_correct` | 정답이 뭐였나 |
| `validation` | recognizer row | validator가 그 답을 어떻게 처리했나 |

### 6.3 `entity`는 어디서 나온 말인가

리서치 문서에 처음 등장하는 말이 맞아요. Phase 5 spec 세션에서 records column을 정하면서 도입했어요. 뜻은 **"이 row가 누구 얘기인가"**예요.

`task`라고 안 한 이유는, task가 아닌 것에 대한 측정도 같은 표에 들어가야 해서예요.

| entity | 무엇 | 예시 metric |
|---|---|---|
| task id (`editor`, `mpv`, `build.c1`, `game.chain.1`, …) | task 하나 | `ready_wait`, `cpu_delivered`, `job` |
| `lane` | CPU 그 자체 | `busy` — CPU가 총 얼마나 바빴나 |
| `schedule` | config schedule | `config_interval` — 설정이 얼마나 유지됐나 |
| `recognizer` | recognizer의 답 | `mode_correct` — 이 query에서 mode를 맞췄나 |

`lane`, `schedule`, `recognizer`는 **예약된 이름**이에요. run file에 이 이름의 task가 있으면 reader가 trace를 거부해요. "누구 얘기인지" 헷갈리면 안 되니까.

### 6.4 row 하나를 읽는 법

```
editor, ready_wait, 10000, 10000, cause=wake
```
"editor가, 시각 10000에, keystroke 때문에 runnable해졌고, CPU를 잡기까지 10000 µs 기다렸다."

```
lane, busy, 180000000, 143200000
```
"CPU가, 180초 window 전체에 대해, 143.2초 바빴다."

```
schedule, config_interval, 60450000, 119550000, provenance=unmodified, algorithm=MLFQ, index=1
```
"schedule의 1번 entry가, 60.45초에 적용됐고, MLFQ였고, validator가 손대지 않은 것이었고, 119.55초 동안 유지됐다."

### 6.5 records에 없는 것

**aggregate가 없어요.** P95도, miss rate도, progress fraction도 없어요. 전부 raw observation이에요. 이게 설계의 핵심이에요.

- primitive(row 하나를 만드는 규칙)를 바꾸면 trace부터 다시 계산해야 해요.
- aggregate(row들을 합치는 규칙)나 weight를 바꾸면 records만 다시 읽으면 돼요. trace는 안 건드려요.
- 논문의 모든 숫자가 "어느 trace의 어느 line"으로 환원돼요.

`c2-p1a`를 예로 들면, 관심 있는 구간은 60–180초예요(training run이 있는 동안). 처음 60초는 editor 혼자라서 latency가 당연히 좋고, 이걸 파일 전체 P95에 섞으면 숫자가 희석돼요. raw row에 `t`가 있으니 scoring 단계에서 `t >= 60000000`으로 filter하면 돼요. primitive는 `ground_truth`를 읽을 필요가 없어요.

---

## 7. primitive 하나하나 — 실제 예시로

이 장은 records에 들어가는 metric 각각을 "어떤 상황에서, trace의 어느 line에서, 어떤 row가 나오는가"로 설명해요. 예시는 ms 단위로 읽기 쉽게 쓰지만 실제 값은 µs예요.

등장인물 둘.
- `editor`: 사람이 타이핑하는 텍스트 에디터. keystroke가 올 때마다 잠깐 일하고 다시 기다림.
- `hog`: 130초짜리 계산을 돌리는 batch 프로그램. 의자만 주면 계속 일함.

### 7.1 `ready_wait` — 줄 서서 기다린 시간

**"일하고 싶어진 순간부터 실제로 의자에 앉기까지 얼마나 걸렸나."**

의자가 비어 있을 때:

```
t=100  ready      editor  cause=wake     ← keystroke가 옴
t=100  run_start  editor                 ← 바로 앉음
t=103  run_end    editor  reason=block   ← 3ms 일하고 다음 keystroke 기다리러 감
```

`ready_wait = 100 − 100 = 0`. 즉각 반응.

`hog`가 의자에 있을 때:

```
t=200  run_start  hog
t=250  ready      editor  cause=wake     ← keystroke. 의자에 hog가 있음
t=260  run_end    hog     reason=preempt ← scheduler가 hog를 끌어내림
t=260  run_start  editor
```

`ready_wait = 260 − 250 = 10 ms`. 타이핑하고 글자가 10 ms 뒤에 찍힌 것.

```
entity=editor, metric=ready_wait, t=250, value=10, cause=wake
```

**규칙:** `ready` line 하나마다 row 하나. `t`는 `ready`의 시각, `value`는 그 task의 다음 `run_start`까지의 시간. `cause`를 row에 실어요.

**특수 규칙:** `ready`가 그 task의 **자기 occupancy 안**에 떨어지면(즉 `run_start`와 `run_end` 사이에) `value = 0`. 이건 "block되지 않고 즉시 완료된 blocking primitive"의 경우예요. 11장에서 실제로 봐요.

**왜 하나의 generic primitive인가.** interaction latency(keystroke 대기), response time(등장 후 첫 실행까지), timer dispatch delay(tick 후 실행까지), starvation(가장 오래 기다린 시간)은 전부 이 row들의 filter와 aggregate예요.

| 이름 | records에서 |
|---|---|
| interaction latency | `cause=wake`인 row들 |
| response time | `cause=arrive`인 row |
| timer dispatch delay | `cause=timer_tick`인 row들 |
| starvation | task별 `ready_wait`의 최대값 (어떤 cause든) |

starvation이 "`ready`부터"이지 "arrive부터"가 아닌 이유: 스스로 자고 있는 task는 굶는 게 아니에요. 깨어나서 줄 선 시간만 세요.

### 7.2 `job` — 주기 작업 하나가 걸린 시간

**"16.7 ms마다 frame 하나 그려야 하는 프로그램이, 각 frame을 tick 후 얼마 만에 끝냈나."**

동영상 player `mpv`는 `LOOP { TIMER(16667) → RUN(6667) }`예요. tick k에 시작한 일을 job k라고 불러요. job k는 **tick k가 소비될 때 시작**하고, **task가 다음 TIMER에 도달할 때 끝나요.**

```
t=0.0   ready      mpv  cause=timer_tick   ← tick 0
t=0.0   run_start  mpv
t=6.7   run_end    mpv  reason=block blocked_on=timer  ← frame 다 그리고 다음 tick 기다림
t=16.7  ready      mpv  cause=timer_tick   ← tick 1
t=16.7  run_start  mpv
t=23.4  run_end    mpv  reason=block blocked_on=timer
```

job 0: tick 0.0, 완료 6.7 → value 6.7. period 16.7보다 작으니 제때.

```
entity=mpv, metric=job, t=0,    value=6.7,  period_us=16.7
entity=mpv, metric=job, t=16.7, value=6.7,  period_us=16.7
```

늦는 경우:

```
t=33.4  ready      mpv  cause=timer_tick   ← tick 2. hog가 의자에 있음
t=45.0  run_start  mpv                     ← 11.6 ms 기다림
t=51.7  run_end    mpv  reason=block
```

job 2: tick 33.4, 완료 51.7 → value 18.3 > 16.7. **miss.** 화면이 한 frame 끊긴 것.

```
entity=mpv, metric=job, t=33.4, value=18.3, period_us=16.7
```

miss 여부는 저장 안 해요. `value > period_us`로 읽는 쪽이 계산.

**game chain은 왜 특별한가.** 게임 파일에서 frame은 task 16개를 릴레이로 지나가요.

```
game.chain.1   LOOP { TIMER(16667) → RUN → WAKE game.chain.2 }
game.chain.2   LOOP { WAIT(chain:game.chain.2) → RUN → WAKE game.chain.3 }
   …
game.chain.16  LOOP { WAIT(chain:game.chain.16) → RUN }
```

TIMER는 **첫 task에만** 있어요. 그래서 simulator가 내는 `deadline` line은 `game.chain.1`의 것이고, 그건 "입력 처리 stage가 자기 몫(1 ms 미만)을 tick 안에 끝냈나"만 답해요. 거의 항상 yes예요. 정작 "frame이 화면에 나왔나"는 `game.chain.16`이 k번째 iteration을 끝낸 시각인데, trace에 "이게 frame k다"라고 적힌 line은 없어요.

그래서 harness가 **재구성**해요. run file에서 TIMER를 가진 task를 찾고, WAKE target을 따라가서 tail을 찾아요(`game.chain.1 → 2 → … → 16`). frame k의 latency = tail의 k번째 iteration 끝 − tick k. 이 규칙은 구조적이에요. `.chain.` 같은 이름 규칙에 의존하지 않아요.

단일 TIMER task(`mpv`)는 길이 1짜리 chain이라 같은 규칙이 그대로 적용돼요. 그 결과가 simulator의 `deadline` line과 같아야 하니, `deadline`은 공짜 cross-check가 돼요.

**규칙:** tick 하나마다 row 하나. entity는 chain의 head(또는 단일 TIMER task). `t` = tick 시각, `value` = 완료 − tick, `period_us`를 row에. harness는 tail의 iteration 수가 head의 tick 수와 같은지 guard해요.

12장에서 3단 chain을 실제로 계산해요.

### 7.3 `cpu_delivered` — 의자에 앉아 있던 시간의 합

**"window 안에서 이 task가 CPU를 총 얼마나 받았나."**

```
t=60000   run_start  hog
t=60050   run_end    hog  reason=preempt   ← 50
t=60070   run_start  hog
t=60120   run_end    hog  reason=preempt   ← 50
  … 수천 조각 …
```

조각을 다 더해요. `T_end`에서 잘라요. `T_end`에 아직 앉아 있으면 `T_end`까지만 세요.

```
entity=hog, metric=cpu_delivered, t=180000, value=80000
```

### 7.4 `demand` — 원래 필요한 시간

**"이 task의 program에 적힌 RUN의 총합."** run file에서 읽어요. trace에는 없어요.

```
entity=hog, metric=demand, t=180000, value=130000
```

progress fraction = `cpu_delivered / demand` = 80000/130000 ≈ 0.62는 scoring이 나눠요. records에는 재료만.

**왜 records에 넣나.** scoring spec이 "hog의 demand는 130초"를 손으로 적어두면, dataset이 re-sampling될 때 숫자가 어긋나요. records에 있으면 항상 그 trace를 만든 run file의 값이에요.

### 7.5 `completed` — 끝났나

**"window 안에서 `task_end(reason=exit)`이 있으면 1, 아니면 0."**

```
entity=hog, metric=completed, t=180000, value=0
```

`c2-p1a`의 `hog`는 130초짜리 일을 60초에 시작하고 파일은 180초에 끝나요. 절대 못 끝나요. 그래서 `completed=0`이고 `turnaround` row는 아예 안 나와요. "늦게 끝났다"가 아니라 "window 안에 안 끝났다"예요. simulator가 그 뒤를 더 돌렸든 말든 안 봐요.

segment-bound task(사용자가 닫는 앱)는 `task_end`의 `reason`이 `depart`라서 항상 `completed=0`이에요. scoring은 이 row를 무시해요. finite task(batch, compile child)에서만 의미가 있어요.

### 7.6 `turnaround` — 등장부터 퇴장까지

**"나타나서 완전히 끝날 때까지 벽시계로 얼마나 걸렸나."** `completed=1`일 때만 row가 나와요.

```
t=2000   task_arrive  build.c1
  … 다른 task들과 의자를 나눠 씀 …
t=2158   task_end     build.c1  reason=exit
```

`turnaround = 2158 − 2000 = 158`. 실제 일한 시간 + 줄 선 시간.

```
entity=build.c1, metric=turnaround, t=2158, value=158
```

`c1-compile`의 makespan(빌드 전체 시간)은 `make`의 `turnaround`예요. `make`는 자식 100개가 다 끝나길 기다렸다가 `EXIT`하니까요. 각 `cc1` 자식도 자기 row를 갖는데, 자식의 등장 시각은 trace의 `task_arrive(source=spawn)`에서 와요.

### 7.7 `preempt_count` — 강제로 끌려 내려온 횟수

**"일하는 중에 scheduler가 끌어내린 횟수."** `run_end(reason=preempt)`의 개수.

```
entity=hog, metric=preempt_count, t=180000, value=3
```

끌어내리는 건 공짜가 아니에요(context switch 비용). 너무 많으면 그것대로 문제예요.

### 7.8 `busy` — 의자가 비어 있지 않던 시간

**"window 안에서 누군가 의자에 앉아 있던 시간의 합."** 모든 task의 occupancy interval을 다 더한 것.

```
entity=lane, metric=busy, t=180000, value=143200
```

entity가 `lane`인 건 특정 task 얘기가 아니라 CPU 얘기라서. idle = `T_end − busy`. utilisation = `busy / T_end`. 이건 주로 sanity check예요. workload가 의자를 100–150% 요구하도록 설계했으니 busy가 이상하게 낮으면 뭔가 잘못된 것.

### 7.9 `config_interval` — 설정이 얼마나 유지됐나

**"config schedule의 각 entry가 적용된 후 다음 entry(또는 `T_end`)까지 얼마나 유지됐나."**

```
t=0       config_applied  index=0  algorithm=MLFQ  provenance=fallback
t=60450   config_applied  index=1  algorithm=EDF   provenance=unmodified
```

```
entity=schedule, metric=config_interval, t=0,     value=60450,  provenance=fallback,   algorithm=MLFQ, index=0
entity=schedule, metric=config_interval, t=60450, value=119550, provenance=unmodified, algorithm=EDF,  index=1
```

이 row들에서 provenance 비율("`fallback`으로 돈 시간의 비율")과 config age가 나와요. guard가 trace를 직접 읽지 않고 records를 읽게 하려고 여기 넣어요.

### 7.10 한 줄 요약표

| metric | 한국어로 | entity | 몇 row | trace의 어디서 | run file에서 |
|---|---|---|---|---|---|
| `ready_wait` | 줄 선 시간 | task | `ready`마다 | `ready` → 다음 `run_start` | — |
| `job` | 주기 작업 하나 걸린 시간 | chain head | tick마다 | `ready(timer_tick)` + run line + tail의 iteration | chain topology |
| `cpu_delivered` | 앉은 시간 합 | task | task당 1 | 모든 `run_start`~`run_end`, `T_end`에서 clip | `T_end` |
| `demand` | 원래 필요한 시간 | task | task당 1 | — | RUN 총합 |
| `completed` | 끝났나 | task | task당 1 | `task_end(exit)` 유무 | `T_end` |
| `turnaround` | 등장부터 퇴장까지 | task | completed일 때 1 | `task_arrive` → `task_end(exit)` | — |
| `preempt_count` | 끌려온 횟수 | task | task당 1 | `run_end(preempt)` 개수 | — |
| `busy` | 의자가 찬 시간 합 | `lane` | trace당 1 | 모든 run interval | `T_end` |
| `config_interval` | 설정 유지 시간 | `schedule` | `config_applied`마다 | `config_applied` → 다음 것 | `T_end` |

---

## 8. recognition primitives — recognizer의 답을 채점한 row

Layer 1은 simulator와 무관해요. recognition log를 `ground_truth`와 비교해요.

recognition log는 query point마다 entry 하나예요. query point는 "process 이름의 집합이 바뀐 순간"이에요. `c2-p1a`라면 0초(`code` 등장), 60초(`python3` 등장), 180초(`code` 퇴장)의 셋.

```jsonc
{ "t_set_change": 60000000,
  "telemetry": { "t_us": 60000000, "processes": [ {"name":"code","count":1}, {"name":"python3","count":1} ] },
  "proposal":  { "system": { "mode": "ml-train", "background_wanted": true }, … },
  "validation": "unmodified",
  "latency_us": 450000 }
```

이 entry 하나에서 나오는 row들. entity는 `recognizer`, `t`는 `t_set_change`.

```
recognizer, mode_correct, 60000000, 1, predicted=ml-train, truth=ml-train, validation=unmodified
recognizer, attr_correct, 60000000, 1, predicted=true,     truth=true,     validation=unmodified
recognizer, latency_us,   60000000, 450000
recognizer, validation,   60000000, unmodified
```

`llm_algo` condition(LLM이 algorithm까지 고르는 조건)에서만 row 하나 더:

```
recognizer, algo_choice_correct, 60000000, 1, predicted=MLFQ, truth=MLFQ
```

`truth`는 calibrated driver table에서 정답 row의 default algorithm이에요. 그래서 grader는 table 파일도 input으로 받아요.

**채점 범위:** `ambiguous`가 아닌 `ground_truth` segment가 `t_set_change`를 덮는 query만 채점해요. 마지막 snapshot(모든 앱이 닫힌 순간)은 덮는 segment가 없으니 건너뛰어요. `c6-dual`의 `ambiguous` segment도 채점 대상이 아니에요.

mode accuracy, attribute accuracy, confusion matrix, latency 분포는 전부 이 row들의 aggregate예요.

run-to-run consistency(같은 snapshot에 매번 같은 답을 하나)는 같은 query point의 sample이 여러 개 있어야 계산돼요. 지금 log 형식에는 "이게 몇 번째 sample인지"의 index가 없어서 박이안에게 memo로 요청해뒀어요.

---

## 9. observation window — `T_end` 규칙

모든 primitive는 `[0, T_end]` 안에서 측정돼요. `T_end`는 run file의 마지막 segment의 끝.

- `t > T_end`인 observation은 버려요. `ready`가 `T_end` 뒤면 row 없음.
- CPU 회계는 `T_end`에서 잘라요. `T_end`에 열려 있는 occupancy interval은 `T_end`까지만 세요.
- `T_end`에 살아 있는 task는 "window 안에 안 끝남"이에요. `completed=0`, `turnaround` 없음.
- simulator가 `T_end` 뒤를 더 돌렸든 말든 어떤 숫자에도 영향 없어요.

왜 이 규칙이 필요한가. 어느 문서도 "run이 언제 끝나는가"를 정해두지 않았어요. `c2-p1a`의 `hog`는 180초 뒤에도 혼자 계속 돌 수 있어요. simulator가 거기서 멈추든 계속 가든, harness가 `T_end`에서 자르면 숫자는 같아요. 그래서 인경민에게는 "멈춰도 안전하다"고 조언만 했고, contract에는 넣지 않았어요.

또 하나. `T_end`는 label이 붙은 시간의 끝이에요. label 없는 시간에 일어난 일은 채점할 근거가 없어요.

---

## 10. mock trace 하나를 처음부터 끝까지 손으로 계산하기

Phase 5의 sub-task 5.1에서 실제로 하게 될 일이에요. 여기서는 축소한 `c2-p1a`로 해요. 숫자는 손으로 따라갈 수 있게 작게 잡았어요. 실제 mock을 만들 때는 이 문서의 숫자를 그대로 쓸 필요 없어요.

### 10.1 reduced run file

```jsonc
{
  "meta": { "id": "mock-c2-p1a", "derived_from": "hand-written", "sampled": { "seed": 0, "archetypes": "n/a" } },
  "ground_truth": [
    { "t_start": 0,     "t_end": 40000,  "mode": "dev",      "attributes": { "background_wanted": true } },
    { "t_start": 40000, "t_end": 100000, "mode": "ml-train", "attributes": { "background_wanted": true } }
  ],
  "events": [
    { "op": "arrive", "t": 0, "id": "editor", "name": "code", "depart": 100000,
      "program": [ { "op": "WAIT", "channel": "input:editor" }, { "op": "RUN", "us": 3000 },
                   { "op": "WAIT", "channel": "input:editor" }, { "op": "RUN", "us": 4000 },
                   { "op": "WAIT", "channel": "input:editor" }, { "op": "RUN", "us": 2000 } ] },
    { "op": "arrive", "t": 40000, "id": "hog", "name": "python3",
      "program": [ { "op": "RUN", "us": 80000 }, { "op": "EXIT" } ] },
    { "op": "wake", "t": 10000, "channel": "input:editor", "target": "editor" },
    { "op": "wake", "t": 22000, "channel": "input:editor", "target": "editor" },
    { "op": "wake", "t": 45000, "channel": "input:editor", "target": "editor" }
  ]
}
```

run file에서 읽는 세 가지:
- `T_end` = 100000 (마지막 segment의 `t_end`)
- chain topology: TIMER를 가진 task가 없으니 chain 없음
- demand: `editor` = 3000 + 4000 + 2000 = 9000, `hog` = 80000

미리 보이는 것: `hog`는 40000에 와서 80000짜리 일을 해야 하는데 window가 60000밖에 안 남았어요. 못 끝나요. editor 혼자면 그것도 못 끝났을 거예요. 실제 `c2-p1a`와 같은 구조예요.

### 10.2 config schedule (이 trace를 만든 조건)

condition `llm_vocab`, prior table. boot 설정이 0에, recognizer의 답이 40000 + latency 450 = 40450에 적용돼요.

### 10.3 trace

scheduler는 아무 legal한 것이어도 돼요. 이 mock은 "keystroke가 오면 1 ms 안에 editor에게 의자를 넘기는 MLFQ"를 가정했어요. 시각은 µs.

```jsonl
{"event":"meta","workload_id":"mock-c2-p1a","condition":"llm_vocab","sim":"mock@0","schedule_entries":2}
{"event":"config_applied","t":0,"index":0,"algorithm":"MLFQ","provenance":"fallback"}
{"event":"task_arrive","t":0,"task":"editor","source":"file"}
{"event":"ready","t":0,"task":"editor","cause":"arrive"}
{"event":"run_start","t":0,"task":"editor"}
{"event":"run_end","t":0,"task":"editor","reason":"block","blocked_on":"wait"}
{"event":"ready","t":10000,"task":"editor","cause":"wake"}
{"event":"run_start","t":10000,"task":"editor"}
{"event":"run_end","t":13000,"task":"editor","reason":"block","blocked_on":"wait"}
{"event":"ready","t":22000,"task":"editor","cause":"wake"}
{"event":"run_start","t":22000,"task":"editor"}
{"event":"run_end","t":26000,"task":"editor","reason":"block","blocked_on":"wait"}
{"event":"task_arrive","t":40000,"task":"hog","source":"file"}
{"event":"ready","t":40000,"task":"hog","cause":"arrive"}
{"event":"run_start","t":40000,"task":"hog"}
{"event":"config_applied","t":40450,"index":1,"algorithm":"MLFQ","provenance":"unmodified"}
{"event":"ready","t":45000,"task":"editor","cause":"wake"}
{"event":"run_end","t":46000,"task":"hog","reason":"preempt"}
{"event":"run_start","t":46000,"task":"editor"}
{"event":"run_end","t":48000,"task":"editor","reason":"block","blocked_on":"wait"}
{"event":"run_start","t":48000,"task":"hog"}
{"event":"task_end","t":100000,"task":"editor","reason":"depart"}
{"event":"run_end","t":122000,"task":"hog","reason":"exit"}
{"event":"task_end","t":122000,"task":"hog","reason":"exit"}
```

말로 풀면:

| 시각 | 일어난 일 |
|---|---|
| 0 | boot 설정 적용. editor 등장, 앉자마자 첫 명령이 `WAIT`라 바로 일어남(길이 0짜리 occupancy) |
| 10000 | keystroke 1. 의자가 비어 있어 바로 앉음. 3000 일하고 다음 keystroke 기다림 |
| 22000 | keystroke 2. 바로 앉음. 4000 일함 |
| 40000 | hog 등장, 바로 앉음. 80000짜리 일 시작 |
| 40450 | recognizer의 답(ml-train, wanted) 적용. `unmodified` |
| 45000 | keystroke 3. 의자에 hog가 있음. editor는 줄 섬 |
| 46000 | scheduler가 hog를 끌어내림(`preempt`). editor 앉음. 2000 일함 |
| 48000 | editor 끝. hog 다시 앉음 |
| 100000 | `T_end`. editor 퇴장(`depart`). hog는 아직 앉아 있음 |
| 122000 | hog 일 끝남(`exit`). window 밖 |

시각 0의 "길이 0짜리 occupancy"는 이 mock이 정한 거예요. task가 등장하면 runnable이 되고, 의자에 앉아 첫 명령 `WAIT`를 실행하니 즉시 block. simulator가 이걸 다르게 표현할 수도 있어요(예: `ready(arrive)` 없이 바로 blocked). 그건 인경민의 결정이고, 결정이 나면 mock을 그에 맞춰 바꿔요. mock이 어떤 가정을 갖고 있는지는 metrics doc 한 곳에 목록으로 적어둬요.

### 10.4 records 계산

identity column은 모든 row가 같아요. `workload_id=mock-c2-p1a`, `condition=llm_vocab`, `table=prior`, `seed=` (빈칸), `sim=mock@0`, `source_sha256=` (trace 파일의 sha256). 아래에서는 observation과 attribute만 써요.

**`ready_wait`** — `ready` line 5개 → row 5개.

| ready line | 다음 run_start | value | row |
|---|---|---|---|
| t=0 editor arrive | 0 | 0 | `editor, ready_wait, 0, 0, cause=arrive` |
| t=10000 editor wake | 10000 | 0 | `editor, ready_wait, 10000, 0, cause=wake` |
| t=22000 editor wake | 22000 | 0 | `editor, ready_wait, 22000, 0, cause=wake` |
| t=40000 hog arrive | 40000 | 0 | `hog, ready_wait, 40000, 0, cause=arrive` |
| t=45000 editor wake | 46000 | 1000 | `editor, ready_wait, 45000, 1000, cause=wake` |

**`job`** — TIMER task 없음. row 없음.

**task lifetime** — task마다.

editor:
- occupancy: [0,0], [10000,13000], [22000,26000], [46000,48000] → `cpu_delivered` = 0 + 3000 + 4000 + 2000 = 9000
- `task_end`가 `depart`라서 `completed` = 0, `turnaround` 없음
- `demand` = 9000
- `preempt_count` = 0

hog:
- occupancy: [40000,46000], [48000, 열림) → `T_end`에서 clip: [48000,100000] → `cpu_delivered` = 6000 + 52000 = 58000
- `task_end(exit)`은 122000, window 밖 → `completed` = 0, `turnaround` 없음
- `demand` = 80000
- `preempt_count` = 1

| row |
|---|
| `editor, cpu_delivered, 100000, 9000` |
| `editor, completed, 100000, 0` |
| `editor, demand, 100000, 9000` |
| `editor, preempt_count, 100000, 0` |
| `hog, cpu_delivered, 100000, 58000` |
| `hog, completed, 100000, 0` |
| `hog, demand, 100000, 80000` |
| `hog, preempt_count, 100000, 1` |

task 전체에 대한 값의 `t`는 `T_end`로 적었어요. `completed=1`이면 `t`는 `task_end`의 시각이에요. 이 anchor 규칙은 spec에 "completed는 그 시각에"라고만 있고 나머지는 5.2에서 확정해요.

**`config_interval`** — `config_applied` 2개 → row 2개.

| entry | 적용 | 다음 entry 또는 T_end | value | row |
|---|---|---|---|---|
| index 0 | 0 | 40450 | 40450 | `schedule, config_interval, 0, 40450, provenance=fallback, algorithm=MLFQ, index=0` |
| index 1 | 40450 | 100000 | 59550 | `schedule, config_interval, 40450, 59550, provenance=unmodified, algorithm=MLFQ, index=1` |

**`busy`** — 모든 occupancy의 합 = 9000 + 58000 = 67000.

| row |
|---|
| `lane, busy, 100000, 67000` |

### 10.5 완성된 expected CSV

```
workload_id,condition,table,seed,sim,source_sha256,entity,metric,t,value,cause,provenance,algorithm,index,period_us,predicted,truth,validation
mock-c2-p1a,llm_vocab,prior,,mock@0,<sha>,editor,ready_wait,0,0,arrive,,,,,,,
mock-c2-p1a,llm_vocab,prior,,mock@0,<sha>,editor,ready_wait,10000,0,wake,,,,,,,
mock-c2-p1a,llm_vocab,prior,,mock@0,<sha>,editor,ready_wait,22000,0,wake,,,,,,,
mock-c2-p1a,llm_vocab,prior,,mock@0,<sha>,hog,ready_wait,40000,0,arrive,,,,,,,
mock-c2-p1a,llm_vocab,prior,,mock@0,<sha>,editor,ready_wait,45000,1000,wake,,,,,,,
mock-c2-p1a,llm_vocab,prior,,mock@0,<sha>,editor,cpu_delivered,100000,9000,,,,,,,,
mock-c2-p1a,llm_vocab,prior,,mock@0,<sha>,editor,completed,100000,0,,,,,,,,
mock-c2-p1a,llm_vocab,prior,,mock@0,<sha>,editor,demand,100000,9000,,,,,,,,
mock-c2-p1a,llm_vocab,prior,,mock@0,<sha>,editor,preempt_count,100000,0,,,,,,,,
mock-c2-p1a,llm_vocab,prior,,mock@0,<sha>,hog,cpu_delivered,100000,58000,,,,,,,,
mock-c2-p1a,llm_vocab,prior,,mock@0,<sha>,hog,completed,100000,0,,,,,,,,
mock-c2-p1a,llm_vocab,prior,,mock@0,<sha>,hog,demand,100000,80000,,,,,,,,
mock-c2-p1a,llm_vocab,prior,,mock@0,<sha>,hog,preempt_count,100000,1,,,,,,,,
mock-c2-p1a,llm_vocab,prior,,mock@0,<sha>,schedule,config_interval,0,40450,,fallback,MLFQ,0,,,,
mock-c2-p1a,llm_vocab,prior,,mock@0,<sha>,schedule,config_interval,40450,59550,,unmodified,MLFQ,1,,,,
mock-c2-p1a,llm_vocab,prior,,mock@0,<sha>,lane,busy,100000,67000,,,,,,,,
```

row의 순서(entity별? metric별? t별?)는 5.2에서 정해요. byte 비교를 하려면 정해져 있어야 해요.

### 10.6 이 records에서 읽히는 것

scoring이 아니라 "이 row들로 뭘 말할 수 있나"의 맛보기.

- editor의 keystroke 대기: `cause=wake` row 3개, value [0, 0, 1000]. 최대 1 ms. 100 ms 임계값을 넘은 건 0개.
- hog의 progress: 58000 / 80000 = 72.5%.
- fallback으로 돈 비율: 40450 / 100000 = 40.45%. 이 파일에서는 당연해요. training run이 40000에 와야 recognizer가 뭔가 할 수 있으니까.
- utilisation: 67000 / 100000 = 67%.

여기서 "editor가 interactive task다", "hog가 batch다"를 harness는 몰라요. scoring이 `c2-p1a`의 scoring spec을 읽고 "editor의 `ready_wait(cause=wake)`를 보라"고 정해요.

---

## 11. 두 번째 mock — backlog 상태의 frame task

`c1-media`를 축소한 것. 이 mock의 목적은 **"`ready` line이 즉시 완료된 blocking primitive에서도 나와야 한다"**는 규칙이 왜 필요한지 보여주는 거예요.

`mpv`: `LOOP { TIMER(16667) → RUN(6667) }`. tick은 0, 16667, 33334, 50001, 66668, 83335, …
어떤 다른 task(`x`)가 20000부터 60000까지 의자를 독점한다고 해요.

### 11.1 trace (mpv 부분만)

```jsonl
{"event":"ready","t":0,"task":"mpv","cause":"timer_tick"}
{"event":"run_start","t":0,"task":"mpv"}
{"event":"run_end","t":6667,"task":"mpv","reason":"block","blocked_on":"timer"}
{"event":"ready","t":16667,"task":"mpv","cause":"timer_tick"}
{"event":"run_start","t":16667,"task":"mpv"}
{"event":"run_end","t":23334,"task":"mpv","reason":"block","blocked_on":"timer"}
{"event":"ready","t":33334,"task":"mpv","cause":"timer_tick"}
{"event":"run_start","t":60000,"task":"mpv"}
{"event":"ready","t":66667,"task":"mpv","cause":"timer_tick"}
{"event":"ready","t":73334,"task":"mpv","cause":"timer_tick"}
{"event":"run_end","t":80001,"task":"mpv","reason":"block","blocked_on":"timer"}
{"event":"ready","t":83335,"task":"mpv","cause":"timer_tick"}
{"event":"run_start","t":83335,"task":"mpv"}
```

무슨 일이 일어났나:

- frame 0, 1: 정상. tick에 바로 앉아 6667 일하고 다음 tick 기다림.
- tick 2 (33334): mpv가 runnable해졌지만 `x`가 의자에 있음. 60000까지 기다림.
- 60000에 앉아서 frame 2를 그림. 66667에 끝나고 다음 `TIMER`에 도달. 그런데 tick 3 (50001)은 이미 지났어요. backlog 규칙: **지나간 tick의 TIMER는 즉시 완료.** mpv는 block되지 않고 바로 frame 3을 그려요. 이때 `ready(timer_tick)` line이 66667에 찍혀요. mpv가 이미 running인 상태에서.
- 73334에 frame 3 끝. tick 4 (66668)도 지났으니 또 즉시 완료. `ready` 73334. frame 4.
- 80001에 frame 4 끝. tick 5 (83335)는 아직 안 왔으니 이제야 진짜로 block.
- 83335에 tick 5. 정상 복귀.

**`ready` line이 즉시 완료된 TIMER에서도 나오지 않았다면** 60000부터 80001까지는 `run_start` 하나, `run_end` 하나뿐인 20001 µs짜리 occupancy 하나예요. frame 2, 3, 4의 경계가 trace에 없어요. 정확히 늦은 frame들만 안 보이게 되는 거예요. 그래서 인경민에게 이 규칙을 요청했어요.

### 11.2 records

**`ready_wait`**: 자기 occupancy 안에 떨어진 `ready`는 value 0.

| ready | 다음 run_start | value | 비고 |
|---|---|---|---|
| 0 | 0 | 0 | |
| 16667 | 16667 | 0 | |
| 33334 | 60000 | 26666 | 진짜 기다림 |
| 66667 | (running 중) | 0 | occupancy [60000, 80001] 안 |
| 73334 | (running 중) | 0 | 같음 |
| 83335 | 83335 | 0 | |

**`job`**: tick마다. 완료 = 다음 TIMER에 도달한 시각 = 그 iteration의 `RUN`이 끝난 시각.

| k | tick | 완료 | value | period 16667 대비 |
|---|---|---|---|---|
| 0 | 0 | 6667 | 6667 | met |
| 1 | 16667 | 23334 | 6667 | met |
| 2 | 33334 | 66667 | 33333 | **miss** |
| 3 | 50001 | 73334 | 23333 | **miss** |
| 4 | 66668 | 80001 | 13333 | met |

```
mpv, job, 0,     6667,  period_us=16667
mpv, job, 16667, 6667,  period_us=16667
mpv, job, 33334, 33333, period_us=16667
mpv, job, 50001, 23333, period_us=16667
mpv, job, 66668, 13333, period_us=16667
```

frame 4는 tick 66668에 시작했어야 하는데 실제로는 73334에 시작해서 80001에 끝났어요. tick부터 재면 13333이라 met. "tick k에 마감이 tick k+1"이라는 정의 그대로예요.

harness는 `ready(cause=timer_tick)` 개수(6개)가 window 안의 tick 개수와 맞는지도 확인할 수 있어요. tick을 skip하는 simulator면 여기서 걸려요.

`spotify`(`TIMER(50000) → RUN(2500)`)는 같은 파일에 있지만 이 예시에서는 생략했어요. 실제 mock에는 둘 다 들어가요.

---

## 12. 세 번째 mock — 3단 chain과 늦은 frame 하나

게임 chain을 3단으로 축소. 목적은 **frame latency를 harness가 재구성하는 규칙**과 **head의 `deadline` line이 왜 frame latency가 아닌지**를 보여주는 것.

run file의 program:

```
s1  LOOP { TIMER(16667) → RUN(1000) → WAKE s2 }     ← head (TIMER 있음)
s2  LOOP { WAIT(chain:s2) → RUN(2000) → WAKE s3 }
s3  LOOP { WAIT(chain:s3) → RUN(1500) }              ← tail
```

chain topology: s1에서 시작해 WAKE를 따라 s1 → s2 → s3. head = s1, tail = s3. 한 frame의 순수 일 = 4500.

어떤 task `x`가 16667부터 30000까지 의자를 독점한다고 해요. `T_end` = 40000.

### 12.1 trace (chain 부분만, 요약)

| 시각 | 일 |
|---|---|
| 0 | tick 0. s1 ready+run 0–1000. WAKE s2. s2 ready 1000, run 1000–3000. WAKE s3. s3 ready 3000, run 3000–4500 |
| 16667 | tick 1. s1 ready. 하지만 x가 의자에 있음 |
| 30000 | x 끝. s1 run 30000–31000. WAKE s2. s2 run 31000–33000. WAKE s3. s3 run 33000–34500 |
| 33334 | tick 2. s1 ready (s3가 running 중이라 기다림) |
| 34500 | s1 run 34500–35500. s2 run 35500–37500. s3 run 37500–39000 |

simulator의 `deadline` line (s1의 것, s1이 다음 TIMER에 도달한 시각 기준):

```
deadline, t=1000,  task=s1, due=16667, met=true
deadline, t=31000, task=s1, due=33334, met=true    ← head는 자기 몫을 마감 안에 끝냄
deadline, t=35500, task=s1, due=50001, met=true
```

### 12.2 records — `job`

frame k = tail(s3)의 k번째 iteration 끝 − tick k.

| k | tick | s3 k번째 끝 | value | 16667 대비 |
|---|---|---|---|---|
| 0 | 0 | 4500 | 4500 | met |
| 1 | 16667 | 34500 | 17833 | **miss** |
| 2 | 33334 | 39000 | 5666 | met |

```
s1, job, 0,     4500,  period_us=16667
s1, job, 16667, 17833, period_us=16667
s1, job, 33334, 5666,  period_us=16667
```

entity는 chain의 head인 s1이에요. "이 chain의 frame"이라는 뜻으로.

**`deadline` line과 비교:** head의 line은 frame 1을 met이라고 해요(31000 < 33334). 하지만 화면에 frame이 나온 건 34500이고 이건 33334를 넘었어요. 16단 chain에서는 이 차이가 훨씬 커요. head는 1 ms 미만이고 나머지 15단이 십수 ms니까. 그래서 harness가 재구성하고, `deadline`은 단일 TIMER task에서만 cross-check로 써요.

**guard:** tail의 iteration 수(3) = head의 tick 수(3). 맞아요. wake가 큐에 쌓이지 않고 사라지는 simulator면 어느 stage에서 frame 하나가 빠지고 이 guard가 깨져요.

**`ready_wait`도 같이 나와요.** chain stage의 `WAIT`가 완료되는 것도 `cause=wake`예요. trace는 channel을 안 적으니 keystroke와 구분이 안 돼요. scoring이 entity(어느 task인지)로 구분해요. 게임 파일에는 keystroke를 받는 task가 없으니 실제로 섞이지는 않아요.

---

## 13. harness가 simulator에 기대는 가정

mock trace는 어떤 simulator 동작을 전제하고 쓰여요. 그 전제가 metrics doc 한 곳에 목록으로 있어야, 인경민이 다르게 결정했을 때 mock을 "우연히 틀린 것"이 아니라 "의도적으로 바꾸는 것"으로 다룰 수 있어요. 인경민에게 보낸 memo(`docs/memos/2026-09-07-trace-clarifications-for-the-simulator.md`)의 내용이에요.

| # | 가정 | 없으면 |
|---|---|---|
| 1 | blocking primitive가 완료될 때마다 `ready` line. 즉시 완료면 wait 0 | 큐에 쌓인 keystroke가 사라짐. backlog 상태의 frame 경계가 안 보임 (11장) |
| 2 | wake는 깊이를 갖고 큐에 쌓임. stage 6이 stage 7을 두 번 깨우면 stage 7은 나중에 `WAIT` 두 개를 완료 | chain 중간에서 frame이 빠지고 그 뒤 모든 tick/iteration 짝이 어긋남 (12장) |
| 3 | 같은 µs에 일어난 event의 순서가 문서화된 deterministic 규칙을 따름 | mock과 실제 trace를 byte 비교할 수 없음 |
| 4 | `deadline` line은 contract대로 계속 emit | cross-check를 잃음 |

그리고 조언 하나: `T_end` 뒤는 harness가 안 읽으니 거기서 멈춰도 돼요. 이건 contract가 아니에요.

이 중 1–3이 다르게 결정되면 mock을 고쳐요. 그래서 5.1(mock)을 5.3(reader)보다 먼저 하고, 인경민의 답을 mock이 확정되기 전에 받는 게 좋아요.

---

## 14. records 위에 올라가는 것 — aggregate, normalisation, score

여기서부터는 Phase 5의 범위 밖(Phase 6, 7)이지만, records를 왜 이렇게 만드는지 이해하려면 그 위를 알아야 해요. 정의는 metrics doc에 들어가고 code는 나중이에요.

### 14.1 aggregate — row들을 숫자 하나로

primitive마다 고정된 aggregate 목록이 있어요.

**`ready_wait`**: count, mean, P50, P95, P99, max, `over_threshold`.

`over_threshold`는 "interaction-latency 임계값을 넘은 row의 비율"이에요. 임계값은 상수 하나(관례상 100 ms 근처)이고, 1차 출처에서 확인하거나 stated assumption으로 적어요. "P95가 47 ms였다"보다 "keystroke의 8%가 임계값을 넘었다"가 파일 간 비교가 쉽고 사람에게 전달이 잘 돼요. 하지만 percentile도 같이 봐요. 비율은 "아슬아슬하게 맞춤"과 "여유 있게 맞춤"을 구분 못 하니까.

**`job`**: count, miss rate (`value > period_us`인 비율), latency P50, P99.

miss rate와 P99를 둘 다 보는 이유: miss rate 0%인데 P99가 마감 직전이면 "조금만 더 부하가 걸리면 무너지는 시스템"이에요. miss rate가 그걸 못 봐요.

**lifetime, bookkeeping row**: progress fraction (`cpu_delivered / demand`), provenance별 시간 비율, utilisation, config age.

**mean은 headline이 아니에요.** interactive work에서는 tail이 경험이에요. 평균이 좋고 P99가 나쁘면 사람은 "가끔 버벅인다"고 느껴요.

### 14.2 normalisation — 단위를 없애기

condition들을 비교하려면 "얼마나 좋아졌나"를 단위 없이 말해야 해요. 규칙:

```
normalised = (fixed − condition) / (fixed − oracle)
```

- `fixed`: recognition 없이 boot 설정만. 바닥.
- `oracle`: 정답 label을 driver table에 넣은 것. perfect recognition. 천장.
- `condition`: 지금 보는 것.

값 1이면 oracle만큼 좋고, 0이면 fixed와 같고, 음수면 fixed보다 나빠요. 음수는 그대로 보여요. 잘라내지 않아요.

숫자 예시. `c2-p1a`에서 editor의 `ready_wait` P95가 fixed 40 ms, oracle 8 ms, llm_vocab 12 ms라면:

```
(40 − 12) / (40 − 8) = 28 / 32 = 0.875
```

"headroom의 87.5%를 가져갔다."

**aggregate마다 따로** normalise해요. weight를 곱해서 합친 뒤에 하는 게 아니라, 각 aggregate를 먼저 unit-free로 만든 다음에 weight를 곱해요. ms와 비율과 초를 weight로 섞으려면 이 순서여야 해요.

### 14.3 floor — 분모가 0에 가까울 때

`fixed − oracle`이 아주 작으면 ratio가 폭발해요. 그래서 aggregate마다 **절대 floor**가 그 aggregate의 단위로 정해져요. 예를 들어 `ready_wait` P95의 floor가 5 ms라면, fixed와 oracle의 P95 차이가 5 ms 미만인 파일에서는 그 aggregate의 normalised 값을 "undefined, no headroom"으로 보고하고 raw 값만 적어요.

floor를 절대값으로 두는 이유: 독자가 숫자를 보고 직접 확인할 수 있어요. latency floor는 지각 임계값(14.1의 상수)에 자연스럽게 anchor돼요.

### 14.4 score — weight를 곱하기

normalised aggregate에 파일별 weight를 곱해 합친 게 score예요. weight는 연구 판단이라 code가 아니라 committed data file(scoring spec)에 있어요. Phase 6.

```yaml
c2-p1a:
  editor.ready_wait.p95:      {weight: 1.0, direction: lower}
  hog.progress:               {weight: 0.4, direction: higher}
c2-p1b:
  editor.ready_wait.p95:      {weight: 1.0, direction: lower}
  # hog.progress 없음 — 아무도 원하지 않은 indexing의 진행은 가치가 0
```

이 예시가 records 설계의 이유를 보여줘요. `c2-p1a`와 `c2-p1b`는 **behaviour가 완전히 같아요.** trace도 같고 records도 같아요. 차이는 오직 이 weight뿐이에요. training run(wanted)의 progress는 점수에 들어가고, indexer(unwanted)의 progress는 0점이에요.

---

## 15. 어떤 score가 좋을까 — 파일별로

Phase 6의 일이지만 미리 생각해두면 Phase 5에서 "이 row가 왜 필요한지"가 보여요. 아래는 준비 노트와 spec 세션의 논의를 정리한 것이고, 확정은 아니에요.

### 15.1 어느 파일이 판정에 들어가나

RQ0 gate("perfect recognition이 random보다 나은 headroom이 있나")의 judging set은 **C2의 6개 파일**이에요. 이유: 짝(pair)이 있어서 attribute(`background_wanted`)의 차이만 남기고 나머지를 통제할 수 있어요.

| 그룹 | 역할 |
|---|---|
| C2 (6) | judging set |
| C1 (6) | 보고만. whitelist가 만점을 받아야 하는 baseline. 단 `c1-gaming`은 demand가 가장 높은 파일이라 별도 보고 line |
| C3 (3), C4 (3) | 보고만. C4는 clean한 C1 원본과의 차이(delta)로 |
| C5 (3) | Layer 2 제외. `c1-media`와 behaviour가 같으니 성능 숫자도 같아야 함. 다르면 bug 신호 |
| C6 (3) | Layer 2 제외. 미리 약속된 miss |
| `c1-idle` | 성능 metric 없음. contention이 없음 |

### 15.2 파일별 primary metric 후보

| 파일 | 사용자의 주의 | 후보 |
|---|---|---|
| `c1-office` | `soffice.bin` | writer의 `ready_wait(wake)` P95/P99, over_threshold |
| `c1-browsing` | `chrome` | browser의 `ready_wait(wake)` |
| `c1-compile` | `code` | **양면**: editor latency + `make`의 turnaround (makespan) |
| `c1-gaming` | 없음 (게임 자체) | chain의 `job` miss rate + P99 |
| `c1-media` | 없음 | `mpv`(60 Hz)와 `spotify`(20 Hz)의 `job` miss rate |
| `c2-p1a/b` | `code` | editor latency + `hog`의 progress (p1a만) |
| `c2-p2a/b` | 없음 | chain `job` + `download`의 progress (p2a만) |
| `c2-p3a/b` | `kdenlive` | editor latency + `bulk`의 progress (둘 다 wanted지만 성격이 다름) |

### 15.3 판단이 필요한 세 곳

**C2는 파일별로 채점할 수 없어요.** 위에서 봤듯 pair의 두 파일은 raw 숫자가 같아요. 차이는 weight vector에만 있어요. 그래서 scoring spec은 "공유 primitive 위의 weight vector"여야 하고, pair마다 달라야 해요.

**`c1-compile`의 trade-off.** editor latency와 build makespan은 서로 당겨요. `batch_bandwidth_cap`이 정확히 그 교환비를 정하는 손잡이예요. 교환비 없이는 cap 값에 근거가 없어요. 제안된 형태: scalar 합이 아니라 "makespan이 cap 없을 때보다 X% 이상 나빠지지 않는 조건에서 editor latency 최소화"라는 constrained objective.

**`c1-media`의 audio/video weighting.** 오디오 끊김은 frame 하나 빠지는 것보다 훨씬 잘 느껴져요. 같은 weight를 주면 scheduler를 잘못된 방향으로 밀어요. 문헌 근거를 찾거나 stated assumption으로 적어요.

### 15.4 사람에게 전달되는 숫자

논문에 실릴 headline 후보:

- "keystroke의 X%가 100 ms 임계값을 넘었다" (over_threshold)
- "frame의 X%가 마감을 놓쳤다" (miss rate)
- "training run이 window 안에 X% 진행됐다" (progress)
- "fixed→oracle headroom의 X%를 llm_vocab이 가져갔다" (normalised)

전부 records의 row에서 한두 단계로 나와요.

---

## 16. guard — score와 별개로 항상 확인하는 것

score가 아니라 pass/fail이에요. 모든 보고 숫자 옆에 붙어요.

| guard | records에서 | 왜 |
|---|---|---|
| provenance 비율 | `config_interval` row의 provenance별 합 | fallback/held로 대부분 돌았으면 recognition이 증명한 게 없음 |
| config age | `config_interval`의 `t` − 그 query의 `t_set_change` | 얼마나 오래된 관측으로 설정했나 |
| starvation floor | task별 `ready_wait` max | 어떤 condition도 task를 굶기면 안 됨 |
| determinism | trace 파일의 hash 비교 (records 밖) | 같은 입력 두 번 → byte-identical |
| utilisation sanity | `busy ≤ T_end` | 물리적으로 말이 되나 |
| tick/iteration 일치 | `ready(timer_tick)` 개수 = tick 개수, tail iteration = head tick | simulator가 frame을 빠뜨리지 않았나 |
| `validation` = `provenance` | recognizer row의 `validation` 순서 = `config_interval`의 provenance 순서(boot 제외) | log와 schedule이 서로 맞나 |

`c6-dual` 같은 파일은 guard 예외를 미리 gate spec에 데이터로 적어요(`ground_truth`가 `ambiguous`라 oracle이 legal한 답을 낼 수 없어서 fallback 100%가 정상).

---

## 17. Phase 5의 sub-task와 이 문서의 대응, harness tree

| sub-task | 하는 일 | 이 문서의 어디 |
|---|---|---|
| **5.1** mock traces | 10–12장 같은 걸 넷 만들기. reduced run file + 20–40줄 trace + expected CSV | 10, 11, 12장 |
| **5.2** metrics doc | 7, 8, 13, 14장의 내용을 normative하게. 상수의 출처. `data-contracts` 수정(`deadline` 예시를 head로, 두 deferred 정의를 이 문서로 pointing). docs index. terminology | 7, 8, 9, 13, 14장 |
| **5.3** trace reader | 3, 4장을 code로. gzip stream, closed set 검증, `x_` 무시, `meta`, run file의 셋 | 3, 4장 |
| **5.4** primitives + writer | 7장을 pure function으로. CSV writer + machine schema. CI. expected CSV와 byte 일치 | 6, 7, 10장 |

순서: 5.1 → (5.2 ∥ 5.3) → 5.4. mock이 먼저인 이유는 doc과 reader가 expected value를 보고 병렬로 갈 수 있어서예요.

**harness tree**는 daemon tree를 그대로 따라요.

```
harness/
  README.md
  Makefile                 # make lint / make test
  records/
    schema/records.schema.json   # CSV column의 machine schema
  tools/
    requirements.txt       # pinned. pandas 없음
    harness/
      reader.py            # trace + run file → yields
      primitives.py        # pure functions
      records.py           # CSV writer
    tests/
      fixtures/
        mock-c1-office/    # run file + trace + expected.csv
        mock-c1-media/
        mock-c2-p1a/
        mock-chain/
      test_reader.py
      test_primitives.py
.github/workflows/harness.yml
```

파일 이름은 예시예요. 원칙은 machine이 읽는 것(schema, fixture)은 code 옆에, 사람이 읽는 것(metrics doc)은 `docs/harness/`에.

---

## 18. 용어 정리

| term | 뜻 |
|---|---|
| **lane** | CPU. 이 프로젝트에서는 하나 |
| **task** | 프로그램 하나. run file의 `arrive` event 하나 |
| **runnable / ready** | 일하고 싶은데 lane이 비길 기다리는 상태 |
| **blocked** | 일할 게 없어 기다리는 상태 (`WAIT`, `SLEEP`, `TIMER`, fork slot) |
| **occupancy interval** | `run_start`부터 `run_end`까지. task가 lane을 잡고 있던 구간 |
| **preempt** | scheduler가 running task를 강제로 내리는 것 |
| **tick** | `TIMER`의 주기적 알람. t₀ + k·period |
| **job** | tick 하나에 대응하는 주기 작업 하나 (frame 하나) |
| **backlog** | 지나간 tick들. 즉시 완료되어 밀린 job들이 연달아 실행됨 |
| **chain** | TIMER를 가진 head에서 WAKE를 따라 이어지는 task들. 게임의 frame pipeline |
| **head / tail** | chain의 첫 task(TIMER 있음) / 마지막 task |
| **exogenous / endogenous** | scheduler가 바꿀 수 없는 시각(keystroke, 등장, depart) / scheduler에 달린 시각(spawn, exit, 모든 실행 시각) |
| **`T_end`** | observation window의 끝. run file의 마지막 segment의 `t_end` |
| **primitive** | trace(또는 recognition log)에서 나오는 raw observation. records의 row |
| **aggregate** | primitive row들을 합친 통계 (P95, miss rate, …). records에 저장하지 않음 |
| **scoring** | aggregate에 파일별 weight를 곱하고 normalise해서 score를 만드는 것. Phase 6/7 |
| **records** | trace 하나당 CSV 하나. long format |
| **entity** | row가 누구 얘기인지. task id, 또는 예약 이름 `lane`/`schedule`/`recognizer` |
| **long format** | 한 row = 측정 한 번. metric 이름이 cell 값으로 들어감 |
| **provenance** | 적용된 config가 어디서 왔나: `unmodified`/`clamped`/`held`/`fallback` |
| **query point** | process 이름 집합이 바뀐 순간. recognizer가 호출되는 시점 |
| **`t_set_change`** | query point의 시각 |
| **Layer 1 / Layer 2** | recognition accuracy / consumer performance |
| **normalisation** | `(fixed − condition)/(fixed − oracle)`. headroom의 몇 %를 가져갔나 |
| **floor** | normalisation의 분모가 이보다 작으면 "no headroom" |
| **guard** | score와 별개의 pass/fail 검사 |
| **mock** | 손으로 쓴 run file + trace + expected records. 정의를 시험하고 code를 test함 |
| **condition** | 어떤 recognizer로 돌렸나: `fixed`, `random`, `whitelist`, `llm_vocab`, `llm_algo`, `llm_full`, `oracle` |
| **driver table** | `(mode, background_wanted)` → scheduler config의 lookup. prior와 calibrated 두 벌 |

---

## 이 문서를 다 읽었으면

- `_dev/docs/spec/jioh/phase-5-primitive-metrics-and-records.md`의 locked decision 17개가 전부 읽혀야 해요. 안 읽히는 항목이 있으면 이 문서의 구멍이에요.
- `_dev/archive/2026-09-07-phase-5-primitive-metrics.md`에 각 결정의 이유와 기각된 대안이 있어요.
- dataset 쪽은 `docs/workload/coreset-guide.md`.
- trace format의 규범적 정의는 `docs/data-contracts.md`의 trace 절.
