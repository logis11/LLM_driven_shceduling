# workload dataset rebuild — 바뀐 것, 부탁할 것, 같이 정할 것

> Status: memo · Created 2026-10-17 · Updated 2026-10-17
> 열림 — 인경민: simulator의 loader가 spawn된 child를 target으로 하는 WAKE를 받는 것(§3.1), RQ0 run 전에 남은 RQ0 gate spec의 simulator conformance 항목 (a)·(b)·(d)·(e)·(g)·(h)를 hand fixture로 보여 주는 것과 (g)에 대한 동의(§3.2), rebuild된 core set에서 regression check와 EDF 재측정(§3.3). 박이안: recognition log에 formatted prompt를 남길지, chat template이 넣는 날짜를 고정할지 기록할지(§5.2). 둘 다: 셋이 같이 정할 제안 둘(§6). 담당 인경민, 박이안.
> From 인지오 to 인경민, 박이안. 제 Phase 9, workload dataset rebuild에서 dataset을 다시 만들고 그 위에 서 있던 것들을 다시 하는 일이 끝났어요. 그동안 바뀐 걸 이 memo 하나에 모았어요: 바뀐 것(§1, §2), 각자한테 부탁할 것과 답(§3–§5), 셋이 같이 정할 제안(§6), 아직 열린 memo(§7), licence(§8). 급하면 §1, §3, §5, §6만 읽어도 돼요.

## 1. 한눈에 — 이번에 바뀐 것

2026-09-13에 archetype의 출처를 원문과 대조해서 나온 finding(`docs/memos/2026-09-13-critical-findings.md`)을 하나씩 원문으로 확인하고, 그걸로 workload dataset을 다시 만들었어요. 그 위에 서 있던 것들도 rebuild된 파일 기준으로 다시 했어요.

- **archetype library.** 29 entry예요: 28개는 우리가 CI에서 잰 값을 싣고(`category_source: meas`), `game-task-chain` 하나는 LAVD 발표(`lavd-ossna24`)가 출처예요(`dataset/archetypes.yaml`).
- **새 file set.** core set 51개(67 segment) 옆에 RQ0 gate spec의 sensitivity variant 78개와 generated layer 1,562개가 생겼어요(§2.3). core 파일 하나는 이름이 바뀌었어요: `c5-t3`이 2026-10-12부터 `c6-alias`예요 — task, archetype, seed는 같아요(`docs/data-contracts.md` §14).
- **그 위에 선 것들.** scoring spec(다시 freeze), guard spec(1.1), RQ0 gate spec(judging 19개, reporting 32개)을 rebuild된 파일 기준으로 다시 썼고(`harness/CHANGELOG.md`의 2026-10-09 entry), prior driver table의 문장과 pair review도 그렇게 다시 썼어요(§4.2).
- **형식에 더해진 것 둘.** 모든 task record의 `declared_class`(§2.1), 그리고 canonical workload 파일의 네 번째 top-level key `focus`와 telemetry의 focus(§2.2). simulator가 읽는 run file은 여전히 `meta.id`와 `events`뿐이고, `declared_class`는 그 안에 실려 와요.
- **형식은 그대로인데 새로 생긴 쓰임 하나.** rebuild된 compile tree에서 spawn된 child가 다른 spawn된 child를 WAKE해요. 지금 simulator의 loader는 이 파일들을 거부해요(§3.1). 인경민한테는 이 memo가 이 문제의 첫 알림이에요.
- **program의 끝.** depart가 pin된 program은 이제 instruction을 다 써서 끝나는 일이 없어요(§2.4).
- **config schedule.** switch의 drain과 entry의 index 순서가 contract 규칙이 됐어요(§2.5).
- **vocabulary.** `render`의 설명이 넓어졌어요. label은 그대로예요(§2.9).
- **licence.** code는 MIT, dataset의 data는 CC-BY-NC-SA-4.0이에요(§8).
- 형식 변경은 날짜별로 `docs/data-contracts.md` §14에, rebuild된 dataset은 `dataset/README.md`에 있어요. `dataset/build/`는 commit되지 않아요: `make -C dataset dataset variants generated`로 만들고 `make -C dataset check`가 manifest의 hash와 대조해요(`docs/data-contracts.md` §4). generated layer까지 다 만들면 약 6.8 GB예요.

## 2. 둘 다 — 바뀐 것

### 2.1 task의 scheduling class, `declared_class` (2026-10-09)

