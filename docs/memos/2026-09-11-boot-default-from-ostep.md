# Boot default 변경 안내 — MLFQ 기본값을 OSTEP 예시 그대로, slice 2 ms에서 10 ms로

> Status: memo · Created 2026-09-11 · Updated 2026-09-11
> From 인지오 to 인경민, 박이안. scheduler의 **boot default configuration**(모든 config schedule의 t = 0 entry이자 `fixed` condition)의 값을 바꿨어요. 이 memo는 왜 바꿨는지, 무엇이 얼마로 바뀌었는지, 그리고 simulator와 daemon 쪽에 무엇이 달라지고 무엇이 그대로인지를 적어요. 규범 문서는 §8에 링크했어요. 급하면 §1과 §5만 읽어도 돼요. §5에 인경민께 여쭤볼 질문 두 개가 있어요.

## 1. 한 문단 요약

boot default의 MLFQ slice가 2 ms였는데, 이 값의 출처가 없었어요. 다른 세 값(queue 3개, level마다 slice 2배, 100 ms마다 boost)은 OSTEP 교재의 예시와 같은데 slice만 어디서도 안 나오는 숫자였어요. 그래서 조사를 했고(§3), "MLFQ의 표준 설정"이라는 건 어느 문헌에도 없다는 걸 확인한 뒤, **OSTEP 8장의 예시 설정을 통째로** boot default로 삼기로 했어요: queue 3개, **slice 10 ms**, level마다 2배, boost 100 ms. EDF의 residual slice와 LOTTERY의 slice는 "MLFQ slice와 같게"라는 우리 규칙을 그대로 따라 **둘 다 10 ms**가 됐어요. 바뀐 건 숫자 세 개뿐이고, **contract(schedule·trace·log의 형식, config schema의 field와 범위)는 하나도 안 바뀌었어요.** daemon이 상황마다 골라 내려보내는 config 목록(driver table — 상황 하나에 config 하나, 32개)도 "params는 boot 값"이라는 자기 규칙대로 같이 바뀌었어요.

## 2. 왜 바꿨나

harness의 채점은 모든 조건을 `fixed`(= boot default) 대비 얼마나 나아졌나로 재요. 그러니까 boot default는 **모든 숫자의 바닥**이에요. 그 바닥의 값 하나가 "어디서 왔는지 모르는 숫자"면, 결과를 누가 물어봤을 때 답을 못 해요.

2 ms는 2026-08-28에 config schema를 freeze할 때 들어간 값이고, 2026-09-07에 기본값 일곱 개의 출처를 점검했을 때 "OSTEP는 최상위 queue에 10 ms 이하, Linux는 0.75 ms, Solaris는 20 ms — 2 ms는 그 사이 어딘가"라고만 적을 수 있었어요. 범위 안에 있다는 것과 출처가 있다는 건 달라요.

바꾸는 원칙은 하나예요: **한 알고리즘의 params는 한 출처에서.** 네 값을 각각 다른 데서 가져와 붙이면 네 개의 주장이 되고, 하나하나 따로 공격받아요. 한 교재의 예시를 통째로 쓰면 "우리는 OSTEP의 MLFQ를 돌렸다"는 한 문장이 돼요.

## 3. 조사 결과 — 표준은 없다

2026-09-11에 원문을 직접 읽어 확인한 것만 적어요. 기억으로 쓴 숫자는 없어요.

**"표준 설정"이라고 말하는 문헌은 없어요.** OSTEP 자신이 "queue를 몇 개로, slice를 얼마로, boost를 얼마나 자주 할지에는 쉬운 답이 없고, workload 경험과 tuning으로만 정해진다"고 써요. Solaris TS의 dispatch table을 다룬 Arpaci-Dusseau의 강의 노트는 "사실 이 표를 잘 설정하는 법은 아무도 모른다"고 해요. 교과서들(Silberschatz, Stallings)은 예시 숫자만 주고, 논문들은 "slice를 level마다 2배로 하는 게 관례"라고만 해요.

