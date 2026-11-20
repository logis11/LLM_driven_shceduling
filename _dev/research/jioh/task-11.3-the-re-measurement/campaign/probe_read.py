#!/usr/bin/env python3
"""The probe's reading (method §5, 2026-11-20, the probe): per probe repeat, the training run's voluntary blocks —
how many, and what ended each, the waker of each wake of the training process in the phase's wakeup rows — beside the
kernel, the transparent-hugepage mode by default and before the phase, the huge pages fault-allocated and collapsed
in the phase, the CPU total and the two block values; and the criterion committed before the probe ran.

    python3 probe_read.py <pool folder> <pooled.json> [--out probe.json]

<pool folder> is the folder `dataset/tools/meas/loop/pool_runs.py background/mnist --since <the probe's run>`
downloaded into (one folder per run, one per artifact); <pooled.json> its pooled record. The form reproduces when
every repeat has `enabled` `[always] madvise never` before the phase, holds 11–24 voluntary blocks — the original
campaign's range — and has every block ended by `khugepaged` but the two sleeps at the start."""
import argparse
import collections
import gzip
import json
import pathlib
import re
import sys

WAKE = re.compile(r"^\s*([0-9.]+)\s+\[(\d+)\]\s+(.+?)\s+awakened: python\[(\d+)\]\s*$")
BLOCKS = (11, 24)          # the original campaign's six repeats, 11–24 voluntary blocks a repeat
START_SLEEPS = 2           # the two sleeps of about 102 µs at the start, every repeat of the original


def kv(path):
    out = {}
    for line in path.read_text(errors="replace").splitlines():
        k, _, v = line.partition("=")
        out[k] = v
    return out


def wakers(path):
    """{pid: Counter(waker comm)} over the phase's wakeup rows of a `python` process."""
    by = collections.defaultdict(collections.Counter)
    with gzip.open(path, "rt", errors="replace") as f:
        for line in f:
            m = WAKE.match(line)
            if m:
                comm = re.sub(r"\[[0-9/]+\]$", "", m.group(3).strip())
                by[m.group(4)][comm] += 1
    return by


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("pool")
    ap.add_argument("pooled")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    pooled = json.loads(pathlib.Path(args.pooled).read_text())["runs"]["mnist"]
    ph = pooled["phases"]["mnist-train"]
    rows = []
    for art in sorted(pathlib.Path(args.pool).glob("*/meas-background-mnist-r*-*")):
        k = re.search(r"-r(\d+)-", art.name).group(1)
        if k not in {str(x) for x in pooled["repeats"]}:
            continue
        r = kv(art / "report.kv")
        by = wakers(art / "perf.mnist-train.wakeups.txt.gz")
        pid, ws = max(by.items(), key=lambda kv_: sum(kv_[1].values())) if by else (None, collections.Counter())
        blocks = sum(ws.values())
        khugepaged = ws.get("khugepaged", 0)
        sleeps = ph["all"]["sleep_us"]["repeat_n"].get(k, 0)
        ok = (r.get("thp.before.enabled") == "[always] madvise never" and BLOCKS[0] <= blocks <= BLOCKS[1]
              and khugepaged == blocks - START_SLEEPS and sleeps == START_SLEEPS)
        rows.append({"repeat": int(k), "run": art.parent.name, "kernel": r.get("kernel") or r.get("machine.kernel"),
                     "thp_default": r.get("thp.default.enabled"), "thp_before": r.get("thp.before.enabled"),
                     "thp_fault_alloc": int(r.get("thp.after.thp_fault_alloc", 0) or 0) - int(r.get("thp.before.thp_fault_alloc", 0) or 0),
                     "thp_collapse_alloc": int(r.get("thp.after.thp_collapse_alloc", 0) or 0) - int(r.get("thp.before.thp_collapse_alloc", 0) or 0),
                     "pid": pid, "blocks": blocks, "start_sleeps": sleeps, "wakers": dict(ws.most_common()),
                     "cpu_total_s": ph["program_cpu_us"][k] / 1e6,
                     "run_between_blocks_mean_s": ph["all"]["batch_run_us"]["repeat_mean"][k] / 1e6,
                     "block_per_run_mean_us": ph["all"]["batch_block_us"]["repeat_mean"][k],
                     "reproduces": ok})
    out = {"criterion": {"thp_before": "[always] madvise never", "blocks": list(BLOCKS),
                         "ended_by": "khugepaged, every block but the two sleeps at the start"},
           "repeats": rows, "form_reproduces": bool(rows) and all(x["reproduces"] for x in rows)}
    text = json.dumps(out, indent=2) + "\n"
    if args.out:
        pathlib.Path(args.out).write_text(text)
    for x in rows:
        print(f"r{x['repeat']}: {x['kernel']} thp {x['thp_default']} -> {x['thp_before']}; blocks {x['blocks']} "
              f"{x['wakers']}; CPU {x['cpu_total_s']:.1f} s, run {x['run_between_blocks_mean_s']:.3f} s, "
              f"block {x['block_per_run_mean_us']:.1f} us; {'reproduces' if x['reproduces'] else 'does not'}")
    print("the form reproduces" if out["form_reproduces"] else "the form does not reproduce")
    return 0


if __name__ == "__main__":
    sys.exit(main())
