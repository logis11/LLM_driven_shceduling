# 2권 · Archetype library: 프로그램 한 종류를 scheduler의 눈으로 적기

> Status: draft · Created 2026-10-14 · Updated 2026-10-30

**`archetypes.yaml`의 29개 항목은 각각 무엇을 어떻게 흉내 내고, 그 숫자들은 어디서 왔나.**

---

이 dataset은 scheduler 실험에 먹일 가짜 desktop 작업을 만듭니다. 만드는 과정은 세 층으로 나뉩니다. 맨 아래층이 이 권의 주제인 **archetype library**(`dataset/archetypes.yaml`)입니다. 여기에는 "이런 종류의 프로그램은 CPU를 이런 모양으로 쓴다"는 행동 규칙과 그 숫자가 들어 있습니다. 그 위층이 **timeline**(`dataset/timelines/coreset/<id>.timeline.yaml`)입니다. timeline은 "이 파일에서는 `soffice.bin`이라는 이름의 task 하나가 0초에 나타나 60초에 사라지고, 그 task는 `office-writer` archetype처럼 행동한다"처럼 이름과 시간과 archetype을 엮습니다. 마지막으로 compiler(`wlc`, `dataset/tools/wlc/`)가 timeline과 library를 읽어, 무작위성을 모두 풀어낸 **workload 파일**(`dataset/build/<set>-single/<id>.workload.json`)을 씁니다. simulator는 이 workload 파일만 읽습니다. archetype은 compile할 때 한 번 읽히고 사라집니다.

그래서 이 dataset에서 "숫자"가 사는 곳은 거의 이 library 하나뿐입니다. `dataset/README.md`의 "Rules of the tree"는 이것을 규칙으로 적어 둡니다. "Behavior parameters live in `archetypes.yaml`, never inline in a timeline" — 행동을 정하는 숫자는 `archetypes.yaml`에만 있고, timeline은 archetype이 허락한 손잡이(`binding_params`)에만 값을 넣습니다. 그러니 "이 workload에서 editor가 key 하나에 CPU를 몇 ms 쓰나", "build는 process를 몇 개 띄우나", "game은 몇 ms마다 깨어나나" 같은 질문의 답은 모두 이 library에서 시작합니다.

지금 library에는 항목이 29개 있습니다(아래 1장 끝에서 shell 명령으로 세어 확인합니다). 그중 28개는 이 repository가 직접 GitHub의 CI runner 위에서 실제 프로그램을 돌려 잰 값을 담습니다. 나머지 하나, `game-task-chain`은 LAVD scheduler 발표 자료에서 숫자를 가져옵니다. 이 상태는 2026-09-13부터 2026-10-18까지 이어진 Phase 9 재건(rebuild)의 결과입니다. 그 전의 library는 문헌과 benchmark에서 숫자를 모아 온 열두 항목이었고, 그 숫자들을 원문과 대조하다 심각한 문제가 발견되어 통째로 다시 만들어졌습니다. 이 권은 그 역사도 다룹니다.

이 권은 다음 순서로 갑니다. 먼저 scheduler가 process에서 무엇을 보는지, 그것을 적는 여섯 개의 primitive가 무엇인지 설명합니다(1장). 다음으로 항목 하나가 어떤 field로 적히는지 실제 항목 하나를 끝까지 따라가며 설명합니다(2장). 숫자를 어떻게 쟀는지는 tag를 읽을 수 있을 만큼만 설명하고, 방법과 검증 기준의 자세한 내용은 측정 방법을 다루는 6권에 넘깁니다(3장). 그다음 29개 항목을 만든 연구 slice(Phase 9가 영역별로 나눈 연구·결정 단위, 4장 첫머리에서 설명)별로 하나씩 봅니다(4장–10장). 끝으로 library가 예전에 어땠는지, 왜 다시 만들었는지(11장), 기록이 스스로 밝히는 한계(12장)를 정리하고, 용어 정리(13장)로 마칩니다. timeline이 archetype을 어떻게 묶는지와 compiler가 workload를 어떻게 쓰는지는 timeline과 compile을 다루는 권에서 자세히 다룹니다. 이 권에서는 archetype을 이해하는 데 필요한 만큼만 다룹니다.

---

## 목차

1. [1장 · scheduler가 보는 process](#1장--scheduler가-보는-process)
2. [2장 · 항목 하나는 어떻게 적혀 있나](#2장--항목-하나는-어떻게-적혀-있나)
3. [3장 · 숫자는 어떻게 얻었나 — tag를 읽을 만큼만](#3장--숫자는-어떻게-얻었나--tag를-읽을-만큼만)
4. [4장 · gaming: LAVD에서 온 game chain과 Steam client](#4장--gaming-lavd에서-온-game-chain과-steam-client)
5. [5장 · interactive와 typing: 사람이 두드리는 application](#5장--interactive와-typing-사람이-두드리는-application)
6. [6장 · compile: make의 spawn table](#6장--compile-make의-spawn-table)
7. [7장 · background와 IO: 혼자 끝까지 도는 job들](#7장--background와-io-혼자-끝까지-도는-job들)
8. [8장 · browser 조각과 comms: 숨은 tab과 chat client](#8장--browser-조각과-comms-숨은-tab과-chat-client)
9. [9장 · daemon과 session process](#9장--daemon과-session-process)
10. [10장 · idle class를 선언하는 세 항목](#10장--idle-class를-선언하는-세-항목)
11. [11장 · library의 과거: 열두 항목에서 스물아홉 항목으로](#11장--library의-과거-열두-항목에서-스물아홉-항목으로)
12. [12장 · 기록이 스스로 밝히는 한계](#12장--기록이-스스로-밝히는-한계)
13. [13장 · 용어 정리](#13장--용어-정리)

---

# 1장 · scheduler가 보는 process

이 장은 "archetype은 process의 무엇을 적는가"라는 질문에 답합니다. 이 질문이 먼저 나오는 이유는 간단합니다. archetype이 적는 것은 우리가 평소에 아는 프로그램의 모습(창, 버튼, 파일 이름)이 아니라, **scheduler**가 보는 모습이기 때문입니다. scheduler가 무엇을 보고 무엇을 보지 못하는지를 알아야, archetype에 어떤 field가 있고 어떤 field가 없는지가 이해됩니다.

## 1.1 이름도 의도도 없는 세계

**scheduler**는 운영체제 안에서 "지금 CPU를 누구에게 줄지" 정하는 부분입니다. 웹 서버의 request queue에서 다음 request를 고르는 dispatcher를 떠올리면 가깝습니다. 다만 scheduler가 다루는 단위는 request가 아니라 **task**(실행 단위. Linux에서는 thread 하나가 task 하나이고, 이 dataset에서는 workload 파일의 실행 단위 하나를 task라 부릅니다)입니다.

scheduler 입장에서 task 하나는 이런 사건들의 흐름일 뿐입니다.

- 언제 **runnable**(CPU만 주면 바로 실행할 수 있는 상태)이 되는가
- runnable이 된 뒤 CPU를 얼마나 오래 쓰는가
- 무엇을 기다리며 멈추는가(디스크, 네트워크, 다른 task, 사용자 입력, 시간)
- 누구를 깨우는가
- 언제 자식 task를 만들고 언제 끝나는가

scheduler는 task가 "VS Code"인지 "LibreOffice"인지 모릅니다. 사용자가 그 창을 보고 있는지, 그 작업이 중요한지도 모릅니다. 이 연구는 바로 그 빈자리 — scheduler가 모르는 이름과 의도를 LLM이 process 이름에서 읽어 낼 수 있는가 — 를 묻습니다. 그래서 dataset은 두 가지를 엄격히 분리합니다. **이름**은 timeline이 붙이고, **행동**은 archetype이 정합니다.

`docs/workload/archetype-plan.md`(archetype 작성 규칙 문서. 2026-10-16에 9.15가 지금 library에 맞게 고쳐 썼고, §4는 29개 항목을 compile 경로별로 나열합니다)는 이 분리를 "boundary rules" 두 문장으로 적습니다. 첫째, scheduler가 관찰할 수 없는 것은 archetype에 살 수 없다 — process **이름**(timeline이 붙임), **개수**(binding 때 정해짐), **의미**(segment label의 일. segment는 timeline 안에서 하나의 상황 label이 유지되는 시간 구간)는 구조적으로 빠진다. 둘째, `source:` tag는 **값과 기술된 구조**를 정당화할 뿐 **field 이름**을 정당화하지 않는다 — field 이름은 이 schema가 지어낸 것이고, 항목의 모양이 출처에 기댄 부분은 `modeling_notes`에 따로 적는다.

> **왜 이렇게 정했나.** archetype-plan §1은 이유를 "what the scheduler cannot observe cannot live in an archetype"이라고만 적습니다. 실험 설계 쪽의 근거는 `docs/research-proposal.md`의 "The information asymmetry is the core of the design" 문단입니다. 이름(`name`)은 model(LLM)에게만, 행동(`pattern`)은 simulator에게만, 정답(`ground_truth`)은 oracle 조건과 채점기에게만 보인다는 것이고, "This must be enforced in code"라고 덧붙입니다. 이름과 행동이 서로 다른 층에 살아야 이 비대칭을 지킬 수 있습니다. core set(손으로 만든 workload 파일 묶음, 지금 51개)의 C2 짝 파일(예: `c2-p1a`/`c2-p1b`)은 이 분리를 이용해 한 segment만 다른 두 파일을 만듭니다(`docs/workload/building-plan.md`의 C2, "Intent pairs, one-segment diffs": "The shared tasks and segment 0 stay byte-identical").

> **코드로.** compiler는 archetype의 이름(`office-writer`)을 workload 파일에 쓰지 않습니다. 각 task의 `arrive` 사건에는 timeline이 준 `name`(예: `soffice.bin`)과 `declared_class`와 풀어진 program만 들어갑니다(`dataset/tools/wlc/compiler.py`의 `_arrive_event`). 그래서 simulator와 recognizer 어느 쪽도 archetype id를 볼 수 없습니다.

## 1.2 burst, sleep, 주기적 wake, input 대기, fork — 다섯 가지 모습

scheduler의 눈으로 보면, desktop의 process들은 몇 가지 모양으로 나뉩니다. 이 모양들이 곧 archetype의 문법(1.3절)을 정합니다.

**1) CPU burst.** **burst**는 task가 깨어난 뒤 다시 멈출 때까지 CPU를 연속으로 쓰는 한 덩어리입니다. 이 dataset은 이것을 **run**이라고 부르고, 측정에서는 "wake 한 번의 CPU 시간"으로 정의합니다(3.2절). 예를 들어 LibreOffice Writer는 key 하나가 눌릴 때마다 수 ms짜리 burst를 냅니다.

**2) Sleep.** task가 "지금부터 N μs 뒤에 다시 깨워 달라"며 스스로 멈추는 것입니다. 상대 시간이라는 점이 중요합니다. 늦게 깨어나면 다음 sleep도 그만큼 밀립니다.

**3) 주기적 wake.** 동영상 player처럼 "33.3 ms마다 한 frame"을 내야 하는 task는, 절대 시간의 격자(grid) 위에서 깨어납니다. 0 ms, 33.3 ms, 66.7 ms, … 처럼 정해진 시각에 깨어나고, 한 번 늦었다고 다음 시각이 밀리지 않습니다. 이런 task에는 **deadline**(이 시각까지 일을 끝내야 한다는 기한)이 자연스럽게 생깁니다. 다음 frame 시각이 이번 frame의 기한입니다.

**4) 무언가를 기다리기.** 사용자의 key 입력, 다른 task의 신호, 자식 process의 종료 같은 사건을 기다리며 멈춥니다. 시간이 아니라 사건이 깨웁니다. 이 깨어남을 **wake**(멈춰 있던 task가 runnable이 되는 사건)라고 부릅니다.

**5) Fork와 exit.** `make`가 compiler process를 수천 개 띄우듯, task가 자식 task를 만들고, 자식은 일을 마치면 끝납니다.

이 다섯 모양 위에 **preemption**(더 급한 task를 위해 실행 중인 task를 강제로 내려놓게 하는 것)과 **time slice**(한 task가 한 번에 쥘 수 있는 CPU 시간의 상한)가 scheduler 쪽 장치로 얹힙니다. archetype은 scheduler 쪽 장치는 적지 않습니다. archetype은 "task가 원하는 것"만 적고, 그것을 언제 얼마나 들어줄지는 simulator 안의 scheduler가 정합니다.

## 1.3 여섯 개의 primitive와 LOOP

archetype의 행동은 여섯 개의 **primitive**(문법의 기본 명령)로 쓴 작은 program입니다. 의미의 기준 문서는 `docs/simulator/interpretation-contract.md` §3이고, archetype-plan §1도 같은 목록을 싣습니다. 웹 개발자에게 익숙한 비유를 들자면, 이것은 task 하나를 위한 아주 작은 bytecode입니다. simulator는 task마다 이 bytecode를 한 줄씩 실행하는 작은 VM을 돌립니다.

| primitive | 뜻 | 쉬운 예 |
|---|---|---|
| `RUN(duration)` | CPU를 `duration`만큼 쓴다. 벽시계 시간이 아니라 CPU 수요다. 중간에 preemption되어도 남은 양은 사라지지 않는다 | key 하나를 처리하는 3 ms |
| `SLEEP(duration)` | 지금부터 `duration` 뒤까지 스스로 멈춘다(상대 시간) | batch job이 디스크를 기다리며 0.3 ms 쉬기 |
| `TIMER(period)` | 절대 격자 t₀ + k·period에서 깨어난다. 이전 반복이 늦게 끝나도 격자는 밀리지 않는다 | video player가 33.348 ms마다 frame 하나 |
| `WAIT(channel)` | `channel`에 WAKE나 외부 wake 사건이 올 때까지 멈춘다 | key 입력을 기다리기, 자식이 모두 끝나길 기다리기 |
| `WAKE(target)` | 다른 task `target`을 runnable로 만든다 | game chain에서 앞 단계가 다음 단계를 깨우기 |
| `FORK` / `EXIT` | spawn table의 다음 자식을 만든다 / 이 task를 끝낸다 | `make`가 `sh`를 띄우기 / `cc1`이 끝나기 |

여기에 반복을 위한 `LOOP`가 하나 더 있습니다. archetype 파일에서는 `loop:` 아래에 primitive 목록을 적고, compile된 workload에서는 `{"op": "LOOP", "count": "unbounded", "body": [...]}` 꼴이 됩니다. 반복 횟수가 정해지지 않은 LOOP는 task가 사라질 때까지 돕니다.

각 primitive를 아주 단순한 예로 다시 보겠습니다.

- **RUN만 있는 task**: `[RUN 30s, EXIT]`. 30초 동안 CPU를 쓰고 끝나는 hog입니다. 실제로 core set의 `c6-spoof` 파일에는 `chrome`이라는 이름을 달고 이렇게 한 번에 30초를 쓰는 task가 있습니다(6.3절, `cpu-batch`의 `spoof` program).
- **TIMER + RUN**: `[TIMER 33348μs, RUN 3982μs, TIMER 33348μs, RUN 3014μs, …]`. 33.348 ms마다 깨어나 그때그때 다른 양의 CPU를 씁니다. 실제 `c1-media`의 `video` task가 이렇게 compile됩니다(5.8절).
- **WAIT + RUN**: `[WAIT input:writer, RUN 3117μs, WAIT input:writer, RUN 10152μs, …]`. key가 올 때마다 깨어나 일합니다. 실제 `c1-office`의 `writer` task의 일부입니다(2.9절).
- **WAIT + RUN + WAKE**: `[WAIT chain:game.wineserver, RUN 341μs, WAKE game.chain.2]`를 LOOP로 감쌉니다. 앞 단계에게 깨워지면 일하고, 다음 단계를 깨웁니다. `c1-gaming`의 `wineserver` member입니다(4.1절).
- **RUN + FORK×6**: `make`가 job 하나를 시작할 때 dispatch CPU를 쓰고 자식 여섯을 띄웁니다. `c1-compile`의 `build` task가 이것을 2,908번 반복합니다(6.1절).

> **왜 이렇게 정했나.** TIMER가 primitive가 된 이유는 archetype-plan §6의 OQ-6 해소(open question 6, "문법이 충분한가")에 적혀 있습니다. "The gap was absolute time, not IO bandwidth: TIMER closes it (drift-free periodic demand)." 상대 SLEEP을 반복하면 task가 늦을수록 주기가 늘어나, 나쁜 scheduler 설정 아래에서 수요가 저절로 줄어듭니다. interpretation-contract §3은 이를 "relative sleeps drift under delay, silently lowering demand exactly under bad configs"라고 적고 "Periodic tasks use TIMER, never SLEEP loops"를 규칙으로 둡니다. 문법의 모양 자체는 rt-app(`rt-app`, Linux scheduler 시험용 workload 생성기)의 JSON task model을 선례로 인용합니다(`docs/references.md`의 `rt-app` 항목 role: "JSON task-model precedent (run/period/deadline in µs); schema-shape citation for archetypes and the TIMER primitive (`timer{ref,period}`)"). 숫자는 하나도 가져오지 않고 데이터셋 파일 어디도 이 id를 인용하지 않으므로, `rt-app`은 2026-10-16에 `dataset/sources.yaml` registry에서 빠졌습니다. 그 references.md 항목은 문서들이 인용하므로 남아 있습니다.

## 1.4 program에서 task의 일생으로

archetype의 program은 "틀"입니다. 실제 task 하나의 일생은 compile할 때 이 틀에 숫자를 채워 만듭니다. 여기서 이 dataset의 핵심 원칙 하나가 나옵니다. interpretation-contract §2가 적는 문장입니다. "Compile time resolves all randomness; run time resolves all timing that scheduling can influence." 무작위로 뽑는 일은 모두 compile할 때 끝나고, scheduler가 영향을 줄 수 있는 시각만 실행할 때 정해집니다.

웹 개발에 빗대면, archetype은 template이고 workload 파일은 seed로 렌더링한 snapshot입니다. 같은 timeline, 같은 library, 같은 seed면 byte까지 같은 파일이 나옵니다(`dataset/README.md`의 규칙). 그래서 CI는 build 결과의 hash를 commit된 manifest와 비교할 수 있습니다.

task의 일생이 어떻게 끝나는지는 archetype의 `lifetime` field가 정합니다. 세 가지가 있습니다(interpretation-contract §5).

| `lifetime` | 언제 떠나나 | 어떻게 끝나나 | 이 library의 예 |
|---|---|---|---|
| `segment-bound` | timeline이 정한 시각(`depart`)에 | 사용자가 닫는다(외부 사건) | editor, browser, player, daemon |
| `finite` | 정해지지 않음 | program이 EXIT에 닿는다. 언제 닿을지는 scheduling의 결과 | build, backup, indexer, download |
| `spawned` | 정해지지 않음 | 부모의 FORK로 실행 중에 생기고 EXIT로 끝난다 | `make`의 자식들, DKMS(새 kernel에 맞춰 kernel 밖 module을 다시 build하는 장치) build의 자식들 |

`finite` task의 끝나는 시각이 scheduling의 결과라는 점이 중요합니다. 30초어치 CPU가 필요한 job은, 다른 task와 CPU를 나눠 쓰면 30초보다 늦게 끝납니다. 이것이 scheduler 실험에서 "turnaround"(job이 시작해서 끝날 때까지의 시간)를 잴 수 있는 이유입니다.

archetype의 숫자 하나를 몇 번 뽑는지는 `sampling` field가 정합니다(interpretation-contract §5의 "Sampling granularity").

- `per-instance`: spawn table의 자식 하나마다 한 번. `make`가 띄우는 `cc1` 하나하나가 자기 CPU 양을 따로 뽑습니다.
- `per-task`: task 하나에 한 번 뽑아 계속 씁니다. 예를 들어 video player의 `period`, game chain member의 `per_schedule_run`.
- `per-iteration`: 반복마다 새로 뽑습니다. 단, 반복 횟수가 정해져 있어 compile 때 모두 펼칠 수 있을 때만 허용됩니다("only when bounded"). key 입력마다의 CPU, timer wake마다의 gap과 run이 여기에 해당합니다.

> **코드로.** `dataset/tools/wlc/sampling.py`는 모든 draw를 (seed, key…, index)의 SHA-256으로 정합니다. 전역 난수열을 쓰지 않으므로, 한 task를 고쳐도 다른 task의 draw가 밀리지 않습니다(파일 첫머리 docstring: "an edit to one task can never shift another task's draws"). `per-task` 값은 index 0으로, `per-iteration` 값은 반복 번호로 뽑힙니다(`compiler.py`의 `_draw`).

## 1.5 TIMER와 WAIT(timer) — deadline이 있는 wake와 없는 wake

이 library를 읽다 보면 같은 "timer로 깨어남"이 두 가지로 적혀 있는 것을 보게 됩니다. 이 차이는 scheduler 실험에서 아주 중요하므로 따로 설명합니다.

- **`TIMER(period)`**: 주기와 **deadline**이 있는 깨어남입니다. 다음 격자 시각이 이번 일의 기한입니다. 이 library에서 TIMER를 쓰는 항목은 넷뿐입니다. 세 개의 재생·통화 항목(`video-player`, `audio-player`, `video-call`)과 game chain의 머리(`game-task-chain`의 첫 member)입니다.
- **`WAIT(timer)`**: 측정에서 관찰된 timer 깨어남입니다. 정해진 시각에 외부 wake 사건이 오지만, **deadline은 없습니다**. editor의 커서 깜빡임, browser의 내부 timer, daemon의 주기 점검 같은 깨어남이 여기에 해당합니다.

> **왜 이렇게 정했나.** 9.5 slice(interactive와 typing을 맡은 연구 slice)의 D74("`TIMER` carries a period with a deadline; a measured timer wake is a `WAIT` on the task's timer channel", 2026-09-26)가 이 구분을 정했습니다. 기록된 이유는 이렇습니다. 그 전의 fold-in(측정값을 library에 넣는 작업)은 측정된 timer wake를 모두 `TIMER`로 compile하면서, 다음 wake까지의 gap을 period로 썼습니다. 그 결과 task들이 1 μs부터 시작하는 TIMER period를 갖게 되었습니다. 그런데 TIMER를 읽는 쪽이 셋이었습니다 — interpretation-contract §3, EDF(Earliest Deadline First, 기한이 가장 이른 task를 먼저 돌리는 scheduling 정책)의 deadline class를 정하는 `docs/recognition-vocabulary.md`, harness의 `job` primitive(`docs/harness/metrics.md` §6.2) — 그리고 셋 다 TIMER를 "deadline이 있는 주기적 job"으로 읽었습니다. 근거로 `liu-jacm73`(Liu & Layland 1973)의 "each task must be completed before the next request for it occurs"를 인용합니다. 기록된 숫자로, 이 정정 전 compile된 core set에서는 `chrome` task 107개 중 106개가 TIMER를 가졌고, `c1-media`의 `video` task는 첫 period가 9 μs였습니다. 정정 후 core set의 timer wake는 531,740개의 외부 wake 사건이 되었고 160만 개의 TIMER step이 사라졌습니다.

TIMER task가 격자 시각을 하나 이상 놓친 뒤에 TIMER에 닿으면 **skip 규칙**을 따릅니다. 이미 지난 격자 중 가장 마지막 것 하나만 즉시 실행하고(기한은 그다음 격자), 그 앞의 밀린 격자들은 일을 하지 않은 채 "기한을 놓친 job"으로 셉니다. archetype 쪽에서는 이 규칙으로 바뀌는 숫자가 없습니다. 규칙은 simulator가 TIMER를 어떻게 실행하느냐의 문제입니다.

> **왜 이렇게 정했나 — TIMER가 늦었을 때의 규칙(9.11 D3, D17).** 9.11 slice(scheduler 쪽 상수와 근거를 맡은 slice)의 D3(2026-10-07)에서 인지오가 그 전의 backlog 규칙(밀린 격자를 하나씩 다 실행)을 skip 규칙으로 바꾸었고, `docs/memos/2026-10-07-timer-skip-rule-for-the-simulator.md`가 simulator 담당 인경민에게 규칙(§1)과 근거(§4)를 적어 보냈습니다. 기록된 근거는 9.11이 읽은 주기 작업 framework와 프로그램이 기본값으로 밀린 주기를 다시 돌리지 않는다는 것입니다. interbench, ROS 2 executor, Lipari와 Palopoli의 soft real-time 주기 thread(그들의 Listing 2)는 늦은 주기를 건너뛰고, rt-app의 기본 모드는 timer를 늦은 시각에 다시 맞춥니다. 2026-10-08의 D17은 memo의 "none replays them"을 정정했습니다. rt-app의 'absolute' 모드와 fixed-timestep game loop의 simulation 단계는 밀린 주기를 따라잡고, 출처들은 늦게 도는 job이 어느 격자의 것인지에서 갈린다는 것입니다. D17은 영상 재생과, 오디오와 게임의 TIMER task를 나누어 적었습니다. 이 library의 항목에 대어 읽으면 이렇습니다. 지나간 마지막 격자를 즉시 실행하는 선택은 영상 재생(`video-player`)에서는 GStreamer video sink의 동작입니다. sink는 5 ms 넘게 늦은 frame을 버리고, 지금 시각이 든 frame을 바로 그립니다. audio의 주기를 가진 `audio-player`와 `video-call`(통화의 주기는 audio worker의 10 ms frame, 9.5 D75), 그리고 game chain의 머리에 대해서는 design입니다. Chromium의 fake audio worker는 늦은 callback 하나를 가장 이른 밀린 격자의 시각으로 돌리고(이 규칙이 고르는 가장 최근의 격자가 아님) 지금 다음의 격자로 건너뛰며(`fake_audio_worker.cc`), Vulkan의 FIFO 모드는 늦은 일이 어느 격자의 것인지 말하지 않습니다. harness의 `job` 지표는 이 규칙으로 읽습니다(`docs/harness/metrics.md` §6.2).

> **코드로.** reference simulator의 TIMER(`simulator/src/sim.cpp`)는 2026-10-23부터 skip 규칙으로 돕니다. 인경민의 stage Y이고(커밋 `a62c10b0`; `simulator/memo/memo_261023.md` Part G), 그 전의 step K("TIMER+backlog")를 대신합니다. 2026-10-17의 final memo(`docs/memos/2026-10-17-workload-dataset-rebuild.md` §6.2)가 RQ0 gate spec의 statement `simulator-conformance` 항목 (b)로 부탁한 것입니다. interpretation-contract §3의 TIMER 행은 2026-10-30에 2026-10-07 memo §6이 제안한 문장으로 바뀌었습니다(`docs/data-contracts.md` §14). "absolute periodic wake on the grid t₀ + k·period, drift-free. Reached after one or more ticks have passed, the task consumes the last passed tick at once and skips the earlier ones, each a missed job with no work."

## 1.6 declared_class: normal과 idle

모든 archetype 항목에는 `declared_class`라는 field가 있습니다. 값은 `normal` 아니면 `idle`입니다. 이 field를 이해하려면 Linux의 scheduling class를 조금 알아야 합니다.

**scheduling class**(또는 scheduling policy)는 프로그램이 "나를 어떤 부류로 취급해 달라"고 커널에 스스로 선언하는 값입니다. 대부분의 프로그램은 기본값인 `SCHED_NORMAL`(이 dataset의 `normal`)로 돕니다. 어떤 배경 프로그램은 스스로를 `SCHED_IDLE`로 선언합니다. **`SCHED_IDLE`**은 "다른 일이 없을 때만 나를 돌려 달라"는 뜻입니다. 커널의 가중치로 보면, 보통 task(nice 0)의 가중치가 1,024일 때 `SCHED_IDLE` task는 3입니다(9.11 D5가 인용하는 Linux 커널 `sched.h`와 `core.c`의 값). 바쁜 보통 task 하나 옆에서 CPU의 약 0.3 %만 받는다는 뜻입니다.

**nice**는 이와 다른 장치입니다. nice는 같은 normal class 안에서의 가중치 조절입니다(값 −20…19, 클수록 양보). nice 0의 가중치가 1,024, nice 10은 110, nice 19는 15입니다(9.11 D4, D6이 인용하는 `sched_prio_to_weight`). 웹 개발에 빗대면, scheduling class는 "이 job은 background queue에 넣어라"이고, nice는 "같은 queue 안에서 우선순위 숫자"입니다.

이 dataset의 결정은 이렇습니다.

- **class는 싣고, nice는 싣지 않습니다.** 이유(9.11 D6, 2026-10-07): "Nice is a weight within the normal class, not a class … of the simulated algorithms only LOTTERY has a weight to carry it, so no one rule holds under every algorithm." simulator는 네 가지 scheduling algorithm(MLFQ: time slice를 다 쓴 task의 우선순위를 내리는 여러 단계 queue; EDF; LOTTERY; FIFO: 먼저 온 task를 먼저 끝까지 돌림)을 돌리는데, nice 같은 가중치를 쓸 수 있는 것은 LOTTERY(추첨권 수로 CPU를 나누는 정책)뿐이라, 넷 모두에 같은 뜻으로 적용할 규칙이 없다는 것입니다.
- **class는 항목의 것이지 이름의 것이 아닙니다.** task의 class는 그 task가 묶인 archetype 항목의 `declared_class`를 그대로 받습니다. 이름에서 추측하지 않습니다. 그래서 어떤 media player에 `tracker-miner-f`라는 indexer 이름을 붙여도 그 task는 `normal`입니다.
- **값은 둘뿐입니다.** `idle`은 `file-indexer`(Tracker가 모든 thread를 `SCHED_IDLE`로 둠)와 `incremental-backup`(Déjà Dup이 backup을 `chrt --idle 0`으로 시작함), 그리고 bounding check용 변형인 `game-download-idle`에만 있습니다. 나머지 26개는 `normal`입니다. batch나 real-time 값은 그런 class의 일을 실제로 싣는 항목이 생길 때만 추가합니다.

executor(simulator에서 algorithm의 결정을 실행하는 부분) 쪽 규칙은 `docs/memos/2026-10-08-declared-scheduling-class.md`(이 field를 인경민과 박이안에게 알린 memo) §2가 적습니다. "A task whose class is `idle` runs only when no task of another class is runnable, and a task of another class that becomes runnable preempts it at once." 이 규칙은 MLFQ, EDF, LOTTERY, FIFO 모두에서 algorithm의 결정 **아래에** 적용됩니다. idle task는 다른 class의 runnable task가 하나도 없을 때만 돌고, 다른 class의 task가 깨어나면 즉시 내려옵니다.

> **왜 이렇게 정했나.** 9.11 D4(2026-10-07)가 "the simulated machine honours a task's declared scheduling class"를 정했습니다. 기록된 이유는 "Background programs declare their class themselves, and a stock Linux kernel acts on it"이고, 그렇지 않으면 "A machine that ignores it gives self-declared background work the standing of foreground work, and the recognizer's headroom on the files that hold it … is the excess"입니다. 즉 실제 desktop이 이미 배경으로 밀어내는 일을 simulator가 전경과 똑같이 대하면, LLM이 개선할 여지("headroom")가 실제보다 부풀려집니다. 9.11 D5는 idle class의 구체 규칙(위의 엄격한 규칙)을, 9.13 spec decision 2(2026-10-09, dataset rebuild sub-task의 결정)는 field 이름 `declared_class`와 "required on every entry, no default"를 정했습니다.

> **왜 이렇게 정했나.** 엄격한 규칙(다른 class가 있으면 0 %)은 커널의 약 0.3 %와 다릅니다. 9.11 D5는 이 차이를 "The deviation, stated"로 적고, 두 대안을 버린 이유를 기록합니다. 커널 가중치를 그대로 쓰는 안(B)은 "only LOTTERY has a weight to carry them, so no one rule holds under every algorithm", 최소 몫을 보장하는 엄격한 class 안(C)은 "its window and mechanism come from no source"라서 택하지 않았습니다.

> **왜 이렇게 정했나 — 엄격한 idle 규칙의 한계(9.11 D16, 2026-10-08).** 실제 Ubuntu desktop에서 idle 선언이 얼마나 먹히는지는 task group(커널이 CPU를 나눌 때 하나로 묶는 process 집단. Linux에서는 cgroup으로 만들고, systemd는 이것을 `app.slice`, `background.slice` 같은 slice로 관리합니다) 배치에 달려 있습니다. 9.11 D16(2026-10-08)은 커널의 idle 규칙이 "같은 task group 안의 형제들 사이"에서만 작동한다는 것을 sched(7) man page로 확인했습니다. Tracker는 `background.slice`에서 돌고 editor는 `app.slice`에서 돌기 때문에, 두 slice의 가중치(30 대 100)로 Tracker 쪽 group이 둘 다 바쁠 때 CPU의 약 23 %를 받습니다. 그러니 simulator의 indexer는 실제 desktop의 indexer보다 editor를 덜 방해하고, indexing 파일의 headroom은 과소평가됩니다. 이것은 `file-indexer` 항목의 `modeling_notes`에 한계로 적혀 있습니다. 반대로 Déjà Dup의 backup은 editor와 같은 `app.slice`에서 돌므로 엄격한 규칙이 실제와 맞습니다(10장).

마지막으로, 개수를 한 번 확인해 두겠습니다. 이 권은 항목이 29개라고 말합니다. 다음 명령이 그 근거입니다(2026-10-14, `jioh/dataset-rebuild` branch).

```
$ grep -cE '^  [a-z][a-z0-9-]*:' dataset/archetypes.yaml
29
```

29개는 다음과 같습니다(파일에 나오는 순서). `office-writer`, `code-editor`, `mail-client`, `web-browser`, `image-editor`, `video-editor`, `video-player`, `audio-player`, `video-call`, `renderer-hidden`, `chat-client`, `game-client`, `cpu-batch`, `compiler-child`, `build-orchestrator`, `module-build-orchestrator`, `module-compiler-child`, `file-archiver`, `game-download`, `game-download-idle`, `package-upgrade`, `file-indexer`, `video-transcoder`, `incremental-backup`, `game-task-chain`, `compositor-shell`, `audio-server`, `service-manager`, `message-bus`.

# 2장 · 항목 하나는 어떻게 적혀 있나

이 장은 "`archetypes.yaml`의 항목 하나를 열면 무엇이 보이고, 각 field는 무슨 뜻인가"에 답합니다. 이 질문이 필요한 이유는, 29개 항목이 모양이 제각각이기 때문입니다. 어떤 항목은 component가 열다섯 개이고, 어떤 항목은 table 두 개뿐이며, 어떤 항목은 job tree를 통째로 들고 있습니다. 공통 field와 종류별 부품을 먼저 익혀 두면 4장부터의 항목 설명을 훨씬 쉽게 읽을 수 있습니다. 장의 끝에서는 실제 항목 하나(`office-writer`)를 yaml에서 compile된 workload까지 손으로 따라가고, linter가 항목에 거는 규칙을 정리합니다.

## 2.1 파일 전체의 모양

`dataset/archetypes.yaml`은 1,946줄입니다(2026-10-17). 맨 위 약 70줄은 주석으로 된 **encoding rules**(이 파일을 쓰는 규칙)이고, 그 아래 `archetypes:` 한 줄 밑에 29개 항목이 이어집니다. 항목의 key가 곧 **archetype id**입니다(`office-writer:` 같은 것). 항목들 사이에는 어느 연구 slice의 어느 campaign에서 왔는지 적은 구분 주석이 있습니다(예: `# ---- measured per-application archetypes — 9.5 same-machine campaigns …`).

머리 주석의 첫 줄은 `# dataset/archetypes.yaml — the archetype library (v0.2)`입니다(2026-10-17). version은 `dataset/README.md`, `docs/data-contracts.md` §1의 계약표와 §2와 같습니다. 9.13 spec decision 9(dataset rebuild sub-task의 결정, "The library's stated version moves from v0.1 to v0.2 in the data-contracts §2 and the dataset README")가 버전을 v0.2로 올렸을 때 실제로 바뀐 곳은 README와 data-contracts §2뿐이어서, yaml 머리 주석과 data-contracts §1은 한동안 v0.1로 남아 있었습니다. 2026-10-16에 9.15가 둘 다 v0.2로 고쳤습니다(머리 주석은 9.15의 재빌드, commit `37c2e233`). 2026-10-16까지 첫 줄은 "Layer 1 archetype library"였습니다. "Layer 1"은 데이터셋의 층에 번호를 붙이던 옛 이름입니다. 2026-10-16부터 저장소 문서는 데이터셋의 층을 이름으로만 부르고(archetype library, scenario 목록, timeline), "Layer 1"은 인식 정확도라는 측정 층만을 뜻합니다(인지오의 결정, 9.15 작업 목록 W-0742). 머리 주석의 이 두 단어는 2026-10-17에 9.15의 두 번째 재빌드(commit `7b024003`)에서 빠졌습니다. 이 파일은 모든 manifest의 입력이라, 주석 한 줄을 고쳐도 일곱 manifest가 다시 bless되고 RQ0 gate spec이 다시 pin됩니다.

머리 주석은 이 파일의 schema가 "our invention"이라고 밝힙니다. 그리고 각 field의 규칙을 짧게 나열합니다. 이 장의 2.2–2.7절은 그 규칙을 하나씩 풀어 설명한 것입니다.

## 2.2 머리 field: 모든 항목이 가진 것

`dataset/tools/wlc/linter.py`의 `REQUIRED_ARCHETYPE_FIELDS`는 모든 항목이 가져야 하는 field 아홉 개를 정합니다. `category_source`, `declared_class`, `pattern`, `params`, `lifetime`, `binding_params`, `scalable`, `validation_stats`, `modeling_notes`입니다. 하나씩 봅니다.

**`category_source`** — 이 항목이 나타내는 "행동 부류"가 어디서 왔는지 적습니다. 머리 주석은 이를 "the Tier-1 ground of the entry's existence"(항목이 존재해도 되는 근거, archetype-plan §2의 Tier 1)라고 적습니다(2026-10-17부터; 그 전에는 "Tier-1 provenance"). archetype-plan §5의 field 목록은 지금도 "Tier-1 provenance"라고 부릅니다. 원래 설계에서는 interbench, ananicy-rules 같은 기존 분류표의 이름을 적게 되어 있었습니다. 지금은 29개 중 28개가 `meas`입니다. `meas`는 "이 행동 부류는 우리 측정에서 관찰한 것"이라는 뜻입니다. 나머지 하나 `game-task-chain`만 `lavd-ossna24`(LAVD 발표 자료)입니다.

**`declared_class`** — 1.6절에서 설명했습니다. `normal` 또는 `idle`, 기본값 없음.

**`pattern`** — 행동의 틀입니다. 대개 `program:` 하나를 가지고, 그 안에 1.3절의 primitive로 쓴 program이 있습니다. 몇몇 항목은 `constructor:`(compiler가 이 항목을 특별한 방식으로 펼치라는 표시)를 가집니다. 지금 쓰이는 constructor는 세 가지입니다. `batch-loop`(7장의 batch job들), `chain`(`game-task-chain`), `module-build`(`module-build-orchestrator`). 또 `module-build-orchestrator`는 `job_order`, `module-compiler-child`는 `trees`, `letters`, `names`를 pattern 안에 가집니다(2.6절).

**`params`** — program이 이름으로 부르는 숫자들입니다. program 안의 `RUN: input_run`은 "`params.input_run`에서 값을 뽑아 RUN하라"는 뜻입니다. params의 모든 숫자는 **distribution object**로 적힙니다(2.3절). measured 항목은 params 안에 `components`, `stimulus`, `operations` 같은 부품을 가집니다(2.4절).

**`lifetime`** — `segment-bound`, `finite`, `spawned` 중 하나(1.4절). `spawned` 항목은 반드시 `spawned_by`(자신을 띄우는 부모 항목)를 가져야 하고, 부모 항목은 `spawns`(자신이 띄우는 자식 항목)를 가집니다. 지금 이 짝은 두 쌍입니다. `build-orchestrator` → `compiler-child`, `module-build-orchestrator` → `module-compiler-child`.

**`binding_params`** — timeline이 반드시 값을 넣어야 하는 손잡이의 **이름**만 적습니다. 값은 적지 않습니다. 머리 주석의 규칙은 "names only — knobs the timeline/scenario binding must supply (counts, caps, total work). Counts never carry values here"입니다. 웹 개발에 빗대면 component의 required props 목록입니다. 지금 쓰이는 손잡이는 다음과 같습니다.

| 손잡이 | 뜻 | 쓰는 항목 |
|---|---|---|
| `total_work` | job이 끝날 때까지 쓸 CPU 총량 | `cpu-batch`와 batch-loop 항목 여섯(+`game-download-idle`) |
| `program` | `cpu-batch`가 어느 프로그램의 table을 쓸지 | `cpu-batch` |
| `spawn_count` | object job 개수 | `build-orchestrator` |
| `parallelism_cap` | 동시에 돌릴 job 개수 상한(`make -jN`의 N) | `build-orchestrator`, `module-build-orchestrator` |
| `child_name` | compiler 자식(`cc1`)에 붙일 이름 | 같은 둘 |
| `lane_share` | game chain의 frame당 수요를 lane의 몇 배로 맞출지 | `game-task-chain` |
| `member_names` | game chain member들의 이름 | `game-task-chain` |

나머지 항목(대부분의 segment-bound 항목)은 `binding_params: []`입니다. 이름과 시각만 받으면 됩니다.

**`scalable`** — compile의 lane-scaling 단계가 바꿔도 되는 field와 그 규칙입니다. **lane**은 simulator가 흉내 내는 CPU 하나를 뜻합니다(이 연구의 simulator는 CPU 하나짜리 machine을 돌립니다). 지금 `scalable`이 비어 있지 않은 항목은 `game-task-chain` 하나뿐입니다. 그 규칙은 "scale the chain's aggregate demand per frame to lane_share of the lane"입니다(4.1절). 나머지 28개는 `scalable: []`, 즉 "측정한 그대로이고 절대 늘리거나 줄이지 않는다"입니다.

**`validation_stats`** — 이 항목이 무엇과 맞아야 하는지, 또는 맞춰 볼 **referee**(심판, 즉 항목이 실제와 맞는지 판정할 기준 관측)가 왜 없는지 적습니다. 2.7절에서 자세히 봅니다.

**`modeling_notes`** — 출처 위에 우리가 지어낸 것을 적는 산문입니다. 2.7절에서 봅니다.

## 2.3 숫자는 모두 distribution object

library의 숫자는 맨 숫자로 적히지 않습니다. 모든 숫자는 `{dist, <매개변수>, sampling, source}` 꼴의 **distribution object**입니다. 시간은 정수 microsecond(μs)입니다. 이 규칙 덕분에 숫자 하나하나가 "어떤 분포에서", "몇 번 뽑고", "어디서 왔는지"를 함께 들고 다닙니다.

지금 library에 쓰이는 `dist`는 세 가지입니다.

**1) `constant`** — 값 하나. 예: `period: {dist: constant, value_us: 33348, sampling: per-task, source: "meas-ci:playback:2026-09-18"}`. 시간이 아닌 값은 `value`를 씁니다(`chain_length: {dist: constant, value: 16, …}`).

**2) `lognormal`** — 로그정규분포. 머리 주석은 `{median_us, sigma_log}`로 적고 compiler가 `median * exp(sigma_log * z)`로 뽑는다고 말합니다. 지금 library에서 lognormal을 쓰는 곳은 `game-task-chain`의 `per_schedule_run` 하나이고, 그것도 median과 sigma 대신 `anchor_min_us: 260, anchor_max_us: 1650`이라는 두 기준점을 줍니다. compiler는 두 값을 5번째와 95번째 percentile로 읽어 median을 √(260×1650) ≈ 655 μs, sigma_log를 ln(1650/655)/1.645 ≈ 0.562로 계산합니다(`sampling.py`의 `anchored_lognormal_params`; 이 숫자는 9.4 slice의 scope card에도 "compiled median 655 µs, σ_log 0.562"로 기록되어 있습니다). 출처가 범위만 줄 때 lognormal을 쓰는 것은 archetype-plan §6의 OQ-5 해소가 정한 **convention**(관례)입니다("lognormal remains the convention where a source gives only a span"). 측정된 분포는 아래의 quantile 표로 싣습니다.

**3) `quantiles`** — 측정한 분포를 그대로 싣는 표입니다. 9.5 slice가 2026-09-15에 도입했습니다(9.5 D17, "measured distributions are encoded as quantile tables"). 생김새는 이렇습니다.

```yaml
input_run:
  {dist: quantiles,
   p: [2049, 2364, 2532, 2850, 3230, 6328, 9551, 10167, 11367, 62153],
   min: 0, max: 194092,
   means: [1870.685, 2236.17, 2449.671, 2703.725, 3043.957, 3988.081,
           8731.309, 9832.528, 10615.573, 13356.447, 166364.952],
   sampling: per-iteration, source: "meas-ci:interactive:2026-09-18"}
```

`p`의 열 개 숫자는 순서대로 p1, p5, p10, p25, p50, p75, p90, p95, p99, p99.9 percentile입니다(μs). `min`과 `max`는 관측된 최솟값과 최댓값입니다. `means`의 열한 개 숫자는 min–p1, p1–p5, …, p99.9–max의 열한 구간 각각에서 실제로 관측된 표본의 평균입니다. 위 예는 `office-writer`의 key 하나당 CPU입니다. 중간값 3.23 ms, 99번째 percentile 11.4 ms, 가장 긴 것 194 ms입니다.

> **왜 이렇게 정했나.** 9.5 D17이 기록한 이유는 측정된 분포가 lognormal에 맞지 않았다는 것입니다. "the log-sigma implied by p90 and by p99 differ by 2–3× for VS Code's per-input run (0.41 vs 1.07), Thunderbird's (0.33 vs 0.92) … Writer's idle gap is bimodal (p50 102 ms, p90 600 ms); the mpv decode worker (0.58 vs 0.49) and the WebRTC audio thread (0.30 vs 0.29) alone fit a log-normal." 분포 family를 억지로 정하는 대신 관측을 표로 싣기로 한 것입니다. 출처가 범위만 줄 때는(`game-task-chain`의 두 기준점) lognormal convention이 그대로 남습니다(archetype-plan §6의 OQ-5).

> **왜 이렇게 정했나.** `min`, `max`, `means`는 처음부터 있던 것이 아닙니다. 9.5 D71(2026-09-24, "the compiled entries reproduce what was measured")이 추가했습니다. 그 전에는 열 개의 percentile 사이를 직선으로 이어 뽑았는데, 2026-09-24의 review가 이 방식이 평균을 지키지 못한다는 것을 찾았습니다. 기록된 숫자는 "3 % off at the median, 17 % at the 90th percentile for runs; 9 % and 53 % for gaps"입니다. 지금 compiler는 draw가 떨어질 구간을 고른 뒤, 그 구간 안에서 lo + (hi − lo)·v^a 꼴의 곡선을 따라 뽑습니다. 지수 a는 그 구간의 평균이 측정된 평균과 같아지도록 정합니다. 그래서 percentile도 지키고 표 전체의 평균도 지킵니다(`sampling.py`의 `_quantile_sample` 주석: "the percentiles are kept and so is the table's mean").

> **코드로.** `sampling.py`의 `_quantile_sample`은 기본적으로 0을 1 μs로 올립니다(너무 짧은 시간은 1 μs로 친다). 단 `allow_zero=True`로 부르면 0을 그대로 둡니다. batch job의 block table과 `input_run`이 이렇게 불립니다. block table의 0은 "다른 thread가 이어서 돌았다"는 측정값이고(9.6 D25), `input_run`의 0은 "key가 task를 깨웠지만 idle 수준 이상의 CPU를 쓰지 않았다"는 측정값이기 때문입니다(9.5 D48: "a drawn zero is kept … an input whose run draws zero emits its WAIT with no RUN after it").

**`sampling`**은 1.4절의 세 값 중 하나입니다. linter는 이 세 값 밖의 것을 거부합니다.

**`source`**는 이 숫자가 어디서 왔는지 적는 **source tag**입니다. 2.8절에서 읽는 법을 자세히 봅니다. 여기서는 모양만 기억하면 됩니다. `<id>` 또는 `<id>:<locator>`이고, `id`는 `dataset/sources.yaml`에 등록된 출처입니다. 예: `meas-ci:interactive:2026-09-18`(우리 측정 campaign), `swell-icmi14:word-c1`(SWELL-KW 데이터의 Word 조건 1 녹화), `lavd-ossna24:s13`(LAVD 발표의 13번 slide).

## 2.4 measured 항목의 부품들

9.5, 9.8, 9.9 slice가 만든 **per-application archetype**(application 하나를 통째로 측정한 항목)은 params 안에 여러 부품을 가집니다. 머리 주석의 설명을 풀어 보겠습니다. 어떤 항목이 어떤 부품을 가지는지 먼저 표로 보이고, 부품마다 설명합니다.

| 항목 | `components` | `focus_components` | `stimulus` + `input_run` | `operations` | `heavy_events` | `launch` | `period` + `cycle_run` |
|---|---|---|---|---|---|---|---|
| `office-writer` | 1 | – | Word | – | – | ○ | – |
| `code-editor` | 9 | – | Word | – | – | – | – |
| `mail-client` | 15 | – | Outlook | `send` | – | ○ | – |
| `web-browser` | 7 | – | IE | `page-load` | `MemoryInfra` | ○ | – |
| `image-editor` | – | 1 | – | `unsharp-mask` | – | – | – |
| `video-editor` | 2 | 3 | – | `preview-render` | – | ○ | – |
| `video-player` | – | – | – | – | – | ○ | ○ |
| `audio-player` | – | – | – | – | – | ○ | ○ |
| `video-call` | – | – | – | – | – | ○ | ○ |
| `renderer-hidden` | 6 | – | – | – | – | ○ | – |
| `chat-client` | 6 | – | – | – | – | ○ | – |
| `game-client` | 11 | – | – | – | `CHTTPClientThre` | ○ | – |
| `compositor-shell` | 3 | – | – | – | – | – | – |
| `audio-server` | 1 | – | – | – | – | – | – |
| `service-manager` | 1 | – | – | – | – | – | – |
| `message-bus` | 1 | – | – | – | – | – | – |

(숫자는 component 개수, residual 포함. ○는 있음. 이 표는 `archetypes.yaml`을 python으로 읽어 세었습니다.)

### `components` — timer로 깨어나는 부분

**component**는 application의 process tree 안에서 같은 이름으로 깨어나는 thread 묶음 하나입니다. 이름은 **comm**(Linux가 thread마다 붙이는 최대 15글자의 짧은 이름. `ps`나 `top`에 보이는 그 이름)으로 정합니다. process가 여럿인 프로그램(Chrome, VS Code)에서는 process의 역할과 comm을 붙여 `gpu/VizCompositorTh`, `renderer/Compositor`처럼 씁니다(9.5 D67, 2026-09-23: "a component is identified by its process role and comm together").

component 하나는 다섯 값을 가집니다.

- `comm`: 이름.
- `threads`: 관측된 thread 수. 숫자 하나 또는 `[최소, 최대]` 범위입니다(repeat마다 달랐을 때).
- `wakes_per_s`: 초당 wake 수. 다섯 자리 유효숫자로 적습니다(9.5 D71).
- `gap`: 연속한 두 wake 사이 시간의 quantile table.
- `run`: wake 한 번의 CPU 시간의 quantile table.

component는 wake 비율이 큰 것부터 차례로 골라, 그 phase 전체 wake의 95 %를 덮을 때까지 싣습니다. 나머지 comm들은 **residual**이라는 component 하나로 묶습니다. residual은 `comms:` 목록에 무엇을 묶었는지 적습니다(9.5 D16, 2026-09-15: "Components kept in descending wake rate until they cover 95 % of idle wakes; the rest pooled into one residual component"). 각 항목의 components 끝에는 `# 8 comms cover 97.2 % of 112.4 wakes/s (D16, target 95 %); the rest pooled as residual` 같은 주석이 붙어 있습니다.

compiler는 component마다 gap table에서 gap을 뽑아 wake 시각을 만들고, wake마다 run table에서 run을 뽑습니다. 그리고 모든 component의 wake를 시간순으로 합쳐 task 하나의 사건 흐름으로 만듭니다. 각 timer wake는 `WAIT timer:<task id>` + `RUN`이 되고, 그 시각에 외부 `wake` 사건이 하나 생깁니다(1.5절의 deadline 없는 wake).

> **왜 이렇게 정했나.** 9.5 D9(2026-09-14, "shape of the six measured archetypes: one task, merged event stream")가 이 모양을 정했습니다. 이유는 둘입니다. 하나는 관측된 연구들이 key 하나당 CPU를 그 앞 gap과 무관한 분포로 잰다는 것입니다(옛 항목의 "burst = gap의 일정 비율" 결합은 출처가 없었습니다). 다른 하나는 모든 관측이 입력 옆에 timer로 깨어나는 일을 보고한다는 것입니다("timer messages 35.1 % vs UI 20.3 % of CPU", Lorch 2003 Table 2; 커서 깜빡임, 맞춤법 검사, 자동 저장, 화면 그리기, 메일 확인 timer). task 하나는 순차 program 하나이므로, 두 종류의 wake를 compile 때 하나의 흐름으로 합칩니다. 버린 대안은 "application당 task 두 개"(이름이 하나 더 생김)와 "입력만 있는 loop"(timer wake를 버림)였습니다.

> **왜 이렇게 정했나.** component의 첫 wake는 task가 시작하는 순간이 아니라 "이미 돌고 있던 흐름의 다음 wake"로 뽑습니다(9.5 D77, 2026-09-26, "a component starts as a stream already running"). 기록된 이유는, 보통의 gap으로 시작하면 gap보다 짧은 span에서 비율이 틀어진다는 것입니다. 60초 task에서 `message-bus`는 측정 비율의 16.5배, `audio-server`는 6.85배로 깨어났습니다. 지금은 임의의 시각이 긴 gap에 걸릴 확률이 더 크다는 점(길이에 비례한 표본, forward-recurrence)을 반영해 첫 gap을 뽑습니다(`sampling.py`의 `sample_first_gap`).

### `focus_components` — 화면 앞에서 조작될 때의 리듬

`image-editor`와 `video-editor`는 사람의 녹화된 입력이 없어서, 측정할 때 scripted pointer loop(정해진 순서로 drag, click, wheel을 반복하는 script, design)로 조작했습니다. 이때 관측된 thread 리듬을 `focus_components`로 싣습니다. compiler는 timeline의 `input` 창(사용자가 그 application에 입력하고 있다고 timeline이 정한 시간 구간) 안에서는 `components` 대신 `focus_components`를 씁니다. 입력 wake는 만들지 않습니다(입력이 script였으므로).

### `stimulus`와 `input_run` — 사람이 두드리는 부분

typing 항목 넷(`office-writer`, `code-editor`, `mail-client`, `web-browser`)은 사람이 실제로 친 key의 시각을 재생합니다. `stimulus`는 어느 녹화를 쓸지 적습니다.

```yaml
stimulus:
  {stream: swell-word-c1, kinds: [key], sampling: per-task, source: "swell-icmi14:word-c1"}
```

`stream`은 `dataset/stimulus/<stream>.jsonl` 파일 이름입니다. 이 파일은 `{"t_us": 6620100, "kind": "key"}` 같은 줄의 목록입니다. `kinds: [key]`는 key 사건만 쓰라는 뜻입니다(click, wheel, drag는 버림). 녹화는 SWELL-KW(`swell-icmi14`: 2012년 학생과 인턴 25명이 실험실의 Windows에서 각각 약 3시간 동안 지식 노동 과제를 한 기록, 키 하나하나의 timestamp와 그때 앞에 있던 application이 남아 있음)에서 왔습니다. 세 stream이 있습니다. `swell-word-c1`(Word, 조건 c1, 82,634줄), `swell-outlook-c23`(Outlook, 조건 c2와 c3, 7,584줄), `swell-ie-c1`(Internet Explorer, 조건 c1, 21,671줄).

compiler는 timeline의 `input` 창마다, 녹화에서 창 길이만큼의 연속한 구간을 seed로 정한 위치에서 잘라 재생합니다. key 하나하나가 `WAIT input:<task id>` + `RUN`이 되고, 그 RUN의 길이는 `input_run` table에서 뽑습니다.

> **왜 이렇게 정했나.** 9.5 D18(2026-09-15)이 "the simulated input is a replayed SWELL-KW stream, cut per focus window at compile time"을 정했습니다. 기록된 이유는 "replay preserves the burst-and-pause structure that forms and drains an editor's queue, which independent sampling from a quantile table … cannot reproduce; the simulated stimulus is then the population the per-input runs (D13) were measured under"입니다. 사람이 타이핑할 때 생기는 몰아치기와 멈춤의 구조를 그대로 살리고, 측정할 때 쓴 바로 그 입력으로 시뮬레이션한다는 것입니다. 9.5 D6은 이를 떠받치는 규칙입니다. "a response-side value … comes from a Linux observation only; a stimulus-side value — inter-key intervals, pauses, click, drag and wheel timing — may come from an observation on any platform, since it is a property of the person, not of the machine." 입력 쪽 시각은 사람의 성질이므로 Windows 녹화를 써도 되고, 응답 쪽(CPU 사용)은 Linux 관측만 쓴다는 것입니다.

`input_run`은 **per-input run**, 즉 key 하나에 대한 application 전체의 CPU 비용입니다. 정의는 9.5 D13의 **window rule**입니다(2026-09-15). "all CPU run time of the application's process tree from a replayed input's send time until the next input, minus the idle phase's CPU rate over that span." 즉 key를 보낸 순간부터 다음 key까지 process tree 전체가 쓴 CPU에서, 아무 입력이 없을 때의 평소 CPU 속도만큼을 뺀 값입니다. 음수는 0으로 자릅니다.

> **왜 이렇게 정했나.** 9.5 D13이 비교한 세 규칙 중 (b) window rule을 택한 이유는, 다른 두 규칙이 다른 thread의 후속 작업을 놓쳤기 때문입니다. "rules (a) first-wake and (c) X-server-woken schedule-ins undercount the follow-up work on other threads (VS Code's renderer and compositor carry the 23 ms)". 기록된 결과: window rule로 Writer 2.84 ms, VS Code 23.0 ms였을 때 (a)는 0.07–0.37 ms, (c)는 0.54–2.61 ms였습니다. 대신 치르는 비용도 scope에 적혀 있습니다. 긴 gap 안의 timer 아닌 일(예: 타이핑 뒤의 자동 저장)이 그 앞 key의 몫으로 잡힙니다.

### `operations` — 이름 붙은 무거운 작업

`operations`는 사용자가 명시적으로 시키는 무거운 작업입니다. 지금 넷이 있습니다. `mail-client`의 `send`(첨부 파일 달린 답장 보내기), `web-browser`의 `page-load`(무거운 feed page 열기), `image-editor`의 `unsharp-mask`(사진에 선명도 필터), `video-editor`의 `preview-render`(timeline 미리보기 렌더링). 각 operation은 `duration`(시작부터 완료까지 걸린 시간의 quantile table)과 그 동안의 `components`를 가집니다.

timeline은 operation의 이름과 시작 시각을 정합니다. compiler는 `duration` table에서 길이를 뽑고, 그 구간 동안 평소 component들을 operation의 component들로 바꿉니다. 그 구간에는 입력 wake를 만들지 않고, operation은 focus 창을 넘어서도 끝까지 갑니다(9.5 follow-ups spec decisions 8–10: "From its start the operation's components replace whatever is active … no input wakes are emitted during it").

### `heavy_events` — 드문 무거운 run

측정 중 가끔 한 번씩만 나오는 무거운 run은 component의 정상 표본에 섞으면 표를 망칩니다. 그래서 따로 **heavy event**로 싣습니다(9.5 D64, 2026-09-21). 지금 둘이 있습니다. `web-browser`의 `MemoryInfra`(Chrome의 메모리 점검 thread가 가끔 하는 53–61 ms짜리 pass)와 `game-client`의 `CHTTPClientThre`(Steam client의 HTTP thread가 가끔 몰아서 하는 1–50 ms짜리 run). 각각 `run_floor_ms`(이 길이 이상의 run만 heavy로 침, design), `count`(관측된 횟수), `span_s`(그 횟수를 센 전체 관측 시간), `rate_per_s`(count / span), `run`(그 run들의 table)을 가집니다. compiler는 이 비율로 간격을 지수분포에서 뽑아 아무 시각에나 둡니다. linter는 heavy event에 `gap`이 있으면 거부합니다. "a heavy event states no gap — none is measured (D64)." 한 session에 많아야 한두 번 나오므로 간격 자체는 잴 수 없었기 때문입니다.

### `launch` — application이 막 켜질 때

timeline이 application을 파일 중간에 시작시키면(0초가 아닌 시각에 `arrive`), 그 application은 먼저 실제로 관측된 **launch phase**(켜진 직후 바쁜 구간)를 재생합니다. `launch: {stream: launch-office-writer, sampling: per-task, source: "meas-ci:desktop:2026-10-04b"}`는 `dataset/launch/launch-office-writer.json.gz` 파일을 가리킵니다. 이 파일은 측정 repeat마다 launch phase의 길이와, 그 동안의 wake 하나하나(phase 시작으로부터의 시각, run, thread)를 담습니다. 예를 들어 `office-writer`의 launch phase는 다섯 repeat 모두 약 40.76초이고, 그 동안 838–863개의 wake가 있습니다(파일을 열어 repeat마다 센 값). compiler는 file seed로 repeat 하나를 골라 그 wake들을 그대로 재생하고, phase가 끝나면 평소의 component 흐름을 시작합니다. 0초에 이미 있는 task는 launch를 재생하지 않습니다(이미 안정 상태로 봄).

> **왜 이렇게 정했나.** 9.10 slice(scenario와 timeline을 맡은 slice)의 D21(2026-10-01)이 "an application started mid-file runs its observed launch phase first"를 정했고, D136(2026-10-04)이 그 형식을 "replay"로 정했습니다. D136이 기록한 이유: "launch work is a sequence (dry run soffice: 1.6 s CPU in its first 2 s, 887 ms of it in two runs of 427 and 459 ms)". launch는 분포가 아니라 순서가 있는 사건열이라, 표로 뽑지 않고 녹화처럼 재생합니다. 버린 대안은 "tables per 10 s slice"였습니다. 같은 결정이 "no value is a distribution, so no stability test"라고 적습니다. launch 재생에는 3장의 stability rule이 적용되지 않습니다. 지금 launch를 가진 항목은 열 개입니다(9.10 D140, 2026-10-05).

### `period`와 `cycle_run` — 재생과 통화

`video-player`, `audio-player`, `video-call`은 component 대신 **주기 job** 하나를 가집니다. `period`(constant, 매체의 한 주기)와 `cycle_run`(한 주기 동안 process tree 전체가 쓴 CPU의 quantile table)입니다. compiler는 task가 사는 동안 `TIMER period` + `RUN cycle_run` 쌍을 주기마다 하나씩 펼칩니다. 이 RUN의 기한은 다음 주기의 시작입니다.

> **왜 이렇게 정했나.** 9.5 D75(2026-09-26, "the playback and call archetypes: one periodic job per medium cycle, period and run measured")가 정했습니다. D74가 TIMER를 "deadline이 있는 주기 job"으로 정의했으므로, 진짜 주기가 있는 이 셋만 TIMER를 갖고, 그 주기는 측정에서 읽습니다. 주기의 시작은 기준 thread로 정했습니다. `video-player`는 video 출력 thread `vo`가 1 ms 이상 도는 frame 복사, `audio-player`는 5 ms 조용한 뒤 audio 출력 thread `ao`의 첫 wake, `video-call`은 audio worker thread의 wake(10 ms audio frame마다)입니다. 기한은 `liu-jacm73`의 period-implicit deadline(다음 요청 시각까지)입니다. 측정 기록에 남은 이 cycle 정의와 값들은 측정 campaign의 pooled record 안 `cycle` 블록에 있고, `archetypes.yaml`에는 그 결과인 `period`와 `cycle_run`만 실립니다. 9.16(exit audit) 항목의 "the three periodic pools' `cycle` blocks reproduce from releases `meas-ci-2026-09-18` and `meas-ci-2026-09-20`"은 2026-10-17에 확인되었습니다. `cc51eb8`의 `pool.py`를 두 release에 돌리자 세 pool 전체가 그 commit의 기록과 같았고(`audio-player` 4,243 leaf, `video-player` 3,966, `video-call` 24,867), 각 `cycle` 블록은 지금의 것과도 같았습니다(`_dev/research/jioh/task-9.16-exit-audits/meas/repro-table.md`의 E절).

## 2.5 batch 항목의 부품: `batch-loop`

7장의 background job들과 6장의 `cpu-batch`는 같은 모양을 공유합니다. `pattern.constructor: batch-loop`이고 program은 이렇습니다.

```yaml
pattern:
  constructor: batch-loop
  program:
    - loop:                    # until total_work of CPU is spent
        - RUN: 7z_run
        - SLEEP: 7z_block
    - EXIT: {}
params:
  7z_run:   {dist: quantiles, p: [...], ..., source: "meas-ci:background:2026-09-19"}
  7z_block: {dist: quantiles, p: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ..., source: "meas-ci:background:2026-09-19"}
binding_params: [total_work]
```

읽는 법은 이렇습니다. job은 **run between voluntary blocks**(프로그램이 스스로 멈추기 전까지 연속으로 쓴 CPU 한 덩어리)를 `<program>_run` table에서 뽑아 RUN하고, 그 뒤에 이어진 **block**(프로그램이 CPU를 쓰지 않고 멈춰 있던 시간)을 `<program>_block` table에서 뽑아 SLEEP합니다. 이것을 timeline이 준 `total_work`만큼의 CPU를 다 쓸 때까지 반복하고 EXIT합니다.

중요한 세부가 하나 있습니다. block table에는 0이 많습니다. 여러 thread를 가진 프로그램에서 한 thread가 멈춰도 다른 thread가 바로 이어서 돌면, 프로그램 전체로 보면 멈춘 시간이 0입니다. compiler는 0인 block을 만나면 SLEEP을 넣지 않고 앞뒤 run을 하나의 RUN으로 합칩니다. 그래서 7-Zip처럼 block이 거의 항상 0인 프로그램은 거의 끊김 없는 긴 RUN 몇 개로 compile됩니다.

> **왜 이렇게 정했나.** 이 모양은 9.6 slice(compile을 맡은 slice)의 D21(2026-09-19, "`cpu-batch` carries each bound program's measured run-between-blocks shape")에서 시작합니다. 기록된 이유는 simulator의 규칙이 task를 "voluntary block 사이의 run 길이"로 분류한다는 것입니다. MLFQ(Multi-Level Feedback Queue, task가 time slice를 다 쓰면 우선순위를 내리는 정책)는 slice가 끝나기 전에 스스로 멈추는 task를 같은 level에 두고, simulator의 batch class 규칙도 같은 것을 봅니다. 그래서 "한 번에 끝까지 RUN"으로 적으면 실제보다 더 batch처럼 보입니다. 기록된 숫자로, 10 ms를 넘어 쉬지 않고 쓴 CPU의 비율은 `clamscan` 0.107–0.115, `python3` 0.917–0.920 등으로 프로그램마다 크게 달랐습니다. 9.6 D22는 여러 thread 프로그램을 task 하나로 두고 모든 thread의 run을 한 표에 모으기로, 9.6 D25는 block을 "run 직후 이어진 프로그램의 off-CPU 시간(다른 thread가 돌았으면 0)"으로 정했습니다. D25가 기록한 이유: gap마다 block을 넣으면 `ffmpeg`의 포화도가 0.9996에서 약 0.89로 떨어집니다(4개 repeat에서 run 106,732개에 gap 165개). 9.7 slice(background와 IO를 맡은 slice)의 D29(2026-09-22)는 이 batch loop를 `file-archiver`, `game-download`(그리고 지금은 사라진 `file-backup`)에도 쓰기로 했습니다. 이유는 run-then-wait 순서로는 여러 thread 프로그램을 재현하지 못했기 때문입니다. 기록된 비교: CPU 점유율이 7-Zip은 실측 1.000인데 run-then-wait로는 0.115, SteamCMD는 실측 0.937인데 0.020이었고, batch loop로는 1.000과 0.936이 나왔습니다.

`cpu-batch`는 table 묶음이 여럿이어서 timeline이 `program` 손잡이로 어느 묶음을 쓸지 정합니다(`python3` 또는 `kdenlive_render`, 그리고 특수값 `spoof`). table 묶음이 하나뿐인 batch-loop 항목은 `program` 없이 그 하나를 씁니다(`compiler.py`의 `_batch_loop` docstring).

## 2.6 spawn 항목의 부품: FORK, spawn table, chain

process를 여럿 만드는 항목은 셋입니다. `build-orchestrator`, `module-build-orchestrator`, `game-task-chain`. 앞의 둘은 FORK를, 마지막 하나는 compile 시점의 constructor를 씁니다.

**spawn table과 FORK.** interpretation-contract §5의 FORK 규칙은 이렇습니다. 부모의 program은 미리 뽑아 둔 순서 있는 **spawn table**(자식 하나하나의 완전히 풀린 program 목록)을 가지고, 실행 중 FORK를 만날 때마다 표의 다음 자식을 만듭니다. "*Which* children exist and *what they do* is compile-time; *when* each arrives is emergent." 어떤 자식이 무엇을 할지는 compile 때 정해지고, 언제 생기는지만 실행 중 scheduling으로 정해집니다. 부모는 **`fork_cap`**(살아 있는 자식 수의 상한)에 닿으면 자리가 날 때까지 FORK에서 멈춥니다. 이것이 `make -j8`의 job slot을 흉내 냅니다.

**object job과 structural step.** `build-orchestrator`의 자식 단위는 process 하나가 아니라 **object job** 하나입니다. Linux kernel을 build할 때 `make`가 `.c` 파일 하나를 `.o`로 만드는 일은 실제로 process 여섯 개가 차례로 하는 일입니다. `sh`(make가 띄운 shell) → `gcc`(compiler driver) → `cc1`(실제 compiler) → `as`(assembler) → `fixdep`(의존성 정리) → `rm`(임시 파일 삭제). 이 library는 이 여섯을 spawn table의 연속한 여섯 항목으로 적고, 서로 WAIT/WAKE로 이어 원래의 부모–자식 순서대로 깨어나게 합니다. 각 process가 도는 횟수는 **structural step**(자기 자식이 forked되고 끝나는 경계로 나뉜 구간)으로 셉니다. `sh`는 넷, `gcc`는 셋, 나머지는 하나입니다. 그래서 `compiler-child`의 params는 `sh_step_1` … `sh_step_4`, `gcc_step_1` … `gcc_step_3`, `cc1_step_1`, `as_step_1`, `fixdep_step_1`, `rm_step_1`의 열한 table입니다. `fork_cap`은 timeline의 `parallelism_cap`(job 수) × 6(job당 process 수)입니다. cap 8이면 48입니다(6장).

`module-build-orchestrator`(DKMS module build)는 같은 생각을 job 종류 넷으로 넓힙니다. 자식 항목 `module-compiler-child`의 `pattern.trees`가 네 종류의 job tree를 적습니다.

```yaml
trees:
  object:     {sh: [{gcc: [cc1, as]}, fixdep, rm]}
  kprobe:     {sh: [mkdir, {gcc: [cc1, as]}, rm]}
  conftest_a: {sh: [{csh: [dirname, {gcc: [cc1]}, rm, tsh1, tsh2]}]}
  conftest_b: {sh: [{csh: [dirname, {gcc: [cc1, as]}, rm, rm2, tsh1, tsh2]}]}
letters: {o: object, p: kprobe, c: conftest_a, C: conftest_b}
names:   {gcc: x86_64-linux-gn, csh: sh, tsh1: sh, tsh2: sh, rm2: rm}
```

tree의 node는 member id이거나 `{member id: [자식들]}`입니다. object와 kprobe job은 member 여섯, conftest_a는 여덟, conftest_b는 열입니다(tree를 세어 확인). `names`는 member id를 실제 comm으로 바꿉니다(예: `gcc` member는 `x86_64-linux-gn`으로 보입니다 — `x86_64-linux-gnu-gcc-13`의 앞 15글자). params는 (job 종류, member, step)마다 하나씩 56개 table입니다.

부모 `module-build-orchestrator`의 `pattern.job_order`는 실제 build가 job을 돌린 순서를 **run-length**로 적은 문자열입니다. `"p21 C2 c1 p4 …"`는 "kprobe 21개, conftest_b 2개, conftest_a 1개, kprobe 4개, …"라는 뜻입니다. 문자열 전체를 더하면 kprobe 1,125, object 200, conftest_a 145, conftest_b 87, 합계 1,557 job입니다(python으로 세어 확인). 이 순서로 spawn table을 만들면 member는 200×6 + 1,125×6 + 145×8 + 87×10 = 9,980개가 되고, 실제로 compile된 `c7-compile`의 `dkms` task는 spawn table 9,980개와 `fork_cap` 48을 가집니다.

**chain constructor.** `game-task-chain`은 FORK를 쓰지 않습니다. compiler가 compile 시점에 task 하나를 `chain_length`(16)개의 game member와 `wineserver` member 하나, 모두 17개의 보통 task로 펼칩니다(interpretation-contract §6, "Constructor specialization — chain topology"). 첫 member(머리)는 `TIMER frame_period`로 깨어나고, 나머지는 앞 member의 WAKE로 깨어나 일하고 다음 member를 깨웁니다. member 이름은 timeline이 `member_names`로 줍니다(4.1절).

## 2.7 `validation_stats`와 `modeling_notes`

**`validation_stats`**는 네 field를 가집니다.

- `referee`: 이 항목을 판정할 기준 관측. 28개 measured 항목은 `meas-ci`(우리 측정)이고, `game-task-chain`만 `none`입니다. `none`일 때는 `reason`을 적어야 합니다.
- `run`: 어느 campaign의 몇 번째 repeat들이고, GitHub Actions의 어느 run id들인지. 예: `"interactive:2026-09-18, repeats [1, …, 14], runs 35341238784, …"`.
- `stats`: 이 항목이 맞춰야 하는 요약 통계. 예: `office-writer`의 `"idle wakes/s 3.4–3.5"`, `"driven cpu-share 0.0059–0.0140"`, repeat마다의 `input_run` 중간값 목록.
- `scope`: 이 측정이 정확히 무엇이었는지 적는 긴 산문입니다. 어떤 프로그램의 어떤 build를, 어떤 문서·입력·설정으로, 어떤 machine에서, 몇 번 반복해 쟀고, 어떤 값이 stability rule을 통과하지 못해 예외로 실렸고, 이 값이 무엇을 주장하지 않는지까지 담습니다. 항목에 대해 가장 최신이고 가장 완전한 설명이 바로 이 scope입니다.

**`modeling_notes`**는 "출처 위에 우리가 지어낸 것"을 적습니다. 머리 주석의 규칙은 "what our encoding invented on top of the sources"이고, `dataset/sources.yaml` 머리 주석의 짝 규칙은 registry의 `notes`가 "what the source establishes and its scope limits — never our modeling on top of it (that lives in archetypes.yaml `modeling_notes`)"라는 것입니다. 두 문서를 합치면 "출처가 말한 것"과 "우리가 만든 것"이 깔끔히 갈립니다. archetype-plan §5는 이 둘을 "together they are the paper-writing guardrail against over-claiming"이라고 부릅니다. 논문을 쓸 때 출처가 말하지 않은 것을 출처의 말처럼 쓰지 않게 막는 난간이라는 뜻입니다.

measured 항목의 `modeling_notes`에는 거의 항상 같은 문단이 두 개 들어갑니다. 하나는 이 항목이 어떻게 task 하나로 compile되는지(9.5 D2, D9, D14, D16, D17, D74 등의 요약), 다른 하나는 **untraced control**의 결과(측정 도구 `perf`를 켠 것 자체가 값을 얼마나 바꿨는지, 3.6절)입니다.

## 2.8 source tag 읽는 법

source tag는 `<id>` 또는 `<id>:<locator>`입니다. `id`는 `dataset/sources.yaml`의 key이고, `docs/references.md`가 그 id의 정식 인용 정보를 가집니다. linter는 두 파일이 맞는지 확인합니다. sources.yaml의 모든 id는 references.md에 `` ### `<id>` `` 제목으로 있어야 합니다("subset lint").

`dataset/sources.yaml`에는 2026-10-17에 19개 id가 있습니다(scholarly 5, deployed-system 11, talk·학회 초록·뉴스 보도 1, measurement 2; python으로 세어 확인). 2026-10-16에 데이터셋 파일 어디도 인용하지 않는 id 열한 개가 빠졌습니다(그 전에는 30개). type은 넷입니다.

- `scholarly`: 학술 문헌(번호 붙은 참고문헌). 경험적·통계적 주장을 받칠 수 있습니다.
- `deployed-system`: 제품·프로젝트 문서(각주). 존재 주장("this scenario/setting/category exists in shipped software"), 그 시스템이 스스로 문서화한 설계나 동작(그 판의 그 출처의 말로), 그 출처가 공개한 숫자(그 출처의 보고로)를 받칠 수 있고, 행동·통계 주장을 논문 자신의 것이나 모집단의 것으로 받치지는 못합니다.
- `talk, conference abstract or news report`: 발표, 학회 초록, 뉴스 보도(각주). 그 주장은 발표자나 기자의 것으로만, 숫자는 그 보고로 날짜와 함께 받칩니다. `lavd-ossna24` 하나.
- `measurement`: 우리 측정. `meas-ci`와 자리표시자 `meas-pending` 둘.

talk·학회 초록·뉴스 보도 type은 9.12 D113이 정했고, 2026-10-16에 9.15가 `docs/references.md`에 적용했습니다. registry는 2026-10-17부터 따릅니다(9.15에서 인지오의 답). 그때 `lavd-ossna24`의 `type`이 `deployed-system`에서 이 type으로 바뀌었고, 머리 주석의 `type` 규칙도 id 규칙의 네 type과 등급 규칙의 문장(줄여 옮긴 것)으로 다시 적혔습니다. 그 전의 머리 주석은 type 셋만 적었습니다.

이 구분은 `docs/references.md`의 **citation-tier rule**(인용 등급 규칙)에서 오고, `docs/workload/grounding-sources.md`가 같은 규칙을 이렇게 옮깁니다. "a deployed-system citation supports existence claims …; the system's own documented design or behaviour, stated as that source's at its pinned version or accessed date; and a figure the source publishes, stated as its report with the date read, the window and how it is computed — never a behavioural or statistical claim stated as the paper's own or as a population's. A talk's, conference abstract's or news report's claims are the speaker's or reporter's, a number stated only as its report with its date." deployed-system 등급을 이렇게 넓힌 것은 9.12 D112입니다(2026-10-16에 9.15가 적용).

**locator**는 출처 안의 위치입니다. sources.yaml의 항목이 `locator_pattern`(정규식)을 가지면 linter가 locator를 그 정규식으로 검사합니다. archetype library에 쓰이는 tag는 다음 셋 종류입니다(library 전체를 python으로 훑어 모은 목록).

| tag 모양 | 뜻 | 예 |
|---|---|---|
| `meas-ci:<workflow>:<campaign>` | 우리 CI 측정 campaign. workflow는 측정 workflow 이름, campaign은 첫 batch를 띄운 날짜(같은 날 두 번째 campaign이면 글자 하나를 붙임) | `meas-ci:interactive:2026-09-18`, `meas-ci:background:2026-10-02b` |
| `swell-icmi14:<app>-c<n>` | SWELL-KW 녹화의 application과 실험 조건 | `swell-icmi14:word-c1`, `swell-icmi14:outlook-c23` |
| `lavd-ossna24:s<n>` | LAVD 발표 자료의 slide 번호 | `lavd-ossna24:s12`, `lavd-ossna24:s13` |
| `steamos-refresh` | locator 없는 deployed-system 출처 | `game-task-chain.frame_period` |

`meas-ci`의 locator 정규식은 `^[a-z0-9_-]+:(\d+|\d{4}-\d{2}-\d{2}[a-z]?)$`입니다. 날짜 대신 숫자가 오는 꼴(`meas-ci:cli:3`)은 campaign 형식이 정해지기 전(2026-09-18 이전)의 한 번짜리 run을 가리키는데, 지금 library에는 그런 tag가 남아 있지 않습니다. 이 형식은 9.5 D27(2026-09-18, "the `meas-ci` locator names the campaign")이 정했고, 기록된 이유는 campaign 하나가 여러 run에 걸치게 되었기 때문입니다("first batch, repeats added one at a time, retries after the machine gate").

library에 쓰인 workflow는 여섯입니다. `interactive`(9.5의 typing·편집 application), `playback`(9.5의 재생·통화), `build`(9.6의 kernel build), `background`(9.7과 9.10의 batch job들), `desktop`(9.8의 browser 조각·comms, 9.10의 launch와 tab 수), `session`(9.9의 desktop session process).

**design, convention, arithmetic.** 출처가 말하지 않은 값은 source tag를 달지 않고, 그 값이 무엇인지 이름표를 붙입니다. Phase 9 decision 1(검증 기준, 2026-09-13)의 문장입니다. "A value no source states carries no source tag and is labelled for what it is: convention, arithmetic, placeholder, or design." 다만 데이터셋에는 `placeholder` 이름표가 없습니다. 측정을 기다리는 값은 `meas-pending` tag를 달고 freeze가 그것을 거부합니다(2.10절; 2026-10-16, 인지오의 결정). archetype library에서는 이 이름표가 field가 아니라 `modeling_notes`나 `scope` 산문 안에 적힙니다(예: `game-task-chain`의 "16667 us is 1/60 s arithmetic — design, ours"). timeline 쪽에서는 bound value마다 `source:` 지도에 tag 또는 이름표(`design`, `convention`, `arithmetic`)를 직접 적고, linter가 확인합니다(9.10 D32, linter의 `BOUND_LABELS`). 예를 들어 `c1-compile`은 `source: {spawn_count: "meas-ci:build:2026-09-18", parallelism_cap: convention, child_name: "meas-ci:build:2026-09-18"}`라고 적습니다.

> **왜 이렇게 정했나 — `parallelism_cap` 8은 `convention`.** 9.6 D4(compile 조각의 `-j`와 cap 기본값을 정한 결정, 2026-09-17, 인지오의 결정)는 이 값을 desktop의 `nproc` 규칙을 8-thread desktop에 적용한 관례로 적습니다("Label: convention, grounds cited for the choice"). `build-orchestrator`의 `modeling_notes`도 같습니다. 2026-10-06의 9.10 D160(core set timeline이 묶는 값을 출처 tag나 이름표와 함께 나열한 결정, 위임으로 내린 것)은 compile의 cap을 `design`으로 적고 그 근거로 9.6 D4를 들었습니다. 나열의 인용은 따로 결정을 담지 않으므로 이름표는 9.6 D4를 따라 `convention`입니다(9.16의 `decisions.md`, 질문 없이 정한 항목). 2026-10-17에 timeline의 `source:` 지도, 9.10의 `bound-values.md`, 생성 층이 `convention`으로 바뀌었습니다. 값(8)은 같으므로 compile된 workload는 바뀌지 않습니다.

## 2.9 한 항목을 끝까지 따라가기: `office-writer`

이제 실제 항목 하나를 yaml에서 compile된 workload까지 따라가 보겠습니다. 가장 작은 typing 항목인 `office-writer`(LibreOffice Writer)를 고릅니다. component가 하나뿐이라 손으로 따라가기 좋습니다.

### 1단계: 항목을 읽는다

```yaml
office-writer:
  category_source: meas
  declared_class: normal
  pattern:
    program:
      - loop:                  # merged event stream … (D9): replayed stimulus in focus windows (D18) + timer components (D16)
          - WAIT: input
          - RUN: event
  params:
    launch:    {stream: launch-office-writer, sampling: per-task, source: "meas-ci:desktop:2026-10-04b"}
    input_run: {dist: quantiles, p: [2049, 2364, 2532, 2850, 3230, 6328, 9551, 10167, 11367, 62153],
                min: 0, max: 194092, means: [...], sampling: per-iteration, source: "meas-ci:interactive:2026-09-18"}
    stimulus:  {stream: swell-word-c1, kinds: [key], sampling: per-task, source: "swell-icmi14:word-c1"}
    components:
      - comm: "soffice.bin"
        threads: 1
        wakes_per_s: 3.4571
        gap: {dist: quantiles, p: [245, 314, 357, 386, 110223, 600682, 600693, 600706, 600718, 600754], min: 121, max: 998153, ...}
        run: {dist: quantiles, p: [21, 25, 25, 27, 70, 311, 339, 355, 389, 429], min: 15, max: 468, ...}
  lifetime: segment-bound
  binding_params: []
  scalable: []
```

한 줄씩 풀면 이렇습니다.

- 이 항목은 우리 측정에서 온 행동 부류이고(`meas`), 보통 class입니다(`normal`).
- program은 "무언가를 기다리고(`WAIT`), 깨면 일한다(`RUN`)"의 반복입니다. 주석이 말하듯 이 loop는 compile 때 두 종류의 wake(재생된 key 입력과 측정된 timer)를 합친 명시적 사건열로 펼쳐집니다.
- `input_run`: key 하나에 Writer 전체가 쓰는 CPU. 중간값 3.23 ms, 99번째 percentile 11.4 ms. 표 전체의 평균은 `sampling.mean_us`로 계산하면 4,906.7 μs, 약 4.9 ms입니다.
- `stimulus`: SWELL-KW의 Word 녹화, key만.
- `components`: `soffice.bin` thread 하나. 초당 3.4571번 깨어나고, gap 표가 특이합니다. p1–p25가 245–386 μs이고 p75 이상이 약 600.7 ms입니다. 즉 Writer는 약 0.6초 간격으로 깨어나는데, 깰 때 0.3–0.4 ms 간격으로 몇 번 연달아 깹니다. gap 표의 평균은 289,261 μs이고, 1초를 이 값으로 나누면 3.4571입니다(`wakes_per_s`와 정확히 일치. 9.5 D71이 "a component's gap table implies its measured wake rate"를 test로 지키게 했습니다). run은 중간값 70 μs, 최대 468 μs로 짧습니다.
- `segment-bound`, 손잡이 없음, scaling 없음.

### 2단계: timeline이 이 항목을 부른다

core set의 `c1-office` 파일(`dataset/timelines/coreset/c1-office.timeline.yaml`. `c1-`은 C1 그룹, 즉 한 가지 상황만 60초 동안 보여 주는 calibration 그룹의 파일이라는 뜻입니다)은 이렇게 적습니다.

```yaml
meta: {id: c1-office, seed: 101, demand: calibration}
tasks:
  - {id: writer, name: soffice.bin, archetype: office-writer, arrive: 0s, depart: 60s}
  - {id: browser, name: chrome, archetype: web-browser, arrive: 0s, depart: 60s}
  - {id: renderers, name: chrome, archetype: renderer-hidden, arrive: 0s, depart: 60s, count: 4, ...}
  - {id: mail, name: thunderbird-bin, archetype: mail-client, arrive: 0s, depart: 60s}
input:
  - {from: 2s, to: 58s, task: writer}
focus:
  - {from: 0s, to: 60s, task: writer}
```

`writer` task는 0초에 와서 60초에 떠나고, 2초부터 58초까지 사용자가 타이핑합니다(`input` 창). 0초에 왔으므로 launch phase는 재생하지 않습니다.

### 3단계: compiler가 사건을 뽑는다

compiler(`compiler.py`의 `_measured_unroll`)는 다음을 합니다.

1. **timer wake**: `soffice.bin` component 하나에 대해, 0초부터 60초까지 "이미 돌고 있던 흐름"의 첫 gap을 뽑고, 이어서 gap을 하나씩 뽑으며 wake 시각을 만듭니다. wake마다 run을 하나 뽑습니다. 60초 × 3.4571/s ≈ 207개를 기대할 수 있습니다.
2. **input wake**: `input` 창 2–58초, 56초 길이에 대해, `swell-word-c1` 녹화에서 seed가 정한 위치부터 56초 분량의 key 시각을 잘라 옵니다. key마다 `input_run`을 뽑습니다(0이 나오면 RUN 없이 WAIT만 둡니다).
3. 두 목록을 시간순으로 합치고, 각 wake를 `WAIT timer:writer` 또는 `WAIT input:writer`와 그 뒤의 `RUN`으로 바꿉니다. 그리고 각 wake 시각에 외부 `wake` 사건을 하나씩 만듭니다.

### 4단계: 결과를 열어 본다

compile된 `dataset/build/coreset-single/c1-office.workload.json`을 python으로 열어 `writer` task를 세면 이렇습니다(2026-10-14 local build).

- program: `WAIT` 475개와 `RUN` 475개.
- wake 사건: `input:writer` 270개, `timer:writer` 205개. timer wake 205개는 위의 기대치 약 207개와 맞습니다. key 270개는 56초 동안 초당 약 4.8개입니다.
- RUN의 합: 1,358,623 μs, 약 1.36초. 60초 중 약 2.3 %입니다.

program의 앞부분은 이렇게 생겼습니다.

```
WAIT timer:writer, RUN 248, WAIT timer:writer, RUN 357, WAIT timer:writer, RUN 152,
WAIT timer:writer, RUN 317, WAIT timer:writer, RUN 355, WAIT timer:writer, RUN 280,
WAIT timer:writer, RUN 21,  WAIT timer:writer, RUN 321,
WAIT input:writer, RUN 3117, WAIT input:writer, RUN 10152, ...
```

그리고 wake 사건의 첫 부분은 이렇습니다(μs).

```
302832 timer:writer
892899 timer:writer
893285 timer:writer
893671 timer:writer
894057 timer:writer
1387227 timer:writer
...
2059422 input:writer
2059422 input:writer
```

892,899 / 893,285 / 893,671 / 894,057 μs의 네 wake가 386 μs 간격으로 붙어 있는 것이 보입니다. gap 표의 짧은 쪽(245–386 μs)이 바로 이 몰아 깨기입니다. 또 2,059,422 μs에 input wake가 두 번 같은 시각에 있습니다. 우리가 추출한 SWELL-KW stream에서 timestamp가 15.6 ms 격자에 떨어져, 같은 시각으로 기록된 key가 있기 때문입니다(9.5 D12: "7 % zero gaps"). 이 격자는 stream에 대한 우리의 읽기이고, 읽은 SWELL-KW 자료는 timestamp의 해상도를 말하지 않습니다.

simulator는 이 task를 이렇게 실행합니다. 0.30초에 timer wake가 오면 runnable이 되어 248 μs를 쓰고, 다음 WAIT에서 멈춥니다. 2.06초에 key가 오면 3,117 μs를 쓰려 하는데, 그때 browser나 mail이 CPU를 쓰고 있으면 기다리게 됩니다. 이 기다림(ready wait)이 이 연구가 재는 지연입니다. 실제로 core set의 scoring spec은 `c1-office`의 항목으로 `{entity: writer, metric: ready_wait, cause: wake, channel: input, aggregate: p99, …}`를 둡니다(`harness/scoring/scoring-spec.yaml`). key 입력으로 깨어난 writer가 CPU를 기다린 시간의 99번째 percentile을 점수로 삼는다는 뜻입니다.

### 5단계: 숫자의 뒷이야기

이 숫자들의 출처는 `validation_stats`와 `scope`가 말합니다. LibreOffice 24.2.7.2(Ubuntu 24.04 apt)로, 약 76쪽짜리 생성 문서(100개 절 × 100단어 문단 다섯 개, 1024×768 그림 열 장; 길이를 정한 출처는 없어 design) 끝에 타이핑하며, GitHub-hosted ubuntu-24.04 runner(4 vCPU AMD EPYC 7763, kernel 6.17.0-1022-azure)의 CPU 하나에 process tree를 묶어, Xvfb 1280×800(화면 refresh, GPU, 소리 장치 없음) 아래에서 `perf sched record`로 14번 repeat를 쟀습니다. key는 xdotool로 녹화된 시각에 재생했고(재생 오차 p99 1.24 ms), click·scroll·drag는 빼서 타이핑이 문서 끝에 머물게 했습니다(9.5 D28). 자세한 이야기는 5.2절에서 합니다.

## 2.10 lint가 지키는 규칙

`make lint`(`dataset/tools/lint.py`)와 `make test`(`dataset/tools/tests/`)는 항목에 여러 규칙을 겁니다. archetype 쪽 규칙은 `dataset/tools/wlc/linter.py`의 `lint_repo` 함수에 모여 있습니다. 하나씩 적습니다.

**필수 field.** `REQUIRED_ARCHETYPE_FIELDS`의 아홉 field(2.2절)가 없으면 `"<id>: missing field '<field>'"` 오류입니다. `declared_class`가 여기 들어 있으므로, **declared class 없는 항목은 lint를 통과하지 못합니다**. 기본값도 없습니다. test `test_repo_lint_requires_declared_class`가 이것을 확인합니다(9.13 spec decisions 2와 8).

**닫힌 값 목록.** `lifetime`은 `segment-bound`, `finite`, `spawned` 중 하나, `declared_class`는 `normal`, `idle` 중 하나(`DECLARED_CLASSES`; 주석 "widened only when an entry carries batch or real-time work"), `sampling`은 세 값 중 하나여야 합니다.

**spawned에는 부모.** `lifetime: spawned`이면 `spawned_by`가 있어야 합니다.

**component 모양.** `components`와 `focus_components`는 비어 있지 않은 목록이어야 하고, 각 component는 `comm`, `gap`, `run`을 가져야 합니다. `operations`는 비어 있지 않은 map이어야 하고, 각 operation은 `duration`과 비어 있지 않은 `components`를 가져야 합니다. `heavy_events`의 각 사건은 `comm`, `count`, `span_s`, `rate_per_s`, `run`을 가져야 하고, `gap`을 가지면 오류입니다.

**파일이 있어야 하는 부품.** `stimulus`의 `stream`은 `dataset/stimulus/<stream>.jsonl`로, `launch`의 `stream`은 `dataset/launch/<stream>.json.gz`로, `replay`의 `stream`은 `dataset/replay/<stream>.json.gz`로 실제 파일이 있어야 합니다. `stimulus`의 `kinds`는 `key`, `click`, `wheel`, `drag` 중에서만 고를 수 있습니다.

**숫자마다 출처.** 모든 distribution object는 `source`를 가져야 하고(없으면 "numeric param without source tag"), tag의 id는 sources.yaml에 있어야 하며, locator는 그 id의 `locator_pattern`에 맞아야 합니다. locator_pattern이 없는 id에 locator를 붙여도 오류입니다.

**quantile table의 모양.** `p`는 정확히 열 개, 음수가 아니고, 줄어들지 않아야 합니다. `min`, `max`, `means`는 셋이 함께 있거나 셋 다 없어야 하고, `min ≤ p1`, `max ≥ p99.9`, `means`는 열한 개이며 각 평균은 자기 구간 안에(1 μs 여유로) 있어야 합니다(`_check_table_extremes`, 주석 "the fidelity fix").

**registry 정합.** sources.yaml의 모든 id는 references.md에 있어야 합니다.

**`meas-pending`은 0개.** `meas-pending`은 "CI 측정을 기다리는 자리표시자"라는 뜻의 sentinel tag입니다. 원래 설계에서는 schema freeze 뒤에 linter가 이것을 거부하기로 되어 있었습니다(sources.yaml: "the linter rejects it after the schema freeze"). 이 규칙은 `lint_repo(..., freeze=True)`로 켜지고, 2026-10-15의 9.23 D13부터 `make lint`가 `lint.py --freeze`로 돌아 library의 숫자에 `meas-pending`이 하나라도 있으면 실패합니다("meas-pending after freeze"). 2026-10-16부터는 freeze가 timeline의 bound value에도 적용됩니다(`lint_bound_sources`). `make test`의 `test_repo_is_freeze_clean`과 `test_real_timelines_are_freeze_clean`도 실제 repository를 freeze로 lint합니다. `dataset/README.md`의 규칙 문장은 "A value awaiting a measurement campaign is tagged `meas-pending`; `make lint`'s freeze rejects the tag in the library's parameters and in the timelines' bound values. The library holds none"입니다. 확인: 2026-10-17에 `grep -c meas-pending dataset/archetypes.yaml`은 1을 돌려주는데, 그 한 줄은 머리 주석의 설명문입니다. 숫자에 붙은 `meas-pending`은 없습니다.

**timeline 쪽 규칙(참고).** archetype 자체의 규칙은 아니지만, timeline이 archetype을 부를 때의 규칙도 있습니다. timeline은 archetype의 `binding_params`에 있는 이름만, 빠짐없이 넣어야 하고(`wlc/timeline.py`), 넣은 값마다 source tag 또는 `design`/`convention`/`arithmetic` 이름표를 달아야 합니다(`lint_bound_sources`, 9.10 D32와 9.18). 이 부분은 timeline을 다루는 권에서 자세히 다룹니다.

> **코드로.** compile 단계의 canonical lint에는 archetype과 관련된 규칙이 하나 더 있습니다. **TIMER-first**: TIMER를 어디든 가진 program은 첫 실행 명령이 TIMER여야 합니다(LOOP 머리의 body도 머리로 침). 9.13 spec decision 8이 정했고, `linter.py`의 `_timer_first_violation`이 검사합니다. 재생 항목(`_periodic_unroll`)과 game chain 머리가 모두 TIMER로 시작하므로 통과합니다.

## 2.11 `dataset/` 안의 이웃 파일들

archetype 항목이 가리키거나, archetype 측정과 관련된 파일들이 `dataset/` 안에 몇 군데 있습니다. 무엇이 어디 있는지 정리합니다.

| 경로 | 무엇 | 누가 읽나 |
|---|---|---|
| `dataset/stimulus/swell-*.jsonl` | 재생할 key 녹화 세 개(`{"t_us", "kind"}` 줄) | compiler(`_load_stream`), linter |
| `dataset/stimulus/streams.json` | 위 stream들을 어느 SWELL-KW 파일에서 어떤 규칙으로 만들었는지(조건, 파일 목록, "2000 ms per segment or file boundary") | 사람 |
| `dataset/launch/launch-<entry>.json.gz` | launch phase 녹화 열 개(repeat마다 phase 길이와 wake 목록) | compiler, linter |
| `dataset/replay/replay-*.json.gz` | trace-replay 변형용 관측 흐름 여섯 개(`code-editor`, `cpu-batch-python3`, `package-upgrade`, `renderer-hidden`, `video-call`, `web-browser`) | compiler(`variants.yaml`의 `replay` 집합이 쓸 때만) |
| `dataset/meas/streams/` | 측정 campaign이 repeat마다 재생한 600초 key 창들(`word-r<k>.jsonl` 56개, `ie-r<k>` 38개, `outlook-r<k>` 8개, `aalto-r<k>` 78개)과 창 선택 기록(`windows.json`, `aalto-windows.json`) | 측정 도구(`dataset/tools/meas/loop/pool_runs.py` 등) |
| `dataset/meas/names/` | 재구축 이전의 이름을 검증한 Phase 2와 Phase 7의 기록(`meas-ci:names:2`, Ubuntu·Fedora·Arch에서 이름이 실제로 그렇게 보이는지; `run-2/`는 dkms run). 역사로 남음. 지금 이름의 근거는 campaign이 추적한 `comm`(9.10 D25) | 어떤 도구도 읽지 않음 |
| (`dataset/meas/summary.json`) | Phase 2(2026-08-28)의 옛 CLI·GUI 측정 요약. 2026-10-16에 지워짐(commit `37c2e233`; 그 전 commit에서 읽을 수 있음) | 어떤 도구도 읽지 않았음. 지금 library의 어떤 값도 이것에서 오지 않음(11장) |

`dataset/meas/streams/`의 이름 때문에 헷갈리기 쉽습니다. 여기 있는 것은 compile된 workload의 wake 흐름이 아니라, **측정할 때 application에 재생해 준 입력 창**입니다. 9.5 slice는 SWELL-KW 녹화를 600초 창으로 잘라 repeat k가 k번째 창을 재생하게 했습니다(9.5 D12: "repeat r replays the r-th 600 s window of recorded time … `dataset/meas/streams/<app>-r<r>.jsonl`, committed"). `aalto-r<k>`는 stimulus 민감도 검사(3.6절)에 쓴 136M Keystrokes 데이터의 창입니다. 그래서 `word-r*` 파일 수(56)가 Word 녹화의 창 수이고, `code-editor`가 44번째 창에서 멈춘 이야기(5.3절)가 이 파일들과 이어집니다.

측정 도구의 지도는 `dataset/tools/meas/README.md`입니다(2026-10-16에 9.15가 씀). 하위 폴더와 도구마다 campaign 계열, 단계(run, 분석, pool, fold-in), 입구를 적고, 각 도구의 docstring이 말하지 않는 것은 주장하지 않습니다. 측정 방법은 각 slice의 `campaign/method.md`, `_dev/research/jioh/measurement-campaign-workflow.md`, `docs/workload/measurement-overview.md`가 설명하고, 측정 방법을 다루는 6권이 이것을 모아 설명합니다. `dataset/meas/`에는 README가 없고, `dataset/README.md`의 Layout이 그 안의 것을 적습니다.

# 3장 · 숫자는 어떻게 얻었나 — tag를 읽을 만큼만

이 장은 "`meas-ci:interactive:2026-09-18`이라는 tag 뒤에 무엇이 있나"에 답합니다. 28개 항목의 숫자가 모두 이런 tag를 달고 있으므로, tag가 무엇을 약속하고 무엇을 약속하지 않는지 알아야 4장부터의 숫자를 바르게 읽을 수 있습니다. 측정 방법 전체와 검증 기준(값이 원 자료에서 다시 나오는지, 출처가 원문과 맞는지)은 측정 방법을 다루는 6권이 자세히 다룹니다. 이 장은 tag를 읽는 데 필요한 만큼만 설명합니다. 기준 문서는 `docs/workload/measurement-overview.md`(측정 개요; status draft, 2026-09-29 작성, 2026-10-17 갱신)와 `dataset/sources.yaml`의 `meas-ci` notes입니다. measurement-overview의 항목 표(§2)는 2026-10-17에 9.15가 다시 써서 지금 library의 measured 항목 28개를 담습니다. 이 권을 처음 쓴 2026-10-14에는 그 표가 2026-09-28에서 멈춰 23개 항목을 세고, `file-backup`, `renderer-visible`처럼 이미 없는 항목을 담고 있었습니다.

## 3.1 CI runner 측정 한 번의 모양

**CI runner**는 GitHub Actions가 workflow를 돌려 주는 가상 machine입니다. 이 repository는 측정 workflow(예: `.github/workflows/meas-interactive.yml`)를 손으로 띄워, runner 위에서 실제 프로그램을 설치하고 돌리며 scheduler trace를 녹화합니다. 웹 개발자에게 익숙한 CI job과 같은 것인데, test를 돌리는 대신 프로그램의 CPU 사용을 녹화한다는 점만 다릅니다.

측정 job 하나는 대략 이렇게 생겼습니다(measurement-overview §3).

```
실제 프로그램 + 현실적인 입력
  → 새 GitHub runner 위의 job 하나   (machine gate, CPU 하나에 고정, settle, phase들, perf sched record)
  → repeat마다 분석                  (wake, run, gap, thread별 component)
  → repeat들을 모음(pool)             (stability rule이 언제 멈출지 정함)
  → archetypes.yaml에 fold-in         (quantile table과 비율; scope와 반폭을 적음)
  → wlc가 task마다 사건열을 뽑음       (seed로, byte까지 같게)
```

몇 가지 장치를 설명합니다.

- **runner**: GitHub-hosted `ubuntu-24.04`, vCPU(가상 machine이 받은 가상 CPU) 4개(`gh-hosted-runners`). 측정할 process tree는 그중 CPU 하나에 고정(**pin**)하고, 측정 도구·입력 재생기·보조 서버(웹 페이지 서버, 메일 서버 역할의 peer, Matrix homeserver)는 나머지 CPU에서 돕니다. 이것은 simulator가 CPU 하나(lane 하나)를 흉내 내기 때문입니다(9.5 follow-ups spec decision 2: "The observation is the application on one CPU … matching the simulator's single lane").
- **`perf sched record`**: Linux 커널의 scheduler 사건(schedule-in/out: task가 CPU에 올라가는/내려오는 순간; wakeup; fork; exit)을 녹화하는 도구입니다. 이 녹화에서 thread마다 언제 깨어나 얼마나 돌았는지 읽습니다. batch 계열은 여기에 **taskstats**(process가 끝날 때 커널이 넘겨주는 CPU·대기 시간 회계)를 더해 두 도구가 서로를 검산하게 했습니다(9.6 D3).
- **Xvfb**: 화면 없는 가상 X server입니다. runner에는 모니터도 GPU도 소리 장치도 없으므로, GUI 프로그램은 Xvfb 위에서 돌았습니다. 이것이 measured 값의 큰 한계 하나입니다(12장).
- **settle**: 프로그램을 켠 뒤 측정을 시작하기 전에 기다리는 시간입니다. 켜진 직후의 바쁜 일(launch work)이 안정 상태 값에 섞이지 않게 하려는 것입니다. 9.5 D34(2026-09-19)가 "the idle phase starts after the application's launch work ends"를 정했고, 길이는 프로그램마다 다릅니다(Chrome 420초, Thunderbird 390초, 통화 210초, Steam client 900초 등). launch work가 끝나는지 되풀이되는지 trace만으로 알 수 없으면 먼저 긴 **long-phase probe**(1,400–3,600초짜리 탐침 측정)를 돌려 정했습니다(9.5 D35).
- **phase**: job 안의 측정 구간입니다. 이름이 여럿입니다. `idle`(입력 없음), `driven`(SWELL-KW 재생), `driven-alt`(민감도 검사용 다른 녹화 재생), `op`(operation 반복), `play`(재생), `steady`(배경 tab 등의 안정 상태), `shown`(Steam 창이 보이는 상태). 항목의 `stats`에 `idle wakes/s`, `driven cpu-share`처럼 phase 이름이 붙어 있는 이유입니다.

## 3.2 wake, run, gap, component의 정의

measurement-overview §5가 정의를 모읍니다.

- **wake**: thread가 마지막으로 잠든 뒤 wakeup 사건이 있었고 그다음에 오는 schedule-in. preemption 뒤의 재개는 wake가 아니며, 그 run은 앞의 wake에 합칩니다(9.5 follow-ups spec decision 4: "A resume after preemption is not a wake: its run is added to the preceding wake's run").
- **run**: wake 한 번의 CPU 시간.
- **gap**: 한 component의 합쳐진 wake 시각들 사이의 간격. 관측 구간을 한 바퀴 감싸서(마지막 wake에서 첫 wake까지도 하나의 gap) 계산하므로, gap 평균은 정확히 "구간 길이 / wake 수"이고, gap 표가 암시하는 비율이 측정된 비율과 같습니다(9.5 D71).
- **component**: process 역할 하나 안의 thread comm 하나(`chat-client`와 `game-client`는 9.8 desktop slice의 규칙대로 tree의 process들을 가로지른 thread comm 하나). wake 비율 순으로 phase wake의 95 %를 덮을 때까지 싣고, 나머지는 residual로 묶습니다. 모든 repeat에서 적어도 두 번씩 깨지 않는 component는 "sporadic"으로 보고만 하고 싣지 않습니다(9.5 D43). 단 sparse component(3.5절)로 싣는 예외가 있습니다.
- **table**: p1…p99.9의 열 percentile, 표본의 min과 max, 각 구간의 평균(2.3절).

## 3.3 repeat, campaign, machine gate

- **repeat**: 새 runner에서 도는 job 하나 전체. measurement-overview §3: "the level at which the largest random variation enters, and so the unit the rule counts." 같은 job 안의 표본이 아니라 job 하나가 반복 단위입니다.
- **campaign**: 한 측정의 모든 repeat. tag `meas-ci:<workflow>:<첫 batch를 띄운 날짜>`가 campaign을 가리킵니다. campaign의 원 자료는 GitHub release로 공개합니다(예: release `meas-ci-2026-09-18`, `meas-ci-background-2026-10-04`). `dataset/meas-releases.yaml`이 데이터가 인용하는 campaign 23개마다 그 release(하나 이상)와 각 asset의 SHA-256을 적고, `make lint`가 지도에 없는 tag를 실패시킵니다(2026-10-16). release는 campaign을 모을 때 손으로 만들고, GitHub이 workflow의 artifact를 지우는 90일이 지나기 전에 만듭니다(`gh-artifact-retention`).
- **landing**: 일부 기록(특히 DKMS campaign)은 job이 목표 machine에 내려앉아 완료된 것을 landing이라 부릅니다. 같은 repeat 번호가 두 번 landing한 경우도 모두 pool에 넣었습니다(9.10 D58: "repeats 7, 10 and 11 landed twice, every landing pooled").
- **machine gate**: runner의 CPU 모델이 AMD EPYC 7763이 아니면 job을 약 20초 안에, 아무것도 설치하기 전에 멈추는 장치입니다(`dataset/tools/meas/machine_gate.sh`). 멈춘 job은 repeat로 세지 않습니다.

> **왜 이렇게 정했나.** 9.6 D10(2026-09-18)이 machine gate를 만들었습니다. 기록된 이유는 같은 이름의 runner가 서로 다른 CPU를 준다는 것입니다. "GitHub-hosted runners guarantee the shape, never the processor." 첫 build 측정의 다섯 repeat 중 넷이 EPYC 7763, 하나가 Intel Xeon Platinum 8573C였는데, `cc1`의 process당 CPU가 Xeon에서 269 ms, EPYC에서 358–392 ms였습니다. measurement-overview §6은 `maricq-osdi18`("servers with supposedly identical parts" differ run to run)을 근거로 인용하고, Intel Xeon이 `cc1`을 0.72배, `fixdep`을 0.50배 시간에 돌린 측정을 덧붙입니다. EPYC 7763을 고른 이유는 가장 자주 나오는 모델이기 때문입니다(9.6 D11: 기록된 job 56개 중 26개). campaign별로 job의 약 50–59 %가 EPYC 7763을 뽑았습니다(`_dev/research/jioh/measurement-campaign-record.md`의 "Machine draws").

## 3.4 stability rule과 멈추는 규칙

repeat를 몇 번 할지는 **stability rule**이 정합니다. 문장은 `sources.yaml`의 `meas-ci` notes와 measurement-overview §6에 있습니다.

- fold-in이 싣는 **모든 값**(component마다 따로, 절대 component끼리 평균 내지 않음)에 대해, repeat들 사이 평균의 95 % t 신뢰구간 반폭이 평균의 5 % 이하, 또는 그 값이 작을 때는 1 μs 이하여야 합니다.
- 비율이나 점유율은 repeat별 값으로, 표는 표가 싣는 count-weighted 평균으로 읽습니다(9.5 D78; 반폭은 `cochran-st77`의 ratio estimator).
- 최소 다섯 repeat(9.5 D29, `kalibera-ismm13` §11: "We do not show counts of fewer than 5 executions as they could hardly be used to get the variance estimate right").
- repeat는 한 번에 하나씩(또는 pool이 예측한 크기의 batch 하나 뒤에 하나씩) 더하며, 모든 값이 통과하면 멈춥니다. 상한은 없습니다(9.5 D33).

> **왜 이렇게 정했나.** 5 %의 근거는 measurement-overview §6에 "design"으로 적혀 있습니다. "half the smallest effect reported as a comparison of carried values (the kernel build's 10 % between `-j8` and `-j1`)." 비교로 보고하는 가장 작은 효과(kernel build에서 `-j8`이 `-j1`보다 compile당 CPU를 약 10 % 더 씀, 9.6 D4·D9)의 절반이라는 뜻입니다. 1 μs는 trace의 해상도(`perf sched timehist`가 정수 μs로 찍음)입니다. 처음에는 9.5의 stimulus 민감도 검사를 5 %의 근거로 들었으나, 9.5 D81(2026-09-27)이 그 근거를 9.6의 `-j8`/`-j1` 차이로 바꿨습니다.

**멈추는 규칙의 대가.** 처음으로 통과한 순간 멈추면, 그 순간의 반폭은 낙관적입니다(우연히 좁게 나온 순간에 멈추기 쉬움). 9.5 D88(2026-09-28)은 이것을 simulation으로 재어 scope에 적기로 했습니다. 기록: 각 항목의 가장 넓은 값에서 simulation하면, 그 값이 기준선 0.5 %p 안에 있는 항목들에서 "stated 95 % interval covers the true mean in about 91–94 % of campaigns"이고 "the stopped mean leans by at most 0.2 %"입니다(`chow-aoms65`가 근거: 첫 통과에서 멈추는 순차 구간의 coverage는 점근적으로만 명목 수준에 닿음). 그래서 `office-writer`, `video-editor`, `audio-player`, `mail-client`의 scope에는 "the rule's stated 95 % interval covers the true mean in about 91–93 % of campaigns" 같은 문장이 들어 있습니다.

## 3.5 다섯 가지 예외 class

어떤 값은 repeat를 늘려도 반폭이 좁아지지 않습니다. 그 값의 흩어짐이 프로그램의 성질이 아니라 다른 데서 오기 때문입니다. 이런 값은 5 % 규칙 대신 다섯 예외 class 중 하나로, 반폭·범위·repeat 수를 scope에 적은 채 싣습니다(measurement-overview §7). 앞의 넷은 그 값이 실패하는 것을 본 뒤 인지오가 값마다 결정했고, 다섯째는 녹화 길이에서 저절로 따라옵니다. 공통 단서가 붙습니다. "no reported result may rest on a difference smaller than a stated half-width."

| class | 언제 | 예 |
|---|---|---|
| machine 따라 흩어짐 | runner의 디스크나 속도를 따라 움직임. 한 repeat 안의 모든 thread run 시간이 함께 움직이고 wake 비율은 1 % 안에서 유지됨 | `game-client`, `renderer-hidden`의 run 평균; `cpu-batch` `python3`의 block 값(9.6 D29, 9.10 D87) |
| session 사이에서 변함 | phase 길이만 한 창을 긴 run 하나 위에서 밀면 거의 안 변하는데 repeat 사이에선 크게 변함 | `code-editor`의 `utility/libuv-worker`(9.5 D57), `service-manager`의 pid 1, `message-bus`의 system bus |
| sparse component | phase당 몇 번밖에 안 깨어 흩어짐이 개수 자체의 것 | `renderer-hidden`의 residual(9.8 D27) |
| run 안의 드문 사건 | repeat 하나가 0–2번 잡는 사건 | `web-browser`의 `MemoryInfra`, `game-client`의 HTTP burst(heavy event로 따로 실음) |
| 녹화가 바닥남 | 재생할 녹화 창이 더 없음 | `mail-client`의 입력과 `send`(Outlook 녹화 창 8개), `web-browser`의 per-input 평균(IE 녹화 창 38개) |

## 3.6 검사들

값을 싣기 전후로 여러 검사를 했습니다(measurement-overview §8). 항목의 `scope`와 `modeling_notes`에 그 결과가 문장으로 들어 있으므로, 무엇을 검사했는지 알아 두면 그 문장들을 읽을 수 있습니다.

- **repeat별 유효성**: 재생이 창의 모든 사건을 보냈는가, operation이 모두 완료됐는가, 화면 캡처가 입력이 의도한 곳에 들어갔음을 보이는가, 안정 phase에 launch work가 없는가, 측정 도구 process가 측정 tree에 끼지 않았는가. 실패한 repeat는 이유와 함께 pool에서 뺍니다(9.5 D47).
- **untraced control**: `perf sched record` 자체가 값을 바꾸는가. 각 phase를 `perf`를 켠 채와 끈 채로 번갈아 두 번 돌리는 job을 프로그램마다 여섯 개씩 돌리고(순서 셋씩), `/proc`에서 thread별 CPU와 switch 수를 읽어 "끈 것/켠 것" 비율의 95 % 구간을 봅니다. 차이가 보이면 항목의 `modeling_notes`에 적고, 실린 값은 켠 쪽(traced) 값 그대로 둡니다(`_dev/docs/spec/jioh/task-9.5-untraced-control.md`; 9.5 D82, 9.8 D32, 9.9 D40, 모두 2026-09-27). 기록된 범위: 차이가 보인 곳에서 wake 비율의 비율은 0.97–1.08, run 평균의 비율은 0.72–0.98이었습니다. tracing이 일부 thread의 run을 길게 만든다는 뜻입니다. batch 계열은 대신 perf와 taskstats를 맞대 봅니다(`cc1`에서 perf/taskstats 1.005).
- **stimulus 민감도 검사**: typing 항목 넷은 SWELL-KW 대신 다른 typing 녹화(136M Keystrokes, `dhakal-chi18`: 외운 문장을 받아 적는 transcription typing)도 재생해, key당 CPU가 녹화에 따라 얼마나 변하는지 미리 등록한 방식으로 비교했습니다(9.5 follow-ups spec decision 11). 결과는 repeat별 비율로 읽습니다(9.5 D81). `office-writer` 1.123(95 % 구간 1.045–1.200), `web-browser` 1.338(1.284–1.392), `mail-client` 0.909(0.824–0.994)로 차이가 보였고, `code-editor` 1.029(0.968–1.090)는 차이가 보이지 않았습니다. 미리 정한 규칙대로, 결과와 상관없이 항목은 SWELL-KW 값을 싣습니다("The archetypes carry SWELL-KW whatever the result … a large difference is a stated limitation of D6, not a re-decision").
- **build 섞임**: vendor가 최신판만 내려주는 프로그램(Chrome, Thunderbird)은 campaign 도중 판이 바뀌었습니다. 판이 바뀐 repeat를 첫 판의 흩어짐과 값마다 비교하고, 다른 값은 scope에 적습니다(9.5 D69). VS Code처럼 판을 고정할 수 있으면 고정하고, 다른 판을 설치한 job은 `gate=wrong-build`로 멈춥니다.
- **시간 창**: 실린 phase를 100초 창으로도 읽어, 일부 일이 phase의 일부에만 몰려 있으면 scope에 적습니다. 실린 값은 phase 평균 그대로입니다(9.5 D85, D87).
- **compile 충실도**: test가 표의 draw가 평균을 지키는지, component마다 gap 표가 측정 비율을 2 % 안에서 내는지, 항목마다 compile된 wake 비율이 실린 비율의 5 % 또는 count 표준오차의 네 배 안에 드는지 확인합니다(`feller-ipta50`이 count 표준오차의 근거).

## 3.7 "this software on this machine"

measured 항목의 scope는 거의 모두 같은 문장으로 끝납니다. "Values are this software on this machine, not desktop truth (D10)." 9.5 D10(2026-09-14, "the runner's absolutes are the observation")이 정한 위치입니다. runner에서 잰 값은 "그 runner에서 그 판의 그 프로그램"에 대한 관측이고, 실제 사용자 desktop에서의 값이라고 주장하지 않습니다. 기록된 이유: "the values are observations of that software on that machine, the only current Linux observations obtainable (D3)." 버린 대안은 옛 building-plan §7의 순위 매김("convention informed by measurement")이었는데, 그렇게 낮추면 어떤 interactive 항목도 Phase 9 decision 2(한 항목의 숫자는 한 observation에서)를 만족할 수 없었기 때문입니다.

measurement-overview §11은 이것을 더 구체적으로 적습니다. "a GitHub-hosted runner, one pinned AMD EPYC 7763 core shared with the runner's own agent, Xvfb or a headless session, no GPU, no display refresh, no sound device, no human, one CPU model over one period. … The precision stated is precision on that configuration — reproducibility, a separate property from representativeness. Real-desktop validation is deferred." stability rule이 보장하는 것은 **재현성**(같은 조건이면 같은 값)이지 **대표성**(실제 desktop을 대표함)이 아니라는 것입니다. `docs/memos/2026-09-20-dataset-validity-review.md`의 판정도 같은 선을 긋습니다. 이 측정은 "sound for the recognition claim, bounded for the scheduling-benefit claim"이고, stability rule은 "precision on one configuration, not representativeness"를 세운다는 것입니다.

# 4장 · gaming: LAVD에서 온 game chain과 Steam client

이 장부터 10장까지는 29개 항목을 하나씩 봅니다. 묶음은 그 항목을 만든 연구 **slice**(Phase 9가 영역별로 나눈 연구·결정 단위. 9.4 gaming, 9.5 interactive와 typing, 9.6 compile, 9.7 background와 IO, 9.8 browser와 comms, 9.9 daemon과 session, 그리고 timeline을 맡으며 일곱 항목을 새로 잰 9.10, scheduler 쪽 상수를 맡은 9.11)를 따릅니다. 각 slice는 `_dev/research/jioh/task-9.<n>-<영역>/changelog.md`에 결정을 D1, D2, … 번호로 남겼고, 이 권은 그 결정을 "9.5 D13(per-input run을 window rule로 정한 결정)"처럼 번호와 내용을 함께 적습니다.

항목마다 다음을 적습니다. 무엇을 흉내 내는가(실제 프로그램), 어떤 행동을 재현하는가, 핵심 숫자와 tag, 그 값을 정한 결정(날짜, 번호, 기록된 이유). 값이 design, convention, arithmetic이면 그렇게 밝힙니다.

gaming은 이 dataset에서 특별합니다. game을 CI runner에서 잴 수 없기 때문입니다(GPU가 없고, Proton(Windows game을 Linux에서 돌리는 Wine 기반 호환 계층) game은 Steam client 안에서만 돎). 그래서 29개 중 유일하게 문헌에서 숫자를 가져온 항목이 여기 있습니다.

## 4.1 `game-task-chain` — 프레임 하나를 이어 달리는 task들

**무엇을 흉내 내나.** Windows game을 Linux에서 Proton(Wine 기반 호환 계층)으로 돌릴 때, 사용자 입력에서 화면 갱신까지 한 frame을 만드는 task들의 사슬입니다. timeline에서는 game process 이름 `Troy.exe`(LAVD 발표가 예로 든 game의 process 이름)로 나타납니다.

**어디서 왔나.** `lavd-ossna24`: Changwoo Min의 발표 "Optimizing Scheduler for Linux Gaming"(Open Source Summit North America 2024, 2024-04-17)의 slide입니다(`docs/references.md`의 cite 줄). LAVD는 sched_ext(BPF program으로 Linux scheduler를 바꿔 끼우는 장치) 기반 scheduler이고(`docs/workload/source-vetting.md`의 B5가 그 code를 `github.com/sched-ext/scx`로 적음; `docs/workload/grounding-sources.md`는 gaming scheduling이 실제 문제라는 근거로 Valve가 LAVD code의 저작권을 갖고 그것을 SteamOS 3.8에 사용자가 고르는 scheduler로 싣는다는 것을 적음), 이 발표는 game이 돌 때 scheduler가 보는 task들을 관찰한 결과를 보여 줍니다. 발표는 관찰에 쓴 도구를 밝히지 않습니다. `sources.yaml`의 notes는 이 출처의 숫자를 "Min's reported figures of 2024-04-17"로, slide 번호와 함께 적습니다. 게임을 하며 모은 trace에서 나온 숫자이고, 게임과 기계는 밝히지 않습니다. system task까지 세어 system 전체에서 약 300개 task가 scheduling되고 그중 약 90 %가 오래 사는 task이며, 가장 자주 scheduling되는 30–40개 task가 scheduling의 95 %를 차지하는데, 그 절반쯤인 system task(특히 wine·graphics·audio server)가 30–40 %, game 전용 task 15–20개가 60–70 %를 차지합니다(s12). schedule당 runtime은 평균 수백 μs에서 최대 수 ms이고(이름이 붙은 예는 wineserver 260 μs와 task worker 1.65 ms), 실행 시간은 "very stable and is predictable using its average"입니다(s13). scheduling 사건의 70–75 %는 대기 system call에서 시작되고(s14), task들은 waker–waiter graph로 묶여 있으며(s16), task 여럿이 한 job, 예컨대 사용자 입력에서 화면 갱신까지를 함께 맡습니다(s17). 그리고 "The slides state no frame period or frame budget"이라고 덧붙입니다. registry(`sources.yaml`)에서 이 출처의 type은 2026-10-17부터 talk, conference abstract or news report이고(그 전에는 deployed-system), notes의 마지막 문장은 "Talk slides, footnote tier: every number is stated as Min's report, with the talk's date"입니다. 그 전의 notes는 같은 숫자를 날짜 없이 "observations established"로 적고 "Slides are footnote-tier despite carrying numbers"로 끝났습니다(2026-10-17, 9.15에서 인지오의 답으로 고침). `docs/references.md`는 2026-10-16부터 이것을 talk·학회 초록·뉴스 보도 등급(2.8절)에 두고, 그 숫자를 Min이 2024-04-17에 보고한 값으로, chain의 꼴을 design으로 적습니다(9.12 D113).

**program.** 이 항목은 `pattern.constructor: chain`입니다. compiler는 task 하나를 member 17개로 펼칩니다. 첫 member(머리)만 timer로 깨어나고, 나머지는 앞 member의 WAKE로 깨어나 일하고 다음 member를 깨웁니다.

```yaml
program:                     # per constructed chain member
  - loop:
      - WAIT: upstream
      - RUN: per_schedule_run
      - WAKE: downstream
```

머리는 `WAIT: upstream` 대신 `TIMER frame_period`를 씁니다. compile된 `c1-gaming`에서 머리의 program은 `LOOP { TIMER 16667, RUN 631, WAKE game.wineserver }`이고, 두 번째 member `wineserver`는 `LOOP { WAIT chain:game.wineserver, RUN 341, WAKE game.chain.2 }`입니다. 마지막 member는 아무도 깨우지 않습니다.

**숫자.**

| param | 값 | tag | 성격 |
|---|---|---|---|
| `wineserver_run` | constant 260 μs, per-instance | `lavd-ossna24:s13` | 출처의 값("Some coordination tasks run very shortly (e.g., wineserver:260 usec)") |
| `per_schedule_run` | lognormal, 기준점 260 / 1,650 μs, per-task | `lavd-ossna24:s13` | 기준점은 출처의 값, 그것을 p05/p95로 읽는 것과 lognormal family와 member당 한 번 뽑기는 우리 것 |
| `frame_period` | constant 16,667 μs, per-instance | `steamos-refresh` | design. 1/60초의 arithmetic |
| `chain_length` | constant 16, per-instance | `lavd-ossna24:s12` | design within a source range. slide의 "15-20 game-specific tasks" 안의 한 점 |

`binding_params: [lane_share, member_names]`이고, `scalable`은 "scale the chain's aggregate demand per frame to lane_share of the lane"입니다. `validation_stats.referee`는 `none`이고 이유는 "validation against LAVD would be circular — LAVD is also the parameter source … and a CI runner cannot observe a Proton game's Wine, DXVK or audio structure (no GPU; Proton is documented only as a tool for use with the Steam client), so no own measurement referees it"입니다.

**lane scaling.** simulator는 CPU 하나만 흉내 내는데, LAVD의 game은 여러 core machine에서 돌았습니다. 그래서 compile할 때 chain member들의 RUN 값을 한꺼번에 늘리거나 줄여, frame 하나 동안 chain 전체가 쓰는 CPU가 `lane_share` × frame_period가 되게 맞춥니다(`compiler.py`의 `_chain_constructor`: `factor = lane_share * frame / sum(runs)`). `c1-gaming`은 `lane_share: 0.9`(design)를 주므로 chain 17개 RUN의 합은 0.9 × 16,667 ≈ 15,000 μs가 됩니다. wineserver의 260 μs가 341 μs로 늘어난 것도 이 scaling 때문입니다. 이것이 library에서 유일하게 `scalable`이 비어 있지 않은 항목입니다.

**member 이름.** 머리는 timeline의 task 이름(`Troy.exe`), 두 번째는 항상 `wineserver`, 나머지 15개는 timeline의 `member_names`가 줍니다. `c1-gaming`은 이렇게 줍니다. `Task worker thr` 넷, `dxvk-cs`, `dxvk-submit`, `winepulse_mainl`, `winepulse_timer`, `FAudio_AudioCli`, 그리고 `Troy.exe` 여섯. tag는 `member_names: "lavd-ossna24:s16"`입니다.

> **왜 이렇게 정했나 — 하나의 observation(9.4 D1, 2026-09-13).** 9.4 slice는 이 항목의 출처를 LAVD 발표 하나로 유지했습니다. 인지오의 결정으로, slide 12–17을 "one observation of an unnamed game on an unnamed machine, collected with `perf sched record`"로 취급합니다. 2024년 발표는 도구를 밝히지 않고, `perf sched record`는 Min의 뒤의 발표를 다룬 보도(LPC 2025 session에 대한 Edge의 보도 `edge-lwn26`: Min의 도구 VaporMark가 "perf sched record"로 모은 data를 분석함)에 나오는 이름이고, 그것을 이 발표의 trace에 이은 것은 9.4 D1의 읽기입니다. 기록은 약점도 함께 적습니다. "the deck's figures draw on at least three process trees … and the text does not say which feeds slides 12–14." 버린 대안은 공개된 `scx_lavd` sample log와 "our own CI measurement of a native game"이었습니다.

> **왜 이렇게 정했나 — frame_period(9.4 D2, 2026-09-13).** 16,667 μs는 원래 LAVD 출처 tag를 달고 있었습니다. 2026-09-13의 critical findings memo(A2)가 slide 30장을 다 읽고 "No slide contains 16.7, 16.67, 60 fps or 'frame budget'"을 적었습니다. 그림까지 보면 frame 주기나 60 fps 목표를 말하는 slide는 없고, slide 29의 benchmark screenshot에 설명 없는 60 FPS / 16.5 ms 표시가 하나 있습니다. slide 27의 "targeted latency (e.g., 15 msec)"는 scheduling 창이지 frame 주기가 아니고, 발표의 benchmark는 V-Sync와 frame 제한을 끈 채 평균 41.3 FPS로 돌았습니다. 그래서 값은 그대로 두고 tag를 `steamos-refresh`(Valve의 "The SteamOS 3.2 Update" 2022-05-26: "The default is 60Hz … 60hz = 16.66ms/frame")로 바꾸고, 이름표를 design으로 붙였습니다. "the game is modelled as display-paced at the Steam Deck LCD default refresh with the 1:1 frame limit; 16667 µs is 1/60 s arithmetic." 버린 대안은 25,000 μs(40 Hz 모드)와 "no period"(발표의 제한 없는 benchmark)였습니다.

> **왜 이렇게 정했나 — chain만 남긴다(9.4 D3, 2026-09-13).** 옛 항목은 `n_tasks: 300`이라는 개수와 꼬리 task용 `tail_idle_gap`(500,000 μs), `tail_run`(200 μs)을 가졌고, 그래서 모든 gaming 파일이 `game.exe`라는 이름의 task 300개를 보였습니다. 9.4 D3이 셋을 지웠습니다. 기록된 이유: "The count was held against the library's own rule (`archetypes.yaml` header: counts never carry values here); the source's figure is system-wide ('Around 300 tasks are scheduled while running a game', slide 12, including the system tasks it names)." 꼬리 값은 "placeholders under a source tag"였습니다(출처가 상위 30–40개 밖의 task에 대해 아무 값도 주지 않음). 그 결과 모든 gaming 파일에서 284개의 `<id>.tail.<j>` task가 사라졌습니다. game의 나머지 thread를 timeline이 몇 개 싣느냐는 9.10에 넘겼고, 9.10 D19(2026-10-01)가 "a gaming file carries the game chain only; the game's other threads are omitted and stated"로 정했습니다.

> **왜 이렇게 정했나 — wineserver는 chain의 member(9.4 D4, 2026-09-13).** 예전에는 `wineserver`를 서버 daemon 측정값에서 온 `system-daemon`에 묶어 두었는데, critical findings memo(B6)가 그 결과 `c1-gaming`의 wineserver가 1,225초 sleep을 뽑아 60초 segment 동안 한 번도 깨지 않았다고 지적했습니다. 9.4 D4는 `wineserver_run` 260 μs를 새로 두고 wineserver를 머리 바로 뒤의 member로 넣었습니다. 근거: slide 11(game의 dispatcher thread들의 hub), slide 13(coordination task), slide 16(graph에서 가장 큰 edge 수: `wineserver → Troy.exe` epoll 134,200회, `Troy.exe → wineserver` pipe_read 58,134회), Wine의 호출 경로(요청 write, 막히는 응답 read). 원래는 왕복(round trip)인 관계를 한 방향 relay로 편 것은 "our linearisation"이라고 `modeling_notes`에 적었습니다.

> **왜 이렇게 정했나 — chain_length(9.4 D5)와 per_schedule_run(9.4 D6), 2026-09-13.** 16은 slide 12의 "There are 15-20 game-specific tasks, which takes 60-70% scheduling" 안의 한 점이고, 이름표는 "design within a source range"입니다. 버린 대안은 15–20 사이에서 instance마다 뽑기였습니다. wineserver member는 이 16에 들어가지 않습니다(출처가 wine을 system task 쪽에 셈). `per_schedule_run`의 두 기준점 260 μs와 1,650 μs는 slide 13이 이름을 들어 예로 든 두 값(coordination task와 work task)이고, 그 사이를 "a few 100s usec on average to a few msec maximum"이 감쌉니다. slide 13의 그림(한 game, 약 128 task, 중앙값 약 0.04 ms)은 chain의 가장 자주 scheduling되는 task들과 다른 모집단이라 쓰지 않았습니다. member당 한 번만 뽑는(`per-task`) 근거는 slide 13의 "Task execution time is very stable and is predictable using its average"입니다.

> **왜 이렇게 정했나 — 쓰이지 않던 두 param(9.4 D7, 2026-09-13).** `frac_long_lived`(0.90)와 `frac_wakeups_from_wait`(0.70–0.75)는 어떤 도구도 읽지 않았습니다(memo B1). 둘을 지우고, 두 사실은 "encoding이 모델링하지 않는 것"으로 `modeling_notes`에 locator와 함께 남겼습니다. 모든 member는 segment 내내 살고, wake의 종류 섞임은 배선(머리 하나가 TIMER, 나머지는 WAIT)으로 고정됩니다.

> **왜 이렇게 정했나 — per-wake RUN의 과소평가는 값을 바꾸지 않음(9.4 D9, 2026-09-17).** 9.5 follow-ups spec decision 4가 RUN을 "wake 한 번의 수요"로 정의하자(preemption 뒤 재개는 앞 wake에 합침), 출처의 "schedule당 runtime"을 wake당 RUN으로 읽는 것이 수요를 줄여 잡는다는 점이 드러났습니다. preemption으로 끊긴 schedule은 wake 하나를 여러 조각으로 셉니다. 크기는 같은 발표의 slide 14가 묶어 줍니다(preemption이 scheduling 사건의 25–30 %, pie의 `sched_preempt` 28.78 %). 그 비율에서 9.4 D9가 계산하면(1/(1 − 0.2878)) 평균으로 wake당 약 1.4 schedule이고(slide가 적은 값이 아니라 우리의 산술), slice 길이에 다가가는 긴 work task(1.65 ms worker 대 `scx_lavd` source 주석의 예, 15 ms를 task 10개가 나누는 1.5 ms)에서 더 크며, 짧은 coordination task에서는 1에 가깝습니다. 결정은 "No value changed"였고, 대신 9.14(consumer rework)가 gaming 파일의 민감도 검사로 chain member RUN을 ×1.0–1.4 이상으로 훑기로 넘겼습니다. 버린 대안은 기준점을 1/0.71로 늘리기("assumes preemption independent of run length and task, which the slice mechanism contradicts")였습니다. 2026-10-10의 dataset audit(A3)는 이 항목을 "resolved as is"로 닫았습니다. "The figures stand as the talk's reported values; the chain-x1.2 and chain-x1.4 variants are the sensitivity check." `variants.yaml`의 chain 배율 변형이 이 검사입니다.

> **왜 이렇게 정했나 — member 이름(9.10 D26, 2026-10-01).** 9.4가 남긴 "`game.exe` 이름" 문제를 9.10이 풀었습니다. 머리 `Troy.exe`, 다음 `wineserver`, 이어서 `Task worker thr` 넷 → `dxvk-cs` → `dxvk-submit`, `winepulse_mainl`, `winepulse_timer` → `FAudio_AudioCli`, 이름 없는 나머지 여섯은 `Troy.exe`. 근거는 slide 16의 tree(tgid 7781, node 열 개)와 edge 수(`Task worker thr → dxvk-cs` 각 약 10,000, `dxvk-cs → dxvk-submit` 30,970, `winepulse_timer → FAudio_AudioCli` 10,213)이고, Wine이 process 이름을 `.exe`로 바꾼다는 사실입니다. slide 16에 `Troy.exe` node는 하나뿐이고, 여섯 구성원이 `Troy.exe`인 것은 자기 이름을 정하지 않은 Wine thread가 process의 `comm`을 그대로 갖는다는 우리 규칙입니다(`game-task-chain`의 `modeling_notes`: "six members carry the process name Troy.exe: slide 16 shows one Troy.exe node, and a Wine thread that sets no name of its own keeps its process's comm (9.10 D26), a rule that is ours"). archetype은 이름을 정하지 않는다는 원칙대로, 이름은 항목이 아니라 timeline의 `member_names`에 들어갑니다.

`modeling_notes`는 이 encoding이 출처와 어떻게 다른지도 솔직히 적습니다. 출처의 graph는 fan-in(task worker 넷 → dxvk-cs), 두 단계 사슬(dxvk-cs → dxvk-submit), audio thread들 사이의 2-cycle, wineserver 주변의 hub인데, 이 항목은 그것을 한 줄로 폈습니다. 또 slide 17은 대부분의 game task가 각자 주기적이라고 말하는데, 이 항목에서는 머리만 timer로 깨어납니다.

## 4.2 `game-client` — 로그아웃된 채 창이 떠 있는 Steam client

**무엇을 흉내 내나.** Valve의 Steam desktop client(`steam`과 그 browser 기반 interface `steamwebhelper`의 process tree 전체)입니다. timeline에서는 `steam`이라는 이름으로 gaming 파일들에 game chain 옆에 놓입니다.

**측정.** 9.8 slice의 desktop campaign `meas-ci:desktop:2026-09-20`, 12 repeat. Steam client build 1788652215(`steam-installer`)를 **로그아웃 상태**로, 창을 보이게 띄우고(Xvfb에 창을 최소화할 수 있도록 openbox window manager를 둠), 900초 settle 뒤 600초 `shown` phase를 쟀습니다. 측정 대상은 CPU 하나에 묶고, 측정 도구와 page 서버, homeserver는 다른 CPU에 두었습니다.

**숫자.** 11개 component(residual 포함), phase 전체 약 299.3 wakes/s(`stats`: "shown wakes/s 298.0720–301.9440"), CPU 점유율 0.013–0.018. 큰 component는 `steamwebhelper`(70.749 wakes/s, gap 중간값 16.15 ms), `steam`(69.467/s), `IPC:CSteamEngin`(44.496/s), `CJobMgr::m_Work`(35.629/s)입니다. `steamwebhelper`의 gap은 중간값부터 p99.9까지 16.15–16.53 ms 사이에 몰려 있어, 거의 일정한 간격으로 깨어납니다. 그 간격이 무엇에서 오는지 적은 문장은 이 권을 쓰며 읽은 기록(항목의 scope, 9.8 changelog의 결정 제목들)에서 찾지 못했습니다(확인 필요). heavy event 하나: `CHTTPClientThre`의 1 ms 이상 run이 12 repeat의 7,200초 동안 62번(2.0–50.2 ms), 비율 0.008611/s로 실립니다.

**예외.** run 평균 넷(`steamwebhelper` ±5.3 %, `steam` ±10.1 %, `IPC:CSteamEngin` ±8.8 %, `VizCompositorTh` ±5.6 %)은 "machine 따라 흩어짐" 예외로 실립니다. 이들의 run이 phase CPU의 80.2 %를 차지한다는 것도 scope에 적혀 있습니다(9.8 D37).

> **왜 이렇게 정했나 — 자기 항목, 로그아웃(9.8 D6, 2026-09-20).** 예전 `steam` task 여섯은 `electron-comms`에 묶여 있었고, 가장 가까운 대안은 `system-daemon`이었는데 그것은 "a pool of 51 stock system services … with a wake gap of 11.24 s against the sub-millisecond cycle of the one in-game sample"이라 맞지 않았습니다. 그래서 Steam client 자체를 runner에서 쟀습니다. 로그아웃인 이유는 규칙입니다. "No account is used, and none may be." 기록은 Steam Subscriber Agreement §4.C(Automation)와 §1.C(계정은 엄격히 개인용)를 인용합니다. 대가로 scope는 "Not covered: a client that is logged in, holds a library, downloads, or runs behind a game — the state the gaming timelines depict"를 적습니다. gaming 파일이 보여 주는 상태(게임 뒤에서 도는 로그인된 client)와 측정한 상태가 다르다는 한계를 숨기지 않은 것입니다. 9.10 D22(2026-10-01)는 "the gaming files keep the logged-out Steam client, its state stated"로 이 선택을 timeline 쪽에서 확인했습니다.

> **왜 이렇게 정했나 — 900초 settle(9.8 D15, 2026-09-20).** 1,800초 long-phase probe에서 Steam은 약 325 wakes/s에서 900초 무렵 약 298 wakes/s로 한 계단 내려갔고, 120초 창의 흩어짐이 그 계단을 빼면 4.8 %에서 0.2 %로 줄었습니다. 그래서 settle을 900초로 정했습니다.

> **왜 이렇게 정했나 — HTTP burst는 드문 사건(9.8 D33, 2026-09-28).** `CHTTPClientThre`의 run 평균이 repeat 사이에서 두 갈래로 갈렸습니다. 원인을 보니 12 repeat 중 넷(4, 5, 6, 12)에서 2.8초 안에 12–18개의 2.0–50.2 ms run이 몰린 burst가 한 번씩 있었고, 그 밖의 run은 0.28 ms 미만이었습니다. 이것을 `web-browser`의 `MemoryInfra`와 같은 "run 안의 드문 사건" class로 보고, 1 ms 이상 run(design 기준선)을 component에서 빼 heavy event로 실었습니다. burst가 몰려 오는 성질("the burst's clustering")은 싣지 않는다고 scope가 적습니다.

> **왜 이렇게 정했나 — 보이는 창(9.8 D5, D18).** 측정은 창을 최소화한 phase도 함께 돌렸고, 보이는 창이 1.225배 더 자주 깨어났습니다(299.316 대 244.386 wakes/s). 9.8 D5의 원래 질문은 `steamwebhelper`를 어느 renderer 상태에 묶을지였는데, Linux가 가려진 창을 숨김으로 표시하지 않는다는 근거들로 "보이는" 쪽을 택했습니다. 그 근거에는 한계가 있습니다. Linux의 Chromium은 가려짐을 스스로 계산하지 않고, X11에서는 X server가 창이 완전히 가려졌다고 알릴 때 그 창을 occluded로 표시합니다. 그려진 desktop이 그 알림을 보내는지는 측정이 시험하지 않았습니다. 9.8 D25(2026-09-22)가 별도의 `steamwebhelper` task 아홉을 timeline에서 은퇴시켰습니다. `game-client`의 tree가 이미 모든 helper를 담고 있어(70.75 wakes/s, 23.6 %) 두 번 세게 되기 때문입니다.

`game-client`는 gaming 파일 외에 Steam이 나오는 곳에도 쓰입니다. 같은 Steam이라도 다운로드하는 Steam은 다른 항목입니다. 그것은 7장의 `game-download`입니다.

# 5장 · interactive와 typing: 사람이 두드리는 application

이 장은 9.5 slice(interactive와 typing)가 만든 아홉 항목을 다룹니다. 사용자가 직접 쓰는 application 여섯(`office-writer`, `code-editor`, `mail-client`, `web-browser`, `image-editor`, `video-editor`)과, 재생·통화 셋(`video-player`, `audio-player`, `video-call`)입니다. 이 장의 질문은 "사람이 키보드를 두드리고 화면을 보는 application을, scheduler가 보는 사건열로 어떻게 옮겼나"입니다. 이 질문이 어려운 이유는, application 하나가 실제로는 thread 수십 개짜리 process 여러 개이고, 사람의 입력과 내부 timer가 섞여 깨어나기 때문입니다.

## 5.1 아홉 항목의 공통 모양

먼저 아홉 항목이 공유하는 결정들을 모읍니다. 개별 항목 절에서는 이것을 다시 설명하지 않습니다.

**application마다 항목 하나(9.5 D2, 2026-09-14).** 예전에는 `desktop-interactive` 하나가 editor, 오피스, 메일, browser, 사진 편집, 동영상 편집 여섯 application을 모두 대표했습니다(9.5 scope card: "44 bindings in 37 files"). 9.5 D2는 이것을 application마다 하나로 나눴습니다. 기록된 근거는 문헌이 application마다 CPU 요구가 크게 다르다고 말한다는 것입니다. Lorch 2003 §4.7("different applications have very different CPU requirements, even when handling the same type of user interface event"), Flautner 2000(Xemacs는 100 ms 이상 episode가 0 %, GIMP는 시간의 91 %), Endo 1996(key 하나에 Notepad 10 ms 미만, Word 약 32 ms).

**runner 측정이 유일한 observation(9.5 D3, 2026-09-14).** 여섯 항목은 각각 CI runner의 측정 campaign 하나에서 모든 값을 가져옵니다. 문헌은 runner가 돌릴 수 없는 application의 대안일 뿐이고, 2000–2004년의 Linux trace는 그 대안도 되지 못합니다. 기록된 이유: "인지오 judges values measured on 100–664 MHz machines two decades ago unable to back a current application"; 그리고 "the search found no newer per-input observation of a Linux editor, office suite, mail client, browser, image editor or video editor".

**task 하나에 process tree 전체(9.5 D14, 2026-09-15).** measured 항목의 task 하나는 application의 process tree 전체, 모든 thread를 합친 것입니다. 단 다른 항목이 가진 process는 뺍니다. Chrome의 경우 다른 tab의 renderer(Chrome에서 page 하나를 그리는 process)는 `renderer-hidden`의 몫입니다(9.5 D84가 나중에 지금 쓰는 page의 renderer는 `web-browser`에 넣었습니다, 5.5절).

**하나의 합쳐진 사건열(9.5 D9), component(D16), quantile table(D17), SWELL-KW 재생(D18), window rule(D13).** 2장에서 설명했습니다.

**CPU 하나, 같은 machine(9.5 D21, D26).** 2026-09-16부터 모든 측정은 CPU 하나에 묶였고(D21), 2026-09-18부터 EPYC 7763 하나의 machine gate 아래 새 campaign으로 다시 쟀습니다(D26). 그 전 campaign(`meas-ci-2026-09-16` release)은 pool에 넣지 않았습니다. D26이 기록한 이유: 45개 job이 다섯 가지 CPU 모델을 뽑았고 다섯 repeat가 한 모델에서 나온 application이 하나도 없었는데, fold-in 도구는 모든 scope에 "4 vCPU AMD EPYC 7763"을 고정 문구로 써 넣고 있었습니다.

**keys only(9.5 D28, D65, D72, D79).** 처음에는 녹화의 key와 pointer 사건을 함께 재생했습니다. 그러자 click, scroll, drag가 타이핑 위치를 옮겼습니다. Writer에서는 타이핑이 76쪽 문서의 끝이 아니라 72–75쪽에 들어갔고, drag가 고른 글자를 타이핑이 덮어써 단어 수가 줄었습니다(D28). VS Code에서는 녹화의 pointer 원점이 activity bar의 검색 icon 위에 떨어져 검색 창에 글자가 들어갔습니다(D72). 그래서 넷 모두 key만 재생하도록 바꾸고, scope에 "the archetype carries typing, not document navigation"처럼 적었습니다.

**TIMER와 WAIT(timer)(9.5 D74, D75).** 1.5절과 2.4절에서 설명했습니다. 여섯 application은 deadline 없는 timer wake만 갖고, 재생·통화 셋만 TIMER를 갖습니다.

**launch phase(9.10 D21, D136, D140).** `code-editor`와 `image-editor`를 뺀 일곱이 launch를 가집니다. 이 둘은 core set 어디에서도 파일 중간에 켜지지 않기 때문입니다(9.10 D21이 나열한 중간 시작. `c3-`는 C3 그룹, 즉 여러 상황을 이어 붙인 긴 arc 파일이고 `c4-`는 끼워 넣기 그룹입니다: `c3-workday`의 writer 60초와 Thunderbird 360초, `c3-evening`의 game·Steam·chat 60초와 player 둘 300초, `c3-creation`의 Kdenlive 120초, `c4-compile`의 Chrome 30초, `c4-gaming`의 chat 30초).

**venue 한계(9.5 D24, 2026-09-16).** Xvfb에는 화면 refresh가 없고 GPU가 없습니다. 9.5 D24는 그 오차의 방향을 문헌으로 한 문장씩 scope에 적었습니다. Chromium 계열(`web-browser`, `video-call`, `code-editor`)은 vsync(화면 refresh에 맞춘 동기화) 없이 compositor(창과 layer를 합쳐 화면을 만드는 부분)를 기본 60 Hz timer로 돌리므로 주기는 60 Hz 화면과 같지만 위상은 다르고, `--disable-gpu` 아래 CPU에서 rasterize(그림을 pixel로 그리는 일)하므로 그 thread들의 run 길이는 GPU desktop보다 길게 잡힙니다("by an amount no source states"). `video-editor`(Qt Quick)는 buffer swap에서 막히며 속도를 맞추는데 software rasteriser는 막히지 않으므로 그 경로의 wake 비율이 과대평가됩니다. `video-player`(mpv)는 audio clock에 맞춰 frame을 내므로 refresh가 없어도 리듬은 같지만, x11 출력의 frame 복사는 GPU 출력이라면 GPU로 갈 CPU 일입니다.

## 5.2 `office-writer` — LibreOffice Writer에 타이핑하기

| | |
|---|---|
| 흉내 내는 것 | LibreOffice Writer(`soffice.bin`) |
| 측정 | LibreOffice 24.2.7.2(Ubuntu 24.04 apt), 약 76쪽 생성 문서 끝에 타이핑, 14 repeat |
| 재현하는 행동 | key마다 수 ms의 CPU; 평소에는 약 0.6초마다 몇 번 몰아서 깨어남 |
| 핵심 숫자 | `input_run` p50 3.23 ms, 평균 4.91 ms, p99 11.4 ms, 최대 194 ms; `soffice.bin` 3.4571 wakes/s, run p50 70 μs; idle CPU 점유율 0.0005–0.0007 |
| tag | `meas-ci:interactive:2026-09-18`(값), `swell-icmi14:word-c1`(입력), `meas-ci:desktop:2026-10-04b`(launch) |

`office-writer`는 2.9절에서 끝까지 따라간 항목입니다. 여기서는 그 숫자를 정한 결정을 정리합니다.

- **문서와 입력(9.5 follow-ups spec decision 6, 9.5 D22).** 100개 절 × 100단어 문단 다섯 개와 1024×768 그림 열 장으로 만든 약 76쪽 문서를 열고 그 끝에 타이핑합니다. 길이를 정한 출처는 없어 design입니다(scope: "design — no source states a length").
- **keys only(9.5 D28, 2026-09-18).** 5.1절에서 설명한 대로, pointer 사건이 타이핑을 문서 중간으로 옮겼기 때문입니다. pointer를 함께 재생한 첫 다섯 repeat는 `input_run` 중간값이 8.67, 3.99, 5.91, 4.53, 4.21 ms로 ±44 % 흩어졌고, 그 흩어짐이면 약 200 repeat가 필요했는데 SWELL-KW에는 Word 창이 56개뿐이었습니다. 그 다섯 repeat는 pool에서 뺐습니다.
- **14 repeat에서 멈춤(9.5 D88).** stability rule이 14 repeat에서 통과했습니다. 가장 넓은 값은 136M 녹화 아래의 per-input run 평균(±4.96 %)이고, scope는 "covers the true mean in about 91–93 % of campaigns"를 적습니다.
- **stimulus 민감도.** 136M 녹화 아래에서 per-input run 평균이 SWELL-KW의 1.123배(1.045–1.200)로, 차이가 있었습니다. 항목은 SWELL-KW 값을 싣습니다.
- **untraced control.** `perf`를 끄면 `soffice.bin`의 wake 비율이 1.003배, per-input run이 0.984배였습니다.
- **긴 span 검사(9.10 D145, D148, D149, 2026-10-05).** `c3-workday`가 Writer를 1,429초 동안 들고 있으므로, 측정 phase(120초)보다 긴 시간에서도 값이 유지되는지 long-phase probe로 확인했습니다. wake는 probe 수준의 0.1 % 안에서 유지됐고, CPU는 처음 2분 0.56–0.58 ms/s에서 5–11분째 0.64–0.66으로 올랐다가 그 뒤 0.56–0.63을 유지해, 120초 phase는 수준보다 −7.5 %(최악 −8.8 %)로 읽힙니다. 실린 CPU 점유율은 수준의 3.7 % 안입니다. 9.10 D149는 이것을 "`office-writer`'s CPU rises early and its span stands"로 정리했습니다.
- **launch(9.10 D140).** launch phase는 다섯 repeat 모두 약 40.76초입니다.

## 5.3 `code-editor` — VS Code에 TypeScript 쓰기

| | |
|---|---|
| 흉내 내는 것 | Visual Studio Code(`code`)와 그 TypeScript language server |
| 측정 | VS Code 1.138.0(vendor .deb, 판 고정), TypeScript project `sindresorhus/got` v16.0.0을 열고 `source/index.ts`에 타이핑, 44 repeat |
| 재현하는 행동 | key 하나마다 language server가 파일을 다시 검사해 수십–수백 ms의 CPU; 평소에도 compositor와 IO thread가 초당 100번 넘게 깨어남 |
| 핵심 숫자 | `input_run` p50 79.7 ms, 평균 99.3 ms, p99 551 ms, 최대 3.04 s; component 9개(residual 포함) 합 112.4 wakes/s; idle CPU 점유율 0.0128–0.0159, driven 0.14–0.45 |
| tag | `meas-ci:interactive:2026-09-25`, `swell-icmi14:word-c1` |

VS Code는 이 library에서 key 하나가 가장 비싼 application입니다. 2.9절의 Writer가 key당 약 3 ms였다면 VS Code는 약 80 ms입니다. scope가 이유를 적습니다. key는 고정된 글자 순환으로 재생되고(D4: timing only), "so the per-key cost is the language server re-checking a file being filled with letter runs". 글자를 칠 때마다 TypeScript language server가 파일을 다시 검사하는 비용입니다.

component는 Chromium 기반 구조를 그대로 보입니다. `gpu/VizCompositorTh`(23.1/s), `renderer/Compositor`(22.8/s), `gpu/Chrome_ChildIOT`(20.2/s), `renderer/code`(19.5/s), `utility/code`(11.5/s), `utility/libuv-worker`(5.38/s), `renderer/ThreadPoolForeg`(3.43/s), `code`(3.37/s), 그리고 21개 comm을 묶은 residual(3.09/s). 8개 comm이 112.4 wakes/s의 97.2 %를 덮습니다.

- **VS Code를 고른 이유와 입력.** 코드 편집용 timestamp 달린 keystroke 데이터는 없어서(9.5 D4: "No code-editing keystroke dataset with timestamps exists"), Word 녹화를 가장 가까운 stream으로 씁니다. project는 design입니다.
- **판 고정(9.5 D69, 2026-09-23).** campaign 도중 VS Code 1.139.0이 나왔고, 그 판은 `copilot-runtime` process를 띄워 idle에서 초당 49.7번 깨어났습니다(이 판 tree 전체의 115/s 대비). 그래서 1.138.0으로 고정하고 다른 판을 설치한 job은 멈추게 했습니다. scope의 "Build bound" 문장: "whether a code editor should describe an assistant-bearing one is the archetype's own question, not this campaign's." AI 보조 기능이 붙은 editor를 대표해야 하는지는 이 측정이 답하지 않는 열린 질문이라는 뜻입니다.
- **idle은 200초부터(9.5 D83, 2026-09-28).** VS Code는 켜진 뒤 한참 launch work를 합니다. idle phase는 시작 200초 뒤부터 읽습니다.
- **session 사이에서 변하는 component(9.5 D57, 2026-09-20).** `utility/libuv-worker`의 비율은 한 run 안에서는 ±10.6 %만 변하는데 repeat 사이에서는 ±39.0 % 변했습니다. 기록된 이유: "Repeats tighten the estimate of such a value's mean; they do not narrow the spread, which is the application's behaviour and is what the dataset should carry." 그래서 이 component의 세 값(wake 비율 5.382/s ±5.63 %, gap 평균 185.8 ms, run 평균 0.0102 ms)은 반폭과 함께 실립니다.
- **44에서 멈춤(9.5 D73, D99).** keys-only campaign은 Word 녹화의 44번째 창에서 멈췄고, 당시에는 그것이 녹화의 마지막 창으로 읽혔습니다. 나중에 녹화가 57개 창(입력 있는 창 56개)을 가진다는 것이 확인됐습니다. 9.5 D99(2026-09-29)는 campaign을 늘리지 않고, 44 repeat에서 per-input 값 둘이 stability rule을 통과한다는 것을 확인하는 쪽을 택했습니다(SWELL-KW 99.26 ms ±4.84 %, 136M 103.9 ms ±3.01 %). 버린 대안은 45–57번째 창으로 campaign을 늘리기였습니다.
- **stimulus 민감도.** 136M 아래 1.029배(0.968–1.090), 차이 없음.
- **긴 span 검사와 extension host 사건(9.10 D144, D154, D158).** `c6-dual`(C6 그룹의 파일로, compile을 기다리며 game을 하는 두 전경이 똑같이 활성인 상황; 사용자의 kernel build 전체를 담아 깁니다)은 2026-10-11의 9.17 D1 전까지 VS Code를 12,068초 동안 초점에 두었습니다. 9.17 D1(focus track을 들인 결정) 뒤로는 editor와 game이 688초마다 번갈아 초점을 쥐어, 지금 editor가 한 번에 초점을 쥐는 구간은 688초입니다. 두 번의 long-phase probe는 그 전의 12,068초 span을 읽었고, probe의 길이와 결과는 그대로입니다(항목의 scope는 2026-10-14의 9.23 D8로 "Read over 12,068 s, the span `c6-dual` held it focused before its focus alternated with the game every 688 s (9.17 D1)"라고 고쳐 적습니다). 두 probe에서, 600초 창마다 commit된 파일로 되돌리면 per-input run 평균이 9.5의 같은 창 repeat 대비 1.00(0.97–1.03), 추세 없음이었습니다(한 줄을 계속 늘려 친 probe의 상승은 그 줄 길이 때문이었음). 그러나 두 probe 모두에서 VS Code의 extension host(TypeScript·JSON language server를 가진 process)가 2–4개 창 동안 창당 최대 400초 CPU를 쓰다가, VS Code가 host를 갈아 끼우는 일이 있었습니다(한 session 6,100–8,500초, 다른 session 10,700–12,050초). 그 동안 per-input run 평균은 실린 값의 최대 3.9배였습니다. 결정은 "The episode is not carried"였습니다.
- **launch 없음.** core set에서 VS Code를 파일 중간에 켜는 곳이 없어 launch가 없습니다.

## 5.4 `mail-client` — Thunderbird로 답장 쓰고 보내기

| | |
|---|---|
| 흉내 내는 것 | Mozilla Thunderbird(`thunderbird-bin`) |
| 측정 | Thunderbird 156.0 / 156.0.1(Ubuntu 24.04 snap), 로컬 계정의 작성 창, loopback SMTP peer; idle phase 77 repeat, 입력과 `send` 8 repeat |
| 재현하는 행동 | 평소 초당 약 2번 깨는 조용한 application; key마다 약 5 ms; `send` 하면 약 3초 동안 무거운 작업(operation 창 안에서 잰 component 비율의 합이 초당 약 2,300번. 보내기 사이의 쉬는 시간까지 포함한 op phase 전체로는 초당 750–760번) |
| 핵심 숫자 | `input_run` p50 4.65 ms, 평균 6.05 ms; idle component 15개(합 1.99 wakes/s); `send` 길이 p50 2.897 s, 평균 2.971 s |
| tag | `meas-ci:interactive:2026-09-19`(idle), `meas-ci:interactive:2026-09-27`(입력과 send), `swell-icmi14:outlook-c23`, `meas-ci:desktop:2026-10-04b`(launch) |

Thunderbird 항목은 두 campaign의 값을 합칩니다. idle phase는 `meas-ci:interactive:2026-09-19`의 77 repeat, 입력이 있거나 그 뒤의 phase는 `meas-ci:interactive:2026-09-27`의 8 repeat입니다(9.5 D79, D80). idle phase는 모든 repeat에서 입력 전에 돌기 때문에 이렇게 나눌 수 있습니다.

idle component는 Gecko(Thunderbird의 엔진) thread 이름을 그대로 보입니다. `thunderbird-bin`(0.397/s), `gmain`(0.25/s, gap이 정확히 4.0초), `IPDL Background`, `Timer`, `WebExtensions/WebExtensions`, `JS Watchdog`(1초 gap이 많음), `IndexedDB IO`, `StreamTrans`, … 그리고 73개 comm을 묶은 residual. `send` 동안에는 `Socket Thread` 732/s, `Compositor` 590/s, `thunderbird-bin` 473/s 등 열두 component가 대신 돕니다.

- **`send` operation(9.5 D31, D37, D49).** 짧은 본문과 Word 문서 하나를 첨부한 답장입니다. 첨부는 `office-writer`의 setup 문서를 `.docx`로 저장한 것으로 runner에서 41,555,063 B, peer가 받는 message는 56,946,735 B입니다(Thunderbird가 base64를 72글자 줄로 나눔). 크기와 내용은 design이고, 첨부의 종류는 CpsMark+의 Outlook workload 서술("receive, browse email contents and attachments offline, including Word, Excel, and PowerPoint files … reply")에서 가져왔습니다(`cpsmark-tbench23`). peer는 harness CPU에서 도는 `aiosmtpd`, 인증·TLS 없음. 완료는 Sent 폴더에 사본이 내려앉는 순간입니다(Thunderbird 소스의 `MessageSend.sys.mjs`가 전송 알림 뒤 `_doFcc()`를 await함). 작성 창은 command line(`-compose`)이 아니라 interface 단축키로 엽니다(D37: runner에서 `-compose`가 아무것도 열지 못했음).
- **settle 390초, idle 600초(9.5 D44, D45).** long-phase probe에서 일회성 episode는 30초 settle 뒤 약 340초까지 끝났고, 그 뒤로는 약 60초마다 `StreamTrans` episode가 되풀이됐습니다. 그래서 settle은 390초(design), idle phase는 600초(design)로 했습니다. 600초는 최악의 위치에서도 wake 비율을 5 % 안에(4.6 %) 두는 가장 짧은 길이였습니다.
- **77 repeat(9.5 D94).** Gecko child process의 thread를 별도 component로 나누자(D94), idle pool은 77 repeat가 필요했고, 34개 idle-only repeat를 batch로 더해(창 45–78) 77에서 통과했습니다. 이 34 repeat는 녹화 창이 없으므로 idle phase만 돌았습니다(9.5 D32: "past the end of a recording, repeats continue for the idle phase").
- **녹화가 바닥남.** Outlook 녹화(조건 c2와 c3)는 창이 8개뿐입니다(Outlook stream은 SWELL-KW의 interruption 조건에만 있음, D12). 그래서 per-input 값과 `send` 값은 8 repeat의 반폭과 함께 실리고, 그중 아홉 값은 5 % 밖입니다(예: per-input run 평균 6.052 ms ±10.41 %, `send`의 `StreamTrans` run 평균 ±18.42 %). scope가 하나씩 "the rule needs N repeats"와 함께 적습니다.
- **04:00의 `glean.mps`(9.5 D91).** Thunderbird의 Glean metrics-ping scheduler는 매일 현지 04:00에 한 번 깨는데, 77 repeat 중 하나(repeat 39)의 idle phase가 runner 시계로 04:00을 지나며 2.299 ms run 하나를 잡았습니다. 이것은 "stated, not carried"입니다. residual에서도 뺐습니다.
- **판 섞임.** idle phase는 156.0(43 repeat)과 156.0.1(34 repeat)을 섞습니다. 45개 idle 값 중 43개가 0.78 표준편차 안에서 일치했습니다.
- **stimulus 민감도.** 136M 아래 0.909배(0.824–0.994)로, 이 항목만 반대 방향(덜 비쌈) 차이가 있었습니다. pooled 중간값으로는 +8 %여서 두 읽기가 엇갈리는데, scope는 repeat별 비율을 공식 읽기로 적습니다(9.5 D81).

## 5.5 `web-browser` — Chrome의 text box에 타이핑하고 page 열기

| | |
|---|---|
| 흉내 내는 것 | Google Chrome(`chrome`)의 process tree, 지금 쓰는 page의 renderer 포함 |
| 측정 | Chrome 152.0.7977.82(29 repeat) / 153.0.8010.52(9 repeat), text area와 400 문단이 있는 로컬 page; 38 repeat |
| 재현하는 행동 | 평소 초당 약 43번 깨어남; key마다 약 4 ms; `page-load` 하면 약 0.5초 동안 무거운 작업(operation 창 안의 component 비율 합 초당 약 2,300번); 가끔 50 ms짜리 메모리 점검 |
| 핵심 숫자 | `input_run` p50 4.07 ms, 평균 4.27 ms; idle component 7개(합 43.2 wakes/s); `page-load` 길이 p50 465 ms; `MemoryInfra` heavy event 0.000351/s, run p50 54.4 ms |
| tag | `meas-ci:interactive:2026-09-20`, `swell-icmi14:ie-c1`, `meas-ci:desktop:2026-10-04b`(launch) |

- **입력과 page(9.5 D65, D22).** Internet Explorer 녹화의 key만, page의 text box에 재생합니다. scope: "the archetype carries typing into a page field, not browsing's scrolling and clicking — the page-load operation carries browsing's heavy work". `page-load`는 local server가 내주는 scripted feed page(`feed.html`: 게시물 300개, 1600×1200 그림 30장, 200,000개 record 정렬)를 여는 것이고, 완료는 첫 paint 뒤 page title입니다. page의 종류는 PCMark 10(pp. 52–53)과 CpsMark+ §4.3.3에서, 크기는 design입니다.
- **settle 420초(9.5 D58, 2026-09-20).** Chrome은 켜진 뒤 언젠가 한 번 약 880 ms짜리 `ThreadPoolForeground` run을 합니다. 관측된 시각이 창 열린 뒤 95초부터 300초까지 흩어져 있었습니다. 그래서 settle을 가장 늦은 관측 너머로 420초(design)로 정하고, idle phase에 그 run이 잡힌 repeat는 빼는 guard를 두었습니다. 버린 대안(270초 settle에 잡힌 repeat를 빼기)에 대한 기록된 말: "trading a measurement problem for a selection one".
- **renderer를 모두 싣는다(9.5 D84, 2026-09-28).** 처음에는 Chrome의 renderer process를 모두 빼고 다른 항목에 맡겼습니다. 2026-09-28의 review가 그렇게 하면 지금 쓰는 page의 renderer를 아무 항목도 설명하지 않는다는 것을 찾았습니다. renderer가 key당 CPU의 59 %, page load당 CPU의 74 %를 차지했습니다. 그래서 `web-browser`가 타이핑하는 page의 renderer, page load가 넘겨받는 spare renderer, Chrome 자신의 WebUI renderer를 모두 싣고, 다른 tab의 renderer만 `renderer-hidden`에 남겼습니다. 이 결정으로 idle wake가 21.7–24.3/s에서 40.8–46.3/s로, per-input 평균이 1.671 ms에서 4.274 ms로, page load당 CPU가 91 ms에서 345 ms로 올랐습니다.
- **`MemoryInfra` heavy event(9.5 D64, 2026-09-21).** 20개 session 모두에서 `MemoryInfra`는 약 300초 간격으로 7.7 ms씩 돌았고, 그중 7개 session에서는 아무 때나 53.8–61.2 ms짜리 무거운 pass를 했습니다(20 × 600초에 9번, 약 22분에 한 번). 30 ms 이상 run(design 기준선)을 component에서 빼 heavy event로 실었습니다. 지금 항목은 22,800초의 idle phase에서 8번을 셉니다.
- **녹화가 바닥남.** IE 녹화는 창이 38개입니다. 그래서 38 repeat에서 멈췄고, SWELL-KW 아래 per-input 평균 4.274 ms는 ±5.90 %로 규칙 밖입니다(52 repeat가 필요).
- **판 섞임(9.5 D69, D93).** Google의 repository는 현재 판만 내려줘 152와 153이 섞였습니다. 60개 실린 값 중 59개가 1.80 표준편차 안에서 일치했고, page load의 `gpu/VizCompositorTh` run 평균만 153에서 16 % 짧았습니다(scope에 적힘).
- **첫 page load.** repeat마다 첫 page load가 739 ms, CPU 545 ms로 나머지(평균 485 ms, 341 ms)보다 무거웠습니다. 56번 중 한 번이고 operation CPU의 2.8 %입니다. 실린 값은 56번의 평균입니다(9.5 D87).
- **stimulus 민감도.** 136M 아래 1.338배(1.284–1.392), 차이가 큽니다. scope는 이 차이를 SWELL-KW 선택의 한계로 적습니다.

## 5.6 `image-editor` — GIMP로 큰 사진 다루기

| | |
|---|---|
| 흉내 내는 것 | GNU Image Manipulation Program(`gimp`) |
| 측정 | GIMP 2.10.36(apt), 4952×3288 이미지(16-bit로 열림), scripted pointer loop; 5 repeat |
| 재현하는 행동 | 손대지 않으면 전혀 깨지 않음; 조작 중에는 초당 약 9번; `unsharp-mask` 필터는 약 2.4초 동안 CPU를 거의 다 씀 |
| 핵심 숫자 | idle component 없음(idle wakes 0.0); `focus_components` `gimp` 8.64 wakes/s; `unsharp-mask` 길이 p50 2.358 s; op phase CPU 점유율 0.23 |
| tag | `meas-ci:interactive:2026-09-18` |

GIMP는 idle phase에서 한 번도 깨지 않았습니다(`stats`: "idle wakes/s 0.0–0.0"). 그래서 이 항목만 `components`가 없고 `focus_components`만 있습니다. 사람의 녹화 입력이 없는 application이라(9.5 D5: GIMP와 Kdenlive는 "have no observed input in any class"), drag·click·wheel을 도는 scripted pointer loop(design)로 조작했고, 그때의 리듬이 `focus_components`입니다. key당 run 같은 것은 없습니다.

- **이미지와 필터(9.5 D22).** 이미지 크기는 PCMark 10 Photo Editing의 interactive 이미지 크기(Technical Guide p. 71), 필터는 PCMark 10의 batch unsharp 값을 GIMP의 plug-in 매개변수로 옮긴 것(std-dev 4.0, amount 0.32, threshold 8; p. 74)입니다. 내용은 합성(synthetic)이고 매개변수 옮기기는 design입니다. Script-Fu server로 필터를 걸고 그 응답을 완료로 칩니다.
- **5 repeat, 최소에서 멈춤.** 가장 넓은 값이 ±4.40 %로, 최소 다섯 repeat에서 통과했습니다(9.5 D88: coverage 94.8 %).
- **launch 없음.** core set에서 GIMP를 파일 중간에 켜는 곳이 없습니다.

## 5.7 `video-editor` — Kdenlive로 timeline 다루고 미리보기 렌더링

| | |
|---|---|
| 흉내 내는 것 | Kdenlive(`kdenlive`)와 그 외부 렌더 process `kdenlive_render` |
| 측정 | Kdenlive 23.08.5(apt), 20초 1920×1080 30 fps H.264 clip 하나에 unsharp 효과, scripted pointer loop로 clip monitor 훑기; driven·op 20 repeat, idle 16 repeat |
| 재현하는 행동 | 평소 초당 약 1.3번(1초 tick과 10초 tick); 조작 중 초당 약 210번, CPU 약 37 %; `preview-render`는 약 11.4초 동안 CPU 절반 |
| 핵심 숫자 | idle: `kdenlive` 1.1611/s(gap 약 1.001 s), `Qt bearer threa` 0.1/s(gap 약 10.0 s); focus 합 211 wakes/s; `preview-render` 길이 p50 11.375 s |
| tag | `meas-ci:interactive:2026-09-18`(driven과 op), `meas-ci:interactive:2026-10-05`(idle), `meas-ci:desktop:2026-10-05`(launch) |

- **llvmpipe 제외(9.5 D15, 2026-09-15).** runner에 GPU가 없어 Kdenlive는 Mesa의 software rasteriser `llvmpipe`로 그렸습니다. driven phase CPU의 93 %가 이 llvmpipe thread 넷이었습니다(약 2,240 wakes/s). 이 thread들은 "present only because the runner has no GPU"라서 값에서 뺐습니다. scope는 GPU rasterization을 모델링하지 않는다고 적습니다.
- **clip과 효과(9.5 D22).** clip 형식과 sharpening 매개변수는 PCMark 10 Video Editing(p. 76)에서, 내용은 합성(design)입니다. `preview-render`는 timeline 전체의 미리보기를 Kdenlive의 외부 `kdenlive_render` process가 렌더링하고 그 process가 끝나면 완료입니다. export(내보내기)는 이 항목의 operation이 아니라 `cpu-batch`의 `kdenlive_render` program입니다(6.3절).
- **idle 재측정(9.10 D146, 2026-10-05).** `c1-transcode` 같은 파일이 Kdenlive를 오래 들고 있으므로 긴 span에서 확인하다가, Kdenlive가 켜진 뒤 한참 launch 꼬리 일을 한다는 것이 드러났습니다. idle phase를 다시 쟀습니다. 창 열린 뒤 240초 settle, 180초 phase, 16 repeat(`meas-ci:interactive:2026-10-05`). 2,790초 probe에서 180초 phase는 CPU를 1.1 %, wake를 0.7 % 안에서 수준에 맞췄습니다. launch phase도 새 settle에 맞춰 다시 녹화했습니다(`meas-ci:desktop:2026-10-05`).
- **`c3-creation`의 span으로 다시 읽기(9.15, 2026-10-17).** D146의 2,790초는 `c3-creation`이 이 idle 상태를 붙잡는 2,851초(120초 도착 뒤 240.6초의 launch 재생이 끝나는 360.6초부터 3,212초의 떠남까지)보다 61초 짧았습니다. 인지오의 결정(2026-10-17)으로 그 span보다 긴 탐침을 하나 더 돌렸습니다. `long-probe` family의 `kdenlive` 13(run 38976976741, release `meas-ci-probes-2026-10-17`)이고, 240초 settle 뒤로 2,890초를 담습니다. 9.10 D143의 5 % 기준으로 2,851초(10초 조각으로는 2,860초) 위에서 읽으니, 모든 repeat가 받는 자리의 180초 phase는 탐침의 수준 대비 CPU −0.3 %, wake +2.9 %였고, 가장 나쁜 자리에서도 +4.5 %, +3.8 %였습니다. 180초 phase는 그대로이고 값도 바뀌지 않습니다(탐침은 repeat가 아니고 값을 바꾸지 않음). scope는 이제 D146의 2,790초 대신 이 읽기를 적습니다. "Read over 2,851 s, the span `c3-creation` holds it (2,860 s in whole 10 s slices), in one long-phase probe held 2,890 s past that settle".
- **driven 상태의 변화(9.10 D150, D153).** 두 driven probe 모두 입력 약 20분째 main thread의 wake가 적고 긴 상태(초당 126번, 3.06 ms; 그 전 135–153번, 2.3–2.8 ms)로 들어갔고, 하나는 끝까지 그 상태였습니다. 그 상태에서 CPU는 실린 phase보다 9 % 높고 wake는 14 % 낮았습니다. 결정은 "`video-editor`'s driven span stands; the state some 20 minutes into the input is stated"였습니다.
- **20 repeat(9.5 D88).** 가장 넓은 값인 driven `kdenlive` run 평균이 ±5.00 %(정확히는 ±4.997 %)로 기준선에 붙어 있었고, scope는 "covers the true mean in about 91 % of campaigns"를 적습니다.

## 5.8 재생과 통화: `video-player`, `audio-player`, `video-call`

세 항목은 component 대신 **매체 주기마다 job 하나**를 가집니다(9.5 D75, 2.4절). 셋 다 입력이 없고, 재생이나 통화가 시작되면 끝날 때까지 주기적으로 일합니다.

| 항목 | 흉내 내는 것 | period | `cycle_run` p50 / 평균 / 최대 | 평균 ÷ period(재생 CPU 점유율) | repeat | tag |
|---|---|---|---|---|---|---|
| `video-player` | mpv 0.37.0, `--vo=x11 --ao=null`, 1280×720 30 fps H.264 + AAC 파일 반복 재생 | 33,348 μs | 3.98 / 4.06 / 16.0 ms | 0.1218 | 24 | `meas-ci:playback:2026-09-18` |
| `audio-player` | mpv 0.37.0, `--no-video --ao=null`, 같은 파일의 AAC | 49,635 μs | 0.328 / 0.352 / 2.38 ms | 0.0071 | 31 | `meas-ci:playback:2026-09-18` |
| `video-call` | Chrome 한 page 안의 loopback WebRTC 통화, 가짜 1280×720 30 fps camera와 microphone(`--use-fake-device-for-media-stream`) | 10,001 μs | 1.19 / 2.37 / 18.9 ms | 0.2371 | 45 | `meas-ci:playback:2026-09-20` |

**주기는 측정에서 읽었습니다.** `video-player`의 33.348 ms는 215,884개 cycle의 시작 간격 평균이고(파일 자체의 frame 간격은 33.333 ms), `audio-player`의 49.635 ms는 187,336개, `video-call`의 10.001 ms는 2,159,645개 cycle의 평균입니다. cycle의 시작은 기준 thread의 사건입니다. video는 `vo` thread의 1 ms 이상 frame 복사(16.7 ms 안의 두 번째 복사는 같은 frame으로 침, design), audio는 5 ms 조용한 뒤 `ao`의 첫 wake, 통화는 `utility/AudioWorkerThre`의 wake입니다. 각 cycle의 run은 그 cycle 동안 process tree 전체가 쓴 CPU입니다.

**deadline은 cycle의 것이지 출력 장치의 것이 아닙니다.** 세 scope가 같은 문장을 적습니다. "an audio server buffers ahead of the device (PulseAudio up to 2 s by default …), so a late cycle is not by itself an audible gap or a dropped frame." 기한을 놓친 cycle이 곧바로 소리 끊김이나 frame 누락이라는 뜻은 아니라는 것입니다.

**`video-call`의 포화 episode.** cycle의 약 5.0 %에서 tree 자신의 일이 period를 넘습니다. scope는 이것을 "the call's saturation episodes, one CPU busy for about 30 s every 240 s (D54)"로 설명합니다. 그래서 그 job들은 CPU를 혼자 써도 기한을 놓칩니다. 통화의 video 경로(약 16.7 ms compositing과 30 fps frame)는 따로 job이 없고, 그 CPU는 audio frame cycle 안에서 돕니다.

> **왜 이렇게 정했나 — mpv를 측정(9.5 D11, 2026-09-14).** 예전 `audio-playback`(50 ms마다 5 % CPU)과 `video-playback`(16.7 ms마다 40 % CPU)은 interbench(Con Kolivas의 interactive scheduling benchmark)의 emulation 상수였습니다. 9.5 D11의 기록: interbench의 50 ms 뒤에 있다는 "popular linux audio player"는 2005–2016년의 어느 release에도 이름이 나오지 않고, 60 Hz / 40 % video와 0–100 % X emulation은 code 주석뿐이며, 상수가 바뀐 적이 없고, 그것을 설명하는 peer-review 연구도 없었습니다. 그래서 mpv를 Xvfb 아래 `--vo=x11 --ao=null`로 직접 쟀습니다. null 출력은 "simulates timing of a perfect audio device"입니다(Azure kernel에는 소리 module이 없음).

> **왜 이렇게 정했나 — WebRTC 통화(9.5 D12, 2026-09-14).** runner probe에서 Chrome의 WebRTC loopback 통화를 돌릴 수 있다는 것이 확인되어 `webrtc` 측정이 campaign에 들어왔고, 예전에 `zoom` 음성과 video를 mpv에 묶으려던 계획을 바꿨습니다. 9.10 D14(2026-10-01)는 meeting 파일들이 통화 하나에 `video-call` task 하나를 묶게 했습니다. timeline에서 이 task의 이름은 `chrome`입니다(통화가 Chrome page 안에서 돌기 때문).

> **왜 이렇게 정했나 — 통화의 settle 210초(9.5 D54, 2026-09-20).** 처음의 통화 값은 통화가 자리잡는 동안(ramp-up)의 것이었습니다. long-phase probe 뒤 settle 210초, play phase 480초로 다시 쟀습니다.

> **코드로.** 세 항목은 `compiler.py`의 `_periodic_unroll`이 펼칩니다. task가 사는 동안 `TIMER period` + `RUN`을 주기마다 하나씩, LOOP 없이 평평하게 늘어놓습니다. 실제로 `c1-media`의 `video` task는 `TIMER` 1,800개와 `RUN` 1,800개(60초 ÷ 33.348 ms ≈ 1,799), `music` task는 각 1,209개(60초 ÷ 49.635 ms ≈ 1,209)를 가지며, wake 사건은 하나도 없습니다. launch phase가 있으면 그 동안의 관측 CPU를 cycle 격자에 나눠 담습니다(9.10 D138). 하나의 cycle이 period보다 많은 launch CPU를 받으면 그 cycle은 늦습니다.

# 6장 · compile: make의 spawn table

이 장은 9.6 slice(compile)가 만든 세 항목, `build-orchestrator`, `compiler-child`, `cpu-batch`를 다룹니다. 질문은 "Linux kernel build처럼 짧은 process 수만 개를 쏟아 내는 일을, 그리고 한 프로그램이 CPU를 끝까지 붙잡는 일을 어떻게 적었나"입니다. compile이 scheduler 연구에서 중요한 이유를 9.6 D2는 이렇게 기록합니다. "every source the slice has names the flood of short-lived processes as the trait that makes a build a scheduler workload." 예로 Linux autogroup commit의 "parallel kbuild has a negative impact on desktop interactivity"를 인용합니다(kbuild는 Linux kernel의 build system). 병렬 build가 desktop 반응성을 해친다는 것은 커널 개발자들도 겪은 문제입니다.

세 항목 모두 하나의 campaign `meas-ci:build:2026-09-18`(14 repeat; `cpu-batch`는 나중에 9.10이 다시 쟀음)에서 왔습니다. 측정 대상은 linux-6.6 `defconfig`를 `make -j8`로, 캐시가 따뜻한(warm) 상태에서 build하는 것이었습니다. gcc 13.3.0(Ubuntu 13.3.0-6ubuntu2~24.04.1)이고, kernel의 Makefile에 `-pipe`가 없어서 `cc1`과 `as`가 차례로 돕니다.

## 6.1 `build-orchestrator` — GNU make

| | |
|---|---|
| 흉내 내는 것 | GNU `make`(timeline 이름 `make`) |
| 측정 | linux-6.6 defconfig, `make -j8`, warm, CPU 하나에 고정; 14 repeat |
| 재현하는 행동 | job 하나마다 잠깐 dispatch CPU를 쓰고 자식 여섯을 띄움; 동시에 8 job까지 |
| 핵심 숫자 | `dispatch_overhead` p50 676 μs, 평균 691 μs(±0.94 %); build당 job 5,254개(object 2,908, archive 681, helper 1,537, probe 90, link 38), make process 719개 아래 fork 5,957번; cap 8에서 살아 있는 job 평균 7.87, 최대 11 |
| binding | `spawn_count`, `parallelism_cap`, `child_name` |
| tag | `meas-ci:build:2026-09-18` |

program은 이렇습니다.

```yaml
program:
  - loop:                    # consumes the pre-sampled spawn table, six entries per object job (D19)
      - RUN: dispatch_overhead
      - FORK: {}             # x6, the job's members; blocks on wait-for-slot at the parallelism cap
  - WAIT: children
  - EXIT: {}
```

`dispatch_overhead`는 "make 자신이 fork 사이에 쓴 CPU"이고, build의 모든 make process를 모아 잰 것입니다(9.6 D8 iv). timeline이 `spawn_count`(object job 수)와 `parallelism_cap`(동시 job 수)을 주면, compiler는 job마다 `RUN dispatch` + `FORK`×6을 펼치고, `fork_cap`을 `parallelism_cap` × 6으로 둡니다.

`c1-compile`(C1 그룹의 compile 상황 파일)은 `spawn_count: 2908, parallelism_cap: 8, child_name: cc1`을 줍니다. 측정한 kernel build의 object job 전부입니다. compile된 `build` task는 spawn table 17,448개(2,908 × 6)와 `fork_cap` 48을 가지고, program은 `RUN 229, FORK×6, RUN 1564, FORK×6, …`로 20,358개 명령입니다(compile된 파일을 열어 셈). 이 파일의 editor는 1,594초 동안 머무는데, build가 혼자 끝까지 갈 수 있도록 파일 길이를 job에 맞춘 것입니다(9.10 D17, D141).

> **왜 이렇게 정했나 — `-j8`와 cap 8(9.6 D4, 2026-09-17).** cap의 기본값은 8로 유지하되, 근거를 바꿨습니다. 예전 근거는 "between interbench's documented -j4 and desktop nproc conventions"였는데, 9.6 D4가 기록한 바로는 interbench의 `-j4`는 make를 실제로 돌리지도 않는 emulation의 이름표였고 뒤쪽 절반은 출처가 없었습니다. 새 근거는 build 도구들의 기본값입니다. "every vendor default found is `nproc` or a memory-capped variant"(make, ninja, cargo, dpkg, Debian kernel handbook, rpm, Gentoo, dkms, Phoronix Test Suite). 이 `nproc` 규칙을 8-thread desktop에 적용하면 8입니다. 이름표는 "convention, grounds cited", binding 때 바꿀 수 있습니다. 문헌에서 관측된 desktop build 하나(O'Callahan 등의 rr 논문, Dell XPS15 8-thread laptop)도 `-j8`이었습니다. CPU 하나에 묶으면 `nproc`이 1이 되므로 workflow는 `-j8`을 명시합니다.

> **왜 이렇게 정했나 — `-j8`의 비용은 진술된 한계(9.6 D4, D9; 9.6 D32).** 같은 run에 `-j1` phase를 미리 등록한 불변성 검사로 넣었습니다. 결과: `-j1`에서 `cc1`의 process당 CPU는 `-j8`의 0.90배(repeat별 0.87–0.92)였습니다. 즉 CPU 하나에서 `-j8`로 돌리면 compile당 CPU가 약 10 % 더 듭니다. 미리 정한 대로 이것은 재결정이 아니라 "a stated limitation of these values"로 scope에 적혔고, 3.4절의 5 % 기준선이 바로 이 10 %의 절반입니다. venue가 측정값에 주는 영향 전반에 대해서는 9.6 D32(2026-09-20)가 "The venue's effect is untested, and the test belongs to the consumer"라고 적고, 9.14(dataset을 쓰는 쪽의 rework)에 민감도 검사를 넘겼습니다. 2026-10-09의 9.14 decision 10이 그 검사를 `venue-x0.8`/`venue-x1.25` variant로 만들었습니다(12.2절). 판정 파일 19개의 측정된 RUN을 공통 배율로 위아래로 바꿔 판정이 바뀌는지 보는 검사입니다.

> **왜 이렇게 정했나 — 나머지 job은 모델링하지 않음(9.6 D9, 2026-09-18).** build의 job 5,254개 중 object job 2,908개만 spawn table에 넣습니다. archive 681, helper 1,537, probe 90, link 38개는 "unmodelled per build"이고, 합쳐서 build CPU의 3 % 미만입니다. 기록된 이유: 다른 job 종류의 비율은 "kbuild's for this tree"여서 다른 build로 옮겨지지 않습니다.

> **왜 이렇게 정했나 — `spawn_count`는 측정 build 전체(9.10 D18, 2026-10-01).** `modeling_notes`의 마지막 문장은 옛 사정을 남깁니다. "`spawn_count` was bound when a spawn-table entry was one process of about 89 ms; a job is now six processes of about 453 ms, and the counts are 9.10's to resize." 9.10 D18이 "the user's build runs the measured kernel build whole: 2,908 object jobs at cap 8"로 정했고, 9.10 D17이 그 일반 규칙을 정했습니다. "a batch job in a core-set file runs its measured whole, at the input its decision fixed … No `total_work` or `spawn_count` describes part of a job." 기록된 이유: "how large a user's job is has no source", 그리고 입력을 파일 길이에 맞춰 줄이면 근거 있는 입력이 design으로 바뀝니다.

`dkms` binding의 옛 이야기도 있습니다. 9.6 D6(2026-09-17)은 원래 `c7-compile`의 DKMS module 재빌드를 이 항목으로 대신하고, 측정 run에 작은 DKMS module build를 구조 검사로 넣었습니다(같은 여섯-process 사슬, driver 이름 `gcc-13`, `-j1`의 object job 셋, `cc1` 288 ms 대 kernel의 365 ms). 지금은 9.10이 실제 NVIDIA module의 DKMS build를 따로 재어 `module-build-orchestrator`를 만들었으므로(7.8절), 이 binding은 쓰이지 않습니다. `build-orchestrator`의 `modeling_notes`는 그 구조 검사 문장을 아직 담고 있습니다.

## 6.2 `compiler-child` — object job 하나의 여섯 process

| | |
|---|---|
| 흉내 내는 것 | object job 하나를 이루는 `sh`, `gcc`, `cc1`, `as`, `fixdep`, `rm` |
| 측정 | `build-orchestrator`와 같은 build; build마다 2,908개 object job 중 2,857개가 정확히 이 여섯 member |
| 재현하는 행동 | `sh`가 `gcc`를 깨우고, `gcc`가 `cc1`과 `as`를 차례로 깨우고, `sh`가 `fixdep`과 `rm`을 깨우는 순서; 거의 모든 CPU는 `cc1` |
| 핵심 숫자 | `cc1_step_1` p50 367.6 ms, 평균 439.1 ms(±0.78 %), p99.9 4.0 s; `as` p50 3.05 ms; `fixdep` p50 5.65 ms; `gcc_step_1` p50 1.74 ms; `sh_step_1` p50 766 μs; `rm` p50 1.04 ms |
| tag | `meas-ci:build:2026-09-18` |

pattern은 사람이 읽으라고 쓴 구조 설명입니다(compiler가 실제 program을 만듦).

```yaml
program:  # one object job, six members forked together, woken in D2's order
  - sh:     [RUN, WAKE gcc, WAIT, RUN, WAKE fixdep, WAIT, RUN, WAKE rm, WAIT, RUN, WAKE each member, EXIT]
  - gcc:    [WAIT, RUN, WAKE cc1, WAIT, RUN, WAKE as, WAIT, RUN, WAKE sh, WAIT, EXIT]
  - cc1:    [WAIT, RUN, WAKE gcc, WAIT, EXIT]
  - as:     [WAIT, RUN, WAKE gcc, WAIT, EXIT]
  - fixdep: [WAIT, RUN, WAKE sh, WAIT, EXIT]
  - rm:     [WAIT, RUN, WAKE sh, WAIT, EXIT]
```

job 하나의 깨어나는 순서는 `sh` → `gcc` → `cc1` → `gcc` → `as` → `gcc` → `sh` → `fixdep` → `sh` → `rm` → `sh`입니다. 일을 마친 member는 CPU 없이 기다리다가, `sh`가 job을 끝낼 때 함께 끝납니다. compile된 `c1-compile`에서 job 1의 `sh`는 `RUN 848, WAKE build.j1.gcc, WAIT job:build.j1.sh, …`로, `gcc`는 `WAIT job:build.j1.gcc, RUN 1731, WAKE build.j1.cc1, …`로 시작합니다.

> **왜 이렇게 정했나 — 단위는 make job 하나(9.6 D2, 2026-09-17).** 예전 `compiler-child`는 "compiler 자식" 하나를 짧은 process 하나로 적었습니다. 9.6 D2는 단위를 make job 하나, 즉 그 job이 돌리는 process 사슬로 바꿨습니다. 이유: Brendan Gregg가 공개한 build의 1초짜리 `perf sched` 기록(9.6 search 후보 S3-01; 숫자는 옮겨 싣지 않음)에서 `cc1`이 CPU의 약 93 %(`cc1` 6,013 ms 대 `gcc` 44, `as` 122, `sh` 107, `fixdep` 81, `make` 54 ms)를 쓰는데, `cc1`만 남기면 "discarding the population", 즉 짧은 process가 쏟아지는 성질 자체를 버립니다. 구조는 프로그램 자신의 소스에서 읽었습니다(kbuild v6.6의 `scripts/Makefile.build`, GCC 13.2.0의 `gcc/gcc.cc`, GNU make 4.4.1의 `src/job.c`). "the run wins any disagreement with the reading" — 소스 읽기와 측정이 다르면 측정을 따릅니다. parallelism cap은 make의 jobserver(`make -jN`의 동시 job 수를 세는 장치)처럼 job(shell) 수를 셉니다.

> **왜 이렇게 정했나 — 연속한 spawn table 항목 여섯(9.6 D19, 2026-09-19).** 처음(9.6 D9)에는 spawn table 항목 하나가 compile 때 여섯 member로 펼쳐지는 chain constructor를 생각했습니다. 그런데 workload 형식은 최상위 task만 task를 만들 수 있게 되어 있고(자식에게는 spawn table이 없음), simulator가 읽는 run file과 recognizer가 보는 visible projection은 2026-09-06에 freeze되어 바꿀 수 없었습니다. 그래서 job 하나를 `build-orchestrator`의 연속한 spawn table 항목 여섯으로 적고, WAIT/WAKE로 순서를 이었습니다. 기록은 무엇이 정확하고 무엇이 근사인지도 적습니다. 정확한 것: member의 순서, CPU, wake당 run, 동시 job 수, build의 turnaround. 근사인 것: member의 trace상 도착과 끝은 job의 것이지 process 수명이 아니고, 기다리는 member는 `ready_wait`를 쌓지 않습니다. recognizer의 시야는 바뀌지 않습니다(visible projection은 spawn table의 이름과 개수를 부모 수명에 붙여 보임).

> **왜 이렇게 정했나 — structural step(9.6 D20, 2026-09-19).** member마다 "자기 자식의 fork와 exit로 나뉜 구간"마다 한 번씩 RUN합니다(`sh` 넷, `gcc` 셋, 나머지 하나). 기록된 이유: repeat 4의 2,857개 job에서 넷은 거의 항상 한 번 깨는데(`cc1` 99.3 %), `sh`는 5–7번, `gcc`는 4–7번 깨고, 첫 run이 크고(중간값 0.72 ms와 1.70 ms) 뒤의 run은 작았습니다(0.01–0.34 ms). "so one table per role describes neither." 그래서 (role, step)마다 table 하나, 모두 열한 개입니다. `modeling_notes`는 정직하게 적습니다. 모델의 4와 3은 구조이지 wake 횟수가 아니고, step과 member는 서로 독립으로 뽑힙니다.

> **왜 이렇게 정했나 — 문헌은 존재만 받친다.** `modeling_notes`: "The literature grounds only that a parallel build forks and execs many processes, mostly short-lived: ocallahan-atc17's "make forks and execs 2430 processes, mostly short-lived" (sec-4.3) counts every process a `make -j8` build of DynamoRio 6.1.0 forks and execs (sec-4.1), and says nothing of what they run; coetzee-arxiv12 names the Linux kernel build's many short-lived processes, its examples `cp` and `mkdir`, with no count (sec-9)". 숫자는 하나도 문헌에서 오지 않습니다. 2026-09-13의 critical findings memo(A1)가 밝혔듯, O'Callahan의 2,430 process는 Linux kernel build가 아니라 DynamoRio 6.1.0의 build였습니다(§4.1: "make builds DynamoRio [8] (version 6.1.0) with make -j8"). 이 인용은 병렬 build가 짧게 사는 process를 많이 fork하고 exec한다는 것만 받칩니다. 2,430은 그 build가 fork하고 exec한 모든 process의 수이고, 논문은 그것들이 무엇을 실행하는지 말하지 않습니다. Coetzee의 문장도 실제로 말하는 짧은 process는 compiler가 아니라 `cp`와 `mkdir`이었습니다(memo A4). 2026-10-16까지의 메모는 두 논문을 "The kernel-build literature"로 묶고 Coetzee가 "corroborates"한다고 적었고, 2026-10-17에 9.15의 재빌드(commit `7b024003`)가 출처 등록부(`dataset/sources.yaml`)의 메모에 맞춰 "grounds the class's existence and short-lived character only"로 고쳤고, 같은 날 9.16의 재빌드(commit `17f28d7f`)가 출구 감사의 claim trace대로 위의 문장으로 고쳤습니다. 우리 측정의 kernel build는 build당 29,035개 process를 띄웠습니다(9.6 D9).

warm 캐시만 싣습니다. 캐시를 비운(cold) 상태에서는 `cc1`이 중간값으로 두 번 깨고 깰 때마다 183 μs의 디스크 대기가 있었는데, 이것은 "reported beside the pool and not carried"입니다(9.6 D8 iii, D9). 9.6 D5(2026-09-17)는 archetype이 warm `-j8` phase를 읽고, cold 수치는 campaign 결과에 남기며, timeline이 어느 상황을 그릴지는 9.10의 몫이라고 적습니다. build에 대해 warm을 고른 이유를 따로 적은 문장은 없습니다(기록된 이유는 없습니다). backup과 archive에 대해 같은 선택을 하며 9.7 D8이 든 이유는 7.2절에서 봅니다.

## 6.3 `cpu-batch` — 한 thread가 CPU를 끝까지 붙잡는 job

| | |
|---|---|
| 흉내 내는 것 | 지배적인 thread 하나로 job이 끝날 때까지 runnable인 batch 프로그램 |
| program 셋 | `python3`(PyTorch MNIST 학습, 이름 `python`), `kdenlive_render`(Kdenlive export), `spoof`(이름만 `chrome`인 hog, design) |
| 재현하는 행동 | 거의 쉬지 않고 CPU를 씀; 프로그램마다 다른 "쉬지 않고 쓰는 길이"와 짧은 멈춤 |
| binding | `total_work`, `program` |
| tag | `meas-ci:background:2026-10-03`(`python3`), `meas-ci:background:2026-10-03c`(`kdenlive_render`) |

`cpu-batch`는 batch-loop(2.5절) 항목인데, table 묶음이 프로그램마다 따로 있습니다. timeline이 `program`으로 고릅니다.

**`python3` — PyTorch의 기본 MNIST 예제.** PyTorch 공식 `pytorch/examples`(commit `acc295d`)의 "Basic MNIST Example"을 기본값 그대로(`python main.py --save-model`: batch 64로 14 epoch, epoch마다 test pass, checkpoint 저장), `torch` 2.14.0의 CPU build로, intra-op thread 하나로 돌렸습니다. process 하나, thread 하나이고 이름은 `python`입니다(venv가 실행하는 이름, 9.10 D84). 6 repeat.

| 값 | 측정 |
|---|---|
| job 전체 CPU | 1,389.885 s ±4.04 %(1,293.8–1,455.8 s) |
| 포화도 | 0.99988–0.99991 |
| voluntary block 사이 run | 평균 69.49 s ±27.3 %(repeat당 53.9–114.9 s) |
| run당 block | 311.5 μs ±10.8 % |
| block 수 | repeat당 11–24개; 처음 두 번의 sleep 말고는 모두 `khugepaged`가 끝냄 |

`python3_run` table의 중간값은 228 ms이지만 p75가 43.5초, 최대가 1,006초입니다. 학습은 몇십 초씩 끊김 없이 돌고, 가끔 커널의 huge page 정리(`khugepaged`)가 잠깐 막을 때만 멈춥니다. 그래서 block 값 둘은 "machine 따라 흩어짐" 예외로 반폭과 함께 실립니다.

> **왜 이렇게 정했나 — MNIST(9.10 D12, 2026-10-01).** 예전 `python3`는 "a PyTorch 2.14 CPU training loop of 300 steps over synthetic images"였습니다. 9.6 D32는 그것이 실제 학습이 아니라 CPU를 포화시키는 batch task의 대역이라고 범위를 좁혔고, 9.10 D12가 PyTorch 자신의 예제로 바꿨습니다. 기록된 이유: 관측된 desktop ML 학습 workload를 찾지 못했고(Procyon은 inference를 잼), "A definition that is not ours". 주장하지 않는 것도 적었습니다. desktop 사용자가 MNIST를 학습한다는 주장은 하지 않고, GPU 학습은 runner에서 관측할 수 없습니다. `sources.yaml`의 `pytorch-examples` notes: "Identifies the job; no claim about what or how often desktop users train."

> **왜 이렇게 정했나 — huge page 설정은 runner의 것(9.10 D87, D88, 2026-10-03).** runner의 커널은 transparent huge pages(THP, 큰 memory page를 자동으로 쓰는 기능)를 `always` 모드로 돌리는데, Ubuntu desktop 커널의 기본값은 `madvise`입니다. 9.10 D87은 runner의 모드를 그대로 두고 측정하되, `madvise`로 다섯 job을 따로 돌려 보기로 했습니다. 결과(D88): `madvise`에서 같은 학습이 CPU를 1.144배(95 % 구간 ×1.102–×1.185) 더 썼고, 시작의 두 sleep 말고는 block이 없었습니다. 결정은 "D87 kept"입니다. 실린 값은 runner(`always`)의 것이고, desktop 기본 설정이면 job이 약 14 % 더 길다는 것이 scope에 한계로 적혀 있습니다. `video-transcoder`의 scope도 같은 THP 차이를 적습니다.

**`kdenlive_render` — Kdenlive의 export.** `video-editor` 항목의 project(20초 1920×1080 30 fps H.264 clip에 unsharp 효과)를 Kdenlive의 render dialog로, 기본 profile MP4-H264/AAC(x264 `veryfast`, CRF 23, GOP 15, AAC 160 kb/s, processing thread 하나)로 내보내는 job입니다. dialog가 띄우는 `kdenlive_render`와 그것이 돌리는 `melt-7`의 tree이고, task 이름은 tree의 뿌리인 `kdenlive_render`입니다. 30 repeat.

| 값 | 측정 |
|---|---|
| job 전체 CPU | 16.545 s ±0.8 %(16.055–17.305 s) |
| 포화도 | 0.9920–0.9946 |
| voluntary block 사이 run | 1.932 ms ±0.8 % |
| run당 block | 4.593 μs ±13.1 %(1 μs 바닥 안) |
| 구성 | process 4개 thread 14개; `melt-7`이 CPU의 0.996, 가장 바쁜 thread 0.682–0.691 |
| 출력 | 매번 같은 결과: 1920×1080 H.264 600 frame, 966,107 B |

> **왜 이렇게 정했나 — export는 Kdenlive 자신의 것(9.10 D10, D105, 2026-10-01/03).** 예전 render 파일들은 `ffmpeg`로 생성 clip 60초를 encode하는 것을 묶었습니다. 9.10 D10의 기록: "ffmpeg (render children)"에는 출처가 없었고, Kdenlive는 실제로 외부 `kdenlive_render` process로 렌더링하며, project는 이미 측정된 상태(`video-editor`)가 있었습니다. 9.10 D105는 이 export가 9.6 D7의 공유 기준(지배적인 thread 하나로 job 내내 runnable)을 만족하므로 `cpu-batch`의 새 program으로 넣고, `ffmpeg` table을 지웠습니다.

> **왜 이렇게 정했나 — block은 repeat를 더해 해결(9.10 D109, 2026-10-03).** 첫 다섯 repeat에서 run당 block 평균이 4.91, 0.21, 5.56, 5.47, 0.74 μs로 ±98 % 흩어졌습니다. 원인은 repeat 1, 3, 4가 약 16.39초에 40.05 ms짜리 block 하나로 끝난다는 것이었습니다. melt의 `-progress` loop가 40 ms씩 잠들기 때문입니다(MLT 7.22.0 `melt.c`). 이 흩어짐은 machine이 아니라 프로그램 자신의 timer이므로 "machine 따라 흩어짐" 예외가 맞지 않았고, pool의 예측대로 30 repeat까지 돌려 해결했습니다. 지금 30 repeat 중 26개가 40 ms block 하나로 끝납니다.

**`spoof` — 이름만 `chrome`인 hog.** `program: spoof`는 측정값이 아니라 design입니다. `total_work`만큼 한 번에 RUN하고 EXIT합니다(`compiler.py`: "the chrome spoof is one uninterrupted RUN by construction (D7)"). core set의 `c6-spoof` 파일(C6 그룹, 즉 이름 기반 인식의 한계를 일부러 보이는 그룹의 파일)이 `chrome`이라는 이름의 task에 `total_work: 30s, program: spoof`를 묶어, 이름은 browser인데 행동은 CPU hog인 상황을 만듭니다. timeline의 source 지도도 둘 다 `design`입니다.

> **왜 이렇게 정했나 — `cpu-batch`를 공유하는 기준(9.6 D7, 2026-09-17).** `cpu-batch`는 원래 interbench의 Burn load(완전히 CPU에 묶인 thread 여럿이 benchmark가 멈출 때까지 도는 load)에 기댄, 저장소 자신의 한 줄 "a process that simply computes until it is done"(`docs/data-contracts.md`)이었습니다. 9.6 D7은 그 주장을 묶인 프로그램들 자신의 관측으로 바꾸고, 공유 기준을 측정 전에 적었습니다. "programs share `cpu-batch` when each is runnable for the whole of its lifetime on one dominant thread; a program showing a distinct shape — sustained I/O waits or several equal threads — gets its own entry." 이 기준 때문에 나중에 HandBrakeCLI(지배적 thread 없음, 9.10 D97), Tracker(포화도 0.659, 9.10 D70), Déjà Dup(지배적 thread 없음, 9.10 D119)이 각자의 항목으로 나갔습니다(7장).

`cpu-batch`에 한때 있었던 program들의 행방은 `modeling_notes`가 적습니다. `tracker`는 `file-indexer`로(9.10 D70), `handbrakecli`는 `video-transcoder`로(9.10 D97), `ffmpeg`은 `kdenlive_render`로 바뀌며 사라졌고(9.10 D10, D105), `clamscan`(kernel `Documentation` 검사, `meas-ci:build:2026-09-18`)은 9.10이 원치 않는 검사를 `package-upgrade`로 바꾸면서 묶는 파일이 없어져 table이 지워졌습니다(9.10 D3, D45).

# 7장 · background와 IO: 혼자 끝까지 도는 job들

이 장은 사용자가 화면 앞에서 다른 일을 하는 동안 뒤에서 도는 job들을 다룹니다. 압축(`file-archiver`), 게임 다운로드(`game-download`, `game-download-idle`), 보안 업데이트(`package-upgrade`), 파일 색인(`file-indexer`), 동영상 변환(`video-transcoder`), 정기 backup(`incremental-backup`), kernel module 재빌드(`module-build-orchestrator`, `module-compiler-child`)입니다. 앞의 셋(`file-archiver`, `game-download`와 그 idle 변형)은 9.7 slice가, 나머지는 9.10 slice가 2026-10-01부터 2026-10-04 사이에 새로 쟀습니다.

이 장의 질문은 "배경 job의 무엇이 scheduler에게 중요하고, 그것을 어떻게 적었나"입니다. 배경 job은 대개 CPU를 끝까지 원하므로, 중요한 것은 두 가지입니다. 첫째, 일의 **총량**(`total_work`, job이 끝나려면 필요한 CPU). 둘째, 그 CPU를 **어떤 리듬으로** 쓰는가(얼마나 오래 쉬지 않고 쓰고, 얼마나 자주 스스로 멈추는가). MLFQ 같은 정책은 이 리듬을 보고 task를 분류하기 때문입니다(2.5절). 그래서 여기의 batch-loop 항목들은 모두 `<program>_run`과 `<program>_block` 두 table과 `total_work` 하나로 적힙니다.

## 7.1 batch-loop 항목들을 나란히

| 항목 | 흉내 내는 것 | timeline 이름 | job 전체 CPU | run between blocks(평균) | 포화도 | repeat | class | tag |
|---|---|---|---|---|---|---|---|---|
| `file-archiver` | 7-Zip 23.01 `-mmt8`, Mahoney 10 GB set | `7z` | 4,882–5,283 s | 4.187 ms | 1.000 | 6 | normal | `meas-ci:background:2026-09-19` |
| `game-download` | SteamCMD, TF2 dedicated server depot 10.4 GB | `steam` | 697–761 s | 162.7 μs | 0.907–0.958 | 30 | normal | `meas-ci:background:2026-09-19` |
| `game-download-idle` | 위와 같음 | `steam` | 위와 같음 | 위와 같음 | 위와 같음 | 위와 같음 | **idle** | 위와 같음 |
| `package-upgrade` | Ubuntu 24.04 unattended upgrade의 install 단계 | `unattended-upgr` | 26.385 s ±3.78 % | 1.798 ms | 0.990–0.994 | 9 | normal | `meas-ci:background:2026-10-01` |
| `file-indexer` | Tracker Miners 3.7.1의 첫 색인 | `tracker-miner-f` | 39.435 s ±0.28 % | 1.876 ms | 0.655–0.676 | 18 | **idle** | `meas-ci:background:2026-10-02b` |
| `video-transcoder` | HandBrakeCLI 1.7.2, Big Buck Bunny 4K → 1080p | `HandBrakeCLI` | 2,970.871 s ±2.6 % | 4.002 ms | 0.99938–0.99947 | 5 | normal | `meas-ci:background:2026-10-03b` |
| `incremental-backup` | Déjà Dup 45.2 / duplicity 2.1.4 주간 incremental | `deja-dup` | 165.668 s ±0.56 % | 1.966 ms | 0.9935–0.9952 | 28 | **idle** | `meas-ci:background:2026-10-04` |

(값은 각 항목의 `validation_stats.stats`에서. `file-archiver`와 `game-download`의 CPU는 repeat별 범위입니다.)

몇 가지 공통 결정을 먼저 적습니다.

> **왜 이렇게 정했나 — job은 측정한 전체를 돈다(9.10 D17, 2026-10-01).** core set 파일의 batch job은 측정한 job 전체를, 그 결정이 정한 입력으로 돌고, 파일과 segment의 길이가 job을 따라 늘어납니다. "No `total_work` or `spawn_count` describes part of a job." 기록된 이유: 사용자의 job이 얼마나 큰지에 대한 출처가 없고("item 56"), 2026-10의 audit가 `c1-backup`의 옛 `borg`가 60초 파일 안에서 혼자서도 끝나지 못한다는 것(132.2초 필요)을 찾았으며, 입력을 파일에 맞춰 줄이면 근거 있는 입력이 design으로 바뀝니다. 그래서 위 표의 "job 전체 CPU"가 곧 timeline이 `total_work`로 묶는 값입니다(예: `c1-transcode`의 `HandBrakeCLI`, `c1-indexing`의 39.435 s). 예외 하나: `c4-office`의 `7z` burst는 6초(design)입니다. 9.10 D161(2026-10-06)이 "an exception to D17 for injections"로 정했습니다. C4 그룹(C1 파일을 복제해 segment 중간에 낯선 process를 끼워 넣고 원본과 짝지은 distractor 그룹)에서 끼워 넣기는 Phase 9 decision 3에 따라 실험 자신의 개입이므로 그 크기는 design입니다. 버린 대안은 둘이었습니다. `7z`를 전부 돌리면 `c4-office`가 약 5,100초로 늘어나 60초짜리 `c1-office`와의 짝이 깨지고, 더 작은 입력으로 7-Zip을 다시 재면 그 입력 크기를 정할 출처가 없습니다.

> **왜 이렇게 정했나 — 단계 순서는 싣지 않는다.** batch loop는 run을 서로 독립으로 뽑으므로, job 안의 단계 순서는 사라집니다. `package-upgrade`의 `modeling_notes`가 예를 듭니다. "the `localedef` runs (above the 99.9th percentile, over 1 s each) fall anywhere in the job rather than in one 20 s stretch." 실제로는 locale 생성이 20초 동안 몰려 있지만, compile된 job에서는 긴 run들이 아무 데나 흩어집니다. `file-indexer`와 `incremental-backup`도 같은 문장을 적습니다.

## 7.2 `file-archiver` — 7-Zip으로 10 GB 압축

**무엇.** 7-Zip 23.01(Ubuntu 24.04의 `7zip` package)이 기본 형식과 수준에 thread 여덟(`-mmt8`)으로 Matt Mahoney의 10 GB benchmark set을 압축합니다. set은 Windows laptop 한 대에서 2009–2013년에 모인 79,431개 파일, 4,006개 directory, 10¹⁰ byte입니다. 캐시에 올린 상태(cached fraction 1.0)에서, 압축본은 runner 디스크에 씁니다.

**행동.** 34개 thread가 모두 comm `7z`이고, CPU 하나 위에서 job 내내 CPU를 100 % 씁니다. block은 모든 percentile에서 0입니다. 다른 thread가 거의 항상 이어서 돌기 때문입니다. 그래서 compile하면 거의 끊김 없는 RUN이 됩니다. thread는 두 종류입니다. 넷이 CPU의 약 70 %를 0.15–0.45초짜리 run으로 쓰고, 넷은 wake당 약 1 ms로 꾸준히 돕니다. 이 둘이 표 하나로 납작해졌다는 것이 `modeling_notes`의 한계 문장입니다.

> **왜 이렇게 정했나 — program마다 항목(9.7 D1, 2026-09-19).** 예전 `io-stream`은 `rsync`와 `tar`의 측정값으로 backup, archive, 동영상 변환 등을 모두 대표했습니다. 9.7 D1은 이것을 묶인 program마다 하나로 나눴습니다. 이유: "the bound programs' documented structure differs from the programs `meas-ci:cli:3` measured" — borg는 process 하나에 worker thread 없음, 7-Zip은 기본으로 여러 thread, rsync는 pipe로 이은 process 셋입니다.

> **왜 이렇게 정했나 — 입력은 Mahoney set(9.7 D7, 2026-09-19).** backup이나 archive workload를 정의한 benchmark도, Linux desktop home의 파일별 내용 데이터셋도 찾지 못했습니다. 이 set은 "the one downloadable real user file tree with its content"이고 licence가 benchmarking을 허락합니다. 한계도 기록했습니다. 한 사용자의 Windows laptop이고 구성이 특이합니다(인간 유전체 FASTA 3,240 MB, 압축 benchmark 1,998 MB). 그래서 미리 등록한 set 검사를 scope에 적습니다. 파일 크기 중간값 2,891 B(GNU/Linux 사용자 연구의 4,707 B 대비), 30 MB 넘는 파일의 byte 비율 0.606(2009년 Windows 모집단의 절반 대비).

> **왜 이렇게 정했나 — warm(9.7 D8)과 thread 여덟(9.7 D9).** warm을 읽는 이유: cold phase의 읽기 대기는 consumer drive가 아니라 "SSD"로만 문서화된 runner 디스크를 재게 되고, desktop backup의 캐시 상태를 말하는 출처가 없으며, runner의 16 GB memory가 set 대부분을 담습니다. cold 수치는 결과에 남겼습니다. thread 여덟인 이유: 7-Zip은 machine의 CPU 수에 맞춰 thread를 정하는데, CPU 하나에 묶으면 CPU 하나짜리 machine을 그리게 되므로 9.6 D4의 "8-thread desktop의 `nproc`" 규칙을 따랐습니다.

> **왜 이렇게 정했나 — 한 CPU에 thread 여덟은 진술된 한계(9.7 D15, D23).** 여덟 thread가 한 CPU를 나눠 쓰는데, desktop에서는 대부분 나란히 돌 것입니다. 미리 등록한 검사(9.7 D15, D23): 모든 repeat에서 thread 여덟이 byte당 CPU를 thread 하나보다 1.04–1.10배 더 썼습니다. 또 thread 하나짜리 검사에서 한 thread가 두 방식 중 하나를 보였는데(repeat 1, 2, 6은 중간 gap 0.36–0.39초에 906–941 wake, repeat 3, 4, 5는 0.40–0.74 ms에 1,246–1,575 wake), 원인은 밝혀지지 않았습니다("for a cause not identified").

## 7.3 `game-download` — SteamCMD로 게임 설치 파일 받기

**무엇.** SteamCMD(build 1788292693)를 익명으로 로그인해, Team Fortress 2 Dedicated Server depot(app 232250, build 24245063)을 새로 설치합니다. 10.4 GB를 받아 14.9 GB를 설치합니다. 링크는 121.0 Mbps로 조였고(`htb` root와 `fq_codel` leaf, kernel 기본값), 30 repeat입니다.

**행동.** 약 1 MB chunk를 받아 복호화하고 압축을 풀고 쓰는 일을 반복하며, consumer 속도에서 CPU를 91–96 % 씁니다. 83–84개 thread가 한 component로 묶였습니다. 두 content-update thread가 CPU의 약 71 %를 약 14 ms run으로 쓰고, 다섯 HTTP thread가 wake의 36 %와 CPU의 6 %를 짧은 run으로 씁니다. run 사이 block은 run의 95–98 % 뒤에서 0입니다.

**숫자.** run between blocks 평균 162.7 μs ±2.21 %, run당 block 9.31 μs, job CPU 697–761 s(760–822 s 동안), 받은 양 10.59–10.68 GB를 payload 115.3–115.8 Mbps로. 보고만 하고 싣지 않는 값: network wait 220.6 μs, wake당 byte 3,937 B.

> **왜 이렇게 정했나 — SteamCMD로 재고 `steam`에 묶는다(9.7 D4, 2026-09-19).** desktop Steam client는 로그인한 계정이 필요하고, 계정을 쓰지 않는다는 규칙이 있습니다. 같은 content system을 쓰는 Valve 자신의 packaged client인 SteamCMD를 쟀고, timeline의 `steam` task는 이 숫자를 "stated approximation"으로 가져갑니다. `modeling_notes`는 오차의 방향조차 모른다고 적습니다. "The search records hold no observation of the desktop client's download CPU at a stated rate (D4), so the direction of the error is not measured; the binding is design."

> **왜 이렇게 정했나 — 121.0 Mbps(9.7 D11, 2026-09-19).** Valve가 공개한 국가별 "Average Download Rate"를 받은 byte로 가중한 중간값입니다(238개 국가 행; 2026-09-19 04:44 UTC에 받은 판). 받은 byte가 모집단의 올바른 가중치라는 것이 기록된 이유이고, 다른 표 읽기(network 표의 가중 중간값 128.9, 국가 가중 평균 131.3)도 7 % 안이었습니다. 버린 대안은 비가중 중간값 65.7 Mbps 등입니다. Azure 링크 자체는 VM당 12,500 Mbps 상한이라 desktop 대역폭이 아니고, client는 속도가 오르면 연결을 늘리므로 속도가 구조를 바꿉니다(D10). 그래서 조인 링크를 읽습니다.

> **왜 이렇게 정했나 — `fq_codel`을 유지하고, 링크 모델이 값을 움직인다는 것을 적음(9.7 D25, 2026-09-20).** 조이는 방식을 token bucket에서 `fq_codel` queue로 바꾸자 repeat 사이 흩어짐이 크게 줄었습니다(network wait의 변동계수 20.5 %→1.9 %). 그러나 두 방식의 값 차이도 컸습니다. token bucket 아래 network wait +43 %, wake당 byte +35 %, wake당 run +17 %. `modeling_notes`: "a far larger effect than 9.5 D23's stimulus sensitivity (+1 % to +12 %), so the queue discipline moves this archetype more than the choice of recording moved those." 그리고 "no source here establishes that consumer equipment manages its queue this way". 실제 가정용 장비가 `fq_codel`처럼 queue를 관리한다는 근거는 없다는 것입니다. 링크의 지연도 runner가 Valve server까지 가는 경로 그대로여서 통제되지 않았습니다. repeat들은 runner가 뽑은 Steam site에 따라 갈렸고(서부 14, 동부 13, 중부 3), 지역이 network wait 분산의 64 %를 설명했습니다.

> **왜 이렇게 정했나 — 새 설치만(9.7 D12; 9.10 D7).** update(이미 설치한 게임의 갱신)는 새 chunk만 받아 binary delta로 고치므로 다른 일입니다. 익명으로 이전 공개 build를 설치할 수 있는지 probe했지만 불가능했습니다(9.7 D20 (3)). 그래서 새 설치만 싣습니다. 9.10 D7(2026-10-01)은 이 측정에 맞춰 `c2-p2a`의 다운로드가 그리는 상황을 고쳤습니다. 게임 중의 배경 update가 아니라 "the user starting to install another game while playing — wanted, `initiated: user`". 근거: Steam은 게임이 켜지면 다운로드를 기본으로 멈추고(Valve FAQ), 게임 중 Install을 누르면 바로 받기 시작합니다(steam-for-linux issue #8821). `c2-p2a`는 60초에 이 task를 띄우고 `total_work: 727.170s`(새 설치의 CPU 전체, 9.10 D142)를 묶습니다.

> **왜 이렇게 정했나 — nice 10의 일은 온전한 지위로(9.11 D6, D20).** SteamCMD의 CPU 중 약 75 %(30 repeat에서 75.33 %, repeat별 73.56–77.57 %)는 nice 10으로 돕니다. 거의 모두 `CContentUpdateC` thread입니다. 나머지 HTTP·IPC thread는 nice 0입니다. 이 dataset은 nice를 싣지 않으므로(1.6절), 시뮬레이션의 다운로드는 온전한 지위로 경쟁합니다. 9.11 D6의 기록: "On a stock desktop EEVDF gives nice-10 work about a tenth of the CPU against a busy nice-0 thread … so the download's interference with the game in `c2-p2a` is overstated, and the headroom there inflated, in the hypothesis's favour." 이 한계의 크기를 재려고 만든 것이 다음 항목입니다.

**tracing 비용.** 이 항목의 값은 socket 읽기·쓰기를 모두 기록하는 `perf trace` 아래에서 쟀습니다. 같은 설치를 그것 없이 돌리면 CPU가 0.975배(0.970–0.981), 시간이 0.991배였습니다. 즉 실린 run은 실제보다 약 2.5 % 많은 CPU 아래서 읽힌 것이고, 그 추가 CPU가 run의 어디에 떨어지는지는 재지 않았습니다(`modeling_notes`).

## 7.4 `game-download-idle` — 같은 다운로드를 idle class로

`game-download-idle`은 yaml의 merge key로 만든 항목입니다.

```yaml
game-download: &game-download
  ...
game-download-idle:
  <<: *game-download
  declared_class: idle
  modeling_notes: >-
    `game-download` with the declared class `idle` in place of the measured download's `normal`; every table and the
    validation record are the base entry's own, shared by reference, so the two entries cannot drift apart. ...
```

`&game-download`은 YAML anchor(이 mapping에 이름을 붙임), `<<: *game-download`는 그 mapping을 그대로 가져와 합치라는 뜻입니다. 그래서 두 항목은 table, lifetime, scaling 규칙, validation 기록을 문자 그대로 공유하고, `declared_class`와 `modeling_notes`만 다릅니다. "the two entries cannot drift apart"가 이 방식을 고른 이유입니다.

이 항목을 묶는 파일은 `c2-p2a-idle` 하나입니다. `c2-p2a`에서 다운로드 task의 항목만 이것으로 바꾼 파일이고, judging set(RQ0 판정에 쓰는 파일 묶음) 밖에 있습니다. 두 파일을 함께 점수 매겨, nice 10 한계가 결과에 얼마나 닿는지 위아래로 묶어 봅니다. `modeling_notes`: "this entry and the base bracket a stock desktop's treatment of that work." 다운로드 전체를 normal로 둔 것(현재 `c2-p2a`)은 실제보다 다운로드에 유리하고, 전체를 idle로 둔 것은 실제보다 불리하므로, 실제 desktop은 그 사이 어딘가라는 생각입니다.

> **왜 이렇게 정했나 — 변형 항목과 변형 파일(9.11 D21, 2026-10-08; 9.13 spec decision 4).** class는 항목의 것이지 task의 것이 아니므로, 어떤 파일도 `game-download`의 다운로드를 idle class로 둘 수 없었습니다. 9.11 D21이 기록한 해결: "A variant of `game-download` — the same tables, the declared class `idle` — and a variant of `c2-p2a` binding it in the download's place, both built by the rebuild and in the manifest the RQ0 gate spec pins. The variant file is outside the judging set; the bounding check alone reads it." 버린 대안은 idle 절반을 빼는 것과, 실행할 때 task의 class를 바꾸는 harness override("against the class being the entry's, and a knob at run time")였습니다. 9.13 decision 4가 merge key 방식과 두 compiled 파일이 그 task의 class에서만 다르다는 test를 정했습니다.

## 7.5 `package-upgrade` — 아무도 시키지 않은 보안 업데이트

**무엇.** Ubuntu 24.04에 기본으로 켜져 있는 unattended upgrade(무인 자동 업그레이드)의 install 단계(`apt-daily-upgrade.service`가 실행하는 `apt.systemd.daily install`)가, 2026-07-27에 Ubuntu가 낸 보안 업데이트를 설치하는 job입니다. glibc 2.39-0ubuntu8.7 → 8.8, binary package 넷(`libc-bin`, `libc6`, `libc6-dbg`, `locales`). 상태는 영어 기본 desktop 설치의 기본 layer(1,445 package)를 Ubuntu snapshot service로 2026-07-27T00:00Z 시점으로 만든 chroot입니다. 9 repeat.

**행동.** 짧게 사는 process 916개가 쉬지 않고 이어지는 사슬입니다. `unattended-upgrade`가 할 일을 계산하고, `dpkg`가 package 넷을 풀고 설정하고, `locale-gen`이 `localedef`를 18번 연달아 돌리고, `mandb`, `apt-check`, `unattended-upgrade`의 마무리가 이어집니다. CPU의 72.8–76.5 %가 `localedef`입니다. task 이름은 `unattended-upgr`(`/usr/bin/unattended-upgrade`의 comm)이지만, 그 이름 아래 CPU 대부분은 `localedef`의 것입니다.

**숫자.** job CPU 26.385 s ±3.78 %(25.25–29.16 s), 포화도 0.990–0.994, run between blocks 평균 1.798 ms, run당 block 8.90 μs. `upgrade_run` table의 중간값은 7 μs이지만 p99.9는 1.04초입니다. 짧은 process 수백 개와 1초 넘는 `localedef` run 몇 개가 한 표에 있기 때문입니다.

> **왜 이렇게 정했나 — 백신 검사 대신 자동 업그레이드(9.10 D3, 2026-10-01).** 예전 core set에서 "아무도 시키지 않은 배경 job"은 `clamscan`(ClamAV 백신 검사)이었습니다. C7 그룹(평소 상황 파일에 원치 않는 배경 일을 끼워 넣은 짝 파일들)의 interactive 짝 열 개와 `c2-p2b`가 그것을 썼습니다. 9.10 D3이 이것을 바꿨습니다. 기록된 이유: ClamAV 문서 자체가 "designed especially for e-mail scanning on mail gateways", "ClamAV is not a traditional anti-virus or endpoint security suite"라고 말하고, 어떤 ClamAV package도 정기 검사를 싣지 않으며, Debian popcon에서 정기 사용 비율이 `clamav` 0.85 %, ClamTk 0.11 %입니다. 반면 `unattended-upgrades`는 Ubuntu 24.04.5.1 desktop의 기본 layer에 있고, 기본으로 켜져 매일 06:00(최대 60분 무작위 지연)에 돌며, `Persistent=true`(놓친 실행을 나중에 함)이고, AC 전원에서만 돕니다.

> **왜 이렇게 정했나 — 어느 날의 업데이트(9.10 D36, 2026-10-01).** 2025-10-01부터 2026-09-30까지 기본 layer의 1,488 binary를 훑은 결과: 222일(61 %)은 아무 업데이트가 없었고, 125일(34 %)은 kernel 아닌 업데이트가 있었으며(중간값 source package 2개, binary 4개), 18일(5 %)은 새 kernel이 있었습니다. 그래서 "median count of binaries a working run installs"인 binary 넷의 날 가운데 가장 최근인 2026-07-27을 골랐습니다. `modeling_notes`는 다른 날이면 다른 job이라고 적습니다. 빈 날은 `unattended-upgrade` 혼자 몇 초, kernel 날은 kernel 설치와 initramfs가 더해집니다. kernel 날의 DKMS 재빌드가 7.8절의 항목입니다.

> **왜 이렇게 정했나 — chroot와 빠진 단계(9.10 D37, D38).** chroot에서는 init이 돌지 않으므로 `libc6`의 postinst가 `systemctl daemon-reexec`와 재부팅 필요 알림을 건너뛰고, unit의 `apt-helper wait-online` 단계는 싣지 않았습니다. scope는 이것을 그대로 적습니다. `locales` 일은 설치가 나열한 locale 수에 비례하며 영어 설치는 18개입니다.

> **왜 이렇게 정했나 — nice 19의 일도 온전한 지위로(9.11 D20, 2026-10-08).** 이 job의 CPU 중 2.67 %(repeat별 2.30–3.36 %)는 nice 19로 돈 `apt-check`와 `dpkg`의 것입니다. 이것도 온전한 지위로 실립니다. 9.11 D20은 이것을 `game-download`와 함께 "nice가 실리지 않는 경우" 둘째로 기록했습니다.

## 7.6 `file-indexer` — Tracker의 첫 색인

**무엇.** GNOME의 파일 색인기 Tracker Miners 3.7.1이 빈 database에서 home 하나를 처음 색인하는 job입니다. 파일 system miner(`tracker-miner-fs-3`)와 그것이 띄우는 모든 process(metadata extractor, 마감으로 끝날 때마다 다시 뜸; GStreamer의 registry scanner)를 miner의 첫 schedule-in부터 extractor가 마지막으로 Idle 상태가 될 때까지 쟀습니다. home에는 HippoCamp의 Bei profile(875개 파일, 40,662,407,070 B, 83개 directory)을 `~/Documents`로 통째로 두고 나머지 폴더는 비웠습니다. 18 repeat.

**행동.** miner는 15초의 기본 초기 sleep 뒤 home을 0.4초 안에 훑고, extractor를 띄웁니다. extractor의 일(PDF와 office 문서의 글, 이미지 metadata, GStreamer의 audio·video 분석)이 job CPU의 96 %입니다. extractor의 파일당 5초 마감(wall clock)이 스캔된 책 PDF 두 개의 추출을 끊고, miner는 1초 유예 뒤 extractor를 다시 띄웁니다. 매 repeat에서 875개 파일이 색인되고 실패 10개가 기록됐습니다.

**숫자.** job CPU 39.435 s ±0.28 %(extractor 37.47–38.35 s, miner 1.53–1.62 s, registry scan 93–106 ms), 포화도 job 전체 0.655–0.676(miner의 Initializing부터는 0.891–0.919), 지배적 thread 0.556–0.559, run between blocks 1.876 ms, run당 block 227.0 μs, run은 최대 4.98–5.48초. class는 **idle**입니다(10장).

> **왜 이렇게 정했나 — 첫 색인이라는 상태(9.10 D5, 2026-10-01).** Tracker 3.7.1은 기본으로 정기 재검사를 하지 않습니다(`DEFAULT_CRAWLING_INTERVAL -1`, "Maybe (depends on a clean last shutdown)"). 전부 다시 색인하는 경우로 보고된 것은 regression 버그들이었습니다. 그래서 그리는 상태를 "Tracker indexing every file from an empty database"로 정했습니다. 원치 않는 쪽(`c7-indexing`, `c2-p1b`)은 login 때의 첫 색인이고, 원하는 쪽(`c1-indexing`)은 사용자가 `tracker3 reset --filesystem`을 한 뒤의 같은 일입니다. "One measured state serves both labels."

> **왜 이렇게 정했나 — 무엇을 색인하나(9.10 D60, D66, D67, D68, 2026-10-02).** 처음 후보였던 Mahoney set은 licence가 "Please do not use this data set for any purpose other than benchmarking data compression and archiving programs"라고 해서 쓸 수 없었습니다(D60). 실제 사람의 home을 측정할 수 있는 조건으로 구할 길이 없었고(Real Data Corpus는 더 이상 없고, 다른 모음은 공개되지 않았거나 내부 용도), HippoCamp의 profile을 골랐습니다. HippoCamp profile은 "a home-like file system its authors aggregated from participants' files, public benchmark documents and synthetic content"이고 licence가 비상업 연구와 benchmarking을 허락합니다(D66). scope는 이것이 한 사람의 파일이 아니라 "anonymized archetypal personal-computing environment"이고, 875개라는 파일 수를 home의 파일 수로 받치는 출처가 없다고 적습니다(design).

> **왜 이렇게 정했나 — 자기 항목(9.10 D70)과 초기 sleep은 도착(D71), 2026-10-02.** dry run에서 이 job은 `cpu-batch`의 공유 기준을 통과하지 못했습니다. 포화도가 job 전체 0.659로 `cpu-batch` 프로그램들(0.925–0.9998)보다 낮았고, extractor process 셋이 차례로 돌았습니다. 그래서 자기 항목이 되었습니다. 15초 초기 sleep은 dry run에서 block 17,944개 중 하나지만 전체 block 시간의 74 %였습니다. 이것을 표에 두면 run당 block 평균이 292 μs에서 1,122 μs로 부풀고, compiler가 block을 독립으로 뽑으므로 15초 sleep이 job 아무 데나 나타납니다. 그래서 그 block 하나를 표에서 빼고, 파일의 도착 시각을 "그 sleep의 끝"으로 읽기로 했습니다. 기록된 근거: 도착 시각은 이미 design입니다(`c1-indexing`의 `arrive: 2s`).

> **왜 이렇게 정했나 — 마감으로 끊긴 추출은 그대로(9.10 D72).** 5초 마감(`tracker-extract.c`의 `DEFAULT_DEADLINE_SECONDS 5`)으로 끝난 두 추출과 재시작을 표와 CPU 합계에 그대로 둡니다. 마감은 wall clock이므로 더 빠르거나 더 바쁜 core에서는 끊기는 파일 수가 달라진다는 것을 scope에 적었습니다.

## 7.7 `video-transcoder` — HandBrakeCLI로 4K 영상을 1080p로

**무엇.** HandBrakeCLI 1.7.2(Ubuntu 24.04의 `handbrake-cli` 1.7.2+ds1-1build2, x264 0.164.3108, FFmpeg 6.1.1)가 기본 preset "Fast 1080p30"(x264 fast, RF 22, main profile, level 4.0, AAC stereo 160 kb/s, MP4)을 바꾸지 않고, Blender Foundation의 Big Buck Bunny 4K 30 fps H.264판 전체(19,036 frame, 634.5초)를 1920×1080으로 변환합니다. clip은 캐시에 올리고 user로 실행했습니다. 5 repeat.

**행동과 숫자.** process 하나에 thread 23개(모두 `HandBrakeCLI`), job 내내 runnable(포화도 0.99938–0.99947), 가장 바쁜 thread가 0.334–0.338, 다음이 0.205–0.208, 셋째가 0.101–0.103. job CPU 2,970.871 s ±2.6 %(약 50분), run between blocks 4.002 ms, run 733k–746k개, 그중 약 10만 개에 2개꼴로만 block이 따릅니다. 매 repeat에서 같은 video track(19,038 frame, 276,311,652 B)이 나왔습니다.

> **왜 이렇게 정했나 — CpsMark+의 transcode(9.10 D11, D91, D92, D95; 2026-10-01/03).** 예전 transcode는 생성한 60초 720p test pattern에 "Fast 720p30" preset이었습니다. 9.10 D11은 이것을 CpsMark+(`cpsmark-tbench23`)의 HandBrake workload로 다시 쟀습니다. 출처 문장: "Convert the H.264 encoded source video with 4K resolution to the H.256 [sic] encoded target video with 2K resolution, the container format is MP4." 다른 어떤 benchmark도 720p 빠른 transcode를 정의하지 않았습니다. 세부 결정: 원본은 Big Buck Bunny 4K 30 fps판(D91), "2K"는 DCI의 2048×1080 container이므로 그림은 1920×1080 그대로(D92), codec은 논문의 오타 "H.256"을 H.265로 읽지 않고 CpsMark+ 자체 code가 쓰는 H.264로, 그래서 HandBrake 기본 preset을 바꾸지 않음(D95가 D93을 고침). scope는 CpsMark+에서 온 것(HandBrake workload, H.264 codec, 1080p "2K")과 오지 않은 것(clip, preset 설정)을 나눠 적습니다.

> **왜 이렇게 정했나 — 자기 항목(9.10 D97, 2026-10-03).** dry run에서 thread 23개의 CPU가 0.335, 0.207, 0.101, 0.088, … 로 퍼져 지배적인 thread가 없었습니다(9.6의 720p encode는 22개 중 하나가 0.61). 9.6 D7의 기준에 따라 `cpu-batch`를 떠나 자기 항목이 되었습니다. 모든 thread가 기본 policy와 nice 0이고 "the encode declares no class"입니다.

## 7.8 `incremental-backup` — Déjà Dup의 주간 incremental backup

**무엇.** Ubuntu의 backup 도구 Déjà Dup 45.2와 그 backend duplicity 2.1.4(Ubuntu 24.04 package)가, 기본 설정(gpg로 암호화, 200 MB volume, 비밀번호 기억)으로, 자기 monitor가 `chrt --idle 0 ionice -c3`로 띄우는 주간 incremental backup을 하는 job입니다. home에는 Mahoney 10 GB set이 있고, Déjà Dup 자신의 도우미로 첫 backup을 한 뒤, Cumulus 연구의 개인 machine 변경률로 7일치 변경(바뀐 파일 9,729개 883.1 MB, 새 파일 304.2 MB; 바뀐 쪽은 상한)을 가한 상태입니다. backup 대상은 외장 drive를 대신하는 loop device 위의 ext4입니다. job은 monitor가 띄운 `deja-dup` tree 전체입니다. duplicity의 collection-status, 모든 backup이 하는 dry-run 크기 계산, volume마다 gpg가 붙는 incremental, 그리고 검증용 restore. 30 repeat 중 28개를 pool에 넣었습니다(repeat 12와 25는 set을 받지 못함).

**행동과 숫자.** process 52개, thread 115–118개. CPU의 0.569–0.576이 duplicity(8번 실행), 0.283–0.291이 deja-dup, 0.134–0.140이 gpg입니다. 가장 바쁜 thread 셋이 0.320–0.333, 0.283–0.291, 0.223–0.239로 지배적인 thread가 없습니다. job CPU 165.668 s ±0.56 %, 시간 162.5–174.9초(dry run 59.9–64.1 s, incremental 96.9–106.4 s, 검증 4.1–4.3 s), run between blocks 1.966 ms ±4.4 %, 포화도 0.9935–0.9952. class는 **idle**입니다.

> **왜 이렇게 정했나 — borg 대신 Déjà Dup(9.10 D8, 2026-10-01).** 예전 backup은 9.7이 잰 `borg`의 첫 backup(새 repository에 처음 넣기)이었습니다(`file-backup` 항목). 9.10 D8의 기록: borg의 반복 backup은 바뀌지 않은 파일의 내용을 읽지도 않으므로 "정기 backup"으로는 다른 일이고, `borg`는 Ubuntu의 어떤 설치 layer에도 없습니다. 반면 Déjà Dup 45.2는 Ubuntu 24.04의 확장 설치에 있고, 정기 backup은 기본으로 꺼져 있지만 켜면 7일마다 돕니다. Debian popcon에서 `deja-dup` 설치 4.07 %, 정기 사용 2.81 %로 `borgbackup`(2.78 %, 1.26 %)보다 많습니다. 2026-10-04 fold-in(D125)으로 `file-backup`은 library를 떠났습니다(9.7의 campaign은 release `meas-ci-background-2026-09-19`에 남음).

> **왜 이렇게 정했나 — 변경 집합(9.10 D115).** 7일치 변경은 Cumulus(`vrable-fast09`)의 개인 machine 변경률을 9.7의 방법으로 적용한 것입니다. 바뀐 쪽은 상한으로 적었습니다.

> **왜 이렇게 정했나 — 두 갈래의 run(9.10 D122, 2026-10-04).** 첫 batch에서 run between blocks 평균이 repeat 2, 4는 1.40 ms, repeat 1, 3, 5는 2.02–2.09 ms로 갈렸습니다(±26.3 %, 72 repeat 필요). 원인은 dry run 단계에서 deja-dup이 duplicity의 log를 pipe로 읽는 방식이었습니다. 거의 매 쓰기마다 읽는 경우와 몰아서 읽는 경우가 있었고, 둘 다 `SCHED_IDLE`로 한 CPU 위에서 도는 pipe 작성자와 읽는 쪽의 끼어들기가 그 갈림을 만들었습니다("the interleaving of a pipe's writer and reader on one CPU"). 결정: 30 repeat까지 돌리고 그래도 실패하면 예외로 싣는다. 30에서 ±4.4 %로 통과했습니다. 28개 repeat 중 2개는 거의 매번 읽기, 26개는 몰아 읽기였습니다.

> **왜 이렇게 정했나 — restore 시험은 그리지 않음(9.10 D118).** Déjà Dup은 두 달에 한 번(주간 실행 약 9번에 1번) 새 cache로 비밀번호를 물으며 restore 시험을 하는데, 이것은 그리지 않았습니다.

## 7.9 `module-build-orchestrator`와 `module-compiler-child` — NVIDIA kernel module의 DKMS 재빌드

**무엇.** **DKMS**(Dynamic Kernel Module Support: 새 kernel이 설치되면 kernel 밖의 module을 그 kernel에 맞게 자동으로 다시 build하는 Linux 장치)가 NVIDIA의 open kernel module `nvidia-dkms-595-open` 595.91.07을 보안 kernel `7.0.0-34-generic`에 맞게 다시 build하는 job입니다. 이 build는 2026-09-23의 unattended upgrade install 단계가 kernel을 설치하며 hook으로 띄웁니다. 상태는 7.5절과 같은 chroot에 설치기가 넣는 HWE kernel(`7.0.0-31`)과 `apt install nvidia-driver-595-open`을 더한 것입니다. job은 그 단계의 두 DKMS kernel hook 아래의 모든 process입니다. `-j8`로 돌고(NVIDIA의 `dkms.conf`와 dkms가 `nproc`을 읽는데 `OMP_NUM_THREADS=8`로 맞춤; 9.6 D4의 8-thread desktop에 적용한 `nproc` 규칙, convention), 26 landing입니다.

**행동.** parallel make가 cap 8에서 약 여덟 job을 동시에 돌린 뒤, 직렬 꼬리(module 다섯을 strip하고 zstd로 압축, 그다음 depmod)를 돕니다. job은 네 종류이고(2.6절의 tree), 실제 build가 돌린 순서(`job_order`)대로 돕니다. object job 200개(6개는 `objtool`이 붙은 일곱 member였으나 `sh`에 접어 넣음), kbuild의 compiler probe 1,125개, NVIDIA의 `conftest` 시험 145개(`as` 없음)와 87개(`as` 있음).

**숫자.**

| 값 | 측정 |
|---|---|
| job CPU(job들, make, 꼬리) | 224.627 s ±1.46 %(210.6–238.9 s) |
| 그중 실린 몫 | hook 실행 CPU의 0.9818–0.9825; 모델링 안 된 3.89–4.32 s |
| `dispatch_overhead` 평균 | 754.3 μs ±0.72 % |
| 꼬리 | 9.29–11.14 s; `tail_work` constant 10,027,983 μs; 꼬리 run 평균 6.151 ms |
| 꼬리의 run당 block | 44.4 μs ±8.35 %(machine 따라 흩어짐 예외) |
| job당 `cc1` 평균 | object 721.9 ms, conftest 171.7 ms(as 없음)·240.0 ms(as 있음), kbuild probe 4.55 ms |
| 동시 object job(cap 8) | 평균 7.86, 여덟인 시간 92.2 % |

task 이름은 `dkms`이고, 자식들은 관측된 comm을 그대로 씁니다(compiler driver는 `x86_64-linux-gn`). `cc1`은 orchestrator의 `child_name`을 받습니다. `c7-compile`의 `dkms` task는 spawn table 9,980개, `fork_cap` 48로 compile됩니다.

> **왜 이렇게 정했나 — 원치 않는 module 재빌드는 실제 DKMS(9.10 D4, 2026-10-01).** 예전 `c7-compile`의 원치 않는 job은 `c1-compile`의 build를 이름만 `make` → `dkms`로 바꾼 것이었습니다(kernel build의 값, 사용자의 100 job). 9.10 D4는 이것을 runner에서 관측한 실제 module의 DKMS autoinstall로 바꿨습니다. 기록된 근거: DKMS hook은 kernel이나 header가 설치되면 `dkms autoinstall`을 돌리고, Debian popcon에서 DKMS는 설치 14.70 %, 정기 사용 7.07 %이며, module별로 `nvidia-kernel-dkms` 3.76 %가 가장 많습니다.

> **왜 이렇게 정했나 — NVIDIA 595 open(9.10 D46, D47, 2026-10-02).** ZFS와 v4l2loopback은 Ubuntu가 미리 build한 module로 내주므로 DKMS를 돌지 않습니다. NVIDIA driver를 `apt install nvidia-driver-<branch>`로 직접 깔면 DKMS package가 따라옵니다(`ubuntu-drivers`는 `--include-dkms` 없이는 미리 build한 것을 깔기 때문에, `modeling_notes`는 "the user installed `nvidia-driver-595-open` by apt"를 전제로 밝힙니다). branch는 NVIDIA의 595 branch(Ubuntu의 control file이 `XB-Support: PB`로 적음), 그중 open flavour입니다. `ubuntu-drivers`가 `-open`을 먼저 고르고, NVIDIA가 "We recommend the use of open kernel modules on all GPUs that support it"라고 하며, Steam 2026년 8월 Linux 조사에서 NVIDIA 사용자의 87.0 %가 open module을 지원하는 GPU였습니다.

> **왜 이렇게 정했나 — spawn 형식의 새 항목(9.10 D52, D53, D54, D57, 2026-10-02).** batch loop로 적으면 build가 늘 runnable한 task 하나가 되고, `build-orchestrator`에 200 job을 묶으면 kernel build의 값을 싣게 됩니다. 그래서 같은 spawn 형식의 새 orchestrator–자식 짝을 만들었습니다(D52). probe는 두 종류로 나눴습니다(D53). 1,357개 probe 중 1,124개가 kbuild의 것(job당 약 10 ms)이고 233개가 NVIDIA `conftest`(46.4 s)여서, 한 표로 모으면 `cc1` draw의 83 %가 약 4 ms 근처, 17 %가 약 250 ms 근처인 이상한 표가 되기 때문입니다. 마지막 job 뒤의 직렬 꼬리(9.73 s CPU, 4.4 %)는 orchestrator 자신의 batch loop로 적었고, helper job 841개, link job 13개, dkms script의 make 전 일, kernel image의 두 번째 hook은 합쳐 약 4 s(1.8 %)로 모델링하지 않았습니다(D54). `fork_cap`은 9.6 D19의 규칙대로 cap × 6 = 48인데, `conftest` 시험은 member가 8–10개라서 그것이 도는 동안(build의 약 27 %)은 여덟 job보다 적게 돕니다. build 전체로 살아 있는 member 평균은 48 대비 49.0이었습니다(D57). job 단위 cap은 simulator 형식을 바꿔야 해서 택하지 않았습니다.

> **왜 이렇게 정했나 — nice 19의 `apt-check`와 `dpkg`는 이 항목에 없다(9.13 reads R3, 2026-10-09).** 9.11 D20(2026-10-08)은 DKMS landing 10의 CPU 중 2.024 s(0.85 %)가 nice 19의 `apt-check`와 `dpkg`라는 것을 보고, 이 일이 항목의 table에 들어 있는지 9.13에 물었습니다. 9.13은 원 자료를 다시 받지 않고 pooling code와 pooled 결과로 이것을 닫았습니다(`_dev/research/jioh/task-9.13-rebuild/reads.md`의 R3). job의 정의는 "every process rooted at a `dkms_autoinstaller` run the kernel install causes"이고, 분석 code(`dataset/tools/meas/background/analyze.py`의 `hook_subtrees`)는 hook을 실행한 pid에서 fork 기록을 따라 **아래로만** 내려가며 자손을 모읍니다. `dpkg`와 `unattended-upgrade`는 hook의 조상이고 `apt-check`는 hook 밖에서 돌므로 어느 것도 들어오지 않습니다. 26 landing의 꼬리 CPU를 process 이름별로 보면 `cp`, `depmod`, `dkms`, `strip`, `zstd` 등만 나옵니다. 0.85 %는 단계 전체(업그레이드 tree 포함)를 더한 값이었습니다. 남은 단서 하나: `hook_subtrees`는 thread id로 짝을 짓는데, 약 17,000 task가 도는 단계 안에서 id 재사용을 막지 않습니다. 원 자료로 확인하는 방법도 R3에 적혀 있습니다(release `meas-ci-background-2026-10-02`의 landing 10 asset에서 nice-19 행의 pid를 hook subtree와 대조; subtree 안의 nice-19 CPU는 0이어야 함). 이 확인은 하지 않았습니다(미실행).

> **왜 이렇게 정했나 — Secure Boot 서명은 그리지 않음(항목의 scope).** chroot에 boot loader와 `shim-signed`가 없어서 module에 서명하지 않았습니다. Secure Boot desktop이라면 module 다섯에 서명하는 일이 더해집니다(scope).

# 8장 · browser 조각과 comms: 숨은 tab과 chat client

이 장은 9.8 slice(browser와 comms)가 남긴 두 항목, `renderer-hidden`과 `chat-client`를 다룹니다(`game-client`도 9.8의 것이지만 4.2절에서 다뤘습니다). 질문은 "사용자가 보고 있지 않은 browser tab과 그냥 켜져 있는 chat 프로그램은 scheduler에게 무엇인가"입니다. 둘 다 거의 일하지 않지만, 개수가 많고(tab) 늘 켜져 있어서(chat) desktop의 배경을 이룹니다. 이 장 끝에서는 9.8과 9.10이 library에서 내보낸 항목들(`electron-comms`, `renderer-visible`)도 정리합니다.

## 8.1 `renderer-hidden` — 배경 tab 하나의 renderer

| | |
|---|---|
| 흉내 내는 것 | Google Chrome의 renderer process 하나(배경 tab 하나의 page) |
| 측정 | Chrome 154.0.8037.57, 창 하나에 전경 대조 tab 하나와 배경 tab 12개(서로 다른 loopback origin 12개의 같은 local page), intensive throttling 유예를 지난 뒤 600초 steady phase; 5 repeat |
| 재현하는 행동 | 거의 잠들어 있음. 10초마다 hang 감시, 가끔 page timer, 1분마다 IPC, 2분마다 compositor |
| 핵심 숫자 | renderer당 0.211 wakes/s: `HangWatcher` 0.100(gap 10.0 s), page thread `chrome` 0.067, `Chrome_ChildIOT` 0.0176(gap 약 60 s), `Compositor` 0.0083(약 120 s), `PerfettoTrace` 0.0083, residual 0.0096; 12개 renderer를 합친 CPU 점유율 약 1 × 10⁻⁴(9.6 × 10⁻⁵; renderer 하나로는 약 8 × 10⁻⁶) |
| tag | `meas-ci:desktop:2026-10-05b` |

**무엇을 쟀나.** Chrome은 site마다 renderer process를 따로 둡니다(site-per-process). 배경으로 간 tab의 page는 timer가 1초에 한 번으로 정렬되고, 5분(기본값; 로딩이 끝난 page는 60초) 유예가 지나면 **intensive wake-up throttling**으로 1분에 한 번까지 줄어듭니다(9.8 D3이 Chromium 소스 commit `999361f1…`에서 읽은 상수: `kDefaultThrottledWakeUpInterval`, `kIntensiveThrottledWakeUpInterval` 등). 이 항목은 그 유예를 지난 뒤의 **terminal steady state**(더 이상 바뀌지 않는 안정 상태)를 잽니다. page는 `setInterval` callback이 counter만 올리는 것이고, 대조 tab 하나를 전경에 두었습니다. 값은 job이 재는 page renderer 12개를 표본으로 모은 "renderer 하나"의 것입니다. 관측된 renderer process 16개 중 대조 tab, Chrome 자신의 extension·WebUI renderer, phase 일부에만 있던 renderer는 뺐습니다.

**값은 바닥입니다.** scope: "Values are floors: a page that does nothing but stay alive, on a runner without a GPU or display vsync … a renderer showing live content does more. Not covered: a tab just switched away from, before the grace." 살아 있기만 하는 page이므로, 움직이는 내용을 보여 주는 실제 tab은 이보다 더 깨어납니다. 그리고 막 배경으로 간 tab(유예 전)은 다루지 않습니다.

**예외.** `HangWatcher`의 run 평균(±18.1 %)과 page thread `chrome`의 run 평균(±11.4 %)은 "machine 따라 흩어짐"(둘의 run이 phase CPU의 84.3 %); `Chrome_ChildIOT`, `Compositor`, `PerfettoTrace`는 "session 사이에서 변함"(phase당 renderer마다 5.0–10.6번 깸); residual(`ThreadPoolServi`, `MemoryInfra`)은 "sparse component"(phase당 renderer마다 5.0–7.2번)로 실립니다.

**개수.** core set에서 Chrome이 나오는 파일은 모두 `renderer-hidden` task를 4개(`count: 4`) 가집니다. tag는 `[glam, "meas-ci:desktop:2026-10-04"]`입니다.

> **왜 이렇게 정했나 — renderer는 자기 task(9.8 D2, 2026-09-20).** renderer를 `web-browser`의 task 하나에 합칠 수도 있었습니다. 9.8 D2는 합치지 않았습니다. 기록된 이유: "the number of independently schedulable entities is a first-order property of a scheduling workload, and merging 102 renderer tasks into the browser tasks beside them changes what contends for the CPU." 당시 core set에 renderer task가 102개 있었습니다.

> **왜 이렇게 정했나 — 배경 tab만, 창 하나(9.8 D4; 9.10 D16, 2026-10-01).** 9.8 D4는 처음에 renderer 항목을 둘로 나눴습니다. 배경 tab의 renderer(`renderer-hidden`)와, 보이는 채로 방치되거나 다른 창에 가려졌을 뿐인 renderer(`renderer-visible`). 9.8 D4는 Linux의 Chromium이 다른 application 창에 가려진 것을 추적하지 않는다고(가려짐을 계산하는 code가 Windows에서만 컴파일됨) 보아, 가려진 창의 tab이 계속 "보이는" 상태라고 적었습니다. Chromium은 X11에서 X server가 창이 완전히 가려졌다고 알릴 때 그 창을 occluded로 표시하고, 그려진 desktop이 그 알림을 보내는지는 측정이 시험하지 않았습니다. 두 상태는 wake 비율이 약 60배 달라 하나로 근사할 수 없었습니다. 그런데 9.10 D16이 Chrome 파일은 창 하나를 그린다고 정하면서 `renderer-visible`이 library를 떠났습니다. 근거: Firefox의 Linux telemetry(release 152, client 7,535,303개)에서 client별 최대 창 수의 중간값이 1이고, Test Pilot 2010에서 창이 둘 이상인 시간의 비율 중간값이 0.03이었습니다. 지금 쓰는 page의 renderer는 `web-browser`가 싣습니다(9.5 D84).

> **왜 이렇게 정했나 — 넷(9.10 D15, D127, D131).** tab 수는 Firefox Linux telemetry(`glam`: Mozilla GLAM 공개 API의 `browser_engagement_max_concurrent_tab_count`)의 client별 최대 동시 tab 수 중간값 4.67을 반올림한 5입니다(D15). 그중 하나는 지금 쓰는 page이므로 `web-browser`의 것이고, 나머지 넷이 배경입니다. renderer 수는 이 tab 구성을 runner의 Chrome에서 실제로 띄워 셌습니다(D131: 5 repeat 모두 spare 끈 launch에서 page renderer 다섯, spare 켠 launch에서 여섯). spare renderer와 Chrome 자신의 renderer는 `web-browser`의 몫이므로 세지 않습니다(D127). 그래서 `count: 4`입니다. 예전 값들(11, 7, 7, 9, 5)은 출처가 없었습니다. `sources.yaml`의 `glam` notes는 "Firefox's distribution read for Chrome's tab count is our modeling"이라고 적습니다. Firefox의 tab 분포를 Chrome에 읽어 쓴 것은 우리의 모델링이라는 뜻입니다.

> **왜 이렇게 정했나 — 1,030초 유예 settle과 Chrome 154(9.10 D152, D156, 2026-10-05).** 3,600초 probe에서 page thread는 steady phase의 첫 4분 동안 wake당 0.106, 0.083, 0.077, 0.080 ms를 쓰다가 일곱째 분부터 0.055–0.060 ms로 내려앉았습니다. 그래서 유예 settle을 630초에서 1,030초(630 + 360 + 여유 40)로 늘리고 다시 쟀습니다. 다시 잰 campaign은 Chrome 154에서 돌았는데, Google의 repository가 현재 판만 내려주기 때문입니다. 9.8의 19 repeat(152/153)와 비교하면 page thread가 1.72배, `Chrome_ChildIOT`가 2.51배 자주 깨고, renderer 전체 0.211 대 0.169 wakes/s였습니다. 결정은 이 항목을 154의 5 repeat로 접어 넣고, `web-browser`는 152/153 그대로 두는 것이었습니다. scope: "`web-browser` stays 152 and 153's, the two halves of one browser on two builds." 한 browser의 두 반쪽이 서로 다른 판에서 왔다는 한계를 밝힌 것입니다.

> **왜 이렇게 정했나 — 600초 창의 흔들림은 진술됨(항목의 scope).** 같은 3,600초 probe에서 600초 창은 wake를 모든 위치에서 수준의 3.7 % 안에 두었지만, CPU는 −7.8 %에서 +10.4 %까지 흔들렸습니다(처음 적은 −7.2 %는 600초 지점 첫 위치의 값이고, 모든 위치의 최저는 −7.8 %입니다. 2026-10-17, 9.16 측정 감사가 고침). 약 1,800초 간격으로 되풀이되는 episode(page thread 0.072–0.075 ms, `Chrome_ChildIOT` 0.243–0.247/s) 때문이고, 1,800초까지 어느 길이도 최악 위치에서 5 %를 지키지 못했습니다(−5.9 %). 이것은 scope에 "stated"로 남았습니다.

## 8.2 `chat-client` — 아무 메시지도 오지 않는 Element Desktop

| | |
|---|---|
| 흉내 내는 것 | Electron 기반 chat client(timeline 이름 `element-desktop`) |
| 측정 | Element Desktop 1.12.28, runner에 설치한 Synapse 1.161.0 homeserver의 방 하나에 로그인, 메시지 없음; launch settle 20초, idle phase 600초; 18 repeat |
| 재현하는 행동 | 초당 약 12번 깸; Matrix의 `/sync` long poll(server가 새 소식이 있을 때까지 응답을 30초까지 미루는 요청 방식)에 맞춰 대기 |
| 핵심 숫자 | 합 12.32 wakes/s(`stats`: 11.98–12.56); component 6개: `ThreadPoolForeg` 4.23/s, `element-desktop` 3.90/s(thread 37개), `Chrome_IOThread` 1.85/s, `Chrome_ChildIOT` 1.48/s, `ThreadPoolServi` 0.38/s, residual 0.47/s; CPU 점유율 0.00088–0.00114 |
| tag | `meas-ci:desktop:2026-09-20`, `meas-ci:desktop:2026-10-04b`(launch) |

> **왜 이렇게 정했나 — Element로 재고, Discord 자리에 쓴다(9.8 D7, 2026-09-20).** core set에는 원래 `discord` task들이 있었습니다. Discord는 관측할 수 없었습니다(bootstrapper, 고정되지 않는 client, login 벽, 자기 server를 둘 수 없음). 그래서 이미 `electron-comms`의 notes가 대역으로 선언했던 Element를, Matrix homeserver를 harness CPU에 두고 쟀습니다. Discord의 게임 overlay 역할은 철회했습니다. Discord 자신의 문서가 "The overlay is compatible with Windows OS only; it does not function on Mac OS or Linux"라고 말하기 때문입니다. 9.10 D23과 D24(2026-10-01)는 chat client를 idle로 보이고, task는 관측한 프로그램의 이름을 보인다고 정했습니다. 그래서 timeline의 이름은 `element-desktop`입니다.

> **왜 이렇게 정했나 — idle만 싣는다(9.8 D11, 2026-09-20).** 모든 repeat가 scripted traffic phase(정해진 비율로 메시지가 오는 phase, design)도 돌렸고, 그때는 초당 49.150번(idle의 약 4배) 깼습니다. 그러나 이 값은 싣지 않습니다. 기록된 이유: "no class found any statement of how often a real user's chat client receives messages"이고, traffic 아래의 값은 "would rest on a rate we chose". 이것은 9.7 D5가 `background-crawler`를 은퇴시킨 것과 같은 근거입니다(우리가 고른 비율에 값이 매이면 안 됨).

`modeling_notes`에 untraced control의 한 줄이 더 있습니다. 대조 측정은 Element 1.12.29에서 돌았고 실린 pool은 1.12.28이었습니다. 두 번째 idle 실행은 traced 여부와 상관없이 `Chrome_IOThread`와 `Chrome_ChildIOT`를 약 3–4 % 더 깨웠습니다.

## 8.3 떠난 항목들: `electron-comms`와 `renderer-visible`

**`electron-comms`.** 예전 library의 "거의 쉬면서 짧게 주기적으로 깨고 renderer 자식을 가진" 항목이었습니다. core set에서 125개 task가 이것에 묶여 있었습니다(`chrome` renderer 102, `steamwebhelper` 9, `steam` 6, `thunderbird` 3, `discord` 3, `zoom` 2). 9.8 D1(2026-09-20)이 이것을 프로그램마다 나눴습니다. 기록된 이유: "the entry's two values describe no process that was observed." heartbeat 중간값 1.85초는 Element main process(gap 0.40–0.43초)와 그 GPU·network helper(3.84–3.92초)의 기하 중심이었고, 1.85초 근처에서 깨는 process는 없었습니다. heartbeat당 일 289 μs도 helper(128–197 μs)와 main(531–857 μs) 사이에 있었고, 측정에 Element renderer는 하나도 없었습니다. 이 값들은 2026-08의 `meas-ci:gui:2`(vCPU 넷, CPU 고정 없음)에서 왔습니다. 9.8 D25(2026-09-22)의 fold-in으로 네 항목이 그 자리를 채웠습니다(`renderer-hidden`, `renderer-visible`, `chat-client`, `game-client`). binding은 이렇게 정리됐습니다. `thunderbird` → `mail-client`(9.8 D9), `discord` → `chat-client`, `steam` → `game-client`, `zoom` helper는 은퇴(9.8 D8), `steamwebhelper` 아홉은 은퇴(`game-client` tree가 이미 담음).

**`renderer-visible`.** 9.8의 visible renderer 항목입니다. 9.10 D16(2026-10-01)이 Chrome 파일을 창 하나로 그리기로 하며 library를 떠났습니다(8.1절). 그 campaign은 release `meas-ci-desktop-2026-09-20`에 남아 있습니다. `docs/workload/measurement-overview.md`의 항목 표도 2026-10-17부터 이 항목을 세지 않습니다(9.15).

# 9장 · daemon과 session process

이 장은 9.9 slice(daemon과 session process)가 만든 네 항목을 다룹니다. `compositor-shell`(GNOME Shell과 Mutter), `audio-server`(PipeWire stack), `service-manager`(systemd), `message-bus`(dbus-daemon). 질문은 "아무도 컴퓨터 앞에 없을 때, desktop을 떠받치는 process들은 scheduler에게 무엇인가"입니다. 답은 "거의 아무것도 아니다"에 가깝습니다. 넷을 합쳐도 초당 0.7번 정도 깹니다. 그러나 그 "거의 아무것도"를 정확히 재는 것이 생각보다 어려웠고, 그 과정의 결정들이 이 장의 내용입니다.

## 9.1 네 항목의 공통 모양

**옛 항목을 둘로 가르기(9.9 D1, 2026-09-22).** 예전 library에는 `system-daemon` 하나가 있었고, 그 값은 runner에 기본으로 깔린 server daemon 51개(systemd 계열, `dbus-daemon`, `cron`, `rsyslogd`, `polkitd`, …)의 process별 평균에서 왔습니다. 그리고 `c1-idle`이 `gnome-shell`, `Xorg`, `pipewire`를 여기에 묶었습니다. 2026-09-13 critical findings memo(B6)가 지적한 대로 이 세 session process는 측정된 적이 없었습니다. 9.9 D1은 system service와 session process를 갈랐습니다. 기록된 이유: "the two populations differ in every class searched." service는 timer와 사건에 깨고(cron 60초, multipathd 5초, udisksd 600초), Mutter의 frame clock은 출력이 꺼지면 멈추며, PipeWire는 WirePlumber가 쉬는 node를 5초 뒤 suspend하면 멈춥니다. 9.9 D2와 D5는 session 쪽과 service 쪽 모두 "프로그램마다 항목 하나"로 정했습니다.

**한 campaign, 실제 Ubuntu desktop session(9.9 D8, 2026-09-22).** 네 항목은 `meas-ci:session:2026-09-24` 하나에서 왔습니다. runner에 `ubuntu-desktop-minimal`을 깔고, 전용 사용자를 GDM의 자동 login으로 로그인시킨 session입니다(먼저 300초 priming login과 logout을 한 번 함, 9.9 D16). 네 항목의 process만 측정 CPU 하나에 두고, session·system·harness의 다른 모든 process는 다른 CPU로 보냈습니다. 그 배치는 고정 뒤와 steady 경계에서 process를 직접 읽어 확인했습니다. `perf sched record`는 모든 CPU에서 돌았습니다. 24 repeat를 네 항목이 공유합니다.

**terminal idle state(9.9 D9, 2026-09-22).** 측정한 상태는 "nobody present past idle-delay"입니다. 아무도 없어서 GNOME의 idle-delay(300초)가 지나, shield가 올라가 잠기고, power daemon이 monitor를 끈 상태입니다. 각각을 측정 login 420초 뒤의 steady 경계에서 확인했고, 그 뒤 1,800초 steady phase를 쟀습니다(9.9 D22). 기록된 근거는 9.8 D3과 같은 규칙(더 이상 바뀌지 않는 terminal 상태를 잼)과 core set 쪽의 묘사("Nobody present, maintenance only")입니다. 대가로 scope는 "Not covered"를 적습니다. 사용 중인 session(application이 열려 있고 화면이 켜져 있고 알림이 옴), session 시작, 그리고 compositor의 경우 그리기 자체.

**wake의 원인을 추적(9.9 D27, 2026-09-24).** session 측정에서 깬 원인을 trace에서 거슬러 올라가 보니, 많은 wake가 desktop 바깥에서 왔습니다. pid 1의 wakeup 행 7,943개 중 54.4 %가 `php-fpm8.3`(runner image에 깔린 것, repeat마다 10.001초 간격으로 180번)였고, system bus의 행 대부분이 그 `php-fpm`이 시작한 pid 1 run 안에 있었습니다. WirePlumber의 행 중 약 절반은 측정 workflow 자신의 `while kill -0 …; do sleep 10; done` loop가 깨운 것이었습니다. 9.9 D27이 세운 규칙: 깨운 쪽의 package가 Ubuntu 24.04 desktop manifest(`ubuntu-24.04.5.1-desktop-amd64.manifest`)에 없거나 harness면 "바깥"이고, 그 wake는 component에서 빠져 scope에 적힙니다. 간접 wake는 원인을 따라가고, 정해진 시각에 도는 desktop job(anacron, sysstat 요약, motd-news, fstrim, man-db 등)은 component의 wake가 아니라 phase의 "사건"으로 적고 싣지 않습니다. 단 1,800초 안에 되풀이되는 desktop job(sysstat의 수집기)은 남깁니다(9.9 D47이 한때의 반대 결정 D32를 되돌림).

**cron session(9.9 D23).** 24 repeat 중 넷(47, 48, 49, 51)은 phase가 UTC 자정을 지나며 runner image의 `sphinxsearch` indexer cron job과 만났습니다. 이 package는 desktop 설치에 없습니다. 그 cron session이 깨운 행(각 cron wakeup ±2초 창 안)은 component에서 빠지고 "stated, not carried"입니다.

**공통 한계.** GNOME Shell은 unit drop-in으로 `--headless --virtual-monitor 1920x1080@60`으로 시작했고 seat에 display 장치도 vblank도 없습니다. 소리 장치가 없어 WirePlumber는 null sink를 씁니다. 측정 CPU에는 CPU별 kernel thread가 함께 돌았고(repeat마다 11,608–15,472번 schedule-in, 보고만 함), 측정 CPU 위의 바깥 사용자 공간 일은 phase의 0.00097–0.0022 %로 2 × 10⁻⁴ 상한 아래였습니다(9.9 D20, D22).

**어디에 쓰이나.** 9.10 D28(2026-10-01)은 core set에서 session process가 idle 파일(`c1-idle`, `c7-idle`)에만 나오고 그 밖의 core 파일은 모두 그것을 생략했다고 밝힌다고 정했습니다. generated layer는 idle을 놓는 곳마다 이 넷을 싣습니다. 182개 파일이 이들을 묶고, 그중 62개에서는 세션이 다른 mode의 프로그램 옆에서 돕니다. 이 62개는 design 조합입니다(인지오의 결정, 2026-10-16; building plan §3a; generated layer를 다루는 5권 2.6절). `Xorg` task는 은퇴했습니다(9.9 D26). Mutter 46.2의 X11 정책이 "on demand"(필요할 때만 띄움)여서 어떤 측정에서도 `Xorg`나 `Xwayland`가 보이지 않았고, `xorg`를 `compositor-shell`에 묶으면 두 번 세게 되기 때문입니다.

## 9.2 네 항목의 숫자

| 항목 | 흉내 내는 것 | timeline 이름 | component | 합 wakes/s | CPU 점유율 | tag |
|---|---|---|---|---|---|---|
| `compositor-shell` | GNOME Shell 46.0 + Mutter 46.2(한 process) | `gnome-shell` | `gnome-shell/JS Helper` 0.3025(thread 4), `gnome-shell/gmain` 0.24984(gap 4.0 s), `gnome-shell/gnome-shell` 0.034745(run 평균 5.7 ms) | 0.587 | 0.000196–0.000249 | `meas-ci:session:2026-09-24` |
| `audio-server` | PipeWire 1.0.5 + WirePlumber 0.4.17 + pipewire-pulse(한 task) | `pipewire` | `wireplumber/gmain` 0.0093(gap 평균 107 s) | 0.0093 | 사실상 0 | 같음 |
| `service-manager` | systemd 255.4: pid 1과 사용자 manager(한 task) | `systemd` | `pid1/systemd` 0.0702(gap 평균 14.2 s, run 평균 0.171 ms) | 0.070 | 0.000009–0.000018 | 같음 |
| `message-bus` | dbus-daemon 1.14.10: system bus와 session bus(한 task) | `dbus-daemon` | `system-bus/dbus-daemon` 0.0140(gap 평균 71.6 s, run 평균 0.121 ms) | 0.014 | 0.000001–0.000003 | 같음 |

component 이름은 `<instance>/<comm>` 꼴입니다(task 하나가 한 프로그램의 process 여럿을 담을 때 instance로 구분). residual이 없습니다. 모든 다른 wake가 sporadic이어서, 항목마다 component 한두 개가 wake의 99.97–100 %를 덮습니다.

**`compositor-shell`.** Mutter와 shell이 한 process에 있습니다(9.9 D3: GNOME Shell 자체를 관측, KWin이나 sway로 대신하지 않음 — "9.8 D1 rejected substitution where the named program is observable"). 화면이 꺼져 있으므로 그리기는 없습니다. scope: "Mutter's frame clock is inhibited while the output is off … no source states a compositor's per-frame CPU cost on a GPU desktop." 100초 창으로 읽으면 steady 경계 직후 첫 100초가 가장 바쁩니다(`JS Helper`가 phase 비율의 1.46배, main thread run 평균 8.03 ms 대 이후 5.10–6.75 ms). class census에서 mutter의 `KMS thread`는 real-time(RR, priority 20)이었지만 이 idle session에서는 실린 component가 아닙니다.

**`audio-server`.** 세 user service를 한 task로 묶었습니다(9.9 D4: 역할이 process 셋에 나뉘어 있음). 그런데 phase 동안 `pipewire`와 `pipewire-pulse`는 한 번도 깨지 않았고, WirePlumber의 `gmain`만 24 repeat 평균 0.0093/s로 깼습니다. 자정을 지난 네 repeat에서는 0.0110/s(나머지 0.0090/s)였는데, 늘어난 wake는 100 ms 간격의 짝이었고 trace가 깨운 쪽을 보여 주지 않아(빈 CPU의 timer나 interrupt) 9.9 D27의 규칙대로 남겼습니다(9.9 D38). census에서 PipeWire의 data loop thread는 RR priority 20, main thread는 nice −11이었지만, 실린 component(`wireplumber/gmain`)는 보통 class nice 0입니다.

**`service-manager`.** pid 1과 `systemd --user`를 한 task로 묶었습니다(9.9 D7: 사용자 manager는 사용자가 로그인했을 때만 있고, `c1-idle`이 그리는 것이 바로 그 상태). 사용자 manager는 cron session을 만난 repeat에서만 깼고 그 wake는 모두 빠져, 실리는 것은 pid 1뿐입니다. phase당 114–139번 깹니다.

**`message-bus`.** system bus와 session bus를 한 task로 묶었습니다(9.9 D6). session bus는 cron repeat에서만 깨(111번) 모두 빠졌고, 실리는 것은 system bus뿐입니다. phase당 16–38번 깹니다.

> **왜 이렇게 정했나 — session 사이에서 변하는 값(9.9 D29, D48).** `pid1/systemd`의 세 값과 `system-bus/dbus-daemon`의 세 값은 "session 사이에서 변함" 예외로 반폭과 함께 실립니다. pid 1: wake 비율 ±1.9 %, gap 평균 ±1.9 %, run 평균 ±7.8 %. system bus: 셋 다 ±11 % 안팎. long-phase probe 36, 41, 44에서 60초마다 창을 밀어 보니 한 run 안에서도 상당히 움직였습니다(pid 1 ±5.0–18.4 %, system bus ±13.6–47.0 %). scope는 "the spread lies in part within a run"이라고 적습니다. 대안이었던 repeat 추가는 bus 하나에 약 115 landing(약 230 job)이 더 필요했고, 그 값은 초당 0.014번 깨는 component의 것이라 택하지 않았습니다(9.9 D29: "~115 more landings for the bus (~230 jobs) for 0.0093, 0.075, 0.014 wakes/s").

> **왜 이렇게 정했나 — 바깥 wake를 거르는 규칙(9.9 D27), 그리고 측정 venue가 바깥 wake를 많이 만든다는 것.** 9.9 D27이 걸러낸 바깥 wake는 실린 wake보다 많았습니다. 예를 들어 `service-manager`의 scope는 `php8.3-fpm.service`가 phase마다 180–188번, `systemd-networkd`가 5–15번 pid 1을 깨웠다고 적고(둘 다 desktop에서는 안 돌거나 기본으로 꺼진 것), 실린 pid 1 wake는 phase당 114–139번입니다. 걸러내는 규칙은 package manifest와 trace 추적에 기대고, trace가 원인을 보여 주지 못한 wake(예: `job launched by pid 1: (install) 9 install systemd`)는 남겼습니다. 실제 사용자 desktop의 idle session과 비교한 검증은 없습니다. 그것은 진술된 한계입니다(3.7절의 "Real-desktop validation is deferred", measurement-overview §11).

# 10장 · idle class를 선언하는 세 항목

이 장은 여러 slice에 흩어진 세 항목을 `declared_class: idle`이라는 공통점으로 다시 모읍니다. `file-indexer`(7.6절), `incremental-backup`(7.8절), `game-download-idle`(7.4절). 질문은 "왜 이 셋만 idle이고, idle이라는 표시가 실험에서 무엇을 바꾸나"입니다. 이 질문이 중요한 이유는, idle 표시 하나가 그 파일들에서 LLM이 개선할 여지가 있는지 없는지를 거의 정해 버리기 때문입니다.

## 10.1 누가 idle인가: class census

9.11 D4(2026-10-07)는 측정된 모든 항목에 대해 "프로그램이 실제로 어떤 class를 선언했나"를 원 자료에서 읽는 일부터 시작했습니다. 이것을 **class census**라고 부릅니다(`_dev/research/jioh/task-9.11-scheduler-constants/classes/audit.md`). 읽는 방법은 둘이었습니다.

- build와 background 계열은 campaign의 taskstats 기록에 thread마다 `ac_sched`(policy)와 `ac_nice`가 남아 있어 그것을 읽었습니다.
- interactive, playback, desktop, session 계열은 `perf sched timehist` text만 남아 있어 policy를 알 수 없었습니다. 그래서 subject마다 dry job 하나를 따로 돌려, job 내내 2초마다 모든 thread의 policy, real-time priority, nice를 `/proc/<pid>/task/<tid>/stat`에서 읽었습니다(release `meas-ci-probes-2026-10-07b`). "A declared class is configuration, not timing, so one job per subject and no machine gate."

결과를 class별로 모으면 이렇습니다(audit.md의 정리).

- **`SCHED_IDLE`**: `file-indexer`(Tracker의 모든 thread, nice 19는 idle policy에서 무시됨), `incremental-backup`(`deja-dup`, `duplicity`, `gpg`).
- **normal class에 nice 0이 아닌 일**: `game-download`(SteamCMD의 content-update와 async thread가 nice 10), `package-upgrade`(`apt-check`와 `dpkg`가 nice 19, pooled CPU의 2.67 %).
- **real-time**: 실린 것 없음. session에 real-time thread가 있었지만(mutter의 KMS thread, PipeWire의 data loop, 모두 RR priority 20) 실린 component가 아닙니다.
- **`SCHED_BATCH`**: 실린 것 없음. Mesa의 shader disk-cache thread(`…:disk$0`)만 batch nice 19였습니다.
- 나머지 모든 measured 항목: normal, nice 0.

"No thread of any subject changed its policy, real-time priority or nice after its first sample." 측정 동안 class를 바꾼 thread는 없었습니다.

그래서 idle은 둘입니다. Tracker는 시작할 때마다 모든 thread를 `SCHED_IDLE`, nice 19, idle I/O class로 둡니다(tracker-miners 소스의 `tracker-main.c`, `tracker-sched.c`; 9.6 D17이 2026-09-19에 taskstats의 `ac_sched` 5, `ac_nice` 19로 처음 기록). Déjà Dup은 자기 monitor가 backup을 `chrt --idle 0 ionice -c3`로 시작합니다(`CommonUtils.vala`; 9.10 D112). 셋째 `game-download-idle`은 측정된 class가 아니라 bounding check를 위한 변형입니다(7.4절). 측정이 아닌 `game-task-chain`의 `normal`은 census가 읽은 값이 아닙니다(`_dev/research/jioh/task-9.11-scheduler-constants/classes/audit.md`: "`game-task-chain` (9.4) is no measurement"). 9.13 spec의 기본값("`normal` on every other entry")이고, 출처 `lavd-ossna24`가 class를 기록하지 않으므로 design입니다.

## 10.2 idle 표시가 바꾸는 것

executor 규칙(1.6절)은 이렇습니다. idle task는 다른 class의 runnable task가 없을 때만 돌고, 다른 class의 task가 깨면 즉시 내려옵니다. 네 algorithm 모두에서 같습니다. 9.11 D5(2026-10-07)는 예상되는 결과를 미리 적었습니다. "in `c1-indexing`, `c1-backup`, `c7-indexing`, `c7-backup`, `c2-p1b` the editor preempts the background task at once, so the editor's P99 and the background task's turnaround in those five judging files likely read no headroom." editor가 깨는 순간 배경 job을 밀어내므로, editor의 지연은 이미 최선이고 LLM이 끼어들 여지가 거의 없다는 것입니다. 9.11 D16은 이 목록에 `c2-p3b`(backup이 있는 judging 파일)를 더했습니다. scoring spec의 머리 주석도 "the six idle-class files"를 headroom이 없을 것으로 예상되는 파일로 꼽습니다(`harness/scoring/scoring-spec.yaml`).

class가 recognizer에게도 보이는지는 박이안의 결정이었습니다. memo 2026-10-08 §3이 질문했고, 2026-10-09 data-contracts §14의 기록대로 visible projection(recognizer가 보는 task 목록)이 task마다 `declared_class`를 보입니다.

idle task가 영원히 굶을 수 있다는 점도 기록에 있습니다. memo §2: "No starvation safety net. The executor builds none." 대신 harness의 `starvation_floor` guard가 모든 task의 대기를 30초로 묶습니다. 이 30초는 sched_ext watchdog이 강제하는 값을 design으로 가져온 것입니다(9.11 D7, D19).

## 10.3 실제 desktop과의 차이

> **왜 이렇게 정했나 — 같은 idle, 다른 group(9.11 D16).** 9.11 D16(2026-10-08)이 밝힌 대로, 커널의 idle 규칙은 같은 task group(cgroup) 안의 형제들 사이에서만 작동합니다(sched(7): "a thread's nice value has an effect for scheduling decisions only relative to other threads in the same task group"). Ubuntu 24.04에서:
>
> - **indexer**: Tracker의 unit은 `Slice=background.slice`이고, GNOME이 띄운 editor는 `app.slice` 아래의 scope에 있습니다. 두 slice의 CPU weight는 30과 100이므로, 둘 다 바쁘면 `background.slice`가 약 30/130 ≈ 23 %를 받습니다. 그러니 실제 desktop의 indexer는 simulator의 indexer(0 %)보다 editor를 더 방해합니다. "the headroom the indexer files can show is understated"(`file-indexer`의 `modeling_notes`).
> - **backup**: Déjà Dup의 monitor는 XDG autostart로 뜨므로 application scope, 즉 editor와 같은 `app.slice` 안입니다. 여기서는 idle weight 3 대 1,024와 즉시 preemption이 그대로 적용되어, 엄격한 규칙이 실제와 맞습니다(`incremental-backup`의 `modeling_notes`: "the strict class matches the depicted desktop's treatment").
>
> 9.11 D16이 읽지 못했다고 적은 것도 있습니다. snap으로 깐 app의 scope 배치, 이미 실행 중인 Déjà Dup 안의 backup, CPU 설정을 가진 다른 `app.slice` unit, Steam이 띄운 game이 도는 곳. simulator는 task group의 가중치를 모델링하지 않습니다. 9.11 D16은 엄격한 idle 규칙을 "design for the scheduler under test"로 두고, indexer의 `background.slice` 몫(약 23 %)과 위의 읽지 못한 것들을 한계로 적었습니다. 이 한계는 `file-indexer`의 `modeling_notes`(엄격한 규칙이 맞는 backup 쪽은 `incremental-backup`의 `modeling_notes`), 그리고 scoring spec의 머리 주석(`harness/scoring/scoring-spec.yaml`: "where the indexer's slice would take about 23 % (9.11 D16)")에 적혀 있습니다.

> **왜 이렇게 정했나 — idle I/O class는 싣지 않음(9.11 D33).** 두 프로그램은 CPU뿐 아니라 I/O에서도 idle class를 선언합니다(`ionice -c3`). simulator가 CPU lane 하나만 schedule하므로 이것은 싣지 않습니다. 측정 venue에서도 디스크 I/O scheduler가 `none`이어서 idle I/O class가 효과가 없었습니다(`incremental-backup` scope).

> **왜 이렇게 정했나 — class는 항목의 것.** memo 2026-10-08 §1: "The class is the entry's, never the name's: `c5-t3` shows two media players as `tracker-miner-f` and `baloo_file`, and they stay `normal`." 그 파일은 2026-10-12에 `c6-alias`로 옮겨졌습니다(C5 그룹, 즉 같은 행동에 점점 낯선 process 이름을 붙이는 familiarity ladder 그룹에서, 이름 기반 인식의 한계를 보이는 C6 그룹으로). indexer의 이름을 단 media player는 여전히 `normal`입니다. `c6.variant.yaml`의 주석은 이 파일을 "Another program's real name on the whole foreground"라 부르고, "No recognizer reaches `media` from these names, so the segment is a pre-committed miss"라고 적습니다. 이름만으로는 이 segment가 media 재생이라는 것을 알 수 없으므로, 처음부터 놓칠 것으로 등록해 둔 파일이라는 뜻입니다.

# 11장 · library의 과거: 열두 항목에서 스물아홉 항목으로

이 장은 "library가 예전에는 어땠고, 왜 통째로 다시 만들었나"에 답합니다. 지금의 29개 항목은 대부분 2026-09-13 이후에 생겼습니다. 그 전에는 문헌과 benchmark에서 숫자를 모은 열두 항목이 있었습니다. 이 역사를 알아야 지금 문서들 사이의 어긋남(어떤 문서는 열두 항목을, 어떤 문서는 `clamscan`이나 `game.exe`를 말함)을 이해할 수 있고, 지금 규칙들(한 항목은 한 observation, 숫자마다 출처, 출처 없는 값은 이름표)이 왜 그렇게 엄격한지도 이해할 수 있습니다.

## 11.1 Phase 2의 열두 항목

library의 첫 설계는 `docs/workload/archetype-plan.md`(2026-08-25 작성)입니다. 그 첫 판의 §2의 생각은 **two-tier grounding**(두 단계의 근거)이었습니다. 1단계, 항목이 존재해도 되는 근거는 이미 행동 분류를 가진 출처에서 "수확"합니다(interbench의 interactive·load 메뉴, LAVD의 gaming task chain, kernel build 문헌의 fork 폭주, ananicy-rules의 `type` 분류). 2단계, 항목들이 충분한지는 인용이 아니라 우리 측정(`meas-ci`)으로 확인합니다. 그 §4가 열두 항목을 나열했습니다. 2026-10-16에 9.15가 §2를 "1단계는 측정으로 근거를 얻는다"로, §4를 지금의 29개 항목으로 고쳐 썼으므로, 열두 항목 목록은 그 전의 commit(예: `18127cc9^`)에서 읽을 수 있습니다. 역사로서 정리하면 이렇습니다.

| 옛 항목 | 무엇이었나 | 숫자의 출처 | 지금은 |
|---|---|---|---|
| `audio-playback` | 50 ms마다 5 % CPU의 TIMER/RUN | interbench의 audio emulation | `audio-player`(mpv 측정) |
| `video-playback` | 16.7 ms마다 40 % CPU | interbench의 video emulation | `video-player`(mpv 측정) |
| `desktop-interactive` | 입력 gap마다 0–100 % 크기의 burst | 입력 gap은 `dhakal-chi18`, 분포 모양은 `roeser-rw24`, burst는 interbench X | application별 여섯 항목 |
| `cpu-batch` | `RUN(total_work)` 한 번, EXIT | interbench Burn, ananicy `Heavy_CPU` | batch-loop 모양의 `cpu-batch` |
| `compiler-child` | 짧은 RUN과 디스크 WAIT, EXIT | `meas-ci:cli:3`의 lognormal 수명 | 여섯-process object job |
| `build-orchestrator` | spawn table을 cap까지 FORK | kernel build 문헌 + `-j8` convention; 기본 `spawn_count` 2,430 | 측정된 dispatch + 2,908 job |
| `io-stream` | 순차 읽기·쓰기 | interbench write/read, 나중에 `meas-ci:cli:3` | `file-archiver`(그리고 한동안 `file-backup`) |
| `background-crawler` | 우선순위 낮은 파일 system 훑기 | ananicy `BG_CPUIO`; `meas-ci:cli:3` | 은퇴(9.7 D5) |
| `game-task-chain` | 약 300 task, chain + 꼬리 | `lavd-ossna24` | chain만 남김(9.4) |
| `network-bulk` | 링크를 채우는 다운로드 | `meas-ci:cli:3`의 `wget` | `game-download`; 9.10 D13에서 완전히 떠남 |
| `electron-comms` | 거의 쉬며 짧게 깸, renderer 자식 | `meas-ci:gui:2`의 Element | 네 항목으로 분할(9.8) |
| `system-daemon` | 거의 쉼, 가끔 sub-ms wake | `meas-ci:gui:2`의 server daemon 51개 | 네 항목으로 분할(9.9) |

`meas-ci:cli:3`과 `meas-ci:gui:2`는 Phase 2(2026-08-27–28)의 측정입니다. vCPU 넷짜리 runner에서 CPU 고정 없이, `forkstat`(process 생성·종료 기록기)과 `/proc` sampler(CLI workflow는 0.5초, GUI workflow는 0.2초 간격; critical findings memo C)로 쟀습니다(critical findings memo가 읽은 release `meas-ci-2026-08-28`의 `spec.json`: `nproc` 4, AMD EPYC 9V74, 16 GB). 그 요약은 `dataset/meas/summary.json`에 남아 있다가, 어떤 도구도 읽지 않아 2026-10-16에 지워졌습니다(commit `37c2e233`; 그 전의 commit에서 읽을 수 있습니다). 지금 library의 어떤 값도 그것에서 오지 않습니다. 당시에는 아직 측정하지 않은 값에 `meas-pending`을 달아 두었다가, 이 두 측정이 그것을 모두 채웠습니다(`test_repo_is_freeze_clean`의 docstring: "All meas-pending placeholders have been folded in (cli:3/gui:2)").

이 library가 compile한 core set에는 지금 기준으로 보면 이상한 모습들이 있었습니다.

- gaming 파일마다 `game.exe`라는 이름의 task가 300개(chain 16 + 꼬리 284) 있었습니다.
- `c1-compile`의 `make`는 compiler 자식 100개(`spawn_count: 100`)를 `fork_cap: 8`로 띄웠습니다.
- C7 그룹(평소 상황에 원치 않는 배경 일을 끼운 짝 파일들)의 interactive 짝 열 개와 `c2-p2b`가 원치 않는 일로 `clamscan`(ClamAV 백신 검사)을 `cpu-batch`에 묶어 돌렸습니다.
- `c1-idle`이 `gnome-shell`, `Xorg`, `pipewire`를 server daemon 값의 `system-daemon`에 묶었고, `c1-gaming`의 `wineserver`도 같은 항목에 묶여 1,225초 sleep을 뽑아 60초 동안 한 번도 깨지 않았습니다.
- 초점을 받은 interactive task는 입력 gap의 평균 절반만큼 burst를 내서 CPU를 약 50 % 썼습니다. `c1-compile`의 초점 받은 `code` task는 56초 창에서 정적 수요가 28,470,806 μs(약 28.5초)였습니다.

## 11.2 2026-09-13의 critical findings

2026-09-13, `docs/memos/2026-09-13-critical-findings.md`(archetype의 출처를 원문과 대조한 memo)가 나왔습니다. memo는 "Nothing in the repository was changed; resolution is left to the owners of each file"라고 적고, 발견을 네 묶음으로 나눕니다. 이 memo가 Phase 9 재건의 방아쇠였습니다. 주요 발견은 이렇습니다.

**A. 원문이 repository의 설명과 다름.**
- **A1.** `ocallahan-atc17`의 "2,430 processes"는 Linux kernel build가 아니라 DynamoRio 6.1.0의 build였습니다(USENIX ATC '17 proceedings §4.1: "make builds DynamoRio [8] (version 6.1.0) with make -j8"). 여덟 문서가 이것을 kernel build로 적었고, `build-orchestrator`의 기본 `spawn_count`가 2,430이었습니다. 측정한 kernel build는 compiler 계열 process가 중간값 11,883개였습니다.
- **A2.** `game-task-chain.frame_period`의 16.7 ms frame 예산은 LAVD slide 어디에도 없었습니다(4.1절).
- **A3.** Roeser의 158 ms는 log 척도의 위치(중간값에 해당)인데 평균으로 저장·추출됐고, 논문 자신의 pause 성분(약 253 ms)은 쓰이지 않았습니다(`desktop-interactive.input_gap`).
- **A4.** Coetzee의 짧은 kernel build process는 compiler가 아니라 `cp`와 `mkdir`였습니다.
- **A5.** ananicy-rules의 `type`은 행동이 아니라 처방(어떻게 대할지)으로 묶은 분류였고, 같은 목록이 `meas` 항목들에도 맞는 class를 갖고 있어 "수확" 규칙이 고르지 않게 적용됐습니다.

**B. dataset과 도구.**
- **B1.** `game-task-chain`의 두 param은 compiler가 읽지 않았고, 꼬리 param은 slide tag를 단 자리표시자였습니다.
- **B2.** `compiler-child.disk_wait`의 `sigma_log: 0.8`은 측정 전 자리표시자가 측정 tag를 단 채 남은 것이었습니다.
- **B3.** 측정한 최대 동시 compiler 계열 process는 16개인데 항목은 자식을 8개로 묶었습니다(단위가 다름: job 대 process).
- **B4.** 끝없는 loop에 `per-iteration` sampling을 선언했지만 compile은 `per-task`로 했고, 측정된 흩어짐은 process 사이의 것이었습니다.
- **B5.** `desktop-interactive`의 burst가 입력 gap의 절반이라 초점 받은 editor가 CPU 약 50 %를 썼습니다. 출처인 interbench X는 "창을 잡아 화면을 가로질러 끄는" emulation이었는데, 입력 gap은 받아쓰기 typing에서 왔습니다.
- **B6.** session process가 server daemon 측정값에 묶였습니다.
- **B7.** 작은 어긋남들(linter가 `category_source`의 값을 검사하지 않음, timeline의 개수에 source 자리가 없음 등).

**C.** measurement fold-in 뒤에도 낡은 문장이 남은 문서들. **D.** 원문을 읽지 못한 출처 둘(`chang-chi21`, `cpsmark-tbench23`).

발견은 A1–A5, B1–B7, C의 13개이고, D는 발견이 아니라 원문을 읽지 못한 출처의 목록입니다(2026-10-16, 인지오의 읽기). Phase 9 spec은 이 13개 발견에, 같은 날의 검사에서 memo가 빠뜨린 여섯 가지를 더했습니다(interbench의 Compile load는 process를 fork하지 않음, 다운로드 sleep "~5.7 ms"가 어떤 판의 library와도 맞지 않음, Roeser의 Table 3이 항목이 convention이라 부른 흩어짐을 보고함, LAVD slide 12와 16의 wineserver, CpsMark+가 "time-shared compositions"와 모순됨, `chang-chi21`의 세부).

## 11.3 Phase 9의 결정: 한 항목은 한 observation

같은 날 Phase 9 spec session이 열렸고(`_dev/docs/spec/jioh/phase-9-workload-dataset-rebuild.md`), 다음을 잠갔습니다.

- **decision 1, 검증 기준.** "A claim taken from a source is verified when it is recorded with the verbatim passage, its locator, and the copy read (URL or commit, version, date), and the check covers the whole claim the repository makes — its object, unit, statistic, scope and population. … A value no source states carries no source tag and is labelled for what it is: convention, arithmetic, placeholder, or design."
- **decision 2, no montage.** "All numbers of one archetype come from one observation: one study population, one trace, or one measurement run. Several documents about the same observation count as one source; one document mixing different traces does not. Our own measurement run counts as one observation. Research looks for one observation that covers the whole archetype first; where none exists, the archetype comes to 인지오 as a decision."
- **decision 3**, timeline에도 같은 규칙. 현실을 그린다고 내세우는 timeline 내용(task 구성, 동시 발생, 순서, 개수, 전형적 길이, process 이름)은 상황마다 한 observation을 따르고, 실험 자신의 개입과 calibration 크기(label 뒤집기, 끼워 넣기, 이름 바꾸기, 파일 길이, `lane_share`)는 design으로 이름표를 붙입니다.
- **decision 4**, 연구로 빈자리를 채운다. 한 observation이 없다고 선언하려면 네 갈래(문헌, 프로젝트·vendor 문서와 source code, 공개 trace와 dataset, 우리 측정이 관측할 수 있는가)의 검색 기록이 먼저 있어야 합니다.
- **decision 5**, 측정 venue. "Our own measurement runs on CI runners only. What a runner cannot observe comes from literature or public traces, or to 인지오 as a decision. This is a stated limitation."

**montage**가 무엇이었는지 예로 보면 decision 2가 왜 필요했는지 보입니다. 옛 `desktop-interactive`는 입력 gap의 전체 평균을 `dhakal-chi18`(136M Keystrokes: 외운 문장을 받아 적는 transcription typing, 참가자별 평균 IKI의 평균 238.66 ms)에서, 분포 모양(fluent 158 ms, pause 확률 0.34)을 `roeser-rw24`(다른 과제의 다른 참가자들)에서, burst 크기를 interbench X(창 끌기 emulation)에서 가져왔습니다. 세 다른 observation의 숫자를 한 항목에 섞으면, 각 숫자는 출처에 충실해도 그 조합은 어떤 실제 process도 그리지 않을 수 있습니다. 그 결과가 B5의 "editor가 CPU 50 %"였습니다. 9.5 D19(2026-09-15)는 이 항목과 두 playback 항목을 "the three montage entries"라고 부르며 측정된 아홉 항목으로 바꿨습니다.

decision 2의 직접적인 결과는, 거의 모든 항목이 우리 CI 측정으로 옮겨 간 것입니다. 각 slice가 네 갈래의 검색을 했고, 한 항목을 통째로 덮는 외부 observation을 찾지 못한 곳(대부분)에서 runner 측정을 택했습니다. 유일한 예외가 runner로 관측할 수 없는 game chain이고, 그것은 LAVD 발표 하나를 "one observation"으로 받아들이는 인지오의 결정(9.4 D1)으로 남았습니다.

## 11.4 재건의 순서

| 날짜 | 무엇이 바뀌었나 | 기록 |
|---|---|---|
| 2026-09-13 | `game-task-chain`: 300 task와 꼬리 제거, wineserver를 member로, frame 주기를 `steamos-refresh`로 | 9.4 D1–D8 |
| 2026-09-15 | 측정된 아홉 항목이 `desktop-interactive`, `audio-playback`, `video-playback`을 대체(vCPU 넷, CPU 고정 없음, 5 repeat) | 9.5 D19 |
| 2026-09-16 | 같은 아홉 항목을 CPU 하나에 고정해 다시 잼; operation 셋 추가 | 9.5 D21, D25 |
| 2026-09-18 → 09-29 | EPYC 7763 machine gate와 stability rule 아래 아홉 항목을 다시 잼(keys only, settle, launch work 배제 등) | 9.5 D26–D99 |
| 2026-09-20 | build campaign fold-in: 여섯-process object job, 측정된 dispatch, `cpu-batch`의 run/block table | 9.6 D31 |
| 2026-09-22 | `io-stream` → `file-backup`, `file-archiver`; `electron-comms` → 네 항목 | 9.7 D31, 9.8 D25 |
| 2026-09-23 | `game-download`가 들어오고 `c2-p2a`의 다운로드가 `network-bulk`에서 옮겨 감 | 9.7 D34 |
| 2026-09-24 | `system-daemon` → session 네 항목; `Xorg` 은퇴 | 9.9 D26 |
| 2026-09-26 | TIMER는 deadline 있는 주기 job만; 측정된 timer wake는 `WAIT(timer)`; 재생 항목은 cycle job | 9.5 D74, D75 |
| 2026-09-27 | untraced control 결과를 모든 measured 항목의 notes에 | 9.5 D82, 9.8 D32, 9.9 D40 |
| 2026-10-01 | `renderer-visible` 떠남; `network-bulk` 떠남; `package-upgrade` 들어옴(`clamscan` 대체) | 9.10 D16, D13, D45 |
| 2026-10-02 | `module-build-orchestrator`와 `module-compiler-child` 들어옴 | 9.10 D59 |
| 2026-10-03 | `file-indexer` 들어옴(`cpu-batch`의 `tracker` 대체); `python3`를 MNIST로 다시 잼; `video-transcoder` 들어옴 | 9.10 D81, D90, D100 |
| 2026-10-04 | `cpu-batch`의 `kdenlive_render` 들어옴(`ffmpeg` 대체); `incremental-backup` 들어옴, `file-backup` 떠남 | 9.10 D111, D125 |
| 2026-10-05 | 열 항목에 launch phase; `video-editor` idle 다시 잼; `renderer-hidden`을 Chrome 154로 다시 잼 | 9.10 D140, D146, D156 |
| 2026-10-09 | 모든 항목에 `declared_class`; `game-download-idle` 들어옴 | 9.13 D2, D4 |

## 11.5 이름이 사라진 것들

지금 문서 일부에는 아직 옛 이름이 남아 있습니다. 무엇이 무엇으로 바뀌었는지 한곳에 모읍니다.

- `clamscan`(원치 않는 백신 검사) → `package-upgrade`(`unattended-upgr`). 9.10 D3.
- `game.exe` × 300 → `Troy.exe` chain 16개 + `wineserver`(이름은 `member_names`). 9.4 D3, 9.10 D26.
- `make`의 compiler 자식 100개, `fork_cap` 8 → object job 2,908개(spawn table 17,448개), `fork_cap` 48. 9.6 D19, 9.10 D18.
- `c7-compile`의 `make` → `dkms` 이름 바꾸기 → 실제 NVIDIA module DKMS build. 9.10 D4.
- `borg`(`file-backup`) → `deja-dup`(`incremental-backup`). 9.10 D8, D125.
- `ffmpeg`(render 대역) → `kdenlive_render`. 9.10 D10, D105.
- `HandBrakeCLI` 720p(`cpu-batch`) → `video-transcoder`. 9.10 D11, D97.
- `tracker-miner-fs-3` 전체 재검사(`cpu-batch`) → `tracker-miner-f`(`file-indexer`, 첫 색인). 9.10 D5, D70, D74.
- `python3` 합성 학습 loop → `python`(PyTorch MNIST). 9.10 D12, D84.
- `discord` → `element-desktop`(`chat-client`); `zoom` helper 은퇴; `steamwebhelper` task 은퇴. 9.8 D7, D8, D25.
- `Xorg` 은퇴. 9.9 D26.

이 권을 처음 쓴 2026-10-14에는 이 변화들 때문에 `docs/workload/archetype-plan.md` §4, `docs/data-contracts.md` §2의 "There are twelve" 문단과 예시, `docs/workload/coreset-guide.md` §4 이후, `docs/workload/scenario-catalog.md`의 process 이름 열, `docs/workload/measurement-overview.md`의 항목 표가 library와 달랐습니다. docs·memo·guidebook 정리 sub-task 9.15가 2026-10-16과 10-17에 이 문서들을 지금 library에 맞게 고쳤습니다. archetype plan §4와 coreset guide §4는 29개 항목을 나열하고, data-contracts §2의 그 문단은 "There are 29"라고 적으며, scenario 목록은 지금 timeline이 묶는 이름을, measurement overview §2는 measured 항목 28개를 적습니다. 그래도 문서와 데이터가 다르면 `dataset/archetypes.yaml`과 그 `scope`·`modeling_notes`, slice changelog들이 기준입니다.

# 12장 · 기록이 스스로 밝히는 한계

이 장은 "이 library의 숫자를 어디까지 믿어도 되나"에 답합니다. 이 질문에 대해 기록은 의외로 솔직합니다. 거의 모든 항목의 scope가 "this software on this machine"으로 끝나고, slice들은 한계를 결정마다 적어 두었습니다. 여기서는 그 한계들을 성격별로 모으고, 각 한계에 대해 dataset을 쓰는 쪽(RQ0 판정 spec)이 어떤 민감도 검사를 준비했는지도 함께 적습니다. 민감도 검사의 정의는 `dataset/variants.yaml`(RQ0 gate spec이 쓰는 변형 파일 집합의 정의)에 있습니다. 변형 파일 자체는 다른 권에서 다룹니다.

## 12.1 library 수준의 scale 한계

9.5 follow-ups spec decision 13(2026-09-16)은 library 전체에 대한 한계를 이렇게 정했습니다. "The library's archetypes come from more than one observation venue, and their relative scales are not calibrated to each other; a timeline composing a runner-measured task with a literature-grounded one carries that limitation. It is stated once at the library level." 항목들이 서로 다른 관측 장소에서 왔고, 그 크기들이 서로 맞춰져 있지 않으므로, runner에서 잰 task와 문헌에서 온 task를 한 timeline에 섞으면 그 한계를 함께 진다는 뜻입니다. 같은 결정은 "A scale bridge, one benchmark figure both machines report, may be written into scope as the ratio, never applied to a value"라고 덧붙입니다. 두 machine을 잇는 기준 숫자가 생겨도 scope에 비율로 적을 뿐 값을 고치는 데 쓰지는 않는다는 것입니다.

지금 library에서 이 경계(composition seam)는 한 곳입니다. LAVD 발표의 이름 없는 machine(여러 core)에서 온 `game-task-chain`과, runner의 core 하나에서 잰 나머지 28개 항목이 gaming 파일에서 만납니다. chain은 `lane_share`로 크기를 맞추지만, 그 맞춤은 "our calibration, not the source's"입니다(`modeling_notes`). runner 항목들끼리도 측정 날짜와 프로그램 판이 다르지만, 모두 같은 CPU 모델(EPYC 7763) 위에서 쟀습니다.

> **왜 이렇게 정했나 — 이 문장이 놓인 곳.** decision 13은 이 한계를 "stated once at the library level"이라고 정했지만, 이 권을 처음 쓴 2026-10-14에는 `dataset/archetypes.yaml` 머리 주석, `dataset/README.md`, `docs/` 어디에도 이 문장이 없었습니다(spec과 slice scope card에만 있었음). 2026-10-16에 9.15가 이 문장을 library를 주제로 하는 문서인 `docs/workload/archetype-plan.md` §2의 "Observation venues" 문단에 decision 13의 문장 그대로 적었습니다. `dataset/README.md`와 measurement-overview §11은 이것을 다시 적지 않습니다. `archetypes.yaml` 머리 주석에 넣지 않은 것은, 그 파일을 고치면 일곱 manifest가 모두 다시 bless되고 RQ0 gate spec이 다시 pin되기 때문입니다(9.15 작업 목록 `_dev/research/jioh/task-9.15-docs-memos-and-guidebook-corrections/work-list.md`의 "Settled at merge"). 함께 넘겨진 두 일 가운데 9.14의 민감도 검사는 아래 12.2절의 `venue-x0.8`/`venue-x1.25`와 `chain-x1.2`/`chain-x1.4` 변형으로 들어갔고, 9.16(exit audit)의 "venue mix listed per timeline"은 2026-10-17에 9.16이 timeline마다 묶는 항목의 venue를 나열해 확인했습니다(`_dev/research/jioh/task-9.16-exit-audits/handed/checks.md`). core set 51개 가운데 두 venue(runner와 `lavd-ossna24`)를 섞는 것은 `game-task-chain`을 묶는 여덟 개(`c1-gaming`, `c2-p2a`, `c2-p2a-idle`, `c2-p2b`, `c3-evening`, `c4-gaming`, `c6-dual`, `c7-gaming`)이고, 나머지 43개는 runner만 씁니다. generated layer에서 두 venue를 섞는 파일도 모두 `game-task-chain`을 묶습니다.

## 12.2 venue의 한계

runner는 실제 desktop이 아닙니다. 항목들의 scope가 적는 venue 한계를 모으면 이렇습니다.

- **화면, GPU, 소리 없음.** Xvfb 또는 headless session, vsync 없음, `--disable-gpu`로 CPU rasterize, 소리 장치 없음(null 출력). Chromium 계열의 compositor는 60 Hz 주기지만 위상이 다르고, rasterize thread의 run은 GPU desktop보다 길게 잡힙니다(양은 출처 없음). Kdenlive의 렌더 경로는 wake가 과대평가됩니다. llvmpipe thread는 뺐습니다(5.1절, 5.7절).
- **CPU 하나에 고정, runner agent와 공유.** 측정한 tree는 CPU 하나에서 돌았고, runner 자신의 agent process가 그 CPU를 함께 썼습니다. 여러 thread 프로그램(7-Zip 여덟 thread, `make -j8`)은 실제 desktop이라면 여러 core에서 나란히 돌 일을 한 core에서 나눠 돌았습니다. 기록된 크기: 7-Zip 여덟 thread가 byte당 CPU 1.04–1.10배, `make -j8`가 `-j1` 대비 compile당 CPU 약 1.1배.
- **CPU 모델 하나, 시기 하나.** AMD EPYC 7763 하나만, 2026-09-18부터 2026-10-05 사이에. runner 커널(6.17.0-1022-azure)은 THP `always`이고 desktop 기본은 `madvise`입니다(학습 job 1.144배).
- **tracing 비용.** `perf sched record`가 일부 thread의 run을 길게 만들었고(untraced control의 run 평균 비율 0.72–0.98), SteamCMD의 `perf trace`는 CPU를 약 2.5 % 더 쓰게 했습니다. 실린 값은 traced 값입니다.
- **사람 없음.** 입력은 2012년 Windows 녹화의 재생이고(key만), 이미지·영상 편집은 script입니다.

> **왜 이렇게 정했나 — 이 한계를 다루는 방식.** 9.6 D32(2026-09-20): "The venue's effect is untested, and the test belongs to the consumer." 그 결과가 RQ0 gate spec의 `venue-x0.8`과 `venue-x1.25` 변형입니다(`dataset/variants.yaml`). judging 파일 19개에서 chain을 뺀 모든 측정 RUN 값을 1/1.25배와 1.25배로 바꿔 다시 판정합니다. 1.25는 design이고, 그 근거로 "a design bracket containing the two measured venue effects — the ×1.144 huge-page ratio … and the tracing overhead's ×1.02 to ×1.16"을 적습니다. 판정 개수가 이 축에서 움직이면 판정을 범위로 보고합니다(9.14 decision 10). chain에는 따로 `chain-x1.2`, `chain-x1.4`가 있습니다(4.1절). 이 괄호는 다른 CPU 기종을 나타내지 않습니다. 다른 CPU는 program마다 다른 배율로 빠르기를 바꾸므로(3.3절의 Intel Xeon: `cc1` 0.72배, `fixdep` 0.50배) 공통 배율 하나로는 재현되지 않습니다. 2026-10-16에 인지오는 괄호를 그대로 두고 이 한계를 적기로 했고, `docs/research-claims.md`의 "What is not claimed"와 measurement-overview §11이 그것을 적습니다.

> **왜 이렇게 정했나 — 실제 desktop 검증은 진술된 한계.** measurement-overview §11: "Real-desktop validation is deferred." 실제 사용자 desktop에서 같은 프로그램을 재어 맞춰 보는 일은 하지 않았습니다. 2026-08-26의 grill 결정(D8)은 "meas-live dropped from the research entirely"였고, 대신 수집 도구와 개인정보 제거 도구를 "open falsification invitation"으로 내놓기로 했는데, critical findings memo(B7)가 그 도구가 repository에 없다고 지적했습니다. 2026-10-14에 repository의 `.py`와 `.sh` 파일을 "scrub"으로 검색했을 때도 그런 도구는 없었습니다(유일하게 걸린 `dataset/tools/meas/campaign/fold_in.py`의 한 줄은 Kdenlive의 clip monitor를 "scrubs"(훑는다)라는 뜻으로 쓴 것임). 2026-10-16에 인지오는 그 도구의 약속을 거두었습니다. 문서들은 약속을 지우고, 실제 desktop 검증은 진술된 한계로 남습니다(measurement-overview §11). 같은 날 인지오는 실제 desktop과의 비교를 열지 않고 runner라는 범위를 논문에 그대로 싣기로 했습니다(`docs/research-claims.md`의 "What is not claimed"). 실제 desktop 검증을 나중에 연다면, 도구는 그 계획 안에서 정합니다.

## 12.3 wake 흐름은 분포를 재현하지 순서를 재현하지 않습니다

compiler는 component마다 gap을 표에서 서로 독립으로 뽑습니다(9.5 D77). 그래서 compile된 흐름은 각 component의 **비율, gap 분포, run 분포**는 지키지만, 다음 두 가지는 지키지 않습니다.

1. **gap의 순서.** 실제 thread는 "짧은 gap 셋 뒤에 긴 gap 하나"처럼 순서 있는 리듬을 가질 수 있는데, 독립 추출은 그 순서를 섞습니다. `office-writer`의 몰아 깨기(2.9절)는 표가 짧은 gap을 많이 담고 있어 우연히 비슷하게 나오지만, 몰아 깨기의 길이와 간격을 보장하지는 않습니다.
2. **component들의 동시 깨어남.** 실제 application에서는 한 thread가 깨면 다른 thread도 곧 깨는 일이 많습니다(compositor와 IO thread처럼). component를 따로 뽑으면 그런 함께 깸이 사라집니다.

batch-loop 항목의 단계 순서(7.1절), heavy event의 몰림(`CHTTPClientThre`의 burst, 4.2절)도 같은 종류의 한계입니다. 같은 항목에 묶인 task 사이에서도 그렇습니다. `renderer-hidden`의 측정에서 숨은 renderer 열둘은 process를 넘어 함께 깨는데(9.8 D15, renderer들의 wake 맞물림을 잰 기록; 2026-09-20 probe: 열둘이 모두 같은 1 s bin에서 깬 것이 243번, 같은 10 ms bin에서 32번, 독립 추출에서는 0번), Chrome 파일에 묶인 renderer task 넷은 각자 독립적으로 compile됩니다. 이 맞물림은 지금의 pool(`meas-ci:desktop:2026-10-05b`)에서 다시 읽지 않았습니다.

이것은 측정으로 크기가 재어졌습니다. `dataset/tools/meas/burstiness.py`(이 비교를 하는 도구)는 repeat마다 측정된 wake 흐름과, 같은 구간을 compile한 흐름을 1 ms, 10 ms, 100 ms, 1 s bin으로 세어 dispersion(분산/평균; Poisson이면 1, 크면 몰려 옴)을 비교합니다. measurement-overview §8은 이것을 "a stated threat to validity"로 적고, 1–100 ms에서 측정된 것의 dispersion을 compile된 것의 dispersion으로 나눈 비율을 항목마다 적습니다(carried repeat의 중앙값, 2026-09-27에 읽음). `chat-client` 3.3–11배, `code-editor` 2.6–3.4배, `web-browser` 2.8–3.4배, `mail-client` 1.9–3.0배, `game-client` 1.9–3.0배로, 이 다섯 항목에서 실제는 compile된 것보다 1.9–11배 더 몰려서 깹니다. `renderer-hidden`(1.26–1.44배)과 `video-editor`(1.22–1.32배)는 차이가 작고(둘 다 지금 실린 pool, `meas-ci:desktop:2026-10-05b`와 `meas-ci:interactive:2026-10-05`의 유휴 단계에서 2026-10-17에 다시 읽은 값), `audio-server`, `service-manager`, `message-bus`는 약 1이며, `compositor-shell`과 `office-writer`는 오히려 compile된 흐름이 더 몰려 있습니다(1 미만). scheduler에게 몰림은 중요합니다. 같은 평균 부하라도 몰려 오면 대기 시간의 꼬리가 길어지기 때문입니다.

> **왜 이렇게 정했나 — 이 한계를 다루는 방식.** `dataset/variants.yaml`의 `replay` 변형이 이 한계를 위한 것입니다(9.14 decision 12). 네 judging 파일(`c7-dev`, `c7-browsing`, `c7-meeting`, `c2-p1a`)에서, 여섯 항목(`code-editor`, `web-browser`, `renderer-hidden`, `video-call`, `package-upgrade`, `cpu-batch`의 `python3`)의 compile된 흐름을 pooled repeat 하나에서 실제로 관측한 흐름으로 바꿔 넣습니다(`dataset/replay/`, 2.11절). 넣는 흐름은 항목마다 종류가 정해져 있습니다(각 흐름 파일의 `kind`). `code-editor`, `web-browser`, `renderer-hidden`은 관측된 wake를 그 시각과 run 그대로(`wakes`), `package-upgrade`와 `cpu-batch`의 `python3`는 관측된 run과 그 뒤의 block을 시간 순서대로(`runs`), `video-call`은 주기는 그대로 두고 cycle마다 관측된 CPU 양을 차례로(`cycles`) 넣습니다. variants manifest의 `replay` 항목을 보면 네 파일 모두 batch job의 run 흐름(`c7-dev`, `c7-browsing`, `c7-meeting`의 `package-upgrade`, `c2-p1a`의 `python3`)을 바꿔 넣고, `c7-meeting`은 통화의 cycle 흐름도 바꿔 넣습니다. 이유: "one pooled repeat's measured wake sequence in place of the compiled stream, for the four judging files that cover every term shape (… the 2026-09-26 burstiness finding)". 이 이유는 "wake sequence"라고만 적지만, `variants.yaml`의 `trace-replay` 주석은 2026-10-17부터 위의 세 종류를 적습니다. library 항목 자체는 바뀌지 않습니다. 항목에 `replay` param을 넣는 것은 이 변형 집합을 만들 때뿐이고, linter는 그 파일이 `dataset/replay/`에 있는지만 확인합니다. 흐름 파일의 종류가 항목이 요구하는 것과 맞는지는 compiler(`dataset/tools/wlc/compiler.py`의 `_replay_window`)가 확인하고, 맞지 않으면 build가 실패합니다.

## 12.4 stability rule이 보장하지 않는 것

- **대표성.** stability rule은 "this software on this machine"에서의 정밀도(재현성)를 보장할 뿐입니다(3.7절).
- **멈춤의 낙관.** 첫 통과에서 멈춰서, 기준선에 붙은 값의 95 % 구간은 실제로 약 91–94 %만 덮습니다(3.4절).
- **예외로 실린 값.** 다섯 예외 class의 값(3.5절)은 5 % 밖일 수 있고, 반폭이 scope에 적혀 있습니다. 규칙: "no reported result may rest on a difference smaller than a stated half-width." RQ0 gate spec은 이 값들을 모두 95 % 구간의 아래 끝과 위 끝으로 옮긴 `corner-low`, `corner-high` 변형으로 판정이 바뀌는지 봅니다(`variants.yaml`의 `carried_values` 목록, 2026-10-17에 표 19개: `code-editor`의 `libuv-worker`, `renderer-hidden`의 component 여섯(residual, `HangWatcher`, page thread `chrome`, 조용한 thread `Chrome_ChildIOT`, `Compositor`, `PerfettoTrace`), `game-client`의 넷, `cpu-batch` `python3`의 둘, `module-build-orchestrator`의 꼬리 block). `Compositor`와 `PerfettoTrace`는 2026-10-17에 목록에 들어왔습니다. 그 전에는 `meas-ci:desktop:2026-10-05b`부터 session 사이에서 변하는 값으로 실렸는데도(9.10 D156) corner set이 훑지 않았습니다. judging 파일이 담지 않는 항목의 값(session daemon의 pid 1과 system bus)은 훑지 않습니다. `variants.yaml`의 주석은 2026-10-16까지 Tracker의 block도 훑지 않는 값으로 적었지만, 지금의 `file-indexer`는 세 값 모두에서 stability rule을 지키고(항목의 scope: "the stability rule holds on all three values"), 그 구절은 2026-10-17에 주석에서 빠졌습니다. 그 구절은 `cpu-batch`의 옛 `tracker` program(9.6 D29의 예외) 때의 것이었습니다.
- **녹화의 끝.** `mail-client`와 `web-browser`의 일부 값은 녹화 창이 바닥나 규칙 밖에 있습니다(5.4절, 5.5절).

## 12.5 항목별로 기록된 한계 모음

마지막으로, 항목의 scope와 modeling_notes가 스스로 적은 한계 중 실험 해석에 직접 닿는 것들을 한곳에 모읍니다.

| 항목 | 한계 | 방향 | 기록 |
|---|---|---|---|
| `game-task-chain` | 출처의 schedule당 runtime을 wake당 RUN으로 읽음 | chain 수요를 줄여 잡음(약 1.4배) | 9.4 D9 |
| `game-task-chain` | 출처의 graph를 한 줄 chain으로 폄; 머리만 timer | 구조 근사 | modeling_notes |
| `game-task-chain` | game의 나머지 thread 생략 | 수요를 줄여 잡음 | 9.10 D19 |
| `game-client` | 로그아웃 상태를 잼; 파일은 게임 뒤 로그인 상태를 그림 | 알 수 없음 | 9.8 D6, 9.10 D22 |
| `game-download` | nice 10의 일(75 %)을 온전한 지위로 실음 | 게임에 대한 간섭을 크게 잡음, headroom 부풂 | 9.11 D6, D20 |
| `game-download` | SteamCMD로 desktop client를 대신함 | 방향 모름 | 9.7 D4 |
| `game-download` | `fq_codel` 링크 모델 | token bucket이면 network wait +43 % | 9.7 D25 |
| `package-upgrade` | nice 19의 일(2.67 %)을 온전한 지위로 | 작음 | 9.11 D20 |
| `file-indexer` | 엄격한 idle class; 실제는 `background.slice`로 약 23 % | indexer 간섭을 작게 잡음, headroom 과소 | 9.11 D16 |
| `file-indexer`, `incremental-backup` | idle I/O class 싣지 않음 | – | 9.11 D33 |
| batch-loop 항목들 | 단계 순서 싣지 않음 | 긴 run이 job 아무 데나 | modeling_notes |
| batch-loop 항목들 | 여러 thread를 한 표로 납작하게 | thread별 강등을 못 보임 | 9.6 D22 |
| `build-orchestrator`, `module-build-orchestrator` | `-j8`을 한 core에서 잼 | compile당 CPU 약 10 % 많음 | 9.6 D4, D9 |
| `compiler-child` | step 수는 구조, wake 수 아님(`sh` 4 대 실제 5–7) | wake 수를 줄여 잡음 | 9.6 D20 |
| `cpu-batch` `python3`, `video-transcoder` | THP `always` | desktop 기본이면 CPU 약 14 % 많음(학습) | 9.10 D87, D88 |
| typing 항목 넷 | SWELL-KW 녹화, key만 | 다른 녹화면 0.91–1.34배 | 9.5 D81 |
| `code-editor` | AI 보조 기능 없는 판(1.139.0의 assistant runtime은 "a different workload"); extension host episode 제외 | episode 동안의 per-input run(실린 값의 최대 3.9배)을 싣지 않음 | 9.5 D69, 9.10 D158 |
| `renderer-hidden` | 살아 있기만 하는 page; 유예 전 tab 제외 | 바닥 값 | scope |
| `renderer-hidden`과 `web-browser` | 서로 다른 Chrome 판(154 대 152/153) | 한 browser의 두 반쪽 | 9.10 D156 |
| `chat-client` | 메시지 없는 idle만 | traffic이면 약 4배 | 9.8 D11 |
| session 네 항목 | 아무도 없는 잠긴 session만 | 사용 중 session은 다루지 않음(9.9 D1이 인용한 다른 관측에서 Mutter 49.3의 GNOME Shell은 login 직후 초당 약 1,500번 깸) | 9.9 D1, D9 |
| 재생·통화 셋 | deadline은 cycle의 것이지 장치의 것 아님 | 늦은 cycle이 곧 끊김은 아님 | scope |

# 13장 · 용어 정리

이 권에서 풀이한 용어를 모읍니다. 두 종류로 나눕니다. 이 repository가 만들었거나 자기 뜻으로 쓰는 **project 용어**, 그리고 웹 개발에서는 잘 만나지 않는 **OS·scheduling 용어**입니다. 괄호 안은 처음 나온 곳입니다.

## 13.1 project 용어

| 용어 | 뜻 |
|---|---|
| archetype | 프로그램 한 종류가 CPU를 쓰는 모양을 적은 규칙과 숫자 묶음. `dataset/archetypes.yaml`의 항목 하나(1장) |
| archetype library | `dataset/archetypes.yaml` 전체. dataset의 맨 아래층이며 행동 숫자가 사는 유일한 곳(머리말) |
| archetype id | 항목의 key(`office-writer` 등). workload 파일에는 쓰이지 않음(1.1) |
| timeline | 이름, 시각, archetype을 엮어 파일 하나의 상황을 적은 문서(`dataset/timelines/coreset/<id>.timeline.yaml`)(머리말) |
| workload 파일 | compiler가 쓴, 무작위성이 모두 풀린 실행 파일. simulator가 읽는 유일한 형식(머리말) |
| wlc / compiler | timeline과 library를 읽어 workload를 쓰는 도구(`dataset/tools/wlc/`)(머리말) |
| core set | 손으로 만든 workload 파일 묶음(지금 51개). 파일 id의 `c1-`…`c7-`는 그룹 이름(1.1, 2.9) |
| C1 그룹 | 한 상황만 60초 동안 보이는 calibration 그룹(2.9) |
| C2 그룹 | 한 segment만 다른 두 파일의 짝(intent pairs). 예: `c2-p1a`/`c2-p1b`(1.1) |
| C3 그룹 | 여러 상황을 이어 붙인 긴 arc 파일들(`c3-workday`, `c3-evening`, `c3-creation`)(5.1) |
| C4 그룹 | C1 파일을 복제해 segment 중간에 낯선 process를 끼우고 원본과 짝지은 distractor 그룹(7.1) |
| C5 그룹 | 같은 행동에 점점 낯선 process 이름을 붙이는 familiarity ladder 그룹(10.3) |
| C6 그룹 | 이름 기반 인식의 한계를 일부러 보이는 그룹(`c6-spoof`, `c6-alias` 등)(6.3, 10.3) |
| C7 그룹 | 평소 상황 파일에 원치 않는 배경 일을 끼운 짝 파일 그룹(7.5) |
| segment | timeline 안에서 하나의 상황 label(mode)이 유지되는 시간 구간(1.1) |
| `input` 창 | 사용자가 그 task에 입력하고 있다고 timeline이 정한 시간 구간. typing 항목은 여기서 key를 재생(2.4) |
| judging set | RQ0 판정에 쓰는 core set 파일 묶음(지금 19개)(7.4) |
| headroom | 기본 scheduler 대비 LLM이 개선할 수 있는 여지(1.6) |
| pre-committed miss | 처음부터 놓칠 것으로 등록해 둔 파일·segment(10.3) |
| visible projection | recognizer가 보는 task 목록(이름, class, 도착·떠남, 자식 개수)(10.2) |
| slice(연구 slice) | Phase 9가 영역별로 나눈 연구·결정 단위. 9.4 gaming, 9.5 interactive·typing, 9.6 compile, 9.7 background·IO, 9.8 browser·comms, 9.9 daemon·session, 9.10 scenario·timeline, 9.11 scheduler 쪽 상수(4장) |
| D번호 | slice changelog의 결정 번호. "9.5 D13"은 9.5 slice의 13번째 결정(4장) |
| Phase 9 decision 1–5 | 재건의 잠긴 결정: 검증 기준, no montage, timeline 규칙, 연구로 빈자리 채우기, CI만 측정 venue(11.3) |
| boundary rules | 이름·개수·의미는 archetype에 없고, source tag는 field 이름을 정당화하지 않는다는 두 규칙(1.1) |
| montage | 서로 다른 observation의 숫자를 한 항목에 섞는 것. Phase 9 decision 2가 금지(11.3) |
| observation | 한 연구 모집단, 한 trace, 한 측정 run. 한 항목의 숫자는 하나의 observation에서(11.3) |
| two-tier grounding | 옛 설계: 존재는 분류표 수확으로, 충분함은 측정으로(11.1) |
| `category_source` | 항목의 행동 부류가 어디서 왔나. 28개가 `meas`, 하나가 `lavd-ossna24`(2.2) |
| `meas` | "우리 측정에서 관찰한 행동 부류"라는 `category_source` 값(2.2) |
| `declared_class` | 프로그램이 스스로 선언한 scheduling class. `normal` 또는 `idle`, 필수(1.6) |
| `pattern` / `program` | 항목의 행동 틀과 그 primitive program(2.2) |
| constructor | compiler가 항목을 특별히 펼치라는 표시. `batch-loop`, `chain`, `module-build`(2.2) |
| `params` | program이 이름으로 부르는 숫자들(2.2) |
| distribution object | `{dist, 매개변수, sampling, source}` 꼴의 숫자 하나(2.3) |
| `constant` / `lognormal` / `quantiles` | dist의 세 종류. quantiles는 p1…p99.9, min, max, 구간 평균을 싣는 측정 표(2.3) |
| anchors | lognormal의 두 기준점(`anchor_min_us`, `anchor_max_us`), p05/p95로 읽음(2.3) |
| `sampling` | 숫자를 몇 번 뽑나: `per-instance`(spawn 자식마다), `per-task`(task마다 한 번), `per-iteration`(반복마다, 반복 수가 정해질 때만)(1.4) |
| source tag | 숫자의 출처 `<id>` 또는 `<id>:<locator>`(2.8) |
| locator | 출처 안의 위치(slide 번호, 조건, campaign 등). `locator_pattern`으로 검사(2.8) |
| registry | `dataset/sources.yaml`. 출처 id 19개(2026-10-17; 2.8) |
| release 지도 | `dataset/meas-releases.yaml`. 데이터가 인용하는 `meas-ci` campaign마다 원 자료를 담은 release와 asset의 SHA-256. `make lint`가 검사(3.3) |
| subset lint | registry의 모든 id가 `docs/references.md`에 있어야 한다는 검사(2.8) |
| citation tier | scholarly(경험적 주장 가능), deployed-system(존재, 그 시스템 자신의 설계와 동작, 그 출처가 공개한 숫자를 그 출처의 말로), talk·학회 초록·뉴스 보도(발표자나 기자의 주장으로만), measurement(2.8) |
| design / convention / arithmetic | 출처 없는 값에 붙이는 이름표: 우리 선택 / 관례 / 계산(2.8) |
| `meas-pending` | 측정을 기다리는 자리표시자 tag. 지금 library와 timeline에 0개(2.10) |
| freeze | `meas-pending`을 거부하는 lint 모드. `make lint`가 `--freeze`로 켬(9.23 D13), library의 매개변수와 timeline의 bound value 모두에(2.10) |
| `lifetime` | `segment-bound`(timeline이 끝을 정함), `finite`(EXIT에 닿으면 끝), `spawned`(부모의 FORK로 생김)(1.4) |
| `spawns` / `spawned_by` | orchestrator와 자식 항목을 잇는 field(2.2) |
| `binding_params` | timeline이 반드시 값을 넣어야 하는 손잡이 이름 목록(2.2) |
| `total_work` | batch job이 끝나려면 쓸 CPU 총량(2.2) |
| `spawn_count` / `parallelism_cap` / `child_name` | object job 수 / 동시 job 상한 / `cc1`에 붙일 이름(2.2, 6.1) |
| `lane_share` / `member_names` | game chain의 frame당 수요 배율 / chain member 이름(4.1) |
| lane | simulator가 흉내 내는 CPU 하나(2.2) |
| lane scaling / `scalable` | compile 때 수요를 lane에 맞추는 단계 / 그 단계가 바꿔도 되는 field. `game-task-chain`만 가짐(2.2, 4.1) |
| `validation_stats` | `referee`, `run`, `stats`, `scope`를 담는 검증 기록(2.7) |
| referee | 항목이 실제와 맞는지 판정할 기준 관측. 28개가 `meas-ci`, chain은 `none`(2.7) |
| scope | 측정이 정확히 무엇이었는지 적은 산문. 항목의 가장 완전한 설명(2.7) |
| `modeling_notes` | 출처 위에 우리가 지어낸 것을 적는 산문(2.7) |
| per-application archetype | application 하나의 process tree 전체를 task 하나로 측정한 항목(2.4) |
| component | 같은 role/comm으로 깨는 thread 묶음 하나. `comm`, `threads`, `wakes_per_s`, `gap`, `run`(2.4) |
| residual | 95 % 덮기 밖의 comm들을 묶은 component(2.4) |
| sporadic | 모든 repeat에서 두 번 이상 깨지 않아 싣지 않고 보고만 하는 component(3.2) |
| `focus_components` | scripted 조작 중의 thread 리듬. `input` 창 안에서 `components`를 대신함(2.4) |
| `stimulus` | 재생할 key 녹화(`dataset/stimulus/*.jsonl`)(2.4) |
| `input_run` / per-input run | key 하나에 대한 process tree 전체의 CPU(2.4) |
| window rule | key를 보낸 때부터 다음 key까지의 tree CPU에서 idle 속도만큼 뺀 값으로 per-input run을 정하는 규칙(9.5 D13)(2.4) |
| operation | 이름 붙은 무거운 작업(`send`, `page-load`, `unsharp-mask`, `preview-render`)(2.4) |
| heavy event | 드물게 나오는 무거운 run을 component에서 빼 비율로 싣는 것(2.4) |
| launch phase | application이 켜진 직후의 바쁜 구간. 파일 중간에 켜질 때 재생(2.4) |
| `period` / `cycle_run` / cycle job | 매체 주기 / 한 주기의 tree CPU / 주기마다의 TIMER job(2.4, 5.8) |
| TIMER-first | TIMER를 가진 program은 첫 명령이 TIMER여야 한다는 canonical lint(2.10) |
| batch loop | run between blocks를 뽑아 RUN, 그 뒤 block을 SLEEP, `total_work`까지 반복하는 모양(2.5) |
| run between voluntary blocks | 프로그램이 스스로 멈추기 전까지 연속으로 쓴 CPU 한 덩어리(2.5) |
| block | run 뒤 프로그램 전체가 CPU를 안 쓴 시간. 다른 thread가 이어 돌면 0(2.5) |
| spawn table | 부모가 FORK할 때마다 차례로 만드는, 미리 풀어 둔 자식 program 목록(2.6) |
| `fork_cap` | 살아 있는 자식 수 상한. `parallelism_cap` × 6(2.6) |
| object job | `.c` 하나를 `.o`로 만드는 make job. `sh`, `gcc`, `cc1`, `as`, `fixdep`, `rm` 여섯 process(2.6) |
| structural step | 자기 자식의 fork와 exit로 나뉜 구간. member는 step마다 한 번 RUN(2.6) |
| `job_order` / `trees` / `letters` / `names` | DKMS build의 job 순서(run-length) / job 종류별 process tree / 순서 문자 / comm 이름 지도(2.6) |
| chain / member | 한 frame을 이어 달리는 task 사슬 / 그 task 하나(2.6, 4.1) |
| `meas-ci` | 우리 CI 측정 출처. tag는 `meas-ci:<workflow>:<campaign>`(2.8) |
| campaign | 한 측정의 모든 repeat. 첫 batch를 띄운 날짜로 이름 붙임(3.3) |
| repeat | 새 runner에서 도는 job 하나 전체. 반복의 단위(3.3) |
| landing | job이 목표 machine에 내려앉아 완료된 것(3.3) |
| machine gate | CPU 모델이 EPYC 7763이 아니면 job을 바로 멈추는 장치(3.3) |
| phase | job 안의 측정 구간(idle, driven, driven-alt, op, play, steady, shown)(3.1) |
| settle | 측정 phase 전에 launch work가 끝나길 기다리는 시간(3.1) |
| long-phase probe | settle이나 phase 길이를 정하려고 먼저 돌리는 1,400–3,600초 측정(3.1) |
| stability rule | 실린 모든 값의 95 % 반폭이 5 % 또는 1 μs 이하, 최소 5 repeat(3.4) |
| 반폭(half-width) | 신뢰구간 폭의 절반. 평균 대비 %로 적음(3.4) |
| 예외 class | machine 따라 흩어짐, session 사이에서 변함, sparse component, run 안의 드문 사건, 녹화가 바닥남(3.5) |
| untraced control | `perf`를 켜고 끈 실행을 비교해 측정 도구 자신의 영향을 재는 검사(3.6) |
| stimulus 민감도 검사 | 다른 typing 녹화(136M Keystrokes)로 key당 CPU가 얼마나 변하는지 미리 등록한 비교(3.6) |
| fold-in | pooled 측정값을 `archetypes.yaml`에 써 넣는 작업(1.5) |
| release | campaign의 원 자료를 공개한 GitHub release(3.3) |
| venue | 측정 장소(CI runner)와 그 조건. 모든 값의 한계(3.7) |
| terminal idle state | 아무도 없어 잠기고 화면이 꺼진, 더 바뀌지 않는 session 상태(9.1) |
| cause tracing | wake의 원인을 trace에서 거슬러 올라가 desktop 바깥 원인을 걸러내는 것(9.1) |
| cron session | 자정의 runner image cron job이 phase와 겹친 구간. 싣지 않고 적음(9.1) |
| class census | 측정된 모든 항목의 실제 policy·nice를 원 자료와 probe로 읽은 조사(10.1) |
| bounding check | 같은 다운로드를 normal과 idle로 두 번 점수 매겨 실제를 위아래로 묶는 검사(7.4) |
| scale 한계 / composition seam | 다른 venue에서 온 항목들의 크기가 서로 맞춰지지 않았다는 library 수준 한계(12.1) |
| dispersion / burstiness | bin당 wake 수의 분산/평균. 실제 흐름이 compile된 흐름보다 1.9–11배 몰려 옴(12.3) |
| 민감도 변형 | RQ0 gate spec이 쓰는 변형 파일: `venue-x0.8`·`venue-x1.25`, `chain-x1.2`·`chain-x1.4`, `corner-low`·`corner-high`, `replay`(12.2–12.4) |
| SWELL-KW | 학생과 인턴 25명이 2012년 Windows 실험실에서 지식 노동 과제를 한 기록. typing 항목의 입력 녹화(2.4) |
| 136M Keystrokes | 외운 문장을 받아 적는 typing 녹화(`dhakal-chi18`). 민감도 검사에만 씀(3.6) |
| LAVD | sched_ext 기반 gaming scheduler와 그 발표(`lavd-ossna24`, 2024). game chain의 출처(4.1) |
| interbench | Con Kolivas의 interactive scheduling benchmark. 옛 항목들의 숫자 출처(5.8, 11.1) |

## 13.2 OS·scheduling 용어

| 용어 | 뜻 |
|---|---|
| scheduler | 운영체제 안에서 지금 CPU를 누구에게 줄지 정하는 부분(1.1) |
| task | scheduler가 다루는 실행 단위. Linux에서는 thread 하나(1.1) |
| runnable | CPU만 주면 바로 실행할 수 있는 상태(1.1) |
| burst / run | 깨어난 뒤 다시 멈출 때까지 CPU를 연속으로 쓰는 덩어리(1.2) |
| sleep | 상대 시간만큼 스스로 멈추는 것(1.2) |
| wake | 멈춰 있던 task가 runnable이 되는 사건. 측정에서는 wakeup 뒤의 schedule-in(1.2, 3.2) |
| schedule-in / schedule-out | task가 CPU에 올라가는 / 내려오는 순간(3.1) |
| deadline | 일을 끝내야 하는 기한. 주기 job은 다음 주기 시작(1.2) |
| period | 주기적 task가 깨어나는 간격(1.2) |
| preemption | 더 급한 task를 위해 실행 중인 task를 강제로 내려놓게 하는 것(1.2) |
| time slice | 한 task가 한 번에 쥘 수 있는 CPU 시간 상한(1.2) |
| fork / exit | 자식 process를 만듦 / 끝냄(1.2) |
| comm | Linux가 thread마다 붙이는 최대 15글자 이름(2.4) |
| scheduling class(policy) | 프로그램이 스스로 선언하는 부류. `SCHED_NORMAL`, `SCHED_IDLE`, `SCHED_BATCH`, real-time(RR 등)(1.6) |
| `SCHED_IDLE` | 다른 일이 없을 때만 돌려 달라는 class. 가중치 3(nice 0은 1,024)(1.6) |
| `SCHED_BATCH` | batch 일이라 선언하는 class. 이 library에는 실린 것 없음(10.1) |
| real-time class(RR) | 우선순위가 정해진 real-time 정책. session의 일부 thread가 가짐, 실리지 않음(10.1) |
| nice | 같은 normal class 안의 가중치 조절(−20…19). 이 dataset은 싣지 않음(1.6) |
| task group / cgroup | 커널이 CPU를 나눌 때 묶는 process 집단. idle 규칙은 같은 group 안에서만 작동(1.6) |
| slice(systemd) | systemd가 cgroup으로 만든 묶음. `app.slice`(application), `background.slice`(배경, weight 30)(1.6) |
| MLFQ | 여러 단계 queue에서 slice를 다 쓴 task의 우선순위를 내리는 정책(1.6) |
| EDF | 기한이 가장 이른 task를 먼저 돌리는 정책(1.5) |
| LOTTERY | 추첨권 수로 CPU를 나누는 정책. 가중치를 쓸 수 있는 유일한 simulator algorithm(1.6) |
| FIFO | 먼저 온 task를 먼저 끝까지 돌리는 정책(1.6) |
| executor | simulator에서 algorithm의 결정을 실행하는 부분. idle 규칙을 algorithm 아래에서 적용(1.6) |
| sched_ext | BPF로 scheduler를 바꿔 끼우는 Linux 장치. 이 연구의 대상 scheduler가 쓰는 틀(4.1) |
| voluntary block | 프로그램이 스스로 멈추는 것(I/O, 대기 등). preemption과 구별(2.5) |
| `perf sched record` | 커널의 scheduler 사건을 녹화하는 도구(3.1) |
| taskstats | process가 끝날 때 커널이 넘겨주는 CPU·대기 회계(3.1) |
| pin | process를 특정 CPU에 묶는 것(3.1) |
| vCPU | 가상 machine이 받은 가상 CPU(3.1) |
| Xvfb | 화면 없는 가상 X server(3.1) |
| vsync | 화면 refresh에 맞춰 그리는 동기화. runner에는 없음(5.1) |
| rasterize / llvmpipe | 그림을 pixel로 그리는 일 / GPU 없을 때 CPU로 그리는 Mesa의 software rasteriser(5.1, 5.7) |
| compositor | 창과 layer를 합쳐 화면을 만드는 부분(Chromium의 compositor thread, GNOME의 Mutter 등)(5.1) |
| renderer process | Chrome에서 page(site) 하나를 그리는 process(5.1) |
| site-per-process | site마다 renderer process를 따로 두는 Chrome 모델(8.1) |
| intensive wake-up throttling | 배경 tab의 timer를 유예 뒤 1분에 한 번까지 줄이는 Chrome 장치(8.1) |
| jobserver | `make -jN`의 동시 job 수를 세는 장치(6.2) |
| kbuild | Linux kernel의 build system(6장 첫머리) |
| DKMS | 새 kernel이 설치되면 kernel 밖 module을 다시 build하는 장치(1.4, 7.9) |
| THP / khugepaged | 큰 memory page를 자동으로 쓰는 기능 / 그것을 정리하는 커널 thread(6.3) |
| idle I/O class(`ionice -c3`) | 디스크에서도 다른 일이 없을 때만 돌겠다는 선언(10.3) |
| long poll | server가 새 소식이 있을 때까지 응답을 미루는 요청 방식(Matrix `/sync`)(8.2) |
| Proton / Wine / wineserver | Windows game을 Linux에서 돌리는 호환 계층 / 그 바탕 / Wine의 중계 server process(4장 첫머리, 4.1) |
| unattended upgrade | Ubuntu가 기본으로 매일 보안 업데이트를 자동 설치하는 장치(7.5) |

