# RQ0 run의 결과 — FAIL(잠정)과 다음에 할 일

> Status: memo · Created 2026-11-18 · Updated 2026-11-21
> 닫힘 — 두 분께 부탁하는 것은 없어요. run의 기록은 `docs/rq0-run-record.md`, report는 `harness/experiments/rq0-gate/`에 있어요.
> From 인지오 to 인경민, 박이안.

## 결과

- RQ0 run의 19,425 run을 2026-11-16 08:57에 시작해서 2026-11-18 06:23에 끝냈어요(45시간 26분). 실패한 run은 없어요. `simulator@0d323c84470a`, `daemon@62c71f0d2de0`로 돌렸어요.
- report를 열기 전에 guard와 `simulator/tools/wait_check.py`부터 읽었어요. verdict이 읽는 1,938 run에서 걸린 것이 없었고, 두 프로그램의 잘못으로 드러난 것도 없어요.
- verdict은 **FAIL**이에요. judging 파일 19개 중 6개가 gap ≥ g = 0.5를 넘었고, 필요한 수는 K = 10이에요.
- **잠정**이에요. spread를 달고 다니는 측정값들을 구간의 아래 끝에 두면 `c7-ml-train`의 gap이 2.51에서 0.00으로 떨어져요. 그래서 re-measurement contingency가 발동했고, 그 값을 다시 재야 결과가 최종이에요. 5개든 6개든 FAIL은 같아요.
- g를 0.25로 낮추면 10개로 PASS예요. 사전 규칙대로 verdict은 g에 대한 범위로 보고해요.
- link 2(행동만 봐서는 안 보이는 차이가 있다)는 서 있어요. 19개 중 17개에 headroom이 있어요.
- 못 넘은 13개 중 넷(`c1-transcode`, `c2-p3a`, `c1-render`, `c1-compile`)에서는 random이 oracle보다 나아요. driver table의 정답 row가 그 파일에서 최선이 아니라는 뜻이에요. 둘(`c7-photo`, `c7-render`)은 headroom이 없어요.

## 인지오가 할 일

1. 10.6 docs sweep으로 Phase 10을 닫아요.
2. 다음 phase에서 RQ0 gate spec의 failure procedure를 밟아요. 규칙으로 고른 failing judging 파일 셋에 configuration search를 먼저 해요(workload를 바꾸기 전에). search가 config 사이의 차이를 못 찾으면 workload를 다시 설계하고, prior table이 놓친 차이를 찾으면 driver table을 다시 써요.
3. `c7-ml-train`을 움직인 값의 재측정도 다음 phase에서 해요. 무엇을 먼저 할지는 그 phase의 spec에서 정해요.

## 두 분께

- 경민: 지금 부탁할 것은 없어요. simulator를 바꾸면 version이 바뀌니까 알려 주세요.
- 이안: 지금 부탁할 것은 없어요. driver table(`daemon/driver-table/prior.yaml`)을 다시 쓰게 되면 그때 따로 알려 드릴게요.

## 정정 (2026-11-18)

- scorer에 부호 오류가 있었어요. oracle이 fixed보다 floor 이상 나쁜 term에서 scorer가 oracle의 개선을 부호 없이 읽어서, share의 부호가 뒤집혔어요. 그 term에서는 fixed보다 나은 condition이 음수 share를 받았어요.
- `c7-ml-train`의 gap 2.51이 그 경우예요. editor의 입력 latency P99가 fixed에서 7.19 s, oracle에서 8.02 s예요. random이 oracle보다 나은 파일인데, 부호가 뒤집혀서 g를 넘은 것으로 읽혔어요.
- harness에서 고쳤어요(`harness/CHANGELOG.md`, 2026-11-18). oracle이 fixed보다 floor 이상 나쁜 term은 no headroom(share 1)이고, "oracle worse than fixed" 표시가 붙어요.
- 첫 verdict은 그대로예요: FAIL, 19개 중 6개, 잠정.
- 고친 규칙으로 같은 run을 다시 채점한 post hoc reading이 `harness/experiments/rq0-gate/post-hoc/`에 있어요. verdict은 아니에요. guard와 grade는 run의 것을 그대로 썼어요.
  - 19개 중 4개가 g를 넘어요: `c2-p2a`, `c2-p2b`, `c7-browsing`, `c7-office`.
  - headroom이 있는 파일은 19개 중 12개예요. `c7-dev`, `c7-video-edit`, `c7-compile`, `c7-ml-train`, `c1-render`가 headroom을 잃었어요.
  - g = 0.25에서도 8개라서 FAIL이에요.
  - random이 oracle보다 나은 파일은 셋이에요: `c1-transcode`, `c2-p3a`, `c1-compile`.
- oracle이 fixed보다 나쁜 term은 judging 파일 9개에 있어요. Phase 11에서 그 run들의 trace를 읽고, 각 경우가 프로그램의 결함인지 configuration의 성질인지 가려요.

## 정정 (2026-11-21)

- re-measurement를 끝냈어요(sub-task 11.3). `c7-ml-train`을 움직인 값은 학습 run(`cpu-batch`의 `python3`)의 voluntary block 사이 run이었어요. `c7-ml-train`이 담은 네 값을 하나씩 구간의 아래 끝에 두고 run의 프로그램으로 돌렸더니, 그 값 하나만 gap을 2.51에서 0.00으로 떨어뜨렸어요.
- 그 entry를 새 repeat 107개로 다시 쟀어요(`meas-ci:background:2026-11-20`). runner의 kernel이 `7.0.0-1017-azure`로 바뀌어서 transparent huge pages의 기본값이 `madvise`예요. job이 `always`를 써 넣고, runner의 agent(`provjobd`)가 끝낸 wait은 그 wait이 끊은 run에 접어 넣었어요.
  - voluntary block 사이 run: 69.49 s ±27.3 % → 55.27 s ±5.89 %
  - block 하나: 311.5 µs ±10.8 % → 403.96 µs ±2.15 %
- 새 값으로 dataset을 다시 bless했어요(`harness/CHANGELOG.md`, 2026-11-21). library hash 말고도 바뀐 artifact는 `python3`을 담은 파일뿐이고, demand는 하나도 안 움직였어요.
- 첫 verdict이 최종이 됐어요: **FAIL, 19개 중 5개**(K = 10). 다시 만든 세 파일(`c2-p1a`, `c1-ml-train`, `c7-ml-train`)만 run의 프로그램과 run의 scorer로 다시 돌렸어요. `c7-ml-train`은 headroom이 없어져서(gap 0.00) 빠졌고, 나머지 16개는 run의 값 그대로예요.
- 고친 프로그램(`simulator@841dc81131cb`, 부호를 고친 scorer)으로 읽은 post hoc reading은 그대로 19개 중 4개예요: `c2-p2a`, `c2-p2b`, `c7-browsing`, `c7-office`. verdict은 아니에요.
- 기록은 `docs/rq0-run-record.md`의 2026-11-21 정정에 있어요.
