# Harness와 records 이해하기 — trace에서 논문의 숫자까지

> Status: draft · Created 2026-09-08 · Updated 2026-10-30

이 문서는 **공부용 문서**예요. Phase 5(primitive metrics and the records pipeline)를 직접 수행하기 위해, harness가 무엇을 읽고 무엇을 쓰는지, `records`의 row 하나가 무슨 뜻인지, 그리고 그 위에 어떤 score가 올라가는지를 OS/시스템 지식이 거의 없는 사람 기준으로 바닥부터 풀어 쓴 거예요. 규범적(normative)인 정의는 `docs/harness/metrics.md`(metrics doc)가 갖고, 이 문서는 그 문서를 읽을 수 있게 만드는 다리예요. 둘이 다르면 metrics doc이 맞아요.

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
11. 두 번째 mock — 늦은 frame과 건너뛴 tick
12. 세 번째 mock — 3단 chain과 늦은 frame 하나
13. harness가 simulator에 기대는 가정
14. records 위에 올라가는 것 — aggregate, normalisation, score
15. 어떤 score가 좋을까 — 파일별로
16. guard — score와 별개로 항상 확인하는 것
17. Layer 1 — recognition log를 채점하는 grader
18. mock daemon과 mock simulator — invocation contract의 첫 구현
19. per-experiment spec과 RQ0 gate evaluator — 판정을 데이터로
20. runner와 execution cache — 13 668 run을 돌리는 법
21. harness tree — 지금 모습
22. 용어 정리

---

## 1. 큰 그림 — harness는 pipeline의 어디에 있나

이 프로젝트의 실험은 파일을 주고받는 pipeline 하나예요. 세 프로그램이 서로 직접 대화하지 않고, 파일만 넘겨요.

```
 workload dataset                daemon                      simulator                 harness
 (run file, 51개)     ──▶   recognizer + validator   ──▶   scheduler 실행   ──▶   trace 읽기
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

- **recognizer**는 process 이름(과 개수, 그리고 window focus를 가진 process의 이름)만 봐요. `code`, `python`, focus는 `code`. 이름을 보고 "개발 중이고 training run이 돌고 있다"를 맞히는 게 그 일이에요.
- **simulator**는 각 process가 어떻게 행동하는지(program)만 봐요. 이름은 몰라요. 그냥 "이 task는 3 ms 일하고 keystroke를 기다린다"만 알아요.
- **harness**는 정답(`ground_truth`)을 봐요. 이 시간 구간의 진짜 mode가 무엇이었는지. 그리고 simulator가 남긴 trace를 읽어서 숫자를 뽑아요.

이 정보 비대칭이 실험의 핵심이에요. recognizer가 정답을 볼 수 없고, simulator가 이름을 볼 수 없어야 "이름에서 의미를 읽어내는 게 scheduling에 도움이 되나"를 깨끗하게 물을 수 있어요.

harness는 이 그림의 맨 오른쪽이에요. 두 가지를 해요.

1. **recognition을 채점**해요. recognition log의 답을 `ground_truth`와 비교. simulator와 무관해요. 이걸 프로젝트에서는 Layer 1(recognition accuracy)이라고 불러요.
2. **성능을 측정**해요. trace에서 "editor가 keystroke마다 얼마나 기다렸나", "frame이 몇 개 늦었나" 같은 숫자를 뽑아요. Layer 2(consumer performance)예요.

그리고 이 두 가지의 결과를 같은 모양의 파일, `records`에 써요. `records` 위에서 aggregate를 내고 weight를 곱해 score를 만들고, guard를 확인하고, RQ0 gate를 판정하는 건 그 다음 단계예요.

Phase 5는 이 중 **trace를 읽어 records를 쓰는 부분**과, **records에 들어갈 모든 숫자의 정의**를 담당해요. score의 weight(scoring spec)는 Phase 6에서, aggregate·score·guard·gate의 code는 Phase 8에서 만들었어요.

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

이 숫자들은 읽기 쉽게 고른 예예요. 실제 compiled 파일의 program은 측정값을 펼친 긴 목록이에요. `c1-media`의 video는 `TIMER(33348)` 뒤에 frame마다 길이가 다른 `RUN`이 이어지고, 측정된 editor는 keystroke(`input:` channel) 말고 자기 timer component의 wake(`timer:` channel)도 기다리고, `c2-p1a`의 training run은 측정된 run(`RUN`)과 그 뒤의 block(`SLEEP`)을 번갈아 하다가 `EXIT`해요.

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
{"event":"task_arrive", "t":2000105, "task":"build.j1.sh", "source":"spawn", "parent":"build"}
{"event":"task_end",    "t":2158000, "task":"build.j1.sh", "reason":"exit"}
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
{"event":"deadline", "t":15625, "task":"video", "due":16667, "met":true, "slack_us":1042}
```

`TIMER`를 가진 task의 job 하나(frame 하나)가 끝났을 때. `due`는 마감, `met`은 맞췄나, `slack_us`는 여유. TIMER skip 규칙으로 건너뛴 tick에도 `met: false`인 line이 하나씩 나와요(11장). harness는 이 line을 **cross-check용**으로만 써요. 자기 계산(7장의 `job`)과 비교해서 다르면 어느 한쪽의 bug예요. 왜 직접 쓰지 않는지는 7장에서.

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

trace는 **일어난 일**만 적어요. **일어났어야 하는 일**은 안 적어요. 그래서 harness는 run file을 두 번째 input으로 받아요. run file은 simulator가 읽는 것과 같은 view예요 — `workload_id`와 `events`(task마다 `arrive` event와 그 program, 그리고 `wake` event). 정답(`ground_truth`)은 run file에 없어요. 여기서 네 가지를 읽어요.

### 4.1 `T_end` — 언제까지를 볼 것인가

run file에서 가장 늦은 pinned 시각 — task의 등장, 정해진 퇴장(depart), wake event 중 최대 — 이 workload의 끝이에요. harness는 이걸 `T_end`라 부르고 `[0, T_end]`만 봐요. core set의 51개 파일에서는 이 값이 정답의 마지막 segment 끝과 같아요. 예를 들어 compiled `c2-p1a`의 정답은 이래요.

```jsonc
"ground_truth": [
  { "t_start": 0,        "t_end": 60000000, "mode": "dev",      "attributes": { "background_wanted": true } },
  { "t_start": 60000000, "t_end": 99435000, "mode": "ml-train", "attributes": { "background_wanted": true } }
]
```

run file 쪽에서는 editor(`code`)의 depart가 99435000이라 `T_end`도 99435000이에요. 자세한 규칙은 9장.

### 4.2 chain topology — 누가 누구를 깨우나

게임 파일에서 frame 하나는 task 17개를 릴레이로 지나가요 — head `game.chain.1`, `game.wineserver`, 그리고 `game.chain.2`부터 `game.chain.16`까지. run file의 `events`에 각 task의 program이 있으니 거기서 "TIMER를 가진 task에서 시작해 WAKE target을 따라가면 어디서 끝나나"를 읽을 수 있어요. 이게 chain topology이고, frame latency를 계산하려면 꼭 필요해요. 7장의 `job`에서 설명.

### 4.3 demand — 원래 얼마나 일해야 했나

`c2-p1a`의 training run(task `hog`, 이름 `python`)의 program은 측정된 run(`RUN`)과 그 뒤의 block(`SLEEP`)을 번갈아 적은 목록이고 `EXIT`로 끝나요. `RUN`을 다 더하면 1,389,885,000 µs, 약 1,390초예요. 이 task는 60초에 오고 파일은 99.435초에 끝나니, trace가 말해주는 건 window 안에서 받은 CPU(많아야 39.435초)까지예요. "필요한 것 중 얼마"라는 비율을 내려면 분모가 필요하고, 그건 run file에서 각 task의 `RUN` 총합으로 읽어요. program에 끝없는 `LOOP`이 있는 task(게임 chain의 stage들처럼)는 총합이 없으니 demand도 없어요. 측정된 player는 cycle을 하나씩 펼친 유한한 목록이라 총합이 있어요.

### 4.4 channel — 깨운 게 keystroke였나

측정된 program은 keystroke만 기다리지 않아요. `WAIT`마다 channel이 있고(`input:editor`, `timer:editor`, `chain:game.chain.2`, `job:build.j1.gcc`, `children:build`), harness는 각 task의 `WAIT`를 program 순서대로 읽어 그 channel의 **종류**(colon 앞의 이름: `input`, `timer`, `chain`, `job`, `children`)를 알아둬요. trace의 `ready(cause=wake)` line은 어느 channel이었는지 안 적으니, 그 line이 완료한 `WAIT`의 channel 종류를 run file에서 읽어 row의 `channel` column에 실어요(6.2). keystroke는 `input`이고, 측정된 timer wake, chain stage의 hand-off, compile job member끼리의 hand-off, orchestrator가 자식을 기다리는 것은 각각 `timer`, `chain`, `job`, `children`이에요. 또 task마다 `input` channel의 wake event 수(keystroke 수)를 세어 trace의 keystroke row 수와 맞춰봐요(guard 입력).

네 가지 다 "scheduler가 바꿀 수 없는 것"이에요. `T_end`는 사용자가 정한 시간, chain topology와 channel은 프로그램의 구조, demand는 일의 양. scheduler가 바꾸는 건 "언제"뿐이고, "언제"는 trace가 갖고 있어요.

### 4.5 세 번째 input — config schedule (Phase 6에서 추가)

trace의 `config_applied` line은 `index`, `algorithm`, `provenance`만 실어요. **params**(MLFQ면 `num_queues`, `timeslice_us`, …)는 안 실어요. 그래서 "algorithm이 MLFQ로 바뀐 뒤 scheduler가 다시 배우는 데 얼마나 걸리나"(7.10의 `switch_window`)를 재려면 그 params가 필요하고, 그건 daemon이 simulator에 넘긴 **config schedule** 파일(data-contracts 문서의 config schedule 절)에서 `index`로 찾아 읽어요. reader의 세 번째 input이에요. 없어도 다른 primitive는 전부 계산되고, MLFQ로의 switch가 있을 때만 "schedule이 없어서 이 row는 못 만들었다"는 guard가 나와요.

schedule의 `t_us`는 daemon이 답을 찍은 시각(t_return)이고, trace의 `config_applied`의 `t`는 실제로 적용된 시각(t_apply)이에요. schedule row의 `t`는 항상 후자예요.

---

## 5. Phase 5의 함수 한 줄 — `(run file, trace) → records`

Phase 5가 만드는 것을 함수 하나로 쓰면 이거예요.

```
primitives(run_file, trace) → records.csv
```

- 실행 파일을 호출하지 않아요. 파일 둘(Phase 6부터는 config schedule까지 셋, 4.5)을 읽어서 파일 하나를 써요.
- simulator도 daemon도 필요 없어요. 손으로 쓴 mock trace로 test할 수 있어요.
- trace 하나당 records 파일 하나예요. core set의 51개 파일 × N condition이면 그만큼의 CSV.
- 이 함수는 "이 파일에서 editor가 interactive task다" 같은 걸 **몰라요.** `ready` line이 있으면 row 하나를 내요. 어느 row가 중요한지는 다음 단계(scoring)가 정해요.

recognition 쪽은 같은 모양의 row를 내지만 input이 달라요.

```
grader(recognition_log, ground_truth, calibrated_table) → records rows (entity=recognizer)
```

이 함수의 **정의**는 Phase 5의 metrics doc에 들어가고, **code**는 Phase 8에서 만들었어요(`harness/tools/harness/grader.py`).

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

### 6.2 column 25개

세 묶음이에요. column의 순서와 뜻은 `harness/tools/harness/records.py`의 `COLUMNS`와 `harness/records/schema/records.schema.json`이 정해요.

**identity 8개** — 이 row가 어느 실험의 어느 trace에서 왔나.

| column | 뜻 | 예 |
|---|---|---|
| `workload_id` | 어느 workload | `c2-p1a` |
| `condition` | 어느 recognizer | `llm_vocab` |
| `table` | 어느 driver table. `prior` 또는 `calibrated`. `fixed`는 table을 안 쓰니 빈칸 | `prior` |
| `seed` | `random` condition의 PRNG seed. 나머지는 빈칸 | `7` |
| `boot_default` | 그 run이 시작한 boot 설정의 id. primary면 빈칸. RQ0 gate spec의 sensitivity check에서 alternative로 돈 `fixed` run만 채워요(8.2에 추가) | `ostep-slice-2000us` |
| `telemetry` | 그 run의 daemon이 recognizer에게 보여준 telemetry 모양: `focus`(이름 → 개수 multiset에 focus를 가진 process 이름까지) 또는 `names`(multiset만)(9.17에 추가) | `focus` |
| `sim` | simulator 버전. recognition row에는 없어요(trace가 아니라 log에서 나오니까) | `simulator@abc123` |
| `source_sha256` | 이 row가 나온 trace(또는 recognition log)의 hash | `9f3a…` |

**observation 4개** — 측정 한 번.

| column | 뜻 |
|---|---|
| `entity` | **누구에 대한** 측정인가 |
| `metric` | **무엇을** 쟀나 |
| `t` | **언제**의 일인가 (anchor time, µs) |
| `value` | **얼마**였나 |

**attribute 13개** — metric에 따라 채워지는 부가 정보. 해당 없으면 빈칸.

| column | 어느 metric이 채우나 | 뜻 |
|---|---|---|
| `cause` | `ready_wait` | 왜 runnable해졌나 (`arrive`, `wake`, `sleep_end`, `timer_tick`, `fork_slot`) |
| `channel` | `ready_wait` 중 `cause = wake`인 row | 그 wake가 완료한 `WAIT`의 channel 종류: `input`, `timer`, `chain`, `job`, `children` (4.4; 9.5에 추가) |
| `provenance` | `config_interval` | 설정이 어디서 왔나 |
| `algorithm` | `config_interval`, `switch_window`, `boost_window` | 어떤 algorithm이었나 |
| `index` | `config_interval`, `switch_window`, `boost_window` | schedule의 몇 번째 entry였나 |
| `period_us` | `job` | 이 주기 작업의 period. `value > period_us`면 miss |
| `predicted` | `mode_correct`, `attr_correct`, `algo_choice_correct` | recognizer가 뭐라고 답했나 |
| `truth` | `mode_correct`, `attr_correct`, `algo_choice_correct` | 정답이 뭐였나 |
| `validation` | recognizer row | validator가 그 답을 어떻게 처리했나 |
| `familiarity` | recognizer row | 이 query를 덮는 segment의 familiarity tier (segment에 적혀 있을 때만). accuracy를 tier별로 나눠 볼 때 묶는 기준 |
| `hogs` | `switch_window`, `boost_window` | 그 순간에 센 hog(CPU만 먹는 task)의 수 H (7.10) |
| `pre_committed_miss` | recognizer row | 이 query를 덮는 segment에 `pre_committed_miss` 표시가 있으면 1, 없으면 0. headline accuracy는 1인 row를 빼고 계산해요(8장; 8.4에 추가) |
| `skipped` | `job` | 1이면 harness가 읽는 TIMER skip 규칙으로 건너뛴 tick의 row — 일이 하나도 없었으니 `value`는 빈칸이고 miss로 세요. 소비된 tick의 row는 0 (11장; 9.14에 추가) |

### 6.3 `entity`는 어디서 나온 말인가

리서치 문서에 처음 등장하는 말이 맞아요. Phase 5 spec 세션에서 records column을 정하면서 도입했어요. 뜻은 **"이 row가 누구 얘기인가"**예요.

`task`라고 안 한 이유는, task가 아닌 것에 대한 측정도 같은 표에 들어가야 해서예요.

| entity | 무엇 | 예시 metric |
|---|---|---|
| task id (`editor`, `video`, `build.j1.cc1`, `game.chain.1`, …) | task 하나. id이지 process 이름이 아니에요(`video`의 이름은 `mpv`) | `ready_wait`, `cpu_delivered`, `job` |
| `lane` | CPU 그 자체 | `busy` — CPU가 총 얼마나 바빴나 |
| `schedule` | config schedule | `config_interval` — 설정이 얼마나 유지됐나; `switch_window` — algorithm이 바뀐 뒤 다시 배우는 구간; `boost_window` — 그 뒤 MLFQ boost마다의 같은 구간 |
| `recognizer` | recognizer의 답 | `mode_correct` — 이 query에서 mode를 맞췄나 |

`lane`, `schedule`, `recognizer`는 **예약된 이름**이에요. run file에 이 이름의 task가 있으면 reader가 trace를 거부해요. "누구 얘기인지" 헷갈리면 안 되니까.

