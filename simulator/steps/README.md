# notes — 시뮬레이터를 한 단계씩 다시 짓기

`src/sim.cpp` 를 답안지로 봉인하고, 계약 문서에서 직접 다시 만든 사다리.
각 파일은 **컴파일·실행되는 완전한 프로그램**이고, 앞 단계에 20~40줄을 얹는다.
앞 단계를 고쳐야 하면 고치고, **무엇을 왜 고쳤는지** 를 그 파일 머리에 적는다.

```
make            # 전부 빌드
make lines      # 단계별 코드 줄수
```

산문은 여기 한 곳에만 둔다. 각 `.cpp` 의 머리 주석은 5~10줄로 제한한다.

---

## 사다리

| 단계 | 얹는 것 | 줄수(델타) | 검증 |
|---|---|---|---|
| **a** | 가상 시계 + 이벤트 큐. 태스크 없음 | 37 | 삽입 순서를 바꿔도 pop 순서 동일 |
| **b** | `Instr`/`Task`/`step()` + Arrive. 아직 아무도 안 뛴다 | 80 (+43) | 도착·즉시종료가 찍힌다 |
| **c** | 레인: `dispatch()` + Lane 이벤트 (비선점) | 104 (+24) | 두 태스크가 순서대로 완주 |
| **d** | WAIT + 외생 wake | 118 (+14) | 블록/해제 |
| **e** | depart | 127 (+9) | **guide §4½ 표와 한 줄씩 일치** |
| **f** | 타임슬라이스 + 선점 + `gen` | 153 (+26) | **§4½ punchline** / `--no-gen` 양성 대조 |
| **g** | `Policy` 인터페이스 **추출** + Fifo/Rr | 189 (+36) | `sim_g fifo` 출력 == `sim_e` |
| **h** | `Trace`/`Clock` 이음매 + MLFQ 규칙 1~4 | 244 (+55) | **guide §5 강등 시나리오** |
| **i** | MLFQ 규칙 5 (boost): `Clock::arm` + `tag` | 284 (+40) | boost 가 터지고 전원 Q0 |
| **j** | SLEEP | 289 (+5) | 해제 경로를 wake 와 공유 |
| **k** | TIMER + backlog | 304 (+15) | 격자가 부하에 안 밀린다 |
| **l** | LOOP 평탄화 | 323 (+19) | unbounded 의 종료자는 depart |
| **m** | 채널 + WAKE (+ 우편함) | 374 (+51) | WAKE 브리게이드가 풀린다 |
| **n** | FORK / spawn_table / fork_cap | 447 (+73) | MLFQ vs FIFO 창발 시각이 갈린다 |
| **o** | JSONL trace 7종 (data-contracts §9) | 478 (+31) | harness 가 읽는 형식 |
| **p** | `deadline` 이벤트 | 494 (+16) | due 가 격자 시각 기준 |
| **q** | JSON 파서(별도 헤더) + 워크로드 로더 | 531 (+37) | 진짜 coreset 파일이 돈다 |
| **r** | config schedule + 정책 교체 + `handoff()` | 603 (+72) | MLFQ→FIFO→MLFQ 인계 |
| **s** | EDF + LOTTERY + `TaskView` 이음매(B1/B2 부류) + 정책 타이머 epoch | 769 (+167) | EDF 마감 100% vs MLFQ 0% (`edfheavy`) / LOTTERY batch 몫 0.15→14.8%, 0.5→49.1% |
| **t** | 자식 trace id = 파일의 `spawn_table` id (q 의 버그 수정) | 773 (+1) | coreset 24파일 중 자식 없는 20개는 sim_s 와 바이트 동일. 자식 있는 4개(c1-compile, c3-workday, c4-compile, c6-dual)는 `task`/`parent` 문자열 말고 diff 0, spawn 된 id 전부가 파일 테이블에 있다 |
| **u** | 교체 의미론: MLFQ cold start(U1) / 같은 알고리즘 엔트리는 홀더 불간섭·큐 순서 유지(U2) / drain(U3) | 801 (+28) | harness `mock-switch` 손 유도 trace 의 `config_applied` 4개 시각 일치(t 는 2번이 10600, 기대 12000). 스케줄 없음·boot 1엔트리 48/48 sim_t 와 바이트 동일. 9엔트리 4알고리즘 스케줄: u 24/24 종료·재현·index 전부 순서대로, t 는 23/24 assert 로 죽는다 |

