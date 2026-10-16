# Coreset 안내 — 51개 workload를 하나씩 뜯어보기

> Status: draft · Created 2026-09-08 · Updated 2026-10-17

이 문서는 **공부용 문서**예요. dataset이 무엇이고, 어떻게 만들어지고, 51개 coreset 파일 각각이 무슨 상황을 담고 있으며 어떤 숫자를 갖고 있는지를 OS/시스템 지식이 거의 없는 사람 기준으로 풀어 써요. 설계의 규범적 근거는 building-plan(`docs/workload/building-plan.md`), archetype의 규범적 정의는 archetype-plan(`docs/workload/archetype-plan.md`), 실행 semantics는 interpretation contract(`docs/simulator/interpretation-contract.md`)에 있어요. 이 문서는 그 셋을 읽을 수 있게 만드는 다리이고, 숫자는 `dataset/build.manifest.json`이 hash로 고정한 `coreset-single`의 51개 파일(2026-10-16에 re-bless된 build)과 그 manifest의 `demand` 기록, 그리고 timeline과 `dataset/archetypes.yaml`에서 직접 읽은 값이에요.

읽는 규칙: term은 영어 그대로, 다른 문서는 절 번호 대신 내용으로 가리켜요.

---

## 목차

1. dataset이 실험에서 하는 역할
2. 세 층 구조 — archetype library, scenario catalog, timeline
3. 여섯 가지 primitive — task의 program
4. archetype 29개 — 각각 어떤 프로그램인가
5. compile — timeline이 workload가 되기까지
6. canonical workload file의 해부
7. recognizer가 보는 것 — telemetry snapshot과 query point
8. demand와 utilization — 의자를 얼마나 요구하나
9. 일곱 그룹 C1–C7 — 각 그룹이 답하는 질문
10. 51개 파일 상세
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
| **recognizer** (daemon 안) | process **이름**과 개수, 창 focus를 가진 process의 이름. `code ×1, python ×1`, focus `code` | 행동, 정답 |
| **simulator** | 각 task의 **program**과 `declared_class`. "3 ms 일하고 keystroke를 기다림" | 정답, focus. 이름은 run file에 있지만 scheduling 결정에 쓰이지 않아요 |
| **harness** | **정답** (`ground_truth`). "60–99.435초는 ml-train" | (전부 봄. 채점자니까) |

이 비대칭이 실험의 근간이에요. recognizer가 행동 통계를 보면 "이름에서 의미를 읽는다"는 주장이 오염되고, executor가 이름으로 결정하면 condition 사이의 차이가 configuration 차이가 아니게 돼요.

또 하나. **compile 시점에 모든 randomness가 해소돼요.** keystroke가 언제 오는지(측정된 typing 기록의 어느 조각인지), 각 wake가 몇 µs 일하는지, 컴파일 자식이 몇 ms 일하는지가 전부 파일에 구체적 숫자로 적혀 있어요. simulator는 주사위를 던지지 않아요. 그래서 어떤 condition으로 돌리든 모든 task는 byte 단위로 같은 일을 요구하고, 결과 차이는 scheduler 설정 차이로만 생겨요.

**core set과 generated layer.** 이 문서가 다루는 51개 파일이 core set이에요(`dataset/timelines/coreset/`, compile 결과는 `dataset/build/coreset-single/`). 그 옆에 generated layer가 있어요. `dataset/tools/generate.py`가 `dataset/grids.yaml`을 읽고 C1(16개의 single-situation 파일)의 task set을 이어 붙이거나 이름을 바꿔서 다섯 set을 만들어요: transition grid 480개, return grid 720개, flap-stress set 24개, distractor grid 272개, familiarity ladder 66개, 모두 1,562개. 같은 compiler로 `build/<set>-single/`에 compile되고, set마다 manifest(`dataset/build.<set>.manifest.json`)가 하나씩 있어요. 전부 design이라 데스크톱에서 그런 상황이 얼마나 자주 오는지는 주장하지 않아요. C3, C4, C5의 rate 주장(전환을 얼마나 빨리 정확히 따라가나, 끼어든 process에 얼마나 흔들리나, 낯선 이름을 얼마나 읽나)은 이 set 위에서 돌고, core set의 손으로 쓴 C3–C5 파일은 그런 상황이 존재한다는 사례예요(9장).

generated 파일은 이렇게 소비돼요.
- scoring spec(`harness/scoring/scoring-spec.yaml`)에 자기 entry가 없어요. harness가 돌 때 규칙 하나로 term을 만들어요(`harness/tools/harness/scoring.py`의 `with_generated`, 규칙 원문은 scoring spec의 header): manifest가 기록한 placement마다(어떤 mode의 C1 task set을 id 접미사 `-s0`, `-s1`, …을 붙여 놓은 것) 그 mode의 `c1-<mode>` entry의 term을 가져와 entity id에 접미사를 붙이고(chain 멤버는 `.chain.<n>` 앞에 붙어 `game-s0.chain.1`), latency·periodic term은 그 placement가 label된 segment로 window를 걸어요. label된 segment가 없는 placement(distractor grid에서 도착하는 set)는 term이 없고, input window가 없는 placement는 `channel: input` term만 빠지고, idle placement는 `c1-idle`처럼 term이 없어요. batch term은 C1 entry의 turnaround인데, job이 끝나지 못한 row에서는 censored bound(파일 끝 − 도착)로 채점돼요.
- experiment spec은 pin된 manifest에서 grid 축으로 파일을 골라요: `files.select`, manifest마다 `pins.generated` pin 하나. 축은 records의 column이 아니라 `workload_id`로 manifest와 join해서 읽고(`harness/tools/harness/manifests.py`), 고른 파일은 spec의 reporting 목록에만 들어가요.

자세한 것은 `dataset/README.md`(tree와 명령)와 `docs/harness/harness-and-records-guide.md`(harness 쪽)에 있어요.

---

## 2. 세 층 구조 — archetype library, scenario catalog, timeline

dataset은 세 층으로 쌓여 있어요. timeline이 archetype id와 scenario tag를 가리키고, 반대 방향 참조는 없어요.

```
ARCHETYPE LIBRARY   한 종류의 process가 어떻게 행동하나      dataset/archetypes.yaml
SCENARIO CATALOG    어떤 사용 상황과 이름이 있나 (S1–S18)      docs/workload/scenario-catalog.md
TIMELINES           scenario들이 시간 위에 어떻게 배치되나     dataset/timelines/coreset/*.timeline.yaml
                                        │
                                        ▼  wlc (workload compiler) + seed
                              CANONICAL WORKLOAD JSON                dataset/build/coreset-single/*.workload.json
```

**archetype library.** "process 한 종류가 scheduler 눈에 어떻게 보이나"의 model. scheduler에게 process는 이름도 의미도 없고 오직 event stream이에요. 언제 runnable해지고, 얼마나 실행하고, 무엇을 기다리고, 누구를 깨우고, 언제 fork하고 exit하는가. archetype은 그 stream을 만드는 규칙 + parameter 분포예요. 29개 중 28개는 우리 CI의 측정 campaign에서 값을 가져왔고, 하나(`game-task-chain`)는 LAVD를 소개한 OSS NA 2024 발표 slide(`lavd-ossna24`)에서 가져왔어요(4장). archetype은 이름을 갖지 않아요. `video-player`라는 archetype은 "mpv가 30 fps 동영상을 재생할 때 33.3 ms 주기마다 측정된 만큼 일한다"만 알고, 그 task가 recognizer에게 무슨 이름으로 보일지는 timeline이 정해요(`c5-t5`에서는 같은 archetype이 `qzvd`로 보여요).

**scenario catalog.** dataset의 파일이 묶는 사용 상황(scenario)과 그 이름들의 목록. S1(office)부터 S18(session process)까지 18개. 각 행은 그 상황과 이름이 실제로 있다는 근거를 외부 출처(PCMark, SYSmark, CpsMark+ 같은 benchmark, LAVD의 OSS NA 2024 발표 slide `lavd-ossna24` 등)로 대요. 어느 것들이 한 segment에 같이 나타나는지는 실험의 구성이라 design이에요. 숫자는 없어요. 이름과 근거만. timeline의 segment가 `scenario: [S1, S2]`처럼 tag로 가리켜요.

**timeline.** 사람이 쓰는 authoring 파일. segment(시간 구간 + label)와 task(이름, archetype, 등장/퇴장 시각)를 시간축 위에 배치하고, keystroke window(`input`), 창 focus(`focus`), operation(`operations`) track을 가져요. 숫자 parameter는 여기 없어요. archetype id로만 참조하고, archetype이 `binding_params`로 요구하는 손잡이(job의 CPU 총량 `total_work`, spawn 개수, `lane_share`, chain 멤버의 이름 같은 것)만 채워요.

이렇게 나눈 이유:
- 측정이 바뀌면 archetype 하나만 고치면 돼요. 파일 수십 개를 안 건드려요.
- **이름과 행동이 분리**돼요. C5(familiarity ladder)는 "같은 archetype, 다른 이름"으로 정의돼요. recognition 차이가 있으면 이름 때문이라고 확신할 수 있어요.
- C6의 "chrome이라는 이름을 단 batch job"도 timeline에서 `{name: chrome, archetype: cpu-batch}`로 그냥 쓸 수 있어요.

timeline 하나를 실제로 보면:

```yaml
# dataset/timelines/coreset/c2-p1a.timeline.yaml (header 주석 생략)
meta:
  id: c2-p1a
  seed: 201

segments:
  - {from: 0s, to: 60s, mode: dev, attributes: {background_wanted: true},
     scenario: [S11]}
  - {from: 60s, to: 99.435s, mode: ml-train, attributes: {background_wanted: true},
     scenario: [S11, S12]}

tasks:
  - {id: editor, name: code, archetype: code-editor,
     arrive: 0s, depart: 99.435s}
  - {id: hog, name: python, archetype: cpu-batch, arrive: 60s,
     bind: {total_work: 1389.885s, program: python3},
     source: {total_work: "meas-ci:background:2026-10-03", program: [pytorch-examples, "meas-ci:background:2026-10-03"]}}

input:
  - {from: 2s, to: 97.435s, task: editor}

focus:
  - {from: 0s, to: 99.435s, task: editor}
```

- `meta`: id와 seed. `demand`가 없으니 class는 기본값 `oversubscribed`예요(8장: class는 design의 이름표일 뿐).
- `segments`: 0–60초는 `dev`, 60–99.435초는 `ml-train`. 둘 다 `background_wanted: true`. 두 번째 segment의 39.435 s는 짝 파일 `c2-p1b`의 indexer가 측정에서 쓴 CPU 총량이에요 — 두 파일 모두 그 segment의 모든 순간에 job이 어떤 policy에서도 살아 있도록. `scenario`는 근거 tag.
- `tasks`: `editor`는 `code`라는 이름으로 `code-editor`(측정된 Visual Studio Code)처럼 행동하고 0초에 와서 99.435초에 사용자가 닫음. `hog`는 `python`이라는 이름(kernel이 보여주는 comm)으로 `cpu-batch`의 `python3` program처럼 행동해요 — PyTorch의 기본 MNIST 예제를 CPU에서 실제로 학습시킨 측정이에요(데스크톱 사용자가 MNIST를 학습시킨다고 주장하는 건 아니에요). 60초에 와서 측정된 CPU 총량 1,389.885 s를 통째로 일하려 해요. 퇴장 시각 없음(일이 끝나면 스스로 나감) — 이 파일은 job이 끝나기 전에 끝나요. `bind`로 묶는 값(그리고 `count`)마다 출처가 있어요: 같은 key로 된 `source` map에 registry tag(`meas-ci:background:2026-10-03` 같은), tag 목록, 또는 label(`design` / `convention` / `arithmetic`) 중 하나. linter가 key set과 tag를 검사해요(2026-10-11, 9.18).
- `input`: keystroke가 어느 task로 들어가나. 2–97.435초 동안 `editor`. **keystroke는 input window 안에서만 생성돼요.** 측정된 typing 기록의 한 조각이 그 window에 재생돼요(5.2절). (2026-10-11 전에는 이 track의 이름이 `focus`였어요.) derived file의 window는 `slice_of: {from, to, index}`로 base의 어느 window의 조각인지 들고 있어요 — deriver가 적고, compiler는 그 base window 기준으로 stimulus offset을 뽑아요. 그래서 c7 counterpart의 keystroke는 base의 같은 구간과 byte-identical이에요(9.18).
- `focus`: 어느 task의 창이 **focus**를 갖고 있나. 0–99.435초 동안 `editor`. 사용자가 마지막으로 앞에 세운 창에 머물고, typing을 멈춰도 사라지지 않고, 창이 하나도 없을 때만 비어 있어요. 모든 `input` window는 같은 task의 `focus` interval 안에 있어야 해요. 이 track은 compile된 파일의 `focus` key로 실려 recognizer에게 **보여지는** 것이에요(7장).
- `operations`(이 파일에는 없음): 측정된 앱의 operation 하나를 어느 시각에 놓을지(3장).

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

TIMER — 주기와 deadline이 있는 periodic job — 를 쓰는 건 playback과 call entry(4.2절)와 game chain의 head뿐이에요. TIMER의 t₀는 task가 그 TIMER를 처음 실행한 시각이에요. dataset lint가 TIMER를 가진 program은 실행 순서상 TIMER로 시작하도록 강제하고(LOOP의 body 첫머리 포함), reference simulator(`simulator/src/sim.cpp`)는 task가 도착하는 순간 그 program을 RUN이나 막히는 명령에 닿을 때까지 진행시켜요. 그래서 첫 TIMER는 lane을 받기 전, 도착하는 순간 실행되고, t₀는 그 task의 도착 시각이에요. lane이 바빠도 그래요(10장 `c3-evening`).

**`WAIT`의 channel**은 누가 깨우느냐로 나뉘어요.
- `input:<task id>`: run file의 `wake` event가 깨워요(keystroke).
- `timer:<task id>`: 역시 run file의 `wake` event가 깨워요. 측정된 앱의 thread가 스스로 깨던 것(timer component, 4.1절)을 compile 때 절대 시각의 wake로 펼친 것이고, deadline이 없어요. 주기적으로 보이지만 TIMER가 아니에요.
- `chain:<task id>`: game chain의 앞 멤버가 `WAKE`로 깨워요.
- `job:<task id>`: build의 job 하나 안에서 멤버들이 job의 부모-자식 순서대로 서로 `WAKE`해요(5.4절).
- `children:<task id>`: orchestrator(`make`, `dkms`)가 마지막 `FORK` 뒤에 기다리는 channel. orchestrator가 spawn한 마지막 자식이 끝날 때 executor가 이 WAIT를 완료시킨다(그때 살아 있는 자식이 없으면 막지 않고 바로)는 규칙이 interpretation contract의 FORK·WAIT에 제안돼 있고, 인경민이 동의하면 효력이 생겨요(`docs/data-contracts.md` §14의 2026-10-16 항목). reference simulator(`simulator/src/sim.cpp`)는 아직 구현하지 않아서 그 simulator에서는 `make`가 run 끝까지 거기서 막혀 있어요(12장).

**operation.** 측정된 앱 넷은 사용자가 시킨 일 하나를 측정해서 들고 있어요: `web-browser`의 page-load(측정 길이 중앙값 약 0.47 s), `image-editor`의 unsharp mask(약 2.36 s), `video-editor`의 preview-render(약 11.4 s), `mail-client`의 send(약 2.9 s). timeline의 `operations` track이 `{at, task, name}`으로 시작 시각만 정하고, compiler가 측정된 길이표에서 길이를 뽑아 그 구간 동안 operation의 component가 task의 다른 wake를 대신하게 해요(그 구간에는 keystroke도 안 생겨요). operation은 그 task의 input window 안에서만 시작하고 window 하나에 하나예요(design). 60 s C1 base에서는 2–58 s window의 30 s(mail의 send는 40 s), 길이를 바꾸거나 자른 파일에서는 window 안의 같은 비율 자리에 놓여요(예: `c7-browsing`의 2–24.385 s window에서 13.1925 s, `c1-transcode`의 2–4,760 s window에서 2,381 s). C2와 C3의 파일은 각자의 표에 적힌 시각에 놓여요. operation은 event op가 아니라 task의 WAIT/RUN stream 안으로 compile되고, compile report(`build/coreset-single/<id>.report.json`의 `operations`)가 시각과 길이를 적어요.

---

## 4. archetype 29개 — 각각 어떤 프로그램인가

`dataset/archetypes.yaml`의 29개. 28개는 우리 CI의 측정 campaign(`meas-ci:<workflow>:<run>` tag; GitHub-hosted ubuntu-24.04 runner의 AMD EPYC 7763 CPU 하나에 측정 대상을 고정하고 `perf sched record`로 기록)에서 값을 가져왔고(`category_source: meas`), 하나(`game-task-chain`)는 `lavd-ossna24`에서 가져왔어요. 각 entry는 `declared_class`(program이 자기에게 거는 scheduling class: `normal` 또는 `idle`; compiler가 그 entry를 묶은 모든 task와 spawn 자식에 복사해요), `pattern.program`(primitive로 쓴 program 모양), `params`(각 숫자가 분포 + 출처; 측정값은 대부분 `quantiles` — p1부터 p99.9까지의 측정 분위수를 보간해서 뽑아요), `lifetime`, `binding_params`(timeline이 채워야 하는 손잡이), `validation_stats`(무엇을 쟀나: 프로그램 version, 입력, repeat 수, 범위), `modeling_notes`(출처 위에 우리가 무엇을 지어냈나)를 가져요. 측정값은 "그 runner에서 그 software를 잰 값"이지 데스크톱의 진실이 아니에요 — 각 entry의 scope가 그렇게 적어요.

### 4.1 측정된 interactive 앱 — 사람이 만지는 앱

| archetype | 측정한 것 | timeline이 보여주는 이름 | keystroke stream |
|---|---|---|---|
| `office-writer` | LibreOffice 24.2 Writer, 약 76쪽 문서의 끝에서 타이핑 | `soffice.bin` | SWELL-KW의 Word stream |
| `code-editor` | Visual Studio Code 1.138, TypeScript project, language server 켬 | `code` | SWELL-KW의 Word stream |
| `mail-client` | Thunderbird 156, compose window, loopback SMTP | `thunderbird-bin` | SWELL-KW의 Outlook stream |
| `web-browser` | Google Chrome 152/153, text area가 있는 local page(보이는 page의 renderer 포함) | `chrome` | SWELL-KW의 Internet Explorer stream |
| `image-editor` | GIMP 2.10.36, 4952×3288 image, script로 움직인 pointer | `gimp` | 없음 |
| `video-editor` | Kdenlive 23.08.5, 20 s 1080p clip project, script로 clip monitor scrub | `kdenlive` | 없음 |

