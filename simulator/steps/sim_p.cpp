// P — deadline 이벤트. TIMER 태스크마다 job 당 한 줄 (metrics.md §6.2):
//   job k 는 자기 틱이 소비될 때 시작하고, 태스크가 **다음 TIMER 에 도달할 때** 완료된다.
//   due = 틱 k 의 격자 시각 + period. 그래서 판정 코드가 TIMER 케이스 맨 앞에 온다.
//   due 가 격자 시각 기준이라 drift 가 섞이지 않는다 — K 의 이유와 같다.
//
// (O 의 주석) 계약의 trace 로 바꾼다: JSONL, meta 헤더 1줄 + 이벤트 7종 (data-contracts §9).
//   Trace::note 의 역할이 좁아진다 — 이제 **x_ 진단 라인 전용**이다. 계약 이벤트는
//   필드가 제각각(ready=cause, run_end=reason+blocked_on, deadline=due/met/slack)이라
//   "문자열 하나"로 표현할 수 없고, 정책은 그것들을 쓸 일이 없다.
//   Task 에 sid(파일의 문자열 id) 추가 — trace 는 인덱스가 아니라 파일 id 로 나가야
//   harness 가 읽는다. 내부 장부는 여전히 인덱스로만 돈다 (비협상 규칙 6).
//   cause/reason 을 코어가 알아야 해서 enqueue(id, cause) 로 바뀌고 blocked_by 가 생긴다.
//
// (N 의 주석) FORK. 태스크가 런타임에 태어난다. spawn_table 4,485개(4파일), depart 없음 —
//   spawned 는 EXIT 으로만 끝난다. *어떤* 자식인지는 컴파일 타임, *언제*는 런타임.
//   fork_cap 이 그 메커니즘: 살아있는 자식이 cap 개면 다음 FORK 가 슬롯까지 블록한다.
//   ★ std::vector<Task> → std::deque<Task>. FORK 는 실행 중 tasks_ 를 키우는데,
//     vector 면 재할당이 step() 한복판의 `Task& t` 를 댕글링으로 만든다. deque 는
//     push_back 후에도 기존 원소 *참조*를 유지한다. ASan 없이는 대개 조용히 지나간다.
//   ★ 관례 예외: cap 에 막힌 FORK 는 pc 를 전진시키지 않는다 — 같은 FORK 를 재시도한다.
//   §9.5 는 미결로 남긴다(README).
//
// (M 의 주석) 채널과 WAKE. 이제 wake 가 태스크가 아니라 **채널**로 배달된다 (입력 그대로).
//   D2 재개정(§9.1): 대기자 없는 wake 를 "잃어버린다"에서 **우편함(깊이 있음)**으로.
//   이유는 K 의 drift 와 같다 — 잃어버리면 굶주린 태스크의 수요가 줄어 측정하려던
//   피해가 은폐된다. 우편함이 둘인 게 걸린다: 외생 wake 는 channel 주소, WAKE 명령어는
//   target 주소(파일이 target 만 준다). 실측은 채널당 대기자가 하나라 결과가 같다 —
//   계약이 이 점을 말하지 않는다 → 인지오 확인 항목.
//   WAKE 배달은 재귀로 푼다. c1-gaming 의 브리게이드가 16단이라 깊이는 유계다.
//
// (L 의 주석) LOOP. 평탄화한다: LOOP_BEGIN/LOOP_END 한 쌍 + 되돌아가는 점프.
//   근거: 실측 1,914개가 **전부 count:"unbounded"** 다 (정수 count 0건 — 컴파일러가
//   평탄화해 풀어버린다). 그래서 pc 를 프레임 스택으로 바꿀 이유가 없다. 계약은 정수
//   count 를 허용하므로 카운터 스택으로 지원만 해둔다(몇 줄).
//   unbounded 의 진짜 종료자는 태스크의 depart 다 (segment-bound 만 legal).
//   step() 이 전진 없이 도는 입력을 대비해 가드를 둔다.
//
// (K 의 주석) TIMER. 절대 격자: t₀ + k·P. SLEEP 과의 차이는 **기준점**이다.
//   SLEEP 루프의 실효 주기 = sleep + 작업 + 대기 → 부하 아래서 뒤로 밀린다(drift).
//   밀린 프레임이 조용히 증발하면 **CPU 수요가 줄어든다** — 스케줄러가 나쁠수록
//   워크로드가 가벼워져서 측정하려던 피해가 스스로를 은폐한다.
//   그래서 밀린 틱은 backlog 로 쌓아 즉시 소비시킨다 (TIMER 한 번이 한 틱).
//   D4(§9.2) t₀ = 그 태스크가 TIMER 를 **처음 실행한 순간**. 후보 셋 중 도착시각은
//   도착~첫TIMER 사이 명령어가 첫 주기를 갉아먹고, 전역 0 은 모든 주기 태스크를
//   인위적으로 동기화시킨다. t=0 도착 태스크는 셋 다 같아 현재 coreset 이 답을 강제 못 함.
//
// (J 의 주석) SLEEP. 상대 시각: now + N 에 다시 runnable.
//   근거: 실측 53,616개로 RUN 다음으로 많다. background-crawler 의 throttle(중앙값 3.8초),
//   system-daemon 의 idle_gap(중앙값 11.2초, sigma_log 1.9) — 둘 다 **비주기적**이라
//   archetypes.yaml 이 명시적으로 TIMER 가 아니라 SLEEP 을 쓴다.
//   외생 wake 와 해제 경로가 완전히 같아서 핸들러를 합친다 (on_unblock).
//   관례: 블록한 명령어의 pc 전진은 *해제 경로*가 한다. (N 의 FORK 만 예외)
//
// (I 의 주석) MLFQ 규칙 5(boost). 정책이 *자기 미래 순간*을 걸어야 하는데 이벤트 큐에는
//   손댈 수 없다 → Clock::arm(t, tag) 로 부탁하고, tag 는 코어에게 불투명하게 되돌아온다.
//   ★ Event 에 tag 가 붙는 두 번째 "나중에 필요해진 필드"다 (첫째는 F 의 gen).
//   홀더를 먼저 release() 하는 이유: boost 가 allot 을 리셋하므로 그 전에 charge 해야
//   하고, 리셋 후 지평선이 넓어져 기존 Lane 예약이 너무 이르다 → 무효화+재무장이 필요.
//   release() 가 그 둘을 동시에 한다. 그래서 "놓고 → 정책 호출 → 되돌려주기".
//
// (H 의 주석) Trace/Clock 이음매 + MLFQ.
//   Mlfq 는 Sim 을 모른다. 좁은 참조 두 개(Trace&, Clock&)만 들고 컴파일된다.
//   Sim& 을 넘기면 정책이 tasks_ 를 만지고 큐에 이벤트를 밀어넣을 수 있다.
//   Trace 와 Clock 을 쪼갠 이유: 출력과 시간은 직교한다 — Fifo 는 둘 다 안 쓴다.
//   둘 다 데이터 멤버 0개인 순수 인터페이스라 C++ 의 위험한 다중상속이 아니다.
// horizon() 이 "슬라이스"가 아니라 "이 레벨에 남은 할당량"이 된다 (규칙 3의 구현).
// allot 은 자발적 블록에 리셋되지 않는다 — OSTEP §8.4 규칙 4 (폐기된 4a/4b 아님).
//
// (G 의 주석) 정책 인터페이스를 **추출**한다. 설계가 아니라 추출인 이유: 무엇이 필요한지
//     모르는 채로 경계를 그리면 틀린다. 두 정책을 같은 코어에 얹어 경계를 시험한다.
//     계약(guide §5)의 검증 가능한 의무: "두 번째 정책 추가가 코어를 고치지 않을 것".
// 코어에서 정책으로 넘어간 것: ready set 자체 / 슬라이스(→horizon) / 선점 규칙(→preempts)
// 회귀 확인: ./sim_g fifo 의 출력은 sim_e 와 **동일**하다.
//   ./sim_g rr 는 sim_f 와 한 줄 다르고, 그게 F 의 버그였다: 선점당해 큐로 돌아가는
//   태스크에 "ready" 를 찍고 있었다. 계약의 ready.cause 는 arrive|wake|sleep_end|
//   timer_tick|fork_slot 뿐이다 — 선점 복귀는 readiness 전이가 아니다
//   (data-contracts §9). on_yield(Preempted) 로 분리되면서 저절로 고쳐졌다.
//
// (F 의 주석) 타임슬라이스와 선점, 그리고 그 대가인 "유령 예약".
// 선점하려면 이미 큐에 든 만료 예약을 취소해야 하는데 priority_queue 는 삭제가 안 된다.
// → 취소 대신 **세대 도장**: 예약에 gen 을 싣고, 레인을 놓을 때마다 태스크의 gen 을 올린다.
// on_lane 의 검사가 두 항인 이유: 다른 놈이 레인을 쥐었다 / 같은 놈이 놨다가 *다시 잡았다*.
// 두 번째 경우는 E 까지 존재하지 않았다(선점이 없었다) — 그 가정이 여기서 깨진다.
// 양성 대조: ./sim_f --no-gen 으로 검사를 끄면 없던 컨텍스트 스위치가 trace 에 심긴다.
// 재현: guide §4½ punchline — 키입력#1 응답 10ms→0, hog turnaround 20→23ms.
// D2(§9.1) 대기자 없는 wake 는 **잃어버린다** — 잠정. M(채널)에서 우편함으로 바꾼다.
// 지금 wake 는 채널이 아니라 태스크 id 로 직행한다 — 채널 테이블도 M 에서.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <cstdio>
#include <deque>
#include <map>
#include <queue>
#include <string>
#include <utility>
#include <vector>

