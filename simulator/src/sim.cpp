// A one-lane discrete-event scheduler simulator.
//
// The core (`Sim`) owns the clock, the event queue, the task programs and the trace.
// The scheduling policy sits behind `Policy` — the "scheduler seat" of
// docs/simulator/simulator-guide.md §5: the core consults it only at decision points,
// it sees nothing but scheduling-relevant task state, and adding a policy must not
// require touching the core. `Fifo` at the bottom of this file is that claim's test —
// it was added without a line of change inside `Sim`.

#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <deque>
#include <queue>
#include <utility>
#include <vector>

using i64 = std::int64_t;

enum class Op { RUN, SLEEP, WAIT, EXIT };  //operations
struct Instr { Op op; i64 us; };

enum class State { Ready, Running, Blocked, Done };

struct Task {
  const char* name;
  std::vector<Instr> prog;
  std::size_t pc = 0;
  State state = State::Blocked;

  i64 run_left = 0;       // demand left on the current RUN instruction
  std::uint64_t gen = 0;  // stale check for an already-scheduled Lane event
  char blocked_by = 'w';  // why the task last blocked: 'w'=WAIT (external wake), 's'=SLEEP (self-timer)
};

// ─────────────────────────── the scheduler seat ───────────────────────────
// One config-schedule entry's scheduler settings. Defaults are the boot default
// (docs/recognition-vocabulary.md §2 provenance table — OSTEP §8's worked example
// whole: 3 queues, 10 ms, doubling, 100 ms boost). Parameters are configuration,
// never constants in code: this struct is where a config schedule will land
constexpr i64 kNoHorizon = -1;  // the policy sets no preemption horizon

struct Params {
  int num_queues        = 3;
  i64 timeslice_us      = 10000;
  int timeslice_growth  = 2;
  i64 boost_interval_us = 100000;
};

// Why a task left the lane. The first two leave it runnable — the policy puts it
// back wherever its own rules say; the last two take it off the ready set entirely
enum class Yield { SliceEnd, Preempted, Blocked, Ended };

// The core's trace writer — the only output a policy gets. It never formats a
// timestamp or a task name itself
struct Trace {
  virtual ~Trace() = default;
  virtual void note(const char* what, int task, const char* detail = nullptr) = 0;
  virtual void note(const char* what) = 0;
};

// The core's clock and event queue, as much of them as a policy may touch:
// read the time, place a future moment of your own on the queue
struct Clock {
  virtual ~Clock() = default;
  virtual i64 now() const = 0;
  virtual void arm(i64 t, int tag) = 0;  // delivers Policy::on_timer(tag) at t
};

struct Policy {
  virtual ~Policy() = default;

  virtual void start(const Params& p) = 0;   // settings take effect (t = 0, or a mid-run config entry)
  virtual void on_ready(int id) = 0;         // task became runnable — arrival, wake, or a satisfied RUN
  virtual void on_yield(int id, Yield why) = 0;  // task left the lane; reinsert it or drop it
  virtual int  pick() = 0;                   // next lane holder, -1 for idle; removes it from the ready set
  virtual i64  horizon(int id) = 0;          // lane time the holder may still take, or kNoHorizon
  virtual void charge(int id, i64 ran) = 0;  // lane time delivered, settled at every release
  virtual bool preempts(int challenger, int holder) = 0;  // a newly runnable task against the holder
  virtual void on_timer(int tag) { (void)tag; }           // a timer this policy armed has fired
};

static void erase_from(std::deque<int>& q, int id) {
  q.erase(std::remove(q.begin(), q.end(), id), q.end());
}

// ─────────────────────────────────── MLFQ ─────────────────────────────────
// The five textbook rules (simulator-guide §5), parameterised by `Params`.
// Every scrap of MLFQ state lives in here — the core knows none of it
struct Mlfq : Policy {
  static constexpr int kBoost = 1;

  struct St {
    int level = 0;  // 0 = topmost queue
    i64 allot = 0;  // CPU consumed so far at this level — a voluntary block does not reset it
                    // (ostep §8.4 rule 4: "regardless of how many times it has
                    //  given up the CPU". Not the retired rules 4a/4b)
  };

  Trace& trace;
  Clock& clock;
  Params p;
  std::vector<std::deque<int>> ready;
  std::vector<St> st;

  Mlfq(Trace& tr, Clock& cl) : trace(tr), clock(cl) {}

  St& slot(int id) {
    if (static_cast<int>(st.size()) <= id) st.resize(id + 1);
    return st[id];
  }