- 모든 task record — `arrive` event와 spawn-table entry 하나하나 — 가 `declared_class`를 필수로 가져요. 값은 `normal`과 `idle` 둘뿐이고 기본값은 없어요(`dataset/schema/workload.schema.json:111`; 필수로 적힌 곳은 `arrive`의 `:119`, spawn-table entry의 `:163`). task의 class는 그 task가 bind하는 archetype entry의 것이고, spawn된 child는 자기 child entry의 것이에요. nice는 싣지 않아요.
- `idle`은 `file-indexer`, `incremental-backup`, `game-download-idle` 세 entry에만 있어요(`dataset/archetypes.yaml:1528`, `:1653`, `:1456`). 그래서 idle task를 가진 core 파일은 일곱 개예요: `c1-indexing`, `c7-indexing`, `c2-p1b`, `c1-backup`, `c7-backup`, `c2-p3b`, `c2-p2a-idle`.
- **executor 규칙.** `idle` task는 다른 class의 task가 하나도 runnable하지 않을 때만 돌고, 그런 task가 깨어나면 곧바로 preempt돼요. FIFO를 포함한 모든 algorithm에서, configured algorithm이 정하는 것 아래에서 적용돼요(`docs/data-contracts.md` §4, 272번째 줄). simulator 쪽 할 일은 §3.2의 (e)예요.
- **visible projection.** task마다 class를 보여 주고, spawn table의 child는 이름과 class로 묶어 개수를 세어요(`docs/data-contracts.md` §4의 visible projection). harness의 mock daemon이 그렇게 만들어요(`harness/tools/tests/mocks/daemon.py:52`, `:58–59`).
- 이번 rebuild에서 제가 정하고 이 memo로 알리는 것: `c2-p2a-idle`(`c2-p2a`의 download를 `idle`로 돌리는 bounding 파일)은 judging set 밖, reporting이에요(`harness/experiments/rq0-gate.yaml:59–65`). native compile mode는 없어지고 single-lane set(`dataset/build/coreset-single/`)만 나가요. archetype contract는 v0.2예요(`docs/data-contracts.md` §14, 2026-10-09 entry).

### 2.2 telemetry의 focus (2026-10-11)

- canonical workload 파일에 네 번째 top-level key `focus`가 생겼어요: window focus를 가진 top-level task와 그 구간, `[{t_start, t_end, task}]`.
- **인경민:** run file(`meta.id`와 `events`)은 그대로예요. 지금 loader도 `meta.id`와 `events`만 읽어서 바뀔 게 없어요(`simulator/src/sim.cpp:892–928`).
- **박이안:**
  - visible projection: focus를 가진 task마다 그 구간 `focus: [{t_start, t_end}]`(`docs/data-contracts.md` §4).
  - telemetry 규칙 6: snapshot이 name → count multiset 옆에 focus를 가진 process의 이름 `focus`를 실어요(어느 window도 focus가 없으면 `null`). focus가 바뀌면 snapshot과 query point가 하나 생기고, 같은 이름의 두 instance 사이의 이동은 아무것도 바꾸지 않아요(`docs/data-contracts.md` §5).
  - telemetry shape 두 가지: `focus`(위 snapshot)와 `names`(`focus` field가 없는 같은 snapshot). query point는 두 shape에서 같아요. daemon은 shape를 필수 flag `--telemetry focus|names`로 받고(`docs/data-contracts.md` §11), recognition log는 보여 준 shape를 top-level `telemetry`에 적어요(같은 문서 §8). run 하나는 workload 하나 × condition 하나 × shape 하나 × (난수 condition이면) seed 하나예요.
  - 모든 condition이 같은 파일에서 두 shape로 돌고, 그 차이가 field의 측정된 값어치예요. harness의 records에는 identity column `telemetry`가 더해져 column이 25개가 됐어요(`docs/harness/metrics.md:67`). RQ0 gate spec은 `focus` 하나만 돌려요 — 그 세 condition은 telemetry를 읽지 않아요(`harness/experiments/rq0-gate.yaml:23`).
- 제가 혼자 정한 변경이라 이 memo로 알려요(`docs/data-contracts.md` §14, 2026-10-11 entry).

### 2.3 generated layer (2026-10-11, 2026-10-12)

- core set 옆에 generated set 다섯이 생겼어요: transition grid 480, return grid 720, flap-stress set 24, distractor grid 272, familiarity ladder 66 — 모두 1,562개. 전부 design이고 realism을 주장하지 않아요. mode마다 하나인 single-mode core 파일들의 task set을 `dataset/grids.yaml`이 조합해 만들어요.
- core set과 같은 compiler, schema, lint로 `dataset/build/<set>-single/`에 compile되고, set마다 manifest가 따로 있어요(`dataset/build.<set>.manifest.json`). 모든 CI run이 만들어요(`.github/workflows/dataset.yml:21`).
- 형식이 core set과 같아서 simulator와 daemon은 core set처럼 읽으면 돼요. 이 중 188개는 §3.1의 loader 문제에 걸려요.
- 실험 spec은 pin된 manifest에서 축으로 파일을 골라요(`files.select`, `pins.generated`; `harness/tools/harness/manifests.py`).

### 2.4 어떤 program도 instruction을 다 써서 끝나지 않아요 (2026-10-15)

