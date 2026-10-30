"""Trace primitives — docs/harness/metrics.md §4 and §6.

`compute(run, events, schedule=None)` folds a trace's event stream, with the
run file's `T_end`, chains, and demands, into raw observation rows: one dict
per row with `entity`, `metric`, `t`, `value`, and the attributes that metric
carries. It knows nothing about which file, task role, or condition it is
looking at. The config schedule is the third input (§3): `switch_window` and `boost_window` read
the incoming entry's params from it by `index`.

A `ready(cause = wake)` line completes the task's next WAIT in program order,
so its row carries that WAIT's channel kind from the run file (`input`, `timer`,
`chain`, …; metrics doc §6.1). Each keystroke — an input wake event of the run
file — also gets an `input_latency` row (§6.12), and each wake event on a
timer channel a `timer_latency` row (§6.13): the k-th line on that channel
completes the WAIT the k-th wake serves, wakes queuing with depth, and the row
runs from the wake event to the start of that service; a wake its task never
serves by its end is censored there.

Alongside the rows it returns the guard messages the metrics doc names: more
tail iterations than consumed head ticks per chain, the `deadline` cross-check on
single-stage chains, the stimulus guard — more `input`-channel wake lines than
the run file's input wake events, or a task ending blocked on an input WAIT
while an input wake sent to it before then went unconsumed — a wake line past
the last WAIT of its task's program, and the schedule cross-check (an applied entry the schedule does not
carry, or carries with another algorithm; a switch into MLFQ with no schedule
given).
"""

import bisect
from dataclasses import dataclass, field
from typing import Dict, Iterable, Iterator, List, Optional

_BLOCKING_END = {"block", "exit", "depart"}


def w_single(params) -> int:
    """Lane time for one CPU-bound task to fall from the top MLFQ queue to the
    bottom: one full slice at each upper level (memo 2026-09-08 §4, revised
    2026-09-09), `timeslice_us · Σ_{l=0}^{num_queues−2} growth^l`, rounded down
    to whole µs. The switch window ends when every hog has received this much
    CPU since t_apply."""
    levels = int(params["num_queues"]) - 1
    growth = params["timeslice_growth"]
    return int(params["timeslice_us"] * sum(growth ** l for l in range(levels)))


@dataclass
class _TaskState:
    arrive_t: Optional[int] = None
    running_since: Optional[int] = None
    pending_ready: List[tuple] = field(default_factory=list)   # (t, cause, channel)
    cpu: int = 0
    preempts: int = 0
    end: Optional[tuple] = None                                 # (t, reason)
    run_ends: List[tuple] = field(default_factory=list)         # (t, reason), for hog counting
    occupancy: List[tuple] = field(default_factory=list)        # (start, end) clipped at T_end
    # chain bookkeeping
    ticks: List[int] = field(default_factory=list)              # ready(timer_tick) times
    waits: Optional[Iterator[str]] = None                       # channel kinds of the WAITs still to complete
    input_ready: int = 0                                        # ready(wake) lines on an input channel
    unmatched: List[int] = field(default_factory=list)         # ready(wake) times past the program's last WAIT
    iter_open: Optional[int] = None                             # start t of the open iteration
    iter_ends: List[int] = field(default_factory=list)          # completion t per iteration
    deadlines: List[dict] = field(default_factory=list)
    blocked_wait: bool = False      # blocked on a WAIT: its arrival step or a run_end(block, wait), no line since
    served: Dict[str, List[int]] = field(default_factory=lambda: {"input": [], "timer": []})   # service start per input- and timer-channel ready line, in order


@dataclass
class Switch:
    """One algorithm switch (§6.9): the applied entry, the hogs counted at it, and
    the window length (0 unless the switch is into MLFQ)."""
    t: int
    index: int
    algorithm: str
    hogs: List[str]
    value: int


@dataclass
class Result:
    rows: List[dict]
    guards: List[str]
    switches: List[Switch] = field(default_factory=list)


