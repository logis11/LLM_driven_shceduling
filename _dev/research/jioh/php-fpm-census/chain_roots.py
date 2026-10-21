#!/usr/bin/env python3
"""census_core's tracing with each wake's path to its cause kept: how the cause reached the wake and where its chain
began. The classes and labels are census_core.Tracer's own (the same rules, in the same order; `check` compares them
wake by wake).

For each wake, `trace` gives (class, label, how, root, hops):
  how    direct — the wake's own wakeup row names the waker the cause is read from (a process outside the tree);
         chain  — the waker is a thread of the measured tree, running in a wake whose cause it passes on (D27 decision 2);
         relay  — the waker is pid 1 or a dbus-daemon, traced on through its own rows;
         D      — the wake continues the wake before it, after a switch-out in D;
         row    — the cause is the row itself (an idle-CPU wake, a relay acting on its own);
  root   the row the cause was read from — (tid it woke, time, waker comm, waker pid) — for a direct wake its own row;
  hops   how many wakes and rows the cause passed through from that row to this wake.

`direct_row` is direct.py's reading, kept beside it: the last wakeup row to the thread at or before the wake's
schedule-in names a waker this tracer classes `outside`.

`runs(traced)` groups the outside-cause wakes by their root: the wakes one outside row reached, how many of them
inherit it, over how many seconds and threads — the form of the `kdenlive_render` case (6 `pgrep` rows reaching
36,040 wakes).
"""

import bisect
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import census_core as cc  # noqa: E402


class RootTracer(cc.Tracer):

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.rmemo = {}

    def r_row(self, tid, j, depth):
        key = ("row", tid, j)
        if key in self.rmemo:
            return self.rmemo[key]
        if depth > 25:
            return "unknown", "chain too deep", "deep", None, 0
        self.rmemo[key] = ("unknown", "cycle", "cycle", None, 0)
        t, wc, wt, wp = self.rows_to[tid][j]
        if wp is None:
            res = ("own", "idle CPU (timer or interrupt)", "row", (tid, t, None, None), 0)
        elif wp in self.tree:
            c = self.r_tree_at(wt, t, depth + 1)
            res = (("own", "own thread") if c[0] == "own" else c[:2]) + ("chain", c[3], c[4] + 1)
        elif wp == 1 or wc in cc.RELAY_COMMS:
            k = self.row_before(wt, t)
            while k is not None and k > 0 and self.rows_to[wt][k][1].startswith("rcu_"):
                k -= 1
            if k is None:
                res = ("desktop", f"{wc} on its own (no earlier row)", "row", (tid, t, wc, wp), 0)
            else:
                c = self.r_row(wt, k, depth + 1)
                if c[0] in ("own", "kernel"):
                    res = ("desktop", f"{wc}{'[1]' if wp == 1 else ''} on its own", "row", (tid, t, wc, wp), 0)
                else:
                    res = c[:2] + ("relay", c[3], c[4] + 1)
        else:
            cls, lab = self.process(wp, wc)
            if j == 0 and self.born(tid) and cls == "outside" and lab.startswith("the harness"):
                cls, lab = "own", f"launch, by {lab}"
            res = (cls, lab, "direct", (tid, t, wc, wp), 0)
        self.rmemo[key] = res
        return res

    def r_tree_at(self, tid, t, depth):
        ws = self.starts.get(tid)
        if ws:
            i = bisect.bisect_right(ws, t + cc.EPS) - 1
            if i >= 0:
                return self.r_wake(tid, i, depth)
        j = self.row_before(tid, t)
        if j is None:
            return "own", "tree thread, no earlier row", "row", None, 0
        return self.r_row(tid, j, depth)

    def r_wake(self, tid, i, depth=0):
        key = ("wake", tid, i)
        if key in self.rmemo:
            return self.rmemo[key]
        if depth > 25:
            return "unknown", "chain too deep", "deep", None, 0
        self.rmemo[key] = ("unknown", "cycle", "cycle", None, 0)
        ws = self.wakes[tid]
        w = ws[i]
        prev = ws[i - 1] if i > 0 else None
        if prev is not None and (getattr(prev, "state", "") or "")[:1] == "D":
            c = self.r_wake(tid, i - 1, depth + 1)
            res = c[:2] + ("D", c[3], c[4] + 1)
        else:
            j = self.row_before(tid, w.t_in, prev.t_in if prev is not None else None)
            res = ("unknown", "no wakeup row", "none", None, 0) if j is None else self.r_row(tid, j, depth + 1)
        self.rmemo[key] = res
        return res

    def direct_row(self, tid, t_in):
        ts = self.row_t.get(tid, [])
        j = bisect.bisect_right(ts, t_in + cc.EPS) - 1
        if j < 0:
            return False
        _t, wc, _wt, wp = self.rows_to[tid][j]
        return wp is not None and wp not in self.tree and self.process(wp, wc)[0] == "outside"

    def trace(self, rows):
        """[(row, class, label, how, root, hops, direct_row)] for the given wakes (each one of `wakes_by_tid`)."""
        idx = {(tid, w.t_in): i for tid, ws in self.wakes.items() for i, w in enumerate(ws)}
        out = []
        for r in rows:
            i = idx.get((r.tid, r.t_in))
            if i is None:
                out.append((r, "unknown", "not a traced wake", "none", None, 0, False))
                continue
            cls, lab, how, root, hops = self.r_wake(r.tid, i)
            out.append((r, cls, lab, how, root, hops, cls == "outside" and self.direct_row(r.tid, r.t_in)))
        return out


def check(tracer, rows):
    """The number of wakes whose class or label differs between census_core's tracing and this one (expected 0)."""
    a = tracer.classify(rows)
    b = tracer.trace(rows)
    return sum(1 for (r, c1, l1), (_r, c2, l2, *_x) in zip(a, b) if (c1, l1) != (c2, l2))


def runs(traced, top=10):
    """The outside-cause wakes grouped by the row their cause was read from: {roots, wakes, direct, inherited, largest:
    [{root, waker, wakes, inherited, span_s, threads, comms}]} — `inherited` counting the wakes whose own row is not
    the root."""
    groups = collections.defaultdict(list)
    for r, cls, lab, how, root, hops, _d in traced:
        if cls == "outside" and root is not None:
            groups[root].append((r, how, hops))
    out = []
    for root, ws in groups.items():
        inh = sum(1 for _r, how, _h in ws if how != "direct")
        span = max(r.t_in for r, _h, _x in ws) - root[1]
        out.append({"root_t": round(root[1], 6), "root_tid": root[0], "waker": f"{root[2]}[{root[3]}]",
                    "wakes": len(ws), "inherited": inh, "span_s": round(span, 3),
                    "max_hops": max(h for _r, _h, h in ws),
                    "threads": len({r.tid for r, _h, _x in ws}),
                    "comms": dict(collections.Counter(r.comm for r, _h, _x in ws).most_common(5))})
    out.sort(key=lambda g: -g["wakes"])
    n = sum(g["wakes"] for g in out)
    inh = sum(g["inherited"] for g in out)
    return {"roots": len(out), "wakes": n, "direct": n - inh, "inherited": inh, "largest": out[:top]}
