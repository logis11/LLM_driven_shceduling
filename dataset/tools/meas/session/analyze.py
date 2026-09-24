#!/usr/bin/env python3
"""Per-phase analysis of a 9.9 session run (changelog D4–D14; method §4, §5).

  analyze.py <run-dir> [--json out.json] [--phase NAME ...] [--from-s SECONDS]

`--from-s` reads the phase from that many seconds past its first row and nothing before, which is how the
unpolled part of a probe is read (D19): `size_steady.py` passes the cut it takes from the last poll.

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
import bisect
import json
import os
import re
import sys

TOOLS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # dataset/tools
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

from meas.campaign.analyze import (   # noqa: E402  — one wake rule and one component layer for every campaign
    ROW, TASK, Row, load_all_wakeups, load_wakeups, merge_resumes, open_text, per_thread,
)
from meas.desktop.analyze import phases_in, slice_profile  # noqa: E402

ENTRIES = ("gnome-shell", "pipewire", "systemd", "dbus-daemon")

# D23, in the form of 9.5 D64: a cron job's session is a rare event within the phase, not a component's wake.
# Whether an 1800 s window meets one is decided by the clock — the hourly `run-parts` at 17 past, the sysstat job
# at 23:59, the daily jobs — so the population a repeat draws from is not stationary: in the first batch cron woke
# pid 1 36-38 times a phase, in the pair that followed 0, and pid 1 carried 20-23 runs of 1 ms or more against
# 11-12.
#
# D64 picks its event out by a run floor, chrome's heavy pass having no other marker. This one has a cause, so it
# is taken by cause: each wakeup by `cron` opens a window of CRON_EVENT_S, and every row of every entry inside it
# belongs to the event — the wakes cron issues and the scope work logind mediates for the session, which carries
# logind's own comm and which a waker-only rule leaves behind. A floor would instead cut by size, removing the
# heavy runs of a repeat whose window met no cron session at all and biasing every quantile above it.
#
# The window is symmetric, two seconds each way from a wakeup. It straddles its marker because pid 1 does the
# scope work before cron's own wakeups: in repeat 47 seven runs of 1 ms or more fall at +318 s and the cron burst
# at +319 s. Two seconds is where the value stops moving — pid 1's mean run over the rows left is 0.207, 0.208,
# 0.211 and 0.219 ms in the four repeats that met a session at ±2 s and the same at ±5 s, against 0.220-0.228 with
# no window at all — so the footprint is inside ±2 s and the window is not cutting into unrelated work. The rows
# leave the component, which is read without them, and the event is stated per repeat with its count, its runs,
# its times into the phase and its rate over the phase time pooled.
CRON_WAKER = r"^cron$"
CRON_EVENT_S = 2.0
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


def poll_summary(D, phase, _unused=None):
    """The probe's polls: when the shield, the blank and SessionIsActive were first seen, seconds from the first
    poll. The polls carry a monotonic clock and `edges.jsonl` the wall clock, so the first poll is the origin.
    `first_mono_s` and `last_mono_s` are on the polls' own clock, which is the trace's (D19)."""
    p = os.path.join(D, f"poll.{phase}.jsonl")
    if not os.path.exists(p):
        return None
    polls = [json.loads(ln) for ln in open(p) if ln.strip()]
    if not polls:
        return None
    t0 = polls[0]["mono_ns"]
    first = lambda f: next(((x["mono_ns"] - t0) / 1e9 for x in polls if f(x)), None)
    return {"polls": len(polls), "span_s": round((polls[-1]["mono_ns"] - t0) / 1e9, 1),
            "first_mono_s": round(t0 / 1e9, 6), "last_mono_s": round(polls[-1]["mono_ns"] / 1e9, 6),
            "first_shield_s": first(lambda x: x.get("shield_active")),
            "first_blank_s": first(lambda x: x.get("power_save_mode") in (1, 2, 3)),
            "session_active_all": all(x.get("session_active") for x in polls) if polls else None,
            "power_save_modes": sorted({x.get("power_save_mode") for x in polls if x.get("power_save_mode") is not None})}


def cron_windows(times, w=CRON_EVENT_S):
    """The windows a cron session occupies: `w` seconds each side of every wakeup by `cron`, overlaps merged."""
    out = []
    for t in sorted(times):
        if out and t - w <= out[-1][1]:
            out[-1][1] = max(out[-1][1], t + w)
        else:
            out.append([t - w, t + w])
    return out


def split_cron(rows, windows):
    """(rows the component keeps, [(t_in, run_ms)] of the rows inside a cron session's window) — D23."""
    if not windows:
        return rows, []
    starts = [a for a, _ in windows]
    keep, events = [], []
    for r in rows:
        i = bisect.bisect_right(starts, r.t_in) - 1
        (events.append((r.t_in, r.run)) if i >= 0 and r.t_in <= windows[i][1] else keep.append(r))
    return keep, events


def analyze_phase(D, phase, meas_cpu, from_s=0.0, from_mono=None):
    """`from_s` starts the phase that many seconds past its first row; `from_mono` at that monotonic second of
    the trace itself (the clock `perf sched record -k CLOCK_MONOTONIC` and the polls' `mono_ns` share), which is
    how the region past the probe's last poll is read (D19). Everything — rates, components, the foreign counts
    and the slice profile — is computed over what is left."""
    th = next((f"perf.{phase}.timehist.txt{s}" for s in (".gz", "")
               if os.path.exists(os.path.join(D, f"perf.{phase}.timehist.txt{s}"))), None)
    if not th:
        return {"missing": True}
    censuses = census_of(D, phase)
    if not censuses:
        return {"missing": True, "why": "no census"}
    inst, other, kthreads = instances_of(censuses)
    rows_cpu, (t0, t1) = load_trace(os.path.join(D, th))
    cut = from_mono if from_mono is not None else (t0 + from_s if from_s else None)
    if cut is not None:
        if not t0 <= cut < t1:
            return {"missing": True, "why": f"the cut {cut} is outside the trace [{t0}, {t1}]"}
        rows_cpu = [(r, cpu) for r, cpu in rows_cpu if r.t_in >= cut]
        t0 = cut
    span = max(t1 - t0, 1e-6)
    entry_pids = {p for by_i in inst.values() for pids in by_i.values() for p in pids}

    wk = next((os.path.join(D, f"perf.{phase}.wakeups.txt{s}") for s in (".gz", "")
               if os.path.exists(os.path.join(D, f"perf.{phase}.wakeups.txt{s}"))), None)
    wakeups = load_all_wakeups(wk, entry_pids) if wk else {}
    # D23: the windows a cron job's session occupies, from its wakeups of any entry thread
    cron_wins = cron_windows([t for t, _comm, _tid in (load_wakeups(wk, entry_pids, CRON_WAKER) if wk else [])])
    llvm = [r for r, _ in rows_cpu if r.pid in entry_pids and r.comm.startswith("llvmpipe-")]
    mine = [r for r, _ in rows_cpu if r.pid in entry_pids and not r.comm.startswith("llvmpipe-")]
    mine, merged = merge_resumes(mine, wakeups, by_state=True)
    on_cpu = {cpu for r, cpu in rows_cpu if r.pid in entry_pids}

    out = {"span_s": round(span, 3), "t0": round(t0, 6), "from_mono": round(cut, 6) if cut is not None else None,
           "resumes_merged": merged, "meas_cpu": meas_cpu,
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
        rows, cron_events = split_cron(rows, cron_wins)        # D23: read without them, stated beside them
        threads, samples = components(rows, ipids, span)
        out["entries"][e] = {
            "instances": {i: sorted(p) for i, p in ipids.items()},
            "missing_instances": sorted(i for i, p in ipids.items() if not p),
            "span_s": round(span, 3),
            "wakes_per_s": round(len(rows) / span, 3),
            "cpu_share": round(sum(r.run for r in rows) / 1000 / span, 6),
            "slices": slice_profile(rows, t0, span),
            "cron_event": {"waker": "cron", "window_s": CRON_EVENT_S, "windows": len(cron_wins),
                           "count": len(cron_events),
                           "runs_ms": [round(x, 3) for _, x in cron_events],
                           "at_s": [round(t - t0, 1) for t, _ in cron_events]},
            "threads": threads, "_samples": samples}
    t_start = next((json.loads(ln)["mono_ns"] for ln in open(os.path.join(D, "edges.jsonl"))
                    if ln.strip() and json.loads(ln).get("phase") == phase and json.loads(ln).get("edge") == "start"), None) \
        if os.path.exists(os.path.join(D, "edges.jsonl")) else None
    if t_start is not None:
        out["polls"] = poll_summary(D, phase, t_start)
    return out


def analyze_run_dir(D, only=(), from_s=0.0):
    report = json.load(open(os.path.join(D, "report.json")))
    meas_cpu = int(report.get("pin.load_cpu") or 0)
    res = {"run_dir": D, "app": report.get("app"), "repeat": report.get("repeat"), "mode": report.get("mode"),
           "gate": report.get("gate"), "edge_idle": report.get("edge.idle"), "phases": {}}
    for phase in phases_in(D):
        if only and phase not in only:
            continue
        res["phases"][phase] = analyze_phase(D, phase, meas_cpu, from_s=from_s)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("--phase", action="append", default=[])
    ap.add_argument("--json")
    ap.add_argument("--from-s", type=float, default=0.0)
    a = ap.parse_args()
    res = analyze_run_dir(a.run_dir, tuple(a.phase), from_s=a.from_s)
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
