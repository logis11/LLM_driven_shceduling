// D — WAIT 과 외생 wake. "사람이 키를 누른다"가 시뮬레이션에 들어오는 길.
// 근거: 입력의 op 2종 중 나머지 하나가 wake 다 (7050개). WAIT 는 program 에 7147개.
// D2(§9.1) 대기자 없는 wake 는 **잃어버린다** — 잠정. M(채널)에서 우편함으로 바꾼다.
// 지금 wake 는 채널이 아니라 태스크 id 로 직행한다 — 채널 테이블도 M 에서.
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
  i64 run_left = 0;           // 현재 RUN 의 남은 수요
};

enum class EvKind { Arrive, Lane, Wake };
struct Event { i64 t; std::uint64_t seq; EvKind kind; int task; };

struct Later {
  bool operator()(const Event& a, const Event& b) const {
    return a.t != b.t ? a.t > b.t : a.seq > b.seq;
  }
};

class Sim {
 public:
  int add(std::string name, i64 t, std::vector<Instr> prog) {
    tasks_.push_back(Task{std::move(name), std::move(prog), 0, State::Blocked, 0});
    const int id = static_cast<int>(tasks_.size()) - 1;
    push(t, EvKind::Arrive, id);
    return id;
  }

  void wake(i64 t, int id) { push(t, EvKind::Wake, id); }

  void run() {
    while (!q_.empty()) {
      const Event e = q_.top();
      q_.pop();
      assert(e.t >= now_);
      now_ = e.t;
      switch (e.kind) {
        case EvKind::Arrive: on_arrive(e.task); break;
        case EvKind::Lane:   on_lane(e);        break;
        case EvKind::Wake:   on_wake(e.task);   break;
      }
      dispatch();
    }
  }

 protected:
  std::vector<Task> tasks_;
  std::priority_queue<Event, std::vector<Event>, Later> q_;
  std::uint64_t seq_ = 0;
  std::deque<int> ready_;
  int running_ = -1;
  i64 lane_start_ = 0, now_ = 0;

  void push(i64 t, EvKind k, int task) { q_.push({t, seq_++, k, task}); }
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

  void ready(int id) { T(id).st = State::Ready; ready_.push_back(id); note("ready", id); }

  void on_arrive(int id) {
    note("task_arrive", id);
    step(id);
    if (T(id).st == State::Ready) ready(id); else settled(id);
  }

  void on_wake(int id) {
    if (T(id).st != State::Blocked) return;    // D2: 대기자가 없으면 편지는 버려진다
    ++T(id).pc;                                // WAIT 이 끝났다
    step(id);
    if (T(id).st == State::Ready) ready(id); else settled(id);
  }

  void on_lane(const Event& e) {
    if (e.task != running_) return;            // 낡은 예약. F 에서 조건이 하나 는다
    const int id = e.task;
    T(id).run_left -= now_ - lane_start_;
    assert(T(id).run_left == 0);               // 비선점이므로 정확히 소진된다
    running_ = -1;
    ++T(id).pc;
    step(id);
    note("run_end", id);
    if (T(id).st == State::Ready) ready(id); else settled(id);
  }

  void dispatch() {
    if (running_ >= 0 || ready_.empty()) return;
    const int id = ready_.front();
    ready_.pop_front();
    running_ = id;
    T(id).st = State::Running;
    lane_start_ = now_;
    push(now_ + T(id).run_left, EvKind::Lane, id);
    note("run_start", id);
  }

  void settled(int id) {  // step() 이 Ready 로 안착하지 못했을 때
    note(T(id).st == State::Blocked ? "x_block" : "task_end", id);
  }

  void note(const char* what, int id) {
    std::printf("t=%8lld  %-12s %s\n", (long long)now_, what, T(id).name.c_str());
  }
};

int main() {
  Sim s;
  const int ed = s.add("editor", 0, {{Op::WAIT, 0}, {Op::RUN, 3000},
                                     {Op::WAIT, 0}, {Op::RUN, 2000}, {Op::WAIT, 0}});
  s.add("hog", 0, {{Op::RUN, 20000}, {Op::EXIT, 0}});
  s.wake(10000, ed);
  s.wake(30000, ed);
  s.run();
}
