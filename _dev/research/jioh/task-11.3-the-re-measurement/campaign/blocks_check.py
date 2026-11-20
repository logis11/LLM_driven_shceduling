#!/usr/bin/env python3
"""Every voluntary block the fold leaves (method §5, the fold), per repeat: what ended it — the waker of its wake, the
thread's last wakeup row after the block's schedule-in and at or before the next — beside the count of waits folded.

    python3 campaign/blocks_check.py <pool folder> [--out blocks-check.json]   (from the repository root)

<pool folder> is the folder `dataset/tools/meas/loop/pool_runs.py background/mnist --since 229` downloaded into."""
import argparse
import bisect
import collections
import concurrent.futures
import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "dataset" / "tools"))
from meas.background import analyze as A  # noqa: E402
from meas.build import shapes  # noqa: E402

MEAS_CPU = 3


def one(art):
    segs = A.load_segments(str(art / "perf.mnist-train.timehist.txt.gz"))
    wk = A.load_wakers(str(art / "perf.mnist-train.wakeups.txt.gz"))
    tid = collections.Counter(s.tid for s in segs if s.comm == "python" and s.cpu == MEAS_CPU).most_common(1)[0][0]
    rows = sorted((s for s in segs if s.tid == tid and s.cpu == MEAS_CPU), key=lambda s: s.t_in)
    folded = A.agent_woken(rows, wk)
    times = [t for t, _ in wk.get(tid, [])]
    ended = collections.Counter()
    for s, n in zip(rows, rows[1:]):
        if s.state[:1] in shapes.VOLUNTARY and (s.tid, s.t_in) not in folded:
            i = bisect.bisect_left(times, n.t_in + 1e-9) - 1
            ended[wk[tid][i][1] if i >= 0 and times[i] > s.t_in else "no row"] += 1
    return {"repeat": int(re.search(r"-r(\d+)-", art.name).group(1)), "run": art.parent.name, "folded": len(folded),
            "blocks": sum(ended.values()), "ended_by": dict(ended)}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("pool")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    arts = sorted(pathlib.Path(args.pool).glob("*/meas-background-mnist-r*-full"))
    with concurrent.futures.ProcessPoolExecutor(max_workers=6) as pool:
        rows = sorted(pool.map(one, arts), key=lambda r: r["repeat"])
    other = [r for r in rows if set(r["ended_by"]) - {"khugepaged", "swapper"} or r["ended_by"].get("swapper", 0) != 2]
    out = {"repeats": len(rows), "every_block_khugepaged_but_two_start_sleeps": not other, "exceptions": other,
           "khugepaged_per_repeat": [min(r["ended_by"].get("khugepaged", 0) for r in rows),
                                     max(r["ended_by"].get("khugepaged", 0) for r in rows)],
           "rows": rows}
    if args.out:
        pathlib.Path(args.out).write_text(json.dumps(out, indent=2) + "\n")
    print(f"{len(rows)} repeats; every block khugepaged's but the two start sleeps: {not other}; "
          f"khugepaged per repeat {out['khugepaged_per_repeat']}; exceptions {[(r['repeat'], r['ended_by']) for r in other]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