**실제로 출하된 table 기반 MLFQ는 둘뿐이고, 둘 다 우리 schema에 안 들어가요.**

| system | level 수 | slice | boost/aging |
|---|---|---|---|
| illumos / Solaris TS (기본 table, hz = 1000) | 60 | 최상위 2 ms → 최하위 20 ms, 계단식 | thread마다 1초에 한 번 나이 먹여 50–59 level로 올림 |
| MINIX 3 | 16 | 모든 level 200 ms | 5초마다 강등된 process를 한 level 올림 |

우리 schema는 queue 2–8개, 최상위 slice 0.5–100 ms, 배수 1–8, boost 10 ms–10 s예요. 60 level이나 16 level, 200 ms slice는 못 담아요. 근사해서 넣으면 그건 다시 우리가 만든 숫자예요.

**나머지는 MLFQ가 아니에요.** Linux(CFS/EEVDF, 기본 slice 0.75 ms), sched_ext(기본 slice 20 ms), scx 스케줄러들(lavd 0.5–5 ms, bpfland 1 ms, rusty 1–20 ms 등)은 queue도 boost도 없어요. macOS, FreeBSD, Windows는 사용량을 감쇠시켜 priority를 계산하는 방식이라 level별 slice 표가 없어요. 이들에서 가져올 수 있는 건 slice 길이 하나뿐이고, 나머지 셋은 어차피 OSTEP에서 가져와야 해요 — 그게 바로 몽타주예요.

그래서 남는 건 **OSTEP의 예시**예요. 네 값이 한 교재 한 장에 다 있고, schema에 그대로 들어가요. 약점은 OSTEP가 그 값을 "예시"로 준다는 것, 특히 boost 100 ms에 대해 "아마 너무 작은 값이지만 예시라서 쓴다"고 스스로 적어둔 것이에요. 그 문장은 vocabulary의 출처 표에 그대로 인용해 뒀어요. 숨기지 않고 sensitivity check(§4의 5번)에서 시험해요.

## 4. 정한 것들

1. **MLFQ boot default = OSTEP 8장 예시 전체.** `num_queues` 3(§8.2 "three-queue scheduler"), `timeslice_us` 10000(§8.2 예시 1 "time slice of 10 ms"), `timeslice_growth` 2(§8.5 그림 8.6의 10/20/40 ms), `boost_interval_us` 100000(§8.3 그림 8.4 "every 100 ms"). `batch_bandwidth_cap`은 OSTEP의 것이 아니라 그대로 null.

2. **allotment = slice.** OSTEP의 규칙 4는 "allotment를 다 쓰면 강등"인데, 예시 1은 allotment를 slice와 같게 두고, 그림 8.6은 level마다 slice 두 개로 둬요. 우리 schema엔 allotment field가 없고 slice 하나를 다 쓰면 강등해요. 그래서 예시 1의 방식을 따라요. OSTEP 예시와 우리 모델이 다른 딱 한 군데이고, 출처 표에 적어뒀어요.

3. **EDF·LOTTERY의 slice는 "MLFQ와 같게"라는 우리 규칙으로 10 ms.** 이 규칙은 출처가 아니라 **우리의 통제 규칙**이에요: 네 알고리즘의 dispatch 단위를 같게 둬서, 상황이 다를 때 config가 내는 차이가 policy(어떤 알고리즘이냐)와 cap에서만 나오고 "한 알고리즘만 짧은 slice를 받아서" 나오지 않게 해요. EDF의 residual slice를 줄 출처는 세상에 없고(Liu & Layland의 EDF는 preemptive라 quantum이 없어요), LOTTERY에 다른 출처를 하나 더 붙이면 다시 몽타주라 안 붙였어요. Waldspurger의 lottery 논문이 10 ms quantum을 쓰는 건 우연히 일치하는 사실일 뿐 근거로 쓰지 않아요.