using i64 = std::int64_t;

enum class Op { RUN, SLEEP, TIMER, WAIT, WAKE, FORK, EXIT, LOOP_BEGIN, LOOP_END };
struct Instr { Op op; i64 us = 0; i64 period_us = 0; int jump = -1; i64 count = -1;
               int chan = -1; int target = -1; };

// Ready 와 Running 을 가르는 이유: 스케줄러가 *고르는 대상*이 Ready 집합이다.
// 자식 하나의 명세 — 파일의 spawn_table 엔트리 그대로 (id/name/program 뿐)
struct ChildSpec { std::string name; std::vector<Instr> prog; };

enum class State { Ready, Running, Blocked, Done };

struct Task {
  std::string sid;            // 파일의 문자열 id — trace 가 이걸로 나간다
  std::string name;           // 라벨. 어떤 스케줄링도 이걸로 분기하지 않는다
  std::vector<Instr> prog;
  std::size_t pc = 0;
  State st = State::Blocked;
  i64 run_left = 0;           // 현재 RUN 의 남은 수요 — 선점을 넘어 보존된다
  i64 timer_next = -1;        // 이 태스크의 격자 다음 틱. -1 = t₀ 미확정
  bool job_open = false; i64 job_tick = 0, job_period = 0;   // 열린 주기 job
  std::vector<i64> loop_left; // 중첩 루프의 남은 반복 수 (-1 = unbounded)
  int wait_chan = -1;         // 지금 블록 중인 채널 (-1 = 채널 대기 아님)
  int mailbox = 0;            // 대기자 없이 도착한 WAKE 들 (태스크 주소)
  std::vector<ChildSpec> spawn_table;  // 순서대로 소비한다
  int fork_cap = 0, live_children = 0, parent = -1;
  std::size_t spawn_next = 0;
  i64 born = -1, ended = -1;
  char blocked_by = 'w';      // w=wait s=sleep t=timer f=fork_slot — cause/blocked_on 용  // born 은 창발 시각 — FORK 자식에게만 의미 있다
  std::uint64_t gen = 0;      // 레인을 놓을 때마다 올라간다 = 예약 무효화
};

