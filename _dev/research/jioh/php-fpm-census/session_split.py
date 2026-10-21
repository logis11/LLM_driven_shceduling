#!/usr/bin/env python3
"""9.9's own session pool under the chain rule: of the wakes 9.9 took out of its four entries' components because the
trace leads to a cause outside the observed desktop (changelog D27, `dataset/tools/meas/session/causes.py`), how
many the outside cause raised itself and how many inherit it, and how far each carried value would move with the
inherited ones put back.

  python3 -I session_split.py <artifacts dir> <out dir> [--cpu-model "EPYC 7763"]

The pool is `session/pool.py`'s own (`find_runs`, `pool_app`, `criterion`), over the release's 24 repeats, run three
times with `causes.Causes` replaced in `session/analyze.py` by a subclass defined here (the tools are unchanged):
  as written  every `outside` wake leaves the component, as the committed record has it (the reproduction check);
  direct      only the outside wakes whose own wakeup row names the outside waker leave; the rest are put back;
  direct+fu   the direct ones and the follow-up wakes leave; the chain and D ones are put back.
`event` wakes (a desktop job bound to a clock time, D23's form) leave in all three.

The subclass reads each wake's cause as `Causes.cause` does, in the same order, and also how the cause reached it:
  direct     its own wakeup row names a waker that is not an entry's thread, and `Causes.process` places it;
  chain      the waker is an entry's thread, passing on the cause of the wake it was running in (D27 decision 2);
  D          the wake continues the wake before it, after a switch-out in D (pid 1 waiting for an RCU grace period);
  follow-up  WirePlumber's worker's idle-CPU wake 100.2 ms after its previous wake, which follows that wake's cause
             (`causes.FOLLOW_UP`);
with the row the cause was read from (the root: the thread it woke, its time, the waker) and the hops from it. Every
wake's class and label are compared with `Causes.cause`'s (`differ`, expected 0). Beside it, direct.py's reading:
the last wakeup row to the thread at or before its schedule-in names a waker classed outside or event.

Outputs in <out dir>: `split.json` (per entry and component, the left wakes by cause and by how; the roots), `effect.json`
(the 18 carried values under the three readings), `pooled-direct.json`, `pooled-direct-fu.json` (the variants' pools).
"""

import argparse
import bisect
import collections
import json
import os
import statistics
import sys

TOOLS = "/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling/dataset/tools"
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)
from meas.session import analyze as A  # noqa: E402
from meas.session import causes as C  # noqa: E402
from meas.session import pool as P  # noqa: E402
from meas.stability import TOLERANCE  # noqa: E402

CUR = {"dir": None, "putback": ()}
BY_REP = {}


