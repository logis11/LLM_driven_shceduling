// A one-lane discrete-event scheduler simulator.
//
// The core (`Sim`) owns the clock, the event queue, the task programs and the trace.
// The scheduling policy sits behind `Policy` — the "scheduler seat" of
// docs/simulator/simulator-guide.md §5: the core consults it only at decision points,
// it sees nothing but scheduling-relevant task state, and adding a policy must not
// require touching the core. `Fifo` is that claim's test — it was added without a line
// of change inside `Sim`.
//
// Built up in stages (see notes/ for the one-rung-at-a-time ladder). What each stage adds:
//   A clock+queue · B Instr/Task/step · C lane+dispatch · D WAIT+wake · E depart
//   F timeslice+preemption+gen · G Policy extracted · H Trace/Clock seam + MLFQ rules 1–4
//   I MLFQ rule 5 (boost) via Clock::arm · J SLEEP · K TIMER+backlog · L LOOP flattening
//   M channels + WAKE + mailbox · N FORK/spawn_table · O JSONL trace (data-contracts §9)
//   P deadline events · Q workload loader (mini_json) · R config schedule + handoff
//
// Design notes worth carrying:
//   · gen (F): a preempted Lane reservation cannot be removed from a priority_queue, so
//     it is stamped with the task's generation and voided on mismatch when it fires.
//   · SLEEP vs TIMER (J/K): SLEEP is relative (now+N); TIMER is an absolute grid
//     (t0 + k·P) so a slow scheduler cannot make the workload lighter by dropping frames —
//     missed ticks pile into a backlog and are consumed at once.
//   · channels (M): an external wake with no waiter is not lost — it goes to a mailbox.
//     Losing it would shrink a starved task's demand and hide the harm being measured.
//   · FORK (N): tasks are born at runtime, so tasks_ is a std::deque — a vector realloc
//     would dangle the `Task&` held across a step().
//   · loader (Q): the loader parses, validates (reject the whole file on any violation),
//     transforms (string ids→indices, nested LOOP→flat, 2-pass forward refs), and
//     isolates — ground_truth is never named by any structure the core can see.

#include "mini_json.hpp"
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <cstdio>
#include <cstring>
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

// One entry of a FORK spawn table — a child spec straight from the file (id/name/program)
struct ChildSpec { std::string name; std::vector<Instr> prog; };

// Ready vs Running: the scheduler *picks from* the Ready set
enum class State { Ready, Running, Blocked, Done };

struct Task {
  std::string sid;            // the file's string id — the trace goes out under this
  std::string name;           // label; no scheduling ever branches on it
  std::vector<Instr> prog;
  std::size_t pc = 0;
  State st = State::Blocked;
  i64 run_left = 0;           // demand left on the current RUN — preserved across preemption
  i64 timer_next = -1;        // this task's next grid tick; -1 = t0 not yet fixed
  bool job_open = false; i64 job_tick = 0, job_period = 0;   // an open periodic job
  std::vector<i64> loop_left; // remaining iterations of nested loops (-1 = unbounded)
  int wait_chan = -1;         // channel currently blocked on (-1 = not a channel wait)
  int mailbox = 0;            // WAKEs that arrived with no waiter (task-addressed)
  std::vector<ChildSpec> spawn_table;  // consumed in order
  int fork_cap = 0, live_children = 0, parent = -1;
  std::size_t spawn_next = 0;
  i64 born = -1, ended = -1;  // born is the emergence time — meaningful only for FORK children
  char blocked_by = 'w';      // why last blocked: w=wait s=sleep t=timer f=fork_slot
  std::uint64_t gen = 0;      // bumped each time the lane is released = reservation void
};

constexpr i64 kNoHorizon = -1;  // the policy sets no preemption horizon

// Frozen-schema MLFQ params (recognition-vocabulary §2 — OSTEP §8's worked example whole).
// Parameters are configuration, never constants in code
struct Params {
  int num_queues        = 3;
  i64 timeslice_us      = 10000;
  int timeslice_growth  = 2;
  i64 boost_interval_us = 100000;
};

