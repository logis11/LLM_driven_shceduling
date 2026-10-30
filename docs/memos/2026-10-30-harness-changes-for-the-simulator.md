# 2026-10-30–31의 변동 사항 — simulator 쪽에서 볼 것

> Status: memo · Created 2026-10-30 · Updated 2026-10-31
> From 인지오 to 인경민.

## 0. 이 문서

2026-10-30과 31에 인지오 쪽에서 바뀐 것을 한 곳에 모았어요. 순서는 이래요.

- 경민이 할 일
- simulator는 그대로인 결정
- harness가 trace를 읽는 방식의 변화
- MLFQ 강등 경계와 boot default sweep
- pin
- 축소 RQ0 spec
- 앞으로 닿을 일

경민의 질문에 대한 답 하나하나의 근거는 `simulator/memo/memo_261023.md` Part H에 있어요.

## 1. 경민이 할 일

- **빈 slot을 바로 얻은 FORK의 line (Part H4).** 이 FORK도 대기 0인 `ready(cause = fork_slot)` line을 써요. `harness/tools/tests/fixtures/`의 `fix-object`와 `fix-tree`에 있는 `reference-trace.jsonl`도 다시 만들어야 해요. RQ0 gate spec의 conformance 항목 (a), 곧 "blocking primitive가 끝날 때마다 `ready` line"에서 남은 경우는 이것 하나예요.
- **RUN 끝의 drain (Part H5).** occupancy 안에서 RUN이 끝나는 순간에 drain이 걸리면, slice 끝에서처럼 적용해요. switch가 적용되고, holder는 ready set으로 돌아가요. 새 algorithm은 holder까지 포함해서 다음 task를 고르고, 다른 task를 고르면 `run_end(reason = preempt)`를 써요. FIFO에서 나가는 경우의 규칙 (a)는 그대로예요.
- **conformance (g)와 (h)는 그대로 남아 있어요.**
  - (g): build parent의 `WAIT children:<id>`는 자기가 spawn한 자식이 모두 끝나면 완료돼요. 그 시점에 살아 있는 자식이 없으면 block 없이 완료돼요.
  - (h): runner가 부르는 invocation contract예요. `--workload`, `--schedule`, `--out-trace` flag를 쓰고, trace header의 `sim`은 runner machine 설정의 version 문자열이어야 해요.
- **회신 두 개.** 하나는 declared-class memo §4 item 4의 공식 회신이에요. 다른 하나는 data contracts §14가 제안한 (g)에 대한 동의예요.

## 2. simulator는 그대로인 결정

- **stimulus guard (Part H2).**
  - input `ready` line이 input wake보다 적다고 해서 guard message가 나오지는 않아요.
  - message가 나오는 경우는 둘이에요. 하나는 task가 input WAIT에 막힌 채 끝났는데, 그보다 먼저 보낸 input wake가 소비되지 않은 경우예요. 곧 잃어버린 wake예요. 다른 하나는 input line이 input wake보다 많은 경우예요.
  - guard spec은 1.3이 됐어요.
- **MLFQ allotment (Part H3).** 한 level에서 쓴 시간은 block이나 preempt 뒤에도 남아요. OSTEP §8.4의 Rule 4가 그렇게 말하고, simulator가 이미 그렇게 해요. simulator guide §5 rule 4, `mock-p1a`, fixture 설명은 인지오가 이 규칙에 맞췄어요. 이 규칙이 harness 쪽 숫자에 미친 영향은 §4에 있어요.
- **일이 없는 job (Part H6).** TIMER 바로 뒤에 TIMER가 오면, simulator는 다음 TIMER에 닿는 순간에 `deadline` line을 써요. 이 line은 그대로 둬요. 대신 harness 쪽이 바뀌었어요. 그런 job은 tick이 소비될 때 값 0으로 끝나요. 또 `ready` line 다음에 `run_start` 없이 다음 `ready` line이 오면, 앞 line을 대기 0으로 읽어요.
- **`fork_cap`이 1보다 작을 때 (Part H7).** loader가 거부하는 것이 맞아요. schema의 `"minimum": 1`이에요.

## 3. harness가 trace를 읽는 방식

trace 형식은 바뀌지 않았어요. 바뀐 것은 harness가 trace를 읽는 방식이에요.

- **`input_latency`.** keystroke 하나마다 row 하나예요. run file의 keystroke 시각부터 그 keystroke를 처리하기 시작한 시각까지를 재요. 처리를 시작한 시각은 그 keystroke에 짝지어진 `ready` line이 occupancy 안이면 line 자신의 시각이고, 아니면 다음 `run_start`예요. 끝내 처리되지 못한 keystroke는 task의 끝과 `T_end` 중 이른 쪽까지의 하한으로 넣고, records의 새 26번째 열 `censored`를 1로 둬요.
- **`timer_latency`.** 같은 규칙을 앱 자신의 timer channel wake에 써요. keystroke stream이 없는 앱(Kdenlive, GIMP, `c7-mail`의 mailer)의 term 15개가 이것을 읽어요.
- **per-switch excess.** MLFQ로 switch한 직후의 구간에서 interactive task가 겪은 지연의 초과분이에요. 이제 그 task의 term이 읽는 지연(`input_latency` 또는 `timer_latency`)으로 재요.

