# 2026-10-30–31의 변동 사항 — simulator 쪽에서 볼 것

> Status: memo · Created 2026-10-30 · Updated 2026-10-31
> From 인지오 to 인경민.

## 0. 이 문서

2026-10-30과 31에 인지오 쪽에서 바뀐 것을 한 곳에 모았어요. simulator가 새로 해야 할 일, simulator는 그대로 두는 결정, harness가 trace를 읽는 방식, 앱 자신의 wake를 출처로 나눈 결정, MLFQ 강등 경계, RQ0 gate spec의 pin 순서로 적었어요.

경민이 2026-10-23에 물은 질문들과 인지오의 답은 `simulator/memo/memo_261023.md` Part H에 있어요. 아래에서 "Part H4"처럼 적으면 그 memo Part H의 네 번째 항목을 말해요.

## 1. 이 문서에서 쓰는 말

- **run file**: simulator의 입력이에요. compile된 workload 파일의 `events`, 곧 task가 도착하는 `arrive` event와 바깥에서 오는 `wake` event의 목록이에요(`docs/data-contracts.md` §4).
- **trace**: simulator의 출력이에요. 한 줄에 event 하나인 JSONL이고, harness는 이것만 읽고 모든 지표를 계산해요(`docs/data-contracts.md` §9).
- **channel**: `WAIT`가 기다리는 이름이에요. 앞부분이 종류예요. `input:<id>`는 키 입력, `timer:<id>`와 `event:<id>`는 측정된 앱 자신의 wake(§5), `chain:`, `job:`, `children:`은 task끼리의 깨움이에요.
- **mailbox**: task가 그 channel에서 기다리고 있지 않을 때 도착한 wake를 붙잡아 두는 곳이에요. 붙잡힌 wake가 있으면, task가 그 channel의 다음 `WAIT`에 닿는 순간 막히지 않고 바로 통과해요.
- **`ready` line**: task가 실행 가능해진 순간을 적는 trace line이에요. `cause`에 이유(`wake`, `timer_tick`, `fork_slot` 등)를 적어요.
- **occupancy**: 한 task가 lane(CPU)을 잡고 있는 구간이에요. `run_start`부터 `run_end`까지예요.
- **blocking primitive**: task를 멈출 수 있는 명령이에요. `WAIT`, `TIMER`, `SLEEP`, 그리고 FORK가 빈 slot을 기다리는 것이에요.
- **RQ0 gate spec**: `harness/experiments/rq0-gate.yaml`이에요. RQ0 실험의 사전 등록 문서예요. 그 안의 `simulator-conformance` 문장은 RQ0 run 전에 simulator가 hand fixture로 보여야 할 동작을 (a)부터 (j)까지 나열해요. 아래의 "conformance 항목 (a)"는 그 목록의 (a)예요.
- **guard spec**: `harness/guards/guard-spec.yaml`이에요. harness가 trace와 run file이 서로 맞지 않을 때 그 run을 거부하는 검사들이에요. 버전이 바뀌면 RQ0 gate spec이 새 버전의 hash를 고정해요.
- **pin**: RQ0 gate spec이 고정하는 파일의 SHA-256이에요. 고정된 파일의 바이트가 바뀌면 harness는 그 spec으로 run을 시작하지 않아요.
- **`T_end`**: run file에 적힌 가장 늦은 시각이에요. 관측 구간의 끝이에요.
- **censored**: 관측 구간 안에서 끝내 처리되지 못한 wake예요. 그 row의 값은 처리 시각을 모르니, task의 끝과 `T_end` 중 이른 쪽까지의 시간을 하한으로 넣고 `censored` 열을 1로 둬요.

## 2. 경민이 할 일

### TL;DR — `simulator/src/sim.cpp`에서 고치고 더할 것

순서는 RQ0 run 전에 끝내야 하는 것부터예요. 자세한 규칙은 아래 2.1–2.4에 있어요.