program 모양은 `LOOP { WAIT(input) → RUN(event) }`라고 적혀 있지만, compile 결과는 측정된 것 여러 가지를 시간순 stream 하나로 합친 거예요(5.2절).
- **timer component** (`components`): 측정 중 앱의 각 thread(comm)가 스스로 깬 빈도와, 간격·RUN의 분위수 표. task의 lifetime 내내 component마다 wake를 표에서 뽑아 `WAIT(timer:<id>)` + `RUN`으로 펼치고, run file에는 그 시각의 `wake` event가 들어가요. 예: `code-editor`는 component가 아홉 개예요(`gpu/VizCompositorTh` 초당 23.1회, `renderer/Compositor` 22.8회, …).
- **keystroke** (`stimulus` + `input_run`): input window 안에서 측정된 typing 기록(SWELL-KW 연구의 실제 keystroke 시각)의 한 조각을 재생해요. keystroke마다 `WAIT(input:<id>)` + `RUN`(측정된 keystroke 처리 시간 `input_run`의 분위수 표에서).
- **driven cadence** (`focus_components`): GIMP와 Kdenlive는 keystroke 대신 pointer로 움직이는 driven phase를 측정했고, input window 안에서는 그 component가 평소 component를 대신해요. 그래서 이 둘에게는 `input:` wake가 하나도 없어요(5.2절).
- **operation** (`operations`): 3장.
- **heavy event** (`heavy_events`): 드물게 오는 큰 run. 정해진 시각 없이 측정된 비율대로 떨어져요(예: `web-browser`의 `MemoryInfra`, 초당 0.00035회).
- **launch phase** (`launch`): 파일 중간에 시작되는 task는 측정된 launch 구간 하나를 먼저 재생하고 steady stream으로 넘어가요(예: `c3-workday`의 writer와 mailer).

결과적으로 측정된 editor의 program은 keystroke와 RUN이 번갈아 나오는 모양이 아니에요. 대부분의 파일에서 timer wake가 keystroke보다 훨씬 많아요(`c1-dev`의 editor: keystroke 186개, timer wake 6,456개; `c1-office` 파일 전체: keystroke 270개, timer wake 3,064개). input window가 없는 task도 timer component로 계속 조금씩 깨요(`c1-office`의 `browser`: timer wake 2,678개, CPU 합 0.18 s).

### 4.2 periodic — playback과 call

| archetype | 측정한 것 | period | cycle run 중앙값 | 이름 |
|---|---|---|---|---|
| `video-player` | mpv 0.37, 1280×720 30 fps H.264 file, `--vo=x11` | 33,348 µs (30 fps) | 3.98 ms | `mpv` |
| `audio-player` | mpv 0.37, 같은 file의 AAC audio, `--no-video` | 49,635 µs | 0.33 ms | `mpv` |
| `video-call` | Chrome의 loopback WebRTC 통화(가짜 720p30 카메라·마이크) | 10,001 µs (10 ms audio frame) | 1.19 ms | `chrome` |

```
LOOP { TIMER(period) → RUN(cycle_run) }
```

앱 thread들의 CPU를 medium cycle(video frame, audio buffer, 통화의 audio frame) 하나당 합쳐서 job 하나로 만든 거예요. thread 하나하나의 wake는 싣지 않아요. compile되면 LOOP가 아니라 cycle마다 `TIMER, RUN`이 펼쳐지고 RUN 값은 cycle마다 분위수 표에서 뽑혀요(`c1-media`의 video: 1,800 cycle, RUN 합 7.25 s; music: 1,209 cycle, 0.43 s). 마지막에 TIMER가 하나 더 붙어서, 사용자가 닫을 때 task는 다음 tick을 기다리는 상태예요. 통화는 audio와 video thread를 합친 task 하나이고 그 job이 10 ms audio frame이에요.

### 4.3 숨은 탭, chat client, Steam client — 아무도 안 만지는 앱

| archetype | 측정한 것 | 이름 | 측정된 wake 빈도 |
|---|---|---|---|
| `renderer-hidden` | Chrome 154의 background 탭 renderer 하나(site-per-process: site 하나에 renderer 하나), Chromium의 intensive throttling grace 이후 | `chrome` | renderer 하나에 초당 약 0.21회 |
| `chat-client` | Element Desktop 1.12.28, homeserver의 방 하나에 로그인, 메시지 없음 | `element-desktop` | 초당 약 12회 |
| `game-client` | Steam desktop client, 로그아웃(계정 없음), 창이 보임 | `steam` | 초당 약 300회 |

program은 `LOOP { WAIT(timer) → RUN(event) }`: timer component만 있어요(keystroke도 cadence도 없음, 사람이 없는 상태로 측정). 주기적인 heartbeat TIMER가 아니에요. `game-client`는 드문 큰 run(`CHTTPClientThre`)도 heavy event로 들고 있어요.

Chrome을 보여주는 파일은 browser(`web-browser`) 옆에 `renderer-hidden` 넷을 둬요(`count: 4`): Firefox Linux telemetry의 창당 탭 다섯(`glam`)과 Chrome에서 관찰한 탭당 renderer 하나(`meas-ci:desktop:2026-10-04`)에서 온 수예요. 실제 page의 cross-site iframe이 가져갈 renderer는 빠져 있으니 이 수는 하한이에요. 보이는 page의 renderer는 `web-browser` task 안에 있어요.

Steam client는 측정된 상태 그대로예요: 로그아웃, 계정 없음, library 없음, 뒤에 도는 game 없음, `gameoverlayui` 없음. gaming timeline들의 header가 이걸 적어요.

### 4.4 batch loop — 끝나면 스스로 나가는 job

```
LOOP { RUN(<program>_run) → SLEEP(<program>_block) }   (total_work만큼 CPU를 쓸 때까지)  → EXIT
```

측정된 job에서 "자발적 block 사이의 run"과 "그 run 뒤의 block"의 분위수 표를 만들어 두고, 거기서 번갈아 뽑아 `total_work`를 다 쓸 때까지 펼쳐요. block이 0이면(다른 thread가 바로 이어서 돌았다는 뜻) 양쪽 run을 RUN 하나로 합쳐요. 표는 task의 표시 이름이 아니라 entry가 정해요(`cpu-batch`는 `program` binding으로 고름). `total_work`는 그 job의 측정된 CPU 총량 전체예요(9.10 D17: job은 측정된 그대로 통째로 묶음). 예외 둘은 design: `c4-office`의 7z 6 s(주입의 크기)와 `c6-spoof`의 30 s.

| archetype | 측정한 job | 이름 | CPU 총량 | class |
|---|---|---|---|---|
| `cpu-batch`, `program: python3` | PyTorch의 기본 MNIST 예제를 기본값으로 CPU에서 학습(14 epoch, 실제 MNIST dataset). 실제 학습 run이지만 데스크톱 사용자가 MNIST를 학습시킨다고 주장하지는 않아요 | `python` | 1,389.885 s | normal |
| `cpu-batch`, `program: kdenlive_render` | Kdenlive가 render dialog로 `video-editor`의 project를 기본 profile로 export(일의 99.6 %는 그 자식 `melt-7`) | `kdenlive_render` | 16.545 s | normal |
| `cpu-batch`, `program: spoof` | 측정 아님: `c6-spoof`의 가짜 chrome. 끊김 없는 RUN 하나(design) | `chrome` | 30 s (design) | normal |
| `file-archiver` | 7-Zip 23.01, thread 여덟, Matt Mahoney의 10 GB 파일 set 압축 | `7z` | 6 s (design, `c4-office`만) | normal |
| `game-download` | SteamCMD로 Team Fortress 2 Dedicated Server를 새로 설치(10.4 GB, 121 Mbps로 shaping) | `steam` | 727.170 s | normal |
| `game-download-idle` | `game-download`의 표를 그대로 공유하고 class만 바꾼 entry | `steam` | 727.170 s | idle |
| `package-upgrade` | Ubuntu 24.04 기본 unattended upgrade의 install 단계(glibc 보안 update; 단명 process 916개의 사슬) | `unattended-upgr` | 26.385 s | normal |
| `file-indexer` | Tracker Miners 3.7.1이 빈 database에서 home을 처음 index(miner, extractor, GStreamer registry scan; process 다섯) | `tracker-miner-f` | 39.435 s | idle |
| `video-transcoder` | HandBrakeCLI 1.7.2 기본 preset "Fast 1080p30"으로 Big Buck Bunny 4K를 1080p로(CpsMark+의 HandBrake workload) | `HandBrakeCLI` | 2,970.871 s | normal |
| `incremental-backup` | Déjà Dup 45.2와 duplicity의 예약된 주간 incremental(gpg 암호화), monitor가 `chrt --idle 0 ionice -c3`로 시작 | `deja-dup` | 165.668 s | idle |

download는 `steam`이라는 이름으로 보이지만 측정은 SteamCMD(Steam의 명령줄 client)로 했어요 — 대체한 것을 밝혀 둬요.

**idle class와 그 한계.** `file-indexer`와 `incremental-backup`은 program이 스스로 SCHED_IDLE을 걸어요(indexer는 nice 19도, backup은 idle I/O class도). 그래서 entry가 `declared_class: idle`이고, executor는 엄격한 idle 규칙으로 돌려요: 다른 class의 task가 runnable하면 안 돌고, 그런 task가 깨면 즉시 밀려나요 — 모든 algorithm에서. nice와 idle I/O class는 싣지 않아요(simulator는 CPU lane 하나만 schedule해요). 한계 하나가 명시돼 있어요. 그려진 Ubuntu 24.04 데스크톱에서 indexer의 unit은 `background.slice`에서 돌고, slice weight 때문에 editor와 둘 다 runnable일 때 CPU의 약 23 %를 받아요 — idle policy는 같은 CPU group 안에서만 작동하니까요. 그래서 시뮬레이션된 indexer는 실제보다 editor를 덜 방해하고, indexer 파일들(`c1-indexing`, `c2-p1b`, `c7-indexing`)이 보일 수 있는 headroom은 과소평가돼요. backup은 editor와 같은 group(`app.slice` 아래)에서 돌아서 엄격한 class가 데스크톱과 맞아요.

**download의 nice-10 한계.** 측정된 SteamCMD는 CPU의 75 %를 nice 10으로 돌리는데 task model은 nice weight를 싣지 않아요. `game-download`(normal)와 `game-download-idle`(idle)이 그 처리의 양 끝을 감싸고, `c2-p2a`와 `c2-p2a-idle`의 차이가 이 한계가 닿는 범위예요(9.14의 bounding check).

### 4.5 build — `make`와 `dkms`

**`build-orchestrator`** — `make -j8`. linux-6.6 defconfig를 warm으로 빌드한 측정(`meas-ci:build:2026-09-18`, 14 repeat).
```
LOOP { RUN(dispatch_overhead) → FORK ×6 }  → WAIT(children) → EXIT
```
object job마다 dispatch RUN 하나(make 자신의 CPU, 측정 중앙값 676 µs) 뒤에 FORK 여섯. `fork_cap` = `parallelism_cap` × 6: simulator는 살아 있는 task를 세고 job 하나가 멤버 여섯이니, make의 jobserver처럼 job이 cap개까지 동시에 돌아요(cap 8이면 48). `parallelism_cap` 8은 8-thread 데스크톱에 `nproc` 규칙을 적용한 값이에요(design). `binding_params`: `spawn_count`(object job 수), `parallelism_cap`, `child_name`.

**`compiler-child`** — object job 하나는 멤버 여섯: `sh`, `gcc`, `cc1`, `as`, `fixdep`, `rm`, 각자 spawn table의 entry 하나. `sh`가 먼저 돌고, 나머지는 자기 `job:` channel에서 기다리다가 job의 부모-자식 순서대로 깨워져요: sh → gcc → cc1 → gcc → as → gcc → sh → fixdep → sh → rm → sh. 각 멤버의 step CPU는 그 (role, step)의 측정 분위수 표에서 뽑아요(`sh` 4 step, `gcc` 3, 나머지 1). 일을 마친 멤버는 CPU 없이 기다리다가 `sh`가 job을 끝낼 때 같이 `EXIT`해요. 측정된 것은 이 role별 표예요(예: `cc1` step 평균 439.1 ms). 파일별 총합(`c1-compile`의 자식 17,448개 CPU 1,313.9 s)은 그 표에서 뽑은 draw예요.

**`module-build-orchestrator` / `module-compiler-child`** — DKMS의 autoinstall: Ubuntu의 unattended upgrade가 2026-09-23의 보안 kernel(`7.0.0-34-generic`)에 맞춰 NVIDIA 595 open kernel module을 다시 빌드한 측정(`meas-ci:background:2026-10-02`). 측정된 build가 돌린 job 순서 그대로(object job 200, kbuild compiler probe 1,125, NVIDIA conftest test 232) 각 job을 자기 종류의 tree 멤버로 펼치고(`compiler-child`와 같은 방식; `objtool`의 CPU는 `sh`에 접혀요), 자식이 다 끝나면 serial tail을 batch loop로 돌아요. task 이름은 `dkms`, 자식 이름은 `sh`, `mkdir`, `x86_64-linux-gn`(compiler driver의 comm), `cc1`, `as`, `fixdep`, `rm`, `dirname`. `c7-compile`에만 쓰여요.

### 4.6 game chain

**`game-task-chain`** — 게임. 유일하게 topology가 parameter인 archetype이고, 유일하게 우리 측정이 아닌 entry예요. 출처는 `lavd-ossna24`의 slide 12–17이고, 이름 모를 game을 이름 모를 machine에서 `perf sched record`로 본 관찰 하나로 읽어요. CI runner에는 GPU가 없어서 Proton game을 직접 잴 수 없어요.

```
constructor: chain
head:    LOOP { TIMER(frame_period) → RUN → WAKE(다음 멤버) }
member:  LOOP { WAIT(chain:<self>) → RUN(per_schedule_run) → WAKE(다음 멤버) }
```

compile 때 constructor가 멤버 17개를 만들어요. head(`game.chain.1`, task 자신의 이름), 그 바로 뒤의 `game.wineserver`(이름 `wineserver`, RUN = `wineserver_run` 260 µs — slide 13의 coordination task), 그리고 `game.chain.2` … `game.chain.16`(15개, 이름은 timeline의 `member_names`). `chain_length` 16은 slide의 "game-specific task 15–20개" 안에서 고른 점(design)이고, wineserver는 그 수 밖이에요. head만 `TIMER(16667)`을 갖고(frame_period: Steam Deck의 60 Hz 기본 refresh에 맞춘 design, `steamos-refresh`), RUN 뒤 다음 멤버를 `WAKE`해요. 마지막 멤버는 RUN만. frame 하나가 17단을 릴레이로 지나가요. 각 멤버의 RUN은 멤버마다 한 번 뽑아 고정해요(slide 13이 든 두 예, wineserver 260 µs와 task worker 1.65 ms를 p05/p95로 읽은 lognormal). slide는 waker–waiter graph를 fan-in, 2-cycle, wineserver 중심의 hub로 그리는데, 여기서는 그걸 한 줄 relay로 폈어요(우리 linearization).

멤버 이름은 timeline이 `member_names`로 줘요(slide 16이 보여주는 game thread 이름, comm 한도 15자로 잘린 그대로). 지금 gaming 파일 여덟 개가 모두 같은 목록이라 recognizer는 `Troy.exe ×7`(head 포함), `Task worker thr ×4`, `dxvk-cs`, `dxvk-submit`, `winepulse_mainl`, `winepulse_timer`, `FAudio_AudioCli`, `wineserver`를 봐요.

chain 밖의 game thread는 없어요. slide는 game이 도는 동안 system 전체에서 약 300개 task가 schedule된다고 하지만, scheduling의 95 %가 상위 30–40개 task에 있고 그 밖의 task는 설명하지 않아요. 그래서 chain과 `wineserver` 밖의 game thread는 생략해요 — 이 entry의 `modeling_notes`와 gaming timeline들의 header가 그렇게 적어요.

`binding_params`: `lane_share`(5.5절), `member_names`.

### 4.7 session process — 아무도 없는 데스크톱

| archetype | 측정한 것 | 이름 | 싣는 wake |
|---|---|---|---|
| `compositor-shell` | GNOME Shell 46(Mutter와 한 process) | `gnome-shell` | thread component 셋(`JS Helper`, `gmain`, `gnome-shell`), 합쳐서 초당 약 0.59회 |
| `audio-server` | PipeWire stack(`pipewire`, `wireplumber`, `pipewire-pulse`를 task 하나로) | `pipewire` | `wireplumber`의 wake만(초당 약 0.009회). 나머지 둘은 측정 구간에 안 깼어요 |
| `service-manager` | systemd 255(pid 1과 user manager를 task 하나로) | `systemd` | pid 1의 wake만(초당 약 0.07회) |
| `message-bus` | dbus-daemon 1.14(system bus와 session bus를 task 하나로) | `dbus-daemon` | system bus의 wake만(초당 약 0.014회) |

측정은 Ubuntu 24.04 데스크톱 session에서 아무도 없이 idle-delay를 지나 잠기고 화면이 꺼진 상태예요(`meas-ci:session:2026-09-24`). 각자 thread별 component의 wake 빈도와 gap/run 분위수 표만 들고 있어요. 이 넷은 idle 파일 둘(`c1-idle`, `c7-idle`)에만 묶이고, X server task는 없어요(9.9 D26: GNOME 46 Wayland session의 idle에는 `Xorg`도 `Xwayland`도 없음). 다른 파일은 데스크톱의 session process를 생략해요 — runner에서는 그것들의 active 상태를 관찰할 수 없어서예요. 손으로 쓴 모든 timeline의 header와 variant recipe가 그렇게 적어요.

### 4.8 정리표

