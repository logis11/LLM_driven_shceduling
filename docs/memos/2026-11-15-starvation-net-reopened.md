# 2026-11-15 cold smoke의 starvation 읽기 — 다시 열린 starvation net과 정한 것

> Status: memo · Created 2026-11-15 · Updated 2026-11-15
> From 인지오 to 인경민.

## TL;DR

- cold smoke(TODO의 10.4)의 1,197 run이 모두 끝났고, guard table과 `simulator/tools/wait_check.py`를 읽었어요. judging 파일 넷에서 `starvation_floor`가 실패해서, 10.4 spec의 규칙대로 executor의 starvation net 질문이 다시 열렸어요.
- 넷 모두 boot default `ostep-slice-100000us`의 `fixed` run이에요. top slice가 100 ms이고 boost 간격도 100 ms예요. boost가 실행 중인 task의 allotment까지 새로 시작해서, block하지 않는 task가 boost를 몇천 번 지나며 lane을 계속 잡아요.
- 인지오가 정한 것: 지금의 계약 그대로 그 sweep point의 성질로 둬요. starvation net도 만들지 않고 simulator도 바꾸지 않아요.

## 1. 읽은 것

`starvation_floor`는 어떤 task든 ready로 30 s를 넘게 기다리면 실패해요. 이 smoke에서 100 ms point의 `fixed` run에서 실패한 것:

| 파일 | judging | 기다린 task | 가장 긴 wait | lane을 잡은 task | 지난 boost |
|---|---|---|---|---|---|
| `c1-ml-train` | 예 | `editor` | 320.3 s | `hog` | 3,203 |
| `c7-ml-train` | 예 | `editor` | 300.0 s | `hog` | 3,000 |
| `c1-transcode` | 예 | `video-editor` | 168.0 s | `batch` | 1,680 |
| `c7-transcode` | 예 | `video-editor` | 167.9 s | `batch` | 1,680 |
| `c3-creation` | 아니요 | `video-editor` | 197.3 s | `batch` | 1,973 |

- 각 wait 동안 lane을 잡은 task는 한 번의 run으로 그 wait 전체를 잡았고, 스스로 block해서야 놓았어요.
- simulator guide §5의 rule 5는 "Every `boost_interval`, everything returns to the top queue with its allotment afresh"예요. `Mlfq::on_timer`가 모든 task의 `allot`을 0으로 되돌리는데, 실행 중인 task도 들어가요(`simulator/src/sim.cpp:305–313`). 실행 중인 task의 horizon은 slice에서 allot을 뺀 값이라서(`:348`), boost가 올 때마다 slice가 처음부터 다시 시작해요. 같은 level의 ready task는 선점하지 못해요(`:350`, 더 높은 level만 선점해요).
- `wait_check.py`가 guard가 못 읽는 wait를 judging 파일에서 둘 더 찾았어요. 같은 point에서 run이 끝날 때 아직 ready였던 `c7-ml-train`의 `editor`(205.0 s)와 `c2-p1a`의 `editor`(38.7 s)예요.
- 다른 아홉 point는 top slice가 30 ms 이하라서 boost 간격보다 짧아요. 거기서는 이 실패가 없어요.

## 2. EDF의 frame chain — Part L 그대로

`simulator/memo/memo_261111.md` Part L의 첫째 원인(EDF에서 frame chain이 lane을 다 가져감)도 smoke에서 그대로 보였어요.

- `oracle`의 다섯 run(`c3-evening`, `c2-p2a`와 `c2-p2b`의 chain-scale 변형 넷)이 이름 붙인 대로 실패해요. `steam`이 `c3-evening`에서 240.0 s, 변형 넷에서 86.4 s 기다려요.
- 변형 넷의 `random-1` run도 실패해요. 첫 구간(0–60 s)에 EDF를 뽑아서 `steam`이 60 s의 전환까지 60.0 s 기다려요. `random-2`는 MLFQ와 LOTTERY를 뽑아서 통과해요.

## 3. 정해진 것

- **100 ms point의 실패는 그 point의 것이에요.** starvation net도, simulator 변경도 없어요. RQ0 gate spec의 `sensitivity-lines` statement가 원인과 함께 적고, 그 point의 count는 report에서 unavailable로 남아요.
- **EDF의 frame chain.** 같은 statement가 원인과 그 원인이 닿는 run을 적어요. 그 다섯 파일에서 schedule이 frame chain 위에 EDF를 두는 run은 실패해요. `oracle`은 언제나, `random`은 거기서 EDF를 뽑은 seed마다요.
- **longest-wait line이 경민과의 질문을 다시 여는 조건.** judging 파일의 run이 15 s를 넘으면 다시 열려요. `ostep-slice-100000us`의 run은 빼요.
- 기록은 `_dev/research/jioh/task-10.4-cold-smoke-and-cost-response/`(README, `starvation.json`)에, 결정은 10.4 spec(`_dev/docs/spec/jioh/task-10.4-cold-smoke-and-cost-response.md`, decisions 16·20)에 있어요.
