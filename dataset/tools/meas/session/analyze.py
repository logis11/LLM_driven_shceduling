#!/usr/bin/env python3
"""Per-phase analysis of a 9.9 session run (changelog D4–D14; method §4, §5).

  analyze.py <run-dir> [--json out.json] [--phase NAME ...]

The four entries are read from one trace. Each entry's processes are the instances the census names by cgroup
(`census.py`): GNOME Shell; `pipewire`, `wireplumber` and `pipewire-pulse`; pid 1 and the user manager; the system
bus and the session bus. Components are per instance and thread comm (method §5), keyed `<instance>/<comm>`, so
nothing is pooled across instances. The wake rule and the component layer are `campaign/analyze.py`'s, imported.

Two counts sit beside the entries, from every row of the trace on the measured CPU (method §5; D12, D14):
  - `foreign.user`: schedule-ins by user-space processes that are none of the four entries' — the gate; a repeat
    with any is not pooled;
  - `foreign.kernel`: schedule-ins and CPU time of kernel threads, which cannot be moved at run time — reported;
  - `in_unit_other`: processes in a pinned unit that are not its program (an Xwayland, a helper) — moved off by the
    sweeps (D15), so any left on the measured CPU gate the repeat as `foreign.user` does.

`llvmpipe-*` threads are left out of GNOME Shell's components, as `load_rows` leaves them out of every campaign
(9.5 D15: the runner's software rasteriser, a venue artefact); their rows are counted and reported.
"""

import argparse
import json
import os
import re
import sys

TOOLS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # dataset/tools
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

from meas.campaign.analyze import (   # noqa: E402  — one wake rule and one component layer for every campaign
    ROW, TASK, Row, load_all_wakeups, merge_resumes, open_text, per_thread,
)
from meas.desktop.analyze import phases_in, slice_profile  # noqa: E402

ENTRIES = ("gnome-shell", "pipewire", "systemd", "dbus-daemon")
# a pid the census never saw (a process born and gone inside the phase) is told kernel from user by its name
KTHREAD_NAME = re.compile(r"^(kworker/|ksoftirqd/|migration/|rcu_|rcuc/|rcuog/|rcuop/|cpuhp/|idle_inject/|irq/|"
                          r"kthreadd$|khugepaged$|kcompactd|kswapd|watchdog/|jbd2/|writeback|scsi_|hv_|kauditd$)")


def load_trace(path):
    """Every task row of the timehist as (Row, cpu), and the capture window over all rows."""
    rows, t_min, t_max = [], None, None
    with open_text(path) as handle:
        for line in handle:
            m = ROW.match(line)
            if not m:
                continue
            t, cpu, task, _wait, delay, run, st = m.groups()
            tf = float(t)
            t_min = tf if t_min is None or tf < t_min else t_min
            t_max = tf if t_max is None or tf > t_max else t_max
            tm = TASK.match(task.strip())
            if not tm:
                continue
            comm, a, b = tm.group(1), int(tm.group(2)), tm.group(3)
            tid, pid = (a, int(b)) if b else (a, a)
            if pid == 0:
                continue      # the idle task
            run, delay = float(run), float(delay)
            rows.append((Row(tf - run / 1000.0, tf - run / 1000.0 - delay / 1000.0, tf, run, comm, tid, pid, st or ""),
                         int(cpu)))
    rows.sort(key=lambda rc: rc[0].t_in)
    return rows, (t_min or 0.0, t_max or 0.0)


def census_of(D, phase):
    out = []
    for edge in ("start", "end"):
        p = os.path.join(D, f"census.{phase}.{edge}.json")
        if os.path.exists(p):
            out.append(json.load(open(p)))
    return out


def instances_of(censuses):
    """entry -> instance -> set of pids, over the phase's two censuses; the in-unit others; the kernel threads."""
    inst = {e: {} for e in ENTRIES}
    other, kthreads = {}, set()
    for c in censuses:
        for e, by_i in (c.get("instances") or {}).items():
            for i, pids in by_i.items():
                inst.setdefault(e, {}).setdefault(i, set()).update(pids)
        for o in c.get("in_unit_other") or []:
            other[o["pid"]] = o
        kthreads.update(c.get("kthreads") or [])
    return inst, other, kthreads