  i64 slice_of(int level) const {
    i64 s = p.timeslice_us;
    for (int i = 0; i < level; ++i) s *= p.timeslice_growth;
    return s;
  }

  // A cold start: everything pending is re-sorted into the top queue and the boost
  // timer restarts here (memo 2026-09-08-algorithm-switch-semantics §1, §7)
  void start(const Params& np) override {
    std::vector<int> waiting = drain();
    p = np;
    ready.assign(p.num_queues, {});
    for (St& s : st) { s.level = 0; s.allot = 0; }
    for (int id : waiting) ready[0].push_back(id);
    clock.arm(clock.now() + p.boost_interval_us, kBoost);
  }

  void on_ready(int id) override { ready[slot(id).level].push_back(id); }

  void on_yield(int id, Yield why) override {
    St& s = slot(id);
    switch (why) {
      case Yield::SliceEnd: {  // rule 4: burned the allotment at this level — demote
        if (s.level + 1 < p.num_queues) ++s.level;  // at the bottom queue, round-robin within it
        s.allot = 0;
        ready[s.level].push_back(id);
        char detail[32];
        std::snprintf(detail, sizeof detail, "level=%d", s.level);
        trace.note("x_mlfq_level", id, detail);
        break;
      }
      case Yield::Preempted:  // rule 1 victim: same level, allotment kept
        ready[s.level].push_back(id);
        break;
      case Yield::Blocked:  // rule 4 again: blocking early keeps both level and allotment
      case Yield::Ended:
        for (auto& q : ready) erase_from(q, id);  // a depart can hit a queued task
        break;
    }
  }

  // rule 1 + rule 2: the front of the highest non-empty queue, round-robin within it
  int pick() override {
    for (auto& q : ready) {
      if (q.empty()) continue;
      int id = q.front();
      q.pop_front();
      return id;
    }
    return -1;
  }

  i64 horizon(int id) override {
    St& s = slot(id);
    return slice_of(s.level) - s.allot;  // allotment left at this level
  }

  void charge(int id, i64 ran) override { slot(id).allot += ran; }

  // rule 1: a higher level waking up preempts at once
  bool preempts(int challenger, int holder) override {
    return slot(challenger).level < slot(holder).level;
  }

  // rule 5: everyone back to the topmost queue. The holder does not give up the lane —
  // it is topmost after the boost too, so there is nothing to switch to — but its
  // allotment is reset like everyone else's and the core re-arms it a fresh slice
  void on_timer(int) override {
    std::vector<int> waiting = drain();
    std::sort(waiting.begin(), waiting.end());  // deterministic rebuild; id is the tie-break (guide §9.3)
    for (St& s : st) { s.level = 0; s.allot = 0; }
    for (int id : waiting) ready[0].push_back(id);
    trace.note("x_mlfq_boost");
    clock.arm(clock.now() + p.boost_interval_us, kBoost);
  }

 private:
  std::vector<int> drain() {
    std::vector<int> waiting;
    for (auto& q : ready) {
      for (int id : q) waiting.push_back(id);
      q.clear();
    }
    return waiting;
  }
};

// ─────────────────────────────────── core ─────────────────────────────────
enum class Kind { Arrive, Lane, Wake, Unblock, Depart, PolicyTimer };  //event state
                                     // Wake = external (a channel/id, may find no waiter)
                                     // Unblock = a SLEEP/TIMER expiry the task scheduled for itself

struct Event {
  i64 t;
  std::uint64_t seq;  // tie breaker
  Kind kind;
  int task;
  std::uint64_t gen;  // task.gen at scheduling time — a mismatch means the reservation is void
  int tag;            // PolicyTimer only: handed back to the policy that armed it
};

struct Later {
  bool operator()(const Event& a, const Event& b) const {
    return a.t != b.t ? a.t > b.t : a.seq > b.seq;
  }
};

struct Sim : Trace, Clock {
  std::vector<Task> tasks;

  void attach(Policy& p) { pol = &p; }

  int add(const char* name, i64 t, std::vector<Instr> prog, i64 depart = -1) {
    tasks.push_back({name, std::move(prog), 0, State::Blocked, 0, 0});
    int id = static_cast<int>(tasks.size()) - 1;
    schedule(t, Kind::Arrive, id);
    if (depart >= 0) schedule(depart, Kind::Depart, id);
    return id;
  }

  void wake(i64 t, int id) { schedule(t, Kind::Wake, id); }

