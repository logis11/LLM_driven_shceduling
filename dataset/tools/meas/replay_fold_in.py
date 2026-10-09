#!/usr/bin/env python3
"""Write the trace-replay streams from the raw releases (9.14 decision 12; dataset/variants.yaml's `replay` set).

replay_fold_in.py <raw-root> [--only ENTRY,…] [--out dataset/replay] [--check]

<raw-root>/<release>/<landing> holds each landing as its release asset unpacks it (SOURCES below names the release,
the asset and the landing's path inside it). For each entry, dataset/replay/replay-<entry>[-<program>].json.gz: one
pooled repeat — the landing's — over the carried phase, as the kind of stream the entry's compilation takes
(wlc/compiler.py, "trace replay"):

  wakes   code-editor, web-browser, renderer-hidden: the tree's merged wakes (campaign/analyze.py's rule — a timehist
          row is a wake when a wakeup row for its thread precedes it, else a resume folded into the wake before), each
          [t_us from the read's start, run_us, thread], the thread an index into the repeat's component list (role/comm,
          9.5 D67); code's idle phase read from 200 s past its start (9.5 D83); the hidden renderers as
          desktop/analyze.py reads them — the renderer processes that are a page's and present for the whole phase,
          the control tab dropped — one stream per renderer, plain comm names;
  cycles  video-call: the play phase's cycles as campaign/pool.py's cycle_windows cuts them (9.5 D75) — a cycle starts
          at each wake of utility/AudioWorkerThre after 5 ms of its silence, its work the tree's segment runs starting
          inside it — each [start_us, work_us, length_us];
  runs    package-upgrade, cpu-batch's python3: the stage's tree as background/analyze.py builds it, the program's
          threads' runs between voluntary blocks with the program-level block after each (build/shapes.py; 9.6 D21,
          D22, D25), in the order of the runs' voluntary sched-outs, each [t_us of the run's first segment, run_us,
          block_us]; a thread's last run without a voluntary end closes the stream with a zero block.

Written byte-stable (gzip without a timestamp, sorted keys); --check exits 1 when a file differs from what the
landings give. The library is not touched: the variant builder points each entry at its stream (wlc/variants.py).
"""

import argparse
import json
import os
import sys
from bisect import bisect_left
from collections import defaultdict

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # dataset/tools
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)
from meas.background import analyze as background  # noqa: E402
from meas.build import shapes  # noqa: E402
from meas.campaign import pool  # noqa: E402
from meas.campaign.analyze import component_name, load_all_wakeups, load_rows, merge_resumes, pid_roles  # noqa: E402
from meas.desktop.analyze import KEEP_ROLE, drop_control_tab, page_renderers  # noqa: E402
from meas.desktop.launch_fold_in import encode  # noqa: E402