constexpr i64 kNoHorizon = -1;                       // 정책이 지평선을 두지 않는다

// 동결 스키마의 MLFQ params (recognition-vocabulary §2 — OSTEP §8 worked example 통째)
struct Params {
  int num_queues        = 3;
  i64 timeslice_us      = 10000;
  int timeslice_growth  = 2;
  i64 boost_interval_us = 100000;   // 규칙 5 는 단계 I
};

// 코어의 trace 작성기 — 정책이 받는 유일한 출력
struct Trace {
  virtual ~Trace() = default;
  virtual void note(const char* what, int task) = 0;   // x_ 진단 전용
  virtual void note(const char* what) = 0;
};

// 코어의 시계 — 정책이 만져도 되는 만큼만
struct Clock {
  virtual ~Clock() = default;
  virtual i64 now() const = 0;
  virtual void arm(i64 t, int tag) = 0;   // t 에 Policy::on_timer(tag) 로 되돌아온다
};

// 레인을 떠난 이유. 앞의 둘은 여전히 runnable, 뒤의 둘은 ready set 에서 빠진다
enum class Yield { SliceEnd, Preempted, Blocked, Ended };

struct Policy {
  virtual ~Policy() = default;
  virtual void start(const Params&) = 0;
  virtual void on_ready(int id) = 0;
  virtual void on_yield(int id, Yield why) = 0;
  virtual int  pick() = 0;                  // 다음 홀더, idle 이면 -1
  virtual i64  horizon(int id) = 0;         // 더 쓸 수 있는 레인 시간
  virtual bool preempts(int challenger, int holder) = 0;
  virtual void charge(int id, i64 ran) = 0;   // 배달된 레인 시간 — 레인을 놓을 때마다
  virtual void on_timer(int tag) { (void)tag; }
};

struct Fifo : Policy {                      // = 단계 E 의 행동
  std::deque<int> q;
  void start(const Params&) override {}
  void on_ready(int id) override { q.push_back(id); }
  void on_yield(int id, Yield why) override {
    if (why == Yield::SliceEnd || why == Yield::Preempted) q.push_back(id);
    else q.erase(std::remove(q.begin(), q.end(), id), q.end());
  }
  int  pick() override { if (q.empty()) return -1; int id = q.front(); q.pop_front(); return id; }
  i64  horizon(int) override { return kNoHorizon; }
  bool preempts(int, int) override { return false; }
  void charge(int, i64) override {}
};

struct Mlfq : Policy {
  struct St { int level = 0; i64 allot = 0; };   // allot: 이 레벨에서 쓴 CPU
  Trace& trace;
  Clock& clock;
  Params p;
  std::vector<std::deque<int>> ready;            // ready set 의 *구조*가 정책이다
  std::vector<St> st;

