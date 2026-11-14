# 2026-11-14의 통합 gate — 인지오가 simulator tree에 더한 것과 gate의 결과

> Status: memo · Created 2026-11-14 · Updated 2026-11-14
> From 인지오 to 인경민.

## TL;DR

- 통합 gate(TODO의 10.2)를 집 machine에서 돌렸고 통과했어요. simulator는 `simulator@0d323c84470a`, daemon은 `daemon@62c71f0d2de0`이에요.
- RQ0 gate spec이 이 두 version 문자열을 pin해요. runner는 machine configuration이 다른 version을 적으면 어떤 run도 시작하지 않아요.
- 인지오가 simulator tree에 unit test 다섯 개와 mutant 다섯 개를 더했어요(`simulator/tests/`). `make -C simulator/src check`가 이제 일곱 개를 돌려요.
- 경민이 할 일은 둘이에요. pull한 뒤 다시 build하고 `check`를 돌리기, 새 test 읽어 보기.
- simulator의 source가 바뀌면 version 문자열이 바뀌어서 gate를 다시 지나야 RQ0 run을 돌릴 수 있어요.

## 1. 경민이 할 일

1. **pull한 뒤 다시 build해요.**

   ```
   make -C simulator/src            # ./sim
   make -C simulator/src version    # simulator@0d323c84470a
   make -C simulator/src check      # unit test 일곱 개
   make -C simulator/src mutants    # 행동 test 넷이 mutant에서 실패하는지
   ```

2. **새 test를 읽어 봐요.** 경민의 tree에 인지오가 쓴 code예요. §2에 무엇을 보는지 적었어요. 고칠 것이 보이면 알려 주세요.
3. **source를 고치면.** `sim.cpp`나 `mini_json.hpp`를 고치면 version이 바뀌어요. 그 binary로 RQ0를 돌리려면 인지오가 gate의 세 부분(unit test, fixture 재생, 짧은 run)을 다시 돌리고 pin을 고쳐야 해요. 바꾼 것을 알려 주세요.

## 2. simulator tree에 더한 것

모두 `simulator/tests/`에 있고, binary를 밖에서 부르는 black-box test예요. 경로를 인자로 받아요(기본값 `simulator/src/sim`).

| 파일 | conformance 항목 | 보는 것 |
|---|---|---|
| `test_cap_ceiling.py` | (d) | cap이 batch class의 상한이에요. hog의 몫이 cap + 세 slice/창 이하예요(MLFQ, FIFO, LOTTERY에서 0.05와 0.2). cap이 없으면 hog가 그 경계를 넘어요. hog 혼자이면 cap 0.05에서도 lane을 다 써요(네 algorithm 모두). |
| `test_idle_class.py` | (e) | 네 algorithm 모두에서 idle task는 normal task가 runnable인 동안 lane을 잡지 않고, wake가 오면 그 µs에 선점돼요. 남는 시간은 idle task가 다 써요. |
| `test_edf_chain.py` | (f) | EDF에서 frame chain의 단계가 deadline class에 있어요. 마감이 29 999 µs인 probe는 단계를 바로 선점하고, 30 000 µs인 probe는 선점하지 못해요. 그래서 단계의 마감이 frame의 마감 30 000 µs와 정확히 같아요. |
| `test_spawn_children.py` | (i), (g) | `fix-object`와 `fix-tree`의 worked.md가 읽는 것 — 태어나기 전에 보낸 wake가 태어날 때 받아지고, 모든 도착에 `task_end`가 하나씩 있고, `WAIT children:build`가 마지막 child의 `task_end`에서 끝나요. 또 child가 하나도 살아 있지 않을 때의 WAIT는 막히지 않고 occupancy 안에서 지나가요. |
| `test_invocation.py` | (h) | 세 flag로 부르면 trace를 그 파일에만 쓰고, 같은 인자로 두 번 쓰면 byte가 같고, header의 `sim`이 `make version`이에요. 여섯 가지 잘못된 호출은 exit 2이고 trace가 없어요. 쓸 수 없는 경로는 exit 0이 아니에요. |
| `mutants.py` | — | 행동 test 넷이 그 행동을 뺀 source에서 실패하는지 봐요. 한 줄을 바꿔 compile해요. idle band 끄기, WAKE가 마감을 안 나르기, 태어나기 전 wake 버리기, children wait를 안 끝내기, 살아 있는 child가 없어도 막히기. 바꿀 줄이 source에 정확히 한 번 있지 않으면 error예요. |
| `blackbox.py` | — | 위 test들이 함께 쓰는 실행과 trace 읽기. |

`src/Makefile`의 `check`에 다섯 test를 더했고, `mutants` target을 새로 만들었어요. `sim.cpp`는 바꾸지 않았어요.

## 3. gate의 결과

결과는 `_dev/research/jioh/task-10.2-integration-gate/`에 부분마다 `<part>.json`과 `<part>.log`로 있어요. compiler는 Apple clang 21.0.0이에요.

- **unit test.** 일곱 개 모두 통과해요. mutant 다섯 개에서는 해당 test가 모두 실패해요.
- **fixture 재생.** hand fixture 일곱 개와 reference fixture 둘을 `src/sim`의 세 flag로 두 번씩 재생했어요.
  - 일곱 개는 line이 같고, `mock-chain`과 `mock-media`는 같은 µs 안의 순서만 달라요.
  - hand fixture 일곱 개 모두 simulator trace로 만든 records가 `expected.csv`와 같아요(`sim`과 `source_sha256` 열 빼고).
  - 두 번의 trace는 byte가 같고, header의 `sim`은 pin한 version이에요.
- **daemon 비교.** RQ0 gate spec에서 runner가 펼치는 run 19 425개 모두에서 `daemon/daemon.py`와 harness의 mock daemon이 쓴 schedule과 log가 byte까지 같아요.
- **짧은 run.** 일곱 파일(`c1-photo`, `c1-office`, `c7-mail`, `c2-p2b`, `c1-gaming`, `c7-compile`, `c1-compile`)을 집 machine의 실제 설정으로 smoke tool에 돌렸어요. 28 run 모두 끝났고 report가 써졌어요. fail인 guard는 하나인데, `c2-p2b`의 짝 `c2-p2a`가 일곱 파일에 없어서 생긴 C2 pair check예요. 58분 걸렸고, 대부분은 `c1-compile`의 records를 만드는 시간이에요(run 하나에 약 12분).

## 4. 정해진 것

- **실패하면 인지오가 고쳐요.** 계약이 어느 쪽이 틀렸는지 정해요. simulator가 틀리면 인지오가 step ladder에 새 단계를 만들고 `src/sim.cpp`에 옮긴 뒤 경민에게 memo로 알려요. fixture나 test가 틀리면 harness changelog에 적고 고쳐요.
- **driver table의 인용.** 네 table이 `simulator/src/sim.cpp:328–366` 대신 `struct Lottery`라는 이름으로 인용해요.

## 5. 자세한 기록

- spec: `_dev/docs/spec/jioh/task-10.2-integration-gate.md`.
- harness 쪽 변경: `harness/CHANGELOG.md`의 2026-11-14 항목.