큰 델타 넷(h, n, r, s)은 쪼갤 수 없는 단위다 — MLFQ 다섯 규칙, FORK 의 생애주기, 두 번째 입력,
그리고 **부류**: EDF 와 LOTTERY 는 같은 실행기 부류(B2 주기 / B1 batch)를 읽으므로 따로 얹으면
이음매를 두 번 설계하게 된다.

### 나중 단계가 앞 단계를 고친 곳

| 고친 것 | 왜 그때 몰랐나 |
|---|---|
| `Event.gen` (a→f) | 취소가 필요해지는 건 **선점이 생긴 다음**이다 |
| `Event.tag` (a→i) | 정책이 자기 타이머를 걸어야 하는 건 **규칙 5** 때문이다 |
| `on_lane` 검사 1항→2항 (c→f) | "레인을 놨다가 다시 잡는" 경우가 e 까지는 없었다 |
| ready set 이 코어→정책 (c→g) | MLFQ 의 ready set 은 "큐 여러 개"다. 구조 자체가 정책이다 |
| `vector<Task>`→`deque` (b→n) | FORK 가 실행 중 tasks_ 를 키운다. vector 면 `Task&` 가 댕글링 |
| D1 tie-break 개정 (a→r) | boot 설정이 같은 t=0 의 arrive 보다 먼저여야 한다 |
| `Mlfq::start` 가 `cold` 를 쓴다 (r/s→u) | s 가 `cold` 를 만들 때 MLFQ 만 "R 의 행동 그대로" 남겼다. MLFQ→X→MLFQ 를 손으로 따라가 본 trace(mock-switch)와 맞춰 보기 전에는 옛 레벨이 되살아나는 게 안 보인다 |
| 같은 알고리즘 엔트리가 홀더를 재무장 (r→u) | r 의 교체 경로가 "알고리즘이 바뀐다"만 상정했다. 슬라이스를 줄이는 엔트리 + 슬라이스 중간의 홀더 → 음수 지평선 → `assert(e.t >= now_)`. mock-switch 는 그 순간 레인이 비어 있어 못 밟는다 |
| 교체 즉시 적용 → drain (r→u) | r 은 `t_us` 에 바로 바꿨다. metrics §11.8 이 정하기(09-09) 전 설계라 drain 이 없었다 |
| 자식 sid 를 파일 id 로 (o/q→t) | o 가 손 시나리오에서 sid 를 `부모.N` 으로 지었고, q 의 로더가 테이블 엔트리의 `id` 를 읽지 않아 그 규칙이 남았다. q 의 검증 "진짜 coreset 이 돈다"는 **돌기만 하면** 통과한다 — harness `reader.py` 는 `build.c1` 으로 알고 trace 는 `build.1` 이었다 |
| 선점 복귀의 `ready` 제거 (f→g) | 계약의 `ready.cause` 에 preempt 가 없다 |
| `PolicyTimer` 에 config epoch (i/r→s) | 정책 타이머가 config 적용을 넘어 살아남았다. MLFQ 가 다시 `start()` 할 때마다 boost 사슬이 하나씩 늘고, 사슬끼리 서로를 `q_` 에 남겨 `arm()` 의 종료 규칙을 무력화한다. **c1-compile × mock-switch 가 sim_r 에서 끝나지 않는다** (15초에 가상 45시간, 2,400만 줄). r 의 검증은 이 조합을 돌리지 않았다 |
| `Policy::start(params, cold)` (g→s) | "알고리즘이 바뀌었나"를 정책이 알아야 하는 건 **같은 알고리즘 엔트리는 슬라이스 유지, 교체는 새 dispatch** (switch 메모 §2a·§7)를 둘 다 지키는 정책이 생긴 다음이다 |
| `deliver(target)` → `deliver(waker, target)` (m→s) | WAKE 가 **마감을 싣는다** — 체인 단계는 TIMER 가 없어서 깨운 쪽의 마감 말고는 마감을 가질 길이 없다 |