  Mlfq(Trace& tr, Clock& cl) : trace(tr), clock(cl) {}
  St& slot(int id) {
    if (st.size() <= (std::size_t)id) st.resize((std::size_t)id + 1);
    return st[(std::size_t)id];
  }
  i64 slice_of(int lv) const {
    i64 s = p.timeslice_us;
    for (int i = 0; i < lv; ++i) s *= p.timeslice_growth;
    return s;
  }
  static constexpr int kBoost = 1;                 // 우리 tag. 코어에겐 불투명하다
  void start(const Params& np) override {
    p = np;
    ready.assign((std::size_t)p.num_queues, {});
    clock.arm(clock.now() + p.boost_interval_us, kBoost);
  }
  void on_timer(int) override {                    // 규칙 5: 전원 최상위 큐로
    std::vector<int> w;
    for (auto& q : ready) { for (int id : q) w.push_back(id); q.clear(); }
    std::sort(w.begin(), w.end());                 // 결정적 재구성 — id 가 tie-break (D1)
    for (St& s : st) { s.level = 0; s.allot = 0; }
    for (int id : w) ready[0].push_back(id);
    trace.note("x_mlfq_boost");
    clock.arm(clock.now() + p.boost_interval_us, kBoost);
  }
  void on_ready(int id) override { ready[(std::size_t)slot(id).level].push_back(id); }
  void on_yield(int id, Yield why) override {
    St& s = slot(id);
    if (why == Yield::SliceEnd) {                       // 규칙 3: 할당량을 다 태웠다 → 강등
      if (s.level + 1 < p.num_queues) ++s.level;
      s.allot = 0;
      ready[(std::size_t)s.level].push_back(id);
      trace.note("x_mlfq_demote", id);
    } else if (why == Yield::Preempted) {               // 레벨·할당량 유지
      ready[(std::size_t)s.level].push_back(id);
    } else {                                            // 규칙 4: 블록해도 둘 다 유지
      for (auto& q : ready) q.erase(std::remove(q.begin(), q.end(), id), q.end());
    }
  }
  int pick() override {                                 // 규칙 1+2
    for (auto& q : ready)
      if (!q.empty()) { int id = q.front(); q.pop_front(); return id; }
    return -1;
  }
  i64  horizon(int id) override { return slice_of(slot(id).level) - slot(id).allot; }
  void charge(int id, i64 ran) override { slot(id).allot += ran; }
  bool preempts(int c, int h) override { return slot(c).level < slot(h).level; }
};

enum class EvKind { Arrive, Lane, Wake, Unblock, Depart, PolicyTimer };
struct Event { i64 t; std::uint64_t seq; EvKind kind; int task; std::uint64_t gen = 0; int tag = 0; };

struct Later {
  bool operator()(const Event& a, const Event& b) const {
    return a.t != b.t ? a.t > b.t : a.seq > b.seq;
  }
};

class Sim : public Trace, public Clock {
 public:
  // ── Trace / Clock 이음매 ──
  i64 now() const override { return now_; }
  void note(const char* what, int id) override {           // 정책의 x_ 라인
    assert(what[0] == 'x' && what[1] == '_');
    std::printf("{\"event\":\"%s\",\"t\":%lld,\"task\":\"%s\"}\n", what, (long long)now_,
                tasks_[(std::size_t)id].sid.c_str());
  }
  void note(const char* what) override {
    std::printf("{\"event\":\"%s\",\"t\":%lld}\n", what, (long long)now_);
  }

  void ev_deadline(int id, i64 due, bool met, i64 slack) {
    std::printf("{\"event\":\"deadline\",\"t\":%lld,\"task\":\"%s\",\"due\":%lld,"
                "\"met\":%s,\"slack_us\":%lld}\n", (long long)now_,
                tasks_[(std::size_t)id].sid.c_str(), (long long)due,
                met ? "true" : "false", (long long)slack);
  }

  // ── 계약 이벤트 (data-contracts §9) ──
  void ev(const char* name, int id, const char* k1 = nullptr, const char* v1 = nullptr,
          const char* k2 = nullptr, const char* v2 = nullptr) {
    std::printf("{\"event\":\"%s\",\"t\":%lld,\"task\":\"%s\"", name, (long long)now_,
                tasks_[(std::size_t)id].sid.c_str());
    if (k1) std::printf(",\"%s\":\"%s\"", k1, v1);
    if (k2) std::printf(",\"%s\":\"%s\"", k2, v2);
    std::printf("}\n");
  }