// The core's trace writer as a policy sees it — x_ diagnostic lines only
struct Trace {
  virtual ~Trace() = default;
  virtual void note(const char* what, int task) = 0;
  virtual void note(const char* what) = 0;
};

// The core's clock, as much of it as a policy may touch
struct Clock {
  virtual ~Clock() = default;
  virtual i64 now() const = 0;
  virtual void arm(i64 t, int tag) = 0;  // delivers Policy::on_timer(tag) at t
};

// Why a task left the lane. The first two leave it runnable; the last two take it off
enum class Yield { SliceEnd, Preempted, Blocked, Ended };

struct Policy {
  virtual ~Policy() = default;
  virtual void start(const Params&) = 0;
  virtual void on_ready(int id) = 0;
  virtual void on_yield(int id, Yield why) = 0;
  virtual int  pick() = 0;                  // next lane holder, -1 for idle
  virtual i64  horizon(int id) = 0;         // lane time the holder may still take
  virtual bool preempts(int challenger, int holder) = 0;
  virtual void charge(int id, i64 ran) = 0; // lane time delivered, settled at every release
  virtual void on_timer(int tag) { (void)tag; }
  virtual std::vector<int> handoff() = 0;   // empties the ready set and hands it out (algo switch)
};

// The second policy — non-preemptive run-until-block (stage E's behaviour)
struct Fifo : Policy {
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
  std::vector<int> handoff() override {
    std::vector<int> o(q.begin(), q.end()); q.clear(); return o;
  }
};

// The five textbook rules (simulator-guide §5), parameterised by Params.
// Every scrap of MLFQ state lives here — the core knows none of it
struct Mlfq : Policy {
  struct St { int level = 0; i64 allot = 0; };  // allot: CPU consumed at this level
  Trace& trace;
  Clock& clock;
  Params p;
  std::vector<std::deque<int>> ready;           // the *structure* of the ready set is the policy
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
  static constexpr int kBoost = 1;              // our tag; opaque to the core
  void start(const Params& np) override {
    p = np;
    ready.assign((std::size_t)p.num_queues, {});
    clock.arm(clock.now() + p.boost_interval_us, kBoost);
  }
  void on_timer(int) override {                 // rule 5: everyone back to the top queue
    std::vector<int> w;
    for (auto& q : ready) { for (int id : q) w.push_back(id); q.clear(); }
    std::sort(w.begin(), w.end());              // deterministic rebuild; id is the tie-break
    for (St& s : st) { s.level = 0; s.allot = 0; }
    for (int id : w) ready[0].push_back(id);
    trace.note("x_mlfq_boost");
    clock.arm(clock.now() + p.boost_interval_us, kBoost);
  }
  void on_ready(int id) override {
    assert(!ready.empty());   // receiving a task without start() dies loudly here
    ready[(std::size_t)slot(id).level].push_back(id);
  }
  void on_yield(int id, Yield why) override {
    St& s = slot(id);
    if (why == Yield::SliceEnd) {               // rule 3: burned the allotment → demote
      if (s.level + 1 < p.num_queues) ++s.level;
      s.allot = 0;
      ready[(std::size_t)s.level].push_back(id);
      trace.note("x_mlfq_demote", id);
    } else if (why == Yield::Preempted) {       // keep level and allotment
      ready[(std::size_t)s.level].push_back(id);
    } else {                                    // rule 4: blocking keeps both level and allotment
      for (auto& q : ready) q.erase(std::remove(q.begin(), q.end(), id), q.end());
    }
  }
  int pick() override {                         // rules 1 + 2
    for (auto& q : ready)
      if (!q.empty()) { int id = q.front(); q.pop_front(); return id; }
    return -1;
  }
  i64  horizon(int id) override { return slice_of(slot(id).level) - slot(id).allot; }
  void charge(int id, i64 ran) override { slot(id).allot += ran; }
  bool preempts(int c, int h) override { return slot(c).level < slot(h).level; }
  std::vector<int> handoff() override {
    std::vector<int> w;
    for (auto& qq : ready) { for (int id : qq) w.push_back(id); qq.clear(); }
    return w;
  }
};

