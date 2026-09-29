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

큰 델타 셋(h, n, r)은 쪼갤 수 없는 단위다 — MLFQ 다섯 규칙, FORK 의 생애주기, 두 번째 입력.

### 나중 단계가 앞 단계를 고친 곳

| 고친 것 | 왜 그때 몰랐나 |
|---|---|
| `Event.gen` (a→f) | 취소가 필요해지는 건 **선점이 생긴 다음**이다 |
| `Event.tag` (a→i) | 정책이 자기 타이머를 걸어야 하는 건 **규칙 5** 때문이다 |
| `on_lane` 검사 1항→2항 (c→f) | "레인을 놨다가 다시 잡는" 경우가 e 까지는 없었다 |
| ready set 이 코어→정책 (c→g) | MLFQ 의 ready set 은 "큐 여러 개"다. 구조 자체가 정책이다 |
| `vector<Task>`→`deque` (b→n) | FORK 가 실행 중 tasks_ 를 키운다. vector 면 `Task&` 가 댕글링 |
| D1 tie-break 개정 (a→r) | boot 설정이 같은 t=0 의 arrive 보다 먼저여야 한다 |
| 선점 복귀의 `ready` 제거 (f→g) | 계약의 `ready.cause` 에 preempt 가 없다 |

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
| **D2** | §9.1 대기자 없는 wake | **우편함(깊이 있음)**. 채널별 + 태스크별 | 잃어버리면 굶주린 태스크의 수요가 줄어 **측정하려던 피해가 은폐된다** (TIMER backlog 와 같은 이유). ⚠️ 우편함이 둘인 게 걸린다 — 외생 wake 는 channel 주소, WAKE 명령어는 target 주소. 실측은 채널당 대기자 하나라 결과가 같다 → **인지오 확인 항목** |
| **D3** | §9.4 depart mid-anything | 즉시 제거, 남은 수요·밀린 틱 전부 폐기 | guide 가 "presumable" 이라 한 그대로. 레인을 쥐었으면 `run_end reason=depart` 를 먼저 찍는다 |
| **D4** | §9.2 TIMER 의 t₀ | 그 태스크가 **TIMER 를 처음 실행한 순간** | 도착 시각: 도착~첫TIMER 사이 명령어가 첫 주기를 갉아먹는다. 전역 0: 모든 주기 태스크를 인위적으로 동기화시켜 경합 패턴을 왜곡한다. t=0 도착 태스크는 셋 다 같아 현재 coreset 이 답을 강제하지 못한다 |
| **D5** | 알고리즘 교체 시 ready set | 떠나는 정책의 `handoff()` → id 정렬 → 새 정책 `start()` → `on_ready` 각각. 레인 홀더는 release 후 되돌려주고 재무장 | guide §5 가 미뤄둔 항목. 홀더를 ready set 에 넣으면 불필요한 컨텍스트 스위치가 생기고, 안 건드리면 새 정책의 지평선이 반영 안 된다 |

### 미결 (기록만 하고 넘어감)

- **§9.5 fork 슬롯**: 자식 둘이 같은 µs 에 EXIT 하면 부모의 FORK 는 한 번만 풀린다
  (다음 FORK 는 cap 이 비어 블록 없이 통과 → 결과 동일). 부모가 FORK 에 도달하는 바로 그
  순간 자식이 EXIT 하면 블록하지 않는다 (EXIT 처리가 먼저 끝나 live_children 이 이미 줄었다).
  둘 다 D1 이 결정한다.
- **EDF / LOTTERY**: 미구현. `register_policy` 에 없으므로 요구하면 **거부**한다 —
  조용히 MLFQ 로 대체하지 않는다.
- **`batch_bandwidth_cap`**: 파싱만 하고 집행하지 않는다.
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
```

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