  // 정책 타이머는 **다른 일이 남아 있을 때만** 다시 건다.
  // "살아있는 태스크가 있으면" 으로는 부족하다: 더 올 wake 도 depart 도 없이 영원히
  // 블록된 태스크는 Done 이 아니지만 죽은 것이고, 그러면 boost 가 자기 혼자 큐를
  // 채워 시계를 무한정 앞으로 민다 (c1-compile 이 1.9억 줄을 뱉었다. t 가 11시간을
  // 넘어갔다). 이 시점의 q_ 는 이 타이머를 pop 한 *뒤*의 미래 전부다 —
  // 비어 있으면 실행은 끝난 것이다. 계약에 T_end 가 생기면 이 규칙이 대체된다.
  void arm(i64 t, int tag) override {
    if (q_.empty()) return;                       // 남은 일이 없다
    for (const Task& tk : tasks_)                 // 남은 일은 있지만 태스크가 다 끝났다
      if (tk.st != State::Done) { q_.push({t, seq_++, EvKind::PolicyTimer, -1, 0, tag}); return; }
  }

  int add(std::string sid, i64 t, std::vector<Instr> prog, i64 depart = -1) {
    Task nt; nt.sid = sid; nt.name = std::move(sid); nt.prog = std::move(prog);
    tasks_.push_back(std::move(nt));
    const int id = static_cast<int>(tasks_.size()) - 1;
    push(t, EvKind::Arrive, id);
    if (depart >= 0) push(depart, EvKind::Depart, id);   // segment-bound
    return id;
  }

  int channel(const std::string& name) {          // 문자열 채널 → 인덱스 (로더의 입구)
    auto it = chan_id_.find(name);
    if (it != chan_id_.end()) return it->second;
    const int c = (int)chan_waiters_.size();
    chan_id_.emplace(name, c);
    chan_waiters_.emplace_back();
    chan_pending_.push_back(0);
    return c;
  }
  // 전방 참조용. WAKE 의 target 은 아직 등록되지 않은 태스크를 가리킬 수 있다.
  // 단계 P 의 로더는 arrive 를 전부 읽어 이름→인덱스 표를 만든 *뒤에* program 을 해소한다
  void set_prog(int id, std::vector<Instr> prog) { T(id).prog = std::move(prog); }
  void set_spawn(int id, std::vector<ChildSpec> tab, int cap) {
    T(id).spawn_table = std::move(tab); T(id).fork_cap = cap;
  }
  void report() const {   // 창발 시각 요약 — FORK 자식만
    i64 first = -1, last = -1, done = -1; int n = 0;
    for (const Task& t : tasks_) {
      if (t.parent < 0) continue;
      ++n;
      if (first < 0 || t.born < first) first = t.born;
      if (t.born > last) last = t.born;
      if (t.ended > done) done = t.ended;
    }
    if (n) std::fprintf(stderr, "자식 %d개 — 첫 탄생 %lld, 마지막 탄생 %lld, 전부 종료 %lld\n",
                        n, (long long)first, (long long)last, (long long)done);
  }

  void wake(i64 t, int chan) { q_.push({t, seq_++, EvKind::Wake, -1, 0, chan}); }

  explicit Sim(bool check_gen = true) : check_gen_(check_gen) {}
  void attach(Policy& p) { pol_ = &p; }

  void run(const Params& p) {
    std::printf("{\"event\":\"meta\",\"workload_id\":\"%s\",\"condition\":\"%s\","
                "\"sim\":\"notes/sim\",\"schedule_entries\":1}\n", wid_.c_str(), cond_.c_str());
    pol_->start(p);
    while (!q_.empty()) {
      const Event e = q_.top();
      q_.pop();
      assert(e.t >= now_);
      now_ = e.t;
      switch (e.kind) {
        case EvKind::Arrive: on_arrive(e.task); break;
        case EvKind::Lane:   on_lane(e);        break;
        case EvKind::Wake:    on_ext_wake(e.tag); break;
        case EvKind::Unblock: on_unblock(e.task); break;
        case EvKind::Depart: on_depart(e.task); break;
        case EvKind::PolicyTimer: on_policy_timer(e); break;
      }
      dispatch();
    }
  }

 protected:
  std::deque<Task> tasks_;   // ★ vector 가 아니다 (머리 주석)
  std::priority_queue<Event, std::vector<Event>, Later> q_;
  std::uint64_t seq_ = 0;
  std::string wid_ = "hand", cond_ = "fixed";
  Policy* pol_ = nullptr;
  int running_ = -1;
  i64 lane_start_ = 0, now_ = 0;

  bool check_gen_ = true;

  void push(i64 t, EvKind k, int task, std::uint64_t gen = 0) { q_.push({t, seq_++, k, task, gen, 0}); }

  void on_policy_timer(const Event& e) {
    int holder = running_;
    if (holder >= 0) {
      release();
      if (T(holder).run_left == 0) { advance(holder); holder = -1; }   // 경계와 겹쳤다
    }
    pol_->on_timer(e.tag);
    if (holder < 0) return;
    if (pol_->horizon(holder) == 0) { ev("run_end", holder, "reason", "preempt");
                                      yield_lane(holder, Yield::SliceEnd); }
    else { running_ = holder; T(holder).st = State::Running;           // 전환 없음 → 무기록
           lane_start_ = now_; arm_lane(holder); }
  }

