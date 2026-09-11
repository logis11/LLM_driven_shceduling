# Coreset 안내 — 50개 workload를 하나씩 뜯어보기

> Status: draft · Created 2026-09-08 · Updated 2026-09-11

이 문서는 **공부용 문서**예요. dataset이 무엇이고, 어떻게 만들어지고, 50개 coreset 파일 각각이 무슨 상황을 담고 있으며 어떤 숫자를 갖고 있는지를 OS/시스템 지식이 거의 없는 사람 기준으로 풀어 써요. 설계의 규범적 근거는 building-plan(`docs/workload/building-plan.md`), archetype의 규범적 정의는 archetype-plan(`docs/workload/archetype-plan.md`), 실행 semantics는 interpretation contract(`docs/simulator/interpretation-contract.md`)에 있어요. 이 문서는 그 셋을 읽을 수 있게 만드는 다리이고, 숫자는 2026-09-08에 `make dataset`으로 빌드한 `coreset-single`에서 직접 읽은 값이에요.

읽는 규칙: term은 영어 그대로, 다른 문서는 절 번호 대신 내용으로 가리켜요.

---

## 목차

1. dataset이 실험에서 하는 역할
2. 세 층 구조 — archetype, scenario, timeline
3. 여섯 가지 primitive — task의 program
4. archetype 12개 — 각각 어떤 프로그램인가
5. compile — timeline이 workload가 되기까지
6. canonical workload file의 해부
7. recognizer가 보는 것 — telemetry snapshot과 query point
8. demand와 utilization — 의자를 얼마나 요구하나
9. 일곱 그룹 C1–C7 — 각 그룹이 답하는 질문
10. 50개 파일 상세
11. 파일들 사이의 관계 — 무엇이 무엇에서 파생됐나
12. 알아둘 특이점과 열린 항목
13. 용어 정리

---

## 1. dataset이 실험에서 하는 역할

이 프로젝트의 실험은 "process 이름에서 상황을 읽어내면 scheduling이 좋아지나"를 묻는 거예요. 그 질문을 물으려면 **정답을 아는 상황**이 필요해요. 진짜 사용자의 컴퓨터에는 정답이 없어요. "지금 이 사람은 게임 중이고 다운로드를 기다리는 중이다"를 누군가 label로 적어줘야 하는데, 실제 machine에서는 그걸 알 수 없으니까요.

그래서 상황을 **만들어요.** 각 workload 파일은 "이런 process들이 이런 시각에 등장해서 이렇게 행동하고, 그동안 machine의 진짜 상황은 이것이다"를 완전히 적은 script예요. 이 script가 곧 실험이에요. 실험의 input이 아니라 실험 그 자체.

파일 하나는 세 audience에게 세 조각으로 나뉘어 보여요.

| audience | 보는 것 | 못 보는 것 |
|---|---|---|
| **recognizer** (daemon 안) | process **이름**과 개수. `code ×1, python3 ×1` | 행동, 정답 |
| **simulator** | 각 task의 **program**. "3 ms 일하고 keystroke를 기다림" | 이름, 정답 |
| **harness** | **정답** (`ground_truth`). "60–180초는 ml-train" | (전부 봄. 채점자니까) |

이 비대칭이 실험의 근간이에요. recognizer가 행동 통계를 보면 "이름에서 의미를 읽는다"는 주장이 오염되고, simulator가 이름을 보면 executor가 condition마다 달라져요.

또 하나. **compile 시점에 모든 randomness가 해소돼요.** keystroke가 언제 오는지, 각 burst가 몇 µs인지, 컴파일 자식이 몇 ms 일하는지가 전부 파일에 구체적 숫자로 적혀 있어요. simulator는 주사위를 던지지 않아요. 그래서 어떤 condition으로 돌리든 모든 task는 byte 단위로 같은 일을 요구하고, 결과 차이는 scheduler 설정 차이로만 생겨요.

---

## 2. 세 층 구조 — archetype, scenario, timeline

dataset은 세 층으로 쌓여 있고, 아래층은 위층을 절대 참조하지 않아요.

```
Layer 1  ARCHETYPE LIBRARY   한 종류의 process가 어떻게 행동하나     dataset/archetypes.yaml
Layer 2  SCENARIO CATALOG    어떤 process들이 같이 나타나나 (S1–S18)  docs/workload/scenario-catalog.md
Layer 3  TIMELINES           scenario들이 시간 위에 어떻게 배치되나    dataset/timelines/coreset/*.timeline.yaml
                                        │
                                        ▼  wlc (workload compiler) + seed
                              CANONICAL WORKLOAD JSON                dataset/build/coreset-single/*.workload.json
```

**Layer 1, archetype.** "process 한 종류가 scheduler 눈에 어떻게 보이나"의 generative model. scheduler에게 process는 이름도 의미도 없고 오직 event stream이에요. 언제 runnable해지고, 얼마나 실행하고, 무엇을 기다리고, 누구를 깨우고, 언제 fork하고 exit하는가. archetype은 그 stream을 만드는 규칙 + parameter 분포예요. 이름은 절대 안 갖고 있어요. `video-playback`이라는 archetype은 "16.7 ms마다 6.7 ms 일한다"만 알지 그게 `mpv`인지 `vlc`인지 몰라요.

**Layer 2, scenario.** "어떤 process들이 현실에서 같이 나타나나"의 목록. S1(문서 작업: `soffice.bin`, `evince`)부터 S18(시스템 기본: `gnome-shell`, `Xorg`, …)까지 18개. 각 행은 외부 출처(PCMark, SYSmark, CpsMark+, ananicy 카탈로그, LAVD 논문 등)로 근거를 대요. 숫자는 없어요. 이름과 조합만.

**Layer 3, timeline.** 사람이 쓰는 authoring 파일. segment(시간 구간 + label)와 task(이름, archetype, 등장/퇴장 시각)를 시간축 위에 배치해요. 숫자 parameter는 여기 없어요. archetype id로만 참조하고, archetype이 `binding_params`로 요구하는 손잡이(총 일의 양, spawn 개수, lane_share)만 채워요.

이렇게 나눈 이유:
- 문헌이나 측정이 바뀌면 archetype 하나만 고치면 돼요. 파일 수십 개를 안 건드려요.
- **이름과 행동이 분리**돼요. C5(familiarity ladder)는 "같은 archetype, 다른 이름"으로 정의돼요. recognition 차이가 있으면 이름 때문이라고 확신할 수 있어요.
- C6의 "chrome이라는 이름을 단 batch job"도 timeline에서 `(name: chrome, archetype: cpu-batch)`로 그냥 쓸 수 있어요.

timeline 하나를 실제로 보면:

```yaml
# dataset/timelines/coreset/c2-p1a.timeline.yaml (전체)
meta:
  id: c2-p1a
  seed: 201

segments:
  - {from: 0s, to: 60s, mode: dev, attributes: {background_wanted: true}, scenario: [S11]}
  - {from: 60s, to: 180s, mode: ml-train, attributes: {background_wanted: true}, scenario: [S11, S12]}

tasks:
  - {id: editor, name: code, archetype: desktop-interactive, arrive: 0s, depart: 180s}
  - {id: hog, name: python3, archetype: cpu-batch, arrive: 60s, bind: {total_work: 130s}}

focus:
  - {from: 2s, to: 178s, task: editor}
```

- `segments`: 0–60초는 `dev`, 60–180초는 `ml-train`. 둘 다 `background_wanted: true`. `scenario`는 근거 tag.
- `tasks`: `editor`는 `code`라는 이름으로 `desktop-interactive`처럼 행동하고 0초에 와서 180초에 사용자가 닫음. `hog`는 `python3`라는 이름으로 `cpu-batch`처럼 행동하고 60초에 와서 130초짜리 일을 함. 퇴장 시각 없음(일이 끝나면 스스로 나감).
- `focus`: 사용자의 주의가 어디에 있나. 2–178초 동안 `editor`. **keystroke는 focus window 안에서만 생성돼요.** 이게 "interactive"의 정의예요.

---

## 3. 여섯 가지 primitive — task의 program

archetype의 program은 여섯 명령으로 써요. simulator 입장의 뜻과 손님 비유(CPU는 의자 하나, task는 손님):

| primitive | simulator에게 | 비유 |
|---|---|---|
| `RUN(N)` | N µs만큼 lane time을 소비. 중간에 preempt되면 남은 양이 보존됨 | 앉아서 N만큼 일함. 끌려나면 다음에 마저 함 |
| `SLEEP(N)` | 지금부터 N µs 뒤에 runnable. 상대 시간 | N만큼 잠 |
| `TIMER(P)` | t₀ + k·P의 절대 격자에서 다음 tick까지 block. **지나간 tick은 backlog로 쌓여 즉시 완료** | P마다 울리는 알람. 못 들은 알람은 밀려서 연달아 울림 |
| `WAIT(channel)` | 그 channel에 wake가 올 때까지 block | 부를 때까지 기다림 |
| `WAKE(target)` | target task를 runnable로 | 옆 손님을 깨움 |
| `FORK` | spawn table의 다음 자식을 만듦. 살아 있는 자식이 cap이면 block | 동행을 부름. 자리가 없으면 기다림 |
| `EXIT` | 자기 자신을 끝냄 | 집에 감 |
| `LOOP` | 제어 흐름. body를 N번 또는 무한 반복 | (명령 아님) |

**`TIMER`와 `SLEEP`의 차이**가 중요해요. `SLEEP(16667)` loop는 늦게 깨어날수록 다음 것도 밀려요. 부하가 걸리면 demand가 스스로 줄어들어서, scheduler가 못할 때 정확히 그 신호가 사라져요. `TIMER(16667)`은 격자가 고정이라 늦으면 밀린 tick이 쌓여요. 진짜 60 fps 게임처럼 "따라잡으려고 몸부림"쳐요. 그래서 주기적인 것은 전부 TIMER예요.

**`WAIT`의 channel** 두 종류. `input:<task id>`는 run file의 `wake` event가 깨워요(keystroke). `chain:<task id>`는 다른 task의 `WAKE` 명령이 깨워요(게임 chain). `children:<id>`는 자식이 다 끝나면 깨워요(`make`). archetype에 `disk` 같은 이름의 `WAIT`가 있는데 그건 깨워줄 task가 없는 "그냥 blocked 시간"이라 compile 때 `SLEEP`으로 바뀌어요.

---

## 4. archetype 12개 — 각각 어떤 프로그램인가

`dataset/archetypes.yaml`의 12개. 각 entry는 `pattern.program`(primitive로 쓴 program), `params`(각 숫자가 분포 + 출처), `lifetime`, `binding_params`(timeline이 채워야 하는 손잡이), `modeling_notes`(출처 위에 우리가 무엇을 지어냈나)를 가져요.

