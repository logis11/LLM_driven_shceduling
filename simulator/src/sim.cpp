// A one-lane discrete-event scheduler simulator.
//
// The core (`Sim`) owns the clock, the event queue, the task programs and the trace.
// The scheduling policy sits behind `Policy` — the "scheduler seat" of
// docs/simulator/simulator-guide.md §5: the core consults it only at decision points,
// it sees nothing but scheduling-relevant task state, and adding a policy must not
// require touching the core. `Fifo` was the first test of that claim; `Edf` and `Lottery`
// (stage S) are the second — the core gained a read-only view of task classes, nothing else.
//
// Built up in stages (see notes/ for the one-rung-at-a-time ladder). What each stage adds:
//   A clock+queue · B Instr/Task/step · C lane+dispatch · D WAIT+wake · E depart
//   F timeslice+preemption+gen · G Policy extracted · H Trace/Clock seam + MLFQ rules 1–4
//   I MLFQ rule 5 (boost) via Clock::arm · J SLEEP · K TIMER+backlog · L LOOP flattening
//   M channels + WAKE + mailbox · N FORK/spawn_table · O JSONL trace (data-contracts §9)
//   P deadline events · Q workload loader (mini_json) · R config schedule + handoff
//   S EDF + LOTTERY via a TaskView seam (executor-owned task classes)
//   T children traced under their spawn_table id · U config-switch semantics (cold/same/drain)
//   V batch_bandwidth_cap enforced (token bucket, D10) · W spawn-table WAKE targets
//   X a ready line per completed primitive, RUN→RUN in one occupancy, a lone slice expiry kept
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
//   · task classes (S): EDF needs deadlines and LOTTERY needs the batch class, but the class
//     is executor state, identical under every algorithm (batch-class memo 2026-09-09 §3) —
//     so the core exposes it through a third narrow seam, TaskView, and no policy sees Sim.
//     B2 periodic class: a task with a TIMER, plus everything reachable from it through WAKE
//     targets (fixed at load). A chain stage has no TIMER of its own, so it inherits the
//     deadline of whoever woke it — the WAKE carries the frame's deadline down the chain.
//     B1 batch class: non-periodic and has received >= one slice of CPU since its last
//     voluntary block (WAIT that blocks, SLEEP, TIMER not yet due); preemption never resets it.
//   · determinism (S): batch_share is the only real number in the schema; the loader turns it
//     into integer basis points, so the run itself does no floating-point math. The lottery
//     PRNG (splitmix64) is seeded once per run from the FNV-1a hash of the workload id
//     (interpretation-contract §1: "a PRNG the simulator seeds deterministically per run").
//   · cold start (S): Policy::start is told whether the algorithm changed. Only then is the
//     lane holder treated as freshly dispatched (switch memo 2026-09-08 §2, rule a).
//   · config-switch semantics (U; switch memo §2–§7, metrics §11.7–9):
//     U1 a switch into MLFQ is a cold start — every task back to Q0 with no allotment.
//     U2 a same-algorithm entry is not a switch: the holder is neither released nor re-armed
//        (its pending Lane event is the slice it was granted), queue order is kept, MLFQ
//        levels clamp to a smaller num_queues, and a task whose allotment now exceeds the
//        shrunken slice is demoted when next picked (otherwise its horizon would be negative).
//     U3 drain: a switch out of MLFQ/EDF/LOTTERY applies the next time the lane is free
//        (slice end, block, preemption, exit, depart); out of FIFO it applies at once.
//        Entries arriving meanwhile queue behind it, so every index applies, in order.
//   · child ids (T): a spawned child is traced under its spawn_table `id`, the id the run
//     file and the harness know it by.
//   · spawn-table WAKE targets (W; dataset audit 2026-10-10 blocker 1, 9.6 D19/9.10 D53):
//     a make job is six (or, for the module build's trees, eight or ten) member processes
//     that wake *each other* by spawn-table id. Such a target has no task index until the
//     parent forks it, so the loader resolves it to a negative target (-slot-1) and the
//     birth fills the slot. A wake that beats the birth is held and handed over at the
//     birth, not dropped: fork_cap is a multiple of six, so an eight- or ten-member job is
//     split by the cap and the root can wake a member not yet forked (c7-compile). Dropping
//     it would block that member forever and deadlock the job.
//   · one occupancy (X; conformance (a), metrics §11 item 1, trace-clarifications memo §4; Q2
//     decided 2026-10-16): RUNs joined without a block are one occupancy — one run_start, one
//     run_end. A RUN boundary is not a decision point: boundary() steps the holder on its lane,
//     with no requeue and no pick, and writes x_run_cont. Every blocking primitive that
//     completes writes its ready line at that instant, a WAIT met from a mailbox and a TIMER in
//     backlog included — inside the occupancy when the holder passes it, at the arrival when the
//     arrival step does. A slice that expires while the policy picks the same holder again is
//     no switch either: no run_end/run_start pair. A FORK that finds a slot writes no line — the
//     fork-slot wait is the block, and there was none. Whatever ends a RUN at the very µs of
//     another decision (a preemption, a cap park, a config apply, a policy timer) leaves the
//     boundary to the RUN's own Lane event, so the boundary is settled in one place.
//     Fixed beside it: a segment-bound task that EXITs before its depart wrote a second
//     task_end at the depart, and the harness read the later one — a completed task as not.
//   · policy-timer epoch (S, fixes R): a policy timer used to survive a config apply, so each
//     MLFQ start() added one more boost chain, and the chains kept each other alive past the
//     arm() stop rule — c1-compile under the mock-switch schedule never terminated. The switch
//     memo says the boost timer restarts at t_apply; like F's gen, a PolicyTimer now carries
//     the config epoch it was armed under and is dropped on mismatch.

#include "mini_json.hpp"
#include <algorithm>
#include <cassert>
#include <cmath>
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
struct ChildSpec { std::string sid, name; std::vector<Instr> prog; bool periodic = false;
                   int slot = -1; };   // W: this entry's deferred-WAKE slot (-1 = never a target)

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
  bool periodic = false;      // B2 class — fixed at load, never changes during the run
  i64 burst = 0;              // B1 — CPU received since the last voluntary block
  i64 chain_dl = -1;          // deadline inherited by a TIMER-less chain stage (-1 = none)
  std::deque<i64> mail_dl;    // the deadline each mailboxed WAKE carried (pairs with mailbox)
};

