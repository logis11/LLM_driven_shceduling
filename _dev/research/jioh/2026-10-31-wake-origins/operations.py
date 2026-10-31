"""operations.py REPO OUT.md RUN_DIR... — each measured operation's largest run (timer wakes by origin, decision 17):
in every successful operation of the op phase (ops.jsonl's [trigger, done) windows), the largest run of the
application's tree — analyze.py's wakes and its `operation_windows` — with its share of the operation's CPU, its
schedule-in from the trigger and the channel its wake's origin gives; per application, over the operations, and the
stability rule (stability.py) on the per-repeat means of its length and of its schedule-in."""
import collections, importlib.util, json, os, statistics, sys
repo, out_path, dirs = sys.argv[1], sys.argv[2], sys.argv[3:]
spec = importlib.util.spec_from_file_location("analyze", os.path.join(repo, "dataset/tools/meas/campaign/analyze.py"))
A = importlib.util.module_from_spec(spec); spec.loader.exec_module(A)
sys.path.insert(0, os.path.join(repo, "dataset/tools/meas"))
from stability import stability  # noqa: E402

per_app = collections.defaultdict(list)            # app -> [(repeat dir, op CPU, largest run, offset, channel)]
for D in dirs:
    report = json.load(open(os.path.join(D, "report.json")))
    th, wk = os.path.join(D, "perf.op.timehist.txt.gz"), os.path.join(D, "perf.op.wakeups.txt.gz")
    pids = set()
    for snap in ("snap.op.before.json", "snap.op.after.json"):
        p = os.path.join(D, snap)
        if os.path.exists(p): pids |= {pr["pid"] for pr in json.load(open(p))["procs"]}
    segs, (t0, t1), extra = A.load_rows(th, pids, report.get("rx"))
    tree = pids | set(extra)
    by_state = report.get("app") in A.STATE_WAKE_APPS and any(r.state for r in segs)
    rows, _ = A.merge_resumes(segs, A.load_all_wakeups(wk, tree), None, by_state)
    rows = A.with_origins(rows, A.load_origins(wk, tree))
    ops = [json.loads(l) for l in open(os.path.join(D, "ops.jsonl")) if l.strip()]
    ow = A.operation_windows(rows, ops)
    cpu = collections.Counter()
    for r in ow["inside"]:
        k = max(i for i, (a, _) in enumerate(ow["windows"]) if a <= r.t_in)
        cpu[k] += r.run
    starts = [a for a, _ in ow["windows"]]
    for r, off in zip(ow["largest"], ow["largest_offsets_ms"]):
        k = max(i for i, a in enumerate(starts) if a <= r.t_in)
        per_app[report.get("app")].append((D, cpu[k], r.run, off, A.wake_channel(r)))

def pct(v, q):
    v = sorted(v); return v[min(len(v) - 1, int(q * len(v)))]

lines = ["| application, operation | repeats | operations | operation CPU p50 (ms) | largest run p50 (ms) | its share of the "
         "operation's CPU, min / p50 | from the trigger p50 / p90 (ms) | channel (timer / event) | largest run mean, "
         "half-width over the repeats | from the trigger mean, half-width |", "|---|---|---|---|---|---|---|---|---|---|"]
names = {"gimp": "unsharp mask", "thunderbird-send": "send", "chrome": "page load", "kdenlive": "preview render"}
for app in sorted(per_app):
    xs = per_app[app]
    reps = collections.defaultdict(list)
    for x in xs: reps[x[0]].append(x)
    run_st = stability([statistics.fmean(x[2] for x in v) for v in reps.values()], 0.001, 5)
    off_st = stability([statistics.fmean(x[3] for x in v) for v in reps.values()], 0.001, 5)
    share = [x[2] / x[1] for x in xs]
    ch = collections.Counter(x[4] for x in xs)
    lines.append(f"| {app}, {names.get(app, '')} | {len(reps)} | {len(xs)} | {pct([x[1] for x in xs], .5):.1f} | "
                 f"{pct([x[2] for x in xs], .5):.1f} | {min(share):.3f} / {pct(share, .5):.3f} | "
                 f"{pct([x[3] for x in xs], .5):.1f} / {pct([x[3] for x in xs], .9):.1f} | {ch['timer']} / {ch['event']} | "
                 f"{run_st['mean']:.1f} ms ±{run_st['half_width']:.2%} | {off_st['mean']:.1f} ms ±{off_st['half_width']:.2%} |")
open(out_path, "w").write("\n".join(lines) + "\n")