- depart가 pin된 program은 이제 자기 loop가 다음에 할 blocking step으로 끝나요: wake로 움직이는 program은 마지막 wake의 channel에 WAIT 하나(wake N번에 WAIT N + 1개), timer로 움직이는 program은 tick이 depart 이후에 떨어지는 TIMER 하나, 아니면 unbounded LOOP. block된 채로 남아 있다가 pin된 depart가 지워요.
- depart가 pin되지 않은 task는 top-level이든 spawn된 것이든 `EXIT`로 끝나요.
- canonical lint가 둘 다 검사해요(`dataset/tools/wlc/linter.py:408–417`). 새로 실행되는 건 없어요: span 안의 CPU, wake, tick은 그대로이고 artifact의 byte만 바뀌었어요.
- **인경민:** instruction을 다 쓴 task를 끝난 것으로 보고(`simulator/src/sim.cpp:662`, `task_end` reason `exit`) depart 때 `task_end`를 한 번 더 내는(`on_depart`, `:838–848`) 경우는 이제 data에서 생기지 않아요.

### 2.5 config schedule — drain과 entry의 index 순서 (2026-10-17)

`docs/data-contracts.md` §7에 두 규칙이 적혔고, 적힌 그대로 지금부터 유효해요(§14, 2026-10-17 entry).

- **Drain.** MLFQ, EDF, LOTTERY에서 다른 algorithm으로 가는 switch가 어떤 task가 lane을 잡고 있을 때 stamp되면, lane이 다음에 빌 때 적용돼요 — 그 task의 slice나 지금 RUN이 끝나거나, preempt되거나, depart할 때. lane이 비어 있을 때의 switch, FIFO에서 나가는 switch, 같은 algorithm의 entry는 stamp된 시각에 적용돼요.
- **Order.** entry는 list 순서(index 순서)대로 적용돼요. switch가 drain 중일 때 stamp된 entry는 같은 algorithm이어도 그 뒤에서 기다렸다가 같은 순간에, 그 뒤에 적용돼요.
- 2026-09-09에 정한 "같은 algorithm entry는 stamp된 시각에 적용"(algorithm-switch memo §7)은 이렇게 고쳐졌어요.
- reference simulator는 2026-10-10부터 둘 다 이렇게 해요(`on_config_apply`와 `dispatch`, `simulator/src/sim.cpp:570–580`, `:823–828`; 인경민의 drain 규칙 U3, `simulator/memo/memo_261010.md` Part B). simulator 쪽에 남은 일은 없어요.

### 2.6 dataset 쪽만 묶는 규칙 둘 (2026-10-16)

`docs/data-contracts.md` §14의 2026-10-16 entry 중 두 규칙은 dataset 쪽만 묶고 인경민과 박이안의 프로그램과는 상관없어요. `make lint`의 freeze에서 timeline의 bound value에 `meas-pending`이 붙어 있으면 library param처럼 fail해요(`lint_bound_sources`). library, timeline, recipe, grid 정의가 싣는 `meas-ci:<workflow>:<campaign>` tag는 모두 `dataset/meas-releases.yaml`의 release로 풀려야 해요(`lint_releases`) — 그 파일은 campaign마다 GitHub release와 asset의 SHA-256을 적어요. 같은 entry의 세 번째 규칙, orchestrator의 `WAIT children:<id>`는 §3.2의 (g)예요.

### 2.7 문서 속 이름 두 개

내용은 그대로이고 이름만 바뀌었어요.

- `docs/research-claims.md`의 chain은 'link 1'–'link 7', 일곱 개예요(전에는 'six links'라고 적혀 있었어요). C1–C7은 core set의 파일 group 이름으로만 남아요(파일 id에 들어 있어요).
- dataset의 layer는 번호 대신 이름으로 불러요: archetype library, scenario catalog, timelines. 'Layer 1/2'는 evaluation layer(recognition accuracy와 consumer performance)만 뜻해요.

### 2.8 '주장하지 않는 것'에 하나 더

`docs/research-claims.md`의 'What is not claimed'에 entry가 하나 생겼어요: scheduling 결과가 다른 CPU나 다른 machine 구성으로 옮겨 간다고 주장하지 않아요. CPU 값은 모두 hosted runner의 AMD EPYC 7763 core 하나의 것이에요(Xvfb, GPU 없음, sound device 없음, 사람 없음). 다른 CPU는 program마다 다른 배율로 속도를 바꾸는데(Xeon Platinum 8573C에서 `cc1`은 EPYC 시간의 0.72배, `fixdep`은 0.50배), venue variant의 공통 배율 0.8–1.25는 그걸 재현하지 않아요. recognition은 CPU 값을 읽지 않아요.

### 2.9 vocabulary의 `render` 설명 (2026-10-17)