class SplitCauses(C.Causes):
    REG = []

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.tmemo, self.records, self.compared, self.differ = {}, [], 0, 0
        self.run_dir = CUR["dir"]
        SplitCauses.REG.append(self)

    def trace(self, key, depth=0):
        """(class, label, how, root, hops) of wake `key`, by `Causes.cause`'s rules in its order."""
        if key in self.tmemo:
            return self.tmemo[key]
        if depth > 12:
            return "unknown", "chain too deep", "deep", None, 0
        self.tmemo[key] = ("unknown", "cycle", "cycle", None, 0)
        tid, i = key
        w = self.by_tid[tid][i]
        prev = self.by_tid[tid][i - 1] if i > 0 else None
        if prev is not None and prev.state[:1] == "D":
            c = self.trace((tid, i - 1), depth + 1)
            res = c[:2] + ("D", c[3], c[4] + 1)
            self.tmemo[key] = res
            return res
        rows, ts = self.rows_to.get(tid, []), self.row_t.get(tid, [])
        j = bisect.bisect_right(ts, w.t_in + C.EPS) - 1
        if j < 0 or (prev is not None and ts[j] <= prev.t_in):
            res = ("unknown", "no wakeup row", "none", None, 0)
        else:
            t, wc, wt, wp = rows[j]
            if wp is None:
                res = ("own", "idle CPU (timer or interrupt)", "row", (tid, t, None, None), 0)
                e, inst = self.entry_of[w.pid]
                fu = C.FOLLOW_UP.get((e, inst, w.comm))
                if fu and prev is not None:
                    k = bisect.bisect_right(ts, prev.t_in + C.EPS) - 1
                    if k >= 0 and (i < 2 or ts[k] > self.by_tid[tid][i - 2].t_in) and abs(t - ts[k] - fu[0]) <= fu[1]:
                        c = self.trace((tid, i - 1), depth + 1)
                        res = c[:2] + ("follow-up", c[3], c[4] + 1)
            elif wp in self.entry_of:
                at = self.wake_at(wt, t)
                if at is None:
                    res = ("unknown", "entry waker with no wake", "none", None, 0)
                else:
                    c = self.trace(at, depth + 1)
                    we, wi = self.entry_of[wp]
                    if c[0] != "own":
                        res = c[:2] + ("chain", c[3], c[4] + 1)
                    elif we == self.entry_of[w.pid][0]:
                        res = ("own", f"own thread {wi}/{wc}", "chain", c[3], c[4] + 1)
                    else:
                        res = ("desktop", f"entry {we} ({wi}/{wc}) on its own", "row", (tid, t, wc, wp), 0)
            else:
                cls, lab = self.process(wp, wc)
                res = (cls, lab, "direct", (tid, t, wc, wp), 0)
        self.tmemo[key] = res
        return res

    def direct_row(self, tid, t_in):
        """direct.py's reading: the class of the last wakeup row's waker at or before the schedule-in, when that waker
        is not an entry's thread."""
        ts = self.row_t.get(tid, [])
        j = bisect.bisect_right(ts, t_in + C.EPS) - 1
        if j < 0:
            return None
        _t, wc, _wt, wp = self.rows_to[tid][j]
        if wp is None or wp in self.entry_of:
            return None
        return self.process(wp, wc)[0]

    def split(self, rows):
        idx = {}
        for tid, ws in self.by_tid.items():
            for i, w in enumerate(ws):
                idx[(tid, w.t_in)] = i
        keep, tally, gone = [], {}, []
        for r in rows:
            i = idx.get((r.tid, r.t_in))
            if i is not None:
                cls, lab = self.cause((r.tid, i))
                tr = self.trace((r.tid, i))
            else:
                cls, lab = "unknown", "not a traced wake"
                tr = (cls, lab, "none", None, 0)
            self.compared += 1
            self.differ += (cls, lab) != tuple(tr[:2])
            tally.setdefault(cls, {}).setdefault(lab, 0)
            tally[cls][lab] += 1
            back = cls == "outside" and tr[2] in CUR["putback"]
            (keep.append(r) if cls in C.KEPT or back else gone.append((r.t_in, cls, lab)))
            if cls in ("outside", "event"):
                e, inst = self.entry_of[r.pid]
                self.records.append({"dir": os.path.basename(self.run_dir), "entry": e,
                                     "component": f"{inst}/{r.comm}", "t_in": r.t_in, "run": r.run, "tid": r.tid,
                                     "class": cls, "label": lab, "how": tr[2],
                                     "root": list(tr[3]) if tr[3] else None, "hops": tr[4],
                                     "direct_row": self.direct_row(r.tid, r.t_in)})
        return keep, tally, gone


_orig_run_dir = A.analyze_run_dir
_orig_pool_entry = P.pool_entry


def run_dir(D, only=(), from_s=0.0):
    CUR["dir"] = D
    return _orig_run_dir(D, only, from_s)


def pool_entry(name, by_rep):
    BY_REP[name] = {k: {"span_s": e["span_s"], "samples": {c: {"n": len(s["runs"]), "run": sum(s["runs"])}
                                                             for c, s in (e.get("_samples") or {}).items()}}
                    for k, e in by_rep.items()}
    return _orig_pool_entry(name, by_rep)


A.Causes = SplitCauses
A.analyze_run_dir = run_dir
P.pool_entry = pool_entry


def pool_once(root, cpu_model, putback):
    CUR["putback"] = putback
    SplitCauses.REG.clear()
    BY_REP.clear()
    runs, _g, _o, _p = P.find_runs(root, cpu_model)
    entry = P.pool_app("session", runs["session"])
    return entry, [c for c in SplitCauses.REG], {k: dict(v) for k, v in BY_REP.items()}


def exact(entry, by_rep):
    """Each carried value unrounded: the wake rate as the mean of the per-repeat rates the pool reads, the gap mean as
    the carried table's span over its wakes (Σ span / Σ n, every carried component waking in every repeat), the run
    mean Σ run / Σ n — and the pool's own half-width and verdict."""
    out = {}
    q = entry["stability"]["quantities"]
    for name, ph in entry["phases"]["steady"]["entries"].items():
        for comm in ph["components"]["selected"]:
            reps = by_rep[name]
            ns = {k: r["samples"].get(comm, {"n": 0})["n"] for k, r in reps.items()}
            runs = {k: r["samples"].get(comm, {"run": 0.0})["run"] for k, r in reps.items()}
            spans = {k: r["span_s"] for k, r in reps.items()}
            rate = statistics.fmean(round(ns[k] / spans[k], 6) for k in reps)
            vals = {"wakes/s": rate, "gap mean (ms)": sum(spans.values()) * 1000.0 / sum(ns.values()),
                    "run mean (ms)": sum(runs.values()) / sum(ns.values())}
            for label, v in vals.items():
                c = q[f"{name} {comm} {label}"]
                out[f"{name} {comm} {label}"] = {"value": v, "mean": c["mean"], "half_width": c["half_width"],
                                                 "passes": c["passes"], "carried": c["carried"],
                                                 "wakes": sum(ns.values()), "zero_repeats": sum(1 for x in ns.values() if not x)}
    return out


