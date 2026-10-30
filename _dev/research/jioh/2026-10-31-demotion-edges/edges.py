"""edges.py OUT — each task's CPU per 100 ms boost interval, read off the 100 000 µs
run's trace (no task is demoted there, so the CPU an interval holds is the task's own):
the run segments summed per interval, over the intervals wholly inside the task's life.
Under the allotment kept across bursts a task is demoted in an interval whose CPU at
the top level reaches the slice, so the median is the slice demoting it in half."""
import collections, json, statistics, sys

BOOST_US = 100000
FILES = {"c1-meeting": ("voice",), "c1-media": ("video", "music"),
         "c1-gaming": ("game.",), "c2-p2a": ("game.",)}


def cpu_per_interval(trace, prefixes):
    start = {}; life = {}; cpu = collections.defaultdict(collections.Counter)
    for line in open(trace):
        d = json.loads(line); ev = d.get("event"); task = d.get("task", "")
        if ev is None or not task.startswith(prefixes):
            continue
        t = d["t"]
        if ev == "run_start":
            start[task] = t
        elif ev == "run_end":
            a = start.pop(task)
            while a < t:
                k = a // BOOST_US; b = min(t, (k + 1) * BOOST_US)
                cpu[task][k] += b - a; a = b
        elif ev in ("task_arrive", "task_end"):
            life.setdefault(task, [None, None])[0 if ev == "task_arrive" else 1] = t
    out = {}
    for task, (a, e) in life.items():
        ks = range(-(-a // BOOST_US), (e if e is not None else 0) // BOOST_US)
        out[task] = [cpu[task][k] for k in ks]
    return out


def main(out):
    print("| file | task | intervals | mean CPU µs | median CPU µs |")
    print("|---|---|---|---|---|")
    for f, prefixes in FILES.items():
        for task, xs in sorted(cpu_per_interval(f"{out}/{f}.100000.jsonl", prefixes).items()):
            print(f"| {f} | {task} | {len(xs)} | {statistics.mean(xs):.0f} | {statistics.median(xs):.0f} |")


if __name__ == "__main__":
    main(sys.argv[1])
