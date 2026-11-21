# 2026-11-19의 변동 사항 — 인지오가 simulator tree에서 바꾼 것

> Status: memo · Created 2026-11-19 · Updated 2026-11-21
> 열림 — 다시 build하고(`simulator@841dc81131cb`) 단계 AF를 읽는 일(§1의 1과 2). batch-class 메모 §7의 항목 5(§1의 3)는 그 메모가 열어 둬요. 담당 인경민.
> From 인지오 to 인경민.

## TL;DR

- RQ0 run에서 oracle이 fixed보다 나빴던 경우를 하나씩 읽다가(TODO의 11.2) simulator의 결함을 하나 찾았어요. 인지오가 simulator tree에서 직접 고쳤어요. 단계가 하나 늘었어요.
  - **AF**: `fork_cap`이 차서 slot을 기다리는 `FORK`도 voluntary block이에요. 규칙 B1의 counter가 0으로 돌아가요.
- 새 version은 `simulator@841dc81131cb`예요.
- 경민이 할 일은 둘이에요. pull한 뒤 다시 build하기, AF 읽어 보기.
- RQ0 run의 판정은 바꾸지 않아요. 고친 simulator는 Phase 12의 두 번째 RQ0 run이 pin해요.

## 1. 경민이 할 일

1. **pull한 뒤 다시 build해요.**

   ```
   make -C simulator/src            # ./sim
   make -C simulator/src version    # simulator@841dc81131cb
   make -C simulator/src check      # unit test 일곱
   ```

2. **단계 AF를 읽어 봐요.** 경민의 tree에 인지오가 쓴 code예요. 바뀐 곳은 §2에 있어요. 고칠 것이 보이면 알려 주세요.
3. batch-class 메모 §7의 항목 5(규칙 B1과 B2를 simulator의 semantics notes에 적는 일)는 그대로 열려 있어요. 적을 때 B1의 voluntary block에 fork-slot 대기가 들어가요.

## 2. simulator에서 바뀐 것

### 2.1 단계 AF — fork-slot 대기와 규칙 B1

- **규칙.** batch-class 메모(`docs/memos/2026-09-09-batch-class-rule-for-the-simulator.md` §3)의 B1이에요. task는 마지막 voluntary block 뒤로 CPU를 한 slice 다 쓰면 batch class에 들어가고, 다음 voluntary block에서 나와요. voluntary block은 task가 스스로 CPU를 놓는 것이에요.
  - 메모의 목록(막히는 `WAIT`, `SLEEP`, 아직 안 온 `TIMER`)은 spawn table과 `FORK`가 생기기 전에 쓰였어요.
  - 두 메모에 2026-11-19 정정을 달아서 목록에 fork-slot 대기를 더했어요. batch-class 메모의 "Correction (2026-11-19)"와 batch-class-and-cap 메모(`2026-10-20-batch-class-and-cap.md`)의 "정정 (2026-11-19)"이에요.
- **전에 일어나던 일.** `FORK`가 `fork_cap`에 걸려 slot을 기다리면 task는 막혔지만 B1의 counter(`burst`)는 그대로였어요.
  - 자식들을 기다리는 `WAIT`에서는 counter가 0으로 돌아가요. 같은 행동인데 다르게 셌어요.
  - 그래서 orchestrator가 slot을 기다리는 동안에도 batch class에 남았어요. RQ0 run의 `oracle`에서 `make`가 `c1-compile`에서 17,004번, `c7-compile`에서 5,639번 그랬어요.
- **바뀐 곳.** `FORK` case에서 slot을 기다리며 막힐 때의 `t.burst = 0` 하나예요.
- **영향.** RQ0 run의 129개 파일을 그 run의 `fixed`와 `oracle` schedule로 다시 돌려서, trace를 header 줄만 빼고 줄 단위로 비교했어요.
  - `fixed`는 129개 모두 그대로예요.
  - `oracle`은 117개가 그대로예요. 다른 12개는 build가 있는 파일이에요(`c1-compile`, `c7-compile`과 각각의 변형 넷, `c3-workday`, `c4-compile`).
  - criterion의 1,938 run(judging 파일 19개 × `fixed`, `oracle`, `random` seed 100개)도 고친 simulator로 다시 돌렸어요. 바뀐 것은 `c1-compile`과 `c7-compile`의 `oracle`과 `random` run이에요(파일마다 102개 중 101개). `fixed`와 나머지 17개 파일은 그대로예요.
  - oracle이 fixed보다 나쁜 경우는 전과 같은 9개예요. 값이 바뀐 것은 `c1-compile`의 editor input latency P99 하나예요. 361.03초에서 363.14초가 됐어요.
- **unit test.** `tests/test_batch_class.py`에 (d)를 더했어요. FIFO에서 돌려요.
  - parent가 15 ms 돌고, 30 ms 자는 자식을 `FORK`하고, 다시 `FORK`해서 slot을 기다린 뒤 9 ms 돌아요.
  - slot 대기 뒤에는 park되지 않아야 해요. 양성 대조는 첫 burst에서의 park(2번)예요.
  - 수정 전 binary(`simulator@0d323c84470a`)에서는 실패해요. slot이 46,000 µs에 온 뒤 46,620, 49,511, 52,511 µs에 park돼요.
  - `tests/mutants.py`에 mutant `fork-wait-keeps-burst`를 더했어요.

### 2.2 그 밖

- **reference trace 둘.** `fix-object`와 `fix-tree`의 header 줄이 새 version을 적어요.
- **`tools/replay_fixtures.py`.** 기본 binary가 `steps/sim_af`예요. fixture 재생 결과는 `sim_ae`와 같아요.
- **`steps/Makefile`, `steps/README.md`, `src/notes.md`.** AF를 더했어요.
- **남은 것 하나.** `src/sim.cpp`의 `main()` 위 주석에 `steps/sim_af: ./sim_ae W [S]`라고 옛 binary 이름이 남아 있어요. version이 source의 hash라서 이번에는 그대로 두었어요. 다음에 source를 고칠 때 같이 고쳐요.

## 3. 확인한 것

- **unit test와 mutant.** `make -C simulator/src check`의 일곱 test file이 모두 통과해요. `make -C simulator/src mutants`의 mutant 여섯은 모두 자기 test에서 실패해요.
- **회귀.** §2.1의 영향에 적은 258 run과 criterion의 1,938 run이에요. 1,938 run은 header 줄을 뺀 trace와, `sim`과 `source_sha256` column을 뺀 records로 RQ0 run과 비교했어요.

## 4. 자세한 기록

- `_dev/research/jioh/task-11.2-the-degraded-oracle/cases.md`의 "The fork-slot wait and rule B1".
- `simulator/steps/README.md`와 `simulator/src/notes.md`의 AF 행.
