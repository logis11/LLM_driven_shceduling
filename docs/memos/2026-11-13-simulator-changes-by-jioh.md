# 2026-11-13의 변동 사항 — 인지오가 simulator tree에서 바꾼 것

> Status: memo · Created 2026-11-13 · Updated 2026-11-13
> From 인지오 to 인경민.

## TL;DR

- 경민의 2026-11-11 commit(`2ee49785`)을 집 machine에서 확인했어요. 2026-10-30 메모 §2의 여섯 항목이 모두 들어와 있어요.
- 남은 차이는 인지오가 simulator tree에서 직접 고쳤어요. 단계가 둘 늘었어요.
  - **AD**: 관측 구간의 끝과 같거나 뒤에 찍힌 schedule entry는 무시해요.
  - **AE**: idle class의 task는 `batch_bandwidth_cap`을 켜지 않아요.
- 경민이 할 일은 셋이에요. pull한 뒤 다시 build하기, AD와 AE 읽어 보기, batch-class 메모 §7의 항목 5.
- 통합 gate(TODO의 10.2)를 막는 일은 경민 쪽에 없어요.
- cold smoke(TODO의 10.3)에서 judging 파일이 starvation guard에 걸리면, starvation 안전망의 설계가 경민에게 돌아가요.

## 1. 경민이 할 일

1. **pull한 뒤 다시 build해요.** `simulator/src/sim`을 git 추적에서 뺐어요. pull하면 그 파일이 지워져요.

   ```
   make -C simulator/src            # ./sim
   make -C simulator/src version    # simulator@0d323c84470a
   make -C simulator/src check      # unit test 넷
   ```

2. **단계 AD와 AE를 읽어 봐요.** 경민의 tree에 인지오가 쓴 code예요. 바뀐 곳은 §2에 있어요. 고칠 것이 보이면 알려 주세요.
3. **batch-class 메모 §7의 항목 5.** 규칙 B1과 B2를 simulator의 semantics notes에 적는 일이에요. 전부터 열려 있던 것이고, gate의 조건은 아니에요.

## 2. simulator에서 바뀐 것

### 2.1 단계 AD — schedule entry의 End 규칙

- **규칙.** `docs/data-contracts.md` §7에 이미 있던 문장이에요. "End: entries at or after the workload's end … are ignored by the simulator."
- **동작.** 관측 구간의 끝(`T_end`)은 run file에 적힌 가장 늦은 시각이에요(도착, depart, wake event). 그 시각과 같거나 뒤에 찍힌 entry는 queue에 넣지 않아요. 적용도 `config_applied` line도 없어요.
  - 찍힌 시각으로 봐요. 끝 전에 찍혀서 drain 때문에 끝을 넘긴 entry는 적용돼요.
  - boot entry(index 0)는 항상 적용해요. `fix-object`와 `fix-tree`는 적힌 시각이 0뿐이라 `T_end`가 0이에요.
- **바뀐 곳.** `set_schedule()`, 그리고 `T_end`를 구하는 `add()`와 `wake()`.
- **영향.**
  - `mock-guards`에 남아 있던 한 line이 사라졌어요.
  - `fixed`의 trace는 129개 파일 모두 그대로예요.
  - `oracle`은 129개 파일 모두 마지막 entry가 정확히 `T_end`에 찍혀 있어서 그 entry가 무시돼요. `T_end` 이전은 모두 그대로예요.
  - 세 run(`c7-gaming@chain-x1.2`, `c7-gaming@chain-x1.4`, `c2-p2a@seg1-120s`)에서는 records가 달라져요. 무시된 entry가 끝 시각에 `steam`을 한순간 실행시키던 것이 없어져서, `steam`의 마지막 timer wake가 censored가 돼요.

### 2.2 단계 AE — idle class 옆의 cap

- **규칙.** `docs/recognition-vocabulary.md` §2에 한 문장을 더했어요. cap은 idle class가 아닌 non-batch task가 runnable일 때만 적용돼요.
- **전에 일어나던 일.** 두 규칙이 서로를 막았어요.
  - idle 규칙이 세워 둔 idle task를 cap이 "runnable인 non-batch task"로 세서, 옆의 batch task를 묶었어요.
  - cap이 세워 둔 batch task를 idle 규칙이 "runnable인 다른 class의 task"로 세서, idle task를 계속 세웠어요.
  - `c2-p1b`의 `oracle`에서 39초 동안 CPU가 4.8%만 쓰였고, idle인 indexer는 그 내내 기다렸어요.