### 4.1 periodic-interactive family (interbench에서 가져옴)

**`audio-playback`** — 음악 재생.
```
LOOP { TIMER(50000) → RUN(2500) }
```
50 ms마다 2.5 ms. CPU 5%. interbench의 "audio" 모델 그대로. compile되면 숫자가 그대로 나와요(constant 분포). 쓰는 곳: `spotify`.

**`video-playback`** — 동영상 재생, 그리고 게임의 compositor.
```
LOOP { TIMER(16667) → RUN(6667) }
```
60 Hz, frame당 6.7 ms. CPU 40%. 쓰는 곳: `mpv`, `gamescope`. 화상회의(S3)도 이걸로 근사한다고 명시.

**`desktop-interactive`** — 사람이 만지는 앱. 가장 중요한 archetype.
```
LOOP { WAIT(input) → RUN(burst) }
```
keystroke를 기다리다가 오면 burst만큼 일해요. 두 개의 분포가 있어요.
- `input_gap`: keystroke 간격. 두 성분 lognormal mixture. 유창하게 칠 때 평균 158 ms, 34% 확률로 멈춤(평균 395 ms). 전체 평균 238.66 ms. 출처는 dhakal-chi18(타이핑 연구)과 roeser-rw24(분포 family).
- `burst_fraction`: burst의 길이 = 직전 gap × uniform(0, 1). interbench의 "0–100% 가변 CPU"를 선형화한 것. 우리 modeling.

compile되면 **unroll**돼요. `LOOP`가 아니라 `WAIT, RUN, WAIT, RUN, …`가 수백 쌍 펼쳐진 형태. 각 RUN의 값이 다 달라요. 예를 들어 `c1-office`의 `writer`는 234쌍이고 RUN 중앙값 ≈ 90 ms, 총 29.8 s. 즉 focus window 56초 중 약 절반을 일해요. 이게 왜 그런지는 `burst = fraction × gap`에서 fraction 평균이 0.5라서예요.

**중요한 결과:** focus되지 않은 desktop-interactive task는 keystroke를 하나도 안 받아요. compile 결과는 `WAIT(input:<id>)` 하나뿐인 program이에요. 영원히 자요. `c1-office`의 `browser`가 그래요. recognizer에게는 `chrome`으로 보이지만 CPU는 0.

### 4.2 compute/batch family

**`cpu-batch`** — CPU를 다 쓰는 job.
```
RUN(total_work) → EXIT
```
가장 단순해요. `total_work`는 timeline이 줘요. 쓰는 곳: `python3` (training), `tracker-miner-fs-3` (P1b의 full-rescan indexer), `clamscan`, `ffmpeg`, `HandBrakeCLI`, C6의 가짜 `chrome`.

**`compiler-child`** — 컴파일러 자식 하나. `build-orchestrator`가 spawn.
```
RUN(cpu_burst) → WAIT(disk) → RUN(cpu_tail) → EXIT
```
compile되면 `RUN, SLEEP, RUN, EXIT`. lognormal이라 편차가 커요: `c1-compile`의 100개 자식은 총 3.84 s, 중앙값 18.5 ms, 최대 478 ms. 출처는 meas-ci의 실제 kernel build 측정.

**`build-orchestrator`** — `make`.
```
LOOP { RUN(dispatch_overhead) → FORK }  → WAIT(children) → EXIT
```
spawn table을 순서대로 소비해요. `FORK`는 살아 있는 자식이 `parallelism_cap`(기본 8, `make -j8`)이면 block. 자식이 언제 태어나는지는 scheduler에 달려요. 마지막에 자식이 다 끝나길 기다렸다가 exit. `binding_params`: `spawn_count`, `parallelism_cap`, `child_name`.

### 4.3 IO family

**`io-stream`** — 순차 읽기/쓰기.
```
LOOP { RUN(block_cpu) → WAIT(io) }  → EXIT   (total_work가 찰 때까지)
```
compile되면 `RUN ~3 ms, SLEEP ~10 ms`가 수천 쌍. CPU:wall 비율 약 0.23. 쓰는 곳: `borg` (backup), `7z`.

**`background-crawler`** — 낮은 우선순위 indexer.
```
LOOP { RUN(scan_burst) → WAIT(io) → SLEEP(throttle) }
```
1.6 ms 일하고 5.9 ms 기다리고 3.8 s 쉼. 현재 coreset에서는 **안 쓰여요.** P1b의 `tracker-miner-fs-3`는 일부러 `cpu-batch`에 binding했어요(full-rescan 상태를 model해서 P1a와 행동이 같도록).

### 4.4 structural-special family (LAVD 논문에서)

**`game-task-chain`** — 게임. 유일하게 topology가 parameter인 archetype.
```
constructor: chain
member:  LOOP { WAIT(upstream) → RUN(per_schedule_run) → WAKE(downstream) }
```
compile 때 constructor가 **task 300개**로 펼쳐요.
- **chain 16개** (`game.chain.1` … `game.chain.16`): frame pipeline. 1번만 `TIMER(16667)`을 갖고, RUN 후 2번을 `WAKE`. 2번은 `WAIT(chain:game.chain.2)` → RUN → `WAKE` 3번. … 16번은 RUN만. frame 하나가 16단을 릴레이로 지나가요. 각 stage의 RUN은 task마다 고정(260 µs–1.65 ms 범위의 lognormal).
- **tail 284개** (`game.tail.1` … `game.tail.284`): 거의 노는 task. `LOOP { SLEEP(~0.5 s) → RUN(~200 µs) }`. LAVD가 말하는 "300개 중 대부분은 기다리는 중"을 encoding.

이름은 전부 `game.exe`. recognizer는 `game.exe ×300`을 봐요.

`binding_params`: `lane_share`. 5장의 lane scaling에서.

### 4.5 meas family (문헌 taxonomy 없음, 우리 측정)

**`network-bulk`** — 다운로드.
```
LOOP { WAIT(net) → RUN(chunk_cpu) }  → EXIT
```
compile되면 `SLEEP ~5.7 ms, RUN ~1 ms`가 수만 쌍. CPU:wall 약 0.06. `c2-p2a`의 steam download(25 s 일, 22,072 chunk), `c3-workday`의 mail send.

**`electron-comms`** — Electron 앱과 chrome renderer. 대부분 자고 가끔 깸.
```
LOOP { TIMER(heartbeat) → RUN(heartbeat_work) }
```
heartbeat는 task마다 lognormal(중앙값 1.85 s, sigma 1.09라 편차 큼). 예: `c1-office`의 renderer 8개는 period 0.7 s–2.5 s, RUN 88–749 µs. 쓰는 곳: chrome renderers, `thunderbird`, `steam`, `steamwebhelper`, `discord`.

**`system-daemon`** — 시스템 daemon.
```
LOOP { SLEEP(idle_gap) → RUN(wake_burst) }
```
SLEEP 중앙값 11 s(sigma 1.9라 매우 넓음), RUN ~155 µs. `SLEEP`을 쓰는 이유는 daemon이 주기적이지 않아서. 쓰는 곳: `c1-idle`의 다섯, `wineserver`. 편차가 커서 어떤 instance는 SLEEP이 1000초 넘게 나와 파일 안에서 한 번도 안 깨요(`c1-gaming`의 `wineserver`: SLEEP 1225 s).

### 4.6 정리표

| archetype | program 모양 | lifetime | compile 결과 | 쓰이는 이름 |
|---|---|---|---|---|
| `audio-playback` | TIMER 50 ms / RUN 2.5 ms | segment-bound | LOOP | spotify |
| `video-playback` | TIMER 16.7 ms / RUN 6.7 ms | segment-bound | LOOP | mpv, gamescope |
| `desktop-interactive` | WAIT input / RUN burst | segment-bound | WAIT/RUN 수백 쌍 unroll, 또는 WAIT 하나 | soffice.bin, chrome, code, kdenlive, gimp, thunderbird |
| `cpu-batch` | RUN total / EXIT | finite | 2줄 | python3, tracker-miner-fs-3, clamscan, ffmpeg, HandBrakeCLI, chrome(spoof) |
| `compiler-child` | RUN / WAIT / RUN / EXIT | spawned | spawn table entry | cc1 |
| `build-orchestrator` | (RUN / FORK)×N / WAIT / EXIT | finite | + spawn_table, fork_cap | make |
| `io-stream` | (RUN / WAIT)… / EXIT | finite | RUN/SLEEP 수천 쌍 | borg, 7z |
| `background-crawler` | RUN / WAIT / SLEEP | segment-bound | (coreset 미사용) | — |
| `game-task-chain` | chain constructor | segment-bound | 300 task | game.exe |
| `network-bulk` | (WAIT / RUN)… / EXIT | finite | SLEEP/RUN 수만 쌍 | steam(download), thunderbird(send) |
| `electron-comms` | TIMER hb / RUN | segment-bound | LOOP | chrome renderers, thunderbird, steam, steamwebhelper, discord |
| `system-daemon` | SLEEP / RUN | segment-bound | LOOP | gnome-shell, Xorg, pipewire, systemd, dbus-daemon, wineserver |

**lifetime 세 종류:**
- **segment-bound**: 사용자가 닫음. `depart` 시각이 파일에 박혀 있음. `LOOP unbounded`가 허용되는 유일한 종류.
- **finite**: program이 `EXIT`에 도달하면 끝. 언제인지는 scheduler에 달림. `depart` 없음.
- **spawned**: `FORK`로 태어나 `EXIT`으로 끝남.

---

## 5. compile — timeline이 workload가 되기까지

`make dataset`이 하는 일. compiler는 `dataset/tools/wlc/`.

### 5.1 seed와 sampling

timeline의 `meta.seed`(예: `c2-p1a`는 201)가 모든 draw를 결정해요. 같은 timeline + 같은 `archetypes.yaml` + 같은 seed → byte-identical 출력. 그래서 `build/`는 commit하지 않고, CI가 다시 compile해서 hash를 `build.manifest.json`과 비교해요.

sampling 단위 세 가지:
- **per-task**: task당 한 번 draw, 모든 iteration에 재사용. LOOP unbounded의 body 값들(heartbeat period, chain stage의 RUN).
- **per-iteration**: iteration마다 다른 값. bounded일 때만 가능 → unroll. keystroke gap, io-stream의 block.
- **per-instance**: spawn table의 entry마다.

### 5.2 desktop-interactive의 unroll (keystroke 생성)