### 6.4 row 하나를 읽는 법

```
editor, ready_wait, 10000, 10000, cause=wake, channel=input
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

`c2-p1a`를 예로 들면, 관심 있는 구간은 60–99.435초예요(training run이 있는 동안). 처음 60초는 editor 혼자라서 latency가 당연히 좋고, 이걸 파일 전체 P99에 섞으면 숫자가 희석돼요. raw row에 `t`가 있으니 scoring 단계에서 `t >= 60000000`으로 filter하면 돼요(scoring spec의 window, 15.2). primitive는 `ground_truth`를 읽을 필요가 없어요.

---

## 7. primitive 하나하나 — 실제 예시로

이 장은 records에 들어가는 metric 각각을 "어떤 상황에서, trace의 어느 line에서, 어떤 row가 나오는가"로 설명해요. 예시는 ms 단위로 읽기 쉽게 쓰지만 실제 값은 µs예요.

등장인물 둘. 숫자는 설명을 위해 고른 가상의 파일(180초짜리)의 것이에요. 실제 파일과 다른 곳은 그때그때 적어요.
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
entity=editor, metric=ready_wait, t=250, value=10, cause=wake, channel=input
```

**규칙:** `ready` line 하나마다 row 하나. `t`는 `ready`의 시각, `value`는 그 task의 다음 `run_start`까지의 시간. `cause`를 row에 싣고, `cause=wake`면 그 wake가 완료한 `WAIT`의 channel 종류(4.4)도 실어요.

**특수 규칙:** `ready`가 그 task의 **자기 occupancy 안**에 떨어지면(즉 `run_start`와 `run_end` 사이에) `value = 0`. 이건 "block되지 않고 즉시 완료된 blocking primitive"의 경우예요. 11장에서 실제로 봐요.

**왜 하나의 generic primitive인가.** interaction latency(keystroke 대기), response time(등장 후 첫 실행까지), timer dispatch delay(tick 후 실행까지), starvation(가장 오래 기다린 시간)은 전부 이 row들의 filter와 aggregate예요.

| 이름 | records에서 |
|---|---|
| interaction latency | `cause=wake`이고 `channel=input`인 row들 (keystroke만; 4.4) |
| response time | `cause=arrive`인 row |
| timer dispatch delay | `cause=timer_tick`인 row들 |
| starvation | task별 `ready_wait`의 최대값 (어떤 cause든) |

starvation이 "`ready`부터"이지 "arrive부터"가 아닌 이유: 스스로 자고 있는 task는 굶는 게 아니에요. 깨어나서 줄 선 시간만 세요.

### 7.2 `job` — 주기 작업 하나가 걸린 시간

**"16.7 ms마다 frame 하나 그려야 하는 프로그램이, 각 frame을 tick 후 얼마 만에 끝냈나."**

동영상 player(task `video`, 이름 `mpv`)가 `LOOP { TIMER(16667) → RUN(6667) }`라고 해요. tick은 `t₀ + k·period`에 놓이고, `t₀`는 task가 처음 TIMER를 실행한 시각이에요 — 주기 task의 첫 명령은 TIMER이고 그건 등장하는 순간에 실행되니, `t₀`는 등장 시각이에요(metrics doc의 simulator 가정 4번). tick k에 시작한 일을 job k라고 불러요. job k는 **tick k가 소비될 때 시작**하고, **task가 다음 TIMER에 도달할 때 끝나요.** 마감은 다음 tick이에요.

```
t=0.0   ready      video  cause=timer_tick   ← tick 0
t=0.0   run_start  video
t=6.7   run_end    video  reason=block blocked_on=timer  ← frame 다 그리고 다음 tick 기다림
t=16.7  ready      video  cause=timer_tick   ← tick 1
t=16.7  run_start  video
t=23.4  run_end    video  reason=block blocked_on=timer
```

job 0: tick 0.0, 완료 6.7 → value 6.7. period 16.7보다 작으니 제때.

```
entity=video, metric=job, t=0,    value=6.7,  period_us=16.7, skipped=0
entity=video, metric=job, t=16.7, value=6.7,  period_us=16.7, skipped=0
```

늦는 경우:

```
t=33.4  ready      video  cause=timer_tick   ← tick 2. hog가 의자에 있음
t=45.0  run_start  video                     ← 11.6 ms 기다림
t=51.7  ready      video  cause=timer_tick   ← 다음 TIMER에 도달. tick 3(50.1)은 이미 지났으니 block 없이 바로 소비
```

job 2: tick 33.4, 완료 51.7 → value 18.3 > 16.7. **miss.** 화면이 한 frame 끊긴 것.

```
entity=video, metric=job, t=33.4, value=18.3, period_us=16.7, skipped=0
```

miss 여부는 저장 안 해요. `value > period_us`로 읽는 쪽이 계산.

**한 번 기다리는 동안 tick이 둘 이상 지나가면** 가장 최근에 지난 tick 하나만 바로 소비하고 그 앞의 소비 안 된 tick은 건너뛰어요. harness가 읽는 TIMER skip 규칙이에요(2026-10-07 memo, `docs/memos/2026-10-07-timer-skip-rule-for-the-simulator.md`). 건너뛴 tick도 row가 하나 나와요. 일을 하나도 안 했으니 `value`는 빈칸, `skipped=1`이고, miss로 세요. 11장에서 실제로 봐요.

**game chain은 왜 특별한가.** 게임 파일에서 frame은 task 17개를 릴레이로 지나가요.

```
game.chain.1     LOOP { TIMER(16667) → RUN → WAKE game.wineserver }
game.wineserver  LOOP { WAIT(chain:game.wineserver) → RUN → WAKE game.chain.2 }
game.chain.2     LOOP { WAIT(chain:game.chain.2) → RUN → WAKE game.chain.3 }
   …
game.chain.16    LOOP { WAIT(chain:game.chain.16) → RUN }
```

TIMER는 **첫 task에만** 있어요. 그래서 simulator가 내는 `deadline` line은 `game.chain.1`의 것이고, 그건 "첫 stage가 자기 몫(`c1-gaming`에서 631 µs)을 tick 안에 끝냈나"만 답해요. 거의 항상 yes예요. 정작 "frame이 화면에 나왔나"는 `game.chain.16`이 그 frame의 iteration을 끝낸 시각인데, trace에 "이게 frame k다"라고 적힌 line은 없어요.

그래서 harness가 **재구성**해요. run file에서 TIMER를 가진 task를 찾고, WAKE target을 따라가서 tail을 찾아요(`game.chain.1 → game.wineserver → game.chain.2 → … → game.chain.16`). head가 j번째로 소비한 tick의 frame은 tail의 j번째 iteration이에요 — 건너뛴 tick은 chain에 wake를 안 보내고, wake는 깊이를 갖고 쌓이니까요. frame latency = 그 iteration의 끝 − tick. 이 규칙은 구조적이에요. `.chain.` 같은 이름 규칙에 의존하지 않아요.

단일 TIMER task(`video`)는 길이 1짜리 chain이라 같은 규칙이 그대로 적용돼요. 그 결과가 simulator의 `deadline` line과 같아야 하니, `deadline`은 공짜 cross-check가 돼요.

**규칙:** tick 하나마다 row 하나(소비됐든 건너뛰었든). entity는 chain의 head(또는 단일 TIMER task). `t` = tick 시각, `value` = 완료 − tick(건너뛴 tick은 빈칸), `period_us`와 `skipped`를 row에. harness는 window 안에서 tail이 끝낸 iteration 수가 head가 소비한 tick 수를 넘지 않는지 guard해요. 모자란 건 guard가 아니에요: `T_end`에 아직 돌고 있는 iteration은 window 안에 끝나지 않은 것이에요(9장) — `c7-gaming`의 마지막으로 소비된 tick은 `T_end` 1,139 µs 전이고 frame 하나는 14,999 µs예요.

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

**"이 task의 program에 적힌 RUN의 총합."** run file에서 읽어요. trace에는 없어요. program에 끝없는 `LOOP`이 있는 task(게임 chain의 stage들처럼)는 총합이 없으니 row도 없어요.

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

실제 `c2-p1a`의 `hog`(training run, 이름 `python`)는 약 1,390초어치 일(demand 1,389,885,000 µs)을 60초에 시작하고 파일은 99.435초에 끝나요. 절대 못 끝나요. 그래서 `completed=0`이고 `turnaround` row는 아예 안 나와요. "늦게 끝났다"가 아니라 "window 안에 안 끝났다"예요. simulator가 그 뒤를 더 돌렸든 말든 안 봐요.

segment-bound task(사용자가 닫는 앱)는 `task_end`의 `reason`이 `depart`라서 항상 `completed=0`이에요. scoring은 이 row를 무시해요. finite task(batch, compile child)에서만 의미가 있어요.

### 7.6 `turnaround` — 등장부터 퇴장까지

**"나타나서 완전히 끝날 때까지 벽시계로 얼마나 걸렸나."** `completed=1`일 때만 row가 나와요.

```
t=2000   task_arrive  build.j1.as
  … 다른 task들과 의자를 나눠 씀 …
t=2158   task_end     build.j1.as  reason=exit
```

`turnaround = 2158 − 2000 = 158`. 실제 일한 시간 + 줄 선 시간(+ compile job의 member라면 같은 job의 다른 member가 깨워주길 기다린 시간).

```
entity=build.j1.as, metric=turnaround, t=2158, value=158
```

**`arrival`** — 등장 시각도 row 하나로 나와요(2026-10-17, 9.15에 추가). task마다 하나, `t`는 `T_end`, `value`는 그 task의 `task_arrive` 시각이에요.

```
entity=build.j1.as, metric=arrival, t=180000, value=2000
```

window 안에 못 끝난 task에는 `turnaround` row가 없으니, 그 task의 turnaround term은 censored bound `T_end − 등장`으로 채점돼요(15.3, metrics doc의 normalisation 절). aggregate는 그 등장 시각을 이 row에서 읽어요. `ready(cause=arrive)` row가 없는 task — 첫 명령이 `WAIT`인 task(10.3) — 에도 이 row는 있어요.

`c1-compile`의 makespan(빌드 전체 시간)은 `make`(task `build`)의 `turnaround`예요. `make`는 자식 17,448개를 만들어요 — object job 2,908개, job마다 `sh`, `gcc`, `cc1`, `as`, `fixdep`, `rm` 여섯 — 동시에 살아 있는 자식은 많아야 48개(`fork_cap`, `-j8`의 8 × 6)이고, 마지막 `FORK` 뒤에 자기 `children:build` channel에서 `WAIT`했다가 `EXIT`해요. 그 `WAIT`은 자식이 모두 끝났을 때 완료돼요 — interpretation contract에 제안된 규칙이고 RQ0 gate spec의 simulator-conformance 항목 (g)예요. reference simulator는 아직 이 `WAIT`을 깨우지 않아서, 그 전까지는 `make`가 `EXIT`에 못 가고 이 row가 안 나와요. 각 자식도 자기 row를 갖는데, 자식의 등장 시각은 trace의 `task_arrive(source=spawn)`에서 와요.

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

entity가 `lane`인 건 특정 task 얘기가 아니라 CPU 얘기라서. idle = `T_end − busy`. utilisation = `busy / T_end`. 이건 주로 sanity check예요. 파일이 의자를 얼마나 요구하는지는 어떤 범위에 맞춰 설계한 게 아니라 측정한 대로예요. job을 측정한 그대로 통째로 묶으니 파일의 demand가 측정에서 따라 나오고, 범위(예전의 의자 100–150%)에 맞추려면 측정된 길이를 구부려야 했어요. 그래서 demand는 맞추지 않고 dataset manifest가 파일별·segment별로 보고해요(`dataset/build.manifest.json`의 `demand`; 2026-10-09). 많은 파일이 의자 하나에 한참 못 미쳐요(core set 51개 중 31개가 1 미만, `c1-idle`은 0.0004). 그래서 `busy`가 낮다는 것만으로는 잘못된 게 아니고, 그 파일의 manifest demand와 비교해서 읽어요.

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

### 7.10 `switch_window` — algorithm이 바뀐 뒤 다시 배우는 구간 (Phase 6에서 추가)

**"algorithm이 다른 것으로 바뀐 순간부터, 새 scheduler가 '누가 batch인지'를 다시 알아내는 데 걸리는 구간의 길이."**

배경은 2026-09-08의 memo(`docs/memos/2026-09-08-algorithm-switch-semantics-for-the-simulator.md`)예요. algorithm이 바뀌면 이전 scheduler가 배운 상태는 버려져요. EDF의 deadline, LOTTERY의 ticket, FIFO의 도착 순서는 config나 program에서 다시 나오니 잃는 게 없지만, **MLFQ의 queue level**은 행동을 보고 배운 것이라 잃어요. MLFQ로 바뀌면 모든 task가 맨 위 queue에서 다시 시작하고, CPU만 먹는 task(hog)는 slice를 한 번씩 다 쓰면서 한 칸씩 내려가요. 그동안 editor 같은 interactive task는 응답이 나빠져요. 이건 MLFQ 자신의 주기적 boost가 만드는 상태와 같아서, "switch 한 번 = boost 한 번 더"라는 단위로 재요.

row는 `config_applied` 중 **직전 entry와 algorithm이 다른 것**마다 하나예요(boot entry는 직전이 없으니 row 없음; params만 바뀐 entry는 switch가 아님). entity `schedule`, `t`는 적용 시각.

- `W_single` = hog 하나가 맨 위 queue에서 맨 아래까지 떨어지는 데 **받아야 하는 CPU 시간**. 위쪽 level마다 slice 하나씩: `timeslice_us × (1 + growth + growth² + …)`, level이 `num_queues − 1`개. 예를 들어 3 queue, 2000 µs, growth 2면 2000 + 4000 = 6000 µs(boot default는 2026-09-11부터 OSTEP 예시의 10 ms slice라 10000 + 20000 = 30000 µs). **바뀐 뒤의 params**로 계산하고, 그래서 config schedule이 필요해요(4.5).
- `H` = 그 순간 살아 있는 task 중, 적용 시각 뒤 **첫 `run_end`가 `preempt`인** task의 수. 행동으로 세요(이름이나 archetype은 모름). `hogs` column에 실려요. FIFO 등으로 바뀔 때도 세어서 적지만 value는 0.
- `value` = MLFQ로 바뀔 때, 적용 시각부터 **마지막 hog가 CPU를 `W_single`만큼 받은 순간**까지의 길이. hog가 실제로 앉아 있던 구간(occupancy)을 적용 시각부터 더해서 6000이 차는 시각을 찾아요. 그 사이 editor가 의자를 쓰면 hog의 시계는 멈추고 창은 그만큼 길어져요. 다음 algorithm switch나 `T_end`까지도 못 채우면 거기서 자르고 guard를 내요. EDF/LOTTERY/FIFO로 바뀔 때는 0.

```
t=40600   config_applied  index=3  algorithm=MLFQ   (직전 entry는 FIFO)
          살아 있는 task: editor, hog, probe
          40600 뒤 첫 run_end: editor 44600 preempt / hog 42600 preempt / probe 45100 block → H = 2
          incoming params 3 / 2000 / 2 → W_single = 6000
          hog의 CPU:    [40600,42600] 2000, (editor·probe가 씀), [45100,49100] 4000 → 49100에 6000 참
          editor의 CPU: [42600,44600] 2000, (probe·hog가 씀),   [49100,53100] 4000 → 53100에 6000 참
```

editor도 hog로 세요. switch 순간에 살아 있었고, 그 뒤 첫 `run_end`가 44600의 preempt(Q0 slice를 다 쓰고 Q1으로 내려가는데 `probe`가 Q0에서 기다리고 있어서)니까요. 이름이나 역할이 아니라 행동으로 세는 규칙이라 이런 일이 생겨요. 창은 마지막 hog인 editor가 6000을 채운 53100에 닫혀요.

```
entity=schedule, metric=switch_window, t=40600, value=12500, algorithm=MLFQ, index=3, hogs=2
```