1. **두 mailbox와 `wake_drop` — conformance 항목 (j), 새 일.** 바뀌는 곳은 channel을 다루는 세 군데예요.
   - **`channel()`** (channel 이름 → index): channel마다 종류를 함께 적어 두세요. 이름이 `timer:`로 시작하는지만 알면 돼요. 새 접두어 `event:`는 `input:`과 똑같이 다루니 지금 코드(`chan_pending_` 계수기, 깊이 제한 없음)를 그대로 써요. 따로 할 일이 없어요.
   - **`on_ext_wake()`** (바깥 wake가 도착할 때): `timer:` channel에서 기다리는 task가 없으면, 붙잡힌 wake가 없을 때만 붙잡아요. 이미 하나가 붙잡혀 있으면 버리고, 그 순간 `{"event":"wake_drop","t":<now>,"task":"<id>","channel":"timer:<id>"}` 한 줄을 써요. `<id>`는 channel 이름의 `:` 뒤예요. task가 아직 도착하기 전에 온 timer wake도 같은 규칙이에요. 처음 것은 붙잡고, 나머지는 그 시각에 `wake_drop`을 써요.
   - **`step()`의 `Op::WAIT`**: task의 k번째 timer `WAIT`는 그 task의 k번째 timer wake와 짝이에요.
     - k번째 wake가 버려진 것이면, 그 `WAIT`와 바로 뒤 `RUN`을 막힘·일·line 없이 건너뛰어요. `RUN`은 다음 명령이 `RUN`일 때만 건너뛰어요. compiler가 run이 0인 wake의 `RUN`을 생략하기 때문이에요.
     - 붙잡힌 것이면 지금처럼 대기 0인 `ready` line을 쓰고 통과해요.
     - 아직 안 왔으면 막혀요.
   - **주의:** 계수기 두 개(붙잡힌 수, 버려진 수)로는 짝이 어긋나요. w1이 붙잡히고 w2가 버려진 채 첫 `WAIT`에 닿을 때와, w1을 소비한 뒤 w3이 붙잡힌 채 둘째 `WAIT`(w2의 짝)에 닿을 때, 두 계수기는 똑같이 (1, 1)인데 해야 할 일은 반대(소비 / 건너뛰기)예요. 그래서 channel마다 "도착한 timer wake 하나하나의 운명(붙잡힘·버려짐·소비됨)"과 "다음 timer `WAIT`의 번호"를 두는 것이 안전해요. harness도 wake 번호로 짝을 맞춰요(`harness/tools/harness/primitives.py`의 `wake_drop` 처리와 `next_wait`).
   - **확인:** `harness/tools/tests/fixtures/mock-wakes/run.json`을 돌린 trace가 같은 폴더의 `trace.jsonl`과 line 단위로 같아야 해요. 지금까지처럼 `steps/`에 새 단계로 두고 `src/sim.cpp`로 옮기면 돼요.
2. **빈 slot을 바로 얻은 FORK의 대기 0 `ready(cause = fork_slot)` line — 항목 (a)의 마지막 경우, Part H4.** `step()`의 `Op::FORK`에서 slot이 남아 바로 `spawn()`하는 갈래에 그 line을 더해요. 그다음 `fix-object`와 `fix-tree`의 `reference-trace.jsonl`을 다시 만들어요(2.2).
3. **RUN 끝의 drain — Part H5.** 기다리는 config switch(U3의 `pending_`, `dispatch()`)를, occupancy 안에서 RUN이 끝나는 순간에도 slice가 끝날 때와 똑같이 적용해요. FIFO에서 나가는 switch는 지금처럼 즉시 적용해요(2.3).
4. **`WAIT children:<id>` — 항목 (g).** 지금은 보통 channel처럼 영원히 막혀요. 그 orchestrator가 spawn한 자식이 모두 끝나면 완료되고, `WAIT`에 닿을 때 살아 있는 자식이 없으면 막히지 않고 대기 0으로 바로 완료되게 해요(2.4).
5. **invocation contract — 항목 (h).** `main()`의 `--workload`, `--schedule`, `--out-trace`, gzip, 다 쓴 경우에만 exit 0은 이미 있어요. 남은 것은 둘이에요. trace header의 `"sim"`이 지금 `"src/sim"`으로 고정이라 runner machine 설정에 적힌 version 문자열로 바꿔야 하고, 미뤄 둔 위치 인자 거부가 있어요(2.4).
6. **회귀 기준선.** core set, sensitivity variant, generated layer가 2026-10-31에 다시 build됐어요. 51개 파일 모두 바뀌었어요(`event:` channel, operation 창 시작의 큰 run). 기존 byte-identical 기준선은 새 build(dataset manifest `27d347bc…`)로 다시 잡아야 해요.

