"""Trace primitives — docs/harness/metrics.md §4 and §6.

`compute(run, events)` folds a trace's event stream, with the run file's
`T_end`, chains, and demands, into raw observation rows: one dict per row with
`entity`, `metric`, `t`, `value`, and the attributes that metric carries. It
knows nothing about which file, task role, or condition it is looking at.

Alongside the rows it returns the guard messages the metrics doc names: tail
iterations versus head ticks per chain, the `deadline` cross-check on
single-stage chains, and stimulus counts against the run file's wake events.
"""

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional

_BLOCKING_END = {"block", "exit", "depart"}


@dataclass
class _TaskState:
    arrive_t: Optional[int] = None
    running_since: Optional[int] = None
    pending_ready: List[tuple] = field(default_factory=list)   # (t, cause)
    cpu: int = 0
    preempts: int = 0
    end: Optional[tuple] = None                                 # (t, reason)
    # chain bookkeeping
    ticks: List[int] = field(default_factory=list)              # ready(timer_tick) times
    wake_ready: int = 0                                         # ready(wake) lines seen
    iter_open: Optional[int] = None                             # start t of the open iteration
    iter_ends: List[int] = field(default_factory=list)          # completion t per iteration
    deadlines: List[dict] = field(default_factory=list)


@dataclass
class Result:
    rows: List[dict]
    guards: List[str]


def compute(run, events: Iterable[dict]) -> Result:
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
                st.running_since = None
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

    # ---- job rows and chain guards
    guards: List[str] = []
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

    return Result(rows=rows, guards=guards)


def _row(entity, metric, t, value, **attrs):
    r = {"entity": entity, "metric": metric, "t": t, "value": value}
    r.update(attrs)
    return r