  // 레인 회계는 이 한 곳에서만. 여기가 "수요는 선점을 넘어 보존된다"의 구현이다
  void release() {
    T(running_).run_left -= now_ - lane_start_;
    assert(T(running_).run_left >= 0);
    pol_->charge(running_, now_ - lane_start_);
    ++T(running_).gen;
    running_ = -1;
  }

  void advance(int id) {   // RUN 하나가 끝났다 — 다음 명령어를 보고 정한다
    ++T(id).pc;
    step(id);
    if (T(id).st == State::Done) ev("run_end", id, "reason", "exit");
    else if (T(id).st == State::Blocked) ev("run_end", id, "reason", "block",
                                            "blocked_on", blocked_on(T(id)));
    if (T(id).st == State::Ready) enqueue(id, "arrive");
    else { settled(id); pol_->on_yield(id, T(id).st == State::Done ? Yield::Ended : Yield::Blocked); }
  }

  void maybe_preempt(int challenger) {
    if (running_ < 0 || !pol_->preempts(challenger, running_)) return;
    const int v = running_;
    release();
    ev("run_end", v, "reason", "preempt");
    if (T(v).run_left == 0) advance(v); else yield_lane(v, Yield::Preempted);
  }
  Task& T(int id) { return tasks_[static_cast<std::size_t>(id)]; }

  // 프로그램만 전진시킨다. ready set 투입도 레인 배정도 호출자의 몫
  void step(int id) {
    Task& t = T(id);
    for (int guard = 0; ; ++guard) {
      if (guard > 1000000) { std::fprintf(stderr, "step: %s 가 전진하지 않는다\n",
                                          t.name.c_str()); std::abort(); }
      if (t.pc >= t.prog.size()) { t.st = State::Done; return; }
      switch (t.prog[t.pc].op) {
        case Op::RUN:  t.st = State::Ready; t.run_left = t.prog[t.pc].us; return;
        case Op::SLEEP: t.st = State::Blocked; t.blocked_by = 's';
                        push(now_ + t.prog[t.pc].us, EvKind::Unblock, id); return;
        case Op::TIMER: {
          const i64 P = t.prog[t.pc].period_us;
          if (t.job_open) {                               // 직전 job 의 마감 판정
            const i64 d = t.job_tick + t.job_period;
            ev_deadline(id, d, now_ <= d, d - now_);
            t.job_open = false;
          }
          if (t.timer_next < 0) t.timer_next = now_;      // D4
          if (now_ >= t.timer_next) {                     // backlog → 틱 즉시 소비
            t.job_tick = t.timer_next; t.job_period = P; t.job_open = true;
            t.timer_next += P; ++t.pc; break;
          }
          const i64 due = t.timer_next;                   // 격자 앞 — 다음 틱까지 블록
          t.job_tick = due; t.job_period = P; t.job_open = true;
          t.timer_next += P;
          t.st = State::Blocked; t.blocked_by = 't';
          push(due, EvKind::Unblock, id);
          return;
        }
        case Op::WAIT: {
          const int c = t.prog[t.pc].chan;
          if (chan_pending_[(std::size_t)c] > 0) { --chan_pending_[(std::size_t)c]; ++t.pc; break; }
          if (t.mailbox > 0) { --t.mailbox; ++t.pc; break; }
          t.st = State::Blocked; t.blocked_by = 'w'; t.wait_chan = c;
          chan_waiters_[(std::size_t)c].push_back(id);
          return;
        }
        case Op::WAKE: deliver(t.prog[t.pc].target); ++t.pc; break;
        case Op::FORK:
          if (t.spawn_next >= t.spawn_table.size()) { ++t.pc; break; }   // 테이블 소진
          if (t.fork_cap > 0 && t.live_children >= t.fork_cap) {
            t.st = State::Blocked; t.blocked_by = 'f'; t.wait_chan = -1; // 슬롯 대기
            return;                                                      // ★ pc 그대로
          }
          spawn(id); ++t.pc; break;
        case Op::EXIT: t.st = State::Done;    return;
        case Op::LOOP_BEGIN:
          if (t.prog[t.pc].count == 0) { t.pc = (std::size_t)t.prog[t.pc].jump; break; }
          t.loop_left.push_back(t.prog[t.pc].count);
          ++t.pc; break;
        case Op::LOOP_END: {
          i64& n = t.loop_left.back();
          if (n < 0 || --n > 0) { t.pc = (std::size_t)t.prog[t.pc].jump; break; }
          t.loop_left.pop_back(); ++t.pc; break;
        }
      }
    }
  }