4. **latency floor는 1 ms 그대로, slice와 분리.** metrics doc의 floor(이보다 작은 latency 차이는 headroom으로 안 읽음)가 "slice의 절반"이라는 이유로 1 ms였어요. 그 이유는 metrics doc을 처음 쓸 때(2026-09-08) 제가 적은 가정이지 출처가 아니었고, slice를 따라 5 ms로 올리면 RQ0가 읽어야 할 차이를 지워버려요. 그래서 1 ms를 "그냥 stated assumption"으로 두고, RQ0 gate spec에 **floor sensitivity line**을 미리 등록해요: 채점 단계에서 floor를 0.5/1/2/5 ms로 바꿔 판정 개수를 다시 세어 옆에 적어요(다시 돌릴 필요 없음). floor 값이 결과를 안 바꿨다는 걸 보여주는 게 출처보다 강한 방어예요.

5. **boot-default sensitivity pair는 팀에서 정해요.** vocabulary에 "fixed를 다른 boot default 두 개로도 돌려서 gap의 부호나 순서가 바뀌면 floor를 범위로 보고한다"는 check가 이미 있어요. 전엔 그 두 개가 "OSTEP 10 ms"와 "Linux 0.75 ms"였는데, 이제 OSTEP가 primary라 짝을 다시 정해야 해요. 후보: illumos TS의 최상위 2 ms(출하된 MLFQ), Linux의 0.75 ms, sched_ext의 20 ms. 실행 전 팀 회의에서 정하고 RQ0 gate spec에 적어요. slice가 하나의 knob이라(3번 규칙) 이 check 한 번이 세 알고리즘의 slice 민감도를 같이 봐요.

6. **driver table은 자기 규칙대로 따라와요.** 표의 header에 "params는 boot 값"이라고 돼 있어서, 32개 상황의 MLFQ·EDF·LOTTERY config 전부가 10 ms로 바뀌었어요. 어느 상황에 어느 알고리즘을 주는지는 하나도 안 바뀌었어요. lint 통과.

## 5. 각자에게 — 무엇이 바뀌고 무엇이 그대로인가

**인경민 (simulator).**

- 바뀐 것: boot default의 값. t = 0 entry는 `{MLFQ, num_queues 3, timeslice_us 10000, timeslice_growth 2, boost_interval_us 100000, cap null}`. EDF의 `residual_timeslice_us`와 LOTTERY의 `timeslice_us` 기본값도 10000. simulator가 기본값을 자체적으로 들고 있다면 거기만 바꾸면 돼요.
- 그대로인 것: config schema의 field, 타입, 범위. schedule·trace 형식. MLFQ의 다섯 규칙, switch memo의 규칙, batch-class memo의 규칙 B1·B2. batch-class memo에 "FIFO는 slice가 없으니 boot default의 2000 µs를 쓴다"고 적힌 부분은 규칙 자체가 "boot default의 `timeslice_us`"라서 이제 **10000**으로 읽으면 돼요(memo는 시점 기록이라 안 고쳤어요).
- 해석 예시(simulator guide §5의 "2000 µs slice로 돌려보기")는 그 miniature에 맞춘 예시라 그대로 두고 "boot default가 아니다"라고만 적었어요.

**여쭤볼 것 두 가지.** 아래 §6의 판정에 이 두 규칙이 그대로 결과를 정해요. 둘 다 interpretation contract가 "정해서 적어 두라"고 하는 종류의 규칙이라, 어느 쪽이든 괜찮고 **적혀 있기만 하면** 돼요. 이미 정해 두셨다면 어디에 적혀 있는지만 알려주셔도 돼요.

**질문 1 — EDF에서, residual task가 slice를 쓰는 도중에 deadline task가 깨어나면 바로 lane을 넘기나요, 아니면 그 slice가 끝날 때까지 기다리나요?**

