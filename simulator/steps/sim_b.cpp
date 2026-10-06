// B — 태스크와 프로그램. 도착해서 ready set 에 들어가는 데까지. 아직 아무도 안 뛴다.
// 근거: 파일의 arrive 이벤트가 program 을 통째로 싣고 온다 → Instr/Task 가 먼저다.
// A 를 고친 곳: Event.what(int) → kind+task. 이벤트가 "누구의" 일인지 알아야 한다.
#include <cassert>
#include <cstdint>
#include <cstdio>
#include <deque>
#include <queue>
#include <string>
#include <utility>
#include <vector>

using i64 = std::int64_t;

enum class Op { RUN, EXIT };
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

enum class EvKind { Arrive };
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

  void run() {
    while (!q_.empty()) {
      const Event e = q_.top();
      q_.pop();
      assert(e.t >= now_);
      now_ = e.t;
      switch (e.kind) {
        case EvKind::Arrive: on_arrive(e.task); break;
      }
    }
  }

 protected:
  std::vector<Task> tasks_;
  std::priority_queue<Event, std::vector<Event>, Later> q_;
  std::uint64_t seq_ = 0;
  std::deque<int> ready_;
  i64 now_ = 0;

  void push(i64 t, EvKind k, int task) { q_.push({t, seq_++, k, task}); }
  Task& T(int id) { return tasks_[static_cast<std::size_t>(id)]; }

  // 프로그램만 전진시킨다. ready set 투입도 레인 배정도 호출자의 몫
  void step(int id) {
    Task& t = T(id);
    for (;;) {
      if (t.pc >= t.prog.size()) { t.st = State::Done; return; }
      switch (t.prog[t.pc].op) {
        case Op::RUN:  t.st = State::Ready; t.run_left = t.prog[t.pc].us; return;
        case Op::EXIT: t.st = State::Done;  return;
      }
    }
  }

  void ready(int id) { T(id).st = State::Ready; ready_.push_back(id); note("ready", id); }

  void on_arrive(int id) {
    note("task_arrive", id);
    step(id);
    if (T(id).st == State::Ready) ready(id); else note("task_end", id);
  }

  void note(const char* what, int id) {
    std::printf("t=%8lld  %-12s %s\n", (long long)now_, what, T(id).name.c_str());
  }
};

int main() {
  Sim s;
  s.add("hog", 0, {{Op::RUN, 20000}, {Op::EXIT, 0}});
  s.add("quick", 5000, {{Op::RUN, 1000}, {Op::EXIT, 0}});
  s.add("empty", 1000, {{Op::EXIT, 0}});   // 도착하자마자 끝나는 태스크
  s.run();
}