## 4. MLFQ 강등 경계와 boot default sweep

Part H3의 규칙에서는 한 level에서 쓴 CPU가 burst를 넘어 다음 boost까지 쌓여요. 그래서 주기 task의 강등 경계는 "한 burst의 run이 slice보다 긴가"가 아니라, boost 구간 100 ms 동안 쓰는 CPU예요. RQ0 gate spec, scoring spec, driver table의 숫자가 예전 읽기로 적혀 있어서 다시 고쳤어요. 인지오가 reference simulator(`8dab1176`)의 trace로 확인했어요(`_dev/research/jioh/2026-10-31-demotion-edges/`).

- **100 ms당 CPU 기준의 경계.** music player 0.71 ms, gaming chain의 task 1.7–8.6 ms(C2 pair는 1.6–12.7 ms), video player 12.1 ms, 통화 23.9 ms.
- **primary 10 ms에서.** 통화는 boost 구간의 98 %에서 강등돼요(예전 읽기로는 열에 넷쯤). video player는 89 %예요(예전 읽기로는 거의 0). gaming chain은 강등되지 않아요.
- **sweep 지점.** threshold 지점은 900 µs, 3 ms, 14 ms 대신 7 ms, 12 ms, 30 ms가 됐어요. 1.2 ms와 5 ms는 그대로예요. backbone 지점(500 µs, 700 µs, 2 ms, 20 ms, 100 ms)은 값을 그대로 두고 설명만 고쳤어요. `harness/boot-defaults/`의 파일도 그에 맞춰 바뀌었어요.
- **`c7-meeting`.** 고정 설정에서 통화는 boost 구간의 97 %에서 강등되고, job의 20 %를 놓쳐요. EDF에서는 자기 overrun인 약 5 %만 놓쳐요.
- **`c7-media`.**
  - 고정 설정에서 video player는 boost 구간의 88 %에서 강등되지만, 어느 player도 job을 놓치지 않아요.
  - 예전 노트의 "최악 32 ms, 여유 1.3 ms"는 산수가 틀렸어요. 측정된 표의 최악 cycle 16.0 ms에 Q1 slice 20 ms 대기를 더하면 36 ms라 33.3 ms 주기를 넘어요.
  - 그래서 headroom이 없다는 판단은 compile된 파일에 기대요. 그 파일의 최악 cycle은 7.28 ms예요.
- **driver table.** MLFQ 문장이 OSTEP §8.4의 Rule 4를 인용하도록 바뀌었어요. 가벼운 editor 셋(browser, 문서 편집기, 메일)은 "대부분 위에 남는다"로 적었어요. 고정 설정에서 boost 구간의 0.04–0.06에서 강등되기 때문이에요. 값은 그대로예요.

경민이 할 일은 없어요.

## 5. pin

RQ0 gate spec은 이 파일들에 고정돼요. dataset의 pin은 그대로예요.

- scoring spec `84b997ad…`
- guard spec 1.3 `7029308e…`
- driver table `36267c38…`

## 6. 축소 RQ0 spec

`harness/experiments/rq0-reduced.yaml`을 지웠어요(`b44fed5c`). 이유는 이래요.

- `harness/experiments/`는 pre-registered 실험만 두는 곳이에요(그 디렉터리의 README). `test_runner`도 이 규칙을 확인해요.
- 그 파일의 pin은 guard spec 1.2와 예전 scoring spec이라, 지금의 spec과 맞지 않아요.

리허설 run은 smoke run처럼 실행할 때 spec을 임시 디렉터리에 만들어 쓰면 돼요. 지운 파일은 git history에 남아 있어요.

## 7. 앞으로 닿을 일

- **timer wake를 쌓을지 건너뛸지.**
  - 지금 simulator는 `timer:` channel의 wake를 keystroke처럼 mailbox에 쌓아요.
  - 그런데 측정된 timer component는 thread별 kernel wakeup이에요. 원인은 timer, X 입력, 다른 thread의 깨움이 섞여 있어요.
  - kernel은 잠들어 있지 않은 task의 wakeup을 쌓지 않아요(`linux-sched-ttwu`). Qt, GLib, Gecko의 timer는 밀린 발화를 건너뛰어요(`qt-qtimer`, `glib-timeout`, `gecko-nsitimer`). 반면 X 입력 event는 쌓여요(`xlib-xnextevent`). 다섯 출처 모두 `docs/references.md`에 있어요.
  - 그래서 인지오가 측정 때 남긴 raw wakeups 파일로 wake를 원인별로 먼저 나눌 거예요. 그다음 timer가 원인인 부분에 `WAIT(timer)`의 skip rule을 interpretation contract에 제안할 거예요. simulator 작업은 그때 생겨요. 지금은 할 일이 없어요.
  - RQ0 run 전에 해요(2026-10-30 결정). 판정 파일 19개 중 7개의 foreground term이 timer wake를 읽기 때문이에요. 경민의 (g), (h)와 나란히 진행해요.