상황을 그려 보면 이래요. `c7-media`를 돌리는데, daemon이 내려보낸 config schedule의 entry가 EDF예요(media 상황에는 EDF를 주기로 돼 있어요). 우리 EDF에서 task는 두 class로 나뉘어요: **deadline class**는 TIMER로 주기적으로 깨어나는 task(마감이 있는 쪽)이고, **residual class**는 그 밖의 모든 task(마감이 없는 쪽)예요. 그러니까 simulator는 EDF로 돌고 있고, task는 셋이에요: `video`(16.67 ms마다 깨어나 6.67 ms 일함, TIMER라서 deadline class), `music`(50 ms마다 2.5 ms, 역시 deadline class), `scan`(clamscan, 60초 내내 CPU만 쓰는 batch, TIMER가 없으니 residual class). vocabulary는 "deadline class는 earliest-deadline-first로 돌고, residual class는 **남는 lane time에** round-robin"이라고만 해요. "남는"이 무슨 뜻인지가 질문이에요. 참고로 이 두 class 구조는 교과서 EDF에 없는 우리 설계예요 — Liu & Layland의 EDF는 모든 task에 deadline이 있고 preemptive라, option A가 교과서에 가까운 기본값이에요. 하지만 residual class가 우리 것이라 우리 문서에 한 줄로 적혀야 해요.

- **option A — 바로 뺏는다.** t = 100000에 `scan`이 residual slice(10 ms)를 시작했어요. t = 103000에 `video`의 TIMER가 만료돼요. deadline class가 residual class보다 항상 우선이니 `scan`은 그 자리에서 `run_end(preempt)`, `video`가 t = 103000에 `run_start`. `video`의 대기는 0.
- **option B — slice 끝까지 기다린다.** 같은 상황에서 `video`는 `scan`의 slice가 끝나는 t = 110000까지 기다렸다가 `run_start`. 대기 7 ms. `scan`의 slice 시작과 거의 동시에 깨어난 tick이면 대기가 최대 10 ms.

option A면 residual slice의 길이는 deadline class에 아무 영향이 없고, `video`와 `music`은 cap이 얼마든 tick을 놓치지 않아요. option B면 `video`가 최대 10 ms를 기다릴 수 있는데, `video`가 마감을 맞추려면 늦어도 10 ms 안에는 시작해야 하니(16.67 − 6.67), 딱 경계에 걸려요. 그 경계를 어떻게 처리하느냐가 질문 2예요. 참고로 MLFQ 쪽은 이미 정해져 있어요(switch memo: 더 높은 queue로 깨어나면 즉시 preempt, 같거나 낮은 queue면 slice 경계까지 대기). EDF에도 그런 한 줄이 필요해요.

**질문 2 — 같은 순간에 두 event가 겹치면 어느 쪽을 먼저 처리하나요? 특히 "residual slice의 끝"과 "deadline task의 TIMER 만료"가 같은 µs에 오는 경우요.**

option B일 때 생기는 상황이에요. `scan`이 t = 100000에 slice를 시작하고, `video`의 TIMER가 정확히 t = 100000에 만료되면(같은 µs), 두 event가 같은 순간에 있어요. 처리 순서에 따라 결과가 달라요.

- **TIMER 만료를 먼저 처리**하면, `video`가 runnable이 된 상태에서 scheduler가 결정을 내리니 `video`가 t = 100000에 바로 lane을 받아요. 대기 0.
- **slice 시작을 먼저 처리**하면, `scan`이 lane을 잡은 뒤에 `video`가 깨어나니 option B대로 t = 110000까지 기다려요. 대기 정확히 10 000 µs. 그러면 `video`는 t = 116667에 끝나고, 마감(다음 period 경계, t + 16667)에 **정확히** 맞아요. harness의 miss 판정은 "job latency가 period보다 **크면** miss"라 이 경우는 met이에요. 하지만 여기서 1 µs만 더 밀리면(예: 같은 순간에 처리되는 다른 event 하나) miss예요.

