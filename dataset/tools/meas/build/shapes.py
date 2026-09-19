"""The readings of the 9.6 build campaign that the fold-in carries beyond method §5's per-role tables (changelog
D16, D19–D23; campaign/method.md §8, the 2026-09-19 entries).

- runs_between_blocks, share_past_slice, program_gaps: a bound program's runs between voluntary blocks, the share of
  its CPU past a scheduler slice, and its program-level gaps (D21, D22);
- tracker_job_end: the end of `tracker`'s rescan, the miner's own `Idle` status (D16);
- member_steps: the CPU of each structural step of an object job's members (D19, D20).

Segments are analyze.Seg: times in s, run and delay in ms, state the timehist sched-out state.
"""

import bisect
import datetime
import re
from collections import defaultdict

BOOT_SLICE_MS = 10.0      # MLFQ timeslice_us 10 000 at boot (docs/recognition-vocabulary.md §2; ostep §8.2)
VOLUNTARY = ("S", "D")    # a sched-out asleep: the task gave the CPU back on its own (batch-class rule B1)
OBJECT_MEMBERS = ("as", "cc1", "fixdep", "gcc", "rm", "sh")   # D19's object job, sorted as jobs_of sorts roles
STATUS = re.compile(r"^Tracker-Message: (\d\d):(\d\d):(\d\d)\.(\d{3}): \(Miner:'TrackerMinerFiles'\) "
                    r"set property:'status' to '(.*)'$")


def runs_between_blocks(rows):
    """Per thread, the CPU from one voluntary block to the next, in ms: segments are summed until one ends asleep
    (S or D); a preemption (R) does not end the run; a thread's last run ends at its exit. rows: one program's
    segments on the measured CPU."""
    acc, out = defaultdict(float), []
    for s in sorted(rows, key=lambda s: s.t_in):
        acc[s.tid] += s.run
        if s.state[:1] in VOLUNTARY:
            out.append(acc.pop(s.tid))
    out.extend(v for v in acc.values() if v > 0)
    return out


def share_past_slice(runs_ms, slice_ms=BOOT_SLICE_MS):
    """The share of the CPU in runs_ms spent past slice_ms since the run's voluntary block — what the batch-class rule
    B1 (docs/memos/2026-09-09-batch-class-rule-for-the-simulator.md) and MLFQ demotion act on. None without CPU."""
    total = sum(runs_ms)
    return sum(max(0.0, r - slice_ms) for r in runs_ms) / total if total else None


def program_gaps(rows, start, end):
    """The intervals within [start, end] (s) in which no thread of the program is on the CPU or runnable, in ms. A
    thread is busy from t_wake (runnable: t_in less its scheduling delay) to t_end, and after a preemption (sched-out
    in R) until its next t_in."""
    by_tid = defaultdict(list)
    for s in rows:
        by_tid[s.tid].append(s)
    spans = []
    for ss in by_tid.values():
        ss.sort(key=lambda s: s.t_in)
        for i, s in enumerate(ss):
            spans.append((s.t_wake, s.t_end))
            if s.state[:1] == "R" and i + 1 < len(ss):
                spans.append((s.t_end, ss[i + 1].t_in))
    gaps, edge = [], start
    for a, b in sorted(spans):
        a, b = max(a, start), min(b, end)
        if b <= a:
            continue
        if a > edge:
            gaps.append((a - edge) * 1000.0)
        edge = max(edge, b)
    if end > edge:
        gaps.append((end - edge) * 1000.0)
    return gaps
