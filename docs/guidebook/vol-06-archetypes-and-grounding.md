# 6권 · Workload 1: 재료와 근거

**archetype의 숫자들은 어디서 왔나**

---

앞 권은 인식기가 답하는 어휘를 다뤘습니다. 열여섯 개의 mode와 참거짓 하나가 무엇을 뜻하고, 그 목록이 어디서 왔고, 어디까지가 한 이름이고 어디부터가 옆 이름인지였습니다. 그 라벨들은 workload 파일, 즉 시뮬레이터에서 돌릴 작업 부하를 시간 순서로 적은 파일의 한 구간에 붙습니다. 그러면 곧바로 다음 질문이 나옵니다. **라벨이 붙는 그 구간 안에서, 프로세스들은 실제로 무엇을 하고 있나.**

이 권은 그 가장 아래층을 다룹니다. 음악 재생기는 몇 밀리초마다 깨어나서 얼마나 일하나. 컴파일러 자식 프로세스 하나는 얼마나 오래 사나. 게임 하나는 task를 몇 개 만들고 그 task들은 서로를 어떻게 깨우나. 이런 것을 규칙과 숫자로 적어둔 것을 저장소는 **archetype**이라고 부릅니다. 우리말로 옮기면 "원형"쯤 되는데, 이 책에서는 저장소에 적힌 대로 archetype이라고 씁니다.

답해야 할 질문은 이겁니다. **archetype의 숫자들은 어디서 왔나.** 숫자 하나마다 그 숫자가 어느 문서의 어느 문장에서 나왔는지, 그 문서가 어떤 등급의 근거인지, 그 문장과 우리 숫자 사이에 우리가 무엇을 덧붙였는지를 봅니다. 그리고 그 사슬이 어디서 끊기는지도 봅니다. 이 권에서는 원문을 그대로 옮기는 자리가 많습니다. 숫자의 근거를 말하려면 그 숫자가 적힌 문장을 보여주는 것이 가장 정직하기 때문입니다.

---

## 목차

1. [scheduler의 눈에 프로세스는 무엇인가](#1장--scheduler의-눈에-프로세스는-무엇인가)
2. [여섯 개의 primitive](#2장--여섯-개의-primitive)
3. [archetype 하나는 어떻게 정의되는가](#3장--archetype-하나는-어떻게-정의되는가)
4. [한 항목에 적히는 것](#4장--한-항목에-적히는-것)
5. [근거의 네 등급](#5장--근거의-네-등급)
6. [열두 개의 목록](#6장--열두-개의-목록)
7. [존재의 근거: 수확](#7장--존재의-근거-수확)
8. [충분함의 근거: 검증](#8장--충분함의-근거-검증)
9. [개수도 숫자다](#9장--개수도-숫자다)
10. [우리가 직접 잰 것](#10장--우리가-직접-잰-것)
11. [손으로 따라가기: compiler-child를 끝까지](#11장--손으로-따라가기-compiler-child를-끝까지)
12. [근거가 약한 자리](#12장--근거가-약한-자리)
13. [용어 정리](#13장--용어-정리)

---

# 1장 · scheduler의 눈에 프로세스는 무엇인가

## 1.1 이름표를 떼고 보면

작업 관리자를 열면 프로그램마다 이름이 붙어 있습니다. `chrome`, `code`, `spotify`. 사람에게는 그 이름이 곧 그 프로그램입니다.

scheduler에게는 그렇지 않습니다. 1권에서 봤듯이 scheduler가 하는 일은 지금 실행할 준비가 된 task들 가운데 누구에게 CPU를 줄지 고르는 것입니다. 여기서 **task**는 scheduler가 실행 여부를 결정하는 단위 하나를 말하고, 대개 thread 하나에 해당합니다. 그리고 그 결정을 내리는 데 이름은 쓰이지 않습니다. scheduler가 보는 것은 task가 **언제 무엇을 했는가**뿐입니다.

task 하나의 일생을 scheduler 쪽에서 적으면 이런 모양이 됩니다.

```text
   시각      무슨 일이 있었나
   ──────────────────────────────────────────────
   0 ms      실행할 준비가 됐다
   0 ms      CPU를 받아 2.5 ms 동안 계산했다
   2.5 ms    스스로 잠들었다. 다음 알람까지 기다린다
   50 ms     알람이 울려서 다시 준비가 됐다
   50 ms     CPU를 받아 2.5 ms 동안 계산했다
   52.5 ms   다시 잠들었다
   …
```

이 목록 어디에도 "음악 재생기"라는 말이 없습니다. 50밀리초마다 깨어나서 2.5밀리초 일한다는 사실만 있습니다. 이렇게 시각과 사건이 이어진 흐름을 **event stream**이라고 부릅니다. 사건들이 시간 순서로 흘러가는 줄이라는 뜻입니다.

**scheduler에게 프로세스는 이 흐름이 전부입니다.** 이름도 없고 의미도 없습니다.

웹 서비스로 치면 로드 밸런서가 보는 요청과 비슷합니다. 로드 밸런서는 요청이 언제 들어왔고 얼마나 오래 걸렸고 연결이 언제 끊겼는지를 압니다. 그 요청이 결제인지 이미지 업로드인지는 모릅니다. 그걸 몰라도 트래픽을 나눌 수는 있습니다. 다만 결제 요청을 먼저 처리해야 하는 순간이 오면, 그 판단은 로드 밸런서 혼자서는 못 합니다.

## 1.2 archetype은 그 흐름을 만드는 규칙입니다

저장소는 archetype을 이렇게 정의합니다. 계획 문서의 첫 문단을 그대로 옮깁니다.

> "An archetype is a **generative model of one process as the scheduler sees it**. To the scheduler a process has no name and no meaning — only an event stream: when it becomes runnable, how long it runs, what it blocks on, whom it wakes, when it forks and exits. An archetype is the rule-plus-parameters bundle that emits that stream."

풀어보면 이렇습니다. archetype은 **scheduler가 보는 모습대로 적은 프로세스 하나의 생성 모형**입니다. **generative model**, 우리말로 생성 모형은 데이터를 요약한 것이 아니라 데이터를 만들어낼 수 있는 규칙이라는 뜻입니다. scheduler에게 프로세스는 이름도 의미도 없고 사건의 흐름만 있습니다. 언제 실행 가능해지는지, 얼마나 오래 도는지, 무엇을 기다리며 멈추는지, 누구를 깨우는지, 언제 자식을 만들고 끝나는지입니다. archetype은 그 흐름을 뱉어내는 **규칙과 파라미터의 묶음**입니다.

두 부분으로 나눠 보면 이해가 쉽습니다.

```text
   archetype = 규칙           +  파라미터
               ─────             ─────────
               "알람을 맞추고     "알람 간격은 50 ms,
                울리면 계산한다    계산은 2.5 ms"
                이걸 반복한다"
```

규칙은 모양이고 파라미터는 크기입니다. 이 권의 대부분은 **파라미터 쪽**, 즉 숫자들이 어디서 왔는지를 다룹니다. 다만 규칙의 모양에도 근거가 필요하고, 그 이야기도 함께 합니다.

> **코드로.** archetype은 `dataset/archetypes.yaml` 한 파일에 들어 있습니다. 열두 개의 항목이 있고, 항목 하나가 archetype 하나입니다. 이 파일이 규범입니다. 무엇이 들어가야 하는지와 왜 그런지를 적은 설명 문서는 `docs/workload/archetype-plan.md`입니다. 둘이 어긋나면 파일이 맞습니다. 이 권에서도 둘이 어긋나는 자리가 여러 번 나오고, 그때마다 표시해둡니다.

## 1.3 archetype이 모르는 셋

정의에서 곧바로 따라 나오는 규칙이 있습니다. **scheduler가 볼 수 없는 것은 archetype에 들어갈 수 없다.** 저장소가 이 규칙으로 명시적으로 빼는 것이 셋입니다.

### 이름

archetype은 프로세스 이름을 모릅니다. `audio-playback`이라는 archetype은 "50 ms마다 깨어나 2.5 ms 일한다"만 압니다. 그게 `spotify`인지 `mpv`인지 `zoom`의 소리 담당 부분인지는 모릅니다.

이름은 한 층 위에서 붙습니다. timeline이라는 파일에서 "이 구간에 `spotify`라는 이름의 task가 있고, 그 task는 `audio-playback`처럼 행동한다"라고 짝을 지어줍니다. **timeline**은 사람이 손으로 쓰는 workload 설계 파일로, 시간축 위에 구간과 라벨과 task들을 배치한 것입니다. 이 짝짓기를 **binding**이라고 부릅니다. 이름과 행동을 묶어준다는 뜻입니다.

### 개수

archetype은 자기가 몇 개 떠 있는지 모릅니다. 브라우저 탭 프로세스가 열두 개인지 스물다섯 개인지, 컴파일러 자식이 백 개인지 이천 개인지는 archetype의 값이 아닙니다. 이것도 binding에서 정해집니다. 개수가 왜 따로 다뤄지는지, 그리고 개수에도 근거가 필요하다는 것이 무슨 뜻인지는 뒤에서 한 장을 들여 봅니다.

### 의미

archetype은 자기가 어떤 상황에 쓰이는지 모릅니다. 똑같이 CPU를 계속 쓰는 archetype이 한 파일에서는 사용자가 시작한 머신러닝 학습이고, 다른 파일에서는 아무도 부탁하지 않은 파일 색인입니다. "원하는 작업인가"라는 판단은 구간의 라벨에 붙어 있고, archetype에는 없습니다.

```text
   archetype 안에 있는 것         archetype 밖에 있는 것
   ─────────────────────         ──────────────────────
   계산을 얼마나 하나              프로세스 이름        ← binding
   얼마나 자주 깨어나나            몇 개가 떠 있나      ← binding
   무엇을 기다리나                 어떤 상황의 일부인가  ← 구간 라벨
   누구를 깨우나
   언제 자식을 만드나
```

## 1.4 이 경계가 실험을 지킵니다

이 경계가 왜 그렇게 중요한지는 4권에서 본 **정보 비대칭**을 떠올리면 보입니다. workload 파일 하나에 세 종류의 정보가 들어 있고, 각각을 볼 수 있는 쪽이 정해져 있다는 것이었습니다. 이름은 인식기만 보고, 행동은 시뮬레이터만 보고, 정답 라벨은 완벽한 인식 조건과 채점기만 봅니다.

archetype은 그중 **행동**입니다. 그리고 행동이 이름과 섞이지 않아야 실험이 성립합니다. 이 연구의 핵심 주장은 "행동으로는 구분되지 않는 상황을 이름으로 구분할 수 있다"입니다. 그 주장을 시험하려면 행동이 정말로 같은 두 파일이 필요합니다.

이 연구에서 가장 중요한 한 쌍의 파일을 다시 보겠습니다. 두 파일 모두 편집기 `code` 옆에서 CPU를 계속 쓰는 작업이 하나 도는데, 한쪽 이름은 `python3`이고 다른 쪽은 `tracker-miner-fs-3`입니다.

```text
   파일 c2-p1a                         파일 c2-p1b
   ──────────────                      ──────────────
   code     → desktop-interactive      code                → desktop-interactive
   python3  → cpu-batch                tracker-miner-fs-3  → cpu-batch
```

**두 줄의 오른쪽이 같습니다.** archetype이 이름을 모르기 때문에, 이름을 바꿔도 행동은 한 글자도 바뀌지 않습니다. 저장소는 두 파일이 그 한 곳 말고는 바이트 단위로 같다는 것을 자동 검사로 확인합니다.

만약 archetype이 이름을 알고 있었다면 어떻게 될까요. 예를 들어 `python3`일 때만 계산량을 조금 늘리는 규칙이 archetype 안에 있었다면, 두 파일의 행동이 달라집니다. 그러면 모델이 두 파일을 구분했을 때 그게 이름을 읽어서인지 행동 차이 때문인지 알 수 없게 됩니다. **실험이 시험하려는 바로 그 변수에 다른 변수가 섞이는 것**입니다.

> **이 연구에서는.** 경계는 계획 문서에 두 문장으로 적혀 있습니다. 첫 문장은 방금 본 것입니다.
>
> > "what the scheduler cannot observe cannot live in an archetype — process *names* (bound in Layer 2/3), *counts* (§3), and *meaning* (segment-label concerns) are excluded by construction."
>
> scheduler가 관찰할 수 없는 것은 archetype 안에 살 수 없다. 이름과 개수와 의미는 **구성상** 빠져 있다. "구성상"이라는 말이 중요합니다. 조심해서 안 넣는 것이 아니라 넣을 자리 자체가 없게 만들어져 있다는 뜻입니다.
>
> 두 번째 문장은 출처 표시가 무엇을 정당화하는지에 대한 것인데, 그건 항목의 필드들을 볼 때 따로 다룹니다.

## 1.5 archetype의 숫자는 어디로도 새지 않습니다

경계의 다른 쪽도 있습니다. archetype의 숫자들은 **인식기에게도, driver table에게도 가지 않습니다.** driver table은 5권에서 본, 인식기의 답을 받아 scheduler 설정을 꺼내는 표입니다.

실행 계약 문서의 문장입니다.

> "archetype numbers never reach the recognizer or the driver table — they build the simulated machine the executor schedules. They set the cost of misrecognition; realistic deadlines, fork storms, and chains are what make good and bad configs diverge in Layer 2."

archetype의 숫자는 인식기에도 driver table에도 닿지 않는다. 그 숫자들은 **executor가 scheduling하는 가상의 기계를 짓는 데** 쓰인다. **executor**는 시뮬레이터 안에서 실제로 scheduling 알고리즘을 돌리는 부분입니다. 그리고 그 숫자들이 하는 일이 하나 더 적혀 있습니다. **잘못 인식했을 때의 비용을 정한다.** 현실적인 deadline, 자식 프로세스가 한꺼번에 쏟아지는 순간, 여러 task가 이어진 chain 같은 것들이 있어야 좋은 설정과 나쁜 설정의 결과가 벌어진다는 것입니다. 여기서 **Layer 2**는 4권에서 본 측정의 두 번째 층, 즉 설정이 실제 scheduling 결과를 얼마나 바꾸는지를 재는 층입니다.

이 문장이 이 권 전체의 무게를 정합니다.

```text
   archetype의 숫자가 엉터리라면

   인식 정확도 (Layer 1)        → 영향 없음
                                  모델은 이름만 보니까

   설정의 효과 (Layer 2)        → 영향이 큼
                                  "나쁜 설정이 얼마나 나쁜가"가
                                  그 숫자들로 정해지니까
```

예를 들어 게임 frame 하나가 실제로는 CPU를 10밀리초 쓰는데 archetype이 1밀리초라고 적어뒀다고 해봅시다. 그러면 가상의 기계가 너무 한가해서, 어떤 설정을 줘도 frame이 제때 나옵니다. 올바른 설정과 틀린 설정의 차이가 사라집니다. 그 상태에서 "상황을 알아도 별 이득이 없다"는 결과가 나오면, 그건 세상에 대한 발견이 아니라 **숫자를 잘못 넣은 결과**입니다.

**그래서 숫자마다 근거가 필요합니다.** 이 권이 한 권을 통째로 들이는 이유입니다.

## 1.6 archetype이 사는 층

마지막으로 archetype이 전체 구조에서 어디 있는지를 한 번 봅니다.

```text
   Layer 1  ARCHETYPE LIBRARY   프로세스 하나가 어떻게 행동하나     archetypes.yaml
   Layer 2  SCENARIO CATALOG    어떤 프로세스들이 함께 뜨나          S1–S18
   Layer 3  TIMELINES           상황들이 시간 위에 어떻게 놓이나     *.timeline.yaml
```

여기서 Layer 1, 2, 3은 **데이터셋을 쌓는 층**입니다. 4권에서 본 **측정의** Layer 1, Layer 2와 이름이 같지만 다른 것입니다. 이 권에서 헷갈릴 만한 자리에서는 "데이터셋의 첫 층", "측정의 두 번째 층"처럼 풀어 쓰겠습니다.

데이터셋의 층에는 규칙이 하나 있습니다. **아래 층은 위 층을 모릅니다.** archetype은 상황 목록을 모르고, 상황 목록은 timeline을 모릅니다. 그리고 규칙이 하나 더 있습니다.

> "The binding rule: **numeric behavior parameters exist only in Layer 1.** Scenarios reference archetypes by id; timelines reference scenarios and archetypes by id; no file copies a number."

행동을 나타내는 숫자 파라미터는 **데이터셋의 첫 층에만** 있다. 상황 목록은 archetype을 id로 가리키고, timeline은 상황과 archetype을 id로 가리키고, 어떤 파일도 숫자를 복사하지 않는다.

데이터베이스를 설계해본 사람에게는 익숙한 규칙입니다. **정규화**입니다. 같은 값을 여러 테이블에 복사해두면 언젠가 하나만 고쳐지고 나머지는 옛날 값으로 남습니다. 그래서 값은 한 곳에 두고 나머지는 외래 키로 가리키게 합니다. 여기서 archetype id가 그 외래 키 역할을 합니다.

이 규칙 덕에 생기는 이득이 계획 문서에 셋 적혀 있습니다. 문헌이나 측정이 바뀌면 파일 수십 개가 아니라 archetype 항목 하나만 고치면 된다는 것, 출처를 검사하는 도구가 한 층만 보면 된다는 것, 그리고 "같은 archetype에 다른 이름"이라는 파일을 만들 수 있어서 인식 결과의 차이가 이름 때문이라고 보장할 수 있다는 것입니다.

> **논문으로.** 이 층 구조와 숫자 한 곳 규칙은 논문에서 데이터셋 구성 절의 뼈대가 됩니다. 그리고 이 규칙이 논문에 쓸 수 있는 강한 문장 하나를 가능하게 합니다. 저장소 문서가 그 문장을 이렇게 적어둡니다.
>
> > "every numeric parameter in the dataset traces to an external source or to our released measurements."
>
> 데이터셋의 모든 숫자 파라미터는 외부 출처나 우리가 공개한 측정으로 추적된다. 그리고 이 문장이 사람의 주장이 아니라 **기계가 검사하는 사실**이라는 것이 핵심입니다. 숫자가 한 층에만 있으니 검사 도구가 그 층의 숫자마다 출처 표시가 붙어 있는지 확인할 수 있습니다. 다만 "추적된다"가 "그 출처가 그 숫자를 정말로 말한다"와 같은 뜻은 아닙니다. 이 둘의 간격이 이 권 뒤쪽의 주제입니다.

---

## 1장 정리

- scheduler에게 프로세스는 이름도 의미도 없고 사건의 흐름만 있습니다. 언제 실행 가능해지는지, 얼마나 도는지, 무엇을 기다리는지, 누구를 깨우는지, 언제 자식을 만들고 끝나는지입니다.
- archetype은 그 흐름을 만들어내는 규칙과 파라미터의 묶음입니다. 데이터를 요약한 것이 아니라 데이터를 만들어내는 생성 모형입니다.
- scheduler가 볼 수 없는 것은 archetype에 들어갈 수 없습니다. 이름, 개수, 의미 셋이 구성상 빠져 있고, 이름과 개수는 binding에서, 의미는 구간 라벨에서 붙습니다.
- 이 경계가 실험을 지킵니다. archetype이 이름을 모르기 때문에 이름만 바꾼 두 파일의 행동이 바이트 단위로 같고, 그래서 인식 결과의 차이를 이름에 돌릴 수 있습니다.
- archetype의 숫자는 인식기에도 driver table에도 가지 않습니다. 가상의 기계를 짓는 데 쓰이고, 잘못 인식했을 때의 비용을 정합니다.
- 그래서 숫자가 엉터리이면 인식 정확도는 멀쩡하고 설정의 효과를 재는 층이 오염됩니다. 너무 가벼운 숫자는 좋은 설정과 나쁜 설정의 차이를 지웁니다.
- 데이터셋은 세 층으로 쌓이고 행동 숫자는 첫 층에만 있습니다. 데이터베이스 정규화와 같은 규칙이고, 덕분에 모든 숫자에 출처가 붙어 있는지를 기계로 검사할 수 있습니다.

---

# 2장 · 여섯 개의 primitive

## 2.1 행동을 프로그램으로 적습니다

archetype의 규칙 부분은 **작은 프로그램**으로 적힙니다. 사람이 쓰는 프로그래밍 언어가 아니라, 명령어가 딱 여섯 개뿐인 아주 작은 언어입니다. 그 명령 하나하나를 **primitive**라고 부릅니다. 더 쪼갤 수 없는 기본 동작이라는 뜻입니다.

음악 재생기를 흉내 내는 archetype의 규칙은 파일에 이렇게 적혀 있습니다.

```yaml
pattern:
  program:
    - loop:
        - TIMER: period
        - RUN: burst
```

읽으면 이렇습니다. "반복한다. 알람이 울릴 때까지 기다린다. 울리면 `burst`만큼 계산한다." `period`와 `burst`는 이름만 적혀 있고 값은 파라미터 쪽에 따로 있습니다.

`loop`는 여섯 primitive에 들어가지 않습니다. 반복이라는 제어 흐름일 뿐 scheduler가 볼 수 있는 사건을 만들지 않기 때문입니다. 프로그래밍 언어의 `for`가 기계어 명령이 아닌 것과 같습니다.

## 2.2 여섯 개를 하나씩

실행 계약 문서가 여섯 개의 뜻을 표 하나로 정해두었습니다. 표의 문장을 그대로 옮기고 하나씩 풀겠습니다.

### RUN

> `RUN(duration)` — "burn CPU for `duration` of lane time (may be preempted; duration is CPU demand, not wall time)"

`duration`만큼 lane 시간을 태운다. 도중에 빼앗길 수 있다. `duration`은 CPU 요구량이지 벽시계 시간이 아니다.

**lane**은 이 연구의 시뮬레이터가 가진 CPU 자리 하나를 부르는 이름입니다. 시뮬레이터는 CPU가 하나뿐인 기계를 흉내 내고, 그 한 자리에 한 번에 한 task만 앉을 수 있습니다.

괄호 안의 문장이 중요합니다. `RUN(2500)`은 "2.5밀리초 뒤에 끝난다"가 아니라 "**CPU를 2.5밀리초어치 받으면** 끝난다"입니다. 중간에 다른 task에게 자리를 뺏기면 벽시계로는 10밀리초가 걸릴 수도 있습니다. 식당으로 치면 "요리에 20분 걸린다"는 요리사가 그 요리에 손을 댄 시간의 합이지, 주문부터 서빙까지의 시간이 아닙니다.

1권의 상태 이름으로 말하면 RUN은 task가 **running** 상태에 있으려고 하는 구간입니다.

### SLEEP

> `SLEEP(duration)` — "voluntary relative wait; task not runnable until now+duration"

스스로 하는 **상대적** 대기. 지금부터 `duration`이 지날 때까지 실행할 수 없다.

"상대적"이라는 말은 **기준점이 지금**이라는 뜻입니다. 언제 잠들든 잠든 순간부터 잽니다. 1권의 상태 이름으로는 스스로 **blocked**로 가는 것, 즉 voluntary하게 CPU를 놓는 것입니다.

### TIMER

> `TIMER(period)` — "absolute periodic wake: runnable at t₀+k·period regardless of when the previous iteration finished — drift-free (rt-app `timer{ref,period}`). Late iterations accumulate as backlog; they are not silently skipped"

**절대적인** 주기 깨어남. 이전 반복이 언제 끝났든 상관없이 t₀ + k·period 시각에 실행 가능해진다. 어긋남이 쌓이지 않는다. 늦어진 반복은 backlog로 쌓이고 조용히 건너뛰어지지 않는다.

t₀는 처음 시작한 시각이고 k는 0, 1, 2, 3으로 늘어나는 정수입니다. 그러니까 period가 50밀리초이면 깨어나는 시각은 0, 50, 100, 150밀리초로 **처음부터 정해진 눈금**입니다. 앞 반복이 늦게 끝났다고 다음 눈금이 밀리지 않습니다.

**backlog**는 1권에서 본 대로 처리하지 못하고 밀린 일이 쌓인 상태입니다. 눈금이 이미 지나갔는데 아직 앞 일을 하고 있으면, 지나간 눈금이 버려지지 않고 밀린 일로 남습니다. 그 밀린 일이 시뮬레이터에서 정확히 어떤 순서로 처리되는지는 시뮬레이터를 다루는 권의 몫입니다. 여기서는 **버리지 않는다**는 선택까지만 봅니다.

### WAIT

> `WAIT(channel)` — "block until a WAKE (or exogenous wake event) on `channel`"

`channel`에 WAKE가 오거나 바깥에서 오는 깨움 사건이 올 때까지 멈춘다.

**channel**은 "무엇을 기다리는가"에 붙인 이름입니다. SLEEP과 TIMER가 **시간**을 기다린다면 WAIT는 **사건**을 기다립니다. 언제 올지 task 자신은 모릅니다.

이 연구의 archetype에 나오는 channel은 성격이 두 가지입니다.

```text
   누군가 깨워주는 channel
   ──────────────────────
   input      사람의 입력. 키 입력 시각이 바깥 사건으로 파일에 적혀 온다
   upstream   게임 chain에서 앞 단계 task가 WAKE로 깨워준다
   children   make가 자식들이 전부 끝나기를 기다린다

   깨워줄 task가 없는 channel
   ────────────────────────
   disk, io, net   디스크나 네트워크를 기다리는 시간
```

뒤쪽 셋은 사정이 다릅니다. 이 시뮬레이터에는 디스크도 네트워크도 없습니다. CPU만 흉내 냅니다. 그러니 디스크를 기다리는 task를 깨워줄 무언가가 없습니다. 이런 WAIT는 "이만큼의 시간 동안 CPU를 쓰지 않고 멈춰 있다"로 바뀌어 들어갑니다.

> **코드로.** 이 변환은 **compile** 단계에서 일어납니다. compile은 timeline과 archetype을 합쳐서 모든 분포를 구체적인 숫자로 바꾸고, 시뮬레이터가 읽는 workload 파일을 만드는 단계입니다. 규칙은 단순합니다. archetype의 파라미터 중에 `disk_wait`처럼 channel 이름 뒤에 `_wait`가 붙은 것이 있으면, 그 WAIT는 그 값만큼의 SLEEP으로 바뀝니다. 없으면 진짜 channel로 남습니다. 규칙은 `dataset/tools/wlc/compiler.py`에 있고, compile 과정 전체는 다음 권에서 봅니다.
>
> 그래서 archetype 파일에는 `WAIT: disk`라고 적혀 있는데 시뮬레이터가 받는 파일에는 SLEEP이 들어 있습니다. archetype 쪽이 "이건 디스크를 기다리는 시간이다"라는 **뜻**을 보존하고, 실행 쪽이 "지금 이 시뮬레이터에서는 그냥 시간이다"라고 **구현**합니다.

### WAKE

> `WAKE(target)` — "make `target` runnable (waker–waiter edges)"

`target`을 실행 가능한 상태로 만든다. 깨우는 쪽과 기다리는 쪽 사이에 선이 생긴다.

1권에서 본 **chain**이 이 primitive로 만들어집니다. task A가 일을 마치고 WAKE로 B를 깨우고, B가 일을 마치고 C를 깨우는 모양입니다. 이 연구에서 WAKE를 쓰는 archetype은 게임 하나뿐입니다.

### FORK와 EXIT

> `FORK` / `EXIT` — "create the next child from the spawn table (§5) / terminate this task"

FORK는 spawn table에서 다음 자식을 만든다. EXIT은 이 task를 끝낸다.

**spawn table**은 자식 프로세스들의 목록입니다. 컴파일을 지휘하는 `make`가 컴파일러 자식을 줄줄이 만들 때, 어떤 자식들이 태어날지를 미리 적어둔 표입니다. FORK 한 번이 그 표의 다음 줄 하나를 꺼내 task로 만듭니다.

EXIT은 1권의 **done** 상태로 가는 것입니다.

## 2.3 1권의 상태 그림에 겹쳐보면

여섯 개가 어디서 왔는지는 1권의 상태 전이 그림에 겹쳐보면 한눈에 보입니다. 1권에서 task는 running, ready, blocked, done 네 상태를 오간다고 했습니다.

| primitive | task가 요청하는 것 | 1권의 상태로 말하면 |
|---|---|---|
| RUN | CPU를 이만큼 쓰고 싶다 | running에 있으려 한다. 빼앗기면 ready로 밀려난다 |
| SLEEP | 지금부터 이만큼 잔다 | 스스로 blocked로 간다. 시간이 지나면 ready |
| TIMER | 다음 눈금까지 잔다 | 스스로 blocked로 간다. 눈금이 오면 ready |
| WAIT | 이 사건이 올 때까지 잔다 | 스스로 blocked로 간다. 사건이 오면 ready |
| WAKE | 저 task를 깨운다 | 다른 task를 blocked에서 ready로 옮긴다 |
| FORK / EXIT | 자식을 만든다 / 끝낸다 | 새 task가 ready로 태어난다 / done |

**표의 오른쪽 열에 scheduler가 하는 일이 하나도 없습니다.** ready에서 running으로 누구를 올릴지는 전부 빠져 있습니다. primitive는 task가 **원하는 것**만 적고, 원하는 대로 되는지는 scheduler가 정합니다. 이 분리가 이 작은 언어의 설계 원칙입니다.

그래서 같은 program을 서로 다른 scheduler 설정 아래에서 돌리면 결과가 달라집니다. RUN(2500)은 어떤 설정에서는 벽시계 2.5밀리초에 끝나고 어떤 설정에서는 30밀리초가 걸립니다. **그 차이가 이 연구가 재려는 것입니다.**

## 2.4 왜 이 여섯인가

### 선례가 있습니다

task의 행동을 몇 가지 기본 동작의 나열로 적는 방식은 이 연구가 발명한 것이 아닙니다. 2권에서 본 rt-app이라는 도구가 이미 그렇게 합니다. rt-app은 주기적인 실시간 부하를 흉내 내려고 만든 도구이고, task의 동작을 JSON 파일에 적습니다. 그 설명서가 쓸 수 있는 동작으로 이런 것들을 듭니다.

> "* sleep : Integer. Emulate the sleep of a task. The duration is defined in usec."

> "* timer : Object. Emulate the wake up of the thread by a timer. Timer differs from sleep event by the start time of the timer duration. Sleep duration starts at the beginning of the sleep event whereas timer duration starts at the end of the last use of the timer. So Timer event are immunized against preemption, frequency scaling and computing capacity of a CPU."

sleep은 task의 잠을 흉내 내고, 길이는 마이크로초로 적는다. timer는 타이머에 의한 깨어남을 흉내 낸다. 둘의 차이는 **시간을 언제부터 재느냐**다. sleep은 sleep 사건이 시작할 때부터 재고, timer는 마지막으로 그 timer를 쓴 끝에서부터 잰다. 그래서 timer 사건은 preemption에도, 주파수 조절에도, CPU 성능 차이에도 영향을 받지 않는다.

이 연구의 SLEEP과 TIMER가 이 두 동작을 그대로 따릅니다. 시간 단위를 마이크로초 정수로 쓰는 것도 같습니다.

> **이 연구에서는.** 저장소는 rt-app을 **형식의 선례**로만 인용합니다. 출처 등록부에 적힌 문장입니다.
>
> > "Schema-shape precedent only; no numeric values are derived from it."
>
> 스키마 모양의 선례일 뿐이고, 여기서 숫자는 하나도 가져오지 않는다. rt-app 설명서의 예제에는 "100밀리초마다 깨어나 10밀리초 실행" 같은 값이 있지만, 그 값은 이 데이터셋 어디에도 쓰이지 않습니다. 모양만 빌려오고 숫자는 다른 곳에서 가져온다는 구분이 이 권 내내 반복됩니다.

> **확인함.** 2026-09-13에 rt-app 원본 저장소(github.com/scheduler-tools/rt-app, 커밋 `d6f8be41`, 2026-06-10)를 받아 `doc/tutorial.txt`에서 위의 두 문단을 읽었습니다. 인용은 원문 그대로이고, 원문의 문법 오류("Timer event are")도 고치지 않았습니다.

### 여섯이면 충분한가

primitive가 여섯 개로 정해지기 전에 "이것으로 충분한가"라는 질문이 열려 있었습니다. 처음 후보로 거론된 빈틈은 **입출력 대역폭**이었습니다. 디스크를 여러 task가 동시에 쓰면 서로 느려지는데, 그걸 표현할 방법이 없다는 것이었습니다.

2026년 8월 26일에 이 질문이 닫혔습니다. 결론은 **진짜 빈틈은 입출력이 아니라 절대 시각이었다**는 것입니다. 입출력 경쟁은 시뮬레이터가 CPU만 흉내 내는 동안에는 어차피 범위 밖이고, 그보다 급한 문제는 "정해진 박자로 깨어나는 일"을 SLEEP만으로는 제대로 적을 수 없다는 것이었습니다. 그래서 TIMER가 여섯 번째로 들어왔습니다.

## 2.5 주기 작업은 왜 SLEEP이 아니라 TIMER인가

이 장에서 가장 중요한 결정입니다. 계약 문서가 한 문장으로 못 박아둡니다.

> "Periodic tasks use TIMER, never SLEEP loops: relative sleeps drift under delay, silently lowering demand exactly under bad configs."

주기 작업은 TIMER를 쓰고 SLEEP 반복은 절대 쓰지 않는다. 상대적인 잠은 지연이 생기면 어긋나서, **정확히 나쁜 설정 아래에서 요구량을 조용히 줄인다.**

말로는 잘 안 와닿으니 rt-app 설명서가 드는 예를 먼저 보겠습니다.

> "As an example to point out the difference between sleep and timer, let consider a task A that run 5 and then sleep 10. The period of task A should be 15. Let's add a task B that runs 5 and use a timer to wakes up every 19."

> "We can see that task B period stays to 19 even if the run event is delayed because of scheduling preemption whereas the period of task A starts at 15 but increases to 19 because of the scheduling delay."

5만큼 돌고 10만큼 자는 task A의 주기는 15여야 한다. 5만큼 돌고 19마다 timer로 깨는 task B를 더하자. 그러면 B의 주기는 실행이 preemption으로 늦어져도 19로 유지되지만, A의 주기는 15로 시작했다가 scheduling 지연 때문에 19로 늘어난다.

### 손으로 계산해봅니다

이 연구의 숫자로 똑같이 해보겠습니다. 초당 60번 화면을 그리는 영상 재생 task입니다. 한 주기가 16.667밀리초이고 그중 6.667밀리초를 계산합니다.

**SLEEP으로 적었다면** 이런 프로그램이 됩니다.

```text
   반복: RUN(6.667 ms) → SLEEP(10 ms)
```

아무도 방해하지 않으면 한 바퀴가 6.667 + 10 = 16.667밀리초이고, 1초에 60번 돕니다. CPU 요구량은 6.667 / 16.667 = **40퍼센트**입니다.

이제 나쁜 설정 아래에서 매 바퀴 CPU를 5밀리초씩 늦게 받는다고 해봅시다.

```text
   한 바퀴 = 기다림 5 ms + RUN 6.667 ms + SLEEP 10 ms = 21.667 ms

   1초에 도는 횟수 = 1000 / 21.667 ≈ 46번
   CPU 요구량     = 6.667 / 21.667 ≈ 30.8퍼센트
```

**무슨 일이 일어났나요.** 설정이 나빠서 task가 늦어졌는데, 그 결과로 task가 **CPU를 덜 원하게** 됐습니다. 40퍼센트였던 요구량이 30.8퍼센트로 떨어졌습니다. 1초에 60장을 그려야 하는 재생기가 46장만 그리겠다고 하고 있습니다.

그런데 시뮬레이터 입장에서는 이게 실패로 보이지 않습니다. task는 매번 자기가 원한 만큼 계산했고, 잠든 시간도 정확했습니다. **deadline을 놓친 기록이 남지 않습니다.** 늦어진 만큼 요구 자체가 줄었기 때문입니다.

**TIMER로 적으면** 다릅니다.

```text
   반복: TIMER(16.667 ms) → RUN(6.667 ms)

   깨어나는 눈금: 0, 16.667, 33.333, 50.0, … ms  (처음부터 고정)
```

5밀리초 늦게 CPU를 받아도 다음 눈금은 그대로입니다. 1초에 60번 깨어나야 한다는 요구가 유지되고, 따라가지 못하면 밀린 일이 쌓입니다. **나쁜 설정이 나쁘다는 사실이 기록에 남습니다.**

```text
                        좋은 설정       나쁜 설정 (매번 5 ms 지연)
   ─────────────────    ─────────       ─────────────────────────
   SLEEP으로 적으면      40% 요구         30.8% 요구, 실패 기록 없음
   TIMER로 적으면        40% 요구         40% 요구 유지, 밀린 일이 쌓임
```

### 왜 이게 실험을 망치나

이 연구가 측정의 두 번째 층에서 재려는 것은 **올바른 설정과 틀린 설정의 차이**입니다. 그런데 SLEEP으로 적으면, 틀린 설정일수록 부하가 스스로 가벼워집니다. 틀린 설정이 받는 벌이 구조적으로 깎입니다.

그 결과는 한 방향으로만 치우칩니다. "상황을 잘못 알아도 별로 손해가 없다" 쪽입니다. 그리고 그 결론은 세상에 대한 발견이 아니라 **적는 방식이 만든 착시**입니다.

웹 서비스로 치면 부하 시험 도구의 두 가지 방식과 같습니다. "응답을 받으면 다음 요청을 보낸다"는 방식은 서버가 느려질수록 요청을 덜 보냅니다. 그래서 서버가 무너지는 순간에도 도구는 "초당 요청 수가 줄었네" 정도로만 보고합니다. "초당 100개를 정해진 시각에 보낸다"는 방식은 서버가 느려지면 요청이 쌓이고, 무너지는 게 그대로 보입니다. SLEEP이 앞의 방식이고 TIMER가 뒤의 방식입니다.

> **이 연구에서는.** 이 결정이 내려진 2026년 8월 26일의 기록은 상대 시간 SLEEP으로 적는 방식을 버린 이유를 한 가지로 적습니다. 어긋남이 생기고, 그 어긋남이 **나쁜 설정 아래에서만** 기계를 체계적으로 한가하게 만들어서, 측정의 두 번째 층을 "나쁜 설정도 그렇게 나쁘지 않다" 쪽으로 기울인다는 것입니다.

### interbench는 어떻게 했나

이 연구가 주기 작업의 숫자를 가져온 출처는 interbench라는 도구입니다. 그 도구의 소스 코드를 보면 흥미로운 점이 하나 있습니다.

interbench도 **절대 시각의 눈금**을 씁니다. 주기 작업을 돌리는 함수가 매 반복마다 deadline에 주기를 더해 다음 눈금을 정합니다. 여기까지는 TIMER와 같습니다. 그런데 눈금을 놓쳤을 때의 처리가 다릅니다. 소스 코드의 주석입니다.

> "If we meet the deadline we move the deadline forward, otherwise we consider it a missed deadline and dropped frame etc."

deadline을 지키면 deadline을 앞으로 옮기고, 못 지키면 놓친 deadline이자 **떨어뜨린 frame**으로 친다. 실제 코드는 놓친 주기 수를 세어 기록한 뒤 그만큼 눈금을 건너뜁니다. 밀린 일을 쌓지 않고 **버리는** 방식입니다.

이 연구의 TIMER는 쌓습니다. 1권에서 봤듯이 영상은 늦은 frame을 버리는 게 자연스럽고 오디오는 쌓는 쪽이 자연스럽습니다. 이 연구는 주기 작업 전체에 쌓는 쪽을 택했습니다.

> **확인함.** 2026-09-13에 interbench 원본 저장소(github.com/ckolivas/interbench, 커밋 `e612a65c`, 2016-10-24, `interbench.c`의 `INTERBENCH_VERSION "0.31"`)를 받아 `periodic_schedule` 함수를 읽었습니다. 눈금을 놓치면 `missed_deadlines`와 `missed_burns`를 늘리고 deadline을 놓친 주기 수만큼 앞으로 옮기는 것을 확인했습니다.
>
> 이 차이를 저장소 문서가 적어두고 있지는 않습니다. 출처가 버리는 방식인데 이 연구가 쌓는 방식을 택한 것은 **출처의 숫자를 가져오면서 출처의 실행 방식은 가져오지 않은** 경우입니다. 이 선택이 결과에 어떤 차이를 만드는지는 시뮬레이터를 다루는 권에서 봅니다.

## 2.6 반대로 SLEEP을 일부러 쓰는 곳

TIMER가 옳은 자리가 있다면 SLEEP이 옳은 자리도 있습니다. 이 연구에서 SLEEP으로 반복하는 archetype이 둘인데, 그중 하나가 운영체제가 늘 돌리는 시스템 서비스를 흉내 내는 `system-daemon`입니다.

그 항목의 메모가 이유를 적습니다.

> "SLEEP (not TIMER) because stock daemons are not drift-free periodic — aperiodicity is the class's character; the encoding is ours."

TIMER가 아니라 SLEEP인 이유는 기본 설치된 daemon들이 어긋남 없는 주기 작업이 아니기 때문이다. **주기가 없다는 것이 이 부류의 성격**이다. 이 표현 방식은 우리가 정한 것이다.

**daemon**은 사용자가 직접 실행하지 않았는데 뒤에서 늘 도는 시스템 프로그램입니다. 이런 프로그램은 "정확히 몇 초마다" 깨어나지 않습니다. 할 일이 생기면 깨어나고, 끝나면 한참 잡니다. 늦게 깨어나면 다음 깨어남도 그만큼 늦어지는 것이 오히려 실제 모습에 가깝습니다.

> **이 연구에서는.** 규칙은 "주기 작업은 TIMER"이지 "SLEEP 금지"가 아닙니다. 판단 기준은 **실제 프로그램이 절대 시각의 박자를 지키려고 하는가**입니다. 영상과 오디오는 지키려고 합니다. daemon은 그렇지 않습니다.
>
> 그리고 메모의 마지막 구절 "the encoding is ours"를 눈여겨볼 만합니다. SLEEP으로 적는다는 선택 자체는 어느 출처도 말해주지 않고 이 연구가 정한 것이라고 스스로 밝혀둔 것입니다. 이런 문장이 항목마다 붙어 있고, 그게 어떤 장치인지는 항목의 필드를 볼 때 자세히 봅니다.

---

## 2장 정리

- archetype의 규칙은 여섯 개의 primitive로 쓴 작은 프로그램입니다. RUN, SLEEP, TIMER, WAIT, WAKE, 그리고 FORK/EXIT입니다. 반복은 제어 흐름일 뿐 primitive가 아닙니다.
- RUN의 길이는 CPU 요구량이지 벽시계 시간이 아닙니다. 도중에 빼앗기면 벽시계로는 더 오래 걸립니다.
- SLEEP은 지금부터 재는 상대적 대기이고, TIMER는 처음부터 정해진 눈금에 깨어나는 절대적 대기입니다. WAIT는 시간이 아니라 사건을 기다립니다.
- 디스크나 네트워크를 기다리는 WAIT는 깨워줄 것이 없는 시뮬레이터에서 정해진 길이의 멈춤으로 바뀌어 들어갑니다. archetype은 뜻을 보존하고 실행 쪽이 구현합니다.
- 여섯 primitive는 전부 task가 원하는 것만 적습니다. 누구에게 CPU를 줄지는 하나도 적혀 있지 않고, 그 결정이 scheduler의 몫이자 이 연구가 재는 대상입니다.
- 이 방식의 선례는 rt-app입니다. sleep과 timer의 구분까지 그대로 따르지만, rt-app에서 숫자는 하나도 가져오지 않습니다.
- 주기 작업은 반드시 TIMER로 적습니다. SLEEP으로 적으면 나쁜 설정 아래에서 요구량이 조용히 줄어듭니다. 40퍼센트짜리 영상 재생이 매번 5밀리초 늦으면 30.8퍼센트짜리가 되고 실패 기록은 남지 않습니다.
- 그 착시는 한 방향으로만 치우쳐서 "잘못 알아도 손해가 적다"는 거짓 결론을 만듭니다. 그래서 TIMER가 여섯 번째 primitive로 들어왔습니다.
- interbench도 절대 시각의 눈금을 쓰지만 놓친 주기를 버립니다. 이 연구의 TIMER는 쌓습니다. 출처의 숫자를 가져오면서 실행 방식은 가져오지 않은 경우입니다.
- 주기가 없는 것이 성격인 daemon은 일부러 SLEEP으로 적습니다. 기준은 실제 프로그램이 절대 시각의 박자를 지키려 하는가입니다.

---

# 3장 · archetype 하나는 어떻게 정의되는가

## 3.1 세 단계

archetype 하나를 만드는 절차가 계획 문서에 세 단계로 적혀 있습니다. 먼저 원문을 옮깁니다.

> "1. **Pattern selection** — transcribe the source's behavioral description into the grammar (interbench's "wakes every 50 ms, needs 5% CPU" becomes a TIMER/RUN loop).
> 2. **Parameter filling** — the source's numbers enter as *distributions*, not point values. Every numeric carries `source: <id>` or `<id>:<locator>`.
> 3. **Validation criterion** — an archetype's identity is not its code but the **statistics it must reproduce**: burst-length CDF, wakeup rate, instantaneous runnable count, declared per entry as `validation_stats`."

풀면 이렇습니다.

**첫째, 모양 고르기.** 출처가 말로 적어둔 행동을 여섯 primitive로 옮겨 적는다. 예를 들어 "50밀리초마다 깨어나 CPU 5퍼센트가 필요하다"는 TIMER와 RUN의 반복이 된다.

**둘째, 값 채우기.** 출처의 숫자는 점 하나가 아니라 **분포**로 들어간다. 모든 숫자에는 출처 표시가 붙는다.

**셋째, 판정 기준 선언.** archetype의 정체는 코드가 아니라 **재현해야 할 통계**다. CPU를 연속으로 쓰는 구간의 길이 분포, 깨어나는 빈도, 한 순간에 실행 가능한 task의 수 같은 것이고, 항목마다 적어둔다.

세 단계가 각각 다른 질문에 답합니다.

```text
   1단계  모양     "이 프로그램은 어떤 순서로 무엇을 하나"
   2단계  값       "각 동작이 얼마나 길고 얼마나 흩어져 있나"
   3단계  판정     "무엇이 맞으면 이 archetype을 제대로 만든 것인가"
```

이 장은 가장 단순한 항목 하나를 세 단계로 끝까지 따라가고, 그다음 셋째 단계가 왜 가장 중요한지를 봅니다.

## 3.2 손으로 따라가기: audio-playback의 세 단계

음악 재생을 흉내 내는 `audio-playback`입니다.

### 출처를 먼저 엽니다

이 항목의 출처는 interbench입니다. 2권에서 봤듯이 interbench는 Linux에서 대화형 작업의 반응성을 재려고 만든 벤치마크 도구이고, 대화형 작업 몇 가지를 흉내 내는 방식이 설명서에 적혀 있습니다. 소리 재생에 대한 문단 전체를 옮깁니다.

> "Audio is simulated as a thread that tries to run at 50ms intervals that then requires 5% cpu. This behaviour ignores any caching that would normally be done by well designed audio applications, but has been seen as the interval used to write to audio cards by a popular linux audio player. It also ignores any of the effects of different audio drivers and audio cards. Audio is also benchmarked running SCHED_FIFO if the real time benchmarking option is used."

소리 재생은 50밀리초 간격으로 돌려고 하고 그때 CPU 5퍼센트가 필요한 thread로 흉내 낸다. 잘 만든 소리 프로그램이라면 했을 버퍼링은 무시한 모형이지만, 널리 쓰이는 Linux 소리 재생기가 사운드 카드에 쓰는 간격으로 관찰된 값이다. 드라이버와 사운드 카드의 차이도 무시한다. 실시간 옵션을 켜면 소리 재생은 실시간 scheduling 정책으로도 측정한다.

첫 문장에 숫자 둘이 있습니다. **50밀리초**와 **5퍼센트**. 그리고 나머지 문장들이 그 숫자의 **성격**을 밝힙니다. 실제 소리 프로그램을 잰 값이 아니라 단순화한 모형이고, 한 재생기에서 관찰된 간격을 빌려왔다는 것입니다.

같은 도구의 소스 코드에도 이 모형이 그대로 있습니다.

```c
#define AUDIO_INTERVAL	(50000)
#define AUDIO_RUN	(AUDIO_INTERVAL / 20)
/* We emulate audio by using 5% cpu and waking every 50ms */
```

간격은 50,000마이크로초이고, 실행 길이는 간격을 20으로 나눈 값입니다.

> **확인함.** 2026-09-13에 interbench 원본 저장소(github.com/ckolivas/interbench, 커밋 `e612a65c`, 2016-10-24)를 받아 설명서 파일 `interbench.8`의 "What interactive tasks are simulated and how?" 절과 `interbench.c`의 `emulate_audio` 함수 위 정의를 읽었습니다. 2권이 같은 문단의 첫 문장을 인용했고, 이 권은 문단 전체를 옮겼습니다.

### 1단계: 모양 고르기

"50밀리초 간격으로 돌려고 한다"를 primitive로 옮깁니다.

간격이 **정해진 박자**라는 점이 핵심입니다. 앞 장에서 봤듯이 정해진 박자를 지키려는 작업은 TIMER로 적습니다. 그리고 매 박자마다 할 일은 계산입니다.

```yaml
program:
  - loop:
      - TIMER: period
      - RUN: burst
```

**여기서 이미 출처에 없는 결정이 하나 들어갔습니다.** 순서입니다. "알람을 기다리고 나서 계산한다"로 적었는데, "계산하고 나서 알람을 기다린다"로 적어도 문장에는 똑같이 맞습니다. interbench의 문장은 순서를 말하지 않습니다.

이 경우에는 순서가 통계를 바꾸지 않습니다. 둘 다 50밀리초마다 한 번 깨어나 2.5밀리초 계산합니다. 그래도 **결정은 결정**이고, 뒤에서 보겠지만 이 연구는 이런 결정을 전부 우리 것이라고 적어둡니다.

### 2단계: 값 채우기

두 파라미터에 값을 넣습니다. 파일의 실제 모습입니다.

```yaml
params:
  period:
    {dist: constant, value_us: 50000, sampling: per-task,
     source: "interbench:man-audio"}
  burst:
    {dist: constant, value_us: 2500, sampling: per-task,
     source: "interbench:man-audio"}
```

하나씩 읽습니다.

**`dist: constant`.** 분포의 종류가 **상수**라는 뜻입니다. 모든 숫자가 분포로 들어간다는 규칙이 있는데, 흩어짐이 없는 값은 "폭이 0인 분포"로 적습니다. interbench의 모형이 매번 정확히 같은 값을 쓰기 때문에 여기서는 상수가 맞습니다.

**`value_us: 50000`.** 값은 50,000마이크로초, 즉 50밀리초입니다. 이 파일의 시간은 전부 마이크로초 정수이고, 필드 이름 끝의 `_us`가 그 단위 표시입니다.

**`value_us: 2500`.** 출처는 "5퍼센트"라고 했지 "2,500마이크로초"라고 하지 않았습니다. 50,000의 5퍼센트가 2,500이라는 산수가 한 번 들어갔습니다.

**`sampling: per-task`.** 값을 **task마다 한 번** 정한다는 뜻입니다. 상수이니 몇 번 정하든 같지만, 필드는 빠짐없이 적습니다.

**`source: "interbench:man-audio"`.** 출처 표시입니다. 콜론 앞의 `interbench`가 출처의 id이고, 뒤의 `man-audio`가 그 출처 **안의 위치**입니다. 이 위치 표시를 **locator**라고 부릅니다. `man-audio`는 "설명서의 Audio 항목"을 가리킵니다.

> **이 연구에서는.** 2,500이라는 산수가 누구 것인지를 항목의 메모가 밝힙니다.
>
> > "interbench man-audio states "wakes every 50 ms needing 5% CPU"; the TIMER/RUN transcription and the duty-cycle-to-duration arithmetic (5% of 50 ms = 2,500 us per period) are ours."
>
> interbench 설명서의 Audio 항목이 "50 ms마다 깨어나 5% CPU가 필요하다"고 적는다. TIMER/RUN으로 옮긴 것과, 비율을 시간으로 바꾼 산수(50 ms의 5% = 주기당 2,500 us)는 우리 것이다.
>
> 두 가지를 짚을 만합니다. 첫째, 메모가 따옴표로 옮긴 "wakes every 50 ms needing 5% CPU"는 **설명서의 원래 문장이 아니라 요약**입니다. 원래 문장은 위에 옮긴 "tries to run at 50ms intervals that then requires 5% cpu"입니다. 뜻은 같지만, 따옴표 안의 글자가 원문과 다르다는 것은 적어둡니다.
>
> 둘째, 메모는 2,500이라는 산수를 "우리 것"이라고 하는데, interbench의 **소스 코드**에도 `AUDIO_INTERVAL / 20`이라는 똑같은 산수가 있습니다. 설명서만 보면 우리 산수이고, 소스 코드까지 보면 출처가 이미 한 산수입니다. 어느 쪽이든 값은 같습니다.

### 영상 재생도 같은 모양입니다

옆 항목 `video-playback`도 같은 절차를 밟았습니다. 설명서의 문장입니다.

> "Video is simulated as a thread that tries to receive cpu 60 times per second and uses 40% cpu. This would be quite a demanding video playback at 60fps."

영상 재생은 초당 60번 CPU를 받으려 하고 CPU 40퍼센트를 쓰는 thread로 흉내 낸다. 60fps 재생으로는 꽤 무거운 편이다.

archetype 파일의 값은 주기 16,667마이크로초, 실행 6,667마이크로초입니다. 1초를 60으로 나누면 16,666.67이고, 그 40퍼센트가 6,666.67입니다. 반올림한 값입니다.

> **확인함.** interbench 소스 코드는 같은 값을 정수 나눗셈으로 계산합니다. `VIDEO_INTERVAL`이 `(1000000 / 60)`이라서 16,666이 되고, `VIDEO_RUN`이 `(VIDEO_INTERVAL * 40 / 100)`이라서 6,666이 됩니다. 이 연구의 값은 각각 1마이크로초 큽니다. 비율로 치면 0.006퍼센트 차이라 결과에 영향은 없고, 산수가 반올림이냐 버림이냐의 차이일 뿐입니다. 2026-09-13에 앞의 저장소에서 확인했습니다.

### 3단계: 판정 기준 선언

이제 가장 중요한 단계입니다. 이 archetype을 **제대로 만들었다는 것은 무엇을 뜻하나**를 적습니다.

```yaml
validation_stats:
  referee: self-consistency
  stats: [wakeup-rate 20 Hz, cpu-share 5%]
  note: values are interbench's community interactivity model, not a
    measured behavior; no meas-ci referee.
```

**`stats`.** 재현해야 할 통계가 둘입니다. 초당 20번 깨어나야 하고, CPU의 5퍼센트를 써야 한다.

**`referee`.** 그 통계가 맞는지를 판정해줄 기준입니다. 우리말로 옮기면 심판입니다. 여기 적힌 값은 `self-consistency`, **자기 일관성**입니다. 바깥의 측정과 비교하는 것이 아니라 만든 결과가 스스로 선언한 숫자와 맞는지만 본다는 뜻입니다.

**`note`.** 이유가 적혀 있습니다. 이 값들은 커뮤니티가 대화형 작업을 모형화한 방식이지 **측정된 행동이 아니다.** 그러니 우리 측정과 비교할 대상이 없다.

이게 무슨 뜻인지 정확히 봐야 합니다. 자기 일관성 심판은 **"우리가 적은 대로 만들어졌는가"**만 확인합니다. "실제 음악 재생기가 이렇게 행동하는가"는 확인하지 않습니다. 그 질문에 대한 답은 이 항목에 없고, 이 항목은 그 사실을 감추지 않고 적어둡니다.

## 3.3 정체가 코드가 아니라 통계라는 것

셋째 단계의 문장을 다시 보겠습니다. "archetype의 정체는 코드가 아니라 재현해야 할 통계다." 왜 이렇게 정했을까요.

### 같은 통계를 내는 다른 코드

음악 재생 archetype을 두 가지로 적어봅니다.

```text
   적는 방식 A                    적는 방식 B
   반복:                          반복:
     TIMER(50 ms)                   RUN(2.5 ms)
     RUN(2.5 ms)                    TIMER(50 ms)
```

A는 알람을 기다렸다 계산하고, B는 계산하고 알람을 기다립니다. 코드는 다릅니다.

scheduler가 보는 것은 같습니다. 50밀리초마다 한 번 깨어나 2.5밀리초 계산합니다. 초당 20번, CPU 5퍼센트. **재현하는 통계가 같으면 같은 archetype입니다.**

반대도 성립합니다. 코드가 똑같아 보여도 파라미터가 달라서 통계가 달라지면 그건 다른 archetype이거나, 잘못 만든 archetype입니다.

### 왜 이게 중요한가

웹 서비스의 API 계약을 떠올리면 이 규칙의 쓸모가 보입니다. 두 서비스가 "같은 기능"을 한다는 것은 구현 코드가 같다는 뜻이 아닙니다. 같은 요청에 같은 응답을 준다는 뜻입니다. 계약 시험은 코드를 읽지 않고 응답을 봅니다.

archetype도 같습니다. 판정을 코드에 두면 "이 프로그램이 출처의 문장을 잘 옮겼나"를 사람이 읽고 판단해야 합니다. 판정을 통계에 두면 **숫자를 비교하는 문제**가 됩니다. 그리고 숫자 비교는 누가 해도 같은 결과가 나옵니다.

그리고 한 가지가 더 따라옵니다. 통계로 정의하면 **판정할 수 없는 archetype이 무엇인지도 드러납니다.** 비교할 바깥의 통계가 없는 항목은 심판란에 그렇게 적어야 하기 때문입니다.

> **이 연구에서는.** 계획 문서가 "올바르다"의 뜻을 한 문장으로 정합니다.
>
> > ""Correct" means the simulated trace matches the `meas-ci` re-enactment of the corresponding scenario — for the CI-runnable entries."
>
> "올바르다"는 시뮬레이션한 trace가 해당 상황을 우리 측정 캠페인에서 다시 연기한 결과와 맞는다는 뜻이다. 단, CI에서 돌릴 수 있는 항목에 한해서다. **trace**는 실행 중에 일어난 사건을 시각 순서로 기록한 것입니다. **meas-ci**는 이 연구가 공개 CI 서버에서 실제 프로그램을 돌려 잰 측정 캠페인의 이름이고, 뒤에서 한 장을 들여 봅니다.
>
> 이 문장의 마지막 구절 "CI에서 돌릴 수 있는 항목에 한해서"가 한계를 미리 선언합니다. 모든 archetype이 이 방법으로 판정되지는 않는다는 것입니다.

## 3.4 심판의 세 종류

실제 파일을 열어보면 열두 항목의 심판란에 세 가지 값이 있습니다.

| 심판 | 뜻 | 몇 항목 |
|---|---|---|
| `meas-ci` | 우리 측정 캠페인이 잰 통계와 비교한다 | 7 |
| `self-consistency` | 적은 대로 만들어졌는지만 본다. 바깥 기준이 없다 | 3 |
| `none` | 판정할 기준 자체가 없다. 이유를 적는다 | 2 |

`self-consistency`인 셋은 음악 재생, 영상 재생, 그리고 CPU를 끝날 때까지 계속 쓰는 `cpu-batch`입니다. 셋 다 커뮤니티 도구의 모형에서 왔고, 모형 자체가 "이렇게 흉내 낸다"이지 "실제로 이렇다"가 아니라서 비교할 측정이 없습니다.

`cpu-batch`의 이유는 조금 다릅니다. 메모가 이렇게 적습니다.

> "interbench Burn is the community's saturation load model; no meas-ci referee needed for "burns CPU until done"."

interbench의 Burn은 커뮤니티가 CPU를 포화시키는 부하를 모형화한 것이고, "끝날 때까지 CPU를 태운다"에는 측정 심판이 필요 없다. 계산만 하다가 끝나는 프로그램은 그 모양이 너무 단순해서 잴 것이 없다는 뜻입니다.

`none`인 둘은 사람의 입력에 반응하는 `desktop-interactive`와 게임의 `game-task-chain`입니다. 둘의 이유가 서로 다르고, 둘 다 이 연구에서 근거가 가장 약한 자리입니다. 이 권의 마지막 본문 장에서 따로 봅니다.

나머지 일곱은 `meas-ci`입니다. 우리가 실제 프로그램을 돌려서 잰 값이 있고, 시뮬레이션 결과를 그 값과 비교할 수 있다는 뜻입니다.

> **미실행.** 심판이 `meas-ci`인 일곱 항목에 대해, **시뮬레이션한 trace를 측정 결과와 실제로 맞대어 본 기록은 아직 없습니다.** 지금까지 한 일은 측정에서 파라미터를 뽑아 archetype에 넣은 것까지입니다. 그 파라미터로 시뮬레이터를 돌려서 나온 통계가 다시 측정과 맞는지를 보는 비교는 계획 문서에 판정 기준으로 적혀 있을 뿐, 언제 돌린다는 일정은 저장소 문서에 적혀 있지 않습니다.
>
> 전제 조건은 둘입니다. 시뮬레이터가 archetype의 통계를 뽑아낼 수 있는 trace를 내야 하고, 두 통계를 비교하는 방법과 "맞다"의 기준이 정해져야 합니다. 뒤엣것을 어떻게 계산하는지는 harness를 다루는 권의 몫입니다.

---

## 3장 정리

- archetype 하나는 세 단계로 정의됩니다. 출처의 서술을 primitive로 옮기고, 숫자를 분포로 채우고, 무엇을 재현해야 하는지를 선언합니다.
- 음악 재생 archetype은 interbench 설명서의 "50ms 간격으로 돌려고 하고 5% CPU가 필요하다"에서 왔습니다. 모양은 TIMER와 RUN의 반복이고, 값은 50,000과 2,500마이크로초 상수입니다.
- 옮기는 과정에 출처에 없는 결정이 들어갑니다. 동작의 순서, 비율을 시간으로 바꾸는 산수 같은 것들이고, 항목의 메모가 그것을 우리 것이라고 밝힙니다.
- 출처 표시는 `id:locator` 모양입니다. `interbench:man-audio`는 interbench 설명서의 Audio 항목을 가리킵니다.
- 원문과 대조하면 작은 차이가 보입니다. 메모가 따옴표로 옮긴 문장은 원문이 아니라 요약이고, 영상 재생의 값은 interbench 코드의 정수 나눗셈보다 1마이크로초 큽니다. 둘 다 값의 뜻을 바꾸지는 않습니다.
- archetype의 정체는 코드가 아니라 재현해야 할 통계입니다. 코드가 달라도 통계가 같으면 같은 archetype이고, 판정은 사람의 해석이 아니라 숫자 비교가 됩니다.
- 심판에는 세 종류가 있습니다. 우리 측정과 비교하는 `meas-ci` 일곱, 적은 대로 만들어졌는지만 보는 `self-consistency` 셋, 판정할 기준이 없는 `none` 둘입니다.
- 자기 일관성 심판은 "실제 프로그램이 이렇게 행동하는가"를 확인하지 않습니다. 그 사실이 항목에 적혀 있습니다.
- 측정과 비교하도록 되어 있는 일곱 항목도 시뮬레이션 결과를 측정과 실제로 맞대어 본 적은 아직 없습니다.

---

# 4장 · 한 항목에 적히는 것

## 4.1 필드 목록

archetype 항목 하나에는 정해진 필드들이 들어갑니다. 계획 문서가 목록을 한 문단으로 적어두었습니다.

> "Per entry: `id`, `category_source` (Tier-1 provenance), `pattern` (grammar program), numeric params (each with `source:`), `sampling` (per-instance | per-task | per-iteration — interpretation-contract §5), `lifetime` (segment-bound | finite | spawned), `spawns`/`spawned_by` (orchestration edges), `scalable` (fields the lane-scaling pass may transform, with rule), `validation_stats` (which CDFs/rates `meas-ci` must match, or the stated reason none exist), and **`modeling_notes`** — prose recording what our encoding invented on top of the sources: field names, structure linearizations, scaling defenses, binding choices."

표로 정리하면 이렇습니다.

| 필드 | 무엇을 적나 |
|---|---|
| `id` | archetype의 이름. 파일에서는 항목의 열쇠 자체 |
| `category_source` | 이런 행동 부류가 존재한다는 근거를 어느 분류 체계에서 거둬왔나 |
| `pattern` | primitive로 쓴 프로그램 |
| `params` | 숫자 파라미터들. 하나하나가 분포이고 출처 표시가 붙는다 |
| `sampling` | 각 파라미터의 값을 얼마나 자주 새로 뽑나 |
| `lifetime` | 이 task가 어떻게 끝나나 |
| `spawns` / `spawned_by` | 누가 누구를 자식으로 만드나 |
| `binding_params` | 이 archetype을 쓰는 쪽이 채워야 하는 손잡이들의 이름 |
| `scalable` | CPU 한 자리에 맞추려고 compile 단계가 바꿔도 되는 값과 그 규칙 |
| `validation_stats` | 무엇을 재현해야 하나, 또는 판정할 수 없는 이유 |
| `modeling_notes` | 출처 위에 우리가 무엇을 지어냈나 |

`pattern`과 `validation_stats`는 앞 두 장에서 봤고, `category_source`는 한 장을 따로 들여 봅니다. 이 장은 나머지를 봅니다. 그중 가장 긴 것이 **`params`의 분포 표기**입니다.

## 4.2 숫자는 분포로 들어갑니다

### 왜 점 하나가 아닌가

컴파일러가 파일 하나를 컴파일하는 데 CPU를 얼마나 쓰나요. 정답은 "파일마다 다르다"입니다. 헤더 몇 줄짜리 파일은 몇 밀리초, 템플릿이 가득한 파일은 몇 초입니다.

이걸 평균 하나로 적으면 모든 자식이 똑같은 길이가 됩니다. 그러면 실제로 scheduler를 괴롭히는 것, 즉 **짧은 것들 사이에 섞여 있는 아주 긴 몇 개**가 사라집니다. 1권에서 봤듯이 사용자가 느끼는 것은 평균이 아니라 꼬리입니다.

그래서 규칙이 이렇습니다. 출처의 숫자는 **분포**로 들어갑니다. 분포는 "값이 대체로 어디쯤이고 얼마나 흩어져 있나"를 적는 방식입니다.

### 파일이 쓰는 분포의 종류

실제 파일에 나오는 분포 표기는 다섯 가지입니다.

| `dist` | 적는 값 | 뜻 |
|---|---|---|
| `constant` | `value_us` 또는 `value` | 흩어짐 없이 늘 같은 값 |
| `uniform` | `min`, `max` | 두 값 사이에서 어느 값이나 똑같이 나올 수 있다 |
| `lognormal` | `median_us`, `sigma_log` | 로그를 취하면 정규 분포가 되는 값 |
| `lognormal` (anchor 형) | `anchor_min_us`, `anchor_max_us` | 위와 같은 분포를 양 끝 두 값으로 정한다 |
| `lognormal-mixture` | 두 성분의 값과 섞는 비율 | 로그 정규 분포 둘을 확률로 섞은 것 |

그리고 값을 뽑지 않고 "이 파라미터가 따르는 분포의 가족은 이것이다"만 선언하는 `family-declaration`이 한 번 나옵니다.

### lognormal을 처음 보는 사람을 위해

**lognormal**, 우리말로 로그 정규 분포는 이 파일에서 가장 많이 쓰이는 분포입니다. 이름이 어렵게 들리지만 성격은 간단합니다.

**곱해서 흩어지는 값**입니다. 정규 분포는 "평균에서 ±몇 밀리초"로 흩어지고, 로그 정규 분포는 "중앙값의 몇 배, 몇 분의 일"로 흩어집니다. 그래서 0 아래로 내려가지 않고, 오른쪽으로 긴 꼬리가 생깁니다. 대부분은 짧은데 가끔 아주 긴 값이 나오는, 컴퓨터에서 흔히 보는 모양입니다.

파일에는 두 값으로 적습니다.

```text
   median_us   중앙값. 뽑힌 값의 절반은 이보다 작고 절반은 크다
   sigma_log   흩어짐의 크기. 로그 척도에서의 표준편차
```

값을 뽑는 방법도 파일 머리에 적혀 있습니다.

> "lognormal params are `{median_us, sigma_log}`; the compiler samples median * exp(sigma_log * z)"

로그 정규 파라미터는 중앙값과 로그 척도 표준편차이고, compile 단계는 **중앙값 × exp(sigma_log × z)**로 값을 뽑는다. z는 표준 정규 분포에서 뽑은 수입니다. 대략 셋 중 둘은 −1과 1 사이에 들어갑니다.

감을 잡기 위해 숫자를 넣어봅니다. 중앙값이 10밀리초이고 `sigma_log`가 1이면 이렇습니다.

```text
   z = -1   →  10 × exp(-1) ≈  3.7 ms
   z =  0   →  10 × exp(0)  = 10.0 ms
   z = +1   →  10 × exp(1)  ≈ 27.2 ms
   z = +2   →  10 × exp(2)  ≈ 73.9 ms
```

z가 1 늘어날 때마다 값이 약 2.7배가 됩니다. `sigma_log`가 2이면 z 하나에 약 7.4배입니다. **`sigma_log`가 1을 넘으면 꼬리가 아주 깁니다.**

한 가지 더 알아둘 성질이 있습니다. 로그 정규 분포의 **평균은 중앙값보다 큽니다.** 긴 꼬리가 평균을 끌어올리기 때문입니다. 정확히는 평균 = 중앙값 × exp(sigma_log² / 2)입니다. `sigma_log`가 2이면 평균이 중앙값의 약 7.4배입니다. 이 성질이 뒤에서 측정값을 파라미터로 옮길 때 실제로 문제가 됩니다.

### 왜 하필 lognormal인가

이 선택에는 출처가 없습니다. 저장소가 **관례로 정했다**고 적어둡니다. 파일 머리의 문장입니다.

> "distribution family defaults to lognormal by stated convention"

분포 가족은 **밝혀둔 관례에 따라** lognormal을 기본으로 한다.

계획 문서는 이 가정이 틀렸을 경우를 대비한 장치로, 분포 가족을 둘로 바꿔가며 결과를 보고하는 민감도 분석을 가리킵니다.

> **확인 필요.** 계획 문서가 가리키는 민감도 분석이 실제로 **archetype 파라미터의 분포 가족**을 덮는지 확인이 필요합니다.
>
> 계획 문서는 lognormal 관례를 적은 자리에서 "자연스러운 workload 묶음의 두 가족 민감도 보고가 이 가정을 덮는다"고 말합니다. 그런데 그 보고를 정의한 데이터셋 구축 문서를 열어보면, 두 가족으로 바꿔 보는 대상은 **구간 길이의 분포**, 즉 한 상황이 몇 분 이어지는가입니다. 로그 정규와 멱법칙을 비교한다고 적혀 있고, archetype의 RUN 길이나 깨어남 간격을 바꿔 본다는 말은 없습니다.
>
> 그러니 지금 문서만으로는 "archetype 분포를 lognormal로 정한 가정"을 덮는 민감도 분석이 계획되어 있다고 말할 수 없습니다. 무엇을 열어보면 되는지: 자연스러운 workload 묶음을 만드는 생성기의 설계가 나올 때 그 분석이 archetype 쪽까지 포함하는지 보면 됩니다. 그 생성기는 RQ0 gate를 통과한 뒤에 만들기로 되어 있어서 아직 확인할 대상이 없습니다.

## 4.3 손으로 따라가기: 사람의 키 입력 간격

분포 표기가 가장 복잡한 항목을 하나 끝까지 봅니다. 사람이 앉아서 만지는 프로그램을 흉내 내는 `desktop-interactive`입니다. 그중 **키를 누르는 간격** 파라미터입니다.

### 파일의 모습

```yaml
input_gap:
  {dist: lognormal-mixture, fluent_mean_us: 158000,
   fluent_sigma_log: 0.35, pause_probability: 0.34,
   pause_mean_us: 395235, pause_sigma_log: 0.6,
   overall_mean_us: 238660, sampling: per-iteration,
   source: "dhakal-chi18"}
input_gap_family:
  {dist: family-declaration, family: two-component-lognormal,
   sampling: per-iteration, source: "roeser-rw24"}
```

**두 성분을 섞은 분포**입니다. 사람이 키를 누르는 간격은 두 종류가 섞여 있다는 모형입니다. 막힘없이 칠 때의 짧은 간격과, 잠깐 멈칫할 때의 긴 간격입니다. 34퍼센트 확률로 멈칫하는 쪽에서 뽑고, 나머지 66퍼센트는 막힘없는 쪽에서 뽑습니다.

숫자가 여섯 개 있습니다. 하나씩 어디서 왔는지 따라가겠습니다.

### 238,660 — 첫 번째 출처

전체 평균 `overall_mean_us: 238660`의 출처는 Dhakal 외 네 명이 2018년 CHI에 낸 논문입니다. 온라인 타자 시험에 참가한 사람들의 키 입력을 모아 분석했습니다. 초록의 첫 문장입니다.

> "We report on typing behaviour and performance of 168,000 volunteers in an online study."

결과 절의 문장입니다.

> "The final dataset includes 136,857,600 keystrokes from 168,960 participants with, on average, about 810 keypresses per participant."

> "INTER-KEY INTERVALS Average inter-key interval is 238.656 ms (SD = 111.6). A lower bound of about 60 ms can be observed. The IKI distribution shown in Figure 2 has a skewness of 1.98 and kurtosis measure of 7.1."

키 입력 간격의 평균은 238.656밀리초이고 표준편차는 111.6이다. 약 60밀리초의 하한이 보인다. 분포는 오른쪽으로 치우쳐 있다.

그리고 이 숫자가 **어떤 조건에서** 나왔는지가 같은 논문에 적혀 있습니다.

> "The experimental task employed in this work is transcription typing, the act of typing sequences of characters by looking at an existing written record."

> "INTER-KEY INTERVAL (IKI) is the difference in timestamps between two keypress events. For IKI-based analysis, we removed keystrokes that were typed more than 5000 ms after the previous keystroke."

실험 과제는 **옮겨 치기**, 즉 적힌 글을 보면서 똑같이 치는 것이다. 키 입력 간격은 두 키 누름 사이의 시각 차이이고, 앞 키에서 5,000밀리초 넘게 지나 눌린 키는 분석에서 뺐다.

이 두 조건이 이 숫자의 **범위**를 정합니다. 글을 생각하면서 쓰는 것이 아니라 보고 옮겨 치는 것이고, 5초 넘게 멈춘 자리는 빠져 있습니다. 그러니 이 숫자는 "사람이 편집기 앞에서 생각하다가 멈추는 시간"을 담고 있지 않습니다.

> **이 연구에서는.** 출처 등록부가 이 범위를 정확히 적어둡니다.
>
> > "Scope limit: within-burst transcription typing — no mouse events, no inter-burst think-pauses. Grounds the intra-burst input gap of interactive archetypes only; burst/pause macro-structure is not established here."
>
> 옮겨 치기 한 덩어리 안의 간격일 뿐이고, 마우스 입력도 없고 덩어리 사이에 생각하느라 멈추는 시간도 없다. 대화형 archetype의 **덩어리 안 입력 간격**만 뒷받침하고, 덩어리와 멈춤이 번갈아 오는 큰 구조는 여기서 나오지 않는다.

> **확인함.** 2026-09-13에 저자들이 공개한 논문 PDF(userinterfaces.aalto.fi/136Mkeystrokes, `chi-18-analysis.pdf`, 12쪽)를 받아 초록, 실험 과제 절, 측정 정의 절, 결과 절을 읽었습니다. 238.656밀리초와 111.6은 본문과 Table 3(IKI 행: 238.66, 111.60)에서 모두 확인됩니다.
>
> 한 가지를 적어둡니다. Table 3의 설명이 이 값을 "mean and SD for each measure"라고 하고, Figure 2가 "over all participants"의 분포라서, 111.6은 **참가자별 평균 간격들이 참가자 사이에서 흩어진 정도**로 읽힙니다. 출처 등록부도 "SD 111.60 across participants' means"로 적어 같은 읽기를 합니다. 반면 archetype은 238.66을 **한 사람이 치는 간격들의 평균**으로 씁니다. 수많은 사람의 평균을 한 사람의 평균 자리에 넣는 것은 우리 쪽의 해석이고, 그 해석이 틀리지는 않지만 원문이 직접 말하는 것도 아닙니다.

### 158,000과 0.34 — 두 번째 출처

막힘없는 성분의 값 158,000과 멈칫할 확률 0.34의 출처는 Roeser 외 세 명의 논문입니다. 키 입력 간격을 두 과정의 섞임으로 모형화한 연구입니다. 초록의 문장입니다.

> "Our results illustrate that we can model copy typing as a mixture process of fluent and disfluent key transitions."

옮겨 치기를 **막힘없는 키 전환과 막힌 키 전환의 섞임 과정**으로 모형화할 수 있다.

두 성분이 무엇인지는 모형 절에 적혀 있습니다.

> "we fixed the number of underlying distributions to two, namely 2 log-Gaussian (log-normal) distributions, of which one represents fluent typing – shorter IKIs – and the other represents disfluencies – longer IKIs."

바탕 분포의 수를 둘로 고정했다. 두 개의 로그 정규 분포이고, 하나는 막힘없는 타자(짧은 간격), 다른 하나는 막힘(긴 간격)을 나타낸다.

그리고 숫자가 나오는 결과 절입니다.

> "After accounting for process disfluencies, keystroke intervals were longer for the consonants task (429 msecs, PI: 356 – 515) compared to the LF-bigrams task (158 msecs, PI: 139 – 180). The slowdown for disfluencies was about four times longer for the consonants task. For the LF-bigrams task, the model determined a slowdown of 95 msecs (PI: 76 – 116) with a probability of 0.34 (PI: 0.31 – 0.38); for the consonants task we found a slowdown of 414 msecs (PI: 333 – 509) with a probability of 0.73 (PI: 0.66 – 0.80)."

막힘을 걸러내고 나면, 자음 나열 과제의 키 간격은 429밀리초, 빈도가 낮은 글자쌍 과제는 158밀리초였다. 빈도 낮은 글자쌍 과제에서 막힘은 95밀리초 느려지는 것이었고 확률은 0.34였다. 자음 나열 과제에서는 414밀리초 느려지고 확률은 0.73이었다.

**158과 0.34는 두 과제 중 한 과제의 값입니다.** 다른 과제에서는 429와 0.73입니다. 같은 사람들이 과제만 바꿨는데 멈칫할 확률이 두 배 넘게 뛰었습니다. 논문도 바로 뒤에서 이렇게 적습니다.

> "In other words, the magnitude for disfluencies and hence their cognitive source in the typing process is task-specific."

막힘의 크기, 그리고 그 인지적 원인은 **과제에 따라 다르다.**

> **이 연구에서는.** 그래서 저장소는 이 출처에서 **가족의 모양만** 가져온다고 적습니다. 출처 등록부의 문장입니다.
>
> > "Cite the family shape, never a single parameter set."
>
> 분포 가족의 모양을 인용하고, 파라미터 한 벌을 인용하지는 말라. 항목 파일에서도 이 출처는 `input_gap_family`라는, 값을 뽑지 않고 가족만 선언하는 줄에 붙어 있습니다. 그런데 158,000과 0.34라는 **값 자체**는 `input_gap` 줄에 들어가 있고, 그 줄의 출처 표시는 `dhakal-chi18`입니다. 값을 준 논문과 출처 표시가 가리키는 논문이 다른 셈이고, 그 사정은 메모에서만 드러납니다.

### 395,235 — 산수

`pause_mean_us: 395235`는 어느 논문에도 없습니다. 메모가 계산 과정을 적어둡니다.

> "pause_mean_us is our arithmetic closing the mixture on dhakal's overall mean: (238,660 - 0.66*158,000)/0.34 ~ 395,235 us."

Dhakal의 전체 평균에 맞게 섞임을 닫는 **우리 산수**다. 직접 계산해봅니다.

```text
   섞인 분포의 평균 = (막힘없음 확률 × 막힘없음 평균) + (멈칫 확률 × 멈칫 평균)

   238,660 = 0.66 × 158,000 + 0.34 × 멈칫 평균
   238,660 = 104,280 + 0.34 × 멈칫 평균
   멈칫 평균 = 134,380 / 0.34 = 395,235.29…
```

두 논문의 숫자를 한 식에 넣어서 남은 빈칸 하나를 채운 것입니다. Dhakal에서 전체 평균, Roeser에서 막힘없음 값과 멈칫 확률을 가져왔습니다.

### 0.35와 0.6 — 관례

두 성분의 흩어짐 `fluent_sigma_log: 0.35`와 `pause_sigma_log: 0.6`에 대해 메모가 적습니다.

> "The sigma_log values are our convention within the cited log-normal family (roeser-rw24 states the family; its parameters are task-dependent, so no single set is citable)."

`sigma_log` 값들은 인용한 로그 정규 가족 안에서 우리가 정한 관례다. Roeser가 가족을 말하지만 파라미터가 과제에 따라 달라서 한 벌을 인용할 수 없다.

### 원문과 대조했을 때 보이는 것

Roeser 논문을 직접 읽으면 저장소 문서가 적지 않은 사정이 두 가지 더 보입니다.

> **확인함.** 2026-09-13에 Nottingham Trent University 기관 저장소(irep.ntu.ac.uk, eprint 43931)에 공개된 저자 원고 PDF(44쪽)를 읽었습니다. 출판사 사이트는 자동 접근을 막아서 출판본 자체는 읽지 못했습니다. 따라서 위의 인용문은 **저자 원고의 문장**이고, 출판본의 쪽 번호와 세부 문구는 대조하지 않았습니다.
>
> **첫째, 158은 평균이라기보다 로그 척도의 위치입니다.** 논문의 식은 막힘없는 성분을 `LogNormal(β + …, σ²)`로 쓰고, 158은 그 β를 밀리초로 옮긴 값입니다. 같은 논문이 다른 자리에서 로그 척도 값을 "5 log msecs (i.e. ≈150 msecs)"처럼 지수를 취해 밀리초로 옮기는데, 로그 정규 분포에서 그렇게 옮긴 값은 평균이 아니라 중앙값에 해당합니다. 그런데 archetype은 이 값을 `fluent_mean_us`, 즉 **평균**이라는 이름으로 담고, compile 단계도 평균으로 받아서 중앙값을 약 148,613마이크로초로 계산합니다. 차이는 6퍼센트쯤이지만, 이름과 원문의 정의가 어긋나 있습니다.
>
> **둘째, 원문에는 멈칫 성분의 값도 있습니다.** 빈도 낮은 글자쌍 과제에서 멈칫은 막힘없는 값에 95밀리초를 더한 것이므로 약 253밀리초입니다. archetype의 멈칫 성분은 산수로 닫은 395밀리초입니다. 같은 논문의 같은 과제에서 0.34를 가져오면서 짝이 되는 253은 가져오지 않고 다른 논문의 평균으로 빈칸을 채운 것입니다. 그 선택 자체는 메모에 적힌 대로 "우리 산수"로 정직하게 표시되어 있습니다. 다만 출처에 짝이 되는 값이 있었다는 사실은 저장소 어디에도 적혀 있지 않습니다.
>
> 논문의 Table 3에는 두 성분의 분산 추정치도 있습니다(빈도 낮은 글자쌍 과제에서 막힘없음 0.29, 막힘 1.16). 과제마다 다르다는 이유로 인용하지 않기로 한 판단은 앞서 본 논문의 문장과 맞습니다.
>
> 이 두 가지를 어떻게 처리할지는 이 권이 정할 일이 아닙니다. 사실만 적어둡니다.

### 입력 한 번에 계산은 얼마나

같은 항목의 파라미터가 하나 더 있습니다. 키가 한 번 눌렸을 때 CPU를 얼마나 쓰는가입니다.

```yaml
burst_fraction:
  {dist: uniform, min: 0.0, max: 1.0, sampling: per-iteration,
   source: "interbench:man-x"}
```

0과 1 사이에서 고르게 뽑은 비율입니다. 출처는 interbench 설명서의 X 항목입니다. 여기서 X는 Linux의 화면 표시 시스템을 말합니다.

> "X is simulated as a thread that uses a variable amount of cpu ranging from 0 to 100%. This simulates an idle gui where a window is grabbed and then dragged across the screen."

X는 CPU를 0에서 100퍼센트 사이의 가변적인 양으로 쓰는 thread로 흉내 낸다. 한가하던 화면에서 창 하나를 잡고 끌어가는 상황이다.

메모가 이 문장을 어떻게 옮겼는지 밝힙니다.

> "Burst CPU cost linearizes interbench man-x's "variable 0-100%" as a uniform fraction of the preceding input gap; the burst/pause macro-structure beyond the mixture is our modeling with no external referee."

"0에서 100퍼센트 가변"을 **직전 입력 간격의 균등한 비율**로 선형화했다. 섞임 분포 너머의 덩어리와 멈춤 구조는 바깥 심판이 없는 우리 모형이다.

그러니까 키 간격이 200밀리초였고 비율이 0.3으로 뽑혔다면, 그 키 입력 뒤에 60밀리초를 계산합니다.

> **확인함.** interbench 소스 코드의 X 흉내 함수는 이렇게 생겼습니다(2026-09-13, 앞의 저장소).
>
> ```c
> /*
>  * We emulate X by running for a variable percentage of cpu from 0-100%
>  * in 1ms chunks.
>  */
> ```
>
> 함수 안에서는 i를 0부터 100까지 올리면서 i밀리초 계산하고 (100 − i)밀리초 쉬는 것을 반복합니다. **무작위가 아니라 0퍼센트에서 100퍼센트까지 차례로 올라가는 경사**이고, 한 바퀴가 100밀리초입니다. archetype은 같은 "0에서 100퍼센트"를 무작위 균등 분포로 옮겼습니다. 두 방식의 평균 CPU 비율은 둘 다 50퍼센트로 같습니다.

**이 선택의 결과가 작지 않습니다.** 비율의 평균이 0.5이므로, 사람이 그 창을 만지는 동안 이 task는 평균적으로 **시간의 절반을 계산에 씁니다.** 실제 파일 하나에서 확인해봅니다. 편집기 `code`가 2초부터 58초까지 입력을 받는 `c1-compile` 파일을 compile하면, 편집기 task의 CPU 요구량 합이 28,470,806마이크로초로 나옵니다. 56초 중 약 28.5초입니다.

1권에서 편집기는 "하루 종일 켜놔도 CPU 사용률이 1퍼센트 안팎"인 대표적인 대화형 프로그램이었습니다. 이 archetype의 편집기는 그보다 훨씬 무겁습니다. 이 연구가 흉내 내는 것은 "글자를 치는 편집기"라기보다 **interbench가 흉내 낸 "창을 끌고 다니는 화면"**에 가깝습니다. 이 점은 근거가 약한 자리를 다루는 장에서 다시 봅니다.

## 4.4 sampling: 값을 얼마나 자주 새로 뽑나

분포에서 값을 뽑는 빈도를 정하는 필드입니다. 실행 계약 문서의 정의입니다.

> "*per-instance* (one draw per spawned task — spawn-table entries), *per-task* (one draw reused across iterations — e.g. per-schedule runtime, matching the source's "stable per task"), *per-iteration, only when bounded* (pre-sampled into the event stream — input wake events)."

| 값 | 뜻 | 예 |
|---|---|---|
| `per-instance` | 자식 task 하나마다 한 번 | 컴파일러 자식 하나하나의 계산 길이 |
| `per-task` | task마다 한 번 뽑아서 모든 반복에 재사용 | 게임 task 하나의 실행 길이 |
| `per-iteration` | 반복마다 새로 뽑는다. **끝이 정해진 반복일 때만** | 키 입력 간격 |

`per-task`의 예로 적힌 "출처의 stable per task에 맞춰"라는 구절이 재미있습니다. 게임 task의 실행 길이를 task마다 한 번만 뽑는 것은, 출처인 LAVD 발표가 "task의 실행 시간은 매우 안정적"이라고 말했기 때문입니다. **뽑는 빈도에도 근거가 있습니다.**

`per-iteration`의 조건 "끝이 정해진 반복일 때만"에는 이유가 있습니다. compile 단계가 모든 무작위성을 미리 해결해서 파일에 구체적인 숫자로 적어야 하는데, 끝이 없는 반복의 매 바퀴 값을 미리 다 적을 수는 없기 때문입니다.

> **확인 필요.** archetype 파일이 이 조건과 어긋나는 자리가 있습니다.
>
> 끝이 없는 반복을 도는 항목 셋이 파라미터에 `sampling: per-iteration`을 적고 있습니다. 파일 색인을 흉내 내는 `background-crawler`의 세 파라미터, 채팅 앱을 흉내 내는 `electron-comms`의 `heartbeat_work`, 시스템 daemon을 흉내 내는 `system-daemon`의 두 파라미터입니다. 셋 다 lifetime이 사용자가 닫을 때까지 도는 `segment-bound`입니다.
>
> 실행 계약은 반복마다 뽑기를 "끝이 정해진 반복일 때만" 허용합니다. 실제 compile 코드는 이 경우를 조용히 **task마다 한 번**으로 바꿉니다. 코드 머리의 설명이 "unbounded (segment-bound) loops compile to LOOP-unbounded bodies whose per-iteration params degrade to per-task draws"라고 적습니다.
>
> 결과는 이렇습니다. 예를 들어 `system-daemon` 하나는 파일 안에서 **매번 똑같은 간격으로** 잠들고 똑같은 길이로 깨어납니다. 흩어짐은 task와 task 사이에만 있고, 한 task의 반복 사이에는 없습니다. 이 항목이 재현해야 할 통계로 "깨어남 빈도와 실행 길이의 분포"를 선언하고 있어서, 한 task 안의 분포를 본다면 그 통계가 나오지 않습니다.
>
> 이것이 의도된 단순화인지, 파일의 표기를 바꿔야 하는 것인지 확인이 필요합니다. 무엇을 열어보면 되는지: 파일의 `sampling` 필드가 "원래 뜻하는 빈도"를 적는 자리인지 "실제로 뽑히는 빈도"를 적는 자리인지를 정한 기록입니다. 저장소에서 그 기록을 찾지 못했습니다.

## 4.5 lifetime: 어떻게 끝나나

task가 끝나는 방식은 세 가지로 나뉩니다. 계약 문서의 표입니다.

| lifetime | 끝나는 시각 | 어떻게 끝나나 |
|---|---|---|
| `segment-bound` | 파일에 박혀 있다 | 바깥 사건. 사용자가 닫는다 |
| `finite` | 없다 | 프로그램이 EXIT에 닿는다. 그 시각은 scheduling의 결과다 |
| `spawned` | 없다 | 실행 중에 FORK로 태어나 EXIT으로 끝난다 |

셋이 나뉘는 이유는 계약 문서의 한 원칙에서 나옵니다.

> "**Compile time resolves all randomness; run time resolves all timing that scheduling can influence.**"

compile 단계가 모든 무작위성을 해결하고, 실행 단계가 scheduling이 영향을 줄 수 있는 모든 시각을 해결한다.

음악 재생기를 사용자가 언제 끄는지는 scheduler와 무관합니다. 그러니 파일에 박아둡니다. 반면 CPU 계산 작업이 언제 끝나는지는 scheduler가 CPU를 얼마나 주느냐에 달려 있습니다. 그걸 파일에 박아두면, 나쁜 설정 아래에서도 작업이 제시간에 끝나버리는 이상한 일이 생깁니다. primitive를 볼 때 본 SLEEP의 착시, 즉 나쁜 설정 아래에서 부하가 저절로 가벼워지는 문제와 같은 종류입니다.

**그래서 lifetime은 archetype의 성격입니다.** 계산 작업은 `finite`일 수밖에 없고, 재생기는 `segment-bound`일 수밖에 없습니다. 이 규칙이 compile과 실행 사이에서 어떻게 지켜지는지는 다음 권과 시뮬레이터 권의 몫입니다.

## 4.6 binding_params와 scalable

### 이름만 적는 손잡이

`binding_params`는 이 archetype을 가져다 쓰는 timeline이 **반드시 채워야 하는 값들의 이름**입니다. 값은 적지 않습니다.

```yaml
cpu-batch:
  binding_params: [total_work]

build-orchestrator:
  binding_params: [spawn_count, parallelism_cap, child_name]
```

`cpu-batch`는 계산만 하다가 끝나는 작업인데, **얼마나 큰 작업인지**는 archetype이 모릅니다. 30초짜리 학습인지 130초짜리 학습인지는 상황 설계의 문제이기 때문입니다. 메모가 그 이유를 적습니다.

> "total_work (the job size, hence the finite lifetime) is scenario design, so it binds in the timeline, not here."

작업의 크기는 상황 설계이므로 여기가 아니라 timeline에서 채운다.

`build-orchestrator`의 `spawn_count`와 `parallelism_cap`은 개수입니다. archetype의 경계를 볼 때 개수가 archetype 밖에 있다고 했는데, 그 규칙이 이렇게 구현됩니다. **이름은 archetype이 정하고, 값은 쓰는 쪽이 채웁니다.** 파일 머리에 규칙이 명시되어 있습니다.

> "`binding_params`: names only — knobs the timeline/scenario binding must supply (counts, caps, total work). Counts never carry values here (archetype-plan §3); binding-time defaults live in modeling_notes prose."

이름만 적는다. 개수는 여기서 절대 값을 갖지 않는다. 쓰는 쪽이 따를 기본값은 메모의 문장으로만 적는다.

### CPU 한 자리에 맞추기

`scalable`은 한 archetype에서만 비어 있지 않습니다. 게임의 `game-task-chain`입니다. 게임을 분석한 출처의 숫자는 코어가 여러 개인 기계에서 잰 것이라, CPU 자리 하나짜리 시뮬레이터에 그대로 넣으면 기계가 감당하지 못합니다. 그래서 compile 단계가 **지정된 값만, 지정된 규칙대로** 줄이도록 허락합니다. 나머지 열한 항목은 `scalable: []`, 빈 목록입니다. RUN의 길이는 기계와 무관한 CPU 요구량이라서 줄일 이유가 없다는 뜻입니다.

어떤 규칙으로 줄이고 그 규칙의 근거가 무엇인지는 게임 항목을 볼 때, 그리고 compile을 다루는 다음 권에서 봅니다.

## 4.7 두 종류의 메모

항목의 마지막 필드가 이 권에서 가장 자주 인용하는 필드입니다. `modeling_notes`.

### 누가 무엇을 적나

출처에 대한 메모는 사실 두 곳에 있습니다. 하나는 **출처 등록부**의 `notes`이고, 하나는 **archetype 항목**의 `modeling_notes`입니다. 계획 문서가 둘의 역할을 한 문장으로 나눕니다.

> "The registry's `notes` records what a source establishes; `modeling_notes` records what we built on it — together they are the paper-writing guardrail against over-claiming."

등록부의 `notes`는 **출처가 무엇을 확립하는지**를 적고, `modeling_notes`는 **우리가 그 위에 무엇을 지었는지**를 적는다. 둘이 함께 논문을 쓸 때 과장을 막는 난간이 된다.

같은 출처에 대한 두 메모를 나란히 보면 차이가 선명합니다. 게임 분석 발표에 대한 것입니다.

```text
   출처 등록부 notes (출처가 말하는 것)
   ─────────────────────────────────
   "~300 tasks per game, ~90% long-lived … per-schedule runtimes
    few-hundred-us average to few-ms max (wineserver ~260 us,
    worker ~1.65 ms), stable and predictable per task (s13) …
    LAVD defines no spec format: any schema encoding of these
    observations … is our modeling"

   archetype modeling_notes (우리가 지은 것)
   ─────────────────────────────────
   "the linearization of the s16-s17 waker-waiter graph into a chain,
    and every field name, are ours … chain_length 16 sits in the
    source's 15-20 frame-critical band … tail param values are our
    placeholder encoding of near-idle"
```

위는 발표가 말한 관찰이고, 아래는 그 관찰을 체인 모양으로 펴고, 길이를 16으로 고르고, 나머지 task의 값을 임시로 정한 우리 결정입니다.

### 필드 이름은 출처가 정당화하지 않습니다

archetype의 경계를 정한 규칙은 두 문장입니다. 첫 문장은 scheduler가 볼 수 없는 이름과 개수와 의미가 archetype에 들어갈 수 없다는 것이었습니다. 두 번째 문장이 여기서 쓰입니다.

> "a `source:` tag justifies the *values and described structure*, never the *field names* — field names are our schema's invention, and every entry whose shape leans on a source records that derivation in `modeling_notes` (§5)."

출처 표시는 **값과 출처가 서술한 구조**를 정당화할 뿐, **필드 이름**은 절대 정당화하지 않는다. 필드 이름은 우리 스키마의 발명이고, 모양을 출처에 기댄 항목은 그 유도 과정을 메모에 적는다.

예를 들어봅니다. 게임 항목에 `chain_length: 16`이 있고 출처 표시가 `lavd-ossna24`입니다. 이것을 "LAVD 발표가 chain의 길이를 16이라고 했다"로 읽으면 틀립니다. 발표에는 `chain_length`라는 개념이 없습니다. 발표가 말한 것은 "15에서 20개의 게임 task가 scheduling의 60에서 70퍼센트를 차지한다"이고, 그걸 16개짜리 사슬로 옮긴 것은 우리입니다.

웹 개발에 빗대면 API 응답의 필드 이름과 같습니다. 백엔드가 `user_created_at`이라는 필드에 가입 시각을 담아도, 그 시각의 근거는 데이터베이스의 기록이지 필드 이름이 아닙니다. 필드 이름은 API를 설계한 사람이 붙인 것입니다.

> **논문으로.** 이 두 메모의 구분이 논문 문장의 동사를 정합니다. 등록부 `notes`에 있는 내용은 "LAVD의 분석에 따르면 게임 하나가 약 300개의 task를 만든다"처럼 **출처를 주어로** 쓸 수 있습니다. `modeling_notes`에 있는 내용은 "우리는 이 관찰을 16단계의 사슬로 모형화했다"처럼 **우리를 주어로** 써야 합니다.
>
> 논문 초고를 쓸 때 문장 하나마다 "이 주어가 맞나"를 두 메모에 대보면 과장이 걸러집니다. 그게 계획 문서가 말한 "난간"입니다.

## 4.8 무엇이 기계로 검사되나

마지막으로, 이 필드들 중 무엇이 도구로 강제되는지를 봅니다. 사람의 약속과 기계의 검사는 다르기 때문입니다.

저장소의 검사 도구가 archetype 파일에 대해 확인하는 것은 이렇습니다.

```text
   1  필수 필드 여덟 개가 전부 있는가
      category_source, pattern, params, lifetime,
      binding_params, scalable, validation_stats, modeling_notes

   2  lifetime이 세 값 중 하나인가
   3  spawned인 항목에 spawned_by가 있는가
   4  숫자 파라미터마다 source 표시가 있는가
   5  source의 id가 출처 등록부에 있는가
   6  locator가 그 출처가 허용하는 모양인가
   7  sampling이 세 값 중 하나인가
   8  (얼린 뒤에는) 측정 대기 표시가 남아 있지 않은가
```

**여섯 번째가 특히 쓸모 있습니다.** 출처 등록부는 출처마다 locator의 모양을 정규식으로 적어둡니다. interbench는 `man-` 또는 `src-`로 시작해야 하고, LAVD 발표는 `s` 뒤에 슬라이드 번호가 와야 합니다. 그래서 `lavd-ossna24:slide12`라고 잘못 쓰면 검사가 실패합니다.

> **코드로.** 검사는 `dataset/tools/wlc/linter.py`의 `lint_repo` 함수에 있고, 저장소의 CI가 모든 변경마다 돌립니다.

> **확인 필요.** 계획 문서는 `category_source`가 "검사 도구로 기계 확인이 가능하다(machine-checkable by the linter)"고 말합니다. 실제 검사 도구는 이 필드가 **있는지만** 봅니다. 값이 출처 등록부의 id이거나 `meas`인지는 확인하지 않습니다. 지금 파일의 열두 항목은 전부 올바른 값을 갖고 있어서 문제가 드러나지 않을 뿐입니다. 계획 문서의 "기계 확인"이 존재 확인을 뜻한 것인지 값 확인까지를 뜻한 것인지 확인이 필요합니다.

---

## 4장 정리

- 항목 하나에는 정해진 필드가 있습니다. 모양, 파라미터, 뽑는 빈도, 끝나는 방식, 자식 관계, 쓰는 쪽이 채울 손잡이, 줄여도 되는 값, 재현할 통계, 그리고 우리가 지어낸 것에 대한 메모입니다.
- 숫자는 분포로 들어갑니다. 평균 하나로 적으면 scheduler를 실제로 괴롭히는 긴 꼬리가 사라지기 때문입니다.
- 가장 많이 쓰이는 분포는 로그 정규입니다. 중앙값의 몇 배로 흩어지는 값이고, 평균이 중앙값보다 큽니다. 이 가족을 고른 것은 출처가 아니라 밝혀둔 관례입니다.
- 계획 문서는 그 관례를 분포 가족 민감도 분석이 덮는다고 말하지만, 그 분석이 정의된 곳에서 바꿔 보는 대상은 구간 길이의 분포입니다.
- 키 입력 간격 파라미터는 두 논문과 산수와 관례로 만들어졌습니다. Dhakal에서 전체 평균 238.66밀리초, Roeser에서 막힘없음 158밀리초와 멈칫 확률 0.34, 산수로 멈칫 평균 395밀리초, 관례로 흩어짐 0.35와 0.6입니다.
- 원문과 대조하면 세 가지가 보입니다. Dhakal의 평균은 참가자들의 평균이고, Roeser의 158은 로그 척도의 위치여서 평균이라는 필드 이름과 어긋나고, Roeser에는 짝이 되는 멈칫 값 약 253밀리초가 따로 있었습니다.
- 입력 한 번의 계산량은 직전 간격의 균등한 비율로 적었습니다. interbench 코드는 같은 범위를 차례로 올라가는 경사로 흉내 냅니다. 이 선택 때문에 사람이 만지는 창의 task가 시간의 절반을 계산합니다.
- 뽑는 빈도에도 근거가 있습니다. 게임 task의 실행 길이를 task마다 한 번만 뽑는 것은 출처가 실행 시간이 안정적이라고 했기 때문입니다.
- 끝이 없는 반복에서 반복마다 뽑기를 선언한 항목들이 있는데, 실제로는 task마다 한 번으로 바뀌어 뽑힙니다.
- lifetime은 scheduling이 영향을 줄 수 있는 시각을 파일에 박지 않는다는 원칙에서 나옵니다. 계산 작업은 끝나는 시각이 scheduling의 결과여야 합니다.
- 개수와 작업 크기는 archetype이 이름만 적고 값은 쓰는 쪽이 채웁니다.
- 메모가 두 종류입니다. 출처가 무엇을 말하는지는 등록부에, 우리가 무엇을 지었는지는 항목에 적습니다. 출처 표시는 값과 서술된 구조를 정당화할 뿐 필드 이름을 정당화하지 않습니다.
- 출처 표시의 모양은 기계로 검사되지만, 출처가 그 숫자를 정말 말하는지는 기계가 검사하지 않습니다.

---

# 5장 · 근거의 네 등급

## 5.1 출처 표시가 붙었다고 다 같은 근거가 아닙니다

archetype 파일의 숫자에는 전부 출처 표시가 붙어 있습니다. 검사 도구가 그걸 강제합니다. 그런데 출처 표시가 붙어 있다는 것과 **그 숫자를 믿어도 된다**는 것은 다른 이야기입니다.

같은 파일에서 숫자 넷을 뽑아보겠습니다.

```text
   238,660 us     사람의 키 입력 간격 평균        학회 논문의 표에서
   50,000 us      음악 재생의 깨어남 간격          벤치마크 도구의 설명서에서
   11,240,000 us  시스템 daemon의 잠든 간격        우리가 CI 서버에서 재서
   3,000 us       파일 복사 한 덩어리의 계산 길이   우리가 그냥 정해서
```

넷 다 출처 표시가 붙어 있습니다. 그런데 네 숫자로 **말할 수 있는 문장**이 다릅니다.

첫째 숫자로는 "사람들이 옮겨 칠 때 키 간격이 평균 239밀리초쯤이라는 연구가 있다"고 말할 수 있습니다. 둘째 숫자로는 "데스크톱의 음악 재생이 50밀리초마다 깨어난다"고 말할 수 **없습니다.** 말할 수 있는 것은 "커뮤니티 벤치마크가 음악 재생을 그렇게 흉내 낸다"입니다. 셋째 숫자로는 "Ubuntu CI 서버의 기본 daemon들이 이렇게 깨어났다"까지, 넷째 숫자로는 "우리는 이렇게 정했다"까지만 말할 수 있습니다.

이 연구는 이 구분을 **등급**으로 부릅니다. 이 장은 그 등급이 무엇이고, 각 등급이 무엇을 뒷받침할 수 있고 무엇을 못 하는지를 봅니다. 뒤의 모든 장에서 숫자를 볼 때마다 이 등급을 함께 적겠습니다.

## 5.2 첫째 등급: 학술 문헌

인용 문서가 규칙을 이렇게 적습니다.

> "**scholarly** → numbered bibliography. May support empirical, behavioral, and statistical claims within its stated role."

학술 문헌은 논문의 번호 붙은 참고문헌 목록에 들어간다. **자기에게 정해진 역할 안에서** 실험적, 행동적, 통계적 주장을 뒷받침할 수 있다.

심사를 거친 논문과, 공개 보관소에 올라간 논문 원고가 여기 들어갑니다. archetype과 직접 관련된 것은 이렇습니다.

| 출처 id | 무엇 | archetype에서 쓰이는 곳 |
|---|---|---|
| `dhakal-chi18` | 1억 3천 6백만 번이 넘는 키 입력 분석 | 키 입력 간격의 평균 |
| `roeser-rw24` | 타자 막힘을 섞임 분포로 모형화 | 키 입력 간격의 분포 가족 |
| `ocallahan-atc17` | 기록과 재생 시스템 논문 | 컴파일 자식 프로세스가 짧게 산다는 것, 그 개수 |
| `coetzee-arxiv12` | 빌드 시스템 논문. 논문 원고로만 공개 | 위를 보조 |
| `dubroy-chi10`, `chang-chi21` | 브라우저 탭 사용 연구 | 브라우저 프로세스 개수의 근거 |

**"자기에게 정해진 역할 안에서"라는 조건이 핵심입니다.** 인용 문서의 항목마다 `role:` 줄이 있어서, 그 출처가 무엇에 쓰일 수 있는지가 적혀 있습니다. 앞 장에서 본 Dhakal 논문은 학술 문헌이지만 옮겨 치기 안의 간격만 뒷받침할 수 있고, 생각하느라 멈추는 시간은 뒷받침하지 못합니다. 학술 문헌이라고 무엇이든 말해주지는 않습니다.

## 5.3 둘째 등급: 배포된 소프트웨어

> "**deployed-system** → footnote with URL + accessed date + pinned version. Supports **existence claims only** ("this scenario/setting/category exists in shipped software") — never behavioral or statistical claims."

배포된 소프트웨어는 URL과 접속 날짜와 고정한 판본을 적은 각주로 인용한다. **존재에 대한 주장만** 뒷받침한다. "이런 상황, 설정, 분류가 실제로 배포된 소프트웨어에 있다"까지이고, 행동이나 통계에 대한 주장은 절대 뒷받침하지 않는다.

벤치마크 도구, 오픈 소스 저장소, 제품 문서, 발표 슬라이드가 여기 들어갑니다. archetype과 관련된 것은 이렇습니다.

| 출처 id | 무엇 |
|---|---|
| `interbench` | 대화형 작업의 반응성을 재는 커뮤니티 벤치마크 |
| `rt-app` | 주기적 부하를 JSON으로 적어 돌리는 도구 |
| `ananicy-rules` | 프로세스 이름별 우선순위 규칙을 모은 커뮤니티 카탈로그 |
| `lavd-ossna24` | 게임용 scheduler를 소개한 학회 발표 슬라이드 |
| `mozilla-testpilot10` | Firefox 사용자 약 2만 7천 명의 탭 사용 기록 |

### 숫자가 적혀 있어도 둘째 등급입니다

LAVD 발표 슬라이드에는 숫자가 많습니다. 게임 하나가 task를 300개쯤 만들고, 그중 90퍼센트가 오래 살고, 실행 한 번이 수백 마이크로초라는 식입니다. 게임 workload에 대해 이만큼 구체적인 숫자를 준 자료는 드뭅니다.

그래도 등급은 둘째입니다. 인용 문서의 문장입니다.

> "Talk slides — footnote tier despite carrying numbers; pair with `corbet-lwn24` for prose-citable coverage."

발표 슬라이드이므로 **숫자를 담고 있어도** 각주 등급이다. 본문에서 인용할 수 있는 글로는 LWN의 보도 기사와 짝지어 쓴다.

**등급은 숫자가 있느냐가 아니라 그 숫자가 어떤 검증을 거쳤느냐로 정해집니다.** 슬라이드의 숫자는 발표자가 자기 분석을 요약한 것이고, 그 분석 방법과 데이터가 심사를 받지 않았습니다.

### 그러면 둘째 등급의 숫자를 파라미터로 써도 되나

여기서 곧바로 질문이 나옵니다. 둘째 등급이 존재만 뒷받침한다면서, 음악 재생 archetype은 interbench의 50밀리초를 **값으로** 쓰고 게임 archetype은 LAVD의 숫자를 값으로 씁니다. 모순 아닌가요.

저장소의 답은 **무엇을 주장하느냐를 바꾸는 것**입니다. 인용 문서의 interbench 항목입니다.

> "Frame as "the community models interactivity this way", never "desktops behave this way"."

"커뮤니티가 대화형 작업을 이렇게 모형화한다"로 쓰고, "데스크톱이 이렇게 행동한다"로는 절대 쓰지 않는다.

그리고 근거 문서가 이 전략의 이유를 적습니다.

> "These are the sources the scheduler community recognizes on sight; calibrating our parameters to them converts "we made up the numbers" into "we instantiated the standard models.""

이것들은 scheduler 커뮤니티가 보자마자 알아보는 출처다. 우리 파라미터를 거기에 맞추면 "숫자를 지어냈다"가 "**표준 모형을 구체화했다**"로 바뀐다.

그러니까 interbench의 50밀리초를 쓴다는 것은 "실제 음악 재생기가 50밀리초마다 깨어난다"는 주장이 아닙니다. "이 분야 사람들이 대화형 작업을 시험할 때 쓰는 그 모형을 우리도 썼다"는 주장입니다. **존재 주장의 한 형태**입니다. 그 모형이 존재하고 널리 쓰인다는 것.

웹 개발에 빗대면 성능 시험에서 업계 표준 벤치마크의 부하 모형을 쓰는 것과 같습니다. "우리 서비스의 실제 사용자는 이렇게 행동한다"가 아니라 "표준 시나리오에서 이렇게 나왔다"입니다. 실제 사용자와 다를 수 있다는 것은 모두가 압니다. 대신 **남들과 비교할 수 있고, 우리가 숫자를 유리하게 골랐다는 의심을 받지 않습니다.**

> **논문으로.** 이 구분이 논문 문장을 이렇게 가릅니다.
>
> ```text
>    쓸 수 있는 문장
>    "Periodic tasks follow interbench's audio and video models."
>    (주기 작업은 interbench의 오디오·영상 모형을 따른다)
>
>    쓸 수 없는 문장
>    "Desktop audio playback wakes every 50 ms."
>    (데스크톱의 오디오 재생은 50 ms마다 깨어난다)
> ```
>
> 둘째 문장이 논문에 들어가면 심사자가 "그 50밀리초는 누가 쟀나요"라고 묻고, 답할 수 없습니다. interbench 설명서 자체가 그 값이 "잘 만든 오디오 프로그램이 했을 버퍼링을 무시한다"고 적어두었기 때문입니다.

## 5.4 셋째 등급: 우리 측정

셋째는 이 연구가 직접 잰 것입니다. 출처 id는 `meas-ci` 하나이고, locator로 어떤 측정의 몇 번째 실행인지를 적습니다. `meas-ci:cli:3`은 명령줄 프로그램을 재는 측정의 세 번째 실행이라는 뜻입니다.

인용 문서가 이 등급이 할 수 있는 것을 좁게 정합니다.

> "structural/shape claims about software behavior only (fork structure, counts, lifetime shapes, periods, heartbeats, comm strings); machine-relative absolutes carry the runner spec and rank as convention-informed-by-measurement. Never desktop-performance claims. N-run spread reported."

소프트웨어 행동의 **구조와 모양**에 대한 주장만 한다. 자식 프로세스를 만드는 구조, 개수, 수명 분포의 모양, 주기, 주기적 신호, 프로세스 이름 문자열이 여기 든다. 기계에 따라 달라지는 **절대값**에는 측정한 서버의 사양을 붙이고, "**측정으로 보강한 관례**" 등급으로 친다. 데스크톱 성능에 대한 주장은 절대 하지 않는다. 여러 번 돌려서 흩어짐을 보고한다.

**셋째 등급 안에 등급이 둘 있는 셈입니다.**

```text
   셋째 등급 · 구조와 모양
   ─────────────────────
   "make -j8 한 번에 컴파일러 자식이 약 1만 2천 개 생긴다"
   "시스템 daemon은 수 초에서 수십 초 간격으로 불규칙하게 깬다"
   → 다른 기계에서 돌려도 대체로 같은 모양이 나올 것

   셋째 등급 · 기계에 따라 달라지는 절대값
   ──────────────────────────────────
   "파일 복사 중 CPU를 쓰는 비율이 23.1퍼센트다"
   "컴파일러 자식 하나가 디스크를 약 3.6밀리초 기다린다"
   → CPU 속도, 디스크 속도에 따라 크게 달라질 것
   → "측정으로 보강한 관례"로 격하
```

디스크 대기 시간은 그 서버의 디스크가 NVMe 저장장치라서 짧게 나온 것입니다. 회전 디스크를 쓰는 기계라면 몇 배가 됩니다. 그러니 그 숫자는 "데스크톱의 컴파일러가 3.6밀리초 기다린다"가 아니라 "이 서버에서는 이렇게 나왔고, 우리는 그 값을 관례로 쓴다"입니다.

이 등급은 한 장을 따로 들여 봅니다.

## 5.5 넷째 등급: 우리가 정한 것

넷째 등급은 출처가 없는 숫자입니다. 이 연구가 **정한** 값이고, 항목의 메모가 "ours", "our convention", "our modeling"이라고 표시합니다.

실제 파일에서 이렇게 표시된 것들을 모아보면 몇 가지 종류로 나뉩니다.

| 종류 | 예 |
|---|---|
| 흩어짐의 크기 | 로그 정규 분포의 `sigma_log` 여러 개. 측정은 중앙값만 주고 흩어짐은 관례로 정한 경우 |
| 덩어리의 크기 | 파일 복사를 3밀리초짜리 계산 덩어리로, 다운로드를 1밀리초짜리 덩어리로 쪼갠 것 |
| 나누는 비율 | 컴파일러 자식의 계산을 앞 90퍼센트, 뒤 10퍼센트로 나눈 것 |
| 기본값 | `make -j8`의 8 |
| 분포 가족 | 모든 분포를 로그 정규로 한 것 |
| 산수 | 비율을 시간으로 바꾸기, 섞임 분포의 빈칸 채우기 |
| 모양 | 프로그램의 순서, 사슬로 편 구조, 필드 이름 전부 |

**넷째 등급이 있다는 것 자체는 약점이 아닙니다.** 어떤 모형이든 출처가 말해주지 않는 빈칸이 생기고, 누군가는 그 빈칸을 채워야 합니다. 약점이 되는 것은 **채운 줄 모르게 채우는 것**입니다. 그래서 이 연구의 규칙은 넷째 등급을 없애는 것이 아니라 **넷째 등급이라고 적는 것**입니다.

> **이 연구에서는.** 넷째 등급의 숫자에도 출처 표시가 붙어 있다는 점에 주의해야 합니다. 예를 들어 파일 복사 archetype의 `block_cpu: 3000`에는 `source: "meas-ci:cli:3"`이 붙어 있습니다. 그런데 메모를 읽으면 이렇습니다.
>
> > "The meas-ci:cli:3 tag covers the block pair jointly: the 3 ms block granularity and sigmas are our convention; the measured quantity is the per-process cpu:wall duty of a stream."
>
> 이 측정 표시는 두 파라미터를 **한 쌍으로** 덮는다. 3밀리초라는 덩어리 크기와 흩어짐은 우리 관례이고, 측정한 것은 **계산 시간과 벽시계 시간의 비율**이다.
>
> 측정은 "CPU를 23.1퍼센트 쓴다"는 비율 하나를 줬습니다. 그 비율을 "3밀리초 계산 + 10밀리초 대기"로 만든 것은 우리입니다. "6밀리초 계산 + 20밀리초 대기"로 만들어도 비율은 같습니다. **출처 표시는 두 숫자에 붙어 있지만, 출처가 뒷받침하는 것은 두 숫자의 비율 하나뿐입니다.**
>
> 파일의 `source:` 필드만 봐서는 이 사정이 보이지 않습니다. 메모를 읽어야 보입니다. 이게 메모가 필수 필드인 이유입니다.

## 5.6 인용이 확인된 정도

등급과 별개로 붙는 표시가 하나 더 있습니다. **그 인용 자체가 확인됐는가**입니다. 인용 문서의 범례입니다.

> "Status legend: `verified` (coordinates confirmed against primary sources, date given) · `to-pin` (identification certain; exact URL/version to pin before submission) · `provisional` (identification incomplete — do not cite until resolved)."

| 상태 | 뜻 |
|---|---|
| `verified` | 1차 자료와 대조해서 서지 정보를 확인했다. 날짜를 적는다 |
| `to-pin` | 무엇인지는 확실하다. 정확한 URL이나 판본은 제출 전에 고정한다 |
| `provisional` | 무엇인지 아직 확실하지 않다. 해결될 때까지 인용하지 않는다 |

이 표시는 **"그 문서가 존재하고 우리가 가리키는 게 그 문서가 맞다"**를 말합니다. **"그 문서가 우리가 쓴 내용을 말한다"**와는 다릅니다.

이 차이가 이 권을 쓰면서 실제로 드러났습니다. 컴파일러 자식 프로세스의 근거인 `ocallahan-atc17`은 인용 문서에 `verified`로 적혀 있습니다. 논문의 저자, 제목, 학회, 쪽수가 전부 맞습니다. 그리고 숫자 2,430과 인용한 문장도 원문에 그대로 있습니다. 그런데 **그 숫자가 어떤 빌드에서 나왔는지**에 대한 저장소의 설명이 원문과 다릅니다. 이 이야기는 컴파일러 항목을 따라가는 장에서 원문과 함께 봅니다.

## 5.7 손으로 따라가기: 숫자 일곱 개에 등급 붙이기

실제 파일의 숫자 일곱 개입니다. 각 숫자의 출처 표시와 메모를 보고 등급을 정해봅니다. 답을 보기 전에 스스로 정해보는 편이 낫습니다.

### 1. 음악 재생의 `period: 50000`

출처 표시 `interbench:man-audio`. 메모: 설명서가 50 ms를 말한다.

<br>

**둘째 등급.** interbench는 배포된 소프트웨어입니다. 이 숫자로 할 수 있는 말은 "커뮤니티 모형을 따랐다"입니다.

### 2. 키 입력 간격의 `overall_mean_us: 238660`

출처 표시 `dhakal-chi18`.

<br>

**첫째 등급.** 다만 역할이 제한됩니다. 옮겨 치기 안의 간격이고, 5초 넘는 멈춤은 빠진 값이며, 여러 사람의 평균입니다.

### 3. 키 입력 간격의 `pause_mean_us: 395235`

출처 표시는 2번과 같은 `dhakal-chi18`. 메모: "our arithmetic".

<br>

**넷째 등급.** 첫째 등급 두 편의 숫자를 넣은 산수의 결과입니다. 재료는 첫째 등급이지만 결과는 어느 논문에도 없습니다. **산수가 등급을 한 단계 낮춥니다.** 산수가 맞더라도 "두 논문의 숫자를 한 식에 넣어도 된다"는 가정이 들어갔기 때문입니다.

### 4. 시스템 daemon의 `idle_gap` 중앙값 11,240,000

출처 표시 `meas-ci:gui:2`. 메모: CI 서버의 기본 daemon 51개를 재서 얻은 간격 분포.

<br>

**셋째 등급, 구조와 모양 쪽.** "daemon은 평균 수십 초 간격으로 불규칙하게 깬다"는 모양은 기계를 바꿔도 크게 달라지지 않을 것입니다. 다만 어떤 daemon이 떠 있느냐는 배포판마다 다르고, 이 값은 Ubuntu CI 서버의 daemon들입니다.

### 5. 파일 복사의 `io_wait` 중앙값 10,000

출처 표시 `meas-ci:cli:3`. 메모: CPU 비율 0.231에서 계산.

<br>

**셋째 등급의 절대값 쪽, 즉 측정으로 보강한 관례.** 비율 0.231은 그 서버의 디스크 속도에 달린 값이고, 10밀리초라는 절대값은 3밀리초라는 우리 관례에 그 비율을 곱해서 나온 것입니다. 셋째 등급과 넷째 등급이 한 숫자에 섞여 있습니다.

### 6. 컴파일러 자식의 `sigma_log: 1.91`

출처 표시 `meas-ci:cli:3`. 메모: 측정한 평균과 중앙값의 비에서 계산.

<br>

**셋째 등급.** 흩어짐이 관례인 경우가 많은데 이 값은 다릅니다. 측정한 평균 약 90밀리초와 측정에서 끌어낸 중앙값 약 14.4밀리초의 비 6.25에서 역산했습니다. 어떻게 계산했는지는 컴파일러 항목을 끝까지 따라가는 장에서 봅니다.

### 7. 게임의 `frame_period: 16667`

출처 표시 `lavd-ossna24`. locator 없음.

<br>

**표시로는 둘째 등급입니다. 그런데 원문을 열면 이 숫자가 없습니다.** LAVD 발표 슬라이드 30장 어디에도 16.7밀리초나 frame 예산이라는 말이 나오지 않습니다. 이 숫자가 실제로 어디서 왔는지는 게임 항목에서 봅니다.

**이 연습에서 가져갈 것.** 출처 표시만 보고 등급을 정할 수 없습니다. 3번과 5번은 출처 표시가 가리키는 등급보다 실제 등급이 낮고, 7번은 표시가 가리키는 문서에 숫자가 없습니다. **메모를 읽어야 하고, 때로는 원문을 열어야 합니다.**

---

## 5장 정리

- 출처 표시가 붙은 숫자라도 그 숫자로 말할 수 있는 문장이 다릅니다. 이 연구는 그 차이를 네 등급으로 나눕니다.
- 첫째 등급은 학술 문헌입니다. 행동과 통계에 대한 주장을 뒷받침할 수 있지만, 그 출처에 정해진 역할 안에서만입니다.
- 둘째 등급은 배포된 소프트웨어입니다. 존재 주장만 뒷받침합니다. 발표 슬라이드는 숫자가 적혀 있어도 이 등급입니다.
- 둘째 등급의 숫자를 파라미터로 쓸 때는 주장을 바꿉니다. "데스크톱이 이렇게 행동한다"가 아니라 "커뮤니티의 표준 모형을 구체화했다"입니다.
- 셋째 등급은 우리 측정입니다. 구조와 모양에 대한 주장은 할 수 있고, 기계에 따라 달라지는 절대값은 측정으로 보강한 관례로 격하됩니다.
- 넷째 등급은 우리가 정한 값입니다. 흩어짐, 덩어리 크기, 나누는 비율, 기본값, 분포 가족, 산수, 모양이 여기 들어갑니다. 규칙은 없애는 것이 아니라 적는 것입니다.
- 출처 표시는 넷째 등급의 숫자에도 붙어 있습니다. 측정 표시가 두 숫자에 붙어 있어도 측정이 뒷받침하는 것은 둘의 비율 하나일 수 있습니다.
- 산수는 등급을 낮춥니다. 첫째 등급의 두 숫자를 한 식에 넣은 결과는 넷째 등급입니다.
- 인용의 확인 상태는 "그 문서가 맞다"를 말할 뿐 "그 문서가 우리 내용을 말한다"를 말하지 않습니다.
- 등급은 출처 표시만 보고 정할 수 없습니다. 메모를 읽어야 하고, 때로는 원문을 열어야 합니다.

---

# 6장 · 열두 개의 목록

## 6.1 목록을 통째로

먼저 열두 개를 한 번에 봅니다. 파일은 항목들을 **다섯 가족**으로 묶어두고, 가족마다 주석으로 어디서 거둬왔는지를 함께 적습니다.

| 가족 | archetype | 한 줄 설명 | 프로그램 모양 |
|---|---|---|---|
| periodic-interactive | `audio-playback` | 소리 재생 | TIMER → RUN 반복 |
| | `video-playback` | 영상 재생 | TIMER → RUN 반복 |
| | `desktop-interactive` | 사람이 만지는 창 | 입력 WAIT → RUN 반복 |
| compute/batch | `cpu-batch` | 끝날 때까지 계산만 하는 작업 | RUN → EXIT |
| | `compiler-child` | 컴파일러 자식 하나 | RUN → WAIT → RUN → EXIT |
| | `build-orchestrator` | 컴파일을 지휘하는 부모 | (RUN → FORK) 반복 → WAIT → EXIT |
| IO | `io-stream` | 연속으로 읽고 쓰기 | (RUN → WAIT) 반복 → EXIT |
| | `background-crawler` | 뒤에서 천천히 파일을 훑는 색인기 | RUN → WAIT → SLEEP 반복 |
| structural-special | `game-task-chain` | 게임 하나 | 사슬 모양으로 펼쳐지는 task 약 300개 |
| meas | `network-bulk` | 회선을 꽉 채우는 다운로드 | (WAIT → RUN) 반복 → EXIT |
| | `electron-comms` | 대부분 쉬다가 가끔 깨는 채팅 앱 | TIMER → RUN 반복 |
| | `system-daemon` | 거의 쉬는 시스템 서비스 | SLEEP → RUN 반복 |

가족 이름 다섯 개를 풀면 이렇습니다.

- **periodic-interactive**: 주기적이거나 사람과 주고받는 작업. interbench의 대화형 작업 목록에서 거둬왔습니다.
- **compute/batch**: 계산 위주의 batch 작업. interbench의 부하 목록과 컴파일을 분석한 논문에서 거둬왔습니다.
- **IO**: 입출력 위주의 작업. interbench의 부하 목록과 ananicy 카탈로그의 분류에서 거둬왔습니다.
- **structural-special**: 구조가 특별한 작업. 게임 scheduler 발표에서 거둬왔습니다.
- **meas**: 문헌의 분류 체계가 없어서 우리 측정에서 부류 자체를 끌어낸 작업들입니다.

**앞의 넷과 마지막 하나의 성격이 다릅니다.** 앞의 넷은 누군가 이미 "이런 종류의 작업이 있다"고 정리해둔 것을 가져왔고, 마지막 하나는 그런 정리가 없었습니다. 이 차이는 다음 장에서 자세히 봅니다.

이 장은 열두 개를 하나씩 보면서, 각각이 **어떤 실제 소프트웨어를 흉내 내는지**, 핵심 숫자가 무엇이고 **그 숫자가 몇 등급인지**를 적습니다. 컴파일러 자식 항목은 뒤에서 한 장을 통째로 들여 따라가므로 여기서는 짧게 봅니다. 측정에서 온 숫자들이 어떻게 얻어졌는지도 뒤의 측정 장에서 자세히 봅니다.

## 6.2 periodic-interactive 가족

### audio-playback — 소리 재생

```text
   반복: TIMER(50,000 us) → RUN(2,500 us)
```

50밀리초마다 깨어나 2.5밀리초 계산합니다. 초당 20번, CPU 5퍼센트입니다. 앞에서 세 단계를 끝까지 따라간 항목입니다.

**흉내 내는 것:** 음악 재생기(`spotify`), 화상 회의의 소리 담당 부분(`zoom`)입니다.

**숫자의 등급:** 둘째 등급입니다. interbench가 소리 재생을 흉내 내는 모형이고, interbench 설명서 스스로 "잘 만든 오디오 프로그램이 했을 버퍼링을 무시한다"고 적어둔 단순화입니다.

### video-playback — 영상 재생

```text
   반복: TIMER(16,667 us) → RUN(6,667 us)
```

초당 60번 깨어나고, 한 번에 6.667밀리초씩, CPU 40퍼센트를 씁니다.

**흉내 내는 것:** 영상 재생기(`mpv`), 게임 화면을 합성하는 `gamescope`, 그리고 화상 회의의 영상 담당 부분(`zoom`)입니다.

**숫자의 등급:** 둘째 등급입니다. interbench 설명서가 "60fps로는 꽤 무거운 재생"이라고 적은 모형입니다.

> **이 연구에서는.** 화상 회의가 이 항목에 묶여 있는 것은 **밝혀둔 근사**입니다. 1권에서 봤듯이 화상 회의는 받은 영상을 풀어 그리는 동시에 내 카메라 영상을 압축해 보내고 네트워크를 계속 씁니다. 이 항목은 그중 받아서 그리는 쪽만 흉내 냅니다. 항목의 메모가 이유를 적습니다.
>
> > "conferencing's encode + network components are out of measurement reach, and inventing parameters for them is forbidden."
>
> 회의의 압축과 네트워크 부분은 측정이 닿지 않는 곳에 있고, **그 파라미터를 지어내는 것은 금지되어 있다.** 측정 캠페인은 CI 서버에서 돌아서 카메라도 상대방도 없고, 압축 부하를 분포로 준 문헌도 찾지 못했습니다. 그래서 숫자를 지어내는 대신 가장 가까운 항목에 묶고 그 사실을 적었습니다.

### desktop-interactive — 사람이 만지는 창

```text
   반복: WAIT(input) → RUN(burst)
         입력 사이 간격: 두 성분 로그 정규 섞임, 평균 238.66 ms
         burst = 직전 간격 × (0에서 1 사이 균등 비율)
```

키 입력이 올 때까지 기다리다가, 오면 계산합니다. 입력이 언제 오는지는 compile 단계에서 미리 뽑아 바깥 사건으로 파일에 적어둡니다.

**흉내 내는 것:** 문서 편집기(`soffice.bin`), 브라우저의 화면 부분(`chrome`), 코드 편집기(`code`), 이미지 편집기(`gimp`), 영상 편집기(`kdenlive`), 메일 프로그램(`thunderbird`)입니다. 사람이 앞에 앉아 있는 상황의 **주인공**을 전부 이 항목이 맡습니다.

**숫자의 등급:** 한 항목에 네 등급이 다 섞여 있습니다. 앞에서 따라간 대로 입력 간격의 평균은 첫째 등급, 분포 가족은 첫째 등급, 멈칫 평균은 넷째 등급의 산수, 흩어짐은 넷째 등급의 관례이고, 계산량 비율은 둘째 등급의 문장을 넷째 등급의 방식으로 옮긴 것입니다.

그리고 입력이 **어느 창으로** 가는지는 이 항목이 아니라 timeline의 `focus` 필드가 정합니다. 사용자의 입력이 향하는 창이 아니면 이 task는 입력을 한 번도 받지 않고, 그래서 CPU를 전혀 쓰지 않습니다. 브라우저가 떠 있지만 사람이 문서를 쓰고 있다면, 브라우저 task는 이름만 보이고 조용합니다.

> **이 연구에서는.** 이 항목에는 판정할 기준이 없습니다. 재현할 통계란의 값이 `none`이고, 이유는 이렇습니다.
>
> > "no full behavioral referee exists — live-usage validation was not performed (stated limitation, building-plan §7); the released sampler + privacy-scrub tool is the open falsification invitation."
>
> 행동 전체를 판정할 기준이 없다. 실제 사용 중인 기계에서 검증하는 일은 하지 않았고, 이것은 밝혀둔 한계다. 대신 수집 도구와 개인정보 제거 도구를 공개해서, **누구든 자기 기계로 우리 분포를 반증해볼 수 있게** 한다.

## 6.3 compute/batch 가족

### cpu-batch — 끝날 때까지 계산만

```text
   RUN(total_work) → EXIT
```

가장 단순한 항목입니다. 파라미터가 하나도 없습니다. 얼마나 큰 작업인지(`total_work`)는 쓰는 쪽이 채웁니다.

**흉내 내는 것:** 머신러닝 학습(`python3`), 영상 인코딩(`ffmpeg`), 형식 변환(`HandBrakeCLI`), 전체 재색인 중인 색인기(`tracker-miner-fs-3`), 바이러스 검사(`clamscan`)입니다.

**부류의 근거:** interbench의 부하 목록 중 Burn입니다. 설명서의 문장입니다.

> "Burn: A configurable number of threads fully cpu bound (4 by default)."

CPU를 완전히 쓰는 thread를 설정한 수만큼. 기본값은 4개.

**원문에서 가져오지 않은 것이 있습니다.** "4개"입니다. 메모가 적습니다.

> "Burn's 4-thread structure is not carried — one task saturates the demand it is given; multiplicity is a binding-time count (archetype-plan §3)."

Burn의 thread 4개 구조는 가져오지 않는다. task 하나가 주어진 요구량을 포화시킨다. 몇 개인지는 binding에서 정한다.

> **이 연구에서는.** 이 항목에 걸린 가장 중요한 결정이 메모 끝에 있습니다. 이 연구의 핵심 한 쌍에서 파일 색인기 `tracker-miner-fs-3`를 이 항목에 묶었다는 것입니다.
>
> > "it models an indexer in full-rescan CPU-saturating state so the P1 pair is behaviorally identical; the everyday low-intensity indexer remains background-crawler elsewhere (C4/S14). The two bindings of one name are intentional, not an inconsistency."
>
> 전체를 다시 훑느라 CPU를 포화시키는 상태의 색인기를 흉내 낸 것이고, 그래서 한 쌍의 두 파일이 행동으로 똑같아진다. 평소의 느린 색인기는 다른 곳에서 `background-crawler`로 남는다. **한 이름에 두 가지 묶음이 있는 것은 의도이지 모순이 아니다.**
>
> 파일 색인기가 늘 CPU를 포화시키지는 않습니다. 그런데 핵심 쌍은 "행동이 똑같다"가 전제라서, 머신러닝 학습과 똑같이 행동하는 순간의 색인기를 골랐습니다. 그 순간이 실제로 존재한다는 것이 이 선택의 근거입니다.

> **확인 필요.** 메모가 "평소의 느린 색인기는 다른 곳에서 `background-crawler`로 남는다"고 하고 그 자리로 파일 묶음 C4와 상황 S14를 가리키는데, 지금 데이터셋의 timeline 파일 어디에도 `background-crawler`에 묶인 task가 없습니다. 파일 묶음 C4의 세 파일도 다른 archetype만 씁니다. 그러니 지금 상태에서 `tracker-miner-fs-3`가 등장하는 곳은 전부 CPU를 포화시키는 쪽입니다. 메모의 문장이 계획을 적은 것인지, 파일이 바뀌면서 문장이 남은 것인지 확인이 필요합니다.

### compiler-child와 build-orchestrator — 컴파일

```text
   build-orchestrator:  (RUN(dispatch_overhead) → FORK) × spawn_count
                        → WAIT(children) → EXIT

   compiler-child:      RUN(cpu_burst) → WAIT(disk) → RUN(cpu_tail) → EXIT
```

`make`가 부모이고 `cc1` 같은 컴파일러가 자식입니다. 부모는 자식 하나를 내보낼 때마다 조금 계산하고, 동시에 도는 자식이 정해진 수에 닿으면 자리가 날 때까지 기다립니다. 자식은 계산하고, 디스크를 잠깐 기다리고, 조금 더 계산하고 끝납니다.

**흉내 내는 것:** `make`와 그 자식들입니다. 커널 업데이트 뒤 배포판이 알아서 모듈을 다시 빌드하는 `dkms`도 같은 부모 archetype에 이름만 바꿔 묶입니다.

**숫자의 등급:** 부류의 존재는 첫째 등급 논문에서, 모든 파라미터 값은 셋째 등급 측정에서, 계산을 90 대 10으로 나눈 것과 동시 실행 수 8은 넷째 등급입니다.

이 두 항목은 뒤에서 한 장을 들여 원문부터 끝까지 따라갑니다. 거기서 **출처 논문이 말하는 빌드가 저장소 문서의 설명과 다르다**는 것도 원문과 함께 봅니다.

## 6.4 IO 가족

### io-stream — 연속으로 읽고 쓰기

```text
   반복: RUN(block_cpu 중앙값 3 ms) → WAIT(io 중앙값 10 ms)   … total_work가 찰 때까지
   → EXIT
```

한 덩어리를 처리하고, 디스크를 기다리고, 다음 덩어리를 처리합니다. CPU를 쓰는 비율이 약 23퍼센트입니다.

**흉내 내는 것:** 백업 도구(`borg`), 압축 도구(`7z`)입니다.

**부류의 근거:** interbench의 Write와 Read 부하입니다.

> "Write: A streaming write to disk repeatedly of a file the size of physical ram."

> "Read: Repeatedly reading a file from disk the size of physical ram (to avoid any caching effects)."

메모리만 한 크기의 파일을 디스크에 계속 쓰기, 그리고 캐시 효과를 피하려고 메모리만 한 크기의 파일을 계속 읽기.

**숫자의 등급:** 메모가 적듯이 interbench는 "부류를 확립하지만 덩어리 단위의 시간은 공개하지 않습니다(publish no per-block timing)". 그래서 값은 셋째 등급 측정에서 왔습니다. 그리고 앞 장에서 봤듯이 측정이 준 것은 **CPU 비율 0.231 하나**이고, 3밀리초라는 덩어리 크기는 넷째 등급 관례입니다.

측정에서 흥미로운 점이 하나 있습니다. 파일 복사를 캐시가 따뜻한 상태에서 재면 비율이 0.276, 캐시를 비우고 재면 0.231이 나옵니다. 항목은 **캐시를 비운 쪽**을 골랐는데, 이유가 interbench의 Read 문장 괄호 안에 있습니다. "캐시 효과를 피하려고". 출처가 캐시를 피하는 부하를 정의했으니, 측정도 그 조건에 맞춘 것입니다.

### background-crawler — 뒤에서 천천히 훑는 색인기

```text
   반복: RUN(scan_burst 중앙값 1.6 ms) → WAIT(io 중앙값 5.9 ms)
         → SLEEP(throttle 중앙값 3.8 s)
```

조금 훑고, 디스크를 기다리고, **몇 초씩 쉽니다.** 쉬는 구간이 이 항목의 성격입니다. 사용자를 방해하지 않으려고 스스로 속도를 늦추는 색인기입니다.

**부류의 근거:** ananicy 카탈로그입니다. 2권에서 봤듯이 이 카탈로그는 프로세스 이름마다 우선순위 분류를 붙여둔 커뮤니티 목록이고, 분류 정의 파일에 이런 항목이 있습니다.

```text
# Type: BackGround CPU/IO Load
# Background CPU/IO it's needed, but it must be as silent as possible
{ "type": "BG_CPUIO", "nice": 16, "ioclass": "idle", "sched": "idle" }
```

배경의 CPU와 입출력 작업은 필요하지만 **최대한 조용해야 한다.** 그리고 KDE 데스크톱의 색인기가 이 분류에 들어가 있습니다.

```text
# https://community.kde.org/Baloo
# Baloo is the file indexing and file search framework for KDE.
{ "name": "baloo_file", "type": "BG_CPUIO" }
```

> **확인함.** 2026-09-13에 카탈로그 저장소(github.com/CachyOS/ananicy-rules)를 받았습니다. 받은 시점의 커밋이 `03ef03fb`(2026-09-08)로, 2권이 같은 카탈로그를 센 커밋과 같습니다. 위의 `baloo_file` 항목은 `00-default/DEs-and-WMs/plasma.rules`에 있습니다.
>
> 같은 커밋에서 `tracker-miner-fs-3`, `updatedb`, `cc1`, `gcc`, `make`, `clamscan`을 이름으로 가진 항목은 찾지 못했습니다. 바이러스 검사 쪽은 daemon인 `clamd`가 `BG_CPUIO`로 들어 있습니다. 그러니 이 카탈로그가 뒷받침하는 것은 "**배경 입출력 작업이라는 분류가 있고, 색인기가 실제로 그 분류에 들어가 있다**"까지입니다.

**숫자의 등급:** 카탈로그는 분류와 우선순위 값만 담고 시간은 담지 않습니다. 파라미터는 전부 셋째 등급 측정입니다. CI 서버에서 GNOME의 색인기 `tracker-miner-fs-3`를 daemon 모드로 300초씩 다섯 번 돌려서 잰 값입니다.

측정 과정에서 나온 발견 하나가 메모에 남아 있습니다.

> "Foreground finding retained: foreground scans never throttle (clamscan per-proc duty ~1.0 warm AND ~0.98 cold) — the daemon-mode run is the only valid pacing referee."

앞에서 직접 실행한 검사는 **절대 속도를 늦추지 않는다.** 바이러스 검사를 명령으로 돌리면 캐시가 따뜻하든 차갑든 CPU를 거의 100퍼센트 쓴다. 그래서 속도를 늦추는 모양을 잴 수 있는 것은 daemon으로 돌린 경우뿐이다.

이 발견이 앞 절의 결정과 맞물립니다. 사람이 직접 돌린 검사나 전체 재색인은 CPU를 포화시키므로 `cpu-batch`이고, 알아서 도는 색인기는 `background-crawler`입니다. **같은 종류의 프로그램도 어떻게 실행되느냐에 따라 archetype이 다릅니다.**

## 6.5 structural-special 가족

### game-task-chain — 게임 하나

유일하게 **구조 자체가 파라미터인** 항목입니다. 다른 항목은 task 하나의 프로그램을 적는데, 이 항목은 task 약 300개가 서로를 깨우는 모양을 적습니다.

```text
   사슬 16개:  첫 task:  반복: TIMER(frame_period) → RUN → WAKE(다음)
               중간 task: 반복: WAIT(앞 task) → RUN → WAKE(다음)
               끝 task:   반복: WAIT(앞 task) → RUN

   나머지 284개: 반복: SLEEP(약 0.5 s) → RUN(약 200 us)
```

frame 하나를 만드는 일이 16개 task를 차례로 지나갑니다. 1권에서 본 **chain**을 그대로 옮긴 모양입니다. 나머지 284개는 거의 아무것도 하지 않습니다.

**흉내 내는 것:** Proton으로 도는 게임입니다. 이름은 전부 `game.exe`입니다.

**출처:** LAVD라는 게임용 scheduler를 소개한 2024년 발표입니다. 이 권은 발표 슬라이드를 직접 열어 이 항목의 숫자를 하나씩 대조했습니다.

> **확인함.** 2026-09-13에 발표 슬라이드 PDF(static.sched.com/hosted_files/ossna2024/9b/scx-lavd-oss-na24.pdf, 30장)를 받아 텍스트를 뽑고, 그림 속 글자는 이미지로 따로 확인했습니다. 아래 인용은 슬라이드의 글머리표 문장 그대로입니다. 슬라이드 번호가 출처 등록부의 locator `s12`, `s13` 같은 것에 해당합니다.

슬라이드 12, "Task scheduling and CPU utilization"입니다.

> "Around 300 tasks are scheduled while running a game.
> ○ Around 90% are long-living tasks; only 10% of tasks are terminated.
> ● Top 30-40 most frequently scheduled tasks take 95% of scheduling.
> ○ Around half of them are system tasks -- especially, wine, graphics, and audio servers , taking 30--40% of scheduling.
> ○ There are 15-20 game-specific tasks, which takes 60-70% scheduling.
> ● CPU utilization is moderately high -- around 65-95%, but not overloaded (i.e., no 100%)."

게임을 하는 동안 약 300개의 task가 scheduling된다. 약 90퍼센트가 오래 사는 task이고 10퍼센트만 끝난다. 가장 자주 scheduling되는 상위 30에서 40개가 전체 scheduling의 95퍼센트를 차지한다. 그중 절반쯤이 시스템 task, 특히 wine과 그래픽과 소리 서버이고 scheduling의 30에서 40퍼센트를 차지한다. 게임 자체의 task는 15에서 20개이고 60에서 70퍼센트를 차지한다. CPU 사용률은 65에서 95퍼센트로 꽤 높지만 넘치지는 않는다.

슬라이드 13, "Task execution time per schedule"입니다.

> "In general, tasks run for very short duration – roughly a few 100s usec on average to a few msec maximum.
> ● Task execution time is very stable and is predictable using its average.
> ○ Some coordination tasks run very shortly (e.g., wineserver:260 usec) but some work tasks (e.g., a task worker: 1.65 msec) run longer than average."

task는 대체로 아주 짧게 돈다. 평균 수백 마이크로초에서 최대 몇 밀리초. 실행 시간은 매우 안정적이라 평균으로 예측할 수 있다. 조율 task는 아주 짧고(wineserver 260마이크로초), 일하는 task는 평균보다 길다(task worker 1.65밀리초).

슬라이드 14, "What makes scheduling happen?"입니다.

> "Preemption (e.g., timer interrupt) takes only 25-30% of scheduling.
> ● 70-75% of scheduling is initiated by waiting system calls – such as epoll, pipe_read, futex_wait , etc."

preemption은 scheduling의 25에서 30퍼센트뿐이다. 70에서 75퍼센트는 **기다리는 system call이 일으킨다.**

슬라이드 16의 제목은 "Tasks are tightly linked in a graph"이고, 17은 요약입니다.

> "A sequence of tasks serves for a single job (e.g., from a user input to display update).
> ● Therefore, the accumulated scheduling delay in a task chain will affect end-user's experience; it would eventually result in a sudden spike of frame time (low 1% FPS)."

여러 task가 순서대로 하나의 일을 한다. 사용자 입력에서 화면 갱신까지. 그래서 task 사슬에 쌓인 scheduling 지연이 사용자 경험에 영향을 주고, 결국 frame 시간이 갑자기 튀는 것으로 나타난다.

이제 항목의 파라미터와 원문을 나란히 놓습니다.

| 파라미터 | 값 | 출처 표시 | 원문 |
|---|---|---|---|
| `n_tasks` | 300 | `s12` | "Around 300 tasks" — 있음 |
| `frac_long_lived` | 0.90 | `s12` | "Around 90% are long-living tasks" — 있음 |
| `per_schedule_run` | 260–1,650 us 사이 로그 정규 | `s13` | wineserver 260 usec, task worker 1.65 msec — 있음 |
| `frac_wakeups_from_wait` | 0.70–0.75 균등 | `s14` | "70-75% of scheduling is initiated by waiting system calls" — 있음 |
| `chain_length` | 16 | locator 없음 | "15-20 game-specific tasks" — 범위만 있음. 16은 그 안에서 고른 값 |
| `frame_period` | 16,667 us | locator 없음 | **없음** |
| `tail_idle_gap` | 중앙값 500,000 us | `s12` | 없음. 메모가 "우리 임시값"이라고 밝힘 |
| `tail_run` | 중앙값 200 us | `s12` | 없음. 위와 같음 |

### 표에서 드러나는 것 네 가지

**하나. frame 주기 16.7밀리초가 원문에 없습니다.**

> **확인함.** 슬라이드 30장의 텍스트와 그림 속 글자 어디에도 16.7, 16.67, 60fps, frame budget이 나오지 않습니다. 시간 예산으로 나오는 숫자는 슬라이드 27의 "targeted latency (e.g., 15 msec)" 하나이고, 그건 frame 주기가 아니라 "모든 실행 가능한 task를 적어도 한 번씩 돌리려는 시간 창"입니다. 슬라이드 6의 예시 게임은 평균 41.3 FPS로 돌고 있어서 60 FPS도 아닙니다.
>
> 짝으로 인용하도록 되어 있는 LWN 보도 기사(`corbet-lwn24`, lwn.net/Articles/991205)와, 인용 문서가 나중에 검토할 후보로 적어둔 LWN 기사(lwn.net/Articles/1051430)도 같은 날 열어봤는데 16.7이라는 숫자는 없었습니다.
>
> 출처 등록부의 LAVD 항목은 "16.7 ms frame budget, 15 ms targeted latency"라고 적고, 초기 조사 문서도 같은 표현을 씁니다. 지금까지 확인한 세 자료에서는 앞의 절반을 찾지 못했습니다. 16,667은 1초를 60으로 나눈 값이라 초당 60 frame이라는 흔한 가정의 산수로 보이지만, **그 가정이 어디서 왔는지는 확인이 필요합니다.** 무엇을 열어보면 되는지: 출처 등록부에 그 문장을 처음 적은 조사 과정이 참고한 자료, 또는 LAVD 소스 코드 저장소입니다. 이 권은 둘 다 찾지 못했습니다.

**둘. 쓰이지 않는 파라미터가 둘 있습니다.**

> **확인 필요.** `frac_long_lived`(0.90)와 `frac_wakeups_from_wait`(0.70–0.75)는 원문과 정확히 맞는 값인데, **compile 단계가 이 두 값을 읽지 않습니다.** compile 코드의 사슬 생성 함수는 `n_tasks`, `chain_length`, `frame_period`, `per_schedule_run`, `tail_idle_gap`, `tail_run`만 뽑습니다. 그러니 이 두 숫자는 파일에 적혀 있고 출처도 맞지만 어떤 workload에도 들어가지 않습니다.
>
> 실제로 만들어지는 300개 task는 전부 파일이 끝날 때까지 살고(끝나는 task 10퍼센트가 없음), 사슬의 첫 task는 TIMER로, 나머지 사슬 15개는 WAIT로 깨고, 사슬 밖의 284개는 전부 SLEEP으로 깹니다(비율이 16 대 284로 정해짐). 선언된 파라미터가 **흉내에 반영되지 않은 원문의 관찰**로 남아 있는 것인지, compile 단계에 빠진 기능인지 확인이 필요합니다.

**셋. 사슬 모양은 원문의 그림과 다릅니다.**

슬라이드 16의 그림은 "waiter-waker 상위 50퍼센트의 task 그래프"입니다. 그림을 보면 **하나의 긴 사슬이 아닙니다.** 게임 본체와 `wineserver`가 서로 주고받는 작은 고리, 여러 작업 thread가 그래픽 제출 thread 하나로 모이는 모양, 소리 서버끼리의 고리가 **따로따로** 있습니다.

이 항목은 그걸 16단계짜리 한 줄로 폈습니다. 메모가 이 결정을 밝힙니다.

> "the linearization of the s16-s17 waker-waiter graph into a chain, and every field name, are ours."

슬라이드 16과 17의 깨우는 쪽·기다리는 쪽 그래프를 한 줄 사슬로 편 것과 모든 필드 이름은 우리 것이다.

한 줄로 편 근거는 슬라이드 17의 "사용자 입력에서 화면 갱신까지 여러 task가 순서대로 하나의 일을 한다"는 문장입니다. 그래프의 실제 모양보다 **그 문장이 말하는 성질**, 즉 앞 단계의 지연이 뒤로 쌓인다는 성질을 가져온 것입니다.

**넷. 나머지 284개의 값은 임시입니다.**

> "tail param values are our placeholder encoding of near-idle, provisional like any meas-pending value."

나머지 task의 값은 "거의 쉬는 상태"를 표현하려고 우리가 넣은 **임시값**이고, 측정 대기 중인 값처럼 잠정적이다.

그런데 이 두 파라미터의 출처 표시는 `lavd-ossna24:s12`입니다. 슬라이드 12가 뒷받침하는 것은 "상위 30에서 40개가 scheduling의 95퍼센트"라는 **집중도**이고, 거기서 "나머지는 거의 쉰다"를 읽어낼 수는 있습니다. 하지만 0.5초와 200마이크로초라는 값은 슬라이드에 없습니다. **출처 표시는 등급이 둘째인 것처럼 보이지만, 실제 값은 넷째 등급입니다.** 메모가 그 사실을 적고 있어서 숨겨진 것은 아닙니다. 다만 출처 표시만 읽는 도구나 사람에게는 보이지 않습니다.

### 실행 한 번의 길이를 분포로 만드는 법

`per_schedule_run`은 두 끝값으로 적힌 로그 정규 분포입니다. 원문이 준 것은 "wineserver 260마이크로초"와 "task worker 1.65밀리초"라는 **두 예**뿐입니다. 메모가 이걸 분포로 만든 방법을 적습니다.

> "anchors are the source's wineserver ~260 us and worker ~1.65 ms endpoints, lognormal family by OQ-5 convention (the compiler derives median/sigma treating the anchors as the p05/p95 span)."

두 끝값을 **5퍼센트 지점과 95퍼센트 지점**으로 보고 중앙값과 흩어짐을 역산한다. 로그 정규 분포에서 두 지점이 주어지면 이렇게 계산됩니다.

```text
   중앙값 = √(260 × 1,650) = √429,000 ≈ 655 us

   95퍼센트 지점은 중앙값에서 표준 정규의 1.645 걸음 위
   sigma_log = ln(1,650 / 655) / 1.645
             = ln(2.519) / 1.645
             ≈ 0.924 / 1.645
             ≈ 0.562
```

**"두 예를 5퍼센트와 95퍼센트로 본다"는 것은 넷째 등급의 해석입니다.** 원문은 wineserver가 짧은 편의 예이고 task worker가 긴 편의 예라고 했지, 그 둘이 분포의 어느 지점인지는 말하지 않았습니다. 1퍼센트와 99퍼센트로 봤다면 흩어짐이 더 좁아졌을 것입니다.

> **코드로.** 이 역산은 `dataset/tools/wlc/sampling.py`의 `anchored_lognormal_params` 함수에 있습니다. 실제로 `c1-gaming` 파일을 compile하면 사슬 16개의 실행 길이가 218마이크로초에서 1,094마이크로초 사이로 뽑힙니다. 이 값들이 CPU 한 자리에 맞춰 늘어나는 과정은 다음 권에서 봅니다.

> **이 연구에서는.** 이 항목에는 판정할 기준이 없습니다. 이유가 다른 항목들과 다릅니다.
>
> > "validation against LAVD would be circular — LAVD is also the parameter source (stated as such, building-plan §7)."
>
> LAVD와 비교해서 검증하면 **순환**이 된다. LAVD가 파라미터의 출처이기도 하기 때문이다. 문제를 낸 사람의 답안지로 채점하는 꼴이라는 뜻입니다. 이 이야기는 근거가 약한 자리를 모은 장에서 다시 봅니다.

## 6.6 meas 가족

마지막 셋은 **부류 자체를 우리 측정에서 끌어낸** 항목입니다. 셋 다 `category_source: meas`이고, 숫자도 전부 측정에서 왔습니다. 측정의 자세한 과정은 뒤의 측정 장에서 보고, 여기서는 무엇을 흉내 내는지와 핵심 숫자만 봅니다.

### network-bulk — 회선을 꽉 채우는 다운로드

```text
   반복: WAIT(net 중앙값 16.7 ms) → RUN(chunk_cpu 중앙값 1 ms)   … total_work까지
   → EXIT
```

네트워크에서 한 조각을 받고, 조금 계산하고, 다음 조각을 기다립니다. CPU를 쓰는 비율이 약 5.6퍼센트입니다.

**흉내 내는 것:** 게임 플랫폼의 다운로드(`steam`), 메일 보내기(`thunderbird`)입니다.

> **이 연구에서는.** 메모가 이 항목의 약점을 스스로 적습니다. CI 서버에서 커널 소스 묶음을 받는 동안의 CPU 비율을 쟀는데, 다섯 번 중 **두 번만** 측정할 수 있을 만큼 오래 걸렸고, 두 값이 0.013과 0.1로 크게 흩어졌습니다. 그리고 한 문장이 붙습니다.
>
> > "Structural claim only — the runner link is datacenter-class; the duty ratio, not the throughput, is the grounded quantity."
>
> 구조에 대한 주장일 뿐이다. 측정 서버의 회선은 데이터센터급이라, 근거가 있는 것은 **비율**이지 전송 속도가 아니다. 집의 회선이라면 전송 속도도, 조각 사이의 대기도 전혀 다를 것입니다.

### electron-comms — 대부분 쉬다가 가끔 깨는 앱

```text
   반복: TIMER(heartbeat 중앙값 1.85 s) → RUN(heartbeat_work 중앙값 289 us)
```

거의 쉬다가 약 2초마다 잠깐 깨어납니다. 메시지가 왔는지 확인하는 등의 짧은 일입니다.

**흉내 내는 것:** 브라우저의 탭 프로세스(`chrome`), 채팅 앱(`discord`), 게임 플랫폼의 화면 프로세스(`steam`, `steamwebhelper`), 화상 회의의 보조 프로세스(`zoom`)입니다.

이름이 **Electron**에서 왔습니다. Electron은 웹 기술로 데스크톱 앱을 만드는 틀이고, Discord나 Slack 같은 앱이 이것으로 만들어졌습니다. 속을 들여다보면 브라우저 엔진이 돌고 있어서, 브라우저의 탭 프로세스와 비슷하게 행동할 것이라는 가정이 있었습니다. 그 가정이 측정으로 판정된 과정은 다음다음 장에서 봅니다.

> **이 연구에서는.** 측정 대상이 실제 채팅 앱이 아닙니다. Discord나 Slack은 계정이 있어야 돌아가서, 공개 CI 서버에서 돌릴 수 없습니다. 그래서 오픈 소스 채팅 앱 **Element**를 로그인하지 않은 채로 띄워놓고 쟀습니다. 메모가 이걸 대체라고 밝히고, 한계도 적습니다. **로그인하지 않았으니 메시지가 오가면서 생기는 깨어남이 없다.**
>
> 그리고 한 가지 더. 실제 앱의 깨어남은 정확한 주기가 아닌데, 이 항목은 TIMER로 적었습니다. 메모가 이것도 "밝혀둔 단순화"라고 적습니다.

### system-daemon — 거의 쉬는 시스템 서비스

```text
   반복: SLEEP(idle_gap 중앙값 11.2 s) → RUN(wake_burst 중앙값 155 us)
```

평균적으로 수십 초에 한 번 깨어나 0.2밀리초도 안 되게 일합니다. 이 archetype이 주기가 없는 것이 성격이라서 일부러 SLEEP으로 적었다는 것은 primitive를 볼 때 봤습니다.

**흉내 내는 것:** 사람이 없는 상황의 시스템 프로세스 다섯(`gnome-shell`, `Xorg`, `pipewire`, `systemd`, `dbus-daemon`), 그리고 게임 옆의 `wineserver`입니다.

흩어짐 `sigma_log: 1.9`가 매우 큽니다. 그래서 어떤 task는 잠드는 간격이 수백 초로 뽑혀서 60초짜리 파일 안에서 한 번도 깨어나지 않습니다. 계산해보면 이렇습니다.

```text
   간격이 60초를 넘을 확률
   = z가 ln(60 / 11.24) / 1.9 보다 클 확률
   = z가 1.675 / 1.9 ≈ 0.882 보다 클 확률
   ≈ 18.9퍼센트
```

다섯에 하나꼴로 파일 안에서 **한 번도 안 깹니다.** 실제로 `c1-gaming` 파일의 `wineserver`는 잠드는 간격이 1,225초로 뽑혔습니다.

> **이 연구에서는.** `wineserver`를 이 항목에 묶은 것은 **잠정적인 근사**라고 메모가 밝힙니다.
>
> > "wineserver -> system-daemon is a provisional approximation — LAVD treats wine as part of the game's task graph (lavd-ossna24:s12); whether wineserver joins the constructed game-task-chain instead is decided at constructor implementation, and this note is superseded by that decision."
>
> LAVD는 wine을 게임의 task 그래프 일부로 본다. 그러니 `wineserver`가 게임 사슬 안으로 들어가야 할지는 사슬 생성기를 구현할 때 정한다.
>
> 원문 슬라이드 13이 wineserver를 "아주 짧게 도는 조율 task, 260마이크로초"로 콕 집어 말하고, 슬라이드 16의 그림에서 게임 본체와 계속 주고받는 고리에 있습니다. 그런 task가 이 연구의 게임 파일에서는 한 번도 안 깨는 daemon으로 흉내 내지고 있습니다.

> **미정.** `wineserver`를 어디에 둘지는 아직 정해지지 않았습니다. 메모는 "사슬 생성기를 구현할 때 정한다"고 했는데, 사슬 생성기는 이미 compile 코드에 구현되어 있고 `wineserver`는 여전히 사슬 밖에 있습니다. 선택지는 셋입니다.
>
> **하나, 지금대로 둔다.** 장점은 게임 사슬의 구조가 단순하게 유지된다는 것입니다. 단점은 원문이 명시적으로 게임 그래프의 일부로 본 task를 가장 한가한 archetype으로 흉내 낸다는 것이고, 60초 파일에서 이 이름이 부하에 거의 기여하지 않습니다.
>
> **둘, 사슬 16개 중 하나로 넣는다.** 장점은 원문과 맞는다는 것입니다. 단점은 사슬 task의 이름이 전부 `game.exe`로 붙는 지금 구조에서 한 단계만 다른 이름을 붙이는 방법이 새로 필요하다는 것이고, 게임 파일들의 compile 결과가 바뀝니다.
>
> **셋, 짧은 주기로 게임과 주고받는 별도 항목을 만든다.** 장점은 wineserver 260마이크로초라는 원문의 값을 직접 쓸 수 있다는 것입니다. 단점은 archetype이 열셋이 되고, 새 항목의 주기와 흩어짐에 근거가 또 필요하다는 것입니다.
>
> 누가 정하나: 게임 사슬은 workload 데이터셋의 영역이고 데이터셋을 맡은 사람이 정할 수 있습니다. 다만 compile 결과가 바뀌면 게임이 들어간 파일들로 잰 숫자를 다시 내야 하므로, 측정을 돌리기 전에 정하는 편이 비용이 작습니다.

---

## 6장 정리

- archetype은 열두 개이고 다섯 가족으로 묶입니다. 주기적이거나 사람과 주고받는 셋, 계산 위주 셋, 입출력 위주 둘, 구조가 특별한 하나, 그리고 측정에서 부류를 끌어낸 셋입니다.
- 음악 재생과 영상 재생은 interbench 모형의 값을 그대로 씁니다. 화상 회의는 영상 재생에 묶여 있는데, 압축과 네트워크 부분의 파라미터를 지어내는 대신 밝혀둔 근사로 둔 것입니다.
- 사람이 만지는 창은 사람이 앞에 있는 상황의 주인공을 전부 맡고, 한 항목에 네 등급의 숫자가 다 섞여 있습니다. 판정할 기준이 없고, 대신 반증할 도구를 공개합니다.
- 끝날 때까지 계산만 하는 작업은 interbench의 Burn에서 부류를 가져왔지만 thread 4개 구조는 가져오지 않았습니다. 핵심 쌍의 색인기를 여기 묶은 것은 의도입니다.
- 연속 입출력은 interbench의 Write와 Read에서 부류를, 우리 측정에서 CPU 비율을 가져왔습니다. 캐시를 비운 측정값을 고른 것은 출처가 캐시 효과를 피하는 부하를 정의했기 때문입니다.
- 뒤에서 천천히 훑는 색인기는 ananicy 카탈로그의 배경 입출력 분류에서 왔습니다. 직접 실행한 검사는 속도를 늦추지 않아서, 속도 조절 모양은 daemon 모드 측정에서만 얻을 수 있었습니다. 지금 데이터셋에서는 이 항목을 쓰는 파일이 없습니다.
- 게임 항목을 LAVD 발표 원문과 대조하면 300개, 90퍼센트, 260마이크로초와 1.65밀리초, 70에서 75퍼센트가 원문에 있습니다. frame 주기 16.7밀리초는 원문에 없습니다.
- 게임 항목의 두 비율 파라미터는 원문과 맞지만 compile 단계가 읽지 않습니다. 사슬 모양은 원문 그림의 여러 고리를 한 줄로 편 우리 해석이고, 나머지 284개의 값은 슬라이드 표시가 붙은 우리 임시값입니다.
- 두 예시값을 분포의 5퍼센트와 95퍼센트 지점으로 보고 중앙값 약 655마이크로초, 흩어짐 약 0.562를 역산했습니다. 그 해석은 넷째 등급입니다.
- 측정에서 부류를 끌어낸 셋은 다운로드, 가끔 깨는 앱, 시스템 daemon입니다. 다운로드는 비율만 근거가 있고, 앱은 로그인하지 않은 대체 앱으로 쟀고, daemon은 흩어짐이 커서 다섯에 하나꼴로 60초 안에 한 번도 깨지 않습니다.
- 게임 옆의 wineserver는 원문에서 게임 그래프의 일부인데 지금은 daemon으로 흉내 내집니다. 어디에 둘지는 정해지지 않았습니다.

---

# 7장 · 존재의 근거: 수확

## 7.1 왜 이 열둘인가

열두 개의 목록을 보고 나면 5권에서 어휘를 보고 나왔던 질문이 똑같이 나옵니다. **누가 이걸 정했나요? 왜 열하나도 열셋도 아닌가요?**

답이 "우리가 앉아서 데스크톱에서 도는 프로그램들을 떠올려봤더니 이 정도로 나뉘었다"라면 곤란합니다. 이유는 5권에서 본 것과 같습니다. 행동의 부류를 우리가 정하고, 그 부류로 workload를 만들고, 그 workload로 실험하면 **자기가 낸 문제를 자기가 푸는 모양**이 됩니다.

그리고 이 목록에는 질문이 **둘** 걸려 있습니다. 성격이 다른 두 질문입니다.

```text
   질문 1   이 열두 부류가 각각 실제로 존재하나?
            "음악 재생 같은 주기 작업"이라는 부류가
            우리 머릿속에만 있는 건 아닌가?

   질문 2   이 열둘이면 충분한가?
            데스크톱에서 도는 것을 흉내 내는 데
            빠진 부류는 없나?
```

계획 문서는 두 질문에 **서로 다른 방법으로** 답합니다. 첫째 질문은 인용으로 닫고, 둘째 질문은 검증으로만 닫는다는 것입니다. 계획 문서는 이 둘을 Tier 1과 Tier 2라고 부릅니다. 학술 문헌이냐 배포된 소프트웨어냐를 가르는 인용의 **등급**과는 다른 말이라서, 이 책에서는 "존재의 근거"와 "충분함의 근거"로 풀어 쓰겠습니다.

이 장은 첫째 질문을 봅니다.

## 7.2 수확이라는 방법

계획 문서의 문장입니다.

> "**Tier 1 — existence of each archetype: closed by harvesting.** The inventory was harvested from sources that had already defined their own behavior categories: interbench's interactive and load menus, LAVD's gaming task-chain characterization, the kernel-build literature's compile fork-burst, and **`ananicy-rules`' `type` field — literally a community-maintained archetype taxonomy** (`Heavy_CPU`, `Game`, `Player`, `BG_CPUIO`, …). Each entry carries a `category_source:` naming the taxonomy it was harvested from — machine-checkable by the linter."

각 archetype의 존재는 **수확으로** 닫는다. 목록은 **이미 자기 나름의 행동 분류를 정의해둔 출처들**에서 거둬들였다. interbench의 대화형 작업 목록과 부하 목록, LAVD의 게임 task 사슬 분석, 컴파일을 다룬 문헌의 fork 폭발, 그리고 ananicy 규칙의 `type` 필드다. 마지막 것은 **말 그대로 커뮤니티가 관리하는 archetype 분류 체계**다. 각 항목은 자기가 어느 분류 체계에서 수확됐는지를 `category_source`에 적는다.

**수확**이라는 말을 골라 쓴 이유가 있습니다. 발명하지 않았다는 것입니다. 밭에서 거둔 곡식처럼, 누군가 이미 키워둔 것을 거둬왔다는 뜻입니다.

웹 개발에 빗대면 HTTP 상태 코드를 새로 설계하지 않고 표준 목록에서 쓰는 것과 같습니다. 우리 서비스에 "요청이 너무 많음" 상태가 필요할 때 `429`를 쓰면, 그 상태가 존재한다는 근거를 따로 댈 필요가 없습니다. 이미 합의된 목록에 있으니까요.

## 7.3 거둬온 곳 넷

### 첫째 밭: interbench의 두 목록

interbench 설명서에는 목록이 둘 있습니다. "어떤 대화형 작업을 흉내 내나"와 "어떤 부하를 흉내 내나"입니다. 둘째 목록의 제목과 항목을 옮깁니다.

> "What loads are simulated?
> None: Otherwise idle system.
> Video: The video simulation thread is also used as a background load.
> X: The X simulation thread is used as a load.
> Burn: A configurable number of threads fully cpu bound (4 by default).
> Write: A streaming write to disk repeatedly of a file the size of physical ram.
> Read: Repeatedly reading a file from disk the size of physical ram (to avoid any caching effects).
> Compile: Simulating a heavy 'make -j4' compilation by running Burn, Write and Read concurrently.
> Memload: Simulating heavy memory and swap pressure by repeatedly accessing 110% of available ram and moving it around and freeing it."

아무것도 없음, 영상, 화면(X), CPU 태우기, 디스크 쓰기, 디스크 읽기, 컴파일, 메모리 압박. 목록 끝에는 `hackbench 50`을 반복해서 돌리는 Hack 부하와, 사용자가 직접 정하는 Custom이 더 있습니다.

두 목록을 archetype과 맞대면 이렇게 됩니다.

| interbench 항목 | 어느 목록 | archetype |
|---|---|---|
| Audio | 대화형 작업 | `audio-playback` |
| Video | 대화형 작업, 부하 | `video-playback` |
| X | 대화형 작업, 부하 | `desktop-interactive` |
| Burn | 부하 | `cpu-batch` |
| Write, Read | 부하 | `io-stream` |
| Compile | 부하 | (보조 근거) `compiler-child` |
| Gaming | 대화형 작업 | **수확하지 않음** |
| None | 부하 | (기준선) |
| Memload | 부하 | **수확하지 않음** |
| Hack | 부하 | **수확하지 않음** |
| Custom | 대화형 작업, 부하 | 해당 없음. 사용자가 비율과 간격을 직접 정하는 칸 |

**수확하지 않은 셋이 흥미롭습니다.**

**Gaming은 버렸습니다.** 설명서의 문장을 보면 이유가 보입니다.

> "Gaming: The cpu usage behind gaming is not at all interactive, yet games clearly are intended for interactive usage. This load simply uses as much cpu as it can get. It does not return deadlines met as there are no deadlines with an unlocked frame rate in a game. This does not accurately emulate a 3d game which is gpu bound (limited purely by the graphics card), only a cpu bound one."

게임의 CPU 사용은 전혀 대화형이 아니지만 게임은 분명 대화형 용도다. 이 부하는 그냥 CPU를 가능한 한 많이 쓴다. frame 상한이 없는 게임에는 deadline이 없으므로 deadline 달성률을 보고하지 않는다. 그래픽 카드에 묶인 3D 게임을 정확히 흉내 내지 못하고, CPU에 묶인 게임만 흉내 낸다.

interbench 스스로 게임을 "CPU를 최대한 쓰는 것"으로 단순화했다고 밝힙니다. 그런데 이 연구에 필요한 게임은 **여러 task가 사슬로 이어져 frame마다 도는 것**이고, 그래서 게임 부류는 더 자세한 분석을 가진 다른 밭에서 거뒀습니다.

**Memload와 Hack은 범위 밖입니다.** 이 연구의 시뮬레이터는 CPU만 흉내 냅니다. 메모리 압박은 표현할 방법이 없습니다. Hack 부하가 쓰는 hackbench는 여러 task가 소켓으로 메시지를 주고받는 부하인데, 이 부류는 목록에 들어오지 않았습니다. 그 사정은 다음 장에서 봅니다.

> **확인함.** 2026-09-13에 interbench 원본 저장소(커밋 `e612a65c`)의 설명서 파일 `interbench.8`에서 "What loads are simulated?" 절 전체를 읽었습니다. 인용은 설명서의 조판 명령을 빼고 항목 이름과 문장만 옮겼습니다.

### 둘째 밭: LAVD의 게임 분석

게임 부류는 LAVD 발표가 게임 workload를 분석한 부분에서 거뒀습니다. 슬라이드 10의 문장이 그 분석의 목적을 밝힙니다.

> "If games have the common characteristics, which are differentiated from other general program domains (e.g., HPC, AI/ML, database), there are chance to come up with a game optimized scheduling policy."

게임이 다른 일반 프로그램 영역, 예를 들어 고성능 계산이나 머신러닝이나 데이터베이스와 구별되는 공통 특성을 갖고 있다면, 게임에 최적화된 scheduling 정책을 만들 기회가 있다.

**"다른 영역과 구별되는 공통 특성"**이 곧 부류의 정의입니다. 발표는 그 특성을 슬라이드 17에서 정리합니다. task가 안정적인 실행 시간과 안정적인 대기 시간을 가져서 대부분 주기적으로 행동하고, 여러 task가 사용자 입력에서 화면 갱신까지 한 줄로 일한다는 것입니다. 이 정리가 `game-task-chain`이라는 부류가 존재한다는 근거입니다.

### 셋째 밭: 컴파일 문헌

컴파일 부류는 두 논문에서 거뒀습니다. 파일의 `category_source`는 `ocallahan-atc17`입니다. 이 논문이 무엇을 말하는지는 컴파일 항목을 끝까지 따라가는 장에서 원문과 함께 봅니다. 여기서는 부류의 성격만 적습니다. **짧게 사는 자식 프로세스가 대량으로 쏟아진다**는 것이고, 그 성격이 다른 어떤 부류에도 없다는 것입니다.

같은 부류를 interbench도 따로 가지고 있습니다. 부하 목록의 Compile이 "무거운 `make -j4` 컴파일"을 흉내 낸다고 했습니다. 다만 interbench는 그걸 Burn과 Write와 Read를 동시에 돌리는 것으로 흉내 내서, **자식이 쏟아지는 모양**은 없습니다. 그래서 보조 근거로만 쓰입니다.

### 넷째 밭: ananicy 카탈로그의 type

마지막 밭이 가장 넓습니다. 2권에서 봤듯이 ananicy 카탈로그는 프로세스 이름마다 우선순위 분류를 붙여둔 커뮤니티 목록이고, 분류는 열다섯 개가 정의되어 있습니다. 2권이 분류 정의 파일 전체를 옮겼으니, 여기서는 archetype과 맞닿는 줄만 다시 가져옵니다.

```text
# Type: BackGround CPU/IO Load
# Background CPU/IO it's needed, but it must be as silent as possible
{ "type": "BG_CPUIO", "nice": 16, "ioclass": "idle", "sched": "idle" }

# Type: Heavy CPU Load
# It must work fast enough but must not create so much noise
{ "type": "Heavy_CPU", "nice": 9, "ioclass": "best-effort", "ionice": 7 }
```

`BG_CPUIO`는 `background-crawler`의 `category_source`이고, `Heavy_CPU`는 `cpu-batch`를 **교차 확인**합니다. interbench의 Burn이 1차 근거이고, 다른 밭에서도 같은 부류가 따로 발견된다는 뜻입니다.

> **이 연구에서는.** 인용 문서가 이 카탈로그에 대해 중요한 구분을 해둡니다. 같은 이름의 프로젝트가 두 갈래로 갈라져서 **분류 이름이 다르다**는 것입니다. 원래 Ananicy는 지금 소문자 분류(`game`, `compiler`)를 쓰고, 대문자 분류(`Heavy_CPU`, `BG_CPUIO`)는 "Depricated types"라는 제목 아래 주석으로 남겨뒀습니다. 대문자 분류는 CachyOS가 관리하는 카탈로그 쪽의 것입니다.
>
> 그래서 archetype의 `category_source`는 `ananicy`가 아니라 `ananicy-rules`입니다. 대문자 분류 이름을 인용하려면 그 갈래를 가리켜야 합니다.

## 7.4 이 밭에서 거둔 것은 무엇인가

넷째 밭에 대해서는 한 가지를 짚고 넘어가야 합니다. 계획 문서는 ananicy의 type 필드를 "**말 그대로** 커뮤니티가 관리하는 archetype 분류 체계"라고 부릅니다. 이 표현이 정확한지 원문으로 확인해볼 만합니다.

분류 정의 파일의 주석을 다시 읽어보면, 각 분류가 말하는 것은 **"이 프로그램을 어떻게 대우해야 하나"**입니다.

```text
   Game       "Use more CPU time if possible"
   BG_CPUIO   "it must be as silent as possible"
   Heavy_CPU  "It must work fast enough but must not create so much noise"
```

CPU를 더 줘라, 최대한 조용하게 해라, 충분히 빠르되 시끄럽지 않게 해라. **처방**입니다. 그리고 archetype이 적는 것은 **행동**입니다. 얼마나 자주 깨고 얼마나 계산하는가.

둘이 겹치는 자리가 있습니다. "배경에서 조용히 돌아야 하는 CPU·입출력 작업"이라는 처방은 "배경에서 CPU와 입출력을 쓰는 작업"이라는 행동 부류를 전제합니다. 그래서 처방의 분류에서 행동의 부류를 읽어내는 것이 가능합니다.

그런데 겹치지 않는 자리도 있습니다. 같은 커밋의 카탈로그에서 실제 항목 몇 개를 봅니다.

```text
   BG_CPUIO   baloo_file            (파일 색인기)
   BG_CPUIO   borg, rsync           (백업, 동기화)
   BG_CPUIO   wget, curl, aria2c    (다운로드)
   BG_CPUIO   transmission-daemon   (토렌트)
   BG_CPUIO   clamd                 (바이러스 검사 daemon)

   Chat       discord, element-desktop, slack
   Chat       zoom                  (화상 회의)
   Chat       thunderbird           (메일)
```

`BG_CPUIO` 한 분류 안에 **색인기와 백업과 다운로드**가 함께 있습니다. 이 연구의 archetype으로 치면 `background-crawler`, `io-stream`, `network-bulk` 셋에 걸칩니다. 행동이 전혀 다른데 처방이 같아서 한 분류입니다. `Chat`에는 채팅 앱과 화상 회의와 메일이 함께 있습니다.

> **확인함.** 2026-09-13에 카탈로그 커밋 `03ef03fb`에서 위의 항목들을 이름으로 찾아 확인했습니다. 다운로드 도구들은 `00-default/Networking/`, 채팅과 회의와 메일은 `00-default/Chats/chats.rules`, 백업 도구는 `00-default/Tools/rsync.rules`와 `00-default/System Utilities & Maintenance/borg.rules`에 있습니다.

**그러니 이 밭에서 거둔 것은 행동의 분류 체계라기보다 처방의 분류 체계이고, 거기서 행동 부류를 읽어낸 것은 우리의 해석입니다.** "말 그대로 archetype 분류 체계"는 조금 강한 표현입니다. 그 해석이 틀렸다는 뜻은 아닙니다. 다만 이 카탈로그를 인용할 때는 "배포된 소프트웨어가 이런 부류를 **처방의 단위로** 구분한다"까지가 원문이 뒷받침하는 문장입니다.

> **확인 필요.** 이 관찰에서 따라 나오는 질문이 하나 있습니다. 측정에서 부류를 끌어냈다고 표시된 세 항목 중 둘에 대해, 같은 카탈로그에 대응할 만한 분류가 있습니다. 채팅 앱을 흉내 내는 `electron-comms`에는 `Chat`이, 시스템 서비스를 흉내 내는 `system-daemon`에는 `Service`(`dbus-daemon`이 여기 들어 있음)가 있습니다. 다운로드를 흉내 내는 `network-bulk`의 대표 도구들은 `BG_CPUIO`에 들어 있습니다.
>
> 그런데 계획 문서는 이 셋에 대해 "문헌의 분류 체계가 없다"고 적고 `category_source: meas`를 붙였습니다. 반면 `background-crawler`는 같은 카탈로그의 `BG_CPUIO`를 근거로 수확된 것으로 표시되어 있습니다.
>
> 두 가지 읽기가 가능합니다. 하나, "문헌의 분류 체계"라는 말이 학술 문헌이나 벤치마크 목록을 뜻하고 ananicy는 한 항목에서만 예외로 쓰였다. 둘, `Chat`이나 `Service`는 처방이 같을 뿐 행동이 너무 달라서 부류의 근거로 쓸 수 없다고 판단했다. 둘째 읽기라면 그 판단은 `BG_CPUIO`에도 똑같이 적용되어야 합니다. `BG_CPUIO`도 행동이 다른 것들을 함께 담고 있기 때문입니다. 어느 쪽이었는지 적힌 기록을 저장소에서 찾지 못했습니다.

## 7.5 정직하게 "측정"이라고 적은 셋

그 질문과 별개로, 세 항목을 **어떻게 표시했는지**는 이 장에서 가장 본받을 만한 부분입니다. 계획 문서의 문장입니다.

> "Three entries (network-bulk, electron-comms, system-daemon) have no literature taxonomy; their `category_source` is honestly `meas` ("behavior class observed in our measurements")."

세 항목은 문헌의 분류 체계가 없다. 그래서 `category_source`를 **정직하게** `meas`로 적는다. "우리 측정에서 관찰한 행동 부류"라는 뜻이다.

**"정직하게"라는 단어가 문서에 적혀 있다**는 것이 중요합니다. 다른 선택지가 있었다는 뜻이기 때문입니다. 비슷해 보이는 밭에서 적당한 분류 하나를 가져다 붙일 수 있었습니다. 채팅 앱에 interbench의 무언가를, 다운로드에 비슷한 도구의 무언가를. 그랬다면 열두 항목이 전부 "수확됨"으로 보였을 것입니다.

그러지 않고 셋을 따로 표시했습니다. 그 결과 이 목록을 읽는 사람은 **어느 항목의 존재가 바깥 근거에 기대고 어느 항목이 우리 관찰에 기대는지**를 한눈에 알 수 있습니다.

```text
   바깥 분류 체계에서 수확한 아홉
   ─────────────────────────────
   audio-playback, video-playback, desktop-interactive  ← interbench
   cpu-batch, io-stream                                 ← interbench
   compiler-child, build-orchestrator                   ← 컴파일 문헌
   background-crawler                                   ← ananicy-rules
   game-task-chain                                      ← LAVD

   우리 측정에서 부류를 끌어낸 셋
   ─────────────────────────────
   network-bulk, electron-comms, system-daemon          ← meas
```

> **논문으로.** 이 구분이 논문에서 한 문장이 됩니다. "열두 archetype 중 아홉은 기존 벤치마크, scheduler 분석, 커뮤니티 카탈로그의 분류에서 수확했고, 셋은 해당하는 분류가 없어 우리 측정에서 부류를 정의했다."
>
> 이 문장이 막아주는 질문이 있습니다. 심사자가 "왜 채팅 앱이 따로 있나요, 그냥 배경 작업 아닌가요"라고 물으면, 그 부류는 **바깥 근거로 존재를 주장하지 않았다**고 답할 수 있습니다. 대신 측정이 그 부류의 행동을 보여줬다고 답합니다. 주장의 강도를 미리 낮춰뒀으니, 강도를 문제 삼는 질문이 성립하지 않습니다.

## 7.6 수확이 해주지 않는 것

수확은 강한 방법이지만 할 수 있는 일이 정해져 있습니다. 셋을 적어둡니다.

**하나, 수확은 값을 주지 않습니다.** 분류가 존재한다는 것과 그 분류의 숫자가 무엇인가는 다른 질문입니다. ananicy 카탈로그는 색인기라는 부류가 있다고 말하지만, 색인기가 몇 초마다 깨는지는 말하지 않습니다. `background-crawler`의 부류는 수확했고 값은 전부 측정했습니다.

**둘, 수확은 경계를 주지 않습니다.** interbench의 X와 Audio가 서로 다른 부류라는 것은 말해주지만, 실제 프로그램 하나가 어느 쪽에 드는지는 말해주지 않습니다. 파일 색인기가 `cpu-batch`일 때도 있고 `background-crawler`일 때도 있다는 것은 수확이 아니라 우리 판단입니다.

**셋, 수확은 충분함을 주지 않습니다.** 네 밭에서 거둔 부류를 전부 모아도, 그게 데스크톱에서 도는 모든 것을 덮는다는 보장은 없습니다. 네 밭이 전부 같은 곳을 비워뒀을 수 있습니다. **이게 다음 장의 질문입니다.**

## 7.7 손으로 따라가기: 부류 하나를 밭까지 따라가기

`cpu-batch`의 존재 근거를 끝까지 따라가 보겠습니다.

```text
   1  archetype 파일의 cpu-batch 항목
      category_source: interbench

   2  출처 등록부의 interbench 항목
      type: deployed-system
      locator_pattern: "^(man|src)-[a-z]+$"
      notes: "Background loads: Burn (4 CPU-bound threads) …"

   3  인용 문서의 interbench 항목
      cite: Kolivas, C. interbench. github.com/ckolivas/interbench,
            GPL-2.0, v0.31 (pin master commit).
      status: verified-in-vetting (2026-08-25); pin commit at submission

   4  interbench 설명서의 부하 목록
      "Burn: A configurable number of threads fully cpu bound
       (4 by default)."

   5  교차 확인: ananicy-rules의 분류 정의
      "Heavy_CPU" — "It must work fast enough but must not
       create so much noise"
      실제 항목: ffmpeg, blender, qemu-system-x86_64 등
```

5번까지 가면 우리가 만든 것이 하나도 없습니다. 벤치마크 도구 하나가 "CPU를 완전히 쓰는 부하"를 자기 목록에 올려뒀고, 전혀 다른 커뮤니티의 우선순위 카탈로그가 "무거운 CPU 작업"을 따로 분류해뒀습니다. **서로 모르는 두 곳이 같은 부류를 따로 세웠습니다.**

그리고 3번에 적힌 상태를 보면 할 일이 하나 남아 있습니다. "제출할 때 커밋을 고정한다". 이 권을 쓰면서 원본 저장소를 받아보니 가장 최근 커밋이 2016년 10월 24일의 `e612a65c`였고, 소스 코드의 판본 표시가 0.31이었습니다. 인용 문서가 적은 판본과 맞습니다.

> **이 연구에서는.** 1번에서 5번까지의 사슬 중 기계가 검사하는 것은 1번과 2번, 2번과 3번의 연결입니다. `category_source`의 값이 등록부에 있는지는 항목의 필드를 볼 때 봤듯이 지금은 검사하지 않고, 필드가 있는지만 검사합니다. 등록부의 id가 인용 문서에 있는지는 검사합니다. 3번과 4번의 연결, 즉 **인용 문서가 가리키는 자료에 정말 그 내용이 있는가**는 사람이 열어봐야 합니다. 이 권이 원문을 옮기는 이유가 그것입니다.

---

## 7장 정리

- 열두 개의 목록에는 질문이 둘 걸려 있습니다. 각 부류가 존재하는가, 그리고 열둘이면 충분한가입니다. 계획 문서는 앞의 것을 인용으로, 뒤의 것을 검증으로만 닫습니다.
- 존재의 근거는 수확입니다. 이미 자기 분류를 정의해둔 출처에서 부류를 거둬왔고, 항목마다 어디서 거뒀는지를 `category_source`에 적습니다.
- 거둬온 곳은 넷입니다. interbench의 대화형 작업과 부하 목록, LAVD의 게임 분석, 컴파일 문헌, ananicy 카탈로그의 분류입니다.
- interbench 목록에서 게임은 거두지 않았습니다. interbench 스스로 게임을 CPU를 최대한 쓰는 것으로 단순화했다고 밝히고 있어서, 사슬 구조를 가진 LAVD 분석에서 거뒀습니다. 메모리 압박과 메시지 부하는 CPU만 흉내 내는 시뮬레이터의 범위 밖입니다.
- ananicy 카탈로그의 분류는 행동이 아니라 처방입니다. 한 분류 안에 색인기와 백업과 다운로드가 함께 있습니다. 거기서 행동 부류를 읽어낸 것은 우리 해석이고, "말 그대로 archetype 분류 체계"는 강한 표현입니다.
- 같은 카탈로그에 채팅과 서비스 분류도 있는데, 그 둘에 대응하는 항목은 분류 체계가 없다고 표시되어 있습니다. 어떤 기준으로 한 분류는 쓰고 다른 분류는 쓰지 않았는지 기록이 없습니다.
- 세 항목은 정직하게 측정에서 부류를 끌어냈다고 표시했습니다. 그래서 어느 항목이 바깥 근거에 기대고 어느 항목이 우리 관찰에 기대는지 한눈에 보입니다.
- 수확은 부류의 존재만 줍니다. 값도, 실제 프로그램이 어느 부류에 드는지의 경계도, 목록이 충분하다는 보장도 주지 않습니다.
- 서로 모르는 두 곳이 같은 부류를 따로 세웠다면 그 부류의 존재는 강하게 뒷받침됩니다. 끝날 때까지 계산만 하는 작업이 그 예입니다.

---

# 8장 · 충분함의 근거: 검증

## 8.1 충분하다는 것은 인용할 수 없습니다

앞 장에서 열두 부류가 각각 존재한다는 근거를 봤습니다. 이제 둘째 질문입니다. **열둘이면 충분한가.**

이 질문에는 인용으로 답할 수 없습니다. 계획 문서가 그 이유를 한 문장으로 적습니다.

> "**Tier 2 — sufficiency of the set: closed by verification, not citation.** No universal taxonomy of process behavior exists, so completeness cannot be cited — and must not be claimed."

목록의 충분함은 **인용이 아니라 검증으로** 닫는다. 프로세스 행동의 보편적인 분류 체계는 존재하지 않으므로, 완전하다는 것은 인용할 수 없고, **주장해서도 안 된다.**

생각해보면 당연합니다. 어떤 논문이 "프로세스의 행동은 정확히 이 열두 가지로 나뉜다"고 말했다면 그걸 인용하면 됩니다. 그런 논문이 없습니다. interbench는 자기가 흉내 내고 싶은 몇 가지를 골랐을 뿐이고, LAVD는 게임만 봤고, ananicy 카탈로그는 우선순위를 줄 단위를 나눴을 뿐입니다. **네 밭을 전부 합쳐도 "이게 전부"라는 문장은 어느 밭에도 없습니다.**

그리고 "주장해서도 안 된다"는 구절이 붙어 있습니다. 논문에 "우리 archetype 목록은 데스크톱 행동을 완전히 덮는다"는 문장이 들어가면 안 된다는 뜻입니다.

## 8.2 대신 무엇을 주장하나

완전함을 주장할 수 없다면 무엇을 주장할까요. 계획 문서의 다음 문장입니다.

> "The claim is weaker and falsifiable: **this inventory spans S1–S18.** The referee is the `meas-ci` campaign: if a CI-runnable scenario's measured statistics cannot be reproduced by any composition of the inventory, the inventory is insufficient and an entry is added."

주장은 더 약하고, **반증할 수 있다.** 이 목록은 S1부터 S18까지를 덮는다. 심판은 우리 측정 캠페인이다. CI에서 돌릴 수 있는 상황의 측정 통계를 목록의 **어떤 조합으로도** 재현할 수 없으면, 목록이 부족한 것이고 항목을 더한다.

세 부분으로 나눠 보겠습니다.

### 무엇을 덮는가: S1부터 S18까지

**S1부터 S18까지**는 5권에서 본 **상황 목록**의 번호입니다. 데스크톱에서 사람들이 하는 일을 열여덟 줄로 정리한 것이고, 줄마다 그 상황에서 뜨는 프로세스 이름들과, 그 상황이 실제로 있다는 바깥 출처가 적혀 있습니다. 문서 작업이 S1, 웹 브라우징이 S2, 게임이 S9, 컴파일이 S11, 사람이 없을 때의 시스템 프로세스가 S18입니다.

주장은 "데스크톱의 모든 행동"이 아니라 **"이 열여덟 상황"**을 덮는다는 것입니다. 범위가 명시되어 있습니다. 그리고 그 열여덟 상황은 바깥 출처로 존재가 확인된 것들입니다.

### 무엇으로 덮는가: 조합

"덮는다"는 상황 하나에 archetype 하나가 대응한다는 뜻이 아닙니다. **여러 archetype을 섞어서** 그 상황을 만들 수 있다는 뜻입니다. 게임 상황은 게임 사슬 하나로 되지 않고, 소리 재생과 화면 합성과 게임 플랫폼의 화면 프로세스가 함께 있어야 합니다.

### 어떻게 반증되는가: 측정이 재현되지 않으면

심판은 측정입니다. 실제 프로그램을 CI 서버에서 돌려 통계를 재고, archetype의 조합으로 그 통계를 흉내 낼 수 있는지 봅니다. 안 되면 **목록이 부족하다는 증거**입니다.

그리고 규칙이 붙어 있습니다. **부족하면 항목을 더한다.** 목록을 지키려고 측정을 달리 해석하지 않는다는 뜻입니다.

웹 서비스로 치면 API 명세의 완전성과 비슷합니다. "우리 API가 모든 사용 사례를 지원한다"는 증명할 수 없습니다. 대신 "이 열여덟 개의 사용자 시나리오를 전부 이 API 호출의 조합으로 구현할 수 있다"는 확인할 수 있습니다. 시나리오 하나가 구현이 안 되면 API를 늘립니다.

## 8.3 열여덟 상황의 조합표

계획 문서는 "S1부터 S18까지가 전부 이 열두 개로 조합된다"고 적습니다. 계획 문서의 항목별 사용처와 실제 timeline 파일의 묶음을 합쳐서 표로 만들면 이렇습니다.

| 상황 | 무엇 | 쓰이는 archetype |
|---|---|---|
| S1 | 문서 작업 | `desktop-interactive` |
| S2 | 웹 브라우징 | `desktop-interactive`, `electron-comms` |
| S3 | 화상 회의 | `video-playback`, `audio-playback`, `electron-comms` |
| S4 | 메일과 비동기 소통 | `desktop-interactive`, `electron-comms`, `network-bulk` |
| S5 | 음성 채팅 곁들이기 | `electron-comms` |
| S6 | 사진 편집 | `desktop-interactive`, `cpu-batch` |
| S7 | 영상 편집과 렌더 | `desktop-interactive`, `cpu-batch` |
| S8 | 일괄 변환 | `cpu-batch`, `io-stream` |
| S9 | 게임 | `game-task-chain`, `audio-playback`, `video-playback`, `electron-comms`, `system-daemon` |
| S10 | 게임·콘텐츠 다운로드 | `network-bulk` |
| S11 | 편집과 컴파일 | `desktop-interactive`, `build-orchestrator`, `compiler-child` |
| S12 | 머신러닝 학습 | `cpu-batch` |
| S13 | 미디어 재생 | `audio-playback`, `video-playback` |
| S14 | 파일 색인 | `background-crawler`, `cpu-batch` |
| S15 | 백업과 동기화 | `io-stream` |
| S16 | 압축 | `io-stream` |
| S17 | 바이러스 검사 | `cpu-batch`, `background-crawler` |
| S18 | 시스템 기반 | `system-daemon` |

**열두 개가 전부 한 번 이상 쓰이고, 열여덟 줄이 전부 채워집니다.** 이게 "덮는다"의 첫 번째 확인입니다. 다만 이 표는 **"만들 수 있다"**를 보여줄 뿐 **"똑같이 행동한다"**를 보여주지는 않습니다. 그 둘째 확인이 측정입니다.

> **코드로.** 계획 문서의 각 항목 설명 끝에 "Consumed by:"로 시작하는 사용처 줄이 있고, 위 표의 대부분이 거기서 나옵니다. 몇 칸은 실제 timeline 파일의 묶음에서 채웠습니다. 예를 들어 S4의 `network-bulk`는 메일을 보내는 `thunderbird`가 그 archetype에 묶인 파일이 있어서 들어갔습니다.

### 창작 앱은 두 archetype의 교대입니다

S6과 S7이 흥미롭습니다. 사진 편집기와 영상 편집기는 archetype 하나로 흉내 내지 않고 **둘을 번갈아** 씁니다. 계획 문서의 문장입니다.

> "Creative apps (S6/S7) are time-shared compositions of `desktop-interactive` + `cpu-batch` — consistent with CpsMark+ Table 4's signature (`cpsmark-tbench23:table-4`)."

창작 앱은 사람이 만지는 창과 계산만 하는 작업을 **시간으로 나눠 섞은** 것이다. CpsMark+ 논문 Table 4의 특징과 일치한다.

사진 편집기를 쓰는 모습을 떠올리면 자연스럽습니다. 붓질을 하는 동안은 입력에 반응하는 창이고, 필터를 누르면 몇 초 동안 계산만 합니다. 두 성격이 시간 순서로 교대합니다.

> **확인 필요.** 이 문장이 인용하는 CpsMark+ Table 4를 이 권은 직접 읽지 못했습니다. 출판사 사이트(ScienceDirect)가 자동 접근을 막아서 2026-09-13에 원문을 받지 못했습니다. 인용 문서에는 이 논문이 2026-08-25에 전문 검토로 확인됐다고 적혀 있습니다.
>
> 저장소 문서가 적어둔 Table 4의 내용은 이렇습니다. 출처 등록부는 "per-workload hardware sensitivity (table-4: CC up to 1.77x GPU-sensitive, CA ~1.0x)"라고 적습니다. 작업마다 **하드웨어 민감도**, 즉 GPU나 CPU나 저장장치를 좋은 것으로 바꿨을 때 얼마나 빨라지는가를 적은 표이고, 계산 위주의 창작 작업은 GPU에 최대 1.77배 민감하고 문서 작업은 거의 민감하지 않다는 것입니다.
>
> 그 내용이 맞다면, Table 4가 뒷받침하는 것은 "창작 작업은 계산 자원을 많이 쓰는 성격이 섞여 있다"이지 **"사람의 입력과 계산이 시간으로 교대한다"**는 구조가 아닙니다. 하드웨어 민감도 표에서 시간 교대를 읽어내려면 해석이 한 단계 더 필요합니다. 계획 문서의 "일치한다(consistent with)"가 어느 정도의 뒷받침을 뜻하는지, 원문 Table 4를 열어 확인이 필요합니다. 무엇을 열면 되는지: DOI 10.1016/j.tbench.2023.100084의 Table 4와 그 표를 설명하는 본문 문단입니다.

## 8.4 심판이 실제로 판정한 사례

측정이 목록을 판정한 적이 실제로 한 번 있습니다. 규모는 작지만 이 절차가 어떻게 돌아가는지를 보여줍니다.

### 질문: 브라우저 탭은 채팅 앱과 같은 부류인가

브라우저 탭 프로세스를 어느 archetype에 묶을지가 열려 있었습니다. 후보는 채팅 앱을 흉내 내는 `electron-comms`였습니다. 채팅 앱이 속에 브라우저 엔진을 돌리니 행동이 비슷할 것이라는 추측이 있었습니다.

두 가지 길이 있었습니다. 미리 **나눠서** 브라우저 탭용 archetype을 따로 만드는 것, 아니면 **같다고 두고** 측정으로 판정하는 것입니다. 계획 문서의 결정입니다.

> "Do not pre-split; the Xvfb workflow compares chromium-renderer vs Electron-app CDFs and the comparison decides."

**미리 나누지 않는다.** 화면 없이 GUI 프로그램을 돌리는 측정에서 chromium의 탭 프로세스와 Electron 앱의 분포를 비교하고, **그 비교가 결정한다.**

이 결정이 목록을 지키는 쪽으로 기울어 있다는 점에 주목할 만합니다. 항목을 늘리려면 증거가 필요하고, 증거가 없으면 늘리지 않습니다. 앞 권에서 어휘에 이름을 더하는 기준이 같은 모양이었습니다.

### 측정 결과

같은 측정에서 두 쪽을 쟀습니다. 측정 요약 파일에 기록된 값입니다.

| | Element(채팅 앱 대체) | chromium 탭 프로세스 |
|---|---|---|
| 잰 프로세스 수 | 15 | 50 |
| 깨어남 간격 중앙값 | 1,848,645 us | 1,609,098 us |
| 깨어남 간격 `sigma_log` | 1.088 | 1.718 |
| 깨어난 한 번의 CPU 중앙값 | 289 us | 647 us |
| 깨어난 한 번의 CPU `sigma_log` | 0.713 | 0.94 |

그리고 판정이 archetype 메모에 이렇게 남았습니다.

> "OQ-3 referee result (same run): idle chromium renderers wake at median ~1.61 s sigma_log ~1.72 — close in median, heavier-tailed; no archetype split warranted, chromium renderers keep binding to this entry."

같은 실행에서 잰 판정 결과다. 한가한 chromium 탭 프로세스는 중앙값 약 1.61초, `sigma_log` 약 1.72로 깬다. **중앙값은 가깝고, 꼬리는 더 길다.** archetype을 나눌 근거는 없다. chromium 탭 프로세스는 계속 이 항목에 묶는다.

> **코드로.** 값은 `dataset/meas/summary.json`의 `across_repeats` 아래 `element`와 `chromium` 항목에 있습니다. 측정 원자료는 저장소의 GitHub release `meas-ci-2026-08-28`에 `meas-gui.zip`으로 올라가 있고, 분석 코드는 `dataset/tools/meas/analyze.py`입니다.

### 이 판정을 다시 보면

이 사례가 절차의 좋은 점과 빈 곳을 동시에 보여줍니다.

**좋은 점.** 미리 나누지 않고 측정에 맡겼고, 측정이 돌았고, 결과가 기록됐습니다. 추측이 증거로 바뀌었습니다.

**빈 곳.** 표를 다시 보면 두 쪽이 모든 칸에서 가깝지는 않습니다. 깨어남 간격의 중앙값은 1.85초와 1.61초로, 한쪽이 다른 쪽의 약 1.15배라 가깝습니다. 그런데 흩어짐은 1.09와 1.72로 크게 다르고, 깨어난 한 번의 CPU는 289와 647로 두 배가 넘게 다릅니다.

**"중앙값은 가깝다"와 "나눌 근거는 없다" 사이에 기준이 적혀 있지 않습니다.** 중앙값이 몇 퍼센트 안이면 같은 부류인가요. 흩어짐 차이는 왜 판정에 들어가지 않았나요. 깨어난 한 번의 CPU 차이는 판정에서 언급되지 않습니다.

> **미정.** 이 목록을 판정하는 측정 심판에 **"재현된다"의 기준**이 정해져 있지 않습니다. 브라우저 탭 사례에서 판정은 "중앙값이 가깝다"는 사람의 읽기로 내려졌습니다. 앞으로 archetype 조합이 측정을 재현하는지 볼 때도 같은 문제가 생깁니다.
>
> 선택지는 셋입니다.
>
> **하나, 분포 비교 통계의 문턱을 미리 정한다.** 두 분포의 모양 차이를 하나의 숫자로 재는 통계를 고르고, 그 숫자가 문턱 안이면 재현된다고 봅니다. 장점은 판정이 사람의 읽기에서 떨어진다는 것입니다. 단점은 문턱 자체에 근거가 필요하다는 것이고, 표본이 15개와 50개처럼 작으면 통계의 힘이 약합니다.
>
> **둘, 판정에 쓸 통계를 항목마다 미리 적는다.** 예를 들어 이 항목은 "깨어남 간격 중앙값만 본다"고 선언해두는 것입니다. 장점은 단순하고 지금의 `validation_stats` 필드와 맞는다는 것입니다. 단점은 선언하지 않은 통계의 차이, 이번 사례로 치면 CPU 두 배 차이를 구조적으로 무시하게 됩니다.
>
> **셋, 기준을 정하지 않고 판정마다 근거를 문장으로 남긴다.** 지금의 방식입니다. 장점은 유연하다는 것입니다. 단점은 결과를 본 뒤에 판정하게 되어, 4권에서 본 "결과를 보기 전에 기준을 못 박는다"는 원칙과 어긋납니다.
>
> 누가 정해야 하나: 기준을 어떻게 계산하는지는 harness의 몫이고, 무엇을 재현해야 하는지는 데이터셋의 몫입니다. 둘이 함께 정해야 합니다.

## 8.5 목록에 들어오지 않은 후보들

검증이 항목을 **더하는** 절차라면, 지금까지 **더하지 않은** 것들도 볼 만합니다. 저장소 문서에 archetype 후보로 이름이 올랐는데 목록에 없는 것이 있습니다.

근거 문서가 행동 파라미터의 출처를 나열한 표에서 두 도구에 대해 이렇게 적습니다.

> "schbench (Mason, 2016) | Wakeup-latency benchmark reporting tail percentiles (P99) | Precedent for our latency metrics (tail-focused, not mean); also the messaging/wakeup-heavy process archetype"

> "hackbench | Kernel-community load-balancing stressor (many communicating tasks) | The chat/IPC-heavy archetype's burst structure; recognizable stressor if we need a stress condition"

schbench는 지연 지표의 선례이면서 **메시지를 주고받고 자주 깨는 프로세스 archetype**의 근거이기도 하다. hackbench는 **채팅이나 프로세스 사이 통신이 많은 archetype**의 버스트 구조를 뒷받침한다.

초기 조사 문서도 hackbench에 대해 "Grounds many-task IPC burst archetype"이라고 적습니다. 여러 task가 통신하며 한꺼번에 몰리는 archetype의 근거라는 것입니다.

그런데 열두 개 목록에는 **메시지를 주고받는 archetype이 없습니다.** WAKE를 쓰는 항목은 게임 사슬 하나뿐이고, 채팅 앱은 대부분 쉬다가 혼자 깨는 `electron-comms`로 흉내 냅니다.

> **확인 필요.** schbench와 hackbench를 근거로 거론된 "메시지를 주고받는 archetype"이 목록에 들어오지 않은 이유가 저장소에서 찾아지지 않습니다. 계획 문서의 열린 질문 해결 목록에도, 결정 기록에도 이 후보를 넣지 않기로 했다는 문장이 없습니다.
>
> 가능한 설명은 둘입니다. 하나, 목록을 만들 때 이 부류가 필요한 상황이 S1부터 S18까지에 없다고 판단했다. 채팅 앱의 측정에서 통신이 몰리는 모양이 보이지 않았다는 사실이 여기에 들어맞습니다. 다만 그 측정은 로그인하지 않아 메시지가 오가지 않는 상태였습니다. 둘, 근거 문서가 초기 계획을 적은 것이고 목록을 확정할 때 이 줄이 갱신되지 않았다.
>
> 이 연구의 규칙대로라면 이 질문은 인용이 아니라 검증으로 답해야 합니다. 메시지가 실제로 오가는 채팅 앱의 통계를 목록의 조합으로 재현할 수 있는가. 그 측정은 계정이 필요한 앱을 CI에서 돌릴 수 없다는 한계 때문에 아직 없습니다.

## 8.6 검증이 닿지 않는 곳

마지막으로 이 방법의 범위를 정확히 적어둡니다. 계획 문서의 문장에 이미 조건이 있었습니다. "**CI에서 돌릴 수 있는** 상황의 측정 통계".

CI에서 돌릴 수 없는 상황이 있습니다.

```text
   CI에서 돌릴 수 있다                   CI에서 돌릴 수 없다
   ─────────────────                    ──────────────────
   make로 커널 빌드                      게임 (GPU, 계정, 창)
   파일 복사, 압축                        화상 회의 (카메라, 상대방, 계정)
   색인기 daemon 모드                    Discord·Slack (계정)
   바이러스 검사                          사람의 실제 입력
   다운로드 (데이터센터 회선)
   계정 없는 채팅 앱, 브라우저 탭
   기본 설치 daemon
```

오른쪽 열의 상황은 이 검증이 **판정할 수 없습니다.** 그리고 오른쪽 열에 이 연구에서 가장 중요한 상황들이 있습니다. 게임과 사람이 앞에 앉은 상황입니다. 그 archetype들의 판정란이 `none`인 것이 우연이 아닙니다.

그러니 "이 목록은 S1부터 S18까지를 덮는다"는 주장을 정확히 쓰면 이렇게 됩니다.

```text
   조합표 수준에서는 열여덟 상황을 전부 만들 수 있다.
   측정으로 재현을 확인할 수 있는 것은 그중 CI에서 돌릴 수 있는 상황뿐이다.
   게임, 화상 회의, 사람의 입력은 조합표 수준의 확인에 머문다.
```

> **미실행.** 그리고 CI에서 돌릴 수 있는 상황에 대해서도, 목록의 조합으로 측정 통계를 재현하는 시험은 아직 돌린 적이 없습니다. 지금까지 한 일은 측정에서 파라미터를 뽑은 것과, 브라우저 탭 하나를 판정한 것까지입니다. 계획 문서는 이 주장을 "측정 실패가 항목을 더하는 절차 아래에서 잠정적"이라고 적어둡니다.
>
> 이 시험을 돌리려면 세 가지가 먼저 있어야 합니다. 시뮬레이터가 archetype 조합을 돌려 trace를 내야 하고, 그 trace에서 측정과 같은 통계를 뽑는 도구가 있어야 하고, 앞 절에서 본 "재현된다"의 기준이 정해져야 합니다. 저장소 문서에 이 시험의 일정은 적혀 있지 않습니다.

> **논문으로.** 이 장의 내용이 논문에서 쓸 수 있는 문장의 경계를 정합니다.
>
> ```text
>    쓸 수 있는 문장
>    "The inventory composes all eighteen catalogued scenarios;
>     sufficiency is a falsifiable claim refereed by measurement
>     for the CI-runnable subset."
>
>    쓸 수 없는 문장
>    "The twelve archetypes cover desktop process behavior."
> ```
>
> 앞 문장은 범위가 있고 반증 절차가 있습니다. 뒤 문장은 계획 문서가 명시적으로 금지한 완전성 주장입니다.

## 8.7 손으로 따라가기: S11을 측정에 대보기

컴파일 상황 S11을 하나 골라서 "조합이 측정을 재현하는가"를 손으로 대보겠습니다. 실제로 시뮬레이터를 돌린 비교가 아니라, **archetype이 선언한 값과 측정 요약 파일의 값을 나란히 놓는 것**까지입니다.

### 조합

```text
   code  → desktop-interactive
   make  → build-orchestrator   (parallelism_cap 8)
   cc1   → compiler-child       (make의 spawn table에서 태어남)
```

### 재현해야 할 통계

두 항목이 선언한 통계입니다.

```text
   build-orchestrator:  fork rate,
                        concurrent-children time series vs make -jN run
   compiler-child:      child lifetime CDF,
                        concurrent-children time series
```

자식을 만드는 빈도, 동시에 살아 있는 자식 수의 시간 변화, 자식의 수명 분포입니다.

### 측정이 준 값

측정 요약 파일에서 커널 빌드를 `make -j8`로 다섯 번 돌린 결과의 중앙값입니다.

| 통계 | 측정값 |
|---|---|
| 한 빌드의 컴파일러 계열 자식 수 | 11,883 |
| 자식을 만드는 빈도 | 초당 24.2 |
| 동시에 살아 있는 컴파일러 계열 프로세스의 최대 | 16 |
| 자식 수명 중앙값 | 99,801 us |

### 나란히 놓기

**자식을 만드는 빈도.** archetype의 부모는 자식 하나당 `dispatch_overhead`만큼 계산하고 FORK합니다. 그 값의 중앙값 234마이크로초도 이 측정에서 왔습니다. 그런데 실제 빈도 초당 24.2는 부모의 계산이 아니라 **자리가 나는 속도**, 즉 자식이 끝나는 속도가 정합니다. 그러니 이 통계는 시뮬레이션을 돌려봐야 비교할 수 있습니다. 여기서는 대볼 수 없습니다.

**동시에 사는 수.** 여기서 눈에 띄는 것이 있습니다. archetype은 동시에 도는 자식을 8개로 막습니다. 측정에서는 동시에 살아 있는 컴파일러 계열 프로세스가 **최대 16개**였습니다.

왜 두 배일까요. 측정 도구가 "컴파일러 계열"로 센 이름들을 보면 답이 보입니다.

```text
   cc1, cc1plus, gcc, g++, as, ld, collect2,
   objtool, fixdep, objcopy, genksyms, modpost
```

`gcc`는 컴파일러 **드라이버**이고, 실제 컴파일은 그 자식인 `cc1`이 합니다. `make -j8`의 작업 8개가 각각 `gcc`와 `cc1`을 동시에 띄우면 16개가 됩니다. `make`가 세는 "작업" 하나가 프로세스 둘 이상이라는 뜻입니다.

archetype은 작업 하나를 자식 하나로 흉내 냅니다. 그러면 동시에 사는 수의 시간 변화는 **최대 8**이 되고, 측정의 **최대 16**과 다릅니다.

> **확인 필요.** 이 차이가 archetype 목록이 부족하다는 증거인지, 비교하는 쪽의 단위가 다른 것인지 확인이 필요합니다.
>
> 사실은 이렇습니다. 측정 분석 코드(`dataset/tools/meas/analyze.py`)는 위의 열두 이름을 전부 "컴파일러 계열"로 묶어서 수명, CPU, 동시 수를 셉니다. 그러니 측정의 자식 11,883개에는 `cc1`만이 아니라 드라이버와 어셈블러와 링커와 커널 빌드 보조 도구가 섞여 있습니다. archetype의 메모는 이 값을 "~11.9k compiler-family children per build"로 옮기고, 자식 하나의 CPU와 수명을 그 계열 전체의 평균에서 끌어냅니다. 그리고 동시 실행 상한은 8입니다.
>
> 두 가지 읽기가 가능합니다. 하나, archetype의 "자식 하나"는 계열 프로세스 하나다. 그렇다면 상한 8은 `make -j8`의 8과 뜻이 달라져서, 측정과 비교하려면 상한을 16 근처로 두어야 합니다. 둘, archetype의 "자식 하나"는 `make`의 작업 하나다. 그렇다면 상한 8이 맞고, 대신 자식 하나의 CPU와 수명을 작업 단위로 다시 모아야 합니다. 지금 파일은 CPU와 수명은 첫째 읽기로, 상한은 둘째 읽기로 적혀 있습니다.
>
> 무엇을 열어보면 되는지: 측정 원자료(`meas-cli3.zip`)의 프로세스 생성 기록에서 `gcc`와 `cc1`의 부모 자식 관계를 따라가 작업 단위로 다시 세면 됩니다. 이 권은 그 재집계를 하지 않았습니다.

**수명.** 자식의 수명 중앙값은 측정에서 99,801마이크로초, 약 0.1초입니다. archetype의 자식은 수명을 직접 적지 않고 계산, 디스크 대기, 계산의 합으로 만듭니다. 세 중앙값을 더하면 12,900 + 3,600 + 1,440 = 17,940마이크로초로 측정 수명 중앙값의 약 5분의 1입니다. 다만 로그 정규 세 개를 더한 합의 분포는 세 중앙값의 합과 같지 않고, 무엇보다 **벽시계 수명은 scheduling의 결과**입니다. CPU를 기다린 시간이 수명에 들어갑니다. 이 비교도 시뮬레이션을 돌려야 의미가 있습니다. 이 파라미터들이 어떻게 만들어졌는지는 컴파일러 항목을 끝까지 따라가는 장에서 봅니다.

**이 연습에서 가져갈 것.** 조합표로는 S11이 덮입니다. 측정과 나란히 놓으면 **동시에 사는 수의 단위**라는, 조합표에서는 보이지 않던 질문이 나옵니다. 검증이 인용보다 강한 이유가 이것입니다. 실제 숫자를 맞대야 드러나는 차이가 있습니다.

---

## 8장 정리

- 목록이 충분하다는 것은 인용할 수 없습니다. 프로세스 행동의 보편적인 분류 체계가 없어서, 완전하다는 주장은 인용도 못 하고 해서도 안 됩니다.
- 대신 약하고 반증 가능한 주장을 합니다. 이 목록의 조합으로 상황 목록 S1부터 S18까지를 만들 수 있고, 측정한 통계를 어떤 조합으로도 재현하지 못하면 항목을 더한다는 것입니다.
- 조합표 수준에서는 열여덟 상황이 전부 채워지고 열두 항목이 전부 쓰입니다. 창작 앱은 사람이 만지는 창과 계산 작업의 시간 교대로 흉내 냅니다.
- 창작 앱 조합의 근거로 인용된 CpsMark+ Table 4는 저장소 기록상 하드웨어 민감도 표이고, 시간 교대 구조를 직접 말하는지는 원문으로 확인해야 합니다.
- 측정 심판이 실제로 판정한 사례가 하나 있습니다. 브라우저 탭을 채팅 앱과 같은 항목에 둘지를 측정으로 정했고, 중앙값이 가깝다는 이유로 나누지 않았습니다.
- 그 판정에는 기준이 적혀 있지 않았습니다. 흩어짐과 깨어난 한 번의 CPU는 크게 달랐습니다. "재현된다"의 기준을 정하는 일이 남아 있습니다.
- 메시지를 주고받는 archetype이 근거 문서에 후보로 거론됐지만 목록에 없고, 넣지 않은 이유의 기록을 찾지 못했습니다.
- 검증은 CI에서 돌릴 수 있는 상황에만 닿습니다. 게임, 화상 회의, 사람의 입력은 조합표 수준의 확인에 머뭅니다.
- CI에서 돌릴 수 있는 상황에 대해서도 조합이 측정을 재현하는지 보는 시험은 아직 돌린 적이 없습니다.
- 컴파일 상황을 측정과 나란히 놓으면 동시에 사는 프로세스 수가 archetype의 상한 8과 측정의 최대 16으로 다릅니다. 측정이 세는 단위와 archetype이 흉내 내는 단위가 다를 수 있다는 질문이 숫자를 맞대야 드러납니다.

---

# 9장 · 개수도 숫자다

## 9.1 "몇 개"에도 근거가 필요합니다

지금까지 본 숫자는 전부 **task 하나가 얼마나** 하는가였습니다. 얼마나 자주 깨고, 얼마나 계산하고, 얼마나 기다리는가. 그런데 workload를 만들려면 숫자가 하나 더 필요합니다. **몇 개가 떠 있는가.**

브라우저 탭 프로세스가 열두 개인지 스물다섯 개인지, `make`가 컴파일러를 백 개 부르는지 이천 개 부르는지, 게임 하나가 task를 몇 개 만드는지. 이 숫자도 결과를 바꿉니다. archetype의 숫자는 가상의 기계를 짓는 데 쓰이고, 떠 있는 task 수는 그 기계가 얼마나 붐비는지를 정합니다.

그래서 계획 문서는 개수에 한 절을 따로 들이고, 제목에 규칙을 박아뒀습니다.

> "Multiplicity (counts are numbers too — they obey the reference-only rule)"

**개수도 숫자다.** 그러니 숫자에 적용되는 규칙, 즉 근거를 가리켜야 한다는 규칙을 똑같이 따른다. 여기서 **multiplicity**는 같은 종류의 것이 몇 개 있는가, 우리말로 다중성을 뜻합니다.

그리고 첫 문장이 이렇습니다.

> "Counts never appear in the scenario catalog. Two kinds, handled differently:"

개수는 상황 목록에 절대 나오지 않는다. 두 종류가 있고, 다르게 다룬다.

5권에서 본 상황 목록 S1부터 S18까지에는 프로세스 **이름**만 있고 개수가 없습니다. S2 웹 브라우징 줄에는 "chrome (+ renderer/gpu children)"이라고만 적혀 있습니다. 몇 개인지는 다른 곳에서, 다른 근거로 정해집니다.

## 9.2 두 소비자에게 개수의 무게가 다릅니다

개수를 어떻게 다루는지 보기 전에, 개수가 **누구에게** 얼마나 중요한지를 먼저 봅니다. 계획 문서의 관찰입니다.

> "Observation: counts matter differently to the two consumers. The executor needs actual task counts to schedule; the recognizer sees only the post-fold annotation (`chrome (25 procs)`), so order-of-magnitude fidelity suffices for recognition experiments — precision matters only for executor-load realism, which `meas-ci` covers for the CI-runnable entries."

개수는 두 소비자에게 다르게 중요하다. executor는 scheduling하려면 실제 task 수가 필요하다. 인식기는 같은 이름을 하나로 접은 뒤의 표시(`chrome (25 procs)`)만 본다. 그러니 인식 실험에는 **자릿수만 맞으면** 충분하고, 정밀함은 executor에 거는 부하가 현실적인지에만 중요하다.

```text
                    chrome 12개 vs 25개의 차이가

   인식기에게        "chrome이 많이 떠 있다"는 같은 이야기
                    자릿수가 같으면 거의 같은 신호

   executor에게      CPU 한 자리를 두고 다투는 task가
                    두 배로 많다는 다른 이야기
```

5권에서 개수가 인식기에게 신호라는 것을 봤습니다. `chrome` 하나와 `chrome` 열셋은 다른 이야기였습니다. 그런데 **열셋과 스물다섯은 크게 다르지 않습니다.** 둘 다 "브라우저가 주인공이다"입니다. 인식기 쪽에서는 한 자리 수인가 두 자리 수인가 세 자리 수인가 정도가 중요합니다.

executor 쪽에서는 사정이 다릅니다. 깨어나는 task가 두 배면 경쟁이 두 배입니다. 여기서는 정확한 수가 결과를 바꿉니다.

**그러니 개수의 근거는 executor를 위해 필요합니다.** 이 구분이 뒤에서 두 종류의 개수를 다루는 방식에 그대로 반영됩니다.

## 9.3 첫째 종류: 창발적 다중성

### 개수를 적지 않고 부모를 적는다

컴파일러 자식이 첫째 종류의 대표입니다. 계획 문서의 문장입니다.

> "**Emergent (dynamic) multiplicity** — cc1 is the exemplar. Its count emerges from the orchestrator's behavior (fork rate, parallelism cap, child lifetime): specify the *orchestrator's* parameters (sourced), and the count time-series falls out of simulation. This preserves churn, which the Q7 material-change test and canonicalization fold need as raw material."

**창발적**(동적) 다중성. `cc1`이 대표 예다. 그 개수는 **부모의 행동에서 저절로 나온다.** 자식을 만드는 빈도, 동시 실행 상한, 자식의 수명이 정한다. 그러니 **부모의** 파라미터를 근거와 함께 적고, 개수의 시간 변화는 시뮬레이션에서 떨어져 나오게 한다. 이렇게 하면 프로세스가 태어나고 죽는 **들고남**이 보존된다.

**창발적**이라는 말은 규칙으로 직접 적지 않았는데 다른 규칙들이 돌아가면서 저절로 생긴다는 뜻입니다. 교통 체증이 좋은 예입니다. "여기에 차 백 대가 서 있다"를 누가 정하지 않았는데, 차들의 속도와 차선 수와 신호 주기가 체증을 만듭니다.

컴파일로 옮기면 이렇습니다.

```text
   적지 않는 것:   "cc1이 8개 살아 있다"

   적는 것:        make는 자식을 100개 만든다      (spawn_count)
                  동시에 8개까지만 돌린다          (parallelism_cap)
                  자식 하나는 이만큼 계산하고 끝난다  (compiler-child의 분포)

   저절로 나오는 것: 어느 순간 cc1이 몇 개 살아 있나
```

### 왜 이렇게까지 하나

"동시에 8개"라고 그냥 적으면 되지 않나요. 두 가지 이유가 있습니다.

**첫째, 개수가 scheduling의 결과이기 때문입니다.** 좋은 설정에서는 자식들이 빨리 끝나서 자리가 금방 나고 다음 자식이 태어납니다. 나쁜 설정에서는 자식이 CPU를 못 받아 오래 살고, 다음 자식은 자리가 날 때까지 기다립니다. **개수의 시간 변화가 설정에 따라 달라집니다.** 실행 계약 문서가 이 원칙을 FORK의 뜻으로 적어뒀습니다.

> "*Which* children exist and *what they do* is compile-time; *when* each arrives is emergent."

**어떤** 자식이 있고 **무엇을** 하는지는 compile 때 정해지고, 각 자식이 **언제** 태어나는지는 창발적이다.

주기 작업을 SLEEP으로 적으면 나쁜 설정 아래에서 요구량이 저절로 줄어든다는 문제와 같은 모양입니다. 태어나는 시각을 파일에 박으면, 나쁜 설정 아래에서도 자식들이 좋은 설정과 같은 속도로 쏟아집니다. 나쁜 설정이 받아야 할 벌이 사라집니다.

**둘째, 들고남 자체가 인식 쪽의 재료이기 때문입니다.** 5권에서 봤듯이 인식기는 이름 집합이 **바뀔 때만** 질문을 받습니다. 컴파일러 자식이 태어나고 죽는 들고남이 있어야 "이름 집합이 바뀌었는가"를 판정하는 규칙과, 같은 이름을 하나로 접는 규칙이 실제로 시험됩니다. 계획 문서의 문장 끝부분이 그 이야기입니다.

### 부모의 파라미터는 어디서 왔나

그러면 "부모의 파라미터를 근거와 함께 적는다"의 근거는 무엇일까요.

**만드는 자식 수.** 파일의 메모가 기본값을 적습니다.

> "spawn_count binds per timeline — the kernel-build default is 2,430 (ocallahan-atc17 sec-4.3)."

자식 수는 timeline마다 채운다. 커널 빌드의 기본값은 2,430이다. 이 숫자의 원문과, 원문이 말하는 빌드가 무엇인지는 컴파일러 항목을 끝까지 따라가는 다음다음 장에서 봅니다.

**동시 실행 상한.** 메모의 문장입니다.

> "parallelism_cap defaults to -j8 by stated convention (archetype-plan OQ-4: between interbench's documented -j4 and desktop nproc conventions), overridable at binding time; on one lane it shapes fork-storm width and queue depth, not throughput."

동시 실행 상한은 **밝혀둔 관례로** `-j8`을 기본으로 한다. interbench 설명서의 `-j4`와 데스크톱에서 흔한 "코어 수만큼"이라는 관례 사이의 값이다. 쓰는 쪽이 바꿀 수 있다. CPU 자리가 하나뿐인 기계에서 이 값은 **처리량이 아니라** 한꺼번에 쏟아지는 폭과 줄의 길이를 정한다.

마지막 구절이 중요합니다. CPU가 하나면 8개를 동시에 띄워도 한 번에 하나만 돕니다. 전체 빌드가 빨라지지 않습니다. 달라지는 것은 **실행 가능한 task가 한순간에 몇 개 줄을 서 있는가**입니다. scheduler에게는 그게 부담의 크기입니다.

`-j8`은 넷째 등급입니다. "-j4와 코어 수 사이"라는 이유가 적혀 있지만, 그 사이의 어느 값이든 같은 이유가 성립합니다.

### 손으로 따라가기: 백 개의 자식이 쏟아지는 모양

`c1-compile` 파일에서 `make`가 무엇을 요청하는지 봅니다. timeline에 적힌 binding입니다.

```yaml
- {id: build, name: make, archetype: build-orchestrator, arrive: 2s,
   bind: {spawn_count: 100, parallelism_cap: 8, child_name: cc1}}
```

2초에 나타나고, `cc1`이라는 이름의 자식을 100개 만들고, 동시에 8개까지만 둡니다.

compile 단계를 거친 뒤 `make`의 프로그램 앞부분은 이렇게 됩니다.

```text
   RUN(105 us)  → FORK      자식 1
   RUN(653 us)  → FORK      자식 2
   RUN(156 us)  → FORK      자식 3
   RUN(304 us)  → FORK      자식 4
   RUN(290 us)  → FORK      자식 5
   RUN(337 us)  → FORK      자식 6
   RUN(312 us)  → FORK      자식 7
   RUN(290 us)  → FORK      자식 8
   RUN(279 us)  → FORK      자식 9   ← 이미 8개가 살아 있으면 자리가 날 때까지 멈춘다
   …
   (100번째 FORK까지)
   WAIT(children)            자식이 전부 끝나기를 기다린다
   EXIT
```

`RUN` 값들은 `dispatch_overhead` 분포(중앙값 234마이크로초)에서 뽑혔습니다. 그리고 spawn table의 첫 다섯 자식은 이렇습니다.

```text
   자식 1:  RUN(664)     → SLEEP(3,126)  → RUN(9)      → EXIT
   자식 2:  RUN(28,042)  → SLEEP(13,339) → RUN(1,281)  → EXIT
   자식 3:  RUN(75,939)  → SLEEP(7,206)  → RUN(2,730)  → EXIT
   자식 4:  RUN(3,029)   → SLEEP(3,007)  → RUN(7,844)  → EXIT
   자식 5:  RUN(113,228) → SLEEP(8,981)  → RUN(81)     → EXIT
                                                    (단위: 마이크로초)
```

**이 파일에 적힌 개수는 100 하나뿐입니다.** "어느 순간 몇 개가 살아 있나"는 어디에도 적혀 있지 않습니다.

그 수가 어떻게 변할지 **요청만 보고** 짐작해보면 이렇습니다. 처음 1밀리초 남짓 동안 부모가 거의 쉬지 않고 8개를 내보냅니다. 그다음부터는 누군가 끝나야 다음이 태어납니다. 자식 1은 계산이 664마이크로초뿐이라 금방 끝날 것이고, 자식 5는 113밀리초를 계산해야 해서 오래 자리를 차지할 것입니다. **얼마나 오래 차지하는지는 scheduler가 CPU를 어떻게 나눠주느냐에 달려 있습니다.**

그래서 여기서 멈춥니다. 실제로 몇 초에 몇 개가 살아 있는지는 시뮬레이터가 이 프로그램을 돌려야 나오고, 자리가 나는 순간을 어떻게 처리하는지는 시뮬레이터를 다루는 권의 몫입니다.

> **이 연구에서는.** 파일마다 자식 수가 다릅니다. `c1-compile`은 100개, 편집기와 게임과 빌드가 겹치는 파일은 85개, 하루 작업의 흐름을 담은 파일은 4,200개입니다. 기본값 2,430을 그대로 쓰는 파일은 없습니다.
>
> 자식 수는 archetype이 아니라 timeline이 정하므로, 각 파일이 왜 그 수를 골랐는지는 파일을 다루는 권의 몫입니다. 여기서 짚을 것은 **기본값의 근거와 실제로 쓰인 값이 다를 수 있다**는 사실입니다. 기본값은 출처를 가리키고, 실제 값은 그 파일이 CPU 한 자리에서 원하는 부하 범위에 들어가도록 고른 설계입니다.

## 9.4 둘째 종류: 정적 다중성

### 개수를 직접 적는다

둘째 종류는 브라우저 탭 프로세스가 대표입니다.

> "**Static multiplicity** — chrome renderers, discord helpers. Binding-time parameters with a source tag: renderer counts from the tab-count literature (`dubroy-chi10`, `mozilla-testpilot10`, `chang-chi21` — defined against the Chromium process model) plus `meas-ci` Xvfb `/proc` counts."

**정적** 다중성. chrome의 탭 프로세스, discord의 보조 프로세스가 여기 든다. binding 때 출처 표시와 함께 정하는 값이다. 탭 프로세스의 수는 **탭 개수를 조사한 문헌**에서, Chromium의 프로세스 구조를 기준으로 정하고, 우리 측정에서 화면 없이 띄운 브라우저의 프로세스 수를 더한다.

이쪽은 개수가 scheduling의 결과가 아닙니다. 사용자가 탭을 열어둔 만큼 프로세스가 떠 있고, 그 수는 CPU를 잘 받든 못 받든 같습니다. 그러니 **파일에 직접 적어도** 앞에서 본 문제가 생기지 않습니다.

실제 파일에서는 이렇게 적힙니다.

```yaml
- {id: renderers, name: chrome, archetype: electron-comms,
   arrive: 0s, depart: 60s, count: 12}
```

`count: 12`. 같은 이름, 같은 archetype의 task가 열두 개입니다. 여기에 사람이 만지는 창인 `chrome` 하나가 더해져서, 인식기는 `chrome × 13`을 봅니다.

### 탭 개수 문헌은 무엇을 말하나

인용된 탭 개수 문헌 셋을 원문으로 봅니다.

**Dubroy와 Balakrishnan의 2010년 CHI 논문**은 Firefox 사용자 21명의 사용 기록을 2주에서 3주 동안 모았습니다. 탭 개수에 대한 문장입니다.

> "Figure 3 shows the number of tabs open when a navigation action occurred. The most common number of tabs to have open is one, with a steady descent down to 9. There is a second peak at 16 tabs, but this was almost entirely due to just two of the participants, P14 and P20."

> "Participant 14 had by far the highest median number of tabs open with 17, while no other participant had a median higher than 6. Participant 20 had the highest number of tabs open at once, with 42."

페이지를 이동할 때 열려 있던 탭 수는 **하나가 가장 흔했고** 9개까지 꾸준히 줄었다. 16개에 두 번째 봉우리가 있었는데 거의 두 참가자 때문이었다. 한 참가자의 중앙값이 17로 가장 높았고, 나머지는 누구도 중앙값이 6을 넘지 않았다. 동시에 열린 탭이 가장 많았던 경우는 42개였다.

그리고 누구를 조사했는지가 같은 논문에 적혀 있습니다.

> "The study was advertised as "a research study exploring how people use web browsers", looking for participants who "use Mozilla Firefox for several hours a day, and often use multiple tabs or windows.""

"하루 몇 시간씩 Firefox를 쓰고 **탭이나 창을 여러 개 자주 쓰는**" 사람을 모집했다. 탭을 많이 쓰는 쪽으로 기운 표본입니다.

> **확인함.** 2026-09-13에 저자가 공개한 논문 PDF(dgp.toronto.edu/~ravin/papers/chi2010_tabbedbrowsing.pdf, 10쪽)에서 참가자 절과 탭 사용 결과 절을 읽었습니다. 출처 등록부가 적은 "per-user medians mostly 1-6, long right tail (max 42). Scope limits: N=21 recruited tab users"와 맞습니다.

**Mozilla Test Pilot 2010년 연구**는 Firefox 사용자 약 2만 7천 명의 일주일 기록입니다. 인용 문서는 이 연구의 집계를 분석한 글이 Slate의 기사라고 적습니다. 그 기사의 문장입니다.

> "About one-half of users kept an average of more than 2.38 tabs open, and one-quarter kept an average of at least 3.59 tabs open. Thanks to some particularly prolific tabbers (for reasons unfathomable, a participant once had 1,103 tabs open), the average of these averages is 3.2 tabs."

> "One-half of the participants maxed out at fewer than eight tabs, but one-quarter of users had 11 or more tabs open at least once during the study."

사용자의 절반은 평균 2.38개가 넘는 탭을 열어뒀고, 4분의 1은 평균 3.59개 이상이었다. 탭을 유난히 많이 여는 사람들 덕에(한 참가자는 1,103개를 연 적이 있다) 평균들의 평균은 3.2개다. 참가자의 절반은 최대치가 8개 미만이었지만, 4분의 1은 연구 기간 중 한 번이라도 11개 이상을 열었다.

> **확인함.** 2026-09-13에 Slate 기사(slate.com/human-interest/2010/12/a-new-data-set-from-firefox-reveals-our-browsing-habits.html)에서 위 문장들을 읽었습니다. 인용 문서가 적은 "mean ≈3.2 tabs, median weekly max <8, 25% of users ≥11"과 맞습니다.
>
> 한 가지를 적어둡니다. 출처 등록부의 이 항목은 "Only aggregate tables survive (mirror)"라고 적는데, 그 사본(GitHub의 `mozilla/testpilotweb`)에 있는 집계 데이터 안내 페이지를 같은 날 열어보니 **데이터 파일의 목록과 표의 열 설명**만 있고 위의 숫자들은 없었습니다. 숫자는 Slate 기사에 있습니다. 인용 문서가 기사를 분석의 출처로 따로 등록해둔 것(`singervine-slate10`)이 그래서 필요합니다.

**Chang 외의 2021년 CHI 논문**은 인용 문서에 따르면 탭이 부담스러워지는 문턱의 중앙값이 8개라고 보고한 조사입니다.

> **확인 필요.** 이 논문의 원문을 이 권은 읽지 못했습니다. 2026-09-13에 ACM Digital Library가 자동 접근을 막았고(HTTP 403), 공개된 다른 사본을 찾지 못했습니다. 출처 등록부는 "median tab-overwhelm threshold 8 tabs (IQR 5-12); ~8% of participants had >10 tabs open at a capped snapshot"이라고 적고, 인용 문서는 2026-08-26에 확인했다고 표시합니다. 원문 문장은 이 책에 옮기지 않았습니다.

### 문헌의 탭 수에서 프로세스 수로

세 문헌이 주는 것은 **탭의 수**입니다. 그런데 파일이 적는 것은 **프로세스의 수**입니다. 그 사이를 잇는 것이 계획 문서가 말하는 "Chromium의 프로세스 구조"입니다. 브라우저가 탭을 여러 프로세스로 나눠 띄운다는 전제 아래에서, 탭 수가 프로세스 수로 번역됩니다.

그리고 여기에 우리 측정이 하나 더해집니다. 화면 없는 환경에서 chromium에 파일 탭 10개를 열었더니 **프로세스가 최대 21에서 22개**였습니다. 탭 하나에 프로세스 하나로 딱 떨어지지 않는다는 뜻입니다.

> **확인 필요.** 계획 문서가 번역의 기준으로 드는 "Chromium의 프로세스 구조"를 설명하는 자료가 인용 문서에 등록되어 있지 않습니다. 탭 하나가 프로세스 몇 개가 되는지의 규칙은 Chromium 프로젝트의 설계 문서가 설명할 것이고, 그 규칙은 판본과 설정(사이트별 격리 여부 등)에 따라 달라집니다. 지금 저장소에서 그 번역의 근거로 쓸 수 있는 것은 우리 측정의 "탭 10개에 프로세스 21에서 22개" 하나입니다. 무엇을 열면 되는지: Chromium의 프로세스 모델 설계 문서를 판본과 함께 등록하는 것입니다.

### 손으로 따라가기: 열두 개는 어디서 왔나

`c1-browsing`의 `count: 12`를 문헌과 측정에 대보겠습니다.

```text
   Test Pilot (Slate)   평균 탭 수 3.2, 최대치 중앙값 8 미만, 4분의 1이 11 이상
   Dubroy               흔한 탭 수는 1, 대부분의 중앙값은 6 이하, 최대 42
   우리 측정             탭 10개에 프로세스 21에서 22개

   c1-browsing          사람이 만지는 창 chrome 1 + 탭 프로세스 chrome 12 = 13
```

**12라는 수를 끌어내는 산수는 어디에도 적혀 있지 않습니다.** 문헌의 평균 탭 수 3.2를 쓰면 프로세스가 열 개를 넘기 어렵고, 측정의 비율을 쓰면 탭 10개에 프로세스가 스무 개를 넘습니다. 12는 그 사이 어딘가입니다.

그런데 이 장 앞에서 본 관찰을 다시 떠올리면, 이게 이상한 일은 아닙니다. 인식기에게는 **자릿수**가 중요하고, 13은 3.2개 탭짜리 브라우저(프로세스 한 자리 수)와도 스무 개 넘는 브라우저와도 같은 두 자리 수입니다. 그리고 탭 프로세스 하나하나는 약 2초에 한 번 0.3밀리초쯤 깨는 한가한 task라서, 12개든 20개든 executor에 거는 부하가 CPU의 1퍼센트를 넘지 않습니다.

직접 계산해봅니다. `electron-comms`의 값으로 탭 프로세스 하나가 쓰는 CPU 비율을 중앙값끼리 나누면 이렇습니다.

```text
   289 us / 1,850,000 us ≈ 0.016퍼센트
   × 12개 ≈ 0.19퍼센트
   × 20개 ≈ 0.31퍼센트
```

**개수의 정밀함이 이 경우에는 결과를 거의 바꾸지 않습니다.** 계획 문서가 "자릿수만 맞으면 충분하다"고 말할 수 있는 이유가 산수로 보입니다.

> **이 연구에서는.** 파일마다 탭 프로세스 수가 다릅니다. 브라우징만 하는 파일은 12개, 문서 작업 중인 파일은 8개, 저녁의 흐름을 담은 파일은 10개입니다. 각 수를 고른 이유는 파일 쪽의 몫이고, 여기서 볼 것은 **그 수들이 문헌과 측정이 주는 범위 안에 있다**는 것까지입니다.

> **확인 필요.** 계획 문서는 정적 개수를 "출처 표시가 붙은 binding 파라미터(Binding-time parameters with a source tag)"라고 적습니다. 그런데 timeline 파일의 `count: 12`에는 출처 표시가 없습니다. 출처 표시를 적을 자리 자체가 timeline의 task 형식에 없습니다. archetype 쪽 메모가 "values bind against the Chromium process model from the tab-count literature … plus meas-ci Xvfb counts"라고 근거를 문장으로 적어둘 뿐입니다.
>
> 그러니 지금은 "모든 숫자에 출처 표시가 붙어 있는지 기계가 검사한다"는 약속이 개수에는 적용되지 않습니다. 계획 문서의 "출처 표시"가 archetype 메모의 문장을 뜻한 것인지, timeline에 출처를 적는 자리를 만들 계획이었는지 확인이 필요합니다.

## 9.5 예외 하나: archetype 안에 개수가 있는 항목

두 종류의 규칙을 보고 나면 한 항목이 눈에 걸립니다. 게임의 `game-task-chain`입니다.

```yaml
n_tasks:
  {dist: constant, value: 300, sampling: per-instance,
   source: "lavd-ossna24:s12"}
```

**archetype 안에 task 수 300이 값으로 들어 있습니다.** archetype의 경계를 정한 규칙은 개수가 archetype에 "구성상" 들어갈 수 없다고 했고, 파일 머리의 규칙은 "개수는 여기서 절대 값을 갖지 않는다"고 했습니다. 그런데 이 항목에서는 개수가 파라미터입니다.

계획 문서는 이 항목을 "구조 자체가 파라미터인 유일한 항목"이라고 부릅니다. 이 표현이 예외의 이유로 읽힙니다. 게임 하나가 만드는 300개의 task는 **서로 다른 프로세스 300개가 아니라 게임이라는 하나의 프로그램이 가진 내부 구조**라는 것입니다. 사슬 16개와 거의 쉬는 284개는 그 구조의 일부이고, 구조를 적으려면 개수를 적어야 합니다.

> **확인 필요.** 이 읽기가 의도인지 확인이 필요합니다. 두 규칙이 문자 그대로는 충돌합니다.
>
> 한쪽은 이렇습니다. 경계 규칙은 archetype에서 개수를 뺀다고 하고, 파일 머리의 규칙은 개수가 `binding_params`에 이름만 오고 값을 갖지 않는다고 합니다. `n_tasks`는 `binding_params`가 아니라 `params`에 값과 함께 들어 있습니다.
>
> 다른 쪽은 이렇습니다. 계획 문서의 목록이 이 항목을 "구조가 파라미터인 유일한 항목"으로 명시하고 "~300 tasks"를 그 구조의 일부로 적습니다.
>
> 이 차이가 결과를 만드는 자리가 있습니다. 인식기는 `game.exe × 300`을 봅니다. 이 300은 다른 개수들처럼 timeline에서 파일마다 정한 값이 아니라, **모든 게임 파일에서 똑같이** archetype이 정한 값입니다. 게임마다 task 수가 다르다는 사실을 흉내 내려면 이 값을 binding으로 옮겨야 합니다. 무엇을 열어보면 되는지: 경계 규칙을 적은 결정에서 "개수"가 프로세스의 개수만 뜻하는지, 한 프로그램 안의 task 수까지 뜻하는지를 적은 기록입니다. 저장소에서 찾지 못했습니다.

---

## 9장 정리

- 몇 개가 떠 있는가도 결과를 바꾸는 숫자이고, 그래서 근거를 가리켜야 한다는 규칙을 똑같이 따릅니다. 상황 목록에는 개수가 없습니다.
- 개수의 무게가 두 소비자에게 다릅니다. 인식기에게는 자릿수만 맞으면 충분하고, executor에게는 정확한 수가 부하를 정합니다.
- 첫째 종류는 창발적 다중성입니다. 컴파일러 자식의 수를 직접 적지 않고, 부모가 몇 개를 만들고 동시에 몇 개까지 두는지를 적습니다. 어느 순간 몇 개가 살아 있는지는 시뮬레이션에서 나옵니다.
- 창발적으로 두는 이유는 둘입니다. 그 개수가 scheduling의 결과라서 파일에 박으면 나쁜 설정의 벌이 사라지고, 태어나고 죽는 들고남이 인식 쪽 규칙들의 재료이기 때문입니다.
- 부모의 자식 수 기본값 2,430은 논문에서 왔고, 동시 실행 상한 8은 관례입니다. CPU가 하나인 기계에서 상한은 처리량이 아니라 한순간에 줄 선 task의 수를 정합니다.
- 둘째 종류는 정적 다중성입니다. 브라우저 탭 프로세스처럼 scheduling과 무관한 수는 파일에 직접 적습니다.
- 탭 개수 문헌을 원문으로 보면 흔한 탭 수는 하나이고, 평균은 3.2개이며, 4분의 1은 한 번이라도 11개 이상을 엽니다. 탭을 많이 쓰는 사람을 모집한 연구에서도 중앙값은 대부분 6 이하였습니다.
- 탭 수를 프로세스 수로 옮기는 Chromium의 구조는 등록된 출처가 없고, 우리 측정의 "탭 10개에 프로세스 21에서 22개"가 유일한 번역 근거입니다.
- 브라우징 파일의 12라는 수를 끌어내는 산수는 적혀 있지 않지만, 탭 프로세스가 워낙 한가해서 12개든 20개든 CPU 부하가 1퍼센트를 넘지 않습니다. 자릿수만 맞으면 된다는 말이 산수로 뒷받침됩니다.
- 게임 항목만 archetype 안에 task 수 300을 값으로 가집니다. 한 프로그램의 내부 구조로 읽으면 예외가 설명되지만, 경계 규칙과 문자 그대로는 충돌하고 그 읽기를 적은 기록이 없습니다.

---

# 10장 · 우리가 직접 잰 것

## 10.1 왜 직접 재야 했나

열두 항목 중 파라미터가 **전부 측정에서 온** 항목이 일곱입니다. 컴파일러 자식과 부모, 연속 입출력, 뒤에서 훑는 색인기, 다운로드, 가끔 깨는 앱, 시스템 daemon입니다. 왜 이렇게 많은 숫자를 직접 재야 했을까요.

**문헌에 없었기 때문입니다.** 초기 조사 문서가 이 빈자리를 적어둡니다.

> "Per-process burst/period numbers for office/web/creation remain undocumented"

사무, 웹, 창작 쪽의 프로세스 단위 버스트 길이와 주기는 **문서화되어 있지 않다.** 게임과 소리·영상 재생은 잘 덮여 있지만 나머지는 비어 있다는 것입니다.

그리고 그 빈자리가 우연이 아니라는 것이 근거 문서에 적혀 있습니다.

> "State it as a finding, not an apology: **no public trace of desktop process timelines with process names exists.**"

변명이 아니라 발견으로 적어라. **프로세스 이름이 붙은 데스크톱 프로세스 시간 기록은 공개된 것이 하나도 없다.**

같은 문서가 이유를 한 문장으로 적습니다.

> "The absence is structural: process names are exactly the field privacy review strips, and process names are exactly what this research is about."

그 부재는 구조적이다. 프로세스 이름은 **개인정보 검토가 정확히 지워버리는 필드**이고, 동시에 **이 연구가 정확히 다루는 대상**이다.

누군가의 컴퓨터에서 어떤 프로그램이 언제 떴는지를 기록하면 그 사람의 생활이 드러납니다. 그래서 그런 기록을 공개하는 연구는 이름을 지우거나 해시로 바꿉니다. 이 연구에 필요한 것이 바로 그 이름입니다. **기다려도 누가 공개해줄 자료가 아닙니다.**

## 10.2 무엇을 쟀나

그래서 이 연구는 측정 캠페인을 하나 만들었습니다. 이름이 **meas-ci**입니다. 데이터셋 구축 문서의 첫 문장입니다.

> "One campaign on public CI runners (GitHub Actions): workflow files released, anyone can re-run."

공개 CI 서버에서 도는 캠페인 하나. 작업 흐름 파일을 공개하고, **누구든 다시 돌릴 수 있다.**

**CI 서버**는 코드가 바뀔 때마다 자동으로 시험을 돌려주는 빌려 쓰는 기계입니다. 웹 서비스를 만들어봤다면 풀 리퀘스트마다 테스트가 도는 그 기계입니다. 이 연구는 그 기계에서 시험 대신 **실제 프로그램을 돌리고 그 프로그램이 어떻게 행동하는지를 기록**했습니다.

"누구든 다시 돌릴 수 있다"는 것이 이 방식을 고른 이유입니다. 연구자의 개인 컴퓨터에서 잰 값은 아무도 확인할 수 없습니다. 공개 CI 서버에서 공개된 작업 흐름으로 잰 값은, 심사자가 저장소를 복제해서 똑같이 돌려볼 수 있습니다.

### 세 가지 작업 흐름

측정은 세 갈래입니다. 구축 문서의 목록을 옮깁니다.

> "1. *Headless CLI measurements:* real `make -jN` build, `tar`/`xz`, `rsync`, `clamscan`, `updatedb` with two sidecars — a process-lifecycle event tracer (netlink proc events: exact fork/exec/exit timestamps) and a 1 s `/proc` state sampler → lifetime CDFs, fork rates, wakeup patterns. …
> 2. *GUI app-intrinsic measurements:* Electron apps / a browser under **Xvfb** — heartbeat periods, renderer-children counts, multiplicities. Open-source substitutes for account-gated apps, substitution stated. …
> 3. *Name verification:* install packages in distro containers, record actual `comm`/`cmdline` strings (soffice.bin vs soffice, updatedb.plocate, cc1 path) — scenario-catalog Note 4."

| 갈래 | 무엇을 돌리나 | 무엇을 얻나 |
|---|---|---|
| 명령줄 측정 | 실제 `make` 빌드, 압축, 복사, 바이러스 검사, 파일 목록 갱신 | 수명 분포, 자식을 만드는 빈도, 깨어나는 모양 |
| GUI 앱 측정 | 화면 없이 띄운 Electron 앱과 브라우저 | 주기적 깨어남, 탭 프로세스 수 |
| 이름 확인 | 배포판 컨테이너에 패키지를 깔고 실행 | 프로세스가 실제로 어떤 이름으로 뜨는가 |

첫 두 갈래가 archetype의 숫자를 줍니다. 셋째 갈래는 5권에서 본 이름들이 실제 이름인지 확인하는 것이라 이 권의 범위 밖입니다.

"화면 없이"는 **Xvfb**라는 가짜 화면 서버를 쓴다는 뜻입니다. CI 서버에는 모니터가 없어서, GUI 프로그램이 그릴 곳을 소프트웨어로 흉내 내줍니다.

### 옆에 붙인 두 기록기

프로그램을 돌리는 동안 **곁에서 기록하는 도구** 둘이 함께 돕니다. 이런 도구를 **sidecar**라고 부릅니다. 오토바이 옆에 붙은 수레처럼 본체 옆에 붙어 따라가는 것이라는 뜻입니다.

**하나는 프로세스의 탄생과 죽음을 기록합니다.** 운영체제가 알려주는 사건을 받아서, 어느 프로세스가 언제 태어나고 언제 다른 프로그램으로 바뀌고 언제 끝났는지를 정확한 시각으로 남깁니다. 컴파일러 자식의 수명이 여기서 나옵니다.

**다른 하나는 주기적으로 사진을 찍습니다.** 일정한 간격마다 모든 프로세스의 상태를 읽어서, CPU를 얼마나 썼는지와 스스로 CPU를 몇 번 놓았는지를 남깁니다. 깨어나는 빈도와 한 번의 계산량이 여기서 나옵니다.

> **확인 필요.** 구축 문서는 사진을 찍는 간격을 "1 s"로 적습니다. 실제 작업 흐름 파일(`.github/workflows/meas-cli.yml`, `meas-gui.yml`)을 열어보면 명령줄 측정은 0.5초, GUI 측정은 0.2초로 돌립니다. archetype 메모도 "the 500 ms sampler", "sampled at 200 ms"라고 적어 작업 흐름 파일과 맞습니다. 구축 문서의 문장이 초기 계획에서 갱신되지 않은 것으로 보이지만 확인이 필요합니다.

### 어떤 기계에서 쟀나

"기계에 따라 달라지는 값"을 말하려면 어떤 기계였는지를 알아야 합니다. 측정 원자료에 기계 사양 파일이 함께 들어 있습니다. 명령줄 측정의 세 번째 실행에서 기록된 값입니다.

```text
   코어 수      4
   CPU         AMD EPYC 9V74 80-Core Processor
   메모리       16 GB
   운영체제     Ubuntu 24.04.4 LTS
   커널         6.17.0-1022-azure
```

> **확인함.** 2026-09-13에 저장소의 GitHub release `meas-ci-2026-08-28`에서 `meas-cli3.zip`을 받아 반복 다섯 개의 `spec.json`을 열었습니다. 다섯 개 모두 코어 4개와 같은 CPU 모델을 적고 있고, 실행 번호 `GITHUB_RUN_NUMBER`가 3입니다. 출처 표시의 locator `meas-ci:cli:3`에서 3이 이 실행 번호입니다.

**코어가 4개**라는 사실이 뒤에서 여러 번 쓰입니다. 이 연구의 시뮬레이터는 CPU가 하나인 기계를 흉내 내는데, 측정은 코어 4개짜리 기계에서 했습니다. 그 차이를 어떻게 다루는지가 측정값을 파라미터로 옮길 때의 핵심 문제입니다.

### 다섯 번씩 돌렸습니다

각 측정은 **다섯 번** 돌렸습니다. 요약 파일은 다섯 번의 결과를 반복마다 따로 저장하고, 반복을 가로질러 **중앙값과 최솟값과 최댓값**을 적습니다. 예를 들어 `make -j8` 한 번에 생긴 컴파일러 계열 자식 수는 이렇게 적혀 있습니다.

```json
"compiler_children": {
  "n_repeats": 5,
  "median": 11883,
  "min": 11835,
  "max": 11914
}
```

다섯 번 중 가장 적었을 때 11,835개, 가장 많았을 때 11,914개입니다. **흩어짐이 1퍼센트도 안 됩니다.** 이 숫자는 믿을 만합니다.

같은 파일에서 다운로드 중 CPU 비율은 이렇습니다.

```json
"wget_proc_duty": {
  "n_repeats": 2,
  "median": 0.0565,
  "min": 0.013,
  "max": 0.1
}
```

다섯 번 중 **두 번만** 값이 있고, 두 값이 거의 여덟 배 차이입니다. 이 숫자는 조심해야 합니다. 그리고 요약 파일이 그 사실을 **감추지 않고 그대로 보여줍니다.**

## 10.3 측정이 말할 수 있는 것

측정이 무엇을 뒷받침할 수 있는지는 근거의 등급을 볼 때 짧게 봤습니다. 구축 문서가 그 경계를 "신뢰의 묶음"이라는 이름으로 적어둡니다.

> "CI measurements support **structural and shape claims about software behavior only** — fork structure, counts, lifetime shapes, periods, heartbeats, name strings. Machine-relative absolutes (CPU %, IO throughput, io-wait fractions) are recorded with the runner spec and rank as *convention informed by measurement*, never desktop truth. Each workflow runs N times; spread is reported. Framing: characterization of software behavior, never desktop-performance measurement."

CI 측정은 **소프트웨어 행동의 구조와 모양에 대한 주장만** 뒷받침한다. 기계에 따라 달라지는 절대값은 서버 사양과 함께 기록하고 **측정으로 보강한 관례**로 친다. 틀은 **소프트웨어 행동의 특성 기술**이지 데스크톱 성능 측정이 아니다.

마지막 구절이 이 캠페인의 정체를 정합니다. "우리 CI 서버에서 make가 얼마나 빨랐다"는 아무 의미가 없습니다. "make는 자식을 이런 모양으로 만들고, 자식들은 이런 모양의 수명 분포를 가진다"는 의미가 있습니다. **소프트웨어가 어떻게 생겼는가**를 재는 것이지 **기계가 얼마나 좋은가**를 재는 것이 아닙니다.

### 모양과 절대값을 가르는 실제 사례

측정에서 나온 숫자들을 둘로 나눠보면 이 구분이 구체적으로 보입니다.

```text
   구조와 모양 (기계를 바꿔도 대체로 유지될 것)
   ──────────────────────────────────────
   컴파일러 계열 자식 수              약 11,900개, 흩어짐 1% 미만
   자식 수명의 분포 모양              로그 척도 흩어짐 약 2.37
   daemon의 깨어남 간격 모양          중앙값 수 초에서 수십 초, 넓게 흩어짐
   브라우저 탭 10개의 프로세스 수      21에서 22개
   daemon 모드 색인기가 스스로 쉰다   (앞에서 직접 실행하면 안 쉰다)

   기계에 따라 달라지는 절대값 (관례로 격하)
   ────────────────────────────────────
   파일 복사 중 CPU 비율             0.231  (디스크 속도에 달림)
   컴파일러 자식의 디스크 대기         약 3.6 ms  (NVMe 저장장치)
   다운로드 중 CPU 비율              0.057  (데이터센터 회선)
   컴파일러 자식 하나의 평균 CPU       약 90 ms  (CPU 속도에 달림)
```

아래쪽 숫자들도 archetype에 들어갑니다. 다만 들어갈 때 등급이 한 단계 내려가고, 메모에 서버 사양이 붙습니다.

## 10.4 결과를 기록하는 방식

측정 결과가 archetype에 들어가기까지 거치는 곳이 넷입니다.

```text
   1  작업 흐름 파일        무엇을 어떻게 돌렸나
      .github/workflows/meas-cli.yml, meas-gui.yml, meas-names.yml

   2  원자료              돌린 결과 전부
      GitHub release meas-ci-2026-08-28의 zip 파일들

   3  분석 코드와 요약      원자료에서 통계를 뽑는 방법과 그 결과
      dataset/tools/meas/analyze.py
      dataset/meas/summary.json

   4  archetype 항목       통계를 파라미터로 옮긴 값과 그 과정
      params의 source: "meas-ci:cli:3"
      modeling_notes의 산수
```

**1번에서 4번까지가 전부 저장소와 그 release에 함께 남아 있고, 연구 결과물과 함께 공개하기로 되어 있습니다.** 누군가 archetype의 숫자 하나를 의심하면, 메모의 산수를 따라 요약 파일로 가고, 요약 파일에서 분석 코드로 가고, 분석 코드를 원자료에 돌려 같은 요약이 나오는지 볼 수 있고, 마지막에는 작업 흐름을 다시 돌려서 새 원자료를 얻을 수 있습니다.

release의 설명문이 어떤 묶음이 인용되는지를 적어둡니다.

> "Raw measurement artifacts backing the meas-ci fold-in. CITED batches (pre-freeze supersession): meas-ci:cli:3 (run 33144766132 — warm+cold phases, tracker daemon-mode), meas-ci:gui:2 (run 33139471432), meas-ci:names:1 (run 33067225138). meas-cli.zip is the superseded cli:1 batch (run 33067219710), retained as history, cited nowhere."

인용되는 묶음은 명령줄 측정의 3번 실행, GUI 측정의 2번 실행, 이름 확인의 1번 실행이다. `meas-cli.zip`은 **대체된** 명령줄 측정 1번 실행이고, **기록으로 남겨두되 어디서도 인용하지 않는다.**

> **확인함.** 2026-09-13에 `gh release view meas-ci-2026-08-28`로 release의 설명문과 첨부 파일 목록(`meas-cli.zip`, `meas-cli3.zip`, `meas-gui.zip`, `meas-names.zip`)을 확인했습니다.

**대체된 측정을 지우지 않고 남겨뒀다**는 점이 다음 절의 이야기입니다.

## 10.5 측정이 모형을 고친 일

측정은 한 번에 끝나지 않았습니다. 명령줄 측정의 **1번 실행** 결과를 먼저 archetype에 넣었다가, **3번 실행**을 새로 돌려서 값을 바꿨습니다. 그 과정에서 archetype의 모형 자체가 틀렸다는 것이 드러났습니다.

### 1번 실행: 열다섯 중 열하나

측정을 돌리기 전 archetype 파일에는 **측정 대기** 표시(`meas-pending`)가 붙은 파라미터가 열다섯 개 있었습니다. 값은 임시값이었습니다.

1번 실행과 GUI 측정 결과를 넣었을 때 열다섯 중 **열하나**가 측정값으로 바뀌었습니다. 나머지 넷은 측정 대기로 남았습니다. 그 넷이 왜 남았는지가 기록에 적혀 있습니다. 넣은 날의 커밋 설명입니다.

> "Stay meas-pending with stated findings: compiler disk_wait + background-crawler x3 (CI corpus page-cache-hot, foreground runs never throttle — cold-cache daemon-mode referee needed)."

**발견을 적고 측정 대기로 남긴다.** 컴파일러의 디스크 대기와 색인기의 세 파라미터다. CI의 파일들이 이미 메모리 캐시에 올라가 있어서 디스크 대기가 거의 보이지 않았고, 앞에서 직접 돌린 검사는 절대 속도를 늦추지 않았다. **캐시를 비운 상태와 daemon 모드로 다시 재야 한다.**

**이게 이 절차에서 가장 본받을 만한 부분입니다.** 1번 실행에서도 디스크 대기 값을 "거의 0"으로 적을 수는 있었습니다. 그런데 그건 디스크가 느리지 않아서가 아니라 **디스크를 아예 안 읽어서** 나온 값이었습니다. 측정 조건이 질문에 맞지 않았다는 것을 알아채고, 값을 넣지 않았습니다.

### 3번 실행: 조건을 바꿔 다시 재기

3번 실행은 두 가지를 더했습니다. 매 측정 전에 운영체제의 파일 캐시를 비우는 단계와, 색인기를 daemon 모드로 300초 돌리는 단계입니다. 작업 흐름 파일에 `sudo sysctl -q vm.drop_caches=3`이 여섯 번 들어가 있는 것이 그 흔적입니다.

결과는 이렇습니다.

**디스크 대기.** 캐시를 비우고 빌드해도 **캐시가 따뜻할 때와 통계적으로 같았습니다.** 메모의 문장입니다.

> "the cold-cache rebuild (vm.drop_caches=3) is statistically identical to the warm build (cpu and lifetime means within repeat spread) — per-child disk waits are noise-bounded at ~4 ms on runner NVMe; median 3.6 ms is that measured bound (machine-relative, runner spec recorded)."

캐시를 비운 재빌드는 따뜻한 빌드와 통계적으로 같다. CPU와 수명의 평균이 반복 사이 흩어짐 안에 들어온다. 그러니 자식 하나의 디스크 대기는 **잡음 수준인 약 4밀리초로 위가 막혀 있다.** 중앙값 3.6밀리초는 그 **측정된 상한**이다.

그러니까 3.6밀리초는 "디스크 대기가 3.6밀리초였다"가 아니라 **"측정이 구별할 수 있는 한도 안에서 이보다 크지 않았다"**입니다. 값이 채워졌지만 값의 성격이 다릅니다.

**색인기.** daemon 모드에서 약 3.8초마다 스스로 깨어 약 1.6밀리초씩 일하는 모양이 잡혔습니다. 앞에서 직접 실행한 검사로는 절대 얻을 수 없던 모양입니다.

### 컴파일러 CPU 모형이 틀렸던 것

3번 실행이 드러낸 가장 큰 것은 **컴파일러 자식의 CPU 모형**입니다.

1번 실행 때의 방식은 이랬습니다. 측정이 잘 준 것은 자식의 **수명** 분포였습니다. 중앙값 약 103밀리초, 로그 척도 흩어짐 약 2.37. 그 수명 분포의 **모양을 그대로** CPU 분포에 가져오고, 크기만 CPU를 쓴 비율로 줄였습니다. 그래서 CPU 파라미터가 중앙값 24,000마이크로초, `sigma_log` 2.37이 됐습니다.

문제는 로그 정규 분포의 성질에 있었습니다. **평균 = 중앙값 × exp(sigma_log² / 2).** `sigma_log`가 2.37이면 exp(2.37² / 2)는 약 16.6입니다. 평균이 중앙값의 16배가 넘습니다.

그 모형으로 자식 하나의 계산 평균을 계산하면, 앞뒤 계산의 중앙값 합 26,700마이크로초에 16.6을 곱해서 **약 443밀리초**가 나옵니다. 그런데 3번 실행에서 샘플러로 **직접 잰 자식 하나의 평균 CPU는 약 90밀리초**였습니다.

```text
   1번 실행의 모형이 뜻하는 평균 CPU    약 443 ms
   3번 실행에서 직접 잰 평균 CPU        약  90 ms
```

**수명의 흩어짐을 CPU에 그대로 옮긴 것이 틀렸습니다.** 수명에는 CPU를 쓴 시간 말고도 기다린 시간이 들어갑니다. 측정 중 코어 4개에 컴파일러 계열 프로세스가 최대 16개 떠 있었으니 기다림이 적지 않았을 것이고, 수명으로 센 프로세스에는 계산을 거의 하지 않는 보조 도구도 섞여 있습니다. 어느 쪽이든 수명의 흩어짐이 곧 CPU의 흩어짐은 아니고, 그걸 CPU로 옮기면 CPU의 꼬리가 직접 잰 평균이 허락하는 것보다 길어집니다.

그래서 3번 실행에서는 방법을 바꿨습니다. **평균을 맞추는** 방식입니다. 이 과정은 다음 장에서 컴파일러 항목을 끝까지 따라가며 산수로 봅니다.

> **확인 필요.** 메모와 커밋 설명은 수명의 흩어짐을 옮기는 방식이 "평균을 2.4배 넘겼다(overshot the mean 2.4x)"고 적습니다. 이 권이 요약 파일의 값으로 다시 계산하면 배수가 비교하는 값에 따라 달라집니다. 3번 실행의 CPU 중앙값 약 14.4밀리초에 수명의 흩어짐 2.366을 붙이면 평균이 약 236밀리초이고, 이를 반복 다섯 개의 중앙값 90밀리초와 비교하면 약 2.6배, 반복 중 가장 큰 값 98.8밀리초와 비교하면 약 2.4배입니다. 위의 443밀리초는 1번 실행의 옛 파라미터 그대로의 평균이라 또 다른 비교입니다. 2.4배가 어느 두 값의 비인지 기록에 적혀 있지 않습니다. 결론, 즉 "수명의 흩어짐을 옮기면 평균이 크게 넘친다"는 어느 계산으로도 같습니다.

### 이 이야기에서 가져갈 것

**측정은 파라미터만 채운 것이 아니라 모형의 가정을 시험했습니다.** "CPU 분포는 수명 분포와 모양이 같다"는 가정이 직접 잰 평균과 맞지 않았고, 가정이 버려졌습니다.

그리고 그 과정이 전부 남아 있습니다. 대체된 1번 실행의 원자료는 release에, 옛 파라미터는 커밋 기록에, 바꾼 이유는 메모에 있습니다. **틀렸던 것을 지우지 않았습니다.**

## 10.6 측정이 할 수 없는 것

측정이 모든 빈자리를 메우지는 못합니다. 측정 자체가 가진 한계를 정리해둡니다. 대부분 항목의 메모에 이미 적혀 있는 것들입니다.

### 대신 잰 것들

CI에서 돌릴 수 없는 프로그램은 **비슷한 다른 프로그램**으로 쟀습니다.

| 흉내 내려는 것 | 실제로 잰 것 | 빠진 것 |
|---|---|---|
| Discord, Slack | 로그인하지 않은 Element | 메시지가 오갈 때의 깨어남 |
| 데스크톱의 시스템 프로세스 | CI 서버의 기본 daemon | 아래 확인 필요를 보세요 |
| 집의 다운로드 | 데이터센터 회선의 커널 소스 다운로드 | 느린 회선의 대기 모양 |
| 편집기 옆의 컴파일 | 편집기 없는 커널 빌드 | 사람의 입력과 섞였을 때 |

> **확인 필요.** `system-daemon`의 측정 대상과 그 archetype이 흉내 내는 대상이 다릅니다.
>
> 메모에 따르면 측정 대상은 "stock runner daemons — systemd family, dbus, cron, etc."입니다. 분석 코드가 daemon으로 센 이름은 `systemd`, `systemd-journal`, `systemd-udevd`, `systemd-resolve`, `systemd-network`, `systemd-logind`, `dbus-daemon`, `cron`, `rsyslogd`, `polkitd`, `chronyd`, `multipathd`, `agetty`, `packagekitd`, `udisksd`, `acpid`입니다. 전부 **서버에서도 도는** 시스템 서비스입니다.
>
> 그런데 이 archetype에 묶이는 이름에는 `gnome-shell`(데스크톱 화면을 그리는 셸), `Xorg`(화면 서버), `pipewire`(소리 서버)가 있습니다. 이 셋은 측정 대상에 없고, CI 서버에는 떠 있지도 않습니다. 그리고 앞에서 본 ananicy 카탈로그는 `gnome-shell`과 `Xorg`와 `pipewire`를 전부 `LowLatency_RT`, 즉 "무겁지는 않지만 절대 늦으면 안 되는" 분류에 넣습니다. 사람이 앉아 있을 때 화면 서버와 소리 서버는 거의 쉬는 daemon과 성격이 다를 수 있습니다.
>
> 사람이 없는 상황만 담는 파일에서라면 이 근사가 크게 문제되지 않을 수 있습니다. 사람이 없으면 화면과 소리 서버도 할 일이 적기 때문입니다. 다만 그 판단이 어디에도 적혀 있지 않습니다. 무엇을 열어보면 되는지: 이 셋을 `system-daemon`에 묶기로 한 결정의 기록입니다. 찾지 못했습니다.

### 표본의 크기

측정이 준 분포 중 몇은 **표본이 아주 작습니다.**

```text
   색인기 daemon 모드     프로세스 5개   (반복마다 하나)
   Element               프로세스 15개
   다운로드 CPU 비율      반복 5번 중 2번
   daemon의 한 번 계산량   프로세스 51개 중 29개
```

색인기의 `sigma_log` 0.428과 0.639는 **값 다섯 개**에서 계산한 표준편차입니다. daemon의 한 번 계산량이 51개 중 29개에서만 나온 것은, 나머지 22개가 측정 기간 동안 CPU 시간이 한 칸도 올라가지 않아서 0으로 기록됐고, 분포를 맞출 때 0은 뺐기 때문입니다.

### 측정의 해상도

분석 코드 머리에 이런 줄이 있습니다.

```python
TICK_US = 10_000  # USER_HZ=100 on the runners (spec.json corroborates)
```

운영체제가 프로세스별 CPU 시간을 **10밀리초 단위**로 센다는 뜻입니다. 그러니 한 번에 0.155밀리초를 쓰는 daemon의 계산량은 한 번 한 번을 잴 수 없고, **긴 기간의 CPU 칸 수를 깨어난 횟수로 나눠서** 얻은 평균입니다.

그리고 그 "깨어난 횟수"는 프로세스가 **스스로 CPU를 놓은 횟수**를 센 것입니다. 한 번 깨서 두 번 놓으면 두 번으로 셉니다.

### 무엇이 분포인가

마지막 한계가 가장 미묘합니다. daemon과 앱과 색인기의 깨어남 간격 분포는 **프로세스마다 평균 간격 하나씩을 구해서, 그 평균들을 모은 분포**입니다. 분석 코드가 프로세스 하나의 측정 기간을 깨어난 횟수로 나눠 간격 하나를 만들고, 그 값들로 로그 정규를 맞춥니다.

```text
   분포가 말하는 것:      daemon A는 평균 5초마다, daemon B는 평균 20초마다 깬다.
                         이런 평균들이 로그 척도로 1.9만큼 흩어져 있다.

   분포가 말하지 않는 것:  daemon A 하나가 3초, 7초, 4초, 6초 간격으로
                         얼마나 불규칙하게 깨는가.
```

**흩어짐이 프로세스와 프로세스 사이에 있고, 한 프로세스 안에는 없습니다.**

이 사실이 항목의 필드를 볼 때 확인 필요로 적어둔 문제와 맞물립니다. 파일은 이 파라미터를 **반복마다** 새로 뽑는다고 선언하는데, compile 단계는 **task마다 한 번** 뽑습니다. 측정이 준 분포가 프로세스 사이의 흩어짐이라면, 오히려 compile 단계의 방식이 측정과 맞고 파일의 선언이 측정과 어긋납니다. 두 문제를 함께 보고 정해야 합니다.

## 10.7 산문 문서들이 측정을 따라오지 못한 자리

측정값이 archetype 파일에 들어간 것은 2026년 8월 28일입니다. 그런데 몇몇 산문 문서는 아직 측정 전의 상태를 적고 있습니다.

> **확인 필요.** 파일과 산문 문서가 측정의 상태에 대해 다른 말을 합니다. 파일이 규범이므로 이 권은 파일 기준으로 썼습니다.
>
> **파일이 말하는 것.** `dataset/archetypes.yaml`의 모든 숫자 파라미터에 측정 대기 표시가 하나도 없습니다. 검사 도구의 "얼린 뒤" 모드도 통과합니다. 데이터셋 안내 문서는 이 파일을 "fully measured, v0.1"이라고 적습니다.
>
> **산문이 말하는 것.** 세 문서가 측정 전 상태를 적고 있습니다.
>
> - 인용 문서의 `meas-ci` 항목: "status: reserved (no runs yet; `meas-pending` placeholders in archetypes until freeze)". 아직 한 번도 돌리지 않았다는 뜻입니다.
> - 계획 문서의 열두 항목 목록: 컴파일러 자식의 수명 분포, 색인기의 빈도, 다운로드와 가끔 깨는 앱과 시스템 daemon의 파라미터를 `meas-pending`으로 적습니다. 연속 입출력의 파라미터 출처를 interbench로 적는데, 파일은 측정으로 적습니다.
> - 데이터셋 구축 문서의 archetype 요약표: 다운로드, 가끔 깨는 앱, 시스템 daemon을 `meas-pending`으로 적습니다.
>
> 계획 문서의 머리에는 "Updated 2026-09-10"이 적혀 있어서, 측정 이후에 한 번 이상 고쳐졌는데도 이 줄들은 갱신되지 않았습니다. 고쳐야 할 자리로 보이지만, 이 권은 산문 문서를 고치지 않습니다.

---

## 10장 정리

- 일곱 항목의 파라미터가 전부 측정에서 왔습니다. 사무, 웹, 창작 쪽 프로세스의 시간 숫자는 문헌에 없고, 이름이 붙은 데스크톱 프로세스 기록은 개인정보 때문에 구조적으로 공개되지 않습니다.
- 측정 캠페인은 공개 CI 서버에서 공개된 작업 흐름으로 돌렸습니다. 누구든 다시 돌릴 수 있다는 것이 이 방식을 고른 이유입니다.
- 명령줄 측정과 GUI 앱 측정이 archetype의 숫자를 줬습니다. 프로세스의 탄생과 죽음을 기록하는 도구와, 주기적으로 상태를 찍는 도구가 함께 돌았습니다.
- 측정한 기계는 코어 4개의 CI 서버였고, 사양이 원자료에 기록되어 있습니다. 각 측정은 다섯 번 돌렸고 요약 파일은 흩어짐을 감추지 않습니다.
- 측정은 소프트웨어 행동의 구조와 모양만 뒷받침합니다. 기계에 따라 달라지는 절대값은 측정으로 보강한 관례로 격하됩니다.
- 작업 흐름, 원자료, 분석 코드와 요약, archetype 메모까지 네 단계가 전부 공개되어 있어서 숫자 하나를 원자료까지 거꾸로 따라갈 수 있습니다.
- 첫 측정에서 조건이 질문에 맞지 않은 넷은 값을 넣지 않고 측정 대기로 남겼습니다. 캐시를 비우고 daemon 모드로 다시 잰 뒤에야 채웠습니다.
- 다시 잰 측정이 모형의 가정을 뒤집었습니다. 수명의 흩어짐을 CPU에 그대로 옮기면 CPU 평균이 직접 잰 값보다 크게 넘쳐서, 평균을 맞추는 방식으로 바꿨습니다. 대체된 결과는 지우지 않고 남겼습니다.
- 측정에는 한계가 있습니다. 계정이 필요한 앱은 대체 앱으로 쟀고, 데스크톱의 화면과 소리 서버는 서버 daemon으로 대신했고, 몇몇 분포는 표본이 다섯 개뿐이고, CPU 시간은 10밀리초 단위로만 셉니다.
- 깨어남 간격 분포는 프로세스마다의 평균 간격을 모은 것이라, 흩어짐이 프로세스 사이에만 있습니다. 파일이 선언한 뽑는 빈도와 함께 봐야 할 사실입니다.
- 산문 문서 세 곳이 아직 측정 전 상태를 적고 있습니다.

---

# 11장 · 손으로 따라가기: compiler-child를 끝까지

## 11.1 왜 이 항목인가

이 장은 archetype 하나를 **출처의 문장에서 시작해 실제로 뽑힌 숫자까지** 끝까지 따라갑니다. 고른 항목은 컴파일러 자식 하나를 흉내 내는 `compiler-child`입니다.

이 항목을 고른 이유는 **사슬의 모든 칸이 다 있기 때문**입니다.

```text
   1  출처의 문장           논문 두 편
   2  측정                  CI 서버에서 다섯 번 돌린 커널 빌드
   3  산수                  측정값을 파라미터로 옮기는 계산
   4  관례                  출처도 측정도 말하지 않는 빈칸
   5  분포                  로그 정규 셋
   6  구체적인 숫자          compile 단계가 뽑은 값
   7  사건의 흐름            그 숫자로 된 프로그램
   8  재현해야 할 통계        판정 기준
```

음악 재생 항목은 1번에서 곧바로 6번으로 갑니다. 게임 항목은 8번이 비어 있습니다. 컴파일러 자식은 여덟 칸이 전부 차 있고, 칸마다 등급이 다릅니다.

먼저 항목 전체를 한 번 봅니다.

```yaml
compiler-child:
  category_source: ocallahan-atc17
  pattern:
    program:
      - RUN: cpu_burst
      - WAIT: disk
      - RUN: cpu_tail
      - EXIT: {}
  params:
    cpu_burst:
      {dist: lognormal, median_us: 12900, sigma_log: 1.91,
       sampling: per-instance, source: "meas-ci:cli:3"}
    cpu_tail:
      {dist: lognormal, median_us: 1440, sigma_log: 1.91,
       sampling: per-instance, source: "meas-ci:cli:3"}
    disk_wait:
      {dist: lognormal, median_us: 3600, sigma_log: 0.8,
       sampling: per-instance, source: "meas-ci:cli:3"}
  lifetime: spawned
  spawned_by: build-orchestrator
  binding_params: []
  scalable: []
  validation_stats:
    referee: meas-ci
    stats: [child lifetime CDF, concurrent-children time series]
```

## 11.2 첫째 칸: 출처의 문장

### 저장소가 적어둔 것

항목의 메모는 이렇게 시작합니다.

> "The kernel-build literature grounds the class's existence and short-lived character only (ocallahan-atc17 sec-4.3: "make forks and execs 2430 processes, mostly short-lived"; coetzee-arxiv12 sec-9 corroborates, kernel-build-specific)."

**커널 빌드 문헌**은 이 부류가 존재한다는 것과 짧게 산다는 성격**만** 뒷받침한다. O'Callahan 논문 4.3절이 "make가 2430개의 프로세스를 fork하고 exec하며, 대부분 짧게 산다"고 적고, Coetzee 논문 9절이 커널 빌드에 한정해서 이를 뒷받침한다.

출처 등록부도 같은 틀로 적습니다.

> "make forks and execs 2430 processes, mostly short-lived" (sec-4.3, Linux kernel-build workload; written "2430" in the paper). Grounds the fork-burst count and short-lived character of compiler children only; the paper gives no lifetime distribution."

4.3절, **Linux 커널 빌드 workload**. 논문에는 "2430"으로 적혀 있다. 컴파일러 자식의 fork 폭발 개수와 짧게 사는 성격만 뒷받침하고, 수명 분포는 주지 않는다.

"뒷받침만 한다(only)"는 표현이 두 문서에 반복됩니다. 이 논문에서 **값은 가져오지 않는다**는 선언입니다. 좋은 절제입니다.

### 원문을 엽니다

O'Callahan 외 다섯 명의 2017년 USENIX ATC 논문은 **rr**이라는 기록·재생 디버깅 도구를 설명합니다. 프로그램 실행을 기록해두었다가 똑같이 다시 돌려볼 수 있게 해주는 도구입니다. 논문의 평가 절이 그 도구의 부담을 여러 workload에서 잽니다.

4.3절의 해당 문단 전체입니다.

> "Overhead on make is significantly higher than for the other workloads. Forcing make onto a single core imposes major slowdown. Also, make forks and execs 2430 processes, mostly short-lived. (The next most prolific workload is sambatest with 89.) In-process system-call interception only starts working in a process once the interception library has been loaded, but at least 80 system calls are performed before that completes, so its effectiveness is limited for short-lived processes."

make에서의 부담이 다른 workload보다 훨씬 크다. make를 코어 하나에 강제하면 크게 느려진다. 또한 make는 2430개의 프로세스를 fork하고 exec하며, 대부분 짧게 산다(다음으로 많은 workload는 sambatest로 89개다). 프로세스 안에서 system call을 가로채는 기능은 가로채기 라이브러리가 로드된 뒤에야 작동하는데 그 전에 system call이 적어도 80번 일어나서, 짧게 사는 프로세스에는 효과가 제한된다.

인용한 문장이 원문에 **글자 그대로** 있습니다. 숫자도 맞고 절 번호도 맞습니다.

그러면 그 `make` workload가 무엇이었는지를 봅니다. 같은 논문의 4.1절 "Workloads"입니다.

> "make builds DynamoRio [8] (version 6.1.0) with make -j8 (-j8 omitted when restricting to a single core). This tests potentially-parallel execution of many short-lived processes."

**make는 DynamoRio(판본 6.1.0)를 `make -j8`로 빌드한다.** 코어 하나로 제한할 때는 `-j8`을 뺀다. 이 workload는 **짧게 사는 프로세스가 많이 병렬로 도는 경우**를 시험한다.

그리고 실험한 기계입니다.

> "All tests run on a Dell XPS15 laptop with a quad-core Intel Skylake CPU (8 SMT threads), 16GB RAM and a 512GB SSD using Btrfs in Fedora Core 23 Linux."

모든 시험은 코어 4개(스레드 8개)의 Intel Skylake CPU, 메모리 16GB, SSD 512GB를 가진 Dell XPS15 노트북에서 Fedora Core 23 Linux로 돌렸다.

> **확인함.** 2026-09-13에 USENIX가 공개한 학회 논문 PDF(usenix.org/system/files/conference/atc17/atc17-o_callahan.pdf, 15쪽)와 확장판 기술 보고서(arXiv:1705.05937, 21쪽)를 받아 둘 다 읽었습니다. 학회판에서 4.1절과 4.3절은 학회 논문집 383쪽에 있고, 두 판 모두 `make` workload를 **DynamoRio 6.1.0 빌드**로 적습니다. 두 판 어디에도 이 workload를 Linux 커널 빌드라고 적은 곳이 없습니다.
>
> **저장소 문서들은 이 숫자를 커널 빌드의 값으로 적고 있습니다.** 출처 등록부("Linux kernel-build workload"), 인용 문서("kernel-build workload"), archetype 메모("the kernel-build default is 2,430"), 초기 조사 문서("kernel build forks/execs 2,430"), 상황 목록 S11의 출처 칸("kernel-build characterization (2,430 short-lived procs, arXiv 1705.05937)"), 계획 문서와 구축 문서가 모두 그렇습니다.
>
> 이 권은 원문을 따라 씁니다. 저장소 문서는 고치지 않았습니다.

### 어긋남이 무엇을 바꾸나

이 어긋남이 이 항목에서 **무엇을 바꾸고 무엇을 바꾸지 않는지**를 정확히 봐야 합니다.

**바꾸지 않는 것.** 부류의 존재입니다. 원문 4.1절은 이 workload를 고른 이유를 "짧게 사는 프로세스가 많이 병렬로 도는 경우를 시험하려고"라고 명시합니다. `make`가 짧게 사는 자식을 대량으로 만든다는 성격은 DynamoRio 빌드에서도 그대로입니다. 부류의 존재 근거로서 이 논문은 여전히 유효합니다. 오히려 **저자들이 그 성격을 의도적으로 고른 workload**라는 점이 더 분명해졌습니다.

**바꾸는 것.** 2,430이라는 **개수의 뜻**입니다. 메모는 이 수를 "커널 빌드의 기본값"으로 부모 archetype에 적어뒀습니다. 그런데 이 수는 커널 빌드가 아니라 DynamoRio라는 도구 하나의 빌드에서 나왔습니다. 그리고 우리 측정에서 커널 빌드 한 번은 컴파일러 계열 자식을 **약 11,900개** 만들었습니다. 2,430과 11,900은 다섯 배 가까이 차이가 나는데, 두 수가 서로 다른 프로젝트의 빌드라면 이 차이는 이상하지 않습니다.

그리고 뜻밖의 발견이 하나 있습니다. **원문도 `make -j8`로 돌렸습니다.** 이 연구가 동시 실행 상한 8을 "interbench의 -j4와 코어 수 사이의 관례"로 정당화한 것은 개수를 다룬 장에서 봤습니다. 부류의 근거로 이미 인용하고 있는 논문이 똑같이 8을 썼다는 사실은 저장소 어디에도 적혀 있지 않습니다.

> **확인 필요.** 두 가지를 확인하고 정해야 합니다.
>
> 하나, 2,430을 부모 archetype의 기본값으로 계속 적을 것인가. 원문을 따르면 이 수는 "DynamoRio 6.1.0 빌드 한 번"의 값입니다. 커널 빌드의 값이 필요하다면 우리 측정의 약 11,900이 있고, 그 수는 컴파일러 드라이버와 어셈블러와 보조 도구까지 센 계열 전체라는 조건이 붙습니다.
>
> 둘, 저장소 문서 여러 곳의 "커널 빌드"라는 설명을 원문에 맞게 고칠 것인가. 이 연구의 인용 규칙은 원문과 대조되지 않은 설명을 쓰지 않는 것이므로 고치는 쪽이 규칙과 맞습니다. 다만 고치는 것은 이 권의 일이 아닙니다.
>
> 이 어긋남이 어디서 시작됐는지는 기록에서 짐작할 수 있습니다. 초기 조사 문서가 이 논문의 id를 확정하기 전 "record-and-replay study"로만 부르던 시기에 "kernel build forks/execs 2,430"이라고 적었고, 나중에 논문이 확정되면서 인용 문장만 원문과 대조되고 workload의 정체는 대조되지 않은 것으로 보입니다. 이 짐작 자체도 기록으로 확인되지는 않습니다.

### 둘째 논문

Coetzee, Bhaskar, Necula의 2012년 논문 원고는 믿을 수 있는 빌드 시스템을 만드는 방법을 다룹니다. 9절 "Preliminary experimental results"의 해당 문장이 들어 있는 문단입니다.

> "Jockey rewrites binaries at load time by searching for system calls, and also keeps a cache of patches to apply for binaries it's seen before. In practice, even with caching, the system added too much overhead to be practical due to the Linux kernel build's enormous number of short-lived processes like cp and mkdir. This is less likely to be an issue in a more monolithic build system."

Jockey는 프로그램이 로드될 때 system call을 찾아 바이너리를 고쳐 쓰고, 한 번 본 바이너리의 수정 사항은 캐시해둔다. 실제로는 캐시를 써도 부담이 너무 커서 쓸 수 없었는데, **Linux 커널 빌드가 `cp`나 `mkdir` 같은 짧게 사는 프로세스를 엄청나게 많이 만들기 때문**이었다. 더 한 덩어리로 된 빌드 시스템에서는 문제가 덜할 것이다.

이쪽은 커널 빌드가 맞습니다. 출처 등록부가 "커널 빌드에 한정된 특성으로 인용하라"고 적은 것도 원문과 맞습니다.

그런데 원문의 예시가 눈에 띕니다. **`cp`와 `mkdir`**. 파일을 복사하고 디렉터리를 만드는 프로그램입니다. 컴파일러가 아닙니다.

> **확인함.** 2026-09-13에 arXiv:1203.2704 v1(11쪽)을 받아 9절을 읽었습니다. 인용한 구절은 원문에 글자 그대로 있고, 짧게 사는 프로세스의 예로 든 것은 `cp`와 `mkdir`입니다.
>
> 그러니 이 논문이 보조하는 것은 "커널 빌드는 짧게 사는 프로세스를 엄청나게 많이 만든다"이지 "컴파일러 자식이 짧게 산다"가 아닙니다. 두 문장이 가까운 것은 맞지만, 메모의 "corroborates"가 뜻하는 뒷받침의 폭은 원문보다 조금 넓습니다.

### 첫째 칸에 남는 것

두 원문을 읽고 나면 첫째 칸에 남는 것이 이렇게 정리됩니다.

```text
   O'Callahan (첫째 등급)
     make가 짧게 사는 프로세스를 대량으로 만든다  ← 부류의 존재. 유효
     DynamoRio 6.1.0 빌드에서 2,430개             ← 개수. 커널 빌드가 아님
     make -j8로 돌렸다                            ← 저장소가 쓰지 않은 사실

   Coetzee (첫째 등급, 논문 원고)
     커널 빌드는 cp, mkdir 같은 짧게 사는
     프로세스를 엄청나게 많이 만든다               ← 부류의 존재를 보조. 컴파일러 한정은 아님
```

**값은 여전히 하나도 가져오지 않습니다.** 두 논문 모두 수명 분포를 주지 않습니다. 이 사실은 메모가 처음부터 정확히 적어뒀습니다.

## 11.3 둘째 칸: 측정

값은 우리 측정에서 옵니다. 메모의 문장입니다.

> "meas-ci:cli:3 (linux-6.6 defconfig, make -j8, 5 repeats): ~11.9k compiler-family children per build, lifetime median ~100 ms sigma_log ~2.37 (forkstat exit durations)."

측정의 3번 실행. Linux 6.6 커널을 기본 설정으로 `make -j8` 빌드, 다섯 번 반복. 빌드 한 번에 컴파일러 계열 자식 약 1만 1천 9백 개, 수명 중앙값 약 100밀리초, 로그 척도 흩어짐 약 2.37. 수명은 프로세스가 끝날 때 기록한 지속 시간에서 얻었다.

측정 요약 파일에서 해당 값들을 가져옵니다. 반복 다섯 개를 가로지른 중앙값입니다.

| 통계 | 중앙값 | 최소 | 최대 |
|---|---|---|---|
| 컴파일러 계열 자식 수 | 11,883 | 11,835 | 11,914 |
| 수명 중앙값 | 99,801 us | 76,885 us | 105,713 us |
| 수명 `sigma_log` | 2.366 | 2.344 | 2.379 |
| 자식 하나의 평균 CPU | 89,997 us | 61,620 us | 98,793 us |
| 자식 하나의 평균 수명 | 625,335 us | 499,646 us | 669,059 us |
| 부모가 자식 하나당 쓴 CPU | 234 us | 183 us | 262 us |

**등급.** 자식 수와 수명 분포의 모양은 셋째 등급의 구조와 모양 쪽입니다. 반복 사이 흩어짐도 작습니다. 평균 CPU는 CPU 속도에 달린 절대값이라 측정으로 보강한 관례 쪽이고, 흩어짐도 61에서 99밀리초로 큽니다.

### 평균 CPU는 하한입니다

평균 CPU 약 90밀리초에는 조건이 붙어 있습니다.

> "the 500 ms sampler measures mean cpu/child ~90 ms directly (still a lower bound — sub-500 ms children are partially censored; the 4-core utilization bound is ~165 ms)"

0.5초 간격 샘플러가 자식 하나의 평균 CPU를 약 90밀리초로 직접 잰다. 다만 **여전히 하한**이다. 0.5초보다 짧게 사는 자식은 일부가 사진에 안 찍힌다. 코어 4개의 사용률로 계산한 상한은 약 165밀리초다.

사진을 0.5초마다 찍으면, 두 사진 사이에 태어나서 죽은 자식은 한 번도 안 찍힙니다. 그 자식이 쓴 CPU는 합계에 들어가지 않습니다. 그래서 90밀리초는 **실제보다 작을 수 있는** 값이고, 반대쪽에서 "코어 4개가 빌드 내내 꽉 찼다고 치면 자식 하나당 이만큼을 넘을 수 없다"는 계산이 165밀리초를 줍니다. 실제 값은 그 사이 어딘가입니다.

**측정이 값 하나가 아니라 범위를 주고, 항목은 그중 아래쪽 끝을 골랐습니다.** 그 선택이 메모에 적혀 있습니다.

## 11.4 셋째 칸: 산수

측정이 준 것은 **수명의 분포**와 **CPU의 평균**입니다. archetype에 필요한 것은 **CPU의 분포**입니다. 둘 사이를 산수로 잇습니다.

앞 장에서 봤듯이 처음에는 수명 분포의 모양을 CPU에 그대로 옮겼다가 평균이 크게 넘쳐서 버렸습니다. 지금의 방식은 메모에 이렇게 적혀 있습니다.

> "cpu params are moment-matched: … median cpu = (cpu_mean/life_mean) x life_median ~ 14.4 ms; sigma_log 1.91 from mean/median = 6.25 — matching the measured mean rather than carrying the lifetime log-std (which overshot the mean 2.4x)."

CPU 파라미터는 **적률을 맞춘다.** 여기서 **적률**은 평균이나 분산처럼 분포를 요약하는 값을 말하고, 적률을 맞춘다는 것은 분포의 모양을 정할 때 측정한 평균이 그대로 나오게 한다는 뜻입니다. 계산은 두 단계입니다.

### 1단계: CPU의 중앙값

```text
   CPU 중앙값 = (평균 CPU / 평균 수명) × 수명 중앙값

             = (89,997 / 625,335) × 99,801
             = 0.14392 × 99,801
             ≈ 14,363 us
             ≈ 14.4 ms
```

**가정이 하나 들어갔습니다.** 자식마다 "수명 중 CPU를 쓴 비율"이 대체로 같다는 가정입니다. 평균 수명의 14.4퍼센트를 CPU로 썼으니, 중앙값 수명을 가진 자식도 그 14.4퍼센트를 CPU로 썼다고 보는 것입니다. 이 가정은 넷째 등급입니다.

### 2단계: CPU의 흩어짐

로그 정규 분포에서 평균과 중앙값의 관계는 **평균 = 중앙값 × exp(sigma_log² / 2)**였습니다. 이걸 거꾸로 풀면 흩어짐이 나옵니다.

```text
   평균 / 중앙값 = 90 / 14.4 = 6.25

   exp(sigma_log² / 2) = 6.25
   sigma_log² / 2      = ln(6.25) ≈ 1.8326
   sigma_log²          ≈ 3.6652
   sigma_log           ≈ 1.914
                       → 1.91
```

**이 흩어짐은 측정한 평균이 나오도록 거꾸로 푼 값입니다.** 수명의 흩어짐 2.37을 그대로 쓰는 대신, "평균이 90밀리초가 되려면 흩어짐이 얼마여야 하나"를 풀었습니다.

### 3단계: 앞뒤로 나누기

프로그램 모양은 "계산 → 디스크 대기 → 계산"입니다. 계산이 두 조각이라 CPU 중앙값을 둘로 나눕니다.

```text
   앞 계산 = 14,363 × 0.9 ≈ 12,927 → 12,900 us
   뒤 계산 = 14,363 × 0.1 ≈  1,436 →  1,440 us
```

메모의 문장이 짧습니다. "The 90/10 burst/tail split is ours." **90 대 10으로 나눈 것은 우리 것이다.** 출처도 측정도 이 비율을 말하지 않습니다. 넷째 등급입니다.

### 검산

만들어진 파라미터로 평균을 다시 계산해서 90밀리초가 나오는지 봅니다.

```text
   exp(1.91² / 2) = exp(1.82405) ≈ 6.197

   앞 계산의 평균 = 12,900 × 6.197 ≈ 79,941 us
   뒤 계산의 평균 =  1,440 × 6.197 ≈  8,924 us
   합                              ≈ 88,865 us ≈ 89 ms
```

측정한 90밀리초와 거의 같습니다. 반올림 때문에 약간 모자랍니다. **산수가 선언한 목표를 지킵니다.**

> **이 연구에서는.** 이 산수에서 등급이 섞이는 모양을 정리하면 이렇습니다.
>
> ```text
>    수명 중앙값 99,801       셋째 등급 · 모양
>    평균 수명 625,335        셋째 등급 · 모양
>    평균 CPU 89,997          셋째 등급 · 절대값, 그리고 하한
>    "CPU 비율은 자식마다 같다"  넷째 등급 · 가정
>    분포 가족 로그 정규        넷째 등급 · 관례
>    90 대 10 나누기           넷째 등급 · 관례
>    ─────────────────────────────────────────
>    cpu_burst 12,900 / 1.91   네 가지가 합쳐진 결과
> ```
>
> 파일의 출처 표시는 `meas-ci:cli:3` 하나입니다. 메모를 읽지 않으면 이 표의 아래 세 줄이 보이지 않습니다.

## 11.5 넷째 칸: 관례로 남은 것

산수로 채우지 못한 빈칸이 하나 더 있습니다. 디스크 대기의 **흩어짐**입니다.

디스크 대기 중앙값 3,600마이크로초는 앞 장에서 본 대로 "캐시를 비워도 구별되지 않는 잡음의 상한"입니다. 그러면 옆의 `sigma_log: 0.8`은 어디서 왔을까요.

메모에는 이 값에 대한 설명이 없습니다. 중앙값의 근거는 길게 적혀 있는데 흩어짐은 언급되지 않습니다. 저장소의 변경 기록을 거꾸로 따라가면 사정이 보입니다.

```text
   처음 만들 때       disk_wait: {dist: lognormal, source: "meas-pending"}
                     값 없음

   임시값을 채울 때     median_us: 20000, sigma_log: 0.8, source: "meas-pending"

   측정을 넣을 때       median_us: 3600,  sigma_log: 0.8, source: "meas-ci:cli:3"
                                         ↑ 그대로
```

**0.8은 측정 전에 넣은 임시값이 측정 후에도 남은 것입니다.** 중앙값은 측정으로 바뀌었고 출처 표시도 측정으로 바뀌었는데, 흩어짐은 바뀌지 않았습니다.

> **확인 필요.** `disk_wait`의 `sigma_log: 0.8`은 측정 전 임시값으로 들어온 값이고, 지금 출처 표시는 측정을 가리키지만 측정 요약 파일에 이 흩어짐의 근거가 되는 값이 없습니다. 메모도 이 값을 관례라고 적지 않습니다. 같은 파일의 다른 항목들은 측정이 흩어짐을 주지 않을 때 "sigma is our convention"이라고 적어두는데, 이 값만 그 문장이 빠져 있습니다.
>
> 측정이 "디스크 대기는 잡음 수준"이라는 것까지만 알려줬다면, 흩어짐을 무엇으로 둘지는 관례의 영역이 맞습니다. 확인할 것은 **0.8을 그런 관례로 의도하고 남긴 것인지**, 측정을 넣을 때 빠뜨린 것인지입니다. 무엇을 열어보면 되는지: 측정을 넣은 날의 작업 기록입니다. 변경 기록의 설명문은 중앙값만 언급합니다.

## 11.6 다섯째와 여섯째 칸: 분포에서 숫자로

이제 분포에서 실제 숫자가 뽑히는 순간입니다. `c1-compile` 파일의 `make`가 만드는 자식 100개 중 **첫째 자식**을 봅니다. compile 단계를 거친 결과입니다.

```text
   build.c1  (이름: cc1)
     RUN    664 us
     SLEEP  3,126 us
     RUN    9 us
     EXIT
```

`WAIT: disk`가 `SLEEP`으로 바뀌었습니다. primitive를 볼 때 본 대로, 깨워줄 디스크가 없는 시뮬레이터에서는 디스크 대기가 정해진 길이의 멈춤이 됩니다.

### 이 숫자들은 분포의 어디쯤인가

로그 정규 분포에서 값 하나가 뽑힐 때의 식은 **중앙값 × exp(sigma_log × z)**였습니다. 값을 알면 z를 거꾸로 구할 수 있습니다. z는 "표준 정규 분포에서 몇 걸음 떨어진 곳에서 뽑혔나"입니다.

```text
   앞 계산   664 = 12,900 × exp(1.91 × z)
             z = ln(664 / 12,900) / 1.91 = ln(0.05147) / 1.91
               ≈ -2.967 / 1.91 ≈ -1.55

   디스크    3,126 = 3,600 × exp(0.8 × z)
             z = ln(3,126 / 3,600) / 0.8 = ln(0.8683) / 0.8
               ≈ -0.141 / 0.8 ≈ -0.18

   뒤 계산   9 = 1,440 × exp(1.91 × z)
             z = ln(9 / 1,440) / 1.91 = ln(0.00625) / 1.91
               ≈ -5.075 / 1.91 ≈ -2.66
```

첫째 자식은 **아주 짧은 자식**입니다. 앞 계산이 표준 정규의 −1.55 걸음, 뒤 계산이 −2.66 걸음입니다. −2.66 걸음보다 작은 값이 나올 확률은 약 0.4퍼센트이니, 뒤 계산 9마이크로초는 드물게 작은 값입니다. 디스크 대기는 중앙값 근처입니다.

다섯째 자식은 반대입니다.

```text
   build.c5
     RUN    113,228 us      z = ln(113,228 / 12,900) / 1.91 ≈ 2.172 / 1.91 ≈ +1.14
     SLEEP  8,981 us
     RUN    81 us
     EXIT
```

앞 계산이 113밀리초로 중앙값의 약 9배입니다. 그런데 뒤 계산은 81마이크로초로 작습니다.

### 앞뒤가 따로 뽑힙니다

**앞 계산과 뒤 계산이 서로 모르고 뽑힌다**는 점이 보입니다. 넷째 자식은 앞 계산 3,029마이크로초, 뒤 계산 7,844마이크로초로 **뒤가 앞보다 깁니다.** 90 대 10이라는 나누기는 **중앙값끼리의 비율**일 뿐, 자식 하나하나에서 지켜지지 않습니다.

그리고 `sampling: per-instance`의 뜻이 여기서 보입니다. 자식마다 따로 뽑습니다. 100개의 자식이 100개의 다른 프로그램을 가집니다.

> **코드로.** 값을 뽑는 방식은 `dataset/tools/wlc/sampling.py`에 있습니다. 뽑기 하나하나가 "timeline의 seed, 부모 task의 id, 몇 번째 자식인가, 어느 파라미터인가"를 이어붙인 문자열의 SHA-256 해시로 정해집니다. `c1-compile`의 seed는 103입니다. 그래서 같은 파일을 몇 번 compile해도 첫째 자식은 늘 664, 3,126, 9를 받습니다. 이 방식이 왜 필요한지는 다음 권에서 봅니다.

## 11.7 일곱째 칸: 사건의 흐름

첫째 자식의 프로그램을 1권의 상태 이름으로 읽으면 이런 흐름을 **요청합니다.**

```text
   부모가 FORK        → 태어나서 ready
   RUN 664 us         → CPU를 받으면 running, 664 us어치 계산
   SLEEP 3,126 us     → 스스로 blocked, 3.126 ms 동안
   (시간이 지남)       → ready
   RUN 9 us           → CPU를 받으면 running, 9 us어치 계산
   EXIT               → done
```

만약 **CPU를 한 번도 기다리지 않는다면** 이 자식은 태어나서 0.664 + 3.126 + 0.009 = 3.799밀리초 뒤에 끝납니다. 그게 이 자식이 원하는 가장 짧은 수명입니다.

실제로 몇 밀리초에 끝나는지는 **ready에서 running으로 언제 올라가느냐**에 달려 있고, 그건 이 프로그램이 정하지 않습니다. 이 자식이 태어나는 순간 이미 7개의 형제와 편집기와 다른 task들이 CPU 한 자리를 두고 줄을 서 있을 것입니다. 그 줄에서 이 자식이 언제 차례를 받는지, 계산 도중 빼앗기는지는 scheduler와 시뮬레이터가 정합니다. 여기서 멈춥니다.

## 11.8 여덟째 칸: 재현해야 할 통계

마지막 칸입니다.

```yaml
validation_stats:
  referee: meas-ci
  stats: [child lifetime CDF, concurrent-children time series]
  note: headless real-build workflow (make -jN with /proc sidecar);
    lifetime absolutes are machine-relative — recorded with the runner
    spec, convention-informed-by-measurement.
```

재현해야 할 통계는 둘입니다. **자식 수명의 누적 분포**와 **동시에 살아 있는 자식 수의 시간 변화**입니다. 그리고 수명의 절대값은 기계에 따라 달라지므로 측정으로 보강한 관례로 친다는 조건이 붙습니다.

**누적 분포**, 영어로 CDF는 "수명이 x 이하인 자식의 비율"을 x마다 그린 곡선입니다. 중앙값 하나가 아니라 분포 전체의 모양을 비교하겠다는 뜻입니다.

### 이 칸이 가진 어려움

손으로 따라온 내용에서 이 판정의 어려움이 세 가지 보입니다.

**하나, 수명은 scheduling의 결과입니다.** 시뮬레이션에서 자식의 수명은 CPU 요구량과 디스크 대기와 **CPU를 기다린 시간**의 합입니다. 측정의 수명도 코어 4개를 두고 다툰 결과입니다. CPU가 하나인 시뮬레이터에서 어떤 설정으로 돌린 수명 분포를, 코어가 4개인 기계에서 기본 scheduler로 돌린 수명 분포와 비교하는 것이 됩니다. **같아야 하는지부터가 질문입니다.**

**둘, 요구량만으로는 측정 수명이 나오지 않습니다.** 세 중앙값을 더하면 12,900 + 3,600 + 1,440 = 17,940마이크로초로, 측정 수명 중앙값 99,801의 약 5분의 1입니다. 나머지 5분의 4는 기다림이어야 합니다. 시뮬레이션이 그만큼의 기다림을 만들어내는지는 설정과 파일의 부하에 따라 달라집니다.

**셋, 세는 단위가 다를 수 있습니다.** 충분함의 검증을 다룬 장에서 봤듯이 측정은 컴파일러 드라이버와 어셈블러와 보조 도구까지 계열 전체를 셌고, 동시에 사는 수가 최대 16이었습니다. archetype은 동시 실행 상한 8입니다.

> **미실행.** 이 두 통계를 시뮬레이션 결과와 측정으로 실제로 맞대본 적은 없습니다. 판정 기준으로 선언되어 있을 뿐입니다. 비교를 하려면 시뮬레이터가 자식의 수명과 동시 개수를 trace로 내야 하고, 앞의 세 어려움에 대해 "무엇과 무엇을 비교하는가"가 정해져야 합니다. 비교 통계를 어떻게 계산하는지는 harness를 다루는 권의 몫입니다.

## 11.9 여덟 칸을 한 장으로

따라온 길을 한 표로 모읍니다.

| 칸 | 내용 | 등급 | 원문·자료와 대조 |
|---|---|---|---|
| 출처 1 | 짧게 사는 자식이 대량으로 생긴다 | 첫째 | 확인함. 단 DynamoRio 빌드이고 커널 빌드가 아님 |
| 출처 1 | 2,430개 | 첫째 | 확인함. 같은 조건 |
| 출처 2 | 커널 빌드의 짧게 사는 프로세스 | 첫째 (원고) | 확인함. 예시는 cp, mkdir |
| 측정 | 자식 수 약 11,900, 수명 분포 모양 | 셋째 · 모양 | 요약 파일과 일치 |
| 측정 | 평균 CPU 약 90 ms | 셋째 · 절대값, 하한 | 요약 파일과 일치 |
| 산수 | CPU 중앙값 14.4 ms, 흩어짐 1.91 | 넷째 가정 위의 계산 | 검산 일치 |
| 관례 | 90 대 10 나누기 | 넷째 | 메모에 명시 |
| 관례 | 로그 정규 가족 | 넷째 | 메모에 명시 |
| 남은 임시값 | 디스크 대기 흩어짐 0.8 | 표시는 셋째, 실제는 근거 없음 | 확인 필요 |
| 숫자 | 첫째 자식 664 / 3,126 / 9 | compile 결과 | seed 103에서 재현됨 |
| 판정 | 수명 누적 분포, 동시 개수 | 선언됨 | 미실행 |

**한 항목의 숫자 몇 개가 이렇게 긴 사슬 끝에 있습니다.** 그리고 사슬의 칸마다 무엇이 확인됐고 무엇이 아닌지가 다릅니다.

이 표에서 가장 중요한 줄은 첫 줄입니다. 원문을 열기 전에는 **확인된 인용 문장**이었고, 원문을 열고 나서도 **문장은 맞았습니다.** 틀린 것은 그 문장이 **어떤 실험에서 나왔는가**라는 설명이었습니다. 인용 문장만 대조하면 이런 어긋남은 드러나지 않습니다. 앞뒤 문단을 읽어야 드러납니다.

---

## 11장 정리

- 컴파일러 자식 항목은 출처의 문장, 측정, 산수, 관례, 분포, 뽑힌 숫자, 사건의 흐름, 판정 기준까지 여덟 칸이 전부 차 있어서 끝까지 따라가기에 좋습니다.
- 첫 번째 출처의 인용 문장 "make forks and execs 2430 processes, mostly short-lived"는 원문에 글자 그대로 있습니다.
- 그런데 원문이 말하는 `make` workload는 Linux 커널 빌드가 아니라 DynamoRio 6.1.0을 `make -j8`로 빌드한 것입니다. 저장소 문서 여러 곳이 커널 빌드로 적고 있습니다.
- 이 어긋남은 부류의 존재 근거를 바꾸지 않습니다. 원문은 짧게 사는 프로세스가 많이 병렬로 도는 경우를 시험하려고 그 workload를 골랐다고 명시합니다. 바뀌는 것은 2,430이라는 개수의 뜻입니다.
- 원문도 동시 실행 상한 8로 돌렸다는 사실은 저장소에 적혀 있지 않습니다.
- 두 번째 출처는 커널 빌드가 맞지만, 짧게 사는 프로세스의 예로 든 것은 컴파일러가 아니라 `cp`와 `mkdir`입니다.
- 두 논문 모두 값을 주지 않고, 값은 전부 측정에서 옵니다. 커널 빌드 한 번에 컴파일러 계열 자식 약 11,900개, 수명 중앙값 약 100밀리초, 자식 하나의 평균 CPU 약 90밀리초이고, 평균 CPU는 샘플러가 짧은 자식을 놓쳐서 하한입니다.
- CPU 분포는 적률을 맞춰 만들었습니다. CPU 비율이 자식마다 같다는 가정으로 중앙값 14.4밀리초를 얻고, 평균이 90밀리초가 되도록 흩어짐 1.91을 풀었습니다. 검산하면 약 89밀리초가 나옵니다.
- 앞뒤를 90 대 10으로 나눈 것은 관례이고, 중앙값끼리만 성립합니다. 뽑힌 자식 하나하나에서는 뒤가 앞보다 길 수도 있습니다.
- 디스크 대기의 흩어짐 0.8은 측정 전 임시값이 남은 것으로, 근거가 적혀 있지 않습니다.
- 첫째 자식은 664, 3,126, 9마이크로초를 받았고, 이 값들은 분포에서 표준 정규의 −1.55, −0.18, −2.66 걸음쯤에서 뽑혔습니다. seed가 같으면 늘 같은 값이 나옵니다.
- 재현해야 할 수명 분포는 scheduling의 결과이고, 요구량의 합은 측정 수명의 약 5분의 1이며, 측정과 archetype이 세는 단위가 다를 수 있습니다. 비교는 아직 돌린 적이 없습니다.
- 인용 문장만 대조하면 이번 어긋남은 드러나지 않습니다. 앞뒤 문단을 읽어야 드러납니다.

---

# 12장 · 근거가 약한 자리

## 12.1 약한 자리를 모으는 이유

지금까지 장마다 근거가 약한 자리를 그때그때 표시했습니다. 이 장은 그것들을 **한곳에 모읍니다.** 그리고 성격에 따라 나눕니다.

```text
   1  판정할 기준이 없는 항목
   2  판정하면 순환이 되는 항목
   3  판정이 동어반복인 항목
   4  관례로 정한 값
   5  밝혀둔 근사
   6  선언은 됐는데 실현되지 않은 것
   7  적히지 않았던 것
```

1번부터 6번까지는 **저장소가 스스로 적어둔 약점**입니다. 7번은 이 권이 원문과 파일을 대조하면서 **새로 찾은 것**입니다. 둘의 차이가 이 장의 마지막 이야기입니다.

## 12.2 판정할 기준이 없는 항목: desktop-interactive

사람이 만지는 창을 흉내 내는 항목입니다. 판정란이 `none`이고, 구축 문서가 이유와 대응을 적어둡니다.

> "**Live-usage validation was not performed and is a stated limitation.** The collection + privacy-scrub tool (a CI-sidecar byproduct) ships in the artifact regardless, as an open falsification invitation: any user can run it against their own machine and check our synthetic distributions."

**실제 사용 중인 기계에서 검증하는 일은 하지 않았고, 그것은 밝혀둔 한계다.** 수집 도구와 개인정보 제거 도구는 결과물에 함께 싣는다. **공개된 반증 초대**다. 누구든 자기 기계에서 돌려서 우리의 합성 분포를 확인해볼 수 있다.

### 왜 판정할 수 없나

CI 서버에는 사람이 없습니다. 이 항목이 흉내 내는 것은 사람이 편집기 앞에서 치고 멈추고 생각하는 모양인데, 그걸 공개적으로 재현 가능하게 잴 방법이 없습니다. 그리고 측정을 다룬 장에서 봤듯이, 누가 어떤 프로그램을 언제 띄웠는지의 기록은 개인정보라서 공개된 것이 없습니다.

한때는 연구팀의 데스크톱에서 직접 재는 계획이 있었습니다. 2026년 8월 26일의 결정 기록은 그 계획을 버린 이유를 적습니다. 팀원 중 Linux 데스크톱을 쓰는 사람이 없었고, "나중에 검증하겠다"는 조건을 남겨두면 발표하는 결과가 계속 잠정적인 상태로 남는다는 것이었습니다. 그래서 **검증하지 않았다고 적는 쪽**을 골랐습니다.

### 이 항목에서 약한 곳을 전부 모으면

앞의 장들에서 이 항목에 대해 표시한 것을 모아봅니다.

| 무엇 | 약한 이유 |
|---|---|
| 키 입력 평균 238.66 ms | 옮겨 치기 과제이고, 5초 넘는 멈춤은 뺀 값이며, 여러 사람 평균을 한 사람 평균 자리에 썼다 |
| 막힘없음 158 ms | 원문에서는 로그 척도의 위치인데 평균이라는 이름으로 들어갔다 |
| 멈칫 확률 0.34 | 두 과제 중 한 과제의 값이고, 다른 과제에서는 0.73이었다 |
| 멈칫 평균 395 ms | 두 논문을 한 식에 넣은 산수. 원문의 짝이 되는 값은 약 253 ms |
| 흩어짐 0.35, 0.6 | 관례 |
| 입력 한 번의 계산 = 간격 × 균등 비율 | "창을 끄는 X는 0에서 100퍼센트"를 옮긴 것. interbench 코드는 경사로 흉내 낸다 |
| 입력 덩어리와 멈춤의 큰 구조 | 메모가 "바깥 심판이 없는 우리 모형"이라고 적었다 |

그리고 이것들이 합쳐져서 만드는 결과가 하나 있습니다. 항목의 필드를 볼 때 계산했듯이, 사람이 창을 만지는 동안 이 task는 **시간의 절반쯤을 계산에 씁니다.** `c1-compile`의 편집기는 56초 동안 약 28.5초를 계산합니다.

1권에서 편집기는 "하루 종일 켜놔도 CPU 사용률이 1퍼센트 안팎"인 대표적인 대화형 프로그램이었습니다. 1권의 설명과 이 archetype의 편집기 사이에 수십 배 차이가 있습니다.

그 차이가 어디서 오는지는 분명합니다. 입력 한 번의 계산량을 정한 출처가 interbench의 X이고, X는 **"한가하던 화면에서 창 하나를 잡고 끌어가는 상황"**을 흉내 냅니다. 창을 끄는 동안 화면은 계속 다시 그려집니다. 글자를 치는 편집기와 다릅니다. 입력 간격은 타자 연구에서, 입력 한 번의 무게는 창 끌기에서 가져와 한 항목에 붙였습니다.

> **미정.** 이 항목이 흉내 내야 할 것이 "가벼운 편집기"인지 "무거운 대화형 화면"인지가 문서에 정해져 있지 않습니다. 선택지는 셋입니다.
>
> **하나, 지금대로 둔다.** 장점은 interbench라는 커뮤니티 표준 모형의 범위를 그대로 따른다는 것이고, 대화형 task가 CPU를 두고 실제로 경쟁하게 되어 scheduler 설정의 차이가 드러나기 쉽습니다. 단점은 1권의 설명, 그리고 편집기라는 이름에서 떠올리는 행동과 멀다는 것입니다.
>
> **둘, 비율의 범위를 줄인다.** 예를 들어 0에서 0.1 사이로 둡니다. 장점은 편집기에 가까워진다는 것입니다. 단점은 그 범위에 근거가 되는 출처가 지금 저장소에 없다는 것이고, 대화형 task의 부하가 줄어서 파일마다 CPU 한 자리에 거는 부하를 다시 맞춰야 합니다.
>
> **셋, 이름별로 다른 비율 범위를 binding에서 준다.** 편집기는 가볍게, 영상 편집기는 무겁게. 장점은 현실에 가깝다는 것입니다. 단점은 archetype이 이름을 모른다는 경계 규칙은 지키지만, 범위마다 근거가 필요해져 근거의 빈칸이 늘어난다는 것입니다.
>
> 누가 정해야 하나: workload 데이터셋을 맡은 사람이 정할 수 있지만, 이 값이 파일마다 CPU 한 자리에 거는 부하를 크게 바꾸므로 측정의 두 번째 층을 돌리기 전에 정해야 합니다.

> **미실행.** 반증 초대로 공개하겠다는 **개인정보 제거 도구**가 저장소에 아직 없습니다. 측정에 쓴 프로세스 상태 샘플러(`dataset/tools/meas/proc_sampler.py`)는 있지만, 사람의 기계에서 모은 기록에서 개인정보를 지우는 부분은 코드로 찾아지지 않습니다. 구축 문서는 이 도구를 결과물에 "싣는다(ships)"고 현재형으로 적습니다. 결과물을 공개하기 전에 만들어져야 하는 것이고, 전제 조건은 무엇을 개인정보로 보고 지울지의 규칙입니다.

## 12.3 판정하면 순환이 되는 항목: game-task-chain

게임 항목의 판정란도 `none`입니다. 그런데 이유가 다릅니다.

> "validation against LAVD would be circular — LAVD is also the parameter source (stated as such, building-plan §7)."

LAVD와 비교해서 검증하면 순환이 된다. LAVD가 파라미터의 출처이기도 하기 때문이다.

### 순환이 무슨 뜻인가

게임 항목의 숫자는 LAVD 발표에서 가져왔습니다. task 300개, 실행 길이 260에서 1,650마이크로초. 그런데 "이 archetype이 실제 게임을 잘 흉내 내는가"를 판정할 기준으로 쓸 수 있는 자료도 LAVD 발표뿐입니다. 그러면 판정은 이렇게 됩니다.

```text
   질문     시뮬레이션한 게임에 task가 300개쯤 있나?
   기준     LAVD가 300개라고 했다
   결과     예. 우리가 300을 넣었으니까.
```

**문제를 낸 사람의 답안지로 채점하는 꼴입니다.** 통과는 보장되지만 아무것도 증명하지 않습니다.

그래서 저장소는 판정을 하지 않고, 판정할 수 없다고 적었습니다.

### 순환이 한 겹 더 있습니다

순환은 판정에서만 일어나지 않습니다. CPU 한 자리에 맞춰 게임의 부하를 줄이는 규칙에도 같은 출처가 쓰입니다. 구축 문서의 문장입니다.

> "`game-task-chain`'s defense: LAVD's own concentration statistics, top 30–40 tasks = 95% of scheduling"

게임 항목의 방어는 **LAVD 자신의 집중도 통계**다. 상위 30에서 40개가 scheduling의 95퍼센트를 차지한다.

그러니까 LAVD의 숫자로 파라미터를 채우고, LAVD의 다른 숫자로 그 파라미터를 줄이는 것을 정당화합니다. 두 번 쓰는 것 자체가 틀린 것은 아닙니다. 같은 발표의 관찰끼리 앞뒤가 맞는지 보는 셈입니다. 다만 **바깥에서 이 모형을 확인해줄 두 번째 목소리가 없다**는 사실은 그대로입니다.

### 이 항목에서 약한 곳을 전부 모으면

| 무엇 | 약한 이유 |
|---|---|
| 판정 | LAVD와 비교하면 순환 |
| 출처의 등급 | 발표 슬라이드. 숫자가 있어도 둘째 등급 |
| frame 주기 16,667 us | 슬라이드에 없음. 출처가 확인되지 않음 |
| 사슬 길이 16 | 원문의 "15에서 20개의 게임 task"에서 고른 값 |
| 사슬 모양 | 원문 그림의 여러 고리를 한 줄로 편 우리 해석 |
| 실행 길이 분포 | 두 예시를 5퍼센트와 95퍼센트 지점으로 본 우리 해석 |
| 나머지 284개의 값 | 슬라이드 표시가 붙은 우리 임시값 |
| 오래 사는 비율 0.90, 기다림에서 오는 비율 0.70–0.75 | 원문과 맞지만 compile 단계가 쓰지 않음 |
| task 수 300 | archetype 안의 개수. 모든 게임 파일에서 같음 |
| wineserver | 원문은 게임 그래프의 일부로 보는데 한가한 daemon으로 흉내 냄 |

**열두 항목 중 가장 긴 표입니다.** 그리고 이 항목이 이 연구에서 중요한 상황인 게임을 통째로 맡고 있습니다.

## 12.4 판정이 동어반복인 항목: 셋

판정란이 `self-consistency`인 셋, 소리 재생과 영상 재생과 끝날 때까지 계산하는 작업입니다.

이 셋은 판정이 **항상 통과합니다.** "50밀리초마다 깨어 CPU 5퍼센트를 쓰는가"를 확인하는데, 파일에 50밀리초와 2.5밀리초를 상수로 넣었으니 흩어짐 없이 늘 그렇게 됩니다.

그래도 이 판정이 아무 의미가 없지는 않습니다. **시뮬레이터나 compile 단계가 적은 대로 만들었는가**를 확인합니다. 파일에는 50밀리초라고 적었는데 compile 결과가 다른 값이 되는 실수는 이 판정으로 잡힙니다. 판정하는 대상이 "모형이 현실과 맞나"가 아니라 **"도구가 모형을 제대로 옮겼나"**입니다.

현실과 맞는지에 대해서는 출처가 스스로 한계를 밝힌 경우가 있습니다. interbench 설명서는 소리 재생 모형이 "잘 만든 오디오 프로그램이 했을 버퍼링을 무시한다"고 하고, 영상은 "60fps 재생으로는 꽤 무거운 편"이라고 합니다. **출처가 적어둔 한계가 그대로 이 archetype의 한계입니다.** 끝날 때까지 계산하는 작업의 출처인 Burn에는 그런 문장이 없는데, 모양이 "CPU를 완전히 쓴다" 하나뿐이라 한계를 적을 자리도 작습니다.

## 12.5 관례로 정한 값

출처도 측정도 말하지 않아서 이 연구가 정한 값들을 열두 항목에서 전부 모읍니다. 메모가 "ours", "our convention", "our modeling"으로 표시한 것들입니다.

### 흩어짐

| 항목 | 파라미터 | `sigma_log` | 메모의 표시 |
|---|---|---|---|
| `desktop-interactive` | 막힘없음 / 멈칫 | 0.35 / 0.6 | our convention |
| `build-orchestrator` | 자식 하나당 부모 계산 | 0.5 | our convention |
| `io-stream` | 덩어리 계산 / 디스크 대기 | 0.6 / 0.6 | our convention |
| `background-crawler` | 디스크 대기 | 0.6 | our convention |
| `network-bulk` | 조각 계산 / 네트워크 대기 | 0.5 / 0.5 | our convention |
| `game-task-chain` | 나머지 task의 쉼 / 계산 | 0.5 / 0.5 | our placeholder |
| `compiler-child` | 디스크 대기 | 0.8 | **표시 없음** |

측정이 비율이나 평균 하나만 줄 때, 분포의 흩어짐은 관례로 채웠습니다. 값이 0.5, 0.6, 0.8처럼 둥근 수인 것이 관례라는 표시이기도 합니다.

### 크기와 나누기

| 항목 | 무엇 | 값 |
|---|---|---|
| `io-stream` | 계산 덩어리의 크기 | 3 ms |
| `network-bulk` | 계산 조각의 크기 | 1 ms |
| `compiler-child` | 앞뒤 계산 나누기 | 90 대 10 |
| `build-orchestrator` | 동시 실행 상한 기본값 | 8 |
| `game-task-chain` | 사슬 길이 | 16 |
| `game-task-chain` | 나머지 task의 쉼과 계산 | 500 ms, 200 µs |

### 해석과 모양

| 항목 | 무엇 |
|---|---|
| 전체 | 분포 가족을 로그 정규로 |
| 전체 | 프로그램의 순서, 필드 이름 |
| `desktop-interactive` | 입력 한 번의 계산을 직전 간격의 균등 비율로 |
| `desktop-interactive` | 두 논문의 숫자로 섞임 분포의 빈칸을 채우기 |
| `compiler-child` | CPU 비율이 자식마다 같다는 가정 |
| `game-task-chain` | 두 예시를 5퍼센트와 95퍼센트 지점으로 |
| `game-task-chain` | 그래프를 한 줄 사슬로 |
| `electron-comms` | 불규칙한 깨어남을 정확한 주기 TIMER로 |
| `system-daemon` | 주기가 없는 깨어남을 SLEEP으로 |

### 이 목록이 말하는 것

**열두 항목 중 넷째 등급의 값이 하나도 없는 항목은 없습니다.** 가장 단순한 `cpu-batch`조차 "thread 4개 구조를 가져오지 않는다"는 결정이 있습니다.

그리고 넷째 등급의 값이 결과를 얼마나 바꾸는지는 값마다 다릅니다. 연속 입출력의 덩어리를 3밀리초로 하든 6밀리초로 하든 CPU 비율은 같지만, scheduler가 보는 "한 번 깨어나 얼마나 일하나"는 두 배가 됩니다. 사람이 만지는 창의 비율 범위는 부하를 열 배 넘게 바꿀 수 있습니다.

> **미정.** 관례로 정한 값들이 결과를 얼마나 흔드는지 확인할지가 정해져 있지 않습니다. 저장소의 계획에는 분포 가족을 바꿔보는 분석이 자연스러운 workload 묶음의 구간 길이에 대해서만 적혀 있고, 이 장의 표에 있는 값들을 바꿔보는 분석은 없습니다. 선택지는 셋입니다.
>
> **하나, 부하를 크게 바꾸는 관례만 바꿔 본다.** 입력 한 번의 계산 비율, 덩어리 크기, 동시 실행 상한, 사슬 길이를 각각 늘리고 줄여 compile하고, RQ0 gate의 판정이 바뀌는지 봅니다. 장점은 "이 관례는 결론에 무해하다"를 값마다 말할 수 있게 된다는 것입니다. 단점은 gate를 여러 번 돌리는 비용이고, 늘리고 줄이는 폭 자체에 또 근거가 필요합니다.
>
> **둘, 관례 전체를 한꺼번에 흔드는 한 번의 분석만 한다.** 장점은 비용이 작다는 것입니다. 단점은 판정이 바뀌었을 때 어느 값 때문인지 알 수 없다는 것입니다.
>
> **셋, 분석하지 않고 한계 절에 관례로 적는 것으로 끝낸다.** 장점은 지금 계획을 바꾸지 않는다는 것입니다. 단점은 심사자가 "그 값이 결론을 바꾸지 않는다는 근거가 있나"라고 물으면 답이 없다는 것입니다.
>
> 누가 정해야 하나: RQ0 gate의 판정 절차는 결과를 보기 전에 얼려두는 것이 원칙이므로, 분석을 넣는다면 gate를 돌리기 전에 세 사람이 함께 정해야 합니다.

## 12.6 밝혀둔 근사

항목 자체는 맞는데, **어떤 실제 프로그램을 그 항목에 묶은 것**이 근사인 경우입니다.

| 묶음 | 근사의 내용 | 표시한 곳 |
|---|---|---|
| 화상 회의 → `video-playback` | 압축과 네트워크 부분이 빠짐 | archetype 메모 |
| `wineserver` → `system-daemon` | 원문은 게임 그래프의 일부로 봄 | archetype 메모 ("provisional") |
| `gamescope` → `video-playback` | 화면 합성기를 영상 재생으로 | timeline 파일의 주석 |
| Discord, Slack → `electron-comms` 값 | 로그인하지 않은 Element로 잼 | archetype 메모 |
| `tracker-miner-fs-3` → `cpu-batch` | 전체 재색인 상태만 흉내 냄 | archetype 메모 |
| Firefox 탭 수 | Chromium의 구조를 그대로 씀 | 구축 문서 ("stated approximation") |

`gamescope` 줄의 표시가 흥미롭습니다. archetype이 아니라 **timeline 파일에** 주석으로 적혀 있습니다.

```yaml
# gamescope -> video-playback: frame-periodic compositor approximation (ours).
```

화면 합성기를 frame 주기로 도는 영상 재생으로 근사한 것이고, 우리 것이다. binding에서 생긴 근사는 binding이 적힌 곳에 적은 것입니다.

그리고 사람이 없을 때의 시스템 프로세스 다섯 중 `gnome-shell`, `Xorg`, `pipewire`를 서버 daemon의 측정값으로 흉내 내는 것은, 측정을 다룬 장에서 봤듯이 **어디에도 근사라고 적혀 있지 않습니다.**

## 12.7 선언은 됐는데 실현되지 않은 것

파일에 적혀 있고 출처나 규칙도 있는데, 실제 workload에는 반영되지 않는 것들입니다. 장마다 **확인 필요**로 적어둔 것을 모읍니다.

```text
   게임 항목의 오래 사는 비율과 기다림 비율
     → 파일에 있고 원문과 맞지만 compile 단계가 읽지 않는다

   끝이 없는 반복 셋의 "반복마다 뽑는다"
     → compile 단계가 task마다 한 번으로 바꾼다

   background-crawler
     → 부류의 근거와 측정값이 다 있는데 어떤 timeline도 쓰지 않는다

   category_source의 값 검사
     → 계획은 기계로 확인한다고 하고 검사 도구는 필드의 존재만 본다

   정적 개수의 출처 표시
     → 계획은 출처 표시가 붙는다고 하고 timeline에는 적을 자리가 없다

   조합이 측정을 재현하는지의 판정
     → 기준으로 선언됐고 돌린 적이 없다
```

이것들은 **틀린 값**이 아닙니다. 적힌 약속과 실제 동작 사이의 틈입니다. 그리고 틈은 둘 중 한쪽으로 닫힙니다. 약속을 지키도록 도구를 고치거나, 실제 동작에 맞게 약속을 고치거나.

## 12.8 적히지 않았던 것

마지막 묶음이 이 장에서 가장 중요합니다. 이 권이 원문을 열고 파일을 compile하면서 **새로 찾은 것**입니다. 저장소 어디에도 약점으로 적혀 있지 않았습니다.

```text
   컴파일 자식 수 2,430의 출처 workload
     저장소: Linux 커널 빌드
     원문:   DynamoRio 6.1.0 빌드

   두 번째 컴파일 논문의 짧게 사는 프로세스
     저장소: 커널 빌드의 짧게 사는 프로세스, 컴파일러 자식을 보조
     원문:   cp와 mkdir

   게임 frame 주기 16.7 ms
     저장소: LAVD 발표가 출처
     원문:   슬라이드에 없음

   키 입력 막힘없음 158 ms
     저장소: 성분의 평균
     원문:   로그 척도의 위치

   컴파일 자식의 디스크 대기 흩어짐 0.8
     저장소: 측정이 출처
     기록:   측정 전 임시값이 남음

   ananicy의 type
     저장소: 말 그대로 archetype 분류 체계
     원문:   처방의 분류. 한 분류에 행동이 다른 것들이 함께 있음

   컴파일 동시 실행 상한
     저장소: 8, 관례
     원문:   부류의 근거 논문이 이미 -j8로 돌렸음
     측정:   동시에 사는 컴파일러 계열 프로세스는 최대 16
```

### 적힌 약점과 적히지 않은 약점

앞 절들의 약점과 이 절의 약점을 나란히 놓으면 차이가 보입니다.

**적힌 약점은 찾기 쉬웠습니다.** 메모에 "ours", "convention", "provisional", "stated limitation"이라고 적혀 있어서 그 단어를 따라가면 나왔습니다. 이 권이 관례의 표를 만들 수 있었던 것도 메모가 일관되게 표시해뒀기 때문입니다.

**적히지 않은 약점은 원문을 열어야 나왔습니다.** 그리고 대부분 **확인된 것으로 표시된 자리**에 있었습니다. O'Callahan 논문은 인용 문서에 `verified`로 적혀 있고, 인용 문장도 원문과 글자 그대로 맞았습니다. 틀린 것은 그 문장 앞 문단에 있던 workload의 정체였습니다.

```text
   적힌 약점                         적히지 않은 약점
   ─────────                         ──────────────
   읽는 사람이 알고 읽는다              읽는 사람이 믿고 읽는다
   논문에서 한계로 쓸 수 있다           심사자가 찾으면 결함이 된다
   고칠지 말지를 정할 수 있다           고칠 대상인 줄도 모른다
```

4권에서 실패가 예상되는 경계 사례의 묶음인 Family 5를 다루면서 "심사자가 찾아내기 전에 적어두면 한계이고, 찾아낸 뒤에 인정하면 결함"이라는 문장이 있었습니다. 이 장의 결론이 같습니다. **적어둔 약점은 약점이지만, 적히지 않은 약점은 결함입니다.**

### 그래서 적어두는 것이 값을 합니다

약점을 적어두는 규칙이 이 권에서 실제로 무엇을 했는지 정리하면 이렇습니다.

**첫째, 등급을 매길 수 있게 했습니다.** 메모가 없었다면 모든 숫자가 출처 표시만 보고 같은 무게로 읽혔을 것입니다.

**둘째, 원문을 열어볼 자리를 좁혀줬습니다.** 메모가 "이 논문에서는 존재만 가져왔다"고 정확히 적어둔 덕에, 원문에서 무엇을 확인해야 하는지가 분명했습니다. 2,430이 부류의 근거로만 쓰였다는 메모가 정확했기 때문에, workload의 정체가 달라도 **archetype의 값은 하나도 틀리지 않았다**고 말할 수 있습니다.

**셋째, 고칠 수 있는 형태로 남겼습니다.** 계획 문서가 말한 대로 두 종류의 메모가 "과장을 막는 난간"입니다. 난간이 있는 곳에서는 떨어질 뻔한 자리가 보이고, 난간이 없는 곳에서만 실제로 떨어집니다. 이 권이 찾은 것들도 대부분 난간을 한 칸 더 세우면 되는 것들입니다.

> **논문으로.** 이 장의 내용이 논문의 한계 절에 들어갈 문장들을 정합니다. 적어도 이 셋은 들어가야 합니다.
>
> ```text
>    "Interactive-task behavior has no behavioral referee; live-usage
>     validation was not performed."
>
>    "Gaming-task parameters and their single-lane scaling both derive
>     from one characterization, so they cannot be validated against it."
>
>    "Where sources supply only means or ratios, distribution spreads
>     and granularities are stated conventions."
> ```
>
> 그리고 이 권이 찾은 적히지 않은 약점들은 **논문을 쓰기 전에** 저장소에서 먼저 정리되어야 합니다. 특히 2,430의 workload와 frame 주기의 출처는 심사자가 원문을 열면 곧바로 보이는 자리입니다.

## 12.9 손으로 따라가기: 게임 파일 하나의 약점 지도

게임 상황만 담은 `c1-gaming` 파일을 열어서, task마다 **가장 약한 고리**를 찾아봅니다.

```yaml
tasks:
  - {id: game, name: game.exe, archetype: game-task-chain,
     arrive: 0s, depart: 60s, bind: {lane_share: 0.9}}
  - {id: steam, name: steam, archetype: electron-comms,
     arrive: 0s, depart: 60s}
  - {id: webhelper, name: steamwebhelper, archetype: electron-comms,
     arrive: 0s, depart: 60s, count: 3}
  - {id: wine, name: wineserver, archetype: system-daemon,
     arrive: 0s, depart: 60s}
  - {id: compositor, name: gamescope, archetype: video-playback,
     arrive: 0s, depart: 60s}
```

인식기는 이 파일에서 `game.exe × 300`, `steam`, `steamwebhelper × 3`, `wineserver`, `gamescope`를 봅니다. 인식기 쪽에서는 문제가 없습니다. 이름이 전부 5권에서 본 상황 S9의 이름입니다. 문제는 **executor가 받는 행동** 쪽입니다.

### game.exe × 300

```text
   사슬 16개   첫 task가 16,667 us마다 TIMER, 차례로 WAKE
   나머지 284개  SLEEP 약 0.5 s → RUN 약 200 us
```

**가장 약한 고리: frame 주기.** 사슬 전체의 박자를 정하는 값인데 출처로 표시된 발표에 없습니다. 박자가 60 FPS가 아니라 발표 슬라이드의 예시 게임처럼 40 FPS 근처였다면, 같은 부하를 더 긴 주기에 나눠 요구했을 것입니다.

그리고 판정은 순환입니다.

### steam, steamwebhelper × 3

```text
   electron-comms   TIMER 중앙값 1.85 s → RUN 중앙값 289 us
```

**가장 약한 고리: 대신 잰 앱.** 값은 로그인하지 않은 채팅 앱에서 왔습니다. 게임 플랫폼의 화면 프로세스가 게임 도중 무엇을 하는지는 측정되지 않았습니다. 다만 부하가 워낙 작아서, 이 약점이 결과에 주는 영향도 작습니다.

### wineserver

```text
   system-daemon   이 파일에서 뽑힌 값: SLEEP 1,225,245,899 us → RUN 97 us
```

**가장 약한 고리: 묶음 자체.** 원문 슬라이드 13이 "260마이크로초짜리 조율 task"로 콕 집어 말한 wineserver가, 이 파일에서는 **1,225초에 한 번** 깨도록 뽑혔습니다. 60초 파일에서 한 번도 깨지 않습니다. 사실상 이름만 있는 task입니다. 메모는 이 묶음을 "provisional"로 표시해뒀습니다.

### gamescope

```text
   video-playback   TIMER 16,667 us → RUN 6,667 us
```

**가장 약한 고리: 근사.** 화면 합성기가 frame마다 영상 재생만큼, 즉 CPU 40퍼센트를 쓴다고 흉내 냅니다. timeline 주석이 "(ours)"라고 적었습니다. interbench의 영상 모형 스스로 "60fps 재생으로는 꽤 무거운 편"이라고 한 값이, 여기서는 게임 옆의 화면 합성기에 붙었습니다.

### 모아보면

| task | 가장 약한 고리 | 성격 | 부하에 주는 영향 |
|---|---|---|---|
| `game.exe` 사슬 | frame 주기의 출처 없음, 판정 순환 | 적히지 않음 + 적힘 | 큼. lane의 90퍼센트를 요구하도록 맞춰짐 |
| `game.exe` 나머지 | 임시값 | 적힘 | 작음 |
| `steam` 계열 | 대신 잰 앱 | 적힘 | 작음 |
| `wineserver` | 잠정 묶음, 사실상 안 깸 | 적힘 | 거의 없음 |
| `gamescope` | 합성기를 영상 재생으로 | 적힘 | 큼. CPU 40퍼센트 |

이 파일을 compile하면 CPU 한 자리 기준의 요구량이 **약 146퍼센트**로 나옵니다. 그중 대부분이 사슬의 90퍼센트와 합성기의 40퍼센트입니다.

**부하를 크게 좌우하는 두 task가 둘 다 근거의 약한 고리를 갖고 있습니다.** 하나는 박자를 정하는 값의 출처가 확인되지 않았고, 하나는 근사입니다. 이 파일로 잰 결과를 읽을 때 이 두 줄을 함께 기억해야 합니다.

---

## 12장 정리

- 근거가 약한 자리는 일곱 종류로 나뉩니다. 판정 기준이 없는 것, 판정이 순환인 것, 판정이 동어반복인 것, 관례로 정한 값, 밝혀둔 근사, 선언만 되고 실현되지 않은 것, 그리고 적히지 않았던 것입니다.
- 사람이 만지는 창은 실제 사용 중인 기계로 검증하지 않았고, 대신 반증 도구를 공개하기로 했습니다. 그 개인정보 제거 도구는 아직 저장소에 없습니다.
- 그 항목은 타자 연구의 입력 간격에 창 끌기의 계산 무게를 붙여서, 사람이 창을 만지는 동안 시간의 절반을 계산합니다. 무엇을 흉내 내야 하는지가 정해져 있지 않습니다.
- 게임 항목은 파라미터의 출처와 판정 기준이 같은 발표라서 판정하면 순환이 되고, CPU 한 자리에 맞추는 규칙의 방어도 같은 발표에서 옵니다. 약한 곳의 목록이 열두 항목 중 가장 깁니다.
- 소리 재생, 영상 재생, 계산만 하는 작업의 판정은 항상 통과합니다. 모형이 현실과 맞는지가 아니라 도구가 모형을 제대로 옮겼는지를 확인합니다.
- 열두 항목 모두에 관례로 정한 값이 있습니다. 흩어짐, 덩어리 크기, 나누는 비율, 상한, 사슬 길이, 분포 가족, 해석이 여기 들어가고, 이 값들을 바꿔보는 민감도 분석은 계획에 없습니다.
- 실제 프로그램을 항목에 묶는 근사가 여섯 곳 적혀 있고, 데스크톱의 화면과 소리 서버를 서버 daemon으로 흉내 내는 것은 적혀 있지 않습니다.
- 선언은 됐는데 실현되지 않은 것들은 틀린 값이 아니라 약속과 동작 사이의 틈입니다.
- 이 권이 원문을 열어 새로 찾은 약점은 대부분 확인된 것으로 표시된 자리에 있었습니다. 적어둔 약점은 약점이고, 적히지 않은 약점은 결함입니다.
- 메모가 약점을 일관되게 적어둔 덕에 등급을 매길 수 있었고, 원문에서 확인할 자리가 좁혀졌고, 출처의 workload가 달라도 archetype의 값은 틀리지 않았다고 말할 수 있었습니다.
- 게임 파일 하나에서 부하를 크게 좌우하는 두 task가 둘 다 약한 고리를 갖고 있습니다. 사슬의 박자는 출처가 확인되지 않았고, 화면 합성기는 근사입니다.

---

# 13장 · 용어 정리

이 권에서 나온 용어를 모았습니다.

## archetype의 바탕

| 용어 | 뜻 |
|---|---|
| **archetype** | scheduler가 보는 모습대로 적은 프로세스 하나의 생성 모형. 사건의 흐름을 만들어내는 규칙과 파라미터의 묶음 |
| **event stream** | 시각과 사건이 이어진 흐름. scheduler에게 프로세스는 이것이 전부다 |
| **generative model** | 데이터를 요약한 것이 아니라 데이터를 만들어낼 수 있는 규칙 |
| **task** | scheduler가 실행 여부를 결정하는 단위 하나. 대개 thread 하나 |
| **lane** | 이 연구의 시뮬레이터가 가진 CPU 자리 하나. 한 번에 한 task만 앉는다 |
| **executor** | 시뮬레이터 안에서 scheduling 알고리즘을 실제로 돌리는 부분 |
| **binding** | 프로세스 이름과 archetype을 짝지어주는 것. timeline이나 상황 목록에서 일어난다 |
| **timeline** | 사람이 손으로 쓰는 workload 설계 파일. 시간축 위에 구간과 라벨과 task를 놓는다 |
| **trace** | 실행 중에 일어난 사건을 시각 순서로 기록한 것 |
| **Layer 1 · 2 · 3** (데이터셋) | 데이터셋을 쌓는 세 층. archetype, 상황 목록, timeline. 행동 숫자는 첫 층에만 있다 |
| **Layer 1 · 2** (측정) | 4권의 측정 두 층. 인식 정확도와 설정의 효과. 데이터셋의 층과 이름만 같다 |

## 여섯 primitive

| 용어 | 뜻 |
|---|---|
| **primitive** | 더 쪼갤 수 없는 기본 동작. archetype의 프로그램을 이루는 명령 |
| **RUN** | 정해진 양의 CPU를 태운다. 길이는 CPU 요구량이지 벽시계 시간이 아니다 |
| **SLEEP** | 지금부터 정해진 시간 동안 잔다. 상대 시간 |
| **TIMER** | 처음부터 정해진 눈금 t₀ + k·period에 깨어난다. 절대 시간. 늦으면 밀린 일이 쌓인다 |
| **WAIT** | 사건이 올 때까지 기다린다. 무엇을 기다리는지를 channel로 적는다 |
| **WAKE** | 다른 task를 실행 가능한 상태로 만든다 |
| **FORK** | spawn table의 다음 자식을 task로 만든다 |
| **EXIT** | 이 task를 끝낸다 |
| **channel** | WAIT가 기다리는 대상의 이름. `input`, `upstream`, `children`처럼 깨워주는 쪽이 있는 것과, `disk`, `io`, `net`처럼 정해진 길이의 멈춤으로 바뀌는 것이 있다 |
| **backlog** | 처리하지 못하고 밀린 일이 쌓인 상태 |
| **spawn table** | 부모가 만들 자식들의 프로그램을 미리 적어둔 순서 있는 목록 |
| **loop** | 반복. 제어 흐름일 뿐 primitive가 아니다 |

## 항목의 필드

| 용어 | 뜻 |
|---|---|
| **`category_source`** | 이 부류가 존재한다는 근거를 어느 분류 체계에서 거둬왔나. 없으면 `meas` |
| **`pattern`** | primitive로 쓴 프로그램 |
| **`params`** | 숫자 파라미터들. 하나하나가 분포이고 출처 표시가 붙는다 |
| **`sampling`** | 값을 얼마나 자주 새로 뽑나. `per-instance`, `per-task`, `per-iteration` |
| **`per-instance`** | 자식 task 하나마다 한 번 |
| **`per-task`** | task마다 한 번 뽑아 모든 반복에 재사용 |
| **`per-iteration`** | 반복마다 새로 뽑는다. 끝이 정해진 반복일 때만 허용된다 |
| **`lifetime`** | task가 어떻게 끝나나. `segment-bound`, `finite`, `spawned` |
| **`segment-bound`** | 사용자가 닫을 때 끝난다. 끝나는 시각이 파일에 박혀 있다 |
| **`finite`** | 프로그램이 EXIT에 닿을 때 끝난다. 그 시각은 scheduling의 결과다 |
| **`spawned`** | 실행 중에 FORK로 태어나 EXIT으로 끝난다 |
| **`spawns` / `spawned_by`** | 누가 누구를 자식으로 만드나 |
| **`binding_params`** | 쓰는 쪽이 채워야 하는 손잡이의 이름. 값은 적지 않는다 |
| **`total_work`** | 계산 작업의 전체 크기. timeline이 채운다 |
| **`spawn_count`** | 부모가 만들 자식 수. timeline이 채운다 |
| **`parallelism_cap`** | 동시에 살아 있을 수 있는 자식 수의 상한. 기본값 8은 관례 |
| **`lane_share`** | 게임 사슬이 CPU 한 자리의 몇 할을 요구하게 맞출지. timeline이 채운다 |
| **`scalable`** | CPU 한 자리에 맞추려고 compile 단계가 바꿔도 되는 값과 그 규칙. 게임 항목에만 있다 |
| **`validation_stats`** | 재현해야 할 통계, 또는 판정할 수 없는 이유 |
| **referee** | 통계가 맞는지 판정해줄 기준. `meas-ci`, `self-consistency`, `none` |
| **`self-consistency`** | 바깥 기준 없이 적은 대로 만들어졌는지만 보는 판정 |
| **`modeling_notes`** | 출처 위에 우리가 무엇을 지어냈나를 적는 메모 |
| **`notes`** (출처 등록부) | 출처가 무엇을 확립하고 어디까지가 범위인지를 적는 메모 |

## 분포

| 용어 | 뜻 |
|---|---|
| **`constant`** | 흩어짐 없이 늘 같은 값 |
| **`uniform`** | 두 값 사이에서 어느 값이나 똑같이 나올 수 있는 분포 |
| **lognormal** | 로그 정규 분포. 로그를 취하면 정규 분포가 되는 값이고, 중앙값의 몇 배로 흩어진다. 평균이 중앙값보다 크다 |
| **`median_us`** | 로그 정규의 중앙값. 마이크로초 |
| **`sigma_log`** | 로그 척도의 표준편차. 1을 넘으면 꼬리가 아주 길다 |
| **anchor** | 분포를 양 끝 두 값으로 정하는 방식. 게임 항목은 두 값을 5퍼센트와 95퍼센트 지점으로 본다 |
| **`lognormal-mixture`** | 로그 정규 둘을 확률로 섞은 분포 |
| **`family-declaration`** | 값을 뽑지 않고 분포의 가족만 선언하는 줄 |
| **moment matching** | 적률 맞추기. 측정한 평균 같은 요약값이 그대로 나오도록 분포의 파라미터를 거꾸로 푸는 것 |
| **CDF** | 누적 분포. 값이 x 이하일 비율을 x마다 그린 곡선 |

## 출처와 등급

| 용어 | 뜻 |
|---|---|
| **source tag** | 숫자에 붙는 출처 표시. `id` 또는 `id:locator` |
| **locator** | 출처 안의 위치. `man-audio`, `s12`, `sec-4.3`, `cli:3` 같은 것 |
| **`locator_pattern`** | 출처마다 허용하는 locator의 모양. 검사 도구가 확인한다 |
| **scholarly** | 학술 문헌. 정해진 역할 안에서 행동과 통계에 대한 주장을 뒷받침한다 |
| **deployed-system** | 배포된 소프트웨어의 문서, 저장소, 발표. 존재 주장만 뒷받침한다 |
| **measurement** | 우리 측정. 구조와 모양에 대한 주장만 뒷받침한다 |
| **convention informed by measurement** | 측정으로 보강한 관례. 기계에 따라 달라지는 절대값의 등급 |
| **`verified` · `to-pin` · `provisional`** | 인용이 확인된 정도. 그 문서가 맞는지를 말하고, 그 문서가 우리 내용을 말하는지는 말하지 않는다 |
| **harvesting** | 수확. 이미 자기 분류를 정의해둔 출처에서 부류를 거둬오는 것. 부류의 존재를 닫는 방법. 계획 문서의 Tier 1 |
| **verification** | 검증. 목록의 조합이 측정을 재현하는지 보는 것. 목록의 충분함을 닫는 유일한 방법. 계획 문서의 Tier 2 |
| **spanning** | 목록의 조합으로 상황 목록 S1부터 S18까지를 만들 수 있다는 주장 |
| **taxonomy** | 분류 체계 |

## 개수

| 용어 | 뜻 |
|---|---|
| **multiplicity** | 다중성. 같은 종류가 몇 개 떠 있는가 |
| **emergent multiplicity** | 창발적 다중성. 개수를 적지 않고 부모의 파라미터를 적어서, 개수의 시간 변화가 시뮬레이션에서 나오게 한다 |
| **static multiplicity** | 정적 다중성. scheduling과 무관한 개수를 파일에 직접 적는다 |
| **churn** | 들고남. 프로세스가 태어나고 죽으면서 이름 집합이 바뀌는 것 |

## 측정

| 용어 | 뜻 |
|---|---|
| **meas-ci** | 이 연구가 공개 CI 서버에서 실제 프로그램을 돌려 잰 측정 캠페인. 출처 id이기도 하다 |
| **meas-pending** | 측정 대기 표시. 얼린 뒤에는 검사 도구가 거절한다. 지금 archetype 파일에는 남아 있지 않다 |
| **CI 서버** | 코드가 바뀔 때마다 자동으로 시험을 돌려주는 빌려 쓰는 기계 |
| **sidecar** | 본체 옆에 붙어 함께 돌면서 기록하는 도구 |
| **Xvfb** | 모니터 없는 기계에서 GUI 프로그램이 그릴 곳을 소프트웨어로 흉내 내는 가짜 화면 서버 |
| **runner spec** | 측정한 CI 서버의 사양 기록. 코어 수, CPU 모델, 메모리, 운영체제 |
| **cold cache** | 운영체제의 파일 캐시를 비운 상태. 디스크를 실제로 읽게 만든다 |
| **daemon** | 사용자가 직접 실행하지 않았는데 뒤에서 늘 도는 시스템 프로그램 |

## 열두 archetype

| 가족 | archetype | 흉내 내는 것 | 판정 |
|---|---|---|---|
| periodic-interactive | **`audio-playback`** | 소리 재생 | self-consistency |
| | **`video-playback`** | 영상 재생, 화면 합성, 화상 회의의 영상 | self-consistency |
| | **`desktop-interactive`** | 사람이 만지는 창 | none |
| compute/batch | **`cpu-batch`** | 끝날 때까지 계산만 하는 작업 | self-consistency |
| | **`compiler-child`** | 컴파일러 자식 하나 | meas-ci |
| | **`build-orchestrator`** | 컴파일을 지휘하는 부모 | meas-ci |
| IO | **`io-stream`** | 연속으로 읽고 쓰기 | meas-ci |
| | **`background-crawler`** | 뒤에서 천천히 훑는 색인기 | meas-ci |
| structural-special | **`game-task-chain`** | 게임 하나 | none |
| meas | **`network-bulk`** | 회선을 꽉 채우는 다운로드 | meas-ci |
| | **`electron-comms`** | 대부분 쉬다가 가끔 깨는 앱, 브라우저 탭 | meas-ci |
| | **`system-daemon`** | 거의 쉬는 시스템 서비스 | meas-ci |

## 이 권에서 원문을 연 출처

| 출처 id | 무엇 | 등급 | 이 권에서 |
|---|---|---|---|
| **`interbench`** | 대화형 반응성 벤치마크 | deployed-system | 설명서와 소스 코드를 읽음 |
| **`rt-app`** | JSON으로 적는 주기 부하 도구 | deployed-system | 설명서를 읽음 |
| **`lavd-ossna24`** | 게임 scheduler 발표 슬라이드 | deployed-system | 슬라이드 30장을 읽음 |
| **`corbet-lwn24`** | 위 발표를 다룬 LWN 기사 | deployed-system | 읽음 |
| **`ananicy-rules`** | 프로세스 이름별 우선순위 카탈로그 | deployed-system | 커밋 `03ef03fb`에서 항목을 찾음 |
| **`dhakal-chi18`** | 키 입력 대규모 분석 | scholarly | 저자 공개 PDF를 읽음 |
| **`roeser-rw24`** | 타자 막힘의 섞임 모형 | scholarly | 기관 저장소의 저자 원고를 읽음 |
| **`ocallahan-atc17`** | 기록·재생 디버거 논문 | scholarly | 학회판과 확장판을 읽음 |
| **`coetzee-arxiv12`** | 빌드 시스템 논문 원고 | scholarly | arXiv 원고를 읽음 |
| **`dubroy-chi10`** | Firefox 탭 사용 연구 | scholarly | 저자 공개 PDF를 읽음 |
| **`mozilla-testpilot10`** | Firefox 사용자 탭 기록 | deployed-system | 집계 안내 페이지와 분석 기사를 읽음 |
| **`chang-chi21`** | 탭 부담 조사 | scholarly | 읽지 못함 |
| **`cpsmark-tbench23`** | 사무용 데스크톱 벤치마크 논문 | scholarly | 읽지 못함 |
| **`meas-ci`** | 우리 측정 | measurement | 요약 파일, 분석 코드, release 원자료의 사양 파일을 읽음 |

## 주의할 표기

| 표기 | 주의할 점 |
|---|---|
| **Tier 1 · Tier 2** | 계획 문서의 존재 근거와 충분함 근거. 인용의 등급(scholarly, deployed-system)과 다른 말이다 |
| **`fluent_mean_us`** | 이름은 평균이지만 원문의 158 ms는 로그 척도의 위치다 |
| **2,430** | 원문에서는 DynamoRio 6.1.0 빌드의 값. 저장소 문서는 커널 빌드로 적는다 |
| **`meas-ci:cli:3`** | 명령줄 측정의 세 번째 실행. 반복 다섯 개를 담고 있다. 세 번째 반복이 아니다 |
| **`ananicy` · `ananicy-rules`** | 원래 Ananicy와 CachyOS 카탈로그. 대문자 분류 이름은 뒤쪽 것이다 |

---

## 이 권을 다 읽었으면

**바탕 확인**

- scheduler에게 프로세스가 무엇인지 한 문장으로 말하고, 그래서 archetype에 들어갈 수 없는 셋을 댈 수 있다.
- archetype이 이름을 모른다는 규칙이 이름만 바꾼 한 쌍의 파일을 어떻게 가능하게 하는지 설명할 수 있다.
- archetype의 숫자가 인식 정확도가 아니라 설정의 효과를 재는 층에 영향을 주는 이유를 말할 수 있다.
- 행동 숫자가 데이터셋의 첫 층에만 있다는 규칙을 데이터베이스 정규화에 빗대어 설명할 수 있다.

**primitive 확인**

- 여섯 primitive를 나열하고 각각을 1권의 상태 전이에 겹쳐 말할 수 있다.
- RUN의 길이가 벽시계 시간이 아니라 CPU 요구량이라는 것이 무슨 뜻인지 예를 들 수 있다.
- 주기 작업을 SLEEP으로 적으면 나쁜 설정 아래에서 무슨 일이 생기는지 숫자로 보일 수 있다.
- 시스템 daemon은 왜 일부러 SLEEP으로 적었는지 말할 수 있다.
- 디스크를 기다리는 WAIT가 시뮬레이터에서 무엇으로 바뀌는지와 그 이유를 말할 수 있다.

**정의와 필드 확인**

- archetype을 정의하는 세 단계를 말하고, 음악 재생 항목으로 세 단계를 따라갈 수 있다.
- archetype의 정체가 코드가 아니라 통계라는 말의 뜻과 그 이점을 설명할 수 있다.
- 판정 기준의 세 종류를 말하고 각각에 속하는 항목을 댈 수 있다.
- 로그 정규 분포의 두 파라미터를 설명하고, 평균이 중앙값보다 큰 이유를 말할 수 있다.
- 값을 뽑는 빈도 세 가지를 말하고, 반복마다 뽑기가 왜 끝이 정해진 반복에서만 허용되는지 설명할 수 있다.
- 출처 등록부의 메모와 archetype의 메모가 각각 무엇을 적는지, 출처 표시가 필드 이름을 정당화하지 않는다는 규칙이 무슨 뜻인지 말할 수 있다.

**등급 확인**

- 근거의 네 등급을 말하고, 각 등급이 뒷받침할 수 있는 문장과 없는 문장을 하나씩 들 수 있다.
- 배포된 소프트웨어의 숫자를 파라미터로 쓸 때 주장이 어떻게 바뀌는지 설명할 수 있다.
- 산수가 등급을 낮추는 이유를 키 입력 간격의 멈칫 평균으로 설명할 수 있다.
- 측정 표시가 두 숫자에 붙어 있어도 측정이 뒷받침하는 것은 둘의 비율 하나일 수 있다는 것을 예로 보일 수 있다.

**목록 확인**

- 열두 archetype을 다섯 가족으로 나눠 나열할 수 있다.
- 파일 색인기가 한 파일에서는 `cpu-batch`이고 다른 곳에서는 `background-crawler`인 이유를 말할 수 있다.
- 게임 항목의 숫자 중 LAVD 발표 원문에 있는 것과 없는 것을 구분할 수 있다.
- 화상 회의를 영상 재생에 묶은 것이 왜 근사인지, 왜 파라미터를 지어내지 않았는지 말할 수 있다.

**존재와 충분함 확인**

- 목록의 존재 근거와 충분함 근거가 왜 다른 방법으로 닫혀야 하는지 설명할 수 있다.
- 부류를 거둬온 네 곳을 말할 수 있다.
- ananicy 카탈로그의 분류가 행동이 아니라 처방이라는 것을 실제 항목으로 보일 수 있다.
- 측정에서 부류를 끌어낸 세 항목을 대고, 그렇게 표시한 것이 왜 정직한지 말할 수 있다.
- 충분함에 대해 쓸 수 있는 주장과 쓸 수 없는 주장을 구분할 수 있다.
- 브라우저 탭 판정 사례에서 무엇이 좋았고 무엇이 비어 있었는지 말할 수 있다.

**개수 확인**

- 개수가 인식기와 executor에게 각각 얼마나 중요한지 설명할 수 있다.
- 창발적 다중성과 정적 다중성의 차이를 예로 설명하고, 컴파일러 자식의 수를 직접 적지 않는 이유 둘을 말할 수 있다.
- 브라우저 탭 프로세스 수가 12든 20이든 부하에 거의 영향이 없다는 것을 산수로 보일 수 있다.
- 게임 항목만 archetype 안에 개수를 가진다는 것이 왜 경계 규칙과 부딪히는지 말할 수 있다.

**측정 확인**

- 데스크톱 프로세스 기록이 공개되지 않는 구조적 이유를 말할 수 있다.
- 측정 캠페인의 세 갈래와 두 기록 도구를 설명할 수 있다.
- 측정값 중 구조와 모양에 속하는 것과 기계에 따라 달라지는 절대값을 구분할 수 있다.
- 첫 측정에서 넷을 측정 대기로 남긴 이유와, 다시 잰 측정이 컴파일러 CPU 모형을 어떻게 고쳤는지 말할 수 있다.
- 깨어남 간격 분포가 프로세스 사이의 흩어짐이라는 것이 뽑는 빈도 문제와 어떻게 맞물리는지 설명할 수 있다.

**손으로 확인**

- 컴파일러 자식 항목을 출처의 문장에서 뽑힌 숫자까지 여덟 칸으로 따라갈 수 있다.
- 평균 CPU와 수명 분포에서 CPU의 중앙값과 흩어짐을 계산하고 검산할 수 있다.
- 뽑힌 값 하나가 분포의 어디쯤에서 나왔는지 z로 계산할 수 있다.
- 두 예시값을 5퍼센트와 95퍼센트 지점으로 보고 로그 정규의 중앙값과 흩어짐을 역산할 수 있다.
- workload 파일 하나를 열어 task마다 가장 약한 근거의 고리를 찾을 수 있다.

**약점 확인**

- 판정 기준이 없는 것, 판정이 순환인 것, 판정이 동어반복인 것의 차이를 예로 설명할 수 있다.
- 관례로 정한 값을 세 종류 이상 들 수 있다.
- 적어둔 약점과 적히지 않은 약점이 논문에서 어떻게 다르게 작동하는지 말할 수 있다.
- 인용 문장이 원문과 글자 그대로 맞아도 인용의 설명이 틀릴 수 있다는 것을 이 권의 사례로 보일 수 있다.

다음 권은 이 archetype들을 불러다 쓰는 쪽을 봅니다. timeline이 archetype과 이름을 짝짓고, seed로 분포에서 값을 뽑고, 실행할 수 있는 workload 파일이 되기까지입니다.
