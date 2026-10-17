#!/usr/bin/env python3
"""By when a file's batch job ends on one lane under every work-conserving policy (9.10 D78's arithmetic).

The job's arrival a, plus its CPU C (its RUNs) and its blocks S (its SLEEPs), plus the other tasks' CPU released
after a, as compiled under the file's seed: a + C + S + O, a bound while the other tasks hold no backlog at a (B = 0).
The changelogs' "ends by … under every policy" and the smallest whole second a segment takes from it are this report.
A task beside the job releases each RUN at the wake its WAIT consumes (the k-th WAIT on a channel, the k-th wake on
it); the job's end is also bounded by the least E with E = a + C + S + B + (that CPU released in [a, E]), B the
other tasks' backlog at a (9.10 D162).

end_bound.py <artifact.workload.json> <job id> [segment end s]   (from dataset/)
"""

import bisect
import json
import sys


def releases(task, wakes):
    """[(t_us, run_us)] for a task of WAITs and RUNs: each RUN at the time of the wake its WAIT consumes."""
    seen, out, t = {}, [], task["t"]
    for op in task["program"]:
        if op["op"] == "WAIT":
            k = seen.get(op["channel"], 0)
            seen[op["channel"]] = k + 1
            t = wakes[(task["id"], op["channel"])][k]
        elif op["op"] == "RUN":
            out.append((t, op["us"]))
        elif op["op"] != "EXIT":
            sys.exit(f"{task['id']}: {op['op']} beside the job; its RUNs have no release time of their own")
    return out


def end_bound(artifact, job_id):
    """{a, C, S, B, others_after, bound, fixed_point} in µs for the job `job_id` of a compiled artifact."""
    wakes = {}
    for e in artifact["events"]:
        if e["op"] == "wake":
            wakes.setdefault((e["target"], e["channel"]), []).append(e["t"])
    for v in wakes.values():
        v.sort()
    tasks = [e for e in artifact["events"] if e["op"] == "arrive"]
    job = next(t for t in tasks if t["id"] == job_id)
    a = job["t"]
    C = sum(o["us"] for o in job["program"] if o["op"] == "RUN")
    S = sum(o["us"] for o in job["program"] if o["op"] == "SLEEP")
    rel = sorted(r for t in tasks if t["id"] != job_id for r in releases(t, wakes))
    ts = [t for t, _ in rel]
    cum = [0]
    for _, u in rel:
        cum.append(cum[-1] + u)
    i_a = bisect.bisect_left(ts, a)
    # the busy period that holds a starts at a release s: what came in over [s, a) less the time to a
    B = max([0] + [cum[i_a] - cum[i] - (a - ts[i]) for i in range(i_a)])
    E = a + C + S + B
    while True:
        nxt = a + C + S + B + cum[bisect.bisect_right(ts, E)] - cum[i_a]
        if nxt == E:
            break
        E = nxt
    after = cum[-1] - cum[i_a]
    return {"a": a, "C": C, "S": S, "B": B, "others_after": after, "bound": a + C + S + after, "fixed_point": E}


def main():
    r = end_bound(json.load(open(sys.argv[1])), sys.argv[2])
    s = {k: v / 1e6 for k, v in r.items()}
    line = (f"{sys.argv[2]}: arrival {s['a']:.3f} s + CPU {s['C']:.6f} s + blocks {s['S']:.6f} s + the other tasks' "
            f"{s['others_after']:.6f} s after it = {s['bound']:.6f} s; backlog at the arrival {s['B']:.6f} s; "
            f"fixed point {s['fixed_point']:.6f} s")
    if len(sys.argv) > 3:
        line += f"; margin to {float(sys.argv[3]):g} s: {float(sys.argv[3]) - s['bound']:.6f} s"
    print(line)


if __name__ == "__main__":
    main()
