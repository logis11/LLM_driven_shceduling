# workload dataset 다시 만들기 예고 — 무엇이 바뀌고 무엇이 그대로인지, 인경민께 질문 세 개

> Status: memo · Created 2026-09-13 · Updated 2026-09-13
> From 인지오 to 인경민, 박이안. 가벼운 예고예요. workload dataset의 근거를 원문과 build에 대조해 봤더니 고칠 게 꽤 나와서, dataset을 한 번 다시 만들고 그 위에 올린 결정들을 다시 해요. 두 분 프로그램의 입출력 형식은 이번 작업 범위 밖이에요. 인경민께는 executor 질문이 세 개 있어요(§4).

## 1. 왜 — 찾은 것 요약

2026-09-13에 dataset이 출처에서 가져온 claim을 원문과 따로 읽어 대조하고, meas-ci 측정을 raw release에서 다시 돌려 보고, 결정 문서에 적힌 숫자를 build와 맞춰 봤어요. 큰 것만:

- **원문과 다른 인용.** 예: `build-orchestrator`의 2,430 process는 Linux kernel build가 아니라 DynamoRio 6.1.0 build의 숫자이고, gaming chain 주기의 16.7 ms frame budget은 LAVD 슬라이드에 없어요. 13건 전체는 `docs/memos/2026-09-13-critical-findings.md`.
- **측정 방법.** compiler "child"가 cc1 하나가 아니라 번역 단위당 process 네 개쯤(gcc·cc1·as·fixdep)이라 cc1 하나의 CPU가 약 4배 작게 잡혔어요. `disk_wait`은 disk 대기를 잰 값이 아니고, voluntary context switch는 main thread만 셌어요.
- **compile된 workload의 동작.** focused editor가 CPU를 약 50% 쓰고 burst의 95% 안팎이 10 ms slice보다 길어요. prior table의 "editor는 slice 안에 block해서 MLFQ 위 queue에 남는다"는 전제가 안 맞아요.
- **harness.** guard `tick_count`의 chain check가 c2-p2a·c2-p2b에서 구조적으로 fail해요(마지막 tick 뒤에 frame 하나를 끝낼 시간이 없어요). c7-gaming도 거의 확실해요. 지금대로면 RQ0 판정이 `invalid`가 돼요.
- **판정 set.** c2-p2a는 10 ms slice에서 두 row가 차이를 못 내고, c1-backup의 borg는 혼자 돌아도 60 s 안에 못 끝나서 turnaround가 항상 censored예요.

기록은 `_dev/research/jioh/2026-09-13-verification/`에 있어요(숫자 대조는 `compiled-numbers-report.md`).

## 2. 무엇이 바뀌나

- **dataset.** archetype 값, timeline 구성, 측정 도구, dataset 문서. 값마다 원문 passage와 위치가 붙고, 출처가 없는 값은 convention·arithmetic·placeholder·design 중 무엇인지 표시돼요. 새로 재야 하는 건 CI runner에서만 재요.
- **dataset 위의 결정.** scoring spec, guard spec(`tick_count` 포함), prior table과 pair review, RQ0 gate spec. harness changelog entry 하나와 re-pin 한 번으로 모아서 바꿔요. RQ0 판정 set, boot-default sweep 지점, K도 결과에 따라 다시 정할 수 있어요.
- **dataset 밖의 인용.** related-work와 research proposal, harness·metrics 상수의 근거, guidebook 정정.
- **순서.** 기록 보존과 측정 도구 수리 → 영역별 조사를 병렬로(gaming, interactive·typing, compile, background·IO, browser·comms, daemon·session process, scenario·timeline, scheduler 쪽 상수, related-work) → dataset rebuild 한 번 → 위 결정들 rework 한 번 → 문서 정리와 마무리 memo.

## 3. 무엇이 그대로이고, 두 분께 뜻하는 것

- config schedule, recognition log, trace, telemetry 형식과 invocation contract는 이번 범위 밖이에요.
- workload 파일은 rebuild 때 내용이 바뀌어요(값, 그리고 timeline 조사 결과에 따라 파일 구성도). 그때까지는 지금 파일로 개발하시면 되고, rebuild가 들어오면 알려드릴게요.
- **인경민:** 첫 integration gate(C1 workload 하나, rerun trace byte-identical)는 지금 파일로 계속하셔도 돼요. 아래 세 답은 결정 rework 전에 필요해요.
- **박이안:** recognition log는 rebuild 뒤에 다시 뽑아야 해요. 형식은 그대로예요.

## 4. 인경민께 — executor 질문 세 개

이미 구현에서 정하셨으면 코드나 문서 위치만 알려주셔도 돼요.

1. **LOTTERY — editor 자신의 burst tail이 batch class일 때 batch share는 어떻게 나뉘나요?**
   - vocabulary §2: LOTTERY는 ticket을 두 class에 `batch_share : (1 − batch_share)`로 나누고, class 안에서는 task마다 같은 ticket. batch-class memo 규칙 B1: 마지막 voluntary block 뒤로 slice 하나를 다 쓴 task는 batch class.
   - compile된 editor는 CPU의 91–92%가 burst 첫 10 ms 뒤에 있어서, burst 대부분 동안 editor도 job도 batch class이고 non-batch class는 비어요. 이때 ticket을 어떻게 나누는지는 적힌 데가 없어요(cap을 재는 window도 batch-class memo §7 3번에서 simulator 쪽에 맡겨 둔 상태).
   - 답에 따라: LOTTERY wanted row들의 "editor가 나머지 절반·2/3을 가진다"는 설명(compile/true, ml-train/true, render/true, pair review p1).
2. **EDF — frame chain의 stage는 deadline class인가요, residual class인가요?**
   - vocabulary §2: "deadline class는 TIMER-driven task". batch-class memo 규칙 B2: TIMER가 있는 task와 거기서 WAKE로 닿는 모든 task가 periodic class이고, 이게 "EDF의 deadline class와 정확히 같은 set".
   - gaming chain의 stage 2–16은 TIMER 없이 WAKE로만 깨어나서, 두 문장이 갈려요.
   - 답에 따라: gaming pair의 "chain stage는 residual class에서 scan과 경쟁한다"는 판단.
3. **editor가 아직 RUN 중일 때 keystroke가 오면 어떻게 되나요?**
   - simulator guide §9.1에 열어 둔 질문 그대로예요: 기억되나(쌓이면 깊이까지), 버려지나.
   - lane을 혼자 써도 keystroke의 31–42%가 이전 burst가 끝나기 전에 도착해서, 드문 경우가 아니에요.
   - 답에 따라: editor의 wait 점수(metrics doc §6.1에서는 task 자신의 occupancy 안에 온 `ready`는 wait 0), guard `tick_count`의 stimulus 개수 대조.