def foreign(rows_cpu, meas_cpu, entry_pids, other_pids, kthreads, t0, span_s, slice_s=10.0):
    """Schedule-ins on the measured CPU by anything that is none of the entries' processes, split user / kernel,
    with the in-unit others apart; per comm, and per slice so the probe shows when they fall."""
    n = max(1, int(span_s // slice_s))
    out = {k: {"schedule_ins": 0, "cpu_ms": 0.0, "by_comm": {}, "per_slice": [0] * n}
           for k in ("user", "kernel", "in_unit_other")}
    for r, cpu in rows_cpu:
        if cpu != meas_cpu or r.pid in entry_pids:
            continue
        if r.pid in other_pids:
            k = "in_unit_other"
        elif r.pid in kthreads or KTHREAD_NAME.search(r.comm):
            k = "kernel"
        else:
            k = "user"
        c = out[k]
        c["schedule_ins"] += 1
        c["cpu_ms"] += r.run
        b = c["by_comm"].setdefault(r.comm, {"schedule_ins": 0, "cpu_ms": 0.0})
        b["schedule_ins"] += 1; b["cpu_ms"] = round(b["cpu_ms"] + r.run, 3)
        i = int((r.t_in - t0) // slice_s)
        if 0 <= i < n:
            c["per_slice"][i] += 1
    for c in out.values():
        c["cpu_ms"] = round(c["cpu_ms"], 3)
    return out


def components(rows, inst_pids, span):
    """Per instance and thread comm (method §5), keyed `<instance>/<comm>`, with the samples the pool reads."""
    threads, samples = {}, {}
    for i, pids in sorted(inst_pids.items()):
        mine = [r for r in rows if r.pid in pids]
        for comm, c in per_thread(mine, span).items():
            key = f"{i}/{comm}"
            threads[key] = c
            rs = [r for r in mine if r.comm == comm]
            by_tid = {}
            for r in rs:
                by_tid.setdefault(r.tid, []).append(r)
            samples[key] = {"gaps": [(b.t_in - a.t_in) * 1000 for trs in by_tid.values() for a, b in zip(trs, trs[1:])],
                            "runs": [r.run for r in rs], "t_in": sorted(r.t_in for r in rs)}
    return threads, samples


def poll_summary(D, phase, t_start_ns):
    """The probe's polls: when the shield, the blank and SessionIsActive were first seen, seconds from the phase start."""
    p = os.path.join(D, f"poll.{phase}.jsonl")
    if not os.path.exists(p):
        return None
    polls = [json.loads(ln) for ln in open(p) if ln.strip()]
    first = lambda f: next(((x["mono_ns"] - t_start_ns) / 1e9 for x in polls if f(x)), None)
    return {"polls": len(polls),
            "first_shield_s": first(lambda x: x.get("shield_active")),
            "first_blank_s": first(lambda x: x.get("power_save_mode") in (1, 2, 3)),
            "session_active_all": all(x.get("session_active") for x in polls) if polls else None,
            "power_save_modes": sorted({x.get("power_save_mode") for x in polls if x.get("power_save_mode") is not None})}


def analyze_phase(D, phase, meas_cpu):
    th = next((f"perf.{phase}.timehist.txt{s}" for s in (".gz", "")
               if os.path.exists(os.path.join(D, f"perf.{phase}.timehist.txt{s}"))), None)
    if not th:
        return {"missing": True}
    censuses = census_of(D, phase)
    if not censuses:
        return {"missing": True, "why": "no census"}
    inst, other, kthreads = instances_of(censuses)
    rows_cpu, (t0, t1) = load_trace(os.path.join(D, th))
    span = max(t1 - t0, 1e-6)
    entry_pids = {p for by_i in inst.values() for pids in by_i.values() for p in pids}

    wk = next((os.path.join(D, f"perf.{phase}.wakeups.txt{s}") for s in (".gz", "")
               if os.path.exists(os.path.join(D, f"perf.{phase}.wakeups.txt{s}"))), None)
    wakeups = load_all_wakeups(wk, entry_pids) if wk else {}
    llvm = [r for r, _ in rows_cpu if r.pid in entry_pids and r.comm.startswith("llvmpipe-")]
    mine = [r for r, _ in rows_cpu if r.pid in entry_pids and not r.comm.startswith("llvmpipe-")]
    mine, merged = merge_resumes(mine, wakeups, by_state=True)
    on_cpu = {cpu for r, cpu in rows_cpu if r.pid in entry_pids}

    out = {"span_s": round(span, 3), "resumes_merged": merged, "meas_cpu": meas_cpu,
           "entry_cpus_seen": sorted(on_cpu),
           "llvmpipe_rows": len(llvm),
           "foreign": foreign(rows_cpu, meas_cpu, entry_pids, set(other), kthreads, t0, span),
           "in_unit_other": sorted(({"pid": o["pid"], "comm": o["comm"], "instance": o["instance"]}
                                    for o in other.values()), key=lambda o: o["pid"]),
           "display_servers": sorted({d["comm"] for c in censuses for d in c.get("display_servers") or []}),
           "entries": {}}
    for e in ENTRIES:
        ipids = {i: pids for i, pids in inst.get(e, {}).items()}
        rows = [r for r in mine if any(r.pid in pids for pids in ipids.values())]
        threads, samples = components(rows, ipids, span)
        out["entries"][e] = {
            "instances": {i: sorted(p) for i, p in ipids.items()},
            "missing_instances": sorted(i for i, p in ipids.items() if not p),
            "span_s": round(span, 3),
            "wakes_per_s": round(len(rows) / span, 3),
            "cpu_share": round(sum(r.run for r in rows) / 1000 / span, 6),
            "slices": slice_profile(rows, t0, span),
            "threads": threads, "_samples": samples}
    t_start = next((json.loads(ln)["mono_ns"] for ln in open(os.path.join(D, "edges.jsonl"))
                    if ln.strip() and json.loads(ln).get("phase") == phase and json.loads(ln).get("edge") == "start"), None) \
        if os.path.exists(os.path.join(D, "edges.jsonl")) else None
    if t_start is not None:
        out["polls"] = poll_summary(D, phase, t_start)
    return out


def analyze_run_dir(D, only=()):
    report = json.load(open(os.path.join(D, "report.json")))
    meas_cpu = int(report.get("pin.load_cpu") or 0)
    res = {"run_dir": D, "app": report.get("app"), "repeat": report.get("repeat"), "mode": report.get("mode"),
           "gate": report.get("gate"), "edge_idle": report.get("edge.idle"), "phases": {}}
    for phase in phases_in(D):
        if only and phase not in only:
            continue
        res["phases"][phase] = analyze_phase(D, phase, meas_cpu)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("--phase", action="append", default=[])
    ap.add_argument("--json")
    a = ap.parse_args()
    res = analyze_run_dir(a.run_dir, tuple(a.phase))
    for ph in res["phases"].values():        # the sample lists are for the pool, not for the printed record
        for e in (ph.get("entries") or {}).values():
            e.pop("_samples", None)
    if a.json:
        json.dump(res, open(a.json, "w"), indent=1)
    for name, ph in res["phases"].items():
        if ph.get("missing"):
            print(f"{name}: missing")
            continue
        f = ph["foreign"]
        print(f"{name}: span {ph['span_s']}s  foreign user {f['user']['schedule_ins']}  kernel {f['kernel']['schedule_ins']}"
              f"  in-unit other {f['in_unit_other']['schedule_ins']}  display servers {ph['display_servers'] or 'none'}")
        for e, v in ph["entries"].items():
            print(f"   {e}: wakes/s {v['wakes_per_s']}  cpu_share {v['cpu_share']}  components {len(v['threads'])}"
                  + (f"  missing {v['missing_instances']}" if v["missing_instances"] else ""))


if __name__ == "__main__":
    main()