  void run(const Params& p) {
    pol->start(p);
    while (!q.empty()) {
      Event e = q.top();
      q.pop();
      now_ = e.t;

      switch (e.kind) {
        case Kind::Arrive: {
          Task& t = tasks[e.task];
          note("task_arrive", e.task);
          step(e.task);
          if (t.state == State::Ready) { enqueue(e.task); note("ready", e.task, "cause=arrive");
                                         maybe_preempt(e.task); }
          else note_settled(e.task);
          break;
        }
        case Kind::Wake:
          // External wake only lifts a WAIT — it must not cut a SLEEP short
          if (tasks[e.task].blocked_by == 'w') unblock(e.task, "cause=wake");
          break;
        case Kind::Unblock:
          // A SLEEP timer only wakes its own sleeper (a stale one after a re-block is ignored)
          if (tasks[e.task].blocked_by == 's') unblock(e.task, "cause=sleep_end");
          break;
        case Kind::Lane: {
          if (e.task != running || e.gen != tasks[e.task].gen) break;  // voided reservation
          int id = e.task;
          release();
          if (tasks[id].run_left == 0) {
            advance(id);                        // the RUN's demand is satisfied
          } else {                              // the horizon is exhausted
            note("run_end", id, "reason=preempt");
            yield_lane(id, Yield::SliceEnd);
          }
          break;
        }
        case Kind::Depart: {
          Task& t = tasks[e.task];
          note("depart", e.task);
          if (running == e.task) release();
          t.state = State::Done;
          pol->on_yield(e.task, Yield::Ended);  // off the ready set too, wherever it sat
          break;
        }
        case Kind::PolicyTimer: {
          int holder = running;
          if (holder >= 0) {
            release();  // settle the lane accounting before the policy looks at it
            if (tasks[holder].run_left == 0) { advance(holder); holder = -1; }  // boundary case
          }
          pol->on_timer(e.tag);
          if (holder >= 0) {
            if (pol->horizon(holder) == 0) {  // the policy revoked the lane at its own timer
              note("run_end", holder, "reason=preempt");
              yield_lane(holder, Yield::SliceEnd);
            } else {  // the holder keeps the lane — no switch happened, so nothing is traced
              running = holder;
              lane_start = now_;
              arm_lane(holder);
            }
          }
          break;
        }
      }

      dispatch();
    }
  }

  // ── Clock seam ──
  i64 now() const override { return now_; }

  void arm(i64 t, int tag) override {
    // Only while some task is still alive. Otherwise a periodic policy timer keeps the
    // queue non-empty forever (to be replaced by T_end once that lands)
    for (const Task& tk : tasks)
      if (tk.state != State::Done) { schedule(t, Kind::PolicyTimer, -1, 0, tag); return; }
  }

  // ── Trace seam ──
  void note(const char* what, int task, const char* detail = nullptr) override {
    std::printf("t=%6lld  %-12s %-8s%s%s\n", (long long)now_, what, tasks[task].name,
                detail ? "  " : "", detail ? detail : "");
  }

  void note(const char* what) override {
    std::printf("t=%6lld  %-12s\n", (long long)now_, what);
  }

 private:
  Policy* pol = nullptr;
  std::priority_queue<Event, std::vector<Event>, Later> q;
  std::uint64_t seq = 0;
  int running = -1;
  i64 lane_start = 0;  // when `running` took the lane
  i64 now_ = 0;

  void schedule(i64 t, Kind k, int task, std::uint64_t gen = 0, int tag = 0) {
    q.push({t, seq++, k, task, gen, tag});
  }

  // Advances the program only. The ready set, the lane and the queueing are all
  // the policy's or the caller's job (memo 2026-09-07-trace-clarifications-for-the-simulator §4).
  // Exception: SLEEP schedules its own timed Unblock here — a relative-time block is
  // part of executing that instruction, not a scheduling decision
  void step(int id) {
    Task& t = tasks[id];
    for (;;) {
      if (t.pc >= t.prog.size()) { t.state = State::Done; return; }  // ran out without EXIT — defensive
      const Instr& in = t.prog[t.pc];
      if (in.op == Op::RUN)   { t.state = State::Ready; t.run_left = in.us; return; }
      if (in.op == Op::SLEEP) { t.state = State::Blocked; t.blocked_by = 's';
                                schedule(now_ + in.us, Kind::Unblock, id); return; }  // relative wake at now+N
      if (in.op == Op::WAIT)  { t.state = State::Blocked; t.blocked_by = 'w'; return; }
      if (in.op == Op::EXIT)  { t.state = State::Done;    return; }
      ++t.pc;
    }
  }