| archetype | 측정 출처 | program 모양 | lifetime | class | core set에서 쓰이는 이름 | 파일 수 |
|---|---|---|---|---|---|---|
| `office-writer` | `meas-ci:interactive:2026-09-18` | timer component + keystroke | segment-bound | normal | `soffice.bin` | 4 |
| `code-editor` | `meas-ci:interactive:2026-09-25` | timer component + keystroke | segment-bound | normal | `code` | 12 |
| `mail-client` | `meas-ci:interactive:2026-09-19`, `-09-27` | timer component + keystroke + send | segment-bound | normal | `thunderbird-bin` | 6 |
| `web-browser` | `meas-ci:interactive:2026-09-20` | timer component + keystroke + page-load | segment-bound | normal | `chrome` | 10 |
| `image-editor` | `meas-ci:interactive:2026-09-18` | cadence + unsharp mask | segment-bound | normal | `gimp` | 3 |
| `video-editor` | `meas-ci:interactive:2026-09-18`, `-10-05` | timer component + cadence + preview-render | segment-bound | normal | `kdenlive` | 11 |
| `video-player` | `meas-ci:playback:2026-09-18` | TIMER 33,348 µs + cycle RUN | segment-bound | normal | `mpv` (C5·C6에서는 다른 이름) | 6 |
| `audio-player` | `meas-ci:playback:2026-09-18` | TIMER 49,635 µs + cycle RUN | segment-bound | normal | `mpv` (C5·C6에서는 다른 이름) | 6 |
| `video-call` | `meas-ci:playback:2026-09-20` | TIMER 10,001 µs + cycle RUN | segment-bound | normal | `chrome` | 3 |
| `renderer-hidden` | `meas-ci:desktop:2026-10-05b` | timer component | segment-bound | normal | `chrome` | 10 |
| `chat-client` | `meas-ci:desktop:2026-09-20` | timer component | segment-bound | normal | `element-desktop` | 2 |
| `game-client` | `meas-ci:desktop:2026-09-20` | timer component + heavy event | segment-bound | normal | `steam` | 7 |
| `cpu-batch` | `meas-ci:background:2026-10-03`, `-10-03c` | batch loop | finite | normal | `python`, `kdenlive_render`, `chrome`(spoof) | 7 |
| `compiler-child` | `meas-ci:build:2026-09-18` | object job 멤버(WAIT/RUN/WAKE) | spawned | normal | `sh`, `gcc`, `cc1`, `as`, `fixdep`, `rm` | 4 |
| `build-orchestrator` | `meas-ci:build:2026-09-18` | (RUN, FORK ×6)×N, WAIT, EXIT | finite | normal | `make` | 4 |
| `module-build-orchestrator` | `meas-ci:background:2026-10-02` | job 순서대로 FORK, WAIT, tail batch loop, EXIT | finite | normal | `dkms` | 1 |
| `module-compiler-child` | `meas-ci:background:2026-10-02` | job tree 멤버 | spawned | normal | `sh`, `mkdir`, `x86_64-linux-gn`, `cc1`, `as`, `fixdep`, `rm`, `dirname` | 1 |
| `file-archiver` | `meas-ci:background:2026-09-19` | batch loop | finite | normal | `7z` | 1 |
| `game-download` | `meas-ci:background:2026-09-19` | batch loop | finite | normal | `steam` | 1 |
| `game-download-idle` | `meas-ci:background:2026-09-19` | batch loop | finite | idle | `steam` | 1 |
| `package-upgrade` | `meas-ci:background:2026-10-01` | batch loop | finite | normal | `unattended-upgr` | 11 |
| `file-indexer` | `meas-ci:background:2026-10-02b` | batch loop | finite | idle | `tracker-miner-f` | 3 |
| `video-transcoder` | `meas-ci:background:2026-10-03b` | batch loop | finite | normal | `HandBrakeCLI` | 3 |
| `incremental-backup` | `meas-ci:background:2026-10-04` | batch loop | finite | idle | `deja-dup` | 3 |
| `game-task-chain` | `lavd-ossna24` | chain constructor: TIMER head + WAIT/RUN/WAKE 멤버 | segment-bound | normal | `Troy.exe`, `Task worker thr`, `dxvk-cs`, `dxvk-submit`, `winepulse_mainl`, `winepulse_timer`, `FAudio_AudioCli`, `wineserver` | 8 |
| `compositor-shell` | `meas-ci:session:2026-09-24` | timer component | segment-bound | normal | `gnome-shell` | 2 |
| `audio-server` | `meas-ci:session:2026-09-24` | timer component | segment-bound | normal | `pipewire` | 2 |
| `service-manager` | `meas-ci:session:2026-09-24` | timer component | segment-bound | normal | `systemd` | 2 |
| `message-bus` | `meas-ci:session:2026-09-24` | timer component | segment-bound | normal | `dbus-daemon` | 2 |

**lifetime 세 종류:**
- **segment-bound**: 사용자가 닫음. `depart` 시각이 파일에 박혀 있음. `LOOP unbounded`가 허용되는 유일한 종류.
- **finite**: program이 `EXIT`에 도달하면 끝. 언제인지는 scheduler에 달림. `depart` 없음.
- **spawned**: `FORK`로 태어나 `EXIT`으로 끝남.

**program이 먼저 바닥나지 않아요**(9.23). segment-bound task의 program은 depart 순간에 막혀 있는 상태로 끝나요: wake로 움직이는 program은 마지막 wake 뒤에 그 wake의 channel에서 WAIT 하나를 더 해요(wake N개에 WAIT N + 1개; 측정된 interactive task는 마지막 wake가 대개 timer component라 `timer:<id>`에서). timer로 움직이는 program은 depart 이후의 다음 tick을 기다리는 TIMER로, chain 멤버는 unbounded LOOP로 끝나요. 그리고 depart가 task를 치워요. depart가 없는 task는 top-level이든 spawned든 `EXIT`로 끝나요. canonical lint가 이걸 검사해요.

---

## 5. compile — timeline이 workload가 되기까지

`make dataset`이 하는 일: `tools/derive.py`가 recipe에서 파생 timeline을 다시 쓰고, `tools/compile.py`가 51개 timeline을 compile해서 `build/coreset-single/`와 `dataset/build.manifest.json`을 다시 써요. compiler는 `dataset/tools/wlc/`. task 하나는 entry에 따라 다섯 길 중 하나로 compile돼요: chain constructor, module build, 측정된 entry(시간순 stream), fork loop(`build-orchestrator`), batch loop. 어느 길에도 안 맞는 entry는 거부돼요.

### 5.1 seed와 sampling

timeline의 `meta.seed`(예: `c2-p1a`는 201)가 모든 draw를 결정해요. 같은 timeline + 같은 `archetypes.yaml` + 같은 stimulus·launch stream + 같은 seed → byte-identical 출력. draw는 모두 (seed, task id, parameter 이름, index)로 key된 substream이라, 파생 파일이 base의 seed를 물려받으면 바꾸지 않은 task는 byte 단위로 같아요.

`build/`는 commit하지 않아요. `make dataset variants generated`가 다시 compile하고 manifest를 다시 써요. `make check`는 다시 compile하지 않고 비교만 해요: derive drift(파생 timeline과 coverage grid의 32 cell)를 확인하고, `dataset/tools/check_build.py`가 `build/`를 모든 manifest의 합집합에, 각 manifest와 모든 파생 timeline과 `coverage-grid.json`을 HEAD에 commit된 byte에 맞춰 봐요.

sampling 단위 세 가지:
- **per-task**: task당 한 번 draw, 모든 iteration에 재사용. 예: chain 멤버의 RUN, playback의 period.
- **per-iteration**: iteration마다 다른 값. 예: timer component의 간격과 RUN, keystroke의 `input_run`, playback의 cycle run, batch loop의 run과 block.
- **per-instance**: spawn table의 entry마다. 예: object job 멤버의 step CPU.

### 5.2 측정된 entry의 compile (stream 재생)

```
for each timer component c of the entry:              # 측정된 thread 하나
    t = 도착 + (이미 돌고 있던 stream의 첫 간격)
    while t < depart:
        emit (t, RUN ~ c.run, timer)                  # input window 안에서는 focus_components가 대신
        t += 간격 ~ c.gap
for each input window w of this task:                 # keystroke
    offset = seed로 뽑은 stimulus stream 위의 위치    # slice_of면 base window의 offset + 앞부분 길이
    for each key event e in stream[offset, offset + w의 길이):
        emit (w.from + (e − offset), RUN ~ input_run, input)
for each operation o of this task:
    [o.at, o.at + 길이 ~ o.duration) 동안 operation의 component가 다른 wake를 대신
시간순으로 합쳐서 → WAIT(timer:<id>) 또는 WAIT(input:<id>), RUN(run), …, 마지막에 WAIT 하나 더
run file에는 wake마다 `wake` event
```

`c1-office`의 `writer`: input 2–58 s → keystroke wake 270개(첫 keystroke 2.059 s) + timer wake 205개, RUN 합 1.36 s.

측정된 keystroke stream은 네 앱에만 있어요(`dataset/stimulus/`): Writer와 VS Code는 SWELL-KW의 Word stream, Thunderbird는 Outlook stream, Chrome은 Internet Explorer stream. Kdenlive와 GIMP는 keystroke stream이 없어요 — 측정된 driven phase는 pointer로 움직이는 operation이고, 그게 앱 자신의 timer component로 실려요. 그래서 이 둘이 묶인 파일 열세 개(`c1-video-edit`, `c1-render`, `c1-transcode`, `c1-backup`, `c1-photo`, `c2-p3a`, `c2-p3b`, `c3-creation`, `c7-video-edit`, `c7-render`, `c7-transcode`, `c7-backup`, `c7-photo`)의 interaction term 열네 개는 `channel: timer`로 앱 자신의 wake가 기다린 시간을 읽어요(9.14). input window가 없는 측정 task는 timer component만 있어요(`c1-office`의 `browser`).

### 5.3 finite job의 compile (batch loop)

batch loop는 `total_work`를 다 쓸 때까지 run과 block을 뽑아 펼쳐요(4.4절). 예:
- `c2-p1a`의 `python`: RUN 28개 / SLEEP 27개로 1,389.885 s. 측정된 training은 자발적 block 사이를 평균 69.49 s(±27.3 %) 달려서 RUN 하나가 수십 초예요.
- `c2-p2a`의 download: RUN 211,121개 / SLEEP 211,120개로 727.170 s.
- `c1-indexing`의 indexer: RUN 19,070개 / SLEEP 19,069개로 39.435 s.
- `c4-office`의 7z: RUN 하나 6 s(7-Zip의 block은 측정에서 모든 분위수가 0이라 run이 하나로 합쳐져요).
- `c6-spoof`의 가짜 chrome: RUN 하나 30 s(구성상).

모두 마지막이 `EXIT`예요.

### 5.4 spawn table

`build-orchestrator`는 object job `spawn_count`개의 멤버 program을 미리 다 만들어 `spawn_table`에 넣어요. 자식 id는 `build.j1.sh`, `build.j1.gcc`, …, `build.j2908.rm`처럼 job 번호와 role. 부모 program은 job마다 dispatch RUN 하나와 FORK 여섯, 마지막에 `WAIT(children:build)`와 `EXIT`. `fork_cap`도 event에 실려요. 어떤 자식이 무슨 일을 하는지는 compile 시점, 언제 태어나는지는 run 시점.

`c1-compile`: object job 2,908개 × 멤버 여섯 = spawn table 17,448 entry, `fork_cap` 48.

job의 멤버들은 서로를 `WAKE`해요(spawn된 자식이 자식을 깨움). format이 허용하는 쓰임이고 canonical lint가 모든 spawned WAKE target이 resolve되는지 검사해요. reference simulator의 loader는 아직 spawn-table 자식을 target으로 하는 WAKE를 거부해요(12장).

### 5.5 chain constructor와 lane scaling

`game-task-chain`은 constructor가 멤버 17개를 만들고(4.6절), 그 RUN 값을 scale해요.

```
factor = lane_share × 16667 / Σ(17개 멤버의 RUN)
각 멤버 RUN ← round(RUN × factor)
```

즉 한 frame(16.667 ms) 동안 chain 멤버 17개가 합쳐서 정확히 `lane_share` × 16.667 ms를 일하도록. `c1-gaming`(`lane_share: 0.9`)의 멤버 RUN은 286 µs–1.44 ms이고 합이 14,999 µs예요. `lane_share`가 0.9면 chain이 lane의 90 %를 요구해요. 이게 lane scaling의 전부예요. 다른 archetype은 scale 안 해요(측정된 RUN은 그 CPU에서의 intrinsic demand예요).

`lane_share`는 파일마다 timeline이 주는 design 값이에요(`source: design`): `c1-gaming`·`c4-gaming`·`c7-gaming` 0.9, `c2-p2a`·`c2-p2a-idle`·`c2-p2b` 0.95, `c3-evening` 1.45(chain이 혼자서도 frame을 못 맞추도록), `c6-dual` 0.6. slide의 집중도 통계(상위 30–40 task가 scheduling의 95 %, game-specific 15–20 task가 60–70 %)는 scheduling 횟수의 비율이고, slide는 그 통계를 낸 machine을 말하지 않아요. chain의 frame당 demand를 lane의 `lane_share`로 맞추는 건 출처의 숫자가 아니라 우리 calibration이에요.

### 5.6 compile mode는 하나

compiler는 `single` mode 하나만 알아요(`dataset/tools/wlc/compiler.py`의 `MODES = ("single",)`; 다른 mode를 요청하면 거부해요). 그래서 dataset이 내는 set도 lane-scaled `coreset-single` 하나이고, 모든 실험이 그걸로 돌아요. `build/coreset-single/`에는 51개 외에 RQ0 gate spec의 sensitivity variant 78개(`<base>@<set>.workload.json`, 정의는 `dataset/variants.yaml`, pin은 `dataset/build.variants.manifest.json`)도 같이 있어요.

---

## 6. canonical workload file의 해부

simulator와 harness가 읽는 유일한 형식. `dataset/build/coreset-single/<id>.workload.json`. top-level key 넷: `meta`, `ground_truth`, `focus`, `events`. 모든 시각은 정수 µs.

### 6.1 `meta`

```jsonc
"meta": {
  "id": "c2-p1a",
  "derived_from": "dataset/timelines/coreset/c2-p1a.timeline.yaml@a0effee9…",
  "sampled": { "archetypes": "archetypes.yaml@818b41b8…", "seed": 201 }
}
```

어느 timeline의 어느 git blob에서, 어느 archetype library의 어느 git blob에서, 어느 seed로. blob은 파일 내용의 hash라 timeline의 주석 한 줄만 바꿔도 달라지고, 그러면 artifact도 manifest도 달라져요. 모든 숫자의 출처가 여기서 추적돼요.

### 6.2 `ground_truth`

```jsonc
"ground_truth": [
  { "t_start": 0,        "t_end": 60000000, "mode": "dev",      "attributes": { "background_wanted": true } },
  { "t_start": 60000000, "t_end": 99435000, "mode": "ml-train", "attributes": { "background_wanted": true } }
]
```

label이 붙은 segment 목록. core set 51개에 segment가 모두 67개예요. `mode`는 16개 중 하나(또는 `ambiguous`), `attributes.background_wanted`는 boolean. 그 외 `background`, `initiated`(`user` / `scheduled` / `session`), `dual_active`, `spoof`, `pre_committed_miss`(`attributes` 안)와 `familiarity`(segment 자체의 key, author가 적었을 때만) 같은 것은 채점 split과 실패 분석용 annotation이고 recognizer의 답에는 없어요.

**마지막 segment의 `t_end`가 harness의 `T_end`예요.**

### 6.3 `focus`

```jsonc
"focus": [ { "t_start": 0, "t_end": 99435000, "task": "editor" } ]
```

어느 top-level task가 창 focus를 가졌나. simulator는 안 읽고(run file에서 빠져요), recognizer가 visible projection으로 봐요(7장). constructor가 만든 task는 task의 이름을 단 첫 멤버가 focus를 받아요(game chain이면 head `game.chain.1`).

### 6.4 `events`

op는 딱 둘. `arrive`와 `wake`.

```jsonc
// segment-bound 측정 task: depart 있음. timer component와 keystroke가 stream 하나 (c2-p1a)
{ "op": "arrive", "t": 0, "id": "editor", "name": "code", "declared_class": "normal", "depart": 99435000,
  "program": [ { "op": "WAIT", "channel": "timer:editor" }, { "op": "RUN", "us": 22 },
               /* … */
               { "op": "WAIT", "channel": "input:editor" }, { "op": "RUN", "us": 177008 },
               /* … wake 11,344개 */
               { "op": "WAIT", "channel": "timer:editor" } ] }

// finite batch task: depart 없음 (c2-p1a)
{ "op": "arrive", "t": 60000000, "id": "hog", "name": "python", "declared_class": "normal",
  "program": [ { "op": "RUN", "us": 192 }, { "op": "SLEEP", "us": 378 }, /* … */
               { "op": "RUN", "us": 6407092 }, { "op": "EXIT" } ] }

// orchestrator: spawn_table과 fork_cap (c1-compile)
{ "op": "arrive", "t": 2000000, "id": "build", "name": "make", "declared_class": "normal", "fork_cap": 48,
  "program": [ { "op": "RUN", "us": 229 }, { "op": "FORK" }, /* FORK 여섯 */
               { "op": "RUN", "us": 1564 }, /* … job 2,908개 */
               { "op": "WAIT", "channel": "children:build" }, { "op": "EXIT" } ],
  "spawn_table": [ { "id": "build.j1.sh", "name": "sh", "declared_class": "normal",
                     "program": [ { "op": "RUN", "us": 848 }, { "op": "WAKE", "target": "build.j1.gcc" },
                                  { "op": "WAIT", "channel": "job:build.j1.sh" }, /* … */ { "op": "EXIT" } ] },
                   { "id": "build.j1.gcc", "name": "gcc", /* … */ },
                   /* … 17,448개 */ ] }

// periodic: cycle마다 TIMER, RUN (c1-media)
{ "op": "arrive", "t": 0, "id": "video", "name": "mpv", "declared_class": "normal", "depart": 60000000,
  "program": [ { "op": "TIMER", "period_us": 33348 }, { "op": "RUN", "us": 3814 },
               { "op": "TIMER", "period_us": 33348 }, { "op": "RUN", "us": 3014 }, /* … */
               { "op": "TIMER", "period_us": 33348 } ] }

// chain 멤버: LOOP unbounded (c1-gaming의 head)
{ "op": "arrive", "t": 0, "id": "game.chain.1", "name": "Troy.exe", "declared_class": "normal", "depart": 60000000,
  "program": [ { "op": "LOOP", "count": "unbounded",
                 "body": [ { "op": "TIMER", "period_us": 16667 }, { "op": "RUN", "us": 631 },
                           { "op": "WAKE", "target": "game.wineserver" } ] } ] }

// 외부 자극: keystroke, 또는 timer component의 wake
{ "op": "wake", "t": 2090485, "channel": "input:editor", "target": "editor" }
{ "op": "wake", "t": 2469,    "channel": "timer:editor", "target": "editor" }
```