**`boost_window` (8.10에 추가).** MLFQ로 들어간 interval 안에서 boost가 일어날 때마다 같은 규칙으로 창을 하나씩 더 재요: 그 순간 H를 세고, 마지막 hog가 그 순간부터 `W_single`을 받으면 닫혀요. boost timer는 그 interval에서 MLFQ entry가 적용될 때마다 다시 시작해요 — switch의 `t_apply`에서, 그리고 그 뒤 params나 cap만 바뀐 같은 algorithm의 entry가 적용될 때마다요(13장 가정 5번; 같은 algorithm의 entry에서 다시 시작하는 건 2026-10-17, 9.15부터). 그래서 boost 시점은 가장 최근에 적용된 entry의 적용 시각 + k × 그 entry의 `boost_interval_us`(k ≥ 1)이고, 다음 entry가 적용되기 전까지예요. 창의 `W_single`도 그 entry의 params로 계산하고, row의 `index`는 그 boost 시점이 놓인 grid의 entry예요. 다음 boost나 interval의 끝에서는 guard 없이 잘라요(boost 창이 다음 boost까지 가는 건 정상이니까). row는 `switch_window`와 같은 column에 `metric`만 `boost_window`. `mock-switch`에서는 boost가 20000마다라 60600과 80600에 row가 하나씩이고, 60600의 창은 editor가 3000밖에 못 받은 채 다음 boost에서 잘려 20000, 80600의 창은 hog 하나가 끊김 없이 6000을 받아 6000이에요.

이 row들 위에서 나오는 숫자(metrics doc의 aggregate 절): switch window `[t, t + value]` 안에 있는 editor의 keystroke `ready_wait`(`cause=wake`, `channel=input`) 평균에서 같은 config interval의 어느 창에도 안 든 row의 평균을 뺀 **초과분**(switch 변형), 그리고 같은 계산을 boost window들로 한 것(boost 변형). 둘이 비슷하면 "switch는 boost 한 번 값이었다", 더 크면 이전 algorithm에서 넘어온 몫. 그리고 전체 시간 중 switch window 안에 든 비율. `mock-switch`에서는 switch 변형이 0 µs(창 안의 keystroke가 editor의 burst 중에 와서 대기 0으로 완료), boost 변형이 600 µs, 비율이 0.125예요. **score에 weight로 들어가지 않고 옆에 보고만 해요.**

fixture `mock-switch`(`harness/tools/tests/fixtures/mock-switch/worked.md`)가 이걸 처음부터 끝까지 손으로 계산한 예예요. memo의 처음 정의는 창을 `W_single × H`의 **벽시계** 길이로 그었어요. 이 fixture로는 [40600, 52600]이라, hog의 하강(49100)은 덮지만 editor의 하강(53100)은 못 덮어요. 창 안에서 다른 task가 의자를 쓰면 hog의 하강이 그만큼 늦어지기 때문이에요. 그래서 창을 위처럼 hog가 실제로 받은 CPU로 재도록 고쳤고(memo 7절), 지금은 창이 53100에 닫혀 둘 다 덮어요. 정의가 현실과 맞는지 감시하는 도구가 `harness/tools/check_mlfq_levels.py`예요: simulator가 `x_mlfq_level`(demotion/boost마다 한 줄)을 내면, harness는 `x_` 규칙대로 무시하지만 이 도구는 읽어서 "각 switch의 창이 hog들의 마지막 demotion을 덮었나"를 보고해요. 체계적으로 못 덮으면 그게 정의를 다시 고치거나 closed set에 field를 추가하자고 제안할 근거예요.

### 7.11 한 줄 요약표

| metric | 한국어로 | entity | 몇 row | trace의 어디서 | run file에서 |
|---|---|---|---|---|---|
| `ready_wait` | 줄 선 시간 | task | `ready`마다 | `ready` → 다음 `run_start` | — |
| `job` | 주기 작업 하나 걸린 시간 (건너뛴 tick은 값 없이 `skipped=1`) | chain head | tick마다 | `ready(timer_tick)` + run line + tail의 iteration | chain topology |
| `cpu_delivered` | 앉은 시간 합 | task | task당 1 | 모든 `run_start`~`run_end`, `T_end`에서 clip | `T_end` |
| `demand` | 원래 필요한 시간 | task | task당 1 | — | RUN 총합 |
| `completed` | 끝났나 | task | task당 1 | `task_end(exit)` 유무 | `T_end` |
| `turnaround` | 등장부터 퇴장까지 | task | completed일 때 1 | `task_arrive` → `task_end(exit)` | — |
| `arrival` | 등장 시각 | task | task당 1 | `task_arrive`의 시각 | `T_end` |
| `preempt_count` | 끌려온 횟수 | task | task당 1 | `run_end(preempt)` 개수 | — |
| `busy` | 의자가 찬 시간 합 | `lane` | trace당 1 | 모든 run interval | `T_end` |
| `config_interval` | 설정 유지 시간 | `schedule` | `config_applied`마다 | `config_applied` → 다음 것 | `T_end` |
| `switch_window` | algorithm 전환 뒤 재학습 구간 | `schedule` | algorithm이 바뀌는 `config_applied`마다 | `config_applied`, 각 task의 첫 `run_end`, hog의 occupancy | config schedule의 params (`index`로) |
| `boost_window` | switch로 들어간 MLFQ 안의 boost 뒤 재학습 구간 | `schedule` | 그 interval 안의 boost 시점마다 | 그 interval의 MLFQ entry가 적용될 때마다 다시 시작하는 boost grid, 각 task의 첫 `run_end`, hog의 occupancy | config schedule의 `boost_interval_us`와 params (`index`로) |

---

## 8. recognition primitives — recognizer의 답을 채점한 row

Layer 1은 simulator와 무관해요. recognition log를 `ground_truth`와 비교해요.

recognition log는 query point마다 entry 하나예요. query point는 "telemetry의 집합이 바뀐 순간"이고, 그 집합은 process 이름 → 개수의 multiset에 window focus를 가진 process의 이름까지 더한 것이에요(data-contracts 문서의 telemetry 절, 규칙 여섯 개; focus는 2026-10-11부터). 그래서 focus만 옮겨가도 query point예요. `c2-p1a`라면 0초(`code` 등장, focus를 잡음), 60초(`python` 등장), 99.435초(`code` 퇴장, focus 없음)의 셋.

```jsonc
{ "t_set_change": 60000000,
  "telemetry": { "t_us": 60000000, "processes": [ {"name":"code","count":1}, {"name":"python","count":1} ], "focus": "code" },
  "proposal":  { "system": { "mode": "ml-train", "background_wanted": true }, … },
  "validation": "unmodified",
  "latency_us": 450000 }
```

log의 맨 위에는 어느 telemetry 모양을 보여줬는지(`"telemetry": "focus"` 또는 `"names"`)가 적혀요. `names`면 snapshot에 `focus`가 없어요. query point는 두 모양에서 같아요.

이 entry 하나에서 나오는 row들. entity는 `recognizer`, `t`는 `t_set_change`.

```
recognizer, mode_correct,   60000000, 1, predicted=ml-train, truth=ml-train, validation=unmodified
recognizer, attr_correct,   60000000, 1, predicted=true,     truth=true,     validation=unmodified
recognizer, latency_us,     60000000, 450000,                                validation=unmodified
recognizer, config_correct, 60000000, 1,                                     validation=unmodified
```

`validation`은 **column**이지 metric이 아니에요 — 모든 recognition row에 붙어요(§6.2). 예전 판에는 `recognizer, validation, …` 이라는 row가 하나 더 적혀 있었는데, records schema의 `metric` 목록에 `validation`이 없고 `value`는 정수라서 그 row는 애초에 만들 수 없어요. 2026-09-11(8.4)에 고쳤어요.

`config_correct`(8.4에 추가)는 **틀린 답이 실제로 scheduler를 바꿨나**를 재요. 예측한 `(mode, background_wanted)` row에서 만들어지는 config(algorithm + params + cap)가 정답 row의 config와 byte 단위로 같으면 1이에요. 이름을 틀렸어도 두 row가 같은 config로 이어지면 scheduler는 똑같이 돌았다는 뜻이라, Layer 1의 accuracy와 Layer 2의 결과가 어긋날 때 그 이유를 여기서 읽어요. 쓰는 table은 **그 run이 실제로 쓴 table**(row의 `table` column)이에요.

`llm_algo` condition(LLM이 algorithm까지 고르는 조건)에서만 row 하나 더:

```
recognizer, algo_choice_correct, 60000000, 1, predicted=MLFQ, truth=MLFQ
```

`truth`는 calibrated driver table에서 정답 row의 default algorithm이에요. 그래서 grader는 table 파일도 input으로 받아요. 이 metric만은 **calibrated** table이어야 하고, prior table을 주면 grader가 거부해요(delegation rung을 엉뚱한 table로 채점하면 안 되니까).

**채점 범위:** `ambiguous`가 아닌 `ground_truth` segment가 `t_set_change`를 덮는 query만 채점해요. 마지막 snapshot(파일이 끝나는 순간의 것)은 덮는 segment가 없으니 건너뛰어요. `c6-dual`의 `ambiguous` segment도 채점 대상이 아니에요. 지금 core set에서 이 규칙을 적용하면 **51개 파일의 query point 147개 중 51개가 마지막 snapshot, 19개가 `ambiguous`**(`c6-dual`의 집합 변화 둘과 focus 이동 열일곱)라서 **77개가 채점 대상**이고(50개 파일), 그중 9개가 `pre_committed_miss` segment 위에 있어서 headline은 **68개(44개 파일)**예요.

`pre_committed_miss`가 붙은 segment는 이름과 행동만으로는 누구도 맞힐 수 없는 label이라, headline accuracy에서는 빼고 포함한 숫자를 두 번째 줄로 같이 보고해요. 어느 row가 빠졌는지는 records의 `pre_committed_miss` column(8.4에 추가)에 적혀 있어요.

이 row들의 aggregate는 `grades` 파일에 나와요. 어떤 축에 어떤 통계를 쓰는지는 **정해져 있어요**:

| 축 | headline | 왜 |
|---|---|---|
| attribute (`true`/`false`) | **balanced accuracy** + Matthews 계수, confusion matrix | 늘 `true`라고만 답해도 75.3%가 나와요(채점되는 77개 중 58개가 `true`; headline 68개 위에서는 79.4%). 그래서 raw accuracy는 majority baseline을 옆에 적을 때만 써요 |
| mode (16개) | raw accuracy + **측정한** majority baseline, confusion matrix, class별 recall | core set이 32개 cell을 전부 덮어서 늘 같은 답만 하면 14.3%밖에 안 나와요(77개 중 11개가 `gaming`; headline 위에서는 16.2%) — 보정할 병이 없어요. macro 평균은 어느 축에서도 안 내요 |
| algorithm choice (4개) | mode와 동일 | |
| configuration | `config_correct` 비율과, 틀린 답 중 config를 실제로 바꾼 비율 | 두 layer를 잇는 숫자 |
| latency | `mode_correct = 1`인 row의 P50/P99 | |

**신뢰구간은 query point가 아니라 workload 파일을 resample해요.** 한 파일 안의 query point들은 같은 process 이름과 같은 상황을 공유하니 독립이 아니에요. 조건끼리 비교할 때는 **같은 draw 위에서 짝지어** 계산해요 — 모든 조건이 똑같은 query point에서 채점되니까요. seed와 반복 횟수는 고정이라 다시 돌려도 bound가 byte 단위로 같아요.

**familiarity tier는 row에 적기만 하고 tier별 aggregate는 안 내요.** 지금 core set에서 tier가 적힌 segment는 2개(C5 파일 둘, `c5-t4`의 tier 4와 `c5-t5`의 tier 5)뿐이고 각각 채점되는 query point가 **1개**예요. tier 1–3은 core set에 없어요(tier 3 파일이던 `c5-t3`은 2026-10-12에 C6의 `c6-alias`가 됐어요). 답 하나로 비율을 내면 안 되니까, tier가 답하는 질문(rule 기반 recognizer의 천장)은 **별도 experiment**로 빼뒀어요. 그 재료는 generated layer의 familiarity ladder(66개 파일)예요.

run-to-run consistency(같은 snapshot에 매번 같은 답을 하나)는 같은 query point의 sample이 여러 개 있어야 계산돼요. 지금 log 형식에는 "이게 몇 번째 sample인지"의 index가 없어서 박이안에게 memo로 요청해뒀어요.

---

## 9. observation window — `T_end` 규칙

모든 primitive는 `[0, T_end]` 안에서 측정돼요. `T_end`는 run file에서 가장 늦은 pinned 시각 — arrive, depart, wake event 중 최대. run file에는 `ground_truth`가 없으니 이게 유일한 출처이고, coreset에서는 마지막 segment의 끝과 같아요.

- `t > T_end`인 observation은 버려요. `ready`가 `T_end` 뒤면 row 없음.
- CPU 회계는 `T_end`에서 잘라요. `T_end`에 열려 있는 occupancy interval은 `T_end`까지만 세요.
- `T_end`에 살아 있는 task는 "window 안에 안 끝남"이에요. `completed=0`, `turnaround` 없음.
- simulator가 `T_end` 뒤를 더 돌렸든 말든 어떤 숫자에도 영향 없어요.

왜 이 규칙이 필요한가. 어느 문서도 "run이 언제 끝나는가"를 정해두지 않았어요. `c2-p1a`의 `hog`는 99.435초 뒤에도 혼자 계속 돌 수 있어요. simulator가 거기서 멈추든 계속 가든, harness가 `T_end`에서 자르면 숫자는 같아요. 그래서 인경민에게는 "멈춰도 안전하다"고 조언만 했고, contract에는 넣지 않았어요.

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
    { "op": "arrive", "t": 0, "id": "editor", "name": "code", "declared_class": "normal", "depart": 100000,
      "program": [ { "op": "WAIT", "channel": "input:editor" }, { "op": "RUN", "us": 3000 },
                   { "op": "WAIT", "channel": "input:editor" }, { "op": "RUN", "us": 4000 },
                   { "op": "WAIT", "channel": "input:editor" }, { "op": "RUN", "us": 2000 } ] },
    { "op": "arrive", "t": 40000, "id": "hog", "name": "python", "declared_class": "normal",
      "program": [ { "op": "RUN", "us": 80000 }, { "op": "EXIT" } ] },
    { "op": "wake", "t": 10000, "channel": "input:editor", "target": "editor" },
    { "op": "wake", "t": 22000, "channel": "input:editor", "target": "editor" },
    { "op": "wake", "t": 45000, "channel": "input:editor", "target": "editor" }
  ]
}
```

이 예시는 읽기 편하게 compiled 파일 모양(`meta`, `ground_truth`, `events`)으로 적었어요. harness가 run file로 읽는 건 `events`뿐이고, 거기서 네 가지를 읽어요:
- `T_end` = 100000 (가장 늦은 pinned 시각, editor의 depart. `ground_truth`의 마지막 `t_end`와 같아요)
- chain topology: TIMER를 가진 task가 없으니 chain 없음
- demand: `editor` = 3000 + 4000 + 2000 = 9000, `hog` = 80000
- channel: editor의 `WAIT` 셋이 모두 `input`, `input` wake event 세 개(keystroke 셋)

미리 보이는 것: `hog`는 40000에 와서 80000짜리 일을 해야 하는데 window가 60000밖에 안 남았어요. 못 끝나요. editor 혼자면 그것도 못 끝났을 거예요. 실제 `c2-p1a`와 같은 구조예요.

### 10.2 config schedule (이 trace를 만든 조건)

condition `llm_vocab`, prior table. boot 설정이 0에, recognizer의 답이 40000 + latency 450 = 40450에 적용돼요. algorithm은 그대로 MLFQ이고 cap만 바뀌는 entry라서 찍힌 시각에 바로 적용되고(drain 없음, 앞에서 drain 중인 switch도 없음), hog의 queue level과 받은 slice는 그대로예요. MLFQ의 boost timer는 이 시각에서 다시 시작해요(13장 가정 5번). algorithm이 바뀌는 entry는, FIFO에서 나가는 것이 아니면, task가 의자에 앉아 있을 때 의자가 빌 때까지 기다렸다가 적용돼요(drain; data-contracts 문서의 config schedule 절, 13장 가정 6번).

### 10.3 trace

scheduler는 아무 legal한 것이어도 돼요. 이 mock은 MLFQ(queue 3개, slice 2000, growth 2)를 simulator guide의 규칙대로 돌려요(boot default는 2026-09-11부터 OSTEP 예시의 10 ms slice예요; 이 mock의 2 ms는 계산을 짧게 하려고 고른 legal config예요): slice를 다 쓰면 한 칸 내려가고, block하면 그 자리에 머물고, 더 높은 queue로 깨어나면 즉시 preempt, 같거나 낮은 queue면 slice 경계까지 기다려요. 시각은 µs.

```jsonl
{"event":"meta","workload_id":"mock-c2-p1a","condition":"llm_vocab","sim":"mock@0","schedule_entries":2}
{"event":"config_applied","t":0,"index":0,"algorithm":"MLFQ","provenance":"fallback"}
{"event":"task_arrive","t":0,"task":"editor","source":"file"}
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
| 0 | boot 설정 적용. editor 등장. 첫 명령이 `WAIT`라 등장하는 step에서 바로 block — `ready` line도, 의자에 앉는 일도 없음 |
| 10000 | keystroke 1. 의자가 비어 있어 바로 앉음. 3000 일함 — Q0 slice 2000을 다 써서 12000에 Q1로 내려감. 13000에 block, Q1에 머묾 |
| 22000 | keystroke 2. 바로 앉음. 4000 일함 — Q1 slice 4000을 26000에 다 쓰고 Q2로. block |
| 40000 | hog 등장, Q0에 바로 앉음. 80000짜리 일 시작 |
| 40450 | recognizer의 답(ml-train, wanted) 적용. `unmodified`. 같은 algorithm이라 hog는 그대로 |
| 42000 | hog의 Q0 slice 다 써서 Q1 |
| 45000 | keystroke 3. editor는 Q2, hog는 Q1 → preempt 없음. editor는 줄 섬 |
| 46000 | hog의 Q1 slice가 끝나 Q2 뒤로 감. editor(Q2, 45000부터 대기) 앉음(`preempt`). 2000 일함 |
| 48000 | editor 끝. hog 다시 앉음 |
| 100000 | `T_end`. editor 퇴장(`depart`). hog는 아직 앉아 있음 |
| 122000 | hog 일 끝남(`exit`). window 밖 |