- `docs/recognition-vocabulary.md` §1의 `render` 설명이 'an offline 3D/graphics render'에서 'an offline render — a 3D scene or a video project rendered to a file'로 넓어졌어요(같은 문서 §5의 2026-10-17 entry). `transcode`(있는 media의 변환)와는 그대로 구별돼요. label도 파일도 안 바뀌어요.
- dataset의 render segment(`c1-render`, `c7-render`, `c2-p3a`의 두 번째 segment(60–326 s), render mode의 generated 파일)는 모두 Kdenlive의 video project export(`kdenlive_render`)를 bind하고, 3D scene은 없어요.
- recognizer latency campaign이 쓴 prompt(`dataset/tools/meas/llm/prompt.json`)는 측정한 그대로 옛 설명을 가지고 있어요.
- 제가 정한 변경이라 이 memo로 알려요.

## 3. 인경민에게 — 부탁할 것

### 3.1 loader — spawn된 child를 target으로 하는 WAKE

- rebuild된 compile tree는 job마다 spawn table의 member들을 job의 부모-자식 순서대로 WAIT/WAKE로 이어요: `make`의 object job은 여섯 member(`sh`, `gcc`, `cc1`, `as`, `fixdep`, `rm`), `c7-compile`의 `dkms` job은 6–10 member예요(`dataset/tools/wlc/compiler.py:563`, `:641`). 그래서 spawn된 child가 다른 spawn된 child를 깨워요. schema는 WAKE target으로 어느 task id든 허용하고, canonical lint는 spawn된 child의 WAKE target이 top-level task의 것처럼 풀리는지 검사해요(`dataset/tools/wlc/linter.py:394`).
- 지금 loader는 id map을 `arrive` event로만 채우고(`simulator/src/sim.cpp:899–905`) spawn-table program도 그 map으로 compile해서(`:917`), 이 파일들에서 "WAKE target is not a top-level task"로 멈춰요(`:876`).
- 걸리는 파일(2026-10-17 build, 1,691개 중 201개):
  - core 다섯: `c1-compile`, `c7-compile`(judging), `c3-workday`, `c4-compile`, `c6-dual`(reporting).
  - RQ0 gate spec이 돌리는 compile variant 여덟: `c1-compile`과 `c7-compile`의 `@corner-high`, `@corner-low`, `@venue-x0.8`, `@venue-x1.25`.
  - generated 188개: transition grid 60, return grid 90, distractor grid 32, familiarity ladder 6.
- spawn된 program 안의 WAKE는 모두 spawn된 child를 target으로 해요: `c1-compile`, `c3-workday`, `c4-compile`, `c6-dual`에 각 43,620개, `c7-compile`에 25,269개, 201개 파일 전체에 855,150개.
- dataset은 이 쓰임을 유지해요. loader가 spawn table의 child id 중에서도 WAKE target을 찾도록 고쳐 줘요.

### 3.2 RQ0 run 전에 남은 simulator conformance

RQ0 gate spec의 statement `simulator-conformance`(`harness/experiments/rq0-gate.yaml:325–357`)가 정한 여덟 항목이에요. RQ0 run은 `random`과 `oracle`의 차이가 잴 만큼 큰지 판정하는 run이고, hand fixture를 simulator로 replay해서 trace를 줄 단위로 맞춰 보이기 전에는 RQ0 run을 시작하지 않아요. (c)와 (f)는 지금 코드에 있고, 나머지 여섯이 남았어요.

