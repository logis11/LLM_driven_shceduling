"""table.py OUT — per file and top slice, the share of a task's 100 ms boost intervals
(those wholly inside its life) holding at least one demotion of it (`x_mlfq_demote`),
the intervals read off the `x_mlfq_boost` lines."""
import collections, json, sys

BOOST_US = 100000
SLICES = (500, 700, 900, 1200, 1500, 2000, 3000, 5000, 7000, 9000, 10000, 12000, 14000,
          20000, 30000, 40000, 100000)


def shares(trace, prefixes):
    boosts = [0]; hit = collections.defaultdict(set); life = {}
    for line in open(trace):
        d = json.loads(line); ev = d.get("event")
        if ev is None:
            continue
        task = d.get("task", "")
        if ev == "x_mlfq_boost":
            boosts.append(d["t"])
        elif ev == "x_mlfq_demote" and task.startswith(prefixes):
            hit[task].add(len(boosts) - 1)
        elif ev in ("task_arrive", "task_end") and task.startswith(prefixes):
            life.setdefault(task, [None, None])[0 if ev == "task_arrive" else 1] = d["t"]
    out = {}
    for task, (a, e) in life.items():
        e = e if e is not None else boosts[-1] + BOOST_US
        idx = [i for i, b in enumerate(boosts) if b >= a and b + BOOST_US <= e]
        out[task] = sum(1 for i in idx if i in hit[task]) / len(idx) if idx else 0
    return out


def main(out):
    print("| top slice µs | call | video player | music | c1-gaming stages ≥ 0.5 / > 0 | c2-p2a stages ≥ 0.5 / > 0 |")
    print("|---|---|---|---|---|---|")
    for sl in SLICES:
        m = shares(f"{out}/c1-meeting.{sl}.jsonl", ("voice",))
        md = shares(f"{out}/c1-media.{sl}.jsonl", ("video", "music"))
        g = shares(f"{out}/c1-gaming.{sl}.jsonl", ("game.",))
        c = shares(f"{out}/c2-p2a.{sl}.jsonl", ("game.",))
        stages = lambda s: f"{sum(v >= 0.5 for v in s.values())} / {sum(v > 0 for v in s.values())} of {len(s)}"
        print(f"| {sl} | {m.get('voice', 0):.2f} | {md.get('video', 0):.2f} | {md.get('music', 0):.2f} | {stages(g)} | {stages(c)} |")


if __name__ == "__main__":
    main(sys.argv[1])