  // Diagnostic line for when step() did not settle on Ready
  void note_settled(int id) {
    if (tasks[id].state == State::Blocked)   note("x_block", id);
    else if (tasks[id].state == State::Done) note("task_end", id);
  }

  // A blocked task becomes runnable again — the WAIT/SLEEP is over, advance past it.
  // Shared by external wake and SLEEP expiry; the caller supplies the trace cause
  void unblock(int id, const char* cause) {
    Task& t = tasks[id];
    if (t.state != State::Blocked) return;
    note("ready", id, cause);
    ++t.pc;
    step(id);
    if (t.state == State::Ready) { enqueue(id); maybe_preempt(id); }
    else note_settled(id);
  }

  void enqueue(int id) {
    tasks[id].state = State::Ready;
    pol->on_ready(id);
  }

  // Settle the lane task's accounting up to `now` and take it off. Any scheduled
  // Lane event is voided through gen
  void release() {
    Task& t = tasks[running];
    i64 ran = now_ - lane_start;
    t.run_left -= ran;
    pol->charge(running, ran);
    ++t.gen;
    running = -1;
  }

  void yield_lane(int id, Yield why) {
    if (why == Yield::SliceEnd || why == Yield::Preempted) tasks[id].state = State::Ready;
    pol->on_yield(id, why);
  }

  // One RUN instruction's demand is satisfied — look at the next instruction before deciding
  void advance(int id) {
    Task& t = tasks[id];
    ++t.pc;
    step(id);
    if (t.state == State::Ready) enqueue(id);
    else { note("run_end", id, t.state == State::Done ? "reason=exit" : "reason=block");
           note_settled(id);
           pol->on_yield(id, t.state == State::Done ? Yield::Ended : Yield::Blocked); }
  }

  void arm_lane(int id) {
    i64 h = pol->horizon(id);
    i64 dt = h == kNoHorizon ? tasks[id].run_left : std::min(tasks[id].run_left, h);
    schedule(now_ + dt, Kind::Lane, id, tasks[id].gen);
  }

  void dispatch() {
    if (running >= 0) return;
    int id = pol->pick();
    if (id < 0) return;
    running = id;
    tasks[id].state = State::Running;
    lane_start = now_;
    arm_lane(id);
    note("run_start", id);
  }

  void maybe_preempt(int challenger) {
    if (running < 0 || !pol->preempts(challenger, running)) return;
    int victim = running;
    release();
    note("run_end", victim, "reason=preempt");
    if (tasks[victim].run_left == 0) advance(victim);  // coincided with the boundary
    else yield_lane(victim, Yield::Preempted);
  }
};

// ─────────────────────────────────── FIFO ─────────────────────────────────
// The second policy. It exists to keep §5's obligation honest — "adding a second
// policy must not require touching the core" — and it reproduces the guide §4½
// walkthrough: non-preemptive run-until-block
struct Fifo : Policy {
  std::deque<int> q;

  void start(const Params&) override {}
  void on_ready(int id) override { q.push_back(id); }

  void on_yield(int id, Yield why) override {
    if (why == Yield::SliceEnd || why == Yield::Preempted) q.push_back(id);
    else erase_from(q, id);
  }

  int pick() override {
    if (q.empty()) return -1;
    int id = q.front();
    q.pop_front();
    return id;
  }

  i64 horizon(int) override { return kNoHorizon; }  // no slice: the holder keeps the lane until it blocks or exits
  void charge(int, i64) override {}
  bool preempts(int, int) override { return false; }
};

int main(int argc, char** argv) {
  bool use_fifo = argc > 1 && std::strcmp(argv[1], "fifo") == 0;

  Sim sim;
  Mlfq mlfq(sim, sim);
  Fifo fifo;
  if (use_fifo) sim.attach(fifo); else sim.attach(mlfq);

  // The guide §4½ miniature, hardcoded until the loader lands (guide §7, gate item 1)
  int editor = sim.add("editor", 0,
                       {{Op::WAIT, 0}, {Op::RUN, 3000},
                        {Op::WAIT, 0}, {Op::RUN, 2000},
                        {Op::WAIT, 0}}, 50000);
  sim.add("hog", 0, {{Op::RUN, 20000}, {Op::EXIT, 0}});

  sim.wake(10000, editor);
  sim.wake(30000, editor);

  Params p;              // the boot default, except for one illustration value:
  p.timeslice_us = 2000;  // guide §5 runs the miniature at 2 ms so the 20 ms hog is
                          // demoted twice. The boot default is 10 ms — a config-schedule
                          // entry's job to carry, not this file's
  sim.run(p);
}