# entry -> the one landing its stream is read from (the handoff's table of 2026-10-09). A batch stream must hold the
# CPU its task binds — the bind is the pool's mean CPU total, so about half the repeats fall short of it — and the
# repeat taken is the nearest whose CPU covers the bind (9.14 grill, Q6): the MNIST run's sixth repeat (the first ran
# 1 378.8 s against c2-p1a's 1 389.885 s, 9.10 D88) and the upgrade's fourth (the first ran 25.56 s against the c7
# files' 26.385 s, 9.10 D45), each stated in its file's `why`.
SOURCES = {
    "code-editor": {"release": "meas-ci-2026-09-25", "asset": "meas-interactive-code-windows-1-22.zip",
                    "landing": "36076988843/meas-interactive-code-r1-full", "run_id": "36076988843", "repeat": "1",
                    "subject": "code", "phase": "idle", "kind": "wakes", "read_from_s": 200.0, "program": None,
                    "source": "meas-ci:interactive:2026-09-25"},
    "web-browser": {"release": "meas-ci-2026-09-20", "asset": "meas-interactive-chrome.zip",
                    "landing": "interactive-chrome-from438/35667380500/meas-interactive-chrome-r1-full",
                    "run_id": "35667380500", "repeat": "1", "subject": "chrome", "phase": "idle", "kind": "wakes",
                    "read_from_s": 0.0, "program": None, "source": "meas-ci:interactive:2026-09-20"},
    "renderer-hidden": {"release": "meas-ci-desktop-2026-10-05b",
                        "asset": "meas-desktop-chrome-hidden-r1-full-37281847886.zip",
                        "landing": "meas-desktop-chrome-hidden-r1-full", "run_id": "37281847886", "repeat": "1",
                        "subject": "chrome-hidden", "phase": "steady", "kind": "wakes", "read_from_s": 0.0,
                        "program": None, "source": "meas-ci:desktop:2026-10-05b"},
    "video-call": {"release": "meas-ci-2026-09-20", "asset": "meas-playback-webrtc.zip",
                   "landing": "playback-webrtc-from245/35498811122/meas-playback-webrtc-r1-full",
                   "run_id": "35498811122", "repeat": "1", "subject": "webrtc", "phase": "play", "kind": "cycles",
                   "read_from_s": 0.0, "program": None, "source": "meas-ci:playback:2026-09-20"},
    "package-upgrade": {"release": "meas-ci-background-2026-10-01",
                        "asset": "meas-background-upgrade-r4-full-36848289469.zip",
                        "landing": "meas-background-upgrade-r4-full", "run_id": "36848289469", "repeat": "4",
                        "subject": "upgrade", "phase": "upgrade-install", "kind": "runs", "read_from_s": 0.0,
                        "program": None, "source": "meas-ci:background:2026-10-01",
                        "why": "the first repeat's install stage ran 25.56 s of CPU, 0.83 s short of the 26.385 s the "
                               "c7 files bind (the pooled mean, 9.10 D45); the fourth is the nearest repeat that "
                               "covers it, 27.25 s (the nine: 25.25–29.16 s)"},
    "cpu-batch": {"release": "meas-ci-background-2026-10-03", "asset": "meas-background-mnist-r6-full-37093607991.zip",
                  "landing": "meas-background-mnist-r6-full", "run_id": "37093607991", "repeat": "6",
                  "subject": "mnist", "phase": "mnist-train", "kind": "runs", "read_from_s": 0.0,
                  "program": "python3", "source": "meas-ci:background:2026-10-03",
                  "why": "the first repeat's python ran 1 378.8 s of CPU, 11.0 s short of the 1 389.885 s c2-p1a "
                         "binds (the pooled mean, 9.10 D88); the sixth is the nearest repeat that covers it, 1 399.4 s"},
}


def stream_name(entry, spec):
    return f"replay-{entry}" + (f"-{spec['program']}" if spec.get("program") else "")


# ---- the three stream shapes ---------------------------------------------------------------------------------------

def wake_stream(rows, t0, t_end, roles=None, comms=None):
    """[t_us, run_us, thread] per merged wake with t0 <= t_in < t_end, sorted; the thread an index into `comms`
    (role/comm with roles, the comm alone without), which grows in place so a repeat's streams share one list."""
    comms = comms if comms is not None else []
    index = {c: i for i, c in enumerate(comms)}
    out = []
    for r in rows:
        if r.t_in < t0 or r.t_in >= t_end:
            continue
        name = component_name(roles.get(r.pid, "main"), r.comm) if roles else r.comm
        if name not in index:
            index[name] = len(comms)
            comms.append(name)
        out.append([round((r.t_in - t0) * 1e6), round(r.run * 1000), index[name]])
    out.sort()
    return out


def cycle_stream(app, phase, rows, segments, roles, t0):
    """[start_us, work_us, length_us] per cycle, the cycles cut as pool.cycle_windows cuts them (the starts off the
    reference component's merged wakes, the work the tree's segment runs starting inside the cycle)."""
    comm, rule, value, spacing = pool.CYCLES[(app, phase)]
    ref = sorted((r.t_in, r.run) for r in rows
                 if component_name(roles.get(r.pid, "main"), pool.component_key(app, r.comm)) == comm)
    if rule == "silence_ms":
        found = [t for i, (t, _) in enumerate(ref) if i == 0 or t - ref[i - 1][0] > value / 1000]
    else:
        found = [t for t, run in ref if run >= value]
    starts = []
    for t in found:
        if not starts or t - starts[-1] >= spacing / 1000:
            starts.append(t)
    seg = sorted((s.t_in, s.run) for s in segments)
    times = [t for t, _ in seg]
    out = []
    for a, b in zip(starts, starts[1:]):
        i, j = bisect_left(times, a), bisect_left(times, b)
        out.append([round((a - t0) * 1e6), round(sum(run for _, run in seg[i:j]) * 1000), round((b - a) * 1e6)])
    return out