`arrive`의 `id`는 harness의 records에서 `entity`가 돼요. `name`은 recognizer가 보는 것. 같은 이름의 task가 여럿이면 id로 구분해요(`renderers.1` … `renderers.4`는 전부 `name: chrome`). 모든 task record(arrive와 spawn-table entry)는 `declared_class`를 가져요. operation은 event op가 아니에요 — task의 WAIT/RUN stream 안에 compile되고, 시각과 길이는 compile report에 있어요.

---

## 7. recognizer가 보는 것 — telemetry snapshot과 query point

daemon은 visible projection에서 **pinned event**(등장, `depart`가 있는 퇴장, 그리고 focus interval의 시작과 끝)만 시간순으로 걸으면서 "살아 있는 이름의 multiset + focus holder의 이름"을 유지해요. 그 집합이 바뀔 때마다 snapshot 하나 = **query point** 하나. recognizer는 그때만 호출돼요. 중간에는 아무것도 안 물어요. visible projection에는 task마다 `declared_class`도 실려요(`/proc`의 이름처럼 실제 machine에서 공개된 사실). snapshot 자체는 이름 multiset과 focus holder예요.

규칙 몇 가지:
- 개수 변화도 변화예요. `chrome ×5`가 `×6`이 되면 snapshot이 나와요(`c6-spoof`의 spoof와 `c6-fold`의 통화가 이걸로 query point를 만들어요).
- 같은 시각의 event는 전부 적용한 뒤 snapshot 하나.
- finite task는 `depart`가 없으니 **끝나도 telemetry에서 안 사라져요.** recognizer는 batch job이 끝난 걸 몰라요.
- spawn 자식은 부모가 나타날 때 같이 보여요. 언제 태어나는지는 emergent라 알 수 없으니 부모의 lifetime에 붙여요. `c1-compile`의 `make`가 오면 `sh ×2908, gcc ×2908, cc1 ×2908, as ×2908, fixdep ×2908, rm ×2908`이 같이 보여요.
- 마지막 순간(모든 segment-bound task가 떠남)의 snapshot도 나와요. 하지만 그 뒤에는 채점할 segment가 없으니 채점에서 빠져요.
- **focus holder**(2026-10-11, 9.17): snapshot에 `focus: "code"`처럼 focus를 가진 process의 **이름**이 실려요(아무 창도 없으면 `null`). focus가 다른 이름으로 옮겨가면 set change라 snapshot이 나오고, 같은 이름의 다른 instance(chrome tab A → B)로 옮겨가는 건 아무것도 바꾸지 않아요. daemon은 두 **telemetry shape** 중 하나로 보여줘요: `focus`(위 모양) 또는 `names`(`focus` field 없음). query point는 두 shape에서 같아요 — `names`에서는 focus만 바뀐 순간에 직전과 똑같은 snapshot이 다시 나가요. 두 shape의 차이가 이 field의 측정된 가치예요.

`c2-p1a`의 query point 셋:

| t | 보이는 것 | focus | 채점 |
|---|---|---|---|
| 0 s | `code ×1` | `code` | `dev`, wanted |
| 60 s | `code ×1, python ×1` | `code` | `ml-train`, wanted |
| 99.435 s | `python ×1` | `null` | (terminal, 채점 안 함) |

recognizer는 두 번 답해요. 그 답이 config schedule의 두 entry(+ boot entry)가 되고, recognition log의 두 query가 돼요. 10장의 파일별 설명에 각 파일의 query point를 적어뒀어요.

---

## 8. demand와 utilization — 의자를 얼마나 요구하나

compiler는 파일마다 static demand estimate를 내요.

```
utilization = Σ(모든 task의 CPU demand) / 파일 길이
```

task의 demand: 측정 task는 RUN의 합, batch job은 `total_work`, chain 멤버는 (RUN / frame) × 살아 있는 시간, orchestrator는 dispatch RUN과 자식 전부(`dkms`는 tail까지). segment별 utilization은 각 task의 demand를 그 task의 lifetime(도착부터 pinned depart까지, depart가 없으면 파일 끝까지)에 고르게 펴서 segment 안에 떨어지는 몫을 더한 거예요(`dataset/tools/wlc/estimate.py`). 1.0이면 그 구간 동안 lane을 100 % 요구한다는 뜻. 1.2면 120 %: 어떻게 해도 누군가는 기다려요. scheduling 차이는 이렇게 의자가 모자란 구간에서만 생겨요. 의자가 남으면 scheduler가 뭘 하든 차이가 안 나니까요 — 그래서 utilization이 낮은 C1의 interactive·periodic 파일은 recognition 쪽 재료이고 RQ0에서는 reporting-only예요.

**demand는 report될 뿐 규칙이 아니에요.** compiler는 파일별·segment별 utilization을 `dataset/build.manifest.json`의 `demand`(와 compile report)에 적고, 그걸로 어떤 파일도 실패시키지 않아요. lint도 검사하지 않아요. 9.10이 모든 job을 측정된 그대로 통째로 묶으니 파일의 demand는 측정에서 따라 나와요. 어떤 범위 안에 붙잡으려면 측정된 길이를 구부려야 하니, demand는 붙잡지 않고 파일별·segment별로 report하고 pair review가 다툼이 있는 segment를 읽어요(2026-10-09, 9.14). timeline의 `meta.demand` class(`oversubscribed` 또는 `calibration`, 없으면 `oversubscribed`)는 design의 이름표일 뿐이에요: C1, C4, C5, C7과 `c6-alias`·`c6-fold`·`c6-spoof`는 `calibration`(파생 파일은 recipe의 `patch-meta`로 명시), C2, C3, `c6-dual`은 `oversubscribed`. 파일의 실제 regime은 manifest의 utilization으로 읽어요.

**정적 추정의 caveat.** job이 파일보다 오래 살면 job 전체의 `total_work`가 파일 끝까지의 lifetime에 펴져요. `c2-p1a`(training 1,389.885 s가 60 s부터 99.435 s까지 펴짐 → segment 1에서 35.7721)와 `c2-p2a`·`c2-p2a-idle`(download 727.170 s가 60 s부터 86.385 s까지 → 28.5251)의 큰 숫자는 오류가 아니지만, oversubscription의 크기로 읽으면 안 돼요.

core set 51개(`dataset/build.manifest.json`의 `demand`):

| 파일 | utilization | segment별 | class | 비고 |
|---|---|---|---|---|
| c1-backup | 0.9897 | | calibration | editor + idle-class backup |
| c1-browsing | 0.0164 | | calibration | |
| c1-compile | 0.9982 | | calibration | build가 파일 대부분을 채움 |
| c1-dev | 0.3319 | | calibration | editor 혼자 |
| c1-gaming | 0.9153 | | calibration | chain 0.9 + steam |
| c1-idle | 0.0004 | | calibration | 사실상 0 |
| c1-indexing | 0.7477 | | calibration | |
| c1-mail | 0.0287 | | calibration | |
| c1-media | 0.128 | | calibration | video 0.121 + music 0.007 |
| c1-meeting | 0.2387 | | calibration | 통화 하나 |
| c1-ml-train | 0.9982 | | calibration | |
| c1-office | 0.027 | | calibration | |
| c1-photo | 0.0442 | | calibration | |
| c1-render | 0.7339 | | calibration | |
| c1-transcode | 0.9993 | | calibration | |
| c1-video-edit | 0.4586 | | calibration | |
| c2-p1a | 14.505 | 0.5272 / 35.7721 | oversubscribed | caveat: training이 파일보다 오래 삶 |
| c2-p1b | 0.9238 | 0.5272 / 1.5272 | oversubscribed | |
| c2-p2a | 9.3829 | 0.9651 / 28.5251 | oversubscribed | caveat: download가 파일보다 오래 삶 |
| c2-p2a-idle | 9.3829 | 0.9651 / 28.5251 | oversubscribed | 같은 caveat |
| c2-p2b | 1.2706 | 0.9651 / 1.9651 | oversubscribed | chain 0.95 + upgrade |
| c2-p3a | 0.4401 | 0.3893 / 0.4515 | oversubscribed | |
| c2-p3b | 0.8975 | 0.3893 / 1.0122 | oversubscribed | |
| c3-creation | 0.9417 | 0.0151 / 0.0169 / 1.0165 | oversubscribed | |
| c3-evening | 0.9006 | 0.0139 / 1.5062 / 0.1327 | oversubscribed | lane_share 1.45 (게임 segment 안에서만) |
| c3-workday | 0.888 | 0.0031 / 0.0053 / 0.9597 / 1.0251 | oversubscribed | |
| c4-compile | 0.9994 | | calibration | c1-compile + 30–60 s의 Chrome |
| c4-gaming | 0.9638 | | calibration | c1-gaming + chat client |
| c4-office | 0.127 | | calibration | c1-office + 7z 6 s |
| c5-t4 | 0.128 | | calibration | = c1-media |
| c5-t5 | 0.128 | | calibration | = c1-media |
| c6-alias | 0.128 | | calibration | = c1-media |
| c6-dual | 0.8388 | | oversubscribed | lane_share 0.6 |
| c6-fold | 0.3144 | 0.0164 / 0.6123 | calibration | 30 s부터 통화 |
| c6-spoof | 0.5164 | 0.0164 / 0.7664 | calibration | 20 s부터 spoof |
| c7-backup | 1.4032 | | calibration | |
| c7-browsing | 1.0268 | | calibration | base + upgrade 1.0 |
| c7-compile | 1.1866 | | calibration | |
| c7-dev | 1.2129 | | calibration | |
| c7-gaming | 1.9149 | | calibration | chain 0.9 + upgrade 1.0 |
| c7-idle | 1.0007 | | calibration | upgrade 혼자 |
| c7-indexing | 1.0937 | | calibration | |
| c7-mail | 1.0545 | | calibration | |
| c7-media | 1.1267 | | calibration | |
| c7-meeting | 1.24 | | calibration | |
| c7-ml-train | 1.1405 | | calibration | |
| c7-office | 1.0251 | | calibration | |
| c7-photo | 1.0967 | | calibration | |
| c7-render | 1.6189 | | calibration | |
| c7-transcode | 1.3727 | | calibration | |
| c7-video-edit | 1.5618 | | calibration | |

주의: utilization은 파일 전체의 평균이에요. segment가 여럿인 파일은 segment별 값을 봐야 해요. `c2-p1b`는 0–60초가 0.53(editor 혼자)이고 60–99.435초가 1.53(indexer의 39.435 s가 그 구간에 꼭 맞게 펴짐)이에요. 흥미로운 구간은 뒤쪽.

---

## 9. 일곱 그룹 C1–C7 — 각 그룹이 답하는 질문

51개 파일은 일곱 그룹이고(segment는 모두 67개), 각 그룹은 하나의 측정을 가능하게 하려고 존재해요. "이 파일이 없으면 깨지는 RQ가 없다"면 그 파일은 없어야 해요.

| 그룹 | 파일 수 | 질문 | 구성 방식 |
|---|---|---|---|
| **C1** single-situation calibration | 16 | 한 가지 명백한 상황을 맞히나. 바닥: 가장 강한 이름 표(`strongest_name_table`)가 만점을 받을 것으로 기대되는 곳 | mode당 하나(16 mode 전부), segment 하나 — 그 mode의 `true` cell |
| **C2** intent pairs | 7 (3쌍 + bounding 하나) | 같은 foreground 옆의 배경 job 하나가 무엇인지(원했나, 누가 시작했나) 읽어서 scheduling을 맞추나. 쌍의 두 job은 행동과 class가 다를 수 있고 맞는 policy가 달라요 | base + 배경 task 하나와 segment 1의 label만 다른 변형; `c2-p2a-idle`은 `c2-p2a`의 bounding check |
| **C3** transition arcs | 3 | 상황이 중간에 바뀌는 모양과 순서가 존재한다는 사례(경계 모두 7개; 통계적 주장 없음). rate 주장은 generated transition grid·return grid·flap-stress set | 3–4 segment |
| **C4** distractor injection | 3 | 무관한 process가 중간에 나타나는 사례. rate 주장은 generated distractor grid(272개) | C1 clone + 30초 주입 1개, label 불변. 원본과 paired |
| **C5** familiarity ladder | 2 | 이름이 낯설어지는 사례(tier 4, 5). rate 주장은 generated familiarity ladder(66개) | `c1-media` + 이름만 교체 |
| **C6** resolution limits | 4 | 이름 기반 recognition이 **설계상** 못 하는 곳. 셋은 미리 약속된 miss | 각각 다름 |
| **C7** attribute counterparts | 16 | 배경 작업이 **원하지 않은 것**일 때 답이 뒤집히나. driver table의 32 cell 전부에 pair를 줌 | mode당 하나, C1 base에서: interactive 10은 base의 처음 26.385 s + unattended upgrade, batch 6은 job을 0 s부터 통째로 두고 label flip(compile은 dkms build로 교체) — 그 mode의 `false` cell |

파생 관계: C4 = C1 + injection, C5 = C1 + rename, C7 = C1 + unwanted job 또는 같은 job의 label flip, C2의 b = a + 배경 task 교체와 segment 1 수정, C6 셋은 `c1-media`나 `c1-browsing` 파생. 진짜 새로 쓴 timeline은 23개(C1 16, C2의 base 3, C3 3, `c6-dual`)이고 나머지 28개는 `*.variant.yaml` recipe 다섯 개로 생성돼요(11장). 파생 파일은 base의 seed를 물려받아서 "변경한 것 외에는 byte-identical"이 보장돼요.

**core set 밖의 짝.** generated layer(1장)가 C3–C5의 rate 주장을 맡아요: C3에는 transition grid(480개 = 16 mode의 순서쌍 240 × 두 form: 경계에서 A의 task가 떠나는 `departs`, A가 남고 focus만 옮기는 `focus`), return grid A → B → A(720개 = 240쌍 × 가운데 segment 60·10·2 s), flap-stress set(24개, hold-time 조정 재료; 간격 5·10·30 s는 GameMode, tuned, systemd-oomd의 debounce 값, 2 s는 design); C4에는 distractor grid(272개: 사용자는 mode A에 머물고 60초에 다른 process set이 도착 — B의 C1 task set 전체(240쌍) 또는 어느 mode에도 속하지 않는 측정된 program 하나); C5에는 familiarity ladder(66개: 16 mode × tier 4·5, 그리고 render와 backup의 job을 tier 3 이름(`melt-7`, `duplicity`)으로; 이름을 바꾸는 범위 — focus를 가진 task의 이름 / 나머지 / 전부 — 를 축으로).

**RQ0에서의 역할**(`harness/experiments/rq0-gate.yaml`; RQ0는 gate 실험: 이 workload에서 configuration이 애초에 중요한가). 파일이 판정(judging)하는 조건은 label이 바뀌는 쌍의 한쪽이고 그 채점 term이 설계상 row 차이를 담는 것이에요. 판정 파일 19개: C2 쌍의 normal-class 쪽(`c2-p1a`, `c2-p2a`, `c2-p2b`, `c2-p3a`), job에 row의 몫이 닿는 batch C1 base 넷(`c1-compile`, `c1-ml-train`, `c1-render`, `c1-transcode`), C7 counterpart 열하나(browsing, office, dev, photo, meeting, gaming, video-edit, compile, ml-train, render, transcode). 나머지 32개는 reporting-only예요: interactive·periodic C1 base, `c1-gaming`(별도 line), idle 쌍, idle-class 일을 가진 여섯 파일(`c1-indexing`, `c7-indexing`, `c2-p1b`, `c1-backup`, `c7-backup`, `c2-p3b`), `c7-mail`, `c7-media`, C3, C4, C5, C6, 그리고 `c2-p2a-idle`. C3–C6는 돌고 보고되지만 Layer 2(scheduling 채점) aggregation에서는 빠져요. 그리고 `pre_committed_miss` segment를 가진 여덟 파일은 Layer 1(recognition 정확도)에서 빠져요(`layer1_exclusions`, 12장).

---

## 10. 51개 파일 상세

각 파일에 대해: 한 문단 이야기, segment, task(compile된 실제 수치), recognizer가 보는 snapshot, harness가 볼 것. 수치는 `coreset-single`에서 읽은 값이에요. "timer wake"는 timer component의 wake, "keystroke"는 `input:` wake의 수예요. `bind`로 묶은 값 옆에는 timeline의 `source`를 괄호로 적어요.

시간 표기: 초. 프로그램 안 숫자: µs 또는 ms.

모든 파일에 공통인 생략 셋:
- 데스크톱의 session process는 idle 파일 둘(`c1-idle`, `c7-idle`) 말고는 생략돼요. runner에서 그것들의 active 상태를 관찰할 수 없어서예요.
- game 파일에서 chain과 `wineserver` 밖의 game thread는 생략돼요(4.6절).
- Steam client는 측정된 상태 그대로예요: 로그아웃, 계정 없음, library 없음, 뒤에 도는 game 없음, `gameoverlayui` 없음.

손으로 쓴 timeline의 header와 recipe의 주석이 이 셋을 적어요. 다만 header는 compile된 파일에 실리지 않으니(`meta`는 `derived_from`, `id`, `sampled`뿐) dataset을 쓰는 사람이 읽는 곳은 이 문서와 `dataset/README.md`예요.

**design으로 정한 크기.** 측정에서 오지 않은 크기는 design이에요(`bind` 값이면 timeline의 `source`가 `design`이라고 적어요). chain의 `lane_share`(`c1-gaming`·`c4-gaming`·`c7-gaming` 0.9, download 쌍과 `c2-p2b` 0.95, `c3-evening` 1.45 — chain이 혼자서도 frame을 못 맞추도록, `c6-dual` 0.6); interactive·periodic 파일의 60 s와 batch 파일의 길이(job 전체가 들어가거나 job이 segment 내내 살아 있는 길이); batch job의 도착 시각(C1 2 s, C2 60 s, `c3-workday` 120 s, `c3-creation` 240 s, `c6-dual` 10 s, C7 0 s); C4의 주입 시각 30 s와 주입한 program의 정체(chat client, 6 s의 7z, Chrome); `c6-spoof`의 spoof(20 s 도착, 30 s짜리 RUN 하나); keystroke window의 위치와 양 끝 2 s 여백(각 파일의 표대로; `c6-dual`은 focus 교대를 따라 아홉); `c6-dual`에서 게임과 build가 같이 있는 것; build의 `parallelism_cap` 8.

