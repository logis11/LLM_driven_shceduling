"""Trace primitives — docs/harness/metrics.md §4 and §6.

`compute(run, events, schedule=None)` folds a trace's event stream, with the
run file's `T_end`, chains, and demands, into raw observation rows: one dict
per row with `entity`, `metric`, `t`, `value`, and the attributes that metric
carries. It knows nothing about which file, task role, or condition it is
looking at. The config schedule is the third input (§3): `switch_window` reads
the incoming entry's params from it by `index`.

Alongside the rows it returns the guard messages the metrics doc names: tail
iterations versus head ticks per chain, the `deadline` cross-check on
single-stage chains, stimulus counts against the run file's wake events, and
the schedule cross-check (an applied entry the schedule does not carry, or
carries with another algorithm; a switch into MLFQ with no schedule given).
"""

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional

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
    pending_ready: List[tuple] = field(default_factory=list)   # (t, cause)
    cpu: int = 0
    preempts: int = 0
    end: Optional[tuple] = None                                 # (t, reason)
    run_ends: List[tuple] = field(default_factory=list)         # (t, reason), for hog counting
    occupancy: List[tuple] = field(default_factory=list)        # (start, end) clipped at T_end
    # chain bookkeeping
    ticks: List[int] = field(default_factory=list)              # ready(timer_tick) times
    wake_ready: int = 0                                         # ready(wake) lines seen
    iter_open: Optional[int] = None                             # start t of the open iteration
    iter_ends: List[int] = field(default_factory=list)          # completion t per iteration
    deadlines: List[dict] = field(default_factory=list)


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
            tasks[tid] = _TaskState()
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
        elif kind == "ready":
            if st.running_since is not None:              # inside own occupancy
                if t <= t_end:
                    rows.append(_row(ev["task"], "ready_wait", t, 0, cause=ev["cause"]))
            else:
                st.pending_ready.append((t, ev["cause"]))
            if ev["cause"] == "timer_tick":
                st.ticks.append(t)
            if ev["cause"] == "wake":
                st.wake_ready += 1
            if iteration_start(ev["task"], ev):
                close_iteration(st, t)                    # zero-wait boundary
                st.iter_open = t
        elif kind == "run_start":
            if t <= t_end:
                for (rt, cause) in st.pending_ready:
                    rows.append(_row(ev["task"], "ready_wait", rt, t - rt, cause=cause))
            st.pending_ready = []
            st.running_since = t
        elif kind == "run_end":
            if st.running_since is not None:
                start = st.running_since
                if start < t_end:
                    st.cpu += min(t, t_end) - start
                    st.occupancy.append((start, min(t, t_end)))
                st.running_since = None
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
        else:
            value = 0
        switches.append(Switch(t=t_apply, index=ev["index"], algorithm=ev["algorithm"],
                               hogs=hogs, value=value))
        rows.append(_row("schedule", "switch_window", t_apply, value,
                         algorithm=ev["algorithm"], index=ev["index"], hogs=len(hogs)))

    # ---- job rows and chain guards
    for chain in run.chains:
        head, tail = chain[0], chain[-1]
        if head not in tasks:
            continue
        hs, ts = tasks[head], tasks[tail]
        period = run.tasks[head].period_us
        # The k-th ready(timer_tick) line marks the consumption of tick k; the
        # tick itself sits on the TIMER grid, t0 + k*period, with t0 the task's
        # arrival (metrics doc §11, assumption 4). A tick is consumed late when
        # the lane was busy or the task was in backlog, so the line's time is
        # never the tick's.
        consumed = [tk for tk in hs.ticks if tk <= t_end]
        t0 = hs.arrive_t
        ticks = [t0 + k * period for k in range(len(consumed))]
        ends = [e for e in ts.iter_ends if e <= t_end]
        if len(ends) != len(ticks):
            guards.append(f"chain {head}: tail {tail} completed {len(ends)} iteration(s) "
                          f"for {len(ticks)} head tick(s) inside the window")
        for k, tick in enumerate(ticks):
            if k < len(ends):
                rows.append(_row(head, "job", tick, ends[k] - tick, period_us=period))
        if len(chain) == 1:
            for k, dl in enumerate(hs.deadlines):
                if k >= len(ends) or dl["t"] > t_end:
                    break
                if dl["t"] != ends[k] or dl["slack_us"] != period - (ends[k] - ticks[k]):
                    guards.append(f"deadline line for {head} job {k} (t={dl['t']}, "
                                  f"slack={dl['slack_us']}) disagrees with the job row "
                                  f"(completion {ends[k]}, value {ends[k] - ticks[k]})")

    # ---- stimulus guard
    for tid, n in run.wakes.items():
        seen = tasks[tid].wake_ready if tid in tasks else 0
        if seen != n:
            guards.append(f"task {tid}: {seen} ready(wake) line(s) for {n} wake event(s) "
                          "in the run file")

    return Result(rows=rows, guards=guards, switches=switches)


def _is_hog(st, t_apply) -> bool:
    """Memo §4: a task alive at t_apply whose first occupancy to end after
    t_apply (inside the window) ends with `run_end(reason = preempt)`."""
    if st.arrive_t is None or st.arrive_t > t_apply:
        return False
    if st.end is not None and st.end[0] <= t_apply:
        return False
    first = next(((t, reason) for (t, reason) in st.run_ends if t > t_apply), None)
    return first is not None and first[1] == "preempt"


def _time_of_cpu_since(occupancy, t0, need) -> Optional[int]:
    """The instant a task's CPU received since t0 reaches `need`, from its
    occupancy intervals; None if it never does inside the window."""
    got = 0
    for (start, end) in occupancy:
        if end <= t0:
            continue
        start = max(start, t0)
        if got + (end - start) >= need:
            return start + (need - got)
        got += end - start
    return None


def _row(entity, metric, t, value, **attrs):
    r = {"entity": entity, "metric": metric, "t": t, "value": value}
    r.update(attrs)
    return r