def run_stream(rows):
    """[t_us, run_us, block_us] per run between voluntary blocks of one program's threads (shapes.runs_between_blocks),
    the block after each as shapes.blocks_after_runs gives it, in the order of the runs' voluntary sched-outs; a
    thread's last run without a voluntary end follows, with a zero block. t_us from the first row's schedule-in."""
    rows = sorted(rows, key=lambda s: s.t_in)
    if not rows:
        return []
    start, end = rows[0].t_in, max(s.t_end for s in rows)
    blocks = shapes.blocks_after_runs(rows, start, end)
    acc, first, out, k = defaultdict(float), {}, [], 0
    for s in rows:
        first.setdefault(s.tid, s.t_in)
        acc[s.tid] += s.run
        if s.state[:1] in shapes.VOLUNTARY:
            out.append([round((first.pop(s.tid) - start) * 1e6), round(acc.pop(s.tid) * 1000), round(blocks[k] * 1000)])
            k += 1
    for tid in sorted(acc, key=lambda t: first[t]):
        if acc[tid] > 0:
            out.append([round((first[tid] - start) * 1e6), round(acc[tid] * 1000), 0])
    return out


# ---- the landings -------------------------------------------------------------------------------------------------

def _phase_files(D, phase):
    th = next((p for p in (f"perf.{phase}.timehist.txt.gz", f"perf.{phase}.timehist.txt")
               if os.path.exists(os.path.join(D, p))), None)
    wk = next((p for p in (f"perf.{phase}.wakeups.txt.gz", f"perf.{phase}.wakeups.txt")
               if os.path.exists(os.path.join(D, p))), None)
    if not th or not wk:
        raise SystemExit(f"{D}: no timehist/wakeups record of the {phase} phase")
    return os.path.join(D, th), os.path.join(D, wk)


def _campaign_rows(D, spec):
    """(merged wakes, raw segments, roles, t0, t1, the snapshots' pid sets) of the phase, as campaign/analyze reads it."""
    phase = spec["phase"]
    pids, ends = set(), []
    for snap in (f"snap.{phase}.before.json", f"snap.{phase}.after.json"):
        p = os.path.join(D, snap)
        if os.path.exists(p):
            here = {pr["pid"] for pr in json.load(open(p))["procs"]}
            pids |= here
            ends.append(here)
    th, wk = _phase_files(D, phase)
    segments, (t0, t1), extra = load_rows(th, pids)
    rows, _merged = merge_resumes(segments, load_all_wakeups(wk, pids | set(extra)))
    return rows, segments, pid_roles(D, phase), t0, t1, ends or [pids]


def read_wakes(D, spec):
    rows, _segments, roles, t0, t1, ends = _campaign_rows(D, spec)
    t_start = t0 + spec["read_from_s"]
    comms, reading = [], {"span_s": round(t1 - t0, 3), "read_from_s": spec["read_from_s"]}
    if spec["subject"] == "chrome-hidden":
        whole = set.intersection(*ends) if len(ends) == 2 else ends[0]
        kept = [r for r in rows if roles.get(r.pid, "main") == KEEP_ROLE]
        pages = page_renderers(D)
        if pages is not None:
            kept = [r for r in kept if r.pid in pages]
        kept = [r for r in kept if r.pid in whole]
        kept, control = drop_control_tab(kept, t1 - t0)
        renderers = sorted({r.pid for r in kept})
        streams = [wake_stream([r for r in kept if r.pid == p], t_start, t1, None, comms) for p in renderers]
        reading.update({"renderers": renderers, "control_tab": control})
    else:
        streams = [wake_stream(rows, t_start, t1, roles, comms)]
    return streams, comms, round((t1 - t_start) * 1e6), reading


def read_cycles(D, spec):
    rows, segments, roles, t0, t1, _ends = _campaign_rows(D, spec)
    stream = cycle_stream(spec["subject"], spec["phase"], rows, segments, roles, t0)
    reading = {"span_s": round(t1 - t0, 3), "cycles": len(stream),
               "rule": dict(zip(("comm", "rule", "value", "spacing_ms"), pool.CYCLES[(spec["subject"], spec["phase"])]))}
    return [stream], [pool.CYCLES[(spec["subject"], spec["phase"])][0]], round((t1 - t0) * 1e6), reading