---

## 입력의 모양 (coreset-single 24파일 실측)

최상위 키 3개: `meta` / `ground_truth` / `events`. 시뮬레이터는 `meta.id` 와 `events` 만 먹는다.

| events op | 개수 | | program op | 필드 | 개수 |
|---|---|---|---|---|---|
| `arrive` | 1949 (`depart` 1935) | | `RUN` | us | 69841 |
| `wake` | 7050 (channel+target) | | `SLEEP` | us | 53616 |
| | | | `WAIT` | channel | 7147 |
| spawn_table 엔트리 | 4485 (4파일, depart 없음) | | `LOOP` | count/body | 1914 (**전부 unbounded**) |
| | | | `TIMER` | period_us | 109 |
| | | | `WAKE` | target | 90 |

읽히는 것들:
- **`LOOP.count` 정수가 0건** → pc 를 프레임 스택으로 바꿀 이유가 없다. 평탄화 + 점프 하나.
- **SLEEP 이 두 번째로 많다** → 주기 작업용이 아니다. `archetypes.yaml` 이 명시한다:
  *"SLEEP (not TIMER) because stock daemons are not drift-free periodic"*.
- **키가 알파벳순으로 저장** (`depart,id,name,op,program,t`) → `op` 보고 분기하는 스트리밍 파싱 불가.
- **id/target/channel 이 전부 문자열** → 로더가 2-pass 로 전방 참조를 해소해야 한다.
- 시각 최대 180,000,000 (180초). `int64` 유지.

⚠️ `dataset/build/coreset-single/` 에 **24개**만 있다. 문서상 coreset 은 Phase 7 이후 50개 —
빌드가 낡았다. `cd dataset && make dataset`.

---

## 결정 기록