시각 0의 editor처럼 첫 명령이 `WAIT`인 task는 등장하는 step에서 앞쪽 명령을 의자 없이 실행하다가 그 `WAIT`에서 block돼요(그 channel에 미리 와 있는 wake가 없으면요). 그래서 trace에는 `task_arrive`만 있고 `ready(arrive)`도 `run_start`도 occupancy도 없어요. reference simulator가 이렇게 하고(`on_arrive`; `FORK`로 만든 자식은 `spawn`에서 같은 일), harness의 mock도 2026-10-17부터 그대로 따라요(metrics doc의 simulator 가정 5번). 그 task의 첫 `ready` line은 그 `WAIT`을 완료하는 wake예요 — 여기서는 10000의 keystroke. mock이 어떤 가정을 갖고 있는지는 metrics doc 한 곳에 목록으로 적어둬요.

### 10.4 records 계산

identity column은 모든 row가 같아요. `workload_id=mock-c2-p1a`, `condition=llm_vocab`, `table=prior`, `seed=` (빈칸), `boot_default=` (빈칸, primary), `telemetry=focus`, `sim=mock@0`, `source_sha256=` (trace 파일의 sha256). 아래에서는 observation과 attribute만 써요.

**`ready_wait`** — `ready` line 4개 → row 4개. editor는 등장할 때 `ready` line이 없으니 `cause=arrive` row도 없어요(10.3). wake row는 완료한 `WAIT`의 channel 종류를 실어요(모두 `input`).

| ready line | 다음 run_start | value | row |
|---|---|---|---|
| t=10000 editor wake | 10000 | 0 | `editor, ready_wait, 10000, 0, cause=wake, channel=input` |
| t=22000 editor wake | 22000 | 0 | `editor, ready_wait, 22000, 0, cause=wake, channel=input` |
| t=40000 hog arrive | 40000 | 0 | `hog, ready_wait, 40000, 0, cause=arrive` |
| t=45000 editor wake | 46000 | 1000 | `editor, ready_wait, 45000, 1000, cause=wake, channel=input` |

**`job`** — TIMER task 없음. row 없음.

**task lifetime** — task마다.

editor:
- `arrival` = 0 (`task_arrive`의 시각)
- occupancy: [10000,13000], [22000,26000], [46000,48000] → `cpu_delivered` = 3000 + 4000 + 2000 = 9000
- `task_end`가 `depart`라서 `completed` = 0, `turnaround` 없음
- `demand` = 9000
- `preempt_count` = 0

hog:
- `arrival` = 40000
- occupancy: [40000,46000], [48000, 열림) → `T_end`에서 clip: [48000,100000] → `cpu_delivered` = 6000 + 52000 = 58000
- `task_end(exit)`은 122000, window 밖 → `completed` = 0, `turnaround` 없음
- `demand` = 80000
- `preempt_count` = 1

| row |
|---|
| `editor, arrival, 100000, 0` |
| `editor, cpu_delivered, 100000, 9000` |
| `editor, completed, 100000, 0` |
| `editor, demand, 100000, 9000` |
| `editor, preempt_count, 100000, 0` |
| `hog, arrival, 100000, 40000` |
| `hog, cpu_delivered, 100000, 58000` |
| `hog, completed, 100000, 0` |
| `hog, demand, 100000, 80000` |
| `hog, preempt_count, 100000, 1` |

task 전체에 대한 값의 `t`는 `T_end`로 적었어요. `completed=1`이면 `t`는 `task_end`의 시각이에요. 이 anchor 규칙은 5.1에서 확정됐어요: window 전체에 대한 값(`arrival`, `cpu_delivered`, `demand`, `preempt_count`, `busy`, 그리고 0인 `completed`)은 `T_end`, `completed=1`과 `turnaround`는 `task_end`의 시각. `arrival`은 2026-10-17(9.15)에 같은 자리로 더해졌어요(7.6).

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
workload_id,condition,table,seed,boot_default,telemetry,sim,source_sha256,entity,metric,t,value,cause,channel,provenance,algorithm,index,period_us,predicted,truth,validation,familiarity,hogs,pre_committed_miss,skipped
mock-c2-p1a,llm_vocab,prior,,,focus,mock@0,<sha>,editor,ready_wait,10000,0,wake,input,,,,,,,,,,,
mock-c2-p1a,llm_vocab,prior,,,focus,mock@0,<sha>,editor,ready_wait,22000,0,wake,input,,,,,,,,,,,
mock-c2-p1a,llm_vocab,prior,,,focus,mock@0,<sha>,hog,ready_wait,40000,0,arrive,,,,,,,,,,,,
mock-c2-p1a,llm_vocab,prior,,,focus,mock@0,<sha>,editor,ready_wait,45000,1000,wake,input,,,,,,,,,,,
mock-c2-p1a,llm_vocab,prior,,,focus,mock@0,<sha>,editor,arrival,100000,0,,,,,,,,,,,,,
mock-c2-p1a,llm_vocab,prior,,,focus,mock@0,<sha>,editor,cpu_delivered,100000,9000,,,,,,,,,,,,,
mock-c2-p1a,llm_vocab,prior,,,focus,mock@0,<sha>,editor,completed,100000,0,,,,,,,,,,,,,
mock-c2-p1a,llm_vocab,prior,,,focus,mock@0,<sha>,editor,demand,100000,9000,,,,,,,,,,,,,
mock-c2-p1a,llm_vocab,prior,,,focus,mock@0,<sha>,editor,preempt_count,100000,0,,,,,,,,,,,,,
mock-c2-p1a,llm_vocab,prior,,,focus,mock@0,<sha>,hog,arrival,100000,40000,,,,,,,,,,,,,
mock-c2-p1a,llm_vocab,prior,,,focus,mock@0,<sha>,hog,cpu_delivered,100000,58000,,,,,,,,,,,,,
mock-c2-p1a,llm_vocab,prior,,,focus,mock@0,<sha>,hog,completed,100000,0,,,,,,,,,,,,,
mock-c2-p1a,llm_vocab,prior,,,focus,mock@0,<sha>,hog,demand,100000,80000,,,,,,,,,,,,,
mock-c2-p1a,llm_vocab,prior,,,focus,mock@0,<sha>,hog,preempt_count,100000,1,,,,,,,,,,,,,
mock-c2-p1a,llm_vocab,prior,,,focus,mock@0,<sha>,schedule,config_interval,0,40450,,,fallback,MLFQ,0,,,,,,,,
mock-c2-p1a,llm_vocab,prior,,,focus,mock@0,<sha>,schedule,config_interval,40450,59550,,,unmodified,MLFQ,1,,,,,,,,
mock-c2-p1a,llm_vocab,prior,,,focus,mock@0,<sha>,lane,busy,100000,67000,,,,,,,,,,,,,
```

row의 순서는 정해져 있어요: `entity`, `metric`, `t`(숫자), `cause`, `channel` 순. 위 표는 계산 순서대로 적은 것이라 정렬 전이에요. `<sha>` 자리에는 실제 fixture에서 trace 파일의 sha256이 그대로 들어가고, 나머지 attribute column(recognizer row의 것, `hogs`, `job`의 `period_us`와 `skipped`)은 여기서 전부 빈칸이에요. 이 trace와 run file을 harness의 `records.build`에 넣으면 정렬된 같은 17개 row가 나와요.

### 10.6 이 records에서 읽히는 것

scoring이 아니라 "이 row들로 뭘 말할 수 있나"의 맛보기.

- editor의 keystroke 대기: `cause=wake`, `channel=input` row 3개, value [0, 0, 1000]. 최대 1 ms. 100 ms 임계값을 넘은 건 0개.
- hog의 progress: 58000 / 80000 = 72.5%.
- fallback으로 돈 비율: 40450 / 100000 = 40.45%. 이 파일에서는 당연해요. training run이 40000에 와야 recognizer가 뭔가 할 수 있으니까.
- utilisation: 67000 / 100000 = 67%.

여기서 "editor가 interactive task다", "hog가 batch다"를 harness는 몰라요. scoring이 `c2-p1a`의 scoring spec을 읽고 "editor의 `ready_wait(cause=wake, channel=input)`를 보라"고 정해요.

---

## 11. 두 번째 mock — 늦은 frame과 건너뛴 tick

fixture `mock-media`(`harness/tools/tests/fixtures/mock-media/`)는 `c1-media`를 축소하고 batch 하나를 끼운 것이에요. 이 mock의 목적은 둘이에요. **TIMER skip 규칙을 harness가 어떻게 읽는지**, 그리고 그 읽기가 왜 **"`ready` line이 즉시 완료된 blocking primitive에서도 나와야 한다"**는 규칙에 기대는지.

규칙부터. TIMER task가 자기 TIMER에 도달했을 때 grid의 tick이 이미 여러 개 지나 있으면, **가장 최근에 지난 tick 하나를 바로 소비하고**(그 job은 지금 시작하고 마감은 다음 tick) **그보다 앞의 소비 안 된 tick은 전부 건너뛰어요.** 건너뛴 tick은 일을 하나도 안 한 job이고, miss예요. chain이면 head에서만 건너뛰어요(2026-10-07 memo, `docs/memos/2026-10-07-timer-skip-rule-for-the-simulator.md`). harness는 2026-10-09부터 trace를 이 규칙으로 읽어요(metrics doc의 `job` 절). reference simulator는 2026-10-23부터(stage Y) 이 규칙을 돌려요. RQ0 gate spec의 simulator-conformance 항목 (b)예요.

| task | 이름 | 등장 | 퇴장 | program |
|---|---|---|---|---|
| `video` | `mpv` | 0 | 95000 | `LOOP { TIMER(16667) → RUN(6667) }` |
| `music` | `spotify` | 0 | 95000 | `LOOP { TIMER(50000) → RUN(2500) }` |
| `scan` | `clamscan` | 20000 | — | `RUN(46666) → EXIT` |

scheduler는 FIFO(block할 때까지 돌고 preempt 없음)예요. oracle의 답이 boot 설정 옆에 0으로 찍혀서 FIFO가 돼요. `T_end` = 95000. 두 player 모두 등장하는 step에서 첫 TIMER를 실행하니 grid는 0에서 시작해요(7.2). `video`의 tick은 0, 16667, 33334, 50001, 66668, 83335(100002는 `T_end` 뒤), `music`의 tick은 0, 50000(100000은 `T_end` 뒤).

### 11.1 trace (video 부분)

```jsonl
{"event":"task_arrive","t":0,"task":"video","source":"file"}
{"event":"ready","t":0,"task":"video","cause":"arrive"}
{"event":"ready","t":0,"task":"video","cause":"timer_tick"}
{"event":"run_start","t":0,"task":"video"}
{"event":"run_end","t":6667,"task":"video","reason":"block","blocked_on":"timer"}
{"event":"deadline","t":6667,"task":"video","due":16667,"met":true,"slack_us":10000}
{"event":"ready","t":16667,"task":"video","cause":"timer_tick"}
{"event":"run_start","t":16667,"task":"video"}
{"event":"run_end","t":23334,"task":"video","reason":"block","blocked_on":"timer"}
{"event":"deadline","t":23334,"task":"video","due":33334,"met":true,"slack_us":10000}
{"event":"ready","t":33334,"task":"video","cause":"timer_tick"}
{"event":"run_start","t":70000,"task":"video"}
{"event":"deadline","t":76667,"task":"video","due":50001,"met":false,"slack_us":-26666}
{"event":"deadline","t":76667,"task":"video","due":66668,"met":false,"slack_us":-9999}
{"event":"ready","t":76667,"task":"video","cause":"timer_tick"}
{"event":"run_end","t":83334,"task":"video","reason":"block","blocked_on":"timer"}
{"event":"deadline","t":83334,"task":"video","due":83335,"met":true,"slack_us":1}
{"event":"ready","t":83335,"task":"video","cause":"timer_tick"}
{"event":"run_start","t":85834,"task":"video"}
{"event":"run_end","t":92501,"task":"video","reason":"block","blocked_on":"timer"}
{"event":"deadline","t":92501,"task":"video","due":100002,"met":true,"slack_us":7501}
{"event":"task_end","t":95000,"task":"video","reason":"depart"}
```

무슨 일이 일어났나:

- 0: `video`와 `music`이 등장하고(file 순서), 각자 등장하는 step에서 의자 없이 첫 명령 TIMER를 실행해요. tick 0이 지금이라 block 없이 완료되고, `ready(arrive)`와 `ready(timer_tick)`가 첫 `run_start` 앞에 찍혀요. `video`가 먼저 앉아 frame 0을 그리고 6667에 다음 TIMER에서 block. `music`은 6667에 처음 앉아요.
- 16667: tick 1. 바로 앉아서 frame 1, 23334에 끝.
- 20000에 `scan`이 와서 줄 서고, 23334에 `video`가 block하자 앉아요. FIFO라 끝날 때(70000)까지 안 내려와요.
- 33334: tick 2. `video`가 runnable해졌지만 의자에 `scan`.
- 50001(tick 3), 66668(tick 4): `video`는 이미 줄 서 있어서 아무 line도 없어요. 완료된 blocking primitive가 없으니까요.
- 70000: `scan` 종료. `video`가 앉아 frame 2를 그리고 76667에 끝내요. 마감(50001)을 한참 넘긴 miss.
- 76667: `video`가 다음 TIMER에 도달. tick 3(50001)과 tick 4(66668)는 지났고 tick 5(83335)는 아직이에요. skip 규칙: 가장 최근에 지난 **tick 4를 바로 소비**하고(`ready(timer_tick)`가 76667에, 자기 occupancy 안에) **tick 3은 건너뛰어요** — 그 tick의 일은 아예 안 해요. simulator는 tick 순서대로 `deadline` line을 써요: job 2의 것(miss), 건너뛴 tick 3의 것(`met: false`, 완료가 없으니 harness는 slack 말고 `met`만 읽어요).
- tick 4의 job(frame 4)은 76667에 시작해서 83334에 끝나요. 마감은 다음 tick인 83335라 1 µs 차로 met. 83334에 TIMER에 도달하면 tick 5까지 1 µs가 남아 진짜로 block해요.
- 83334에 `music`이 앉고(tick 1의 50000부터 줄 서 있었어요), 83335의 tick 5에 `video`가 runnable해져도 FIFO라 85834까지 기다렸다가 frame 5를 그려요(92501, met).

**`ready` line이 즉시 완료된 TIMER에서 나오지 않았다면** 76667의 line이 없어요. 그러면 70000부터 83334까지는 `run_start` 하나, `run_end` 하나뿐인 13334 µs짜리 occupancy 하나이고, frame 2와 frame 4의 경계가 trace에 안 보여요. harness는 그 trace를 "frame 2가 83334에 끝났고 tick 3과 4를 둘 다 건너뛰었다"로 읽게 돼요 — miss가 하나 늘고, `deadline` 교차검사가 두 군데서 어긋나요. 정확히 늦은 frame들에서만 생기는 일이에요. 그래서 이 규칙을 인경민에게 요청했어요(metrics doc의 simulator 가정 1번). reference simulator는 2026-10-23부터(stage X) 이 zero-wait line을 내요 — RQ0 gate spec의 simulator-conformance 항목 (a)예요 — 그리고 harness의 skip 읽기는 그 line에 기대고 있어요.

### 11.2 records

**`ready_wait`** (`video`): 자기 occupancy 안에 떨어진 `ready`는 value 0.

| ready | 짝 | value | 비고 |
|---|---|---|---|
| 0 `arrive` | `run_start` 0 | 0 | |
| 0 `timer_tick` | `run_start` 0 | 0 | tick 0을 등장하는 step에서 소비 |
| 16667 `timer_tick` | `run_start` 16667 | 0 | |
| 33334 `timer_tick` | `run_start` 70000 | 36666 | 진짜 기다림 |
| 76667 `timer_tick` | occupancy [70000, 83334] 안 | 0 | tick 4를 바로 소비 |
| 83335 `timer_tick` | `run_start` 85834 | 2499 | |

window 안의 tick은 여섯인데 `timer_tick` row는 다섯이에요. 건너뛴 tick 3은 line이 없어요.

**`job`** (`video`, period 16667): 소비된 tick의 완료 = 그 iteration의 `RUN`이 끝나고 다음 TIMER에 도달한 시각.

| k | tick | 완료 | value | skipped | period 대비 |
|---|---|---|---|---|---|
| 0 | 0 | 6667 | 6667 | 0 | met |
| 1 | 16667 | 23334 | 6667 | 0 | met |
| 2 | 33334 | 76667 | 43333 | 0 | **miss** |
| 3 | 50001 | — | (빈칸) | 1 | **miss (건너뜀)** |
| 4 | 66668 | 83334 | 16666 | 0 | met |
| 5 | 83335 | 92501 | 9166 | 0 | met |

```
video, job, 0,     6667,  period_us=16667, skipped=0
video, job, 16667, 6667,  period_us=16667, skipped=0
video, job, 33334, 43333, period_us=16667, skipped=0
video, job, 50001, ,      period_us=16667, skipped=1
video, job, 66668, 16666, period_us=16667, skipped=0
video, job, 83335, 9166,  period_us=16667, skipped=0
```

`video`의 miss rate는 6개 중 2개예요. frame 4는 tick 66668의 job인데 실제로는 76667에야 시작했어요. 그래도 늦은 job은 "가장 최근에 지난 tick의 것, 지금 시작, 마감은 다음 tick"이라 83335가 마감이고, 83334에 끝나서 met이에요.

**guard:** 소비된 tick 다섯 = iteration 끝 다섯이라 chain guard가 통과해요. 소비가 tick 번호를 앞으로 못 밀면 그것도 guard예요. `deadline` line 여섯은 tick 순서로 row와 짝지어지고, 소비된 tick의 line은 완료 시각과 slack이 row와 같아야 하고, 건너뛴 tick의 line은 `met: false`이기만 하면 돼요.

**`music`.** `music`도 등장하는 step에서 첫 TIMER를 실행하니 `t₀`는 등장 시각 0이고 grid는 0과 50000이에요(metrics doc의 simulator 가정 4번). 의자에 `video`가 있어서 6667에 처음 앉아 job 0을 9167에 끝내고(0 → 9167), job 1은 `scan`과 `video` 뒤에서 83334에 앉아 85834에 끝내요(50000 → 85834, value 35834). 마감은 각각 50000과 100000이라 둘 다 met이에요. tick 0의 `ready(timer_tick)`는 등장하는 순간, 자기 occupancy 밖에 찍히니 다음 `run_start`(6667)와 짝지어져 `ready_wait`가 6667이에요. fixture는 2026-10-17에 이 읽기로 다시 유도됐어요.

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
s1, job, 0,     4500,  period_us=16667, skipped=0
s1, job, 16667, 17833, period_us=16667, skipped=0
s1, job, 33334, 5666,  period_us=16667, skipped=0
```