def read_runs(D, spec):
    phase = spec["phase"]
    base = os.path.join(D, f"perf.{phase}")
    th, wk, fk, ts = base + ".timehist.txt.gz", base + ".wakeups.txt.gz", base + ".forks.txt.gz", os.path.join(D, f"taskstats.{phase}.tsv")
    for p in (th, fk, ts):
        if not os.path.exists(p):
            raise SystemExit(f"{D}: no {os.path.basename(p)}")
    report = json.load(open(os.path.join(D, "report.json"))) if os.path.exists(os.path.join(D, "report.json")) else {}
    meas_cpu = int(report.get("pin.load_cpu", 3))
    job = background.job_of(phase)
    segs = background.load_segments(th)
    forks, _exits = background.load_forks(fk)
    exec_rows = background.load_exec_rows(fk)
    execs = {pid: f for _t, pid, f in exec_rows}
    root, tree, tid2pid, last_comm, _out = background.phase_tree(job, segs, forks, meas_cpu,
                                                                 background.launched_root(job, exec_rows))
    ts_rows, _trailer = background.load_taskstats(ts)
    recs = background.process_records(ts_rows)
    pids = sorted({tid2pid.get(t, t) for t in tree})
    role = {pid: (recs[pid]["comm"] if pid in recs else last_comm.get(pid, "?")) for pid in pids}
    prog = {p for p in pids if background.is_program(job, execs.get(p), role.get(p))}
    rows = [s for s in segs if s.cpu == meas_cpu and s.tid in tree and tid2pid.get(s.tid, s.tid) in prog]
    stream = run_stream(rows)
    comms = sorted({s.comm for s in rows})
    span = (max(s.t_end for s in rows) - min(s.t_in for s in rows)) if rows else 0.0
    reading = {"meas_cpu": meas_cpu, "root": root, "processes": len(prog), "threads": len({s.tid for s in rows}),
               "cpu_s": round(sum(r for _, r, _ in stream) / 1e6, 3), "runs": len(stream), "span_s": round(span, 3)}
    return [stream], comms, round(span * 1e6), reading


READERS = {"wakes": read_wakes, "cycles": read_cycles, "runs": read_runs}


def document(entry, spec, streams, comms, phase_us, reading=None):
    return {"entry": entry, "program": spec.get("program"), "kind": spec["kind"], "subject": spec["subject"],
            "source": spec["source"], "release": spec["release"], "asset": spec["asset"], "landing": spec["landing"],
            "phase": spec["phase"], "read_from_s": spec["read_from_s"], "why": spec.get("why"),
            "reading": reading or {},
            "repeats": [{"repeat": spec["repeat"], "run_id": spec["run_id"], "phase_us": phase_us, "comms": comms,
                         "streams": streams}]}


def build(root, only=None):
    docs = {}
    for entry, spec in SOURCES.items():
        if only and entry not in only:
            continue
        D = os.path.join(root, spec["release"], spec["landing"])
        if not os.path.isdir(D):
            raise SystemExit(f"{entry}: no landing at {D} (unpack {spec['asset']} of release {spec['release']})")
        streams, comms, phase_us, reading = READERS[spec["kind"]](D, spec)
        docs[stream_name(entry, spec)] = document(entry, spec, streams, comms, phase_us, reading)
    return docs


def summary(doc):
    rep = doc["repeats"][0]
    n = sum(len(s) for s in rep["streams"])
    span = rep["phase_us"] / 1e6
    if doc["kind"] == "runs":
        return f"{n} runs, {doc['reading']['cpu_s']:.3f} s of CPU over {span:.1f} s"
    if doc["kind"] == "cycles":
        return f"{n} cycles over {span:.1f} s"
    cpu = sum(r for s in rep["streams"] for _, r, _ in s) / 1e6
    return f"{n} wakes in {len(rep['streams'])} stream(s) over {span:.1f} s, {n / span:.2f}/s, CPU share {cpu / span:.4f}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root")
    ap.add_argument("--only", default=None)
    ap.add_argument("--out", default=os.path.join(os.path.dirname(TOOLS), "replay"))
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    docs = build(a.root, set(a.only.split(",")) if a.only else None)
    differ = []
    os.makedirs(a.out, exist_ok=True)
    for name, doc in docs.items():
        path = os.path.join(a.out, f"{name}.json.gz")
        data = encode(doc)
        same = os.path.exists(path) and open(path, "rb").read() == data
        print(f"{name}: {summary(doc)}, {len(data)} bytes{'' if same else ' (differs)'}")
        if a.check:
            if not same:
                differ.append(name)
        else:
            open(path, "wb").write(data)
    if a.check and differ:
        raise SystemExit(f"differ from the landings: {', '.join(differ)}")


if __name__ == "__main__":
    main()
