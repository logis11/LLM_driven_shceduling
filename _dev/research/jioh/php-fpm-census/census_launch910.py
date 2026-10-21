#!/usr/bin/env python3
"""9.10's launch phases (`meas-ci:desktop:2026-10-04b`; `video-editor`'s re-trace `meas-ci:desktop:2026-10-05`;
`renderer-hidden`'s re-trace `meas-ci:desktop:2026-10-05b`): each pooled landing's streams read as
`meas/desktop/launch.py analyze` reads them — the tree by the fork rows from the launched root (the call: Chrome's
threads at the opening), the phase from the application's exec (the call: its opening) to the settle's end, a segment
a wake by 9.6's rule (`build.analyze.merge_resumes`) — and every wake traced by chain_roots (census_core's rules).

  python3 -I census_launch910.py <rel dir> <dataset/launch dir> <out.json>

Each landing is the one the committed stream file names (repeat and run id); its streams are checked wake by wake
against that file. A process born in the phase (fork rows) and started by the harness is the launch's own when it is
the tree's first row (census_core); `xdotool`, the drivers' keystrokes and clicks after the window, is the phase's
`stimulus`, and for the call so is the `chrome` the harness runs to open the call page in the running browser (with
its crash handler), which hands the address over and exits (9.10 D134). Scripted peers by their pid files
(tally910). The streams are the whole tree's, or `renderer-hidden`'s one per measured renderer (launch.py's
selection, the control tab dropped).

Beside the reading as the phase has it, a context reading (`context`): the same phase wakes traced on the tree's
wakes from the trace's start (2 s before the exec), so that the phase's first wake of a thread that was already
running at the exec continues the wake it resumes, and a wake that follows a block in D before the exec continues the
wake before it — census_core's rules, with the predecessors the phase's start cuts off.
"""

import glob
import gzip
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import census_core as cc  # noqa: E402
import chain_roots as cr  # noqa: E402
import tally910 as t9  # noqa: E402
from meas.build import analyze as _build  # noqa: E402
from meas.desktop import launch  # noqa: E402

SUBJECTS = (("soffice", "office-writer", "meas-ci:desktop:2026-10-04b", "meas-ci-desktop-2026-10-04b"),
            ("thunderbird-send", "mail-client", "meas-ci:desktop:2026-10-04b", "meas-ci-desktop-2026-10-04b"),
            ("chrome", "web-browser", "meas-ci:desktop:2026-10-04b", "meas-ci-desktop-2026-10-04b"),
            ("mpv-video", "video-player", "meas-ci:desktop:2026-10-04b", "meas-ci-desktop-2026-10-04b"),
            ("mpv-audio", "audio-player", "meas-ci:desktop:2026-10-04b", "meas-ci-desktop-2026-10-04b"),
            ("webrtc", "video-call", "meas-ci:desktop:2026-10-04b", "meas-ci-desktop-2026-10-04b"),
            ("element", "chat-client", "meas-ci:desktop:2026-10-04b", "meas-ci-desktop-2026-10-04b"),
            ("steam", "game-client", "meas-ci:desktop:2026-10-04b", "meas-ci-desktop-2026-10-04b"),
            ("kdenlive", "video-editor", "meas-ci:desktop:2026-10-05", "meas-ci-desktop-2026-10-05"),
            ("chrome-hidden", "renderer-hidden", "meas-ci:desktop:2026-10-05b", "meas-ci-desktop-2026-10-05b"))
DRIVERS = {"webrtc": ("xdotool", "chrome", "chrome_crashpad")}


def landing(rel, release, subject, k, run_id):
    pat = re.compile(rf"^meas-desktop-launch-{re.escape(subject)}-r{k}-full(-\d+)?$")
    for d in glob.glob(os.path.join(rel, release, "x", "**", "meas-desktop-launch-*"), recursive=True):
        if not pat.match(os.path.basename(d)) or not os.path.exists(os.path.join(d, "report.json")):
            continue
        spec = json.load(open(os.path.join(d, "spec.json")))
        if str((spec.get("github_run") or {}).get("GITHUB_RUN_ID")) == run_id:
            return d
    return None


def phase(D):
    """launch.analyze's tree, phase and wakes, and its streams' pids (renderer-hidden)."""
    kv, edges = launch.read_kv(D), launch.read_edges(D)
    subject = kv.get("app", "")
    base = os.path.join(D, "perf.launch")
    segs = _build.load_segments(base + ".timehist.txt.gz")
    wakeups = _build.load_wakeups(base + ".wakeups.txt.gz")
    forks, _exits = _build.load_forks(base + ".forks.txt.gz")
    execs = launch.exec_rows(base + ".forks.txt.gz")
    t1 = edges.get(("traced.settle", "end"))
    if subject == "launch-webrtc":
        roots = set()
        for line in open(os.path.join(D, "launch.seed.tsv")):
            f = line.rstrip("\n").split("\t")
            if len(f) >= 2 and f[1].isdigit():
                roots.add(int(f[1]))
        tree = launch.descendants(roots, forks)
        t0 = edges.get(("traced.call", "open"))
    else:
        tree = launch.descendants({int(kv.get("launch.traced.root", "0") or 0)}, forks)
        ex = launch.app_exec(execs, tree)
        t0 = ex[0] if ex else edges.get(("traced.exec", "mark"))
    rows = [s for s in segs if s.tid in tree and t0 <= s.t_in < t1]
    wakes, _merged = _build.merge_resumes(rows, wakeups)
    # the context reading: the tree's wakes from the trace's start, so a phase wake whose run began before the exec
    # (a resume the phase's start cut from its wake) and a wake after a block in D before the exec read their
    # predecessors
    context, _m = _build.merge_resumes([s for s in segs if s.tid in tree and s.t_in < t1], wakeups)
    pids = {s.pid for s in segs if s.tid in tree} | set(tree)
    stream_of_pid = None
    if subject == "launch-chrome-hidden":
        _out, events = launch.analyze(D)
        stream_of_pid = {e[4]: e[0] for e in events if e[0] != "tree"}
    born = {c for _t, _p, _pc, c, _cc in forks}
    return t0, t1, wakes, pids, born, stream_of_pid, context