---

### C1 — single-situation calibration

#### `c1-office` — 문서 작업

사람이 LibreOffice Writer에 타이핑하고 있고, Chrome 창 하나(탭 다섯)가 뒤에 있고, Thunderbird가 켜져 있어요. 60초.

| segment | mode | attributes |
|---|---|---|
| 0–60 s | office | background_wanted: true |

| id | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| writer | soffice.bin | office-writer | 0 → 60 | input 2–58 s: keystroke 270개(Word stream의 조각) + timer wake 205개, RUN 합 1.36 s |
| browser | chrome | web-browser | 0 → 60 | input 없음: timer wake 2,678개, RUN 합 0.18 s |
| renderers.1–4 | chrome | renderer-hidden | 0 → 60 | timer wake 9–14개씩 (`count: 4`; `[glam, meas-ci:desktop:2026-10-04]`) |
| mail | thunderbird-bin | mail-client | 0 → 60 | input 없음: timer wake 135개, RUN 합 0.08 s |

recognizer: 0 s `chrome ×5, soffice.bin ×1, thunderbird-bin ×1`, focus `soffice.bin` → 정답 office/wanted. 60 s 빈 집합(terminal).

harness: writer의 `ready_wait(cause = wake)`, `channel: input`의 P99 하나. 경쟁 상대는 browser·renderer·mail의 작은 wake뿐이라 대부분 0에 가까울 거예요. utilization 0.027. reporting-only. `harness/tools/tests/fixtures/mock-office`가 이 파일의 축소판이에요(input window 안의 editor, burst 중간에 queued된 keystroke, 한 번도 안 깨는 unfocused task).

#### `c1-browsing` — 웹 브라우징

Chrome 창 하나, 탭 다섯(보이는 page 하나 + 숨은 탭 넷의 renderer). 30초에 page 하나를 load해요. C6의 `c6-spoof`와 `c6-fold`가 여기서 파생돼요. 60초.

| segment | mode | attributes |
|---|---|---|
| 0–60 s | browsing | background_wanted: true |

| id | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| browser | chrome | web-browser | 0 → 60 | input 2–58 s: keystroke 123개(IE stream의 조각) + timer wake 3,679개, page-load 30 s, RUN 합 0.98 s |
| renderers.1–4 | chrome | renderer-hidden | 0 → 60 | timer wake 10–15개씩 (`count: 4`; `[glam, meas-ci:desktop:2026-10-04]`) |

recognizer: 0 s `chrome ×5`, focus `chrome`. 60 s 빈 집합.

harness: browser의 input P99 하나. utilization 0.0164. reporting-only.

#### `c1-compile` — 코드 편집 + 빌드

VS Code에 타이핑하면서 2초에 Linux kernel(defconfig)을 `make -j8`로 통째로 빌드해요. 파일 길이 1,594 s는 build가 어떤 policy에서도 끝나는 가장 작은 정수 초예요.

| segment | mode | attributes |
|---|---|---|
| 0–1594 s | compile | background_wanted: true |

| id | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| editor | code | code-editor | 0 → 1594 | input 2–1592 s: keystroke 2,544개 + timer wake 178,482개, RUN 합 275.3 s |
| build | make | build-orchestrator | 2 → finite | object job 2,908개(`spawn_count`, `meas-ci:build:2026-09-18`), cap 8(`parallelism_cap`, `design`) → `fork_cap` 48. dispatch RUN 2,908개 합 1.98 s |
| build.j1.sh … build.j2908.rm | sh, gcc, cc1, as, fixdep, rm | compiler-child | spawn | 17,448개(job당 여섯; `child_name: cc1`, `meas-ci:build:2026-09-18`), CPU 합 1,313.9 s |

recognizer: 0 s `code`. 2 s `as ×2908, cc1 ×2908, code, fixdep ×2908, gcc ×2908, make, rm ×2908, sh ×2908`(자식은 부모와 함께 보임). 1594 s `make`와 자식들(finite라 안 사라짐).

harness: **양면** 파일. editor의 input P99(weight 1.0)와 `make`의 `turnaround`(= makespan, weight 1.0). editor latency와 makespan이 서로 당기는 trade-off가 scoring 판단 대상. utilization 0.9982. RQ0 판정 파일이에요. `make`의 turnaround는 `WAIT children:build`가 마지막 자식이 끝날 때 완료돼야 읽혀요(3장).

#### `c1-gaming` — 게임

Proton 게임 하나(`Troy.exe`)의 frame chain과 Steam client. input 없음(게임은 keystroke 모델이 아니라 frame 모델). focus는 게임 창. 60초.

| segment | mode | attributes |
|---|---|---|
| 0–60 s | gaming | background_wanted: true |

| id | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| game.chain.1 | Troy.exe | game-task-chain | 0 → 60 | head: TIMER 16667, RUN 631 µs, `game.wineserver`를 WAKE |
| game.wineserver | wineserver | game-task-chain | 0 → 60 | RUN 341 µs, `game.chain.2`를 WAKE |
| game.chain.2–16 | Task worker thr ×4, dxvk-cs, dxvk-submit, winepulse_mainl, winepulse_timer, FAudio_AudioCli, Troy.exe ×6 | game-task-chain | 0 → 60 | 멤버 RUN 286 µs–1.44 ms. 17개 합 14,999 µs = 0.9 × 16,667 (`lane_share: 0.9`, `design`; `member_names`, `lavd-ossna24:s16`) |
| steam | steam | game-client | 0 → 60 | timer wake 18,062개(초당 약 301회), RUN 합 0.92 s |

recognizer: 0 s `FAudio_AudioCli, Task worker thr ×4, Troy.exe ×7, dxvk-cs, dxvk-submit, steam, winepulse_mainl, winepulse_timer, wineserver`, focus `Troy.exe`. 60 s 빈 집합.

harness: chain head의 `job` miss rate 하나. utilization 0.9153: chain 0.9 + steam 약 0.015. judging set에는 안 들어가요(pair가 없어 attribute 변화가 없음). chain의 부하를 family 종류와 따로 읽는 별도 보고 line이에요.

#### `c1-media` — 미디어 재생

mpv 두 개: 하나는 30 fps 동영상, 하나는 음악(audio만). C5 둘과 `c6-alias`가 여기서 파생돼요. 60초.

| segment | mode | attributes |
|---|---|---|
| 0–60 s | media | background_wanted: true |

| id | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| video | mpv | video-player | 0 → 60 | TIMER 33348 × 1,800 cycle, RUN 합 7.25 s (cycle당 약 4 ms) |
| music | mpv | audio-player | 0 → 60 | TIMER 49635 × 1,209 cycle, RUN 합 0.43 s |

recognizer: 0 s `mpv ×2`, focus `mpv`. 60 s 빈 집합.

harness: 두 task의 `job` miss rate(music 1.0, video 0.5 — 오디오 끊김은 바로 들리고 60 Hz의 frame 하나는 자주 안 보인다는 stated assumption). utilization 0.128이라 경쟁이 거의 없고, 측정된 player는 자기 overrun만 놓칠 것으로 예상돼요(headroom 없음). `fixtures/mock-media`가 이 파일의 축소판이에요.

#### `c1-idle` — 아무도 없음

잠긴 데스크톱, session process 넷만. 사람 없음, focus 없음. 60초.

| segment | mode | attributes |
|---|---|---|
| 0–60 s | idle | background_wanted: true |

| id | name | archetype | compile 결과 |
|---|---|---|---|
| shell | gnome-shell | compositor-shell | timer wake 53개, RUN 합 21 ms |
| audio-srv | pipewire | audio-server | wake 없음(측정 빈도 초당 약 0.009회라 60초 안에 안 깸) → `WAIT` 하나 |
| init | systemd | service-manager | timer wake 6개 |
| bus | dbus-daemon | message-bus | wake 없음 → `WAIT` 하나 |

recognizer: 0 s `dbus-daemon, gnome-shell, pipewire, systemd`, focus `null`. 60 s 빈 집합.

harness: **성능 metric 없음**(scoring spec에 entry가 없어요). utilization 0.0004. 이 파일의 역할은 "recognizer가 idle이라고 하나"뿐이에요.

---

#### Phase 7에서 추가된 열 개의 C1 (2026-09-10)

원래 C1은 여섯이었고(위) 나머지 열 mode는 다른 파일의 segment 안에만 있었어요. Phase 7이 mode당 하나씩 채웠어요. task set은 그 mode를 이미 담고 있던 segment에서 가져왔고(파일 header에 출처가 적혀 있어요), `c1-meeting`만 새로 설계했어요 — 다른 파일에 통화 자신의 task set이 없었으니까요. 지금 모양: interactive·periodic mode는 60 s, input 2–58 s. batch job이 있는 mode는 job을 측정된 그대로 통째로 2초에 묶고, 파일 길이는 job이 어떤 policy에서도 끝나는 가장 작은 정수 초이거나(`c1-ml-train`, `c1-transcode`, `c1-backup`), job이 60 s 안에 끝나면 60 s예요(`c1-render`, `c1-indexing`) — 그래야 turnaround term이 끝난 job을 읽어요.

| 파일 | 길이 | task set (compile 결과) | utilization | term |
|---|---|---|---|---|
| `c1-dev` | 60 s | `code`(code-editor) 혼자: keystroke 186 + timer wake 6,456, RUN 합 19.9 s | 0.3319 | editor input P99 |
| `c1-video-edit` | 60 s | `kdenlive`(video-editor) 혼자: keystroke 없음, timer wake 17,232, preview-render 30 s, RUN 합 27.5 s | 0.4586 | editor timer P99 |
| `c1-photo` | 60 s | `gimp`(image-editor) 혼자: timer wake 511, unsharp mask 30 s, RUN 합 2.65 s | 0.0442 | photo-editor timer P99 |
| `c1-mail` | 60 s | `thunderbird-bin`(mail-client) 혼자: keystroke 35(전부 45.9–53.1 s, Outlook stream의 typing 한 덩어리) + timer wake 5,371, send 40 s, RUN 합 1.72 s | 0.0287 | mailer input P99 |
| `c1-meeting` | 60 s | `chrome`(video-call) 하나: 통화 전체가 task 하나, TIMER 10001 × 6,000 cycle, RUN 합 14.3 s | 0.2387 | voice job miss rate |
| `c1-ml-train` | 1,612 s | `code` + `python`(cpu-batch `python3`, 2 s 도착, 1,389.885 s; `meas-ci:background:2026-10-03`) | 0.9982 | editor input P99 + hog turnaround 0.5 |
| `c1-render` | 60 s | `kdenlive` + `kdenlive_render`(cpu-batch, 2 s, 16.545 s; `meas-ci:background:2026-10-03c`), preview-render 30 s; `initiated: user` | 0.7339 | editor timer P99 + bulk turnaround 0.5 |
| `c1-transcode` | 4,762 s | `kdenlive` + `HandBrakeCLI`(video-transcoder, 2 s, 2,970.871 s; `meas-ci:background:2026-10-03b`), preview-render 2,381 s; `initiated: user` | 0.9993 | video-editor timer P99 + batch turnaround 0.5 |
| `c1-indexing` | 60 s | `code` + `tracker-miner-f`(file-indexer, idle class, 2 s, 39.435 s; `meas-ci:background:2026-10-02b`); `initiated: user`, **pre_committed_miss** | 0.7477 | editor input P99 + hog turnaround 1.0 |
| `c1-backup` | 277 s | `kdenlive` + `deja-dup`(incremental-backup, idle class, 2 s, 165.668 s; `meas-ci:background:2026-10-04`), preview-render 138.5 s; `initiated: scheduled` | 0.9897 | editor timer P99 + bulk turnaround 0.25 |

batch 쪽 weight는 그 mode의 다른 파일이 가진 weight를 따랐어요(ml-train·render·transcode 0.5, backup 0.25). `c1-indexing`의 turnaround weight 1.0은 stated assumption이에요 — reindex를 기다리는 사용자를 build를 기다리는 `c1-compile`의 사용자처럼 봐요.

`c1-indexing`은 indexing의 **`true`** cell이에요 — 사용자가 직접 database를 지우고(`tracker3 reset`) 다시 돌린 index. 같은 indexer가 같은 일을 하니 이름·행동으로는 원하지 않은 index(`c2-p1b`, `c7-indexing`)와 구분이 안 되고, label은 의도로만 달라요. 그래서 `pre_committed_miss: true`가 붙어요(12장).

RQ0에서는 batch 넷(`c1-compile`, `c1-ml-train`, `c1-render`, `c1-transcode`)이 판정하고, 나머지 C1은 reporting-only예요(idle-class job을 가진 `c1-indexing`과 `c1-backup`은 어느 row도 배경 job에 닿지 못해서).

---

### C2 — intent pairs

각 pair의 b는 a에서 배경 task 하나와 segment 1의 label만 바꾼 것이에요(recipe `c2-pairs.variant.yaml`). seed를 물려받으니 나머지 task는 byte-identical이고, 결과 차이는 그 변경에 귀속돼요. latency·frame term은 segment 1(60초부터 파일 끝)에 window를 걸고, progress term은 window가 없어요.

#### `c2-p1a` — 개발 + 내가 돌린 training run (★ load-bearing pair의 base)

VS Code에 타이핑하다가 60초에 PyTorch의 기본 MNIST 예제를 CPU에서 학습시키기 시작해요. 실제 학습 run이고(데스크톱 사용자가 MNIST를 학습시킨다고 주장하는 건 아니에요), 사용자가 원한 일.

| segment | mode | attributes |
|---|---|---|
| 0–60 s | dev | background_wanted: true |
| 60–99.435 s | ml-train | background_wanted: true |

| id | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| editor | code | code-editor | 0 → 99.435 | input 2–97.435 s: keystroke 525개 + timer wake 10,819개, RUN 합 52.4 s |
| hog | python | cpu-batch (`program: python3`) | 60 → finite | RUN 28 / SLEEP 27, `total_work` 1,389.885 s (`meas-ci:background:2026-10-03`; program `[pytorch-examples, meas-ci:background:2026-10-03]`) |

recognizer: 0 s `code`. 60 s `code, python`. 99.435 s `python`. focus는 계속 `code`.

harness: editor의 input P99(segment 1, weight 1.0), hog의 `cpu_delivered` progress(weight 0.5). **hog는 파일 안에서 절대 못 끝나요**: 1,389.885 s의 일을 60초에 시작하는데 파일은 39.435 s 뒤에 끝나요. 그래서 `turnaround`는 없고 progress만. utilization 14.505(segment 1에서 35.7721)는 8장의 caveat대로 job 전체를 파일 끝까지 편 값이에요. `fixtures/mock-p1a`가 이 파일의 축소판(60 s의 config switch + latency, `T_end`에 끝나지 않은 batch).

**load-bearing pair.** P1은 recognition 주장을 싣는 쌍이에요 — 원한 training run과 원하지 않은 indexer를 구분하는 것 — 그리고 그 scheduling headroom은 `c2-p1a` 쪽에 있어요. RQ0는 `c2-p1a`를 판정하고 `c2-p1b`는 보고만 해요: indexer의 declared `idle` class를 executor의 엄격한 idle 규칙이 모든 row 아래에 두니, 그쪽은 class가 이미 정해서 어느 row도 움직이지 못하고 headroom이 0이에요.

#### `c2-p1b` — 개발 + 아무도 안 부른 indexer

`c2-p1a`의 hog 자리에 GNOME Tracker가 home을 처음 index하는 측정된 job(`file-indexer`, 이름 `tracker-miner-f`)을 넣고 segment 1을 `indexing`, `background_wanted: false`, `initiated: session`(첫 login의 index)으로 바꿔요. `python3`의 표에 이름만 바꾼 게 아니라 측정된 indexer 자신의 표예요.

| segment | mode | attributes |
|---|---|---|
| 0–60 s | dev | background_wanted: true |
| 60–99.435 s | indexing | **background_wanted: false**, initiated: session |

| 바뀐 task | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| hog | tracker-miner-f | file-indexer (idle) | 60 → finite | RUN 19,330 / SLEEP 19,329, `total_work` 39.435 s (`meas-ci:background:2026-10-02b`) |

recognizer: 60 s `code, tracker-miner-f`. 99.435 s `tracker-miner-f`.

harness: editor의 input P99 하나(원하지 않은 일에는 term이 없어요). reporting-only. utilization 0.9238(segment 1에서 1.5272).

**P1의 두 job은 행동도 class도 달라요.** training 쪽은 thread 하나, 자발적 block 사이 run이 평균 69.49 s(±27.3 %), 기본 policy nice 0. indexer 쪽은 process 다섯, block 사이 1.876 ms, program이 스스로 건 SCHED_IDLE·nice 19·idle I/O class, job 동안 saturation 약 0.66이고, dataset의 indexer는 CPU의 0.844–0.849를 10 ms slice를 넘는 run에서 써요. 맞는 policy가 반대인 두 실제 job이고, 이 쌍은 indexer의 declared class를 이미 존중하는 baseline 위에 recognition이 무엇을 더하나를 물어요. LLM은 `python`과 `tracker-miner-f`의 의미를 알아야 둘을 구분할 수 있어요. 이름 표 condition(`shipped_catalogue`: CachyOS가 ananicy-cpp와 함께 까는 catalogue를 그대로; `strongest_name_table`: 그 catalogue의 설계로 dataset이 아는 software를 다 덮은 rule 목록)은 이름마다 정해진 rule 하나로 답하는데, `tracker-miner-f`라는 이름은 사용자가 시킨 reindex(`c1-indexing`)와 여기서 같아요.

#### `c2-p2a` — 게임 + 내가 시작한 다운로드

