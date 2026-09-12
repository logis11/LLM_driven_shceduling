# RQ0 gate spec 확정 안내 — 판정 기준을 실행 전에 파일로 못 박았어요

> Status: memo · Created 2026-09-12 · Updated 2026-09-12
> From 인지오 to 인경민, 박이안. RQ0(random vs oracle의 gap이 잴 만큼 큰가)의 판정 기준을 **실행 전에** 하나의 파일로 확정했어요: `harness/experiments/rq0-gate.yaml`. 이 memo는 거기에 무엇이 어떤 근거로 들어갔는지, 그리고 두 분께 확인을 부탁드릴 것이 무엇인지 적어요. 두 분 프로그램의 입출력 형식은 하나도 안 바뀌었어요. 급하면 §1과 §4·§5만 읽어도 돼요.

## 1. 한 문단 요약

RQ0 gate spec은 harness가 그대로 읽고 실행하는 데이터예요: 어떤 파일을 판정에 쓰는지(25개), 몇 개가 넘어야 통과인지(K = 13, 과반), 파일 하나가 "넘었다"는 기준(g = 0.5, oracle이 얻는 개선의 절반 이상을 random이 못 얻음), random을 몇 번 돌리는지(N = 100), boot default를 바꿔 가며 다시 재는 sweep(9개 지점), 실패하면 무엇부터 하는지(config search 먼저), 그리고 채점 규칙 파일들의 hash pin. 숫자마다 근거가 같은 파일 안에 적혀 있고, 실행이 시작된 뒤에는 changelog 없이는 아무것도 못 바꿔요. 두 가지는 **두 분의 답을 기다리는 가정**으로 들어갔어요: 인경민께 여쭤본 executor 규칙 세 개(§4), 박이안께 드리는 `random`의 정의와 N(§5).

## 2. 정한 것

1. **판정 set 25개.** C2 pair 여섯, batch C1 base 여섯, term이 있는 C7 counterpart 열셋. 09-11 memo §6에서 말한 `c7-meeting`·`c7-media`는 §4의 가정 아래에서는 두 row가 모든 term에서 비기고 `fixed`와도 비겨서 — 판정 규칙("term이 row의 차이를 설계상 드러내는 파일만")에 안 맞아 — **보고 전용**으로 뺐어요. 답이 오면 되돌아올 조건이 spec에 적혀 있어요(§4).
2. **g = 0.5.** 읽는 법: "인식(recognition)이 얻을 수 있는 개선의 절반 이상을 책임진다". 출처가 있는 값은 아니고, 실행 전에 정한 최소 효과 크기예요. 그래서 g를 0.25 / 0.33 / 0.5 / 0.67로 바꿨을 때 통과 개수가 어떻게 되는지를 **함께 보고**해요(채점 단계에서 다시 세기만 하면 돼요). 개수가 band 안에서 움직이면 결과를 점이 아니라 범위로 적어요.
3. **K = 13.** 25개 중 과반. 보고서에는 K와 무관하게 실제 개수가 찍히니, K는 선 하나만 그어요.
4. **N = 100.** 근거 둘. (a) 정밀도: random 점수의 seed 평균을 쓰는데, seed마다 값이 아무리 흩어져도 N = 100이면 평균의 오차가 0.05(g의 1/10) 아래. (b) 커버리지: draw는 32 row 위의 균등 분포라, 한 row짜리 config가 100번 동안 한 번도 안 뽑힐 확률은 (31/32)^100 ≈ 4%. 파일마다 seed 평균의 표준오차도 보고서에 찍어서, 정밀도 주장을 데이터로 확인해요.
5. **boot default sweep.** 09-11 memo §4의 5번("sensitivity pair는 팀에서")을 pair가 아니라 **9개 지점의 sweep**으로 바꿨어요: OSTEP 설정에서 최상위 slice만 0.5 / 0.75 / 0.9 / 1.2 / 2 / 3 / 5 / 20 / 100 ms로 바꾼 것(primary는 10 ms 그대로). 뼈대는 schema의 양 끝(0.5, 100)과 출하된 기본값 셋(Linux 0.75, illumos TS 2, sched_ext 20)이고, 나머지는 판정 set의 주기 task가 slice에 반응하는 문턱(gaming pair의 frame 여유 831 µs, chain stage 최대 1 470/2 176 µs, compositor burst 6 667 µs, boost 뒤 1 ms 지점)의 양옆이에요. 지점마다 이유가 spec에 있어요. **`fixed` run만** 다른 boot default로 다시 돌고, oracle·random과 driver table은 그대로예요. 두 분 쪽에서 할 일은 없어요 — daemon은 boot default 파일을 경로로 받는 것뿐이고(invocation contract), simulator는 schedule의 첫 entry를 읽을 뿐이에요.
6. **실패 절차.** 통과 못 하면 workload를 고치기 전에 **config search 먼저**: 실패한 파일 셋을 규칙으로 고르고(prior table의 중복 구조 때문에 갈리는 두 부류에서 하나씩 + gap이 g에서 가장 멀었던 파일), 설정을 훑어 spread가 있는지 봐요. spread가 없으면 workload 재설계, v0 table이 놓친 spread가 있으면 table을 다시 써요.
7. **prior table의 구조를 미리 적어 뒀어요.** 32 row지만 config는 8종류뿐이고(params가 전부 boot 값이라 algorithm과 cap만 다름), 그중 13 row가 같은 config(MLFQ, cap 0.05)예요. 그래서 판정 파일 25개 중 13개에서는 random이 41% 확률로 oracle과 똑같은 config를 뽑아요. 이건 gate를 **보수적으로** 만드는 성질이고(random이 세짐), 실패가 그 13개에 몰리면 table 점검부터 하도록 실패 절차에 넣었어요.
8. **freeze.** scoring spec과 guard spec(0.1 → 1.0)을 2026-09-12에 얼렸고(`harness/CHANGELOG.md`), RQ0 gate spec이 그 파일들의 SHA-256을 pin해요. 이후의 변경은 changelog entry 하나로 남아요. 팀 회의에서 함께 확인해 주시면 돼요.

