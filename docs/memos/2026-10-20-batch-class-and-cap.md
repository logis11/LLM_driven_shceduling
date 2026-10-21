# batch class와 `batch_bandwidth_cap` — 정의와 cap 값의 기준

> Status: memo · Created 2026-10-20 · Updated 2026-10-21
> 닫힘 (2026-10-21) — 인경민이 conformance item (d), executor가 `batch_bandwidth_cap`을 batch class에 work-conserving 상한으로 적용하는 것을 simulator stage V에 구현했어요(2026-10-20, 커밋 `1074b14d`). 상한을 재는 window는 인경민의 decision D10이고 `simulator/memo/memo_261020.md` Part F에 적혀 있어요. 남은 것은 (d)에 기대는 문장들의 확인이에요(§4).
> From 인지오 to 인경민.

## 0. 이 문서

batch class가 무엇이고, driver table의 cap 값이 어떤 기준으로 정해졌는지 한 장으로 정리했어요. 새로 정한 것은 없어요. 지금 repository에 있는 규칙과 값을 모은 것이고, 근거는 항목마다 적은 파일에 있어요.

## 1. batch class

**무엇.** executor가 task의 행동만 보고 붙이는 분류예요. 프로그램이 선언하는 속성이 아니고, process 이름이나 ground truth도 보지 않아요. executor가 모든 condition에서 같아야 condition 사이의 차이가 recognizer에서만 나오기 때문이에요.

**왜 필요한가.** `background_wanted`(사용자가 그 background 작업을 원했는가)가 scheduler에 효과를 내는 통로가 `batch_bandwidth_cap`이에요. mode는 algorithm을 고르고 attribute는 cap을 골라요(research proposal §4.5). cap은 걸 대상이 있어야 하고, executor는 이름을 볼 수 없으니 대상을 행동으로 정해요. 그 대상이 batch class예요.

**규칙** (B1·B2는 batch-class memo §3, simulator에 구현됨: `simulator/src/sim.cpp`, stage S. declared idle은 아직 구현 전)

| 규칙 | 내용 |
|---|---|
| B1, 들어가고 나가기 | 마지막 voluntary block(기다려야 하는 `WAIT`, `SLEEP`, 아직 오지 않은 `TIMER`) 이후 CPU를 slice 하나만큼 쓰면 들어가요. 다음 voluntary block에서 나가요. preempt는 class를 바꾸지 않아요. slice는 지금 config의 `timeslice_us`(MLFQ, LOTTERY), `residual_timeslice_us`(EDF), FIFO는 boot 기본값이에요. boot 기본값은 10 ms예요. |
| B2, 주기적인 task 제외 | `TIMER`를 가진 task와, 거기서 `WAKE`로 닿는 task 전부(frame chain)는 burst 길이와 상관없이 batch가 아니에요. EDF의 deadline class와 같은 집합이에요. |
| declared idle | `declared_class`가 `idle`인 task(Tracker indexer, Déjà Dup)는 다른 class의 task가 runnable하면 돌지 않아요. 그래서 cap도 share도 닿지 않아요(declared-class memo, conformance item (e)). |

**rebuild된 core set에서** (batch-class memo의 2026-10-17 correction)

- `c2-p2b`의 unattended upgrade는 CPU의 92 %를 batch class로 써요. 그래서 0.05 cap이 이 작업에 걸려요.
- `c2-p2a`의 Steam 다운로드는 EDF 아래에서 file이 주는 구간이 짧게 돌고 멈추는 launch 단계라 batch class가 아니에요. 그래서 cap이 걸리지 않아요.
- game frame chain은 B2 때문에 batch가 아니에요.
- VS Code는 keystroke 하나에 약 78 ms를 써요(prior table header). 그래서 깨어난 순간에는 batch가 아니고, 10 ms가 지나면 batch가 되고, 다음 key를 기다리며 block하면 다시 나가요. 채점이 재는 깨어남→실행 대기는 보호돼요.

## 2. `batch_bandwidth_cap`

**무엇** (`docs/recognition-vocabulary.md` §2). batch가 아닌 task가 runnable한 동안 batch class 전체가 쓸 수 있는 CPU 비율의 상한이에요. `null` 또는 0.05–0.95예요.

- **상한만 있어요.** batch에게 몇 %를 보장하는 장치는 executor에 없어요. 30 s `starvation_floor`는 harness guard예요. 넘으면 run이 invalid가 될 뿐, CPU를 나눠 주지는 않아요.
- **work-conserving이에요.** batch가 아닌 task가 runnable하지 않으면 cap은 꺼져요. batch 작업 혼자면 cap이 0.05여도 CPU를 다 써요.
- **window는 token bucket이에요**(인경민의 decision D10, `simulator/memo/memo_261020.md` Part F). batch가 아닌 task가 runnable한 동안에만 cap의 속도로 차고, batch class가 받은 CPU 시간만큼 빠져요. 깊이는 slice 하나예요. 그래서 batch class는 길게 보면 cap만큼 받고, batch가 아닌 task가 기다리는 동안 한 번에 이어 도는 길이는 slice 하나를 넘지 않아요. cap 0.05에 slice 10 ms면 200 ms마다 10 ms예요.
- **LOTTERY만 몫이 있어요.** `batch_share`는 batch class의 ticket 비율, 즉 기대값으로 받는 몫이에요. `batch_share ≤ cap`이고, prior table에서는 둘이 같아요.