```
for each focus window of this task:
    t = window.from
    loop:
        gap = draw(input_gap)          # ~238 ms 평균의 mixture
        t += gap
        if t >= window.to: break
        burst = round(draw(burst_fraction) × gap)   # gap의 0–100%
        emit wake event at t on channel input:<id>
        append WAIT(input:<id>), RUN(burst) to program
```

`c1-office`의 `writer`: focus 2–58 s → 234개 wake, 234쌍 WAIT/RUN. 첫 wake는 2.216 s. focus가 없는 task는 program이 `WAIT` 하나.

### 5.3 finite job의 unroll

`cpu-batch`는 `RUN(total_work), EXIT` 두 줄. `io-stream`과 `network-bulk`는 total_work가 찰 때까지 body를 반복해 펼쳐요. `borg`의 75 s → 21,078쌍.

### 5.4 spawn table

`build-orchestrator`는 자식 `spawn_count`개의 program을 미리 다 만들어 `spawn_table`에 넣어요. 자식 id는 `build.c1`, `build.c2`, …. `fork_cap`도 event에 실려요. 어떤 자식이 무슨 일을 하는지는 compile 시점, 언제 태어나는지는 run 시점.

### 5.5 chain constructor와 lane scaling

`game-task-chain`은 constructor가 300개 task를 만들어요. 그리고 **`-single` mode에서만** chain 16개의 RUN 값을 scale해요.

```
factor = lane_share × 16667 / Σ(16개 stage의 RUN)
각 stage RUN ← RUN × factor
```

즉 한 frame(16.667 ms) 동안 chain 16개가 합쳐서 정확히 `lane_share` × 16.667 ms를 일하도록. `lane_share: 0.9`면 chain이 lane의 90%를 요구해요. 이게 lane scaling의 전부예요. 다른 archetype은 scale 안 해요(RUN duration은 intrinsic한 CPU demand라서). 그래서 `-native`와 `-single`은 게임이 없는 파일에서는 byte-identical이에요.

왜 scale하나: LAVD의 숫자는 multi-core machine에서 잰 것이라 single lane에 그대로 넣으면 의미가 달라져요. LAVD 스스로 "상위 15–20개 task가 scheduling의 60–70%를 차지한다"고 하니, frame-critical chain의 aggregate demand를 lane 기준으로 잡고 tail은 거의 놀게 두는 게 방어 가능한 근사예요.

### 5.6 두 compile mode

| mode | 무엇 | 용도 |
|---|---|---|
| `coreset-single` | lane-scaled | **모든 실험은 이것으로** |
| `coreset-native` | 측정된 그대로 | 공개용 참고. 실행 안 함 |

---

## 6. canonical workload file의 해부

simulator와 harness가 읽는 유일한 형식. `dataset/build/coreset-single/<id>.workload.json`. top-level key 셋. 모든 시각은 정수 µs.

### 6.1 `meta`

```jsonc
"meta": {
  "id": "c1-office",
  "derived_from": "dataset/timelines/coreset/c1-office.timeline.yaml@0e120586…",
  "sampled": { "archetypes": "archetypes.yaml@99495a37…", "seed": 101 }
}
```

어느 timeline의 어느 commit에서, 어느 archetype library의 어느 commit에서, 어느 seed로. 모든 숫자의 출처가 여기서 추적돼요.

### 6.2 `ground_truth`

```jsonc
"ground_truth": [
  { "t_start": 0,        "t_end": 60000000,  "mode": "dev",      "attributes": { "background_wanted": true } },
  { "t_start": 60000000, "t_end": 180000000, "mode": "ml-train", "attributes": { "background_wanted": true } }
]
```

label이 붙은 segment 목록. `mode`는 16개 중 하나(또는 `ambiguous`), `attributes.background_wanted`는 boolean. 그 외 `background`, `initiated`, `dual_active`, `spoof`, `pre_committed_miss`(`attributes` 안)와 `familiarity`(segment 자체의 key, 적혀 있을 때만) 같은 것은 채점 split과 실패 분석용 annotation이고 recognizer의 답에는 없어요.

**마지막 segment의 `t_end`가 harness의 `T_end`예요.**

### 6.3 `events`

op는 딱 둘. `arrive`와 `wake`.

```jsonc
// segment-bound task: depart 있음
{ "op": "arrive", "t": 0, "id": "editor", "name": "code", "depart": 180000000,
  "program": [ { "op": "WAIT", "channel": "input:editor" }, { "op": "RUN", "us": 23439 },
               { "op": "WAIT", "channel": "input:editor" }, { "op": "RUN", "us": 253642 }, /* … 774쌍 */ ] }

// finite task: depart 없음
{ "op": "arrive", "t": 60000000, "id": "hog", "name": "python3",
  "program": [ { "op": "RUN", "us": 130000000 }, { "op": "EXIT" } ] }

// orchestrator: spawn_table과 fork_cap
{ "op": "arrive", "t": 2000000, "id": "build", "name": "make", "fork_cap": 8,
  "program": [ { "op": "RUN", "us": 105 }, { "op": "FORK" }, { "op": "RUN", "us": 653 }, { "op": "FORK" }, /* … 100회 */
               { "op": "WAIT", "channel": "children:build" }, { "op": "EXIT" } ],
  "spawn_table": [ { "id": "build.c1", "name": "cc1",
                     "program": [ { "op": "RUN", "us": 664 }, { "op": "SLEEP", "us": 3126 }, { "op": "RUN", "us": 9 }, { "op": "EXIT" } ] },
                   /* … 100개 */ ] }

// periodic: LOOP unbounded
{ "op": "arrive", "t": 0, "id": "video", "name": "mpv", "depart": 60000000,
  "program": [ { "op": "LOOP", "count": "unbounded",
                 "body": [ { "op": "TIMER", "period_us": 16667 }, { "op": "RUN", "us": 6667 } ] } ] }

// 외부 자극
{ "op": "wake", "t": 2098333, "channel": "input:editor", "target": "editor" }
```

`arrive`의 `id`는 harness의 records에서 `entity`가 돼요. `name`은 recognizer가 보는 것. 같은 이름의 task가 여럿이면 id로 구분해요(`renderers.1` … `renderers.8`은 전부 `name: chrome`).

---

## 7. recognizer가 보는 것 — telemetry snapshot과 query point

daemon은 run file에서 **pinned event**(등장, 그리고 `depart`가 있는 퇴장)만 시간순으로 걸으면서 "살아 있는 이름의 multiset"을 유지해요. 그 집합이 바뀔 때마다 snapshot 하나 = **query point** 하나. recognizer는 그때만 호출돼요. 중간에는 아무것도 안 물어요.

규칙 몇 가지:
- 개수 변화도 변화예요. `chrome ×13`이 `×14`가 되면 snapshot이 나와요(`c6-spoof`가 이걸 이용).
- 같은 시각의 event는 전부 적용한 뒤 snapshot 하나.
- finite task는 `depart`가 없으니 **끝나도 telemetry에서 안 사라져요.** recognizer는 batch job이 끝난 걸 몰라요.
- spawn 자식(`cc1 ×100`)은 부모 `make`가 나타날 때 같이 보여요. 언제 태어나는지는 emergent라 알 수 없으니 부모의 lifetime에 붙여요.
- 마지막 순간(모든 segment-bound task가 떠남)의 snapshot도 나와요. 하지만 그 뒤에는 채점할 segment가 없으니 채점에서 빠져요.

`c2-p1a`의 query point 셋:

| t | 보이는 것 | 채점 |
|---|---|---|
| 0 s | `code ×1` | `dev`, wanted |
| 60 s | `code ×1, python3 ×1` | `ml-train`, wanted |
| 180 s | `python3 ×1` | (terminal, 채점 안 함) |

recognizer는 두 번 답해요. 그 답이 config schedule의 두 entry(+ boot entry)가 되고, recognition log의 두 query가 돼요. 10장의 파일별 표에 각 파일의 query point를 다 적어뒀어요.

---

## 8. demand와 utilization — 의자를 얼마나 요구하나

compiler는 파일마다 static demand estimate를 내요.

```
utilization = Σ(모든 task의 RUN 총합) / T_end
```

editor는 focus window 안의 burst 합, batch는 total_work, periodic은 (RUN/period) × 살아 있는 시간, spawn 자식은 전부 합산. 1.0이면 파일 전체 시간 동안 lane을 100% 요구한다는 뜻. 1.2면 120%: 어떻게 해도 누군가는 기다려요. **이 oversubscription이 실험의 재료예요.** 의자가 남으면 scheduler가 뭘 하든 차이가 안 나니까.

**demand window 규칙:** `-single` 파일 중 demand class가 `oversubscribed`인 것은 utilization이 1.00–1.50 안에 있어야 해요. lint가 검사. `calibration` class는 면제. class는 timeline의 `meta.demand`로 선언하고, 파일의 실제 demand가 낮다는 뜻이 아니라 "검사 면제"라는 뜻이에요(`c1-gaming`은 calibration인데 1.46).

원래 24개 (`coreset-single`, 2026-09-08 빌드; Phase 7의 26개는 §10의 C1 추가분과 C7 표에):

| 파일 | utilization | class | native | 비고 |
|---|---|---|---|---|
| c1-browsing | 0.45 | calibration | 0.45 | |
| c1-compile | 0.54 | calibration | 0.54 | |
| c1-gaming | **1.46** | calibration | 1.23 | coreset 최고. lane_share 0.9 + compositor 0.4 |
| c1-idle | 0.0004 | calibration | 0.0004 | 사실상 0 |
| c1-media | 0.45 | calibration | 0.45 | 0.40 + 0.05 |
| c1-office | 0.50 | calibration | 0.50 | writer 혼자 |
| c2-p1a / p1b | 1.20 | oversubscribed | 1.20 | editor 0.48 + hog 0.72 |
| c2-p2a / p2b | 1.29 | oversubscribed | 1.09 | lane_share 0.95 |
| c2-p3a / p3b | 1.12 | oversubscribed | 1.12 | |
| c3-creation | 1.04 | oversubscribed | 1.04 | |
| c3-evening | 1.11 | oversubscribed | 0.65 | lane_share 1.45 (segment 안에서만) |
| c3-workday | 1.04 | oversubscribed | 1.04 | 자식 4200개 |
| c4-compile | 0.54 | calibration | 0.54 | c1-compile + 거의 0 |
| c4-gaming | 1.46 | calibration | 1.23 | |
| c4-office | 0.60 | calibration | 0.60 | + 7z 6 s |
| c5-t3 / t4 / t5 | 0.45 | calibration | 0.45 | = c1-media |
| c6-dual | 1.28 | oversubscribed | 1.55 | lane_share 0.6 |
| c6-fold | 0.45 | calibration | 0.45 | = c1-browsing |
| c6-spoof | 0.95 | calibration | 0.95 | window 바로 아래 |

