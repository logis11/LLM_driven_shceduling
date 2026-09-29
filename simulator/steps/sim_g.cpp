// G — 정책 인터페이스를 **추출**한다. 설계가 아니라 추출인 이유: 무엇이 필요한지
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
#include <queue>
#include <string>
#include <utility>
#include <vector>

using i64 = std::int64_t;

enum class Op { RUN, WAIT, EXIT };
struct Instr { Op op; i64 us = 0; };

// Ready 와 Running 을 가르는 이유: 스케줄러가 *고르는 대상*이 Ready 집합이다.
enum class State { Ready, Running, Blocked, Done };

struct Task {
  std::string name;           // 라벨. 어떤 스케줄링도 이걸로 분기하지 않는다
  std::vector<Instr> prog;
  std::size_t pc = 0;
  State st = State::Blocked;
  i64 run_left = 0;           // 현재 RUN 의 남은 수요 — 선점을 넘어 보존된다
  std::uint64_t gen = 0;      // 레인을 놓을 때마다 올라간다 = 예약 무효화
};

constexpr i64 kNoHorizon = -1;                       // 정책이 지평선을 두지 않는다
struct Params { i64 timeslice_us = kNoHorizon; };

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
};

struct Rr : Fifo {                          // = 단계 F 의 행동 + 슬라이스
  Params p;
  void start(const Params& np) override { p = np; }
  i64  horizon(int) override { return p.timeslice_us; }
  bool preempts(int, int) override { return true; }
};

enum class EvKind { Arrive, Lane, Wake, Depart };
struct Event { i64 t; std::uint64_t seq; EvKind kind; int task; std::uint64_t gen = 0; };

struct Later {
  bool operator()(const Event& a, const Event& b) const {
    return a.t != b.t ? a.t > b.t : a.seq > b.seq;
  }
};

class Sim {
 public:
  int add(std::string name, i64 t, std::vector<Instr> prog, i64 depart = -1) {
    tasks_.push_back(Task{std::move(name), std::move(prog), 0, State::Blocked, 0, 0});
    const int id = static_cast<int>(tasks_.size()) - 1;
    push(t, EvKind::Arrive, id);
    if (depart >= 0) push(depart, EvKind::Depart, id);   // segment-bound
    return id;
  }

  void wake(i64 t, int id) { push(t, EvKind::Wake, id); }

  explicit Sim(bool check_gen = true) : check_gen_(check_gen) {}
  void attach(Policy& p) { pol_ = &p; }

  void run(const Params& p) {
    pol_->start(p);
    while (!q_.empty()) {
      const Event e = q_.top();
      q_.pop();
      assert(e.t >= now_);
      now_ = e.t;
      switch (e.kind) {
        case EvKind::Arrive: on_arrive(e.task); break;
        case EvKind::Lane:   on_lane(e);        break;
        case EvKind::Wake:   on_wake(e.task);   break;
        case EvKind::Depart: on_depart(e.task); break;
      }
      dispatch();
    }
  }

 protected:
  std::vector<Task> tasks_;
  std::priority_queue<Event, std::vector<Event>, Later> q_;
  std::uint64_t seq_ = 0;
  Policy* pol_ = nullptr;
  int running_ = -1;
  i64 lane_start_ = 0, now_ = 0;

  bool check_gen_ = true;

  void push(i64 t, EvKind k, int task, std::uint64_t gen = 0) { q_.push({t, seq_++, k, task, gen}); }

  // 레인 회계는 이 한 곳에서만. 여기가 "수요는 선점을 넘어 보존된다"의 구현이다
  void release() {
    T(running_).run_left -= now_ - lane_start_;
    assert(T(running_).run_left >= 0);
    ++T(running_).gen;
    running_ = -1;
  }

  void advance(int id) {   // RUN 하나가 끝났다 — 다음 명령어를 보고 정한다
    ++T(id).pc;
    step(id);
    note("run_end", id);
    if (T(id).st == State::Ready) enqueue(id);
    else { settled(id); pol_->on_yield(id, T(id).st == State::Done ? Yield::Ended : Yield::Blocked); }
  }