**값의 기준** (`daemon/driver-table/prior.yaml` header)

| 칸 | cap | 기준 |
|---|---|---|
| `background_wanted: false` | 0.05 | schema 최저치 |
| `true`, file에 batch 채점 항목 있음 | w_batch / (w_fg + w_batch) | 채점 비중을 그대로 CPU 비율로 |
| `true`, batch 채점 항목 없음 | 0.5 | 반반, stated assumption |

prior table에 들어간 값이에요. 채점 비중은 `harness/scoring/scoring-spec.yaml`의 값이에요.

| 행 (`background_wanted: true`) | 채점 비중 (foreground : batch) | cap |
|---|---|---|
| ml-train, render, transcode, gaming | 1.0 : 0.5 | 0.333 |
| compile, indexing | 1.0 : 1.0 | 0.5 |
| backup | 1.0 : 0.25 | 0.2 |
| browsing, office, mail, dev, photo, meeting, media, video-edit, idle | batch 항목 없음 | 0.5 |
| 모든 mode의 `false` 행 | — | 0.05 |

**근거의 성격.** 이 값들은 측정값도 문헌값도 아니에요.

- 범위 0.05–0.95와 최저치는 이 프로젝트가 정한 값이에요(recognition-vocabulary §2). 장치의 모양은 Linux의 두 장치에서 반씩 왔어요(§3).
- 채점 비중도 design 값이에요.
  - 0.5는 C2·C3 file의 progress 항목에서 왔어요.
  - backup의 0.25는 `c2-p3b`에서 왔어요.
  - indexing의 1.0은 scoring spec이 직접 stated assumption이라고 적어 둔 값이에요.
- prior table은 이론으로 채운 출발점이에요. calibrated table은 configuration search로 값을 맞춰요.

## 3. cap 값에 대한 우려

- cap의 범위, 최저치, 행마다 값은 근거가 design이에요. 출처가 있는 건 batch class 규칙(OSTEP 8장, Liu & Layland 1973)과 cap 모양의 두 반쪽까지예요.
- 그 두 반쪽은 kernel 문서 원문으로 확인했어요(2026-10-20). 상한이라는 면은 CFS bandwidth control(`cpu.max`, `linux-sched-bwc`)이에요. 다만 이 장치는 quota를 다 쓰면 다른 task가 CPU를 원하지 않아도 다음 period까지 throttle해서 work-conserving이 아니에요. 경쟁할 때만 나눈다는 면은 cgroup v2의 `cpu.weight`(`linux-cgroup-v2`)인데, 이건 상한이 아니라 비율이에요. 둘을 합친 "batch가 아닌 task가 runnable할 때만 걸리는 상한"은 우리 design이에요(`docs/references.md`, recognition-vocabulary §2).
- 모든 condition이 같은 driver table을 쓰기 때문에 cap 값이 condition 사이의 비교를 한쪽으로 기울이지는 않아요. 하지만 `random`과 `oracle` 사이 차이의 크기는 cap 값에 따라 달라져요.
- 그 영향이 한곳에 몰려 있어요. RQ0 판정용 file 중 9개가 MLFQ에 cap 0.05인 행으로 가요(RQ0 gate spec의 `prior-table-structure`). 최저치 0.05 하나가 판정의 큰 몫을 차지하는 셈이에요.
- 대응: RQ0 gate spec에 cap band line을 넣어요. g band line처럼 다른 cap 값 아래에서의 판정 수를 primary 옆에 찍는 방식이고, 쓸 값은 RQ0 run 전에 spec에서 고정해요(인지오, Phase 10). 행마다 값을 측정으로 맞추는 건 configuration search로 만드는 calibrated table의 몫이에요.

## 4. 인경민에게

- conformance item (d)는 끝났어요(stage V, 2026-10-20). window는 decision D10으로 simulator 문서에 적혀 있어요.
- 남은 것은 (d)에 기대는 문장들의 확인이에요(9.16 기록 `compiled/uncheckable-by-item.md`의 (d) "Check" 줄). `c7-browsing`, `c7-office`, `c7-dev`, `c7-photo`, `c7-video-edit`와 `c6-spoof`에서 foreground의 P99가 cap 0.05일 때 cap 0.5일 때보다 나쁘지 않은지, foreground가 runnable한 동안 batch class의 CPU가 cap 이하인지 봐요.
- B1·B2는 simulator에 있는 그대로 적었어요. declared idle 규칙은 conformance item (e)로 따로 열려 있어요(declared-class memo). 다른 점이 있으면 알려 주세요.