def context_reading(wakeup_rows, pids, born, drivers, servers, context, kept):
    """Each phase wake's cause read on the context wakes: the context wake it is (same thread and start), or the one
    it resumes. Returns {class: {n, run}} and the outside-cause labels."""
    import bisect
    tr = t9.PeerTracer(wakeup_rows, pids, cc.by_tid(context), born=born, drivers=drivers, servers=servers)
    out, labels = {}, {}
    for w in kept:
        i = bisect.bisect_right(tr.starts.get(w.tid, []), w.t_in + cc.EPS) - 1
        cls, lab = ("unknown", "not a traced wake") if i < 0 else tr.r_wake(w.tid, i)[:2]
        x = out.setdefault(cls, {"n": 0, "run": 0.0})
        x["n"] += 1
        x["run"] += w.run
        if cls == "outside":
            labels[lab] = labels.get(lab, 0) + 1
    return out, labels


def main():
    rel, lib, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    result = {}
    for subject, entry, tag, release in SUBJECTS:
        doc = json.load(gzip.open(os.path.join(lib, f"launch-{entry}.json.gz")))
        sec = result.setdefault(f"launch {entry}", {"campaign": tag, "phase": "launch", "kind": "launch",
                                                    "subject": subject, "repeats": {}, "runs": {}, "check": {},
                                                    "stream_check": {}, "phase_s": {}, "first10": {}})
        for rep in doc["repeats"]:
            k, run_id = rep["repeat"], rep["run_id"]
            D = landing(rel, release, subject, k, run_id)
            t0, t1, wakes, pids, born, stream_of_pid, context = phase(D)
            wrows = cc.load_wakeup_rows(os.path.join(D, "perf.launch.wakeups.txt.gz"))
            drivers, servers = DRIVERS.get(subject, ("xdotool",)), t9.servers_of(D)
            tr = t9.PeerTracer(wrows, pids, cc.by_tid(wakes), born=born, drivers=drivers, servers=servers)
            if stream_of_pid is None:
                name_of = lambda r: "tree"
                kept = wakes
            else:
                name_of = lambda r: stream_of_pid[r.pid]
                kept = [w for w in wakes if w.pid in stream_of_pid]
            # the check: each stream, wake by wake, against the committed file
            mine = {}
            for w in kept:
                mine.setdefault(name_of(w), []).append([round((w.t_in - t0) * 1e6), round(w.run * 1000)])
            names = ["tree"] if stream_of_pid is None else sorted(set(stream_of_pid.values()),
                                                                 key=lambda s: int(s[len("renderer"):]))
            same = all(sorted(mine.get(n, [])) == sorted([x[0], x[1]] for x in s)
                       for n, s in zip(names, rep["streams"])) and len(names) == len(rep["streams"])
            sec["stream_check"][k] = {"same": same, "wakes": len(kept),
                                      "committed_wakes": sum(len(s) for s in rep["streams"]),
                                      "phase_us": round((t1 - t0) * 1e6), "committed_phase_us": rep["phase_us"]}
            traced = tr.trace(kept)
            span = t1 - t0
            sec["repeats"][k] = t9.tally(traced, name_of, lambda _n: span)
            sec["runs"][k] = cr.runs(traced, 5)
            sec["phase_s"][k] = span
            # the first 10 s slice: the stream's CPU there and the outside-cause wakes' run there
            f10 = [x for x in traced if x[0].t_in - t0 < 10.0]
            sec["first10"][k] = {"cpu_ms": sum(x[0].run for x in f10),
                                 "outside_ms": sum(x[0].run for x in f10 if x[1] == "outside"),
                                 "direct_ms": sum(x[0].run for x in f10 if x[1] == "outside" and x[6])}
            ctx, ctx_labels = context_reading(wrows, pids, born, drivers, servers, context, kept)
            sec.setdefault("context", {})[k] = {"classes": ctx, "outside_labels": ctx_labels}
            if not sec["check"]:
                sec["check"][k] = cr.check(tr, kept)
            o = sum(c["classes"].get("outside", {}).get("n", 0) for c in sec["repeats"][k].values())
            print(f"launch {entry} r{k}: {len(kept)} wakes, outside {o}, stream as committed {same}", flush=True)
    json.dump(result, open(out_path, "w"), indent=1)


if __name__ == "__main__":
    main()