### 2.1 두 channel의 mailbox와 `wake_drop` (새 일)

측정된 앱 자신의 wake가 이제 두 channel로 나뉘어 와요(§5). simulator는 channel 종류에 따라 mailbox를 다르게 다뤄야 해요.

- **`event:<id>`는 `input:<id>`와 똑같이 다뤄요.** 붙잡힌 wake는 깊이를 가지고 쌓여요. wake 셋이 쌓이면 다음 `WAIT` 셋이 차례로 바로 통과해요. 지금 키 입력을 다루는 코드를 그대로 쓰면 돼요.
- **`timer:<id>`의 mailbox는 wake를 하나만, 처음 것만 붙잡아요.**
  - task가 timer channel에서 기다리지 않을 때 timer wake가 오면, mailbox가 비어 있으면 붙잡아요.
  - 이미 하나가 붙잡혀 있으면 새 wake는 **버려요(drop)**. 버리는 순간, 그 wake의 시각으로 trace line 하나를 써요.

    ```jsonc
    {"event":"wake_drop", "t":1250000, "task":"editor", "channel":"timer:editor"}
    ```

  - 버려진 wake에도 compile된 `WAIT`와 그 뒤의 `RUN`이 program 안에 자리를 지키고 있어요. task의 timer channel `WAIT`는 run file의 그 task timer wake와 시각 순서대로 하나씩 짝을 이뤄요. k번째 timer `WAIT`의 짝은 k번째 timer wake예요.
  - program이 버려진 wake의 `WAIT`에 닿으면, 그 `WAIT`와 뒤의 `RUN`을 바로 지나가요. 막히지도 않고, 일도 하지 않고, line도 쓰지 않아요. `ready` line도 occupancy도 없어요.
  - 붙잡힌 wake의 `WAIT`는 키 입력과 똑같이, program이 닿는 순간 막히지 않고 통과하며 대기 0인 `ready` line을 써요.
- **conformance.** RQ0 gate spec의 `simulator-conformance`에 항목 (j)로 들어갔어요. 내용은 위의 두 mailbox와 `wake_drop`이에요. 항목 (a), 곧 "blocking primitive가 끝날 때마다 `ready` line"에는 예외가 하나 생겼어요. 버려진 timer wake의 `WAIT`와 `RUN`은 line 없이 지나가요.
- **(j)를 보일 hand fixture.** `harness/tools/tests/fixtures/mock-wakes/`예요. 측정된 앱 하나에 timer wake 셋이 RUN 하나 동안 와요. 첫째는 처리되고, 둘째는 붙잡혀 있다가 대기 0으로 처리되고, 셋째는 버려져요. event wake 둘은 쌓였다가 차례로 처리돼요. `run.json`을 simulator로 돌린 trace가 `trace.jsonl`과 line 단위로 같으면 (j)를 보인 거예요. 순간마다 일어나는 일과 records는 `worked.md`에 손으로 풀어 두었어요.
- **trace 계약.** `wake_drop`은 trace의 여덟 번째 runtime event예요(`docs/data-contracts.md` §9). harness의 reader는 이 line을 이미 읽어요. 계약 변경 기록은 `docs/data-contracts.md` §14의 2026-10-31 항목에 있어요.
- harness의 mock simulator는 `mock-simulator@3`부터 이렇게 해요(`harness/tools/tests/mocks/simulator.py`). 한 순간에 같은 task로 timer wake가 여럿 오면, 첫째는 task가 막혀 있던 `WAIT`를 완료하고, 둘째는 붙잡혀 같은 run 안에서 다음 `WAIT`를 완료하고, 셋째부터 버리고 `wake_drop`을 써요. 등장 전에 온 timer wake도 처음 하나만 붙잡아요.