interpretation contract가 "같은 순간의 event는 적어 둔 결정적 순서로 처리한다"고 하는 게 이 규칙이에요. 저희 mock fixture는 "config entry 먼저, 그 다음 arrival을 파일 순서로"까지만 정해 뒀고, slice 경계와 TIMER 만료의 순서는 안 정해져 있어요. 어느 순서든 괜찮아요. 다만 (a) 어느 쪽인지, (b) 그 순서가 trace의 line 순서에도 그대로 나타나는지(harness는 trace의 순서를 그대로 믿어요)를 알려주시면 돼요.

**지오 생각 (참고만).** 둘 다 교과서 쪽으로 답하면 될 것 같아요. 질문 1은 **option A(바로 뺏는다)**. deadline class를 두는 이유가 마감 있는 일이 깨어나는 순간 다른 모든 일보다 앞서게 하려는 것이라, residual slice가 끝날 때까지 기다리게 하면 non-preemptive EDF가 되어 다른(더 약한) scheduler가 돼요. 우리 MLFQ가 이미 "더 높은 queue로 깨어나면 즉시 preempt"인 것과도 맞고, Linux의 `SCHED_DEADLINE`이 fair class를 다루는 방식과도 같아요. 구현도 더 단순해요 — residual round-robin은 deadline class가 비워 둔 lane에서만 돌면 되니까요. 질문 2는 **TIMER 만료(깨어남)를 먼저, dispatch 결정을 나중에**. 같은 µs에 두 일이 있으면, scheduler가 결정을 내리기 전에 깨어난 task가 보이는 순서가 "정보를 다 가지고 결정하는" 유일한 순서예요. 반대로 dispatch부터 하고 그 다음에 runnable task를 발견하는 순서는, 물리적 이유 없이 정확히 slice 하나만큼의 대기를 만들어내요. 둘 다 이렇게 정해지면 `c7-media`·`c7-meeting`의 답은 확정이에요: 어느 config에서도 `fixed`에서도 miss가 없고, 두 파일은 headroom 없음. 어디까지나 제 생각이고, 정하는 건 경민 님이에요 — 다르게 정하셔도 적혀 있기만 하면 돼요.

**왜 이게 중요한가.** simulator에는 난수가 없어서, 이 두 규칙만 적히면 `c7-media`·`c7-meeting`에서 `video`가 tick을 놓치는지 안 놓치는지가 **실행 전에** 계산으로 나와요. 그 답에 따라 두 파일이 RQ0 판정 set에 남을지가 정해져요(§6). 반대로 규칙이 안 적혀 있으면, 결과가 나온 뒤에 "왜 miss가 났지/안 났지"를 구현 세부에서 찾아야 하고, 그건 pre-registration이 막으려는 상황이에요.

**박이안 (daemon).**

- 바뀐 것: `fixed` condition이 내는 한 줄짜리 schedule과 모든 schedule의 t = 0 boot entry의 값. `daemon/tools/drivertable/config_schema.py`의 기본값 세 개(10000). prior table의 entry 값.
- 그대로인 것: telemetry, recognition log, schedule의 형식. `oracle`과 `random`의 동작(상황을 정하고 그 상황의 config를 schedule에 찍는 것 — config의 숫자만 바뀜). validator의 범위 검사. `fallback`·`held`·`clamped` 규칙.

**공통.**

- vocabulary §2의 "Provenance of the boot default" 표가 다시 쓰였어요. 어떤 값이 어디서 왔는지 한 줄씩.
- harness의 mock fixture 두 개(`mock-p1a`, `mock-switch`)는 2 ms MLFQ로 손으로 계산한 거라, boot entry 옆에 2 ms MLFQ entry를 하나 명시적으로 찍는 방식으로 정합성을 맞췄어요(`mock-media`가 boot 옆에 FIFO entry를 찍는 것과 같은 수법). 손 계산 값은 안 바뀌었어요.

## 6. 알아둘 것 — `c7-meeting`과 `c7-media`의 기대치가 바뀌어요

09-10 memo §6에서 "cap이 안 닿는 두 pair"로 적었던 파일들이에요. 그때의 계산은 2 ms slice 위에서 한 거라 다시 했어요. 쉬운 말로:

