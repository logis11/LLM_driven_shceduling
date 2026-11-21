# configuration search의 결과 — driver table을 다시 써요

> Status: memo · Created 2026-11-21 · Updated 2026-11-21
> 닫힘 — 두 분께 부탁하는 것은 없어요. 기록은 `docs/rq0-run-record.md`의 2026-11-21 configuration search, report는 `harness/experiments/rq0-config-search/`에 있어요.
> From 인지오 to 인경민, 박이안.

## 결과

- RQ0 gate spec의 failure procedure가 정한 configuration search를 끝냈어요(sub-task 11.4). search spec(`harness/experiments/rq0-config-search.yaml`)을 search를 돌리기 전에 commit했고, harness의 새 tool(`harness/tools/search.py`)이 그 파일대로 돌렸어요.
- point 하나가 configuration 하나예요. oracle이 자기 row를 적용하는 자리에 그 configuration을 대신 적용하고, label은 보지 않아요. configuration 470개(MLFQ 288, LOTTERY 110, EDF 66, FIFO 6)를 파일 10개에 돌려서 4,700 run이에요. 실패한 run은 없어요.
- `simulator@841dc81131cb`, `daemon@62c71f0d2de0`, 두 번째 bless의 dataset으로 돌렸어요. 2026-11-21 10:20에 시작해서 15:41에 끝났어요(5시간 21분).
- 파일 10개는 이래요.
  - 규칙으로 고른 셋: `c7-transcode`, `c7-gaming`, `c1-transcode`.
  - 모든 term에 headroom이 없는 judging 파일 일곱: `c7-dev`, `c7-video-edit`, `c7-compile`, `c1-render`, `c7-photo`, `c7-ml-train`, `c7-render`.
- grid를 읽기 전에 파일마다 두 가지를 확인했어요. boot default의 point가 그 파일의 fixed run을 재현하는지, row의 point가 oracle run을 재현하는지요. 20개 모두 재현했어요.
- point의 값은 이렇게 매겨요. term마다 fixed보다 나아진 만큼을 fixed의 값으로 나눠요(부호 포함, floor 미만은 0). 그걸 scoring spec의 weight로 평균해요.
- 파일마다 finding이 셋 중 하나예요.
  - finding 1, config 사이에 차이가 없음: 어느 두 point도 어떤 term에서 floor 이상 다르지 않아요.
  - finding 3, prior table이 놓친 차이: row의 값이 최선 point 값의 절반(1 − g, g = 0.5) 이하이고, 최선 point가 어떤 term에서 row보다 floor 이상 나아요.
  - finding 2, 둘 다 아님: prior table의 row가 버텨요.
- **route: driver table을 다시 써요.** 10개 중 8개가 finding 3이에요. g band(0.25–0.67)의 모든 g에서, 그리고 열 개의 다른 boot default 모두에서 route가 같아요.

| 파일 | finding | row의 값 | 최선 point | 최선의 값 |
|---|---|---|---|---|
| `c7-transcode` | 2 | 0.865 | `fifo-c0.2` | 0.988 |
| `c7-gaming` | 2 | 1.000 | row 자신(`edf-s10000-c0.05`) | 1.000 |
| `c1-transcode` | 3 | 0.005 | `mlfq-s20000-b10000-q3-x2-c0.5` | 0.562 |
| `c7-dev` | 3 | −2.200 | `mlfq-s10000-b10000-q3-x2-c0.95` | 0.684 |
| `c7-video-edit` | 3 | −0.703 | `mlfq-s10000-b10000-q3-x2-c0.333` | 0.809 |
| `c7-compile` | 3 | −0.495 | `mlfq-s100000-b100000-q3-x2-cnone` | 0.974 |
| `c1-render` | 3 | −0.011 | `mlfq-s30000-b10000-q3-x2-c0.95` | 0.053 |
| `c7-photo` | 3 | 0.000 | `fifo-c0.333` | 0.356 |
| `c7-ml-train` | 3 | 0.000 | `fifo-c0.95` | 0.898 |
| `c7-render` | 3 | 0.000 | `mlfq-s10000-b10000-q3-x2-c0.05` | 0.944 |

point의 이름이 곧 configuration이에요. `mlfq-s<top slice, µs>-b<boost 간격, µs>-q<queue 수>-x<slice 증가율>-c<cap>`, `edf-s<residual slice>-c<cap>`, `lottery-s<slice>-w<batch share>-c<cap>`, `fifo-c<cap>`이고, `cnone`은 cap이 없다는 뜻이에요.

- `c7-gaming`에서는 row(EDF)가 frame miss rate 0으로 이미 최선이에요. EDF point 66개가 모두 0에 닿고, 다른 algorithm의 point는 하나도 안 닿아요.
- `c7-transcode`에서는 읽은 point 450개 중 23개가 row보다 나아요.
- 읽지 않은 point가 파일 넷에 75개 있어요. guard에 걸렸거나 30 s 넘는 wait이 있는 point예요: `c7-transcode` 20, `c1-transcode` 16, `c7-compile` 32, `c7-ml-train` 7.
  - 100 ms boot default의 point가 `c7-transcode`, `c1-transcode`, `c7-ml-train`에서 그 안에 들어 있어요. 그래서 그 boot default에서는 이 세 파일의 finding이 없어요.
  - RQ0 run에서도 이 세 파일의 fixed run이 100 ms에서 `starvation_floor`에 걸렸어요.
- 한계가 두 가지 있어요.
  - MLFQ의 queue 수와 slice 증가율은 다른 knob과 교차하지 않고 하나씩만 움직였어요.
  - variant 파일은 search하지 않았어요.
- search는 읽기만 해요. 찾은 것을 table에 써 넣지 않았으니 driver table은 아직 그대로예요.

## 인지오가 할 일

1. 11.5에서 Phase 11이 바꾼 docs와 docs index를 정리하고 Phase 11을 닫아요.
2. Phase 12에서 driver table을 다시 쓰고, 두 번째 RQ0 gate spec을 run 전에 고정한 다음 두 번째 RQ0 run을 돌려요. 파일별 finding이 Phase 12를 설계하는 바탕이에요. table을 어떻게 다시 쓸지는 Phase 12의 spec에서 정해요.

## 두 분께

- 경민: 지금 부탁할 것은 없어요. 확인할 때 걸린 줄이 하나 있었어요. 같은 algorithm의 MLFQ entry가 들어오면 boost timer가 다시 시작돼요(`docs/harness/metrics.md` §11 item 9). 그래서 oracle이 2 s에 row를 다시 적용하는 `c1-transcode`와 `c1-render`에서는, boot default의 point와 fixed run의 trace가 그 순간의 `x_mlfq_boost` 한 줄만 달라요. 그 줄은 빼고 비교했어요. simulator를 바꾸면 version이 바뀌니까 알려 주세요.
- 이안: 지금 부탁할 것은 없어요. driver table(`daemon/driver-table/prior.yaml`)을 다시 쓰게 됐어요. Phase 12 spec에서 어떻게 다시 쓸지 정하면 그때 알려 드릴게요.