  void enqueue(int id, const char* cause) {
    T(id).st = State::Ready; pol_->on_ready(id); ev("ready", id, "cause", cause);
  }
  static const char* cause_of(const Task& t) {
    switch (t.blocked_by) { case 's': return "sleep_end"; case 't': return "timer_tick";
                            case 'f': return "fork_slot"; default: return "wake"; }
  }
  static const char* blocked_on(const Task& t) {
    switch (t.blocked_by) { case 's': return "sleep"; case 't': return "timer";
                            case 'f': return "fork_slot"; default: return "wait"; }
  }
  void yield_lane(int id, Yield why) {
    if (why == Yield::SliceEnd || why == Yield::Preempted) T(id).st = State::Ready;
    pol_->on_yield(id, why);
  }

  void on_arrive(int id) {
    ev("task_arrive", id, "source", "file");
    step(id);
    if (T(id).st == State::Ready) { enqueue(id, "arrive"); maybe_preempt(id); } else settled(id);
  }

  std::map<std::string, int> chan_id_;
  std::vector<std::deque<int>> chan_waiters_;
  std::vector<int> chan_pending_;               // 채널 우편함

  void spawn(int parent_id) {
    Task& par = T(parent_id);
    Task c;
    c.name = par.spawn_table[par.spawn_next].name;
    c.sid = par.sid + "." + std::to_string(par.spawn_next + 1);
    c.prog = par.spawn_table[par.spawn_next].prog;
    c.parent = parent_id;
    ++par.spawn_next; ++par.live_children;
    tasks_.push_back(std::move(c));            // deque 이므로 par 참조는 유효하다
    const int id = (int)tasks_.size() - 1;
    T(id).born = now_;
    ev("task_arrive", id, "source", "spawn", "parent", T(parent_id).sid.c_str());
    step(id);
    if (T(id).st == State::Ready) { enqueue(id, "arrive"); maybe_preempt(id); } else settled(id);
  }

  // 종료를 한 곳으로 모은다. EXIT 이든 depart 든 부모의 슬롯은 정확히 한 번 돌아와야
  // 한다 — 두 번 돌리면 cap 이 새고, 안 돌리면 빌드가 영원히 멈춘다
  void on_task_end(int id) {
    Task& t = T(id);
    if (t.ended >= 0) return;
    t.ended = now_;
    if (t.parent < 0) return;
    Task& p = T(t.parent);
    assert(p.live_children > 0);
    --p.live_children;
    if (p.st == State::Blocked && p.wait_chan < 0) on_unblock_fork(t.parent);
  }
  void on_unblock_fork(int id) {   // 슬롯이 났다 — 같은 FORK 를 재시도한다 (pc 전진 없음)
    T(id).st = State::Ready;
    ev("ready", id, "cause", "fork_slot");
    step(id);
    if (T(id).st == State::Ready) { pol_->on_ready(id); maybe_preempt(id); } else settled(id);
  }

  void on_ext_wake(int c) {                     // 외생 wake — 채널 주소
    auto& w = chan_waiters_[(std::size_t)c];
    if (w.empty()) { ++chan_pending_[(std::size_t)c]; return; }
    const int id = w.front(); w.pop_front();
    T(id).wait_chan = -1;
    on_unblock(id);
  }

  void deliver(int target) {                    // WAKE 명령어 — 태스크 주소
    Task& t = T(target);
    if (t.st == State::Done) return;
    if (t.st == State::Blocked && t.wait_chan >= 0) {
      auto& w = chan_waiters_[(std::size_t)t.wait_chan];
      w.erase(std::remove(w.begin(), w.end(), target), w.end());
      t.wait_chan = -1;
      on_unblock(target);                       // 재귀 — 체인이 여기서 풀린다
    } else ++t.mailbox;
  }

  void on_unblock(int id) {                    // 외생 wake / SLEEP 만료 공통
    if (T(id).st != State::Blocked) return;    // D2: 대기자가 없으면 편지는 버려진다
    const char* c = cause_of(T(id));
    ++T(id).pc;                                // 블록했던 명령어가 끝났다
    step(id);
    if (T(id).st == State::Ready) { enqueue(id, c); maybe_preempt(id); } else settled(id);
  }

  void on_lane(const Event& e) {
    if (e.task != running_) return;
    if (check_gen_ && e.gen != T(e.task).gen) return;   // ★ 무효화된 예약
    const int id = e.task;
    release();
    if (T(id).run_left == 0) advance(id);              // RUN 수요 소진
    else { ev("run_end", id, "reason", "preempt"); yield_lane(id, Yield::SliceEnd); }
  }

  void arm_lane(int id) {
    const i64 h = pol_->horizon(id);
    const i64 dt = h == kNoHorizon ? T(id).run_left : std::min(T(id).run_left, h);
    push(now_ + dt, EvKind::Lane, id, T(id).gen);
  }