주의: utilization은 파일 전체의 평균이에요. `c2-p1a`는 0–60초는 0.48이고 60–180초는 1.56이에요. 흥미로운 구간은 뒤쪽.

---

## 9. 일곱 그룹 C1–C7 — 각 그룹이 답하는 질문

50개 파일은 일곱 그룹이고, 각 그룹은 하나의 측정을 가능하게 하려고 존재해요. "이 파일이 없으면 깨지는 RQ가 없다"면 그 파일은 없어야 해요.

| 그룹 | 파일 수 | 질문 | 구성 방식 |
|---|---|---|---|
| **C1** calibration | 16 | 한 가지 명백한 상황을 맞히나. 바닥. **whitelist가 만점을 받아야 하는 곳** | mode당 하나(16 mode 전부, Phase 7부터), segment 하나 — 그 mode의 `true` cell |
| **C2** intent pairs | 6 (3쌍) | **행동이 완전히 같고 의도만 다를 때** 구분되나. RQ0 judging set | base + 한 segment만 다른 변형 |
| **C3** transition arcs | 3 | 상황이 중간에 바뀔 때 얼마나 빨리 정확히 따라가나 | 3–4 segment |
| **C4** distractor | 3 | 무관한 process가 중간에 나타나면 답이 흔들리나 | C1 clone + 주입 1개. 원본과 paired |
| **C5** familiarity | 3 | 이름이 낯설어져도 알아보나 | c1-media + 이름만 교체 |
| **C6** resolution limits | 3 | 이름 기반 recognition이 **설계상** 못 하는 곳. 미리 약속된 miss | 각각 다름 |
| **C7** attribute counterparts | 16 | 배경 작업이 **원하지 않은 것**일 때 답이 뒤집히나. driver table의 32 cell 전부에 pair를 줌 | mode당 하나, C1 base + op 하나(scan 주입 또는 rename) + label flip — 그 mode의 `false` cell |

파생 관계: C4 = C1 + injection, C5 = C1 + rename, C7 = C1 + unwanted job 또는 rename + label flip, C2의 b = a + 한 segment 수정, C6 둘은 c1-browsing 파생. 진짜 새로 쓴 timeline은 23개(C1 16, C2의 a 3, C3 3, c6-dual)이고 나머지 27개는 `*.variant.yaml` recipe 다섯 개로 생성돼요. 파생 파일은 base의 seed를 물려받아서 "변경한 것 외에는 byte-identical"이 보장돼요.

---

## 10. 50개 파일 상세

각 파일에 대해: 한 문단 이야기, segment, task(compile된 실제 수치), recognizer가 보는 snapshot, harness가 볼 것. RUN 수치는 `coreset-single`에서 읽은 값. "RUN/iter"는 LOOP body 한 바퀴의 RUN, "RUN 총"은 파일 전체의 합.

시간 표기: 초. 프로그램 안 숫자: µs 또는 ms.

---

### C1 — single-situation calibration

#### `c1-office` — 문서 작업

사람이 LibreOffice Writer에 타이핑하고 있고, chrome이 탭 몇 개 열린 채 뒤에 있고, Thunderbird가 켜져 있어요. 60초.

| segment | mode | attributes |
|---|---|---|
| 0–60 s | office | background_wanted: true |

| id | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| writer | soffice.bin | desktop-interactive | 0 → 60 | focus 2–58 s. wake 234개. RUN 234개, 중앙값 89.7 ms, 총 29.8 s |
| browser | chrome | desktop-interactive | 0 → 60 | focus 없음 → `WAIT` 하나. **한 번도 안 깸** |
| renderers.1–8 | chrome | electron-comms | 0 → 60 | TIMER 0.7–2.5 s, RUN 88–749 µs |
| mail | thunderbird | electron-comms | 0 → 60 | TIMER 2.02 s, RUN 71 µs |

recognizer: 0 s `chrome ×9, soffice.bin ×1, thunderbird ×1` → 정답 office/wanted. 60 s 빈 집합(terminal).

harness: writer의 `ready_wait(cause=wake)` 234개. contention 상대는 renderer/mail의 작은 heartbeat뿐이라 대부분 0에 가까울 거예요. utilization 0.50. **Phase 5의 mock 1번**이 이 파일의 축소판이에요(focus된 editor, burst 중간에 queued된 keystroke 하나, 한 번도 안 깨는 unfocused task).

#### `c1-browsing` — 웹 브라우징

chrome 하나에 탭 12개. 60초. C6의 두 파일이 여기서 파생돼요.

| segment | mode | attributes |
|---|---|---|
| 0–60 s | browsing | background_wanted: true |

| id | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| browser | chrome | desktop-interactive | 0 → 60 | focus 2–58 s. wake 229개. RUN 중앙값 90.4 ms, 총 26.6 s |
| renderers.1–12 | chrome | electron-comms | 0 → 60 | TIMER 1.1–4.1 s, RUN 86 µs–2.4 ms |

recognizer: 0 s `chrome ×13`. 60 s 빈 집합.

harness: browser의 `ready_wait(wake)` 229개. utilization 0.45.

#### `c1-compile` — 코드 편집 + 빌드

VS Code에 타이핑하면서 2초에 `make -j8`을 돌려요. 자식 100개.

| segment | mode | attributes |
|---|---|---|
| 0–60 s | compile | background_wanted: true |

| id | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| editor | code | desktop-interactive | 0 → 60 | focus 2–58 s. wake 239개. RUN 중앙값 79.9 ms, 총 28.5 s |
| build | make | build-orchestrator | 2 → finite | fork_cap 8. dispatch RUN 100개 (중앙값 272 µs). spawn_table 100 |
| build.c1–c100 | cc1 | compiler-child | spawn | 각 `RUN, SLEEP, RUN, EXIT`. 총 3.84 s, 중앙값 18.5 ms, 최대 478 ms, SLEEP 중앙값 3.6 ms |

recognizer: 0 s `code ×1`. 2 s `code ×1, make ×1, cc1 ×100`(자식은 부모와 함께 보임). 60 s `make ×1, cc1 ×100`(finite라 안 사라짐).

harness: **양면** 파일. editor의 `ready_wait(wake)`와 `make`의 `turnaround`(= makespan). 자식 100개 각각의 `turnaround`도 나오고, 자식의 `task_arrive`는 trace의 emergent 시각. 총 일이 3.84 s라 60초 안에 여유 있게 끝나요. editor latency와 makespan이 서로 당기는 trade-off가 scoring 판단 대상.

#### `c1-gaming` — 게임

Proton 게임. `game.exe` 300개 task, Steam과 helper 셋, wineserver, compositor(gamescope). focus 없음(게임은 keystroke 모델이 아니라 frame 모델).

| segment | mode | attributes |
|---|---|---|
| 0–60 s | gaming | background_wanted: true |

| id | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| game.chain.1–16 | game.exe | game-task-chain | 0 → 60 | head TIMER 16667. stage RUN 293 µs–1.47 ms (scaled, 합 = 0.9 × 16667 = 15.0 ms) |
| game.tail.1–284 | game.exe | game-task-chain | 0 → 60 | SLEEP ~0.3–1.2 s, RUN 49 µs–1 ms |
| compositor | gamescope | video-playback | 0 → 60 | TIMER 16667, RUN 6667 |
| steam | steam | electron-comms | 0 → 60 | TIMER 3.28 s, RUN 381 µs |
| webhelper.1–3 | steamwebhelper | electron-comms | 0 → 60 | TIMER 0.78 s / 0.83 s / 26.9 s |
| wine | wineserver | system-daemon | 0 → 60 | SLEEP 1225 s → 파일 안에서 **한 번도 안 깸** |

recognizer: 0 s `game.exe ×300, gamescope ×1, steam ×1, steamwebhelper ×3, wineserver ×1`. 60 s 빈 집합.

harness: chain의 `job`(frame latency, miss rate)과 compositor의 `job`. **utilization 1.46, coreset 최고.** chain 0.9 + compositor 0.4 = 1.3만으로 이미 lane을 넘어요. 두 개의 60 Hz 소비자가 한 lane을 두고 싸우는 파일이에요. judging set에는 안 들어가지만(pair가 없어 attribute 변화가 없음) demand가 가장 높아 "gap이 family 때문인지 demand 때문인지"를 분리해 보는 별도 보고 line.

#### `c1-media` — 미디어 재생

mpv로 동영상, spotify로 음악. C5 셋이 여기서 파생.

| segment | mode | attributes |
|---|---|---|
| 0–60 s | media | background_wanted: true |

| id | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| video | mpv | video-playback | 0 → 60 | TIMER 16667, RUN 6667 (40%) |
| music | spotify | audio-playback | 0 → 60 | TIMER 50000, RUN 2500 (5%) |

recognizer: 0 s `mpv ×1, spotify ×1`. 60 s 빈 집합.

harness: 두 task의 `job`. utilization 0.45라 contention이 거의 없어요(두 tick이 겹칠 때 하나가 최대 6.7 ms 기다림). **Phase 5의 mock 2번**이 이 파일의 축소판(TIMER task 둘, 하나는 backlog). scoring에서 audio와 video의 weight를 다르게 줄지가 판단 대상(오디오 끊김이 더 잘 들림).

#### `c1-idle` — 아무도 없음

시스템 daemon 다섯만. 사람 없음.

| segment | mode | attributes |
|---|---|---|
| 0–60 s | idle | background_wanted: true |

| id | name | archetype | compile 결과 |
|---|---|---|---|
| shell | gnome-shell | system-daemon | SLEEP 2.8 s, RUN 99 µs |
| xorg | Xorg | system-daemon | SLEEP 5.0 s, RUN 65 µs |
| audio-srv | pipewire | system-daemon | SLEEP 1.46 s, RUN 237 µs |
| init | systemd | system-daemon | SLEEP 0.46 s, RUN 63 µs |
| bus | dbus-daemon | system-daemon | SLEEP 3.49 s, RUN 314 µs |

recognizer: 0 s 다섯 이름. 60 s 빈 집합.

harness: **성능 metric 없음.** utilization 0.0004. 이 파일의 역할은 "recognizer가 idle이라고 하나"뿐이에요.

---

#### Phase 7에서 추가된 열 개의 C1 (2026-09-10)