- **(a) zero-wait `ready` line — 남음.** blocking primitive(`WAIT`, `TIMER`, `SLEEP`, fork slot)가 끝날 때마다 `ready` line 하나, block하지 않았으면 wait 0으로, occupancy 안에서는 `run_start` 뒤에(`docs/harness/metrics.md` §11 1번; 2026-09-07 trace-clarifications memo). 지금 코드는 밀린 TIMER tick과 mailbox로 채워진 WAIT를 `ready` line 없이 지나가고(`simulator/src/sim.cpp:675–678`, `:686–691`), RUN이 block 없이 다음 RUN으로 이어지면 `run_end` 없이 `ready(cause=arrive)`로 다시 줄을 세워요(`advance`, `:636–644`).
- **(b) TIMER skip rule — 남음.** TIMER에 닿았을 때 이미 지나간 tick이 있으면 가장 최근 tick을 소비하고 나머지는 건너뛰어요. 건너뛴 tick마다 일 없이 `met: false`인 `deadline` line 하나예요(2026-10-07 TIMER memo). 지금 코드는 backlog rule이에요: 밀린 tick을 그 자리에서 하나씩 소비해요(`:675–678`). harness는 이미 skip rule로 읽어요(`docs/harness/metrics.md` §6.2). simulator가 skip rule을 구현할 때까지 interpretation contract와 simulator guide는 backlog rule을 그대로 적어 두고, 구현되면 TIMER 문서들을 skip rule로 고칠게요.
- **(c) algorithm switch — 코드에 있음.** MLFQ로의 switch는 cold start(모든 task가 top queue), 같은 algorithm entry는 holder가 받은 slice를 끝까지 써요(인경민의 U1·U2 규칙: `:205–209`, `:582–610`).
- **(d) `batch_bandwidth_cap` — 남음.** behavioural batch class에 work-conserving ceiling으로 적용해요(2026-09-09 batch-class memo). 지금 loader는 이 field를 읽지 않아요(`load_schedule`, `:937–967`).
- **(e) strict idle class — 남음.** §2.1의 규칙이에요(2026-10-08 declared-class memo). 지금 loader는 `declared_class`를 읽지 않아요.
- **(f) EDF의 chain stage — 코드에 있음.** frame chain의 깨어난 stage가 deadline class에서 frame의 deadline을 물려받아요(`:34–38`, `deliver` `:787–798`).
- **(g) orchestrator의 `WAIT children:<id>` — 동의와 구현을 부탁해요.** spawn한 child가 모두 끝났을 때(살아 있는 마지막 child가 끝날 때) 완료되고, WAIT 시점에 살아 있는 child가 없으면 block 없이 zero-wait `ready` line과 함께 지나가요. `build-orchestrator`와 `module-build-orchestrator`가 마지막 FORK 뒤에 두는 step이고(`dataset/tools/wlc/compiler.py:620`, `:705`), compiler의 첫 commit부터 있었어요. 지금 코드는 `children:`을 보통 channel로 다뤄서(`on_task_end`, `:759–768`은 fork slot만 돌려줘요) orchestrator가 run 끝까지 block된 채 EXIT에 닿지 않아요. 그러면 `c1-compile`의 build turnaround(judging, weight 1.0, `harness/scoring/scoring-spec.yaml:112`)가 모든 condition에서 똑같이 censored돼요. 이 규칙은 `docs/data-contracts.md` §4 Example B와 §14 2026-10-16 entry, interpretation contract의 `WAIT(channel)`·FORK 글에 제안으로, 인경민이 동의하면 유효한 것으로 적혀 있어요. RQ0 gate spec은 run에 이걸 요구해요.
- **(h) invocation contract — 남음.** runner가 부르는 그대로예요: workload와 config schedule은 `--workload`, `--schedule`으로, trace 경로는 `--out-trace`로, 위치 인자 없이; trace는 그 파일에 쓰고 stdout은 무시; trace를 썼을 때만 exit 0; 같은 argument line이면 byte-identical trace; trace header의 `sim`은 runner의 machine configuration이 이름 붙인 version string(`docs/data-contracts.md` §11, contract 10). 지금 코드는 `<workload.json> [<config-schedule.json>]`를 위치 인자로 받고 trace를 stdout에 쓰며, `sim`은 `"src/sim"`으로 고정이에요(`main` `:970–988`, `:514–516`).

### 3.3 rebuild된 core set에서 regression check, EDF 재측정

- 마지막 regression check는 rebuild 전 24개 파일 위에서였어요(`simulator/memo/memo_261010.md` Part B의 regression, Part D의 `src/sim.cpp` port 확인). §3.1의 loader가 고쳐지면 rebuild된 core set 51개와 variant 78개에서 다시 돌려 줘요.
- 함께, 인경민 backlog의 EDF 재측정(memo_261010 Part F; `simulator/notes/note-for-jioh-edf-chain-stage-class.md`의 Answer): rebuild된 `c1-gaming`과 `c2-p2b`에서 p2 pair(`c2-p2a`와 `c2-p2b`)의 두 EDF row가 `game.chain.1`의 frame에서 여전히 차이가 없는지. `c1-gaming`에는 compositor가 없고, `c2-p2b`의 background는 이제 unattended upgrade(`package-upgrade`, 이름 `unattended-upgr`)예요. 이 재측정이 대조할 prior table의 gaming row는 §4.2에 있어요.

## 4. 인경민에게 — 답과 알림

### 4.1 저한테 물은 질문의 답

memo_261010 Part F의 'Questions for jioh — all written up' 표 그대로예요.