| id | 질문 (guide §) | 답 | 이유 / 버린 대안 |
|---|---|---|---|
| **D1** | §9.3 동시각 이벤트 순서 | (종류 우선순위, 삽입 순번). ConfigApply 가 최우선 | 삽입 순번만 쓰면 t=0 boot 설정이 arrive 뒤로 갈 수 있다(실제로 segfault). 종류 우선순위만 쓰면 같은 종류끼리 미정의 |
| **D2** | §9.1 대기자 없는 wake | **우편함(깊이 있음)**. 채널별 + 태스크별 | 잃어버리면 굶주린 태스크의 수요가 줄어 **측정하려던 피해가 은폐된다** (TIMER backlog 와 같은 이유). ⚠️ 우편함이 둘인 게 걸린다 — 외생 wake 는 channel 주소, WAKE 명령어는 target 주소. 실측은 채널당 대기자 하나라 결과가 같다 → ✅ **2026-10-10 결정: 하나로 합친다** (지워도 된다). 어느 쪽을 남길지·구현은 미정 — `../memo/memo_261010.md` Part E |
| **D3** | §9.4 depart mid-anything | 즉시 제거, 남은 수요·밀린 틱 전부 폐기 | guide 가 "presumable" 이라 한 그대로. 레인을 쥐었으면 `run_end reason=depart` 를 먼저 찍는다 |
| **D4** | §9.2 TIMER 의 t₀ | 그 태스크가 **TIMER 를 처음 실행한 순간** | 도착 시각: 도착~첫TIMER 사이 명령어가 첫 주기를 갉아먹는다. 전역 0: 모든 주기 태스크를 인위적으로 동기화시켜 경합 패턴을 왜곡한다. t=0 도착 태스크는 셋 다 같아 현재 coreset 이 답을 강제하지 못한다 |
| **D6** | EDF 의 체인 단계 마감 | WAKE 가 깨운 쪽의 현재 마감을 싣는다. 대기자가 없으면 우편함에 마감도 같이 쌓인다(`mail_dl`). 외생 wake 와 채널 우편함은 마감을 지운다 → residual | batch 메모 B2 "WAKE 로 닿는 전부 = EDF deadline class" 를 따랐다. ⚠️ **문서 충돌**: vocab §2 ("TIMER-driven") 와 pair review finding 5 ("woken stages are residual-class") 는 반대다. c2-p2b frame miss 가 0% ↔ 99.8% 로 갈린다 → `../notes/note-for-jioh-edf-chain-stage-class.md`. ✅ **2026-10-10 인지오 답: deadline class 가 맞다, 상속(head tick + 1 period) 그대로.** 코드 변경 없음. 데이터셋 개조(c1-gaming compositor 제거, c2-p2b clamscan → unattended-upgrade) 뒤 EDF 수치 재측정 |
| **D7** | EDF 동률 / 마감 부류의 슬라이스 | (마감, id) 순. 마감 부류는 지평선 없음, 동률은 선점 안 함. residual 은 RR, 선점당하면 남은 슬라이스 유지 | vocab "ties broken by a fixed executor rule" — D1 과 같은 id. Liu & Layland EDF 는 quantum 이 없다 |
| **D8** | LOTTERY 추첨 | ① 두 부류가 다 runnable 이면 bp 로 부류 ② 부류 안 균등. splitmix64, rejection 으로 편향 제거. seed = FNV-1a(workload 파일의 `meta.id`), 런당 1회 | "부류별 split + 부류 안 동일 티켓" 과 같은 분포. 스케줄 파일의 `workload_id` 는 쓰지 않는다 — 덮이기 전에 시드한다 |
| **D9** | FIFO 아래 B1 문턱 | boot default 의 `timeslice_us` = **10000** | batch 메모 §3 의 "2000 µs" 는 09-11 이전 문장. boot-default 메모 §5 가 "이제 10000 으로 읽으면 된다"고 이미 답했다 |
| **D5** | 알고리즘 교체 시 ready set | 떠나는 정책의 `handoff()` → id 정렬 → 새 정책 `start()` → `on_ready` 각각. 레인 홀더는 release 후 되돌려주고 재무장 | guide §5 가 미뤄둔 항목. 홀더를 ready set 에 넣으면 불필요한 컨텍스트 스위치가 생기고, 안 건드리면 새 정책의 지평선이 반영 안 된다 |

### 미결 (기록만 하고 넘어감)

- **§9.5 fork 슬롯**: 자식 둘이 같은 µs 에 EXIT 하면 부모의 FORK 는 한 번만 풀린다
  (다음 FORK 는 cap 이 비어 블록 없이 통과 → 결과 동일). 부모가 FORK 에 도달하는 바로 그
  순간 자식이 EXIT 하면 블록하지 않는다 (EXIT 처리가 먼저 끝나 live_children 이 이미 줄었다).
  둘 다 D1 이 결정한다.
- **`batch_bandwidth_cap`**: 여전히 집행하지 않는다 (읽지도 않는다). B1/B2 부류는 s 에서 생겼으니
  남은 건 "non-batch 가 runnable 한 동안 batch 몫 ≤ cap" 의 회계 창 하나다. 실행기 안전망(starvation
  window)도 미구현 — EDF 마감 부류와 FIFO 는 지평선이 없다.
- **cross-field 규칙 5** (`batch_share ≤ cap`) 와 범위 clamp: 로더가 하지 않는다. MLFQ 와 같이
  상류(validator)가 합성한 설정을 믿는다.