원래 C1은 여섯이었고 나머지 열 mode는 다른 파일의 segment 안에만 있었어요. Phase 7이 mode당 하나씩 채웠어요 — 모양은 위와 같아요(60 s, segment 하나, `background_wanted: true`, `demand: calibration`, focus 2–58 s). task set은 그 mode를 이미 담고 있던 segment에서 그대로 가져왔고(파일 header에 출처가 적혀 있어요), batch job은 60 s 안에 끝나도록 30 s로 줄였어요(turnaround term을 갖기 위해). `c1-meeting`만 새로 설계했어요 — `c6-fold`의 meeting segment는 browser 그대로라 가져올 task set이 없었고, S3는 archetype-plan OQ-2대로 video-playback에 묶어요.

| 파일 | task set | 출처 segment | utilization |
|---|---|---|---|
| `c1-dev` | code 편집기 혼자 | c2-p1a seg 0 | 0.46 |
| `c1-video-edit` | kdenlive 혼자 | c2-p3a seg 0 | 0.46 |
| `c1-photo` | gimp 혼자 | c3-creation seg 0 | 0.47 |
| `c1-mail` | thunderbird + 40초의 send burst(network-bulk) | c3-workday seg 3 | 0.53 |
| `c1-meeting` | zoom: video-playback + audio-playback + electron-comms helper (신규 설계, OQ-2) | — | 0.45 |
| `c1-ml-train` | code + python3 cpu-batch 30 s | c2-p1a seg 1 | 0.97 |
| `c1-render` | kdenlive + ffmpeg cpu-batch 30 s, initiated: user | c2-p3a seg 1 | 0.90 |
| `c1-transcode` | kdenlive + HandBrakeCLI cpu-batch 30 s, initiated: user | c3-creation seg 2 | 0.97 |
| `c1-indexing` | code + tracker-miner-fs-3 cpu-batch 30 s, initiated: user, **pre_committed_miss** | c2-p1b seg 1 | 0.95 |
| `c1-backup` | kdenlive + borg io-stream 30 s, initiated: scheduled (wanted: true, p3b와 같음) | c2-p3b seg 1 | 0.97 |

`c1-indexing`은 indexing의 **`true`** cell이에요 — 사용자가 직접 돌린 reindex. 같은 indexer가 같은 일을 하니 이름·행동으로는 `c2-p1b`의 unwanted rescan과 구분이 안 돼요. 그래서 `pre_committed_miss: true`가 붙어요(§12).

---

### C2 — intent pairs (RQ0 judging set)

각 pair의 a와 b는 **한 segment만 달라요.** 나머지는 byte-identical. 그래서 결과 차이는 그 하나의 변경에 귀속돼요.

#### `c2-p1a` — 개발 + 내가 돌린 training run (★ load-bearing pair의 base)

VS Code에 타이핑하다가 60초에 `python3` training을 시작해요. 사용자가 원한 일.

| segment | mode | attributes |
|---|---|---|
| 0–60 s | dev | background_wanted: true |
| 60–180 s | ml-train | background_wanted: true |

| id | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| editor | code | desktop-interactive | 0 → 180 | focus 2–178 s. wake 774개. RUN 중앙값 80.4 ms, 총 86.7 s |
| hog | python3 | cpu-batch | 60 → finite | `RUN 130 s, EXIT` |

recognizer: 0 s `code ×1`. 60 s `code ×1, python3 ×1`. 180 s `python3 ×1`.

harness: editor의 `ready_wait(wake)` 774개(60초 이후가 관심 구간), hog의 `cpu_delivered` / `demand`(progress). **hog는 절대 못 끝나요**: 130 s 일을 60초에 시작, 120초 남음, 그마저도 editor가 절반을 씀. 그래서 `turnaround`는 없고 progress만. utilization 1.20 (60초 이후는 1.56). **Phase 5의 mock 3번**이 이 파일의 축소판(config switch at 60 s + latency, batch unfinished at T_end).

#### `c2-p1b` — 개발 + 아무도 안 부른 indexer

`c2-p1a`에서 **이름만** `python3` → `tracker-miner-fs-3`로 바꾸고 segment 2의 label을 `indexing`, `background_wanted: false`로. archetype은 그대로 `cpu-batch`(full-rescan indexer를 model, 일부러 P1a와 행동을 동일하게).

| segment | mode | attributes |
|---|---|---|
| 0–60 s | dev | background_wanted: true |
| 60–180 s | indexing | **background_wanted: false** |

task는 `c2-p1a`와 동일(hog의 name만 다름). recognizer: 60 s `code ×1, tracker-miner-fs-3 ×1`.

harness: **trace와 records가 p1a와 같아요**(같은 condition이면). 차이는 scoring의 weight뿐. p1a는 hog의 progress에 양의 weight, p1b는 0. 이 pair가 "attribute recognition이 scheduling에 영향을 주나"를 가장 깨끗하게 물어요. LLM은 `python3`와 `tracker-miner-fs-3`의 의미를 알아야만 구분할 수 있고, whitelist는 두 이름을 다 등록해야 해요.

#### `c2-p2a` — 게임 + 내가 켜둔 다운로드

게임 중 60초에 Steam 다운로드 worker가 붙어요. Valve의 "게임 중 다운로드 허용" 설정이 이 상황의 근거.

| segment | mode | attributes |
|---|---|---|
| 0–60 s | gaming | background_wanted: true |
| 60–120 s | gaming | background_wanted: true, background: download |

| id | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| game.chain.1–16 | game.exe | game-task-chain | 0 → 120 | scaled: 합 = 0.95 × 16667. stage RUN 230 µs–2.18 ms |
| game.tail.1–284 | game.exe | game-task-chain | 0 → 120 | 거의 idle |
| steam | steam | electron-comms | 0 → 120 | TIMER 2.38 s |
| wine | wineserver | system-daemon | 0 → 120 | SLEEP 2.1 s, RUN 212 µs |
| download | **steam** | network-bulk | 60 → finite | SLEEP ~5.7 ms / RUN ~1 ms × 22,072. RUN 총 25.0 s |

recognizer: 0 s `game.exe ×300, steam ×1, wineserver ×1`. 60 s `… steam ×2 …`(개수 변화가 query point). 120 s `steam ×1`.

harness: chain의 `job` + download의 progress. download는 25 s의 CPU를 60초 안에 받아야 하는데 chain이 lane의 95%를 요구하니 **못 끝나요**(lane의 42%가 필요). utilization 1.29. compositor(`gamescope`)는 이 파일에 없어요. TIMER를 가진 task는 `game.chain.1`과 `steam`뿐.

#### `c2-p2b` — 게임 + 아무도 안 부른 바이러스 검사

`c2-p2a`에서 download task를 `clamscan`(cpu-batch, 25 s)으로 교체, segment 2를 `background_wanted: false, background: av-scan`.

| segment | mode | attributes |
|---|---|---|
| 0–60 s | gaming | background_wanted: true |
| 60–120 s | gaming | **background_wanted: false**, background: av-scan |

| 바뀐 task | name | archetype | compile 결과 |
|---|---|---|---|
| download | clamscan | cpu-batch | `RUN 25 s, EXIT` |

recognizer: 60 s `clamscan ×1, game.exe ×300, steam ×1, wineserver ×1`.

harness: 주의. p1과 달리 **이 pair는 행동이 완전히 같지는 않아요.** download는 network-bulk(CPU 6%짜리 chunk 수만 개), clamscan은 cpu-batch(연속 25 s). 같은 것은 "게임 + 배경 일 25 s"의 모양이고, 다른 것은 wanted 여부. 그래서 scoring은 p2a에서 download의 progress를 세고 p2b에서 clamscan의 progress를 0으로 둬요.

#### `c2-p3a` — 영상 편집 + 내가 시작한 렌더

kdenlive에서 편집하다가 60초에 ffmpeg 렌더를 걸어요.

| segment | mode | attributes |
|---|---|---|
| 0–60 s | video-edit | background_wanted: true |
| 60–120 s | render | background_wanted: true, initiated: user |

| id | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| editor | kdenlive | desktop-interactive | 0 → 120 | focus 2–118 s. wake 480개. RUN 중앙값 89.4 ms, 총 59.6 s |
| bulk | ffmpeg | cpu-batch | 60 → finite | `RUN 75 s, EXIT` |

recognizer: 0 s `kdenlive ×1`. 60 s `ffmpeg ×1, kdenlive ×1`. 120 s `ffmpeg ×1`.

harness: editor latency + bulk progress. 75 s를 60초 안에 → 못 끝남. utilization 1.12.

#### `c2-p3b` — 영상 편집 + 예약된 백업

bulk를 `borg`(io-stream, 75 s)로, segment 2를 `backup`, `initiated: scheduled`. **여기서는 `background_wanted`가 둘 다 true예요.** 이 pair가 구분하는 건 wanted/unwanted가 아니라 mode(`render` vs `backup`)와 "누가 시작했나"예요.

| segment | mode | attributes |
|---|---|---|
| 0–60 s | video-edit | background_wanted: true |
| 60–120 s | backup | background_wanted: true, initiated: scheduled |

| 바뀐 task | name | archetype | compile 결과 |
|---|---|---|---|
| bulk | borg | io-stream | RUN ~3 ms / SLEEP ~2 ms × 21,078. RUN 총 75.0 s |

recognizer: 60 s `borg ×1, kdenlive ×1`.

harness: borg는 io-stream이라 RUN 사이에 SLEEP이 있어요. 연속 25 s가 아니라 잘게 쪼개진 3 ms 조각이라 editor를 덜 방해해요. p3a와 행동이 다르니 records도 달라요. scoring이 "backup의 progress를 얼마나 칠지"를 정해야 해요.

---

### C3 — transition arcs

상황이 여러 번 바뀌어요. query point가 여럿이고, 각 경계에서 recognizer가 얼마나 빨리 정확히 따라가는지를 봐요. 전부 oversubscribed.

#### `c3-workday` — 하루 일과

chrome 검색 → LibreOffice 글쓰기 → make 빌드 시작 → Thunderbird 메일 → 메일 전송. CpsMark+의 협업 workflow 순서.

| segment | mode | attributes |
|---|---|---|
| 0–60 s | browsing | wanted |
| 60–120 s | office | wanted |
| 120–360 s | compile | wanted |
| 360–420 s | mail | wanted |

| id | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| browser | chrome | desktop-interactive | 0 → 420 | focus 2–58 s만. wake 242개, RUN 총 27.5 s |
| renderers.1–8 | chrome | electron-comms | 0 → 420 | TIMER 0.6–10 s |
| writer | soffice.bin | desktop-interactive | 60 → 420 | focus 62–118 s. wake 244개, 총 27.8 s |
| build | make | build-orchestrator | 120 → finite | spawn 4200, cap 8. dispatch 총 1.1 s |
| build.c1–c4200 | cc1 | compiler-child | spawn | **총 349 s**, 중앙값 20 ms, 최대 5.6 s |
| mailer | thunderbird | desktop-interactive | 360 → 420 | focus 362–418 s. wake 220개, 총 27.7 s |
| send | thunderbird | network-bulk | 400 → finite | RUN 총 3.0 s |

