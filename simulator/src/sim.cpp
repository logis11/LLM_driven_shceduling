#include <cstdint>
#include <cstdio>
#include <deque>
#include <queue>
#include <utility>
#include <vector>

using i64 = std::int64_t;

enum class Op { RUN, WAIT, EXIT };  //operations
struct Instr { Op op; i64 us; };

enum class State { Ready, Running, Blocked, Done };

struct Task {
  const char* name;
  std::vector<Instr> prog;
  std::size_t pc = 0;
  State state = State::Blocked;
};

enum class Kind { Arrive, RunEnd, Wake, Depart }; //event state

struct Event {
  i64 t;
  std::uint64_t seq;  // tie breaker
  Kind kind;
  int task;
};

struct Later {
  bool operator()(const Event& a, const Event& b) const {
    return a.t != b.t ? a.t > b.t : a.seq > b.seq;
  }
};

int main() {

  std::vector<Task> tasks;
  std::priority_queue<Event, std::vector<Event>, Later> q;
  std::uint64_t seq = 0;
  auto schedule = [&](i64 t, Kind k, int task) {
    q.push({t, seq++, k, task});
  };


  auto arrive = [&](const char* name, i64 t, std::vector<Instr> prog, i64 depart = -1) {
    tasks.push_back({name, std::move(prog)});
    int id = static_cast<int>(tasks.size()) - 1;
    schedule(t, Kind::Arrive, id);
    if (depart >= 0) schedule(depart, Kind::Depart, id);
    return id;
  };

  int editor = arrive("editor", 0,
                      {{Op::WAIT, 0}, {Op::RUN, 3000},
                       {Op::WAIT, 0}, {Op::RUN, 2000},
                       {Op::WAIT, 0}}, 50000);
  arrive("hog", 0, {{Op::RUN, 20000}, {Op::EXIT, 0}});

 
  schedule(10000, Kind::Wake, editor);
  schedule(30000, Kind::Wake, editor);

  std::deque<int> ready;
  int running = -1;
  i64 now = 0;

  auto log = [&](const char* what, int id, const char* cause = nullptr) {
    std::printf("t=%6lld  %-12s %-8s%s%s\n", (long long)now, what, tasks[id].name,
                cause ? "  cause=" : "", cause ? cause : "");
  };

  // (memo 2026-09-07-trace-clarifications-for-the-simulator §4)
  auto step = [&](int id) {
    Task& t = tasks[id];
    for (;;) {
      if (t.pc >= t.prog.size()) { t.state = State::Done; log("task_end", id); return; }
      const Instr& in = t.prog[t.pc];
      if (in.op == Op::RUN)  { t.state = State::Ready;   ready.push_back(id);   return; }
      if (in.op == Op::WAIT) { t.state = State::Blocked;                      log("x_block", id); return; }
      if (in.op == Op::EXIT) { t.state = State::Done;                         log("task_end", id); return; }
      ++t.pc;
    }
  };

  while (!q.empty()) {
    Event e = q.top();
    q.pop();
    now = e.t;
    Task& t = tasks[e.task];  

    switch (e.kind) {
      case Kind::Arrive:
        log("task_arrive", e.task);
        step(e.task);
        if (t.state == State::Ready) log("ready", e.task, "arrive");
        break;
      case Kind::Wake:
        if (t.state == State::Blocked) {
          log("ready", e.task, "wake");  // WAIT 완료 — 블록했든 안 했든 이 자리에서
          ++t.pc;
          step(e.task);
        }
        break;
      case Kind::RunEnd:
        log("run_end", e.task);
        running = -1;
        ++t.pc; 
        step(e.task);
        break;
      case Kind::Depart:
        log("depart", e.task);
        t.state = State::Done;
        if (running == e.task) running = -1;
        break;
    }

    // TODO add more scheduling methods
    if (running < 0 && !ready.empty()) {
      running = ready.front();
      ready.pop_front();
      tasks[running].state = State::Running;
      log("run_start", running);
      schedule(now + tasks[running].prog[tasks[running].pc].us, Kind::RunEnd, running);
    }
  }
}
