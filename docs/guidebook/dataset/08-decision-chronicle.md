# 8권 · 의사결정 연대기: 2026-08-23부터 지금까지

> Status: draft · Created 2026-10-14 · Updated 2026-10-17

**이 데이터셋의 모양을 정한 결정들은 언제, 왜, 무엇을 대신해서 내려졌고, 무엇이 아직 열려 있나.**

---

이 시리즈의 다른 권들은 지금 있는 workload dataset을 설명합니다. archetype library에 들어 있는 29개 entry가 무엇이고 어떻게 쟀는지, core set의 51개 timeline이 각각 무엇을 보여 주는지, generated layer의 1,562개 파일이 어떤 규칙으로 만들어지는지, compile과 build gate가 어떻게 같은 bytes를 다시 만들어 내는지를 다룹니다. 이 권은 그 결과물 대신 과정을 다룹니다. 지금의 모양에 어떻게 도달했는지, 그 사이에 무엇을 시도했다가 버렸는지를 시간 순서로 따라갑니다.

이야기는 2026-08-23의 설계 회의에서 시작합니다. 그 회의에서 "코어는 몇 개인가", "workload란 무엇이고 label은 어디에 붙나", "workload set이 충분히 강하다는 기준은 무엇인가" 같은 질문이 처음 적혔습니다. 2026-08-26의 grill에서 그 질문들에 답이 붙었고, 2026-08-28까지 24개 파일짜리 첫 데이터셋이 만들어졌습니다. 2026-09-10에 파일이 50개로 늘었습니다. 그리고 2026-09-13에 데이터셋의 근거를 원문과 대조한 검증이 열세 개의 critical finding을 내놓았고, 데이터셋을 처음부터 다시 짓는 Phase 9가 시작되었습니다. Phase 9는 아직 진행 중입니다. 이 글을 쓰는 2026-10-14 현재, 문서와 memo를 바로잡는 9.15가 WIP이고 마지막 exit audit인 9.16이 남아 있습니다.

이 권은 이야기로 쓰지만, 이야기의 근거는 저장소의 기록입니다. 각 결정마다 날짜, 기록이 적은 이유, 그 결정이 대신한 것을 함께 적습니다. 기록에 이유가 없으면 "기록된 이유는 없습니다"라고 씁니다. 결정의 내용은 이야기에 필요한 만큼만 반복하고, 자세한 설명은 그 내용을 다루는 권으로 넘깁니다. 예를 들어 archetype 하나하나의 측정값은 archetype library를 다루는 권에서, compile 과정은 compiler와 build를 다루는 권에서 설명합니다.

마지막으로, 이 권은 "지금 무엇이 열려 있나"를 따로 한 장으로 모읍니다. 열린 자리마다 무엇이 미정인지, 어떤 선택지나 전제 조건이 있는지, 누가 정하는지를 기록에서 인용합니다. 책 끝에는 한 장짜리 연표와 용어 정리가 있습니다.

---

## 목차

1. [1장 · 이 권을 읽는 법](#1장--이-권을-읽는-법)
2. [2장 · 전사: 2026-08-23 설계 회의와 2026-08-26 grill](#2장--전사-2026-08-23-설계-회의와-2026-08-26-grill)
3. [3장 · Phase 1과 Phase 2: 기초 공사와 첫 데이터셋](#3장--phase-1과-phase-2-기초-공사와-첫-데이터셋)
4. [4장 · Phase 3: 검증과 protocol freeze, 그리고 Phase 4–6](#4장--phase-3-검증과-protocol-freeze-그리고-phase-46)
5. [5장 · Phase 7: 32개 cell을 전부 채우다](#5장--phase-7-32개-cell을-전부-채우다)
6. [6장 · 전환점: 2026-09-13의 critical findings와 Phase 9 spec](#6장--전환점-2026-09-13의-critical-findings와-phase-9-spec)
7. [7장 · Phase 9 첫 구간: 기록, 도구, 아홉 개의 research slice](#7장--phase-9-첫-구간-기록-도구-아홉-개의-research-slice)
8. [8장 · Phase 9 둘째 구간: 한 번의 rebuild와 한 번의 consumer rework](#8장--phase-9-둘째-구간-한-번의-rebuild와-한-번의-consumer-rework)
9. [9장 · 2026-10-10/11 audit과 방향 전환](#9장--2026-101011-audit과-방향-전환)
10. [10장 · Phase 9 셋째 구간: focus, build gate, build time, generated layer](#10장--phase-9-셋째-구간-focus-build-gate-build-time-generated-layer)
11. [11장 · 뒤집힌 결정과 다시 지은 것들](#11장--뒤집힌-결정과-다시-지은-것들)
12. [12장 · 지금 열려 있는 자리](#12장--지금-열려-있는-자리)
13. [13장 · 한 장짜리 연표](#13장--한-장짜리-연표)
14. [14장 · 용어 정리](#14장--용어-정리)

---

# 1장 · 이 권을 읽는 법

이 장은 "기록이 어디에 어떤 모양으로 남아 있고, 결정 번호는 어떻게 읽나"라는 질문에 답합니다. 이 질문이 먼저 필요한 이유는 간단합니다. 데이터셋의 결정은 한 문서에 모여 있지 않습니다. TODO, spec, archive, changelog, memo, audit에 흩어져 있고, slice의 changelog만 해도 합쳐서 1.5 MB가 넘습니다. 이 권이 인용하는 문장이 어느 종류의 기록에서 왔는지 알면, 그 문장의 무게도 알 수 있습니다.

## 1.1 왜 연대기가 필요한가

인지오는 데이터셋의 소유자입니다. 하지만 결정의 상당수와 코드의 대부분을 assistant에게 맡겼습니다. 그래서 "이 값은 왜 이 값인가"라는 질문에 대한 답은 대개 대화 속에서 내려졌고, 그 대화가 남긴 기록 속에만 있습니다.

웹 개발에서 비슷한 경험을 떠올려 볼 수 있습니다. 오래된 서비스의 설정 하나가 왜 그 값인지 알고 싶을 때, 우리는 `git blame`으로 commit을 찾고, commit 메시지에서 PR을 찾고, PR의 리뷰 스레드에서 이유를 찾습니다. 이 권은 그 일을 데이터셋 전체에 대해 미리 해 둔 것입니다. 다만 commit 대신 결정 기록을 따라갑니다.

연대기 형식을 고른 이유도 있습니다. 같은 주제의 결정이 여러 번 뒤집혔기 때문입니다. 예를 들어 "파일의 CPU 수요가 lane의 100–150 % 안에 있어야 한다"는 규칙은 2026-08-26에 생겨서 2026-10-09에 gate에서 물러났습니다. 지금의 규칙만 보면 왜 그 문장이 아직 여러 문서에 남아 있는지 설명할 수 없습니다. 시간 순서로 보면 설명됩니다.

## 1.2 기록의 종류

이 권에서 계속 나오는 기록의 종류를 먼저 정리합니다. 모두 이 저장소가 쓰는 말입니다.

- **phase** — 인지오의 작업 단위입니다. `_dev/TODO.md`의 인지오 section에 Phase 1부터 Phase 10까지 번호가 붙어 있습니다. 데이터셋에 직접 관계된 phase는 1, 2, 3, 7, 9입니다.
- **sub-task** — phase 안의 작업입니다. `9.13`처럼 "phase 번호.순번"으로 부릅니다.
- **`_dev/TODO.md`** — 팀 전체의 작업 목록입니다. 사람마다 section이 하나씩 있습니다. 인지오(`jioh`), 인경민(`kyungmin`, simulator 담당), 박이안(`ian`, daemon 담당). 이 권이 인용하는 TODO 줄은 모두 인지오 section의 것입니다.
- **grill** — 결정을 내리기 위한 질의응답 세션입니다. assistant가 질문을 하나씩 던지고 인지오가 답하면서 결정이 하나씩 고정됩니다.
- **spec** — grill이 끝난 뒤 그 결정만을 적은 문서입니다. phase마다 phase spec이 있고, 일부 sub-task는 task spec을 가집니다. 위치는 `_dev/docs/spec/jioh/`입니다. spec의 결정은 "Locked decisions"라는 제목 아래 번호가 붙어 있습니다.
- **archive** — 결정 세션의 기록입니다. 결정과 그 이유, 세션 안에서 확인한 사실을 적습니다. 위치는 `_dev/archive/`이고, 지금 일곱 개가 있습니다. 이 저장소의 규칙상 archive는 인지오가 요청할 때만 씁니다.
- **research slice** — Phase 9의 9.4부터 9.12까지의 sub-task를 부르는 말입니다. 영역(gaming, compile 등)마다 하나씩이고, 각자 연구하고 결정합니다.
- **changelog** — slice의 결정 기록입니다. 위치는 `_dev/research/jioh/task-<N.M>-<영역>/changelog.md`입니다. 결정마다 `## D<번호> — <제목> (<날짜>)` 형태의 heading이 붙어 있습니다. slice에는 task spec이 없는 경우가 많아서, changelog가 곧 결정의 기록입니다.
- **memo** — 팀원에게 보내는 글입니다. 위치는 `docs/memos/`입니다. 이 권은 2026-09-10, 2026-09-13(두 개), 2026-09-20, 2026-10-07, 2026-10-08의 memo를 자주 인용합니다.
- **audit** — 데이터셋을 독립적으로 점검한 기록입니다. 2026-10-10/11의 audit 기록이 `_dev/docs/audit/jioh/2026-10-10-dataset-audit-before-9.15.md`에 있습니다.

> **코드로.** 이 기록들의 위치는 모두 저장소 안입니다. `_dev/`는 개발 과정의 기록이고 `main` 브랜치에서만 편집한다는 규칙이 있습니다(저장소 `CLAUDE.md`). 공개 문서는 `docs/`에 있고, 데이터와 그 도구는 `dataset/`에 있습니다.

## 1.3 결정 번호를 읽는 법

결정은 출처에 따라 이름이 다릅니다. 이 권은 아래 형식을 씁니다.

- "2026-08-26 grill D15" — 2026-08-26 grill archive의 D15라는 결정입니다.
- "Phase 7 결정 5" — Phase 7 phase spec의 Locked decision 5번입니다.
- "9.10 D44" — 9.10 slice changelog의 `## D44` heading입니다.
- "9.14 결정 4" — 9.14 task spec의 Locked decision 4번입니다. 같은 sub-task라도 spec의 "결정 n"과 changelog의 "Dn"은 다른 번호 체계입니다.

이 시리즈의 규칙에 따라, 결정 번호는 나올 때마다 그 내용을 함께 적습니다. "9.10 D44"라고만 쓰지 않고 "9.10 D44(잘린 counterpart의 시간 배치를 비례로 유지하는 규칙)"처럼 씁니다. 처음 읽을 때는 반복처럼 느껴질 수 있습니다. 하지만 표 하나를 머리에 들고 있지 않아도 어느 문장이든 바로 읽을 수 있게 하려는 것입니다. core set의 파일 묶음 이름(C1부터 C7)도 같은 방식으로 씁니다.

## 1.4 먼저 알아야 할 용어 몇 개

연대기를 따라가려면 데이터셋의 기본 어휘 몇 개가 먼저 필요합니다. 여기서는 짧게만 소개하고, 자세한 설명은 그 주제를 다루는 권에 맡깁니다.

- **workload** — 실험 하나가 돌리는 입력 파일입니다. 정해진 시간 동안 어떤 process들이 언제 도착하고, 언제 깨어나고, 언제 떠나는지를 적은 JSON 파일(`*.workload.json`)입니다. 이 저장소에서는 "canonical workload"라고도 부릅니다.
- **timeline** — 사람이 쓰는 원본 파일입니다(`*.timeline.yaml`). 어느 구간에 어떤 프로그램이 돌고, 사용자가 어느 창에 입력하는지를 적습니다. compiler가 timeline을 workload로 바꿉니다.
- **archetype** — 프로그램 하나의 행동 방식을 담은 library entry입니다. "이 프로그램은 몇 ms마다 깨어나서 몇 ms 동안 CPU를 쓴다" 같은 값과 그 근거를 담습니다. 모두 `dataset/archetypes.yaml`에 있습니다.
- **segment** — workload 안의 한 시간 구간입니다. 구간 안에서는 정답 label이 변하지 않습니다.
- **mode** — 그 구간에서 사용자가 하고 있는 일의 이름입니다. 지금은 `idle`, `browsing`, `office`, `mail`, `dev`, `photo`, `meeting`, `media`, `gaming`, `video-edit`, `compile`, `ml-train`, `render`, `transcode`, `indexing`, `backup`의 열여섯 개입니다.
- **`background_wanted`** — 그 구간의 배경 작업이 사용자가 원한 것인지를 나타내는 true/false 속성입니다. 데이터셋이 채점하는 유일한 attribute입니다.
- **driver table** — mode와 `background_wanted`의 조합마다 scheduler 설정 하나를 적어 둔 표입니다. 16 × 2 = 32개 row가 있습니다. 데이터셋 쪽에서는 이 조합 하나를 **cell**이라고 부릅니다.
- **recognizer** — process 이름 목록을 읽고 지금의 mode와 attribute를 맞히는 쪽입니다. 연구의 주인공은 LLM recognizer입니다.
- **oracle과 random** — 비교용 recognizer 두 개입니다. oracle은 정답을 그대로 답하고, random은 무작위로 답합니다.
- **RQ0** — 연구의 첫 관문 질문입니다. "정답을 알면(oracle) 무작위(random)보다 scheduling 결과가 측정 가능하게 좋아지는가"를 묻습니다. 이 질문을 판정하는 규칙 파일이 **RQ0 gate spec**(`harness/experiments/rq0-gate.yaml`)입니다.
- **RQ1–RQ5** — 연구 제안서(`docs/research-proposal.md`)의 나머지 질문입니다. RQ1은 "process 이름과 개수만으로 LLM이 상황을 맞히는가", RQ2는 "맞히면 scheduling이 측정 가능하게 좋아지는가", RQ3는 "mode와 attribute라는 어휘로 충분한가", RQ4는 "추론 지연을 감안하면 상황이 얼마나 오래 지속되어야 이득인가", RQ5는 "driver table이라는 측정 도구 자체가 건전한가"입니다. RQ2의 비교 대상은 상황을 모르는 경우, 그리고 배포판이 기본으로 켜는 이름 catalogue를 재현한 조건(`shipped_catalogue`)과 그 catalogue의 설계 안에서 가장 강한 이름 표(`strongest_name_table`)입니다. RQ2에 답하는 것은 `shipped_catalogue`와의 비교이고, `strongest_name_table`을 이기는 것은 논문의 주장입니다(9.12 D6, D115). 처음의 `whitelist` 조건 하나가 이 둘로 나뉜 과정은 8장에서 봅니다.

이 권 전체에 걸쳐 나오는 이름 몇 개도 미리 적습니다.

- **simulator, daemon, harness** — 프로젝트의 세 프로그램입니다. simulator(인경민 담당)는 workload와 설정 변경 일정을 받아 CPU 하나에서 실행을 흉내 내고 trace(실행 중 일어난 scheduling 사건을 한 줄씩 적은 파일)를 냅니다. daemon(박이안 담당)은 recognizer를 돌려 "언제 어떤 scheduler 설정으로 바꿀지"를 정합니다. harness(인지오 담당)는 trace를 읽어 채점하고 RQ0을 판정합니다.
- **core set (coreset)** — 손으로 쓰거나 recipe로 파생한 timeline 묶음입니다. 지금 51개이고, compile 결과는 `coreset-single`이라는 이름으로 나옵니다. 파일 묶음 C1–C7은 3장과 5장에서 하나씩 소개합니다.
- **generated layer** — core set 옆에 생성기로 만드는 파일 묶음입니다. 지금 1,562개입니다. 생긴 과정은 9장과 10장에서 봅니다.
- **variant** — core set의 파일을 정해진 변환으로 바꾼 민감도 점검용 파일입니다. 지금 78개입니다.
- **campaign** — CI runner에서 같은 측정을 여러 번 반복한 한 묶음입니다. 그 raw 기록은 GitHub release로 공개합니다.
- **critical finding** — 2026-09-13의 원문 대조 검증이 찾은, 데이터셋의 근거가 틀렸거나 비었다는 지적입니다. 열세 개가 있고 6장에서 다룹니다.
- **manifest와 bless, pin** — manifest는 build 결과의 hash 목록이고, bless는 그것을 공식 판으로 정해 commit하는 일이며, pin은 다른 파일(예: RQ0 gate spec)이 그 hash에 묶이는 것입니다. 3장과 8장에서 자세히 봅니다.

그리고 OS 용어 두 개를 먼저 정리합니다.

- **core와 lane** — core는 CPU의 실행 단위 하나입니다. 이 프로젝트의 simulator는 CPU를 하나만 가진 기계를 흉내 내는데, 그 하나의 CPU를 **lane**이라고 부릅니다. "lane의 1.2배 수요"는 CPU 하나가 감당할 수 있는 양의 1.2배만큼 일이 쌓여 있다는 뜻입니다.
- **scheduler** — 여러 process가 동시에 CPU를 원할 때 누가 먼저 쓰는지를 정하는 OS의 부분입니다. 웹 서버의 worker pool이 요청을 어느 worker에게 줄지 정하는 것과 비슷한 일을 CPU 시간에 대해 합니다.

## 1.5 다섯 구간으로 본 전체

연대기 전체를 다섯 구간으로 나누면 아래와 같습니다. 날짜는 모두 기록에 적힌 날짜입니다.

```text
2026-08-23 ─ 08-26 ─ 08-28 ── 09-06 ── 09-10/11 ── 09-13 ─────────── 10-09/10 ── 10-11 ───────── 10-14
   │          │        │        │          │           │                  │           │              │
 설계 회의   grill   Phase 2  Phase 3   Phase 7    critical         9.13 rebuild   audit 결과로     9.15 WIP
 질문 Q1–Q8  D1–D22  24 파일   freeze    50 파일    findings         51 파일 bless  generated      9.16 남음
             Phase 1                              Phase 9 시작     9.14 rework    layer 추가
                                                                                  (9.17–9.22)
│◄── 구간 1: 전사 ──►│◄─ 구간 2: 첫 데이터셋 ─►│◄──── 구간 3: 넓히기 ────►│◄─ 구간 4: 다시 짓기 ─►│◄─ 구간 5: 넓히기와 마무리 ─►│
```

- **구간 1, 전사(2026-08-23 → 08-26).** 설계 회의의 질문들과 workload-generation grill의 스물두 개 결정입니다. 2장에서 다룹니다.
- **구간 2, 첫 데이터셋(2026-08-26 → 09-06).** Phase 1의 문서 작업, Phase 2의 compiler와 24개 파일, Phase 3의 검증과 contract freeze입니다. 3장과 4장에서 다룹니다.
- **구간 3, 넓히기(2026-09-09 → 09-12).** Phase 7이 32개 cell을 모두 채우면서 파일이 50개가 됩니다. Phase 8이 RQ0 gate spec을 처음 확정합니다. 5장에서 다룹니다.
- **구간 4, 다시 짓기(2026-09-13 → 10-10).** critical findings, Phase 9 spec, 아홉 개의 research slice, 한 번의 rebuild, 한 번의 consumer rework입니다. 6장, 7장, 8장에서 다룹니다.
- **구간 5, 다시 넓히기와 마무리(2026-10-10 → 지금).** audit, generated layer, focus, build gate와 build time, 이 guidebook이 찾은 결함의 처리(9.23), 그리고 아직 열려 있는 9.15와 9.16입니다. 9장, 10장, 12장에서 다룹니다.

11장은 시간 순서를 잠시 벗어나, 뒤집힌 결정만 모아 "전 → 후 → 이유 → 날짜"로 정리합니다.

# 2장 · 전사: 2026-08-23 설계 회의와 2026-08-26 grill

이 장은 "데이터셋을 만들기 전에 무엇이 이미 정해져 있었나"라는 질문에 답합니다. 이 질문이 중요한 이유는, 나중의 거의 모든 결정이 이 시기의 결정을 고치거나 다시 확인하는 모양을 하기 때문입니다. 예를 들어 Phase 9가 "native set을 버린다"고 할 때, 버리는 대상은 2026-08-26 grill이 만든 "네 개의 release artifact" 결정입니다. 시작점을 모르면 무엇이 바뀌었는지도 알 수 없습니다.

## 2.1 2026-08-23 설계 회의: 여섯 의제와 여덟 질문

2026-08-23에 팀 설계 회의가 있었습니다. 그 회의의 의제와 미해결 질문은 원래 `docs/MEETING_AGENDA.md`와 `docs/OPEN_QUESTIONS.md`라는 두 파일에 있었습니다. 2026-08-26에 두 파일을 그대로 합쳐 `_dev/archive/2026-08-23-design-meeting-open-questions.md`로 옮겼습니다. 이 archive의 머리말은 "Q1 was decided in the 2026-08-26 workload-generation grill … the remaining questions carry their leans as of archiving"이라고 적습니다. 즉 Q1만 결정되었고, 나머지는 "기울어진 방향(lean)"만 적힌 채 보존되었습니다.

의제는 여섯 개였습니다. 코어가 하나인가 여럿인가(Q1), simulator와 daemon이 동시에 살아 있는가(Q2), 실행 중에 설정이 바뀌면 무슨 일이 일어나나(Q3), driver table을 어떻게 만드나(Q4), 비교의 상한선이 두 개 필요하다는 문제(Q5), 서로 다른 workload를 어떻게 함께 채점하나(Q6)입니다. 여기에 회의 뒤에 두 질문이 더해졌습니다. workload란 무엇이고 label은 어디에 붙나(Q7), workload set이 충분히 강하다는 기준은 무엇인가(Q8)입니다.

이 여덟 질문 중 데이터셋의 모양을 직접 정한 것은 Q1, Q7, Q8입니다. 나머지는 simulator, daemon, harness 쪽의 질문입니다. Q2의 lean("daemon이 먼저 돌고 config schedule을 내보내면 simulator가 그것을 재생한다")은 2026-08-28에 정식으로 채택되는데, 이것은 3장에서 다시 나옵니다.

## 2.2 Q1 — 코어 하나인가, 여럿인가

Q1은 simulator가 CPU를 하나만 흉내 낼지, 여러 개를 흉내 낼지를 묻습니다. 회의 의제의 lean은 이랬습니다. "build single core; design workloads whose demand exceeds one core and state the core count as a deliberate choice."

archive가 보존한 이유는 측정하려는 효과의 크기입니다. 원문의 예시는 이렇습니다.

```text
  game (9ms of CPU per 16ms frame) + encoder + download

  on 1 core   they contend. the scheduler decides who loses.
  on 8 cores  everyone fits. the scheduler barely matters.
```

이 연구는 "정답을 알면 무작위보다 결과가 좋아지는가"를 재야 합니다. 그런데 core가 많으면 모든 일이 다 들어가서 scheduler가 고를 일이 없어집니다. archive의 문장으로는 "Additional cores shrink that gap by removing the need to choose. Single core is where recognition quality is most visible." 여기에 하나가 더해집니다. "EDF optimality also holds only on a single core."

- **EDF**(Earliest Deadline First)는 마감 시각이 가장 가까운 일을 먼저 돌리는 scheduling 방식입니다. 이 프로젝트의 driver table이 고를 수 있는 네 알고리즘(MLFQ, EDF, LOTTERY, FIFO) 중 하나입니다. CPU가 하나일 때 EDF는 이론적으로 가장 좋은 결과를 보장한다는 성질이 있습니다.

archive는 반론도 적어 둡니다. "A reviewer will observe that the effect depends on a one-core machine while real machines have eight or more." 선택지는 세 개였습니다. (i) 코어 하나를 연구 범위로 명시한다. (ii) 코어 하나를 쓰되, 전체 수요가 코어 하나를 분명히 넘는 workload를 만들어 "N개 코어에 3N만큼의 일이 쌓인 것과 같은 경쟁 상태"로 framing한다. (iii) N개 코어, 하나의 공유 queue, migration 비용 없음. 결정은 "build (i), frame with (ii)"였고, 2026-08-26 grill에서 확정되었습니다.

- **oversubscription**은 CPU가 감당할 수 있는 것보다 많은 일이 동시에 쌓여 있는 상태입니다. 이 상태에서만 scheduler의 선택이 결과를 바꿉니다.

이 결정은 지금까지 바뀌지 않았습니다. 다만 "(ii)"를 강제하는 장치인 demand window는 나중에 물러납니다. 그 이야기는 8장에서 합니다.

## 2.3 Q7 — workload란 무엇이고, label은 어디에 붙나

Q7은 workload schema를 검토하다 나왔습니다. archive는 문제를 이렇게 적습니다. 연구 제안서의 Family 표에 있는 각 행은 workload 파일처럼 읽히지만 실제로는 "one process set, one label, one instant"인 정지 화면이다. 그런데 workload는 수십 초 동안 돌고, 그 사이에 process가 도착하고 떠난다. "Nothing in the documents says what the ground truth is at those moments, because the documents never distinguish a workload from a snapshot."

해결은 두 개의 사건 흐름을 분리하는 것이었습니다.

```text
process-set changes   ●────●──●─────────●───●──●────●──●───●     query points

ground-truth segments ├──────────────────┼──────────────────┤    label boundaries
                            gaming              compile
```

- **query point**는 process 집합이 의미 있게 바뀌는 순간입니다. daemon은 이 순간마다 recognizer에게 다시 묻습니다.
- **segment**는 정답 label이 변하지 않는 구간입니다. segment의 경계는 query point의 부분집합입니다.

결정된 문장은 이것입니다. "A workload is an ordered list of segments, each segment a cell of the driver table, plus the process-set changes that carry it from one to the next. The path is chosen, not discovered."

> **왜 이렇게 정했나.** archive가 적은 이유는 label 작업이 끝나지 않는다는 것입니다. 두 흐름을 섞어 읽으면 "every arrival and departure demands a label"이 되고, 사람이 매 전환마다 "이 process 집합이면 지금 무슨 mode인가"를 분류해야 합니다. archive는 "For any workload with realistic churn it does not terminate"라고 씁니다. 분리하면 질문이 "이 도착이 label을 바꾸나?"라는 예/아니오 하나로 줄어듭니다. 그리고 그 답은 작성자가 timeline을 쓸 때 정합니다(`_dev/archive/2026-08-23-design-meeting-open-questions.md`, Q7 "Resolution").

Q7은 "material change"(의미 있는 변화)도 정의합니다. raw PID 단위로 보면 브라우저가 tab마다 renderer를 만들고 `make -j16`이 초당 수백 개의 compiler process를 만들고 지우므로, "변화마다 질문한다"는 말이 홍수가 됩니다. 그래서 canonical set이라는 개념을 정의했습니다. 구조적 정보(조상 관계, cgroup, 이름의 문자열 동일성)만으로 process를 접고, 이름의 의미로는 아무것도 걸러내지 않는다는 규칙입니다. archive가 비준을 요청한 문장은 이것입니다. "The canonicalization function may reference only structural metadata — process ancestry, cgroup membership, string identity — and performs no classification, filtering, or prioritization based on the meaning of any name."

- **cgroup**은 Linux가 process들을 묶어서 자원을 관리하는 단위입니다. systemd가 사용자 session의 프로그램과 system service를 서로 다른 cgroup에 둡니다.

Q7에는 edge case도 적혀 있습니다. 사용자가 타이핑을 멈춰서 interactive에서 idle로 바뀌었는데 아무 process도 시작하거나 끝나지 않으면, query point가 없으므로 그 label 변화는 "a guaranteed miss"가 됩니다. archive는 "Either forbid it by authoring rule, or admit it to Family 5 … as a stated resolution limit. It should not arrive by accident"라고 적습니다. 이 edge case는 2026-10-11에 focus가 telemetry에 들어오면서 다른 모양으로 다시 등장합니다(9장).

## 2.4 Q8 — workload set이 충분히 강하다는 기준

Q8은 Q7에서 나왔습니다. workload가 "선택된 경로"라면, 어떤 경로를 만들지 기준이 필요합니다. archive는 두 후보를 모두 기각합니다.

- **vocabulary에서 파생하기**는 순환입니다. "The vocabulary is itself under test (RQ3). A workload set generated from it makes every situation expressible by construction — the exam written from the answer key."
- **실제 세계를 흉내 내기**는 데이터 없이는 반증할 수 없습니다. "No telemetry corpus of real desktop machines exists." 게다가 실제 사용은 대부분 정상 상태여서, 충실하게 표본을 뜨면 측정하려는 효과가 희석됩니다.

채택된 기준은 **discriminative construction**입니다. "The set is constructed to force rival hypotheses apart. Each family is a probe aimed at one of them." 각 family는 경쟁 가설 하나를 죽이거나 한계 지으려고 만들어집니다. 예를 들어 "같은 process 집합, 다른 의도"를 담은 Family 2는 "행동만 보는 heuristic으로 충분했다"는 가설을, 이름을 바꾼 Family 5는 "이름을 읽는 방법은 언제나 통한다"는 가설을 겨냥합니다.

현실성은 두 층에만 들어옵니다. 이름과 command line은 진짜 소프트웨어의 것이어야 하고, 행동의 크기(16 ms frame, 수 ms의 audio 마감 등)는 그럴듯해야 합니다. 조합은 일부러 골라도 됩니다.

그리고 네 항목의 **admission checklist**가 적혔습니다. 두 번째 항목이 이후의 이야기에서 여러 번 모양을 바꿉니다.

```text
  2  each workload passes a headroom admission test: an oracle-vs-random
     gap measurable on that workload. RQ0 applied per file; Q1's
     oversubscription rule is the mechanism. A workload with no headroom
     dilutes every summary statistic
```

- **headroom**은 "좋은 설정과 나쁜 설정의 결과 차이가 날 여지"입니다. CPU가 남아돌면 어떤 설정이든 결과가 같으므로 headroom이 없습니다.

이 per-file admission test는 2026-09-10에 Phase 7의 결정 14로 RQ0 gate spec의 파일별 기준("K개 이상의 judging file에서 gap이 g 이상")이 됩니다. 그 사이에 "Q1's oversubscription rule is the mechanism"이라는 부분, 즉 demand window가 기준에서 빠집니다. 5장과 8장에서 그 과정을 봅니다.

Q8은 공개 데이터셋을 쓸 수 없는 이유도 적어 둡니다. Google Borg, Alibaba, Azure 같은 trace는 "wrong world"(datacenter batch job만 있고 사용자가 없음), "anonymised"(recognizer가 읽어야 할 이름이 해시됨), "no ground truth"(배경 작업을 원했는지는 사용자 머릿속에 있음)라는 것입니다. 그래서 이 데이터셋 자체가 "a releasable artifact"가 된다는 문장으로 Q8은 끝납니다.

## 2.5 2026-08-26 workload-generation grill: 스물두 개의 결정

2026-08-26에 grill이 열렸습니다. archive(`_dev/archive/2026-08-26-workload-generation-grill.md`)의 머리말은 "Owner of contracts + workload dataset generation: 인지오"라고 적고, 모든 결정이 확정이라고 말합니다. 결정은 다섯 묶음, D1부터 D22까지입니다. 여기서는 데이터셋의 모양에 오래 남은 것을 중심으로 봅니다.

### 2.5.1 출처와 registry (D1–D5)

데이터셋의 모든 숫자는 출처를 가져야 합니다. grill은 출처를 기록하는 방식을 정했습니다.

- **D1 — id 짓는 규칙.** entry 하나는 "one citable artifact"입니다. 예를 들어 LAVD(Valve가 Steam Deck용으로 만든 Linux scheduler)에 관한 자료는 슬라이드, 저장소, LWN 기사의 세 artifact이므로 entry도 세 개입니다. 학술 자료는 `<저자>-<학회><연도>`(예: `dhakal-chi18`), 배포된 시스템은 프로젝트 이름(예: `interbench`), 직접 잰 값은 `meas-ci`입니다.
- **D2 — `roleD`라는 이름을 없앰.** 측정값은 `meas-ci`, 아직 재지 않은 자리는 `meas-pending`이라고 부릅니다. `meas-pending`은 freeze 뒤에는 linter가 거부합니다.
- **D4 — notes를 둘로 나눔.** registry의 `notes`는 "그 출처가 무엇을 확립하는가"를, archetype 쪽의 `modeling_notes`는 "우리 encoding이 그 위에 무엇을 지어냈는가"를 적습니다. 경계 규칙은 "a source tag justifies values and described structure, never field names"입니다.
- **D5 — 인용의 주인을 바꿈.** 모든 인용 문자열은 `docs/references.md`가 갖고, yaml registry(지금의 `dataset/sources.yaml`)는 기계가 쓰는 필드만 갖습니다. 기록된 이유는 "`cite` was unlintable presentation"입니다. 그리고 "every yaml id must have a REFERENCES.md entry (subset lint, CI-checked)"라는 lint가 생겼습니다.

> **코드로.** 이 규칙은 지금도 그대로입니다. `docs/references.md`가 id 규칙을 자기 section으로 갖고, `dataset/sources.yaml`의 모든 id가 `docs/references.md`에 있는지를 dataset의 lint가 검사합니다. 저장소 `CLAUDE.md`의 "Citations" 규칙도 이 결정을 옮긴 것입니다.

### 2.5.2 측정 (D6–D8)

- **D6 — `meas-ci` 채택.** `meas-ci`는 GitHub Actions의 runner에서 직접 측정하는 방식입니다. grill은 여기에 "trust-scoping package"를 붙였습니다. CI runner의 측정은 구조와 모양에 대한 주장(fork 구조, 개수, 수명 모양, 주기, 이름 문자열)만 뒷받침하고, 기계에 따라 달라지는 절댓값(CPU %, I/O 처리량)은 "convention informed by measurement"로만 쓰며 "never desktop truth"라고 적었습니다. 그리고 "Each workflow runs N times and reports spread."
- **D7 — D-live 해체.** 실제 사용자의 데스크톱을 재야 했던 값(타이핑 간격, tab 개수)은 문헌으로 옮겼습니다. 타이핑 간격은 `dhakal-chi18`(136M Keystrokes 연구), tab 개수는 `dubroy-chi10` 등입니다.
- **D8 — meas-live 완전히 제외.** 이유는 "No teammate Linux desktops known; a standing 'validate later' conditional would leave published results provisional"입니다. 다만 수집 도구와 개인정보 제거 도구는 artifact로 함께 배포한다고 적었습니다. 이 "배포한다"는 약속은 2026-09-13 critical finding B7에서 "The privacy-scrub tool that `building-plan.md:189` says 'ships in the artifact' is not in the repository"라는 지적을 받습니다. 2026-10-16에 인지오가 그 약속을 거두었고(9.15 작업 목록 W-0734), 실제 desktop에서의 검증은 `docs/workload/measurement-overview.md` §11이 적는 한계("Real-desktop validation is deferred")로 남았습니다. 같은 날 인지오는 실제 desktop과의 비교를 열지 않고 이 범위를 논문의 한계로 싣기로 정했습니다(W-0753).

나중에 D6의 "절댓값은 convention"이라는 범위는 크게 바뀝니다. Phase 9에서 CI runner 측정이 archetype 값의 주된 근거가 되고, 대신 측정을 CPU 하나에 고정하고 한 CPU model(AMD EPYC 7763)로 묶는 규칙이 생깁니다. 7장에서 그 과정을 봅니다.

### 2.5.3 형식과 interpretation contract (D9–D14)

이 묶음은 workload 파일의 형식과, simulator가 그것을 어떻게 해석하는지를 정했습니다.

- **D9 — timeline이라는 이름과 pipeline.** 사람이 쓰는 파일은 timeline이고, `archetypes.yaml + timeline (+ scenario catalog) + seed → workload`가 pipeline입니다. 이유는 "Core timelines are hand-authored; the naturalistic generator emits timelines too — one compile path, so linter/invariants/provenance apply uniformly."
- **D10 — 수명의 두 종류.** segment에 묶인 task(사용자가 여는 앱)는 떠나는 시각(`depart`)이 고정되고, 할 일이 정해진 task(`finite`, `spawned`)는 자기 프로그램이 끝날 때 떠납니다. 기각된 대안은 "fully pinned arrive+depart trace"였고, 이유는 "open-loop, deletes the good-vs-bad config divergence RQ0 measures"입니다. 끝나는 시각까지 고정하면 좋은 설정과 나쁜 설정의 차이가 사라진다는 뜻입니다.
- **D11 — FORK는 실행 시점의 primitive로 남음.** compiler가 자식 process 목록(spawn table)을 미리 뽑아 두고, 언제 fork되는지는 실행 중에 정해집니다. 기각된 대안은 compile 시점에 자식을 다 펼치는 것이었고, 이유는 "pins cc1 arrivals, so a bad scheduler faces the same fork-storm pace as a good one"입니다.
- **D12 — 지배 원칙.** archive는 이 문장을 "write into the format spec verbatim"이라고 적습니다. "*compile time resolves all randomness; run time resolves all timing that scheduling can influence.*"
- **D13 — 절대 시각의 깨어남.** 여섯 번째 primitive `TIMER(period)`가 생겼습니다. 주기 task는 t₀ + k·period에 깨어나고, 비주기 입력(키 입력)은 미리 고정된 `{t, op: wake, target}` 사건이 됩니다. 기각된 대안은 상대적 SLEEP이었고, 이유는 "it drifts, systematically underloading the machine exactly under bad configs (biases Layer 2 toward 'bad configs aren't so bad')"입니다.
- **D14 — contract 먼저.** simulator가 아직 없으므로, D10–D13에서 쓴 interpretation contract가 simulator의 spec이 됩니다. "contract first, implementation second."

- **primitive**는 workload 안의 program이 쓰는 기본 명령입니다. RUN(CPU를 쓴다), SLEEP, TIMER, WAIT(신호를 기다린다), WAKE(다른 task를 깨운다), FORK와 EXIT의 여섯 종류입니다.
- **interpretation contract**(`docs/simulator/interpretation-contract.md`)는 simulator가 workload를 어떻게 실행해야 하는지 적은 문서입니다.

> **왜 이렇게 정했나.** D12는 이후 모든 설계의 기준이 됩니다. 무작위성을 compile 시점에 다 정해 두면, 같은 timeline과 같은 seed는 언제나 같은 bytes를 만듭니다. 그리고 scheduling이 영향을 줄 수 있는 시각만 실행 시점에 남기면, 좋은 설정과 나쁜 설정의 차이가 그 시각에 드러납니다. 웹 개발로 치면 snapshot test가 같은 입력에 같은 출력을 요구하는 것과, 성능 테스트가 실제 실행 시간을 재는 것을 한 파일 안에서 분리한 셈입니다(2026-08-26 grill D12).

### 2.5.4 Single lane과 네 개의 artifact (D15–D16)

grill은 회의가 미처 보지 못한 충돌 하나를 발견했습니다. 측정된 archetype의 수요가 여러 코어 기계에서 잰 값이라는 점입니다. archive는 "Multi-core-measured archetype demands (LAVD gaming: ~300 tasks at 65–95% of a many-core machine) cannot fit the simulator's single lane"이라고 적습니다.

**D15**는 이 충돌을 데이터셋 쪽에서 풀었습니다. "Single lane stands, ratifying OPEN_QUESTIONS Q1(i)+(ii)." 여러 lane으로 바꾸는 대안은 "Multi-lane blast radius judged too large"라는 이유로 기각되었습니다. 그 blast radius로 archive는 Q1을 뒤집는 것, EDF에 대한 Dhall 효과(CPU가 여럿일 때 EDF가 전체 사용률이 낮아도 마감을 놓칠 수 있다는 알려진 현상), executor 의미의 변경, tuning pool 재작업, trace와 metric 변경을 꼽습니다. 그리고 두 가지가 더해졌습니다.

- **demand-budget rule.** "every compiled workload's aggregate demand lands in the measurable oversubscription regime (~100–150% of the lane); the per-file RQ0 admission test (OPEN_QUESTIONS Q8) is the enforcement mechanism." 이것이 나중에 **demand window**라고 불리는 규칙입니다.
- **game-task-chain scaling defense.** LAVD의 약 300개 task를 그대로 두되 긴 꼬리는 거의 idle로 두고, 프레임에 중요한 chain만 lane에 맞게 줄인다는 것입니다. 근거는 LAVD 슬라이드의 집중도 통계("top 30–40 tasks = 95% of scheduling")입니다.

**D16**은 release artifact를 네 개로 정했습니다. "2 timeline sets × 2 compile modes: `coreset-native`, `coreset-single`, `generalset-native`, `generalset-single`." `-native`는 측정된 그대로의 수요이고, `-single`은 lane-scaling compile pass를 거친 것입니다. 실험은 `-single`에서만 돌리고, `-native`는 "unexecuted-status line"과 함께 재사용을 위해 배포한다고 적었습니다. "multi"라는 이름은 "no specific core count or machine model is defined"라는 이유로 기각되었습니다.

- **lane-scaling pass**는 여러 코어에서 잰 archetype의 CPU 사용량을 lane 하나에 맞게 비율로 줄이는 compile 단계입니다.
- **generalset**은 core set 옆에 둘 예정이던 두 번째 timeline 묶음입니다. naturalistic generator가 문헌의 분포에서 timeline을 뽑아 만든다는 계획이었습니다. 이 계획은 지금 backlog에 있습니다(12장).

> **열린 자리.** 이 두 결정은 모두 나중에 바뀝니다. demand window는 2026-10-09에 gate에서 물러나고(9.14 결정 4, 8장), native compile mode는 2026-09-16에 버리기로 정해져 2026-10-09에 compiler에서 빠집니다(9.5 follow-ups 결정 14와 9.13 D1, 7장과 8장). generalset은 아직 만들어지지 않았습니다.

### 2.5.5 나머지 정리 (D17–D22)

- **D17 — naturalistic 분포의 자세.** "'Validated against Role D' is dead." 평균과 전환 빈도는 문헌(`mark-chi08`; `zhang-chb15`가 "약 3분마다 전환"을 독립적으로 뒷받침)에서 가져오고, 분포 모양(lognormal인가 power-law인가)은 명시된 가정으로 두며 headline 숫자를 두 분포 모두로 보고한다고 정했습니다. 그리고 일반 원칙 하나를 적었습니다. "every doc sentence of the form 'Role D will validate X' must name its replacement."
- **D18 — build 순서.** (0) 출처 문서와 registry → (1) `archetypes.yaml` v0.1 → (2) interpretation contract와 JSON Schema → (3) compiler → (4) core timelines → (5) simulator → (6) RQ0 gate → (7) generator와 generalset. 이유는 "Core timelines before simulator so authoring stresses the format while fixes are cheap."
- **D19 — archetype-plan의 열린 질문 닫기.** GPU flag는 없음(simulator가 CPU만 흉내 내므로), 화상회의는 `video-playback`에 근사로 묶음, compile의 병렬 상한은 관례로 `-j8`(interbench의 `-j4`와 데스크톱의 `nproc` 관례 사이), 분포는 관례로 lognormal 등입니다.
- **D20 — 브라우저 기본값은 Chrome.** firefox는 coverage grid가 이름의 다양성을 원할 때만 씁니다.
- **D21 — 두 활동이 겹친 label.** 정말로 모호한 경우는 "a documented resolution limit — and shipped as a third C6 file ('even the oracle cannot assign a label')"입니다. 이것이 지금의 `c6-dual` 파일입니다.
- **D22 — binding note 두 개.** "wineserver → `system-daemon` is a provisional approximation"이고, P1 pair가 `tracker-miner-fs-3`를 `cpu-batch`에 묶는 것은 의도적인 선택이라는 note입니다.

- **C6**은 core set의 파일 묶음 중 "pre-committed miss", 즉 recognizer가 맞힐 수 없음을 미리 인정하고 따로 보고하는 파일들의 묶음입니다.
- **wineserver**는 Windows 게임을 Linux에서 돌리는 Wine의 중앙 조정 process입니다. **`tracker-miner-fs-3`**는 GNOME 데스크톱의 파일 색인기 Tracker의 process 이름입니다.
- **P1 pair**는 core set의 C2 묶음(의도만 다른 쌍)의 첫 번째 쌍입니다. 한쪽은 사용자가 원한 ML 학습, 다른 쪽은 원치 않은 색인기입니다.

D22의 두 note는 모두 Phase 9에서 바뀝니다. wineserver는 2026-09-13에 game chain의 member가 되고(9.4 D4), tracker는 2026-10-02/03에 자기 entry(`file-indexer`)를 얻습니다(9.10 D70).

## 2.6 같은 날의 addendum: 인용 검증

grill 당일 sub-task 1.1에서 `REFERENCES.md`를 쓰며 인용을 검증했고, archive 끝에 addendum이 붙었습니다. 두 가지가 이후 이야기에 중요합니다.

첫째는 Mark 계열 수치의 재귀속입니다. "both headline figures — ~12 min/working sphere (~10/day) AND ~3 min/task (>2 min/tool) — are **González & Mark, CHI 2004** (`gonzalez-chi04`) … **CHI 2008 contains neither figure** … The 23:15 figure exists only in the 2006 Gallup Business Journal interview (`mark-gallup06`)." 즉 그 전까지 문서들이 엉뚱한 논문에 붙여 두었던 숫자를 원래 논문으로 옮긴 것입니다. 이 `gonzalez-chi04`의 "약 11분 28초"는 2026-10-11에 `c6-dual`의 focus 교대 주기 688 s의 근거가 됩니다(10장).

둘째는 arXiv 1705.05937의 식별입니다. addendum은 이것을 O'Callahan et al., USENIX ATC '17로 확인하고 "'make forks and execs 2430 processes, mostly short-lived' confirmed verbatim (§4.3)"이라고 적었습니다. 인용 문장 자체는 정확했습니다. 하지만 그 workload가 Linux kernel build라는 저장소의 설명은 틀렸습니다. 2026-09-13 critical finding A1은 그것이 DynamoRio 6.1.0의 build였다고 밝힙니다(6장).

## 2.7 이 구간이 남긴 것과, 나중에 바뀐 것

2026-08-26까지 정해진 것 중 지금도 그대로인 것은 많습니다. single lane, D12의 지배 원칙, TIMER와 절대 시각의 깨어남, FORK와 spawn table, segment framing, discriminative construction, 출처 registry와 id 규칙, timeline이라는 작성 단위가 그렇습니다.

바뀐 것도 많습니다. 미리 정리하면 아래와 같습니다. 자세한 내용은 11장의 표에 있습니다.

| 2026-08-26의 결정 | 지금 | 바뀐 날짜와 기록 |
|---|---|---|
| demand-budget rule (lane의 ~100–150 %) | gate에서 물러남. 수요는 manifest에 기록만 함 | 2026-10-09, 9.14 결정 4 |
| 네 개의 release artifact | single-lane set 하나(`coreset-single`) | 2026-09-16 결정, 2026-10-09 적용 (9.5 follow-ups 결정 14, 9.13 D1) |
| `zhang-chb15`의 "약 3분 전환" | registry에서 빠짐 | 2026-10-01, 9.10 D1 |
| wineserver → `system-daemon` 근사 | game chain의 member | 2026-09-13, 9.4 D4 |
| tracker → `cpu-batch` | 자기 entry `file-indexer` | 2026-10-02/03, 9.10 D70 |
| meas-ci는 모양만, 절댓값은 관례 | CPU 하나에 고정한 측정의 절댓값이 archetype의 값 | 2026-09-14 → 09-16, 9.5 D3, D10과 follow-ups 결정 2–3 |
| generalset을 build order (7)에 둠 | naturalistic set은 backlog, 대신 generated layer | 2026-10-11, audit의 방향과 Phase 9 결정 9 |

# 3장 · Phase 1과 Phase 2: 기초 공사와 첫 데이터셋

이 장은 "첫 데이터셋은 어떤 결정으로 만들어졌고, 끝났을 때 어떤 모양이었나"라는 질문에 답합니다. 2026-08-26부터 2026-08-28까지 사흘 동안 문서, registry, compiler, 24개 timeline, 첫 측정 campaign, 첫 contract freeze가 모두 생겼습니다. 이 사흘의 결정 중 일부는 이유가 기록되지 않았는데, 그 사실도 이 장에서 분명히 적습니다.

## 3.1 Phase 1 — grill의 결정을 문서로 옮기기 (2026-08-26 → 08-27)

Phase 1의 spec(`_dev/docs/spec/jioh/phase-1-workload-dataset-groundwork.md`)은 목표를 한 문장으로 적습니다. "Lands every decision from the 2026-08-26 workload-generation grill into the project docs." 범위는 엄격하게 문서였습니다. "Docs and registry files only — no compiler, simulator, or archetype-content work."

spec의 Locked decisions 열세 개는 grill의 결정을 문서 단위로 다시 묶은 것입니다. registry와 references의 분리(결정 1), id 규칙(결정 2), 측정의 이름과 범위(결정 3), D-live 해체와 meas-live 제외(결정 4), notes 분리(결정 5), timeline이라는 용어(결정 6), interpretation contract(결정 7), single lane과 네 artifact(결정 8), naturalistic 분포의 자세(결정 9), build 순서(결정 10), archetype-plan의 정리(결정 11), 인용 정정(결정 12), 소유권과 팀 memo(결정 13)입니다.

TODO에 적힌 sub-task는 여덟 개였고, 모두 체크되었습니다.

- **1.1** `docs/references.md` — id 규칙 section과 검증된 entry들
- **1.2** `dataset/sources.yaml` — 기계용 registry, references의 부분집합
- **1.3** interpretation contract — 여섯 primitive, `{arrive, wake}` 사건 집합, 시각 원칙, 실행 시점 FORK, single lane, lane-scaling pass
- **1.4** `docs/workload/building-plan.md` 재작성 — build 순서, 네 artifact, demand-budget rule 등
- **1.5** `docs/workload/archetype-plan.md` 재작성 — `modeling_notes`, `meas-pending`, OQ 정리, binding note
- **1.6** 정정 — "Yun et al." → Zhang `chb15`, Mark 계열 수치를 `gonzalez-chi04`로
- **1.7** `docs/workload/` 정리 — 주제마다 규범 문서 하나
- **1.8** 팀 memo — 담당자별 영향

git 기록으로 보면 Phase 1은 2026-08-26에 spec이 들어가고 2026-08-27에 "mark phase 1 done — all 8 sub-tasks landed"로 닫혔습니다. spec의 열린 항목은 두 개였습니다. "Wineserver's place in the game-task-chain topology: decided at topology-constructor implementation time"과 "Coverage-grid fill for the ~50 core segments: build-step work". 첫째는 2026-09-13에 9.4 D4(wineserver를 game chain의 member로 넣은 결정)로 닫힙니다.

## 3.2 Phase 2 — build 순서의 1–4단계 (2026-08-27 → 08-28)

Phase 2의 spec(`_dev/docs/spec/jioh/phase-2-workload-dataset-generation.md`)은 "Builds steps 1–4 of the adopted build order … plus a closing repo-handoff sub-task"라고 시작합니다. 결정 1이 phase의 경계를 정했습니다. "Phase 2 ends at build step 4: the authored timelines and their compiled canonical coreset, checked statically (linter, provenance, invariants, demand estimate) but not executed." 즉 Phase 2는 데이터셋을 만들고 정적으로만 검사하며, 실제로 simulator에 넣어 돌리는 것은 그 뒤의 일입니다.

같은 결정 1에는 2026-08-27의 수정이 하나 있습니다. 측정 campaign을 phase 안에서 돌리기로 한 것입니다. 이유는 "its results land during Phase 2 so the coreset ships on measured numbers"입니다.

sub-task는 여섯 개였습니다.

```text
2.1 archetypes.yaml v0.1 ─┐
                          ├─► 2.3 compiler ─► 2.4 core timelines ─► 2.5 repo prep
2.2 canonical JSON Schema ┘                         ▲
2.6 meas-ci campaign (parallel) ─── fold-in ────────┘ (2.4의 마지막 compile 전에)
```

나머지 결정 몇 개도 이후에 오래 남았습니다. 결정 3은 timeline 형식의 소유를 나눴습니다. "The base timeline format (what the compiler parses) is fixed in 2.3's own spec session; the authoring sugar … is fixed in 2.4's." 결정 4는 linter와 invariant test를 2.3의 결과물로 GitHub Actions에 연결하라고 했습니다. 결정 5는 compiler가 파일별 정적 수요 추정치를 내고, 2.4의 파일이 lane의 ~100–150 % 창 안에 들어가야 한다고 했습니다. 다만 "The RQ0 admission test remains the real enforcement of the demand budget; files may still be redesigned at the gate"라는 단서가 붙었습니다.

## 3.3 2.3 — timeline compiler와 형식 (2026-08-27)

2.3의 task spec(`_dev/docs/spec/jioh/task-2.3-timeline-compiler.md`)은 timeline 형식과 compiler의 계약을 정했습니다. 일곱 결정이 있습니다.

1. **세 개의 독립 track.** timeline은 `meta:`와 `segments:`(정답이 될 시간 구간), `tasks:`(process들), `focus:`(사용자의 입력 주의 track)로 이루어집니다. 이유는 "The split mirrors the canonical `ground_truth`/`events` separation."
2. **task entry.** 안정적인 `id`, `name`, `archetype`, `arrive`, segment에 묶인 경우에만 `depart`, archetype이 선언한 key만 허용하는 `bind:`, 같은 task를 여럿 만드는 `count:`. 그 밖의 숫자를 쓰면 "the inline-numerics lint violation"입니다.
3. **focus track.** `focus:`는 겹치지 않는 `{from, to, task}` 창들의 목록이고, compiler는 그 창 안에서 focus를 받은 task의 입력 간격 분포로 키 입력 사건을 뽑습니다.
4. **segment의 scenario 주석.** compiler는 무시하고 linter만 읽습니다.
5. **seed와 keyed substream.** seed는 timeline의 `meta:`에 있고, 무작위 추출은 `(seed, task id, param, draw index)`에서 파생한 독립 흐름을 씁니다. 이유는 "so unrelated edits cannot shift another task's draws and C2 byte-identity holds by construction."
6. **lockfile 패턴.** `dataset/build/`는 git에 넣지 않고, 결과물의 hash를 적은 manifest를 commit하며, CI가 다시 compile해서 확인합니다.
7. **demand window 강제.** "The linter hard-fails a compiled `-single` file whose static demand estimate falls outside ~100–150% of the lane, unless the timeline's `meta:` declares the calibration demand class."

- **manifest**(`dataset/build.manifest.json`)는 build 결과물 각각의 SHA-256 hash와 입력을 적은 파일입니다. JavaScript 프로젝트의 lockfile처럼, 결과물 자체 대신 "무엇이 나와야 하는가"를 commit합니다.
- **demand class**는 파일이 수요 창의 검사를 받는지를 정하는 timeline의 표시입니다. `calibration`은 면제, `oversubscribed`는 검사 대상입니다.

spec에는 test suite의 "charter"도 있습니다. "Same timeline + same library commit + same seed ⇒ byte-identical canonical output. A one-entry diff between two timelines changes only that entry's compiled events. `-native` and `-single` variants of one timeline differ only in declared-scalable fields."

이 일곱 결정이 지금 어떻게 되었는지 미리 봅니다. 결정 1의 세 track은 2026-10-11에 네 track이 됩니다. 키 입력 창의 track 이름이 `focus`에서 `input`으로 바뀌고, `focus`라는 이름은 창 focus를 뜻하는 새 track이 가져갑니다(9.17 D1, 10장). 결정 5의 keyed substream과 결정 6의 lockfile 패턴은 그대로입니다. 결정 7의 hard-fail은 2026-10-09에 사라집니다(9.14 결정 4, 8장).

2.3의 형식을 정한 grill의 이유는 그때 archive로 남지 않았습니다. 2026-08-28 archive가 "task-2.3 format grill"을 "Still owed … not reconstructible here" 목록에 넣었습니다(3.7절). 2026-10-16에 인지오가 기억하는 대로 적은 archive(`_dev/archive/2026-08-27-phase-2-grills-rationales.md`, 9.15 작업 목록 W-0741)가 생겨, 2.3에 대해서는 결정 6(lockfile pattern)의 이유를 되살렸습니다. 결정 1, 2, 5는 결정의 문장이나 다른 기록이 이유를 적고, 결정 3(focus track)과 결정 7(demand window)은 나중의 결정이 대체했습니다(3.7절).

## 3.4 2.4 — core timelines (2026-08-28)

2.4의 task spec(`_dev/docs/spec/jioh/task-2.4-core-timelines.md`)은 파일 목록 자체는 다시 정하지 않는다고 적습니다. "The file inventory itself (C1×6, C2 3 pairs, C3×3, C4×3, C5×3, C6×3) is normative in docs/workload/building-plan.md §3 and is not re-decided here." 그때 core set의 묶음은 여섯 개였습니다.

- **C1** — 상황 하나만 담은 단일 segment 파일. 그때는 `browsing`, `compile`, `gaming`, `idle`, `media`, `office`의 여섯 개였습니다.
- **C2** — 의도만 다른 쌍. 두 파일이 한 segment에서만 다르고, 그 segment의 `background_wanted`가 다릅니다. P1, P2, P3의 세 쌍입니다.
- **C3** — 여러 mode를 이어 붙인 하루의 흐름(arc). `c3-workday`, `c3-creation`, `c3-evening`입니다.
- **C4** — label을 바꾸지 않는 방해 요소(distractor)를 끼워 넣은 파일.
- **C5** — 이름의 친숙도(familiarity tier)를 바꾼 파일. 당시 `c5-t3`, `c5-t4`, `c5-t5`.
- **C6** — 맞힐 수 없음을 미리 인정한 파일(pre-committed miss). 당시 `c6-dual`, `c6-fold`, `c6-spoof`.

- **familiarity tier**는 process 이름이 얼마나 알아보기 쉬운지를 1부터 5까지로 나눈 등급입니다. tier 1은 누구나 아는 이름(예: `chrome`), tier 5는 의미 없는 문자열입니다.
- **pre-committed miss**는 "어떤 관찰자도 이름과 행동만으로는 맞힐 수 없다"고 미리 선언하고 정확도 채점에서 빼는 segment입니다.

2.4의 다섯 결정은 이렇습니다.

1. **파생은 선언형 variant spec과 범용 deriver로.** 새로 설계한 timeline은 그대로 쓰고, 파생 파일은 `from: <base>`와 닫힌 op 집합(replace-task, add-task, rename, set-meta 등)으로 된 작은 yaml입니다. 이유는 "The C2/C4/C5 disciplines are structural: a derived file provably differs from its base by exactly its ops."
2. **coverage grid는 주석에서 자동 생성.** segment에 `familiarity:` 주석이 붙고, grid(domain × familiarity, segment 단위)가 기계적으로 만들어집니다. "Hole sign-off stays human."
3. **길이와 demand class의 관례.** 기본 segment 120 s, C1 파일 60 s. C1은 `calibration`, C2–C6은 기본 `oversubscribed`.
4. **seed 정책.** 새 timeline마다 고유한 seed, variant는 base의 seed를 물려받고 몰래 바꾸지 않습니다.
5. **이름 문자열.** scenario catalog대로 묶고, meas-ci의 이름 확인 결과(`soffice.bin`, 살아 있는 `cc1`, 그냥 `updatedb`)를 기록합니다.

- **coverage grid**(`dataset/coverage-grid.json`)는 core set의 segment가 어떤 칸을 얼마나 채우는지를 세는 표입니다. 논문의 dataset-design 표가 될 예정이었습니다.
- **deriver**는 variant spec(recipe)을 읽어 base timeline에서 파생 timeline을 만드는 도구입니다.

결과는 TODO의 2.4 줄에 적혀 있습니다. "13 novel + 11 derived, all windows green on cli:3 numbers; grid signed off 2026-08-28 (tier concentration by design; grid counts spawn-child names)." 24개 파일이 두 compile mode로 compile되어 artifact가 48개였습니다.

이 결정 중 결정 2는 2026-09-10에 대체되었습니다. spec 안에 그 표시가 있습니다. "*Superseded 2026-09-10 (Phase 7 decision 11): the grid counts the driver-table cell, mode × `background_wanted`, against the tier columns, and an empty cell fails CI — the human sign-off had missed the attribute's `false` side.*" 사람이 서명한 grid가 attribute의 `false` 쪽 구멍을 보지 못했다는 것입니다. 5장에서 이 이야기를 이어 갑니다.

## 3.5 2.6 — 첫 meas-ci campaign (2026-08-28)

2.6의 task spec(`_dev/docs/spec/jioh/task-2.6-meas-ci.md`)은 측정 도구와 workflow를 정했습니다.

1. **두 개의 sidecar 도구.** netlink로 process의 fork/exec/exit를 정확히 기록하는 tracer와, 1초마다 `/proc`의 상태를 읽는 sampler입니다.
2. **데이터는 artifact로만.** "CI never writes to the repo." 측정값을 archetype에 넣는 fold-in은 사람이 하는 commit입니다.
3. **N=5 matrix, 손으로만 실행.** workflow 하나를 다섯 번 반복하고, run id 하나가 인용 가능한 batch 하나입니다(`meas-ci:<workflow>:<run>`). 3a(2026-08-28 수정)는 "At most one cited batch per workflow at any time"이라는 대체 규칙을 더합니다.
4. **CLI workflow.** Linux kernel의 `defconfig` build를 `make -j8`로 돌리고, 그 kernel 소스 tree를 `tar`/`xz`, `rsync`, `updatedb`, `clamscan`의 공통 corpus로 씁니다. 조용한 구간을 잡아 `system-daemon`의 기준선으로 씁니다.
5. **Xvfb workflow.** Chromium과, `electron-comms`의 공개 대체물로 Element Desktop을 씁니다.
6. **이름 확인.** Ubuntu, Fedora, Arch container에서 실제 process 이름(`comm`)을 확인합니다.

- **fold-in**은 측정 campaign의 결과를 `dataset/archetypes.yaml`의 값으로 옮기는 commit입니다.
- **Xvfb**는 화면 없이 그래픽 프로그램을 돌리는 가상 X 서버입니다. CI runner에는 모니터가 없으므로 GUI 프로그램은 이 위에서 돌립니다.
- **`comm`**은 Linux kernel이 process마다 붙여 두는 짧은 이름입니다(최대 15글자). `ps`나 `top`이 보여 주는 이름이 이것입니다.

결과는 TODO의 2.6 줄에 있습니다. "batches cli:1/gui:2/names:1; 11/15 folded, 4 stay pending with stated findings (cache-hot corpus, foreground no-throttle); raw data: release `meas-ci-2026-08-28`." 열다섯 개의 `meas-pending` 자리 중 열한 개가 측정값으로 채워졌습니다.

> **열린 자리.** TODO의 2.4 줄은 "all windows green on cli:3 numbers"라고 적고, 2.6 줄은 "batches cli:1/gui:2/names:1"이라고 적습니다. 두 줄이 다른 CLI batch 번호를 말합니다. 2026-09-13의 9.3 spec 결정 1은 release의 notes를 고치면서 "the summary comes from cli:3, not cli:1; … cli:1 is cited by `system-daemon`"이라고 적었습니다. 즉 대부분의 값은 cli:3에서, `system-daemon`만 cli:1에서 왔다는 것이 9.3의 정리입니다. 2.6 batch를 대체하는 과정("batch-tag supersession")의 이유는 archive로 남지 않았습니다(3.7절).

## 3.6 2.5 — 저장소 준비와 첫 contract freeze (2026-08-28)

2.5는 원래 "repo prep + onboarding docs"였지만, archive(`_dev/archive/2026-08-28-task-2.5-repo-prep-and-contracts.md`)의 머리말대로 "grew into the first protocol-freeze round"가 되었습니다. 데이터셋의 모양에 영향을 준 결정이 여기에 많습니다.

**구조.** component마다 최상위 tree 하나(`dataset/`, `simulator/`, `daemon/`, `harness/`)와 tree마다 Makefile 하나. 이유는 "trees match ownership so cross-tree needs go through contracts."

**아키텍처의 정정.** 네 가지가 지금까지 그대로입니다.

- "The simulator and daemon never talk at run time." daemon이 recognition 전체를 먼저 돌려 **config schedule**을 내보내고, simulator는 (workload 사건, config schedule) → trace라는 순수 함수입니다. 이유는 "each side buildable/testable alone; conditions stay comparable because the simulator is condition-agnostic."
- "Query points are pinned events only (arrivals + scripted user-closes)." 이유는 "keeps telemetry scheduler-independent by construction"이고, 대안(두 번 simulation해서 끝나는 시각을 알아내기)은 "buys realism at real complexity cost"라고 기각되었습니다. 받아들인 결과로 "finite tasks never vanish from telemetry"를 적었습니다.
- "Spawn-table children are telemetry-visible." 확인한 사실로 "C1-compile's recognition scenario is `{code, make, cc1×N}`"를 들었습니다. 자식이 안 보이면 compile 시나리오가 무너진다는 것입니다.
- "Names+counts aggregation: telemetry carries `{name, count}`." 확인한 사실로 "compiled `c1-browsing` = 13 tasks named `chrome` … `c1-gaming` = 300 × `game.exe`"를 들었습니다.

- **telemetry**는 daemon이 recognizer에게 보여 주는 입력입니다. 그때는 "지금 돌고 있는 process 이름과 그 개수의 목록"이었습니다. 2026-10-11에 "지금 focus를 가진 process"가 더해집니다.
- **config schedule**은 daemon이 "몇 초에 어떤 scheduler 설정으로 바꾼다"를 적어 simulator에게 넘기는 파일입니다.

그리고 하나가 더 있습니다. "LLM inference never occupies the simulated lane … recognition cost is modeled as latency only." 이유는 "If inference consumed simulated CPU, LLM conditions would face different workloads than the oracle — destroying the controlled comparison."

**recognition vocabulary 비준.** 데이터셋의 모양을 직접 정한 결정입니다.

- "Modes = the dataset's 16 ground-truth labels (fine, source-backed), not the proposal's draft 5." 이유는 "labels are already frozen into 24 workloads + signed-off grid; fine→coarse grading mappings would inject judgment exactly where measurement must be clean."
- `ambiguous`는 정답 쪽에만 있습니다. recognizer의 선택지에 있으면 "an escape hatch rewarding calibrated cowardice"가 되기 때문입니다.
- "One graded attribute: `background_wanted` (renamed from `wanted`)." 이름을 바꾼 이유는 "bare `wanted` is ambiguous without context"입니다. 배경 작업이 없는 segment는 vacuous-true로 둡니다. 이 이름 변경은 같은 세션에서 데이터셋 전체에 적용되고 다시 compile되었습니다.
- 실시간 encoder 여부를 뜻하는 attribute(`has_realtime_encoder`)는 채택하지 않았습니다. 이유는 "the attribute has no dataset support today, adding it would mean manufacturing derived files for an undemonstrated dimension, and it doubles the oracle's attribute space."

**freeze.** `cpu_scheduler` config schema와 trace 형식이 frozen되었습니다. trace 쪽의 핵심 결정은 "`ready` is its own event"였습니다. 이유는 "per-stimulus latency = `run_start − ready`, and readiness is emergent … the harness must never re-implement simulator semantics to reconstruct it."

- **frozen**은 이 저장소에서 "형식이 고정되었고 바꾸려면 세 사람의 결정이 필요하다"는 뜻의 상태입니다.

## 3.7 기록되지 않은 이유들

2026-08-28 archive는 마지막에 이렇게 적습니다.

> "Still owed (older sessions, not reconstructible here): Archive docs for the 2026-08-27 sessions (phase-2 grill Q1–Q7; task-2.3 format grill) and pre-2.5 2026-08-28 sessions (2.6 grill; 2.4 grill; batch-tag supersession; grid sign-off) — their rationale lives only in those conversations and was not recoverable from this session."

이 문장이 말하는 바를 분명히 적어 둡니다. Phase 2의 grill(Q1–Q7), 2.3의 형식 grill, 2.6의 grill, 2.4의 grill, 측정 batch를 대체한 결정, grid 서명의 이유는 그 대화 속에만 있었고 저장소에 남지 않았습니다. 결정 자체는 spec(Phase 2, 2.3, 2.4, 2.6의 spec 파일)과 TODO 줄에 남았습니다. 하지만 spec에 적힌 한 줄짜리 이유를 넘는 논거, 예를 들어 "왜 C1 파일은 60 s이고 기본 segment는 120 s인가"(2.4 결정 3)나 "왜 N=5인가"(2.6 결정 3)에 대한 논거는 없습니다.

그리고 이 공백 중 하나는 실제로 나중에 문제가 되었습니다. 2026-09-18에 9.6 D10(같은 기계 반복과 안정성 기준으로 반복 횟수를 정한 결정)은 "the task 2.6 spec §3 states 'N=5 matrix' without a ground"라고 적고, 다섯 번이라는 횟수를 버리고 안정성 기준으로 반복 횟수를 정하기로 합니다(7장). 이유가 기록되지 않은 결정은, 다시 볼 때 지킬 근거도 없다는 것을 보여 주는 예입니다.

2026-10-16에 이 공백의 일부가 메워졌습니다. 인지오가 그 session들의 이유를 아는 대로 적은 archive를 남기기로 했고(9.15 작업 목록 W-0741), `_dev/archive/2026-08-27-phase-2-grills-rationales.md`가 그 기록입니다. session의 대화 기록은 남아 있지 않으므로 인지오가 기억하는 것에서 썼습니다. 되살린 이유는 셋입니다. 2.4 결정 4(파생 파일은 seed를 바꿀 수 없음)는 "a rule is enforced by refusal, not by a warning"이고, deriver는 첫 커밋 `63c677dc`부터 거부합니다. 2.4 결정 3의 길이(C1 60 s, 기본 segment 120 s)는 어떤 출처도 그 길이를 말하지 않으므로 고른 값, 곧 design입니다. 2.3 결정 6의 lockfile pattern은 build가 입력에서 바이트 단위로 다시 만들어지는 파생물이라는 것입니다. 나머지는 결정의 문장이나 다른 기록이 이유를 적고 있거나(2.3 결정 1, 2, 5, 2.4 결정 1, 2.6 결정 2), 나중의 결정이 대체했거나(예: 2.6의 N = 5는 Phase 9의 안정성 기준), 단계를 조직한 결정입니다.

## 3.8 Phase 2가 끝났을 때의 데이터셋

2026-08-28 저녁의 데이터셋을 한 번에 그려 보면 이렇습니다.

```text
dataset/archetypes.yaml v0.1 — 12 entries
  desktop-interactive  audio-playback  video-playback  game-task-chain
  build-orchestrator   compiler-child  cpu-batch       background-crawler
  io-stream            network-bulk    electron-comms  system-daemon
  (값의 출처: 문헌 + meas-ci cli/gui/names batch, 4개 자리는 meas-pending)

dataset/timelines — 24 files (13 novel + 11 derived)
  C1 ×6   C2 ×3 pairs   C3 ×3   C4 ×3   C5 ×3   C6 ×3

build — 24 × {coreset-single, coreset-native} = 48 artifacts
coverage grid — mode × familiarity, 2026-08-28 서명
```

이 그림에서 지금까지 살아남은 archetype은 `game-task-chain`, `build-orchestrator`, `compiler-child`, `cpu-batch`의 넷뿐입니다. 그나마 앞의 셋은 값과 구조가 모두 다시 정해졌습니다. 나머지 여덟 개가 어떻게 사라지고 대체되었는지가 7장의 이야기입니다.

몇 가지 compile된 모습도 이후 이야기에 나옵니다. `c1-gaming`은 `game.exe`라는 이름의 task 300개를 가졌고, `c1-browsing`은 `chrome` task 13개를 가졌습니다(2026-08-28 archive). 그리고 `c1-compile`은 `make` 아래 `cc1` 자식 100개를 가졌습니다(2026-09-13 critical finding A1이 "`c1-compile` 100, `c6-dual` 85, `c3-workday` 4,200"이라고 적습니다).

# 4장 · Phase 3: 검증과 protocol freeze, 그리고 Phase 4–6

이 장은 "첫 데이터셋을 실험에 쓰기 전에 무엇을 확인하고 무엇을 굳혔나"라는 질문에 답합니다. Phase 3는 2026-09-06 하루에 끝났습니다. 그 하루 동안 파일별 CPU 수요를 처음 읽었고, RQ0의 판정 파일을 처음 정했고, 다섯 개의 data contract를 frozen으로 바꿨습니다. Phase 4부터 6은 데이터셋이 아니라 driver table과 harness의 phase이지만, 데이터셋에 몇 군데 흔적을 남겼고 그중 하나가 Phase 7을 불렀습니다.

## 4.1 Phase 3의 자리

Phase 3의 spec(`_dev/docs/spec/jioh/phase-3-verification-and-protocol-freeze.md`)은 자신을 "Stage 0 of `_dev/docs/rq0-preparation-notes.md`"라고 소개합니다. RQ0 준비 노트의 Stage 0부터 Stage 6까지가 Phase 3부터 Phase 8이 되었습니다(2026-09-06 archive의 "Phase split").

범위는 넷이었습니다. C1의 demand class 문제를 파일별 수요 추정치로 정리하고 그 추정치를 build artifact로 만들기, `c6-dual`의 vocabulary 밖 label을 점검하기, driver table 형식에 의존하지 않는 contract를 굳히기, vocabulary와 status를 정리하기입니다. 2026-09-06 archive는 네 sub-task가 모두 그날 끝났고 "Executed directly on `main` without worktree or plan at the user's direction"이었다고 적습니다.

## 4.2 3.1 — 수요 추정치를 manifest에 넣고, 판정 파일을 정하다

Phase 3 결정 6은 "The compiler writes each file's `utilization` and `demand_class` into `dataset/build.manifest.json`"입니다. archive가 적은 이유는 "so the paper can cite a committed value"이고, 세션에서 확인한 사실은 "the compiler computed utilization and demand class but printed them to stdout only; the manifest carried hashes alone"이었습니다.

- **utilization**(manifest의 `demand`)은 파일 전체에서 task들이 원하는 CPU 시간의 합을 파일 길이로 나눈 값입니다. 1.0이면 lane 하나를 꽉 채운다는 뜻입니다.

그날 처음 읽은 `-single` 값은 아래와 같습니다(archive의 표에서 옮김).

| 파일 | utilization | class |
|---|---|---|
| `c1-browsing` | 0.45 | calibration |
| `c1-compile` | 0.54 | calibration |
| `c1-gaming` | 1.46 | calibration |
| `c1-idle` | 0.00 | calibration |
| `c1-media` | 0.45 | calibration |
| `c1-office` | 0.50 | calibration |
| `c2-p1a` / `p1b` | 1.20 | oversubscribed |
| `c2-p2a` / `p2b` | 1.29 | oversubscribed |
| `c2-p3a` / `p3b` | 1.12 | oversubscribed |
| `c3-creation` / `workday` | 1.04 | oversubscribed |
| `c3-evening` | 1.11 | oversubscribed |
| `c6-dual` | 1.28 | oversubscribed |

여기서 첫 판정 파일이 정해졌습니다. archive의 문장은 "**The RQ0 judging set is C2's 6 files, not 12**; all six sit inside the demand window; C1 stays reporting-only."입니다.

- **judging set**은 RQ0 gate의 판정에 쓰이는 파일들입니다. 나머지 파일은 결과를 보고만 하는 reporting-only 파일입니다.

이때 archive는 중요한 관찰 하나를 남겼습니다. RQ0 준비 노트는 "calibration 파일은 경쟁이 적으니 random과 oracle의 차이도 작을 것"이라고 추론했는데, archive는 이것이 그대로는 맞지 않다고 적습니다. "Demand bounds throughput headroom, not latency headroom: at 0.8 utilisation two tasks still become runnable at the same instant, and a keystroke arriving while a batch task holds the lane still waits a slice." 그래서 C1을 판정에서 빼는 이유는 headroom이 없어서가 아니라 "its designed role is the baseline where the whitelist scores perfectly"라는 것이었습니다.

- **time slice**는 scheduler가 task 하나에게 한 번에 CPU를 쓰게 해 주는 시간의 단위입니다. slice가 끝나기 전에는 다른 task가 기다려야 할 수 있습니다.
- **whitelist**는 프로그램 이름마다 scheduling 규칙을 미리 적어 둔 표로 상황을 정하는 비교 조건입니다. 2026-10-09에 두 조건(`shipped_catalogue`, `strongest_name_table`)으로 나뉩니다(8장).

이 "수요는 처리량의 여지를 묶을 뿐, 지연의 여지를 묶지 않는다"는 관찰은 한 달 넘게 지나서 두 번 다시 쓰입니다. 2026-09-10에 Phase 7의 judging set 결정이 "demand is not a criterion"이라고 할 때, 그리고 2026-10-09에 9.14가 demand window를 gate에서 내릴 때입니다.

`c1-gaming`에 대해서도 결정이 있었습니다. 1.46으로 core set에서 가장 수요가 높고, 단일 상황 파일 중 유일하게 창 안에 있었습니다. archive는 이것을 "an accidental natural experiment (decided)"라고 부르고, judging set에는 넣지 않되 "a pre-registered **separate reporting line**"을 두기로 했습니다. 빼는 이유 둘 중 "the second mattering more"라고 적은 것은 "selecting the highest-demand file after reading demand numbers is selection along an axis correlated with expected gap size"입니다. 수요를 본 뒤 가장 수요가 큰 파일을 고르는 것은 결과를 미리 보고 고르는 것과 비슷하다는 뜻입니다.

마지막으로, 해결되지 않은 항목이 하나 남았습니다. 파생 파일들(`c4-*`, `c5-*`, `c6-fold`, `c6-spoof`)은 base의 `meta`를 deriver가 통째로 복사한 덕분에 `calibration`을 물려받고 있었습니다. 2.4 결정 3은 예외를 "a visible authored declaration"으로 요구했는데, 그것이 작성된 선언이 아니라 상속이었던 것입니다. archive는 이것을 "Unresolved"로 적었고, 2026-09-09에 Phase 7 결정 7(모든 파생 파일이 `calibration`을 `patch-meta`로 직접 선언)이 닫습니다.

## 4.3 3.2 — `c6-dual`은 oracle에게도 풀 수 없다

`c6-dual`은 2026-08-26 grill D21(정말 모호한 두 활동의 겹침을 C6의 세 번째 파일로 낸다는 결정)이 만든 파일입니다. 240 s짜리 segment 하나에 `mode: ambiguous`, `dual_active: true`가 붙어 있고, 게임과 editor와 build가 함께 돕니다. 3.2는 oracle과 validator가 이 파일을 어떻게 처리하는지 문서대로 따라가 봤습니다.

결론은 "the file runs on **`fallback`** for its whole length under the oracle condition"이었습니다. oracle이 답할 정답이 선택지(16개 mode)에 없으므로 validator가 그 답을 거부하고, 쓸 만한 답이 한 번도 오지 않으니 끝까지 기본 설정으로 돈다는 것입니다. 그 결과 "On `c6-dual`, oracle ≡ `fixed`; `random` draws legal answers and can beat the oracle."

- **fixed**는 처음부터 끝까지 기본 설정(boot default) 하나만 쓰는 비교 조건입니다.

인지오의 검토로 여섯 가지가 정리되었습니다. 그중 데이터셋에 남은 것은 셋입니다. 첫째, oracle은 어떤 core set 파일에서도 정상 종료하고 유효한 schedule을 내야 한다는 "no-crash contract"입니다. 둘째, `background_wanted` lint입니다. "every segment carries a boolean `background_wanted`; on `mode: ambiguous` it must be absent." 그리고 이 lint를 적용하자 "**The coreset did not already pass**: `c1-idle` carried `attributes: {}`"가 드러났습니다. `c1-idle`을 `background_wanted: true`로 고쳤고, 정답과 두 artifact의 hash가 바뀌었습니다. 셋째, `c6-dual`을 "random이 oracle을 이기면 이상하다"는 guard에서 면제하는 `guard_exemptions`입니다.

## 4.4 3.3 — 다섯 contract가 frozen되다

Phase 3 결정 3과 4로 run file, visible projection, telemetry, config schedule, recognition log의 다섯 contract가 "frozen by ratified decision"이 되었습니다. 이를 위해 "frozen"의 정의를 고쳤습니다. 이전 정의는 code와 CI의 강제를 요구했는데, 소비자가 아직 없는 contract는 그 조건을 만족할 수 없었기 때문입니다. 새 정의는 "the format is fixed and changing it is a team decision; schema and CI enforcement follow when the consumer lands"입니다.

- **run file**은 workload에서 정답을 빼고 simulator에게 주는 파일입니다. 3.3은 이것을 형식이 아니라 추출 규칙("drop `ground_truth`, reduce `meta` to `workload_id`")으로 굳혔습니다. 확인한 사실로 "today's `c1-idle` ground-truth fix left its run file byte-identical — a label correction must not change what the simulator runs"를 들었습니다.
- **visible projection**은 daemon이 볼 수 있는 workload의 부분입니다. "one entry per canonical task instance, never folded"로 굳었습니다.

데이터셋의 모양에 가장 큰 영향을 준 것은 telemetry의 다섯 snapshot 규칙입니다. 첫 규칙은 "The set is the name→count multiset, so count-only changes emit a snapshot"입니다. 이 규칙의 근거가 데이터셋에서 나왔습니다. "under a names-only rule `c6-spoof` would have 1 query point instead of 3 — its spoofing `chrome` arriving among 13 existing ones would never be seen, turning the file into a second `c6-fold`." 이름만 보면 이미 `chrome` 13개가 있는 곳에 가짜 `chrome` 하나가 더 와도 아무 변화가 없으므로, 개수까지 봐야 한다는 것입니다.

- **multiset**은 같은 원소가 여러 번 들어갈 수 있는 집합입니다. 여기서는 "이름 → 개수"의 목록입니다.

이 규칙 목록에는 2026-10-11에 여섯 번째 규칙이 더해집니다. focus를 가진 process가 바뀌는 것도 집합의 변화라는 규칙입니다(9.17, 10장).

## 4.5 3.4 — vocabulary와 status 정리

3.4는 문서들을 vocabulary freeze와 contract freeze에 맞췄습니다. 데이터셋 쪽에서 눈여겨볼 것은 연구 제안서의 Part 5 표 정정입니다. ML 학습 행이 `compile`이라고 적혀 있었는데, 그 행이 가리키는 파일 `c2-p1a`의 label이 `ml-train`이어서 데이터셋에 맞게 고쳤습니다. 문서가 데이터셋을 따라가야 한다는 원칙이 이때도 적용되었습니다. 이 원칙은 9.15의 spec에서 "the code and data as they stand … the current docs, never an authority"라는 우선순위로 명문화됩니다(12장).

## 4.6 Phase 4–6이 데이터셋에 남긴 흔적

Phase 4(driver table 형식, 2026-09-07), Phase 5(primitive metric과 records, 2026-09-07/08), Phase 6(driver table v0과 scoring spec, 2026-09-08/09)은 harness와 daemon의 phase입니다. 데이터셋에 닿은 곳은 아래와 같습니다.

**Phase 5 — `familiarity`가 compile을 통과하게 되다.** 2026-09-07 archive(`_dev/archive/2026-09-07-phase-5-primitive-metrics.md`)는 문제를 "the compiler dropped the annotation, so compiled `ground_truth` had no split key"라고 적습니다. timeline에 적은 familiarity tier가 compile된 정답에 남지 않았던 것입니다. compiler가 그 주석을 segment key로 내보내도록 고쳤고, schema가 `familiarity`(1–5의 정수)를 받게 되었습니다. 바뀐 hash는 C5의 세 artifact뿐이었습니다.

**Phase 5 — compile된 데이터셋에서 읽은 사실들.** 이 archive는 compile된 파일에서 몇 가지를 읽었습니다. "`c1-office` has 234 wake events, all on `input:writer`", "Only the chain head carries the frame TIMER", 그리고 "C2's batch tasks cannot finish inside their files"입니다. 마지막 것의 예로 `c2-p1a`의 hog는 180 s 파일에서 130.0 s의 일을, `c2-p3a`의 ffmpeg는 60 s에서 75.0 s를, `c2-p2a`의 download는 60 s에서 25.0 s를 가졌습니다. batch job이 파일 안에서 끝나지 못한다는 이 사실은, 2026-10-01에 9.10 D17(batch job은 측정한 전체를 그대로 돌리고 파일이 그 길이를 따라간다는 결정)이 다른 방향에서 다시 다룹니다.

**Phase 6 — pair review의 finding 2.** Phase 6의 6.4는 driver table의 같은 mode 쌍들을 하나씩 검토했습니다(`docs/daemon/prior-table-pair-review.md`). 그 finding 2가 "the coverage grid tracked mode × familiarity only, so the coreset instances 17 of the 32 driver-table cells"였습니다. driver table의 32개 row 중 core set이 실제로 건드리는 것은 17개뿐이었습니다. 이것이 Phase 7을 불렀습니다.

- **prior table**은 driver table의 첫 판(v0)입니다. 각 row의 scheduler 설정을 이론에서 정했습니다(`daemon/driver-table/prior.yaml`).
- **pair review**는 그 표의 같은 mode 두 row(true와 false)가 무엇이 다르고, 어느 파일의 어느 채점 항목을 움직이는지를 한 문장씩 검토한 문서입니다.
- **scoring spec**(`harness/scoring/scoring-spec.yaml`)은 파일마다 무엇을 채점하는지(어떤 task의 어떤 지표를 어떤 가중치로)를 적은 파일입니다. 채점 항목 하나를 **term**이라고 부릅니다.

# 5장 · Phase 7: 32개 cell을 전부 채우다

이 장은 "core set은 왜 24개에서 50개가 되었고, 그때 무엇을 정했나"라는 질문에 답합니다. Phase 7은 2026-09-09의 spec session과 2026-09-10/11의 sub-task 7.1–7.7로 이루어집니다. 지금 core set의 뼈대, 즉 mode마다 C1 base 하나와 C7 counterpart 하나가 쌍을 이루는 구조가 이때 생겼습니다. 그리고 이때 정한 "원치 않는 배경 작업"의 정체(`clamscan`)와 크기(60 s)는 한 달 뒤 Phase 9에서 모두 다시 정해집니다.

## 5.1 구멍: 32개 중 17개

Phase 6의 pair review는 "the coreset instances 17 of the 32 driver-table cells"라고 적었습니다. Phase 7 archive(`_dev/archive/2026-09-11-phase-7-coreset-attribute-coverage.md`)는 질문을 시작하기 전에 이것을 compile된 정답에서 다시 셌습니다. "17 cells exercised; missing were the 14 `false` cells other than `gaming` and `indexing`, and `indexing/true`." pair review는 "thirteen `false` and `meeting/true`"라고 적었는데, `meeting/true`는 사실 `c6-fold`가 채우고 있었습니다. 다만 `c6-fold`는 pre-committed miss였습니다.

2026-09-10의 팀 memo(`docs/memos/2026-09-10-coreset-before-and-after-phase-7.md`)는 이 상태를 표로 보여 줍니다.

| | 있음 | 없음 |
|---|---|---|
| `true` row (16) | 15 | `indexing/true` |
| `false` row (16) | 2 (`gaming`, `indexing`) | 나머지 14 |

`false` 쪽의 두 개는 C2 쌍의 b 파일, 즉 `c2-p1b`의 색인 rescan과 `c2-p2b`의 `clamscan`이었습니다. memo는 이 상태의 의미를 이렇게 씁니다. "이러면 attribute accuracy라는 metric은 거의 의미가 없어요 — recognizer가 항상 `true`라고 답해도 95%가 나오니까요."

왜 못 봤을까요. archive가 확인한 사실은 grid 도구의 축이었습니다. "`dataset/tools/wlc/grid.py` counted `mode|tier` per segment and had no `background_wanted` axis, while building plan §3 framed the coreset as 'driver-table cell × familiarity tier × distractor presence'. The 2026-08-28 sign-off read a table that could not show the hole." memo는 같은 내용을 "표에 안 보이는 구멍은 sign-off에서 못 잡아요. 그래서 도구부터 고쳤어요"라고 씁니다.

그리고 "왜 지금인가"에 대한 memo의 답이 있습니다. "pipeline(harness 상단, simulator 통합, RQ0 실행)이 아직 coreset 위에서 돌기 전이라 지금이 제일 싼 시점이에요."

## 5.2 2026-09-09 spec session의 결정들

archive는 결정을 질문한 순서대로 열세 개 적습니다. spec은 같은 내용을 열네 개의 Locked decision으로 정리합니다(14번은 7.7에서 추가). 아래는 데이터셋의 모양을 정한 것들을 기록된 이유와 함께 옮긴 것입니다.

**목표 — 32개 cell 전부, 쌍으로(Phase 7 결정 1).** "All 32 driver-table cells are instanced in the coreset, each `false` cell as a one-diff pair of a same-mode `true` base." 더 좁은 세 선택지(C1 base가 있는 interactive mode 셋, C1 base 다섯, interactive mode 아홉)가 있었습니다. archive가 적은 기각 이유는 셋입니다. "controlled claims never rest on the generalset (building plan §4), so any `false` row left to it is never measured under controlled conditions", "the 'five novel designs' cost was overstated (every mode had a liftable segment)", 그리고 "building plan §3's own organizing frame is the driver-table cell." archive는 처음의 추천(파일 세 개)을 "withdrawn as resting on effort and TODO wording rather than research design"이라고 적습니다.

**batch mode의 `false`가 뜻하는 것(결정 2).** `compile`, `ml-train`, `render`, `transcode`, `indexing`, `backup`에서는 batch job 자체가 attribute가 판단하는 배경 작업이므로, `false` cell은 "그 job을 원치 않는 것"입니다. 다른 해석(원한 build에 원치 않는 색인기를 더하기)은 "contradicted `c2-p1b` and would make the segment's mode ambiguous"라는 이유로 기각되었습니다.

**보이는 단서가 없는 cell(결정 3).** 이름과 행동으로 구별할 수 없는 cell은 pre-committed miss로 낸다. 이유는 "Scoring them would charge the model for a distinction no observer of names and behaviour could make; leaving them empty would break the all-32 target."

**C1은 열여섯, 새 묶음 C7(결정 4).** C1은 mode마다 하나씩 열여섯 개가 되고, 새 묶음 **C7**이 mode마다 counterpart 하나씩 열여섯 개를 가집니다. `c7-<mode>`는 `c1-<mode>`에서 파생됩니다. C2(두 segment짜리 쌍)나 C4(label을 바꾸지 않는 끼워 넣기)에 넣는 안은 "one transform per group"이라는 이유로 기각되었습니다.

- **C7**은 attribute counterpart 묶음입니다. C1 base와 같은 mode인데 `background_wanted`만 `false`로 뒤집힌 파일들입니다.
- **counterpart**는 base 파일에서 한 가지만 바꿔 파생한 짝 파일입니다.

**interactive counterpart는 `clamscan`을 넣는다(결정 5).** 열 개의 interactive mode에서 counterpart는 job 하나를 넣습니다. "`clamscan` bound to `cpu-batch`, the same name in every file, arriving at 0 s with `total_work` equal to the 60 s segment, label flipped to `false`." 이유는 "One name so the ten `false` cells differ only in mode; tier 1 so no pair changes familiarity tier." archive는 0 s 도착의 이유도 적습니다(archive 결정 7). "so the label holds at every instant under every policy and the pair is one task apart. Mid-segment arrival leaves thirty seconds mislabelled or breaks same-interval pairing."

- **`clamscan`**은 ClamAV 백신의 명령줄 검사 프로그램입니다. 2026-10-01에 9.10 D3이 이것을 "stock 데스크톱에서 실제로 예약 실행되지 않는다"는 이유로 Ubuntu의 무인 업그레이드로 바꿉니다(7장).

**batch counterpart는 이름을 바꾼다(결정 6).** 여섯 batch mode에서는 orchestrator의 이름을 같은 archetype의 "원치 않는" 이름으로 바꿉니다. 이름 규칙은 base와 같은 tier의 검증된 이름이 우선, 없으면 다른 tier의 이름을 쓰고 불일치를 적으며, 그것도 없으면 결정 3을 적용합니다.

**demand class는 직접 선언한다(결정 7).** 모든 C7 파일과 기존의 파생 파일 여덟 개가 `demand: calibration`을 recipe의 `patch-meta`로 직접 선언합니다. archive의 이유는 "`oversubscribed` cannot hold for a uniform op (gaming's base alone is 1.46); admitting inheritance keeps the exception invisible. Closes the Phase 3 item."입니다.

**새 base는 기존 segment에서 가져온다(결정 8).** 새 C1 열 개(`mail`, `dev`, `photo`, `meeting`, `video-edit`, `ml-train`, `render`, `transcode`, `indexing`, `backup`)는 그 mode를 이미 담고 있던 다른 파일의 segment에서 task 집합을 가져오고, 출처를 파일 머리에 적습니다. "batch jobs sized to the 60 s segment where the source segment was longer." `meeting`만은 가져올 segment가 없어서 새로 설계했습니다. 이 "60 s에 맞춘 batch job"은 2026-10-01에 9.10 D17(batch job을 통째로 돌리는 결정)이 뒤집습니다.

**채점 항목(결정 9, 10).** 새 base의 term은 mode의 종류에 따라 정합니다. interactive는 전면 프로그램의 P99 대기 시간, 주기적 mode는 소비자의 `job` miss rate, batch-옆-editor mode는 editor의 P99와 job의 term입니다. 그리고 결정 10은 "Unwanted work carries no term"입니다. TODO에는 "base's terms verbatim"이라고 적혀 있었는데, archive는 이것이 "wrong for batch counterparts (it would reward the unwanted job's progress on a floor-cap row)"라고 적습니다. 원치 않는 job이 많이 진행된 것을 점수로 주면 안 된다는 것입니다.

- **P99**는 99번째 percentile 값입니다. 여기서는 키 입력이 CPU를 받기까지 기다린 시간의 상위 1 % 경계입니다.
- **miss rate**는 주기 작업이 마감을 놓친 비율입니다.

**grid는 보고만이 아니라 강제한다(결정 11).** "The grid becomes one row per driver-table cell, 32 rows with the five tier columns, per-segment counts, `ambiguous` reported outside the 32. The CI check fails when any cell has zero segments." archive의 이유는 짧습니다. "Report-only was rejected as the failure mode of August."

**generalset도 32개를 채워야 한다(결정 12).** building plan §4에 "a generated set instances every driver-table cell"을 적습니다.

> **왜 이렇게 정했나.** 결정 11의 이유 "the failure mode of August"는 2026-08-28의 grid 서명을 가리킵니다. 사람이 표를 보고 서명했지만, 표에 attribute 축이 없어서 구멍을 볼 수 없었습니다. 그래서 이번에는 사람의 눈 대신 CI가 빈 칸을 막게 했습니다. 웹 개발로 치면 code review에 맡기던 규칙을 lint rule로 옮긴 것입니다(Phase 7 결정 11, 2026-09-09).

## 5.3 sub-task들: 2026-09-10/11

**7.1 grid의 attribute 축**(`f6c3911`). 새 segment 주석 `pre_committed_miss`가 생겼습니다. 기존 `initiated` 주석으로는 표시할 수 없었기 때문입니다("since P3b is `scheduled` and fully recognizable"). 빈 cell 검사는 7.1부터 매번 보고하되 7.3부터 치명적으로 했습니다(`--require-coverage`). 7.2 동안 CI가 초록으로 남게 하려는 순서였습니다.

**7.2 새 C1 열 개**(`5700cf2`). seed 107–116. utilization 0.45–0.97. `c1-indexing`이 `pre_committed_miss`를 설정한 첫 파일이 되었습니다.

**7.3 C7 counterpart, 7.4 흡수**(`2273feb`, `6e4d405`). 이름 탐색의 결과가 이때 나왔습니다.

- `compile/false` → `dkms`. 근거는 Ubuntu noble의 man page와 Debian의 package 설명이었습니다("kernel modules to be dynamically built for each kernel on your system"). 이름 확인 workflow를 다시 돌렸고(`meas-ci:names:2`, run 34466009254), Ubuntu, Fedora, Arch에서 `dkms`가 runtime 수준으로 확인되었습니다.
- `transcode/false` → miss. Jellyfin의 transcoder가 `ffmpeg`라는 이름으로 설치되어, render 쌍의 원한 이름과 "a collision, not a cue"였습니다.
- `ml-train`, `render`, `backup` → miss. 같은 mode의 원치 않는 orchestrator가 다른 이름으로 존재하지 않았습니다.

여기서 작은 결정 하나도 기록되어 있습니다. names:2의 Ubuntu 표가 `tar`, `xz`, `clamscan`, `make`를 runtime에서 binary-only로 낮춰 보고했는데, archive는 이것을 "a container timing flake, not evidence to overwrite"로 보고 run-1 표를 유지한 채 run 2를 옆에 저장했습니다(`dataset/meas/names/run-2/`). 이 names:2의 Actions artifact는 2026-12-09에 만료될 예정이어서, 2026-09-13에 9.3이 release에 보존합니다.

7.3이 끝나자 32개 cell이 모두 채워졌고, artifact가 100개가 되었고, 기존 파생 파일 여덟 개는 bytes가 그대로였습니다.

**7.5 pair review**(`2793aff`). 열여섯 쌍을 검토했고, 두 grill이 있었습니다. (a) C7을 `calibration`으로 두는 이유를 building plan에 적기로 했습니다. "a counterpart's demand is its base's plus the injected job by construction; the pair, not the window, is the control." 세 번째 class를 만드는 안은 "reopening the Phase 3 item"으로, mode마다 크기를 바꾸는 안은 "impossible for gaming"으로 기각되었습니다. (b) `c7-meeting`과 `c7-media`는 cap이 채점 항목에 닿지 않는데도 judging pool에 남기로 했습니다. 이유는 "their `oracle`-versus-`fixed` gap is real and comes from EDF against the MLFQ default; the cap axis is unmeasured; report-only would have removed every periodic pair from the gate."

attribute 정확도에 관한 정정도 이때 있었습니다. "18 of 63 grid segments are `false`, so an always-`true` answer still scores about 71 percent by segment count; the headline is balanced accuracy with the confusion matrix." 파일을 더 넣는 대신 지표의 정의로 불균형에 답한 것입니다.

- **balanced accuracy**는 각 정답 class의 재현율을 평균한 정확도입니다. 한쪽 class가 많아도 "항상 많은 쪽으로 답하기"가 높은 점수를 받지 못합니다.

**7.6 문서 정리와 팀 memo**(`88ed887`). building plan, coreset guide, harness guide 등과 2026-09-10 memo가 이때 나왔습니다.

## 5.4 7.7 — RQ0 judging set을 다시 정하다

7.7은 2026-09-10에 7.5의 grill 도중 추가된 sub-task입니다. archive는 그 시작을 이렇게 적습니다. "The user rejected deferring it to Phase 8 ('we haven't run the gate; think as research design, not as what is frozen') and a first proposal to write it as decided without a grill." 일곱 질문으로 grill했습니다.

- **Q1 기준.** "pairs with a scored term, demand not a criterion (the window was built for progress terms; Phase 3's own note says demand bounds throughput, not latency, headroom)." 기각된 안은 "C2 only (no interactive row judged), pairs inside the window (a throughput criterion on latency terms, dropping office by 0.0008 of a lane)"였습니다. 수요 창을 기준으로 하면 office 쌍이 lane의 0.0008만큼 모자라서 빠지는데, 그것은 지연을 재는 항목에 처리량 기준을 들이대는 것이라는 뜻입니다.
- **Q2 C1 base.** batch base 여섯 개는 들어옵니다. "a wanted LOTTERY share is what a random row removes."
- **Q4 pre-committed miss.** 다섯 개의 pre-committed-miss 파일도 판정합니다. "the gate needs labels, not recognizability." Layer 1에서만 뺍니다.
- **Q6 admission test.** 2026-08-23 Q8의 파일별 headroom admission test가 gate의 파일별 기준이 됩니다. K개 이상의 judging file에서 파일별 gap이 g 이상이면 통과이고, K와 g는 실행 전에 정합니다. "no file removed after its gap is seen; the window a build-time heuristic for `oversubscribed` files only."

- **Layer 1**은 recognizer가 정답을 맞혔는가를 재는 층이고, **Layer 2**는 그 답으로 고른 scheduler 설정이 실제로 결과를 좋게 했는가를 재는 층입니다.
- **K와 g**는 RQ0 gate의 통과 기준입니다. 판정 파일 중 K개 이상에서 oracle과 random의 차이(gap)가 g 이상이어야 합니다.

결과는 Phase 7 결정 14입니다. "Twenty-seven files: the six C2 files, the six batch C1 bases …, and the fifteen C7 counterparts that carry a term." Phase 3의 여섯 파일이 스물일곱 개가 되었습니다.

## 5.5 숫자로 본 Phase 7

2026-09-10 memo §8의 표를 옮깁니다.

| | 전 | 후 |
|---|---|---|
| 파일 | 24 | 50 |
| segment (grid 위) | 37 (+1 ambiguous) | 63 (+1 ambiguous) |
| driver-table cell 채움 | 17 / 32 | 32 / 32 |
| `false` segment | 2 | 18 |
| always-`true`의 attribute accuracy | ≈ 95% | ≈ 71% |
| pre-committed miss (attribute 쪽) | 0 | 5 |
| novel / derived timeline | 13 / 11 | 23 / 27 |
| recipe 파일 | 4 | 5 |
| compiled artifacts | 48 | 100 |
| scoring spec | 23 파일, 44 term | 48 파일, 78 term |
| CI가 빈 cell을 잡나 | 아니오 | 예 |

memo의 요약 문장 하나도 기억해 둘 만합니다. "**simulator와 daemon의 contract는 하나도 안 바뀌었어요.**" Phase 7은 데이터셋만 넓혔고 형식은 건드리지 않았습니다. 반면 Phase 9는 형식(`declared_class`, focus 등)도 바꿉니다.

## 5.6 인경민에게 답한 두 가지

Phase 7 archive에는 인경민의 질문에 답한 부분이 있습니다. 데이터셋 자체는 아니지만, 이후 "원치 않는 배경 작업"이 어떻게 scheduler에 닿는지를 이해하는 데 필요합니다.

- **왜 simulator에 batch class가 있나.** workload 파일은 프로그램만 담고 archetype 이름도 label도 담지 않으므로, executor가 행동에서 class를 추론한다는 것입니다. "a full slice since the last voluntary block; TIMER tasks never." 미리 batch라고 표시하면 "would hand the OS intent — a different experiment."
- **왜 cap인가.** attribute가 CPU scheduler에 닿는 손잡이로, "a per-class share ceiling is the one knob that means the same thing under all four algorithms." 원래 출처로는 Linux의 CFS bandwidth control을 들었지만 "**No reference entry exists yet**; a `linux-sched-bwc` deployed-system entry (existence only) was proposed and not yet added."

- **voluntary block**은 task가 스스로 CPU를 내려놓고 기다리는 것(I/O나 신호 대기)입니다. 반대로 시간이 다 되어 강제로 내려오는 것은 **preemption**(선점)입니다.
- **cap**(`batch_bandwidth_cap`)은 batch class가 쓸 수 있는 CPU 비율의 상한입니다.

이 "행동에서 추론한 class" 옆에, 2026-10-09에 "프로그램이 스스로 선언한 class"(`declared_class`)가 두 번째 입력으로 들어옵니다(9.11 D4, 9.13 D2). `linux-sched-bwc` entry는 지금도 추가되지 않았습니다(12장).

## 5.7 Phase 8 — RQ0 gate spec이 처음 commit되다 (2026-09-11/12)

Phase 8은 harness의 윗부분을 records에서 판정까지 만든 phase입니다. 데이터셋의 phase는 아니지만, 그 끝에 commit된 RQ0 gate spec이 Phase 9의 목표 지점이 되므로 짧게 적습니다.

8.1은 boot default를 OSTEP 교과서에서 다시 가져왔습니다(3개 queue, 10 ms 등). 8.8은 RQ0 gate spec(`harness/experiments/rq0-gate.yaml`)을 commit했습니다. RQ0 준비 노트는 그 내용을 "25 judging files — `c7-meeting` and `c7-media` reporting-only under the executor assumptions, with a re-entry condition — K = 13, g = 0.5, N = 100, a nine-point boot-default sweep"이라고 적습니다. Phase 7의 스물일곱 개에서 두 개가 빠진 것입니다.

- **boot default**는 recognizer가 아직 답하지 않았을 때 쓰는 기본 scheduler 설정입니다. **boot-default sweep**은 그 기본값을 여러 값으로 바꿔 가며 결과가 기본값에 민감한지 보는 사전 등록된 점검입니다.
- **N**은 random 조건을 몇 번(seed 몇 개) 돌리는지입니다.

Phase 9의 spec은 자기 목표를 "return the project to the state Phase 8 ended in: the RQ0 gate spec committed and ready for the RQ0 run"이라고 적습니다. 즉 Phase 9는 Phase 8의 끝 상태를 다시 만드는 것이 목표입니다. 다만 그 gate spec의 내용은 크게 바뀝니다. 2026-10-09에 judging set은 19개, K는 10이 됩니다(8장).

## 5.8 Phase 7에서 나중에 바뀐 것

Phase 7이 만든 구조, 즉 C1 열여섯과 C7 열여섯의 쌍, 32개 cell을 CI가 강제하는 grid, `pre_committed_miss` 주석, "원치 않는 작업에는 term이 없다"는 규칙은 지금도 그대로입니다. 바뀐 것은 쌍의 내용입니다.

| Phase 7의 결정 | 지금 | 날짜와 기록 |
|---|---|---|
| interactive counterpart에 `clamscan`, 60 s | Ubuntu의 무인 업그레이드 `package-upgrade`, `unattended-upgr`로 표시, 26.385 s | 2026-10-01, 9.10 D3, D41, D45 |
| `compile/false`는 `dkms`라는 이름만 바꿈 | 실제 NVIDIA 모듈의 DKMS 재빌드를 측정한 두 entry, `c7-compile`은 base의 처음 225.458 s | 2026-10-02, 9.10 D4, D46–D59 |
| batch job을 60 s segment에 맞춤 | 측정한 job을 통째로, 파일이 그 길이를 따라감 | 2026-10-01, 9.10 D17 |
| judging set 27개 | 19개, K 10 | 2026-10-09, 9.14 결정 2와 그 수정 |
| C5의 tier 3 파일(`c5-t3`) | C6의 `c6-alias`로 이동 | 2026-10-12, 9.20 D8 |

# 6장 · 전환점: 2026-09-13의 critical findings와 Phase 9 spec

이 장은 "왜 데이터셋을 처음부터 다시 짓기로 했고, 다시 지을 때의 규칙은 무엇이었나"라는 질문에 답합니다. 2026-09-13 하루에 세 가지가 일어났습니다. 데이터셋의 근거를 원문과 대조한 검증이 열세 개의 critical finding을 냈고, 팀에게 예고 memo가 갔고, Phase 9의 spec이 열 개(처음에는 여덟 개)의 결정을 고정했습니다. 그 열 개의 결정이 이후 한 달 동안 모든 slice의 판단 기준이 됩니다.

## 6.1 2026-09-13에 한 일: 원문과 대조하기

2026-09-13의 검증은 세 갈래였습니다. 이 기록은 나중에 9.1이 `_dev/research/jioh/2026-09-13-verification/`에 그대로 옮겨 두었습니다.

1. **claim 대조.** 데이터셋이 출처에서 가져온 모든 주장을 목록으로 만들었습니다(`claims.md`). 그리고 독립된 reader들에게 저장소의 설명 없이 "주제와 서지 정보만" 주고 원문을 읽게 했습니다(`reads/R01–R11`). 그 다음 reader의 읽기와 저장소의 문장을 비교했습니다(`compare/K1–K5`). 판정은 SUPPORTED, WORDING-FIX, MISATTRIBUTED, CONTRADICTED, NOT IN SOURCE, OURS-UNDER-SOURCE-TAG, UNVERIFIABLE 중 하나였습니다.
2. **측정 audit.** meas-ci의 값을 raw release에서 다시 계산했습니다(`meas-report.md`, 결함 #1–#16).
3. **compile된 숫자 audit.** 결정 문서에 적힌 숫자를 build와 맞춰 봤습니다(`compiled-numbers-report.md`).

웹 개발의 비유로 하면, 문서에 "이 API는 p99가 200 ms다"라고 적혀 있을 때 그 숫자가 어느 대시보드의 어느 기간에서 왔는지 다시 찾아가 보는 일입니다. 그리고 찾아가 보니 다른 서비스의 대시보드였다는 것을 발견하는 일입니다.

- **claim**은 데이터셋이나 문서가 출처를 근거로 하는 주장 하나입니다. 이 프로젝트에서 "claim inventory"는 그 주장들의 목록입니다.

## 6.2 열세 개의 critical finding

검증의 결과는 `docs/memos/2026-09-13-critical-findings.md`에 정리되었습니다. 이 memo는 "Nothing in the repository was changed; resolution is left to the owners of each file"이라고 적습니다. memo의 요약은 네 묶음(A, B, C, D)이고, 열세 개의 finding은 A1–A5, B1–B7, C입니다. D는 원문과 대조하지 못한 출처의 목록이고 finding이 아닙니다(인지오의 답, 2026-10-16; 9.15 작업 목록 W-0749). 그래서 memo의 내용은 finding 열셋과 원문과 대조하지 못한 출처의 목록 하나입니다.

**A — 원문이 저장소의 설명과 다름.**

- **A1.** "`ocallahan-atc17`'s 2,430 processes come from a DynamoRio 6.1.0 build, not a Linux kernel build." 원문(USENIX ATC '17 §4.1)은 "make builds DynamoRio [8] (version 6.1.0) with make -j8"이라고 적습니다. 인용 문장은 정확했지만 workload의 정체가 틀렸습니다. 영향은 문서 여덟 개와 `build-orchestrator`의 기본 `spawn_count`였습니다. 같은 memo는 측정된 kernel build가 "a median of 11,883 compiler-family processes"였다고 적습니다.
- **A2.** "The 16.7 ms frame budget attributed to `lavd-ossna24` does not appear in the slides." 30장의 슬라이드 어디에도 16.7, 60 fps, "frame budget"이 없었습니다. 유일한 시간 예산은 슬라이드 27의 "a targeted latency (e.g., 15 msec)"였고, 그것은 frame 주기가 아니라 scheduling 창이었습니다. 영향은 `game-task-chain.frame_period`였고, 이 값은 모든 gaming 파일의 박자와 lane-scaling의 분모였습니다.
- **A3.** Roeser의 158 ms는 log 척도의 위치 모수인데 평균으로 저장되고 뽑혔습니다. 논문 자신의 pause 성분(~253 ms)은 쓰이지 않았습니다.
- **A4.** Coetzee의 "짧게 사는 kernel-build process"는 compiler가 아니라 `cp`와 `mkdir`이었습니다.
- **A5.** `ananicy-rules`의 `type` class는 행동이 아니라 처방으로 묶인 것이었고, 그것을 가져오는 규칙도 고르지 않게 적용되었습니다.

**B — 데이터셋과 도구.**

- **B1.** `game-task-chain`의 두 파라미터(`frac_long_lived`, `frac_wakeups_from_wait`)는 compiler가 한 번도 읽지 않았고, 꼬리 파라미터는 슬라이드 tag를 달았지만 placeholder였습니다. 그리고 `n_tasks: 300`은 "counts never carry values here"라는 library 자신의 규칙을 어겼습니다. 그래서 모든 gaming 파일이 `game.exe × 300`을 보였습니다.
- **B2.** `compiler-child.disk_wait`의 분산 `sigma_log: 0.8`은 측정 전의 placeholder인데 측정 tag를 달고 있었습니다.
- **B3.** 측정된 최대 동시 compiler-family process는 `-j8`에서 16개였는데 archetype은 자식을 8개로 제한했습니다.
- **B4.** 끝이 없는 loop에 선언된 `per-iteration` 추출이 실제로는 `per-task`로 compile되었습니다.
- **B5.** "`desktop-interactive` bursts average half of each input gap, so a focused editor runs at ~50% CPU." 예로 `c1-compile`의 focus를 받은 `code` task가 56 s focus 창에서 정적 수요 28,470,806 µs를 가졌습니다. 출처인 interbench의 X는 "창을 잡고 화면을 가로질러 끄는" 부하였는데, 입력 간격은 타이핑에서 왔습니다. memo는 "The archetype thus combines typing inter-arrivals with window-drag CPU cost"라고 적습니다.
- **B6.** `gnome-shell`, `Xorg`, `pipewire`가 server daemon에서 잰 `system-daemon` 값에 묶여 있었습니다. 그리고 `c1-gaming`의 `wineserver`는 1,225 s의 sleep을 뽑아서 60 s 파일 안에서 한 번도 깨어나지 않았습니다.
- **B7.** 작은 틈들. linter는 `category_source`의 값이 아니라 존재만 봤고, timeline의 `count`에는 출처 칸이 없었고, `background-crawler`는 어떤 timeline에도 묶이지 않았고, building plan이 배포한다고 한 개인정보 제거 도구가 저장소에 없었습니다.

**C — 측정 fold-in 뒤에 남은 낡은 문장.** 예를 들어 `docs/references.md`가 `meas-ci`를 "reserved (no runs yet …)"라고 적고 있었습니다.

**D — 원문과 대조하지 못한 출처(finding이 아닌 목록).** `chang-chi21`(ACM이 403을 돌려줌)과 `cpsmark-tbench23`(ScienceDirect가 자동 접근을 거부함)는 `verified`로 표시되어 있었지만 원문을 읽지 못했습니다. 그 뒤 `cpsmark-tbench23`은 Wayback에 보관된 출판사 PDF로 같은 날 전문을 읽었고(`docs/references.md`의 status), `chang-chi21`은 2026-10-16에 registry와 `docs/references.md`에서 빠졌습니다(9.10 D34, 9.12 D102).

- **placeholder**는 측정이나 출처가 없는 자리를 임시로 채운 값입니다. Phase 9 spec 결정 1은 출처 없는 값의 label로 convention, arithmetic, design과 함께 "placeholder"를 들었지만, 2026-10-16에 인지오가 placeholder label을 두지 않기로 정했습니다(9.15 작업 목록 W-0750). 측정을 기다리는 값은 `meas-pending`을 달고, `make lint`의 freeze가 library의 parameter와 timeline의 bound value에서 그것을 거부합니다.

## 6.3 측정 audit과 compile audit이 보탠 것

memo의 열세 개 외에도, 측정 audit과 compile된 숫자 audit이 문제를 보탰습니다. 2026-09-13의 예고 memo(`docs/memos/2026-09-13-dataset-rebuild-heads-up.md`)가 그 핵심을 한국어로 요약합니다.

- **측정 방법.** "compiler 'child'가 cc1 하나가 아니라 번역 단위당 process 네 개쯤(gcc·cc1·as·fixdep)이라 cc1 하나의 CPU가 약 4배 작게 잡혔어요. `disk_wait`은 disk 대기를 잰 값이 아니고, voluntary context switch는 main thread만 셌어요."
- **compile된 workload의 동작.** "focused editor가 CPU를 약 50% 쓰고 burst의 95% 안팎이 10 ms slice보다 길어요. prior table의 'editor는 slice 안에 block해서 MLFQ 위 queue에 남는다'는 전제가 안 맞아요."
- **harness.** "guard `tick_count`의 chain check가 c2-p2a·c2-p2b에서 구조적으로 fail해요 … 지금대로면 RQ0 판정이 `invalid`가 돼요."
- **판정 set.** "c2-p2a는 10 ms slice에서 두 row가 차이를 못 내고, c1-backup의 borg는 혼자 돌아도 60 s 안에 못 끝나서 turnaround가 항상 censored예요."

- **context switch**는 CPU가 한 task에서 다른 task로 넘어가는 일입니다. voluntary context switch는 task가 스스로 기다리러 갈 때의 전환입니다.
- **MLFQ**(Multi-Level Feedback Queue)는 CPU를 오래 쓰는 task를 점점 낮은 우선순위 queue로 내리는 scheduling 방식입니다. 짧게 쓰고 기다리는 interactive task가 높은 queue에 남는 것을 기대합니다.
- **turnaround**는 job이 도착해서 끝날 때까지의 시간입니다. 파일이 끝날 때까지 job이 끝나지 않으면 그 값은 "censored"(관측되지 않음)가 됩니다.

phase 9의 spec은 이 밖에 memo에 없는 여섯 개 finding도 범위에 넣었습니다. "interbench's Compile load forks no processes; the '~5.7 ms' download sleep matches no version of `dataset/archetypes.yaml`; Roeser's Table 3 reports the spreads the archetype calls convention; LAVD slides 12 and 16 on wineserver; CpsMark+ contradicts 'time-shared compositions'; the `chang-chi21` details." 그리고 그전까지 원문과 대조한 적이 없던 registry entry 열두 개(`pcmark10`, `sysmark30`, `sysmark25`, `procyon`, `gamemode-docs`, `steam-downloads`, `dkms-man`, `dkms-debian`, `zhang-chb15`, `gonzalez-chi04`, `mark-chi05`, `focal-arxiv26`)도 넣었습니다.

## 6.4 예고 memo — 무엇이 바뀌고 무엇이 그대로인가

같은 날 인경민과 박이안에게 예고 memo가 갔습니다(9.2). 제목은 "workload dataset 다시 만들기 예고 — 무엇이 바뀌고 무엇이 그대로인지, 인경민께 질문 세 개"입니다.

바뀌는 것은 넷이었습니다. 데이터셋(archetype 값, timeline 구성, 측정 도구, 문서), 데이터셋 위의 결정(scoring spec, guard spec, prior table과 pair review, RQ0 gate spec), 데이터셋 밖의 인용(related-work, 연구 제안서, harness 상수의 근거), 그리고 순서입니다. memo는 순서를 이렇게 적습니다. "기록 보존과 측정 도구 수리 → 영역별 조사를 병렬로 … → dataset rebuild 한 번 → 위 결정들 rework 한 번 → 문서 정리와 마무리 memo."

그대로인 것은 "config schedule, recognition log, trace, telemetry 형식과 invocation contract"였습니다. 즉 두 팀원의 프로그램이 읽고 쓰는 형식은 범위 밖이라고 약속했습니다. 이 약속에는 나중에 예외가 둘 생깁니다. 2026-10-08에 memo 끝에 "정정"이 붙어 `declared_class` 필드가 들어간다고 알렸고, 2026-10-11에는 focus가 telemetry에 들어갑니다. 그리고 2026-10-10 audit은 rebuild된 compile 파일에서 자식이 자식을 깨우는 WAKE가 생겨 simulator의 loader가 다섯 파일을 거부한다는 것을 찾고, "the heads-up memo promised the input format unchanged. The usage is new; 경민 was not told"라고 적습니다(9장).

memo §4는 인경민에게 executor 질문 세 개를 던졌습니다. 이 셋은 Phase 9 spec 결정 7에도 그대로 적혀 있습니다.

1. "LOTTERY — editor 자신의 burst tail이 batch class일 때 batch share는 어떻게 나뉘나요?"
2. "EDF — frame chain의 stage는 deadline class인가요, residual class인가요?"
3. "editor가 아직 RUN 중일 때 keystroke가 오면 어떻게 되나요?"

- **LOTTERY**는 task마다 추첨권을 주고 추첨으로 다음 task를 고르는 scheduling 방식입니다. 이 프로젝트에서는 batch class와 나머지에 추첨권을 `batch_share : (1 − batch_share)`로 나눕니다.
- **executor**는 simulator 안에서 scheduling 규칙을 실제로 집행하는 부분입니다.

이 세 질문이 지금 어떻게 되었는지는 12장에서 정리합니다.

## 6.5 Phase 9 spec의 결정들

Phase 9의 spec(`_dev/docs/spec/jioh/phase-9-workload-dataset-rebuild.md`)은 "Decided in the 2026-09-13 spec session"이라고 적습니다. 목표는 이렇습니다. "Resolve what the workload dataset and everything built on it rest on, rebuild the dataset, and return the project to the state Phase 8 ended in: the RQ0 gate spec committed and ready for the RQ0 run."

결정은 열 개입니다. 1–8은 2026-09-13에, 9와 10은 2026-10-11에 더해졌습니다. 아래에 각 결정을 원문 그대로 인용하고, 그 뜻을 풀어 적습니다.

**결정 1 — 검증 기준.**

> "A claim taken from a source is verified when it is recorded with the verbatim passage, its locator, and the copy read (URL or commit, version, date), and the check covers the whole claim the repository makes — its object, unit, statistic, scope and population. The source is read independently, without the repository's description of the claim, before the reading is compared with the repository's wording. A claim whose passage is not found is unverified. A value no source states carries no source tag and is labelled for what it is: convention, arithmetic, placeholder, or design."

풀어 쓰면 이렇습니다. 출처의 주장은 원문 구절, 위치, 읽은 사본(URL이나 commit, 버전, 날짜)과 함께 기록될 때만 검증된 것입니다. 검사는 주장의 대상, 단위, 통계량, 범위, 모집단을 모두 덮어야 합니다. A1의 2,430은 문장은 맞았지만 "대상"이 틀렸습니다. 그리고 출처가 없는 값은 tag를 달지 않고, convention, arithmetic, placeholder, design 중 무엇인지 label을 답니다.

- **design**은 이 저장소에서 "출처가 아니라 실험 설계자가 고른 값"이라는 뜻의 label입니다. 예를 들어 파일의 길이, 끼워 넣는 job의 정체가 design입니다.
- **locator**는 출처 안의 위치(쪽, 절, 슬라이드 번호, 코드 줄)입니다.

**결정 2 — archetype 안에서 몽타주 금지.**

> "All numbers of one archetype come from one observation: one study population, one trace, or one measurement run. Several documents about the same observation count as one source; one document mixing different traces does not. Our own measurement run counts as one observation. Research looks for one observation that covers the whole archetype first; where none exists, the archetype comes to 인지오 as a decision."

archetype 하나의 숫자는 모두 관찰 하나에서 와야 합니다. 이 결정이 Phase 2 library의 여러 entry를 해체합니다. 예를 들어 `desktop-interactive`는 입력 간격을 타이핑 연구에서, CPU 비용을 interbench의 창 끌기에서 가져왔습니다(B5). 서로 다른 관찰을 이어 붙인 몽타주였던 것입니다.

**결정 3 — timeline에도 같은 규칙.**

> "Timeline content presented as how real desktops behave — task sets, co-occurrence, order, counts, typical durations, process names — follows decision 2, one observation per situation. The experiment's own interventions and calibration sizes — label flips, injections, renames, file length, `lane_share` — are labelled as design and carry no source tag."

timeline이 "실제 데스크톱이 이렇다"고 보여 주는 것은 관찰 하나에서 와야 하고, 실험 자체의 개입(label 뒤집기, 끼워 넣기, 이름 바꾸기, 파일 길이)은 design이라고 적어야 합니다.

**결정 4 — 연구가 빈칸을 채운다.**

> "Where the current sources do not ground a value or a structure, the phase researches new grounding rather than leaving the gap empty. A slice declares that no single observation exists only after a search log covering four classes — peer-reviewed and preprint literature; primary project and vendor documentation and source code; public traces and datasets; whether our own measurement can observe it — with the terms, venues and results recorded, and then brings 인지오 the nearest candidates with what each covers and does not."

"관찰이 없다"고 말하려면 네 종류(문헌, 프로젝트와 vendor 문서와 소스 코드, 공개 trace와 데이터셋, 우리 측정으로 볼 수 있는가)를 모두 찾아본 기록이 있어야 합니다.

**결정 5 — 측정 장소.**

> "Our own measurement runs on CI runners only. What a runner cannot observe comes from literature or public traces, or to 인지오 as a decision. This is a stated limitation."

- **CI runner**는 GitHub Actions가 workflow를 돌리는 가상 기계입니다. 이 프로젝트의 측정은 모두 여기서 합니다.

**결정 6 — phase의 구조.**

> "First, the 2026-09-13 verification records are persisted into the repository, and the measurement tools are fixed, including preserving the `meas-ci:names:2` run before its Actions artifacts expire on 2026-12-09. Then research-and-decision slices by domain, runnable in parallel: gaming; interactive and typing; compile; background and IO; browser and comms; daemons and session processes; scenarios and timelines; scheduler-side constants and groundings; related-work and proposal prose. Then one rebuild of the dataset. Then one consumer rework — scoring spec, guard spec, prior table and pair review, RQ0 gate spec — with one harness changelog entry and one re-pin. Last, one sweep of docs, memos and guidebook corrections. Before the sweep, added 2026-10-11: the telemetry's focus, the compiler and build-gate fixes, the generator and the grids, and their consumer work (decisions 9 and 10)."

**결정 7 — 팀과의 소통.**

> "A heads-up memo to 인경민 and 박이안 at the start of the phase: what will change, what stays stable, and three executor questions to 인경민 … A final memo at the end of the phase with the actual changes."

**결정 8 — 끝나는 조건.**

> "Every finding is resolved. The claim audit, the measurement audit and the compiled-number audit are re-run on the final repository state and return nothing unresolved: every claim meets decision 1, every archetype and every realism claim in a timeline meets decisions 2 and 3 or carries 인지오's recorded decision, every measured value reproduces from the released raw data and describes what its method measured, and no statement in the prior table, pair review, scoring spec, guard spec, RQ0 gate spec or memos is wrong or stale against the rebuilt data. The final memo is sent. The project stands where Phase 8 ended: the RQ0 gate spec committed and ready for the RQ0 run. The generated layer reproduces from its generator and manifest."

마지막 문장("The generated layer reproduces …")은 2026-10-11에 결정 9, 10과 같은 commit(`4f0eb86a`)으로 더해졌습니다(`git log -S`로 확인). 이 끝나는 조건을 확인하는 일이 9.16(exit audit)입니다.

**결정 9 — generated layer (2026-10-11 추가).**

> "A generated layer stands beside the core set. Each group whose claim is a rate has a generated set that enumerates the factor in full from the C1 task sets, labelled design with no realism claim; the authored files remain as existence cases. The naturalistic set stays in the backlog."

**결정 10 — telemetry의 focus (2026-10-11 추가).**

> "The recognizer's snapshot carries the focus holder beside the name → count multiset; a focus change is a set change. Behaviour, labels and PIDs stay out."

결정 9와 10이 어떻게 생겼는지는 9장에서, 어떻게 실현되었는지는 10장에서 다룹니다.

spec의 열린 항목은 "Left to each sub-task's own spec session"이라는 제목 아래 넷이었습니다. 검증 기록의 형식과 위치, 측정 도구를 고치는 방법, 각 archetype과 timeline의 값과 구조, 그리고 "Any re-decision of the RQ0 judging set, the boot-default sweep points, or K."

## 6.6 phase의 구조: 기록 → 도구 → slice → rebuild → rework → sweep

결정 6의 구조를 TODO의 실행 순서와 함께 그리면 아래와 같습니다. TODO의 문장은 "9.1 ∥ 9.2 ∥ 9.3 first → 9.4–9.12 in parallel, after 9.1 and 9.3 → 9.13 → 9.14 → 9.17 → 9.18 → 9.22 → 9.19 → 9.20 → 9.21 → 9.15 → 9.16"입니다.

```text
2026-09-13          2026-09-13 → 10-09                  10-09     10-09/10     10-11 → 10-14                         10-14 →
┌──────────┐   ┌─────────────────────────────────┐   ┌──────┐   ┌──────┐   ┌──────────────────────────────┐   ┌──────┐   ┌──────┐
│ 9.1 기록  │   │ research slices (병렬)           │   │ 9.13 │   │ 9.14 │   │ 2026-10-11에 추가된 다섯과 하나 │   │ 9.15 │   │ 9.16 │
│ 9.2 memo │──►│ 9.4 gaming   9.5 interactive    │──►│ re-  │──►│ con- │──►│ 9.17 focus                    │──►│ docs │──►│ exit │
│ 9.3 도구  │   │ 9.6 compile  9.7 background/IO  │   │ build│   │ sumer│   │ 9.18 compiler·schema·gate     │   │ sweep│   │ audit│
└──────────┘   │ 9.8 browser  9.9 daemon·session │   └──────┘   │ re-  │   │ 9.22 build time               │   └──────┘   └──────┘
               │ 9.10 scenarios·timelines        │              │ work │   │ 9.19 generator, C3 grids      │    (WIP)      (open)
               │ 9.11 scheduler constants        │              └──────┘   │ 9.20 C4·C5 grids, C5 → C6     │
               │ 9.12 related-work prose         │                         │ 9.21 generated layer 소비자    │
               └─────────────────────────────────┘                         └──────────────────────────────┘
```

TODO에는 두 개의 운영 규칙도 적혀 있습니다. 하나는 "always work on branch `jioh/dataset-rebuild`"이고, 다른 하나는 slice의 규칙입니다. "9.4–9.12 follow `_dev/research/jioh/research-slice-workflow.md`: domain slices own archetypes, 9.10 owns timelines; decisions are applied to `dataset/archetypes.yaml` as they land, logged in the slice's research folder, never in the public docs."

## 6.7 research slice의 작업 방식

slice의 작업 방식은 9.4를 시작하면서 2026-09-13에 정해졌습니다(`_dev/research/jioh/research-slice-workflow.md`). 데이터셋이 지금처럼 결정마다 근거를 가진 모양이 된 것은 이 방식 덕분이므로 요약해 둡니다.

**범위.** 영역 slice(9.4–9.9)는 자기 영역의 archetype을 모두 갖습니다. timeline의 내용(task 집합, 함께 도는 것, 순서, 개수, 이름)은 어느 영역을 그리든 9.10의 것입니다. archetype 안에 있던 개수는 영역 slice의 결정으로 archetype을 떠나고, timeline이 대신 가지는 숫자는 9.10이 정합니다.

**네 단계.**

1. **scope card.** slice가 다룰 항목 목록입니다. 항목마다 현재 값, 현재 tag, 검증 판정, 종류(source claim, convention, arithmetic, placeholder, design)를 적습니다. 인지오가 검토한 뒤에 검색이 시작됩니다.
2. **search.** 항목마다 Phase 9 결정 4의 네 종류를 찾아봅니다. reader는 저장소의 현재 값을 보지 않고 중립적인 주제만 받습니다.
3. **decision session.** 항목을 하나씩 후보와 함께 인지오에게 가져가고, 결정이 나면 바로 `dataset/archetypes.yaml`에 적용하고 다시 compile하고 changelog와 함께 commit합니다.
4. **hand-off.** changelog가 9.10, 9.13, 9.14, 9.15에 넘기는 인터페이스가 됩니다.

**기록.** "The public docs (`docs/`, `dataset/README.md`) carry no changelog of Phase 9 corrections and no account of the prior values. They describe the final state; 9.15 brings them there." 그래서 2026-09-13부터 지금까지 공개 문서는 대부분 Phase 9 이전의 데이터셋을 설명하고 있습니다. 이것이 9.15가 해야 할 일의 크기입니다(12장).

> **왜 이렇게 정했나.** slice를 영역별로 나누고 병렬로 돌린 이유는 Phase 9 결정 6이 적습니다("research-and-decision slices by domain, runnable in parallel"). 결정을 바로 `archetypes.yaml`에 적용하는 이유에 대해서는 workflow 문서가 "Each decision is applied as it lands"라고만 적고, 별도의 논거는 기록되어 있지 않습니다. 다만 결과적으로 slice마다 compile이 깨지지 않는지 바로 확인되었고, 각 changelog entry에 "make lint clean, make check verified" 같은 확인이 붙어 있습니다(예: 9.4 D2).

# 7장 · Phase 9 첫 구간: 기록, 도구, 아홉 개의 research slice

이 장은 "2026-09-13부터 2026-10-09까지, archetype library와 timeline은 어떤 결정을 거쳐 지금의 모습이 되었나"라는 질문에 답합니다. 이 구간에서 Phase 2의 열두 개 entry 중 여덟 개가 사라지고, 측정된 entry가 스물아홉 개가 됩니다. 그리고 core set의 "원치 않는 작업"과 batch job이 모두 실제로 관찰한 job으로 바뀝니다. 결정이 수백 개이므로, 이 장은 데이터셋의 모양을 바꾼 결정과 그 결정을 부른 측정만 고릅니다. 각 archetype의 값과 측정 방법은 archetype library를 다루는 권과 측정 campaign을 다루는 권에서 자세히 설명합니다.

## 7.1 9.1 — 검증 기록을 저장소에 (2026-09-13)

9.1의 spec(`_dev/docs/spec/jioh/task-9.1-verification-records.md`)은 2026-09-13의 검증 결과를 저장소에 옮기는 규칙 여섯 개를 정했습니다. 위치는 `_dev/research/jioh/2026-09-13-verification/`입니다(결정 1). 글로 된 기록과 audit script, 그 출력은 commit하고(결정 2), 출처의 사본과 raw 측정 데이터는 local에 두고 gitignore합니다(결정 3). 예외는 `meas-ci:names:2`의 artifact 사본 하나로, 그것만은 commit합니다(결정 4). 기록은 경로 외에는 고치지 않고 옮깁니다(결정 5). "passages, locators, verdicts and the known input errors that the comparisons already correct stay as they were."

이 결정 덕분에, 이후 slice들은 "C-lavd-9 NOT IN SOURCE" 같은 판정을 근거로 인용할 수 있었습니다. 9.16의 exit audit도 이 기록을 출발점으로 다시 돌릴 예정입니다.

## 7.2 9.2 — 예고 memo (2026-09-13)

9.2는 6장에서 본 예고 memo(`docs/memos/2026-09-13-dataset-rebuild-heads-up.md`)를 보낸 일입니다. 이 memo의 "Updated"는 2026-10-08입니다. 그날 `declared_class`에 관한 정정이 끝에 붙었기 때문입니다.

## 7.3 9.3 — 측정 도구를 고치고 다시 분석하다 (2026-09-13)

9.3의 spec(`_dev/docs/spec/jioh/task-9.3-measurement-tools.md`)은 2026-09-13 측정 audit의 결함을 둘로 나눴습니다.

**고친 것(결정 2).** "Where a tool reports a wrong number for what actually ran, it is fixed." 도구가 실제로 일어난 일을 틀리게 세는 경우입니다. `proc_sampler.py`는 voluntary context switch를 main thread만 셌습니다(#3). `verify_names.py`는 검증 수준 판정과 15글자 `comm` 자름이 틀렸습니다(#14). `analyze.py`는 compiler-family 전체를 compiler 자식 하나로 취급했고(#1), Chromium renderer 집합이 틀렸고(#5), fit에서 0 값을 버렸고(#9), `dispatch_overhead`의 나눗수가 틀렸습니다(#12).

**넘긴 것(결정 3).** 도구가 애초에 재지 않는 양, 즉 I/O 대기(#2), wake 단위 분포(#8), 네트워크 처리량(#11)과, workflow의 설정이 이름대로의 행동을 만들지 못한 경우, 즉 Element renderer가 없음(#4), tab이 load되지 않음(#6), tracker가 색인하지 않음(#7), `tar -cf /dev/null`이 내용을 읽지 않음(#16)은 고치지 않고 slice들에 넘겼습니다.

그리고 결정 4는 "One re-analysis, no new CI runs"였습니다. 고친 analyzer를 release `meas-ci-2026-08-28`의 raw 데이터에 한 번 돌려, 어떤 값이 얼마나 움직였는지 비교표를 만들었습니다(`_dev/research/jioh/2026-09-13-meas-reanalysis/`). `dataset/`는 바꾸지 않았습니다. 결정 1은 names:2를 release의 asset으로 보존하고, release notes를 "the summary comes from cli:3, not cli:1"로 고쳤습니다.

> **왜 이렇게 정했나.** "고칠 것"과 "넘길 것"을 나눈 기준은 결정 2와 3의 문장 자체입니다. 도구가 일어난 일을 틀리게 센 것은 도구의 버그이므로 고치고, 도구가 원래 재지 못하는 것이나 측정 설정이 목표한 행동을 만들지 못한 것은 측정 설계의 문제이므로 각 영역의 slice가 새 campaign으로 답하게 했습니다(9.3 spec 결정 2–3, 2026-09-13).

## 7.4 9.4 — gaming: 출처 하나와 그 한계 (2026-09-13, D9는 2026-09-17)

9.4는 첫 slice였고, slice 작업 방식이 이것을 시작하며 정해졌습니다. 대상은 `game-task-chain` 하나입니다. 이 archetype은 게임의 frame을 만드는 thread들이 한 줄로 서로를 깨우는 chain입니다.

- **chain**은 앞의 task가 일을 마치고 다음 task를 깨우는 순서로 연결된 task들입니다. 게임에서는 입력 처리, 게임 logic, 그래픽 명령 제출이 이렇게 이어집니다.

**9.4 D1(출처 하나를 관찰로 인정한 결정).** 인지오의 결정으로 `game-task-chain`은 `lavd-ossna24`(Valve의 LAVD scheduler 발표 슬라이드)를 하나의 출처로 유지했습니다. 슬라이드 12–17을 "one observation of an unnamed game on an unnamed machine, collected with `perf sched record`"로 받아들였습니다. 택하지 않은 대안은 공개된 `scx_lavd` sample log와 "our own CI measurement of a native game"이었습니다. 이 결정은 2026-10-11 audit의 class-A 결함 A3("game chain이 talk 등급의 출처에 기대고 있다")로 다시 올라오지만, 인지오가 "resolved as is"로 닫습니다(9장).

**9.4 D2(frame 주기를 design으로 바꾼 결정).** `frame_period` 16667 µs는 값은 그대로 두고 tag를 `lavd-ossna24`에서 `steamos-refresh`로 바꿨습니다. label은 design입니다. "the game is modelled as display-paced at the Steam Deck LCD default refresh with the 1:1 frame limit; 16667 µs is 1/60 s arithmetic." 이유는 critical finding A2 그대로입니다. "The deck states no frame period." 새 entry `steamos-refresh`의 원문은 Valve의 "The SteamOS 3.2 Update"(2022-05-26)의 "The default is 60Hz … 60hz = 16.66ms/frame"입니다. 택하지 않은 대안은 25000 µs(40 Hz 모드)와 주기 없음(슬라이드의 무제한 benchmark)이었습니다.

**9.4 D3(archetype을 chain만으로 줄인 결정).** `n_tasks`(300), `tail_idle_gap`, `tail_run`을 지웠습니다. 이유는 둘입니다. 개수는 "The count was held against the library's own rule"이었고, 꼬리 값은 "No observation describes the tasks outside the deck's top 30–40 … the values were placeholders under a source tag"였습니다. compile된 결과로 모든 gaming 파일이 `<id>.tail.<j>` task 284개를 잃었고, `c1-gaming`의 수요가 1.46에서 1.30이 되었습니다. "The recognizer-visible count `game.exe ×300` is gone."

**9.4 D4(wineserver를 chain의 member로 넣은 결정).** 새 파라미터 `wineserver_run`(260 µs, 슬라이드 13의 "Some coordination tasks run very shortly (e.g., wineserver:260 usec)")이 생기고, wineserver가 chain의 첫 member 바로 뒤에 들어갔습니다. 근거는 슬라이드 11, 13, 16과 Wine의 호출 경로입니다. 그래서 2026-08-26 grill D22의 "wineserver → `system-daemon` 근사"가 끝났고, Phase 1의 열린 항목도 닫혔습니다. compile 결과로 wineserver는 "a `wineserver` task that runs each frame … instead of one that slept 1 225 s"가 되었습니다.

**9.4 D7(쓰이지 않던 두 파라미터를 지운 결정).** `frac_long_lived`와 `frac_wakeups_from_wait`는 "Neither was read by any tool"이므로 지웠습니다. 사실은 `modeling_notes`에 "what the encoding does not model"로 남겼습니다.

**9.4 D9(슬라이드의 schedule당 runtime을 wake당 RUN으로 읽은 한계, 2026-09-17).** 9.5 follow-ups 결정 4가 "RUN은 wake 하나의 수요"라고 정한 뒤, 슬라이드의 per-schedule runtime을 per-wake RUN으로 읽으면 선점으로 끝난 schedule에서 수요가 작게 잡힌다는 한계를 적었습니다. 크기는 같은 슬라이드의 선점 비율(25–30 %)에서 "about 1.4 schedules per wake on average"로 추정했습니다. 값은 바꾸지 않고, 9.14에 "the gaming files' sensitivity check sweeps chain-member RUNs over ×1.0–1.4"를 넘겼습니다. 이것이 지금의 chain-x1.2, chain-x1.4 variant 집합입니다.

## 7.5 9.5 — interactive와 typing: 몽타주를 측정으로 (2026-09-14 → 09-29)

9.5는 D1부터 D99까지, 가장 긴 slice 중 하나입니다. 대상은 editor, 브라우저, 메일, 미디어 재생 같은 interactive 프로그램입니다. Phase 2 library에서는 이것들이 `desktop-interactive`, `audio-playback`, `video-playback`의 세 entry였습니다.

**9.5 D2(`desktop-interactive`를 프로그램별로 나눈 결정, 2026-09-14).** "`desktop-interactive` is replaced by one archetype per bound application — `code`, `kdenlive`, `chrome` …, `soffice.bin`, `thunderbird`, `gimp` — each grounded on one observation of that application under phase decision 2." 근거로 든 문헌의 한 문장이 핵심을 보여 줍니다. "different applications have very different CPU requirements, even when handling the same type of user interface event"(Lorch, §4.7). 예를 들어 키 입력 하나에 Notepad는 10 ms 미만, Word는 약 32 ms를 썼습니다(Endo 1996).

**9.5 D3(관찰은 runner 측정 campaign이라는 결정, 2026-09-14).** 각 archetype은 CI runner에서 그 프로그램을 직접 돌린 측정 하나에서 값을 모두 가져옵니다. 2000–2004년의 Linux trace들은 제외했습니다. 이유는 "인지오 judges values measured on 100–664 MHz machines two decades ago unable to back a current application"입니다. 그리고 runner의 한계를 각 archetype에 적기로 했습니다. "no display refresh under Xvfb (paint cadence falls to toolkit timers), no GPU (rasterisation on CPU threads), no sound device."

**9.5 D4(재생할 타이핑 stream은 SWELL-KW라는 결정, 2026-09-14).** 측정 중에 프로그램에 실제 키 입력을 재생해야 했습니다. 고른 것은 SWELL-KW(`swell-icmi14`)입니다. 25명이 약 3시간씩 자유롭게 글을 쓴 기록으로, 키마다 시각과 focus된 프로그램이 있고 멈춤도 남아 있습니다. 택하지 않은 대안은 136M Keystrokes 데이터("transcription of memorised sentences, share > 1 s 0.7 %")와 Roeser의 copy-task 데이터였습니다. Word의 stream이 LibreOffice Writer와 VS Code를 함께 몹니다. 코드 편집의 시각 있는 키 입력 데이터셋이 없기 때문이고, 그 한계는 `modeling_notes`에 적었습니다.

- **SWELL-KW**는 네덜란드의 사무 작업 스트레스 연구가 공개한 데이터셋입니다. 이 데이터셋의 stream은 `dataset/stimulus/`에 들어 있고, 그 licence(CC-BY-NC-SA-4.0)가 9.15의 `dataset/LICENSE` 결정으로 이어집니다(12장).
- **stimulus**는 측정이나 compile 때 프로그램에 넣어 주는 입력(여기서는 키 입력의 시각 열)입니다.

**9.5 D6(응답 쪽 값은 Linux에서만이라는 규칙, 2026-09-14).** "a response-side value — CPU per wake, wake cadence, timer and paint behaviour, thread structure — comes from a Linux observation only; a stimulus-side value — inter-key intervals, pauses, click, drag and wheel timing — may come from an observation on any platform, since it is a property of the person, not of the machine." Windows에서 기록된 SWELL-KW를 쓸 수 있는 근거가 이 규칙입니다. 이 규칙은 9.6과 9.7도 따릅니다(9.6 D1).

**9.5 D19(측정한 아홉 entry가 몽타주 세 entry를 대체한 fold-in, 2026-09-15).** `office-writer`, `code-editor`, `mail-client`, `web-browser`, `image-editor`, `video-editor`, `video-player`, `audio-player`, `video-call`이 들어오고, `desktop-interactive`, `audio-playback`, `video-playback`이 빠졌습니다. 그와 함께 library의 모든 `dhakal-chi18`, `roeser-rw24`, `interbench:man-*` tag도 빠졌습니다. 2026-08-26 grill D7이 타이핑 간격의 출처로 정한 Dhakal이 이렇게 물러났습니다.

**2026-09-16 follow-ups grill.** D20까지의 fold-in 뒤에 follow-up grill이 열렸고, 그 결과가 9.5의 task spec(`_dev/docs/spec/jioh/task-9.5-interactive-typing-follow-ups.md`)입니다. Phase 9 전체에 영향을 준 결정이 여기서 나왔습니다.

- **결정 2 — 관찰은 CPU 하나에 고정한 프로그램.** "A measured archetype's observation is the application's process tree pinned to one CPU, matching the simulator's single lane."
- **결정 3 — phase 전체에서 모든 runner 측정은 single-core.** 그리고 Phase 2의 4-vCPU 측정을 아직 가진 일곱 entry(`build-orchestrator`, `compiler-child`, `background-crawler`, `io-stream`, `network-bulk`, `electron-comms`, `system-daemon`)를 9.6–9.9에 넘겼습니다.
- **결정 4 — wake 하나의 정의.** "A wake is a schedule-in preceded by a wakeup event for that thread since its last sleep. A resume after preemption is not a wake: its run is added to the preceding wake's run."
- **결정 7 — operation 세 개.** GIMP의 filter, Kdenlive의 timeline preview render, Chrome의 local page load. "Writer, VS Code and Thunderbird carry no operation."
- **결정 11 — stimulus 민감도는 사전 등록된 점검.** 136M 데이터를 두 번째 phase로 재생해 비교하되, "The archetypes carry SWELL-KW whatever the result."
- **결정 13 — 조합 지점의 scale 한계.** "The library's archetypes come from more than one observation venue, and their relative scales are not calibrated to each other; a timeline composing a runner-measured task with a literature-grounded one carries that limitation. It is stated once at the library level."
- **결정 14 — native compiled set을 버린다.** "The dataset ships the single-lane set only. Handed to 9.13 for the build and to 9.15 for the docs." spec의 scope는 이것이 결정 13과 "arose from the same reasoning"이라고 적습니다.

- **pin to one CPU**는 process가 특정 CPU 하나에서만 돌도록 묶는 것입니다(`taskset` 등). 측정 대상 프로그램을 CPU 하나에 묶으면 simulator의 lane 하나와 같은 조건이 됩니다.
- **operation**은 프로그램의 "무거운 작업 한 번"(filter 적용, page load 등)을 측정한 단위입니다. timeline이 시점을 정해 놓으면 compiler가 그 동안 operation의 행동을 끼워 넣습니다.

> **왜 이렇게 정했나.** native set을 버린 이유는 결정 13에 있습니다. library의 entry들이 서로 다른 관찰 장소에서 왔고 그 상대적 크기가 서로 맞춰져 있지 않으므로, "측정된 그대로의 수요"라는 native set의 전제가 성립하지 않습니다. 실험은 원래 `-single`에서만 돌렸으므로(2026-08-26 grill D16), native set은 근거 없는 숫자를 배포하는 것이 되었습니다(9.5 follow-ups spec 결정 13–14, 2026-09-16).

**9.5 D26(같은 기계에서 반복하는 campaign, 2026-09-18).** 이 결정을 부른 측정이 있습니다. 2026-09-16에 release한 campaign(`meas-ci-2026-09-16`)의 "45 jobs drew five CPU models, 22 on the EPYC 7763, and no application has its five repeats on one model." 그런데 `fold_in.py`는 모든 scope에 "4 vCPU AMD EPYC 7763"을 고정 문구로 써 넣고 있었습니다. 그래서 AMD EPYC 7763 한 model에서만 반복하고, 9.6 D10의 안정성 기준으로 반복 횟수를 정하는 새 campaign을 열었습니다. 기준은 "a 95 % half-width of at most 5 %, half the smallest difference this slice reports"입니다.

- **machine gate**는 측정 job이 시작할 때 CPU model을 확인하고, 정해진 model(AMD EPYC 7763)이 아니면 아무것도 재지 않고 멈추는 장치입니다(`dataset/tools/meas/machine_gate.sh`). GitHub의 runner는 사양의 모양만 보장하고 processor model은 보장하지 않기 때문입니다.
- **stability rule**은 반복 측정의 평균에 대한 95 % 신뢰구간의 반폭이 값의 5 %(또는 1 µs) 이하가 될 때까지, 같은 기계에서 최소 다섯 번 이상 반복한다는 규칙입니다. 측정 campaign을 다루는 권에서 자세히 설명합니다.

**9.5 D29(최소 다섯 번, 2026-09-19).** 9.6 D24(반복 방법의 출처를 원문으로 확인하고 최소 다섯 번을 정한 결정)의 hand-off로, 문헌에 기댄 보편 규칙이 되었습니다. 근거는 "`kalibera-ismm13` §11: 'We do not show counts of fewer than 5 executions as they could hardly be used to get the variance estimate right'"입니다.

**9.5 D47(유효성 검사에 실패한 반복을 빼는 규칙, 2026-09-20).** workflow가 "유효한 반복만 센다"고 했지만 빼는 방법이 없었습니다. 사례는 `thunderbird-send`의 반복 29였습니다. Outlook 창이 잘리지 않아서 다른 분기를 탔고, 함께 pool하면 operation 값의 반폭이 ±12.1 %에서 ±25.3 %로 벌어졌습니다. 그래서 이유와 함께 손으로 빼는 규칙과 도구(`pool_runs.py --exclude`)가 생겼습니다.

**9.5 D74(TIMER는 주기가 선언된 task에만, 2026-09-26).** 2026-09-26 검토에서 나온 결정입니다. 그때까지 fold-in은 측정된 모든 timer wake를 TIMER step으로 compile했고, 주기는 다음 wake까지의 간격이었습니다. 그런데 TIMER를 "주기 job, 마감은 다음 주기 경계"로 읽는 소비자가 셋(simulator contract, EDF의 deadline class, harness의 `job` 지표) 있었습니다. 결정을 부른 측정은 이것입니다. "In the compiled `c1-media` the `video` task's first period is 9 µs against a mean of 1,182 µs over 50,764 steps." 그래서 TIMER는 주기가 선언된 task(재생과 통화)에만 쓰고, 측정된 timer wake는 "a `WAIT` on a per-task timer channel, woken by an exogenous wake event at its measured absolute time"이 되었습니다. 이 결정 때문에 workload의 wake 사건 수가 크게 늘어납니다. 2026-09-26의 50개 파일은 531,740개 wake 사건, 84 MB였습니다(9.13 reads R4가 이 수치를 인용).

**untraced control(2026-09-27 grill).** 2026-09-26 검토는 "`perf sched record`로 측정하는 것 자체가 측정값을 움직이는가"를 물었습니다. 그래서 별도의 spec(`_dev/docs/spec/jioh/task-9.5-untraced-control.md`)이 생겼습니다. 같은 phase를 perf로 trace하면서 한 번, trace 없이 한 번 돌려 비율을 읽습니다. "A difference is written into that archetype's `modeling_notes` as a limitation of its values. No carried value changes." raw 기록은 release `meas-ci-control-2026-09-27`입니다.

- **`perf sched record`**는 Linux kernel의 scheduling 사건(누가 언제 깨어나고 CPU를 받고 내려놓는지)을 기록하는 도구입니다. 이 프로젝트의 측정 campaign은 대부분 이것으로 wake와 run을 셉니다.

**9.5 D99(`code`의 반복이 녹음의 끝보다 일찍 멈춘 것을 다시 읽은 결정, 2026-09-29).** `code`의 campaign은 window 44에서 멈췄는데, SWELL-KW의 Word 녹음은 57개 window를 가졌습니다. 그 횟수는 규칙의 첫 통과도, 녹음의 끝도 정하지 않은 것이었습니다. 인지오는 반복을 더하지 않고(선택지 B, 57까지 연장, 기각) 멈춤을 다시 읽는 선택지 A를 골랐습니다. 이 경우처럼 "예외로 실린 값"을 사전에 정한 횟수로 다시 잴지는 9.14로 넘겼고, 9.14는 그것을 사전 등록된 조건부 작업(contingency)으로 두었습니다(8장).

## 7.6 9.6 — compile: 첫 campaign을 버리고 다시 재다 (2026-09-17 → 09-29)

9.6은 D1부터 D38까지입니다. 대상은 `compiler-child`, `build-orchestrator`, `cpu-batch`입니다. 이 slice의 이야기는 "첫 campaign을 통째로 버리고 다시 잰" 과정으로 기억할 만합니다.

**9.6 D9(campaign이 돌았고, object job을 chain constructor로 쓰기로 한 결정, 2026-09-18).** 첫 campaign `meas-ci:build:35215328887`가 2026-09-17에 다섯 번 반복으로 돌았습니다. 이 campaign이 보여 준 것은 이후의 compile 파일 모양을 정했습니다. "29 035 processes per build in every repeat; 5 254 jobs — 2 908 object, 681 archive, 1 537 helper, 90 compiler probes, 38 links … 2 857 of the 2 908 object jobs are exactly `sh`, `gcc`, `cc1`, `as`, `fixdep`, `rm`." 즉 C 파일 하나를 compile하는 "object job" 하나는 process 여섯 개였습니다. critical finding의 "compiler 'child'가 cc1 하나가 아니라 번역 단위당 process 네 개쯤"이 측정으로 확인된 것입니다.

- **object job**은 make가 C 소스 파일 하나를 object 파일로 만드는 단위 작업입니다. 그 안에서 `sh` → `gcc` → `cc1` → `as` → `fixdep` → `rm` 같은 process들이 차례로 돕니다.

**9.6 D10(같은 기계 반복과 안정성 기준, 2026-09-18).** 다섯 반복을 보니 "four draws of an AMD EPYC 7763 and one of an Intel Xeon Platinum 8573C"였습니다. 차이는 컸습니다. "`cc1` CPU per process 269 ms against 358–392 ms." 그래서 관찰을 한 CPU model로 묶고, machine gate를 공유 도구에 넣고, 반복 횟수를 안정성 기준으로 정하기로 했습니다. 이때 3.7절에서 본 문장이 나옵니다. "The number of repeats is no longer the inherited five — the task 2.6 spec §3 states 'N=5 matrix' without a ground." 방법의 출처로는 Georges et al.(OOPSLA 2007), Kalibera and Jones(ISMM 2013), Maricq et al.(OSDI 2018)을 들었습니다.

**9.6 D11(campaign을 처음부터 다시 돌린 결정, 2026-09-18).** D10은 기존의 EPYC 네 반복에 두 개씩 더하는 안이었습니다. D11은 그것도 버렸습니다. "nothing of `meas-ci:build:35215328887` is used as data — its EPYC 7763 repeats are not pooled and its Xeon 8573C repeat is no longer D10's cross-machine check — and its four EPYC 7763 repeats set only the starting count." 새 campaign은 여섯 반복으로 시작해서 기준이 성립할 때까지 하나씩 더했습니다. 상한은 없앴습니다. EPYC 7763을 고른 이유는 "the most frequent model in the project's recorded draws: 26 of 56 jobs"였습니다. campaign의 tag는 `meas-ci:build:2026-09-18`입니다.

**9.6 D16(tracker rescan에 별도 entry를 주려던 D12–D15를 철회한 결정, 2026-09-19).** D12–D15는 tracker의 전체 rescan을 `cpu-batch`에서 빼서 `indexer-rescan`이라는 entry로 만들려 했습니다. 근거는 포화도 0.26–0.34였습니다. 그런데 그 포화도는 harness의 정지 규칙이 정한 수명으로 CPU를 나눈 값이었습니다. job 자체로 다시 계산하니 "saturation 0.954–0.962"였고, block-I/O 비율(0.05–0.80)은 "an exit-accounting artefact"였습니다. 그래서 네 결정을 모두 철회하고 tracker는 `cpu-batch`에 남았습니다. 이 tracker는 2026-10-02/03에 9.10이 실제 첫 색인을 측정한 `file-indexer`로 다시 바꿉니다.

**9.6 D19(object job을 frozen 형식 안에서 쓴 결정, 2026-09-19).** D9는 "spawn-table entry 하나가 compile 때 object job의 member task들로 펼쳐진다"고 했습니다. D19는 이것을 바로잡았습니다. "the workload format lets only a top-level task create tasks, one per spawn-table entry … a spawned child has no spawn table of its own, and the run file and visible projection are frozen." 그래서 "each object job is six consecutive spawn-table entries of `build-orchestrator` — `sh`, `gcc`, `cc1`, `as`, `fixdep`, `rm` — forked together after one dispatch run; `sh` runs first and the others wait on WAIT/WAKE channels, woken in the job's parent-child order." 그리고 `fork_cap`(orchestrator가 동시에 살려 둘 수 있는 자식 task 수의 상한)은 timeline의 `parallelism_cap`(make의 `-j` 값, 즉 동시에 도는 job 수) × 6이 됩니다.

> **열린 자리.** 9.6 D19는 frozen 형식을 지키려고 이 모양을 골랐지만, 이 모양은 "자식이 자식을 깨우는" WAKE를 만듭니다. 2026-10-10 audit은 simulator의 loader(`simulator/src/sim.cpp:874-904`)가 WAKE의 target을 최상위 task에서만 찾기 때문에 `c1-compile`, `c7-compile`, `c3-workday`, `c4-compile`, `c6-dual`의 다섯 파일을 거부한다는 것을 찾았습니다. schema는 어떤 task id든 target으로 허용하지만, contract의 예시는 최상위 target만 보여 줍니다. 인경민의 2026-10-10 memo는 해결 방향("One mailbox: keep the task mailbox; the loader reads the wake's `target`")을 "Implementation owed"에 넣었습니다. 고치는 일은 인경민의 것이고, 9.15의 최종 memo가 이것을 알립니다(12장).

**9.6 D31(fold-in, 2026-09-20).** 세 entry가 campaign `meas-ci:build:2026-09-18`의 값을 갖게 되었고, raw 기록은 release `meas-ci-build-2026-09-18`입니다(D18). 그 뒤 D32–D38은 문장을 측정에 맞게 좁히고 오래된 숫자를 고친 결정입니다. 예를 들어 D32는 `python3` binding을 "training-loop stand-in"이라고 부르는 문장을 좁혔고, 이 문제는 9.10 D12(PyTorch의 MNIST 예제를 실제로 측정한 결정)가 근본적으로 풉니다.

## 7.7 9.7 — background와 IO: 프로그램마다 하나씩 (2026-09-19 → 10-01)

9.7은 D1부터 D41까지입니다. 대상은 `io-stream`, `network-bulk`, `background-crawler`였습니다.

**9.7 D1(`io-stream`과 `network-bulk`를 묶인 프로그램별로 나눈 결정, 2026-09-19).** 두 entry가 묶인 프로그램은 `borg`(백업), `7z`(압축), Steam의 depot 다운로드, Thunderbird의 메일 전송이었습니다. 그런데 측정은 `rsync`와 `wget`으로 했었습니다. D1의 근거는 프로그램들의 구조가 서로 다르다는 것입니다. 예를 들어 "borg is one process with no worker threads, cutting 512 KiB–8 MiB content-defined chunks … against rsync's three pipe-connected processes"이고, Steam client는 약 1 MB의 암호화·압축된 chunk를 받아 풀고 패치하는데 "against wget's one process, one thread, one connection"이었습니다. 그래서 9.5 D2가 `desktop-interactive`에 준 것과 같은 모양으로 프로그램마다 entry 하나를 주었습니다.

**9.7 D3(Thunderbird의 send를 `mail-client`의 operation으로 한 결정, 2026-09-19).** D1의 수정입니다. 이유는 "the send runs inside the Thunderbird process — its SMTP client is a JavaScript module of the application … a separate send task would put a second `thunderbird` task in c1-mail, c7-mail and c3-workday and either count Thunderbird's background twice or rest on a subtraction no observation backs." 그래서 Thunderbird를 send operation과 함께 통째로 다시 관찰했습니다. 이 결정이 9.5에 Thunderbird의 재측정을 넘겼고, 9.5 D31–D46의 `send` campaign이 되었습니다.

**9.7 D5(`background-crawler`를 은퇴시킨 결정, 2026-09-19).** 이 entry는 critical finding B7에서 "bound nowhere"로 지적받았습니다. D5의 근거는 넷입니다. 첫째, "no timeline binds it … so it covers no driver-table cell and compiles into no workload." 둘째, 이 entry가 섬긴다던 scenario는 다른 entry로 이미 실현되어 있었습니다. 셋째, 값 자체가 "an idle miner's housekeeping wakes from a run that never indexed the corpus (X7) multiplied by `updatedb.plocate`'s duty, a different program"이었습니다. 넷째, 평소 색인기의 wake 주기를 관찰한 자료가 네 종류 어디에도 없었고, 그 정상 상태는 파일 변경 알림에 따라 움직여서 "a measurement would carry a designed stimulus"였습니다. 제거 전후로 다시 build해서 compile report가 같음을 확인했습니다.

**9.7 D11, D25(다운로드 속도와 link 모델).** SteamCMD(Valve가 배포하는 Steam의 명령줄 client) 다운로드는 소비자 수준의 속도로 제한해서 측정했습니다. 속도는 "121.0 Mbps, the byte-weighted median of Valve's per-country download rates"입니다(D11). 처음에는 token bucket(`tbf`)으로 제한했는데, 사전 등록한 진단에서 runner 간 변동계수가 약 20 %였고, `htb`와 `fq_codel`로 바꾸자 약 2 %로 떨어졌습니다(D24–D25). bucket의 결과는 link 모델의 민감도로 남겼습니다.

**9.7 D21(wake를 switch-out 상태로 판정하는 결정, 2026-09-19).** 9.5 D21(공유 측정 도구의 wake 정의 구현)은 이전 switch-out의 1 µs 앞부터 wakeup 기록을 찾는 창을 썼습니다. 9.7 D21은 이것을 task가 직전에 CPU를 내려놓을 때의 상태(스스로 잠들었나, 선점되었나)로 판정하도록 고쳤고, 모든 campaign에 적용했습니다. 기록된 근거는 kernel의 동작입니다. `sched_waking`은 잠든 thread에만 발생하고 scheduler가 그 thread를 내려놓기 전에 찍히므로, "on a wait of microseconds the row precedes the sleeper's own recorded switch-out." 그 결과 옛 창은 9.7의 dry run에서 "folded 1,458 of `borg`'s 3,204 uninterruptible sleeps of the warm full-set backup into the preceding wake"였습니다.

**fold-in.** `file-backup`(borg)과 `file-archiver`(7z)가 2026-09-22에 `io-stream`을 대체했고(D31), `game-download`(SteamCMD)가 2026-09-23에 들어와 `c2-p2a`의 다운로드가 다시 묶였습니다(D34). `network-bulk`는 Thunderbird의 send task 셋 때문에 남아 있다가(D30), 9.10 D13(메일 send를 operation으로 두고 `network-bulk`를 library에서 뺀 결정)으로 사라졌습니다. raw 기록은 release `meas-ci-background-2026-09-19`입니다.

`file-backup`은 오래 살지 못했습니다. 9.10 D8과 D119/D125(정기 백업을 Déjà Dup의 incremental로 바꾸고 `file-backup`을 은퇴시킨 결정)로 2026-10-04에 빠졌습니다. 9.7이 남긴 entry 중 지금도 있는 것은 `file-archiver`와 `game-download`입니다.

## 7.8 9.8 — browser와 comms: 측정값이 어떤 process도 그리지 않았다 (2026-09-20 → 09-28)

9.8은 D1부터 D38까지입니다. 대상은 `electron-comms`였습니다.

**9.8 D1(`electron-comms`를 묶인 프로그램별로 나눈 결정, 2026-09-20).** 이 entry는 core set 전체에서 task 125개를 가졌습니다(`chrome` renderer 102, `steamwebhelper` 9, `steam` 6, `thunderbird` 3, `discord` 3, `zoom` 2). 그런데 그 두 값은 관찰된 어떤 process도 그리지 않았습니다. "`heartbeat.median_us` 1 850 000 being the geometric centre between the Element main process (wake gap 0.40–0.43 s) and its GPU and network-service helpers (3.84–3.92 s) … and no process waking near 1.85 s." 두 집단의 기하 중심이어서, 실제로 1.85초마다 깨어나는 process는 없었다는 것입니다.

나눈 결과 네 entry가 생겼습니다. `renderer-hidden`, `renderer-visible`(보이지 않는/보이는 Chrome renderer), `chat-client`(Element), `game-client`(Steam client)입니다. 2026-09-22에 fold-in되었습니다(D25). `renderer-visible`은 9.10 D16("브라우저 창은 하나"라는 결정)으로 2026-10-01에 빠집니다.

**9.8 D6(Steam 계정을 쓰지 않은 결정, 2026-09-20).** `steam`은 자기 entry를 가지되 "measured on the desktop client run logged out on the runner"입니다. TODO는 이것을 "no Steam account used (D6)"이라고 요약합니다.

**9.8 D30 → D33(한 번 정한 처리를 철회한 사례).** Steam client의 `CHTTPClientThre` thread는 반복마다 run 평균이 두 무리로 갈렸습니다(8번은 0.0137–0.0170 ms, 4번은 0.0572–0.0639 ms). 2026-09-26의 D30은 이것을 "session 사이의 변동"(9.5 D57의 예외)으로 실었습니다. 2026-09-28의 D33은 반복마다 50 s 창으로 다시 읽어 보고 그것을 철회했습니다. "Read per repeat in 50 s windows, the upper mode is one burst: in each of repeats 4, 5, 6 and 12, 12–18 runs of 2.0–50.2 ms within 1.8–2.8 s … It is a rare event within a run, 9.5 D64's class (`chrome`'s `MemoryInfra` pass), not a spread between sessions." 그래서 1 ms 이상의 run은 component에서 빼서 `heavy_events`로 따로 실었습니다.

- **component**는 측정된 archetype 안에서 thread 종류 하나(같은 역할과 이름)의 wake 간격과 run 길이 분포입니다. 9.5 D16(timer wake를 thread 종류마다 component 하나로 두고 compile 때 합치는 결정) 이후 측정된 entry는 component들의 합으로 compile됩니다.

> **왜 이렇게 정했나.** D30과 D33의 차이는 "같은 현상을 어떤 시간 해상도로 읽었나"입니다. 반복 전체의 평균으로 보면 두 무리로 갈린 값이 session마다 다른 상태처럼 보였고, 반복 안을 50 s 창으로 쪼개 보니 몇 초짜리 burst 하나가 평균을 끌어올린 것이었습니다. 이 결정은 2026-09-28 검토가 요청한 "carried phases read in time windows"의 결과입니다(9.8 D33–D34, 2026-09-28).

## 7.9 9.9 — daemon과 session process: 꺼져 있다고 읽었다가 되돌리다 (2026-09-22 → 10-01)

9.9는 D1부터 D48까지입니다. 대상은 `system-daemon`이었습니다.

**9.9 D1(`system-daemon`을 system service와 session process로 나눈 결정, 2026-09-22).** critical finding B6이 지적한 대로, `gnome-shell`, `Xorg`, `pipewire`가 server daemon의 값에 묶여 있었습니다. D1의 근거는 "the two populations differ in every class searched"입니다. 예를 들어 system service는 고정 timer나 사건에 깨어나지만(cron 60 s, multipathd 5 s), Mutter(GNOME Shell의 compositor)의 frame clock은 그릴 것이 없으면 쉬고, PipeWire(오디오 서버)는 WirePlumber(PipeWire의 session manager)가 idle node를 5초 뒤 멈추면 tick을 멈춥니다. 결과로 네 entry가 생겼습니다. `compositor-shell`(GNOME Shell 46), `audio-server`(PipeWire stack), `service-manager`(`systemd`), `message-bus`(`dbus-daemon`)입니다. 관찰은 runner에서 띄운 idle Ubuntu 24.04 desktop session 하나였습니다(D8, D9).

**9.9 D26(fold-in, 2026-09-24).** 네 entry가 `system-daemon`을 대체했고, `c1-idle`과 `c7-idle`이 다시 묶였고, `xorg` task는 은퇴했습니다. raw 기록은 release `meas-ci-session-2026-09-24`입니다.

**9.9 D32 → D47(되돌린 결정).** 이 slice에서 가장 눈에 띄는 뒤집기입니다.

2026-09-25의 D32는 sysstat(시스템 통계를 주기적으로 모으는 package)의 수집 job을 "관찰된 데스크톱 밖"이라고 보고 pool에서 뺐습니다. 이 job은 큰 몫이었습니다. "277 of `audio-server`'s 402 kept wakes (69 %, WirePlumber's worker reacting to the collector's file writes), 361 of `message-bus`'s 609 (59 %)." 근거는 Debian의 sysstat package가 `sysstat/enable`을 기본 false로 두고 postinst가 timer를 끈다는 것이었습니다. "A stock desktop install therefore has the package and runs none of its jobs; the runner image enabled them."

2026-10-01의 D47이 이것을 되돌렸습니다. postinst는 package를 설치한 뒤 도는 script입니다. "The postinst does so only where systemd runs — `manage_systemd_services` returns unless `[ -d /run/systemd/system ]` — while `debian/rules` calls `dh_installsystemd` without `--no-enable`, so the units are enabled first." 그리고 결정적인 사실로 "A desktop image is built with no systemd running"을 확인했습니다. 실제 24.04.5.1 desktop image의 기본 설치 층을 ISO에서 range request로 읽어 보니 sysstat의 timer들이 켜져 있었습니다. "A stock install therefore runs sysstat's jobs, as the runner image did." 그래서 D32를 되돌리고 수집 job을 다시 데스크톱의 job으로 실었습니다.

> **왜 이렇게 정했나.** D47의 근거는 "설치 스크립트가 실제로 어떤 조건에서 무엇을 하는가"를 끝까지 읽은 것입니다. D32는 package의 기본값과 postinst의 의도를 읽었고, D47은 postinst가 systemd가 돌 때만 동작한다는 조건과, desktop image가 systemd 없이 만들어진다는 사실을 더 읽었습니다. 이 발견은 2026-09-29의 9.5–9.9 요약 읽기에서 나왔습니다(9.9 D47, 2026-10-01).

## 7.10 9.10 — scenario와 timeline: 모든 대역 job을 관찰한 job으로 (2026-10-01 → 10-07)

9.10은 D1부터 D174까지, Phase 9에서 가장 큰 slice입니다. stage 3의 결정 D1–D35가 2026-10-01에 나왔고, D36부터는 그 결정이 만든 campaign들입니다. 이 slice만 task spec(`_dev/docs/spec/jioh/task-9.10-scenarios-timelines.md`)을 따로 가집니다. 이 slice가 core set의 51개 timeline의 내용을 지금의 모습으로 만들었습니다.

### 7.10.1 무엇이 design이고 무엇이 현실 주장인가

**9.10 D1(닿을 수 없는 출처를 버린 결정).** "A reference or work whose copy is unreachable or paywalled is dropped; `zhang-chb15` leaves the registry." 기록된 사유는 "no reachable copy: closed access, ScienceDirect 403, Elsevier API 429"입니다. 2026-08-26 grill D17이 "약 3분 전환"의 독립적 뒷받침으로 들었던 출처가 이렇게 빠졌습니다.

**9.10 D2(core set의 task 집합은 design이라는 결정).** "which programs share a segment of a core-set file is the experiment's composition, chosen for the claim the file makes, and is labelled design (phase decision 3). No core-set file presents its task set as how desktops behave." 근거는 building plan이 core set을 "one file per claim"으로 짓는다는 것과, 검색이 "no observation of which programs run together on Linux desktops"를 찾았다는 것입니다. 대신 현실 주장으로 남는 것을 명시했습니다. 각 프로그램이 그 이름으로 Ubuntu 24.04에 존재하는 것, 파일이 "일어나는 일"로 보여 주는 상황, 묶인 entry의 상태가 파일이 그리는 상태와 맞는 것, 그리고 개수입니다.

이 구분이 9.10의 나머지 결정을 이끕니다. "상황이 실제로 일어난다"는 주장은 관찰이 필요하므로, 그때까지 쓰던 대역(stand-in) job들을 하나씩 실제 관찰로 바꿨습니다.

### 7.10.2 대역 job을 관찰한 job으로

아래 일곱 결정이 core set의 batch job과 "원치 않는 작업"을 모두 바꿨습니다.

**9.10 D3(원치 않는 백신 검사를 stock 무인 업그레이드로 바꾼 결정).** C7의 interactive counterpart 열 개와 `c2-p2b`에 넣던 `clamscan`이 Ubuntu 24.04의 stock 무인 업그레이드로 바뀌었습니다. 근거의 첫째는 검사의 전제가 무너졌다는 것입니다. ClamAV의 문서는 스스로를 "ClamAV is not a traditional anti-virus or endpoint security suite"라고 하고, 예약 검사는 endpoint suite의 기능이라고 적으며, 검사한 ClamAV package 어디에도 예약 검사가 없었습니다. 데스크톱에서 예약 `clamscan`이 생기는 길은 ClamTk뿐인데 ClamTk는 "is no longer maintained"이고 Debian popcon에서 0.11 %였습니다. 둘째는 대체물의 존재입니다. `unattended-upgrades`는 stock 데스크톱의 기본 층에 있고 기본으로 켜져 있으며 매일 돕니다. campaign은 2026-07-27 하루치 보안 업데이트(`glibc`)를 Ubuntu의 snapshot service로 재구성해 측정했고(D36–D38), 새 entry `package-upgrade`가 되었고, task 이름은 `unattended-upgr`입니다(D39–D40). 2026-10-01에 아홉 반복으로 fold-in되었습니다(D45).

**9.10 D4(`c7-compile`의 job을 실제 DKMS 재빌드로 바꾼 결정).** Phase 7 7.3의 "`make`를 `dkms`로 이름만 바꾸기"가 실제 관찰로 바뀌었습니다. NVIDIA의 open kernel module(`nvidia-dkms-595-open`)을 2026-09-23의 보안 kernel(`7.0.0-31` → `7.0.0-34`)에 대해 무인 업그레이드가 재빌드하는 과정을 측정했습니다(D46–D51). 새 entry 두 개 `module-build-orchestrator`, `module-compiler-child`가 생겼고, 26번의 landing으로 2026-10-02에 fold-in되었습니다(D59).

- **DKMS**(Dynamic Kernel Module Support)는 kernel이 업데이트될 때 외부 kernel module(예: 그래픽 드라이버)을 새 kernel에 맞게 다시 compile하는 Ubuntu와 Debian의 장치입니다.
- **kernel module**은 실행 중인 kernel에 끼워 넣는 코드 조각입니다. 장치 드라이버가 대표적입니다.

**9.10 D5(색인 파일을 Tracker의 실제 첫 색인으로 바꾼 결정).** `c1-indexing`, `c7-indexing`, `c2-p1b`는 `cpu-batch`의 tracker rescan 표를 쓰고 있었습니다. 이것이 빈 database에서 집 같은 파일 집합을 처음 색인하는 Tracker 3.7.1로 바뀌었습니다. 파일 집합은 처음에 "a real user's file set"을 찾았지만, D60과 D66이 그것을 고쳤습니다. TODO의 요약은 "no real user's home is reachable under open terms, so the set is HippoCamp's aggregated profile"입니다. 색인 대상은 HippoCamp의 Bei profile이고, 새 entry `file-indexer`가 생겼고, task 이름은 `tracker-miner-f`입니다(D70, D74). 2026-10-03에 열여덟 반복으로 fold-in되었습니다(D81).

**9.10 D8(정기 백업을 Déjà Dup의 incremental로 바꾼 결정).** borg의 첫 백업(`file-backup`) 대신 Déjà Dup 45.2가 스스로 시작하는 주간 incremental 백업을 측정했습니다. 새 entry `incremental-backup`이 생기고 `file-backup`은 은퇴했습니다(D119, D125). 2026-10-04에 서른 번 중 유효한 스물여덟 번으로 fold-in되었습니다.

**9.10 D10(render를 Kdenlive의 export로 바꾼 결정).** `cpu-batch`의 `ffmpeg` 표 대신 Kdenlive 23.08.5가 render dialog로 시작하는 export를 측정했고, `cpu-batch`에 새 program `kdenlive_render`가 생겼습니다(D105). 서른 반복입니다(D111).

**9.10 D11(transcode를 CpsMark+의 HandBrake workload로 바꾼 결정).** HandBrake 1.7.2의 기본 preset을 Big Buck Bunny 4K 영상 전체에 돌렸습니다. 여기에는 원문 읽기의 흥미로운 사례가 있습니다. CpsMark+ 논문은 "H.256"이라고 적었는데, 그것은 존재하지 않는 codec입니다. 9.10 D95는 benchmark 자신의 코드를 읽어 H.264로 정했습니다("the codec and target of CpsMark+'s own code against its paper's 'H.256'"). 새 entry `video-transcoder`, 다섯 반복입니다(D100).

**9.10 D12(ML 학습을 PyTorch의 기본 MNIST 예제로 바꾼 결정).** `python3` placeholder 학습이 PyTorch의 `main.py --save-model`(torch 2.14.0, CPU)로 바뀌었습니다. 측정 중에 runner의 huge page 모드가 데스크톱 kernel과 다르다는 것이 드러났고, 데스크톱의 `madvise` 모드에서는 "×1.144 the CPU"가 든다는 것을 다섯 job으로 확인해 적었습니다(D87, D88). 여섯 반복입니다(D90).

- **huge page**는 kernel이 메모리를 보통보다 큰 단위로 관리하는 방식입니다. 켜는 정책에 따라 같은 프로그램의 CPU 사용량이 달라질 수 있습니다.

> **왜 이렇게 정했나.** 일곱 개의 대역 job을 바꾼 공통의 이유는 9.10 D2가 남긴 현실 주장, 즉 "파일이 일어나는 일로 보여 주는 상황"입니다. 예를 들어 "사용자가 원치 않는 백신 검사가 돈다"는 상황은 stock 데스크톱에서 일어나지 않는다는 것이 ClamAV 자신의 문서로 드러났습니다(9.10 D3). 같은 기준으로 이름만 바꾼 DKMS, rescan 상태의 색인, 60 s짜리 백업도 각각 관찰한 job으로 바뀌었습니다(9.10 D3–D12, 2026-10-01 → 10-04).

### 7.10.3 크기: job을 통째로, 파일이 길이를 따라간다

**9.10 D17(batch job은 측정한 전체를 돌리고 파일이 길어진다는 결정).** "a batch job in a core-set file runs its measured whole, at the input its decision fixed … A file's and its segments' lengths follow the job. No `total_work` or `spawn_count` describes part of a job." 기록된 근거는 셋입니다.

- "A slice describes part of a job." 측정된 entry는 job 전체를 그리는데, 그보다 작은 `total_work`는 job의 일부를 그리고, 사용자의 job이 얼마나 큰지는 출처가 없습니다. 2026-09-13의 audit은 "`c1-backup`'s `borg` could not finish even alone in its 60 s file (132.2 s uncontended; J2)"를 찾았습니다.
- "File length is the design part." 파일 길이는 Phase 9 결정 3에 따라 design이므로, 길이를 바꾸는 것은 이미 design인 것만 바꾸는 일입니다.
- "The inputs keep their grounding." 파일 길이에 맞추려고 입력을 줄이면, 근거 있는 입력이 design으로 바뀝니다.

이 결정으로 9.6 D7과 9.7 D13의 "`total_work` stays timeline design"이 물러났습니다.

**9.10 D18과 D141(사용자의 kernel build를 통째로 묶은 결정).** D18은 사용자의 build를 9.6이 측정한 kernel build 전체로 정했습니다. 2,908개 object job, cap 8입니다. D141은 2026-10-05에 그 길이를 적용했습니다. 각 파일은 "the smallest whole second by which the build ends under every policy"로 길어졌습니다. `c1-compile`은 1,594 s, `c3-workday`의 compile segment는 120–1,485 s, `c6-dual`은 12,072 s가 되었습니다. Phase 2의 `c1-compile`이 60 s에 `cc1` 자식 100개였던 것과 비교하면 모양이 완전히 바뀌었습니다.

**9.10 D41(interactive counterpart는 job의 CPU 총량만큼 긴 segment 하나라는 결정).** 열 개의 interactive counterpart는 base의 처음 C초가 되고, C는 `package-upgrade` job의 CPU 총량입니다. 이유는 "On one lane a job of C seconds of CPU is alive for at least C seconds under every policy, so the job is present throughout a segment of length C." 60 s 파일에 job을 넣으면 "some policies end it 13–34 s before the segment ends in nine of the ten files"가 되어 label이 틀린 구간이 생깁니다. C는 fold-in 때 26.385 s로 정해졌습니다(D45).

**9.10 D44(잘린 counterpart의 시간 배치를 비례로 유지하는 규칙).** counterpart를 C초로 자르면 base의 operation(30 s나 40 s에 있던)이 잘려 나갑니다. D44는 focus 창을 2 s부터 C − 2 s로 두고, 각 operation을 base에서와 같은 비율의 지점에 두기로 했습니다. 예를 들어 `c7-mail`의 send는 창의 0.679 지점입니다. 이 규칙이 무엇을 정하지 않았는지가 나중에 문제가 됩니다. 키 입력 stream을 어디서 자르는지는 정하지 않았고, 2026-10-10 audit의 A1이 그것을 찾습니다(9장).

### 7.10.4 브라우저, 게임, 이름, 실행 시작

**9.10 D15와 D127(Chrome의 renderer 개수).** 브라우저 파일마다 placeholder였던 renderer 개수(11, 7, 7, 9, 5)를 관찰로 바꿨습니다. D15는 두 단계로 정했습니다. tab 개수는 Firefox의 Linux telemetry(GLAM, 7,535,303 client)의 "median per-client peak of concurrent tabs" 4.67에서 다섯 tab으로, renderer 개수는 그 tab 집합을 runner의 Chrome에 열고 관찰한 수로 합니다. D127(2026-10-04)은 D15를 고쳤습니다. D15는 "the spare included if one shows"라고 했는데, spare renderer와 Chrome 자신의 renderer는 이미 `web-browser`가 갖고 있어서 두 번 세게 된다는 이유로 빼기로 했습니다. 관찰 결과는 다섯 반복 모두 "4 page renderers beyond the page in use and 1 spare"였고, Chrome 파일 열 개가 `renderer-hidden` task 넷씩을 갖게 되었습니다(D131).

- **renderer**는 Chrome이 웹 페이지를 그리기 위해 띄우는 별도 process입니다. 대체로 site마다 하나입니다.

**9.10 D16(브라우저 창은 하나라는 결정).** `renderer-visible` task가 파일과 library에서 빠졌습니다.

**9.10 D19(gaming 파일은 game chain만 갖는다는 결정).** 게임의 다른 thread는 생략하고 그 사실을 적습니다. 그리고 D24로 `gamescope`가 gaming 파일에서 빠졌습니다. Phase 5가 읽었던 "`c1-gaming` compositor 0.40 of the lane"이 사라진 것입니다.

**9.10 D24와 D25(이름은 관찰한 프로그램의 `comm`).** `zoom`은 `chrome`으로, `spotify`는 `mpv`로, `discord`는 `element-desktop`으로 바뀌었습니다(D24). 그리고 이름은 kernel의 `comm`이므로 15바이트로 잘립니다. `tracker-miner-fs-3`는 `tracker-miner-f`, `thunderbird`는 `thunderbird-bin`이 되었습니다(D25). **9.10 D26**은 game chain의 member 이름을 LAVD 슬라이드 16의 이름(`Troy.exe` 등)으로 바꿨습니다. `game.exe`가 사라졌습니다.

**9.10 D21(파일 중간에 시작하는 프로그램은 관찰한 시작 phase부터 돈다는 결정).** 9.5의 trace에서 시작 직후의 일이 크고 정해진 지점에 나타난다는 것이 보였습니다. 예를 들어 Chrome은 idle phase의 20–40 s에 burst가 있었습니다. 그래서 시작 phase를 따로 측정해서, 파일 중간에 프로그램을 시작하는 `c3-workday`, `c3-evening`, `c3-creation`, `c4-compile`, `c4-gaming`, `c6-fold`가 그것을 재생하게 했습니다(D132–D140). 열 entry가 `launch`를 갖고, stream은 `dataset/launch/`에 있습니다.

**9.10 D143 이후(span probe).** 파일이 entry의 관찰 구간보다 길게 entry를 잡고 있는 경우, 그 길이만큼 다시 재 보고 나서야 그 길이를 인정하기로 했습니다(D143). 그 결과 `video-editor`의 idle phase와 `renderer-hidden`은 다시 측정되었습니다(D146, D152).

### 7.10.5 bound value의 출처

**9.10 D32(timeline에 묶인 값도 library의 규칙을 따른다는 결정).** "each value a timeline binds carries `source: <id>:<locator>` or a label for what it is (design, convention, arithmetic), checked by the linter." 근거는 "The provenance claim covers only the library today"였습니다. 그리고 "9.10 sets the content; the field and the lint are a schema change, 9.13's." 즉 내용은 9.10이 정하고, 필드와 lint는 9.13(rebuild)이 넣기로 했습니다. 9.10 D160(2026-10-06)은 그 내용을 `bound-values.md`에 목록으로 만들었습니다.

9.13은 이 필드를 넣지 않았습니다. 2026-10-10 audit의 A2가 이것을 찾았고("9.10 D32 decided `source:`/label on every bound value with a lint, 'the field and the lint are 9.13's'; `timeline.py` has no source slot"), 2026-10-11에 9.18 D2가 넣었습니다(10장). 2026-10-14에 이 권은 이 빈틈이 생긴 이유가 기록에 없다고 적었습니다. 2026-10-16에 인지오가 그것을 "놓친 인계"로 기록하기로 정했습니다(9.15 작업 목록 W-0740). 9.10 D32가 필드와 lint를 9.13에 넘겼는데 9.13의 spec이 그것을 받지 않았고, audit이 잡았습니다.

## 7.11 9.11 — scheduler 쪽의 상수와 근거 (2026-10-07 → 10-08)

9.11은 D1부터 D34까지입니다. 데이터셋 자체보다 simulator와 harness의 상수를 다뤘지만, 두 결정이 데이터셋의 형식을 바꿨습니다.

**9.11 D3(TIMER는 놓친 tick을 건너뛴다는 결정, 2026-10-07).** 그전까지 interpretation contract는 TIMER task가 늦으면 놓친 tick을 연달아 따라잡는다고 적었습니다(backlog 규칙). D3는 이것을 skip 규칙으로 바꿨습니다. 늦게 TIMER에 도달하면 가장 최근의 지난 tick 하나만 바로 소비하고 그 이전의 tick은 건너뛰며, 건너뛴 tick은 마감을 놓친 job으로 셉니다. 근거는 "every program and periodic framework found skips; only rt-app's non-default mode catches up"입니다. 이 결정은 memo(`docs/memos/2026-10-07-timer-skip-rule-for-the-simulator.md`)로 인경민에게 갔습니다.

- **tick**은 TIMER의 주기 격자 위의 한 시점(t₀ + k·P)입니다. **backlog 규칙**은 놓친 tick을 모두 차례로 처리하는 규칙이고, **skip 규칙**은 놓친 tick을 건너뛰고 마감 실패로 세는 규칙입니다.

**9.11 D4–D6(프로그램이 선언한 scheduling class를 존중한다는 결정, 2026-10-07).** "Background programs declare their class themselves, and a stock Linux kernel acts on it." 예를 들어 Tracker는 시작할 때마다 스스로를 `SCHED_IDLE`, nice 19로 설정하고, Déjà Dup은 backend를 `chrt --idle 0`으로 돌립니다. 그래서 task model에 declared-class 필드를 더하고, executor가 class마다 규칙 하나로 그것을 존중하기로 했습니다(D4). idle class는 다른 class의 task가 없을 때만 돕니다(D5). 필드는 nice가 아니라 policy만 담습니다(D6). 이유는 "Nice is a weight within the normal class, not a class … of the simulated algorithms only LOTTERY has a weight to carry it."

- **scheduling class(policy)**는 Linux가 process마다 붙이는 scheduling 종류입니다. 보통은 `SCHED_OTHER`(normal)이고, `SCHED_IDLE`은 다른 일이 없을 때만 CPU를 받는 가장 낮은 종류입니다.
- **nice**는 normal class 안에서의 가중치입니다. 값이 클수록 CPU를 덜 받습니다(-20부터 19).

이 필드는 세 frozen contract(archetype, workload, run file)를 바꾸므로 세 사람의 합의가 필요했습니다. D18은 그 요청을 memo(`docs/memos/2026-10-08-declared-scheduling-class.md`)로 보냈고, 합의가 2026-10-09에 기록되었습니다.

**9.11 D7 → D19(starvation 하한).** D7은 starvation 하한을 1초에서 30초로 바꾸고 sched_ext의 watchdog을 출처로 들었습니다. D19(2026-10-08)는 그것을 design으로 다시 label하고, "executor의 안전망"이라는 약속을 문서에서 지웠습니다.

**9.11 D15(C2 pair guard).** P1 쌍이 `fixed` 조건에서 더 이상 동일하지 않다는 것을 찾았습니다. 그대로 두었다면 "every RQ0 run set would otherwise have been invalid"였습니다. 이것은 9.14의 guard spec 1.1로 이어집니다.

**9.11 D21(`c2-p2a`의 bounding check).** SteamCMD의 일부 work가 nice 10으로 돈다는 한계를 재기 위해, 같은 표에 class만 `idle`로 바꾼 variant entry와 variant 파일을 만들기로 했습니다. 이것이 9.13의 `game-download-idle`과 `c2-p2a-idle`이 됩니다.

**9.11 D33(I/O class 필드는 없음).** "the simulator schedules one CPU lane"이므로 색인기와 백업의 idle I/O class는 싣지 않습니다.

## 7.12 9.12 — related-work와 제안서의 문장 (2026-10-08 → 10-09)

9.12는 D1부터 D116까지입니다. 대부분 데이터셋 밖, 즉 related-work와 연구 제안서의 문장을 원문에 맞게 고친 결정입니다. 데이터셋과 닿는 것만 적습니다.

- **9.12 D6.** `whitelist` 조건이 둘로 나뉩니다. 배포된 catalogue(`shipped_catalogue`)와 가장 강한 이름 표(`strongest_name_table`)입니다. 9.14의 guard spec이 이것을 모든 frozen 목록에 반영했습니다.
- **9.12 D110.** 노트북에서 잰 측정에 `meas-local`이라는 registry 형식이 생겼습니다(`meas-local:m1pro-llm:2026-10-08`).
- **9.12 D113.** 발표, 학회 초록, 뉴스 기사를 위한 id 유형이 생겼습니다. "footnote tier, their claims the speaker's or reporter's." 2026-10-10 audit의 A3는 `lavd-ossna24`가 아직 이 유형으로 바뀌지 않았다고 지적합니다. 2026-10-15에 인지오가 re-type하기로 정했고(9.15 작업 목록 W-0072), `docs/references.md`의 entry는 talk·학회 초록·뉴스 기사의 절로 옮겨져 숫자를 "Min's reported figures of 2024-04-17"로 적습니다. 값과 data 파일은 바뀌지 않았고, `dataset/sources.yaml`의 registry는 이 id를 여전히 `type: deployed-system`으로 둡니다(이 `type`은 lint하지 않습니다).
- **9.12 D55–D116(audit).** slice 자신의 audit이 D30–D53의 대부분을 고쳤습니다. 예를 들어 D61은 D41을 뒤집었습니다. "the indexer does *not* leave a third idle — 88–91 % busy once indexing."

## 7.13 이 구간의 중간 점검들

slice들이 도는 동안 세 번의 점검이 있었습니다.

**2026-09-20 dataset validity review.** memo(`docs/memos/2026-09-20-dataset-validity-review.md`)의 판정은 "**sound for the recognition claim, bounded for the scheduling-benefit claim.**"이었습니다. recognizer는 "reads identity, not timing"이므로 인식 주장은 측정의 미세한 정확도가 아니라 compile의 결정성에 기대고, scheduling 이득의 주장은 측정에 기댄다는 것입니다. 권고는 안정성 ledger를 공개하고, demand window를 "scoping decision"으로 밝히라는 것이었습니다. 이 memo는 "a file outside it is redesigned rather than waved through"라고 적는데, 이 문장은 2026-10-09에 9.14 결정 4로 사실이 아니게 됩니다. 또 이 memo의 "Untouched" 절은 `zhang-chb15`를 인용하는데, 그 출처는 2026-10-01에 빠졌습니다. 둘 다 9.15가 다룰 낡은 문장입니다.

**2026-09-26 review of 9.5–9.9.** 이 검토가 두 가지를 낳았습니다. 하나는 untraced control(7.5절)이고, 다른 하나는 타당성 위협의 문장입니다. TODO의 9.15 줄이 그것을 적습니다. "the compiled wake streams reproduce each component's rate, gap and run distributions, not the order of its gaps nor its components waking together." 측정값으로 비교한 결과도 붙어 있습니다. 1–100 ms 창의 wake 개수 분산이 측정에서 compile된 것보다 `chat-client`는 3.3–11배, `code-editor`는 2.6–3.4배 컸습니다. 그리고 Phase 10에 trace-replay 점검이 생겼습니다(12장).

**2026-09-28 coverage sweep.** 9.5–9.9의 아홉 finding이 모두 닫혔습니다. 닫은 것은 각 slice의 정정 결정들(문장과 guard를 code와 기록에 맞춘 9.5 D90–D95, 9.7 D39, 9.8 D37–D38, 9.9 D44)입니다. TODO는 "9.5–9.9 are closed, and a later review of them is this audit's"라고 적어, 이후의 재검토를 9.16에 맡깁니다.

## 7.14 2026-10-07 무렵의 archetype library

slice들이 끝났을 때 library는 스물여덟 개, 9.13이 하나를 더해 지금 스물아홉 개입니다. 어느 slice가 무엇을 만들었는지 정리합니다. 이 수는 `dataset/archetypes.yaml`의 `archetypes` 아래 key를 `python3.12`로 세어 확인했습니다(29개).

| 만든 slice | entry |
|---|---|
| 9.4 (Phase 2부터 남음) | `game-task-chain` |
| 9.5 | `office-writer`, `code-editor`, `mail-client`, `web-browser`, `image-editor`, `video-editor`, `video-player`, `audio-player`, `video-call` |
| 9.6 (Phase 2부터 남음, 값은 다시 측정) | `compiler-child`, `build-orchestrator`, `cpu-batch` |
| 9.7 | `file-archiver`, `game-download` |
| 9.8 | `renderer-hidden`, `chat-client`, `game-client` |
| 9.9 | `compositor-shell`, `audio-server`, `service-manager`, `message-bus` |
| 9.10 | `package-upgrade`, `module-build-orchestrator`, `module-compiler-child`, `file-indexer`, `incremental-backup`, `video-transcoder` |
| 9.13 | `game-download-idle` |

사라진 entry는 `desktop-interactive`, `audio-playback`, `video-playback`(9.5 D19), `background-crawler`(9.7 D5), `io-stream`(9.7 D31), `network-bulk`(9.10 D13), `electron-comms`(9.8 D25), `system-daemon`(9.9 D26), 그리고 잠시 있었던 `file-backup`(9.10 D125)과 `renderer-visible`(9.10 D16)입니다.

2026-10-10 audit은 이 library를 "29 entries, 28 measured on own campaigns with version, runner, instrument, repeats, stability rule; 6,953 leaf numerics 96.6 % measured"라고 적습니다. 측정하지 않은 하나는 LAVD 슬라이드에 기댄 `game-task-chain`입니다.

# 8장 · Phase 9 둘째 구간: 한 번의 rebuild와 한 번의 consumer rework

이 장은 "slice들의 결정이 어떻게 하나의 blessed 데이터셋이 되었고, 그 위의 채점과 판정 규칙은 어떻게 다시 정해졌나"라는 질문에 답합니다. 2026-10-09 하루에 9.13의 grill, rebuild, bless가 있었고, 같은 날 9.14의 grill이 열려 2026-10-10에 끝났습니다. Phase 9 spec 결정 6이 말한 "one rebuild"와 "one consumer rework"가 이것입니다. 그리고 이 구간에서 2026-08-26부터 있던 demand window가 gate에서 물러납니다.

## 8.1 9.13 — rebuild의 결정들 (2026-10-09 grill)

9.13의 spec(`_dev/docs/spec/jioh/task-9.13-rebuild.md`)은 자신을 "The one build of the workload dataset after the research slices 9.4–9.12: the structural changes the slices could not make as their decisions landed, then a single blessed single-lane set for 9.14 to re-pin"이라고 소개합니다. 범위 밖으로는 "any archetype value — the slices' values stand as applied"를 명시했습니다. 즉 9.13은 값을 정하지 않고, slice들이 값만으로는 할 수 없던 구조적 변경을 했습니다.

- **bless**는 build 결과를 "이것이 공식 데이터셋"이라고 정하고 그 manifest를 commit하는 일입니다.
- **pin**은 다른 파일(예: RQ0 gate spec)이 특정 manifest의 SHA-256을 적어 두어, 그 데이터셋 판에 묶이는 것입니다. **re-pin**은 그 hash를 새 판으로 바꾸는 일입니다.

**9.13 결정 1 — 합의 관문 없음.** "인경민 and 박이안 have agreed the contract change of the 2026-10-08 declared-scheduling-class memo. Throughout 9.13, 인지오 decides; the teammates are told in the phase's final memo."

**9.13 결정 2 / D2 — `declared_class`.** "Every task record — the top-level arrive event and every spawn-table entry — carries `declared_class`, required, from the closed set `normal` and `idle` … It is `idle` on `file-indexer` and `incremental-backup` and `normal` on every other entry. A task's class is its bound entry's, never one read from its name." 9.11 D4–D6(선언된 class를 존중하되 policy만 싣는 결정)을 형식으로 만든 것입니다. 마지막 문장의 뜻은 TODO가 예로 보여 줍니다. "a spoofed name changes no class (`c5-t3`'s `tracker-miner-f` and `baloo_file` on the media players stay normal)." 미디어 플레이어가 색인기 이름을 쓰고 있어도 class는 플레이어의 것입니다.

**9.13 결정 3 — visible projection도 class를 싣는다.** 이유는 "on the standing that a real machine exposes a process's class as it exposes its name"입니다.

**9.13 결정 4 / D4 — `game-download-idle`과 `c2-p2a-idle`.** 9.11 D21의 bounding check를 위해, `game-download`과 표를 공유하고 class만 `idle`인 entry와, `c2-p2a`에서 download task의 entry 하나만 바꾼 파일을 만들었습니다. "The two compiled files differ in that task's class and nowhere else." 이 파일은 judging set 밖에 있고 9.14의 bounding check만 읽습니다. 이것이 core set의 51번째 파일입니다.

**9.13 결정 5 / D1 — native compile mode를 compiler에서 뺌.** "`dataset/tools/wlc/compiler.py`: the mode list `("native", "single")` → `("single",)`; the lane-scaling pass is the only pass, and a request for `native` is refused." 2026-09-16의 9.5 follow-ups 결정 14가 이렇게 실현되었습니다. 2026-08-26 grill D16의 네 artifact가 하나로 줄었습니다.

**9.13 결정 8 / D3 — lint와 test 네 개.** TIMER-first invariant("a program that contains a TIMER anywhere has a TIMER as its first executed instruction"), library entry의 class, task record의 class, bounding pair의 byte 동일성입니다. TIMER-first의 이유는 TODO가 적습니다. "so TIMER's t₀, its first TIMER execution, is the task's arrival (D11, D33)." 9.13 reads R2는 TIMER를 가진 task 22개가 모두 통과한다는 것을 확인했습니다.

**9.13 결정 10 / D7 — bless와 window.** "The bless runs the dataset target with the compiler's existing allowance that reports demand-window violations as warnings and still writes. The nine violating files and their demands are recorded in the changelog as the state 9.14 inherits; the CI gate stays strict, red on the window until 9.14 redoes the rule."

## 8.2 9.13의 reads — rebuild 전에 읽은 사실들

9.13은 값을 바꾸지 않고 읽기만 한 것들을 `_dev/research/jioh/task-9.13-rebuild/reads.md`에 R1–R6으로 남겼습니다. 둘이 이후 이야기에 중요합니다.

**R4 — 크기와 wake 사건 수.** TODO의 9.13 줄에는 9.5 D74(측정된 timer wake마다 외부 wake 사건 하나를 만든 결정)의 2026-09-26 수치(531,740개, 84 MB)가 적혀 있었습니다. 다시 세어 보니 크게 달랐습니다.

| 양 | 2026-09-26 (9.5 D74) | 2026-10-09 |
|---|---|---|
| single-lane 파일 | 50 | 50 |
| 외부 wake 사건 | 531,740 | 4,496,190 |
| canonical bytes | 84 MB | 665,836,426 (666 MB) |

가장 큰 파일은 `c6-dual`(189.8 MB, 1,391,059 wake), `c1-transcode`(152.8 MB), `c7-transcode`(95.1 MB)였습니다. R4는 원인을 이렇게 적습니다. "The growth follows 9.10's bindings after D74 — the kernel build whole in `c6-dual` (12,072 s, D141), the transcode whole (4,762 s, D91–D100), four `renderer-hidden` tasks per Chrome file (D131), the launch replays (D140) — with every measured wake of every component carried as its own event (D74)." 즉 9.10 D17(job을 통째로)과 9.5 D74(측정된 wake마다 사건 하나)가 곱해진 결과입니다. 이 크기는 이후 build 시간(9.22 build time)과 harness의 시간과 메모리(9.14 D13의 aggregation 11시간, 9.21 D12의 test 메모리 7.66 GB)의 문제로 이어집니다.

**R5 — 오늘의 demand window.** compiler의 window 규칙("a single-lane file's demand in [1.00, 1.50] lanes unless its demand class is `calibration`")을 모든 파일에 적용했습니다. `oversubscribed` class 파일 열 개 중 아홉 개가 창 밖이었습니다.

| 파일 | 수요(lane) |
|---|---|
| `c2-p1a` | 14.51 |
| `c2-p2a` | 9.38 |
| `c6-dual` | 1.00 |
| `c2-p1b` | 0.92 |
| `c2-p3b` | 0.90 |
| `c3-evening` | 0.90 |
| `c3-creation` | 0.94 |
| `c3-workday` | 0.89 |
| `c2-p3a` | 0.44 |

원인도 적었습니다. "`c2-p1a`'s and `c2-p2a`'s demands follow the training run and the download bound whole at their CPU totals (9.10 D17, D90, D142) inside short files." 학습 job(1,389.885 s의 CPU)과 다운로드 job(727.170 s)을 통째로 묶었는데, 파일은 그 job이 끝나기 전에 끝나도록 짧게 두었기 때문입니다(9.10 D86, D142). 정적 추정치는 job의 전체 CPU를 파일 길이로 나누므로 14.5 lane 같은 숫자가 나옵니다.

## 8.3 9.13의 bless (2026-10-09)

9.13 D7이 bless의 기록입니다. "51 artifacts under `coreset-single/` alone … `dataset/coverage-grid.json` at 66 segments with all 32 cells instanced. 15:18:40 → 15:40:47 on the M1 Pro, 22 minutes, the schema validation most of it."

| 양 | blessed set |
|---|---|
| 파일 | 51 |
| canonical bytes | 680,806,752 (681 MB) |
| 외부 wake 사건 | 4,522,200 |
| 가장 큰 파일 | `c6-dual`, 190.3 MB, 1,391,059 wake |
| `idle` task를 가진 파일 | `c1-indexing`, `c7-indexing`, `c2-p1b`(`tracker-miner-f`), `c1-backup`, `c7-backup`, `c2-p3b`(`deja-dup`), `c2-p2a-idle`(`steam`) |
| window 경고 | 10 (R5의 아홉과 `c2-p2a-idle`) |

"`build/` stays uncommitted"입니다. 그리고 D7은 9.15에 최종 memo의 수치(681 MB, `c6-dual` 190 MB)를, 9.16에 "the full dataset lint with schema validation takes about 41 minutes and the bless 22 on this machine"을 넘겼습니다. 이 41분과 22분이 이틀 뒤 9.22의 출발점이 됩니다.

현재 tree가 이 수를 그대로 가지는지 확인했습니다. `dataset/build.manifest.json`의 `artifacts`는 51개이고, `dataset/timelines/coreset/`에는 timeline 51개와 recipe 다섯 개(`c2-pairs`, `c4`, `c5`, `c6`, `c7`의 `*.variant.yaml`)가 있고, `dataset/coverage-grid.json`의 `empty_cells`는 비어 있습니다. `segments_total`은 2026-10-14에 66이었고, 2026-10-17에는 67입니다. 9.23 D2(2026-10-14)가 `c6-spoof`의 segment를 spoof가 도착하는 20 s에서 둘로 나누었기 때문입니다(10.7).

## 8.4 9.14 — consumer rework의 결정들 (2026-10-09 grill, 2026-10-10 완료)

9.14의 spec(`_dev/docs/spec/jioh/task-9.14-consumer-rework.md`)은 "The one rework of what consumes the rebuilt workload dataset — the scoring spec, the guard spec, the prior driver table with its pair review, and the RQ0 gate spec — with one harness changelog entry and one re-pin"입니다. 9.4–9.13이 9.14에 넘긴 모든 hand-off가 범위였습니다. 결정 열네 개 중 데이터셋의 모양과 그 쓰임에 영향을 준 것을 봅니다.

**9.14 결정 1 — 모든 소비자는 지금의 simulator가 아니라 비준된 contract를 기준으로 쓴다.** "Primitives, mocks, fixtures, scoring statements, pair review and gate spec read the simulator as the docs state it: the TIMER skip rule (9.11 D3, D17), the zero-wait `ready` line, a cold start into MLFQ, a same-algorithm entry letting the granted slice finish, the batch bandwidth cap, the strict idle class, and the frame chain in EDF's deadline class." 그리고 gate spec에 conformance statement를 넣었습니다. 실제 simulator가 RQ0 실행 전에 이 행동들을 보여야 한다는 것입니다. 이 결정 때문에 harness와 simulator 사이에 "약속된 행동"과 "구현된 행동"의 차이가 생겼고, 그 차이가 지금의 열린 자리 중 하나입니다(12장).

- **conformance statement**는 RQ0 gate spec 안의 목록으로, 실제 simulator가 보여야 RQ0를 실행할 수 있는 행동들을 적습니다. 9.14에서는 (a)–(f)의 여섯이었고, 2026-10-16에 (g)가 더해져 일곱입니다(12.4).

**9.14 결정 2와 그 수정 — judging set 19개, K 10.** 처음 결정은 20개, K 11이었습니다. 바뀐 이유가 데이터셋의 rebuild에서 나왔습니다. 첫째, idle class 작업을 가진 여섯 파일(`c1-indexing`, `c7-indexing`, `c2-p1b`, `c1-backup`, `c7-backup`, `c2-p3b`)이 빠졌습니다. "the executor's idle rule places the background task below every row and the cap is work-conserving, so no row reaches it." 둘째, `c7-meeting`이 다시 들어왔습니다. "the measured call's cycle runs consume the boot slice in about a fifth of its cycles, so the tie with the boot default that moved it out in 8.8 no longer holds." 그리고 2026-10-09의 수정으로 `c7-mail`도 빠졌습니다. "its cut, the base's first 26.385 s, holds no keystroke — `c1-mail`'s 35 fall between 45.9 s and 53.1 s." 결과는 "The judging set is 19, K 10 by the same reading". 현재의 `harness/experiments/rq0-gate.yaml`에서 `files.judging`은 19개, `k`는 10, `g`는 0.5임을 확인했습니다.

**9.14 결정 3 — 결과에 의존하는 점검은 모두 사전 등록하고, 9.14 안에서는 하나도 돌리지 않는다.** 예외로 실린 값(예: pid 1의 run 평균, `code`의 `utility/libuv-worker`)의 재측정은 "a pre-registered contingency"입니다.

**9.14 결정 4 — demand window가 gate에서 물러남.** 이 결정은 원문을 그대로 옮깁니다.

> "The compiler records demand per file, as now, and per segment, newly, in the manifest, and never fails on it. The pair review reads each judging file's contended segment's demand where it reports the regime per pair. The building plan's §5a paragraph is restated: the `oversubscribed` class marks a file designed to hold contention, its demand a measured fact reported, not a window held."

> **왜 이렇게 정했나.** 9.14 spec의 결정 4와 changelog D4(window 정책을 지우고 segment별 수요를 manifest에 더한 기록)는 새 규칙만 적고, 이유를 따로 적지 않습니다. 이유는 2026-10-16에 인지오가 적었습니다(9.15 작업 목록 W-0737). 9.10 D17이 모든 job을 측정한 그대로 통째로 묶으므로 파일의 수요는 측정에서 따라 나오고, 그것을 창 안에 붙잡으려면 측정된 길이를 구부려야 했습니다. 그래서 수요는 붙잡지 않고 파일별, segment별로 기록하며, pair review가 경합하는 segment를 읽습니다. 기록이 보여 주는 배경은 둘입니다. 하나는 9.13 reads R5입니다. `oversubscribed` class 열 개 중 아홉 개가 창 밖이었고, 그 원인을 R5는 9.10 D17(batch job을 통째로 묶고 파일 길이가 따라가게 한 결정)과 9.10 D90(학습 job을 통째로 묶은 fold-in), 9.10 D142(다운로드를 통째로 묶은 결정)로 적었습니다. 다른 하나는 Phase 3의 3.1과 Phase 7의 7.7이 이미 적어 둔 "demand bounds throughput, not latency, headroom"입니다. 결정 4는 그 위에서 2026-08-26의 demand-budget rule을 "기록하는 사실"로 내렸습니다(9.14 결정 4, 2026-10-09). D4는 pair review가 읽을 경쟁 segment의 수요도 적었습니다. `c2-p1a`의 두 번째 segment가 35.77 lane(학습 job을 통째로 묶었으므로), `c2-p3a` 0.45, `c3-workday`의 compile segment 0.96과 mail segment 1.03입니다.

이로써 2026-08-23 Q8의 admission checklist 2번에서 "Q1's oversubscription rule is the mechanism"이라는 부분이 완전히 빠졌습니다. 남은 것은 "an oracle-vs-random gap measurable on that workload", 즉 Phase 7이 RQ0 gate의 파일별 기준으로 만든 부분입니다.

**9.14 결정 5와 6 — 채점 창과 항목.** 채점 창은 segment 경계와 일치해야 한다는 lint가 생겼습니다(결정 5). 항목에서는 데이터셋의 변화가 그대로 반영되었습니다. 세 gaming 파일은 `compositor` term을 잃었고(9.10 D24가 `gamescope`를 뺐으므로), 두 meeting 파일은 `video` term을 잃었고(9.10 D14가 통화 task를 하나로 줄였으므로), `c2-p2a-idle`이 `base: c2-p2a`로 들어왔습니다. 그리고 D2에서 발견이 하나 있었습니다. "fourteen of the scored editors have no input-channel wake at all — every file of the video editor (Kdenlive …) and of the image editor (GIMP …)." Kdenlive와 GIMP의 driven phase는 마우스로 하는 operation이어서 키 입력 stream이 없기 때문입니다. 그래서 그 열네 term은 `channel: timer`를 읽습니다. scoring spec은 "49 files, 75 terms (78 before …)"가 되었습니다.

**9.14 결정 7 — guard spec 1.1.** C2 쌍의 guard가 trace 본문 대신 설정 순서를 비교하게 되었고(9.11 D15), `whitelist` 조건이 모든 frozen 목록에서 `shipped_catalogue`와 `strongest_name_table` 둘이 되었습니다(9.12 D6).

**9.14 결정 8 — prior table의 문장을 고쳐 쓰되 값은 그대로.** "No row's algorithm, cap or params changes." 대신 문장이 데이터셋에 맞게 바뀌었습니다. 예를 들어 "the ten `clamscan` sentences to the unattended upgrade … the editor-premise rows to the measured per-keystroke work (about 5 ms for the writer and the mail client, about 78 ms for VS Code, none for Kdenlive and GIMP; 9.5 D23)." 2026-09-13 heads-up memo가 지적한 "editor는 slice 안에 block한다는 전제"가 측정값으로 다시 쓰인 것입니다.

**9.14 결정 9 — boot-default sweep 열 점.** Phase 8의 아홉 점이 열 점이 되었고, 각 점에 데이터셋의 측정값에서 온 이유가 붙었습니다. 예를 들어 700 µs는 "below the C2 pair's 834 µs chain slack", 14,000 µs는 "above the voice job's 12.2 ms ninth-decile cut"입니다.

**9.14 결정 10과 12 — 사전 등록된 민감도 점검과 variant 집합.** 점검 항목은 venue factor(측정된 모든 RUN을 ×1/1.25와 ×1.25로), chain scale(×1.2, ×1.4), segment 길이(C2 쌍의 60 s를 30 s, 120 s로), 예외로 실린 값의 반폭, trace replay, download bounding check 등입니다. 이것들을 돌릴 파일을 9.14 안에서 미리 build하고 pin했습니다. 결과는 "Nine variant sets, 78 artifacts: 19 + 19 venue, 3 + 3 chain, 4 + 4 segment-length, 11 + 11 corner, 4 replay"입니다. `dataset/variants.yaml`이 그 정의이고, compiler에 variant 변환이 이름 있는 mode로 더해졌습니다. 현재 `dataset/build.variants.manifest.json`의 artifact가 78개임을 확인했습니다.

- **variant**는 core set의 파일을 정해진 변환(배율, 길이 변경, 측정 trace 재생 등)으로 바꿔 만든 민감도 점검용 파일입니다. variant 집합을 다루는 권에서 자세히 설명합니다.
- **replay**는 측정된 반복 하나에서 관찰한 stream을 sampling 대신 그대로 재생해 task를 만드는 방식입니다(`dataset/replay/`). stream은 entry에 따라 세 가지 가운데 하나입니다. 편집기, browser, 보이지 않는 Chrome renderer(`code-editor`, `web-browser`, `renderer-hidden`)는 wake 순서와 각 wake의 run(`wakes`), batch job(`package-upgrade`, `cpu-batch`의 `python3`)은 run과 그 뒤의 block(`runs`), 영상 통화(`video-call`)는 cycle마다의 work(`cycles`)입니다(각 파일의 `kind`; 9.14 changelog D10, 2026-10-09). variants manifest를 보면 replay set의 네 파일은 모두 batch job 하나의 run을 재생합니다. 분포에서 뽑는 보통의 compile과 비교하기 위해 씁니다.

**9.14 결정 11 — Layer 1과 RQ4의 항목은 넘긴다.** 9.12에서 나온 recognizer 쪽 항목들은 gate spec이 아니라 Phase 10의 실험 spec들로 넘겼습니다.

## 8.5 9.14가 만난 크기의 문제 (2026-10-10)

rebuild된 데이터셋은 이전보다 여덟 배 컸습니다(8.2절의 R4). 9.14는 smoke run에서 그 대가를 처음 치렀습니다. 9.14 changelog D13–D14가 그 기록입니다.

- "the smoke completed its 196 runs in about two hours and then spent eleven hours in the aggregation step … 43 million rows across the smoke's runs, 14.5 million for each run of `c6-dual` alone … on the 16 GB M1 Pro the process was swapping." 그래서 "each run is aggregated right after its records are written."
- hog 판정 test는 "recomputes the hog set at every boost instant … instants × tasks × millions"여서 bisection으로 바꿨습니다.
- 결과로 49개 채점 파일의 smoke가 "196 runs …, 4 h 50 min on the M1 Pro, `c6-dual`'s four runs about three hours of it"이었습니다.

그리고 Phase 10에 비용 하나를 넘겼습니다. "the records build on `c6-dual` costs about 40 minutes a run … the RQ0 run's 100 `random` seeds on that file are a cost to plan for."

> **열린 자리.** `c6-dual`의 records build 비용(실행 하나에 약 40분, random seed 100개 계획)은 Phase 10의 RQ0 실행에서 계획해야 할 비용으로 남아 있습니다. 9.14의 handoff는 "a cheaper records path is a task of its own"이라고 적었습니다. 2026-10-16에 인지오는 지금 어느 대응도 고르지 않기로 하고, 비용을 Phase 10의 TODO 줄에 올렸습니다(9.15 작업 목록 W-0757). 그 줄은 비용을 "about 40 minutes a run on the mock trace (9.14 D14), about 67 hours for the `random` condition's 100 seeds on that file alone"으로, 메모리를 "one run's memory peak its 14.5 million rows, a machine under about 8 GB free swapping (9.14 D13)"으로 적고, 이 파일이 보고만 하는 파일임을 적습니다. 대응은 실제 simulator로 잰 비용 위에서 Phase 10에 정합니다. 선택지는 "a cheaper records path, N changed under the RQ0 gate spec's `n-grounding` statement (a harness changelog entry before any run), or the cost carried"입니다(12.4).

9.14의 끝은 "the dataset and harness CI jobs are green at the end"였습니다(결정 14). 다만 세 CI workflow가 `main`으로의 push에서만 돌았기 때문에, 이 branch에서는 그 step들을 local에서 돌렸습니다. 이 "CI가 이 manifest를 한 번도 compile한 적이 없다"는 사실은 다음 날 audit의 A4가 됩니다.

# 9장 · 2026-10-10/11 audit과 방향 전환

이 장은 "rebuild가 끝난 뒤 데이터셋을 다시 점검했을 때 무엇이 나왔고, 그것이 Phase 9의 계획을 어떻게 바꿨나"라는 질문에 답합니다. 원래 계획대로라면 9.14 다음은 문서 정리인 9.15였습니다. 그런데 9.15를 시작하기 전에 audit을 한 번 돌렸고, 그 결과로 다섯 개의 sub-task(9.17–9.21)와 하나(9.22)가 더해졌습니다. 그리고 그 과정에서 인지오가 "core set이 정말 맞는 도구인가"라는 질문을 던졌고, 그 답이 generated layer입니다.

## 9.1 다섯 auditor와 네 질문

audit 기록(`_dev/docs/audit/jioh/2026-10-10-dataset-audit-before-9.15.md`)의 머리말은 "Five independent auditors on `jioh/dataset-rebuild` at `fe19be86`: A consumer consistency, B provenance, C build reliability, D real-world fidelity, E external review"입니다. 각 auditor의 보고서는 보존하지 않았고, 이 통합 기록이 유일한 기록입니다. Created는 2026-10-10, Updated는 2026-10-11입니다.

네 질문의 답을 옮깁니다.

| 질문 | 답(요약) |
|---|---|
| `coreset-single`이 RQ0 실행 준비가 되었나 | "The dataset side is ready … The run is blocked outside the dataset: the simulator at HEAD refuses five rebuilt files (two judging) and four of the six pre-registered executor conformance items are unimplemented." |
| 전문 연구에 맞나 | "Major revision, not reject. Per-value provenance, determinism and pin discipline are above the field's norm." 거절 사유가 될 만한 것으로 공개 문서와 데이터의 불일치, C7 counterpart 구성이 "one-diff pair" 문구보다 약함, gaming의 숫자가 talk 슬라이드에 기댐, timeline의 bound value에 출처 필드가 없음, raw 데이터의 가용성이 명시되지 않음을 들었습니다. |
| build는 얼마나 믿을 만한가 | "Reproduces exactly here … Never compiled by CI." gate의 구멍도 적었습니다. |
| 실제 사용과 얼마나 가까운가 | "At the individual program: more faithfully measured than any desktop-scheduler workload the repository cites (27 of 28 kinds on the real program, 5–77 repeats, raw traces released). Above the individual program: task mix, co-occurrence, order, durations, core count, display/GPU/audio path and the human are designed, proxied or absent." |

마지막 답에는 RQ0의 통과가 무엇을 주장하는지도 적혀 있습니다. "A pass on RQ0 claims that contended single-core situations composed from real program behaviour exist where the right configuration differs measurably; not how often desktops are in them, how large the benefit is on a multi-core GPU desktop, or how a live user would experience it."

## 9.2 데이터셋 밖의 blocker

audit은 RQ0 실행을 막는 것 두 개를 데이터셋 밖에서 찾았고, 둘 다 다시 확인했습니다.

**1. simulator의 loader가 다섯 파일을 거부한다.** "`simulator/src/sim.cpp:874-904` resolves `WAKE.target` against top-level `arrive` ids only. The rebuilt build trees wire each object job's six spawn-table members with WAIT/WAKE in parent–child order (9.6 D19 …), so children wake children. Refused: `c1-compile`, `c7-compile` (judging), `c3-workday`, `c4-compile`, `c6-dual` (reporting)." 개수도 셌습니다. "`c7-compile` 25,269 child-targeted WAKEs, `c1-compile` 43,620." audit은 이것을 소통의 문제로도 적었습니다. "The schema allows any `task_id` as a target; the contract's prose example shows only top-level targets; the heads-up memo promised the input format unchanged. The usage is new; 경민 was not told."

**2. executor conformance가 빚으로 남아 있다.** RQ0 gate spec의 conformance statement가 요구하는 여섯 행동 중 "implemented (c) MLFQ cold start, (f) chain stages in EDF's deadline class; owed (a) zero-wait ready line, (b) TIMER skip rule, (d) `batch_bandwidth_cap` (field never read), (e) strict idle class (`declared_class` never read)." 인경민의 2026-10-10 memo도 (d)와 안전망이 구현되지 않았음을 확인합니다.

그리고 셋째로 "Last simulator regression check was on the 24-file pre-rebuild set"이라는 사실도 적었습니다.

이 blocker들은 데이터셋이 아니라 simulator의 일이고, 인경민의 것입니다. 데이터셋 쪽의 할 일은 알리는 것입니다. 그래서 9.15의 최종 memo가 이것을 담도록 TODO의 9.15 줄에 들어갔습니다(12장).

## 9.3 class A — 인지오의 결정이 필요한 결함 넷

**A1 — C7 counterpart의 키 입력이 base의 처음 26.385 s가 아니다.** 9.10 D41(counterpart는 base의 처음 C초라는 결정)은 task, 도착, 떠남에 대해서만 test되었고, 키 입력 stream을 어디서 자를지는 아무도 정하지 않았습니다. compiler는 `offset = uniform(seed, iid, "stimulus", j) × (span − window length)`로 stream의 시작점을 뽑는데, counterpart의 창(22.385 s)과 base의 창(56 s)이 길이가 다르므로 같은 seed가 다른 offset을 냅니다. audit은 이것을 다시 확인한 표를 남겼습니다.

| mode | base의 [0, 26.385 s) 안 입력 wake | counterpart | 공유하는 시각 |
|---|---|---|---|
| browsing | 90 | 29 | 0 |
| office | 112 | 103 | 0 |
| dev | 49 | 78 | 0 |
| mail | 0 | 0 | 0 |

"공유하는 시각 0"은 counterpart의 키 입력이 base의 키 입력과 하나도 겹치지 않는다는 뜻입니다. audit은 RQ0에는 혼동이 없다고 적었습니다("headroom is within-file across conditions"). 하지만 "one-diff pair"라는 문구는 과장이고, 두 고정된 문서(pair review finding 8과 scoring spec의 `c7-mail` 주석)가 틀린 메커니즘을 적고 있었습니다. 선택지는 둘이었습니다. (i) design으로 기록하고 문장을 고친다, (ii) compiler 규칙을 더해 파생 파일의 stimulus offset을 base의 창에서 뽑게 하고, 열 counterpart와 variant를 다시 build한다. audit의 추천은 (ii)였습니다. "it realises the recorded decision and makes the pinned sentences true."

**A2 — timeline의 bound value에 출처 필드가 없다.** 7.10.5절에서 본 9.10 D32(timeline의 bound value에도 출처 tag나 label을 단다는 결정)의 빈틈입니다. "`c2-p2a.timeline.yaml:28` binds `total_work: 727.170s` untagged."

**A3 — game chain이 talk 슬라이드에 기댄다.** "`game-task-chain` paces 8 of 51 files (3 judging: c2-p2a, c2-p2b, c7-gaming) on a talk deck." 그리고 `lavd-ossna24`의 역할 줄은 "Talk slides — footnote tier despite carrying numbers"입니다. 선택지는 9.12 D113(발표 자료용 id 유형)을 적용해 숫자를 "발표자가 보고한 값"으로 적는 것, 또는 chain을 직접 측정하는 것이었습니다.

**A4 — build gate의 구멍.** "`make check` compares an in-memory manifest to the committed one and never hashes `build/` on disk … `variants.py --check` runs in no workflow … `build.manifest.json.inputs` pins archetypes and schema only … CI has never compiled this manifest."

- **build gate**는 "commit된 manifest가 다시 compile한 결과와 같은가"를 검사하는 `make check`와 CI workflow를 함께 부르는 말입니다. compile과 build gate를 다루는 권에서 자세히 설명합니다.

**해결(2026-10-11, 인지오).**

- **A1** — 선택지 (ii)를 택했습니다. "the compiler draws a derived file's stimulus offset from its base's window, so a counterpart's keystrokes are its base's first C seconds … the test 'c7 input wakes ⊂ c1 input wakes in [0, C)' is added." → 9.18 (a)
- **A2** — 필드와 lint를 넣기로 했습니다. → 9.18 (b)
- **A3** — "resolved as is. The figures stand as the talk's reported values; the chain-x1.2 and chain-x1.4 variants are the sensitivity check. No change to the entry or the files."
- **A4** — 한 번의 변경으로 구멍을 닫고 Linux CI에서 이 manifest를 compile하기로 했습니다. → 9.18 (c)

> **왜 이렇게 정했나.** A1에서 (ii)를 고른 이유는 audit의 추천 문장 그대로입니다. "it realises the recorded decision and makes the pinned sentences true." 이미 기록된 결정(9.10 D41의 "base's first C seconds")과 이미 고정된 문서의 문장을 사실로 만드는 쪽을 택한 것입니다. A3를 그대로 둔 이유로 기록된 것은 "The figures stand as the talk's reported values; the chain-x1.2 and chain-x1.4 variants are the sensitivity check"입니다(audit 기록 "Resolutions", 2026-10-11).

## 9.4 건전하다고 확인된 것

audit은 문제만 적지 않았습니다. "Sound, and verified" 절의 숫자 몇 개를 옮깁니다. "129/129 artifacts match both manifests; 5 gate pins equal current bytes; 129/129 schema-valid; 863 arrive + 189,484 spawn records all carry `declared_class`, idle in exactly the 7 predicted files; 19 judging / 32 reporting / 78 variants; dataset lint clean; harness suite 279 passed." 그리고 "`make check` 1517 s exit 0 … `variants.py --check` 2098 s exit 0 (78)."

이 129는 core set 51개와 variant 78개의 합입니다.

## 9.5 현실 충실도의 지도

auditor D는 데이터셋의 각 층이 현실과 얼마나 가까운지를 등급으로 매겼습니다. 몇 행을 옮깁니다.

| 층 | 등급 | 차이 |
|---|---|---|
| CPU 행동 | PROXY, strong | EPYC 7763 Azure VM의 vCPU 하나, Xvfb, GPU·refresh·소리 없음, perf 아래. 측정된 venue 효과: tracing 0.72–0.98, huge page ×1.144, Xeon 대 EPYC 0.50–0.72× |
| game chain | STYLISED → DESIGN | 슬라이드의 260/1650 µs, 관례의 lognormal, 16단 chain은 우리 것, 60 Hz는 Steam Deck 사양 |
| wake 시각 구조 | STYLISED | rate/gap/run 표는 2 % 안, 순서와 동시 깨어남은 잃음 |
| 입력 stimulus | PROXY, large | SWELL-KW 2012 Windows lab, 키만, Word stream이 LibreOffice와 VS Code를 모두 몸, 포인터 입력 없음 |
| task 조합 | DESIGN | |
| 함께 도는 것·순서 | DESIGN / UNGROUNDED | |
| 길이 | DESIGN | 압축된 사건 시간, 60 s interactive 파일, counterpart 26.385 s |
| scheduling class | FAITHFUL class / DESIGN rule | 엄격한 idle = 0 % 대 `background.slice` ~23 % |

"함께 도는 것·순서: DESIGN / UNGROUNDED" 행이 다음 절의 질문으로 이어집니다.

## 9.6 열린 질문: core set이 맞는 도구인가 (2026-10-11)

audit 기록에는 인지오가 2026-10-11에 제기한 "Open" 절이 있습니다. 원문을 옮깁니다.

> "The core set serves milestones 1–7 (RQ0–RQ4), not RQ0 alone. Its C3 group holds three arcs with about eight segment boundaries in all, each ordered mode pair seen at most once, and the set has 64 segments over 32 driver-table cells. It cannot carry a statistical claim on transition recognition (RQ1), on recognition accuracy per cell, or on the phase-shift family (RQ4: a fixed sequence at 60 s / 10 s / 2 s transitions, whose files do not exist). The building plan assigns generalisation to the Layer 3b naturalistic set, which is not built and is on no phase line. Fidelity-map row 'co-occurrence / order: design, ungrounded' is this finding; the consolidation under-classed it by reading it against RQ0 only."

즉 core set은 RQ0에는 충분하지만, 연구 전체가 묻는 "전환을 얼마나 잘 알아보나", "cell마다 정확도가 얼마인가", "전환이 빠를 때 비용은 얼마인가" 같은 비율의 주장에는 표본이 너무 적다는 것입니다. 상태는 "open. 인지오 is weighing whether the core set as defined is the right instrument at all, against a naturalistic or generated set."

같은 날 방향이 정해졌습니다("Direction taken on the open item").

- "A generated layer is added beside the core set; the core set stays. Each group whose claim is a rate gets a generated set that enumerates the factor in full, with no realism claim (design). The naturalistic set stays in the backlog for the frequency claims."
- C3: 240개 순서쌍에 대한 2-segment grid, 그리고 A → B → A 3-segment return grid(가운데 길이를 variant로). "Longer chains are not enumerated. The three authored arcs remain as existence cases."
- 작은 flap-stress set: daemon의 hold time과 hysteresis를 위한 재료. "the values are tuned on files disjoint from the ones measured."

- **generated layer**는 core set 옆에 생성기로 만드는 파일 묶음입니다. 현실성은 주장하지 않고(design), 하나의 요인을 빠짐없이 나열합니다. generated layer를 다루는 권에서 자세히 설명합니다.
- **existence case**는 "이런 상황이 존재한다"는 것만 보여 주는 파일입니다. 비율을 재는 표본이 아닙니다.
- **240개 순서쌍**은 열여섯 mode 중 서로 다른 두 mode를 순서 있게 고르는 경우의 수(16 × 15)입니다.

> **왜 이렇게 정했나.** generated layer를 택한 이유는 "Open" 절의 진단 그대로입니다. 비율의 주장에는 요인을 빠짐없이 나열한 표본이 필요하고, core set은 각 순서쌍을 많아야 한 번 봅니다. naturalistic set이 아니라 generated layer를 먼저 택한 이유는 backlog 줄에 적혀 있습니다. naturalistic generator는 "its prerequisite is a source for Linux-desktop co-occurrence and transition frequency, which 9.10's search did not find." 출처가 없으니 현실의 빈도를 주장할 수 없고, 그래서 현실성을 주장하지 않는 나열을 택했습니다(audit 기록, 2026-10-11; `_dev/TODO.md` Backlog).

## 9.7 focus가 telemetry에 들어가다 (2026-10-11)

같은 날 또 하나의 결정이 있었습니다("Decision — focus enters the telemetry").

> "The recognizer's snapshot carries, beside the name → count multiset, which process holds the focus (none when no window does). … Behaviour (burst patterns, CPU use) stays out; labels stay out; PIDs stay out."

결과로 기록된 것은 넷입니다. focus의 변화는 집합의 변화이므로 snapshot과 query point를 냅니다. whitelist 조건도 focus를 받습니다. 모든 조건은 focus 필드가 있을 때와 없을 때 같은 파일로 돌 수 있고, 그 차이를 보고합니다. generated layer의 정답은 segment마다 focus 주인을 적습니다.

- **focus**는 지금 사용자의 키보드와 마우스 입력을 받는 창입니다. 데스크톱에서는 맨 앞에 있는 창입니다.

이 결정은 2026-09-06에 frozen된 telemetry contract를 바꿉니다. 그리고 2.3절의 Q7 edge case와 연결됩니다. 프로그램이 아무것도 시작하거나 끝나지 않고 사용자가 다른 창으로 옮겨 가기만 하면, 이전에는 query point가 없었습니다. 이제는 focus의 변화가 query point를 냅니다. 이것이 transition grid의 두 번째 형태("A stays, the focus moves to B")가 의미를 갖는 이유입니다.

## 9.8 C4, C5, C2의 방향과 원치 않는 job의 backlog (2026-10-11)

**C4의 방향.** "The distractor's Layer 1 axis is the name's relation to the vocabulary, not its CPU behaviour: another mode's foreground program (the 240 cross-mode cells, the focus staying on the running mode), a program outside the vocabulary (the library's measured ones), an unknown name (C5's axis). CPU behaviour is a Layer 2 axis, read on the same files." 이때는 "The three authored C4 files remain as cells of the grid"였는데, 이 부분은 9.20이 바꿉니다(10장).

**C5의 방향.** familiarity ladder를 열여섯 mode에 대해 생성합니다. tier 4 이름은 조합형(`<function>-<role>`), tier 5는 의미 없는 문자열, 모두 15글자 `comm` 한계 안입니다. tier 3은 "the program's own real name that carries no meaning"입니다. 그리고 "The present C5 tier-3 files, a real name of another program standing in (an indexer's name on a player), move to C6 as the name-collision limit."

**C2의 방향과 A1의 종결.** "The rate claim on intent runs on the sixteen C1–C7 pairs; no new C2 pairs are generated." 그리고 building plan의 C2 문구("behaviorally identical", "differ only in intent")를 rebuild된 상태로 고칩니다. "the unwanted side is a measured job of its own (file-indexer, package-upgrade, incremental-backup), differing in name and in behaviour; P3 flips the mode and `initiated`, not `background_wanted`."

**원치 않는 job의 backlog.** 선택 규칙과 후보를 적었습니다. 규칙은 "`background_wanted: false` by the vocabulary's definition; in the stock Ubuntu 24.04 desktop image and enabled by default; measurable on the CI runner with the real program; a name distinct from `unattended-upgr` and `tracker-miner-f`"입니다. 후보는 우선순위대로 `gnome-software` + `packagekitd`, `snapd` 자동 갱신, `updatedb.plocate`, `update-initramfs`, `mandb`와 `apt-get update`입니다. `clamscan`은 "not stock"(9.10 D3, 백신 검사를 무인 업그레이드로 바꾼 결정)이라는 이유로, Steam의 shader 사전 캐싱(`fossilize`)은 "not measurable on the runner"라는 이유로 규칙 밖입니다.

## 9.9 TODO와 spec에 무엇이 더해졌나

이 audit의 결과로 2026-10-11에 세 가지가 바뀌었습니다.

1. **Phase 9 spec에 결정 9와 10이 더해졌습니다.** 6.5절에서 인용한 generated layer와 focus의 결정입니다. 결정 6의 끝에 "Before the sweep, added 2026-10-11: …"도 더해졌습니다. 이 변경은 commit `4f0eb86a`입니다.
2. **TODO에 9.17–9.21이 더해졌습니다.** TODO는 "9.17–9.21 added 2026-10-11; they keep their numbers and run before the sweep"이라고 적습니다. 각 줄은 "read `_dev/docs/audit/jioh/2026-10-10-dataset-audit-before-9.15.md` first"로 시작합니다.
3. **9.22도 더해졌습니다.** "9.22 added 2026-10-11 after 9.18's verification run, before the generated layers." 이유는 10장에서 봅니다.

그리고 audit이 찾은 문서의 낡은 곳 중 9.15 줄에 없던 것들("Docs-staleness found that is NOT on the 9.15 TODO line")이 2026-10-11에 9.15 줄로 옮겨졌습니다. 예를 들어 interpretation contract의 TIMER backlog 문구, "25 judging, K = 13" 같은 옛 숫자, `dataset/README.md`가 demand window를 규칙으로 적은 줄, `docs/references.md`에 `dhakal-chi18`이 두 번 있는 것, 라이선스 파일이 없는 것 등입니다.

실행 순서는 "9.13 → 9.14 → 9.17 → 9.18 → 9.22 → 9.19 → 9.20 → 9.21 → 9.15 → 9.16"이 되었습니다.

# 10장 · Phase 9 셋째 구간: focus, build gate, build time, generated layer

이 장은 "2026-10-11부터 2026-10-15까지 더해진 일곱 sub-task가 데이터셋에 무엇을 더하고 고쳤나"라는 질문에 답합니다. 실행 순서는 9.17 → 9.18 → 9.22 → 9.19 → 9.20 → 9.21 → 9.23이었고, 이 장도 그 순서를 따릅니다. 9.23은 이 guidebook이 찾은 결함을 처리한 sub-task로, 2026-10-14에 더해졌습니다(10.7). 이 구간이 끝났을 때 데이터셋은 core set 51개, variant 78개, generated layer 1,562개를 가지게 되었고, 그 전부를 CI가 매번 build합니다.

## 10.1 9.17 — focus가 telemetry에 (2026-10-11)

9.17의 spec(`_dev/docs/spec/jioh/task-9.17-focus-in-the-telemetry.md`)은 "Decided in the 2026-10-11 grill, on the decision recorded in [the audit]"이라고 적습니다. 즉 audit의 "focus enters the telemetry"를 형식과 데이터로 실현한 sub-task입니다.

**9.17 결정 1과 7 — 창 focus track을 키 입력 창과 따로.** "that track is a compile-time stimulus placement, and the window focus is the real-desktop signal the experiment measures. Every keystroke window lies inside a focus interval of the same task." 그리고 이름(결정 7). "The keystroke-window track is renamed `input`. The window-focus track takes the name `focus`." 2026-08-27의 2.3 결정 3이 만든 `focus:` track이 이렇게 `input`으로 이름을 바꿨고, `focus`라는 이름은 새 의미를 얻었습니다.

**9.17 결정 2 — focus의 주인은 process 이름.** "The resolution is that of `/proc/<pid>/comm` on a real machine … Only top-level tasks can hold the focus; spawn-table children cannot."

**9.17 결정 3 — focus의 자리.** canonical workload에 `meta`, `ground_truth`, `events` 옆에 네 번째 최상위 key로 들어갑니다. "`ground_truth` does not change: the focus is shown to the recognizer, so it is not part of the answer key."

**9.17 결정 4 — core set의 작성 규칙.** "The focus stays on the window the user last brought to the front, does not leave when typing stops, and is none only when no window exists." 파일 묶음마다 적용한 결과도 spec에 있습니다. 단일 mode 파일은 전면 프로그램이 처음부터 끝까지, `c1-idle`은 없음, C3 arc는 segment 경계에서 옮겨 갑니다.

`c6-dual`만은 정할 것이 남아 있었습니다. spec의 열린 항목이 "The alternation period in `c6-dual`: taken from the window-switching sources 9.10 recorded … if one supplies a usable value; otherwise labelled design"이었습니다. 9.17 D1이 그것을 정했습니다. "the focus alternates between the editor and the game every 688 s — the mean continuous segment in a working sphere before switching, 11 min 28 s, `gonzalez-chi04` as 9.10 C-gonzalez-1 reads it … the regular alternation, the editor first and the typing's 2 s lead-in are design." 2026-08-26 addendum이 원래 논문으로 돌려놓은 González & Mark(CHI 2004)의 숫자가 여기서 쓰였습니다. 결과로 `c6-dual`의 키 입력은 "9 typing windows of 686–688 s in place of one of 12 068 s"가 되었습니다.

**9.17 결정 5 — telemetry 모양은 조건과 직교하는 축.** 모든 조건을 focus가 보이는 모양(`focus`)과 이름만 보이는 모양(`names`)의 두 가지로 같은 파일에서 돌립니다. records에 25번째 열 `telemetry`가 생기고, run 이름이 `<condition>[-seed][+boot]~<shape>`가 됩니다.

**9.17 결정 6 — query point는 전체 집합 위에서 정의.** focus를 숨겨도 focus만 바뀐 순간은 query point입니다. 같은 snapshot이 반복되고, recognizer의 반복된 답이 채점됩니다.

결과의 숫자는 9.17 D4에 있습니다. "147 query points over 51 files — 130 before — the 17 new ones `c6-dual`'s focus moves (ambiguous, ungraded)."

**9.17 결정 8 / D6 — 닫힐 때 일관되게.** 새 최상위 key가 모든 artifact의 hash를 바꾸므로, 9.17 안에서 다시 build하고 bless하고 pin했습니다. pin은 데이터셋 `625e431f…`, variant `328560cf…`였고, compile에 24분 20초, variant에 34분 34초가 들었습니다.

## 10.2 9.18 — compiler, schema, build gate (2026-10-11)

9.18의 spec(`_dev/docs/spec/jioh/task-9.18-compiler-schema-and-build-gate.md`)은 audit의 class-A 결함 A1, A2, A4와 9.17에서 넘어온 test 시간 문제를 다뤘습니다.

**(a) 키 입력 slice — 9.18 결정 1–3 / D1.** "An input window may carry the window of which it is a slice (`slice_of: {from, to, index}`) … the compiler draws the stimulus offset for the outer window … so a counterpart's keystrokes are byte-identical to its base's over the slice." deriver가 이 필드를 씁니다(결정 2). test는 같음이 아니라 부분집합입니다(결정 3). 이유는 "the compiler drops the keystrokes that fall inside an operation"입니다. counterpart에서는 operation의 위치가 비례로 옮겨지므로(9.10 D44), base에서는 살아 있던 키 입력 일부가 counterpart에서는 operation 안에 들어가 빠질 수 있습니다. 9.18 D6이 세어 본 결과입니다. "browsing 85 → 79 (the six inside the page load), office 102 → 91, dev 47 → 47, mail 0 → 0, indexing 46 → 27, compile 2354 → 358, ml-train 1844 → 1 628; every counterpart's set a subset of its base's."

**(b) bound value의 출처 — 9.18 결정 4 / D2.** "`source` is a map beside `bind`. Each task carrying a `bind`, or a `count`, carries a `source` map with the same keys … A value is one source tag, a list of source tags, or one of the labels `design`, `convention`, `arithmetic`." 9.10 D32(timeline에 묶인 값도 출처 tag나 label을 단다는 결정)가 9일 만에 실현되었습니다. `bound-values.md`의 측정값 열두 개에 tag를 달았고, `dataset/sources.yaml`에 `pytorch-examples`, `kdenlive`, `glam`이 더해졌습니다.

**(c) build gate — 9.18 결정 5, 6, 8 / D3, D4.** manifest의 `inputs`가 compiler의 소스와 stimulus·replay stream을 내용으로 pin합니다(결정 5). `make check`가 디스크의 `build/`를 검사합니다. "every file in `build/` matching an entry, every entry present, no file in neither. A missing `build/` fails"(결정 6). compile report도 blessed artifact가 되어 manifest에 자기 section을 가집니다(결정 8). 처음 `check_build`를 돌렸을 때 결함이 하나 나왔습니다. "`compile.py` keyed the manifest's `reports` section by the artifact's path, not the report's, so the section overwrote the artifact hashes in `check_build`'s union." 102개 오류였고, report의 경로를 key로 쓰도록 고쳤습니다(D6).

**(d) test 시간 — 9.18 결정 8의 fixture 규칙 / D5.** `test_coreset.py`의 fixture가 51개 timeline을 test 안에서 다시 compile하느라 test suite 50분 중 약 25분을 썼습니다. 이제 blessed build에서 hash가 맞으면 읽고, 아니면 compile합니다. "The `coreset` fixture reads the 51 pairs from the blessed build in 5 s."

**9.18 D7 — 검증 run, 그리고 취소된 CI.** 결정 7은 `dataset.yml`에 손으로 띄우는 trigger를 더하고 Linux에서 한 번 이 manifest를 compile하라고 했습니다. 첫 dispatch(run 38129714928)는 "was cancelled by 인지오's decision after 23 min still in `lint`: on the 4-vCPU runner the five steps would have run past the 6 h job limit." 집에서의 측정도 같은 이야기를 했습니다. `make check`는 56분 27초, dataset test suite는 44분 3초였습니다. 그리고 그 44분은 두 test 때문이었습니다. "`test_manifest.py::test_manifest_records_demand_per_artifact` (1,367 s, the in-process compile of the set) and `test_coreset.py::test_no_file_fails_on_its_demand` (1,153 s, `lint_canonical`'s jsonschema pass)." schema 검증은 "about 0.6 MB/s — `c6-dual` 187.6 MB in 335 s"였습니다.

이 CI 취소가 9.22를 낳았습니다. 9.18의 Linux run은 9.22의 도구로 다시 돌린 run 38131040159가 대신합니다.

## 10.3 9.22 — build 시간 (2026-10-11)

9.22의 spec(`_dev/docs/spec/jioh/task-9.22-build-time.md`)은 "decided in the 2026-10-11 grill after 9.18's verification run"이라고 적습니다. 문제는 9.18 D7이 적은 그대로입니다. "today `lint`, `dataset`, `test` and `check` each compile it, 3.5 h a run." 한 CI run이 같은 데이터셋을 네 번 compile하고 있었습니다.

**9.22 결정 1 — build가 재현성을 증명하고, check는 비교만 한다.** "`make dataset variants` rewrites the two manifests; `make check` is derive drift, both manifests equal to their committed bytes, and `build/` equal to the manifests. The in-memory recompile flags of `compile.py` and `variants.py` remain for independent verification and leave the gate." changelog D1은 이 둘이 같은 진술이라고 설명합니다. build가 manifest를 다시 썼으므로, 그것이 commit된 bytes와 같다는 것은 "the recompile reproduces the committed set — the same statement the in-memory flags made at twice the compile"입니다.

**9.22 결정 2 — `lint`는 compile 전의 검사.** compile이 이미 모든 artifact에 같은 canonical lint를 돌리므로, `make lint`는 저장소, timeline, bound-value lint만 합니다.

**9.22 결정 3 — schema 검증은 `jsonschema-rs`로.** `c7-transcode`(95 MB)로 잰 결과입니다. "`jsonschema` 141 s, `fastjsonschema` 19.7 s …, `jsonschema-rs` 1.4 s, a malformed event caught by each." schema 자체와 검증의 의미는 바꾸지 않았습니다.

그리고 compile과 variant를 파일마다 병렬로 돌리되, 결과를 정렬해 manifest의 bytes가 직렬 build와 같게 했습니다(D4). spec의 invariant대로 "No artifact or report byte changes"였고, compiler 소스가 바뀌었으므로 manifest의 `inputs`만 바뀌어 다시 bless하고 pin했습니다(D5, pin `d10bcd42…`, `831a854e…`).

전후의 측정입니다(9.22 changelog, M1 Pro, 10 core, Python 3.12).

| step | 전 | 후 |
|---|---|---|
| `make lint` | ~42 min | 0.8 s |
| `make dataset` | 22–24 min | 52 s |
| `make variants` | 33–35 min | 1 min 46 s |
| `make test` | 44 min | 2 min 01 s |
| `make check` | 56–59 min | 1.7 s |

CI run 38131040159는 checkout부터 끝까지 6분 34초였습니다. 9.22 D6은 이 run이 "also 9.18's Linux run (its D7)"이라고 적습니다. audit의 A4가 지적한 "Never compiled by CI"가 이렇게 닫혔습니다.

> **왜 이렇게 정했나.** build가 증명하고 check가 비교하게 한 이유는 같은 진술을 두 번 compile해서 확인할 필요가 없다는 것입니다(9.22 D1). `jsonschema-rs`를 고른 이유는 측정값입니다. 같은 파일에서 100배 빨랐고 잘못된 사건을 똑같이 잡았습니다(9.22 D3). 그리고 이 작업이 generated layer보다 먼저 온 이유는 TODO에 적혀 있습니다. "9.22 added 2026-10-11 after 9.18's verification run, before the generated layers." 수백 개의 파일을 더하기 전에 build 시간을 해결해야 했기 때문입니다.

## 10.4 9.19 — generator와 C3 grid (2026-10-11)

9.19의 spec(`_dev/docs/spec/jioh/task-9.19-generator-and-the-c3-grids.md`)이 generated layer의 첫 세 set을 만들었습니다.

**9.19 결정 1 / D2 — segment는 60 s, batch job의 크기는 살아 있어야 할 구간에 맞춘다.** "Every grid segment is 60 s, the length of the interactive C1 files. A batch mode's job … is bound by the generator to the span of segments the job must be alive in … the value derived from the C1 binding's rate and labelled `source: design`. The job's CPU pattern is the archetype's measured one; only its total is design." 손으로 확인한 예가 changelog에 있습니다. "compile → office `departs` binds `make` to 106 object jobs (2,908 × 58 / 1,592)." core set이 9.10 D17로 job을 통째로 묶은 것과 달리, generated layer는 job의 크기만 design으로 줄이고 행동 모양은 측정 그대로 씁니다.

**9.19 결정 2 — transition grid의 두 형태.** "Form 1 ('A departs and B arrives'): at 60 s A's tasks depart, B's arrive, the focus moves to B. Form 2 ('A stays and the focus moves to B'): at 60 s B's tasks arrive and the focus moves to B; A's tasks remain to the end of the file."

- **transition grid**는 두 segment짜리 파일 240 × 2 = 480개로, 모든 mode 순서쌍의 전환을 두 형태로 나열한 set입니다.

**9.19 결정 3 — segment 안의 배치는 9.10 D44 그대로.** segment의 task는 C1 task를 C1의 도착 시각대로 segment 시작에 맞춰 옮긴 것이고, 입력 창은 2 s의 여유를 두고, operation은 창의 같은 비율 지점에 둡니다. "A segment of 4 s or less has no input window."

**9.19 결정 4 — 생성된 timeline은 commit하지 않는다.** "The generator emits ordinary timeline YAML that the existing compiler compiles — no canonical artifact is produced directly. The timelines and their artifacts are build products, not committed; committed are the generator, its grid definition and each set's manifest. The generator is pure."

**9.19 결정 6 — tuning과 측정의 분리.** return grid의 240쌍은 쌍 id의 keyed hash 순위로 120/120으로 나누고, flap-stress 파일은 tuning seed와 측정 seed로 두 번 build합니다. "the rule is design."

**9.19 결정 7과 P — flap-stress의 간격.** 이 결정 앞에 선례 검색(changelog P)이 있었습니다. hold-time 계획의 step 3, 즉 "real systems가 비교할 만한 전환에 쓰는 debounce 값"을 찾는 일입니다. 검색 결과는 세 규모였습니다. "hardware-state governors at 0.5 ms–80 ms …, daemon-level tuning switches at 5–30 s (GameMode, tuned, systemd-oomd), capacity provisioning at 5–15 min." 이 daemon은 daemon 수준의 전환이므로 비교할 범위는 5–30 s입니다. 그래서 간격은 GameMode의 `reaper_freq` 5 s, tuned의 `update_interval` 10 s, systemd-oomd의 30 s, 그리고 그 아래 한 점으로 2 s(design)가 되었습니다. "Three pairs × four intervals × two seeds: 24 files." 세 쌍은 keyed hash로 뽑힌 "mail → gaming, meeting → photo, render → gaming"입니다(D1).

- **flap**은 일시적이거나 틀린 답 때문에 설정이 적용되었다가 곧 되돌아가는 것입니다. **flap-stress set**은 process 집합이 짧은 간격으로 여러 번 바뀌는 파일 24개입니다.
- **hold time**은 설정을 적용한 뒤 N초 동안 새 답을 적용하지 않는 규칙이고, **hysteresis**는 새 답이 K번 연속으로 나와야 적용하는 규칙입니다.

**9.19 결정 8 — 작성된 arc는 그대로.** "`c3-workday`, `c3-evening` and `c3-creation` are unchanged, their pins unchanged; their role is existence cases."

**9.19 결정 10 — return grid는 form 1만.** "A → B → A … 240 pairs × three middle lengths = 720 files." spec의 열린 항목이 "A form-2 return grid (A stays, the focus moves to B and back) is not built; if the RQ4 experiment spec's session needs it, the grid is added then"입니다.

- **return grid**는 A → B → A 세 segment짜리 파일 720개입니다. 가운데 B의 길이를 60 s, 10 s, 2 s로 바꿉니다. 짧은 전환 뒤 원래 상태로 돌아올 때 낡은 설정의 비용을 재려는 것입니다.

**9.19 결정 9 / D5, D7 — build gate와 CI에 바로.** 세 set의 manifest가 `check`의 목록에 들어가고, `dataset.yml`에 step이 생겼습니다. 집에서 세 set의 build는 "2 min 09 s … (1,224 artifacts, 4.3 GB on disk …)"였고, CI run 38135623993이 세 manifest를 Linux에서 재현했습니다.

## 10.5 9.20 — C4와 C5의 grid, C5에서 C6으로 (2026-10-12)

9.20의 spec(`_dev/docs/spec/jioh/task-9.20-c4-and-c5-grids.md`)은 audit의 C4와 C5 방향을 실현했습니다.

**9.20 결정 1 / D1 — C4 cell은 transition grid의 focus 형태에서 focus를 A에 둔 것.** TODO의 9.20 줄은 "B's foreground program arriving at 30 s"라고 적었는데, grill은 다른 모양을 택했습니다. "two 60 s segments, B's whole set at 60 s by the composition rules, A's focus and input to the file's end, both segments labelled A." 기록된 이유는 "the transition grid's `focus` form and this cell then have the same open programs and differ in the focus track alone, so every condition run on the pair under the `focus` and `names` telemetry shapes isolates the field's worth."

> **왜 이렇게 정했나.** 이 모양에서 transition grid의 form 2 파일(A가 남고 focus가 B로)과 C4 cell 파일(B가 오지만 focus는 A에)은 열린 프로그램이 똑같고 focus track만 다릅니다. 그래서 두 파일을 focus가 보이는 모양과 이름만 보이는 모양으로 돌리면, focus라는 필드 하나의 가치를 따로 잴 수 있습니다(9.20 D1, 2026-10-12). 9.17 결정 5가 만든 "telemetry 모양" 축과 이렇게 맞물립니다.

**9.20 결정 3 / D2 — 두 focus 주인이 같은 이름인 26개 cell은 pre-committed miss.** "`code` over dev, compile, ml-train and indexing; `kdenlive` over video-edit, render, transcode and backup; `chrome` over browsing and meeting — the C4 cell and the `focus` form produce the same telemetry (the focus holder is carried by name, telemetry rule 6), so the C4 label is unreachable."

**9.20 결정 2 / D3 — 하나의 distractor set, 두 관계.** cross-mode 240개와 vocabulary 밖의 프로그램 32개입니다. 후자는 `element-desktop`(chat client)과 `7z`(file archiver)를 열여섯 mode에 각각 넣은 것입니다. "These two are the library's measured programs that belong to no mode's task set and leave the label unchanged; the library offers no third." 합해서 272개입니다.

**9.20 결정 4 — 작성된 C4 파일은 existence case.** audit의 C4 방향은 "The three authored C4 files remain as cells of the grid"였지만, 결정 1의 모양 때문에 바뀌었습니다. "their injection at 30 s within one segment is not the cell's shape."

**9.20 결정 5–7 / D4, D6, D7 — familiarity ladder.** tier 4와 5를 열여섯 mode에 대해, 이름을 바꾸는 대상(focus 주인만, 나머지만, 전부)을 축으로 만들되 결과가 같은 cell은 하나로 접었습니다. "eight modes with one program … give one cell per tier, eight give three — 32 per tier, 64 over tiers 4 and 5, plus the two tier-3 cells: 66." tier 3은 측정 기록에서 찾았습니다. render의 `kdenlive_render` → `melt-7`("the child holding 99.6 % of the render's CPU"), backup의 `deja-dup` → `duplicity`(57 %)입니다. tier 4의 이름은 손으로 쓴 표이고 design입니다. tier 5의 이름은 네 글자 소문자의 keyed draw입니다. 15글자 한계의 근거로 kernel의 `TASK_COMM_LEN`을 `linux-sched-h`(v6.17의 `include/linux/sched.h`)로 references에 넣었습니다.

- **familiarity ladder**는 C1 task set의 이름을 tier 4와 5의 이름으로, render와 backup의 job은 tier 3의 이름으로도 바꿔 만든 파일 66개입니다. 이름이 낯설어질수록 recognizer가 어떻게 되는지 재려는 것입니다.

**9.20 결정 8 / D8 — `c5-t3`가 `c6-alias`가 되다.** "The recipe moves from the C5 recipe file to the C6 one under the id `c6-alias` — two players wearing indexers' names, the name-collision limit beside `c6-spoof`. Its segment drops `familiarity: 3` and gains `spoof: true` and `pre_committed_miss: true`; tasks, archetypes and seed are unchanged." 이유는 audit의 C5 방향입니다. tier 3은 "the program's own real name that carries no meaning"인데, `c5-t3`는 다른 프로그램(색인기)의 진짜 이름을 플레이어에 씌운 것이므로 tier가 아니라 이름 충돌의 한계라는 것입니다. core set을 다시 build했고 "51 artifacts, 50 byte-identical"이었습니다. scoring spec의 entry는 C6 section으로 옮겨 "terms verbatim"으로 다시 freeze했고(`9cd9a155…`), RQ0 gate spec의 reporting 목록과 Layer-1 제외 목록이 `c6-alias`를 갖게 되었습니다.

**9.20 결정 9 / D5 — 원치 않는 job의 측정은 backlog에, 시점을 적어서.** "today the ten interactive counterparts share one unwanted name, `unattended-upgr`. How many unwanted jobs the attribute claim needs is decided in the RQ1 experiment spec's session; the campaigns run after Phase 10's RQ0 run and before the RQ1 run." changelog D5는 이것을 "a validity limit for RQ1's attribute accuracy, not for RQ0"이라고 적습니다.

**9.20 D10 — build와 작은 사고.** "A first run had changed every generated artifact through `meta.derived_from` because the generated files' header comment had been reworded ('composed or renamed'); the wording was restored and the sets regenerated — the header is part of the timeline bytes the artifact pins." 생성된 timeline의 머리 주석 한 줄이 바뀌자 모든 artifact의 hash가 바뀐 것입니다. 이것은 D12(같은 입력은 같은 bytes)의 원칙이 얼마나 엄격하게 지켜지는지를 보여 줍니다. CI run 38243554308이 일곱 manifest를 Linux에서 재현했습니다.

## 10.6 9.21 — generated layer의 소비자 (2026-10-13 → 10-14)

9.21의 spec(`_dev/docs/spec/jioh/task-9.21-consumer-work-for-the-generated-layer.md`)은 2026-10-13의 grill에서 나왔습니다. 생성된 1,562개 파일을 harness와 데이터셋 도구가 읽을 수 있게 하는 일입니다.

**9.21 결정 1 / D1, D3 — 생성된 파일은 규칙으로 채점한다.** "Generated files are scored by a run-time rule from the C1 entries, as the variants are. No generated file has an entry in the scoring spec." 파일 안의 각 placement(한 mode의 C1 task 집합에 id 접미사를 붙인 것)마다 그 mode의 `c1-<mode>` entry의 term을 가져와, latency와 주기 term은 그 placement가 label된 segment로 창을 두르고 batch term은 창 없이 씁니다. 첫 lint에서 버그 하나가 나왔습니다. "the first lint over the five sets returned 282 errors, every one a gaming placement — `game.chain.1-s0: no task with that id`. The compiler forms a chain member's id from its task's id (`game-s0` → `game-s0.chain.1`), so the suffix belongs on the task id, before `.chain.<n>`."

**9.21 결정 2, 3 — term이 없는 경우.** 어느 segment에도 label되지 않은 placement(distractor로 들어온 B 집합)는 term이 없습니다. 입력 창이 없는 placement는 입력 channel term만 빼고 timer와 주기 term은 남깁니다.

**9.21 결정 4 / D2 — coverage 표는 manifest에서.** "No empty-cell rule applies to it." 표는 generator 옆에 두었고 `wlc`에 두지 않았습니다. 이유는 changelog D2에 있습니다. "the core set's manifest pins `wlc/*.py` by content (9.18 decision 5) — any edit there moves the core manifest and, through it, the variants manifest and the RQ0 gate spec's dataset pin." compiler 소스를 pin한 9.18의 결정이 이렇게 코드의 자리까지 정했습니다.

**9.21 결정 5, 6 / D6 — 파일의 축은 manifest join으로, 선택은 축으로.** records는 바뀌지 않습니다. 실험 spec은 `files.select`와 `pins.generated`로 manifest에서 축에 따라 파일을 고릅니다. "The RQ0 gate spec keeps its explicit lists."

**9.21 결정 7 / D7 — flip 개수와 그 비용.** daemon이 적용한 설정 변경 수, 그중 채점기가 틀렸다고 한 것, 그 틀린 전환이 만든 초과 대기의 합을 한 줄로 보고합니다. "No new primitive, metric or records column." 이것이 hold-time 계획의 규칙 없는 측정(그 step 1)의 재료입니다.

**9.21 결정 8 / D8 — generated layer는 모든 CI run에서 build한다.** 측정이 근거입니다. "5 min 13 s of a 12 min 04 s run on the 4-vCPU runner; 1,562 artifacts, `build/` 6.8 GB." runner의 저장 공간은 새 reference `gh-hosted-runners`(GitHub Docs, 2026-10-13 읽음)의 "4 vCPU, 16 GB RAM and 14 GB SSD"입니다. 필요할 때만 build하거나 일부만 pin하는 안은 기각되었습니다. 이유는 "both put an exception into the gate's rule that `build/` equals the union of every manifest." 다시 볼 기준도 README에 적었습니다. set이 더해질 때, 또는 step의 시간이나 build 크기가 runner의 저장 공간에 다가갈 때입니다.

**9.21 D11–D13 — CI에서 죽은 test.** dataset CI는 run 38390052552에서 11분 58초로 초록이었습니다. harness CI는 두 번(38387289484, 38396745220) coreset 전체를 도는 mock test 두 개에서 runner가 process를 죽였습니다. D12는 그 원인을 집에서 쟀습니다. 두 test가 `c6-dual` 하나에 대해 workload, trace의 줄 객체와 문자열, run file, rows를 한꺼번에 들고 있어서 "peak resident set 7.66 GB"였습니다. test 도구를 고쳐 한 파일의 객체만 들게 했지만, `compute`가 파일의 모든 row를 list로 돌려주는 바닥은 남았습니다. 그래서 D13(2026-10-14)은 두 test에 `coreset_wide` marker를 붙였습니다. "`make -C harness test` runs the suite with `-m "not coreset_wide"` (296 of 298 tests) and is what `harness.yml` runs; `make -C harness test-full` runs the whole suite and is run at home." 이유는 "Marking the tests rather than slicing the set inside them keeps each test's assertion whole — 51 files, the 8.4 measured graded set — where it runs." 이후 harness run 38547043521이 초록이었습니다(2026-10-14 wrap-up commit).

## 10.7 9.23 — guidebook이 찾은 것 (2026-10-14 → 10-15)

이 dataset guidebook의 여덟 권을 쓴 사람들이 tree, manifest, code, 기록을 읽다가 scoring, 데이터셋, gate에 관한 발견을 모았습니다(`_dev/docs/audit/jioh/2026-10-14-guidebook-findings.md`, `5709a079` 기준. scoring과 데이터셋의 A1–A8, gate·CI·lint의 B1–B5). 문서의 낡은 곳은 이 목록에 넣지 않고 9.15로 보냈습니다. 그 발견을 처리한 것이 sub-task 9.23입니다. 인지오가 2026-10-14의 grill에서 하나씩 tree에 대조한 뒤 정했고, 기록은 `_dev/research/jioh/task-9.23-guidebook-findings/changelog.md`의 D1–D18입니다.

**9.23 D1, D2 — C6의 두 파일에 pre-committed miss.** `c6-fold`에서는 30 s에 통화의 `chrome` task가 도착해 snapshot이 `chrome ×5`에서 `chrome ×6`이 되고, 개수의 변화도 집합의 변화이므로 그때 query가 생깁니다. "Nothing in the 30 s snapshot says call — a sixth `chrome` is also what a new tab shows — so the meeting label cannot be reached from the names." 그래서 meeting segment(30–60 s)가 pre-committed miss가 되었습니다(D1). `c6-spoof`의 segment 하나는 `background_wanted: true`였는데, 그 `true`는 `c1-browsing`에서 물려받았을 뿐 기록된 이유가 없었습니다. "from 20 s the spoof is sustained CPU work nobody asked for, and the snapshot shows one more `chrome` and nothing else." 그래서 spoof가 도착하는 20 s에서 나누어 뒤 segment를 `false`와 pre-committed miss로 두었습니다(D2). core set의 segment는 66개에서 67개가 되었고, RQ0 gate spec의 `layer1_exclusions`에 두 파일이 들어갔습니다.

**9.23 D3–D6 — generated layer를 읽는 법.** 넷 다 데이터를 바꾸지 않고 읽는 법을 정했습니다. D3은 생성된 파일의 batch term이 turnaround를 유지하고, job이 끝나지 않는 row는 censored bound를 받는다고 정했습니다(scoring spec은 머리글만 바뀜). D4는 generated layer에서도 도착이 program의 시작이고 측정된 launch 단계를 재생한다고 정했습니다(9.10 D136). 기록된 이유는 "the generated layer exists to answer the research questions, not to make a claim"입니다. D5는 return grid와 flap-stress가 형태를 유지하고 경계마다 한 mode의 program을 닫고 다른 mode의 program을 연다고 정했고, D6은 transition grid의 focus 형태와 distractor grid의 cross-mode cell이 recognition 쌍이며 seed는 그대로라고 정했습니다.

**9.23 D8 — library의 문장 하나.** `code-editor`의 validation scope는 "Read over 12,068 s, the span `c6-dual` holds it focused"라고 적었는데, 9.17 이후 `c6-dual`의 편집기가 focus를 가장 오래 가지는 구간은 686–688 s입니다. 문장을 "the span `c6-dual` held it focused before its focus alternated with the game every 688 s (9.17 D1)"로 고쳤고, probe의 길이와 읽은 값은 그대로입니다. library의 바이트가 바뀌었으므로 모든 artifact의 바이트도 바뀌었습니다.

**9.23 D10 — 첫 rebuild (2026-10-14).** D1, D2, D3, D8을 한 번에 build했습니다. "2 of the core set's 51 change beyond it, `c6-fold` and `c6-spoof`", 나머지 artifact는 library hash만 달라졌습니다. RQ0 gate spec의 pin은 dataset `c5f7fa5a…`, variants `8986b58a…`, scoring spec `2ad757b6…`이 되었습니다.

**9.23 D11–D16 — gate, lint, CI, 그리고 program의 끝 (2026-10-15).** 모두 인지오의 결정입니다. D11은 compiler가 읽는데 manifest가 pin하지 않던 launch stream 열 개를 `inputs`에 넣었습니다(core 33, generated 55). D12는 `make check`가 build가 다시 쓰는 파생 timeline과 `coverage-grid.json`도 commit된 바이트와 비교하게 했습니다. 그 전에는 "A derived timeline regenerated and left uncommitted passed CI, its artifact's `derived_from` naming a blob not in git"였습니다. D13은 `make lint`가 freeze lint를 돌리게 했습니다. D14는 canonical lint에 셋을 더했습니다. spawn된 child의 WAKE 대상, 15자를 넘는 이름, program의 끝입니다. D15는 두 requirements 파일을 집 기계의 버전으로 고정하고(runner가 그날의 최신 버전을 설치해, pytest 9.1.1에서 dataset test가 실패한 적이 있습니다), 집 기계에서 4시간 50분이 걸리는 smoke를 손으로만 돌리게 했습니다. D16은 D14를 쓰다가 찾은 것입니다. segment-bound program 7,400개가 depart 전에 할 일이 없어 끝나 버렸고, interpretation contract와 harness의 mock은 그 task를 막혀 있다고 읽는데 reference simulator는 끝났다고 읽었습니다. 그래서 program을 다음 blocking 명령으로 끝맺게 했습니다. wake로 움직이는 program은 마지막 wake의 channel에서 WAIT로, timer로 움직이는 program은 다음 TIMER로 끝납니다. "Nothing new executes"라고 기록은 적습니다.

**9.23 D17, D18 — 둘째 rebuild와 CI (2026-10-15).** D11–D16을 한 번에 build했고, 모든 artifact가 D16으로 바뀌었습니다(끝에 붙은 명령을 빼면 이전 hash와 같습니다). pin은 dataset `81d3213d…`, variants `7079e677…`이 되었습니다. D18은 그 tree를 손으로 CI에 돌린 기록입니다. dataset run 38722675475가 17분 04초에 초록이었고, runner가 일곱 manifest, 파생 timeline, coverage grid를 바이트 단위로 재현했습니다. harness run 38722678829도 초록이었습니다.

D7은 기록 두 곳(9.18 D6의 base keystroke 수, `c6-dual`의 utilization)을 바로잡았고, D9는 P1 pair가 RQ0에서 맡는 역할을 지금 상태대로 적었습니다. 9.23은 데이터셋 문서의 정정을 9.15에 넘겼고, 9.15는 그 정정 중에 인지오가 정한 data와 code의 수정을 2026-10-16에 묶어 다시 build했습니다(12.1, 13장).

## 10.8 지금의 데이터셋

이 구간이 끝났을 때의 데이터셋을 tree에서 세어 확인했습니다. 2026-10-17에 다시 세어도 파일 수는 같습니다.

| 묶음 | 파일 수 | 확인한 곳 |
|---|---|---|
| core set | 51 | `dataset/build.manifest.json`의 `artifacts` |
| variant | 78 | `dataset/build.variants.manifest.json` |
| transition grid | 480 | `dataset/build.transition-grid.manifest.json` |
| return grid | 720 | `dataset/build.return-grid.manifest.json` |
| flap-stress | 24 | `dataset/build.flap-stress.manifest.json` |
| distractor grid | 272 | `dataset/build.distractor-grid.manifest.json` |
| familiarity ladder | 66 | `dataset/build.familiarity-ladder.manifest.json` |

generated layer는 480 + 720 + 24 + 272 + 66 = 1,562개입니다. TODO의 9.20 줄이 적은 "`make -C dataset check`, 3,304 files, 7 manifests"의 3,304는 artifact와 compile report를 함께 센 수입니다. 일곱 manifest의 `artifacts`와 `reports` 항목을 세어 보면 core set 51 + 51, generated layer 1,562 + 1,562, variant 78(variant manifest에는 `reports` section이 없음)로 합이 3,304입니다(`python3.12`로 manifest를 읽어 확인).

# 11장 · 뒤집힌 결정과 다시 지은 것들

이 장은 "무엇이 무엇으로 바뀌었고, 왜, 언제였나"라는 질문에 표로 답합니다. 앞 장들은 시간 순서로 이야기를 따라갔기 때문에, 같은 주제의 변화가 여러 장에 흩어져 있습니다. 이 장은 그것을 주제별로 모읍니다. 표의 "이유"는 기록의 말을 짧게 옮긴 것이고, 기록에 이유가 없으면 그렇게 적었습니다. 슬라이스 안에서 같은 날 고친 작은 정정(예: 9.5의 D1부터 D99 사이의 수많은 수정)은 여기에 다 싣지 않고, 데이터셋의 모양을 바꾼 것만 실었습니다.

## 11.1 출처와 registry

| 전 | 후 | 이유(기록) | 날짜와 기록 |
|---|---|---|---|
| 작업 전환 연구의 저자 "Yun et al." | Zhang, Sun, Chai & Aghajan, CHB 49 (2015), `zhang-chb15` | 세션에서 원문을 확인한 정정 | 2026-08-26, grill archive "Verified sources"; Phase 1의 1.6 |
| `zhang-chb15`가 "약 3분 전환"을 독립적으로 뒷받침 | registry와 references에서 빠짐 | "no reachable copy: closed access, ScienceDirect 403, Elsevier API 429" | 2026-10-01, 9.10 D1 |
| Mark 계열 수치를 CHI 2008/2014에 붙임 | González & Mark, CHI 2004(`gonzalez-chi04`) | "CHI 2008 contains neither figure"; 23:15는 Gallup 인터뷰에만 있음 | 2026-08-26, grill addendum |
| `ocallahan-atc17`의 2,430 process = kernel build | DynamoRio 6.1.0 build의 숫자 | 원문 §4.1 "make builds DynamoRio … with make -j8" | 2026-09-13, critical finding A1 |
| `frame_period` 16.7 ms의 출처 `lavd-ossna24` | `steamos-refresh`, label design | "The deck states no frame period" | 2026-09-13, 9.4 D2 |
| "Role D will validate X" (live 측정) | meas-ci + 문헌 + 명시한 한계, meas-live 제외 | "No teammate Linux desktops known" | 2026-08-26, grill D2, D7, D8 |
| 타이핑 간격 `dhakal-chi18` + Roeser | 측정 중 SWELL-KW 재생, Dhakal과 Roeser tag 삭제 | 응답 쪽 값은 Linux 관찰에서만(9.5 D6); 136M은 외운 문장의 전사 | 2026-09-14/15, 9.5 D4, D19 |

## 11.2 형식과 compiler

| 전 | 후 | 이유(기록) | 날짜와 기록 |
|---|---|---|---|
| 주기 task의 상대 SLEEP | `TIMER(period)`, drift 없음 | "it drifts, systematically underloading the machine exactly under bad configs" | 2026-08-26, grill D13 |
| 네 release artifact(native와 single × coreset과 generalset) | single-lane set 하나, `coreset-single` | 관찰 장소마다 크기가 맞춰져 있지 않음(scale 한계) | 2026-09-16 결정(9.5 follow-ups 결정 13–14), 2026-10-09 적용(9.13 D1) |
| lane의 ~100–150 %를 벗어나면 build 실패 | gate 아님, 수요는 파일별·segment별로 기록만 | 별도 이유 기록 없음. 배경은 열 개 중 아홉 개가 창 밖(9.13 reads R5) | 2026-10-09, 9.14 결정 4 |
| TIMER의 backlog 규칙(늦은 tick을 모두 따라잡음) | skip 규칙(놓친 tick은 마감 실패) | "every program and periodic framework found skips" | 2026-10-07, 9.11 D3; 2026-10-09, 9.14 결정 1 |
| 측정된 timer wake마다 TIMER step(주기 = 다음 wake까지 간격) | 주기가 선언된 task만 TIMER, 나머지는 timer channel의 WAIT | `c1-media`의 첫 주기가 9 µs인데 평균 1,182 µs, 세 소비자가 TIMER를 주기 job으로 읽음 | 2026-09-26, 9.5 D74 |
| task model에 scheduling class 없음 | `declared_class` (`normal`, `idle`) | "Background programs declare their class themselves, and a stock Linux kernel acts on it" | 2026-10-07 결정(9.11 D4–D6), 2026-10-09 적용(9.13 D2) |
| `focus:` = 키 입력 창 track | `input`으로 이름 변경, 새 `focus` = 창 focus | audit의 "focus enters the telemetry" | 2026-10-11, 9.17 D1 |
| counterpart의 stimulus offset을 따로 뽑음(공유 시각 0) | `slice_of`로 base의 창에서 뽑음 | "it realises the recorded decision and makes the pinned sentences true" | 2026-10-11, 9.18 D1 (audit A1 선택지 ii) |
| timeline의 bound value에 출처 칸 없음 | `bind`/`count` 옆에 `source` map, lint | 9.10 D32가 정했지만 9.13이 넣지 않음 | 2026-10-11, 9.18 D2 (audit A2) |
| object job = spawn-table entry 하나가 펼쳐지는 chain constructor | 연속된 spawn-table entry 여섯 개, WAIT/WAKE로 연결 | "the workload format lets only a top-level task create tasks" | 2026-09-18 → 09-19, 9.6 D9 → D19 |
| compiler가 `familiarity` 주석을 버림 | 정답 segment의 key로 내보냄 | "compiled `ground_truth` had no split key" | 2026-09-08, Phase 5 archive |

## 11.3 core set의 모양

| 전 | 후 | 이유(기록) | 날짜와 기록 |
|---|---|---|---|
| coverage grid = mode × familiarity, 사람이 서명 | 32개 cell × 다섯 tier, 빈 cell이면 CI 실패 | "the human sign-off had missed the attribute's `false` side"; "Report-only was rejected as the failure mode of August" | 2026-09-09, Phase 7 결정 11 |
| 24개 파일, 17/32 cell, `false` segment 2개 | 50개 파일(C1 ×16, 새 C7 ×16), 32/32 cell, `false` 18개 | Phase 6 pair review finding 2 | 2026-09-10, Phase 7 |
| 50개 파일 | 51개(`c2-p2a-idle` 추가) | bounding check의 idle 절반(9.11 D21) | 2026-10-09, 9.13 D4 |
| 파생 파일이 demand class를 상속 | recipe의 `patch-meta`로 `calibration`을 직접 선언 | "admitting inheritance keeps the exception invisible" | 2026-09-09, Phase 7 결정 7 |
| `c1-idle`의 `attributes: {}` | `background_wanted: true` | vacuous-true 규칙을 지키지 않았음 | 2026-09-06, Phase 3 3.2 |
| core set이 RQ0–RQ4의 유일한 도구 | core set 옆에 generated layer(1,562개) | core set으로는 비율의 주장을 할 수 없음 | 2026-10-11, audit의 방향, Phase 9 결정 9 |
| 작성된 C3 arc와 C4 파일이 grid의 cell | existence case | C4의 30 s 끼워 넣기는 cell의 모양이 아님 | 2026-10-11/12, 9.19 결정 8, 9.20 결정 4 |
| C4 cell = B의 전면 프로그램이 30 s에 도착 | 두 60 s segment, B 전체가 60 s에, focus는 A에 | focus track 하나만 다른 쌍이 되어 필드의 가치를 잴 수 있음 | 2026-10-12, 9.20 D1 |
| `c5-t3`(tier 3) | `c6-alias`(spoof, pre-committed miss, tier 없음) | "a real name of another program standing in … move to C6 as the name-collision limit" | 2026-10-12, 9.20 D8 |
| gaming 파일에 `game.exe` × 300 | chain만, 이름은 LAVD 슬라이드 16의 이름 | 개수 규칙 위반, 꼬리는 placeholder | 2026-09-13, 9.4 D3; 2026-10-01, 9.10 D26 |
| wineserver → `system-daemon` 근사 | chain의 member, 260 µs | 슬라이드 11, 13, 16 | 2026-09-13, 9.4 D4 |
| gaming 파일의 `gamescope` | 없음, 게임의 다른 thread는 생략을 명시 | 9.10의 결정(D19, D24) | 2026-10-01, 9.10 D19, D24 |
| Chrome renderer 개수 placeholder(11, 7, 7, 9, 5) | Chrome 파일마다 `renderer-hidden` 넷 | Firefox Linux telemetry 4.67 → 다섯 tab, runner에서 관찰 | 2026-10-01 → 10-04, 9.10 D15, D127, D131 |
| `renderer-visible` task | 없음 | 브라우저 창은 하나 | 2026-10-01, 9.10 D16 |
| 파일 중간에 시작하는 앱이 정상 상태로 도착 | 관찰한 시작 phase를 재생 | 시작 직후 일이 크고 정해진 지점에 나타남 | 2026-10-01 → 10-05, 9.10 D21, D132–D140 |
| batch job을 60 s segment에 맞춤 | 측정한 job을 통째로, 파일이 길어짐 | "A slice describes part of a job"; 입력의 근거를 지킴 | 2026-10-01, 9.10 D17; 2026-10-05, D141 |
| 2026-09-26의 50개 파일, wake 531,740개, 84 MB | 51개, 4,522,200개, 681 MB | 통째로 묶은 job, renderer, launch replay, wake마다 사건 하나 | 2026-10-09, 9.13 reads R4, D7 |

## 11.4 job의 정체 — 대역에서 관찰로

| 전 | 후 | 이유(기록) | 날짜와 기록 |
|---|---|---|---|
| interactive counterpart와 `c2-p2b`의 `clamscan` on `cpu-batch` | Ubuntu 24.04 stock 무인 업그레이드 `package-upgrade`, 26.385 s | "ClamAV is not a traditional anti-virus or endpoint security suite"; ClamTk "is no longer maintained" | 2026-10-01, 9.10 D3, D36–D45 |
| `c7-compile`의 `make` → `dkms` 이름 바꾸기 | NVIDIA 모듈의 실제 DKMS 재빌드, 225.458 s | 상황의 현실 주장에는 관찰이 필요(9.10 D2) | 2026-10-02, 9.10 D4, D46–D59 |
| 색인 파일의 tracker rescan(`cpu-batch`) | Tracker 3.7.1의 첫 색인, `file-indexer`, 39.435 s | "no real user's home is reachable under open terms" → HippoCamp profile | 2026-10-03, 9.10 D5, D60–D81 |
| borg의 첫 백업(`file-backup`) | Déjà Dup의 주간 incremental, `incremental-backup` | 정기 백업의 실제 모습 | 2026-10-04, 9.10 D8, D112–D125 |
| `cpu-batch`의 `ffmpeg` 표로 render | Kdenlive export, `kdenlive_render` + `melt-7` | 같은 프로젝트의 실제 export | 2026-10-04, 9.10 D10, D101–D111 |
| `cpu-batch`의 HandBrakeCLI 표 | CpsMark+의 workload, `video-transcoder`, 2,970.871 s | benchmark 자신의 코드로 codec을 H.264로 확정 | 2026-10-03, 9.10 D11, D91–D100 |
| `python3` placeholder 학습 | PyTorch 기본 MNIST 예제, 1,389.885 s | 실제 학습 job | 2026-10-03, 9.10 D12, D82–D90 |
| Thunderbird를 세 가지로 묶고 별도 send task | `mail-client`의 `send` operation, `network-bulk` 삭제 | send는 Thunderbird process 안에서 돌고, 따로 두면 배경을 두 번 셈 | 2026-09-19 → 10-01, 9.7 D3, 9.5 D31–D46, 9.10 D13 |

## 11.5 archetype library

| 전 | 후 | 이유(기록) | 날짜와 기록 |
|---|---|---|---|
| `desktop-interactive`, `audio-playback`, `video-playback` | 측정한 프로그램별 entry 아홉 개 | 몽타주 금지(Phase 9 결정 2), 프로그램마다 CPU 요구가 다름 | 2026-09-15, 9.5 D2, D19 |
| `background-crawler` | 은퇴 | 어떤 timeline도 묶지 않고, 값이 다른 프로그램과 섞였고, 관찰이 없음 | 2026-09-19, 9.7 D5 |
| `io-stream`, `network-bulk` | `file-backup`, `file-archiver`, `game-download` (`file-backup`은 뒤에 은퇴) | 묶인 프로그램들의 구조가 측정한 프로그램과 다름 | 2026-09-19 → 09-23, 9.7 D1, D31, D34 |
| `electron-comms` | `renderer-hidden`, `renderer-visible`, `chat-client`, `game-client` (`renderer-visible`은 뒤에 삭제) | 두 값이 관찰된 어떤 process도 그리지 않음 | 2026-09-20 → 09-22, 9.8 D1, D25 |
| `system-daemon` | `compositor-shell`, `audio-server`, `service-manager`, `message-bus` | 두 집단이 검색한 모든 class에서 다름 | 2026-09-22 → 09-24, 9.9 D1, D26 |
| tracker rescan에 별도 entry `indexer-rescan` (D12–D15) | 철회, `cpu-batch`에 남음 | 포화도를 job 위에서 다시 계산하니 0.954–0.962 | 2026-09-19, 9.6 D16 |
| library v0.1 | v0.2 | `declared_class`의 추가 | 2026-10-09, 9.13 결정 9 (파일의 머리 주석은 2026-10-16, 9.15) |

library의 판 번호는 2026-10-14에 기록과 파일이 어긋나 있었습니다. 9.13 결정 9는 "The library's stated version moves from v0.1 to v0.2 in the data-contracts §2 and the dataset README"라고 정했는데, `dataset/archetypes.yaml`의 첫 줄은 "(v0.1)"이었습니다. 2026-10-10 audit이 이것을 낡은 곳으로 적었고, 9.15 줄에 "`dataset/archetypes.yaml:1` '(v0.1)'"로 들어갔습니다. 2026-10-16에 인지오가 머리 주석을 고치기로 정했고(9.15 작업 목록 W-0778), 9.15의 묶은 rebuild(커밋 `37c2e233`)에서 첫 줄이 "(v0.2)"가 되었습니다. library는 모든 manifest의 입력이므로, 이 한 줄 때문에 모든 manifest가 다시 bless되고 RQ0 gate spec이 다시 pin되었습니다(같은 rebuild의 다른 수정과 함께 한 번).

## 11.6 측정의 방법

| 전 | 후 | 이유(기록) | 날짜와 기록 |
|---|---|---|---|
| meas-ci는 구조와 모양만, 절댓값은 관례 | CPU 하나에 고정한 프로그램의 절댓값이 archetype의 값 | 관찰은 simulator의 lane과 같은 조건이어야 함 | 2026-09-14 → 09-16, 9.5 D3, D10, follow-ups 결정 2–3 |
| N = 5 반복 | 안정성 기준(95 % 반폭 ≤ 5 % 또는 1 µs), 최소 다섯 번 | "the task 2.6 spec §3 states 'N=5 matrix' without a ground"; 다섯 번 미만은 분산을 못 잡음(`kalibera-ismm13`) | 2026-09-18 → 09-19, 9.6 D10, D11, D24, 9.5 D29 |
| 첫 compile campaign `meas-ci:build:35215328887` | 버리고 처음부터 다시 | 다섯 반복이 두 CPU model에 걸침 | 2026-09-18, 9.6 D11 |
| runner의 CPU model이 섞임 | machine gate, AMD EPYC 7763만 | Xeon의 `cc1` 269 ms 대 EPYC 358–392 ms; 45개 job이 다섯 model | 2026-09-18, 9.6 D10, 9.5 D26 |
| wake = 이전 switch-out 1 µs 앞부터 여는 wakeup 창 | task가 직전에 CPU를 내려놓을 때의 상태(잠듦인가 선점인가)로 판정 | `sched_waking`은 짧은 대기에서 switch-out 기록보다 먼저 찍혀, 옛 창이 `borg`의 잠듦 3,204개 중 1,458개를 앞의 wake에 합쳐 버림 | 2026-09-19, 9.7 D21 |
| SteamCMD의 속도 제한에 token bucket | `htb` + `fq_codel` | runner 간 변동계수 ~20 % → ~2 % | 2026-09-20, 9.7 D24, D25 |
| `CHTTPClientThre`의 run 평균을 session 사이 변동으로 | 한 run 안의 드문 사건(`heavy_events`) | 50 s 창으로 읽으니 burst 하나 | 2026-09-26 → 09-28, 9.8 D30 → D33 |
| sysstat의 job을 데스크톱 밖으로 | 다시 데스크톱의 job | postinst는 systemd가 돌 때만 끄고, desktop image는 systemd 없이 만들어짐 | 2026-09-25 → 10-01, 9.9 D32 → D47 |
| perf로 trace하는 영향은 모름 | untraced control로 읽고 notes에 적음 | 2026-09-26 검토의 질문 | 2026-09-27, 9.5 untraced-control spec |

## 11.7 소비자와 gate

| 전 | 후 | 이유(기록) | 날짜와 기록 |
|---|---|---|---|
| RQ0 judging set = C2의 여섯 파일 | 스물일곱 개 | "demand bounds throughput, not latency, headroom" | 2026-09-06 → 09-10, Phase 3 3.1 → Phase 7 결정 14 |
| 스물일곱 개 | 스물다섯 개, K 13, 아홉 점 sweep | `c7-meeting`, `c7-media`는 executor 가정 아래 reporting-only | 2026-09-12, Phase 8 8.8 |
| 스물다섯 개, K 13 | 스무 개, K 11 → 열아홉 개, K 10 | idle class 파일 여섯은 어떤 row도 닿지 않음; `c7-meeting` 복귀; `c7-mail`의 잘린 부분에 키 입력 없음 | 2026-10-09, 9.14 결정 2와 수정 |
| boot-default sweep 아홉 점 | 열 점 | 각 점에 측정값에서 온 이유 | 2026-10-09, 9.14 결정 9 |
| C7 entry가 base의 term을 그대로 | "Unwanted work carries no term" | 원치 않는 job의 진행에 점수를 주게 됨 | 2026-09-09, Phase 7 결정 10 |
| `c2_pair` guard가 trace 본문을 비교 | 설정 순서를 비교 | P1이 `fixed`에서 더 이상 동일하지 않음(9.11 D15) | 2026-10-09, 9.14 결정 7 |
| `whitelist` 조건 하나 | `shipped_catalogue`와 `strongest_name_table` | 9.12의 결정(D6) | 2026-10-08 → 10-09, 9.12 D6, 9.14 결정 7 |
| starvation 하한 1 s, executor의 안전망 | 30 s, design, 안전망 약속 삭제 | sched_ext watchdog의 한계를 빌림 → design으로 다시 label | 2026-10-07 → 10-08, 9.11 D7 → D19 |
| `make check`가 메모리에서 다시 compile, `build/`는 hash 안 함 | `build/`가 manifest의 합과 같아야 함 | audit A4 | 2026-10-11, 9.18 D4 |
| `lint`, `dataset`, `test`, `check`가 각각 compile(3.5 h) | build가 증명, check는 비교(전체 약 5분) | 같은 진술을 두 번 compile할 필요 없음 | 2026-10-11, 9.22 D1–D5 |
| schema 검증 `jsonschema`(0.6 MB/s) | `jsonschema-rs` | 95 MB 파일에서 141 s → 1.4 s | 2026-10-11, 9.22 D3 |
| harness CI가 coreset 전체 mock test 두 개를 돌림 | `coreset_wide` marker, CI는 빼고 집에서 `test-full` | runner가 두 번 process를 죽임 | 2026-10-13 → 10-14, 9.21 D12, D13 |

## 11.8 뒤집기의 무늬

표를 모아 보면 몇 가지 반복되는 무늬가 보입니다. 이것은 기록이 스스로 정리한 것이 아니라, 위의 표에서 읽히는 공통점을 적은 것입니다.

첫째, 많은 뒤집기가 "원문을 끝까지 읽었다"에서 왔습니다. 2,430은 문장이 맞았지만 workload가 틀렸고(A1), 16.7 ms는 슬라이드에 없었고(A2), CpsMark+의 "H.256"은 benchmark의 코드가 H.264를 썼고(9.10 D95), sysstat의 postinst는 조건문 하나가 결론을 바꿨습니다(9.9 D47). Phase 9 결정 1의 "the check covers the whole claim … its object, unit, statistic, scope and population"이 이런 발견을 낳았습니다.

둘째, "작게 맞춘 값"이 "측정한 전체"로 바뀌었습니다. 60 s에 맞춘 batch job, 100개의 `cc1` 자식, 300개의 `game.exe`가 모두 그렇습니다. 그 대가로 데이터셋이 여덟 배 커졌고(9.13 reads R4, 크기와 wake 사건 수를 다시 센 기록), build 시간과 harness 메모리의 문제가 따라왔습니다(9.22, 9.14 D13, 9.21 D12).

셋째, 사람의 확인을 기계의 gate로 바꾸는 방향이 일관됩니다. 사람이 서명한 grid는 CI의 빈 cell 검사가 되었고(Phase 7 결정 11), 메모리 안의 비교는 디스크의 `build/` 검사가 되었고(9.18 D4), bound value의 출처는 lint가 되었습니다(9.18 D2). 반대 방향은 하나뿐입니다. demand window는 gate에서 기록으로 내려왔습니다(9.14 결정 4).

넷째, 철회와 되돌림이 기록에 그대로 남아 있습니다. 9.6 D12–D15(tracker rescan에 별도 entry를 주려던 결정)는 D16으로, 9.8 D30(Steam thread의 run 평균을 session 사이 변동으로 실은 결정)은 D33으로, 9.9 D32(sysstat job을 데스크톱 밖으로 뺀 결정)는 D47로 철회되거나 되돌려졌지만, 철회된 결정도 지우지 않고 "Superseded by …" 또는 "Reverted by …" 표시와 함께 changelog에 남았습니다. 그래서 이 표를 만들 수 있었습니다.

# 12장 · 지금 열려 있는 자리

이 장은 "2026-10-14 현재, 데이터셋과 그 주변에서 무엇이 아직 정해지지 않았거나 실행되지 않았고, 누가 정하나"라는 질문에 답합니다. 각 항목은 기록에서 인용하고, 무엇이 미정인지, 어떤 선택지나 전제 조건이 있는지, 누가 정하는지를 적습니다. 출처는 주로 `_dev/TODO.md`의 9.15, 9.16, Phase 10, Backlog 줄과, 각 spec과 handoff의 열린 항목입니다. TODO는 다른 session이 동시에 고칠 수 있는 파일이므로, 이 장의 인용은 2026-10-14에 읽은 상태입니다. 그 뒤 닫히거나 바뀐 자리는 2026-10-17에 다시 읽어 고쳐 적었습니다.

## 12.1 9.15 — 문서, memo, guidebook 정정 (WIP, 2026-10-14부터)

9.15는 2026-10-14의 grill로 spec(`_dev/docs/spec/jioh/task-9.15-docs-memos-and-guidebook-corrections.md`)을 얻었고, 같은 날 WIP가 되었습니다. spec의 소개는 "The one sweep that brings the public docs, the memos and the guidebook volumes already written in line with the rebuilt workload dataset and the decisions of Phase 9, ending in the final memo to 인경민 and 박이안"입니다.

**무엇을 하나.** 범위는 9.15에 넘겨진 모든 것입니다. TODO의 9.15 줄, 모든 slice changelog의 "Hands to 9.15" 줄(9.12와 9.10은 전부), 2026-10-10 audit의 항목입니다. 대상은 `docs/`(guidebook 포함), `dataset/README.md`, memo들입니다. 그리고 root `LICENSE`와 `dataset/LICENSE`를 새로 만들고, 마지막에 최종 memo를 씁니다. TODO의 9.15 줄은 한 줄이 18,000 bytes가 넘습니다(`sed -n 179p _dev/TODO.md | wc -c`로 18,441). 그중 데이터셋의 모양과 관계된 대표 항목만 옮깁니다.

- "native set removed from every doc (spec decision 14); library-level scale limitation stated (spec decision 13)"
- "the docs naming `background-crawler` (D5)", `electron-comms`, `system-daemon`, `Xorg`를 이름으로 부르는 문서
- 타당성 위협의 문장: "the compiled wake streams reproduce each component's rate, gap and run distributions, not the order of its gaps nor its components waking together"
- "the prose citing the dropped `zhang-chb15` rewritten without it"
- `docs/data-contracts.md` §2의 "There are twelve (…)" archetype 목록
- building plan의 층과 C 묶음의 역할을 rebuild된 상태로(C3는 existence case, C2의 "behaviorally identical"을 고침, C5의 tier 3을 좁힘, C6이 이름 충돌 cell을 받음)
- `dataset/README.md:77,131`의 demand window를 규칙으로 적은 줄, `dataset/archetypes.yaml:1`의 "(v0.1)", `docs/references.md`의 중복된 `dhakal-chi18`
- 데이터 가용성: "release URL and asset hash beside the values, a LICENSE, the stimulus streams' CC-BY-NC-SA, the manual releases"
- 9.17–9.21에서 온 것: coreset guide의 `c6-dual` focus 교대, C7의 "one-diff pair" 문구, return grid로 다시 쓰는 proposal의 Family 4, `c5-t3`가 `c6-alias`라는 것, generated layer의 소비자

**어떻게 하나 — spec의 결정 열넷.** 요약하면 이렇습니다. 먼저 하나의 작업 목록을 만들고 인지오가 검토합니다(결정 1). 편집 agent가 만나는 항목을 스스로 정하고 기록하며, "Code is first, not docs"(결정 2). 출처가 어긋나면 우선순위가 있습니다(결정 3). "Highest first: the code and data as they stand … for anything the code expresses; the latest decision record on the matter for what code does not express … the hand-off text, which says where to look and not what to write; the current docs, never an authority." 데이터셋을 설명하는 문서는 code와 대조해 전체를 다시 봅니다(결정 4). 작업은 대상 파일 단위의 chunk로 나누고 `docs/references.md` chunk를 먼저 혼자 돌립니다(결정 5). 새 reviewer agent가 chunk마다 검토하고 통과하면 main session이 commit합니다(결정 6). 인지오의 검토는 막지 않고 뒤따릅니다(결정 8). memo의 원문은 고치지 않고 "`## Correction (<date>)`" 절을 덧붙입니다(결정 10). `_dev/`의 기존 파일은 건드리지 않습니다(결정 11). 라이선스는 code가 MIT, 데이터가 CC-BY-NC-SA-4.0이고, `dataset/LICENSE`는 SWELL-KW를 크레딧합니다(결정 12).

**결정 9 — TIMER 행은 component별로 나눈다.** 이 결정은 지금의 불일치를 분명히 적습니다. "The simulator runs the backlog rule (`simulator/src/sim.cpp`); the harness reads the skip rule (`docs/harness/metrics.md` §6.2, `harness/tools/harness/primitives.py`). Rows on the harness's reading are applied in 9.15. Rows on the simulator's behaviour or the TIMER op's meaning are blocked — the docs keep the backlog rule — and carried to the Phase 10 TIMER line in `_dev/TODO.md`. The final memo names the simulator's skip rule and the zero-wait `ready` line as owed."

> **열린 자리.** 9.15의 미정 사항은 셋입니다. (1) 작업 목록과 chunk 구분은 인지오가 검토하기 전입니다(결정 1). (2) spec의 유일한 열린 항목은 "The final memo's language — decided at the memo step"입니다. 정할 사람은 인지오입니다. (3) 9.15는 끝나는 조건(결정 14)이 정해져 있습니다. 모든 작업 목록 행이 닫히고, 모든 chunk가 reviewer를 통과해 commit되고, 인지오가 모든 chunk log를 읽고, 기록된 모든 "code와 결정의 불일치"에 인지오가 답하고, 모든 memo가 열림/닫힘 줄을 갖고, 최종 memo가 commit되는 것입니다. 지금은 그 전입니다.

**최종 memo가 실을 것.** spec 결정 13과 TODO는 최종 memo의 내용을 정해 두었습니다. "the field `declared_class` on every archetype entry and every task record …, the closed set `normal` and `idle` …; the archetype contract at v0.2 … — and tells 인경민 the simulator loads files up to 190 MB (`c6-dual`), the set 681 MB in all"(190 MB와 681 MB는 9.13의 bless 때의 크기입니다. 9.23 D8은 최종 memo의 크기 행에 9.23 D10의 rebuild(2026-10-14) 뒤 크기, 곧 `c6-dual` 187,601,756 bytes와 core set 678,168,083 bytes를 넘겼고, 다음 날 9.23 D17의 rebuild가 그 크기를 바꾸었습니다. 그래서 최종 memo가 실을 크기는 D17 뒤의 것, 곧 `c6-dual` 187.6 MB(187,601,795 bytes)와 core set 678 MB(51개 파일, 678,172,716 bytes)입니다. 2026-10-17의 build에서도 같은 크기입니다), 그리고 "the simulator loader's refusal of child-targeted WAKEs (`simulator/src/sim.cpp:874-904`; `c1-compile`, `c7-compile`, `c3-workday`, `c4-compile`, `c6-dual`; 9.6 D19), the four executor conformance items owed, the telemetry's focus and the generated layer." 그리고 spec 결정 13이 더하는 것은 "the memos still open, the simulator's skip rule and zero-wait `ready` line as owed, and the licences chosen"입니다. 박이안에게는 9.14 결정 11의 recognition log 항목 두 개("the formatted prompt kept in the recognition log, the chat template's inserted date … fixed or recorded")가 frozen contract의 질문으로 갑니다.

## 12.2 9.16 — exit audit (아직 시작 전)

9.16은 Phase 9 spec 결정 8의 끝나는 조건을 확인하는 일입니다. TODO의 줄은 "Exit audits — the claim, measurement and compiled-number audits re-run on the final state (spec decision 8)"로 시작합니다. 아직 task spec은 없습니다(`_dev/docs/spec/jioh/`에 9.16 파일이 없음을 확인).

9.16 줄에는 각 slice가 넘긴 재현 목록이 길게 붙어 있습니다. 대표적인 것만 옮깁니다.

- "the measurement audit reads how each campaign's repeat count was chosen, the stopping rule being what makes the binding value's half-width optimistic"
- "venue mix listed per timeline (9.5 spec decision 13)"
- release에서 pool을 재현: 주기 entry 셋의 `cycle` block은 `meas-ci-2026-09-18`과 `meas-ci-2026-09-20`에서 `pool.py` `cc51eb8`로, session entry는 `meas-ci-session-2026-09-24`에서, `mail-client`의 77반복 idle pool은 `meas-ci-2026-09-18`과 `meas-ci-2026-09-28`에서 `0aa25ac`로
- "every entry's `declared_class` rests on 9.11's class census"
- sub-task마다의 manifest와 pin(9.17 `625e431f…`, 9.18 `976a943c…`, 9.22 `d10bcd42…`, 9.19, 9.20, 9.21의 생성 manifest들, scoring spec `0ff71b1f…`). pin은 그 뒤 9.23 D10(2026-10-14: dataset `c5f7fa5a…`, variants `8986b58a…`, scoring spec `2ad757b6…`)과 9.23 D17(2026-10-15: dataset `81d3213d…`, variants `7079e677…`)을 거쳐, 9.15의 2026-10-16 re-pin(dataset `b6017a10…`, variants `087ef27c…`, driver table `0fba4b3c…`, 생성 manifest는 transition grid `a8eebb33…`, return grid `2e57a6c1…`, flap-stress `dd6a7c24…`, distractor grid `264d3333…`, familiarity ladder `58a34d65…`)을 지나, 2026-10-17에는 9.15의 2026-10-17 re-pin이 현재입니다. dataset `d52e7bd4…`, variants `6c1c3e09…`, scoring spec `2ad757b6…`, guard spec `24ccb875…`, driver table `0fba4b3c…`, 생성 manifest는 transition grid `4bb7a444…`, return grid `ec7ca574…`, flap-stress `79a6c5c4…`, distractor grid `3478a908…`, familiarity ladder `415cfbd6…`입니다(`harness/CHANGELOG.md`, `harness/experiments/rq0-gate.yaml`의 `pins`)
- 9.23(D15)에서: 최종 build 위에서 집 기계로 돌리는 full smoke(`make -C harness smoke`)와 그 시간의 기록
- 9.15에서: `renderer-hidden`과 `video-editor`의 idle pool에 대한 burstiness와 window 읽기의 재실행, 그리고 stability ledger(허용 오차를 맞춘 양, 예외로 실은 양, 가장 큰 반폭)
- "every timeline's `source` map agrees entry for entry with `_dev/research/jioh/task-9.10-scenarios-timelines/bound-values.md` (the lint checks form, not that each tag is the right ground)"
- CI run 38131040159와 38243554308의 재현, "`gh-hosted-runners` read 2026-10-13"

> **열린 자리.** 9.16은 9.15가 끝난 상태 위에서 돈다고 9.15 spec 결정 14가 적습니다("9.16's exit audits run on that state"). 9.16의 방법(누가, 몇 명의 auditor가, 어떤 형식으로)은 아직 spec session이 없어서 정해지지 않았습니다. 정할 사람은 인지오입니다. 그리고 Phase 9 결정 8이 요구하는 "every measured value reproduces from the released raw data"는 9.16에서 처음 전체로 확인됩니다. 위의 마지막 항목이 적듯이, 지금의 `source` lint는 형식만 확인하고 "그 tag가 맞는 근거인가"는 확인하지 않습니다.

## 12.3 9.22의 나머지

9.22는 2026-10-11에 끝났고(TODO의 [x]), 남은 작업은 없습니다. 넘긴 것만 있습니다. 9.15에는 coreset guide §5.1의 CI 문장("CI가 다시 compile해서 hash를 `build.manifest.json`과 비교해요")을 지금의 gate(build가 manifest를 다시 쓰고 `check`가 commit된 bytes와 비교)에 맞게 고치는 일을, 9.16에는 세 pin과 CI run 38131040159의 재현을 넘겼습니다(9.22 D6). 9.18이 9.21에 넘긴 "schema 검증 0.6 MB/s" 문제는 9.22가 `jsonschema-rs`로 풀었고, 9.21이 generated layer의 CI 전략을 정하면서 측정을 다시 적었습니다.

## 12.4 Phase 10 — 통합과 RQ0 실행

Phase 10의 TODO 줄은 "Swap mocks for the real simulator and daemon, end-to-end smoke, run all coreset files × 3 conditions, check guards before looking at results, judge per the RQ0 gate spec; on failure, config search before workload redesign. Depends on Phase 9, 경민's integration gate and algorithm extension, and 이안's daemon"입니다. 데이터셋과 관계된 열린 항목은 다섯입니다.

**1. trace-replay 점검.** "a few scored files built twice — as compiled, and with the measured wake trace replayed — and their verdicts compared; its files, its agreement criterion and what a disagreement leads to are fixed in the RQ0 gate spec before the RQ0 run (9.14; from the 2026-09-28 review of 9.5–9.9)." 9.14가 이미 파일 넷(`c7-dev`, `c7-browsing`, `c7-meeting`, `c2-p1a`)과 일치 기준("each file's gap falls on the same side of g under both builds and differs by less than 0.17")을 gate spec에 사전 등록했습니다(9.14 결정 10). 실행은 Phase 10의 것입니다.

**2. Layer 1과 RQ4의 항목.** 9.12의 recognizer 쪽 항목들이 Layer 1과 RQ1–RQ4 실험 spec으로 넘어갔습니다. "the two rule lists' build (`shipped_catalogue`, `strongest_name_table`; no phase yet, 박이안 the owner)"도 여기 있습니다.

**3. TIMER 문서.** 2026-10-14에 9.15에서 넘어온 줄입니다. "TIMER docs restated to the skip rule once 인경민's simulator implements it … the simulator-side TIMER rows 9.15 leaves blocked." 전제 조건은 인경민이 simulator에 skip 규칙을 구현하는 것입니다.

**4. simulator의 blocker.** 9장에서 본 두 가지입니다. loader의 child-targeted WAKE 거부와, conformance 항목 (a) zero-wait `ready` 줄, (b) TIMER skip 규칙, (d) `batch_bandwidth_cap`, (e) 엄격한 idle class의 구현입니다. 인경민의 2026-10-10 memo는 이것들을 "Implementation owed (the docs already answer)"에 넣었습니다. 9.14 결정 1이 gate spec에 conformance statement를 넣었으므로, 이것들이 구현되기 전에는 RQ0 실행이 허용되지 않습니다. 2026-10-16에 인지오가 statement를 고쳤습니다(9.15 작업 목록 W-0758, W-0743). 끝 문장이 "(c) and (f) the simulator does today"가 되었고(cold start로 MLFQ에 들어가는 (c)는 `simulator/src/sim.cpp`의 2026-10-10 수정에 있음), 일곱째 항목 (g)가 더해졌습니다. "an orchestrator's WAIT children:<id> completes when the last child it spawned ends, and without blocking when none is live at the WAIT". (g)가 없으면 `c1-compile`의 build turnaround term(judging, weight 1.0)이 모든 조건에서 똑같이 censored가 되기 때문입니다. (g)의 규칙은 interpretation contract와 `docs/data-contracts.md`에 제안으로 적혀 있고 인경민이 동의하면 효력을 가지며, RQ0 gate spec은 실행에 그것을 요구합니다. 그래서 지금 빚으로 남은 conformance 항목은 (a), (b), (d), (e), (g)의 다섯입니다(`harness/experiments/rq0-gate.yaml`의 `simulator-conformance`).

**5. `c6-dual`의 비용.** 9.14 handoff의 "the records build on `c6-dual` costs about 40 minutes a run … the RQ0 run's 100 `random` seeds on that file are a cost to plan for"입니다. "a cheaper records path is a task of its own"이라고 적혔지만, 2026-10-14에는 TODO에 줄이 없었습니다. 2026-10-16에 인지오가 지금 어느 대응도 고르지 않고 비용을 Phase 10의 TODO 줄에 올렸습니다(9.15 작업 목록 W-0757). 그 줄은 `random` 조건의 seed 100개에 이 파일 하나로 약 67시간, 한 run의 memory 최고점이 1,450만 row라고 적고, 대응(더 싼 records 경로, gate spec의 `n-grounding` statement 아래에서 N을 바꾸기, 비용을 그대로 지기)은 실제 simulator로 잰 비용 위에서 Phase 10에 정한다고 적습니다(8.5).

> **열린 자리.** Phase 10의 시작은 인경민의 통합 gate와 박이안의 daemon에 달려 있습니다(TODO). simulator 쪽 다섯 항목과 loader 수정은 인경민이, `c6-dual` records 비용의 대응은 Phase 10에 인지오가 정합니다. trace-replay 점검의 실행 결과에 따라 "what a disagreement leads to"가 이미 gate spec에 고정되어 있어야 한다는 것이 TODO 줄의 조건입니다.

## 12.5 Backlog

Backlog의 데이터셋 관련 줄은 다섯입니다.

**naturalistic generator와 generalset.** "Naturalistic generator + generalset + full condition matrix — its prerequisite is a source for Linux-desktop co-occurrence and transition frequency, which 9.10's search did not find (audit record 2026-10-11)." 2026-08-26 grill D18의 build 순서 (7)이 아직 남아 있는 것입니다. 전제 조건은 출처입니다. 9.10 D35는 hub-and-spoke 전환을 "unsourced"로 표시하고 "left to the naturalistic generator's own search"로 남겼습니다.

**hold time과 hysteresis.** 계획(`_dev/docs/plan/jioh/hold-time-and-hysteresis.md`)의 목표는 "Decide whether the daemon needs flap protection, and if so fix the policy's form and values before the RQ4 run, with the values chosen on files disjoint from the ones measured." step 3(선례 검색)은 9.19의 spec session에서 끝났고(5–30 s), 규칙 없이 필요를 재는 측정의 재료(flap-stress set, return grid, `flip_cost` 보고 줄)는 9.19와 9.21이 만들었습니다. 남은 것은 둘입니다. 첫째는 그 측정, 계획의 step 1입니다. "the need measured with no rule — the flap-stress set and the C4 files under `oracle` and `random`, the wrong-flip count and its Layer 2 cost — right after Phase 10's integration, in the RQ0 run's pipeline; no LLM needed. If the cost is below the floor the plan ends there and daemon guide §9.3 records the measurement." 둘째는 steps 2, 4, 5, 6이고 "in the RQ4 experiment spec's session, after step 1 and before any LLM condition runs"입니다. 2026-10-14의 TODO는 이 측정을 step 0, 나머지를 steps 1, 2, 4, 5, 6이라고 적었는데, 계획 안에서 When 표와 Steps 목록의 번호가 달랐기 때문입니다. 2026-10-16에 인지오가 Steps 목록의 번호(step 1)로 정했고(9.15 작업 목록 W-0481), TODO의 두 줄이 그렇게 고쳐졌습니다. 계획의 When 표는 개발 기록으로 남아 0이라고 적습니다.

**form-2 return grid.** "A form-2 return grid (A stays, the focus moves to B and back; 9.19 spec, open item): not built; decided in the RQ4 experiment spec's session if that run needs it — a form axis on `dataset/grids.yaml`'s return-grid, 720 files more, its own re-bless."

**측정할 원치 않는 job.** "how many the attribute's `false` side needs is decided in the RQ1 experiment spec's session; the campaigns run after Phase 10's RQ0 run and before the RQ1 run (today the ten interactive counterparts share one name, `unattended-upgr`; 9.20 decision 9)." 후보는 `gnome-software` + `packagekitd`, `snapd` 자동 갱신, `updatedb.plocate`, `update-initramfs`, `mandb`와 `apt-get update`입니다.

**held-out-rows arm.** "after the main experiments, on the calibrated table: blank a row to the schema defaults, compare `llm_vocab` and `llm_algo` on the files that exercise it." 설계는 Phase 7(2026-09-10)에 고정되었습니다. 전제 조건은 "Needs the calibrated table, whose per-row tuning pool must itself cover all 32 cells … the throwaway pool's definition (7.7 / Phase 8) decides that."

> **열린 자리.** 다섯 backlog 항목은 모두 정할 자리가 정해져 있습니다. naturalistic set은 출처가 생길 때, hold time의 규칙 없는 측정(step 1)은 Phase 10 통합 직후, 나머지 hold time steps와 form-2 return grid는 RQ4 실험 spec session에서, 원치 않는 job의 개수는 RQ1 실험 spec session에서, held-out-rows arm은 calibrated table이 생긴 뒤입니다. 모두 인지오가 정합니다.

## 12.6 executor 질문들 — 두 방향

"세 개의 executor 질문"은 기록에 두 묶음이 있습니다. 하나는 인지오가 인경민에게 물은 것이고(2026-09-13), 다른 하나는 인경민이 인지오에게 물은 것입니다(2026-10-10).

**인지오가 인경민에게 물은 셋 (heads-up memo §4, Phase 9 결정 7).**

1. **LOTTERY — editor 자신의 burst 꼬리가 batch class일 때 batch share는 어떻게 나뉘나.** 이 질문의 전제는 2026-09-13의 compile된 editor가 "CPU의 91–92%가 burst 첫 10 ms 뒤"에 있었다는 것입니다. 그 뒤 9.5가 editor를 측정한 entry로 바꿨고, 9.14 결정 8은 prior table의 문장을 "the measured per-keystroke work (about 5 ms for the writer and the mail client, about 78 ms for VS Code …)"로 다시 썼습니다. 인경민이 글로 적은 답은 이 권이 읽은 기록에서 찾지 못했지만, 답은 reference simulator의 code에 있습니다. `simulator/src/sim.cpp`의 LOTTERY 주석은 "tickets split batch : non-batch = share : (1−share), equal tickets per task within a class … ① if both classes are runnable, pick the class by share; ② pick uniformly inside it. Only runnable tasks hold tickets"라고 적습니다. 즉 class 안에서는 모든 task가 같은 표를 가지고, editor 자신의 burst 꼬리가 batch class일 때도 마찬가지입니다. 2026-10-16에 9.15가 prior table의 compile row 문장을 이 규칙으로 고쳤고, driver table의 pin이 `0fba4b3c…`가 되었습니다(값은 그대로, 9.15 작업 목록 W-0777). 인경민의 2026-10-10 memo는 cap에 대해 "**not implemented.** The field is not read from the config. B1 currently acts only through LOTTERY's class split"이라고 적습니다.
2. **EDF — frame chain의 stage는 deadline class인가 residual class인가.** 답이 있습니다. 인경민의 2026-10-10 memo는 "Answered on 2026-10-10: the EDF chain-stage class (deadline class, inherited deadline, no change)"라고 적고, audit은 conformance 항목 (f) "chain stages in EDF's deadline class"를 "implemented"로 적습니다.
3. **editor가 아직 RUN 중일 때 키 입력이 오면.** contract 쪽의 답은 9.14 결정 1이 소비자의 기준으로 정한 "the zero-wait `ready` line"입니다. 구현은 빚입니다. 인경민의 memo는 "RUN→RUN boundary fix: one occupancy, zero-wait `ready(cause)`, `x_run_cont`"를 "Implementation owed"에 넣었고, audit은 conformance 항목 (a)를 "owed"로 적습니다.

**인경민이 인지오에게 물은 셋 (2026-10-10 memo, "Questions for jioh").**

1. **TIMER backlog 대 frame drop.** 2026-09-29의 note에 대해 인지오의 memo(2026-10-07)가 "TIMER's backlog rule is replaced by a skip rule"이라고 답했습니다. 다만 9.15 spec 결정 9가 적듯이 simulator는 지금도 backlog 규칙을 돌리고 있고, skip 규칙의 구현은 인경민의 빚입니다.
2. **`fork_cap`의 의미.** note(`simulator/notes/note1010.md`)는 "is `fork_cap` what makes child birth times emergent?", 필드가 없을 때의 의미, 그리고 critical finding B3(측정된 동시 compiler process 16)을 묻습니다. 인경민의 memo는 현재 동작을 "`fork_cap` absent: treated as unbounded"로 적습니다. 답은 9.6 D19(2026-09-19, 인지오의 결정)에 있습니다. 형식에서는 top-level task만 task를 만들 수 있고 "`fork_cap` bounding its live children"이며, object job 하나는 여섯 구성원(`sh`, `gcc`, `cc1`, `as`, `fixdep`, `rm`)의 spawn-table entry입니다. 그래서 compiler는 `fork_cap`을 `parallelism_cap` × 6으로 쓰고(`dataset/tools/wlc/compiler.py`의 `_orchestrator_unroll`, "jobs in flight, six members each"; `-j8`이면 48), 동시에 도는 job 수를 make의 jobserver처럼 묶습니다. child가 언제 태어나는지는 slot이 비는 때이므로 scheduling이 정합니다. compiler는 spawn table을 가진 모든 `arrive` event에 `fork_cap`을 쓰므로(`_arrive_event`) 필드가 없는 경우는 compile된 파일에 생기지 않고, simulator는 그것을 event에서 읽습니다(`simulator/src/sim.cpp`의 loader).
3. **`mock-switch` Q1–Q3.** `mock-switch`는 FIFO에서 MLFQ로 바뀌는 순간을 손으로 계산해 둔 harness의 mock fixture입니다(Phase 6의 6.1). 인경민의 memo는 세 질문을 "Q1 (44600 vs MLFQ rule 2), Q2 (lone slice expiry: one occupancy or a pair), Q3 (guide §4½ needs a fifth instruction)"으로 요약합니다(note1010.md의 마지막 절). 셋 다 답이 있습니다. Q1은 mock이 틀렸습니다. 44600에 editor가 Q1으로 내려가면 Q0에서 기다리던 `probe`가 lane을 받아야 하고(MLFQ 규칙 2), 2026-10-16에 9.15가 fixture를 그 시점부터 다시 유도했습니다(커밋 `d5443eb0`, 9.15 작업 목록 W-0804). Q2는 2026-10-16에 인지오가 "한 번의 점유"로 정했습니다(W-0736). 다른 task가 실행 가능하지 않을 때 slice가 끝나면 holder를 내리고 lane에 그대로 두며, `run_end`/`run_start` 쌍을 내지 않습니다. 근거는 Linux v6.12 `kernel/sched/core.c`의 `__schedule()`(같은 task를 다시 고르면 context switch로 세지 않음, `docs/references.md`의 `linux-sched-core`)이고, mock과 그 `expected.csv`는 그대로입니다. trace 계약이 frozen이므로 이 규칙은 최종 memo가 인경민과 박이안에게 제안하고, 동의하면 계약 문서에 들어갑니다. Q3는 9.23 D16이 답했습니다. 편집기의 program이 끝에 WAIT를 하나 더 가지게 되어, guide §4½의 "next instruction WAIT → blocks"가 맞게 되었습니다.

audit의 "Recommended order before 9.15 proper"는 첫 항목으로 "Heads-up to 경민 now on the loader refusal (blocker 1) with the counts and the contract reading; answer his three open questions"를 적었습니다. 2026-10-14에 이 권은 그 heads-up과 답을 보냈는지를 열린 자리로 적었습니다. 인지오의 답은 "보내지 않았다"입니다(2026-10-16, 9.15 작업 목록 W-0735). 최종 memo가 loader의 child-targeted WAKE 거부를 인경민에게 처음 알리고, 위의 답들(인지오가 물은 셋이 모두 답해졌다는 것과 인경민이 물은 셋의 답)을 전합니다. 최종 memo는 9.15의 마지막 단계이고 2026-10-17에는 아직 쓰이지 않았습니다.

## 12.7 spec과 handoff에 남은 작은 열린 항목들

- **driver table의 tuning set.** Phase 7 spec의 열린 항목. "The driver table tuning set … the calibrated table is tuned on is undefined in every document … *Phase 8 (8.8) renamed it and deferred its composition past Phase 9.*" held-out-rows arm의 전제 조건이기도 합니다. 정할 사람은 인지오입니다.
- **`linux-sched-bwc` reference.** Phase 7 archive. cap의 배포된 대응물인 Linux CFS bandwidth control의 entry가 "proposed, not added"입니다.
- **9.7 handoff의 두 항목.** "The block per run is a marginal value. It has sat between ±10.4 % and ±12.5 % against its 1 µs floor for a dozen repeats …. Whether it belongs under the rule's machine-spread exception (9.6 D29) was never put to 인지오." 그리고 "The unshaped phase's `perf.data` truncation is undiagnosed (repeat 33)." 정할 사람은 인지오입니다.
- **9.5 handoff의 두 항목.** "`dataset/tools/meas/desktop/run.sh` line 162 still reads `app.affinity` at launch", 그리고 `.github/workflows/meas-gui.yml`이 은퇴해야 한다는 것입니다.
- **Phase 8 handoff.** "Layer 1 is underpowered for the whitelist comparison at 44 to 49 independent units"와, run 간 일관성이 "blocked on the recognition log's missing repeat index"라는 것입니다. 후자는 박이안의 recognition log 형식과 관계됩니다.
- **9.10 D35.** "Hub-and-spoke switching: unsourced, left to the naturalistic generator's own search."
- **사전 등록된 조건부 재측정.** 9.14 결정 3의 "The re-measurement of the exception-carried values (pid 1's run mean and the system bus's three values, 9.9 D48; the editor's `utility/libuv-worker` wake rate and gap mean, 9.5 D99; the desktop slice's machine-speed exceptions, 9.8 D28) is a pre-registered contingency." 조건이 맞을 때만 실행됩니다.

## 12.8 문서와 tree의 불일치 (2026-10-14 현재)

마지막으로, 2026-10-14에 공개 문서가 그때의 데이터셋과 다르게 말하던 곳을 적습니다. 이것들은 모두 9.15의 작업 목록에 있거나 들어갈 항목이었고, 9.15 spec 결정 3에 따라 code와 data가 이깁니다. 이 시리즈의 각 권은 이 경우 tree의 값을 씁니다. 앞의 세 열은 2026-10-14의 표이고, 마지막 열은 2026-10-17에 다시 읽은 상태입니다(guidebook과 memo 밖의 공개 문서).

| 문서가 말하는 것 (2026-10-14) | tree의 사실 | 확인한 곳 | 2026-10-17 |
|---|---|---|---|
| core set 50개, segment 64개(building plan, background guide, coreset guide 등) | 51개, 66개 | `build.manifest.json` 51개, `coverage-grid.json`의 `segments_total` 66 | 고쳐짐. tree는 이제 51개, 67개(9.23 D2가 `c6-spoof`를 20 s에서 둘로 나눔; `coverage-grid.json`의 `segments_total` 67). building plan과 coreset guide가 51개, 67개를 적고(9.15), background guide에도 50과 64가 남지 않음. `docs/README.md`의 coreset guide 설명 줄에는 "all 50 coreset files"가 남아 있음 |
| archetype 열두 개(`docs/data-contracts.md` §2의 "There are twelve" 등) | 29개, 그중 28개 측정 | `dataset/archetypes.yaml`의 key 29개 | 고쳐짐. data contracts §2와 coreset guide가 29개를 적음(9.15). `docs/README.md`의 coreset guide 설명 줄에는 "the twelve archetypes"가 남아 있음 |
| library v0.1(`archetypes.yaml` 첫 줄) | v0.2로 정함(9.13 결정 9) | `dataset/archetypes.yaml:1` | 고쳐짐. 첫 줄이 "(v0.2)"(2026-10-16, 커밋 `37c2e233`, 11.5) |
| demand window를 규칙으로(`dataset/README.md`, interpretation contract §7 등) | 2026-10-09에 gate에서 물러남, 기록만 | 9.14 결정 4, `dataset/tools/wlc/estimate.py` | 고쳐짐. README의 규칙 "Demand is reported, not held"와 contract §7의 "reported, not held"(9.15) |
| TIMER의 backlog 규칙(interpretation contract §3, `docs/data-contracts.md`) | harness는 skip 규칙을 읽고, simulator는 아직 backlog | 9.15 spec 결정 9 | 그대로. 문서는 simulator가 skip 규칙을 구현할 때까지 backlog 규칙을 적고, 그 정정은 Phase 10의 TIMER 줄에 있음(12.4) |
| 두 compile mode, `coreset-native` | single 하나 | 9.13 D1 | 고쳐짐. building plan, coreset guide, contract §7이 single 하나를 적음(9.15) |
| C7의 원치 않는 job `clamscan` | `package-upgrade`(`unattended-upgr`) | 9.10 D3 | 고쳐짐. building plan, scenario catalog의 S17(무인 업그레이드), coreset guide(9.15) |
| RQ0 judging 25개, K = 13 | 19개, K = 10 | `harness/experiments/rq0-gate.yaml` | guidebook과 memo 밖의 공개 문서에 남은 곳 없음(grep) |
| `c5-t3` | `c6-alias` | 9.20 D8, `dataset/timelines/coreset/` | 고쳐짐. coreset guide가 `c6-alias`를 적고, 남은 `c5-t3`는 날짜가 붙은 기록(data contracts §14의 2026-10-12 항목, coreset guide의 내력 문장, harness guide(`docs/harness/harness-and-records-guide.md`)의 familiarity tier 문단에 붙은 괄호)뿐임 |
| README 예시의 attribute `wanted` | `background_wanted` | 2026-08-28 archive, critical finding C | 고쳐짐(README, 9.15) |

# 13장 · 한 장짜리 연표

이 장은 "언제 무슨 일이 있었고, 그 기록은 어디에 있나"를 한 표로 보여 줍니다. 날짜는 기록에 적힌 날짜이고, 하루에 여러 일이 있으면 한 줄에 모았습니다. 경로는 저장소 root 기준입니다.

| 날짜 | 사건 | 기록 |
|---|---|---|
| 2026-08-23 | 설계 회의. 의제 여섯과 질문 Q1–Q8(코어 수, segment framing, workload set의 기준) | `_dev/archive/2026-08-23-design-meeting-open-questions.md` |
| 2026-08-26 | workload-generation grill D1–D22. Q1을 single core로 결정. demand-budget rule, 네 artifact, TIMER, D12의 지배 원칙. 같은 날 addendum(Mark 수치 재귀속, `ocallahan-atc17` 식별) | `_dev/archive/2026-08-26-workload-generation-grill.md` |
| 2026-08-26 → 08-27 | Phase 1: references, registry, interpretation contract, building plan과 archetype plan 재작성, 팀 memo | `_dev/docs/spec/jioh/phase-1-workload-dataset-groundwork.md`; `_dev/TODO.md` Phase 1 |
| 2026-08-27 | Phase 2 spec session. 2.3의 timeline 형식(세 track, keyed substream, lockfile, demand window hard-fail). grill의 이유는 archive되지 않음 | `phase-2-…`, `task-2.3-timeline-compiler.md` |
| 2026-08-28 | 2.4 core timelines 24개(13 novel + 11 derived), 48 artifact, grid 서명. 2.6 meas-ci, release `meas-ci-2026-08-28`. 2.5 저장소 준비, vocabulary 16 mode, `background_wanted`, config schema와 trace freeze | `task-2.4-…`, `task-2.6-…`; `_dev/archive/2026-08-28-task-2.5-repo-prep-and-contracts.md` |
| 2026-09-06 | Phase 3: 수요를 manifest에, judging set = C2 여섯, `c6-dual` finding, `c1-idle` 수정, 다섯 contract freeze | `_dev/archive/2026-09-06-phase-3-verification-and-protocol-freeze.md` |
| 2026-09-07 → 09-09 | Phase 4–6. `familiarity`가 compile을 통과, scoring spec, pair review finding 2(17/32 cell) | `_dev/archive/2026-09-07-phase-5-primitive-metrics.md`; `docs/daemon/prior-table-pair-review.md` |
| 2026-09-09 | Phase 7 spec session, 결정 1–13(32개 cell, C7, `clamscan`, grid 강제) | `_dev/docs/spec/jioh/phase-7-coreset-attribute-coverage.md` |
| 2026-09-10/11 | 7.1–7.7: 50개 파일, 100 artifact, judging set 27(결정 14), 팀 memo | `_dev/archive/2026-09-11-phase-7-coreset-attribute-coverage.md`; `docs/memos/2026-09-10-coreset-before-and-after-phase-7.md` |
| 2026-09-11/12 | Phase 8: boot default를 OSTEP에서, RQ0 gate spec commit(25개, K 13, 아홉 점) | `_dev/TODO.md` Phase 8; `harness/experiments/rq0-gate.yaml` |
| 2026-09-13 | 원문 대조 검증, critical findings A1–D, 예고 memo, Phase 9 spec 결정 1–8, 9.1·9.2·9.3, slice workflow, 9.4 D1–D8 | `docs/memos/2026-09-13-critical-findings.md`; `docs/memos/2026-09-13-dataset-rebuild-heads-up.md`; `_dev/docs/spec/jioh/phase-9-workload-dataset-rebuild.md`; `_dev/research/jioh/` |
| 2026-09-14/15 | 9.5 D1–D20: 측정한 아홉 entry가 몽타주 세 entry를 대체 | `_dev/research/jioh/task-9.5-interactive-typing/changelog.md` |
| 2026-09-16 | 9.5 follow-ups grill: CPU 하나, wake 정의, scale 한계, native set 버림 | `_dev/docs/spec/jioh/task-9.5-interactive-typing-follow-ups.md` |
| 2026-09-17/18 | 9.6 첫 compile campaign, 다시 시작(D10–D11), machine gate. 9.5 D26 같은 기계 campaign. 9.4 D9 | `task-9.6-compile/changelog.md`; `task-9.5-…/changelog.md` |
| 2026-09-19 | 9.7 D1–D21(나누기, send operation, `background-crawler` 은퇴, wake 판정). 9.6 D16, D19. 9.5 D29 | `task-9.7-background-io/changelog.md` |
| 2026-09-20 | 9.8 D1(`electron-comms` 나누기). 9.6 D31 fold-in. validity review memo | `task-9.8-browser-comms/changelog.md`; `docs/memos/2026-09-20-dataset-validity-review.md` |
| 2026-09-22 → 09-25 | 9.8 D25, 9.7 D31/D34, 9.9 D1–D26 fold-in(`system-daemon` 나누기, `xorg` 은퇴), 9.9 D32 | 각 changelog; release `meas-ci-session-2026-09-24` |
| 2026-09-26 | 9.5–9.9 검토: 9.5 D74(TIMER는 선언된 주기에만), 타당성 위협 문장, trace-replay 점검 | `task-9.5-…/changelog.md`; `_dev/TODO.md` 9.15, Phase 10 |
| 2026-09-27 | untraced control grill, release `meas-ci-control-2026-09-27` | `_dev/docs/spec/jioh/task-9.5-untraced-control.md` |
| 2026-09-28/29 | coverage sweep, 9.8 D33, 9.5 D99 | `_dev/TODO.md` 9.16; 각 changelog |
| 2026-10-01 | 9.10 D1–D35: `zhang-chb15` 삭제, task 집합은 design, `clamscan` → 무인 업그레이드, job을 통째로, `source` 규칙. 9.9 D47(되돌림) | `task-9.10-scenarios-timelines/changelog.md`; `_dev/docs/spec/jioh/task-9.10-scenarios-timelines.md` |
| 2026-10-02 → 10-06 | 9.10 campaign: DKMS, Tracker, MNIST, HandBrake, Kdenlive, Déjà Dup, Chrome tab, launch, span. D141 build 통째로 | `task-9.10-…/changelog.md`; `bound-values.md` |
| 2026-10-07 | 9.10 끝(D174). 9.11 D3 skip 규칙, D4–D6 declared class. TIMER memo | `task-9.11-scheduler-constants/changelog.md`; `docs/memos/2026-10-07-timer-skip-rule-for-the-simulator.md` |
| 2026-10-08 | declared class memo(9.11 D18). 9.12 시작 | `docs/memos/2026-10-08-declared-scheduling-class.md`; `task-9.12-related-work-prose/changelog.md` |
| 2026-10-09 | 9.13 grill, rebuild, bless(51개, 681 MB, 4,522,200 wake). 9.14 grill: demand window 은퇴, judging 19, K 10, variant 78 | `_dev/docs/spec/jioh/task-9.13-rebuild.md`; `task-9.13-rebuild/changelog.md`, `reads.md`; `task-9.14-consumer-rework.md` |
| 2026-10-10 | 9.14 끝(D13–D14 runner 수정). audit 시작(`fe19be86`). 인경민의 simulator memo | `task-9.14-consumer-rework/changelog.md`; `_dev/docs/audit/jioh/2026-10-10-dataset-audit-before-9.15.md`; `simulator/memo/memo_261010.md` |
| 2026-10-11 | audit 해결(A1 ii, A3 그대로)과 방향(generated layer, focus, C4·C5·C2). Phase 9 결정 9–10, TODO에 9.17–9.22. 9.17 focus, 9.18 gate, 9.22 build 시간(CI 38131040159), 9.19 grid 480/720/24(CI 38135623993) | audit 기록; 각 spec과 changelog |
| 2026-10-12 | 9.20: distractor 272, ladder 66, `c5-t3` → `c6-alias`(CI 38243554308) | `task-9.20-c4-and-c5-grids.md`; changelog |
| 2026-10-13 | 9.21 grill과 작업: 규칙에 의한 채점, coverage 표, `files.select`, `flip_cost`, 매 run build | `task-9.21-consumer-work-for-the-generated-layer.md`; changelog |
| 2026-10-14 | 9.21 D13 `coreset_wide` marker, harness run 38547043521 초록. 9.15 grill → spec, WIP. simulator 쪽 TIMER 행을 Phase 10으로. 이 guidebook의 발견 목록, 9.23 grill과 D1–D10(C6의 pre-committed miss, segment 67개, rebuild) | `task-9.21-…/changelog.md`; `task-9.15-docs-memos-and-guidebook-corrections.md`; `_dev/TODO.md`; `_dev/docs/audit/jioh/2026-10-14-guidebook-findings.md`; `task-9.23-guidebook-findings/changelog.md` |
| 2026-10-15 | 9.23 D11–D18: launch stream을 inputs에, `check`가 파생 timeline과 coverage grid도, `make lint`의 freeze, canonical lint 셋, requirements 고정과 smoke는 손으로, program이 depart 전에 끝나지 않게. rebuild(CI 38722675475, 38722678829) | `task-9.23-guidebook-findings/changelog.md`; `harness/CHANGELOG.md` |
| 2026-10-16 | 9.15: 작업 목록의 질문에 대한 인지오의 답(일부는 2026-10-15). 그 답의 data와 code 수정을 묶은 rebuild(쓰이지 않는 compile 경로 삭제, bound value의 freeze, release map, 머리 주석과 library v0.2), driver table re-pin | `_dev/research/jioh/task-9.15-docs-memos-and-guidebook-corrections/work-list.md`; `harness/CHANGELOG.md` |
| 2026-10-17 | 9.15: 정정 작업이 찾은 data와 code 수정을 다시 묶은 rebuild(generated layer의 scenario tag를 9.10 D168의 한 규칙으로, corner set이 숨은 탭 renderer의 조용한 thread 둘까지 쓸어 봄, library의 머리 주석과 notes, schema의 설명, `c1-idle`의 머리 주석, code의 주석과 docstring), 일곱 manifest re-bless, dataset과 variants re-pin | `_dev/research/jioh/task-9.15-docs-memos-and-guidebook-corrections/logs/B1-data-rebuild.md`; `harness/CHANGELOG.md` |

# 14장 · 용어 정리

이 권에서 처음 쓰기 전에 풀이한 용어를 모았습니다. 두 종류로 나눕니다. 이 저장소가 만들었거나 자기 뜻을 붙인 **프로젝트 용어**와, 웹 개발에서 보통 만나지 않는 **OS와 scheduling 용어**입니다.

## 14.1 프로젝트 용어 — 기록과 작업 단위

- **phase** — `_dev/TODO.md`의 인지오 section에 번호가 붙은 작업 단위입니다. 데이터셋과 직접 관계된 것은 Phase 1, 2, 3, 7, 9입니다.
- **sub-task** — phase 안의 작업입니다. "phase 번호.순번"(예: 9.13)으로 부릅니다.
- **`_dev/TODO.md`** — 사람마다 section이 있는 팀 전체의 작업 목록입니다.
- **grill** — 질문을 하나씩 던지고 답하며 결정을 고정하는 질의응답 세션입니다.
- **spec** — grill이 끝난 뒤 결정만을 적은 문서입니다. phase spec과 task spec이 있고, "Locked decisions"에 번호가 붙습니다.
- **archive** — 결정 세션의 기록입니다. 결정, 이유, 확인한 사실을 적습니다. `_dev/archive/`에 있습니다.
- **research slice** — Phase 9의 9.4–9.12입니다. 영역마다 하나씩 연구하고 결정합니다.
- **scope card** — slice가 다룰 항목의 목록입니다. 항목마다 현재 값, tag, 검증 판정, 종류를 적습니다.
- **changelog** — slice의 결정 기록입니다. 결정마다 `## Dn` heading이 붙습니다.
- **memo** — 팀원에게 보내는 글입니다. `docs/memos/`에 있습니다.
- **audit** — 데이터셋을 독립적으로 점검한 기록입니다.

## 14.2 프로젝트 용어 — 데이터셋의 구성

- **workload** — 실험 하나가 돌리는 입력 JSON 파일입니다(`*.workload.json`). canonical workload라고도 합니다.
- **timeline** — 사람이 쓰는 원본 파일입니다(`*.timeline.yaml`). compiler가 workload로 바꿉니다.
- **archetype** — 프로그램 하나의 행동 방식을 값과 근거로 담은 library entry입니다(`dataset/archetypes.yaml`).
- **segment** — 정답 label이 변하지 않는 workload의 시간 구간입니다.
- **mode** — segment에서 사용자가 하는 일의 이름입니다. 열여섯 개가 있습니다.
- **`background_wanted`** — 그 segment의 배경 작업을 사용자가 원했는지를 나타내는, 데이터셋이 채점하는 유일한 attribute입니다.
- **driver table** — mode와 `background_wanted`의 조합마다 scheduler 설정을 적은 32행의 표입니다.
- **cell** — driver table의 한 조합(mode × `background_wanted`)입니다.
- **core set (coreset)** — 손으로 쓴(또는 recipe로 파생한) 51개 timeline의 묶음입니다. 파일 묶음 C1–C7로 나뉩니다.
- **C1** — 상황 하나만 담은 단일 segment base 파일 묶음입니다. 지금은 mode마다 하나, 열여섯 개입니다.
- **C2** — 의도(`background_wanted`)만 다른 두 파일의 쌍입니다. P1, P2, P3의 세 쌍입니다.
- **P1 pair** — C2의 첫 쌍입니다. ML 학습(원함) 대 색인(원치 않음)입니다.
- **C3** — 여러 mode를 이어 붙인 하루의 흐름(arc) 파일입니다. 지금은 existence case입니다.
- **C4** — label을 바꾸지 않는 방해 요소(distractor)를 넣은 파일입니다. 지금은 existence case입니다.
- **C5** — 이름의 친숙도를 바꾼 파일입니다. 지금은 `c5-t4`, `c5-t5`가 있습니다.
- **C6** — 이름으로는 원리적으로 맞힐 수 없는 경우(resolution limit)의 묶음입니다. `c6-dual`, `c6-fold`, `c6-spoof`, `c6-alias`가 있습니다. `c6-alias`는 전체가, `c6-fold`와 `c6-spoof`는 뒤 segment가 pre-committed miss이고(9.23 D1, D2), `c6-dual`의 segment는 `ambiguous`입니다.
- **C7** — attribute counterpart 묶음입니다. C1 base마다 하나씩, 그 mode의 `background_wanted: false` 쪽을 담은 열여섯 파생 파일입니다. base의 처음 C초이고, 원하지 않은 배경 작업을 더하거나 base의 job을 아무도 원하지 않은 것으로 둡니다.
- **counterpart** — base 파일에서 한 가지만 바꿔 파생한 짝 파일입니다.
- **familiarity tier** — process 이름이 얼마나 알아보기 쉬운지를 1–5로 나눈 등급입니다.
- **pre-committed miss** — 어떤 관찰자도 맞힐 수 없다고 미리 선언하고 정확도 채점에서 빼는 segment입니다.
- **coverage grid** — core set의 segment가 cell과 tier를 얼마나 채우는지 세는 표입니다(`dataset/coverage-grid.json`).
- **deriver** — recipe(variant spec)를 읽어 base timeline에서 파생 timeline을 만드는 도구입니다.
- **manifest** — build 결과물의 SHA-256 hash와 입력을 적은 commit된 파일입니다. lockfile과 같은 역할입니다.
- **demand class** — 파일이 수요 창의 검사를 받는지 정하던 표시입니다. `calibration`은 면제, `oversubscribed`는 대상이었습니다.
- **utilization** — 파일의 task들이 원하는 CPU 시간의 합을 파일 길이로 나눈 값입니다. manifest의 `demand`에 기록됩니다.
- **demand-budget rule / demand window** — 파일의 수요가 lane의 약 100–150 % 안에 있어야 한다던 규칙입니다. 2026-10-09에 gate에서 물러났습니다.
- **primitive** — workload 안의 program이 쓰는 기본 명령(RUN, SLEEP, TIMER, WAIT, WAKE, FORK와 EXIT)입니다.
- **interpretation contract** — simulator가 workload를 어떻게 실행해야 하는지 적은 문서입니다.
- **lane-scaling pass** — 여러 코어에서 잰 CPU 사용량을 lane 하나에 맞게 줄이는 compile 단계입니다.
- **native / single** — lane-scaling을 하지 않은/한 compile mode입니다. 지금은 single 하나만 있습니다.
- **generalset** — core set 옆에 naturalistic generator로 만들 예정이던 timeline 묶음입니다. backlog에 있습니다.
- **chain** — 앞의 task가 다음 task를 깨우는 순서로 연결된 task들입니다. 게임의 frame을 만드는 `game-task-chain`이 대표입니다.
- **object job** — make가 C 소스 파일 하나를 object 파일로 만드는 단위입니다. 데이터셋에서는 spawn-table entry 여섯 개로 씁니다.
- **operation** — 프로그램의 무거운 작업 한 번(filter, preview render, page load, mail send)을 측정한 단위입니다.
- **component** — 측정된 archetype 안에서 thread 종류 하나의 wake 간격과 run 길이 분포입니다.
- **stimulus** — 측정이나 compile 때 프로그램에 넣는 입력(키 입력의 시각 열)입니다.
- **SWELL-KW** — 사무 작업 중의 키 입력을 기록한 공개 데이터셋입니다. 데이터셋의 키 입력 stream이 여기서 옵니다.
- **variant** — core set의 파일을 정해진 변환으로 바꾼 민감도 점검용 파일입니다. 78개가 있습니다.
- **replay** — 측정된 반복 하나에서 관찰한 stream을 그대로 재생해 task를 만드는 방식입니다. stream은 entry에 따라 wake 순서(`wakes`), batch job의 run과 그 뒤의 block(`runs`), 주기 task의 cycle(`cycles`)입니다.
- **generated layer** — 생성기로 만드는, 현실성을 주장하지 않고 요인을 빠짐없이 나열한 파일 묶음입니다. 1,562개입니다.
- **existence case** — "이런 상황이 존재한다"만 보여 주는 파일입니다. 비율의 표본이 아닙니다.
- **240개 순서쌍** — 열여섯 mode에서 서로 다른 두 mode를 순서 있게 고르는 경우의 수(16 × 15)입니다.
- **transition grid** — 모든 mode 순서쌍의 전환을 두 형태로 나열한 480개 파일입니다.
- **return grid** — A → B → A 세 segment 파일 720개입니다. 가운데 길이를 60 s, 10 s, 2 s로 바꿉니다.
- **flap / flap-stress set** — 설정이 적용되었다가 곧 되돌아가는 것 / process 집합이 짧은 간격으로 여러 번 바뀌는 24개 파일입니다.
- **hold time / hysteresis** — 설정 적용 뒤 N초 동안 새 답을 무시하는 규칙 / 같은 답이 K번 연속이어야 적용하는 규칙입니다.
- **familiarity ladder** — C1 task set의 이름을 tier 4와 5의 이름으로 바꾸고, render와 backup의 job은 tier 3의 이름(`melt-7`, `duplicity`)으로도 바꾼 66개 파일입니다.
- **canonical set** — 구조적 정보(조상, cgroup, 이름의 동일성)만으로 접은 process 집합입니다. 그 변화가 의미 있는 변화입니다.
- **headroom** — 좋은 설정과 나쁜 설정의 결과 차이가 날 여지입니다.
- **discriminative construction** — 경쟁 가설을 서로 갈라놓도록 workload를 일부러 구성한다는 기준입니다.
- **admission checklist** — workload set이 충분히 강한지 보는 2026-08-23의 네 항목입니다.

## 14.3 프로젝트 용어 — 측정과 출처

- **meas-ci** — GitHub Actions runner에서 하는 이 프로젝트의 측정입니다. campaign은 `meas-ci:<family>:<date>`로 인용합니다.
- **CI runner** — GitHub Actions가 workflow를 돌리는 가상 기계입니다.
- **fold-in** — 측정 결과를 `dataset/archetypes.yaml`의 값으로 옮기는 commit입니다.
- **machine gate** — job이 정해진 CPU model(AMD EPYC 7763)이 아니면 재지 않고 멈추는 장치입니다.
- **stability rule** — 같은 기계의 반복 평균에 대한 95 % 신뢰구간 반폭이 5 %(또는 1 µs) 이하가 될 때까지, 최소 다섯 번 반복하는 규칙입니다.
- **pin to one CPU** — 측정 대상 process를 CPU 하나에서만 돌게 묶는 것입니다.
- **claim** — 출처를 근거로 하는 주장 하나입니다.
- **locator** — 출처 안의 위치(쪽, 절, 슬라이드, 코드 줄)입니다.
- **placeholder** — 측정이나 출처 없이 임시로 채운 값입니다.
- **design** — 출처가 아니라 실험 설계자가 고른 값이라는 label입니다.
- **Xvfb** — 화면 없이 그래픽 프로그램을 돌리는 가상 X 서버입니다.

## 14.4 프로젝트 용어 — 실험과 소비자

- **recognizer** — process 이름 목록을 읽고 mode와 attribute를 맞히는 쪽입니다.
- **simulator / daemon / harness** — workload와 설정 일정을 받아 CPU 하나의 실행을 흉내 내는 프로그램(인경민) / recognizer를 돌려 설정 일정을 내는 프로그램(박이안) / trace를 채점하고 RQ0을 판정하는 도구(인지오)입니다.
- **trace** — simulator가 실행 중 일어난 scheduling 사건을 한 줄씩 적은 출력 파일입니다.
- **campaign** — CI runner에서 같은 측정을 여러 번 반복한 한 묶음입니다. raw 기록은 GitHub release로 공개합니다.
- **critical finding** — 2026-09-13의 원문 대조 검증이 찾은, 데이터셋의 근거가 틀렸거나 빈 곳에 대한 지적입니다. A1–A5, B1–B7, C의 열세 개이고, 함께 실린 D는 원문과 대조하지 못한 출처의 목록입니다.
- **oracle / random / fixed** — 정답을 그대로 답하는 / 무작위로 답하는 / 기본 설정 하나만 쓰는 비교 조건입니다.
- **whitelist** — 프로그램 이름마다 규칙을 미리 적은 표로 상황을 정하는 비교 조건입니다. 지금은 `shipped_catalogue`와 `strongest_name_table`로 나뉩니다.
- **RQ0** — 정답을 알면 무작위보다 결과가 측정 가능하게 좋아지는가를 묻는 첫 관문 질문입니다.
- **RQ1–RQ5** — 상황을 맞히는가 / 맞히면 좋아지는가 / 어휘가 충분한가 / 지연을 감안해 얼마나 지속되어야 이득인가 / driver table이라는 도구가 건전한가를 묻는 연구 질문입니다.
- **RQ0 gate spec** — RQ0을 판정하는 규칙 파일입니다(`harness/experiments/rq0-gate.yaml`).
- **judging set** — RQ0 판정에 쓰이는 파일들입니다. 지금 19개입니다.
- **K와 g** — 판정 파일 중 K개 이상에서 gap이 g 이상이어야 한다는 통과 기준입니다. 지금 K = 10, g = 0.5입니다.
- **N** — random 조건을 돌리는 seed의 개수입니다.
- **boot default / boot-default sweep** — recognizer가 답하기 전의 기본 설정 / 그 값을 바꿔 가며 민감도를 보는 사전 등록 점검입니다.
- **conformance statement** — 실제 simulator가 RQ0 실행 전에 보여야 할 행동 목록입니다. 2026-10-16부터 (a)–(g)의 일곱입니다(12.4).
- **Layer 1 / Layer 2** — recognizer가 맞혔는가 / 그 답으로 고른 설정이 결과를 좋게 했는가를 재는 층입니다.
- **telemetry** — daemon이 recognizer에게 보여 주는 입력입니다. 이름 → 개수의 목록과, 2026-10-11부터 focus 주인입니다.
- **query point** — process 집합(지금은 focus 포함)이 의미 있게 바뀌어 recognizer에게 다시 묻는 순간입니다.
- **multiset** — 같은 원소가 여러 번 들어가는 집합입니다. telemetry에서는 이름 → 개수입니다.
- **config schedule** — daemon이 "몇 초에 어떤 설정으로"를 적어 simulator에 넘기는 파일입니다.
- **run file** — workload에서 정답을 뺀, simulator에게 주는 파일입니다.
- **visible projection** — daemon이 볼 수 있는 workload의 부분입니다.
- **frozen** — 형식이 고정되어 바꾸려면 세 사람의 결정이 필요한 상태입니다.
- **prior table** — driver table의 첫 판(v0)입니다.
- **pair review** — prior table의 같은 mode 두 row가 무엇이 다르고 어느 term을 움직이는지 검토한 문서입니다.
- **scoring spec / term** — 파일마다 무엇을 채점하는지 적은 파일 / 그 채점 항목 하나입니다.
- **P99** — 99번째 percentile입니다. 여기서는 대기 시간 분포의 상위 1 % 경계입니다.
- **miss rate** — 주기 작업이 마감을 놓친 비율입니다.
- **balanced accuracy** — 정답 class마다의 재현율의 평균인 정확도입니다.
- **cap (`batch_bandwidth_cap`)** — batch class가 쓸 수 있는 CPU 비율의 상한입니다.
- **executor** — simulator 안에서 scheduling 규칙을 집행하는 부분입니다.
- **tick / backlog 규칙 / skip 규칙** — TIMER 주기 격자의 한 시점 / 놓친 tick을 모두 따라잡는 규칙 / 놓친 tick을 건너뛰고 마감 실패로 세는 규칙입니다.
- **`declared_class`** — 프로그램이 스스로 선언한 scheduling policy를 담는 task 필드입니다(`normal`, `idle`).
- **focus** — 지금 키보드와 마우스 입력을 받는 창입니다. timeline의 `focus` track이 그 주인을 적습니다.
- **bless / pin / re-pin** — build 결과를 공식 판으로 정하고 manifest를 commit함 / 다른 파일이 manifest의 hash에 묶임 / 그 hash를 새 판으로 바꿈입니다.
- **build gate** — commit된 manifest가 다시 build한 결과와 같은지 검사하는 `make check`와 CI입니다.

## 14.5 OS와 scheduling 용어

- **core와 lane** — CPU의 실행 단위 하나 / simulator가 흉내 내는 CPU 하나입니다.
- **scheduler** — 여러 process가 CPU를 원할 때 누가 먼저 쓰는지 정하는 OS의 부분입니다.
- **oversubscription** — CPU가 감당할 수 있는 것보다 많은 일이 쌓여 있는 상태입니다.
- **EDF** — 마감이 가장 가까운 일을 먼저 돌리는 scheduling 방식입니다.
- **MLFQ** — CPU를 오래 쓰는 task를 점점 낮은 우선순위 queue로 내리는 scheduling 방식입니다.
- **LOTTERY** — 추첨권으로 다음 task를 고르는 scheduling 방식입니다.
- **time slice** — scheduler가 task 하나에 한 번에 주는 CPU 시간의 단위입니다.
- **preemption** — 시간이 다 되었거나 더 급한 task가 와서 실행 중인 task를 강제로 내리는 것입니다.
- **voluntary block** — task가 스스로 CPU를 내려놓고 I/O나 신호를 기다리는 것입니다.
- **context switch** — CPU가 한 task에서 다른 task로 넘어가는 일입니다.
- **turnaround** — job이 도착해서 끝날 때까지의 시간입니다.
- **cgroup** — Linux가 process들을 묶어 자원을 관리하는 단위입니다.
- **`comm`** — kernel이 process마다 붙이는 최대 15글자의 짧은 이름입니다.
- **scheduling class (policy)** — Linux가 process마다 붙이는 scheduling 종류입니다. `SCHED_OTHER`(normal), `SCHED_IDLE` 등이 있습니다.
- **nice** — normal class 안의 가중치입니다. 클수록 CPU를 덜 받습니다.
- **`perf sched record`** — kernel의 scheduling 사건(깨어남, CPU 받음, 내려놓음)을 기록하는 도구입니다.
- **DKMS** — kernel이 업데이트될 때 외부 kernel module을 새 kernel에 맞게 다시 compile하는 장치입니다.
- **kernel module** — 실행 중인 kernel에 끼워 넣는 코드 조각입니다. 장치 드라이버가 대표입니다.
- **huge page** — kernel이 메모리를 큰 단위로 관리하는 방식입니다. 정책에 따라 CPU 사용량이 달라질 수 있습니다.
- **renderer** — Chrome이 웹 페이지를 그리려고 띄우는 별도 process입니다.
- **wineserver** — Windows 게임을 Linux에서 돌리는 Wine의 중앙 조정 process입니다.
- **`tracker-miner-fs-3`** — GNOME의 파일 색인기 Tracker의 process 이름입니다. `comm`으로는 `tracker-miner-f`입니다.
- **spawn table** — compiler가 미리 뽑아 둔, orchestrator가 실행 중에 fork할 자식 process들의 목록입니다.
- **`fork_cap` / `parallelism_cap`** — orchestrator가 동시에 살려 둘 수 있는 자식 task 수의 상한 / make의 `-j` 값(동시에 도는 job 수)입니다.
- **Dhall 효과** — CPU가 여럿일 때 EDF가 전체 사용률이 낮아도 마감을 놓칠 수 있다는 알려진 현상입니다.
- **SteamCMD** — Valve가 배포하는 Steam의 명령줄 client입니다.
- **sysstat / postinst** — 시스템 통계를 주기적으로 모으는 package / package를 설치한 뒤 도는 script입니다.
- **Mutter / PipeWire / WirePlumber** — GNOME Shell의 compositor / Linux의 오디오 서버 / PipeWire의 session manager입니다.