def summarise(regs):
    differ = sum(c.differ for c in regs)
    compared = sum(c.compared for c in regs)
    recs = [r for c in regs for r in c.records]
    comp = {}
    for r in recs:
        key = f"{r['entry']} {r['component']}"
        c = comp.setdefault(key, {"outside": 0, "event": 0, "how": collections.Counter(), "by_label": {},
                                  "per_repeat": collections.Counter(), "direct_row": collections.Counter(),
                                  "event_how": collections.Counter()})
        if r["class"] == "event":
            c["event"] += 1
            c["event_how"][r["how"]] += 1
            continue
        c["outside"] += 1
        c["how"][r["how"]] += 1
        c["by_label"].setdefault(r["label"], collections.Counter())[r["how"]] += 1
        c["per_repeat"][r["dir"]] += 1
        c["direct_row"][str(r["direct_row"])] += 1
    # the roots: the outside wakes grouped by the row their cause was read from
    groups = collections.defaultdict(list)
    for r in recs:
        if r["class"] == "outside" and r["root"]:
            groups[(r["dir"], tuple(r["root"]))].append(r)
    roots = []
    for (d, root), ws in groups.items():
        roots.append({"dir": d, "root_t": root[1], "root_tid": root[0], "waker": f"{root[2]}[{root[3]}]",
                      "label": ws[0]["label"], "wakes": len(ws), "inherited": sum(1 for w in ws if w["how"] != "direct"),
                      "span_s": round(max(w["t_in"] for w in ws) - root[1], 6), "max_hops": max(w["hops"] for w in ws),
                      "threads": len({w["tid"] for w in ws}),
                      "components": dict(collections.Counter(w["component"] for w in ws))})
    roots.sort(key=lambda g: (-g["wakes"], -g["span_s"]))
    sizes = collections.Counter(g["wakes"] for g in roots)
    delays = sorted(w["t_in"] - w["root"][1] for w in recs if w["class"] == "outside" and w["root"] and w["how"] != "direct")
    pct = lambda p: delays[min(len(delays) - 1, int(p * len(delays)))] if delays else None
    for c in comp.values():
        reps = c.pop("per_repeat")
        c["per_repeat_min_max"] = [min(reps.values()) if len(reps) == 24 else 0, max(reps.values()) if reps else 0]
        c["repeats_with"] = len(reps)
        c["how"] = dict(c["how"])
        c["direct_row"] = dict(c["direct_row"])
        c["event_how"] = dict(c["event_how"])
        c["by_label"] = {k: dict(v) for k, v in c["by_label"].items()}
    return {"compared": compared, "differ": differ, "components": comp, "roots": len(roots),
            "wakes_per_root": dict(sorted(sizes.items())), "largest_roots": roots[:15],
            "inherited_delay_s": {"n": len(delays), "p50": pct(.5), "p90": pct(.9), "p99": pct(.99),
                                  "max": delays[-1] if delays else None},
            "records": recs}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("artifacts")
    ap.add_argument("out")
    ap.add_argument("--cpu-model", default="EPYC 7763")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    results = {}
    for tag, putback in (("as written", ()), ("direct", ("chain", "D", "follow-up")), ("direct+fu", ("chain", "D"))):
        entry, regs, by_rep = pool_once(a.artifacts, a.cpu_model, putback)
        results[tag] = exact(entry, by_rep)
        if tag == "as written":
            split = summarise(regs)
            json.dump(split, open(os.path.join(a.out, "split.json"), "w"), indent=1)
            print(f"compared {split['compared']} wakes, differ {split['differ']}", flush=True)
        else:
            json.dump(entry, open(os.path.join(a.out, f"pooled-{tag.replace('+', '-')}.json"), "w"), indent=1, default=list)
            print(f"{tag}: rule {'holds' if entry['stability']['passes'] else 'does not hold'}", flush=True)
    eff = {}
    for q, base in results["as written"].items():
        row = {"committed": base["mean"], "half_width": base["half_width"], "value": base["value"],
               "passes": base["passes"], "carried": base["carried"], "wakes": base["wakes"]}
        for tag in ("direct", "direct+fu"):
            v = results[tag][q]
            s = (v["value"] - base["value"]) / base["value"]
            row[tag] = {"value": v["value"], "shift": s, "half_width": v["half_width"], "passes": v["passes"],
                        "carried": v["carried"], "wakes": v["wakes"],
                        "beyond_half_width": abs(s) > (base["half_width"] or 0), "beyond_tolerance": abs(s) > TOLERANCE}
        eff[q] = row
    json.dump(eff, open(os.path.join(a.out, "effect.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
