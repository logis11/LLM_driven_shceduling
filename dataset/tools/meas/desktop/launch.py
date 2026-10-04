"""The launch subjects of the desktop family (9.10 changelog D132–D135; method
_dev/research/jioh/task-9.10-scenarios-timelines/campaign/launch/method.md).

    launch.py tree --root <pid> [--json <out>] [--check]
        the launched tree as it stands: every process in the root's session or below it by parent; --check prints the
        number of harness processes in it and lists them on stderr
    launch.py maps --root <pid> --out <file>
        the files the tree's processes map, one path a line
    launch.py warm <file> [--tsv <out>]
        each listed file read whole, then its cached fraction by fincore; prints report keys
    launch.py seed --pattern <s> --out <tsv>
        every thread of every process whose command line holds the pattern (the call's browser at the opening, D134)
    launch.py analyze <run-dir>
        the traced launch: the tree by the fork rows, its wakes, the event stream and the 10 s slice profile; writes
        launch.events.tsv.gz and launch.summary.json and prints report keys
    launch.py pool <run-dir>... [--json <out>] [--md <out>]
        the repeats side by side

The tree (D135) is the launched process and every descendant by the fork rows, which carry threads as well as
processes; for the call, Chrome's threads at the opening and their descendants. A segment is a wake by 9.6's rule
(`build.analyze.merge_resumes`). The phase runs from the application's exec (the call: the opening) to the settle's
end; each wake's time is taken from the phase's start.
"""

import argparse
import gzip
import json
import os
import re
import statistics
import subprocess
import sys
from collections import defaultdict

TOOLS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # dataset/tools
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)
from meas.build import analyze as _build   # noqa: E402  9.6's loaders and wake rule
from meas.desktop.analyze import NOT_PAGE_RENDERER   # noqa: E402  9.8's page-renderer rule (D127)

SLICE_S = 10.0
# the launch chain the job's own command runs before the application: taskset pins, setsid detaches, bash -c runs
LAUNCHER = {"taskset", "setsid", "bash", "sh"}
HARNESS = re.compile(r"desktop/run\.sh|Xvfb|openbox|synapse\.app|traffic\.py")
# session services an application starts and a desktop session keeps after it quits (the session bus, accessibility,
# settings, KDE's launcher daemons): `tree --app-only` leaves them out of "the tree exited" (D135)
SESSION = re.compile(r"^(dbus-daemon|dbus-launch|at-spi|gvfs|dconf-service|xdg-.*portal|gnome-keyring|kdeinit|klauncher|"
                     r"kded|kwalletd|kactivitymanage|kioslave|kioworker|file\.so|baloo_file|ksmserver)")
EXEC = re.compile(r"^\s*(\d+\.\d+):\s+sched:sched_process_exec:\s+filename=(.*?)\s+pid=(\d+)\s+old_pid=(\d+)")
SKIP_MAP = ("/dev/", "/memfd:", "/SYSV", "/proc/", "/sys/", "/run/user/")


# ---- the live tree ---------------------------------------------------------------------------------------------

def procs(proc="/proc"):
    """pid -> (ppid, sid, comm, argv) for every process readable now."""
    out = {}
    for d in os.listdir(proc):
        if not d.isdigit():
            continue
        try:
            stat = open(os.path.join(proc, d, "stat")).read()
            raw = open(os.path.join(proc, d, "cmdline"), "rb").read()
        except OSError:
            continue
        comm = stat[stat.index("(") + 1:stat.rindex(")")]
        f = stat[stat.rindex(")") + 2:].split()   # f[0] is field 3, the state
        # Chrome rewrites its children's titles into one space-joined string (9.10 dry run #72): split on both
        argv = raw.replace(b"\0", b" ").decode(errors="replace").split()
        out[int(d)] = (int(f[1]), int(f[3]), comm, argv)
    return out


def live_tree(root, table):
    """The root, every process in its session (launch_app starts it under setsid) and every descendant by parent."""
    kids = defaultdict(list)
    for pid, (ppid, _sid, _c, _a) in table.items():
        kids[ppid].append(pid)
    tree = {p for p, (_pp, sid, _c, _a) in table.items() if sid == root}
    if root in table:
        tree.add(root)
    stack = sorted(tree)
    while stack:
        for c in kids.get(stack.pop(), ()):
            if c not in tree:
                tree.add(c)
                stack.append(c)
    return sorted(tree)