- **바뀐 곳.** `capped_now()`의 조건 하나.
- **영향.**
  - idle task가 없는 파일은 그대로예요.
  - `oracle`에서 idle task와 cap이 함께 있는 여섯 파일(`c1-indexing`, `c7-indexing`, `c2-p1b`, `c1-backup`, `c7-backup`, `c2-p3b`)의 trace가 달라져요.
  - `c2-p1b`의 `oracle`은 harness의 starvation guard가 fail에서 pass로 바뀌어요.
- **unit test.** `tests/test_batch_class.py`에 (c)를 더했어요. 수정 전 binary에서는 실패해요.

### 2.3 그 밖

- **reference trace 둘.** `fix-object/generate.py`가 `src/sim`을 flag 셋과 boot entry 하나짜리 schedule로 불러요. header의 `sim`은 version 문자열이에요.
- **`tools/replay_fixtures.py`.** 기본 binary가 `steps/sim_ae`예요. reference fixture도 boot entry schedule로 재생해요.
- **`tools/wait_check.py`(새 도구).** trace에서 task마다 CPU를 기다린 시간을 세요. starvation guard가 읽지 못하는 두 가지(끝까지 열린 기다림, 선점 뒤의 기다림)도 세요.
- **`.gitignore`.** `src/`는 `sim`과 `sim.dSYM/`, `steps/`는 `*.dSYM/`를 더했어요.
- **mailbox 합치기(D2).** 경민의 제안대로 닫았어요. 추론이라고 적은 부분은 여섯 파일에서 확인했어요.
- **`_dev/TODO.md`의 경민 section.** 인지오가 저장소 상태에 맞췄어요. 1.3 완료, backlog의 (g)·(h)·unit test 줄, mailbox 합치기 줄이에요.

## 3. 확인한 것

- **경민이 못 돌린 harness 검사.** 일곱 파일을 `fixed`와 `oracle`로 실제 daemon, `src/sim`, harness의 records까지 돌렸어요. 14 run 모두 guard message가 0개예요.
- **hand fixture 아홉 개.** cap을 끄면 모두 일치하거나 같은 µs 안의 순서만 달라요.
- **회귀.** AD와 AE 각각, 129개 파일을 `fixed`와 `oracle`로 돌린 258 run을 앞 단계와 비교했어요. 모두 exit 0이에요.

## 4. 정해진 것

- **통합 gate의 비교 규칙 셋.**
  - `mock-guards`, `mock-p1a`, `mock-switch`는 cap을 null로 두고 재생해요. fixture가 cap을 모델링하지 않아서예요.
  - 같은 µs 안의 line 순서는 보지 않고, simulator trace로 만든 records가 `expected.csv`와 같은지를 봐요.
  - header line은 비교에서 빼요.
- **driver table의 인용.** `simulator/src/sim.cpp:328–366` 대신 `struct Lottery`라는 이름으로 인용해요. 통합 gate가 통과할 때 고쳐요.
- **starvation.** `oracle`에서 다섯 run이 30초를 넘어요. EDF에서 frame chain이 CPU를 다 써서 `steam`이 기다리는 경우예요.
  - `c3-evening` 240.0초, `c2-p2a`와 `c2-p2b`의 chain 1.2배·1.4배 변형 넷 86.4초.
  - judging 파일은 모두 멀쩡해요(가장 긴 기다림 1.15초). `fixed`에는 30초를 넘는 run이 없어요.
  - 안전망은 넣지 않아요. 다른 조건은 cold smoke에서 봐요.

## 5. 자세한 기록

- `simulator/memo/memo_261111.md`의 Part K(경민의 질문 여섯에 대한 답, 단계 AD)와 Part L(starvation 계수, 단계 AE).
- `simulator/steps/README.md`와 `simulator/src/notes.md`의 AD, AE 행.