### 2.2 빈 slot을 바로 얻은 FORK의 line (Part H4)

FORK가 빈 slot을 바로 얻어 막히지 않았을 때도, 대기 0인 `ready(cause = fork_slot)` line을 써요. `harness/tools/tests/fixtures/`의 `fix-object`와 `fix-tree`에 있는 `reference-trace.jsonl`도 그에 맞춰 다시 만들어야 해요. 두 fixture는 build의 job tree가 spawn table의 자식을 깨우는 동작(conformance 항목 (i))을 보이는 파일이에요. 이 line이 conformance 항목 (a)에서 simulator가 아직 하지 않는 마지막 경우예요.

### 2.3 RUN 끝의 drain (Part H5)

drain은 algorithm switch가 지금 lane을 잡은 task의 slice나 RUN이 끝날 때까지 기다렸다가 적용되는 것을 말해요. occupancy 안에서 RUN이 끝나는 순간에 drain이 걸려 있으면, slice가 끝날 때와 똑같이 처리해요. switch가 적용되고, lane을 잡고 있던 task는 ready set으로 돌아가요. 새 algorithm은 그 task까지 포함해서 다음 task를 고르고, 다른 task를 고르면 `run_end(reason = preempt)`를 써요. FIFO에서 나가는 switch의 규칙 (a), 곧 즉시 적용은 그대로예요.

### 2.4 그대로 남은 항목 (g)와 (h)

- (g): build 부모의 `WAIT children:<id>`는 자기가 spawn한 자식이 모두 끝나면 완료돼요. 그 순간 살아 있는 자식이 없으면 막히지 않고 바로 완료되며, 대기 0인 `ready` line을 써요. 경민이 말로 동의한 규칙이에요(2026-10-31 기록).
- (h): runner가 simulator를 부르는 방식(invocation contract)이에요. `--workload`, `--schedule`, `--out-trace` flag를 쓰고, 위치 인자는 없어요. trace는 그 경로에 쓰고, 쓴 경우에만 exit 0이에요. 같은 인자면 바이트까지 같은 trace를 내고, trace header의 `sim`은 runner machine 설정에 적힌 version 문자열이어야 해요.

## 3. simulator는 그대로 두는 결정

- **stimulus guard (Part H2).** stimulus guard는 task가 받은 wake와 trace의 `ready` line 수를 맞춰 보는 harness 검사예요.
  - input `ready` line이 input wake보다 적은 것만으로는 guard가 걸리지 않아요. task가 program에서 뒤처져 아직 처리하지 못한 키 입력일 수 있으니까요.
  - guard가 걸리는 경우는 둘이에요. 하나는 task가 input `WAIT`에 막힌 채 끝났는데, 그보다 먼저 보낸 input wake가 소비되지 않은 경우예요. 곧 잃어버린 wake예요. 다른 하나는 input line이 input wake보다 많은 경우예요.
  - guard spec은 1.3을 거쳐 1.4가 됐어요. 1.4는 같은 검사를 `event:` channel에 그대로 하고, `timer:` channel에서는 모든 timer wake가 처리(`ready` line)와 버림(`wake_drop` line) 중 정확히 하나를 가져야 한다고 봐요. 둘 다 없는 wake, 붙잡힌 wake가 없는데 버려진 wake, run file에 없는 wake를 버린 line은 guard예요.