여기서는 건너뛴 tick이 없어서 k번째 tick이 그대로 tail의 k번째 iteration이에요. tick을 건너뛰면 "head가 j번째로 소비한 tick ↔ tail의 j번째 iteration"으로 짝지어요(7.2).

entity는 chain의 head인 s1이에요. "이 chain의 frame"이라는 뜻으로.

**`deadline` line과 비교:** head의 line은 frame 1을 met이라고 해요(31000 < 33334). 하지만 화면에 frame이 나온 건 34500이고 이건 33334를 넘었어요. 게임 파일의 17개 task chain에서는 이 차이가 훨씬 커요. `c1-gaming`에서 head는 631 µs이고 나머지 16개 task가 합쳐서 14,368 µs니까. 그래서 harness가 재구성하고, `deadline`은 단일 TIMER task에서만 cross-check로 써요.

**guard:** tail이 끝낸 iteration 수(3)가 head가 소비한 tick 수(3)를 넘지 않아요. 통과예요. 넘으면 head가 보낸 적 없는 wake로 frame이 끝났다는 뜻이에요. 반대로 wake가 큐에 쌓이지 않고 사라지는 simulator면 어느 stage에서 frame 하나가 빠져 tail이 모자라는데, 이 guard는 그걸 잡지 못해요 — `T_end`에 아직 도는 frame과 같은 모양이니까요. guard spec의 `tick_count` grounding이 이 약점을 적어요.

**`ready_wait`도 같이 나와요.** chain stage의 `WAIT`가 완료되는 것도 `cause=wake`예요. trace는 channel을 안 적지만, harness가 run file에서 그 `WAIT`의 channel 종류를 읽어 row에 실으니(4.4) chain stage의 row는 `channel=chain`, keystroke의 row는 `channel=input`으로 구분돼요. 그래서 `c6-dual`처럼 editor와 게임이 한 파일에 있어도 섞이지 않아요.

---

## 13. harness가 simulator에 기대는 가정

mock trace는 어떤 simulator 동작을 전제하고 쓰여요. 그 전제가 metrics doc 한 곳에 목록으로 있어야, 인경민이 다르게 결정했을 때 mock을 "우연히 틀린 것"이 아니라 "의도적으로 바꾸는 것"으로 다룰 수 있어요. 인경민에게 보낸 memo(`docs/memos/2026-09-07-trace-clarifications-for-the-simulator.md`)의 내용이에요.

| # | 가정 | 없으면 |
|---|---|---|
| 1 | blocking primitive가 완료될 때마다 `ready` line. 즉시 완료면 wait 0 | 큐에 쌓인 keystroke가 사라짐. occupancy 안에서 바로 소비된 tick의 job 경계가 안 보여서, harness가 그 tick을 건너뛴 것으로 잘못 읽음 (11장) |
| 2 | wake는 깊이를 갖고 큐에 쌓임. stage 6이 stage 7을 두 번 깨우면 stage 7은 나중에 `WAIT` 두 개를 완료 | chain 중간에서 frame이 빠지고 그 뒤 모든 tick/iteration 짝이 어긋남 (12장) |
| 3 | 같은 µs에 일어난 event의 순서가 문서화된 deterministic 규칙을 따름 | mock과 실제 trace를 byte 비교할 수 없음 |
| 4 | `deadline` line은 contract대로 계속 emit | cross-check를 잃음 |
| 5 | boost timer는 MLFQ entry가 적용될 때마다 그 적용 시각에서 다시 시작: MLFQ로의 switch의 `t_apply`(인경민 확인, 2026-09-09)와 그 뒤 같은 algorithm의 entry 각각(reference simulator가 entry를 적용할 때마다 boost를 새로 걸어요; 2026-10-17 결정) | 7.10의 boost 변형이 보는 시점들이 달라짐 |
| 6 | FIFO에서 나가는 switch는 즉시 적용(지금 앉아 있는 task는 새 algorithm이 막 dispatch한 것으로 침), 다른 algorithm에서 나가는 switch는 task가 의자에 있으면 의자가 빌 때 적용 — 그 task의 slice나 지금의 `RUN`이 끝나거나, preempt되거나 depart할 때(drain). 의자가 비어 있으면 찍힌 시각에 (memo의 규칙 (a), 인경민 확인, 2026-09-09; drain의 시점은 data-contracts 문서의 config schedule 절, 2026-10-17) | `mock-switch`의 적용 시각이 달라짐 |
| 7 | 같은 algorithm의 entry(params나 cap만 바뀜)는 switch가 아니라 찍힌 시각에 바로 적용, queue level 유지 (인경민 확인, 2026-09-09). 단 entry는 index 순서로 적용돼서, switch가 drain 중일 때 찍힌 entry는 같은 algorithm의 것이어도 그 switch 뒤에서 기다렸다가 같은 순간 그 다음에 적용 (2026-10-17 결정; reference simulator는 2026-10-10부터 그렇게 해요). MLFQ면 boost timer가 그 적용 시각에서 다시 시작(5번) | `mock-p1a`와 10장의 적용 시각이 달라짐 |

그리고 조언 하나: `T_end` 뒤는 harness가 안 읽으니 거기서 멈춰도 돼요. 이건 contract가 아니에요.

이 중 1–3이 다르게 결정되면 mock을 고쳐요. 그래서 5.1(mock)을 5.3(reader)보다 먼저 하고, 인경민의 답을 mock이 확정되기 전에 받는 게 좋아요.

---

## 14. records 위에 올라가는 것 — aggregate, normalisation, score

여기서부터는 Phase 5의 범위 밖(Phase 6, 8)이지만, records를 왜 이렇게 만드는지 이해하려면 그 위를 알아야 해요. 정의는 metrics doc에 있고 code는 Phase 8에서 만들었어요(`harness/tools/harness/aggregates.py`, `scorer.py`).

### 14.1 aggregate — row들을 숫자 하나로

primitive마다 고정된 aggregate 목록이 있어요.

**`ready_wait`**: count, mean, P50, P95, P99, max, `over_threshold`.

`over_threshold`는 "interaction-latency 임계값을 넘은 row의 비율"이에요. 임계값은 상수 `T_interaction` 하나, 100,000 µs(0.1초)이고 design 값이에요. Miller(1968)가 keystroke에서 화면 echo까지 0.1–0.2초를 넘지 말라고 한 guideline 범위의 엄한 쪽 끝을 골랐고(`miller-fjcc68`), Deber et al.(2015)이 측정한 지연 감지 threshold로 교차 확인했어요(`deber-chi15`). 지각 threshold를 잰 값이 아니라 guideline에서 고른 값이에요. 이 상수는 keystroke row(`cause=wake`, `channel=input`)를 읽으려고 정한 값이에요. 비율 자체는 harness가 어느 filter에서나 내요(metrics doc의 constants 절). "P95가 47 ms였다"보다 "keystroke의 8%가 임계값을 넘었다"가 파일 간 비교가 쉽고 사람에게 전달이 잘 돼요. 하지만 percentile도 같이 봐요. 비율은 "아슬아슬하게 맞춤"과 "여유 있게 맞춤"을 구분 못 하니까.

**`job`**: count, miss rate (`value > period_us`인 비율), latency P50, P99. 건너뛴 tick(`skipped=1`)은 count와 miss rate에는 miss로 들어가고 latency percentile에서는 빠져요(값이 없으니까).

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

floor를 절대값으로 두는 이유: 독자가 숫자를 보고 직접 확인할 수 있어요. 실제 latency floor는 1,000 µs(1 ms)이고 design 값이에요 — 두 configuration 사이의 1 ms 미만 latency 차이는 읽지 않는다는 선이고, 어떤 scheduler parameter에도 묶여 있지 않아요. 비율 aggregate(`over_threshold`, miss rate, progress)의 floor는 0.01(1%p)이에요. RQ0 gate spec은 floor를 0.5 / 1 / 2 / 5 ms로 바꿔 판정을 다시 세는 line을 미리 등록해뒀어요(19.4).

### 14.4 score — weight를 곱하기

normalised aggregate에 파일별 weight를 곱해 합친 게 score예요. weight는 연구 판단이라 code가 아니라 committed data file(**scoring spec**, `harness/scoring/scoring-spec.yaml`)에 있어요. Phase 6에서 확정됐고, 2026-10-09(9.14)에 다시 지은 dataset 위에서 고쳐졌어요. 실제 파일의 한 조각:

```yaml
  c2-p1a:
    terms:
      - {entity: editor, metric: ready_wait, cause: wake, channel: input, window: {start_us: 60000000, end_us: 99435000}, aggregate: p99, direction: lower, weight: 1.0}
      - {entity: hog, metric: cpu_delivered, aggregate: progress, direction: higher, weight: 0.5}
  c2-p1b:
    terms:
      - {entity: editor, metric: ready_wait, cause: wake, channel: input, window: {start_us: 60000000, end_us: 99435000}, aggregate: p99, direction: lower, weight: 1.0}
```

term 하나 = entity(누구), metric(어느 primitive), cause·channel·window(어느 row만), aggregate(어떤 통계), direction(aggregate가 정함), weight. 옆의 lint가 entity가 compiled workload에 실제로 있는 task인지, metric/aggregate 짝이 허용된 것인지, window가 그 파일의 ground-truth segment인지, 파생 파일이 base와 같은지(label을 unwanted로 뒤집은 C7 counterpart는 base에서 batch term만 뺀 것과 같은지)를 CI에서 검사해요.

이 예시가 records 설계의 이유를 보여줘요. `c2-p1a`와 `c2-p1b`는 60초에 오는 background job 하나와 그 segment의 label만 달라요 — `c2-p1a`는 training run(`python`, wanted), `c2-p1b`는 Tracker의 indexer(`tracker-miner-f`, unwanted, idle class). 그 전의 event는 두 파일이 똑같아요. weight가 label이 말하는 가치를 담아요. training run의 progress는 점수에 들어가고(0.5), 아무도 원하지 않은 indexing의 진행에는 term이 없어요.

---

## 15. 어떤 score가 좋을까 — 파일별로

Phase 6 spec 세션(2026-09-08)에서 처음 정했고, 다시 지은 dataset 위에서 2026-10-09(9.14)에 고쳤어요. 규범은 `harness/scoring/scoring-spec.yaml`(term)과 `harness/experiments/rq0-gate.yaml`(어느 파일이 판정에 들어가나) 자체이고, 여기는 왜 그렇게 정했는지의 요약이에요.

### 15.1 어느 파일이 판정에 들어가나

RQ0 gate("perfect recognition이 random보다 나은 headroom이 있나")의 judging set은 Phase 3에서는 C2의 6개 파일, Phase 7(2026-09-10)에서는 27개, 2026-09-12에 커밋된 RQ0 gate spec에서는 25개였고, 다시 지은 core set 위에서 2026-10-09(9.14)에 **19개**로 다시 정했어요. 규칙은 그대로예요: **label이 다른 pair의 한쪽이고, 그 파일의 scored term이 row 차이를 설계상 감지하는 파일.** demand는 기준이 아니에요. 판정은 judging 파일 19개 중 **K = 10개 이상**(과반)이 gap **g = 0.5 이상**이면 pass예요(`k_of_n_gap`; random은 seed N = 100개의 평균, 19.2). 나머지 core 파일 32개는 돌고 보고만 해요. 규범은 `harness/experiments/rq0-gate.yaml`이에요.