constexpr i64 kNoHorizon = -1;  // the policy sets no preemption horizon

// The union of the frozen schema's params (recognition-vocabulary §2); the defaults are the
// boot default. timeslice_us is shared by MLFQ (top-queue slice) and LOTTERY (one draw's
// tenure). Parameters are configuration, never constants in code
struct Params {
  int num_queues        = 3;        // MLFQ
  i64 timeslice_us      = 10000;    // MLFQ, LOTTERY
  int timeslice_growth  = 2;        // MLFQ
  i64 boost_interval_us = 100000;   // MLFQ
  i64 residual_timeslice_us = 10000;  // EDF — round-robin slice of the residual class
  int batch_share_bp    = 1500;     // LOTTERY — batch_share 0.15 as an integer in 1/10000
};
constexpr int kShareDen = 10000;    // denominator of batch_share_bp

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

// The executor-owned task classes, as much as a policy may read (no names, no ground truth)
struct TaskView {
  virtual ~TaskView() = default;
  virtual i64  deadline(int id) const = 0;   // the current job's deadline, -1 = none
  virtual bool batch(int id) const = 0;      // B1 and not B2
};

// Why a task left the lane. The first two leave it runnable; the last two take it off
enum class Yield { SliceEnd, Preempted, Blocked, Ended };