- **c1-gaming 은 EDF 에서 무너진다** (마감 5/5,664) — ~~과부하라 버그 아님~~ 은 반쪽 설명이었다.
  과부하(utilization 1.46, coreset-guide)는 사실이지만, 머리·compositor 의 마감까지 무너지는 건
  **D6 이 체인 16단을 deadline class 에 넣기 때문**이다. 상속을 끄면 7,372/7,372 met. → D6 질문.
- **⚠️ RUN→(블록 없이)→RUN 경계의 trace 결함 — r 부터 있다, s 는 고치지 않았다.** `advance()` 가
  다음 RUN 에 닿으면 `ready cause=arrive` 를 찍고 **run_end 없이** 레인을 놓고 재큐한다.
  boot MLFQ 에서 c1-gaming `ready` 86,239 줄 중 35,803 (41%), c2-p2b 175,443 중 43,098.
  **문서가 이미 답했다**: trace-clarifications 메모 §4 ("the line is emitted at that instant with the
  task already running", fake run_end/run_start 금지), metrics §6.1·§11.1. 질문이 아니라 구현 대기다.
  harness `records.py` 를 sim_r trace 에 돌리면 c1-media 에서 guard 4,798 — tick 0 의
  `ready(timer_tick)` 가 없어 job 번호가 하나씩 밀리고 music job 이 전부 miss 로 읽힌다.
  **다음 단계의 1순위.** LOTTERY 는 이 때문에 RUN 경계마다 재추첨한다.
- **`arm()` 의 임시 규칙**: 큐에 다른 일이 남아 있을 때만 정책 타이머를 다시 건다.
  계약에 `T_end` 가 생기면 대체된다. ⚠️ 처음엔 "살아있는 태스크가 있으면"으로 짰는데
  그게 버그였다 — 더 올 wake 도 depart 도 없이 영원히 블록된 태스크는 `Done` 이 아니지만
  죽은 것이고, 그러면 boost 가 자기 혼자 큐를 채워 시계를 무한정 민다.
  c1-compile 이 **1.95억 줄**(가상시간 11시간+)을 뱉었다. 고친 뒤 6,244 줄.
  ⇒ "프로그램이 끝났다"가 "맞게 돌았다"가 아니다. 규모를 안 봤으면 못 잡았다.
  ⇒ 그리고 첫 수정(`q_` 비면 중단)도 반쪽이었다: 태스크가 전부 `Done` 인데 큐에만
    일이 남은 경우(떠난 태스크 앞으로 온 wake 들)에 꼬리 boost 가 붙었다. c1-browsing
    이 7456 → 7491 줄로 *늘었다*. 두 조건의 **논리곱**이 맞다.
    두 판본 모두 "돌긴 돌았다" — 수정 전후 줄수를 대조하지 않았으면 못 봤다.
- **guide §4½ 문서 불일치**: 프로그램 리스팅은 명령어 4개인데 바로 아래 표는 t=32000 에서
  "next instruction WAIT → blocks" 라고 한다. 5번째가 있어야 성립한다 → 인지오 확인 항목.

---

## 검증

```bash
D=../../dataset/build/coreset-single
M=../../harness/tools/tests/fixtures/mock-switch/config-schedule.json

./sim_e                                   # guide §4½ 표
./sim_f && diff <(./sim_f) <(./sim_f --no-gen)   # gen 양성 대조
diff <(./sim_g fifo) <(./sim_e)           # 정책 추출이 행동을 안 바꿨나
./sim_r $D/c1-media.workload.json $M | grep config_applied
diff <(./sim_r $D/c1-office.workload.json) <(./sim_r $D/c1-office.workload.json)  # 바이트 동일
cmp <(./sim_r $D/c1-gaming.workload.json) <(./sim_s $D/c1-gaming.workload.json)   # s 회귀: 스케줄 없으면 동일
```

s 의 검증 (24파일 전수, 스케줄 6종):

| 무엇 | 결과 |
|---|---|
| 스케줄 없음 / MLFQ→FIFO (재진입 없음) 에서 `sim_s` == `sim_r` | 24×2 바이트 동일 |
| mock-switch / EDF / LOTTERY(0.15) / 8-엔트리 4알고리즘 교체 | 24×4 전부 종료, 두 번 돌려 바이트 동일 |
| `src/sim` == `sim_s` (`meta.sim` 만 정규화) | 위 전부 + 손 워크로드 18조합 동일 |
| LOTTERY seed 양성 대조 | `meta.id` 만 바꾸면 trace 가 달라진다 |
| `edfheavy` (TIMER 16.7ms·burst 12ms + hog) | EDF 599/599, MLFQ 0/250, LOTTERY 84/598 |
| `share2` (주기 부류 1 + hog 1, 둘 다 늘 runnable) | batch 몫 share 0.15 → 14.8%, 0.5 → 49.1% |
| EDF 슬라이스 경계 선점 수정 후 EDF·교체 경로 재검증 | 48/48 종료·재현·이식 동일. boot-default 메모 §5 시나리오에서 길이 0 occupancy 600 → 0 |

⚠️ 같은 µs 에 residual 슬라이스 끝과 TIMER 만료가 겹치면 선점으로 처리되면서 다 쓴 슬라이스를 유지해,
다음 dispatch 의 지평선이 0 → 길이 0 occupancy 가 생겼다. "경계와 같은 µs 의 선점 = 슬라이스 끝"으로 고쳤다.
첫 수정은 그 태스크를 ready set 에서 **지워버렸다**(t=166670 이후 scan 이 영영 안 뜀) — 레인이
일감을 두고 노는 걸 보고 잡았다. 상태 기록: `../memo/memo_261001.md`.

### §7 통합 게이트

1. ✅ coreset **24파일 전수**가 로드되고 끝까지 돈다
2. ✅ config schedule (boot default / MLFQ→FIFO→MLFQ 교체) 로 돌아간다
3. ✅ 24파일 전부 두 번 돌려 trace **바이트 동일** (md5 일치)
4. ⬜ 정상성 검사 4종이 아직 자동화 안 됨 (배달 CPU ≤ 경과 시간 / 완료 태스크의 RUN
   수요 전부 배달 / segment-bound 가 depart 에 사라짐 / 시간 역순 이벤트 없음).
   1·4 는 `release()` 의 assert 와 루프의 `assert(e.t >= now_)` 가 이미 지킨다.

---

## 곁가지로 확인된 것 — C2 가 구성적으로 보인다

`c2-p1a`(ml-train, wanted) 와 `c2-p1b`(indexing, **not** wanted) 는 논문이 걸린 그 한 쌍이다.
두 파일의 trace 를 뽑아 `task` 이름만 지우고 비교하면 **바이트 동일**하다.

```
c2-p1a  names: [code, python3]              gt: dev/wanted → ml-train/wanted
c2-p1b  names: [code, tracker-miner-fs-3]   gt: dev/wanted → indexing/NOT wanted
```

같은 도착 시각, 같은 프로그램, 같은 스케줄링 결과. 차이는 `name` 한 필드에만 있고
시뮬레이터는 그걸 trace 에 내보내지도 않는다. research-claims 의 사슬 C2
("행동 관찰로는 안 보인다")가 데이터셋 수준에서 구성적으로 성립한다는 뜻이다.

---

## 읽는 순서

계약 문서는 `docs/simulator/simulator-guide.md` (특히 §2 비협상 규칙, §4½, §5, §9) 와
`docs/simulator/interpretation-contract.md` (§2 지배 타이밍 원리, §3 명령어 의미론),
출력 형식은 `docs/data-contracts.md` §9, 설정 스키마는 `docs/recognition-vocabulary.md` §2.