recognizer (6 query point): 0 s `chrome ×9` → 60 s `+soffice.bin` → 120 s `+make, cc1 ×4200` → 360 s `+thunderbird` → 400 s `thunderbird ×2` → 420 s `make, cc1, thunderbird`(terminal).

harness: 주목할 점. **빌드는 window 안에 절대 못 끝나요.** 자식 349 s의 일이 120초에 시작하고 window는 300초 남았는데 그 사이 writer와 mailer가 lane의 일부를 써요. 그래서 `make`의 `turnaround`는 안 나오고 progress만. 각 segment의 foreground task(browser → writer → mailer)의 `ready_wait`가 시간에 따라 어떻게 바뀌는지, 그리고 120초 이후 4200개 자식의 fork storm이 editor를 얼마나 방해하는지가 이 파일의 이야기예요. utilization 1.04.

#### `c3-evening` — 저녁

브라우징 → 게임(Discord overlay 포함) → 미디어 재생.

| segment | mode | attributes |
|---|---|---|
| 0–60 s | browsing | wanted |
| 60–300 s | gaming | wanted |
| 300–420 s | media | wanted |

| id | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| browser | chrome | desktop-interactive | 0 → 60 | wake 229개, 총 28.7 s |
| renderers.1–10 | chrome | electron-comms | 0 → 60 | |
| game.chain.1–16 | game.exe | game-task-chain | 60 → 300 | **lane_share 1.45** → stage RUN 합 = 24.2 ms per 16.7 ms frame. 혼자서도 못 따라감 |
| game.tail.1–284 | game.exe | game-task-chain | 60 → 300 | |
| overlay | discord | electron-comms | 60 → 300 | TIMER 0.31 s, RUN 558 µs |
| steam | steam | electron-comms | 60 → 300 | |
| wine | wineserver | system-daemon | 60 → 300 | SLEEP 457 s → 안 깸 |
| video | mpv | video-playback | 300 → 420 | |
| music | spotify | audio-playback | 300 → 420 | |

recognizer (4): 0 s `chrome ×11` → 60 s `discord, game.exe ×300, steam, wineserver` → 300 s `mpv, spotify` → 420 s 빈 집합.

harness: 게임 segment의 chain은 lane_share 1.45라 **설계상 frame을 계속 놓쳐요.** backlog 규칙이 실제로 작동하는 파일. utilization은 파일 평균 1.11이지만 게임 segment 안은 1.45 이상. 세 segment의 primary metric이 다 달라요(browser latency → frame miss → media job). 참고로 `game.chain.1`은 60초에 등장하는 TIMER task라 "TIMER의 t₀가 무엇인가"(등장 시각? 전역 0?)라는 simulator의 미결 질문이 실제로 영향을 주는 파일이에요.

#### `c3-creation` — 창작

GIMP 사진 편집 → kdenlive 영상 편집 → HandBrake 변환.

| segment | mode | attributes |
|---|---|---|
| 0–120 s | photo | wanted |
| 120–240 s | video-edit | wanted |
| 240–420 s | transcode | wanted, initiated: user |

| id | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| photo-editor | gimp | desktop-interactive | 0 → 120 | focus 2–118 s. wake 488개, 총 58.2 s |
| video-editor | kdenlive | desktop-interactive | 120 → 420 | focus 122–238 s만. wake 510개, 총 56.6 s |
| batch | HandBrakeCLI | cpu-batch | 240 → finite | `RUN 320 s` |

recognizer (4): 0 s `gimp` → 120 s `kdenlive` → 240 s `HandBrakeCLI, kdenlive` → 420 s `HandBrakeCLI`.

harness: 240초 이후 kdenlive는 focus가 없어요(사용자가 변환을 걸어놓고 손을 뗌). 그래서 마지막 segment는 batch 혼자 lane을 쓰고 contention이 없어요. 320 s 일을 180초에 → 못 끝남. progress만. utilization 1.04. 중요한 구간은 오히려 photo → video-edit 전환에서 recognizer가 mode를 갈아타는 것.

---

### C4 — distractor injection

C1 파일의 clone에 무관한 process 하나를 30초에 주입. 원본과 pair로 비교해서 "답이 흔들렸나"를 봐요. seed와 demand class는 원본에서 상속.

#### `c4-gaming` — 게임 중 Discord 켜짐

`c1-gaming` + 30초에 `discord`(electron-comms). label 불변(gaming, wanted).

| 주입된 task | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| injected-overlay | discord | electron-comms | 30 → 60 | TIMER 1.71 s, RUN 590 µs |

recognizer: 0 s (c1-gaming과 동일) → **30 s `+discord ×1`** (새 query point) → 60 s 빈 집합.

harness: 성능은 c1-gaming과 거의 같아야 해요(discord는 CPU를 거의 안 씀). 관심은 30초의 query에서 recognizer가 여전히 gaming/wanted라고 하는가. utilization 1.46.

#### `c4-office` — 문서 작업 중 압축

`c1-office` + 30초에 `7z`(io-stream, 6 s 일).

| 주입된 task | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| injected-burst | 7z | io-stream | 30 → finite | RUN ~3 ms / SLEEP ~11 ms × 1651. RUN 총 6.0 s |

recognizer: 0 s (c1-office와 동일) → 30 s `+7z ×1` → 60 s `7z ×1`(finite라 남음).

harness: 이 파일은 성능 차이도 조금 있어요. 7z가 30초 동안 3 ms 조각으로 lane을 두드리니 writer의 `ready_wait`가 원본보다 살짝 나빠질 수 있어요. C1 원본과의 delta로 봐요. utilization 0.60.

#### `c4-compile` — 빌드 중 chrome 열림

`c1-compile` + 30초에 `chrome` 하나와 renderer 6개.

| 주입된 task | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| injected-browser | chrome | desktop-interactive | 30 → 60 | focus 없음 → `WAIT` 하나 |
| injected-renderers.1–6 | chrome | electron-comms | 30 → 60 | TIMER 0.8–7 s |

recognizer: 0 s `code` → 2 s `+make, cc1 ×100` → **30 s `+chrome ×7`** → 60 s `make, cc1`.

harness: 주입된 것들은 CPU를 거의 안 써요(browser는 아예 0). 성능은 원본과 같아야 하고, 관심은 30초 query에서 mode가 `compile`에서 `browsing`으로 흔들리는가. utilization 0.54.

---

### C5 — familiarity ladder

`c1-media`와 **structure, archetype, seed, 숫자가 전부 같고 이름만 달라요.** test suite가 "이름 외 byte-identical"을 강제해요. 성능 숫자는 c1-media와 같아야 하고, 다르면 bug. 이 셋은 Layer 1(recognition) 전용이에요.

tier 정의:
1. transparent (`firefox`, `blender`) — C1에 이미 있음
2. semi-opaque (`soffice.bin`, `gamescope`) — C1에 이미 있음
3. opaque: 실제 있지만 이름에서 뜻이 안 보임. corpus에서 recall해야 함
4. nonexistent-compositional: 없는 소프트웨어지만 단어 뜻으로 추론 가능
5. nonexistent-opaque: recall도 추론도 불가

| 파일 | video (mpv 자리) | music (spotify 자리) | familiarity |
|---|---|---|---|
| `c5-t3` | baloo_file | tracker-miner-fs-3 | 3 |
| `c5-t4` | video-playback-svc | audio-stream-helper | 4 |
| `c5-t5` | qzvd | xkrr | 5 |

segment: 0–60 s media, wanted, `familiarity: N` annotation.

recognizer: 0 s 두 이름. 60 s 빈 집합.

**주의 (t3):** `baloo_file`과 `tracker-miner-fs-3`는 **실제로는 indexer**인데 여기서는 동영상/음악 player처럼 행동해요. 이름이 행동을 오도하는 tier예요. whitelist는 t4, t5에서 구조적으로 0점(등록할 이름이 없음). tier 4와 5를 나눈 이유는 "corpus에서 본 적 있는가"와 "단어 조합으로 추론하는가"를 분리하려고.

**familiarity란 무엇인가.** process **이름**이 language model에게 얼마나 알아볼 만한가를 나타내는 등급이에요. 행동과는 무관하고, 오직 이름의 속성이에요. 기준은 사람이 아니라 **corpus**예요 — "model이 학습 데이터에서 이 이름을 봤을 법한가". 그래서 `soffice.bin`은 사람에게는 낯설어도 corpus에는 충분히 있으니 tier 2이고, `video-playback-svc`는 세상에 없는 이름이지만 단어 뜻으로 추론이 되니 tier 4예요.

**왜 필요한가.** research-claims 문서는 whitelist가 실패하는 이유를 둘로 나눠요. 하나는 조합(같은 process가 옆에 뭐가 있느냐에 따라 뜻이 다름, C2가 검사), 다른 하나는 **세상 지식**(등록된 적 없는 소프트웨어는 목록에 없음). 두 번째를 검사하는 게 tier 4–5예요. whitelist는 거기서 구조적으로 0점이고, model은 tier 4는 읽고 tier 5는 못 읽을 것으로 예측해요. 이 계단 모양이 예측대로 나오는 게 증거예요.

**metric 계산에서 어떻게 쓰이나.** primitive에는 전혀 안 들어가요. **aggregate할 때의 split key**예요. recognition row 하나(이 query에서 mode를 맞췄나)는 정확히 하나의 ground-truth segment에 덮이고, 그 segment의 tier를 grouping label로 물려받아요. 그래서 accuracy를 전체 평균 하나로 내지 않고 "tier 1–2 이름에서 정확도", "tier 3에서", "tier 4에서", "tier 5에서"로 condition마다 따로 내요. `condition`이나 `workload_id`처럼 **묶는 기준**이지 계산하는 숫자가 아니에요. tier를 섞어 평균 내면 위의 계단이 사라져요.

**지금 tier가 어디에 적혀 있나.** 명시적으로는 C5 세 파일의 segment에만(`familiarity: 3/4/5`). 나머지 파일은 annotation이 없고, coverage-grid tool이 내부 이름표(`_TIER_BY_NAME`)로 계산하며 모르는 이름은 tier 5로 쳐요. 2026-09-08부터 compiler가 이 annotation을 `ground_truth`의 segment key로 그대로 실어 보내요 — author가 적은 경우에만이고, 안 적었으면 key 자체가 없어요(grid tool의 추정값은 싣지 않아요). 그래서 C5 세 파일의 compiled `ground_truth`에는 `familiarity: 3/4/5`가 있고, 나머지 21개 파일에는 없어요. grader는 이 key로 accuracy를 tier별로 묶어요. 어느 segment에 annotation을 더 달지(tier 1 기준선으로 `c1-media`가 자연스러운 첫 후보)는 열린 항목이에요(12장).