- **MLFQ allotment (Part H3).** allotment는 한 queue level에서 쓸 수 있는 CPU 시간이에요. 한 level에서 쓴 시간은 block이나 preempt 뒤에도 남아서, 다음 boost(모든 task를 맨 위 level로 올리는 주기적 재설정)까지 쌓여요. OSTEP §8.4의 Rule 4가 그렇게 말하고, simulator가 이미 그렇게 해요. simulator guide §5 rule 4, `mock-p1a`, fixture 설명은 인지오가 이 규칙에 맞췄어요. 이 규칙이 harness 쪽 숫자에 미친 영향은 §6에 있어요.
- **일이 없는 job (Part H6).** `TIMER` 바로 뒤에 `TIMER`가 오면, simulator는 다음 `TIMER`에 닿는 순간 `deadline` line을 써요. 이 line은 그대로 둬요. 대신 harness 쪽이 바뀌었어요. 그런 job은 tick이 소비될 때 값 0으로 끝나요. 또 `ready` line 다음에 `run_start` 없이 다음 `ready` line이 오면, 앞 line을 대기 0으로 읽어요.
- **`fork_cap`이 1보다 작을 때 (Part H7).** loader가 거부하는 것이 맞아요. workload schema가 `"minimum": 1`이에요.

## 4. harness가 trace를 읽는 방식

- **`input_latency`.** 키 입력 하나마다 row 하나예요. run file의 키 입력 시각부터 그 키 입력의 처리를 시작한 시각까지를 재요. 처리를 시작한 시각은, 그 키 입력에 짝지어진 `ready` line이 occupancy 안이면 line 자신의 시각이고, 아니면 다음 `run_start`예요. 끝내 처리되지 못한 키 입력은 censored row예요(§1). records의 26번째 열이 `censored`예요.
- **`app_latency`.** 2026-10-30의 `timer_latency`를 이 이름으로 바꾸고 두 channel로 넓혔어요(`docs/harness/metrics.md` §6.13). 앱 자신의 `timer:`와 `event:` wake 하나마다 row 하나이고, row에 `channel`(`timer` 또는 `event`)을 적어요.
  - `event:` wake는 `input_latency`와 같은 규칙이에요.
  - 처리된 `timer:` wake도 같은 규칙이에요.
  - 버려진 timer wake는, 그 wake가 왔을 때 mailbox에 붙잡혀 있던 wake의 처리 시작까지를 재고 `skipped`를 1로 둬요. 그 붙잡힌 wake가 버려진 wake의 몫까지 처리한 셈이니까요.
  - 키 입력이 없는 앱(Kdenlive, GIMP, `c7-mail`의 mailer 등)의 scoring spec term 15개가 이 row의 P99를 읽어요. 두 channel을 합쳐서요.
- **per-switch excess.** MLFQ로 switch한 직후 구간에서 interactive task가 겪은 지연의 초과분이에요. 그 task의 term이 읽는 지연(`input_latency` 또는 `app_latency`)으로 재요.

## 5. 앱 자신의 wake를 출처로 나눈 결정 (2026-10-31)

### 5.1 왜 이 결정이 필요했나

측정된 앱의 component는 thread별 kernel wakeup이에요. 지금까지는 그 wake를 모두 `timer:` channel에 compile했고, simulator는 그것을 키 입력처럼 mailbox에 쌓았어요. 그런데 측정된 wake의 원인은 섞여 있어요.

- 앱의 toolkit timer는 밀린 발화를 쌓지 않고 한 번만 내요. Qt(`qt-qtimer`), GLib(`glib-timeout`), Gecko(`gecko-nsitimer`)의 문서가 그렇게 말해요.
- X 입력 event(`xlib-xnextevent`)와 다른 thread가 보낸 Qt event(`qt-postevent`)는 queue에 쌓여요.
- 출처는 모두 `docs/references.md`에 원문으로 확인해 두었어요.

그래서 RQ0 run 전에, 인지오가 측정 때 남긴 raw wakeups 파일로 wake를 원인별로 나눴어요. 결정 18개와 근거는 `_dev/docs/spec/jioh/timer-wakes-by-origin.md`에, 측정은 `_dev/research/jioh/2026-10-31-wake-origins/`에 있어요.

### 5.2 결정들