게임 중 60초에 다른 게임의 설치를 시작해요. Steam은 게임이 켜지면 대기 중인 download는 멈추지만, 게임 중에 사용자가 새로 시작한 설치는 바로 시작해요(`steam-downloads`; Valve의 steam-for-linux #8821). segment 1은 짝 파일 `c2-p2b`의 upgrade가 측정에서 쓴 CPU 총량 26.385 s만큼 길어요.

| segment | mode | attributes |
|---|---|---|
| 0–60 s | gaming | background_wanted: true |
| 60–86.385 s | gaming | background_wanted: true, background: download, initiated: user |

| id | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| game.chain.1–16, game.wineserver | Troy.exe ×7, Task worker thr ×4, …, wineserver | game-task-chain | 0 → 86.385 | `lane_share: 0.95`(`design`): 멤버 RUN 225 µs–2.13 ms, 합 15,833 µs |
| steam | steam | game-client | 0 → 86.385 | timer wake 26,010개 |
| download | **steam** | game-download | 60 → finite | RUN 211,121 / SLEEP 211,120, `total_work` 727.170 s (`meas-ci:background:2026-09-19`) |

recognizer: 0 s(c1-gaming과 같은 이름들, focus `Troy.exe`). 60 s `… steam ×2 …`(개수 변화가 query point). 86.385 s `steam`.

harness: chain의 `job` miss rate(segment 1, weight 1.0) + download의 progress(weight 0.5). download는 파일이 끝날 때도 돌고 있어요. 측정된 SteamCMD는 거의 쉬지 않고 돌아서 batch class인데, EDF에서는 deadline class인 chain이 lane의 0.95를 가져가 residual이 어떤 cap보다도 작고, boot MLFQ는 boost slice로 더 줘요 — 그래서 progress term은 headroom 없음으로 예상돼요(scoring spec). utilization 9.3829(segment 1에서 28.5251, 8장 caveat). RQ0 판정 파일. download의 nice-10 한계는 `c2-p2a-idle`과의 bounding check가 재요.

#### `c2-p2a-idle` — 같은 파일, download만 idle class

`c2-p2a`에서 download를 `game-download-idle`(같은 표, `declared_class: idle`)로 바꾼 것뿐이에요. seed를 물려받아서 두 compiled 파일은 그 task의 class만 달라요. judging set 밖이고, 9.14의 사전 등록된 bounding check만 이 파일을 읽어요: 두 파일의 차이가 nice-10 한계가 닿는 범위예요(4.4절). scoring은 base와 같은 term이에요. utilization 9.3829.

#### `c2-p2b` — 게임 + 아무도 안 부른 unattended upgrade

`c2-p2a`의 download 자리에 Ubuntu 24.04 기본 unattended upgrade의 install 단계(`package-upgrade`, 이름 `unattended-upgr`)를 넣고 segment 1을 `background_wanted: false, background: package-upgrade`로 바꿔요.

| segment | mode | attributes |
|---|---|---|
| 0–60 s | gaming | background_wanted: true |
| 60–86.385 s | gaming | **background_wanted: false**, background: package-upgrade |

| 바뀐 task | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| download | unattended-upgr | package-upgrade | 60 → finite | RUN 2,012 / SLEEP 2,011, `total_work` 26.385 s (`meas-ci:background:2026-10-01`) |

recognizer: 60 s `…, steam, unattended-upgr, …`. 86.385 s `unattended-upgr`.

harness: chain의 miss rate 하나(upgrade에는 term이 없어요). 같은 것은 "게임 + 배경 job"의 모양이고 다른 것은 job과 wanted 여부. EDF를 쓰는 판정 파일(`c2-p2a`, `c2-p2b`, `c7-gaming`, `c7-meeting`)에서 두 row는 채점 term에서 설계상 비겨요: EDF는 deadline class의 chain이나 통화를 어떤 residual task보다 먼저 돌리니까요. 그래서 그 gap은 EDF 대 뽑힌 algorithm, 곧 mode recognition을 읽어요. utilization 1.2706(segment 1에서 1.9651). RQ0 판정 파일.

#### `c2-p3a` — 영상 편집 + 내가 시작한 export

Kdenlive에서 편집하다가 60초에 Kdenlive 자신의 export(render dialog, 기본 profile)를 걸어요.

| segment | mode | attributes |
|---|---|---|
| 0–60 s | video-edit | background_wanted: true |
| 60–326 s | render | background_wanted: true, initiated: user |

| id | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| editor | kdenlive | video-editor | 0 → 326 | input 2–324 s(keystroke 없음): timer wake 73,890개, preview-render 30 s, RUN 합 126.9 s |
| bulk | kdenlive_render | cpu-batch (`program: kdenlive_render`) | 60 → finite | RUN 318 / SLEEP 317, `total_work` 16.545 s (`meas-ci:background:2026-10-03c`) |

recognizer: 0 s `kdenlive`. 60 s `kdenlive, kdenlive_render`. 326 s `kdenlive_render`.

harness: editor의 timer P99(segment 1, weight 1.0) + bulk의 `turnaround`(weight 0.5). export는 16.5 s의 CPU라 어떤 row에서도 약 99.5 s까지 끝나서, 받은 CPU는 못 움직이고 turnaround는 움직여요. utilization 0.4401(segment 0.3893 / 0.4515). RQ0 판정 파일.

#### `c2-p3b` — 영상 편집 + 예약된 backup

bulk를 Déjà Dup의 예약된 주간 incremental(`incremental-backup`, 이름 `deja-dup`, idle class)로, segment 1을 `backup`, `initiated: scheduled`로 바꿔요. **여기서는 `background_wanted`가 둘 다 true예요.** 이 pair가 구분하는 건 wanted/unwanted가 아니라 mode(`render` vs `backup`)와 "누가 시작했나"예요.

| segment | mode | attributes |
|---|---|---|
| 0–60 s | video-edit | background_wanted: true |
| 60–326 s | backup | background_wanted: true, initiated: scheduled |

| 바뀐 task | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| bulk | deja-dup | incremental-backup (idle) | 60 → finite | RUN 325 / SLEEP 324, `total_work` 165.668 s (`meas-ci:background:2026-10-04`) |

recognizer: 60 s `deja-dup, kdenlive`. 326 s `deja-dup`.

harness: editor의 timer P99 + bulk의 progress(weight 0.25). segment 1의 길이(60–326 s, 두 파일 공통)는 9.10이 공유 lane 위에서 정한 것이에요. idle class(9.13)에서는 backup이 editor가 비운 lane만 받아서(약 162 s) 그 안에 끝나지 못하고 progress로 채점돼요(9.14). base의 export는 약 99.5 s까지 끝나요. idle-class 파일이라 reporting-only. utilization 0.8975(segment 0.3893 / 1.0122).

---

### C3 — transition arcs

상황이 여러 번 바뀌어요. 이 세 arc는 그런 모양과 순서의 전환이 존재한다는 사례예요(경계 모두 7개) — 통계적 주장은 없어요. 전환 인식의 rate 주장(경계에서의 latency와 정확도, 방향 포함, 16 mode의 모든 순서쌍)과 낡은 configuration의 비용은 generated transition grid, return grid, flap-stress set이 맡아요(9장). 순서는 design이에요. 셋 다 `oversubscribed` class이고, term은 task별로 걸리고 focus와 task lifetime이 window를 정해요. 셋 다 reporting-only예요.

#### `c3-workday` — 하루 일과

Chrome 검색 → LibreOffice 글쓰기 → kernel build → Thunderbird 메일. CpsMark+의 협업 workflow가 browsing → office → mail 전환의 존재 근거예요.

| segment | mode | attributes |
|---|---|---|
| 0–60 s | browsing | wanted |
| 60–120 s | office | wanted |
| 120–1485 s | compile | wanted |
| 1485–1545 s | mail | wanted |

| id | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| browser | chrome | web-browser | 0 → 1545 | input 2–58 s: keystroke 7개 + timer wake 67,612개, page-load 30 s, RUN 합 4.74 s |
| renderers.1–4 | chrome | renderer-hidden | 0 → 1545 | timer wake 312–372개씩 |
| writer | soffice.bin | office-writer | 60 → 1545 | launch phase를 재생한 뒤 steady. input 62–118 s: keystroke 139개 + timer wake 5,850개, RUN 합 3.24 s |
| build | make | build-orchestrator | 120 → finite | object job 2,908개(`meas-ci:build:2026-09-18`), cap 8(`design`) → `fork_cap` 48; 자식 17,448개 CPU 합 1,358.0 s |
| mailer | thunderbird-bin | mail-client | 1485 → 1545 | launch phase 재생(파일이 그 안에서 끝나요). input 1487–1543 s: keystroke 60개 + timer wake 17,789개, send 1,525 s |

focus: browser 0–60, writer 60–1485, mailer 1485–1545.

recognizer (5 query point): 0 s `chrome ×5`(focus `chrome`) → 60 s `+soffice.bin`(focus `soffice.bin`) → 120 s `+make`와 자식 여섯 이름 ×2908 → 1485 s `+thunderbird-bin`(focus `thunderbird-bin`) → 1545 s `make`와 자식들(terminal).

harness: browser·writer·mailer 각자의 input P99와 build의 progress(weight 0.5). compile segment는 build가 어떤 policy에서도 끝나는 가장 작은 정수 초(1,485 s)에서 끝나요. 각 segment의 foreground task(browser → writer → mailer)의 대기가 시간에 따라 어떻게 바뀌는지, 그리고 120초 이후 fork storm이 editor를 얼마나 방해하는지가 이 파일의 이야기예요. utilization 0.888(segment 0.0031 / 0.0053 / 0.9597 / 1.0251).

#### `c3-evening` — 저녁

브라우징 → 게임(chat client와 Steam 곁에서) → 미디어 재생.

| segment | mode | attributes |
|---|---|---|
| 0–60 s | browsing | wanted |
| 60–300 s | gaming | wanted |
| 300–420 s | media | wanted |

| id | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| browser | chrome | web-browser | 0 → 60 | input 2–58 s: keystroke 77개 + timer wake 3,636개, page-load 30 s |
| renderers.1–4 | chrome | renderer-hidden | 0 → 60 | timer wake 9–17개씩 |
| game.chain.1–16, game.wineserver | Troy.exe ×7, …, wineserver | game-task-chain | 60 → 300 | **lane_share 1.45**(`design`) → 멤버 RUN 합 24,166 µs per 16.667 ms frame. 혼자서도 못 따라감. 출처에 launch data가 없어 steady로 도착 |
| chat | element-desktop | chat-client | 60 → 300 | launch phase 재생, 메시지 없는 idle. timer wake 12,121개 |
| steam | steam | game-client | 60 → 300 | launch phase 재생. timer wake 91,259개 |
| video | mpv | video-player | 300 → 420 | launch phase를 cycle 격자에 binning. TIMER 33348 × 3,599 cycle |
| music | mpv | audio-player | 300 → 420 | TIMER 49635 × 2,418 cycle |

focus: browser 0–60, 게임 60–300, video 300–420.

recognizer (4): 0 s `chrome ×5` → 60 s `FAudio_AudioCli, Task worker thr ×4, Troy.exe ×7, dxvk-cs, dxvk-submit, element-desktop, steam, winepulse_mainl, winepulse_timer, wineserver`(focus `Troy.exe`) → 300 s `mpv ×2` → 420 s 빈 집합.

harness: 게임 segment의 chain은 lane_share 1.45라 **설계상 frame을 계속 놓쳐요.** backlog 규칙이 실제로 작동하는 파일. utilization은 파일 평균 0.9006이지만 게임 segment 안은 1.5062. 세 segment의 primary metric이 다 달라요(browser latency → frame miss → media job). 참고로 `game.chain.1`은 60초에, `video`와 `music`은 300초에 등장하는 TIMER task예요. TIMER의 t₀는 task가 TIMER를 처음 실행한 시각이고, lint가 TIMER를 첫 명령으로 강제하니 그 task의 도착 시각이에요(3장). lane이 바빠도 그래요: schedule 없이 돌리면 `video`는 300,000,000 µs에 도착해 300,010,000에야 lane을 처음 받지만, 첫 job의 deadline은 300,033,348 = 도착 + 33,348이에요. harness는 t₀를 그 task의 첫 `ready(cause = timer_tick)` line의 시각으로 읽어요. reference simulator는 도착할 때 막힘 없이 소비된 첫 TIMER에 그 line을 아직 내지 않아서(12장), 같은 run(schedule 없이)에서 지금 harness가 읽는 t₀는 도착보다 `game.chain.1`은 한 주기(60,016,667), `video`는 열한 주기(300,366,828), `music`은 아홉 주기(300,446,715) 늦어요. 몇 주기 늦는지는 각 task가 처음 막히는 때에 달려서 설정마다 달라지고, 적어도 한 주기 늦다는 것만 모든 run에서 같아요.

#### `c3-creation` — 창작

GIMP 사진 편집 → Kdenlive 영상 편집 → HandBrake 변환. SYSmark 30의 Advanced Content Creation이 사진 편집 옆의 background encode의 존재 근거예요.

| segment | mode | attributes |
|---|---|---|
| 0–120 s | photo | wanted |
| 120–240 s | video-edit | wanted |
| 240–3212 s | transcode | wanted, initiated: user |

| id | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| photo-editor | gimp | image-editor | 0 → 120 | input 2–118 s(keystroke 없음): timer wake 981개, unsharp mask 30 s, RUN 합 1.81 s |
| video-editor | kdenlive | video-editor | 120 → 3212 | launch phase 재생(240 s settle까지). input 122–238 s: timer wake 34,672개, preview-render 150 s, RUN 합 52.1 s |
| batch | HandBrakeCLI | video-transcoder | 240 → finite | RUN 92 / SLEEP 91, `total_work` 2,970.871 s (`meas-ci:background:2026-10-03b`) |

focus: photo-editor 0–120, video-editor 120–3212.

recognizer (4): 0 s `gimp` → 120 s `kdenlive` → 240 s `HandBrakeCLI, kdenlive` → 3212 s `HandBrakeCLI`.

harness: 240초 이후 kdenlive는 input window가 없어요(사용자가 변환을 걸어놓고 손을 뗌; 창의 focus는 kdenlive에 남아요). transcode segment는 job이 어떤 policy에서도 끝나는 가장 작은 정수 초(3,212 s)에서 끝나요. 그 구간은 editor의 idle wake 말고는 경쟁이 없어서 cap이 거의 안 물어요. term은 두 editor의 timer P99와 batch의 progress(weight 0.5). utilization 0.9417(segment 0.0151 / 0.0169 / 1.0165). 중요한 구간은 오히려 photo → video-edit 전환에서 recognizer가 mode를 갈아타는 것.

---

### C4 — distractor injection

C1 파일의 clone에 무관한 process 하나를 30초에 주입. label은 그대로. 원본과 pair로 비교해서 "답이 흔들렸나"를 봐요. seed는 원본에서 물려받고, term은 base의 것을 그대로 써요(scoring spec의 `base`). 이 셋은 그런 상황이 존재한다는 사례이고 rate 주장은 generated distractor grid가 맡아요. 셋 다 reporting-only예요.

#### `c4-gaming` — 게임 중 chat client 켜짐

`c1-gaming` + 30초에 `element-desktop`(chat-client: Element, 메시지 없는 idle; launch phase를 재생해요). segment의 scenario tag에 S5(게임 곁의 chat 앱)가 더해져요.

| 주입된 task | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| injected-chat | element-desktop | chat-client | 30 → 60 | timer wake 9,115개, RUN 합 2.91 s |

recognizer: 0 s(c1-gaming과 같음) → **30 s `+element-desktop`**(새 query point) → 60 s 빈 집합.

harness: chain의 miss rate. 관심은 30초의 query에서 recognizer가 여전히 gaming/wanted라고 하는가. utilization 0.9638.

#### `c4-office` — 문서 작업 중 압축

`c1-office` + 30초에 `7z`(file-archiver, `total_work` 6 s, `design`). 6 s는 주입의 크기이고, 9.7이 잰 Mahoney set 압축 전체는 CPU 4,882–5,283 s예요.

| 주입된 task | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| injected-burst | 7z | file-archiver | 30 → finite | RUN 6 s 하나(측정된 block이 모두 0이라 run이 하나로 합쳐짐), EXIT |

recognizer: 0 s(c1-office와 같음) → 30 s `+7z` → 60 s `7z`(finite라 남음).

harness: writer의 input P99. 이 파일은 성능 차이도 조금 있어요. 7z가 30초부터 6 s짜리 RUN 하나로 lane을 잡으니 writer의 `ready_wait`가 원본보다 나빠질 수 있어요. C1 원본과의 delta로 봐요. utilization 0.127.

#### `c4-compile` — 빌드 중 Chrome 열림

`c1-compile` + 30초에 Chrome(`web-browser`, input 없음)과 숨은 탭의 renderer 넷이 launch phase부터 열리고 60초에 닫혀요. segment의 scenario tag에 S2(웹 브라우징)가 더해져요.

| 주입된 task | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| injected-browser | chrome | web-browser | 30 → 60 | launch phase 재생 후 timer wake. 합 7,151개, RUN 합 1.69 s |
| injected-renderers.1–4 | chrome | renderer-hidden | 30 → 60 | launch phase 재생. timer wake 365–435개씩 |

recognizer: 0 s `code` → 2 s `+make`와 자식들 → **30 s `+chrome ×5`** → 60 s `chrome ×5` 빠짐 → 1594 s `make`와 자식들.

harness: base의 term(editor input P99, build turnaround). 주입된 것들은 CPU를 조금만 써요. 관심은 30초 query에서 mode가 `compile`에서 `browsing`으로 흔들리는가. utilization 0.9994.

---

### C5 — familiarity ladder

`c1-media`와 **structure, archetype, seed, 숫자가 전부 같고 이름만 달라요.** test suite(`dataset/tools/tests/test_coreset.py`)가 "이름 외 byte-identical"을 강제해요. 성능 숫자는 c1-media와 같아야 하고, 다르면 bug. 이 둘은 recognition 정확도 측정(Layer 1) 쪽 재료예요. authored 파일 둘은 tier 4와 5의 사례이고, tier 4·5의 rate 주장은 generated familiarity ladder가 맡아요(tier 3은 render와 backup의 job 두 cell).

tier 정의:
1. transparent (`chrome`, `code`, `mpv`)
2. semi-opaque (`soffice.bin`, `Troy.exe`, `wineserver`)
3. opaque: 실제 있지만 이름에서 뜻이 안 보임. corpus에서 recall해야 함 (`tracker-miner-f`, `cc1`, `dkms`)
4. nonexistent-compositional: 없는 소프트웨어지만 단어 뜻으로 추론 가능
5. nonexistent-opaque: recall도 추론도 불가

| 파일 | video (mpv 자리) | music (mpv 자리) | familiarity |
|---|---|---|---|
| `c5-t4` | `video-playback-` | `audio-stream-he` | 4 |
| `c5-t5` | `qzvd` | `xkrr` | 5 |

tier 4의 단어 조합 이름은 comm 한도(15자)에서 잘린 그대로예요. segment: 0–60 s media, wanted, `familiarity: N` annotation.

recognizer: 0 s 두 이름(focus는 video 쪽 이름). 60 s 빈 집합.

harness: c1-media의 term 그대로. 두 파일 다 reporting-only, utilization 0.128.

tier 4와 5를 나눈 이유는 "단어 조합으로 추론하는가"와 "아무것도 못 하는가"를 분리하려고. 가장 강한 이름 표(`strongest_name_table`)도 tier 4–5에서는 구조적으로 실패해요(등록할 이름이 없음). 2026-10-12까지 C5에 있던 tier 3 파일 `c5-t3`는 C6의 `c6-alias`가 됐어요.

**familiarity란 무엇인가.** process **이름**이 language model에게 얼마나 알아볼 만한가를 나타내는 등급이에요. 행동과는 무관하고, 오직 이름의 속성이에요. 기준은 사람이 아니라 **corpus**예요 — "model이 학습 데이터에서 이 이름을 봤을 법한가". 그래서 `soffice.bin`은 사람에게는 낯설어도 corpus에는 충분히 있으니 tier 2이고, `video-playback-`는 세상에 없는 이름이지만 단어 뜻으로 추론이 되니 tier 4예요.

**왜 필요한가.** 이름 표가 실패하는 이유는 둘이에요. 하나는 조합(같은 process가 옆에 뭐가 있느냐에 따라 뜻이 다름, C2와 C7이 검사), 다른 하나는 **세상 지식**(등록된 적 없는 소프트웨어는 목록에 없음). 두 번째를 검사하는 게 tier 4–5예요. 이름 표는 거기서 구조적으로 실패하고, model은 tier 4는 읽고 tier 5는 못 읽을 것으로 예측해요. 이 계단 모양이 예측대로 나오는 게 증거예요.

**metric 계산에서 어떻게 쓰이나.** primitive에는 전혀 안 들어가요. **aggregate할 때의 split key**예요. recognition row 하나(이 query에서 mode를 맞췄나)는 정확히 하나의 ground-truth segment에 덮이고, 그 segment의 tier를 grouping label로 물려받아요. 그래서 accuracy를 전체 평균 하나로 내지 않고 "tier 1–2 이름에서 정확도", "tier 3에서", "tier 4에서", "tier 5에서"로 condition마다 따로 내요. `condition`이나 `workload_id`처럼 **묶는 기준**이지 계산하는 숫자가 아니에요. tier를 섞어 평균 내면 위의 계단이 사라져요.

**지금 tier가 어디에 적혀 있나.** 명시적으로는 C5 두 파일의 segment(`familiarity: 4/5`)와 generated familiarity ladder의 파일에만 있어요. compiler는 author가 적은 annotation만 `ground_truth`의 segment key로 실어요 — 안 적었으면 key 자체가 없어요. 그래서 core set에서 compiled `ground_truth`에 `familiarity`가 있는 건 C5 둘뿐이에요. grader는 이 key로 accuracy를 tier별로 묶어요. annotation이 없는 segment의 tier는 coverage-grid tool이 이름표(`dataset/tools/wlc/grid.py`의 `NAME_TIERS`)로 계산하는데, 살아 있는 이름 중 가장 높은 tier를 쓰고 모르는 이름은 tier 5로 쳐요.

---

### C6 — resolution limits

이름 기반 recognition이 **설계상** 못 하는 네 경우. 셋(`c6-alias` 전체, `c6-fold`의 meeting segment, `c6-spoof`의 20–60 s segment)은 미리 약속된 miss(pre-committed miss)예요 — 결과가 나쁠 것을 알고 넣어요. 한계를 주장만 하지 않고 측정하려고. `c6-dual`은 miss가 아니라 정답 자체가 없는 파일이에요. 넷 다 reporting-only예요.

#### `c6-alias` — player가 indexer의 진짜 이름을 달았음

`c1-media`의 두 player가 두 indexer의 실제 이름을 달아요: video는 `baloo_file`(KDE Baloo), music은 `tracker-miner-f`(GNOME Tracker). 다른 program의 진짜 이름이 foreground 전체에 붙은 경우 — `c6-spoof`가 보여주지 않는 한계예요. familiarity tier가 아니에요(이름이 player 자신의 불투명한 이름이 아니라 다른 program의 이름이니까요). 이 이름들에서 `media`에 닿는 recognizer는 없으니 segment 전체가 pre-committed miss예요.

| segment | mode | attributes |
|---|---|---|
| 0–60 s | media | background_wanted: true, spoof: true, **pre_committed_miss: true** |

recognizer: 0 s `baloo_file, tracker-miner-f`(focus `baloo_file`). 60 s 빈 집합.

harness: c1-media의 term 그대로. utilization 0.128.

#### `c6-spoof` — chrome이라는 이름의 광부

`c1-browsing` + 20초에 `chrome`이라는 **이름**의 cpu-batch(`program: spoof`, `total_work` 30 s, 둘 다 `design`). 진짜 Chrome의 task 다섯 사이에 여섯 번째 chrome이 나타나는데 그건 CPU를 다 먹는 batch예요.

| segment | mode | attributes |
|---|---|---|
| 0–20 s | browsing | background_wanted: true |
| 20–60 s | browsing | **background_wanted: false**, spoof: true, **pre_committed_miss: true** |

| 추가된 task | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| spoof | chrome | cpu-batch | 20 → finite | `RUN 30 s, EXIT` |

spoof가 오기 전에는 원하지 않은 일이 없으니 vocabulary의 관례대로 `true`이고, 20초부터는 아무도 안 시킨 지속적인 일이라 `false`예요.

recognizer: 0 s `chrome ×5` → **20 s `chrome ×6`**(개수 변화가 query point) → 60 s `chrome`(spoof는 finite).

harness: 이름만으로는 여섯 번째 chrome이 다른 걸 알 수 없어요. snapshot에 chrome 하나가 늘었다는 것 말고는 아무것도 없으니까요. oracle은 20초부터 browsing/`false`를 읽고 그 row(cap 0.05)를 광부에 걸어요. 이름만 보는 recognizer는 그럴 근거가 없어서 batch를 throttle하지 못하고 browser의 latency가 나빠져요. term은 browser의 input P99. utilization 0.5164(segment 0.0164 / 0.7664). path 기반 검증은 schema 밖(names only 결정).

#### `c6-fold` — process 이름은 그대로인데 상황이 바뀜

`c1-browsing`에서 30초에 브라우저 탭이 화상회의가 돼요. 통화는 브라우저 자신의 이름으로 돌아서 이름은 `{chrome}` 그대로이지만, 통화가 `chrome`을 하나 더해요(`video-call`, launch phase를 cycle 격자에 binning).

| segment | mode | attributes |
|---|---|---|
| 0–30 s | browsing | background_wanted: true |
| 30–60 s | meeting | background_wanted: true, **pre_committed_miss: true** |

| 추가된 task | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| call | chrome | video-call | 30 → 60 | TIMER 10001, 약 3,000 cycle, RUN 합 17.9 s |

recognizer: 0 s `chrome ×5` → **30 s `chrome ×6`** → 60 s 빈 집합. 30초의 개수 변화가 telemetry 규칙 1(개수 변화도 변화)에 따라 query point를 내지만, snapshot에는 통화라고 말하는 것이 없어요. 그래서 meeting segment는 pre-committed miss예요. meeting segment의 scenario tag에는 S3(화상회의) 옆에 S2(웹 브라우징)가 같이 붙어요.

harness: browser의 input P99(c1-browsing의 term). utilization 0.3144(segment 0.0164 / 0.6123). "이름 집합이 같은 모양으로 남으면 상황 변화를 못 본다"는 scope boundary를 숫자로 남기는 파일.

#### `c6-dual` — 둘 다 진짜 foreground

게임을 하면서 동시에 kernel build가 끝나기를 적극적으로 기다리며 editor에서 일하는 상황. oracle조차 label을 못 붙여요. 파일 하나에 segment 하나, 12,072 s — build가 게임이 자기 몫의 lane을 가진 채로 어떤 policy에서도 끝나는 가장 작은 정수 초.

| segment | mode | attributes |
|---|---|---|
| 0–12072 s | **ambiguous** | dual_active: true (background_wanted 없음) |

| id | name | archetype | arrive → depart | compile 결과 |
|---|---|---|---|---|
| game.chain.1–16, game.wineserver | Troy.exe ×7, …, wineserver | game-task-chain | 0 → 12072 | `lane_share: 0.6`(`design`): 멤버 RUN 175 µs–1.07 ms, 합 10,002 µs |
| editor | code | code-editor | 0 → 12072 | input window 9개(686–688 s씩): keystroke 13,751개 + timer wake 1,357,541개, RUN 합 1,518.6 s |
| build | make | build-orchestrator | 10 → finite | object job 2,908개(`meas-ci:build:2026-09-18`), cap 8(`design`) → `fork_cap` 48; 자식 CPU 합 1,361.2 s |

focus는 0초의 editor부터 688 s마다 editor ↔ 게임으로 교대해요(18 interval). 688 s는 working sphere에서 전환하기 전의 평균 연속 구간 11분 28초예요(`gonzalez-chi04`). 규칙적인 교대, editor가 먼저인 것, 첫 window의 2 s 지연은 design이에요. input window는 editor가 focus를 가진 아홉 구간이에요 — 사용자는 앞에 있는 창에 타이핑해요.

recognizer (20): 0 s `code`와 game 이름들(focus `code`) → 10 s `+make`와 자식들 → 688 s부터 focus만 바뀌는 query point 17개(`Troy.exe` ↔ `code`) → 12,072 s `make`와 자식들. 이 17개가 core set에서 유일한 focus-only query point예요.

harness: `ambiguous`는 recognizer의 menu에 없어요. oracle은 이 segment에서 합법적인 답이 없어 처음부터 fallback으로 돌고(fallback share 1; RQ0 gate spec의 guard 예외), Layer 1 grader는 `ambiguous` segment를 채점하지 않아요(`harness/tools/harness/grader.py`). scoring spec에는 chain의 miss rate와 editor의 input P99가 있지만, 파일은 reporting-only이고 Layer 2 aggregation에서 빠져요. 단 oracle이 crash하면 안 되고 valid한 schedule과 log를 내야 해요. utilization 0.8388: focus 교대로 editor의 typing이 window 하나(12,068 s)에서 686–688 s window 아홉으로 바뀌면서 editor의 CPU가 3,460 s에서 1,519 s로 줄어 0.9997에서 내려왔어요.

---

### C7 — attribute counterparts (2026-09-10)

mode마다 하나, `c7-<mode>`는 `c1-<mode>`에서 파생돼요. base가 그 mode의 `true` cell, counterpart가 `false` cell(indexing만 반대: `c1-indexing`이 사용자가 시작한 `true` cell). 이렇게 해서 driver table의 32 cell 전부가 core set 안에 한 쌍씩 있어요 — Phase 6 pair review가 발견한 구멍(false cell 14개가 비어 있었음)을 메운 것.

두 가지 만드는 법:
- **interactive mode 10개**(browsing, office, mail, dev, photo, meeting, gaming, media, video-edit, idle): 원하지 않은 job 하나를 넣어요 — Ubuntu 24.04 기본 unattended upgrade의 install 단계(`package-upgrade`, 이름 `unattended-upgr`). 열 파일 모두 같은 이름이라 열 개의 `false` cell이 mode로만 다르고, tier 1이라 어떤 pair도 familiarity tier가 안 바뀌어요. upgrade는 0초에 측정된 CPU 총량 C = 26.385 s로 통째로 묶여 도착하고, counterpart는 base의 처음 C초예요: segment 하나, base의 모든 task가 C에 떠나니 lane 하나에서 job이 segment의 모든 순간에 어떤 policy에서도 살아 있어요. input window는 base의 2 s 여백을 지켜 2–24.385 s이고, base window의 slice라 keystroke는 base의 그 구간 것 그대로예요. operation은 base에서의 비율 자리에 놓여요: page-load·unsharp mask·preview-render는 13.1925 s(base의 2–58 s 중 30 s), mail의 send는 17.19 s(base의 40 s, 38/56).
- **batch mode 6개**: batch job 자체가 attribute가 판단하는 배경 작업이에요(vocabulary §1의 batch-mode clause). 그래서 counterpart는 "같은 일인데 아무도 안 시킨 것"이고, job을 0초부터 통째로 두고 파일을 base의 처음 C초로 잘라요(C는 job이 segment 내내 살아 있는 길이).
  - `compile`: 사용자의 build 대신 관찰된 DKMS autoinstall — unattended upgrade가 2026-09-23의 보안 kernel에 맞춰 NVIDIA 595 open module을 다시 빌드한 것(`dkms`, module-build-orchestrator; 4.5절). C = 225.458 s(이 seed로 compile된 build의 CPU). 이름이 바뀌니 miss가 아니에요.
  - `indexing`: base와 같은 job(Tracker의 첫 index)을 첫 login의 index(`initiated: session`)로. C = 39.435 s.
  - `ml-train`, `render`, `transcode`, `backup`: 같은 이름, 같은 일에 label만 뒤집어요(`initiated: scheduled`). 배포판이나 vendor가 그런 job을 아무도 안 시켰는데 돌리는 사례를 찾지 못했고(Jellyfin의 transcoder도 process 이름은 그냥 `ffmpeg`), backup의 유일한 unasked job(dpkg의 `dpkg-db-backup`)은 시작한 그 초에 끝나서 backup segment를 채울 수 없어요. 그래서 넷 다 pre-committed miss로 배송해요. C는 각 job의 CPU 총량: 1,389.885 s, 16.545 s, 2,970.871 s, 165.668 s.

| 파일 | base + op | 길이 | mode / attributes | utilization | term | RQ0 |
|---|---|---|---|---|---|---|
| `c7-browsing` | `c1-browsing` + `unattended-upgr` 0 s부터 | 26.385 s | browsing / **false**, background: package-upgrade | 1.0268 | browser input P99 | 판정 |
| `c7-office` | `c1-office` + upgrade | 26.385 s | office / **false**, background: package-upgrade | 1.0251 | writer input P99 | 판정 |
| `c7-mail` | `c1-mail` + upgrade | 26.385 s | mail / **false**, background: package-upgrade | 1.0545 | mailer **timer** P99 (base 없음) | reporting |
| `c7-dev` | `c1-dev` + upgrade | 26.385 s | dev / **false**, background: package-upgrade | 1.2129 | editor input P99 | 판정 |
| `c7-photo` | `c1-photo` + upgrade | 26.385 s | photo / **false**, background: package-upgrade | 1.0967 | photo-editor timer P99 | 판정 |
| `c7-meeting` | `c1-meeting` + upgrade | 26.385 s | meeting / **false**, background: package-upgrade | 1.24 | voice job miss rate | 판정 |
| `c7-gaming` | `c1-gaming` + upgrade | 26.385 s | gaming / **false**, background: package-upgrade | 1.9149 | chain miss rate | 판정 |
| `c7-media` | `c1-media` + upgrade | 26.385 s | media / **false**, background: package-upgrade | 1.1267 | music·video miss rate | reporting |
| `c7-video-edit` | `c1-video-edit` + upgrade | 26.385 s | video-edit / **false**, background: package-upgrade | 1.5618 | editor timer P99 | 판정 |
| `c7-idle` | `c1-idle` + upgrade | 26.385 s | idle / **false**, background: package-upgrade | 1.0007 | — (metric 없음) | reporting |
| `c7-compile` | `make` build → `dkms` module build, 0 s부터 | 225.458 s | compile / **false**, initiated: scheduled | 1.1866 | editor input P99 | 판정 |
| `c7-indexing` | `c1-indexing`의 job을 0 s부터 | 39.435 s | indexing / **false**, initiated: session | 1.0937 | editor input P99 | reporting (idle class) |
| `c7-ml-train` | job 0 s부터, label만 flip | 1,389.885 s | ml-train / **false**, initiated: scheduled, **pre_committed_miss** | 1.1405 | editor input P99 | 판정 |
| `c7-render` | job 0 s부터, label만 flip | 16.545 s | render / **false**, initiated: scheduled, **pre_committed_miss** | 1.6189 | editor timer P99 | 판정 |
| `c7-transcode` | job 0 s부터, label만 flip | 2,970.871 s | transcode / **false**, initiated: scheduled, **pre_committed_miss** | 1.3727 | video-editor timer P99 | 판정 |
| `c7-backup` | job 0 s부터, label만 flip | 165.668 s | backup / **false**, initiated: scheduled, **pre_committed_miss** | 1.4032 | editor timer P99 | reporting (idle class) |

recognizer: interactive counterpart는 0 s에 base의 이름들 + `unattended-upgr`, 26.385 s에 `unattended-upgr`만(finite라 남음). batch counterpart는 0 s에 base의 이름들(`c7-compile`은 `code`, `dkms`와 자식 `sh ×2253, rm ×1644, x86_64-linux-gn ×1557, cc1 ×1557, as ×1412, mkdir ×1125, dirname ×232, fixdep ×200`), 파일 끝에 job만.

**score.** counterpart는 base의 term에서 batch term(turnaround, progress)을 뺀 것을 가져요 — unwanted work carries no term. 주입한 upgrade와 label이 뒤집힌 job에는 term이 없어서 false row의 cap이 자유롭게 작동해요. scoring lint가 `base`와 term이 같은지 검사해요. 예외 하나가 `c7-mail`이에요.

**`c7-mail`.** counterpart의 input window(2–24.385 s)는 `c1-mail`의 2–58 s window의 slice라 base와 같은 stimulus offset을 쓰는데, base의 keystroke 35개(SWELL Outlook stream의 typing 한 덩어리)가 전부 45.9–53.1 s에 있어서 잘린 구간에는 하나도 없어요. 그래서 `c7-mail`은 reporting-only이고, term은 base 없이 mailer 자신의 wake(`channel: timer`)를 읽고, mail 쌍의 attribute는 측정되지 않아요.

**demand.** 전부 recipe에 `demand: calibration`을 선언해요(design의 이름표일 뿐; 8장). interactive counterpart는 base + upgrade의 1 lane이라 대부분 1.0–1.6이고, `c7-gaming`은 1.9149(chain 0.9 + upgrade 1.0)예요.

**`c7-idle`.** 네 session task는 idle session의 측정 상태 그대로이고, upgrade가 그 안에 일으키는 일은 싣지 않아요. 부팅된 데스크톱에서 관찰한 것 — PID 1과 system bus의 추가 일, PID 1의 daemon-reexec가 generator를 돌리는 것, apt의 PackageKit hook이 `packagekitd`를 시작하는 것 — 은 전부 빠져 있어요(recipe 주석).

**측정에서 알아둘 것.** `c7-meeting`은 2026-10-09부터 판정 파일이에요: 측정된 통화는 10 ms audio frame마다 job 하나인 task 하나이고, 그 cycle run이 약 다섯 번에 한 번 boot slice를 다 써서 강등되면 upgrade의 slice 뒤에서 다음 boost까지 기다려요. EDF row에서는 deadline class라 자기 overrun(약 5 %)만 놓쳐요. `c7-media`는 reporting-only예요: 측정된 표에서 video player의 최악 cycle은 33.3 ms 주기에 run 16.0 ms이고, boot MLFQ가 걸 수 있는 가장 긴 대기는 드문 강등 뒤의 Q1 slice 20 ms 하나라 합해서 32 ms예요. fixed 대비로도 두 EDF row 사이에서도 headroom이 없고, 그 margin 1.3 ms가 knife edge로 적혀 있어요(RQ0 gate spec의 note).

---

## 11. 파일들 사이의 관계 — 무엇이 무엇에서 파생됐나

```
c1-office ────────────▶ c4-office     (+7z at 30 s, 6 s)
c1-compile ───────────▶ c4-compile    (+chrome ×5 at 30 s: web-browser + renderer-hidden ×4, 60 s에 닫힘)
c1-gaming ────────────▶ c4-gaming     (+element-desktop at 30 s)
c1-media ─────┬───────▶ c5-t4         (rename → video-playback-, audio-stream-he)
              ├───────▶ c5-t5         (rename → qzvd, xkrr)
              └───────▶ c6-alias      (rename → baloo_file, tracker-miner-f; spoof, pre-committed miss)
c1-browsing ──┬───────▶ c6-spoof      (+chrome cpu-batch at 20 s; segments → 0–20 true, 20–60 false + miss)
              └───────▶ c6-fold       (+chrome video-call at 30 s; segments → browsing 0–30, meeting 30–60 + miss)
c2-p1a ───────────────▶ c2-p1b        (python → tracker-miner-f on file-indexer; seg 1 → indexing, false, session)
c2-p2a ───────┬───────▶ c2-p2b        (download → unattended-upgr on package-upgrade; seg 1 → false)
              └───────▶ c2-p2a-idle   (download → game-download-idle; 그 밖엔 그대로)
c2-p3a ───────────────▶ c2-p3b        (kdenlive_render → deja-dup on incremental-backup; seg 1 → backup, scheduled)
c1-<mode> ×16 ────────▶ c7-<mode>     (interactive 10: 처음 26.385 s + unattended-upgr at 0 s;
                                       compile: make → dkms module build, 처음 225.458 s;
                                       indexing: job 0 s부터, session; ml-train, render, transcode, backup:
                                       job 0 s부터 label만 flip + miss; 전부 wanted → false)
c3-workday, c3-evening, c3-creation, c6-dual: 독립 (파생 없음)
```

recipe는 `dataset/timelines/coreset/*.variant.yaml` 다섯(`c2-pairs`, `c4`, `c5`, `c6`, `c7`). op는 `rename`, `patch-task`, `add-task`, `patch-segment`, `set-segments`, `set-input`, `set-focus`, `set-operations`, `patch-meta`(seed·id는 못 바꿈). 파생 파일은 base의 seed를 물려받아요 — deriver는 seed를 바꾸려는 recipe를 거부해요. 파생 timeline은 commit돼 있고 `derive.py --check`가 drift를 실패로 잡아요.

이 관계가 실험에 주는 것:
- C4는 "원본과의 delta"로만 의미가 있어요.
- C5와 `c6-alias`는 성능이 c1-media와 같아야 하고, 그 자체가 pipeline의 sanity check예요.
- C2의 b는 a와 배경 task 하나와 그 segment의 label만 다르니 gap이 그 변경에 귀속돼요.
- C7은 base와 task 하나(또는 label만) 다르니 attribute의 효과가 그 한 곳에 귀속돼요.

core set 밖의 파생도 있어요: `build/coreset-single/`의 sensitivity variant 78개는 판정 파일들을 변형한 것(`dataset/variants.yaml`)이고, generated layer의 1,562개는 C1 timeline 열여섯에서 만들어요(1장).

---

## 12. 알아둘 특이점과 열린 항목

이 문서를 쓰면서 compiled file에서 직접 확인한 것들이에요.

**행동에 관한 것**
- 측정된 interactive task는 keystroke보다 자기 timer component로 훨씬 많이 깨요(`c1-dev`의 editor: keystroke 186개, timer wake 6,456개). input window가 없는 task도 timer component로 계속 깨요: `c1-office`의 `browser`, `c4-compile`의 `injected-browser`, `c3-creation`의 240초 이후 `kdenlive`.
- Kdenlive와 GIMP에는 keystroke stream이 없어요. 그래서 그 앱의 interaction term은 `channel: timer`예요(13개 파일, term 14개).
- `c1-idle`·`c7-idle`의 `pipewire`와 `dbus-daemon`은 측정된 wake 빈도가 너무 낮아서 파일 안에서 한 번도 안 깨요 — program이 `WAIT` 하나예요.
- C2에서 파일보다 오래 사는 job은 셋이에요: `c2-p1a`의 training(남은 39.435 s에 1,389.885 s의 일), `c2-p2a`·`c2-p2a-idle`의 download(남은 26.385 s에 727.170 s), `c2-p3b`의 backup(idle class라 266 s 안에 못 끝남). 이 셋은 progress(`cpu_delivered / demand`)가 batch 쪽 metric이에요. C7 counterpart의 job도 파일 안에서 못 끝나요: 파일 길이가 job의 CPU 총량과 같고 foreground가 lane을 나눠 쓰니까요 — 그래서 segment 내내 살아 있고, term은 없어요. 나머지 batch job은 파일 안에서 어떤 policy에서도 끝나도록 길이가 잡혀 있어요(C1의 batch base, `c3-workday`, `c3-creation`, `c6-dual`).
- `c3-evening`의 chain은 lane_share 1.45라 혼자서도 frame을 못 맞춰요. backlog가 설계상 발생.
- `c2-p3` pair는 둘 다 `background_wanted: true`. 구분 축은 mode와 `initiated`.
- "행동이 같은" pair는 없어요. P1의 두 job은 행동도 class도 다르고(10장), P2의 두 job은 같은 normal class지만 행동이 달라요: download는 측정된 SteamCMD가 727 s의 CPU를 계속 쓰는 것, upgrade는 단명 process 916개의 사슬이 26.385 s를 쓰는 것.
- `c6-alias`의 이름(`baloo_file`, `tracker-miner-f`)은 실제로는 indexer인데 player처럼 행동해요. 의도된 오도.
- TIMER를 가진 task는 core set에 23개예요: gaming 파일 여덟의 chain head, mpv 열둘(`c1-media`, `c3-evening`, `c5-t4`, `c5-t5`, `c6-alias`, `c7-media`에 둘씩), 통화 셋(`c1-meeting`, `c6-fold`, `c7-meeting`의 `chrome`). 넷은 중간에 등장해요(`c3-evening`의 chain head·`video`·`music`, `c6-fold`의 `call`). Steam, chat client, renderer, editor의 주기적으로 보이는 wake는 TIMER가 아니라 `timer:` channel의 WAIT라 deadline이 없어요.
- core set의 compiled 이름 44개는 네 종류예요. (1) 측정 campaign이 trace에서 본 comm — 대부분이에요(`soffice.bin`, `thunderbird-bin`, `tracker-miner-f`, `unattended-upgr`, training run의 `python` 등). task의 이름은 kernel comm이에요: exec된 basename을 15 byte로 자른 것, script는 자기 이름, prctl로 바꾼 것은 새 이름. (2) game chain의 thread 이름(`lavd-ossna24` slide 16)과 compiler가 붙이는 `wineserver`. (3) tier 4·5의 이름(design). (4) 의도된 spoof(`c6-spoof`의 `chrome`, `c6-alias`의 `baloo_file`, design).

**telemetry에 관한 것**
- finite task는 telemetry에서 안 사라져요. 마지막 snapshot에 `make`와 자식들, `python`, `7z`, `deja-dup`, `unattended-upgr` 같은 것이 남아 있어요.
- `c6-spoof`(20 s)와 `c6-fold`(30 s)는 `chrome ×5 → ×6` 개수 변화로 query point가 생겨요.
- spawn 자식은 부모와 함께 보여요(`make`: 여섯 이름 ×2,908; `dkms`: 여덟 이름, 10장의 C7 참고).
- focus만 바뀌는 query point는 `c6-dual`의 17개뿐이에요.

**reference simulator가 아직 못 하는 것**
- loader가 spawn-table 자식을 target으로 하는 WAKE를 거부해요(`simulator/src/sim.cpp`: "WAKE target is not a top-level task"). object job의 멤버가 서로 깨우니, build가 있는 core 파일 다섯(`c1-compile`, `c7-compile`, `c3-workday`, `c4-compile`, `c6-dual`)을 아직 읽지 못해요. dataset은 이 쓰임을 지키고(canonical lint가 spawned WAKE target이 resolve되는지 검사), 고칠 곳은 simulator예요.
- `WAIT children:<id>`를 마지막 자식이 끝날 때 완료하지 않아요(3장). `c1-compile`의 build turnaround term(판정, weight 1.0)이 읽히려면 필요해요.
- 막을 수 있는 명령(`TIMER`, `WAIT`, `FORK`)이 막히지 않고 끝나도 zero-wait `ready` line을 내지 않아요. 그 자리의 line은 `ready(cause = arrive)`예요(`docs/harness/metrics.md` §11 item 1이 simulator에 남은 일로 적어 둔 것). 도착할 때 소비되는 첫 TIMER도 그래서, harness가 첫 `ready(cause = timer_tick)` line으로 읽는 t₀가 도착보다 주기의 정수배만큼 늦어요(10장 `c3-evening`).

**결정된 것과 남은 것**
- **pre_committed_miss**(2026-09-10): 이름·행동으로는 label에 닿을 수 없는 segment에 붙는 annotation. core set에서 여덟 파일이에요: attribute 쪽 `c1-indexing`, `c7-ml-train`, `c7-render`, `c7-transcode`, `c7-backup`; C6의 `c6-alias`(전체), `c6-fold`(30 s부터의 meeting segment), `c6-spoof`(20 s부터). coverage grid가 이걸 읽어 cell을 "채워졌지만 recognition-limited"로 표시하고, RQ0 gate spec의 `layer1_exclusions`가 이 여덟을 recognition 정확도에서 빼요(lint가 compiled 파일에서 같은 목록을 끌어내 검사해요). 그중 셋(`c7-ml-train`, `c7-render`, `c7-transcode`)은 scheduling 판정에는 들어가요 — gate에 필요한 건 label이지 알아볼 수 있음이 아니니까요.
- familiarity annotation은 C5 둘과 generated familiarity ladder에만 있어요. 나머지 segment의 tier는 coverage grid가 이름표로 계산해요(10장 C5).
- `random` condition은 driver table의 32 row에서 uniform하게 뽑아요(`harness/tools/tests/mocks/daemon.py`).

---

## 13. 용어 정리

| term | 뜻 |
|---|---|
| **workload** | 실험 하나를 완전히 적은 canonical JSON. `meta`, `ground_truth`, `focus`, `events` |
| **run file** | simulator가 읽는 workload의 view: `events`와 id. `ground_truth`와 `focus`는 빠짐 |
| **timeline** | 사람이 쓰는 authoring YAML. compile되어 workload가 됨 |
| **archetype** | process 한 종류의 행동 model. program + parameter 분포(대부분 측정된 분위수 표). 이름 없음 |
| **scenario** | 사용 상황 하나와 그 process 이름들. S1–S18. segment의 근거 tag |
| **segment** | label(mode + attributes)이 붙은 시간 구간. core set에 67개 |
| **mode** | 16개 label 중 하나. machine이 주로 뭘 하고 있나 |
| **`background_wanted`** | 지속적인 배경 작업이 사용자가 원한 것인가. 배경 작업이 없으면 true |
| **`ambiguous`** | ground truth 전용 label. recognizer menu에 없음 |
| **task** | workload의 `arrive` event 하나. id와 name을 가짐 |
| **id / name** | id는 simulator·harness용 고유 식별자(`renderers.3`), name은 recognizer가 보는 것(`chrome`) — kernel comm, 15자까지 |
| **declared class** | program이 자기에게 거는 scheduling class. `normal` 또는 `idle`(indexer, backup, `game-download-idle`). 모든 task record에 실림 |
| **program** | task의 script. 여섯 primitive + LOOP |
| **primitive** | RUN, SLEEP, TIMER, WAIT, WAKE, FORK/EXIT |
| **channel** | WAIT/WAKE가 만나는 이름. `input:<id>`, `timer:<id>`, `chain:<id>`, `job:<id>`, `children:<id>` |
| **wake event** | run file의 외부 자극. keystroke(`input:`) 또는 timer component의 wake(`timer:`) |
| **timer component** | 측정된 앱의 thread 하나가 스스로 깨는 빈도와 간격·RUN의 분위수 표. compile 때 `timer:` wake로 펼쳐짐. TIMER가 아님 |
| **stimulus stream** | SWELL-KW 연구의 실제 typing 기록(`dataset/stimulus/`). input window 안에서 한 조각이 재생됨 |
| **operation** | 측정된 앱이 사용자 지시로 하는 일 하나(page-load, unsharp mask, preview-render, send). timeline의 `operations` track |
| **input** | timeline에서 keystroke가 어느 task로 들어가나. keystroke가 생성되는 window (2026-10-11 전의 이름은 `focus`) |
| **focus** | timeline에서 어느 task의 창이 focus를 갖나. compile된 파일의 `focus` key, projection의 task별 interval, snapshot의 `focus` 이름으로 recognizer에게 보여요 |
| **segment-bound / finite / spawned** | lifetime 세 종류 |
| **depart** | segment-bound task의 pinned 퇴장 시각 |
| **batch loop** | finite job의 compile 모양: 측정된 run과 block을 `total_work`까지 번갈아 |
| **spawn table** | orchestrator가 만들 자식들의 program 목록. compile 시점에 고정 |
| **object job** | make job 하나 = spawn table의 멤버 여섯(`sh`, `gcc`, `cc1`, `as`, `fixdep`, `rm`) |
| **fork_cap** | 동시에 살아 있을 수 있는 자식 수. `parallelism_cap` × 6, `make -j8`이면 48 |
| **chain** | game-task-chain의 frame pipeline. head(TIMER) → wineserver → … → 마지막 멤버, 17개 |
| **lane_share** | chain이 요구하는 lane의 비율(design). chain RUN을 이 값에 맞춰 scale |
| **lane scaling** | `single` compile의 scale pass. game-task-chain에만 적용 |
| **utilization** | Σ CPU demand / 파일 길이. 파일(또는 segment)이 lane을 얼마나 요구하나. manifest에 report됨 |
| **demand class** | `oversubscribed` 또는 `calibration`. design의 이름표일 뿐, 검사하지 않음 |
| **familiarity** | process 이름이 corpus에서 얼마나 알아볼 만한가, 1–5 tier. 이름의 속성, 행동과 무관. recognition accuracy를 묶어서 보고하는 split key. 명시 annotation은 C5 segment와 generated ladder에만 |
| **seed** | timeline의 난수 seed. 모든 draw를 결정 |
| **per-task / per-iteration / per-instance** | sampling 단위 |
| **unroll** | 반복을 compile 때 구체적 값으로 펼치는 것 |
| **variant** | base timeline + op로 파생된 timeline. seed 상속. (RQ0 gate spec의 sensitivity variant는 다른 것: `<base>@<set>`) |
| **coreset-single** | compile된 core set. compile mode는 `single` 하나뿐이고 모든 실험이 이것으로 |
| **generated layer** | C1 task set으로 만든 다섯 set, 1,562개. C3–C5의 rate 주장이 도는 곳 |
| **telemetry snapshot** | 살아 있는 이름의 multiset + focus holder. 바뀔 때마다 하나 |
| **query point** | snapshot이 나온 시각. recognizer가 호출됨 |
| **pinned event** | 시각이 파일에 박힌 event. 등장, depart, wake, focus interval의 경계 |
| **emergent** | scheduler에 따라 달라지는 시각. spawn, exit, 모든 실행 |
| **meas-ci** | 우리 CI 측정 campaign의 source tag(`meas-ci:<workflow>:<run>`) |
| **C1–C7** | coreset의 일곱 그룹 |
| **counterpart (C7)** | 한 mode의 `false` cell을 담는 파일. 그 mode의 C1 base + op 하나 |
| **pre_committed_miss** | 이름·행동으로는 맞힐 수 없는 segment의 annotation. accuracy에서 제외, 따로 보고 |
| **judging set** | RQ0 gate 판정에 쓰는 파일 19개(C2 넷, batch C1 넷, C7 열하나) |
| **Layer 1 / Layer 2** | 평가의 두 층: recognition 정확도 / scheduling 채점 |

---

## 이 문서를 다 읽었으면

- `dataset/README.md`가 tree와 명령을, building-plan이 설계 근거를, archetype-plan이 archetype 규칙을, interpretation contract가 실행 semantics를 갖고 있어요. 이 문서는 그것들의 "왜"와 "실제 숫자"를 이어준 것.
- harness가 이 파일들을 어떻게 읽고 숫자로 바꾸는지는 `docs/harness/harness-and-records-guide.md`.
- 숫자를 직접 보려면 `cd dataset && make dataset PY=python3.12` 후 `build/coreset-single/`(compile report `<id>.report.json` 포함)와 `build.manifest.json`의 `demand`. build는 Python 3.12로 해요.
