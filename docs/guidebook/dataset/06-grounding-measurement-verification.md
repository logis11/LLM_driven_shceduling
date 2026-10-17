# 6권 · 근거, 측정, 검증: 숫자 하나가 믿을 수 있게 되는 길

> Status: draft · Created 2026-10-14 · Updated 2026-10-17

**데이터셋의 숫자와 구조는 어떤 기준으로 근거를 얻고, 우리가 직접 잰 것은 어떻게 재고 확인했으며, 틀린 것은 어떻게 찾아내 고쳤나.**

---

이 데이터셋은 세 겹으로 되어 있습니다. 맨 아래에는 `dataset/archetypes.yaml`, 곧 **archetype library**가 있습니다. archetype은 "어떤 종류의 프로그램이 CPU를 어떻게 쓰는가"를 규칙과 숫자로 적어 둔 항목입니다(예: `office-writer`는 LibreOffice Writer에 사람이 타이핑할 때의 행동). 그 위에 **timeline**이 있습니다. timeline은 "몇 초부터 몇 초까지 어떤 이름의 프로그램이 어떤 archetype으로 살아 있고, 사용자는 지금 무슨 상황(mode)에 있다"를 적은 각본입니다. 맨 위에서 **compile**(이 저장소의 `wlc` 컴파일러가 timeline과 library를 읽어 무작위성을 모두 풀어 낸 실행 가능한 workload 파일을 만드는 단계)이 일어나고, 그 결과물이 simulator와 harness가 먹는 workload 파일입니다. 다른 권들이 각 층이 무엇이고 어떤 값을 갖는지를 설명한다면, 이 권은 그 값들 **밑에 깔린 바닥**을 설명합니다.

바닥이란 이런 질문들입니다. `package-upgrade`라는 archetype이 CPU를 26.385초 쓴다고 적혀 있는데, 그 26.385는 어디서 왔습니까. 게임 archetype의 한 frame이 16,667 µs라는 숫자는 누가 정했습니까. 어떤 숫자는 논문에서, 어떤 숫자는 제품 문서에서, 어떤 숫자는 우리가 GitHub의 CI runner 위에서 직접 잰 측정에서, 어떤 숫자는 "출처 없음, 우리가 정한 설계값"이라는 꼬리표와 함께 왔습니다. 이 권은 그 네 가지 길이 각각 어떤 규칙으로 운영되는지, 누가 그 규칙을 정했고 왜 그렇게 정했는지를 다룹니다.

이 권의 이야기에는 날짜가 있습니다. 2026-09-13, 데이터셋의 출처를 원문(primary text)과 하나하나 대조한 검증에서 심각한 오류들이 나왔습니다. 대표적으로, 컴파일러 프로세스 수의 근거로 쓰던 "2,430개 프로세스"가 Linux kernel build의 숫자가 아니라 DynamoRio라는 다른 프로젝트의 build 숫자였습니다. 이 발견들(`docs/memos/2026-09-13-critical-findings.md`, 이하 critical findings memo)이 Phase 9, 곧 데이터셋 재건축의 방아쇠가 되었습니다. Phase 9는 검증 기준을 새로 세우고(2026-09-13), 측정 도구를 고치고, 영역별 연구 조각(research slice) 아홉 개로 모든 값을 다시 찾거나 다시 재었으며, 그 뒤에도 여러 번의 검토와 감사로 틀린 곳을 찾아 고쳤습니다. 이 권은 그 과정을 "숫자 하나가 믿을 수 있게 되는 길"로 따라갑니다.

마지막으로 이 권은 아직 끝나지 않은 일을 숨기지 않습니다. 문서 전체를 데이터에 맞추는 정리 작업(9.15)과 최종 상태에서 검증을 다시 돌리는 exit audit(9.16)은 이 권을 쓰는 2026-10-14 현재 아직 끝나지 않았습니다. 그래서 이 권에는 "열린 자리"가 여럿 나옵니다. 각 자리마다 무엇이 열려 있고, 무엇이 먼저 있어야 하고, 누가 결정하는지를 적었습니다.

---

## 목차

1. [1장 · 왜 근거인가: 데스크톱에 대한 주장과 숫자의 책임](#1장--왜-근거인가-데스크톱에-대한-주장과-숫자의-책임)
2. [2장 · 인용 장치: `references.md`, `sources.yaml`, `source` 태그](#2장--인용-장치-referencesmd-sourcesyaml-source-태그)
3. [3장 · 검증 기준: Phase 9의 다섯 결정](#3장--검증-기준-phase-9의-다섯-결정)
4. [4장 · 2026-09-13 검증과 critical findings](#4장--2026-09-13-검증과-critical-findings)
5. [5장 · 검증을 저장하고 도구를 고치다: 9.1과 9.3](#5장--검증을-저장하고-도구를-고치다-91과-93)
6. [6장 · 우리가 직접 잰다: CI runner 위의 측정 캠페인](#6장--우리가-직접-잰다-ci-runner-위의-측정-캠페인)
7. [7장 · 몇 번 재야 충분한가: stability rule과 멈춤 규칙](#7장--몇-번-재야-충분한가-stability-rule과-멈춤-규칙)
8. [8장 · 측정이 측정을 망치지 않았나: 검사와 대조군](#8장--측정이-측정을-망치지-않았나-검사와-대조군)
9. [9장 · 원자료와 기록: release, 기록 문서, 재현](#9장--원자료와-기록-release-기록-문서-재현)
10. [10장 · 측정값 하나를 끝까지: `package-upgrade`의 26.385초](#10장--측정값-하나를-끝까지-package-upgrade의-26385초)
11. [11장 · runner가 볼 수 없는 것](#11장--runner가-볼-수-없는-것)
12. [12장 · 연구 조각을 연구로 읽기: 9.4부터 9.12까지](#12장--연구-조각을-연구로-읽기-94부터-912까지)
13. [13장 · 그 뒤의 검토와 감사](#13장--그-뒤의-검토와-감사)
14. [14장 · 아직 남은 것: 9.15, 9.16, 그리고 기록이 밝힌 한계](#14장--아직-남은-것-915-916-그리고-기록이-밝힌-한계)
15. [15장 · 용어 정리](#15장--용어-정리)

---

# 1장 · 왜 근거인가: 데스크톱에 대한 주장과 숫자의 책임

이 장은 "왜 이 연구는 숫자 하나하나의 출처에 이렇게까지 집착하는가"라는 질문에 답합니다. 이 질문이 있는 이유는 간단합니다. 이 연구의 결론은 모두 데이터셋 위에서 나오기 때문에, 데이터셋의 숫자가 흔들리면 결론이 같이 흔들립니다. 먼저 이 데이터셋이 받치는 주장이 무엇인지 보고, 근거 없는 숫자가 실제로 어떤 사고를 냈는지 보고, 마지막으로 숫자가 근거를 얻는 네 가지 길을 한눈에 정리합니다.

## 1.1 이 데이터셋이 받치는 두 주장

이 연구는 데스크톱 컴퓨터에서 지금 실행 중인 프로세스들의 이름을 LLM이 읽고 "사용자가 지금 무엇을 하는 중인가"를 알아낸 뒤, 그에 맞게 CPU scheduler 설정을 바꾸면 더 낫다는 가설을 다룹니다. 여기서 **scheduler**(여러 프로그램이 CPU 하나를 나눠 쓸 때 다음에 누가 CPU를 받을지 정하는 운영체제 부품)는 웹 개발자에게 익숙한 비유로 말하면 event loop가 다음에 어떤 callback을 돌릴지 고르는 규칙과 비슷한 자리에 있습니다.

2026-09-20에 쓴 데이터셋 타당성 검토 memo(`docs/memos/2026-09-20-dataset-validity-review.md`)는 이 데이터셋이 받쳐야 하는 주장을 둘로 나눕니다.

- **인식 주장(recognition claim).** 이름을 읽는 추론이 고정된 이름 표로는 못 읽는 상황을 읽어 낸다는 주장입니다.
- **scheduling 이득 주장(scheduling-benefit claim).** 그 인식을 바탕으로 설정을 바꾸면 scheduling 결과(입력 응답의 꼬리 지연, deadline을 놓친 비율, 일괄 작업이 끝나는 시간)가 실제로 달라진다는 주장입니다.

memo의 판정은 한 줄입니다. "Verdict: sound for the recognition claim, bounded for the scheduling-benefit claim." 인식 주장에는 탄탄하고, 이득 주장에는 범위가 정해져 있다는 뜻입니다. memo가 든 이유는 이렇습니다. 인식기(recognizer)의 입력은 프로세스 이름과 개수 같은 정체(identity)일 뿐 시간 분포가 아니므로, 인식 주장을 받치는 것은 측정의 정밀도가 아니라 compile 경로의 결정성입니다. 같은 timeline, 같은 library, 같은 seed는 바이트까지 같은 workload를 만들고, 짝을 이루는 두 파일은 정확히 한 segment(파일 안의 시간 구간 하나로, 그 구간의 정답 mode 라벨이 붙습니다)만 다르게 만들어집니다. 반면 이득 주장이 다루는 꼬리 지연, 놓친 비율, makespan(일괄 작업이 모두 끝나기까지의 시간)은 "direct functions of the measured burst and gap distributions"(burst는 프로그램이 한 번 깨어나 CPU를 연속으로 쓰는 덩어리, gap은 깨어남 사이의 간격)이기 때문에 측정 캠페인이 하중을 받습니다.

이 구분이 이 권 전체의 뼈대입니다. 숫자의 출처를 따지는 일은 결국 이득 주장이 어디까지 유효한지를 정하는 일이기 때문입니다. memo는 이렇게도 적었습니다. 측정 장치가 보장하는 것은 "precision on one configuration", 곧 하나의 구성 위에서의 정밀도이며, 대표성(representativeness)이 아닙니다. 재현성(reproducibility)과 대표성은 다른 성질이고 다른 문장으로 주장해야 한다고 memo는 권합니다. 이 말은 6장과 11장에서 다시 나옵니다.

> **왜 이렇게 정했나.** 2026-09-20 memo는 "Assessment only; nothing in the repository was changed"라고 스스로를 규정합니다. 즉 결정이 아니라 판정입니다. 다만 그 판정 가운데 "stability ledger를 공개하라", "demand window를 범위 결정으로 밝혀라", "venue가 이득 주장을 묶는다"는 세 권고는 뒤의 기록들(campaign record와 9.5 D76의 scope 문장, 9.14 decision 4, `measurement-overview.md` §11)에서 형태를 얻습니다. 13장에서 하나씩 봅니다.

## 1.2 근거 없는 숫자는 연구를 어떻게 약하게 하는가

추상적으로 말하기보다 실제로 있었던 일 두 가지를 보겠습니다.

**첫째, 2,430.** Phase 9 이전의 `build-orchestrator` archetype(빌드 도구 `make`가 컴파일러 자식 프로세스들을 띄우는 모습을 흉내 내는 항목)은 자식 프로세스 기본값으로 2,430을 들고 있었고, 그 근거는 `ocallahan-atc17`, 곧 O'Callahan 등이 USENIX ATC '17에 낸 record-and-replay 논문의 §4.3이었습니다. 저장소의 여러 문서는 이 숫자를 "Linux kernel build의 프로세스 수"라고 적었습니다. 2026-09-13에 원문을 읽어 보니 논문은 이렇게 말합니다.

> "make builds DynamoRio [8] (version 6.1.0) with make -j8 (-j8 omitted when restricting to a single core). This tests potentially-parallel execution of many short-lived processes." (§4.1)

> "Also, make forks and execs 2430 processes, mostly short-lived. (The next most prolific workload is sambatest with 89.)" (§4.3)

인용문 자체는 정확했지만, 그 숫자가 무엇의 숫자인지가 틀렸습니다. kernel build가 아니라 DynamoRio build였습니다. 그리고 이 프로젝트가 같은 일을 직접 잰 kernel build(`meas-ci:cli:3`, linux-6.6 defconfig, `make -j8`, 5회 반복)는 compiler 계열 프로세스를 중앙값 11,883개 만들었습니다(critical findings memo A1). 같은 "빌드"라도 다섯 배 가까이 차이 나는 숫자에 엉뚱한 이름표를 붙이고 있었던 셈입니다.

**둘째, 16.7 ms.** 게임 archetype `game-task-chain`의 `frame_period`(게임 한 frame의 주기)는 16,667 µs였고, 출처 태그는 LAVD 발표(Changwoo Min, Open Source Summit North America 2024)의 슬라이드였습니다. 2026-09-13에 30장의 슬라이드를 텍스트와 그림까지 다 확인해 보니 16.7, 16.67, 60 fps, "frame budget"이라는 말이 어디에도 없었습니다. 유일한 시간 예산은 slide 27의 "targeted latency (e.g., 15 msec)"였는데, 이것은 scheduler의 스케줄링 창이지 frame 주기가 아닙니다(critical findings memo A2). 이 숫자는 모든 게임 파일의 박자와 부하 크기를 정하는 값이었습니다.

두 사례에서 배우는 것은, 출처 태그가 붙어 있다고 근거가 있는 것은 아니라는 점입니다. 태그는 "이 숫자를 저 문서가 말한다"는 주장일 뿐이고, 그 주장 자체도 검증해야 합니다. 이것이 3장에서 볼 Phase 9 결정 1, 검증 기준의 출발점입니다.

이 저장소의 `CLAUDE.md`도 같은 원칙을 규칙으로 적어 두었습니다. "Never write a citation that isn't verified against a primary source — unverified entries are marked, not invented." 원문과 대조하지 않은 인용은 쓰지 않으며, 확인되지 않은 항목은 지어내지 않고 표시만 한다는 뜻입니다.

## 1.3 숫자가 근거를 얻는 네 가지 길

데이터셋의 숫자 하나는 다음 네 길 중 하나로 근거를 얻습니다.

```
                       숫자 하나 (예: 26.385 s, 16667 µs, count: 4)
                                       │
       ┌───────────────┬───────────────┼────────────────┬─────────────────────────┐
       ▼               ▼               ▼                ▼
  scholarly       deployed-system    measurement        label (출처 없음)
  학술 문헌         배포된 소프트웨어의    우리 자신의 측정       design / convention /
  (논문, 학회)       문서·소스·데이터      meas-ci 캠페인       arithmetic
       │               │               │                │
       ▼               ▼               ▼                ▼
  docs/references.md에 항목 + (값을 끌어오면) dataset/sources.yaml에 등록
  값 옆에는 source: "<id>" 또는 "<id>:<locator>"          값 옆에는 label 하나
```

- **scholarly**(학술 문헌): 동료 심사 논문이나 보관된 preprint입니다. 인용 규칙상 경험적, 행동적, 통계적 주장을 받칠 수 있습니다(단, 그 항목의 역할 범위 안에서).
- **deployed-system**(배포된 시스템): 제품 문서, 소스 코드, 공개 데이터처럼 실제로 배포된 소프트웨어의 자료입니다. 원래 규칙은 "존재 주장만" 받칠 수 있다는 것이었고, 9.12 D112가 그 시스템이 문서로 밝힌 자기 설계와 자기 보고 수치까지 넓혔습니다(2.3절). 발표 슬라이드, 학회 초록, 뉴스 기사는 9.12 D113 이후 따로 한 type(talk, conference abstract or news report)이고, 역시 각주 등급이며 그 주장과 숫자는 발표자나 기자의 보고로만 적습니다. 게임 chain의 근거인 LAVD 발표(`lavd-ossna24`)가 이 type입니다. 그림에서는 deployed-system 칸에 함께 둡니다.
- **measurement**(측정): 이 프로젝트가 GitHub Actions의 runner 위에서 직접 잰 값입니다. 출처 id는 `meas-ci`이고, 어느 캠페인인지를 locator로 붙입니다(`meas-ci:background:2026-10-01`).
- **label**: 어떤 출처도 말하지 않는 값은 출처 태그 없이 무엇인지를 밝히는 꼬리표를 답니다. 지금 lint가 받는 꼬리표는 `design`(우리가 고른 설계값), `convention`(관례), `arithmetic`(다른 값에서 계산한 값) 셋입니다.

이 네 길의 비율이 데이터셋의 성격을 말해 줍니다. 2026-10-10 감사(13장)는 library의 "6,953 leaf numerics 96.6 % measured; 312 tagged objects 97.4 % `meas-ci`"라고 셌습니다. 이 권을 쓰며 tree를 다시 세어 보니 `archetypes.yaml` 안에서 `source`를 단 객체는 314개, 그중 `meas-ci`가 306개(97.5 %)이고, 나머지는 `swell-icmi14` 4개, `lavd-ossna24` 3개, `steamos-refresh` 1개였습니다(python으로 `source` 키를 가진 dict를 모두 센 결과입니다). 감사 시점(커밋 `fe19be86`)과 두 개 차이가 나는 것은 그 뒤의 변경 때문으로 보이며, 어느 커밋에서 늘었는지는 확인하지 않았습니다. 요점은, 이 library의 거의 모든 숫자가 문헌이 아니라 우리 자신의 측정에서 왔다는 것입니다. Phase 9 이전에는 반대였습니다. 그 이유가 3장과 12장의 이야기입니다.

## 1.4 이 권의 길잡이

- 2장은 인용 장치 자체를 봅니다: 두 장부(`docs/references.md`와 `dataset/sources.yaml`), 태그 문법, 꼬리표, 그리고 그것을 지키는 lint.
- 3장은 Phase 9의 다섯 결정, 곧 무엇이 "검증되었다"는 말인지를 정한 규칙을 봅니다.
- 4장과 5장은 그 규칙을 낳은 2026-09-13 검증과, 검증 기록을 저장하고 측정 도구를 고친 9.1과 9.3을 봅니다.
- 6장부터 10장은 우리 자신의 측정, `meas-ci` 캠페인을 처음부터 끝까지 봅니다. 10장에서는 측정값 하나를 job에서 `archetypes.yaml`의 태그까지 손으로 따라갑니다.
- 11장은 runner가 볼 수 없는 것, 12장은 아홉 연구 조각이 각자 어떻게 찾고 무엇을 들고 인지오에게 왔는지를 봅니다.
- 13장은 그 뒤의 검토와 감사, 14장은 아직 남은 일과 기록이 밝힌 한계를 봅니다.

---

# 2장 · 인용 장치: `references.md`, `sources.yaml`, `source` 태그

이 장은 "숫자 옆에 붙은 `source: "meas-ci:background:2026-10-01"` 같은 글자는 정확히 무엇이고, 어디로 연결되며, 누가 그것을 지키는가"라는 질문에 답합니다. 이 질문이 있는 이유는, 1장에서 본 것처럼 태그가 붙어 있다는 사실과 근거가 있다는 사실은 다르기 때문입니다. 태그가 무엇을 약속하는지 정확히 알아야 그 약속이 지켜졌는지 검사할 수 있습니다.

## 2.1 두 장부: 사람이 읽는 장부와 기계가 읽는 장부

인용 정보는 두 파일에 나뉘어 있습니다.

| 파일 | 누가 읽나 | 무엇을 갖나 |
|---|---|---|
| `docs/references.md` | 사람(그리고 논문의 bibliography) | 인용 문자열(`cite`), 역할(`role`), 상태(`status`), URL, 접근 날짜, 고정한 버전. 프로젝트 전체의 출처 id 하나하나에 한 항목. |
| `dataset/sources.yaml` | 기계(데이터셋 linter) | 데이터셋이 값이나 구조를 끌어오는 출처만. 항목마다 `type`, 선택적 `locator_pattern`, `notes`. |

`references.md`의 첫 문단은 이 관계를 이렇게 적습니다. 이 파일이 "every citation string and every citation-constituent field (`url`, `accessed`, `pinned_version`)"를 소유하고, yaml registry는 "machine/derivation fields only"를 가지며 "must be a subset of this index"라고. 즉 `sources.yaml`의 모든 id는 `references.md`에 항목이 있어야 하고(이것을 **subset lint**라 부릅니다), 반대로 `references.md`에만 있고 `sources.yaml`에 없는 항목은 "paper-only references", 곧 논문 본문에서만 인용하고 데이터셋 값에는 쓰지 않는 출처입니다.

웹 개발의 비유를 들자면, `references.md`는 사람이 읽는 의존성 설명서이고 `sources.yaml`은 빌드가 실제로 해석(resolve)하는 의존성 목록입니다. 빌드는 목록에 없는 패키지를 import하면 실패하고, 목록의 패키지가 설명서에 없어도 실패합니다.

tree를 세어 보면 다음과 같습니다(2026-10-17, `grep -c '^### '`와 python으로 센 값).

- `docs/references.md`: `### ` 제목 164개, 모두 서로 다른 id. 섹션별로 scholarly 26개, deployed-system 95개, talk·학회 초록·뉴스 6개, measurement 3개(`meas-ci`, `meas-local`, `meas-pending`), "Related work only (never in the yaml registry)" 34개입니다.
- `dataset/sources.yaml`: 19개 id. `type`별로 scholarly 5개, deployed-system 11개, talk·학회 초록·뉴스 1개(`lavd-ossna24`), measurement 2개.

> **왜 이렇게 정했나.** 두 장부의 분업은 2026-08-26의 workload 생성 grill 결정 D5("Citation ownership flipped", `_dev/archive/2026-08-26-workload-generation-grill.md`)이며 Phase 1 spec decision 1로 이어졌습니다. 기록된 이유는 "`cite` was unlintable presentation — dropped from the yaml"입니다. 인용 문자열은 사람용 표현이라 기계가 검사할 수 없으니 yaml에서 빼고, 기계가 검사할 수 있는 필드만 yaml에 남겼다는 뜻입니다. 같은 날 D4는 "notes split"을 정했습니다. registry의 `notes`는 출처가 무엇을 성립시키는지와 그 범위의 한계만 적고, 우리가 그 위에 얹은 모델링은 archetype 쪽 `modeling_notes`에 적는다는 규칙입니다. 그 결과 `sources.yaml` 머리말에는 "A source tag justifies values and described structure, never field names"라는 문장이 있습니다. 출처는 값과 구조를 정당화할 뿐, 우리가 지은 필드 이름까지 정당화하지는 않습니다.

`dhakal-chi18` 항목은 한때 `references.md`에 두 번 있었고 역할 문장이 서로 달랐습니다("stimulus of the 9.5 campaign's stimulus-sensitivity check only"와 "Role C, typing study … Paper-only after Phase 9"). 2026-10-10 감사가 이 중복을 지적했고, 9.15의 `references.md` 정리(2026-10-16)가 둘을 한 항목으로 합쳤습니다. 지금 그 항목은 데이터(136M Keystrokes 데이터셋)를 cite에 함께 싣고, 역할 줄은 "the alternative stream of the 9.5 campaign's stimulus-sensitivity check only (follow-ups spec decision 11) … It grounds no archetype value"라고 적습니다(8.3절).

## 2.2 id를 만드는 규칙

`references.md`의 "Id-minting rule"은 id 하나가 무엇의 이름인지를 정합니다. 핵심 문장은 "Entry unit: one citable artifact — the thing that gets exactly one citation, one URL, one accessed date"입니다. 인용 한 번, URL 하나, 접근 날짜 하나가 붙는 단위 하나가 항목 하나입니다. 그래서 논문과 슬라이드와 저장소를 가진 프로젝트는 항목을 여러 개 갖습니다.

`type`에 따라 id 모양이 정해집니다.

- **scholarly** → `<label>-<venue><yy>`. label은 제1저자의 성(surname), 또는 모두가 시스템 이름으로 아는 경우 그 이름입니다(`cpsmark-tbench23`, `ghost-sosp21`). arXiv에만 있는 글은 venue 자리에 `arxiv`를 씁니다(`focal-arxiv26`). arXiv 번호 자체를 id로 쓰는 것은 금지입니다. 번호는 인용 문자열 안에 둡니다.
- **deployed-system** → 프로젝트 이름, 연도 없음. 최신성은 `pinned_version`이 담습니다(`interbench`, `rt-app`, `steam-downloads`).
- **talk, conference abstract or news report**(발표, 학회 초록, 뉴스 기사) → `<label>-<venue><yy>`. label은 발표자나 글쓴이의 성, 또는 시스템 이름입니다(`lavd-ossna24`, `corbet-lwn24`). 그 주장은 발표자나 기자의 것으로 적고, 그것이 담은 숫자는 날짜와 함께 그 보고로만 적습니다.
- **measurement** → `meas-ci`, 그리고 어느 캠페인인지를 locator로 붙입니다: `meas-ci:<workflow>:<campaign>`. campaign은 그 캠페인 첫 batch를 띄운 날짜(`YYYY-MM-DD`)이고, 같은 workflow로 같은 날 두 번째 캠페인을 띄우면 글자를 붙입니다(`YYYY-MM-DDb`). 한 캠페인은 여러 run에 걸칠 수 있고, 각 반복의 run id는 pooled record에 남으며, 원자료는 release 하나입니다(2026-09-18부터 2026-09-20까지의 9.5 캠페인들은 release를 나눠 쓰고, 그 가운데 하나는 release 둘에 걸칩니다; 데이터가 인용하는 캠페인마다 그 release는 `dataset/meas-releases.yaml`이 적습니다, 9.1절). run 번호 하나로 된 태그(`meas-ci:<workflow>:<run>`)는 이 형식 이전의, run 하나짜리 캠페인을 가리킵니다. 이름이 붙은 개인 기계에서의 측정은 `meas-local`이고, locator는 `meas-local:<machine>-<subject>:<date>`입니다. 그 원자료는 기계의 hostname을 지운 release 하나이고, 숫자마다 기계의 사양과 반복 사이의 퍼짐을 함께 적습니다.

규칙 끝에는 "Contributor recipe"가 있습니다. (1) 이 규칙을 읽고 id를 만든다, (2) `references.md`에 항목을 넣는다, (3) 데이터셋이 그 출처에서 값이나 구조를 끌어올 때만 `dataset/sources.yaml`에 넣는다. 이 저장소의 `CLAUDE.md` "Citations" 항목도 같은 순서를 적어 두었습니다.

> **왜 이렇게 정했나.** id 규칙은 2026-08-26 grill D1(Phase 1 decision 2)입니다. 기록은 단위와 형식을 정하고, arXiv 번호에 대해서는 "(they live in the citation fields)"라고 그 번호가 있을 자리만 적습니다. 금지의 이유는 따로 적혀 있지 않습니다. 기록된 이유는 없습니다. `meas-ci`의 locator가 run 번호에서 캠페인 날짜로 바뀐 것은 9.5 D27(2026-09-18)이며, 이유는 이렇게 기록되어 있습니다. 9.5 D26과 9.6 D11 이후 캠페인 하나는 "first batch, repeats added one at a time, retries after the machine gate"로 여러 run에 걸치므로, run 번호 하나로는 캠페인을 가리킬 수 없다는 것입니다.

위의 talk type과 `meas-local` 형식은 2026-10-09에 9.12(관련 연구 서술 조각)가 인지오의 결정으로 더했습니다. 9.12 D110은 노트북 측정을 위한 `meas-local:<machine>-<subject>:<date>` 형식을(그 첫 항목 `meas-local:m1pro-llm:2026-10-08`), 9.12 D113은 발표·학회 초록·뉴스 기사를 위한 type을 만들었고(기록은 이것을 "a fifth type"이라 부릅니다), D113은 `lavd-ossna24`와 `corbet-lwn24`를 이 type으로 옮겼습니다. 두 결정은 9.15의 `references.md` 정리(2026-10-16)에서 규칙 문단에 반영되었고, 그때 scholarly의 예도 `lavd-ossna24`에서 `ghost-sosp21`로 바뀌었습니다. 기계가 읽는 `dataset/sources.yaml`은 2026-10-17에 따라왔습니다(9.15, 인지오의 답에 따라). `lavd-ossna24`의 `type`은 `references.md`의 type 이름 그대로 "talk, conference abstract or news report"이고, 머리말의 규칙은 `type` 값으로 id 규칙의 type들(scholarly, deployed-system, talk, conference abstract or news report, measurement)을 적고, 각 type의 등급은 등급 규칙(2.3절)의 문장을 줄여 옮깁니다. 각주에 함께 적는 URL, accessed date, pinned version과 괄호 속 예는 빠졌습니다. 등급 규칙에는 measurement의 등급이 없어서 머리말도 적지 않습니다. 그 전의 머리말은 type 셋(scholarly, deployed-system, measurement)과 deployed-system의 "existence claims only"를 적었습니다. linter는 `type` 값을 검사하지 않고, `sources.yaml`은 어느 manifest의 입력도 아니어서 이 변경으로 다시 bless한 manifest는 없습니다.

## 2.3 인용 등급 규칙과 상태 표시

id 규칙 바로 아래에 "Citation-tier rule"이 있습니다.

- **scholarly** → 번호 붙은 참고문헌. "May support empirical, behavioral, and statistical claims within its stated role."
- **deployed-system** → URL, 접근 날짜, 고정 버전을 단 각주. "Supports existence claims ("this scenario/setting/category exists in shipped software"); the system's own documented design or behaviour, stated as that source's at its pinned version or accessed date ("the kernel's documentation states …"); and a figure the source publishes, stated as its report with the date read, the window and how it is computed. Never a behavioural or statistical claim stated as the paper's own or as a population's."
- **talk, conference abstract or news report** → URL과 접근 날짜를 단 각주. "Its claims are stated as the speaker's or reporter's, never as the paper's own; a number it carries is stated only as its report, with its date."
- 항목의 `role:` 줄이 그 항목이 받칠 수 있는 주장을 말하며, 역할 밖으로 인용하지 않습니다.

**존재 주장(existence claim)**이란 "배포된 소프트웨어에 이런 시나리오, 설정, 범주가 있다"는 주장입니다. 예를 들어 `steamos-refresh`(Valve의 SteamOS 3.2 업데이트 공지)는 "Steam Deck LCD의 기본 화면 주사율이 60 Hz이다"를 받칠 수 있지만, "게이머들이 60 fps로 게임한다"는 받칠 수 없습니다.

상태 표시(status legend)는 세 가지입니다. `verified`(원문과 대조해 좌표를 확인함, 날짜 포함), `to-pin`(식별은 확실하나 정확한 URL이나 버전을 제출 전에 고정해야 함), `provisional`(식별이 불완전함 — 해결 전에는 인용하지 말 것). tree를 세어 보면(2026-10-17) `status:` 줄은 `verified`로 시작하는 것이 161개(그 가운데 `verified-in-vetting` 4개), "in use" 2개(`meas-ci`, `meas-local`), `sentinel` 1개(`meas-pending`)이고, `to-pin`이나 `provisional`로 시작하는 줄은 없습니다.

deployed-system 등급의 넓힘은 9.12 D112(2026-10-09, 인지오의 결정)입니다. 존재 주장 외에 (i) 그 시스템이 문서로 밝힌 자기 설계나 동작을 그 버전의 것으로 밝혀 적는 것, (ii) 그 출처가 자기 보고로 발표한 수치를 날짜·창·계산법과 함께 그 출처의 보고로 적는 것을 허용합니다. 단 행동이나 통계에 대한 주장을 논문 자신의 것이나 모집단의 것으로 적는 일은 여전히 안 됩니다. 이유로 기록된 것은, 9.12의 여러 결정이 이미 deployed-system 출처로 존재 이상의 문장(sched_ext의 무결성, scx_lavd의 메커니즘, Linux에서 class를 누가 정하는지 등)을 받치고 있었다는 사실입니다. 9.15의 `references.md` 정리(2026-10-16)가 위의 규칙 문단과 해당 항목들의 역할 줄을 이 결정에 맞췄습니다.

## 2.4 `sources.yaml`의 19개 id

`sources.yaml`은 주석 머리말로 항목을 묶습니다. 아래 표는 19개 전부이며(2026-10-17), 마지막 열은 tree를 직접 센 결과입니다. `dataset/archetypes.yaml`, `dataset/grids.yaml`, `dataset/variants.yaml`, `dataset/timelines/coreset/*.yaml`을 YAML로 읽어 `source` 또는 `category_source` 키 아래에 그 id가 몇 번 나오는지 셌습니다.

| 묶음(주석 머리말) | id | type | `locator_pattern` | tree에서 태그로 쓰인 횟수 |
|---|---|---|---|---|
| stimulus recordings | `swell-icmi14` | scholarly | `^(word\|outlook\|ie)-c[0-9]+$` | 4 (archetypes) |
| behavior parameters (Role B) | `lavd-ossna24` | talk, conference abstract or news report(2.2절) | `^s\d+$` | 12 (archetypes, gaming timelines) |
| | `ocallahan-atc17` | scholarly | `^sec-[0-9.]+$` | 0 |
| | `coetzee-arxiv12` | scholarly | `^sec-[0-9.]+$` | 0 |
| scenario taxonomy (Role A) | `cpsmark-tbench23` | scholarly | `^(table-\d+\|sec-[0-9.]+)$` | 0 |
| | `pcmark10`, `sysmark30` | deployed-system | — | 0 |
| | `steam-downloads` | deployed-system | — | 0 |
| | `steamos-refresh` | deployed-system | — | 1 (`frame_period`) |
| segment structure & user behavior (Role C) | `gonzalez-chi04` | scholarly | — | 0 |
| grounds of the timelines' bound values | `pytorch-examples`, `kdenlive`, `glam` | deployed-system | — | 3, 3, 11 |
| our measurements | `meas-ci` | measurement | `^[a-z0-9_-]+:(\d+\|\d{4}-\d{2}-\d{2}[a-z]?)$` | 376 |
| | `meas-pending` | measurement | — | 0 (sentinel) |
| generated layer's name limit | `linux-sched-h` | deployed-system | — | 1 (`grids.yaml`) |
| flap-stress intervals | `feral-gamemode`, `tuned`, `systemd-oomd` | deployed-system | — | 1, 1, 1 |

세어 보면 19개 중 11개(`swell-icmi14`, `lavd-ossna24`, `steamos-refresh`, `pytorch-examples`, `kdenlive`, `glam`, `meas-ci`, `linux-sched-h`, `feral-gamemode`, `tuned`, `systemd-oomd`)가 데이터셋 파일의 태그로 쓰입니다. 나머지 8개 가운데 sentinel `meas-pending`을 뺀 7개는 태그가 아니라 데이터 파일의 주석이나 문장 속에서 이름으로 인용됩니다. `ocallahan-atc17`과 `coetzee-arxiv12`는 `compiler-child`의 `modeling_notes`에, `gonzalez-chi04`는 `c6-dual`의 머리 주석에, `steam-downloads`는 `c2-p2a`의 머리 주석에 있습니다. CpsMark+(`cpsmark-tbench23`)와 SYSmark 30(`sysmark30`)은 core timeline의 머리 주석(`c1-transcode`, `c3-workday`; `c3-creation`)에 이름으로 나오고, CpsMark+와 PCMark 10(`pcmark10`)은 archetype의 scope와 notes 문장 안에서 측정 입력의 근거로 나옵니다(예: `web-browser`의 page-load operation은 "design after PCMark 10 pp. 52–53 and CpsMark+ §4.3.3"라고 적혀 있습니다). 문장 속 언급은 태그가 아니므로 위의 세기에 들어가지 않습니다.

이 상태가 된 경위는 이렇습니다. Phase 9 이전의 library는 interbench, LAVD, 작업 전환 연구 같은 문헌에서 값을 끌어왔습니다. Phase 9의 연구 조각들이 archetype을 하나씩 측정 기반으로 바꾸면서(12장), 그 문헌들은 값을 받치는 자리에서 물러나 존재 주장이나 논문 본문의 맥락으로만 남았습니다. 그 사이 registry는 2026-10-10 감사 시점의 23개에서, 9.18이 timeline 값의 근거로 `pytorch-examples`, `kdenlive`, `glam`을, 9.19가 flap-stress 간격의 근거로 `feral-gamemode`, `tuned`, `systemd-oomd`를, 9.20이 이름 길이 한도의 근거로 `linux-sched-h`를 더해 30개가 되었습니다. 감사는 "`dataset/sources.yaml`: 18 of 23 ids ground nothing"이라고 적었고, 9.10 D34(2026-10-01)는 `procyon`, `dkms-man`, `dkms-debian`, `gamemode-docs`, `dubroy-chi10`, `chang-chi21`, `mozilla-testpilot10`가 registry를 떠난다고 결정했지만 그 제거를 넘겨받은 9.13은 하지 않았습니다. 9.15가 이것을 정리했습니다(2026-10-16, 인지오의 답에 따라). D34의 일곱과, 어떤 데이터 파일도 태그로도 주석으로도 이름으로도 인용하지 않는 넷(`sysmark25`, `rt-app`, `focal-arxiv26`, `mark-chi05`)이 registry를 떠나 19개가 되었습니다. 데이터 파일이 이름으로 인용하는 `cpsmark-tbench23`, `pcmark10`, `sysmark30`은 registry의 규칙(데이터셋이 값이나 구조를 끌어오는 출처만)에 따라 남았습니다. 떠난 열한 개 가운데 본문이 인용하지 않는 다섯(`dkms-man`, `dkms-debian`, `dubroy-chi10`, `chang-chi21`, `mozilla-testpilot10`)은 `references.md`에서도 빠졌고(9.12 D102), `mozilla-testpilot10`의 분석 논문인 `singervine-slate10`도 함께 빠졌습니다. 나머지(`procyon`, `gamemode-docs`, `sysmark25`, `rt-app`, `focal-arxiv26`, `mark-chi05`)는 본문이 인용하므로 `references.md`에 paper-only 항목으로 남았습니다.

`ocallahan-atc17`의 두 문장도 고쳐졌습니다. `sources.yaml`의 notes는 "The workload is a `make -j8` build of DynamoRio 6.1.0 (sec-4.1), not a Linux kernel build. Grounds only the existence and short-lived character of compiler children"이라고 적고, `references.md`의 같은 항목 role 줄도 "of a `make -j8` build of DynamoRio 6.1.0 (§4.1), not a kernel build (the critical findings memo's A1)"라고 적습니다. critical findings memo A1이 2026-09-13에 틀렸다고 밝힌 "kernel-build workload"는 두 줄 모두에서 빠졌습니다. 이 id는 어떤 값도 받치지 않으므로 compile 결과와는 상관이 없습니다.

## 2.5 태그의 문법: `<id>`와 `<id>:<locator>`

값 옆의 태그는 두 모양 중 하나입니다. `<id>` 또는 `<id>:<locator>`. **locator**는 출처 안의 위치입니다. 논문이면 절(`sec-4.3`)이나 표(`table-4`), 슬라이드면 장 번호(`s13`), 데이터셋이면 그 안의 파일(`word-c1`), 측정이면 workflow와 캠페인(`background:2026-10-01`)입니다.

registry 항목에 `locator_pattern`이 있으면 linter는 locator가 그 정규식에 맞는지 검사하고, 없으면 locator를 붙이는 것 자체가 오류입니다. 몇 가지 예를 보겠습니다.

- `source: "swell-icmi14:word-c1"` — SWELL-KW 데이터셋의 Word, 조건 c1 기록. 패턴 `^(word|outlook|ie)-c[0-9]+$`에 맞습니다.
- `source: "lavd-ossna24:s13"` — LAVD 슬라이드 13장. 패턴 `^s\d+$`.
- `source: "steamos-refresh"` — locator 없는 bare id. 이 항목에는 패턴이 없으므로 locator를 붙이면 오류입니다.
- `source: "meas-ci:interactive:2026-09-18"` — workflow `interactive`, 2026-09-18에 첫 batch를 띄운 캠페인.

> **코드로.** 태그 검사는 `dataset/tools/wlc/linter.py`의 `_check_tag`가 합니다. 태그를 정규식 `([a-z0-9-]+)(?::(.+))?`로 id와 locator로 가르고, id가 registry에 없으면 "source id … not in registry", locator가 있는데 패턴이 없으면 "has a locator but … declares no pattern", 패턴에 맞지 않으면 "locator … violates … pattern"을 돌려줍니다. `meas-ci`의 패턴 `^[a-z0-9_-]+:(\d+|\d{4}-\d{2}-\d{2}[a-z]?)$`는 run 번호 형식(옛 `cli:3`)과 날짜 형식(`background:2026-10-02b`)을 둘 다 받습니다.

## 2.6 꼬리표: 출처가 말하지 않는 값

Phase 9 결정 1(3장)은 "A value no source states carries no source tag and is labelled for what it is: convention, arithmetic, placeholder, or design"이라고 정했습니다. 출처가 없는 값은 태그를 달지 않고, 무엇인지를 꼬리표로 밝힌다는 뜻입니다. 네 꼬리표의 뜻은 이렇습니다.

- **design**: 실험을 위해 우리가 고른 값. 예: `c1-gaming`의 `lane_share: 0.9`, 생성 층(generated layer)의 segment 길이 60 s.
- **convention**: 분야의 관례를 따른 값. 예: 출처가 범위만 줄 때 lognormal을 쓰는 것(archetype-plan의 OQ-5: "lognormal remains the convention where a source gives only a span", `game-task-chain`의 `per_schedule_run`).
- **arithmetic**: 다른 값에서 계산한 값. 예: 16,667 µs = 1/60 s.
- **placeholder**: 측정을 기다리며 임시로 넣은 값. 지금의 규칙에는 이 꼬리표가 없습니다. 측정을 기다리는 값은 `meas-pending` 태그를 달고, `make lint`의 freeze가 그것을 거부하므로 데이터셋에 들어가지 않습니다(아래 "왜 이렇게 정했나"와 2.7절).

이 꼬리표가 어디에 붙을 수 있는지는 층마다 다릅니다.

1. **library(`archetypes.yaml`)**: 모든 숫자 파라미터는 반드시 registry 태그를 가져야 합니다. `lint_repo`의 `_check_param`은 태그가 없으면 "numeric param without source tag"를 냅니다. 따라서 library 안에는 꼬리표 자리가 없고, "이 값의 해석은 우리 것"이라는 말은 `modeling_notes`의 문장으로 들어갑니다. 예를 들어 `game-task-chain.frame_period`는 `source: "steamos-refresh"`(60 Hz라는 존재 사실)를 달고, notes에 "16667 us is 1/60 s arithmetic) — design, ours"라고 적혀 있습니다. 60 Hz의 존재는 출처가 말하고, 게임을 화면 주사율에 맞춰 도는 것으로 모델링한 선택은 우리 설계입니다.
2. **timeline**: 각 task의 `source` map이 `bind`의 키와 `count`를 그대로 따라가며, 항목 하나는 태그 하나, 태그 목록, 또는 꼬리표 하나입니다. lint가 받는 꼬리표는 `BOUND_LABELS = ("design", "convention", "arithmetic")` 셋이고, 꼬리표는 혼자 서야 합니다(목록 안에 꼬리표를 섞으면 오류).
3. **`grids.yaml`(생성 층의 정의)**: 숫자마다 출처나 꼬리표를 답니다. 예: flap-stress 간격 `{length: 2s, source: design}`, `{length: 5s, source: feral-gamemode}`, `{length: 10s, source: tuned}`, `{length: 30s, source: systemd-oomd}`; 이름 길이 한도 `comm_limit: {chars: 15, source: linux-sched-h}`.

> **왜 이렇게 정했나.** timeline의 bound value에 출처나 꼬리표를 다는 규칙은 9.10 D32(2026-10-01)입니다. 기록된 이유는 `building-plan.md` §6의 provenance 주장이 library만 덮고 있었고, timeline 값에는 출처 칸이 없었으며(`timeline.py`; critical findings memo B7), 그런데도 `archetype-plan.md:40`은 count를 "binding-time parameters with a source tag"라고 부르고 있었다는 것입니다. 즉 문서가 이미 약속한 것을 실제로 만들자는 결정이었습니다. 9.10은 내용을 정하고 필드와 lint는 9.13에 넘겼는데, 9.13의 spec이 그것을 받지 않아(넘긴 일이 빠진 것) 2026-10-10 감사가 "Timeline bound values carry no source field"(감사의 A2)를 발견할 때까지 만들어지지 않았고, 9.18(2026-10-11)이 필드와 lint를 실제로 넣었습니다. 꼬리표 목록이 셋인 것은 9.10 D32가 "a label (design, convention, arithmetic)"이라고 셋만 적었기 때문이고 `linter.py`의 주석도 그 결정을 가리킵니다. Phase 9 결정 1의 넷째 꼬리표 placeholder에 대해서는 인지오가 2026-10-16에 정했습니다(9.15 작업 목록 W-0750). 측정을 기다리는 값은 `meas-pending`을 달고, freeze가 그것을 거부하며, placeholder 꼬리표는 두지 않습니다. 이를 위해 freeze 검사가 library의 파라미터뿐 아니라 timeline의 bound value에도 걸리게 되었습니다(`lint_bound_sources(…, freeze=True)`, 9.15의 rebuild, 2026-10-16). Phase 9 spec의 "placeholder"는 개발 이력으로 남습니다.

## 2.7 linter가 지키는 것, 지키지 못하는 것

`make -C dataset lint`는 `dataset/tools/lint.py --freeze`를 부르고, 그것은 네 가지 검사를 돌립니다.

| 검사 | 함수 | 무엇을 보나 |
|---|---|---|
| repo lint | `lint_repo` (`wlc/linter.py`) | `sources.yaml`의 모든 id가 `references.md`의 `### \`id\`` 제목으로 있는가(subset lint); 모든 archetype이 필수 필드 9개(`category_source`, `declared_class`, `pattern`, `params`, `lifetime`, `binding_params`, `scalable`, `validation_stats`, `modeling_notes`)를 갖는가; 모든 파라미터가 태그를 갖고 그 태그가 registry와 locator 패턴을 통과하는가; quantile 표가 열 개의 단조 증가 값과 min/max/구간 평균을 일관되게 갖는가 |
| bound-source lint | `lint_bound_sources` | 각 timeline task의 `source` map이 `bind` 키와 `count`를 빠짐없이, 넘치지 않게 덮는가; 각 항목이 태그, 태그 목록, 또는 꼬리표 하나인가 |
| grid lint | `lint_grids` (`gen/cells.py`) | `grids.yaml`의 모든 숫자에 출처나 꼬리표가 있는가; 생성 층이 쓰는 모든 이름이 15자 한도 안인가 |
| release-map lint | `lint_releases` (`wlc/linter.py`) | library, timeline, variant recipe, `grids.yaml`이 담은 `meas-ci:<workflow>:<campaign>` 태그마다 `dataset/meas-releases.yaml`에 그 캠페인의 release가 있는가; 항목마다 release 태그, GitHub release 주소, asset마다 이름과 SHA-256이 있는가(9.15, 2026-10-16) |

`meas-pending`, 곧 측정을 기다리는 임시값 표시는 "schema freeze" 이후에는 거부됩니다. 9.23 D13(2026-10-15)부터 `make lint`가 `lint.py --freeze`를 돌리므로 lint 자체가 이것을 거부하고("meas-pending after freeze"), 9.15(2026-10-16)부터는 library의 파라미터뿐 아니라 timeline의 bound value에 달린 `meas-pending`도 거부합니다. `dataset/tools/tests/test_lint.py`도 `freeze=True`로 돌립니다. `dataset/README.md`의 "No `meas-pending`"이라는 규칙이 이렇게 지켜집니다.

linter가 지키지 못하는 것도 분명히 알아야 합니다. linter는 **형식**을 검사합니다. 태그가 registry에 있는지, locator가 패턴에 맞는지, 칸이 비지 않았는지. 그러나 그 태그가 **올바른 근거인지**는 검사하지 못합니다. `_dev/TODO.md`의 9.16 줄이 이것을 그대로 적습니다. "every timeline's `source` map agrees entry for entry with `_dev/research/jioh/task-9.10-scenarios-timelines/bound-values.md` (the lint checks form, not that each tag is the right ground)". 그래서 "이 태그가 정말 이 값을 말하는가"는 사람이 원문을 읽는 검증, 곧 3장과 4장의 일입니다. 1장의 2,430 사례도 형식으로는 완벽한 태그였습니다.

## 2.8 한 값의 출처를 손으로 따라가기

`c1-ml-train`(사용자가 편집기를 쓰는 옆에서 PyTorch 학습이 도는 상황을 담은 timeline)을 열어 보면 학습 task가 이렇게 적혀 있습니다.

```yaml
  - {id: hog, name: python, archetype: cpu-batch, arrive: 2s,
     bind: {total_work: 1389.885s, program: python3},
     source: {total_work: "meas-ci:background:2026-10-03", program: [pytorch-examples, "meas-ci:background:2026-10-03"]}}
```

손으로 따라가면 다음과 같습니다.

1. `total_work: 1389.885s`는 이 학습 작업이 쓰는 CPU 시간 총량입니다. 출처는 `meas-ci:background:2026-10-03`입니다.
2. `sources.yaml`에서 `meas-ci`를 찾으면 type `measurement`, locator 패턴, 그리고 notes가 있습니다. notes는 "A measured value is this software on this machine: a GitHub-hosted ubuntu-24.04 runner, pinned to one CPU of the AMD EPYC 7763 only (machine gate) … never desktop truth"라고 이 출처가 무엇을 성립시키고 무엇을 성립시키지 않는지 적습니다.
3. `references.md`의 `meas-ci` 항목은 role을 "a measured value is this software on this machine — a GitHub-hosted ubuntu-24.04 runner, pinned to one CPU of the AMD EPYC 7763 only (the machine gate), its runner spec written into the archetype's scope — never desktop truth"로 시작하고, status 줄에서 캠페인을 어떻게 돌리고 언제 멈추는지는 `_dev/research/jioh/measurement-campaign-workflow.md`라고 가리킵니다.
4. locator `background:2026-10-03`은 workflow `meas-background.yml`로 2026-10-03에 띄운 캠페인입니다. `_dev/research/jioh/measurement-campaign-record.md`의 "9.10 — `cpu-batch`'s `python3`, PyTorch's basic MNIST example" 절에 이 캠페인의 반복 횟수, 값, 반폭이 있습니다. CPU 총량은 6회 반복의 평균 1,389.885 s, 95 % 반폭 ±4.04 %입니다(반복별 1,293.8–1,455.8 s).
5. 원자료는 GitHub release `meas-ci-background-2026-10-03`에 있습니다. `dataset/meas-releases.yaml`이 이 캠페인 태그를 그 release의 주소와 asset마다의 SHA-256에 잇습니다(9.1절).
6. `program: python3`에는 태그가 두 개 붙어 있습니다. `pytorch-examples`는 "무엇을 돌렸는가"(PyTorch examples 저장소의 Basic MNIST Example, 커밋 `acc295dc…`)의 존재 근거이고, `meas-ci:background:2026-10-03`은 그 프로그램을 잰 캠페인입니다. `references.md`의 `pytorch-examples` 역할 줄은 "Identifies the measurement's job; existence only, no claim that desktop users train MNIST or how often anyone trains"라고 범위를 못박습니다.

이렇게 하나의 숫자는 timeline → registry → 인용 항목 → 캠페인 기록 → 원자료까지 끊기지 않고 이어져야 합니다. 10장에서는 같은 길을 반대 방향, 곧 측정 job에서 출발해 따라갑니다.

## 2.9 `grounding-sources.md`: 어떤 출처가 어떤 주장을 받칠 수 있나

`docs/workload/grounding-sources.md`(Status: normative, Created 2026-08-25, Updated 2026-10-17)는 출처를 **역할(role)** A–D로 나눕니다. 역할이란 "이 출처는 어떤 종류의 근거를 제공하는가"입니다. 9.15의 전체 정리(spec decision 4)가 이 문서를 지금의 데이터셋에 맞췄고, 표는 그 뒤의 모습입니다.

| 역할 | 문서의 제목 줄 | 문서가 든 출처 |
|---|---|---|
| A — Scenario taxonomy | "these situations are standard, not imagined": 각 출처는 시나리오가 출하된 벤치마크나 시스템에 있다는 것만 보이고, 얼마나 흔한지나 어떤 프로그램이 함께 도는지는 말하지 않음 | PCMark 10, SYSmark 30/25, UL Procyon, CpsMark+, game mode 시스템들(Windows Game Mode, macOS Game Mode, Feral GameMode), Steam의 download 설정, CachyOS의 ananicy 카탈로그 |
| B — Process behavior parameters | "precedents, and LAVD's reported figures for the game chain": library의 프로세스별 값은 우리 측정(Role D)이고, 게임 chain만 `lavd-ossna24`의 보고 값. 나머지 커뮤니티 도구는 task 모형과 지표의 형식에 대한 선례일 뿐 데이터셋 값을 받치지 않음 | rt-app, interbench, schbench, hackbench, LAVD, stress-ng, kernel build |
| C — Segment structure and switching statistics | "observed human timelines": core set의 segment 길이는 design이거나 묶인 작업의 측정 길이이고, 이 역할의 출처에 기대는 것은 `c6-dual`의 688 s focus 교대 하나(`gonzalez-chi04`); 나머지는 naturalistic set의 몫 | González & Mark CHI 2004, Mark 등 CHI 2005, Czerwinski 등 CHI 2004, SWELL-KW, BEHACOM, DesktopBench(FOCAL) |
| D — Our own measurement | "'this software on this machine'": 측정된 archetype 28개의 모든 값. 사용자 쪽 값(키 입력 시각, 탭 수)은 사용자를 재지 않고 공개 기록에서 옴 | `meas-ci` |

이 문서에는 규칙이 셋 있습니다.

- **부정적 결과(the negative result).** "no public trace gives desktop process trees with names over time." 이름이 붙은 데스크톱 process tree를 시간에 따라 담은 공개 trace는 없다는 발견을, 사과가 아니라 결과로 진술하라는 규칙입니다. 처음의 문장("no public trace of desktop process timelines with process names exists")은 9.10 D35가 좁힌 지금의 모양이 되었습니다. BEHACOM은 자연스러운 사용에서 분 단위로 전경 실행 파일 이름을 공개하고, DARPA OpTC는 Windows 10 기업 endpoint의 process 생성 사건을 담기 때문입니다. 이유도 적혀 있습니다. "process names are exactly the field privacy review strips, and process names are exactly what this research is about." 프라이버시 검토가 지우는 바로 그 필드가 이 연구의 주제라는 것입니다.
- **반-역할(anti-roles).** Phoronix Test Suite나 UnixBench(기계의 성능 측정이지 시나리오 정의가 아님), 모바일 앱 사용 데이터셋(모바일의 전경 독점 구조가 데스크톱 멀티태스킹과 다름; 여러 앱의 실행을 기록하는 Carat도 쓰지 않음), SchedCP의 평가 workload(재사용하면 데스크톱 framing을 양보하게 됨)는 근거로 쓰지 말라는 목록입니다.
- **등급 규칙 재진술.** `references.md`의 등급 규칙(2.3절: deployed-system은 존재 주장, 그 시스템이 문서로 밝힌 자기 설계, 자기 보고 수치; talk와 뉴스는 발표자나 기자의 보고)을 범위의 규율로 다시 적고, interbench에 빗대어 "the community *models* interactivity this way", not "desktops *behave* this way"라고 덧붙입니다. "얼마나 자주, 얼마나 많이, 사용자가 어떻게"를 말하는 문장은 scholarly 출처나 우리 자신의 Role D 측정이 있어야 합니다.

이 권을 처음 쓸 때(2026-10-14) 이 문서의 목록에는 Phase 9 이후 낡은 줄이 여럿 있었습니다. Role B의 interbench, schbench, hackbench, stress-ng가 값을 받치는 것처럼 적혀 있었고, LAVD 행에 슬라이드에 없는 "the 16ms-frame deadline"(A2)과 2026-09-13 검증이 MISATTRIBUTED로 판정한 "Valve ships it; Meta adopted the scheduler server-side"(K2 C-lavd-18)가 있었으며, SWELL-KW는 "access-gated", "qualitative"(K4 C-swell-1, CONTRADICTED)로, 사본에 닿을 수 없어 9.10 D1이 뺀 `zhang-chb15`는 "Standing verification tasks" 1번에 남아 있었습니다. 9.15의 정리가 이것들을 모두 고쳤습니다. 지금 문서는 Role B의 커뮤니티 도구를 존재와 형식의 선례로만 적고(interbench는 "it supplies no parameter values"), LAVD 행은 Min의 2024-04-17 보고 값과 chain의 형식이 design이라는 것, 그리고 Valve가 SteamOS 3.8에서 사용자가 고르는 scheduler로 싣는다는 것(`steamos-lavd`)과 Meta의 발표자들이 fleet 기본 scheduler 후보로 소개했다는 것(`dai-lpc25`)을 적으며, SWELL-KW는 CC BY-NC-SA 4.0으로 열려 있는 데이터, `zhang-chb15`는 2026-10-01에 빠진 것으로 적습니다.

## 2.10 `source-vetting.md`: 첫 심사의 기록

`docs/workload/source-vetting.md`(Status: record — append-only, Created 2026-08-25, Updated 2026-10-17)는 데이터셋을 처음 만들 때 후보 출처 약 20개를 심사한 기록입니다. rev. 2(2026-08-25)에서 CpsMark+를 "CONDITIONALLY USABLE"에서 "USABLE"로 올렸고, rev. 3(2026-08-26)에서 인용 오류 몇 개(작업 전환 연구의 저자, Gloria Mark 수치의 진짜 출처, kernel build 관련 arXiv 논문 두 편의 정체)를 고쳤습니다. 끝에는 출처별 판정표(Summary Verdict Table)가 있습니다.

이 문서는 **기록(record)**이며 append-only입니다. 즉 그 시점에 무엇을 근거로 무엇을 판정했는지를 남기는 것이 목적이고, 나중에 틀린 것으로 밝혀져도 원문을 고치지 않습니다. 그래서 이 문서를 인용할 때는 "2026-08-25의 심사가 이렇게 판정했다"로 인용해야지, "이것이 사실이다"로 인용하면 안 됩니다.

실제로 2026-09-13 검증은 이 기록의 여러 문장이 원문과 다르다는 것을 밝혔습니다. 대표적인 것만 적습니다.

| 심사 기록이 적은 것 | 2026-09-13 검증의 판정 |
|---|---|
| interbench Compile 부하가 "heavy make -j4"로 compiler-child를 교차 확인 | CONTRADICTED (K1 C-interbench-9): Compile은 한 프로세스 안의 스레드 셋(Burn+Write+Read)이고 프로세스를 하나도 fork하지 않음 |
| LAVD "16.7 ms frame budget / 15 ms targeted latency" | NOT IN SOURCE (K2 C-lavd-9) |
| kernel build가 2,430개의 짧은 프로세스를 fork/exec | MISATTRIBUTED (K1 C-ocallahan-1): DynamoRio 6.1.0 build |
| SWELL-KW "request/registration required" | CONTRADICTED (K4 C-swell-1) |
| ananicy 카탈로그 "audio nice −11" | MISATTRIBUTED (K3 C-ananicy-rules-2): 고정 시점의 `Player-Audio`는 nice −4 |
| Game Mode "updates/notifications deferred" | MISATTRIBUTED, CONTRADICTED (K3 C-gamemode-5): Xbox Support 문서에만 있음 |
| schbench가 percentile 20/50/75/90/95/99/99.5/99.9를 보고 | CONTRADICTED (K1 C-schbench-1): 어떤 버전도 그 집합을 RPS와 함께 찍지 않음 |

이 표는 심사 기록이 가치 없다는 뜻이 아닙니다. 심사 기록은 "어디를 읽어야 하는가"의 지도로 쓸모가 있었고, 바로 그 지도를 원문과 하나하나 대조한 것이 2026-09-13 검증입니다. 차이는 방법에 있습니다. 첫 심사는 저장소가 이미 가진 설명을 들고 원문을 읽었고, 2026-09-13 검증은 저장소의 설명을 감춘 채 원문을 읽었습니다. 그 방법의 차이가 3장의 결정 1이 되었습니다.

9.11 D12와 9.12의 여러 결정이 `source-vetting.md:52, 57, 58, 61, 64, 66, 67, 87, 90`의 선례(precedent) 문장을 고친 항목들로 바로잡으라고 넘겼습니다(TODO 9.15 줄). 이 문서는 append-only 기록이므로 원문은 그대로 두고, 9.15가 끝에 "## Correction (2026-10-17)" 절을 덧붙였습니다. 그 절은 고친 줄마다 줄 번호를 이름 짓고 지금의 사실을 적습니다(예: "**Line 70** (kernel build): O'Callahan et al.'s 2,430 mostly short-lived processes are a `make -j8` build of DynamoRio 6.1.0, not a kernel build"). 위 표의 LAVD, kernel build, SWELL-KW, ananicy, Game Mode, schbench 판정도 그 절에 해당 줄 번호와 함께 들어 있고(17, 70, 81, 47, 46, 57–58행), 인용 문자열과 고정 버전과 역할은 `references.md`의 것, 출처들이 지금 맡는 역할은 `grounding-sources.md`의 것이라고 절의 첫 문장이 밝힙니다.

---

# 3장 · 검증 기준: Phase 9의 다섯 결정

이 장은 "이 데이터셋에서 '검증되었다'는 말은 정확히 무엇을 뜻하는가"라는 질문에 답합니다. 이 질문이 필요한 이유는, 2026-09-13 이전에도 `references.md`의 거의 모든 항목이 `verified`라고 적혀 있었는데 그 가운데 상당수가 원문과 달랐기 때문입니다(4장). "검증"이라는 낱말이 아무 절차도 약속하지 않으면, 상태 표시는 장식이 됩니다. Phase 9는 그 낱말에 절차를 붙였습니다.

## 3.1 Phase 9가 시작된 날

2026-09-13, 인지오는 critical findings memo와 같은 날의 검증 결과를 받고 Phase 9 spec 세션을 열었습니다. 그 결과가 `_dev/docs/spec/jioh/phase-9-workload-dataset-rebuild.md`입니다. spec의 목표 문장은 이렇습니다. "Resolve what the workload dataset and everything built on it rest on, rebuild the dataset, and return the project to the state Phase 8 ended in: the RQ0 gate spec committed and ready for the RQ0 run." 데이터셋과 그 위에 지은 모든 것이 무엇에 기대고 있는지 해결하고, 데이터셋을 다시 짓고, Phase 8이 끝났던 상태 — 첫 실험(RQ0, 연구 질문 0번의 실험)의 판정 규칙을 미리 고정한 문서인 **RQ0 gate spec**이 커밋되어 실험을 돌릴 준비가 된 상태 — 로 돌아가는 것이 목표입니다.

spec의 범위(Scope)는 다음과 같습니다.

- critical findings memo의 findings.
- memo에 없지만 같은 날의 확인에서 나온 여섯 가지 발견(4.5절).
- 데이터셋이 출처에서 가져온 모든 주장, 특히 그전에 원문과 대조한 적이 없는 registry 항목 열두 개(`pcmark10`, `sysmark30`, `sysmark25`, `procyon`, `gamemode-docs`, `steam-downloads`, `dkms-man`, `dkms-debian`, `zhang-chb15`, `gonzalez-chi04`, `mark-chi05`, `focal-arxiv26`).
- 모든 `meas-ci` 값을, 원자료 release와 그 값을 만든 방법에 대고.
- 2026-09-13 검증이 찾은 모든 것.
- 네 무리의 산출물: 데이터셋 자체, 데이터셋을 소비하는 것(우선순위 표, scoring spec, guard spec, RQ0 gate spec, demand window 규칙), 데이터셋 밖의 인용(관련 연구 서술, harness 상수 등), 팀 memo.

그리고 spec은 열 개의 결정을 고정했습니다(9와 10은 2026-10-11에 추가). 이 권의 주제는 1번부터 5번이며, 6번부터 8번은 뒤의 장들이 기대는 틀이라 짧게 함께 봅니다.

> **왜 이렇게 정했나.** spec에는 각 결정의 이유를 적는 칸이 없고, 2026-09-13 spec 세션의 archive도 `_dev/archive/`에 없습니다(그 폴더의 가장 최근 archive는 2026-09-11의 Phase 7 것입니다). 따라서 결정 1부터 5까지 각각에 대해 **기록된 이유는 없습니다**. 이 장에서는 결정 옆에, 같은 날의 critical findings memo가 기록한 발견 가운데 그 결정이 금지하는 일의 실제 예를 나란히 놓습니다. 그것은 "이 예가 결정의 이유였다"는 주장이 아니라 "결정이 막는 실패가 실제로 이런 모습이었다"는 설명입니다.

## 3.2 결정 1 — 검증 기준

spec 원문은 이렇습니다.

> "A claim taken from a source is verified when it is recorded with the verbatim passage, its locator, and the copy read (URL or commit, version, date), and the check covers the whole claim the repository makes — its object, unit, statistic, scope and population. The source is read independently, without the repository's description of the claim, before the reading is compared with the repository's wording. A claim whose passage is not found is unverified. A value no source states carries no source tag and is labelled for what it is: convention, arithmetic, placeholder, or design."

이 문단에는 요소가 일곱 개 있습니다. 하나씩 풀고, 각각이 실제로 무엇을 잡아냈는지 예를 붙입니다.

**(1) 원문 그대로의 구절(verbatim passage).** 요약이나 기억이 아니라 출처의 문장을 그대로 기록합니다. 1장의 DynamoRio 인용이 그 예입니다. 요약했다면 "kernel build"라는 오해가 그대로 살아남았을 것입니다.

**(2) 위치(locator).** 절, 쪽, 슬라이드, 표 번호. 위치가 있어야 다른 사람이 같은 구절을 찾을 수 있습니다. 2026-09-13 검증은 `ocallahan-atc17`의 경우 "§4.3 has the workload description"이라는 저장소의 전제도 틀렸다고 밝혔습니다. 작업 부하 설명은 §4.1 "Workloads"에 있고, §4.3은 "Observations"이며 2,430이라는 수만 담고 있었습니다(R03 C-ocallahan-3).

**(3) 읽은 사본(copy read): URL 또는 커밋, 버전, 날짜.** 같은 논문도 판본이 여러 개이고, 같은 저장소도 커밋마다 내용이 다릅니다. 예를 들어 interbench는 master 커밋 `e612a65c`와 태그 v0.31 사이에 부하 기본값이 다릅니다(`references.md`의 `interbench` 항목: "its load defaults differ from tag v0.31"). 사본을 적지 않으면 "검증했다"가 무엇을 검증한 것인지 알 수 없습니다. 2026-09-13 검증의 read 문서는 맨 앞에 "Copies used" 표를 두고 URL, 판본, 날짜, 로컬 경로, SHA-256을 적습니다.

**(4) 주장 전체를 덮는다: 대상, 단위, 통계량, 범위, 모집단.** 이것이 결정 1의 핵심입니다. 숫자 하나가 맞아도 그 숫자에 붙은 다섯 가지 속성 중 하나가 틀리면 주장은 틀린 것입니다.

| 속성 | 뜻 | 2026-09-13에 잡힌 예 |
|---|---|---|
| 대상(object) | 그 숫자가 무엇의 숫자인가 | 2,430은 kernel build가 아니라 DynamoRio build의 프로세스 수(A1) |
| 단위(unit) | 무엇당, 어떤 단위인가 | González & Mark의 "~3 min"은 작업(task)당이 아니라 사건(event)당(K4 C-gonzalez-3) |
| 통계량(statistic) | 평균인가 중앙값인가 위치 모수인가 | Roeser의 158 ms는 로그 척도의 위치(중앙값에 해당)인데 저장소는 평균으로 저장하고 평균으로 샘플링함(A3, 영향 약 6 %) |
| 범위(scope) | 어떤 조건에서 성립하나 | Coetzee의 "enormous number of short-lived processes"는 `cp`, `mkdir` 같은 프로세스이고 컴파일러를 말하지 않음(A4) |
| 모집단(population) | 누구/무엇의 집합에서 나왔나 | Dhakal의 238.66 ms는 168,960명이 외운 문장을 옮겨 친 결과의 "참가자별 평균의 평균"인데, 저장소는 이것을 한 사용자 입력 흐름의 평균으로 씀(A3); LAVD의 "~300 tasks"는 게임 하나가 아니라 시스템 전체의 task 수(K2 C-lavd-1) |

**(5) 독립적으로 읽는다.** "The source is read independently, without the repository's description of the claim, before the reading is compared with the repository's wording." 출처를 읽는 사람은 저장소가 그 출처에 대해 뭐라고 적었는지 모르는 상태에서 읽고, 그다음에 비교합니다. 이것이 왜 중요한지는 소프트웨어 엔지니어에게 익숙한 비유로 설명할 수 있습니다. 테스트의 기대값을 구현 코드를 보고 적으면, 구현의 버그가 기대값에 그대로 복사됩니다(snapshot test를 처음 찍을 때 버그까지 같이 찍히는 것과 같습니다). 저장소의 설명을 들고 원문을 읽으면, 원문에서 그 설명과 닮은 문장을 찾게 됩니다. 2026-09-13 검증은 이것을 구조로 막았습니다. 읽는 사람(reader)에게는 `topics.md`의 **중립 주제(neutral topic)**만 주었습니다. 예를 들어 `ocallahan-atc17`에 대한 주제는 "in the paper's section describing its benchmark workloads, what the kernel-build workload builds and how it is configured; any stated count of processes forked/exec'd by make …"였고, 저장소의 숫자 2,430은 주지 않았습니다.

**(6) 찾지 못하면 미검증이다.** "A claim whose passage is not found is unverified." 구절을 못 찾았다고 "아마 맞을 것"으로 두지 않습니다. 예를 들어 `zhang-chb15`(Computers in Human Behavior 2015, 작업 전환 연구)는 사본에 닿을 수 없어(닫힌 접근, ScienceDirect 403, Elsevier API 429) 검증에서 UNVERIFIABLE이 되었고, 9.10 D1(2026-10-01)이 "a reference or a work of literature whose copy is technically unreachable or paywalled is dropped"라는 규칙으로 데이터셋과 `references.md`에서 뺐습니다.

**(7) 출처가 말하지 않는 값은 꼬리표를 단다.** 2.6절에서 본 그대로입니다. 이 요소가 막는 실패의 예는 critical findings memo B2입니다. `compiler-child.disk_wait`의 `sigma_log: 0.8`은 측정 이전에 넣은 임시값이었는데, 중앙값만 측정값으로 바뀌면서 태그가 `meas-ci:cli:3`로 바뀌었고, 그 결과 측정되지 않은 퍼짐(spread)이 측정 태그를 달고 있었습니다(커밋 이력 `df2c5f5` → `349423b` → `8416025`).

결정 1은 꼬리표를 넷(convention, arithmetic, placeholder, design)으로 적었지만, timeline lint는 셋을 받습니다(`BOUND_LABELS = ("design", "convention", "arithmetic")`, `dataset/tools/wlc/linter.py`). timeline의 bound value에 대해서는 9.10 D32가 결정 1보다 뒤의 결정이고, D32는 셋만 적었습니다(2.6절). 측정을 기다리는 값은 `meas-pending` 태그를 달며, 9.23 D13(2026-10-15)부터 `make lint`가 `lint.py --freeze`를 돌려 그것을 거부합니다("meas-pending after freeze"). 그래서 측정을 기다리는 값은 freeze 뒤에 데이터셋에 들어올 수 없습니다. 인지오가 2026-10-16에 이 방식을 규칙으로 정했고(placeholder 꼬리표는 두지 않음), freeze 검사는 그날부터 timeline의 bound value에도 걸립니다(9.15 작업 목록 W-0750). 지금 library에도 timeline에도 `meas-pending`은 하나도 없습니다.

## 3.3 결정 2 — archetype 안에서 montage 금지

> "All numbers of one archetype come from one observation: one study population, one trace, or one measurement run. Several documents about the same observation count as one source; one document mixing different traces does not. Our own measurement run counts as one observation. Research looks for one observation that covers the whole archetype first; where none exists, the archetype comes to 인지오 as a decision."

**montage**는 영화에서 서로 다른 장면을 이어 붙여 하나의 흐름처럼 보이게 하는 편집입니다. 이 결정이 금지하는 것은, 한 archetype의 숫자들을 서로 다른 관찰에서 가져와 하나의 프로그램처럼 보이게 이어 붙이는 일입니다.

왜 이어 붙이면 안 되는지는 예로 보는 것이 가장 빠릅니다. Phase 9 이전의 `desktop-interactive` archetype이 그런 montage였습니다. critical findings memo B5에 따르면, 이 archetype의 입력 간격(키 입력 사이의 시간)은 타이핑 연구(Dhakal, Roeser)에서 왔고, 입력마다 쓰는 CPU는 interbench의 X 부하에서 왔습니다. 그런데 interbench의 X 부하는 "an idle gui where a window is grabbed and then dragged across the screen", 곧 창 하나를 잡아 화면 위로 끌고 가는 동작이며, interbench는 이것을 1 ms 조각으로 0 %에서 100 %까지 올라가는 결정적 경사(ramp)로 구현합니다(`interbench.c`의 `emulate_x`, 커밋 `e612a65c`). 타이핑 간격과 창 끌기 CPU 비용을 이어 붙인 결과, `burst_fraction`이 `uniform(0, 1)`이라 burst(입력 하나에 깨어나 CPU를 연속으로 쓰는 덩어리)의 기댓값이 간격의 절반이 되었고, 초점을 받은 편집기가 CPU를 약 50 % 쓰는 workload가 되었습니다(`c1-compile`의 `code` task가 56 s 초점 구간 동안 28,470,806 µs의 CPU 수요). 실제 편집기보다 훨씬 무거운 부하이고, 초점을 받은 상호작용 task를 가진 모든 파일이 그것을 물려받았습니다. 그리고 그 입력 간격 자체도 Roeser의 혼합 분포 모양에 Dhakal의 전체 평균을 맞춰 닫은 것이었으니(A3), 서로 다른 두 모집단의 이어 붙이기였습니다.

결정 2는 이렇게 막습니다. 한 archetype의 숫자는 하나의 관찰에서 와야 합니다. 같은 관찰에 대한 여러 문서(논문과 그 논문의 데이터셋, 발표와 그 녹화)는 하나로 셉니다. 반대로 한 문서 안에 서로 다른 trace가 섞여 있으면 하나로 세지 않습니다. 그리고 **우리 자신의 측정 run도 하나의 관찰로 셉니다** — 이 한 문장이 Phase 9의 방향을 바꿨습니다. 문헌에서 한 관찰로 archetype 전체를 덮을 수 없으면, 우리가 그 프로그램을 직접 재면 하나의 관찰이 되기 때문입니다. 12장에서 보듯 9.5부터 9.10까지의 조각들은 거의 모두 이 길을 택했습니다.

"one document mixing different traces does not"의 실제 적용은 9.4 D1(2026-09-13)에 있습니다. LAVD 슬라이드 12–17장은 이름 없는 게임 하나에 대한 관찰처럼 보이지만, 9.4의 검색은 슬라이드의 그림들이 적어도 세 개의 프로세스 트리(`Troy.exe` tgid 7781, `GameThread` + `redDispatcher1–7` tgid 6340, `Umask: 0022` 스레드 tgid 4727)에서 나왔고 본문은 12–14장이 어느 것에서 나왔는지 말하지 않는다는 것을 찾았습니다. 그래서 이것을 "한 관찰"로 받아들이는 일은 결정 2의 기본값이 아니라 **인지오의 결정**으로 기록되었습니다("`game-task-chain` keeps `lavd-ossna24` as its one source under phase decision 2, by 인지오's decision").

## 3.4 결정 3 — 그 규칙을 timeline에 적용하기

> "Timeline content presented as how real desktops behave — task sets, co-occurrence, order, counts, typical durations, process names — follows decision 2, one observation per situation. The experiment's own interventions and calibration sizes — label flips, injections, renames, file length, `lane_share` — are labelled as design and carry no source tag."

timeline은 archetype과 다른 종류의 주장을 합니다. "이 프로그램이 이렇게 행동한다"가 아니라 "이런 프로그램들이 함께, 이 순서로, 이만큼 오래 돈다"입니다. 결정 3은 timeline 내용을 둘로 나눕니다.

- **현실 주장으로 제시된 내용**: 어떤 프로그램들이 함께 도는가(task set), 동시 출현(co-occurrence), 순서, 개수, 전형적 지속 시간, 프로세스 이름. 이것은 결정 2처럼 "상황 하나당 관찰 하나"를 따라야 합니다.
- **실험 자체의 개입과 보정 크기**: 라벨 뒤집기(label flip, 같은 파일에서 정답 라벨만 바꾼 짝을 만드는 것), 주입(injection, 방해 프로그램을 끼워 넣는 것), 이름 바꾸기(rename), 파일 길이, `lane_share`(게임 chain이 CPU 한 개 중 얼마를 쓰도록 크기를 맞출지 정하는 값). 이것들은 현실 주장이 아니므로 design 꼬리표를 달고 출처 태그를 달지 않습니다.

이 결정의 실제 귀결은 9.10(시나리오와 timeline 조각)의 결정들에서 볼 수 있습니다. 9.10 D2(2026-10-01)는 "the core set's task sets are design"으로 정했습니다. 이유는 core set이 "one file per claim"으로 지어졌고, 9.10의 검색이 "no observation of which programs run together on Linux desktops"를 찾았기 때문입니다(가장 가까운 후보는 SWELL-KW로, Windows 7 실험실에서 2012년에 기록된 것이며 Outlook, Word, IE가 근무 시간의 63.4 % 동안 함께 열려 있었습니다). 즉 결정 3이 "현실 주장이면 관찰이 있어야 한다"고 했고, 관찰이 없었으므로 task set은 현실 주장의 지위를 내려놓고 design이 되었습니다. 그 대가도 기록되었습니다. "the scheduling-benefit result holds on these compositions, which are not shown to be typical." scheduling 이득은 이 조합들 위에서 성립하며, 이 조합들이 전형적이라고 보인 것은 아니라는 한계 문장입니다.

같은 방식으로 9.10 D29는 세 arc(`c3-workday`, `c3-creation`, `c3-evening`, 하루의 흐름처럼 mode가 이어지는 파일)의 순서를 design으로 정했고, 9.10 D31은 남은 보정 크기들(`lane_share` 0.9/0.95/1.45/0.6, 60 s 길이, 2 s 도착, 30 s 주입 등)을 각자의 전제와 함께 design으로 기록했습니다. 그리고 `c6-spoof`의 `chrome`이라는 이름을 단 일괄 작업은 `total_work: 30s`, `program: spoof`에 "design: by construction"이라는 꼬리표를 답니다(`bound-values.md`).

## 3.5 결정 4 — 연구가 빈자리를 채운다

> "Where the current sources do not ground a value or a structure, the phase researches new grounding rather than leaving the gap empty. A slice declares that no single observation exists only after a search log covering four classes — peer-reviewed and preprint literature; primary project and vendor documentation and source code; public traces and datasets; whether our own measurement can observe it — with the terms, venues and results recorded, and then brings 인지오 the nearest candidates with what each covers and does not."

이 결정은 두 가지를 정합니다. 첫째, 근거가 없는 자리를 비워 두거나 대충 메우지 않고 새로 찾습니다. 둘째, "관찰이 없다"고 선언하려면 **네 부류(four classes)**의 검색을 마친 기록이 있어야 합니다.

| 부류 | 각 조각의 기록 파일 | 무엇을 찾나 |
|---|---|---|
| S1 — 동료 심사 문헌과 preprint | `search/S1-literature.md` | 논문의 측정, 표, 그림 |
| S2 — 프로젝트와 벤더의 1차 문서, 소스 코드 | `search/S2-project-docs.md` | 매뉴얼, 소스의 상수, 기본 설정 |
| S3 — 공개 trace와 데이터셋 | `search/S3-traces-datasets.md` | 버그 리포트의 측정, 공개 trace, 로그 |
| S4 — 우리 측정이 관찰할 수 있는가 | `search/S4-ci-observability.md` | runner 위에서 그 프로그램을 돌리고 볼 수 있는가 |

검색 기록에는 검색어, 찾아본 곳(venue), 결과가 적혀야 하고, 그 끝에 "가장 가까운 후보들과 각 후보가 덮는 것과 덮지 않는 것"을 들고 인지오에게 옵니다. 각 조각 폴더의 `search/candidates.md`가 그 정리이며, 후보 id는 부류를 따라 `S1-xx`, `S2-xx`, `S3-xx`, `S4-xx`로 붙습니다. 12장에서 조각마다 이 기록을 봅니다.

S4라는 부류가 있다는 점이 결정 2와 맞물립니다. 문헌, 문서, 공개 trace 어디에도 한 관찰이 없을 때, "우리가 직접 잴 수 있는가"가 네 번째 질문으로 항상 남습니다. 그래서 Phase 9의 검색 결과는 대부분 "기존 관찰 없음 → 우리 측정으로"였습니다.

## 3.6 결정 5 — 측정 장소

> "Our own measurement runs on CI runners only. What a runner cannot observe comes from literature or public traces, or to 인지오 as a decision. This is a stated limitation."

우리 측정은 CI runner(GitHub Actions가 빌려주는 가상 머신)에서만 합니다. runner가 볼 수 없는 것은 문헌이나 공개 trace에서 오거나, 인지오의 결정이 됩니다. 그리고 이것은 숨기지 않고 밝히는 한계입니다.

이 결정의 실제 의미는 6장과 11장에서 길게 보지만, 미리 요점만 적으면 이렇습니다. runner에는 화면 주사율(display refresh)도, GPU도, 소리 장치도, 사람도 없습니다. 그래서 측정된 값은 `measurement-overview.md` §11의 말대로 "this software on this machine", 이 소프트웨어가 이 기계에서 보인 행동이지 "desktop truth"가 아닙니다. 대신 누구나 같은 workflow를 다시 돌릴 수 있고, 원자료가 공개됩니다.

결정 5를 어떻게 적용했는지는 9.5 D3(2026-09-14)에 이유와 함께 기록되어 있습니다. 상호작용 프로그램 여섯 개의 값을 runner 측정 캠페인에서 가져오기로 하면서, 기록된 이유는 "인지오 judges values measured on 100–664 MHz machines two decades ago unable to back a current application"과 "the search found no newer per-input observation of a Linux editor, office suite, mail client, browser, image editor or video editor"였습니다. 문헌에 있는 Linux 데스크톱 측정은 20년 전 100–664 MHz 기계의 것이라 지금의 프로그램을 받칠 수 없다고 판단했고, 더 새로운 관찰은 찾지 못했다는 것입니다. 같은 날 9.5 D10은 runner에서 잰 절대값을 "convention informed by measurement"(측정으로 정보를 얻은 관례)라는 낮은 등급으로 두지 않고 "a source claim whose source is the run"으로 올렸습니다. 기록된 이유는 "the values are observations of that software on that machine, the only current Linux observations obtainable"이며, 낮은 등급으로 두면 "no interactive archetype would meet decision 2"라는 것이었습니다.

결정 5와 결정 2를 함께 적용하면, 측정 장소가 다른 두 archetype을 한 timeline에 함께 두는 일이 생깁니다(예: runner에서 잰 편집기와 LAVD 발표에서 온 게임 chain). 9.5 follow-ups spec decision 13은 이것을 "Scale limitation at the composition seam"이라 부르고 "stated once at the library level"로 정했으며, 민감도 점검은 9.14에 넘겼습니다. 이 library 수준의 한계 문장은 9.15에서 archetype plan(`docs/workload/archetype-plan.md`) §2의 "Observation venues" 단락에 들어갔고, 그 문서에만 있습니다. "The library's archetypes come from more than one observation venue, and their relative scales are not calibrated to each other; a timeline composing a runner-measured task with a literature-grounded one carries that limitation." 장소는 둘입니다. 측정된 entry 28개(모든 값이 GitHub runner의 AMD EPYC 7763 코어 하나의 것)와, `lavd-ossna24` 발표 슬라이드에서 온 lane-scaled `game-task-chain`입니다. 민감도 점검은 venue variant `venue-x0.8`과 `venue-x1.25`(게임 chain을 뺀 모든 RUN을 0.8배와 1.25배로, 9.14 decision 12)입니다.

## 3.7 결정 6–8: 일의 구조, 팀 소통, 끝내는 조건

나머지 결정 가운데 이 권과 닿는 것을 요약합니다.

- **결정 6, 구조.** 먼저 2026-09-13 검증 기록을 저장소에 저장하고(9.1) 측정 도구를 고치며(9.3, `meas-ci:names:2` run을 그 artifact가 2026-12-09에 만료되기 전에 보존하는 일 포함), 그다음 영역별 연구-결정 조각을 병렬로 돌리고(게이밍, 상호작용과 타이핑, 컴파일, 백그라운드와 IO, 브라우저와 통신, 데몬과 세션, 시나리오와 timeline, scheduler 쪽 상수, 관련 연구 서술 — 9.4부터 9.12), 그다음 데이터셋을 한 번 다시 짓고(9.13), 소비자 쪽을 한 번 다시 고치고(9.14), 마지막으로 문서를 한 번 정리합니다(9.15). 2026-10-11에 그 정리 앞에 telemetry의 focus, 컴파일러와 build gate 수정, 생성기와 grid들, 그 소비자 작업(9.17–9.22)이 추가되었습니다.
- **결정 7, 팀 소통.** 시작할 때 인경민(simulator 담당)과 박이안(daemon 담당)에게 무엇이 바뀌고 무엇이 그대로인지 알리는 heads-up memo(9.2, `docs/memos/2026-09-13-dataset-rebuild-heads-up.md`), 끝날 때 실제 변경을 담은 최종 memo.
- **결정 8, 끝내는 조건(exit criteria).** "Every finding is resolved. The claim audit, the measurement audit and the compiled-number audit are re-run on the final repository state and return nothing unresolved: every claim meets decision 1, every archetype and every realism claim in a timeline meets decisions 2 and 3 or carries 인지오's recorded decision, every measured value reproduces from the released raw data and describes what its method measured, and no statement in the prior table, pair review, scoring spec, guard spec, RQ0 gate spec or memos is wrong or stale against the rebuilt data." 세 가지 감사 — 주장 감사, 측정 감사, compile된 숫자 감사 — 를 최종 상태에서 다시 돌려 아무것도 미해결로 남지 않아야 Phase 9가 끝납니다. 이것이 9.16이며, 14장에서 봅니다.

spec 끝의 "Open items"는 "The format and location of the verification records, and whether source copies are kept"(→ 9.1), "How the measurement tools are fixed"(→ 9.3), "Each archetype's and each timeline's values and structure"(→ 각 조각)를 하위 작업의 spec 세션에 남겼습니다. 다음 두 장이 그 첫 두 자리를 채운 이야기입니다.

---

# 4장 · 2026-09-13 검증과 critical findings

이 장은 "2026-09-13에 무엇을 어떻게 확인했고, 무엇이 틀렸다고 나왔으며, 그것이 각각 무엇을 바꿨는가"라는 질문에 답합니다. 이 질문이 중요한 이유는, Phase 9의 모든 결정이 이 검증을 출발점으로 삼기 때문입니다. 9.4부터 9.12까지의 연구 조각은 각자의 할 일 목록(scope card)을 이 검증 기록에서 뽑았습니다(`research-slice-workflow.md` stage 1).

## 4.1 검증 세션의 구조

검증은 저장소 커밋 `e3d3c9a`를 대상으로 했습니다. 다섯 부분으로 되어 있고, 그 결과는 9.1이 `_dev/research/jioh/2026-09-13-verification/`에 저장했습니다(5장).

```
 (1) 주장 목록                 (2) 독립 읽기                (3) 비교
 claims.md ───────────┐      inputs/R01–R11             compare/K1–K5
  저장소가 외부 출처에서   │      (읽는 이가 받은 것:         (읽기 결과 ↔ 저장소 문장,
  가져온 모든 주장,       ├────▶  bib 항목 + 중립 주제만) ──▶  위치마다 판정)
  위치와 원문 그대로       │      reads/R01–R11
 topics.md (중립 주제) ────┘      (사본, 원문 구절, 판정)
 bib.md (서지)

 (4) 측정 감사                                 (5) compile된 숫자 감사
 meas-report.md + meas/                         compiled-numbers-report.md + 스크립트
  dataset/meas/summary.json을 release            결정 문서들의 숫자 진술을
  meas-ci-2026-08-28에서 재현, 방법 감사,            실제 build에 대고 HOLDS / STALE / WRONG /
  meas-ci 파라미터마다 M / D / C / X 분류             UNCHECKABLE 판정
```

**(1) 주장 목록(claim inventory), `claims.md`.** 저장소가 외부 출처에서 가져온 모든 주장을 위치(`file:line`)와 원문 그대로 모은 목록입니다. 첫머리가 스스로를 "Read-only inventory; nothing fetched from the web; no claim judged"라고 규정합니다. 판정은 이 파일에서 하지 않습니다. Part 1은 출처별 주장(`C-<source>-<n>` 형식의 id), Part 2(a)는 `archetypes.yaml`의 모든 숫자와 그 태그, Part 2(b)는 timeline의 숫자, Part 3은 시나리오 태그, Part 4는 출처별 개수입니다. Part 4의 합계는 "177 (176 distinct + 1 cross-reference)", 경계선(borderline, 저장소가 출처에 대해 주장하는 것인지 불분명한 문장) 29개입니다. Part 2(a)는 45개 숫자 행 가운데 17개에 FLAG(외부 태그가 붙어 있으나 의심되는 값)를 달았습니다(interbench 6, `dhakal-chi18` 태그 6, `lavd-ossna24` 5). Part 2(b)의 결론은 짧습니다. "0 numbers in timelines justified by an external (non-meas) citation; 1 number justified by a meas-ci citation." 당시 timeline의 숫자 가운데 외부 문헌으로 정당화된 것은 하나도 없었다는 뜻입니다.

**(2) 독립 읽기(independent read), `reads/R01–R11`.** 출처를 열한 묶음으로 나눠 읽는 이(reader)마다 하나씩 맡겼습니다. 읽는 이가 받은 것은 `inputs/R01–R11`, 곧 서지 항목과 `topics.md`의 중립 주제뿐이며, 저장소의 숫자나 문장은 받지 않았습니다. 각 read 문서는 "Copies used" 표(URL 또는 커밋, 판본, 날짜, 로컬 경로, SHA-256)로 시작하고, 주제마다 원문 구절과 위치, 그리고 판정을 적습니다. read의 판정 어휘는 `FOUND`(찾음), `PARTIAL`(일부), `NOT FOUND`(못 찾음), `PREMISE NOT IN SOURCE`(주제의 전제 자체가 출처에 없음), `COPY UNREACHABLE`(사본에 닿지 못함)입니다.

| read | 출처 |
|---|---|
| R01 | interbench, rt-app, hackbench, schbench, stress-ng, kernel build |
| R02 | `lavd-ossna24`, `corbet-lwn24`, scx |
| R03 | `ocallahan-atc17`, `coetzee-arxiv12`, `schedcp-mlsys25` |
| R04 | `cpsmark-tbench23` |
| R05 | `pcmark10`, `sysmark30`, `sysmark25`, `procyon` |
| R06 | `ananicy-rules`, ananicy |
| R07 | `gamemode-docs`, `steam-downloads`, `dkms-man`, `dkms-debian` |
| R08 | `dhakal-chi18`, `roeser-rw24` |
| R09 | `dubroy-chi10`, `chang-chi21`, `mozilla-testpilot10`, `singervine-slate10` |
| R10 | `zhang-chb15`, `gonzalez-chi04`, `mark-chi05`, `mark-chi08`, `mark-chi14`, `czerwinski-chi04`, `mark-gallup06`, `swell-icmi14` |
| R11 | `focal-arxiv26`, `videogui-arxiv24`, 출처 없이 적힌 일반 주장 C-plain-1–9 |

이 표는 2026-09-13에 읽은 것의 기록입니다. 그 가운데 `zhang-chb15`는 2026-10-01(9.10 D1)에, `dkms-man`, `dkms-debian`, `dubroy-chi10`, `chang-chi21`, `mozilla-testpilot10`, `singervine-slate10`은 2026-10-16(9.15)에 `references.md`를 떠났습니다(2.4절). 같은 날 참고문헌 전용 항목 `mark-chi08`, `mark-chi14`, `mark-gallup06`, `videogui-arxiv24`도 `references.md`를 떠났습니다. 9.10 D169가 이 항목들을 9.15에 넘기며, 본문이 인용하는 항목은 판정에 맞게 고쳐 남기고 나머지는 빼도록 정했습니다.

**(3) 비교(comparison), `compare/K1–K5`.** 읽기 결과를 저장소의 문장과 위치마다 맞대어 판정했습니다. K1은 R01과 R03, K2는 R02와 R04, K3은 R06과 R07, K4는 R08, R09, R10(그리고 DOI 아홉 개에 대한 Crossref 기록), K5는 R05와 R11을 비교합니다. 비교자는 읽기 결과만 믿지 않고 필요하면 원문을 다시 열었습니다(예: K1은 `interbench.c`의 `periodic_schedule()` 378–457행, `emulate_compile` 770–797행을 직접 열었습니다). README는 비교 단계에서 바로잡은 입력 오류 세 가지도 적어 둡니다. R11이 C-plain-9를 엉뚱한 도구에 대해 답한 것(K5가 다시 판정), R01이 C-hackbench-2에 붙인 "premise" 판정(K1이 정정), `claims.md`에서 자리를 잘못 잡은 C-plain-7 한 줄(K5가 지적).

**(4) 측정 감사(measurement audit), `meas-report.md`.** 그때의 측정 요약 `dataset/meas/summary.json`(Phase 2의 요약; 9.15가 2026-10-16에 지웠고(커밋 `37c2e233`), 그 앞의 커밋에서 읽을 수 있습니다)을 원자료 release `meas-ci-2026-08-28`에서 다시 만들어 보고(재현 결과: `out_cli3.json`이 `summary.json`과 바이트 단위로 같았습니다, 1,083개 leaf field), 측정 방법을 감사하고, `meas-ci` 태그를 단 파라미터마다 M(measured, 재현됨), D(derived, 산술 확인), C(convention 또는 placeholder), X(불일치)로 분류했습니다. X 항목이 X1부터 X16까지 열여섯 개입니다(4.6절).

**(5) compile된 숫자 감사(compiled-number audit), `compiled-numbers-report.md`.** 우선순위 표, 짝 검토(pair review), scoring spec, guard spec, RQ0 gate spec, memo, spec들에 적힌 "compile된 파일이 이렇다"는 숫자 진술을 실제 build에 대고 판정했습니다. 판정 어휘는 `HOLDS`(성립), `STALE`(낡았으나 결론은 성립), `WRONG`(틀림), `UNCHECKABLE`(확인 불가)입니다(4.7절).

## 4.2 판정 어휘

비교 단계의 판정 어휘는 일곱 개입니다. 이 어휘는 뒤의 연구 조각들이 scope card에서 그대로 씁니다.

| 판정 | 뜻 |
|---|---|
| `SUPPORTED` | 출처가 그 주장을 그대로 받침 |
| `WORDING-FIX` | 내용은 맞으나 표현을 출처에 맞게 고쳐야 함 |
| `MISATTRIBUTED` | 출처가 말하는 내용이지만 다른 대상, 다른 출처, 다른 위치의 것임 |
| `CONTRADICTED` | 출처가 반대를 말함 |
| `NOT IN SOURCE` | 출처에 그런 내용이 없음 |
| `OURS-UNDER-SOURCE-TAG` | 우리가 만든 값이나 해석인데 출처 태그를 달고 있음 |
| `UNVERIFIABLE` | 사본에 닿지 못해 확인할 수 없음 |

`OURS-UNDER-SOURCE-TAG`가 특히 중요합니다. 이것은 거짓말이 아니라 표시의 실패입니다. 예를 들어 interbench의 video 부하 상수는 소스에서 `VIDEO_INTERVAL 1000000/60` = 16666 µs인데 저장소는 16,667/6,667 µs를 interbench 태그로 들고 있었습니다(K1 C-interbench-2). 1 µs 차이는 사소하지만, 반올림을 우리가 했다면 그것은 우리 산술이고 태그는 그렇게 말해야 합니다. 3장의 결정 1이 "label it for what it is"라고 한 이유가 이런 사례들입니다(기록된 이유가 아니라 결정이 다루는 사례라는 뜻입니다).

## 4.3 주장 하나를 끝까지 따라가기: C-ocallahan-1

검증이 실제로 어떻게 돌아갔는지, 1장의 2,430을 처음부터 끝까지 따라가 보겠습니다.

**주장 목록.** `claims.md`는 이 주장이 저장소의 열 군데 넘게 있다고 기록했습니다: `sources.yaml:70-72`, `references.md:107`, `archetypes.yaml:202-204, :247-248`, `archetype-plan.md:53`, `building-plan.md:61`, `source-vetting.md:70, :95, :123`, `scenario-catalog.md:22`. 

**중립 주제.** 읽는 이(R03)가 받은 주제는 이랬습니다. "C-ocallahan-1: in the paper's section describing its benchmark workloads, what the kernel-build workload builds and how it is configured; any stated count of processes forked/exec'd by make and any characterization of their lifetimes; the next workload listed and its count." 저장소의 2,430은 주지 않았습니다.

**독립 읽기.** R03은 USENIX ATC '17 proceedings PDF(SHA-256 `589ec379…`), arXiv:1705.05937v1, 그 전신인 arXiv:1610.02144v1을 모두 내려받아 읽었습니다. 판정은 `PREMISE NOT IN SOURCE`였습니다. "The paper has no kernel-build workload. Its build workload, named *make*, builds **DynamoRio 6.1.0** with `make -j8`." 그리고 검색 방법까지 적었습니다. 세 판본 전체에서 `lifetime`, `short-lived`, `kernel`, `build`, `compil`, `vmlinux`, `defconfig` 등을 grep했고, "`kernel` hits never refer to building a kernel"이었습니다.

**비교.** K1은 R03의 결과를 원문 텍스트로 다시 확인한 뒤 위치마다 판정했습니다. `sources.yaml:70-72`와 `references.md:107`과 `archetypes.yaml:247-248`(기본값 2,430)은 `MISATTRIBUTED`, `archetypes.yaml`의 `category_source` 태그와 "kernel-build literature"라는 표현은 `WORDING-FIX`("the source … names neither compilers nor a behaviour category"), `source-vetting.md:70`의 "next workload: 89"는 `WORDING-FIX`("89 belongs to the 'next most prolific workload' (sambatest)"). 그리고 영향 범위를 적었습니다. 이 오귀속은 구조 태그, 문서의 기본값, 카탈로그 한 행에 닿을 뿐 "not a compiled number"였습니다. 당시 어느 timeline도 2,430을 쓰지 않았기 때문입니다(`c1-compile` 100, `c6-dual` 85, `c3-workday` 4,200).

이 한 사례에서 결정 1의 모든 요소가 보입니다. 원문 구절, 위치(§4.1과 §4.3의 구분), 사본(세 판본과 SHA-256), 대상(무엇의 숫자인가), 독립 읽기(중립 주제), 그리고 비교.

## 4.4 critical findings memo의 발견들과, 각각이 바꾼 것

critical findings memo(`docs/memos/2026-09-13-critical-findings.md`, Status: memo, Created/Updated 2026-09-13)는 "Findings from checking `dataset/archetypes.yaml` and its grounding documents against the primary sources and against the compiler, measurement summary and raw measurement release"이며, "Nothing in the repository was changed; resolution is left to the owners of each file"라고 스스로를 규정합니다. 요약표에는 A1–A5(원문이 저장소의 설명과 모순), B1–B7(데이터셋과 도구), C(측정을 반영한 뒤 남은 낡은 문장), D(원문과 대조하지 않은 출처)가 있습니다.

Phase 9 spec과 2026-10-10 감사는 이 memo의 발견을 "13"개로 셉니다("The 13 findings in `docs/memos/2026-09-13-critical-findings.md`", "the 13 + 6 critical findings"). memo의 요약표에는 A1–A5 다섯, B1–B7 일곱, C 하나, D 하나로 열네 행이 있는데, 13은 A1–A5, B1–B7, C입니다. D는 원문과 대조하지 못한 출처의 목록이지 발견이 아닙니다(인지오의 답, 2026-10-16; 9.15 작업 목록 W-0749). 그래서 memo의 내용은 "발견 열셋과 읽지 못한 출처의 목록 하나"입니다. 이 권은 열네 행을 모두 다룹니다.

아래 표는 각 발견이 무엇이었고, 그 뒤 어떤 결정이 그것을 다뤘는지입니다. "다룬 결정" 열은 그 주제를 실제로 바꾼 기록을 적은 것이며, 자세한 값은 archetype library를 다루는 2권과, timeline과 coreset을 다루는 3권과 4권이 다룹니다.

| 발견 | 무엇이 틀렸나 | 그 뒤 무엇이 바뀌었나 |
|---|---|---|
| A1 | `ocallahan-atc17`의 2,430은 DynamoRio build | 9.6이 kernel build를 직접 재어(`meas-ci:build:2026-09-18`) `build-orchestrator`가 측정된 build 전체를 묶게 됨: object job 2,908개, `parallelism_cap` 8(9.10 D18). 카탈로그의 2,430 출처 줄은 9.10 D33이 뺌. `sources.yaml`과 `references.md`의 문장은 9.15(2026-10-16)에서 DynamoRio build로 고쳐짐(2.4절). `compiler-child`의 `modeling_notes`는 2026-10-17에 같은 내용으로 고쳐짐 |
| A2 | 16.7 ms frame budget이 LAVD 슬라이드에 없음 | 9.4 D2: `frame_period` 16,667 µs는 그대로, 태그를 `lavd-ossna24` → `steamos-refresh`로, "design — display-paced at the Steam Deck LCD default refresh … 1/60 s arithmetic"으로 표시. LAVD registry notes에 "States no frame period or frame budget" 추가 |
| A3 | Roeser의 158 ms는 로그 척도 위치인데 평균으로 저장·샘플; 논문 자신의 pause 성분(≈253 ms)은 안 쓰고 Dhakal의 평균으로 닫음 | 9.5가 `desktop-interactive`를 응용 프로그램별 측정 archetype으로 대체(9.5 D2, D19). 타이핑 자극은 SWELL-KW 기록을 재생(9.5 D4). `dhakal-chi18`과 `roeser-rw24`는 "Paper-only after Phase 9"(역할 줄 2026-09-14 정정) |
| A4 | Coetzee의 짧은 프로세스는 `cp`, `mkdir` | `compiler-child`가 측정값으로 바뀌면서 `coetzee-arxiv12`가 받치는 값이 없어짐. 그 항목의 `modeling_notes`에는 "coetzee-arxiv12 sec-9 corroborates"가 2026-10-16까지 남았고, 2026-10-17에 9.15의 재빌드가 Coetzee는 리눅스 커널 빌드의 짧게 사는 많은 프로세스를 `cp`와 `mkdir`을 예로 수 없이 말한다고 고쳐 적음. `coetzee-arxiv12`는 지금 아무 값도 받치지 않음 |
| A5 | `ananicy-rules`의 `type`은 처방(prescription)이지 행동 분류가 아님; 수확 규칙이 고르지 않게 적용됨 | 28개 측정 항목의 `category_source`가 모두 `meas`가 됨(나머지 하나 `game-task-chain`은 `lavd-ossna24`). `ananicy-rules`는 `sources.yaml`에 없음. 9.12 D1은 이것을 비교 조건이 재현하는 이름 기반 카탈로그로 다룸(근거가 아니라 비교 대상). 그 조건은 9.12 D6, D105 이후 `shipped_catalogue`(CachyOS가 ananicy-cpp와 함께 설치하고 켜는 카탈로그를 `03ef03fb` 시점 그대로, 각 process의 `argv[0]` basename으로 맞춤)이고, 옛 `whitelist` 조건의 다른 반쪽은 `strongest_name_table` |
| B1 | `game-task-chain`의 두 파라미터는 컴파일러가 읽지 않음; tail 파라미터는 슬라이드 태그를 단 placeholder; `n_tasks: 300`은 개수를 archetype 안에 둠 | 9.4 D3: `n_tasks`, `tail_idle_gap`, `tail_run` 삭제, 게임 파일마다 284개 tail task가 사라짐. 9.4 D7: 읽히지 않던 두 파라미터 정리 |
| B2 | `compiler-child.disk_wait`의 `sigma_log: 0.8`은 측정 태그를 단 placeholder | 9.6이 `compiler-child`를 단계별 CPU 표로 다시 측정, `disk_wait` 파라미터가 사라짐 |
| B3 | 측정된 동시 실행은 compiler 계열 16개, archetype의 상한은 8 — 단위가 다름 | 9.6 D2: 단위를 "make job 하나 = 역할별 프로세스 사슬"로. job 하나가 여섯 프로세스(`sh`, `gcc`, `cc1`, `as`, `fixdep`, `rm`)이므로 상한 8 job은 compile된 파일에서 `fork_cap` 48 |
| B4 | 끝없는 loop에 선언한 `per-iteration` 샘플링이 `per-task`로 compile됨; 측정 퍼짐은 프로세스 사이의 퍼짐 | 해당 항목 셋(`background-crawler`, `electron-comms`, `system-daemon`)이 모두 은퇴(9.7 D5, 9.8 D25, 9.9 D26)하고, 측정 항목은 스레드 종류별 component가 측정된 gap 표에서 wake마다 gap을 뽑는 형식으로 바뀜(9.5 D16, D17) |
| B5 | `desktop-interactive`의 burst가 입력 간격의 절반 → 편집기가 CPU 약 50 % | 9.5가 편집기, 워드프로세서 등을 실제 프로그램으로 측정. 입력 하나당 CPU(`input_run`)가 측정값(예: LibreOffice Writer 중앙값 3.23 ms) |
| B6 | `gnome-shell`, `Xorg`, `pipewire`가 서버 데몬 값의 `system-daemon`에 묶임; `wineserver`가 1,225 s를 잠 | 9.9가 `system-daemon`을 넷으로 나눠 유휴 Ubuntu 데스크톱 세션에서 측정, `xorg` 은퇴(9.9 D26). `wineserver`는 게임 chain의 구성원(9.4 D4, 260 µs, `lavd-ossna24:s13`) |
| B7 | 작은 틈들: linter가 `category_source`의 값이 아닌 존재만 검사; timeline `count`에 출처 칸 없음; `background-crawler`는 어디에도 묶이지 않음; "2.4×" 모호; CpsMark+ Table 4 오용; `electron-comms` 심판 판정의 근거 부족; schbench/hackbench archetype은 만들어진 적 없음; privacy-scrub 도구가 저장소에 없음 | count 출처 칸: 9.10 D32 → 9.18의 `source` map과 lint. `background-crawler` 은퇴(9.7 D5). Table 4는 9.10 D34/D170이 "CC module's best graphics-card configuration performing 1.77 times its base configuration"으로 역할을 다시 씀. `electron-comms`는 9.8이 넷으로 나눠 측정. privacy-scrub 도구의 약속은 거두어짐(인지오의 결정, 2026-10-16): 문서는 그 약속을 빼고, 실제 데스크톱 검증은 밝혀 둔 한계로 남음(`measurement-overview.md` §11; 11.3절) |
| C | 측정 반영 후 남은 낡은 문장(`references.md:280`의 "reserved (no runs yet)", `archetype-plan`의 `meas-pending`, `building-plan`의 "1 s" sampler, coreset-guide의 "~5.7 ms", README의 `wanted`) | 대부분 9.15의 문서 정리로 넘어감. `references.md`의 `meas-ci` 항목은 지금 "status: in use …"로 바뀌어 있음 |
| D | `chang-chi21`(ACM 403), `cpsmark-tbench23`(ScienceDirect 거부)를 원문과 대조하지 못했는데 둘 다 `verified` | 같은 검증의 R09가 `chang-chi21`을, R04가 `cpsmark-tbench23`을 다른 사본(Wayback 보관본 등)으로 읽음. 9.10 D1이 두 사본이 2026-10-01에도 닿는 것을 확인하고 유지. `chang-chi21`은 그 뒤 아무 값도 받치지 않고 본문도 인용하지 않아 9.15(2026-10-16)에서 registry와 `references.md`를 떠남(9.10 D34, 9.12 D102) |

이 표에서 눈에 띄는 패턴이 있습니다. 문헌 값을 고친 경우보다, 문헌 값을 **측정으로 대체한** 경우가 훨씬 많습니다. 결정 2(montage 금지)와 결정 5(runner 측정)가 합쳐진 결과입니다. 문헌 하나로 archetype 전체를 덮을 수 없으면 직접 재는 쪽이 한 관찰을 얻는 유일한 길이었습니다.

## 4.5 memo에 없던 여섯 가지

Phase 9 spec의 Scope는 memo 밖의 발견 여섯 개를 따로 적었습니다. 같은 날의 확인에서 나왔지만 memo에는 들어가지 않은 것들입니다.

1. **interbench의 Compile 부하는 프로세스를 하나도 fork하지 않는다.** K1 C-interbench-9는 `CONTRADICTED`였습니다. `archetype-plan.md:53`은 interbench의 Compile("heavy make -j4")이 compiler-child를 교차 확인한다고 적었는데, 원문의 Compile은 Burn, Write, Read 스레드 셋을 한 프로세스 안에서 돌릴 뿐입니다. 이것은 "이름이 같다고 같은 것을 말하는 것이 아니다"의 좋은 예입니다.
2. **"~5.7 ms" download sleep은 어떤 판본의 `archetypes.yaml`과도 맞지 않는다.** compile된 숫자 감사는 `network-bulk.net_wait`이 커밋 `8416025`(2026-08-28) 이후 16,700 µs였으므로 "~5.7 ms"는 한 번도 compile된 적이 없다고 확인했습니다. compile된 `c2-p2a` download의 SLEEP 중앙값은 16,712 µs, 평균 18,954 µs였습니다. 출처 없는 숫자가 문서(coreset guide)에만 떠돌던 경우입니다.
3. **Roeser의 Table 3은 archetype이 "convention"이라 부른 퍼짐을 보고한다.** Table 3에는 fluent 퍼짐 0.29가 두 과제 모두에 있었습니다(R08). 즉 관례라고 적었던 값 일부는 실제로 출처에 있었습니다. 표시가 틀린 방향이 "출처가 있는데 없다고 함"인 드문 예입니다.
4. **LAVD 슬라이드 12장과 16장의 wineserver.** 슬라이드 12장은 wine을 시스템 task로 분류하고, 16장의 그래프는 wineserver를 중심으로 한 구조를 보입니다(K2 C-lavd-4 `MISATTRIBUTED`). 9.4 D4가 wineserver를 chain의 구성원으로 넣고 260 µs(`lavd-ossna24:s13`)를 주었습니다.
5. **CpsMark+는 "time-shared compositions"를 반박한다.** `archetype-plan.md:69`는 창작 프로그램이 시간을 나눠 쓰는 조합이라는 주장에 `cpsmark-tbench23:table-4`를 달았는데, Table 4는 작업별 하드웨어 민감도(GPU/CPU/저장장치) 표입니다. 그리고 K2 C-cpsmark-6은 저장소가 인용한 "1.77×"가 Table 4가 아니라 Table 5의 CC 모듈 수치라고 `MISATTRIBUTED` 판정했습니다.
6. **`chang-chi21`의 세부.** K4는 "~8 %가 10개 넘는 탭을 열었다"는 `SUPPORTED`(정확히는 MTurk가 아닌 참가자 중 7.8 %), "Article 149"는 `UNVERIFIABLE`, "fatter modern tail"(현대의 탭 분포 꼬리가 더 두껍다)은 우리 해석(`OURS`)으로 판정했습니다. `chang-chi21`은 어떤 값도 받치지 않게 되었고, 9.15(2026-10-16)에서 registry와 `references.md`를 떠났습니다(2.4절).

## 4.6 측정 감사의 X 항목

측정 감사(`meas-report.md`)는 Phase 2의 측정 캠페인(2026-08-28의 `cli:3`, `gui:2`, `names:1`)을 재현하고 방법을 들여다봤습니다. 그 결과 X(불일치)로 분류된 열여섯 항목 가운데 데이터셋에 가장 크게 닿은 것들을 적습니다.

- **X1 compiler "child"는 compiler 계열 프로세스였다.** build 하나에 약 11.9k개 = gcc 약 2,990 + cc1 2,970 + as 2,950 + fixdep 2,890 + 기타 약 110, 번역 단위 하나에 약 네 개. cc1이 compiler CPU의 99 %를 쓰는데, "child 하나의 CPU"를 넷으로 나눠 계산했으니 cc1 하나의 CPU가 약 4배 작게 잡혔습니다. heads-up memo는 이것을 이렇게 요약했습니다: "compiler 'child'가 cc1 하나가 아니라 번역 단위당 process 네 개쯤(gcc·cc1·as·fixdep)이라 cc1 하나의 CPU가 약 4배 작게 잡혔어요."
- **X2 `disk_wait` 3,600 µs는 disk 대기를 잰 값이 아니었다.** cold build와 warm build의 수명 중앙값 차이(103,397 − 99,801 = 3,596 µs)였고, 그 차이는 warm build 자체의 퍼짐(76.9–105.7 ms) 안에 있었습니다.
- **X3 voluntary context switch를 main thread만 셌다.** **context switch**(CPU가 한 스레드에서 다른 스레드로 넘어가는 일; 스레드가 스스로 잠들어 넘기면 voluntary, 빼앗기면 nonvoluntary)를 `/proc/<pid>/status`에서 읽었는데, 커널은 그 값을 main thread 것만 보여 줍니다(`fs/proc/array.c` v6.17). 반면 CPU 시간은 모든 스레드를 합한 값이었습니다. 그래서 "wake 하나당 CPU"가 다중 스레드 프로그램에서 부풀었습니다.
- **X4–X7 workflow가 그 단계 이름이 말하는 행동을 만들지 않았다.** Element Desktop은 renderer 프로세스를 하나도 띄우지 않았고(X4), Chromium의 파일 탭 10개는 약 0.35 s 안에 renderer가 종료되었으며(X6), tracker는 300 s 동안 색인을 하지 않았습니다(X7, miner가 쓴 CPU 30–250 ms).
- **X8, X9 샘플링 단위.** `per-iteration`으로 선언한 퍼짐이 실제로는 프로세스 사이, 반복 사이의 퍼짐이었고(X8), 데몬 burst 값은 51개 중 CPU tick이 0이 아닌 29개에서만 계산되었습니다(X9).
- **X11 network-bulk의 "runner 링크를 포화시킨다"는 측정된 적이 없다.** download는 0.6–4.7 s였고 처리량은 기록되지 않았습니다.
- **X12 `dispatch_overhead`는 비율의 평균을 `median_us`로 저장했다.**
- **X14 이름 검증이 주장보다 약했다.** `tracker-miner-fs-3`은 **comm**(커널이 프로세스마다 저장하는 실행 파일 이름, 최대 15자)으로 한 번도 관찰되지 않았습니다(잘린 `tracker-miner-f`로만 보임). 카탈로그 이름 자체가 관찰되지 않았는데 `runtime` 등급을 준 경우가 있었습니다.
- **X16 `tar -cf /dev/null`은 파일 내용을 읽지 않는다.** GNU tar는 출력이 `/dev/null`이면 내용을 읽지 않으므로(`file_dumpable_p`, `dev_null_output`), "read stream"의 duty라던 값이 사실 읽기를 하지 않은 단계의 값이었습니다.

이 항목들은 두 갈래로 처리되었습니다. 도구가 실제로 일어난 일에 대해 틀린 숫자를 내는 결함(X1, X3, X5, X9, X12, X14)은 9.3이 고쳤고, 도구가 재지 않는 양이나 단계가 행동을 만들지 않는 설계 결함(X2, X4, X6, X7, X8, X11, X16)은 연구 조각으로 넘겨졌습니다(5장).

## 4.7 compile된 숫자 감사의 WRONG 항목

compile된 숫자 감사는 데이터셋을 소비하는 문서들의 숫자 진술을 확인했습니다. `WRONG`으로 나온 열 항목과, 같은 주제를 그 뒤에 다룬 기록을 함께 적습니다.

| 항목 | 내용 | 그 뒤 |
|---|---|---|
| J1 | `c2-p2a`에서 10 ms slice(scheduler가 한 번에 주는 CPU 시간 조각)로는 어떤 task도 batch class(executor가 CPU를 오래 쓰는 행동을 보고 분류하는 등급으로, 설정의 `batch_bandwidth_cap`이 그 몫을 제한함; `docs/recognition-vocabulary.md`)에 들어가지 않아 우선순위 표의 두 행(EDF, 곧 마감이 가장 이른 일을 먼저 돌리는 알고리즘에서 cap을 0.333과 0.05로 둔 두 설정)이 같은 schedule을 냄 | 9.14 decision 2가 `c2-p2a`를 판정 파일로 두되 caveat를 deadline-class chain 기준으로 다시 씀 |
| J2 | `c1-backup`의 borg가 혼자 돌아도 60 s 파일 안에 끝나지 못함(132.2 s), turnaround가 항상 잘림 | 9.10 D17: 일괄 작업은 측정된 전체를 돌리고 파일이 그 길이에 맞춰 늘어남 |
| H1 | `c7-meeting`/`c7-media`의 "fixed도 동률" 진술 | 9.14 decision 2: `c7-meeting` 판정 집합 재진입, `c7-media`는 보고 전용 |
| H2 | `c1-backup`의 `bulk` turnaround가 no-headroom 목록에서 빠짐 | 9.14 decision 6이 no-headroom 머리말을 다시 씀 |
| T1 | "키 입력 task는 slice가 끝나기 전에 막힌다": 실제로는 편집기 burst의 95 % 이상이 10 ms 이상 | `desktop-interactive` 대체(9.5) |
| T2 | borg의 RUN/SLEEP 진술 | `file-backup`으로 측정(9.7), 그 뒤 timeline에서 Déjà Dup로 바뀜(9.10) |
| S1 | 831 µs "frame slack"이 행동 단계가 아님 | 9.14 decision 9가 boot-default sweep의 점마다 이유를 다시 적음 |
| G1 | guard의 `tick_count` chain 검사가 `c2-p2a`/`c2-p2b`에서 구조적으로 실패해 RQ0 판정을 `invalid`로 만듦 | 9.14 decision 1: chain guard가 소비된 tick을 tail iteration에 대고 셈 |
| D1 | "모든 oversubscribed -single 파일은 1.00–1.50에 든다": 열 중 넷이 벗어남 | 9.14 decision 4: demand window가 gate에서 은퇴 |
| D2 | "일괄 작업은 끝나도록 크기를 맞췄다" | 9.10 D17 |

heads-up memo는 이 감사의 요점을 팀에게 이렇게 전했습니다. "focused editor가 CPU를 약 50% 쓰고 burst의 95% 안팎이 10 ms slice보다 길어요", "guard `tick_count`의 chain check가 c2-p2a·c2-p2b에서 구조적으로 fail해요", "c1-backup의 borg는 혼자 돌아도 60 s 안에 못 끝나서 turnaround가 항상 censored예요."

## 4.8 이 검증이 남긴 방법

2026-09-13 검증의 결과물 가운데 가장 오래 남은 것은 개별 판정보다 **방법**입니다. 그 뒤의 모든 연구 조각이 같은 모양을 따랐습니다.

- 주제를 중립적으로 만들어 저장소의 숫자를 감춘다(`topics.md` → 각 조각의 `search/input.md`).
- 사본을 내려받아 SHA-256과 함께 기록한다(각 조각의 `sources/`, gitignored).
- 원문 구절을 위치와 함께 적는다(각 조각의 `search/S1–S4`).
- 판정 어휘를 고정한다(scope card가 그대로 씀). 9.11의 scope card는 여기에 `NOT READ`("an item 9.1 never read against its source")를 더했습니다. 9.1의 주장 목록이 `docs/memos/`, `harness/`, `docs/harness/`를 건너뛰었기 때문입니다.

---

# 5장 · 검증을 저장하고 도구를 고치다: 9.1과 9.3

이 장은 "2026-09-13 검증의 결과물은 어디에 어떻게 남았고, 측정 도구의 결함은 어떻게 고쳤는가"라는 질문에 답합니다. Phase 9 spec decision 6은 연구 조각을 시작하기 전에 이 두 일을 먼저 하도록 정했습니다. 연구 조각이 검증 기록에서 할 일 목록을 뽑아야 하고, 고친 도구로 다시 재야 하기 때문입니다. 실행 순서는 TODO에 "9.1 ∥ 9.2 ∥ 9.3 first → 9.4–9.12 in parallel, after 9.1 and 9.3"로 적혀 있습니다.

## 5.1 9.1: 검증 기록을 저장소에 남기기

9.1의 spec(`_dev/docs/spec/jioh/task-9.1-verification-records.md`)은 phase spec이 남긴 열린 자리("The format and location of the verification records, and whether source copies are kept")를 여섯 결정으로 채웠습니다.

1. **위치.** 기록은 `_dev/research/jioh/2026-09-13-verification/`에 둡니다. 기록된 이유: "`_dev/research/jioh/` is the space for research files, and later research gets its own dated sibling folders." 연구 파일의 자리가 이미 있고, 나중 연구는 날짜를 붙인 형제 폴더를 갖는다는 것입니다. 실제로 9.3의 재분석은 `2026-09-13-meas-reanalysis/`라는 형제 폴더에 들어갔습니다.
2. **커밋하는 것.** 텍스트 기록과 감사 스크립트, 그 스크립트의 텍스트 출력과 작업 데이터.
3. **로컬에만 두는 것.** 출처 사본(PDF, 저장소 clone 등)과 원자료 측정 데이터는 같은 폴더 안에 두되 gitignore합니다. 기록된 이유는 없습니다.
4. **names:2 artifact.** 단 하나의 예외로, `meas-ci:names:2`(Actions run 34466009254)의 artifact 사본은 기록과 함께 커밋합니다. 이 run의 artifact는 어떤 release에도 없었고 2026-12-09에 만료되기 때문입니다(이 만료 날짜는 phase spec decision 6에 적혀 있습니다). 영구 보존 장소는 9.3에 맡겼습니다.
5. **경로 외에는 고치지 않고 옮긴다.** 2026-09-13 세션의 임시 폴더를 가리키던 경로만 새 폴더의 경로로 바꾸고, "passages, locators, verdicts and the known input errors that the comparisons already correct stay as they were." 비교 단계에서 이미 바로잡은 입력 오류까지 그대로 둡니다. 기록은 기록이기 때문입니다.
6. **색인.** 폴더에 짧은 색인을 둡니다. 커밋된 기록마다 무엇을 다루는지, gitignore된 로컬 폴더마다 어디서 왔는지. 그것이 폴더의 `README.md`이며, 4.1절의 구조도는 그 README를 따른 것입니다.

> **코드로.** 폴더에는 기록 문서(`claims.md`, `topics.md`, `bib.md`, `inputs/`, `reads/`, `compare/`, `meas-report.md`, `compiled-numbers-report.md`)와 함께 compile된 숫자 감사의 스크립트들(`analyze.py`, `extra.py`, `deliverable.py`, `pairs.py`, `mlfq_media.py`, `misc_checks.py`, `dump.py`)과 출력(`analysis.txt`, `single.txt`, `single_f.txt`, `native_f.txt`)이 있습니다. README는 "The scripts read the repository at its absolute path on the home machine"이라고 적습니다. 즉 이 스크립트들은 다른 기계에서 그대로 돌지 않습니다. `r01_xsim.py`와 `xsim.py`는 interbench의 `periodic_schedule()`과 `emulate_x()`를 이상적인 기계에서 흉내 낸 모델이고, R01이 그것을 인용합니다. 로컬 전용(gitignored)은 `sources/`(읽은 원본 사본), `meas/release/`(release `meas-ci-2026-08-28`의 zip 넷), 그것을 푼 폴더들, Linux v6.17의 `fs/proc/array.c`와 GNU tar의 `create.c`입니다.

## 5.2 9.3: 측정 도구를 고치고 한 번만 다시 분석하기

9.3의 spec(`_dev/docs/spec/jioh/task-9.3-measurement-tools.md`)은 측정 감사의 결함(`meas-report.md`의 #1–#16)을 다룹니다. 일곱 결정의 요지는 이렇습니다.

**결정 1, names:2를 release에.** names:2 artifact를 release `meas-ci-2026-08-28`의 asset으로 더하고, 같은 편집에서 release의 제목과 설명을 바로잡습니다. 요약은 cli:1이 아니라 cli:3에서 나왔고, names:2가 더해졌으며, cli:1은 `system-daemon`이 인용한다는 것. "Publishing is confirmed with 인지오 first." 공개 release를 바꾸는 일이므로 먼저 인지오의 확인을 받습니다. 지금 이 release의 제목은 "meas-ci raw data: cli:3, gui:2, names:1, names:2"입니다(`gh release list`로 확인).

**결정 2, 고치는 결함.** 기준은 "Where a tool reports a wrong number for what actually ran, it is fixed", 곧 실제로 돈 것에 대해 틀린 숫자를 보고하는 도구는 고칩니다.

| 도구 | 결함 | 고친 내용 |
|---|---|---|
| `proc_sampler.py` | #3 voluntary context switch를 main thread만 셈 | `--ctxt`일 때 `/proc/<pid>/task/<tid>/status`에서 스레드마다 `tctxt` {tid: [voluntary, nonvoluntary]}를 함께 기록; `analyze.py`가 있으면 스레드별 증분을 합산 |
| `verify_names.py` | #14 검증 등급 논리와 15자 comm 잘림 | `runtime` 등급은 카탈로그 이름 자체가 관찰될 때만(comm이 15자로 자른 이름과 같거나 argv0의 basename이 이름과 같음); `/sbin/`도 binary로 셈; snap stub 스크립트는 binary가 아님; binary 없는 패키지는 `package-no-binary` |
| `analyze.py` | #1 compiler 계열을 compiler child로 취급 | child는 `cc1`(`CHILD_NAMES`), 계열은 따로 보고 |
| `analyze.py` | #5 Chromium renderer 집합 | 자기 `lifecycle.log` 줄에 `--type=renderer`가 있는 pid만 |
| `analyze.py` | #9 fit이 0 값을 버림 | 0은 log fit에서 빼되 조용히 버리지 않음: `n_nonpositive`, `median_all_us`를 함께 보고 |
| `analyze.py` | #12 `dispatch_overhead`의 나눗수 | `make`의 CPU를 `make` 자신이 fork한 수로 나눔 |

**결정 3, 넘기는 결함.** 어떤 도구도 재지 않는 양 — I/O 대기(#2), wake마다의 분포(#8), 네트워크 처리량(#11) — 과, 단계 이름이 말하는 행동을 만들지 못한 workflow 설정 — Element의 renderer 없음(#4), 탭이 로드되지 않음(#6), tracker가 색인하지 않음(#7), `tar -cf /dev/null`이 내용을 읽지 않음(#16) — 은 여기서 고치지 않고, 현재 도구의 알려진 한계로 기록해 연구 조각에 넘깁니다. 이유는 결정의 구분 자체에 있습니다. 고칠 수 있는 것은 "계산이 틀린 것"이고, 넘기는 것은 "애초에 재지 않았거나 잘못된 것을 잰 것"이라 계산을 고쳐서는 해결되지 않습니다.

**결정 4, 한 번의 재분석, 새 CI run 없음.** "The fixed analyzer is run once on the raw data of release `meas-ci-2026-08-28`. No new measurement runs."

**결정 5, 재분석의 위치.** 출력은 `_dev/research/jioh/<date>-meas-reanalysis/`에 두며 "`dataset/` is unchanged." 고친 요약이 데이터셋에 들어가지 않는다는 뜻입니다. 데이터셋의 값은 연구 조각들이 정합니다.

**결정 6, 완료 확인.** "Every fixed number agrees with the audit's independent computation where one exists; every field no fix touches is byte-identical to the current `dataset/meas/summary.json`. The `proc_sampler.py` and `verify_names.py` fixes each pass a test on a constructed case." 고친 숫자는 감사가 독립적으로 계산한 값과 일치해야 하고, 고치지 않은 필드는 바이트까지 그대로여야 합니다. 리팩터링 후 회귀 테스트를 돌리는 것과 같은 생각입니다. 바꾸려던 것만 바뀌고 나머지는 하나도 바뀌지 않았음을 보입니다.

**결정 7, 한계 기록.** 재분석 폴더의 색인은 넘긴 한계마다 영향받는 파라미터와 담당 조각을 적습니다.

### 결과

재분석 폴더(`_dev/research/jioh/2026-09-13-meas-reanalysis/`)의 `comparison.md`는 `compare.py`가 만들며, 완료 확인이 실패하면 0이 아닌 값으로 끝납니다. 완료 확인의 결과는 두 줄입니다.

- "Untouched fields: 735 of 1083; all byte-identical."
- "Audit agreement: 78 of 78 figures agree."

그리고 값이 움직인 필드들입니다. 대표적인 것만 적습니다.

| 필드 | 고친 결함 | 전 | 후 | 비 |
|---|---|---|---|---|
| `compiler_lifetime_median_us` (중앙값) | #1 | 99,801 | 840,515 | 8.42× |
| `compiler_children` (중앙값) | #1 | 11,883 | 2,964 | 0.25× |
| `compiler_cpu_mean_us` (중앙값) | #1 | 89,997 | 358,103 | 3.98× |
| `compiler_life_mean_us` (중앙값) | #1 | 625,335 | 1,225,528 | 1.96× |
| `make_dispatch_us` (중앙값) | #12 | 234 | 474 | 2.03× |
| `fork_rate_hz` (중앙값) | #12 | 24.2 | 11.9 | 0.49× |
| `chromium/procs` | #5 | 50 | 3 | 0.06× |
| `daemons/work/p90_us` | #9 | 280 | 333 | 1.19× |

읽는 법을 하나 덧붙입니다. `compiler_children`이 11,883에서 2,964로 줄어든 것은 프로세스가 줄었다는 뜻이 아니라, "child"를 cc1 하나로 정의하니 cc1의 개수가 그만큼이라는 뜻입니다. 같은 build에서 compiler 계열 프로세스의 총수는 별도 필드 `compiler_family_exits`로 11,883(11,835–11,914)이 남았습니다. 그리고 cc1 하나의 CPU는 약 4배, 수명은 약 8배로 커졌습니다. 1장과 4장에서 본 "cc1 하나의 CPU가 약 4배 작게 잡혔다"가 숫자로 확인된 것입니다.

이 움직인 값에 기대던 archetype 파라미터는 `compiler-child`의 `cpu_burst`, `cpu_tail`, `disk_wait`, `build-orchestrator`의 `dispatch_overhead`, `system-daemon`의 `wake_burst`, 그리고 유휴 Chromium renderer에 대한 notes였습니다. 결정 5에 따라 이 값들은 데이터셋에 넣지 않았습니다. 대신 9.6(컴파일), 9.8(브라우저와 통신), 9.9(데몬과 세션)이 같은 대상을 고친 도구와 새 방법(한 CPU에 고정, 같은 CPU 모델만)으로 처음부터 다시 쟀습니다. 9.3의 재분석은 "어디가 얼마나 틀렸었나"를 보여 주는 기록이고, 데이터셋의 값은 그 뒤의 새 캠페인들에서 왔습니다.

넘겨진 한계 표(README의 "Known limitations of the current tools")는 각 한계와 그 담당 조각을 적습니다. 예를 들어 "No instrument measures I/O wait (#2)"는 9.6과 9.7, "Element starts no renderer process (#4)"는 9.8, "The tracker miner never indexes the corpus (#7)"는 9.7, 그리고 "names:1 and names:2 were produced by the pre-fix level logic"은 9.10에 넘겨졌습니다.

`dataset/meas/summary.json`은 9.3 결정 5대로 바뀌지 않았고, 데이터셋의 어떤 값도 이 파일에서 오지 않았습니다. 2026-10-10 감사가 "`dataset/meas/summary.json` orphaned pre-rebuild analysis"라고 적었고, 인지오가 2026-10-16에 지우기로 정했습니다(9.15 작업 목록 W-0784). 어떤 도구도 이 파일을 읽지 않았고(개발 이력의 비교 스크립트 하나만), 어느 manifest의 입력도 아니었습니다. 파일은 9.15의 rebuild 커밋 `37c2e233`(2026-10-16)에서 지워졌고, 그 앞의 커밋에서 읽을 수 있습니다. `dataset/README.md`의 `meas/` 줄은 이제 `names/`와 `streams/`만 적습니다(33–35행). 이 파일을 인용하는 memo들은 그 시점의 기록으로 그대로 둡니다.

## 5.3 같은 시기의 팀 소통: heads-up memo

9.2는 9.1, 9.3과 나란히 진행되었고, 그 결과가 `docs/memos/2026-09-13-dataset-rebuild-heads-up.md`(한국어, 인경민과 박이안에게)입니다. 이 memo는 검증 결과를 팀의 언어로 옮겼습니다. 측정 쪽으로는 "compiler 'child'가 … cc1 하나의 CPU가 약 4배 작게 잡혔어요. `disk_wait`은 disk 대기를 잰 값이 아니고, voluntary context switch는 main thread만 셌어요."라고 썼고, 무엇이 바뀌고(archetype 값, timeline 구성, 측정 도구, 데이터셋 위의 결정들) 무엇이 그대로인지(프로그램들의 입출력 형식)를 알렸습니다. 2026-10-08에 덧붙인 정정은 그 "그대로인 것"에 예외가 하나 생겼다는 것, 곧 모든 task 기록에 `declared_class` 필드가 생겼다는 것입니다(12.9절).

---

# 6장 · 우리가 직접 잰다: CI runner 위의 측정 캠페인

이 장은 "`meas-ci`란 무엇이고, 측정 job 하나는 무엇을 왜 하며, 그 결과가 어떻게 숫자가 되는가"라는 질문에 답합니다. 1.3절에서 본 것처럼 library 숫자의 97 % 이상이 `meas-ci`에서 왔으므로, 이 장치를 이해하는 것이 곧 데이터셋 대부분의 근거를 이해하는 것입니다.

## 6.1 `meas-ci`의 내력

**`meas-ci`**는 이 프로젝트가 GitHub Actions의 hosted runner 위에서 실제 프로그램을 돌리며 scheduler 수준의 행동을 잰 측정이고, 동시에 그 측정을 가리키는 출처 id입니다. **campaign**(캠페인)은 한 측정의 모든 반복을 묶은 단위이며, `meas-ci:<workflow>:<첫 batch를 띄운 날짜>`로 태그됩니다.

이 장치는 두 단계를 거쳐 지금 모양이 되었습니다.

**Phase 2(2026-08-28)의 첫 캠페인.** 2026-08-26의 grill D6은 "meas-ci adopted with the trust-scoping package"를 정했습니다. 원문은 "CI-runner measurement supports structural/shape claims only (fork structure, counts, lifetime shapes, periods, heartbeat rates, comm strings); machine-relative absolutes … are recorded with the runner spec and rank as 'convention informed by measurement', never desktop truth. Each workflow runs N times and reports spread. Framing: characterization of software behavior, never desktop-performance measurement." CI 측정은 구조와 모양에 대한 주장만 받치고, 기계에 따라 달라지는 절대값은 runner 사양과 함께 기록하되 "측정으로 정보를 얻은 관례" 등급으로 둔다는 것입니다. 같은 날 D8은 팀원의 실제 데스크톱에서 재는 "meas-live"를 연구에서 뺐습니다. 기록된 이유는 "No teammate Linux desktops known; a standing 'validate later' conditional would leave published results provisional"입니다. 이에 따라 task 2.6(`_dev/docs/spec/jioh/task-2.6-meas-ci.md`)이 두 보조 도구(netlink proc event로 프로세스 생성·종료를 잡는 tracer와 1 s 주기의 `/proc` sampler), "artifacts only, CI never writes to the repo", "N=5 matrix, dispatch-only", run 번호 태그(`meas-ci:<workflow>:<run>`)를 정했습니다. CLI workflow는 kernel defconfig build(`make -j8`)와 같은 소스 트리 위의 `tar`/`xz`, `rsync`, `updatedb`, `clamscan`, 그리고 kernel 소스 download를 `network-bulk` 측정으로 겸했고, GUI workflow는 Xvfb 위의 Chromium과 Element Desktop을, names workflow는 ubuntu/fedora/archlinux 컨테이너에서 프로세스 이름을 확인했습니다. 그 결과가 release `meas-ci-2026-08-28`과 `dataset/meas/summary.json`입니다(뒤의 것은 9.15가 2026-10-16에 지웠습니다, 5.2절).

**Phase 9의 다시 짓기.** 4장과 5장에서 본 감사가 이 첫 캠페인의 결함을 드러냈고, Phase 9의 연구 조각들은 측정 방법을 크게 바꿨습니다. 가장 큰 변화 넷을 순서대로 적습니다.

1. **runner의 절대값을 출처 주장으로**(9.5 D10, 2026-09-14). 위의 "convention informed by measurement" 등급을 버리고, 측정값을 "a source claim whose source is the run (`meas-ci:<workflow>:<run>`) and whose scope and population are the recorded runner spec and the pinned application version"으로 올렸습니다. 이유는 3.6절에서 본 대로입니다.
2. **CPU 하나에 고정**(9.5 follow-ups spec decision 2–3, 2026-09-16; 9.5 D21). "The observation is the application on one CPU. A measured archetype's observation is the application's process tree pinned to one CPU, matching the simulator's single lane." simulator는 CPU 하나(lane 하나)를 흉내 내는데, 4 vCPU runner에서 재면 프로그램의 스레드들이 병렬로 돌아 버리기 때문입니다(9.5 D21의 WHY가 가리키는 H1).
3. **CPU 모델 하나만**(9.6 D10–D11, 2026-09-18). machine gate로 AMD EPYC 7763이 아닌 runner는 아무것도 재지 않고 끝냅니다(6.2절).
4. **반복을 규칙이 정할 때까지**(9.6 D10–D11, 9.5 D26, D29, D30). "N=5" 대신, 모든 값이 정밀도 기준을 만족할 때까지 한 번씩 반복을 더합니다(7장). 그래서 캠페인이 여러 run에 걸치게 되었고, 태그가 run 번호에서 캠페인 날짜로 바뀌었습니다(9.5 D27).

2026-09-19에는 이 규칙들을 모든 캠페인이 공유하는 문서로 묶었습니다. `_dev/research/jioh/measurement-campaign-workflow.md`이며, 첫 줄이 "How a domain slice obtains the values its archetypes carry from a measurement on a GitHub-hosted runner: one CPU model, repeats added until the stability rule holds"입니다. 이 장과 7장은 대부분 이 문서를 풀어 쓴 것입니다.

## 6.2 무대: "이 소프트웨어, 이 기계"

workflow 문서의 첫 절 "What a measured value is"는 측정값이 무엇인지를 이렇게 정합니다.

- **This software on this machine** (9.5 D10): "one observation, pinned to one CPU of a 4-vCPU `ubuntu-24.04` runner (9.5 D21), its runner spec written into the archetype's scope."
- **One CPU model: the AMD EPYC 7763.** "A hosted runner guarantees a shape, not a processor; each job is an independent draw from several models, and one core of another model differs by a different factor per program (9.6: a Xeon Platinum 8573C ran `cc1` at 0.72× and `fixdep` at 0.50× the EPYC's time). … A job on any other model measures nothing."

무대를 구체적으로 그리면 이렇습니다.

```
 GitHub-hosted runner  (ubuntu-24.04, 4 vCPU, kernel 6.17.0-1022-azure)
 ┌──────────────────────────────────────────────────────────────────────────┐
 │  CPU 0, 1, 2  (harness CPUs)                 CPU 3  (measured CPU)        │
 │  ─────────────────────────────               ───────────────────────────  │
 │  perf sched record (전체 CPU를 기록)             측정 대상 프로그램의 process tree │
 │  taskstats listener                           (taskset으로 고정; 자식과 스레드도  │
 │  Xvfb (가상 X 서버, 1280×800)                    상속)                       │
 │  xdotool로 키 입력 재생, 스크린샷                 runner 자신의 agent 프로세스가    │
 │  page server, SMTP peer, Matrix homeserver     이 CPU를 함께 씀(scope에 명시)   │
 │  setup: 설치, 데이터 내려받기, 캐시 데우기                                         │
 └──────────────────────────────────────────────────────────────────────────┘
   CPU 모델이 AMD EPYC 7763이 아니면: machine_gate가 report에 gate=wrong-machine을 쓰고
   설치도 측정도 하기 전에 exit 0  →  "반복"이 아님
```

몇 가지 낱말을 풀어 둡니다.

- **vCPU**: 가상 머신에 할당된 가상 CPU 하나. runner는 4개를 갖습니다(`gh-hosted-runners`: "processor 4, memory 16 GB, storage (SSD) 14 GB").
- **pin(고정)**: 프로세스가 특정 CPU에서만 돌도록 제한하는 것. `taskset -c 3 <cmd>`처럼 씁니다. 자식 프로세스와 스레드는 이 제한을 물려받습니다.
- **Xvfb**: 실제 화면 없이 메모리 안에서 도는 X 서버. GUI 프로그램을 화면 없는 runner에서 띄울 수 있게 해 주지만, 화면 주사율(vsync)도 GPU도 없습니다.
- **`perf sched record`**: Linux의 `perf` 도구로 scheduler 사건(누가 언제 CPU에 올라가고 내려갔는지, 누가 누구를 깨웠는지)을 기록하는 명령. 이 캠페인들은 `-k CLOCK_MONOTONIC`으로 단조 시계를 쓰고, 기록을 `perf sched timehist`로 읽습니다.
- **taskstats**: 프로세스(정확히는 스레드)가 끝날 때 커널이 넘겨주는 회계 기록(user/system CPU, 경과 시간, 부모, comm, block I/O 지연, nice, scheduling policy 등)을 netlink로 받는 장치. `dataset/tools/meas/build/taskstats_listen.c`가 받습니다. 9.6 D3의 기록된 이유는 "Each process's CPU is observed twice, as summed run times and as exit accounting, so the instruments check each other and the tracing overhead, unquantified in any source, is bounded from the comparison"입니다. 두 장치가 같은 CPU를 서로 다른 방식으로 세므로 서로를 검산합니다.

> **왜 이렇게 정했나.** 한 CPU 모델만 받는 규칙은 9.6 D10(2026-09-18)에서 왔습니다. 9.6의 첫 다섯 반복이 EPYC 7763 네 번과 Intel Xeon Platinum 8573C 한 번에 떨어졌는데, `cc1` 프로세스당 CPU가 Xeon에서 269 ms, EPYC에서 358–392 ms였습니다. 기록은 이 차이를 "GitHub-hosted runners guarantee the shape, never the processor"라고 적고, 근거로 RunsOn의 30일 표본(같은 `ubuntu-24.04` 라벨에 Xeon 6973P-C와 Platinum 8573C가 섞이고 Passmark 단일 스레드 중앙값이 26 % 차이)을 듭니다. EPYC 7763을 고른 이유는 "the most frequent model in the project's recorded draws: 26 of 56 jobs"입니다. 이 선택이 문헌의 권고를 거스른다는 것도 기록되어 있습니다. `maricq-osdi18`은 공유 환경에서 "run many more repetitions, run on many different VMs and at different times"를 권하는데, 이 프로젝트는 비교 가능성을 위해 한 모델을 붙잡았고, 그래서 "every value is one CPU model's over one period, a stated limitation of the library's precision"이라고 적었습니다.

> **코드로.** `dataset/tools/meas/machine_gate.sh`는 `/proc/cpuinfo`의 첫 `model name`을 읽어 원하는 부분 문자열(`EPYC 7763`)을 포함하는지 봅니다. 각 family의 `run.sh`는 `runner_spec.py > spec.json` 직후 이것을 source해, 다른 모델이면 `gate=wrong-machine`과 `machine.model`을 report에 쓰고 exit 0으로 끝냅니다. job이 "실패"가 아니라 "성공적으로 아무것도 안 함"으로 끝나는 것이 요점입니다. `dataset/tools/meas/pin.sh`는 측정 대상을 마지막 CPU(`MEAS_CPU`)에, harness를 나머지(`MEAS_HARNESS_CPUS`)에 고정하는 함수(`pin_load`, `pin_harness`, `pin_self_harness`)를 줍니다.

## 6.3 workflow와 trigger 파일

측정 job은 `.github/workflows/meas-*.yml`로 정의되며, 각 workflow는 대응하는 trigger 파일이 바뀌는 push로 시작됩니다. workflow 머리 주석이 설명하듯 "Dispatch is unavailable off the default branch, so a push that changes this file starts the runs it names"이기 때문입니다(Phase 9 작업은 `jioh/dataset-rebuild` 브랜치에서 했습니다).

| workflow | trigger 파일 | 무엇을 재나 | 처음 쓴 조각 |
|---|---|---|---|
| `meas-interactive.yml` | `.github/campaign.json` | 상호작용 프로그램(LibreOffice Writer, VS Code, Thunderbird, Chrome, GIMP, Kdenlive) | 9.5 |
| `meas-playback.yml` | `.github/campaign.json` | 재생과 통화(mpv 비디오, mpv 오디오, WebRTC 통화) | 9.5 |
| `meas-build.yml` | `.github/campaign-build.json` | kernel build와 일괄 프로그램 | 9.6 |
| `meas-background.yml` | `.github/campaign-background.json` | borg, 7-Zip, SteamCMD; 9.10의 upgrade, dkms, tracker, mnist, handbrake, kdenlive export, dejadup | 9.7, 9.10 |
| `meas-desktop.yml` | `.github/campaign-desktop.json` | 숨은/보이는 Chrome renderer, Element, Steam client; 9.10의 chrome-tabs, launch | 9.8, 9.10 |
| `meas-session.yml` | `.github/campaign-session.json` | 유휴 Ubuntu 데스크톱 세션의 GNOME Shell, PipeWire, systemd, dbus | 9.9 |
| `meas-costs.yml` | `.github/campaign-costs.json` | 커널 context switch 비용, LLM 구조화 응답 지연(archetype 아님) | 9.12 |
| `meas-long-probe.yml` | `.github/campaign-long-probe.json` | 긴 단계 탐침(launch 작업이 끝나는가, 되풀이되는가) | 9.5 |
| `meas-probe.yml` | (push) | runner가 무엇을 돌리고 볼 수 있는가 — "Never a measurement" | 9.5 |
| `meas-names.yml` | (dispatch) | 세 배포판 컨테이너에서 프로세스 이름 확인 | Phase 2 |
| `meas-sched.yml` | (push) | runner 커널의 scheduler 설정값 읽기 — "A configuration read, not a workload measurement" | 9.11 |

trigger 파일은 실행할 프로그램, 반복 번호(모든 프로그램에 같은 목록이거나 프로그램별 목록), CPU 모델, 모드(`dry`, `probe`, `full` 등)를 담습니다. 예를 들어 지금 `campaign-background.json`은 `"mode": "full"`, `"cpu_model": "EPYC 7763"`, `"apps": ["dejadup"]`, `"repeats": {"dejadup": [27, 28]}`, `"attempt": 196`입니다. workflow 문서는 "nothing else [starts runs]"라고 못박고, "The workflows have no concurrency group: a new push never cancels a run in flight"라고 덧붙입니다. 새 push가 진행 중인 측정을 취소하지 않습니다.

웹 개발의 CI matrix와 같은 구조입니다. plan job이 trigger 파일을 읽어 `(app, repeat)` 조합의 matrix를 만들고, run job이 조합마다 runner 하나를 받아 `run.sh <app> <repeat> <mode>`를 실행하고, 결과 폴더를 `meas-<family>-<app>-r<k>-<mode>`라는 이름의 artifact로 올립니다. 조합 하나가 runner 하나이므로 각 반복은 **새 runner 위의 독립된 job**입니다. 이것이 7장의 "반복의 단위"가 됩니다.

## 6.4 도구 상자 `dataset/tools/meas/`

`dataset/tools/meas/README.md`가 이 폴더의 지도입니다. 하위 폴더와 맨 위 도구마다 그 캠페인 family, 단계(run, analysis, pool, fold-in), 입구를 적고, 각 도구가 무엇을 하는지는 그 도구의 docstring이나 머리 주석에 맡깁니다(이 권을 쓰며 각 파일 머리를 읽었습니다). 공용 도구와 family 폴더를 나눠 정리합니다.

| 파일/폴더 | 역할 |
|---|---|
| `machine_gate.sh`, `pin.sh`, `phase.sh` | CPU 모델 확인, CPU 고정, 단계의 시작과 끝 기록 |
| `runner_spec.py` | runner 사양을 `spec.json`으로 기록. docstring: "Record the runner spec: a measured value is a source claim scoped to the runner this record describes, not a downgrade to convention (9.5 D10, D26)." 측정값은 runner로 범위를 정한 출처 주장입니다(6.1절) |
| `stability.py` | 모든 캠페인이 공유하는 stability rule(7장): `TOLERANCE = 0.05`, t 배수 `t975`, `stability`, `ratio_stability` |
| `stopping.py` | 멈춤 규칙을 관찰된 퍼짐에서 모의실험(9.5 D88) |
| `distribution.py` | 측정 분포를 표로 만드는 방법: 열 개 분위수 p1…p99.9, 최솟값과 최댓값, 열한 구간의 평균 |
| `burstiness.py` | 측정 wake 흐름과 compile된 흐름의 몰림 정도(dispersion) 비교 |
| `windows.py` | 단계를 시간 창으로 나눠 읽기 |
| `control.py`, `control_report.py` | 추적 없는 대조군(untraced control) |
| `replay_fold_in.py` | release 원자료에서 trace-replay 흐름 만들기(`dataset/replay/`); `--check` |
| `batch_fold_in.py` | 컴파일과 백그라운드 항목의 batch-loop 표를 pooled record에서 `archetypes.yaml`로; `--check` |
| `verify_names.py`, `proc_sampler.py`, `analyze.py` | Phase 2의 이름 검증, `/proc` sampler, 분석기(9.3이 고침) |
| `campaign/` | 9.5 family: `run.sh`, `analyze.py`, `pool.py`, `fold_in.py`, `control.py`, `build_windows.py`, `slices.py`, `wake_check.py` 등 |
| `build/` | 9.6: `run.sh`, `analyze.py`, `pool.py`, `shapes.py`, `taskstats_listen.c`, `train.py`, `clamav_db.sh` |
| `background/` | 9.7, 9.10: `run.sh`, `analyze.py`, `pool.py`, `nettrace.py`, `fileset.py`, `hippocamp.py`, `kdenlive_export.py`, `dejadup_*.py`, `upgrade-layer.txt`, `inputs.json` |
| `desktop/` | 9.8, 9.10: `run.sh`, `analyze.py`, `pool.py`, `fold_in.py`, `tabs.py`, `launch*.py`, `within_run.py` 등 |
| `session/` | 9.9: `run.sh`, `analyze.py`, `pool.py`, `fold_in.py`, `causes.py`, `census.py`, `upgrade_probe.py` 등 |
| `costs/`, `llm/` | 9.12의 costs 캠페인 |
| `loop/` | 개발 기계에서 캠페인을 돌리는 반복 도구: `launch.py`, `status.py`, `pool_runs.py`, `watch.py`, `cut_windows.sh` |
| `probe/` | runner 탐침과 입력 재생: `replay_stream.py`, `swell_streams.py`, `aalto_streams.py`, `appdefs.sh`, `feed.html`, `webrtc-loopback.html` 등 |
| `sched/` | 9.11: `classes.py`(스레드마다 scheduling policy와 nice 기록), `tunables.sh` |

이 도구들은 compile이 읽지 않습니다. 데이터셋을 build하는 데는 필요 없고, 측정을 다시 하거나 pooled record에서 값을 다시 만들 때 필요합니다. `dataset/README.md`의 도구 지도는 `tools/meas/`를 "the measurement campaigns' tooling, one folder per campaign family — map: tools/meas/README.md"로 적습니다.

이 README는 9.15에서 생겼습니다. 이 권을 처음 쓸 때(2026-10-14)는 폴더의 도구를 한 곳에서 설명하는 문서가 없었고, 유일한 색인인 workflow 문서의 "Tooling" 절은 `session/`, `sched/`, `costs/`, `llm/`, `batch_fold_in.py`, `replay_fold_in.py`, `verify_names.py`를 이름 짓지 않았습니다. 인지오가 2026-10-16에 README를 쓰기로 정했고(9.15 작업 목록 W-0751), README는 docstring이 말하지 않는 것을 주장하지 않는 지도로 쓰였습니다.

## 6.5 job 하나가 하는 일

family마다 세부는 다르지만, job 하나의 뼈대는 같습니다. `background/run.sh`의 머리 주석이 가장 간결하게 적습니다. "Every measured phase is one command pinned to the measured CPU (pin.sh, phase.sh MEAS_PIN=load), observed over the whole phase from the harness CPUs by `perf sched record -a` — with the exec rows that name each process's program — and a taskstats listener registered on the measured CPU. … Setup — the set fetched, extracted and verified, warmed, changed and restored, the older build staged — runs on the harness CPUs."

```
 1. spec.json 기록 (runner_spec.py)
 2. machine gate  ── 다른 모델 → gate=wrong-machine, exit 0 (끝)
 3. 설치와 준비 (harness CPU)       예: apt 패키지, 입력 데이터 내려받고 SHA-256 확인, 캐시 데우기
 4. 계측기 준비                      taskstats listener 컴파일, kernel.task_delayacct=1 등
 5. (settle)                       launch 작업이 끝날 때까지 기다림 — 프로그램마다 설계값
 6. 측정 단계들 (measured CPU)        phase.sh가 경계를 기록; perf sched record가 전체를 기록
 7. 결과 정리, report.json            반환 코드, 버전, 확인값
 8. artifact 업로드                  meas-<family>-<app>-r<k>-<mode>
```

**settle**(가라앉히기)은 프로그램을 띄운 뒤 측정을 시작하기 전까지 기다리는 시간입니다. workflow 문서는 "Steady behaviour starts after launch"라고 정하고, 이유를 9.5 D34에서 가져옵니다. 30 s settle로는 Chrome, Thunderbird, WebRTC 통화, VS Code가 launch나 ramp-up 작업을 측정 단계 안으로 가져왔고, 그 작업이 모든 반복에서 같은 지점에 "up to 20 times the steady CPU"로 나타났습니다. 그래서 settle은 프로그램마다 trace를 보고 정하며 design 꼬리표를 답니다. trace만으로 launch 작업과 되풀이되는 행동을 구분할 수 없으면 먼저 **long-phase probe**(긴 단계 탐침: settle과 아주 긴 측정 단계 하나만 돌려 보는 run, 반복이 아님)를 돌립니다(9.5 D35). 일화가 멈추면 settle을 그만큼 잡고, 되풀이되면 단계를 늘려 그 일화를 담습니다. 그 결과 `measurement-overview.md` §4가 적은 값들이 나왔습니다: "Chrome settles 420 s, Thunderbird 390 s, the call 210 s, the Steam client 900 s; VS Code's idle phase is read from 200 s past its start."

## 6.6 trace가 숫자가 되는 방법: wake, run, gap, component, table

측정 단계의 trace는 "어느 스레드가 언제 CPU에 올라가 얼마나 있다 내려갔고, 누가 깨웠는가"의 긴 목록입니다. 이것을 archetype이 담는 숫자로 바꾸는 정의가 workflow 문서와 `measurement-overview.md` §5에 있습니다.

- **wake**(깨어남): "A schedule-in preceded by a wakeup event for that thread since its last sleep; a resume after preemption is folded into the wake it continues." 스레드가 잠들었다가 누군가에게 깨워져 CPU에 올라가는 것이 wake 하나입니다. **schedule-in**은 스레드가 CPU를 받는 순간입니다. **preemption**(선점)은 스레드가 스스로 잠들지 않았는데 scheduler가 CPU를 빼앗아 다른 스레드에 주는 것입니다. 선점당했다가 다시 올라가는 것은 새 wake가 아니라 이전 wake의 연장으로 셉니다. 웹으로 비유하면, `await`에서 잠들었다 깨어나는 것이 wake이고, 같은 callback이 time slice 때문에 잠시 밀렸다 이어지는 것은 같은 실행의 연속입니다.
- **run**: wake 하나의 CPU 시간. 선점으로 끊긴 조각들은 합칩니다.
- **gap**: 한 component의 연속된 wake 사이 시간. 9.5 D71 이후로 gap은 component의 모든 스레드를 합친 wake 시각들 위에서 재고, 관찰 구간을 고리처럼 이어 마지막 wake의 gap이 첫 wake로 넘어가게 합니다. 그래서 "the gaps sum to the span, one per wake, so the rate a gap table implies is the rate measured." gap 표가 암시하는 wake 빈도가 측정된 빈도와 정확히 같아집니다.
- **component**: 한 프로세스 역할 안의 스레드 이름(comm) 하나(예: `gpu/Chrome_ChildIOT`, `pid1/systemd`). 9.5 D67은 "a component is identified by its process role and comm together"로 정했습니다. component는 wake 빈도가 큰 순서로 단계 wake의 95 %를 덮을 때까지 고르고, 나머지는 **residual**(나머지) 하나로 묶습니다.
- **table**(표): "the ten pooled quantiles p1 … p99.9, the sample's minimum and maximum, and the measured mean of the samples in each of the eleven intervals they bound". 열 개의 분위수(p1, p5, p10, p25, p50, p75, p90, p95, p99, p99.9), 최솟값과 최댓값, 그리고 그 열두 값이 나누는 열한 구간 각각의 실제 평균. 구간 평균을 함께 들고 다니므로 표에서 뽑은 값의 평균이 표본의 평균과 같아집니다(`distribution.py`의 docstring: "so a table's mean is the sample's mean").

entry의 종류에 따라 담는 것이 다릅니다.

- **타이핑 entry**(`office-writer`, `code-editor`, `mail-client`, `web-browser`): component들과 함께 **per-input run**(입력 하나당 run)을 담습니다. 9.5 D13의 "window rule"에 따라 "all run time of the process tree until the next input minus the idle rate", 곧 한 입력에서 다음 입력까지 process tree 전체가 쓴 CPU에서 유휴 상태의 기본 소비를 뺀 값입니다.
- **operation**: 벤치마크가 정의한 무거운 동작(GIMP의 unsharp mask, Kdenlive의 preview render, Chrome의 page load, Thunderbird의 send)은 지속 시간 표와 자기 component들을 담습니다.
- **재생과 통화 entry**: 매체의 주기마다 periodic job 하나 — 주기(`period`)와 주기당 CPU(`cycle_run`)(9.5 D75).
- **build, 일괄, 백그라운드 entry**: "runs between voluntary blocks and the block after each run", 곧 스스로 잠들기 전까지 연속으로 쓴 CPU 덩어리와, 그 뒤 잠들어 있던 시간의 표(9.6 D21, D22, D25; 9.7 D29). **voluntary block**은 스레드가 I/O나 다른 사건을 기다리며 스스로 CPU를 내려놓는 것입니다.

## 6.7 family마다 무엇을, 왜 재나

각 family의 job이 무엇을 돌리고 왜 그렇게 했는지 요점만 적습니다. 숫자와 항목별 세부는 archetype library를 다루는 2권이 다룹니다.

**interactive (9.5).** 실제 프로그램을 stock 빌드와 기본 설정으로 띄워 유휴(idle) 단계, 기록된 사람 입력을 재생하는 구동(driven) 단계, 두 번째 자극의 구동 단계(driven-alt), 그리고 operation 단계를 잽니다. 재생하는 입력은 SWELL-KW 기록입니다. 9.5 D4의 이유는 "25 participants × ~3 h, per-keystroke timestamps with the focused application, free composition, pauses retained"이고, 코드 편집 키 입력 데이터셋은 찾지 못했다는 것입니다(S3 "Not found"). 키만 재생하고 클릭과 스크롤은 빼는데(9.5 D28, D65, D72, D79), 그 이유는 첫 같은-기계 반복들에서 기록의 클릭과 드래그가 76쪽 문서 안에서 타이핑 위치를 옮겨(72–75쪽) `input_run` 퍼짐이 ±44 %가 되었기 때문입니다. 그 퍼짐은 프로그램의 것이 아니라 재생 설계의 것이었습니다. 또 입력 기록이 Windows에서 2012년에 만들어졌다는 점은 이렇게 정리됩니다. "Stimulus timing may come from any platform, the response only from Linux"(`measurement-overview.md` §4). 입력의 시각은 어느 플랫폼의 것이어도 되지만, 그 입력에 대한 프로그램의 반응은 Linux에서 잰 것만 씁니다.

**playback (9.5).** mpv로 1280×720 30 fps 비디오와 같은 파일의 오디오를 재생하고, Chrome 안에서 가짜 카메라와 마이크로 loopback WebRTC 통화를 돌립니다. 9.5 D75 이후 각 entry는 매체 주기마다 periodic job 하나로 담깁니다(예: 통화는 10 ms 오디오 프레임마다 job 하나, 주기 10.001 ms).

**build (9.6).** linux-6.6 defconfig를 warm 상태에서 `make -j8`로 빌드하는 것이 주 단계이고, cold build(`make clean`, `sync`, `vm.drop_caches=3` 후), `-j1` build(불변성 점검), DKMS(커널이 바뀔 때 외부 커널 모듈을 다시 빌드하는 장치) 모듈 빌드, 그리고 일괄 프로그램들(`clamscan`, `ffmpeg`, `HandBrakeCLI`, `python3 train.py`, tracker)이 함께 돌았습니다. `-j8`의 근거는 "design: the eight-thread desktop"(9.6 D4)입니다.

**background (9.7, 9.10).** 9.7은 borg와 7-Zip이 Matt Mahoney의 10 GB 압축 벤치마크 세트(79,431 파일)를 읽게 했고, SteamCMD가 TF2 전용 서버 depot을 121.0 Mbps로 조절한 링크(Valve의 국가별 download 속도의 바이트 가중 중앙값, `fq_codel` 큐)로 내려받게 했습니다. 9.10은 같은 workflow로 무인 업그레이드, DKMS 자동 설치, Tracker의 첫 색인, PyTorch MNIST 학습, HandBrake 변환, Kdenlive 내보내기, Déjà Dup 증분 백업을 쟀습니다. 9.10의 일곱 백그라운드 캠페인은 같은 chroot(디렉터리 하나를 새 루트 파일시스템처럼 쓰는 격리 환경)를 공유합니다. 영어 Ubuntu 24.04 설치의 기본 층(1,445 패키지, `upgrade-layer.txt`)을 Ubuntu의 snapshot 서비스에서 특정 시점의 archive로 만든 것입니다. 시점을 고정하는 이유는 "그날 설치될 업데이트"까지 재현 가능하게 하기 위해서입니다(10장).

**desktop (9.8, 9.10).** 백그라운드 탭의 숨은 Chrome renderer, 보이는 창의 renderer, 로그인한 Element Desktop(로컬 Synapse homeserver 상대), 로그아웃 상태로 창을 보인 Steam client를 쟀고, 9.10이 Chrome 다섯 탭의 renderer 개수 세기(`chrome-tabs`, perf 없음)와 열 개 프로그램의 launch 단계 기록(`launch-*`)을 더했습니다.

**session (9.9).** `ubuntu-desktop-minimal`의 GNOME 세션을 GDM 자동 로그인으로 띄우고, 사람이 없는 상태로 300 s 유휴 지연이 지나 화면이 잠기고 꺼진 "terminal idle state"에서, 네 entry의 프로세스만 측정 CPU에 두고 1,800 s를 쟀습니다. 9.9 D9의 이유는 "nobody present past the idle delay"라는 우선순위 표의 상황 정의("Nobody present, maintenance only")와 그 상태를 정하는 문서화된 메커니즘들입니다.

**costs (9.12).** archetype이 아니라 논문 본문(관련 연구와 제안서의 커널 비용, LLM 응답 지연 문장)을 위해, 데이터셋과 같은 기계에서 context switch 비용과 공정 class의 다음 task 고르기(pick) 비용, 그리고 3B와 8B 모델의 구조화 응답 지연을 쟀습니다(`meas-ci:costs:2026-10-08`). 이유는 9.12 D31에 "Literature gives switch costs only on 2007–2021 machines … nothing for the pick … The dataset's values are this machine's"로 기록되어 있습니다.

**탐침들.** `meas-probe.yml`은 캠페인을 설계하기 전에 runner가 무엇을 할 수 있는지 봅니다(perf, tracefs, uinput, 소리 장치, 각 프로그램이 Xvfb에서 뜨는지, xdotool 재생 정밀도 — p99 1.24 ms). `meas-long-probe.yml`은 settle을 정하는 긴 단계 탐침입니다. `meas-sched.yml`은 9.11 D2를 위해 runner 커널의 EEVDF(Linux의 현재 기본 공정 scheduler) base slice를 CPU 수별로 읽었습니다(release `meas-ci-sched-2026-10-07`). 그리고 9.11의 class census(release `meas-ci-probes-2026-10-07b`)는 모든 측정 대상에서 스레드마다 scheduling policy와 nice를 2 s마다 읽었습니다(12.9절).

## 6.8 이름 검증: `dataset/meas/names/`

데이터셋의 timeline은 프로세스 이름을 씁니다(인식기가 읽는 것이 이름이기 때문입니다). 그 이름이 실제 Linux에서 그 모양으로 나타나는지를 확인하는 것이 이름 검증입니다. `dataset/meas/names/`에는 두 번의 run 결과가 있습니다.

- `names/names-{ubuntu,fedora,arch}.json`: Phase 2의 `meas-ci:names:1`(run 33067225138). 이름 22개.
- `names/run-2/names-{ubuntu,fedora,arch}.json`: `meas-ci:names:2`(run 34466009254), Phase 7에서 `dkms`를 더해 이름 23개. 이 run의 artifact는 release에 없었고 9.1이 기록과 함께 커밋, 9.3이 release `meas-ci-2026-08-28`에 asset으로 더했습니다.

각 파일은 `distro`, `not_attempted`, `results`를 갖고, `results`의 이름마다 `binaries`, `level`, `observed`, `package`, `note`가 있습니다. **level**은 `runtime`(실행해서 그 이름이 실제로 관찰됨), `binary-only`(패키지에 실행 파일은 있으나 실행해 보지 않음 — 컨테이너에서 띄울 수 없는 데스크톱 데몬 등), `package-not-found` 등입니다. tree를 세어 보면 run 2의 Ubuntu 표는 `runtime` 11, `binary-only` 11, `package-not-found` 1이고, run 1의 Ubuntu 표는 `runtime` 14, `binary-only` 7, `package-not-found` 1입니다.

이 표에는 두 가지 주의가 있습니다. 첫째, 9.3 README가 적은 대로 "names:1 and names:2 were produced by the pre-fix level logic". 두 표 모두 X14의 결함(카탈로그 이름 자체를 보지 않고 `runtime`을 줌)이 고쳐지기 전의 논리로 만들어졌습니다. 둘째, 표에 있는 이름들(`clamscan`, `borg`, `tracker-miner-fs-3`, `gamescope`, `python3` 등)은 Phase 9 이전 timeline의 이름이고, 지금 timeline이 쓰는 이름(`unattended-upgr`, `tracker-miner-f`, `deja-dup`, `python`, `melt-7` 등)의 상당수는 이 표에 없습니다. 지금 이름들의 근거는 각 측정 캠페인의 trace에 실제로 찍힌 comm입니다. 예를 들어 9.20의 생성 층에서 tier 3 이름 `melt-7`과 `duplicity`는 각각 `meas-ci:background:2026-10-03c`와 `meas-ci:background:2026-10-04`의 프로세스 이름 조사에 기댑니다(`grids.yaml`의 `source` 값과 TODO 9.16 줄).

지금 timeline이 쓰는 이름을 고친 `verify_names.py`로 다시 확인한 run은 없고, 하지 않습니다. 인지오가 2026-10-16에 이름의 근거를 이렇게 정했습니다(9.15 작업 목록 W-0738). 이름은 9.10 D25에 기댑니다. task의 이름은 그 process의 kernel `comm`이고, 캠페인이 돌린 프로그램이면 캠페인이 관찰한 `comm`, 아니면 kernel의 규칙으로 끌어내고 캠페인이나 `meas-ci:names:2`가 보여 주는 곳에서 확인한 것입니다. Phase 2와 Phase 7의 이름 표(`dataset/meas/names/`)는 이력이고, 어떤 도구도 읽지 않습니다. compile된 core 파일이 담은 이름 44개는 네 종류입니다. 캠페인이 추적한 `comm`(대부분; 학습 run의 `python`은 관찰된 `comm`), `lavd-ossna24` 슬라이드 16장의 게임 chain 스레드 이름(`wineserver`는 compiler가 붙임), tier 4와 tier 5의 이름(design), 그리고 일부러 붙인 가짜 이름(`c6-spoof`의 `chrome`, `c6-alias`의 `baloo_file`과 `tracker-miner-f`; design)입니다(`dataset/README.md`의 "A task's name is its kernel `comm`" 규칙).

## 6.9 입력 창: `dataset/meas/streams/`

`dataset/meas/streams/`는 측정 캠페인이 재생한 입력 기록의 **창(window)**들입니다. wake 흐름이 아니라 사람 입력의 흐름입니다. 반복 하나가 창 하나를 재생합니다.

- `word-r1` … `word-r57`(56개; `word-r43` 없음), `outlook-r1` … `outlook-r8`, `ie-r1` … `ie-r38`: SWELL-KW의 Word, Outlook, Internet Explorer 기록에서 자른 600 s 창들.
- `aalto-r1` … `aalto-r78`: 136M Keystrokes 데이터에서 자른 창들(자극 민감도 점검용, 8.3절).
- `windows.json`, `aalto-windows.json`: 창마다 출처 파일, 사건 수, 키 수, 포인터 수, 길이를 적은 색인.

`windows.json`의 `rule`은 "D12: c1 for word and ie, c2+c3 for outlook; participant order; 2000 ms per segment/file boundary; 600 s windows"입니다. Word와 IE는 조건 c1(중립)에서, Outlook은 조건 c2와 c3(방해 조건)에서 자르고(SWELL-KW의 Outlook 키 입력은 방해 조건에만 있기 때문, 9.5 D12), 참가자 순서대로 이어 붙이며, 파일 경계마다 2,000 ms를 두고, 600 s씩 자릅니다. 각 줄은 `{gap_ms, seg, kind, x, y, button, wheel}`입니다. `word-r43`이 없는 것은 workflow 문서의 "An empty window is not committed" 때문이며, 9.5 D99가 "the recording holds 57 windows, 56 with input"이라고 적은 것과 맞습니다.

이 창들과 별개로 `dataset/stimulus/`에는 compile이 실제로 쓰는 자극 흐름(`swell-word-c1.jsonl` 등)이 있습니다. 측정이 재생한 창(`meas/streams/`)과 simulator의 workload가 재생하는 흐름(`stimulus/`)은 같은 SWELL-KW에서 나왔지만 다른 파일이고, 앞의 것은 측정의 입력, 뒤의 것은 compile의 입력입니다.

---

# 7장 · 몇 번 재야 충분한가: stability rule과 멈춤 규칙

이 장은 "측정을 몇 번 반복해야 그 평균을 믿을 수 있고, 언제 멈추며, 멈춘다는 행위 자체가 무엇을 왜곡하는가"라는 질문에 답합니다. 이 질문이 있는 이유는, 같은 프로그램을 같은 runner 모델에서 돌려도 결과가 매번 조금씩 다르기 때문입니다. 반복을 많이 하면 평균이 안정되지만, 반복은 runner 시간을 씁니다(한 반복에 수 분에서 수 시간). 그래서 "충분함"의 기준이 필요하고, 그 기준이 **stability rule**입니다.

## 7.1 반복, landing, 캠페인

- **repeat(반복)**: "one full job on a fresh runner"(`measurement-overview.md` §3). 새 runner 위에서 측정 절차 전체를 한 번 돈 것. 같은 job 안에서 측정 단계를 여러 번 도는 것은 반복이 아닙니다.
- **landing(착지)**: 반복 번호 하나를 띄운 job이 올바른 CPU 모델을 뽑아 측정을 마치고 artifact를 올린 것. machine gate에 걸린 job은 "gated"이고 반복이 아닙니다. 한 번호가 여러 번 착지하면(예: 한 push가 두 run을 띄운 경우) 9.8 D24에 따라 "every landing of it … is pooled once per landing, keyed `<index>@<run id>`"입니다.
- **pool(묶음)**: 같은 캠페인의 모든 유효한 반복을 모아 값을 계산하는 것. 결과가 **pooled record**(기계가 읽는 `pooled.json`과 사람이 읽는 `results.md`)이며 각 조각의 `campaign/` 폴더에 들어갑니다.

반복의 단위를 "새 runner 위의 job 하나"로 잡은 이유는 workflow 문서에 `kalibera-ismm13`의 인용으로 적혀 있습니다. "repetition 'must be done at the highest level that has random variation to avoid bias' (§3) — here the job, one full protocol on a fresh runner." 무작위 변동이 들어오는 가장 높은 층에서 반복해야 치우침이 없다는 것입니다. runner마다 디스크, 이웃 가상 머신, 커널의 상태가 다르므로, 같은 runner 안에서 단계를 여러 번 도는 것으로는 그 변동을 보지 못합니다.

## 7.2 규칙의 구성

stability rule은 한 문장으로 이렇습니다. "for every value the fold-in carries — a rate or share by its per-repeat values, a table by its mean as the table carries it, count-weighted over the repeats (the ratio estimator's half-width, `cochran-st77`) — the 95 % confidence half-width is at most 5 % of it or 1 µs, whichever is larger, over at least five same-machine repeats"(`measurement-campaign-record.md`의 Campaigns 절). 여기서 **fold-in**은 pooled record의 값을 `archetypes.yaml`에 써 넣는 단계입니다. 구성 요소를 표로 풀면 다음과 같습니다(`measurement-overview.md` §6의 표를 바탕으로, 근거 열은 workflow 문서의 문장).

| 요소 | 내용 | 근거 |
|---|---|---|
| CPU 모델 하나 | AMD EPYC 7763만. 다른 모델을 뽑은 job은 약 20 s 안에, 설치 전에 멈추며 반복이 아님 | `maricq-osdi18`; 9.6의 측정(Xeon이 `cc1` 0.72×, `fixdep` 0.50×) |
| 반복의 층 | 구간은 독립된 반복들 위에서, 한 run 안의 표본들 위에서는 절대 아님 | `kalibera-ismm13` §3, §9.3 |
| 어떤 값을 | fold-in이 담는 모든 값. component마다 따로, residual 포함. component들의 평균으로 뭉뚱그리지 않음 | 설계(9.5 D30, 9.6 D23, 9.8 D17) |
| 기준 | 95 % t 반폭이 평균의 5 % 이하, 시간 값이면 1 µs가 더 클 때 1 µs | 5 %는 설계: 보고하는 가장 작은 효과의 절반. 1 µs는 trace의 해상도 |
| 최소 | 같은 기계 반복 최소 다섯 | `kalibera-ismm13` §11 |
| 추가와 멈춤 | 한 번씩(또는 pool의 예측치까지 한 batch) 더하며, 매번 규칙을 읽고, 모든 값이 통과하면 멈춤. 상한 없음 | `kalibera-ismm13` §11; `georges-oopsla07` §4 |
| 멈춤이 보장하는 것 | 처음 통과한 지점에서 멈추면 그때의 반폭은 낙관적 | `chow-aoms65` |

몇 낱말을 풀어 둡니다.

- **95 % 신뢰구간의 반폭(half-width)**: 반복들의 평균 m, 표준편차 s, 반복 수 k가 있을 때 반폭은 t(k−1)·s/√k이고, 구간은 m ± 반폭입니다. 이 프로젝트는 반폭을 평균에 대한 비율로 읽습니다(예: ±3.78 %).
- **t 배수**: 반복 수가 적을 때는 정규분포의 1.96 대신 Student t 분포의 97.5 % 점을 씁니다. `stability.py`의 `t975(k)`가 그 값을 k−1 자유도로 계산합니다(9.6 D35 이후 20회가 넘는 반복에서도 정확히 계산).
- **tolerance(허용 오차)**: 반폭이 넘지 말아야 할 선, 여기서는 5 %.

> **왜 이렇게 정했나.** 5 %라는 선은 "this project's design"이라고 workflow 문서가 분명히 적습니다. 방법의 출처인 Kalibera와 Jones는 허용 오차를 처방하지 않습니다. 그들의 "within 1%, 1.5%, 2.5% or 5% of the mean"(§11)은 자기 플랫폼의 DaCapo 결과 표의 열일 뿐이고, §12는 "it is essential that experimenters do not use our dimensioning results at face value but apply our method to their systems"라고 말합니다. 그래서 이 프로젝트는 5 %에 자기 근거를 붙였습니다. "The 5 % is half the smallest effect a slice reports as a comparison of carried values (9.6, half of the 10 % `-j8` against `-j1` difference)." 9.6이 보고하는 비교 가운데 가장 작은 효과(`-j8`과 `-j1` build의 약 10 % 차이)의 절반이면, 그 효과는 측정 오차에 묻히지 않는다는 생각입니다. 처음(9.5 D26, 2026-09-18)에는 9.5의 자극 민감도 점검의 +10 %가 근거였는데, 9.5 D81(2026-09-27)이 그 점검을 자기 구간으로 읽기로 하면서 허용 오차의 근거에서 빠졌습니다. 1 µs 바닥(floor)의 근거는 "the trace's resolution, `perf sched timehist` printing whole microseconds"입니다. 측정 장치가 마이크로초 단위로만 찍으므로, 그보다 작은 차이는 볼 수 없습니다. 몇 µs짜리 값(예: `file-archiver`의 block per run)은 5 %가 아니라 이 바닥으로 통과합니다.

## 7.3 비율과 표를 서로 다르게 읽는 이유

규칙은 값의 종류에 따라 반폭을 다르게 계산합니다.

**비율이나 몫(rate, share)은 반복별 값으로.** 예: 초당 wake 수, CPU 점유율. 반복마다 값 하나가 나오므로, 그 k개 값의 평균과 표준편차로 반폭을 냅니다. 근거는 Kalibera의 §9.3입니다. "the multi-level interval is the same as if we had used a single-level interval for the means of all data from all but the highest level."

**표(table)는 표가 담는 평균으로, 개수 가중으로.** 예: gap 표, run 표, 입력당 run 표. 9.5 D78(2026-09-26) 이후 표는 "every repeat's samples pooled, so its mean is their sum over their count"로 읽습니다. 표는 모든 반복의 표본을 한데 모은 것이므로, 표가 담는 평균은 반복별 평균의 평균이 아니라 전체 합을 전체 개수로 나눈 값입니다. 그러면 표본이 많은 반복이 평균에 더 큰 몫을 갖습니다. 이 평균의 불확실성은 반복을 cluster(묶음)로 보는 표본조사의 비율 추정량(ratio estimator)으로 계산합니다. 근거는 `cochran-st77` §9A.1의 "a ratio estimate in which Mᵢ is taken as the auxiliary variate xᵢ"와 식 (6.13)이며, 유한 모집단 보정 f = 0(반복이 끝없는 job 모집단에서 뽑혔다고 봄)과 정규 대신 t 배수를 쓰는 것은 이 프로젝트의 선택입니다.

비유를 들면 이렇습니다. 여러 날의 서버 로그에서 "요청당 평균 지연"을 낼 때, 날마다의 평균 지연을 평균하면 요청이 적은 날이 과대 대표됩니다. 전체 요청의 지연 합을 전체 요청 수로 나누는 것이 "표가 담는 평균"이고, 그 불확실성은 "날"을 단위로 퍼짐을 재야 합니다. 같은 날의 요청들은 서로 독립이 아니기 때문입니다.

> **코드로.** `stability.py`의 `stability(values_by_repeat, abs_floor, min_k, keep_zero)`가 비율과 몫을, `ratio_stability`가 표를 처리합니다. 각 family의 `pool.py`가 이 함수들을 불러 캠페인의 목록 전체에 규칙을 적용하고, 값마다 "지금의 퍼짐이라면 몇 번의 반복에서 통과할지"(projection, 예측치)를 함께 출력합니다. 10장의 `package-upgrade` 결과표에 이 예측치(`needed at this spread`)가 보입니다.

## 7.4 첫 실행 전에 정하는 것, 반복을 더하는 방법

workflow 문서의 "Before the first run" 절은 캠페인을 띄우기 전에 조각의 method 문서와 changelog에 적어 둘 네 가지를 정합니다.

1. **목록(the list)**: fold-in이 담을 모든 값.
2. **그 조각이 보고하는 가장 작은 효과**: 허용 오차의 근거.
3. **첫 batch와 그 근거**: 최소 다섯. 9.6은 여섯(앞선 같은-모델 반복들의 퍼짐에서 모든 중앙값이 처음 통과하는 수), 9.5는 창 1–5.
4. **반복이 무엇인가**: 같은 작업(빌드, 스크립트 상호작용, 재생)이면 다음 반복 번호, 기록된 입력이 이끄는 작업이면 다음 입력 창. 입력의 한계와 거기서 무슨 일이 일어나는지도 미리 적습니다.

결과를 보기 전에 무엇을 재고 무엇으로 판단할지 적어 두는 것은 실험의 사전 등록(pre-registration)과 같은 생각입니다. 결과를 보고 기준을 바꾸는 일을 막습니다.

반복을 더하는 방법은 이렇습니다. "Repeats are added one at a time until every value on the list holds." 다만 9.7 D26(인지오의 결정)에 따라 "a slice may add a batch up to the pool's own projection, then continue one at a time, the rule read after each". pool이 "지금의 퍼짐이면 아홉 번이면 된다"고 예측하면 한꺼번에 아홉까지 채우고, 그다음부터는 하나씩 더합니다. 상한은 없습니다(9.5 D33). 기록된 이유는 Kalibera §11의 "the required and optimum numbers of repetitions depend on the platform, VM, and benchmark"와, Georges의 "30 runs"가 예시일 뿐이라는 읽기입니다. 대신 9.5 D33은 "A value that does not converge because of how it is observed or analysed comes to 인지오 as a design question … instead of more repeats"라고 정했습니다. 수렴하지 않는 원인이 재는 방식에 있으면 반복을 늘려도 소용없으니 설계를 바꾸라는 것입니다(6.7절의 키만 재생하기가 그 예).

기록된 입력이 먼저 바닥나는 경우도 있습니다. SWELL-KW의 Outlook 기록은 창이 여덟 개뿐이고, IE 기록은 38개, Word 기록은 57개(입력이 있는 것은 56개)입니다. 그때는 "the values of the phases that replay it pool every window it holds and state their half-widths"(9.5 D32), 곧 기록의 모든 창을 다 쓰고 반폭을 밝힙니다. 입력보다 앞에 도는 단계(유휴 단계)의 값은 그 단계만 도는 반복을 더해 계속 채웁니다. `mail-client`의 유휴 단계가 77회 반복이 된 것이 이 때문입니다.

## 7.5 다섯 가지 예외

모든 값이 5 % 안에 들어오지는 않습니다. workflow 문서와 `measurement-overview.md` §7은 허용 오차 대신 반폭을 밝혀 담는 다섯 가지 예외를 정합니다. 앞의 넷은 "taken per value by 인지오's decision, after the value is seen failing", 곧 값이 실패하는 것을 본 뒤 값마다 인지오가 결정합니다. 다섯 번째는 기록의 길이에서 따라 나옵니다.

| 예외 | 언제 | 예 | 처음 정한 결정 |
|---|---|---|---|
| 퍼짐이 기계를 따름(machine spread) | 값이 프로그램이 아니라 runner의 디스크나 속도를 따라 움직임: 한 반복 안의 모든 스레드 run이 함께 움직이고 wake 빈도는 약 1 % 안에 머묾 | `cpu-batch`의 `python3`의 run between blocks와 block per run(±27.3 %, ±10.8 %; runner의 `khugepaged`); `module-build-orchestrator`의 tail block per run(±8.35 %; dkms의 진행 loop와 runner의 디스크); `renderer-hidden`과 `game-client`의 run 평균(±5.3–18.1 %) | 9.6 D29 (2026-09-20); 9.8 D17, D18 |
| 세션마다 다름(between sessions) | 한 긴 run 안에서 단계 길이의 창을 밀어 보면 반복 사이보다 훨씬 덜 움직임 | `code-editor`의 `utility/libuv-worker`(한 run 안 ±10.6 %, 반복 사이 ±39 %); `renderer-hidden`의 조용한 스레드 `Chrome_ChildIOT`, `Compositor`, `PerfettoTrace`(±6.5–17.6 %); `service-manager`의 pid 1 run 평균(±7.8 %); `message-bus`의 system bus(±11 %) | 9.5 D57 (2026-09-20) |
| 드문 component(sparse) | 한 단계에 몇 번만 깨어나 퍼짐이 개수 자체의 퍼짐 | `renderer-hidden`의 residual(단계마다 renderer당 5.0–7.2 wake) | 9.8 D27; 9.9 D33 |
| run 안의 드문 사건(rare event) | 한 반복이 0번, 1번, 2번 잡는 사건이 component 평균을 끌고 감 | Chrome의 `MemoryInfra` heavy pass(유휴 단계 22,800 s에 8번, 약 47분에 한 번); Steam client의 HTTP burst | 9.5 D64; 9.8 D33 |
| 기록이 바닥남(recording runs out) | 기록된 입력을 재생하는 단계인데 기록에 다음 창이 없음 | `mail-client`의 입력과 send(Outlook 8창; SWELL-KW 아래 입력당 평균 ±10.4 %, send의 `StreamTrans` run 평균 ±18.4 %); `web-browser`의 입력당 평균(38창, ±5.9 %) | 9.5 D32, D46 |

예외로 담은 값에는 공통의 단서가 붙습니다. "No reported result may rest on a difference in such a value smaller than its stated half-width." 반폭이 ±15 %인 값으로는 15 %보다 작은 차이를 결과로 주장할 수 없습니다. 그리고 machine-spread 예외는 "only for a value that carries none of the effects the slice reports"입니다. 조각이 보고하는 효과가 기대는 값에는 쓸 수 없습니다. 그런 값이 흔들리면, 9.8 D18처럼 효과를 흔들리지 않는 관찰량으로 다시 진술합니다(Steam client의 보이기/최소화 비교를 run 평균 대신 wake 빈도 비율로).

> **왜 이렇게 정했나.** machine-spread 예외의 이유는 9.6 D29에 있습니다. 네 값의 퍼짐이 runner의 디스크를 따르는데, machine gate는 CPU 모델만 잡고 디스크는 잡지 않으며(매번 같은 이름의 150 GB "Virtual Disk"), 반복을 늘려도 좁아지지 않았습니다(`tracker`는 6회에 ±11 %, 14회에 ±15 %). 그 값들이 job 시간에서 차지하는 몫도 함께 기록되었습니다(`clamscan` 2.4 %, `tracker` 4 %, `python3` 0.01 %). 이것은 9.6의 캠페인 때의 값들이고, 지금 library가 이 예외로 담는 값은 위 표의 것들입니다(`clamscan`과 `tracker`의 값은 그 뒤 library에 없고, `python3`은 9.10의 MNIST 캠페인으로 다시 쟀습니다). between-sessions 예외의 이유는 9.5 D57의 세 가지 발견입니다. 분석 탓이 아님(모든 반복에 같은 스레드), 단계의 위치 탓이 아님(긴 탐침 위에서 창을 밀어도 반복 사이만큼 움직이지 않음), 그리고 그 component가 단계 wake에서 차지하는 무게. 이 셋을 먼저 확인한 뒤에야 예외로 담습니다.

> **열린 자리.** 예외로 담은 값을 미리 정한 반복 수로 다시 잴지는 9.14 decision 3이 "pre-registered contingency"로 정했습니다. RQ0 gate spec의 반폭 줄(예외 값을 구간의 양 끝에 두고 다시 compile한 variant)이 판정 파일 하나라도 기준 g의 반대편으로 넘기면, 판정을 범위로 보고하고 그 entry를 다시 잽니다. 이것은 simulator가 계약대로 구현된 뒤 Phase 10의 RQ0 run에서 돌아갑니다. 아직 돌지 않았습니다(미실행).

## 7.6 처음 통과한 곳에서 멈추면 반폭이 낙관적이 되는 이유

이 절은 이 권에서 가장 미묘한 이야기입니다. 웹 엔지니어에게 가장 가까운 비유는 A/B 테스트의 "peeking"입니다. 실험을 돌리면서 매일 p값을 보다가 처음 유의해지는 날 멈추면, 거짓 양성이 명목상의 5 %보다 많아집니다. 멈추는 날을 결과가 골랐기 때문입니다.

stability rule도 같은 구조입니다. 반복을 하나씩 더하며 매번 반폭을 계산하고, **처음으로** 5 % 안에 들어온 순간 멈춥니다. 그런데 반폭은 표본 표준편차로 계산하므로 우연에 따라 흔들립니다. 우연히 표준편차가 작게 나온 순간에 반폭이 5 % 안으로 들어오기 쉽고, 바로 그 순간에 멈춥니다. 따라서 멈춘 시점의 반폭은 그 값의 진짜 불확실성보다 작게 나오는 경향이 있습니다. 반복 수가 그 반복 수가 만들어 낸 추정치에 의해 골라졌기 때문입니다.

이것을 수학으로 다룬 것이 Chow와 Robbins(1965, `chow-aoms65`)입니다. 이 규칙은 그들의 식 (3), "N = smallest k ≥ 1 such that v_k ≤ (d²k)/a_k²"와 같은 모양입니다. 그들의 정리는 폭 d가 0으로 갈 때만 명목 수준에 도달한다고 말하고(점근적), 유한한 경우에 대해서는 Starr의 계산을 전합니다. 정규 모집단에서 t 규칙을 쓰면 "for α = .95 the lower bound … is about .929". 95 % 구간이라고 말해도 실제로 참값을 덮을 확률이 최저 약 92.9 %까지 내려갈 수 있다는 뜻입니다.

이 문제는 기록에 세 단계로 남아 있습니다.

1. **발견(2026-09-24).** `measurement-campaign-record.md`의 "What the half-widths do and do not claim" 단락(자체 검토 중에 적음, "no decision taken")입니다. "the value that stopped an application sat at the boundary by construction: `soffice` 4.93 %, `mpv-audio` 4.93 %, `kdenlive` 4.94 %, `webrtc` 4.95 %, `mpv-video` 4.98 %, `thunderbird-send` 5.00 %, `gimp` 4.59 %." 멈추게 한 값은 구조상 경계에 앉아 있었습니다. 같은 단락은 라이브러리 전체에서 규칙을 읽는 133개 값 가운데 7개만 반폭이 4.5 % 이상이고 나머지는 여유 있게 통과했다는 것, "Stopping at the first crossing cannot bias a mean, so the values themselves stand; it does make the stated precision of that one value per application optimistic"라는 것, 그리고 미리 정한 반복 수로 다시 재면 "about three hours for `webrtc`, `mpv-video` and `mpv-audio` … about a day for `chrome` and `code`"가 든다는 것을 적었습니다.
2. **결정(2026-09-28, 9.5 D88).** 다시 재지 않고, 멈춤을 모의실험해 그 크기를 밝히기로 했습니다. `dataset/tools/meas/stopping.py`가 entry마다 규칙을 읽는 값 가운데 가장 넓은 것의 반복별 변동계수로 반복을 뽑아(정규와 로그정규, 각 4,000번의 캠페인), 규칙대로 멈추게 하고, 멈춘 평균의 치우침과 멈춘 구간이 참값을 덮는 비율을 셉니다. 결과는 "coverage 91.3–92.7 %, 91.3–91.4 %, 92.1–92.4 %; bias −0.09 to +0.20 %"(`office-writer`, `video-editor`, `audio-player`)였고, "Stopping at the first crossing cannot bias a mean"이 0.2 % 안에서 성립함을 확인했습니다. 이 단서는 해당 entry의 scope 문장에 들어갔습니다(`fold_in.py`의 `STOPPING_STATED`). 예를 들어 `office-writer`의 scope에는 "The repeat count is the rule's first pass (D88): simulated at the spread of the widest value … the rule's stated 95 % interval covers the true mean in about 91–93 % of campaigns and the stopped mean leans by at most 0.2 %"라고 적혀 있습니다.
3. **남은 일(9.16).** `_dev/TODO.md`의 9.16 줄은 "from 9.5's self-review: the measurement audit reads how each campaign's repeat count was chosen, the stopping rule being what makes the binding value's half-width optimistic"라고 적습니다. 여기서 **binding value**는 캠페인을 멈추게 한 값, 곧 멈춘 순간 기준선에 가장 가까웠던 값입니다. 최종 측정 감사는 캠페인마다 반복 수가 어떻게 정해졌는지 읽어야 합니다.

> **왜 이렇게 정했나.** 9.5 D88이 다시 재지 않고 단서를 다는 쪽을 고른 기록된 이유는 "taken before 9.13 on the question the self-review left to 9.14 and 9.16 — the count is chosen by the estimate it produces"입니다. 9.13의 재건축 전에 이 질문에 답을 내야 했다는 것입니다. 그리고 9.14 decision 3은 "The stated-precision caveats of 9.5 D88 are carried, not re-measured"로 이 선택을 확정했습니다.

## 7.7 이 규칙에 붙는 단서들

workflow 문서는 규칙을 인용할 때마다 따라다녀야 할 단서 둘을 적습니다.

- `maricq-osdi18`은 "nonparametric intervals of the median 'unless normality can be demonstrated'"(§2)를 권합니다. 이 규칙의 구간은 t 구간입니다. 이 프로젝트는 그 권고를 따르지 않았고, 그것을 밝힙니다.
- `cochran-st77`의 비율 분산은 대표본 결과입니다. "the large-sample results may be used if the sample size exceeds 30 and is also large enough so that the coefficients of variation of x̄ and ȳ are both less than 10%"(§6.3), 그리고 조건이 맞지 않으면 "the formula for v(R̂) tends to give values that are too low"(§6.5). 캠페인의 반복 수는 5부터 45입니다(workflow 문서; `measurement-overview.md`는 `mail-client`의 77을 넣어 "5 to 77"로 적습니다). 대부분 30보다 작으므로, 표의 반폭도 낮게 나올 수 있습니다.

`references.md`의 방법 문헌 항목들은 이런 단서를 항목 안에 적어 둡니다. 예를 들어 `kalibera-ismm13`의 role 줄은 "Its §11 precision figures … are the columns of its Table 6 for DaCapo on its platform P1, not a prescribed tolerance"라고 적고, `georges-oopsla07`은 "its machine variation is across different hardware platforms (§6.2.1), nothing on machines of one nominal type"이라고 적습니다. 문헌을 인용할 때 그 문헌이 말하지 않는 범위까지 함께 들고 다니는 것이 결정 1의 "whole claim"을 지키는 방식입니다.

## 7.8 기계 뽑기의 비용

CPU 모델 하나만 받는 규칙의 비용은 버려지는 job입니다. `measurement-campaign-record.md`의 "Machine draws" 절은 캠페인마다 job 수와 EPYC 7763을 뽑은 비율을 적습니다. 몇 개만 옮깁니다. 9.6 build 28 job 중 14(50.0 %), 9.5의 2026-09-18/19 캠페인 252 job 중 144 착지(57.1 %), 9.7 145 job 중 78(53.8 %), 9.8 105 job 중 60(57.1 %), 9.9 42 job 중 24(57.1 %), 무인 업그레이드 15 중 9(60.0 %), DKMS 37 중 26(70.3 %), Tracker 38 중 18(47.4 %), MNIST 8 중 6(75.0 %), costs 96 중 30(31.3 %). `measurement-overview.md` §6은 이것을 "About half of all jobs draw it (50–59 % by campaign)"로 요약합니다. 다른 모델에 걸린 job은 약 20 s 만에 설치 없이 끝나므로, 비용은 runner 시간보다 기다림(다시 띄우고 기다리는 시간)에 있습니다. 그래서 `loop/watch.py`가 걸린 창을 자동으로 다시 띄웁니다.

---

# 8장 · 측정이 측정을 망치지 않았나: 검사와 대조군

이 장은 "잰 값이 정말 그 프로그램의 행동인가, 아니면 측정 장치나 재생 장치나 분석이 만든 것인가"라는 질문에 답합니다. stability rule(7장)은 값이 **정밀한지**를 말할 뿐, 그 값이 **무엇을 잰 것인지**는 말하지 않습니다. 반복할 때마다 똑같이 틀리는 측정도 정밀합니다. 그래서 캠페인들은 여러 겹의 검사와 대조군을 두었습니다. `measurement-overview.md` §8이 그 목록입니다.

## 8.1 반복마다의 유효성 검사

반복 하나가 pool에 들어가기 전에 유효성(validity) 검사를 통과해야 합니다. workflow 문서의 loop 4단계가 목록입니다.

- gate가 EPYC 7763에서 열렸는가.
- 모든 단계가 있는가(어느 반복에 빠진 단계는 pool이 버립니다).
- 재생이 창의 모든 사건을 보냈는가(`replay.jsonl`을 `windows.json`에 대어), 모든 operation이 끝났는가(`n_ok`, `n_failed`).
- 0이 아닌 반환 코드는 모두 설명되는가(예: `perf record`의 130은 SIGINT로 멈춘 것, `freshclam`의 2는 시스템 서비스가 잠금을 쥔 것).
- 입력이 어디에 떨어지는지가 중요한 곳은 스크린샷.
- settle이 있는 곳은 안정 단계의 10 s 조각별 CPU 윤곽(launch 작업이 섞이지 않았는가).
- 측정 tree에 harness 프로세스가 없는가(`gate=harness-in-tree`, 9.8 D14).
- 속도를 조절한 네트워크 단계면 바이트가 실제로 조절기를 지났는가(9.7 D27, `gate=no-vf`).
- family 고유의 검사(9.8 D13: renderer 수가 job의 최소 이상인가, page server가 답하는가, 채팅 client가 homeserver에 닿았는가).

실패한 반복은 이유와 함께 빠지고(`pool_runs.py --exclude K --exclude-why TEXT`), 규칙과 예측치와 모든 값은 나머지로 다시 읽습니다(9.5 D47). 실제로 빠진 예를 보면 검사가 무엇을 막는지 알 수 있습니다.

- `file-backup`(borg)의 반복 3: 3.70 GB archive 대신 12,108 B 파일을 받아 빈 트리 위에서 단계가 돌았습니다.
- `incremental-backup`(Déjà Dup)의 반복 12와 25: mattmahoney.net이 12 KB 페이지를 돌려줬습니다(입력 세트를 못 받음).
- `game-download`(SteamCMD)의 반복 21(조절되지 않은 링크), 23(잘못 띄움), 32(`FAILED (No Connection)`), 33(잘린 `perf.data`).
- `mail-client`의 창 29: Outlook 창이 잘리지 않은 채 떠 있었습니다(9.5 D47).

이런 반복이 pool에 섞였다면 stability rule은 퍼짐이 커진 것만 보았을 것이고, 무엇이 잘못됐는지는 말해 주지 못했을 것입니다. 유효성 검사는 "이 반복이 그 측정을 한 것이 맞는가"를 먼저 묻습니다.

## 8.2 추적 없는 대조군: perf 자체가 값을 바꾸는가

모든 측정 단계는 `perf sched record` 아래에서 돌았습니다. 그런데 기록하는 행위 자체가 프로그램을 느리게 하지 않을까요? 2026-09-26의 9.5–9.9 검토가 이 질문을 던졌고, 2026-09-27 grill이 그 방법을 `_dev/docs/spec/jioh/task-9.5-untraced-control.md`로 정했습니다. spec의 첫 문단이 목적을 적습니다. "whether `perf sched record` over a measured phase moves the values the archetypes carry."

**방법.** 대조 job 하나가 측정 단계를 두 번 돕니다. 한 번은 캠페인과 똑같이 `perf sched record` 아래에서(traced), 한 번은 perf 없이(untraced). 두 번 모두 `/proc`(스레드마다 `schedstat`의 run 시간과 switch 수, `status`)를 읽습니다. job마다 값 하나당 비율(untraced ÷ traced)이 하나 나옵니다. 대상은 9.5의 아홉 응용, 9.8의 네 주체, 9.9의 세션으로 열네 주체이고, "Every archetype is controlled on itself"(decision 2)입니다. 주체마다 대조 job 여섯, 순서마다 셋씩(traced 먼저 셋, untraced 먼저 셋)이며, 반복별 비율의 95 % t 구간이 1을 빼면 차이로 읽습니다. 차이가 나면 그 archetype의 `modeling_notes`에 한계로 적고, **담은 값은 바꾸지 않습니다**. traced 값이 캠페인 전체와 같은 조건에서 잰 값이기 때문입니다. 원자료는 release 하나(`meas-ci-control-2026-09-27`)로 공개했습니다.

**결과.** `measurement-overview.md` §8의 요약은 "Where a difference is resolved, a wake rate's ratio, untraced over traced, lies in 0.97–1.08, and a run mean's in 0.72–0.98: tracing lengthens some threads' runs"입니다. 차이가 해결된 곳에서 wake 빈도는 거의 그대로(0.97–1.08)이고, run 평균은 추적이 없을 때 최대 28 % 짧았습니다. 예를 들어 `code-editor`의 `utility/libuv-worker` run 평균 비율은 0.716(0.639–0.792), `audio-player`의 재생 CPU 점유율은 0.860(0.834–0.886), `video-call`은 0.952(0.934–0.971)였습니다. 세 slice 합쳐 148 job 중 87이 착지했고(84가 pool에 들어감) 61이 gate에 걸렸습니다(`measurement-campaign-record.md`). 대조군은 2026-09-27에 entry들이 담고 있던 단계만 돌렸습니다. 그 뒤에 잰 세 묶음, 곧 열 entry의 launch 단계, `renderer-hidden`의 지금 안정 단계(`meas-ci:desktop:2026-10-05b`, Chrome 154), `video-editor`의 유휴 단계(`meas-ci:interactive:2026-10-05`)는 대조군을 거치지 않았고, `renderer-hidden`이 적은 비율은 Chrome 153의 이전 안정 단계에서 읽은 것입니다(`measurement-overview.md` §8).

다른 캠페인들은 다른 방식의 교차 확인을 가졌습니다. build 캠페인은 perf가 센 CPU와 taskstats가 센 CPU를 비교했습니다(`cc1`에서 약 1.005–1.01). SteamCMD download는 socket 추적의 비용을 따로 쟀습니다(추적 없을 때 CPU 0.975). 둘 다 "같은 양을 두 장치로 재서 장치의 영향을 경계 짓는다"는 같은 생각입니다.

> **왜 이렇게 정했나.** "No carried value changes"의 기록된 이유는 spec decision 2의 구조에 있습니다. 차이를 각 archetype의 limitation으로 적는다는 것입니다. 또 spec은 대조군의 traced run을 pool에 넣지 않는다고 정했습니다("The traced runs stay out of the pools"). 대조군은 측정의 일부가 아니라 측정에 대한 측정이기 때문입니다. 대조 결과는 각 entry의 notes에 들어갔고, 그 과정에서 대조가 비율을 읽지 못한 component(실행 중 시작하고 끝나는 스레드)는 9.5 D92가 따로 밝혔습니다.

## 8.3 자극 민감도 점검: 다른 사람의 타이핑이었다면

타이핑 entry 넷(`office-writer`, `code-editor`, `mail-client`, `web-browser`)은 SWELL-KW 기록을 재생합니다. 그런데 SWELL-KW는 2012년 Windows 실험실의 25명입니다. 다른 사람들의 다른 타이핑이었다면 값이 얼마나 달라졌을까요? 9.5 follow-ups spec decision 11은 이것을 사전 등록된 점검으로 정했습니다. "The 136M Keystrokes data is replayed as a second phase for the four typing-driven applications … The archetypes carry SWELL-KW whatever the result … a large difference is a stated limitation of D6, not a re-decision."

즉 각 반복이 `driven-alt` 단계에서 136M Keystrokes(`dhakal-chi18`, 168,960명이 외운 문장을 옮겨 친 기록)에서 자른 창을 함께 재생하고, 두 자극 아래의 입력당 run 평균을 비교합니다. 결과가 어떻든 archetype은 SWELL-KW 값을 담으며, 큰 차이는 한계로 밝힐 뿐 결정을 다시 하지 않습니다. 결과를 보고 자극을 바꾸는 일을 미리 막아 둔 것입니다.

9.5 D81(2026-09-27)은 이 점검을 반복별로 읽기로 했습니다. 각 반복의 136M 아래 평균을 같은 반복의 SWELL-KW 아래 평균으로 나누고, 그 비율들의 95 % t 구간이 1을 빼면 차이입니다. 결과는 `measurement-campaign-record.md`에 있습니다.

| entry | 비율 (136M ÷ SWELL-KW) | 95 % 구간 | 읽기 |
|---|---|---|---|
| `office-writer` | 1.123 | 1.045–1.200 | 차이 |
| `web-browser` | 1.338 | 1.284–1.392 | 차이 |
| `code-editor` | 1.029 | 0.968–1.090 | 해결 안 됨 |
| `mail-client` | 0.909 | 0.824–0.994 | 차이(pooled 중앙값은 반대 방향 +8 %) |

이 비율들은 각 entry의 scope에 한 문장씩 들어 있습니다. 이 점검이 말하는 것은 "자극이 바뀌면 값이 10–34 % 바뀔 수 있다"이고, 이것은 timeline의 입력 자극(SWELL-KW 하나)이 갖는 한계의 크기입니다.

> **왜 이렇게 정했나.** 9.5 D81이 점검을 반복별로 읽기로 한 이유는 "as 9.7 D36 reads a check — a comparison against ±5 % precision misses a shift every repeat shares"입니다. 모든 반복이 같은 방향으로 함께 움직이는 차이는, 두 값의 반폭을 각각 5 %와 비교하는 방식으로는 놓칠 수 있다는 것입니다. 짝을 지은 비교(paired comparison)가 그 차이를 잡습니다.

## 8.4 시간 창과 긴 탐침: 평균이 숨기는 것

archetype이 담는 값은 단계 전체의 평균입니다. 그런데 단계 안에서 일이 고르게 일어나지 않으면, 평균은 그 사실을 숨깁니다. 2026-09-28의 검토가 이것을 지적했고, 그 결과 `dataset/tools/meas/windows.py`가 모든 담은 단계를 시간 창(100 s, 짧은 단계는 20 s)으로 나눠 component마다 wake 빈도, run 평균, CPU를 읽게 되었습니다(9.5 D85, D87; 9.8 D34; 9.9 D42). 값은 바꾸지 않고, 단계의 일부에서만 일하는 것이 보이면 scope에 적습니다. 예를 들어 `web-browser`의 page load 56회 가운데 반복마다 첫 번째가 739 ms와 CPU 545 ms로 나머지 55회 평균(485 ms, 341 ms)보다 무거웠고, 그 사실이 scope에 적혀 있습니다(9.5 D87).

timeline은 측정 단계보다 훨씬 긴 시간 동안 프로그램을 붙잡아 둡니다(예: `c6-dual`은 12,068 s 동안 VS Code에 초점을 두었습니다. 9.17 D1이 그 초점을 686–688 s마다 게임과 번갈아 쥐게 하기 전의 일이고, 그 12,068 s가 VS Code의 span probe를 읽은 길이입니다. library의 `code-editor` scope가 9.23 D8 이후 그렇게 적습니다. "Read over 12,068 s, the span `c6-dual` held it focused before its focus alternated with the game every 688 s (9.17 D1)". 탐침의 길이와 읽은 값은 그대로입니다). 측정한 10분이 그 긴 시간에도 성립할까요? 9.10은 이것을 **span probe**(측정 단계보다 긴 탐침)로 확인했습니다(9.10 D143–D154, release `meas-ci-probes-2026-10-05`). 탐침은 반복이 아니며 어떤 값도 바꾸지 않습니다. 결과의 예를 몇 개 들면, `renderer-hidden`은 1,545 s 동안 wake 빈도는 유지되었으나 CPU는 그렇지 않았고, `code-editor`는 두 번째 탐침에서 매 창 전에 파일을 되돌리자 입력당 run 평균이 9.5의 같은 창 대비 1.00(0.97–1.03)이었습니다. 반면 첫 탐침에서는 줄 하나가 계속 길어지며 값이 올라갔고, 두 탐침 모두에서 VS Code의 extension host가 창 2–4개 동안 창당 최대 400 s의 CPU를 쓰는 일화가 있었는데, 그 일화는 담지 않고 scope에 밝혔습니다. 이렇게 확인한 뒤 `video-editor`의 유휴 단계는 Kdenlive의 launch 꼬리 뒤에서 다시 쟀습니다(9.10 D146, `meas-ci:interactive:2026-10-05`). 그 단계를 받친 탐침은 240 s settle 뒤 2,790 s를 읽어, `c3-creation`이 그 상태를 붙잡는 2,851 s보다 61 s 짧았습니다. 그래서 9.15가 그 span 전체를 담는 탐침을 하나 더 돌려(`kdenlive` 13, run 38976976741, release `meas-ci-probes-2026-10-17`; 인지오의 결정, 2026-10-17) 2,851 s 위에서 다시 읽었고, 180 s 단계는 9.10 D143의 5 % 기준을 지켰습니다(모든 반복이 받는 자리에서 CPU −0.3 %, wake +2.9 %; 가장 나쁜 자리에서 +4.5 %, +3.8 %).

## 8.5 compile이 측정을 재현하는가, 그리고 재현하지 못하는 것

측정값이 archetype에 들어간 뒤에는, 컴파일러가 그 값에서 다시 그린 wake 흐름이 측정과 같은 성질을 갖는지가 문제입니다. `measurement-overview.md` §8은 두 가지를 적습니다.

**재현하는 것.** 테스트(`dataset/tools/tests/test_measured_fidelity.py` 등)가 확인합니다. 표에서 뽑은 값의 평균이 표의 평균과 같은가, component마다 gap 표가 암시하는 wake 빈도가 측정 빈도와 2 % 안인가, 그리고 측정 archetype마다 compile된 흐름이 담은 wake 빈도를 "within 5 % or four standard errors of the count (`feller-ipta50`)"로 맞추는가. 표준오차는 Feller의 갱신 과정(recurrent event) 정리에서 옵니다(9.5 D86이 확인되지 않은 `feller-tams49` 대신 책 `feller-ipta50`을 인용하도록 바꿈).

**재현하지 못하는 것.** 컴파일러는 component마다 gap을 표에서 **독립적으로** 뽑습니다(9.5 D77). 그래서 각 component의 빈도와 gap 분포와 run 분포는 유지되지만, gap들이 실제로 어떤 순서로 왔는지(몰려서 오는지)와 여러 component가 함께 깨어나는지는 유지되지 않습니다. `dataset/tools/meas/burstiness.py`가 이것을 쟀습니다. 1 ms, 10 ms, 100 ms, 1 s 구간마다 wake 수를 세어 분산을 평균으로 나눈 값(dispersion; Poisson 흐름이면 1, 몰리면 1보다 큼)을 측정 흐름과 compile된 흐름에서 각각 구하고 그 비를 봅니다. `measurement-overview.md` §8이 적은 결과(2026-09-27에 읽음, 담은 반복들의 중앙값)는 이렇습니다. 1–100 ms에서 측정이 compile보다 `chat-client` 3.3–11배, `code-editor` 2.6–3.4배, `web-browser` 2.8–3.4배, `mail-client` 1.9–3.0배, `game-client` 1.9–3.0배, `video-editor` 1.3–1.4배, `renderer-hidden` 1.06–1.15배 더 몰려 있고, `audio-server`, `service-manager`, `message-bus`는 약 1, `compositor-shell` 0.86–0.97, `office-writer` 0.60–0.91(compile된 쪽이 더 몰림)입니다. `video-editor`의 값은 `meas-ci:interactive:2026-09-18`의 유휴 단계에서, `renderer-hidden`의 값은 `meas-ci:desktop:2026-09-20`에서 읽은 것이고, 두 entry가 지금 담은 pool(`meas-ci:interactive:2026-10-05`, `meas-ci:desktop:2026-10-05b`)은 아직 읽지 않았습니다. 그 다시 읽기는 9.16의 측정 감사에 들어 있습니다(`_dev/TODO.md` 9.16 줄).

이것은 **threat to validity**(타당성 위협)로 진술하기로 2026-09-26 검토가 정했고, `measurement-overview.md` §8이 그 위협을 진술합니다. TODO에 적힌 문장은 이렇습니다. "the compiled wake streams reproduce each component's rate, gap and run distributions, not the order of its gaps nor its components waking together." 그리고 이 위협이 결과에 영향을 주는지는 Phase 10의 **trace-replay check**로 확인합니다. 9.14 decision 10은 이것을 RQ0 gate spec에 사전 등록했습니다. `c7-dev`, `c7-browsing`, `c7-meeting`, `c2-p1a` 네 파일을 compile된 그대로 한 번, 측정된 반복 하나의 흐름(실제 순서)을 그대로 재생한 variant로 한 번 돌려, "each file's gap falls on the same side of g under both builds and differs by less than 0.17"이면 일치로 봅니다. 재생하는 흐름은 entry에 따라 세 종류입니다. `code-editor`, `web-browser`, `renderer-hidden`은 wake 순서(`wakes`), `package-upgrade`와 `cpu-batch`의 `python3`는 run과 그 뒤의 block(`runs`), `video-call`은 통화의 cycle(`cycles`)입니다(각 흐름 파일의 `kind`; `dataset/variants.yaml`의 `trace-replay` 주석은 2026-10-17부터 이렇게 적습니다). 네 파일 모두 batch job의 run 흐름도 재생합니다(variants manifest의 `replay` 항목: `c7-dev`, `c7-browsing`, `c7-meeting`의 upgrade, `c2-p1a`의 `python3`). 재생 흐름은 `dataset/replay/`에 있고, `replay_fold_in.py`가 release 원자료에서 만들며, `--check`로 바이트까지 재현됩니다.

> **열린 자리.** trace-replay check는 아직 돌지 않았습니다(미실행). simulator가 계약대로 구현된 뒤 Phase 10의 RQ0 run과 함께 돕니다. 불일치가 나오면 "disagreement stated as the compiled streams' ordering threat"입니다(9.14 decision 10). 그 뒤에 무엇을 할지(예: 순서를 보존하는 compile)는 기록에 정해지지 않았습니다.

## 8.6 빌드 혼합과 RQ0의 민감도 variant

**빌드 혼합.** 어떤 프로그램은 버전을 고정할 수 없었습니다. Google의 Chrome 저장소는 현재 버전만 내주므로 `web-browser`의 38회 반복은 152(29회)와 153(9회)이 섞였습니다. 9.5 D69는 "the application build is pinned where it can be, recorded and stated where it cannot"으로 정했고, 9.5 D93은 두 빌드를 값마다 비교했습니다. 60개 값 중 59개는 152 반복들의 퍼짐 안 1.80 표준편차 이내에서 같았고, page load의 `gpu/VizCompositorTh` run 평균 하나만 −16.0 %(−2.31 표준편차) 달랐습니다. 그 값은 두 빌드를 합친 값으로 담고, 차이는 scope에 밝혔습니다.

**민감도 variant.** 측정의 한계가 결과에 얼마나 닿는지를 보기 위해, 9.14 decision 10과 12는 판정 파일들의 variant를 만들어 RQ0 gate spec에 고정했습니다(`dataset/variants.yaml`, 아홉 set, artifact 78개). 측정과 관련된 것은 셋입니다.

- `venue-x0.8`, `venue-x1.25`(`scale-runs`): 게임 chain을 뺀 모든 RUN을 ×0.8과 ×1.25로. 이유 문장은 "the venue factor's lower edge, 1/1.25 (9.6 D32; the bracket contains the ×1.144 huge-page ratio of 9.10 D88 and the tracing overhead's ×1.02–1.16)"입니다. runner라는 장소가 값을 얼마나 흔들 수 있는지에 대한 설계상의 괄호입니다.
- `corner-low`, `corner-high`(`carried-bounds`): 예외로 담은 값(`carried_values`의 표 19개)을 반폭의 양 끝으로 옮겨 다시 compile. 2026-10-17에 `renderer-hidden`의 `Compositor`와 `PerfettoTrace`(세션 사이에서 변하는 값, 7.5절의 표)가 gap과 run 표 둘씩 더해져 15개에서 19개가 되었습니다(9.15 기록 `logs/B1-data-rebuild.md`).
- `replay`(`trace-replay`): 위의 trace-replay check.

2026-10-10 감사의 fidelity map은 "venue sweep ×0.8–1.25 narrower than the measured 0.50–0.72× cross-CPU spread"라고 적었습니다. 9.6이 잰 CPU 모델 사이의 차이(Xeon Platinum 8573C가 `cc1`을 EPYC 시간의 0.72배, `fixdep`을 0.50배에 돌림)가 venue variant의 괄호보다 넓다는 뜻입니다. 인지오가 2026-10-16에 괄호를 그대로 두기로 정했습니다(9.15 작업 목록 W-0752). 괄호(×1/1.25, ×1.25)가 담는 것은 측정된 두 장소 효과, 곧 huge page 비율 ×1.144와 추적 overhead ×1.02–1.16이고, CPU 모델은 아닙니다. 다른 CPU 모델은 프로그램마다 다른 비율로 속도를 바꾸므로 공통 배수 하나로 재현되지 않습니다. 이 한계는 세 곳에 적혀 있습니다. `docs/research-claims.md`의 "What is not claimed"(scheduling 결과가 다른 CPU나 다른 기계 구성으로 옮겨 간다고 주장하지 않음), `measurement-overview.md` §11의 CPU 모델 항목, 그리고 venue variant를 설명하는 문서들(`dataset/README.md`의 Sensitivity variants 절, harness guide의 RQ0 gate 장)입니다. 이 variant들은 Phase 10에서 처음 돌아갑니다(미실행).

---

# 9장 · 원자료와 기록: release, 기록 문서, 재현

이 장은 "측정의 원자료는 어디에 있고, 측정의 기록은 어떤 문서들에 나뉘어 있으며, 값을 다시 만들어 보려면 무엇을 하면 되는가"라는 질문에 답합니다. 결정 8(exit criteria)이 "every measured value reproduces from the released raw data"를 요구하므로, 이 경로가 열려 있는지가 곧 Phase 9가 끝날 수 있는지를 정합니다.

## 9.1 왜 release인가

측정 job의 결과는 GitHub Actions의 artifact로 올라갑니다. 그런데 artifact는 기한이 지나면 사라집니다. GitHub 문서는 "By default, checks, workflow runs, commit statuses, and the artifacts and log files generated by workflows are retained for 90 days before they are automatically deleted"라고 적고(`gh-artifact-retention`, 2026-10-16에 읽음), 9.10 D174 등 여러 기록이 같은 기한을 적으며, phase spec decision 6은 `meas-ci:names:2` run의 artifact가 2026-12-09에 만료된다는 것을 Phase 9의 첫 일 가운데 하나로 꼽았습니다. 그래서 캠페인의 원자료는 GitHub **release**(저장소에 태그와 함께 붙는 영구 파일 묶음)로 옮깁니다. id 규칙과 workflow 문서는 이것을 "The raw records of a campaign are one release"라는 규칙으로 적습니다. 다만 2026-09-18부터 2026-09-20까지의 9.5 캠페인들은 release를 나눠 쓰고(예: `meas-ci-2026-09-18`이 세 캠페인의 자료를 담고, `meas-ci:interactive:2026-09-19`는 `meas-ci-2026-09-18`과 `meas-ci-2026-09-28`에 걸침), id 규칙도 이제 그렇게 적습니다.

release를 만드는 것은 바깥으로 공개되는 일이므로, workflow 문서의 loop 7단계는 "the raw records are released (outward-facing: ask first)"라고 적습니다. 실제로 여러 기록이 "by 인지오's decision"이나 "released on 인지오's go-ahead"로 release를 남깁니다(예: 9.12 D54의 `meas-ci-costs-2026-10-08`). release는 앞으로도 손으로 만듭니다(인지오의 결정, 2026-10-16; 9.15 작업 목록 W-0732). 모든 `meas-*` workflow는 `actions/upload-artifact`에서 끝나고, 캠페인을 pool할 때, artifact가 90일에 지워지기 전에 release를 만듭니다.

데이터가 인용하는 캠페인과 그 release를 잇는 기계용 지도가 `dataset/meas-releases.yaml`입니다(9.15, 2026-10-16). 캠페인 태그마다 그 원자료를 담은 release의 태그, 주소, asset마다의 이름과 SHA-256(GitHub API의 `digest`)을 적습니다. 2026-10-16에 지도를 만들 때 데이터가 인용하는 캠페인 23개가 release 21개, 서로 다른 asset 463개에 이어졌고(지도의 asset 항목은 464개입니다. `meas-ci-2026-09-18`의 `meas-interactive-six.zip`이 `meas-ci:interactive:2026-09-18`과 `meas-ci:interactive:2026-09-19` 아래 모두 적혀 있기 때문입니다), 인용하는 캠페인 가운데 release가 없는 것은 없었습니다. `make lint`의 release-map lint(2.7절)가 지도에 없는 캠페인 태그를 실패시키므로, release가 없는 태그는 데이터에 들어올 수 없습니다. 이 지도는 어느 manifest의 입력도 아닙니다.

release에는 착지한 반복만이 아니라 gate에 걸린 job의 report도 들어갑니다. 9.7 D37("the pooled records carry the jobs the gates stopped")의 취지이며, 예를 들어 `meas-ci-background-2026-10-02b`(Tracker)는 "18 pooled + 3 dry + 12 unpooled landings + 32 gated reports"를 담습니다. 무엇을 버렸는지도 공개된다는 뜻입니다.

## 9.2 release 목록

2026-10-17에 `gh release list`로 확인한 release는 33개입니다(이 권의 처음 판은 32개라고 적었지만 그때의 release는 표의 처음 31행이 전부였습니다. 마지막 두 행은 9.15가 2026-10-17에 만든 것입니다). 제목은 release에 붙은 그대로이고, "담은 것"은 기록 문서들에서 옮겼습니다.

| release | 제목 | 담은 것 |
|---|---|---|
| `meas-ci-2026-08-28` | meas-ci raw data: cli:3, gui:2, names:1, names:2 | Phase 2의 첫 캠페인(지금 어떤 값도 받치지 않음); 9.3이 names:2를 더함 |
| `meas-ci-2026-09-14` | meas-ci raw data: interactive:3, playback:3 (9.5 campaign) | 9.5 D3의 첫 캠페인(4 vCPU, 고정 없음); 9.5 D21의 wake 정의 점검의 데이터 |
| `meas-ci-2026-09-16` | 9.5 follow-up campaign (single-core) | 9.5 D25의 한 CPU 캠페인; D26이 대체(여러 CPU 모델이 섞임) |
| `meas-ci-build-2026-09-18` | 9.6 compile campaign (single-core) | `build-orchestrator`, `compiler-child`, `cpu-batch`(9.6 프로그램들) |
| `meas-ci-background-2026-09-19` | 9.7 background and IO campaign (single-core) | `file-archiver`, `game-download`(그리고 9.10이 Déjà Dup으로 대체한 `file-backup`); 9.7 D41의 Valve 통계 snapshot asset |
| `meas-ci-desktop-2026-09-20` | 9.8 browser and comms campaign (single-core) | `renderer-hidden`(뒤에 `-10-05b`로 대체), `renderer-visible`(9.10 D16이 library에서 뺌), `chat-client`, `game-client` |
| `meas-ci-session-2026-09-24` | 9.9 daemons and session campaign (single-core) | `compositor-shell`, `audio-server`, `service-manager`, `message-bus` |
| `meas-ci-2026-09-18` | 9.5 same-machine repeats, the six (single-core) | `office-writer`, `image-editor`, `video-editor`, `video-player`, `audio-player`; `mail-client`의 첫 유휴 반복 43개 |
| `meas-ci-2026-09-20` | 9.5 same-machine repeats, the three re-measured (single-core) | `web-browser`, `video-call` |
| `meas-ci-2026-09-25` | 9.5 code re-measured keys only (single-core) | `code-editor` |
| `meas-ci-2026-09-27` | 9.5 thunderbird-send re-measured keys only (single-core) | `mail-client`의 입력과 send |
| `meas-ci-control-2026-09-27` | the untraced control of 9.5, 9.8 and 9.9 (single-core) | 추적 없는 대조군(8.2절) |
| `meas-ci-2026-09-28` | 9.5 thunderbird-send idle-only repeats added (single-core) | `mail-client`의 유휴 반복 34개 추가 |
| `meas-ci-background-2026-10-01` | 9.10 unattended-upgrade campaign (single-core) | `package-upgrade` |
| `meas-ci-background-2026-10-02` | 9.10 DKMS campaign (single-core) | `module-build-orchestrator`, `module-compiler-child` |
| `meas-ci-background-2026-10-02b` | 9.10 Tracker campaign (single-core) | `file-indexer` |
| `meas-ci-background-2026-10-03` | 9.10 MNIST training campaign (single-core) | `cpu-batch`의 `python3` |
| `meas-ci-background-2026-10-03b` | 9.10 HandBrakeCLI transcode campaign (single-core) | `video-transcoder` |
| `meas-ci-background-2026-10-03c` | 9.10 Kdenlive export campaign (single-core) | `cpu-batch`의 `kdenlive_render` |
| `meas-ci-background-2026-10-04` | 9.10 Déjà Dup backup campaign (single-core) | `incremental-backup` |
| `meas-ci-desktop-2026-10-04` | 9.10 Chrome tab-set campaign | `renderer-hidden`의 `count: 4` |
| `meas-ci-desktop-2026-10-04b` | 9.10 launch campaign | 열 entry의 `launch` 흐름(`dataset/launch/`) |
| `meas-ci-interactive-2026-10-05` | 9.10 Kdenlive idle campaign | `video-editor`의 유휴 단계 |
| `meas-ci-desktop-2026-10-05` | 9.10 Kdenlive launch re-trace | `launch-video-editor` 흐름 |
| `meas-ci-desktop-2026-10-05b` | 9.10 hidden-renderer campaign | `renderer-hidden`의 지금 값과 그 launch |
| `meas-ci-probes-2026-10-05` | 9.10 span probes | 긴 탐침(8.4절) |
| `meas-ci-probes-2026-10-07` | 9.10 upgrade probe | 세션 옆의 무인 업그레이드 탐침(`c7-idle`의 진술) |
| `meas-ci-sched-2026-10-07` | 9.11 runner read of the scheduler tunables | runner 커널의 base slice 읽기 |
| `meas-ci-probes-2026-10-07b` | 9.11 class census | 모든 측정 대상의 scheduling class 조사 |
| `meas-ci-costs-2026-10-08` | 9.12 kernel-cost and LLM-latency campaign | 본문용 커널 비용과 LLM 지연(archetype 아님) |
| `meas-local-m1pro-llm-2026-10-08` | meas-local:m1pro-llm:2026-10-08 — raw records | 인지오의 M1 Pro 노트북 관찰(`meas-ci` 아님, 9.12 D110) |
| `meas-ci-probes-2026-10-17` | 9.15 Kdenlive idle span probe | `video-editor` 유휴 단계의 `c3-creation` span 읽기(8.4절) |
| `meas-ci-probes-2026-09-20` | 9.5 long-phase probes | settle을 정한 9.5의 긴 단계 탐침(`thunderbird-send`, `chrome`, `code`, `webrtc`; 6.5절) |

이름에 주의할 점이 있습니다. 2026-09-24의 session campaign release는 `meas-ci-session-2026-09-24`입니다. 이름이 `meas-ci-2026-09-24`인 release는 없습니다. 다만 `meas-ci-2026-09-18`과 `meas-ci-2026-09-20`은 2026-09-24에 공개되었습니다(9.5 D70의 fold-in 때). 그리고 release 이름의 날짜는 캠페인 태그의 날짜와 같은 규칙(첫 batch를 띄운 날)을 따르므로, 공개된 날과 다를 수 있습니다.

2026-10-10 감사는 데이터 공개에 대해 네 가지를 적었습니다. "no release URL/asset hash beside values (only replay streams carry release+asset); no LICENSE; SWELL-derived `dataset/stimulus/` is CC-BY-NC-SA; releases made manually (workflows end at upload-artifact)." 값 옆에 release URL과 asset 해시가 없고(replay 흐름만 가짐), LICENSE가 없으며, SWELL에서 파생한 자극 흐름은 CC-BY-NC-SA 4.0이고, release는 손으로 만든다는 것입니다. 9.15가 넷을 모두 다뤘습니다.

- **LICENSE.** 9.15 spec decision 12(2026-10-14)대로 두 파일이 생겼습니다. 저장소 맨 위의 `LICENSE`는 코드를 MIT로, `dataset/LICENSE`는 데이터셋의 데이터(code가 아닌 `dataset/`의 파일, compile된 `dataset/build/`, 측정 release의 asset)를 CC-BY-NC-SA-4.0으로 둡니다. 저작권자는 Jioh In, Kyungmin Inn, Ian Park입니다. `dataset/LICENSE`는 자극 흐름과 SWELL-KW 입력 창의 출처로 SWELL-KW(Koldijk et al., 2014, DANS, CC-BY-NC-SA-4.0)를 밝히고, 136M Keystrokes에서 자른 `aalto-*` 창은 이 licence에 들지 않고 그 출처의 조건(비상업적 연구, 저자 표시)으로 배포된다고 적습니다(인지오의 결정, 2026-10-16).
- **값 옆의 release 주소와 해시.** 캠페인 단위의 기계용 지도 `dataset/meas-releases.yaml`과 그 lint로 정했습니다(9.1절; 인지오의 결정, 2026-10-16). 사람용 요약은 `measurement-overview.md` §9의 release 표입니다.
- **손으로 만드는 release.** 그대로 손으로 만들고, 문서가 그렇게 말합니다(9.1절).
- **compile된 데이터셋의 공개.** `build/`는 공개하지 않습니다. 저장소와 commit된 manifest로 다시 만들고 확인합니다(`make dataset variants generated`, `make check`). 논문을 제출할 때 저장소의 태그와 compile된 build의 snapshot을 DOI를 발급하는 데이터 저장소에 올리고, 데이터는 CC-BY-NC-SA-4.0입니다(인지오의 결정, 2026-10-16; 9.15 작업 목록 W-0733).

`dataset/README.md`는 이것을 "Licence and data availability" 절에 적습니다. 감사가 지적한 옛 문장 "raw data lives on the GitHub release named in the tag's registry entry"(registry 항목은 어떤 release도 이름 짓지 않았음)는 지금 "Each `meas-ci` campaign the data cites has its raw records on one or more GitHub releases of this repository; `meas-releases.yaml` lists each with its tag, its URL and every asset's sha256, and `make lint` fails a campaign tag it does not map"로 바뀌었습니다.

## 9.3 기록이 나뉘어 있는 곳

측정 하나의 이야기는 여러 문서에 나뉘어 있습니다. 어디에 무엇이 있는지를 한 표로 정리합니다.

| 문서 | 무엇이 있나 | 상태 |
|---|---|---|
| `_dev/research/jioh/measurement-campaign-workflow.md` | 모든 캠페인이 따르는 규칙: 측정값의 정의, stability rule, 예외, 첫 실행 전 할 일, 도구, loop | 2026-09-19 고정, 2026-09-24까지 개정 |
| `_dev/research/jioh/measurement-campaign-record.md` | 캠페인마다 반복 수, 규칙이 덮는 값, 가장 넓은 반폭, 무엇이 멈추게 했나, 기계 뽑기; 2026-09-24의 반폭 단서; 대조군 결과 | 9.12까지 기록 |
| 각 조각의 `campaign/method.md` | 그 캠페인의 설계(목록, 첫 batch, 단계, 입력), 날짜를 단 개정 | 캠페인마다 |
| 각 조각의 `campaign/results/` | `pooled.json`, `results.md`(pool이 쓴 그대로) | 캠페인마다 |
| 각 조각의 `campaign/machine-draws.md` | job마다 뽑힌 CPU 모델 | 캠페인마다 |
| 각 조각의 `changelog.md` | 측정에 관한 결정(설계, 예외, 반복 추가, fold-in, release) | 조각마다 |
| `dataset/archetypes.yaml`의 entry | `validation_stats`(`referee`, `run`, `stats`, `scope`), `modeling_notes` | 지금 값 |
| `docs/workload/measurement-overview.md` | 사람을 위한 요약: 원칙, 측정 archetype, 파이프라인, 정의, 규칙, 예외, 검사, 캠페인과 release, 문헌, 주장의 범위 | draft, 2026-09-29 작성, 2026-10-17 갱신 |

`measurement-campaign-record.md`의 첫 문단은 각 행을 어떻게 다시 만드는지까지 적습니다. "Each row regenerates with `dataset/tools/meas/loop/pool_runs.py <family>/<app> --since 10`"이고, 캠페인마다 `--since` 값(그 캠페인의 첫 run 번호)과 제외할 반복이 이어집니다(예: `chrome`: `--since 438 --exclude 16@35712250969`). 즉 이 기록은 결과의 사본이 아니라 결과를 다시 계산하는 명령의 목록이기도 합니다.

두 사람용 요약 가운데 `measurement-overview.md`는 9.15의 전체 정리(spec decision 4)가 library에 맞췄습니다. 이 권을 처음 쓸 때(2026-10-14) 그 문서는 "The 23 archetypes"라고 하며 지금 library에 없는 `file-backup`, `renderer-visible`을 싣고, 9.10의 측정 entry 일곱(`module-build-orchestrator`, `module-compiler-child`, `package-upgrade`, `file-indexer`, `video-transcoder`, `incremental-backup`, `game-download-idle`)과 9.10의 release들을 빠뜨렸습니다(§9의 release 표가 9.9에서 멈춤). 지금은 측정 entry 28개(`archetypes.yaml`에서 `category_source: meas`인 항목 수)를 §2에 싣고, §9의 release 표가 9.10의 캠페인 release까지 담습니다. 다른 하나인 `measurement-campaign-record.md`의 맨 앞 Campaigns 표는 14개 태그만 싣고 9.10의 나머지 캠페인(Tracker, MNIST, HandBrake, Kdenlive export, Déjà Dup, Chrome 탭, launch, Kdenlive 유휴, 숨은 renderer)은 본문 절에만 있습니다. 감사는 이것을 "campaign-record master table omits 10 of 22 cited campaigns"로 적었습니다. 이 기록은 `_dev/` 아래의 개발 이력이므로 9.15 spec decision 11("The existing files under `_dev/` are not touched")에 따라 그대로 둡니다. 9.10의 캠페인들은 기록의 본문 절과 `measurement-overview.md` §9, 그리고 `dataset/meas-releases.yaml`에서 찾을 수 있습니다.

## 9.4 다시 만들어 보는 길

측정값이 원자료에서 다시 나오는지는 세 층에서 확인할 수 있습니다.

**1. 원자료 → pooled record.** release의 asset을 내려받아 `pool_runs.py`(또는 family의 `pool.py`)를 돌리면 `pooled.json`이 다시 나옵니다. 이 단계의 재현은 지금 테스트에 들어 있지 않고, 9.16의 측정 감사가 할 일입니다. TODO 9.16 줄이 구체적인 경우를 적습니다. 예: "from 9.5 (D75): the three periodic pools' `cycle` blocks reproduce from releases `meas-ci-2026-09-18` and `meas-ci-2026-09-20` with `pool.py` at `cc51eb8`", "from 9.9 (D26, D47): reproduction from release `meas-ci-session-2026-09-24` with the tooling of 9.9 D47", "from 9.5 (D94, D97): `mail-client`'s 77-repeat idle pool reproduces from releases `meas-ci-2026-09-18` and `meas-ci-2026-09-28` at `0aa25ac`". 도구가 그 뒤에 바뀌었을 수 있으므로 커밋까지 고정해 둔 것입니다.

**2. pooled record → `archetypes.yaml`.** 이 단계는 테스트가 매번 확인합니다.

- `test_meas.py::test_the_fold_in_regenerates_the_nine_entries_from_the_pooled_records` — 9.5의 아홉 entry.
- `test_meas_desktop.py::test_the_fold_in_regenerates_the_library_s_entries_from_the_pooled_record` — 9.8과 9.10의 desktop entry.
- `test_meas_session.py::test_the_fold_in_regenerates_the_four_entries_from_the_pooled_record` — 9.9의 넷.
- `test_measured_fidelity.py::test_the_batch_tables_regenerate_from_the_pooled_records` — 컴파일과 백그라운드 entry의 batch-loop 표(`batch_fold_in.py --check`와 같은 일).

9.13 D8(2026-10-09)은 이 재생성 테스트를 "the audit's check that each measured entry still reproduces from its pooled record with the field in place"로 9.16에 넘겼습니다. 재건축(9.13)이 `declared_class` 필드를 더하면서 이 도구들이 library 문자열을 줄 패턴으로 읽다 깨졌던 것을 고친 결정입니다.

**3. `archetypes.yaml`과 timeline → compile된 workload.** 이 단계는 build gate, manifest, CI, tests를 다루는 7권이 자세히 다룹니다. 요점만 적으면, 같은 timeline과 library와 seed는 바이트까지 같은 결과를 내고, manifest가 그 해시를 고정하며, CI가 매번 다시 compile해 비교합니다.

trace-replay 흐름(`dataset/replay/`)은 1단계를 건너뛰는 특별한 경우입니다. `replay_fold_in.py`가 release의 asset에서 직접 흐름을 만들고(`<raw-root>/<release>/<landing>` 배치), `--check`가 committed 파일과 바이트까지 같은지 확인합니다. 2026-10-10 감사는 이것을 실제로 돌려 "`replay_fold_in.py --check` 14 s exit 0 (6 streams byte-identical from landings)"를 확인했습니다.

---

# 10장 · 측정값 하나를 끝까지: `package-upgrade`의 26.385초

이 장은 2.8절의 길을 반대 방향으로 걷습니다. 측정 job 하나에서 출발해, 그 숫자가 `archetypes.yaml`의 태그와 timeline의 `source` map에 이르기까지를 한 단계씩 따라갑니다. 질문은 "이 숫자 하나가 근거를 얻기까지 정확히 무엇이 일어났는가"입니다.

## 10.1 왜 이 값을 골랐나

`package-upgrade`는 Ubuntu 24.04가 기본으로 켜 두는 무인 업그레이드(`unattended-upgrades`)의 설치 단계를 담은 archetype입니다. 이 값을 고른 이유는 셋입니다. 첫째, 하중이 큽니다. CPU 총량 26.385 s는 C7의 상호작용 counterpart 열 개(`c7-browsing`, `c7-dev`, `c7-gaming`, `c7-idle`, `c7-mail`, `c7-media`, `c7-meeting`, `c7-office`, `c7-photo`, `c7-video-edit`)와 `c2-p2b`, 모두 열한 파일이 묶고, 그 가운데 여덟(`c7-browsing`, `c7-office`, `c7-dev`, `c7-photo`, `c7-meeting`, `c7-gaming`, `c7-video-edit`, `c2-p2b`)이 RQ0 판정 파일입니다(`dataset/variants.yaml`의 `judging` 목록). **counterpart**는 C7 group에서 기준 파일(C1)과 짝을 이루어 "사용자가 원하지 않는 백그라운드 작업"이 끼어든 쪽을 맡는 파일입니다. 둘째, 캠페인이 작습니다(9회 반복). 셋째, 결정부터 compile까지 모든 단계의 기록이 한 날(2026-10-01)에 몰려 있어 따라가기 쉽습니다.

## 10.2 왜 이것을 재게 되었나: 결정들

**9.10 D3, 바꿀 대상.** 이전의 C7 파일들은 원하지 않는 작업으로 `clamscan`(ClamAV의 바이러스 검사)을 넣었습니다. 9.10 D3(2026-10-01)은 이것을 Ubuntu 24.04의 stock 무인 업그레이드로 바꾸고, 그것을 runner 캠페인으로 재기로 했습니다. 기록된 이유는 이렇습니다. ClamAV 문서 스스로 "designed especially for e-mail scanning on mail gateways", "ClamAV is not a traditional anti-virus or endpoint security suite"라고 하고, 어떤 ClamAV 패키지도 예약 검사를 싣지 않으며(2026-09-13 검증의 C-plain-2도 `CONTRADICTED`였습니다), Debian popcon에서 ClamTk의 정기 사용은 0.11 %입니다. 반면 `unattended-upgrades`는 Ubuntu 24.04.5.1 데스크톱의 기본 층에 있고, 기본으로 켜져 있으며, 매일 06:00에 최대 60분 지연으로 돕니다. 결정 3이 말한 "현실 주장이면 관찰이 있어야 한다"를 따라, 존재가 확인되는 stock 작업으로 바꾼 것입니다.

**9.10 D36, 어떤 날의 업그레이드인가.** 업그레이드의 일의 양은 그날 설치될 업데이트에 달렸습니다. D36은 "one real day's security updates"를 재기로 하고 2026-07-27을 골랐습니다. 그날은 glibc 2.39-0ubuntu8.7 → 8.8, 바이너리 넷(`libc-bin`, `libc6`, `libc6-dbg`, `locales`)이었습니다. 기록된 이유는 한 해(2025-10-01 – 2026-09-30) 동안 기본 층의 1,488개 바이너리에 대한 일별 업데이트 조사(S3-58)입니다. 아무것도 없는 날이 222일(61 %), 커널이 아닌 업데이트가 있는 날이 125일(34 %)로 그 중앙값이 소스 패키지 둘, 바이너리 넷, 새 커널이 있는 날이 18일(5 %)이었습니다. 바이너리 넷은 125일의 중앙값이고, 그런 날 여덟 가운데 2026-07-27이 가장 최근이었습니다.

**9.10 D37, D38, 상태와 경계.** 매 반복은 영어 기본 설치의 기본 층(1,445개 바이너리)을 2026-07-27T00:00Z 시점의 archive로 chroot 안에 짓고, 2026-07-28T00:00Z의 archive에 대해 내려받기 단계(`apt.systemd.daily update`)를 돌린 뒤, 설치 단계(`apt.systemd.daily install`)만 측정 CPU에서 잽니다. 영어 설치는 design입니다. dry run(run 36843481310)이 보여 준 것 때문에 unit의 `apt-helper wait-online` 단계는 빼고 밝혔습니다. chroot 안에서는 `systemctl is-active`가 세 네트워크 관리자 모두에 성공을 답해 대기 프로그램 셋이 다 돌았고, 그중 하나가 30 s를 기다려 56 s 단계의 27 s를 CPU 없이 채웠기 때문입니다. 온라인 데스크톱은 그 상태에 있지 않습니다.

**9.10 D39, D40, 형식과 이름.** 측정된 job은 916개의 짧은 프로세스가 이어지는 포화된 사슬이었으므로, entry는 `cpu-batch`의 batch-loop 형식을 따르되 프로세스 tree 전체에서 "voluntary block 사이의 run"과 "그 뒤의 block"을 모읍니다(D39). task의 이름은 `/usr/bin/unattended-upgrade`의 comm인 `unattended-upgr`(15자로 잘림)이고, entry id는 `package-upgrade`입니다(D40). CPU의 대부분(76 %)은 `locale-gen`이 18개 영어 locale을 컴파일하는 `localedef`의 것이지만, 이름은 tree 전체를 대표합니다.

**9.10 D17, 통째로.** 일괄 작업은 측정된 전체를 돌리고, 파일 길이가 그에 맞춥니다. 그래서 `total_work`는 측정된 CPU 총량 그 자체입니다.

## 10.3 방법 문서: 띄우기 전에 정한 것

캠페인을 띄우기 전에 `_dev/research/jioh/task-9.10-scenarios-timelines/campaign/upgrade/method.md`(2026-10-01)가 7.4절의 네 가지를 정했습니다.

- **목록**: `upgrade-install` 단계의 run between voluntary blocks와 block per run(각각 표가 담는 평균으로, 비율 추정량), 그리고 CPU 총량(반복별 값으로). 프로세스 수는 보고만 하고 담지 않습니다.
- **허용 오차**: workflow의 5 %, 시간 표에는 1 µs. "this campaign reports no comparison of carried values, so the 5 % rests on the workflow's ground alone."
- **첫 batch**: 반복 1–5, 규칙의 최소. dry run은 job 하나라 퍼짐을 예측할 수 없기 때문입니다.
- **유효성**: gate가 EPYC 7763에서 열림; 모든 반환 코드 0(perf record의 130 제외); 층이 빠지거나 넘치는 패키지 없이 지어짐; 내려받기가 패키지 넷을 받음; 설치가 넷을 8.7 → 8.8로 바꾸고 로그에 "All upgrades installed"; 모든 반복에서 같은 변경 집합; chroot에 `/run/systemd/system` 없음.

## 10.4 trigger와 workflow

campaign은 `.github/campaign-background.json`의 `apps`에 `upgrade`를, `repeats`에 번호들을, `cpu_model`에 `EPYC 7763`을, `mode`에 `full`을 써서 push하면 시작됩니다(`loop/launch.py`가 파일을 쓰고 커밋하고 push합니다). `meas-background.yml`의 plan job이 이를 읽어 `(upgrade, k)`의 matrix를 만들고, run job마다 새 runner에서 `bash dataset/tools/meas/background/run.sh upgrade <k> full`을 돕니다(제한 시간 330분, 동시 최대 5).

## 10.5 job 하나의 안

`background/run.sh`의 `upgrade` 부분이 하는 일을 순서대로 적습니다(파일의 주석과 코드에서).

1. `spec.json` 기록, machine gate. 다른 모델이면 여기서 끝.
2. harness CPU에서 `mmdebstrap`을 설치하고, `upgrade-layer.txt`의 1,445개 패키지로 chroot를 짓습니다. archive는 `http://snapshot.ubuntu.com/ubuntu`의 `20260727T000000Z` 시점입니다. 층의 SHA-256(`b137960b…`), 빠진 패키지 수, 넘친 패키지 수를 기록합니다.
3. chroot의 `/run`은 runner의 것이 아닌 새 tmpfs입니다. 주석의 이유: "with /run/systemd/system absent the packages' scripts cannot reach the runner's systemd, and ischroot holds, as on any chroot." 패키지 스크립트가 runner 자신의 systemd를 건드리지 못하게 하는 것입니다.
4. harness CPU에서 `apt.systemd.daily update`를 `20260728T000000Z`의 archive에 대해 돌립니다.
5. 측정 단계: `phase upgrade-install -- sudo taskset -c "$MEAS_CPU" chroot "$r" … /usr/lib/apt/apt.systemd.daily install`. 이 명령 전체가 측정 CPU에 고정되고, `perf sched record -a`가 harness CPU에서 전체를 기록하며, taskstats listener가 측정 CPU에 등록됩니다.
6. 결과: 받은 수(4), 바뀐 수(4), 변경 집합의 SHA-256, "All upgrades installed" 여부 등을 `report`에 씁니다. `pooled.json`의 `also.state`에 반복마다 `'downloaded': '4', 'changed': '4', 'changed_sha256': '2c64508e…', 'uu.all_installed': '1'`이 남아 있습니다.
7. artifact `meas-background-upgrade-r<k>-full`을 올립니다.

## 10.6 기계 뽑기

`campaign/upgrade/machine-draws.md`는 job마다 무엇을 뽑았는지 적습니다. 요약은 "Full mode, runs #100–#105: 15 jobs, 9 drew the EPYC 7763 and landed (60 %), 6 were stopped by the machine gate — AMD EPYC 9V45 2, AMD EPYC 9V74 2, Intel Xeon Platinum 8370C 1, Intel Xeon Platinum 8573C 1"입니다. 표를 보면 반복 4는 run #100(9V45), #101(9V74), #102(9V74), #103(8573C)에서 네 번 걸린 뒤 #104에서 착지했습니다. workflow 문서의 loop 2단계는 같은 작업에서 gate에 걸린 job을 "the next index (identical work)"로 다시 띄우라고 하지만, batch가 이미 이름 붙인 번호는 예외입니다. "a batch's gated indices … are relaunched together in one push (2026-09-20 and 2026-09-25, 인지오's decisions): they are the indices the batch already named, and every one of them has to land for the batch." 반복 4는 첫 batch(1–5)가 이름 붙인 번호이므로 같은 번호로 착지할 때까지 다시 띄워졌습니다.

## 10.7 pool과 규칙

`background/pool.py`를 `--cpu-model "EPYC 7763"`으로 돌리면 아홉 반복의 `pooled.json`과 `results.md`가 나옵니다. 9.10 D45의 기록대로, 첫 batch(반복 1–5)에서 block per run은 통과했지만 run between voluntary blocks(±6.31 %)와 CPU 총량(±7.72 %)은 통과하지 못했고, pool이 아홉을 예측했습니다. 9.7 D26에 따라 반복 6–9를 한 batch로 더했고(run #105), 아홉에서 규칙이 섰습니다. `results/results.md`의 stability 표(8,303행 근처)는 이렇습니다.

| quantity | repeats | mean | cv | 95 % half-width | leave-one-out | needed at this spread | passes |
|---|---|---|---|---|---|---|---|
| upgrade-install run between voluntary blocks (µs) | 9 | 1797.7576 | 4.0% | ±3.1% | 1.0% | 6 | yes |
| upgrade-install block per run (µs) | 9 | 8.8975 | 7.8% | ±6.0% | 1.7% | 5 | yes |
| upgrade-install CPU total (µs) | 9 | 26384689.8889 | 4.9% | ±3.8% | 1.3% | 7 | yes |

block per run은 ±6.0 %로 5 %를 넘지만 통과입니다. 반폭의 절대값이 ±0.53 µs로 1 µs 바닥 안이기 때문입니다(7.2절). "leave-one-out"은 반복 하나를 뺐을 때 평균이 가장 크게 움직이는 정도이고, "needed at this spread"는 지금의 퍼짐이면 몇 번에서 통과했을지입니다. CPU 총량은 일곱 번이면 통과했을 퍼짐인데 아홉에서 멈춘 것은, batch를 예측치까지 한꺼번에 채웠기 때문입니다.

`pooled.json`은 같은 결과를 기계가 읽는 형태로 담습니다. 맨 위에 `tag: meas-ci:background:2026-10-01`과 `machine: EPYC 7763`, 그리고 `runs.upgrade` 아래에 `repeats: [1, …, 9]`, 반복마다 `cpu_model`(모두 "AMD EPYC 7763 64-Core Processor"), `kernel`(모두 `6.17.0-1022-azure`), `run_id`(예: 반복 1은 `36847549673`, 반복 2와 3은 `36847096521`, 반복 4는 `36848289469`, 6–9는 `36851095354`)가 있고, `stability` 아래에 위 표의 숫자들이 있습니다.

반복별 CPU 총량을 펼쳐 보면(9.14 reads R2) 25.559, 25.247, 25.563, 27.245, 29.155, 25.724, 25.413, 26.174, 27.381 s이고 평균이 26.385 s입니다. 기록은 여기서 한 가지를 더 밝힙니다. "repeats 4, 5 and 9 ran 6–14 % above the mean of the other six in identical work, `unattended-upgrade`'s own Python 21–50 % above them (repeats 4 and 5)." 같은 CPU 모델, 같은 작업인데 반복마다 6–14 % 차이가 있었고, 규칙은 아홉에서 그것을 흡수했습니다. 이것이 한 CPU 모델만 받아도 남는 퍼짐의 크기입니다.

## 10.8 기록과 release

결과는 세 곳에 남습니다.

- `measurement-campaign-record.md`의 "9.10 — `package-upgrade`" 절: 반복 1–9, 유효성, 15 job 중 9 착지와 걸린 모델, 첫 batch가 실패해 아홉으로 늘린 경위, 세 값의 표, 함께 보고한 것들(916 프로세스, 단계 동안 CPU 0.990–0.994, `localedef` 72.8–76.5 %, taskstats/perf 0.980–0.982).
- `task-9.10-scenarios-timelines/changelog.md`의 D45: 위 내용과 함께 release, fold-in, 다시 묶은 열한 파일, compile 결과(100개 artifact 중 24개가 바뀜, 파일별 demand 변화).
- GitHub release `meas-ci-background-2026-10-01`(2026-10-01T12:20:45Z 공개): D45의 "published on 인지오's go-ahead".

## 10.9 fold-in: `archetypes.yaml`에 들어가기

`batch_fold_in.py`가 `pooled.json`의 두 표를 읽어 `package-upgrade` entry의 `params`에 씁니다. 표는 6.6절의 형식(열 개 분위수, 최솟값, 최댓값, 열한 구간 평균)이고, 태그는 캠페인입니다.

```yaml
      upgrade_run:
        {dist: quantiles, p: [4, 4, 4, 4, 7, 60, 313, 707, 3863, 1041069], min: 3, max: 2667594,
         means: [3.404, 4, 4, 4, 4.932, 30.891, 149.47, 581.806, 1366.482, 62863.079, 1115870.066],
         sampling: per-iteration, source: "meas-ci:background:2026-10-01"}
```

이 표를 읽는 법을 하나 적어 두면, run의 중앙값(p50)은 7 µs밖에 안 되지만 p99.9는 1,041,069 µs(약 1 s)이고 최댓값은 2.67 s입니다. 짧은 프로세스 수백 개의 짧은 run 사이에 `localedef`의 긴 run이 섞여 있기 때문입니다. 그래서 평균(마지막 구간 평균 1,115,870 µs가 크게 끌어올림)이 1,798 µs가 됩니다. 이 극단을 버리지 않고 구간 평균으로 들고 다니는 것이 "a table's mean is the sample's mean"의 의미입니다.

entry의 `validation_stats`는 출처를 사람이 읽을 수 있게 펼칩니다.

- `referee: meas-ci`
- `run: "background:2026-10-01; repeats [1-9]; runs 36847096521, 36847549673, 36848289469, 36851095354"`
- `stats`: 세 값과 반폭, 반복별 범위, 프로세스 수, 반복 4, 5, 9의 차이.
- `scope`: "One observation (phase decision 2; 9.10 D3, D36-D38): the stock Ubuntu 24.04 unattended upgrade's install stage … Pinned to one CPU of a GitHub-hosted ubuntu-24.04 runner (4 vCPU AMD EPYC 7763, kernel 6.17.0-1022-azure), the rest of the machine idealised; the runner's agent processes share the measured CPU outside the process tree; no desktop session. … 9 same-machine repeats under the machine gate; the stability rule holds on all three values. Values are this software on this machine, not desktop truth (9.5 D10)."

`modeling_notes`는 우리가 그 위에 얹은 것을 밝힙니다. 예: "The stages' order and the process count are not carried: the loop draws runs independently, so the `localedef` runs … fall anywhere in the job rather than in one 20 s stretch." 실제 job에서는 `localedef`가 한 덩어리로 몰려 도는데, batch loop는 run을 독립적으로 뽑으므로 그 순서가 흩어진다는 것입니다(8.5절의 순서 위협과 같은 종류입니다). 또 "Another day's pending set is another job"이라고, 이 값이 2026-07-27이라는 하루의 업그레이드라는 범위를 적습니다.

**CPU 총량은 entry에 없습니다.** `package-upgrade`의 `binding_params`는 `[total_work]`이고, 개수나 총량 같은 binding 값은 library가 아니라 timeline이 담습니다(`archetypes.yaml` 머리말: "Counts never carry values here"). 그래서 26.385 s는 다음 단계, timeline으로 갑니다.

## 10.10 timeline과 compile

C7 counterpart들은 `dataset/timelines/coreset/c7.variant.yaml`이라는 파생 레시피에서 만들어집니다. 그 안에 이렇게 적혀 있습니다.

```yaml
                   arrive: 0s, bind: {total_work: 26.385s}, source: {total_work: "meas-ci:background:2026-10-01"}}
      - set-segments: [{from: 0s, to: 26.385s, mode: browsing,
```

`c2-p2b`는 `c2-pairs.variant.yaml`에서 `arrive: 60s, bind: {total_work: 26.385s}, source: {total_work: "meas-ci:background:2026-10-01"}`로 묶습니다. µs 단위 평균 26,384,689.89를 밀리초까지 반올림한 것이 26.385 s입니다. `bound-values.md`(9.10 D160)의 표는 이 값의 행을 "`total_work: 26.385s`, the job's CPU total | the unattended upgrade (`package-upgrade`) | (열한 파일) | `meas-ci:background:2026-10-01` | D45"로 적고, 9.18이 넣은 `lint_bound_sources`가 이 `source` map의 형식을 확인합니다.

이 값은 파일의 모양까지 정합니다. 9.10 D41에 따라 각 counterpart는 기준 파일의 처음 C초(C = 26.385 s)이고, 업그레이드는 0 s에 도착해 통째로 묶입니다. 기록된 이유: "on one lane a job of C seconds CPU is alive ≥ C seconds under every policy". CPU 하나에서 C초의 CPU가 필요한 작업은 어떤 scheduling 정책 아래서도 적어도 C초 동안 살아 있으므로, 파일의 모든 순간에 "원하지 않는 작업이 돌고 있다"는 라벨이 참이 됩니다. 측정값 하나가 실험 설계의 길이를 정한 사례입니다.

그다음은 compile입니다(timeline에서 canonical workload로 가는 포맷과 compiler는 3권이 다룹니다). 같은 timeline과 library와 seed는 같은 바이트를 내고, `dataset/build.manifest.json`이 그 해시를 고정합니다. 또 `dataset/replay/replay-package-upgrade.json.gz`는 trace-replay variant를 위해 한 반복(27.4 s, run 14,699개, CPU 27.245 s, 프로세스 916개 — 반복 4의 CPU 총량과 같습니다)의 실제 run 순서를 담고 있습니다.

## 10.11 이 숫자가 주장하는 것과 주장하지 않는 것

정리하면, 26.385라는 숫자는 다음을 주장합니다. "2026-07-27의 glibc 보안 업데이트를 영어 기본 층의 chroot에 설치하는 stock 무인 업그레이드의 설치 단계는, GitHub-hosted runner의 AMD EPYC 7763 CPU 하나에 고정되었을 때, 아홉 번의 독립된 측정에서 평균 26.385 s(95 % 반폭 ±3.78 %)의 CPU를 썼다."

그리고 다음은 주장하지 않습니다.

- 데스크톱에서 업그레이드가 얼마나 걸리는가(다른 CPU, 다른 날의 업데이트, init이 있는 실제 시스템).
- 다른 날의 업그레이드(아무것도 없는 날은 `unattended-upgrade` 혼자 몇 초, 커널이 오는 날은 커널과 initramfs가 더해짐 — `modeling_notes`).
- 업그레이드가 쓰는 nice 19의 일을 낮은 우선순위로 다룬 것(9.11 D20: `apt-check`와 `dpkg`의 nice 19 일이 pool CPU의 2.67 %이며, nice는 담지 않으므로 이 몫도 보통 우선순위로 돕니다).
- 그 단계 순서(위의 `modeling_notes`).

이 목록이 결정 1의 "whole claim — object, unit, statistic, scope and population"을 측정값에 적용한 모습입니다. 대상은 무인 업그레이드의 설치 단계, 단위는 CPU µs, 통계량은 아홉 반복의 평균(반복별 값의 t 구간), 범위는 그날의 업데이트와 chroot와 runner, 모집단은 EPYC 7763 runner의 job들입니다.

---

# 11장 · runner가 볼 수 없는 것

이 장은 "결정 5가 'stated limitation'이라 부른 그 한계는 구체적으로 무엇이고, runner가 볼 수 없는 것은 각각 어디서 왔는가"라는 질문에 답합니다. 6장부터 10장이 "무엇을 쟀는가"였다면, 이 장은 "무엇을 재지 못했는가"입니다. 이 질문은 이득 주장(1.1절)의 범위를 정합니다.

## 11.1 장소의 목록

`measurement-overview.md` §11은 측정값이 무엇을 주장하는지 한 문단으로 적습니다. "Every measured value is this software on this machine: a GitHub-hosted runner, one pinned AMD EPYC 7763 core shared with the runner's own agent, no GPU, no display refresh, no sound device, no human, one CPU model over one period. The values are not desktop truth. The precision stated is precision on that configuration — reproducibility, a separate property from representativeness. Real-desktop validation is deferred." 디스플레이는 그 아래 항목들이 따로 적습니다(응용은 Xvfb의 X11 client로, 세션은 Wayland 세션에서 잼).

항목별로 풀면 이렇습니다.

| runner에 없는 것 | 그 결과 | 기록 |
|---|---|---|
| 실제 화면과 주사율(vsync) | Chromium은 vsync 없이 기본 60 Hz 타이머로 compositor를 돌림: 60 Hz의 주기는 있으나 실제 화면의 위상은 없음. Qt Quick의 threaded render loop는 software rasteriser가 주지 않는 blocking buffer swap에 맞춰 돌아 렌더링 경로의 wake 빈도가 과대 | 9.5 D24 |
| GPU | `--disable-gpu`로 래스터화와 합성을 CPU 스레드가 하므로, 그 스레드들의 run 길이가 GPU 데스크톱보다 길게 잡힘. 얼마나 긴지는 어떤 출처도 말하지 않음 | 9.5 D24 ("by an amount no source states") |
| 소리 장치 | mpv는 `--ao=null`로, 오디오 서버를 거치지 않음. Azure 커널에 `CONFIG_SND`가 없음 | 9.5 D11; 9.9 D8 |
| 사람 | 입력은 기록을 재생한 것(SWELL-KW 키만, 포인터 없음). GIMP와 Kdenlive는 관찰된 입력이 없어 스크립트로 만든 포인터 반복(design) | 9.5 D4, D5, D28; `measurement-overview.md` §4 |
| 여러 CPU, 다른 CPU 모델 | 한 CPU에 고정, 한 모델(EPYC 7763), 한 기간 | 9.5 D21; 9.6 D10 |
| 데스크톱의 디스플레이 서버 | 응용 entry는 Xvfb의 X11 client로 잼(예: Kdenlive의 `QXcbEventQueue`, mpv `--vo=x11`), 세션 entry는 Wayland 세션에서 잼; core 파일 가운데 둘을 함께 담은 것은 없음(생성 층의 62개 파일은 idle 세션의 이름을 응용 옆에 두는 design 조합, `building-plan.md` §3a); Wayland 데스크톱에서 각 프로그램이 어떻게 도는지는 관찰하지 않음 | 9.10 D172 (D28의 X11 문장을 다시 씀); 생성 층은 인지오의 결정(2026-10-16) |
| 실시간 우선순위 부여 | 헤드리스 runner에서 RTKit(데스크톱 프로그램에 실시간 우선순위를 나눠 주는 서비스)이나 세션에 실시간 스레드를 청하는 프로그램은 venue가 주는 만큼만 받음: 통화의 오디오 worker도 NORMAL nice 0("no RTKit in the venue") | 9.11 class census (`classes/audit.md`) |
| 사용 중인 데스크톱 세션 | 세션은 "terminal idle state"(화면이 잠기고 꺼짐)에서만 잼; 사용 중이거나 막 떠난 데스크톱은 덮지 않음 | 9.9 D9 ("a desktop in use or just left is not covered") |

> **왜 이렇게 정했나.** 9.5 D24의 장소 문장들은 9.5 follow-ups spec decision 12에서 왔습니다. "No archetype value changes: under phase decision 2 no literature figure is folded into a measured archetype." 디스플레이와 GPU의 효과를 문헌에서 찾아 값에 곱하지 않고, 오차의 **방향**만 출처와 함께 적는다는 것입니다. 검색 기록(`search/S8-display-gpu.md`)은 "no measurement in any class of a Linux desktop application's CPU-side wakes with and without a real display or GPU"를 찾았습니다. 값에 곱할 숫자가 어디에도 없었던 것입니다.

## 11.2 runner가 볼 수 없어서 다른 데서 온 것

결정 5는 "What a runner cannot observe comes from literature or public traces, or to 인지오 as a decision"이라고 했습니다. 실제로 어디서 왔는지 항목별로 봅니다.

**게임의 task chain.** runner에서는 Proton(Windows 게임을 Linux에서 돌리는 Valve의 호환 계층) 게임을 돌릴 수 없습니다. `game-task-chain`의 `validation_stats.reason`이 이유를 적습니다. "a CI runner cannot observe a Proton game's Wine, DXVK or audio structure (no GPU; Proton runs only under the Steam client), so no own measurement referees it." 그래서 LAVD 발표 슬라이드 12–17장을 "one observation"으로 받아들였고(9.4 D1, 인지오의 결정), frame 주기는 Steam Deck 사양(`steamos-refresh`)에 기댄 design입니다. 이 entry의 심판(referee)은 `none`이며, "validation against LAVD would be circular — LAVD is also the parameter source"라고 적혀 있습니다. 2026-10-10 감사는 이것을 이렇게 평가했습니다. "`game-task-chain` paces 8 of 51 files (3 judging: c2-p2a, c2-p2b, c7-gaming) on a talk deck." 2026-10-11 인지오의 결정(감사의 A3 해결)은 "resolved as is. The figures stand as the talk's reported values; the chain-x1.2 and chain-x1.4 variants are the sensitivity check."였습니다.

**사람의 입력 간격.** 9.5의 S4 기록은 "Not observable on a runner: human inter-arrival is replay input, not a measurement"라고 적습니다. 사람의 타이핑 시각은 runner가 만들 수 없으므로 공개 데이터(SWELL-KW)를 재생합니다(user-side 값은 어느 플랫폼에서 와도 된다는 규칙, 6.7절).

**어떤 프로그램들이 함께, 얼마나 오래 도는가.** 9.10의 검색은 네 부류에서 "Which applications run together on Linux desktops at population scale, and for how long each stays open"을 찾지 못했습니다(`search/candidates.md`의 "Not found across classes"). 그래서 task set, 순서, 길이는 design입니다(9.10 D2, D29, D31; 3.4절).

**탭 수.** 사용자가 탭을 몇 개 여는가는 runner가 볼 수 없습니다. 9.10 D15는 Mozilla의 공개 telemetry(GLAM, `glam`)에서 Linux Firefox의 "median per-client peak of concurrent tabs 4.67, so five tabs"를 가져왔고, 그 다섯 탭이 Chrome에서 몇 개의 renderer가 되는지는 runner에서 직접 셌습니다(`meas-ci:desktop:2026-10-04`, 숨은 renderer 4개). 사용자 쪽 값은 공개 데이터에서, 프로그램 쪽 값은 Linux 측정에서 온 조합이며, `references.md`의 `glam` 항목은 "A user-side value from Firefox, not Chromium … the median of a per-client peak errs high for a random instant (D15's stated choice)"라는 한계를 함께 적습니다.

**Steam 계정이 필요한 것.** 9.8 D6은 Steam 계정을 쓰지 않기로 했고, Steam client는 로그아웃 상태로 쟀습니다. 게임 download는 Steam client 대신 SteamCMD로 쟀고, `steam`의 download는 그것에 "by stated approximation"으로 묶습니다(9.7 D4). Steam의 shader 사전 캐싱(`fossilize`)은 "not measurable on the runner (9.4 S4: no headless Steam client route)"로 감사의 backlog에 남았습니다.

**데스크톱의 cgroup slice.** 실제 Ubuntu 데스크톱에서 Tracker는 `background.slice`에, 응용은 `app.slice`에 놓입니다. 9.11 D16은 그 무게(CPUWeight 30 대 100)로 색인기가 편집기와 함께 바쁠 때 약 23 %의 CPU를 받는다고 읽었습니다. simulator의 executor는 idle class를 "다른 class가 실행 가능하면 절대 돌지 않음"으로 다루므로, 색인기의 방해가 실제보다 작게 나타납니다. 기록은 이것을 "the headroom the indexer files can show is understated, against the hypothesis"라는 한계로 적었습니다.

## 11.3 fidelity map: 무엇이 얼마나 현실에 가까운가

2026-10-10 감사의 auditor D(real-world fidelity)는 차원마다 현실에 얼마나 가까운지를 등급으로 매겼습니다. 등급 낱말은 FAITHFUL(충실), PROXY(대리 — 같은 것은 아니나 그것을 대신하는 측정), STYLISED(양식화 — 일부 성질만 보존), DESIGN(설계), UNGROUNDED(근거 없음)입니다. 감사 문서의 표를 옮깁니다.

| 차원 | 등급 | 틈 |
|---|---|---|
| CPU behaviour, 27 measured kinds | PROXY, strong | one pinned vCPU of an EPYC 7763 Azure VM under Xvfb, no GPU/refresh/sound, under perf; measured venue effects 0.72–0.98 tracing, ×1.144 huge pages, Xeon vs EPYC 0.50–0.72× |
| game chain | STYLISED → DESIGN | 260/1650 µs slide anchors, lognormal by convention, 16-stage chain ours, 60 Hz from a Steam Deck spec, demand by `lane_share` |
| wake timing structure | STYLISED | rate/gap/run tables within 2 %; order and co-waking lost |
| input stimulus | PROXY, large | SWELL-KW 2012 Windows lab, keys only, 15.6 ms quantised; Word stream drives both LibreOffice and VS Code; no pointer input; none for GIMP/Kdenlive and six other modes |
| task mix per scenario | DESIGN | 9.10 D2 |
| co-occurrence / order | DESIGN / UNGROUNDED | no Linux-desktop co-occurrence observation found in four source classes |
| durations | DESIGN | compressed event time; 60 s interactive files; counterparts 26.385 s |
| process population | PROXY (names faithful) | 1–26 tasks per file vs ~300 system-wide; stand-ins (SteamCMD, WebRTC loopback, Element, mpv); X11 under Xvfb; no RT threads |
| hardware / scale | PROXY → DESIGN | one server vCPU measured, one lane simulated; "eight-thread desktop" by convention; only the chain is lane-scaled; venue sweep ×0.8–1.25 narrower than the measured 0.50–0.72× cross-CPU spread |
| scheduling classes | FAITHFUL class / DESIGN rule | read from source + /proc; strict idle = 0 % vs `background.slice` ~23 % |

같은 감사는 결론을 이렇게 적었습니다. "At the individual program: more faithfully measured than any desktop-scheduler workload the repository cites (27 of 28 kinds on the real program, 5–77 repeats, raw traces released). Above the individual program: task mix, co-occurrence, order, durations, core count, display/GPU/audio path and the human are designed, proxied or absent. A pass on RQ0 claims that contended single-core situations composed from real program behaviour exist where the right configuration differs measurably; not how often desktops are in them, how large the benefit is on a multi-core GPU desktop, or how a live user would experience it."

이 문단이 이 권 전체의 결론에 가깝습니다. 프로그램 하나하나의 수준에서는 이 데이터셋이 매우 단단하게 측정되어 있습니다. 그 위의 수준, 곧 무엇이 함께 얼마나 오래 도는가, 몇 개의 코어인가, 화면과 GPU와 소리와 사람은 설계이거나 대리이거나 없습니다. 그래서 RQ0의 통과가 말할 수 있는 것은 "실제 프로그램의 행동으로 조합한, 경쟁이 있는 단일 코어 상황 가운데 올바른 설정이 측정 가능하게 다른 상황이 존재한다"까지입니다.

2026-09-20 memo §5는 이득 주장의 한계를 두 가지 방식으로 다룰 수 있다고 적었습니다. "Either carry that scoping into the paper, or run one bounded comparison against a real desktop with a display and a GPU and report the offset, which converts the limitation from unbounded to measured." 인지오가 2026-10-16에 앞의 길을 골랐습니다(9.15 작업 목록 W-0753). 범위를 논문에 싣습니다. `docs/research-claims.md`의 "What is not claimed"에 한 항목이 있습니다. scheduling 결과가 다른 CPU나 다른 기계 구성으로 옮겨 간다고 주장하지 않으며, 모든 CPU 값은 hosted runner(Xvfb, GPU 없음, 소리 장치 없음, 사람 없음)의 AMD EPYC 7763 코어 하나의 것이라는 항목입니다. `measurement-overview.md` §11의 "Real-desktop validation is deferred"는 그대로이고, 실제 데스크톱과의 비교는 열지 않습니다. 2026-08-26 grill D8이 팀원의 실제 데스크톱 측정("meas-live")을 뺀 결정(이유: "No teammate Linux desktops known")도 그대로입니다. 같은 날 인지오는 그 대신 약속했던 수집·개인정보 제거 도구도 거두었습니다(4.4절 B7).

---

# 12장 · 연구 조각을 연구로 읽기: 9.4부터 9.12까지

이 장은 "Phase 9의 아홉 연구 조각(research slice)은 각각 어떻게 찾았고, 무엇을 찾았으며, 무엇을 들고 인지오에게 왔는가"라는 질문에 답합니다. 결과로 나온 archetype 값들은 archetype library를 다루는 2권이, timeline 쪽 결과는 포맷과 compiler를 다루는 3권과 51개 coreset 파일을 다루는 4권이 다루므로, 이 장은 **과정으로서의 연구**에 집중합니다. 조각마다 같은 틀로 적습니다: 무엇을 맡았나, 네 부류의 검색이 무엇을 찾았고 무엇을 못 찾았나, 그래서 무엇이 인지오의 결정으로 왔나.

## 12.1 조각이 일하는 방식

`_dev/research/jioh/research-slice-workflow.md`(2026-09-13, 9.4를 시작하며 고정)가 모든 조각의 틀입니다.

**경계.** "A domain slice (9.4–9.9) owns the archetypes of its domain: every parameter of each archetype, its bindings, its modeling notes, and the tags on its values." timeline 내용(task set, 동시 출현, 순서, 개수, 프로세스 이름, 시나리오 구조)은 어느 영역을 그리든 9.10의 것입니다. archetype 안에 있던 개수는 영역 조각의 결정으로 archetype을 떠나고, 그 뒤 timeline이 담는 숫자는 9.10이 정합니다. registry 항목은 그것이 받치는 주장을 따라갑니다.

**네 단계.**

1. **Scope card.** 2026-09-13 검증 기록(`claims.md`, `topics.md`, memo의 발견)에서 그 조각의 할 일 목록을 뽑습니다. 항목마다 현재 값, 현재 태그, 검증 판정, 그리고 종류(source claim, convention, arithmetic, placeholder, design). "인지오 reviews the card before any search."
2. **Search.** 항목마다 결정 4의 네 부류. 읽는 이는 `topics.md`처럼 중립적인 주제만 받고 저장소의 현재 값은 받지 않습니다. 읽기마다 사본(URL 또는 커밋, 판본, 날짜, 로컬 경로), 원문 구절과 위치, 항목 목록에 대한 덮음(coverage) 진술을 적습니다. 검색 기록은 검색어, 장소, 결과를 적습니다. 출처 사본은 9.1의 결정대로 로컬에만, gitignore.
3. **Decision session.** "Items are brought to 인지오 one at a time in chat with their candidates, each candidate's coverage, and a recommendation with its reference." 결정은 내려지는 대로 적용합니다. `archetypes.yaml` 수정, 데이터셋 다시 compile, changelog 항목과 함께 커밋. "The changelog is the slice's decision record; no task spec is written."
4. **Hand-off.** changelog가 9.10, 9.13, 9.14, 9.15로의 인터페이스이고(항목마다 "Hands to …"), 검색 기록과 읽기와 changelog가 9.16 exit audit으로의 인터페이스입니다.

**기록.** 조각마다 `_dev/research/jioh/task-<N.M>-<domain>/` 폴더에 `scope-card.md`, `search/`(`input.md`, `S1-literature.md`, `S2-project-docs.md`, `S3-traces-datasets.md`, `S4-ci-observability.md`, `candidates.md`), `sources/`(gitignored), `changelog.md`, 측정을 한 조각은 `campaign/`이 있습니다. 공개 문서(`docs/`, `dataset/README.md`)에는 Phase 9의 고친 이력을 쓰지 않습니다. "They describe the final state; 9.15 brings them there."

조각의 changelog에 적힌 결정 수를 세면(`grep -c '^## D'`) 9.4가 10(D9가 두 번 적혀 있어 실제로는 D1–D9), 9.5가 99, 9.6이 38, 9.7이 41, 9.8이 38, 9.9가 48, 9.10이 174(D1–D174), 9.11이 34, 9.12가 116입니다. 9.10은 2026-10-01부터 2026-10-07까지 일주일 만에 174개입니다.

## 12.2 9.4 게이밍

**맡은 것.** `game-task-chain` 하나.

**찾은 것.** `search/candidates.md`의 "Observations that exist" 표는 관찰(숫자가 있는 모집단, trace, run)을 문서와 구분합니다. S1(문헌)은 LAVD의 OSS NA 2024 슬라이드 12–17장(이름 없는 게임, 이름 없는 기계; 그림은 적어도 세 프로세스 트리에서 옴), 같은 그림을 쓴 LPC 2024 슬라이드, 그리고 Android(Pixel 8의 Angry Birds)와 Windows 연구를 찾았습니다. S3(공개 trace)은 sched-ext/scx 저장소의 issue #234와 #296에 붙은 `scx_lavd` 표본 로그(Helldivers 2, Apex Legends, Diablo III, StarCraft II)를 찾았습니다. 이것들은 다른 scheduler(`scx_lavd`) 아래의 EWMA 값이고 자주 스케줄되는 task 쪽으로 치우친 표본입니다. S2(문서)는 Valve의 SteamOS 3.2 공지(60 Hz 기본, "60hz = 16.66ms/frame"), gamescope의 frame 제한 메커니즘, DXVK와 MangoHud의 제한기를 찾았습니다. S4(runner)는 Proton 게임을 runner에서 돌릴 길이 없음(GPU 없음, Proton은 Steam client 아래에서만)을 확인했습니다.

**못 찾은 것.** Proton 게임의 frame 주기를 task 구조와 묶은 관찰, 상위 30–40개 밖의 task를 설명하는 관찰.

**인지오의 결정으로 온 것.**

- **D1(2026-09-13).** LAVD 슬라이드를 "one observation"으로 유지. 결정 2의 기본값이 아니라 인지오의 결정입니다(3.3절). 받아들이지 않은 대안: 공개 `scx_lavd` 표본 로그, 우리의 네이티브 게임 측정.
- **D2.** `frame_period`의 태그를 `steamos-refresh`로, design으로 표시(4.4절 A2).
- **D3.** archetype을 chain만으로. `n_tasks`와 tail 파라미터 삭제(placeholder였음). 게임 파일마다 284개 tail task가 사라지고 demand가 바뀜(예: `c1-gaming` single 1.46 → 1.30).
- **D4.** wineserver를 chain의 구성원으로, 260 µs(`lavd-ossna24:s13`).
- **D5.** `chain_length` 16에 위치 `s12`를 붙이고 "design within a source range"(슬라이드의 15–20 안의 한 점).
- **D6.** `per_schedule_run`의 두 기준점 260/1,650 µs는 슬라이드의 이름 붙은 예시 둘이며 통계량은 표시되어 있지 않음, lognormal과 p05/p95 읽기는 우리 것이라고 notes에 명시.
- **D9(2026-09-17).** 슬라이드의 "per-schedule runtime"을 wake 하나의 RUN으로 읽는 것이 아래쪽으로 치우친다는 것을 한계로 명시. 크기도 같은 관찰에서 경계를 지었습니다(선점이 스케줄 사건의 25–30 %이므로 wake당 평균 약 1.4번의 스케줄). 기준점을 1/0.71로 늘리는 대안은 받아들이지 않았습니다(선점이 run 길이와 무관하다고 가정하게 되므로).

9.4는 측정 캠페인이 없는 유일한 영역 조각입니다. 그래서 이 조각의 결정들은 "문헌 하나를 어떻게 정직하게 쓰는가"의 예입니다. 값을 거의 바꾸지 않았지만, 각 값이 출처의 무엇이고 무엇이 우리 것인지를 하나씩 갈랐습니다.

## 12.3 9.5 상호작용과 타이핑

**맡은 것.** `desktop-interactive`(편집기, 워드프로세서 등 모든 상호작용 프로그램을 한 entry로), 그리고 경계 판단으로 `audio-playback`, `video-playback`.

**찾은 것.** 입력 간격에 대해 S1과 S3는 많은 타이핑 데이터를 찾았습니다(136M Keystrokes, Roeser의 OSF 데이터, How-We-Type, CMU 비밀번호, KeyRecs, SWELL-KW 등). 그 가운데 응용 프로그램 이름과 함께 자유 작문의 키 입력 시각을 담은 것은 SWELL-KW였습니다. 입력 하나당 CPU에 대해서는 문헌에 Linux 관찰이 있었지만 모두 2000–2004년의 100–664 MHz 기계였습니다(Flautner, Tsafrir/Etsion 등). S4는 runner가 아홉 프로그램을 Xvfb에서 띄우고 재생하고 perf로 기록할 수 있음을 탐침으로 확인했습니다(`meas-probe.yml`, 재생 오차 p99 1.24 ms).

**인지오의 결정으로 온 것(골라서).**

- **D2.** `desktop-interactive`를 응용 프로그램마다 나눔.
- **D3.** 값은 runner 측정 캠페인에서. 이유는 3.6절("unable to back a current application").
- **D4.** 재생하는 타이핑은 SWELL-KW.
- **D10.** runner의 절대값을 출처 주장으로(6.1절).
- **D26–D30.** 같은 기계 반복, 최소 다섯, 모든 담는 값에 규칙.
- **D28, D65, D72, D79.** 키만 재생(7.4절).
- **D57.** between-sessions 예외(7.5절).
- **D81, D82.** 자극 민감도 점검을 반복별로, 추적 없는 대조군(8.2–8.3절).
- **D88.** 멈춤의 낙관성을 모의실험하고 단서로(7.6절).

이 조각은 99개의 결정으로 가장 길었습니다. 그 이유의 상당 부분은 측정 방법 자체를 이 조각이 처음 만들었기 때문입니다. CPU 하나 고정과 wake의 정의(D21), 같은 기계 반복(D26), 태그 형식(D27), 반복 최소(D29), 규칙이 덮는 값(D30), settle(D34, D35), 표의 평균(D71, D78) — 이 결정들이 workflow 문서로 모여 다른 조각들의 공통 규칙이 되었습니다. 결과로 아홉 개의 측정 archetype(`office-writer`, `code-editor`, `mail-client`, `web-browser`, `image-editor`, `video-editor`, `video-player`, `audio-player`, `video-call`)이 세 개의 montage entry를 대체했습니다(D19, 뒤에 D70으로 다시 생성). TODO의 9.5 줄은 "real-desktop validation a stated limitation"으로 끝납니다.

## 12.4 9.6 컴파일

**맡은 것.** `compiler-child`, `build-orchestrator`, `cpu-batch`.

**찾은 것.** S1과 S3는 build의 숫자를 여럿 찾았습니다. rr 논문(DynamoRio, 2,430), Antfarm(ATC '06, bash 빌드의 프로세스 생성 815/748), Gouicem 등(ATC '20, 80코어 kernel build의 단계 구조), MOSBENCH의 gmake, Brendan Gregg의 1초짜리 `perf sched` 기록, Debian과 Fedora의 kernel 빌드 로그, kcbench, Phoronix 결과 등입니다. 그러나 어느 것도 "CPU 하나에 고정된 kernel build에서 역할별 프로세스의 CPU와 wake"를 주지 않았습니다. S4는 runner에서 linux-6.6 defconfig를 `perf sched record`와 taskstats로 잴 수 있음을 확인했고, RunsOn의 표본에서 같은 runner 라벨에 CPU 모델이 섞인다는 것도 찾았습니다(S4-19).

**인지오의 결정으로 온 것(골라서).**

- **D1.** 9.5의 두 규칙(CPU 하나 고정, 반응 쪽 값은 Linux 관찰에서만)을 모든 결정에. 1990년대 UNIX 수명 연구, Windows XP 안티바이러스 연구, 2006년 Antfarm, 1999·2006년 LKML 글은 후보가 아니라 맥락.
- **D2.** 단위는 make job 하나 = 역할별 프로세스 사슬(4.4절 B3).
- **D3.** 관찰은 perf sched와 taskstats를 함께(6.2절).
- **D4.** `-j8`과 `parallelism_cap` 기본값 8: "design: the eight-thread desktop".
- **D10, D11.** CPU 모델 하나, machine gate, 규칙이 반복 수를 정함(6.2절, 7장). 이 두 결정이 그 뒤 모든 캠페인의 틀이 되었습니다.
- **D12–D16.** Tracker의 전체 재색인을 별도 entry로 뺐다가(D12–D15) 같은 날 되돌렸습니다(D16). 포화도를 프로세스 수명이 아니라 job 동안으로 다시 계산하자 재색인도 포화된 일괄 작업이었기 때문입니다. 기록은 D12의 숫자가 harness의 멈춤 규칙(상태 질의 세 번)에서 온 인공물이었다고 적습니다. 결정이 틀렸을 때 그것을 지우지 않고 "withdrawn"으로 남기는 기록 방식의 예입니다.
- **D29.** machine-spread 예외(7.5절).

## 12.5 9.7 백그라운드와 IO

**맡은 것.** `io-stream`, `network-bulk`, `background-crawler`.

**찾은 것.** S1과 S3는 rsync와 cp의 비교(LWN 2010), Gregg의 `tar` off-CPU 분석, 압축 도구 비교, borgbase의 borg/restic 벤치마크, restic과 borg의 issue들, GNOME LocalSearch와 KDE Baloo의 버그 리포트, Valve의 Steam download 통계, Linux Steam의 content log, ClamAV 검사 요약 등을 찾았습니다. 모두 특정 프로그램의 특정 상태에 대한 단편이고, 어느 것도 entry 전체를 한 관찰로 덮지 않았습니다. 그리고 결정적으로, 묶인 프로그램들(borg, 7z, Steam download, Thunderbird send)의 문서화된 구조가 Phase 2가 잰 프로그램들(rsync, wget)과 달랐습니다.

**인지오의 결정으로 온 것(골라서).**

- **D1.** `io-stream`과 `network-bulk`를 묶인 프로그램마다 나눔. 이유: "the bound programs' documented structure differs from the programs `meas-ci:cli:3` measured"(borg는 한 프로세스, 7-Zip은 기본 다중 스레드, Steam은 암호화된 1 MB chunk와 여러 연결 등).
- **D2.** 새 캠페인, perf sched와 taskstats에 socket 호출의 `perf trace`를 더함. `strace`는 호출마다 tracee를 멈추므로 받아들이지 않음.
- **D4.** Steam download는 SteamCMD로 관찰, `steam`은 그것에 stated approximation으로 묶음.
- **D5.** `background-crawler` 은퇴. 이유: 어떤 timeline도 묶지 않았고, 값은 색인하지 않은 miner의 관리 wake에 `updatedb`의 duty를 곱한 것이었으며(X7), 일상적 색인기의 주기를 담은 관찰이 없음.
- **D7, D10, D11.** 입력과 링크: Mahoney의 10 GB 세트, Valve 통계의 바이트 가중 중앙값 121.0 Mbps, `fq_codel`.
- **D26.** pool의 예측치까지 batch로 더하기(인지오의 결정, 7.4절).
- **D36.** 캠페인 자신의 점검은 허용 오차가 아니라 자기 반복별 비율의 구간으로 읽음(9.5 D81이 같은 방식을 받음).

그 뒤 9.10이 이 조각의 `file-backup`(borg)을 Déjà Dup(`incremental-backup`)으로 바꿨고, 지금 library에는 9.7의 `file-archiver`와 `game-download`가 남아 있습니다.

## 12.6 9.8 브라우저와 통신

**맡은 것.** `electron-comms`(Chrome renderer, Steam helper, Discord, Zoom, Thunderbird를 한 entry로 묶고 있었음; 125개 task).

**찾은 것.** `candidates.md`의 요약이 정확합니다. "None is a per-wake distribution; none is a pinned single-core run." Slack/Discord/Skype 통화의 1 Hz CPU 측정(Ubuntu 22.04), renderer 재사용 임계(Debian 8, Chromium 53), Chrome의 Windows 현장 데이터, Chromium issue들의 유휴 renderer 읽기, Zoom과 Discord 포럼의 유휴 CPU, Element의 병리적 상태, Steam client의 유휴 전력 등이 있었지만 모두 산문 읽기나 병리 상태였습니다.

**인지오의 결정으로 온 것(골라서).**

- **D1.** `electron-comms`를 묶인 프로그램마다 나눔. 이유는 측정 감사의 X4: 그 entry의 두 값은 관찰된 어떤 프로세스도 기술하지 않았음(Element 주 프로세스와 helper 사이의 기하 중심).
- **D2.** Chrome renderer는 browser task에 합치지 않고 자기 entry를 가짐. 이유: "the number of independently schedulable entities is a first-order property of a scheduling workload".
- **D6.** Steam 계정은 쓰지 않음("No account is used, and none may be"), 근거로 Steam Subscriber Agreement §4.C와 §1.C(사본의 SHA-256까지 기록). client는 로그아웃 상태로 측정.
- **D17, D18.** run 평균의 machine-spread 예외를 class 단위로(7.5절).
- **D24.** 모든 착지를 `<index>@<run id>`로(7.1절).
- **D27.** renderer residual을 sparse component로.

## 12.7 9.9 데몬과 세션

**맡은 것.** `system-daemon`(systemd 계열, dbus, cron 등 서버 데몬의 값으로 `gnome-shell`, `Xorg`, `pipewire`까지 묶고 있었음).

**찾은 것.** `candidates.md`: "None is a per-wake distribution; none is a pinned single-core run; none holds a system service and a session process of one idle desktop in per-process rows." Intel의 2013년 PowerTOP 백서, OLS 논문들, 포럼의 PowerTOP 출력, 버그 리포트의 병리 상태 등이 있었습니다.

**인지오의 결정으로 온 것(골라서).**

- **D1.** 시스템 서비스와 세션 프로세스를 나눔. 이유: "the two populations differ in every class searched"(서비스는 타이머와 사건으로 깨고, Mutter의 frame clock은 화면이 꺼지면 IDLE, PipeWire는 유휴 node가 멈추면 멈춤 등).
- **D8, D9.** Ubuntu 데스크톱 세션 하나를 runner에서 새로 측정, 사람이 없는 "terminal idle state"에서.
- **D27.** wake마다 원인을 trace를 따라 추적하고, 관찰한 데스크톱 밖의 원인(데스크톱 manifest에 없는 패키지, harness)에서 온 wake는 component에서 뺌. 예: pid 1의 wakeup 행 7,943개 중 54.4 %가 runner 이미지에 있던 `php-fpm8.3`(10.001 s마다)이었습니다. 이것을 빼지 않았다면 `service-manager`의 wake 빈도는 runner의 PHP 설치를 잰 것이 되었을 것입니다. 이 결정의 "Hands to 9.16"은 "9.5–9.8 ran beside the same `php-fpm` and workflow loops"입니다. 다른 캠페인들도 같은 runner의 같은 배경 위에서 돌았으므로, exit audit이 확인할 거리입니다.
- **D32 → D47.** sysstat의 수집기를 데스크톱 밖으로 뺐다가(D32, 2026-09-25) 다시 데스크톱의 것으로 되돌렸습니다(D47, 2026-10-01). 데스크톱 이미지(`casper/minimal.squashfs`)가 `sysstat.service`를 켜 둔다는 것을 ISO를 직접 읽어 확인했기 때문입니다.

## 12.8 9.10 시나리오와 timeline

**맡은 것.** timeline의 모든 현실 주장(task set, 동시 출현, 순서, 개수, 프로세스 이름, 시나리오 구조)과 시나리오 카탈로그, 그리고 timeline이 묶는 일괄 작업의 크기.

**찾은 것과 못 찾은 것.** `search/candidates.md`의 "Not found across classes"가 이 조각의 핵심 발견입니다. 몇 줄을 옮깁니다. "Which applications run together on Linux desktops at population scale, and for how long each stays open", "A Linux focus log at sub-minute resolution from real users", "A Proton game's full thread inventory in normal play", "The share of Linux desktop sessions on X11 against Wayland", "An unasked anti-virus scan, transcode, render or training run on a desktop", "The sizes of transcodes, renders, ML runs, local compiles and archives users start themselves". 가장 가까운 것은 SWELL-KW(Windows 실험실)와 BEHACOM(분 단위 전경 프로그램, 12명 중 4명이 Linux)이었습니다.

**인지오의 결정으로 온 것(골라서).**

- **D1.** 닿을 수 없거나 유료인 문헌은 뺌(`zhang-chb15`; 3.2절).
- **D2, D29, D31.** task set, arc의 순서, 보정 크기는 design(3.4절).
- **D3, D4, D5, D8, D10, D11, D12.** 일괄 작업을 실제로 존재하는 stock 작업이나 정의된 작업으로 바꾸고 각각 runner에서 측정: 무인 업그레이드(10장), NVIDIA 모듈의 DKMS 자동 설치, Tracker의 첫 색인(HippoCamp 데이터셋의 `Bei` 트리, 875 파일, 40,662,407,070 B를 `~/Documents`로), Déjà Dup의 예약 증분 백업, Kdenlive 내보내기, CpsMark+가 정의한 HandBrake 변환, PyTorch MNIST 예제.
- **D15, D16.** 탭 수는 GLAM에서, renderer 수는 측정에서; 브라우저 창은 하나, `renderer-visible` entry는 library에서 빠짐.
- **D17.** 일괄 작업은 측정된 전체로, 파일 길이가 따라감.
- **D32.** timeline의 bound value에 출처나 꼬리표(2.6절).
- **D33, D34, D35.** 카탈로그는 데이터셋이 묶는 것만, 각 줄이 성립하는 존재 주장으로; registry 항목의 정리; naturalistic generator의 근거와 "부정적 결과"를 출처에 맞게 다시 진술.
- **D143–D158.** span probe(8.4절).
- **D172.** X11/Wayland 문장(11.1절).

이 조각은 7개의 백그라운드 캠페인, Chrome 탭 캠페인, launch 캠페인, Kdenlive 유휴 캠페인, 숨은 renderer 캠페인, span probe, 세션 옆 업그레이드 탐침을 돌렸습니다(9.2절의 release 표). 결정 수가 많은 이유는 timeline 하나하나가 여러 entry와 크기를 묶고, 각 크기를 측정으로 바꿀 때마다 파일 길이와 짝과 판정이 따라 움직였기 때문입니다.

> **열린 자리.** 9.10의 검색이 동시 출현과 전환 빈도의 Linux 관찰을 찾지 못한 결과, 자연스러운 생성기(naturalistic generator, 실제 사용 분포에서 timeline을 뽑는 것)는 backlog에 남았습니다. TODO의 backlog 줄: "its prerequisite is a source for Linux-desktop co-occurrence and transition frequency, which 9.10's search did not find." 이 자리를 채울 출처가 나타나기 전에는 시작되지 않습니다.

## 12.9 9.11 scheduler 쪽 상수 — 데이터셋에 닿는 부분

**맡은 것.** harness와 simulator 쪽의 상수와 그 근거(`docs/harness/metrics.md` §8–§11의 상수, 우선순위 표의 boot default, guard 문턱값 등). 대부분 데이터셋 밖입니다. 이 조각의 scope card는 판정 어휘에 `NOT READ`를 더했습니다. 2026-09-13 검증의 주장 목록이 `docs/memos/`, `harness/`, `docs/harness/`를 읽지 않았기 때문입니다.

**데이터셋에 닿은 결정: declared scheduling class.** 9.11 D4(2026-10-07)는 "the simulated machine honours a task's declared scheduling class"로 정했습니다. 기록된 이유는 "Background programs declare their class themselves, and a stock Linux kernel acts on it"입니다. Tracker(LocalSearch)는 시작할 때마다 자기 스레드에 `SCHED_IDLE`, nice 19, idle I/O class를 걸고(`tracker-main.c`), Déjà Dup의 backend는 `chrt --idle 0`과 `ionice -c3` 아래에서 돕니다. **SCHED_IDLE**은 Linux의 scheduling policy 가운데 하나로, 다른 일이 있으면 거의 CPU를 받지 못하는 가장 낮은 class입니다(커널 무게 3, nice 0의 1,024에 비해). **nice**는 보통 class 안에서의 상대적 무게를 정하는 -20부터 19까지의 값입니다.

이 결정의 근거는 측정입니다. D4의 단계 (1)은 "each measured entry's observed scheduling policy and nice value, read from its campaign's raw records"였고, 그 결과가 `_dev/research/jioh/task-9.11-scheduler-constants/classes/audit.md`입니다. 두 부분입니다. 첫째, taskstats를 남긴 build와 background family는 release의 zip에서 `ac_sched`와 `ac_nice`를 HTTP range read로 읽었습니다. 둘째, perf 텍스트만 남긴 나머지 family는 class census(2026-10-07)로 새로 조사했습니다. 주체마다 dry job 하나에서 `dataset/tools/meas/sched/classes.py`가 job 내내 2 s마다 모든 스레드의 policy, 실시간 우선순위, nice를 `/proc/<pid>/task/<tid>/stat`에서 읽었습니다(원자료 release `meas-ci-probes-2026-10-07b`). "A declared class is configuration, not timing, so one job per subject and no machine gate." 결과: `file-indexer`(Tracker의 68개 스레드 모두 IDLE)와 `incremental-backup`(`deja-dup`, `duplicity`, `gpg`)만 idle class의 일을 담고, 나머지 측정 entry는 모두 NORMAL nice 0이었습니다. 몇 가지 예외(SteamCMD의 nice 10 스레드, 업그레이드의 nice 19 `apt-check`/`dpkg`, Mesa의 `disk$0` 스레드)는 notes와 한계로 남았습니다.

이것이 9.13에서 `declared_class` 필드(모든 archetype entry와 모든 task 기록, 값은 `normal`과 `idle`)가 된 경위입니다. 그리고 TODO의 9.16 줄은 "every entry's `declared_class` rests on 9.11's class census"를 감사가 확인할 것으로 적습니다.

**함께 결정된 한계들.** D6과 D20: nice는 담지 않음(SteamCMD의 일 75.33 %가 nice 10인데 보통 우선순위로 돌므로 `c2-p2a`에서 download의 게임 방해가 과대, 가설에 유리한 방향). D21: 그 한계의 경계를 재기 위해 `game-download-idle`과 `c2-p2a-idle` variant를 만듦. D16: 색인기의 `background.slice` 한계(11.2절, 가설에 불리한 방향).

## 12.10 9.12 관련 연구 서술 — 데이터셋에 닿는 부분

**맡은 것.** `docs/related-work.md`, `docs/research-proposal.md`의 출처 문장들과 그 registry 항목. 데이터셋 밖입니다. 이 조각은 D1–D53 뒤에 자기 결정을 다시 감사해(D55–D116) 많은 결정을 고쳤습니다.

**데이터셋에 닿은 결정.**

- **costs 캠페인(D31, D50, D55).** 본문의 커널 비용과 LLM 지연 문장을 위해 데이터셋과 같은 기계에서 쟀습니다(`meas-ci:costs:2026-10-08`, 6.7절). 이 캠페인도 stability rule을 따랐고, 규칙 밖으로 나간 네 값(측정 CPU의 유휴 switch 빈도와 `schedule()` 빈도, 유휴 경로 pick 중앙값, newidle 평균)은 D55에서 인지오의 결정으로 목록에서 빠져 관찰 범위로만 남았습니다. 이유: "the workflow's exception … requires the exception be taken per value by 인지오 with stated half-width, range, repeat count and projection; no stated quantity rests on them." 예외를 쓰지 않고 목록에서 빼는 것이 더 정직했다는 판단입니다.
- **D106.** `cpu-batch`의 `python3` 묶음을 설명하는 글은 그것을 실제 학습 run(PyTorch의 기본 MNIST 예제, CPU)이라고 부르되, 데스크톱 사용자가 MNIST를 학습한다고 주장하지 않는다. `references.md`의 `pytorch-examples` 항목이 이미 그렇게 적습니다(2.8절).
- **D102.** 9.10이 넘긴 질문, 곧 `sources.yaml`을 떠나는 항목 가운데 본문이 아직 인용하는 것이 무엇인가에 답했습니다.
- **D110, D112, D113.** `meas-local` 형식, deployed-system 등급의 확장, 발표와 뉴스 type(2.2–2.3절). 셋 모두 9.15(2026-10-16)에서 `references.md`에 반영되었습니다.

---

# 13장 · 그 뒤의 검토와 감사

이 장은 "2026-09-13 검증 뒤에도 틀린 것을 찾아내는 일은 어떻게 계속되었나"라는 질문에 답합니다. 검증은 한 번의 사건이 아니었습니다. 연구 조각들이 일하는 동안과 끝난 뒤에 네 번의 큰 검토가 있었고, 각각이 무엇을 확인했고, 무엇을 찾았고, 무엇을 바꿨는지를 날짜 순서로 봅니다.

```
2026-09-13  검증과 critical findings  ──▶ Phase 9 시작
2026-09-20  데이터셋 타당성 검토 memo    ──▶ 두 주장의 범위, ledger, demand window, venue
2026-09-26  9.5–9.9 검토              ──▶ 추적 없는 대조군, 순서 위협, 반복별 점검 읽기
2026-09-28  9.5–9.9 검토와 coverage sweep ─▶ 시간 창, web-browser의 renderer, 기록과 코드의 불일치 정리
2026-10-10/11 9.15 전 데이터셋 감사        ──▶ class A 결함 넷, fidelity map, 문서 낡음, 9.17–9.21
(열림)       9.16 exit audits
```

## 13.1 2026-09-20: 데이터셋 타당성 검토 memo

**무엇을 확인했나.** `docs/memos/2026-09-20-dataset-validity-review.md`는 `dataset/archetypes.yaml`, 그 근거 문서들, 그리고 9.5의 측정 방법을 연구의 두 주장(1.1절)이 데이터셋에 요구하는 것에 대어 읽었습니다. "Assessment only; nothing in the repository was changed."

**무엇을 찾았나.** 판정은 "sound for the recognition claim, bounded for the scheduling-benefit claim"이었고, 다섯 가지 진술이 있습니다.

1. 인식기는 시간이 아니라 정체를 읽으므로, 인식 주장은 compile의 결정성이 받친다.
2. 측정 장치가 성립시키는 것은 한 구성에서의 정밀도이지 대표성이 아니다. 재현성과 대표성은 다른 문장으로 주장해야 한다.
3. **stability ledger를 공개하라.** "Carry that to the whole library and report the summary: how many quantities met the tolerance, how many are carried under a stated exception, and the largest half-width carried. It is the evidence no comparable workload suite reports, and without it the stability rule reads as decoration."
4. **demand window를 범위 결정으로 진술하라.** "Below contention no scheduling policy differs, so the regime is the right one to measure in — but it is chosen, not found."
5. **이득 주장의 경계.** 값은 hosted runner, Xvfb, 화면 주사율 없음, GPU 없음, 소리 장치 없음, 한 코어에 고정, 사람 없음의 값이며 데스크톱의 진실이 아니다. 논문에 이 범위를 담거나, 실제 데스크톱과 한 번 비교해 오프셋을 보고하라.

그리고 "Untouched"로, segment 구성(어떤 응용이 언제, 얼마나 오래, 무엇 옆에서 도는가)은 평균에서 지은 것이며 이 검토가 건드리지 않았다고 적었습니다.

**무엇이 바뀌었나.**

- 3번의 ledger는 `measurement-campaign-record.md`(캠페인마다 규칙이 덮는 값, 가장 넓은 반폭, 예외)와 각 entry의 scope 문장(9.5 D76, 2026-09-26: "the nine scopes state the stability rule and the values it was not held to"), 그리고 `measurement-overview.md` §7, §9에 담겼습니다. 라이브러리 전체의 요약 수치(규칙을 통과한 값의 수, 예외 class마다 담은 값의 수, 담은 가장 넓은 반폭)를 한곳에 모은 표는 아직 없습니다. 가장 가까운 것은 campaign record의 2026-09-24 단락("7 of the 133 values the rule is read on … have half-widths of 4.5 % or more")입니다. 인지오가 2026-10-16에 이 요약을 만들기로 정했습니다(9.15 작업 목록 W-0739). 조각들의 pooled record 위에서 도는 스크립트가 계산하고 `measurement-overview.md`의 stability 절에 싣는 일이며, 9.16의 측정 감사에 들어 있습니다(`_dev/TODO.md` 9.16 줄).
- 4번의 demand window는 그 뒤 더 나아갔습니다. 9.14 decision 4(2026-10-09)가 그것을 gate에서 은퇴시켰습니다. "The compiler records demand per file … and per segment … and never fails on it. … the `oversubscribed` class marks a file designed to hold contention, its demand a measured fact reported, not a window held." memo의 "a file outside it is redesigned rather than waved through"는 그날로 낡은 문장이 되었습니다. 은퇴의 이유는 인지오가 2026-10-16에 밝혔습니다(9.15 작업 목록 W-0737). 9.10 D17이 모든 작업을 측정된 그대로 통째로 묶으므로 파일의 수요는 측정에서 따라 나오고, 그것을 창 안에 맞추려면 측정된 길이를 구부려야 했다는 것입니다. 그래서 수요는 맞추지 않고 파일마다, segment마다 보고하며, 짝 검토(pair review)가 경합이 있는 segment를 읽습니다. `dataset/README.md`의 "Demand is reported, not held" 규칙이 이것을 이유와 함께 적습니다(14.4절).
- 5번은 각 entry의 scope와 `measurement-overview.md` §11에 들어갔고, 2026-10-16에 인지오가 그 범위를 논문에 싣기로 정했습니다(`docs/research-claims.md`의 "What is not claimed"). 실제 데스크톱 비교는 열지 않습니다(11.3절).
- "Untouched"의 segment 구성은 2026-10-11 감사의 열린 항목과 이어지고(13.4절), 생성 층(generated layer를 다루는 5권)과 backlog의 naturalistic set으로 갔습니다.

memo 자체는 바뀌지 않았습니다. memo는 `zhang-chb15`(2026-10-01에 빠짐)를 인용하고 demand window를 규칙으로 적고 있지만, 9.15 spec decision 10에 따라 memo의 원문은 고치지 않고 `## Correction (<date>)` 절을 덧붙입니다.

## 13.2 2026-09-26: 9.5–9.9 검토

**무엇을 확인했나.** 9.5부터 9.9까지 측정을 마친 다섯 조각을 한꺼번에 검토했습니다. 이 검토의 독립된 보고서는 저장소에 없고, 그것이 정한 일들이 결정 기록과 TODO 줄에 남아 있습니다.

**무엇을 찾았고 무엇이 바뀌었나.**

- **perf 자체의 영향을 잰 적이 없다.** → 추적 없는 대조군(8.2절). spec은 "The method of the untraced control set by the 2026-09-26 review of 9.5–9.9"로 시작합니다(2026-09-27 grill, 실행은 2026-09-27에 끝남, release `meas-ci-control-2026-09-27`).
- **compile된 wake 흐름은 gap의 순서와 함께 깨어남을 재현하지 않는다.** → 타당성 위협 진술(`burstiness.py`로 잰 숫자, 2026-09-27; 9.15에서 `measurement-overview.md` §8에 실림)과 Phase 10의 trace-replay check(8.5절).
- **캠페인 자신의 점검을 ±5 % 정밀도와 비교하면 모든 반복이 공유하는 차이를 놓친다.** → 9.5 D81이 자극 민감도 점검을 반복별 비율의 구간으로 읽게 바꿈(8.3절). 9.7 D36도 같은 방식.

## 13.3 2026-09-28: 9.5–9.9 검토와 coverage sweep

**무엇을 확인했나.** 두 가지입니다. 하나는 측정의 내용에 대한 검토, 다른 하나는 조각들의 changelog가 말하는 "덮음"의 주장(이 값은 이렇게 되어 있다, 이 테스트가 이것을 지킨다)을 코드, library, 기록에 대어 하나하나 읽은 **coverage sweep**입니다.

**무엇을 찾았고 무엇이 바뀌었나.**

- 담은 단계를 시간 창으로 읽지 않았다 → `windows.py`와 9.5 D85, D87, 9.8 D34, 9.9 D42(8.4절).
- `web-browser`가 자기 run의 renderer를 빼고 있었다 → 9.5 D84: "`web-browser` carries every renderer of its run." 기록된 이유는 9.5 D14가 다른 archetype이 소유한 것만 빼도록 했는데, renderer entry들은 사람 없는 페이지를 기술하므로 쓰고 있는 페이지는 어느 entry도 기술하지 않았다는 것입니다. 그 결과 입력당 CPU 평균이 1.671 ms에서 4.274 ms로, 자극 민감도 비율이 1.160에서 1.338로 바뀌었습니다. renderer가 키 하나의 CPU의 59 %를 썼기 때문입니다.
- coverage sweep은 조각마다 한 결정으로 정리되었습니다(9.5 D89, 9.6 D37, 9.7 D38, 9.8 D36, 9.9 D43). 예를 들어 9.5 D89는 이런 것들을 바로잡았습니다. 아홉 scope가 4 vCPU 기계만 적고 "the application's process tree pinned to one of its CPUs, which the runner's own agent processes share"를 적지 않았던 것, 입력당 run의 window rule이 낳는 결과(긴 간격 안의 자동 저장이 그 앞의 입력에 청구됨)를 적지 않았던 것, `mpv-video` 반복 9의 gap 수를 segment 수로 잘못 센 것 등. 9.5 D89는 "this entry changes no carried value"였습니다. 숨긴 값이나 발견이 있는 것은 따로 결정했습니다(9.5 D90–D95, 9.7 D39, 9.8 D37–D38, 9.9 D44). TODO 9.16 줄은 이것을 "its nine findings closed …, none handed here; 9.5–9.9 are closed, and a later review of them is this audit's"로 요약합니다.

## 13.4 2026-10-10/11: 9.15 전 데이터셋 감사

**무엇을 확인했나.** `_dev/docs/audit/jioh/2026-10-10-dataset-audit-before-9.15.md`(Status: record, Created 2026-10-10, Updated 2026-10-11)는 9.13의 재건축과 9.14의 소비자 재작업이 끝난 뒤, 9.15의 문서 정리에 들어가기 전에 한 감사입니다. "Five independent auditors on `jioh/dataset-rebuild` at `fe19be86`: A consumer consistency, B provenance, C build reliability, D real-world fidelity, E external review." 다섯 감사자의 보고서는 작업 파일이라 남기지 않았고, 이 통합본이 기록입니다. "re-verified"로 표시된 항목은 조정 세션이 감사자와 독립적으로 재현한 것입니다.

**네 질문과 답.**

| 질문 | 답(요지) |
|---|---|
| core set이 RQ0 run에 준비되었나? | 데이터셋 쪽은 준비됨(모든 artifact, pin, schema 검사, class 필드, 항이 해석되고 이 기계에서 바이트까지 재현됨). run은 데이터셋 밖에서 막힘: HEAD의 simulator가 다시 지은 파일 다섯(판정 둘)을 거부하고, 사전 등록된 executor 적합성 항목 여섯 중 넷이 미구현 |
| 전문적 연구에 맞나? | "Major revision, not reject." 값 단위의 출처, 결정성, pin 규율은 분야의 수준 이상. 심사자가 거부할 이유: 공개 문서가 데이터와 다른 데이터셋을 진술함; C7 counterpart가 "one-diff pair"라는 말보다 약함; 게임 archetype의 숫자가 발표 슬라이드에 기댐; timeline bound value에 출처 칸이 없음; 원자료의 공개가 진술되지 않음 |
| build는 얼마나 믿을 만한가? | 이 기계에서 정확히 재현됨. 그러나 CI가 이 manifest를 compile한 적이 없음(main에는 재건축 전 manifest); `make check`가 디스크의 `build/`를 해시하지 않음; variants manifest는 어떤 workflow도 drift 검사하지 않음; manifest가 입력 약 75개 중 둘만 고정 |
| 실제 사용에 얼마나 가까운가? | 11.3절의 인용 |

**class A 결함(인지오의 결정이 필요한 것).** 여기서 A1–A4는 이 감사가 붙인 번호이며, critical findings memo의 A1–A5와 다른 것입니다.

- **감사의 A1, C7 counterpart의 키 입력 조각.** counterpart의 키 입력이 기준 파일의 처음 26.385 s가 아니었습니다(re-verified). 컴파일러가 자극의 시작 위치를 창 길이로 뽑는데, counterpart의 창(22.385 s)과 기준의 창(56 s)이 달라 같은 seed가 다른 위치를 냈습니다. 예: browsing은 기준의 [0, 26.385 s)에 입력 wake 90개, counterpart에 29개, 공유하는 시각 0. 9.10 D41은 "its base's first C seconds"라고 결정했는데 그것은 task와 도착과 떠남에 대해서만 테스트되었고, 키 입력 조각은 아무도 결정하지 않았습니다. 선택지 (ii)를 권고했습니다.
- **감사의 A2, timeline bound value에 출처 칸이 없음.** 9.10 D32가 결정했고 "the field and the lint are 9.13's"였는데, 만들어지지 않았습니다. 근거는 `bound-values.md`에만 있었습니다.
- **감사의 A3, 게임 chain이 발표 슬라이드에 기댐.** "`game-task-chain` paces 8 of 51 files (3 judging: c2-p2a, c2-p2b, c7-gaming) on a talk deck."
- **감사의 A4, build gate의 구멍.** 9.14 이후 CI가 이 manifest를 compile한 적이 없고, `make check`가 `build/`를 해시하지 않는 등.

**확인된 것("Sound, and verified").** "129/129 artifacts match both manifests; 5 gate pins equal current bytes; 129/129 schema-valid; 863 arrive + 189,484 spawn records all carry `declared_class`, idle in exactly the 7 predicted files; 19 judging / 32 reporting / 78 variants; dataset lint clean; harness suite 279 passed"; 재현 "`make check` 1517 s exit 0 …; `variants.py --check` 2098 s exit 0 (78); `replay_fold_in.py --check` 14 s exit 0 (6 streams byte-identical from landings); `batch_fold_in.py --check` exit 0"; 출처 "29 entries, 28 measured on own campaigns with version, runner, instrument, repeats, stability rule; 6,953 leaf numerics 96.6 % measured; 312 tagged objects 97.4 % `meas-ci`; the 13 + 6 critical findings each resolved against a primary read; session/build entries regenerate byte-for-byte".

**9.15 줄에 없던 문서 낡음.** TIMER backlog 문장(interpretation contract), 낡은 사전 등록 숫자("25 judging, K = 13" 등), `dataset/README.md`의 demand window 규칙, `measurement-overview.md`의 release 표, `references.md`의 `dhakal-chi18` 중복과 상태 줄들, `sources.yaml`의 아무것도 받치지 않는 id와 `ocallahan-atc17` note, `archetypes.yaml:1`의 "(v0.1)", 고아가 된 `dataset/meas/summary.json`, 데이터 공개(release URL과 해시, LICENSE, CC-BY-NC-SA, 손으로 만드는 release), 파일보다 오래 사는 일괄 작업의 manifest `demand`("c2-p1a 14.5 lanes, c2-p2a 9.4"). 이것들은 2026-10-11에 9.15 줄에 합쳐졌습니다.

**무엇이 바뀌었나(2026-10-11, 인지오).**

- 감사의 A3: "resolved as is. The figures stand as the talk's reported values; the chain-x1.2 and chain-x1.4 variants are the sensitivity check. No change to the entry or the files."
- 감사의 A1: 선택지 (ii). "the compiler draws a derived file's stimulus offset from its base's window, so a counterpart's keystrokes are its base's first C seconds; … the test 'c7 input wakes ⊂ c1 input wakes in [0, C)' is added." → 9.18이 `slice_of`와 그 테스트로 실행(2026-10-11).
- 감사의 A2: → 9.18이 `source` map과 `lint_bound_sources`로 실행.
- 감사의 A4: → 9.18(build gate)과 9.22(build 시간; CI가 한 번에 compile)로 실행. CI run 38131040159가 두 manifest를 Linux에서 6분 34초에 재현(9.22 D6).
- 열린 항목 "core set의 전환과 일반화 덮음": core set의 C3에는 arc 셋, 경계 약 여덟 개뿐이라 전환 인식이나 셀별 정확도에 대한 통계적 주장을 못 함. → 생성 층(phase spec decision 9, 2026-10-11), 9.19–9.21. 그리고 "focus enters the telemetry"(decision 10) → 9.17.
- 측정할 원하지 않는 작업의 backlog(`gnome-software`와 `packagekitd`, `snapd` 자동 갱신, `updatedb.plocate`, `update-initramfs`, `mandb`와 `apt-get update`): 각각 workflow 문서를 따르는 캠페인 하나. 몇 개가 필요한지는 RQ1 실험 spec 세션이 정하고, 캠페인은 Phase 10의 RQ0 run 뒤에 돕니다.

## 13.5 지금 기계가 지키는 검사들

이 검토들의 결과 가운데 일부는 매번 도는 검사가 되었습니다. build gate와 CI와 tests를 다루는 7권이 자세히 다루므로 목록만 적습니다.

- repo lint(subset, 필수 필드, 태그와 locator, freeze), bound-source lint(freeze 포함), grid lint, release-map lint(2.7절).
- `declared_class`가 모든 entry와 task 기록에 있는지, TIMER-first(9.13).
- C7 counterpart의 입력 wake가 기준의 처음 C초 입력 wake의 부분집합인지(9.18의 `test_c7_input_wakes_are_a_subset_of_the_bases_in_the_first_c_seconds`).
- `check_build.py`: `build/`가 모든 manifest의 합집합과 같고, 각 manifest가 커밋된 바이트와 같은지(9.18, 9.22); 파생 timeline과 `coverage-grid.json`도 커밋된 바이트와 같은지(9.23 D12).
- 측정 entry가 pooled record에서 다시 생성되는지(9.4절의 재생성 테스트들, 9.13 D8).
- compile된 흐름이 측정 빈도를 지키는지(8.5절).
- `--check` 모드: `compile.py`, `variants.py`, `generate.py`, `derive.py`, `replay_fold_in.py`, `batch_fold_in.py`.

검사가 지키지 못하는 것은 2.7절에서 본 그대로입니다. 형식은 지키지만 근거가 옳은지는 사람이 읽어야 하고, 그것이 9.16의 일입니다.

---

# 14장 · 아직 남은 것: 9.15, 9.16, 그리고 기록이 밝힌 한계

이 장은 "Phase 9가 끝나려면 무엇이 남았고, 지금까지의 기록이 스스로 밝힌 한계는 무엇이며, 문서와 tree가 어디서 어긋나는가"라는 질문에 답합니다. 2026-10-14 현재 `_dev/TODO.md`의 인지오 절에서 9.15는 `[WIP]`, 9.16은 `[ ]`입니다. 실행 순서는 "… → 9.21 → 9.15 → 9.16"이므로, 9.15가 끝나야 9.16이 시작됩니다.

## 14.1 9.15: 문서, memo, guidebook 정리

**무엇인가.** "The one sweep that brings the public docs, the memos and the guidebook volumes already written in line with the rebuilt workload dataset and the decisions of Phase 9, ending in the final memo to 인경민 and 박이안." spec은 2026-10-14의 grill에서 정해졌습니다(`_dev/docs/spec/jioh/task-9.15-docs-memos-and-guidebook-corrections.md`). 범위는 9.15에 넘겨진 모든 항목(TODO의 9.15 줄, 조각 changelog의 모든 "Hands to 9.15", 2026-10-10 감사의 항목), `docs/`(guidebook 포함), `dataset/README.md`, memo, 그리고 LICENSE 파일 둘과 최종 memo입니다. 새 guidebook 권을 쓰는 것과 `_dev/`의 기존 파일은 범위 밖입니다.

**이 권과 닿는 결정.**

- **decision 3, 출처들이 어긋날 때의 우선순위.** "Highest first: the code and data as they stand … ; the latest decision record on the matter for what code does not express, a later decision superseding an earlier; the hand-off text, which says where to look and not what to write; the current docs, never an authority." 그리고 "A new `docs/references.md` entry needs a verified passage on file; without one the entry is marked unverified, not invented." 이 권의 3장 결정 1이 9.15의 편집 규칙에도 그대로 이어집니다.
- **decision 4, 문서의 범위.** 데이터셋을 설명하는 문서(`docs/workload/`, `dataset/README.md`, `docs/data-contracts.md`, harness guide의 records와 dataset 장)는 코드에 대어 전체를 다시 훑습니다. 이 권이 낡았다고 지적한 `grounding-sources.md`, `source-vetting.md`, `measurement-overview.md`, `dataset/README.md`가 여기에 들어갑니다.
- **decision 5, `references.md`를 먼저.** "The `docs/references.md` chunk runs alone first." 2.2–2.4절의 열린 자리(`meas-local`, 발표 type, 등급 규칙 확장, `dhakal-chi18` 중복, `ocallahan-atc17` 문장)가 이 묶음의 일입니다.
- **decision 10, memo.** 원문은 고치지 않고 `## Correction (<date>)` 절을 덧붙이며, memo마다 닫힘/열림 한 줄을 답니다. critical findings memo와 2026-09-20 memo가 여기에 해당합니다.
- **decision 11, `_dev/`는 개발 이력.** 기존 `_dev/` 파일은 건드리지 않습니다. 따라서 `measurement-campaign-record.md`의 Campaigns 표 누락(9.3절)은 9.15의 대상이 아닙니다.
- **decision 12, LICENSE.** 코드는 MIT, 데이터와 release asset은 CC-BY-NC-SA-4.0(SWELL-KW를 출처로 밝힘), 저작권자는 Jioh In, Kyungmin Inn, Ian Park.

> **열린 자리.** 9.15는 진행 중입니다. spec의 유일한 열린 항목은 "The final memo's language — decided at the memo step"입니다. 9.15가 끝나는 조건(decision 14)은 작업 목록의 모든 행이 닫히고, 모든 묶음이 검토자를 통과해 커밋되고, 인지오가 모든 묶음의 log를 읽고, 코드와 결정의 모든 불일치가 인지오의 답을 받고, 모든 memo가 열림/닫힘 줄을 갖고, 최종 memo가 커밋되는 것입니다. "9.16's exit audits run on that state."

## 14.2 9.16: exit audits

**무엇인가.** "Exit audits — the claim, measurement and compiled-number audits re-run on the final state (spec decision 8)." 2026-09-13 검증의 세 감사(4.1절의 (1)–(3), (4), (5))를 최종 상태에서 다시 돌리는 것입니다. 결정 8의 조건을 다시 적으면: 모든 주장이 결정 1을 만족하고, 모든 archetype과 timeline의 모든 현실 주장이 결정 2와 3을 만족하거나 인지오의 기록된 결정을 갖고, 모든 측정값이 공개된 원자료에서 재현되고 그 방법이 잰 것을 기술하며, 우선순위 표, 짝 검토, scoring spec, guard spec, RQ0 gate spec, memo의 어떤 진술도 다시 지은 데이터에 대해 틀리거나 낡지 않을 것.

**TODO 9.16 줄이 모은 확인 목록.** 조각들이 각자 "Hands to 9.16"으로 넘긴 것을 모은 것입니다. 측정과 근거에 닿는 것만 정리합니다.

| 확인할 것 | 넘긴 곳 |
|---|---|
| 캠페인마다 반복 수가 어떻게 정해졌는가 — 멈춤 규칙이 binding value의 반폭을 낙관적으로 만든다는 점을 읽음 | 9.5의 자체 검토(2026-09-24 단락) |
| timeline마다 장소의 혼합(venue mix)을 나열 | 9.5 spec decision 13 |
| 세 periodic pool의 `cycle` 블록이 release `meas-ci-2026-09-18`과 `meas-ci-2026-09-20`에서 `pool.py` at `cc51eb8`로 재현 | 9.5 D75 |
| release에서의 재현 | 9.8 D25 |
| release `meas-ci-session-2026-09-24`에서 9.9 D47의 도구로 재현 | 9.9 D26, D47 |
| `mail-client`의 77회 유휴 pool이 `meas-ci-2026-09-18`과 `meas-ci-2026-09-28`에서 `0aa25ac`로 재현 | 9.5 D94, D97 |
| 9.13의 reads가 `scans/`의 스크립트로 재현; 모든 entry의 `declared_class`가 9.11의 class census에 기댐; blessed manifest의 개수 | 9.13 |
| mock-media fixture의 유도; 판정 파일의 입력 wake 수; manifest의 재현; variants와 replay 흐름의 재현(`replay_fold_in.py --check`, `variants.py --check`); `reads.md` R1, R2의 반복 표(`scans/mnist_cpu.py`, `scans/upgrade_cpu.py`) | 9.14 D1, D2, D4, D6, D7, D8, D10 |
| 생성 층이 generator, library, C1 artifact에서 manifest와 함께 재현; 9.18의 counterpart 테스트와 source-field lint 통과; gate pin과 생성 층 pin이 커밋된 바이트와 같음 | 2026-10-11 검토 |
| 각 하위 작업 시점의 manifest와 pin 해시: 9.17 `625e431f…`/`328560cf…`; 9.18 `976a943c…`/`6c244f17…`/`1f7e9e30…`; 9.22 `d10bcd42…`/`831a854e…`; 9.19 `899efa53…`/`7a758f6e…`/`8c4c6fce…`; 9.20 `fad7192d…`/`03f14b2c…`/`593dc23a…`/`183deedb…`/`d2686e73…`/`7236f4b2…`/`0b8b76ce…`; 9.21 `e26aa8e6…`/`21826be3…`/`a8c271dd…`/`6d9192db…`/`2cb56e69…`, scoring spec `0ff71b1f…` | 9.17–9.22 |
| 모든 timeline의 `source` map이 `bound-values.md`와 항목별로 일치("the lint checks form, not that each tag is the right ground") | 9.18 D6 |
| flap-stress 간격의 세 출처를 release 태그에서 읽음; tier-3 이름 `melt-7`과 `duplicity`가 캠페인 기록에 기댐; `linux-sched-h`를 v6.17에서 읽음 | 9.19 D5, 9.20 D10 |
| CI run 38131040159와 38243554308이 manifest들을 Linux에서 재현 | 9.22 D6, 9.20 D11 |
| `gh-hosted-runners` 2026-10-13에 읽음 | 9.21 |
| 마지막 build 위에서 집에서 도는 전체 smoke(`make -C harness smoke`), 걸린 시간 기록 | 9.23 D15 |
| `renderer-hidden`의 pool(`meas-ci:desktop:2026-10-05b`)과 `video-editor`의 유휴 pool(`meas-ci:interactive:2026-10-05`)에서 burstiness와 시간 창을 다시 읽고 `measurement-overview.md`의 위협 문장을 그 값으로(8.5절) | 9.15 (2026-10-16) |
| stability ledger: 허용 오차를 통과한 값, 예외 class마다 담은 값, 담은 가장 넓은 반폭을 조각들의 pooled record에서 스크립트로 계산해 `measurement-overview.md`의 stability 절에(13.1절) | 9.15 (2026-10-16; 2026-09-20 memo §3) |

2026-10-11 검토의 항목("the five gate pins and the generated layer's pins equal the committed bytes")이 대는 것은 그때의 커밋된 바이트입니다. 위 표의 하위 작업 시점 hash 뒤에 9.23 D10(2026-10-14)과 D17(2026-10-15), 그리고 9.15의 세 rebuild(2026-10-16에 한 번, 2026-10-17에 두 번; `harness/CHANGELOG.md`의 2026-10-16 항목과 2026-10-17의 두 data 항목)가 다시 bless와 pin을 했습니다. 2026-10-17 현재의 pin은 9.15의 2026-10-17 두 번째 rebuild의 것입니다. dataset manifest `0f0af422…`, variants manifest `cdc14319…`, scoring spec `2ad757b6…`(9.23 D10), guard spec `24ccb875…`, driver table `0fba4b3c…`(RQ0 gate spec의 `pins`), 그리고 생성 층의 다섯 manifest `d84fb68a…`(transition grid), `a6980482…`(return grid), `92676677…`(flap-stress), `1d129a51…`(distractor grid), `8c38e7a8…`(familiarity ladder)입니다. 같은 날 첫 rebuild의 값(dataset `d52e7bd4…`, variants `6c1c3e09…`, 생성 층 `4bb7a444…`/`ec7ca574…`/`79a6c5c4…`/`3478a908…`/`415cfbd6…`)이 그 바로 앞의 pin이고, 9.15의 2026-10-16 값(dataset `b6017a10…`, variants `087ef27c…`, 생성 층 `a8eebb33…`/`2e57a6c1…`/`dd6a7c24…`/`264d3333…`/`58a34d65…`)이 그 앞, 9.23 D17의 값(dataset `81d3213d…`, variants `7079e677…`, 생성 층 `826c719c…`/`392d6071…`/`97ba813f…`/`919bb2c0…`/`b6f82df5…`)이 그 앞입니다.

그리고 13.3절에서 본 대로, 2026-09-28의 coverage sweep이 9.5–9.9를 닫았으므로 "a later review of them is this audit's"입니다. 9.9 D27이 넘긴 "9.5–9.8 ran beside the same `php-fpm` and workflow loops"(다른 캠페인의 component에도 runner 배경의 wake가 섞였을 수 있음)도 이 감사가 볼 거리입니다.

> **열린 자리.** 9.16은 아직 시작되지 않았습니다(미실행). 9.15가 먼저 끝나야 합니다. 9.16 자신의 spec은 아직 없습니다. 위 목록이 감사의 형식(누가, 어떤 도구로, 무엇을 "해결됨"으로 볼지)을 정하지는 않으므로, 그것은 9.16의 spec 세션에서 인지오가 정합니다.

## 14.3 기록이 스스로 밝힌 한계

이 권 전체에 흩어진, 기록이 스스로 "stated limitation"으로 적은 것들을 한곳에 모읍니다. 각 줄은 그 한계를 처음 진술한 기록입니다.

1. **장소.** 측정값은 "this software on this machine"이며 데스크톱의 진실이 아니다: runner, 한 CPU에 고정, EPYC 7763 하나, 한 기간, Xvfb 또는 헤드리스, GPU·주사율·소리·사람 없음(결정 5; 9.5 D10; `measurement-overview.md` §11). 실제 데스크톱 검증은 미뤄짐. 이 범위는 논문에 실림(`docs/research-claims.md`의 "What is not claimed"; 인지오의 결정, 2026-10-16).
2. **CPU 모델 하나.** `maricq-osdi18`의 권고(여러 VM, 여러 시간)를 비교 가능성을 위해 따르지 않음 — "a stated limitation of the library's precision"(workflow 문서).
3. **정밀도는 재현성이지 대표성이 아님**(2026-09-20 memo §2).
4. **멈춤의 낙관성.** 처음 통과에서 멈춘 반폭은 낙관적이며, 모의실험 결과 명목 95 %가 약 91–94 %를 덮음(9.5 D88; `chow-aoms65`).
5. **t 구간과 대표본 공식.** 비모수 중앙값 구간을 쓰지 않음; 비율 분산은 n > 30, cv < 10 %의 대표본 결과인데 반복은 대부분 30 미만(workflow 문서).
6. **예외로 담은 값.** 그 반폭보다 작은 차이에 어떤 결과도 기댈 수 없음(9.6 D29).
7. **추적의 영향.** run 평균이 추적 아래에서 최대 약 28 % 길게 잡힘(0.72–0.98), entry별로 notes에 적음(9.5 D82 등).
8. **자극.** SWELL-KW 하나(2012, Windows 실험실, 키만, 15.6 ms 양자화); 다른 타이핑으로 바꾸면 입력당 CPU가 −9 %에서 +34 % 달라짐(8.3절). 포인터 입력 없음; GIMP와 Kdenlive는 스크립트 포인터(design).
9. **순서와 동시 깨어남.** compile된 흐름은 component의 빈도와 분포를 재현하나 gap의 순서와 함께 깨어남은 재현하지 않음(`measurement-overview.md` §8의 위협 진술; trace-replay check로 경계).
10. **디스플레이와 GPU의 방향.** compositor 주기는 60 Hz이나 위상이 없음; CPU 래스터화가 run 길이를 과대(9.5 D24).
11. **X11과 Wayland.** 응용은 X11 client로, 세션은 Wayland에서 잼; Wayland 데스크톱에서의 각 프로그램은 관찰 안 됨(9.10 D172).
12. **조합.** task set, 동시 출현, 순서, 길이는 design; "the scheduling-benefit result holds on these compositions, which are not shown to be typical"(9.10 D2).
13. **장소가 다른 archetype의 조합.** runner 측정과 문헌(게임 chain)의 규모가 서로 보정되지 않음 — library 수준의 한계로 archetype plan §2의 "Observation venues" 단락이 진술함(9.5 follow-ups spec decision 13; 9.15).
14. **게임 chain.** 발표 슬라이드의 보고 값; 심판 없음; per-schedule runtime을 wake당 RUN으로 읽어 아래쪽으로 치우침(9.4 D9).
15. **declared class와 nice.** nice를 담지 않아 SteamCMD의 nice 10 일(75 %)과 업그레이드의 nice 19 일(2.7 %)이 보통 우선순위로 돎 — download의 방해가 과대, 가설에 유리(9.11 D6, D20); 색인기의 `background.slice` 몫(약 23 %)을 executor가 0으로 다룸 — 가설에 불리(9.11 D16).
16. **세션 상태.** 세션 entry는 사람이 떠나 화면이 꺼진 상태만; 사용 중인 데스크톱은 덮지 않음(9.9 D9).
17. **일괄 작업의 하루.** 무인 업그레이드는 2026-07-27이라는 하루의 업데이트; 다른 날은 다른 job(`package-upgrade`의 notes).
18. **naturalistic set 없음.** 데스크톱 동시 출현과 전환 빈도의 Linux 출처가 없어 backlog(9.10의 검색; TODO backlog 줄).

## 14.4 문서와 tree가 어긋나는 곳

이 권을 처음 쓸 때(2026-10-14) tree와 대조해 찾은 불일치를 모읍니다. 둘째 칸은 그때 문서가 말한 것, 셋째 칸은 2026-10-17의 사실과 그 출처입니다. 9.15가 대부분을 고쳤습니다.

| 어디 | 2026-10-14에 문서가 말한 것 | 지금(2026-10-17) |
|---|---|---|
| critical findings memo의 개수 | spec과 감사: "13 findings"; memo 요약표는 14행(A1–A5, B1–B7, C, D) | 13은 A1–A5, B1–B7, C이고 D는 읽지 못한 출처의 목록(인지오의 답, 2026-10-16; 4.4절) |
| `dataset/sources.yaml` `ocallahan-atc17` notes, `docs/references.md`의 같은 항목 role | "Linux kernel-build workload" | 두 줄 모두 DynamoRio 6.1.0의 `make -j8` build로 고쳐짐(9.15; critical findings A1; 2.4절) |
| `dataset/sources.yaml`의 일곱 항목 | 9.10 D34가 떠난다고 결정했으나 9.13에서 적용되지 않아 그대로 있음(`procyon`, `dkms-man`, `dkms-debian`, `gamemode-docs`, `dubroy-chi10`, `chang-chi21`, `mozilla-testpilot10`) | 일곱 모두 registry를 떠남(9.15, 2026-10-16; 2.4절) |
| `dataset/sources.yaml` 전체 | 30개 id 중 11개만 데이터셋 파일의 태그로 쓰임 | 19개 id, 11개가 태그, 7개가 데이터 파일 속 이름 인용, 1개가 sentinel(2.4절) |
| `docs/references.md` | `dhakal-chi18` 두 번(35, 65행), 역할 다름 | 한 항목으로 합쳐짐(9.15; 2.1절) |
| `docs/references.md` id 규칙 | type 셋(scholarly, deployed-system, measurement); scholarly의 예가 `lavd-ossna24` | talk·학회 초록·뉴스 type(9.12 D113)과 `meas-local` 형식(D110) 반영, scholarly의 예는 `ghost-sosp21`(9.15; 2.2절) |
| `docs/references.md` 등급 규칙 | deployed-system은 "existence claims only" | 9.12 D112의 넓힌 규칙 반영(9.15; 2.3절) |
| `dataset/README.md`의 측정 태그 문장 | "Measured values are tagged `meas-ci:<workflow>:<run>`; raw data lives on the GitHub release named in the tag's registry entry" | 태그는 캠페인 날짜(9.5 D27), release는 `dataset/meas-releases.yaml`이 잇고 lint가 지킴(README의 "Every parameter value is sourced"와 "Licence and data availability"; 9.2절) |
| `dataset/README.md`의 demand window 규칙 | demand window ~100–150 %가 규칙, "Files outside it get redesigned" | "Demand is reported, not held"(2026-10-09에 gate에서 은퇴한 9.14 decision 4와 그 이유; 13.1절) |
| `dataset/README.md:8` 대 `dataset/archetypes.yaml:1` | README "v0.2", yaml 머리말 "(v0.1)" | yaml 머리말도 "(v0.2)"(9.15의 rebuild, 2026-10-16) |
| `dataset/README.md`의 `meas/` 줄 | `dataset/meas/summary.json`을 "the campaign summary"로 | 파일이 지워지고(커밋 `37c2e233`) `meas/` 줄은 `names/`와 `streams/`만 적음(5.2절) |
| `docs/workload/measurement-overview.md` | "The 23 archetypes"; `file-backup`, `renderer-visible` 포함; release 표가 9.9에서 멈춤 | 측정 entry 28개, release 표가 9.10의 캠페인까지(9.15; 9.3절) |
| `docs/workload/grounding-sources.md` | Role B의 interbench 등이 값을 받침; LAVD "16ms-frame deadline"; SWELL-KW "qualitative"; `zhang-chb15` | 9.15의 전체 정리로 고쳐짐(2.9절) |
| `docs/workload/source-vetting.md` | 2.10절의 표; append-only 기록을 어떻게 고칠지 미정 | 원문은 그대로, 끝에 "## Correction (2026-10-17)" 절이 고친 줄을 줄 번호로 이름 지음(2.10절) |
| `_dev/research/jioh/measurement-campaign-record.md` Campaigns 표 | 태그 14개 | 그대로: 개발 이력이라 9.15가 손대지 않음(spec decision 11; 9.3절) |
| `dataset/meas/names/` | `tracker-miner-fs-3`, `clamscan` 등 이전 이름 | 이력으로 남김; 이름의 근거는 9.10 D25의 `comm` 규칙과 캠페인 trace(인지오의 결정, 2026-10-16; 6.8절) |
| privacy-scrub 도구 | `building-plan.md`가 "ships in the artifact"; 저장소에 없음(critical findings B7) | 약속을 거둠, 실제 데스크톱 검증은 밝혀 둔 한계(인지오의 결정, 2026-10-16; 4.4절) |
| `docs/references.md` `chang-chi21` | role 줄의 "~8% had >10 open", "fatter modern tail"(K4: 뒤의 것은 우리 해석, "Article 149"는 확인 불가) | 항목이 registry와 `references.md`를 떠남(9.15; 9.10 D34, 9.12 D102) |

---

# 15장 · 용어 정리

이 권에서 풀어 쓴 낱말을 모읍니다. 앞의 무리는 이 저장소가 만들었거나 자기 뜻을 준 **프로젝트 용어**, 뒤의 무리는 웹 개발에서 잘 만나지 않는 **OS·scheduling 용어**입니다. 괄호 안은 처음 나온 장입니다.

## 15.1 프로젝트 용어

| 용어 | 뜻 |
|---|---|
| archetype (서문) | 어떤 종류의 프로그램이 CPU를 어떻게 쓰는지를 규칙과 숫자로 적은 항목. `dataset/archetypes.yaml`의 entry 하나 |
| archetype library (서문) | archetype 29개를 담은 `dataset/archetypes.yaml`, 데이터셋의 맨 아래 층 |
| timeline (서문) | 몇 초부터 몇 초까지 어떤 이름의 프로그램이 어떤 archetype으로 살아 있고 사용자가 어떤 mode에 있는지를 적은 각본 |
| compile, `wlc` (서문) | timeline과 library를 읽어 무작위성을 모두 풀어 낸 실행 가능한 workload 파일을 만드는 단계와 그 컴파일러 |
| mode (서문) | 사용자가 지금 하는 일의 종류(16개, 예: `browsing`, `dev`, `gaming`) |
| segment (1장) | 파일 안의 시간 구간 하나. 정답 mode 라벨이 붙음 |
| 인식 주장, 이득 주장 (1장) | 이름을 읽는 추론이 상황을 알아낸다는 주장; 그에 맞춘 설정이 scheduling 결과를 바꾼다는 주장 |
| burst, gap (1장) | 한 번 깨어나 CPU를 연속으로 쓰는 덩어리; 깨어남 사이의 간격 |
| makespan (1장) | 일괄 작업이 모두 끝나기까지의 시간 |
| scholarly (1장) | 동료 심사 논문이나 보관된 preprint 출처. 경험적·통계적 주장을 역할 안에서 받칠 수 있음 |
| deployed-system (1장) | 배포된 소프트웨어의 문서, 소스, 데이터 출처. 존재 주장, 그 시스템이 문서로 밝힌 자기 설계, 자기 보고 수치를 받침(9.12 D112가 넓힘) |
| talk, conference abstract or news report (1장, 2장) | 발표 슬라이드, 학회 초록, 뉴스 기사 출처. 각주 등급; 주장과 숫자는 발표자나 기자의 보고로만(9.12 D113; 예: `lavd-ossna24`) |
| measurement, `meas-ci` (1장, 6장) | 이 프로젝트가 GitHub runner에서 직접 잰 측정, 그리고 그 출처 id |
| label: design / convention / arithmetic (1장, 2장) | 출처가 말하지 않는 값에 다는 꼬리표: 우리가 고른 설계값 / 관례 / 다른 값에서 계산한 값. Phase 9 결정 1이 적은 넷째 placeholder는 두지 않고, 측정을 기다리는 값은 `meas-pending` |
| `references.md` (2장) | 사람이 읽는 인용 장부. 모든 출처 id의 `cite`, `role`, `status` |
| `sources.yaml`, registry (2장) | 기계가 읽는 출처 장부. 데이터셋이 값이나 구조를 끌어오는 출처만, `type`과 `locator_pattern`과 `notes` |
| subset lint (2장) | `sources.yaml`의 모든 id가 `references.md`에 항목을 가져야 한다는 검사 |
| id-minting rule (2장) | 출처 id를 만드는 규칙. 인용 단위 하나 = 항목 하나; type별 id 모양 |
| source 태그, locator (2장) | 값 옆의 `<id>` 또는 `<id>:<locator>`. locator는 출처 안의 위치(절, 슬라이드, 파일, 캠페인) |
| `locator_pattern` (2장) | registry 항목이 locator에 요구하는 정규식 |
| existence claim, 존재 주장 (2장) | "배포된 소프트웨어에 이런 시나리오, 설정, 범주가 있다"는 주장 |
| citation-tier rule (2장) | 출처의 등급(scholarly는 번호 참고문헌, deployed-system과 talk·뉴스는 각주)과 각 등급이 받칠 수 있는 주장 |
| status: verified / to-pin / provisional (2장) | 원문과 좌표를 확인함 / 식별은 확실하나 버전 고정이 남음 / 식별이 불완전해 인용 금지 |
| role A–D (2장) | `grounding-sources.md`의 출처 역할: A 시나리오 분류, B 프로세스 행동 파라미터(선례, 그리고 게임 chain에 대한 LAVD의 보고 값), C segment 구조와 전환 통계, D 우리 자신의 측정("this software on this machine", `meas-ci`) |
| the negative result (2장) | 이름이 붙은 데스크톱 process tree를 시간에 따라 담은 공개 trace는 없다는 발견 |
| anti-roles (2장) | 근거로 쓰면 안 되는 출처의 목록(PTS, 모바일 데이터, SchedCP 평가 workload) |
| `source` map (2장) | timeline task의 `bind` 키와 `count`마다 태그나 꼬리표를 다는 칸(9.10 D32, 9.18) |
| `meas-pending`, freeze (2장) | 측정을 기다리는 값의 표시; `make lint`의 freeze가 library의 파라미터와 timeline의 bound value 모두에서 거부 |
| `meas-local` (2장) | 노트북 같은 이름 붙은 개인 기계의 측정 형식(9.12 D110) |
| `meas-releases.yaml`, release-map lint (2장, 9장) | 데이터가 인용하는 캠페인 태그마다 그 원자료 release와 asset의 SHA-256을 적은 지도, 그리고 지도에 없는 태그를 실패시키는 lint |
| verification standard (3장) | Phase 9 결정 1: 원문 구절, 위치, 읽은 사본, 주장 전체(대상, 단위, 통계량, 범위, 모집단), 독립 읽기, 못 찾으면 미검증, 출처 없는 값은 꼬리표 |
| montage (3장) | 한 archetype의 숫자를 서로 다른 관찰에서 가져와 이어 붙이는 것. 결정 2가 금지 |
| observation (3장) | 하나의 연구 모집단, 하나의 trace, 하나의 측정 run. 우리 측정 run도 하나의 관찰 |
| four search classes (3장) | 결정 4의 검색 네 부류: S1 문헌, S2 프로젝트·벤더 문서와 소스, S3 공개 trace와 데이터셋, S4 우리 측정이 볼 수 있는가 |
| RQ0, RQ0 gate spec (3장) | 첫 실험(연구 질문 0번)과 그 판정 규칙을 미리 고정한 문서(`harness/experiments/rq0-gate.yaml`) |
| label flip, injection, `lane_share` (3장) | 같은 파일에서 정답 라벨만 바꾼 짝 만들기; 방해 프로그램 끼워 넣기; 게임 chain이 CPU 하나 중 얼마를 쓰도록 맞출지의 값 |
| exit criteria (3장) | Phase 9를 끝내는 조건(결정 8): 세 감사를 최종 상태에서 다시 돌려 미해결이 없을 것 |
| critical findings (4장) | 2026-09-13 memo가 적은 원문과 저장소의 불일치들: 발견 열셋(A1–A5, B1–B7, C)과 원문과 대조하지 못한 출처의 목록 하나(D) |
| claim inventory (4장) | 저장소가 외부 출처에서 가져온 모든 주장의 목록(`claims.md`), 판정 없음 |
| neutral topic (4장) | 저장소의 숫자와 표현을 뺀, 읽는 이에게 주는 질문(`topics.md`) |
| independent read (4장) | 저장소의 설명을 모르는 채 원문을 읽은 기록(`reads/R01–R11`) |
| comparison (4장) | 읽기 결과와 저장소 문장을 위치마다 맞댄 판정(`compare/K1–K5`) |
| 판정 어휘 (4장) | SUPPORTED, WORDING-FIX, MISATTRIBUTED, CONTRADICTED, NOT IN SOURCE, OURS-UNDER-SOURCE-TAG, UNVERIFIABLE; 9.11이 더한 NOT READ |
| measurement audit, M/D/C/X (4장) | 측정 요약을 원자료에서 재현하고 파라미터를 measured / derived / convention / 불일치로 분류한 감사 |
| compiled-number audit, HOLDS/STALE/WRONG/UNCHECKABLE (4장) | 결정 문서의 compile된 숫자 진술을 build에 대어 판정한 감사 |
| batch class, EDF cap (4장) | executor가 CPU를 오래 쓰는 행동으로 분류하는 등급과, 그 몫의 상한(`batch_bandwidth_cap`); EDF는 마감이 가장 이른 일을 먼저 돌리는 알고리즘 |
| re-analysis (5장) | 9.3이 고친 분석기를 release `meas-ci-2026-08-28`에 한 번 돌린 것. `dataset/`은 바꾸지 않음 |
| name verification, level (6장) | 프로세스 이름이 실제로 그 모양으로 나타나는지의 확인과 등급(`runtime`, `binary-only`, `package-not-found` 등) |
| campaign (6장) | 한 측정의 모든 반복. `meas-ci:<workflow>:<첫 batch 날짜>`로 태그 |
| family (6장) | 같은 workflow와 trigger 파일을 쓰는 측정 무리(interactive, playback, build, background, desktop, session, costs 등) |
| trigger 파일 (6장) | `.github/campaign*.json`. 바뀌면 그 workflow가 시작됨 |
| machine gate (6장) | AMD EPYC 7763이 아닌 runner가 아무것도 재지 않고 끝나게 하는 장치(`machine_gate.sh`) |
| settle (6장) | 프로그램을 띄운 뒤 launch 작업이 끝나기를 기다리는 시간. 프로그램마다 trace로 정하는 design |
| long-phase probe, span probe (6장, 8장) | settle을 정하거나 긴 시간에도 값이 유지되는지 보는 긴 탐침. 반복이 아니며 값을 바꾸지 않음 |
| phase (6장) | job 안의 측정 단계 하나(idle, driven, op, play, install 등) |
| wake, run, gap, component, residual, table (6장) | 깨어남; 그 깨어남의 CPU 시간; component의 깨어남 사이 간격; 프로세스 역할 안의 스레드 이름 하나; 95 %를 덮고 남은 나머지; 열 분위수와 최솟값·최댓값과 열한 구간 평균의 측정 분포 |
| per-input run, window rule (6장) | 입력 하나에서 다음 입력까지 process tree가 쓴 CPU에서 유휴 소비를 뺀 값 |
| operation (6장) | 벤치마크가 정의한 무거운 동작(page load, unsharp mask, preview render, send) |
| batch loop, voluntary block 사이의 run (6장) | 일괄 entry의 형식: 스스로 잠들기 전까지의 CPU 덩어리와 그 뒤의 block을 반복 |
| input window (6장) | 측정이 반복마다 재생한 입력 기록의 600 s 조각(`dataset/meas/streams/`) |
| repeat, landing (7장) | 새 runner 위의 job 하나; 올바른 모델을 뽑아 측정을 마친 job |
| pool, pooled record (7장) | 유효한 반복을 모아 값을 계산하는 것과 그 결과(`pooled.json`, `results.md`) |
| fold-in (7장) | pooled record의 값을 `archetypes.yaml`에 써 넣는 단계 |
| stability rule (7장) | 담는 모든 값의 95 % t 반폭이 5 % 또는 1 µs 이하, 같은 기계 반복 최소 다섯 |
| half-width, tolerance, floor (7장) | 신뢰구간의 반폭; 넘으면 안 되는 선(5 %); 시간 값의 바닥(1 µs) |
| projection (7장) | 지금의 퍼짐이면 몇 번의 반복에서 통과할지의 예측 |
| first batch (7장) | 캠페인의 첫 반복 묶음(최소 다섯) |
| 다섯 가지 예외 (7장) | machine spread, between sessions, sparse, rare event, recording runs out |
| carried value (7장) | entry가 담는 값. 예외로 담은 값은 `dataset/variants.yaml`의 `carried_values`에 반폭과 함께 |
| first crossing, binding value (7장) | 처음 기준을 통과한 순간에 멈추는 것; 그때 멈추게 한 값. 그 반폭은 낙관적 |
| validity check (8장) | 반복이 pool에 들어가기 전의 유효성 검사 |
| untraced control (8장) | 같은 단계를 perf 있이/없이 돌려 추적의 영향을 잰 대조군 |
| stimulus-sensitivity check (8장) | 다른 타이핑 기록(136M Keystrokes)으로도 재어 자극의 영향을 본 사전 등록 점검 |
| time windows (8장) | 단계를 시간 창으로 나눠 평균이 숨기는 변화를 읽는 것 |
| burstiness, dispersion (8장) | 구간별 wake 수의 분산 ÷ 평균; 측정과 compile의 몰림 비교 |
| threat to validity (8장) | 결과의 타당성을 위협하는 알려진 한계의 진술 |
| trace-replay check (8장) | 측정된 반복 하나의 흐름을 그대로 재생한 variant로 판정이 같은지 보는 Phase 10의 점검. 흐름은 entry에 따라 wake 순서(`wakes`), batch job의 run과 그 뒤의 block(`runs`), 통화의 cycle(`cycles`) |
| venue variant (8장) | 장소의 영향을 괄호로 묶기 위한 RUN ×0.8/×1.25 variant |
| release (9장) | 캠페인의 원자료를 담은 GitHub release(영구) |
| campaign record, campaign workflow (9장) | `measurement-campaign-record.md`(캠페인마다의 결과)와 `measurement-campaign-workflow.md`(공통 규칙) |
| counterpart (10장) | C7 group에서 기준 파일과 짝을 이루어 원하지 않는 백그라운드 작업이 끼어든 쪽 파일 |
| judging file (10장) | RQ0 판정에 들어가는 파일(19개, `dataset/variants.yaml`의 `judging`) |
| `validation_stats`, `modeling_notes` (10장) | entry의 출처 펼침(심판, run, 통계, scope)과, 우리가 출처 위에 얹은 것의 기록 |
| `binding_params` (10장) | archetype이 아니라 timeline이 값을 주는 파라미터 이름들(예: `total_work`) |
| fidelity map (11장) | 2026-10-10 감사의 차원별 현실 근접도 표(FAITHFUL, PROXY, STYLISED, DESIGN, UNGROUNDED) |
| research slice (12장) | Phase 9의 영역별 연구-결정 하위 작업(9.4–9.12) |
| scope card, candidates, decision session, hand-off (12장) | 조각의 할 일 목록; 네 부류 검색이 찾은 후보 정리; 항목을 하나씩 인지오에게 가져오는 결정 자리; 다음 작업으로 넘기는 changelog 항목 |
| `declared_class` (12장) | 프로그램이 스스로 정한 scheduling class를 archetype과 task 기록에 담는 필드(`normal`, `idle`) |
| class census (12장) | 모든 측정 대상의 스레드마다 policy와 nice를 조사한 것(9.11, release `meas-ci-probes-2026-10-07b`) |
| coverage sweep (13장) | changelog의 "덮음" 주장을 코드와 기록에 하나씩 대어 읽은 2026-09-28의 정리 |
| class A defect (13장) | 2026-10-10 감사에서 인지오의 결정이 필요했던 결함(감사의 A1–A4; critical findings의 A1–A5와 다름) |
| docs sweep, 9.15 (14장) | 공개 문서, memo, guidebook을 다시 지은 데이터셋에 맞추는 한 번의 정리 |
| exit audits, 9.16 (14장) | 주장, 측정, compile된 숫자의 세 감사를 최종 상태에서 다시 돌리는 일 |

## 15.2 OS·scheduling 용어

| 용어 | 뜻 |
|---|---|
| scheduler (1장) | 여러 프로그램이 CPU를 나눠 쓸 때 다음에 누가 CPU를 받을지 정하는 운영체제 부품 |
| slice, time slice (4장) | scheduler가 한 번에 주는 CPU 시간 조각 |
| context switch, voluntary / nonvoluntary (4장) | CPU가 한 스레드에서 다른 스레드로 넘어가는 일; 스스로 잠들어 넘기면 voluntary, 빼앗기면 nonvoluntary |
| comm (4장) | 커널이 프로세스마다 저장하는 실행 파일 이름, 최대 15자(`TASK_COMM_LEN` 16, NUL 포함) |
| vCPU (6장) | 가상 머신에 할당된 가상 CPU |
| pin (6장) | 프로세스를 특정 CPU에서만 돌게 묶는 것(`taskset`) |
| Xvfb (6장) | 화면 없이 메모리 안에서 도는 X 서버 |
| `perf sched record` / `timehist` (6장) | scheduler 사건(누가 언제 CPU에 오르내렸고 누가 깨웠는지)을 기록하고 읽는 Linux 도구 |
| taskstats (6장) | 스레드가 끝날 때 커널이 넘겨주는 회계 기록(CPU, 경과 시간, block I/O 지연, nice, policy) |
| schedule-in (6장) | 스레드가 CPU를 받는 순간 |
| preemption (6장) | 스레드가 스스로 잠들지 않았는데 scheduler가 CPU를 빼앗는 것 |
| voluntary block (6장) | 스레드가 I/O나 사건을 기다리며 스스로 CPU를 내려놓는 것 |
| DKMS (6장) | 커널이 바뀔 때 외부 커널 모듈을 다시 빌드하는 장치 |
| chroot (6장) | 디렉터리 하나를 새 루트 파일시스템처럼 쓰는 격리 환경 |
| EEVDF (6장) | Linux의 현재 기본 공정 scheduler |
| lane (6장) | simulator가 흉내 내는 CPU 하나 |
| RTKit (11장) | 데스크톱 프로그램에 실시간 우선순위를 나눠 주는 서비스 |
| Proton (11장) | Windows 게임을 Linux에서 돌리는 Valve의 호환 계층 |
| cgroup slice (11장) | systemd가 프로세스 무리를 묶어 CPU 무게를 주는 단위(예: `app.slice`, `background.slice`) |
| scheduling policy, `SCHED_IDLE` (12장) | 스레드가 속한 scheduling 규칙의 종류; 다른 일이 있으면 거의 CPU를 받지 못하는 가장 낮은 policy(커널 무게 3) |
| nice (12장) | 보통 policy 안의 상대적 무게를 정하는 -20부터 19까지의 값(높을수록 덜 받음) |