1. **원인으로 나눠요.** toolkit timer가 원인인 wake는 task가 기다리지 않을 때 쌓지 않아요. 입력이나 다른 thread·process의 메시지가 원인인 wake는 키 입력처럼 쌓아요.
2. **timer channel은 처음 wake 하나만 붙잡아요.** 이미 하나가 붙잡혀 있으면 새 wake는 버리고, 그 wake의 `WAIT`와 `RUN`은 일 없이 지나가요(§2.1). 붙잡힌 wake의 지연은 그 wake 자신의 도착부터 재요.
3. **버려진 wake도 지연 row를 가져요.** 값은 그것을 덮은 처리의 시작에서 자신의 도착을 뺀 것이고, `skipped`로 표시해요(§4).
4. **새 channel 종류 `event:<id>`.** timer가 원인인 wake는 `timer:<id>`에 남고, 쌓이는 나머지 wake는 `event:<id>`로 가요. 키 입력은 `input:<id>` 그대로예요.
5. **simulator가 버리는 순간 `wake_drop`을 써요.** 버려진 wake의 짝은 나중에 line 없이 지나가요. 이것이 conformance 항목 (a)의 예외예요.
6. **앱의 모든 wake 출처를 나눠요.** component, focus component(포인터 조작 구간의 component), operation(측정된 작업 구간), launch stream(앱 실행 구간을 측정 그대로 재생하는 stream), trace replay stream(측정 trace를 그대로 재생하는 변형), heavy event(드문 긴 run) 모두예요. launch와 replay stream은 wake마다 channel을 네 번째 열로 실어요(0 timer, 1 event). 이 일은 compile 때 끝나니, simulator는 두 channel의 `wake` event를 받기만 해요.
7. **term 15개는 두 channel을 함께 읽어요.**
8. **`timer:`로 가는 것은 timer가 원인인 wake뿐이에요.** wake의 원인은 wake chain의 시작이에요. wakeup event를 시각 순서로 따라가면서, 앱 tree의 thread가 깨운 wake는 그 thread 자신의 마지막 wake의 원인을 물려받아요. X 서버도 같은 식으로 원인을 전달해요. chain이 idle CPU의 timer interrupt에서 시작하면 timer가 원인이에요. 측정의 입력 재생, 원인이 기록에 없는 X 서버, 다른 process, kernel thread, 기록 안에서 아직 깨어난 적 없는 thread는 모두 `event:`로 가요. Chrome과 VS Code는 측정 snapshot에 X 서버가 없어서, 처음에는 X 서버를 거친 wake가 모두 출처 미상으로 읽혔어요. 지금은 snapshot과 상관없이 X 서버 자신의 wake를 따라가요.
9. **operation도 같은 규칙이에요.** 측정 driver가 앱으로 들어가는 길은 입력으로 세요. xdotool과 driver process, 그리고 driver가 GIMP의 unsharp mask를 실행할 때 거치는 GIMP의 Script-Fu server예요.
10. **component를 둘로 나누고, coverage cut을 channel마다 해요.** 모든 component를 timer 부분과 나머지 부분으로 나누고, 각 부분의 gap 표와 run 표를 그 부분의 wake로 다시 만들어요. coverage cut(9.5 D16: wake 비율이 큰 component부터 wake의 95 %까지 고르고 나머지를 residual 하나로 묶는 규칙)은 channel 안에서 따로 해요. library에서 event 부분은 `channel: event`를 달아요.
11. **primitive 하나, `app_latency`.** §4예요.
12. **stimulus guard가 두 channel을 다뤄요(guard spec 1.4).** §3이에요.
13. **desktop과 session campaign의 task도 똑같이 나눠요.** `renderer-hidden`, `chat-client`, `game-client`, session daemon(`compositor-shell`, `audio-server`, `service-manager`, `message-bus`)이에요.
14. **안정성 규칙을 통과하지 못하는 event 부분은 반폭을 밝힌 채 실어요.** 안정성 규칙(9.5 D26, D30, D78)은 entry가 싣는 모든 값의 95 % 반폭이 반복 간 5 % 이내여야 한다는 규칙이에요. 나눈 뒤 작아진 event 부분 몇 개가 이 규칙을 통과하지 못해요. 이런 부분은 증거가 맞는 기존 범주로 실어요. 세션마다 수준이 다른 경우(9.5 D57), 퍼짐의 일부가 한 실행 안에 있는 경우(9.8 D21이 D57을 넓힌 범주), phase당 몇 번만 깨는 드문 component(9.8 D27)예요. 각 entry의 scope에 두 퍼짐, phase당 wake 수, 값이 실패하는 것을 본 뒤 정했다는 순서(9.8 D28)를 적어요.
15. **`video-editor`의 포인터 phase main thread timer 부분 run mean은 9.8 D17로 실어요.** runner마다 CPU 속도가 달라 run 시간이 함께 움직이는 경우의 범주예요.
16. **`audio-server`의 `wireplumber/gmain` timer 부분은 결정 14의 규칙으로 실어요.**
17. **operation마다 측정한 조작별 가장 큰 run을 창마다 한 번 실어요.** 측정한 조작 하나하나에는 가장 큰 run이 하나 있어요. GIMP unsharp mask는 조작 CPU 2,443 ms(중앙값) 가운데 2,434 ms가 필터의 run 하나예요. 이 run을 component의 wake 하나로 두면 창 안에 들어갈지가 뽑기에 달려서, 다시 build했을 때 `c1-photo`, `c7-photo`, `c3-creation`의 unsharp mask 창에서 필터 run이 빠졌어요(창 안 CPU 2.49 s → 0.33 ms). 그래서 operation 넷(unsharp mask, 메일 보내기, page load, preview render) 모두 이 run을 따로 표로 두고, operation 창이 열리는 순간 `event:` wake 하나로 실어요. 창의 나머지 wake는 그 run을 뺀 component로 뽑아요. simulator에게 바뀌는 것은 없어요. 그 run도 `event:` channel의 `wake` event와 `WAIT`·`RUN`이에요.
18. **GIMP operation의 남은 값 셋은 반폭을 밝힌 채 실어요.** 결정 17로 필터 run을 떼고 나니, GIMP operation의 남은 `gimp` event 부분의 세 값이 repeat 5개에서 안정성 규칙을 넘지 못했어요. repeat를 더 측정했더니 GitHub runner의 kernel이 바뀌어 있었어요(`6.17.0-1022-azure` → `7.0.0-1017-azure`). 새 kernel에서는 unsharp mask가 약 20 % 길어서(repeat 평균 2,823–2,861 ms, 옛 repeat는 2,342–2,396 ms), 같은 조건으로 repeat를 더할 수 없어요. 그래서 녹음 창이 바닥난 값을 다루는 9.5 D46처럼 반폭과 함께 싣고, 새 kernel의 repeat 6개는 증거로만 남겨요(pool에는 넣지 않아요).