## 3. 무엇이 그대로인가

- config schedule, recognition log, trace, telemetry의 형식. invocation contract(09-11 memo).
- boot default의 값(OSTEP 예시, 10 ms). sweep의 9개 파일은 harness 안에 있고, daemon은 경로로 받을 뿐이에요.
- guard 여덟 개와 threshold. `starvation_floor`만 §4의 세 번째 답을 기다려요.

## 4. 인경민께 — 세 질문이 "가정"으로 들어갔어요

09-11 memo §5의 세 질문에 아직 답을 못 받아서, 제 제안을 **가정**으로 spec에 적고(`statements: executor-assumptions`, "2026-09-11 제안, 인경민 확인 대기"로 표시) phase를 닫았어요. 답이 오면 spec에 기록하고, 값이 달라지면 실행 전에 changelog entry로 바꿔요.

1. **EDF에서 deadline task가 깨어나면 residual slice를 바로 뺏는다** (option A).
2. **같은 µs에 slice 경계와 TIMER 만료가 겹치면 깨어남을 먼저, dispatch를 나중에** 처리하고, trace의 line 순서도 그렇다.
3. **executor의 starvation window는 1 000 000 µs** (guard `starvation_floor`의 threshold).

답에 따라 달라지는 건 딱 하나예요. 1·2가 제안대로면 `c7-meeting`·`c7-media`는 지금처럼 보고 전용이에요. **반대로, residual task가 slice를 끝까지 쓰고(option B) 같은 µs에서 dispatch가 깨어남보다 먼저**라면, 두 파일은 cap 축이 처음으로 측정되는 파일이 되어 **판정 set으로 되돌아오고** K는 같은 읽기(과반)로 27개 중 14로 바뀌어요 — 실행 전에, changelog entry로. 그 조건도 spec에 그대로 적혀 있어요. 이미 정해 두셨거나 구현에 상수가 있으면 위치만 알려주셔도 돼요.

## 5. 박이안께 — `random`의 정의와 N을 확인해 주세요

spec에 적힌 `random`의 정의(`statements: random-reading`)는 daemon guide의 것 그대로예요: **telemetry set이 바뀔 때마다, 32 row 위에서 균등하게 하나를 뽑고, 이전 draw나 telemetry와 무관하며, run마다 seed된 PRNG에서 뽑고, draw와 seed를 log에 남기고, latency는 0.** 이 읽기가 맞는지, 그리고 **N = 100**(seed 1..100, harness가 `--seed`로 넘겨요)이 daemon 쪽에서 문제없는지 확인 부탁드려요. 비용은 random run이 파일당 100번이라 전체 5 000 run이에요(simulator 시간이 얼마나 걸리는지는 경민 님 것이 오면 재 보고, 감당이 안 되면 N을 changelog entry로 조정해요). draw 공간을 sampling 대신 **열거**하는 것(32 row를 다 돌리기)은 나중 선택지로 이름만 적어 두고 채택하지 않았어요. 확인이 오면 spec에 기록해요 — Phase 9 시작 전 필수예요.

## 6. 어디를 읽으면 되나

- `harness/experiments/rq0-gate.yaml` — spec 본문. `statements`에 근거가 다 있어요.
- `harness/CHANGELOG.md` — freeze 기록.
- `harness/boot-defaults/` — primary `ostep.json`과 sweep 9개.
- `docs/recognition-vocabulary.md` §2 sensitivity 문단과 changelog 2026-09-12.
- `docs/memos/2026-09-11-boot-default-from-ostep.md` §5 — 세 질문의 원문.