// One line of a config schedule. The loader fills it; the core consumes it via ConfigApply
struct ConfigEntry { i64 t_us; std::string algorithm; Params params; std::string provenance; };

enum class Kind { Arrive, Lane, Wake, Unblock, Depart, PolicyTimer, ConfigApply };
struct Event { i64 t; std::uint64_t seq; Kind kind; int task; std::uint64_t gen = 0; int tag = 0; };

// D1 (guide §9.3): at equal µs, ① kind priority (config apply first) ② insertion order
static int prio_of(Kind k) { return k == Kind::ConfigApply ? 0 : 1; }

struct Later {
  bool operator()(const Event& a, const Event& b) const {
    if (a.t != b.t) return a.t > b.t;
    const int pa = prio_of(a.kind), pb = prio_of(b.kind);
    if (pa != pb) return pa > pb;
    return a.seq > b.seq;
  }
};

class Sim : public Trace, public Clock {
 public:
  // ── Trace / Clock seams ──
  i64 now() const override { return now_; }
  void note(const char* what, int id) override {           // a policy's x_ line
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

  // ── contract events (data-contracts §9) ──
  void ev(const char* name, int id, const char* k1 = nullptr, const char* v1 = nullptr,
          const char* k2 = nullptr, const char* v2 = nullptr) {
    std::printf("{\"event\":\"%s\",\"t\":%lld,\"task\":\"%s\"", name, (long long)now_,
                tasks_[(std::size_t)id].sid.c_str());
    if (k1) std::printf(",\"%s\":\"%s\"", k1, v1);
    if (k2) std::printf(",\"%s\":\"%s\"", k2, v2);
    std::printf("}\n");
  }

  // A policy timer re-arms only while other work remains. "some task alive" is not enough:
  // a task blocked forever (no more wake, no depart) is not Done but is dead, and then the
  // boost fills the queue by itself and pushes the clock forward without end. When this
  // timer is popped, q_ is the entire future — empty means the run is over
  void arm(i64 t, int tag) override {
    if (q_.empty()) return;
    for (const Task& tk : tasks_)
      if (tk.st != State::Done) { q_.push({t, seq_++, Kind::PolicyTimer, -1, 0, tag}); return; }
  }

  int add(std::string sid, i64 t, std::vector<Instr> prog, i64 depart = -1) {
    Task nt; nt.sid = sid; nt.name = std::move(sid); nt.prog = std::move(prog);
    tasks_.push_back(std::move(nt));
    const int id = static_cast<int>(tasks_.size()) - 1;
    push(t, Kind::Arrive, id);
    if (depart >= 0) push(depart, Kind::Depart, id);   // segment-bound
    return id;
  }

  int channel(const std::string& name) {          // string channel → index (the loader's entry)
    auto it = chan_id_.find(name);
    if (it != chan_id_.end()) return it->second;
    const int c = (int)chan_waiters_.size();
    chan_id_.emplace(name, c);
    chan_waiters_.emplace_back();
    chan_pending_.push_back(0);
    return c;
  }
  // For forward references: a WAKE target may name a task not yet added. The loader reads
  // every arrive to build the name→index table *before* resolving any program
  void set_prog(int id, std::vector<Instr> prog) { T(id).prog = std::move(prog); }
  void set_spawn(int id, std::vector<ChildSpec> tab, int cap) {
    T(id).spawn_table = std::move(tab); T(id).fork_cap = cap;
  }
  void report() const {   // emergence-time summary — FORK children only
    i64 first = -1, last = -1, done = -1; int n = 0;
    for (const Task& t : tasks_) {
      if (t.parent < 0) continue;
      ++n;
      if (first < 0 || t.born < first) first = t.born;
      if (t.born > last) last = t.born;
      if (t.ended > done) done = t.ended;
    }
    if (n) std::fprintf(stderr, "children %d — first born %lld, last born %lld, all ended %lld\n",
                        n, (long long)first, (long long)last, (long long)done);
  }

  void wake(i64 t, int chan) { q_.push({t, seq_++, Kind::Wake, -1, 0, chan}); }

  explicit Sim(bool check_gen = true) : check_gen_(check_gen) {}
  void attach(Policy& p) { pol_ = &p; }

  void run(const Params& p) {
    std::printf("{\"event\":\"meta\",\"workload_id\":\"%s\",\"condition\":\"%s\","
                "\"sim\":\"src/sim\",\"schedule_entries\":%zu}\n", wid_.c_str(), cond_.c_str(),
                schedule_.size());
    if (schedule_.empty()) pol_->start(p);   // no schedule → start with the argument params
    while (!q_.empty()) {
      const Event e = q_.top();
      q_.pop();
      assert(e.t >= now_);
      now_ = e.t;
      switch (e.kind) {
        case Kind::Arrive:      on_arrive(e.task);      break;
        case Kind::Lane:        on_lane(e);             break;
        case Kind::Wake:        on_ext_wake(e.tag);     break;
        case Kind::Unblock:     on_unblock(e.task);     break;
        case Kind::Depart:      on_depart(e.task);      break;
        case Kind::PolicyTimer: on_policy_timer(e);     break;
        case Kind::ConfigApply: on_config_apply(e.tag); break;
      }
      dispatch();
    }
  }

  // ── registration / schedule wiring ──
  void set_meta(std::string w, std::string c) { wid_ = std::move(w); cond_ = std::move(c); }
  void register_policy(const std::string& algo, Policy& p) { registry_[algo] = &p; }

  void set_schedule(std::vector<ConfigEntry> sched) {
    if (sched.empty() || sched[0].t_us != 0) die("config schedule's first entry must be t_us:0");
    schedule_ = std::move(sched);
    for (std::size_t k = 0; k < schedule_.size(); ++k)
      q_.push({schedule_[k].t_us, seq_++, Kind::ConfigApply, -1, 0, (int)k});
  }

 private:
  std::deque<Task> tasks_;   // deque, not vector (FORK grows it mid-run — see header)
  std::priority_queue<Event, std::vector<Event>, Later> q_;
  std::uint64_t seq_ = 0;
  std::string wid_ = "hand", cond_ = "fixed";
  std::map<std::string, Policy*> registry_;
  std::vector<ConfigEntry> schedule_;
  Policy* pol_ = nullptr;
  int running_ = -1;
  i64 lane_start_ = 0, now_ = 0;
  bool check_gen_ = true;
  std::map<std::string, int> chan_id_;
  std::vector<std::deque<int>> chan_waiters_;
  std::vector<int> chan_pending_;               // channel mailboxes

  void push(i64 t, Kind k, int task, std::uint64_t gen = 0) { q_.push({t, seq_++, k, task, gen, 0}); }
  Task& T(int id) { return tasks_[static_cast<std::size_t>(id)]; }

  void on_config_apply(int idx) {
    const ConfigEntry& c = schedule_[(std::size_t)idx];
    auto it = registry_.find(c.algorithm);
    if (it == registry_.end()) die("unregistered algorithm: " + c.algorithm);
    std::printf("{\"event\":\"config_applied\",\"t\":%lld,\"index\":%d,"
                "\"algorithm\":\"%s\",\"provenance\":\"%s\"}\n",
                (long long)now_, idx, c.algorithm.c_str(), c.provenance.c_str());

    int holder = running_;
    if (holder >= 0) {                       // same pattern as I's PolicyTimer
      release();
      if (T(holder).run_left == 0) { advance(holder); holder = -1; }
    }
    std::vector<int> waiting = pol_->handoff();
    std::sort(waiting.begin(), waiting.end());   // deterministic handoff; id is the tie-break
    pol_ = it->second;
    pol_->start(c.params);
    for (int id : waiting) pol_->on_ready(id);
    if (holder >= 0) { running_ = holder; T(holder).st = State::Running;
                       lane_start_ = now_; arm_lane(holder); }
  }

  void on_policy_timer(const Event& e) {
    int holder = running_;
    if (holder >= 0) {
      release();
      if (T(holder).run_left == 0) { advance(holder); holder = -1; }   // coincided with the boundary
    }
    pol_->on_timer(e.tag);
    if (holder < 0) return;
    if (pol_->horizon(holder) == 0) { ev("run_end", holder, "reason", "preempt");
                                      yield_lane(holder, Yield::SliceEnd); }
    else { running_ = holder; T(holder).st = State::Running;           // no switch → nothing traced
           lane_start_ = now_; arm_lane(holder); }
  }

  // Lane accounting lives here alone — this is where "demand is preserved across preemption" is
  void release() {
    T(running_).run_left -= now_ - lane_start_;
    assert(T(running_).run_left >= 0);
    pol_->charge(running_, now_ - lane_start_);
    ++T(running_).gen;
    running_ = -1;
  }

  void advance(int id) {   // one RUN's demand satisfied — look at the next instruction
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

  // Advances the program only; the ready set, the lane and the queueing are the policy's or
  // the caller's job. Exceptions: SLEEP/TIMER schedule their own timed Unblock here, and
  // WAKE delivers here — a timed or instantaneous side effect is part of executing the op
  void step(int id) {
    Task& t = T(id);
    for (int guard = 0; ; ++guard) {
      if (guard > 1000000) { std::fprintf(stderr, "step: %s does not advance\n",
                                          t.name.c_str()); std::abort(); }
      if (t.pc >= t.prog.size()) { t.st = State::Done; return; }
      switch (t.prog[t.pc].op) {
        case Op::RUN:  t.st = State::Ready; t.run_left = t.prog[t.pc].us; return;
        case Op::SLEEP: t.st = State::Blocked; t.blocked_by = 's';
                        push(now_ + t.prog[t.pc].us, Kind::Unblock, id); return;
        case Op::TIMER: {
          const i64 P = t.prog[t.pc].period_us;
          if (t.job_open) {                               // judge the previous job's deadline
            const i64 d = t.job_tick + t.job_period;
            ev_deadline(id, d, now_ <= d, d - now_);
            t.job_open = false;
          }
          if (t.timer_next < 0) t.timer_next = now_;      // D4: t0 = first TIMER execution
          if (now_ >= t.timer_next) {                     // backlog → consume the tick at once
            t.job_tick = t.timer_next; t.job_period = P; t.job_open = true;
            t.timer_next += P; ++t.pc; break;
          }
          const i64 due = t.timer_next;                   // ahead of the grid — block until next tick
          t.job_tick = due; t.job_period = P; t.job_open = true;
          t.timer_next += P;
          t.st = State::Blocked; t.blocked_by = 't';
          push(due, Kind::Unblock, id);
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
          if (t.spawn_next >= t.spawn_table.size()) { ++t.pc; break; }   // table exhausted
          if (t.fork_cap > 0 && t.live_children >= t.fork_cap) {
            t.st = State::Blocked; t.blocked_by = 'f'; t.wait_chan = -1;  // wait for a slot
            return;                                                       // pc stays put
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

  void spawn(int parent_id) {
    Task& par = T(parent_id);
    Task c;
    c.name = par.spawn_table[par.spawn_next].name;
    c.sid = par.sid + "." + std::to_string(par.spawn_next + 1);
    c.prog = par.spawn_table[par.spawn_next].prog;
    c.parent = parent_id;
    ++par.spawn_next; ++par.live_children;
    tasks_.push_back(std::move(c));            // deque, so the par reference stays valid
    const int id = (int)tasks_.size() - 1;
    T(id).born = now_;
    ev("task_arrive", id, "source", "spawn", "parent", T(parent_id).sid.c_str());
    step(id);
    if (T(id).st == State::Ready) { enqueue(id, "arrive"); maybe_preempt(id); } else settled(id);
  }

  // Termination in one place. EXIT or depart, a parent's slot must come back exactly once —
  // twice and the cap leaks, never and the build stalls forever
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
  void on_unblock_fork(int id) {   // a slot opened — retry the same FORK (no pc advance)
    T(id).st = State::Ready;
    ev("ready", id, "cause", "fork_slot");
    step(id);
    if (T(id).st == State::Ready) { pol_->on_ready(id); maybe_preempt(id); } else settled(id);
  }

  void on_ext_wake(int c) {                     // external wake — channel-addressed
    auto& w = chan_waiters_[(std::size_t)c];
    if (w.empty()) { ++chan_pending_[(std::size_t)c]; return; }  // mailbox (D2)
    const int id = w.front(); w.pop_front();
    T(id).wait_chan = -1;
    on_unblock(id);
  }

  void deliver(int target) {                    // WAKE instruction — task-addressed
    Task& t = T(target);
    if (t.st == State::Done) return;
    if (t.st == State::Blocked && t.wait_chan >= 0) {
      auto& w = chan_waiters_[(std::size_t)t.wait_chan];
      w.erase(std::remove(w.begin(), w.end(), target), w.end());
      t.wait_chan = -1;
      on_unblock(target);                       // recursion — a brigade unwinds here
    } else ++t.mailbox;
  }

  void on_unblock(int id) {                     // shared by external wake and SLEEP/TIMER expiry
    if (T(id).st != State::Blocked) return;     // D2: with no waiter the letter is dropped
    const char* c = cause_of(T(id));
    ++T(id).pc;                                 // the blocking instruction is over
    step(id);
    if (T(id).st == State::Ready) { enqueue(id, c); maybe_preempt(id); } else settled(id);
  }

  void on_lane(const Event& e) {
    if (e.task != running_) return;
    if (check_gen_ && e.gen != T(e.task).gen) return;   // voided reservation
    const int id = e.task;
    release();
    if (T(id).run_left == 0) advance(id);              // RUN demand satisfied
    else { ev("run_end", id, "reason", "preempt"); yield_lane(id, Yield::SliceEnd); }
  }

  void arm_lane(int id) {
    const i64 h = pol_->horizon(id);
    const i64 dt = h == kNoHorizon ? T(id).run_left : std::min(T(id).run_left, h);
    push(now_ + dt, Kind::Lane, id, T(id).gen);
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
    pol_->on_yield(id, Yield::Ended);   // off the ready set too, wherever it sat
  }

  void settled(int id) {  // step() did not settle on Ready
    if (T(id).st == State::Done) { ev("task_end", id, "reason", "exit"); on_task_end(id); }
    else note("x_block", id);
  }
};

// ── loader ──────────────────────────────────────────────────────────────────
using IdMap = std::map<std::string, int>;

static void compile_prog(const Json& a, Sim& s, const IdMap& ids, std::vector<Instr>& out) {
  for (const Json& in : a.arr) {
    const std::string& op = in.at("op").as_str("op");
    if      (op == "RUN")   out.push_back({Op::RUN,   in.at("us").as_int("RUN.us")});
    else if (op == "SLEEP") out.push_back({Op::SLEEP, in.at("us").as_int("SLEEP.us")});
    else if (op == "EXIT")  out.push_back({Op::EXIT});
    else if (op == "FORK")  out.push_back({Op::FORK});
    else if (op == "TIMER") {
      Instr i{Op::TIMER};
      i.period_us = in.at("period_us").as_int("period_us");
      if (i.period_us <= 0) die("TIMER.period_us must be > 0");
      out.push_back(i);
    }
    else if (op == "WAIT")  { Instr i{Op::WAIT}; i.chan = s.channel(in.at("channel").as_str("ch"));
                              out.push_back(i); }
    else if (op == "WAKE")  { const std::string& tg = in.at("target").as_str("target");
                              auto it = ids.find(tg);
                              if (it == ids.end()) die("WAKE target is not a top-level task: " + tg);
                              Instr i{Op::WAKE}; i.target = it->second; out.push_back(i); }
    else if (op == "LOOP")  {
      const std::size_t b = out.size();
      Instr bi{Op::LOOP_BEGIN};
      const Json& c = in.at("count");
      if (c.k == Json::K::Str) { if (c.s != "unbounded") die("LOOP.count: " + c.s); bi.count = -1; }
      else bi.count = c.as_int("LOOP.count");
      out.push_back(bi);
      compile_prog(in.at("body"), s, ids, out);
      Instr e{Op::LOOP_END}; e.jump = (int)(b + 1); out.push_back(e);
      out[b].jump = (int)out.size();
    } else die("unknown op: " + op);
  }
}

static void load_workload(const std::string& path, Sim& s) {
  const Json j = load_json(path);
  s.set_meta(j.at("meta").at("id").as_str("meta.id"), "fixed");
  // j also carries ground_truth, but this function never names it: nothing that reaches the
  // core holds it, so no scheduler code can branch on it (guide §2.5)
  const Json& evs = j.at("events");

  IdMap ids;                                    // pass 1 — fix the indices first
  for (const Json& e : evs.arr) {
    if (e.at("op").as_str("op") != "arrive") continue;
    const std::string& sid = e.at("id").as_str("id");
    const i64 dep = e.has("depart") ? e.at("depart").as_int("depart") : -1;
    ids[sid] = s.add(sid, e.at("t").as_int("t"), {}, dep);
  }
  for (const Json& e : evs.arr) {               // pass 2 — programs and wakes
    const std::string& op = e.at("op").as_str("op");
    if (op == "arrive") {
      const int id = ids.at(e.at("id").as_str("id"));
      std::vector<Instr> prog;
      compile_prog(e.at("program"), s, ids, prog);
      s.set_prog(id, std::move(prog));
      if (e.has("spawn_table")) {
        std::vector<ChildSpec> tab;
        for (const Json& c : e.at("spawn_table").arr) {
          std::vector<Instr> cp;
          compile_prog(c.at("program"), s, ids, cp);
          tab.push_back(ChildSpec{c.at("name").as_str("name"), std::move(cp)});
        }
        s.set_spawn(id, std::move(tab), (int)e.at("fork_cap").as_int("fork_cap"));
      }
    } else if (op == "wake") {
      s.wake(e.at("t").as_int("t"), s.channel(e.at("channel").as_str("channel")));
    } else die("unknown event op: " + op);
  }
}

static void load_schedule(const std::string& path, Sim& s) {
  const Json j = load_json(path);
  s.set_meta(j.at("workload_id").as_str("workload_id"), j.at("condition").as_str("condition"));
  std::vector<ConfigEntry> out;
  for (const Json& e : j.at("schedule").arr) {
    const Json& c = e.at("config");
    ConfigEntry ce;
    ce.t_us = e.at("t_us").as_int("t_us");
    ce.algorithm = c.at("algorithm").as_str("algorithm");
    ce.provenance = e.at("provenance").as_str("provenance");
    const Json& pp = c.at("params");
    if (ce.algorithm == "MLFQ") {            // params: exactly the fields declared per algorithm
      if (pp.obj.size() != 4) die("MLFQ params must have 4 fields");
      ce.params.num_queues        = (int)pp.at("num_queues").as_int("num_queues");
      ce.params.timeslice_us      = pp.at("timeslice_us").as_int("timeslice_us");
      ce.params.timeslice_growth  = (int)pp.at("timeslice_growth").as_int("timeslice_growth");
      ce.params.boost_interval_us = pp.at("boost_interval_us").as_int("boost_interval_us");
    } else if (ce.algorithm == "FIFO") {
      if (!pp.obj.empty()) die("FIFO params must be empty");
    }  // EDF/LOTTERY are not in register_policy, so they are rejected at apply time
    out.push_back(std::move(ce));
  }
  s.set_schedule(std::move(out));
}

int main(int argc, char** argv) {
  Sim sim;
  Fifo fifo;
  Mlfq mlfq(sim, sim);
  sim.attach(mlfq);
  sim.register_policy("MLFQ", mlfq);
  sim.register_policy("FIFO", fifo);
  if (argc < 2) die("usage: ./sim <workload.json> [<config-schedule.json>]");
  load_workload(argv[1], sim);
  if (argc > 2) load_schedule(argv[2], sim);
  Params p;                     // the boot default when there is no schedule (OSTEP §8 whole)
  sim.run(p);
  sim.report();
}