### 5.3 나눈 결과

wake chain의 시작으로 본 몫이에요(wake 수 기준 / CPU 기준).

- 문서 편집기, VS Code, Chrome, Thunderbird의 idle phase는 거의 모두 timer가 원인이에요(0.99–1.00).
- GIMP의 포인터 phase는 입력이 0.73, Kdenlive의 포인터 phase는 timer가 0.89예요.
- 측정된 작업은 대부분 입력이 원인이에요. GIMP unsharp mask 0.85, Kdenlive preview render 0.99, Chrome page load 0.64, Thunderbird 메일 보내기 0.40(timer 0.59)이에요.
- library에서 event 몫이 큰 entry는 `chat-client`(Element, idle wake의 절반 넘게)이고, `service-manager`(systemd)와 `message-bus`(dbus-daemon)는 component 전부가 event 부분이에요.
- core set 51개 파일의 wake는 모두 4,504,773개이고, 키 입력 25,745개, `timer:` 4,146,411개, `event:` 332,617개예요.

## 6. MLFQ 강등 경계와 boot default sweep

Part H3의 규칙에서는 한 level에서 쓴 CPU가 burst를 넘어 다음 boost까지 쌓여요. 그래서 주기 task가 맨 위 queue에서 강등되는 경계는 "한 burst의 run이 slice보다 긴가"가 아니라, boost 구간 100 ms 동안 그 level에서 쓰는 CPU예요. RQ0 gate spec, scoring spec, driver table의 숫자가 예전 읽기로 적혀 있어서 다시 고쳤어요. 인지오가 reference simulator(commit `8dab1176`)의 trace로 확인했어요(`_dev/research/jioh/2026-10-31-demotion-edges/`).