- **TIMER backlog 대 frame drop**(`simulator/notes/note-for-jioh-timer-backlog-vs-drop.md`): skip rule로 정했어요(2026-10-07 TIMER memo). 구현은 §3.2의 (b)예요.
- **`fork_cap`**(`simulator/notes/note1010.md`): `make`의 build(`build-orchestrator`; core의 `c1-compile`, `c3-workday`, `c4-compile`, `c6-dual`과 generated layer의 compile 파일)에서는 object job 하나가 spawn-table entry 여섯 개이고, 끝난 member는 `sh`가 job을 끝낼 때까지 CPU 없이 기다려요. 그래서 거기서는 `fork_cap` = timeline의 `parallelism_cap` × 6(`c1-compile`은 8 × 6 = 48, `dataset/tools/wlc/compiler.py:605`)이 make의 jobserver가 세는 동시 실행 job 수를 정확히 묶어요 — cap은 `make -jN`을 따른 것이고, critical-findings memo의 B3(`-j8`에서 측정된 최대 동시 process 16)의 '`-jN`의 단위가 process냐 make job이냐'는 make job으로 정해졌어요. `c7-compile`의 DKMS module build(`dkms`, `module-build-orchestrator`)도 같은 `fork_cap` = `parallelism_cap` × 6(48)을 쓰지만(`:693`), 그 job은 member가 6개, 8개, 10개예요(spawn-table entry 9,980개 = job 1,557개: 6개짜리 1,325, 8개짜리 145, 10개짜리 87; 그 sensitivity variant 넷도 같아요). 그래서 거기서 cap은 동시에 살아 있는 child 48개를 묶고, 동시 실행 job 수를 정확히 묶지는 않아요. compiler는 spawn table을 쓰는 task마다 `fork_cap`을 함께 써서(`:128–130`), spawn table이 있는 build 파일 201개 어디에도 `fork_cap` 없는 spawn table은 없어요.
- **`mock-switch` 질문 1**(slice가 끝났을 때 더 높은 queue에 task가 기다리는 경우): mock이 틀렸어요. MLFQ 규칙 2대로 44600에 `probe`가 lane을 가져가도록 fixture를 다시 유도했어요(`harness/tools/tests/fixtures/mock-switch/worked.md`, 2026-10-16).
- **질문 2**(경쟁자 없는 slice 만료): 한 occupancy로 하자는 제안이에요 — §6.1.
- **질문 3**(simulator guide §4½의 listing이 instruction 하나 모자람): 끝의 WAIT는 이제 data의 규칙이고(§2.4), guide의 §4½ program도 세 번째 WAIT로 끝나요(`docs/simulator/simulator-guide.md:171–173`).
- **제가 물었던 executor 질문 셋**도 모두 답이 있어요: LOTTERY에서 non-batch class가 비었을 때는 simulator가 정한 대로 — 두 class가 모두 runnable할 때만 `batch_share`로 class를 고르고, 아니면 runnable한 class 안에서 균등하게 뽑아요(`simulator/src/sim.cpp:329–334`, `:364–372`); EDF에서 chain의 깨어나는 stage는 deadline class예요(2026-10-10 답); RUN 중에 온 keystroke는 깊이를 가진 mailbox에 쌓여요(`docs/harness/metrics.md` §11 2번).

### 4.2 prior table의 gaming row — EDF chain-stage 답의 글

2026-10-10의 답(frame chain 전체가 EDF deadline class이고 head의 deadline을 물려받음)은 `daemon/driver-table/prior.yaml`의 gaming row 둘(`:209–232`)과 pair review(`docs/daemon/prior-table-pair-review.md`)에 rebuild된 파일 기준으로 적혔어요.

- EDF가 어떤 residual task보다 frame을 먼저 처리하니 cap은 chain term에 닿지 않고, 두 gaming row(`background_wanted` `true`의 cap 0.333, `false`의 cap 0.05)는 chain term에서 같아요.
- boot MLFQ 대비 차이는 EDF 대 MLFQ의 결과예요: MLFQ의 100 ms boost가 slack이 1.7 ms 미만인 frame 안에서 upgrade에게 10 ms slice를 줘요.
- chain은 `c1-gaming`에서 lane의 0.9, `c2-p2a`·`c2-p2b`에서 0.95로 lane 안에 들어가고, `c3-evening`에서는 1.45로 넘쳐요 — utilisation 1을 넘으면 EDF는 miss를 막지 못하고 순서만 정해요.
- `c2-p2a`의 download는 쉬지 않고 돌아서 batch class예요.

### 4.3 MLFQ boost timer는 적용된 entry마다 다시 시작

harness는 reference simulator가 하는 그대로 읽어요: boost timer는 적용된 MLFQ entry마다, 같은 algorithm entry도 포함해 다시 시작돼요(`simulator/src/sim.cpp:597`, `:603`, `:210`). `boost_window`는 적용된 entry마다 grid를 새로 깔아요(`docs/harness/metrics.md` §6.10, §11 9번; `harness/tools/harness/primitives.py:241–275`). 그래서 memo_261010 Part F의 'Ours to decide and write down' 표에서 "Same-algorithm MLFQ entry: restart the boost grid?" 줄은 지금 동작(restarts)으로 정해졌다고 적어도 돼요.

### 4.4 첫 instruction이 block하는 task의 arrival

harness mock도 이제 reference simulator가 하는 그대로 해요: 첫 instruction이 WAIT인 task(LOOP의 body도, spawn된 child도 포함)는 저장된 wake가 없으면 arrival step에서 block되고, `ready` line도 occupancy도 없어요(`harness/tools/tests/mocks/simulator.py`; `docs/harness/metrics.md` §11 5번; simulator의 `on_arrive` `:734–738`, `spawn` `:740–755`). 그래서 memo_261010 Part F의 'Ours to decide and write down' 표에서 "Zero-length occupancy for an arriving task whose first instruction blocks" 줄("none, only `x_block`. The mock has one")은 지금 동작(occupancy 없이 `x_block`만)으로 정해졌다고 적어도 돼요.

### 4.5 `simulator/src/notes.md` §4의 gap 1과 gap 3

두 gap이 인용한 simulator guide 문장이 고쳐졌어요. 인경민의 tree는 건드리지 않았어요.