---

### C6 — resolution limits (미리 약속된 miss)

이름 기반 recognition이 **설계상** 못 하는 세 경우. 결과가 나쁠 것을 알고 넣어요. 한계를 주장만 하지 않고 측정하려고.

#### `c6-spoof` — chrome이라는 이름의 광부

`c1-browsing` + 20초에 `chrome`이라는 **이름**의 cpu-batch(30 s 일). 진짜 브라우저 13개 사이에 14번째 chrome이 나타나는데 그건 CPU를 다 먹는 batch예요.

| segment | mode | attributes |
|---|---|---|
| 0–60 s | browsing | wanted, spoof: true |

| 추가된 task | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| spoof | chrome | cpu-batch | 20 → finite | `RUN 30 s, EXIT` |

recognizer: 0 s `chrome ×13` → **20 s `chrome ×14`**(개수 변화가 query point) → 60 s `chrome ×1`(spoof는 finite).

harness: 이름만으로는 14번째 chrome이 다른 걸 알 수 없어요. recognizer가 뭐라 답하든 browsing이고, 그러면 batch를 throttle할 근거가 없어서 browser의 latency가 나빠져요. utilization 0.95(window 바로 아래인데 상속된 calibration class라 lint를 통과). path 기반 검증은 schema 밖(names only 결정).

#### `c6-fold` — process는 그대로인데 상황이 바뀜

`c1-browsing`과 **task가 완전히 같고** segment만 둘로 나뉨. 30초에 브라우저 탭이 화상회의로 바뀐 상황.

| segment | mode | attributes |
|---|---|---|
| 0–30 s | browsing | wanted |
| 30–60 s | meeting | wanted |

recognizer: 0 s `chrome ×13` → 60 s 빈 집합. **30초에 query point가 없어요.** 이름 집합이 안 바뀌었으니까. 30–60초 segment는 채점되지만 그 안에 답이 없으니 0초의 답(browsing)이 meeting segment를 덮어요. 보장된 miss.

harness: 성능은 c1-browsing과 동일(같은 task, 같은 trace). Layer 1에서 "canonical set이 안 바뀌면 못 본다"는 scope boundary를 숫자로 남기는 파일.

#### `c6-dual` — 둘 다 진짜 foreground

게임을 하면서 동시에 컴파일이 끝나기를 적극적으로 기다리는 상황. oracle조차 label을 못 붙여요.

| segment | mode | attributes |
|---|---|---|
| 0–240 s | **ambiguous** | dual_active: true (background_wanted 없음) |

| id | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| game.chain.1–16 | game.exe | game-task-chain | 0 → 240 | lane_share 0.6. stage RUN 182 µs–1.09 ms |
| game.tail.1–284 | game.exe | game-task-chain | 0 → 240 | |
| editor | code | desktop-interactive | 0 → 240 | focus 2–238 s. wake 976개, 총 117.7 s |
| build | make | build-orchestrator | 10 → finite | spawn 85, cap 8. 자식 총 10.6 s |
| wine | wineserver | system-daemon | 0 → 240 | |

recognizer: 0 s `code, game.exe ×300, wineserver` → 10 s `+make, cc1 ×85` → 240 s `make, cc1`.

harness: `ambiguous`는 recognizer의 menu에 없어요. oracle이 이 파일에서 뭘 내는지는 **미결**이고(규칙대로면 답이 거부되어 fallback), 그래서 RQ0 gate spec에 guard 예외를 미리 적어둬요("random이 oracle을 이겨도 됨", "fallback 100%가 정상"). Layer 2 채점에서 제외. 단 oracle이 crash하면 안 되고 valid한 schedule과 log를 내야 해요. utilization 1.28.

---

### C7 — attribute counterparts (2026-09-10)

mode마다 하나, `c7-<mode>`는 `c1-<mode>`에서 파생돼요. base가 그 mode의 `true` cell, counterpart가 `false` cell(indexing만 반대). 이렇게 해서 driver table의 32 cell 전부가 coreset 안에 한 쌍씩 있어요 — Phase 6 pair review가 발견한 구멍(false cell 14개가 비어 있었음)을 메운 것.

두 가지 만드는 법:
- **interactive mode 10개**: base + `clamscan`(cpu-batch) 하나. 0초에 도착해 60 s 일을 하니 segment 내내 살아 있어요 — label이 매 순간 맞도록. 이름을 하나로 통일한 건 열 개 `false` cell이 mode로만 다르게 하려고, tier 1이라 어떤 pair도 familiarity tier가 안 바뀌어요.
- **batch mode 6개**: batch job 자체가 attribute가 판단하는 배경 작업이에요(vocabulary §1의 batch-mode clause, `c2-p1b`가 이미 쓰던 읽기). 그래서 counterpart는 "같은 일인데 아무도 안 시킨 것" — P1b의 rename 수법. `compile`은 `make`→`dkms`(kernel 업데이트 때 배포판이 알아서 돌리는 module rebuild). 나머지 넷은 배포판·vendor가 다른 이름으로 돌리는 같은 mode의 unwanted job이 없어서(Jellyfin의 transcoder도 process 이름은 그냥 `ffmpeg`) label만 뒤집고 pre-committed miss로 배송해요.

| 파일 | base + op | mode / attributes | utilization | miss |
|---|---|---|---|---|
| `c7-browsing` | `c1-browsing` + `clamscan`(cpu-batch, 0 s부터 60 s) | browsing / **false**, background: av-scan | 1.45 | — |
| `c7-office` | `c1-office` + `clamscan`(cpu-batch, 0 s부터 60 s) | office / **false**, background: av-scan | 1.50 | — |
| `c7-mail` | `c1-mail` + `clamscan`(cpu-batch, 0 s부터 60 s) | mail / **false**, background: av-scan | 1.53 | — |
| `c7-dev` | `c1-dev` + `clamscan`(cpu-batch, 0 s부터 60 s) | dev / **false**, background: av-scan | 1.46 | — |
| `c7-photo` | `c1-photo` + `clamscan`(cpu-batch, 0 s부터 60 s) | photo / **false**, background: av-scan | 1.47 | — |
| `c7-meeting` | `c1-meeting` + `clamscan`(cpu-batch, 0 s부터 60 s) | meeting / **false**, background: av-scan | 1.45 | — |
| `c7-gaming` | `c1-gaming` + `clamscan`(cpu-batch, 0 s부터 60 s) | gaming / **false**, background: av-scan | 2.46 | — |
| `c7-media` | `c1-media` + `clamscan`(cpu-batch, 0 s부터 60 s) | media / **false**, background: av-scan | 1.45 | — |
| `c7-video-edit` | `c1-video-edit` + `clamscan`(cpu-batch, 0 s부터 60 s) | video-edit / **false**, background: av-scan | 1.46 | — |
| `c7-idle` | `c1-idle` + `clamscan`(cpu-batch, 0 s부터 60 s) | idle / **false**, background: av-scan | 1.00 | — |
| `c7-compile` | `make` → `dkms` rename (kernel 업데이트 뒤 module rebuild, meas-ci:names:2로 검증) | compile / **false**, initiated: scheduled | 0.54 | — |
| `c7-indexing` | `c1-indexing`에서 label만 뒤집음 | indexing / **false**, initiated: scheduled | 0.95 | — (miss는 `c1-indexing` 쪽) |
| `c7-ml-train` | label만 뒤집음 (같은 이름, 같은 일) | ml-train / **false**, initiated: scheduled | 0.97 | **pre_committed_miss** |
| `c7-render` | label만 뒤집음 (같은 이름, 같은 일) | render / **false**, initiated: scheduled | 0.90 | **pre_committed_miss** |
| `c7-transcode` | label만 뒤집음 (같은 이름, 같은 일) | transcode / **false**, initiated: scheduled | 0.97 | **pre_committed_miss** |
| `c7-backup` | label만 뒤집음 (같은 이름, 같은 일) | backup / **false**, initiated: scheduled | 0.97 | **pre_committed_miss** |

**score.** counterpart는 base의 term에서 batch term을 뺀 것을 가져요 — unwanted work carries no term. interactive mode는 base와 같고(scan에는 term이 없으니), batch mode는 foreground P99만 남아요. lint가 이 규칙을 강제해요.

**demand.** 전부 `demand: calibration`을 recipe에 명시해서 window 검사에서 면제예요 — counterpart의 demand는 "base + 주입한 job"이라 pair가 통제이지 window가 아니에요. interactive counterpart는 1.45–1.53, `c7-gaming`은 2.46(base가 이미 lane_share 0.9), `c7-idle`은 정확히 1.00, batch counterpart는 base와 같아요.

**측정에서 알아둘 것.** `c7-meeting`과 `c7-media`는 두 row(true/false)가 모두 EDF라, TIMER task는 deadline class로 scan보다 먼저 돌아요. 2026-09-11에 boot default가 OSTEP 예시(10 ms slice)로 바뀌면서 residual slice도 10 ms가 됐고, 이건 video의 tick 허용치(10 ms)와 정확히 같아요. 계산상으로는 어느 row에서도, 그리고 `fixed`에서도(10 ms slice는 video의 6.67 ms burst를 강등시키지 않아요) tick을 놓치지 않아 headroom이 없지만, 경계에서 1 µs로 갈리는 knife edge라 simulator의 규칙 두 개(deadline task가 residual slice 도중에 lane을 뺏는지, 같은 순간 event의 처리 순서)가 답을 정해요(memo 2026-09-11 §5). 이 두 파일이 RQ0 판정 set에 남는지는 그 답을 받은 뒤 RQ0 gate spec에서 정해요(pair review finding 5 addendum).

---

## 11. 파일들 사이의 관계 — 무엇이 무엇에서 파생됐나