def compute(run, events: Iterable[dict], schedule=None) -> Result:
    t_end = run.t_end
    chain_of: Dict[str, List[str]] = {}
    for chain in run.chains:
        for tid in chain:
            chain_of[tid] = chain
    heads = {chain[0] for chain in run.chains}

    tasks: Dict[str, _TaskState] = {}
    rows: List[dict] = []
    configs: List[dict] = []
    order: List[str] = []           # task ids in first-seen order

    def state(tid):
        if tid not in tasks:
            info = run.tasks.get(tid)
            tasks[tid] = _TaskState(waits=info.wait_channels() if info is not None else iter(()))
            order.append(tid)
        return tasks[tid]

    def iteration_start(tid, ev):
        """Is this ready line the start of a chain iteration for its stage?"""
        if tid not in chain_of:
            return False
        if tid in heads:
            return ev["cause"] == "timer_tick"
        return ev["cause"] == "wake"

    def close_iteration(st, t):
        if st.iter_open is not None:
            st.iter_ends.append(t)
            st.iter_open = None

    for ev in events:
        kind, t = ev["event"], ev["t"]
        if kind == "config_applied":
            if t < t_end:
                configs.append(ev)
            continue
        st = state(ev["task"])
        if kind == "task_arrive":
            st.arrive_t = t
            info = run.tasks.get(ev["task"])
            st.blocked_wait = info is not None and info.first_op == "WAIT"
        elif kind == "ready":
            if st.running_since is None and st.pending_ready and st.pending_ready[-1][0] < t:
                # no run_start since the task's last ready lines, now past: no RUN lay
                # between them and this one, so the task went on to its next blocking
                # primitive at once. Each waited for nothing (§6.1), and an iteration
                # opened there ended there (§6.2: a TIMER directly after the TIMER)
                for (rt, cause, channel) in st.pending_ready:
                    if rt <= t_end:
                        rows.append(_ready_row(ev["task"], rt, 0, cause, channel))
                        if channel in st.served:
                            st.served[channel].append(rt)
                st.pending_ready = []
                if st.iter_open is not None:
                    close_iteration(st, st.iter_open)
            st.blocked_wait = False
            channel = None
            if ev["cause"] == "wake":
                channel = next(st.waits, None)
                if channel is None:
                    st.unmatched.append(t)
                elif channel == "input":
                    st.input_ready += 1
            if st.running_since is not None:              # inside own occupancy
                if t <= t_end:
                    rows.append(_ready_row(ev["task"], t, 0, ev["cause"], channel))
                    if channel in st.served:
                        st.served[channel].append(t)
            else:
                st.pending_ready.append((t, ev["cause"], channel))
            if ev["cause"] == "timer_tick":
                st.ticks.append(t)
            if iteration_start(ev["task"], ev):
                close_iteration(st, t)                    # zero-wait boundary
                st.iter_open = t
        elif kind == "run_start":
            if t <= t_end:
                for (rt, cause, channel) in st.pending_ready:
                    rows.append(_ready_row(ev["task"], rt, t - rt, cause, channel))
                    if channel in st.served:
                        st.served[channel].append(t)
            st.pending_ready = []
            st.running_since = t
            st.blocked_wait = False
        elif kind == "run_end":
            if st.running_since is not None:
                start = st.running_since
                if start < t_end:
                    st.cpu += min(t, t_end) - start
                    st.occupancy.append((start, min(t, t_end)))
                st.running_since = None
            st.blocked_wait = ev["reason"] == "block" and ev.get("blocked_on") == "wait"
            if t <= t_end:
                st.run_ends.append((t, ev["reason"]))
            if ev["reason"] == "preempt" and t <= t_end:
                st.preempts += 1
            if ev["reason"] in _BLOCKING_END:
                close_iteration(st, t)
        elif kind == "task_end":
            st.end = (t, ev["reason"])
        elif kind == "deadline":
            st.deadlines.append(ev)

    # open occupancy at T_end
    for st in tasks.values():
        if st.running_since is not None and st.running_since < t_end:
            st.cpu += t_end - st.running_since
            st.occupancy.append((st.running_since, t_end))

    # ---- lifetime rows
    busy = 0
    for tid in order:
        st = tasks[tid]
        if st.arrive_t is None or st.arrive_t > t_end:
            continue
        info = run.tasks.get(tid)
        # the task_arrive line's time, the arrival §9's censored turnaround reads: a task
        # whose first instruction is a WAIT has no ready(cause = arrive) line (§11 item 5)
        rows.append(_row(tid, "arrival", t_end, st.arrive_t))
        rows.append(_row(tid, "cpu_delivered", t_end, st.cpu))
        busy += st.cpu
        if info is not None and info.demand is not None:
            rows.append(_row(tid, "demand", t_end, info.demand))
        completed = st.end is not None and st.end[1] == "exit" and st.end[0] <= t_end
        if completed:
            rows.append(_row(tid, "completed", st.end[0], 1))
            rows.append(_row(tid, "turnaround", st.end[0], st.end[0] - st.arrive_t))
        else:
            rows.append(_row(tid, "completed", t_end, 0))
        rows.append(_row(tid, "preempt_count", t_end, st.preempts))
    rows.append(_row("lane", "busy", t_end, busy))

    # ---- schedule rows
    for i, ev in enumerate(configs):
        until = configs[i + 1]["t"] if i + 1 < len(configs) else t_end
        rows.append(_row("schedule", "config_interval", ev["t"], until - ev["t"],
                         provenance=ev["provenance"], algorithm=ev["algorithm"],
                         index=ev["index"]))

    # ---- switch rows (§6.9) and the schedule cross-check
    guards: List[str] = []
    switches: List[Switch] = []
    for i, ev in enumerate(configs):
        entry = schedule.entry(ev["index"]) if schedule is not None else None
        if schedule is not None:
            if entry is None:
                guards.append(f"config_applied index {ev['index']} at t={ev['t']}: the "
                              f"config schedule has no entry {ev['index']}")
            elif entry.algorithm != ev["algorithm"]:
                guards.append(f"config_applied index {ev['index']} at t={ev['t']} says "
                              f"{ev['algorithm']} but schedule entry {ev['index']} is "
                              f"{entry.algorithm}")
                entry = None
        if i == 0 or ev["algorithm"] == configs[i - 1]["algorithm"]:
            continue
        t_apply = ev["t"]
        hogs = [tid for tid in order if _is_hog(tasks[tid], t_apply)]
        if ev["algorithm"] == "MLFQ":
            if entry is None or entry.algorithm != "MLFQ":
                if schedule is None:
                    guards.append(f"switch into MLFQ at t={t_apply} (index {ev['index']}): "
                                  "no config schedule given, switch_window row omitted")
                continue
            # the window ends when the last hog has received W_single of CPU since
            # t_apply; clipped at the next algorithm switch or T_end
            limit, limit_name = t_end, "T_end"
            for later in configs[i + 1:]:
                if later["algorithm"] != ev["algorithm"]:
                    limit, limit_name = later["t"], f"the switch at index {later['index']}"
                    break
            need = w_single(entry.params)
            end = t_apply
            for tid in hogs:
                reached = _time_of_cpu_since(tasks[tid].occupancy, t_apply, need)
                if reached is None or reached > limit:
                    guards.append(f"switch into MLFQ at t={t_apply} (index {ev['index']}): hog "
                                  f"{tid} had not received W_single = {need} µs by {limit_name} "
                                  f"({limit}); window clipped there")
                    reached = limit
                end = max(end, reached)
            value = end - t_apply
            # ---- boost windows (§6.10): the boost timer restarts at every applied MLFQ
            # entry of this interval, a same-algorithm one included, as in the reference
            # simulator (`apply_config` voids the policy timers, `Mlfq::start` arms the
            # boost at the applied time + boost_interval_us). So the instants are
            # t_e + k·boost_interval_us (k ≥ 1) of the latest applied entry e, before the
            # next entry applies and before the interval's end; each window is sized by the
            # same rule from its instant with e's params, clipped at the next boost instant
            # (or the interval's end). An entry the schedule does not carry as MLFQ (a guard
            # above) keeps the params before it.
            segments = [(ev, entry.params)]
            for later in configs[i + 1:]:
                if later["algorithm"] != ev["algorithm"]:
                    break
                later_entry = schedule.entry(later["index"])
                ok = later_entry is not None and later_entry.algorithm == "MLFQ"
                segments.append((later, later_entry.params if ok else segments[-1][1]))
            instants = []                               # (t_b, entry in force, its params)
            for j, (e, params) in enumerate(segments):
                stop = segments[j + 1][0]["t"] if j + 1 < len(segments) else limit
                boost = int(params["boost_interval_us"])
                t_b = e["t"] + boost
                while t_b < stop:
                    instants.append((t_b, e, params))
                    t_b += boost
            for n, (t_b, in_force, params) in enumerate(instants):
                t_next = instants[n + 1][0] if n + 1 < len(instants) else limit
                need_b = w_single(params)
                hogs_b = [tid for tid in order if _is_hog(tasks[tid], t_b)]
                end_b = t_b
                for tid in hogs_b:
                    reached = _time_of_cpu_since(tasks[tid].occupancy, t_b, need_b)
                    if reached is None or reached > t_next:
                        reached = t_next
                    end_b = max(end_b, reached)
                rows.append(_row("schedule", "boost_window", t_b, end_b - t_b,
                                 algorithm="MLFQ", index=in_force["index"], hogs=len(hogs_b)))
        else:
            value = 0
        switches.append(Switch(t=t_apply, index=ev["index"], algorithm=ev["algorithm"],
                               hogs=hogs, value=value))
        rows.append(_row("schedule", "switch_window", t_apply, value,
                         algorithm=ev["algorithm"], index=ev["index"], hogs=len(hogs)))

    # ---- job rows and chain guards (§6.2 under the TIMER skip rule; 9.11 D3, D17; 9.14 decision 1)
    for chain in run.chains:
        head, tail = chain[0], chain[-1]
        if head not in tasks:
            continue
        hs, ts = tasks[head], tasks[tail]
        period = run.tasks[head].period_us
        # Each ready(timer_tick) line marks the consumption of one tick: the latest
        # grid tick at or before the line's time, the grid being t0 + k*period with
        # t0 the task's first TIMER execution — its first ready(timer_tick) line,
        # at its arrival: the TIMER-first invariant makes the TIMER the task's first
        # instruction and the executor executes it in the arrival step, on a free
        # lane or a busy one (metrics doc §11, assumption 4). A tick consumed late sits
        # before its line, never at it. Every unconsumed tick between two
        # consumptions was skipped: a job with no work and no completion, missed.
        # The j-th consumption is the tail's j-th iteration, since a skipped tick
        # sends no wake down the chain and wakes queue with depth.
        # The tail can fall short at T_end and that is no error: an iteration still
        # running there is not completed within the window (metrics doc §4), and a
        # tick consumed shortly before T_end has no time to finish its frame (9.16
        # D3). So only a tail with more completions than consumed ticks fails; a
        # wake lost mid-run, which also leaves the tail short, is not caught here.
        consumed = [tk for tk in hs.ticks if tk <= t_end]
        if not consumed:
            continue
        t0 = consumed[0]
        indices = [(tk - t0) // period for tk in consumed]
        ends = [e for e in ts.iter_ends if e <= t_end]
        if len(ends) > len(consumed):
            guards.append(f"chain {head}: tail {tail} completed {len(ends)} iteration(s) "
                          f"for {len(consumed)} consumed head tick(s) inside the window")
        jobs = []                                   # (tick index, completion or None, skipped)
        prev = -1
        for j, k in enumerate(indices):
            if k <= prev:
                guards.append(f"chain {head}: ready(timer_tick) at t={consumed[j]} consumes tick {k}, "
                              f"not after tick {prev}")
                continue
            for s in range(prev + 1, k):
                jobs.append((s, None, True))
            jobs.append((k, ends[j] if j < len(ends) else None, False))
            prev = k
        for k, completion, skipped in jobs:
            tick = t0 + k * period
            if skipped:
                rows.append(_row(head, "job", tick, None, period_us=period, skipped=1))
            elif completion is not None:
                rows.append(_row(head, "job", tick, completion - tick, period_us=period, skipped=0))
        if len(chain) == 1:
            # one deadline line per tick, consumed or skipped, in tick order; a skipped
            # tick's line is read by `met` alone (9.11 D17), a consumed tick's by its
            # completion and slack
            lines = [dl for dl in hs.deadlines if dl["t"] <= t_end]
            for n, (k, completion, skipped) in enumerate(jobs):
                if n >= len(lines):
                    break
                dl = lines[n]
                tick = t0 + k * period
                if skipped:
                    if dl["met"]:
                        guards.append(f"deadline line {n} for {head} (t={dl['t']}) says met where "
                                      f"tick {k} was skipped")
                elif completion is not None:
                    if dl["t"] != completion or dl["slack_us"] != period - (completion - tick):
                        guards.append(f"deadline line for {head} job {k} (t={dl['t']}, "
                                      f"slack={dl['slack_us']}) disagrees with the job row "
                                      f"(completion {completion}, value {completion - tick})")

    # ---- input_latency (§6.12) and timer_latency (§6.13): one row per wake event on an input
    # channel (a keystroke) or a timer channel, at the wake. The k-th line on that channel served
    # the k-th wake (wakes queue with depth, §11 item 2); a wake served by no line inside the
    # window is censored at its task's end or T_end
    for kind, metric, wakes, noun in (("input", "input_latency", run.input_wakes, "keystroke"),
                                      ("timer", "timer_latency", run.timer_wakes, "timer wake")):
        for tid, times in wakes.items():
            st = tasks.get(tid)
            served = st.served[kind] if st is not None else []
            end = min(st.end[0], t_end) if st is not None and st.end is not None else t_end
            for k, wt in enumerate(times):
                if k < len(served):
                    if served[k] < wt:
                        guards.append(f"task {tid}: {kind} line {k} served at t={served[k]}, before its "
                                      f"{noun} at t={wt}")
                        continue
                    rows.append(_row(tid, metric, wt, served[k] - wt, censored=0))
                elif wt < end:
                    rows.append(_row(tid, metric, wt, end - wt, censored=1))

    # ---- stimulus guard (§8), and wake lines the run file has no WAIT for. A task that
    # ends with input it has not reached, behind its program, is no guard; one that ends
    # blocked on an input WAIT while an input wake sent to it before then went unconsumed
    # lost that wake
    for tid, times in run.input_wakes.items():
        st = tasks.get(tid)
        if st is None:
            guards.append(f"task {tid}: {len(times)} input wake event(s) in the run file and "
                          "no line in the trace")
            continue
        if st.input_ready > len(times):
            guards.append(f"task {tid}: {st.input_ready} input ready(wake) line(s) for "
                          f"{len(times)} input wake event(s) in the run file")
        if st.blocked_wait and st.running_since is None and not st.pending_ready:
            end = min(st.end[0], t_end) if st.end is not None else t_end
            sent = bisect.bisect_left(times, end)
            if sent > st.input_ready and next(st.waits, None) == "input":
                guards.append(f"task {tid}: blocked on an input WAIT at its end (t={end}) with "
                              f"{sent - st.input_ready} input wake event(s) sent before then "
                              "unconsumed")
    for tid in order:
        extra = tasks[tid].unmatched
        if extra:
            guards.append(f"task {tid}: {len(extra)} ready(wake) line(s) past the last WAIT "
                          f"of its program, the first at t={extra[0]}")

    return Result(rows=rows, guards=guards, switches=switches)


def _is_hog(st, t_apply) -> bool:
    """Memo §4: a task alive at t_apply whose first occupancy to end after
    t_apply (inside the window) ends with `run_end(reason = preempt)`."""
    if st.arrive_t is None or st.arrive_t > t_apply:
        return False
    if st.end is not None and st.end[0] <= t_apply:
        return False
    # run_ends is in trace order, so the first run end past t_apply is found by bisection — the boost-window loop
    # asks this per hog per boost instant, and a long file's task holds millions of run ends (9.14 D14)
    i = bisect.bisect_right(st.run_ends, t_apply, key=lambda e: e[0])
    return i < len(st.run_ends) and st.run_ends[i][1] == "preempt"


def _time_of_cpu_since(occupancy, t0, need) -> Optional[int]:
    """The instant a task's CPU received since t0 reaches `need`, from its
    occupancy intervals; None if it never does inside the window. The intervals
    are in trace order and disjoint, so those ending at or before t0 are a prefix
    skipped by bisection (9.14 D14)."""
    got = 0
    for j in range(bisect.bisect_right(occupancy, t0, key=lambda iv: iv[1]), len(occupancy)):
        start, end = occupancy[j]
        start = max(start, t0)
        if got + (end - start) >= need:
            return start + (need - got)
        got += end - start
    return None


def _ready_row(entity, t, value, cause, channel):
    if channel is None:
        return _row(entity, "ready_wait", t, value, cause=cause)
    return _row(entity, "ready_wait", t, value, cause=cause, channel=channel)


def _row(entity, metric, t, value, **attrs):
    r = {"entity": entity, "metric": metric, "t": t, "value": value}
    r.update(attrs)
    return r