- **gap 1**(`batch_bandwidth_cap`을 읽지 않음): guide §5는 이제 configuration이 정하는 cap 하나, `batch_bandwidth_cap`을 batch class의 work-conserving ceiling으로, 아직 구현되지 않은 것으로 적어요(`docs/simulator/simulator-guide.md:221`). gap은 그대로 §3.2의 (d)예요.
- **gap 3**(TIMER의 t₀): guide §9.2가 닫혔어요 — t₀는 task의 arrival이고, simulator가 arrival step에서 leading TIMER를 실행하니 이미 그렇게 하고 있어요(`simulator/src/sim.cpp:674`, `on_arrive` `:734–738`). 남은 일은 없어요. memo_261010 Part F의 'TIMER t₀ (D4)' 줄도 같은 답이에요.

### 4.6 workload 끝 이후의 config entry

`docs/data-contracts.md` §7의 End 규칙(2026-09-06 freeze)은 workload 끝(terminal snapshot의 시각)이나 그 뒤에 stamp된 entry를 simulator가 무시한다고 해요. reference simulator는 그런 entry도 적용하고 trace에 적어요: `load_schedule`은 entry를 다 받고, `set_schedule`이 하나씩 event queue에 넣고, `run`이 모든 event를 처리해요(`simulator/src/sim.cpp:540–545`, `:937–967`, `:513–534`). 숫자는 바뀌지 않아요: harness가 `T_end`나 그 뒤의 `config_applied` line을 버려요(`harness/tools/harness/primitives.py:114–117`; `docs/harness/metrics.md` §4). contract와 harness는 그대로예요.

### 4.7 starvation safety net

memo_261010 Part F의 'Implementation owed'에 있는 starvation safety net은 2026-10-08 declared-class memo에 적은 대로 만들지 않아요. executor에는 자기 starvation window가 없고, 어떤 task가 30 s보다 오래 기다린 run은 harness의 `starvation_floor` guard가 fail시켜요(`docs/simulator/simulator-guide.md:221`; `harness/guards/guard-spec.yaml:143–148`).

### 4.8 파일 크기

simulator가 load할 core 파일은 가장 큰 것이 187,601,795 B(약 187.6 MB, `c6-dual`), core set 51개 합이 678,172,716 B(약 678 MB)예요(2026-10-17 build). 2026-10-09 rebuild 때 기록한 190 MB, 681 MB를 대신해요. variant 78개와 generated 1,562개는 그 밖의 set이에요. `c6-dual` 하나의 trace는 mock simulator로 약 4,200만 줄이었어요.

## 5. 박이안에게

### 5.1 바뀐 입력

- visible projection: task마다 `declared_class`(§2.1)와 focus 구간(§2.2).
- telemetry: 규칙 6의 focus holder, shape `focus`/`names`, 필수 flag `--telemetry`, recognition log의 top-level `telemetry`(§2.2).
- generated layer 1,562개도 core set과 같은 형식이에요(§2.3).
- rebuild 전 파일로 뽑은 recognition log는 다시 뽑아야 해요.

### 5.2 frozen contract 질문 — formatted prompt와 chat template의 날짜

recognition log(`docs/data-contracts.md` §8)는 frozen이라 바꾸려면 우리 셋의 동의와 §14 entry가 필요해요(§13). 같은 telemetry snapshot이 어느 날 돌려도 같은 input이 되게 하려고 두 가지를 물어볼게요.

1. recognition log에 formatted prompt(chat template을 적용한 뒤 model이 받는 그대로의 text)를 남길까요?
2. chat template이 넣는 날짜 — Llama 3.1의 "Today Date" — 를 prompt에서 고정할까요, log에 기록할까요?

지금 contract와 `daemon/`에는 둘 다 적힌 데가 없어요.

## 6. 둘 다 — 셋이 같이 정할 제안

### 6.1 경쟁자 없이 MLFQ slice가 끝날 때의 trace (`mock-switch` 질문 2)

- **제안.** holder의 slice가 끝났는데 다른 runnable task가 없으면 occupancy 하나가 이어져요: holder는 강등되고(`x_mlfq_level`) lane에 남고, `run_end(preempt)`와 `run_start`의 쌍은 없어요.
- **근거.** Linux v6.12 `kernel/sched/core.c`의 `__schedule()`은 `prev == next`일 때 switch를 세지 않아요(`docs/references.md`의 `linux-sched-core`).
- **바뀌는 것.** 각 task가 받는 CPU는 어느 쪽이든 같아요. 바뀌는 건 MLFQ baseline trace의 `run_end(preempt)` 수이고, `preempt_count`는 보고만 되고 점수 term에는 없어요. 인경민이 RUN→RUN fix(memo_261010 Part C)와 함께 구현하면 MLFQ baseline trace가 한 번 바뀌어요. harness mock(`mock-switch`)은 이미 이렇게 해요.
- 둘 다 동의하면 metrics doc과 interpretation contract에 적고 `docs/data-contracts.md` §14 entry를 남길게요.