```
c1-office ────────────▶ c4-office     (+7z at 30 s)
c1-compile ───────────▶ c4-compile    (+chrome ×7 at 30 s)
c1-gaming ────────────▶ c4-gaming     (+discord at 30 s)
c1-media ─────┬───────▶ c5-t3         (rename → baloo_file, tracker-miner-fs-3)
              ├───────▶ c5-t4         (rename → video-playback-svc, audio-stream-helper)
              └───────▶ c5-t5         (rename → qzvd, xkrr)
c1-browsing ──┬───────▶ c6-spoof      (+chrome cpu-batch at 20 s)
              └───────▶ c6-fold       (segments → browsing 0–30, meeting 30–60)
c2-p1a ───────────────▶ c2-p1b        (rename python3 → tracker-miner-fs-3; seg 2 → indexing, unwanted)
c2-p2a ───────────────▶ c2-p2b        (download → clamscan cpu-batch; seg 2 → unwanted, av-scan)
c2-p3a ───────────────▶ c2-p3b        (ffmpeg → borg io-stream; seg 2 → backup, scheduled)
c1-<mode> ×16 ────────▶ c7-<mode>     (interactive 10: +clamscan cpu-batch at 0 s; compile: make → dkms;
                                       indexing, ml-train, render, transcode, backup: label만 flip; 전부 wanted → false)
c3-workday, c3-evening, c3-creation, c6-dual: 독립 (파생 없음)
```

recipe는 `dataset/timelines/coreset/*.variant.yaml` 다섯(`c2-pairs`, `c4`, `c5`, `c6`, `c7`). op는 `rename`, `patch-task`, `add-task`, `patch-segment`, `set-segments`, `patch-meta`(seed·id는 못 바꿈). 파생 파일은 base의 seed를 물려받아요.

이 관계가 실험에 주는 것:
- C4는 "원본과의 delta"로만 의미가 있어요.
- C5는 성능이 c1-media와 같아야 하고, 그 자체가 pipeline의 sanity check예요.
- C2의 b는 a와 한 곳만 다르니 gap이 그 한 곳에 귀속돼요.
- C7은 base와 task 하나(또는 이름 하나, 또는 label만) 다르니 attribute의 효과가 그 한 곳에 귀속돼요.

---

## 12. 알아둘 특이점과 열린 항목

이 문서를 쓰면서 compiled file에서 직접 확인한 것들. 일부는 Phase 5 spec 세션의 아카이브에도 있어요.

**행동에 관한 것**
- focus가 없는 `desktop-interactive` task는 `WAIT` 하나짜리 program이라 CPU를 전혀 안 써요. `c1-office`의 `browser`, `c4-compile`의 `injected-browser`, `c3-creation`의 240초 이후 `kdenlive`.
- `system-daemon`의 SLEEP은 편차가 매우 커서 어떤 instance는 파일 안에서 한 번도 안 깨요. `c1-gaming`/`c4-gaming`의 `wineserver`(1225 s), `c3-evening`의 `wineserver`(457 s).
- C2의 batch task 셋과 C3의 batch/build 셋은 **전부 window 안에 못 끝나요.** `c2-p1a` hog 130 s/120 s 남음, `c2-p2a` download 25 s이지만 chain이 95% 요구, `c2-p3a` ffmpeg 75 s/60 s, `c3-creation` HandBrake 320 s/180 s, `c3-workday` 자식 349 s/300 s. 그래서 judging set에서 `turnaround`는 관측 불가이고 progress(`cpu_delivered / demand`)가 batch 쪽의 metric이에요.
- `c3-evening`의 chain은 lane_share 1.45라 혼자서도 frame을 못 맞춰요. backlog가 설계상 발생.
- `c2-p2a`와 `c2-p2b`는 p1 pair와 달리 background task의 archetype이 달라요(network-bulk vs cpu-batch). "행동 동일"은 p1에만 엄격히 성립.
- `c2-p3` pair는 둘 다 `background_wanted: true`. 구분 축은 mode와 `initiated`.
- `c5-t3`의 이름(`baloo_file`, `tracker-miner-fs-3`)은 실제로는 indexer인데 player처럼 행동해요. 의도된 오도.
- 게임 파일에서 TIMER를 가진 task는 `game.chain.1`, `steam`(heartbeat), `steamwebhelper`, `gamescope`(c1/c4-gaming만), `discord`, chrome renderer들이에요. Electron heartbeat도 TIMER라 `deadline` line을 내지만 records가 entity별이라 무해해요.

**telemetry에 관한 것**
- finite task는 telemetry에서 안 사라져요. 마지막 snapshot에 `make`, `python3`, `7z` 같은 것이 남아 있어요.
- `c6-fold`는 30초에 query point가 없어요. `c6-spoof`는 개수 변화(13→14)로 query point가 생겨요.
- spawn 자식은 부모와 함께 보여요(`cc1 ×100`, `×4200`, `×85`).

**열린 항목** (결정된 것이 아님)
- ~~C1에서 파생된 8개 파일의 `demand: calibration`이 상속인지 선언인지 미결~~ → **2026-09-10 결정(Phase 7)**: 모든 파생 파일(`c4-*`, `c5-*`, `c6-fold`, `c6-spoof`, `c7-*`)이 recipe에 `patch-meta: {demand: calibration}`을 명시해요. 파일의 실제 regime은 manifest의 utilization으로 읽어요. C6는 여전히 calibration 둘 + oversubscribed 하나라 논문 표에 각주 필요.
- `wineserver`를 `system-daemon`으로 두는 건 provisional. LAVD는 wine을 게임 task graph의 일부로 봐요. constructor 구현 때 결정.
- TIMER의 t₀(등장 시각 vs 전역 0)는 simulator의 미결 질문. `c3-evening`처럼 TIMER task가 중간에 등장하는 파일에서 영향.
- familiarity tag는 2026-09-08부터 compile을 통과해 `ground_truth`에 실려요(`dataset/schema/workload.schema.json`의 optional 필드; C5 세 파일의 hash가 바뀜). 남은 것: C5 밖의 segment에 annotation을 달지 — `c1-media`가 tier 1 기준선으로 자연스러운 첫 후보예요. 이름별 tag는 여전히 없고, 파일(segment) 단위예요.
- `random` condition이 무엇에서 uniform하게 뽑는지(16 mode? 32 row?) 미정. 박이안과.
- **pre_committed_miss**(2026-09-10): 이름·행동으로는 label에 닿을 수 없는 segment에 붙는 다섯 번째 annotation. attribute 쪽에서는 `c1-indexing`과 `c7-ml-train`·`c7-render`·`c7-transcode`·`c7-backup`. coverage grid가 이걸 읽어 cell을 "채워졌지만 recognition-limited"로 표시하고, grader는 Phase 8에서 accuracy에서 제외해요.

---

## 13. 용어 정리

| term | 뜻 |
|---|---|
| **workload** / **run file** | 실험 하나를 완전히 적은 canonical JSON. `meta`, `ground_truth`, `events` |
| **timeline** | 사람이 쓰는 authoring YAML. compile되어 workload가 됨 |
| **archetype** | process 한 종류의 행동 model. program + parameter 분포. 이름 없음 |
| **scenario** | 같이 나타나는 process 이름의 묶음. S1–S18. 근거 tag |
| **segment** | label(mode + attributes)이 붙은 시간 구간 |
| **mode** | 16개 label 중 하나. machine이 주로 뭘 하고 있나 |
| **`background_wanted`** | 지속적인 배경 작업이 사용자가 원한 것인가. 배경 작업이 없으면 true |
| **`ambiguous`** | ground truth 전용 label. recognizer menu에 없음 |
| **task** | workload의 `arrive` event 하나. id와 name을 가짐 |
| **id / name** | id는 simulator·harness용 고유 식별자(`renderers.3`), name은 recognizer가 보는 것(`chrome`) |
| **program** | task의 script. 여섯 primitive + LOOP |
| **primitive** | RUN, SLEEP, TIMER, WAIT, WAKE, FORK/EXIT |
| **channel** | WAIT/WAKE가 만나는 이름. `input:<id>`, `chain:<id>`, `children:<id>` |
| **wake event** | run file의 외부 자극. keystroke |
| **focus** | timeline에서 사용자 주의가 어느 task에 있나. keystroke가 생성되는 window |
| **segment-bound / finite / spawned** | lifetime 세 종류 |
| **depart** | segment-bound task의 pinned 퇴장 시각 |
| **spawn table** | orchestrator가 만들 자식들의 program 목록. compile 시점에 고정 |
| **fork_cap** | 동시에 살아 있을 수 있는 자식 수. `make -j8`의 8 |
| **chain** | game-task-chain의 frame pipeline. head(TIMER) → … → tail |
| **tail (game)** | chain 밖의 near-idle task 284개 |
| **lane_share** | chain이 요구하는 lane의 비율. `-single`에서 chain RUN을 이 값에 맞춰 scale |
| **lane scaling** | `-single` compile의 scale pass. game-task-chain에만 적용 |
| **utilization** | Σ RUN / T_end. 파일이 lane을 얼마나 요구하나 |
| **demand class** | `oversubscribed`(1.0–1.5 window 검사) 또는 `calibration`(면제) |
| **familiarity** | process 이름이 corpus에서 얼마나 알아볼 만한가, 1–5 tier. 이름의 속성, 행동과 무관. recognition accuracy를 묶어서 보고하는 split key. 명시 annotation은 C5 segment에만 |
| **seed** | timeline의 난수 seed. 모든 draw를 결정 |
| **per-task / per-iteration / per-instance** | sampling 단위 |
| **unroll** | bounded 반복을 구체적 값으로 펼치는 것 |
| **variant** | base timeline + op로 파생된 timeline. seed 상속 |
| **coreset-single / -native** | lane-scaled(실험용) / 측정 그대로(공개용) |
| **telemetry snapshot** | 살아 있는 이름의 multiset. 바뀔 때마다 하나 |
| **query point** | snapshot이 나온 시각. recognizer가 호출됨 |
| **pinned event** | 시각이 파일에 박힌 event. 등장, depart, wake |
| **emergent** | scheduler에 따라 달라지는 시각. spawn, exit, 모든 실행 |
| **meas-ci** | 우리 CI 측정 캠페인의 source id |
| **C1–C7** | coreset의 일곱 그룹 |
| **counterpart (C7)** | 한 mode의 `false` cell을 담는 파일. 그 mode의 C1 base + op 하나 |
| **pre_committed_miss** | 이름·행동으로는 맞힐 수 없는 segment의 annotation. accuracy에서 제외, 따로 보고 |
| **judging set** | RQ0 gate 판정에 쓰는 파일. C2의 6개 |

---

## 이 문서를 다 읽었으면

- `dataset/README.md`가 tree와 명령을, building-plan이 설계 근거를, archetype-plan이 archetype 규칙을, interpretation contract가 실행 semantics를 갖고 있어요. 이 문서는 그것들의 "왜"와 "실제 숫자"를 이어준 것.
- harness가 이 파일들을 어떻게 읽고 숫자로 바꾸는지는 `docs/harness/harness-and-records-guide.md`.
- 숫자를 직접 보려면 `cd dataset && make dataset` 후 `build/coreset-single/`.