struct Policy {
  virtual ~Policy() = default;
  // cold = we took over from a different algorithm; false for a same-algorithm params change
  virtual void start(const Params&, bool cold) = 0;
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
  void start(const Params&, bool) override {}
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
  void start(const Params& np, bool cold) override {
    p = np;
    ready.assign((std::size_t)p.num_queues, {});
    if (cold) for (St& s : st) s = St{};                                   // U1: all to Q0
    else for (St& s : st) s.level = std::min(s.level, p.num_queues - 1);   // U2: levels kept
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
    for (std::size_t lv = 0; lv < ready.size(); ++lv) {
      auto& q = ready[lv];
      while (!q.empty()) {
        const int id = q.front(); q.pop_front();
        St& s = slot(id);
        if (s.allot <= slice_of(s.level)) return id;
        // U2: a same-algorithm entry shrank the slice below this allotment → rule 3 now
        s.allot = 0;
        if (s.level + 1 >= p.num_queues) return id;   // bottom: a fresh slice, as is
        ++s.level;
        ready[(std::size_t)s.level].push_back(id);
        trace.note("x_mlfq_demote", id);
      }
    }
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

// Per-task lane-time ledger — EDF's residual slice, LOTTERY's per-draw tenure
struct Ledger {
  std::vector<i64> v;
  i64& operator[](int id) {
    if (v.size() <= (std::size_t)id) v.resize((std::size_t)id + 1, 0);
    return v[(std::size_t)id];
  }
  void clear() { std::fill(v.begin(), v.end(), 0); }
};

// EDF (vocab §2): tasks with a deadline run earliest-deadline-first; ties go to the lower id
// (the fixed executor rule). The deadline class has no slice — Liu & Layland's EDF is
// preemptive without a quantum. A task with no deadline is in the residual class and
// round-robins in the remaining lane time. No admission control (v1).
// The class is judged at pick time through TaskView, because a ready task can gain a
// deadline while it waits (the mailbox path)
struct Edf : Policy {
  TaskView& view;
  i64 slice = 10000;
  std::deque<int> q;                        // the ready set in ready order (= residual RR order)
  Ledger used;                              // residual: lane time used of the current slice

  explicit Edf(TaskView& v) : view(v) {}
  void start(const Params& p, bool cold) override {
    slice = p.residual_timeslice_us;
    if (cold) used.clear();                 // rule (a): the holder starts a fresh slice too
  }
  void on_ready(int id) override { q.push_back(id); }
  void on_yield(int id, Yield why) override {
    if (why == Yield::SliceEnd || why == Yield::Preempted) {
      // a preemption keeps the rest of the slice — except one landing in the same µs as the
      // slice boundary, which is a slice end; otherwise the next dispatch has horizon 0 and
      // traces a zero-length occupancy
      if (why == Yield::SliceEnd || used[id] >= slice) used[id] = 0;
      q.push_back(id);
      return;
    }
    used[id] = 0;
    q.erase(std::remove(q.begin(), q.end(), id), q.end());
  }
  int pick() override {
    if (q.empty()) return -1;
    auto best = q.end(); i64 bd = 0;
    for (auto it = q.begin(); it != q.end(); ++it) {
      const i64 d = view.deadline(*it);
      if (d < 0) continue;
      if (best == q.end() || d < bd || (d == bd && *it < *best)) { best = it; bd = d; }
    }
    if (best == q.end()) best = q.begin();  // no deadline work → residual round-robin
    const int id = *best; q.erase(best); return id;
  }
  i64  horizon(int id) override {          // 0 if a same-algorithm entry shrank the slice
    return view.deadline(id) >= 0 ? kNoHorizon : std::max<i64>(0, slice - used[id]);
  }
  void charge(int id, i64 ran) override { if (view.deadline(id) < 0) used[id] += ran; }
  bool preempts(int c, int h) override {
    const i64 dc = view.deadline(c), dh = view.deadline(h);
    return dc >= 0 && (dh < 0 || dc < dh);  // a tie does not preempt
  }
  std::vector<int> handoff() override {
    std::vector<int> o(q.begin(), q.end()); q.clear(); return o;
  }
};

// LOTTERY (vocab §2, waldspurger-osdi94): tickets split batch : non-batch = share : (1−share),
// equal tickets per task within a class. That is the same distribution as a two-stage draw:
// ① if both classes are runnable, pick the class by share; ② pick uniformly inside it.
// Only runnable tasks hold tickets. One draw's tenure is timeslice_us. A wake never
// preempts — the next draw is LOTTERY's only preemption. The draw is integer-only, and
// rejection sampling removes the modulo bias
struct Lottery : Policy {
  TaskView& view;
  i64 slice = 10000;
  int share_bp = 1500;
  std::vector<int> pool;                    // the ready set in ready order
  Ledger used;                              // lane time used of the current draw's tenure
  std::uint64_t rng = 0;                    // splitmix64 state — seed() once per run

  explicit Lottery(TaskView& v) : view(v) {}
  void seed(std::uint64_t s) { rng = s; }
  std::uint64_t next() {
    std::uint64_t z = (rng += 0x9E3779B97F4A7C15ull);
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ull;
    z = (z ^ (z >> 27)) * 0x94D049BB133111EBull;
    return z ^ (z >> 31);
  }
  std::uint64_t below(std::uint64_t n) {    // uniform in [0, n)
    const std::uint64_t lim = UINT64_MAX - UINT64_MAX % n;
    for (;;) { const std::uint64_t r = next(); if (r < lim) return r % n; }
  }
  void start(const Params& p, bool cold) override {
    slice = p.timeslice_us; share_bp = p.batch_share_bp;
    if (cold) used.clear();
  }
  void on_ready(int id) override { pool.push_back(id); }
  void on_yield(int id, Yield why) override {
    if (why == Yield::SliceEnd || why == Yield::Preempted) pool.push_back(id);
    else pool.erase(std::remove(pool.begin(), pool.end(), id), pool.end());
  }
  int pick() override {
    if (pool.empty()) return -1;
    std::vector<std::size_t> b, n;          // positions in pool, per class
    for (std::size_t k = 0; k < pool.size(); ++k) (view.batch(pool[k]) ? b : n).push_back(k);
    const std::vector<std::size_t>* cls = b.empty() ? &n : &b;
    if (!b.empty() && !n.empty())
      cls = below(kShareDen) < (std::uint64_t)share_bp ? &b : &n;
    const std::size_t k = (*cls)[cls->size() == 1 ? 0 : below(cls->size())];
    const int id = pool[k];
    pool.erase(pool.begin() + (std::ptrdiff_t)k);
    used[id] = 0;                           // a new draw is a new tenure
    return id;
  }
  i64  horizon(int id) override { return std::max<i64>(0, slice - used[id]); }
  void charge(int id, i64 ran) override { used[id] += ran; }
  bool preempts(int, int) override { return false; }
  std::vector<int> handoff() override { std::vector<int> o = pool; pool.clear(); return o; }
};

// One line of a config schedule. The loader fills it; the core consumes it via ConfigApply
// cap_bp: batch_bandwidth_cap as an integer in 1/10000. -1 = null (no ceiling) — no float at run time
struct ConfigEntry { i64 t_us; std::string algorithm; Params params; std::string provenance;
                     int cap_bp = -1; };

enum class Kind { Arrive, Lane, Wake, Unblock, Depart, PolicyTimer, ConfigApply, CapRefill };
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

class Sim : public Trace, public Clock, public TaskView {
 public:
  // ── Trace / Clock / TaskView seams ──
  i64 now() const override { return now_; }
  i64 deadline(int id) const override {     // the task's own TIMER job first, else the inherited one
    const Task& t = tasks_[(std::size_t)id];
    if (!t.periodic) return -1;
    return t.job_open ? t.job_tick + t.job_period : t.chain_dl;
  }
  bool batch(int id) const override {
    const Task& t = tasks_[(std::size_t)id];
    if (t.periodic) return false;
    // burst grows only at release(). B1 says a task enters the class "the moment it has
    // consumed one full time slice", so the unsettled part of the current occupancy counts:
    // without it a task that never gives up the lane (FIFO) is never seen as batch. At pick
    // time running_ is -1, so what the policies read does not change (V).
    const i64 b = t.burst + (id == running_ ? now_ - lane_start_ : 0);
    return b >= batch_slice_;
  }
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

  // V's diagnostic. The harness ignores x_ lines (its event set is closed, data-contracts §9).
  // It is the only trace of the cap biting: a park leaves no other mark but run_end(preempt)
  void ev_cap(int id, bool parked) {
    std::printf("{\"event\":\"x_cap_park\",\"t\":%lld,\"task\":\"%s\",\"in\":%s,"
                "\"allow_us\":%lld}\n", (long long)now_, tasks_[(std::size_t)id].sid.c_str(),
                parked ? "true" : "false", (long long)allow_);
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
      if (tk.st != State::Done) { q_.push({t, seq_++, Kind::PolicyTimer, -1, pol_epoch_, tag}); return; }
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
  // W: one slot per spawn-table entry that a WAKE can name. The index is unknown until the
  // parent forks it, so the slot carries the birth and holds wakes that arrive before it
  int spawn_slot(const std::string& sid) {
    spawn_sid_.push_back(sid);
    spawn_live_.push_back(-1);
    return (int)spawn_sid_.size() - 1;
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
  const std::string& workload_id() const { return wid_; }

  // B2 (batch-class memo §3): every task with a TIMER, and everything reachable from one
  // through WAKE targets. Run once after loading. A spawn-table child is periodic if its own
  // program has a TIMER, and then its WAKE targets seed the closure too
  void classify_periodic() {
    auto has = [](const std::vector<Instr>& p, Op op) {
      return std::any_of(p.begin(), p.end(), [op](const Instr& i) { return i.op == op; });
    };
    std::vector<int> work;
    auto mark = [&](int id) { if (!T(id).periodic) { T(id).periodic = true; work.push_back(id); } };
    auto seed_targets = [&](const std::vector<Instr>& p) {
      // W: a negative target names a spawn-table entry, not a task index. No spawned child in
      // the dataset carries a TIMER (compiler-child and module-compiler-child are RUN/WAIT/
      // WAKE/EXIT only), so the B2 closure never has to cross into the spawn table. If one
      // ever does, this is the seat: the closure would have to mark ChildSpec::periodic.
      for (const Instr& i : p) if (i.op == Op::WAKE && i.target >= 0) mark(i.target);
    };
    for (std::size_t k = 0; k < tasks_.size(); ++k) {
      if (has(tasks_[k].prog, Op::TIMER)) mark((int)k);
      for (ChildSpec& c : tasks_[k].spawn_table)
        if ((c.periodic = has(c.prog, Op::TIMER))) seed_targets(c.prog);
    }
    while (!work.empty()) { const int id = work.back(); work.pop_back(); seed_targets(T(id).prog); }
  }

  explicit Sim(bool check_gen = true) : check_gen_(check_gen) {}
  void attach(Policy& p) { pol_ = &p; }

  void run(const Params& p) {
    std::printf("{\"event\":\"meta\",\"workload_id\":\"%s\",\"condition\":\"%s\","
                "\"sim\":\"src/sim\",\"schedule_entries\":%zu}\n", wid_.c_str(), cond_.c_str(),
                schedule_.size());
    if (schedule_.empty()) { pol_->start(p, true); batch_slice_ = p.timeslice_us; }  // no schedule → argument params
    while (!q_.empty()) {
      const Event e = q_.top();
      q_.pop();
      assert(e.t >= now_);
      now_ = e.t;
      settle_cap();            // V: settle the accrual over [cap_mark_, now_] first
      switch (e.kind) {
        case Kind::Arrive:      on_arrive(e.task);      break;
        case Kind::Lane:        on_lane(e);             break;
        case Kind::Wake:        on_ext_wake(e.tag);     break;
        case Kind::Unblock:     on_unblock(e.task);     break;
        case Kind::Depart:      on_depart(e.task);      break;
        case Kind::PolicyTimer: on_policy_timer(e);     break;
        case Kind::ConfigApply: on_config_apply(e.tag); break;
        case Kind::CapRefill:   break;   // V: waking up is the work — cap_gate below judges
      }
      cap_gate();              // V: park/admit is judged even while the lane is held
      dispatch();
      capped_ = capped_now();  // V: the verdict for the next interval; no time passed here
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
  std::string algo_;                        // the algorithm in force — decides `cold`
  std::uint64_t pol_epoch_ = 0;             // +1 per config apply; carried in PolicyTimer's gen
  i64 batch_slice_ = Params{}.timeslice_us; // B1's threshold = the running config's slice
  int running_ = -1;
  int lane_prev_ = -1;                      // X/Q2: the holder whose slice just ended, until dispatch
  i64 lane_start_ = 0, now_ = 0;
  bool check_gen_ = true;

  // ── V: batch_bandwidth_cap ────────────────────────────────────────────────
  int cap_bp_ = -1;              // the running config's cap, 1/10000. -1 = null → path off
  i64 allow_ = 0;                // token bucket, µs. Negative = debt from a stretch that
                                 // opened mid-occupancy
  i64 accrue_rem_ = 0;           // remainder of the integer accrual — keeps it drift-free
  i64 cap_mark_ = 0;             // the accrual is settled up to here
  bool capped_ = false;          // was [cap_mark_, now_] capped (what accrual and spend read)
  std::vector<int> runnable_;    // Ready+Running — the population "is a non-batch task runnable"
  std::vector<int> parked_;      // batch tasks held out of the policy's ready set, in park order
  std::uint64_t cap_epoch_ = 0;  // generation of the CapRefill reservation
  i64 cap_timer_at_ = -1;        // the cap timer now armed (so it is not armed twice)

  static bool is_run_state(State s) { return s == State::Ready || s == State::Running; }

  // The single funnel for every state transition; runnable_ is maintained here alone. Batch
  // membership changes with burst, without a transition, so the set is kept and the question
  // is asked of batch() each time
  void set_st(int id, State s) {
    Task& t = T(id);
    const bool was = is_run_state(t.st), now = is_run_state(s);
    t.st = s;
    if (was == now) return;
    if (now) runnable_.push_back(id);
    else {
      runnable_.erase(std::remove(runnable_.begin(), runnable_.end(), id), runnable_.end());
      parked_.erase(std::remove(parked_.begin(), parked_.end(), id), parked_.end());
    }
  }

  bool capped_now() const {      // is any non-batch task runnable (batch-class memo §3)
    for (int id : runnable_) if (!batch(id)) return true;
    return false;
  }

  // Accrual and spending in one place. Over [cap_mark_, now_] neither the runnable set nor the
  // holder changes — both move only at decision points, and every decision point passes here —
  // so the interval is homogeneous
  void settle_cap() {
    const i64 dt = now_ - cap_mark_;
    cap_mark_ = now_;
    if (cap_bp_ < 0 || dt <= 0 || !capped_) return;
    const i64 num = dt * cap_bp_ + accrue_rem_;
    allow_ += num / kShareDen;
    accrue_rem_ = num % kShareDen;
    if (allow_ > batch_slice_) { allow_ = batch_slice_; accrue_rem_ = 0; }   // bucket depth
    // Spend only what this interval delivered to a task while it was in the batch class. The
    // interval is split at the B1 threshold for an occupancy that crosses it (FIFO, where
    // nothing preempts). burst grows only at release(), so count the effective burst here
    if (running_ >= 0 && !T(running_).periodic) {
      const i64 b0 = T(running_).burst + (cap_mark_ - dt - lane_start_);
      const i64 in_class = (b0 + dt) - std::max(b0, batch_slice_);
      if (in_class > 0) allow_ -= in_class;
    }
  }

  // Empty bucket → hold every runnable batch task out of the policy's ready set; full bucket or
  // no ceiling → give them back. Called at every decision point, so pick() never sees a task it
  // may not run and the verdict is never late. Idempotent
  void cap_gate() {
    if (cap_bp_ < 0) { unpark_all(); return; }
    if (!capped_now() || allow_ >= batch_slice_) { unpark_all(); arm_cap_timer(); return; }
    if (allow_ > 0) { arm_cap_timer(); return; }   // still in credit — nothing to park
    // The bucket is empty. A batch holder comes off the lane first: when the stretch opened
    // mid-occupancy its horizon was set with no ceiling, and the debt would keep growing
    if (running_ >= 0 && batch(running_) && !run_ends_now()) {   // X: else its boundary first
      const int v = running_;
      release();
      ev("run_end", v, "reason", "preempt");
      set_st(v, State::Ready); park(v);
    }
    for (std::size_t k = 0; k < runnable_.size(); ++k) {
      const int id = runnable_[k];
      if (id != running_ && batch(id) && !is_parked(id)) park(id);
    }
    arm_cap_timer();
  }

  bool is_parked(int id) const {
    return std::find(parked_.begin(), parked_.end(), id) != parked_.end();
  }
  void park(int id) {
    pol_->on_yield(id, Yield::Blocked);   // "remove from the ready set" in all four policies
    parked_.push_back(id);
    ev_cap(id, true);
  }
  void unpark_all() {
    if (parked_.empty()) return;
    const std::vector<int> back = parked_;         // park order — deterministic
    parked_.clear();
    cap_timer_at_ = -1;
    for (int id : back) { pol_->on_ready(id); ev_cap(id, false); }
    for (int id : back) maybe_preempt(id);         // the policy may take the lane back
  }

  // The cap judges at decision points, and a decision point may never come — under FIFO a
  // holder's horizon can be a whole second with no event in between. So the cap arms its own
  // timer. Two cases: ① parked → when the bucket is full again (without it the admit is late
  // and the class is served below its ceiling); ② a holder spending → when it empties.
  // ②'s rate: inside a capped stretch accrual f runs beside the spend 1, so the net is (1−f)
  void arm_cap_timer() {
    if (cap_bp_ <= 0) return;
    i64 at = -1;
    if (!parked_.empty()) {
      const i64 need = batch_slice_ - allow_;
      if (need > 0) at = now_ + (need * kShareDen + cap_bp_ - 1) / cap_bp_;      // ceil
    }
    if (running_ >= 0 && cap_bp_ < kShareDen && capped_now()) {
      const i64 d = drain_in(running_);            // when the holder reaches the ceiling
      if (d >= 0 && (at < 0 || now_ + d < at)) at = now_ + d;
    }
    if (at < 0 || at == cap_timer_at_) return;     // none, or already armed for that instant
    cap_timer_at_ = at;
    push(at, Kind::CapRefill, -1, ++cap_epoch_);   // the epoch voids every earlier reservation
  }

  // How long until the bucket empties if id keeps running as it is. -1 for a periodic task
  i64 drain_in(int id) const {
    if (T2(id).periodic) return -1;
    const i64 b = T2(id).burst + (now_ - lane_start_);
    const i64 to_class = std::max<i64>(0, batch_slice_ - b);   // free until the B1 threshold
    i64 a = allow_ + to_class * cap_bp_ / kShareDen;           // which still accrues meanwhile
    if (a > batch_slice_) a = batch_slice_;
    if (a < 0) a = 0;   // in debt: it is over the moment it crosses. Dividing a negative here
                        // yields a nonsense horizon — the defect that looped sim_v on c2-p3b
    return to_class + (a * kShareDen + (kShareDen - cap_bp_) - 1) / (kShareDen - cap_bp_);
  }
  const Task& T2(int id) const { return tasks_[static_cast<std::size_t>(id)]; }
  std::map<std::string, int> chan_id_;
  std::vector<std::deque<int>> chan_waiters_;
  std::vector<int> chan_pending_;               // channel mailboxes
  std::vector<std::string> spawn_sid_;          // W: slot → the file's id (diagnostics only)
  std::vector<int> spawn_live_;                 // W: slot → task index, -1 before the birth
  std::map<int, std::deque<i64>> spawn_mail_;   // W: slot → deadlines of wakes before the birth
                                                // (sparse — most slots never take an early one)

  void push(i64 t, Kind k, int task, std::uint64_t gen = 0) { q_.push({t, seq_++, k, task, gen, 0}); }
  Task& T(int id) { return tasks_[static_cast<std::size_t>(id)]; }

  std::deque<int> pending_;                  // U3: entries waiting for the drain, in arrival order

  void on_config_apply(int idx) {
    const ConfigEntry& c = schedule_[(std::size_t)idx];
    if (registry_.find(c.algorithm) == registry_.end()) die("unregistered algorithm: " + c.algorithm);
    const bool drains = running_ >= 0 && c.algorithm != algo_ && algo_ != "FIFO";
    if (!pending_.empty() || drains) {        // U3: dispatch() applies it once the lane is free
      pending_.push_back(idx);
      std::printf("{\"event\":\"x_config_pending\",\"t\":%lld,\"index\":%d}\n", (long long)now_, idx);
      return;
    }
    apply_config(idx);
  }

  void apply_config(int idx) {
    const ConfigEntry& c = schedule_[(std::size_t)idx];
    Policy* next = registry_.at(c.algorithm);
    std::printf("{\"event\":\"config_applied\",\"t\":%lld,\"index\":%d,"
                "\"algorithm\":\"%s\",\"provenance\":\"%s\"}\n",
                (long long)now_, idx, c.algorithm.c_str(), c.provenance.c_str());

    const bool cold = c.algorithm != algo_;
    const int holder = running_;              // a holder here means out of FIFO, or same algorithm
    if (holder >= 0 && cold) release();       // rule a: freshly dispatched by the new algorithm. A
                                              // RUN ending now is re-armed at 0 µs below (X)
    std::vector<int> waiting = pol_->handoff();
    if (cold) std::sort(waiting.begin(), waiting.end());   // D5; U2 keeps the queue order
    ++pol_epoch_;                                // voids every policy timer armed so far
    algo_ = c.algorithm;
    // B1's slice (batch-class memo §3). FIFO has no slice, so it uses the boot default's
    batch_slice_ = c.algorithm == "EDF"  ? c.params.residual_timeslice_us
                 : c.algorithm == "FIFO" ? Params{}.timeslice_us : c.params.timeslice_us;
    // V: the cap and the bucket depth move together. A parked task is not in handoff, so it
    // stays parked and the next cap_gate judges it under the new config
    cap_bp_ = c.cap_bp;
    if (allow_ > batch_slice_) { allow_ = batch_slice_; accrue_rem_ = 0; }
    pol_ = next;
    pol_->start(c.params, cold);
    for (int id : waiting) pol_->on_ready(id);
    if (holder >= 0 && cold) { running_ = holder; set_st(holder, State::Running);
                               lane_start_ = now_; arm_lane(holder); }
    // U2: same algorithm — the holder is untouched; its pending Lane event (same gen) is
    // the slice it was granted
  }

  void on_policy_timer(const Event& e) {
    if (e.gen != pol_epoch_) return;   // armed under an earlier config — void (header, stage S)
    const int holder = running_;
    if (holder >= 0) release();
    pol_->on_timer(e.tag);
    if (holder < 0) return;
    if (T(holder).run_left > 0 && pol_->horizon(holder) == 0) slice_over(holder);
    else { running_ = holder; set_st(holder, State::Running);           // no switch → nothing traced;
           lane_start_ = now_; arm_lane(holder); }                       // a RUN ending now: 0 µs (X)
  }

  // Lane accounting lives here alone — this is where "demand is preserved across preemption" is
  void release() {
    T(running_).run_left -= now_ - lane_start_;
    assert(T(running_).run_left >= 0);
    pol_->charge(running_, now_ - lane_start_);
    T(running_).burst += now_ - lane_start_;   // B1 — preemption never resets it
    ++T(running_).gen;
    running_ = -1;
  }

  // X: one RUN's demand is delivered (release() settled it) and the holder steps on. Reaching
  // the next RUN without a block continues the occupancy: no run_end, no requeue, no pick
  void boundary(int id) {
    ++T(id).pc;
    step(id);
    if (T(id).st != State::Ready) {
      if (T(id).st == State::Done) ev("run_end", id, "reason", "exit");
      else ev("run_end", id, "reason", "block", "blocked_on", blocked_on(T(id)));
      settled(id); pol_->on_yield(id, T(id).st == State::Done ? Yield::Ended : Yield::Blocked);
      return;
    }
    note("x_run_cont", id);
    running_ = id; set_st(id, State::Running); lane_start_ = now_;
    // Drain: a waiting switch applies as the current RUN ends, the holder freshly dispatched by
    // the incoming algorithm (rule a), as a switch out of FIFO treats it
    while (!pending_.empty()) { const int idx = pending_.front(); pending_.pop_front(); apply_config(idx); }
    const i64 h = pol_->horizon(id);
    if (h != kNoHorizon && h <= 0) { release(); slice_over(id); return; }   // slice spent here, or
                                                                             // shrunk below it (U2)
    ++T(id).gen; arm_lane(id);   // voids a Lane a rule-a apply armed above
    // The step may have woken, spawned or re-dated someone (EDF: the holder's own next job)
    for (std::size_t k = 0; k < runnable_.size(); ++k) {
      const int c = runnable_[k];
      if (c != id && !is_parked(c) && pol_->preempts(c, id)) { maybe_preempt(c); return; }
    }
  }

  // Q2 (decided 2026-10-16): the holder's slice is over. It goes back to the ready set and
  // dispatch() writes run_end only if the policy picks someone else — after a drain waiting on
  // this slice end has applied, so the incoming algorithm is the one that picks (mock-switch
  // at 12000: the hog's slice ends, FIFO applies, the hog keeps the lane with no run_end)
  void slice_over(int id) {
    yield_lane(id, Yield::SliceEnd);
    lane_prev_ = id;
  }

  bool run_ends_now() const { return T2(running_).run_left == now_ - lane_start_; }

  void maybe_preempt(int challenger) {
    if (running_ < 0 || !pol_->preempts(challenger, running_)) return;
    if (run_ends_now()) return;   // X: the RUN's Lane event, queued at this µs, settles the
                                  // boundary first, and the boundary judges this challenger again
    const int v = running_;
    release();
    ev("run_end", v, "reason", "preempt");
    yield_lane(v, Yield::Preempted);
  }

  // Advances the program only; the ready set, the lane and the queueing are the policy's or
  // the caller's job. Exceptions: SLEEP/TIMER schedule their own timed Unblock here, and
  // WAKE delivers here — a timed or instantaneous side effect is part of executing the op
  void step(int id) {
    Task& t = T(id);
    for (int guard = 0; ; ++guard) {
      if (guard > 1000000) { std::fprintf(stderr, "step: %s does not advance\n",
                                          t.name.c_str()); std::abort(); }
      if (t.pc >= t.prog.size()) { set_st(id, State::Done); return; }
      switch (t.prog[t.pc].op) {
        case Op::RUN:  set_st(id, State::Ready); t.run_left = t.prog[t.pc].us; return;
        case Op::SLEEP: set_st(id, State::Blocked); t.blocked_by = 's'; t.burst = 0;
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
            t.timer_next += P; ++t.pc;
            ready_line(id, "timer_tick");                 // X: completed without blocking
            break;
          }
          const i64 due = t.timer_next;                   // ahead of the grid — block until next tick
          t.job_tick = due; t.job_period = P; t.job_open = true;
          t.timer_next += P;
          set_st(id, State::Blocked); t.blocked_by = 't'; t.burst = 0;   // a voluntary block
          push(due, Kind::Unblock, id);
          return;
        }
        case Op::WAIT: {
          const int c = t.prog[t.pc].chan;
          if (chan_pending_[(std::size_t)c] > 0) { --chan_pending_[(std::size_t)c];
                                                   t.chain_dl = -1; ++t.pc;
                                                   ready_line(id, "wake"); break; }   // X
          if (t.mailbox > 0) { --t.mailbox; t.chain_dl = t.mail_dl.front(); t.mail_dl.pop_front();
                               ++t.pc; ready_line(id, "wake"); break; }            // X
          set_st(id, State::Blocked); t.blocked_by = 'w'; t.wait_chan = c; t.burst = 0;
          chan_waiters_[(std::size_t)c].push_back(id);
          return;
        }
        case Op::WAKE: deliver(id, t.prog[t.pc].target); ++t.pc; break;
        case Op::FORK:
          if (t.spawn_next >= t.spawn_table.size()) { ++t.pc; break; }   // table exhausted
          if (t.fork_cap > 0 && t.live_children >= t.fork_cap) {
            set_st(id, State::Blocked); t.blocked_by = 'f'; t.wait_chan = -1;  // wait for a slot
            return;                                                       // pc stays put
          }
          spawn(id); ++t.pc; break;
        case Op::EXIT: set_st(id, State::Done); return;
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

  // X: the ready line of a primitive that completed without blocking. During a task's arrival
  // step its lines are held, so that its ready(arrive) comes first, as the mocks write it
  std::vector<const char*>* held_ = nullptr;
  int held_id_ = -1;
  void ready_line(int id, const char* cause) {
    if (id == held_id_) held_->push_back(cause); else ev("ready", id, "cause", cause);
  }
  // The arrival step (metrics §11 items 4–5): the leading instructions run without the lane.
  // A task that reaches a RUN gets ready(arrive), then the zero-wait lines of what it passed —
  // its tick 0, a WAIT met by a wake stored before it arrived
  void arrival_step(int id) {
    std::vector<const char*> held;
    std::vector<const char*>* const outer = held_;
    const int outer_id = held_id_;          // a FORK in the step runs a child's arrival step
    held_ = &held; held_id_ = id;
    step(id);
    held_ = outer; held_id_ = outer_id;
    const bool ready = T(id).st == State::Ready;
    if (ready) ev("ready", id, "cause", "arrive");
    for (const char* c : held) ev("ready", id, "cause", c);
    if (ready) { pol_->on_ready(id); maybe_preempt(id); } else settled(id);
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
    if (why == Yield::SliceEnd || why == Yield::Preempted) set_st(id, State::Ready);
    pol_->on_yield(id, why);
  }

  void on_arrive(int id) {
    ev("task_arrive", id, "source", "file");
    arrival_step(id);
  }

  void spawn(int parent_id) {
    Task& par = T(parent_id);
    Task c;
    c.name = par.spawn_table[par.spawn_next].name;
    c.sid = par.spawn_table[par.spawn_next].sid;   // the file's id (stage T)
    c.prog = par.spawn_table[par.spawn_next].prog;
    c.periodic = par.spawn_table[par.spawn_next].periodic;
    c.parent = parent_id;
    const int slot = par.spawn_table[par.spawn_next].slot;   // W: read before the push_back
    ++par.spawn_next; ++par.live_children;
    tasks_.push_back(std::move(c));            // deque, so the par reference stays valid
    const int id = (int)tasks_.size() - 1;
    T(id).born = now_;
    if (slot >= 0) {                           // W: the slot is live from here on, and any wake
      spawn_live_[(std::size_t)slot] = id;     // that beat the birth is handed over now —
      auto it = spawn_mail_.find(slot);        // before step() reaches the first WAIT, which is
      if (it != spawn_mail_.end()) {           // where the mailbox is consumed
        T(id).mailbox = (int)it->second.size();
        T(id).mail_dl.assign(it->second.begin(), it->second.end());
        spawn_mail_.erase(it);
      }
    }
    ev("task_arrive", id, "source", "spawn", "parent", T(parent_id).sid.c_str());
    arrival_step(id);
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
    set_st(id, State::Ready);
    ev("ready", id, "cause", "fork_slot");
    step(id);
    if (T(id).st == State::Ready) { pol_->on_ready(id); maybe_preempt(id); } else settled(id);
  }

  void on_ext_wake(int c) {                     // external wake — channel-addressed
    auto& w = chan_waiters_[(std::size_t)c];
    if (w.empty()) { ++chan_pending_[(std::size_t)c]; return; }  // mailbox (D2)
    const int id = w.front(); w.pop_front();
    T(id).wait_chan = -1;
    T(id).chain_dl = -1;                        // an external wake carries no deadline
    on_unblock(id);
  }

  // WAKE instruction — task-addressed. It carries the waker's deadline, so a frame's
  // deadline follows it down the chain
  void deliver(int waker, int target) {
    if (target < 0) {                           // W: a spawn-table sibling, resolved at its birth
      const int slot = -target - 1;
      const int live = spawn_live_[(std::size_t)slot];
      if (live < 0) { spawn_mail_[slot].push_back(deadline(waker)); return; }   // held, not lost
      target = live;
    }
    Task& t = T(target);
    if (t.st == State::Done) return;
    const i64 dl = deadline(waker);
    if (t.st == State::Blocked && t.wait_chan >= 0) {
      auto& w = chan_waiters_[(std::size_t)t.wait_chan];
      w.erase(std::remove(w.begin(), w.end(), target), w.end());
      t.wait_chan = -1;
      t.chain_dl = dl;
      on_unblock(target);                       // recursion — a brigade unwinds here
    } else { ++t.mailbox; t.mail_dl.push_back(dl); }
  }

  void on_unblock(int id) {                     // shared by external wake and SLEEP/TIMER expiry
    if (T(id).st != State::Blocked) return;     // D2: with no waiter the letter is dropped
    ev("ready", id, "cause", cause_of(T(id)));  // X: the primitive is over — its line first, then
    ++T(id).pc;                                 // the zero-wait lines of what the step passes
    step(id);
    if (T(id).st == State::Ready) { pol_->on_ready(id); maybe_preempt(id); } else settled(id);
  }

  void on_lane(const Event& e) {
    if (e.task != running_) return;
    if (check_gen_ && e.gen != T(e.task).gen) return;   // voided reservation
    const int id = e.task;
    release();
    if (T(id).run_left == 0) boundary(id);             // RUN demand satisfied
    else slice_over(id);
  }

  void arm_lane(int id) {
    const i64 h = pol_->horizon(id);
    const i64 dt = h == kNoHorizon ? T(id).run_left : std::min(T(id).run_left, h);
    push(now_ + dt, Kind::Lane, id, T(id).gen);
  }

  void dispatch() {
    if (running_ >= 0) { assert(lane_prev_ < 0); return; }
    while (!pending_.empty()) {                // U3: the lane is free — the drain is over
      const int idx = pending_.front(); pending_.pop_front();
      apply_config(idx);
    }
    cap_gate();                               // V: filter before the policy picks
    const int id = pol_->pick();
    const int prev = lane_prev_;              // Q2: a slice just ended — a switch only if the
    lane_prev_ = -1;                          // policy picks someone else
    if (prev >= 0 && id != prev) ev("run_end", prev, "reason", "preempt");
    if (id < 0) return;
    running_ = id;
    set_st(id, State::Running);
    lane_start_ = now_;
    arm_lane(id);
    arm_cap_timer();        // V: armed once the holder is known — the gate call before the
                            // pick had no holder to look at
    if (id != prev) ev("run_start", id);
  }

  void on_depart(int id) {
    if (T(id).st == State::Done) return;   // X: a task that exited before its depart has ended once
    if (running_ == id) { ev("run_end", id, "reason", "depart"); release(); }
    if (T(id).wait_chan >= 0) {
      auto& w = chan_waiters_[(std::size_t)T(id).wait_chan];
      w.erase(std::remove(w.begin(), w.end(), id), w.end());
    }
    set_st(id, State::Done);
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

static void compile_prog(const Json& a, Sim& s, const IdMap& ids, const IdMap& spawn,
                         std::vector<Instr>& out) {
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
                              Instr i{Op::WAKE};
                              auto it = ids.find(tg);
                              if (it != ids.end()) i.target = it->second;   // top-level: fixed here
                              else {                                        // W: a spawn-table entry
                                auto st = spawn.find(tg);
                                if (st == spawn.end()) die("WAKE target is not a known task: " + tg);
                                i.target = -st->second - 1;                 // resolved at its birth
                              }
                              out.push_back(i); }
    else if (op == "LOOP")  {
      const std::size_t b = out.size();
      Instr bi{Op::LOOP_BEGIN};
      const Json& c = in.at("count");
      if (c.k == Json::K::Str) { if (c.s != "unbounded") die("LOOP.count: " + c.s); bi.count = -1; }
      else bi.count = c.as_int("LOOP.count");
      out.push_back(bi);
      compile_prog(in.at("body"), s, ids, spawn, out);
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
  IdMap spawn;                                  // pass 1b (W) — every spawn-table entry gets a
  for (const Json& e : evs.arr) {               // slot before any program is resolved, since a
    if (e.at("op").as_str("op") != "arrive") continue;   // member wakes siblings both earlier
    if (!e.has("spawn_table")) continue;                 // and later in the table
    for (const Json& c : e.at("spawn_table").arr) {
      const std::string& cid = c.at("id").as_str("id");
      if (ids.count(cid)) die("spawn_table id collides with a top-level task: " + cid);
      if (!spawn.emplace(cid, 0).second) die("duplicate spawn_table id: " + cid);
      spawn[cid] = s.spawn_slot(cid);
    }
  }
  for (const Json& e : evs.arr) {               // pass 2 — programs and wakes
    const std::string& op = e.at("op").as_str("op");
    if (op == "arrive") {
      const int id = ids.at(e.at("id").as_str("id"));
      std::vector<Instr> prog;
      compile_prog(e.at("program"), s, ids, spawn, prog);
      s.set_prog(id, std::move(prog));
      if (e.has("spawn_table")) {
        std::vector<ChildSpec> tab;
        for (const Json& c : e.at("spawn_table").arr) {
          std::vector<Instr> cp;
          compile_prog(c.at("program"), s, ids, spawn, cp);
          ChildSpec cs{c.at("id").as_str("id"), c.at("name").as_str("name"), std::move(cp)};
          cs.slot = spawn.at(cs.sid);           // W: the slot its siblings' WAKEs resolve through
          tab.push_back(std::move(cs));
        }
        s.set_spawn(id, std::move(tab), (int)e.at("fork_cap").as_int("fork_cap"));
      }
    } else if (op == "wake") {
      s.wake(e.at("t").as_int("t"), s.channel(e.at("channel").as_str("channel")));
    } else die("unknown event op: " + op);
  }
  s.classify_periodic();
}

// The lottery PRNG seed — FNV-1a 64 of the workload id. Not a config field (vocab §2 LOTTERY)
static std::uint64_t fnv1a(const std::string& s) {
  std::uint64_t h = 0xCBF29CE484222325ull;
  for (unsigned char ch : s) { h ^= ch; h *= 0x100000001B3ull; }
  return h;
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
    // V: the cap. null = no ceiling. Clamping into 0.05–0.95 is the upstream validator's job,
    // as for the MLFQ params — what is checked here is only that the arithmetic holds
    const Json& bc = c.at("batch_bandwidth_cap");
    if (bc.k == Json::K::Null) ce.cap_bp = -1;
    else {
      const double v = bc.as_num("batch_bandwidth_cap");
      if (!(v > 0.0 && v <= 1.0)) die("batch_bandwidth_cap must be null or in (0,1]");
      ce.cap_bp = (int)std::llround(v * kShareDen);
    }
    const Json& pp = c.at("params");
    if (ce.algorithm == "MLFQ") {            // params: exactly the fields declared per algorithm
      if (pp.obj.size() != 4) die("MLFQ params must have 4 fields");
      ce.params.num_queues        = (int)pp.at("num_queues").as_int("num_queues");
      ce.params.timeslice_us      = pp.at("timeslice_us").as_int("timeslice_us");
      ce.params.timeslice_growth  = (int)pp.at("timeslice_growth").as_int("timeslice_growth");
      ce.params.boost_interval_us = pp.at("boost_interval_us").as_int("boost_interval_us");
    } else if (ce.algorithm == "EDF") {
      if (pp.obj.size() != 1) die("EDF params must have 1 field");
      ce.params.residual_timeslice_us = pp.at("residual_timeslice_us").as_int("residual_timeslice_us");
    } else if (ce.algorithm == "LOTTERY") {
      if (pp.obj.size() != 2) die("LOTTERY params must have 2 fields");
      ce.params.timeslice_us   = pp.at("timeslice_us").as_int("timeslice_us");
      // the schema's only real number → an integer here; every draw compares integers only
      ce.params.batch_share_bp = (int)std::llround(pp.at("batch_share").as_num("batch_share") * kShareDen);
    } else if (ce.algorithm == "FIFO") {
      if (!pp.obj.empty()) die("FIFO params must be empty");
    }  // an algorithm off the menu is not in register_policy, so it is rejected at apply time
    out.push_back(std::move(ce));
  }
  s.set_schedule(std::move(out));
}

int main(int argc, char** argv) {
  Sim sim;
  Fifo fifo;
  Mlfq mlfq(sim, sim);
  Edf edf(sim);
  Lottery lottery(sim);
  sim.attach(mlfq);
  sim.register_policy("MLFQ", mlfq);
  sim.register_policy("FIFO", fifo);
  sim.register_policy("EDF", edf);
  sim.register_policy("LOTTERY", lottery);
  if (argc < 2) die("usage: ./sim <workload.json> [<config-schedule.json>]");
  load_workload(argv[1], sim);
  lottery.seed(fnv1a(sim.workload_id()));   // before a schedule file's workload_id overwrites it
  if (argc > 2) load_schedule(argv[2], sim);
  Params p;                     // the boot default when there is no schedule (OSTEP §8 whole)
  sim.run(p);
  sim.report();
}
