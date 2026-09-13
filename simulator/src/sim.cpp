#include <algorithm>
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

// ── MLFQ boot default (docs/recognition-vocabulary.md §2 provenance table) ──
constexpr int NUM_QUEUES       = 3;       // ostep §8.2 "a three-queue scheduler"
constexpr i64 TIMESLICE_US     = 2000;
constexpr int TIMESLICE_GROWTH = 2;       // ostep Fig. 8.6 
constexpr i64 BOOST_INTERVAL   = 100000;  // ostep Fig. 8.4 — rule 5 

static i64 slice_of(int level) {
  i64 s = TIMESLICE_US;
  for (int i = 0; i < level; ++i) s *= TIMESLICE_GROWTH;
  return s;
}

struct Task {
  const char* name;
  std::vector<Instr> prog;
  std::size_t pc = 0;
  State state = State::Blocked;

  // MLFQ state. Not a class attribute — state owned by the algorithm itself
  int level = 0;          // 0 = topmost queue
  i64 allot = 0;          // CPU consumed so far at this level — a voluntary block does not reset it
                          // (ostep §8.4 rule 4: "regardless of how many times it has
                          //  given up the CPU". Not the retired rules 4a/4b)
  i64 run_left = 0;       // demand left on the current RUN instruction
  std::uint64_t gen = 0;  // stale check for an already-scheduled Lane event
};

enum class Kind { Arrive, Lane, Wake, Depart, Boost }; //event state

