"""The readings of the 9.6 build campaign that the fold-in carries beyond method §5's per-role tables (changelog
D16, D19–D23; campaign/method.md §8, the 2026-09-19 entries).

- runs_between_blocks, share_past_slice, blocks_after_runs, program_gaps: a bound program's runs between voluntary
  blocks, the share of its CPU past a scheduler slice, the block after each run and its program-level gaps (D21,
  D22, D25);
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


def _gap_spans(rows, start, end):
    """The program-level gaps within [start, end] as (from, to) in s: no thread of the program on the CPU or runnable.
    A thread is busy from t_wake (runnable: t_in less its scheduling delay) to t_end, and after a preemption (sched-out
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
            gaps.append((edge, a))
        edge = max(edge, b)
    if end > edge:
        gaps.append((edge, end))
    return gaps


def program_gaps(rows, start, end):
    """The program-level gaps within [start, end] (s), in ms (reported beside the block table, D25)."""
    return [(b - a) * 1000.0 for a, b in _gap_spans(rows, start, end)]


def blocks_after_runs(rows, start, end):
    """The block that follows each run between voluntary blocks (D25), in ms, in time order: the program-level gap
    starting where the run's thread went to sleep, zero when another thread of the program runs on or is runnable."""
    starts = {round(a, 7): (b - a) * 1000.0 for a, b in _gap_spans(rows, start, end)}
    return [starts.get(round(min(s.t_end, end), 7), 0.0)
            for s in sorted(rows, key=lambda s: s.t_in) if s.state[:1] in VOLUNTARY]


def tracker_job_end(lines, start_mono_ns, start_real_ns):
    """The end of the rescan (D16) on CLOCK_MONOTONIC, in s: the miner's first `Idle` status after its last status
    that is not `Idle`. The log stamps the time of day in UTC; the phase's start edge (edges.jsonl: mono_ns, real_ns)
    gives the date and the offset between the clocks. None when the miner never left `Idle`."""
    st = []
    for line in lines:
        m = STATUS.match(line.rstrip("\n"))
        if m:
            h, mi, sec, ms, status = m.groups()
            st.append((int(h) * 3600 + int(mi) * 60 + int(sec) + int(ms) / 1000.0, status))
    busy = [i for i, (_, status) in enumerate(st) if status != "Idle"]
    if not busy:
        return None
    end = next((tod for tod, status in st[busy[-1] + 1:] if status == "Idle"), None)
    if end is None:
        return None
    t0 = datetime.datetime.fromtimestamp(start_real_ns / 1e9, tz=datetime.timezone.utc)
    real = t0.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(seconds=end)
    if real < t0 - datetime.timedelta(hours=12):
        real += datetime.timedelta(days=1)
    return start_mono_ns / 1e9 + (real - t0).total_seconds()


def member_steps(jobs, role, parent_pid, segs_by_pid, fork_time, exit_time):
    """For the object jobs with exactly D19's six members: each member's CPU per structural step, in ms, keyed
    "<role> <k>/<n>" — the member's segments on the measured CPU grouped by the exits of its own children (D20: `sh`
    four steps around `gcc`, `fixdep`, `rm`; `gcc` three around `cc1`, `as`; a childless member one) — and the
    parents' child orders by fork time, counted. jobs: analyze.jobs_of's list; segs_by_pid: pid -> that process's
    segments on the measured CPU; fork_time, exit_time: pid -> s."""
    kids = defaultdict(list)
    for c, p in parent_pid.items():
        kids[p].append(c)
    steps, order, n = defaultdict(list), defaultdict(int), 0
    for j in jobs:
        if j["kind"] != "object" or tuple(j["roles"]) != OBJECT_MEMBERS:
            continue
        n += 1
        members = set(j["members"])
        for x in j["members"]:
            ch = sorted((c for c in kids.get(x, ()) if c in members), key=lambda c: fork_time.get(c, 0.0))
            bounds = sorted(exit_time[c] for c in ch if c in exit_time)
            acc = [0.0] * (len(bounds) + 1)
            for sg in segs_by_pid.get(x, ()):
                acc[bisect.bisect_right(bounds, sg.t_in)] += sg.run
            for k, v in enumerate(acc):
                steps[f"{role[x]} {k + 1}/{len(acc)}"].append(v)
            if ch:
                order[f"{role[x]}: " + " ".join(role[c] for c in ch)] += 1
    return {"jobs": n, "steps": dict(steps), "child_order": dict(order)}