| 그룹 | 역할 |
|---|---|
| C2의 normal-class 쪽 4개(`c2-p1a`, `c2-p2a`, `c2-p2b`, `c2-p3a`) | judging |
| C1 batch base 4개(`c1-compile`, `c1-ml-train`, `c1-render`, `c1-transcode`) | judging — row의 share가 job까지 닿아요 |
| C7 counterpart 11개(`browsing`, `office`, `dev`, `photo`, `meeting`, `gaming`, `video-edit`, `compile`, `ml-train`, `render`, `transcode`) | judging. EDF를 쓰는 judging 파일(`c2-p2a`, `c2-p2b`, `c7-gaming`, `c7-meeting`)에서는 두 row가 scored term에서 설계상 비겨요 — EDF가 deadline class인 chain이나 call을 cap과 상관없이 먼저 돌리니까 — 그래서 gap은 EDF 대 random이 뽑은 algorithm, 즉 mode recognition을 읽어요. `c7-meeting`은 2026-10-09부터 judging이에요. 측정된 call의 cycle이 boot slice(10 ms)를 스무 번에 한 번꼴로(측정된 table에서 4.9 %, compile된 파일에서 5.5 %) 다 써서, 100 ms boost 간격 열 번 중 약 네 번은 call이 demotion되어 다음 boost까지 upgrade 뒤에서 기다려요(1 − 0.95¹⁰, cycle을 서로 독립으로, boost 간격 하나에 cycle 열 개로 본 계산). 그래서 예전의 짧은 burst에서 `fixed`와 비기던 일이 없어졌어요 |
| idle class job을 가진 6개(`c1-indexing`, `c7-indexing`, `c2-p1b`: Tracker의 indexer; `c1-backup`, `c7-backup`, `c2-p3b`: Déjà Dup의 backup) | 보고만. executor는 idle task를 다른 class의 task가 runnable하지 않을 때만 돌리고(모든 algorithm에서), cap은 work-conserving이라 어떤 row도 background job에 닿지 않아요 |
| `c7-mail` | 보고만. counterpart의 keystroke 창은 `c1-mail`의 것을 잘라 온 것인데, `c1-mail`의 keystroke 35개는 45.9–53.1초에 있어서 2–24.385초 창에 하나도 없어요. 그래서 term이 mailer 자신의 wake를 읽고, keystroke latency는 못 읽어요 |
| `c7-media` | 보고만. 측정된 table로는 `fixed`와도, 두 row 사이에서도 headroom이 없어요. video의 최악 cycle이 16.0 ms(주기 33.3 ms)이고 boot MLFQ가 줄 수 있는 가장 긴 대기까지 합쳐도 32 ms라, 여유 1.3 ms예요 |
| C1 interactive·periodic base 8개(`browsing`, `office`, `mail`, `dev`, `photo`, `meeting`, `media`, `video-edit`)와 `c1-gaming` | 보고만. foreground 뒤에 아무것도 없어 row가 움직일 게 없어요. strongest name table(`strongest_name_table` condition)이 만점을 받을 것으로 기대되는 C1 calibration 파일들이에요(C1 16개 전부에 해당). `c1-gaming`은 chain이 의자의 0.9를 쓰는 파일로 별도 보고 line(note)이 있고, pair가 없어서 judging이 아니에요 |
| `c1-idle`, `c7-idle` | 보고만. 성능 metric 없음(scoring spec에 entry가 없어요) |
| C3 (3), C4 (3), C5 (2: `c5-t4`, `c5-t5`), C6 (4: `c6-alias`, `c6-dual`, `c6-fold`, `c6-spoof`) | 보고만. RQ0 gate spec은 이들을 Layer 2 aggregation에서 빼요. C5는 `c1-media`의 player를 tier 4·5 이름으로 바꾼 것이라 성능 숫자가 `c1-media`와 같아야 하고, 다르면 bug 신호예요. C6은 recognition의 해상도 한계: `c6-dual`은 `ambiguous`, 나머지 셋은 미리 약속된 miss가 있어요 |
| `c2-p2a-idle` | 보고만. `c2-p2a`에서 download의 class만 idle로 바꾼 bounding check의 짝(19.4의 `bounding_pair`) |
| Layer-1 exclusion 8개(`c1-indexing`, `c6-alias`, `c6-fold`, `c6-spoof`, `c7-backup`, `c7-ml-train`, `c7-render`, `c7-transcode`) | `pre_committed_miss` segment를 가진 파일들. 그 segment 안의 query point가 recognition accuracy(Layer 1)의 headline에서만 빠져요 — 여섯 파일은 segment 하나가 파일 전체라 전부 빠지고, `c6-fold`는 통화가 오는 30초부터, `c6-spoof`는 spoof가 시작하는 20초부터라 그 앞의 point는 headline에 남아요(grader가 point마다 그 segment의 표시를 봐요, 17장). 이 중 `c7-ml-train`, `c7-render`, `c7-transcode`는 judging이고(gate는 label만 있으면 돼요), 나머지 다섯은 보고만 해요 |

### 15.2 파일별 term

채점되는 aggregate는 넷이에요: `ready_wait`는 **P99**, `job`은 **miss rate**, 그리고 batch job은 둘 중 하나 — 파일 안에서 끝나는 job은 **turnaround**, 어떤 row에서도 파일 안에 못 끝나는 job은 **progress**(`cpu_delivered / demand`). term은 row에 따라 움직이는 양을 읽어야 하니까요(9.14). 나머지 aggregate는 옆에 보고만 해요.

interaction latency term은 2026-10-09부터 모두 `channel`을 적어요. keystroke stream이 있는 task는 `input`이고, video editor(Kdenlive)와 image editor(GIMP)의 14개 term은 `timer`예요. 두 앱의 측정된 driven phase는 mouse로 하는 조작이라 keystroke stream이 없고, 그래서 그 term은 앱 자신의 timer component wake의 대기 — keystroke echo가 아니라 앱의 반응성 — 를 읽어요. `T_interaction` threshold line(14.1)은 `input`만 읽어요.

| 파일 | term (entity · aggregate · weight) |
|---|---|
| `c1-office` · `c1-browsing` · `c1-dev` · `c1-mail` | writer / browser / editor / mailer P99 (`input`) 1.0 |
| `c1-video-edit` · `c1-photo` | editor / photo-editor P99 (`timer`) 1.0 |
| `c1-compile` | editor P99 (`input`) 1.0 · build turnaround(makespan) 1.0 |
| `c1-gaming` | `game.chain.1` miss rate 1.0 (chain만. compositor task는 9.9에서 빠졌어요) |
| `c1-media` | music miss rate 1.0 · video miss rate 0.5 |
| `c1-meeting` | voice miss rate 1.0 (측정된 call은 task 하나, 10 ms audio frame마다 job 하나) |
| `c1-idle` | 없음 |
| `c1-ml-train` | editor P99 (`input`) 1.0 · hog turnaround **0.5** |
| `c1-render` · `c1-transcode` | editor / video-editor P99 (`timer`) 1.0 · bulk / batch turnaround **0.5** |
| `c1-indexing` | editor P99 (`input`) 1.0 · hog turnaround **1.0** (stated assumption: 사용자가 기다리는 reindex) |
| `c1-backup` | editor P99 (`timer`) 1.0 · bulk turnaround **0.25** |
| C7 (`c7-<mode>`) | base의 term에서 batch term을 뺀 것. interactive mode는 base와 같고, batch mode는 foreground P99만 (**원하지 않은 일에는 term이 없어요**; lint가 강제). 예외 `c7-mail`은 mailer P99 (`timer`) — 창에 keystroke가 없어서(15.1) |
| `c2-p1a` / `c2-p1b` | editor P99 (`input`, 60–99.435 s) 1.0 · hog progress 0.5 / 없음 |
| `c2-p2a` / `c2-p2b` | `game.chain.1` miss rate (60–86.385 s) 1.0 · download progress 0.5 / 없음 |
| `c2-p2a-idle` | `c2-p2a`와 같음 |
| `c2-p3a` / `c2-p3b` | editor P99 (`timer`, 60–326 s) 1.0 · bulk turnaround 0.5 (export가 모든 row에서 끝나요) / bulk turnaround **0.25** (예약된 backup. idle class라 editor가 남긴 lane만 받지만, 그 lane이 약 166초라 모든 row에서 파일 끝 약 0.3초 전에 끝나요) |
| `c3-workday` | browser · writer · mailer P99 (`input`) 각 1.0 · build progress 0.5 |
| `c3-evening` | browser P99 (`input`) 1.0 · chain miss rate 1.0 · music miss rate 1.0 · video miss rate 0.5 |
| `c3-creation` | photo-editor · video-editor P99 (`timer`) 각 1.0 · batch progress 0.5 |
| C4, C5, `c6-alias`, `c6-spoof`, `c6-fold` | base 파일의 term 그대로 (C4는 각자의 C1 base, C5와 `c6-alias`는 `c1-media`, `c6-spoof`·`c6-fold`는 `c1-browsing`; lint가 강제) |
| `c6-dual` | chain miss rate 1.0 · editor P99 (`input`) 1.0 |

C2의 latency/frame term은 60초부터 파일 끝까지만 봐요(P1 99.435초, P2 86.385초, P3 326초. 각 창은 그 파일의 두 번째 ground-truth segment예요). 첫 60초는 a와 b의 event가 똑같아서 차이를 희석시키기만 하거든요. 60초의 전환과 그 transient는 창 안이라 condition의 비용으로 잡혀요. batch term은 창이 없어요(batch job이 60초에 등장하니까). C3는 focus와 task 수명이 알아서 창 역할을 해서 명시적 창이 없어요.

### 15.3 판단이 필요했던 세 곳 — 어떻게 정했나

**C2 pair의 weight.** pair의 두 파일은 60초에 오는 background job 하나와 그 segment의 label만 달라요(14.4). 원한 batch — P1의 training run(`python`), P2의 game download(`steam`), P3의 video export(`kdenlive_render`) — 는 0.5. 원하지 않은 batch — P1b의 Tracker indexer(`tracker-miner-f`), P2b의 unattended upgrade(`unattended-upgr`) — 에는 term이 없어요. P3b의 예약된 backup(`deja-dup`)은 원한 일이지만 아무도 기다리지 않으니 0.25. foreground는 항상 1.0이에요. 사용자가 파일 내내 foreground 앱을 쓰는 중이라 foreground가 앞서요. P1과 P2의 job은 어떤 row에서도 파일 안에 못 끝나서 progress로, P3a의 export는 CPU 16.5초어치라 266초 segment 안에서 모든 row에서 끝나니 turnaround로 재요 — 끝나는 job의 progress는 어떤 row에서도 같아서 움직이지 않으니까요(9.14).

**`c1-compile`의 trade-off.** constrained objective 대신 weight 1.0 : 1.0으로 했어요. normalised share는 이미 `fixed`(boot 설정, cap 없음) 대비 부호가 있어서, build를 늦추는 config는 makespan share가 음수로 나오고 weight가 그 교환비예요. 별도의 constraint 형태는 필요 없었어요. mode 이름이 `compile`이라 build도 상황 그 자체예요. 이 파일은 judging이에요. build의 turnaround는 `make`가 `WAIT children:build`를 지나 `EXIT`해야 나오는데(7.6), 그 완료 규칙이 RQ0 gate spec의 simulator-conformance 항목 (g)예요. 그게 없으면 build term이 모든 condition에서 똑같이 censored돼요(못 끝난 job은 `T_end` − 등장으로 채점, metrics doc의 normalisation 절).

**`c1-media`의 audio/video weighting.** music 1.0 : video 0.5, stated assumption이에요(audio가 끊기면 바로 들리지만 frame 하나 빠진 건 못 알아챌 때가 많아요; 문헌 검색 안 함). 단, 이 파일에서는 어떤 legal config도 tick을 놓칠 수 없어요. compiled `c1-media`에 실린 두 player(둘 다 `mpv`)의 cycle 중 가장 긴 것이 video 11.5 ms(주기 33.3 ms), music 0.8 ms(주기 49.6 ms)라서(측정된 table에서 sample된 값이에요. 15.1의 `c7-media` row가 적는 16.0 ms는 table 자체의 최댓값이고요), video는 21.9 ms 넘게 기다려야 miss인데 music이 줄 수 있는 대기는 0.8 ms, 반대는 48.8 ms 대 11.5 ms예요. 그래서 두 miss rate가 전부 0이고 floor 규칙대로 "no headroom"이 나와요. weight는 contention이 있는 media 구간을 위해 적어두는 거예요. C5 두 파일과 `c6-alias`도 `c1-media`의 player 그대로라 같아요.

### 15.4 사람에게 전달되는 숫자

논문에 실릴 headline 후보:

- "keystroke의 X%가 100 ms 임계값을 넘었다" (over_threshold)
- "frame의 X%가 마감을 놓쳤다" (miss rate)
- "training run이 window 안에 X% 진행됐다" (progress)
- "fixed→oracle headroom의 X%를 llm_vocab이 가져갔다" (normalised)

전부 records의 row에서 한두 단계로 나와요.

### 15.5 generated layer의 파일 — entry 없이 규칙으로

generated layer의 파일 1,562개 — `transition-grid` 480, `return-grid` 720, `flap-stress` 24(2026-10-11, 9.19), `distractor-grid` 272, `familiarity-ladder` 66(2026-10-12, 9.20) — 는 scoring spec에 entry가 없어요. harness가 돌 때 규칙 하나로 term을 만들어요(규칙은 2026-10-13, 9.21; `harness/tools/harness/scoring.py`의 `with_generated`; 규칙의 문장은 scoring spec의 머리말에 있어요). set의 manifest가 파일마다 placement — 어느 mode의 C1 task 묶음을 어떤 id suffix로 놓았나, 어느 segment에 label이 붙었나, input 창이 있나 — 를 적어두고, 규칙은 placement마다 이렇게 해요.

- 그 mode의 `c1-<mode>` entry의 term을 가져와요. entity의 task id에 suffix `-s<k>`가 붙어요(chain head `game.chain.1`은 `game-s0.chain.1`).
- latency·주기 term은 그 placement에 label이 붙은 segment들로 창을 걸어요(파일 전체면 창 없음). batch term은 창이 없어요.
- label이 붙은 segment가 없는 placement(distractor grid에서 끼어드는 쪽)는 term이 없어요. score는 label이 붙은 상황을 읽고, 끼어든 것의 영향은 그 상황의 term에 나타나요.
- input 창이 없는 placement(4초 이하 segment)는 `channel: input` term만 빼요 — 읽을 keystroke row가 없으니까요. idle placement는 `c1-idle`처럼 term이 없어요.

batch term은 C1 entry의 turnaround 그대로예요. generated 파일의 job은 살아 있어야 하는 구간에 맞춘 크기라, C1 파일에 없던 동료 옆에서 어떤 row에서는 끝나고 어떤 row에서는 못 끝날 수 있어요. 파일 안에서 못 끝난 row는 censored bound(파일 끝 − 등장)로 채점돼요 — 끝난 어떤 값보다도 나쁘고, 그런 row 둘은 비겨요. idle class placement(indexing, backup)는 job이 모든 row에서 같은 시각에 끝나니 no headroom이 기대돼요.

experiment spec은 generated 파일을 이름으로 나열하지 않고, pin한 manifest에서 축으로 골라요 — `files.select`(manifest 하나와 축 조건, 예: `split: measurement`, `form: focus`, `tier: 5`)와 manifest마다 pin 하나(`pins.generated`). 고른 파일은 reporting으로만 들어가요(generated 파일은 전부 보고 재료예요). 파일의 축(pair, form, middle 길이, interval, split, relation, tier, carrier …)은 records column이 아니에요. reporting line이 `workload_id`로 manifest의 record에 join해서 읽어요(`harness/tools/harness/manifests.py`). RQ0 gate spec은 generated 파일을 고르지 않아요.

---

## 16. guard — score와 별개로 항상 확인하는 것

score가 아니라 pass/fail이에요. 모든 보고 숫자 옆에 붙어요. guard 여덟 개의 목록, threshold, 그리고 그 threshold를 왜 그렇게 잡았는지(grounding)는 **guard spec**(`harness/guards/guard-spec.yaml`, 8.3에서 만들었고 2026-10-17부터 version 1.2)이 데이터로 갖고, 코드(`harness/tools/harness/guards.py`)는 guard마다 이름 붙은 함수 하나예요. 결과는 run마다 guard 하나에 row 하나인 `guards` 파일(pass / fail / not_applicable, 잰 값, 적용된 threshold, 짝 run, fail이면 이유)로 나와요. 입력이 없어서 못 잰 guard는 fail이에요(통과시킨 게 아니니까). `not_applicable`은 guard의 범위가 그 run을 애초에 안 보는 경우만이에요(예: `fixed`에는 recognition이 없으니 provenance 비율을 안 봐요).