struct Event {
  i64 t;
  std::uint64_t seq;  // tie breaker
  Kind kind;
  int task;
  std::uint64_t gen;  // task.gen at scheduling time — a mismatch means the reservation is void
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
  auto schedule = [&](i64 t, Kind k, int task, std::uint64_t gen = 0) {
    q.push({t, seq++, k, task, gen});
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

  schedule(BOOST_INTERVAL, Kind::Boost, -1);

  std::vector<std::deque<int>> ready(NUM_QUEUES);
  int running = -1;
  i64 lane_start = 0;  // when `running` took the lane
  i64 now = 0;

  auto log = [&](const char* what, int id, const char* note = nullptr) {
    std::printf("t=%6lld  %-12s %-8s%s%s\n", (long long)now, what, tasks[id].name,
                note ? "  " : "", note ? note : "");
  };

  // Advances the program only. The ready queues, the lane and the queueing are all
  // the caller's job (memo 2026-09-07-trace-clarifications-for-the-simulator §4)
  auto step = [&](int id) {
    Task& t = tasks[id];
    for (;;) {
      if (t.pc >= t.prog.size()) { t.state = State::Done; return; }  // ran out without EXIT — defensive
      const Instr& in = t.prog[t.pc];
      if (in.op == Op::RUN)  { t.state = State::Ready; t.run_left = in.us; return; }
      if (in.op == Op::WAIT) { t.state = State::Blocked; return; }
      if (in.op == Op::EXIT) { t.state = State::Done;    return; }
      ++t.pc;
    }
  };

  // Diagnostic line for when step() did not settle on Ready
  auto log_settled = [&](int id) {
    if (tasks[id].state == State::Blocked)   log("x_block", id);
    else if (tasks[id].state == State::Done) log("task_end", id);
  };

  auto enqueue = [&](int id) {
    tasks[id].state = State::Ready;
    ready[tasks[id].level].push_back(id);
  };

  // Settle the lane task's accounting up to `now` and take it off. Any scheduled
  // Lane event is voided through gen
  auto release = [&]() {
    Task& t = tasks[running];
    i64 ran = now - lane_start;
    t.run_left -= ran;
    t.allot    += ran;
    ++t.gen;
    running = -1;
  };

  // One RUN instruction's demand is satisfied — look at the next instruction before deciding
  auto advance = [&](int id) {
    Task& t = tasks[id];
    ++t.pc;
    step(id);
    if (t.state == State::Ready) enqueue(id);
    else { log("run_end", id, t.state == State::Done ? "reason=exit" : "reason=block");
           log_settled(id); }
  };

  // rule 1 + rule 2: take the front of the highest non-empty queue, round-robin within it
  auto dispatch = [&]() {
    if (running >= 0) return;
    for (int L = 0; L < NUM_QUEUES; ++L) {
      if (ready[L].empty()) continue;
      running = ready[L].front();
      ready[L].pop_front();
      Task& t = tasks[running];
      t.state = State::Running;
      lane_start = now;
      i64 quantum = slice_of(t.level) - t.allot;  // allotment left at this level
      i64 dt = std::min(t.run_left, quantum);
      schedule(now + dt, Kind::Lane, running, t.gen);
      log("run_start", running);
      return;
    }
  };

  // rule 1: a higher level waking up preempts at once. No demotion, no allot reset
  auto maybe_preempt = [&](int id) {
    if (running < 0 || tasks[id].level >= tasks[running].level) return;
    int victim = running;
    release();
    log("run_end", victim, "reason=preempt");
    if (tasks[victim].run_left == 0) advance(victim);  // coincided with the boundary
    else enqueue(victim);
  };

  while (!q.empty()) {
    Event e = q.top();
    q.pop();
    now = e.t;

    switch (e.kind) {
      case Kind::Arrive: {
        Task& t = tasks[e.task];
        log("task_arrive", e.task);
        step(e.task);
        if (t.state == State::Ready) { enqueue(e.task); log("ready", e.task, "cause=arrive");
                                       maybe_preempt(e.task); }
        else log_settled(e.task);
        break;
      }
      case Kind::Wake: {
        Task& t = tasks[e.task];
        if (t.state == State::Blocked) {
          log("ready", e.task, "cause=wake");  // WAIT is over — blocked or not, it lands here
          ++t.pc;
          step(e.task);
          if (t.state == State::Ready) { enqueue(e.task); maybe_preempt(e.task); }
          else log_settled(e.task);
        }
        break;
      }
      case Kind::Lane: {
        if (e.task != running || e.gen != tasks[e.task].gen) break;  // voided reservation
        int id = e.task;
        release();
        Task& t = tasks[id];
        if (t.run_left == 0) {
          advance(id);                     // the RUN's demand is satisfied
        } else {                           // allotment exhausted — rule 4
          log("run_end", id, "reason=preempt");
          if (t.level + 1 < NUM_QUEUES) ++t.level;   // at the bottom queue, round-robin within it
          t.allot = 0;
          enqueue(id);
          char note[32];
          std::snprintf(note, sizeof note, "level=%d", t.level);
          log("x_mlfq_level", id, note);
        }
        break;
      }
      case Kind::Depart: {
        Task& t = tasks[e.task];
        log("depart", e.task);
        if (running == e.task) { release(); }
        t.state = State::Done;
        break;
      }
      case Kind::Boost: {                  // rule 5: move everyone to the topmost queue
        int cur = running;                 // the running task does not give up the lane —
        if (cur >= 0) {                    // it is topmost after the boost too, so there is
          release();                       // nothing to switch to; settle accounting, void the
          if (tasks[cur].run_left == 0) { advance(cur); cur = -1; }  // reservation. Boundary case
        }
        for (int L = 0; L < NUM_QUEUES; ++L) ready[L].clear();
        for (int i = 0; i < (int)tasks.size(); ++i) {
          Task& t = tasks[i];
          t.level = 0;
          t.allot = 0;
          if (i != cur && t.state == State::Ready) enqueue(i);
        }
        if (cur >= 0) {
          Task& t = tasks[cur];
          running = cur;
          lane_start = now;
          schedule(now + std::min(t.run_left, slice_of(0)), Kind::Lane, cur, t.gen);
        }
        std::printf("t=%6lld  %-12s\n", (long long)now, "x_mlfq_boost");
        // Arm the next boost only while some task is still alive. Otherwise this one event
        // keeps the queue non-empty forever (to be replaced by T_end once that lands)
        for (const Task& t : tasks)
          if (t.state != State::Done) { schedule(now + BOOST_INTERVAL, Kind::Boost, -1); break; }
        break;
      }
    }

    dispatch();
  }
}