- video 소비자는 16.67 ms마다 깨어나 6.67 ms 일해요. 그러니까 **10 ms까지는 기다려도 마감을 맞추고, 그보다 1 µs라도 더 기다리면 miss**예요.
- 이 두 파일에서는 simulator가 EDF로 돌아요(media·meeting 상황의 config가 EDF라서, `background_wanted`가 true든 false든). scan(clamscan)은 TIMER가 없으니 residual class라 slice 단위로 lane을 잡아요. 그 slice가 이제 **딱 10 ms**예요. video가 scan의 slice 시작 직후에 깨어나면 10 ms를 기다리고, 6.67 ms 일하고, 마감에 **정확히** 맞아요. 여유가 0이에요. 이걸 "knife edge"라고 부르고 있어요 — 두 출처의 숫자(interbench의 video 프로파일, OSTEP의 slice)가 우연히 10 ms에서 만난 거예요.
- `fixed`(MLFQ)에서는 전에 2 ms slice가 video의 6.67 ms burst를 강등시켜서 scan과 같은 queue에서 경쟁하게 만들었고, 그게 EDF config가 `fixed`를 이기는 이유였어요. 10 ms slice에서는 video가 강등되지 않아요. 그래서 이 이유도 사라져요.

결과는 §5의 질문 두 개에 달려 있어요. deadline task가 바로 뺏거나, 경계에서 "맞춤"으로 처리하면 → cap이 얼마든, 어느 조건에서도 miss가 없고, 두 파일은 `c1-media`·`c1-meeting`처럼 "headroom 없음"이 돼요. 경계에서 "miss"로 처리하면 → scan이 lane을 잡는 빈도(cap이 `background_wanted` true면 0.5, false면 0.05)에 따라 두 config의 miss rate가 달라져서, 오히려 처음으로 cap 축이 측정돼요. 어느 쪽이든 **simulator는 결정적**이라 규칙만 적히면 실행 전에 답이 나와요. 그래서 여쭤보는 거예요. 이 두 파일을 RQ0 판정 set(지금 27개)에 두는지는 답을 받은 뒤, 실행 전에 RQ0 gate spec을 확정하는 단계에서 정해요.

## 7. 숫자 요약

| 값 | 전 | 후 | 근거 |
|---|---|---|---|
| MLFQ `num_queues` | 3 | 3 | OSTEP §8.2 |
| MLFQ `timeslice_us` | 2000 | **10000** | OSTEP §8.2 예시 1 |
| MLFQ `timeslice_growth` | 2 | 2 | OSTEP §8.5 그림 8.6 |
| MLFQ `boost_interval_us` | 100000 | 100000 | OSTEP §8.3 그림 8.4 (OSTEP 자신의 "too small" caveat 인용) |
| EDF `residual_timeslice_us` | 2000 | **10000** | 같은 granularity 규칙 (우리 규칙) |
| LOTTERY `timeslice_us` | 2000 | **10000** | 같은 granularity 규칙 (우리 규칙) |
| LOTTERY `batch_share` | 0.15 | 0.15 | 출처 없음 (그대로) |
| latency floor (metrics doc) | 1 000 µs "slice의 절반" | 1 000 µs, slice와 무관한 stated assumption | floor sensitivity line으로 방어 |
| prior table entry | 2000 | 10000 | header의 "params는 boot 값" 규칙 |

## 8. 어디를 읽으면 되나

- `docs/recognition-vocabulary.md` §2 — 기본값 표, "Provenance of the boot default", allotment와 같은 granularity 규칙, changelog 2026-09-11.
- `docs/harness/metrics.md` §10 floor 행과 changelog 2026-09-11.
- `daemon/driver-table/prior.yaml` — 바뀐 entry 값. `daemon/tools/drivertable/config_schema.py` — 기본값.
- `docs/references.md` — `ostep`, `illumos-ts`, `linux-sched-fair`, `waldspurger-osdi94`의 role 줄.
- `harness/tools/tests/fixtures/README.md` — mock 두 개의 정합성 처리.