| guard | 무엇을 재나 | threshold | 왜 |
|---|---|---|---|
| provenance 비율 | `config_interval`의 시간 가중 `fallback` + `held` 비율(aggregates의 fallback share) | 0.5 미만 (design) | fallback/held로 대부분 돌았으면 recognition이 증명한 게 없음. `fixed`는 not_applicable |
| config age | non-boot schedule entry마다, 그 entry가 찍힌 시각이 **그 query의 `t_set_change`를 덮는 ground-truth segment가 끝나기 전**인가 | 숫자 없음, 구조적 검사 | 상황 A를 보고 낸 config가 상황 B가 시작된 뒤에 적용되면, log의 채점(A)과 trace의 결과(B)가 서로 다른 segment 얘기가 돼서 결과를 recognition에 귀속시킬 수 없음. 값으로는 가장 큰 관측 나이(적용 시각 − `t_set_change`)를 기록. metrics doc §8의 `config_age_*` aggregate는 "config가 얼마나 오래 유효했나"(time in force)라서 다른 양이고, 보고만 해요 |
| starvation floor | task별 `ready_wait` max(cause 무관, 파일 전체, idle class task 포함; `fixed`를 포함한 모든 condition) | 30 000 000 µs(30초) 이하 (design) | sched_ext의 watchdog이 최대이자 기본값으로 강제하는 한계(`kernel/sched/ext.c`, v6.17)를 이 연구가 가는 배포 경로의 타당성 한계로 빌려 왔어요. 어떤 task가 이보다 오래 기다린 run은 실제 sched_ext 배포라면 계속 돌 수 없는 configuration을 그린 거예요. executor에는 starvation 안전망이 없어요 |
| determinism | trace 파일의 SHA-256 vs 같은 run을 한 번 더 돌린 trace의 SHA-256 | byte-identical | 같은 입력 두 번 → 같은 trace. 두 번째 실행을 언제 어떻게 만드는지는 runner(8.6)의 일 |
| utilisation sanity | `busy / T_end` | 1.0 이하, 그리고 scoring spec에 term이 있는 파일이면 0 초과 | 물리적으로 말이 되나; 파싱은 됐는데 비어 있는 trace를 잡음 |
| tick count | primitives가 records를 만들면서 낸 consistency 메시지(window 안에서 tail이 끝낸 iteration 수가 head가 소비한 tick 수 이하, keystroke row 수, `deadline` 교차검사, `config_applied`와 schedule의 일치) | 메시지 0개 | records가 trace·run file과 맞나 — head가 보낸 적 없는 wake로 끝난 frame, 빠진 keystroke row 같은 것. chain 검사는 tail이 모자란 것은 잡지 않아서, 중간에 사라진 chain wake는 이 guard로 안 잡혀요 |
| `validation` = `provenance` | recognition log의 `validation` 순서 = config schedule의 `provenance` 순서(boot 제외), 위치별 비교 | 불일치 0개 | log와 schedule이 서로 맞나 |
| C2 pair | C2 pair(P1 `c2-p1a`/`c2-p1b`, P2 `c2-p2a`/`c2-p2b`, P3 `c2-p3a`/`c2-p3b`) 두 run의 config schedule. 정답이 다른 segment의 시작에 걸려 있던 configuration과 그 segment 안에 찍힌 entry 전부를 (algorithm, params, cap)으로 entry마다 비교. 짝은 같은 condition·seed·boot default의 다른 파일 | `oracle`과 recognition 조건(`shipped_catalogue`, `strongest_name_table`, `llm_vocab`, `llm_algo`, `llm_full`)에서 두 sequence가 같으면 fail. `fixed`와 `random`은 not_applicable. trace는 비교하지 않고, `fixed`에서 두 파일이 같아야 한다는 요구도 없어요 | 두 sequence가 같으면 recognizer의 답이 wanted/unwanted 사이에서 한 번도 안 바뀌었다는 뜻이라, gap 0을 recognition 결과로 읽으면 안 됨(table이나 recognizer의 결함). trace는 pair마다 background job이 다른 측정된 프로그램이라 configuration과 상관없이 달라서 비교할 의미가 없어요. `oracle`에서는 설계상 다르니 plumbing 확인이에요 |

`c6-dual` 같은 파일은 guard 예외를 미리 RQ0 gate spec에 데이터로 적어요(`ground_truth`가 `ambiguous`라 oracle이 legal한 답을 낼 수 없어서 fallback 100%가 정상). 예외는 실험별 데이터고 guard spec에는 없어요.

---

## 17. Layer 1 — recognition log를 채점하는 grader

8장에서 recognition log의 entry 하나가 어떤 row가 되는지 봤어요. 그 row들을 실제로 만들고, 파일들을 모아 숫자 하나로 만드는 것이 **grader**(`harness/tools/harness/grader.py`, 8.4)예요. simulator는 전혀 안 끼어요. 입력은 recognition log와 compiled workload의 `ground_truth`, 그리고 driver table이에요(driver table은 "이 답이 어떤 config가 됐나"를 알기 위해서예요 — algorithm 선택의 정답은 label이 아니라 label을 table에 넣었을 때 나오는 algorithm이니까요).

### 17.1 어떤 query가 채점되나

log의 entry마다 `t_set_change`가 있어요. 그 순간을 덮는 `ground_truth` segment가 있고 그 segment가 `ambiguous`가 아닐 때만 채점해요. 그래서 마지막 snapshot(파일이 끝나는 순간의 것)과 `c6-dual`의 ambiguous segment는 빠져요. core set 전체로는 query point 147개 중 51개가 terminal, 19개가 ambiguous라 **77개**가 채점되고(50개 파일), 그중 9개가 `pre_committed_miss` segment 위에 있어서 headline은 68개(44개 파일)예요. 이 수는 mock daemon으로 재현되고 test가 pin해요(`harness/tools/tests/test_mock_daemon.py`; core set 전체를 읽는 test라 CI의 `make test`가 아니라 집에서 `make -C harness test-full`로 돌아요).

row마다 `validation`(daemon이 그 답을 어떻게 처리했나), segment의 `familiarity`(있으면), `pre_committed_miss`가 붙어요. `pre_committed_miss`는 "이름과 행동만으로는 맞출 수 없다고 미리 약속한 segment"라는 표시예요. headline accuracy는 그 segment를 **빼고** 계산하고, 안 뺀 값을 옆에 같이 보고해요(exclusion accuracy line). 어느 쪽이 headline인지는 미리 정해져 있어요.

### 17.2 어떤 통계인가 — 축마다 하나씩, 정해져 있음

축은 셋이에요: `background_wanted`(binary), mode(16개), algorithm 선택(4개). 어느 축에 어느 통계를 쓰는지는 metrics doc이 정하고 설정할 수 없어요.

| 축 | headline | 옆에 같이 |
|---|---|---|
| attribute (binary) | **balanced accuracy** (두 class의 recall 평균) | Matthews correlation coefficient, confusion matrix |
| mode | **raw accuracy** | 측정된 majority baseline("제일 흔한 답만 하면 몇 점인가"), class별 recall, confusion matrix |
| algorithm choice | raw accuracy | 같음 |

macro-average는 어디에도 없어요. binary 축에 balanced accuracy를 쓰는 이유는 `true`가 훨씬 많아서 "다 true"라고 답해도 raw accuracy가 높게 나오기 때문이에요. 다중 class 축에서 raw accuracy 옆에 majority baseline을 놓는 것도 같은 이유예요.

### 17.3 seed는 평균, 파일은 cluster

`random`은 seed마다 한 번씩 돌아요. seed는 "같은 질문을 다시 던진 것"이지 새 질문이 아니라서, 채점 row를 seed끼리 **합치지(pool) 않고 평균**해요. 합치면 관측 수가 seed 수만큼 부풀어서 평균이 실제보다 많은 증거처럼 읽혀요. grades 파일의 `over_seeds` column이 그 구분이에요(0이면 seed 하나의 값, 1이면 seed 평균).

신뢰구간은 **파일을 단위로 하는 cluster bootstrap**이에요. 같은 파일 안의 query들은 독립이 아니니까(같은 process 집합, 같은 저자) 파일 단위로 다시 뽑아요. seed와 반복 횟수는 metrics doc에 고정돼 있어요. condition끼리의 비교는 같은 bootstrap draw 위에서 **paired**로 해요.

솔직한 한계: 독립 단위가 44개(headline)에서 50개(채점 전체) 파일이라 Layer 1은 두 name table condition(`shipped_catalogue`, `strongest_name_table`)과의 비교에 힘이 부족해요. familiarity tier별 비교는 tier 4·5에 채점 query가 하나씩뿐이라 아예 집계하지 않고 row에 tier만 실어요. 이건 8.4 spec이 인정하고 적은 사실이에요.

### 17.4 출력

`grades` 파일(`harness/grades/schema/`): row의 identity는 condition·table·seed·telemetry이고 workload는 **없어요** — Layer 1 숫자는 파일을 가로질러 모은 것이니까요. `level`이 row의 종류예요: `statistic`(축 하나의 통계), `class_recall`, `confusion`(cell 하나), `paired`(다른 condition과의 차이). 명령은 `tools/grade.py`이고, 채점 중 "oracle이 채점 query에서 만점이 아니다"라는 consistency 메시지가 나오면 exit 2예요 — 그건 결과가 아니라 bug예요.

---

## 18. mock daemon과 mock simulator — invocation contract의 첫 구현

harness는 daemon과 simulator를 **프로세스로 실행**해요. 그래서 "어떤 명령으로 실행하는가"가 계약이어야 해요. 그 계약이 **invocation contract**(data-contracts 문서의 contract 10, 8.5)예요. 규칙의 뼈대는 넷: 입력은 전부 이름 있는 flag(`--workload`, `--schedule`, …)로, 출력은 flag로 받은 경로에 쓰고, 성공 여부는 exit code로, 그 외의 채널(stdout, 환경변수, 현재 디렉토리)은 없음. 그리고 계약의 유일한 행동 규칙: **같은 입력으로 두 번 실행하면 출력이 byte 단위로 같아야** 해요. runner가 매 실행을 두 번 돌려 그걸 확인해요(20.2).

```
daemon:    --workload W.json --condition C --telemetry focus|names --driver-table T.yaml
           --boot-default B.json --out-schedule S.json --out-log L.json [--seed N]
simulator: --workload W.json --schedule S.json --out-trace TRACE.jsonl
```

`C`는 daemon guide의 condition 이름 하나예요(mock daemon은 `fixed`·`oracle`·`random`만). `--telemetry`는 recognizer에게 보여줄 telemetry 모양이에요(2026-10-11부터 필수). 그래서 run 하나는 workload 하나 × condition 하나 × telemetry 모양 하나(× draw하는 condition이면 seed 하나)예요.

실제 프로그램이 오기 전에 이 계약을 지키는 두 대역(`harness/tools/tests/mocks/`)이 있어요. 둘 다 test tree에 있고, Phase 10에서 runner의 machine 설정이 실제 프로그램을 가리키게 바뀌어요.

**mock daemon**은 `fixed`·`oracle`·`random`에 대해 **충실**해요. workload에서 visible projection(daemon이 실제로 보게 될 것: task마다 process 이름, `declared_class`, focus 구간)을 뽑고, 여섯 가지 telemetry 규칙으로 query point를 찾고(여섯 번째가 focus를 가진 process의 이름도 집합에 넣는 규칙이라 focus 이동도 query point예요), `oracle`이면 ground truth를, `random`이면 seed된 균등 draw로 table의 row 하나를, `fixed`면 아무것도 답하지 않고, contract에 맞는 schedule과 log를 써요. validator가 없어서 `unmodified`만 내고, `held`·`clamped`·LLM 경로는 없어요. oracle의 답이 정의되지 않는 곳(ambiguous segment, terminal snapshot)에서는 query가 `fallback`을 달고 schedule entry가 boot default를 반복해요 — `c6-dual`의 fallback 100%가 여기서 나와요.

**mock simulator**는 두 가지예요. **generator**는 어떤 workload와 schedule에도 contract에 맞는 trace를 내지만, **scheduling을 전혀 모델하지 않아요**: 자극이 올 때마다 그 task가 ready가 되고 정확히 1 µs 돌고 끝나요. 첫 명령이 `WAIT`인 task(`LOOP`으로 시작하면 그 몸통의 첫 명령; `FORK`로 만든 자식 포함)는 예외예요. 그 `WAIT`에 쓸 wake가 등장 전에 와 있지 않으면 reference simulator처럼 등장하는 step에서 block되니(10.3), 등장은 자극이 아니고 `ready` line도 run도 없어요. 처음 도는 건 그 `WAIT`을 완료하는 wake에서예요. generator는 pinned wake와 tick과 chain stage 사이의 wake만 자극으로 내고 다른 task의 `WAKE` 명령은 모델하지 않아서, 형제의 `WAKE`로만 깨워지는 task(`c1-compile`의 job member 같은)는 mock에서 한 번도 돌지 않고 끝나지도 않아요. 그래서 core set 51개 파일 전부가 pipeline을 통과하지만, `fixed`·`oracle`·`random`의 점수가 같고, 모든 judging 파일이 no headroom으로 나와요. 이건 queue를 모델하지 않는 simulator의 **정상 결과**이지 결함이 아니에요. **replay**는 손으로 쓴 fixture trace를 그대로 복사해요 — 10–12장에서 손으로 계산한 값이 runner의 같은 경로로 흘러가게 하려고요.

두 mock이 있어서 harness의 위쪽 절반 전체가 실제 프로그램 없이 test돼요. 전체 smoke(`make -C harness smoke`: scoring spec에 entry가 있는 core 파일 49개 전부를 mock으로)는 다시 지은 dataset 위에서 집 기계로 약 4시간 50분이 걸려서 요청할 때만 돌아요(`.github/workflows/harness-smoke.yml`). 대신 push마다 CI의 `make test`가 같은 smoke 경로를 파일 한 개에서 세 개까지로 돌려요(`harness/tools/tests/test_runner.py`). smoke의 판정은 만들 때부터 `invalid`예요 — smoke spec에는 guard 예외가 없어서 `c6-dual`의 `oracle` run이 fallback만으로 돌아 provenance guard에 걸리니까요. smoke는 판정이 아니라 배관을 확인해요. 인경민의 simulator와 박이안의 daemon이 오면 runner의 machine 설정(명령 prefix와 version 문자열)만 바뀌고 나머지는 그대로예요 — 두 프로그램이 invocation contract대로 실행되면요. simulator 쪽은 그게 RQ0 gate spec의 simulator-conformance 항목 (h)예요(19.1). 지금의 reference simulator는 workload와 config schedule을 위치 인자로 받고 trace를 stdout에 써요.

---

## 19. per-experiment spec과 RQ0 gate evaluator — 판정을 데이터로

Phase 8 전체를 관통하는 원칙 하나: **evaluator가 적용하는 판단은 전부 committed 파일 안의 데이터이고, 코드 안의 상수가 아니다.** 그래야 숫자를 본 뒤에 판정 기준을 슬쩍 바꾸는 일이 git에 남지 않고는 불가능해져요. 그 파일이 **per-experiment spec**이고, RQ0의 것이 **RQ0 gate spec**(`harness/experiments/rq0-gate.yaml`, 2026-09-12 commit, 2026-10-09에 다시 지은 dataset 위에서 다시 씀, 9.14)이에요.

### 19.1 spec에 무엇이 있나

- **generic part** — 어떤 실험에나 필요한 것: condition 목록, telemetry 모양 목록(RQ0는 `focus` 하나), seed 수 N, boot default(primary와 alternatives), judging 파일·reporting 파일·sensitivity line이 읽는 variant 파일(그리고 generated set에서 축으로 고른 파일, 15.5), `pre_committed_miss`에서 **유도된** Layer-1 exclusion(lint가 실제 annotation과 맞는지 확인해요 — 손으로 고를 수 없어요), guard 예외(이유 필수), typed reporting line, 그리고 **pin** — scoring spec·guard spec(version 1.2)·driver table·dataset manifest·variants manifest의 SHA-256(generated 파일을 고르는 spec이면 그 manifest마다 하나 더).
- **statements** — 숫자의 근거를 적은 글. evaluator가 보고서에 그대로 옮겨 적어요. RQ0 gate spec에는 열다섯 개가 있어요: 판정 set의 규칙, idle class 파일 여섯이 보고만 하는 이유, executor 가정(인경민의 2026-10-01 simulator 상태 memo와 9.11 결정 위에 둔 committed assumption. 그중 두 가지에 대한 인경민의 정식 답은 2026-10-08 memo로 요청), simulator conformance(RQ0 run 전에 simulator가 hand fixture에서 보여야 할 아홉 항목 (a)–(i). (h)는 2026-10-17에 더해진 것으로, simulator가 runner가 부르는 대로 invocation contract에 따라 실행되는 것 — workload와 config schedule을 `--workload`·`--schedule`로, trace 경로를 `--out-trace`로 받고 trace를 그 파일에 쓰는 것(18장). (i)는 2026-10-21에 더해진 것으로, spawn table의 자식을 가리키는 WAKE가 그 자식에게 닿고, 자식이 태어나기 전에 온 wake는 보관했다가 태어날 때 넘기는 것. reference simulator는 (a)–(f)와 (i)를 하고, (g)와 (h)가 남아 있어요), g·K·N의 근거, random condition의 정의, prior table의 중복 구조, boot-default sweep의 설계, sensitivity line들, 다시 측정할 조건, Layer-1 구간의 caveat, 실패 절차, held-out-rows 사전등록.
- **criterion** — 실험별 판정 규칙. RQ0는 `k_of_n_gap`: judging 파일 19개 중 **K = 10개 이상**이 gap **g = 0.5 이상**이면 pass.

### 19.2 gap 하나 손으로

파일 하나의 gap은 "oracle의 headroom 중 random이 못 가져간 몫"이에요.

```
gap = 1 − mean_seeds(score_random) / score_oracle
```