  void dispatch() {
    if (running_ >= 0) return;
    const int id = pol_->pick();
    if (id < 0) return;
    running_ = id;
    T(id).st = State::Running;
    lane_start_ = now_;
    arm_lane(id);
    ev("run_start", id);
  }

  void on_depart(int id) {
    if (running_ == id) { ev("run_end", id, "reason", "depart"); release(); }
    if (T(id).wait_chan >= 0) {
      auto& w = chan_waiters_[(std::size_t)T(id).wait_chan];
      w.erase(std::remove(w.begin(), w.end(), id), w.end());
    }
    T(id).st = State::Done;
    ev("task_end", id, "reason", "depart");
    on_task_end(id);
    pol_->on_yield(id, Yield::Ended);   // 어디 앉아 있었든 ready set 에서도 빠진다
  }

  void settled(int id) {  // step() 이 Ready 로 안착하지 못했을 때
    if (T(id).st == State::Done) { ev("task_end", id, "reason", "exit"); on_task_end(id); }
    else note("x_block", id);
  }

};

// LOOP 평탄화 헬퍼 — 단계 P 의 로더가 JSON 의 중첩 LOOP 에 대해 할 일을 손으로 한다
static std::vector<Instr> loop_forever(std::vector<Instr> body) {
  std::vector<Instr> out;
  out.push_back(Instr{Op::LOOP_BEGIN, 0, 0, -1, -1});
  for (const Instr& i : body) out.push_back(i);
  Instr end{Op::LOOP_END, 0, 0, 1, -1};          // 본문 첫 명령어 = 인덱스 1
  out.push_back(end);
  out[0].jump = (int)out.size();                 // 본문 다음 = 끝
  return out;
}

int main(int argc, char** argv) {
  const std::string mode = argc > 1 ? argv[1] : "mlfq";
  Sim s;
  Fifo fifo;
  Mlfq mlfq(s, s);                 // 같은 객체, 두 개의 좁은 창
  if (mode == "fifo") s.attach(fifo); else s.attach(mlfq);
  s.add("daemon", 0, {{Op::SLEEP, 7000}, {Op::RUN, 155},
                      {Op::SLEEP, 9000}, {Op::RUN, 155}, {Op::EXIT, 0}});
  // 60Hz 한 프레임씩. 부하에 밀려도 격자는 안 움직인다
  // c1-media 의 mpv 그대로: LOOP unbounded [ TIMER 16667, RUN 6667 ], depart 가 종료자
  s.add("mpv", 0, loop_forever({{Op::TIMER, 0, 16667}, {Op::RUN, 6667}}), 50000);
  const int ch = s.channel("input:editor");
  s.add("editor", 0, {{Op::WAIT, 0, 0, -1, -1, ch}, {Op::RUN, 3000},
                      {Op::WAIT, 0, 0, -1, -1, ch}, {Op::RUN, 2000},
                      {Op::WAIT, 0, 0, -1, -1, ch}}, 50000);
  // c1-gaming 브리게이드 축소판: TIMER 소스 → WAKE → WAIT/RUN
  const int c2 = s.channel("chain:2");
  const int src = s.add("chain.1", 0, {}, 50000);          // 전방 참조: 먼저 자리만 잡는다
  const int t2 = s.add("chain.2", 0, loop_forever({{Op::WAIT, 0, 0, -1, -1, c2},
                                                   {Op::RUN, 1218}}), 50000);
  s.set_prog(src, loop_forever({{Op::TIMER, 0, 16667}, {Op::RUN, 646},
                                {Op::WAKE, 0, 0, -1, -1, -1, t2}}));
  s.add("hog", 0, {{Op::RUN, 20000}, {Op::EXIT, 0}});
  s.wake(10000, ch);
  s.wake(30000, ch);
  // make -j8 + 자식 40개. 희소성이 없으면 스케줄러는 아무것도 못 바꾸므로 hog 를 세운다
  std::vector<Instr> mk; std::vector<ChildSpec> tab;
  for (int k = 0; k < 40; ++k) {
    mk.push_back({Op::RUN, 300});
    mk.push_back({Op::FORK});
    tab.push_back(ChildSpec{"cc1", {{Op::RUN, 664}, {Op::SLEEP, 3126},
                                    {Op::RUN, 9}, {Op::EXIT, 0}}});
  }
  mk.push_back({Op::EXIT, 0});
  const int b = s.add("make", 0, mk);
  s.set_spawn(b, std::move(tab), 8);
  s.add("hog", 0, {{Op::RUN, 60000}, {Op::EXIT, 0}});

  Params p;
  p.timeslice_us = 2000;        // guide §5 의 예시값 — 20ms hog 가 두 번 강등되도록
  p.boost_interval_us = 20000;  // 50ms 런에서 boost 가 실제로 터지도록 한 예시값
  s.run(p);
  s.report();
}