### 6.2 주장의 표현

- 지금 `docs/research-claims.md` ## The claim이 실험에 거는 형태는 "a language model reading process names recovers the difference, and the strongest name table cannot" — recognition 기준이에요.
- **제안.** scheduling 점수로 적어요: model이 process 이름을 읽고 고른 configuration이 RQ0 judging 파일들에서 strongest name table의 configuration보다 점수가 좋다. recognition accuracy(RQ1, model이 process 이름과 focus holder에서 상황을 읽는가)는 그 차이를 설명하는 쪽이 되고, headline은 RQ5(측정 도구가 건전한가)의 ladder(fixed, strongest name table, variant A, perfect recognition, perfect config)에서 model이 perfect recognition의 이득 중 얼마를 잡는지, (fixed − model) / (fixed − perfect recognition)이에요.
- claims 문서는 우리 셋의 것이라 동의 전에는 안 고쳐요.

## 7. 아직 열린 memo

각 memo의 머리 줄이 적은 부탁과 담당 그대로예요.

**인경민**

- `2026-09-07-trace-clarifications-for-the-simulator.md` — §8 1번, zero-wait `ready` line(§3.2의 (a)). 2–4번은 답이 있어요.
- `2026-09-08-algorithm-switch-semantics-for-the-simulator.md` — §6의 simulator 쪽 셋: demotion과 boost마다 level을 단 `x_mlfq_level {t, task, from, to}`(지금은 level 없는 `x_mlfq_demote`, `x_mlfq_boost`), 정해진 세 규칙을 simulator의 semantics notes에, switch를 건너 남은 demand가 보존되는지의 unit test.
- `2026-09-09-batch-class-rule-for-the-simulator.md` — §7 3번, `batch_bandwidth_cap`과 그 accounting window(§3.2의 (d)), 그리고 5·6번(semantics notes의 규칙, unit test 둘).
- `2026-09-11-invocation-contract.md` — simulator가 contract 10의 명령 모양으로 실행되는 것(§3.2의 (h)).
- `2026-10-07-timer-skip-rule-for-the-simulator.md` — §6: skip rule(§3.2의 (b))과 zero-wait `ready` line((a)), 그 뒤 interpretation contract의 TIMER row 확정.
- `2026-10-08-declared-scheduling-class.md` — §4 1번, executor의 idle 규칙(§3.2의 (e)); 4번, status memo(`simulator/memo/memo_261001.md`) §6의 답 1·2를 RQ0 gate spec의 statement `executor-assumptions`가 기다리는 정식 답으로 확인.

**박이안**

- `2026-09-07-repeat-samples-for-the-daemon.md` — §3, 한 query point의 독립 sample N개를 묶는 repeat index를 recognition log에 두고 `docs/data-contracts.md` §8에 한 줄로 정하기(`docs/harness/metrics.md` §7의 run-to-run consistency가 이걸 기다려요).
- `2026-09-11-invocation-contract.md` — daemon이 contract 10의 명령 모양으로 실행되는 것. daemon program은 아직 이 저장소에 없어요.
- `2026-09-12-rq0-pre-registration.md` — §5, `random`의 읽기와 N = 100을 daemon 쪽에서 확인(RQ0 gate spec의 statement `random-reading`).

**인지오**

- `2026-09-20-dataset-validity-review.md` — §3, stability-ledger 요약(허용오차를 만족한 양, 예외 class마다 실린 양, 가장 큰 half-width): slice들의 pooled record에서 script로 계산해서 `docs/workload/measurement-overview.md`의 stability 부분에, 이번 dataset rebuild를 마무리하는 measurement audit과 함께 실을게요.

## 8. licence

- **code:** MIT, 저장소 root의 `LICENSE`.
- **dataset의 data:** CC-BY-NC-SA-4.0, `dataset/LICENSE`. 대상은 `dataset/` 아래에서 code(`dataset/tools/`, `dataset/Makefile`)와 136M Keystrokes window를 뺀 모든 파일, 그것에서 compile된 workload(`dataset/build/`, commit된 manifest가 pin하는 그대로), campaign의 raw record를 담은 measurement release의 asset(`dataset/meas-releases.yaml`이 나열하는 것)이에요.
- 저작권자는 둘 다 Jioh In, Kyungmin Inn, Ian Park이에요.
- `dataset/stimulus/`의 input stream과 `dataset/meas/streams/`의 SWELL-KW window는 SWELL Knowledge Work dataset(Koldijk et al., 2014; DANS, CC-BY-NC-SA-4.0)에서 가져왔고, `dataset/LICENSE`가 출처를 밝혀요.
- `dataset/meas/streams/aalto-*` window와 `aalto-windows.json`(136M Keystrokes dataset, Dhakal et al., 2018)은 licence의 대상이 아니에요: 출처의 조건(비상업적 사용, 저자 표시) 그대로 배포되고 `dataset/LICENSE`는 그것에 대한 권리를 주지 않아요.