`score_oracle`은 그 파일의 weight 합이에요(oracle의 share는 term마다 1이니까). `mock-experiment` fixture의 숫자로: weight 합 2.5, random의 파일 점수가 seed 1에서 1.639359, seed 2에서 0.433333 → 평균 1.036346 → gap = 1 − 1.036346 / 2.5 = **0.585462**. g = 0.5보다 크니 이 파일은 "met". seed별 값은 전부 보고서에 평균 옆에 찍혀요.

no headroom 규칙 둘. term 하나가 no headroom이면(oracle 자신의 개선이 floor 아래) 그 term은 random이 다 가져간 것처럼 share 1로 들어가요 — 이건 scorer의 research-wide 규칙이에요. judging 파일의 **모든** term이 no headroom이면 그 파일은 set에 남되 "g를 못 넘긴 것"으로 세요 — 이건 RQ0 gate spec의 규칙이에요.

### 19.3 verdict는 셋

pass, fail, 그리고 **invalid**. criterion이 읽는 run(judging 파일의 `fixed`·`oracle`·`random`)에서 예외 처리되지 않은 guard가 하나라도 fail이면 verdict는 pass/fail 대신 invalid이고 어느 guard가 어느 run에서 걸렸는지를 이름으로 적어요. gap row는 그래도 다 계산해서 보여줘요. pin이 안 맞거나 run set이 불완전하면(어떤 파일의 random seed가 N개가 아니면) verdict가 아니라 **거부**(GateError)예요 — 아무것도 안 써요.

### 19.4 reporting line — 판정을 흔들어 보기

verdict는 primary boot default에서 한 번만 계산해요. 그 판정이 우연한 선택에 기대고 있지 않다는 걸 보이려고 미리 등록한 line들이 있어요.

| line | 무엇을 다시 세나 | 비용 |
|---|---|---|
| `sensitivity` | boot default를 sweep의 10개 지점(top slice 0.5, 0.7, 0.9, 1.2, 2, 3, 5, 14, 20, 100 ms)으로 바꿔 `fixed`를 다시 돌리고, gap을 다시 계산한 뒤 통과 개수. 지점마다 이유가 spec에 적혀 있어요(config schema의 두 경계와 배포된 scheduler들의 기본값, 그리고 judging 파일의 주기 task가 갖는 계단 — chain의 frame당 여유, stage의 demotion 경계, video player의 cycle 범위, call의 demotion 경계 — 양쪽) | `fixed` run 10개 × listed 파일 51개 |
| `floor_band` | latency floor를 0.5 / 1 / 2 / 5 ms로 바꿔 채점을 다시 하고 통과 개수 | 재채점만 |
| `g_band` | g를 0.25 / 0.33 / 0.5 / 0.67로 바꿔 통과 개수 | 재계산만 |
| `seed_standard_error` | 파일마다 random 점수의 seed 평균의 표준오차 — N이 산 정밀도 | 계산만 |
| `exclusion_accuracy`, `layer1_headline` | grades 파일에서 | — |
| `random_beats_oracle` | random 평균이 oracle을 넘은 파일 표시 | — |
| `note` | 파일 하나에 묶인 미리 쓴 문장(`c7-gaming`, `c7-meeting`의 읽는 법, `c1-gaming`의 별도 line, `c7-media`, `c7-mail`이 보고만 하는 이유) | — |
| `variant_set` (8개) | 다시 지은 judging 파일 묶음을 primary boot default로 돌려 통과 개수를 다시 세요. variant 파일은 판정에 안 들어가요. `venue-x0.8`·`venue-x1.25`(19개 파일): 측정된 `RUN`을 chain 빼고 전부 1/1.25배·1.25배. 측정된 두 venue 효과 — training run의 huge page 비율 ×1.144와 tracing overhead ×1.02–1.16 — 를 담는 design bracket이고, 다른 CPU model은 담지 않아요. 다른 CPU는 프로그램마다 제 배율로 속도를 바꾸는데(Xeon Platinum 8573C는 EPYC 7763 대비 `cc1`을 0.72배, `fixdep`을 0.50배 시간에 돌렸어요) 공통 배율 하나로는 그걸 재현할 수 없어요. `chain-x1.2`·`chain-x1.4`(3개): 게임 chain의 `RUN`만 1.2배·1.4배. `seg1-30s`·`seg1-120s`(C2 4개): 첫 segment 60초를 30초·120초로. `corner-low`·`corner-high`(11개): 안정성 규칙의 예외로 실어 온 값들을 구간의 아래·위 끝으로 | variant 파일 78개(`trace_replay`의 4개 포함) × (`fixed` 1 + `oracle` 1 + `random` 100) |
| `trace_replay` | judging 파일 넷(`c7-dev`, `c7-browsing`, `c7-meeting`, `c2-p1a`)을 compile된 stream 대신 측정된 repeat 하나의 stream으로 다시 지어 돌려요. stream의 종류는 entry를 따라 셋이에요: wake 순서(`wakes`: `code-editor`, `web-browser`, `renderer-hidden`), run과 그 뒤의 block(`runs`: `package-upgrade`, `cpu-batch`의 `python3`), cycle(`cycles`: `video-call`). 네 파일 모두 batch job의 run을 측정된 것으로 바꿔요(`c7-dev`·`c7-browsing`·`c7-meeting`은 upgrade, `c2-p1a`는 `python3`), `c7-meeting`은 통화의 cycle도요. 두 build에서 gap이 g의 같은 쪽에 있고 그 차이가 g band의 간격보다 작으면 일치 | 그 78개에 포함 |
| `input_wake_count` | judging 파일의 interaction latency term마다 P99가 기대는 keystroke 수(26초짜리 counterpart는 약 100개, `c3-workday`의 browser는 7개라 P99가 상위 한두 개의 대기예요) | 계산만 |
| `longest_wait` | run마다 가장 긴 `ready_wait`를 30초 floor와 비교. 15초를 넘은 run이 하나라도 있으면 판정을 읽기 전에 executor의 안전망 문제를 인경민과 다시 열어요 | 계산만 |
| `bounding_pair` | `c2-p2a`(download를 측정된 그대로 full standing으로)와 `c2-p2a-idle`(같은 download를 idle class로)의 판정을 각각 보고하고 그 차이를 적어요. 실제 desktop은 nice 10인 download를 그 사이에서 다뤄요 | 계산만 |
| `flip_cost` | (RQ0 gate spec은 안 씀) recognizing run마다 configuration이 바뀐 횟수(`change_count`), 그중 config-incorrect로 채점된 query의 것(`wrong_change_count`), 그 틀린 MLFQ 전환들의 per-switch excess 합(`wrong_switch_excess_sum`)을 파일 점수 옆에 찍어요. hold-time plan의 no-rule measurement(그 plan의 step 1) — hold time도 hysteresis도 없이 flip이 얼마나 일어나고 얼마나 비싼지 재는 일 — 이 읽는 line이에요 | 계산만 |

개수가 band나 sweep, variant 축 안에서 움직이면 결과를 점이 아니라 **범위**로 보고해요. 이게 "왜 0.5인가"에 대한 방어예요: 숫자 자체보다, 그 숫자를 바꿔도 결론이 안 바뀐다는 걸 보이는 것.

### 19.5 report

실험 run 하나당 machine-readable 보고서 하나(`report.json`, schema `harness/experiments/schema/report.schema.json`)가 진실이고, `report.md`는 거기서 렌더링만 한 것이라 손으로 고치지 않아요. 논문 표는 JSON에서 나와요. 안에는 verdict와 그 근거, 파일별 gap과 seed별 점수, 채점된 run 전부, run마다 provenance 비율(unmodified / clamped / held / fallback), guard 결과 전부, statements, line들이 있어요.

---

## 20. runner와 execution cache — 13 668 run을 돌리는 법

**runner**(`harness/tools/harness/runner.py`, `tools/run.py`, 8.6)는 spec의 generic part를 **run matrix**로 펼치고, run마다 daemon과 simulator를 invocation contract로 실행하고, 위의 모든 단계를 순서대로 돌려 보고서까지 써요.

### 20.1 matrix

listed 파일(judging + reporting) 하나마다: `fixed`를 primary boot default로 한 번, alternative마다 한 번씩; 다른 condition은 primary로; draw하는 condition(`random`)은 seed 1..N마다 한 번. variant 파일은 primary boot default로만 돌아요(`fixed` 한 번, 나머지 condition은 위와 같이). 그리고 이 전부를 spec의 `telemetry` 목록에 있는 모양마다 한 벌씩 돌려요. RQ0 gate spec은 `focus` 하나라 한 벌이에요. RQ0 gate spec으로는 51 × (1 + 10 + 1 + 100) + 78 × (1 + 1 + 100) = **13 668 run**이에요(`fixed` 639, `oracle` 129, `random` 12 900).

### 20.2 두 번 실행, byte 일치

run마다 daemon도 simulator도 **두 번** 실행해요. determinism guard가 rerun trace를 요구하기도 하고, contract의 행동 규칙("같은 입력 → 같은 출력")을 runner가 직접 확인하기도 해서예요. 두 실행의 출력이 다르면 그 run은 실패이고, 실패한 run은 출력이 없는 채로 남고 runner는 채점 전에 멈춰요(`failures.json`에 이름). trace는 압축 없이 요청해요 — gzip header에 timestamp가 있어서 `.gz`는 byte 단위로 안정적일 수 없거든요.

### 20.3 cache

모든 실행은 key로 cache돼요: 프로그램의 version 문자열, 명령 prefix, condition과 seed, telemetry 모양, 입력 파일들의 hash. 같은 key는 다시 실행하지 않고 두 실행의 출력과 stderr를 그대로 꺼내요. 실패한 실행은 cache되지 않아요. 그래서 spec의 파일 하나를 바꾸면 그 파일의 run만 다시 돌고, 프로그램 version이 바뀌면 전부 다시 돌아요 — 정확히 그래야 하는 만큼만이에요. 참고로 key에 seed가 들어 있어서, 두 seed가 같은 row를 뽑아 schedule이 같아도 simulator는 따로 돌아요.

### 20.4 machine 설정과 layout

실험 모양(어떤 파일, 어떤 condition)은 spec에 있고, **이 기계에서 어떻게 돌리나**(명령 prefix, version, build 경로, runs·cache 디렉토리)는 uncommitted `runner.yaml`에 있어요. committed 예시 `runner.example.yaml`은 mock 둘을 가리켜요. 출력은 `runs/<experiment>/<workload>/<run>/`에 run별로 놓이고, run의 이름은 `<condition>[-seed][+boot]~<shape>`예요(예: `random-5~focus`, `fixed+ostep-slice-2000us~focus`). `aggregates.csv`·`scores.csv`·`guards.csv`·`grades.csv`·`report.json`·`report.md`는 experiment 수준에 놓여요. `make -C harness smoke`는 scoring spec에 entry가 있는 core 파일 49개로 throwaway spec을 만들어 이 경로 전체를 mock으로 돌려요. 다시 지은 dataset 위에서 집 기계로 약 4시간 50분이라 요청할 때만 돌고(`harness-smoke.yml`), push마다 도는 `make test`는 같은 경로를 파일 한 개에서 세 개까지로 돌려요(18장).

---

## 21. harness tree — 지금 모습

Phase 5 때의 tree 그림은 오래됐어요. 지금은 폴더마다 README가 있고, 그 README가 "무엇을 위한 폴더인지, 파일이 어떻게 만들어지고 읽히는지, 어떻게 돌리는지"를 설명해요. 이 문서에서 다룬 장과 폴더의 대응은 이래요.

| 폴더 | 이 문서의 장 | README |
|---|---|---|
| `harness/records/` | 5, 6, 7, 10–12 | `harness/records/README.md` |
| `harness/aggregates/`, `harness/scores/`, `harness/scoring/` | 14, 15 | 각 폴더의 README |
| `harness/guards/` | 16 | `harness/guards/README.md` |
| `harness/grades/` | 8, 17 | `harness/grades/README.md` |
| `harness/tools/tests/mocks/` | 18 | `harness/tools/tests/mocks/README.md` |
| `harness/experiments/`, `harness/boot-defaults/` | 19 | 각 폴더의 README |
| `harness/tools/harness/runner.py` | 20 | `harness/tools/harness/README.md` |

시작점은 `harness/README.md`예요. 원칙은 그대로예요: machine이 읽는 것(schema, spec, fixture)은 code 옆에, 사람이 읽는 것(metrics doc, 이 문서)은 `docs/harness/`에. 규범 정의는 언제나 metrics doc이고, 판정 규칙은 언제나 RQ0 gate spec이에요.

---

## 22. 용어 정리

| term | 뜻 |
|---|---|
| **lane** | CPU. 이 프로젝트에서는 하나 |
| **task** | 프로그램 하나. run file의 `arrive` event 하나, 또는 그 task가 `FORK`로 만든 spawn table의 entry 하나 |
| **runnable / ready** | 일하고 싶은데 lane이 비길 기다리는 상태 |
| **blocked** | 일할 게 없어 기다리는 상태 (`WAIT`, `SLEEP`, `TIMER`, fork slot) |
| **occupancy interval** | `run_start`부터 `run_end`까지. task가 lane을 잡고 있던 구간 |
| **preempt** | scheduler가 running task를 강제로 내리는 것 |
| **tick** | `TIMER`의 주기적 알람. t₀ + k·period, t₀는 task가 첫 TIMER를 실행한 시각(= 등장 시각) |
| **job** | tick 하나에 대응하는 주기 작업 하나 (frame 하나) |
| **skip (TIMER)** | TIMER에 도달했을 때 이미 지난 tick이 여럿이면 가장 최근 것 하나만 바로 소비하고 그 앞의 소비 안 된 tick은 건너뛰는 것. 건너뛴 tick마다 `skipped=1`인 `job` row(값 없음, miss). harness가 읽는 규칙이고, reference simulator도 2026-10-23부터(stage Y) 이 규칙을 돌려요 |
| **chain** | TIMER를 가진 head에서 WAKE를 따라 이어지는 task들. 게임의 frame pipeline |
| **head / tail** | chain의 첫 task(TIMER 있음) / 마지막 task |
| **exogenous / endogenous** | scheduler가 바꿀 수 없는 시각(keystroke, 등장, depart) / scheduler에 달린 시각(spawn, exit, 모든 실행 시각) |
| **`T_end`** | observation window의 끝. run file에서 가장 늦은 pinned 시각(등장, depart, wake event). core set에서는 마지막 segment의 `t_end`와 같아요 |
| **primitive** | trace(또는 recognition log)에서 나오는 raw observation. records의 row |
| **aggregate** | primitive row들을 합친 통계 (P95, miss rate, …). records에 저장하지 않음 |
| **scoring** | aggregate에 파일별 weight를 곱하고 normalise해서 score를 만드는 것. Phase 6/7 |
| **records** | trace 하나당 CSV 하나. long format |
| **entity** | row가 누구 얘기인지. task id, 또는 예약 이름 `lane`/`schedule`/`recognizer` |
| **long format** | 한 row = 측정 한 번. metric 이름이 cell 값으로 들어감 |
| **provenance** | 적용된 config가 어디서 왔나: `unmodified`/`clamped`/`held`/`fallback` |
| **query point** | telemetry 집합(process 이름 → 개수, 그리고 focus를 가진 process의 이름)이 바뀐 순간. recognizer가 호출되는 시점 |
| **`t_set_change`** | query point의 시각 |
| **Layer 1 / Layer 2** | recognition accuracy / consumer performance |
| **normalisation** | `(fixed − condition)/(fixed − oracle)`. headroom의 몇 %를 가져갔나 |
| **floor** | normalisation의 분모가 이보다 작으면 "no headroom" |
| **guard** | score와 별개의 pass/fail 검사 |
| **mock** | 손으로 쓴 run file + trace + expected records. 정의를 시험하고 code를 test함 |
| **condition** | 어떤 recognizer로 돌렸나: `fixed`, `random`, `shipped_catalogue`, `strongest_name_table`, `llm_vocab`, `llm_algo`, `llm_full`, `oracle` |
| **driver table** | `(mode, background_wanted)` → scheduler config의 lookup. prior와 calibrated 두 벌 |

---

## 이 문서를 다 읽었으면

- `_dev/docs/spec/jioh/phase-5-primitive-metrics-and-records.md`의 locked decision 17개가 전부 읽혀야 해요. 안 읽히는 항목이 있으면 이 문서의 구멍이에요.
- `_dev/archive/2026-09-07-phase-5-primitive-metrics.md`에 각 결정의 이유와 기각된 대안이 있어요.
- dataset 쪽은 `docs/workload/coreset-guide.md`.
- trace format의 규범적 정의는 `docs/data-contracts.md`의 trace 절.