def role_of(argv, comm):
    typ = next((a.split("=", 1)[1] for a in argv if a.startswith("--type=")), None)
    if typ == "renderer":
        return "renderer-own" if any(f in argv for f in NOT_PAGE_RENDERER) else "renderer"
    return typ or comm


def mapped_files(pids, proc="/proc"):
    files = set()
    for p in pids:
        try:
            lines = open(os.path.join(proc, str(p), "maps")).read().splitlines()
        except OSError:
            continue
        for line in lines:
            parts = line.split(None, 5)
            if len(parts) < 6 or parts[4] == "0":
                continue
            path = parts[5]
            if not path.startswith("/") or path.endswith("(deleted)") or path.startswith(SKIP_MAP):
                continue
            files.add(path)
    return sorted(files)


PAGE = 4096


def warm(paths, chunk=200):
    """Read each file whole, then fincore it: (rows of (path, resident pages, pages the file spans), unreadable count).
    Residency is counted in whole pages, so the fraction is pages over the pages the files span (the background
    family's `cached`)."""
    bad = 0
    for p in paths:
        try:
            with open(p, "rb") as handle:
                while handle.read(1 << 20):
                    pass
        except OSError:
            bad += 1
    rows = []
    for i in range(0, len(paths), chunk):
        part = paths[i:i + chunk]
        res = subprocess.run(["fincore", "--bytes", "--noheadings", "--raw", "--output", "PAGES,SIZE,FILE", *part],
                             capture_output=True, text=True)
        for line in res.stdout.splitlines():
            f = line.split(None, 2)
            if len(f) == 3 and f[0].isdigit() and f[1].isdigit():
                rows.append((f[2], int(f[0]), -(-int(f[1]) // PAGE)))
    return rows, bad


def seed(pattern, table):
    """(pid, tid, comm) of every thread of every process whose command line holds the pattern."""
    me = os.getpid()
    out = []
    for pid, (_pp, _sid, _c, argv) in sorted(table.items()):
        if pid == me or not any(pattern in a for a in argv):
            continue
        try:
            tids = sorted(int(t) for t in os.listdir(f"/proc/{pid}/task"))
        except OSError:
            continue
        for t in tids:
            try:
                comm = open(f"/proc/{pid}/task/{t}/comm").read().strip()
            except OSError:
                comm = ""
            out.append((pid, t, comm))
    return out


# ---- the traced launch -----------------------------------------------------------------------------------------

def read_kv(D):
    p = os.path.join(D, "report.json")
    if os.path.exists(p):
        return json.load(open(p))
    kv = {}
    p = os.path.join(D, "report.kv")
    if os.path.exists(p):
        for line in open(p):
            k, _, v = line.rstrip("\n").partition("=")
            kv[k] = v
    return kv


def read_edges(D):
    """(label, edge) -> monotonic seconds, from launch-edges.jsonl (perf's clock, -k CLOCK_MONOTONIC)."""
    out = {}
    p = os.path.join(D, "launch-edges.jsonl")
    if os.path.exists(p):
        for line in open(p):
            try:
                e = json.loads(line)
            except ValueError:
                continue
            out[(e["phase"], e["edge"])] = e["mono_ns"] / 1e9
    return out


def exec_rows(path):
    out = []
    with _build.open_text(path) as handle:
        for line in handle:
            m = EXEC.match(line)
            if m:
                out.append((float(m.group(1)), int(m.group(3)), m.group(2)))
    out.sort()
    return out


def descendants(roots, forks):
    children = defaultdict(list)
    for _t, p, _pc, c, _cc in forks:
        children[p].append(c)
    tree, stack = set(), list(roots)
    while stack:
        t = stack.pop()
        if t not in tree:
            tree.add(t)
            stack.extend(children.get(t, ()))
    return tree


def app_exec(execs, tree):
    """The application's exec: the first exec in the tree past the launch chain (taskset, setsid, bash)."""
    return next(((t, pid, f) for t, pid, f in execs if pid in tree and os.path.basename(f) not in LAUNCHER), None)


def slice_profile(wakes, t0, span_s, slice_s=SLICE_S):
    n = max(1, int(-(-span_s // slice_s)))
    cpu, n_w = [0.0] * n, [0] * n
    for r in wakes:
        i = int((r.t_in - t0) // slice_s)
        if 0 <= i < n:
            cpu[i] += r.run
            n_w[i] += 1
    last = span_s - (n - 1) * slice_s   # the last slice may be short
    width = [slice_s] * (n - 1) + [max(last, 1e-6)]
    return {"slice_s": slice_s,
            "cpu_ms_per_s": [round(c / w, 3) for c, w in zip(cpu, width)],
            "wakes_per_s": [round(k / w, 2) for k, w in zip(n_w, width)]}


def page_renderers(D, label="traced"):
    """pids of the page renderers at the settle's end (D127), from launch.renderers.<label>.tsv."""
    p = os.path.join(D, f"launch.renderers.{label}.tsv")
    if not os.path.exists(p):
        return None
    out = set()
    for line in open(p):
        parts = line.rstrip("\n").split("\t", 1)
        if len(parts) == 2 and "--type=renderer" in parts[1] and not any(f in parts[1] for f in NOT_PAGE_RENDERER):
            out.add(int(parts[0]))
    return out


def analyze(D):
    kv, edges = read_kv(D), read_edges(D)
    subject = kv.get("app", "")
    base = os.path.join(D, "perf.launch")
    segs = _build.load_segments(base + ".timehist.txt.gz")
    wakeups = _build.load_wakeups(base + ".wakeups.txt.gz")
    forks, exits = _build.load_forks(base + ".forks.txt.gz")
    execs = exec_rows(base + ".forks.txt.gz")
    meas_cpu = int(kv.get("pin.load_cpu", "-1"))
    out = {"subject": subject, "repeat": kv.get("repeat"), "mode": kv.get("mode"), "version": kv.get("version")}
    t1 = edges.get(("traced.settle", "end"))
    if subject == "launch-webrtc":   # D134: the call opened in the running browser
        roots, start = set(), edges.get(("traced.call", "open"))
        p = os.path.join(D, "launch.seed.tsv")
        if os.path.exists(p):
            for line in open(p):
                f = line.rstrip("\n").split("\t")
                if len(f) >= 2 and f[1].isdigit():
                    roots.add(int(f[1]))
        tree = descendants(roots, forks)
        t0 = start
        out["start"] = "the call's opening"
    else:
        root = int(kv.get("launch.traced.root", "0") or 0)
        tree = descendants({root}, forks)
        ex = app_exec(execs, tree)
        t0 = ex[0] if ex else edges.get(("traced.exec", "mark"))
        out["start"] = f"exec of {ex[2]}" if ex else "the job's exec edge"
        out["root"] = root
    if t0 is None or t1 is None or t1 <= t0:
        out["error"] = "no phase: a missing start or settle edge"
        return out, []
    span = t1 - t0
    rows = [s for s in segs if s.tid in tree and t0 <= s.t_in < t1]
    wakes, merged = _build.merge_resumes(rows, wakeups)
    # role per process: the settle's tree listing where it holds the pid, else the last executed file, else comm
    roles, listed = {}, os.path.join(D, "launch.tree.traced.json")
    if os.path.exists(listed):
        for p in json.load(open(listed)):
            roles[p["pid"]] = role_of(p["argv"], p["comm"])
    last_exec = {}
    for _t, pid, f in execs:
        last_exec[pid] = os.path.basename(f)
    tid2pid = {s.tid: s.pid for s in rows}

    def role(r):
        return roles.get(r.pid) or last_exec.get(r.pid) or r.comm
    streams = {"tree": wakes}
    if subject == "launch-chrome-hidden":   # D127: each tab's page renderer but the control tab's is one stream
        # the tabs' renderers are the page renderers at the gate; one started later hosts no tab (dry run #80)
        gate = page_renderers(D, "traced.gate")
        end = page_renderers(D) or set()
        pages = gate if gate is not None else end
        out["late_renderers"] = sorted(end - pages)
        by_pid = defaultdict(list)
        for r in wakes:
            if r.pid in pages:
                by_pid[r.pid].append(r)
        if by_pid:
            control = max(by_pid, key=lambda p: len(by_pid[p]))
            ranked = sorted((len(v) for v in by_pid.values()), reverse=True)
            out["control_tab"] = {"pid": control, "wakes_per_s": round(ranked[0] / span, 3),
                                  "next_wakes_per_s": round(ranked[1] / span, 3) if len(ranked) > 1 else None}
            for k, p in enumerate(sorted(q for q in by_pid if q != control)):
                streams[f"renderer{k + 1}"] = by_pid[p]
        out["page_renderers"] = len(pages)
    on_cpu = [s for s in segs if s.cpu == meas_cpu and t0 <= s.t_in < t1]
    outside = defaultdict(lambda: [0, 0.0])
    for s in on_cpu:
        if s.tid not in tree:
            outside[s.comm][0] += 1
            outside[s.comm][1] += s.run
    per_role = defaultdict(lambda: [0, 0.0])
    for r in wakes:
        per_role[role(r)][0] += 1
        per_role[role(r)][1] += r.run
    out.update({
        "phase_s": round(span, 3), "tree_tids": len(tree), "segments": len(rows), "resumes_merged": merged,
        "wakes": len(wakes), "cpu_ms": round(sum(r.run for r in wakes), 3),
        "rows_off_measured_cpu": sum(1 for s in rows if s.cpu != meas_cpu),
        "exits_in_phase": sum(1 for t, (te, _c) in exits.items() if t in tree and t0 <= te < t1),
        "roles": {k: {"wakes": v[0], "cpu_ms": round(v[1], 3)} for k, v in sorted(per_role.items(), key=lambda kv: -kv[1][1])},
        "outside": {k: {"rows": v[0], "run_ms": round(v[1], 3)} for k, v in sorted(outside.items(), key=lambda kv: -kv[1][1])[:12]},
        "streams": {name: {"wakes": len(ws), "cpu_ms": round(sum(r.run for r in ws), 3),
                           "slices": slice_profile(ws, t0, span)} for name, ws in streams.items()},
    })
    events = []
    for name, ws in streams.items():
        for r in ws:
            events.append((name, round((r.t_in - t0) * 1e6), round(r.run * 1000), r.tid, tid2pid.get(r.tid, r.pid), r.comm, role(r)))
    events.sort(key=lambda e: (e[0], e[1]))
    return out, events


def write(D, out, events):
    json.dump(out, open(os.path.join(D, "launch.summary.json"), "w"), indent=1, sort_keys=True)
    with gzip.open(os.path.join(D, "launch.events.tsv.gz"), "wt") as handle:
        handle.write("stream\tt_us\trun_us\ttid\tpid\tcomm\trole\n")
        for e in events:
            handle.write("\t".join(str(x) for x in e) + "\n")


def keys(out):
    """The report keys run.sh appends to report.kv."""
    if "error" in out:
        return [f"launch.analysis={out['error']}"]
    tree = out["streams"]["tree"]
    lines = [f"launch.phase_s={out['phase_s']}", f"launch.start={out['start']}", f"launch.wakes={out['wakes']}",
             f"launch.cpu_ms={out['cpu_ms']}", f"launch.tree_tids={out['tree_tids']}",
             f"launch.rows_off_measured_cpu={out['rows_off_measured_cpu']}",
             f"launch.slices.cpu_ms_per_s={' '.join(str(x) for x in tree['slices']['cpu_ms_per_s'])}"]
    if "page_renderers" in out:
        lines.append(f"launch.page_renderers={out['page_renderers']}")
        lines.append(f"launch.renderer_streams={sum(1 for k in out['streams'] if k.startswith('renderer'))}")
    return lines


# ---- the repeats -----------------------------------------------------------------------------------------------

def pool(dirs):
    reps = []
    for D in dirs:
        p = os.path.join(D, "launch.summary.json")
        if not os.path.exists(p):
            continue
        s = json.load(open(p))
        if "error" in s:
            continue
        reps.append(s)
    reps.sort(key=lambda s: int(s.get("repeat") or 0))
    by = defaultdict(list)
    for s in reps:
        by[s["subject"]].append(s)
    out = {}
    for subject, rs in sorted(by.items()):
        n = min(len(r["streams"]["tree"]["slices"]["cpu_ms_per_s"]) for r in rs)
        cols = [[r["streams"]["tree"]["slices"]["cpu_ms_per_s"][i] for r in rs] for i in range(n)]
        out[subject] = {
            "repeats": [r.get("repeat") for r in rs],
            "versions": sorted({r.get("version") or "" for r in rs}),
            "phase_s": [r["phase_s"] for r in rs],
            "cpu_ms": [r["cpu_ms"] for r in rs],
            "wakes": [r["wakes"] for r in rs],
            "slice_cpu_ms_per_s_mean": [round(statistics.fmean(c), 3) for c in cols],
            "slice_cpu_ms_per_s": [r["streams"]["tree"]["slices"]["cpu_ms_per_s"] for r in rs],
        }
    return out


def pool_reps(reps):
    """pool.py's form: the repeats of one subject keyed by index (`find_runs`), with each repeat's run id."""
    dirs = {str(k): info["dir"] for k, info in reps.items()}
    out = pool(list(dirs.values()))
    e = next(iter(out.values()), {"repeats": []})
    e["run_ids"] = {k: str((info["spec"].get("github_run") or {}).get("GITHUB_RUN_ID") or "") for k, info in reps.items()}
    e["mode"] = sorted({info["mode"] for info in reps.values()})
    return e


def render_subject(subject, e):
    return render({subject: e})[2:]


def render(out):
    L = ["# 9.10 launch campaign — pooled results", ""]
    for subject, e in out.items():
        L += [f"## {subject}", "", f"Repeats: {e['repeats']}  ·  versions {e['versions']}", "",
              "| repeat | phase s | CPU ms | wakes |", "|---|---|---|---|"]
        L += [f"| {k} | {p} | {c} | {w} |" for k, p, c, w in zip(e["repeats"], e["phase_s"], e["cpu_ms"], e["wakes"])]
        L += ["", "CPU ms/s per 10 s slice, mean over the repeats:", "",
              " ".join(str(x) for x in e["slice_cpu_ms_per_s_mean"]), ""]
    return L


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("tree"); t.add_argument("--root", type=int, required=True); t.add_argument("--json"); t.add_argument("--check", action="store_true")
    t.add_argument("--app-only", action="store_true", help="leave out the session services (SESSION)")
    m = sub.add_parser("maps"); m.add_argument("--root", type=int, required=True); m.add_argument("--out", required=True)
    w = sub.add_parser("warm"); w.add_argument("file"); w.add_argument("--tsv")
    s = sub.add_parser("seed"); s.add_argument("--pattern", required=True); s.add_argument("--out", required=True)
    a = sub.add_parser("analyze"); a.add_argument("run_dir")
    p = sub.add_parser("pool"); p.add_argument("dirs", nargs="+"); p.add_argument("--json"); p.add_argument("--md")
    args = ap.parse_args()
    if args.cmd == "tree":
        table = procs()
        pids = live_tree(args.root, table)
        if args.app_only:
            pids = [q for q in pids if not SESSION.match(table[q][2])]
        if args.json:
            json.dump([{"pid": q, "ppid": table[q][0], "sid": table[q][1], "comm": table[q][2], "argv": table[q][3]} for q in pids],
                      open(args.json, "w"), indent=1)
        if args.check:
            bad = [" ".join(table[q][3])[:80] for q in pids if HARNESS.search(" ".join(table[q][3]))]
            print(len(bad))
            print("\n".join(bad), file=sys.stderr)
        else:
            print(" ".join(str(q) for q in pids))
    elif args.cmd == "maps":
        files = mapped_files(live_tree(args.root, procs()))
        open(args.out, "w").write("".join(f + "\n" for f in files))
        print(len(files))
    elif args.cmd == "warm":
        paths = [ln.strip() for ln in open(args.file) if ln.strip()]
        try:
            rows, bad = warm(paths)
        except FileNotFoundError as e:   # no fincore: recorded, and the job's validity then fails on the fraction
            print(f"cache.launch.error={e}")
            return
        res, span = sum(r[1] for r in rows), sum(r[2] for r in rows)
        if args.tsv:
            open(args.tsv, "w").write("".join(f"{p}\t{r}\t{z}\n" for p, r, z in rows))
        print(f"cache.launch.files={len(paths)}")
        print(f"cache.launch.measured={len(rows)}")
        print(f"cache.launch.unreadable={bad}")
        print(f"cache.launch.pages={span}")
        print(f"cache.launch.fraction={res / span:.4f}" if span else "cache.launch.fraction=")
    elif args.cmd == "seed":
        rows = seed(args.pattern, procs())
        open(args.out, "w").write("".join(f"{p}\t{t}\t{c}\n" for p, t, c in rows))
        print(len(rows))
    elif args.cmd == "analyze":
        out, events = analyze(args.run_dir)
        write(args.run_dir, out, events)
        print("\n".join(keys(out)))
    elif args.cmd == "pool":
        out = pool(args.dirs)
        if args.json:
            json.dump(out, open(args.json, "w"), indent=1)
        text = "\n".join(render(out))
        if args.md:
            open(args.md, "w").write(text + "\n")
        print(text)


if __name__ == "__main__":
    main()