- **100 ms당 CPU로 본 경계.** music player 0.71 ms, gaming chain의 task 1.7–8.6 ms, video player 12.1 ms, 화상 통화 23.9 ms예요. 두 앱을 함께 띄운 C2 pair 파일들에서는 gaming chain이 1.6–12.7 ms예요.
- **primary의 10 ms slice에서.** primary는 실험의 기본 boot 설정이에요. 통화는 boost 구간의 98 %에서 강등돼요(예전 읽기로는 열에 넷쯤). video player는 89 %예요(예전 읽기로는 거의 0). gaming chain은 강등되지 않아요.
- **sweep 지점.** boot default sweep은 boot 설정의 slice 값을 바꿔 가며 결과가 얼마나 흔들리는지 보는 민감도 검사예요. 강등 경계를 겨냥한 지점은 900 µs, 3 ms, 14 ms 대신 7 ms, 12 ms, 30 ms가 됐어요. 1.2 ms와 5 ms는 그대로예요. 나머지 지점(500 µs, 700 µs, 2 ms, 20 ms, 100 ms)은 값을 그대로 두고 설명만 고쳤어요. `harness/boot-defaults/`의 파일도 그에 맞춰 바뀌었어요.
- **`c7-meeting`(통화 파일).** 고정 설정에서 통화는 boost 구간의 97 %에서 강등되고, job의 20 %를 놓쳐요. EDF에서는 통화 자신의 초과 실행 몫인 약 5 %만 놓쳐요.
- **`c7-media`(video와 music 재생 파일).**
  - 고정 설정에서 video player는 boost 구간의 88 %에서 강등되지만, 어느 player도 job을 놓치지 않아요.
  - 예전 노트의 "최악 32 ms, 여유 1.3 ms"는 계산이 틀렸어요. 측정된 표의 최악 cycle 16.0 ms에 두 번째 queue의 slice 20 ms 대기를 더하면 36 ms라서 33.3 ms 주기를 넘어요.
  - 그래서 이 파일에서 recognizer가 개선할 여지가 없다는 판단은, compile된 파일 자체에 기대요. 그 파일의 최악 cycle은 7.28 ms예요.
- **driver table.** MLFQ 문장이 OSTEP §8.4의 Rule 4를 인용하도록 바뀌었어요. 가벼운 앱 셋(browser, 문서 편집기, 메일)은 "대부분 맨 위 queue에 남는다"로 적었어요. 고정 설정에서 boost 구간의 0.04–0.06에서만 강등되기 때문이에요. 값은 그대로예요.

이 절에서 경민이 할 일은 없어요.

## 7. pin

RQ0 gate spec은 지금 이 파일들에 고정돼요.

- scoring spec `4f3e34c1…`
- guard spec 1.4 `7d79201d…`
- driver table `36267c38…`
- dataset manifest `27d347bc…`, variants manifest `de9802e7…`(core set, sensitivity variant, generated layer를 다시 빌드했어요)

## 8. 축소 RQ0 spec

`harness/experiments/rq0-reduced.yaml`을 지웠어요(commit `b44fed5c`). 이유는 둘이에요.

- `harness/experiments/`는 사전 등록된 실험만 두는 곳이에요(그 디렉터리의 README). harness의 runner 테스트도 이 규칙을 확인해요.
- 그 파일의 pin은 guard spec 1.2와 예전 scoring spec이라, 지금의 spec과 맞지 않아요.

리허설 run은 smoke run처럼, 실행할 때 spec을 임시 디렉터리에 만들어 쓰면 돼요. 지운 파일은 git history에 남아 있어요.