  void maybe_preempt(int challenger) {
    if (running_ < 0 || !pol_->preempts(challenger, running_)) return;
    const int v = running_;
    release();
    note("run_preempt", v);
    if (T(v).run_left == 0) advance(v); else yield_lane(v, Yield::Preempted);
  }
  Task& T(int id) { return tasks_[static_cast<std::size_t>(id)]; }

  // 프로그램만 전진시킨다. ready set 투입도 레인 배정도 호출자의 몫
  void step(int id) {
    Task& t = T(id);
    for (;;) {
      if (t.pc >= t.prog.size()) { t.st = State::Done; return; }
      switch (t.prog[t.pc].op) {
        case Op::RUN:  t.st = State::Ready; t.run_left = t.prog[t.pc].us; return;
        case Op::WAIT: t.st = State::Blocked; return;
        case Op::EXIT: t.st = State::Done;    return;
      }
    }
  }

  void enqueue(int id) { T(id).st = State::Ready; pol_->on_ready(id); note("ready", id); }
  void yield_lane(int id, Yield why) {
    if (why == Yield::SliceEnd || why == Yield::Preempted) T(id).st = State::Ready;
    pol_->on_yield(id, why);
  }

  void on_arrive(int id) {
    note("task_arrive", id);
    step(id);
    if (T(id).st == State::Ready) { enqueue(id); maybe_preempt(id); } else settled(id);
  }

  void on_wake(int id) {
    if (T(id).st != State::Blocked) return;    // D2: 대기자가 없으면 편지는 버려진다
    ++T(id).pc;                                // WAIT 이 끝났다
    step(id);
    if (T(id).st == State::Ready) { enqueue(id); maybe_preempt(id); } else settled(id);
  }

  void on_lane(const Event& e) {
    if (e.task != running_) return;
    if (check_gen_ && e.gen != T(e.task).gen) return;   // ★ 무효화된 예약
    const int id = e.task;
    release();
    if (T(id).run_left == 0) advance(id);              // RUN 수요 소진
    else { note("run_slice", id); yield_lane(id, Yield::SliceEnd); }  // 슬라이스 만료
  }

  void dispatch() {
    if (running_ >= 0) return;
    const int id = pol_->pick();
    if (id < 0) return;
    running_ = id;
    T(id).st = State::Running;
    lane_start_ = now_;
    const i64 h = pol_->horizon(id);
    const i64 dt = h == kNoHorizon ? T(id).run_left : std::min(T(id).run_left, h);
    push(now_ + dt, EvKind::Lane, id, T(id).gen);
    note("run_start", id);
  }

  void on_depart(int id) {
    note("depart", id);
    if (running_ == id) release();
    T(id).st = State::Done;
    pol_->on_yield(id, Yield::Ended);   // 어디 앉아 있었든 ready set 에서도 빠진다
  }

  void settled(int id) {  // step() 이 Ready 로 안착하지 못했을 때
    note(T(id).st == State::Blocked ? "x_block" : "task_end", id);
  }

  void note(const char* what, int id) {
    std::printf("t=%8lld  %-12s %s\n", (long long)now_, what, T(id).name.c_str());
  }
};

int main(int argc, char** argv) {
  const std::string mode = argc > 1 ? argv[1] : "rr";
  Sim s;
  Fifo fifo; Rr rr;
  if (mode == "fifo") s.attach(fifo); else s.attach(rr);
  const int ed = s.add("editor", 0, {{Op::WAIT, 0}, {Op::RUN, 3000},
                                     {Op::WAIT, 0}, {Op::RUN, 2000}, {Op::WAIT, 0}}, 50000);
  s.add("hog", 0, {{Op::RUN, 20000}, {Op::EXIT, 0}});
  s.wake(10000, ed);
  s.wake(30000, ed);
  Params p;                     // kNoHorizon = 슬라이스 없음
  s.run(p);
}
